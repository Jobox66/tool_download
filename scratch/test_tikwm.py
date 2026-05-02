import requests
url = "https://www.tiktok.com/@mrbeast/video/7405957169453059348"
try:
    res = requests.get(f"https://tikwm.com/api/?url={url}")
    data = res.json()
    if data.get("code") == 0:
        info = data.get("data", {})
        print("Success:", info.get("title"))
        print("Video URL:", info.get("play"))
    else:
        print("Failed:", data)
except Exception as e:
    print("Error:", e)
