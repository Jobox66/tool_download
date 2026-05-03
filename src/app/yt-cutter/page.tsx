"use client";

import { useState, useEffect } from "react";
import styles from "./page.module.css";

interface YTVideo {
  id: string;
  title: string;
  url: string;
  duration: number;
  view_count: number;
}

export default function YTCutter() {
  const [url, setUrl] = useState("");
  const [videos, setVideos] = useState<YTVideo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [theme, setTheme] = useState("light");
  const [processingId, setProcessingId] = useState<string | null>(null);

  useEffect(() => {
    const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
    setTheme(currentTheme);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setError("");
    setVideos([]);
    try {
      const res = await fetch(`/api/youtube/channel?url=${encodeURIComponent(url)}`);
      const data = await res.json();
      
      if (!res.ok || !data.success) {
        throw new Error(data.detail || data.error || "Failed to fetch videos");
      }
      
      setVideos(data.data);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  const handleCut = async (videoUrl: string, id: string) => {
    setProcessingId(id);
    try {
      const res = await fetch("/api/youtube/cut", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoUrl }),
      });
      
      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || data.detail || "Failed to cut video");
      }
      
      if (data.download_url) {
        alert(`Cắt thành công đoạn từ ${data.start_time}s đến ${data.end_time}s`);
        const a = document.createElement("a");
        a.href = data.download_url;
        a.download = `yt_short_${id}.mp4`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
    } catch (err: any) {
      alert(err.message || "Failed to process video");
    } finally {
      setProcessingId(null);
    }
  };

  const formatDuration = (seconds: number) => {
    if (!seconds) return "N/A";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <main className={styles.container}>
      <header className={styles.header}>
        <button className={styles.themeToggle} onClick={toggleTheme}>
          {theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode"}
        </button>
      </header>

      <div className={styles.dashboard}>
        <h1 className={styles.title}>YouTube Auto Cutter</h1>
        <p className={styles.subtitle}>Automatically find and cut the most replayed (hottest) segment of any YouTube video.</p>

        <form className={styles.searchBar} onSubmit={handleSearch}>
          <input
            type="url"
            className={styles.input}
            placeholder="Enter YouTube Channel URL or Video URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
          <button type="submit" className={styles.button} disabled={loading}>
            {loading ? "Scanning..." : "Analyze"}
          </button>
        </form>

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.list}>
          {videos.map((video) => (
            <div key={video.id} className={styles.card}>
              <div className={styles.thumbnail}>
                <img src={`https://img.youtube.com/vi/${video.id}/mqdefault.jpg`} alt={video.title} />
              </div>
              <div className={styles.cardContent}>
                <h3 className={styles.videoTitle}>{video.title || 'Untitled Video'}</h3>
                <div className={styles.stats}>
                  <span>⏱️ {formatDuration(video.duration)}</span>
                  <span>👁️ {video.view_count ? video.view_count.toLocaleString() : "N/A"} views</span>
                </div>
                <button
                  className={styles.cutBtn}
                  onClick={() => handleCut(video.url, video.id)}
                  disabled={processingId === video.id}
                >
                  {processingId === video.id ? "✂️ Cutting..." : "✂️ Get Hot Segment"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
