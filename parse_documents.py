"""
🎯 GOAL:
Given two PDFs — a resume (CV) and a DICE personality test result — extract structured data for an AI recruiter system (Anu).

📥 Inputs:
- cv_text: raw extracted text from a candidate's CV (PDF)
- dice_text: raw extracted text from a DICE test PDF

📤 Outputs:
Return a dictionary with:
- name: (if available in CV)
- email: (if available)
- skills: list of tools or domains mentioned (e.g., SolidWorks, CAM)
- cad_tools: list of CAD tools mentioned (e.g., Fusion 360, AutoCAD)
- projects: list of final year / internship projects (max 3)
- personality_type: extracted from DICE (e.g., High C, Mid D)
- tone_profile: text description of interview tone (e.g., "structured and logical")

📎 Style Guide:
Use short, structured answers.
Avoid guessing — return empty arrays if not found.
"""

import json
import openai
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_candidate_profile(cv_text: str, dice_text: str, api_key: Optional[str] = None) -> Dict:
    """
    Extract structured candidate data from CV and DICE test results.
    
    Args:
        cv_text: Raw text extracted from CV PDF
        dice_text: Raw text extracted from DICE test PDF
        api_key: OpenAI API key (optional, can be set via environment)
    
    Returns:
        Dictionary containing extracted candidate profile data
    """
    
    # Set up OpenAI client
    if api_key:
        client = openai.OpenAI(api_key=api_key)
    else:
        client = openai.OpenAI()  # Uses OPENAI_API_KEY environment variable
    
    prompt = f"""
CV TEXT:
{cv_text}

DICE TEXT:
{dice_text}

---

Please extract the following structured data in JSON format:

{{
  "name": "<name>",
  "email": "<email>",
  "skills": ["...", "..."],
  "cad_tools": ["SolidWorks", "Fusion 360"],
  "projects": ["...", "..."],
  "personality_type": "<DICE summary>",
  "tone_profile": "<interview tone>"
}}

IMPORTANT GUIDELINES:
- Return ONLY valid JSON, no additional text
- For skills: include technical tools, software, domains mentioned
- For cad_tools: specifically CAD/CAM software (SolidWorks, Fusion 360, AutoCAD, etc.)
- For projects: list actual project names/titles (max 3)
- For personality_type: analyze DICE responses to determine work style (e.g., "High C (Creative), Mid D (Drive)", "Balanced DICE profile", "Detail-oriented and systematic")
- For tone_profile: describe interview approach based on personality (e.g., "warm and curious", "structured and mentor-like", "enthusiastic and collaborative")
- If information is not found, use empty strings for text fields and empty arrays for lists
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful data extractor for an AI recruiter. Analyze CV and DICE assessment data to extract structured candidate information. For DICE assessments, analyze the pattern of responses to determine work style preferences. Always return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1  # Low temperature for consistent extraction
        )

        extracted_data = response.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            parsed_data = json.loads(extracted_data)
            logger.info(f"Successfully extracted profile for: {parsed_data.get('name', 'Unknown')}")
            return parsed_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Raw response: {extracted_data}")
            return _get_default_profile()
            
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return _get_default_profile()

def _get_default_profile() -> Dict:
    """Return default profile structure when extraction fails."""
    return {
        "name": "",
        "email": "",
        "skills": [],
        "cad_tools": [],
        "projects": [],
        "personality_type": "",
        "tone_profile": ""
    }

def validate_profile(profile: Dict) -> bool:
    """
    Validate that the extracted profile has required fields.
    
    Args:
        profile: Extracted candidate profile
    
    Returns:
        True if profile is valid, False otherwise
    """
    required_fields = ["name", "email", "skills", "cad_tools", "projects", "personality_type", "tone_profile"]
    
    for field in required_fields:
        if field not in profile:
            logger.warning(f"Missing required field: {field}")
            return False
    
    return True

# Example usage and testing
if __name__ == "__main__":
    # Example CV and DICE text for testing
    sample_cv = """
    SAMIYA NAIK
    Email: samiya@example.com
    
    SKILLS:
    - SolidWorks
    - Fusion 360
    - CAM Programming
    - 3D Modeling
    
    PROJECTS:
    - Drone kill switch circuit design
    - Tool design for vacuum forming mold
    - Automated assembly line optimization
    """
    
    sample_dice = """
    DICE PERSONALITY ASSESSMENT RESULTS:
    
    Primary Type: High C (Conscientious)
    Secondary Type: Mid D (Dominant)
    
    Interview Style: Structured and analytical approach
    Communication: Direct and logical
    """
    
    # Test the extraction
    result = extract_candidate_profile(sample_cv, sample_dice)
    print("Extracted Profile:")
    print(json.dumps(result, indent=2))
    
    # Validate the result
    is_valid = validate_profile(result)
    print(f"\nProfile validation: {'✅ Valid' if is_valid else '❌ Invalid'}") 