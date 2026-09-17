#!/usr/bin/env python3
"""
Idea 1156 (lane cloud, 2026-09-17)
can-a-SPLIT-HALF-claim-be-made-REGIME-CHECKABLE-without-a-THIRD-TAPE

THE QUESTION, AS THE QUEUE PUT IT
---------------------------------
Idea 1148 found that 0 of 2,140,569 committed split-half rows can price the LENGTH axis,
because a half is ONE length, so the regime-to-length clause is unsatisfiable for the
record's commonest sub-tape comparison.  This run prices the three cheap repairs the queue
names — QUARTERS, OVERLAPPING HALVES, and a WITHIN-HALF BLOCK SPREAD as the regime term —
against the full fraction-ladder re-run, on 1148's own 81-book grid.

WHY A HALF CANNOT PRICE LENGTH (the arithmetic, stated before it is measured)
----------------------------------------------------------------------------
The regime-to-length ratio is WITHIN / BETWEEN.  WITHIN is a dispersion of the statistic
over segments OF THE SAME LENGTH; BETWEEN is a contrast of the statistic ACROSS lengths.
A split-half gives two segments at exactly one length, n/2.  The WITHIN term is therefore
available (it is |H1 - H2|) and the BETWEEN term is a contrast over a SINGLE point, which
is not defined.  This is structural, not statistical: no amount of tape fixes it, and
publishing more halves does not fix it either.

THE TWO DIALS AND NO MORE (rule 4 — and the queue names both)
-------------------------------------------------------------
  dial 1  REPAIR     {P_HALF, P_OVERLAP, P_QUARTERS, P_BLOCK}
  dial 2  STATISTIC  {CAGR, VOL, SHARPE, MAXDD, ULCER, CALMAR}
  = 24 cells, EVERY ONE PUBLISHED, at every one of the 81 rung books.

  P_HALF     the status quo.  2 segments at one length n/2.                 cost 2
  P_OVERLAP  half-length windows at tape offsets 0, 1/4, 1/2.  3 segments,
             STILL ONE LENGTH.  PRE-DECLARED UNSATISFIABLE — it buys
             resolution in the WITHIN term and cannot buy a BETWEEN term
             at all.  It is in the grid as the falsification control: if it
             ever scores, this pre-declaration was wrong.                    cost 3
  P_QUARTERS halves PLUS quarters.  6 segments at two lengths n/2, n/4.      cost 6
  P_BLOCK    halves PLUS 3 blocks inside each half.  8 segments at two
             lengths n/2, n/6 — the queue's "within-half block spread as
             the regime term".                                               cost 8

THE REFERENCE IS NOT A DIAL VALUE
---------------------------------
P_FULL, the full re-run, is the TARGET the repairs are priced against, never selected on:
the count-matched regime-to-length ratio on 1158's finest fraction ladder
L8 = {1,2,3,4,5,6,8}, 29 segments over six lengths.  That is 1158's committed resolved
target (R_COUNT at L8), reproduced here and not re-chosen, so this run and 1187's read the
same object.

NOT DIALS: PANEL {U56, B136, SMALL}; the four dial ladders that are the grid's books
(CADENCE, GROSS, H, N = 27 rung books per panel, 81 total, 1148's grid); the WITHIN
statistic (count-matched all-pairs mean |difference|, headline, 1158's); the census; the
rule-8 choosers.  Tape PINNED at 2026-09-15 (idea 1163).

WHAT "CHEAP ENOUGH" MEANS — three legs, declared before any number
------------------------------------------------------------------
  SATISFIABLE  the repair yields >= 2 distinct sub-tape LENGTHS.  Structural, binary.
  LANDS        |r_repair - r_FULL| / |r_FULL| <= 0.25 (1158's landing bar, verbatim).
  ORDERS       Spearman rho between the repair's reading and P_FULL's ACROSS the 27 rung
               books of a (panel, statistic) cell >= 0.50.  This is the leg that matters
               operationally: a cheap repair earns its place only if it RANKS books the
               way the expensive one does, whatever it does to the level.
A repair SERVES iff it is SATISFIABLE and LANDS at a majority of the 81 books and ORDERS
at a majority of the 18 (panel, statistic) cells.

PRE-DECLARED OUTCOMES, SCORED IN THIS ORDER
-------------------------------------------
  (A) BLOCK     the block spread serves, at cost 8 — cheapest satisfiable repair that works
  (B) QUARTERS  quarters serve and the block spread does not
  (C) BOTH      both serve; the record may pick on cost alone
  (D) NEITHER   no cheap repair reproduces the full re-run, i.e. a split-half claim CANNOT
                be made regime-checkable without the third tape, and the honest clause is
                that the record's 2.1M committed split-half rows are not repairable in
                place — they need re-running or they need withdrawing.
  (E) OVERLAP scores — would falsify the pre-declaration above and is reported as such.

KEEP PATHS AND RULE 8 (protocol, mandatory; this run is NOT a capital finding)
-----------------------------------------------------------------------------
A sub-tape reporting repair is not a trading rule and cannot be a KEEP.  Rule 8 is run in
full anyway: all 81 rung books scored against 4a (vs live RULES v2) and 4b (vs SPY) on the
full tape AND out of sample, parameters chosen on 2009-2016 and 2017-2026 read once, with
one chooser per repair plus the honest IS-Sharpe incumbent, so the reader can see whether
the choice of repair moves a capital decision.  Every book and every pick is published.

SURVIVORSHIP: the SMALL panel is current constituents of a sub-$2B screen (see
data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first.  Its levels are optimistic and every 4a/4b count on it is an UPPER bound.
"""
import sys
import time
import warnings
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

