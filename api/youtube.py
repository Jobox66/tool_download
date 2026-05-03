import yt_dlp
import os

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

def cut_hot_segment(video_url: str):
    try:
        ydl_opts_info = {'quiet': True, 'skip_download': True}
        best_segment = None
        
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(video_url, download=False)
            heatmap = info.get('heatmap', [])
            
            if not heatmap:
                return {"success": False, "error": "Video này không có dữ liệu Heatmap (đoạn được xem lại nhiều nhất) từ YouTube."}
                
            # Find the segment with max value
            best_segment = max(heatmap, key=lambda x: x.get('value', 0))
        
        if not best_segment:
            return {"success": False, "error": "Không thể xác định đoạn Hot nhất."}
            
        start_time = best_segment['start_time']
        end_time = best_segment['end_time']
        
        os.makedirs("public/downloads", exist_ok=True)
        output_filename = f"public/downloads/yt_short_{info.get('id')}.mp4"
        
        # If file already exists, just return it
        if os.path.exists(output_filename):
            return {
                "success": True, 
                "message": "Video đã được cắt từ trước", 
                "start_time": start_time,
                "end_time": end_time,
                "download_url": f"/downloads/yt_short_{info.get('id')}.mp4"
            }
            
        def download_range_func(info_dict, ydl):
            return [{'start_time': start_time, 'end_time': end_time}]
            
        ydl_opts_download = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'download_ranges': download_range_func,
            'outtmpl': output_filename,
            'quiet': True,
            'noplaylist': True,
            'force_keyframes_at_cuts': True # Ensure cuts are accurate
        }
        
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([video_url])
            
        return {
            "success": True, 
            "message": "Cắt video thành công", 
            "start_time": start_time,
            "end_time": end_time,
            "download_url": f"/downloads/yt_short_{info.get('id')}.mp4"
        }
    except Exception as e:
        return {"success": False, "error": f"Lỗi xử lý: {str(e)}"}
