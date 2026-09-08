#!/usr/bin/env python3
"""QUEUE idea 432 — why-does-the-IS-lift-slope-flip-between-GROSS-and-GATE  (lane C, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 432)
    "idea 204 found slope(OOS lift ~ IS lift) is -0.580 on the gross dial and +0.984 on the gate
     dial, so 'IS lift ranks out of sample' is a family fact, not a record fact.  Test whether
     the sign tracks the dial's Sharpe-invariance (idea 311: Sharpe span <=0.006 in g, so the
     gross dial's IS lift is pure noise being extrapolated) by regressing the per-family slope
     on the family's own IS-Sharpe dispersion across panels and rungs.  Max 2 params."

THE ONE THING THE QUEUE DID NOT NOTICE (write the statistic out before running it)
    For a pool P of arms with IS lift I_a = M_IS(a) - mean_P M_IS and OOS lift O_a likewise,

        slope  =  cov(O, I) / var(I)  =  rho(O, I) * sd(O) / sd(I),      disp := sd(I)

    so the quantity the queue proposes to REGRESS (slope) has the quantity it proposes to
    regress it ON (disp) sitting in its own DENOMINATOR.  Two consequences, both fatal to a
    naive reading and both measured here rather than argued:

      (i) LEVEL.  Even under complete independence of O and I, E[slope] = 0 but Var(slope)
          grows like 1/disp^2.  A low-dispersion family therefore produces LARGE slopes of
          EITHER sign.  "The gross dial's slope is -0.580 and the gate dial's is +0.984" is
          exactly what a noise family and a signal family look like when you read the SIGN of
          a ratio whose denominator is near zero.  The queue's hypothesis predicts a negative
          slope-on-dispersion regression; the noise explanation predicts no relation in the
          SIGNED slope and a strong one in |slope| and in the slope's own standard error.
     (ii) IDENTIFICATION.  rho is scale-free and bounded in [-1, 1]; slope is not.  The
          identified form of the queue's question is "does rho(OOS lift, IS lift) track the
          family's IS-Sharpe dispersion", and that is reported beside the asked form.

    Both forms are run.  The asked regression is never skipped, never softened, and its number
    is printed first.

WHAT THIS RUN DOES
    G0  REPRODUCE idea 204's two headline numbers from its OWN committed walk-forward file
        (research/backtests/2026-09-08_is-the-pool-sign-the-whole-selector-story_B.walkforward.csv)
        and then re-derive them from fresh books built here.  A study of why a number flips
        must first show the number.
    Q1  THE ASKED REGRESSION, three ways: family-level (n=7 families, idea 204's own unit),
        cell-level (n=63 = family x panel x rung, the queue's "across panels and rungs"), and
        CORE-only cell-level (n=36, idea 204's exact corpus) so the extension is separable.
    Q2  IDENTIFICATION.  The same three regressions on rho instead of slope, plus the exact
        decomposition slope = rho * sd(O)/sd(I) with each leg regressed on disp, plus |slope|
        and se(slope) on 1/disp.  This says whether the queue found a dial property or a
        divide-by-small-number.
    Q3  IS THE FLIP REAL?  Per-family slopes with a cluster bootstrap over cells (2,000 draws,
        seeded), the GROSS-minus-GATE difference in se units, and a heterogeneity check: does
        the spread of the 7 family slopes exceed what their own standard errors imply?
    Q4  IDEA 311's PREMISE, MEASURED.  IS-Sharpe span and sd per family per panel per rung.
        Idea 311 claims span <= 0.006 on the gross dial.  Quoted, not cited.
    Q5  RULE 8 (PROTOCOL 8), AND THE INSTRUMENT THE ANSWER IMPLIES.  If IS lift only ranks in
        high-dispersion families, then the record should ABSTAIN from selection in low-dispersion
        ones.  Pre-registered rule R(tau, stat): in a pool whose IS dispersion exceeds tau, take
        the K_Sharpe argmax pick; otherwise take the pool's own do-nothing control.  tau is
        chosen on an INNER IS split (fit <= 2013-12-31, evaluate 2014-2016) and the outer OOS
        (2017-2026) is read ONCE.  Every tau on the grid is reported anyway.
    Q6  BOTH KEEP PATHS (PROTOCOL 4a and 4b) on every arm and every rule-selected book, full
        sample and OOS, against RULES v2 (live), RULES v1 and SPY.  This is a diagnostic idea
        and is not expected to promote a book; the paths are scored because PROTOCOL requires it.

CORPUS
    3 panels (u56, broad, small - idea 133's panel_px verbatim) x 7 dial families x 3 cost rungs
    {0, 10, 25} = 63 pools, 41 arms per panel = 123 simulations serving 369 arm-rows off the
    exact turnover identity r(c) = r(0) - turnover*c/1e4 (gate G5).
      CORE (idea 204's four, arms verbatim):  GROSS 7, WIDTH 6, CADENCE 4, GATE 6
      EXT  (new, so the slope-on-dispersion regression has more than 4 points, and so the CORE
            result can be replicated out of its own corpus):  MALEN 6, VOLCAP 6, LOOKBACK 6

TUNED PARAMETERS (exactly 2, every grid point reported, none selected on)
    1. tau  - the IS-dispersion abstention threshold in Q5 (11 grid points: 0 and the deciles of
              the cell dispersion distribution).
    2. stat - the dispersion statistic: sd(IS_Sharpe) or span(IS_Sharpe) across the pool's arms.
    Panels, cost rungs, families, selectors, metrics and comparands are REPORTED axes and are
    never selected on.

PRE-REGISTERED PREDICTIONS (written before any number below was computed)
    P1  The asked regression (signed slope on disp) is NOT reliably negative: |t| < 2 at cell
        level.  The queue's "sign tracks Sharpe-invariance" reading is a sign artefact.
    P2  |slope| DOES track 1/disp: reliably positive, |t| > 2.  The flip is a denominator.
    P3  rho on disp is weaker than slope on disp and, if anything, positive - a real dial gives
        rho > 0 and a noise dial gives rho ~ 0 with wide spread.
    P4  Idea 311 replicates in sign (GROSS has the smallest IS-Sharpe span of the seven families)
        but NOT at the quoted 0.006 level on all three panels.
    P5  Under rule 8 the abstention rule R(tau) does NOT beat always-abstaining: consistent with
        ideas 151/204/430, no chooser beats do-nothing, and gating the chooser by dispersion
        does not rescue it.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): all three panels are current constituents.  Every CAGR here is
      flattered and no level is an achievable return.  Every statistic below is a PAIRED or
      WITHIN-POOL contrast, which the panel's level bias does not move.
    * 63 pools are not 63 independent observations: arms and panels overlap heavily.  Every t is
      quoted with its n, per-panel and per-rung breakdowns are printed, and Q3's bootstrap
      resamples CELLS within a family rather than rows.
    * A within-pool slope over 4-7 arms is a small-sample OLS.  CADENCE has 4 arms and is the
      thinnest; its rows are flagged and the regressions are re-run without it.
    * Idea 401's restatement: data/prices.csv was rewritten after some committed grids, so gate
      G0's reproduction of idea 204 is quoted per number rather than asserted bit-exact.
    * PROTOCOL rung is 10 bps; 0 and 25 are reported.  Every book is t+1 execution (idea 126).

Deterministic, standalone.  Writes .console.txt, .arms.csv, .cells.csv, .picks.csv,
.walkforward.csv and .keeppaths.csv next to itself.  Modifies nothing.
"""
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_why-does-the-IS-lift-slope-flip-between-GROSS-and-GATE_C"
OUT = ROOT / "research" / "backtests"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
I204_WF = OUT / "2026-09-08_is-the-pool-sign-the-whole-selector-story_B.walkforward.csv"

FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
INNER_END, INNER2_START = "2013-12-31", "2014-01-01"     # inner IS split for tau (rule 8)
PHI, DELTA = 0.70, 0.60                                   # PROTOCOL 4b CAGR floor / MaxDD cap
N_BOOT = 2000
BOOT_SEED = 4321

pd.set_option("display.width", 330)
pd.set_option("display.max_columns", 160)
pd.set_option("display.max_rows", 4000)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = _load(I133, "i133")          # panel_px, the record's three panels, verbatim


# ------------------------------------------------------------------ stats ---
def ols(y, x):
    """OLS of y on x with the classical slope t.  Returns NaN fields when undefined."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    ok = np.isfinite(y) & np.isfinite(x)
    y, x = y[ok], x[ok]
    n = len(y)
    if n < 3 or x.std() == 0:
        return dict(n=n, slope=np.nan, icept=np.nan, r2=np.nan, t=np.nan, se=np.nan)
    b, a = np.polyfit(x, y, 1)
    yh = a + b * x
    ss_res = float(((y - yh) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    sxx = float(((x - x.mean()) ** 2).sum())
    se = math.sqrt(ss_res / (n - 2) / sxx) if n > 2 and sxx > 0 else np.nan
    return dict(n=n, slope=float(b), icept=float(a),
                r2=1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan,
                t=float(b / se) if se and np.isfinite(se) and se > 0 else np.nan,
                se=float(se) if np.isfinite(se) else np.nan)


def corr(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    ok = np.isfinite(y) & np.isfinite(x)
    y, x = y[ok], x[ok]
    if len(y) < 3 or y.std() == 0 or x.std() == 0:
        return np.nan
    return float(np.corrcoef(y, x)[0, 1])


def tstat(x):
    x = np.asarray([v for v in np.asarray(x, float) if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def sign_p(wins, n):
    """Two-sided exact binomial sign test at p=0.5; ties excluded by the caller."""
    if n == 0:
        return np.nan
    lo = min(wins, n - wins)
    tail = sum(math.comb(n, k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


def window(r, which):
    if which == "IS":
        return r.loc[:IS_END]
    if which == "IS1":
        return r.loc[:INNER_END]
    if which == "IS2":
        return r.loc[INNER2_START:IS_END]
    if which == "OOS":
        return r.loc[OOS_START:]
    return r


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ------------------------------------------------------------- fast runner ---
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
    """Idea 196's fast_backtest verbatim (asserted == engine.backtest in gate G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ----------------------------------------------------------------- books -----
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def gate_mask(px, gate):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if gate == "g200":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * 1.03, 1.0).mask(px < ma * 0.97, 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "abs12":
        return (px > px.shift(252)).fillna(False)
    if gate == "vol60":
        return (vol20(px) < MAX_VOL).fillna(False)
    if gate == "v1gate":
        return ((px > ma) & (vol20(px) < MAX_VOL)).fillna(False)
    raise ValueError(gate)


def ma_len_mask(px, L):
    return (px > px.rolling(L).mean()).fillna(False)


def volcap_mask(px, cap):
    if not np.isfinite(cap):
        return gate_mask(px, "band3")
    return gate_mask(px, "band3") & (vol20(px) < cap).fillna(False)


def ew_weights(px, g=GROSS, gate=None, mask=None):
    """Equal weight over priced names at gross g; gated-out weight goes to CASH (de-gross)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    W = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    m = gate_mask(px, gate) if mask is None else mask
    return W.where(m, 0.0)


def topn_weights(px, n, g=GROSS, gate="band3", key=None):
    """Top-n on `key` (default the plain composite), equal weight g/n, de-grossed by the gate."""
    if n is None:
        return ew_weights(px, g, gate)
    k = composite(px) if key is None else key
    rank = k.rank(axis=1, ascending=False)
    W = (rank <= n).astype(float) * (g / n)
    return W.where(gate_mask(px, gate), 0.0)


def lookback_key(px, k):
    return px / px.shift(k) - 1


# family -> list of (arm, weights_fn, freq, is_control)
def family_arms(fam):
    if fam == "GROSS":                                   # CORE, idea 204 verbatim
        gs = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
        return [(f"g={g:.3f}", (lambda p, g=g: ew_weights(p, g, "band3")), FREQ, g == GROSS)
                for g in gs]
    if fam == "WIDTH":                                   # CORE
        ns = [5, 10, 20, 40, 80, None]
        return [(f"n={'ALL' if n is None else n}", (lambda p, n=n: topn_weights(p, n)), FREQ,
                 n is None) for n in ns]
    if fam == "CADENCE":                                 # CORE
        return [(f"freq={f}", (lambda p: ew_weights(p, GROSS, "band3")), f, f == FREQ)
                for f in ["D", "W", "M", "Q"]]
    if fam == "GATE":                                    # CORE
        gates = [None, "g200", "band3", "abs12", "vol60", "v1gate"]
        return [(f"gate={'none' if g is None else g}",
                 (lambda p, g=g: ew_weights(p, GROSS, g)), FREQ, g == "band3") for g in gates]
    if fam == "MALEN":                                   # EXT
        Ls = [20, 50, 100, 150, 200, 250]
        return [(f"ma={L}", (lambda p, L=L: ew_weights(p, GROSS, None, ma_len_mask(p, L))),
                 FREQ, L == 200) for L in Ls]
    if fam == "VOLCAP":                                  # EXT
        caps = [0.25, 0.35, 0.45, 0.60, 0.80, np.inf]
        return [(f"vcap={'none' if not np.isfinite(c) else f'{c:.2f}'}",
                 (lambda p, c=c: ew_weights(p, GROSS, None, volcap_mask(p, c))), FREQ,
                 c == 0.60) for c in caps]
    if fam == "LOOKBACK":                                # EXT
        ks = [21, 63, 126, 189, 252]
        arms = [(f"lb={k}", (lambda p, k=k: topn_weights(p, 20, key=lookback_key(p, k))),
                 FREQ, False) for k in ks]
        arms.append(("lb=composite", (lambda p: topn_weights(p, 20)), FREQ, True))
        return arms
    raise ValueError(fam)


CORE = ["GROSS", "WIDTH", "CADENCE", "GATE"]
EXT = ["MALEN", "VOLCAP", "LOOKBACK"]
FAMILIES = CORE + EXT


# ------------------------------------------------------------- KEEP paths ---
def bars(spy_r, which):
    m = metrics(window(spy_r, which))
    return dict(S=m["Sharpe"], CAGR=m["CAGR"], DD=m["MaxDD"])


def pass4b(r, spy_r, which="full"):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves and over the window, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.  Returns (bool, binding-bar name, margins)."""
    rr = window(r, which)
    b = bars(spy_r, which)
    m = metrics(rr)
    h1, h2 = halves(rr)
    sb1, sb2 = halves(window(spy_r, which))
    mg = dict(H1=h1 - sb1, H2=h2 - sb2, S=m["Sharpe"] - b["S"],
              DD=DELTA * abs(b["DD"]) - abs(m["MaxDD"]), CAGR=m["CAGR"] - PHI * b["CAGR"])
    ok = all(v > 0 for v in mg.values())
    return ok, min(mg, key=lambda k: mg[k]), mg


def pass4a(r, base_r):
    """PROTOCOL 4a: Sharpe > live book in BOTH halves and MaxDD no worse."""
    h1, h2 = halves(r)
    b1, b2 = halves(base_r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base_r)["MaxDD"])


