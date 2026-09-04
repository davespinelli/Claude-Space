#!/usr/bin/env python3
"""Scan Freelancer.com public API for fresh, well-budgeted jobs we can do (Python, data, automation,
AI agents, scraping, dashboards, trading). Writes products/freelance/JOBS.md (latest shortlist) and appends
new ids to products/freelance/seen.csv so proposals are drafted once. No login needed."""
import json, time, datetime as dt, csv
from pathlib import Path
import requests
ROOT = Path(__file__).resolve().parents[2]; OUT = ROOT / "products" / "freelance"
QUERIES = ["python", "scraping", "automation", "chatbot", "dashboard", "pandas", "backtest", "trading", "excel", "api", "openai", "streamlit", "etl", "selenium", "fastapi"]
SKILL_WORDS = {"python", "scrap", "automat", "bot", "api", "data", "dashboard", "pandas", "trading", "backtest", "excel", "csv", "etl", "ai", "gpt", "llm", "claude", "openai", "streamlit", "fastapi", "django", "flask", "sql", "pipeline", "selenium", "playwright"}
MIN_BUDGET_USD = 100
API = "https://www.freelancer.com/api/projects/0.1/projects/active/"

def fetch(q):
    r = requests.get(API, params={"query": q, "limit": 50, "compact": "true", "job_details": "true", "full_description": "true", "sort_field": "time_updated"}, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status(); return r.json()["result"]["projects"]

def main():
    seen_path = OUT / "seen.csv"; seen = set()
    if seen_path.exists(): seen = {row[0] for row in csv.reader(seen_path.open()) if row}
    jobs = {}
    for q in QUERIES:
        try:
            for p in fetch(q): jobs[p["id"]] = p
        except Exception as e: print("query failed", q, e)
        time.sleep(0.5)
    rows = []
    for pid, p in jobs.items():
        b = p.get("budget") or {}; cur = (p.get("currency") or {}).get("exchange_rate", 1.0) or 1.0
        lo, hi = (b.get("minimum") or 0) * cur, (b.get("maximum") or 0) * cur
        if p.get("type") == "hourly": lo, hi = lo * 20, hi * 20      # rough: 20h project
        if max(lo, hi) < MIN_BUDGET_USD: continue
        text = (p.get("title", "") + " " + (p.get("preview_description") or p.get("description") or "")).lower()
        fit = sum(1 for w in SKILL_WORDS if w in text)
        if fit < 2: continue
        rows.append(dict(id=pid, title=p.get("title", "").strip(), budget=f"${lo:,.0f}–${hi:,.0f}" + (" (hourly est.)" if p.get("type") == "hourly" else ""), hi=hi,
                         bids=p.get("bid_stats", {}).get("bid_count", 0), age_h=(time.time() - p.get("time_submitted", time.time())) / 3600, fit=fit,
                         url=f"https://www.freelancer.com/projects/{p.get('seo_url', pid)}", new=str(pid) not in seen,
                         desc=(p.get("preview_description") or p.get("description") or "")[:600].replace("\n", " ")))
    rows.sort(key=lambda r: (-r["new"], -r["fit"], r["bids"], -r["hi"]))
    md = [f"# Freelancer.com shortlist — {dt.datetime.utcnow():%Y-%m-%d %H:%M} UTC", f"{len(rows)} matching jobs (budget ≥ ${MIN_BUDGET_USD}, ≥2 skill hits). NEW = not seen before.", "",
          "| New | Fit | Bids | Age h | Budget | Title | Link |", "|---|---|---|---|---|---|---|"]
    md += [f"| {'NEW' if r['new'] else ''} | {r['fit']} | {r['bids']} | {r['age_h']:.0f} | {r['budget']} | {r['title'][:70]} | [open]({r['url']}) |" for r in rows[:60]]
    md += ["", "## Descriptions (new jobs only)"] + [f"### {r['id']} — {r['title']}\n{r['budget']} · {r['bids']} bids · {r['url']}\n\n{r['desc']}\n" for r in rows if r["new"]][:25]
    (OUT / "JOBS.md").write_text("\n".join(md))
    with seen_path.open("a", newline="") as f:
        w = csv.writer(f); [w.writerow([r["id"], dt.date.today(), r["title"][:80]]) for r in rows if r["new"]]
    print(f"{len(rows)} jobs, {sum(r['new'] for r in rows)} new; top: " + "; ".join(f"{r['title'][:40]} {r['budget']} ({r['bids']} bids)" for r in rows[:5]))

if __name__ == "__main__": main()
