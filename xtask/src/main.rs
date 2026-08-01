use std::path::Path;
use std::process::Command;

fn main() {
    let arguments: Vec<_> = std::env::args().skip(1).collect();
    if arguments.as_slice() != ["validate"] {
        eprintln!("usage: cargo validate");
        std::process::exit(2);
    }

    let root = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("xtask manifest must have a repository root");
    for (label, arguments) in [
        ("format check", &["+stable", "fmt", "--all", "--check"][..]),
        (
            "Clippy",
            &[
                "+stable",
                "clippy",
                "--workspace",
                "--all-targets",
                "--locked",
                "--",
                "-D",
                "warnings",
            ][..],
        ),
        (
            "locked tests",
            &[
                "+stable",
                "test",
                "--workspace",
                "--all-targets",
                "--locked",
            ][..],
        ),
    ] {
        run_cargo(root, label, arguments);
    }
    match xtask::validate(root) {
        Ok(()) => println!("repository validation passed"),
        Err(findings) => {
            eprintln!("repository validation failed:");
            for finding in findings {
                eprintln!("- {finding}");
            }
            std::process::exit(1);
        }
    }
}

fn run_cargo(root: &Path, label: &str, arguments: &[&str]) {
    let status = Command::new("cargo")
        .args(arguments)
        .current_dir(root)
        .status()
        .unwrap_or_else(|error| {
            eprintln!("failed to run {label}: {error}");
            std::process::exit(2);
        });
    if !status.success() {
        eprintln!("{label} failed");
        std::process::exit(status.code().unwrap_or(1));
    }
}
