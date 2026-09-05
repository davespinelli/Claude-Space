#!/usr/bin/env python3
"""IDEA 217  does-the-modal-constant-result-survive-a-cost-ladder   (cloud, 2026-09-05)

THE QUESTION
------------
Idea 189 answered "does any fitted dial beat its own modal pick?" at ONE cost rung, 10 bps.
Its verdict -- read the mode once and write it down, because fitting per book is weakly
dominated -- is a PROTOCOL-clause candidate, and the queue's objection is specific:

    two of idea 171's five dials MOVE TURNOVER.  CADENCE moves it by an order of magnitude
    (D vs Q) and N moves it with book size.  Cost is therefore the one axis that could
    reverse the modal constant's edge, because it re-prices exactly the dial points the
    selector and the mode disagree about.

So: re-run idea 171's five dials on BOTH of idea 189's corpora at 5 / 10 / 15 / 20 / 25 bps
and report, at every rung, the mode, its share, and the MODE-minus-SEL gap.

  Q1  REPRODUCTION.  The 10 bps rung must reproduce idea 171's committed ladder.csv (1908
      rows) and idea 189's published mode/share table, before any new rung is read.
  Q2  COST ADDITIVITY.  The cost ladder is derived, not re-simulated (see DESIGN).  That
      identity is asserted against a direct re-simulation at 25 bps before it is used.
  Q3  THE MODE AT EVERY RUNG.  Per (corpus, dial, rung): the modal SEL-SHARPE pick, its
      share, and whether the mode MOVES with cost.  A mode that migrates with cost is not
      writable as a constant, whatever its share.
  Q4  THE GAP AT EVERY RUNG.  MODE-minus-SEL, paired over books, on both OOS scores and
      under all three mode definitions -- 5 rungs x 2 corpora x 5 dials x 3 modes x 2
      scores = 300 grid points, every one reported.
  Q5  RULE 8 (PROTOCOL clause 8) at every rung, and BOTH KEEP PATHS at every rung.

DESIGN
------
Idea 171's script is IMPORTED, not re-implemented (`Book`, `build_corpus`, `fast_backtest`,
`rel_margin`, `keep_4a`, `keep_4b`, `tstat`, `sign_p`, the five dials and their ladders), and
idea 189's `build_corpus_B` is imported for corpus B.  Every number here sits on the
simulator being audited.

  THE COST LADDER IS DERIVED, NOT RE-SIMULATED.  In idea 171's `fast_backtest` the cost term
  is strictly additive and does NOT feed back into the holdings:

      port[t] = (held[t] * rets[t]).sum()  -  turn[t] * cost_bps / 1e4

  `held` and `turn` are computed from target weights and gross compounding alone, so

      net(c) = gross_returns - turnover * c / 1e4          EXACTLY, for any c.

  Each (book, dial, point) is therefore simulated ONCE at 0 bps and all five rungs are
  subtractions.  Control [d] asserts the identity against a direct fast_backtest(cost=25)
  re-simulation on a sample of books.  This is what makes a 5-rung x 6048-row study cost the
  same as idea 189's 1-rung one; it is an identity, not an approximation.

  dials (idea 171's, unchanged)
      GROSS   [0.20 .. 1.00], 10 points, incumbent 0.75
      N       [3 .. 50],      10 points, incumbent 20
      BAND    [0.00 .. 0.08],  5 points, incumbent 0.00
      CADENCE [D, W, M, Q],    4 points, incumbent W
      SLEEVE  [0.00 .. 0.30],  7 points, incumbent 0.00
  corpus A : idea 171's 53 books (5 fixed panels + 48 seeded B136 sub-panels)
  corpus B : idea 189's 115 books (idea 175's panel definitions under idea 171's Book class)
  rungs    : 5, 10, 15, 20, 25 bps.  t+1 execution.  IS <= 2016-12-31, OOS >= 2017-01-01.
  The RULES v1 baseline and every 4a comparison are re-costed at the SAME rung; SPY is
  buy-and-hold and carries no cost at any rung.

  ARMS, per dial x book x rung
      CONST-INC     idea 171's inherited incumbent                     (the do-nothing arm)
      SEL-SHARPE    argmax of IS Sharpe over the ladder                (the incumbent fit)
      SEL-4B        argmax of the IS 4b relative margin                (the other fit)
      MODE-GLOBAL   the modal SEL-SHARPE pick over the whole corpus, at that rung
      MODE-LOO      the modal SEL-SHARPE pick over the OTHER books     (no self-vote)
      MODE-XCORPUS  corpus A's mode applied to corpus B and vice versa (out-of-corpus)
      RANDOM        a uniformly random ladder point, fixed seed        (idea 151's control)
      ORACLE        the OOS argmax                                     (not implementable)

  TUNED PARAMETER 1: the mode definition   {GLOBAL, LOO, XCORPUS}   (all three reported)
  TUNED PARAMETER 2: the OOS score         {OOS Sharpe, OOS 4b margin} (both reported)
  The COST RUNG is the swept axis the queue asked for, not a tuned parameter: nothing is
  chosen on it and all five are reported side by side.  The dials, ladders and corpora are
  inherited.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  The 10 bps rung reproduces idea 171's committed ladder.csv at < 1e-12 with 0 verdict
      mismatches, and idea 189's mode/share table exactly.
  P2  The cost-additivity identity [d] holds at < 1e-15.
  P3  The mode MOVES with cost on CADENCE (the turnover dial): the modal pick at 25 bps is
      SLOWER than at 5 bps on at least one corpus.
  P4  On the three degenerate dials (GROSS, BAND, SLEEVE -- idea 189/218 showed the IS argmax
      sits on the ladder ENDPOINT in 69-100% of books) the mode does NOT move with cost, and
      |MODE-minus-SEL| stays under 0.01 OOS Sharpe at every rung.
  P5  MODE-LOO's win over SEL-SHARPE on the two live dials (N, CADENCE) survives all five
      rungs on both corpora: 4 of 4 corpus x dial cells positive at every rung, i.e. 20 of 20.
  P6  The MODE-minus-SEL gap on CADENCE is LARGER at 25 bps than at 5 bps (cost punishes the
      selector's off-modal fast picks harder).
  P7  4b pass counts fall monotonically with cost, and no arm produces a 4b KEEP on a FIXED
      panel at 25 bps.

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): B136, U56 and both small panels are CURRENT-CONSTITUENT lists
    with no delistings.  Every arm inherits it equally so the PAIRED comparison is unaffected,
    but every LEVEL here is biased upward and is not a tradable estimate.
  * Corpus A's SMALL484 book is inherited from idea 171 WITHOUT the `max_1d_move >= 1.0`
    filter, because control [c] requires byte-level reproduction of its committed ladder.
    Corpus B's SMALL439 book DOES apply the filter (44 names dropped).  Both are reported
    separately wherever the small family appears.
  * The mode is a statistic of the corpus.  MODE-GLOBAL uses a book's own vote to build the
    constant applied to that book -- a mild leak, which is why MODE-LOO and MODE-XCORPUS sit
    beside it and why the headline is read off MODE-LOO.
  * The books in a corpus are NOT independent: 48 of corpus A's 53 are sub-panels of B136 and
    112 of corpus B's 115 are sub-panels of three parents.  Every paired t is over correlated
    units and its nominal size is optimistic; the exact sign test is reported beside it and
    neither is treated as a p-value on a fresh sample.
  * The five rungs share ONE simulation per ladder point, so the rung-to-rung differences are
    perfectly paired by construction and carry NO simulation noise.  That is the point of the
    identity, but it also means a rung comparison is not an independent replication.
  * Costs here are a flat linear bps charge on turnover.  Real cost is spread + impact and is
    a function of book size and name liquidity; 25 bps on a 439-name sub-$2B panel is not the
    same instrument as 25 bps on U56.  No slippage model is claimed.
  * Idea 144: a re-grossed / re-cadenced / re-sleeved book is the SAME book.  Nothing here is
    a new signal and nothing is proposed.
  * On k=20 sub-panels the N ladder saturates (n >= 20 admits every eligible name), so those
    points collapse onto ew-all.  Inherited from idea 171, reported not hidden.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .modes.csv, .paired.csv,
.walkforward.csv, .keep.csv
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import metrics  # noqa: E402

STEM = "2026-09-05_does-the-modal-constant-result-survive-a-cost-ladder_cloud"
OUT = ROOT / "research" / "backtests"
P171_STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"
P189_STEM = "2026-09-05_does-any-fitted-dial-beat-its-own-modal-pick_cloud"

RUNGS = [5, 10, 15, 20, 25]
BASE_RUNG = 10                      # the rung idea 189/171 published; the reproduction anchor
MODE_ARMS = ["MODE-GLOBAL", "MODE-LOO", "MODE-XCORPUS"]
SCORES = ["OOS_Sharpe", "OOS_margin"]
RAND_SEED = 189_900                 # idea 189's seed, so RANDOM is the same control

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load(stem, name):
    spec = importlib.util.spec_from_file_location(name, OUT / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p171 = _load(P171_STEM, "p171")
p189 = _load(P189_STEM, "p189")
p171.P = P
p189.P = P

DIALS, DIAL_ORDER, INC = p171.DIALS, p171.DIAL_ORDER, p171.INC
IS_END, OOS_START = p171.IS_END, p171.OOS_START
PHI, DELTA, EPS = p171.PHI, p171.DELTA, p171.EPS
fast_backtest, tstat, sign_p = p171.fast_backtest, p171.tstat, p171.sign_p


# ------------------------------------------------------- numpy metric kernels (asserted ==)
def _cagr_sh_dd(x):
    n = len(x)
    if n < 2:
        return np.nan, np.nan, np.nan
    yrs = n / 252.0
    eq = np.cumprod(1.0 + x)
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    vol = x.std(ddof=1) * np.sqrt(252.0)
    sh = (x.mean() * 252.0) / vol if vol else np.nan
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    return float(cagr), float(sh), dd


def _sh(x):
    return _cagr_sh_dd(x)[1] if len(x) > 5 else np.nan


def _halves(x):
    h = len(x) // 2
    return _sh(x[:h]), _sh(x[h:])


def _rel_margin(x, s, sm=None):
    """idea 171's rel_margin, numpy.  sm = precomputed (s1, s2, sSharpe, sMaxDD, sCAGR)."""
    h1, h2 = _halves(x)
    if sm is None:
        s1, s2 = _halves(s)
        sc, ss, sd = _cagr_sh_dd(s)
    else:
        s1, s2, ss, sd, sc = sm
    c, sh, dd = _cagr_sh_dd(x)
    parts = {
        "H1": (h1 - s1) / max(abs(s1), EPS),
        "H2": (h2 - s2) / max(abs(s2), EPS),
        "S": (sh - ss) / max(abs(ss), EPS),
        "DD": (DELTA * abs(sd) - abs(dd)) / max(DELTA * abs(sd), EPS),
        "CAGR": (c - PHI * sc) / max(abs(PHI * sc), EPS),
    }
    worst = min(parts, key=parts.get)
    return min(parts.values()), worst


