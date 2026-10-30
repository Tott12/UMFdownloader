# UMFdownloaded — Universal Media File Downloader

A simple GUI application (built with Python `tkinter`) that downloads a **single video file** from YouTube using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

> ⚠️ **Proprietary Software License:** Copyright (c) 2019 Mehdi CHEMSI. All Rights Reserved.
> Use of this software is subject to the [Proprietary Software License](LICENSE). The application will ask you to accept the license on first launch.

---

## 📋 Requirements

- Python **3.10+**
- `tkinter` (included with standard Python distributions; on Linux may require `python3-tk`)
- `yt-dlp` (installed via pip)

## 🛠️ Setup

1. **Clone or download this repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/UMFdownloaded.git
   cd UMFdownloaded
   ```

2. **Install the requirements:**

   ```bash
   pip install -r requirements.txt
   ```

   > This installs `yt-dlp`. `tkinter` is part of the Python standard library and does not need separate installation on Windows.

3. **Run the application:**

   ```bash
   python app.py
   ```

## 📄 First Launch — License Agreement

- On first launch, the app displays the **Proprietary Software License**.
- Click **"I Agree & Continue"** to use the app, or **"I Disagree (Exit)"** to close it.
- Your acceptance is remembered locally, so you will only be asked once.

## ⬇️ Downloading a Video

1. **Copy & paste** the YouTube video URL into the **"Target Video URL"** field.
   - Example: `https://www.youtube.com/watch?v=N_4kTaVltPM`
   - ⚠️ **Playlists are automatically blocked** — only single videos are supported.
2. Set the **"Save Destination Folder"** where the file should be saved (or click **Browse**).
3. Optionally set the **"Download Speed Limit"** (KB/s, `0` = unlimited).
4. Click **"Download File"**.
5. Wait for the status to show **"Download complete!"**.

The downloaded file will be saved to your destination folder.

## 📦 Running the Executable (UMF.exe)

- A ready-to-run Windows executable is provided in the GitHub **Releases** section: `UMF.exe`.
- Simply download and run `UMF.exe` on Windows (the `yt-dlp` binary is bundled inside).
- Accept the license on first launch, then paste and download your video as above.

---

## 📄 License

This software is licensed under the **Proprietary Software License** (Copyright (c) 2019 Mehdi CHEMSI). All rights reserved.
