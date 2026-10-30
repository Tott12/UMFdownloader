// UMF Downloader - Native Messaging Host for Chrome (com.umfdownloaded)
// Receives download requests from the Chrome extension and runs yt-dlp.

import json
import os
import re
import struct
import subprocess
import sys

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
NATIVE_HOST_NAME = "com.umfdownloaded"


def read_exact(n):
    data = b""
    while len(data) < n:
        chunk = sys.stdin.buffer.read(n - len(data))
        if not chunk:
            return None if not data else data
        data += chunk
    return data


def read_message():
    raw = read_exact(4)
    if not raw:
        return None
    length = struct.unpack("<I", raw)[0]
    data = read_exact(length)
    if not data:
        return None
    return json.loads(data.decode("utf-8"))


def send_message(obj):
    payload = json.dumps(obj).encode("utf-8")
    sys.stdout.buffer.write(struct.pack("<I", len(payload)) + payload)
    sys.stdout.buffer.flush()


def run_download(url):
    output_template = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    cmd = ["yt-dlp", "--no-playlist", "-o", output_template, url]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    destination = None

    while True:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if "Destination:" in line:
            destination = line.split("Destination:")[1].strip()

    proc.wait()

    if proc.returncode == 0:
        return {"type": "done", " status": "ok", " file": destination or output_template}
    return {"type": "error", " msg": f"yt-dlp failed with code {proc.returncode}"}


def main():
    while True:
        try:
            msg = read_message()
        except Exception:
            break
        if msg is None:
            break
        if msg.get("type") == "exit":
            break
        if msg.get("type") == "download":
            response = run_download(msg.get("url", ""))
            send_message(response)


if __name__ == "__main__":
    main()
