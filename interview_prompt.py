"""
🎯 GOAL:
Transform Anu from a fixed-question chatbot into a conversational, mentor-style AI who builds rapport with candidates and understands them deeply.

Anu should:
- Ask personalized questions one at a time
- React warmly to each answer with encouragement or follow-ups
- Ask for a story or example behind important responses
- Store emotional/contextual takeaways as `memories[]`
- End with a smart final summary based on tone, answers, and memory

📥 Inputs:
- profile_data: {
    name, email,
    tone_profile,
    personality_type,
    skills,
    cad_tools,
    projects
  }

📤 Outputs:
- chat_log: full list of Q&A interactions
- answers: structured key values (location, relocation, cad_tools, etc.)
- memories: list of 1–2 line insights Anu gathered from the candidate
- summary_notes: a 3-line summary of candidate's strengths, mindset, and culture fit

🧠 Chat Flow:
1. Friendly intro
2. For each question:
   a. Ask original question
   b. React to answer + ask for story/example
   c. Add to memory
3. At end: call OpenAI to summarize from memories + answers

🎨 Style:
- Warm, informal, startup-vibe
- Use tone_profile to adjust energy (e.g. "structured and curious" vs "enthusiastic and warm")
- Use emojis occasionally (e.g. "🚀", "💡", "👏")
"""