# An all-NaN median is an EXPECTED reading here, not a defect: P_HALF and P_OVERLAP have no
# BETWEEN term at all, so their ratio column is NaN by construction and is printed as
# "undef".  The warning is silenced; the undefinedness is published.
warnings.filterwarnings("ignore", message="All-NaN slice encountered")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "can-a-SPLIT-HALF-claim-be-made-REGIME-CHECKABLE-without-a-THIRD-TAPE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent

PIN = "2026-09-15"
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136", "SMALL"]
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"CADENCE": LAD_C, "GROSS": LAD_G, "H": LAD_H, "N": LAD_N}
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)

STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]               # dial 2
REPAIRS = ["P_HALF", "P_OVERLAP", "P_QUARTERS", "P_BLOCK"]                   # dial 1
SEG_COST = {"P_HALF": 2, "P_OVERLAP": 3, "P_QUARTERS": 6, "P_BLOCK": 8, "P_FULL": 29}
FULL_LADDER = [1, 2, 3, 4, 5, 6, 8]          # 1158's L8, the reference's fraction ladder
OVERLAP_OFFSETS = (0.0, 0.25, 0.5)
N_BLOCKS = 3

LAND_BAR = 0.25       # 1158's landing bar, verbatim
RHO_BAR = 0.50        # the ordering bar
HEAD_STAT = "MAXDD"

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
DD_COMMITTED = {"U56": -19.127569, "B136": -20.740302, "SMALL": -35.814054}
# 1158/1187's committed C_POOLED/ALIGNED resolved target (R_COUNT @ L8), SMALL / MAXDD
RESOLVED_1158_SMALL_MAXDD = 1.173713969601412

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
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what}   (dev {value:.3e})")


