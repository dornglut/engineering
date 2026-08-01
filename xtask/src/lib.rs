use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Component, Path, PathBuf};

const TEXT_SUFFIXES: &[&str] = &["md", "markdown", "yml", "yaml", "txt", "py", "toml", "json"];
const ADR_STATUSES: &[&str] = &["proposed", "accepted", "superseded", "rejected"];
const INITIATIVE_STATUSES: &[&str] = &["proposed", "active", "completed", "cancelled"];
const RUST_WORKFLOW: &str = "dornglut/github-workflows/.github/workflows/reusable-rust-cargo-validate.yml@624cb41adeed21a6461eb838bc7330bd0a5079fd";

pub fn validate(root: &Path) -> Result<(), Vec<String>> {
    let mut failures = BTreeSet::new();
    required_paths(root, &mut failures);
    workflow(root, &mut failures);
    for path in files(root, &mut failures) {
        text_file(root, &path, &mut failures);
    }
    authority_content(root, &mut failures);
    adrs(root, &mut failures);
    initiatives(root, &mut failures);
    standard_markers(root, &mut failures);
    if failures.is_empty() {
        Ok(())
    } else {
        Err(failures.into_iter().collect())
    }
}

fn fail(failures: &mut BTreeSet<String>, message: impl Into<String>) {
    failures.insert(message.into());
}
fn rel(root: &Path, path: &Path) -> String {
    let relative = path.strip_prefix(root).unwrap_or(path);
    relative
        .to_str()
        .map(|value| value.replace('\\', "/"))
        .unwrap_or_else(|| format!("{relative:?}"))
}
fn require_utf8_path(root: &Path, path: &Path, failures: &mut BTreeSet<String>) -> bool {
    if path.strip_prefix(root).unwrap_or(path).to_str().is_some() {
        true
    } else {
        fail(
            failures,
            format!(
                "{}: validator-supported paths must be valid UTF-8",
                rel(root, path)
            ),
        );
        false
    }
}
fn extension_is(path: &Path, expected: &str) -> bool {
    path.extension()
        .and_then(|value| value.to_str())
        .is_some_and(|value| value.eq_ignore_ascii_case(expected))
}
fn is_markdown(path: &Path) -> bool {
    extension_is(path, "md") || extension_is(path, "markdown")
}

fn files(root: &Path, failures: &mut BTreeSet<String>) -> Vec<PathBuf> {
    let mut result = Vec::new();
    collect(root, root, &mut result, failures);
    result.sort();
    result
}
fn collect(
    root: &Path,
    directory: &Path,
    output: &mut Vec<PathBuf>,
    failures: &mut BTreeSet<String>,
) {
    let Ok(entries) = fs::read_dir(directory) else {
        fail(
            failures,
            format!("{}: failed to read directory", rel(root, directory)),
        );
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if path.file_name().and_then(|name| name.to_str()) == Some(".git")
            || path == root.join("target")
        {
            continue;
        }
        let Ok(kind) = entry.file_type() else {
            fail(
                failures,
                format!("{}: failed to inspect path", rel(root, &path)),
            );
            continue;
        };
        if !require_utf8_path(root, &path, failures) {
            continue;
        }
        if kind.is_symlink() {
            fail(
                failures,
                format!("{}: symlinks are not supported", rel(root, &path)),
            );
        } else if kind.is_dir() {
            collect(root, &path, output, failures);
        } else if kind.is_file() {
            output.push(path);
        }
    }
}
fn read(root: &Path, path: &Path, failures: &mut BTreeSet<String>) -> Option<String> {
    fs::read_to_string(path)
        .map_err(|error| {
            fail(
                failures,
                format!("{}: failed to read UTF-8 text: {error}", rel(root, path)),
            )
        })
        .ok()
}

