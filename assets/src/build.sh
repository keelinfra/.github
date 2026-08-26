#!/usr/bin/env bash
# Regenerate all keelinfra brand assets into ../ (assets/).
# Requirements: python3 + fontTools, Google Chrome, rsvg-convert, ImageMagick, macOS (Avenir Next).
set -euo pipefail
cd "$(dirname "$0")"
ASSETS=".."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

echo "==> wordmark glyph outlines (Avenir Next Demi Bold)"
python3 wordmark_paths.py > wordmark.json

echo "==> logo / wordmark SVGs"
python3 compose_svgs.py

echo "==> banner HTML masters"
python3 build_banners.py

echo "==> render banners via headless Chrome (2x, then downscale)"
python3 - <<'EOF'
import json, subprocess, os
sizes = json.load(open("sizes.json"))
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for name, (w, h) in sizes.items():
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={w},{h}",
                    f"--screenshot={name}@2x.png", f"file://{os.getcwd()}/{name}.html"],
                   check=True, capture_output=True)
    subprocess.run(["magick", f"{name}@2x.png", "-resize", f"{w}x{h}", f"../{name}.png"], check=True)
    os.remove(f"{name}@2x.png")
    print(f"  {name}.png {w}x{h}")
EOF

echo "==> avatar.png (1024)"
rsvg-convert -w 1024 -h 1024 "$ASSETS/logo.svg" -o "$ASSETS/avatar.png"

echo "done."
