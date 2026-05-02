import yt_dlp
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'noplaylist': True,
    'quiet': False,
    'impersonate': 'chrome',
}
url = "https://www.tiktok.com/@mrbeast/video/7405957169453059348"
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    print("Success:", info.get('title'))
