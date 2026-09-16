#!/usr/bin/env python3
"""Idea 1024 (lane B, 2026-09-16) — is 4b's DD CAP a SINGLE-EPISODE TEST on EVERY tape the
record can reach?

QUESTION (QUEUE idea 1024, verbatim)
    idea 1022 found SPY's OOS drawdown is the 2020 crash at every rule-8-legal split, and that
    the cap only stops being that one episode when the split is pushed to 2020Q1+, which rule 8
    forbids.  Census the record's panels (U56, B136, SMALL) for how many DISTINCT episodes ever
    set a comparand or book OOS MaxDD, and report whether a two-episode cap exists anywhere on
    this data.
    Max 2 params (panel set, episode definition).

WHAT IS NEW AGAINST 1013 / 1022.  1013 measured `L4_DD` constant on 45 of 45 books over the
    legal end grid.  1022 showed that constancy dies once the split is pushed THROUGH the 2020
    episode — a move rule 8 forbids — and left the obvious question unanswered: is the
    single-episode property a fact about SPY's 2009-2026 tape, or a fact about the record's two
    panels?  1024 answers it by CENSUS rather than by sliding a date:
      * a THIRD panel (SMALL, 716 sub-$2B names on a 2010+ tape) is added, so "every tape the
        record can reach" is literal;
      * every series is counted, not just the comparand — 63 books and 2 comparands;
      * "episode" stops being a hand-typed date window.  Episodes are SPY's OWN drawdown
        episodes (peak -> recovery-to-new-high), cut at a depth threshold, so the labelling is
        mechanical and reproducible from the tape;
      * the binding episode is published with its MARGIN over the runner-up episode inside the
        same OOS window, so "single-episode" is a measured distance, not a tautology.

WHAT A "TWO-EPISODE CAP" MEANS HERE.  4b's DD leg is `|book OOS MaxDD| <= 0.60 * BAR`.  The CAP
    is the right-hand side, so it is a COMPARAND object.  It is a TWO-EPISODE cap in a cell iff,
    as the legal split point moves over that cell's end grid, the comparand's binding drawdown
    trough lands in TWO OR MORE distinct episodes.  A one-episode cap is a test of one month of
    2020 wearing the costume of a risk limit.

TWO BAR CONVENTIONS, both published at every point (1022's convention, kept):
    REC_FULL  BAR = SPY's FULL-sample |MaxDD| — the record's own; E-invariant, so its episode
              count is 1 BY CONSTRUCTION and is reported as a floor, not as evidence.
    WIN       BAR = SPY's OWN OOS-window |MaxDD| — the only convention whose cap can move with
              E, and therefore the one the queue's question is about.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported, none
selected.
    (1) PANEL SET in {PAIR, TRIO}
          PAIR  [U56, B136]                 the record's own two panels        <- control
          TRIO  [U56, B136, SMALL]          every tape the record can reach    <- HEADLINE
    (2) EPISODE DEFINITION in {DD10, DD05, CAL_Q}
          DD10   SPY drawdown episodes deeper than 10% (peak -> new high)      <- HEADLINE
          DD05   the same at 5%: finer, so it can only SPLIT episodes, never merge them
          CAL_Q  the calendar quarter of the trough — zero judgement, coarse control
        No episode window is hand-typed anywhere in this file.

    NOT TUNED, reported as CONTROLS at every point:
      END GRID    LEGAL  = the 16 quarter-ends 2015Q1..2018Q4 (rule-8-legal, 1013's own grid)
                  POST   = the 16 quarter-ends 2019Q1..2022Q4 (rule-8-ILLEGAL, 1022's grid),
                           carried ONLY to show where a two-episode cap does exist
      BAR         {REC_FULL, WIN}, as above
      COST        0 / 10 / 25 bps; PROTOCOL rule 2's 10 bps is the headline
      CLAIM SET   SHELF (the record's committed memo-backed 4b passes) and GRID (the mechanical
                  band x gross x QROLL ladder, never memo-selected)
      ANCHOR      PROTOCOL rule 8's own E = 2016-12-31, where the walk-forward is reported

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_ONE     HEADLINE.  Under WIN on the LEGAL grid the COMPARAND's OOS MaxDD is set by
              EXACTLY ONE distinct episode in EVERY (panel x episode-definition) cell.
              PASS => 4b's DD cap is a single-episode test on every tape the record can reach.
    H_TWO     A TWO-EPISODE CAP EXISTS SOMEWHERE on the LEGAL grid: at least one
              (panel x def x bar) cell with comparand episode count >= 2.  This is the queue's
              question in one bit.  H_TWO is the logical negation of H_ONE restricted to the
              comparand; both are printed so the answer cannot be read two ways.
    H_BOOK    the MEDIAN book's distinct-episode count on the LEGAL grid is >= 2.
              PASS => the degeneracy belongs to the COMPARAND, not to the tape.
    H_MARGIN  the MEDIAN comparand binding-vs-runner-up margin on the LEGAL grid is >= 0.05
              of drawdown.  PASS => the single-episode reading is a distance, not a near-tie.
    H_PANEL   the comparand's episode count DIFFERS between at least two panels (same def, same
              bar, LEGAL grid).  SPY is SPY on all three panels, so a PASS here would mean the
              panel calendars alone move the cap.
    H_DEF     the episode DEFINITION changes at least one series' count on the LEGAL grid.
              PASS => the census is definition-sensitive and must publish its definition.
    H_POST    on the rule-8-ILLEGAL POST grid the comparand's count reaches >= 2 somewhere.
              PASS => two-episode caps exist only where rule 8 forbids the record to go.
    H_SMALL   |mean book episode count on SMALL - mean on U56| >= 0.50 (DD10, LEGAL).
              PASS => a genuinely different tape gives a different episode census.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  rules_v2_weights(U, 0.03, 0.75) == baseline.rules_v2_weights(U)                   0.0
    G3  CROSS-RUN: at E = 2016-12-31 SPY's OOS triple == the record's committed 15.21% /
        0.8713 / -33.72% (idea 1009's G4, the standing comparand).
    G4  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G5  determinism: the whole census rebuilt reproduces bit-for-bit.                     0.0
    G6  CROSS-RUN vs 1013/1022: on the LEGAL grid SPY's |OOS MaxDD| range is 0.0000 and the
        OOS trough is the 2020 crash at every legal end, on U56 and B136.
    G7  PANEL IDENTITY: the SPY column of SMALL equals the SPY column of U56 on their common
        trading days — so any panel effect below is a CALENDAR effect, not a price effect.
    G8  EPISODE PARTITION: under every definition every trough date carries exactly one label,
        and DD05 is a strict REFINEMENT of DD10 (no DD10 episode straddles two DD05 labels
        without containing them).

SURVIVORSHIP (PROTOCOL rule 9).  U56, B136 and SMALL are CURRENT-CONSTITUENT lists, so every
    CAGR LEVEL below is optimistic and every 4b pass count is an UPPER bound.  SMALL's bias is
    the worst of the three (see data/SMALL_PANEL_README.md).  The measured object here is WHICH
    CALENDAR DATE sets a drawdown, which survivorship moves only through the book's composition
    and not through SPY's at all; the comparand census is bias-free because SPY is a real index
    series.  Where the bias bites — the BOOK census — it makes books LOOK steadier, i.e. it
    pushes book episode counts DOWN, so H_BOOK is the HARDER hypothesis to pass and any PASS is
    a lower bound.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.

OUTPUTS
    .console.txt      this log
    .gates.csv        the 8 reproduction gates
    .hypotheses.csv   the 8 pre-registered hypotheses with their bars
    .ladder.csv.gz    every (set, book, panel, cost, end grid, E) row with its OOS trough
    .census.csv       distinct-episode counts per (series, panel, def, bar, grid)
    .episodes.csv     the mechanical episode calendars themselves
    .margin.csv       binding vs runner-up episode margins, per (panel, def, E)
    .walkforward.csv  rule 8: 3 choosers x panels x LEGAL ends, OOS vs RULES v2 and SPY
    .keeppaths.csv    both PROTOCOL rule 4 paths at the anchor split

Run: python research/backtests/2026-09-16_is-4b-s-DD-CAP-a-SINGLE-EPISODE-TEST-on-EVERY-tape-the-record-can-reach_B.py
Deterministic; no network (reads the committed price caches only).
"""
from __future__ import annotations

