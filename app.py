from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from main import run_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Anu AI Recruiter API",
    description="AI-powered candidate processing and interview generation",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Anu AI Recruiter API is running!", "status": "healthy"}

@app.post("/api/process_candidate")
async def process_candidate(request: Request):
    """
    Process candidate CV and DICE documents to generate profile and interview.
    
    Expected JSON body:
    {
        "name": "Candidate Name",
        "email": "candidate@example.com", 
        "cv_url": "path/to/cv.pdf",
        "dice_url": "path/to/dice.pdf"
    }
    """
    try:
        # Parse request body
        body = await request.json()
        
        # Validate required fields
        required_fields = ["name", "email", "cv_url", "dice_url"]
        for field in required_fields:
            if field not in body:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Missing required field: {field}"
                )
        
        logger.info(f"Processing candidate: {body['name']}")
        
        # Run the pipeline
        result = run_pipeline(
            name=body["name"],
            email=body["email"],
            cv_url=body["cv_url"],
            dice_url=body["dice_url"],
            push_supabase=True,
            return_json=True
        )
        
        # Check if pipeline was successful
        if result.get("status") == "error":
            logger.error(f"Pipeline failed: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=f"Processing failed: {result.get('error')}"
            )
        
        logger.info(f"Successfully processed candidate: {body['name']}")
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing candidate: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "Anu AI Recruiter API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 