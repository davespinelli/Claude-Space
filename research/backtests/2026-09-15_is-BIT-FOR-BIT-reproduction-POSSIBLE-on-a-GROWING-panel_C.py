#!/usr/bin/env python3
"""IDEA 890 (lane C, 2026-09-15) — is BIT-FOR-BIT reproduction of a committed run POSSIBLE at
all on a GROWING panel, and what does a panel end-date stamp actually buy?

Idea 886 re-ran two committed scripts and neither left its artifacts bit-identical, blaming the
trading days data/prices.csv has gained since.  This run decomposes the reproduction error into
its channels and prices the proposed PROTOCOL stamp against each:

  CHANNEL A — LENGTH.   The panel is longer than it was when the number was published, so the
                        run covers more days.  A panel end-date stamp is *supposed* to fix this.
  CHANNEL B — RESTATEMENT. research/cache_prices.py re-downloads the WHOLE history every day
                        (yfinance auto_adjust=True) and overwrites data/prices.csv.  Adjusted
                        closes are restated backwards on every dividend/split, so cells the
                        published run READ may no longer hold the values it read.  No end-date
                        stamp can reach this channel.
  CHANNEL C — CALENDAR/UNIVERSE (found by S5, not pre-declared).  The panel's row calendar and
                        column set have themselves been revised inside the committed history.
                        No end-date stamp can reach this channel either.

TWO TUNED PARAMETERS, exactly, both reported at every grid point:
  P1  run set        = 6 books (all baseline.py primitives or committed-memo books, never new)
  P2  stamp granularity = {DAY, WEEK, MONTH, QUARTER, YEAR}
  -> 30 cells, all published.  Panel / window / rung are reported axes, not tuned.

PROTOCOL: 10 bps per unit turnover, next-day execution (engine), 260-day warm-up, no shorting,
no leverage.  Rule 8 walk-forward is run and reported (book leg AND drift-law leg).

Artifacts: .console.txt .curve.csv .truerungs.csv .drift.csv .flips.csv .stamp.csv .restate.csv
           .calendar.csv .walkforward.csv .lengthlaw.csv  (+ .result.md written by hand)
Deterministic, standalone: python research/backtests/<this file>
"""
from __future__ import annotations
import hashlib, io, re, subprocess, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

SLUG = "2026-09-15_is-BIT-FOR-BIT-reproduction-POSSIBLE-on-a-GROWING-panel_C"
OUT = ROOT / "research" / "backtests"
COST_BPS, WARM = 10, 260
CONSOLE: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    CONSOLE.append(s)


# ----------------------------------------------------------------------------- P1: the run set
def w_top20(px, gross=0.65, n=20, max_vol=0.60):
    """The 2026-09-04 first-KEEP-4b book / idea 879 memo: top-n composite, NO vol scaler."""
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < max_vol))
    return (elig.rank(axis=1, ascending=False) <= n).astype(float) * (gross / n)


def w_spy(px):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w["SPY"] = 1.0
    return w


BOOKS = {                                   # key: (weights_fn, rebalance freq)
    "LIVE-v2-g075-W":  (lambda p: rules_v2_weights(p, band=0.03, gross=0.75), "W"),
    "v2-g100-W":       (lambda p: rules_v2_weights(p, band=0.03, gross=1.00), "W"),
    "RULESv1-n5-W":    (lambda p: rules_v1_weights(p), "W"),
    "TOP20-g065-M":    (lambda p: w_top20(p, gross=0.65), "M"),
    "TOP20-g075-M":    (lambda p: w_top20(p, gross=0.75), "M"),
    "SPY-BH-W":        (w_spy, "W"),
}
GRAINS = ["DAY", "WEEK", "MONTH", "QUARTER", "YEAR"]


def run_returns(px, key):
    fn, freq = BOOKS[key]
    return backtest(px, fn(px), cost_bps=COST_BPS, freq=freq)["returns"]


def read(r):
    """The record's published triple + the two half Sharpes, exactly as baseline._row reads them."""
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"], N=len(r))


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


t0 = time.time()
px = load_universe()
PANEL_END, PANEL_START = px.index[-1], px.index[0]
START = px.index[WARM]
PX_SHA = sha((ROOT / "data" / "prices.csv").read_bytes())
say(f"# {SLUG}")
say(f"panel U56  {px.shape[0]} rows x {px.shape[1]} cols  {PANEL_START.date()} -> {PANEL_END.date()}"
    f"   warm-start {START.date()}   sha256(prices.csv)[:16] = {PX_SHA}")
say("")

FULL = {k: run_returns(px, k).loc[START:] for k in BOOKS}
FULLM = {k: read(FULL[k]) for k in BOOKS}

# =============================================================================== GATES (first)
say("## GATES — printed before any hypothesis is read")
gates = []