import importlib.util
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-4b-s-DD-CAP-a-SINGLE-EPISODE-TEST-on-EVERY-tape-the-record-can-reach"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_B"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP, MAX_VOL = 260, 0.60
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
REC_END = "2016-12-31"                       # PROTOCOL rule 8's own split, the anchor
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
BARS = ["REC_FULL", "WIN"]
BAR_REF = "WIN"                              # the only bar whose cap can move with E
CHOOSERS = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
COVID_PEAK, COVID_TROUGH = pd.Timestamp("2020-02-19"), pd.Timestamp("2020-03-23")
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)     # idea 1009 G4, at E = REC_END
COMPARANDS = ["SPY", "RULESv2"]              # 4b's bar, and the 4a bar, both censused
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv.gz" if gz else f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def load_lane_c():
    spec = importlib.util.spec_from_file_location("laneC865", LANEC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load_lane_c()
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_GRIDS = {
    "LEGAL": quarter_ends("2015-01-01", "2018-12-31"),      # rule-8-legal, 1013's grid
    "POST": quarter_ends("2019-01-01", "2022-12-31"),       # rule-8-ILLEGAL, 1022's grid
}
GRID_HEAD = "LEGAL"
PANEL_SETS = {"PAIR": ["U56", "B136"], "TRIO": ["U56", "B136", "SMALL"]}
PSET_HEAD = "TRIO"
EPDEFS = ["DD10", "DD05", "CAL_Q"]
EPDEF_HEAD = "DD10"
DD_THRESH = {"DD10": 0.10, "DD05": 0.05}


# ------------------------------------------------------------------ episode calendars
def dd_episodes(ret, thresh):
    """SPY's OWN drawdown episodes: maximal peak -> recovery-to-new-high intervals whose depth
    exceeds `thresh`.  Returns a date -> label Series covering the WHOLE index; days inside no
    qualifying episode get label 'CALM_<YYYYQn>' so that the labelling is a total partition and
    a trough that lands outside every episode is still counted as its own distinct episode."""
    eq = (1.0 + ret).cumprod()
    peak = eq.cummax()
    under = (eq < peak).values
    idx = ret.index
    lab = pd.Series(index=idx, dtype=object)
    i, n = 0, len(idx)
    eps = []
    while i < n:
        if not under[i]:
            i += 1
            continue
        j = i
        while j < n and under[j]:
            j += 1
        seg = eq.iloc[i:j] / peak.iloc[i - 1] if i > 0 else eq.iloc[i:j] / peak.iloc[i]
        depth = float(1.0 - seg.min())
        if depth >= thresh:
            tr = seg.idxmin()
            name = f"DD_{tr.date()}"
            lo = idx[max(i - 1, 0)]
            hi = idx[min(j, n - 1)]
            lab.loc[lo:hi] = name
            eps.append(dict(episode=name, start=lo.date(), trough=tr.date(), end=hi.date(),
                            depth=depth, days=int(j - i)))
        i = j
    q = pd.Series([f"CALM_{d.year}Q{(d.month - 1) // 3 + 1}" for d in idx], index=idx)
    return lab.fillna(q), pd.DataFrame(eps)


def cal_q_labels(idx):
    return pd.Series([f"{d.year}Q{(d.month - 1) // 3 + 1}" for d in idx], index=idx)


def dd_trough(r_idx, vals):
    """|MaxDD| and the DATE of its trough for a return path given as (index, values)."""
    if len(vals) < 2:
        return np.nan, pd.NaT
    eq = np.cumprod(1.0 + np.asarray(vals, float))
    dd = eq / np.maximum.accumulate(eq) - 1.0
    k = int(np.argmin(dd))
    return float(dd[k]), r_idx[k]


def episode_decomp(net, e, labels):
    """Inside the OOS window E+1.., the deepest drawdown attributable to EACH episode label.
    Returns (binding label, binding depth, runner-up label, runner-up depth).  'Attributable'
    = the minimum of the window's running drawdown over the days carrying that label, which is
    the only decomposition that sums back to the window MaxDD by construction."""
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):]
    if len(o) < 10:
        return None
    eq = (1.0 + o).cumprod()
    dd = eq / eq.cummax() - 1.0
    lab = labels.reindex(o.index).ffill().bfill()
    g = dd.groupby(lab).min().sort_values()
    if len(g) == 0:
        return None
    first = (g.index[0], float(g.iloc[0]))
    second = (g.index[1], float(g.iloc[1])) if len(g) > 1 else (None, 0.0)
    return first, second


