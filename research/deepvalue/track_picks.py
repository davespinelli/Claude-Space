#!/usr/bin/env python3
"""Track every published verdict (PICKS.md ideas and COVERAGE.md passes) vs IWM and SPY since publication.
Writes research/deepvalue/TRACK.md. Run daily."""
import re, datetime as dt
from pathlib import Path
import pandas as pd, yfinance as yf
ROOT = Path(__file__).resolve().parents[2]; DV = ROOT / "research" / "deepvalue"
def rows(path, cols):
    out = []
    for line in path.read_text().splitlines():
        if not line.startswith("| 20"): continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= len(cols): out.append(dict(zip(cols, parts)))
    return out
picks = rows(DV / "PICKS.md", ["date","ticker","verdict","conviction","price","thesis","kill","note"])
cov = rows(DV / "COVERAGE.md", ["date","ticker","verdict","conviction","price","line"])
seen = {(r["date"], r["ticker"]) for r in picks}
allrows = picks + [r for r in cov if (r["date"], r["ticker"]) not in seen]
if not allrows:
    (DV / "TRACK.md").write_text("# Track record\n\nNo published verdicts yet.\n"); raise SystemExit("no rows")
tickers = sorted({r["ticker"] for r in allrows} | {"IWM", "SPY"})
start = min(r["date"] for r in allrows)
px = yf.download(tickers, start=start, auto_adjust=True, progress=False)["Close"].ffill()
out = []
for r in allrows:
    t, d0 = r["ticker"], pd.Timestamp(r["date"])
    if t not in px.columns: continue
    s = px[t].loc[d0:].dropna()
    if s.empty: continue
    p0 = float(re.sub(r"[^0-9.]", "", r["price"]) or s.iloc[0]); p1 = float(s.iloc[-1])
    b = lambda tk: float(px[tk].loc[d0:].dropna().iloc[-1] / px[tk].loc[d0:].dropna().iloc[0] - 1)
    out.append(dict(date=r["date"], ticker=t, verdict=r["verdict"], conv=r["conviction"], p0=p0, p1=p1, ret=p1/p0-1, iwm=b("IWM"), spy=b("SPY"), days=(s.index[-1]-d0).days))
df = pd.DataFrame(out)
df["vs_iwm"] = df.ret - df.iwm
md = [f"# Track record — updated {dt.date.today()}", "", "Every verdict since publication. Returns are price-only, no costs. IDEA = published pick; WATCH/PASS tracked so we learn from rejections.", ""]
for v in ["IDEA", "WATCH", "PASS"]:
    sub = df[df.verdict.str.upper().str.startswith(v)]
    if sub.empty: continue
    md += [f"## {v} ({len(sub)}) — avg return {sub.ret.mean():+.1%}, avg vs IWM {sub.vs_iwm.mean():+.1%}", "| Date | Ticker | Conv | Price at pub | Now | Return | IWM | SPY | vs IWM | Days |", "|---|---|---|---|---|---|---|---|---|---|"]
    md += [f"| {r.date} | {r.ticker} | {r.conv} | {r.p0:.2f} | {r.p1:.2f} | {r.ret:+.1%} | {r.iwm:+.1%} | {r.spy:+.1%} | {r.vs_iwm:+.1%} | {r.days} |" for r in sub.itertuples()]
    md.append("")
(DV / "TRACK.md").write_text("\n".join(md)); print(f"tracked {len(df)} verdicts")
