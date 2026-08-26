#!/usr/bin/env python3
"""Extract 'keelinfra' glyph outlines from Avenir Next as SVG path data.

Emits one <path> per letter, positioned on a shared baseline in font units
(1000 upm), y-down already applied. Prints total advance width.
"""
from fontTools.ttLib import TTCollection
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.svgPathPen import SVGPathPen
import json, sys

TTC = "/System/Library/Fonts/Avenir Next.ttc"
WANT_FACE = sys.argv[1] if len(sys.argv) > 1 else "Avenir Next Demi Bold"
TEXT = "keelinfra"
TRACKING = -6  # font units per 1000 upm, slight tightening

coll = TTCollection(TTC)
font = None
for f in coll.fonts:
    name = f["name"].getDebugName(4)  # full name
    if name == WANT_FACE:
        font = f
        break
if font is None:
    names = [f["name"].getDebugName(4) for f in coll.fonts]
    sys.exit(f"face not found; available: {names}")

upm = font["head"].unitsPerEm
cmap = font.getBestCmap()
glyph_set = font.getGlyphSet()
hmtx = font["hmtx"]

x = 0.0
paths = []
for ch in TEXT:
    gname = cmap[ord(ch)]
    pen = SVGPathPen(glyph_set)
    # flip y (font y-up -> svg y-down), shift to current x
    tpen = TransformPen(pen, (1, 0, 0, -1, x, 0))
    glyph_set[gname].draw(tpen)
    d = pen.getCommands()
    paths.append({"char": ch, "d": d})
    adv, _ = hmtx[gname]
    x += adv + TRACKING
x -= TRACKING  # no tracking after last glyph

# vertical metrics
os2 = font["OS/2"]
result = {
    "face": WANT_FACE,
    "upm": upm,
    "width": x,
    "capHeight": os2.sCapHeight,
    "xHeight": os2.sxHeight,
    "ascender": font["hhea"].ascent,
    "descender": font["hhea"].descent,
    "paths": paths,
}
print(json.dumps(result))