# G1: the committed TOP20-g065-M triple from the 2026-09-15 idea-879 memo (same panel, same day)
m = FULLM["TOP20-g065-M"]
g1 = max(abs(m["CAGR"] - 0.1269), abs(m["Sharpe"] - 1.201) / 10, abs(m["MaxDD"] + 0.1711))
say(f"G1 committed memo book TOP20-g065-M rebuilt from baseline.score: {m['CAGR']:.4%} / {m['Sharpe']:.4f} / "
    f"{m['MaxDD']:.4%} vs memo 12.69% / 1.201 / -17.11%  max|d| {g1:.3e} (bar 5e-4)  "
    f"{'PASS' if g1 < 5e-4 else 'FAIL'}")
gates.append(("G1 memo TOP20 triple", g1 < 5e-4))

# G2: the LIVE book and SPY anchors the record quotes
lv, sp = FULLM["LIVE-v2-g075-W"], FULLM["SPY-BH-W"]
g2 = max(abs(lv["CAGR"] - 0.0862), abs(lv["Sharpe"] - 1.201) / 10, abs(lv["MaxDD"] + 0.1205),
         abs(sp["CAGR"] - 0.1513), abs(sp["Sharpe"] - 0.885) / 10, abs(sp["MaxDD"] + 0.3372))
say(f"G2 LIVE {lv['CAGR']:.4%} / {lv['Sharpe']:.4f} / {lv['MaxDD']:.4%} (memo 8.62/1.201/-12.05) ; "
    f"SPY {sp['CAGR']:.4%} / {sp['Sharpe']:.4f} / {sp['MaxDD']:.4%} (memo 15.13/0.885/-33.72)  "
    f"max|d| {g2:.3e} (bar 5e-4)  {'PASS' if g2 < 5e-4 else 'FAIL'}")
gates.append(("G2 LIVE+SPY anchors", g2 < 5e-4))

# G3: TRUNCATION == PREFIX.  Re-running on a panel cut at T must reproduce the full run's prefix
#     exactly, or CHANNEL A is not even a clean object.
g3, g3rows = 0.0, []
for T in [px.index[-1 - k] for k in (1, 21, 63, 252, 756, 1260)]:
    pxt = px.loc[:T]
    for k in ("LIVE-v2-g075-W", "TOP20-g065-M"):
        a = run_returns(pxt, k).loc[START:]
        b = FULL[k].loc[:T]
        d = float((a - b).abs().max())
        g3 = max(g3, d)
        g3rows.append((str(T.date()), k, len(a), d))
say(f"G3 truncation==prefix over 6 end-dates x 2 books (12 re-runs): max|d_return| {g3:.3e} "
    f"(bar 1e-12)  {'PASS' if g3 < 1e-12 else 'FAIL'}")
gates.append(("G3 truncation==prefix", g3 < 1e-12))

# G4: determinism of the engine on one book (same input twice)
g4 = float((run_returns(px, "TOP20-g065-M").loc[START:] - FULL["TOP20-g065-M"]).abs().max())
say(f"G4 determinism, same panel re-run: max|d| {g4:.3e} (bar 0)  {'PASS' if g4 == 0.0 else 'FAIL'}")
gates.append(("G4 determinism", g4 == 0.0))

# G5: the committed history of data/prices.csv is readable and complete
REVS = subprocess.run(["git", "log", "--format=%H %ad", "--date=short", "--", "data/prices.csv"],
                      cwd=ROOT, capture_output=True, text=True).stdout.strip().split("\n")
REVS = [r.split() for r in REVS if r]
shallow = (ROOT / ".git" / "shallow").exists()
say(f"G5 committed data/prices.csv revisions found: {len(REVS)} "
    f"({REVS[-1][1]} -> {REVS[0][1]}), history shallow={shallow}  "
    f"{'PASS' if len(REVS) >= 5 and not shallow else 'FAIL'}")
gates.append(("G5 price-file history", len(REVS) >= 5 and not shallow))
say(f"GATES {sum(g for _, g in gates)}/{len(gates)} PASS")
say("")

# ========================================================================== HYPOTHESES (declared)
say("## HYPOTHESES, declared before the numbers below are read")
say("H_BIT   : a panel END-DATE STAMP is sufficient for bit-for-bit reproduction of a committed run.")
say("H_DRIFT : one added month of panel moves a published number by less than its published precision")
say("          (median |dCAGR| < 0.05 pp, |dSharpe| < 0.005, |dMaxDD| < 0.05 pp per month).")
say("H_FLIP  : no committed 4a/4b verdict flips inside 12 months of panel growth.")
say("H_STAMP : a MONTH-granularity stamp leaves residual ambiguity below published precision.")
say("H_WF    : per-month drift measured in sample (rungs <= 2016-12-31) predicts the out-of-sample")
say("          drift (rungs >= 2017-01-01) within a factor of 2, per book.")
say("")

# ============================================================= S1  the panel-growth curve (CHANNEL A)
RUNGS = [d for d in px.index if d >= pd.Timestamp("2011-01-03")]
curve = []
for k in BOOKS:
    r = FULL[k]
    for T in RUNGS:
        rr = r.loc[:T]
        mm = read(rr)
        curve.append(dict(book=k, rung=T, **mm))
