import requests
import random

def calculate_hot_score(likes: int, comments: int, shares: int, views: int) -> float:
    if views == 0:
        return 0
    return round((likes * 1 + comments * 2 + shares * 3) / views * 100, 2)

def get_trending_feed(region: str = "VN"):
    # Try free API for feed list
    api_url = f"https://www.tikwm.com/api/feed/list?region={region}&count=20"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        if data.get("code") == 0 and data.get("data"):
            videos = []
            for item in data.get("data", []):
                views = item.get("play_count", 0)
                likes = item.get("digg_count", 0)
                comments = item.get("comment_count", 0)
                shares = item.get("share_count", 0)
                
                hot_score = calculate_hot_score(likes, comments, shares, views)
                
                # author username is needed for the URL
                author = item.get("author", {})
                username = author.get("unique_id", "unknown")
                
                videos.append({
                    "id": item.get("video_id"),
                    "title": item.get("title", ""),
                    "cover": item.get("cover"),
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "hot_score": hot_score,
                    "url": f"https://www.tiktok.com/@{username}/video/{item.get('video_id')}"
                })
            
            # Sort by hot_score descending
            videos.sort(key=lambda x: x["hot_score"], reverse=True)
            return {"success": True, "data": videos}
    except Exception as e:
        print(f"Failed to fetch feed data: {e}")
        pass
        
    # Fallback to Mock Data
    print("Using Mock Data for trending dashboard")
    mock_videos = []
    
    # Real video for testing download
    mock_videos.append({
        "id": "7272990666016148738",
        "title": "Real Video (Test Download)",
        "cover": "https://placehold.co/400x600/ef4444/ffffff.png?text=REAL%0AVIDEO",
        "views": 5000000,
        "likes": 500000,
        "comments": 10000,
        "shares": 50000,
        "hot_score": calculate_hot_score(500000, 10000, 50000, 5000000),
        "url": "https://www.tiktok.com/@hoaa.hanassii/video/7272990666016148738"
    })
    
    for i in range(1, 12):
        views = random.randint(10000, 5000000)
        likes = int(views * random.uniform(0.05, 0.2))
        comments = int(likes * random.uniform(0.01, 0.1))
        shares = int(likes * random.uniform(0.05, 0.15))
        hot_score = calculate_hot_score(likes, comments, shares, views)
        
        mock_videos.append({
            "id": f"mock_vid_{i}",
            "title": f"Mock Video {i} - Awesome Content",
            "cover": f"https://placehold.co/400x600/333333/ffffff.png?text=Mock%0AVideo+{i}",
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "hot_score": hot_score,
            "url": f"https://www.tiktok.com/@{username}/video/mock_{i}"
        })
        
    mock_videos.sort(key=lambda x: x["hot_score"], reverse=True)
    return {"success": True, "data": mock_videos, "is_mock": True}
