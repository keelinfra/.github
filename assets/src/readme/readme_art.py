#!/usr/bin/env python3
"""Build the README artwork for keelinfra repositories.

Every image is an SVG with its text converted to outlines (IBM Plex, in
fonts/), so it renders the same on github.com, in the GitHub apps and in any
viewer, with no font download. Each image comes in a light and a dark version
for <picture> with prefers-color-scheme.

The facts drawn into the images are the constants below; update them and run

    pip install fonttools brotli uharfbuzz
    python3 readme_art.py --repos ~/src/keelinfra

with the keelinfra repositories cloned side by side under --repos. It writes

    .github/assets/readme/              org profile hero and project cards
    agent8/.github/readme/              Agent8 hero
    jenkins-extended-security/.github/readme/
    jenkins-upgrade-check/.github/readme/   (strip drawn from matrix.json)
    aix-runner/.github/readme/
    jenkins-bench/.github/readme/
"""
import argparse
import io
import json
import os
import re
import urllib.request

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(os.path.dirname(HERE))  # .github/assets

# ---------------------------------------------------------------- facts ----
UPSTREAM_LTS = "2.580.2"            # current upstream LTS (Java 21 only)
JES_RELEASE = "2.541.3-k4"          # latest jenkins-extended-security release
JES_RELEASE_DOTS = 3                # releases on the line so far: k2, k3, k4
JES_CVES = 41                       # core/Remoting/Stapler CVEs in COVERAGE.md
JES_ADVISORY = "2026-10-28"         # newest advisory covered
MATRIX_URL = ("https://raw.githubusercontent.com/keelinfra/jenkins-upgrade-check/"
              f"matrix/{UPSTREAM_LTS}/matrix.json")
MATRIX_STARTS = 328                 # Jenkins starts in that matrix run
AIX_RUNNER = "v19.5.1"              # latest aix-runner release (= upstream gitlab-runner tag)
BENCH_CONTROLS = 15                 # controls in jenkins-bench (14 CIS + plugin updates)
BENCH_VERIFIED = "2.541.3 \u00b7 2.580.1"  # LTS lines its e2e fixture runs against

# ---------------------------------------------------------------- theme ----
THEMES = {
    "light": dict(
        bg="#f6f7f9", panel="#ffffff", ink="#0f1c2a", body="#3b4a59", muted="#556574",
        line="#e2e7ed", line_strong="#cdd5de", dot="#dde3ea", accent="#9a5b06",
        amber="#e8a33d", navy="#0b2239", chip_bg="#eef1f5", chip_ink="#3b4a59",
        ok_bg="#e6f4ec", ok_ink="#145c3b", exp_bg="#fdf1dc", exp_ink="#7a4705",
        st_ok="#1f8a5a", st_part="#d99a2b", st_no="#c8412f", bad="#b4321f", good="#17734a",
        shadow="#0f1c2a", shadow_op="0.10", ctl_stroke="#24425f", tile_stroke="none",
    ),
    "dark": dict(
        bg="#0c141d", panel="#121e2a", ink="#e4ecf3", body="#c3d0dc", muted="#8fa1b3",
        line="#22303e", line_strong="#33465a", dot="#1d2a37", accent="#e8a33d",
        amber="#e8a33d", navy="#0b2239", chip_bg="#1c2a38", chip_ink="#c3d0dc",
        ok_bg="#12352a", ok_ink="#8fe0b5", exp_bg="#3a2a10", exp_ink="#f3cf8f",
        st_ok="#2e9d6a", st_part="#bf8a1c", st_no="#e0566a", bad="#f0788a", good="#4cc38a",
        shadow="#000000", shadow_op="0.45", ctl_stroke="#2d4f70", tile_stroke="#2d4f70",
    ),
}

# ---------------------------------------------------------------- fonts ----
class Face:
    def __init__(self, fname):
        tt = TTFont(os.path.join(HERE, "fonts", fname))
        tt.flavor = None
        buf = io.BytesIO()
        tt.save(buf)
        self.hbfont = hb.Font(hb.Face(buf.getvalue()))
        self.upem = tt["head"].unitsPerEm
        self.glyphs = tt.getGlyphSet()
        self.order = tt.getGlyphOrder()

    def shape(self, s):
        b = hb.Buffer()
        b.add_str(s)
        b.guess_segment_properties()
        hb.shape(self.hbfont, b, {"kern": True, "liga": True})
        return [(self.order[i.codepoint], p.x_advance, p.x_offset, p.y_offset)
                for i, p in zip(b.glyph_infos, b.glyph_positions)]


FACES = {}


def face(family, weight):
    key = f"plex-{family}-{weight}.woff2"
    if key not in FACES:
        FACES[key] = Face(key)
    return FACES[key]


ARROW = "\u2192"  # not in the Plex subset: drawn as a line and a head


def width(s, size, family="sans", weight=400, ls=0.0):
    f = face(family, weight)
    total = 0.0
    for i, seg in enumerate(s.split(ARROW)):
        if i:
            total += size * 0.9
        total += sum(a for _, a, _, _ in f.shape(seg)) * size / f.upem if seg else 0
    return total + ls * max(len(s) - 1, 0)


