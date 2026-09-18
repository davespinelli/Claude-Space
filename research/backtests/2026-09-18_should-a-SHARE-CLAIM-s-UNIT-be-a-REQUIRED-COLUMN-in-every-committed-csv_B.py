#!/usr/bin/env python3
"""
Idea 979 (lane B, 2026-09-18) — should a SHARE CLAIM's UNIT be a REQUIRED COLUMN in every
committed csv?

THE PREMISE, AND WHY THIS RUN IS NOT THE SEVEN SKIPS BEFORE IT.  Idea 973 had to INFER each
artifact's cell key from whichever of {panel, book, arm, gross, cadence, n/k, cost} it happened
to carry, and only 909 of 4,759 artifacts were eligible at all.  979 asked for a minimal schema
(a `unit` / `cell_key` column) and a costing of it.  Seven lanes in a row SKIPPED it on the
grounds that "there is no capital book to price, so it cannot carry the mandatory rule-8
walk-forward or either KEEP path".  Lane B's own 1265 correction says otherwise: a census CAN
carry a capital arm.  This run gives 979 one, and the arm is not decoration — it is the COSTING
the idea asked for, denominated in capital rather than in text.

  A committed row that reads "U56 / N=20 / gross 0.65 -> 4b PASS" and names no cadence and no
  rebalance phase does not identify ONE book.  It identifies a SET of books, every member of
  which an implementer reading that row could legitimately build.  The cost of the missing
  column is therefore not a bookkeeping inconvenience: it is the SPREAD of realised outcomes
  over that set, and the column is worth requiring exactly to the extent that the set straddles
  the 4b bar.  ARM A measures how often the record leaves that set open.  ARM B builds it.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  ARM A — THE CENSUS (mechanical, over committed headers, no prose parsed).  Every .csv /
      .csv.gz under research/ is read for its HEADER ONLY and scored for (i) whether it carries
      an explicit self-describing `unit` / `cell_key` / `key` column, and (ii) which of the
      eight capital-determining dials {panel, book/arm, n/k, gross, cadence, phase, cost, hold}
      it names.  Published in `.census.csv`.  The headline is the share of committed artifacts
      that name CADENCE and the share that name PHASE — ARM B's two dials, i.e. the two fields
      an implementer must guess.
  ARM B — THE COSTING (real books).  The record's standing certified book (idea 1295's rule-8
      pick: U56 / N=20 / gross 0.65 / sector cap 5) is rebuilt at EVERY point of the dial set
      that a cadence-and-phase-silent row leaves open, on three panels, with BOTH KEEP paths
      (rule 4) and both 4b margins at every cell.  48 books, ALL published in `.grid.csv`.
  ARM C — RULE 8.  Both dials chosen on warm-up..2016-12-31 ONLY by the chooser declared below;
      2017-2026 read ONCE; OOS CAGR / Sharpe / MaxDD against RULES v2 and SPY.  Published in
      `.walkforward.csv`.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) THE COLUMN IS LOAD-BEARING — the open set straddles the 4b bar on U56, i.e. a
        cadence-and-phase-silent row is consistent with both a PASS and a FAIL, and the schema
        column is worth requiring at a cost measurable in pp.
    (B) THE COLUMN IS COSMETIC — every member of the open set carries the same 4b verdict on
        every panel, so the missing field costs an implementer nothing in capital terms and the
        proposal should be REFUSED as unpriced overhead.
    (C) THE ROW WAS NEVER A CLAIM — the open set fails 4b nearly everywhere, i.e. the committed
        verdict is a property of one unnamed cell and not of the recipe.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4).  Both are chosen because ARM A measures them to be
the two most-often-unnamed capital-determining fields, NOT because they were tried and worked.

  CADENCE  {D, W, M, Q}                     (W = the incumbent's)
  PHASE p  {0, 1, 2, 3, 4} = rebalance on the p-th trading row BEFORE the period's last one
                                            (p = 0 = the incumbent's "last trading day of the
                                            period"; D has no phase, so p = 0 only)

  16 cells per panel (1 + 5 + 5 + 5), 48 in all, EVERY ONE PUBLISHED.

FROZEN, NOT DIALS: N = 20 names, sector cap = 5, gross = 0.65 (idea 1295's certified triple),
H = 126 min hold, decide-at-t / apply-at-t+1 (rule 2), 3-leg composite (21/252, 0/126, 0/63)
equal-ranked, above-200d and vol20 < 0.60 eligibility, 10 bps per unit turnover (rule 2),
260-row warm-up, first-wins stable tie-break, equal weights inside the book, un-invested weight
in cash at 0%.  COST IS NOT A DIAL HERE: PROTOCOL rule 2 fixes it at 10 bps, so a silent row is
not silent about cost — the protocol names it.  That is the point of the proposal.

THE SECTOR GROUPING IS CONSTRUCTION, NOT A DIAL, AND IT IS POINT-IN-TIME — idea 1289's
convention, reused byte-for-byte via the same argmax-correlation rule so this run is comparable
to 1289 / 1295.  Each investable name is assigned to whichever of NINE sector ETFs (XLK, XLF,
XLV, XLE, XLI, XLY, XLP, XLU, XLB) its daily returns correlate with most over THE FIRST 252
TRADING DAYS OF ITS OWN HISTORY; a name is UNCLASSIFIED and cap-exempt until its own first 252
days have elapsed, so no assignment uses data from after the day it is first applied.

THE ANCHOR.  (U56, W, p=0) must reproduce idea 1295's committed pick (13.76% / 1.2116 /
-19.06%, OOS 14.60% / 1.2261) to within 5e-4.  It is reported as a CHECK, not a result; a
failure to reproduce it invalidates every number below and the run says so.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  On the IS window
(warm-up .. 2016-12-31) only, per panel: among cells clearing the IS analogues of 4b's three
non-half legs (Sharpe > SPY, MaxDD >= 0.60 x SPY MaxDD, CAGR >= 0.70 x SPY CAGR), take the
highest IS joint margin J = min(IS DD margin, IS CAGR margin); ties to the SLOWER cadence
(Q < M < W < D), then to the LOWER phase.  J rather than IS Sharpe because idea 1290 showed IS
Sharpe cannot size a book.  If that set is empty the declared fallback is the highest IS J over
the whole grid, and the run says the strict set was empty.  Then 2017-2026 is read ONCE.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists and SMALL is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).
Delisted, acquired and bankrupt names are absent from all three, which flatters every momentum
book here and the drawdown leg specifically.  Every claim below is a WITHIN-GRID difference on
fixed panels and identical dates, so the survivorship bias is common to all 48 cells and cannot
manufacture the SPREAD that is this run's object — but it does mean no cell's level is a live
expectancy.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell; rule 8 walk-forward
with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_should-a-SHARE-CLAIM-s-UNIT-be-a-REQUIRED-COLUMN-in-every-committed-csv_B.py
"""
from __future__ import annotations