fn required_paths(root: &Path, failures: &mut BTreeSet<String>) {
    let manifest = root.join("validation-required-files.txt");
    let Some(contents) = read(root, &manifest, failures) else {
        return;
    };
    for line in contents
        .lines()
        .map(str::trim)
        .filter(|line| !line.is_empty() && !line.starts_with('#'))
    {
        if !root.join(line).exists() {
            fail(failures, format!("{line}: required path is missing"));
        }
    }
    for path in [
        "governance/README.md",
        "governance/authority-model.md",
        "governance/repository-lifecycle.md",
        "governance/decision-records.md",
        "architecture/README.md",
        "architecture/repository-system.md",
        "architecture/runen-framework-map.md",
        "portfolio/README.md",
        "scripts/validate.py",
    ] {
        if root.join(path).exists() {
            fail(
                failures,
                format!("{path}: retired authority path must not exist"),
            );
        }
    }
}

fn workflow(root: &Path, failures: &mut BTreeSet<String>) {
    let directory = root.join(".github/workflows");
    let mut actual = BTreeSet::new();
    match fs::read_dir(&directory) {
        Ok(entries) => {
            for entry in entries {
                match entry {
                    Ok(entry) => {
                        let path = entry.path();
                        if !require_utf8_path(root, &path, failures) {
                            continue;
                        }
                        if extension_is(&path, "yml") || extension_is(&path, "yaml") {
                            actual.insert(rel(root, &path));
                        }
                    }
                    Err(error) => fail(
                        failures,
                        format!(
                            "{}: failed to read workflow entry: {error}",
                            rel(root, &directory)
                        ),
                    ),
                }
            }
        }
        Err(error) => fail(
            failures,
            format!(
                "{}: failed to read workflow directory: {error}",
                rel(root, &directory)
            ),
        ),
    }
    let expected = BTreeSet::from([".github/workflows/validate.yml".to_owned()]);
    if actual != expected {
        fail(
            failures,
            format!(
                "workflow inventory must be .github/workflows/validate.yml; found {}",
                actual.iter().cloned().collect::<Vec<_>>().join(", ")
            ),
        );
    }
    let Some(contents) = read(root, &directory.join("validate.yml"), failures) else {
        return;
    };
    let expected = format!(
        "name: Validate\non:\n  pull_request:\n  push:\n    branches:\n      - main\npermissions:\n  contents: read\njobs:\n  validate:\n    uses: {RUST_WORKFLOW}"
    );
    let normalized = contents
        .lines()
        .filter(|line| !line.trim().is_empty() && !line.trim_start().starts_with('#'))
        .map(str::trim_end)
        .collect::<Vec<_>>()
        .join("\n");
    if normalized != expected {
        fail(
            failures,
            ".github/workflows/validate.yml: must be the single read-only immutable Rust validation caller",
        );
    }
}

