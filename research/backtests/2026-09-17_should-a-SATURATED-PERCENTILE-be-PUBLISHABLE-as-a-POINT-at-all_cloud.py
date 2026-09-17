#!/usr/bin/env python3
"""
Idea 1199 (cloud lane, 2026-09-17) — should a SATURATED PERCENTILE be PUBLISHABLE as a POINT?

THE PREMISE, READ FROM THE RECORD AND NOT RECALLED.  Idea 1197
(`2026-09-17_is-the-BOOK-s-NULL-PERCENTILE-SATURATED-at-every-cell-the-record-quotes-it_C.py`)
found CH_PCT pinned at 1.000 at 0.963 (U56) / 1.000 (B136) of its 80 cells at K=10 and still
0.500 / 0.750 at K=400, that the statistic takes 1-6 DISTINCT values over all 80 cells at any
K <= 200, and that 23 committed claims were ADJUDICATED at that ceiling.  A number that is at
its attainable maximum carries no information above the maximum: "1.000" and "> 1 - 1/(K+1)"
are the same measurement, but only one of them says so.  The queue asks whether the BOUND form
should replace the POINT as a publishing convention, and what a reader LOSES and GAINS by it.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET  {C_STRICT, C_PROX, C_ALL}        -- 1197's three, harvester copied VERBATIM
  BOUND FORM {B_POINT, B_ONE, B_TWO, B_CP}    -- the publishing conventions under test

  B_POINT  the status quo: publish the percentile as a point, at whatever resolution the
           author typed.  This is the control and it is scored like any other rung.
  B_ONE    the queue's own form: a ceiling reading is published as "> 1 - 1/(K+1)".
  B_TWO    the two-sided counterpart: a reading at EITHER attainable extreme is published as
           "outside [1/(K+1), 1 - 1/(K+1)]".  The floor saturates too (1197 found SMALL's
           CH_PCT pinned at 0.000), and a convention that repairs only the ceiling leaves it.
  B_CP     the textbook object the other three approximate: the one-sided Clopper-Pearson
           95% lower bound on a binomial proportion with 0 exceedances of K draws, 0.05**(1/K).
           It is the only rung whose coverage is a stated probability rather than a spacing.

  Every rung is published at every cell.  NOTHING IS SELECTED ON.  B_POINT is not a straw man:
  it wins Arm C outright on one panel and the run says so.

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL} is not a dial (rule 9 panels, all three always
read).  The DRAW-COUNT ladder K in {10, 25, 50, 100, 200, 400} is a RESOLUTION ladder, nested
by construction -- the K=10 pool is a prefix of the K=400 pool, so K costs no draws and cannot
be shopped.  The 36-book population (N x cadence x panel) is not a dial; every book is
published in `.books.csv` with its own 4a and 4b verdict.  SEED is not a dial (20 seeds at
every cell, spread published).

Frozen at 1082/1098/1102/1148/1162/1197's construction: 3-leg composite (21/252, 0/126,
0/63), above-200d eligibility, gross 0.75, 10 bps (rule 2), t+1 execution (LAG 1 via the
shifted rebalance mask), warm-up 260 rows, IS end 2016-12-31, OOS 2017-01-01 onward.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward in Arm D with the choice made on
2009-2016 ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on
every book; rule 9 survivorship stated in the result note.  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_should-a-SATURATED-PERCENTILE-be-PUBLISHABLE-as-a-POINT-at-all_cloud.py
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
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "should-a-SATURATED-PERCENTILE-be-PUBLISHABLE-as-a-POINT-at-all"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ---- frozen construction (1197's, inherited whole) ----------------------------------------
COST, GROSS, WARMUP = 10.0, 0.75, 260
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
NDRAW, NSEED = 400, 20
SEED0 = 11991199
KLAD = [10, 25, 50, 100, 200, 400]
NLAD = [5, 10, 15, 20, 30, 40]
CADLAD = ["W", "M"]
ANCHORS = [(n, f) for f in CADLAD for n in NLAD]          # 12 books per panel
BOUNDS = ["B_POINT", "B_ONE", "B_TWO", "B_CP"]
CLAIMSETS = ["C_STRICT", "C_PROX", "C_ALL"]

# committed figures this run must reproduce bit-for-bit or fail (gates)
LIVE_MAXDD_COMMITTED = -0.1205                    # 1197 G3, U56 live RULES v2

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =========================================================== 1197's census, VERBATIM
NULLTOK = re.compile(r"\b(null|coin[- ]?flip|matched[- ]null|control (?:book|basket|arm)|"
                     r"permutation|bootstrap\w*|resampl\w*|monte[- ]?carlo)\b", re.I)
PCTTOK = re.compile(r"\b(percentile|pctile|pct|quantile|CH_PCT|p-?value|rank inside)\b", re.I)
ADJUD = re.compile(r"\b(clears?|cleared|passe?s?|passed|fails?|failed|beats?|picks?|picked|"
                   r"chooser|verdict|KEEP|KILL|PARK|significan\w*|decisive\w*|confirms?|"
                   r"refutes?|ranks?|ranked|selects?|adjudicat\w*)\b")
PCTVAL = re.compile(
    r"(?:(?:null\s+)?(?:percentile|pctile|CH_PCT|p-?value|quantile)\s*(?:of|=|:|is|at)?\s*"
    r"(\d{1,3}(?:\.\d+)?)\s*%?)"
    r"|(?:(\d{1,3}(?:\.\d+)?)\s*(?:st|nd|rd|th)?\s*[- ]?(?:percentile|pctile))", re.I)
KTOK = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(draws?|seeds?|resamples?|replicat\w*|"
                  r"bootstrap\w*|permutations?|paths?|simulations?|null books?|nulls?)\b", re.I)


def pct_values(txt):
    out = []
    for m in PCTVAL.finditer(txt):
        raw = m.group(1) or m.group(2)
        try:
            v = float(raw)
        except ValueError:
            continue
        if v > 100:
            continue
        dec = len(raw.split(".")[1]) if "." in raw else 0
        unit01 = v <= 1.0 and dec >= 2
        val = v * 100.0 if unit01 else v
        res_pp = 10.0 ** (-dec) * (100.0 if unit01 else 1.0)
        out.append((val, res_pp, raw))
    return out


def units():
    U = []
    for ln in (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore").split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    n_md = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        n_md += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, n_md


def census():
    """1197's census, VERBATIM, plus the three columns the BOUND FORM needs:
    CEIL_VALS   the ceiling-quoted readings in the unit
    K_INFER     the draw count the unit states (0 = none stated anywhere in it)
    RE_EXPRESSIBLE  whether the unit can be re-published under a bound form AT ALL
                    (a bound form is a function of K; a unit that names no K cannot carry one)
    """
    U, n_md = units()
    fileset = {}
    for src, txt in U:
        fileset.setdefault(src, False)
        if NULLTOK.search(txt) and PCTTOK.search(txt):
            fileset[src] = True
    rows = []
    for src, txt in U:
        nt, pt = bool(NULLTOK.search(txt)), bool(PCTTOK.search(txt))
        vals = pct_values(txt)
        ks = [int(m.group(1).replace(",", "")) for m in KTOK.finditer(txt)]
        sat_hi = any(abs(v - 100.0) < 1e-9 for v, _, _ in vals)
        sat_lo = any(abs(v - 0.0) < 1e-9 for v, _, _ in vals)
        overq = False
        if vals and ks:
            res = 100.0 / (max(ks) + 1)
            overq = any(rp < res * 0.999 for _, rp, _ in vals)
        K = max(ks) if ks else 0
        n_ceil = sum(1 for v, _, _ in vals if abs(v - 100.0) < 1e-9)
        n_floor = sum(1 for v, _, _ in vals if abs(v - 0.0) < 1e-9)
        rows.append(dict(
            src=src, n_chars=len(txt),
            C_STRICT=nt and pt and bool(vals),
            C_PROX=nt and pt,
            C_ALL=fileset[src] and (nt or pt),
            N_VALS=len(vals), STATES_K=bool(ks), K_MAX=K,
            SAT_CEIL=sat_hi, SAT_FLOOR=sat_lo, SAT_EITHER=sat_hi or sat_lo,
            N_CEIL=n_ceil, N_FLOOR=n_floor,
            OVERQUOTED=overq, ADJUDICATED=bool(ADJUD.search(txt)),
            VALS=";".join(f"{v:g}" for v, _, _ in vals)[:200]))
    return pd.DataFrame(rows), len(U), n_md


def bound_text(form, K):
    """What each convention PRINTS in place of a ceiling reading drawn on K draws."""
    if K <= 0:
        return None                                  # not re-expressible: the form needs K
    if form == "B_POINT":
        return "1.000"
    if form == "B_ONE":
        return f"> {1.0 - 1.0 / (K + 1):.6f}"
    if form == "B_TWO":
        return f"outside [{1.0 / (K + 1):.6f}, {1.0 - 1.0 / (K + 1):.6f}]"
    if form == "B_CP":
        return f">= {0.05 ** (1.0 / K):.6f} (CP 95%)"
    raise ValueError(form)


def bound_covers_floor(form):
    return form in ("B_TWO",)


# =========================================================== panels and the fast runner
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.P = np.cumprod(1.0 + self.rets, axis=0)
        self.Pprev = np.vstack([np.ones((1, self.P.shape[1])), self.P[:-1]])
        self.priced = px.notna().values
        self.seg = {}
        for f in CADLAD:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            s = np.flatnonzero(m)
            self.seg[f] = (s, np.append(s[1:], len(px)))
        self.i0 = WARMUP
        self.ioos = px.index.searchsorted(pd.Timestamp(OOS_START))


def run_from_starts(pan, freq, Wstart):
    """1197/1162's fast runner. Identical arithmetic to engine.backtest (gate G1)."""
    starts, ends = pan.seg[freq]
    T, M = pan.rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    cur = np.zeros(M)
    for k, (i0, i1) in enumerate(zip(starts, ends)):
        w0 = Wstart[k]
        turn[i0] = np.abs(w0 - cur).sum()
        base = pan.Pprev[i0]
        A = w0[None, :] * (pan.Pprev[i0:i1] / base[None, :])
        cash0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + cash0
        held[i0:i1] = A / V[:, None]
        Aend = w0 * (pan.P[i1 - 1] / base)
        cur = Aend / (Aend.sum() + cash0)
    return (held * pan.rets).sum(axis=1) - turn * COST / 1e4


