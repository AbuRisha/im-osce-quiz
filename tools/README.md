# tools/ — build & content helpers for the OSCE study system

These scripts build the Pediatrics PDF and scrape clinical images. Site patchers
live in the repo root (`patch_*.py`, `rebuild_site.ps1`) since they edit `index.html`
directly.

## Quick reference

| Script | What it does |
|---|---|
| `peds_pdf_v3.py` | Master PDF generator. Reads `STUDY_GUIDE.md` + `peds_model_answers.py` + per-case manifests → renders HTML → Chrome headless → `Pediatrics_Study_Guide.pdf`. ~68 KB. |
| `peds_model_answers.py` | Dict of all 38 peds cases + standalone topic: model answers + pearls. ~43 KB. |
| `add_histology_findings.py` | Annotates microscopy/histology images in manifests with `findings: [...]` arrays. |
| `amboss_dl_all_cases.py` | Playwright AMBOSS scraper. Uses saved `amboss_state.json` (NOT committed). |
| `search_wikimedia.py` | Wikimedia Commons API search helper (UA header + 15s timeout). |
| `get_commons_urls.py` | Resolves Wikimedia file titles → download URLs. Output: `commons_urls.json`. |
| `download_pdf_image_fixes.py` | One-shot Wikimedia image downloader for specific cases. |
| `purge_grey_turner.py` | Example purge script for removing a wrong-condition AMBOSS scrape. |
| `patch_pdf_primary_flags.py` | Sets `pdf_primary: true` on specific image entries (overrides PDF picker). |

## Standard workflows

### Regen the PDF

```powershell
$env:PYTHONIOENCODING = "utf-8"
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
python tools/peds_pdf_v3.py
Get-Item "$HOME/Downloads/Pediatrics_Study_Guide.pdf" | Select-Object Length, LastWriteTime
```

### Rebuild the site (from repo root, NOT from tools/)

```powershell
./rebuild_site.ps1
```

### Add a new clinical image

1. Scrape: `python tools/amboss_dl_all_cases.py` (or Wikimedia helpers)
2. Visually verify via `python -m http.server 8765 --directory img/peds`
3. (If microscopy) edit `tools/add_histology_findings.py` to add `findings: [...]`
4. Site rebuild: `./rebuild_site.ps1`
5. PDF regen: `python tools/peds_pdf_v3.py`
6. Commit + push

## Hard rules

- **Always kill Chrome before PDF regen** — it locks the open PDF.
- **`$env:PYTHONIOENCODING="utf-8"`** before any script (em-dashes, Greek letters).
- **Never edit `index.html` by hand** — use the patchers from repo root.
- **`amboss_state.json`** is gitignored (auth cookies). Refresh via Playwright + manual login.

## Skills

Claude has these skills available for this system (see `~/.claude/skills/`):

- `nimbus-peds-master` — umbrella index
- `nimbus-peds-pdf-builder` — PDF gen workflow
- `nimbus-peds-site-patcher` — site rebuild flow
- `amboss-media-scraper` — image scraping
- `localhost-image-preview` — chat-inline image preview
- `nimbus-peds-histology-findings` — annotation schema + render flow

Load `nimbus-peds-master` first in any cold-start session.
