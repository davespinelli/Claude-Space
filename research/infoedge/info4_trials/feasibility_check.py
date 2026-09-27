"""INFO-4 feasibility check: can ClinicalTrials.gov record histories be pulled by a script?

Takes a sample of industry-sponsored Phase 2/3 trials from the public v2 API, then asks
for each trial's current record (public v2 API), its version list (internal endpoint
used by the website's "History of Changes" tab) and one past version. The version list is
also requested once with no cookies at all: the internal endpoints answer 403 to a client
that has never received the site's ordinary ncbi_sid session cookie, and 200 once it has
(any public response, such as the v2 API, sets it). Paced at one
request every 3 seconds (it ran alongside the history download), well under the robots.txt
crawl-delay of 1 second. Uses only plain requests with the project User-Agent: no
browser impersonation, no cookie other than the one the site itself sets, no retries
designed to get past a firewall.

Raw responses go to cache/feasibility/ (gitignored); the summary goes to
data/feasibility.json.

Run: python3 research/infoedge/info4_trials/feasibility_check.py
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache" / "feasibility"
OUT = HERE / "data" / "feasibility.json"
UA = "Claude Space research dspinjr@gmail.com"
PAUSE = 3.0
N_TRIALS = 10

BASE = "https://clinicaltrials.gov"


def get(session, url, params=None):
    time.sleep(PAUSE)
    r = session.get(url, params=params, timeout=60)
    return r.status_code, r.headers.get("content-type", ""), r.text


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = UA

    # 1. Universe size and a sample of trials, from the public v2 API.
    flt = ("AREA[LeadSponsorClass]INDUSTRY AND AREA[StudyType]INTERVENTIONAL "
           "AND AREA[StartDate]RANGE[2015-01-01,MAX]")
    counts = {}
    for label, extra in [("industry_interventional_since_2015", ""),
                         ("of_which_phase2_or_3", " AND (AREA[Phase]PHASE2 OR AREA[Phase]PHASE3)")]:
        code, _, body = get(s, f"{BASE}/api/v2/studies",
                            {"filter.advanced": flt + extra, "countTotal": "true",
                             "pageSize": 1, "fields": "NCTId"})
        counts[label] = json.loads(body)["totalCount"] if code == 200 else None

    code, _, body = get(s, f"{BASE}/api/v2/studies",
                        {"filter.advanced": flt + " AND (AREA[Phase]PHASE2 OR AREA[Phase]PHASE3)",
                         "pageSize": N_TRIALS, "fields": "NCTId,LeadSponsorName"})
    (CACHE / "sample.json").write_text(body)
    sample = [(st["protocolSection"]["identificationModule"]["nctId"],
               st["protocolSection"].get("sponsorCollaboratorsModule", {})
                 .get("leadSponsor", {}).get("name"))
              for st in json.loads(body)["studies"]]

    # 2. For each trial: current record, version list, one past version.
    rows = []
    for nct, sponsor in sample:
        row = {"nct": nct, "lead_sponsor": sponsor}
        time.sleep(PAUSE)
        r0 = requests.get(f"{BASE}/api/int/studies/{nct}?history=true", headers={"User-Agent": UA}, timeout=60)
        row["int_history_list_no_cookie"] = r0.status_code
        for key, url in [
            ("v2_current", f"{BASE}/api/v2/studies/{nct}?fields=NCTId,OverallStatus,LastUpdatePostDate"),
            ("int_history_list", f"{BASE}/api/int/studies/{nct}?history=true"),
            ("int_version_1", f"{BASE}/api/int/studies/{nct}/history/1"),
        ]:
            code, ctype, body = get(s, url)
            (CACHE / f"{nct}_{key}.txt").write_text(body)
            row[key] = code
            row[key + "_type"] = ctype.split(";")[0]
        rows.append(row)
        print(nct, row["int_history_list_no_cookie"], row["v2_current"], row["int_history_list"], row["int_version_1"])

    summary = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "user_agent": UA,
        "seconds_between_requests": PAUSE,
        "universe_counts_v2": counts,
        "trials_probed": len(rows),
        "ok_counts": {k: sum(r[k] == 200 for r in rows)
                      for k in ("int_history_list_no_cookie", "v2_current", "int_history_list", "int_version_1")},
        "rows": rows,
    }
    OUT.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary["ok_counts"]), counts)


if __name__ == "__main__":
    main()
