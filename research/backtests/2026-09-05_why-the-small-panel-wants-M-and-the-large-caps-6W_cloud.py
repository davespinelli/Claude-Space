#!/usr/bin/env python3
"""IDEA 188  why-does-the-small-panel-want-M-and-the-large-caps-6W   (cloud, 2026-09-05)

THE QUESTION (verbatim from QUEUE.md idea 188)
----------------------------------------------
    "idea 175's constant table splits cleanly: M is +0.0978 (t +3.91) on the small family
     where 6W is +0.0163 (n.s.), while on u56/ETF 6W is +0.164/+0.160 and Q is -0.25/-0.29.
     Turnover alone does not explain it (small turns 15.6x at D vs 12.7x on u56).  Decompose
     the M-vs-6W gap by holding-episode length (idea 76) and by realised signal decay per
     panel; the output is the universe clause idea 77 wants.  Max 2 params."

M is 21 bars; 6W is 30.  So the small panel wants the FASTER of the two and the large-cap
panels want the SLOWER one -- the opposite of what cost alone would predict, because the
small panel is the one that turns over harder.  Two candidate mechanisms, and this run
separates them:

    COST      the gap is a turnover-pricing effect.  Then it must SHRINK to zero (or reverse)
              when the same books are run at 0 bps, and must GROW at 25 bps.
    SIGNAL    the gap is a decay effect: the composite's forecast dies faster on small caps,
              so a 30-bar hold is stale there and a 21-bar hold is not.  Then it must SURVIVE
              at 0 bps, and the panel's realised IC decay curve must cross between h=21 and
              h=30 in the direction the cadence table says.

  Q1  REPRODUCTION.  Rebuild idea 175's 805-row ladder with its own code and match its
      committed ladder.csv before any new number is read; re-derive its published M/6W table.
  Q2  THE GAP.  M minus 6W, paired over books, per family, on full Sharpe and OOS Sharpe.
  Q3  COST vs SIGNAL.  The same paired gap at 0 / 10 / 25 bps.  The 0 bps column is the pure
      signal effect; (10 bps - 0 bps) is the pure cost effect, exactly (see DESIGN).
  Q4  HOLDING-EPISODE LENGTH (idea 76's instrument).  Per panel and cadence: episodes per
      year, mean episode length, and the PERSISTENCE RATIO -- mean episode length divided by
      the cadence's nominal block length.  A ratio near 1 means the book re-picks from
      scratch every block; a large ratio means names persist through rebalances and the dial
      is not really changing the book.
  Q5  REALISED SIGNAL DECAY per panel: the cross-sectional rank IC of the composite against
      forward h-bar returns among ELIGIBLE names, h in {5,10,21,30,42,63,84}, plus the
      realised top-20-minus-eligible-mean forward excess at the same horizons.  The M-vs-6W
      question is literally IC(21) vs IC(30).
  Q6  RULE 8 (PROTOCOL clause 8) and BOTH KEEP PATHS.
  Q7  THE CLAUSE.  Whatever survives Q3-Q5, written as the universe clause idea 77 asked for.

DESIGN
------
Idea 175's script is IMPORTED, not re-implemented (`cad_mask`, `fast_backtest`, `Book`,
`build_corpus`, `family_of`, `rel_margin`, `keep_4a`, `keep_4b`, `tstat`, `sign_p`, the
7-point ladder and the 115-book corpus), so every number sits on the simulator being audited.

  THE COST AXIS IS DERIVED, NOT RE-SIMULATED.  In idea 175's `fast_backtest` the cost term is
  additive and does not feed back into the holdings:

      port[t] = (held[t] * rets[t]).sum() - turn[t] * cost_bps / 1e4
      =>  net(c) = gross_returns - turnover * c / 1e4     EXACTLY, for any c.

  Each (book, cadence) is simulated ONCE at 0 bps and the 10 and 25 bps columns are
  subtractions.  Control [d] asserts the identity against a direct re-simulation before it is
  used.  This is what makes the cost/signal split EXACT rather than two noisy runs: the 0 bps
  and 10 bps books are the same book, bar for bar.

  ladder   D, 2D, W, 2W, M, 6W, Q  (idea 175's, unchanged; all 7 reported)
  corpus   idea 175's 115 books: SMALL439 / U56 / ETF36 + 112 seeded sub-panels
  book     idea 2's 4b candidate: top-20 EW on the scan.py composite, no vol scaler,
           gross 0.75, bare 200d gate, vol20 < 0.60.  Held fixed; only cadence moves.
  windows  IS <= 2016-12-31, OOS >= 2017-01-01 read once.  t+1 execution throughout.

  TUNED PARAMETER 1: the cadence ladder point (7 values, ALL reported, none picked).
  TUNED PARAMETER 2: the IC horizon h (7 values, ALL reported, none picked).
  The cost rungs are a DECOMPOSITION axis, not a tuned parameter: nothing is chosen on them
  and all three are reported side by side.  Panel and family are corpus axes.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  Idea 175's ladder reproduces at < 1e-12 over all 805 rows with 0 verdict mismatches.
  P2  The cost-additivity identity [d] holds at < 1e-15.
  P3  SIGNAL, not COST: the M-minus-6W gap on the SMALL family is still POSITIVE at 0 bps,
      i.e. it is not bought by turnover pricing.
  P4  The sign SPLIT survives at 0 bps too: M-minus-6W is positive on SMALL and negative on
      U56 and ETF at every one of the three cost rungs (9 of 9 sign cells as published).
  P5  DECAY: the small panel's eligible-name rank IC falls by a larger FRACTION between h=21
      and h=30 than U56's does, i.e. IC(30)/IC(21) is smaller on SMALL than on U56.
  P6  PERSISTENCE: the small panel's persistence ratio at M is LOWER than U56's at M (small
      names churn out of the top 20 within a block; mega caps persist across blocks).
  P7  No arm produces a 4b KEEP on a FIXED panel at any cost rung that is not a re-cadencing
      of an existing book (idea 144).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md).  SMALL439 is the 483-name sub-$2B
    screen with the 44 `max_1d_move >= 1.0` names dropped, and it is a CURRENT-CONSTITUENT
    list: names that delisted, were acquired or went to zero are absent, and the bias falls
    hardest on exactly the beaten-down cohort a trend gate would have excluded.  U56 and ETF36
    are current lists too.  Every cadence and every arm inherits the bias equally so the
    PAIRED M-minus-6W comparison is unaffected; every LEVEL here is biased upward and no
    small-panel CAGR or Sharpe below is an attainable return.
  * THE SURVIVORSHIP BIAS IS NOT NEUTRAL FOR Q5.  A current-constituent small-cap panel has
    had its worst forward returns removed, which inflates the measured IC at EVERY horizon.
    The comparison read here is the SHAPE of the decay curve (the ratio IC(30)/IC(21)) across
    panels, not its level; the shape is still contaminated if the bias is horizon-dependent,
    and that cannot be ruled out from this data.  Stated, not hidden.
  * Idea 38: data/prices.csv is calendar-day indexed from 2014-09-17, so a "bar" is a calendar
    day on U56/ETF36 after that date while the small panel is trading-day indexed throughout.
    M (a calendar month) and 6W (6 ISO weeks) are therefore slightly different numbers of BARS
    on the two panel families -- which is itself part of what a cadence clause has to say.
    The realised bar counts are measured and reported in Q4 rather than assumed.
  * The books are NOT independent: 112 of 115 are sub-panels of three parents.  Every paired t
    is over correlated units and its nominal size is optimistic; the exact sign test is
    reported beside it and neither is a p-value on a fresh sample.
  * The three cost rungs share ONE simulation per book x cadence, so rung-to-rung differences
    carry no simulation noise -- that is the point of the identity, but it also means the
    0 vs 10 bps comparison is not an independent replication.
  * Cost is a flat linear bps charge on turnover.  Real cost is spread plus impact and is a
    function of name liquidity; 10 bps on a 439-name sub-$2B panel is not the same instrument
    as 10 bps on U56, and that alone could carry a cadence clause.  No slippage model is
    claimed, and this is the single largest reason the SMALL numbers here are soft.
  * Idea 144: a re-cadenced book is the SAME book.  Nothing here is a new signal and nothing
    is proposed for RULES.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .paired.csv, .episodes.csv,
.decay.csv, .walkforward.csv
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

STEM = "2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud"
OUT = ROOT / "research" / "backtests"
P175_STEM = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"

RUNGS = [0, 10, 25]
BASE_RUNG = 10
HORIZONS = [5, 10, 21, 30, 42, 63, 84]
PAIR = ("M", "6W")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


spec = importlib.util.spec_from_file_location("p175", OUT / f"{P175_STEM}.py")
p175 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p175)
p175.P = P

LADDER, CONST_PT = p175.LADDER, p175.CONST_PT
IS_END, OOS_START = p175.IS_END, p175.OOS_START
PHI, DELTA, EPS = p175.PHI, p175.DELTA, p175.EPS
INC_N, INC_GROSS = p175.INC_N, p175.INC_GROSS
FAMILIES = p175.FAMILIES
fast_backtest, cad_mask, family_of = p175.fast_backtest, p175.cad_mask, p175.family_of
tstat, sign_p = p175.tstat, p175.sign_p


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


def _rel_margin(x, sm):
    h1, h2 = _halves(x)
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


def _keep_4b(h1, h2, sh_oos, cagr, dd, sm, sh_spy_oos):
    s1, s2, ss, sd, sc = sm
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


# ------------------------------------------------------------------ holding-episode audit
def held_mask(px, weights, cad):
    """The book's actual holdings bar by bar: the target weights of the most recent
    rebalance, carried until the next one.  Same `reb`/`s0` construction fast_backtest uses,
    so this is the simulator's own holding indicator, not a re-derivation."""
    idx = px.index
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad).shift(1, fill_value=False).values.copy()
    mask[0] = True
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(len(idx)), side="right") - 1
    return wt[reb[seg]] > 1e-9, reb