fn text_file(root: &Path, path: &Path, failures: &mut BTreeSet<String>) {
    let text = path
        .extension()
        .and_then(|value| value.to_str())
        .is_some_and(|value| {
            TEXT_SUFFIXES
                .iter()
                .any(|suffix| value.eq_ignore_ascii_case(suffix))
        })
        || path.file_name().and_then(|value| value.to_str()) == Some("CODEOWNERS");
    if !text {
        return;
    }
    let Ok(bytes) = fs::read(path) else {
        fail(failures, format!("{}: failed to read", rel(root, path)));
        return;
    };
    if bytes.contains(&0) {
        fail(
            failures,
            format!("{}: contains a NUL byte", rel(root, path)),
        );
        return;
    }
    let Ok(contents) = String::from_utf8(bytes) else {
        fail(failures, format!("{}: is not valid UTF-8", rel(root, path)));
        return;
    };
    if !contents.is_empty() && !contents.ends_with('\n') {
        fail(
            failures,
            format!("{}: must end with a newline", rel(root, path)),
        );
    }
    for (number, line) in contents.lines().enumerate() {
        if line.ends_with([' ', '\t']) {
            fail(
                failures,
                format!("{}:{}: trailing whitespace", rel(root, path), number + 1),
            );
        }
        if line.contains('\t') {
            fail(
                failures,
                format!("{}:{}: tab character", rel(root, path), number + 1),
            );
        }
    }
    if is_markdown(path) {
        links(root, path, &contents, failures);
    }
}
fn links(root: &Path, path: &Path, contents: &str, failures: &mut BTreeSet<String>) {
    for raw in markdown_link_targets(contents) {
        let raw = raw.trim();
        let target = raw
            .split_whitespace()
            .next()
            .unwrap_or("")
            .trim_matches(['<', '>']);
        if target.is_empty()
            || target.starts_with('#')
            || target.starts_with("http://")
            || target.starts_with("https://")
            || target.starts_with("mailto:")
        {
            continue;
        }
        let target = target.split(['#', '?']).next().unwrap_or("");
        if target.contains('\\') {
            fail(
                failures,
                format!(
                    "{}: link uses a non-portable path separator: {raw}",
                    rel(root, path)
                ),
            );
            continue;
        }
        let Some(target) = percent_decode(target) else {
            fail(
                failures,
                format!("{}: link target is not valid UTF-8: {raw}", rel(root, path)),
            );
            continue;
        };
        let base = path
            .parent()
            .unwrap_or(root)
            .strip_prefix(root)
            .unwrap_or(Path::new(""));
        let Some(joined) = normalize_relative(&base.join(target)) else {
            fail(
                failures,
                format!("{}: link escapes repository: {raw}", rel(root, path)),
            );
            continue;
        };
        if !root.join(joined).exists() {
            fail(
                failures,
                format!("{}: broken relative link: {raw}", rel(root, path)),
            );
        }
    }
}
fn markdown_link_targets(contents: &str) -> Vec<&str> {
    let mut targets = Vec::new();
    let mut offset = 0;
    while let Some(opening) = contents[offset..].find('[') {
        let opening = offset + opening;
        let label_start = opening + 1;
        let mut nested_opening = None;
        let mut closing = None;
        for (index, character) in contents[label_start..].char_indices() {
            match character {
                '[' => {
                    nested_opening = Some(label_start + index);
                    break;
                }
                ']' => {
                    closing = Some(label_start + index);
                    break;
                }
                _ => {}
            }
        }
        if let Some(nested_opening) = nested_opening {
            offset = nested_opening;
            continue;
        }
        let Some(closing) = closing else {
            break;
        };
        let target_start = closing + 2;
        if !contents[closing..].starts_with("](") {
            offset = closing + 1;
            continue;
        }
        let mut nested_opening = None;
        let mut closing_parenthesis = None;
        for (index, character) in contents[target_start..].char_indices() {
            match character {
                '[' => {
                    nested_opening = Some(target_start + index);
                    break;
                }
                ')' => {
                    closing_parenthesis = Some(target_start + index);
                    break;
                }
                _ => {}
            }
        }
        if let Some(nested_opening) = nested_opening {
            offset = nested_opening;
            continue;
        }
        let Some(closing_parenthesis) = closing_parenthesis else {
            break;
        };
        targets.push(&contents[target_start..closing_parenthesis]);
        offset = closing_parenthesis + 1;
    }
    targets
}
fn percent_decode(value: &str) -> Option<String> {
    let bytes = value.as_bytes();
    let mut output = Vec::new();
    let mut index = 0;
    while index < bytes.len() {
        if bytes[index] == b'%'
            && index + 2 < bytes.len()
            && let (Some(a), Some(b)) = (hex(bytes[index + 1]), hex(bytes[index + 2]))
        {
            output.push(a * 16 + b);
            index += 3;
            continue;
        }
        output.push(bytes[index]);
        index += 1;
    }
    String::from_utf8(output).ok()
}
fn hex(value: u8) -> Option<u8> {
    match value {
        b'0'..=b'9' => Some(value - b'0'),
        b'a'..=b'f' => Some(value - b'a' + 10),
        b'A'..=b'F' => Some(value - b'A' + 10),
        _ => None,
    }
}
fn normalize_relative(path: &Path) -> Option<PathBuf> {
    let mut result = PathBuf::new();
    for component in path.components() {
        match component {
            Component::Normal(value) => result.push(value),
            Component::CurDir => {}
            Component::ParentDir => {
                if !result.pop() {
                    return None;
                }
            }
            Component::RootDir | Component::Prefix(_) => return None,
        }
    }
    Some(result)
}

