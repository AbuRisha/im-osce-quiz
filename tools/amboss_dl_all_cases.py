"""
Walk AMBOSS for all 38 pediatrics cases + standalone, harvest Media tiles,
download to img/peds/pedN/, set primary as img/pedN.png.

Strategy:
  - Reuse existing amboss_state.json session
  - For each case, GET https://next.amboss.com/us/search?v=media&q=<term>
  - Scrape all <img> tiles in the Media grid, keep clinically-relevant ones
    (skip logos/avatars/promotional banners)
  - Resolve thumb URLs to full-res via the media-us.amboss.com pattern
  - Download up to 5 tiles per case (illustrations + clinical photos)
  - Save manifest.json per case folder
"""
from pathlib import Path
import json
import time
from playwright.sync_api import sync_playwright

STATE = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\amboss_state.json")
REPO_IMG = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\img")
LOG_PATH = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\amboss_dl_log.json")

# Case map: (case_num, topic, primary_search_term, fallback_terms_csv)
CASES = [
    (2,  "Down syndrome",                "Down syndrome",                  "trisomy 21"),
    (3,  "Preseptal cellulitis",         "preseptal cellulitis",           "periorbital cellulitis"),
    (4,  "Respiratory distress syndrome","neonatal respiratory distress syndrome", "hyaline membrane disease"),
    (5,  "Acute lymphoblastic leukemia", "acute lymphoblastic leukemia",   "ALL childhood"),
    (6,  "Sickle cell disease",          "sickle cell disease",            "sickle cell anemia"),
    (7,  "Acute chest syndrome",         "acute chest syndrome",           "sickle cell chest"),
    (8,  "Beta thalassemia major",       "beta thalassemia major",         "cooley anemia"),
    (9,  "Iron deficiency anemia",       "iron deficiency anemia",         "microcytic anemia child"),
    (10, "Nephrotic syndrome",           "nephrotic syndrome",             "minimal change disease"),
    (11, "Meningococcemia",              "meningococcemia",                "meningococcal sepsis"),
    (12, "Henoch-Schonlein purpura",     "henoch-schonlein purpura",       "IgA vasculitis"),
    (13, "Varicella",                    "varicella",                      "chickenpox"),
    (14, "Measles",                      "measles",                        "rubeola"),
    (15, "Roseola",                      "roseola infantum",               "exanthem subitum"),
    (16, "Hand foot mouth disease",      "hand foot and mouth disease",    "coxsackievirus rash"),
    (17, "Scarlet fever",                "scarlet fever",                  "streptococcal scarlatina"),
    (18, "Kawasaki disease",             "kawasaki disease",               "mucocutaneous lymph node"),
    (19, "Mongolian spot",               "mongolian spot",                 "congenital dermal melanocytosis"),
    (20, "Lobar pneumonia",              "lobar pneumonia",                "pneumococcal pneumonia child"),
    (21, "Foreign body aspiration",      "foreign body aspiration",        "airway foreign body"),
    (22, "Cystic fibrosis",              "cystic fibrosis",                "CF lung disease"),
    (23, "Bacterial meningitis",         "bacterial meningitis",           "meningococcal meningitis"),
    (24, "Tetralogy of Fallot",          "tetralogy of fallot",            "tet spell"),
    (25, "Neonatal jaundice ABO",        "neonatal jaundice",              "ABO incompatibility hemolytic"),
    (26, "Biliary atresia",              "biliary atresia",                "kasai procedure"),
    (27, "Congenital diaphragmatic hernia","congenital diaphragmatic hernia","CDH bochdalek"),
    (28, "Duodenal atresia",             "duodenal atresia",               "double bubble sign"),
    (29, "Duchenne muscular dystrophy",  "duchenne muscular dystrophy",    "DMD gowers"),
    (30, "Becker muscular dystrophy",    "becker muscular dystrophy",      "BMD dystrophinopathy"),
    (31, "Myelomeningocele",             "myelomeningocele",               "spina bifida cystica"),
    (32, "Hydrocephalus",                "hydrocephalus",                  "ventriculomegaly child"),
    (33, "Cerebral palsy",               "cerebral palsy",                 "spastic diplegia"),
    (34, "Sturge-Weber syndrome",        "sturge-weber syndrome",          "port wine stain"),
    (35, "Rickets",                      "rickets",                        "vitamin D deficiency child"),
    (36, "Turner syndrome",              "turner syndrome",                "monosomy X"),
    (37, "Marfan syndrome",              "marfan syndrome",                "fibrillin-1"),
    (38, "Pyelonephritis",               "pyelonephritis child",           "acute pyelonephritis pediatric"),
    (39, "Meningococcal vs viral rash",  "petechial rash child",           "non-blanching rash differential"),
]


def scrape_media(page, term: str) -> list[dict]:
    """Search AMBOSS Media for term, return list of tile dicts."""
    url = f"https://next.amboss.com/us/search?v=media&q={term.replace(' ', '+')}"
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    try:
        page.wait_for_function("document.querySelectorAll('img').length > 5", timeout=12000)
    except Exception:
        pass
    page.wait_for_timeout(2000)
    for y in [600, 1500, 2500, 3500, 4500]:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(500)

    tiles = page.evaluate("""
        () => {
          const imgs = Array.from(document.querySelectorAll('img'))
            .filter(i => /media-us\\.amboss\\.com/.test(i.src) && i.naturalWidth >= 80);
          return imgs.map(img => {
            let host = img;
            for (let k=0; k<6; k++) { host = host.parentElement; if (!host) break; }
            const txt = host ? (host.innerText||'').trim().slice(0, 240) : '';
            return {
              src: img.src,
              w: img.naturalWidth, h: img.naturalHeight,
              alt: (img.alt||'').slice(0,200),
              label: txt
            };
          });
        }
    """)
    # Dedupe by src
    seen = set()
    out = []
    for t in tiles:
        if t["src"] in seen:
            continue
        seen.add(t["src"])
        # Skip obvious non-clinical: logos, badges, profile pics
        if any(skip in t["src"].lower() for skip in ("logo", "avatar", "icon")):
            continue
        out.append(t)
    return out


