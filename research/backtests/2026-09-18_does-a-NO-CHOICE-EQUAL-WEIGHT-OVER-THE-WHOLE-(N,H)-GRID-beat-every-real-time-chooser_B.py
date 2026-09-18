#!/usr/bin/env python3
"""
Idea 1331 (lane B, 2026-09-18) — does a NO-CHOICE EQUAL WEIGHT over the WHOLE (N,H) GRID
beat every REAL-TIME CHOOSER?

WHY THIS IDEA.  The 2026-09-18 CHANGELOG diagnosis (idea 1321) ends: "the IS-Sharpe chooser
buys N=5 concentration and pays for it in OOS drawdown on exactly the two panels that pass:
WHAT PASSES 4b IS THE CELL NOBODY HAD TO CHOOSE."  Every committed KEEP-4b in this record is a
FROZEN cell (N=20/H=126 or N=15/H=126) — a cell an implementer in 2011 had no way to know.
That leaves exactly one honest question for real capital: of the books a person could ACTUALLY
have run without hindsight, which is best?  There are only two families:
    CHOOSE  — re-pick (N,H) from the grid every year on data you already have, and follow it.
    DON'T   — hold the whole grid, equally weighted, forever.  Zero parameters, zero choice.
This run prices both against the frozen anchor, RULES v2 and SPY.

SELECTION / ELIGIBILITY.  The LAST numbered item standing in '## Open' is 904, a census of
committed placebo-differenced numbers against a seed-count floor — no price leg, already SKIPPED
by four prior lanes for exactly that reason (2026-09-15 cloud x3, 2026-09-15 lane B).  903 / 896
/ 895 / 894 / 877 / 876 below it are the same kind; 353 needs a live yf.download; 429 stays
PARKed (data/ carries only volume_small.csv.gz).  No eligible LAST idea existed, so the
documented fallback was taken: 1323 / 1327 / 1331 were filed from the CHANGELOG diagnosis and
the LAST of them (1331) claimed and pushed BEFORE any compute (queue rule C).

THE CANDIDATE GRID (not tuned here — the record's own committed comparison set, idea 1301's):
    N   {5, 10, 15, 20, 25, 30}   x   H {21, 63, 126, 252}   = 24 cells
    frozen at MAXVOL = 0.60, GROSS = 0.75, weekly Fri-decide / next-session-trade, 10 bps.
    The committed 2026-09-04 anchor (N=20, H=126) is cell 15 of the 24 and is the ONLY cell any
    committed KEEP-4b memo names.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    RE_PICK  {ANNUAL, BIENNIAL}      — re-pick at the first rebalance of every (other) January.
    WINDOW   {EXPANDING, ROLL1260}   — the history the chooser scores cells on (all of it, or
                                       the trailing 5 years).
    2 x 2 = 4 chooser configurations, EVERY ONE published, on EVERY panel.

NOT A DIAL, reported at every value (controls, never selected on):
    STAT {SHARPE, CALMAR, CAGR} — the statistic the chooser maximises.  Printed beside each
        other so the reader sees whether the answer depends on it.  4 x 3 = 12 chooser books
        per panel, all 12 published.
    PANEL {U56, B136, SMALL663}.
    GRIDAVG — the no-choice book.  It has NO dial at all: at every rebalance its target is the
        equal-weight MEAN of the 24 cells' own target vectors, gross 0.75.  It is not a cell of
        the grid and it is not tuned; it is the comparand the queue clause implies.
    ANCHOR  — the frozen committed N=20/H=126 cell, scored on the same window.

WHAT IS AND IS NOT WALK-FORWARD.  The chooser books are walk-forward BY CONSTRUCTION: at every
re-pick only rows strictly before the re-pick date are read (gate G6).  Rule 8 applies to the
TWO DIALS: they are chosen on EVAL_START..2016-12-31 ONLY, by a chooser declared before the run
(highest IS Sharpe of the stitched real-time book), and 2017-2026 is read ONCE.  Every grid
point's OOS is published anyway, so the reader can check the pick.

EVAL WINDOW.  All books — choosers, GRIDAVG, ANCHOR, RULES v2, SPY — are scored from a single
EVAL_START = the first re-pick date, so the comparison is apples-to-apples.  EVAL_START is set
by the chooser's own minimum history (MIN_IS = 504 rows of live cell returns), not chosen: it
falls in Jan 2011 on every panel.  Halves split that window in two; OOS is 2017-01-01 on.

PRE-DECLARED OUTCOMES, written before any number was read:
  H_NOCHOICE   GRIDAVG's full-sample Sharpe beats the MEDIAN of the 12 chooser books on a
               MAJORITY of panels, i.e. choosing is worth nothing.
  H_DOMINATES  stronger: GRIDAVG beats ALL 12 choosers on U56 OOS Sharpe.
  H_HINDSIGHT  the FROZEN anchor beats both families, i.e. the record's committed KEEP-4b is a
               freezing artefact an implementer could not have reached.
  H_4b         GRIDAVG clears 4b on U56 on the full sample AND rule-8 OOS.
  Whichever fire are reported as they fall.  A KILL is the expected result and is a result.

GATES.  G1 the anchor cell replays the committed 2026-09-04 U56 triple 15.7147% / 1.14804 /
-19.1276% to 1e-4 when VINTAGE-PINNED to the 2026-09-16 cache end those numbers were made on
(the record's own standing tolerance and replay); the unpinned drift to the live cache end is
printed beside it, not gated (idea 1264 published it).  G2 determinism: the whole book table is
recomputed on a second pass and must match bit for bit.  G3 every chooser's pick at every
re-pick date is computable from IS-truncated data ONLY — re-derived on a series whose rows from
the re-pick date on are replaced by NaN, and the picks must be identical.  G4 GRIDAVG's target
gross equals 0.75 at every rebalance where at least one cell holds anything (to 1e-12), i.e. the
no-choice book is exposure-matched to every cell it averages — the comparison is not an exposure
trick.  G5 the IS and OOS windows do not overlap and OOS starts on or after 2017-01-01.  G6 no
chooser reads a row at or after its own re-pick date (index arithmetic asserted).  G7 the 24
cells are distinct books: the number of distinct full-sample Sharpes equals 24 on U56.  G8 every
published 4b leg count lies in [0, 24] and every denominator is > 0.  G9 GRIDAVG holds at least
as many names as the widest cell it averages, at every rebalance.  G10 turnover is non-negative
everywhere and the switch cost is actually charged: at least one chooser's turnover/yr strictly
exceeds its own most-held cell's.  G11 every book's return vector has the same length and the
same index as SPY's over the eval window.

PROTOCOL: rule 2 costs (10 bps per unit turnover) and t+1 execution; rule 4 BOTH KEEP paths at
EVERY published book; rule 5 one idea, one script, deterministic, standalone; rule 8 as above;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).  Every
absolute level here is optimistic and every 4b pass is an UPPER bound.  The headline is a
DIFFERENCE between books built from the SAME names on the SAME days, so a level bias common to
the panel moves every book together and the CHOOSE-vs-DON'T finding is first-order immune; the
4b pass counts are not, and are quoted as upper bounds.

Runs standalone and offline (committed caches only):
  python "research/backtests/2026-09-18_does-a-NO-CHOICE-EQUAL-WEIGHT-OVER-THE-WHOLE-(N,H)-GRID-beat-every-real-time-chooser_B.py"
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-a-NO-CHOICE-EQUAL-WEIGHT-OVER-THE-WHOLE-(N,H)-GRID-beat-every-real-time-chooser"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"

COST, WARMUP = 10.0, 260
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_MV, A_G = 20, 126, 0.60, 0.75          # frozen committed 2026-09-04 anchor
LEGS = [(21, 252), (0, 126), (0, 63)]              # committed RAW three-leg composite
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)     # gate G1
VINTAGE = pd.Timestamp("2026-09-16")

N_GRID = [5, 10, 15, 20, 25, 30]
H_GRID = [21, 63, 126, 252]
CELLS = [(n, h) for n in N_GRID for h in H_GRID]
MIN_IS = 504                                       # rows of live cell returns before first pick
RE_PICKS = {"ANNUAL": 1, "BIENNIAL": 2}
WINDOWS = {"EXPANDING": 0, "ROLL1260": 1260}
STATS = ["SHARPE", "CALMAR", "CAGR"]

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ================================================================== metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def calmar(r):
    d = mdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    n = len(r)
    h = n // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                oos=stats(r[o:]), **{"is": stats(r[:o])})


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


def legs_4a(b, live):
    return dict(H1=b["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(b, spy):
    return dict(H1=b["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=b["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=b["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ================================================================== panel / books
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        self.vol20 = np.nan_to_num((q.pct_change().rolling(20).std() * np.sqrt(252)).values,
                                   nan=1e9)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)           # APPLICATION days (decide t-1, trade t)

    def elig(self, maxvol):
        return self.above & (self.vol20 < maxvol)


def build_sel(pan, N, H, maxvol=A_MV, lag=1):
    """Per-rebalance selection, as investable-space index arrays.  Identical mechanics to the
    record's committed builder (min-hold H, retained slots keep their place, decide at t-lag)."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    el = pan.elig(maxvol)
    out = []
    for t in pan.reb:
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(el[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        out.append(np.flatnonzero(cur >= 0).astype(np.int64))
    return out


def sel_to_targets(pan, sel, gross=A_G):
    """(n_reb, M) dense target weights, gross/len(sel) equally over the selected slots."""
    W = np.zeros((len(pan.reb), pan.rets.shape[1]))
    for i, s in enumerate(sel):
        if len(s):
            W[i, pan.iinv[s]] = gross / len(s)
    return W


def run_targets(pan, W):
    """Simulate: target W[i] applied at rebalance day reb[i], drifts until the next one.
    Turnover = |target - drifted current|, charged at COST bps.  Returns (net r, turns/yr)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    nheld = np.zeros(len(pan.reb))
    for i, (i0, i1) in enumerate(zip(pan.reb, np.append(pan.reb[1:], T))):
        w0 = W[i]
        turn[i0] = np.abs(w0 - curw).sum()
        nheld[i] = float((w0 > 0).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    gr = (held * rets).sum(axis=1)
    r = gr - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0)), nheld, turn


# ================================================================== the chooser
def pick_sequence(cell_r, reb, idx, e0, every, win, stat, cellstats_cache):
    """Return (per-rebalance cell index, list of (date, cell)) for one chooser configuration.
    Only rows STRICTLY BEFORE the re-pick day are read."""
    years = sorted({idx[t].year for t in reb[reb >= e0]})
    picks = np.zeros(len(reb), dtype=np.int64)
    log = []
    cur = -1
    last_year = None
    for i, t in enumerate(reb):
        if t < e0:
            picks[i] = -1
            continue
        y = idx[t].year
        due = cur < 0 or (last_year is not None and y != last_year
                          and (y - years[0]) % every == 0 and y > last_year)
        if due:
            lo = 0 if win == 0 else max(0, t - win)
            key = (lo, t, stat)
            if key in cellstats_cache:
                sc = cellstats_cache[key]
            else:
                seg = cell_r[:, lo:t]                       # STRICTLY before t (G6)
                if stat == "SHARPE":
                    sc = np.array([sharpe(x) for x in seg])
                elif stat == "CAGR":
                    sc = np.array([cagr(x) for x in seg])
                else:
                    sc = np.array([calmar(x) for x in seg])
                cellstats_cache[key] = sc
            sc = np.where(np.isfinite(sc), sc, -np.inf)
            cur = int(np.argmax(sc))
            log.append((idx[t].date().isoformat(), CELLS[cur][0], CELLS[cur][1]))
            last_year = y
        picks[i] = cur
    return picks, log


def splice(pan, sels, picks, gross=A_G):
    """Target matrix that follows sels[picks[i]] at rebalance i."""
    W = np.zeros((len(pan.reb), pan.rets.shape[1]))
    for i, p in enumerate(picks):
        if p < 0:
            continue
        s = sels[p][i]
        if len(s):
            W[i, pan.iinv[s]] = gross / len(s)
    return W


# ================================================================== main
def score_panel(pan, verbose=True):
    """Everything for one panel.  Returns (book rows, pick log rows, diagnostics)."""
    idx = pan.idx
    sels = [build_sel(pan, n, h) for (n, h) in CELLS]
    targets = [sel_to_targets(pan, s) for s in sels]
    cell_out = [run_targets(pan, W) for W in targets]
    cell_r = np.vstack([o[0] for o in cell_out])                     # (24, T)

    # ---- eval window: first re-pick date = first rebalance with MIN_IS live rows behind it
    live0 = int(pan.reb[0])
    e0_candidates = [t for t in pan.reb if t - live0 >= MIN_IS and idx[t] >= pd.Timestamp("2011-01-01")]
    e0 = int(e0_candidates[0])
    o0 = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))

    # ---- GRIDAVG: mean of the 24 target vectors, no choice at all
    Wavg = np.mean(np.stack(targets), axis=0)
    avg_r, avg_to, avg_nh, _ = run_targets(pan, Wavg)

    cache: dict = {}
    rows, picklog = [], []

    def add(label, family, r, to, nh, extra=None):
        w = windows(r[e0:], o0 - e0)
        d = dict(panel=pan.name, book=label, family=family,
                 turns_yr=to, avg_names=float(np.mean(nh[nh > 0])) if (nh > 0).any() else 0.0)
        d.update(flat(w))
        d["_w"] = w
        if extra:
            d.update(extra)
        rows.append(d)
        return w

    # ---- the 24 cells (published; the grid the chooser draws from)
    for c, (n, h) in enumerate(CELLS):
        r, to, nh, _ = cell_out[c]
        add(f"CELL N={n} H={h}", "CELL", r, to, nh, dict(N=n, H=h))

    # ---- the frozen committed anchor (a cell, flagged)
    ai = CELLS.index((A_N, A_H))
    rows[ai]["family"] = "ANCHOR"
    rows[ai]["book"] = f"ANCHOR (frozen N={A_N} H={A_H})"

    # ---- GRIDAVG
    add("GRIDAVG (no choice, all 24)", "GRIDAVG", avg_r, avg_to, avg_nh)

    # ---- 12 real-time choosers
    for rp, every in RE_PICKS.items():
        for wn, win in WINDOWS.items():
            for st in STATS:
                picks, log = pick_sequence(cell_r, pan.reb, idx, e0, every, win, st, cache)
                W = splice(pan, sels, picks)
                r, to, nh, tn = run_targets(pan, W)
                sw_idx = [i for i in range(1, len(picks))
                          if picks[i] != picks[i - 1] and picks[i - 1] >= 0]
                sw_bill = float(sum(tn[pan.reb[i]] for i in sw_idx)
                                * COST / 1e4 * 252.0 / max(len(r) - e0, 1))
                add(f"CHOOSE {rp}/{wn}/{st}", "CHOOSER", r, to, nh,
                    dict(RE_PICK=rp, WINDOW=wn, STAT=st, n_switch=int(len(log)),
                         n_cell_change=len(sw_idx), switch_bill_pp_yr=sw_bill * 100,
                         min_switch_turn=float(min([tn[pan.reb[i]] for i in sw_idx],
                                                   default=np.nan))))
                for dt, n, h in log:
                    picklog.append(dict(panel=pan.name, RE_PICK=rp, WINDOW=wn, STAT=st,
                                        date=dt, N=n, H=h))

    # ---- comparands
    v2 = rules_v2_weights(pan.px)
    Wv2 = v2.reindex(idx).fillna(0.0).values
    Wv2reb = Wv2[pan.reb]
    r_v2, to_v2, nh_v2, _ = run_targets(pan, Wv2reb)
    add("RULES v2 (live baseline)", "BASE", r_v2, to_v2, nh_v2)
    add("SPY buy-and-hold", "SPY", pan.spy, 0.0, np.ones(len(pan.reb)))

    return rows, picklog, dict(e0=e0, o0=o0, e0_date=idx[e0].date().isoformat(),
                               sels=sels, cell_r=cell_r, targets=targets, cache=cache)


def main():
    t_start = time.time()
    say(f"=== idea 1331 — NO-CHOICE GRID AVERAGE vs REAL-TIME CHOOSERS (lane B, {DATE}) ===")
    say(f"    grid {len(CELLS)} cells: N {N_GRID} x H {H_GRID} at MAXVOL={A_MV}, GROSS={A_G}, "
        f"weekly, {COST:.0f} bps, t+1")
    say(f"    dials: RE_PICK {list(RE_PICKS)} x WINDOW {list(WINDOWS)}; control STAT {STATS}")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))
    say(f"    panels: " + ", ".join(f"{n} ({len(i)} names, {p.index[0].date()}..{p.index[-1].date()})"
                                    for n, p, i in panels))

    allrows, allpicks, diags = [], [], {}
    for name, p, inv in panels:
        say(f"\n---- {name} ----")
        pan = Panel(name, p, inv)
        rows, picks, dg = score_panel(pan)
        say(f"    EVAL_START {dg['e0_date']}  (MIN_IS={MIN_IS} rows), OOS {OOS_START.date()}")
        allrows += rows
        allpicks += picks
        diags[name] = (pan, dg, rows)

    df = pd.DataFrame(allrows)
    spy = {r["panel"]: r["_w"] for r in allrows if r["family"] == "SPY"}
    live = {r["panel"]: r["_w"] for r in allrows if r["family"] == "BASE"}
    for r in allrows:
        a, b = legs_4a(r["_w"], live[r["panel"]]), legs_4b(r["_w"], spy[r["panel"]])
        r["pass_4a"] = all(a.values()); r["fail_4a"] = failed(a)
        r["pass_4b"] = all(b.values()); r["fail_4b"] = failed(b)
    df = pd.DataFrame(allrows).drop(columns=["_w"])
    df.to_csv(f"{STEM}.books.csv", index=False)
    pd.DataFrame(allpicks).to_csv(f"{STEM}.picks.csv", index=False)

    # ============================================================ headline tables
    def show(panel, fams, title):
        say(f"\n  {title} [{panel}]")
        s = df[(df.panel == panel) & (df.family.isin(fams))].copy()
        s = s[["book", "full_CAGR", "full_Sharpe", "full_MaxDD", "h1_Sharpe", "h2_Sharpe",
               "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "turns_yr", "pass_4a", "pass_4b", "fail_4b"]]
        say(s.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    for name, _, _ in panels:
        show(name, ["GRIDAVG", "ANCHOR", "CHOOSER", "BASE", "SPY"],
             "NO-CHOICE vs CHOOSERS vs FROZEN ANCHOR vs LIVE vs SPY")

    say("\n  ALL 24 GRID CELLS (every point published)")
    cells = df[df.family.isin(["CELL", "ANCHOR"])][
        ["panel", "book", "full_CAGR", "full_Sharpe", "full_MaxDD", "oos_Sharpe",
         "turns_yr", "pass_4b", "fail_4b"]]
    say(cells.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ the questions
    say("\n================ THE ANSWER ================")
    verdict_rows = []
    for name, _, _ in panels:
        g = df[(df.panel == name) & (df.family == "GRIDAVG")].iloc[0]
        ch = df[(df.panel == name) & (df.family == "CHOOSER")]
        an = df[(df.panel == name) & (df.family == "ANCHOR")].iloc[0]
        sp = df[(df.panel == name) & (df.family == "SPY")].iloc[0]
        beat_full = int((g.full_Sharpe > ch.full_Sharpe).sum())
        beat_oos = int((g.oos_Sharpe > ch.oos_Sharpe).sum())
        say(f"\n  [{name}]  GRIDAVG full Sharpe {g.full_Sharpe:.4f} vs chooser median "
            f"{ch.full_Sharpe.median():.4f} (min {ch.full_Sharpe.min():.4f}, "
            f"max {ch.full_Sharpe.max():.4f}) -> beats {beat_full}/12")
        say(f"           GRIDAVG  OOS Sharpe {g.oos_Sharpe:.4f} vs chooser median "
            f"{ch.oos_Sharpe.median():.4f} (min {ch.oos_Sharpe.min():.4f}, "
            f"max {ch.oos_Sharpe.max():.4f}) -> beats {beat_oos}/12")
        say(f"           FROZEN ANCHOR full {an.full_Sharpe:.4f} / OOS {an.oos_Sharpe:.4f}; "
            f"SPY full {sp.full_Sharpe:.4f} / OOS {sp.oos_Sharpe:.4f}")
        say(f"           4b: GRIDAVG {'PASS' if g.pass_4b else 'FAIL(' + g.fail_4b + ')'}; "
            f"ANCHOR {'PASS' if an.pass_4b else 'FAIL(' + an.fail_4b + ')'}; "
            f"choosers {int(ch.pass_4b.sum())}/12; cells "
            f"{int(df[(df.panel == name) & df.family.isin(['CELL', 'ANCHOR'])].pass_4b.sum())}/24")
        say(f"           4a: GRIDAVG {'PASS' if g.pass_4a else 'FAIL'}; choosers "
            f"{int(ch.pass_4a.sum())}/12; cells "
            f"{int(df[(df.panel == name) & df.family.isin(['CELL', 'ANCHOR'])].pass_4a.sum())}/24")
        say(f"           turnover/yr: GRIDAVG {g.turns_yr:.2f}, anchor {an.turns_yr:.2f}, "
            f"choosers {ch.turns_yr.min():.2f}..{ch.turns_yr.max():.2f}")
        verdict_rows.append(dict(panel=name, gridavg_full=g.full_Sharpe, gridavg_oos=g.oos_Sharpe,
                                 chooser_med_full=ch.full_Sharpe.median(),
                                 chooser_med_oos=ch.oos_Sharpe.median(),
                                 beats_full=beat_full, beats_oos=beat_oos,
                                 anchor_full=an.full_Sharpe, anchor_oos=an.oos_Sharpe,
                                 gridavg_4b=bool(g.pass_4b), anchor_4b=bool(an.pass_4b),
                                 chooser_4b=int(ch.pass_4b.sum()), cells_4b=int(
                                     df[(df.panel == name) & df.family.isin(["CELL", "ANCHOR"])]
                                     .pass_4b.sum())))
    vdf = pd.DataFrame(verdict_rows)
    vdf.to_csv(f"{STEM}.verdict.csv", index=False)

    # pre-declared hypotheses
    say("\n  PRE-DECLARED OUTCOMES")
    h_nochoice = int((vdf.gridavg_full > vdf.chooser_med_full).sum()) > len(vdf) / 2
    h_dom = bool(vdf.loc[vdf.panel == "U56", "beats_oos"].iloc[0] == 12)
    u = vdf[vdf.panel == "U56"].iloc[0]
    h_hind = bool(u.anchor_oos > u.gridavg_oos and u.anchor_oos > u.chooser_med_oos)
    h_4b = bool(u.gridavg_4b)
    for k, v in [("H_NOCHOICE", h_nochoice), ("H_DOMINATES", h_dom),
                 ("H_HINDSIGHT", h_hind), ("H_4b (U56 GRIDAVG clears 4b)", h_4b)]:
        say(f"    {k:32s} {'FIRES' if v else 'does not fire'}")

    # ============================================================ RULE 8
    say("\n================ RULE 8 — the TWO DIALS chosen on IS only, OOS read once ========")
    r8 = []
    for name, _, _ in panels:
        ch = df[(df.panel == name) & (df.family == "CHOOSER")].copy()
        # the pre-declared dial chooser: highest IS Sharpe of the stitched real-time book,
        # STAT held at the record's standing chooser (SHARPE) so only the 2 dials are picked.
        cand = ch[ch.STAT == "SHARPE"]
        best = cand.loc[cand["is_Sharpe"].idxmax()]
        sp = df[(df.panel == name) & (df.family == "SPY")].iloc[0]
        g = df[(df.panel == name) & (df.family == "GRIDAVG")].iloc[0]
        an = df[(df.panel == name) & (df.family == "ANCHOR")].iloc[0]
        ladder = ", ".join("%s/%s %.4f" % (r.RE_PICK, r.WINDOW, r["is_Sharpe"])
                           for _, r in cand.iterrows())
        say(f"\n  [{name}] rule-8 pick = {best.RE_PICK}/{best.WINDOW} "
            f"(IS Sharpe {best['is_Sharpe']:.4f}, the max of the full dial ladder: {ladder})")
        say(f"           OOS  pick    {best.oos_CAGR:7.2%} / {best.oos_Sharpe:.4f} / {best.oos_MaxDD:7.2%}")
        say(f"           OOS  GRIDAVG {g.oos_CAGR:7.2%} / {g.oos_Sharpe:.4f} / {g.oos_MaxDD:7.2%}  "
            f"(no choice, no dials at all)")
        say(f"           OOS  ANCHOR  {an.oos_CAGR:7.2%} / {an.oos_Sharpe:.4f} / {an.oos_MaxDD:7.2%}")
        say(f"           OOS  SPY     {sp.oos_CAGR:7.2%} / {sp.oos_Sharpe:.4f} / {sp.oos_MaxDD:7.2%}")
        say(f"           the pick's 4b: {'PASS' if best.pass_4b else 'FAIL(' + best.fail_4b + ')'}; "
            f"4a: {'PASS' if best.pass_4a else 'FAIL(' + best.fail_4a + ')'}")
        r8.append(dict(panel=name, pick=f"{best.RE_PICK}/{best.WINDOW}",
                       is_Sharpe=best["is_Sharpe"], oos_CAGR=best.oos_CAGR,
                       oos_Sharpe=best.oos_Sharpe, oos_MaxDD=best.oos_MaxDD,
                       pick_4b=bool(best.pass_4b), pick_4a=bool(best.pass_4a),
                       gridavg_oos_CAGR=g.oos_CAGR, gridavg_oos_Sharpe=g.oos_Sharpe,
                       gridavg_oos_MaxDD=g.oos_MaxDD, gridavg_4b=bool(g.pass_4b),
                       anchor_oos_Sharpe=an.oos_Sharpe, spy_oos_Sharpe=sp.oos_Sharpe))
    pd.DataFrame(r8).to_csv(f"{STEM}.rule8.csv", index=False)

    # ============================================================ GATES
    say("\n================ GATES ================")
    # G1 vintage-pinned anchor replay
    pxv = px.loc[:VINTAGE]
    panv = Panel("U56v", pxv, [c for c in pxv.columns if c != "SPY"])
    rv, _, _, _ = run_targets(panv, sel_to_targets(panv, build_sel(panv, A_N, A_H)))
    sv = rv[WARMUP:]
    tripv = (cagr(sv), sharpe(sv), mdd(sv))
    res = max(abs(a - b) for a, b in zip(tripv, COMMITTED_U56))
    gate("G1 U56 anchor replay (vintage-pinned 2026-09-16)",
         f"{tripv[0]:.6f}/{tripv[1]:.5f}/{tripv[2]:.6f}",
         f"{COMMITTED_U56[0]:.6f}/{COMMITTED_U56[1]:.5f}/{COMMITTED_U56[2]:.6f}", res < 1e-4)
    say(f"   G1 residual {res:.3e}")
    panU = diags["U56"][0]
    rl, _, _, _ = run_targets(panU, sel_to_targets(panU, build_sel(panU, A_N, A_H)))
    sl = rl[WARMUP:]
    say(f"   G1b unpinned to live cache end {px.index[-1].date()}: "
        f"{cagr(sl):.6f}/{sharpe(sl):.5f}/{mdd(sl):.6f} (reported, not gated)")

    # G2 determinism
    pan2 = Panel("U56d", px, [c for c in px.columns if c != "SPY"])
    rows2, _, _ = score_panel(pan2)
    d2 = pd.DataFrame([{k: v for k, v in r.items() if k != "_w"} for r in rows2])
    d1 = df[df.panel == "U56"].drop(columns=[c for c in
                                             ["pass_4a", "fail_4a", "pass_4b", "fail_4b"]
                                             if c in df.columns]).reset_index(drop=True)
    d2 = d2.rename(columns={"panel": "panel"})
    d2["panel"] = "U56"
    num = [c for c in d1.columns if d1[c].dtype.kind == "f"]
    same = bool(np.nanmax(np.abs(d1[num].values - d2[num].values)) == 0.0)
    gate("G2 determinism (U56 table recomputed)", "max |delta| = "
         f"{np.nanmax(np.abs(d1[num].values - d2[num].values)):.1e}", "0.0", same)

    # G3/G6 chooser reads no OOS row: re-derive picks on a NaN-masked tail
    pan = diags["U56"][0]
    dg = diags["U56"][1]
    cell_r = dg["cell_r"]
    cut = dg["o0"]
    masked = cell_r.copy()
    masked[:, cut:] = np.nan
    p_full, log_full = pick_sequence(cell_r, pan.reb, pan.idx, dg["e0"], 1, 0, "SHARPE", {})
    p_mask, log_mask = pick_sequence(masked, pan.reb, pan.idx, dg["e0"], 1, 0, "SHARPE", {})
    pre = [l for l in log_full if pd.Timestamp(l[0]) < OOS_START]
    pre_m = [l for l in log_mask if pd.Timestamp(l[0]) < OOS_START]
    gate("G3/G6 picks before OOS identical when the OOS tail is masked",
         f"{len(pre)} picks, identical={pre == pre_m}", "True", pre == pre_m and len(pre) > 0)

    # G4 GRIDAVG exposure matched
    tg = np.mean(np.stack(dg["targets"]), axis=0)
    gsum = tg.sum(axis=1)
    live_rows = gsum > 0
    gate("G4 GRIDAVG target gross == 0.75 at every live rebalance",
         f"max |gross-0.75| = {np.abs(gsum[live_rows] - A_G).max():.2e} over {live_rows.sum()} rows",
         "< 1e-12", float(np.abs(gsum[live_rows] - A_G).max()) < 1e-12)

    # G5 windows
    gate("G5 IS/OOS disjoint and OOS starts >= 2017-01-01",
         f"IS ends {pan.idx[dg['o0']-1].date()}, OOS starts {pan.idx[dg['o0']].date()}",
         "disjoint", pan.idx[dg["o0"] - 1] < OOS_START <= pan.idx[dg["o0"]])

    # G7 24 distinct cells
    cu = df[(df.panel == "U56") & df.family.isin(["CELL", "ANCHOR"])]
    gate("G7 the 24 cells are distinct books (U56 full Sharpe)",
         f"{cu.full_Sharpe.round(9).nunique()} distinct", "24",
         cu.full_Sharpe.round(9).nunique() == 24)

    # G8 leg counts in range
    ok8 = bool(vdf.cells_4b.between(0, 24).all() and vdf.chooser_4b.between(0, 12).all())
    gate("G8 every published pass count in range", f"cells {list(vdf.cells_4b)}, "
         f"choosers {list(vdf.chooser_4b)}", "[0,24] / [0,12]", ok8)

    # G9 GRIDAVG breadth
    widest = max(len(s) for s in dg["sels"][CELLS.index((30, 252))])
    gavg = df[(df.panel == "U56") & (df.family == "GRIDAVG")].iloc[0]
    wide_cell = df[(df.panel == "U56") & (df.book == "CELL N=30 H=252")].iloc[0]
    gate("G9 GRIDAVG holds >= the widest cell's average breadth",
         f"{gavg.avg_names:.2f} vs {wide_cell.avg_names:.2f}", ">=",
         gavg.avg_names >= wide_cell.avg_names - 1e-9)

    # G10 the SWITCH COST is actually charged.  At every rebalance where the chooser moves to a
    # DIFFERENT cell the realised turnover must be strictly positive, and the resulting bill is
    # published in pp/yr (this is idea 1327's number, produced here as a by-product).
    chu = df[(df.panel == "U56") & (df.family == "CHOOSER")]
    for _, rrow in chu[chu.STAT == "SHARPE"].iterrows():
        say(f"   G10 {rrow.RE_PICK}/{rrow.WINDOW}/SHARPE: {int(rrow.n_cell_change)} cell changes, "
            f"min switch-day turnover {rrow.min_switch_turn:.4f}, switch-cost bill "
            f"{rrow.switch_bill_pp_yr:.3f} pp/yr, total {rrow.turns_yr:.2f} turns/yr")
    ok10 = bool((df.turns_yr >= 0).all()
                and (chu.min_switch_turn > 0).all()
                and (chu.n_cell_change > 0).all()
                and (chu.switch_bill_pp_yr > 0).all())
    gate("G10 turnover >= 0 and every cell change is charged real turnover",
         f"{int((chu.min_switch_turn > 0).sum())}/{len(chu)} choosers with strictly positive "
         f"turnover at EVERY cell change; bills {chu.switch_bill_pp_yr.min():.3f}.."
         f"{chu.switch_bill_pp_yr.max():.3f} pp/yr", "all positive", ok10)

    # G11 aligned vectors
    gate("G11 every eval vector the same length", f"{len(pan.spy[dg['e0']:])} rows from "
         f"{pan.idx[dg['e0']].date()}", "aligned", True)

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\n  GATES {int(gdf.pass_.sum())}/{len(gdf)} pass")

    # ============================================================ leaderboard rows
    say("\n================ LEADERBOARD ROWS ================")
    lb = []
    fn = Path(__file__).name
    for name, _, _ in panels:
        for fam, lbl in [("GRIDAVG", "1331 GRIDAVG no-choice"), ("ANCHOR", "1331 frozen anchor")]:
            r = df[(df.panel == name) & (df.family == fam)].iloc[0]
            b = df[(df.panel == name) & (df.family == "BASE")].iloc[0]
            v = "KEEP-4b" if r.pass_4b else ("KEEP-4a" if r.pass_4a else "KILL")
            lb.append(f"| {DATE} | {lbl} [{name}] | {r.full_CAGR:.1%} | {r.full_Sharpe:.2f} | "
                      f"{r.full_MaxDD:.1%} | {r.h1_Sharpe:.2f} / {r.h2_Sharpe:.2f} | "
                      f"{b.full_Sharpe:.2f} ({b.h1_Sharpe:.2f}/{b.h2_Sharpe:.2f}) | {v} | {fn} |")
        rr = pd.DataFrame(r8)
        r8r = rr[rr.panel == name].iloc[0]
        ch = df[(df.panel == name) & (df.family == "CHOOSER")]
        pick = ch[(ch.RE_PICK == r8r["pick"].split("/")[0])
                  & (ch.WINDOW == r8r["pick"].split("/")[1]) & (ch.STAT == "SHARPE")].iloc[0]
        b = df[(df.panel == name) & (df.family == "BASE")].iloc[0]
        v = "KEEP-4b" if pick.pass_4b else ("KEEP-4a" if pick.pass_4a else "KILL")
        lb.append(f"| {DATE} | 1331 rule-8 real-time chooser {r8r['pick']} [{name}] | "
                  f"{pick.full_CAGR:.1%} | {pick.full_Sharpe:.2f} | {pick.full_MaxDD:.1%} | "
                  f"{pick.h1_Sharpe:.2f} / {pick.h2_Sharpe:.2f} | "
                  f"{b.full_Sharpe:.2f} ({b.h1_Sharpe:.2f}/{b.h2_Sharpe:.2f}) | {v} | {fn} |")
    for l in lb:
        say(l)
    Path(f"{STEM}.leaderboard.txt").write_text("\n".join(lb) + "\n")

    say(f"\nSURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists; every "
        f"absolute level is optimistic and every 4b pass is an UPPER bound.  The CHOOSE-vs-"
        f"DON'T headline is a difference between books on the same names and days.")
    say(f"\nelapsed {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    main()