fn sections(contents: &str) -> BTreeMap<String, String> {
    let mut result: BTreeMap<String, Vec<&str>> = BTreeMap::new();
    let mut current = None;
    for line in contents.lines() {
        if let Some(name) = line.strip_prefix("## ") {
            current = Some(name.trim().to_owned());
            result.entry(name.trim().to_owned()).or_default();
        } else if let Some(name) = &current {
            result.entry(name.clone()).or_default().push(line);
        }
    }
    result
        .into_iter()
        .map(|(name, lines)| (name, lines.join("\n").trim().to_owned()))
        .collect()
}
fn metadata(contents: &str) -> BTreeMap<String, String> {
    contents
        .lines()
        .filter_map(|line| {
            let line = line.strip_prefix("- ")?;
            let (key, value) = line.split_once(':')?;
            key.chars()
                .all(|value| value.is_ascii_alphabetic() || value == ' ')
                .then(|| (key.to_owned(), value.trim().to_owned()))
        })
        .collect()
}

fn authority_content(root: &Path, failures: &mut BTreeSet<String>) {
    for path in files(root, failures) {
        if !is_markdown(&path) {
            continue;
        }
        let relative = rel(root, &path);
        let Some(contents) = read(root, &path, failures) else {
            continue;
        };
        let lowered = contents.to_lowercase();
        if [
            "README.md",
            "AGENTS.md",
            "governance/",
            "standards/",
            "architecture/",
        ]
        .iter()
        .any(|prefix| relative == *prefix || relative.starts_with(prefix))
        {
            for token in ["github.com/crystonix/", "`crystonix/", "crystonix/runen"] {
                if lowered.contains(token) {
                    fail(
                        failures,
                        format!(
                            "{relative}: active authority contains historical owner token {token:?}"
                        ),
                    );
                }
            }
            for (token, label) in [
                ("refs/heads/", "mutable branch ref"),
                ("github.com/dornglut/engineering/pull/", "pull-request URL"),
                ("actions/runs/", "workflow-run URL"),
                ("workflow run:", "workflow-run state"),
                ("head sha:", "head SHA state"),
            ] {
                if lowered.contains(token) {
                    fail(
                        failures,
                        format!(
                            "{relative}: durable authority contains volatile {label}: {token:?}"
                        ),
                    );
                }
            }
        }
    }
}

