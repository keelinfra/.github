#!/usr/bin/env python3
"""Compose keelinfra logo SVG masters from the extracted wordmark paths."""
import json, os

BRAND_DIR = os.path.dirname(os.path.abspath(__file__))  # assets/src
ASSETS = os.path.dirname(BRAND_DIR)  # assets/

NAVY = "#0b2239"
AMBER = "#e8a33d"
INK_LIGHT = "#e4ecf3"   # text on dark backgrounds

wm = json.load(open(os.path.join(BRAND_DIR, "wordmark.json")))
WM_WIDTH = wm["width"]          # 3999 font units
WM_ASC = 756                    # top of k/l/f ascenders (measured)

# ---- the mark: K + hull curve, mastered on a 512 grid ----
K_STROKES = "M112 96V416M112 256L272 96M112 256L272 416M336 96C384 144 400 208 400 256C400 304 384 368 336 416"
SW = 42  # stroke width at 512

def mark_group(scale=1.0, tx=0.0, ty=0.0, color=AMBER, tile=NAVY, tile_stroke=None, rx=96):
    """Return SVG for the mark; tile=None -> transparent background mark."""
    parts = [f'<g transform="translate({tx} {ty}) scale({scale})">']
    if tile is not None:
        stroke_attr = f' stroke="{tile_stroke}" stroke-width="3"' if tile_stroke else ""
        parts.append(f'<rect width="512" height="512" rx="{rx}" fill="{tile}"{stroke_attr}/>')
    parts.append(
        f'<path d="{K_STROKES}" fill="none" stroke="{color}" stroke-width="{SW}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )
    parts.append("</g>")
    return "".join(parts)

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">\n{body}\n</svg>\n')

def write(name, content):
    path = os.path.join(ASSETS, name)
    with open(path, "w") as f:
        f.write(content)
    print("wrote", name, len(content), "bytes")

# 1. logo.svg — tile mark, 512
write("logo.svg", svg(512, 512, mark_group()))

# 2/3. transparent marks for light / dark surfaces
write("logo-mark-navy.svg", svg(512, 512, mark_group(color=NAVY, tile=None)))
write("logo-mark-amber.svg", svg(512, 512, mark_group(color=AMBER, tile=None)))

# 4/5. horizontal wordmark lockups, mastered at 128 tall
def wordmark(text_color, tile_stroke=None):
    H = 128
    tile_scale = H / 512.0            # tile at 128px
    s = 0.128                          # text scale: k-height ~97px
    gap = 34
    text_x = H + gap
    baseline = H / 2 + (WM_ASC / 2) * s
    text_w = WM_WIDTH * s
    total_w = round(text_x + text_w + 6)
    letters = "".join(f'<path d="{p["d"]}"/>' for p in wm["paths"])
    body = (
        mark_group(scale=tile_scale, tile_stroke=tile_stroke, rx=96)
        + f'\n<g fill="{text_color}" transform="translate({text_x} {baseline:.1f}) scale({s})">'
        + letters + "</g>"
    )
    return svg(total_w, H, body)

write("wordmark-light.svg", wordmark(NAVY))                      # for light backgrounds
write("wordmark-dark.svg", wordmark(INK_LIGHT, tile_stroke="#28394a"))  # for dark backgrounds

# 6. standalone text-only wordmark paths (for banner reuse), amber-free
letters = "".join(f'<path d="{p["d"]}"/>' for p in wm["paths"])
frag = f'<g transform="translate(0 {WM_ASC}) ">{letters}</g>'
with open(os.path.join(BRAND_DIR, "wordmark-textpaths.svg.frag"), "w") as f:
    f.write(letters)
print("wordmark text width @1em:", WM_WIDTH / 1000.0)
