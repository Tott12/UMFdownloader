import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import os
import sys
import shutil

LICENSE_TEXT = """Proprietary Software License

Copyright (c) 2019 Mehdi CHEMSI. All Rights Reserved.

Permission is hereby granted to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to inspect, copy, use, 
and modify the Software strictly for personal, educational, or non-commercial 
purposes, subject to the following conditions:

1. NON-COMMERCIAL USE: Copying, distribution, and personal usage of the Software 
   are permitted provided that all original copyright notices and this permission 
   notice are retained in all copies or substantial portions of the Software.

2. COMMERCIAL USE: Any commercial use, including but not limited to selling, 
   sublicensing, integrating into commercial products, or using the Software 
   for profit-generating activities, is strictly prohibited without a prior 
   written mutual agreement signed by Mehdi CHEMSI.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, 
OUTSIDE OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE."""

LICENSE_FILE = os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"), "UMFdownloaded", "license_accepted")


class LicenseDialog(tk.Toplevel):
    """Modal dialog that displays the proprietary software license."""

    def __init__(self, root):
        super().__init__(root)
        self.agreed = False
        self.title("UMFdownloaded - License Agreement")
        self.geometry("560x540")
        self.transient(root)
        self.grab_set()  # Make the dialog modal
        self.protocol("WM_DELETE_WINDOW", self.on_disagree)

        frame = tk.Frame(self, bg="#1e1e1e", padx=20, pady=12)
        frame.pack(fill="both", expand=True)

        title_label = tk.Label(frame, text="Welcome to UMFdownloaded", bg="#1e1e1e", fg="white", font=("Arial", 12, "bold"))
        title_label.pack()

        instruction = tk.Label(frame, text="Before using this software, you must read and accept the following Proprietary Software License:", bg="#1e1e1e", fg="#cccccc", font=("Arial", 9))
        instruction.pack(anchor="w", pady=(8, 0))

        text = tk.Text(frame, bg="#2d2d2d", fg="#cccccc", font=("Arial", 8), wrap="word", relief="flat", bd=0)
        text.pack(fill="both", expand=True, pady=10, padx=(0, 10))
        text.insert("1.0", LICENSE_TEXT)
        text.configure(state="disabled")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        btn_frame = tk.Frame(frame, bg="#1e1e1e")
        btn_frame.pack(fill="x", pady=(5, 0))

        self.agree_btn = tk.Button(btn_frame, text="I Agree & Continue", bg="#28a745", fg="white", bd=0, font=("Arial", 10, "bold"), command=self.on_agree, pady=8)
        self.agree_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.disagree_btn = tk.Button(btn_frame, text="I Disagree (Exit)", bg="#dc3545", fg="white", bd=0, font=("Arial", 10, "bold"), command=self.on_disagree, pady=8)
        self.disagree_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def on_agree(self):
        self.agreed = True
        try:
            os.makedirs(os.path.dirname(LICENSE_FILE), exist_ok=True)
            with open(LICENSE_FILE, "w", encoding="utf-8") as f:
                f.write("UMFdownloaded proprietary software license accepted.\n")
        except Exception:
            pass
        self.destroy()

    def on_disagree(self):
        self.agreed = False
        self.destroy()


class SingleFileDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Frameless Window
        self.root.geometry("620x480")
        self.root.configure(bg="#1e1e1e")

        self.current_process = None
        self.licensed = False

        # Ask the user to accept the proprietary license before use
        if not self.check_license(root):
            root.destroy()
            return

        # Center window on screen
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (620 // 2)
        y = (sh // 2) - (480 // 2)
        self.root.geometry(f"620x480+{x}+{y}")

        # --- Custom Title Bar ---
        self.title_bar = tk.Frame(self.root, bg="#2d2d2d", height=35)
        self.title_bar.pack(fill="x", side="top")

        title_label = tk.Label(self.title_bar, text=" Universal Media File Media Downloader", bg="#2d2d2d", fg="white", font=("Arial", 10, "bold"))
        title_label.pack(side="left", padx=10)

        close_btn = tk.Button(self.title_bar, text="✕", bg="#2d2d2d", fg="white", bd=0, font=("Arial", 10, "bold"), command=self.on_close, activebackground="#e81123", activeforeground="white")
        close_btn.pack(side="right", padx=5, pady=5)

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        title_label.bind("<Button-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.do_move)

        # --- Content Frame ---
        cf = tk.Frame(self.root, bg="#1e1e1e")
        cf.pack(fill="both", expand=True, padx=20, pady=20)

        # URL Input
        tk.Label(cf, text="Target Video URL (Playlists automatically blocked):", bg="#1e1e1e", fg="#cccccc", font=("Arial", 9)).pack(anchor="w")
        self.url_entry = tk.Entry(cf, bg="#2d2d2d", fg="white", insertbackground="white", bd=0, font=("Arial", 10))
        self.url_entry.pack(fill="x", ipady=6, pady=5)
        self.url_entry.insert(0, "https://www.youtube.com/watch?v=N_4kTaVltPM")

        # Destination Directory Picker
        tk.Label(cf, text="Save Destination Folder:", bg="#1e1e1e", fg="#cccccc", font=("Arial", 9)).pack(anchor="w", pady=(10, 0))
        
        dest_frame = tk.Frame(cf, bg="#1e1e1e")
        dest_frame.pack(fill="x", pady=5)
        
        self.dest_entry = tk.Entry(dest_frame, bg="#2d2d2d", fg="white", insertbackground="white", bd=0, font=("Arial", 10))
        self.dest_entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 5))
        self.dest_entry.insert(0, "C:/Users/chems/Downloads")
        
        browse_btn = tk.Button(dest_frame, text="Browse", bg="#007acc", fg="white", bd=0, command=self.browse_directory, font=("Arial", 9, "bold"), padx=10)
        browse_btn.pack(side="right")

        # Speed Limit Slider
        tk.Label(cf, text="Download Speed Limit (KB/s, 0 = Unlimited):", bg="#1e1e1e", fg="#cccccc", font=("Arial", 9)).pack(anchor="w", pady=(10, 0))
        self.speed_slider = tk.Scale(cf, from_=0, to=5000, resolution=100, orient="horizontal", bg="#1e1e1e", fg="white", highlightbackground="#1e1e1e", troughcolor="#2d2d2d")
        self.speed_slider.set(0)
        self.speed_slider.pack(fill="x", pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(cf, orient="horizontal", length=100, mode="indeterminate")
        self.progress.pack(fill="x", pady=15)

        # Status Label
        self.status_label = tk.Label(cf, text="Ready (Check terminal for live logs)", bg="#1e1e1e", fg="#00ff00", font=("Arial", 9))
        self.status_label.pack(anchor="w")

        # Action Buttons
        btn_frame = tk.Frame(cf, bg="#1e1e1e")
        btn_frame.pack(fill="x", pady=(15, 0))

        self.start_btn = tk.Button(btn_frame, text="Download File", bg="#28a745", fg="white", bd=0, font=("Arial", 10, "bold"), command=self.start_workflow, pady=8)
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.cancel_btn = tk.Button(btn_frame, text="Cancel / Stop", bg="#dc3545", fg="white", bd=0, font=("Arial", 10, "bold"), command=self.cancel_download, pady=8, state="disabled")
        self.cancel_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def check_license(self, root):
        """Show the proprietary license dialog until the user agrees to it."""
        if os.path.exists(LICENSE_FILE):
            self.licensed = True
            return True

        dialog = LicenseDialog(root)
        self.root.wait_window(dialog)

        if dialog.agreed:
            self.licensed = True
            return True

        messagebox.showwarning(
            "License Required",
            "You must accept the Proprietary Software License\nto use UMFdownloaded.\n\n"
            "The application will now close. Please accept or reject the license\n"
            "and start the application again.",
        )
        return False

    def get_ydlp_command(self):
        """Return the yt-dlp executable to run (works from a PyInstaller bundle too)."""
        if getattr(sys, "frozen", False):
            candidates = [
                os.path.join(sys._MEIPASS, "yt-dlp.exe"),
                os.path.join(sys._MEIPASS, "_internal", "yt-dlp.exe"),
                os.path.join(sys._MEIPASS, "yt_dlp.exe"),
            ]
            for candidate in candidates:
                if os.path.isfile(candidate):
                    return [candidate]

        found = shutil.which("yt-dlp")
        if found:
            return [found]

        return ["yt-dlp"]

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def browse_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, dir_path)

    def start_workflow(self):
        url = self.url_entry.get().strip()
        dest_dir = self.dest_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL!")
            return
        if not os.path.isdir(dest_dir):
            messagebox.showerror("Error", "Please select a valid destination folder!")
            return

        self.start_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress.start(10)
        self.status_label.config(text="Downloading single file...")
        
        threading.Thread(target=self.run_process, args=(url, dest_dir), daemon=True).start()

    def run_process(self, url, dest_dir):
        try:
            speed_limit = self.speed_slider.get()
            #output_template = os.path.join(dest_dir, "%(title)s.%(ext)s")
            output_template = os.path.join(dest_dir, "%(id)s.%(ext)s")
            # Added "--no-playlist" to ensure only one single file downloads
            cmd = self.get_ydlp_command() + ["--no-playlist", "-o", output_template, url]
            if speed_limit > 0:
                cmd.extend(["--limit-rate", f"{speed_limit}K"])

            print(f"\n[INFO] Starting download command: {' '.join(cmd)}")

            self.current_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            for line in self.current_process.stdout:
                print(line, end="")

            self.current_process.wait()
            returncode = self.current_process.returncode

            self.root.after(0, self.download_finished, returncode, dest_dir)

        except Exception as e:
            self.root.after(0, self.download_error, str(e))

    def download_finished(self, returncode, dest_dir):
        self.progress.stop()
        self.start_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.current_process = None

        if returncode == 0:
            self.status_label.config(text="Download complete!")
            messagebox.showinfo("Success", f"File downloaded successfully to:\n{dest_dir}")
        else:
            self.status_label.config(text="Download stopped or failed.")

    def download_error(self, err_msg):
        self.progress.stop()
        self.start_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.current_process = None
        messagebox.showerror("Execution Error", err_msg)
        self.status_label.config(text="Error occurred.")

    def cancel_download(self):
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                print("\n[INFO] Download cancelled by user.")
                self.status_label.config(text="Download cancelled.")
            except Exception:
                pass

    def on_close(self):
        self.cancel_download()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SingleFileDownloaderApp(root)
    if app.licensed:
        root.mainloop()