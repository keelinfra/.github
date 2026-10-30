#!/usr/bin/env python3
"""Generate HTML masters for keelinfra banners; rendered via headless Chrome."""
import json, os

BRAND = os.path.dirname(os.path.abspath(__file__))
SRC = BRAND  # HTML masters live next to this script
wm = json.load(open(os.path.join(BRAND, "wordmark.json")))

NAVY, AMBER, INK, MUTED = "#0b2239", "#e8a33d", "#e4ecf3", "#8fa1b3"
LINE, BG_DEEP, GREEN, STEEL = "#22303e", "#0a1520", "#4cc38a", "#5f7d99"

K_STROKES = "M112 96V416M112 256L272 96M112 256L272 416M336 96C384 144 400 208 400 256C400 304 384 368 336 416"

def mark_svg(size, tile=True, color=AMBER):
    s = size / 512
    tile_el = f'<rect width="512" height="512" rx="96" fill="{NAVY}" stroke="#2a3b4d" stroke-width="4"/>' if tile else ""
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">'
            f'{tile_el}<path d="{K_STROKES}" fill="none" stroke="{color}" stroke-width="42" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def wordmark_svg(height, color=INK):
    """Text-only 'keelinfra' as paths. height = ascender-to-baseline pixel height."""
    s = height / 756.0
    w = wm["width"] * s
    letters = "".join(f'<path d="{p["d"]}"/>' for p in wm["paths"])
    return (f'<svg width="{w:.0f}" height="{height}" viewBox="0 0 {w:.0f} {height}" '
            f'xmlns="http://www.w3.org/2000/svg"><g fill="{color}" '
            f'transform="translate(0 {height}) scale({s:.5f})">{letters}</g></svg>')

def keel_ripples(height, n=5, x0=0):
    """Concentric hull curves, fading — the 'keel lines' motif."""
    paths = []
    for i in range(n):
        inset = i * 110
        op = 0.32 - i * 0.055
        sw = 10
        h = height
        bulge = 0.42 * h
        x = x0 - inset
        paths.append(
            f'<path d="M{x} 0 C{x + bulge * 0.75} {h * 0.25} {x + bulge} {h * 0.42} {x + bulge} {h / 2} '
            f'C{x + bulge} {h * 0.58} {x + bulge * 0.75} {h * 0.75} {x} {h}" '
            f'fill="none" stroke="{AMBER}" stroke-opacity="{op:.3f}" stroke-width="{sw}" stroke-linecap="round"/>')
    return "".join(paths)