def _keep_4a(h1, h2, dd, b1, b2, bdd):
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not dd >= bdd: f.append("DD")
    return ",".join(f) if f else "-"


def _keep_4b(h1, h2, sh_oos, cagr, dd, sm_full, sh_spy_oos):
    s1, s2, ss, sd, sc = sm_full
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not sh_oos > sh_spy_oos: f.append("OOS")
    if not abs(dd) <= DELTA * abs(sd): f.append("DD")
    if not cagr >= PHI * sc: f.append("CAGR")
    return ",".join(f) if f else "-"


def _spy_pack(s):
    s1, s2 = _halves(s)
    c, sh, dd = _cagr_sh_dd(s)
    return (s1, s2, sh, dd, c)


# ------------------------------------------------------------------------ the ladder run
def run_ladder(books, panels, tag, t0):
    """One simulation per (book, dial, point) at 0 bps; every rung derived by subtraction."""
    ctx = {}
    for b in books:
        if b.parent not in ctx:
            px = panels[b.parent]
            st = px.index[260]
            spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
            bw = rules_v1_weights(px)
            bres = fast_backtest(px, bw, 0.0, "W")
            ctx[b.parent] = dict(st=st, spy=spy,
                                 bg=bres["returns"].loc[st:], bt=bres["turnover"].loc[st:])

    rows = []
    for bi, bk in enumerate(books):
        c = ctx[bk.parent]
        idx = bk.px.index
        i0 = int(np.searchsorted(idx, c["st"]))
        widx = idx[i0:]
        is_n = int((widx <= pd.Timestamp(IS_END)).sum())
        oos_i = int(np.searchsorted(widx, pd.Timestamp(OOS_START)))

        spy = c["spy"].reindex(widx).fillna(0.0).values
        spy_is, spy_oos = spy[:is_n], spy[oos_i:]
        SM_F, SM_IS, SM_OOS = _spy_pack(spy), _spy_pack(spy_is), _spy_pack(spy_oos)
        sh_spy_oos = _cagr_sh_dd(spy_oos)[1]

        bg = c["bg"].reindex(widx).fillna(0.0).values
        bt = c["bt"].reindex(widx).fillna(0.0).values
        BASE = {}
        for cb in RUNGS:
            bn = bg - bt * cb / 1e4
            b1, b2 = _halves(bn)
            BASE[cb] = (b1, b2, _cagr_sh_dd(bn)[2])

        for dial in DIAL_ORDER:
            ladder, _ = DIALS[dial]
            for pt in ladder:
                kw = dict(gross=INC["GROSS"], n=INC["N"], band=INC["BAND"], sleeve=INC["SLEEVE"])
                fq = INC["CADENCE"]
                if dial == "GROSS":   kw["gross"] = pt
                elif dial == "N":     kw["n"] = pt
                elif dial == "BAND":  kw["band"] = pt
                elif dial == "SLEEVE": kw["sleeve"] = pt
                elif dial == "CADENCE": fq = pt
                res = fast_backtest(bk.px, bk.weights(**kw), 0.0, fq)
                g = res["returns"].values[i0:]
                tn = res["turnover"].values[i0:]
                tpy = tn.sum() / (len(g) / 252.0)

                for cb in RUNGS:
                    r = g - tn * cb / 1e4
                    r_is, r_oos = r[:is_n], r[oos_i:]
                    cf, shf, ddf = _cagr_sh_dd(r)
                    ci, shi, ddi = _cagr_sh_dd(r_is)
                    co, sho, ddo = _cagr_sh_dd(r_oos)
                    h1, h2 = _halves(r)
                    mg_is, wb_is = _rel_margin(r_is, spy_is, SM_IS)
                    mg_oos, wb_oos = _rel_margin(r_oos, spy_oos, SM_OOS)
                    b1, b2, bdd = BASE[cb]
                    rows.append(dict(
                        corpus=tag, cost_bps=cb, book=bk.name, parent=bk.parent, dial=dial,
                        point=pt, is_incumbent=(pt == INC[dial]),
                        CAGR=cf, Sharpe=shf, MaxDD=ddf, H1=h1, H2=h2, turnover=tpy,
                        IS_Sharpe=shi, IS_CAGR=ci, IS_MaxDD=ddi,
                        IS_margin=mg_is, IS_worstbar=wb_is,
                        OOS_Sharpe=sho, OOS_CAGR=co, OOS_MaxDD=ddo,
                        OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                        fail4a=_keep_4a(h1, h2, ddf, b1, b2, bdd),
                        fail4b=_keep_4b(h1, h2, sho, cf, ddf, SM_F, sh_spy_oos)))
        if (bi + 1) % 25 == 0:
            P(f"   ... {tag} {bi + 1}/{len(books)} books  ({time.time() - t0:.0f}s)")
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------ arm logic
_IDX: dict = {}