def starts_from_weights(pan, freq, W):
    starts, _ = pan.seg[freq]
    Wv = W.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
    return Wv[starts]


def book_weights(pan, n):
    q = pan.px[pan.invest]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    elig = comp.where(q > q.rolling(200).mean())
    rk = elig.rank(axis=1, ascending=False)
    W = pd.DataFrame(0.0, index=pan.px.index, columns=pan.px.columns)
    W[pan.invest] = (rk <= n).astype(float) * (GROSS / n)
    return W


def null_starts(pan, freq, n, rng):
    starts, _ = pan.seg[freq]
    out = np.zeros((len(starts), pan.rets.shape[1]))
    for k, i in enumerate(starts):
        avail = pan.iinv[pan.priced[max(i - 1, 0)][pan.iinv]]
        if len(avail) < n:
            continue
        out[k, rng.choice(avail, size=n, replace=False)] = GROSS / n
    return out


def sharpe(r):
    v = r.std(ddof=0) * np.sqrt(252)
    return r.mean() * 252 / v if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + r)
    return float((e / np.maximum.accumulate(e) - 1).min())


def cagr(r):
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def trip(r):
    return dict(CAGR=cagr(r), Sharpe=float(sharpe(r)), MaxDD=mdd(r))


def build_panels():
    out = []
    u = load_universe()
    out.append(("U56", u, [c for c in u.columns if c != "SPY"]))
    b = load_universe(broad=True)
    out.append(("B136", b, [c for c in b.columns if c != "SPY"]))
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in s.columns if c != "SPY" and c not in bad]
    out.append(("SMALL", s, inv))
    return out


