"""
Main orchestrator for the AI Recruiter Document Parsing System
Handles the complete workflow from PDF extraction to profile generation
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from parse_documents import extract_candidate_profile, validate_profile
from pdf_extractor import extract_cv_and_dice_texts, extract_text_from_pdf
from interview_prompt import generate_interview_chat, validate_interview_data, format_chat_for_display
from supabase_insert import insert_candidate_to_supabase

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline(name: str, email: str, cv_url: str, dice_url: str, push_supabase: bool = True, return_json: bool = False) -> Dict[str, Any]:
    """
    Main pipeline function for Railway API integration.
    
    Args:
        name: Candidate name
        email: Candidate email
        cv_url: URL or path to CV PDF file
        dice_url: URL or path to DICE test PDF file
        push_supabase: Whether to push results to Supabase
        return_json: Whether to return JSON response
    
    Returns:
        Dictionary containing profile and interview data
    """
    try:
        logger.info(f"Starting pipeline for candidate: {name}")
        
        # Step 1: Extract text from PDFs
        logger.info("Extracting text from PDF files...")
        cv_text = extract_text_from_pdf(cv_url)
        dice_text = extract_text_from_pdf(dice_url)
        
        # Step 2: Extract structured profile data
        logger.info("Extracting candidate profile data...")
        profile_data = extract_candidate_profile(cv_text, dice_text)
        
        # Step 3: Validate the extracted profile
        logger.info("Validating extracted profile...")
        is_valid = validate_profile(profile_data)
        
        if not is_valid:
            logger.warning("Profile validation failed - some fields may be missing")
        
        # Step 4: Generate interview conversation
        logger.info("Generating personalized interview conversation...")
        chat_data = generate_interview_chat(profile_data)
        
        if validate_interview_data(chat_data):
            logger.info("Interview generated successfully")
        else:
            logger.warning("Interview generation failed")
        
        # Step 5: Push to Supabase if requested
        if push_supabase:
            logger.info("🔗 Pushing candidate data to Supabase...")
            supabase_result = insert_candidate_to_supabase(
                profile_data=profile_data,
                chat_data=chat_data,
                cv_url=cv_url,
                dice_url=dice_url
            )
            
            if supabase_result:
                logger.info("✅ Successfully pushed to Supabase!")
            else:
                logger.warning("⚠️ Failed to push to Supabase - check credentials")
        
        # Step 6: Prepare response
        result = {
            "profile": profile_data,
            "interview": chat_data,
            "summary_notes": chat_data.get("summary_notes", ""),
            "memories": chat_data.get("memories", []),
            "status": "success"
        }
        
        logger.info(f"Successfully processed documents for: {name}")
        return result
        
    except Exception as e:
        logger.error(f"Error in pipeline: {e}")
        return {
            "status": "error",
            "error": str(e),
            "profile": {},
            "interview": {},
            "summary_notes": "",
            "memories": []
        }

class DocumentProcessor:
    """Main class for processing CV and DICE documents."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the document processor.
        
        Args:
            openai_api_key: OpenAI API key (optional, can be set via environment)
        """
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to the constructor.")
    
    def process_candidate_documents(self, cv_pdf_path: str, dice_pdf_path: str, output_path: Optional[str] = None, generate_interview: bool = False, push_to_supabase: bool = False) -> dict:
        """
        Process CV and DICE documents to extract candidate profile.
        
        Args:
            cv_pdf_path: Path to CV PDF file
            dice_pdf_path: Path to DICE test PDF file
            output_path: Optional path to save the extracted profile as JSON
            generate_interview: Whether to generate interview conversation
        
        Returns:
            Extracted candidate profile dictionary (with interview data if requested)
        """
        try:
            logger.info("Starting document processing...")
            
            # Step 1: Extract text from PDFs
            logger.info("Extracting text from PDF files...")
            cv_text, dice_text = extract_cv_and_dice_texts(cv_pdf_path, dice_pdf_path)
            
            # Step 2: Extract structured profile data
            logger.info("Extracting candidate profile data...")
            profile = extract_candidate_profile(cv_text, dice_text, self.api_key)
            
            # Step 3: Validate the extracted profile
            logger.info("Validating extracted profile...")
            is_valid = validate_profile(profile)
            
            if not is_valid:
                logger.warning("Profile validation failed - some fields may be missing")
            
            # Step 4: Generate interview if requested
            if generate_interview:
                logger.info("Generating personalized interview conversation...")
                interview_data = generate_interview_chat(profile, self.api_key)
                
                if validate_interview_data(interview_data):
                    profile['interview'] = interview_data
                    logger.info("Interview generated successfully")
                else:
                    logger.warning("Interview generation failed - profile saved without interview data")
            
            # Step 5: Save to file if output path provided
            if output_path:
                self._save_profile(profile, output_path)
            
            # Step 6: Push to Supabase if requested
            if push_to_supabase and 'interview' in profile:
                logger.info("🔗 Pushing candidate data to Supabase...")
                cv_url = f"anu.cv.uploads/{os.path.basename(cv_pdf_path)}"
                dice_url = f"anu.dice.uploads/{os.path.basename(dice_pdf_path)}"
                
                supabase_result = insert_candidate_to_supabase(
                    profile_data=profile,
                    chat_data=profile['interview'],
                    cv_url=cv_url,
                    dice_url=dice_url
                )
                
                if supabase_result:
                    logger.info("✅ Successfully pushed to Supabase!")
                else:
                    logger.warning("⚠️ Failed to push to Supabase - check credentials")
            
            logger.info(f"Successfully processed documents for: {profile.get('name', 'Unknown')}")
            return profile
            
        except Exception as e:
            logger.error(f"Error processing documents: {e}")
            raise
    
    def _save_profile(self, profile: dict, output_path: str):
        """Save the extracted profile to a JSON file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            logger.info(f"Profile saved to: {output_path}")
        except Exception as e:
            logger.error(f"Error saving profile to {output_path}: {e}")
            raise