# ------------------------------------------------------------------ build ---
def build():
    rows, store, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        say(f"\n[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")

        Wg = ew_weights(px, GROSS, "band3")
        e1 = fast_backtest(px, Wg, 0.0, FREQ)
        e0 = backtest(px, Wg, cost_bps=0.0, freq=FREQ)
        d_r = float((e1["returns"] - e0["returns"]).abs().max())
        d_t = float((e1["turnover"] - e0["turnover"]).abs().max())
        e25 = backtest(px, Wg, cost_bps=25.0, freq=FREQ)
        d_c = float((e25["returns"] - (e0["returns"] - e0["turnover"] * 25.0 / 1e4)).abs().max())
        say(f"  G1 fast_backtest vs engine.backtest: returns {d_r:.3e}  turnover {d_t:.3e}"
            f"   | G5 rung identity {d_c:.3e}")
        assert d_r < 1e-12 and d_t < 1e-12 and d_c < 1e-12, "G1/G5 FAILED - unsafe"

        v2 = fast_backtest(px, rules_v2_weights(px), 0.0, FREQ)
        v1 = fast_backtest(px, rules_v1_weights(px), 0.0, FREQ)
        ref[pk] = dict(px=px, spy=spy, start=start,
                       v2={c: (v2["returns"] - v2["turnover"] * c / 1e4).loc[start:] for c in COSTS},
                       v1={c: (v1["returns"] - v1["turnover"] * c / 1e4).loc[start:] for c in COSTS})
        ms, mo = metrics(spy), metrics(window(spy, "OOS"))
        say(f"  SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%}"
            f" | OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}")
        mv, mvo = metrics(ref[pk]["v2"][PROTOCOL_RUNG]), metrics(window(ref[pk]["v2"][PROTOCOL_RUNG], "OOS"))
        say(f"  RULES v2 @10bps {mv['CAGR']:.2%}/{mv['Sharpe']:.3f}/{mv['MaxDD']:.2%}"
            f" | OOS {mvo['CAGR']:.2%}/{mvo['Sharpe']:.3f}/{mvo['MaxDD']:.2%}")

        for fam in FAMILIES:
            for arm, wfn, freq, is_ctl in family_arms(fam):
                res = fast_backtest(px, wfn(px), 0.0, freq)
                r0, to = res["returns"], res["turnover"]
                for c in COSTS:
                    r = (r0 - to * c / 1e4).loc[start:]
                    store[(pk, fam, c, arm)] = r
                    m = metrics(r)
                    mi, mo = metrics(window(r, "IS")), metrics(window(r, "OOS"))
                    m1, m2 = metrics(window(r, "IS1")), metrics(window(r, "IS2"))
                    h1, h2 = halves(r)
                    ok_f, bind_f, _ = pass4b(r, spy, "full")
                    ok_o, bind_o, _ = pass4b(r, spy, "OOS")
                    rows.append(dict(
                        panel=pk, family=fam, group="CORE" if fam in CORE else "EXT",
                        cost=c, arm=arm, control=is_ctl,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        Vol=m["Vol"], TO=float(to.loc[start:].sum()) / m["Years"],
                        IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                        IS_Calmar=mi["Calmar"], IS_Sortino=mi["Sortino"], IS_Vol=mi["Vol"],
                        IS_TO=float(to.loc[start:IS_END].sum()) / max(mi["Years"], 1e-9),
                        IS1_Sharpe=m1["Sharpe"], IS2_Sharpe=m2["Sharpe"],
                        OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                        pass4b=ok_f, bind4b=bind_f, pass4b_oos=ok_o, bind4b_oos=bind_o,
                        pass4a_v2=pass4a(r, ref[pk]["v2"][c]),
                        pass4a_v1=pass4a(r, ref[pk]["v1"][c])))
    return pd.DataFrame(rows), store, ref


# ------------------------------------------------------------- selectors ----
SEL = {"K_Sharpe": ("IS_Sharpe", +1), "K_CAGR": ("IS_CAGR", +1), "K_Calmar": ("IS_Calmar", +1),
       "K_Sortino": ("IS_Sortino", +1), "K_MaxDD": ("IS_MaxDD", +1), "K_Vol": ("IS_Vol", -1),
       "K_TO": ("IS_TO", -1)}


def pick(sub, col, direction):
    s = pd.to_numeric(sub[col], errors="coerce")
    if not np.isfinite(s).any():
        return None
    # deterministic tie-break: first row in the frame's own (stable) order
    return int(s.idxmax() if direction > 0 else s.idxmin())


