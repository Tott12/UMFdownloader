from PIL import Image, ImageDraw

def make_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = int(size * 0.12)
    d.rounded_rectangle([pad, pad, size - pad, size - pad], radius=int(size * 0.22), fill=(40, 167, 69, 255))
    cx = size / 2.0
    top = size * 0.38
    bottom = size * 0.68
    w = size * 0.28
    d.polygon([(cx - w / 2, top), (cx + w / 2, top), (cx, bottom)], fill=(255, 255, 255, 255))
    d.rectangle([cx - w / 2, bottom, cx + w / 2, size - pad], fill=(255, 255, 255, 255))
    return img

import os
os.makedirs("C:/UMFDownloader/extension/icons", exist_ok=True)
for size in (16, 48, 128):
    make_icon(size).save(f"C:/UMFDownloader/extension/icons/icon{size}.png")
    print(f"icon{size}.png created")
