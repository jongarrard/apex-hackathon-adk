#!/usr/bin/env python3
"""
Setup script for the Apex Hackathon ADK project.
Run this script to set up your development environment.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None


def main():
    """Main setup function."""
    print("🚀 Setting up Apex Hackathon ADK Project")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path(".venv")
    if not venv_path.exists():
        run_command("python3 -m venv .venv", "Creating virtual environment")
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_script = ".venv\\Scripts\\activate"
        pip_command = ".venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_script = ".venv/bin/activate"
        pip_command = ".venv/bin/pip"
    
    # Install dependencies
    run_command(f"{pip_command} install --upgrade pip", "Upgrading pip")
    run_command(f"{pip_command} install -r requirements.txt", "Installing dependencies")
    run_command(f"{pip_command} install -e .", "Installing project in development mode")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate your virtual environment:")
    if os.name == 'nt':
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("2. Copy .env.example to .env and add your API keys")
    print("3. Run your agent: python -m multi_tool_agent")
    print("\nHappy hacking! 🚀")


if __name__ == "__main__":
    main()
