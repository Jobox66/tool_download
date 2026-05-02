from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

# Relative import when running locally or on Vercel
try:
    from .downloader import extract_video_info
except ImportError:
    from downloader import extract_video_info

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str

@app.post("/api/download")
def download_video(req: DownloadRequest):
    if not req.url:
        raise HTTPException(status_code=400, detail="URL is required")
        
    result = extract_video_info(req.url)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to extract video"))
        
    return result

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
