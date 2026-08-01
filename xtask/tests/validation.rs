use std::fs;
use std::path::{Path, PathBuf};
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
        copy(source, &path);
        Self(path)
    }
    fn replace(&self, path: &str, from: &str, to: &str) {
        let file = self.0.join(path);
        let text = fs::read_to_string(&file).unwrap();
        assert!(text.contains(from));
        fs::write(file, text.replacen(from, to, 1)).unwrap();
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
fn copy(source: &Path, destination: &Path) {
    fs::create_dir_all(destination).unwrap();
    for entry in fs::read_dir(source).unwrap().flatten() {
        let name = entry.file_name();
        if name == ".git" || name == "target" {
            continue;
        }
        let from = entry.path();
        let to = destination.join(name);
        if entry.file_type().unwrap().is_dir() {
            copy(&from, &to);
        } else {
            fs::copy(from, to).unwrap();
        }
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
    fs::write(
        fixture.0.join("reports/broken.md"),
        "[broken](missing.md)\n",
    )
    .unwrap();
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
    fs::write(
        fixture.0.join("scripts/validate.py"),
        "#!/usr/bin/env python3\n",
    )
    .unwrap();
    fixture.fails("scripts/validate.py: retired authority path must not exist");
}
