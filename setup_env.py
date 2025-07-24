"""
Environment Setup Script
Helps you create a .env file from the example template
"""

import os
import shutil
from pathlib import Path

def setup_environment():
    """Create .env file from env.example if it doesn't exist."""
    
    env_example = Path("env.example")
    env_file = Path(".env")
    
    if not env_example.exists():
        print("❌ env.example file not found!")
        return False
    
    if env_file.exists():
        print("✅ .env file already exists")
        print("📝 Current .env contents:")
        with open(env_file, 'r') as f:
            print(f.read())
        return True
    
    # Copy env.example to .env
    try:
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from env.example")
        print("📝 Please edit .env file and add your API keys:")
        print("   - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys")
        print("   - Uncomment other variables as needed")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_environment():
    """Check if required environment variables are set."""
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("📝 Please set these in your .env file or environment")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def main():
    """Main setup function."""
    print("🔧 AI Recruiter Environment Setup")
    print("=" * 40)
    
    # Setup .env file
    if setup_environment():
        print("\n📋 Next Steps:")
        print("1. Edit .env file and add your OpenAI API key")
        print("2. Run: python setup_env.py --check")
        print("3. Test the system: python test_structure.py")
    
    # Check if --check flag is provided
    if "--check" in os.sys.argv:
        print("\n🔍 Checking Environment Variables...")
        check_environment()

if __name__ == "__main__":
    main() 