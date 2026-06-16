"""Download Wikimedia images for the PDF primary-image fixes:
- #9  IDA   : peripheral blood smear (microcytic hypochromic)
- #26 BA    : neonatal jaundice (clinical photo)
- #36 Turner: real Turner webbed neck (two options)

Saves into the existing img/peds/pedN/ dirs with _wm_v2_NN naming and adds
a manifest_v2.json (or extends the existing one) with pdf_primary=true on
the new image. The site picker already reads manifest_v2.json so the gallery
gets it for free.
"""
import json
import os
import urllib.request
import socket
from pathlib import Path

socket.setdefaulttimeout(45)
UA = "Mozilla/5.0 (PedsStudyTool/1.0; medical-education)"
BASE = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\img\peds")

# (case, target_filename, url, type, label, attribution, license, set_pdf_primary)
JOBS = [
    (9,  "ped9_wm_01_microscopy.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/2/29/Iron-deficiency_Anemia%2C_Peripheral_Blood_Smear_%284422704616%29.jpg",
     "MICROSCOPY",
     "Iron-deficiency anemia \u2014 peripheral blood smear (microcytic, hypochromic)",
     "Ed Uthman, MD",
     "CC BY 2.0",
     True),
    (26, "ped26_wm_02_photo.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/7/7c/Jaundice_in_newborn.jpg",
     "PHOTO",
     "Jaundice in a newborn (clinical photo)",
     "Wikimedia Commons",
     "Public domain",
     True),
    (36, "ped36_wm_01_photo.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/2/2f/Preoperative_webbed_neck_in_Turner_syndrome.jpg",
     "PHOTO",
     "Turner syndrome \u2014 preoperative webbed neck",
     "Wikimedia Commons contributors",
     "CC BY 4.0",
     True),
    (36, "ped36_wm_02_photo.png",
     "https://upload.wikimedia.org/wikipedia/commons/1/1b/Turner_syndrome_webbed_neck.png",
     "PHOTO",
     "Turner syndrome \u2014 webbed neck (alternative view)",
     "Wikimedia Commons contributors",
     "CC BY 2.0",
     False),
]


def download(url, dst):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read()
    with open(dst, "wb") as f:
        f.write(data)
    return len(data)


def main():
    by_case = {}
    for j in JOBS:
        by_case.setdefault(j[0], []).append(j)

    for case, jobs in by_case.items():
        case_dir = BASE / f"ped{case}"
        case_dir.mkdir(exist_ok=True)
        mf_path = case_dir / "manifest_v2.json"
        if mf_path.exists():
            mf = json.loads(mf_path.read_text(encoding="utf-8"))
            mf.setdefault("images", [])
        else:
            mf = {"case": case, "images": []}

        for case_n, fname, url, typ, label, attr, lic, set_primary in jobs:
            dst = case_dir / fname
            if dst.exists():
                print(f"[skip-dl] ped{case}: {fname} already on disk ({dst.stat().st_size}B)")
            else:
                try:
                    n = download(url, dst)
                    print(f"[ok-dl]   ped{case}: {fname} <- {url}  ({n}B)")
                except Exception as e:
                    print(f"[err-dl]  ped{case}: {fname} {type(e).__name__}: {e}")
                    continue

            # Update manifest entry: dedup by filename, set pdf_primary on chosen one
            existing = next((i for i in mf["images"] if i.get("filename") == fname), None)
            if existing is None:
                entry = {
                    "filename": fname,
                    "type": typ,
                    "label": label,
                    "source": "Wikimedia Commons",
                    "source_url": url,
                    "license": lic,
                    "attribution": attr,
                }
                if set_primary:
                    # Clear any pdf_primary on other entries first
                    for i in mf["images"]:
                        i.pop("pdf_primary", None)
                    entry["pdf_primary"] = True
                mf["images"].append(entry)
            else:
                existing["type"] = typ
                existing["label"] = label
                existing["license"] = lic
                existing["attribution"] = attr
                if set_primary:
                    for i in mf["images"]:
                        i.pop("pdf_primary", None)
                    existing["pdf_primary"] = True

        mf_path.write_text(json.dumps(mf, indent=2), encoding="utf-8")
        print(f"[ok-mf]   ped{case}: wrote {mf_path.name} ({len(mf['images'])} images)\n")

    # Also clear v1 pdf_primary on case 26 so v2 wins (case 26 has only v1's fact sheet)
    p26 = BASE / "ped26" / "manifest.json"
    if p26.exists():
        m = json.loads(p26.read_text(encoding="utf-8"))
        for i in m.get("images", []):
            i.pop("pdf_primary", None)
        p26.write_text(json.dumps(m, indent=2), encoding="utf-8")
        print("[ok-mf]   ped26: cleared v1 pdf_primary")


if __name__ == "__main__":
    main()