BASE_CSS = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:100%; height:100%; overflow:hidden; }}
body {{
  font-family:"Avenir Next","Helvetica Neue",sans-serif;
  background:linear-gradient(126deg,#0e2540 0%,{NAVY} 42%,#0a1727 100%);
  color:{INK}; position:relative;
}}
.glow {{ position:absolute; inset:0;
  background:radial-gradient(900px 500px at 82% 30%, rgba(232,163,61,.10), transparent 65%); }}
.ripples {{ position:absolute; top:0; right:0; height:100%; }}
.mono {{ font-family:"SF Mono",Menlo,monospace; }}
.chips {{ display:flex; gap:14px; }}
.chip {{ border:1.5px solid {LINE}; background:rgba(10,21,32,.55); color:{MUTED};
  border-radius:999px; padding:9px 20px; font-size:21px; font-weight:500; letter-spacing:.2px; }}
.chip b {{ color:{INK}; font-weight:600; }}
.term {{ background:{BG_DEEP}; border:1.5px solid {LINE}; border-radius:12px;
  padding:16px 22px; font-size:21px; line-height:1.5; color:#d7e3ee; display:inline-block; }}
.term .p {{ color:{GREEN}; }} .term .c {{ color:{STEEL}; }}
.domain {{ color:{MUTED}; font-size:22px; font-weight:500; letter-spacing:.4px; }}
.domain b {{ color:{AMBER}; font-weight:600; }}
"""

def page(w, h, body, extra_css=""):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}{extra_css}'
            f'body{{width:{w}px;height:{h}px;}}</style></head><body>'
            f'<div class="glow"></div>{body}</body></html>')

def lockup(mark_px, text_px, gap=None):
    gap = gap or int(mark_px * 0.30)
    return (f'<div style="display:flex;align-items:center;gap:{gap}px;">{mark_svg(mark_px)}'
            f'<div style="display:flex;align-items:center;padding-top:{int(text_px*0.04)}px;">'
            f'{wordmark_svg(text_px)}</div></div>')

pages = {}
sizes = {}

TAGLINE = "Open-source tools that keep Jenkins, GitLab and their build hosts current."
PRODUCTS_LINE = ("Agent8 · Extended Security for Jenkins 2.541.x · Upgrade matrix · AIX Runner"
                 f"&nbsp;&nbsp;—&nbsp;&nbsp;<span style=\"color:{AMBER};\">keelinfra.io</span>")

def add(name, w, h, body):
    pages[name] = page(w, h, body)
    sizes[name] = (w, h)

def chips(items):
    return '<div class="chips">' + "".join(f'<div class="chip">{c}</div>' for c in items) + "</div>"

# ---------- 1. GitHub social preview — org / generic (1280x640) ----------
add("social-preview", 1280, 640, f"""
<svg class="ripples" width="620" height="640" viewBox="0 0 620 640">{keel_ripples(640, x0=330)}</svg>
<div style="position:absolute; inset:0; padding:72px 80px; display:flex; flex-direction:column;">
  {lockup(96, 74)}
  <div style="margin-top:58px; font-size:54px; font-weight:600; line-height:1.22; max-width:1000px;">
    Open-source tools that keep Jenkins,<br>GitLab and their build hosts current.
  </div>
  <div style="margin-top:40px;">{chips([
    "<b>Agent8</b> for Jenkins",
    "<b>Extended Security</b> 2.541.x",
    "<b>Upgrade</b> matrix",
    "<b>AIX Runner</b> for GitLab"])}</div>
  <div style="margin-top:auto; display:flex; align-items:flex-end; justify-content:space-between;">
    <div class="domain">Open source · tested in public</div>
    <div class="domain"><b>keelinfra</b>.io</div>
  </div>
</div>""")

# ---------- 2. GitHub social previews — one per product repo (1280x640) ----------
# Upload each to github.com/keelinfra/<repo> → Settings → Social preview.
# Keep claims durable: no version numbers or counts that change with each run.
PRODUCTS = [
    dict(repo="agent8",
         headline="Jenkins agents for build hosts<br>stuck on Java 8, 11 or 17.",
         sub="The controller moves to Java 21. AIX, Solaris, <span style=\"white-space:nowrap\">HP-UX</span> and older Linux hosts keep their Java.",
         chips=["<b>Java</b> 8 · 11 · 17", "<b>Checksum</b>-verified install",
                "<b>Ansible</b> for fleets", "<b>MIT</b>"],
         note="Open source · tested in public CI",
         url="<b>keelinfra</b>.io/jenkins"),
    dict(repo="jenkins-extended-security",
         headline="Jenkins core security fixes<br>for 2.541.x on Java 17.",
         sub="Backports for the last LTS that runs on Java 17, for the time until you can move to Java 21.",
         chips=["<b>Core</b>, Remoting, Stapler", "<b>Reproducible</b> WAR",
                "<b>SBOM</b> &amp; attestation", "<b>MIT</b>"],
         note="Unofficial · not a Jenkins project release",
         url="github.com/<b>keelinfra</b>"),
    dict(repo="aix-runner",
         headline="GitLab Runner for<br>AIX 7.2 and 7.3.",
         sub="Built from the unmodified upstream release, with four small dependency patches. ppc64.",
         chips=["<b>Upstream</b> runner", "<b>Shell</b> executor", "<b>Experimental</b>", "<b>MIT</b>"],
         note="Unofficial · not affiliated with GitLab Inc.",
         url="github.com/<b>keelinfra</b>"),
    dict(repo="jenkins-upgrade-check",
         headline="Tested upgrade paths<br>for old Jenkins controllers.",
         sub="Every LTS line since 2.60.3, upgraded in rehearsal with the most installed plugins: what broke, and the stops that work.",
         chips=["<b>Upgrade</b> matrix", "<b>Planned</b> stops",
                "<b>Rehearse</b> your own plugins", "<b>Apache-2.0</b>"],
         note="Open source · tested in public CI",
         url="<b>keelinfra</b>.io/jenkins/upgrade-matrix"),
    dict(repo="release-ledger",
         headline="EU Cyber Resilience Act evidence,<br>recorded by your release pipeline.",
         sub="An SBOM and signed provenance for every release, and a daily check of every supported version for exploited vulnerabilities.",
         chips=["<b>GitHub</b> Action", "<b>SBOM</b> per release",
                "<b>Exploited-vuln</b> alerts", "<b>Apache-2.0</b>"],
         note="Open source",
         url="<b>keelinfra</b>.io/cra"),
    dict(repo="release-integrity",
         headline="Could someone swap the files<br>in a GitHub release?",
         sub="A monthly scan of popular Go and Rust CLI releases: immutable releases, provenance, signatures, checksums.",
         chips=["<b>Monthly</b> scan", "<b>Open</b> data, CC BY 4.0", "<b>Apache-2.0</b>"],
         note="Open source · open data",
         url="github.com/<b>keelinfra</b>"),
]

for p in PRODUCTS:
    add(f"social-preview-{p['repo']}", 1280, 640, f"""
<svg class="ripples" width="620" height="640" viewBox="0 0 620 640">{keel_ripples(640, x0=330)}</svg>
<div style="position:absolute; inset:0; padding:68px 80px; display:flex; flex-direction:column;">
  <div style="display:flex;align-items:center;gap:22px;">{mark_svg(72)}
    <div style="display:flex;align-items:center;gap:14px;padding-top:4px;">{wordmark_svg(44)}
      <span style="color:{MUTED};font-size:46px;font-weight:400;margin-top:-6px;">/</span>
      <span style="color:{AMBER};font-size:42px;font-weight:600;letter-spacing:.3px;">{p['repo']}</span>
    </div>
  </div>
  <div style="margin-top:52px; font-size:58px; font-weight:600; line-height:1.18;">{p['headline']}</div>
  <div style="margin-top:22px; font-size:27px; font-weight:500; color:{MUTED}; line-height:1.45; max-width:1040px; text-wrap:balance;">{p['sub']}</div>
  <div style="margin-top:34px;">{chips(p['chips'])}</div>
  <div style="margin-top:auto; display:flex; align-items:flex-end; justify-content:space-between;">
    <div class="domain">{p['note']}</div>
    <div class="domain">{p['url']}</div>
  </div>
</div>""")

# ---------- 3. X / Twitter header (1500x500) ----------
add("banner-x", 1500, 500, f"""
<svg class="ripples" width="560" height="500" viewBox="0 0 560 500">{keel_ripples(500, x0=300)}</svg>
<div style="position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding-bottom:8px;">
  {lockup(110, 86)}
  <div style="margin-top:38px; font-size:34px; font-weight:500; color:{INK}; letter-spacing:.2px;">
    {TAGLINE}
  </div>
  <div style="margin-top:20px; font-size:24px; color:{MUTED}; font-weight:500;">
    {PRODUCTS_LINE}
  </div>
</div>""")

# ---------- 4. LinkedIn personal cover (1584x396) ----------
add("banner-linkedin", 1584, 396, f"""
<svg class="ripples" width="520" height="396" viewBox="0 0 520 396">{keel_ripples(396, x0=280)}</svg>
<div style="position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding-left:210px; padding-bottom:30px;">
  {lockup(92, 72)}
  <div style="margin-top:30px; font-size:29px; font-weight:500;">
    {TAGLINE}
  </div>
  <div style="margin-top:14px; font-size:22px; color:{MUTED}; font-weight:500;">
    {PRODUCTS_LINE}
  </div>
</div>""")

# ---------- 5. LinkedIn company cover (1128x191) ----------
add("banner-linkedin-company", 1128, 191, f"""
<svg class="ripples" width="330" height="191" viewBox="0 0 330 191">{keel_ripples(191, n=4, x0=180)}</svg>
<div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; gap:34px; padding-left:60px;">
  {lockup(64, 50)}
  <div style="width:1.5px; height:64px; background:{LINE};"></div>
  <div style="font-size:20px; color:{MUTED}; font-weight:500; line-height:1.5;">
    Open-source tools that keep Jenkins, GitLab<br>and their build hosts current.
    &nbsp;—&nbsp; <span style="color:{AMBER};">keelinfra.io</span>
  </div>
</div>""")

os.makedirs(SRC, exist_ok=True)
for name, html in pages.items():
    with open(os.path.join(SRC, f"{name}.html"), "w") as f:
        f.write(html)
    print("wrote", name + ".html")

with open(os.path.join(BRAND, "sizes.json"), "w") as f:
    json.dump(sizes, f)
