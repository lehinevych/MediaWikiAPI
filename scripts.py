#!/usr/bin/env python3
"""Development scripts for MediaWikiAPI."""

import argparse
import subprocess
import sys
from typing import List


def run_command(command: List[str]) -> int:
    """Run a command and return its exit code."""
    print(f"Running: {' '.join(command)}")
    return subprocess.call(command)


def install() -> int:
    """Install the package and dependencies."""
    return run_command(["uv", "pip", "install", "-e", "."])


def install_dev() -> int:
    """Install development dependencies."""
    return run_command(["uv", "pip", "install", "-e", ".[dev]"])


def install_docs() -> int:
    """Install documentation dependencies."""
    return run_command(["uv", "pip", "install", "-e", ".[docs]"])


def setup_hooks() -> int:
    """Set up pre-commit hooks."""
    result = run_command(["uv", "pip", "install", "pre-commit"])
    if result != 0:
        return result
    return run_command(["pre-commit", "install"])


def test(args: List[str]) -> int:
    """Run tests with pytest."""
    cmd = ["pytest"]
    if not args:
        cmd.extend(
            [
                "--junitxml=pytest.xml",
                "--cov-report=term-missing:skip-covered",
                "--cov=mediawikiapi",
            ]
        )
    else:
        cmd.extend(args)
    return run_command(cmd)


def lint() -> int:
    """Run linting tools with ruff."""
    return run_command(["ruff", "check", "."])


def typecheck() -> int:
    """Run type checking."""
    return run_command(["mypy", "--strict", "."])


def format_code() -> int:
    """Format code with ruff."""
    return run_command(["ruff", "format", "."])


def format_check() -> int:
    """Check code formatting with ruff."""
    return run_command(["ruff", "format", "--check", "."])


def build() -> int:
    """Build the package."""
    return run_command(["python", "-m", "build"])


def build_docs() -> int:
    """Build the documentation."""
    return run_command(["sphinx-build", "docs/source", "docs/build"])


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Development scripts for MediaWikiAPI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Install commands
    install_parser = subparsers.add_parser("install", help="Install the package")
    install_dev_parser = subparsers.add_parser(
        "install-dev", help="Install development dependencies"
    )
    install_docs_parser = subparsers.add_parser(
        "install-docs", help="Install documentation dependencies"
    )

    # Test commands
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("args", nargs="*", help="Arguments to pass to pytest")

    # Lint and format commands
    subparsers.add_parser("lint", help="Run linting tools with ruff")
    subparsers.add_parser("typecheck", help="Run type checking")
    subparsers.add_parser("format", help="Format code with ruff")
    subparsers.add_parser("format-check", help="Check code formatting with ruff")

    # Build commands
    subparsers.add_parser("build", help="Build the package")
    subparsers.add_parser("build-docs", help="Build the documentation")

    # Git hooks
    subparsers.add_parser("setup-hooks", help="Set up pre-commit hooks")

    args = parser.parse_args()

    if args.command == "install":
        return install()
    elif args.command == "install-dev":
        return install_dev()
    elif args.command == "install-docs":
        return install_docs()
    elif args.command == "test":
        return test(args.args)
    elif args.command == "lint":
        return lint()
    elif args.command == "typecheck":
        return typecheck()
    elif args.command == "format":
        return format_code()
    elif args.command == "format-check":
        return format_check()
    elif args.command == "build":
        return build()
    elif args.command == "build-docs":
        return build_docs()
    elif args.command == "setup-hooks":
        return setup_hooks()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
