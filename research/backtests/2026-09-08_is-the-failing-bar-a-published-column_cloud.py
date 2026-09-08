#!/usr/bin/env python3
"""Idea 161 — is the FAILING BAR a published column?   (cloud lane, 2026-09-08)

QUESTION (QUEUE 161): idea 152 showed that a 4b near-miss failing DD or CAGR is closable on
the gross ladder (POS: DD margin -1.14 pp at m=0.75 closes at m<=0.70) while one failing
H1/H2/OOS is not at any gross (NONE's H2 moves 0.0087 over a 7x range against a 0.027 gap).
"Sweep the whole leaderboard's recorded near-misses, classify each by failing bar, and
measure what fraction of the DD/CAGR ones actually close on their own ladder.  If it is
near 1.0 the failing bar belongs in the leaderboard schema."

THE FIVE 4b BARS (PROTOCOL rule 4b, as the record stores them):
    H1     m_H1   = Sharpe(1st half)  - SPY Sharpe(1st half)      > 0
    H2     m_H2   = Sharpe(2nd half)  - SPY Sharpe(2nd half)      > 0
    SHARPE m_OOS  = the record's third Sharpe leg                 > 0
    DD     m_DD   = MaxDD - 0.60 * SPY MaxDD                      > 0   (both negative)
    CAGR   m_CAGR = CAGR  - 0.70 * SPY CAGR                       > 0
A NEAR-MISS is an arm-row that fails EXACTLY ONE of the five.

DESIGN
  PART A — CLASSIFICATION CENSUS of the record.  Every `research/backtests/*.grid.csv`
    carrying the five margin columns and a committed pass4b, behind a GATE: the five bars
    must reconstruct the committed verdict on EVERY row of the file or the file is rejected.
    Classify every failing row by its failing-bar set; report the near-miss population by
    class, panel, cost rung and parent file, with the margin sizes.
  PART B — THE CLOSURE TEST on REAL PRICES, because the record's `gross` column is a
    REALISED mean gross, not a dial: no recorded grid contains a reconstructible own-ladder
    (ledger committed).  So the ladder is built: 8 books (EW-all inside the 200d band x
    2 widths x 2 cadences, TOP-N momentum at n = 10/20/40, and an ungated control) x
    7 ABSOLUTE gross points 0.15..1.00 (a 6.7x range, no leverage, PROTOCOL rule 2) x
    3 panels (u56 / broad136 / SMALL439) x 3 cost rungs (0 / 10 / 25 bps) = 504 arm-rows,
    every one of which has its OWN 7-point ladder.  Classify each near-miss, then ask
    whether ANY other gross point on its own ladder passes 4b.

THE TWO TUNED PARAMETERS: the LADDER GRID (7 gross points, swept, all reported) and the
NEAR-MISS WIDTH (n_fail == 1; n_fail <= 2 reported as robustness).  Nothing else is tuned.

RULE 8: near-misses are classified and their closure measured on the IS window
(<= 2016-12-31) ONLY; the OOS window (2017-01-01..) is then read once and the same closure
question asked of it, so the transfer rate of an IS-window closure is reported, not assumed.

PROTOCOL: 10 bps anchor (0 and 25 bps also reported), next-day execution (engine), no
shorting, no leverage.  SURVIVORSHIP: universe_broad.json and the sub-$2B panel are CURRENT
constituents only (data/SMALL_PANEL_README.md) — read the closure fractions, not the levels.
Deterministic, standalone.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
Writes .console.txt, .census.csv.gz, .ledger.csv, .grid.csv, .closure.csv.
"""
from __future__ import annotations

import sys
from math import lgamma
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from baseline import band_state, load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_is-the-failing-bar-a-published-column_cloud"
OUT = ROOT / "research" / "backtests"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BARS = ["H1", "H2", "SHARPE", "DD", "CAGR"]
MARGIN_COL = {"H1": "m_H1", "H2": "m_H2", "SHARPE": "m_OOS", "DD": "m_DD", "CAGR": "m_CAGR"}

