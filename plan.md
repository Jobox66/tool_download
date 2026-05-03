# Kế Hoạch Triển Khai: Cỗ Máy Tạo Video Reup (TikTok & YouTube)

Bản kế hoạch này mô tả chi tiết các bước để xây dựng hệ thống tải video đa nền tảng và **Tính năng mới: Tự động cắt video ngắn từ đoạn Hot nhất trên YouTube**.

## 🔴 Cần Người Dùng Phê Duyệt

> [!IMPORTANT]
> **1. Yêu cầu hệ thống (FFmpeg)**
> Để tính năng cắt video hoạt động, máy tính của bạn BẮT BUỘC phải có `ffmpeg`. 
> - *Câu hỏi:* Máy tính của bạn đã có sẵn `ffmpeg` chưa? Nếu chưa, tôi có thể thiết lập để hệ thống tự động tải `ffmpeg.exe` về thư mục dự án cho bạn. Bạn muốn tôi làm theo cách nào?

> [!IMPORTANT]
> **2. Định dạng Video cắt ra (Shorts/Reels)**
> Khi cắt đoạn "được xem nhiều nhất" (Heatmap Peak), video gốc thường có tỷ lệ ngang (16:9).
> - *Câu hỏi 1:* Bạn có muốn hệ thống **tự động crop (cắt lẹm hai bên)** khung hình thành tỷ lệ dọc 9:16 để đăng Shorts/TikTok không, hay giữ nguyên tỷ lệ gốc ngang 16:9?
> - *Câu hỏi 2:* Độ dài của video cắt ra nên là bao nhiêu giây? (Ví dụ: Lấy chính xác điểm Hot nhất làm trung tâm, lùi về trước 15 giây và tiến tới 15 giây để tạo ra clip dài tròn 30 giây?).

## Chi Tiết Các Tính Năng Mới Đề Xuất

### Phần 1: Bổ Sung Nguồn Download Từ YouTube
- Hệ thống tải đơn (Single Download) hiện tại đã sử dụng `yt-dlp` làm fallback. Tôi sẽ làm rõ trên UI và tinh chỉnh logic Backend để tối ưu tốc độ khi dán link YouTube (Hỗ trợ cả link Shorts, link Video dài và Playlist cơ bản).

### Phần 2: Công Cụ "Auto Shorts Cutter" (Cắt đoạn YouTube Hot nhất)

#### 1. Backend (Python FastAPI)
- **Cài đặt thư viện:** Đảm bảo `yt-dlp` bản mới nhất để lấy dữ liệu `heatmap` của YouTube.
- **[NEW] `api/youtube.py`:**
  - `get_channel_videos(channel_url)`: Quét kênh YouTube và lấy danh sách video mới nhất.
  - `find_best_segment(video_url)`: Gọi `yt-dlp` (với tùy chọn `skip_download=True`) để trích xuất dữ liệu `heatmap` (biểu đồ lượt xem lại). Tìm ra mốc thời gian có `value == 1.0` (đỉnh của video).
  - `cut_video_segment(video_url, start_time, end_time)`: Sử dụng `yt-dlp` kết hợp `ffmpeg` để chỉ tải xuống và cắt đúng đoạn thời gian đó (tiết kiệm băng thông thay vì tải cả video dài 2 tiếng). Có thể thêm lệnh `ffmpeg` crop 9:16 ở bước này.
- **[MODIFY] `api/index.py`:** Thêm các endpoint `/api/youtube/analyze` và `/api/youtube/cut`.

#### 2. Frontend (Next.js)
- **[MODIFY] `src/app/layout.tsx`:** Bổ sung thêm tab thứ 3 vào thanh Navigation: **"YT Shorts Cutter"**.
- **[NEW] `src/app/yt-cutter/page.tsx`:** 
  - Giao diện nhập Link Kênh YouTube (hoặc Link 1 Video YouTube dài bất kỳ).
  - Hiển thị danh sách video. Khi bấm "Analyze", hệ thống sẽ chỉ ra **Đoạn được xem nhiều nhất** (Ví dụ: `12:05 - 12:45`).
  - Nút **"✂️ Tạo Video Ngắn (Short)"**: Gọi API cắt video và trả về file `.mp4` trực tiếp cho người dùng.
- **[NEW] `src/app/yt-cutter/page.module.css`:** Style giao diện tương đồng với Trending Dashboard.

## Kế Hoạch Kiểm Thử (Verification Plan)

### Automated Tests
- Bổ sung file `tests/api/test_youtube.py`.
- Viết test cho hàm tìm kiếm Heatmap đảm bảo thuật toán luôn bắt được đỉnh cao nhất của video.

### Manual Verification
1. Dán 1 link video Podcast dài (như của Joe Rogan hoặc video kể chuyện dài 1 tiếng).
2. Kiểm tra xem hệ thống có tìm đúng phân đoạn gay cấn nhất (được tua lại nhiều nhất) không.
3. Bấm "Cắt Video", chờ hệ thống xử lý và tải file MP4 về.
4. Mở file MP4 kiểm tra xem độ mượt, chất lượng âm thanh/hình ảnh và tỷ lệ khung hình có đúng như yêu cầu không.
