"use client";

import { useState, useEffect } from "react";
import styles from "./page.module.css";

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    // Read current theme from document
    const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
    setTheme(currentTheme);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  };

  const handleDownload = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setResult(null);
    
    if (!url) {
      setError("Please enter a valid URL.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/download", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });
      
      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || data.detail || "Failed to download video");
      }
      
      setResult(data);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className={styles.container}>
      <header className={styles.header}>
        <button className={styles.themeToggle} onClick={toggleTheme}>
          {theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode"}
        </button>
      </header>

      <div className={styles.card}>
        <h1 className={styles.title}>Video Downloader</h1>
        <p className={styles.subtitle}>
          Download videos from TikTok and Instagram Reels without watermarks.
        </p>

        <form className={styles.form} onSubmit={handleDownload}>
          <div className={styles.inputGroup}>
            <input
              type="url"
              className={styles.input}
              placeholder="Paste TikTok or Instagram Reel link..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>
          <button type="submit" className={styles.button} disabled={loading}>
            {loading ? (
              <>
                <div className={styles.spinner}></div>
                Extracting...
              </>
            ) : (
              "Get Video"
            )}
          </button>
          {error && <div className={styles.error}>{error}</div>}
        </form>

        {result && (
          <div className={styles.result}>
            {result.thumbnail && (
              <img src={result.thumbnail} alt="Thumbnail" className={styles.thumbnail} />
            )}
            <h3 className={styles.videoTitle}>{result.title}</h3>
            {result.video_url && (
              <a
                href={result.video_url}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.downloadBtn}
                download
              >
                Download Video
              </a>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
