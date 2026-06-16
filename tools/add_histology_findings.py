"""Add `findings` text to histology/microscopy images in peds manifests.
The PDF + site galleries will render this as bullet points under the image."""
import json
from pathlib import Path

BASE = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\img\peds")

# (case, manifest, filename, findings_bullets_as_list)
JOBS = [
    (4, "manifest.json", "ped4_04_other.jpg", [
        "Pink amorphous **hyaline membranes** lining alveolar walls",
        "Collapsed alveoli (atelectasis)",
        "Type II pneumocyte hyperplasia",
        "Interstitial edema + neutrophilic infiltrate",
    ]),
    (5, "manifest.json", "ped5_05_other.jpg", [
        "Hypercellular marrow replaced by **monomorphic blasts**",
        "High N:C ratio; scant basophilic cytoplasm",
        "Fine open chromatin; inconspicuous nucleoli",
        "**TdT+** on flow (immature lymphoblasts)",
        "CD19/CD10/CD22 positive (B-ALL panel)",
    ]),
    (6, "manifest.json", "ped6_05_other.jpg", [
        "**Sickle cells** (drepanocytes) — crescent/banana-shaped RBCs",
        "**Target cells** (codocytes)",
        "**Howell-Jolly bodies** (autosplenectomy)",
        "Nucleated RBCs + polychromasia (\u2191 reticulocytes)",
        "Anisocytosis + poikilocytosis",
    ]),
    (9, "manifest_v2.json", "ped9_wm_01_microscopy.jpg", [
        "**Microcytic** (small RBCs, MCV <80 fL)",
        "**Hypochromic** — \u2191 central pallor (>1/3 cell diameter)",
        "**Anisopoikilocytosis** (variable size/shape)",
        "**Pencil/cigar cells** (elongated elliptocytes)",
        "**Target cells** may be present",
        "Reactive **thrombocytosis** commonly accompanies",
    ]),
    (23, "manifest.json", "ped23_03_imaging.jpg", [
        "CSF Gram stain in bacterial meningitis:",
        "**Gram-negative diplococci** \u2192 *N. meningitidis*",
        "**Gram-positive diplococci** \u2192 *S. pneumoniae*",
        "**Gram-negative coccobacilli** \u2192 *H. influenzae*",
        "**Gram-positive rods** \u2192 *L. monocytogenes* (neonates/elderly)",
        "Abundant **PMNs** (neutrophil-predominant pleocytosis)",
    ]),
    (29, "manifest.json", "ped29_03_other.jpg", [
        "Muscle biopsy in DMD:",
        "**Variable fiber size** (rounded atrophic + hypertrophic fibers)",
        "**Necrotic fibers** + active **regeneration** (basophilic fibers)",
        "**Endomysial fibrosis** + **fatty infiltration**",
        "**Absent dystrophin** on immunostain (DMD) / reduced or truncated (BMD)",
        "Internal nuclei, opaque/hyaline fibers",
    ]),
    (29, "manifest.json", "ped29_04_other.jpg", [
        "Same DMD biopsy pattern \u2014 see above",
    ]),
    (30, "manifest.json", "ped30_02_other.jpg", [
        "Muscle biopsy in BMD:",
        "Same dystrophinopathy pattern as DMD but **less severe**",
        "**Reduced or truncated dystrophin** (vs absent in DMD) on Western blot / IHC",
        "Variable fiber size, necrosis, regeneration, fibrosis \u2014 milder",
    ]),
]


def main():
    for case, mf_name, fname, findings in JOBS:
        mp = BASE / f"ped{case}" / mf_name
        if not mp.is_file():
            print(f"[skip] ped{case}/{mf_name} missing")
            continue
        m = json.loads(mp.read_text(encoding="utf-8"))
        hit = False
        for img in m.get("images", []):
            if img.get("filename") == fname:
                img["findings"] = findings
                hit = True
        if hit:
            mp.write_text(json.dumps(m, indent=2), encoding="utf-8")
            print(f"[ok] ped{case}/{mf_name} :: {fname} \u2190 {len(findings)} findings")
        else:
            print(f"[!] ped{case}/{mf_name} :: {fname} NOT FOUND in images[]")


if __name__ == "__main__":
    main()
