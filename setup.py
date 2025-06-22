#!/usr/bin/env python3
"""
Setup script for Code Inspector Pro v3.0 Enhanced Edition
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print the application banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚀 Code Inspector Pro v3.0                ║
    ║                    Enhanced Edition Setup                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "enhanced_requirements.txt"
        ])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        print("Please run: pip install -r enhanced_requirements.txt")
        sys.exit(1)

def create_env_file():
    """Create .env file for API key"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    print("\n🔑 Setting up environment variables...")
    
    api_key = input("Enter your Groq API key (or press Enter to skip): ").strip()
    
    if api_key:
        with open(env_file, "w") as f:
            f.write(f"GROQ_API_KEY={api_key}\n")
        print("✅ .env file created with API key")
    else:
        print("ℹ️ You can add your API key later in the .env file or in the app settings")

def create_config_file():
    """Create default configuration file"""
    config_file = Path("config.json")
    
    if config_file.exists():
        print("✅ Configuration file already exists")
        return
    
    default_config = {
        "theme": "Dark",
        "font_size": 14,
        "wrap_text": True,
        "auto_save": True,
        "notifications": True,
        "default_model": "llama-3.3-70b-versatile",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    with open(config_file, "w") as f:
        json.dump(default_config, f, indent=2)
    
    print("✅ Default configuration file created")

def check_files():
    """Check if required files exist"""
    required_files = [
        "enhanced_code_inspector.py",
        "enhanced_requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def run_app():
    """Run the application"""
    print("\n🚀 Starting Code Inspector Pro...")
    print("The application will open in your default web browser.")
    print("Press Ctrl+C to stop the application.")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "enhanced_code_inspector.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Check required files
    if not check_files():
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Create configuration files
    create_env_file()
    create_config_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Make sure you have a Groq API key")
    print("2. Run the application with: python enhanced_code_inspector.py")
    print("3. Or use Streamlit: streamlit run enhanced_code_inspector.py")
    
    # Ask if user wants to run the app now
    run_now = input("\n🚀 Would you like to run the application now? (y/n): ").lower().strip()
    
    if run_now in ['y', 'yes']:
        run_app()
    else:
        print("\n👋 Setup complete! Run the application when you're ready.")

if __name__ == "__main__":
    main() 