CU = pd.DataFrame(curve)
CU["ym"] = CU["rung"].dt.to_period("M")
CU.to_csv(OUT / f"{SLUG}.curve.csv", index=False)
say(f"## S1  panel-growth curve: {len(RUNGS)} daily rungs x {len(BOOKS)} books = {len(CU)} readings "
    f"({RUNGS[0].date()} -> {RUNGS[-1].date()})")

# TRUE re-runs (not prefixes) on month-end rungs of the last 36 months + the last 63 daily rungs,
# so the curve above is licensed by measurement, not by G3 alone.
me = CU[CU.book == "SPY-BH-W"].groupby("ym")["rung"].max().tolist()[-36:]
true_rungs = sorted(set(me) | set(px.index[-63:]))
trows = []
for T in true_rungs:
    pxt = px.loc[:T]
    for k in BOOKS:
        a = read(run_returns(pxt, k).loc[START:T])
        b = read(FULL[k].loc[:T])
        trows.append(dict(rung=T, book=k, **{f"true_{x}": a[x] for x in ("CAGR", "Sharpe", "MaxDD")},
                          **{f"pref_{x}": b[x] for x in ("CAGR", "Sharpe", "MaxDD")},
                          dCAGR=a["CAGR"] - b["CAGR"], dSharpe=a["Sharpe"] - b["Sharpe"],
                          dMaxDD=a["MaxDD"] - b["MaxDD"]))
TR = pd.DataFrame(trows)
TR.to_csv(OUT / f"{SLUG}.truerungs.csv", index=False)
say(f"     TRUE re-runs on {len(true_rungs)} rungs x {len(BOOKS)} books = {len(TR)} full backtests; "
    f"max|true-prefix| CAGR {TR.dCAGR.abs().max():.3e}  Sharpe {TR.dSharpe.abs().max():.3e}  "
    f"MaxDD {TR.dMaxDD.abs().max():.3e}")
say("")

# ====================================================================== S2  drift per added month
ME = CU[CU.rung.isin(CU.groupby(["book", "ym"])["rung"].transform("max"))].copy()
ME = ME.sort_values(["book", "rung"])
drows = []
for k, g in ME.groupby("book"):
    for win, gg in (("ALL 2011+", g), ("IS <=2016", g[g.rung <= "2016-12-31"]),
                    ("OOS 2017+", g[g.rung >= "2017-01-01"]), ("LAST 24m", g.tail(25))):
        d = gg[["CAGR", "Sharpe", "MaxDD", "H1", "H2"]].diff().dropna().abs()
        if d.empty:
            continue
        drows.append(dict(book=k, window=win, months=len(d),
                          **{f"med_{c}": d[c].median() for c in d.columns},
                          **{f"p90_{c}": d[c].quantile(0.9) for c in d.columns},
                          **{f"max_{c}": d[c].max() for c in d.columns}))
DR = pd.DataFrame(drows)
DR.to_csv(OUT / f"{SLUG}.drift.csv", index=False)
say("## S2  drift per ONE added month of panel (month-end rungs, |delta| vs the previous rung)")
say("     book                  window      n  med|dCAGR|  p90|dCAGR|  med|dSharpe|  med|dMaxDD|  "
    "med|dH1|  med|dH2|")
for _, r in DR.iterrows():
    say(f"     {r.book:<21} {r.window:<10} {int(r.months):>3}  {r.med_CAGR*100:>9.4f}pp {r.p90_CAGR*100:>9.4f}pp"
        f"  {r.med_Sharpe:>12.5f}  {r.med_MaxDD*100:>9.4f}pp  {r.med_H1:>7.4f}  {r.med_H2:>7.4f}")
a = DR[DR.window == "ALL 2011+"]
say(f"     POOLED median per month: dCAGR {a.med_CAGR.median()*100:.4f}pp  dSharpe {a.med_Sharpe.median():.5f}  "
    f"dMaxDD {a.med_MaxDD.median()*100:.4f}pp  dH1 {a.med_H1.median():.4f}  dH2 {a.med_H2.median():.4f}")
# one-directional test: MaxDD can only deepen, CAGR/Sharpe can move either way
sgn = []
for k, g in ME.groupby("book"):
    d = g[["CAGR", "Sharpe", "MaxDD", "H1", "H2"]].diff().dropna()
    sgn.append(dict(book=k, **{f"up_{c}": float((d[c] > 0).mean()) for c in d.columns}))
SG = pd.DataFrame(sgn)
say("     share of months the metric moves UP (0.5 = two-directional, 0/1 = one-directional):")
for _, r in SG.iterrows():
    say(f"     {r.book:<21} CAGR {r.up_CAGR:.3f}  Sharpe {r.up_Sharpe:.3f}  MaxDD {r.up_MaxDD:.3f}  "
        f"H1 {r.up_H1:.3f}  H2 {r.up_H2:.3f}")
say("")

