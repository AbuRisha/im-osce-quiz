"""
Wire multi-image galleries into the live index.html.

For each pediatric case (pedN), reads img/peds/pedN/manifest*.json,
builds a primary image + thumbnail strip + click-to-zoom lightbox,
replaces the single <div class="ic"><img src="img/pedN.png"...></div>.

Idempotent: detects 'data-peds-gallery' marker and won't double-patch.
"""
from pathlib import Path
import json
import re
import shutil

ROOT = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz")
INDEX = ROOT / "index.html"
IMG_PEDS = ROOT / "img" / "peds"
BACKUP = ROOT / "index.html.pre_gallery_backup"


def collect_case(n: int):
    """Return ordered list of images for case n, primary first, then supporting."""
    case_dir = IMG_PEDS / f"ped{n}"
    if not case_dir.exists():
        return []
    all_imgs = []
    for mf_name in ("manifest_v2.json", "manifest.json"):
        mf = case_dir / mf_name
        if not mf.exists():
            continue
        m = json.loads(mf.read_text(encoding="utf-8"))
        for i in m.get("images", []):
            # Serialize findings list into a compact JSON for the data attr;
            # lightbox JS will render it as <ul>.
            findings = i.get("findings") or []
            findings_attr = (
                json.dumps(findings, ensure_ascii=False)
                .replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
            ) if findings else ""
            all_imgs.append({
                "path": f"img/peds/ped{n}/{i['filename']}",
                "type": i.get("type", "OTHER"),
                "label": (i.get("label") or "").replace('"', "&quot;").replace("<", "&lt;"),
                "primary": bool(i.get("primary")),
                "findings_attr": findings_attr,
                "has_findings": bool(findings),
            })
    # Dedupe by path
    seen = set()
    deduped = []
    for i in all_imgs:
        if i["path"] in seen:
            continue
        seen.add(i["path"])
        deduped.append(i)
    # Primary first (only re-order the FIRST primary; others stay in place, demoted)
    primary_idx = next((idx for idx, i in enumerate(deduped) if i["primary"]), None)
    if primary_idx is not None and primary_idx != 0:
        primary = deduped.pop(primary_idx)
        deduped.insert(0, primary)
    # Demote all-but-first 'primary' flags so the UI only highlights one
    seen_primary = False
    for i in deduped:
        if i["primary"]:
            if seen_primary:
                i["primary"] = False
            else:
                seen_primary = True
    return deduped


def build_gallery_html(n: int, images: list) -> str:
    if not images:
        # Fallback to the old single-image render
        return (f'<div class="ic" data-peds-gallery="1">'
                f'<img src="img/ped{n}.png" alt="Pediatrics Case {n}" loading="lazy" '
                f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'block\'">'
                f'<div class="img-ph" style="display:none">[Add image as <code>img/ped{n}.png</code>]</div>'
                f'</div>')

    # Thumbnail-only layout: every image is a small thumb, click any to open lightbox.
    parts = [f'<div class="ic peds-gallery" data-peds-gallery="1"><div class="peds-thumbs">']
    for img in images:
        primary_cls = " is-primary" if img.get("primary") else ""
        findings_cls = " has-findings" if img.get("has_findings") else ""
        findings_attr = (
            f' data-findings="{img["findings_attr"]}"' if img.get("findings_attr") else ""
        )
        parts.append(
            f'<img class="peds-thumb tag-{img["type"]}{primary_cls}{findings_cls}" '
            f'src="{img["path"]}" '
            f'alt="Pediatrics Case {n} - {img["type"]}" loading="lazy" '
            f'data-label="{img["label"]}"{findings_attr} '
            f'onclick="pedsLightbox(this)">'
        )
    parts.append('</div></div>')
    return "".join(parts)


