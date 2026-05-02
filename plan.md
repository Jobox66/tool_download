# Kế Hoạch Triển Khai: Dashboard Đánh Giá & Tải Video Hot

Bản kế hoạch này mô tả chi tiết các bước để xây dựng tính năng phân tích, lọc và tải hàng loạt các video đang "Hot" (Trending) trên TikTok, giúp tăng hiệu quả xây kênh (reup).

## Cần Người Dùng Phê Duyệt

> [!IMPORTANT]
> **1. Nguồn Dữ Liệu (API)**
> Lấy danh sách video hàng loạt từ TikTok là một tác vụ khó vì cơ chế chống bot (Cloudflare).
> - **Đề xuất của tôi:** Tạm thời xây dựng hệ thống sử dụng **Mock Data (Dữ liệu giả)** để bạn xem giao diện và tính năng lọc/đánh giá hoạt động thế nào. Đồng thời, tôi sẽ thử gọi API miễn phí từ `tikwm.com/api/user/posts` (nếu API này còn sống thì sẽ lấy được video thật của một kênh).
> - Nếu bạn có sẵn API key của các dịch vụ như **TikAPI** hay **RapidAPI**, hãy cung cấp để tôi thay thế, hệ thống sẽ cực kỳ ổn định.
> *Vui lòng xác nhận bạn có đồng ý làm với Mock Data / Free API trước không?*

> [!IMPORTANT]
> **2. Công thức tính "Độ Hot" (Hot Score)**
> Để đánh giá video nào đáng tải, tôi đề xuất thuật toán sau:
> `Hot Score = (Likes * 1 + Comments * 2 + Shares * 3) / Views * 100`
> *(Shares và Comments được đánh giá cao hơn vì đòi hỏi nhiều tương tác từ người dùng).*
> Hệ thống cũng sẽ cho phép lọc thủ công: **"Chỉ hiển thị video > 100,000 Views"**.
> *Bạn có muốn thay đổi công thức hoặc bộ lọc này không?*

## Chi Tiết Các Thay Đổi Đề Xuất

### 1. Backend (Python FastAPI)

Cần thêm một endpoint để gọi danh sách video và chỉ số tương tác (Views, Likes, Comments, v.v.).

#### [NEW] `api/trending.py`
- Tách riêng logic lấy video trending để code gọn gàng.
- Hàm `get_user_videos(username)`: Nhận username, trả về danh sách video. Nếu gọi API thật thất bại, sẽ trả về Mock Data gồm 10 video giả lập với số Views/Likes ngẫu nhiên để test UI.

#### [MODIFY] `api/index.py`
- Bổ sung route: `@app.get("/api/trending")`.
- Route này sẽ gọi hàm `get_user_videos` từ `api/trending.py`.

### 2. Frontend (Next.js & Vanilla CSS)

Xây dựng trang Dashboard riêng biệt.

#### [MODIFY] `src/app/layout.tsx` (hoặc `page.tsx`)
- Thêm thanh Menu (Navigation Bar) phía trên cùng để chuyển đổi giữa 2 tab: 
  - **Single Download (Trang chủ hiện tại)**
  - **Trending Dashboard (Trang mới)**

#### [NEW] `src/app/trending/page.tsx`
- **Thanh tìm kiếm:** Ô input cho phép nhập tên kênh TikTok (vd: `@hoaa.hanassii`).
- **Bộ lọc (Filter):** Slider chọn mức Views tối thiểu (vd: > 1M views).
- **Khu vực hiển thị (Grid):**
  - Hiển thị danh sách video dạng lưới.
  - Mỗi thẻ video hiện ảnh bìa, số View, Like, Comment, và điểm **Hot Score**.
  - Các thẻ tự động sắp xếp theo Hot Score từ cao xuống thấp.
  - Nút **"Tải Video"** trực tiếp (gọi đến API `/api/download` đã làm trước đó).

#### [NEW] `src/app/trending/page.module.css`
- Sử dụng Vanilla CSS với phong cách Glassmorphism và màu sắc hiện đại tương tự trang chủ.
- Responsive dạng Grid: 1 cột (Mobile), 2 cột (Tablet), 3-4 cột (Desktop).

## Kế Hoạch Kiểm Thử (Verification Plan)

### Automated Tests
- *(Theo quy tắc AGENTS.md mới)* Tạo file test `tests/api/test_trending.py`.
- Viết test bằng `pytest` đảm bảo `/api/trending` trả về mảng dữ liệu chuẩn xác, công thức Hot Score tính đúng.
- Lệnh chạy: `pytest tests/api/test_trending.py`.

### Manual Verification
1. Mở trình duyệt, truy cập tab **Trending Dashboard**.
2. Nhập một kênh bất kỳ (vd: `@mrbeast`).
3. Kiểm tra xem danh sách video có hiện ra với đầy đủ thông số Views/Likes/Shares không.
4. Kéo thanh Slider lọc View xem danh sách có thay đổi real-time không.
5. Bấm "Tải Video" trên một thẻ bất kỳ xem video tải về có thành công và không dính watermark không.