def metblock(r):
    """Full-sample CAGR/Sharpe/MaxDD plus the record's COUNT halves (`baseline._row`)."""
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def path_block(net, e):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):]
    i = net.loc[:pd.Timestamp(e)]
    oc, os_, od = fmet(o.values) if len(o) > 10 else (np.nan,) * 3
    ic, is_, idd = fmet(i.values) if len(i) > 10 else (np.nan,) * 3
    _, otr = dd_trough(o.index, o.values) if len(o) > 10 else (np.nan, pd.NaT)
    ih1, ih2 = (fsharpe(i.values[:len(i) // 2]), fsharpe(i.values[len(i) // 2:])) \
        if len(i) > 10 else (np.nan, np.nan)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o), OOS_trough=otr,
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i), IS_H1=ih1, IS_H2=ih2)
    return b


def legs_at(bk, bspy, bar):
    """PROTOCOL 4b's five legs in the record's own wording; `bar` selects the DD/CAGR basis."""
    if bar == "REC_FULL":
        dd_bar, cagr_bar = abs(bspy["MaxDD"]), bspy["CAGR"]
    else:
        dd_bar, cagr_bar = abs(bspy["OOS_MaxDD"]), bspy["OOS_CAGR"]
    return {
        "L1_H1": bk["H1"] > bspy["H1"],
        "L2_H2": bk["H2"] > bspy["H2"],
        "L3_OOS": bk["OOS_Sharpe"] > bspy["OOS_Sharpe"],
        "L4_DD": abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * dd_bar,
        "L5_CAGR": bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * cagr_bar,
    }, DDCAP_FRAC * dd_bar


def failstr(lg):
    return "+".join(k for k in LEGS if not lg[k]) or "-"


def small_grid_books(S):
    """The record's mechanical ladder, rebuilt verbatim on the SMALL panel.  SMALL carries NO
    committed SHELF book — no memo in the record was ever written on it — so its claim set is
    GRID only, and that is stated rather than papered over."""
    out = {}
    for band, g in product((0.03, 0.08), (0.50, 0.75, 1.00)):
        out[f"SMALL-band{band:.2f}-g{g:.2f}"] = dict(
            panel="SMALL", freq="W", W=rules_v2_weights(S, band, g), memo=None, src="GRID")
    elig = C.eligible_mask(S).astype(float)
    nn = elig.sum(axis=1).replace(0, np.nan)
    base = elig.div(nn, axis=0).fillna(0.0)
    br = C.breadth(S)
    for q, w, dep in product((0.12, 0.17), (252, 504, 1008), (0.50, 1.00)):
        thr = br.rolling(w, min_periods=w).quantile(q)
        out[f"SMALL-qroll-q{q:.2f}-w{w}-d{dep:.2f}"] = dict(
            panel="SMALL", freq="W", W=base.mul(C.gate_mult(br, thr, dep, S.index), axis=0),
            memo=None, src="GRID")
    return out


