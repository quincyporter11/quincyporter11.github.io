---
title: "YouTube Downloader"
slug: "youtube-downloader"
date: "2026-02-05"
tags: ["tui", "python"]
---

This project is a terminal UI I built to download YouTube videos. It allows a user to download audio only, lower quality videos with audio, or high quality videos and then utilize ffmpeg to merge audio and video together. Most of the time straight up YouTube is fine but this allows you to have YouTube on the go.

### What is does
- built to pull Omarchy theme automatically
- Shows YouTube video metadata
- Gives multiple download formats
- Allows for high quality downloads with audio (utilizes ffmpeg)
- auto selects best 1080p format

### Screenshots
![Main screen](/static/img/youtube-download/main.png)

![Formats screen](/static/img/youtube-download/formats.png)

### Notes / Lessons Learned
This was a pretty fun project to build. I have downloaded YouTube videos using Python before but this was my first time integrating a TUI. I utilized what I learned from my SSH TUI and built this one. It was fairly straight forward. I'm really happy with the progress I made so far. Eventually I might even make it into a downloader and media player. I also may build a separate GUI and web UI as I way to interface with to backend. There are always ways to improve code so I'll keep my eyes out for those as well.

<div class="repo-link">
  <strong>Source Code:</strong><br>
  <a href="https://github.com/quincyporter11/yt_downloader" target="_blank" rel="noopener">
    View on GitHub →
  </a>
</div>
