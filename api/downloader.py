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

def extract_video_info(url: str):
    # Dùng API chuyên dụng cho TikTok để tránh bị block (Unable to extract webpage video data)
    if "tiktok.com" in url.lower():
        tiktok_res = extract_tiktok(url)
        if tiktok_res.get("success"):
            return tiktok_res

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