# TUNED PARAMETER 1: the ladder (absolute gross, no leverage), swept, every point reported
LADDER = [0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.00]
# TUNED PARAMETER 2: near-miss width
NEARMISS_K = 1                      # fails exactly one bar; k <= 2 reported alongside
RUNGS = [0.0, 10.0, 25.0]

LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def _lchoose(n, k):
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def sign_p(w, l):
    nz = w + l
    if nz == 0:
        return np.nan
    k = min(w, l)
    c = sum(np.exp(_lchoose(nz, i) - nz * np.log(2.0)) for i in range(0, k + 1))
    return float(min(1.0, 2.0 * c))


def wilson(k, n, z=1.96):
    """Wilson 95% interval for a closure fraction — the queue's threshold is 'near 1.0'."""
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ------------------------------------------------------------------ Part A: the record
def classify(fails: np.ndarray) -> str:
    """fails is a boolean row over BARS (True = that bar FAILS)."""
    s = [b for b, f in zip(BARS, fails) if f]
    if not s:
        return "PASS"
    return "+".join(s) if len(s) <= 2 else f"{len(s)}-bar"


def census():
    """Every grid carrying the five margins and a committed pass4b, behind the gate."""
    rows, ledger = [], []
    for f in sorted(OUT.glob("*.grid.csv")):
        if f.name.startswith(STEM):
            continue
        rec = dict(file=f.name, rows=0, status="")
        try:
            d = pd.read_csv(f)
        except Exception as e:
            rec["status"] = f"unreadable:{type(e).__name__}"
            ledger.append(rec)
            continue
        miss = [c for c in list(MARGIN_COL.values()) + ["pass4b"] if c not in d.columns]
        if miss:
            rec["status"] = "missing " + ",".join(miss[:3])
            ledger.append(rec)
            continue
        M = {b: pd.to_numeric(d[MARGIN_COL[b]], errors="coerce") for b in BARS}
        ok = np.ones(len(d), bool)
        for b in BARS:
            ok &= (M[b] > 0).to_numpy()
        committed = d["pass4b"].astype(str).str.lower().isin(["true", "1", "1.0", "yes"]).to_numpy()
        hits = int((ok == committed).sum())
        rec["rows"] = len(d)
        if hits != len(d):
            rec["status"] = f"GATE FAILED {hits}/{len(d)}"
            ledger.append(rec)
            continue
        rec["status"] = "ADMITTED"
        ledger.append(rec)
        F = np.column_stack([(M[b] <= 0).to_numpy() for b in BARS])
        for i in range(len(d)):
            r = dict(file=f.name, date=f.name[:10],
                     panel=str(d["panel"].iloc[i]) if "panel" in d.columns else "n/a",
                     rung=str(d["cost"].iloc[i]) if "cost" in d.columns else "n/a",
                     n_fail=int(F[i].sum()), cls=classify(F[i]), pass4b=bool(committed[i]))
            for b in BARS:
                r["fail_" + b] = bool(F[i, BARS.index(b)])
                r["m_" + b] = float(M[b].iloc[i])
            rows.append(r)
    return pd.DataFrame(rows), pd.DataFrame(ledger)


# ------------------------------------------------------------------ Part B: the ladder
def ew_band_weights(px, band, gross, gated=True):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0) if gated else ew


def topn_weights(px, n, gross):
    """The 2026-09-04 KEEP-4b shape: top-n by the scan composite, EQUAL weight, NO vol
    scaler, held only above the 200d MA."""
    s, above, _ = score(px, vol_scale=False)
    rank = s.where(above).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


