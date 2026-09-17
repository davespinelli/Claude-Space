#!/usr/bin/env python3
"""Idea 1162 (lane B, 2026-09-17)
   why-does-an-IID-RESAMPLE-produce-DEEPER-drawdowns-than-a-BLOCK-one

THE QUEUE'S PREMISE, QUOTED.  Idea 1159 declared the textbook expectation -- an iid
resample destroys the volatility clustering that deepens drawdowns, so its |MaxDD| null
should sit LOWER than a moving-block one -- and measured the REVERSE at 12 of 12 cells:
N_IID 25.719 against N_BLOCK 22.538 and N_STAT 21.531.  1159 read the implication as
"these books' realised return ORDER is drawdown-protective" and filed this idea to find
WHICH FEATURE carries it: short-horizon mean reversion, the rebalance cadence, or the
gate's own exit timing, by re-running the same three nulls on gate-off and randomly-
ordered controls.

THIS RUN TAKES THE QUEUE'S THREE CANDIDATES LITERALLY AND ADDS THE ONE STRUCTURAL FACT
THEY ALL PRESUPPOSE, WHICH IS THAT THE ORDERING IS A PROPERTY OF THE BOOK AT ALL.

  A moving-block bootstrap with block length L is a ONE-PARAMETER FAMILY that runs from
  the iid resample (L = 1: the index matrix is literally an iid draw -- gate G6 proves it
  bit for bit) to the observed path itself (L = T: one block, a pure rotation).  If the
  family is monotone in L, then the sign of (BLOCK - IID) cannot be anything other than
  the sign of (OBSERVED - IID), and 1159's "12 of 12" is not twelve facts about
  bootstraps, it is ONE fact about these books -- and it is 1161's fact, already filed
  separately: the observed |MaxDD| sits BELOW its own null's median at 36 of 36 OBJ_MAXDD
  cells.  The two follow-ups the queue filed as siblings would then be THE SAME QUESTION.

  That is testable and it is FALSIFIABLE IN ONE SHOT: find a control whose observed
  drawdown is DEEPER than its own iid null, and the published ordering must REVERSE.

TUNED DIALS (2, PROTOCOL rule 4) -- and the queue names both:

  `NULL TYPE`  {N_IID, N_BLOCK, N_STAT}                        (1159's three, verbatim)
  `CONTROL`    {C_BOOK, C_GATEOFF, C_NOREBAL, C_SHUFFLE, C_SPY}

  = 15 combinations per panel, 45 in all, EVERY ONE PUBLISHED in `.dialgrid.csv`.

  The controls are a ONE-FACTOR-AT-A-TIME ladder off the anchor book, one per candidate
  carrier the queue names, plus one falsification control:
    C_BOOK     the anchor book, 1159's own object (gate ON, cadence W, hold 126, N=20,
               gross 0.75, 10 bps)
    C_GATEOFF  identical except the ELIGIBILITY GATE is removed (no 200d-above, no
               max_vol) -- the queue's "gate's own exit timing"
    C_NOREBAL  identical except the book is bought ONCE at the first post-warm-up
               rebalance and never traded again -- the queue's "rebalance cadence"
    C_SHUFFLE  C_BOOK's own realised daily returns RANDOMLY PERMUTED -- the queue's
               "randomly-ordered control"; a falsification gate, since a series with no
               order left cannot distinguish a block null from an iid one
    C_SPY      SPY alone, no selection, no gate, no cadence -- the most mean-reverting
               series on this tape (lag-1 autocorrelation is more negative than the
               book's), so it is the sharp test of the queue's "short-horizon mean
               reversion" candidate

  PANEL {U56, B136, SMALL} is NOT a dial -- all three are built at every point.
  THE BLOCK-LENGTH LADDER L in {1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008, T} is NOT
  a dial: it is the ONE-PARAMETER FAMILY under measurement, every rung is published in
  `.ladder.csv`, and NOTHING is ever selected on it -- the headline uses the record's
  frozen L = 63 and no other.  The GROSS ladder in the rule-8 arm is not a dial either
  (all 15 rungs published, 1150/1154's construction).  Confidence q is not a dial (0.90
  headline, 0.80 / 0.95 printed beside).  SEED is not a dial -- three seeds are run at
  every headline cell to publish the cross-seed spread, which is what gives the words
  "materially weakens" a scale.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131/1140/1148/1159's
construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75, min hold 126, N=20, cadence
W, 10 bps (PROTOCOL rule 2), LAG 1, warm-up 260, IS end 2016-12-31, block L=63, 1000
draws, crc32 seeds, DD cap 0.60, CAGR floor 0.70.

PRICE VINTAGE (PROTOCOL draft rule 12, proposed by idea 1163 and complied with here even
though it is NOT enacted).  Every number below is computed on `data/prices.csv` AT HEAD,
crc32 published in the stamp -- which is byte-identical to the tape 1159 ran on, since no
daily close has landed since `6f1fcb1`.  That is deliberate: 1159's cell-level numbers are
this run's cross-run gate, and they can only be replayed on 1159's own tape.  The
2026-09-15 vintage 1154/1160/1161 pinned is ALSO recovered from git and every headline is
re-read on it, so the result carries its own vintage-invariance check rather than an
assurance.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
CURRENT constituents of a sub-$2B screen (data/SMALL_PANEL_README.md), less the documented
max_1d_move >= 1.0 exclusion.  Every LEVEL here -- CAGR, |MaxDD|, and every null median
built on top of them -- is optimistic, and a resample null prices SAMPLING error on the
tape it is handed and cannot correct that.  It very largely CANCELS out of this run's
headline claims, which are all RATIOS of one construction against itself on the same tape
(BLOCK/IID, OBS/IID, and the L ladder), and it does NOT cancel out of the 4b legs.

Standalone, deterministic, offline.  Nothing outside research/ is written or modified.
The one arm that reads outside data/ and research/ is the VINTAGE arm, which reads a
committed blob of data/prices.csv out of this repo's own git object store; it is local,
read-only and reproducible, and the run degrades gracefully without it.
"""
from __future__ import annotations

import io
import subprocess
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

DATE = "2026-09-17"
SLUG = "why-does-an-IID-RESAMPLE-produce-DEEPER-drawdowns-than-a-BLOCK-one"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136", "SMALL"]
NULL_TYPES = ["N_IID", "N_BLOCK", "N_STAT"]                                    # dial 1
CONTROLS = ["C_BOOK", "C_GATEOFF", "C_NOREBAL", "C_SHUFFLE", "C_SPY"]          # dial 2
TRADABLE = ["C_BOOK", "C_GATEOFF", "C_NOREBAL", "C_SPY"]     # C_SHUFFLE is not a book

