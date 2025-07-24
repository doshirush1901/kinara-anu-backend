#!/usr/bin/env python3
"""
Test script for the Anu AI Recruiter API
Run this to test the API locally before deploying to Railway
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_health():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_process_candidate():
    """Test the process_candidate endpoint"""
    # Test data - you can modify these paths
    test_data = {
        "name": "Test Candidate",
        "email": "test@example.com",
        "cv_url": "candidate data/kishore_bv/kishore_resume.pdf",
        "dice_url": "candidate data/kishore_bv/kishore_dice.pdf"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/process_candidate",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Process candidate: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result.get('status')}")
            print(f"Summary: {result.get('summary_notes', 'No summary')}")
            print(f"Memories: {len(result.get('memories', []))} captured")
        else:
            print(f"Error: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Process candidate failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Anu AI Recruiter API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    health_ok = test_api_health()
    
    # Test 2: Process candidate (only if health check passed)
    if health_ok:
        print("\n2. Testing process candidate...")
        process_ok = test_process_candidate()
        
        if process_ok:
            print("\n🎉 All tests passed! API is working correctly.")
        else:
            print("\n⚠️ Process candidate test failed. Check logs for details.")
    else:
        print("\n❌ Health check failed. Make sure the API is running.")
        print("Run: uvicorn app:app --reload")

if __name__ == "__main__":
    main() 