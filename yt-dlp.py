import os
import subprocess
import datetime
import threading
import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk

LOG_FILE = "download_history.log"

class YTDLPDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader GUI - developed by kentosama10")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.url_var = ctk.StringVar()
        self.format_var = ctk.StringVar(value="mp4")
        self.quality_var = ctk.StringVar(value="best")
        self.status_var = ctk.StringVar()
        self.output_dir = os.getcwd()

        ctk.CTkLabel(self, text="YouTube URL:").pack(pady=(20, 5))
        ctk.CTkEntry(self, textvariable=self.url_var, width=400).pack()

        ctk.CTkLabel(self, text="Format:").pack(pady=(15, 5))
        ctk.CTkOptionMenu(self, values=["mp4", "mp3", "webm", "m4a", "best"], variable=self.format_var).pack()

        ctk.CTkLabel(self, text="Quality:").pack(pady=(15, 5))
        ctk.CTkOptionMenu(self, values=["best", "1080p", "720p", "480p", "360p", "audio only"], variable=self.quality_var).pack()

        ctk.CTkButton(self, text="Select Output Directory", command=self.select_output_directory).pack(pady=10)
        ctk.CTkButton(self, text="Download", command=self.start_download_thread).pack(pady=10)
        ctk.CTkButton(self, text="View Download History", command=self.view_history).pack()

        ctk.CTkLabel(self, textvariable=self.status_var, text_color="green").pack(pady=(10, 0))

        # Text widget to display yt-dlp output
        self.output_text = ctk.CTkTextbox(self, wrap="word", width=550, height=200)
        self.output_text.pack(pady=(10, 0))

    def select_output_directory(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir, title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.status_var.set(f"📁 Output Directory: {self.output_dir}")

    def build_format_string(self, fmt, quality):
        if fmt == "mp3":
            return ["-x", "--audio-format", "mp3"]
        elif quality == "audio only":
            return ["-f", "bestaudio"]
        elif fmt == "mp4":
            q_map = {
                "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]",
                "720p":  "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]",
                "480p":  "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]",
                "360p":  "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]",
                "best":  "bestvideo[ext=mp4]+bestaudio[ext=m4a]"
            }
            return ["-f", q_map.get(quality, "best"), "--merge-output-format", "mp4"]
        elif fmt == "webm":
            return ["-f", "bestvideo[ext=webm]+bestaudio[ext=webm]", "--merge-output-format", "webm"]
        elif fmt == "m4a":
            return ["-f", "bestaudio[ext=m4a]"]
        return ["-f", "best"]

    def start_download_thread(self):
        threading.Thread(target=self.start_download, daemon=True).start()

    def start_download(self):
        url = self.url_var.get().strip()
        fmt = self.format_var.get()
        quality = self.quality_var.get()

        if not url:
            self.status_var.set("❌ Please enter a URL.")
            return

        self.status_var.set("⏳ Downloading...")
        output_template = os.path.join(self.output_dir, "%(title)s.%(ext)s")
        cmd = ["yt-dlp", "--yes-playlist", "--no-mtime"] + self.build_format_string(fmt, quality) + ["-o", output_template, url]

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                self.output_text.insert("end", line)  # Append yt-dlp output to the text widget
                self.output_text.see("end")  # Auto-scroll to the latest line
                self.update_idletasks()
            process.wait()
            if process.returncode == 0:
                self.status_var.set("✅ Download complete.")
                self.log_download(url, fmt, quality, True)
            else:
                self.status_var.set("❌ Download failed.")
                self.log_download(url, fmt, quality, False)
        except Exception as e:
            self.status_var.set(f"❌ Error: {e}")

    def log_download(self, url, fmt, quality, success):
        with open(LOG_FILE, "a") as f:
            status = "SUCCESS" if success else "FAILED"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {status} - {url} | Format: {fmt} | Quality: {quality}\n")

    def view_history(self):
        if not os.path.exists(LOG_FILE):
            self.status_var.set("ℹ️ No history found.")
            return

        history_window = ctk.CTkToplevel(self)
        history_window.title("Download History")
        history_window.geometry("480x300")

        with open(LOG_FILE, "r") as f:
            log_content = f.read()

        textbox = ctk.CTkTextbox(history_window, wrap="word", width=450, height=250)
        textbox.insert("0.0", log_content)
        textbox.configure(state="disabled")
        textbox.pack(pady=10)

if __name__ == "__main__":
    app = YTDLPDownloader()
    app.mainloop()
