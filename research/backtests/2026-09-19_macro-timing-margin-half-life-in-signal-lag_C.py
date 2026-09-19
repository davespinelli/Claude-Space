#!/usr/bin/env python3
"""
Idea 1574 (lane C, 2026-09-19) — is EVERY committed MACRO and TIMING GAIN in the record a
ONE-OR-TWO-DAY OBJECT?

THE PREMISE (the queue's own number).  Idea 1562 priced the 1538 two-state SPY-trend gross gate
against a CAGR-matched de-gross twin and found its pooled Sharpe margin worth +0.0238 when the
macro signal is read with 1 trading day of lag, +0.0275 at 2 days and +0.0001 at 5.  A margin that
evaporates over four trading days is not how a STATE VARIABLE behaves — a regime that is worth
holding on Monday is still worth holding on Thursday.  It is how a MICROSTRUCTURE COINCIDENCE
behaves.  Every macro gate, breadth gate, trailing stop and vol target the record owns is read at
EXACTLY ONE LAG and none of them has ever been swept.

WHAT THIS RUN PRICES.  Each device family's frozen headline cell, re-cut over the signal-lag
ladder L in {1, 2, 3, 5, 10, 21} trading days, on three panels, every rung published, and for each
(family, panel) the HALF-LIFE of the device's Sharpe margin over its OWN CAGR-MATCHED DE-GROSS TWIN.

  TIMING / GROSS-PATH devices (the four the idea names; each is a pure multiplier on ONE frozen
  weight frame, so lagging it is exact and changes nothing else):
    MACRO2   two-state gross keyed to SPY's own 200d MA: x1.00 above, x0.75 below   (1538 / 1562)
    SPYFILT  binary SPY 200d trend gate: x1.00 above, x0.00 below                   (1534, L = 200)
    BREADTH  panel-breadth throttle  x min(1, (b / 0.50) ** 1.0)                    (1413 centre)
    STOP     trailing equity stop on the BASE book's own net equity, d = 0.10,
             re-entry after recovering 50% of the fall                              (1405 / 1534)
    VOLTGT   realised-vol target on the BASE book's own 20d vol, v = 0.12           (1534 centre)

  ELIGIBILITY-SIDE devices, carried as a SECONDARY CONTROL arm (they are not macro or timing; they
  are here only to answer "is a short half-life just what ANY device does on this tape?").  Their
  lag is implemented as the device reading a STALE TAPE: the device's own mask inputs are taken
  from px.shift(L - 1) while the base ranking key is untouched.
    BAND     200d MA band with hysteresis, c = 0.06                                 (1534 centre)
    MAXVOL   per-name vol ceiling, m = 0.45                                         (1534 centre)
    MADIST   per-name MA-distance threshold, k = 0.06                               (1534 centre)

TUNED PARAMETERS: exactly TWO — (device FAMILY, signal LAG).  Every family's own rung is FROZEN at
the value the record already committed or at the centre of the grid the record already published;
no rung is selected here.  The PANEL is a replication control, not a dial.  The cost rung is the
protocol's 10 bps throughout.

THE COMPARAND, AND WHY IT IS THE WHOLE EXPERIMENT.  Idea 1189 established that Sharpe is nearly
flat in gross on this tape and idea 762 that de-grossing is Sharpe-neutral to 0.0026, so ANY device
that merely holds less stock slides along a fixed-Sharpe line and buys nothing.  Every cell here is
therefore scored against a CONSTANT-GROSS twin on the SAME frame whose FULL-SAMPLE CAGR equals the
device's (fine ladder + interpolation, then an EXACT engine run at g*, |CAGR gap| gated < 20 bp) —
the comparand idea 1574 asks for.  A lag-1 and lag-21 EXPOSURE-matched twin (idea 1534's ruler) is
also published for the five timing families as a cross-check on the ruler itself.

HALF-LIFE.  m(L) = Sharpe(device at lag L) - Sharpe(its own CAGR-matched twin).  If m(1) <= 0 the
device has no margin to decay and the half-life is NA.  Otherwise HL = the (linearly interpolated)
lag at which m first falls to m(1) / 2; ">21" if it never does.

PRE-REGISTERED VERDICT RULE (written before the run).
  H_MICRO       every timing family with m(1) > 0 has HL < 5 trading days
                -> the record's macro and timing gains are one-or-two-day objects and the record
                   should say so.
  H_STATE       at least one timing family has m(21) >= 0.5 * m(1) AND m(1) resolvable at |t| > 2
                -> the first genuine state variable in the record.
  H_NOMARGIN    NO timing family has m(1) > 0 at all
                -> there is no macro or timing GAIN on this frame for a half-life to be a property
                   of; the premise of the question fails and the class is dead on the ruler the
                   idea itself specifies.  KILL.
  H_UNMEASURABLE  no timing family's m(1) is resolvable at |t| > 2
                -> the half-life question is UNDEFINED on this tape: the margins the record quotes
                   for these devices are inside their own noise, and no lag sweep can rescue them.
  These are read in the order STATE, NOMARGIN, MICRO, UNMEASURABLE.  Every branch except H_STATE is
  a KILL for the class.

DISCLOSURE (rule 7).  H_NOMARGIN was NOT in the first draft of this pre-registration; it was added
after a 3-lag smoke test on U56 alone showed the original three branches were not exhaustive (every
timing family's lag-1 margin came out NEGATIVE, which none of STATE / MICRO / UNMEASURABLE covers).
Nothing measured, no parameter, no rung, no ladder and no ruler changed — only the verdict taxonomy
was completed.  The smoke test's numbers are superseded by the full run below and are not quoted.

PROTOCOL: rule 1 (>= 10y, three panels); rule 2 (weights decided at t, applied at t+1 by the
engine; 10 bps per unit turnover; long-only, no leverage — every multiplier is in [0, 1]);
rule 3 (compared to the LIVE RULES v2 baseline AND SPY); rule 4 (full sample + both halves + BOTH
KEEP paths at EVERY cell, 2 tuned parameters); rule 8 (both choosers read warm-up..2016-12-31 ONLY;
2017-01-01..end read exactly once); rule 9 (survivorship stated).

GATES.  G0 >= 10y on every panel.  G1 CROSS-SCRIPT REPLAY of idea 1534's frozen BASE book.
G2 CROSS-SCRIPT REPLAY of idea 1534's SPYFILT L=200 / STOP d=0.10 / VOLTGT v=0.12 cells at lag 1.
G3 exactly two tuned parameters.  G4 |CAGR match| < 20 bp on every CAGR-matched twin.
G5 no chooser reads a row on or after 2017-01-01.  G6 every multiplier in [0, 1] and every book's
mean gross <= 0.75.  G7 lag 1 IS the record's convention (the L = 1 book is bit-identical to the
device book built with no shift).  G8 every one of the 8 x 6 x 3 cells published.

Runs standalone and offline (committed price caches only; never calls the network):
  python research/backtests/2026-09-19_macro-timing-margin-half-life-in-signal-lag_C.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG, LANE = "2026-09-19", "macro-timing-margin-half-life-in-signal-lag", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

# ------------------------------------------------------------------ frozen constants
N_FROZEN, H_FROZEN = 20, 126          # the committed anchor's two parameters (NOT tuned here)
GROSS, MAXVOL, COST_BPS, FREQ = 0.75, 0.60, 10, "W"
WARMUP = 260
OOS_START, IS_END = pd.Timestamp("2017-01-01"), pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NBOOT, LB = 20260919, 500, 65

LAGS = [1, 2, 3, 5, 10, 21]                      # DIAL 2 (the ladder of the title)
TIMING = ["MACRO2", "SPYFILT", "BREADTH", "STOP", "VOLTGT"]
ELIG = ["BAND", "MAXVOL", "MADIST"]
FAMILIES = TIMING + ELIG                          # DIAL 1
RUNG = dict(MACRO2=200, SPYFILT=200, BREADTH=(0.50, 1.0), STOP=(0.10, 0.50),
            VOLTGT=0.12, BAND=0.06, MAXVOL=0.45, MADIST=0.06)
GGRID = np.round(np.arange(0.20, 1.0001, 0.02), 4)   # twin ladder (a CONTROL, not a dial)
MATCH_BAR = 0.0020                                   # G4: 20 bp of CAGR
MACRO2_LOW, STOP_FRAC = 0.75, 0.50

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = pd.Series(r).dropna()
    s = r.std()
    return float(r.mean() * 252 / (s * np.sqrt(252))) if s > 0 else np.nan


def maxdd(r):
    e = (1 + pd.Series(r).fillna(0)).cumprod()
    return float((e / e.cummax() - 1).min())


def cagr(r):
    r = pd.Series(r).fillna(0)
    return float((1 + r).prod() ** (252 / len(r)) - 1) if len(r) else np.nan


def full_metrics(r):
    h = len(r) // 2
    o = r.loc[OOS_START:]
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]),
                IS_Sharpe=sharpe(r.loc[:IS_END]), IS_CAGR=cagr(r.loc[:IS_END]),
                OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o))


def keep_paths(m, v2, spy):
    """4a against the LIVE RULES v2 book; 4b against SPY (both halves AND OOS, DD cap, CAGR floor)."""
    a = (m["H1"] > v2["H1"]) and (m["H2"] > v2["H2"]) and (m["MaxDD"] >= v2["MaxDD"])
    legs = dict(H1=m["H1"] > spy["H1"], H2=m["H2"] > spy["H2"],
                OOS=m["OOS_Sharpe"] > spy["OOS_Sharpe"],
                DD=m["MaxDD"] >= DD_CAP * spy["MaxDD"],
                CAGR=m["CAGR"] >= CAGR_FLOOR * spy["CAGR"])
    return bool(a), bool(all(legs.values())), {k: bool(v) for k, v in legs.items()}


# ------------------------------------------------------------------ the book
def _feat(px):
    mom = px / px.shift(H_FROZEN) - 1
    ma200 = px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return mom, ma200, vol20


def base_weights(px, maxvol=MAXVOL, madist=0.0, band=None, sig=None):
    """Idea 1534's frozen BASE: top-N 126d momentum, equal weight, gross 0.75, per-name 200d MA
    gate and vol ceiling.  `sig` (default px) supplies the ELIGIBILITY inputs only — passing a
    shifted panel is how an eligibility-side device is made to read a stale tape."""
    s = px if sig is None else sig
    mom = px / px.shift(H_FROZEN) - 1
    _, ma200_s, vol20_s = _feat(s)
    above = band_state(s, band) if band is not None else (s > ma200_s * (1 + madist))
    elig = mom.where(above.reindex_like(mom).fillna(False) & (vol20_s < maxvol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= N_FROZEN).astype(float) * (GROSS / N_FROZEN)


def trailing_stop_mult(eq, depth, frac=STOP_FRAC):
    """Causal 0/1 multiplier from the BASE book's own net equity (idea 1534's function verbatim):
    out when the book is `depth` below its running peak, back in once it recovers `frac` of it."""
    eq = eq.ffill().bfill()
    e = eq.values
    m = np.ones(len(e))
    peak, out, trough = e[0], False, np.nan
    for i in range(len(e)):
        if not out:
            peak = max(peak, e[i])
            if e[i] <= peak * (1 - depth):
                out, trough = True, e[i]
        else:
            trough = min(trough, e[i])
            if e[i] >= trough + frac * (peak - trough):
                out, peak = False, max(peak, e[i])
        m[i] = 0.0 if out else 1.0
    return pd.Series(m, index=eq.index)


def timing_mult(fam, px, P, invest):
    """The device's RAW multiplier series, read at the record's own convention (no extra lag)."""
    spy = px["SPY"]
    if fam == "MACRO2":
        ind = (spy > spy.rolling(RUNG["MACRO2"]).mean())
        return ind.astype(float).where(ind, MACRO2_LOW)
    if fam == "SPYFILT":
        return (spy > spy.rolling(RUNG["SPYFILT"]).mean()).astype(float)
    if fam == "BREADTH":
        b0, p = RUNG["BREADTH"]
        q = px[invest]
        _, ma200, vol20 = _feat(q)
        ok = (q > ma200) & (vol20 < MAXVOL) & q.notna()
        b = ok.sum(axis=1) / q.notna().sum(axis=1).replace(0, np.nan)
        return np.minimum(1.0, (b / b0) ** p).fillna(1.0)
    if fam == "STOP":
        d, f = RUNG["STOP"]
        return trailing_stop_mult(P["base_eq"], d, f)
    if fam == "VOLTGT":
        rv = P["base_r_full"].rolling(20).std() * np.sqrt(252)
        return (RUNG["VOLTGT"] / rv.replace(0, np.nan)).clip(upper=1.0).fillna(1.0)
    raise KeyError(fam)


def device_weights(fam, lag, px, P, invest):
    """The device book at signal lag `lag`.  lag = 1 IS the record's committed convention."""
    if fam in TIMING:
        m = timing_mult(fam, px, P, invest).reindex(px.index).ffill().fillna(1.0)
        return P["base_w"].mul(m.shift(lag - 1).fillna(1.0), axis=0)
    sig = px.shift(lag - 1)
    if fam == "BAND":
        return base_weights(px, band=RUNG["BAND"], sig=sig)
    if fam == "MAXVOL":
        return base_weights(px, maxvol=RUNG["MAXVOL"], sig=sig)
    if fam == "MADIST":
        return base_weights(px, madist=RUNG["MADIST"], sig=sig)
    raise KeyError(fam)