def index_ladder(lad):
    for rec in lad.to_dict("records"):
        _IDX[(rec["corpus"], rec["cost_bps"], rec["dial"], rec["book"], str(rec["point"]))] = rec


def sc(tag, cb, dial, book, point, col):
    r = _IDX.get((tag, cb, dial, book, str(point)))
    return float(r[col]) if r is not None else np.nan


def picks_of(lad, tag, cb, books):
    rng = np.random.default_rng(RAND_SEED)
    out = []
    sub_all = lad[(lad.corpus == tag) & (lad.cost_bps == cb)]
    for dial in DIAL_ORDER:
        ladder, const = DIALS[dial]
        d = sub_all[sub_all.dial == dial]
        for bk in books:
            s = d[d.book == bk].set_index("point").reindex(ladder)
            out.append(dict(corpus=tag, cost_bps=cb, dial=dial, book=bk, CONST_INC=const,
                            SEL_SHARPE=s["IS_Sharpe"].idxmax(), SEL_4B=s["IS_margin"].idxmax(),
                            RANDOM=ladder[int(rng.integers(len(ladder)))],
                            ORACLE=s["OOS_Sharpe"].idxmax()))
    return pd.DataFrame(out)


def mode_of(vals):
    """Modal pick.  Ties broken by FIRST APPEARANCE in the book order, deterministically."""
    s = [str(x) for x in vals]
    cnt = pd.Series(s).value_counts()
    best, bc = None, -1
    for k in dict.fromkeys(s):                        # first-seen order
        if int(cnt[k]) > bc:
            best, bc = k, int(cnt[k])
    return best, bc / len(s), len(set(s))


