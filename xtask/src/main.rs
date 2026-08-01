use std::path::PathBuf;
use std::process::Command;

fn main() {
    let arguments: Vec<_> = std::env::args().skip(1).collect();
    if arguments.as_slice() != ["validate"] {
        eprintln!("usage: cargo validate");
        std::process::exit(2);
    }

    let root = std::env::current_dir().unwrap_or_else(|error| {
        eprintln!("failed to resolve repository root: {error}");
        std::process::exit(2);
    });
    let tests = Command::new("cargo")
        .args(["test", "--locked", "--package", "xtask"])
        .current_dir(&root)
        .status()
        .unwrap_or_else(|error| {
            eprintln!("failed to run validator tests: {error}");
            std::process::exit(2);
        });
    if !tests.success() {
        std::process::exit(tests.code().unwrap_or(1));
    }
    match xtask::validate(&PathBuf::from(root)) {
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