fn adrs(root: &Path, failures: &mut BTreeSet<String>) {
    let directory = root.join("adrs");
    let Some(index) = read(root, &directory.join("README.md"), failures) else {
        return;
    };
    let indexed = sections(&index);
    let mut records = BTreeMap::new();
    let mut numbers = Vec::new();
    let Ok(entries) = fs::read_dir(&directory) else {
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        let filename = path
            .file_name()
            .and_then(|value| value.to_str())
            .unwrap_or("");
        if filename == "README.md" || !extension_is(&path, "md") {
            continue;
        }
        let Some(number) = adr_number(filename) else {
            fail(failures, format!("adrs/{filename}: invalid ADR filename"));
            continue;
        };
        numbers.push(number);
        let Some(contents) = read(root, &path, failures) else {
            continue;
        };
        if !contents.starts_with(&format!("# ADR {number:04}: ")) {
            fail(
                failures,
                format!("adrs/{filename}: header must start with '# ADR {number:04}: '"),
            );
        }
        let values = metadata(&contents);
        for key in ["Status", "Date", "Owner", "Scope"] {
            if !values.contains_key(key) {
                fail(
                    failures,
                    format!("adrs/{filename}: missing metadata: {key}"),
                );
            }
        }
        let status = values
            .get("Status")
            .map(String::as_str)
            .unwrap_or("")
            .to_lowercase();
        if !ADR_STATUSES.contains(&status.as_str()) {
            fail(
                failures,
                format!("adrs/{filename}: invalid status {status:?}"),
            );
        }
        let document_sections = sections(&contents);
        let required: &[&str] = if number == 1 {
            &["Context", "Decision", "Consequences"]
        } else {
            &[
                "Context",
                "Decision",
                "Alternatives considered",
                "Consequences",
                "Affected repositories",
                "Adoption or migration",
                "Supersedes",
                "Superseded by",
            ]
        };
        for section in required {
            if !document_sections.contains_key(*section) {
                fail(
                    failures,
                    format!("adrs/{filename}: missing sections: {section}"),
                );
            }
        }
        let link = format!("({filename})");
        if index.matches(&link).count() != 1 {
            fail(
                failures,
                format!("adrs/{filename}: ADR index must link this file exactly once"),
            );
        }
        let wanted = match status.as_str() {
            "accepted" => "Current",
            "proposed" => "Proposed",
            "superseded" => "Superseded",
            "rejected" => "Rejected",
            _ => "",
        };
        if !wanted.is_empty() && !indexed.get(wanted).is_some_and(|part| part.contains(&link)) {
            fail(
                failures,
                format!(
                    "adrs/{filename}: status {status:?} does not match index section {wanted:?}"
                ),
            );
        }
        records.insert(filename.to_owned(), (status, document_sections));
    }
    for target in markdown_link_targets(&index) {
        let target = target.split_whitespace().next().unwrap_or("");
        if looks_like_adr_filename(target) && adr_number(target).is_none() {
            fail(
                failures,
                format!("adrs/README.md: invalid ADR index target: {target}"),
            );
        }
    }
    numbers.sort_unstable();
    if let Some(maximum) = numbers.last().copied() {
        let expected: Vec<_> = (1..=maximum).collect();
        if numbers != expected {
            fail(
                failures,
                format!(
                    "adrs: numbering must be sequential; expected {expected:?}, found {numbers:?}"
                ),
            );
        }
    }
    for (filename, (status, document_sections)) in &records {
        let supersedes = adr_links(
            filename,
            "Supersedes",
            document_sections
                .get("Supersedes")
                .map(String::as_str)
                .unwrap_or(""),
            failures,
        );
        let superseded_by = adr_links(
            filename,
            "Superseded by",
            document_sections
                .get("Superseded by")
                .map(String::as_str)
                .unwrap_or(""),
            failures,
        );
        if status == "superseded" && superseded_by.is_empty() {
            fail(
                failures,
                format!("adrs/{filename}: superseded ADR must name its replacement"),
            );
        }
        for target in supersedes.iter().chain(superseded_by.iter()) {
            if !records.contains_key(target) {
                fail(
                    failures,
                    format!("adrs/{filename}: supersession target does not exist: {target}"),
                );
            }
        }
        for target in supersedes {
            if let Some((_, target_sections)) = records.get(&target)
                && !adr_links(
                    filename,
                    "Superseded by",
                    target_sections
                        .get("Superseded by")
                        .map(String::as_str)
                        .unwrap_or(""),
                    failures,
                )
                .contains(filename)
            {
                fail(
                    failures,
                    format!("adrs/{filename}: supersession link to {target} is not bidirectional"),
                );
            }
        }
        for target in superseded_by {
            if let Some((_, target_sections)) = records.get(&target)
                && !adr_links(
                    filename,
                    "Supersedes",
                    target_sections
                        .get("Supersedes")
                        .map(String::as_str)
                        .unwrap_or(""),
                    failures,
                )
                .contains(filename)
            {
                fail(
                    failures,
                    format!("adrs/{filename}: replacement link to {target} is not bidirectional"),
                );
            }
        }
    }
}
fn adr_number(filename: &str) -> Option<u32> {
    let (number, rest) = filename.split_once('-')?;
    (number.len() == 4
        && number.bytes().all(|value| value.is_ascii_digit())
        && rest.strip_suffix(".md").is_some_and(valid_slug))
    .then(|| number.parse().ok())
    .flatten()
}
fn valid_slug(value: &str) -> bool {
    let mut characters = value.chars();
    characters
        .next()
        .is_some_and(|value| value.is_ascii_lowercase() || value.is_ascii_digit())
        && characters
            .all(|value| value.is_ascii_lowercase() || value.is_ascii_digit() || value == '-')
}
fn looks_like_adr_filename(value: &str) -> bool {
    value.as_bytes().first().is_some_and(u8::is_ascii_digit)
        && value.to_ascii_lowercase().ends_with(".md")
}
fn adr_links(
    filename: &str,
    section: &str,
    text: &str,
    failures: &mut BTreeSet<String>,
) -> BTreeSet<String> {
    let mut links = BTreeSet::new();
    for target in markdown_link_targets(text) {
        let target = target.split_whitespace().next().unwrap_or("");
        if looks_like_adr_filename(target) {
            if adr_number(target).is_some() {
                links.insert(target.to_owned());
            } else {
                fail(
                    failures,
                    format!("adrs/{filename}: invalid ADR {section} target: {target}"),
                );
            }
        }
    }
    links
}

