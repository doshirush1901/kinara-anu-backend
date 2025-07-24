"""
Test script to verify the system structure without requiring OpenAI API key
"""

import json
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported correctly."""
    try:
        from parse_documents import extract_candidate_profile, validate_profile, _get_default_profile
        from pdf_extractor import extract_text_from_pdf, extract_cv_and_dice_texts
        from interview_prompt import generate_interview_chat, validate_interview_data, format_chat_for_display
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_default_profile():
    """Test the default profile structure."""
    try:
        from parse_documents import _get_default_profile
        
        profile = _get_default_profile()
        required_fields = ["name", "email", "skills", "cad_tools", "projects", "personality_type", "tone_profile"]
        
        for field in required_fields:
            if field not in profile:
                print(f"❌ Missing field in default profile: {field}")
                return False
        
        print("✅ Default profile structure is correct")
        print(f"Default profile: {json.dumps(profile, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error testing default profile: {e}")
        return False

def test_validation():
    """Test profile validation function."""
    try:
        from parse_documents import validate_profile
        
        # Test valid profile
        valid_profile = {
            "name": "Test User",
            "email": "test@example.com",
            "skills": ["SolidWorks"],
            "cad_tools": ["Fusion 360"],
            "projects": ["Test Project"],
            "personality_type": "High C",
            "tone_profile": "structured"
        }
        
        if validate_profile(valid_profile):
            print("✅ Profile validation works for valid profiles")
        else:
            print("❌ Profile validation failed for valid profile")
            return False
        
        # Test invalid profile
        invalid_profile = {"name": "Test"}
        if not validate_profile(invalid_profile):
            print("✅ Profile validation correctly rejects invalid profiles")
        else:
            print("❌ Profile validation should reject invalid profiles")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error testing validation: {e}")
        return False

def test_interview_functions():
    """Test interview generation functions."""
    try:
        from interview_prompt import validate_interview_data, format_chat_for_display, _get_default_interview_data
        
        # Test default interview data
        sample_profile = {"name": "Test User"}
        default_data = _get_default_interview_data(sample_profile)
        
        if validate_interview_data(default_data):
            print("✅ Default interview data validation works")
        else:
            print("❌ Default interview data validation failed")
            return False
        
        # Test chat formatting
        formatted = format_chat_for_display(default_data)
        if "Anu:" in formatted and "Candidate:" in formatted:
            print("✅ Chat formatting works correctly")
        else:
            print("❌ Chat formatting failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error testing interview functions: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    required_files = [
        "parse_documents.py",
        "pdf_extractor.py", 
        "main.py",
        "interview_prompt.py",
        "setup_env.py",
        "env.example",
        "requirements.txt",
        "README.md",
        ".gitignore"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run all tests."""
    print("🧪 Testing AI Recruiter Document Parser Structure")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("Default Profile", test_default_profile),
        ("Profile Validation", test_validation),
        ("Interview Functions", test_interview_functions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System structure is correct.")
        print("\n📝 Next steps:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY=your_key_here")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Test with real PDFs: python main.py --cv-pdf cv.pdf --dice-pdf dice.pdf")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main()) 