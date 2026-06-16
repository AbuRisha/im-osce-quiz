"""Remove the misleading 'Grey Turner sign' photo from case 36.
Grey Turner sign = flank bruising in hemorrhagic pancreatitis, has NOTHING
to do with Turner syndrome. It was scraped because of keyword overlap."""
import json
from pathlib import Path

mp = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\img\peds\ped36\manifest.json")
m = json.loads(mp.read_text(encoding="utf-8"))
before = len(m.get("images", []))
m["images"] = [i for i in m.get("images", []) if i.get("filename") != "ped36_02_photo.jpg"]
for i in m["images"]:
    i.pop("pdf_primary", None)
mp.write_text(json.dumps(m, indent=2), encoding="utf-8")
removed = before - len(m["images"])
print(f"ped36 manifest.json: {before} -> {len(m['images'])} images (removed {removed} Grey Turner entry)")

fp = Path(r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\img\peds\ped36\ped36_02_photo.jpg")
if fp.exists():
    fp.unlink()
    print(f"deleted {fp.name} from disk")
