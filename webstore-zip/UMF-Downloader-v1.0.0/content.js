// UMF Downloader - Content Script
// Injects a small floating download button (IDM-style) when a <video> element is present.

let currentButton = null;
let downloadInProgress = false;

function getVideoUrl() {
  const videos = document.querySelectorAll("video");
  if (videos.length > 0) {
    const v = videos[videos.length - 1];
    const url = v.currentSrc || v.src || "";
    if (url) return url;
  }
  const iframe = document.querySelector("iframe");
  if (iframe) {
    try {
      return new URL(iframe.src, location.href).href;
    } catch (e) {
      return "";
    }
  }
  return "";
}

function updateButtonText(text) {
  if (currentButton) currentButton.textContent = text;
}

function handleDownload(videoUrl) {
  if (downloadInProgress) return;
  downloadInProgress = true;
  updateButtonText("⏳ Starting...");

  chrome.runtime
    .sendMessage({ type: "download", url: videoUrl })
    .then((response) => {
      if (!response) {
        updateButtonText("❌ Failed");
      } else if (response.type === "done") {
        updateButtonText("✅ Done");
      } else if (response.type === "error") {
        updateButtonText("❌ Error");
      } else {
        updateButtonText("⏳ ...");
      }
    })
    .catch(() => {
      updateButtonText("❌ Failed");
    })
    .finally(() => {
      downloadInProgress = false;
    });
}

function createButton() {
  const btn = document.createElement("div");
  btn.id = "umf-download-fab";
  btn.title = "UMF Downloader";
  btn.style.cssText = [
    "position:fixed",
    "top:0",
    "left:50%",
    "transform:translateX(-50%)",
    "z-index:2147483647",
    "background:#28a745",
    "color:#ffffff",
    "font-family:Arial,sans-serif",
    "font-size:13px",
    "font-weight:bold",
    "padding:10px 18px",
    "border-radius:0 0 12px 12px",
    "box-shadow:0 6px 18px rgba(0,0,0,0.5)",
    "cursor:pointer",
    "display:none",
    "align-items:center",
    "gap:8px",
    "user-select:none",
    "text-align:center",
  ].join(";");
  btn.innerHTML = '<span style="font-size:14px;">&#11015;</span> <span>Download</span>';
  btn.addEventListener("click", () => {
    const url = getVideoUrl();
    if (url && !downloadInProgress) handleDownload(url);
  });
  return btn;
}

function tryShow() {
  const url = getVideoUrl();
  if (url) {
    if (!currentButton) currentButton = createButton();
    if (currentButton.style.display === "none") {
      currentButton.style.display = "flex";
      currentButton.style.top = "0px";
    }
    if (!downloadInProgress) updateButtonText("⬇ Download");
  } else if (currentButton) {
    currentButton.style.display = "none";
  }
}

function init() {
  const check = () => {
    try {
      if (document.body) tryShow();
    } catch (e) {}
  };
  check();
  const observer = new MutationObserver(() => {
    clearTimeout(window.__umfCheckTimer);
    window.__umfCheckTimer = setTimeout(check, 500);
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });
}

if (document.body) {
  init();
} else {
  document.addEventListener("DOMContentLoaded", init);
}
