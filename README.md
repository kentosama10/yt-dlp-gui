# yt-dlp-gui

A simple GUI application for downloading YouTube videos and playlists using `yt-dlp`.

## Features
- Download videos or playlists in various formats (e.g., MP4, MP3, WEBM, M4A).
- Choose video quality (e.g., 1080p, 720p, audio only).
- Select output directory for downloaded files.
- View real-time download progress and download history.

## Requirements
1. Python 3.7 or higher.
2. `ffmpeg` binary (ensure it is in the system PATH or the application directory).
3. `yt-dlp` binary (place `yt-dlp.exe` in the application directory).

## How to Use
1. Clone or download this repository.
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python yt-dlp.py
   ```
4. Enter the YouTube URL, select the format and quality, and click "Download".
5. Use the "Select Output Directory" button to choose where files will be saved.
6. To create a standalone executable:
   ```bash
   pyinstaller --onefile --icon=your-icon.ico --add-binary "yt-dlp.exe;." --add-binary "ffmpeg.exe;." yt-dlp.py
   ```