# ---------------------------------------------------------------- kernel (1082/1157/1158)
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
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_scores(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
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


def six_stats(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return {k: np.nan for k in STATS6}
    eq = np.cumprod(1.0 + r)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    vol = r.std(ddof=1) * np.sqrt(252.0)
    mdd = float(dd.min())
    return {"CAGR": cagr * 100.0, "VOL": vol * 100.0,
            "SHARPE": (r.mean() * 252.0 / vol if vol else np.nan),
            "MAXDD": mdd * 100.0, "ULCER": float(np.sqrt((dd ** 2).mean())) * 100.0,
            "CALMAR": (cagr / abs(mdd) if mdd < 0 else np.nan)}


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def blocks_m(r, ins, oos):
    c, s, d = fmet(r)
    h = len(r) // 2
    ic, is_, idd = fmet(r[ins])
    oc, os_, od = fmet(r[oos])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def matched_exact(v):
    """1158's count-matched statistic: the exact mean |difference| over all C(k,2) pairs."""
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    return float(np.mean([abs(a - b) for a, b in combinations(v, 2)]))


# --------------------------------------------------- THE FOUR SEGMENTATIONS + REFERENCE
def segments(r, repair):
    """Return {length_label: [segment, ...]}.  The KEY is the segment LENGTH — the whole
    question is how many distinct keys a repair produces."""
    n = len(r)
    if repair == "P_HALF":
        L = n // 2
        return {L: [r[:L], r[L:2 * L]]}
    if repair == "P_OVERLAP":
        L = n // 2
        segs = []
        for o in OVERLAP_OFFSETS:
            s = int(round(o * n))
            if s + L <= n:
                segs.append(r[s:s + L])
        return {L: segs}
    if repair == "P_QUARTERS":
        L2, L4 = n // 2, n // 4
        return {L2: [r[:L2], r[L2:2 * L2]],
                L4: [r[k * L4:(k + 1) * L4] for k in range(4)]}
    if repair == "P_BLOCK":
        L2 = n // 2
        halves = [r[:L2], r[L2:2 * L2]]
        LB = L2 // N_BLOCKS
        blocks = [h[k * LB:(k + 1) * LB] for h in halves for k in range(N_BLOCKS)]
        return {L2: halves, LB: blocks}
    raise ValueError(repair)


def segments_full(r):
    """The reference: 1158's L8 fraction ladder, aligned partition, 29 segments."""
    n = len(r)
    out = {}
    for f in FULL_LADDER:
        L = n // f
        if L < 3:
            continue
        out[L] = [r[k * L:(k + 1) * L] for k in range(f)]
    return out


def ratio_of(segmap, stat):
    """WITHIN / BETWEEN, both count-matched, on whatever segmentation is handed in.
    WITHIN  = median over lengths (with >= 2 segments) of the all-pairs mean |difference|.
    BETWEEN = the all-pairs mean |difference| of the per-length MEDIANS.
    Returns (within, between, ratio, n_lengths, n_segments)."""
    per_len, withins = {}, []
    nseg = 0
    for L, segs in segmap.items():
        vals = [six_stats(s)[stat] for s in segs]
        vals = [v for v in vals if np.isfinite(v)]
        nseg += len(segs)
        if not vals:
            continue
        per_len[L] = float(np.median(vals))
        if len(vals) >= 2:
            m = matched_exact(vals)
            if np.isfinite(m):
                withins.append(m)
    nlen = len(per_len)
    w = float(np.median(withins)) if withins else np.nan
    b = matched_exact(list(per_len.values())) if nlen >= 2 else np.nan
    r = (w / b) if (np.isfinite(w) and np.isfinite(b) and b != 0) else np.nan
    return w, b, r, nlen, nseg


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(meta), len(meta) - (len(keep) - 1)


# ---------------------------------------------------------------- the census
HALF_SETS = [("H1", "H2"), ("IS_Sharpe", "OOS_Sharpe"), ("IS_CAGR", "OOS_CAGR"),
             ("IS_MaxDD", "OOS_MaxDD"), ("first_half", "second_half"), ("h1", "h2")]
LENGTH_COLS = {"frac", "fraction", "fracs", "frac_ladder", "n_days", "length", "seg_len",
               "sub_len", "L", "window", "tape_len", "n_bars"}


def census():
    """Every committed CSV in research/backtests that carries a SPLIT-HALF column pair, and
    whether that same file carries ANY column that could supply a SECOND sub-tape length."""
    rows = []
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(f"{DATE}_{SLUG}"):
            continue
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cols = set(head.columns)
        pairs = [p for p in HALF_SETS if p[0] in cols and p[1] in cols]
        if not pairs:
            continue
        try:
            n = sum(1 for _ in open(f, "r", errors="ignore")) - 1
        except Exception:
            n = np.nan
        lcols = sorted(cols & LENGTH_COLS)
        nlen = np.nan
        if lcols:
            try:
                d = pd.read_csv(f, usecols=lcols)
                nlen = int(max(d[c].nunique(dropna=True) for c in lcols))
            except Exception:
                nlen = np.nan
        rows.append(dict(file=f.name, n_rows=n,
                         half_pairs="+".join("/".join(p) for p in pairs),
                         length_cols="+".join(lcols), n_distinct_lengths=nlen,
                         can_price_length=bool(np.isfinite(nlen) and nlen >= 2)))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    P(f"# Idea 1156 (lane cloud, {DATE}) — can a SPLIT-HALF claim be made REGIME-CHECKABLE")
    P("# without a THIRD TAPE?")
    P(f"# 2 tuned dials: REPAIR {REPAIRS} x STATISTIC {STATS6} = 24 cells, EVERY ONE")
    P("#   PUBLISHED at every one of the 81 rung books.")
    P("# SEGMENT COSTS: " + ", ".join(f"{k} {v}" for k, v in SEG_COST.items()) + ".")
    P("# P_OVERLAP is PRE-DECLARED UNSATISFIABLE (3 windows, still ONE length) and is in")
    P("#   the grid as the falsification control — if it scores, the pre-declaration was")
    P("#   wrong and this run says so.")
    P("# THE REFERENCE IS NOT A DIAL VALUE: P_FULL = 1158's committed resolved target, the")
    P(f"#   count-matched ratio on the finest fraction ladder L8 = {FULL_LADDER}, 29 segments")
    P("#   over six lengths.  Reproduced, not re-chosen, so 1187 and this run read the same")
    P("#   object.")
    P(f"# NOT dials: PANEL {PANELS}; the four DIAL LADDERS (27 rung books/panel, 81 total);")
    P("#   the WITHIN statistic (count-matched all-pairs mean |difference|, 1158's); the")
    P("#   census; the rule-8 choosers.")
    P(f"# SERVES := SATISFIABLE (>= 2 distinct sub-tape LENGTHS) AND LANDS (within")
    P(f"#   {LAND_BAR:.0%} of P_FULL) at a majority of the 81 books AND ORDERS (Spearman rho")
    P(f"#   vs P_FULL across a cell's 27 books >= {RHO_BAR:.2f}) at a majority of the 18")
    P("#   (panel, statistic) cells.  Scored (A) BLOCK, (B) QUARTERS, (C) BOTH, (D) NEITHER.")
    P(f"# TAPE PINNED at {PIN}.  This is a reporting-schema result and can never be a KEEP.")
    P("")

    # ---------------------------------------------------------------- panels
    P("## PANELS, PINNED AND UNPINNED")
    cells, cells_un = {}, {}
    for panel in PANELS:
        if panel == "SMALL":
            px0, nmeta, ndrop = load_small()
        else:
            px0 = load_universe(broad=(panel == "B136"))
            nmeta = ndrop = 0
        px0 = px0.dropna(how="all").ffill()
        for store, px in ((cells_un, px0), (cells, px0.loc[:PIN])):
            idx = px.index
            T, K = len(idx), len(px.columns)
            rets = px.pct_change().fillna(0.0).values
            priced = px.notna().values
            sc, elig = mech_scores(px)
            rank_key = -np.nan_to_num(sc, nan=-np.inf)
            rank_key[np.isnan(sc)] = np.inf
            warm = np.zeros(T, dtype=bool)
            warm[WARMUP:] = True
            oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
            ins = warm & ~oos
            store[panel] = dict(px=px, idx=idx, T=T, K=K, rets=rets, priced=priced,
                                rank_key=rank_key, elig=elig, warm=warm, ins=ins, oos=oos)
        d = cells[panel]
        P(f"  {panel:<6s} PINNED {d['T']:5d} bars x {d['K']:4d} cols  {d['idx'][0].date()} .. "
          f"{d['idx'][-1].date()}   (unpinned {cells_un[panel]['T']} bars)")
        if panel == "SMALL":
            P(f"  SMALL STAMP (SURVIVORSHIP): data/small_meta.csv lists {nmeta} tickers; "
              f"{ndrop} dropped for max_1d_move >= 1.0; pool served = {d['K']-1} names + SPY.")
            P("  Current constituents of the screen only — SMALL levels are OPTIMISTIC and")
            P("  every 4a / 4b count on that panel is an UPPER bound.")
    P("")

    # ---------------------------------------------------------------- rung books
    P("## RUNG BOOKS — 27 per panel, 81 in total, 1148's grid")
    RB: dict = {}

    def book(store, panel, N, H, gross, cadence):
        key = (id(store), panel, N, H, round(gross, 6), cadence)
        if key in RB:
            return RB[key]
        d = store[panel]
        mk = rebalance_mask(d["idx"], cadence).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        W = build(d["rank_key"], d["elig"], d["priced"], np.flatnonzero(mk), N, H,
                  d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        RB[key] = nrun(d["rets"], Wl, mkl)
        return RB[key]

    def rung_book(store, panel, lad, rg):
        c = dict(ANCHOR)
        c[lad] = rg
        return book(store, panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])[
            store[panel]["warm"]]

    CAND = [(lad, rg) for lad, rungs in LADDERS.items() for rg in rungs]
    for panel in PANELS:
        for lad, rg in CAND:
            rung_book(cells, panel, lad, rg)
    P(f"  built {len(CAND)} rung books x {len(PANELS)} panels = {len(CAND)*len(PANELS)}  "
      f"({time.time()-t0:.0f}s).  The anchor book (N=20/H=126/gross 0.75/W) is a rung of all")
    P("  four ladders, so the 81 are 78 DISTINCT books; every duplicate is published and")
    P("  none is counted twice in any claim about distinct books.")
    P("")

    # ---------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = cells["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(d["rank_key"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values[d["warm"]]
    v = float(np.abs(eng - rung_book(cells, "U56", "N", N0)).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20, gross 0.75)", v, v < 1e-12)

    def triple_dev(store):
        dd_ = store["U56"]
        w = dd_["warm"]
        m = blocks_m(rung_book(store, "U56", "N", N0), dd_["ins"][w], dd_["oos"][w])
        a = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
                abs(m["MaxDD"] - A936_WH126[2]))
        sp = dd_["px"]["SPY"].pct_change().fillna(0.0).values[w]
        sm = blocks_m(sp, dd_["ins"][w], dd_["oos"][w])
        b = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
        return a, b

    a_pin, b_pin = triple_dev(cells)
    a_un, b_un = triple_dev(cells_un)
    gate("G2", f"CROSS-RUN the committed U56 W/H126/N=20 triple, PINNED at {PIN}", a_pin,
         a_pin < 5e-5)
    gate("G3", f"CROSS-RUN the committed SPY OOS triple on U56's tape, PINNED at {PIN}", b_pin,
         b_pin < 5e-4)
    P(f"     THE VINTAGE, PUBLISHED NOT ABSORBED: the same two gates on the UNPINNED file "
      f"read {a_un:.3e} and {b_un:.3e}.")

    lv = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq=FREQ0)["returns"].values
    v = abs(fmet(lv[d["warm"]])[2] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == the committed -12.05%", v, v < 5e-4)

    v = max(abs(six_stats(rung_book(cells, p, "N", N0))["MAXDD"] - DD_COMMITTED[p])
            for p in PANELS)
    gate("G5", "CROSS-RUN 1157/1158's committed full-tape MaxDD LEVELS (U56/B136/SMALL)", v,
         v < 5e-4)

    # G6 — THE PREMISE, PROVED AS ARITHMETIC AND NOT ASSERTED: how many LENGTHS does each
    # repair yield, on every one of the 81 books?
    nlen_seen = {rep_: set() for rep_ in REPAIRS}
    nlen_seen["P_FULL"] = set()
    for panel in PANELS:
        for lad, rg in CAND:
            r = rung_book(cells, panel, lad, rg)
            for rep_ in REPAIRS:
                nlen_seen[rep_].add(len(segments(r, rep_)))
            nlen_seen["P_FULL"].add(len(segments_full(r)))
    bad = sorted(nlen_seen["P_HALF"] | nlen_seen["P_OVERLAP"])
    gate("G6", "1148's PREMISE AS ARITHMETIC: P_HALF and P_OVERLAP yield exactly ONE sub-tape "
         "length on every one of the 81 books, so their BETWEEN term is undefined",
         float(max(bad) - 1), bad == [1])
    P("     distinct-length counts by repair: " +
      ", ".join(f"{k} {sorted(v)}" for k, v in nlen_seen.items()))
    P("")

    # ---------------------------------------------------------------- the 24-cell grid
    P("## (A) THE 24-CELL GRID (dial 1 REPAIR x dial 2 STATISTIC) — at all 81 books")
    rows = []
    for panel in PANELS:
        for lad, rg in CAND:
            r = rung_book(cells, panel, lad, rg)
            segmaps = {rep_: segments(r, rep_) for rep_ in REPAIRS}
            segmaps["P_FULL"] = segments_full(r)
            for stat in STATS6:
                w0, b0, ref, nl0, ns0 = ratio_of(segmaps["P_FULL"], stat)
                for rep_ in REPAIRS:
                    w, b, rr, nl, ns = ratio_of(segmaps[rep_], stat)
                    gap = (abs(rr - ref) / abs(ref)
                           if np.isfinite(rr) and np.isfinite(ref) and ref != 0 else np.nan)
                    rows.append(dict(panel=panel, ladder=lad, rung=str(rg), stat=stat,
                                     repair=rep_, n_lengths=nl, n_segments=ns,
                                     seg_cost=SEG_COST[rep_], within=w, between=b, ratio=rr,
                                     ref_within=w0, ref_between=b0, ref_ratio=ref,
                                     ref_n_lengths=nl0, ref_n_segments=ns0,
                                     satisfiable=bool(nl >= 2), rel_gap=gap,
                                     lands=bool(np.isfinite(gap) and gap <= LAND_BAR)))
    G = pd.DataFrame(rows)
    dump(G, "grid")
    P(f"  {len(G):,} rows = 3 panels x 27 rung books x 6 statistics x 4 repairs.")

    # G7 — the reference reproduces 1158/1187's committed resolved target at its own cell.
    # 1158 pooled ALL FOUR LADDERS' books before taking medians; this run reads ONE book at a
    # time, so the cell is a SUPERSET check: the committed value must lie inside the range the
    # 81-book reading spans on SMALL / MAXDD.  Published as an interval, not asserted as equal.
    s = G[(G.panel == "SMALL") & (G.stat == HEAD_STAT) & (G.repair == "P_HALF")]
    lo, hi = float(np.nanmin(s.ref_ratio)), float(np.nanmax(s.ref_ratio))
    inside = lo <= RESOLVED_1158_SMALL_MAXDD <= hi
    gate("G7", f"1158/1187's committed SMALL/MAXDD resolved target "
         f"{RESOLVED_1158_SMALL_MAXDD:.6f} lies inside this run's per-book P_FULL range "
         f"[{lo:.4f}, {hi:.4f}]", 0.0 if inside else 1.0, inside)

    idx = G.set_index(["panel", "ladder", "rung", "stat", "repair"])
    dev = 0.0
    for panel in PANELS:
        for lad, rg in CAND:
            r = rung_book(cells, panel, lad, rg)
            for stat in (HEAD_STAT, "SHARPE"):
                for rep_ in REPAIRS:
                    again = ratio_of(segments(r, rep_), stat)[2]
                    was = float(idx.loc[(panel, lad, str(rg), stat, rep_), "ratio"])
                    if np.isfinite(again) or np.isfinite(was):
                        dev = max(dev, abs(np.nan_to_num(again) - np.nan_to_num(was)))
    gate("G8", "the segmentation and every ratio are deterministic on re-computation "
         "(648 re-reads)", dev, dev < 1e-15)
    P("")

    # ---------------------------------------------------------------- landing + ordering
    P("## (B) DOES A CHEAP REPAIR LAND ON THE FULL RE-RUN'S LEVEL?")
    P(f"  {'repair':<12s}{'cost':>6s}{'SATISF':>8s}{'n':>6s}{'LANDS':>7s}{'rate':>8s}"
      f"{'med gap':>10s}{'med ratio':>11s}{'ref':>10s}")
    lrows = []
    for rep_ in REPAIRS:
        s = G[G.repair == rep_]
        fin = s[np.isfinite(s.ratio)]
        lrows.append(dict(repair=rep_, seg_cost=SEG_COST[rep_], n_books=len(s),
                          n_satisfiable=int(s.satisfiable.sum()),
                          n_finite=len(fin), n_lands=int(s.lands.sum()),
                          rate_lands=float(s.lands.mean()),
                          med_rel_gap=float(np.nanmedian(s.rel_gap)),
                          med_ratio=float(np.nanmedian(s.ratio)),
                          med_ref=float(np.nanmedian(s.ref_ratio))))
        z = lrows[-1]
        g4 = f"{z['med_rel_gap']:.4f}" if np.isfinite(z["med_rel_gap"]) else "undef"
        r4 = f"{z['med_ratio']:.4f}" if np.isfinite(z["med_ratio"]) else "undef"
        P(f"  {rep_:<12s}{z['seg_cost']:>6d}{z['n_satisfiable']:>8d}{z['n_books']:>6d}"
          f"{z['n_lands']:>7d}{z['rate_lands']:>8.3f}{g4:>10s}{r4:>11s}"
          f"{z['med_ref']:>10.4f}")
    dump(pd.DataFrame(lrows), "landing")
    P("  Per statistic (dial 2), landing rate over the 81 books:")
    P(f"  {'stat':<9s}" + "".join(f"{r:>12s}" for r in REPAIRS))
    srows = []
    for stat in STATS6:
        line = f"  {stat:<9s}"
        for rep_ in REPAIRS:
            s = G[(G.stat == stat) & (G.repair == rep_)]
            srows.append(dict(stat=stat, repair=rep_, n=len(s),
                              n_satisfiable=int(s.satisfiable.sum()),
                              n_lands=int(s.lands.sum()), rate=float(s.lands.mean()),
                              med_rel_gap=float(np.nanmedian(s.rel_gap))))
            line += f"{s.lands.mean():>12.3f}"
        P(line)
    dump(pd.DataFrame(srows), "by_statistic")
    P("")

    P("## (C) DOES A CHEAP REPAIR *ORDER* THE BOOKS THE WAY THE FULL RE-RUN DOES?")
    P("  Spearman rho across a (panel, statistic) cell's 27 rung books, repair vs P_FULL.")
    P("  This is the leg that matters operationally: a cheap repair earns its place only if")
    P("  it RANKS books the way the expensive one does, whatever it does to the level.")
    rrows = []
    P(f"  {'panel':<7s}{'stat':<9s}" + "".join(f"{r:>12s}" for r in REPAIRS))
    for panel in PANELS:
        for stat in STATS6:
            line = f"  {panel:<7s}{stat:<9s}"
            for rep_ in REPAIRS:
                s = G[(G.panel == panel) & (G.stat == stat) & (G.repair == rep_)]
                rho = spearman(s.ratio.values, s.ref_ratio.values)
                rrows.append(dict(panel=panel, stat=stat, repair=rep_, rho=rho,
                                  orders=bool(np.isfinite(rho) and rho >= RHO_BAR)))
                cell = f"{rho:.3f}" if np.isfinite(rho) else "undef"
                line += f"{cell:>12s}"
            P(line)
    R = pd.DataFrame(rrows)
    dump(R, "ordering")
    P(f"  {'repair':<12s}{'ORDERS':>8s}{'of':>5s}{'rate':>8s}{'median rho':>12s}")
    for rep_ in REPAIRS:
        s = R[R.repair == rep_]
        mr = np.nanmedian(s.rho) if np.isfinite(s.rho).any() else np.nan
        mrs = f"{mr:.4f}" if np.isfinite(mr) else "undef"
        P(f"  {rep_:<12s}{int(s.orders.sum()):>8d}{len(s):>5d}{s.orders.mean():>8.3f}"
          f"{mrs:>12s}")
    P("")

    # ---------------------------------------------------------------- serves
    P("## (D) DOES ANY CHEAP REPAIR *SERVE*?  All three legs, majority on each")
    P(f"  {'repair':<12s}{'cost':>6s}{'SATISF':>9s}{'LANDS maj':>11s}{'ORDERS maj':>12s}"
      f"{'SERVES':>9s}")
    vrows = []
    for rep_ in REPAIRS:
        s = G[G.repair == rep_]
        rr = R[R.repair == rep_]
        sat = bool(s.satisfiable.all())
        lm = bool(s.lands.sum() > len(s) / 2)
        om = bool(rr.orders.sum() > len(rr) / 2)
        serves = sat and lm and om
        vrows.append(dict(repair=rep_, seg_cost=SEG_COST[rep_], satisfiable=sat,
                          lands_majority=lm, orders_majority=om, serves=serves))
        P(f"  {rep_:<12s}{SEG_COST[rep_]:>6d}{('YES' if sat else 'NO'):>9s}"
          f"{('YES' if lm else 'no'):>11s}{('YES' if om else 'no'):>12s}"
          f"{('**YES**' if serves else 'NO'):>9s}")
    V = pd.DataFrame(vrows)
    dump(V, "serves")
    P("")

    # ---------------------------------------------------------------- census
    P("## (E) THE RECORD'S OWN SPLIT-HALF ROWS — 1148's premise, re-counted here")
    CEN = census()
    dump(CEN, "census")
    tot = float(np.nansum(CEN.n_rows))
    can = CEN[CEN.can_price_length]
    P(f"  {len(CEN):,} committed CSVs carry a SPLIT-HALF column pair, {tot:,.0f} rows in all.")
    P(f"  Of those files, {len(can)} ({len(can)/max(len(CEN),1):.4f}) carry any column with "
      f">= 2 distinct sub-tape LENGTHS, i.e. could price the length axis in place;")
    P(f"  {int((~CEN.can_price_length).sum())} cannot, covering "
      f"{float(np.nansum(CEN.loc[~CEN.can_price_length,'n_rows'])):,.0f} rows.")
    P("  (1148 committed '0 of 2,140,569'.  This run's file set and its column test are its")
    P("   own — the figure is published beside 1148's, not substituted for it.)")
    P("")

    # ---------------------------------------------------------------- rule 8 + KEEP paths
    P("## (F) RULE 8 WALK-FORWARD AND BOTH KEEP PATHS — 81 rung books, every one published")
    P("  Parameters chosen on 2009-2016 ONLY; 2017-2026 read once.  4a judged against the")
    P("  live RULES v2 book, 4b against SPY, full tape and again out of sample.")
    bookrows, benchrows, pickrows = [], [], []
    bench = {}
    for panel in PANELS:
        dd_ = cells[panel]
        w = dd_["warm"]
        spy = dd_["px"]["SPY"].pct_change().fillna(0.0).values[w]
        sb = blocks_m(spy, dd_["ins"][w], dd_["oos"][w])
        lvr = backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                       freq=FREQ0)["returns"].values[w]
        lb = blocks_m(lvr, dd_["ins"][w], dd_["oos"][w])
        bench[panel] = (sb, lb)
        for nm, bb in (("SPY", sb), ("RULES v2 (live)", lb)):
            benchrows.append(dict(panel=panel, name=nm, **bb))
        P(f"  {panel:<6s} SPY  {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f}/{sb['H2']:.4f}), OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {'':<6s} LIVE {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%} "
          f"(halves {lb['H1']:.4f}/{lb['H2']:.4f}), OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        for lad, rg in CAND:
            b = blocks_m(rung_book(cells, panel, lad, rg), dd_["ins"][w], dd_["oos"][w])
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            bookrows.append(dict(panel=panel, ladder=lad, rung=str(rg), **b, **l4b, **l4bo,
                                 **l4a, pass_4b_full=all(l4b.values()),
                                 pass_4b_oos=all(l4bo.values()), pass_4a=all(l4a.values())))
    BK = pd.DataFrame(bookrows)
    dump(BK, "books")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P(f"  4b FULL {int(BK.pass_4b_full.sum())} of {len(BK)} rung books | 4b OOS "
      f"{int(BK.pass_4b_oos.sum())} | BOTH {int((BK.pass_4b_full & BK.pass_4b_oos).sum())} | "
      f"4a {int(BK.pass_4a.sum())} of {len(BK)}")
    for panel in PANELS:
        s = BK[BK.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.pass_4b_full.sum()):2d}/{len(s)}  4b OOS "
          f"{int(s.pass_4b_oos.sum()):2d}/{len(s)}  4a {int(s.pass_4a.sum()):2d}/{len(s)}")
    P("")

    P("  THE CHOOSERS (all choose on 2009-2016 ONLY and read 2017-2026 ONCE):")
    P("    CH_ISSHARPE — argmax IS Sharpe over the 27 rung books.  The honest incumbent.")
    P("    CH_<repair>  — among the top-9 IS-Sharpe books, the one whose IN-SAMPLE")
    P(f"      regime-to-length ratio on {HEAD_STAT} is LOWEST under that repair.  CH_P_FULL is")
    P("      the expensive reference chooser.  A cheap repair that changes the pick is a")
    P("      cheap repair that changes capital.")
    for panel in PANELS:
        dd_ = cells[panel]
        w = dd_["warm"]
        ins_w = dd_["ins"][w]
        isS = {k: fsharpe(rung_book(cells, panel, k[0], k[1])[ins_w]) for k in CAND}
        top = sorted(CAND, key=lambda k: -isS[k])[:9]
        sb, lb = bench[panel]
        for ch in ["CH_ISSHARPE"] + [f"CH_{r}" for r in REPAIRS] + ["CH_P_FULL"]:
            if ch == "CH_ISSHARPE":
                pick, br = max(CAND, key=lambda k: isS[k]), np.nan
            else:
                rep_ = ch[3:]
                br_all = {}
                for lad, rg in top:
                    r_is = rung_book(cells, panel, lad, rg)[ins_w]
                    sm = segments_full(r_is) if rep_ == "P_FULL" else segments(r_is, rep_)
                    br_all[(lad, rg)] = ratio_of(sm, HEAD_STAT)[2]
                fin = {k: v for k, v in br_all.items() if np.isfinite(v)}
                pick = (min(fin, key=lambda k: fin[k]) if fin
                        else max(top, key=lambda k: isS[k]))
                br = br_all.get(pick, np.nan)
            b = blocks_m(rung_book(cells, panel, pick[0], pick[1]), dd_["ins"][w], dd_["oos"][w])
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            pickrows.append(dict(
                panel=panel, chooser=ch, ladder=pick[0], rung=str(pick[1]), book_ratio=br,
                IS_Sharpe=b["IS_Sharpe"], OOS_Sharpe=b["OOS_Sharpe"], OOS_CAGR=b["OOS_CAGR"],
                OOS_MaxDD=b["OOS_MaxDD"], CAGR=b["CAGR"], Sharpe=b["Sharpe"],
                MaxDD=b["MaxDD"], H1=b["H1"], H2=b["H2"],
                SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                beats_SPY_OOS=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                pass_4a=all(l4a.values())))
    PK = pd.DataFrame(pickrows)
    dump(PK, "picks")
    P(f"  {'panel':<7s}{'chooser':<14s}{'pick':<14s}{'IS_S':>8s}{'OOS_S':>8s}{'SPY_S':>8s}"
      f"{'OOS_CAGR':>10s}{'OOS_DD':>9s}{'>SPY':>6s}{'4b':>4s}{'4bO':>5s}{'4a':>4s}")
    for r in PK.itertuples():
        P(f"  {r.panel:<7s}{r.chooser:<14s}{(r.ladder+'='+r.rung):<14s}{r.IS_Sharpe:>8.4f}"
          f"{r.OOS_Sharpe:>8.4f}{r.SPY_OOS_Sharpe:>8.4f}{r.OOS_CAGR:>10.2%}{r.OOS_MaxDD:>9.2%}"
          f"{'Y' if r.beats_SPY_OOS else '.':>6s}{'Y' if r.pass_4b_full else '.':>4s}"
          f"{'Y' if r.pass_4b_oos else '.':>5s}{'Y' if r.pass_4a else '.':>4s}")
    agree = 0
    for panel in PANELS:
        ref = PK[(PK.panel == panel) & (PK.chooser == "CH_P_FULL")][["ladder", "rung"]].iloc[0]
        for rep_ in REPAIRS:
            s = PK[(PK.panel == panel) & (PK.chooser == f"CH_{rep_}")][["ladder", "rung"]].iloc[0]
            agree += int(s.ladder == ref.ladder and s.rung == ref.rung)
    P(f"  A CHEAP REPAIR'S CHOOSER AGREES WITH THE EXPENSIVE ONE at {agree} of "
      f"{len(PANELS)*len(REPAIRS)} (panel, repair) cells.")
    P(f"  4b FULL {int(PK.pass_4b_full.sum())} of {len(PK)} picks | 4b OOS "
      f"{int(PK.pass_4b_oos.sum())} | 4a {int(PK.pass_4a.sum())}.")
    P("")

    # ---------------------------------------------------------------- verdict
    P("## VERDICT AGAINST THE PRE-DECLARED OUTCOMES, SCORED IN THE DECLARED ORDER")
    sv = {r: bool(V[V.repair == r].serves.iloc[0]) for r in REPAIRS}
    for r in REPAIRS:
        P(f"  {r:<12s} serves: {'YES' if sv[r] else 'NO'}")
    if sv["P_OVERLAP"]:
        outcome = "(E) OVERLAP SCORES — the pre-declaration that a single length cannot " \
                  "price the length axis is FALSIFIED"
    elif sv["P_BLOCK"] and sv["P_QUARTERS"]:
        outcome = "(C) BOTH serve; the record may pick on segment cost alone (BLOCK 8, " \
                  "QUARTERS 6, so QUARTERS is cheaper)"
    elif sv["P_BLOCK"]:
        outcome = "(A) BLOCK — the within-half block spread serves at cost 8"
    elif sv["P_QUARTERS"]:
        outcome = "(B) QUARTERS — quarters serve at cost 6 and the block spread does not"
    else:
        outcome = ("(D) NEITHER — no cheap repair reproduces the full re-run, so a "
                   "SPLIT-HALF claim CANNOT be made regime-checkable without the third "
                   "tape; the record's committed split-half rows are not repairable in "
                   "place and must be re-run or withdrawn")
    P(f"  OUTCOME: {outcome}")
    P("")

    ok = all(g["pass_"] for g in GATES)
    dump(pd.DataFrame(GATES), "gates")
    P(f"## GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    P(f"## DONE in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