# ================================================================= S3  verdict flips (4a and 4b)
def verdicts(row_b, row_live, row_spy):
    a = (row_b["H1"] > row_live["H1"] and row_b["H2"] > row_live["H2"]
         and row_b["MaxDD"] >= row_live["MaxDD"])
    b = (row_b["H1"] > row_spy["H1"] and row_b["H2"] > row_spy["H2"]
         and row_b["MaxDD"] >= 0.60 * row_spy["MaxDD"] and row_b["CAGR"] >= 0.70 * row_spy["CAGR"])
    return a, b


piv = {k: g.set_index("rung") for k, g in ME.groupby("book")}
frows = []
for k in BOOKS:
    for T in piv[k].index:
        rb, rl, rs = piv[k].loc[T], piv["LIVE-v2-g075-W"].loc[T], piv["SPY-BH-W"].loc[T]
        a, b = verdicts(rb, rl, rs)
        frows.append(dict(book=k, rung=T, p4a=a, p4b=b))
FL = pd.DataFrame(frows)
FL.to_csv(OUT / f"{SLUG}.flips.csv", index=False)
say("## S3  verdict census over panel end-dates (4a vs the LIVE book, 4b full-sample legs vs SPY,")
say("       both re-read at EVERY rung; the rule-8 leg of 4b is handled in S6, not here)")
say("     book                  4a flips  4b flips  4a today  4b today  months the TODAY verdict has held")
for k in BOOKS:
    g = FL[FL.book == k].sort_values("rung")
    fa = int((g.p4a != g.p4a.shift()).iloc[1:].sum())
    fb = int((g.p4b != g.p4b.shift()).iloc[1:].sum())
    held = {}
    for c in ("p4a", "p4b"):
        v = g[c].tolist()
        n = 0
        for x in reversed(v[:-1]):
            if x == v[-1]:
                n += 1
            else:
                break
        held[c] = n
    say(f"     {k:<21} {fa:>8} {fb:>9}  {str(g.p4a.iloc[-1]):>8} {str(g.p4b.iloc[-1]):>9}  "
        f"4a {held['p4a']:>3}m / 4b {held['p4b']:>3}m  (of {len(g)-1})")
flip12 = 0
for k in BOOKS:
    g = FL[FL.book == k].sort_values("rung").tail(13)
    flip12 += int((g.p4a != g.p4a.shift()).iloc[1:].sum()) + int((g.p4b != g.p4b.shift()).iloc[1:].sum())
say(f"     flips inside the LAST 12 months of panel growth, pooled over 6 books x 2 paths: {flip12}")
say("")

# ============================================== S4  P2: what a stamp of each granularity leaves open
KEY = {"DAY": lambda i: i.strftime("%Y-%m-%d"), "WEEK": lambda i: i.strftime("%G-W%V"),
       "MONTH": lambda i: i.strftime("%Y-%m"), "QUARTER": lambda i: f"{i.year}Q{(i.month-1)//3+1}",
       "YEAR": lambda i: str(i.year)}
srows = []
CU17 = CU[CU.rung >= "2017-01-01"].copy()
for k in BOOKS:
    g = CU17[CU17.book == k].copy()
    for gr in GRAINS:
        g["bucket"] = [KEY[gr](d) for d in g["rung"]]
        sp_ = g.groupby("bucket")[["CAGR", "Sharpe", "MaxDD", "H1", "H2"]].agg(lambda x: x.max() - x.min())
        n = g.groupby("bucket").size()
        sp_ = sp_[n >= 2]
        srows.append(dict(book=k, grain=gr, buckets=int(len(sp_)),
                          **{f"med_{c}": (sp_[c].median() if len(sp_) else 0.0) for c in sp_.columns},
                          **{f"max_{c}": (sp_[c].max() if len(sp_) else 0.0) for c in sp_.columns}))
ST = pd.DataFrame(srows)
ST.to_csv(OUT / f"{SLUG}.stamp.csv", index=False)
say("## S4  P1 x P2 GRID, all 30 cells: residual ambiguity a stamp of each granularity LEAVES OPEN")
say("       (max-min of the metric across the trading days that share one stamp; rungs 2017+)")
say("     book                  grain     buckets  med spread CAGR   max CAGR   med Sharpe  max Sharpe  med MaxDD")
for _, r in ST.iterrows():
    say(f"     {r.book:<21} {r.grain:<8} {r.buckets:>7}  {r.med_CAGR*100:>13.4f}pp {r.max_CAGR*100:>9.4f}pp"
        f"  {r.med_Sharpe:>10.5f}  {r.max_Sharpe:>9.5f}  {r.med_MaxDD*100:>8.4f}pp")
say("")

