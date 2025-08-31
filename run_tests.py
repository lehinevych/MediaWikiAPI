#!/usr/bin/env python3
import os
import sys
import subprocess

"""
This script runs only the tests that are known to work without making live API requests.
It can be used as a replacement for ./scripts.py test
"""


def run_tests():
    """Run the specified working tests with pytest"""
    # Get path to pytest in virtual environment
    pytest_path = os.path.join(".venv", "bin", "pytest")
    if not os.path.exists(pytest_path):
        print(
            f"Error: {pytest_path} not found. Make sure you have activated the virtual environment."
        )
        return 1

    # Build the command
    cmd = [
        pytest_path,
        "--junitxml=pytest.xml",
        "--cov-report=term-missing:skip-covered",
        "--cov=mediawikiapi",
    ]
    # Add any additional arguments from command line
    cmd.extend(sys.argv[1:])

    print(f"Running tests with command: {' '.join(cmd)}")

    # Run the tests
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(run_tests())

