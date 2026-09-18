#!/usr/bin/env python3
"""IDEA 1273 (lane cloud, 2026-09-18) — is a DECISIVENESS BAR worth anything once ITS OWN DIAL is
priced at EVERY INNER SPLIT?

THE QUESTION.  1260 priced an observed-side decisiveness bar head-to-head with the incumbent
P_boot bar on 72 real book choices, found the observed side better as a class (mean licensed-
minus-refused +0.0401 vs -0.0142), and then KILLED it on one number: the bar's own dial does not
transfer, inner/outer licensed-minus-refused rank corr -0.4292, measured at ONE inner split
(pick on warm-up..2012, score 2013-2016).  A single rank correlation on a single draw of the split
is not evidence that the dial anti-selects; it is one observation of a statistic with its own
sampling distribution.  This run walks the inner boundary across {2011, 2012, 2013, 2014} and the
SCORE CLASS across {OBS, BAR, ALL} and reports, at all 12 grid points, the rule-8 chosen cell, its
OUTER licensed-minus-refused, its capital value d_sel, and the inner/outer rank correlation — so
the record learns whether "the dial does not transfer" is a fact about the tape or one unlucky
split.

TWO DIALS (rule 4), 12 cells, EVERY ONE PUBLISHED:
  dial 1 = INNER BOUNDARY  {2011-12-31, 2012-12-31, 2013-12-31, 2014-12-31}
           the date splitting the IS window into an inner TRAIN (warm-up..boundary, where the pick
           is made) and an inner VALIDATION (boundary+1..2016-12-31, where the bar's dial is
           scored).  1260 used 2012-12-31 and only that.
  dial 2 = SCORE CLASS     {OBS (12 cells), BAR (12 cells), ALL (24 cells)}
           the candidate set the rule-8 argmax may choose from.  1260 chose from ALL.

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL663}, ANCHOR {A, B}, LADDER {N, H, GROSS, CADENCE},
CHOOSER {CH_ISSHARPE, CH_ISCAGR, CH_ISDD} = the same 72 decisions everywhere; the 4 scores and the
6 bar quantiles are 1260's, inherited whole and never re-tuned; block length frozen at L = 63.

EXECUTION (binding, rule 2): weights decided at the rebalance close t, applied at t+1; 10 bps per
unit turnover; no shorting, no leverage.  RULE 8: every book pick is made on warm-up..2016-12-31
ONLY, every dial choice is made on the inner split ONLY, and 2017-2026 is read ONCE per cell.

Offline, deterministic, standalone.  Writes .grid.csv .decisions.csv .books.csv .cells.csv
.walkforward.csv .gates.csv .console.txt
"""
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "is-a-DECISIVENESS-BAR-WORTH-ANYTHING-ONCE-ITS-OWN-DIAL-IS-PRICED-AT-EVERY-INNER-SPLIT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ----- 1101/1252/1260's construction, inherited whole -------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]
ANCHORS = {"A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
           "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M")}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]

SCORES = ["S_OBS_RATIO", "S_OBS_MARGIN", "S_PBOOT_TOP", "S_PBOOT_MARGIN"]
OBS_SIDE = {"S_OBS_RATIO", "S_OBS_MARGIN"}
QUANTS = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
L_FROZEN = 63
BDRAWS = 1000
SEED_BASE = 12601260            # 1260's own seed base, so the frozen-cell gates can bind

# ----- THIS RUN'S DIALS -------------------------------------------------------------------------
BOUNDARIES = ["2011-12-31", "2012-12-31", "2013-12-31", "2014-12-31"]
CLASSES = {"OBS": ["S_OBS_RATIO", "S_OBS_MARGIN"],
           "BAR": ["S_PBOOT_TOP", "S_PBOOT_MARGIN"],
           "ALL": SCORES}

# ----- committed numbers QUOTED and GATED, never re-derived -------------------------------------
C1260_RHO_INNER_OUTER = -0.4292          # 24 cells, inner boundary 2012-12-31, class ALL
C1260_INNER_ARGMAX = ("S_OBS_MARGIN", 0.90)
C1260_OUTER_LICREF_AT_ARGMAX = 0.0297
C1260_DSEL_AT_ARGMAX = 0.0040
C1260_4B_AT_ARGMAX, C1260_4B_DONOTHING = 23, 24
C1260_DALL = 0.0095                      # mean d over the 72
C1246_ANCHOR_OOS, C1246_ACT_OOS = 0.7922, 0.8016
C1101_TRIPLE = (0.155787, 1.139701, -0.191276)
LIVE_MAXDD_COMMITTED = -0.1205
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
C1260_BEST_OBS = 0.1839                  # S_OBS_MARGIN @ q0.95 licensed-minus-refused

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<6s} {what}  ->  {value:.4e}")
    return bool(ok)


# ================================================================================================
# 1101/1252/1260's runner and metrics, verbatim
# ================================================================================================
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
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
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


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def inner_of(idx, ins, boundary):
    tr = ins & np.asarray(idx <= pd.Timestamp(boundary))
    va = ins & ~tr
    return tr, va


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


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
        self.inner = {b: inner_of(px.index, self.ins, b) for b in BOUNDARIES}
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if name == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG)
            m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def book(pan, N, H, gross, freq):
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    return r - turn * COST / 1e4


