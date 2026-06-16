"""Resolve Wikimedia Commons File: titles to direct image URLs + license info.
Output JSON for the next step."""
import urllib.request, urllib.parse, json, socket, sys
socket.setdefaulttimeout(15)
UA = "Mozilla/5.0 (PedsStudyTool/1.0; medical-education)"

TITLES = [
    "File:Iron-deficiency Anemia, Peripheral Blood Smear (4422704616).jpg",
    "File:Preoperative webbed neck in Turner syndrome.jpg",
    "File:Turner syndrome webbed neck.png",
    "File:Neonatal jaundice.jpg",
    "File:Jaundice in newborn.jpg",
    "File:Newborn jaundice phototherapy.jpg",
    "File:Purpura fulminans on baby.jpg",
    "File:Meningococcemia.jpg",
]

results = []
for t in TITLES:
    url = ("https://commons.wikimedia.org/w/api.php?action=query&titles=" + urllib.parse.quote(t) +
           "&prop=imageinfo&iiprop=url|size|mime|extmetadata&format=json")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        r = urllib.request.urlopen(req, timeout=15).read()
        d = json.loads(r)
        pages = d.get("query", {}).get("pages", {})
        for pid, p in pages.items():
            if pid == "-1":
                print(f"[miss] {t}", flush=True)
                continue
            ii = p.get("imageinfo", [{}])[0]
            md = ii.get("extmetadata", {})
            lic = (md.get("LicenseShortName") or {}).get("value", "?")
            artist = (md.get("Artist") or {}).get("value", "?")
            print(f"[ok]  {t}", flush=True)
            print(f"       url={ii.get('url')}  ({ii.get('width')}x{ii.get('height')}, {ii.get('size')}B, {ii.get('mime')})", flush=True)
            print(f"       license={lic}", flush=True)
            results.append({
                "title": t, "url": ii.get("url"),
                "width": ii.get("width"), "height": ii.get("height"),
                "size": ii.get("size"), "mime": ii.get("mime"),
                "license": lic, "artist_html": artist,
            })
    except Exception as e:
        print(f"[err] {t}: {type(e).__name__}: {e}", flush=True)

with open(r"C:\Users\erick\AppData\Local\Temp\opencode\commons_urls.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved {len(results)} resolutions to commons_urls.json", flush=True)