def episode_stats(H, yrs):
    """Contiguous holding runs per name (idea 9's audit, vectorised)."""
    A = H.T.astype(np.int8)
    Ap = np.pad(A, ((0, 0), (1, 1)))
    d = np.diff(Ap, axis=1)
    si = np.argwhere(d == 1)
    ei = np.argwhere(d == -1)
    if len(si) == 0:
        return dict(episodes=0, per_year=0.0, mean_len=np.nan, median_len=np.nan,
                    frac_ge2=np.nan)
    lens = (ei[:, 1] - si[:, 1]).astype(float)
    return dict(episodes=int(len(lens)), per_year=len(lens) / yrs,
                mean_len=float(lens.mean()), median_len=float(np.median(lens)),
                frac_ge2=float((lens > 1).mean()))


# ------------------------------------------------------------------------- signal decay
def decay_curve(bk, window):
    """Cross-sectional rank IC of the composite against forward h-bar returns among ELIGIBLE
    names, and the realised top-20-minus-eligible-mean forward excess, at each horizon.
    Measured on `window` bars only.  Ranks are computed inside the eligible set each bar, so
    this is the discrimination the book actually uses, not a whole-panel correlation."""
    px = bk.px[bk.tradable]
    comp = bk.comp[bk.tradable].where(bk.elig[bk.tradable])
    sel = comp.rank(axis=1, ascending=False) <= INC_N
    m = window.reindex(px.index).fillna(False).values
    out = []
    for h in HORIZONS:
        fwd = px.shift(-h) / px - 1.0
        cr = comp.rank(axis=1, pct=True)
        fr = fwd.where(comp.notna()).rank(axis=1, pct=True)
        a, b = cr.values, fr.values
        ok = np.isfinite(a) & np.isfinite(b) & m[:, None]
        ic = []
        for t in range(len(px)):
            j = ok[t]
            if j.sum() >= 5:
                x, y = a[t, j], b[t, j]
                sx, sy = x.std(), y.std()
                if sx > 0 and sy > 0:
                    ic.append(float(((x - x.mean()) * (y - y.mean())).mean() / (sx * sy)))
        fw = fwd.values
        e_ok = np.isfinite(fw) & comp.notna().values & m[:, None]
        s_ok = e_ok & sel.values
        ex = []
        for t in range(len(px)):
            if s_ok[t].sum() >= 3 and e_ok[t].sum() >= 5:
                ex.append(float(np.nanmean(fw[t, s_ok[t]]) - np.nanmean(fw[t, e_ok[t]])))
        out.append(dict(h=h, n_bars=len(ic), IC=float(np.mean(ic)) if ic else np.nan,
                        IC_t=tstat(ic) if len(ic) > 2 else np.nan,
                        excess=float(np.mean(ex)) if ex else np.nan,
                        excess_ann=float(np.mean(ex)) * 252.0 / h if ex else np.nan))
    return pd.DataFrame(out)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 188  why-does-the-small-panel-want-M-and-the-large-caps-6W   (cloud, 2026-09-05)")
    P("=" * 118)
    P(f"ladder = {LADDER} | cost rungs = {RUNGS} bps | IS <= {IS_END}, OOS >= {OOS_START}")
    P(f"the pair under test: {PAIR[0]} (a calendar month) minus {PAIR[1]} (6 ISO weeks)")

    P("\nbuilding idea 175's corpus (its build_corpus, imported) ...")
    books, panels = p175.build_corpus()
    P(f"  {len(books)} books")

    P("\nREPRODUCTION CONTROLS (asserted before any new number is read)")
    ok = all([p175.check_a(books[1]), p175.check_b(books[1]), p175.check_c(books[1])])
    if not ok:
        P("\n*** REPRODUCTION FAILED -- not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    P("\n  [e] numpy metric kernels vs engine.metrics and idea 175's helpers:")
    de = dh = dm = 0.0
    for bk in books[:3]:
        for cd in ["D", "W", "M", "Q"]:
            r = fast_backtest(bk.px, bk.weights(), BASE_RUNG, cd)["returns"].iloc[260:]
            spy = bk.px["SPY"].pct_change().fillna(0.0).reindex(r.index).fillna(0.0)
            mm = metrics(r)
            c, s, d = _cagr_sh_dd(r.values)
            de = max(de, abs(c - mm["CAGR"]), abs(s - mm["Sharpe"]), abs(d - mm["MaxDD"]))
            h, hh = p175.halves(r), _halves(r.values)
            dh = max(dh, abs(h[0] - hh[0]), abs(h[1] - hh[1]))
            dm = max(dm, abs(p175.rel_margin(r, spy)[0] - _rel_margin(r.values, _spy_pack(spy.values))[0]))
    P(f"      max |dCAGR/dSharpe/dMaxDD| = {de:.3e} | halves {dh:.3e} | rel_margin {dm:.3e}"
      f"   -> {'PASS' if max(de, dh, dm) < 1e-12 else 'FAIL'}")
    if max(de, dh, dm) >= 1e-12:
        P("\n*** metric kernels do not reproduce engine.metrics.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    P("\n  [d] cost additivity: derived net(c) = gross - turnover*c/1e4  vs a DIRECT "
      "fast_backtest(cost=c) re-simulation")
    dadd = 0.0
    for bk in books[:3]:
        w = bk.weights()
        for cd in LADDER:
            z = fast_backtest(bk.px, w, 0.0, cd)
            for cb in RUNGS:
                direct = fast_backtest(bk.px, w, cb, cd)["returns"].values
                der = z["returns"].values - z["turnover"].values * cb / 1e4
                dadd = max(dadd, float(np.abs(direct - der).max()))
    P(f"      max |direct - derived| over 3 books x 7 cadences x 3 rungs = {dadd:.3e}"
      f"   -> {'PASS' if dadd < 1e-15 else 'FAIL'}")
    if dadd >= 1e-15:
        P("\n*** the derived cost axis is not an identity.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ------------------------------------------------------------------------- the ladder
    P("\nrunning the 7-point ladder (1 simulation per book x cadence, 3 rungs derived) ...")
    ctx = {}
    for b in books:
        if b.parent not in ctx:
            px = panels[b.parent]
            st = px.index[260]
            br = fast_backtest(px, rules_v1_weights(px), 0.0, "W")
            ctx[b.parent] = dict(st=st, spy=px["SPY"].pct_change().fillna(0.0).loc[st:],
                                 bg=br["returns"].loc[st:], bt=br["turnover"].loc[st:])

    rows, eprows = [], []
    for bi, bk in enumerate(books):
        c = ctx[bk.parent]
        idx = bk.px.index
        i0 = int(np.searchsorted(idx, c["st"]))
        widx = idx[i0:]
        is_n = int((widx <= pd.Timestamp(IS_END)).sum())
        oos_i = int(np.searchsorted(widx, pd.Timestamp(OOS_START)))
        spy = c["spy"].reindex(widx).fillna(0.0).values
        SM_F, SM_IS, SM_OOS = _spy_pack(spy), _spy_pack(spy[:is_n]), _spy_pack(spy[oos_i:])
        sh_spy_oos = _cagr_sh_dd(spy[oos_i:])[1]
        bg = c["bg"].reindex(widx).fillna(0.0).values
        bt = c["bt"].reindex(widx).fillna(0.0).values
        BASE = {}
        for cb in RUNGS:
            bn = bg - bt * cb / 1e4
            b1, b2 = _halves(bn)
            BASE[cb] = (b1, b2, _cagr_sh_dd(bn)[2])

        w = bk.weights()
        yrs = len(widx) / 252.0
        for cd in LADDER:
            res = fast_backtest(bk.px, w, 0.0, cd)
            g = res["returns"].values[i0:]
            tn = res["turnover"].values[i0:]
            tpy = tn.sum() / yrs
            H, reb = held_mask(bk.px, w, cd)
            es = episode_stats(H[i0:], yrs)
            reb_w = reb[reb >= i0]
            blk = (len(widx) / max(len(reb_w), 1))
            eprows.append(dict(book=bk.name, family=family_of(bk.name), parent=bk.parent,
                               cadence=cd, n_names=len(bk.tradable), turnover=tpy,
                               rebalances_per_year=len(reb_w) / yrs, block_bars=blk,
                               persistence=es["mean_len"] / blk if blk else np.nan, **es))
            for cb in RUNGS:
                r = g - tn * cb / 1e4
                cf, shf, ddf = _cagr_sh_dd(r)
                ci, shi, ddi = _cagr_sh_dd(r[:is_n])
                co, sho, ddo = _cagr_sh_dd(r[oos_i:])
                h1, h2 = _halves(r)
                mg_is, wb_is = _rel_margin(r[:is_n], SM_IS)
                mg_oos, wb_oos = _rel_margin(r[oos_i:], SM_OOS)
                b1, b2, bdd = BASE[cb]
                rows.append(dict(
                    book=bk.name, family=family_of(bk.name), parent=bk.parent, point=cd,
                    cost_bps=cb, is_incumbent=(cd == CONST_PT),
                    CAGR=cf, Sharpe=shf, MaxDD=ddf, H1=h1, H2=h2, turnover=tpy,
                    IS_Sharpe=shi, IS_CAGR=ci, IS_MaxDD=ddi, IS_margin=mg_is,
                    IS_worstbar=wb_is, OOS_Sharpe=sho, OOS_CAGR=co, OOS_MaxDD=ddo,
                    OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                    fail4a=_keep_4a(h1, h2, ddf, b1, b2, bdd),
                    fail4b=_keep_4b(h1, h2, sho, cf, ddf, SM_F, sh_spy_oos)))
        if (bi + 1) % 25 == 0:
            P(f"   ... {bi + 1}/{len(books)} books  ({time.time() - t0:.0f}s)")
    lad = pd.DataFrame(rows)
    eps = pd.DataFrame(eprows)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    eps.to_csv(OUT / f"{STEM}.episodes.csv", index=False)
    P(f"   {len(lad)} rung-rows = {len(lad)//len(RUNGS)} ladder points x {len(RUNGS)} rungs"
      f"  ({time.time() - t0:.0f}s)")

    # [c] the 10 bps rung must be idea 175's committed ladder
    C175 = pd.read_csv(OUT / f"{P175_STEM}.ladder.csv")
    m = lad[lad.cost_bps == BASE_RUNG].merge(C175, on=["book", "point"], suffixes=("", "_c"))
    P(f"\n  [c] derived {BASE_RUNG} bps rung vs idea 175's committed ladder.csv: "
      f"{len(m)}/{len(C175)} rows matched")
    dmax = 0.0
    for col in ["Sharpe", "CAGR", "MaxDD", "H1", "H2", "turnover", "IS_Sharpe", "IS_margin",
                "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_margin"]:
        d = float((m[col] - m[f"{col}_c"]).abs().max())
        dmax = max(dmax, d)
        P(f"      max |d{col}| = {d:.3e}")
    v4 = int((m["fail4a"] != m["fail4a_c"]).sum()) + int((m["fail4b"] != m["fail4b_c"]).sum())
    P(f"      4a/4b verdict mismatches: {v4}")
    repro = (len(m) == len(C175)) and dmax < 1e-12 and v4 == 0
    P(f"      -> {'PASS' if repro else 'FAIL'}")
    if not repro:
        P("\n*** idea 175's ladder does not reproduce.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ------------------------------------------------------- Q2/Q3 the gap, cost vs signal
    P("\n" + "=" * 118)
    P("Q2/Q3  THE M-minus-6W GAP AT 0 / 10 / 25 bps.  0 bps is the PURE SIGNAL effect; "
      "(10 - 0) is the PURE COST effect.")
    P("=" * 118)
    prows = []
    for score in ["Sharpe", "OOS_Sharpe", "CAGR", "OOS_CAGR"]:
        for fam in ["ALL"] + FAMILIES:
            for cb in RUNGS:
                s = lad[lad.cost_bps == cb]
                s = s if fam == "ALL" else s[s.family == fam]
                a = s[s.point == PAIR[0]].set_index("book")[score]
                b = s[s.point == PAIR[1]].set_index("book")[score]
                d = (a - b.reindex(a.index)).dropna()
                p, wn, ls = sign_p(d.values)
                prows.append(dict(score=score, family=fam, cost_bps=cb, n=len(d),
                                  mean_d=float(d.mean()), median_d=float(d.median()),
                                  t=tstat(d.values), wins=wn, losses=ls, sign_p=p,
                                  mean_M=float(a.mean()), mean_6W=float(b.mean())))
    paired = pd.DataFrame(prows)
    paired.to_csv(OUT / f"{STEM}.paired.csv", index=False)

    for score in ["Sharpe", "OOS_Sharpe"]:
        P(f"\nM minus 6W, paired over books   score = {score}")
        P(f"  {'family':<7s} {'n':>4s} " + " ".join(f"{str(c) + 'bps':>22s}" for c in RUNGS)
          + f" {'cost effect (10-0)':>20s}")
        for fam in ["ALL"] + FAMILIES:
            cells = []
            for cb in RUNGS:
                r = paired[(paired.score == score) & (paired.family == fam)
                           & (paired.cost_bps == cb)].iloc[0]
                cells.append(f"{r['mean_d']:+.4f} t{r['t']:+6.2f} {r['wins']:>3d}W")
            n = int(paired[(paired.score == score) & (paired.family == fam)].iloc[0]["n"])
            z = paired[(paired.score == score) & (paired.family == fam)]
            ce = (float(z[z.cost_bps == 10]["mean_d"].iloc[0])
                  - float(z[z.cost_bps == 0]["mean_d"].iloc[0]))
            P(f"  {fam:<7s} {n:>4d} " + " ".join(f"{c:>22s}" for c in cells)
              + f" {ce:>+20.4f}")

    P("\nthe LEVELS behind the gap (mean over books), full-sample Sharpe")
    P(f"  {'family':<7s} {'bps':>4s} " + " ".join(f"{p:>9s}" for p in LADDER) + f" {'argmax':>8s}")
    for fam in ["ALL"] + FAMILIES:
        for cb in RUNGS:
            s = lad[lad.cost_bps == cb]
            s = s if fam == "ALL" else s[s.family == fam]
            g = s.groupby("point")["Sharpe"].mean().reindex(LADDER)
            P(f"  {fam:<7s} {cb:>4d} " + " ".join(f"{g[p]:>9.4f}" for p in LADDER)
              + f" {g.idxmax():>8s}")
    P("\nsame, OOS Sharpe (2017-01-01 onward, read once)")
    P(f"  {'family':<7s} {'bps':>4s} " + " ".join(f"{p:>9s}" for p in LADDER) + f" {'argmax':>8s}")
    for fam in ["ALL"] + FAMILIES:
        for cb in RUNGS:
            s = lad[lad.cost_bps == cb]
            s = s if fam == "ALL" else s[s.family == fam]
            g = s.groupby("point")["OOS_Sharpe"].mean().reindex(LADDER)
            P(f"  {fam:<7s} {cb:>4d} " + " ".join(f"{g[p]:>9.4f}" for p in LADDER)
              + f" {g.idxmax():>8s}")

    # --------------------------------------------------------------- Q4 holding episodes
    P("\n" + "=" * 118)
    P("Q4  HOLDING-EPISODE LENGTH (idea 76 / idea 9's instrument).  persistence = mean "
      "episode length / cadence block length.")
    P("    persistence ~ 1 => the book re-picks from scratch every block; >> 1 => names "
      "survive rebalances and the dial barely moves the book.")
    P("=" * 118)
    P(f"  {'family':<7s} {'cad':>4s} {'blk bars':>9s} {'reb/yr':>7s} {'ep/yr':>9s} "
      f"{'mean ep':>8s} {'med ep':>7s} {'persist':>8s} {'turn/yr':>8s}")
    for fam in FAMILIES:
        for cd in LADDER:
            s = eps[(eps.family == fam) & (eps.cadence == cd)]
            P(f"  {fam:<7s} {cd:>4s} {s['block_bars'].mean():>9.2f} "
              f"{s['rebalances_per_year'].mean():>7.1f} {s['per_year'].mean():>9.1f} "
              f"{s['mean_len'].mean():>8.2f} {s['median_len'].mean():>7.2f} "
              f"{s['persistence'].mean():>8.3f} {s['turnover'].mean():>8.2f}")
    P("\nthe M vs 6W cells only, fixed panels (no sub-panel averaging)")
    P(f"  {'book':<10s} {'cad':>4s} {'blk bars':>9s} {'mean ep':>8s} {'persist':>8s} "
      f"{'ep/yr':>9s} {'turn/yr':>8s}")
    for nm in ["SMALL439", "U56", "ETF36"]:
        for cd in PAIR:
            s = eps[(eps.book == nm) & (eps.cadence == cd)].iloc[0]
            P(f"  {nm:<10s} {cd:>4s} {s['block_bars']:>9.2f} {s['mean_len']:>8.2f} "
              f"{s['persistence']:>8.3f} {s['per_year']:>9.1f} {s['turnover']:>8.2f}")

    # ------------------------------------------------------------------ Q5 signal decay
    P("\n" + "=" * 118)
    P("Q5  REALISED SIGNAL DECAY per panel.  rank IC of the composite vs forward h-bar "
      "returns, among ELIGIBLE names.")
    P("    IC(30)/IC(21) is the M-vs-6W question stated as a decay ratio.  LEVELS are "
      "survivorship-inflated; read the SHAPE (see caveats).")
    P("=" * 118)
    drows = []
    for nm in ["SMALL439", "U56", "ETF36"]:
        bk = [b for b in books if b.name == nm][0]
        full = pd.Series(True, index=bk.px.index)
        st = ctx[bk.parent]["st"]
        full.loc[:st] = False
        for wname, wmask in [("FULL", full),
                             ("IS", full & (bk.px.index <= pd.Timestamp(IS_END))),
                             ("OOS", full & (bk.px.index >= pd.Timestamp(OOS_START)))]:
            dc = decay_curve(bk, wmask)
            dc.insert(0, "window", wname)
            dc.insert(0, "panel", nm)
            drows.append(dc)
    decay = pd.concat(drows, ignore_index=True)
    decay.to_csv(OUT / f"{STEM}.decay.csv", index=False)
    for wname in ["FULL", "IS", "OOS"]:
        P(f"\nwindow = {wname}   rank IC by horizon (bars)")
        P(f"  {'panel':<10s} " + " ".join(f"{'h=' + str(h):>9s}" for h in HORIZONS)
          + f" {'IC(30)/IC(21)':>14s}")
        for nm in ["SMALL439", "U56", "ETF36"]:
            s = decay[(decay.panel == nm) & (decay.window == wname)].set_index("h")
            rt = s.loc[30, "IC"] / s.loc[21, "IC"] if s.loc[21, "IC"] else np.nan
            P(f"  {nm:<10s} " + " ".join(f"{s.loc[h, 'IC']:>9.4f}" for h in HORIZONS)
              + f" {rt:>14.4f}")
        P(f"  {'panel':<10s} " + " ".join(f"{'h=' + str(h):>9s}" for h in HORIZONS)
          + f" {'top20 excess, annualised':>26s}")
        for nm in ["SMALL439", "U56", "ETF36"]:
            s = decay[(decay.panel == nm) & (decay.window == wname)].set_index("h")
            P(f"  {nm:<10s} " + " ".join(f"{s.loc[h, 'excess_ann']:>9.2%}" for h in HORIZONS))

    # ----------------------------------------------------------- Q6 rule 8 + KEEP paths
    P("\n" + "=" * 118)
    P("Q6  RULE 8 WALK-FORWARD.  Every arm chooses on IS <= 2016-12-31 ONLY; 2017-2026 read "
      "once.  ORACLE is not implementable.")
    P("=" * 118)
    wrows = []
    for fam in ["ALL"] + FAMILIES:
        for cb in RUNGS:
            s = lad[lad.cost_bps == cb]
            s = s if fam == "ALL" else s[s.family == fam]
            bl = sorted(set(s.book))
            arms = {"CONST-W": None, "CONST-M": None, "CONST-6W": None,
                    "SEL-SHARPE": None, "SEL-4B": None, "ORACLE": None}
            for arm in arms:
                acc = {k: [] for k in ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_margin"]}
                p4a = p4b = 0
                for b in bl:
                    sb = s[s.book == b].set_index("point").reindex(LADDER)
                    if arm == "CONST-W":      pt = "W"
                    elif arm == "CONST-M":    pt = "M"
                    elif arm == "CONST-6W":   pt = "6W"
                    elif arm == "SEL-SHARPE": pt = sb["IS_Sharpe"].idxmax()
                    elif arm == "SEL-4B":     pt = sb["IS_margin"].idxmax()
                    else:                     pt = sb["OOS_Sharpe"].idxmax()
                    r = sb.loc[pt]
                    for k in acc:
                        acc[k].append(r[k])
                    p4a += r["fail4a"] == "-"
                    p4b += r["fail4b"] == "-"
                wrows.append(dict(family=fam, cost_bps=cb, arm=arm, n=len(bl),
                                  **{k: float(np.nanmean(v)) for k, v in acc.items()},
                                  pass4a=p4a, pass4b=p4b))
    wf = pd.DataFrame(wrows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    ARMS = ["CONST-W", "CONST-M", "CONST-6W", "SEL-SHARPE", "SEL-4B", "ORACLE"]
    for fam in ["ALL"] + FAMILIES:
        P(f"\npooled OOS by arm -- family {fam}")
        P(f"  {'arm':<11s} " + " ".join(f"{str(c) + 'bps Sharpe':>17s}" for c in RUNGS)
          + f" {'OOS CAGR@10':>12s} {'OOS MaxDD@10':>13s} {'4b@10':>7s}")
        for arm in ARMS:
            v = [float(wf[(wf.family == fam) & (wf.cost_bps == cb) & (wf.arm == arm)]["OOS_Sharpe"].iloc[0])
                 for cb in RUNGS]
            r10 = wf[(wf.family == fam) & (wf.cost_bps == 10) & (wf.arm == arm)].iloc[0]
            P(f"  {arm:<11s} " + " ".join(f"{x:>17.4f}" for x in v)
              + f" {r10['OOS_CAGR']:>12.2%} {r10['OOS_MaxDD']:>13.2%} "
                f"{int(r10['pass4b'])}/{int(r10['n'])}".rjust(8))

    P("\nreferences on the OOS window, per parent panel")
    P(f"  {'panel':<8s} {'series':<14s} {'bps':>4s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s}")
    refrows = []
    for par, px in panels.items():
        st = px.index[260]
        c, s, d = _cagr_sh_dd(px["SPY"].pct_change().fillna(0.0).loc[st:].loc[OOS_START:].values)
        refrows.append(dict(panel=par, series="SPY", cost_bps=np.nan, CAGR=c, Sharpe=s, MaxDD=d))
        P(f"  {par:<8s} {'SPY buy&hold':<14s} {'-':>4s} {c:>8.2%} {s:>8.4f} {d:>8.2%}")
        br = fast_backtest(px, rules_v1_weights(px), 0.0, "W")
        bg = br["returns"].loc[st:].loc[OOS_START:].values
        bt = br["turnover"].loc[st:].loc[OOS_START:].values
        for cb in RUNGS:
            c, s, d = _cagr_sh_dd(bg - bt * cb / 1e4)
            refrows.append(dict(panel=par, series="RULES v1", cost_bps=cb, CAGR=c, Sharpe=s,
                                MaxDD=d))
            P(f"  {par:<8s} {'RULES v1':<14s} {cb:>4d} {c:>8.2%} {s:>8.4f} {d:>8.2%}")
    pd.DataFrame(refrows).to_csv(OUT / f"{STEM}.refs.csv", index=False)

    P("\nBOTH KEEP PATHS on all ladder rows (4a vs each panel's own RULES v1 at the same rung; "
      "4b vs SPY)")
    P(f"  {'bps':>4s} {'rows':>6s} {'4a':>6s} {'4b':>6s} | fixed-panel 4b by book")
    for cb in RUNGS:
        s = lad[lad.cost_bps == cb]
        fx = " ".join(f"{nm}:{int((s[(s.book == nm)].fail4b == '-').sum())}/{len(LADDER)}"
                      for nm in ["SMALL439", "U56", "ETF36"])
        P(f"  {cb:>4d} {len(s):>6d} {int((s.fail4a == '-').sum()):>6d} "
          f"{int((s.fail4b == '-').sum()):>6d} | {fx}")

    # ------------------------------------------------------------------------ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)

    def gap(fam, cb, score="Sharpe"):
        return float(paired[(paired.score == score) & (paired.family == fam)
                            & (paired.cost_bps == cb)]["mean_d"].iloc[0])

    p3 = gap("SMALL", 0) > 0
    signs = [(gap("SMALL", cb) > 0) and (gap("U56", cb) < 0) and (gap("ETF", cb) < 0)
             for cb in RUNGS]
    p4 = all(signs)
    dF = decay[decay.window == "FULL"].set_index(["panel", "h"])
    rat = {nm: float(dF.loc[(nm, 30), "IC"] / dF.loc[(nm, 21), "IC"])
           for nm in ["SMALL439", "U56", "ETF36"]}
    p5 = rat["SMALL439"] < rat["U56"]
    pers = {(nm, cd): float(eps[(eps.book == nm) & (eps.cadence == cd)]["persistence"].iloc[0])
            for nm in ["SMALL439", "U56", "ETF36"] for cd in PAIR}
    p6 = pers[("SMALL439", "M")] < pers[("U56", "M")]
    fixed4b = {cb: int((lad[(lad.cost_bps == cb)
                            & (lad.book.isin(["SMALL439", "U56", "ETF36"]))].fail4b == "-").sum())
               for cb in RUNGS}
    preds = [
        ("P1 idea 175's 805-row ladder reproduces", repro, f"{dmax:.1e}, {v4} mismatches"),
        ("P2 cost additivity < 1e-15", dadd < 1e-15, f"{dadd:.3e}"),
        ("P3 SMALL's M-6W gap is still positive at 0 bps", p3, f"{gap('SMALL', 0):+.4f}"),
        ("P4 sign split holds at all 3 rungs (SMALL +, U56 -, ETF -)", p4,
         " ".join(f"{cb}bps:{'Y' if s else 'N'}" for cb, s in zip(RUNGS, signs))),
        ("P5 IC(30)/IC(21) smaller on SMALL than U56", p5,
         " ".join(f"{k}:{v:.3f}" for k, v in rat.items())),
        ("P6 persistence at M lower on SMALL439 than U56", p6,
         f"SMALL {pers[('SMALL439', 'M')]:.3f} vs U56 {pers[('U56', 'M')]:.3f}"),
        ("P7 no fixed-panel 4b pass at any rung", sum(fixed4b.values()) == 0, str(fixed4b)),
    ]
    for nm, hit, det in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {nm:<58s} {det}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
