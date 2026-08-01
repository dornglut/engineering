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
    fn fails(self, expected: &str) {
        let errors = xtask::validate(&self.0).expect_err("fixture should fail");
        assert!(
            errors.iter().any(|error| error.contains(expected)),
            "expected {expected:?} in {errors:#?}"
        );
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
    assert!(xtask::validate(&fixture.0).is_ok());
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