BOOKS = ([("EWband0.00-W", dict(kind="band", band=0.00, freq="W")),
          ("EWband0.03-W", dict(kind="band", band=0.03, freq="W")),
          ("EWband0.00-M", dict(kind="band", band=0.00, freq="M")),
          ("EWband0.03-M", dict(kind="band", band=0.03, freq="M")),
          ("TOP10-W", dict(kind="topn", n=10, freq="W")),
          ("TOP20-W", dict(kind="topn", n=20, freq="W")),
          ("TOP40-W", dict(kind="topn", n=40, freq="W")),
          ("EWungated-W", dict(kind="ungated", freq="W"))])


def build_weights(univ, spec, gross):
    if spec["kind"] == "band":
        return ew_band_weights(univ, spec["band"], gross, gated=True)
    if spec["kind"] == "ungated":
        return ew_band_weights(univ, 0.0, gross, gated=False)
    return topn_weights(univ, spec["n"], gross)


def win_bars(r, spy, lo=None, hi=None):
    """The five 4b bars of a return series against SPY over the same window."""
    x = r.loc[lo:hi] if (lo or hi) else r
    s = spy.reindex(x.index).fillna(0.0)
    mx, ms = metrics(x), metrics(s)
    h = len(x) // 2
    xh = (metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"])
    sh = (metrics(s.iloc[:h])["Sharpe"], metrics(s.iloc[h:])["Sharpe"])
    m = dict(m_H1=xh[0] - sh[0], m_H2=xh[1] - sh[1], m_SHARPE=mx["Sharpe"] - ms["Sharpe"],
             m_DD=mx["MaxDD"] - 0.60 * ms["MaxDD"], m_CAGR=mx["CAGR"] - 0.70 * ms["CAGR"])
    fails = np.array([m["m_" + b] <= 0 for b in BARS])
    m.update(CAGR=mx["CAGR"], Sharpe=mx["Sharpe"], MaxDD=mx["MaxDD"], H1=xh[0], H2=xh[1],
             n_fail=int(fails.sum()), cls=classify(fails), pass4b=bool(~fails.any()))
    return m


def keep_4a(r, base, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    b = base.reindex(x.index).fillna(0.0)
    h = len(x) // 2
    return bool(metrics(x.iloc[:h])["Sharpe"] > metrics(b.iloc[:h])["Sharpe"]
                and metrics(x.iloc[h:])["Sharpe"] > metrics(b.iloc[h:])["Sharpe"]
                and metrics(x)["MaxDD"] >= metrics(b)["MaxDD"])


def load_panels():
    P = {"u56": load_universe(), "broad136": load_universe(broad=True)}
    small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["small439"] = small[[c for c in small.columns if c not in bad]]
    return P, len(bad)


def fresh_ladders(panels):
    rows, bench = [], {}
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        bench[pname] = dict(SPY=spy, V2=v2)
        univ = px.drop(columns=["SPY"], errors="ignore") if pname == "small439" else px
        for bname, spec in BOOKS:
            for g in LADDER:
                w = build_weights(univ, spec, g)
                res = backtest(px, w.reindex(columns=px.columns).fillna(0.0), cost_bps=0.0,
                               freq=spec["freq"])
                r0, to = res["returns"], res["turnover"]
                for c in RUNGS:
                    r = (r0 - to * c / 1e4).loc[start:]      # rung identity (idea 352)
                    row = dict(panel=pname, book=bname, gross=g, cost=c, freq=spec["freq"],
                               TO=float(to.loc[start:].mean() * 252))
                    for tag, kw in (("", {}), ("IS_", dict(hi=IS_END)),
                                    ("OOS_", dict(lo=OOS_START))):
                        b = win_bars(r, spy, **kw)
                        row.update({tag + k: v for k, v in b.items()})
                    row["pass4a"] = keep_4a(r, v2)
                    row["pass4a_oos"] = keep_4a(r, v2, lo=OOS_START)
                    rows.append(row)
    return pd.DataFrame(rows), bench


def closure(FG, prefix):
    """For every near-miss on the (panel, book, cost) ladder: does ANY other gross point on
    the SAME ladder pass 4b in the same window?"""
    out = []
    for (pn, bk, c), g in FG.groupby(["panel", "book", "cost"]):
        g = g.sort_values("gross")
        passes = g.loc[g[prefix + "pass4b"], "gross"].tolist()
        for _, r in g.iterrows():
            if int(r[prefix + "n_fail"]) == 0:
                continue
            others = [x for x in passes if x != r.gross]
            out.append(dict(panel=pn, book=bk, cost=c, gross=r.gross, window=prefix or "full",
                            n_fail=int(r[prefix + "n_fail"]), cls=r[prefix + "cls"],
                            closes=bool(others), closers=len(others),
                            closer_lo=min(others) if others else np.nan,
                            closer_hi=max(others) if others else np.nan,
                            margin=(float(r[prefix + "m_" + r[prefix + "cls"]])
                                    if r[prefix + "cls"] in BARS else np.nan),
                            **{"m_" + b: r[prefix + "m_" + b] for b in BARS}))
    return pd.DataFrame(out)


def closure_table(C, k=NEARMISS_K):
    nm = C[C.n_fail == k]
    out = []
    for cls, g in nm.groupby("cls"):
        lo, hi = wilson(int(g.closes.sum()), len(g))
        out.append(dict(cls=cls, n=len(g), closes=int(g.closes.sum()),
                        frac=g.closes.mean(), lo95=lo, hi95=hi,
                        med_margin=float(g.margin.median())))
    return pd.DataFrame(out).sort_values("n", ascending=False)


# ------------------------------------------------------------------ main
def main():
    say("=" * 100)
    say("IDEA 161 — is the FAILING BAR a published column?   (cloud, 2026-09-08)")
    say("=" * 100)
    say("Two tuned parameters: the LADDER GRID (7 absolute gross points, all reported) and the")
    say("NEAR-MISS WIDTH (n_fail == 1, with n_fail <= 2 reported alongside).")

    # ---------------- Part A
    say("\n\n## PART A — classification census of the record's 4b failures\n")
    CEN, LED = census()
    CEN.to_csv(OUT / f"{STEM}.census.csv.gz", index=False, compression="gzip")
    LED.to_csv(OUT / f"{STEM}.ledger.csv", index=False)
    adm = LED[LED.status == "ADMITTED"]
    say(f"  grid files scanned {len(LED)}; ADMITTED {len(adm)} ({int(adm.rows.sum())} arm-rows); "
        f"gate failures {int((LED.status.str.startswith('GATE')).sum())}; "
        f"missing the margin schema {int(LED.status.str.startswith('missing').sum())}")
    say("  GATE: the five bars must reconstruct the file's committed pass4b on EVERY row.")
    for _, r in LED[LED.status.str.startswith("GATE")].iterrows():
        say(f"    REJECTED {r.file}: {r.status}")
    say(f"  census rows {len(CEN)}; passing 4b {int(CEN.pass4b.sum())} "
        f"({CEN.pass4b.mean():.2%}); failing {int((~CEN.pass4b).sum())}")

    say("\n### How many failing bars does a failure fail?")
    vc = CEN[~CEN.pass4b].n_fail.value_counts().sort_index()
    for k, v in vc.items():
        say(f"  n_fail = {k}: {v:6d} rows ({v / max(1, int((~CEN.pass4b).sum())):6.2%} of failures)")
    say(f"  NEAR-MISSES (n_fail == 1): {int(vc.get(1, 0))} rows = "
        f"{vc.get(1, 0) / max(1, len(CEN)):.2%} of the whole census")

    say("\n### The near-miss population by FAILING BAR")
    nm = CEN[CEN.n_fail == 1]
    say("  bar       rows    share   median margin   |margin| p25/p75")
    for b in BARS:
        g = nm[nm.cls == b]
        if not len(g):
            say(f"  {b:8s} {0:6d}")
            continue
        m = g["m_" + b]
        say(f"  {b:8s} {len(g):6d} {len(g) / len(nm):8.1%}   {m.median():+12.4f}   "
            f"{m.quantile(.25):+.4f} / {m.quantile(.75):+.4f}")
    say("\n### Which bar fails MOST OFTEN overall (any n_fail)?")
    for b in BARS:
        f = CEN["fail_" + b]
        say(f"  {b:8s} fails in {int(f.sum()):6d} of {len(CEN)} rows ({f.mean():6.1%}); "
            f"is the SOLE failure in {int((nm.cls == b).sum()):5d}")
    say("\n### Near-misses per panel and per rung")
    for key in ("panel", "rung"):
        for k, g in CEN.groupby(key):
            g1 = g[g.n_fail == 1]
            dist = "; ".join(f"{b} {int((g1.cls == b).sum())}" for b in BARS)
            say(f"  {key}={str(k):10s} rows {len(g):6d}  near-misses {len(g1):5d}  [{dist}]")
    say("\n### Near-misses per parent file (top 12 by count)")
    t = (CEN[CEN.n_fail == 1].groupby("file").size().sort_values(ascending=False).head(12))
    for f, n in t.items():
        say(f"  {n:5d}  {f}")

    say("\n### LEDGER — why the record cannot answer the closure question itself")
    say("  The `gross` column in every admitted grid is a REALISED mean gross (e.g. 157 distinct")
    say("  values in 306 rows), not a ladder dial, and no admitted grid carries a book label")
    say("  crossed with a gross dial.  Reconstructible own-ladders in the record: 0 of "
        f"{len(adm)} files.  The closure fraction is therefore measured on fresh prices below.")

    # ---------------- Part B
    say("\n\n## PART B — the closure test on real prices: every arm gets its OWN 7-point ladder\n")
    panels, nbad = load_panels()
    for k, v in panels.items():
        say(f"  panel {k:9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    say(f"  SMALL439 = the sub-$2B panel less the {nbad} names with max 1d move >= 1.0.")
    say("  SURVIVORSHIP: the small panel and universe_broad.json are CURRENT constituents only")
    say("  (data/SMALL_PANEL_README.md) — read the closure fractions, not the levels.")
    say(f"  ladder (absolute gross, no leverage): {LADDER}  -> {LADDER[-1] / LADDER[0]:.1f}x range")
    say(f"  books: {[b for b, _ in BOOKS]}")
    FG, bench = fresh_ladders(panels)
    FG.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"  grid {len(FG)} arm-rows = {len(BOOKS)} books x {len(LADDER)} gross x "
        f"{len(panels)} panels x {len(RUNGS)} rungs; "
        f"{FG.groupby(['panel', 'book', 'cost']).ngroups} distinct ladders")

    say("\n### Benchmarks, freshly computed")
    for pn in panels:
        for lab, lo in (("full", None), ("OOS ", OOS_START)):
            s = bench[pn]["SPY"] if lo is None else bench[pn]["SPY"].loc[lo:]
            v = bench[pn]["V2"] if lo is None else bench[pn]["V2"].loc[lo:]
            ms, mv = metrics(s), metrics(v)
            say(f"  {pn:9s} {lab}  SPY {ms['CAGR']:7.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:7.2%}"
                f"   RULES v2@10bps {mv['CAGR']:7.2%} / {mv['Sharpe']:.4f} / {mv['MaxDD']:7.2%}"
                f"   [4b bars: CAGR >= {0.70 * ms['CAGR']:.2%}, MaxDD >= {0.60 * ms['MaxDD']:.2%}]")

    say("\n### 4b/4a pass counts over the whole fresh grid")
    say(f"  full window: 4b {int(FG.pass4b.sum())}/{len(FG)}   4a(v2) {int(FG.pass4a.sum())}/{len(FG)}"
        f"   BOTH {int((FG.pass4b & FG.pass4a).sum())}")
    say(f"  OOS window:  4b {int(FG.OOS_pass4b.sum())}/{len(FG)}   4a(v2) "
        f"{int(FG.pass4a_oos.sum())}/{len(FG)}   BOTH {int((FG.OOS_pass4b & FG.pass4a_oos).sum())}")
    say(f"  IS window:   4b {int(FG.IS_pass4b.sum())}/{len(FG)}")

    say("\n### THE QUEUE'S MEASUREMENT — closure fraction by failing bar, IS window "
        "(rule 8: classified and closed on IS only)")
    CI = closure(FG, "IS_")
    CF = closure(FG, "")
    CO = closure(FG, "OOS_")
    for w, C in (("IS", CI), ("full", CF), ("OOS", CO)):
        C["window"] = w
    ALL = pd.concat([CI, CF, CO], ignore_index=True)
    ALL.to_csv(OUT / f"{STEM}.closure.csv", index=False)
    for w, C in (("IS (<=2016)", CI), ("full sample", CF), ("OOS (2017..)", CO)):
        T = closure_table(C)
        say(f"\n  window = {w}   (near-miss = fails exactly 1 of 5 bars)")
        say("    failing bar   n   closes   fraction   95% CI          median margin")
        for _, r in T.iterrows():
            say(f"    {r.cls:10s} {int(r.n):4d}   {int(r.closes):4d}   {r.frac:7.1%}   "
                f"[{r.lo95:.2f}, {r.hi95:.2f}]   {r.med_margin:+.4f}")
        dd = T[T.cls.isin(["DD", "CAGR"])]
        oth = T[~T.cls.isin(["DD", "CAGR"])]
        nd, cd = int(dd.n.sum()), int(dd.closes.sum())
        no, co = int(oth.n.sum()), int(oth.closes.sum())
        lo1, hi1 = wilson(cd, nd)
        lo2, hi2 = wilson(co, no)
        say(f"    POOLED  DD/CAGR near-misses close {cd}/{nd} = {cd / max(1, nd):.1%} "
            f"[{lo1:.2f}, {hi1:.2f}]   |   H1/H2/SHARPE close {co}/{no} = "
            f"{co / max(1, no):.1%} [{lo2:.2f}, {hi2:.2f}]")

    say("\n### Robustness: near-miss width n_fail <= 2 (IS window)")
    nm2 = CI[CI.n_fail == 2]
    say(f"  n_fail == 2 rows {len(nm2)}; closure "
        f"{(nm2.closes.mean() if len(nm2) else float('nan')):.1%}")
    for cls, g in nm2.groupby("cls"):
        say(f"    {cls:14s} n {len(g):4d} closes {g.closes.mean():6.1%}")

    say("\n### WHERE ON THE LADDER a near-miss closes (IS window, n_fail == 1)")
    say("  failing bar   median closing gross   direction of the closer vs the failing point")
    for b in BARS:
        g = CI[(CI.n_fail == 1) & (CI.cls == b) & CI.closes]
        if not len(g):
            say(f"  {b:10s}  (no closures)")
            continue
        down = int((g.closer_lo < g.gross).sum())
        up = int((g.closer_hi > g.gross).sum())
        say(f"  {b:10s}  {float(np.nanmedian(g[['closer_lo', 'closer_hi']].mean(axis=1))):.2f}"
            f"                 DOWN-ladder closer in {down}/{len(g)}, UP-ladder in {up}/{len(g)}")

    say("\n### IS THE CLOSURE A LADDER PROPERTY RATHER THAN A NEAR-MISS PROPERTY?")
    for w, C, pref in (("IS", CI, "IS_"), ("full", CF, ""), ("OOS", CO, "OOS_")):
        L = FG.groupby(["panel", "book", "cost"])[pref + "pass4b"].sum()
        live = int((L > 0).sum())
        nm = C[C.n_fail == 1]
        idx = nm.set_index(["panel", "book", "cost"]).index
        on_live = L.reindex(idx).fillna(0).to_numpy() > 0
        say(f"  {w:5s}: ladders carrying at least one 4b PASS {live}/{len(L)}; near-misses "
            f"sitting on such a ladder {int(on_live.sum())}/{len(nm)}; closure GIVEN a live "
            f"ladder {nm.closes.to_numpy()[on_live].mean() if on_live.any() else float('nan'):.1%}, "
            f"given a dead ladder "
            f"{nm.closes.to_numpy()[~on_live].mean() if (~on_live).any() else float('nan'):.1%}")
    say("  -> a near-miss closes iff its own ladder contains a passing point; the failing bar")
    say("     says WHERE to look on the ladder (down for DD, up for CAGR), not WHETHER it closes.")

    say("\n### RULE 8 TRANSFER — does an IS-window closure still hold out of sample?")
    key = ["panel", "book", "cost", "gross"]
    j = CI[CI.n_fail == 1].merge(CO[key + ["closes", "n_fail", "cls"]],
                                 on=key, how="inner", suffixes=("_IS", "_OOS"))
    say(f"  IS-window near-misses matched into the OOS window: {len(j)}")
    for b in BARS:
        g = j[j.cls_IS == b]
        if not len(g):
            continue
        both = int((g.closes_IS & g.closes_OOS).sum())
        say(f"    {b:8s} n {len(g):4d}   closes IS {g.closes_IS.mean():6.1%}   "
            f"closes OOS too {both}/{int(g.closes_IS.sum())} = "
            f"{both / max(1, int(g.closes_IS.sum())):6.1%}   "
            f"(OOS still a near-miss in {int((g.n_fail_OOS == 1).sum())})")
    dd = j[j.cls_IS.isin(["DD", "CAGR"])]
    if len(dd):
        b_ = int((dd.closes_IS & dd.closes_OOS).sum())
        w, l = b_, int((dd.closes_IS & ~dd.closes_OOS).sum())
        say(f"  POOLED DD/CAGR: IS closures that also close OOS {b_}/{int(dd.closes_IS.sum())} "
            f"= {b_ / max(1, int(dd.closes_IS.sum())):.1%}  (sign p on hold-vs-break "
            f"{sign_p(w, l):.4f})")

    say("\n### THE DECISION the queue pre-registered ('near 1.0' -> the failing bar is a column)")
    T = closure_table(CI)
    def frac(c):
        r = T[T.cls == c]
        return (float(r.frac.iloc[0]), int(r.n.iloc[0])) if len(r) else (np.nan, 0)
    fdd, ndd = frac("DD")
    fcg, ncg = frac("CAGR")
    say(f"  DD near-misses close on their own ladder in {fdd:.1%} of {ndd}")
    say(f"  CAGR near-misses close on their own ladder in {fcg:.1%} of {ncg}")
    oth = T[~T.cls.isin(["DD", "CAGR"])]
    say(f"  H1/H2/SHARPE near-misses close in {oth.closes.sum()}/{int(oth.n.sum())} = "
        f"{oth.closes.sum() / max(1, int(oth.n.sum())):.1%}")

    say("\n### The books and rungs behind the near-misses (IS window)")
    for key2 in ("book", "cost", "panel"):
        for k, g in CI[CI.n_fail == 1].groupby(key2):
            say(f"  {key2}={str(k):14s} near-misses {len(g):4d}  closes {g.closes.mean():6.1%}  "
                f"[{'; '.join(f'{b} {int((g.cls == b).sum())}' for b in BARS)}]")

    say("\n### Arms clearing 4b on BOTH windows (for the record)")
    both = FG[FG.pass4b & FG.OOS_pass4b]
    say(f"  {len(both)} of {len(FG)}")
    if len(both):
        say(both.sort_values("OOS_Sharpe", ascending=False)
            .head(8)[["panel", "book", "gross", "cost", "CAGR", "Sharpe", "MaxDD",
                      "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    say(f"\nwrote {STEM}.console.txt / .census.csv.gz / .ledger.csv / .grid.csv / .closure.csv")


if __name__ == "__main__":
    main()