def main():
    """Main function to run the document processing workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Recruiter Document Parser")
    parser.add_argument("--cv-pdf", required=True, help="Path to CV PDF file")
    parser.add_argument("--dice-pdf", required=True, help="Path to DICE test PDF file")
    parser.add_argument("--output", help="Output JSON file path for extracted profile")
    parser.add_argument("--api-key", help="OpenAI API key (optional, can use environment variable)")
    parser.add_argument("--generate-interview", action="store_true", help="Generate personalized interview conversation")
    parser.add_argument("--push-supabase", action="store_true", help="Push candidate data to Supabase database")
    parser.add_argument("--dry-run", action="store_true", help="Run without making API calls (for testing)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate input files
    if not Path(args.cv_pdf).exists():
        logger.error(f"CV PDF file not found: {args.cv_pdf}")
        return 1
    
    if not Path(args.dice_pdf).exists():
        logger.error(f"DICE PDF file not found: {args.dice_pdf}")
        return 1
    
    try:
        # Initialize processor
        processor = DocumentProcessor(openai_api_key=args.api_key)
        
        # Process documents
        profile = processor.process_candidate_documents(
            cv_pdf_path=args.cv_pdf,
            dice_pdf_path=args.dice_pdf,
            output_path=args.output,
            generate_interview=args.generate_interview,
            push_to_supabase=args.push_supabase
        )
        
        # Display results
        print("\n" + "="*50)
        print("EXTRACTED CANDIDATE PROFILE")
        print("="*50)
        
        # Display basic profile info
        basic_profile = {k: v for k, v in profile.items() if k != 'interview'}
        print(json.dumps(basic_profile, indent=2))
        
        # Display interview if generated
        if 'interview' in profile:
            print("\n" + "="*50)
            print("GENERATED INTERVIEW CONVERSATION")
            print("=" * 50)
            print(f"Summary: {profile['interview'].get('summary_notes', 'No summary')}")
            
            # Display memories if available
            if 'memories' in profile['interview'] and profile['interview']['memories']:
                print(f"\n📝 Memories ({len(profile['interview']['memories'])} captured):")
                for i, memory in enumerate(profile['interview']['memories'], 1):
                    print(f"  {i}. {memory}")
            
            print(f"\nChat Preview:")
            chat_preview = format_chat_for_display(profile['interview'])
            print(chat_preview[:800] + "..." if len(chat_preview) > 800 else chat_preview)
        
        if args.output:
            print(f"\nProfile saved to: {args.output}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 