# ================================================== S5  CHANNEL B: does the PAST of the panel move?
say("## S5  CHANNEL B — restatement. Every committed revision of data/prices.csv compared, cell by")
say("       cell, against TODAY's file on the dates and tickers they SHARE.")
today_raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
rrows = []
for h, dte in REVS:
    blob = subprocess.run(["git", "show", f"{h}:data/prices.csv"], cwd=ROOT,
                          capture_output=True).stdout
    old = pd.read_csv(io.BytesIO(blob), index_col=0, parse_dates=True)
    oend = old.index[-1]
    idx = old.index.intersection(today_raw.index)
    cols = old.columns.intersection(today_raw.columns)
    A, B = old.loc[idx, cols], today_raw.loc[idx, cols]
    both = A.notna() & B.notna()
    diff = (A - B).abs()
    changed = ((diff > 0) & both)
    rel = (diff / B.abs().replace(0, np.nan))[changed]
    first_chg = changed.any(axis=1)
    rrows.append(dict(rev=h[:10], date=dte, sha=sha(blob), rows=len(old), end=str(oend.date()),
                      shared_cells=int(both.sum().sum()), changed=int(changed.sum().sum()),
                      share=float(changed.sum().sum() / max(both.sum().sum(), 1)),
                      tickers_touched=int((changed.sum(axis=0) > 0).sum()),
                      max_absdiff=float(diff[changed].max().max()) if changed.any().any() else 0.0,
                      max_reldiff=float(rel.max().max()) if changed.any().any() else 0.0,
                      first_changed_date=str(first_chg[first_chg].index.min().date()) if first_chg.any() else "-",
                      index_prefix=bool(len(idx) == len(old.index))))
RS = pd.DataFrame(rrows)
say("     rev        date        sha16              rows  end         shared cells  changed  share    "
    "tickers  max|d|     max rel   first changed date  dates-are-prefix")
for _, r in RS.iterrows():
    say(f"     {r.rev:<10} {r.date}  {r.sha}  {r.rows:>5}  {r.end}  {r.shared_cells:>12,}  "
        f"{r.changed:>7,}  {r.share:>7.4%}  {r.tickers_touched:>7}  {r.max_absdiff:>9.4f}  "
        f"{r.max_reldiff:>8.4%}  {r.first_changed_date:<18}  {r.index_prefix}")

# metric cost of CHANNEL B alone: same end date, OLD file vs TODAY's file cut to that end date
say("     metric cost of CHANNEL B ALONE (identical end date, so a perfect stamp is assumed):")
brows = []
for h, dte in REVS:
    blob = subprocess.run(["git", "show", f"{h}:data/prices.csv"], cwd=ROOT,
                          capture_output=True).stdout
    old = pd.read_csv(io.BytesIO(blob), index_col=0, parse_dates=True).dropna(how="all").ffill()
    old = old.loc[px.index[0]:].reindex(columns=px.columns)
    oend = old.index[-1]
    if oend not in px.index or old.isna().all(axis=0).any():
        say(f"     (revision {h[:10]} skipped for the metric leg: end {oend.date()} not on today's calendar "
            f"or a column is missing)")
        continue
    new = px.loc[:oend]
    for k in ("LIVE-v2-g075-W", "TOP20-g065-M", "SPY-BH-W"):
        a = read(run_returns(old, k).loc[START:])
        b = read(run_returns(new, k).loc[START:])
        brows.append(dict(rev=h[:10], date=dte, end=str(oend.date()), book=k,
                          old_CAGR=a["CAGR"], new_CAGR=b["CAGR"], dCAGR=a["CAGR"] - b["CAGR"],
                          old_Sharpe=a["Sharpe"], new_Sharpe=b["Sharpe"], dSharpe=a["Sharpe"] - b["Sharpe"],
                          old_MaxDD=a["MaxDD"], new_MaxDD=b["MaxDD"], dMaxDD=a["MaxDD"] - b["MaxDD"]))
BC = pd.DataFrame(brows)
pd.concat([RS.assign(kind="cells"), BC.assign(kind="metric")], ignore_index=True).to_csv(
    OUT / f"{SLUG}.restate.csv", index=False)
say("     rev        end         book                  dCAGR(pp)   dSharpe     dMaxDD(pp)")
for _, r in BC.iterrows():
    say(f"     {r.rev:<10} {r.end}  {r.book:<21} {r.dCAGR*100:>10.4f}  {r.dSharpe:>10.5f}  {r.dMaxDD*100:>10.4f}")
if len(BC):
    say(f"     CHANNEL B pooled: median |dCAGR| {BC.dCAGR.abs().median()*100:.4f}pp  max {BC.dCAGR.abs().max()*100:.4f}pp"
        f" | median |dSharpe| {BC.dSharpe.abs().median():.5f}  max {BC.dSharpe.abs().max():.5f}"
        f" | max |dMaxDD| {BC.dMaxDD.abs().max()*100:.4f}pp")
    say(f"     bit-for-bit cells: {int((RS.changed == 0).sum())} of {len(RS)} committed revisions leave EVERY "
        f"shared cell identical")