import gzip
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest  # noqa: E402

OUT = Path(str(Path(__file__))[:-3])
WARMUP, MAXVOL, REF_COST, LAG = 260, 0.60, 10.0, 1
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_CAP, A_GROSS = 20, 126, 5, 0.65          # idea 1295's certified triple, frozen
CADENCES = ["D", "W", "M", "Q"]                      # dial 1
PHASES = [0, 1, 2, 3, 4]                             # dial 2
SECTORS = ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB"]
CLASSIFY_DAYS = 252
OOS_START = pd.Timestamp("2017-01-01")
CAD_ORDER = {"Q": 0, "M": 1, "W": 2, "D": 3}          # tie-break: slower cadence wins
ANCHOR = dict(CAGR=0.1376, Sharpe=1.2116, MaxDD=-0.1906, OOS_CAGR=0.1460, OOS_Sharpe=1.2261)

# ---- ARM A vocabulary: the eight capital-determining dials, and the self-describing columns.
SELFDESC = ("unit", "cell_key", "cellkey", "key")
DIALS = {
    "panel":   ("panel", "uni", "universe", "pool"),
    "book":    ("book", "arm", "rule", "strategy", "variant", "template"),
    "n":       ("n", "k", "topn", "n_names", "nk", "width", "breadth"),
    "gross":   ("gross", "g", "exposure", "lev"),
    "cadence": ("cadence", "freq", "step", "rebal", "rebalance", "cad"),
    "phase":   ("phase", "offset", "dom", "weekday", "dow", "delay", "lag"),
    "cost":    ("cost", "cost_bps", "bps", "fee"),
    "hold":    ("hold", "h", "minhold", "min_hold", "holding"),
}