def classify_tile(tile: dict) -> str:
    """Classify by AMBOSS label keyword."""
    lab = tile["label"].upper()
    if "ILLUSTRATION" in lab:
        return "ILLUSTRATION"
    if "PHOTO" in lab:
        return "PHOTO"
    if any(k in lab for k in ("CT", "MRI", "X-RAY", "RADIOGRAPH", "ULTRASOUND", "IMAGING")):
        return "IMAGING"
    return "OTHER"


def pick_top_tiles(tiles: list[dict], limit: int = 5) -> list[dict]:
    """Pick best N tiles: prefer ILLUSTRATION first (anatomy/diagram), then PHOTO + IMAGING."""
    ill = [t for t in tiles if classify_tile(t) == "ILLUSTRATION"]
    photo = [t for t in tiles if classify_tile(t) == "PHOTO"]
    img = [t for t in tiles if classify_tile(t) == "IMAGING"]
    other = [t for t in tiles if classify_tile(t) == "OTHER"]
    ordered = ill[:2] + img[:2] + photo[:3] + other[:2]
    # Dedupe preserving order
    seen = set()
    picked = []
    for t in ordered:
        if t["src"] in seen:
            continue
        seen.add(t["src"])
        picked.append(t)
        if len(picked) >= limit:
            break
    return picked


def main() -> int:
    log = {"started_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "cases": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            storage_state=str(STATE),
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        page = ctx.new_page()
        api = ctx.request

        for case_num, topic, term, fallback in CASES:
            print(f"\n{'='*70}\nCase {case_num}: {topic}\n  term: {term!r}")
            case_dir = REPO_IMG / "peds" / f"ped{case_num}"
            case_dir.mkdir(parents=True, exist_ok=True)

            # Primary search
            tiles = scrape_media(page, term)
            print(f"  primary tiles: {len(tiles)}")
            # Fallback if primary returned few
            if len(tiles) < 2:
                print(f"  fallback term: {fallback!r}")
                tiles_fb = scrape_media(page, fallback)
                # Merge, dedupe
                seen = {t["src"] for t in tiles}
                for t in tiles_fb:
                    if t["src"] not in seen:
                        tiles.append(t)
                        seen.add(t["src"])
                print(f"  total after fallback: {len(tiles)}")

            picked = pick_top_tiles(tiles, limit=5)
            print(f"  picked: {len(picked)}")

            manifest = {
                "case": case_num,
                "topic": topic,
                "search_term": term,
                "fallback_term": fallback,
                "source": "AMBOSS",
                "images": [],
            }

            for idx, tile in enumerate(picked, start=1):
                cls = classify_tile(tile)
                # Normalize to big_ thumbnail URL (AMBOSS already serves big_ in search grid)
                src = tile["src"]
                ext = "jpg" if src.lower().endswith((".jpg", ".jpeg")) else "png"
                fname = f"ped{case_num}_{idx:02d}_{cls.lower()}.{ext}"
                out = case_dir / fname
                try:
                    resp = api.get(src, headers={"Referer": "https://next.amboss.com/"})
                    if resp.status != 200:
                        print(f"  [{idx}] !! skip status={resp.status}")
                        continue
                    body = resp.body()
                    if len(body) < 3000:
                        print(f"  [{idx}] !! skip tiny ({len(body)} bytes)")
                        continue
                    out.write_bytes(body)
                    print(f"  [{idx}] {cls:13s} {tile['w']}x{tile['h']}  {len(body)//1024}KB  -> {fname}")
                    entry = {
                        "type": cls,
                        "filename": fname,
                        "label": tile["label"][:120],
                        "alt": tile["alt"],
                        "source_url": src,
                        "bytes": len(body),
                        "w": tile["w"], "h": tile["h"],
                        "primary": idx == 1,
                    }
                    manifest["images"].append(entry)
                except Exception as e:
                    print(f"  [{idx}] !! {e}")

            # Set primary thumbnail at img/pedN.png (replaces placeholder)
            if manifest["images"]:
                import shutil
                primary = manifest["images"][0]
                src_path = case_dir / primary["filename"]
                dest = REPO_IMG / f"ped{case_num}.png"
                shutil.copyfile(src_path, dest)
                print(f"  primary -> img/ped{case_num}.png")

            (case_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
            log["cases"].append({
                "case": case_num,
                "topic": topic,
                "count": len(manifest["images"]),
                "types": [i["type"] for i in manifest["images"]],
            })

        ctx.close()
        browser.close()

    log["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"\n{'='*70}\n[OK] log -> {LOG_PATH}")
    total = sum(c["count"] for c in log["cases"])
    print(f"[OK] {total} images downloaded across {len(log['cases'])} cases")
    empty = [c for c in log["cases"] if c["count"] == 0]
    if empty:
        print(f"[!] {len(empty)} cases returned 0 images:")
        for c in empty:
            print(f"    case {c['case']}: {c['topic']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
