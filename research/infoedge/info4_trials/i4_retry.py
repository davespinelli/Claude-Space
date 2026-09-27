"""One retry pass over priced-sponsor trials whose history download failed or stopped part way
(cache/retry_nolist.csv, cache/retry_partial.csv). Each URL gets at most 2 tries, 1.1 s apart;
whatever still fails is written to data/history_exclusions.csv instead of being retried again."""
import gzip, json, time
from pathlib import Path
import pandas as pd, requests
import i4_hist as H

HERE = Path(__file__).resolve().parent


def get(s, url):
    for k in range(2):
        time.sleep(1.1)
        try:
            r = s.get(url, timeout=60)
            if r.status_code == 200: return r.content, 200
            if r.status_code == 404: return None, 404
            code = r.status_code
        except requests.RequestException:
            code = -1
    return None, code


def main():
    s = requests.Session(); s.headers["User-Agent"] = H.UA; s.get(f"{H.BASE}/api/v2/version")
    ncts = pd.concat([pd.read_csv(HERE / "cache/retry_nolist.csv"), pd.read_csv(HERE / "cache/retry_partial.csv")]).nct.tolist()
    out = open(HERE / "cache/versions_retry.jsonl", "a"); comp = open(HERE / "cache/complete_retry.txt", "a")
    excl = []
    for nct in ncts:
        f = H.LIST / f"{nct}.json.gz"
        if f.exists(): raw = gzip.decompress(f.read_bytes())
        else:
            raw, code = get(s, f"{H.BASE}/api/int/studies/{nct}?history=true")
            if raw is None: excl.append((nct, "history list", code)); continue
            f.write_bytes(gzip.compress(raw))
        changes = json.loads(raw).get("history", {}).get("changes", [])
        before = [ch for ch in changes if ch["date"] < H.BASELINE_BEFORE]
        need = {before[-1]["version"]} if before else set()
        for ch in changes:
            if (H.BASELINE_BEFORE <= ch["date"] <= H.LAST_VERSION_DATE
                    and (ch["version"] == 0 or H.KEEP_MODULES & set(ch.get("moduleLabels", [])))):
                need.add(ch["version"])
        bad = False
        for v in sorted(need):
            vf = H.VER / f"{nct}_{v}.json.gz"
            if vf.exists(): vraw = gzip.decompress(vf.read_bytes())
            else:
                vraw, code = get(s, f"{H.BASE}/api/int/studies/{nct}/history/{v}")
                if vraw is None: excl.append((nct, f"version {v}", code)); bad = True; continue
                vf.write_bytes(gzip.compress(vraw))
            out.write(json.dumps(H.extract(nct, v, json.loads(vraw))) + "\n")
        out.flush()
        if not bad: comp.write(nct + "\n"); comp.flush()
    pd.DataFrame(excl, columns=["nct", "what", "last_http"]).to_csv(HERE / "data/history_exclusions.csv", index=False)
    print(len(ncts), "retried;", len({e[0] for e in excl}), "still failing")


if __name__ == "__main__":
    main()
