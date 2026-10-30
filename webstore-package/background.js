// UMF Downloader - Chrome Extension Background Service Worker
// Forwards download requests from the content script to the native messaging host.

const NATIVE_HOST_NAME = "com.umfdownloaded";

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === "download" && msg.url) {
    // Async response
    (async () => {
      try {
        const response = await chrome.runtime.sendNativeMessage({
          type: "download",
          url: msg.url,
        });
        sendResponse(response);
      } catch (e) {
        sendResponse({ type: "error", msg: String(e) });
      }
    })();
    return true; // keep the message channel open for async response
  }
  return false;
});