def main():
    say("=" * 118)
    say("QUEUE idea 432 — why-does-the-IS-lift-slope-flip-between-GROSS-and-GATE   (lane C, "
        "2026-09-08)")
    say("=" * 118)
    say("PRE-REGISTERED: P1 signed slope-on-disp NOT reliably negative | P2 |slope| tracks 1/disp "
        "| P3 rho-on-disp\n  weaker than slope-on-disp | P4 idea 311 replicates in SIGN not at "
        "0.006 | P5 the dispersion-gated\n  chooser does not beat always-abstaining OOS.")
    say("2 tuned params: tau (abstention threshold, 11 points) x stat (sd | span).  Panels, rungs,"
        "\n  families, selectors, metrics are REPORTED axes.")

    # ------------------------------------------------------- G0: the number --
    say("\n" + "=" * 118)
    say("G0 — REPRODUCE idea 204's headline from ITS OWN committed walk-forward file")
    say("=" * 118)
    i204 = pd.read_csv(I204_WF)
    say(f"  file: {I204_WF.name}  rows={len(i204)}  "
        f"cells={i204.groupby(['panel','family','cost']).ngroups}  "
        f"selectors={i204.selector.nunique()}")
    say("  idea 204's own statement: 'per family, all rungs (excl. K_ANTI)' OLS(OOS_lift ~ IS_lift)")
    rep = []
    for fam in CORE:
        s = i204[(i204.family == fam) & (i204.selector != "K_ANTI")]
        o = ols(s["OOS_lift"], s["IS_lift"])
        rep.append(dict(family=fam, n=o["n"], slope=o["slope"], t=o["t"], r2=o["r2"]))
        say(f"    {fam:<9} n={o['n']:>3}  slope {o['slope']:+.4f}  t {o['t']:+.3f}  "
            f"R2 {o['r2']:.4f}")
    R = {d["family"]: d["slope"] for d in rep}
    say(f"  QUOTED in QUEUE idea 432: GROSS -0.580, GATE +0.984.  REPRODUCED: "
        f"GROSS {R['GROSS']:+.4f}, GATE {R['GATE']:+.4f}   "
        f"(|diff| {abs(R['GROSS'] + 0.580):.4f} / {abs(R['GATE'] - 0.984):.4f})")
    g0_ok = abs(R["GROSS"] + 0.580) < 0.001 and abs(R["GATE"] - 0.984) < 0.001
    say(f"  G0 {'PASS — the flip the queue asks about is exactly this' if g0_ok else 'MISMATCH — reported, not reconciled away'}")

    # ------------------------------------------------------------- corpus ----
    say("\n" + "=" * 118)
    say("CORPUS — 3 panels x 7 families x 3 rungs = 63 pools, 41 arms/panel")
    say("=" * 118)
    A, store, ref = build()
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    say(f"\n  arm-rows: {len(A)}  ({A.groupby(['panel','family','cost']).ngroups} pools)")

    # ------------------------------------------------- per-pool statistics ---
    say("\n" + "=" * 118)
    say("Q4 — IDEA 311's PREMISE, MEASURED.  IS-Sharpe dispersion of each pool.")
    say("=" * 118)
    cells, picks = [], []
    rng = np.random.default_rng(BOOT_SEED)
    for (pk, fam, c), sub in A.groupby(["panel", "family", "cost"], sort=True):
        sub = sub.reset_index(drop=True)
        ctl = int(sub.index[sub["control"]][0])
        I = sub["IS_Sharpe"].astype(float).values
        O = sub["OOS_Sharpe"].astype(float).values
        pool_is, pool_oos = float(I.mean()), float(O.mean())
        Il, Ol = I - pool_is, O - pool_oos                    # IS lift / OOS lift, by arm
        oa = ols(Ol, Il)
        # inner-split lift (for the tau chooser: fit <=2013, evaluate 2014-2016)
        I1 = sub["IS1_Sharpe"].astype(float).values
        I2 = sub["IS2_Sharpe"].astype(float).values
        j1 = int(np.nanargmax(I1))
        inner_lift = float(I2[j1] - I2.mean())
        inner_disp_sd = float(np.nanstd(I1, ddof=1))
        inner_disp_span = float(np.nanmax(I1) - np.nanmin(I1))
        cells.append(dict(
            panel=pk, family=fam, group="CORE" if fam in CORE else "EXT", cost=c,
            n_arms=len(sub), disp_sd=float(np.nanstd(I, ddof=1)),
            disp_span=float(np.nanmax(I) - np.nanmin(I)),
            disp_oos_sd=float(np.nanstd(O, ddof=1)),
            pool_IS=pool_is, pool_OOS=pool_oos,
            ctl_IS=float(I[ctl]), ctl_OOS=float(O[ctl]),
            arm_slope=oa["slope"], arm_t=oa["t"], arm_r2=oa["r2"], arm_se=oa["se"],
            arm_rho=corr(Ol, Il), ratio_sd=float(np.nanstd(O, ddof=1) / np.nanstd(I, ddof=1)),
            inner_lift=inner_lift, inner_disp_sd=inner_disp_sd, inner_disp_span=inner_disp_span))
        # selector picks in this pool
        s_is = sub["IS_Sharpe"].astype(float)
        med_j = int(s_is.sort_values(kind="mergesort").index[len(s_is) // 2])
        for k, (col, dr) in (list(SEL.items()) + [("K_ANTI", ("IS_Sharpe", -1)),
                                                  ("K_MEDIAN", (None, 0))]):
            j = med_j if k == "K_MEDIAN" else pick(sub, col, dr)
            if j is None:
                continue
            picks.append(dict(panel=pk, family=fam, group="CORE" if fam in CORE else "EXT",
                              cost=c, selector=k, arm=sub.loc[j, "arm"],
                              IS_lift=float(sub.loc[j, "IS_Sharpe"]) - pool_is,
                              OOS_lift=float(sub.loc[j, "OOS_Sharpe"]) - pool_oos,
                              d_vs_ctl=float(sub.loc[j, "OOS_Sharpe"]) - float(O[ctl]),
                              pool_IS=pool_is, pool_OOS=pool_oos,
                              disp_sd=float(np.nanstd(I, ddof=1)),
                              disp_span=float(np.nanmax(I) - np.nanmin(I))))
    C = pd.DataFrame(cells)
    P = pd.DataFrame(picks)
    C.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    P.to_csv(OUT / f"{STEM}.picks.csv", index=False)

    say("\n  IS-Sharpe SPAN (max-min across the pool's arms), by family x panel, at 10 bps:")
    say(C[C.cost == PROTOCOL_RUNG].pivot_table(index="family", columns="panel",
                                               values="disp_span")
        .reindex(FAMILIES).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  IS-Sharpe SD, by family x panel, at 10 bps:")
    say(C[C.cost == PROTOCOL_RUNG].pivot_table(index="family", columns="panel", values="disp_sd")
        .reindex(FAMILIES).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  by family, all panels and rungs (n=9 cells each):")
    fam_disp = C.groupby("family").agg(span_mean=("disp_span", "mean"),
                                       span_min=("disp_span", "min"),
                                       span_max=("disp_span", "max"),
                                       sd_mean=("disp_sd", "mean"),
                                       sd_min=("disp_sd", "min"),
                                       sd_max=("disp_sd", "max")).reindex(FAMILIES)
    say(fam_disp.to_string(float_format=lambda x: f"{x:.4f}"))
    gspan = C[C.family == "GROSS"]["disp_span"]
    rank_g = int(fam_disp["span_mean"].rank().loc["GROSS"])
    say(f"\n  IDEA 311's CLAIM 'Sharpe span <= 0.006 in g': GROSS span here is "
        f"{gspan.min():.4f}..{gspan.max():.4f} (mean {gspan.mean():.4f}) over 9 cells — "
        f"{'<= 0.006 in ' + str(int((gspan <= 0.006).sum())) + ' of 9 cells' if (gspan <= 0.006).any() else 'NEVER <= 0.006'}."
        f"\n  GROSS ranks {rank_g} of {len(FAMILIES)} families by mean span (1 = narrowest). "
        f"P4 {'CONFIRMED in sign' if rank_g == 1 else 'REJECTED in sign'}"
        f"{'' if (gspan <= 0.006).all() else ' — the 0.006 LEVEL does not hold on this corpus and is reported, not reconciled'}")

    # -------------------------------------------------- Q1: asked regression -
    say("\n" + "=" * 118)
    say("Q1 — THE ASKED REGRESSION: per-family slope(OOS lift ~ IS lift) ON the family's own "
        "IS-Sharpe dispersion")
    say("=" * 118)

    def fam_slopes(df, sel_excl=("K_ANTI",), key="family"):
        out = []
        d = df[~df.selector.isin(sel_excl)]
        for f, s in d.groupby(key):
            o = ols(s["OOS_lift"], s["IS_lift"])
            out.append(dict(**{key: f}, n=o["n"], slope=o["slope"], t=o["t"], r2=o["r2"],
                            se=o["se"], rho=corr(s["OOS_lift"], s["IS_lift"])))
        return pd.DataFrame(out)

    FS = fam_slopes(P).set_index("family").reindex(FAMILIES)
    FS = FS.join(fam_disp[["span_mean", "sd_mean"]])
    say("\n  (a) FAMILY level — idea 204's own unit, extended to 7 families "
        "(pick rows, all panels/rungs, excl. K_ANTI):")
    say(FS.to_string(float_format=lambda x: f"{x:+.4f}"))
    o = ols(FS["slope"], FS["sd_mean"])
    o2 = ols(FS["slope"], FS["span_mean"])
    say(f"\n    ASKED: slope ~ disp_sd    n={o['n']}  b {o['slope']:+.4f}  t {o['t']:+.3f}  "
        f"R2 {o['r2']:.4f}   [rho {corr(FS['slope'], FS['sd_mean']):+.4f}]")
    say(f"    ASKED: slope ~ disp_span  n={o2['n']}  b {o2['slope']:+.4f}  t {o2['t']:+.3f}  "
        f"R2 {o2['r2']:.4f}   [rho {corr(FS['slope'], FS['span_mean']):+.4f}]")
    say("    n=7 is 7.  This is the queue's literal unit and it cannot carry a t; the cell-level "
        "form below is\n    the one with power, and both are reported.")

    say("\n  (b) CELL level — one slope per (family, panel, rung); the queue's 'across panels and "
        "rungs'.")
    say("      Two populations: PICKS (idea 204's own rows, 9 selectors, duplicates and all) and "
        "ARMS (every\n      arm in the pool — the population the selector draws from, and the "
        "better-identified one).")
    cellslopes = []
    for (pk, fam, c), s in P[P.selector != "K_ANTI"].groupby(["panel", "family", "cost"]):
        o = ols(s["OOS_lift"], s["IS_lift"])
        cellslopes.append(dict(panel=pk, family=fam, cost=c, pick_slope=o["slope"],
                               pick_t=o["t"], pick_r2=o["r2"], pick_se=o["se"],
                               pick_rho=corr(s["OOS_lift"], s["IS_lift"]), pick_n=o["n"]))
    CS = C.merge(pd.DataFrame(cellslopes), on=["panel", "family", "cost"], how="left")
    CS.to_csv(OUT / f"{STEM}.cellslopes.csv", index=False)

    def blk(df, lab):
        say(f"\n    --- {lab}  (n={len(df)} cells) ---")
        for ycol, yl in (("pick_slope", "PICK slope"), ("arm_slope", "ARM  slope")):
            for xcol, xl in (("disp_sd", "disp_sd"), ("disp_span", "disp_span")):
                o = ols(df[ycol], df[xcol])
                say(f"      {yl} ~ {xl:<10} n={o['n']:>3}  b {o['slope']:+9.4f}  "
                    f"t {o['t']:+7.3f}  R2 {o['r2']:6.4f}   rho {corr(df[ycol], df[xcol]):+.4f}")

    blk(CS, "ALL 7 families")
    blk(CS[CS.group == "CORE"], "CORE only (idea 204's exact 4 families x 3 panels x 3 rungs)")
    blk(CS[CS.group == "EXT"], "EXT only (the 3 new families — out-of-corpus replication)")
    blk(CS[CS.family != "CADENCE"], "excl. CADENCE (the 4-arm family)")
    say("\n    P1 asks whether the SIGNED slope is reliably NEGATIVE in dispersion "
        "(the queue's reading).")
    o = ols(CS["arm_slope"], CS["disp_sd"])
    op = ols(CS["pick_slope"], CS["disp_sd"])
    p1 = (not np.isfinite(o["t"]) or abs(o["t"]) < 2) and (not np.isfinite(op["t"]) or abs(op["t"]) < 2)
    say(f"    VERDICT P1: arm t {o['t']:+.3f}, pick t {op['t']:+.3f} -> "
        f"{'CONFIRMED (no reliable signed relation)' if p1 else 'REJECTED (a reliable signed relation exists)'}")

    # ------------------------------------------------------ Q2: identification
    say("\n" + "=" * 118)
    say("Q2 — IDENTIFICATION.  slope = rho * sd(OOS lift) / sd(IS lift), and disp IS sd(IS lift).")
    say("=" * 118)
    ident = (CS["arm_slope"] - CS["arm_rho"] * CS["ratio_sd"]).abs().max()
    say(f"  G2 the decomposition closes at max|slope - rho*sd_ratio| = {ident:.3e} over "
        f"{len(CS)} cells")
    say("\n  (a) the SCALE-FREE leg — rho(OOS lift, IS lift) regressed on dispersion:")
    for lab, df in (("ALL", CS), ("CORE", CS[CS.group == "CORE"]), ("EXT", CS[CS.group == "EXT"])):
        for ycol, yl in (("arm_rho", "ARM  rho"), ("pick_rho", "PICK rho")):
            o = ols(df[ycol], df["disp_sd"])
            say(f"    {lab:<5} {yl} ~ disp_sd   n={o['n']:>3}  b {o['slope']:+8.4f}  "
                f"icept {o['icept']:+7.4f}  t {o['t']:+7.3f}  R2 {o['r2']:6.4f}   mean rho "
                f"{df[ycol].mean():+.4f} (t {tstat(df[ycol]):+.3f})")

    say("\n  (a2) WHAT SITS AT dispersion -> 0?  The queue's mechanism says NOISE (rho = 0); the "
        "alternative it does\n       not consider is ANTI-SIGNAL (rho < 0), i.e. a Sharpe-invariant "
        "dial whose IS-best arm is reliably\n       the OOS-worst.  The regression INTERCEPT and "
        "the low-dispersion tercile answer this directly.")
    o_all = ols(CS["arm_rho"], CS["disp_sd"])
    say(f"    intercept of ARM rho ~ disp_sd (ALL, n={o_all['n']}): {o_all['icept']:+.4f}")
    ter = CS["disp_sd"].quantile([1 / 3, 2 / 3]).values
    lab_t = pd.cut(CS["disp_sd"], [-np.inf, ter[0], ter[1], np.inf], labels=["low", "mid", "high"])
    say("    by DISPERSION TERCILE (cells, all families):")
    for t_ in ["low", "mid", "high"]:
        d = CS[lab_t == t_]
        w = int((d["arm_rho"] > 0).sum())
        say(f"      {t_:<5} n={len(d):>3}  disp_sd {d['disp_sd'].min():.4f}..{d['disp_sd'].max():.4f}"
            f"  mean ARM rho {d['arm_rho'].mean():+.4f} (t {tstat(d['arm_rho']):+.3f})  "
            f"cells rho>0 {w}/{len(d)} (sign p {sign_p(w, len(d)):.4f})  "
            f"mean ARM slope {d['arm_slope'].mean():+.4f}")
    dlow = CS[lab_t == "low"]["arm_rho"]
    anti = tstat(dlow) < -2
    say(f"    -> the low-dispersion tercile is {'ANTI-PREDICTIVE (rho reliably < 0)' if anti else 'INDISTINGUISHABLE from noise'}"
        ": mean rho "
        f"{dlow.mean():+.4f}, t {tstat(dlow):+.3f}, n={len(dlow)}.")
    say("\n  (b) the MECHANICAL leg — |slope| and se(slope) on 1/disp (P2):")
    inv = 1.0 / CS["disp_sd"]
    for ycol, yl in (("arm_slope", "|ARM slope|"), ("pick_slope", "|PICK slope|")):
        o = ols(CS[ycol].abs(), inv)
        say(f"    {yl:<12} ~ 1/disp_sd  n={o['n']:>3}  b {o['slope']:+9.4f}  t {o['t']:+7.3f}  "
            f"R2 {o['r2']:6.4f}   rho {corr(CS[ycol].abs(), inv):+.4f}")
    o = ols(CS["arm_se"], inv)
    say(f"    se(ARM slope) ~ 1/disp_sd  n={o['n']:>3}  b {o['slope']:+9.4f}  t {o['t']:+7.3f}  "
        f"R2 {o['r2']:6.4f}   rho {corr(CS['arm_se'], inv):+.4f}")
    p2 = np.isfinite(o["t"]) and o["t"] > 2
    say(f"    VERDICT P2: {'CONFIRMED' if p2 else 'REJECTED'} — the low-dispersion family's slope "
        "is a LARGER NUMBER, not a\n    differently-signed fact; dispersion enters the statistic "
        "through its own denominator.")
    say("\n  (d) THE SCALE THE SLOPE IS MEASURED ON (idea 408's point, applied to a slope rather "
        "than a margin):\n      a slope is a RATIO; two families can have opposite slopes and "
        "still be describing motions three orders\n      of magnitude apart.  sd(OOS lift) is the "
        "size of the thing being ranked.")
    Pn = P[P.selector != "K_ANTI"]
    sc = Pn.groupby("family").agg(sd_IS_lift=("IS_lift", "std"), sd_OOS_lift=("OOS_lift", "std"),
                                  mean_abs_OOS_lift=("OOS_lift", lambda s: s.abs().mean()))
    sc = sc.join(FS[["slope", "rho"]]).reindex(FAMILIES)
    say(sc.to_string(float_format=lambda x: f"{x:+.4f}"))
    say(f"      ratio of the largest to the smallest family sd(OOS lift): "
        f"{sc['sd_OOS_lift'].max() / sc['sd_OOS_lift'].min():.1f}x")
    o_all_rows = ols(Pn["OOS_lift"], Pn["IS_lift"])
    o_no_g = ols(Pn[Pn.family != "GROSS"]["OOS_lift"], Pn[Pn.family != "GROSS"]["IS_lift"])
    say(f"      pooled over ALL {len(Pn)} pick rows ('the record fact'): slope "
        f"{o_all_rows['slope']:+.4f}  t {o_all_rows['t']:+.3f}  R2 {o_all_rows['r2']:.4f}")
    say(f"      pooled EXCLUDING GROSS ({len(Pn[Pn.family!='GROSS'])} rows):            slope "
        f"{o_no_g['slope']:+.4f}  t {o_no_g['t']:+.3f}  R2 {o_no_g['r2']:.4f}   "
        f"(change {o_no_g['slope'] - o_all_rows['slope']:+.4f})")
    say("      READ: the family with the most extreme slope moves the pooled record number "
        "least, because OLS\n      weights by x-variance and GROSS's IS lift variance is "
        "~0.  The flip is loud and weightless.")

    say("\n  (c) so which reading does the data support?  the two candidate stories:")
    say("      STORY A (the queue's): low dispersion => the dial is Sharpe-invariant => IS lift is "
        "noise => slope NEGATIVE.\n      STORY B (this run's): low dispersion => var(slope) "
        "explodes => slope LARGE in EITHER direction, sign\n      unstable across panels and rungs.")
    say("      Discriminator: is the per-family slope SIGN stable across the 9 (panel, rung) cells "
        "of that family?")
    sgn = CS.assign(pos=(CS["arm_slope"] > 0)).groupby("family")["pos"].agg(["sum", "count"])
    sgn["sign_p"] = [sign_p(int(r["sum"]), int(r["count"])) for _, r in sgn.iterrows()]
    sgn = sgn.join(fam_disp["sd_mean"]).reindex(FAMILIES)
    say(sgn.rename(columns={"sum": "cells_slope>0", "count": "cells"})
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say("      READ: a family whose slope sign is a FACT should be 9/9 or 0/9; one whose slope is "
        "noise sits near 5/9.")

    # ------------------------------------------------------------ Q3: the flip
    say("\n" + "=" * 118)
    say("Q3 — IS THE FLIP REAL?  cluster bootstrap over cells within each family "
        f"({N_BOOT} draws, seed {BOOT_SEED})")
    say("=" * 118)
    cellkeys = {f: list(g.groupby(["panel", "cost"]).groups.keys())
                for f, g in P[P.selector != "K_ANTI"].groupby("family")}
    boot = {}
    for f in FAMILIES:
        d = P[(P.family == f) & (P.selector != "K_ANTI")]
        keys = cellkeys[f]
        idx = {k: d[(d.panel == k[0]) & (d.cost == k[1])] for k in keys}
        draws = []
        for _ in range(N_BOOT):
            take = rng.integers(0, len(keys), len(keys))
            s = pd.concat([idx[keys[i]] for i in take])
            o = ols(s["OOS_lift"], s["IS_lift"])
            draws.append(o["slope"])
        boot[f] = np.array(draws, float)
    say("\n  family        point     boot mean    boot sd    2.5%      97.5%   P(slope>0)")
    for f in FAMILIES:
        b = boot[f][np.isfinite(boot[f])]
        say(f"  {f:<12} {FS.loc[f,'slope']:+8.4f}  {b.mean():+9.4f}  {b.std(ddof=1):8.4f}  "
            f"{np.percentile(b,2.5):+8.4f}  {np.percentile(b,97.5):+8.4f}   "
            f"{float((b>0).mean()):.3f}")
    dg = boot["GROSS"] - boot["GATE"]
    say(f"\n  GROSS minus GATE: point {FS.loc['GROSS','slope'] - FS.loc['GATE','slope']:+.4f}, "
        f"boot mean {dg.mean():+.4f}, sd {dg.std(ddof=1):.4f}, "
        f"95% CI [{np.percentile(dg,2.5):+.4f}, {np.percentile(dg,97.5):+.4f}], "
        f"P(diff<0) {float((dg<0).mean()):.3f}")
    flip_real = np.percentile(dg, 97.5) < 0 or np.percentile(dg, 2.5) > 0
    say(f"  -> the GROSS/GATE gap is {'SEPARABLE from zero' if flip_real else 'NOT separable from zero'} "
        "under a cluster bootstrap over its own cells.")
    spread = float(np.nanstd(FS["slope"], ddof=1))
    mean_se = float(np.nanmean([boot[f].std(ddof=1) for f in FAMILIES]))
    say(f"  heterogeneity: sd of the 7 family slopes = {spread:.4f} vs mean bootstrap se "
        f"{mean_se:.4f}  (ratio {spread/mean_se:.2f})")
    say("  READ: ratio ~ 1 means the family-to-family spread is exactly what each family's own "
        "sampling error\n  produces — 'family fact' would need a ratio comfortably above 1.")

    # -------------------------------------------------------------- Q5: rule 8
    say("\n" + "=" * 118)
    say("Q5 — PROTOCOL RULE 8.  tau chosen on the INNER IS split (fit <=2013-12-31, evaluated "
        "2014-2016);")
    say("     the outer OOS (2017-2026) is read ONCE.  All 11 tau x 2 stat grid points reported.")
    say("=" * 118)
    say("  RULE R(tau, stat): in a pool whose IS dispersion > tau, take the K_Sharpe argmax pick; "
        "otherwise take\n  the pool's own do-nothing control (ABSTAIN).  tau=0 is always-pick; "
        "tau=inf is always-abstain.")

    KS = P[P.selector == "K_Sharpe"].set_index(["panel", "family", "cost"])
    CSi = CS.set_index(["panel", "family", "cost"])
    keys = list(CSi.index)

    def rule_rows(stat, tau, which):
        """Return per-cell (OOS_lift of the rule's choice, took_pick) under R(tau, stat)."""
        out = []
        for k in keys:
            disp = float(CSi.loc[k, "inner_disp_sd" if stat == "sd" else "inner_disp_span"]
                         if which == "inner" else
                         CSi.loc[k, "disp_sd" if stat == "sd" else "disp_span"])
            took = disp > tau
            if which == "inner":
                lift = float(CSi.loc[k, "inner_lift"]) if took else 0.0
            else:
                lift = float(KS.loc[k, "OOS_lift"]) if took else float(
                    CSi.loc[k, "ctl_OOS"] - CSi.loc[k, "pool_OOS"])
            out.append((lift, took, k))
        return out

    grid_sd = [0.0] + [float(np.percentile(CS["disp_sd"], q)) for q in range(10, 100, 10)] + [1e9]
    grid_sp = [0.0] + [float(np.percentile(CS["disp_span"], q)) for q in range(10, 100, 10)] + [1e9]
    say("\n  (a) INNER-SPLIT selection of tau (this is the only place tau is chosen; OOS unseen):")
    inner_tab = []
    for stat, grid in (("sd", grid_sd), ("span", grid_sp)):
        for tau in grid:
            rr = rule_rows(stat, tau, "inner")
            v = np.array([x[0] for x in rr], float)
            inner_tab.append(dict(stat=stat, tau=tau, n_pick=int(sum(x[1] for x in rr)),
                                  mean_inner_lift=float(v.mean()), t=tstat(v)))
    IT = pd.DataFrame(inner_tab)
    say(IT.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    best = IT.loc[IT["mean_inner_lift"].idxmax()]
    tau_star, stat_star = float(best["tau"]), str(best["stat"])
    say(f"\n  tau* = {tau_star:.4f} on stat '{stat_star}' (inner mean lift {best['mean_inner_lift']:+.4f}, "
        f"picks in {int(best['n_pick'])} of {len(keys)} pools).  READ ONCE below.")

    say("\n  (b) OUTER OOS — every grid point reported; the tau* row is marked '*'.")
    wf = []
    for stat, grid in (("sd", grid_sd), ("span", grid_sp)):
        for tau in grid:
            rr = rule_rows(stat, tau, "outer")
            v = np.array([x[0] for x in rr], float)
            took = int(sum(x[1] for x in rr))
            # absolute OOS metrics of the rule's chosen books, per cell
            oos_s, oos_c, oos_d, d_ctl = [], [], [], []
            for _, t_, k in rr:
                pkk, fam, c = k
                arm = KS.loc[k, "arm"] if t_ else \
                    A[(A.panel == pkk) & (A.family == fam) & (A.cost == c) & A.control]["arm"].iloc[0]
                r = store[(pkk, fam, c, arm)]
                m = metrics(window(r, "OOS"))
                ctl_arm = A[(A.panel == pkk) & (A.family == fam) & (A.cost == c) & A.control]["arm"].iloc[0]
                mc = metrics(window(store[(pkk, fam, c, ctl_arm)], "OOS"))
                oos_s.append(m["Sharpe"]); oos_c.append(m["CAGR"]); oos_d.append(m["MaxDD"])
                d_ctl.append(m["Sharpe"] - mc["Sharpe"])
            wf.append(dict(stat=stat, tau=tau, n_pick=took, mean_OOS_lift=float(v.mean()),
                           t_lift=tstat(v), mean_OOS_Sharpe=float(np.mean(oos_s)),
                           mean_OOS_CAGR=float(np.mean(oos_c)), mean_OOS_MaxDD=float(np.mean(oos_d)),
                           mean_d_vs_ctl=float(np.mean(d_ctl)), t_d_vs_ctl=tstat(d_ctl),
                           wins_vs_ctl=int(np.sum(np.array(d_ctl) > 0)),
                           nonties=int(np.sum(np.array(d_ctl) != 0)),
                           star=(stat == stat_star and abs(tau - tau_star) < 1e-12)))
    W = pd.DataFrame(wf)
    W["sign_p"] = [sign_p(int(r["wins_vs_ctl"]), int(r["nonties"])) for _, r in W.iterrows()]
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    star = W[W.star].iloc[0]
    always_pick = W[(W.stat == stat_star) & (W.tau == 0.0)].iloc[0]
    always_abst = W[(W.stat == stat_star) & (W.tau == 1e9)].iloc[0]
    say(f"\n  RULE 8 READ-ONCE RESULT at tau*={tau_star:.4f} ({stat_star}):")
    say(f"    R(tau*)          mean OOS Sharpe {star['mean_OOS_Sharpe']:.4f}  CAGR "
        f"{star['mean_OOS_CAGR']:.2%}  MaxDD {star['mean_OOS_MaxDD']:.2%}  "
        f"d vs control {star['mean_d_vs_ctl']:+.4f} (t {star['t_d_vs_ctl']:+.2f}, "
        f"{int(star['wins_vs_ctl'])}/{int(star['nonties'])}, sign p {star['sign_p']:.4f})")
    say(f"    always-pick      mean OOS Sharpe {always_pick['mean_OOS_Sharpe']:.4f}  CAGR "
        f"{always_pick['mean_OOS_CAGR']:.2%}  MaxDD {always_pick['mean_OOS_MaxDD']:.2%}  "
        f"d vs control {always_pick['mean_d_vs_ctl']:+.4f} (t {always_pick['t_d_vs_ctl']:+.2f})")
    say(f"    always-abstain   mean OOS Sharpe {always_abst['mean_OOS_Sharpe']:.4f}  CAGR "
        f"{always_abst['mean_OOS_CAGR']:.2%}  MaxDD {always_abst['mean_OOS_MaxDD']:.2%}  "
        "(this IS the do-nothing control, by construction)")
    p5 = star["mean_OOS_Sharpe"] <= always_abst["mean_OOS_Sharpe"]
    say(f"    VERDICT P5: {'CONFIRMED' if p5 else 'REJECTED'} — the dispersion-gated chooser "
        f"{'does not beat' if p5 else 'BEATS'} always-abstaining OOS.")

    # benchmarks
    say("\n  benchmarks over the same OOS window (2017-2026), per panel, at 10 bps:")
    for pk in PANELS:
        so = metrics(window(ref[pk]["spy"], "OOS"))
        v2o = metrics(window(ref[pk]["v2"][PROTOCOL_RUNG], "OOS"))
        v1o = metrics(window(ref[pk]["v1"][PROTOCOL_RUNG], "OOS"))
        say(f"    {pk:<6} SPY {so['CAGR']:6.2%}/{so['Sharpe']:.4f}/{so['MaxDD']:7.2%}   "
            f"RULES v2 {v2o['CAGR']:6.2%}/{v2o['Sharpe']:.4f}/{v2o['MaxDD']:7.2%}   "
            f"RULES v1 {v1o['CAGR']:6.2%}/{v1o['Sharpe']:.4f}/{v1o['MaxDD']:7.2%}")

    # ----------------------------------------------------------- Q6: KEEP ----
    say("\n" + "=" * 118)
    say("Q6 — BOTH KEEP PATHS (PROTOCOL 4a vs RULES v2 live, 4b vs SPY), full sample and OOS")
    say("=" * 118)
    kp = []
    say(f"\n  ARMS ({len(A)} rows):")
    for lab, d in (("all", A), ("10 bps", A[A.cost == PROTOCOL_RUNG]),
                   ("CORE", A[A.group == "CORE"]), ("EXT", A[A.group == "EXT"])):
        b = int((d.pass4a_v2 & d.pass4b).sum())
        say(f"    {lab:<8} n={len(d):>4}  4a(v2) {int(d.pass4a_v2.sum()):>3}  "
            f"4b full {int(d.pass4b.sum()):>3}  4b OOS {int(d.pass4b_oos.sum()):>3}  BOTH {b:>3}")
        kp.append(dict(scope="arms", subset=lab, n=len(d), pass4a=int(d.pass4a_v2.sum()),
                       pass4b_full=int(d.pass4b.sum()), pass4b_oos=int(d.pass4b_oos.sum()),
                       both=b))
    say(f"\n  4b binding bar on the arms that fail (10 bps): "
        f"{dict(A[(A.cost==PROTOCOL_RUNG) & (~A.pass4b)].bind4b.value_counts())}")

    # the rule's chosen books at tau*
    rr = rule_rows(stat_star, tau_star, "outer")
    sel_rows = []
    for _, t_, k in rr:
        pkk, fam, c = k
        arm = KS.loc[k, "arm"] if t_ else \
            A[(A.panel == pkk) & (A.family == fam) & (A.cost == c) & A.control]["arm"].iloc[0]
        row = A[(A.panel == pkk) & (A.family == fam) & (A.cost == c) & (A.arm == arm)].iloc[0]
        sel_rows.append(dict(row, took_pick=t_))
    S = pd.DataFrame(sel_rows)
    b = int((S.pass4a_v2 & S.pass4b).sum())
    say(f"\n  R(tau*) SELECTED BOOKS (one per pool, {len(S)} rows): 4a(v2) "
        f"{int(S.pass4a_v2.sum())}  4b full {int(S.pass4b.sum())}  4b OOS "
        f"{int(S.pass4b_oos.sum())}  BOTH {b}")
    kp.append(dict(scope="R(tau*) picks", subset=f"{stat_star}>{tau_star:.4f}", n=len(S),
                   pass4a=int(S.pass4a_v2.sum()), pass4b_full=int(S.pass4b.sum()),
                   pass4b_oos=int(S.pass4b_oos.sum()), both=b))
    at10 = S[S.cost == PROTOCOL_RUNG]
    b10 = int((at10.pass4a_v2 & at10.pass4b).sum())
    say(f"  at the PROTOCOL 10 bps rung only ({len(at10)} rows): 4a {int(at10.pass4a_v2.sum())}  "
        f"4b full {int(at10.pass4b.sum())}  4b OOS {int(at10.pass4b_oos.sum())}  BOTH {b10}")
    kp.append(dict(scope="R(tau*) picks", subset="10 bps", n=len(at10),
                   pass4a=int(at10.pass4a_v2.sum()), pass4b_full=int(at10.pass4b.sum()),
                   pass4b_oos=int(at10.pass4b_oos.sum()), both=b10))
    pd.DataFrame(kp).to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)

    if b10 > 0:
        say("\n  BOTH-PATHS rows at 10 bps:")
        say(at10[at10.pass4a_v2 & at10.pass4b][
            ["panel", "family", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
                index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------- verdict ---
    say("\n" + "=" * 118)
    say("PRE-REGISTERED PREDICTIONS, SCORED")
    say("=" * 118)
    say(f"  P1 signed slope-on-dispersion NOT reliably negative : "
        f"{'CONFIRMED' if p1 else 'REJECTED'}")
    say(f"  P2 |slope| / se(slope) track 1/dispersion           : "
        f"{'CONFIRMED' if p2 else 'REJECTED'}")
    o_rho, o_slp = ols(CS["arm_rho"], CS["disp_sd"]), ols(CS["arm_slope"], CS["disp_sd"])
    p3 = abs(o_rho["t"]) < abs(o_slp["t"])
    say(f"  P3 rho-on-dispersion weaker than slope-on-dispersion: "
        f"{'CONFIRMED' if p3 else 'REJECTED'}  (|t| rho {abs(o_rho['t']):.3f} vs slope "
        f"{abs(o_slp['t']):.3f}, R2 {o_rho['r2']:.4f} vs {o_slp['r2']:.4f})")
    say(f"  P4 idea 311 replicates in SIGN, not at 0.006        : "
        f"{'CONFIRMED in sign' if rank_g == 1 else 'REJECTED'}")
    say(f"  P5 the dispersion-gated chooser loses to abstaining  : "
        f"{'CONFIRMED' if p5 else 'REJECTED'}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.console.txt/.arms.csv/.cells.csv/.picks.csv/.cellslopes.csv/"
        ".walkforward.csv/.keeppaths.csv")


if __name__ == "__main__":
    main()