GALLERY_CSS = """
/* ---- peds image gallery (thumbnail-only) ---- */
.peds-gallery{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.peds-thumbs{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px}
.peds-thumb{width:130px;height:130px;object-fit:cover;border-radius:6px;cursor:zoom-in;border:2px solid #1e293b;background:#000;transition:transform .12s,border-color .12s,box-shadow .12s}
.peds-thumb:hover{transform:scale(1.08);border-color:#38bdf8;box-shadow:0 6px 20px rgba(56,189,248,.35)}
.peds-thumb.is-primary{border-color:#38bdf8}
.peds-thumb.tag-PHOTO{outline:2px solid rgba(34,197,94,.45);outline-offset:-2px}
.peds-thumb.tag-IMAGING{outline:2px solid rgba(245,158,11,.55);outline-offset:-2px}
.peds-thumb.tag-ILLUSTRATION{outline:2px solid rgba(59,130,246,.45);outline-offset:-2px}
.peds-thumb.tag-OTHER{outline:2px solid rgba(148,163,184,.35);outline-offset:-2px}
.peds-thumb.tag-MICROSCOPY{outline:2px solid rgba(124,58,237,.55);outline-offset:-2px}
.peds-thumb.tag-HISTOLOGY{outline:2px solid rgba(124,58,237,.55);outline-offset:-2px}
/* findings badge: small purple dot on thumbs with annotations */
.peds-thumb.has-findings{position:relative}
.peds-gallery .peds-thumb.has-findings::after{content:""}
.peds-thumb.has-findings{box-shadow:inset 0 -22px 0 rgba(124,58,237,.85);}
/* lightbox */
#peds-lb{position:fixed;inset:0;background:rgba(0,0,0,.94);z-index:9999;display:none;align-items:center;justify-content:center;flex-direction:column;cursor:zoom-out;padding:24px}
#peds-lb.show{display:flex}
#peds-lb img{max-width:96vw;max-height:86vh;border-radius:8px;box-shadow:0 12px 60px rgba(0,0,0,.7)}
#peds-lb .lb-cap{color:#e2e8f0;font:14px/1.5 system-ui,sans-serif;margin-top:14px;max-width:80vw;text-align:center}
#peds-lb .lb-close{position:absolute;top:14px;right:18px;color:#fff;font:600 22px/1 system-ui;background:rgba(255,255,255,.08);border:0;width:40px;height:40px;border-radius:50%;cursor:pointer;z-index:2}
#peds-lb .lb-nav{position:absolute;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.08);border:0;color:#fff;font:600 28px/1 system-ui;width:48px;height:64px;border-radius:8px;cursor:pointer;z-index:2}
#peds-lb .lb-prev{left:18px}
#peds-lb .lb-next{right:18px}
#peds-lb .lb-nav:hover{background:rgba(56,189,248,.3)}
/* findings panel inside lightbox */
#peds-lb .lb-findings{margin-top:12px;max-width:560px;background:#1e1b4b;border:1px solid #4c1d95;border-radius:6px;padding:10px 14px;color:#ede9fe;font:13px/1.5 system-ui,sans-serif;text-align:left;display:none}
#peds-lb .lb-findings.show{display:block}
#peds-lb .lb-findings h4{margin:0 0 6px;font-size:12px;color:#c4b5fd;letter-spacing:.04em;text-transform:uppercase}
#peds-lb .lb-findings ul{margin:0;padding-left:18px}
#peds-lb .lb-findings li{margin:2px 0}
#peds-lb .lb-findings li b{color:#ddd6fe}
#peds-lb .lb-findings li i{color:#a78bfa}
"""

