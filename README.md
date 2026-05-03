# 🎬 Universal Video Downloader & Reup Tool

All-in-one web tool for downloading videos from **TikTok**, **Instagram Reels**, and **YouTube** (MP4/MP3). Includes a **Trending Dashboard** to scout hot videos by region and a **YouTube Auto Cutter** that finds the most-replayed segment of any video.

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## ✨ Features

| Feature | Description |
|---|---|
| **Single Download** | Paste a TikTok / Instagram Reels / YouTube link → get a clean MP4 or MP3 |
| **Trending Dashboard** | Browse trending videos from 🇻🇳 VN, 🇨🇳 CN, 🇺🇸 US, 🇰🇷 KR, 🇯🇵 JP, 🇹🇭 TH |
| **YT Shorts Cutter** | Analyze YouTube heatmap → auto-cut the most replayed segment |
| **Format Selection** | Choose between MP4 (video) and MP3 (audio) for YouTube downloads |

## 🛠️ Tech Stack

- **Frontend:** Next.js 16, React 19, CSS Modules (Glassmorphism)
- **Backend:** Python FastAPI, yt-dlp, FFmpeg
- **Deployment:** Vercel (Serverless)

## 🚀 Quick Start

### Prerequisites

- [Node.js](https://nodejs.org/) ≥ 18
- [Python](https://www.python.org/) ≥ 3.10
- [FFmpeg](https://ffmpeg.org/) (required for YouTube MP3 & Auto Cutter)

### Install & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/Jobox66/tool_download.git
cd tool_download

# 2. Install frontend dependencies
npm install

# 3. Create Python virtual environment & install backend deps
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt

# 4. Run both servers (in separate terminals)
npm run dev            # → http://localhost:3000
uvicorn api.index:app --reload --port 8000   # → http://localhost:8000
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
tool_download/
├── api/                    # Python FastAPI backend
│   ├── index.py            # Main router & endpoints
│   ├── downloader.py       # TikTok / Instagram / YouTube download logic
│   ├── trending.py         # Trending feed (tikwm API)
│   └── youtube.py          # YT channel scan & heatmap cutter
├── src/app/                # Next.js frontend
│   ├── page.tsx            # Single Download page
│   ├── trending/           # Trending Dashboard page
│   └── yt-cutter/          # YouTube Auto Cutter page
├── tests/                  # Pytest test suite
├── vercel.json             # Vercel deployment config
├── requirements.txt        # Python dependencies
└── package.json            # Node.js dependencies
```

## 🌐 Deploy to Vercel

1. Push your code to GitHub.
2. Go to [vercel.com/new](https://vercel.com/new) → Import your GitHub repo.
3. Vercel auto-detects Next.js + Python API routes. Click **Deploy**.

> **Note:** YouTube download/cut features require `yt-dlp` and `FFmpeg`, which have limited support in Vercel's serverless environment (10 s timeout on Free plan). TikTok download and Trending Dashboard work perfectly on Vercel. For full YouTube support, consider self-hosting or upgrading to Vercel Pro (60 s timeout).

## ⚠️ Limitations on Vercel

| Feature | Vercel Free | Vercel Pro | Self-hosted |
|---|:---:|:---:|:---:|
| TikTok Download | ✅ | ✅ | ✅ |
| Instagram Download | ✅ | ✅ | ✅ |
| Trending Dashboard | ✅ | ✅ | ✅ |
| YouTube MP4/MP3 | ⚠️ | ✅ | ✅ |
| YT Shorts Cutter | ❌ | ⚠️ | ✅ |

## 🧪 Running Tests

```bash
# Activate venv first, then:
pytest tests/api/test_trending.py
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
