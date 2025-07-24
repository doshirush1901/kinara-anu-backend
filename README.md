# 🤖 AI Recruiter Document Parser (Anu)

A sophisticated document parsing system for AI-powered recruitment that extracts structured candidate data from CV and DICE personality test PDFs.

## 🎯 Features

- **CV Parsing**: Extracts skills, CAD tools, projects, and contact information
- **DICE Analysis**: Processes personality test results for interview tone matching
- **Personalized Interviews**: Generates mentor-style interview conversations
- **Structured Output**: Returns clean JSON with candidate profiles and chat logs
- **PDF Support**: Handles complex PDF layouts with multiple extraction methods
- **Error Handling**: Robust error handling with fallback mechanisms

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- PDF files (CV and DICE test results)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd Kinara_Recruit_Anu

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key and Supabase credentials
```

### 2. Environment Setup

Run the setup script to create your `.env` file:
```bash
python setup_env.py
```

This will create a `.env` file from the template. Edit it to add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Check your environment setup:
```bash
python setup_env.py --check
```

Test your connections:
```bash
# Test OpenAI API
python test_openai.py

# Test Supabase connection
python test_supabase.py
```

### 3. Basic Usage

```bash
# Process CV and DICE documents
python main.py --cv-pdf path/to/cv.pdf --dice-pdf path/to/dice.pdf --output profile.json

# Generate personalized interview conversation
python main.py --cv-pdf cv.pdf --dice-pdf dice.pdf --generate-interview --output profile.json

# With verbose logging
python main.py --cv-pdf cv.pdf --dice-pdf dice.pdf --output profile.json --verbose

# Push to Supabase database
python main.py --cv-pdf cv.pdf --dice-pdf dice.pdf --generate-interview --push-supabase --output profile.json

# Dry run (for testing without API calls)
python main.py --cv-pdf cv.pdf --dice-pdf dice.pdf --dry-run --verbose
```

## 📁 File Structure

```
Kinara_Recruit_Anu/
├── main.py              # Main orchestrator
├── parse_documents.py   # CV/DICE parsing logic
├── interview_prompt.py  # Interview conversation generator
├── pdf_extractor.py     # PDF text extraction utilities
├── supabase_insert.py   # Supabase database integration
├── setup_env.py         # Environment setup script
├── test_openai.py       # OpenAI API connection test
├── test_supabase.py     # Supabase connection test
├── env.example          # Environment variables template
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env               # Environment variables (create this)
```

## 🔧 API Reference

### `parse_documents.py`

#### `extract_candidate_profile(cv_text, dice_text, api_key=None)`

Extracts structured candidate data from CV and DICE test text.

**Parameters:**
- `cv_text` (str): Raw text from CV PDF
- `dice_text` (str): Raw text from DICE test PDF
- `api_key` (str, optional): OpenAI API key

**Returns:**
```json
{
  "name": "Candidate Name",
  "email": "candidate@email.com",
  "skills": ["SolidWorks", "Fusion 360", "CAM Programming"],
  "cad_tools": ["SolidWorks", "Fusion 360"],
  "projects": ["Drone kill switch circuit", "Tool design for vacuum forming mold"],
  "personality_type": "High C, Mid D",
  "tone_profile": "structured and logical"
}
```

### `pdf_extractor.py`

#### `extract_text_from_pdf(pdf_path, method="pdfplumber")`

Extracts text from PDF files using specified method.

**Parameters:**
- `pdf_path` (str): Path to PDF file
- `method` (str): "pdfplumber" or "pypdf2"

**Returns:**
- `str`: Extracted text content

### `interview_prompt.py`

#### `generate_interview_chat(profile_data, api_key=None)`

Generates personalized interview conversations between Anu and candidates.

**Parameters:**
- `profile_data` (dict): Extracted candidate profile
- `api_key` (str, optional): OpenAI API key

**Returns:**
```json
{
  "chat_log": [
    {"role": "Anu", "message": "Hi Samiya! I'm Anu from Kinara..."},
    {"role": "Candidate", "message": "Hi Anu! Nice to meet you..."}
  ],
  "answers": {
    "location": "Mumbai",
    "education_status": "Recently graduated",
    "cad_tools": "Fusion 360, SolidWorks",
    "relocation": "Yes, open to relocate",
    "salary_expectation": "4-5 LPA"
  },
  "summary_notes": "Candidate shows strong technical skills and flexibility..."
}
```

## 🧪 Testing

### Test with Sample Data

```python
# Run the built-in test
python parse_documents.py
```

### Test PDF Extraction

```python
# Test PDF text extraction
python pdf_extractor.py
```

## 📊 Example Output

```json
{
  "name": "Samiya Naik",
  "email": "samiya@example.com",
  "skills": [
    "SolidWorks",
    "Fusion 360", 
    "CAM Programming",
    "3D Modeling"
  ],
  "cad_tools": [
    "Fusion 360",
    "SolidWorks"
  ],
  "projects": [
    "Drone kill switch circuit design",
    "Tool design for vacuum forming mold"
  ],
  "personality_type": "High C, Mid D",
  "tone_profile": "structured and mentor-like",
  "interview": {
    "chat_log": [
      {"role": "Anu", "message": "Hi Samiya! I'm Anu from Kinara. Where are you currently based?"},
      {"role": "Candidate", "message": "Hi Anu! I'm based in Mumbai."}
    ],
    "answers": {
      "location": "Mumbai",
      "education_status": "Recently graduated",
      "cad_tools": "Fusion 360, SolidWorks",
      "relocation": "Yes, open to relocate"
    },
    "summary_notes": "Samiya shows strong technical skills and flexibility for relocation."
  }
}
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```bash
   # Use the setup script
   python setup_env.py
   # Edit .env file and add your API key
   
   # Or set environment variable directly
   export OPENAI_API_KEY=your_key_here
   
   # Or use --api-key flag
   python main.py --api-key your_key_here --cv-pdf cv.pdf --dice-pdf dice.pdf
   ```

2. **PDF Extraction Issues**
   - Try different extraction methods: `--method pdfplumber` or `--method pypdf2`
   - Ensure PDF files are not password-protected
   - Check if PDF contains selectable text

3. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Debug Mode

```bash
# Enable verbose logging
python main.py --cv-pdf cv.pdf --dice-pdf dice.pdf --verbose
```

## 🔄 Integration

### Programmatic Usage

```python
from main import DocumentProcessor

# Initialize processor
processor = DocumentProcessor()

# Process documents
profile = processor.process_candidate_documents(
    cv_pdf_path="path/to/cv.pdf",
    dice_pdf_path="path/to/dice.pdf",
    output_path="profile.json"
)

print(f"Extracted profile for: {profile['name']}")
```

### Next Steps

This system is designed to integrate with:
- **Interview System**: Use `tone_profile` for personalized interview flows
- **Database Storage**: Save extracted profiles to Supabase/PostgreSQL
- **Matching Engine**: Compare skills and personality with job requirements

## 📝 License

This project is part of the Kinara AI Recruiter system.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Ready for the next step?** 🚀

- Want the `interview_prompt.py` for mentor-style chat flows?
- Need the Supabase integration for profile storage?
- Looking for the matching engine to compare candidates?

Let me know what you'd like to build next! 