_LOG: list[str] = []


def say(s=""):
    print(s)
    _LOG.append(s)


# ------------------------------------------------------------------ ARM A: the census
def header_of(p: Path):
    try:
        op = gzip.open if p.suffix == ".gz" else open
        with op(p, "rt", errors="replace") as fh:
            line = fh.readline()
        if not line.strip():
            return None
        return [c.strip().strip('"').lower() for c in line.rstrip("\n").split(",")]
    except Exception:
        return None


def census():
    files = sorted(list(ROOT.joinpath("research").rglob("*.csv"))
                   + list(ROOT.joinpath("research").rglob("*.csv.gz")))
    rows = []
    for p in files:
        cols = header_of(p)
        if cols is None:
            rows.append(dict(path=str(p.relative_to(ROOT)), readable=False, selfdesc=False,
                             ncols=0, **{f"has_{d}": False for d in DIALS}))
            continue
        cs = set(cols)
        rec = dict(path=str(p.relative_to(ROOT)), readable=True,
                   selfdesc=any(s in cs for s in SELFDESC), ncols=len(cols))
        for d, alia in DIALS.items():
            rec[f"has_{d}"] = any(a in cs for a in alia)
        rows.append(rec)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ mechanics (ideas 1289/1295)
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])


def sector_returns(idx):
    px = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    return px[SECTORS].reindex(idx, method="ffill").pct_change()


def classify(pan):
    """Point-in-time group per investable name — idea 1289's convention, unchanged."""
    S = sector_returns(pan.idx).values
    T, K = len(pan.idx), len(pan.iinv)
    grp = np.full(K, -1, dtype=np.int64)
    ready = np.full(K, T, dtype=np.int64)
    for k, ci in enumerate(pan.iinv):
        r = pan.px.iloc[:, ci].pct_change().values
        ok = np.flatnonzero(np.isfinite(r) & (pan.priced[:, ci]))
        ok = ok[ok > 0]
        if len(ok) < CLASSIFY_DAYS:
            continue
        w = ok[:CLASSIFY_DAYS]
        ready[k] = int(w[-1]) + 1
        x = r[w]
        best, bg = -np.inf, -1
        for g in range(len(SECTORS)):
            y = S[w, g]
            m = np.isfinite(x) & np.isfinite(y)
            if m.sum() < 60:
                continue
            xs, ys = x[m] - x[m].mean(), y[m] - y[m].mean()
            den = np.sqrt((xs * xs).sum() * (ys * ys).sum())
            if den <= 0:
                continue
            c = float((xs * ys).sum() / den)
            if c > best:
                best, bg = c, g
        grp[k] = bg
        if bg < 0:
            ready[k] = T
    return grp, ready


def decision_rows(idx, cad, p):
    """Decision rows for cadence `cad` at phase `p`: the p-th trading row BEFORE the period's
    last one.  p = 0 reproduces the record's 'last trading day of the period' convention.
    Cadence D has no phase and returns every row."""
    if cad == "D":
        return np.arange(len(idx))
    per = idx.to_period({"W": "W", "M": "M", "Q": "Q"}[cad])
    pos = pd.Series(np.arange(len(idx)), index=per)
    out = []
    for _, v in pos.groupby(level=0):
        a = v.values
        out.append(int(a[max(len(a) - 1 - p, 0)]))
    return np.array(sorted(set(out)), dtype=np.int64)