def ladder_books(pan, anchor, lad):
    a = ANCHORS[anchor]
    out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        out[rung] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"])
    return out


# ----- 1101's joint moving-block bootstrap, verbatim --------------------------------------------
def block_index(rng, T, L, B):
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def pboot_argmax(R, stat, L, seed, B=BDRAWS, chunk=100):
    T, k = R.shape
    rng = np.random.default_rng(seed)
    cnt = np.zeros(k)
    done = 0
    while done < B:
        b = min(chunk, B - done)
        idx = block_index(rng, T, L, b)
        X = R[idx]
        if stat == "CH_ISSHARPE":
            v = X.mean(axis=1) * 252.0 / (X.std(axis=1, ddof=1) * np.sqrt(252.0))
        elif stat == "CH_ISCAGR":
            eq = np.cumprod(1.0 + X, axis=1)
            v = eq[:, -1, :] ** (252.0 / T) - 1.0
        elif stat == "CH_ISDD":
            eq = np.cumprod(1.0 + X, axis=1)
            v = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
        else:
            raise ValueError(stat)
        v = np.where(np.isfinite(v), v, -np.inf)
        cnt += np.bincount(v.argmax(axis=1), minlength=k)
        done += b
    return cnt / B


def is_stat(r, win, stat):
    x = r[win]
    n = len(x)
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    if stat == "CH_ISCAGR":
        eq = np.cumprod(1.0 + x)
        return eq[-1] ** (252.0 / n) - 1.0
    if stat == "CH_ISDD":
        eq = np.cumprod(1.0 + x)
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