# Glyph outlines are defined once per image and placed with <use>.
GLYPHS = {}


def glyph_ref(fkey, f, name):
    gid = f"{fkey}-{name}"
    if gid not in GLYPHS:
        pen = SVGPathPen(f.glyphs, ntos=lambda v: f"{v:.0f}")
        f.glyphs[name].draw(pen)
        GLYPHS[gid] = pen.getCommands()
    return gid if GLYPHS[gid] else None


def text(x, y, s, size, fill, family="sans", weight=400, anchor="start", ls=0.0, extra=""):
    """Outlined text. y is the baseline. ls = letter spacing in px."""
    fkey = f"{family[0]}{weight // 100}"
    f = face(family, weight)
    k = size / f.upem
    w = width(s, size, family, weight, ls)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    out = []
    cx = x
    for i, seg in enumerate(s.split(ARROW)):
        if i:
            a, b, yy, hh = cx + size * 0.12, cx + size * 0.72, y - size * 0.3, size * 0.2
            out.append(f'<path d="M{a:.1f} {yy:.1f}H{b:.1f}M{b - hh:.1f} {yy - hh:.1f}L{b:.1f} {yy:.1f}'
                       f'L{b - hh:.1f} {yy + hh:.1f}" fill="none" stroke="{fill}" '
                       f'stroke-width="{size * 0.085:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
            cx += size * 0.9 + ls
        if not seg:
            continue
        for name, adv, xo, yo in f.shape(seg):
            ref = glyph_ref(fkey, f, name)
            if ref:
                out.append(f'<use href="#{ref}" transform="matrix({k:.4f} 0 0 {-k:.4f} '
                           f'{cx + xo * k:.1f} {y - yo * k:.1f})"/>')
            cx += adv * k + ls
    return f'<g fill="{fill}"{extra}>{"".join(out)}</g>'


def lines(x, y, rows, size, lh, fill, **kw):
    return "".join(text(x, y + i * lh, r, size, fill, **kw) for i, r in enumerate(rows))


def fit(s, size, maxw, family="sans", weight=400, ls=0.0):
    while width(s, size, family, weight, ls) > maxw and size > 8:
        size -= 0.5
    return size

# --------------------------------------------------------------- pieces ----
MARK = ("M112 96V416M112 256L272 96M112 256L272 416M336 96C384 144 400 208 400 256"
        "C400 304 384 368 336 416")


def wordmark(x, y, h, theme):
    """The keelinfra wordmark from assets/wordmark-*.svg, h px tall."""
    src = open(os.path.join(ASSETS, f"wordmark-{theme}.svg")).read()
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S)
    w = h * 680 / 128
    return (f'<svg x="{x}" y="{y}" width="{w:.1f}" height="{h}" viewBox="0 0 680 128">'
            f"{inner}</svg>")


def tile(x, y, s, icon, t):
    """Project icon: amber line icon on a navy tile, as on keelinfra.io."""
    k = s / 48
    return (f'<g transform="translate({x} {y}) scale({k:.4f})">'
            f'<rect width="48" height="48" rx="10" fill="{t["navy"]}" stroke="{t["tile_stroke"]}"/>'
            f'<g transform="translate(11 11)" fill="none" stroke="#e8a33d" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g></g>')


ICONS = {
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "agent": '<rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>'
             '<path d="M6.5 14v-2.5a2 2 0 0 1 2-2h3M17.5 10v2.5a2 2 0 0 1-2 2h-3"/>',
    "grid": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
    "runner": '<rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/>'
              '<path d="M7 7.5h.01M7 16.5h.01M11 7.5h6M11 16.5h6"/>',
}


def chip(x, y, label, kind, t, size=15):
    """Pill like the site's .chip; returns (svg, width). y = top."""
    h = size * 2.15
    pad = size * 0.8
    dot = kind in ("ok", "exp")
    tw = width(label, size, "sans", 600)
    w = tw + 2 * pad + (size * 0.85 if dot else 0)
    bg, ink = {"ok": (t["ok_bg"], t["ok_ink"]), "exp": (t["exp_bg"], t["exp_ink"])}.get(
        kind, (t["chip_bg"], t["chip_ink"]))
    out = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" fill="{bg}"/>'
    tx = x + pad
    if kind == "ok":
        out += f'<circle cx="{tx + size*0.25:.1f}" cy="{y + h/2:.1f}" r="{size*0.24:.1f}" fill="{ink}"/>'
        tx += size * 0.85
    elif kind == "exp":
        out += (f'<circle cx="{tx + size*0.25:.1f}" cy="{y + h/2:.1f}" r="{size*0.2:.1f}" fill="none" '
                f'stroke="{ink}" stroke-width="{size*0.1:.1f}"/>')
        tx += size * 0.85
    out += text(tx, y + h / 2 + size * 0.36, label, size, ink, weight=600)
    return out, w


