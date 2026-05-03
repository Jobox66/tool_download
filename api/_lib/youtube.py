import yt_dlp
import os

# On Vercel, only /tmp is writable. Locally, use public/downloads.
DOWNLOAD_DIR = "/tmp/downloads" if os.environ.get("VERCEL") else "public/downloads"

def extract_channel_videos(channel_url: str):
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'quiet': True,
        'skip_download': True,
        'playlist_end': 20,
    }
    videos = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    videos.append({
                        'id': entry.get('id'),
                        'title': entry.get('title'),
                        'url': entry.get('url'),
                        'duration': entry.get('duration'),
                        'view_count': entry.get('view_count'),
                    })
            else:
                # If it's a single video URL
                videos.append({
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'url': info.get('webpage_url', channel_url),
                    'duration': info.get('duration'),
                    'view_count': info.get('view_count'),
                })
        return {"success": True, "data": videos}
    except Exception as e:
        return {"success": False, "error": str(e)}

def find_hot_segments(heatmap: list) -> list:
    """Find contiguous hot segments where heatmap value >= 0.8 (top 20%).
    Returns a list of {'start_time', 'end_time', 'peak_value'} sorted by peak_value desc.
    """
    if not heatmap:
        return []

    threshold = 0.8
    segments = []
    current_start = None
    current_peak = 0

    for point in heatmap:
        value = point.get('value', 0)
        if value >= threshold:
            if current_start is None:
                current_start = point['start_time']
            current_peak = max(current_peak, value)
        else:
            if current_start is not None:
                segments.append({
                    'start_time': current_start,
                    'end_time': point['start_time'],
                    'peak_value': current_peak
                })
                current_start = None
                current_peak = 0

    # Close last segment if it extends to the end
    if current_start is not None:
        segments.append({
            'start_time': current_start,
            'end_time': heatmap[-1]['end_time'],
            'peak_value': current_peak
        })

    segments.sort(key=lambda s: s['peak_value'], reverse=True)
    return segments

def cut_hot_segment(video_url: str):
    try:
        ydl_opts_info = {'quiet': True, 'skip_download': True}

        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(video_url, download=False)
            heatmap = info.get('heatmap', [])
            vid = info.get('id', 'video')

            if not heatmap:
                return {"success": False, "error": "Video này không có dữ liệu Heatmap (đoạn được xem lại nhiều nhất) từ YouTube."}

        # Find the hottest contiguous segment
        segments = find_hot_segments(heatmap)
        if not segments:
            # Fallback to single peak point
            best_point = max(heatmap, key=lambda x: x.get('value', 0))
            start_time = best_point['start_time']
            end_time = best_point['end_time']
        else:
            best = segments[0]
            start_time = best['start_time']
            end_time = best['end_time']

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        output_filename = os.path.join(DOWNLOAD_DIR, f"yt_short_{vid}.mp4")

        # On Vercel serverless: return direct stream URL with time range info
        if os.environ.get("VERCEL"):
            return {
                "success": True,
                "message": f"Đoạn hot nhất: {start_time:.1f}s - {end_time:.1f}s. Trên Vercel không thể cắt trực tiếp, vui lòng dùng bản local.",
                "start_time": start_time,
                "end_time": end_time,
                "download_url": None
            }

        # If file already exists, just return it
        if os.path.exists(output_filename):
            return {
                "success": True,
                "message": "Video đã được cắt từ trước",
                "start_time": start_time,
                "end_time": end_time,
                "download_url": f"/downloads/yt_short_{vid}.mp4"
            }

        def download_range_func(info_dict, ydl):
            return [{'start_time': start_time, 'end_time': end_time}]

        ydl_opts_download = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'download_ranges': download_range_func,
            'outtmpl': output_filename,
            'quiet': True,
            'noplaylist': True,
            'force_keyframes_at_cuts': True
        }

        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([video_url])

        return {
            "success": True,
            "message": "Cắt video thành công",
            "start_time": start_time,
            "end_time": end_time,
            "download_url": f"/downloads/yt_short_{vid}.mp4"
        }
    except Exception as e:
        return {"success": False, "error": f"Lỗi xử lý: {str(e)}"}