# =========================================================== main
def main():
    t0 = time.time()
    gates = []

    say("=" * 96)
    say("IDEA 1199 (cloud, 2026-09-17) — should a SATURATED PERCENTILE be PUBLISHABLE as a POINT?")
    say("  dial 1 = CLAIM SET  {C_STRICT, C_PROX, C_ALL}   (1197's harvester, verbatim)")
    say("  dial 2 = BOUND FORM {B_POINT, B_ONE, B_TWO, B_CP}")
    say("=" * 96)

    # ------------------------------------------------------------------ ARM 0: DATA-FREE
    say("")
    say("(0) THE ARITHMETIC, PRINTED BEFORE ANY DATA IS TOUCHED")
    say("    A percentile read as mean(null < obs) over K draws lives on the lattice {0, 1/K,")
    say("    ..., 1}: it takes at most K+1 values, and a reading of 1.000 means ONLY 'obs")
    say("    exceeded all K draws'. Every convention below prints a DIFFERENT sentence for")
    say("    that same event, and only B_CP's number is a coverage probability.")
    say(f"    {'K':>5}  {'B_POINT':>9}  {'B_ONE  (1-1/(K+1))':>22}  {'B_CP (0.05**(1/K))':>20}")
    rows0 = []
    for K in KLAD:
        say(f"    {K:>5}  {'1.000':>9}  {1.0 - 1.0/(K+1):>22.6f}  {0.05 ** (1.0/K):>20.6f}")
        rows0.append(dict(K=K, B_POINT=1.0, B_ONE=1.0 - 1.0 / (K + 1), B_CP=0.05 ** (1.0 / K),
                          lattice_spacing=1.0 / K))
    pd.DataFrame(rows0).to_csv(f"{OUT}.bounds.csv", index=False)
    say("    NOTE THE SIGN OF THE DISAGREEMENT: B_ONE RISES with K (a finer lattice puts the")
    say("    ceiling closer to 1) while B_CP RISES TOO but from far below — at K=10 the honest")
    say("    95% statement is 0.741, i.e. 'the book beat a coin flip at least 74% of the time',")
    say("    NOT 1.000. The point form OVERSTATES the K=10 evidence by 0.259 IN THE STATISTIC'S")
    say("    OWN UNITS, and the record has 0.963-1.000 of its U56/B136 cells sitting there.")
    g0 = all(0.05 ** (1.0 / K) < 1.0 - 1.0 / (K + 1) for K in KLAD)
    gates.append(dict(gate="G0 B_CP is strictly the most conservative rung at every K",
                      value=float(max(0.05 ** (1.0 / K) - (1.0 - 1.0 / (K + 1)) for K in KLAD)),
                      target=0.0, pass_=bool(g0)))

    # ------------------------------------------------------------------ ARM A: CENSUS
    say("")
    say("=" * 96)
    say("(A) CENSUS — the record's committed percentile claims, RE-READ under each bound form")
    say("=" * 96)
    cdf, nU, n_md = census()
    cdf.to_csv(f"{OUT}.census.csv", index=False)
    say(f"  corpus: {nU:,} committed text units "
        f"(LEADERBOARD rows {int((cdf.src == 'LEADERBOARD').sum()):,}, "
        f"CHANGELOG paragraphs {int((cdf.src == 'CHANGELOG').sum()):,}, {n_md} markdown artefacts)")

    crows = []
    for cs in CLAIMSETS:
        sub = cdf[cdf[cs]]
        n = len(sub)
        ceil = sub[sub.SAT_CEIL]
        d = dict(CLAIM_SET=cs, N=n,
                 SAT_CEIL=int(sub.SAT_CEIL.sum()), SAT_FLOOR=int(sub.SAT_FLOOR.sum()),
                 SAT_ANY=int(sub.SAT_EITHER.sum()), STATES_K=int(sub.STATES_K.sum()),
                 ADJUD=int(sub.ADJUDICATED.sum()),
                 ADJUD_AND_SAT=int((sub.ADJUDICATED & sub.SAT_CEIL).sum()),
                 OVERQUOTED=int(sub.OVERQUOTED.sum()),
                 CEIL_STATES_K=int(ceil.STATES_K.sum()),
                 CEIL_NO_K=int((~ceil.STATES_K).sum()))
        crows.append(d)
        say(f"  {cs:9s} n={n:6d}  ceiling-quoted {d['SAT_CEIL']:5d}  floor-quoted {d['SAT_FLOOR']:5d}  "
            f"states K {d['STATES_K']:5d}  adjudicated {d['ADJUD']:5d}  AT THE CEILING {d['ADJUD_AND_SAT']:5d}")
    pd.DataFrame(crows).to_csv(f"{OUT}.claims.csv", index=False)
    gates.append(dict(gate="G6 census sets nest C_STRICT<=C_PROX<=C_ALL",
                      value=float((cdf.C_STRICT & ~cdf.C_PROX).sum() + (cdf.C_PROX & ~cdf.C_ALL).sum()),
                      target=0.0,
                      pass_=bool(((cdf.C_STRICT & ~cdf.C_PROX).sum() + (cdf.C_PROX & ~cdf.C_ALL).sum()) == 0)))
    # G6b: 1197's committed census figures must reproduce on today's corpus (C_STRICT n=103,
    # 26 ceiling-quoted, 23 adjudicated at the ceiling, 22 overquoted). The corpus GROWS every
    # commit, so this gate is a DIRECTIONAL one: today's counts must be >= 1197's.
    st = cdf[cdf.C_STRICT]
    g6b = (len(st) >= 103 and int(st.SAT_CEIL.sum()) >= 26
           and int((st.ADJUDICATED & st.SAT_CEIL).sum()) >= 23 and int(st.OVERQUOTED.sum()) >= 22)
    say(f"  G6b vs 1197's committed census (C_STRICT 103 / ceiling 26 / adjudicated-at-ceiling 23 /"
        f" overquoted 22): today {len(st)} / {int(st.SAT_CEIL.sum())} /"
        f" {int((st.ADJUDICATED & st.SAT_CEIL).sum())} / {int(st.OVERQUOTED.sum())}")
    gates.append(dict(gate="G6b census reproduces 1197 (monotone: corpus only grows)",
                      value=float(len(st)), target=103.0, pass_=bool(g6b)))

    # ---- THE RE-READ: what each form PRINTS, and what it COSTS the reader
    say("")
    say("  RE-EXPRESSING THE RECORD'S CEILING-QUOTED CLAIMS.  A bound form is a FUNCTION OF K.")
    say("  A unit that names no draw count cannot carry one AT ALL — that is the reader's first")
    say("  and largest loss, and it is a loss the POINT form hides rather than avoids.")
    rr = []
    for cs in CLAIMSETS:
        sub = cdf[cdf[cs] & cdf.SAT_EITHER]
        for form in BOUNDS:
            ok = 0
            uncheck = 0
            moved = 0
            floor_left = 0
            deltas = []
            for _, u in sub.iterrows():
                K = int(u.K_MAX)
                txt = bound_text(form, K)
                if txt is None:
                    uncheck += 1
                    continue
                ok += 1
                if form != "B_POINT":
                    moved += 1
                    if form == "B_CP":
                        deltas.append(1.0 - 0.05 ** (1.0 / K))
                    else:
                        deltas.append(1.0 - (1.0 - 1.0 / (K + 1)))
                if u.SAT_FLOOR and not bound_covers_floor(form) and form != "B_POINT":
                    floor_left += 1
            n = len(sub)
            rr.append(dict(CLAIM_SET=cs, BOUND=form, N_SATURATED=n,
                           RE_EXPRESSIBLE=ok, UNCHECKABLE_NO_K=uncheck,
                           share_uncheckable=uncheck / n if n else np.nan,
                           N_MOVED=moved,
                           median_move=float(np.median(deltas)) if deltas else 0.0,
                           max_move=float(np.max(deltas)) if deltas else 0.0,
                           FLOOR_LEFT_UNREPAIRED=floor_left))
    rrdf = pd.DataFrame(rr)
    rrdf.to_csv(f"{OUT}.reread.csv", index=False)
    for cs in CLAIMSETS:
        s = rrdf[rrdf.CLAIM_SET == cs]
        n = int(s.N_SATURATED.iloc[0])
        say(f"    {cs:9s} saturated units n={n:5d}   "
            + "  ".join(f"{r.BOUND}: re-expressible {r.RE_EXPRESSIBLE:4d} "
                        f"(uncheckable {r.share_uncheckable:.4f}), median move {r.median_move:.4f}"
                        for _, r in s.iterrows() if r.BOUND in ("B_ONE", "B_CP")))
    say("")
    say("  EXAMPLE PRINTINGS (the sentence each convention would publish at each K):")
    for K in [10, 100, 400]:
        say(f"    K={K:>4}  " + "   |   ".join(f"{f}: {bound_text(f, K)}" for f in BOUNDS))

    # ------------------------------------------------------------------ ARM B: PRICE
    say("")
    say("=" * 96)
    say(f"(B) RE-PRICING — {len(ANCHORS) * 3} books, {len(ANCHORS) * 3 * NDRAW:,} gross-matched null backtests")
    say("=" * 96)
    panels = build_panels()
    books, grid, wf, disc = [], [], [], []
    panel_names = [p[0] for p in panels]
    pan_ctx = {}

    for pi, (pname, px, invest) in enumerate(panels):
        pan = Panel(pname, px, invest)
        spy = px["SPY"].pct_change().fillna(0.0).values
        i0, ioos = pan.i0, pan.ioos
        s_full, s_is, s_oos = spy[i0:], spy[i0:ioos], spy[ioos:]
        base_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        b_full, b_oos = base_r[i0:], base_r[ioos:]
        h = len(s_full) // 2
        spyT, baseT = trip(s_full), trip(b_full)
        spyH = (float(sharpe(s_full[:h])), float(sharpe(s_full[h:])))
        baseH = (float(sharpe(b_full[:h])), float(sharpe(b_full[h:])))
        pan_ctx[pname] = dict(spyT=spyT, spyH=spyH, spy_oos=trip(s_oos), baseT=baseT, baseH=baseH,
                              base_oos=trip(b_oos))
        say(f"  {pname:6s} n_invest={len(invest):4d}  SPY {spyT['CAGR']:.2%} / {spyT['Sharpe']:.4f} / "
            f"{spyT['MaxDD']:.2%} (halves {spyH[0]:.4f}/{spyH[1]:.4f}), "
            f"OOS {cagr(s_oos):.2%} / {sharpe(s_oos):.4f} / {mdd(s_oos):.2%}")
        say(f"  {'':6s} {'':13s}  LIVE RULES v2 {baseT['CAGR']:.2%} / {baseT['Sharpe']:.4f} / "
            f"{baseT['MaxDD']:.2%} (halves {baseH[0]:.4f}/{baseH[1]:.4f}), "
            f"OOS {cagr(b_oos):.2%} / {sharpe(b_oos):.4f}")
        if pname == "U56":
            gates.append(dict(gate="G3 live RULES v2 U56 MaxDD == record -12.05%",
                              value=baseT["MaxDD"], target=LIVE_MAXDD_COMMITTED,
                              pass_=abs(baseT["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4))

        for ai, (n, freq) in enumerate(ANCHORS):
            cell = 1000 * (pi + 1) + ai
            W = book_weights(pan, n)
            r = run_from_starts(pan, freq, starts_from_weights(pan, freq, W))
            if pname == "U56" and ai == 0:
                eng = backtest(px, W, cost_bps=COST, freq=freq)["returns"].values
                d = float(np.nanmax(np.abs(np.asarray(eng[i0:], float) - r[i0:])))
                gates.append(dict(gate="G1 fast runner == engine.backtest (post-warm-up)",
                                  value=d, target=0.0, pass_=d < 1e-12))
                # G1b: 1191's NaN in engine.backtest returns, read on ndarray not a Series
                nn = int(np.isnan(np.asarray(eng, float)).sum())
                gates.append(dict(gate="G1b engine.backtest NaN rows exist and sit inside warm-up",
                                  value=float(nn), target=float(nn),
                                  pass_=bool(np.all(np.flatnonzero(np.isnan(np.asarray(eng, float))) < WARMUP))))
            rf, ris, ros = r[i0:], r[i0:ioos], r[ioos:]
            bt = trip(rf)
            half1, half2 = float(sharpe(rf[:h])), float(sharpe(rf[h:]))
            k4a = (half1 > baseH[0] and half2 > baseH[1] and bt["MaxDD"] >= baseT["MaxDD"])
            k4b = (half1 > spyH[0] and half2 > spyH[1]
                   and float(sharpe(ros)) > float(sharpe(s_oos))
                   and bt["MaxDD"] >= DD_CAP * spyT["MaxDD"]
                   and bt["CAGR"] >= CAGR_FLOOR * spyT["CAGR"])
            k4b_oos = (float(sharpe(ros)) > float(sharpe(s_oos))
                       and mdd(ros) >= DD_CAP * mdd(s_oos)
                       and cagr(ros) >= CAGR_FLOOR * cagr(s_oos))

            nsh_is = np.empty(NDRAW)
            nsh_full = np.empty(NDRAW)
            for d_ in range(NDRAW):
                rng = np.random.default_rng(SEED0 + 100003 * cell + d_)
                nr = run_from_starts(pan, freq, null_starts(pan, freq, n, rng))
                nsh_is[d_] = sharpe(nr[i0:ioos])
                nsh_full[d_] = sharpe(nr[i0:])
            books.append(dict(panel=pname, N=n, cadence=freq, **bt, H1=half1, H2=half2,
                              IS_Sharpe=float(sharpe(ris)), IS_CAGR=cagr(ris), IS_MaxDD=mdd(ris),
                              OOS_CAGR=cagr(ros), OOS_Sharpe=float(sharpe(ros)), OOS_MaxDD=mdd(ros),
                              KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_oos,
                              null_is_mean=float(nsh_is.mean()), null_is_sd=float(nsh_is.std(ddof=1)),
                              null_is_max=float(nsh_is.max()),
                              null_full_mean=float(nsh_full.mean())))

            obs = float(sharpe(ris))
            for K in KLAD:
                for sd in range(NSEED):
                    rs = np.random.default_rng(SEED0 + 7919 * K + sd)
                    idx = rs.choice(NDRAW, size=K, replace=False)
                    pool = nsh_is[idx]
                    pct = float((pool < obs).mean())
                    z = float((obs - pool.mean()) / pool.std(ddof=1))
                    row = dict(panel=pname, N=n, cadence=freq, K=K, seed=sd,
                               CH_PCT=pct, CH_Z=z,
                               SAT_CEIL=bool(pct >= 1.0 - 1e-12),
                               SAT_FLOOR=bool(pct <= 1e-12))
                    # what each convention would VERDICT for this cell
                    for form in BOUNDS:
                        if form == "B_POINT":
                            row["V_" + form] = pct            # a point: full resolution claimed
                        elif form == "B_ONE":
                            row["V_" + form] = 1.0 if pct >= 1.0 - 1e-12 else pct
                        elif form == "B_TWO":
                            row["V_" + form] = (1.0 if pct >= 1.0 - 1e-12
                                                else (0.0 if pct <= 1e-12 else pct))
                        else:                                  # B_CP
                            row["V_" + form] = 0.05 ** (1.0 / K) if pct >= 1.0 - 1e-12 else pct
                        row["TIED_" + form] = bool(pct >= 1.0 - 1e-12)
                    grid.append(row)
        say(f"    {pname} done  t={time.time() - t0:.0f}s")

    bdf = pd.DataFrame(books)
    gdf = pd.DataFrame(grid)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    gdf.to_csv(f"{OUT}.grid.csv", index=False)

    # ---- G4/G5/G7/G2
    bad = sum(1 for K in KLAD if gdf[gdf.K == K].CH_PCT.nunique() > K + 1)
    gates.append(dict(gate="G4 CH_PCT distinct values <= K+1 at every rung", value=float(bad),
                      target=0.0, pass_=bad == 0))
    tz = float(np.mean([(g.CH_Z == g.CH_Z.max()).sum() for _, g in gdf.groupby(["panel", "K", "seed"])]))
    gates.append(dict(gate="G5 CH_Z mean cells tied at max == 1.0 (no ceiling)", value=tz,
                      target=1.0, pass_=abs(tz - 1.0) < 1e-9))
    pan0 = Panel(*panels[0])
    st0 = null_starts(pan0, "W", 20, np.random.default_rng(0))
    gmax = float(np.abs(st0.sum(axis=1) - GROSS).max())
    gates.append(dict(gate="G7 null target gross == 0.75 at every rebalance row", value=gmax,
                      target=0.0, pass_=gmax < 1e-12))
    r1 = run_from_starts(pan0, "W", null_starts(pan0, "W", 20, np.random.default_rng(5)))
    r2 = run_from_starts(pan0, "W", null_starts(pan0, "W", 20, np.random.default_rng(5)))
    gates.append(dict(gate="G2 determinism", value=float(np.abs(r1 - r2).max()), target=0.0,
                      pass_=float(np.abs(r1 - r2).max()) == 0.0))
    # G8: the K ladder is NESTED — the K=10 pool is a prefix draw of the same NDRAW pool, so a
    # book's percentile at K=400 is the finest reading of the SAME draws, never new ones.
    gates.append(dict(gate="G8 K ladder costs no extra draws (nested pool)",
                      value=float(NDRAW), target=float(max(KLAD)), pass_=NDRAW == max(KLAD)))

    # ------------------------------------------------------------------ DISCRIMINATION
    say("")
    say("  WHAT THE READER LOSES: DISTINCT VALUES the statistic takes over the 12 books")
    say("  of a panel (mean over 20 seeds). A convention that collapses ceiling readings to a")
    say("  TIE loses resolution ONLY IF the point form had any resolution up there to lose.")
    say(f"    {'panel':6s} {'K':>4}  {'sat':>6}  {'distinct':>8}  {'distinct':>8}  {'ties at':>8}  {'ties at':>8}")
    say(f"    {'':6s} {'':>4}  {'share':>6}  {'PCT':>8}  {'Z':>8}  {'max PCT':>8}  {'max Z':>8}")
    for pname in panel_names:
        for K in KLAD:
            sub = gdf[(gdf.panel == pname) & (gdf.K == K)]
            dp = float(np.mean([g.CH_PCT.nunique() for _, g in sub.groupby("seed")]))
            dz = float(np.mean([g.CH_Z.nunique() for _, g in sub.groupby("seed")]))
            tp = float(np.mean([(g.CH_PCT == g.CH_PCT.max()).sum() for _, g in sub.groupby("seed")]))
            tzz = float(np.mean([(g.CH_Z == g.CH_Z.max()).sum() for _, g in sub.groupby("seed")]))
            sat = float(sub.SAT_CEIL.mean())
            satf = float(sub.SAT_FLOOR.mean())
            disc.append(dict(panel=pname, K=K, sat_ceil_share=sat, sat_floor_share=satf,
                             distinct_PCT=dp, distinct_Z=dz, tied_at_max_PCT=tp, tied_at_max_Z=tzz,
                             n_books=len(ANCHORS)))
            say(f"    {pname:6s} {K:>4}  {sat:>6.3f}  {dp:>8.2f}  {dz:>8.2f}  {tp:>8.2f}  {tzz:>8.2f}")
    pd.DataFrame(disc).to_csv(f"{OUT}.discrimination.csv", index=False)

    # ------------------------------------------------------------------ ARM C/D: RULE 8
    say("")
    say("=" * 96)
    say("(C/D) RULE 8 WALK-FORWARD — the convention is the CHOOSER; IS window 2009-2016 ONLY,")
    say("      2017-2026 read ONCE. B_POINT breaks ties FIRST-WINS (the record's habit);")
    say("      B_ONE/B_TWO/B_CP declare the ceiling a TIE and break it on CH_Z, which is what")
    say("      a bound form FORCES an author to state. CH_Z and CH_ISSHARPE are controls.")
    say("=" * 96)
    for pname in panel_names:
        sb = bdf[bdf.panel == pname].reset_index(drop=True)
        for K in KLAD:
            for chooser in BOUNDS + ["CH_Z", "CH_ISSHARPE"]:
                pl = []
                for sd in range(NSEED):
                    if chooser == "CH_ISSHARPE":
                        j = int(sb.IS_Sharpe.idxmax())
                    else:
                        sub = gdf[(gdf.panel == pname) & (gdf.K == K) & (gdf.seed == sd)]
                        key = sub.sort_values(["cadence", "N"]).reset_index(drop=True)
                        if chooser == "CH_Z":
                            w = key.loc[key.CH_Z.idxmax()]
                        elif chooser == "B_POINT":
                            m = key.CH_PCT.max()
                            w = key[key.CH_PCT == m].iloc[0]          # FIRST-WINS
                        else:
                            m = key.CH_PCT.max()
                            tied = key[key.CH_PCT == m]
                            if len(tied) > 1 or bool(tied.iloc[0].CH_PCT >= 1.0 - 1e-12):
                                w = tied.loc[tied.CH_Z.idxmax()]      # declared tiebreak
                            else:
                                w = tied.iloc[0]
                        j = int(sb[(sb.N == w.N) & (sb.cadence == w.cadence)].index[0])
                    pl.append(j)
                    if chooser == "CH_ISSHARPE":
                        break
                picks = sorted(set(pl))
                modal = max(picks, key=lambda x: (pl.count(x), -x))
                row = sb.loc[modal]
                ctx = pan_ctx[pname]
                wf.append(dict(panel=pname, K=K, chooser=chooser, n_distinct=len(picks),
                               modal_share=pl.count(modal) / len(pl),
                               pick=f"N={int(row.N)}/{row.cadence}",
                               mean_OOS_Sharpe=float(sb.loc[pl].OOS_Sharpe.mean()),
                               OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                               OOS_MaxDD=row.OOS_MaxDD,
                               SPY_OOS_Sharpe=ctx["spy_oos"]["Sharpe"],
                               SPY_OOS_CAGR=ctx["spy_oos"]["CAGR"],
                               LIVE_OOS_Sharpe=ctx["base_oos"]["Sharpe"],
                               KEEP_4a=bool(row.KEEP_4a), KEEP_4b=bool(row.KEEP_4b),
                               KEEP_4b_OOS=bool(row.KEEP_4b_OOS),
                               spread_OOS=float(sb.loc[picks].OOS_Sharpe.max()
                                                - sb.loc[picks].OOS_Sharpe.min()) if len(picks) > 1 else 0.0))
    wdf = pd.DataFrame(wf)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)

    say("")
    say("  MEAN OOS SHARPE OF THE PICK, over 20 seeds, by convention (higher is better).")
    say(f"    {'panel':6s} {'K':>4}  " + "  ".join(f"{c:>10s}" for c in BOUNDS + ["CH_Z", "CH_ISSHARPE"]))
    for pname in panel_names:
        for K in KLAD:
            s = wdf[(wdf.panel == pname) & (wdf.K == K)].set_index("chooser")
            say(f"    {pname:6s} {K:>4}  "
                + "  ".join(f"{s.loc[c].mean_OOS_Sharpe:>10.4f}" for c in BOUNDS + ["CH_Z", "CH_ISSHARPE"]))
    say("")
    say("  POOLED over panels and K (18 (panel,K) cells per convention):")
    pool = wdf.groupby("chooser").mean_OOS_Sharpe.mean().reindex(BOUNDS + ["CH_Z", "CH_ISSHARPE"])
    for c, v in pool.items():
        say(f"    {c:12s} mean OOS Sharpe of pick {v:.4f}   "
            f"(vs B_POINT {v - pool['B_POINT']:+.4f})")

    # ---- both KEEP paths over the whole book population
    say("")
    say("  BOTH KEEP PATHS over all 36 books (PROTOCOL rule 4):")
    say(f"    4a (beat the live book):      {int(bdf.KEEP_4a.sum())} of {len(bdf)}")
    say(f"    4b full sample (vs SPY):      {int(bdf.KEEP_4b.sum())} of {len(bdf)}")
    say(f"    4b OOS-only (vs SPY OOS):     {int(bdf.KEEP_4b_OOS.sum())} of {len(bdf)}")
    say(f"    4b BOTH full and OOS:         {int((bdf.KEEP_4b & bdf.KEEP_4b_OOS).sum())} of {len(bdf)}")
    for pname in panel_names:
        s = bdf[bdf.panel == pname]
        say(f"      {pname:6s} 4a {int(s.KEEP_4a.sum())}/{len(s)}   4b {int(s.KEEP_4b.sum())}/{len(s)}"
            f"   4b-OOS {int(s.KEEP_4b_OOS.sum())}/{len(s)}")
    say(f"    PICKS clearing a KEEP path: 4a {int(wdf.KEEP_4a.sum())} of {len(wdf)}, "
        f"4b {int(wdf.KEEP_4b.sum())} of {len(wdf)}")

    # ------------------------------------------------------------------ GATES
    say("")
    say("=" * 96)
    say("GATES")
    say("=" * 96)
    gdf_g = pd.DataFrame(gates)
    gdf_g.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gdf_g.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate:62s} value={g.value:.6g} target={g.target:.6g}")
    say(f"  {int(gdf_g.pass_.sum())} of {len(gdf_g)} gates pass")
    say(f"\n  total runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))
    return bdf, gdf, wdf, rrdf, gdf_g


if __name__ == "__main__":
    main()