def chips(x, y, items, t, size=15, gap=10):
    out = ""
    for label, kind in items:
        s, w = chip(x, y, label, kind, t, size)
        out += s
        x += w + gap
    return out


def check(x, y, s, t):
    """Green check mark, 1em = s, (x, y) = left of the baseline."""
    return (f'<path d="M{x:.1f} {y - s*0.36:.1f}l{s*0.3:.1f} {s*0.3:.1f} {s*0.58:.1f}-{s*0.62:.1f}" '
            f'fill="none" stroke="{t["good"]}" stroke-width="{s*0.12:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')


def cross(x, y, s, t):
    c = t["bad"]
    a, b = x + s * 0.1, x + s * 0.7
    top, bot = y - s * 0.66, y - s * 0.06
    return (f'<path d="M{a:.1f} {top:.1f}L{b:.1f} {bot:.1f}M{b:.1f} {top:.1f}L{a:.1f} {bot:.1f}" '
            f'stroke="{c}" stroke-width="{s*0.12:.1f}" stroke-linecap="round"/>')


def defs(t, uid):
    return (f'<defs><pattern id="dots{uid}" width="18" height="18" patternUnits="userSpaceOnUse">'
            f'<circle cx="1.5" cy="1.5" r="1.3" fill="{t["dot"]}"/></pattern>'
            f'<filter id="sh{uid}" x="-10%" y="-10%" width="120%" height="135%">'
            f'<feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="{t["shadow"]}" '
            f'flood-opacity="{t["shadow_op"]}"/></filter></defs>')


def card(x, y, w, h, t, uid, dots=True, shadow=True):
    f = f' filter="url(#sh{uid})"' if shadow else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{t["panel"]}"{f}/>'
    if dots:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#dots{uid})"/>'
    out += (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="15.5" fill="none" '
            f'stroke="{t["line"]}"/>')
    return out


MOTION = """<style>
.draw{stroke-dasharray:var(--len);stroke-dashoffset:var(--len);animation:draw 1.6s .3s cubic-bezier(.6,0,.2,1) forwards}
.pop{opacity:0;animation:pop .5s ease-out forwards}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.8s ease-out 2s infinite}
.flow{animation:flow 1.4s linear infinite}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes pop{to{opacity:1}}
@keyframes pulse{0%{transform:scale(1);opacity:.6}70%,100%{transform:scale(2.4);opacity:0}}
@keyframes flow{to{stroke-dashoffset:-18}}
@media (prefers-reduced-motion:reduce){.draw{animation:none;stroke-dashoffset:0}.pop{animation:none;opacity:1}.pulse,.flow{animation:none}}
</style>"""


def svg(w, h, title, desc, body):
    glyphs = "".join(f'<path id="{g}" d="{d}"/>' for g, d in sorted(GLYPHS.items()) if d)
    GLYPHS.clear()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d">\n'
            f"<!-- Generated by keelinfra/.github assets/src/readme/readme_art.py; edit that, not this. -->\n"
            f'<title id="t">{title}</title><desc id="d">{desc}</desc>\n{MOTION}\n'
            f'<defs>{glyphs}</defs>\n{body}\n</svg>\n')

# ------------------------------------------------------------- diagrams ----

