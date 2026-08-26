# keelinfra brand assets

The mark is a **K with a keel line** — the hull curve that keeps a ship stable. Same idea as the product: the structural backbone under your infrastructure.

## Palette

| Token | Hex | Use |
|---|---|---|
| Keel Navy | `#0b2239` | primary surface, logo tile, text on light |
| Beacon Amber | `#e8a33d` | accent, the mark's strokes (`#b06d10` on light bg for contrast) |
| Deep | `#0a1520` | code/terminal surfaces |
| Ink | `#e4ecf3` | text on dark |
| Muted | `#8fa1b3` | secondary text on dark |
| Line | `#22303e` | borders on dark |

Wordmark face: **Avenir Next Demi Bold**, lowercase, converted to outlines (no font dependency in the SVGs).

## Files & where to upload them

| File | Size | Use |
|---|---|---|
| `logo.svg` | vector | master mark (navy tile + amber K) |
| `avatar.png` | 1024×1024 | GitHub org avatar · X profile photo · LinkedIn company logo |
| `logo-mark-navy.svg` / `logo-mark-amber.svg` | vector | bare mark for light / dark surfaces, favicons |
| `wordmark-light.svg` / `wordmark-dark.svg` | vector | horizontal lockup for light / dark backgrounds |
| `social-preview.png` | 1280×640 | GitHub social preview, org-level / generic repos |
| `social-preview-keycloak.png` | 1280×640 | `keelinfra/keycloak` → Settings → Social preview |
| `banner-x.png` | 1500×500 | X / Twitter profile header |
| `banner-linkedin.png` | 1584×396 | LinkedIn personal profile cover |
| `banner-linkedin-company.png` | 1128×191 | LinkedIn company page cover |

## Embedding in a README

Theme-aware wordmark:

```html
<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/wordmark-dark.svg">
  <img alt="keelinfra" width="380"
       src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/wordmark-light.svg">
</picture>
```

## Regenerating

Everything is generated from code — no design tool needed:

```bash
cd src && ./build.sh
```

`src/` holds the geometry (`compose_svgs.py`), the banner layouts (`build_banners.py` → HTML masters), and the wordmark outline extractor (`wordmark_paths.py`, requires macOS Avenir Next + fontTools). Banners render through headless Chrome at 2× and downscale to exact platform sizes.
