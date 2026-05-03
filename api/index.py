from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

# Relative import when running locally or on Vercel
try:
    from .downloader import extract_video_info
    from .trending import get_trending_feed
    from .youtube import extract_channel_videos, cut_hot_segment
except ImportError:
    from downloader import extract_video_info
    from trending import get_trending_feed
    from youtube import extract_channel_videos, cut_hot_segment

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
    format: str = "mp4"

@app.post("/api/download")
def download_video(req: DownloadRequest):
    if not req.url:
        raise HTTPException(status_code=400, detail="URL is required")
        
    result = extract_video_info(req.url, req.format)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to extract video"))
        
    return result

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/trending")
def trending_videos(region: str = "VN"):
    result = get_trending_feed(region)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Failed to fetch trending videos")
    return result

@app.get("/api/youtube/channel")
def youtube_channel(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Channel or video URL is required")
    result = extract_channel_videos(url)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@app.post("/api/youtube/cut")
def youtube_cut(req: DownloadRequest):
    if not req.url:
        raise HTTPException(status_code=400, detail="Video URL is required")
    result = cut_hot_segment(req.url)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result