fn initiatives(root: &Path, failures: &mut BTreeSet<String>) {
    let directory = root.join("initiatives");
    let Some(index) = read(root, &directory.join("README.md"), failures) else {
        return;
    };
    let indexed = sections(&index);
    let Ok(entries) = fs::read_dir(&directory) else {
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        let filename = path
            .file_name()
            .and_then(|value| value.to_str())
            .unwrap_or("");
        if filename == "README.md" || !extension_is(&path, "md") {
            continue;
        }
        if !valid_initiative_filename(filename) {
            fail(
                failures,
                format!("initiatives/{filename}: invalid initiative filename"),
            );
            continue;
        }
        let Some(contents) = read(root, &path, failures) else {
            continue;
        };
        let values = metadata(&contents);
        for key in [
            "Status",
            "Owner",
            "Opened",
            "Closed",
            "Owning issue",
            "Decision authority",
        ] {
            if !values.contains_key(key) {
                fail(
                    failures,
                    format!("initiatives/{filename}: missing metadata {key:?}"),
                );
            }
        }
        let status = values
            .get("Status")
            .map(String::as_str)
            .unwrap_or("")
            .to_lowercase();
        if !INITIATIVE_STATUSES.contains(&status.as_str()) {
            fail(
                failures,
                format!("initiatives/{filename}: invalid status {status:?}"),
            );
        }
        let link = format!("({filename})");
        if index.matches(&link).count() != 1 {
            fail(
                failures,
                format!(
                    "initiatives/{filename}: initiative index must link this file exactly once"
                ),
            );
        }
        let wanted = match status.as_str() {
            "proposed" => "Proposed",
            "active" => "Active",
            "completed" | "cancelled" => "Closed",
            _ => "",
        };
        if !wanted.is_empty() && !indexed.get(wanted).is_some_and(|part| part.contains(&link)) {
            fail(
                failures,
                format!(
                    "initiatives/{filename}: status {status:?} does not match index section {wanted:?}"
                ),
            );
        }
        let document_sections = sections(&contents);
        for section in [
            "Outcome",
            "Rationale",
            "Affected repositories",
            "Dependency graph",
            "Acceptance evidence",
            "Sequencing constraints",
            "Linked local issues",
            "Risks and rollback",
            "Closure record",
        ] {
            if !document_sections.contains_key(section) {
                fail(
                    failures,
                    format!("initiatives/{filename}: missing required section {section:?}"),
                );
            }
        }
        let closure = document_sections
            .get("Closure record")
            .map(String::as_str)
            .unwrap_or("")
            .trim();
        let closed = values
            .get("Closed")
            .map(String::as_str)
            .unwrap_or("")
            .trim();
        match status.as_str() {
            "active" => {
                if !closed.is_empty() {
                    fail(
                        failures,
                        format!(
                            "initiatives/{filename}: active initiative must not have a close date"
                        ),
                    );
                }
                if !closure.to_lowercase().starts_with("open") {
                    fail(
                        failures,
                        format!(
                            "initiatives/{filename}: active initiative requires an open closure state"
                        ),
                    );
                }
            }
            "completed" | "cancelled" => {
                if !date(closed) {
                    fail(
                        failures,
                        format!(
                            "initiatives/{filename}: closed initiative requires a YYYY-MM-DD close date"
                        ),
                    );
                }
                if closure.is_empty()
                    || matches!(
                        closure.to_lowercase().as_str(),
                        "open" | "open." | "none" | "none."
                    )
                {
                    fail(
                        failures,
                        format!(
                            "initiatives/{filename}: closed initiative requires a non-open closure record"
                        ),
                    );
                }
            }
            "proposed" if !closed.is_empty() => fail(
                failures,
                format!("initiatives/{filename}: proposed initiative must not have a close date"),
            ),
            _ => {}
        }
        if !date(values.get("Opened").map(String::as_str).unwrap_or("")) {
            fail(
                failures,
                format!("initiatives/{filename}: requires a YYYY-MM-DD opened date"),
            );
        }
        if !issue_link(values.get("Owning issue").map(String::as_str).unwrap_or("")) {
            fail(
                failures,
                format!(
                    "initiatives/{filename}: owning issue must contain a syntactically valid GitHub issue link"
                ),
            );
        }
    }
}
fn valid_initiative_filename(filename: &str) -> bool {
    filename.strip_suffix(".md").is_some_and(valid_slug)
}
fn date(value: &str) -> bool {
    let bytes = value.as_bytes();
    bytes.len() == 10
        && bytes[4] == b'-'
        && bytes[7] == b'-'
        && bytes
            .iter()
            .enumerate()
            .all(|(index, value)| matches!(index, 4 | 7) || value.is_ascii_digit())
}
fn issue_link(value: &str) -> bool {
    let Some(start) = value.find("https://github.com/") else {
        return false;
    };
    let parts: Vec<_> = value[start + 19..]
        .split(|value: char| value == '/' || value == ')' || value.is_whitespace())
        .collect();
    parts.len() >= 4
        && !parts[0].is_empty()
        && !parts[1].is_empty()
        && parts[2] == "issues"
        && parts[3].parse::<u64>().is_ok_and(|number| number > 0)
}

