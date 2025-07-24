"""
PDF Text Extraction Utility
Extracts raw text from CV and DICE PDF files for processing by parse_documents.py
"""

import pdfplumber
import PyPDF2
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str, method: str = "pdfplumber") -> str:
    """
    Extract text from a PDF file using the specified method.
    
    Args:
        pdf_path: Path to the PDF file
        method: Extraction method ("pdfplumber" or "pypdf2")
    
    Returns:
        Extracted text as string
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    try:
        if method == "pdfplumber":
            return _extract_with_pdfplumber(pdf_path)
        elif method == "pypdf2":
            return _extract_with_pypdf2(pdf_path)
        else:
            raise ValueError(f"Unknown extraction method: {method}")
    except Exception as e:
        logger.error(f"Error extracting text from {pdf_path}: {e}")
        raise

def _extract_with_pdfplumber(pdf_path: Path) -> str:
    """Extract text using pdfplumber (better for complex layouts)."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"pdfplumber extraction failed: {e}")
        raise

def _extract_with_pypdf2(pdf_path: Path) -> str:
    """Extract text using PyPDF2 (faster for simple layouts)."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"PyPDF2 extraction failed: {e}")
        raise

def extract_cv_and_dice_texts(cv_pdf_path: str, dice_pdf_path: str) -> tuple[str, str]:
    """
    Extract text from both CV and DICE PDF files.
    
    Args:
        cv_pdf_path: Path to CV PDF file
        dice_pdf_path: Path to DICE test PDF file
    
    Returns:
        Tuple of (cv_text, dice_text)
    """
    logger.info(f"Extracting CV text from: {cv_pdf_path}")
    cv_text = extract_text_from_pdf(cv_pdf_path)
    
    logger.info(f"Extracting DICE text from: {dice_pdf_path}")
    dice_text = extract_text_from_pdf(dice_pdf_path)
    
    return cv_text, dice_text

# Example usage
if __name__ == "__main__":
    # Test with sample files (if they exist)
    import os
    
    cv_path = "sample_cv.pdf"
    dice_path = "sample_dice.pdf"
    
    if os.path.exists(cv_path) and os.path.exists(dice_path):
        cv_text, dice_text = extract_cv_and_dice_texts(cv_path, dice_path)
        print("CV Text Preview:")
        print(cv_text[:500] + "..." if len(cv_text) > 500 else cv_text)
        print("\nDICE Text Preview:")
        print(dice_text[:500] + "..." if len(dice_text) > 500 else dice_text)
    else:
        print("Sample PDF files not found. Please provide valid PDF paths.") 