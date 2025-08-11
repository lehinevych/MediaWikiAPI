#!/usr/bin/env python3
"""Set up pre-commit hooks for the project."""

import os
import subprocess
import sys


def main() -> int:
    """Install pre-commit hooks."""
    print("Setting up pre-commit hooks...")
    
    # Install pre-commit if not already installed
    try:
        subprocess.check_call(["pre-commit", "--version"], stdout=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing pre-commit...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pre-commit"])
    
    # Install pre-commit hooks
    result = subprocess.call(["pre-commit", "install"])
    
    if result == 0:
        print("Pre-commit hooks successfully installed!")
    else:
        print("Failed to install pre-commit hooks.")
    
    return result


if __name__ == "__main__":
    sys.exit(main())