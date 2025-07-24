from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from main import run_pipeline

app = FastAPI()

# ✅ Allow all CORS origins (you can later restrict to Lovable URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Anu backend is live"}

@app.post("/api/process_candidate")
async def process_candidate(request: Request):
    try:
        body = await request.json()
        print("📥 Received:", body)

        result = run_pipeline(
            name=body["name"],
            email=body["email"],
            cv_url=body["cv_url"],
            dice_url=body["dice_url"],
            push_supabase=True,
            return_json=True
        )

        return {
            "status": "success",
            "summary_notes": result.get("summary_notes", ""),
            "answers": result.get("interview", {}).get("answers", {})
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)}) 