# S5b: CHANNEL C — the panel's CALENDAR/UNIVERSE convention itself changed on 2026-09-04 (the two
# 2026-09-03 revisions carry 6,059-6,060 rows incl. weekend rows from the crypto tickers, and 58
# columns).  Re-run the same revisions RESTRICTED to today's trading calendar to separate the
# calendar channel from the restatement channel.
say("     CHANNEL C — calendar/universe convention. Same revisions, re-run on TODAY's trading days only:")
crows = []
for h, dte in REVS:
    blob = subprocess.run(["git", "show", f"{h}:data/prices.csv"], cwd=ROOT, capture_output=True).stdout
    raw = pd.read_csv(io.BytesIO(blob), index_col=0, parse_dates=True)
    oend = raw.index[-1]
    if oend not in px.index:
        continue
    wknd = int((raw.index.dayofweek >= 5).sum())
    old_cal = raw.reindex(columns=px.columns).loc[px.index[0]:].dropna(how="all").ffill()
    old_fix = raw.reindex(index=px.index[px.index <= oend], columns=px.columns).ffill()
    new = px.loc[:oend]
    for k in ("LIVE-v2-g075-W", "TOP20-g065-M", "SPY-BH-W"):
        b = read(run_returns(new, k).loc[START:])
        a = read(run_returns(old_cal, k).loc[START:])
        c = read(run_returns(old_fix, k).loc[START:])
        crows.append(dict(rev=h[:10], end=str(oend.date()), book=k, rows_raw=len(raw), cols_raw=raw.shape[1],
                          weekend_rows=wknd,
                          asis_dCAGR=a["CAGR"] - b["CAGR"], asis_dSharpe=a["Sharpe"] - b["Sharpe"],
                          calfix_dCAGR=c["CAGR"] - b["CAGR"], calfix_dSharpe=c["Sharpe"] - b["Sharpe"],
                          calfix_dMaxDD=c["MaxDD"] - b["MaxDD"]))
CC = pd.DataFrame(crows)
CC.to_csv(OUT / f"{SLUG}.calendar.csv", index=False)
say("     rev        end         book                  raw rows  cols  weekend rows |  AS IS dCAGR  dSharpe |  "
    "CALENDAR-FIXED dCAGR  dSharpe  dMaxDD")
for _, r in CC.iterrows():
    say(f"     {r.rev:<10} {r.end}  {r.book:<21} {r.rows_raw:>8}  {r.cols_raw:>4}  {r.weekend_rows:>12} | "
        f"{r.asis_dCAGR*100:>11.4f}pp {r.asis_dSharpe:>8.5f} | {r.calfix_dCAGR*100:>19.4f}pp "
        f"{r.calfix_dSharpe:>8.5f} {r.calfix_dMaxDD*100:>7.4f}pp")
odd = CC[CC.weekend_rows > 0]
if len(odd):
    say(f"     the {odd.rev.nunique()} revisions carrying weekend rows: as-is max |dCAGR| {odd.asis_dCAGR.abs().max()*100:.4f}pp "
        f"/ |dSharpe| {odd.asis_dSharpe.abs().max():.5f}; once cut to today's calendar "
        f"{odd.calfix_dCAGR.abs().max()*100:.4f}pp / {odd.calfix_dSharpe.abs().max():.5f} "
        f"-> the gap is {'ENTIRELY' if odd.calfix_dCAGR.abs().max() < 1e-4 else 'NOT entirely'} a calendar fact.")
say("")

say("")

# ============================================================== S6  RULE 8 — required walk-forward
say("## S6  RULE 8 walk-forward. IS = warm-start..2016-12-31 (selector sees this only); "
    "OOS = 2017-01-01..panel end, read once.")
IS_END = pd.Timestamp("2016-12-31")
is_m = {k: read(FULL[k].loc[:IS_END]) for k in BOOKS}
oos_m = {k: read(FULL[k].loc["2017-01-01":]) for k in BOOKS}
say("     book                  IS CAGR  IS Sharpe  IS MaxDD | OOS CAGR  OOS Sharpe  OOS MaxDD  OOS H1/H2")
for k in BOOKS:
    i_, o_ = is_m[k], oos_m[k]
    say(f"     {k:<21} {i_['CAGR']:>7.2%} {i_['Sharpe']:>10.3f} {i_['MaxDD']:>9.2%} | {o_['CAGR']:>8.2%} "
        f"{o_['Sharpe']:>11.3f} {o_['MaxDD']:>10.2%}  {o_['H1']:.3f}/{o_['H2']:.3f}")
pick = max((k for k in BOOKS if k != "SPY-BH-W"), key=lambda k: is_m[k]["Sharpe"])
o, ol, os_ = oos_m[pick], oos_m["LIVE-v2-g075-W"], oos_m["SPY-BH-W"]
p4a, p4b = verdicts(o, ol, os_)
say(f"     IS-only selector (max IS Sharpe among the 5 non-SPY books) picks: {pick}")
say(f"     OOS read once: {o['CAGR']:.2%} / {o['Sharpe']:.3f} / {o['MaxDD']:.2%}  halves {o['H1']:.3f}/{o['H2']:.3f}")
say(f"       vs LIVE OOS {ol['CAGR']:.2%} / {ol['Sharpe']:.3f} / {ol['MaxDD']:.2%} (halves {ol['H1']:.3f}/{ol['H2']:.3f})")
say(f"       vs SPY  OOS {os_['CAGR']:.2%} / {os_['Sharpe']:.3f} / {os_['MaxDD']:.2%} (halves {os_['H1']:.3f}/{os_['H2']:.3f})")
say(f"       PATH 4a {'PASS' if p4a else 'FAIL'}   PATH 4b {'PASS' if p4b else 'FAIL'}")