import json
import openai
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_interview_chat(profile_data: Dict, api_key: Optional[str] = None) -> Dict:
    """Generate a conversational, mentor-style interview with Anu."""
    
    # Set up OpenAI client
    if api_key:
        client = openai.OpenAI(api_key=api_key)
    else:
        client = openai.OpenAI()
    
    # Extract key information
    name = profile_data.get('name', 'Candidate')
    personality_type = profile_data.get('personality_type', 'Unknown')
    tone_profile = profile_data.get('tone_profile', 'warm and curious')
    skills = profile_data.get('skills', [])
    cad_tools = profile_data.get('cad_tools', [])
    projects = profile_data.get('projects', [])
    
    # System primer for the new conversational Anu
    system_msg = f"""
You are Anu, an AI recruiter with a warm, mentor-like tone. You are smart, emotionally intelligent, and deeply curious about people. Your tone is: {tone_profile}

Your goal is to interview a candidate conversationally. Ask one question at a time. React to their answer with genuine interest and encouragement. Then ask them to share a story, example, or what they learned from that experience.

Build a memory of each exchange as a 1-line takeaway about their personality, work style, or values. At the end, use the answers + memories to write a 3-line summary of the candidate's strengths, mindset, and culture fit.

Key questions to cover (but ask them naturally in conversation):
- Where are they based?
- Education/graduation status
- Tell me about their projects (ask for specific stories)
- CAD tools they enjoy using
- Preference for hands-on vs design-only work
- Openness to relocating to Umargam
- Commitment to 2-3 years
- Salary expectations
- Interest in factory visit

Use emojis occasionally to keep it warm and engaging. Be genuinely curious about their experiences and what drives them.

Respond in JSON format:
{{
  "chat_log": [
    {{"role": "Anu", "message": "Hi {name}! So happy to chat with you today! Where are you currently based?"}},
    {{"role": "Candidate", "message": "I'm in Bengaluru."}},
    {{"role": "Anu", "message": "Love that city! 💫 What do you enjoy most about living there?"}}
  ],
  "answers": {{
    "location": "Bengaluru",
    "education_status": "Recently graduated",
    "internship_work": "Worked on drone projects",
    "cad_tools": "SolidWorks, AutoCAD",
    "role_preference": "Hands-on work",
    "relocation": "Open to relocating",
    "commitment": "Willing for 2-3 years",
    "salary_expectation": "Within budget",
    "factory_visit_interest": "Very interested"
  }},
  "memories": [
    "Kishore enjoys hands-on roles and feels most fulfilled when seeing his designs in action.",
    "He took initiative during his internship to integrate ML models without being asked."
  ],
  "summary_notes": "Kishore is a thoughtful, technically sharp candidate who thrives in hands-on environments. He takes initiative and has strong interdisciplinary thinking. Great culture fit for small team learning environments."
}}
"""

    user_msg = f"""
Here's the candidate profile:

Name: {name}
Personality Type: {personality_type}
Skills: {', '.join(skills)}
CAD Tools: {', '.join(cad_tools)}
Projects: {', '.join(projects)}

Begin the interview now. Make it feel like a natural conversation between two people getting to know each other.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.8  # Higher temperature for more natural conversation
        )

        chat_data = response.choices[0].message.content.strip()
        
        try:
            parsed_data = json.loads(chat_data)
            
            # Add metadata
            parsed_data['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'candidate_name': name,
                'personality_type': personality_type,
                'tone_profile': tone_profile,
                'version': 'Anu v2 - Conversational Mentor'
            }
            
            # Validate and ensure all required fields exist
            if 'memories' not in parsed_data:
                parsed_data['memories'] = []
            if 'answers' not in parsed_data:
                parsed_data['answers'] = {}
            if 'summary_notes' not in parsed_data:
                parsed_data['summary_notes'] = f"Interview completed for {name}. Manual review recommended."
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse interview JSON: {e}")
            return _get_default_interview_data(profile_data)
            
    except Exception as e:
        logger.error(f"Error generating interview: {e}")
        return _get_default_interview_data(profile_data)

def _get_default_interview_data(profile_data: Dict) -> Dict:
    """Return default interview structure when generation fails."""
    name = profile_data.get('name', 'Candidate')
    
    return {
        "chat_log": [
            {"role": "Anu", "message": f"Hi {name}! I'm Anu from Kinara. So excited to chat with you today! ✨"},
            {"role": "Candidate", "message": "Hi Anu! Nice to meet you too."}
        ],
        "answers": {
            "location": "",
            "education_status": "",
            "internship_work": "",
            "cad_tools": "",
            "role_preference": "",
            "relocation": "",
            "commitment": "",
            "salary_expectation": "",
            "factory_visit_interest": ""
        },
        "memories": [
            f"Interview generation failed for {name}. Manual review required."
        ],
        "summary_notes": f"Interview generation failed for {name}. Manual review required.",
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "candidate_name": name,
            "error": "Interview generation failed",
            "version": "Anu v2 - Fallback"
        }
    }

def validate_interview_data(interview_data: Dict) -> bool:
    """Validate that the generated interview data has required fields."""
    required_fields = ["chat_log", "answers", "memories", "summary_notes"]
    
    for field in required_fields:
        if field not in interview_data:
            return False
    
    return True

def format_chat_for_display(chat_data: Dict) -> str:
    """Format the chat log for easy reading."""
    if "chat_log" not in chat_data:
        return "No chat log available"
    
    formatted_chat = []
    for message in chat_data["chat_log"]:
        role = message.get("role", "Unknown")
        content = message.get("message", "")
        formatted_chat.append(f"{role}: {content}")
    
    return "\n\n".join(formatted_chat)

def format_memories_for_display(chat_data: Dict) -> str:
    """Format the memories for easy reading."""
    if "memories" not in chat_data:
        return "No memories available"
    
    memories = chat_data["memories"]
    if not memories:
        return "No memories captured"
    
    formatted_memories = []
    for i, memory in enumerate(memories, 1):
        formatted_memories.append(f"{i}. {memory}")
    
    return "\n".join(formatted_memories)

# Example usage
if __name__ == "__main__":
    sample_profile = {
        "name": "Kishore BV",
        "email": "kishore@example.com",
        "skills": ["CAD Designing", "ML Programming", "Python Programming"],
        "cad_tools": ["SolidWorks", "AutoCAD"],
        "projects": ["Lifebuoy Rescue Drone", "Tethered Drone System"],
        "personality_type": "High C, Mid D",
        "tone_profile": "warm and curious"
    }
    
    print("🧪 Testing Anu v2 - Conversational Mentor...")
    
    try:
        result = generate_interview_chat(sample_profile)
        print("✅ Interview generated successfully!")
        print(f"Summary: {result.get('summary_notes', 'No summary')}")
        print(f"Memories: {len(result.get('memories', []))} captured")
        
        is_valid = validate_interview_data(result)
        print(f"Validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        if is_valid:
            print("\n📝 Memories:")
            print(format_memories_for_display(result))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Set OPENAI_API_KEY to test with real API calls.") 