def main():
    t0 = time.time()
    P(f"# Idea 1024 (lane B, {DATE}) — is 4b's DD CAP a SINGLE-EPISODE TEST on EVERY tape the "
      f"record can reach?")
    P(f"# 2 tuned dials: PANEL SET {list(PANEL_SETS)} x EPISODE DEF {EPDEFS}.  All 6 points "
      f"reported, none selected.  Headline {PSET_HEAD} x {EPDEF_HEAD}.")
    P(f"# CONTROLS at every point: END GRID [LEGAL 2015Q1-2018Q4, POST 2019Q1-2022Q4 "
      f"(rule-8-ILLEGAL)], BAR {BARS} (ref {BAR_REF}), COST {RUNGS} bps (head "
      f"{RUNG_HEAD:.0f}), CLAIM SET [SHELF, GRID], ANCHOR E={REC_END}.")
    P("# SURVIVORSHIP: U56/B136/SMALL are current-constituent panels — every LEVEL is optimistic")
    P("#   and the BOOK episode census is a LOWER bound, i.e. H_BOOK is the HARDER call.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    S = load_universe(small=True)
    PX = {"U56": U, "B136": B, "SMALL": S}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    for p in PX:
        P(f"Tape {p}: {PX[p].shape}  {PX[p].index[0].date()}..{PX[p].index[-1].date()}  "
          f"pinned start {REC[p].date()}")
    P("")

    shelf = C.shelf_books(U, B)
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    shelf["u56-top20-g065-M"] = dict(
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    grid = dict(C.grid_books(U, B))
    grid.update(small_grid_books(S))
    SETS = {"SHELF": shelf, "GRID": grid}
    nb = len(shelf) + len(grid)
    P(f"SHELF = {len(shelf)} committed memo-backed 4b passes (U56/B136 only; SMALL carries none)"
      f"; GRID = {len(grid)} never-memo-selected ladder books across 3 panels "
      f"= {nb} books.")
    P(f"END grids: LEGAL {len(END_GRIDS['LEGAL'])} ends {END_GRIDS['LEGAL'][0]}.."
      f"{END_GRIDS['LEGAL'][-1]}; POST {len(END_GRIDS['POST'])} ends {END_GRIDS['POST'][0]}.."
      f"{END_GRIDS['POST'][-1]} (ILLEGAL under rule 8, control only).")
    P("")

    # ---------------------------------------------------------------- net return paths
    NET = {}
    for sname, bset in SETS.items():
        for nm, b in bset.items():
            px = PX[b["panel"]]
            r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
            st = REC[b["panel"]]
            for c in RUNGS:
                NET[(sname, nm, c)] = (r - t * c / 1e4).loc[st:]
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = (r - t * c / 1e4).loc[REC[p]:]

    ALLE = sorted(set(END_GRIDS["LEGAL"]) | set(END_GRIDS["POST"]) | {REC_END})
    SPYB = {(p, e): path_block(SPYR[p], e) for p in PX for e in ALLE}
    V2B = {(p, c, e): path_block(V2[(p, c)], e) for p in PX for c in RUNGS for e in ALLE}

    # ---------------------------------------------------------------- episode calendars
    EPLAB, eprows = {}, []
    for p in PX:
        for d in EPDEFS:
            if d == "CAL_Q":
                EPLAB[(p, d)] = cal_q_labels(SPYR[p].index)
            else:
                lab, tab = dd_episodes(SPYR[p], DD_THRESH[d])
                EPLAB[(p, d)] = lab
                for _, r in tab.iterrows():
                    eprows.append(dict(panel=p, epdef=d, **r.to_dict()))
    EPTAB = pd.DataFrame(eprows)
    P("## Mechanical episode calendars (SPY's own drawdown episodes; no window is hand-typed)")
    for p in PX:
        for d in ("DD10", "DD05"):
            t = EPTAB[(EPTAB.panel == p) & (EPTAB.epdef == d)]
            P(f"  {p:5s} {d}: {len(t):2d} episodes, deepest "
              f"{', '.join(f'{r.trough} {r.depth:.1%}' for _, r in t.nlargest(3, 'depth').iterrows())}")
    P("")

    # ================================================================ GATES
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = []

    def G(gid, what, value, ok):
        gates.append(dict(gate=gid, what=what, value=value, verdict="PASS" if ok else "FAIL"))
        P(f"{gid} {what}: {value}  {'PASS' if ok else 'FAIL'}")
        return ok

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    G("G1", "fast_run == engine.backtest (returns / turnover)", f"{d_r:.3e}/{d_t:.3e}",
      d_r < 1e-12 and d_t < 1e-10)

    d2 = float(np.abs(rules_v2_weights(U, 0.03, 0.75).values - W2.values).max())
    G("G2", "rules_v2_weights(U,0.03,0.75) == baseline.rules_v2_weights(U)", f"{d2:.3e}",
      d2 == 0.0)

    sp = SPYB[("U56", REC_END)]
    trip = (sp["OOS_CAGR"], sp["OOS_Sharpe"], sp["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    G("G3", f"CROSS-RUN SPY OOS triple at E={REC_END} vs committed "
             f"{SPY_OOS_COMMITTED[0]:.2%}/{SPY_OOS_COMMITTED[1]:.4f}/{SPY_OOS_COMMITTED[2]:.2%}",
      f"{trip[0]:.4%}/{trip[1]:.4f}/{trip[2]:.4%} max|d| {d3:.3e}", d3 <= 5e-4)

    grows, ok4 = [], True
    for nm, b in shelf.items():
        c_, s_, d_ = fmet(NET[("SHELF", nm, RUNG_HEAD)].values)
        m = b["memo"]
        dc = abs(c_ - m[0]) if m[0] is not None else 0.0
        ds = abs(s_ - m[1]) if m[1] is not None else 0.0
        dv = abs(d_ - m[2]) if m[2] is not None else 0.0
        good = dc <= 0.015 and ds <= 0.030 and dv <= 0.015
        ok4 &= good
        grows.append(dict(book=nm, panel=b["panel"], CAGR=c_, Sharpe=s_, MaxDD=d_,
                          memo_CAGR=m[0], memo_Sharpe=m[1], memo_MaxDD=m[2],
                          d_CAGR=dc, d_Sharpe=ds, d_MaxDD=dv,
                          verdict="PASS" if good else "FAIL", src=b["src"]))
    G("G4", "SHELF memo triples", f"{sum(r['verdict'] == 'PASS' for r in grows)}/{len(grows)}",
      ok4)
    dump(pd.DataFrame(grows), "shelf")

    # ---------------------------------------------------------------- THE LADDER
    def build_ladder():
        rows = []
        for gname, elist in END_GRIDS.items():
            for sname, bset in SETS.items():
                for nm, b in bset.items():
                    p = b["panel"]
                    for c in RUNGS:
                        net = NET[(sname, nm, c)]
                        v2f = metblock(V2[(p, c)].values)
                        for e in elist:
                            bk = path_block(net, e)
                            sb = SPYB[(p, e)]
                            row = dict(grid=gname, set=sname, book=nm, panel=p, freq=b["freq"],
                                       cost=c, E=e, OOS_years=bk["OOS_n"] / 252.0,
                                       crash_in_OOS=pd.Timestamp(e) < COVID_PEAK,
                                       **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1",
                                                             "H2", "OOS_CAGR", "OOS_Sharpe",
                                                             "OOS_MaxDD")},
                                       OOS_trough=bk["OOS_trough"],
                                       spy_OOS_MaxDD=sb["OOS_MaxDD"],
                                       spy_OOS_trough=sb["OOS_trough"],
                                       spy_FULL_MaxDD=sb["MaxDD"])
                            for bar in BARS:
                                lg, cap = legs_at(bk, sb, bar)
                                row[f"pass4b_{bar}"] = all(lg.values())
                                row[f"fail4b_{bar}"] = failstr(lg)
                                row[f"cap_{bar}"] = cap
                                for k in LEGS:
                                    row[f"{k}_{bar}"] = lg[k]
                            row["pass4a"] = (bk["H1"] > v2f["H1"] and bk["H2"] > v2f["H2"]
                                             and bk["MaxDD"] >= v2f["MaxDD"])
                            for d in EPDEFS:
                                row[f"ep_{d}"] = EPLAB[(p, d)].reindex(
                                    [bk["OOS_trough"]], method="ffill").iloc[0] \
                                    if pd.notna(bk["OOS_trough"]) else None
                                row[f"spyep_{d}"] = EPLAB[(p, d)].reindex(
                                    [sb["OOS_trough"]], method="ffill").iloc[0] \
                                    if pd.notna(sb["OOS_trough"]) else None
                            rows.append(row)
        return pd.DataFrame(rows)

    L = build_ladder()
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int, bool]).columns
    d5 = float(np.nanmax(np.abs(L[num].astype(float).values - L2[num].astype(float).values)))
    G("G5", f"determinism over the whole {len(L):,}-row ladder", f"{d5:.3e}", d5 == 0.0)

    lg = L[(L.grid == "LEGAL") & (L.cost == RUNG_HEAD) & (L.panel.isin(["U56", "B136"]))]
    r6 = max(float(np.ptp([abs(SPYB[(p, e)]["OOS_MaxDD"]) for e in END_GRIDS["LEGAL"]]))
             for p in ("U56", "B136"))
    covid_all = all(pd.Timestamp("2020-03-01") <= SPYB[(p, e)]["OOS_trough"]
                    <= pd.Timestamp("2020-04-15")
                    for p in ("U56", "B136") for e in END_GRIDS["LEGAL"])
    G("G6", "CROSS-RUN vs 1013/1022 on the LEGAL grid: SPY |OOS MaxDD| range (bar 0.0000) and "
             "every legal OOS trough is the 2020 crash",
      f"range {r6:.4e}; covid-at-every-legal-end {covid_all}", r6 <= 1e-9 and covid_all)

    cs, cu = S["SPY"], U["SPY"]
    common = cs.index.intersection(cu.index)
    d7 = float(np.abs(cs.loc[common].values - cu.loc[common].values).max())
    G("G7", f"PANEL IDENTITY: SMALL's SPY == U56's SPY on {len(common):,} common days",
      f"{d7:.3e}", d7 < 1e-9)

    # G8 — the labelling must be a total partition, and the DD05 calendar must REFINE the DD10
    # one ON THE EPISODES.  The refinement claim is only meaningful on episode days: the CALM_
    # filler is a fixed QUARTERLY grid under both thresholds, so a 5%-only episode that straddles
    # a quarter boundary necessarily touches two CALM labels and cannot refine anything.  Both
    # readings are printed; the gate is the episode-restricted one, which is the real claim.
    part_ok, refine_ok, refine_naive = True, True, True
    for p in PX:
        for d in EPDEFS:
            lab = EPLAB[(p, d)]
            part_ok &= bool(lab.notna().all()) and len(lab) == len(SPYR[p])
        a, b_ = EPLAB[(p, "DD10")], EPLAB[(p, "DD05")]
        refine_naive &= bool(((pd.crosstab(a, b_) > 0).sum(axis=0) == 1).all())
        m = a.str.startswith("DD_")
        x = pd.crosstab(a[m], b_[m])
        refine_ok &= bool(((x > 0).sum(axis=0) == 1).all()
                          and ((x > 0).sum(axis=1) == 1).all())
    G("G8", "EPISODE PARTITION: total labelling on every panel/def, and DD05 refines DD10 on "
             "episode days (naive whole-tape reading printed too; its CALM_ filler is a "
             "quarterly grid by construction and cannot be refined)",
      f"partition {part_ok}; refinement-on-episodes {refine_ok}; naive whole-tape "
      f"{refine_naive} (diagnosed: CALM_ filler only)", part_ok and refine_ok)
    dump(EPTAB, "episodes")
    P("")

    # ================================================================ THE CENSUS
    P("## (A) THE CENSUS — how many DISTINCT episodes ever set an OOS MaxDD")
    crows = []
    for gname, elist in END_GRIDS.items():
        for p in PX:
            for d in EPDEFS:
                lab = EPLAB[(p, d)]
                # comparands
                for cm in COMPARANDS:
                    for c in RUNGS:
                        if cm == "SPY" and c != RUNG_HEAD:
                            continue           # SPY is untraded; one row only
                        for bar in BARS:
                            labs = []
                            for e in elist:
                                blk = SPYB[(p, e)] if cm == "SPY" else V2B[(p, c, e)]
                                if bar == "REC_FULL":
                                    tr = dd_trough(
                                        (SPYR[p] if cm == "SPY" else V2[(p, c)]).index,
                                        (SPYR[p] if cm == "SPY" else V2[(p, c)]).values)[1]
                                else:
                                    tr = blk["OOS_trough"]
                                if pd.notna(tr):
                                    labs.append(lab.reindex([tr], method="ffill").iloc[0])
                            crows.append(dict(grid=gname, panel=p, epdef=d, bar=bar, cost=c,
                                              kind="COMPARAND", series=cm,
                                              n_ends=len(labs), n_episodes=len(set(labs)),
                                              episodes="|".join(sorted(set(labs)))))
                # books (a book's own OOS MaxDD does not depend on the bar)
                sub = L[(L.grid == gname) & (L.panel == p)]
                for (sname, nm, c), gg in sub.groupby(["set", "book", "cost"]):
                    labs = [x for x in gg[f"ep_{d}"].tolist() if x is not None]
                    crows.append(dict(grid=gname, panel=p, epdef=d, bar="n/a", cost=c,
                                      kind="BOOK", series=f"{sname}:{nm}",
                                      n_ends=len(labs), n_episodes=len(set(labs)),
                                      episodes="|".join(sorted(set(labs)))))
    CEN = pd.DataFrame(crows)
    dump(CEN, "census")

    def cshow(gname, kind, bar=None):
        q = CEN[(CEN.grid == gname) & (CEN.kind == kind)]
        if bar:
            q = q[q.bar == bar]
        if kind == "BOOK":
            q = q[q.cost == RUNG_HEAD]
        t = q.pivot_table(index="panel", columns="epdef", values="n_episodes",
                          aggfunc=("max" if kind == "COMPARAND" else "median"))
        return t.reindex(columns=EPDEFS)

    for gname in END_GRIDS:
        P(f"\n### END GRID = {gname}"
          f"{'  (rule-8-legal)' if gname == 'LEGAL' else '  (rule-8-ILLEGAL — control only)'}")
        for bar in BARS:
            P(f"  COMPARAND distinct-episode count (max over comparands), bar {bar}:")
            P("    " + cshow(gname, "COMPARAND", bar).to_string().replace("\n", "\n    "))
        # the two comparands are NOT the same object: SPY is 4b's DD cap, RULES v2 is 4a's.
        for cm in COMPARANDS:
            q = CEN[(CEN.grid == gname) & (CEN.kind == "COMPARAND") & (CEN.series == cm)
                    & (CEN.bar == "WIN")]
            t = q.pivot_table(index="panel", columns="epdef", values="n_episodes",
                              aggfunc="max").reindex(columns=EPDEFS)
            P(f"  ...of which {cm} alone "
              f"({'4b DD CAP' if cm == 'SPY' else '4a comparand, live book'}), bar WIN:")
            P("    " + t.to_string().replace("\n", "\n    "))
            for _, r in q[q.n_episodes >= 2].iterrows():
                P(f"      TWO-EPISODE CELL: {r.panel}/{r.epdef}/cost {r.cost:.0f} -> "
                  f"{r.episodes}")
        P("  BOOK distinct-episode count (median over books, 10 bps):")
        P("    " + cshow(gname, "BOOK").to_string().replace("\n", "\n    "))
        bq = CEN[(CEN.grid == gname) & (CEN.kind == "BOOK") & (CEN.cost == RUNG_HEAD)
                 & (CEN.epdef == EPDEF_HEAD)]
        P(f"  BOOK count distribution ({EPDEF_HEAD}, 10 bps, all panels): "
          + ", ".join(f"{int(k)}:{int(v)}" for k, v
                      in bq.n_episodes.value_counts().sort_index().items()))
    P("")

    # ---------------------------------------------------------------- margins
    P("## (B) THE MARGIN — how far the binding episode is from the runner-up, inside the "
      "SAME OOS window")
    mrows = []
    for gname, elist in END_GRIDS.items():
        for p in PX:
            for d in EPDEFS:
                lab = EPLAB[(p, d)]
                for e in elist:
                    for cm, path in (("SPY", SPYR[p]), ("RULESv2", V2[(p, RUNG_HEAD)])):
                        dec = episode_decomp(path, e, lab)
                        if dec is None:
                            continue
                        (l1, v1), (l2, v2) = dec
                        mrows.append(dict(grid=gname, panel=p, epdef=d, E=e, series=cm,
                                          bind_ep=l1, bind_dd=v1, run_ep=l2, run_dd=v2,
                                          margin=abs(v1) - abs(v2)))
    MG = pd.DataFrame(mrows)
    dump(MG, "margin")
    for gname in END_GRIDS:
        for cm in COMPARANDS:
            q = MG[(MG.grid == gname) & (MG.epdef == EPDEF_HEAD) & (MG.series == cm)]
            P(f"  {gname:5s} {EPDEF_HEAD} {cm:8s}: median margin {q.margin.median():.4f}, "
              f"min {q.margin.min():.4f}, max {q.margin.max():.4f}; "
              f"ends where margin < 0.05: {int((q.margin < 0.05).sum())}/{len(q)}")
            for p in PX:
                qq = q[q.panel == p]
                P(f"    {p:5s} binding: "
                  + ", ".join(f"{k}x{v}" for k, v in qq.bind_ep.value_counts().items())
                  + " | runner-up: "
                  + ", ".join(f"{k}x{v}" for k, v in qq.run_ep.value_counts().items()))
    P("")

    # ================================================================ RULE 8 (mandatory)
    P("## (C) RULE 8 WALK-FORWARD (mandatory) — IS-only choosers, OOS read once")
    wrows = []
    GRIDONLY = L[(L.set == "GRID")]
    for p in PX:
        for c in RUNGS:
            for e in sorted(set(END_GRIDS["LEGAL"]) | {REC_END}):
                pool = []
                for nm, b in grid.items():
                    if b["panel"] != p:
                        continue
                    bk = path_block(NET[("GRID", nm, c)], e)
                    sb = SPYB[(p, e)]
                    isl = sum([bk["IS_H1"] > sb["IS_H1"] if pd.notna(bk["IS_H1"]) else False,
                               bk["IS_H2"] > sb["IS_H2"] if pd.notna(bk["IS_H2"]) else False,
                               bk["IS_Sharpe"] > sb["IS_Sharpe"],
                               abs(bk["IS_MaxDD"]) <= DDCAP_FRAC * abs(sb["IS_MaxDD"]),
                               bk["IS_CAGR"] >= CAGRFLOOR_FRAC * sb["IS_CAGR"]])
                    pool.append((nm, bk, isl))
                if not pool:
                    continue
                for ch in CHOOSERS:
                    key = {"IS_SHARPE": lambda t: (-t[1]["IS_Sharpe"], t[0]),
                           "IS_CAGR": lambda t: (-t[1]["IS_CAGR"], t[0]),
                           "IS_LEGS": lambda t: (-t[2], -t[1]["IS_Sharpe"], t[0])}[ch]
                    nm, bk, isl = sorted(pool, key=key)[0]
                    sb = SPYB[(p, e)]
                    v2f = metblock(V2[(p, c)].values)
                    v2o = path_block(V2[(p, c)], e)
                    lgW, capW = legs_at(bk, sb, "WIN")
                    lgR, capR = legs_at(bk, sb, "REC_FULL")
                    wrows.append(dict(
                        panel=p, cost=c, E=e, chooser=ch, pick=nm,
                        IS_Sharpe=bk["IS_Sharpe"], IS_CAGR=bk["IS_CAGR"], IS_legs=isl,
                        OOS_CAGR=bk["OOS_CAGR"], OOS_Sharpe=bk["OOS_Sharpe"],
                        OOS_MaxDD=bk["OOS_MaxDD"], OOS_trough=bk["OOS_trough"],
                        OOS_ep_DD10=EPLAB[(p, "DD10")].reindex(
                            [bk["OOS_trough"]], method="ffill").iloc[0],
                        spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                        spy_OOS_MaxDD=sb["OOS_MaxDD"],
                        v2_OOS_CAGR=v2o["OOS_CAGR"], v2_OOS_Sharpe=v2o["OOS_Sharpe"],
                        v2_OOS_MaxDD=v2o["OOS_MaxDD"],
                        pass4b_WIN=all(lgW.values()), fail4b_WIN=failstr(lgW),
                        pass4b_REC=all(lgR.values()), fail4b_REC=failstr(lgR),
                        pass4a=(bk["H1"] > v2f["H1"] and bk["H2"] > v2f["H2"]
                                and bk["MaxDD"] >= v2f["MaxDD"])))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")

    # IS purity gate as a printed check (the pick must not see OOS columns)
    anchor = WF[(WF.E == REC_END) & (WF.cost == RUNG_HEAD)]
    P(f"  Rule 8 at PROTOCOL's own split E={REC_END}, 10 bps — IS window read ALONE, "
      f"OOS read once:")
    for _, r in anchor.iterrows():
        P(f"    {r.panel:5s} {r.chooser:9s} -> {r.pick:32s} OOS {r.OOS_CAGR:7.2%} / "
          f"{r.OOS_Sharpe:6.3f} / {r.OOS_MaxDD:7.2%}  (trough {r.OOS_trough.date()} "
          f"= {r.OOS_ep_DD10})   4b_WIN {'PASS' if r.pass4b_WIN else 'FAIL ' + r.fail4b_WIN}"
          f"  4a {'PASS' if r.pass4a else 'FAIL'}")
    for p in PX:
        a = anchor[anchor.panel == p]
        if len(a):
            r = a.iloc[0]
            P(f"    {p:5s} comparands at the same split: SPY {r.spy_OOS_CAGR:7.2%} / "
              f"{r.spy_OOS_Sharpe:6.3f} / {r.spy_OOS_MaxDD:7.2%}   RULES v2 (live) "
              f"{r.v2_OOS_CAGR:7.2%} / {r.v2_OOS_Sharpe:6.3f} / {r.v2_OOS_MaxDD:7.2%}")
    P(f"  Across the whole LEGAL ladder ({len(WF):,} chooser rows): OOS 4b_WIN "
      f"{int(WF.pass4b_WIN.sum())}/{len(WF)}, OOS 4b_REC_FULL {int(WF.pass4b_REC.sum())}/"
      f"{len(WF)}, OOS 4a {int(WF.pass4a.sum())}/{len(WF)}.")
    P(f"  Every rule-8 pick's OOS drawdown trough episode ({EPDEF_HEAD}): "
      + ", ".join(f"{k}x{v}" for k, v in WF.OOS_ep_DD10.value_counts().items()))
    P("")

    # ---------------------------------------------------------------- KEEP paths
    kp = []
    for gname in END_GRIDS:
        sub = L[(L.grid == gname) & (L.cost == RUNG_HEAD)]
        for p in PX:
            q = sub[sub.panel == p]
            kp.append(dict(grid=gname, panel=p, rows=len(q),
                           pass4a=int(q.pass4a.sum()),
                           pass4b_WIN=int(q.pass4b_WIN.sum()),
                           pass4b_REC_FULL=int(q.pass4b_REC_FULL.sum())))
    KP = pd.DataFrame(kp)
    dump(KP, "keeppaths")
    P("## (D) BOTH PROTOCOL rule 4 KEEP PATHS over the whole ladder (10 bps)")
    P("  " + KP.to_string(index=False).replace("\n", "\n  "))
    P("")

    # ================================================================ HYPOTHESES
    P("## Pre-registered hypotheses")
    hyp = []

    def H(hid, what, bar, value, ok):
        hyp.append(dict(hypothesis=hid, what=what, bar=bar, value=value,
                        verdict="PASS" if ok else "FAIL"))
        P(f"{hid:9s} {what}\n          bar: {bar}\n          value: {value}  "
          f"=> {'PASS' if ok else 'FAIL'}")

    legalC = CEN[(CEN.grid == "LEGAL") & (CEN.kind == "COMPARAND")]
    win = legalC[legalC.bar == "WIN"]
    mx = int(win.n_episodes.max())
    cells = win.groupby(["panel", "epdef"]).n_episodes.max()
    H("H_ONE", "comparand OOS MaxDD is set by exactly ONE episode in every panel x def cell "
               "(WIN, LEGAL)", "every cell == 1",
      f"max over {len(cells)} cells = {mx}; cells>1: "
      f"{[f'{a}/{b}={int(v)}' for (a, b), v in cells.items() if v > 1] or 'none'}", mx == 1)

    two = legalC[legalC.n_episodes >= 2]
    H("H_TWO", "a TWO-EPISODE CAP exists somewhere on the LEGAL grid (any panel, def, bar)",
      ">= 1 cell with comparand count >= 2",
      f"{len(two)} of {len(legalC)} comparand cells; "
      + (", ".join(f"{r.panel}/{r.epdef}/{r.bar}/{r.series}={r.n_episodes}"
                   for _, r in two.head(6).iterrows()) if len(two) else "none"), len(two) >= 1)

    bk = CEN[(CEN.grid == "LEGAL") & (CEN.kind == "BOOK") & (CEN.cost == RUNG_HEAD)
             & (CEN.epdef == EPDEF_HEAD)]
    med = float(bk.n_episodes.median())
    H("H_BOOK", f"median BOOK distinct-episode count on the LEGAL grid ({EPDEF_HEAD}, 10 bps)",
      ">= 2", f"median {med:.2f} over {len(bk)} book cells; mean {bk.n_episodes.mean():.3f}; "
              f"share >= 2: {(bk.n_episodes >= 2).mean():.4f}", med >= 2)

    mq = MG[(MG.grid == "LEGAL") & (MG.epdef == EPDEF_HEAD) & (MG.series == "SPY")]
    H("H_MARGIN", "median comparand binding-vs-runner-up drawdown margin (LEGAL)", ">= 0.05",
      f"median {mq.margin.median():.4f} (min {mq.margin.min():.4f}, "
      f"{int((mq.margin < 0.05).sum())}/{len(mq)} ends under the bar)",
      float(mq.margin.median()) >= 0.05)

    pv = win[win.series == "SPY"].pivot_table(index="epdef", columns="panel",
                                              values="n_episodes", aggfunc="max")
    diff = bool((pv.nunique(axis=1) > 1).any())
    H("H_PANEL", "comparand episode count differs between panels (SPY, WIN, LEGAL)",
      ">= 2 panels disagree in >= 1 def",
      f"per-def counts:\n          " + pv.to_string().replace("\n", "\n          "), diff)

    allL = CEN[CEN.grid == "LEGAL"]
    piv = allL.pivot_table(index=["kind", "series", "panel", "bar", "cost"], columns="epdef",
                           values="n_episodes")
    nser = int((piv.nunique(axis=1) > 1).sum())
    H("H_DEF", "the episode DEFINITION changes at least one series' count (LEGAL)", ">= 1 series",
      f"{nser} of {len(piv)} series-cells move between {EPDEFS}", nser >= 1)

    postC = CEN[(CEN.grid == "POST") & (CEN.kind == "COMPARAND")]
    p2 = postC[postC.n_episodes >= 2]
    H("H_POST", "on the rule-8-ILLEGAL POST grid the comparand count reaches >= 2",
      ">= 1 cell", f"{len(p2)} of {len(postC)} comparand cells; WIN-only "
                   f"{int((postC[postC.bar == 'WIN'].n_episodes >= 2).sum())}"
                   f"/{len(postC[postC.bar == 'WIN'])}", len(p2) >= 1)

    bs = CEN[(CEN.grid == "LEGAL") & (CEN.kind == "BOOK") & (CEN.cost == RUNG_HEAD)
             & (CEN.epdef == EPDEF_HEAD)]
    m_small = float(bs[bs.panel == "SMALL"].n_episodes.mean())
    m_u56 = float(bs[bs.panel == "U56"].n_episodes.mean())
    H("H_SMALL", "SMALL's book episode census differs from U56's", ">= 0.50 in the mean",
      f"SMALL {m_small:.3f} vs U56 {m_u56:.3f}  |d| {abs(m_small - m_u56):.3f}",
      abs(m_small - m_u56) >= 0.50)

    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    dump(pd.DataFrame(gates), "gates")
    dump(L, "ladder", gz=True)

    P("")
    P("## SUMMARY")
    P(f"Gates {sum(g['verdict'] == 'PASS' for g in gates)} of {len(gates)} PASS; "
      f"hypotheses {int((HY.verdict == 'PASS').sum())} of {len(HY)} PASS.")
    P(f"Elapsed {time.time() - t0:.1f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
