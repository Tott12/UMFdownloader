# UMF Downloader — Chrome Web Store Official Addon

This folder is the **store-ready Chrome extension package** source.

## Official Chrome Web Store publishing steps

1. **Developer account**
   - You need a [Chrome Web Store Developer account](https://chrome.google.com/webstore/devconsole) (one-time fee: ~$5).

2. **Package the extension**
   - The extension source lives in `C:\UMFDownloader\extension` (with `manifest.json` at its root and `icons/` inside).
   - For the Web Store, the uploaded ZIP must contain the extension root (manifest.json at top level):
     ```
     manifest.json
     background.js
     content.js
     icons/icon16.png
     icons/icon48.png
     icons/icon128.png
     ```

3. **Create the ZIP**
   ```
   C:\UMFDownloader\webstore-package\UMF-Downloader-v1.0.0.zip
   ```

4. **Upload**
   - Go to: https://chrome.google.com/webstore/devconsole
   - Click **Add new listing** → **Upload package**.
   - Select the ZIP file → fill in store listing (name, description, screenshots, category, etc.) → submit for review.

5. **Privacy policy**
   - Chrome requires a privacy policy URL for any published extension. Host one (e.g., GitHub Pages / your site) describing that the extension does not collect personal data, only handles video URLs during download.

6. **Review**
   - Review usually takes a few days. Requirements: no remote code (all JS ships inside the ZIP ✓), single purpose (video downloader ✓), functional demo.

7. **After approval**
   - Users install from the Chrome Web Store like any other addon.

## How it works after official install
- User installs from Web Store.
- Native messaging host (`com.umfdownloaded`) + `native_host.py` must still be installed locally by the user (Python + `yt-dlp`) for downloads to actually work — the store listing provides the UI button.

## Limitations
- The actual download execution depends on the locally installed Python native host.
- Official review requires a privacy policy and functional verification.
