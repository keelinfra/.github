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
| `social-preview.png` | 1280×640 | GitHub social preview for org-level / generic repos (`keelinfra/keelinfra.io`, `keelinfra/.github`) · default `og:image` on keelinfra.io |
| `social-preview-agent8.png` | 1280×640 | `keelinfra/agent8` → Settings → Social preview |
| `social-preview-jenkins-extended-security.png` | 1280×640 | `keelinfra/jenkins-extended-security` → Settings → Social preview |
| `social-preview-aix-runner.png` | 1280×640 | `keelinfra/aix-runner` → Settings → Social preview |
| `social-preview-jenkins-upgrade-check.png` | 1280×640 | `keelinfra/jenkins-upgrade-check` → Settings → Social preview |
| `social-preview-release-ledger.png` | 1280×640 | `keelinfra/release-ledger` → Settings → Social preview |
| `social-preview-release-integrity.png` | 1280×640 | `keelinfra/release-integrity` → Settings → Social preview |
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

## README artwork

The heroes and project cards in the org profile and the repository READMEs are SVGs drawn by `src/readme/readme_art.py`, in the keelinfra.io visual language (IBM Plex, navy and amber, the release-lines diagram, the matrix strip). Text is converted to outlines, so they look the same everywhere with no font download; each comes in a light and a dark version for `<picture>`.

| File | Use |
|---|---|
| `readme/profile-hero-{light,dark}.svg` | top of `profile/README.md` |
| `readme/card-<repo>-{light,dark}.svg` | project cards in `profile/README.md` |
| `<repo>/.github/readme/hero-{light,dark}.svg` | top of agent8, jenkins-extended-security and jenkins-upgrade-check READMEs |

The facts in them (current LTS, latest 2.541.x release, CVE count, matrix) are constants at the top of the script, and the matrix strip is drawn from `matrix.json`. After a release or a new matrix, update them and run, with the repositories cloned side by side:

```bash
pip install fonttools brotli uharfbuzz
python3 src/readme/readme_art.py --repos ..   # writes here and into ../<repo>/.github/readme/
```

## Regenerating

Everything is generated from code — no design tool needed:

```bash
cd src && ./build.sh
```

`src/` holds the geometry (`compose_svgs.py`), the banner layouts (`build_banners.py` → HTML masters), and the wordmark outline extractor (`wordmark_paths.py`, requires macOS Avenir Next + fontTools). Banners render through headless Chrome at 2× and downscale to exact platform sizes.
