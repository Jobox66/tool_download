"use client";

import { useState, useEffect } from "react";
import styles from "./page.module.css";

interface Video {
  id: string;
  title: string;
  cover: string;
  views: number;
  likes: number;
  comments: number;
  shares: number;
  hot_score: number;
  url: string;
}

export default function TrendingDashboard() {
  const [region, setRegion] = useState("VN");
  const [videos, setVideos] = useState<Video[]>([]);
  const [filteredVideos, setFilteredVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [minViews, setMinViews] = useState(0);
  const [theme, setTheme] = useState("light");
  const [downloadingId, setDownloadingId] = useState<string | null>(null);

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

    setLoading(true);
    setError("");
    try {
      const res = await fetch(`/api/trending?region=${encodeURIComponent(region)}`);
      const data = await res.json();
      
      if (!res.ok || !data.success) {
        throw new Error(data.detail || "Failed to fetch trending videos");
      }
      
      setVideos(data.data);
      setFilteredVideos(data.data.filter((v: Video) => v.views >= minViews));
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setFilteredVideos(videos.filter((v) => v.views >= minViews));
  }, [minViews, videos]);

  const handleDownload = async (url: string, id: string) => {
    setDownloadingId(id);
    try {
      const res = await fetch("/api/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      
      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || data.detail || "Failed to download video");
      }
      
      if (data.video_url) {
        // Create an invisible a element to trigger download
        const a = document.createElement("a");
        a.href = data.video_url;
        a.download = `video_${id}.mp4`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
    } catch (err: any) {
      alert(err.message || "Failed to download");
    } finally {
      setDownloadingId(null);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
    if (num >= 1000) return (num / 1000).toFixed(1) + "K";
    return num.toString();
  };

  return (
    <main className={styles.container}>
      <header className={styles.header}>
        <button className={styles.themeToggle} onClick={toggleTheme}>
          {theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode"}
        </button>
      </header>

      <div className={styles.dashboard}>
        <h1 className={styles.title}>Trending Dashboard</h1>
        <p className={styles.subtitle}>Analyze and download top performing videos.</p>

        <form className={styles.searchBar} onSubmit={handleSearch}>
          <select
            className={styles.input}
            value={region}
            onChange={(e) => setRegion(e.target.value)}
          >
            <option value="VN">🇻🇳 Vietnam Trending</option>
            <option value="CN">🇨🇳 Douyin (China) Trending</option>
            <option value="US">🇺🇸 US Trending</option>
            <option value="KR">🇰🇷 Korea Trending</option>
            <option value="JP">🇯🇵 Japan Trending</option>
            <option value="TH">🇹🇭 Thailand Trending</option>
          </select>
          <button type="submit" className={styles.button} disabled={loading}>
            {loading ? "Fetching..." : "Get Hot Videos"}
          </button>
        </form>

        {error && <div className={styles.error}>{error}</div>}

        {videos.length > 0 && (
          <div className={styles.filterSection}>
            <label className={styles.filterLabel}>
              Min Views: {formatNumber(minViews)}
            </label>
            <input
              type="range"
              min="0"
              max="10000000"
              step="100000"
              value={minViews}
              onChange={(e) => setMinViews(Number(e.target.value))}
              className={styles.slider}
            />
          </div>
        )}

        <div className={styles.grid}>
          {filteredVideos.map((video) => (
            <div key={video.id} className={styles.card}>
              <div className={styles.imageWrapper}>
                <img src={video.cover} alt={video.title} className={styles.coverImage} />
                <div className={styles.hotBadge}>🔥 {video.hot_score}</div>
              </div>
              <div className={styles.cardContent}>
                <h3 className={styles.videoTitle}>{video.title || 'Untitled Video'}</h3>
                <div className={styles.stats}>
                  <span>👁️ {formatNumber(video.views)}</span>
                  <span>❤️ {formatNumber(video.likes)}</span>
                  <span>💬 {formatNumber(video.comments)}</span>
                  <span>↗️ {formatNumber(video.shares)}</span>
                </div>
                <button
                  className={styles.downloadBtn}
                  onClick={() => handleDownload(video.url, video.id)}
                  disabled={downloadingId === video.id}
                >
                  {downloadingId === video.id ? "Downloading..." : "Download Video"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