fn standard_markers(root: &Path, failures: &mut BTreeSet<String>) {
    markers(
        root,
        "standards/validation.md",
        &[
            "reviewed feature head",
            "synthetic merge-result evidence",
            "github.event.pull_request.head.sha",
            "explicitly selects the expected revision",
            "git rev-parse head",
            "accepted squash merge",
            "accepted-main push evidence",
            "repository-owned canonical command",
            "compact",
            "bounded diagnostics",
        ],
        failures,
    );
    markers(
        root,
        "standards/repositories.md",
        &[
            "accepted base",
            "reviewed feature head",
            "exact feature head",
            "post-merge revision",
        ],
        failures,
    );
    if let Some(contents) = read(root, &root.join("standards/github.md"), failures) {
        let lower = contents.to_lowercase();
        if lower.contains("reviewed head or merge ref") {
            fail(
                failures,
                "standards/github.md: ambiguous reviewed-head wording is forbidden",
            );
        }
        for marker in [
            "accepted base",
            "reviewed feature head",
            "exact-head validation",
            "accepted squash merge",
        ] {
            if !lower.contains(marker) {
                fail(
                    failures,
                    format!("standards/github.md: missing pull-request evidence marker: {marker}"),
                );
            }
        }
    }
}
fn markers(root: &Path, path: &str, wanted: &[&str], failures: &mut BTreeSet<String>) {
    if let Some(contents) = read(root, &root.join(path), failures) {
        let lower = contents.to_lowercase();
        let missing: Vec<_> = wanted
            .iter()
            .copied()
            .filter(|value| !lower.contains(value))
            .collect();
        if !missing.is_empty() {
            fail(
                failures,
                format!("{path}: missing required markers: {}", missing.join(", ")),
            );
        }
    }
}
