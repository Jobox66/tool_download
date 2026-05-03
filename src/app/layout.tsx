import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Universal Video Downloader",
  description: "Download TikTok and Instagram Reels without watermark",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  var localTheme = localStorage.getItem('theme');
                  var theme = localTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
                  document.documentElement.setAttribute('data-theme', theme);
                } catch (e) {}
              })();
            `,
          }}
        />
        <nav className="navbar">
          <Link href="/" className="nav-link">Single Download</Link>
          <Link href="/trending" className="nav-link">Trending Dashboard</Link>
          <Link href="/yt-cutter" className="nav-link">YT Shorts Cutter</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}