def build(pan, dec, N, cap, grp, ready):
    """Unit-gross min-hold top-N frame with at most `cap` names per sector group, decided on
    rows `dec` and applied LAG rows later (rule 2).  Returns the frame and the application rows."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = dec + LAG
    keep_m = app < T
    dec, app = dec[keep_m], app[keep_m]
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    ng = int(grp.max()) + 1 if (grp >= 0).any() else 1
    for i, t in enumerate(app):
        ts = dec[i]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < A_H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        cnt = np.zeros(ng, dtype=np.int64)
        for c in keep:
            if grp[c] >= 0 and t >= ready[c]:
                cnt[grp[c]] += 1
        ks = set(keep)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in ks:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if len(take) >= need or not np.isfinite(k[c]):
                    break
                c = int(c)
                gg = grp[c] if t >= ready[c] else -1
                if gg >= 0 and cnt[gg] >= cap:
                    continue
                take.append(c)
                if gg >= 0:
                    cnt[gg] += 1
        new = np.full(K, -1, dtype=np.int64)
        for c in ks:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = app[i + 1] if i + 1 < len(app) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, app


def nrun(pan, Wt, app):
    rets, Cp = pan.rets, pan.Cp
    T, M = rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    app = np.asarray(app, dtype=np.int64)
    ends = np.append(app[1:], T)
    for i0, i1 in zip(app, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        curw = held[i1 - 1]
    nm = (Wt > 0).sum(axis=1).astype(float)
    return (held * rets).sum(axis=1), turn, nm


def at_cost(gr, turn, c):
    return gr - turn * c / 1e4


# ------------------------------------------------------------------ metrics (ideas 1290/1295)
def mt(r):
    r = np.asarray(r, dtype=float)
    if len(r) < 20:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(r.std(ddof=1) * np.sqrt(252))
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1.0),
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd)


def windows(idx):
    n = len(idx)
    h = n // 2
    h1 = np.zeros(n, bool); h1[:h] = True
    h2 = np.zeros(n, bool); h2[h:] = True
    oos = np.asarray(idx >= OOS_START)
    return h1, h2, ~oos, oos


def legs(r, spy, live, idx):
    h1, h2, ins, oos = windows(idx)
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[h1]), mt(r[h2])
    s1, s2 = mt(spy[h1]), mt(spy[h2])
    l1, l2 = mt(live[h1]), mt(live[h2])
    Ro, So = mt(r[oos]), mt(spy[oos])
    Ri, Si = mt(r[ins]), mt(spy[ins])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"], b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    dd_m = 100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"])
    cg_m = 100.0 * (R["CAGR"] - 0.70 * S["CAGR"])
    is_dd = 100.0 * (Ri["MaxDD"] - 0.60 * Si["MaxDD"])
    is_cg = 100.0 * (Ri["CAGR"] - 0.70 * Si["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], IS_Sharpe=Ri["Sharpe"], IS_CAGR=Ri["CAGR"],
                IS_MaxDD=Ri["MaxDD"], OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"],
                OOS_MaxDD=Ro["MaxDD"], dd_margin_pp=dd_m, cagr_margin_pp=cg_m,
                J=min(dd_m, cg_m), IS_J=min(is_dd, is_cg),
                is_b_sh=bool(Ri["Sharpe"] > Si["Sharpe"]), is_b_dd=bool(is_dd >= 0.0),
                is_b_cagr=bool(is_cg >= 0.0),
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


def make_panels():
    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    n_drop = len([c for c in pxS.columns if c != "SPY" and c in bad])
    return ([Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
             Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
             Panel("SMALL", pxS, inv)], n_drop)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 979 (lane B, 2026-09-18) — should a SHARE CLAIM's UNIT be a REQUIRED COLUMN in")
    say("every committed csv?  Costed in CAPITAL, not in text.")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): CADENCE {CADENCES} x PHASE {PHASES} = 16 cells/panel, 48 published.")
    say(f"  FROZEN (idea 1295's certified triple): N={A_N}, sector cap={A_CAP}, gross={A_GROSS},")
    say(f"          H={A_H}, t+1, {REF_COST:.0f} bps, above-200d & vol20<0.60, equal weights, cash 0%.")
    say("  OUTCOMES: (A) COLUMN LOAD-BEARING  (B) COLUMN COSMETIC  (C) ROW WAS NEVER A CLAIM.")
    say("")

    # ------------------------------------------------------------- ARM A
    say("=" * 100)
    say("ARM A — THE CENSUS.  Header-only scan of every committed csv under research/.")
    say("=" * 100)
    say("")
    cen = census()
    cen.to_csv(f"{OUT}.census.csv", index=False)
    tot = len(cen)
    rd = cen[cen["readable"]]
    say(f"  {tot} csv artifacts found; {len(rd)} readable headers; {tot - len(rd)} unreadable.")
    say(f"  SELF-DESCRIBING (a `unit` / `cell_key` / `key` column): "
        f"{int(rd['selfdesc'].sum())} of {len(rd)} ({rd['selfdesc'].mean():.2%}).")
    say("")
    say(f"  {'dial':10} {'files naming it':>16} {'share':>9}")
    for d in DIALS:
        n = int(rd[f"has_{d}"].sum())
        say(f"  {d:10} {n:16d} {n / max(len(rd), 1):9.2%}")
    say("")
    full = rd[[f"has_{d}" for d in DIALS]].all(axis=1)
    both = rd["has_cadence"] & rd["has_phase"]
    say(f"  Naming ALL EIGHT dials: {int(full.sum())} of {len(rd)} ({full.mean():.2%}).")
    say(f"  Naming BOTH of this run's dials (cadence AND phase): {int(both.sum())} "
        f"({both.mean():.2%}).")
    say(f"  Naming NEITHER: {int((~rd['has_cadence'] & ~rd['has_phase']).sum())} "
        f"({(~rd['has_cadence'] & ~rd['has_phase']).mean():.2%}).")
    say("")
    say("  => CADENCE and PHASE are the two most-often-unnamed capital-determining fields, which")
    say("     is why ARM B opens exactly those two and no others.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY = benchmark only.")
    say("")

    say("=" * 100)
    say("ARM B.0 — BENCHMARKS (post-warm-up, 10 bps, weekly for the live book)")
    say("=" * 100)
    say("")
    B = {}
    say(f"  {'panel':6} {'series':22} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8}")
    for pan in panels:
        spy = pan.spy[WARMUP:]
        live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST,
                        freq="W")["returns"].values[WARMUP:]
        idx = pan.idx[WARMUP:]
        h1, h2, _, oos = windows(idx)
        B[pan.name] = dict(spy=spy, live=live, idx=idx)
        for tag, ser in (("SPY (buy & hold)", spy), ("RULES v2 (live book)", live)):
            m, mo = mt(ser), mt(ser[oos])
            say(f"  {pan.name:6} {tag:22} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(ser[h1])['Sharpe']:7.4f} {mt(ser[h2])['Sharpe']:7.4f} {mo['CAGR']:9.2%} "
                f"{mo['Sharpe']:8.4f} {mo['MaxDD']:8.2%}")
    say("")

    # ------------------------------------------------------------- ARM B: the grid
    say("=" * 100)
    say("ARM B — THE OPEN SET.  Every (cadence, phase) a silent row permits. ALL 48 CELLS.")
    say("=" * 100)
    say("")
    rows = []
    for pan in panels:
        spy, live, idx = B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["idx"]
        grp, ready = classify(pan)
        nunc = int((grp < 0).sum())
        say(f"  {pan.name}: {len(grp) - nunc} of {len(grp)} names classified; {nunc} never.")
        for cad in CADENCES:
            ph = [0] if cad == "D" else PHASES
            for p in ph:
                dec = decision_rows(pan.idx, cad, p)
                W1, app = build(pan, dec, A_N, A_CAP, grp, ready)
                gr, turn, nm = nrun(pan, W1 * A_GROSS, app)
                r = at_cost(gr, turn, REF_COST)[WARMUP:]
                d = legs(r, spy, live, idx)
                yrs = len(r) / 252.0
                d.update(panel=pan.name, cadence=cad, phase=p,
                         turns_yr=float(turn[WARMUP:].sum() / yrs) * A_GROSS,
                         names=float(nm[WARMUP:][nm[WARMUP:] > 0].mean()))
                rows.append(d)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    say("")

    say(f"  {'panel':6} {'cad':4} {'ph':>3} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} "
        f"{'H2':>7} {'OOS CAGR':>9} {'OOS Sh':>8} {'ddM pp':>8} {'cgM pp':>8} {'J pp':>8} "
        f"{'4a':>3} {'4b':>3} {'trn/yr':>7}")
    for _, x in G.iterrows():
        say(f"  {x['panel']:6} {x['cadence']:4} {int(x['phase']):3d} {x['CAGR']:8.2%} "
            f"{x['Sharpe']:8.4f} {x['MaxDD']:8.2%} {x['H1']:7.4f} {x['H2']:7.4f} "
            f"{x['OOS_CAGR']:9.2%} {x['OOS_Sharpe']:8.4f} {x['dd_margin_pp']:8.2f} "
            f"{x['cagr_margin_pp']:8.2f} {x['J']:8.2f} "
            f"{'Y' if x['pass4a'] else '.':>3} {'Y' if x['pass4b'] else '.':>3} {x['turns_yr']:7.2f}")
    say("")

    # ------------------------------------------------------------- the anchor check
    say("-" * 100)
    say("ANCHOR CHECK — (U56, W, p=0) against idea 1295's committed rule-8 pick.")
    say("-" * 100)
    a = G[(G["panel"] == "U56") & (G["cadence"] == "W") & (G["phase"] == 0)].iloc[0]
    worst = 0.0
    for k, v in ANCHOR.items():
        d = abs(float(a[k]) - v)
        worst = max(worst, d)
        say(f"  {k:12} here {float(a[k]):9.4f}   committed {v:9.4f}   |d| {d:.2e}")
    ok = worst <= 5e-4
    say(f"  max |d| = {worst:.2e} -> {'REPRODUCED' if ok else 'DID NOT REPRODUCE'} at the 5e-4 bar.")
    if not ok:
        say("  *** ANCHOR FAILED. Every number in this run is suspect and no verdict is published. ***")
    say("")

    # ------------------------------------------------------------- the spread
    say("=" * 100)
    say("ARM B.1 — WHAT THE MISSING COLUMN COSTS: the SPREAD over the open set, per panel.")
    say("=" * 100)
    say("")
    say(f"  {'panel':6} {'cells':>6} {'4b pass':>8} {'4a pass':>8} {'Sharpe range':>22} "
        f"{'MaxDD range':>22} {'CAGR range':>22} {'J range pp':>18}")
    spread_rows = []
    for pn in ("U56", "B136", "SMALL"):
        g = G[G["panel"] == pn]
        s = dict(panel=pn, cells=len(g), n4b=int(g["pass4b"].sum()), n4a=int(g["pass4a"].sum()),
                 sh_lo=g["Sharpe"].min(), sh_hi=g["Sharpe"].max(),
                 dd_lo=g["MaxDD"].min(), dd_hi=g["MaxDD"].max(),
                 cg_lo=g["CAGR"].min(), cg_hi=g["CAGR"].max(),
                 J_lo=g["J"].min(), J_hi=g["J"].max())
        spread_rows.append(s)
        say(f"  {pn:6} {len(g):6d} {s['n4b']:8d} {s['n4a']:8d} "
            f"{s['sh_lo']:10.4f}..{s['sh_hi']:<10.4f} {s['dd_lo']:10.2%}..{s['dd_hi']:<10.2%} "
            f"{s['cg_lo']:10.2%}..{s['cg_hi']:<10.2%} {s['J_lo']:8.2f}..{s['J_hi']:<8.2f}")
    pd.DataFrame(spread_rows).to_csv(f"{OUT}.spread.csv", index=False)
    say("")
    say("  WITHIN the incumbent's OWN cadence (W), i.e. the spread a row that names cadence but")
    say("  NOT phase still leaves open:")
    say(f"  {'panel':6} {'cells':>6} {'4b pass':>8} {'Sharpe range':>22} {'MaxDD range':>22} "
        f"{'J range pp':>18}")
    for pn in ("U56", "B136", "SMALL"):
        g = G[(G["panel"] == pn) & (G["cadence"] == "W")]
        say(f"  {pn:6} {len(g):6d} {int(g['pass4b'].sum()):8d} "
            f"{g['Sharpe'].min():10.4f}..{g['Sharpe'].max():<10.4f} "
            f"{g['MaxDD'].min():10.2%}..{g['MaxDD'].max():<10.2%} "
            f"{g['J'].min():8.2f}..{g['J'].max():<8.2f}")
    say("")

    # ------------------------------------------------------------- binding legs
    say("  BINDING LEGS over the 48 cells (4b failures only):")
    f = G[~G["pass4b"]]
    for lg, lab in (("b_h1", "H1 Sharpe > SPY"), ("b_h2", "H2 Sharpe > SPY"),
                    ("b_oos", "OOS Sharpe > SPY"), ("b_dd", "MaxDD >= 0.60 x SPY"),
                    ("b_cagr", "CAGR >= 0.70 x SPY")):
        n = int((~f[lg]).sum())
        sole = int(((~f[lg]) & (f[[c for c in ("b_h1", "b_h2", "b_oos", "b_dd", "b_cagr")
                                   if c != lg]].all(axis=1))).sum())
        say(f"    {lab:24} binds {n:3d} of {len(f)} failures, SOLE binder {sole:3d}")
    say(f"    4a passes {int(G['pass4a'].sum())} of {len(G)} cells.")
    say("")

    # ------------------------------------------------------------- ARM C: rule 8
    say("=" * 100)
    say("ARM C — RULE 8.  Both dials chosen on warm-up..2016 ONLY; 2017-2026 read ONCE.")
    say("=" * 100)
    say("")
    wf = []
    for pn in ("U56", "B136", "SMALL"):
        g = G[G["panel"] == pn].copy()
        strict = g[g["is_b_sh"] & g["is_b_dd"] & g["is_b_cagr"]]
        used_fb = len(strict) == 0
        pool = g if used_fb else strict
        pool = pool.assign(_c=pool["cadence"].map(CAD_ORDER))
        pool = pool.sort_values(["IS_J", "_c", "phase"], ascending=[False, True, True])
        pick = pool.iloc[0]
        spy, live, idx = B[pn]["spy"], B[pn]["live"], B[pn]["idx"]
        _, _, _, oos = windows(idx)
        so, lo = mt(spy[oos]), mt(live[oos])
        say(f"  {pn}: strict IS set has {len(strict)} of {len(g)} cells"
            f"{'  -> EMPTY, declared fallback used' if used_fb else ''}.")
        say(f"     PICK  cadence={pick['cadence']}  phase={int(pick['phase'])}   (IS J "
            f"{pick['IS_J']:.2f} pp, IS Sharpe {pick['IS_Sharpe']:.4f})")
        say(f"     FULL  {pick['CAGR']:7.2%} / {pick['Sharpe']:.4f} / {pick['MaxDD']:7.2%}   "
            f"halves {pick['H1']:.4f} / {pick['H2']:.4f}   4a {'Y' if pick['pass4a'] else 'N'}  "
            f"4b {'Y' if pick['pass4b'] else 'N'}")
        say(f"     OOS   {pick['OOS_CAGR']:7.2%} / {pick['OOS_Sharpe']:.4f} / "
            f"{pick['OOS_MaxDD']:7.2%}")
        say(f"     OOS SPY      {so['CAGR']:7.2%} / {so['Sharpe']:.4f} / {so['MaxDD']:7.2%}")
        say(f"     OOS RULES v2 {lo['CAGR']:7.2%} / {lo['Sharpe']:.4f} / {lo['MaxDD']:7.2%}")
        # what a silent row would have handed an implementer instead
        say(f"     IF THE ROW HAD BEEN SILENT: the implementer draws uniformly from {len(g)} "
            f"cells; {int(g['pass4b'].sum())} clear 4b "
            f"({g['pass4b'].mean():.1%}), OOS Sharpe {g['OOS_Sharpe'].min():.4f}.."
            f"{g['OOS_Sharpe'].max():.4f}.")
        wf.append(dict(panel=pn, strict_cells=len(strict), fallback=used_fb,
                       pick_cadence=pick["cadence"], pick_phase=int(pick["phase"]),
                       IS_J=pick["IS_J"], IS_Sharpe=pick["IS_Sharpe"], CAGR=pick["CAGR"],
                       Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"], H1=pick["H1"], H2=pick["H2"],
                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                       OOS_MaxDD=pick["OOS_MaxDD"], pass4a=bool(pick["pass4a"]),
                       pass4b=bool(pick["pass4b"]), spy_oos_CAGR=so["CAGR"],
                       spy_oos_Sharpe=so["Sharpe"], spy_oos_MaxDD=so["MaxDD"],
                       live_oos_CAGR=lo["CAGR"], live_oos_Sharpe=lo["Sharpe"],
                       live_oos_MaxDD=lo["MaxDD"],
                       silent_4b_rate=float(g["pass4b"].mean()),
                       silent_oos_sh_lo=float(g["OOS_Sharpe"].min()),
                       silent_oos_sh_hi=float(g["OOS_Sharpe"].max())))
        say("")
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------- verdict
    say("=" * 100)
    say("VERDICT")
    say("=" * 100)
    say("")
    u = G[G["panel"] == "U56"]
    straddles = bool(u["pass4b"].any() and (~u["pass4b"]).any())
    allsame = all(G[G["panel"] == pn]["pass4b"].nunique() == 1 for pn in ("U56", "B136", "SMALL"))
    if not ok:
        out = "VOID — anchor did not reproduce"
    elif straddles:
        out = "(A) THE COLUMN IS LOAD-BEARING"
    elif allsame:
        out = "(B) THE COLUMN IS COSMETIC"
    else:
        out = "(C) mixed / the row was never a claim"
    say(f"  OUTCOME: {out}")
    say(f"  U56 open set: {int(u['pass4b'].sum())} of {len(u)} cells clear 4b; "
        f"Sharpe {u['Sharpe'].min():.4f}..{u['Sharpe'].max():.4f}, "
        f"MaxDD {u['MaxDD'].min():.2%}..{u['MaxDD'].max():.2%}, "
        f"J {u['J'].min():.2f}..{u['J'].max():.2f} pp.")
    say(f"  4a passes {int(G['pass4a'].sum())} of {len(G)} cells across all three panels.")
    say("")
    say("  NOT CLAIMED: that cadence and phase are the ONLY unnamed fields (ARM A lists eight and")
    say("  measures all of them); that the proposed column would fix claims made before it exists;")
    say("  that any cell here is a new candidate book (the recipe is 1295's, frozen, not re-tuned);")
    say("  that anything changes in RULES.md (rule 6).")
    say("")
    say(f"  SURVIVORSHIP (rule 9): current constituents only on all three panels. Every number")
    say("  above is a WITHIN-GRID difference on fixed panels and identical dates.")
    say("")
    say(f"  [{time.time() - t0:.1f}s]  wrote {OUT.name}.census.csv / .grid.csv / .spread.csv / "
        ".walkforward.csv / .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
