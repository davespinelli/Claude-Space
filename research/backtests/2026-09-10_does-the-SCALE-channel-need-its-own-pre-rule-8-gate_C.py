#!/usr/bin/env python3
"""Idea 628 - does the SCALE channel need its own pre-rule-8 gate?   (lane C, 2026-09-10)

THE QUEUE'S QUESTION
    Idea 623 (lane B, 2026-09-10) built a DATING certificate (T2: truncation invariance) that is
    perfect on the terminal-dating axis (TP 10 / FP 0 / FN 0 / TN 10) and removes every oracle
    from the rule-8 candidate set -- and the surviving pick STILL beat SPY out of sample by
    +0.706 Sharpe, because the pick was PXDVOL, a price-LEVEL key with |IC vs the realised
    forward return| of 0.5996.  Only T1&T2 (scale AND dating) produced an honest walk-forward
    (OOS 0.467, losing to SPY at 3/3 rungs).  The queue therefore asks whether the SCALE
    certificate earns its place as a STANDING pre-rule-8 gate on the record's own key families,
    or whether idea 185's LEAK LAW -- 'a key's dSharpe is priced by its look-ahead content',
    Spearman(|IC vs realised forward return|, mean dSharpe) = +0.806 broad / +0.881 small --
    already prices the same thing more cheaply.

WHAT 'MORE CHEAPLY' HAS TO MEAN, STATED BEFORE ANYTHING IS RUN
    The two instruments are not the same kind of object and the run is designed around that.
      T1 (scale certificate) is STRUCTURAL: rank(key(px)) vs rank(key(px x diag(c))).  It reads
        no returns, needs no future, and is computable on the key's source alone.
      The LEAK LAW is STATISTICAL: it scores a key by |mean cross-sectional IC against a REALISED
        forward return|.  In idea 185's published form that forward return runs to the END of the
        sample -- i.e. the screen itself is oracle-conditioned and is NOT available at the rule-8
        decision point.  So this run prices TWO forms:
          LEAKT  idea 185's exact statistic: IC vs (px[-1]/px - 1), read at dates across the whole
                 sample.  Oracle input.  Published for comparability; NOT implementable.
          LEAKH  the implementable analogue: IC vs the 252-day forward return, computed ONLY at
                 dates t with t+252d <= 2016-12-31, so every input is inside the IS window a
                 rule-8 chooser is allowed to read.  This is the version that could actually
                 stand as a gate.
    A screen is a CHEAPER SUBSTITUTE for T1 only if some threshold on it (i) flags the scale
    leaks the dating gate misses and (ii) does not flag the causal keys -- and, in consequence,
    (iii) hands rule 8 a pick that behaves honestly.  Any threshold that buys (i) by killing the
    honest family has not substituted for T1, it has just turned the candidate set off.

PARTS
    A  INSTRUMENT.  26 keys (idea 623's 20 verbatim + 6 new, so its published confusion counts
       reproduce) with hand-derived ground truth on both axes.  T1 / T2 / LEAKT / LEAKH scored on
       the SCALE axis over the T2-cleared set -- the operative set, since dating is already
       gated -- at every threshold on a fixed 19-point ladder, plus AUC.  Every point reported.
    A2 THE BAND (POST-HOC: added after PART A's ladder was read, and labelled as such wherever it
       is used).  The ladder showed a screen can order the two classes perfectly and still have no
       ladder point that separates them, so A2 measures the separating BAND directly -- (max
       non-leak |IC|, min leak |IC|] -- its width, its width in ladder steps, and whether it
       survives being re-estimated on two disjoint halves of the IS window.  A threshold whose
       band is narrower than the grid it would be published on cannot be placed by anyone who
       does not already know the answer.
    B  PRICER.  Idea 185's leak law re-measured on this corpus: Spearman(screen, mean dSharpe)
       and the AUC of each screen for the event 'this key's rule-8 arm beats SPY out of sample'.
       Does the statistical screen predict what the structural one certifies?
    C  CONSEQUENCE BOOK.  The gate priced where it is proposed to sit: BEFORE rule 8.  Gates
       NONE / T1 / T2 / T1&T2 / LEAKT(tau) / LEAKH(tau) / T2&LEAKT(tau) / T2&LEAKH(tau), each
       restricted to each KEY FAMILY (causal / level / both / termonly / ALL), at 0, 10 and 25
       bps.  PROTOCOL 2/3/4 on every arm; PROTOCOL 8 walk-forward on every gate x family x rung.

TUNED PARAMETERS: exactly two, as the queue prescribes -- GATE (which certificate/screen, and at
    which threshold: the whole tau ladder is reported, none is selected) and KEY FAMILY (which of
    the record's four families the gate is allowed to admit).  The tilt strength m and the cost
    rung are NOT tuned here: m is inherited verbatim from ideas 185/195/623 ({0.20,0.50,1.00})
    and is chosen inside by rule 8 itself, and all three rungs are always reported.  The
    certificate tolerance is fixed at idea 433's one rank step on idea 623's MEDIAN statistic.

PRE-REGISTERED PREDICTIONS (scored in PART D, before any of them is read)
    P1  Gates G1-G5 pass at their stated tolerances, including reproduction of idea 623's
        committed .arms.csv rows on the 20 shared keys and of its certificate FLAGS under an
        independent RNG seed.
    P2  No threshold on the IMPLEMENTABLE screen LEAKH separates the scale family from the causal
        family on the T2-cleared set: at every tau that flags PXDVOL, at least one causal key is
        flagged too.  (T1 does this by construction at FP 0.)
    P3  T1 given T2 changes the rule-8 pick at 2 or more of the 3 rungs on the full corpus --
        i.e. the scale channel is not already priced by the dating gate.
    P4  LEAKT (oracle input) scores a strictly higher AUC on the scale axis than LEAKH
        (implementable): the leak law's power comes from the future it is allowed to read.
    P5  There EXISTS a tau at which T2&LEAKH picks a key that loses to SPY OOS at all 3 rungs,
        AND at that tau the admitted set differs from T1&T2's -- the screen can buy honesty, but
        not by identifying the same keys.
    P6  4a 0 and 4b 0 across the whole grid (ideas 195/623 on this panel).

SURVIVORSHIP, as PROTOCOL 9 requires: PART C runs on idea 195/623's SMALL430 -- current
    constituents of a sub-$2B screen (data/SMALL_PANEL_README.md) intersected with the names that
    still file today, and then filtered by data/small_meta.csv's own FULL-SAMPLE max_1d_move.  A
    survivor of a survivor, with a terminal-dated panel filter that idea 623's T2 flags.  Every
    PART C number is biased in the tilt's favour and none of them is a capital claim.

Costs 10 bps (PROTOCOL 2) with 0 and 25 bps reported; weights at close t applied t+1 (engine).
Deterministic, standalone:
    python research/backtests/2026-09-10_does-the-SCALE-channel-need-its-own-pre-rule-8-gate_C.py
Writes .console.txt .certs.csv .ladder.csv .pricer.csv .arms.csv .walkforward.csv .repro.csv
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, load_volume, rules_v1_weights,  # noqa: E402
                      rules_v2_weights)
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_does-the-SCALE-channel-need-its-own-pre-rule-8-gate_C"
OUT = ROOT / "research" / "backtests"
P623 = "2026-09-10_does-a-TERMINAL-DATING-certificate-belong-BEFORE-rule-8_B"
SHARES_PIN = OUT / "2026-09-10_market-cap-as-the-third-substitution_B.shares.csv"

# ---- inherited verbatim from ideas 181/185/193/195/623 so the published cells stay comparable
SEED = 628                                          # NOT 623: the flags must survive a new seed
N, GROSS, FREQ, MAXVOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
DIRS = {"POS": 1.0, "NEG": -1.0}
COSTS = [0.0, 10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
PHI, DELTA = 0.70, 0.60
REPRO_TOL = 5e-3

# ---- certificate settings (NOT tuned; idea 433's recommendation, idea 623's median statistic)
N_SCALE_DRAWS = 8
PROBE_FRAC = [0.35, 0.50, 0.65, 0.80, 0.95]
TOL_STEPS = 1.0
IC_STRIDE = 63                                      # idea 623's IC sampling, verbatim
FWD_H = 252                                         # LEAKH horizon, one year, fixed
TAUS = [round(0.05 * i, 2) for i in range(1, 20)]   # 0.05 .. 0.95, every point reported

_console = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _console.append(s)


def rankpct(df):
    return df.rank(axis=1, pct=True)


# ------------------------------------------------------------------ vectorised engine equivalent
def fast_backtest(prices, weights, freq=FREQ):
    """(gross returns at 0 bps, turnover).  Idea 623's harness verbatim; gate G1 checks it."""
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
    port = (held * rets).sum(axis=1)
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ======================================================================= PART A: the key corpus
def _entry(px):
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(fv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def _term(px):
    lv = px.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(lv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def _bcast(vec, px):
    return pd.DataFrame(np.tile(np.asarray(vec, float), (len(px), 1)),
                        index=px.index, columns=px.columns).where(px.notna())


def _composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


# idea 623's 20 keys VERBATIM (so its confusion matrix reproduces), then 6 NEW ones marked below.
#                          fn(px, vol, shares) -> key frame        scale_leak  term_date  family
KEY_SPECS = {
    # ---- causal, scale-invariant (the honest family)
    "MOM":      (lambda p, v, s: _composite(p),                      False, False, "causal"),
    "R6":       (lambda p, v, s: rankpct(p / p.shift(126) - 1),       False, False, "causal"),
    "DDTR":     (lambda p, v, s: rankpct(p / p.rolling(252).max() - 1), False, False, "causal"),
    "REBASED":  (lambda p, v, s: rankpct(p / _entry(p)),              False, False, "causal"),
    "VOL20":    (lambda p, v, s: rankpct(p.pct_change().rolling(20).std()), False, False, "causal"),
    "VOLSH":    (lambda p, v, s: rankpct(v.rolling(20).mean()),       False, False, "causal"),
    # ---- causal but price-LEVEL dependent (T1's own domain)
    "PRICE":    (lambda p, v, s: rankpct(p),                          True,  False, "level"),
    "FROZEN":   (lambda p, v, s: rankpct(_entry(p)),                  True,  False, "level"),
    "DVOL":     (lambda p, v, s: rankpct((p * v).rolling(20).mean()), True,  False, "level"),
    "PXDVOL":   (lambda p, v, s: rankpct(p * v.rolling(20).mean()),   True,  False, "level"),
    # ---- terminal-dated AND scale-dependent
    "MCAP":     (lambda p, v, s: rankpct(p * _bcast(s, p)),           True,  True,  "both"),
    "MCAPFRZ":  (lambda p, v, s: rankpct(_entry(p) * _bcast(s, p)),   True,  True,  "both"),
    "PXTERM":   (lambda p, v, s: rankpct(_term(p)),                   True,  True,  "both"),
    # ---- terminal-dated but SCALE-INVARIANT: the family T1 is structurally blind to
    "FWDRET":   (lambda p, v, s: rankpct(_term(p) / p - 1.0),         False, True,  "termonly"),
    "TERMREB":  (lambda p, v, s: rankpct(p / _term(p)),               False, True,  "termonly"),
    "MCAPREB":  (lambda p, v, s: rankpct((p / _entry(p)) * _bcast(s, p)), False, True, "termonly"),
    "SHARES":   (lambda p, v, s: rankpct(_bcast(s, p)),               False, True,  "termonly"),
    "FULLVOL":  (lambda p, v, s: rankpct(_bcast(p.pct_change().std(), p)), False, True, "termonly"),
    "FULLSHRP": (lambda p, v, s: rankpct(_bcast(p.pct_change().mean() / p.pct_change().std(), p)),
                 False, True, "termonly"),
    "MAXMOVE":  (lambda p, v, s: rankpct(_bcast(p.pct_change().abs().max(), p)),
                 False, True, "termonly"),
    # ================= NEW IN THIS RUN (6), to widen each family the gate is cut by =============
    # causal, scale-free: both are functions of RETURNS only, so px -> px x diag(c) leaves them
    # pointwise unchanged.
    "UPDAYS":   (lambda p, v, s: rankpct((p.pct_change() > 0).rolling(252).mean()),
                 False, False, "causal"),
    "SKEW60":   (lambda p, v, s: rankpct(p.pct_change().rolling(60).skew()),
                 False, False, "causal"),
    # price-LEVEL, causal: a dollar RANGE and an Amihud illiquidity ratio.  PXRANGE scales by c;
    # AMIHUD = mean|ret| / mean(px x vol) scales by 1/c.  Both are order-changing under rescale.
    "PXRANGE":  (lambda p, v, s: rankpct(p.rolling(252).max() - p.rolling(252).min()),
                 True, False, "level"),
    "AMIHUD":   (lambda p, v, s: rankpct(p.pct_change().abs().rolling(60).mean()
                                         / (p * v).rolling(60).mean()),
                 True, False, "level"),
    # terminal AND scale-dependent: a terminal price times a causal share volume.
    "DVOLTERM": (lambda p, v, s: rankpct(_term(p) * v.rolling(20).mean()), True, True, "both"),
    # terminal, scale-INVARIANT: a ratio of two prices of the SAME name, so c cancels.
    "FWDR21":   (lambda p, v, s: rankpct(_term(p) / p.shift(21) - 1.0), False, True, "termonly"),
}
SHARED_623 = [k for k in KEY_SPECS if k not in
              ("UPDAYS", "SKEW60", "PXRANGE", "AMIHUD", "DVOLTERM", "FWDR21")]


def _rank_int(k):
    return k.rank(axis=1, method="first")


def _perday_max(d):
    ok = d.notna().sum(axis=1) >= 20
    return d.max(axis=1).where(ok)


def disp_T1(fn, px, vol, shares, rng):
    """SCALE certificate (idea 433 form, idea 623 median statistic).  Returns (global max,
    median-over-days of the per-day max), in rank steps."""
    base = _rank_int(fn(px, vol, shares))
    gmax, per = 0.0, None
    for _ in range(N_SCALE_DRAWS):
        c = pd.Series(np.exp(rng.normal(0.0, 1.0, size=px.shape[1])), index=px.columns)
        alt = _rank_int(fn(px.mul(c, axis=1), vol, shares))
        d = (base - alt).abs()
        gmax = max(gmax, float(np.nanmax(d.values)) if d.notna().any().any() else 0.0)
        pm = _perday_max(d)
        per = pm if per is None else pd.concat([per, pm], axis=1).max(axis=1)
    med = float(np.nanmedian(per.values)) if per is not None and per.notna().any() else 0.0
    return gmax, med


def disp_T2(fn, px, vol, shares, shares_asof):
    """DATING certificate (idea 623).  Truncation invariance at five probe dates."""
    base = _rank_int(fn(px, vol, shares))
    nan_shares = shares * np.nan
    per = []
    for f in PROBE_FRAC:
        t = px.index[int(f * (len(px) - 1))]
        s_t = shares if shares_asof <= t else nan_shares
        alt = _rank_int(fn(px.loc[:t], vol.loc[:t], s_t))
        b, a = base.loc[t], alt.loc[t]
        if bool((b.notna() & a.isna()).any()):
            return float("inf"), float("inf")
        d = (b - a).abs()
        per.append(float(np.nanmax(d.values)) if d.notna().any() else 0.0)
    return float(max(per)), float(np.median(per))


def mean_ic(key, fwd, dates):
    """|mean cross-sectional Spearman IC| of a key against a forward-return frame, over dates."""
    vals = []
    for t in dates:
        if t not in key.index or t not in fwd.index:
            continue
        a, b = key.loc[t], fwd.loc[t]
        m = a.notna() & b.notna()
        if m.sum() >= 20:
            ra, rb = a[m].rank(), b[m].rank()
            if ra.std() > 0 and rb.std() > 0:
                vals.append(float(np.corrcoef(ra, rb)[0, 1]))
    return float(np.mean(vals)) if vals else np.nan


def auc(score, truth):
    """Mann-Whitney AUC of a continuous score for a binary truth vector.  Ties count 0.5."""
    s = np.asarray(score, float)
    y = np.asarray(truth, bool)
    ok = ~np.isnan(s)
    s, y = s[ok], y[ok]
    if y.sum() == 0 or (~y).sum() == 0:
        return np.nan
    r = pd.Series(s).rank().values
    n1, n0 = int(y.sum()), int((~y).sum())
    return float((r[y].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def spearman(a, b):
    a, b = pd.Series(a, dtype=float), pd.Series(b, dtype=float)
    m = a.notna() & b.notna()
    if m.sum() < 3:
        return np.nan
    ra, rb = a[m].rank(), b[m].rank()
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# --------------------------------------------------------------------------------------- metrics
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def full_row(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_LO))):
        m = metrics(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = \
            m["CAGR"], m["Sharpe"], m["MaxDD"]
    return out


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= DELTA * spy["MaxDD_F"]
                and row["CAGR_F"] >= PHI * spy["CAGR_F"])


# ============================================================================================ run
def main():
    t0 = time.time()
    repro = []

    pxF = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxF = pxF[[c for c in pxF.columns if c == "SPY" or c not in bad]]
    pin = pd.read_csv(SHARES_PIN)
    shares = pin.set_index("ticker")["shares"]
    covered = [c for c in pxF.columns if c != "SPY" and c in shares.index]
    px = pxF[covered]
    spy_px = pxF["SPY"]
    vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
    sh = shares.reindex(px.columns)
    start = px.index[260]

    say("=" * 112)
    say(f"IDEA 628 - does the SCALE channel need its own pre-rule-8 gate?   (lane C, "
        f"{pd.Timestamp.utcnow().date()})")
    say("=" * 112)
    say(f"Panel SMALL{len(covered)} (ideas 195/623): {px.shape[1]} names, "
        f"{px.index[0].date()}..{px.index[-1].date()}, SPY benchmark only.  Shares from the "
        f"PINNED {SHARES_PIN.name}.")
    say(f"Corpus: {len(KEY_SPECS)} keys = idea 623's {len(SHARED_623)} verbatim + 6 new "
        f"(UPDAYS SKEW60 PXRANGE AMIHUD DVOLTERM FWDR21).")
    say("")

    # =============================================================== GATES (pre-registered, G1-G5)
    say("-" * 112)
    say("GATES (five, pre-registered)")
    comp = _composite(px)
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = (px > px.rolling(200).mean()) & (vol20 < MAXVOL)
    rk = comp.where(elig).rank(axis=1, ascending=False)
    wctl = (rk <= N).astype(float) * (GROSS / N)
    ev = px.index[260:]

    eng0 = backtest(px, wctl, cost_bps=0.0, freq=FREQ)
    g0, t0turn = fast_backtest(px, wctl)
    g1r = float(np.abs(eng0["returns"].loc[ev].values - g0.loc[ev].values).max())
    g1t = float(np.abs(eng0["turnover"].loc[ev].values - t0turn.loc[ev].values).max())
    say(f"  G1  fast_backtest == engine.backtest (control book)      returns {g1r:.3e}  "
        f"turnover {g1t:.3e}   [tol 1e-12, evaluation window]")
    repro.append(dict(gate="G1_fast_vs_engine", value=max(g1r, g1t), tol=1e-12,
                      passed=max(g1r, g1t) < 1e-12))

    eng25 = backtest(px, wctl, cost_bps=25.0, freq=FREQ)
    derived = g0 - t0turn * 25.0 / 1e4
    g2 = float(np.abs(eng25["returns"].loc[ev].values - derived.loc[ev].values).max())
    say(f"  G2  cost-rung identity r(c)=r(0)-turnover*c/1e4 @25bps    {g2:.3e}   [tol 1e-12]")
    repro.append(dict(gate="G2_rung_identity", value=g2, tol=1e-12, passed=g2 < 1e-12))

    # G4: a causal scale-free control clears BOTH certificates at exactly zero
    ident = lambda p, v, s: rankpct(p / p.shift(21) - 1.0)          # noqa: E731
    x1, m1 = disp_T1(ident, px, vol, sh, np.random.default_rng(SEED + 1))
    x2, m2 = disp_T2(ident, px, vol, sh, px.index[-1])
    say(f"  G4  both certificates clear a causal scale-free control   T1 med {m1:.3e} (max "
        f"{x1:.1f})  T2 med {m2:.3e} (max {x2:.1f})   [tol 0 exactly on the MEDIAN statistic]")
    repro.append(dict(gate="G4_control_key", value=max(m1, m2), tol=0.0,
                      passed=(m1 == 0.0 and m2 == 0.0)))

    # ============================================================ PART A -- THE INSTRUMENT
    say("")
    say("=" * 112)
    say("PART A  THE INSTRUMENT: T1 (structural) vs the LEAK LAW (statistical) on the SCALE axis")
    say("=" * 112)
    shares_asof = px.index[-1]
    fwd_T = px.iloc[-1] / px - 1.0                                  # idea 185's oracle forward
    fwd_H = px.shift(-FWD_H) / px - 1.0                             # implementable 252d forward
    ic_dates_T = list(px.index[260::IC_STRIDE])                     # idea 623's sampling, verbatim
    cut = px.index[px.index <= IS_END]
    ic_dates_H = [t for t in px.index[260::IC_STRIDE]
                  if t <= cut[-1] and px.index.get_loc(t) + FWD_H < len(px)
                  and px.index[px.index.get_loc(t) + FWD_H] <= IS_END]
    say(f"  LEAKT dates: {len(ic_dates_T)} ({ic_dates_T[0].date()}..{ic_dates_T[-1].date()}), "
        f"forward return to {px.index[-1].date()} -- ORACLE.")
    say(f"  LEAKH dates: {len(ic_dates_H)} ({ic_dates_H[0].date()}..{ic_dates_H[-1].date()}), "
        f"{FWD_H}d forward, every input dated on or before {IS_END.date()} -- IMPLEMENTABLE.")
    say("")

    crows = []
    for i, (name, (fn, sleak, tdate, fam)) in enumerate(KEY_SPECS.items()):
        k = fn(px, vol, sh)
        a1, med1 = disp_T1(fn, px, vol, sh, np.random.default_rng(SEED + 101 * i))
        a2, med2 = disp_T2(fn, px, vol, sh, shares_asof)
        crows.append(dict(key=name, family=fam, truth_scale_leak=sleak, truth_term_dated=tdate,
                          T1_flag=bool(med1 > TOL_STEPS), T1_med=med1, T1_max=a1,
                          T2_flag=bool(med2 > TOL_STEPS), T2_med=med2, T2_max=a2,
                          absIC_T=abs(mean_ic(k, fwd_T, ic_dates_T)),
                          absIC_H=abs(mean_ic(k, fwd_H, ic_dates_H))))
    C = pd.DataFrame(crows)
    flagT1 = dict(zip(C.key, C.T1_flag))
    flagT2 = dict(zip(C.key, C.T2_flag))
    icT = dict(zip(C.key, C.absIC_T))
    icH = dict(zip(C.key, C.absIC_H))

    say(f"{'key':10s} {'family':9s} {'scale?':7s} {'term?':6s} {'T1':>5s} {'T1med':>7s} "
        f"{'T2':>5s} {'T2med':>7s} {'|IC|T':>7s} {'|IC|H':>7s}")
    for _, r in C.iterrows():
        say(f"{r['key']:10s} {r['family']:9s} {str(r['truth_scale_leak']):7s} "
            f"{str(r['truth_term_dated']):6s} {('FLAG' if r['T1_flag'] else '  .'):>5s} "
            f"{r['T1_med']:7.1f} {('FLAG' if r['T2_flag'] else '  .'):>5s} {r['T2_med']:7.1f} "
            f"{r['absIC_T']:7.4f} {r['absIC_H']:7.4f}")
    C.to_csv(OUT / f"{STEM}.certs.csv", index=False)
    say("")

    # G3 / G5: reproduce idea 623's committed certificate flags on the 20 shared keys, under a
    # DIFFERENT rng seed, and its committed arms rows.
    c623 = pd.read_csv(OUT / f"{P623}.certs.csv").set_index("key")
    sh623 = C[C.key.isin(SHARED_623)].set_index("key")
    d1 = int((sh623["T1_flag"] != c623.loc[sh623.index, "T1_flag"]).sum())
    d2 = int((sh623["T2_flag"] != c623.loc[sh623.index, "T2_flag"]).sum())
    say(f"  G5  idea 623's certificate FLAGS reproduced on the {len(sh623)} shared keys under a "
        f"NEW seed ({SEED} vs 623):  T1 disagreements {d1}   T2 disagreements {d2}   [tol 0]")
    repro.append(dict(gate="G5_flags_reproduce_623", value=float(d1 + d2), tol=0.0,
                      passed=(d1 + d2) == 0))

    say("")
    say("SEPARATION ON THE SCALE AXIS.  The operative set is the T2-CLEARED one: dating is")
    say("already gated (idea 623), so the only question is what is left to catch.")
    T2clear = C[~C.T2_flag].copy()
    say(f"  T2-cleared keys: {len(T2clear)} of {len(C)} "
        f"({', '.join(sorted(T2clear.key))})")
    say(f"  ... of which SCALE-LEAKING (truth): {int(T2clear.truth_scale_leak.sum())} "
        f"({', '.join(sorted(T2clear.loc[T2clear.truth_scale_leak, 'key']))})")
    say("")
    aucs = {}
    for lab, col in (("T1_med", "T1_med"), ("LEAKT", "absIC_T"), ("LEAKH", "absIC_H")):
        aucs[lab] = (auc(T2clear[col], T2clear.truth_scale_leak),
                     auc(C[col], C.truth_scale_leak))
    say(f"  AUC for the SCALE axis:   {'screen':8s} {'T2-cleared':>11s} {'all keys':>9s}")
    for lab, (a_t2, a_all) in aucs.items():
        say(f"                            {lab:8s} {a_t2:11.4f} {a_all:9.4f}")
    say("")

    say("THRESHOLD LADDER (every point reported; no tau is selected).  On the T2-cleared set:")
    say(f"  {'screen':6s} {'tau':>5s} {'admits':>6s} {'TP':>3s} {'FP':>3s} {'FN':>3s} {'TN':>3s} "
        f"{'catches PXDVOL':>14s} {'causal killed':>13s}  keys flagged")
    lrows = []
    for lab, col in (("LEAKT", "absIC_T"), ("LEAKH", "absIC_H")):
        for tau in TAUS:
            fl = T2clear[col] > tau
            tp = int((fl & T2clear.truth_scale_leak).sum())
            fp = int((fl & ~T2clear.truth_scale_leak).sum())
            fn_ = int((~fl & T2clear.truth_scale_leak).sum())
            tn = int((~fl & ~T2clear.truth_scale_leak).sum())
            killed = sorted(T2clear.loc[fl & (T2clear.family == "causal"), "key"])
            catches = bool(fl[T2clear.key == "PXDVOL"].any())
            lrows.append(dict(screen=lab, tau=tau, n_admitted=int((~fl).sum()), TP=tp, FP=fp,
                              FN=fn_, TN=tn, catches_PXDVOL=catches, n_causal_killed=len(killed),
                              causal_killed=";".join(killed),
                              flagged=";".join(sorted(T2clear.loc[fl, "key"]))))
            if tau in (0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70):
                say(f"  {lab:6s} {tau:5.2f} {int((~fl).sum()):6d} {tp:3d} {fp:3d} {fn_:3d} "
                    f"{tn:3d} {str(catches):>14s} {len(killed):13d}  "
                    f"{';'.join(sorted(T2clear.loc[fl, 'key']))[:44]}")
    L = pd.DataFrame(lrows)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    clean = L[(L.TP == int(T2clear.truth_scale_leak.sum())) & (L.FP == 0)]
    say("")
    say(f"  thresholds achieving T1's own reading (all scale leaks caught, zero false "
        f"positives): {len(clean)} of {len(L)}")
    if len(clean):
        for _, r in clean.iterrows():
            say(f"    {r['screen']} tau={r['tau']}")
    say(f"  T1 on the same set: TP {int((T2clear.T1_flag & T2clear.truth_scale_leak).sum())}  "
        f"FP {int((T2clear.T1_flag & ~T2clear.truth_scale_leak).sum())}  "
        f"FN {int((~T2clear.T1_flag & T2clear.truth_scale_leak).sum())}  "
        f"TN {int((~T2clear.T1_flag & ~T2clear.truth_scale_leak).sum())}")
    say("")

    # ------------------------------------------------- PART A2 (POST-HOC): the separating BAND
    say("-" * 112)
    say("PART A2  THE BAND  [POST-HOC -- added after the ladder above was read, and every number")
    say("         below is labelled ORACLE-PLACED: the band can only be located by someone who")
    say("         already knows which keys are leaks, which is exactly what T1 certifies.]")
    say("-" * 112)

    def band(sub, col):
        lo = float(sub.loc[~sub.truth_scale_leak, col].max())
        hi = float(sub.loc[sub.truth_scale_leak, col].min())
        return lo, hi, hi - lo

    bands = {}
    step = TAUS[1] - TAUS[0]
    say(f"  {'screen':7s} {'max non-leak':>13s} {'min leak':>9s} {'band width':>11s} "
        f"{'in ladder steps':>16s} {'separable':>10s}")
    for lab, col in (("T1_med", "T1_med"), ("LEAKT", "absIC_T"), ("LEAKH", "absIC_H")):
        lo, hi, wdt = band(T2clear, col)
        bands[lab] = (lo, hi, wdt)
        say(f"  {lab:7s} {lo:13.4f} {hi:9.4f} {wdt:11.4f} {wdt / step:16.3f} "
            f"{str(wdt > 0):>10s}")
    say(f"  (one ladder step = {step:.2f}; T1's 'band' is the gap between a structural zero and "
        f"the first flagged key, in RANK STEPS, and needs no threshold to be placed at all.)")
    say("")

    # does the band survive re-estimation on two disjoint halves of the IS window?
    mid = ic_dates_H[len(ic_dates_H) // 2]
    subw = {"IS-early": [t for t in ic_dates_H if t < mid],
            "IS-late": [t for t in ic_dates_H if t >= mid]}
    say("  STABILITY: |IC|_H re-estimated on two disjoint halves of its own IS date set")
    say(f"  {'window':9s} {'dates':>5s} {'AUC (scale)':>11s} {'max non-leak':>13s} "
        f"{'min leak':>9s} {'width':>8s} {'full-band tau* still clean?':>28s}")
    tau_star = (bands["LEAKH"][0] + bands["LEAKH"][1]) / 2.0 if bands["LEAKH"][2] > 0 else np.nan
    srows = []
    for wname, dts in subw.items():
        vals = {}
        for kname, (fn, _, _, _) in KEY_SPECS.items():
            vals[kname] = abs(mean_ic(fn(px, vol, sh), fwd_H, dts))
        sub = T2clear.copy()
        sub["ic_w"] = sub.key.map(vals)
        a = auc(sub.ic_w, sub.truth_scale_leak)
        lo, hi, wdt = band(sub, "ic_w")
        if np.isnan(tau_star):
            clean = False
        else:
            fl = sub.ic_w > tau_star
            clean = bool((fl == sub.truth_scale_leak).all())
        say(f"  {wname:9s} {len(dts):5d} {a:11.4f} {lo:13.4f} {hi:9.4f} {wdt:8.4f} "
            f"{str(clean):>28s}")
        srows.append(dict(window=wname, n_dates=len(dts), auc_scale=a, max_nonleak=lo,
                          min_leak=hi, width=wdt, tau_star=tau_star, tau_star_clean=clean))
    pd.DataFrame(srows).to_csv(OUT / f"{STEM}.stability.csv", index=False)
    say(f"  tau* (band midpoint on the FULL IS date set, ORACLE-PLACED) = {tau_star:.4f}")
    say("")

    # ============================================================ PART C -- CONSEQUENCE BOOK
    say("=" * 112)
    say("PART C  THE GATE PRICED WHERE IT SITS: BEFORE RULE 8   (SMALL430, top-20 EW, g=0.75, W)")
    say("=" * 112)
    spy = spy_px.pct_change().fillna(0).loc[start:]
    srow = full_row(spy)
    ctrl = {c: full_row(g0.loc[start:] - t0turn.loc[start:] * c / 1e4) for c in COSTS}
    b1 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
    b2 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
    v1 = {c: full_row(b1["returns"].loc[start:] - b1["turnover"].loc[start:] * c / 1e4)
          for c in COSTS}
    v2 = {c: full_row(b2["returns"].loc[start:] - b2["turnover"].loc[start:] * c / 1e4)
          for c in COSTS}
    say(f"  SPY                        {srow['CAGR_F']:7.2%} / {srow['Sharpe_F']:6.3f} / "
        f"{srow['MaxDD_F']:7.2%}   (H1 {srow['Sharpe_H1']:.3f} / H2 {srow['Sharpe_H2']:.3f} / "
        f"OOS {srow['Sharpe_OOS']:.3f})")
    for nm, rr in (("control (untilted composite)", ctrl), ("RULES v1", v1),
                   ("RULES v2 (live baseline)", v2)):
        r = rr[10.0]
        say(f"  {nm:26s} {r['CAGR_F']:7.2%} / {r['Sharpe_F']:6.3f} / {r['MaxDD_F']:7.2%}   "
            f"(H1 {r['Sharpe_H1']:.3f} / H2 {r['Sharpe_H2']:.3f} / OOS {r['Sharpe_OOS']:.3f})")
    say("")

    arms = []
    for c in COSTS:
        r = dict(key="CONTROL", family="control", dir="-", m=0.0, cost=c, T1_flag=False,
                 T2_flag=False, absIC_T=np.nan, absIC_H=np.nan,
                 turnover_yr=float(t0turn.sum() / (len(t0turn) / 252)))
        r.update(ctrl[c])
        r["dSharpe_F"] = 0.0
        r["dSharpe_IS"] = 0.0
        r["dSharpe_OOS"] = 0.0
        r["pass4a"] = pass4a(r, v2[c])
        r["pass4b"] = pass4b(r, srow)
        arms.append(r)
    for kname, (fn, _, _, fam) in KEY_SPECS.items():
        kv = fn(px, vol, sh)
        for dname, sgn in DIRS.items():
            for m in MS:
                s_ = comp + sgn * m * (kv - 0.5)
                rr_ = s_.where(elig).rank(axis=1, ascending=False)
                w_ = (rr_ <= N).astype(float) * (GROSS / N)
                g_, t_ = fast_backtest(px, w_)
                g_, t_ = g_.loc[start:], t_.loc[start:]
                ty = float(t_.sum() / (len(t_) / 252))
                for c in COSTS:
                    row = dict(key=kname, family=fam, dir=dname, m=m, cost=c,
                               T1_flag=bool(flagT1[kname]), T2_flag=bool(flagT2[kname]),
                               absIC_T=icT[kname], absIC_H=icH[kname], turnover_yr=ty)
                    row.update(full_row(g_ - t_ * c / 1e4))
                    row["dSharpe_F"] = row["Sharpe_F"] - ctrl[c]["Sharpe_F"]
                    row["dSharpe_IS"] = row["Sharpe_IS"] - ctrl[c]["Sharpe_IS"]
                    row["dSharpe_OOS"] = row["Sharpe_OOS"] - ctrl[c]["Sharpe_OOS"]
                    row["pass4a"] = pass4a(row, v2[c])
                    row["pass4b"] = pass4b(row, srow)
                    arms.append(row)
    A = pd.DataFrame(arms)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    say(f"  {len(A)} grid points written to .arms.csv  ({len(KEY_SPECS)} keys x 2 dirs x "
        f"{len(MS)} m x {len(COSTS)} rungs + control)")
    say(f"  PROTOCOL 4 over the whole grid: 4a {int(A.pass4a.sum())}/{len(A)}   "
        f"4b {int(A.pass4b.sum())}/{len(A)}")
    fails = {"MaxDD": int((A.MaxDD_F < DELTA * srow["MaxDD_F"]).sum()),
             "CAGR": int((A.CAGR_F < PHI * srow["CAGR_F"]).sum()),
             "H1": int((A.Sharpe_H1 <= srow["Sharpe_H1"]).sum()),
             "H2": int((A.Sharpe_H2 <= srow["Sharpe_H2"]).sum()),
             "OOS": int((A.Sharpe_OOS <= srow["Sharpe_OOS"]).sum())}
    say("  4b leg failure counts: " + "  ".join(f"{k} {v}" for k, v in
                                                sorted(fails.items(), key=lambda z: -z[1])))

    # G3: reproduce idea 623's committed arms rows on the shared keys
    a623 = pd.read_csv(OUT / f"{P623}.arms.csv")
    mrg = A.merge(a623, on=["key", "dir", "m", "cost"], suffixes=("", "_623"))
    g3 = float(np.nanmax(np.abs(pd.concat([
        mrg["Sharpe_F"] - mrg["Sharpe_F_623"], mrg["CAGR_F"] - mrg["CAGR_F_623"],
        mrg["MaxDD_F"] - mrg["MaxDD_F_623"], mrg["Sharpe_OOS"] - mrg["Sharpe_OOS_623"]]).values)))
    say("")
    say(f"  G3  idea 623's committed .arms.csv reproduced on {len(mrg)} shared rows "
        f"(CAGR_F, Sharpe_F, MaxDD_F, Sharpe_OOS)   max |diff| {g3:.3e}   [tol {REPRO_TOL:g}]")
    repro.append(dict(gate="G3_reproduce_623_arms", value=g3, tol=REPRO_TOL, passed=g3 < REPRO_TOL))
    say("")

    # ============================================================ PART B -- THE LEAK LAW AS PRICER
    say("=" * 112)
    say("PART B  IDEA 185's LEAK LAW AS A PRICER on this corpus (10 bps, dirs and m pooled)")
    say("=" * 112)
    a10 = A[(A.cost == 10.0) & (A.key != "CONTROL")]
    per_key = a10.groupby("key").agg(mean_dS_F=("dSharpe_F", "mean"),
                                     mean_dS_OOS=("dSharpe_OOS", "mean"),
                                     max_dS_OOS=("dSharpe_OOS", "max")).reset_index()
    per_key = per_key.merge(C[["key", "family", "truth_scale_leak", "truth_term_dated",
                               "T1_flag", "T2_flag", "absIC_T", "absIC_H"]], on="key")
    # NEG-direction reading, as idea 185 published it
    neg = a10[a10.dir == "NEG"].groupby("key")["dSharpe_F"].mean().rename("mean_dS_NEG")
    per_key = per_key.merge(neg, on="key")
    beats = a10.assign(b=a10.Sharpe_OOS > srow["Sharpe_OOS"]).groupby("key")["b"].any()
    per_key["any_arm_beats_SPY_OOS"] = per_key.key.map(beats)
    per_key.to_csv(OUT / f"{STEM}.pricer.csv", index=False)
    say(f"  Spearman(|IC|_T , mean NEG dSharpe_F)  = {spearman(per_key.absIC_T, per_key.mean_dS_NEG):+.4f}"
        f"    (idea 185 published +0.881 on its small panel)")
    say(f"  Spearman(|IC|_H , mean NEG dSharpe_F)  = {spearman(per_key.absIC_H, per_key.mean_dS_NEG):+.4f}")
    say(f"  Spearman(|IC|_T , max dSharpe_OOS)     = {spearman(per_key.absIC_T, per_key.max_dS_OOS):+.4f}")
    say(f"  Spearman(|IC|_H , max dSharpe_OOS)     = {spearman(per_key.absIC_H, per_key.max_dS_OOS):+.4f}")
    say("")
    say("  AUC for the event 'some arm of this key beats SPY OOS' "
        f"({int(per_key.any_arm_beats_SPY_OOS.sum())} of {len(per_key)} keys):")
    for lab, col in (("|IC|_T", "absIC_T"), ("|IC|_H", "absIC_H"),
                     ("T1_flag", "T1_flag"), ("T2_flag", "T2_flag"),
                     ("T1|T2", None)):
        s = (per_key.T1_flag | per_key.T2_flag).astype(float) if col is None \
            else per_key[col].astype(float)
        say(f"    {lab:8s} AUC {auc(s, per_key.any_arm_beats_SPY_OOS):.4f}")
    say("")

    # ------------------------------------------------------- PROTOCOL 8, gate x family x rung
    say("-" * 112)
    say("RULE 8 (PROTOCOL 8): (KEY, m) chosen on 2010-2016 IS Sharpe ALONE; 2017-2026 read once.")
    say("The GATE is applied BEFORE the choice.  Both tuned parameters vary here: GATE x FAMILY.")
    say("-" * 112)
    GATES = {"NONE": lambda k: True,
             "T1": lambda k: not flagT1[k],
             "T2": lambda k: not flagT2[k],
             "T1&T2": lambda k: (not flagT1[k]) and (not flagT2[k])}
    for tau in TAUS:
        GATES[f"LEAKT>{tau:.2f}"] = (lambda k, t=tau: not (icT[k] > t))
        GATES[f"LEAKH>{tau:.2f}"] = (lambda k, t=tau: not (icH[k] > t))
        GATES[f"T2&LEAKT>{tau:.2f}"] = (lambda k, t=tau: (not flagT2[k]) and not (icT[k] > t))
        GATES[f"T2&LEAKH>{tau:.2f}"] = (lambda k, t=tau: (not flagT2[k]) and not (icH[k] > t))
    if not np.isnan(tau_star):                     # POST-HOC, ORACLE-PLACED (PART A2)
        GATES["LEAKH>tau*"] = (lambda k, t=tau_star: not (icH[k] > t))
        GATES["T2&LEAKH>tau*"] = (lambda k, t=tau_star: (not flagT2[k]) and not (icH[k] > t))
    FAMILIES = ["ALL", "causal", "level", "both", "termonly"]

    wf = []
    for gname, gfn in GATES.items():
        for fam in FAMILIES:
            adm = [k for k in KEY_SPECS if gfn(k)
                   and (fam == "ALL" or KEY_SPECS[k][3] == fam)]
            admset = set(adm)
            for c in COSTS:
                sub = A[(A.cost == c) & (A.key.isin(admset))]
                if len(sub):
                    pick = sub.loc[sub.Sharpe_IS.idxmax()]
                    tag = f"{pick['key']}/{pick['dir']}/m={pick['m']:.2f}"
                else:
                    pick = A[(A.cost == c) & (A.key == "CONTROL")].iloc[0]
                    tag = "CONTROL (nothing admitted)"
                wf.append(dict(gate=gname, family=fam, cost=c, n_admitted=len(adm),
                               admitted=";".join(sorted(adm)), pick=tag, pick_key=pick["key"],
                               pick_family=pick["family"],
                               pick_scale_leak=bool(KEY_SPECS[pick["key"]][1])
                               if pick["key"] in KEY_SPECS else False,
                               pick_term_dated=bool(KEY_SPECS[pick["key"]][2])
                               if pick["key"] in KEY_SPECS else False,
                               Sharpe_IS=pick["Sharpe_IS"], CAGR_OOS=pick["CAGR_OOS"],
                               Sharpe_OOS=pick["Sharpe_OOS"], MaxDD_OOS=pick["MaxDD_OOS"],
                               CAGR_F=pick["CAGR_F"], Sharpe_F=pick["Sharpe_F"],
                               MaxDD_F=pick["MaxDD_F"], Sharpe_H1=pick["Sharpe_H1"],
                               Sharpe_H2=pick["Sharpe_H2"],
                               spy_CAGR_OOS=srow["CAGR_OOS"], spy_Sharpe_OOS=srow["Sharpe_OOS"],
                               spy_MaxDD_OOS=srow["MaxDD_OOS"],
                               v2_CAGR_OOS=v2[c]["CAGR_OOS"], v2_Sharpe_OOS=v2[c]["Sharpe_OOS"],
                               v2_MaxDD_OOS=v2[c]["MaxDD_OOS"], v1_Sharpe_OOS=v1[c]["Sharpe_OOS"],
                               ctrl_Sharpe_OOS=ctrl[c]["Sharpe_OOS"],
                               beats_spy_OOS=bool(pick["Sharpe_OOS"] > srow["Sharpe_OOS"]),
                               beats_v2_OOS=bool(pick["Sharpe_OOS"] > v2[c]["Sharpe_OOS"]),
                               pass4a=bool(pick["pass4a"]), pass4b=bool(pick["pass4b"])))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"  {len(W)} gate x family x rung cells written to .walkforward.csv "
        f"({len(GATES)} gates x {len(FAMILIES)} families x {len(COSTS)} rungs)")
    say("")
    say(f"  OOS comparands @10bps: SPY {srow['CAGR_OOS']:.2%}/{srow['Sharpe_OOS']:.3f}/"
        f"{srow['MaxDD_OOS']:.2%}   RULES v2 {v2[10.0]['CAGR_OOS']:.2%}/"
        f"{v2[10.0]['Sharpe_OOS']:.3f}/{v2[10.0]['MaxDD_OOS']:.2%}   RULES v1 "
        f"{v1[10.0]['CAGR_OOS']:.2%}/{v1[10.0]['Sharpe_OOS']:.3f}   control "
        f"{ctrl[10.0]['CAGR_OOS']:.2%}/{ctrl[10.0]['Sharpe_OOS']:.3f}")
    say("")
    say("  FAMILY=ALL, the four structural gates and the tau ladder at every 4th rung:")
    say(f"  {'gate':16s} {'rung':>4s} {'adm':>4s} {'pick':24s} {'IS Shrp':>8s} {'OOS CAGR':>9s} "
        f"{'OOS Shrp':>9s} {'OOS MaxDD':>10s} {'vs SPY':>8s} {'vs v2':>7s}")
    show = ["NONE", "T1", "T2", "T1&T2"] + \
           [g for g in GATES if g.startswith(("LEAKH", "T2&LEAKH")) and
            any(g.endswith(f">{t:.2f}") for t in (0.10, 0.20, 0.30, 0.40, 0.50, 0.60))] + \
           [g for g in GATES if g.startswith("T2&LEAKT") and
            any(g.endswith(f">{t:.2f}") for t in (0.20, 0.40, 0.60))] + \
           [g for g in ("LEAKH>tau*", "T2&LEAKH>tau*") if g in GATES]
    for gname in show:
        for _, r in W[(W.gate == gname) & (W.family == "ALL")].iterrows():
            say(f"  {gname:16s} {r['cost']:4.0f} {r['n_admitted']:4d} {r['pick'][:24]:24s} "
                f"{r['Sharpe_IS']:8.3f} {r['CAGR_OOS']:9.2%} {r['Sharpe_OOS']:9.3f} "
                f"{r['MaxDD_OOS']:10.2%} {r['Sharpe_OOS'] - srow['Sharpe_OOS']:+8.3f} "
                f"{r['Sharpe_OOS'] - v2[r['cost']]['Sharpe_OOS']:+7.3f}")
    say("")
    WA = W[W.family == "ALL"]
    say("  gate summary on FAMILY=ALL (beats-SPY-OOS out of 3 rungs; a gate that works should "
        "NOT beat SPY):")
    for gname in show:
        s = WA[WA.gate == gname]
        say(f"    {gname:16s} admits {int(s.n_admitted.iloc[0]):2d}  beats SPY OOS "
            f"{int(s.beats_spy_OOS.sum())}/3   picks a SCALE-LEAK {int(s.pick_scale_leak.sum())}/3"
            f"   picks a TERMINAL {int(s.pick_term_dated.sum())}/3   "
            f"mean OOS Sharpe {s.Sharpe_OOS.mean():+.3f}")
    say("")
    say("  the KEY-FAMILY cut (10 bps, the four structural gates):")
    say(f"    {'gate':7s} " + "".join(f"{f:>26s}" for f in FAMILIES))
    for gname in ("NONE", "T1", "T2", "T1&T2"):
        cells = []
        for fam in FAMILIES:
            r = W[(W.gate == gname) & (W.family == fam) & (W.cost == 10.0)]
            r = r.iloc[0]
            cells.append(f"{r['pick_key'][:10]:>10s} {r['Sharpe_OOS']:+6.3f}"
                         f"{'*' if r['beats_spy_OOS'] else ' '}    ")
        say(f"    {gname:7s} " + "".join(f"{c:>26s}" for c in cells))
    say("    (* = beats SPY out of sample; SPY OOS Sharpe "
        f"{srow['Sharpe_OOS']:.3f})")
    say("")

    # the decisive marginal reading: T1 given T2, and the cheapest LEAKH that matches it
    honest = WA[(WA.beats_spy_OOS == False)].groupby("gate").size()  # noqa: E712
    fully_honest = sorted([g for g in honest.index if honest[g] == 3])
    say(f"  gates whose pick LOSES to SPY OOS at all 3 rungs ({len(fully_honest)} of "
        f"{len(GATES)}): {', '.join(fully_honest[:14])}"
        f"{' ...' if len(fully_honest) > 14 else ''}")
    t1t2_adm = set(k for k in KEY_SPECS if not flagT1[k] and not flagT2[k])
    same_set = []
    for g in fully_honest:
        adm = set(WA[WA.gate == g].admitted.iloc[0].split(";")) if \
            WA[WA.gate == g].admitted.iloc[0] else set()
        if g.startswith(("LEAKH", "T2&LEAKH", "LEAKT", "T2&LEAKT")):
            same_set.append((g, len(adm), len(adm & t1t2_adm), adm == t1t2_adm))
    say(f"  T1&T2 admits {len(t1t2_adm)}: {', '.join(sorted(t1t2_adm))}")
    if same_set:
        say("  honest LEAK-based gates vs the T1&T2 admitted set:")
        for g, na, ov, eq in same_set[:12]:
            say(f"    {g:18s} admits {na:2d}  overlap with T1&T2 {ov:2d}  identical set {eq}")
    else:
        say("  no LEAK-based gate is honest at any tau on the ladder.")
    say("")

    # ============================================================ PART D -- predictions scored
    say("=" * 112)
    say("PART D  PRE-REGISTERED PREDICTIONS, SCORED")
    say("=" * 112)
    R = pd.DataFrame(repro)
    R.to_csv(OUT / f"{STEM}.repro.csv", index=False)
    p1 = bool(R.passed.all())
    lh = L[(L.screen == "LEAKH") & L.catches_PXDVOL]
    p2 = bool(len(lh) == 0 or (lh.n_causal_killed > 0).all())
    picks_t2 = list(W[(W.gate == "T2") & (W.family == "ALL")].sort_values("cost").pick_key)
    picks_t1t2 = list(W[(W.gate == "T1&T2") & (W.family == "ALL")].sort_values("cost").pick_key)
    n_changed = sum(1 for a, b in zip(picks_t2, picks_t1t2) if a != b)
    p3 = n_changed >= 2
    p4 = bool(aucs["LEAKT"][0] > aucs["LEAKH"][0])
    # P5 is scored on the pre-registered LADDER only; the post-hoc tau* gate is excluded here and
    # reported separately, because its threshold was placed with the ground truth in hand.
    hon_h = [g for g in fully_honest if g.startswith("T2&LEAKH") and "tau*" not in g]
    p5 = bool(len(hon_h) > 0 and any(
        set(WA[WA.gate == g].admitted.iloc[0].split(";")) != t1t2_adm for g in hon_h))
    p6 = int(A.pass4a.sum()) == 0 and int(A.pass4b.sum()) == 0
    for tag, ok, txt in [
        ("P1", p1, f"gates all pass ({int(R.passed.sum())}/{len(R)})"),
        ("P2", p2, f"LEAKH taus catching PXDVOL: {len(lh)}; of those, taus that kill NO causal "
                   f"key: {int((lh.n_causal_killed == 0).sum()) if len(lh) else 0}"),
        ("P3", p3, f"T2 picks {picks_t2} -> T1&T2 picks {picks_t1t2} ({n_changed}/3 changed)"),
        ("P4", p4, f"AUC on the T2-cleared scale axis: LEAKT {aucs['LEAKT'][0]:.4f} vs LEAKH "
                   f"{aucs['LEAKH'][0]:.4f}"),
        ("P5", p5, f"honest T2&LEAKH gates: {hon_h[:6]}"),
        ("P6", p6, f"4a {int(A.pass4a.sum())}/{len(A)}, 4b {int(A.pass4b.sum())}/{len(A)}")]:
        say(f"  {tag} {'HIT ' if ok else 'MISS'}  {txt}")
    say("")
    say(f"runtime {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