# the drift law's own walk-forward
wrows = []
for k in BOOKS:
    i_ = DR[(DR.book == k) & (DR.window == "IS <=2016")]
    o_ = DR[(DR.book == k) & (DR.window == "OOS 2017+")]
    if len(i_) and len(o_):
        ic, oc = float(i_.med_CAGR.iloc[0]), float(o_.med_CAGR.iloc[0])
        isx, osx = float(i_.med_Sharpe.iloc[0]), float(o_.med_Sharpe.iloc[0])
        wrows.append(dict(book=k, IS_medCAGR=ic, OOS_medCAGR=oc, ratio_CAGR=oc / ic if ic else np.nan,
                          IS_medSharpe=isx, OOS_medSharpe=osx, ratio_Sharpe=osx / isx if isx else np.nan,
                          within2x=bool(ic and 0.5 <= oc / ic <= 2.0)))
WF = pd.DataFrame(wrows)
WF.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
say("     drift-law walk-forward: does the IS per-month drift predict the OOS per-month drift?")
say("     book                  IS med|dCAGR|  OOS med|dCAGR|  ratio   IS med|dS|  OOS med|dS|  ratio   within 2x")
for _, r in WF.iterrows():
    say(f"     {r.book:<21} {r.IS_medCAGR*100:>12.4f}pp {r.OOS_medCAGR*100:>14.4f}pp {r.ratio_CAGR:>6.2f}"
        f"  {r.IS_medSharpe:>10.5f}  {r.OOS_medSharpe:>11.5f} {r.ratio_Sharpe:>6.2f}   {r.within2x}")
rho = WF[["IS_medCAGR", "OOS_medCAGR"]].corr(method="spearman").iloc[0, 1]
say(f"     spearman(IS med|dCAGR|, OOS med|dCAGR|) over {len(WF)} books = {rho:+.4f}; "
    f"within-2x {int(WF.within2x.sum())}/{len(WF)}")

# S6b: if the drift level does not walk forward, is its LAW portable?  A metric averaged over T
# years should move ~1/T per added month, so fit log|dCAGR| = a + b*log(years) per book, predict
# b = -1, and re-test the IS->OOS prediction after rescaling by the panel length.
lrows = []
for k, g in ME.groupby("book"):
    g = g.sort_values("rung").copy()
    g["yrs"] = g["N"] / 252.0
    d = g[["CAGR", "Sharpe"]].diff().abs()
    y = np.log(d["CAGR"].replace(0, np.nan)).dropna()
    x = np.log(g["yrs"]).reindex(y.index)
    b, a = np.polyfit(x, y, 1)
    r2 = float(np.corrcoef(x, y)[0, 1] ** 2)
    yi = float(g.loc[g.rung <= IS_END, "yrs"].median())
    yo = float(g.loc[g.rung >= "2017-01-01", "yrs"].median())
    w = WF[WF.book == k].iloc[0]
    pred = w.IS_medCAGR * (yo / yi) ** b
    lrows.append(dict(book=k, slope_b=b, R2=r2, yrs_IS=yi, yrs_OOS=yo,
                      pred_OOS_medCAGR=pred, act_OOS_medCAGR=w.OOS_medCAGR,
                      ratio=w.OOS_medCAGR / pred, within2x=bool(0.5 <= w.OOS_medCAGR / pred <= 2.0)))
LW = pd.DataFrame(lrows)
LW.to_csv(OUT / f"{SLUG}.lengthlaw.csv", index=False)
say("     drift LAW (post-hoc, parameter-free prediction b = -1): log|dCAGR| = a + b*log(panel years)")
say("     book                  slope b      R2   median yrs IS/OOS   predicted OOS med|dCAGR|   actual    ratio  within2x")
for _, r in LW.iterrows():
    say(f"     {r.book:<21} {r.slope_b:>7.3f} {r.R2:>7.3f}   {r.yrs_IS:>5.2f} / {r.yrs_OOS:>5.2f}      "
        f"{r.pred_OOS_medCAGR*100:>19.4f}pp {r.act_OOS_medCAGR*100:>8.4f}pp {r.ratio:>7.2f}   {r.within2x}")
say(f"     median slope {LW.slope_b.median():+.3f} (prediction -1, miss {abs(LW.slope_b.median()+1):.3f}); "
    f"length-rescaled IS->OOS within 2x: {int(LW.within2x.sum())}/{len(LW)} vs {int(WF.within2x.sum())}/{len(WF)} in levels")
say("")