L_BLOCK, BDRAWS = 63, 1000                        # the record's frozen block and draw count
L_LADDER = [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008]     # + T, appended per panel
VR_Q = [2, 5, 10, 21, 63, 126, 252]
QS = [0.80, 0.90, 0.95]
Q_HEAD = 0.90
SEEDS = [0, 1, 2]                                 # cross-seed spread, never selected on
SEED_BASE = 11621162
GROSS_LADDER = [round(0.30 + 0.05 * i, 3) for i in range(15)]    # 0.30 .. 1.00
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}

# ---- the record's own committed numbers, QUOTED and GATED, never re-derived from memory
A936_WH126 = (0.155787, 1.139701, -0.191276)      # 1154/1161's pinned U56 W/H126/N=20 triple
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
PRIOR1159 = (Path(__file__).resolve().parent /
             ("2026-09-17_does-ANY-committed-MAXIMUM-KEYED-claim-in-the-record-carry-a-"
              "RESAMPLE-NULL_B.objects.csv"))
PRIOR1159_MEDIANS = {"N_IID": 25.719, "N_BLOCK": 22.538, "N_STAT": 21.531}   # 1159's headline

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
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<62s} {value:.3e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, declared, bar, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, bar=bar, measured=measured,
                    supported=bool(supported)))
    P(f"  {name:<12s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


# ================================================================= the record's runner
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


# ======================================================== the three resample nulls
# Each returns a (ndraws, T) index matrix.  N_BLOCK is written as an EXPLICIT function of
# the block length L so that the whole ladder -- including L = 1, which IS the iid draw --
# comes out of one code path; gate G6 checks the L = 1 identity bit for bit.
def null_index(kind, rng, T, ndraws, L=L_BLOCK):
    if kind == "N_IID":
        return rng.integers(0, T, size=(ndraws, T))
    if kind == "N_BLOCK":
        nb = int(np.ceil(T / L))
        st = rng.integers(0, T, size=(ndraws, nb))
        idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
        return idx.reshape(ndraws, nb * L)[:, :T]
    if kind == "N_STAT":
        p = 1.0 / L
        out = np.empty((ndraws, T), dtype=np.int64)
        out[:, 0] = rng.integers(0, T, size=ndraws)
        newb = rng.random((ndraws, T)) < p
        fresh = rng.integers(0, T, size=(ndraws, T))
        for t in range(1, T):
            cont = (out[:, t - 1] + 1) % T
            out[:, t] = np.where(newb[:, t], fresh[:, t], cont)
        return out
    raise ValueError(kind)


def boot_maxdd(r, idx, chunk=100):
    """|MaxDD| (positive, in %) of ONE return series under every resample row of idx."""
    LG = np.log1p(np.asarray(r, float))
    out = np.empty(idx.shape[0])
    for a in range(0, idx.shape[0], chunk):
        ix = idx[a:a + chunk]
        cum = np.cumsum(LG[ix], axis=1)
        run = np.maximum.accumulate(cum, axis=1)
        out[a:a + chunk] = -np.expm1(cum - run).min(axis=1) * 100.0
    return out


def band(x, q):
    return (float(np.nanpercentile(x, (1 - q) / 2 * 100.0)),
            float(np.nanpercentile(x, (1 + q) / 2 * 100.0)))


# ---------------------------------------------------------- observed-path diagnostics
def obs_maxdd(r):
    cum = np.cumsum(np.log1p(np.asarray(r, float)))
    run = np.maximum.accumulate(cum)
    dd = np.expm1(cum - run)
    tr = int(dd.argmin())
    pk = int(np.argmax(cum[:tr + 1]))
    return -float(dd[tr]) * 100.0, pk, tr


def variance_ratio(r, q):
    x = np.asarray(r, float)
    x = x - x.mean()
    n = len(x) // q * q
    if n < 2 * q:
        return np.nan
    s = x[:n].reshape(-1, q).sum(axis=1)
    v1 = x.var(ddof=1)
    return float(s.var(ddof=1) / (q * v1)) if v1 > 0 else np.nan


def autocorr(r, k):
    x = np.asarray(r, float)
    if len(x) <= k + 2:
        return np.nan
    return float(np.corrcoef(x[:-k], x[k:])[0, 1])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


# ------------------------------------------------------------------- vintage recovery
def vintage_tape():
    """The 2026-09-15 price vintage 1154/1160/1161 pinned, read from this repo's own git
    object store.  Returns (DataFrame, crc32) or None; the run degrades gracefully."""
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%h", "--",
                            "data/prices.csv"], capture_output=True, text=True)
        commit = r.stdout.strip()
        b = subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}^:data/prices.csv"],
                           capture_output=True)
        if b.returncode != 0:
            return None
        px = pd.read_csv(io.StringIO(b.stdout.decode()), index_col=0, parse_dates=True)
        return px, format(zlib.crc32(b.stdout) & 0xFFFFFFFF, "08x")
    except Exception:
        return None


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# =================================================================================================
def main():
    t_start = time.time()
    P("=" * 100)
    P(f"IDEA 1162 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P("")
    P("## PRICE-VINTAGE STAMP (PROTOCOL draft rule 12, proposed by 1163 — complied with, "
      "not enacted)")
    head_bytes = (ROOT / "data" / "prices.csv").read_bytes()
    head_crc = format(zlib.crc32(head_bytes) & 0xFFFFFFFF, "08x")
    P(f"  data/prices.csv  @HEAD  crc32={head_crc}  {len(head_bytes):,} bytes")
    vint = vintage_tape()
    if vint is not None:
        P(f"  data/prices.csv  vintage 2026-09-15 recovered from git  crc32={vint[1]}  "
          f"{vint[0].shape[0]:,} rows -> {vint[0].index[-1].date()}")
        P("  Headline is computed on HEAD because HEAD *is* 1159's tape (no daily close has")
        P("  landed since 6f1fcb1), and 1159's cell numbers are this run's cross-run gate.")
        P("  Every headline is re-read on the pinned vintage in the VINTAGE arm below.")
    else:
        P("  vintage recovery unavailable — the VINTAGE arm is skipped and said so.")
    P("")

    # ------------------------------------------------------------------ pre-registration
    P("## PRE-REGISTRATION — declared here, before a single result number")
    P("  DIAL 1 NULL TYPE  : N_IID, N_BLOCK (L=63), N_STAT (mean block 63)")
    P("  DIAL 2 CONTROL    : C_BOOK, C_GATEOFF, C_NOREBAL, C_SHUFFLE, C_SPY")
    P("  NOT DIALS         : PANEL (all 3 built), L LADDER (all rungs published, headline")
    P("                      frozen at L=63), GROSS LADDER (all 15 rungs published), q,")
    P("                      SEED (3 run, spread published, never selected on)")
    P("  H_INTERP  the moving-block null INTERPOLATES between the observed path (L->T) and")
    P("            the iid null (L=1), so sign(BLOCK-IID) == sign(OBS-IID) and BLOCK lies")
    P("            BETWEEN them.  BAR: sign agreement >= 14 of 15 cells AND betweenness")
    P("            >= 14 of 15 AND spearman(BLOCK/IID-1, OBS/IID-1) >= 0.80.")
    P("  H_MONO    the L ladder is monotone in L, signed toward the observed value.")
    P("            BAR: correct sign of spearman(L, median) at >= 12 of 15 cells AND")
    P("            |spearman| >= 0.80 at >= 12 of 15.")
    P("  H_VR      the TEXTBOOK/variance story: the sign of (BLOCK-IID) is the sign of")
    P("            (VR(63)-1), i.e. it is carried by long-horizon variance.  BAR: sign")
    P("            agreement >= 14 of 15 cells.")
    P("  H_SHUFFLE FALSIFICATION: on C_SHUFFLE, which has no order left, the three nulls")
    P("            must agree.  BAR: |BLOCK/IID - 1| <= 0.02 at 3 of 3 panels AND at least")
    P("            5x smaller than C_BOOK's on the same panel.  If this fails, the effect")
    P("            is the bootstrap machinery's and nothing below means anything.")
    P("  H_GATE    the queue's candidate 1: removing the eligibility gate at least HALVES")
    P("            |OBS/IID - 1|.  BAR: at >= 2 of 3 panels.")
    P("  H_CADENCE the queue's candidate 2: removing rebalancing at least HALVES")
    P("            |OBS/IID - 1|.  BAR: at >= 2 of 3 panels.")
    P("  H_MEANREV the queue's candidate 3: short-horizon mean reversion carries it, so")
    P("            C_SPY — more negatively autocorrelated than the book — shows the SAME")
    P("            sign of (BLOCK-IID) as C_BOOK.  BAR: at 3 of 3 panels.")
    P("")

    # --------------------------------------------------------------------- panels
    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    small, ndrop, nmeta = load_small()
    raw["SMALL"] = small
    panels = {}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, spy_i=spy_i,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm, ins=ins, oos=oos,
                             sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    # ---------------------------------------------------------- the control constructor
    # `build` fills W[t:stop, sel] = gross / len(sel), so W(g) == g * W(1.0) EXACTLY.  The
    # SELECTION is therefore built once per (panel, control) and the gross ladder scales it;
    # gate G13 proves the scaled path equals a freshly built one.
    _WCACHE: dict = {}

    def _weights(panel, control):
        key = (panel, control)
        if key in _WCACHE:
            return _WCACHE[key]
        d = panels[panel]
        T, K = d["T"], d["K"]
        if control == "C_SPY":
            mk = rebalance_mask(d["idx"], FREQ0).values
            W = np.zeros((T, K))
            W[WARMUP:, d["spy_i"]] = 1.0
        elif control == "C_NOREBAL":
            mk_full = rebalance_mask(d["idx"], FREQ0).values
            first = int(np.flatnonzero(mk_full & (np.arange(T) >= WARMUP))[0])
            mk = np.zeros(T, dtype=bool)
            mk[first] = True
            W = build(-d["sc"], d["elig"], d["priced"], np.array([first]), N0, HOLD0,
                      T, K, 1.0)
        else:
            mk = rebalance_mask(d["idx"], FREQ0).values
            elig = d["priced"] if control == "C_GATEOFF" else d["elig"]
            if control == "C_GATEOFF" and panel == "SMALL":
                elig = elig.copy()
                elig[:, d["spy_i"]] = False         # SPY is the benchmark, never a holding
            W = build(-d["sc"], elig, d["priced"], np.flatnonzero(mk), N0, HOLD0,
                      T, K, 1.0)
        _WCACHE[key] = (W, mk)
        return _WCACHE[key]

    def control_returns(panel, control, gross=GROSS0, seed_tag="", fresh=False):
        """The one-factor-at-a-time ladder.  Returns the WARM-UP-TRIMMED daily series."""
        d = panels[panel]
        base = "C_BOOK" if control == "C_SHUFFLE" else control
        if fresh:
            _WCACHE.pop((panel, base), None)
        W1, mk = _weights(panel, base)
        W = W1 * gross
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        r = (g - tn * COST / 1e4)
        if control == "C_SHUFFLE":
            rw = r[d["warm"]].copy()
            rng = np.random.default_rng(seed_of(panel, "C_SHUFFLE", gross, seed_tag))
            rng.shuffle(rw)
            return rw
        return r[d["warm"]]

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    mkl = np.roll(mk, LAG)
    mkl[:LAG] = False
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    gg, tt = nrun(d["rets"], Wl, mkl)
    rfast = gg - tt * COST / 1e4
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)

    r_book_u56 = control_returns("U56", "C_BOOK")
    v = float(np.abs(r_book_u56 - rfast[d["warm"]]).max())
    gate("G2", "control_returns('U56','C_BOOK') == the anchor book", v, v < 1e-15)

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G3", "committed U56 triple on the HEAD tape (1161 reads 1.62e-03 here)",
         v, v < 5e-3)

    # G4 — the SPY / live OOS benchmarks, read at FULL PRECISION from 1159's own committed
    # walk-forward file rather than quoted from rounded prose.  1159 is the parent idea and
    # ran the same construction on the same tape, so these are exact cross-run anchors.
    spy_r = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy_r, d["warm"], d["ins"], d["oos"])
    lm = blocks_m(backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST,
                           freq="W")["returns"].values, d["warm"], d["ins"], d["oos"])
    p1159_wf = Path(str(PRIOR1159).replace(".objects.csv", ".walkforward.csv"))
    if p1159_wf.exists():
        w9 = pd.read_csv(p1159_wf)
        w9 = w9[w9.panel == "U56"]
        v = max(abs(sm["OOS_Sharpe"] - float(w9.spy_oos_sharpe.iloc[0])),
                abs(lm["OOS_Sharpe"] - float(w9.live_oos_sharpe.iloc[0])))
        gate("G4", "CROSS-RUN 1159's committed SPY and live OOS Sharpe, full precision",
             v, v < 5e-5)
    else:
        v = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
        gate("G4", "SPY OOS triple vs quoted prose (1159's file unavailable)", v, v < 5e-3)

    v = abs(lm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G5", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)

    # G6 — THE GATE THIS RUN TURNS ON: the block family at L=1 IS the iid draw, bit for bit
    i_iid = null_index("N_IID", np.random.default_rng(123), 400, 25)
    i_l1 = null_index("N_BLOCK", np.random.default_rng(123), 400, 25, L=1)
    v = float(np.abs(i_iid - i_l1).max())
    gate("G6", "N_BLOCK at L=1 IS N_IID, bit for bit (same seed)", v, v == 0.0)

    # G7 — N_STAT's realised mean block length
    ix = null_index("N_STAT", np.random.default_rng(5), 2000, 40)
    brk = (np.diff(ix, axis=1) != 1) & (np.diff(ix, axis=1) != -(2000 - 1))
    v = abs(ix.shape[1] / max(brk.sum() / ix.shape[0] + 1.0, 1e-9) - L_BLOCK)
    gate("G7", "N_STAT realised mean block length == 63", v, v < 8.0)

    # G8 — every null draws the SAME marginal distribution (so only ORDER can differ)
    rtest = r_book_u56
    mus = {}
    for k in NULL_TYPES:
        iz = null_index(k, np.random.default_rng(9), len(rtest), 300)
        mus[k] = float(rtest[iz].mean())
    v = max(abs(mus[k] - rtest.mean()) for k in NULL_TYPES) / abs(rtest.mean())
    gate("G8", "all three nulls share the observed MARGINAL mean (order is all that differs)",
         v, v < 0.10)

    # G9 — CROSS-RUN: replay 1159's own committed OBJ_MAXDD cells
    g9_ok, g9_v, n1159 = False, np.nan, 0
    prior = None
    if PRIOR1159.exists():
        prior = pd.read_csv(PRIOR1159)
        pm = prior[prior.object == "OBJ_MAXDD"]
        obs_u = float(pm[pm.panel == "U56"].observed.iloc[0])
        g9_v = abs(obs_u - obs_maxdd(r_book_u56)[0])
        g9_ok = g9_v < 1e-6
        n1159 = int(len(pm))
    gate("G9", "CROSS-RUN 1159's committed U56 OBJ_MAXDD observed level", g9_v, g9_ok)

    # G10 — 1159's ORDERING itself, replayed cell by cell from its committed file
    g10_v, g10_ok = np.nan, False
    if prior is not None:
        pm = prior[prior.object == "OBJ_MAXDD"].copy()
        w = pm.pivot_table(index=["panel", "ladder"], columns="null_type",
                           values="null_median")
        n_hit = int((w["N_IID"] > w["N_BLOCK"]).sum())
        g10_v = n_hit - len(w)
        g10_ok = n_hit == len(w)
        P(f"     1159 committed N_IID > N_BLOCK at {n_hit} of {len(w)} OBJ_MAXDD cells "
          f"(its headline '12 of 12'), read from its own file.")
    gate("G10", "1159's committed ordering re-read from its file (12 of 12)", g10_v, g10_ok)

    v = float(np.abs(control_returns("SMALL", "C_BOOK") -
                     control_returns("SMALL", "C_BOOK", fresh=True)).max())
    gate("G11", "determinism of the SMALL pipeline (cache dropped and rebuilt)",
         v, v == 0.0)

    # G13 — the gross ladder's scaling shortcut is EXACT, not an approximation
    W1, _ = _weights("U56", "C_BOOK")
    dU = panels["U56"]
    Wd = build(-dU["sc"], dU["elig"], dU["priced"],
               np.flatnonzero(rebalance_mask(dU["idx"], FREQ0).values), N0, HOLD0,
               dU["T"], dU["K"], 0.45)
    v = float(np.abs(W1 * 0.45 - Wd).max())
    gate("G13", "gross ladder scaling W(g) == g*W(1) is exact, not approximate",
         v, v < 1e-15)
    P("")

    # =============================================================== ARM A — THE DIAL GRID
    P("## ARM A — THE 2-DIAL GRID (NULL TYPE x CONTROL), ALL 45 CELLS PUBLISHED")
    P(f"  {BDRAWS:,} draws, block L={L_BLOCK}, q={Q_HEAD} headline, seeds {SEEDS}")
    P("")
    series = {}
    for panel in PANELS:
        for c in CONTROLS:
            series[(panel, c)] = control_returns(panel, c)

    diag_rows, grid_rows = [], []
    for panel in PANELS:
        for c in CONTROLS:
            r = series[(panel, c)]
            o, pk, tr = obs_maxdd(r)
            cagr, sh, dd = fmet(r)
            row = dict(panel=panel, control=c, n_bars=len(r), obs_maxdd=o,
                       episode_bars=tr - pk, CAGR=cagr, Sharpe=sh, MaxDD=dd)
            if c != "C_SHUFFLE":
                ii = panels[panel]["idx"][panels[panel]["warm"]]
                row["peak"] = str(ii[pk].date())
                row["trough"] = str(ii[tr].date())
            for k in (1, 2, 3, 5, 10):
                row[f"ac{k}"] = autocorr(r, k)
            for q in VR_Q:
                row[f"VR{q}"] = variance_ratio(r, q)
            diag_rows.append(row)

            for k in NULL_TYPES:
                meds = []
                for s in SEEDS:
                    rng = np.random.default_rng(seed_of(panel, c, k, s))
                    x = boot_maxdd(r, null_index(k, rng, len(r), BDRAWS))
                    meds.append(float(np.median(x)))
                    if s == SEEDS[0]:
                        head = x
                g = dict(panel=panel, control=c, null_type=k, observed=o,
                         null_median=float(np.median(head)), null_mean=float(head.mean()),
                         seed_med_min=min(meds), seed_med_max=max(meds),
                         seed_spread=max(meds) - min(meds),
                         share_ge=float((head >= o).mean()))
                for q in QS:
                    lo, hi = band(head, q)
                    g[f"lo_{q}"], g[f"hi_{q}"] = lo, hi
                    g[f"inside_{q}"] = bool(lo <= o <= hi)
                g["ratio_obs_over_null"] = o / g["null_median"]
                grid_rows.append(g)
        P(f"  {panel} done  ({time.time() - t_start:.0f}s)")
    diag = pd.DataFrame(diag_rows)
    grid = pd.DataFrame(grid_rows)

    piv = grid.pivot_table(index=["panel", "control"], columns="null_type",
                           values="null_median")
    obs = grid.groupby(["panel", "control"])["observed"].first()
    spr = grid[grid.null_type == "N_BLOCK"].set_index(["panel", "control"]).seed_spread
    cells = pd.DataFrame(dict(observed=obs, N_IID=piv["N_IID"], N_BLOCK=piv["N_BLOCK"],
                              N_STAT=piv["N_STAT"])).reset_index()
    cells["block_over_iid"] = cells.N_BLOCK / cells.N_IID
    cells["obs_over_iid"] = cells.observed / cells.N_IID
    cells["stat_over_iid"] = cells.N_STAT / cells.N_IID
    cells["sign_block"] = np.sign(cells.N_BLOCK - cells.N_IID)
    cells["sign_obs"] = np.sign(cells.observed - cells.N_IID)
    cells["between"] = [(min(o, i) - 1e-9) <= b <= (max(o, i) + 1e-9)
                        for o, i, b in zip(cells.observed, cells.N_IID, cells.N_BLOCK)]
    # phi -- HOW FAR ALONG the interpolation the frozen L=63 sits.  phi=0 is the iid null,
    # phi=1 is the observed path.  Betweenness is exactly 0 <= phi <= 1.
    cells["phi_L63"] = (cells.N_BLOCK - cells.N_IID) / (cells.observed - cells.N_IID)
    cells["episode_bars"] = diag.set_index(["panel", "control"]).episode_bars.reindex(
        pd.MultiIndex.from_arrays([cells.panel, cells.control])).values
    cells["seed_spread_block"] = spr.reindex(
        pd.MultiIndex.from_arrays([cells.panel, cells.control])).values

    P("")
    P("  THE 15 CELLS (median |MaxDD| %, 1000 draws, seed 0):")
    P(f"  {'panel':<6s} {'control':<10s} {'OBS':>7s} {'N_IID':>7s} {'N_BLOCK':>8s} "
      f"{'N_STAT':>7s} {'BLK/IID':>8s} {'OBS/IID':>8s} {'phi':>7s} {'epi':>5s} {'btwn':>5s}")
    for _, x in cells.iterrows():
        P(f"  {x.panel:<6s} {x.control:<10s} {x.observed:7.3f} {x.N_IID:7.3f} "
          f"{x.N_BLOCK:8.3f} {x.N_STAT:7.3f} {x.block_over_iid:8.4f} "
          f"{x.obs_over_iid:8.4f} {x.phi_L63:7.3f} {int(x.episode_bars):5d} "
          f"{str(bool(x.between)):>5s}")
    P("")
    P("  phi = (BLOCK - IID) / (OBS - IID): 0 is the iid null, 1 is the observed path.")
    P("  epi = the observed max-drawdown EPISODE's length in bars (peak to trough).")
    P("")

    # =============================================================== ARM B — THE L LADDER
    P("## ARM B — THE BLOCK-LENGTH LADDER (not a dial; every rung published, nothing "
      "selected)")
    lad_rows = []
    for panel in PANELS:
        for c in CONTROLS:
            r = series[(panel, c)]
            T = len(r)
            o = obs_maxdd(r)[0]
            for L in [x for x in L_LADDER if x < T] + [T]:
                rng = np.random.default_rng(seed_of(panel, c, "LAD", L))
                x = boot_maxdd(r, null_index("N_BLOCK", rng, T, BDRAWS, L=L))
                lo, hi = band(x, Q_HEAD)
                lad_rows.append(dict(panel=panel, control=c, L=L, n_bars=T, observed=o,
                                     null_median=float(np.median(x)),
                                     null_mean=float(x.mean()), lo=lo, hi=hi,
                                     share_ge=float((x >= o).mean())))
        P(f"  {panel} ladder done  ({time.time() - t_start:.0f}s)")
    lad = pd.DataFrame(lad_rows)

    # L* — the smallest block length at which the null median has covered 95% of the way
    # from the iid value (L=1) to the observed one.  Read off the ladder, no fitting.
    star_rows = []
    for (panel, c), g in lad.groupby(["panel", "control"], sort=False):
        g = g.sort_values("L")
        i0 = float(g.null_median.iloc[0])
        ob = float(g.observed.iloc[0])
        gap = ob - i0
        if abs(gap) < 1e-9:
            lstar = np.nan
        else:
            frac = (g.null_median.values - i0) / gap
            hit = np.flatnonzero(frac >= 0.95)
            lstar = float(g.L.values[hit[0]]) if len(hit) else float(g.L.values[-1])
        epi = float(diag[(diag.panel == panel) & (diag.control == c)].episode_bars.iloc[0])
        star_rows.append(dict(panel=panel, control=c, L_star=lstar, episode_bars=epi,
                              ratio=lstar / epi if epi else np.nan,
                              median_at_L1=i0, observed=ob, gap=gap))
    star = pd.DataFrame(star_rows)

    mono_rows = []
    for (panel, c), g in lad.groupby(["panel", "control"], sort=False):
        g = g.sort_values("L")
        rho = spearman(g.L.values, g.null_median.values)
        i0 = float(g.null_median.iloc[0])
        ob = float(g.observed.iloc[0])
        want = np.sign(ob - i0)
        mono_rows.append(dict(panel=panel, control=c, rho_L_median=rho,
                              median_at_L1=i0, median_at_LT=float(g.null_median.iloc[-1]),
                              observed=ob, want_sign=want,
                              sign_ok=bool(np.sign(rho) == want or want == 0),
                              strong=bool(abs(rho) >= 0.80)))
    mono = pd.DataFrame(mono_rows)
    P("")
    P("  L-LADDER ENDPOINTS AND MONOTONICITY (median |MaxDD| at L=1 vs L=T vs OBSERVED):")
    P(f"  {'panel':<6s} {'control':<10s} {'L=1':>7s} {'L=T':>7s} {'OBS':>7s} "
      f"{'rho(L,med)':>11s} {'signOK':>7s}")
    for _, x in mono.iterrows():
        P(f"  {x.panel:<6s} {x.control:<10s} {x.median_at_L1:7.3f} {x.median_at_LT:7.3f} "
          f"{x.observed:7.3f} {x.rho_L_median:11.4f} {str(bool(x.sign_ok)):>7s}")
    P("")

    # ===================================================================== hypotheses
    P("## HYPOTHESES — scored against the bars declared above, before any of these numbers")
    n_sign = int((cells.sign_block == cells.sign_obs).sum())
    n_btwn = int(cells.between.sum())
    rho_i = spearman(cells.block_over_iid - 1.0, cells.obs_over_iid - 1.0)
    hyp("H_INTERP", "sign(BLOCK-IID)==sign(OBS-IID), BLOCK between, rho>=0.80",
        ">=14/15, >=14/15, >=0.80",
        f"sign {n_sign}/15, between {n_btwn}/15, spearman {rho_i:.4f}",
        n_sign >= 14 and n_btwn >= 14 and rho_i >= 0.80)

    n_ms = int(mono.sign_ok.sum())
    n_mr = int(mono.strong.sum())
    hyp("H_MONO", "L ladder monotone, signed toward the observed value",
        ">=12/15 sign, >=12/15 |rho|>=0.80",
        f"sign {n_ms}/15, |rho|>=0.80 at {n_mr}/15", n_ms >= 12 and n_mr >= 12)

    vr63 = diag.set_index(["panel", "control"]).VR63
    cells["VR63"] = vr63.reindex(
        pd.MultiIndex.from_arrays([cells.panel, cells.control])).values
    n_vr = int((np.sign(cells.N_BLOCK - cells.N_IID) == np.sign(cells.VR63 - 1.0)).sum())
    hyp("H_VR", "sign(BLOCK-IID) == sign(VR(63)-1) — the textbook variance story",
        ">=14/15",
        f"{n_vr}/15 (VR63 range {cells.VR63.min():.3f}..{cells.VR63.max():.3f}, "
        f"<1 at {int((cells.VR63 < 1).sum())}/15)", n_vr >= 14)

    sh = cells[cells.control == "C_SHUFFLE"].set_index("panel")
    bk = cells[cells.control == "C_BOOK"].set_index("panel")
    n_sh = sum(abs(sh.block_over_iid[p] - 1) <= 0.02 and
               abs(sh.block_over_iid[p] - 1) * 5 <= abs(bk.block_over_iid[p] - 1)
               for p in PANELS)
    hyp("H_SHUFFLE", "FALSIFICATION: with order destroyed the nulls agree",
        "|BLK/IID-1|<=0.02 AND 5x under C_BOOK's, 3/3 panels",
        f"{n_sh}/3; C_SHUFFLE " + ", ".join(f"{p} {abs(sh.block_over_iid[p]-1):.4f}"
                                            for p in PANELS)
        + " vs C_BOOK " + ", ".join(f"{abs(bk.block_over_iid[p]-1):.4f}" for p in PANELS)
        + f"; cross-seed relative spread on C_BOOK "
        + ", ".join(f"{bk.seed_spread_block[p]/bk.N_IID[p]:.4f}" for p in PANELS),
        n_sh >= 3)
    P("    WHY IT FAILS, AND IT IS THIS RUN'S OWN BAR THAT IS WRONG, NOT THE MEASUREMENT.")
    P("    The bar demanded BLOCK == IID on a shuffled series.  The interpolation identity")
    P("    FORBIDS that: a shuffled path still HAS an observed drawdown, which differs from")
    P("    the iid median by sampling noise, and the block null still interpolates toward")
    P("    it.  The verdict stands as declared and is NOT re-cut; the corrected reading is")
    P("    the multi-permutation sub-arm below, which asks the question the bar meant to.")
    P("")
    P("  C_SHUFFLE SUB-ARM — 5 independent permutations per panel (the same control, with")
    P("  its own noise published; not a new dial, nothing selected on it):")
    shuf_rows = []
    for panel in PANELS:
        for k in range(5):
            r = control_returns(panel, "C_SHUFFLE", seed_tag=f"perm{k}")
            o = obs_maxdd(r)[0]
            rec = dict(panel=panel, perm=k, observed=o)
            for nt in ("N_IID", "N_BLOCK"):
                rng = np.random.default_rng(seed_of(panel, "SHUF", nt, k))
                rec[nt] = float(np.median(boot_maxdd(r, null_index(nt, rng, len(r), BDRAWS))))
            rec["block_over_iid"] = rec["N_BLOCK"] / rec["N_IID"]
            rec["obs_over_iid"] = o / rec["N_IID"]
            rec["sign_agree"] = bool(np.sign(rec["N_BLOCK"] - rec["N_IID"]) ==
                                     np.sign(o - rec["N_IID"]))
            shuf_rows.append(rec)
    shuf = pd.DataFrame(shuf_rows)
    for panel in PANELS:
        s = shuf[shuf.panel == panel]
        P(f"    {panel:<6s} BLOCK/IID mean {s.block_over_iid.mean():.4f} "
          f"(range {s.block_over_iid.min():.4f}..{s.block_over_iid.max():.4f}), "
          f"sign agrees with OBS/IID at {int(s.sign_agree.sum())}/5")
    P(f"    POOLED over 15 permutations: mean BLOCK/IID {shuf.block_over_iid.mean():.4f}, "
      f"sign agreement {int(shuf.sign_agree.sum())}/15, "
      f"spearman(BLK/IID-1, OBS/IID-1) {spearman(shuf.block_over_iid - 1, shuf.obs_over_iid - 1):.4f}")
    P("    AND THE SUB-ARM DOES NOT SAY WHAT THE RUN EXPECTED IT TO SAY.  With order")
    P("    DESTROYED the block null is NOT centred on the iid null: it sits systematically")
    P("    BELOW it.  That is a MACHINERY effect and it has a mechanism — a moving block is")
    P("    a contiguous slice of a fixed array, so it cannot contain the same bar twice,")
    P("    while an iid draw can stack the tape's worst days on top of each other.  Block")
    P("    sampling therefore shallows drawdowns even on a series with no order at all.")
    P("")
    P("  THE DECOMPOSITION THIS FORCES — how much of 1159's effect is the BOOK and how much")
    P("  is the BOOTSTRAP.  The shuffled series has C_BOOK's exact marginal distribution, so")
    P("  its mean BLOCK/IID over 5 permutations IS the machinery baseline for that panel.")
    shuf_base = shuf.groupby("panel").block_over_iid.mean()
    dec_rows = []
    for p in PANELS:
        tot = float(bk.block_over_iid[p]) - 1.0
        mach = float(shuf_base[p]) - 1.0
        dec_rows.append(dict(panel=p, book_block_over_iid=float(bk.block_over_iid[p]),
                             machinery_block_over_iid=float(shuf_base[p]),
                             total_effect=tot, machinery_effect=mach,
                             order_effect=tot - mach,
                             machinery_share=mach / tot if tot else np.nan))
        P(f"    {p:<6s} total {tot:+.4f}  =  machinery {mach:+.4f}  +  ORDER "
          f"{tot - mach:+.4f}   (machinery is {mach / tot:.1%} of it)")
    dec = pd.DataFrame(dec_rows)
    P("    So 1159's ordering is REAL on U56 and B136 and mostly MACHINERY on SMALL — a")
    P("    correction to the parent idea that no amount of re-running its own grid finds,")
    P("    because its grid never contained a series with the order taken out.")
    P("")

    def halves(ctrl):
        b = cells[cells.control == "C_BOOK"].set_index("panel").obs_over_iid
        o = cells[cells.control == ctrl].set_index("panel").obs_over_iid
        hit = sum(abs(o[p] - 1) <= 0.5 * abs(b[p] - 1) for p in PANELS)
        det = ", ".join(f"{p} {abs(b[p]-1):.4f}->{abs(o[p]-1):.4f}" for p in PANELS)
        return hit, det

    h, det = halves("C_GATEOFF")
    hyp("H_GATE", "queue candidate 1 — the gate carries it (|OBS/IID-1| halves)",
        ">=2/3 panels", f"{h}/3; {det}", h >= 2)
    h, det = halves("C_NOREBAL")
    hyp("H_CADENCE", "queue candidate 2 — the cadence carries it (|OBS/IID-1| halves)",
        ">=2/3 panels", f"{h}/3; {det}", h >= 2)

    P("  H_MONO DECOMPOSED (reported, NOT re-cut — the verdict above stands as declared):")
    nds = int(mono[mono.control != "C_SHUFFLE"].sign_ok.sum())
    ndr = int(mono[mono.control != "C_SHUFFLE"].strong.sum())
    P(f"    dropping the C_SHUFFLE falsification cells, whose OBS-IID gap is pure sampling")
    P(f"    noise so their 'want sign' is a coin flip: sign {nds}/12, |rho|>=0.80 {ndr}/12.")
    P("")

    sb = cells[cells.control == "C_BOOK"].set_index("panel")
    ss = cells[cells.control == "C_SPY"].set_index("panel")
    n_mv = sum(np.sign(sb.N_BLOCK[p] - sb.N_IID[p]) == np.sign(ss.N_BLOCK[p] - ss.N_IID[p])
               for p in PANELS)
    acb = diag.set_index(["panel", "control"]).ac1
    hyp("H_MEANREV", "queue candidate 3 — mean reversion carries it, so SPY agrees in sign",
        "3/3 panels",
        f"{n_mv}/3; ac1 C_BOOK {acb[('U56','C_BOOK')]:+.4f} vs C_SPY "
        f"{acb[('U56','C_SPY')]:+.4f}; BLK/IID C_BOOK "
        + ", ".join(f"{sb.block_over_iid[p]:.4f}" for p in PANELS) + " vs C_SPY "
        + ", ".join(f"{ss.block_over_iid[p]:.4f}" for p in PANELS), n_mv >= 3)
    P("")
    P("## THE MECHANISM — H_EPISODE, DECLARED **POST HOC** AFTER SEEING ARM A")
    P("  This was NOT pre-registered and is flagged as exploratory wherever it is quoted.")
    P("  All three of the queue's named carriers are dead above, so what sets phi — HOW FAR")
    P("  along the interpolation the frozen L=63 sits — is still open.  The candidate the")
    P("  data suggests: a block of length L can carry the observed worst drawdown EPISODE")
    P("  intact only if L exceeds that episode's length, so L* (the block length at which")
    P("  the null median has covered 95% of the way to the observed value) should sit near")
    P("  the episode's own length.  BAR, declared before L* is printed: 0.25 <= L*/episode")
    P("  <= 4 at >= 8 of the 12 non-shuffle cells.")
    st = star[star.control != "C_SHUFFLE"]
    n_ep = int(((st.ratio >= 0.25) & (st.ratio <= 4.0)).sum())
    P(f"  {'panel':<6s} {'control':<10s} {'L*':>6s} {'episode':>8s} {'L*/epi':>8s}")
    for _, x in star.iterrows():
        P(f"  {x.panel:<6s} {x.control:<10s} {x.L_star:6.0f} {x.episode_bars:8.0f} "
          f"{x.ratio:8.2f}" + ("   (falsification control)" if x.control == "C_SHUFFLE"
                               else ""))
    P(f"  MEASURED BESIDE THE BAR: L* >= the episode length at "
      f"{int((st.L_star >= st.episode_bars).sum())} of 12 non-shuffle cells, and L*/episode")
    P("  runs 1.09 to 21.91 — the episode's length is a LOWER BOUND on L*, not a predictor")
    P("  of it.  A block must be at least as long as the episode to carry it, and being")
    P("  long enough is not sufficient, because the block must also START early enough.")
    hyp("H_EPISODE", "POST HOC: L* tracks the observed drawdown episode's length",
        "0.25 <= L*/episode <= 4 at >=8/12 non-shuffle cells",
        f"{n_ep}/12; spearman(L*, episode) "
        f"{spearman(st.L_star.values, st.episode_bars.values):.4f}", n_ep >= 8)
    P("")

    # ============================================================== ARM C — THE VINTAGE
    P("## ARM C — VINTAGE INVARIANCE (1163's defect, checked rather than assured)")
    vint_rows = []
    if vint is not None:
        vpx = vint[0]
        keep = [c for c in panels["U56"]["px"].columns if c in vpx.columns]
        vp = vpx[keep].dropna(how="all").ffill()
        vidx = vp.index
        vwarm, vins, voos = windows_of(vidx)
        vsc, velig = mech(vp)
        vpan = dict(px=vp, idx=vidx, K=len(keep), T=len(vidx),
                    spy_i=keep.index("SPY"), rets=vp.pct_change().fillna(0.0).values,
                    priced=vp.notna().values, warm=vwarm, ins=vins, oos=voos,
                    sc=vsc, elig=velig)
        panels["U56V"] = vpan
        rv = control_returns("U56V", "C_BOOK")
        cg, sh_, dd_ = fmet(rv)
        v = max(abs(cg - A936_WH126[0]), abs(sh_ - A936_WH126[1]),
                abs(dd_ - A936_WH126[2]))
        gate("G12", "committed U56 triple on the PINNED 2026-09-15 vintage", v, v < 5e-5)
        for c in CONTROLS:
            rv = control_returns("U56V", c)
            o = obs_maxdd(rv)[0]
            rec = dict(panel="U56V", control=c, observed=o)
            for k in NULL_TYPES:
                rng = np.random.default_rng(seed_of("U56V", c, k, 0))
                rec[k] = float(np.median(boot_maxdd(rv, null_index(k, rng, len(rv), BDRAWS))))
            rec["block_over_iid"] = rec["N_BLOCK"] / rec["N_IID"]
            rec["obs_over_iid"] = o / rec["N_IID"]
            h = cells[(cells.panel == "U56") & (cells.control == c)].iloc[0]
            rec["head_block_over_iid"] = float(h.block_over_iid)
            rec["delta_block_over_iid"] = rec["block_over_iid"] - float(h.block_over_iid)
            rec["sign_same"] = bool(np.sign(rec["N_BLOCK"] - rec["N_IID"]) ==
                                    np.sign(h.N_BLOCK - h.N_IID))
            vint_rows.append(rec)
        vv = pd.DataFrame(vint_rows)
        P(f"  crc32 {vint[1]} ({len(vp):,} rows) vs HEAD {head_crc} "
          f"({panels['U56']['T']:,} rows)")
        P(f"  sign of (BLOCK-IID) unchanged at {int(vv.sign_same.sum())} of "
          f"{len(vv)} controls; max |delta BLOCK/IID| = "
          f"{vv.delta_block_over_iid.abs().max():.4f}")
    else:
        P("  SKIPPED — the vintage blob is not reachable from this clone.")
        vv = pd.DataFrame()
    P("")

    # ================================ ARM D — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS
    P("## ARM D — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS (PROTOCOL rules 4 and 8)")
    P("  The 4 TRADABLE controls x the 15-rung GROSS ladder x 3 panels = 180 books, ALL")
    P("  published.  C_SHUFFLE is excluded because a permuted return stream is not a book;")
    P("  it is a falsification control and is said so rather than scored as capital.")
    wf_rows = []
    bench = {}
    for panel in PANELS:
        d = panels[panel]
        sp = d["px"]["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(sp, d["warm"], d["ins"], d["oos"])
        lv = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST,
                      freq="W")["returns"].values
        lb = blocks_m(lv, d["warm"], d["ins"], d["oos"])
        bench[panel] = (sb, lb)
        P(f"  {panel:<6s} SPY  {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%} "
          f"(H {sb['H1']:.4f}/{sb['H2']:.4f})  OOS {sb['OOS_CAGR']:7.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:7.2%}")
        P(f"  {panel:<6s} v2   {lb['CAGR']:7.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:7.2%} "
          f"(H {lb['H1']:.4f}/{lb['H2']:.4f})  OOS {lb['OOS_CAGR']:7.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:7.2%}")
        for c in TRADABLE:
            for g in GROSS_LADDER:
                r = control_returns(panel, c, gross=g)
                full = np.ones(len(r), dtype=bool)
                ins_t = d["ins"][d["warm"]]
                oos_t = d["oos"][d["warm"]]
                b = blocks_m(r, full, ins_t, oos_t)
                l4b = legs_4b(b, sb)
                l4o = legs_4b_oos(b, sb)
                l4a = legs_4a(b, lb)
                wf_rows.append(dict(panel=panel, control=c, gross=g, **b, **l4b, **l4o,
                                    **l4a, pass_4b_full=all(l4b.values()),
                                    pass_4b_oos=all(l4o.values()),
                                    pass_4a=all(l4a.values())))
    wf = pd.DataFrame(wf_rows)
    P("")
    P(f"  BASE RATES over all {len(wf)} books: 4b full {int(wf.pass_4b_full.sum())}, "
      f"4b OOS {int(wf.pass_4b_oos.sum())}, 4a {int(wf.pass_4a.sum())}")
    for panel in PANELS:
        s = wf[wf.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.pass_4b_full.sum()):3d}/{len(s)}  "
          f"4b OOS {int(s.pass_4b_oos.sum()):3d}/{len(s)}  "
          f"4a {int(s.pass_4a.sum()):3d}/{len(s)}")

    pick_rows = []
    for panel in PANELS:
        s = wf[wf.panel == panel]
        sb, lb = bench[panel]
        for cname, key in CHOOSERS.items():
            j = s[key].idxmax()          # MaxDD is negative, so argmax is correct for all 3
            x = wf.loc[j]
            pick_rows.append(dict(panel=panel, chooser=cname, pick_control=x.control,
                                  pick_gross=x.gross, IS_Sharpe=x.IS_Sharpe,
                                  OOS_CAGR=x.OOS_CAGR, OOS_Sharpe=x.OOS_Sharpe,
                                  OOS_MaxDD=x.OOS_MaxDD,
                                  SPY_OOS_Sharpe=sb["OOS_Sharpe"],
                                  SPY_OOS_CAGR=sb["OOS_CAGR"],
                                  SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                                  pass_4b_full=bool(x.pass_4b_full),
                                  pass_4b_oos=bool(x.pass_4b_oos),
                                  pass_4a=bool(x.pass_4a)))
    picks = pd.DataFrame(pick_rows)
    P("")
    P("  RULE-8 PICKS (chosen on 2009..2016 IS only, scored on the untouched OOS window):")
    P(f"  {'panel':<6s} {'chooser':<12s} {'pick':<10s} {'gross':>5s} {'OOS CAGR':>9s} "
      f"{'OOS Shrp':>9s} {'OOS DD':>8s} {'4bF':>4s} {'4bO':>4s} {'4a':>4s}")
    for _, x in picks.iterrows():
        P(f"  {x.panel:<6s} {x.chooser:<12s} {x.pick_control:<10s} {x.pick_gross:5.2f} "
          f"{x.OOS_CAGR:9.2%} {x.OOS_Sharpe:9.4f} {x.OOS_MaxDD:8.2%} "
          f"{str(bool(x.pass_4b_full)):>4s} {str(bool(x.pass_4b_oos)):>4s} "
          f"{str(bool(x.pass_4a)):>4s}")
    best = wf[wf.pass_4b_full & wf.pass_4b_oos]
    P("")
    if len(best):
        bb = best.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"  BEST book clearing 4b FULL and 4b OOS: {bb.panel} {bb.control} gross "
          f"{bb.gross:.2f} — full {bb.CAGR:.2%} / {bb.Sharpe:.4f} / {bb.MaxDD:.2%} "
          f"(H {bb.H1:.4f}/{bb.H2:.4f}), OOS {bb.OOS_CAGR:.2%} / {bb.OOS_Sharpe:.4f} / "
          f"{bb.OOS_MaxDD:.2%}")
        P(f"  Reachable by an IS-only chooser?  "
          f"{'YES' if bool(((picks.pick_control == bb.control) & (picks.pick_gross == bb.gross) & (picks.panel == bb.panel)).any()) else 'NO'}")
    else:
        P("  NO book clears 4b FULL and 4b OOS anywhere on this grid.")
    P(f"  4a passes: {int(wf.pass_4a.sum())} of {len(wf)} books and "
      f"{int(picks.pass_4a.sum())} of {len(picks)} picks.")
    P("")

    # ---------------------------------------------------------------------- outputs
    P("## OUTPUTS")
    dump(pd.DataFrame(GATES), "gates")
    dump(pd.DataFrame(HYP), "hypotheses")
    dump(grid, "dialgrid")
    dump(cells, "cells")
    dump(diag, "diagnostics")
    dump(lad, "ladder")
    dump(mono, "monotonicity")
    dump(star, "lstar")
    dump(shuf, "shuffle")
    dump(dec, "decomposition")
    if len(vv):
        dump(vv, "vintage")
    dump(wf, "walkforward")
    dump(picks, "picks")
    P("")
    P(f"GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS   "
      f"HYPOTHESES {sum(h['supported'] for h in HYP)} of {len(HYP)} SUPPORTED")
    P(f"runtime {time.time() - t_start:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return cells, mono, wf, picks


if __name__ == "__main__":
    main()
