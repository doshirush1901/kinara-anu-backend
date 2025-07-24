# test_supabase.py

"""
Test script to verify Supabase connection and table setup.
Run this to ensure your Supabase credentials are working correctly.
"""

import os
from dotenv import load_dotenv
from supabase_insert import test_supabase_connection, get_supabase_client

# Load environment variables
load_dotenv()

def main():
    """Test Supabase connection and basic operations."""
    print("🧪 Testing Supabase Connection and Setup")
    print("=" * 50)
    
    # Check environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    print(f"🔗 Supabase URL: {supabase_url}")
    print(f"🔑 Supabase Key: {supabase_key[:10]}...{supabase_key[-4:] if supabase_key else 'NOT SET'}")
    print()
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials!")
        print("📝 Please set SUPABASE_URL and SUPABASE_KEY in your .env file")
        return False
    
    # Test connection
    print("🔍 Testing connection...")
    if test_supabase_connection():
        print("✅ Connection successful!")
        
        # Test table structure
        print("\n🔍 Testing table structure...")
        try:
            supabase = get_supabase_client()
            if supabase:
                # Try to get table info
                result = supabase.table("anu_interviews").select("*").limit(1).execute()
                print("✅ Table 'anu_interviews' exists and is accessible!")
                print(f"📊 Current record count: {len(result.data)}")
                
                # Show table structure (first record if any)
                if result.data:
                    print("\n📋 Sample record structure:")
                    sample = result.data[0]
                    for key, value in sample.items():
                        if key not in ['chat_log', 'answers']:  # Skip large fields
                            print(f"   {key}: {type(value).__name__}")
                else:
                    print("📋 Table is empty - ready for first insertion!")
                
                return True
            else:
                print("❌ Failed to get Supabase client")
                return False
                
        except Exception as e:
            print(f"❌ Error testing table: {e}")
            return False
    else:
        print("❌ Connection failed!")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Supabase is ready for use!")
        print("💡 You can now run main.py with --push-supabase flag")
    else:
        print("\n❌ Please fix the issues above before proceeding") 