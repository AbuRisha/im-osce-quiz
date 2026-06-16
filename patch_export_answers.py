"""
Add 'Export My Answers' control to index.html.

Adds a button (in the top .ctrls row) that, when clicked:
  - Collects every <textarea> answer in both IM (c1..c27) and Peds (pc1..pc39)
  - Builds a Markdown dump grouped by subject + case + question
  - Copies to clipboard AND offers .txt download
  - Reads each case <h2> for the case title and each .qlabel for the question text
  - Skips empty answers (option: include all w/ "(blank)")
Idempotent: detects 'data-export-answers' marker and skips re-injection.
"""
from pathlib import Path

INDEX = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\index.html")
MARKER = 'data-export-answers="1"'

EXPORT_BTN = (
    '<button data-export-answers="1" onclick="exportAllAnswers()" '
    'style="background:#0e7490;color:#cffafe">Export My Answers</button>'
)

EXPORT_JS = """
<script>
(function(){
  function collectAnswers(){
    var out=[];
    // Two subject sections: IM = #sec-im, Peds = #sec-ped (or scan all .cc)
    document.querySelectorAll('section.subject-section').forEach(function(sec){
      var subject = sec.id === 'sec-im' ? 'Internal Medicine' :
                    sec.id === 'sec-ped' ? 'Pediatrics' :
                    (sec.id||'Section');
      var cases = sec.querySelectorAll('.cc');
      if(!cases.length) return;
      out.push('## '+subject);
      cases.forEach(function(cc){
        var h2 = cc.querySelector('h2');
        var title = h2 ? (h2.textContent||'').replace(/\\s+/g,' ').trim() : (cc.id||'Case');
        // strip score badge text (look like '4/5' or '100%')
        title = title.replace(/\\s*\\d+(\\.\\d+)?\\s*\\/\\s*\\d+\\s*$/,'').replace(/\\s*\\d+%\\s*$/,'').trim();
        var rows=[];
        cc.querySelectorAll('.qblock').forEach(function(qb){
          var lbl = qb.querySelector('.qlabel');
          var ta  = qb.querySelector('textarea');
          if(!ta) return;
          var qtext = lbl ? (lbl.textContent||'').replace(/\\s+/g,' ').trim() : (ta.id||'Q');
          var ans = (ta.value||'').trim();
          rows.push({q:qtext, a:ans, id:ta.id});
        });
        // Only emit the case if it has at least one non-empty answer
        var hasAny = rows.some(function(r){return r.a.length>0;});
        if(!hasAny) return;
        out.push('\\n### '+title);
        rows.forEach(function(r){
          if(r.a.length===0){
            out.push('- **'+r.q+'**\\n  _(blank)_');
          } else {
            out.push('- **'+r.q+'**\\n  '+r.a.replace(/\\r?\\n/g,'\\n  '));
          }
        });
      });
    });
    if(out.length===0) return '# OSCE Answers Export\\n\\n_(no answers typed yet)_';
    var when=new Date().toISOString().replace('T',' ').slice(0,19)+' UTC';
    return '# OSCE Answers Export\\n_Captured: '+when+'_\\n\\n'+out.join('\\n');
  }

  async function copyText(text){
    if(navigator.clipboard && window.isSecureContext){
      try{ await navigator.clipboard.writeText(text); return true; }catch(e){}
    }
    // Fallback: hidden textarea + execCommand
    var ta=document.createElement('textarea');
    ta.value=text; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    var ok=false; try{ ok=document.execCommand('copy'); }catch(e){}
    document.body.removeChild(ta);
    return ok;
  }

  function downloadTxt(text){
    var blob=new Blob([text],{type:'text/markdown;charset=utf-8'});
    var url=URL.createObjectURL(blob);
    var a=document.createElement('a');
    a.href=url;
    a.download='osce_answers_'+new Date().toISOString().replace(/[:T]/g,'-').slice(0,19)+'.md';
    document.body.appendChild(a); a.click();
    setTimeout(function(){URL.revokeObjectURL(url); a.remove();}, 100);
  }

  function showModal(text, copied){
    var prior=document.getElementById('export-modal');
    if(prior) prior.remove();
    var m=document.createElement('div');
    m.id='export-modal';
    m.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:10000;display:flex;align-items:center;justify-content:center;padding:24px';
    var lines=text.split('\\n').length;
    m.innerHTML=
      '<div style="background:#0f172a;color:#e2e8f0;border-radius:10px;max-width:900px;width:100%;max-height:88vh;display:flex;flex-direction:column;border:1px solid #334155;box-shadow:0 20px 60px rgba(0,0,0,.6)">'+
      '<div style="padding:14px 18px;border-bottom:1px solid #334155;display:flex;align-items:center;gap:12px">'+
        '<strong style="font-size:16px">Exported '+lines+' lines</strong>'+
        '<span style="color:'+(copied?'#22c55e':'#fca5a5')+';font-size:13px">'+(copied?'\u2713 Copied to clipboard':'\u26a0 Auto-copy blocked \u2014 manually select + copy below')+'</span>'+
        '<span style="flex:1"></span>'+
        '<button id="export-modal-dl" style="background:#0e7490;color:#cffafe;border:0;padding:7px 14px;border-radius:6px;cursor:pointer;font-weight:600">Download .md</button>'+
        '<button id="export-modal-recopy" style="background:#334155;color:#e2e8f0;border:0;padding:7px 14px;border-radius:6px;cursor:pointer;font-weight:600">Copy again</button>'+
        '<button id="export-modal-close" style="background:#7f1d1d;color:#fca5a5;border:0;padding:7px 14px;border-radius:6px;cursor:pointer;font-weight:600">Close</button>'+
      '</div>'+
      '<textarea id="export-modal-text" readonly style="flex:1;width:100%;background:#020617;color:#e2e8f0;border:0;padding:14px 18px;font:13px/1.55 ui-monospace,Menlo,Consolas,monospace;resize:none"></textarea>'+
      '</div>';
    document.body.appendChild(m);
    var taEl=document.getElementById('export-modal-text');
    taEl.value=text;
    setTimeout(function(){taEl.focus(); taEl.select();},50);
    document.getElementById('export-modal-dl').onclick=function(){downloadTxt(text);};
    document.getElementById('export-modal-recopy').onclick=async function(){
      var ok=await copyText(text);
      this.textContent= ok ? '\u2713 Copied' : 'Copy failed';
      var btn=this; setTimeout(function(){btn.textContent='Copy again';}, 1500);
    };
    document.getElementById('export-modal-close').onclick=function(){m.remove();};
    m.addEventListener('click',function(e){if(e.target===m) m.remove();});
    document.addEventListener('keydown',function escClose(e){
      if(e.key==='Escape'){var x=document.getElementById('export-modal'); if(x){x.remove(); document.removeEventListener('keydown',escClose);}}
    });
  }

  window.exportAllAnswers=async function(){
    var text=collectAnswers();
    var copied=await copyText(text);
    showModal(text, copied);
  };
})();
</script>
"""


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")

    # Button: inject only if our marker is missing
    if MARKER in html:
        print("[skip-btn] export button already present")
    else:
        needle = '<button onclick="resetAll()" style="background:#7f1d1d;color:#fca5a5">Reset All</button>'
        if needle not in html:
            print("[!] could not find Reset All button to anchor on")
            return 1
        html = html.replace(needle, needle + "\n" + EXPORT_BTN, 1)
        print("[btn] inserted Export My Answers button after Reset All")

    # JS: inject only if window.exportAllAnswers definition is missing
    if "window.exportAllAnswers" not in html:
        if "</body>" in html:
            html = html.replace("</body>", EXPORT_JS + "\n</body>", 1)
            print("[js]  injected exportAllAnswers before </body>")
        else:
            html += EXPORT_JS
            print("[js]  appended exportAllAnswers at EOF (no </body>)")

    INDEX.write_text(html, encoding="utf-8")
    print(f"[ok]  index.html now {len(html):,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
