#!/usr/bin/env python3
"""
Diderot AI Startup Script
Checks configuration and launches the Streamlit application
"""

import os
import sys
import subprocess
from config import Config

def check_configuration():
    """Check if the application is properly configured"""
    print("🔧 Checking configuration...")
    
    status = Config.validate_config()
    
    if not status["openai_configured"]:
        print("❌ OpenAI API key not configured!")
        print("   Please set the OPENAI_API_KEY environment variable")
        print("   Example: export OPENAI_API_KEY='your-api-key'")
        return False
    
    if status["warnings"]:
        print("⚠️  Warnings:")
        for warning in status["warnings"]:
            print(f"   - {warning}")
    
    if status["errors"]:
        print("❌ Errors:")
        for error in status["errors"]:
            print(f"   - {error}")
        return False
    
    print("✅ Configuration looks good!")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def launch_app():
    """Launch the Streamlit application"""
    print("🚀 Launching Diderot AI...")
    print("   The app will open in your browser at http://localhost:8501")
    print("   Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")

def main():
    """Main startup function"""
    print("🎯 Diderot AI - Multi-Perspective Daily News")
    print("=" * 50)
    
    # Check if we should skip tests
    skip_tests = "--skip-tests" in sys.argv
    
    # Check configuration
    if not check_configuration():
        sys.exit(1)
    
    # Install dependencies if needed
    if "--install-deps" in sys.argv:
        if not install_dependencies():
            sys.exit(1)
    
    # Run tests unless skipped
    if not skip_tests:
        if not run_tests():
            print("\n⚠️  Tests failed, but continuing anyway...")
            print("   Use --skip-tests to bypass this check")
    
    # Launch the application
    launch_app()

if __name__ == "__main__":
    main() 