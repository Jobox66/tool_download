import requests
try:
    res = requests.get("https://tikwm.com/api/feed/?region=US&count=5")
    data = res.json()
    if data.get("code") == 0:
        videos = data.get("data", [])
        print("Success, got", len(videos), "videos")
        for v in videos[:2]:
            print(f"Title: {v.get('title')} | Play: {v.get('play_count')} | Likes: {v.get('digg_count')}")
    else:
        print("Failed:", data)
except Exception as e:
    print("Error:", e)