def release_lines(ox, oy, t, compact=False):
    """Upstream LTS line and the keelinfra 2.541.x branch, in a 488 wide box."""
    m = "mono"
    o = ""
    o += text(ox, oy + 16, "UPSTREAM JENKINS LTS", 15.5, t["muted"], m, 600, ls=1.6)
    y = oy + 82
    xs = (ox + 78, ox + 262, ox + 410)
    o += f'<path d="M{ox} {y}H{ox + 478}" stroke="{t["line_strong"]}" stroke-width="2.5" fill="none"/>'
    o += (f'<path d="M{ox + 470} {y - 7}l9 7-9 7" stroke="{t["line_strong"]}" stroke-width="2.5" '
          f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    for x, v in zip(xs, ("2.541.3", "2.555.1", UPSTREAM_LTS)):
        o += f'<circle cx="{x}" cy="{y}" r="7.5" fill="{t["panel"]}" stroke="{t["muted"]}" stroke-width="2.5"/>'
        o += text(x, y - 21, v, 19, t["ink"], m, 500, anchor="middle")
    o += text(ox + 22, y + 34, "Java 17", 16.5, t["muted"], m, 400, anchor="middle")
    o += text((xs[1] + xs[2]) / 2, y + 34, "Java 21 only", 16.5, t["muted"], m, 400, anchor="middle")
    by = y + 118
    path = f"M{xs[0]} {y + 8}C{xs[0]} {by - 40} {xs[0] + 36} {by} {xs[0] + 100} {by}H{ox + 478}"
    o += (f'<path class="draw" style="--len:620" d="{path}" stroke="{t["amber"]}" stroke-width="3.2" '
          f'fill="none" stroke-linecap="round"/>')
    dots = [xs[2] - 80 * i for i in range(JES_RELEASE_DOTS)][::-1]
    for i, x in enumerate(dots):
        o += (f'<circle class="pop" style="animation-delay:{1.2 + .2 * i:.1f}s" cx="{x}" cy="{by}" r="6.5" '
              f'fill="{t["amber"]}"/>')
    o += (f'<circle class="pulse" cx="{xs[2]}" cy="{by}" r="7" fill="none" stroke="{t["amber"]}" '
          f'stroke-width="2"/>')
    o += f'<circle cx="{xs[2]}" cy="{by}" r="13" fill="none" stroke="{t["amber"]}" stroke-width="1.6" opacity=".45"/>'
    o += text(xs[2] - 6, by - 25, JES_RELEASE, 19, t["accent"], m, 600, anchor="middle")
    o += text(xs[0] + 50, by + 47, "keelinfra 2.541.x, still on Java 17", 21, t["ink"], "sans", 600)
    o += text(xs[0] + 50, by + 74, "with the core security fixes released after it", 17, t["muted"], "sans", 400)
    return o, by + 74 - oy


def hosts(ox, oy, t, rows, w=488, lane="BUILD HOSTS THAT KEEP THEIR JAVA", tag="agent8",
          box=("controller", "Java 21")):
    """Pills on the left converge through an amber tag into a navy box (agent8 by default)."""
    o = text(ox, oy + 16, lane, 15.5, t["muted"], "mono", 600, ls=1.6)
    ph, gap, pw = 40, 11, 200
    top = oy + 40
    cys = [top + ph / 2 + i * (ph + gap) for i in range(len(rows))]
    mid = (cys[0] + cys[-1]) / 2
    cx0 = ox + w - 150
    for cy in cys:
        o += (f'<path class="flow" d="M{ox + pw} {cy}C{ox + pw + 90} {cy} {cx0 - 110} {mid} {cx0} {mid}" '
              f'stroke="{t["amber"]}" stroke-width="2" fill="none" stroke-dasharray="6 3"/>')
    for cy, r in zip(cys, rows):
        o += (f'<rect x="{ox}" y="{cy - ph/2}" width="{pw}" height="{ph}" rx="{ph/2}" fill="{t["chip_bg"]}" '
              f'stroke="{t["line_strong"]}"/>')
        o += text(ox + pw / 2, cy + 6, r, 17, t["ink"], "mono", 400, anchor="middle")
    tx = (ox + pw + cx0) / 2 + 4
    tw = max(92, width(tag, 17, "mono", 600) + 26)
    o += f'<rect x="{tx - tw / 2:.1f}" y="{mid - 16}" width="{tw:.1f}" height="32" rx="16" fill="{t["amber"]}"/>'
    o += text(tx, mid + 6, tag, 17, "#0b2239", "mono", 600, anchor="middle")
    o += (f'<rect x="{cx0}" y="{mid - 40}" width="150" height="80" rx="12" fill="{t["navy"]}" '
          f'stroke="{t["ctl_stroke"]}"/>')
    o += text(cx0 + 75, mid - 7, box[0], 15.5, "#8fa6bc", "mono", 400, anchor="middle", ls=1)
    o += text(cx0 + 75, mid + 23, box[1], 21, "#ffffff", "mono", 600, anchor="middle")
    return o, cys[-1] + ph / 2 - oy


def matrix_strip(ox, oy, t, m, w=488):
    rows = [r for r in m["rows"] if r["top"] == 300]
    n = len(rows)
    lw = 106
    gap = 2.4
    cw = (w - lw - gap * (n - 1)) / n
    o = text(ox, oy + 16, f"EVERY LTS LINE → {m['to']} · 300 PLUGINS", 15.5, t["muted"], "mono", 600, ls=1.6)
    for ri, (label, key) in enumerate((("core only", "core"), ("in steps", "steps"))):
        y = oy + 44 + ri * 76
        o += text(ox, y + 38, label, 16.5, t["muted"], "mono", 400)
        for i, r in enumerate(rows):
            if key == "core":
                a = r["asIs"]
                cls = "no" if not a["started"] else ("part" if a["failed"] or a["broken"] else "ok")
            else:
                last = r["stops"][-1]
                cls = "ok" if last["started"] and not last["failed"] and not last["broken"] else "part"
            x = ox + lw + i * (cw + gap)
            delay = 0.25 + i * 0.03 + ri * 0.5
            o += (f'<rect class="pop" style="animation-delay:{delay:.2f}s" x="{x:.1f}" y="{y}" '
                  f'width="{cw:.1f}" height="60" rx="3" fill="{t["st_" + cls]}"/>')
    ty = oy + 44 + 2 * 76 + 6
    picks = [0, n - 1]
    for i in picks:
        x = ox + lw + i * (cw + gap)
        end = i == n - 1
        lx = x + cw if end else x
        o += f'<path d="M{lx:.1f} {ty - 6}V{ty + 16}" stroke="{t["line_strong"]}" stroke-width="1.5"/>'
        o += text(lx + (-6 if end else 6), ty + 12, rows[i]["from"], 15, t["muted"], "mono", 400,
                  anchor="end" if end else "start")
    return o, ty + 16 - oy, rows


def stat_row(ox, y, w, items, t):
    """Big mono figures with a small label underneath, evenly spread."""
    o = f'<path d="M{ox} {y}H{ox + w}" stroke="{t["line_strong"]}" stroke-dasharray="2 5"/>'
    cw = w / len(items)
    bs = min(fit(big, 30, cw - 14, "mono", 600) for big, _, _ in items)
    ss = min(fit(small, 16, cw - 8) for _, small, _ in items)
    for i, (big, small, color) in enumerate(items):
        x = ox + i * cw
        o += text(x, y + 46, big, bs, color or t["ink"], "mono", 600)
        o += text(x, y + 74, small, ss, t["muted"], "sans", 400)
    return o

# ---------------------------------------------------------------- heroes ----

def hero(theme, uid, eyebrow, title, tagline, chip_items, diagram, h=520, title_hl=None, wm=34):
    """Copy on the left, a diagram card on the right, as on keelinfra.io."""
    t = THEMES[theme]
    W = 1280
    o = defs(t, uid)
    o += f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="24" fill="{t["bg"]}" stroke="{t["line"]}"/>'
    o += wordmark(64, 52, wm, theme)
    ts = min(fit(r, 58, 560, "sans", 700, -1.2) for r in title)
    block = (12 + ts * 1.25 + (len(title) - 1) * ts * 1.08 + 58 + 34 * (len(tagline) - 1)
             + (66 if chip_items else 0))
    top = 52 + wm + 14
    e = top + (h - 44 - top - block) / 2 + 12
    o += text(64, e, eyebrow, 16.5, t["accent"], "mono", 500, ls=0.6)
    y = e + ts * 1.25
    for i, r in enumerate(title):
        if i:
            y += ts * 1.08
        x = 64
        parts = [(r, t["ink"])]
        if title_hl and title_hl in r:
            pre, post = r.split(title_hl, 1)
            parts = [(pre, t["ink"]), (title_hl, t["accent"]), (post, t["ink"])]
        for part, col in parts:
            if part:
                o += text(x, y, part, ts, col, "sans", 700, ls=-1.2)
                x += width(part, ts, "sans", 700, -1.2) - 1.2
    y += 58
    o += lines(64, y, tagline, 22.5, 34, t["body"])
    y += 34 * (len(tagline) - 1) + 34
    if chip_items:
        o += chips(64, y, chip_items, t, 16)
    cx, cy, cw, ch = 680, 44, 552, h - 88
    o += card(cx, cy, cw, ch, t, uid)
    o += diagram(cx + 32, cy + 32, t)
    return o


def hero_jes(theme):
    def diagram(x, y, t):
        o, used = release_lines(x, y, t)
        o += stat_row(x, y + used + 26, 488, [
            (str(JES_CVES), "core CVEs backported", None),
            (JES_ADVISORY, "newest advisory covered", None),
            ("17 · 21", "Java versions in CI", None),
        ], t)
        return o
    body = hero(theme, "j", "jenkins · security backports · java 17",
                ["Extended Security", "for Jenkins 2.541.x"],
                ["Jenkins 2.541.3, the last LTS that runs on Java 17,",
                 "with the core security fixes released after it.",
                 "Each fix listed with its upstream commit."],
                [(f"Released {JES_RELEASE}", "ok"), ("Not an official Jenkins release", None)],
                diagram)
    return svg(1280, 520, "Extended Security for Jenkins 2.541.x",
               f"Upstream Jenkins LTS moves from 2.541.3 on Java 17 to 2.555.1 and {UPSTREAM_LTS} on Java 21 only. "
               f"keelinfra's 2.541.x line branches off at 2.541.3 and stays on Java 17 with the core security "
               f"fixes released after it, now at {JES_RELEASE}: {JES_CVES} core CVEs, up to the "
               f"{JES_ADVISORY} advisory, built and tested in CI on Java 17 and 21.", body)


def hero_agent8(theme):
    def diagram(x, y, t):
        o, used = hosts(x, y, t, ["AIX · Java 8", "Solaris · Java 8", "HP-UX · Java 8",
                                  "CentOS 6 · Java 8"])
        yy = y + used + 30
        o += f'<path d="M{x} {yy}H{x + 488}" stroke="{t["line_strong"]}" stroke-dasharray="2 5"/>'
        o += cross(x, yy + 44, 18, t)
        o += text(x + 28, yy + 44, "stock agent.jar", 17, t["ink"], "mono", 500)
        o += text(x + 488, yy + 44, "UnsupportedClassVersionError", fit("UnsupportedClassVersionError", 17, 280, "mono"),
                  t["bad"], "mono", 400, anchor="end")
        o += check(x + 1, yy + 80, 18, t)
        o += text(x + 28, yy + 80, "agent8", 17, t["ink"], "mono", 500)
        o += text(x + 488, yy + 80, "connects, builds run", 17, t["good"], "mono", 400, anchor="end")
        return o
    body = hero(theme, "a", "jenkins agents · java 8, 11, 17",
                ["Agent8", "for Jenkins"],
                ["Run Jenkins agents on build hosts stuck on",
                 "Java 8, 11 or 17, while the controller moves",
                 "to Java 21. The host keeps its Java."],
                [("Available", "ok"), ("Tested on AIX · Solaris · HP-UX", "ok")],
                diagram)
    return svg(1280, 520, "Agent8 for Jenkins",
               "Build hosts on AIX, Solaris, HP-UX and CentOS 6 keep Java 8 and connect to a Jenkins controller "
               "on Java 21 through agent8. The stock agent.jar fails there with UnsupportedClassVersionError; "
               "agent8 connects and runs builds.", body)


def hero_upgrade(theme, m):
    rows = [r for r in m["rows"] if r["top"] == 300]
    no = sum(1 for r in rows if not r["asIs"]["started"])
    part = sum(1 for r in rows if r["asIs"]["started"] and (r["asIs"]["failed"] or r["asIs"]["broken"]))
    share = sum(r["share"] for r in rows if not r["asIs"]["started"]
                or r["asIs"]["failed"] or r["asIs"]["broken"]) * 100
    ok_steps = sum(1 for r in rows if r["stops"][-1]["started"] and not r["stops"][-1]["failed"]
                   and not r["stops"][-1]["broken"])

    def diagram(x, y, t):
        o, used, _ = matrix_strip(x, y, t, m)
        o += stat_row(x, y + used + 26, 488, [
            (f"{no} + {part}", "lines break core-only", t["st_no"]),
            (f"{share:.1f}%", "of controllers on them", None),
            (f"{ok_steps}/{len(rows)}", "load every plugin in steps", t["good"]),
        ], t)
        ly = y + used + 26 + 116
        lx = x
        for cls, label in (("ok", "every plugin loads"), ("part", "starts, plugins fail"), ("no", "does not start")):
            o += f'<rect x="{lx}" y="{ly - 12}" width="13" height="13" rx="3" fill="{t["st_" + cls]}"/>'
            o += text(lx + 21, ly, label, 16, t["muted"])
            lx += 21 + width(label, 16) + 22
        return o
    body = hero(theme, "u", f"jenkins upgrades · 2.60.3 → {m['to']}",
                ["Jenkins", "upgrade check"],
                [f"Every LTS line since 2.60.3, upgraded to {m['to']}",
                 "in a rehearsal: what broke, and the stops",
                 "that work. Then rehearse your own controller."],
                [(f"Matrix for {m['to']}", "ok"), (f"{MATRIX_STARTS} Jenkins starts", None)],
                diagram)
    return svg(1280, 520, "Jenkins upgrade check",
               f"One bar per Jenkins LTS line from {rows[0]['from']} to {rows[-1]['from']}, upgraded to {m['to']} "
               f"with the 300 most installed plugins. Replacing only the core, Jenkins does not start from {no} "
               f"lines and starts with plugins failing from {part}; {share:.1f}% of reporting controllers are on "
               f"those lines. Going through the planned stops, {ok_steps} of {len(rows)} load every plugin.", body)


def hero_aix(theme):
    def diagram(x, y, t):
        o, used = hosts(x, y, t, ["machineid", "moby/term", "go-billy/v5", "go-git/v5"],
                        lane=f"GITLAB-RUNNER {AIX_RUNNER} + 4 PATCHES", tag="go build", box=("GOOS=aix", "ppc64"))
        yy = y + used + 30
        o += f'<path d="M{x} {yy}H{x + 488}" stroke="{t["line_strong"]}" stroke-dasharray="2 5"/>'
        o += text(x, yy + 40, "TESTED ON AIX 7.3 \u00b7 SHELL EXECUTOR", 15.5, t["muted"], "mono", 600, ls=1.6)
        items = ["register", "jobs", "artifacts", "local cache", "git clone", "cancel"]
        for i, it in enumerate(items):
            cx = x + (0, 182, 336)[i % 3]
            cy = yy + 78 + (i // 3) * 34
            o += check(cx + 1, cy, 18, t)
            o += text(cx + 28, cy, it, 17, t["ink"], "mono", 400)
        return o
    body = hero(theme, "x", "gitlab runner \u00b7 aix 7.2, 7.3 \u00b7 ppc64",
                ["AIX Runner", "for GitLab"],
                ["GitLab Runner for AIX 7.2 and 7.3, which GitLab",
                 "doesn\u2019t ship. The unmodified upstream runner,",
                 "with four small dependency patches."],
                [("Experimental", "exp"), ("Tested on AIX 7.3", "ok")],
                diagram)
    return svg(1280, 520, "AIX Runner for GitLab",
               f"The upstream gitlab-runner {AIX_RUNNER}, unmodified, plus patches to four dependencies "
               f"(machineid, moby/term, go-billy, go-git), built with GOOS=aix GOARCH=ppc64. Tested on AIX 7.3 "
               f"with the shell executor: register, jobs, artifacts, local cache, git clone and cancel.", body)


def hero_profile(theme):
    def diagram(x, y, t):
        o, used = release_lines(x, y, t)
        yy = y + used + 28
        o += f'<path d="M{x} {yy}H{x + 488}" stroke="{t["line_strong"]}" stroke-dasharray="2 5"/>'
        d, _ = hosts(x, yy + 26, t, ["AIX \u00b7 Java 8", "Solaris \u00b7 Java 8", "HP-UX \u00b7 Java 8"])
        return o + d
    body = hero(theme, "p", "open source \u00b7 tested in public \u00b7 built with its users",
                ["CI that can\u2019t", "upgrade yet, kept", "running."],
                ["Plenty of CI can\u2019t move to what upstream supports.",
                 "keelinfra keeps shipping tested, open-source builds",
                 "for it until it can, and publishes the CI runs and",
                 "test data behind what it says."],
                None, diagram, h=660, title_hl="running", wm=40)
    return svg(1280, 660, "keelinfra: CI that can't upgrade yet, kept running",
               f"Upstream Jenkins moves from 2.541.3 on Java 17 to 2.555.1 and {UPSTREAM_LTS} on Java 21 only. "
               f"keelinfra's 2.541.x line branches off at 2.541.3 and stays on Java 17 with later core security "
               f"fixes, now at {JES_RELEASE}. Below, build hosts on AIX, Solaris and HP-UX keep Java 8 and connect "
               f"to a Java 21 controller through Agent8.", body)


def findings(ox, oy, t, rows, w=488, lane="SCAN --DEMO \u00b7 THE BUNDLED SAMPLE"):
    """Report rows: a status pill, the control and what the scan saw."""
    o = text(ox, oy + 16, lane, 15.5, t["muted"], "mono", 600, ls=1.6)
    rh, pw, ph = 47, 86, 30
    kinds = {"FAIL": (t["st_no"], "#ffffff", None), "PASS": (t["ok_bg"], t["ok_ink"], None),
             "MANUAL": (t["exp_bg"], t["exp_ink"], t["st_part"])}
    for i, (status, cid, what) in enumerate(rows):
        y = oy + 38 + i * rh
        cy = y + ph / 2
        bg, ink, stroke = kinds[status]
        s = f' stroke="{stroke}" stroke-width="1.4"' if stroke else ""
        o += f'<g class="pop" style="animation-delay:{0.3 + 0.18 * i:.2f}s">'
        o += f'<rect x="{ox}" y="{y}" width="{pw}" height="{ph}" rx="{ph / 2}" fill="{bg}"{s}/>'
        o += text(ox + pw / 2, cy + 5.5, status, 14.5, ink, "mono", 600, anchor="middle", ls=0.6)
        o += text(ox + pw + 14, cy + 6, cid, 16, t["accent"], "mono", 500)
        tx = ox + pw + 14 + width("CIS-2.1.6", 16, "mono", 500) + 16
        o += text(tx, cy + 6, what, fit(what, 16.5, ox + w - tx), t["ink"], "sans", 400)
        o += "</g>"
        if i < len(rows) - 1:
            ly = y + ph + (rh - ph) / 2
            o += f'<path d="M{ox} {ly:.1f}H{ox + w}" stroke="{t["line"]}"/>'
    return o, 38 + (len(rows) - 1) * rh + ph


def hero_bench(theme):
    def diagram(x, y, t):
        o, used = findings(x, y, t, [
            ("FAIL", "CIS-2.1.6", "anonymous GET of the API returned 200"),
            ("FAIL", "CIS-2.2.3", "2 executors on the built-in node"),
            ("FAIL", "CIS-2.1.2", "pipeline runs outside the Groovy sandbox"),
            ("PASS", "CIS-2.1.5", "CSRF protection is enabled"),
            ("MANUAL", "CIS-2.3.5", "job config needs Job/ExtendedRead"),
        ])
        o += stat_row(x, y + used + 28, 488, [
            (str(BENCH_CONTROLS), "controls, CIS section 2", None),
            ("GET", "the only request it sends", None),
            ("MANUAL", "when it can\u2019t see, not PASS", t["accent"]),
        ], t)
        return o
    body = hero(theme, "b", "jenkins \u00b7 cis supply chain \u00b7 read-only",
                ["Supply-chain audit", "for Jenkins"],
                ["Scan a controller against the Build Pipelines",
                 "section of the CIS Software Supply Chain guide.",
                 "Each finding names the setting that fixes it."],
                [(f"Verified on {BENCH_VERIFIED}", "ok"), ("Read-only token", None)],
                diagram)
    return svg(1280, 520, "jenkins-bench: supply-chain audit for Jenkins",
               "Report rows from jenkins-bench scanning its bundled sample controller: CIS-2.1.6 FAIL, an anonymous "
               "GET of the API returned 200; CIS-2.2.3 FAIL, 2 executors on the built-in node; CIS-2.1.2 FAIL, a "
               "pipeline runs outside the Groovy sandbox; CIS-2.1.5 PASS, CSRF protection is enabled; CIS-2.3.5 "
               f"MANUAL, the job configuration needs Job/ExtendedRead. {BENCH_CONTROLS} controls from CIS section 2, "
               "GET requests only, and a control it cannot see reports MANUAL rather than PASS.", body)


# ----------------------------------------------------------------- cards ----
CARDS = {
    "jenkins-extended-security": dict(
        icon="shield", title="Extended Security for Jenkins 2.541.x",
        repo="keelinfra/jenkins-extended-security · MIT",
        chips=[("Released", "ok"), ("Not an official Jenkins release", None)],
        pitch=["Jenkins 2.541.3, the last LTS that runs on Java 17,",
               "with the core security fixes released after it."],
        checks=["Each fix listed with its upstream commit",
                "Built and tested in public CI on Java 17 and 21",
                "Reproducible WAR, SBOM, attestation, Docker image"]),
    "agent8": dict(
        icon="agent", title="Agent8 for Jenkins", repo="keelinfra/agent8 · MIT",
        chips=[("Available", "ok"), ("Tested on AIX · Solaris · HP-UX", "ok")],
        pitch=["Run Jenkins agents on hosts stuck on Java 8, 11",
               "or 17, while the controller moves to Java 21."],
        checks=["The old host keeps its Java, stays an ordinary node",
                "Tested in CI on Linux, including RHEL/CentOS 6",
                "A release for each Jenkins version, one install script"]),
    "jenkins-upgrade-check": dict(
        icon="grid", title="Jenkins upgrade matrix",
        repo="keelinfra/jenkins-upgrade-check · Apache-2.0",
        chips=[("Published", "ok"), (f"{MATRIX_STARTS} Jenkins starts", None)],
        pitch=[f"Which Jenkins LTS lines can go straight to {UPSTREAM_LTS},",
               "and which need to stop on the way."],
        checks=["38 LTS lines, from 2.60.3 to 2.568.3",
                "The 100 and the 300 most installed plugins",
                "Core-only and stepped, with the Java for each step"]),
    "aix-runner": dict(
        icon="runner", title="AIX Runner for GitLab", repo="keelinfra/aix-runner · MIT",
        chips=[("Experimental", "exp"), ("Tested on AIX 7.3", "ok")],
        pitch=["GitLab Runner for AIX 7.2 and 7.3,",
               "which GitLab doesn\u2019t ship."],
        checks=["The unmodified upstream runner, four small patches",
                "Latest upstream release built daily in CI",
                "Shell executor tested: jobs, artifacts, cache, cancel"]),
}


def project_card(theme, key):
    c = CARDS[key]
    t = THEMES[theme]
    W, H = 640, 380
    uid = "c" + key[:3]
    o = defs(t, uid)
    o += card(1, 1, W - 2, H - 2, t, uid, dots=False, shadow=False)
    o += tile(36, 34, 52, c["icon"], t)
    ts = fit(c["title"], 28, W - 104 - 30, "sans", 600, -0.4)
    o += text(104, 59, c["title"], ts, t["ink"], "sans", 600, ls=-0.4)
    o += text(104, 84, c["repo"], 16, t["muted"], "mono", 400)
    o += chips(36, 112, c["chips"], t, 15)
    o += lines(36, 184, c["pitch"], 21, 30, t["ink"], weight=500)
    y = 184 + 30 * (len(c["pitch"]) - 1) + 50
    for s in c["checks"]:
        o += check(38, y, 18, t)
        o += text(68, y, s, fit(s, 18, W - 68 - 28), t["body"])
        y += 34
    return svg(W, H, c["title"], f'{c["title"]}: {" ".join(c["pitch"])} {". ".join(c["checks"])}.', o)

# ------------------------------------------------------------------ main ----

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  {path} ({len(content) // 1024} KB)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos", help="directory with the other keelinfra repositories cloned in it")
    ap.add_argument("--matrix", help="matrix.json to draw (default: download it)")
    a = ap.parse_args()
    for th in ("light", "dark"):
        write(os.path.join(ASSETS, "readme", f"profile-hero-{th}.svg"), hero_profile(th))
        for k in CARDS:
            write(os.path.join(ASSETS, "readme", f"card-{k}-{th}.svg"), project_card(th, k))
    if not a.repos:
        return
    if a.matrix:
        m = json.load(open(a.matrix))
    else:
        with urllib.request.urlopen(MATRIX_URL) as r:
            m = json.load(r)
    for repo, fn in (("agent8", hero_agent8), ("jenkins-extended-security", hero_jes),
                     ("jenkins-upgrade-check", lambda th: hero_upgrade(th, m)),
                     ("aix-runner", hero_aix), ("jenkins-bench", hero_bench)):
        root = os.path.join(a.repos, repo)
        if not os.path.isdir(root):
            print(f"  skip {repo}: not in {a.repos}")
            continue
        for th in ("light", "dark"):
            write(os.path.join(root, ".github", "readme", f"hero-{th}.svg"), fn(th))


if __name__ == "__main__":
    main()
