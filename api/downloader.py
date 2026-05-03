import yt_dlp
import requests

def extract_tiktok(url: str):
    try:
        res = requests.get(f"https://tikwm.com/api/?url={url}", timeout=10)
        data = res.json()
        if data.get("code") == 0:
            info = data.get("data", {})
            return {
                "success": True,
                "title": info.get("title", "TikTok Video"),
                "thumbnail": info.get("cover"),
                "video_url": info.get("play"),
                "source_url": url,
            }
        return {"success": False, "error": data.get("msg", "Failed to extract TikTok video")}
    except Exception as e:
        return {"success": False, "error": str(e)}

import os

def download_youtube(url: str, format: str):
    try:
        os.makedirs("public/downloads", exist_ok=True)
        # Extract info first
        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            vid = info.get('id', 'video')
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail')
            
        ext = "mp3" if format == "mp3" else "mp4"
        output_filename = f"public/downloads/{vid}.{ext}"
        
        # Check if already downloaded
        if not os.path.exists(output_filename):
            ydl_opts = {
                'outtmpl': f"public/downloads/{vid}.%(ext)s", # yt-dlp replaces %(ext)s
                'quiet': True,
                'noplaylist': True,
            }
            if format == "mp3":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                ydl_opts['outtmpl'] = output_filename # MP4 will be directly saved as mp4
                
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
        return {
            "success": True,
            "title": title,
            "thumbnail": thumbnail,
            "video_url": f"/downloads/{vid}.{ext}",
            "source_url": url,
            "format": ext
        }
    except Exception as e:
        return {"success": False, "error": f"Lỗi tải YouTube: {str(e)}"}

def extract_video_info(url: str, format: str = "mp4"):
    # Dùng API chuyên dụng cho TikTok để tránh bị block
    if "tiktok.com" in url.lower():
        tiktok_res = extract_tiktok(url)
        if tiktok_res.get("success"):
            return tiktok_res

    # Tải YouTube với tùy chọn định dạng mp4/mp3
    if "youtube.com" in url.lower() or "youtu.be" in url.lower():
        return download_youtube(url, format)

    # Fallback to yt-dlp cho Instagram Reels hoặc các trang khác
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get('url', None)
            title = info_dict.get('title', 'Video')
            thumbnail = info_dict.get('thumbnail', None)
            
            return {
                "success": True,
                "title": title,
                "thumbnail": thumbnail,
                "video_url": video_url,
                "source_url": url,
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
