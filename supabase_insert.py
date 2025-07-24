# supabase_insert.py

"""
🎯 GOAL:
Insert a candidate profile + AI interview data into Supabase table `anu_interviews`.

📥 Inputs:
- profile_data: dict from parse_documents.py
- chat_data: dict from interview_prompt.py
- cv_url: Supabase Storage path (or mock path)
- dice_url: Supabase Storage path (or mock path)

📤 Output:
- Confirmation or failure notice
"""

import os
import json
import logging
from typing import Dict, Optional
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Optional[Client]:
    """Initialize and return Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("❌ Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in your .env file")
        return None
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Supabase client initialized successfully")
        return supabase
    except Exception as e:
        logger.error(f"❌ Error initializing Supabase client: {e}")
        return None

def insert_candidate_to_supabase(profile_data: Dict, chat_data: Dict, cv_url: str, dice_url: str) -> Optional[Dict]:
    """
    Insert candidate profile and interview data into Supabase.
    
    Args:
        profile_data: Dictionary containing candidate profile information
        chat_data: Dictionary containing interview chat data
        cv_url: URL/path to CV file in Supabase Storage
        dice_url: URL/path to DICE file in Supabase Storage
    
    Returns:
        Supabase response data or None if failed
    """
    try:
        # Get Supabase client
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        # Prepare data for insertion - start with minimal fields to test
        data = {
            "name": profile_data.get("name", ""),
            "email": profile_data.get("email", ""),
            "cv_url": cv_url,
            "dice_url": dice_url,
            "skills": ", ".join(profile_data.get("skills", [])),  # Convert list to string
            "status": "pending"
        }
        
        # Add optional fields if they exist
        if profile_data.get("personality_type"):
            data["personality_type"] = profile_data.get("personality_type", "")
        if profile_data.get("tone_profile"):
            data["tone_profile"] = profile_data.get("tone_profile", "")
        if chat_data.get("summary_notes"):
            data["summary_notes"] = chat_data.get("summary_notes", "")
        if chat_data.get("memories"):
            data["memories"] = chat_data.get("memories", [])
        
        logger.info(f"📝 Inserting candidate: {data['name']}")
        
        # Debug: Print the exact data being sent
        print("📤 Inserting the following data to Supabase:")
        print(json.dumps(data, indent=2))
        
        # Insert into Supabase with better error handling
        try:
            result = supabase.table("anu_interviews").insert(data).execute()
            print("✅ Supabase insert successful!")
            return result.data
        except Exception as insert_error:
            print(f"❌ Error inserting into Supabase: {insert_error}")
            print(f"   Error type: {type(insert_error).__name__}")
            return None
        
        if result.data:
            logger.info("✅ Successfully inserted candidate data into Supabase!")
            logger.info(f"📊 Inserted {len(result.data)} record(s)")
            return result.data
        else:
            logger.error("❌ No data returned from Supabase insert")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error inserting into Supabase: {e}")
        return None

def test_supabase_connection() -> bool:
    """Test Supabase connection and table access."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        # Try to query the table to test connection
        result = supabase.table("anu_interviews").select("count", count="exact").limit(1).execute()
        logger.info("✅ Supabase connection test successful!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Supabase connection test failed: {e}")
        return False

def get_table_schema() -> Optional[Dict]:
    """Get the table schema to understand available columns."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        # Try to get table info by selecting all columns
        result = supabase.table("anu_interviews").select("*").limit(1).execute()
        
        if result.data:
            # Get column names from the first row
            columns = list(result.data[0].keys()) if result.data else []
            print("📋 Available columns in anu_interviews table:")
            for col in columns:
                print(f"   - {col}")
            return {"columns": columns, "sample_data": result.data[0]}
        else:
            print("📋 Table exists but is empty. Checking schema...")
            return {"columns": [], "empty": True}
            
    except Exception as e:
        print(f"❌ Error getting table schema: {e}")
        return None

if __name__ == "__main__":
    # Test the connection and schema
    print("🧪 Testing Supabase Connection and Schema...")
    print("=" * 50)
    
    if test_supabase_connection():
        print("✅ Connection successful!")
        print("\n📋 Checking table schema...")
        schema = get_table_schema()
        if schema:
            print("🎉 Supabase is ready for use!")
        else:
            print("⚠️  Could not retrieve table schema")
    else:
        print("❌ Please check your Supabase credentials and table setup") 