def spear(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return 0.0
    return float(np.corrcoef(ra, rb)[0, 1])


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 2 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def welch_t(a, b):
    a = np.asarray([v for v in a if np.isfinite(v)], float)
    b = np.asarray([v for v in b if np.isfinite(v)], float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    if va + vb == 0:
        return np.nan
    return float((a.mean() - b.mean()) / np.sqrt(va + vb))


# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1273 (lane cloud, {DATE}) — is a DECISIVENESS BAR worth anything once ITS OWN DIAL")
    P("                                 is priced at EVERY INNER SPLIT?")
    P("=" * 100)
    P("  dial 1 = INNER BOUNDARY {2011-12-31, 2012-12-31, 2013-12-31, 2014-12-31}")
    P("  dial 2 = SCORE CLASS    {OBS, BAR, ALL}            -> 12 cells, ALL PUBLISHED")
    P("  NOT dials: panel (3), anchor (2), ladder (4), chooser (3) = the same 72 decisions;")
    P("             1260's 4 scores and 6 bar quantiles inherited whole; L frozen at 63.")
    P("  10 bps, t+1, warm-up 260.  Book picks on warm-up..2016-12-31; dial picks on the inner")
    P("  split ONLY; 2017-2026 read ONCE.")
    P("")

    P("-" * 100)
    P("ARM 0 — WHAT IS DECLARED BEFORE THE TAPE IS TOUCHED")
    P("-" * 100)
    P(f"  1260 read inner/outer licensed-minus-refused rank corr {C1260_RHO_INNER_OUTER:+.4f} over its 24 cells")
    P("  at ONE inner boundary (2012-12-31) and concluded 'choosing the bar in sample ANTI-selects'.")
    P("  That is one draw of a statistic, not a property.  Pre-declared outcomes:")
    P("    (A) ANTI-SELECTION IS A FACT — rank corr < 0 at a MAJORITY of the 4 boundaries and the")
    P("        rule-8 chosen cell's outer d_sel is <= 0 on average over the 12 grid points.")
    P("    (B) ONE UNLUCKY SPLIT — rank corr > 0 at a majority and the chosen cell's outer d_sel")
    P("        is positive on average, i.e. 1260's -0.4292 was a draw and the dial does transfer.")
    P("    (C) THE DIAL IS UNRESOLVED — signs mixed and the chosen cell scatters across boundaries,")
    P("        i.e. neither 'transfers' nor 'anti-selects' is supportable at this sample size.")
    P("  H_CORR    : majority of the 12 (boundary, class) rank corrs are > 0.")
    P("  H_TRANSFER: mean outer d_sel of the 12 rule-8 chosen cells > 0.")
    P("  H_STABLE  : within a class, the SAME (score, quantile) is chosen at >= 3 of 4 boundaries.")
    P("  H_1260    : at (2012-12-31, ALL) this run reproduces 1260's chosen cell and its outer")
    P("              LIC-REF / d_sel / 4b count.")
    P("  H_CAPITAL : some rule-8 chosen selector beats do-nothing on mean OOS Sharpe WITHOUT")
    P("              costing a 4b pass.")
    P("")

    # ---------------------------------------------------------------------------- panels
    P("-" * 100)
    P("ARM 1 — PANELS, BENCHMARKS AND THE 162 RUNG BOOKS")
    P("-" * 100)
    u = load_universe()
    b = load_universe(broad=True)
    s, n_bad, n_meta = load_small()
    PAN = {}
    for nm, px in (("U56", u), ("B136", b), ("SMALL", s)):
        PAN[nm] = Panel(nm, px)
        pan = PAN[nm]
        inner_txt = "  ".join(f"{bd[:4]}:{int(pan.inner[bd][0].sum())}/{int(pan.inner[bd][1].sum())}"
                              for bd in BOUNDARIES)
        P(f"  {nm:<6s} {px.shape[1]:>4d} cols x {px.shape[0]:>5d} rows  "
          f"{px.index[0].date()} .. {px.index[-1].date()}  IS {pan.ins.sum():>5d}  OOS {pan.oos.sum():>5d}")
        P(f"         inner train/val by boundary: {inner_txt}")
    P(f"  SMALL exclusion: {n_bad} of {n_meta} names dropped on max_1d_move >= 1.0 (documented).")

    BM = {}
    for nm, pan in PAN.items():
        spy = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lw = rules_v2_weights(pan.px)
        lr = backtest(pan.px, lw, cost_bps=COST, freq="W")["returns"].values
        live = blocks_m(lr, pan.warm, pan.ins, pan.oos)
        BM[nm] = dict(spy=spy, live=live)
        P(f"  {nm:<6s} SPY     full {spy['CAGR']:>7.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:>7.2%}"
          f"  halves {spy['H1']:.4f}/{spy['H2']:.4f}  OOS {spy['OOS_CAGR']:>7.2%} / {spy['OOS_Sharpe']:.4f} / {spy['OOS_MaxDD']:>7.2%}")
        P(f"  {nm:<6s} LIVE v2 full {live['CAGR']:>7.2%} / {live['Sharpe']:.4f} / {live['MaxDD']:>7.2%}"
          f"  halves {live['H1']:.4f}/{live['H2']:.4f}  OOS {live['OOS_CAGR']:>7.2%} / {live['OOS_Sharpe']:.4f}")

    RB, brows = {}, []
    for pnm in PANELS:
        pan = PAN[pnm]
        for anc in ANCHORS:
            for lad in LADNAMES:
                bks = ladder_books(pan, anc, lad)
                RB[(pnm, anc, lad)] = bks
                a = ANCHORS[anc]
                for rung, r in bks.items():
                    m = blocks_m(r, pan.warm, pan.ins, pan.oos)
                    kw = dict(N=a["N"], H=a["H"], GROSS=a["GROSS"], CADENCE=a["CADENCE"])
                    kw[lad] = rung
                    row = dict(panel=pnm, anchor=anc, ladder=lad, rung=rung, **kw, **m)
                    row.update(legs_4b(m, BM[pnm]["spy"]))
                    row.update(legs_4b_oos(m, BM[pnm]["spy"]))
                    row.update(legs_4a(m, BM[pnm]["live"]))
                    row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                    row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                    brows.append(row)
    books = pd.DataFrame(brows)
    P(f"  built {len(books)} rung books;  4a {int(books.pass_4a.sum())} of {len(books)};"
      f"  4b full {int(books.pass_4b_full.sum())};  4b OOS {int(books.pass_4b_oos.sum())};"
      f"  BOTH {int((books.pass_4b_full & books.pass_4b_oos).sum())}")
    dump(books, "books")

    inc = books[(books.panel == "U56") & (books.anchor == "A") & (books.ladder == "N") & (books.rung == 20)].iloc[0]
    e1 = max(abs(inc.CAGR - C1101_TRIPLE[0]), abs(inc.Sharpe - C1101_TRIPLE[1]), abs(inc.MaxDD - C1101_TRIPLE[2]))
    P(f"  incumbent U56/A/N=20 replays {inc.CAGR:.4%} / {inc.Sharpe:.4f} / {inc.MaxDD:.4%}")
    gate("G1", "incumbent triple vs 1101's committed (tape restated daily)", e1, e1 < 5e-3)
    e2 = abs(BM["U56"]["live"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G2", "U56 live RULES v2 MaxDD vs committed -12.05%", e2, e2 < 5e-3)
    e3 = max(abs(BM["U56"]["spy"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(BM["U56"]["spy"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(BM["U56"]["spy"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "U56 SPY OOS triple vs committed", e3, e3 < 5e-3)
    ov = sum(int((PAN[p].ins & PAN[p].oos).sum()) for p in PANELS)
    gate("G4", "IS n OOS rows (must be 0)", ov, ov == 0)
    ivmax = 0
    for p in PANELS:
        for bd in BOUNDARIES:
            tr, va = PAN[p].inner[bd]
            ivmax = max(ivmax, int((tr & va).sum()) + abs(int((tr | va).sum()) - int(PAN[p].ins.sum())))
    gate("G4b", "every inner boundary partitions IS exactly", ivmax, ivmax == 0)
    pan = PAN["U56"]
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb["W"], 20, 126, pan.T, pan.K, 0.75)
    eng = backtest(pan.px, pd.DataFrame(W, index=pan.idx, columns=pan.px.columns), cost_bps=COST, freq="W")["returns"].values
    e5 = float(np.abs(eng[WARMUP:] - RB[("U56", "A", "N")][20][WARMUP:]).max())
    gate("G5", "fast runner == engine.backtest (U56 A N=20)", e5, e5 < 1e-9)

    # ------------------------------------------------- the 72 decisions, scored at EVERY boundary
    P("")
    P("-" * 100)
    P("ARM 2 — THE 72 DECISIONS, SCORED ON THE FULL IS WINDOW AND AT ALL FOUR INNER BOUNDARIES")
    P("-" * 100)
    P("  OUTER (1260's own): pick = IS argmax of the chooser stat on warm-up..2016-12-31;")
    P("                      d = OOS Sharpe(pick) - OOS Sharpe(anchor rung), 2017-2026.")
    P("  INNER at boundary b: pick = argmax on warm-up..b; d_inner = validation Sharpe(pick) -")
    P("                      validation Sharpe(anchor) over b+1..2016-12-31.")
    P("  Scores at both: S_OBS_MARGIN (top-minus-runner-up over |anchor stat|), S_OBS_RATIO")
    P("  (margin / rung spread), S_PBOOT_TOP, S_PBOOT_MARGIN (L = 63, 1000 draws).")
    drows = []
    for pnm in PANELS:
        pan = PAN[pnm]
        for anc in ANCHORS:
            for lad in LADNAMES:
                bks = RB[(pnm, anc, lad)]
                rungs = list(LADDERS[lad])
                anchor_rung = ANCHORS[anc][lad]
                Ris = np.column_stack([bks[r][pan.ins] for r in rungs])
                for ch in CHOOSERS:
                    st = np.array([is_stat(bks[r], pan.ins, ch) for r in rungs], float)
                    order = np.argsort(-np.where(np.isfinite(st), st, -np.inf), kind="stable")
                    top, second = order[0], order[1]
                    pick = rungs[top]
                    spread = float(np.nanmax(st) - np.nanmin(st))
                    margin = float(st[top] - st[second])
                    scale = abs(st[rungs.index(anchor_rung)]) or 1.0
                    pb = pboot_argmax(Ris, ch, L_FROZEN, seed_of(pnm, anc, lad, ch, L_FROZEN))
                    pbo = np.argsort(-pb, kind="stable")
                    mp = blocks_m(bks[pick], pan.warm, pan.ins, pan.oos)
                    ma = blocks_m(bks[anchor_rung], pan.warm, pan.ins, pan.oos)
                    row = dict(
                        panel=pnm, anchor=anc, ladder=lad, chooser=ch, k=len(rungs),
                        anchor_rung=anchor_rung, pick=pick, moved=bool(pick != anchor_rung),
                        S_OBS_MARGIN=margin / scale, S_OBS_RATIO=(margin / spread) if spread > 0 else 0.0,
                        S_PBOOT_TOP=float(pb[top]), S_PBOOT_MARGIN=float(pb[pbo[0]] - pb[pbo[1]]),
                        d=mp["OOS_Sharpe"] - ma["OOS_Sharpe"],
                        pick_OOS_Sharpe=mp["OOS_Sharpe"], anchor_OOS_Sharpe=ma["OOS_Sharpe"],
                        pick_CAGR=mp["CAGR"], pick_Sharpe=mp["Sharpe"], pick_MaxDD=mp["MaxDD"],
                        pick_H1=mp["H1"], pick_H2=mp["H2"],
                        pick_OOS_CAGR=mp["OOS_CAGR"], pick_OOS_MaxDD=mp["OOS_MaxDD"])
                    for bd in BOUNDARIES:
                        tr, va = pan.inner[bd]
                        Rtr = np.column_stack([bks[r][tr] for r in rungs])
                        sti = np.array([is_stat(bks[r], tr, ch) for r in rungs], float)
                        oi = np.argsort(-np.where(np.isfinite(sti), sti, -np.inf), kind="stable")
                        itop, isec = oi[0], oi[1]
                        ipick = rungs[itop]
                        ispread = float(np.nanmax(sti) - np.nanmin(sti))
                        imargin = float(sti[itop] - sti[isec])
                        iscale = abs(sti[rungs.index(anchor_rung)]) or 1.0
                        ipb = pboot_argmax(Rtr, ch, L_FROZEN, seed_of("inner", pnm, anc, lad, ch)
                                           if bd == "2012-12-31" else seed_of("inner", bd, pnm, anc, lad, ch))
                        ipbo = np.argsort(-ipb, kind="stable")
                        tag = bd[:4]
                        row[f"i{tag}_pick"] = ipick
                        row[f"i{tag}_moved"] = bool(ipick != anchor_rung)
                        row[f"i{tag}_d"] = fsharpe(bks[ipick][va]) - fsharpe(bks[anchor_rung][va])
                        row[f"i{tag}_S_OBS_MARGIN"] = imargin / iscale
                        row[f"i{tag}_S_OBS_RATIO"] = (imargin / ispread) if ispread > 0 else 0.0
                        row[f"i{tag}_S_PBOOT_TOP"] = float(ipb[itop])
                        row[f"i{tag}_S_PBOOT_MARGIN"] = float(ipb[ipbo[0]] - ipb[ipbo[1]])
                    drows.append(row)
    dec = pd.DataFrame(drows)
    assert len(dec) == 72, len(dec)
    dump(dec, "decisions")
    P(f"  {len(dec)} decisions;  moved {int(dec.moved.sum())} of 72;  mean d {dec.d.mean():+.4f} "
      f"(t {tstat(dec.d):+.2f}), 1260 committed {C1260_DALL:+.4f}")
    gate("G6", "mean d over all 72 vs 1260's committed +0.0095", abs(dec.d.mean() - C1260_DALL),
         abs(dec.d.mean() - C1260_DALL) < 5e-3)
    for bd in BOUNDARIES:
        tag = bd[:4]
        P(f"  inner {tag}: moved {int(dec[f'i{tag}_moved'].sum())} of 72,  mean d_inner "
          f"{dec[f'i{tag}_d'].mean():+.4f} (t {tstat(dec[f'i{tag}_d']):+.2f}),  pick == outer pick at "
          f"{int((dec[f'i{tag}_pick'] == dec['pick']).sum())} of 72")

    base_sel = float(dec.anchor_OOS_Sharpe.mean())
    act_sel = float(dec.pick_OOS_Sharpe.mean())
    gate("G7", "do-nothing / always-act mean OOS Sharpe vs 1246/1260's committed 0.7922 / 0.8016",
         max(abs(base_sel - C1246_ANCHOR_OOS), abs(act_sel - C1246_ACT_OOS)),
         max(abs(base_sel - C1246_ANCHOR_OOS), abs(act_sel - C1246_ACT_OOS)) < 5e-3)
    bkey = books.set_index(["panel", "anchor", "ladder", "rung"])

    def realised(mask):
        oos, both = [], 0
        for (_, r), f in zip(dec.iterrows(), mask):
            rung = r.pick if f else r.anchor_rung
            row = bkey.loc[(r.panel, r.anchor, r.ladder, rung)]
            oos.append(float(row.OOS_Sharpe))
            both += int(bool(row.pass_4b_full) and bool(row.pass_4b_oos))
        return float(np.mean(oos)), both

    def n_distinct(mask):
        sub = dec[np.asarray(mask, bool)]
        return int(sub[["panel", "anchor", "ladder", "pick"]].drop_duplicates().shape[0])

    _, both_anchor = realised(np.zeros(72, bool))
    _, both_act = realised(np.ones(72, bool))
    P(f"  DO NOTHING mean OOS Sharpe {base_sel:.4f} (4b BOTH {both_anchor});  "
      f"ALWAYS ACT {act_sel:.4f} (4b BOTH {both_act})")

    # -------------------------------------------- ARM 3: the 24 cells at every boundary
    P("")
    P("-" * 100)
    P("ARM 3 — THE 24 (SCORE, QUANTILE) CELLS: OUTER VALUE ONCE, INNER VALUE AT ALL 4 BOUNDARIES")
    P("-" * 100)
    crows = []
    for sc in SCORES:
        for q in QUANTS:
            obar = float(dec[sc].quantile(q))
            fo = (dec[sc] >= obar).values
            ao, bo = dec.d[fo], dec.d[~fo]
            outer = (ao.mean() - bo.mean()) if len(bo) and len(ao) else np.nan
            sel_oos, n_both = realised(fo)
            row = dict(score=sc, side=("OBS" if sc in OBS_SIDE else "BAR"), quantile=q,
                       outer_bar=obar, outer_n_fire=int(fo.sum()), outer_n_distinct=n_distinct(fo),
                       outer_d_fire=ao.mean(), outer_d_refuse=bo.mean(), outer_lic_minus_ref=outer,
                       outer_welch=welch_t(ao, bo), sel_mean_OOS_Sharpe=sel_oos,
                       d_sel=sel_oos - base_sel, n_4b_both=n_both)
            for bd in BOUNDARIES:
                tag = bd[:4]
                isc, idd = f"i{tag}_{sc}", f"i{tag}_d"
                ibar = float(dec[isc].quantile(q))
                fi = (dec[isc] >= ibar).values
                ai, bi = dec[idd][fi], dec[idd][~fi]
                row[f"inner{tag}_bar"] = ibar
                row[f"inner{tag}_n_fire"] = int(fi.sum())
                row[f"inner{tag}_lic_minus_ref"] = (ai.mean() - bi.mean()) if len(bi) and len(ai) else np.nan
            crows.append(row)
    cells = pd.DataFrame(crows)
    dump(cells, "cells")
    P(f"  {'SCORE':<16s} {'q':>5s} {'fire':>5s} {'dist':>5s} {'outLIC-REF':>11s} {'welch':>7s} "
      f"{'d_sel':>8s} {'4bB':>4s} | " + " ".join(f"{'in' + bd[:4]:>9s}" for bd in BOUNDARIES))
    for _, r in cells.iterrows():
        P(f"  {r['score']:<16s} {r['quantile']:5.2f} {r['outer_n_fire']:5d} {r['outer_n_distinct']:5d} "
          f"{r['outer_lic_minus_ref']:+11.4f} {r['outer_welch']:+7.2f} {r['d_sel']:+8.4f} "
          f"{int(r['n_4b_both']):4d} | " + " ".join(f"{r['inner' + bd[:4] + '_lic_minus_ref']:+9.4f}" for bd in BOUNDARIES))

    # -------------------------------------------- ARM 4: the 12-cell dial grid (THIS RUN'S DIALS)
    P("")
    P("-" * 100)
    P("ARM 4 — THE 12-CELL GRID: RULE 8 ON THE DIAL AT EVERY (INNER BOUNDARY, SCORE CLASS)")
    P("-" * 100)
    P(f"  {'boundary':<12s} {'class':<5s} {'k':>3s} {'chosen cell':<24s} {'inLIC-REF':>10s} "
      f"{'outLIC-REF':>11s} {'d_sel':>8s} {'4bB':>4s} {'rho_in_out':>11s} {'bestOut':>9s} {'regret':>8s}")
    grows = []
    for bd in BOUNDARIES:
        tag = bd[:4]
        for cls, scs in CLASSES.items():
            sub = cells[cells.score.isin(scs)].reset_index(drop=True)
            inner_col = f"inner{tag}_lic_minus_ref"
            j = int(sub[inner_col].idxmax())
            ch = sub.loc[j]
            rho = spear(sub[inner_col], sub.outer_lic_minus_ref)
            best_out = float(sub.outer_lic_minus_ref.max())
            best_dsel = float(sub.d_sel.max())
            grows.append(dict(boundary=bd, score_class=cls, k_cells=len(sub),
                              chosen_score=str(ch["score"]), chosen_quantile=float(ch["quantile"]),
                              inner_lic_minus_ref=float(ch[inner_col]),
                              inner_n_fire=int(ch[f"inner{tag}_n_fire"]),
                              outer_lic_minus_ref=float(ch.outer_lic_minus_ref),
                              outer_n_fire=int(ch.outer_n_fire), outer_n_distinct=int(ch.outer_n_distinct),
                              sel_mean_OOS_Sharpe=float(ch.sel_mean_OOS_Sharpe), d_sel=float(ch.d_sel),
                              n_4b_both=int(ch.n_4b_both), do_nothing_4b=both_anchor,
                              rho_inner_outer=rho, best_outer_in_class=best_out,
                              regret_lic=best_out - float(ch.outer_lic_minus_ref),
                              best_dsel_in_class=best_dsel, regret_dsel=best_dsel - float(ch.d_sel)))
            g = grows[-1]
            cellname = "{} @ q{:.2f}".format(g["chosen_score"], g["chosen_quantile"])
            P(f"  {bd:<12s} {cls:<5s} {len(sub):3d} {cellname:<24s} "
              f"{g['inner_lic_minus_ref']:+10.4f} {g['outer_lic_minus_ref']:+11.4f} {g['d_sel']:+8.4f} "
              f"{g['n_4b_both']:4d} {g['rho_inner_outer']:+11.4f} {g['best_outer_in_class']:+9.4f} "
              f"{g['regret_lic']:8.4f}")
    grid = pd.DataFrame(grows)
    dump(grid, "grid")

    # the frozen 1260 cell, gated
    g1260 = grid[(grid.boundary == "2012-12-31") & (grid.score_class == "ALL")].iloc[0]
    P("")
    P(f"  1260's OWN CELL (boundary 2012-12-31, class ALL): chosen {g1260.chosen_score} @ "
      f"q{g1260.chosen_quantile:.2f}  [1260: {C1260_INNER_ARGMAX[0]} @ q{C1260_INNER_ARGMAX[1]:.2f}]")
    P(f"    outer LIC-REF {g1260.outer_lic_minus_ref:+.4f} [1260 {C1260_OUTER_LICREF_AT_ARGMAX:+.4f}], "
      f"d_sel {g1260.d_sel:+.4f} [1260 {C1260_DSEL_AT_ARGMAX:+.4f}], 4b {int(g1260.n_4b_both)} vs "
      f"{both_anchor} [1260 {C1260_4B_AT_ARGMAX} vs {C1260_4B_DONOTHING}]")
    P(f"    rank corr inner/outer {g1260.rho_inner_outer:+.4f} [1260 {C1260_RHO_INNER_OUTER:+.4f}]")
    same = (g1260.chosen_score == C1260_INNER_ARGMAX[0]) and abs(g1260.chosen_quantile - C1260_INNER_ARGMAX[1]) < 1e-9
    gate("G8", "1260's rule-8 chosen cell reproduced at its own boundary/class", 0.0 if same else 1.0, same)
    gate("G9", "1260's outer LIC-REF at that cell", abs(g1260.outer_lic_minus_ref - C1260_OUTER_LICREF_AT_ARGMAX),
         abs(g1260.outer_lic_minus_ref - C1260_OUTER_LICREF_AT_ARGMAX) < 5e-3)
    gate("G10", "1260's d_sel at that cell", abs(g1260.d_sel - C1260_DSEL_AT_ARGMAX),
         abs(g1260.d_sel - C1260_DSEL_AT_ARGMAX) < 5e-3)
    gate("G11", "1260's inner/outer rank corr at its own boundary/class",
         abs(g1260.rho_inner_outer - C1260_RHO_INNER_OUTER),
         abs(g1260.rho_inner_outer - C1260_RHO_INNER_OUTER) < 0.05)
    best_obs = float(cells[cells.side == "OBS"].outer_lic_minus_ref.max())
    gate("G12", "1260's best observed-side cell LIC-REF +0.1839", abs(best_obs - C1260_BEST_OBS),
         abs(best_obs - C1260_BEST_OBS) < 5e-3)

    # ---------------------------------------------------------------- ARM 5: the three hypotheses
    P("")
    P("-" * 100)
    P("ARM 5 — WHAT THE 12 CELLS SAY ABOUT 1260's -0.4292")
    P("-" * 100)
    n_pos = int((grid.rho_inner_outer > 0).sum())
    P(f"  H_CORR    : rank corr > 0 at {n_pos} of {len(grid)} grid points; "
      f"values {'  '.join(f'{v:+.4f}' for v in grid.rho_inner_outer)}")
    P(f"              mean {grid.rho_inner_outer.mean():+.4f}, median {grid.rho_inner_outer.median():+.4f}, "
      f"min {grid.rho_inner_outer.min():+.4f}, max {grid.rho_inner_outer.max():+.4f}")
    for cls in CLASSES:
        sub = grid[grid.score_class == cls]
        P(f"              class {cls:<4s}: {'  '.join(f'{v:+.4f}' for v in sub.rho_inner_outer)}  "
          f"(mean {sub.rho_inner_outer.mean():+.4f})")
    P(f"  H_TRANSFER: mean outer d_sel of the 12 chosen cells {grid.d_sel.mean():+.4f} "
      f"(median {grid.d_sel.median():+.4f}, > 0 at {int((grid.d_sel > 0).sum())} of {len(grid)})")
    P(f"              mean outer LIC-REF of the chosen cells {grid.outer_lic_minus_ref.mean():+.4f} "
      f"(> 0 at {int((grid.outer_lic_minus_ref > 0).sum())} of {len(grid)})")
    P(f"              mean regret against the best outer cell in the same class "
      f"{grid.regret_lic.mean():+.4f} LIC-REF, {grid.regret_dsel.mean():+.4f} d_sel")
    stable = {}
    for cls in CLASSES:
        sub = grid[grid.score_class == cls]
        cellset = sub.chosen_score + "@" + sub.chosen_quantile.map(lambda x: f"{x:.2f}")
        vc = cellset.value_counts()
        stable[cls] = int(vc.iloc[0])
        P(f"  H_STABLE  : class {cls:<4s} chose {list(cellset)} -> modal cell {vc.index[0]} at "
          f"{int(vc.iloc[0])} of 4 boundaries")
    n_beat = int(((grid.d_sel > 0) & (grid.n_4b_both >= both_anchor)).sum())
    P(f"  H_CAPITAL : chosen cells beating do-nothing on mean OOS Sharpe: {int((grid.d_sel > 0).sum())} of 12;")
    P(f"              and doing so WITHOUT costing a 4b pass ({both_anchor}): {n_beat} of 12")
    P(f"              mean 4b BOTH of the 12 chosen selectors {grid.n_4b_both.mean():.2f} vs do-nothing {both_anchor}")

    H_CORR = n_pos > len(grid) / 2
    H_TRANSFER = bool(grid.d_sel.mean() > 0)
    H_STABLE = all(v >= 3 for v in stable.values())
    H_1260 = same and abs(g1260.rho_inner_outer - C1260_RHO_INNER_OUTER) < 0.05
    H_CAPITAL = n_beat > 0

    # ------------------------------------------------------- ARM 6: capital, both KEEP paths
    P("")
    P("-" * 100)
    P("ARM 6 — CAPITAL: BOTH KEEP PATHS ON THE 162 RUNG BOOKS AND ON THE SELECTED BOOKS")
    P("-" * 100)
    P(f"  4a (beat the live book): {int(books.pass_4a.sum())} of {len(books)}   "
      f"failing A_DD at {int((~books.A_DD).sum())} of {len(books)} (live RULES v2's shallow MaxDD)")
    P(f"  4b full {int(books.pass_4b_full.sum())};  4b OOS {int(books.pass_4b_oos.sum())};  "
      f"BOTH {int((books.pass_4b_full & books.pass_4b_oos).sum())}  "
      f"-> {int(books[books.pass_4b_full & books.pass_4b_oos][['panel','anchor','ladder','rung']].drop_duplicates().shape[0])} rows, "
      f"{books[books.pass_4b_full & books.pass_4b_oos].groupby('panel').size().to_dict()}")
    for leg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        P(f"    4b leg {leg:<7s} fails at {int((~books[leg]).sum()):>3d} of {len(books)}")
    both = books[books.pass_4b_full & books.pass_4b_oos].copy()
    if len(both):
        keycols = ["panel", "anchor", "ladder", "rung", "N", "H", "GROSS", "CADENCE"]
        u_both = both.drop_duplicates(subset=["panel", "N", "H", "GROSS", "CADENCE"])
        P(f"  distinct 4b BOTH books: {len(u_both)}")
        for _, r in u_both.sort_values("OOS_Sharpe", ascending=False).head(12).iterrows():
            P(f"    {r.panel:<6s} N={r.N:<3.0f} H={r.H:<4.0f} G={r.GROSS:.2f} {r.CADENCE:<2s}  "
              f"full {r.CAGR:>7.2%} / {r.Sharpe:.4f} / {r.MaxDD:>7.2%}  halves {r.H1:.4f}/{r.H2:.4f}  "
              f"OOS {r.OOS_CAGR:>7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:>7.2%}")
    P("  NOTE: every one of these is prior art (1260's own census) — this run adds no new book.")
    P("  THE RULE-8 SELECTORS THEMSELVES, as books:")
    wrows = []
    for _, g in grid.iterrows():
        sc, q = g.chosen_score, g.chosen_quantile
        bar = float(dec[sc].quantile(q))
        f = (dec[sc] >= bar).values
        oos_list, full_list, dd_list = [], [], []
        for (_, r), fired in zip(dec.iterrows(), f):
            rung = r.pick if fired else r.anchor_rung
            row = bkey.loc[(r.panel, r.anchor, r.ladder, rung)]
            oos_list.append(float(row.OOS_Sharpe)); full_list.append(float(row.Sharpe)); dd_list.append(float(row.MaxDD))
        wrows.append(dict(boundary=g.boundary, score_class=g.score_class, cell=f"{sc}@q{q:.2f}",
                          n_fire=int(f.sum()), n_distinct=n_distinct(f),
                          sel_mean_full_Sharpe=float(np.mean(full_list)),
                          sel_mean_OOS_Sharpe=float(np.mean(oos_list)),
                          sel_mean_MaxDD=float(np.mean(dd_list)), d_sel=g.d_sel,
                          n_4b_both=int(g.n_4b_both), do_nothing_OOS=base_sel,
                          do_nothing_4b=both_anchor, always_act_OOS=act_sel, always_act_4b=both_act))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    for _, r in wf.iterrows():
        P(f"    {r.boundary} {r.score_class:<4s} {r.cell:<22s} fires {r.n_fire:>2d} ({r.n_distinct} distinct)  "
          f"mean full Sharpe {r.sel_mean_full_Sharpe:.4f}  mean OOS {r.sel_mean_OOS_Sharpe:.4f} "
          f"({r.d_sel:+.4f})  4b {r.n_4b_both}")

    # ------------------------------------------------------------------------- verdict
    P("")
    P("-" * 100)
    P("VERDICT")
    P("-" * 100)
    if not H_CORR and not H_TRANSFER:
        outcome = "(A) ANTI-SELECTION IS A FACT"
    elif H_CORR and H_TRANSFER:
        outcome = "(B) 1260's -0.4292 WAS ONE UNLUCKY SPLIT"
    else:
        outcome = "(C) THE DIAL IS UNRESOLVED AT THIS SAMPLE SIZE"
    P(f"  OUTCOME: {outcome}")
    P(f"  H_CORR {'SUPPORTED' if H_CORR else 'REFUTED'};  H_TRANSFER {'SUPPORTED' if H_TRANSFER else 'REFUTED'};"
      f"  H_STABLE {'SUPPORTED' if H_STABLE else 'REFUTED'};  H_1260 {'SUPPORTED' if H_1260 else 'REFUTED'};"
      f"  H_CAPITAL {'SUPPORTED' if H_CAPITAL else 'REFUTED'}")
    P(f"  CAPITAL: 4a 0 of {len(books)} unless stated above; no new book; KILL (capital) unless a")
    P("  chosen selector both beats do-nothing and keeps every 4b pass.")

    gate("G13", "determinism: 12 grid rows, 24 cells, 72 decisions, 162 books",
         abs(len(grid) - 12) + abs(len(cells) - 24) + abs(len(dec) - 72) + abs(len(books) - 162),
         len(grid) == 12 and len(cells) == 24 and len(dec) == 72 and len(books) == 162)
    spy_days = int((PAN["SMALL"].elig[:, list(PAN["SMALL"].px.columns).index("SPY")]).sum())
    gate("G14", "SPY never eligible on SMALL (benchmark, not constituent)", spy_days, spy_days == 0)

    gates = pd.DataFrame(GATES)
    dump(gates, "gates")
    P(f"  GATES {int(gates.pass_.sum())} of {len(gates)}")
    P(f"  elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