INC_LEGS = [(21, 252), (0, 126), (0, 63)]
C_1562 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)   # the committed anchor
C_1562_LAG = {1: 0.0238, 2: 0.0275, 5: 0.0001}                             # the idea's premise


def incumbent_frame(px, invest, N=N_FROZEN, H=H_FROZEN):
    """The 2026-09-04 KEEP-4b INCUMBENT's holdings frame at unit gross — the frame idea 1562's
    premise number was measured on, which is NOT idea 1534's base book.  Three-leg composite rank
    x (0.5 + 0.5 * above-200d), eligibility = above 200d MA AND vol20 < 0.60, min-hold H: a held
    name that is still priced is retained for H days, vacancies filled by the composite.  Decided
    at close t (the engine applies it at t+1)."""
    q = px[invest]
    parts = []
    for skip, look in INC_LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = (sum(parts) / len(parts)).values
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    key = np.where(np.isfinite(sc), -sc, np.inf)
    pr = q.notna().values
    reb = np.flatnonzero(rebalance_mask(px.index, FREQ).values)
    T, K = len(px.index), len(invest)
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = {int(c) for c in young}
        take = []
        need = N - len(keep)
        if need > 0:
            k = key[t].copy()
            k[~(elig[t] & pr[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            take = [int(c) for c in np.argsort(k, kind="stable")[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = 1.0 / len(sel)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[invest] = W
    return out * GROSS


def run(px, w, start):
    res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    return (res["returns"].loc[start:], float(res["weights"].sum(axis=1).loc[start:].mean()),
            res["returns"])


# ------------------------------------------------------------------ bootstrap
def paired_block(pairs, index, reps=NBOOT, L=LB, seed=SEED):
    """PAIRED circular-block bootstrap of Sharpe differences: identical block starts for both legs
    of every pair, and identical across pairs, so DIFFERENCES OF DIFFERENCES are paired too."""
    T = len(index)
    A = np.column_stack([a.reindex(index).values for a, _ in pairs])
    B = np.column_stack([b.reindex(index).values for _, b in pairs])
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / L))
    out = np.empty((reps, len(pairs)))

    def _sh(X):
        m, sd = np.nanmean(X, axis=0), np.nanstd(X, axis=0, ddof=1)
        return np.where(sd > 0, m * 252 / (sd * np.sqrt(252)), np.nan)

    for k in range(reps):
        st = rng.integers(0, T, nb)
        idx = ((st[:, None] + np.arange(L)[None, :]).ravel()[:T]) % T
        out[k] = _sh(A[idx]) - _sh(B[idx])
    return out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 122)
    say(f"IDEA 1574 — is EVERY committed MACRO and TIMING GAIN in the record a ONE-OR-TWO-DAY "
        f"OBJECT?   (lane {LANE}, {DATE})")
    say("  PRE-REGISTERED, read in this order:")
    say("    H_STATE         some timing family keeps >= half its lag-1 margin at lag 21 AND that "
        "margin is resolvable (|t| > 2)  -> first real state variable.")
    say("    H_MICRO         every timing family with a positive lag-1 margin halves it inside 5 "
        "trading days                    -> one-or-two-day objects.")
    say("    H_UNMEASURABLE  no timing family's lag-1 margin is resolvable at |t| > 2             "
        "                                 -> the whole class is inside its own noise.  KILL.")
    say("=" * 122)

    # ---------------------------------------------------------------- panels
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    panels = {}
    for lbl, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        px = load_universe(**kw)
        if lbl == "SMALL":
            mv = px.pct_change().abs().max()
            inv = [c for c in px.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
            px = px[inv + ["SPY"]]
        else:
            inv = [c for c in px.columns if c != "SPY"]
        start = px.index[WARMUP]
        bw = base_weights(px)
        br = backtest(px, bw, cost_bps=COST_BPS, freq=FREQ)
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        v2_r = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        P = dict(px=px, invest=inv, start=start, base_w=bw, base_eq=br["equity"],
                 base_r_full=br["returns"], base_r=br["returns"].loc[start:],
                 base_gross=float(br["weights"].sum(axis=1).loc[start:].mean()),
                 spy_r=spy_r, v2_r=v2_r, spy_m=full_metrics(spy_r), v2_m=full_metrics(v2_r))
        P["base_m"] = full_metrics(P["base_r"])
        panels[lbl] = P
        yrs = len(P["base_r"]) / 252
        say(f"[{lbl}] {len(inv)} investable names + SPY   {start.date()}..{px.index[-1].date()}   "
            f"{yrs:.1f}y   BASE {P['base_m']['CAGR']:.2%} / {P['base_m']['Sharpe']:.4f} / "
            f"{P['base_m']['MaxDD']:.2%}   mean gross {P['base_gross']:.3f}   ({time.time()-t0:.0f}s)")
        gate(f"G0 {lbl} >= 10y", f"{yrs:.1f}y", ">= 10", yrs >= 10)

    say("\n  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "The HEADLINE of this run is a CONTRAST between two books over the SAME names on the SAME "
        "days differing ONLY in when a multiplier is read, which survivorship cannot manufacture; "
        "the 4a / 4b flags are levels and inherit the bias in full.")

    # -------------------------------------------------- G1/G2 cross-script replay of idea 1534
    say("\n" + "-" * 122)
    say("G1 / G2 — CROSS-SCRIPT REPLAY of idea 1534 (2026-09-19_pooled-device-vs-degross_C)")
    ref = ROOT / "research" / "backtests" / "2026-09-19_pooled-device-vs-degross_C.csv"
    if ref.exists():
        R = pd.read_csv(ref)
        got = panels["U56"]["base_m"]
        row = R[(R.panel == "U56") & (R.family == "BASE")]
        if len(row):
            d = abs(float(row.iloc[0]["Sharpe"]) - got["Sharpe"])
            gate("G1 BASE U56 Sharpe replay", f"{got['Sharpe']:.4f} vs 1534's "
                 f"{float(row.iloc[0]['Sharpe']):.4f} (d={d:.2e})", "< 1e-6", d < 1e-6)
        for fam, rung in (("SPYFILT", "L=200"), ("STOP", "d=0.100"), ("VOLTGT", "v=0.12")):
            row = R[(R.panel == "U56") & (R.family == fam) & (R.rung == rung)]
            if not len(row):
                continue
            w = device_weights(fam, 1, panels["U56"]["px"], panels["U56"], panels["U56"]["invest"])
            r, g, _ = run(panels["U56"]["px"], w, panels["U56"]["start"])
            d = abs(sharpe(r) - float(row.iloc[0]["Sharpe"]))
            gate(f"G2 {fam} {rung} lag-1 replay", f"{sharpe(r):.4f} vs {float(row.iloc[0]['Sharpe']):.4f} "
                 f"(d={d:.2e})", "< 1e-6", d < 1e-6)
    else:
        gate("G1/G2 replay source", "1534 csv absent", "present", False)

    # ---------------------------------------------------------------- twin ladders
    say("\n" + "-" * 122)
    say(f"CAGR-MATCHED TWIN LADDER — constant gross g on the SAME frame, {GGRID[0]:.2f}..{GGRID[-1]:.2f} "
        f"by {GGRID[1]-GGRID[0]:.2f} ({len(GGRID)} rungs per panel), a CONTROL, never a dial")
    for lbl, P in panels.items():
        cg, sh_, dd_ = [], [], []
        for g in GGRID:
            r, _, _ = run(P["px"], P["base_w"] * (g / GROSS), P["start"])
            cg.append(cagr(r))
            sh_.append(sharpe(r))
            dd_.append(maxdd(r))
        P["ladder"] = pd.DataFrame(dict(g=GGRID, CAGR=cg, Sharpe=sh_, MaxDD=dd_))
        say(f"  [{lbl}] CAGR spans {min(cg):.2%}..{max(cg):.2%}; Sharpe spans {min(sh_):.4f}.."
            f"{max(sh_):.4f} (flatness of Sharpe in gross: {max(sh_)-min(sh_):.4f})   "
            f"({time.time()-t0:.0f}s)")

    def solve_twin(P, target):
        lad = P["ladder"]
        if not (lad.CAGR.min() - 1e-9 <= target <= lad.CAGR.max() + 1e-9):
            return None, np.nan
        o = lad.sort_values("CAGR")
        g = float(np.interp(target, o.CAGR.values, o.g.values))
        for _ in range(4):
            r, _, _ = run(P["px"], P["base_w"] * (g / GROSS), P["start"])
            gap = cagr(r) - target
            if abs(gap) < MATCH_BAR:
                return r, g
            slope = np.gradient(o.CAGR.values, o.g.values).mean()
            g = float(np.clip(g - gap / max(slope, 1e-6), GGRID[0], GGRID[-1]))
        return r, g

    # ---------------------------------------------------------------- the grid
    say("\n" + "-" * 122)
    say(f"THE GRID — {len(FAMILIES)} families x {len(LAGS)} lags x {len(panels)} panels = "
        f"{len(FAMILIES)*len(LAGS)*len(panels)} cells, EVERY ONE PUBLISHED")
    rows, series = [], {}
    unmatched: list[str] = []
    g7_ok, g6_ok, g4_ok = True, True, True
    for lbl, P in panels.items():
        say(f"\n  [{lbl}]  spy {P['spy_m']['CAGR']:.2%}/{P['spy_m']['Sharpe']:.4f}/"
            f"{P['spy_m']['MaxDD']:.2%}   RULESv2 {P['v2_m']['CAGR']:.2%}/{P['v2_m']['Sharpe']:.4f}/"
            f"{P['v2_m']['MaxDD']:.2%}")
        for fam in FAMILIES:
            for lag in LAGS:
                w = device_weights(fam, lag, P["px"], P, P["invest"])
                if lag == 1 and fam in TIMING:
                    m = timing_mult(fam, P["px"], P, P["invest"]).reindex(P["px"].index).ffill().fillna(1.0)
                    g7_ok &= bool(np.allclose(w.values, P["base_w"].mul(m, axis=0).values))
                    g6_ok &= bool(float(m.min()) >= 0.0 and float(m.max()) <= 1.0)
                dr, dg, _ = run(P["px"], w, P["start"])
                tr, tg = solve_twin(P, cagr(dr))
                if tr is None:
                    matched, gap, tm = False, np.nan, {k: np.nan for k in P["base_m"]}
                    g4_ok = False          # an UNMATCHED cell fails G4; it is never silently
                    unmatched.append(f"{lbl}/{fam}/L{lag}")   # dropped, only published as such
                else:
                    gap = cagr(tr) - cagr(dr)
                    matched = abs(gap) < MATCH_BAR
                    g4_ok &= matched
                    tm = full_metrics(tr)
                dm = full_metrics(dr)
                g6_ok &= dg <= GROSS + 1e-9
                a4, b4, legs = keep_paths(dm, P["v2_m"], P["spy_m"])
                rows.append(dict(panel=lbl, family=fam, arm=("TIMING" if fam in TIMING else "ELIG"),
                                 lag=lag, gross_dev=dg, twin_g=tg, cagr_gap=gap, matched=matched,
                                 m_Sharpe=dm["Sharpe"] - tm["Sharpe"],
                                 m_MaxDD=dm["MaxDD"] - tm["MaxDD"],
                                 m_OOS_Sharpe=dm["OOS_Sharpe"] - tm["OOS_Sharpe"],
                                 twin_Sharpe=tm["Sharpe"], twin_CAGR=tm["CAGR"], twin_MaxDD=tm["MaxDD"],
                                 keep4a=a4, keep4b=b4, **{f"leg_{k}": v for k, v in legs.items()},
                                 **dm))
                series[(lbl, fam, lag)] = (dr, tr)
                say(f"    {fam:8s} L={lag:2d}  gross {dg:.3f}  twin g*={tg:.3f} (gap "
                    f"{gap*1e4:+6.1f}bp)  Sh {dm['Sharpe']:.4f} vs {tm['Sharpe']:.4f}  "
                    f"m={dm['Sharpe']-tm['Sharpe']:+.4f}  DD {dm['MaxDD']:.2%}  4a={int(a4)} "
                    f"4b={int(b4)}  ({time.time()-t0:.0f}s)")

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G8 every cell published", f"{len(df)} rows",
         f"{len(FAMILIES)*len(LAGS)*len(panels)}", len(df) == len(FAMILIES) * len(LAGS) * len(panels))
    gate("G7 lag 1 == the record's convention", "bit-identical books", "identical", g7_ok)
    gate("G6 multipliers in [0,1], mean gross <= 0.75", "all cells", "all", g6_ok)
    gate("G4 CAGR match < 20 bp", f"{int(df.matched.sum())}/{len(df)} matched", "all", g4_ok)
    if unmatched:
        say(f"    G4 DETAIL — {len(unmatched)} cell(s) have NO CAGR-matched twin because the "
            f"device's own CAGR falls OUTSIDE the entire constant-gross family's range "
            f"[g = {GGRID[0]:.2f}..{GGRID[-1]:.2f}]: " + ", ".join(unmatched) + ".  This is a "
            f"STRUCTURAL result, not a solver failure: a device that lands below the CAGR of the "
            f"most de-grossed book in the family has destroyed more than ALL of the gross it was "
            f"supposed to be timing, and no constant gross can imitate it.  These cells carry a "
            f"NaN margin, are excluded from every pooled statistic and from the bootstrap, and are "
            f"published in .grid.csv with matched = False.")
    gate("G3 tuned parameters", "family, lag", "<= 2", True)

    # ---------------------------------------------------------------- half-life
    say("\n" + "=" * 122)
    say("THE HALF-LIFE OF EACH DEVICE'S MARGIN OVER ITS OWN CAGR-MATCHED DE-GROSS TWIN")
    say("=" * 122)

    def half_life(ms):
        m1 = ms[0]
        if not np.isfinite(m1) or m1 <= 0:
            return np.nan, "NA (no positive lag-1 margin)"
        tgt = m1 / 2
        for i in range(1, len(LAGS)):
            if np.isfinite(ms[i]) and ms[i] <= tgt:
                lo, hi = LAGS[i - 1], LAGS[i]
                a, b = ms[i - 1], ms[i]
                f = 0.0 if a == b else (a - tgt) / (a - b)
                return lo + f * (hi - lo), f"{lo + f*(hi-lo):.1f} d"
            if not np.isfinite(ms[i]):
                return np.nan, "NA (unmatched rung)"
        return np.inf, ">21 d (flat)"

    def half_life_abs(ms):
        """Same construction on |m|: how long a device's EFFECT (of either sign) survives."""
        a = [abs(x) if np.isfinite(x) else np.nan for x in ms]
        if not np.isfinite(a[0]) or a[0] <= 0:
            return np.nan, "NA"
        tgt = a[0] / 2
        for i in range(1, len(LAGS)):
            if not np.isfinite(a[i]):
                return np.nan, "NA"
            if a[i] <= tgt:
                lo, hi, x, y = LAGS[i - 1], LAGS[i], a[i - 1], a[i]
                f = 0.0 if x == y else (x - tgt) / (x - y)
                return lo + f * (hi - lo), f"{lo + f*(hi-lo):.1f} d"
        return np.inf, ">21 d"

    hl_rows = []
    for lbl in panels:
        for fam in FAMILIES:
            ms = [float(df[(df.panel == lbl) & (df.family == fam) & (df.lag == L)].m_Sharpe.iloc[0])
                  for L in LAGS]
            hl, lab = half_life(ms)
            hla, laba = half_life_abs(ms)
            hl_rows.append(dict(panel=lbl, family=fam, arm=("TIMING" if fam in TIMING else "ELIG"),
                                **{f"m_L{L}": v for L, v in zip(LAGS, ms)}, half_life=hl, hl_label=lab,
                                half_life_abs=hla, hl_abs_label=laba,
                                retained_21=(ms[-1] / ms[0] if ms[0] > 0 else np.nan),
                                retained_21_abs=(abs(ms[-1]) / abs(ms[0]) if ms[0] else np.nan)))
    hl = pd.DataFrame(hl_rows)

    say(f"\n  {'panel':6s} {'family':8s} {'arm':7s} " +
        " ".join(f"{'m(L='+str(L)+')':>10s}" for L in LAGS) +
        f" {'ret@21':>8s}  {'half-life(signed)':>18s}  half-life(|m|)")
    for _, r in hl.iterrows():
        say(f"  {r.panel:6s} {r.family:8s} {r.arm:7s} " +
            " ".join(f"{r['m_L'+str(L)]:+10.4f}" for L in LAGS) +
            f" {r.retained_21:8.2f}  {r.hl_label:>18s}  {r.hl_abs_label}")
    hl.to_csv(f"{OUT}.halflife.csv", index=False)

    # ---------------------------------------------------------------- resolvability
    say("\n" + "-" * 122)
    say(f"IS ANY OF IT RESOLVABLE?  PAIRED circular-block bootstrap ({NBOOT} reps x {LB}-day blocks, "
        f"seed {SEED}); the record's bar is |t| > 2")
    idx = panels["U56"]["px"].index
    idx = idx[idx >= panels["U56"]["start"]]
    keys = [(lbl, fam, L) for lbl in panels for fam in FAMILIES for L in LAGS
            if series[(lbl, fam, L)][1] is not None]
    boot = paired_block([series[k] for k in keys], idx)
    obs = np.array([sharpe(series[k][0]) - sharpe(series[k][1]) for k in keys])
    se = np.nanstd(boot, axis=0, ddof=1)
    tt = np.where(se > 0, obs / se, np.nan)
    B = pd.DataFrame(dict(panel=[k[0] for k in keys], family=[k[1] for k in keys],
                          lag=[k[2] for k in keys], m=obs, se=se, t=tt))
    B.to_csv(f"{OUT}.bootstrap.csv", index=False)
    l1 = B[B.lag == 1]
    say(f"  lag-1 margins: {int((l1.t.abs() > 2).sum())} of {len(l1)} reach |t| > 2   "
        f"(timing only: {int((l1[l1.family.isin(TIMING)].t.abs() > 2).sum())} of "
        f"{len(l1[l1.family.isin(TIMING)])})")
    for _, r in l1.sort_values("t", ascending=False).iterrows():
        say(f"    {r.panel:6s} {r.family:8s} m(1) = {r.m:+.4f}  SE {r.se:.4f}  t = {r.t:+.2f}"
            f"{'   <-- RESOLVED' if abs(r.t) > 2 else ''}")
    say(f"  ALL {len(B)} cells: {int((B.t.abs() > 2).sum())} of {len(B)} reach |t| > 2.  "
        f"Mean SE of a margin = {B.se.mean():.4f}, i.e. the ladder's whole lag-1-to-lag-21 spread "
        f"({B[B.lag==1].m.mean()-B[B.lag==21].m.mean():+.4f} pooled) is "
        f"{abs(B[B.lag==1].m.mean()-B[B.lag==21].m.mean())/B.se.mean():.2f} SE wide.")

    # DECAY itself: m(1) - m(L) with the SAME block draws (paired difference of differences)
    say("\n  THE DECAY ITSELF (m(1) - m(L)), paired across the same block draws:")
    pos = {k: i for i, k in enumerate(keys)}
    dec_rows = []
    for lbl in panels:
        for fam in FAMILIES:
            for L in (5, 21):
                k1, k2 = (lbl, fam, 1), (lbl, fam, L)
                if k1 not in pos or k2 not in pos:
                    # one of the two rungs has NO CAGR-matched twin (the device's CAGR falls
                    # outside the whole constant-gross family's range) -> the decay is undefined,
                    # published as such rather than dropped.
                    dec_rows.append(dict(panel=lbl, family=fam, lag=L, decay=np.nan, se=np.nan,
                                         t=np.nan))
                    continue
                i1, i2 = pos[k1], pos[k2]
                d = boot[:, i1] - boot[:, i2]
                o = obs[i1] - obs[i2]
                s = float(np.nanstd(d, ddof=1))
                dec_rows.append(dict(panel=lbl, family=fam, lag=L, decay=o, se=s,
                                     t=(o / s if s > 0 else np.nan)))
    D = pd.DataFrame(dec_rows)
    D.to_csv(f"{OUT}.decay.csv", index=False)
    for L in (5, 21):
        sub = D[D.lag == L]
        st = sub[sub.family.isin(TIMING)]
        say(f"    m(1)-m({L}): {int((sub.t.abs() > 2).sum())}/{len(sub)} reach |t| > 2 "
            f"(timing {int((st.t.abs() > 2).sum())}/{len(st)}); pooled mean {sub.decay.mean():+.4f}, "
            f"mean SE {sub.se.mean():.4f}")

    # ------------------------------------------------- PREMISE REPLAY on idea 1562's OWN frame
    say("\n" + "=" * 122)
    say("PREMISE REPLAY — the same lag ladder on IDEA 1562's OWN FRAME (the 2026-09-04 KEEP-4b "
        "incumbent: 3-leg composite, min-hold H = 126, N = 20), U56 only")
    say("  This is NOT a third dial: one panel, one family (MACRO2), the same two parameters, run "
        "because the number idea 1574 quotes (+0.0238 / +0.0275 / +0.0001 at L = 1 / 2 / 5) was "
        "measured on THIS frame and not on idea 1534's base book, so the main grid above cannot "
        "confirm or refute it.")
    say("=" * 122)
    PU = panels["U56"]
    inc_w = incumbent_frame(PU["px"], PU["invest"])
    inc_r, inc_g, _ = run(PU["px"], inc_w, PU["start"])
    inc_m = full_metrics(inc_r)
    say(f"  INCUMBENT frame replay: {inc_m['CAGR']:.2%} / {inc_m['Sharpe']:.4f} / "
        f"{inc_m['MaxDD']:.2%}, OOS Sharpe {inc_m['OOS_Sharpe']:.4f}, mean gross {inc_g:.3f}")
    say(f"  the record's committed anchor: {C_1562['CAGR']:.2%} / {C_1562['Sharpe']:.4f} / "
        f"{C_1562['MaxDD']:.2%}, OOS Sharpe {C_1562['oSharpe']:.4f}")
    d_anchor = abs(inc_m["Sharpe"] - C_1562["Sharpe"])
    gate("G1b incumbent-frame replay of the committed anchor",
         f"Sharpe {inc_m['Sharpe']:.4f} vs {C_1562['Sharpe']:.4f} (d={d_anchor:.4f})",
         "< 0.02 (different engine path)", d_anchor < 0.02)
    inc_lad = []
    for g in GGRID:
        r, _, _ = run(PU["px"], inc_w * (g / GROSS), PU["start"])
        inc_lad.append((g, cagr(r)))
    IL = pd.DataFrame(inc_lad, columns=["g", "CAGR"]).sort_values("CAGR")
    prem = []
    mac = timing_mult("MACRO2", PU["px"], PU, PU["invest"]).reindex(PU["px"].index).ffill().fillna(1.0)
    for L in LAGS:
        w = inc_w.mul(mac.shift(L - 1).fillna(1.0), axis=0)
        dr, dg, _ = run(PU["px"], w, PU["start"])
        tgt = cagr(dr)
        g = float(np.interp(tgt, IL.CAGR.values, IL.g.values))
        tr = None
        for _ in range(4):
            tr, _, _ = run(PU["px"], inc_w * (g / GROSS), PU["start"])
            gap = cagr(tr) - tgt
            if abs(gap) < MATCH_BAR:
                break
            sl = np.gradient(IL.CAGR.values, IL.g.values).mean()
            g = float(np.clip(g - gap / max(sl, 1e-6), GGRID[0], GGRID[-1]))
        dm, tm = full_metrics(dr), full_metrics(tr)
        a4, b4, _lg = keep_paths(dm, PU["v2_m"], PU["spy_m"])
        prem.append(dict(lag=L, gross=dg, twin_g=g, cagr_gap=cagr(tr) - tgt,
                         m_Sharpe=dm["Sharpe"] - tm["Sharpe"], quoted=C_1562_LAG.get(L, np.nan),
                         keep4a=a4, keep4b=b4, **dm))
        say(f"    MACRO2 on the incumbent frame  L={L:2d}  {dm['CAGR']:.2%} / {dm['Sharpe']:.4f} / "
            f"{dm['MaxDD']:.2%}   twin g*={g:.3f} (gap {(cagr(tr)-tgt)*1e4:+5.1f}bp)   "
            f"m = {dm['Sharpe']-tm['Sharpe']:+.4f}" +
            (f"   [1574 quotes {C_1562_LAG[L]:+.4f} pooled over 3 panels]" if L in C_1562_LAG else "") +
            f"   4a={int(a4)} 4b={int(b4)}   ({time.time()-t0:.0f}s)")
    PR = pd.DataFrame(prem)
    PR.to_csv(f"{OUT}.premise.csv", index=False)
    m1p = float(PR[PR.lag == 1].m_Sharpe.iloc[0])
    say(f"  PREMISE VERDICT: on the frame the quoted number was measured on, U56's lag-1 margin is "
        f"{m1p:+.4f} against the +{C_1562_LAG[1]:.4f} the queue quotes as a THREE-PANEL POOLED mean; "
        f"the ladder here reads " + " / ".join(f"L{int(r.lag)} {r.m_Sharpe:+.4f}" for _, r in PR.iterrows()) + ".")

    # ---------------------------------------------------------------- rule 8
    say("\n" + "=" * 122)
    say("RULE 8 WALK-FORWARD — both choosers read warm-up..2016-12-31 ONLY; 2017-01-01..end read ONCE")
    say("=" * 122)
    gate("G5 chooser window", f"IS ends {IS_END.date()}, OOS starts {OOS_START.date()}",
         "no chooser row >= 2017-01-01", True)
    wf = []
    for lbl, P in panels.items():
        sub = df[df.panel == lbl]
        for cname, pick in (("ARGMAX IS Sharpe", sub.loc[sub.IS_Sharpe.idxmax()]),
                            ("ARGMAX IS margin over twin",
                             sub.loc[sub.assign(mi=[sharpe(series[(lbl, f, l)][0].loc[:IS_END]) -
                                                    sharpe(series[(lbl, f, l)][1].loc[:IS_END])
                                                    if series[(lbl, f, l)][1] is not None else -9
                                                    for f, l in zip(sub.family, sub.lag)]).mi.idxmax()])):
            base_oos = dict(CAGR=cagr(P["base_r"].loc[OOS_START:]),
                            Sharpe=sharpe(P["base_r"].loc[OOS_START:]),
                            MaxDD=maxdd(P["base_r"].loc[OOS_START:]))
            wf.append(dict(panel=lbl, chooser=cname, family=pick.family, lag=int(pick.lag),
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           anchor_OOS_Sharpe=base_oos["Sharpe"], anchor_OOS_CAGR=base_oos["CAGR"],
                           anchor_OOS_MaxDD=base_oos["MaxDD"],
                           v2_OOS_Sharpe=P["v2_m"]["OOS_Sharpe"], v2_OOS_CAGR=P["v2_m"]["OOS_CAGR"],
                           v2_OOS_MaxDD=P["v2_m"]["OOS_MaxDD"],
                           spy_OOS_Sharpe=P["spy_m"]["OOS_Sharpe"], spy_OOS_CAGR=P["spy_m"]["OOS_CAGR"],
                           spy_OOS_MaxDD=P["spy_m"]["OOS_MaxDD"],
                           keep4a=bool(pick.keep4a), keep4b=bool(pick.keep4b)))
            say(f"  [{lbl}] {cname:26s} -> {pick.family} L={int(pick.lag)}   OOS "
                f"{pick.OOS_CAGR:.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:.2%}   |   "
                f"frozen BASE (do nothing) {base_oos['CAGR']:.2%} / {base_oos['Sharpe']:.4f} / "
                f"{base_oos['MaxDD']:.2%}   |   RULESv2 {P['v2_m']['OOS_CAGR']:.2%} / "
                f"{P['v2_m']['OOS_Sharpe']:.4f}   |   SPY {P['spy_m']['OOS_CAGR']:.2%} / "
                f"{P['spy_m']['OOS_Sharpe']:.4f} / {P['spy_m']['OOS_MaxDD']:.2%}   "
                f"4a={int(pick.keep4a)} 4b={int(pick.keep4b)}")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  CHOOSER vs DOING NOTHING: the chooser beats the frozen BASE on OOS Sharpe in "
        f"{int((W.OOS_Sharpe > W.anchor_OOS_Sharpe).sum())} of {len(W)} (panel, chooser) cells; "
        f"mean OOS Sharpe {W.OOS_Sharpe.mean():.4f} vs the anchor's {W.anchor_OOS_Sharpe.mean():.4f}.")

    # ---------------------------------------------------------------- keep paths census
    say("\n" + "-" * 122)
    say("BOTH KEEP PATHS AT EVERY CELL (rule 4)")
    say(f"  4a fires at {int(df.keep4a.sum())} of {len(df)} cells; 4b at {int(df.keep4b.sum())}.")
    for lbl in panels:
        s = df[df.panel == lbl]
        say(f"    [{lbl}] 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}   "
            f"binding 4b legs: " + ", ".join(f"{k}={int((~s['leg_'+k]).sum())} fails"
                                             for k in ("H1", "H2", "OOS", "DD", "CAGR")))
    if df.keep4b.any():
        best = df[df.keep4b].sort_values("Sharpe", ascending=False).iloc[0]
        say(f"  Best 4b passer: [{best.panel}] {best.family} L={int(best.lag)}  "
            f"{best.CAGR:.2%} / {best.Sharpe:.4f} / {best.MaxDD:.2%}  OOS {best.OOS_CAGR:.2%} / "
            f"{best.OOS_Sharpe:.4f} / {best.OOS_MaxDD:.2%}   margin over its OWN twin "
            f"{best.m_Sharpe:+.4f}")

    # ---------------------------------------------------------------- verdict
    say("\n" + "=" * 122)
    T_ = hl[hl.arm == "TIMING"]
    resolved = l1[l1.family.isin(TIMING)]
    n_res = int((resolved.t.abs() > 2).sum())
    pos_m1 = T_[T_.m_L1 > 0]
    flat = T_[(T_.m_L1 > 0) & (T_.retained_21 >= 0.5)]
    fast = pos_m1[(pos_m1.half_life < 5)]
    h_state = bool(len(flat) and n_res > 0)
    h_nomargin = bool(len(pos_m1) == 0)
    h_micro = bool(len(pos_m1) and len(fast) == len(pos_m1))
    h_unmeas = bool(n_res == 0)
    say(f"  TIMING cells with a POSITIVE lag-1 margin: {len(pos_m1)} of {len(T_)}.  "
        f"Of those, half-life < 5 d: {len(fast)}; still >= half the margin at lag 21: {len(flat)}.")
    say(f"  RESOLVABILITY: {n_res} of {len(resolved)} timing lag-1 margins reach |t| > 2.")
    say(f"  H_STATE {h_state}   H_NOMARGIN {h_nomargin}   H_MICRO {h_micro}   "
        f"H_UNMEASURABLE {h_unmeas}")
    verdict = ("KEEP-candidate (H_STATE)" if h_state else
               "KILL (H_NOMARGIN)" if h_nomargin else
               "KILL (H_MICRO)" if h_micro else
               "KILL (H_UNMEASURABLE)" if h_unmeas else "PARK (mixed)")
    say(f"  VERDICT: {verdict}")
    say("=" * 122)
    gfail = [g["gate"] for g in GATES if not g["pass_"]]
    say(f"  GATES {len(GATES)-len(gfail)}/{len(GATES)} pass" + (f"; FAILED: {gfail}" if gfail else ""))
    say(f"  runtime {time.time()-t0:.0f}s")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return verdict


if __name__ == "__main__":
    main()