# ============================================= S7  what the record stamps today (secondary reading)
say("## S7  secondary: does the record STAMP its panel today?  regex over committed memo/result files")
files = sorted(OUT.glob("*.md"))
pat_end = re.compile(r"(panel|sample|data)[^.\n]{0,40}(end|through|to)\s*[:=]?\s*20\d\d-\d\d-\d\d", re.I)
pat_sha = re.compile(r"sha ?-?256|sha1|md5|file hash", re.I)
n_end = sum(1 for f in files if pat_end.search(f.read_text(errors="ignore")))
n_sha = sum(1 for f in files if pat_sha.search(f.read_text(errors="ignore")))
say(f"     {len(files)} committed .md files in research/backtests: {n_end} ({n_end/max(len(files),1):.1%}) carry an "
    f"explicit panel end-date; {n_sha} ({n_sha/max(len(files),1):.1%}) carry any file hash.")
say("")

# ====================================================================================== VERDICTS
say("## VERDICTS on the declared hypotheses")
bit_ok = bool(len(RS) and (RS.changed == 0).all()) and g3 < 1e-12
say(f"H_BIT   {'PASS' if bit_ok else 'FAIL'}: truncation reproduces a run exactly (CHANNEL A closed, G3 {g3:.1e}), "
    f"but {int((RS.changed > 0).sum())} of {len(RS)} committed price-file revisions DISAGREE with today's file on "
    f"cells they share (max {RS.share.max():.4%} of shared cells) and {int((CC.weekend_rows>0).sum()/3)} carry a "
    f"different row calendar. A date stamp reaches neither CHANNEL B nor CHANNEL C.")
dr = DR[DR.window == "ALL 2011+"]
h_drift = bool(dr.med_CAGR.median() < 0.0005 and dr.med_Sharpe.median() < 0.005
               and dr.med_MaxDD.median() < 0.0005)
say(f"H_DRIFT {'PASS' if h_drift else 'FAIL'}: median per-month dCAGR {dr.med_CAGR.median()*100:.4f}pp, "
    f"dSharpe {dr.med_Sharpe.median():.5f}, dMaxDD {dr.med_MaxDD.median()*100:.4f}pp "
    f"(bars 0.05pp / 0.005 / 0.05pp).")
say(f"H_FLIP  {'PASS' if flip12 == 0 else 'FAIL'}: {flip12} verdict flips inside the last 12 months of panel "
    f"growth over 6 books x 2 paths.")
mo = ST[ST.grain == "MONTH"]
h_stamp = bool(mo.med_CAGR.median() < 0.0005 and mo.med_Sharpe.median() < 0.005)
say(f"H_STAMP {'PASS' if h_stamp else 'FAIL'}: a MONTH stamp leaves median {mo.med_CAGR.median()*100:.4f}pp of CAGR "
    f"and {mo.med_Sharpe.median():.5f} of Sharpe open (max {mo.max_CAGR.max()*100:.4f}pp / {mo.max_Sharpe.max():.5f}).")
h_wf = bool(len(WF) and WF.within2x.mean() >= 0.5)
say(f"H_WF    {'PASS' if h_wf else 'FAIL'}: {int(WF.within2x.sum())}/{len(WF)} books have OOS drift within 2x of "
    f"their IS drift; spearman {rho:+.4f}.")
say("")
say("## PRICING THE PROPOSED PROTOCOL CLAUSE (proposed, NOT applied — rule 6)")
me_last = DR[(DR.window == "LAST 24m")]
say(f"     CHANNEL A (length), what a DAY stamp BUYS: the whole of it. Median UNSTAMPED error at one month of "
    f"panel growth is {dr.med_CAGR.median()*100:.4f}pp CAGR / {dr.med_Sharpe.median():.5f} Sharpe "
    f"({me_last.med_CAGR.median()*100:.4f}pp / {me_last.med_Sharpe.median():.5f} at today's panel length); "
    f"with the stamp it is exactly 0 (G3).")
say(f"     CHANNEL B (restatement), what NO date stamp buys: {RS.share.median():.2%} of shared cells differ at the "
    f"median revision, but the metric cost is {BC.dCAGR.abs().median()*100:.4f}pp CAGR / "
    f"{BC.dSharpe.abs().median():.5f} Sharpe on same-calendar revisions (max "
    f"{BC[BC.rev.isin(CC[CC.weekend_rows==0].rev)].dCAGR.abs().max()*100:.4f}pp) — a restated adjusted close "
    f"rescales a level series, and the book reads returns.")
say(f"     CHANNEL C (calendar/universe), what NO date stamp buys: up to "
    f"{CC.asis_dCAGR.abs().max()*100:.4f}pp CAGR / {CC.asis_dSharpe.abs().max():.5f} Sharpe at the SAME end date. "
    f"Only a file hash (or the committed panel itself) detects it.")
say(f"     Cost of the clause: one date + one 16-char hash per published number; the record carries an end-date on "
    f"{n_end}/{len(files)} files and any hash on {n_sha}/{len(files)} today.")
say("")
say(f"GATES {sum(g for _, g in gates)}/{len(gates)} PASS. runtime {time.time()-t0:.1f}s")
(OUT / f"{SLUG}.console.txt").write_text("\n".join(CONSOLE) + "\n")
