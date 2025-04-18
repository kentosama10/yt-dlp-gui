﻿# yt-dlp-gui

A simple GUI application for downloading YouTube videos and playlists using `yt-dlp`.

## Features
- Download videos or playlists in various formats (e.g., MP4, MP3, WEBM, M4A).
- Choose video quality (e.g., 1080p, 720p, audio only).
- Select output directory for downloaded files.
- View real-time download progress in the application.
- View download history.

## Requirements
- Python 3.7 or higher
- `yt-dlp` installed (`pip install yt-dlp`)
- `customtkinter` installed (`pip install customtkinter`)

## How to Use
1. Clone or download this repository.
2. Install the required dependencies:
   pip install -r requirements.txt
3. Run the application:
    python yt-dlp.py
4. Enter the YouTube URL, select the format and quality, and click "Download".
5. Use the "Select Output Directory" button to choose where files will be saved.
6. To install via Pyinstaller/EXE
"pyinstaller --noconsole --onefile --icon=K.ico yt-dlp.py"
