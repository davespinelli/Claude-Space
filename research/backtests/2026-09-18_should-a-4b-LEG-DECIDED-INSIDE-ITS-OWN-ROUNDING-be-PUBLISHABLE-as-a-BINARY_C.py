#!/usr/bin/env python3
"""
Idea 1259 (lane C, 2026-09-18) — should a 4b LEG DECIDED INSIDE ITS OWN ROUNDING be
PUBLISHABLE as a BINARY?

THE PREMISE, READ FROM THE RECORD.  Idea 1257 found M12_1+M3/MEAN fails 4b's DD leg at
-0.2023392 against an exact cap of -0.2023034 — a margin of 3.58e-05 (0.0036pp) — while the
incumbent's own DD margin is 308x wider.  The record publishes every 4b leg as a BINARY
(PASS / FAIL) and counts those binaries in headlines ("4b 0 of 18", "14 passes collapse to
8").  A binary is only information if the quantity it thresholds is resolved at the bar.
1257 compared one margin against ANOTHER MARGIN, which says nothing about whether either is
measurable.  This run asks the question the record has never asked: WHAT IS A 4b LEG'S OWN
SAMPLING RESOLUTION ON THIS TAPE, and how many committed-style verdicts are decided inside it?

WHAT IS BEING MEASURED, STATED BEFORE ANY NUMBER IS READ.

  For a book b, a leg l and a window w, the MARGIN is the signed distance from the bar in the
  leg's own units:

    L_H1    M = Sharpe(b, first half of w)  - Sharpe(SPY, first half of w)
    L_H2    M = Sharpe(b, second half of w) - Sharpe(SPY, second half of w)
    L_CAGR  M = CAGR(b, w)                  - 0.70 * CAGR(SPY, w)
    L_DD    M = MaxDD(b, w)                 - 0.60 * MaxDD(SPY, w)     (both negative; a book
                                                                        passes when M >= 0)
    L_OOS   M = Sharpe(b, OOS) - Sharpe(SPY, OOS)                      (PROTOCOL rule 8's leg)

  PASS is M >= 0 (M > 0 for the three strict Sharpe legs, which is how the record writes them;
  the distinction moves nothing here and is reported).

  The RESOLUTION SD(M) is the sampling SD of that SAME margin under a CIRCULAR BLOCK BOOTSTRAP
  of the daily return rows (block length 63, the record's inherited L — idea 1241 found it
  never argued, idea 1250 found the [42,126] neighbourhood safe, so 63 is used and 42/126 are
  reported as a robustness reading, not as a dial).  The book and SPY are resampled with the
  SAME block draws, so SD(M) is the paired resolution of the comparison actually published,
  not the sum of two marginal noises.

  A verdict is DECIDED INSIDE ITS OWN ROUNDING at bar b iff  |M| < b * SD(M).

  PRE-DECLARED OUTCOMES, neither selected on:
    (A) THE BINARY IS SAFE      — the inside-share is < 0.25 at b = 1.0 on every leg.
    (B) THE BINARY IS UNSAFE    — the inside-share is >= 0.50 at b = 1.0 on some leg, i.e. a
                                  coin could flip that leg's published verdict.
    (C) LEG-DEPENDENT           — anything between; report the per-leg split and name which
                                  legs may be published as binaries and which may not.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  DIAL 1  VERDICT SET   {V_LAD, V_GRID}
          V_LAD  = the record's own four ladders around its anchor (N=20 / H=126 / GROSS=0.75
                   / CADENCE=W): N in 6 rungs, H in 4, GROSS in 10, CADENCE in 2.
          V_GRID = a two-axis N x H product grid at CADENCE=W, GROSS=0.75, which is NOT the
                   record's set and contains no degenerate GROSS axis (ideas 1189/1214/1224/
                   1236/1279 all found the GROSS ladder's own SE is ~0).
  DIAL 2  PRECISION BAR b   {1.0, 2.0} SD

  Every one of the 2 x 2 dial cells is published, on every panel and every leg, in
  `.census.csv` and `.dialcells.csv`.  No verdict is read at one cell only.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL663} (rule 9); the five legs; the
three windows (FULL / IS 2009-2016 / OOS 2017-2026); block length {42, 63, 126}; the
text-rounding reference bar.

FROZEN at the record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, decide-at-t / apply-at-t+1 (rule 2), warm-up 260 rows, cost 10 bps
(rule 2's rung — the cost ladder is NOT opened here, it is idea 1277's object).

THE CAPITAL ARM (PROTOCOL rule 8, OOS READ ONCE).  The census above is a measurement question.
The capital question the record actually needs answered is: DOES DECISIVENESS PAY?  Two
choosers see the SAME candidate books and the SAME in-sample window (warm-up..2016-12-31):

    CHOOSER_ANY  buys the highest-IS-Sharpe book that passes all four in-sample 4b legs.
    CHOOSER_DEC  buys the highest-IS-Sharpe book that passes all four in-sample 4b legs WITH
                 EVERY MARGIN >= b * SD(M) measured on the IS window only.

  Both fall back to the highest-IS-Sharpe book when their filter is empty (stated in advance,
  not chosen after).  2017-2026 is then read ONCE for both, against SPY (4b) and against the
  live RULES v2 book (4a).  d = DEC - ANY is the price of the decisiveness filter.  If d is
  indistinguishable from zero, a decisive 4b pass is a publishing property and not a capital
  one, and the honest verdict is KILL (capital) with a publishing recommendation.

PROTOCOL: rule 2 execution (10 bps, next-day); rule 4 both KEEP paths on every OOS row;
rule 8 walk-forward; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_should-a-4b-LEG-DECIDED-INSIDE-ITS-OWN-ROUNDING-be-PUBLISHABLE-as-a-BINARY_C.py
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "should-a-4b-LEG-DECIDED-INSIDE-ITS-OWN-ROUNDING-be-PUBLISHABLE-as-a-BINARY"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0                                  # PROTOCOL rule 2's rung; not a dial here
LEGS_MOM = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"      # the record's anchor
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED = 1259
B_REPS = 400
BLOCK_REF = 63                               # the record's inherited L (1241/1250)
BLOCKS = [42, 63, 126]                       # robustness, reported; not a dial
BARS = [1.0, 2.0]                            # DIAL 2
LEGNAMES = ["L_H1", "L_H2", "L_CAGR", "L_DD"]
LADDERS = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
GRID_N, GRID_H = [5, 10, 20, 40], [21, 63, 126]     # V_GRID's two axes
# The record's own printed precision, read off LEADERBOARD.md's row format
# (`{CAGR:.1%}` / `{Sharpe:.2f}` / `{MaxDD:.1%}`) and off the 4-dp Sharpes the prose uses.
TEXT_HALFWIDTH = {"L_H1": 0.005, "L_H2": 0.005, "L_CAGR": 0.0005, "L_DD": 0.0005}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"  GATE {name}: {'PASS' if ok else 'FAIL'}  value={value}  target={target}")
    return bool(ok)


# ============================================================ panels / books (the record's)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LADDERS["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def mech(q):
    parts = []
    for skip, look in LEGS_MOM:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def build1(pan, N, H, freq, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight."""
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, reb):
    """The record's fast runner: GROSS daily returns and one-way turnover at each row.  Costs
    are applied afterwards as r(c) = gross - turn * c / 1e4 (gate G1 checks this against
    engine.backtest)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1), turn


# ============================================================ metrics (scalar and vectorised)
def m_sharpe(r):
    r = np.asarray(r, float)
    if r.size < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def m_cagr(r):
    r = np.asarray(r, float)
    if r.size < 5:
        return np.nan
    return float(np.prod(1 + r) ** (252 / r.size) - 1)


def m_mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if e.size else np.nan


def v_sharpe(R):
    v = R.std(axis=1, ddof=0) * np.sqrt(252)
    out = np.full(R.shape[0], np.nan)
    ok = v > 0
    out[ok] = R[ok].mean(axis=1) * 252 / v[ok]
    return out


def v_cagr(R):
    return np.exp(np.log1p(R).sum(axis=1) * (252 / R.shape[1])) - 1


def v_mdd(R):
    e = np.cumprod(1 + R, axis=1)
    return (e / np.maximum.accumulate(e, axis=1) - 1).min(axis=1)


def legs_of(r, spy):
    """The four 4b margins of one return series against SPY over the same rows."""
    h = len(r) // 2
    return {
        "L_H1": m_sharpe(r[:h]) - m_sharpe(spy[:h]),
        "L_H2": m_sharpe(r[h:]) - m_sharpe(spy[h:]),
        "L_CAGR": m_cagr(r) - CAGR_FLOOR * m_cagr(spy),
        "L_DD": m_mdd(r) - DD_CAP * m_mdd(spy),
    }


def v_legs_of(R, S):
    """Vectorised legs_of over B bootstrap replicates: R and S are (B, T)."""
    h = R.shape[1] // 2
    return {
        "L_H1": v_sharpe(R[:, :h]) - v_sharpe(S[:, :h]),
        "L_H2": v_sharpe(R[:, h:]) - v_sharpe(S[:, h:]),
        "L_CAGR": v_cagr(R) - CAGR_FLOOR * v_cagr(S),
        "L_DD": v_mdd(R) - DD_CAP * v_mdd(S),
    }


def block_index(T, L, reps, rng):
    """Circular block bootstrap row index, (reps, T).  The SAME draw is reused for the book
    and for SPY, so every margin is a PAIRED resample."""
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, T, size=(reps, nb))
    off = np.arange(L)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(reps, nb * L)[:, :T]
    return idx % T


# ============================================================ book construction
def book_specs(verdict_set):
    """(key, N, H, gross, cadence) for a verdict set.  V_LAD is the record's four ladders
    around its anchor; V_GRID is an N x H product with no GROSS axis."""
    out = {}
    if verdict_set == "V_LAD":
        for n in LADDERS["N"]:
            out[f"N={n}"] = (n, A_H, A_G, A_C)
        for h in LADDERS["H"]:
            out[f"H={h}"] = (A_N, h, A_G, A_C)
        for g in LADDERS["GROSS"]:
            out[f"G={g:.2f}"] = (A_N, A_H, g, A_C)
        for c in LADDERS["CADENCE"]:
            out[f"C={c}"] = (A_N, A_H, A_G, c)
    else:
        for n in GRID_N:
            for h in GRID_H:
                out[f"N={n},H={h}"] = (n, h, A_G, A_C)
    return out


def all_books(pan):
    """Every distinct book in V_LAD U V_GRID as net daily returns at 10 bps, plus a map from
    each verdict set to its member keys."""
    specs = {}
    members = {}
    for vs in ("V_LAD", "V_GRID"):
        s = book_specs(vs)
        members[vs] = list(s.keys())
        specs.update({k: v for k, v in s.items()})
    frames = {}
    for (n, h, g, c) in set(specs.values()):
        frames.setdefault((n, h, c), None)
    for key in list(frames):
        frames[key] = build1(pan, key[0], key[1], key[2])
    rets, turns = {}, {}
    cache = {}
    for k, (n, h, g, c) in specs.items():
        rk = (n, h, g, c)
        if rk not in cache:
            gr, tu = nrun(pan, g * frames[(n, h, c)], pan.seg[c])
            cache[rk] = (gr - tu * COST / 1e4, tu)
        rets[k], turns[k] = cache[rk][0], cache[rk][1]
    return rets, turns, specs, members


# ============================================================ windows
def windows(pan):
    i0 = WARMUP
    ioos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
    ioos = max(ioos, i0 + 252)
    return {"FULL": (i0, len(pan.idx)), "IS": (i0, ioos), "OOS": (ioos, len(pan.idx))}


def resolution(pan, rets, win, L, reps, seed):
    """SD of every leg's margin for every book over `win`, paired block bootstrap."""
    a, b = win
    T = b - a
    rng = np.random.default_rng(seed)
    idx = block_index(T, L, reps, rng)
    S = pan.spy[a:b][idx]
    out = {}
    for k, r in rets.items():
        R = r[a:b][idx]
        lg = v_legs_of(R, S)
        out[k] = {ln: float(np.nanstd(lg[ln], ddof=1)) for ln in LEGNAMES}
    return out


