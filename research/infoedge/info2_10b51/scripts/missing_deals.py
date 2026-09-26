"""Information only (not part of the verdict): for primary events whose company has no Yahoo price, did a
takeover filing (PREM14A / DEFM14A / SC TO-T / SC 14D9 / SC TO-C / DEFA14A) appear inside the +1..+60
trading-day window, or later? Uses the EDGAR submissions API (one request per company).
Writes data/missing_price_deal_check.csv."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec

DEAL = {"PREM14A", "DEFM14A", "SC TO-T", "SC 14D9", "SC TO-C", "SC 14D9-C", "PREM14C", "DEFM14C", "SC 13E3"}
P = pd.read_parquet(sec.CACHE / "yahoo" / "px" / "SPY.parquet")
cal = P.index


def main():
    t = pd.read_csv(sec.ROOT / "data" / "event_returns_terminations.csv", parse_dates=["filed"], low_memory=False)
    m = t[t.primary.astype(bool) & t.status.isin(["no_price", "no_price_at_event"])].copy()
    rows = []
    for r in m.itertuples():
        d = sec.get_json(f"https://data.sec.gov/submissions/CIK{int(r.cik):010d}.json", "submissions")
        rec = d.get("filings", {}).get("recent", {})
        f = pd.DataFrame({"form": rec.get("form", []), "date": pd.to_datetime(rec.get("filingDate", []))})
        pos0 = cal.searchsorted(r.filed, side="right") - 1
        end = cal[min(pos0 + 60, len(cal) - 1)]
        deal = f[f.form.isin(DEAL)]
        inwin = deal[(deal.date > r.filed) & (deal.date <= end)]
        later = deal[deal.date > end]
        rows.append({"company": r.company, "cik": r.cik, "filed": r.filed.date(), "window_end": end.date(),
                     "deal_filing_in_window": not inwin.empty, "first_in_window": inwin.date.min(),
                     "deal_filing_later": not later.empty, "first_later": later.date.min(),
                     "deal_before_event": not deal[deal.date <= r.filed].empty})
    out = pd.DataFrame(rows)
    out.to_csv(sec.ROOT / "data" / "missing_price_deal_check.csv", index=False)
    print(out[["deal_filing_in_window", "deal_filing_later", "deal_before_event"]].sum().to_dict(), len(out))


if __name__ == "__main__":
    main()
