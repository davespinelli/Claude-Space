"""Step 3: detect the pre-registered registry changes in the fetched version histories.

Compares each fetched version with the previous fetched version of the same trial (versions
that changed neither the Study Status nor the Study Design module cannot change the
primary completion date, enrollment or status, so they are not fetched).
  delay  : primary completion date later by >= 6 months
  cut    : target (estimated) enrollment down to <= 75% of the previous target
  status : overall status moves to SUSPENDED, TERMINATED or WITHDRAWN
Keeps changes posted 2015-01-01 .. 2026-08-26. Output: data/trial_changes.csv, plus
data/post_lag.csv (QC date -> posting date lag for every fetched version).
"""
import gzip, json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
STOP = {"SUSPENDED", "TERMINATED", "WITHDRAWN"}
TARGET = {"ESTIMATED", "ANTICIPATED"}
FIRST, LAST = "2015-01-01", "2026-08-26"


def ym(d):
    if not d or not isinstance(d, str) or len(d) < 7: return None
    y, m = int(d[:4]), int(d[5:7]); day = int(d[8:10]) if len(d) >= 10 else None
    return y, m, day


def delay_6m(old, new):
    a, b = ym(old), ym(new)
    if not a or not b: return False, None
    months = (b[0] * 12 + b[1]) - (a[0] * 12 + a[1])
    if months > 6: return True, months
    if months == 6:
        if a[2] is not None and b[2] is not None and b[2] < a[2]: return False, months
        return True, months
    return False, months


def main():
    V = pd.concat([pd.read_json(fp, lines=True) for fp in sorted((HERE / "cache").glob("versions*.jsonl"))],
                  ignore_index=True).drop_duplicates(["nct", "v"])
    # QC dates from the history lists
    qc = []
    for nct in V.nct.unique():
        f = HERE / "cache" / "hist_list" / f"{nct}.json.gz"
        if not f.exists(): continue
        for ch in json.loads(gzip.decompress(f.read_bytes())).get("history", {}).get("changes", []):
            qc.append((nct, ch["version"], ch["date"], ch.get("status")))
    Q = pd.DataFrame(qc, columns=["nct", "v", "qc_date", "list_status"])
    V = V.merge(Q, on=["nct", "v"], how="left").sort_values(["nct", "v"])
    lag = V.dropna(subset=["qc_date", "last_update_post"]).copy()
    lag["lag_days"] = (pd.to_datetime(lag.last_update_post) - pd.to_datetime(lag.qc_date)).dt.days
    lag[["nct", "v", "qc_date", "last_update_post", "lag_days"]].to_csv(HERE / "data" / "post_lag.csv", index=False)

    rows = []
    for nct, g in V.groupby("nct"):
        g = g.sort_values("v").to_dict("records")
        for prev, cur in zip(g, g[1:]):
            post = cur["last_update_post"] or None
            base = {"nct": nct, "v": cur["v"], "prev_v": prev["v"], "qc_date": cur["qc_date"],
                    "post_date": post, "lead_sponsor": cur["lead_sponsor"], "phases": cur["phases"]}
            if cur["status"] in STOP and prev["status"] != cur["status"]:
                rows.append({**base, "type": "status", "old": prev["status"], "new": cur["status"],
                             "why_stopped": cur.get("why_stopped")})
            ok, months = delay_6m(prev["pcd"], cur["pcd"])
            if ok:
                rows.append({**base, "type": "delay", "old": prev["pcd"], "new": cur["pcd"], "months": months})
            pe, ce = prev["enroll"], cur["enroll"]
            if (prev["enroll_type"] in TARGET and cur["enroll_type"] in TARGET and pd.notna(pe) and pd.notna(ce)
                    and pe > 0 and ce <= 0.75 * pe):
                rows.append({**base, "type": "cut", "old": pe, "new": ce})
    C = pd.DataFrame(rows)
    if len(C):
        C = C[(C.post_date >= FIRST) & (C.post_date <= LAST)]
    C.to_csv(HERE / "data" / "trial_changes.csv", index=False)
    print(len(C), "changes;", C.type.value_counts().to_dict() if len(C) else {})
    print("posting lag (days) quantiles:", lag.lag_days.quantile([.5, .9, .95, .99]).to_dict())


if __name__ == "__main__":
    main()
