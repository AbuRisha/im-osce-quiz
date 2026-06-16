"""
Inject a Meningococcal-vs-Viral comparison table at the top of Case 39's body.
Idempotent: detects 'data-cmp-table-39' marker.
"""
from pathlib import Path

INDEX = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\index.html")
MARKER = 'data-cmp-table-39="1"'

# Use double-letter HTML entities to dodge encoding mojibake on push
TABLE_CSS = """
/* ---- comparison table (case 39) ---- */
.cmp-wrap{margin:14px 0 18px;border:1px solid #1e293b;border-radius:8px;overflow:hidden;background:#0b1220}
.cmp-wrap h3{margin:0;padding:10px 14px;background:#1e293b;color:#e2e8f0;font-size:15px;border-bottom:1px solid #334155}
.cmp-table{width:100%;border-collapse:collapse;color:#e2e8f0;font-size:13px;line-height:1.55}
.cmp-table th,.cmp-table td{padding:9px 12px;border-bottom:1px solid #1e293b;vertical-align:top;text-align:left}
.cmp-table thead th{background:#0f172a;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:#94a3b8}
.cmp-table tbody th{background:#0f172a;font-weight:600;color:#cbd5e1;width:130px}
.cmp-table td.col-meningo{background:rgba(127,29,29,.18)}
.cmp-table td.col-viral{background:rgba(7,89,133,.18)}
.cmp-table strong.red{color:#fca5a5}
.cmp-table strong.green{color:#86efac}
.cmp-table strong.orange{color:#fdba74}
.cmp-table strong.blue{color:#7dd3fc}
.cmp-pearl{padding:10px 14px;background:rgba(245,158,11,.12);border-top:1px solid #334155;color:#fde68a;font-size:13px}
"""

TABLE_HTML = """<div class="cmp-wrap" data-cmp-table-39="1">
<h3>Meningococcal vs Viral Exanthem &mdash; Side-by-Side</h3>
<table class="cmp-table">
<thead><tr><th></th><th>Meningococcal (sepsis)</th><th>Viral exanthem</th></tr></thead>
<tbody>
<tr><th>Appearance</th>
  <td class="col-meningo"><strong class="red">Petechial &rarr; purpuric / hemorrhagic</strong>, dark purple-red, irregular; may coalesce into ecchymoses (<strong class="red">purpura fulminans</strong>); may start blanching maculopapular early.</td>
  <td class="col-viral">Maculopapular, erythematous, pink/red; may be vesicular (varicella, HFMD); typically discrete.</td></tr>
<tr><th>Blanching</th>
  <td class="col-meningo"><strong class="red">NON-blanching</strong> (key feature &mdash; glass / tumbler test).</td>
  <td class="col-viral">Blanches on pressure.</td></tr>
<tr><th>Systemic</th>
  <td class="col-meningo">Fever, lethargy, <strong class="red">SHOCK</strong> (tachycardia, prolonged CRT, hypotension), neck stiffness, photophobia, vomiting, <strong class="red">&darr; GCS</strong>, leg pain, cold peripheries &mdash; child looks <strong class="red">toxic</strong>.</td>
  <td class="col-viral">Fever, malaise; child often well between febrile peaks; specific clues (cough/coryza/Koplik in measles; conjunctivitis; oral lesions in HFMD).</td></tr>
<tr><th>Mechanism</th>
  <td class="col-meningo"><em><strong class="blue">Neisseria meningitidis</strong></em> endotoxin &rarr; <strong class="red">DIC</strong> &rarr; microthrombi + intravascular hemorrhage (vasculitic).</td>
  <td class="col-viral">Viral cytopathic / immune-complex / direct viral effect on skin.</td></tr>
<tr><th>Investigations</th>
  <td class="col-meningo"><strong class="orange">Do NOT delay antibiotics</strong>. Blood culture, PCR (meningococcal), CBC, coag/<strong class="orange">DIC screen</strong>, lactate, ABG, U&amp;E, CRP, LP (only if no contraindication and after Abx).</td>
  <td class="col-viral">Usually clinical. Targeted serology / PCR if needed (measles IgM, VZV PCR, EBV/CMV).</td></tr>
<tr><th>Management</th>
  <td class="col-meningo"><strong class="green">IMMEDIATE IV/IM benzylpenicillin or ceftriaxone</strong>, IV fluids, ABCDE, PICU, notify public health, <strong class="green">chemoprophylaxis</strong> for close contacts.</td>
  <td class="col-viral">Supportive &mdash; antipyretics, hydration; specific antivirals only in select cases (e.g., <strong class="green">acyclovir</strong> for severe varicella / immunocompromised).</td></tr>
<tr><th>Prognosis</th>
  <td class="col-meningo">Time-critical &mdash; mortality <strong class="orange">10&ndash;15%</strong>; higher with purpura fulminans / shock; survivors may need digit/limb amputation.</td>
  <td class="col-viral">Self-limiting in most; complications uncommon in immunocompetent children.</td></tr>
</tbody>
</table>
<div class="cmp-pearl"><strong>Pearl:</strong> Any <strong class="red">non-blanching rash + fever</strong> in a child = assume meningococcal sepsis until proven otherwise &rarr; <strong class="green">IV/IM antibiotics IMMEDIATELY</strong>, do not wait for investigations.</div>
</div>
"""


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")
    if MARKER in html:
        print("[skip] cmp table for case 39 already present")
        return 0

    anchor = '<div class="st">Not a clinical case \u2014 high-yield comparison topic for the OSCE.</div>'
    if anchor not in html:
        print("[!] case 39 stem anchor not found")
        return 1
    html = html.replace(anchor, anchor + "\n" + TABLE_HTML, 1)
    print("[tbl] injected comparison table at top of Case 39 body")

    # Inject CSS in first <style> block
    if ".cmp-wrap{" not in html:
        if "</style>" in html:
            html = html.replace("</style>", TABLE_CSS + "\n</style>", 1)
            print("[css] injected cmp CSS before first </style>")
        else:
            html = html.replace("<body>", f"<style>{TABLE_CSS}</style>\n<body>", 1)

    INDEX.write_text(html, encoding="utf-8")
    print(f"[ok] index.html now {len(html):,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
