# API Documentation

Ngày cập nhật: 2026-05-02
Base URL: http://localhost:8000

---

## 📹 Video Download

### POST /api/download
Tải video từ TikTok hoặc Instagram Reels không dính watermark (logo).

**Request:**
```json
{
  "url": "https://www.tiktok.com/@mrbeast/video/123456789"
}
```

**Response (200):**
```json
{
  "success": true,
  "title": "Video Title",
  "thumbnail": "https://...",
  "video_url": "https://...",
  "source_url": "https://..."
}
```

**Errors:**
- 400: URL is required
- 400: Failed to extract video

---

## 🔥 Trending Videos

### GET /api/trending
Lấy danh sách các video đang thịnh hành (Trending) tại một quốc gia (Region). Trả về danh sách được xếp hạng bằng điểm Hot Score.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| region | string | VN | Mã quốc gia (VN, CN, US, KR, JP, TH) |

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "123456789",
      "title": "Amazing Video",
      "cover": "https://...",
      "views": 1000000,
      "likes": 100000,
      "comments": 5000,
      "shares": 2000,
      "hot_score": 15.5,
      "url": "https://www.tiktok.com/@username/video/123456789"
    }
  ]
}
```

**Errors:**
- 400: Failed to fetch trending videos

---

## ⚙️ System

### GET /api/health
Kiểm tra trạng thái server.

**Response (200):**
```json
{
  "status": "ok"
}
```
