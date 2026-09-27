"""Step 1a: current records of every industry-sponsored interventional trial updated since 2015.

Public ClinicalTrials.gov v2 API, 1,000 records a page, one request every 1.5 s.
Raw pages -> cache/v2_pages/; flat table -> data/trials_current.csv.
"""
import csv, json, time
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
PAGES = HERE / "cache" / "v2_pages"; PAGES.mkdir(parents=True, exist_ok=True)
UA = "Claude Space research dspinjr@gmail.com"
FIELDS = ("NCTId,LeadSponsorName,LeadSponsorClass,Phase,StudyType,OverallStatus,StartDate,"
          "StudyFirstPostDate,LastUpdatePostDate,PrimaryCompletionDate,EnrollmentCount,"
          "CollaboratorName,OrgFullName")
FILTER = ("AREA[LeadSponsorClass]INDUSTRY AND AREA[StudyType]INTERVENTIONAL "
          "AND AREA[LastUpdatePostDate]RANGE[2015-01-01,MAX]")

def main():
    s = requests.Session(); s.headers["User-Agent"] = UA
    token, page, rows = None, 0, []
    while True:
        f = PAGES / f"page_{page:03d}.json"
        if f.exists():
            j = json.loads(f.read_text())
        else:
            params = {"filter.advanced": FILTER, "fields": FIELDS, "pageSize": 1000, "countTotal": "true"}
            if token: params["pageToken"] = token
            for attempt in range(5):
                time.sleep(1.5)
                r = s.get("https://clinicaltrials.gov/api/v2/studies", params=params, timeout=120)
                if r.status_code == 200: break
                time.sleep(10 * (attempt + 1))
            r.raise_for_status()
            f.write_text(r.text); j = r.json()
        if page == 0: print("total", j.get("totalCount"))
        for st in j["studies"]:
            p = st["protocolSection"]
            sp = p.get("sponsorCollaboratorsModule", {}); stt = p.get("statusModule", {}); d = p.get("designModule", {})
            rows.append({
                "nct": p["identificationModule"]["nctId"],
                "lead_sponsor": sp.get("leadSponsor", {}).get("name", ""),
                "org": p["identificationModule"].get("organization", {}).get("fullName", ""),
                "collaborators": "|".join(c.get("name", "") for c in sp.get("collaborators", [])),
                "phases": "|".join(d.get("phases", [])),
                "status": stt.get("overallStatus", ""),
                "start": stt.get("startDateStruct", {}).get("date", ""),
                "first_post": stt.get("studyFirstPostDateStruct", {}).get("date", ""),
                "last_update_post": stt.get("lastUpdatePostDateStruct", {}).get("date", ""),
                "pcd": stt.get("primaryCompletionDateStruct", {}).get("date", ""),
                "enroll": d.get("enrollmentInfo", {}).get("count", ""),
            })
        token = j.get("nextPageToken"); page += 1
        if not token: break
    out = HERE / "data" / "trials_current.csv"
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), "trials ->", out)

if __name__ == "__main__":
    main()
