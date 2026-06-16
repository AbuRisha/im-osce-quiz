"""Set pdf_primary=true on the correct image for each case where the PDF
should use a specific (non-default) image.

For each case, we clear any pre-existing pdf_primary flag first, then set
it on the target filename. If the target isn't found, we print a warning."""
import json
import os
from pathlib import Path

BASE = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\img\peds")

# (case_num, manifest_basename, target_filename, reason)
PICKS = [
    (4,  "manifest.json",    "ped4_02_imaging.jpg",      "RDS \u2014 want chest X-ray, not alveolar collapse diagram"),
    (5,  "manifest.json",    "ped5_05_other.jpg",        "ALL \u2014 want B-cell ALL bone marrow microscopy"),
    (6,  "manifest.json",    "ped6_05_other.jpg",        "Sickle cell \u2014 want erythrocyte morphology smear"),
    (22, "manifest.json",    "ped22_04_imaging.jpg",     "CF \u2014 want CT bronchiectasis (NOT rectal prolapse photo)"),
    (24, "manifest.json",    "ped24_03_imaging.jpg",     "TOF \u2014 want boot-shaped heart X-ray"),
    (27, "manifest.json",    "ped27_02_imaging.jpg",     "CDH \u2014 want left-sided CDH X-ray"),
]


def main():
    for case, mf_name, target, reason in PICKS:
        mf_path = BASE / f"ped{case}" / mf_name
        if not mf_path.is_file():
            print(f"[skip] ped{case}: {mf_name} missing")
            continue
        m = json.loads(mf_path.read_text(encoding="utf-8"))
        images = m.get("images") or []
        target_path = BASE / f"ped{case}" / target
        if not target_path.is_file():
            print(f"[!] ped{case}: target file {target} not on disk \u2014 SKIPPING")
            continue
        hit = False
        for img in images:
            if img.get("filename") == target:
                img["pdf_primary"] = True
                hit = True
            else:
                # Clear stale pdf_primary flags so picker resolves cleanly
                img.pop("pdf_primary", None)
        if not hit:
            print(f"[!] ped{case}: '{target}' not in manifest images[] \u2014 SKIPPING")
            continue
        mf_path.write_text(json.dumps(m, indent=2), encoding="utf-8")
        print(f"[ok] ped{case}: pdf_primary={target}  ({reason})")


if __name__ == "__main__":
    main()
