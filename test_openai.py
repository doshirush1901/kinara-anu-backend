import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection with the provided key."""
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No OpenAI API key found in environment variables")
        print("📝 Please set OPENAI_API_KEY in your .env file or export it")
        return False
    
    if api_key == "your_openai_api_key_here":
        print("❌ API key is still the placeholder value")
        print("📝 Please update your .env file with your actual API key")
        return False
    
    print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        # Test with OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello, are you online? Just respond with 'Yes, working!'"}],
            max_tokens=50
        )
        
        print("✅ OpenAI connected successfully!")
        print(f"🤖 Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print("❌ Error connecting to OpenAI:")
        print(f"   Error: {e}")
        
        # Provide helpful debugging info
        if "401" in str(e):
            print("   💡 This looks like an authentication error. Check your API key.")
        elif "429" in str(e):
            print("   💡 Rate limit exceeded. Try again in a moment.")
        elif "network" in str(e).lower():
            print("   💡 Network connectivity issue. Check your internet connection.")
        
        return False

def test_with_provided_key():
    """Test with the specific API key provided by the user."""
    
    print("🔑 Testing with provided key...")
    print("⚠️  This function requires a valid API key to be provided manually")
    print("📝 To test with a specific key, modify this function with your API key")
    
    return False

if __name__ == "__main__":
    print("🧪 Testing OpenAI API Connection")
    print("=" * 40)
    
    # Test with environment variable first
    print("🔍 Testing with environment variable...")
    env_success = test_openai_connection()
    
    print("\n" + "=" * 40)
    
    # Test with provided key
    print("🔍 Testing with provided API key...")
    provided_success = test_with_provided_key()
    
    print("\n" + "=" * 40)
    
    if env_success:
        print("🎉 Environment setup is working! You can now run the main system.")
    elif provided_success:
        print("🎉 The provided API key works! Update your .env file with this key.")
        print("📝 Add your API key to your .env file: OPENAI_API_KEY=your_key_here")
    else:
        print("❌ Both tests failed. Please check your API key and internet connection.") 