# ============================================================ the record's text census
def text_census():
    """How the record actually PUBLISHES a 4b leg: does a committed 4b verdict ever state the
    margin that decided it?  Counts over LEADERBOARD.md + CHANGELOG.md.  This is a reading of
    committed text, reported as such; it moves no gate and decides no verdict."""
    rows = []
    pat_4b = re.compile(r"\b4b\b")
    pat_leg = re.compile(r"\bL_(H1|H2|CAGR|DD|OOS)\b")
    pat_margin = re.compile(r"\bmargin\b", re.I)
    pat_sd = re.compile(r"\b(SE|SD)\b")
    for fn in ("LEADERBOARD.md", "CHANGELOG.md"):
        p = ROOT / "research" / fn
        if not p.exists():
            continue
        txt = p.read_text(errors="replace")
        units = [u for u in txt.split("\n") if u.strip()]
        n4b = sum(1 for u in units if pat_4b.search(u))
        nleg = sum(1 for u in units if pat_leg.search(u))
        nmar = sum(1 for u in units if pat_4b.search(u) and pat_margin.search(u))
        nsd = sum(1 for u in units if pat_4b.search(u) and pat_sd.search(u))
        rows.append(dict(file=fn, bytes=p.stat().st_size, units=len(units), units_4b=n4b,
                         units_named_leg=nleg, units_4b_with_margin=nmar,
                         units_4b_with_SE_or_SD=nsd,
                         share_4b_with_margin=nmar / n4b if n4b else np.nan,
                         share_4b_with_SE=nsd / n4b if n4b else np.nan))
    return pd.DataFrame(rows)


