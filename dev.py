#!/usr/bin/env python3
"""
Development helper script for common tasks.
Usage: python dev.py <command>

Commands:
  setup     - Set up the development environment
  run       - Run the agent
  format    - Format code with black
  lint      - Run linting with flake8
  clean     - Clean up cache files
"""

import sys
import subprocess
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return None


def setup():
    """Set up the development environment."""
    print("🚀 Setting up development environment...")
    subprocess.run([sys.executable, "setup.py"])


def run_agent():
    """Run the agent."""
    print("🤖 Running the agent...")
    subprocess.run([sys.executable, "-m", "multi_tool_agent"])


def format_code():
    """Format code with black."""
    run_command("black .", "Formatting code")


def lint():
    """Run linting."""
    run_command("flake8 multi_tool_agent/", "Running linter")


def clean():
    """Clean up cache files."""
    print("🧹 Cleaning up cache files...")
    
    # Remove __pycache__ directories
    for pycache in Path(".").rglob("__pycache__"):
        if pycache.is_dir():
            run_command(f"rm -rf {pycache}", f"Removing {pycache}")
    
    # Remove .pyc files
    for pyc_file in Path(".").rglob("*.pyc"):
        if pyc_file.is_file():
            pyc_file.unlink()
    
    print("✅ Cleanup completed")


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    commands = {
        "setup": setup,
        "run": run_agent,
        "format": format_code,
        "lint": lint,
        "clean": clean,
    }
    
    if command not in commands:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)
    
    commands[command]()


if __name__ == "__main__":
    main()
