"""Step 2: version histories from ClinicalTrials.gov for the study's trials.

For each NCT in data/trials_universe.csv:
  1. /api/int/studies/{NCT}?history=true  -> list of versions (number, QC date, status, modules changed)
  2. /api/int/studies/{NCT}/history/{v}   -> the record as it stood at version v, for
     - the last version dated before 2014-12-01 (the baseline), and
     - every later version (dated up to 2026-08-26) whose changed modules include "Study Status" or "Study Design"
       (primary completion date and overall status live in Study Status, enrollment in
       Study Design; a version that changes neither leaves them as they were).

The site's internal endpoints answer once the client holds the ordinary ncbi_sid session
cookie that any public ClinicalTrials.gov response sets; requests.Session keeps it. The
project User-Agent is sent; nothing is impersonated. Each process sends one request
every PAUSE (1.035) seconds; at most three shards run at once, so the total stays at or below
2.9 requests a second, under the 3-a-second cap set for this test.
On 403/429/5xx the script refreshes the session and backs off (1, 2, 4 ... up to 15 minutes);
after 8 failures in a row it stops so it can be resumed later.

Raw responses are stored gzipped in cache/hist_list/ and cache/hist_ver/. Only the fields
this test needs are extracted, to cache/versions_<shard>.jsonl (one line per fetched version).
Resumable: anything already cached is skipped.

Run: python3 i4_hist.py <shard> <n_shards> [seconds]   (e.g. 0 3, 1 3, 2 3 in parallel)
"""
import gzip, json, sys, time
from pathlib import Path
import pandas as pd, requests

HERE = Path(__file__).resolve().parent
LIST = HERE / "cache" / "hist_list"; LIST.mkdir(parents=True, exist_ok=True)
VER = HERE / "cache" / "hist_ver"; VER.mkdir(parents=True, exist_ok=True)
UA = "Claude Space research dspinjr@gmail.com"
BASE = "https://clinicaltrials.gov"
PAUSE = 1.035
BASELINE_BEFORE = "2014-12-01"
LAST_VERSION_DATE = "2026-08-26"   # later versions cannot be posted in time for a 20-day window
KEEP_MODULES = {"Study Status", "Study Design"}


class Client:
    def __init__(self):
        self.s = None; self.fails = 0; self.n = 0; self.last = 0.0
        self.new_session()

    def new_session(self):
        self.s = requests.Session(); self.s.headers["User-Agent"] = UA
        self._get(f"{BASE}/api/v2/version")

    def _get(self, url):
        wait = PAUSE - (time.time() - self.last)
        if wait > 0: time.sleep(wait)
        self.last = time.time(); self.n += 1
        return self.s.get(url, timeout=90)

    def get_json(self, url):
        while True:
            try:
                r = self._get(url)
                code = r.status_code
            except requests.RequestException:
                code = -1
            if code == 200:
                self.fails = 0
                return r.content
            if code == 404:
                return None
            self.fails += 1
            if self.fails >= 8:
                raise SystemExit(f"stopping: {self.fails} failures in a row (last HTTP {code}) at {url}")
            back = min(60 * 2 ** (self.fails - 1), 900)
            print(f"  HTTP {code}; backing off {back}s", flush=True)
            time.sleep(back)
            self.new_session()


def extract(nct, v, j):
    p = j["study"]["protocolSection"]
    st = p.get("statusModule", {}); d = p.get("designModule", {})
    e = d.get("enrollmentInfo", {})
    return {"nct": nct, "v": v,
            "status": st.get("overallStatus"),
            "pcd": st.get("primaryCompletionDateStruct", {}).get("date"),
            "pcd_type": st.get("primaryCompletionDateStruct", {}).get("type"),
            "enroll": e.get("count"), "enroll_type": e.get("type"),
            "why_stopped": st.get("whyStopped"),
            "last_update_submit": st.get("lastUpdateSubmitDate"),
            "last_update_post": st.get("lastUpdatePostDateStruct", {}).get("date"),
            "phases": "|".join(d.get("phases", []) or []),
            "lead_sponsor": p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name")}


def main():
    shard, nsh = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 1)
    budget = float(sys.argv[3]) if len(sys.argv) > 3 else float("inf")   # seconds, then stop cleanly
    ncts = pd.read_csv(HERE / "data" / "trials_universe.csv", dtype=str).nct.tolist()
    ncts = [n for i, n in enumerate(ncts) if i % nsh == shard]
    done_v = set()
    for fp in (HERE / "cache").glob("versions*.jsonl"):
        for line in open(fp):
            r = json.loads(line); done_v.add((r["nct"], r["v"]))
    out_path = HERE / "cache" / f"versions_{shard}.jsonl"
    out = open(out_path, "a")
    complete = set()
    for fp in (HERE / "cache").glob("complete_*.txt"):
        complete |= set(fp.read_text().split())
    comp_out = open(HERE / "cache" / f"complete_{shard}.txt", "a")
    c = Client(); t0 = time.time()
    for i, nct in enumerate(ncts):
        if nct in complete: continue
        if time.time() - t0 > budget:
            print(f"time budget reached after {i} trials, {c.n} requests", flush=True); break
        f = LIST / f"{nct}.json.gz"
        if f.exists():
            raw = gzip.decompress(f.read_bytes())
        else:
            raw = c.get_json(f"{BASE}/api/int/studies/{nct}?history=true")
            if raw is None: continue
            f.write_bytes(gzip.compress(raw))
        changes = json.loads(raw).get("history", {}).get("changes", [])
        if not changes: continue
        before = [ch for ch in changes if ch["date"] < BASELINE_BEFORE]
        need = set()
        if before: need.add(before[-1]["version"])
        for ch in changes:
            if (BASELINE_BEFORE <= ch["date"] <= LAST_VERSION_DATE
                    and (ch["version"] == 0 or KEEP_MODULES & set(ch.get("moduleLabels", [])))):
                need.add(ch["version"])
        for v in sorted(need):
            if (nct, v) in done_v: continue
            vf = VER / f"{nct}_{v}.json.gz"
            if vf.exists():
                vraw = gzip.decompress(vf.read_bytes())
            else:
                vraw = c.get_json(f"{BASE}/api/int/studies/{nct}/history/{v}")
                if vraw is None: continue
                vf.write_bytes(gzip.compress(vraw))
            out.write(json.dumps(extract(nct, v, json.loads(vraw))) + "\n"); done_v.add((nct, v))
        out.flush()
        comp_out.write(nct + "\n"); comp_out.flush()
        if i % 25 == 0:
            el = time.time() - t0
            print(f"{i+1}/{len(ncts)} trials, {c.n} requests, {el/60:.1f} min", flush=True)
    print("done", c.n, "requests")


if __name__ == "__main__":
    main()