def loo_modes(names, vals):
    """Modal pick over the OTHER books, for every book.  Same tie-break as mode_of (pandas
    value_counts: count desc, then first-seen order), computed by removing one vote."""
    s = [str(x) for x in vals]
    base = pd.Series(s).value_counts()
    order = list(pd.Series(s).drop_duplicates())      # first-seen order, mode_of's tie-break
    out = {}
    for nm, v in zip(names, s):
        cnt = base.copy()
        cnt[v] -= 1
        best, bc = None, -1
        for k in order:
            c = int(cnt.get(k, 0))
            if c > bc:
                best, bc = k, c
        out[nm] = best
    return out


def as_point(dial, s):
    for p in DIALS[dial][0]:
        if str(p) == s:
            return p
    raise KeyError((dial, s))


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 217  does-the-modal-constant-result-survive-a-cost-ladder   (cloud, 2026-09-05)")
    P("=" * 118)
    P(f"rungs = {RUNGS} bps | dials = {DIAL_ORDER} | IS <= {IS_END}, OOS >= {OOS_START}")

    # ------------------------------------------------------------------ corpora + repro
    P("\nbuilding corpus A (idea 171's build_corpus, imported) ...")
    booksA, panelsA = p171.build_corpus()
    P(f"  corpus A: {len(booksA)} books   (SMALL484 inherited UNFILTERED -- see caveats)")
    P("\nREPRODUCTION CONTROLS (asserted before any new number is read)")
    okA = p171.check_a(booksA[1])
    okB = all(p171.check_b(b) for b in booksA[:3])
    if not (okA and okB):
        P("\n*** REPRODUCTION FAILED -- not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # [e] the numpy metric kernels must equal engine.metrics / idea 171's helpers
    P("\n  [e] numpy metric kernels vs engine.metrics and idea 171's rel_margin/halves:")
    rng0 = np.random.default_rng(217)
    de = dh = dm = 0.0
    for bk in booksA[:3]:
        for fq in ["D", "W", "M", "Q"]:
            w = bk.weights(INC["GROSS"], INC["N"], INC["BAND"], INC["SLEEVE"])
            r = fast_backtest(bk.px, w, 10, fq)["returns"].iloc[260:]
            spy = bk.px["SPY"].pct_change().fillna(0.0).reindex(r.index).fillna(0.0)
            mm = metrics(r)
            c, s, d = _cagr_sh_dd(r.values)
            de = max(de, abs(c - mm["CAGR"]), abs(s - mm["Sharpe"]), abs(d - mm["MaxDD"]))
            h = p171.halves(r)
            hh = _halves(r.values)
            dh = max(dh, abs(h[0] - hh[0]), abs(h[1] - hh[1]))
            a, _ = p171.rel_margin(r, spy)
            b, _ = _rel_margin(r.values, spy.values)
            dm = max(dm, abs(a - b))
    P(f"      max |dCAGR/dSharpe/dMaxDD| = {de:.3e} | halves {dh:.3e} | rel_margin {dm:.3e}"
      f"   -> {'PASS' if max(de, dh, dm) < 1e-12 else 'FAIL'}")
    if max(de, dh, dm) >= 1e-12:
        P("\n*** metric kernels do not reproduce engine.metrics.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # [d] the cost-additivity identity, asserted BEFORE it is used anywhere
    P("\n  [d] cost additivity: derived net(c) = gross - turnover*c/1e4  vs a DIRECT "
      "fast_backtest(cost=c) re-simulation")
    dmax_add = 0.0
    for bk in booksA[:3]:
        for dial, pt, fq in [("GROSS", 0.40, "W"), ("N", 5, "W"), ("CADENCE", INC["N"], "D"),
                             ("CADENCE", INC["N"], "Q"), ("SLEEVE", 0.30, "W")]:
            kw = dict(gross=INC["GROSS"], n=INC["N"], band=INC["BAND"], sleeve=INC["SLEEVE"])
            if dial == "GROSS": kw["gross"] = pt
            elif dial == "N": kw["n"] = pt
            elif dial == "SLEEVE": kw["sleeve"] = pt
            w = bk.weights(**kw)
            z = fast_backtest(bk.px, w, 0.0, fq)
            for cb in RUNGS:
                direct = fast_backtest(bk.px, w, cb, fq)["returns"].values
                der = z["returns"].values - z["turnover"].values * cb / 1e4
                dmax_add = max(dmax_add, float(np.abs(direct - der).max()))
    P(f"      max |direct - derived| over 3 books x 5 configs x 5 rungs = {dmax_add:.3e}"
      f"   -> {'PASS' if dmax_add < 1e-15 else 'FAIL'}")
    if dmax_add >= 1e-15:
        P("\n*** the derived cost ladder is not an identity.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    P("\nrunning corpus A ladders (1 simulation per point, 5 rungs derived) ...")
    ladA = run_ladder(booksA, panelsA, "A", t0)
    P(f"   {len(ladA)} rung-rows = {len(ladA)//len(RUNGS)} ladder points x {len(RUNGS)} rungs"
      f"  ({time.time() - t0:.0f}s)")

    # [c] the 10 bps rung must be idea 171's committed ladder
    C171 = pd.read_csv(OUT / f"{P171_STEM}.ladder.csv")
    a10 = ladA[ladA.cost_bps == BASE_RUNG].copy()
    m = a10.astype({"point": str}).merge(C171.astype({"point": str}),
                                         on=["book", "dial", "point"], suffixes=("", "_c"))
    P(f"\n  [c] derived 10 bps rung vs idea 171's committed ladder.csv: "
      f"{len(m)}/{len(C171)} rows matched")
    dmax = 0.0
    for col in ["IS_Sharpe", "OOS_Sharpe", "OOS_margin", "OOS_CAGR", "OOS_MaxDD", "Sharpe",
                "CAGR", "MaxDD", "H1", "H2", "IS_margin", "turnover"]:
        d = float((m[col] - m[f"{col}_c"]).abs().max())
        dmax = max(dmax, d)
        P(f"      max |d{col}| = {d:.3e}")
    v4 = int((m["fail4b"] != m["fail4b_c"]).sum()) + int((m["fail4a"] != m["fail4a_c"]).sum())
    P(f"      4a/4b verdict mismatches: {v4}")
    repro = (len(m) == len(C171)) and dmax < 1e-12 and v4 == 0
    P(f"      -> {'PASS' if repro else 'FAIL'}")
    if not repro:
        P("\n*** idea 171's corpus does not reproduce.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    P("\nbuilding corpus B (idea 189's build_corpus_B, imported) ...")
    booksB, panelsB = p189.build_corpus_B()
    P(f"  corpus B: {len(booksB)} books")
    P("\nrunning corpus B ladders ...")
    ladB = run_ladder(booksB, panelsB, "B", t0)
    P(f"   {len(ladB)} rung-rows  ({time.time() - t0:.0f}s)")

    lad = pd.concat([ladA, ladB], ignore_index=True)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    index_ladder(lad)
    NAMES = {"A": [b.name for b in booksA], "B": [b.name for b in booksB]}

    # --------------------------------------------------------------------------- picks
    P(f"\nderiving picks ({time.time() - t0:.0f}s) ...")
    PICKS = {}
    for tag in ["A", "B"]:
        for cb in RUNGS:
            PICKS[(tag, cb)] = picks_of(lad, tag, cb, NAMES[tag])

    # ------------------------------------------------------------- Q3 the mode at every rung
    mrows = []
    for tag in ["A", "B"]:
        for cb in RUNGS:
            pk = PICKS[(tag, cb)]
            for dial in DIAL_ORDER:
                v = pk[pk.dial == dial]["SEL_SHARPE"].tolist()
                md, share, dis = mode_of(v)
                mrows.append(dict(corpus=tag, cost_bps=cb, dial=dial, mode=md, mode_share=share,
                                  n_books=len(v), distinct=dis, incumbent=str(INC[dial]),
                                  mode_is_incumbent=(md == str(INC[dial]))))
    modes = pd.DataFrame(mrows)
    modes.to_csv(OUT / f"{STEM}.modes.csv", index=False)
    MODE = {(r["corpus"], r["cost_bps"], r["dial"]): r["mode"] for r in mrows}

    LOO = {}
    for tag in ["A", "B"]:
        for cb in RUNGS:
            pk = PICKS[(tag, cb)]
            for dial in DIAL_ORDER:
                d = pk[pk.dial == dial]
                for bk, mm in loo_modes(list(d["book"]), list(d["SEL_SHARPE"])).items():
                    LOO[(tag, cb, dial, bk)] = mm

    P("\n" + "=" * 118)
    P("Q3  THE MODE AT EVERY RUNG  (modal SEL-SHARPE pick / its share).  A mode that MOVES "
      "with cost is not writable.")
    P("=" * 118)
    for tag in ["A", "B"]:
        P(f"\ncorpus {tag}  ({len(NAMES[tag])} books)")
        P(f"  {'dial':<9s} {'inc':<6s} " + " ".join(f"{str(c) + 'bps':>16s}" for c in RUNGS)
          + "   moves?")
        for dial in DIAL_ORDER:
            cells, ms = [], []
            for cb in RUNGS:
                r = modes[(modes.corpus == tag) & (modes.cost_bps == cb) & (modes.dial == dial)].iloc[0]
                cells.append(f"{r['mode']:>7s} {r['mode_share']:>7.1%}")
                ms.append(r["mode"])
            mv = "MOVES " + " -> ".join(dict.fromkeys(ms)) if len(set(ms)) > 1 else "stable"
            P(f"  {dial:<9s} {str(INC[dial]):<6s} " + " ".join(f"{c:>16s}" for c in cells)
              + f"   {mv}")

    # ------------------------------------------------- Q4 the gap at every rung (paired)
    P("\n" + "=" * 118)
    P("Q4  MODE-minus-SEL AT EVERY RUNG   (positive = the constant beats the fit).  "
      "Paired over books; every grid point reported.")
    P("=" * 118)
    prows = []
    for tag in ["A", "B"]:
        oth = "B" if tag == "A" else "A"
        for cb in RUNGS:
            pk = PICKS[(tag, cb)].set_index(["dial", "book"])
            for dial in DIAL_ORDER:
                for arm in MODE_ARMS + ["CONST-INC", "SEL-4B", "RANDOM", "ORACLE"]:
                    for score in SCORES:
                        ds, agree = [], 0
                        off = []
                        for bk in NAMES[tag]:
                            row = pk.loc[(dial, bk)]
                            sel = row["SEL_SHARPE"]
                            if arm == "MODE-GLOBAL":
                                cand = MODE[(tag, cb, dial)]
                            elif arm == "MODE-LOO":
                                cand = LOO[(tag, cb, dial, bk)]
                            elif arm == "MODE-XCORPUS":
                                cand = MODE[(oth, cb, dial)]
                            elif arm == "CONST-INC":
                                cand = str(INC[dial])
                            elif arm == "SEL-4B":
                                cand = str(row["SEL_4B"])
                            elif arm == "RANDOM":
                                cand = str(row["RANDOM"])
                            else:
                                cand = str(row["ORACLE"])
                            a = sc(tag, cb, dial, bk, as_point(dial, cand), score)
                            b = sc(tag, cb, dial, bk, sel, score)
                            ds.append(a - b)
                            same = (cand == str(sel))
                            agree += same
                            if not same:
                                off.append(a - b)
                        ds = np.array(ds, float)
                        p, w, l = sign_p(ds)
                        prows.append(dict(corpus=tag, cost_bps=cb, dial=dial, arm=arm,
                                          score=score, n=len(ds), mean_d=float(np.nanmean(ds)),
                                          median_d=float(np.nanmedian(ds)), t=tstat(ds),
                                          wins=w, losses=l, ties=int((ds == 0).sum()),
                                          sign_p=p, agree_share=agree / len(ds),
                                          off_n=len(off),
                                          off_mean_d=float(np.mean(off)) if off else np.nan))
    paired = pd.DataFrame(prows)
    paired.to_csv(OUT / f"{STEM}.paired.csv", index=False)

    for score in SCORES:
        for tag in ["A", "B"]:
            P(f"\nMODE-LOO minus SEL-SHARPE   score = {score}   corpus {tag}")
            P(f"  {'dial':<9s} " + " ".join(f"{str(c) + 'bps':>20s}" for c in RUNGS))
            for dial in DIAL_ORDER:
                cells = []
                for cb in RUNGS:
                    r = paired[(paired.corpus == tag) & (paired.cost_bps == cb)
                               & (paired.dial == dial) & (paired.arm == "MODE-LOO")
                               & (paired.score == score)].iloc[0]
                    cells.append(f"{r['mean_d']:+.4f} t{r['t']:+6.2f}")
                P(f"  {dial:<9s} " + " ".join(f"{c:>20s}" for c in cells))
            won = []
            for cb in RUNGS:
                s = paired[(paired.corpus == tag) & (paired.cost_bps == cb)
                           & (paired.arm == "MODE-LOO") & (paired.score == score)]
                won.append(int((s.mean_d > 0).sum()))
            P(f"  {'dials won':<9s} " + " ".join(f"{str(x) + '/5':>20s}" for x in won))

    P("\nALL THREE MODE DEFINITIONS x BOTH SCORES x 5 RUNGS -- dials won (of 5), per corpus")
    P(f"  {'arm':<13s} {'score':<11s} {'corpus':<7s} " + " ".join(f"{str(c) + 'bps':>8s}" for c in RUNGS))
    for arm in MODE_ARMS:
        for score in SCORES:
            for tag in ["A", "B"]:
                cnt = []
                for cb in RUNGS:
                    s = paired[(paired.corpus == tag) & (paired.cost_bps == cb)
                               & (paired.arm == arm) & (paired.score == score)]
                    cnt.append(int((s.mean_d > 0).sum()))
                P(f"  {arm:<13s} {score:<11s} {tag:<7s} " + " ".join(f"{str(x) + '/5':>8s}" for x in cnt))

    P("\nTHE TWO LIVE DIALS (N, CADENCE) -- MODE-LOO minus SEL-SHARPE, OOS Sharpe, "
      "with the exact sign test")
    P(f"  {'corpus':<7s} {'dial':<9s} {'bps':>4s} {'agree':>7s} {'off n':>6s} {'off mean':>10s} "
      f"{'overall':>10s} {'t':>8s} {'W/L':>8s} {'sign p':>8s}")
    for tag in ["A", "B"]:
        for dial in ["N", "CADENCE"]:
            for cb in RUNGS:
                r = paired[(paired.corpus == tag) & (paired.cost_bps == cb) & (paired.dial == dial)
                           & (paired.arm == "MODE-LOO") & (paired.score == "OOS_Sharpe")].iloc[0]
                P(f"  {tag:<7s} {dial:<9s} {cb:>4d} {r['agree_share']:>7.1%} {r['off_n']:>6d} "
                  f"{r['off_mean_d']:>+10.4f} {r['mean_d']:>+10.4f} {r['t']:>+8.2f} "
                  f"{r['wins']:>3d}/{r['losses']:<4d} {r['sign_p']:>8.4f}")

    # ------------------------------------------------------------------- Q5 rule 8 + KEEP
    P("\n" + "=" * 118)
    P("Q5  RULE 8 WALK-FORWARD AT EVERY RUNG.  Every arm chooses on IS <= 2016-12-31 ONLY; "
      "2017-2026 read once.")
    P("    (ORACLE reads the OOS window and is NOT implementable -- it is the ceiling, not "
      "an arm.)")
    P("=" * 118)
    wrows = []
    ARMS8 = ["CONST-INC", "SEL-SHARPE", "SEL-4B", "MODE-GLOBAL", "MODE-LOO", "MODE-XCORPUS",
             "RANDOM", "ORACLE"]
    for tag in ["A", "B"]:
        oth = "B" if tag == "A" else "A"
        for cb in RUNGS:
            pk = PICKS[(tag, cb)].set_index(["dial", "book"])
            for arm in ARMS8:
                acc = {k: [] for k in ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_margin"]}
                p4a = p4b = 0
                for dial in DIAL_ORDER:
                    for bk in NAMES[tag]:
                        row = pk.loc[(dial, bk)]
                        if arm == "CONST-INC":       cand = str(INC[dial])
                        elif arm == "SEL-SHARPE":    cand = str(row["SEL_SHARPE"])
                        elif arm == "SEL-4B":        cand = str(row["SEL_4B"])
                        elif arm == "MODE-GLOBAL":   cand = MODE[(tag, cb, dial)]
                        elif arm == "MODE-XCORPUS":  cand = MODE[(oth, cb, dial)]
                        elif arm == "RANDOM":        cand = str(row["RANDOM"])
                        elif arm == "ORACLE":        cand = str(row["ORACLE"])
                        else:                        cand = LOO[(tag, cb, dial, bk)]
                        rec = _IDX[(tag, cb, dial, bk, cand)]
                        for k in acc:
                            acc[k].append(rec[k])
                        p4a += rec["fail4a"] == "-"
                        p4b += rec["fail4b"] == "-"
                wrows.append(dict(corpus=tag, cost_bps=cb, arm=arm,
                                  n=len(acc["OOS_Sharpe"]),
                                  **{k: float(np.nanmean(v)) for k, v in acc.items()},
                                  pass4a=p4a, pass4b=p4b))
    wf = pd.DataFrame(wrows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # SPY and RULES v1 OOS references, per parent panel, per rung
    P("\nreferences on the OOS window (2017-01-01 onward), per parent panel")
    P(f"  {'corpus':<7s} {'panel':<8s} {'series':<16s} {'bps':>4s} {'CAGR':>8s} {'Sharpe':>8s} "
      f"{'MaxDD':>8s}")
    refrows = []
    for nm, panels in [("A", panelsA), ("B", panelsB)]:
        for par, px in panels.items():
            st = px.index[260]
            spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
            c, s, d = _cagr_sh_dd(spy.loc[OOS_START:].values)
            refrows.append(dict(corpus=nm, panel=par, series="SPY", cost_bps=np.nan,
                                OOS_CAGR=c, OOS_Sharpe=s, OOS_MaxDD=d))
            P(f"  {nm:<7s} {par:<8s} {'SPY buy&hold':<16s} {'-':>4s} {c:>8.2%} {s:>8.4f} {d:>8.2%}")
            br = fast_backtest(px, rules_v1_weights(px), 0.0, "W")
            bg = br["returns"].loc[st:].loc[OOS_START:].values
            bt = br["turnover"].loc[st:].loc[OOS_START:].values
            for cb in RUNGS:
                c, s, d = _cagr_sh_dd(bg - bt * cb / 1e4)
                refrows.append(dict(corpus=nm, panel=par, series="RULES v1", cost_bps=cb,
                                    OOS_CAGR=c, OOS_Sharpe=s, OOS_MaxDD=d))
                P(f"  {nm:<7s} {par:<8s} {'RULES v1':<16s} {cb:>4d} {c:>8.2%} {s:>8.4f} {d:>8.2%}")
    pd.DataFrame(refrows).to_csv(OUT / f"{STEM}.refs.csv", index=False)

    for tag in ["A", "B"]:
        P(f"\npooled OOS Sharpe by arm and rung -- corpus {tag} "
          f"(mean over 5 dials x {len(NAMES[tag])} books)")
        P(f"  {'arm':<13s} " + " ".join(f"{str(c) + 'bps':>9s}" for c in RUNGS)
          + f" {'d(25-5)':>10s}")
        for arm in ARMS8:
            v = [float(wf[(wf.corpus == tag) & (wf.cost_bps == cb) & (wf.arm == arm)]["OOS_Sharpe"].iloc[0])
                 for cb in RUNGS]
            P(f"  {arm:<13s} " + " ".join(f"{x:>9.4f}" for x in v) + f" {v[-1] - v[0]:>+10.4f}")
        P(f"\npooled OOS CAGR / MaxDD by arm -- corpus {tag}")
        P(f"  {'arm':<13s} " + " ".join(f"{str(c) + 'bps':>17s}" for c in RUNGS))
        for arm in ARMS8:
            cells = []
            for cb in RUNGS:
                r = wf[(wf.corpus == tag) & (wf.cost_bps == cb) & (wf.arm == arm)].iloc[0]
                cells.append(f"{r['OOS_CAGR']:>7.2%}/{r['OOS_MaxDD']:>8.2%}")
            P(f"  {arm:<13s} " + " ".join(f"{c:>17s}" for c in cells))

    # -------------------------------------------------------------------- both KEEP paths
    P("\n" + "=" * 118)
    P("BOTH KEEP PATHS AT EVERY RUNG   (4a vs each panel's own RULES v1 re-costed at the "
      "same rung; 4b vs SPY)")
    P("=" * 118)
    krows = []
    for tag in ["A", "B"]:
        for cb in RUNGS:
            s = lad[(lad.corpus == tag) & (lad.cost_bps == cb)]
            fx = s[~s.book.str.contains("k[0-9]+d[0-9]+$", regex=True)]
            krows.append(dict(corpus=tag, cost_bps=cb, rows=len(s),
                              pass4a=int((s.fail4a == "-").sum()),
                              pass4b=int((s.fail4b == "-").sum()),
                              fixed_rows=len(fx),
                              fixed4a=int((fx.fail4a == "-").sum()),
                              fixed4b=int((fx.fail4b == "-").sum())))
    keep = pd.DataFrame(krows)
    keep.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  {'corpus':<7s} {'bps':>4s} {'rows':>6s} {'4a':>7s} {'4b':>7s} | "
      f"{'fixed rows':>10s} {'4a':>6s} {'4b':>6s}")
    for r in krows:
        P(f"  {r['corpus']:<7s} {r['cost_bps']:>4d} {r['rows']:>6d} {r['pass4a']:>7d} "
          f"{r['pass4b']:>7d} | {r['fixed_rows']:>10d} {r['fixed4a']:>6d} {r['fixed4b']:>6d}")

    P("\n4b passes on the FIXED panels only, by panel and rung  (sub-panel books are a corpus "
      "device, not tradable books)")
    fixnames = sorted(set(lad[~lad.book.str.contains("k[0-9]+d[0-9]+$", regex=True)].book))
    P(f"  {'panel':<10s} {'corpus':<7s} " + " ".join(f"{str(c) + 'bps':>9s}" for c in RUNGS))
    for tag in ["A", "B"]:
        for nm in fixnames:
            s0 = lad[(lad.corpus == tag) & (lad.book == nm)]
            if s0.empty:
                continue
            v = [int((s0[s0.cost_bps == cb].fail4b == "-").sum()) for cb in RUNGS]
            tot = len(s0[s0.cost_bps == RUNGS[0]])
            P(f"  {nm:<10s} {tag:<7s} " + " ".join(f"{str(x) + '/' + str(tot):>9s}" for x in v))

    P("\n4b passes among the ARM-CHOSEN cells only (implementable arms; the number that would "
      "matter for capital)")
    P(f"  {'arm':<13s} {'corpus':<7s} " + " ".join(f"{str(c) + 'bps':>9s}" for c in RUNGS))
    for arm in ARMS8:
        for tag in ["A", "B"]:
            v = [int(wf[(wf.corpus == tag) & (wf.cost_bps == cb) & (wf.arm == arm)]["pass4b"].iloc[0])
                 for cb in RUNGS]
            n = int(wf[(wf.corpus == tag) & (wf.cost_bps == RUNGS[0]) & (wf.arm == arm)]["n"].iloc[0])
            P(f"  {arm:<13s} {tag:<7s} " + " ".join(f"{str(x) + '/' + str(n):>9s}" for x in v))

    # ------------------------------------------------------------------------ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    p189_modes = pd.read_csv(OUT / f"{P189_STEM}.modes.csv")
    m10 = modes[modes.cost_bps == BASE_RUNG][["corpus", "dial", "mode", "mode_share"]]
    j = m10.merge(p189_modes[["corpus", "dial", "mode", "mode_share"]], on=["corpus", "dial"],
                  suffixes=("", "_189"))
    mode_ok = bool((j["mode"].astype(str) == j["mode_189"].astype(str)).all()
                   and (j["mode_share"] - j["mode_share_189"]).abs().max() < 1e-12)
    P(f"  idea 189 mode/share table reproduced on {len(j)} cells: {mode_ok}")

    cad_moves = any(len(set(modes[(modes.corpus == t) & (modes.dial == "CADENCE")]["mode"])) > 1
                    for t in ["A", "B"])
    order = {"D": 0, "W": 1, "M": 2, "Q": 3}
    cad_slower = any(order[modes[(modes.corpus == t) & (modes.dial == "CADENCE")
                                 & (modes.cost_bps == 25)]["mode"].iloc[0]]
                     > order[modes[(modes.corpus == t) & (modes.dial == "CADENCE")
                                   & (modes.cost_bps == 5)]["mode"].iloc[0]] for t in ["A", "B"])
    deg_stable = all(len(set(modes[(modes.corpus == t) & (modes.dial == d)]["mode"])) == 1
                     for t in ["A", "B"] for d in ["GROSS", "BAND", "SLEEVE"])
    deg_small = float(paired[(paired.arm == "MODE-LOO") & (paired.score == "OOS_Sharpe")
                             & (paired.dial.isin(["GROSS", "BAND", "SLEEVE"]))]["mean_d"].abs().max())
    live = paired[(paired.arm == "MODE-LOO") & (paired.score == "OOS_Sharpe")
                  & (paired.dial.isin(["N", "CADENCE"]))]
    live_pos = int((live.mean_d > 0).sum())
    cadA = [float(paired[(paired.corpus == t) & (paired.cost_bps == cb) & (paired.dial == "CADENCE")
                         & (paired.arm == "MODE-LOO") & (paired.score == "OOS_Sharpe")]["mean_d"].iloc[0])
            for t in ["A", "B"] for cb in [5, 25]]
    cad_bigger = (cadA[1] > cadA[0]) and (cadA[3] > cadA[2])
    mono4b = all(list(keep[keep.corpus == t].sort_values("cost_bps")["pass4b"])
                 == sorted(keep[keep.corpus == t]["pass4b"], reverse=True) for t in ["A", "B"])
    fixed4b25 = int(keep[keep.cost_bps == 25]["fixed4b"].sum())

    preds = [
        ("P1 10bps reproduces idea 171 ladder + idea 189 modes", repro and mode_ok,
         f"ladder {dmax:.1e}/{v4} mismatches, modes {mode_ok}"),
        ("P2 cost additivity holds at < 1e-15", dmax_add < 1e-15, f"{dmax_add:.3e}"),
        ("P3 CADENCE mode moves with cost, slower at 25 than 5", cad_moves and cad_slower,
         f"moves={cad_moves} slower={cad_slower}"),
        ("P4 degenerate dials: mode stable AND |gap| < 0.01", deg_stable and deg_small < 0.01,
         f"stable={deg_stable} max|gap|={deg_small:.4f}"),
        ("P5 live dials: MODE-LOO positive in 20 of 20 cells", live_pos == 20, f"{live_pos}/20"),
        ("P6 CADENCE gap larger at 25 bps than at 5 bps (both corpora)", cad_bigger,
         f"A {cadA[0]:+.4f}->{cadA[1]:+.4f}, B {cadA[2]:+.4f}->{cadA[3]:+.4f}"),
        ("P7 4b counts fall monotonically; 0 fixed-panel 4b at 25 bps",
         mono4b and fixed4b25 == 0, f"monotone={mono4b}, fixed 4b @25bps={fixed4b25}"),
    ]
    for nm, hit, det in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {nm:<58s} {det}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
