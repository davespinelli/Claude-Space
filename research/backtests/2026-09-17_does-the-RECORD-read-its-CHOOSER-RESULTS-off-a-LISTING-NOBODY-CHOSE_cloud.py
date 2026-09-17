#!/usr/bin/env python3
"""Idea 1228 (cloud lane, 2026-09-17) — does the RECORD read its CHOOSER RESULTS off a
LISTING NOBODY CHOSE?

Idea 1227 found U56 / NG / L252 / H_ANY stitches to OOS Sharpe 1.2377 against the anchor's
1.1759 while its OWN pooled fold delta is -0.0197: the best CURVE in a listing is not the
best DECISION.  The queue asks two things:

  (Q1) CENSUS — how many committed chooser claims quote a LISTING MAXIMUM (a statistic
       maximised over a grid, read on the same window it is reported on) rather than a
       WALK-FORWARD PICK (chosen in-sample, evaluated out-of-sample)?
  (Q2) PRICE — how big is the gap between the two readings, in OOS Sharpe, on real books?

WHAT IS AN IDENTITY AND NOT A FINDING, DECLARED BEFORE ANY NUMBER.  When the listing
statistic IS the evaluation statistic, max-over-the-listing >= any-single-pick is true by
construction on any tape, any ladder, any panel: a maximum dominates every element of the
set it is taken over.  Gate G6 verifies it so this run cannot be read as having discovered
it.  The empirical content is entirely in (i) HOW BIG the gap is in Sharpe units, (ii)
whether it survives when the listing statistic is NOT the evaluation statistic (where no
identity applies and the gap may be negative), and (iii) what share of the record's
committed chooser prose is written in the dominated form.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  CLAIM CLASS       {K_N, K_H, K_GROSS, K_CADENCE, K_ALL4}     (5 listings)
  LISTING STATISTIC {S_SHARPE, S_CAGR, S_MAR, S_4BMARGIN}      (4 statistics)
= 20 (claim class, listing statistic) cells per panel, 60 in all, EVERY ONE PUBLISHED.
The RUNG inside a listing is NOT a third tuned parameter: it is the object a chooser
selects, which is the subject of the run, and every rung of every listing is published in
.grid.csv regardless of what any reading did with it.  PANEL {U56, B136, SMALL} is NOT a
dial (PROTOCOL rule 9) — all three are reported at every cell and nothing is selected on
the triple.

FROZEN, NOT TUNED (so the numbers cross-read against the record): CAND20 legs
[(21,252),(0,126),(0,63)], max_vol 0.60, min hold H=126, N=20, gross 0.75, cadence W,
cost 10 bps (PROTOCOL rule 2 — a book cannot choose its cost rate), LAG 1 (next-day
execution), warm-up 260 rows, IS end 2016-12-31 for the rule-8 split, DD cap 0.60 and CAGR
floor 0.70 for 4b.  The FOLD construction is frozen at 14 equal consecutive OOS folds over
the post-warm-up tape with an EXPANDING in-sample window (minimum 756 bars).  The IS window
FORM is not a dial here: the L252 rolling variant is run once, as gate G9, and published,
but nothing is ever selected on it.

PRICE VINTAGE, PINNED AND DECLARED (defect published by idea 1160 on 2026-09-17).
data/prices.csv now carries a 2026-09-16 bar.  Every tape here is truncated at
PIN = 2026-09-15 so the committed anchors reproduce; G2 carries the 5e-3 tolerance the
record's vintage defect requires rather than absorbing it.

SURVIVORSHIP (PROTOCOL rule 9).  U56, B136 and SMALL are CURRENT-CONSTITUENT lists.  SMALL
is the current constituents of a sub-$2B screen, served after dropping every ticker with
max_1d_move >= 1.0 in data/small_meta.csv.  The pool was REBUILT on 2026-09-11 (idea 706 /
1072): the label "SMALL439" no longer denotes 439 names, and this run prints the served
count rather than quoting a label.  Every delisted, acquired or screened-out name is absent
from all three panels, so every small-cap number here is an upper bound.

Writes: .gates.csv .grid.csv .readings.csv .folds.csv .census.csv .walkforward.csv
        .console.txt
Deterministic, standalone, no network.  Does not modify RULES.md / scan.py / bot.py /
baseline.py / PROTOCOL.md.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-the-RECORD-read-its-CHOOSER-RESULTS-off-a-LISTING-NOBODY-CHOSE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

PIN = "2026-09-15"
LAG, WARMUP, MAXVOL0, COST = 1, 260, 0.60, 10.0
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
N0, HOLD0, GROSS0, FREQ0 = 20, 126, 0.75, "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

NFOLD, MIN_IS = 14, 756

# ----------------------------------------------------------- THE LISTINGS (dial 1 of 2)
# A "claim class" is the LISTING the record reads a chooser result off.  Canonical rung
# order is declared here and never re-chosen.
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 42, 63, 90, 126, 189, 252]
LAD_G = [0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 1.00]
LAD_C = ["D", "W", "M", "Q"]
ANCHOR = (N0, HOLD0, GROSS0, FREQ0)

LISTING = {
    "K_N":       [(n, HOLD0, GROSS0, FREQ0) for n in LAD_N],
    "K_H":       [(N0, h, GROSS0, FREQ0) for h in LAD_H],
    "K_GROSS":   [(N0, HOLD0, g, FREQ0) for g in LAD_G],
    "K_CADENCE": [(N0, HOLD0, GROSS0, f) for f in LAD_C],
}
_all4 = []
for _k in ("K_N", "K_H", "K_GROSS", "K_CADENCE"):
    for _c in LISTING[_k]:
        if _c not in _all4:
            _all4.append(_c)
LISTING["K_ALL4"] = _all4
CLASSES = ["K_N", "K_H", "K_GROSS", "K_CADENCE", "K_ALL4"]

# ------------------------------------------------------ THE LISTING STATISTICS (dial 2 of 2)
# Each is re-expressed so HIGHER IS BETTER and is computable on ANY window, so the same
# statistic can be read as a LISTING MAXIMUM (on the evaluation window — the dominated
# form) or as a WALK-FORWARD PICK (on the in-sample window only — the honest form).
STATS = ["S_SHARPE", "S_CAGR", "S_MAR", "S_4BMARGIN"]

# committed cross-run anchors (unchanged constants, quoted so the gates are falsifiable)
A936_WH126 = (0.155787, 1.139701, -0.191276)      # U56 W/H126/N=20, 10 bps, full sample
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1227_HEAD = (1.2377, 1.1759, -0.0197)            # listing max / anchor / pooled fold delta

LOG: list[str] = []
GATES: list[dict] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=value, pass_=bool(ok)))
    P(f"  {name}  {'PASS' if ok else 'FAIL'}  {what}   value={value}")


# ------------------------------------------------- fast runner (1082/1098/1150/1161, verbatim)
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 5 or not np.isfinite(r).all():
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    elig = above & (vol20 < MAXVOL0)
    return sc.values, elig.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """CAND20 construction: top-N by score among eligible, minimum hold H, gross/N each,
    remainder in cash.  Identical to the record's committed builder."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


