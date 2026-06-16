import urllib.request, urllib.parse, json, sys, socket
socket.setdefaulttimeout(15)
UA = "Mozilla/5.0 (PedsStudyTool/1.0; medical-education)"

QUERIES = [
    ("IDA smear",          "iron deficiency anemia blood smear"),
    ("IDA smear alt",      "microcytic hypochromic anemia peripheral smear"),
    ("Purpura fulminans",  "purpura fulminans"),
    ("Meningococcemia",    "meningococcemia rash"),
    ("Biliary atresia",    "neonatal jaundice biliary atresia"),
    ("Jaundiced infant",   "infant cholestasis jaundice"),
    ("Turner webbed",      "Turner syndrome webbed neck"),
    ("Turner phenotype",   "Turner syndrome phenotype"),
    ("Turner clinical",    "Turner syndrome clinical features"),
]
for tag, q in QUERIES:
    url = ("https://commons.wikimedia.org/w/api.php?action=query&list=search"
           "&srsearch=" + urllib.parse.quote(q) +
           "&srnamespace=6&format=json&srlimit=6")
    print(f"--- {tag}: '{q}' ---", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        r = urllib.request.urlopen(req, timeout=15).read()
        d = json.loads(r)
        for h in d.get("query", {}).get("search", []):
            title = h["title"]
            print(f"  {title}", flush=True)
    except Exception as e:
        print(f"  [err] {type(e).__name__}: {e}", flush=True)
    print(flush=True)
