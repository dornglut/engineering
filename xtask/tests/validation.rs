use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::atomic::{AtomicUsize, Ordering};

static NEXT: AtomicUsize = AtomicUsize::new(0);
struct Fixture(PathBuf);
impl Fixture {
    fn new() -> Self {
        let source = Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap();
        let path = std::env::temp_dir().join(format!(
            "dornglut-engineering-validator-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        let _ = fs::remove_dir_all(&path);
        copy_tracked(source, &path);
        Self(path)
    }
    fn replace(&self, path: &str, from: &str, to: &str) {
        let file = self.0.join(path);
        let text = fs::read_to_string(&file).unwrap();
        assert!(text.contains(from));
        fs::write(file, text.replacen(from, to, 1)).unwrap();
    }
    fn write(&self, path: &str, contents: &str) {
        let file = self.0.join(path);
        if let Some(parent) = file.parent() {
            fs::create_dir_all(parent).unwrap();
        }
        fs::write(file, contents).unwrap();
    }
    fn write_bytes(&self, path: &str, contents: &[u8]) {
        let file = self.0.join(path);
        if let Some(parent) = file.parent() {
            fs::create_dir_all(parent).unwrap();
        }
        fs::write(file, contents).unwrap();
    }
    fn errors(&self) -> Vec<String> {
        xtask::validate(&self.0).expect_err("fixture should fail")
    }
    fn fails(self, expected: &str) {
        let errors = self.errors();
        assert!(
            errors.iter().any(|error| error.contains(expected)),
            "expected {expected:?} in {errors:#?}"
        );
    }
    fn passes(self) {
        assert!(xtask::validate(&self.0).is_ok());
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn copy_tracked(source: &Path, destination: &Path) {
    fs::create_dir_all(destination).unwrap();
    let output = Command::new("git")
        .args(["-C"])
        .arg(source)
        .args(["ls-files", "-z"])
        .output()
        .unwrap_or_else(|error| panic!("fixture requires Git-tracked source: {error}"));
    assert!(
        output.status.success(),
        "fixture could not list Git-tracked source: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    let mut paths: Vec<_> = output
        .stdout
        .split(|byte| *byte == 0)
        .filter(|path| !path.is_empty())
        .map(|path| String::from_utf8(path.to_vec()).expect("fixture path must be UTF-8"))
        .collect();
    paths.sort();
    for path in paths {
        let relative = Path::new(&path);
        assert!(
            relative.is_relative()
                && !relative
                    .components()
                    .any(|component| matches!(component, std::path::Component::ParentDir)),
            "fixture rejected non-relative tracked path: {path}"
        );
        let from = source.join(relative);
        assert!(
            fs::symlink_metadata(&from)
                .unwrap_or_else(|error| panic!("fixture source is unavailable at {path}: {error}"))
                .is_file(),
            "fixture source is not a regular file: {path}"
        );
        let to = destination.join(relative);
        fs::create_dir_all(to.parent().unwrap()).unwrap();
        fs::copy(&from, &to)
            .unwrap_or_else(|error| panic!("fixture could not copy {path}: {error}"));
    }
}

#[test]
fn valid_repository_passes() {
    let fixture = Fixture::new();
    assert!(
        fixture
            .0
            .join("adrs/0005-authorize-werkstatt-pilot.md")
            .exists()
    );
    assert!(
        fixture
            .0
            .join("initiatives/provider-neutral-repository-automation.md")
            .exists()
    );
    assert!(xtask::validate(&fixture.0).is_ok());
}

#[test]
fn strict_adr_and_initiative_filenames() {
    for filename in ["0006-bad_name.md", "0006-Bad.md", "0006-bad name.md"] {
        let fixture = Fixture::new();
        fixture.write(&format!("adrs/{filename}"), "# invalid\n");
        fixture.fails("invalid ADR filename");
    }
    for filename in [
        "-pilot.md",
        "_pilot.md",
        "Pilot.md",
        "bad_name.md",
        "bad name.md",
    ] {
        let fixture = Fixture::new();
        fixture.write(&format!("initiatives/{filename}"), "# invalid\n");
        fixture.fails("invalid initiative filename");
    }
    let fixture = Fixture::new();
    fixture.replace(
        "adrs/README.md",
        "(0005-authorize-werkstatt-pilot.md)",
        "(0005-bad_name.md)",
    );
    fixture.fails("adrs/README.md: invalid ADR index target: 0005-bad_name.md");
    let fixture = Fixture::new();
    fixture.replace(
        "adrs/0002-provider-neutral-repository-automation.md",
        "(0003-retire-provider-neutral-repository-automation.md)",
        "(0003-bad_name.md)",
    );
    fixture.fails("invalid ADR Superseded by target: 0003-bad_name.md");
}

#[test]
fn text_and_workflow_suffixes_are_ascii_case_insensitive() {
    let fixture = Fixture::new();
    fs::remove_file(fixture.0.join("README.md")).unwrap();
    fixture.write_bytes("README.MD", b"contains\0nul\n");
    fixture.fails("README.MD: contains a NUL byte");
    let fixture = Fixture::new();
    fixture.write("document.Markdown", "[broken](missing.md)\n");
    fixture.fails("document.Markdown: broken relative link");
    let fixture = Fixture::new();
    fixture.write_bytes("config.TOML", b"invalid \xff\n");
    fixture.fails("config.TOML: is not valid UTF-8");
    let fixture = Fixture::new();
    fixture.write("data.JSON", "{\"ok\": true} \n");
    fixture.fails("data.JSON:1: trailing whitespace");
    let fixture = Fixture::new();
    fixture.write("script.PY", "\tprint('tab')\n");
    fixture.fails("script.PY:1: tab character");
    for filename in ["workflow.YML", "workflow.YAML"] {
        let fixture = Fixture::new();
        fixture.write(&format!(".github/workflows/{filename}"), "name: extra\n");
        fixture.fails("workflow inventory must be .github/workflows/validate.yml");
    }
}

#[test]
fn markdown_link_scanner_recovers_and_excludes_external_targets() {
    let fixture = Fixture::new();
    fixture.write(
        "reports/unrelated-prefix.md",
        "literal ]( prose before [missing](missing.md)\n",
    );
    fixture.fails("unrelated-prefix.md: broken relative link: missing.md");
    let fixture = Fixture::new();
    fixture.write(
        "reports/malformed-then-valid.md",
        "[malformed] text [missing](missing.md)\n",
    );
    fixture.fails("malformed-then-valid.md: broken relative link: missing.md");
    let fixture = Fixture::new();
    fixture.write("reports/multiple.md", "[one](one.md) and [two](two.md)\n");
    let errors = fixture.errors();
    assert!(
        errors
            .iter()
            .any(|error| error.contains("multiple.md: broken relative link: one.md"))
    );
    assert!(
        errors
            .iter()
            .any(|error| error.contains("multiple.md: broken relative link: two.md"))
    );
    let fixture = Fixture::new();
    fixture.write("reports/escaping.md", "[escape](../../outside.md)\n");
    fixture.fails("escaping.md: link escapes repository: ../../outside.md");
    let fixture = Fixture::new();
    fixture.write(
        "reports/ordinary-prose.md",
        "ordinary ]( prose and [fragment](#section) plus [external](https://example.invalid)\n",
    );
    fixture.write(
        "reports/valid-fragment.md",
        "[local fragment](../README.md#canonical-validation)\n",
    );
    fixture.passes();
}

fn closed_initiative(status: &str, closed: &str, closure: &str) -> String {
    format!(
        "# Fixture initiative\n\n- Status: {status}\n- Owner: Dornglut organization\n- Opened: 2026-08-01\n- Closed: {closed}\n- Owning issue: [engineering#27](https://github.com/dornglut/engineering/issues/27)\n- Decision authority: [Validation standard](../standards/validation.md)\n\n## Outcome\n\nFixture outcome.\n\n## Rationale\n\nFixture rationale.\n\n## Affected repositories\n\n- `dornglut/engineering`\n\n## Dependency graph\n\nNone.\n\n## Acceptance evidence\n\nFixture evidence.\n\n## Sequencing constraints\n\nNone.\n\n## Linked local issues\n\n- [engineering#27](https://github.com/dornglut/engineering/issues/27)\n\n## Risks and rollback\n\nNone.\n\n## Closure record\n\n{closure}\n"
    )
}

fn add_closed_initiative(fixture: &Fixture, status: &str, closed: &str, closure: &str) {
    fixture.write(
        "initiatives/fixture-closure.md",
        &closed_initiative(status, closed, closure),
    );
    fixture.replace(
        "initiatives/README.md",
        "## Closed",
        "## Closed\n\n- [Fixture initiative](fixture-closure.md) — fixture lifecycle evidence",
    );
}

#[test]
fn closed_initiatives_require_dates_and_substantive_closure_records() {
    let fixture = Fixture::new();
    add_closed_initiative(
        &fixture,
        "completed",
        "2026-08-02",
        "Completed with reviewed evidence.",
    );
    fixture.passes();
    let fixture = Fixture::new();
    add_closed_initiative(
        &fixture,
        "cancelled",
        "2026-08-02",
        "Cancelled because the authorized outcome was no longer needed.",
    );
    fixture.passes();
    for (status, closed, closure) in [
        ("completed", "2026-08-02", "None."),
        ("completed", "2026-08-02", "Open."),
        ("cancelled", "2026-08-02", "None."),
        ("cancelled", "2026-08-02", ""),
        ("cancelled", "", "Cancelled with a recorded rationale."),
    ] {
        let fixture = Fixture::new();
        add_closed_initiative(&fixture, status, closed, closure);
        fixture.fails("closed initiative requires");
    }
}
#[test]
fn initiative_lifecycle_rejections() {
    let fixture = Fixture::new();
    fixture.replace(
        "initiatives/verified-head-validation.md",
        "- Status: completed",
        "- Status: active",
    );
    fixture.fails("active initiative must not have a close date");
    let fixture = Fixture::new();
    fixture.replace(
        "initiatives/verified-head-validation.md",
        "- Closed: 2026-07-29",
        "- Closed:",
    );
    fixture.fails("closed initiative requires a YYYY-MM-DD close date");
    let fixture = Fixture::new();
    fixture.replace(
        "initiatives/verified-head-validation.md",
        "- Status: completed",
        "- Status: active",
    );
    fixture.replace(
        "initiatives/verified-head-validation.md",
        "Verified-head validation adoption completed",
        "Completed delivery.",
    );
    fixture.fails("active initiative requires an open closure state");
    let fixture = Fixture::new();
    fixture.replace("initiatives/README.md", "## Closed", "## Active\n\n- [Verified-head validation adoption](verified-head-validation.md)\n\n## Closed");
    fixture.replace("initiatives/README.md", "- [Verified-head validation adoption](verified-head-validation.md) — completed immutable, exact-head repository validation adoption\n", "");
    fixture.fails("does not match index section");
    let fixture = Fixture::new();
    fixture.replace(
        "initiatives/README.md",
        "## Closed",
        "- [Verified-head validation adoption](verified-head-validation.md)\n\n## Closed",
    );
    fixture.fails("initiative index must link this file exactly once");
    let fixture = Fixture::new();
    fixture.replace(
        "initiatives/provider-neutral-repository-automation.md",
        "## Closure record",
        "## Retired closure record",
    );
    fixture.fails("missing required section \"Closure record\"");
    let fixture = Fixture::new();
    fixture.replace(
        "initiatives/verified-head-validation.md",
        "- Status: completed",
        "- Status: unknown",
    );
    fixture.fails("invalid status");
    let fixture = Fixture::new();
    fixture.replace(
        "initiatives/verified-head-validation.md",
        "- Owner: Dornglut organization\n",
        "",
    );
    fixture.fails("missing metadata \"Owner\"");
}
#[test]
fn authority_rejections() {
    let fixture = Fixture::new();
    fixture.replace(
        "adrs/0005-authorize-werkstatt-pilot.md",
        "- Status: accepted",
        "- Status: proposed",
    );
    fixture.fails("does not match index section");
    let fixture = Fixture::new();
    fixture.write("reports/broken.md", "[broken](missing.md)\n");
    fixture.fails("broken relative link");
    let fixture = Fixture::new();
    fixture.replace(
        "standards/repositories.md",
        "# Repository standard",
        "# Repository standard\n\nCrystonix/RunenSDF",
    );
    fixture.fails("historical owner token");
    let fixture = Fixture::new();
    fixture.replace(
        ".github/workflows/validate.yml",
        "@624cb41adeed21a6461eb838bc7330bd0a5079fd",
        "@main",
    );
    fixture.fails("immutable Rust validation caller");
    let fixture = Fixture::new();
    assert!(!fixture.0.join("scripts").exists());
    fixture.write("scripts/validate.py", "#!/usr/bin/env python3\n");
    fixture.fails("scripts/validate.py: retired authority path must not exist");
}