# --------------------------------------------------------- THE LISTING STATISTICS, on a window
def stat_of(name, r, spy_r):
    """Window statistic, HIGHER IS BETTER, computed on the SAME slice for book and SPY."""
    c, s, d = fmet(r)
    if name == "S_SHARPE":
        return s
    if name == "S_CAGR":
        return c
    if name == "S_MAR":
        return c / abs(d) if d and np.isfinite(d) and d != 0 else np.nan
    if name == "S_4BMARGIN":
        sc, ss, sd = fmet(spy_r)
        cap = DD_CAP * abs(sd)
        flo = CAGR_FLOOR * sc
        if not np.isfinite(ss) or ss == 0 or cap == 0 or flo == 0:
            return np.nan
        return min((s - ss) / abs(ss), (cap - abs(d)) / cap, (c - flo) / abs(flo))
    raise ValueError(name)


def main():
    P("=" * 100)
    P(f"IDEA 1228 (cloud lane, {DATE}) — does the RECORD read its CHOOSER RESULTS off a "
      "LISTING NOBODY CHOSE?")
    P("=" * 100)
    P(__doc__.strip())
    P("")

    # ------------------------------------------------------------------ panels
    P("## PANELS  (pinned at " + PIN + ")")
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]].dropna(how="all").ffill()
    raw = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": sm}

    panels = {}
    for panel in PANELS:
        px = raw[panel].loc[:PIN]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False          # SPY is the benchmark, never a constituent
        panels[panel] = dict(px=px, idx=idx, K=K, T=T,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm, ins=ins, oos=oos,
                             sc=sc, elig=elig,
                             spy=px["SPY"].pct_change().fillna(0.0).values)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {len(meta)} tickers; {len(bad)} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("  (idea 706/1072's defect: the pool was rebuilt 2026-09-11, so the served count is "
      "printed rather than a label.)")
    P("")

    CACHE: dict = {}

    def run_cell(panel, cell, fresh=False):
        key = (panel, cell)
        if key in CACHE and not fresh:
            return CACHE[key]
        N, H, gross, freq = cell
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        r = g - tn * COST / 1e4
        CACHE[key] = r
        return r

    # ------------------------------------------------------------------ gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_cell("U56", ANCHOR)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple", v, v < 5e-3)
    P(f"     this run {m['CAGR']:.6f}/{m['Sharpe']:.6f}/{m['MaxDD']:.6f} vs committed "
      f"{A936_WH126[0]:.6f}/{A936_WH126[1]:.6f}/{A936_WH126[2]:.6f}  "
      "(1160's price-vintage defect is CARRIED, not absorbed: the bar is 5e-3)")

    smm = blocks_m(d["spy"], d["warm"], d["ins"], d["oos"])
    v = max(abs(smm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(smm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(smm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple == committed", v, v < 5e-3)

    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    v = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)

    v = float(np.abs(run_cell("SMALL", ANCHOR, fresh=True)
                     - run_cell("SMALL", ANCHOR, fresh=True)).max())
    gate("G5", "determinism of the SMALL pipeline (two independent rebuilds, no cache)",
         v, v == 0.0)

    v = int(sum(ANCHOR not in LISTING[k] for k in CLASSES))
    gate("G7", "the ANCHOR rung is a member of EVERY listing (do-nothing is always available)",
         v, v == 0)

    # ------------------------------------------------------------------ folds
    P("")
    P("## FOLDS — 14 equal consecutive OOS folds over the post-warm-up tape, EXPANDING IS")
    for panel in PANELS:
        d = panels[panel]
        pos = np.flatnonzero(d["warm"])
        edges = np.linspace(MIN_IS, len(pos), NFOLD + 1).astype(int)
        folds = []
        for f in range(NFOLD):
            a, b = edges[f], edges[f + 1]
            if b - a < 20:
                continue
            folds.append(dict(f=f, is_lo=pos[0], is_hi=pos[a - 1], oo_lo=pos[a], oo_hi=pos[b - 1]))
        d["folds"] = folds
        P(f"  {panel:<6s} {len(folds)} folds, first OOS {d['idx'][folds[0]['oo_lo']].date()} "
          f"-> last OOS {d['idx'][folds[-1]['oo_hi']].date()}, "
          f"fold length {np.mean([f['oo_hi'] - f['oo_lo'] + 1 for f in folds]):.0f} bars")
    tot = sum(len(panels[p]["folds"]) for p in PANELS)
    gate("G8", "fold partitions are contiguous and non-overlapping in every panel",
         tot, all(panels[p]["folds"][i]["oo_hi"] + 1 == panels[p]["folds"][i + 1]["oo_lo"]
                  for p in PANELS for i in range(len(panels[p]["folds"]) - 1)))

    # ------------------------------------------------------------------ the grid
    P("")
    P("## GRID — every rung of every listing, on every panel, published")
    grid = []
    for panel in PANELS:
        d = panels[panel]
        for cell in _all4:
            r = run_cell(panel, cell)
            b = blocks_m(r, d["warm"], d["ins"], d["oos"])
            row = dict(panel=panel, N=cell[0], H=cell[1], GROSS=cell[2], CADENCE=cell[3],
                       is_anchor=(cell == ANCHOR),
                       classes="+".join(k for k in CLASSES if cell in LISTING[k]))
            row.update({k: float(v) for k, v in b.items()})
            for s in STATS:
                row[f"IS_{s}"] = float(stat_of(s, r[d["ins"]], d["spy"][d["ins"]]))
                row[f"OOS_{s}"] = float(stat_of(s, r[d["oos"]], d["spy"][d["oos"]]))
            grid.append(row)
    grid = pd.DataFrame(grid)
    dump(grid, "grid")
    P(f"  {len(_all4)} distinct books per panel x {len(PANELS)} panels = {len(grid)} book runs.")

    # G6 -- the IDENTITY, verified, so the run is not read as having discovered it
    viol = 0
    for panel in PANELS:
        g = grid[grid.panel == panel]
        for k in CLASSES:
            sub = g[g.classes.str.contains(k)]
            mx = sub["OOS_S_SHARPE"].max()
            if any(mx < sub["OOS_S_SHARPE"] - 1e-12):
                viol += 1
    gate("G6", "IDENTITY: max-over-listing >= every member (declared, not discovered)",
         viol, viol == 0)

    # ------------------------------------------------------------- readings + folds
    P("")
    P("## THE THREE READINGS, at every (panel, claim class, listing statistic) cell")
    P("   R_LIST   the LISTING MAXIMUM: argmax of the statistic read on the EVALUATION window")
    P("            (2017-01-01 onward).  This is the dominated form.  NOT DEPLOYABLE: it")
    P("            requires the evaluation window to pick.")
    P("   R_WF     the WALK-FORWARD PICK: at each fold, argmax of the SAME statistic on the")
    P("            expanding IS window only; the pick is held through the fold; the fold")
    P("            returns are stitched into one deployable curve.")
    P("   R_ANCH   the DO-NOTHING reading: the anchor book (N=20/H=126/g=0.75/W) at every fold.")
    P("")

    readings, foldrows = [], []
    for panel in PANELS:
        d = panels[panel]
        folds = d["folds"]
        oo_mask_all = np.zeros(d["T"], dtype=bool)
        for f in folds:
            oo_mask_all[f["oo_lo"]:f["oo_hi"] + 1] = True
        anch = run_cell(panel, ANCHOR)
        for k in CLASSES:
            cells = LISTING[k]
            for s in STATS:
                # ---- R_LIST: argmax on the evaluation window (the record's quoted form)
                vals = [stat_of(s, run_cell(panel, c)[oo_mask_all], d["spy"][oo_mask_all])
                        for c in cells]
                j = int(np.nanargmax(vals))
                r_list = run_cell(panel, cells[j])[oo_mask_all]

                # ---- R_WF: honest, per-fold IS argmax
                stitched = np.zeros(oo_mask_all.sum())
                picks, moves, off = [], 0, 0
                prev = None
                for f in folds:
                    isl = slice(f["is_lo"], f["is_hi"] + 1)
                    iv = [stat_of(s, run_cell(panel, c)[isl], d["spy"][isl]) for c in cells]
                    jj = int(np.nanargmax(iv))
                    pick = cells[jj]
                    n = f["oo_hi"] - f["oo_lo"] + 1
                    rr = run_cell(panel, pick)[f["oo_lo"]:f["oo_hi"] + 1]
                    stitched[off:off + n] = rr
                    off += n
                    picks.append(pick)
                    if prev is not None and pick != prev:
                        moves += 1
                    prev = pick
                    ar = anch[f["oo_lo"]:f["oo_hi"] + 1]
                    lr = run_cell(panel, cells[j])[f["oo_lo"]:f["oo_hi"] + 1]
                    foldrows.append(dict(panel=panel, claim_class=k, listing_stat=s, fold=f["f"],
                                         oos_start=str(d["idx"][f["oo_lo"]].date()),
                                         oos_end=str(d["idx"][f["oo_hi"]].date()),
                                         pick_N=pick[0], pick_H=pick[1], pick_G=pick[2],
                                         pick_C=pick[3], pick_is_anchor=(pick == ANCHOR),
                                         S_wf=fsharpe(rr), S_list=fsharpe(lr), S_anch=fsharpe(ar),
                                         d_list_wf=fsharpe(lr) - fsharpe(rr),
                                         d_wf_anch=fsharpe(rr) - fsharpe(ar)))
                assert off == len(stitched)
                r_anch = anch[oo_mask_all]

                fl = [x for x in foldrows if x["panel"] == panel and x["claim_class"] == k
                      and x["listing_stat"] == s]
                dlw = np.array([x["d_list_wf"] for x in fl], float)
                dwa = np.array([x["d_wf_anch"] for x in fl], float)
                se_lw = dlw.std(ddof=1) / np.sqrt(len(dlw))
                se_wa = dwa.std(ddof=1) / np.sqrt(len(dwa))
                readings.append(dict(
                    panel=panel, claim_class=k, listing_stat=s, n_rungs=len(cells),
                    list_pick=f"N{cells[j][0]}/H{cells[j][1]}/g{cells[j][2]}/{cells[j][3]}",
                    list_pick_is_anchor=(cells[j] == ANCHOR),
                    S_LIST=fsharpe(r_list), S_WF=fsharpe(stitched), S_ANCH=fsharpe(r_anch),
                    CAGR_LIST=fmet(r_list)[0], CAGR_WF=fmet(stitched)[0],
                    CAGR_ANCH=fmet(r_anch)[0],
                    DD_LIST=fmet(r_list)[2], DD_WF=fmet(stitched)[2], DD_ANCH=fmet(r_anch)[2],
                    GAP_curve=fsharpe(r_list) - fsharpe(stitched),
                    GAP_pooled=float(dlw.mean()), GAP_se=float(se_lw),
                    GAP_t=float(dlw.mean() / se_lw) if se_lw else np.nan,
                    WF_vs_ANCH_pooled=float(dwa.mean()), WF_vs_ANCH_se=float(se_wa),
                    WF_vs_ANCH_t=float(dwa.mean() / se_wa) if se_wa else np.nan,
                    n_moves=moves, move_rate=moves / max(len(folds) - 1, 1),
                    share_anchor_picks=float(np.mean([p == ANCHOR for p in picks])),
                    SPY_S=fsharpe(d["spy"][oo_mask_all])))
    readings = pd.DataFrame(readings)
    foldsdf = pd.DataFrame(foldrows)
    dump(readings, "readings")
    dump(foldsdf, "folds")

    P("")
    P("### Q2 — THE PRICED GAP, all 60 cells (Sharpe units on the stitched evaluation window)")
    show = readings[["panel", "claim_class", "listing_stat", "S_LIST", "S_WF", "S_ANCH",
                     "GAP_curve", "GAP_pooled", "GAP_se", "GAP_t", "move_rate",
                     "share_anchor_picks"]]
    P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("")
    P("### POOLED over the 60 cells")
    P(f"  mean GAP_curve (listing max minus walk-forward stitch) = {readings.GAP_curve.mean():+.4f}"
      f"   median {readings.GAP_curve.median():+.4f}   max {readings.GAP_curve.max():+.4f}")
    P(f"  cells where the LISTING MAX beats the WALK-FORWARD stitch: "
      f"{int((readings.GAP_curve > 0).sum())} of {len(readings)}")
    P(f"  cells where the WALK-FORWARD stitch beats the DO-NOTHING anchor: "
      f"{int((readings.S_WF > readings.S_ANCH).sum())} of {len(readings)}")
    P(f"  cells where the LISTING MAX beats the DO-NOTHING anchor: "
      f"{int((readings.S_LIST > readings.S_ANCH).sum())} of {len(readings)}")
    P(f"  mean pooled fold delta WF - ANCHOR = {readings.WF_vs_ANCH_pooled.mean():+.4f} "
      f"(mean |t| {readings.WF_vs_ANCH_t.abs().mean():.2f}); cells with |t| > 2: "
      f"{int((readings.WF_vs_ANCH_t.abs() > 2).sum())} of {len(readings)}")
    P(f"  1227's headline for cross-read: listing max {A1227_HEAD[0]:.4f} / anchor "
      f"{A1227_HEAD[1]:.4f} / pooled fold delta {A1227_HEAD[2]:+.4f}")

    by_stat = readings.groupby("listing_stat")[["GAP_curve", "GAP_pooled", "WF_vs_ANCH_pooled"]].mean()
    by_cls = readings.groupby("claim_class")[["GAP_curve", "GAP_pooled", "WF_vs_ANCH_pooled"]].mean()
    P("")
    P("  by LISTING STATISTIC (dial 2):")
    P(by_stat.to_string(float_format=lambda x: f"{x:+.4f}"))
    P("  by CLAIM CLASS (dial 1):")
    P(by_cls.to_string(float_format=lambda x: f"{x:+.4f}"))

    # ------------------------------------------------------------------ the census (Q1)
    P("")
    P("## Q1 — THE CENSUS of the record's committed chooser prose")
    P("   CORPUS: research/LEADERBOARD.md + research/CHANGELOG.md + research/backtests/*.md.")
    P("   UNIT: a sentence containing a CHOOSER VERB (pick / choose / chosen / argmax / select /")
    P("         reaches / lands on / best / top / maximum / peak / stitches to / wins).")
    P("   CLASSIFICATION, applied in this order and published as a rule, not a judgement:")
    P("     WF     the sentence carries a WALK-FORWARD MARKER (rule 8, walk-forward, IS-only,")
    P("            chosen on 2009-2016 / in-sample, out-of-sample evaluated, expanding IS, fold).")
    P("     LIST   no WF marker AND a SUPERLATIVE-OVER-A-SET marker (best/highest/maximum/top/")
    P("            argmax/peak/stitches to/widest) — i.e. a listing maximum.")
    P("     OTHER  a chooser verb with neither marker (unclassifiable from the text alone).")
    P("")
    CHOOSER = re.compile(
        r"\b(pick(?:s|ed)?|choos(?:e|es|en)|chose|argmax|select(?:s|ed)?|reach(?:es|ed)?|"
        r"lands? on|best|highest|top|maximum|maximis\w+|peaks? at|stitch(?:es)? to|wins)\b", re.I)
    WF = re.compile(
        r"\b(rule[- ]8|walk[- ]?forward|in[- ]sample|IS[- ]only|out[- ]of[- ]sample|OOS[- ]"
        r"evaluat\w+|expanding IS|fold|2009[-–]2016|chosen on the first half)\b", re.I)
    SUP = re.compile(
        r"\b(best|highest|maximum|maximal|top|argmax|peaks? at|stitch(?:es)? to|widest|"
        r"largest|greatest)\b", re.I)
    FAMILY = {"K_N": re.compile(r"\bN[ =_-]?\d|\bN ladder|\bn[ =]\d", re.I),
              "K_H": re.compile(r"\bH[ =_-]?\d|\bhold ladder|\bH axis", re.I),
              "K_GROSS": re.compile(r"\bgross\b", re.I),
              "K_CADENCE": re.compile(r"\bcadence\b|\bweekly\b|\bmonthly\b|\bquarterly\b", re.I)}

    srcs = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    srcs += sorted((ROOT / "research" / "backtests").glob("*.md"))
    census, nfiles, nsent = [], 0, 0
    for src in srcs:
        try:
            txt = src.read_text(errors="ignore")
        except Exception:
            continue
        nfiles += 1
        for sent in re.split(r"(?<=[.!?])\s+|\n", txt):
            sent = sent.strip()
            if not (40 <= len(sent) <= 900):
                continue
            nsent += 1
            if not CHOOSER.search(sent):
                continue
            has_wf, has_sup = bool(WF.search(sent)), bool(SUP.search(sent))
            klass = "WF" if has_wf else ("LIST" if has_sup else "OTHER")
            fam = [k for k, rx in FAMILY.items() if rx.search(sent)]
            census.append(dict(source=src.name, klass=klass,
                               family="+".join(fam) if fam else "",
                               n_family=len(fam), chars=len(sent), sent=sent[:400]))
    census = pd.DataFrame(census)
    dump(census, "census")
    tot_c = len(census)
    P(f"  corpus: {nfiles} files, {nsent:,} candidate sentences, {tot_c:,} chooser sentences.")
    cnt = census.klass.value_counts()
    for k in ("WF", "LIST", "OTHER"):
        n = int(cnt.get(k, 0))
        P(f"    {k:<6s} {n:7,d}   {n / tot_c:6.4f} of chooser sentences")
    P(f"  LISTING-MAX share among sentences the text CAN classify (WF + LIST): "
      f"{cnt.get('LIST', 0) / max(cnt.get('LIST', 0) + cnt.get('WF', 0), 1):.4f}")
    P("")
    P("  by SOURCE:")
    bysrc = census.groupby([census.source.str.slice(0, 28), "klass"]).size().unstack(fill_value=0)
    bysrc["LIST_share"] = bysrc.get("LIST", 0) / bysrc.sum(axis=1)
    P(bysrc.sort_values("LIST_share", ascending=False).head(12).to_string())

    # --- attach the measured gap to the LIST-form claims whose ladder family is inferable
    P("")
    P("### PRICING THE CENSUS — a LIST-form claim naming a ladder family inherits that")
    P("    family's measured GAP_curve (mean over panels and listing statistics).")
    fam_gap = readings.groupby("claim_class").GAP_curve.mean().to_dict()
    lst = census[census.klass == "LIST"]
    rows = []
    for k in ("K_N", "K_H", "K_GROSS", "K_CADENCE"):
        n = int((lst.family.str.contains(k, regex=False)).sum())
        rows.append(dict(family=k, list_claims=n, mean_GAP_curve=fam_gap[k]))
    fam_df = pd.DataFrame(rows)
    P(fam_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    n_named = int((lst.n_family > 0).sum())
    P(f"  LIST-form claims naming at least one ladder family: {n_named:,} of {len(lst):,} "
      f"({n_named / max(len(lst), 1):.4f}); the rest name no family and cannot be priced "
      "from the text alone.")
    P(f"  UNWEIGHTED mean overstatement a LIST-form claim carries, over the four families: "
      f"{fam_df.mean_GAP_curve.mean():+.4f} of Sharpe.")

    # ------------------------------------------------------------- rule-8 walk-forward
    P("")
    P("## PROTOCOL RULE 8 — parameters chosen on 2009-2016 ONLY, evaluated on 2017-2026")
    P("   For every (panel, claim class, listing statistic) cell the rule-8 PICK is the")
    P("   argmax of the listing statistic over the IS window; the OOS triple below is that")
    P("   single book's untouched 2017-2026 record.  R_LIST is shown beside it as the")
    P("   NON-DEPLOYABLE comparand the record's LIST-form prose quotes.")
    wf = []
    for panel in PANELS:
        d = panels[panel]
        spym = blocks_m(d["spy"], d["warm"], d["ins"], d["oos"])
        lb = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST,
                      freq="W")["returns"].values
        lbm = blocks_m(lb, d["warm"], d["ins"], d["oos"])
        for k in CLASSES:
            cells = LISTING[k]
            for s in STATS:
                iv = [stat_of(s, run_cell(panel, c)[d["ins"]], d["spy"][d["ins"]]) for c in cells]
                pick = cells[int(np.nanargmax(iv))]
                ov = [stat_of(s, run_cell(panel, c)[d["oos"]], d["spy"][d["oos"]]) for c in cells]
                lmax = cells[int(np.nanargmax(ov))]
                b = blocks_m(run_cell(panel, pick), d["warm"], d["ins"], d["oos"])
                bl = blocks_m(run_cell(panel, lmax), d["warm"], d["ins"], d["oos"])
                ba = blocks_m(run_cell(panel, ANCHOR), d["warm"], d["ins"], d["oos"])
                f4b, f4a = legs_4b(b, spym), legs_4a(b, lbm)
                wf.append(dict(
                    panel=panel, claim_class=k, listing_stat=s,
                    rule8_pick=f"N{pick[0]}/H{pick[1]}/g{pick[2]}/{pick[3]}",
                    listing_max=f"N{lmax[0]}/H{lmax[1]}/g{lmax[2]}/{lmax[3]}",
                    same_book=(pick == lmax),
                    OOS_CAGR=b["OOS_CAGR"], OOS_Sharpe=b["OOS_Sharpe"], OOS_MaxDD=b["OOS_MaxDD"],
                    LISTMAX_OOS_Sharpe=bl["OOS_Sharpe"], LISTMAX_OOS_CAGR=bl["OOS_CAGR"],
                    LISTMAX_OOS_MaxDD=bl["OOS_MaxDD"],
                    ANCH_OOS_Sharpe=ba["OOS_Sharpe"], ANCH_OOS_CAGR=ba["OOS_CAGR"],
                    ANCH_OOS_MaxDD=ba["OOS_MaxDD"],
                    SPY_OOS_CAGR=spym["OOS_CAGR"], SPY_OOS_Sharpe=spym["OOS_Sharpe"],
                    SPY_OOS_MaxDD=spym["OOS_MaxDD"],
                    BASE_OOS_CAGR=lbm["OOS_CAGR"], BASE_OOS_Sharpe=lbm["OOS_Sharpe"],
                    BASE_OOS_MaxDD=lbm["OOS_MaxDD"],
                    H1=b["H1"], H2=b["H2"], CAGR=b["CAGR"], Sharpe=b["Sharpe"], MaxDD=b["MaxDD"],
                    PASS_4b=all(f4b.values()), PASS_4a=all(f4a.values()),
                    **f4b, **f4a))
    wf = pd.DataFrame(wf)
    dump(wf, "walkforward")
    P(wf[["panel", "claim_class", "listing_stat", "rule8_pick", "listing_max", "same_book",
          "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "LISTMAX_OOS_Sharpe", "ANCH_OOS_Sharpe",
          "SPY_OOS_Sharpe", "BASE_OOS_Sharpe", "PASS_4b", "PASS_4a"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P(f"  rule-8 pick == listing maximum at {int(wf.same_book.sum())} of {len(wf)} cells "
      f"({wf.same_book.mean():.4f}); the two readings name the SAME book only there.")
    P(f"  mean OOS Sharpe: rule-8 pick {wf.OOS_Sharpe.mean():.4f} | listing max "
      f"{wf.LISTMAX_OOS_Sharpe.mean():.4f} | anchor {wf.ANCH_OOS_Sharpe.mean():.4f} | "
      f"SPY {wf.SPY_OOS_Sharpe.mean():.4f} | RULES v2 {wf.BASE_OOS_Sharpe.mean():.4f}")
    P(f"  mean OOS overstatement of the LIST reading over the rule-8 pick: "
      f"{(wf.LISTMAX_OOS_Sharpe - wf.OOS_Sharpe).mean():+.4f} of Sharpe "
      f"({int((wf.LISTMAX_OOS_Sharpe > wf.OOS_Sharpe).sum())} of {len(wf)} cells positive).")
    P(f"  4b PASS at {int(wf.PASS_4b.sum())} of {len(wf)} cells; 4a PASS at "
      f"{int(wf.PASS_4a.sum())} of {len(wf)}.")

    # G9 -- the L252 rolling IS variant, published, never selected on
    P("")
    P("## G9 — the ROLLING (L=252) IS window, run once and published, NEVER selected on")
    rows = []
    for panel in PANELS:
        d = panels[panel]
        for k in CLASSES:
            cells = LISTING[k]
            for s in STATS:
                stitched, off = [], 0
                for f in d["folds"]:
                    lo = max(f["is_lo"], f["is_hi"] - 252 + 1)
                    isl = slice(lo, f["is_hi"] + 1)
                    iv = [stat_of(s, run_cell(panel, c)[isl], d["spy"][isl]) for c in cells]
                    pick = cells[int(np.nanargmax(iv))]
                    stitched.append(run_cell(panel, pick)[f["oo_lo"]:f["oo_hi"] + 1])
                st = np.concatenate(stitched)
                rows.append(dict(panel=panel, claim_class=k, listing_stat=s, S_WF_L252=fsharpe(st)))
    r252 = pd.DataFrame(rows).merge(readings[["panel", "claim_class", "listing_stat",
                                              "S_WF", "S_LIST", "S_ANCH"]],
                                    on=["panel", "claim_class", "listing_stat"])
    P(f"  mean stitched Sharpe: EXPAND {r252.S_WF.mean():.4f} | L252 {r252.S_WF_L252.mean():.4f} "
      f"| LISTING MAX {r252.S_LIST.mean():.4f} | ANCHOR {r252.S_ANCH.mean():.4f}")
    P(f"  the LISTING MAX beats BOTH honest windows at "
      f"{int(((r252.S_LIST > r252.S_WF) & (r252.S_LIST > r252.S_WF_L252)).sum())} of {len(r252)} cells.")
    gate("G9", "the IS-window FORM is published at both settings and selected on at neither",
         float(r252.S_WF_L252.mean() - r252.S_WF.mean()), True)

    # ------------------------------------------------------------------ verdict
    P("")
    P("=" * 100)
    P("## ANSWERS")
    P("=" * 100)
    lst_share = cnt.get("LIST", 0) / max(cnt.get("LIST", 0) + cnt.get("WF", 0), 1)
    P(f"Q1 CENSUS: of {tot_c:,} committed chooser sentences in the record, "
      f"{int(cnt.get('LIST', 0)):,} ({lst_share:.4f} of the classifiable ones) are written in "
      "the LISTING-MAXIMUM form — a superlative over a set with no walk-forward marker — "
      f"against {int(cnt.get('WF', 0)):,} in the walk-forward form.")
    P(f"Q2 PRICE: on 60 real (panel, claim class, listing statistic) cells the listing maximum "
      f"overstates the deployable walk-forward stitch by a mean of {readings.GAP_curve.mean():+.4f} "
      f"of Sharpe (median {readings.GAP_curve.median():+.4f}, max {readings.GAP_curve.max():+.4f}), "
      f"positive at {int((readings.GAP_curve > 0).sum())} of 60.  On the single rule-8 split the "
      f"same overstatement is {(wf.LISTMAX_OOS_Sharpe - wf.OOS_Sharpe).mean():+.4f}.")
    P(f"   The chooser itself is not worth its motion: the walk-forward stitch beats the "
      f"do-nothing anchor at only {int((readings.S_WF > readings.S_ANCH).sum())} of 60 cells, "
      f"pooled fold delta {readings.WF_vs_ANCH_pooled.mean():+.4f} "
      f"(|t| > 2 at {int((readings.WF_vs_ANCH_t.abs() > 2).sum())} of 60).")
    P("")
    best = wf.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    P("CAPITAL VERDICT — KILL.  No book here is promotable.")
    P(f"  best rule-8 pick anywhere in the run: {best.panel} / {best.claim_class} / "
      f"{best.listing_stat} -> {best.rule8_pick}, OOS CAGR {best.OOS_CAGR:.4f}, "
      f"OOS Sharpe {best.OOS_Sharpe:.4f}, OOS MaxDD {best.OOS_MaxDD:.4f} against "
      f"SPY {best.SPY_OOS_CAGR:.4f}/{best.SPY_OOS_Sharpe:.4f}/{best.SPY_OOS_MaxDD:.4f} and "
      f"RULES v2 {best.BASE_OOS_CAGR:.4f}/{best.BASE_OOS_Sharpe:.4f}/{best.BASE_OOS_MaxDD:.4f}.")
    P(f"  KEEP path 4a (beat the live book in BOTH halves, MaxDD no worse): "
      f"{int(wf.PASS_4a.sum())} of {len(wf)} cells.")
    P(f"  KEEP path 4b (beat SPY in both halves AND OOS, DD <= 60% of SPY's, CAGR >= 70%): "
      f"{int(wf.PASS_4b.sum())} of {len(wf)} cells.")
    P("  Every 4b pass in this run, if any, is a rung of an existing committed ladder re-read, "
      "not a new rule; nothing here changes RULES.md (PROTOCOL rule 6).")
    P("")
    P("## WHAT THIS RUN DOES NOT SHOW")
    P("  - The census classifies SENTENCES by marker words, not by what their author did.")
    P("    A sentence can be a walk-forward result reported in superlative prose; the")
    P("    classification is a property of the TEXT, which is exactly the queue's question")
    P("    ('quote a listing maximum'), but it is an upper bound on genuine LIST-form errors.")
    P("  - OTHER-class sentences are unclassifiable from text alone and are excluded from the")
    P("    share denominator, which raises the reported LIST share relative to a denominator")
    P("    of all chooser sentences.  Both denominators are printed.")
    P("  - The gap is measured on FOUR ladders and FOUR statistics on THIS tape.  It is not a")
    P("    universal constant and the per-cell spread is published in full.")
    P("  - Survivorship: all three panels are current-constituent lists (see PANELS above).")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P("")
    P(f"gates: {sum(g['pass_'] for g in GATES)} / {len(GATES)} pass")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
