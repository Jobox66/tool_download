import requests
try:
    res = requests.get("https://tikwm.com/api/user/posts?unique_id=@mrbeast&count=5")
    data = res.json()
    if data.get("code") == 0:
        videos = data.get("data", {}).get("videos", [])
        print("Success, got", len(videos), "videos")
    else:
        print("Failed:", data)
except Exception as e:
    print("Error:", e)