GALLERY_JS = """
<script>
(function(){
  var current=null; // {gallery:Element, idx:Number}
  function ensureLB(){
    var lb=document.getElementById('peds-lb');
    if(lb) return lb;
    lb=document.createElement('div');
    lb.id='peds-lb';
    lb.innerHTML='<button class="lb-close" type="button" aria-label="Close">&times;</button>'+
      '<button class="lb-nav lb-prev" type="button" aria-label="Previous">&#8249;</button>'+
      '<button class="lb-nav lb-next" type="button" aria-label="Next">&#8250;</button>'+
      '<img alt=""><div class="lb-cap"></div>'+
      '<div class="lb-findings"><h4>Findings on this slide</h4><ul></ul></div>';
    lb.onclick=function(e){if(e.target===lb) close();};
    lb.querySelector('.lb-close').onclick=function(e){e.stopPropagation();close();};
    lb.querySelector('.lb-prev').onclick=function(e){e.stopPropagation();step(-1);};
    lb.querySelector('.lb-next').onclick=function(e){e.stopPropagation();step(1);};
    document.body.appendChild(lb);
    document.addEventListener('keydown',function(e){
      if(!lb.classList.contains('show')) return;
      if(e.key==='Escape') close();
      else if(e.key==='ArrowLeft') step(-1);
      else if(e.key==='ArrowRight') step(1);
    });
    return lb;
  }
  function close(){var lb=document.getElementById('peds-lb');if(lb) lb.classList.remove('show'); current=null;}
  function mdInline(s){
    s=String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    s=s.replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>');
    s=s.replace(/(^|[^\w*])\*([^*]+)\*(?![\w*])/g,'$1<i>$2</i>');
    return s;
  }
  function renderFindings(lb,el){
    var panel=lb.querySelector('.lb-findings');
    var ul=panel.querySelector('ul');
    var raw=el.getAttribute('data-findings');
    ul.innerHTML='';
    if(!raw){panel.classList.remove('show');return;}
    var arr;try{arr=JSON.parse(raw);}catch(e){panel.classList.remove('show');return;}
    if(!arr||!arr.length){panel.classList.remove('show');return;}
    arr.forEach(function(f){var li=document.createElement('li');li.innerHTML=mdInline(f);ul.appendChild(li);});
    panel.classList.add('show');
  }
  function show(el){
    var lb=ensureLB();
    lb.querySelector('img').src=el.src;
    lb.querySelector('.lb-cap').textContent=el.getAttribute('data-label')||'';
    renderFindings(lb,el);
    lb.classList.add('show');
    var gallery=el.closest('.peds-gallery');
    var thumbs=gallery? Array.from(gallery.querySelectorAll('.peds-thumb')) : [el];
    var hasMany=thumbs.length>1;
    lb.querySelector('.lb-prev').style.display=hasMany?'block':'none';
    lb.querySelector('.lb-next').style.display=hasMany?'block':'none';
    current={gallery:gallery, thumbs:thumbs, idx:thumbs.indexOf(el)};
  }
  function step(d){
    if(!current||!current.thumbs||current.thumbs.length<2) return;
    var n=current.thumbs.length;
    current.idx=(current.idx+d+n)%n;
    var el=current.thumbs[current.idx];
    var lb=document.getElementById('peds-lb');
    lb.querySelector('img').src=el.src;
    lb.querySelector('.lb-cap').textContent=el.getAttribute('data-label')||'';
    renderFindings(lb,el);
  }
  window.pedsLightbox=show;
})();
</script>
"""


def main():
    html = INDEX.read_text(encoding="utf-8")
    if not BACKUP.exists():
        BACKUP.write_text(html, encoding="utf-8")
        print(f"[backup] -> {BACKUP.name}")

    # Already patched? Re-patch fresh from backup to keep idempotent.
    if 'data-peds-gallery' in html:
        print("[detect] existing gallery markers -> restoring from backup before re-patch")
        html = BACKUP.read_text(encoding="utf-8")

    # Pattern: <div class="ic"><img src="img/pedN.png"...></div>
    # (the div sometimes spans multiple lines? — based on grep it's all single-line)
    pattern = re.compile(
        r'<div class="ic"><img src="img/ped(\d+)\.png"[^>]*onerror[^>]*>'
        r'<div class="img-ph"[^>]*>\[Add image as <code>img/ped\d+\.png</code>\]</div>'
        r'</div>',
        re.IGNORECASE
    )

    replacements = 0
    case_summary = []

    def repl(match):
        nonlocal replacements
        n = int(match.group(1))
        imgs = collect_case(n)
        replacements += 1
        case_summary.append((n, len(imgs)))
        return build_gallery_html(n, imgs)

    new_html = pattern.sub(repl, html)

    if replacements == 0:
        print("[!] no .ic blocks matched - pattern needs adjustment")
        return 1

    # Inject CSS in <style> block. Marker is the actual selector that ONLY appears in our CSS
    # block (not in HTML body), and is reliably present in GALLERY_CSS.
    if "#peds-lb{" not in new_html:
        # Try to inject just before the closing </style> of the main style block
        if "</style>" in new_html:
            new_html = new_html.replace("</style>", GALLERY_CSS + "\n</style>", 1)
            print("[css] injected before first </style>")
        else:
            print("[!] no </style> found, prepending CSS to <body>")
            new_html = new_html.replace("<body>", f"<style>{GALLERY_CSS}</style>\n<body>", 1)

    # Inject JS once before </body>
    if 'function pedsLightbox' not in new_html:
        if "</body>" in new_html:
            new_html = new_html.replace("</body>", GALLERY_JS + "\n</body>", 1)
            print("[js] injected before </body>")
        else:
            new_html += GALLERY_JS
            print("[js] appended at EOF (no </body> found)")

    INDEX.write_text(new_html, encoding="utf-8")

    print(f"\n[ok] patched {replacements} case galleries")
    for n, k in case_summary:
        marker = "" if k > 0 else "  (no manifest images - using primary fallback)"
        print(f"  case {n:2d}: {k} images{marker}")
    print(f"\nsize: {len(html):,} -> {len(new_html):,} bytes (+{len(new_html)-len(html):,})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
