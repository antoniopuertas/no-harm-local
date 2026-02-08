#!/usr/bin/env python3
"""
Setup Script: Download Ollama Models for Jury System

Downloads and verifies all 5 jury member models.
"""

import subprocess
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml


def run_command(cmd):
    """Run shell command and return output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout, result.stderr


def check_ollama_installed():
    """Check if Ollama is installed"""
    success, stdout, stderr = run_command("ollama --version")
    if not success:
        print("✗ Ollama is not installed!")
        print("\nPlease install Ollama first:")
        print("  Visit: https://ollama.ai/")
        print("  Or run: curl https://ollama.ai/install.sh | sh")
        sys.exit(1)
    print(f"✓ Ollama installed: {stdout.strip()}")


def pull_model(model_name, model_id, size_gb):
    """Pull a single Ollama model"""
    print(f"\n{'='*80}")
    print(f"Downloading: {model_name} ({size_gb} GB)")
    print(f"Model ID: {model_id}")
    print(f"{'='*80}")
    
    # Check if already downloaded
    success, stdout, stderr = run_command(f"ollama list | grep '{model_id.split(':')[0]}'")
    if success and model_id in stdout:
        print(f"✓ {model_name} already downloaded")
        return True
    
    # Pull model
    print(f"Pulling {model_id}... (this may take a while)")
    success, stdout, stderr = run_command(f"ollama pull {model_id}")
    
    if success:
        print(f"✓ {model_name} downloaded successfully")
        return True
    else:
        print(f"✗ Failed to download {model_name}")
        print(f"Error: {stderr}")
        return False


def main():
    """Download all jury models"""
    print("=" * 80)
    print("NO-HARM-LOCAL: MODEL SETUP")
    print("=" * 80)
    print("This will download 5 jury models (~320GB total)")
    print("Ensure you have sufficient disk space and a stable internet connection.")
    print("=" * 80)
    
    # Check Ollama installation
    check_ollama_installed()
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "jury_config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    jury_members = config['jury_members']
    
    print(f"\nModels to download: {len(jury_members)}")
    total_size = sum(m['size_gb'] for m in jury_members)
    print(f"Total size: {total_size:.1f} GB")
    
    # Confirm
    response = input("\nProceed with download? [y/N]: ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        sys.exit(0)
    
    # Download each model
    success_count = 0
    failed_models = []
    
    for member in jury_members:
        success = pull_model(
            member['name'],
            member['ollama_model'],
            member['size_gb']
        )
        
        if success:
            success_count += 1
        else:
            failed_models.append(member['name'])
    
    # Summary
    print("\n" + "=" * 80)
    print("SETUP SUMMARY")
    print("=" * 80)
    print(f"Successfully downloaded: {success_count}/{len(jury_members)} models")
    
    if failed_models:
        print(f"\nFailed models:")
        for model in failed_models:
            print(f"  - {model}")
        print("\nYou can retry failed downloads by running this script again.")
    else:
        print("\n✓✓ All models downloaded successfully!")
        print("\nYou can now run evaluations:")
        print("  python scripts/run_evaluation.py --dataset medqa --samples 10")
    
    print("=" * 80)


if __name__ == "__main__":
    main()
