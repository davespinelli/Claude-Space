"""Download SEC Financial Statement and Notes data sets (one request per file) into cache/fsn/.
These carry every XBRL fact in each 10-Q/10-K, including the ecd (Item 408) tags that the
companyfacts / frames APIs leave out."""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec

BASE = "https://www.sec.gov/files/dera/data/financial-statement-notes-data-sets/"
FILES = (["2023q2_notes.zip", "2023q3_notes.zip", "2023q4_notes.zip", "2024q1_notes.zip", "2024q2_notes.zip",
          "2024q3_notes.zip", "2024q4_notes.zip", "2025q1_notes.zip", "2025q2_notes.zip"]
         + [f"2025_{m:02d}_notes.zip" for m in range(7, 13)] + [f"2026_{m:02d}_notes.zip" for m in range(1, 9)])
OUT = sec.CACHE / "fsn"


def fetch(name):
    p = OUT / name
    if p.exists():
        return p
    OUT.mkdir(parents=True, exist_ok=True)
    for a in range(6):
        sec._wait()
        try:
            with sec.SESSION.get(BASE + name, stream=True, timeout=120) as r:
                if r.status_code != 200:
                    raise RuntimeError(f"HTTP {r.status_code}")
                tmp = p.with_suffix(".part")
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
                os.replace(tmp, p)
                return p
        except Exception as e:
            print(name, "retry", a, e, flush=True)
            time.sleep(10 * (a + 1))
    raise RuntimeError(name)


if __name__ == "__main__":
    files = sys.argv[1:] or FILES
    for n in files:
        t = time.time()
        p = fetch(n)
        print(n, p.stat().st_size // 1_000_000, "MB", f"{time.time() - t:.0f}s", flush=True)