# ============================================================ main
def main():
    t0 = time.time()
    say(f"# Idea 1259 (lane C, {DATE}) — is a 4b LEG decided inside its own ROUNDING?")
    say(f"# seed {SEED}, B {B_REPS}, block {BLOCK_REF} (robustness {BLOCKS}), cost {COST:.0f} bps")

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL663", pxS, inv)]
    say(f"\nPANELS: U56 {len(pxU.columns)-1} names ({pxU.index[0].date()}..{pxU.index[-1].date()}); "
        f"B136 {len(pxB.columns)-1} ({pxB.index[0].date()}..{pxB.index[-1].date()}); "
        f"SMALL663 {len(inv)} of {len(pxS.columns)-1} kept ({pxS.index[0].date()}..{pxS.index[-1].date()})")

    # ---- G1: the fast runner reproduces engine.backtest at the anchor rung
    p0 = panels[0]
    Wa = A_G * build1(p0, A_N, A_H, A_C)
    gr, tu = nrun(p0, Wa, p0.seg[A_C])
    fast = pd.Series(gr - tu * COST / 1e4, index=p0.idx)
    Wdf = pd.DataFrame(Wa, index=p0.idx, columns=p0.px.columns).shift(-1).fillna(0.0)
    eng = backtest(p0.px, Wdf, cost_bps=COST, freq=A_C)["returns"]
    d = float(np.nanmax(np.abs((fast - eng).iloc[WARMUP:].values)))
    gate("G1 fast runner == engine.backtest (anchor, U56)", f"{d:.3e}", "< 1e-10", d < 1e-10)

    census_rows, dial_rows, cap_rows, book_rows = [], [], [], []
    for pan in panels:
        say(f"\n=== {pan.name} ===")
        rets, turns, specs, members = all_books(pan)
        win = windows(pan)
        say(f"  books {len(rets)} distinct keys; windows "
            f"FULL {pan.idx[win['FULL'][0]].date()}..{pan.idx[-1].date()}, "
            f"IS ..{pan.idx[win['IS'][1]-1].date()}, OOS {pan.idx[win['OOS'][0]].date()}..")

        # ---------- ARM 1: the census, every leg x every book x every window x 3 block lengths
        for wname, w in win.items():
            a, b = w
            spy = pan.spy[a:b]
            obs = {k: legs_of(r[a:b], spy) for k, r in rets.items()}
            sds = {L: resolution(pan, rets, w, L, B_REPS, SEED + L) for L in BLOCKS}
            for k in rets:
                for ln in LEGNAMES:
                    M = obs[k][ln]
                    row = dict(panel=pan.name, window=wname, book=k, leg=ln, margin=M,
                               passes=bool(M >= 0),
                               text_halfwidth=TEXT_HALFWIDTH[ln])
                    for L in BLOCKS:
                        row[f"SD_L{L}"] = sds[L][k][ln]
                    sd = sds[BLOCK_REF][k][ln]
                    row["ratio"] = abs(M) / sd if sd > 0 else np.nan
                    for bar in BARS:
                        row[f"inside_b{bar:g}"] = bool(abs(M) < bar * sd)
                    row["inside_text"] = bool(abs(M) < TEXT_HALFWIDTH[ln])
                    census_rows.append(row)

        # ---------- book levels at the reference window, for the record
        for wname in ("FULL", "IS", "OOS"):
            a, b = win[wname]
            spy = pan.spy[a:b]
            for k, r in rets.items():
                book_rows.append(dict(panel=pan.name, window=wname, book=k,
                                      CAGR=m_cagr(r[a:b]), Sharpe=m_sharpe(r[a:b]),
                                      MaxDD=m_mdd(r[a:b]),
                                      turnover_yr=float(turns[k][a:b].sum() * 252 / (b - a)),
                                      SPY_CAGR=m_cagr(spy), SPY_Sharpe=m_sharpe(spy),
                                      SPY_MaxDD=m_mdd(spy)))

        # ---------- ARM 2: the capital arm (rule 8) — does DECISIVENESS pay?
        aI, bI = win["IS"]
        aO, bO = win["OOS"]
        spyI, spyO = pan.spy[aI:bI], pan.spy[aO:bO]
        obsI = {k: legs_of(r[aI:bI], spyI) for k, r in rets.items()}
        sdI = resolution(pan, rets, win["IS"], BLOCK_REF, B_REPS, SEED)
        shI = {k: m_sharpe(r[aI:bI]) for k, r in rets.items()}

        # live comparands, built on the same panel (4a's book and rule 3's SPY)
        v2 = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        v1 = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=COST, freq="W")["returns"].values

        for vs in ("V_LAD", "V_GRID"):
            keys = members[vs]
            best = max(keys, key=lambda k: (shI[k] if np.isfinite(shI[k]) else -9e9))
            passers = [k for k in keys if all(obsI[k][ln] >= 0 for ln in LEGNAMES)]
            pick_any = max(passers, key=lambda k: shI[k]) if passers else best
            for bar in BARS:
                dec = [k for k in passers
                       if all(obsI[k][ln] >= bar * sdI[k][ln] for ln in LEGNAMES)]
                pick_dec = max(dec, key=lambda k: shI[k]) if dec else best
                cells = {}
                for tag, pk in (("ANY", pick_any), ("DEC", pick_dec)):
                    r = rets[pk][aO:bO]
                    lg = legs_of(r, spyO)
                    cells[tag] = dict(
                        pick=pk, OOS_CAGR=m_cagr(r), OOS_Sharpe=m_sharpe(r), OOS_MaxDD=m_mdd(r),
                        L_H1=lg["L_H1"] > 0, L_H2=lg["L_H2"] > 0,
                        L_CAGR=lg["L_CAGR"] >= 0, L_DD=lg["L_DD"] >= 0,
                        m_H1=lg["L_H1"], m_H2=lg["L_H2"], m_CAGR=lg["L_CAGR"], m_DD=lg["L_DD"])
                v2o, v1o = v2[aO:bO], v1[aO:bO]
                for tag in ("ANY", "DEC"):
                    c = cells[tag]
                    r = rets[c["pick"]][aO:bO]
                    h = len(r) // 2
                    keep4b = c["L_H1"] and c["L_H2"] and c["L_CAGR"] and c["L_DD"]
                    keep4a = (m_sharpe(r[:h]) > m_sharpe(v2o[:h]) and
                              m_sharpe(r[h:]) > m_sharpe(v2o[h:]) and
                              m_mdd(r) >= m_mdd(v2o))
                    cap_rows.append(dict(
                        panel=pan.name, verdict_set=vs, bar=bar, chooser=tag, pick=c["pick"],
                        n_candidates=len(keys), n_IS_pass=len(passers),
                        n_IS_decisive=(len(dec) if tag == "DEC" else np.nan),
                        filter_empty=bool((tag == "ANY" and not passers) or
                                          (tag == "DEC" and not dec)),
                        IS_Sharpe=shI[c["pick"]],
                        OOS_CAGR=c["OOS_CAGR"], OOS_Sharpe=c["OOS_Sharpe"], OOS_MaxDD=c["OOS_MaxDD"],
                        SPY_OOS_CAGR=m_cagr(spyO), SPY_OOS_Sharpe=m_sharpe(spyO),
                        SPY_OOS_MaxDD=m_mdd(spyO),
                        V2_OOS_CAGR=m_cagr(v2o), V2_OOS_Sharpe=m_sharpe(v2o), V2_OOS_MaxDD=m_mdd(v2o),
                        V1_OOS_Sharpe=m_sharpe(v1o),
                        L_H1=c["L_H1"], L_H2=c["L_H2"], L_CAGR=c["L_CAGR"], L_DD=c["L_DD"],
                        m_H1=c["m_H1"], m_H2=c["m_H2"], m_CAGR=c["m_CAGR"], m_DD=c["m_DD"],
                        KEEP_4b=keep4b, KEEP_4a=keep4a))
                same = cells["ANY"]["pick"] == cells["DEC"]["pick"]
                dial_rows.append(dict(
                    panel=pan.name, verdict_set=vs, bar=bar,
                    n_candidates=len(keys), n_IS_pass=len(passers), n_IS_decisive=len(dec),
                    pick_ANY=cells["ANY"]["pick"], pick_DEC=cells["DEC"]["pick"], same_pick=same,
                    d_OOS_Sharpe=cells["DEC"]["OOS_Sharpe"] - cells["ANY"]["OOS_Sharpe"],
                    d_OOS_CAGR=cells["DEC"]["OOS_CAGR"] - cells["ANY"]["OOS_CAGR"],
                    d_OOS_MaxDD=cells["DEC"]["OOS_MaxDD"] - cells["ANY"]["OOS_MaxDD"]))

    cen = pd.DataFrame(census_rows)
    dia = pd.DataFrame(dial_rows)
    cap = pd.DataFrame(cap_rows)
    bks = pd.DataFrame(book_rows)
    txt = text_census()

    # ---- G2: the paired bootstrap's own SD is stable in the seed (a control)
    p0 = panels[0]
    r0, _, _, _ = all_books(p0)
    w0 = windows(p0)["FULL"]
    s_a = resolution(p0, r0, w0, BLOCK_REF, B_REPS, SEED)
    s_b = resolution(p0, r0, w0, BLOCK_REF, B_REPS, SEED + 7777)
    rel = [abs(s_a[k][ln] - s_b[k][ln]) / s_a[k][ln] for k in s_a for ln in LEGNAMES if s_a[k][ln] > 0]
    gate("G2 SD stable across rng streams (U56 FULL, median rel. move)",
         f"{np.median(rel):.4f}", "< 0.15", float(np.median(rel)) < 0.15)

    # ---- G3: a margin's SD is not zero anywhere (a zero would make the bar meaningless)
    z = int((cen[f"SD_L{BLOCK_REF}"] <= 0).sum())
    gate("G3 no degenerate (zero-SD) leg", z, "== 0", z == 0)

    # ================================================================== headline readings
    say("\n" + "=" * 78)
    say("ARM 1 — HOW MANY 4b VERDICTS ARE DECIDED INSIDE THEIR OWN RESOLUTION?")
    say("=" * 78)
    for vsname, keyset in (("V_LAD", set(book_specs("V_LAD"))), ("V_GRID", set(book_specs("V_GRID")))):
        sub = cen[cen.book.isin(keyset)]
        for bar in BARS:
            t = sub.groupby("leg")[f"inside_b{bar:g}"].mean()
            say(f"  {vsname} bar {bar:g} SD — inside-share by leg: " +
                ", ".join(f"{ln} {t[ln]:.3f}" for ln in LEGNAMES) +
                f"  | ALL {sub[f'inside_b{bar:g}'].mean():.3f}  (n={len(sub)})")
    say("")
    for wname in ("FULL", "IS", "OOS"):
        sub = cen[cen.window == wname]
        say(f"  window {wname:4s} bar 1 SD inside-share: " +
            ", ".join(f"{ln} {sub[sub.leg==ln]['inside_b1'].mean():.3f}" for ln in LEGNAMES) +
            f"  | median |M|/SD: " +
            ", ".join(f"{ln} {sub[sub.leg==ln]['ratio'].median():.2f}" for ln in LEGNAMES))
    say("")
    for pan in ("U56", "B136", "SMALL663"):
        sub = cen[cen.panel == pan]
        say(f"  panel {pan:9s} bar 1 SD inside-share {sub['inside_b1'].mean():.3f}, "
            f"bar 2 SD {sub['inside_b2'].mean():.3f}, median |M|/SD {sub['ratio'].median():.2f}")

    say("\n  THE RESOLUTION ITSELF (median SD of the margin, L=63, over all books/panels/windows):")
    for ln in LEGNAMES:
        s = cen[cen.leg == ln]
        u = "Sharpe" if ln in ("L_H1", "L_H2") else "fraction"
        say(f"    {ln:7s} median SD {s[f'SD_L{BLOCK_REF}'].median():.4f} {u}; "
            f"L=42 {s['SD_L42'].median():.4f}, L=126 {s['SD_L126'].median():.4f}; "
            f"the record PRINTS this leg to +/-{TEXT_HALFWIDTH[ln]:.4g} "
            f"({s[f'SD_L{BLOCK_REF}'].median()/TEXT_HALFWIDTH[ln]:.0f}x coarser than it measures)")

    say(f"\n  TEXT-ROUNDING reference: only {cen['inside_text'].mean():.4f} of verdicts are "
        f"inside the record's PRINTED precision, against {cen['inside_b1'].mean():.4f} inside "
        f"1 SD — the published digits are ~{cen[f'SD_L{BLOCK_REF}'].median()/np.mean(list(TEXT_HALFWIDTH.values())):.0f}x "
        f"finer than the tape resolves.")

    say("\n  THE RECORD'S OWN PUBLISHING HABIT (committed text, reported not gated):")
    for _, r in txt.iterrows():
        say(f"    {r['file']:15s} {r['bytes']/1e6:.2f} MB, {r['units_4b']} units mention 4b; "
            f"{r['units_4b_with_margin']} state a MARGIN ({r['share_4b_with_margin']:.4f}), "
            f"{r['units_4b_with_SE_or_SD']} state an SE/SD ({r['share_4b_with_SE']:.4f})")

    say("\n" + "=" * 78)
    say("ARM 2 — CAPITAL ARM (PROTOCOL rule 8, OOS 2017-2026 READ ONCE): DOES DECISIVENESS PAY?")
    say("=" * 78)
    say(dia.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    d = dia["d_OOS_Sharpe"].values
    n = len(d)
    se = float(np.std(d, ddof=1) / np.sqrt(n)) if n > 1 else np.nan
    say(f"\n  d(OOS Sharpe) DEC-ANY: mean {d.mean():+.4f}, SE {se:.4f}, "
        f"t {d.mean()/se if se else np.nan:+.2f}, n={n}; "
        f"picks differ in {int((~dia.same_pick).sum())} of {n} cells")
    say(f"  d(OOS CAGR)   mean {dia['d_OOS_CAGR'].mean():+.4f}; "
        f"d(OOS MaxDD) mean {dia['d_OOS_MaxDD'].mean():+.4f} "
        f"(negative = deeper drawdown; negative in {int((dia.d_OOS_MaxDD<0).sum())} of {n})")

    say("\n  EVERY OOS CHOOSER ROW, BOTH KEEP PATHS:")
    cols = ["panel", "verdict_set", "bar", "chooser", "pick", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "SPY_OOS_Sharpe", "V2_OOS_Sharpe", "L_H1", "L_H2", "L_CAGR", "L_DD",
            "KEEP_4b", "KEEP_4a"]
    say(cap[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  KEEP paths over {len(cap)} OOS chooser rows: 4b {int(cap.KEEP_4b.sum())}, "
        f"4a {int(cap.KEEP_4a.sum())}.  Binding leg counts (failures): " +
        ", ".join(f"{ln} {int((~cap[ln]).sum())}" for ln in LEGNAMES))
    s0 = cap.iloc[0]
    say(f"  SPY OOS {s0.SPY_OOS_CAGR:.2%} / {s0.SPY_OOS_Sharpe:.4f} / {s0.SPY_OOS_MaxDD:.2%} (U56 rows); "
        f"RULES v2 OOS {s0.V2_OOS_CAGR:.2%} / {s0.V2_OOS_Sharpe:.4f} / {s0.V2_OOS_MaxDD:.2%}; "
        f"RULES v1 OOS Sharpe {s0.V1_OOS_Sharpe:.4f}")

    # ---- the pre-declared outcome, read mechanically
    worst = cen.groupby("leg")["inside_b1"].mean()
    if worst.max() < 0.25:
        outcome = "(A) THE BINARY IS SAFE"
    elif worst.max() >= 0.50:
        outcome = "(B) THE BINARY IS UNSAFE"
    else:
        outcome = "(C) LEG-DEPENDENT"
    say(f"\n  PRE-DECLARED OUTCOME, read mechanically: {outcome} "
        f"(worst leg {worst.idxmax()} at {worst.max():.3f} inside 1 SD; "
        f"best leg {worst.idxmin()} at {worst.min():.3f})")

    OUT.with_suffix(".census.csv").write_text(cen.to_csv(index=False))
    OUT.with_suffix(".dialcells.csv").write_text(dia.to_csv(index=False))
    OUT.with_suffix(".capital.csv").write_text(cap.to_csv(index=False))
    OUT.with_suffix(".books.csv").write_text(bks.to_csv(index=False))
    OUT.with_suffix(".textcensus.csv").write_text(txt.to_csv(index=False))
    OUT.with_suffix(".gates.csv").write_text(pd.DataFrame(GATES).to_csv(index=False))
    say(f"\nwrote {OUT.name}.[census|dialcells|capital|books|textcensus|gates].csv  "
        f"({time.time()-t0:.0f}s)")
    OUT.with_suffix(".result.md").write_text("# Idea 1259 (lane C) — run log\n\n```\n" +
                                             "\n".join(LOG) + "\n```\n")


if __name__ == "__main__":
    main()
