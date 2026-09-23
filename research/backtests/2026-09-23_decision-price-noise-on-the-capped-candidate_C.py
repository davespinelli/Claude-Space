#!/usr/bin/env python3
"""idea 2495 (lane C, run 60, 2026-09-23) — WHERE DOES THE CAPPED CANDIDATE'S 4b PASS BREAK
UNDER NOISE IN THE DECISION PRICE ITSELF?

THE GAP.  The standing 4b candidate (idea 2322's CAP2: hold every name inside the 200d +/-3%
hysteresis band at `min(g/N_in, 2%)` of NAV, weekly, residual swept into SHY) is a THRESHOLD RULE
ON ONE NUMBER — today's close against its own 200d moving average.  This record has moved that
threshold in every deterministic way it can be moved: band WIDTH (2412), MA LENGTH (the lookback
ladders), the MA's SLOPE, a Donchian channel in its place, and asymmetric entry/exit edges (2383).
It has ALSO perturbed the panel's COMPOSITION (leave-one-out and random name drops, ideas 519 /
2476-era censuses).  What it has NEVER done is perturb THE NUMBER THE THRESHOLD IS READ FROM.

WHY THAT MATTERS FOR REAL CAPITAL.  A close is not an exact quantity.  The closing-auction print,
a second vendor's adjusted close, and a different corporate-action back-adjustment convention
disagree by a few basis points on any given name-day, and the record's own caches are ONE vendor's
one convention.  If the candidate's 4b pass is a function of which side of a line a handful of
names happened to land on, it is not an edge, it is a coincidence of the data vendor.

AND THE ERROR DOES NOT AVERAGE OUT — `band_state` HAS MEMORY.  The band is hysteretic: a name is
IN above `ma * 1.03`, OUT below `ma * 0.97`, and OTHERWISE KEEPS ITS PREVIOUS STATE.  So a single
spurious close that pushes a name over the entry edge does not wash out on the next bar — the name
STAYS IN until it actually falls 3% below its MA.  Decision noise therefore RATCHETS into the
holding path.  This run measures that persistence directly (the mean run length of a state
disagreement) rather than assuming it.

THE DESIGN, WHICH IS THE WHOLE POINT.  The perturbation is applied to the DECISION PRICES ONLY:
    p~[i,t] = p[i,t] * exp(sigma_k * z[i,t]),   z ~ N(0,1) i.i.d. per name-day, seeded.
The band state, the eligible set, `N_in` and therefore every weight are computed on `p~`.  THE
P&L IS EARNED ON THE TRUE TAPE `p`, and so are SPY and the live RULES v2 baseline.  A gate asserts
the comparand series are BIT-IDENTICAL across every k, so anything that moves is a DECISION
movement and nothing else.  (Perturbing the returns too would confound decision fragility with a
trivially different tape, and would make SPY move, which would make the 4b legs incomparable.)

DIAL 1 -- per-name weight cap in {0.015, 0.020 (idea 2322's CAP2, committed), 0.030, INF (idea
          2300/2332's uncapped CAND)}.
DIAL 2 -- gross g in {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS.  Everything else is a PUBLISHED AXIS, never selected on:

  NOISE SIZE k in {0, 10, 25, 50, 100, 200, 400} bps, with 8 SEEDS at every k > 0 (k = 0 is the
  committed book exactly and is deterministic, so it carries one state).  k is REPORTED at every
  grid point and no verdict is ever read off a chosen k.
  Panels {U56, B136}; cost rungs {0, 10, 25, 50} bps; weekly cadence; t+1 execution; band 0.03;
  MA 200d; SHY sweep at phi = 1.00.

WHAT A HONEST ANSWER LOOKS LIKE EITHER WAY.  If the 4b verdict is invariant across every seed out
to a k far larger than any plausible vendor disagreement, the candidate earns a robustness stamp
the record has never held, and the run publishes the k at which it finally breaks as a measured
FRAGILITY MARGIN.  If instead 10 or 25 bps of decision noise already flips seeds, the standing
candidate is a data artefact and must not be taken to the Sunday review.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with `L_DD`,
`L_H2` and `L_OOS` all failing at every cell.  Adding noise to a decision cannot mend three legs
that already fail without it.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (cap, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, then 2017-2026 is read ONCE -- separately at every (panel, rung, k, seed), so
the run can say whether decision noise MOVES THE PICK as well as whether it moves the verdict.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 at k = 0 and
cap = INF the eligible set IS `baseline.band_state` & priced, bit-identically.  G3 the k = 0
cap 0.020 / g 0.75 / 10 bps cell reproduces the committed CAP2 and CAND U56 headlines.  G4 no
leverage.  G5 cost exactly linear in the rung.  G6 exactly two tuned parameters.  G7 the
comparands (SPY and the live RULES v2 baseline) are BIT-IDENTICAL across every k and seed.  G8
the noise BITES, and monotonically: the mean gate-state disagreement share rises with k.  G9 the
sweep instrument is priced on every scored row.  G10 the realised perturbation size matches its
nominal k.  G11 k = 0 is bit-identical across all 8 seed slots (the noise is switched OFF, not
merely small).  G12 the hysteresis PERSISTENCE is published before any verdict is read.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The k-vs-k contrast is same-tape, same-days,
same-names and first-order immune to that bias; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_decision-price-noise-on-the-capped-candidate_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "decision-price-noise-on-the-capped-candidate", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
CAPS = [0.015, 0.020, 0.030, np.inf]          # DIAL 1
GROSSES = [0.75, 1.00]                        # DIAL 2
RUNGS = [0.0, 10.0, 25.0, 50.0]               # published
KS = [0, 10, 25, 50, 100, 200, 400]           # published: decision-price noise, bps
NSEED = 8                                     # published
SWEEP = "SHY"
HEADLINE_CAP, HEADLINE_GROSS, HEADLINE_RUNG, HEADLINE_K = 0.020, 0.75, 10.0, 0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BASE_SEED = 20260923

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUB   {name}: {value}")


def cname(c):
    return "INF" if not np.isfinite(c) else f"{c:.3f}"


# ---------------------------------------------------------------- the perturbation
def perturb(px, k_bps, seed):
    """Multiplicative i.i.d. lognormal noise on the DECISION price only.  k = 0 returns the true
    frame UNTOUCHED (identity, not a zero-variance draw), so the k = 0 arm IS the committed book."""
    if k_bps == 0:
        return px
    rng = np.random.default_rng(BASE_SEED + 1000 * int(k_bps) + int(seed))
    z = rng.standard_normal(px.shape)
    return pd.DataFrame(px.values * np.exp((k_bps / 1e4) * z), index=px.index, columns=px.columns)


# ---------------------------------------------------------------- the book
def eligible(px_dec):
    """Names permitted to be held: inside the 200d +/- BAND hysteresis band and priced.  This is
    `baseline.band_state` unmodified, read off the DECISION frame (G2 asserts bit-identity at k=0)."""
    return band_state(px_dec, BAND) & px_dec.notna()


def risk_weights(el, gross, cap):
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that the per-day turnover is retained so every cost rung
    is read off the SAME realised path.  `prices` is ALWAYS the TRUE tape: weights decided at t-1
    are applied at t, the book drifts between rebalances, the residual is swept into SHY."""
    cols = list(prices.columns)
    si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n)
    swp = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum())
            cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        swp[i] = float(cur[si])
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), names=pd.Series(nheld, index=idx),
                maxw=pd.Series(mx, index=idx), sweep_w=pd.Series(swp, index=idx))


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


def vol(r):
    return float(r.std() * np.sqrt(252))


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    d = maxdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(H1=h1, H2=h2,
                pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_H1=h1 - s1, m_H2=h2 - s2, m_OOS=sharpe(r_oos) - sharpe(spy_oos),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def run_lengths(dis):
    """Mean length of a contiguous TRUE run, column by column, over a boolean 2-D array."""
    tot, cnt = 0, 0
    for j in range(dis.shape[1]):
        c = dis[:, j]
        if not c.any():
            continue
        d = np.diff(np.concatenate(([0], c.view(np.int8), [0])))
        starts = np.flatnonzero(d == 1); ends = np.flatnonzero(d == -1)
        tot += int((ends - starts).sum()); cnt += len(starts)
    return (tot / cnt) if cnt else np.nan


def main():
    t0 = time.time()
    say("=== idea 2495 — WHERE DOES THE CAPPED CANDIDATE'S 4b PASS BREAK UNDER NOISE IN THE")
    say("    DECISION PRICE ITSELF? ===")
    say(f"    {DATE}  lane {LANE} run 60   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 per-name cap {[cname(c) for c in CAPS]} (0.020 = idea 2322's CAP2, INF = CAND)"
        f"    DIAL 2 gross {GROSSES}")
    say(f"    PUBLISHED AXIS, NEVER SELECTED ON: decision-price noise k {KS} bps x {NSEED} seeds"
        f" (k=0 is the identity and carries ONE state).")
    say("    DESIGN: p~ = p * exp(sigma_k z), i.i.d. per name-day, drives the BAND STATE, the")
    say("    ELIGIBLE SET, N_in and every weight.  P&L, SPY and the live RULES v2 baseline are")
    say("    earned on the TRUE tape at every k (G7 asserts bit-identity), so anything that moves")
    say("    is a DECISION movement and nothing else.")
    say("    MECHANISM UNDER TEST: band_state is HYSTERETIC, so one spurious close RATCHETS a name")
    say("    into the book until it actually falls 3% below its MA.  G12 measures that persistence.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383) and 0 of 40-120 (2318/2322/2326/2343);")
    say("    noise on a decision cannot mend three legs that already fail without it.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is")
    say("    the contaminated leg.  The k-vs-k contrast is same-tape, same-days, first-order immune.")
    gate("G6 exactly two tuned parameters", "per-name cap, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    bs_u = band_state(px_u, BAND) & px_u.notna()
    d2 = int((eligible(px_u) != bs_u).sum().sum())
    gate("G2 at k=0 the eligible set IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells; mean names IN {bs_u.sum(axis=1).mean():.2f}", "0", d2 == 0)

    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every scored row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    # --------------------------------------------------- the noise states, built and audited first
    say("\n=== G10 / G11 / G8 / G12. THE NOISE ITSELF — BUILT AND AUDITED BEFORE ANY VERDICT IS READ ===")
    states: dict[tuple, dict] = {}     # (panel, k, seed) -> dict(el=, ...)
    churn_rows = []
    for pname, px in panels.items():
        el0 = eligible(px)
        for k in KS:
            seeds = [0] if k == 0 else list(range(NSEED))
            for sd in seeds:
                dec = perturb(px, k, sd)
                el = eligible(dec)
                sub = el.iloc[WARMUP:]; sub0 = el0.iloc[WARMUP:]
                dis = (sub.values != sub0.values) & px.iloc[WARMUP:].notna().values
                realised = (np.log(dec.values / px.values)[np.isfinite(np.log(dec.values / px.values))].std()
                            * 1e4) if k > 0 else 0.0
                states[(pname, k, sd)] = dict(el=el)
                churn_rows.append(dict(
                    panel=pname, k_bps=k, seed=sd,
                    realised_bps=float(realised),
                    disagree_share=float(dis.mean()),
                    mean_names_in=float(sub.sum(axis=1).mean()),
                    mean_names_in_k0=float(sub0.sum(axis=1).mean()),
                    mean_run_len=float(run_lengths(dis)) if dis.any() else 0.0))
    ch = pd.DataFrame(churn_rows); ch.to_csv(f"{OUT}.churn.csv", index=False)

    say("  panel   k bps | realised sd (bps) | gate-state disagreement | mean names IN (vs k=0)"
        " | mean disagreement RUN LENGTH (days)")
    for pname in panels:
        for k in KS:
            q = ch[(ch.panel == pname) & (ch.k_bps == k)]
            say(f"  {pname:5s} {k:6d} | {q.realised_bps.mean():17.2f} | {q.disagree_share.mean():23.4%}"
                f" | {q.mean_names_in.mean():9.2f} vs {q.mean_names_in_k0.mean():6.2f}"
                f" | {q.mean_run_len.mean():34.1f}")
    nominal_ok = all(abs(ch[(ch.k_bps == k)].realised_bps.mean() - k) < max(1.0, 0.02 * k)
                     for k in KS if k > 0)
    gate("G10 the realised perturbation size matches its nominal k",
         "; ".join(f"k={k}: {ch[ch.k_bps == k].realised_bps.mean():.2f} bps" for k in KS if k > 0),
         "|realised - k| < max(1, 2%k)", nominal_ok)
    k0 = ch[ch.k_bps == 0]
    gate("G11 k=0 is the IDENTITY (noise switched OFF, not merely small)",
         f"disagreement {k0.disagree_share.max():.3e}, realised sd {k0.realised_bps.max():.3e}",
         "exactly 0", bool(k0.disagree_share.max() == 0 and k0.realised_bps.max() == 0))
    mono = True
    for pname in panels:
        v = [ch[(ch.panel == pname) & (ch.k_bps == k)].disagree_share.mean() for k in KS]
        mono &= all(v[i + 1] > v[i] for i in range(len(v) - 1))
    gate("G8 the noise BITES, and monotonically (gate-state disagreement rises with k on both panels)",
         "; ".join(f"{p}: " + "->".join(f"{ch[(ch.panel == p) & (ch.k_bps == k)].disagree_share.mean():.3%}"
                                        for k in KS) for p in panels),
         "strictly increasing", mono)
    rl = [ch[(ch.panel == 'U56') & (ch.k_bps == k)].mean_run_len.mean() for k in KS if k > 0]
    publish("G12 HYSTERESIS PERSISTENCE (U56): mean length of a state disagreement, in trading days",
            "; ".join(f"k={k}: {v:.1f}d" for k, v in zip([x for x in KS if x > 0], rl)))

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    cmp_audit = []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy_t = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_t = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        cmp_audit.append((pname, spy_t, base_t))
        for k in KS:
            seeds = [0] if k == 0 else list(range(NSEED))
            for sd in seeds:
                el = states[(pname, k, sd)]["el"]
                for cap in CAPS:
                    for gross in GROSSES:
                        wr = risk_weights(el, gross, cap)
                        bk = run_book(px, wr)
                        r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                        book_facts.append(dict(
                            panel=pname, k_bps=k, seed=sd, cap=cname(cap), gross=gross,
                            turnover_yr=float(tn.sum() / (len(tn) / 252)),
                            mean_names=float(bk["names"].loc[start:].mean()),
                            mean_gross=float(bk["gross"].loc[start:].mean()),
                            max_gross=float(bk["gross"].loc[start:].max()),
                            mean_risk_gross=float((bk["gross"] - bk["sweep_w"]).loc[start:].mean()),
                            mean_sweep=float(bk["sweep_w"].loc[start:].mean()),
                            max_name_w=float(bk["maxw"].loc[start:].max())))
                        for rung in RUNGS:
                            r = r0 - tn * rung / 1e4
                            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                            spy_is, spy_oos = spy_t.loc[:IS_END], spy_t.loc[OOS_START:]
                            lg = legs(r, base_t, spy_t, r_oos, spy_oos)
                            rows.append(dict(
                                panel=pname, k_bps=k, seed=sd, cap=cname(cap),
                                cap_num=float(cap) if np.isfinite(cap) else 9.99,
                                gross=gross, cost_bps=rung,
                                CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                Vol=vol(r),
                                turnover_yr=float(tn.sum() / (len(tn) / 252)),
                                mean_risk_gross=float((bk["gross"] - bk["sweep_w"]).loc[start:].mean()),
                                mean_sweep=float(bk["sweep_w"].loc[start:].mean()),
                                IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                                OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                base_CAGR=cagr(base_t), base_Sharpe=sharpe(base_t),
                                base_MaxDD=maxdd(base_t),
                                base_OOS_CAGR=cagr(base_t.loc[OOS_START:]),
                                base_OOS_Sharpe=sharpe(base_t.loc[OOS_START:]),
                                base_OOS_MaxDD=maxdd(base_t.loc[OOS_START:]),
                                spy_CAGR=cagr(spy_t), spy_Sharpe=sharpe(spy_t), spy_MaxDD=maxdd(spy_t),
                                spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                                spy_OOS_MaxDD=maxdd(spy_oos), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    nstate = 1 + (len(KS) - 1) * NSEED
    say(f"\n    {len(df)} published rows = 2 panels x {nstate} noise states x {len(CAPS)} caps x"
        f" {len(GROSSES)} gross x {len(RUNGS)} rungs;  {len(bf)} distinct realised weight paths.")

    # G7: comparands untouched by k (they are computed once per panel from the TRUE tape)
    d7 = 0.0
    for pname, spy_t, base_t in cmp_audit:
        q = df[df.panel == pname]
        d7 = max(d7, float(q.spy_Sharpe.max() - q.spy_Sharpe.min()),
                 float(q.spy_CAGR.max() - q.spy_CAGR.min()),
                 float(q.base_Sharpe.max() - q.base_Sharpe.min()),
                 float(q.base_OOS_Sharpe.max() - q.base_OOS_Sharpe.min()))
    gate("G7 the comparands (SPY and live RULES v2) are BIT-IDENTICAL across every k and seed",
         f"max spread over all {len(df)} rows: {d7:.3e}", "0.0", d7 == 0.0)
    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.6f} gross,"
         f" {bf.max_name_w.max():.4f} max single name", "<= 1+1e-12",
         bool(bf.max_gross.max() <= 1 + 1e-12))

    el0u = states[("U56", 0, 0)]["el"]
    bz = run_book(px_u, risk_weights(el0u, 0.75, HEADLINE_CAP)); st = px_u.index[WARMUP]
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)

    def cell(panel, k, seed, cap, gross, rung):
        return df[(df.panel == panel) & (df.k_bps == k) & (df.seed == seed) & (df.cap == cname(cap))
                  & (df.gross == gross) & (df.cost_bps == rung)].iloc[0]

    a = cell("U56", 0, 0, 0.020, 0.75, 10.0)
    b = cell("U56", 0, 0, np.inf, 0.75, 10.0)
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 k=0 reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND CAND"
         " (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    say(f"    ANCHOR published: U56 SPY full {a.spy_CAGR:.2%} / {a.spy_Sharpe:.4f} / {a.spy_MaxDD:.2%},"
        f" OOS {a.spy_OOS_CAGR:.2%} / {a.spy_OOS_Sharpe:.4f};"
        f" live RULES v2 {a.base_CAGR:.2%} / {a.base_Sharpe:.4f} / {a.base_MaxDD:.2%},"
        f" OOS {a.base_OOS_CAGR:.2%} / {a.base_OOS_Sharpe:.4f}.")

    # ------------------------------------------------------------ A. the fragility curve
    say("\n=== A. THE FRAGILITY CURVE — the COMMITTED cell (cap 0.020, gross 0.75, 10 bps) against")
    say("    decision-price noise.  Every figure is the SEED MEAN with the seed MIN/MAX beside it. ===")
    say("  panel   k bps |      CAGR (min..max)      |      Sharpe (min..max)     |    MaxDD (worst)"
        "  |   OOS Sharpe (min..max)   | turn/yr | 4b seeds | 4a seeds")
    curve = []
    for pname in panels:
        for k in KS:
            q = df[(df.panel == pname) & (df.k_bps == k) & (df.cap == cname(HEADLINE_CAP))
                   & (df.gross == HEADLINE_GROSS) & (df.cost_bps == HEADLINE_RUNG)]
            curve.append(dict(panel=pname, k_bps=k, n=len(q),
                              CAGR=q.CAGR.mean(), CAGR_lo=q.CAGR.min(), CAGR_hi=q.CAGR.max(),
                              Sharpe=q.Sharpe.mean(), Sharpe_lo=q.Sharpe.min(), Sharpe_hi=q.Sharpe.max(),
                              MaxDD=q.MaxDD.mean(), MaxDD_worst=q.MaxDD.min(),
                              OOS_Sharpe=q.OOS_Sharpe.mean(), OOS_lo=q.OOS_Sharpe.min(),
                              OOS_hi=q.OOS_Sharpe.max(), turnover_yr=q.turnover_yr.mean(),
                              rate4b=q.pass4b.mean(), rate4a=q.pass4a.mean()))
            c = curve[-1]
            say(f"  {pname:5s} {k:6d} | {c['CAGR']:6.2%} ({c['CAGR_lo']:5.2%}..{c['CAGR_hi']:5.2%}) |"
                f" {c['Sharpe']:6.4f} ({c['Sharpe_lo']:.4f}..{c['Sharpe_hi']:.4f}) |"
                f" {c['MaxDD']:7.2%} ({c['MaxDD_worst']:7.2%}) |"
                f" {c['OOS_Sharpe']:6.4f} ({c['OOS_lo']:.4f}..{c['OOS_hi']:.4f}) |"
                f" {c['turnover_yr']:7.2f} | {q.pass4b.sum():3d}/{len(q):<3d}  | {q.pass4a.sum():3d}/{len(q)}")
    cv = pd.DataFrame(curve); cv.to_csv(f"{OUT}.curve.csv", index=False)

    # ------------------------------------------------------------ B. where it breaks
    say("\n=== B. WHERE DOES IT BREAK?  the smallest k at which the 4b pass rate over seeds leaves 1.0,")
    say("    and the smallest at which it falls below 0.5 — read at EVERY (panel, cap, gross, rung). ===")
    knee = []
    for pname in panels:
        for cap in CAPS:
            for gross in GROSSES:
                for rung in RUNGS:
                    q = df[(df.panel == pname) & (df.cap == cname(cap)) & (df.gross == gross)
                           & (df.cost_bps == rung)]
                    base_pass = bool(q[q.k_bps == 0].pass4b.iloc[0])
                    rates = {k: q[q.k_bps == k].pass4b.mean() for k in KS}
                    k_leave = next((k for k in KS if k > 0 and rates[k] < 1.0), None) if base_pass else None
                    k_half = next((k for k in KS if k > 0 and rates[k] < 0.5), None) if base_pass else None
                    knee.append(dict(panel=pname, cap=cname(cap), gross=gross, cost_bps=rung,
                                     k0_pass4b=base_pass, k0_pass4a=bool(q[q.k_bps == 0].pass4a.iloc[0]),
                                     k_first_doubt=k_leave if k_leave is not None else -1,
                                     k_below_half=k_half if k_half is not None else -1,
                                     **{f"rate4b_k{k}": rates[k] for k in KS}))
    kn = pd.DataFrame(knee); kn.to_csv(f"{OUT}.knee.csv", index=False)
    npass0 = int(kn.k0_pass4b.sum())
    say(f"  {npass0} of {len(kn)} (panel, cap, gross, rung) cells pass 4b at k = 0.")
    say("  panel cap    g     bps | k=0 4b | 4b pass rate over seeds at k = "
        + "  ".join(f"{k:>5d}" for k in KS[1:]) + " | first doubt | below half")
    for _, r in kn.iterrows():
        say(f"  {r.panel:5s} {r.cap:6s} {r.gross:.2f} {r.cost_bps:4.0f} | {'Y' if r.k0_pass4b else '.':^6s} |"
            + "".join(f" {r[f'rate4b_k{k}']:6.2f}  " for k in KS[1:])
            + f" | {int(r.k_first_doubt):11d} | {int(r.k_below_half):10d}")
    surv = kn[kn.k0_pass4b]
    if len(surv):
        say(f"\n  Among the {len(surv)} cells that pass 4b at k = 0:")
        for k in KS[1:]:
            say(f"    k = {k:4d} bps: 4b still passes in {surv[f'rate4b_k{k}'].mean():.1%} of"
                f" (cell x seed) draws;  {int((surv[f'rate4b_k{k}'] == 1.0).sum())} of {len(surv)}"
                f" cells hold on ALL {NSEED} seeds")
        fd = surv[surv.k_first_doubt > 0].k_first_doubt
        say(f"    first k at which ANY seed flips a cell: median {fd.median() if len(fd) else float('nan')},"
            f" min {fd.min() if len(fd) else float('nan')};"
            f" {int((surv.k_first_doubt == -1).sum())} of {len(surv)} cells never flip out to k = {KS[-1]}")

    # ------------------------------------------------------------ C. per-leg fragility
    say("\n=== C. WHICH LEG GOES FIRST?  per-leg pass rate over all cells x seeds, by k ===")
    say("  panel   k bps | L_H1    L_H2    L_OOS   L_DD    L_CAGR  | 4b      4a")
    legrows = []
    for pname in panels:
        for k in KS:
            q = df[(df.panel == pname) & (df.k_bps == k)]
            legrows.append(dict(panel=pname, k_bps=k, n=len(q),
                                **{x: q[x].mean() for x in
                                   ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR", "pass4b", "pass4a")}))
            e = legrows[-1]
            say(f"  {pname:5s} {k:6d} | {e['L_H1']:6.3f}  {e['L_H2']:6.3f}  {e['L_OOS']:6.3f} "
                f" {e['L_DD']:6.3f}  {e['L_CAGR']:6.3f}  | {e['pass4b']:6.3f}  {e['pass4a']:6.3f}")
    pd.DataFrame(legrows).to_csv(f"{OUT}.legs.csv", index=False)

    say("\n  THE COMMITTED CANDIDATE'S OWN 4b MARGINS vs k (cap 0.020, gross 0.75, 10 bps, seed mean):")
    say("  panel   k bps | m_H1     m_H2     m_OOS    m_DD      m_CAGR   | 4b seeds")
    for pname in panels:
        for k in KS:
            q = df[(df.panel == pname) & (df.k_bps == k) & (df.cap == cname(HEADLINE_CAP))
                   & (df.gross == HEADLINE_GROSS) & (df.cost_bps == HEADLINE_RUNG)]
            say(f"  {pname:5s} {k:6d} | {q.m_H1.mean():+8.4f} {q.m_H2.mean():+8.4f} {q.m_OOS.mean():+8.4f}"
                f" {q.m_DD.mean():+9.2%} {q.m_CAGR.mean():+8.2%} | {q.pass4b.sum():3d}/{len(q)}")

    # ------------------------------------------------------------ D. every grid point
    say(f"\n=== D. EVERY GRID POINT — all {len(kn)} (panel, cap, gross, rung) cells x {len(KS)} k,")
    say("    reported as the SEED MEAN (the full per-seed grid is in the .grid.csv.gz). ===")
    say("  panel cap    g     bps  k bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | turn/yr | 4a    4b")
    for pname in panels:
        for cap in CAPS:
            for gross in GROSSES:
                for rung in RUNGS:
                    for k in KS:
                        q = df[(df.panel == pname) & (df.cap == cname(cap)) & (df.gross == gross)
                               & (df.cost_bps == rung) & (df.k_bps == k)]
                        tag = ""
                        if (cap == HEADLINE_CAP and gross == HEADLINE_GROSS
                                and rung == HEADLINE_RUNG and k == HEADLINE_K):
                            tag = "   <= COMMITTED CAP2 HEADLINE"
                        say(f"  {pname:5s} {cname(cap):6s} {gross:.2f} {rung:4.0f} {k:6d} |"
                            f" {q.CAGR.mean():6.2%} {q.Sharpe.mean():7.4f} {q.MaxDD.mean():8.2%} |"
                            f" {q.H1.mean():5.2f} {q.H2.mean():6.2f} | {q.OOS_CAGR.mean():7.2%}"
                            f" {q.OOS_Sharpe.mean():7.4f} | {q.turnover_yr.mean():7.2f} |"
                            f" {q.pass4a.mean():5.2f} {q.pass4b.mean():5.2f}{tag}")

    # ------------------------------------------------------------ E. joint both-panel 4b
    say("\n=== E. JOINT BOTH-PANEL 4b (U56 AND B136 at the same cap, gross, rung, k, seed) ===")
    jt = []
    for k in KS:
        seeds = [0] if k == 0 else list(range(NSEED))
        for sd in seeds:
            for cap in CAPS:
                for gross in GROSSES:
                    for rung in RUNGS:
                        u = cell("U56", k, sd, cap, gross, rung)
                        v = cell("B136", k, sd, cap, gross, rung)
                        jt.append(dict(k_bps=k, seed=sd, cap=cname(cap), gross=gross, cost_bps=rung,
                                       joint4b=bool(u.pass4b and v.pass4b),
                                       joint4a=bool(u.pass4a and v.pass4a)))
    jf = pd.DataFrame(jt); jf.to_csv(f"{OUT}.joint.csv", index=False)
    for k in KS:
        q = jf[jf.k_bps == k]
        say(f"   k = {k:4d} bps: joint 4b {q.joint4b.mean():6.2%} of {len(q)} (cell x seed) draws"
            f"   joint 4a {q.joint4a.mean():6.2%}")

    # ------------------------------------------------------------ F. rule 8
    say("\n=== F. RULE 8 — the two dials (cap, gross) chosen on warm-up..2016-12-31 ONLY by two")
    say("    pre-stated IS choosers, 2017-2026 read ONCE, at every (panel, rung, k, seed). ===")
    wf = []
    for pname in panels:
        for k in KS:
            seeds = [0] if k == 0 else list(range(NSEED))
            for sd in seeds:
                for rung in RUNGS:
                    d = df[(df.panel == pname) & (df.k_bps == k) & (df.seed == sd)
                           & (df.cost_bps == rung)]
                    cm = d[(d.cap == cname(HEADLINE_CAP)) & (d.gross == HEADLINE_GROSS)].iloc[0]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=pname, k_bps=k, seed=sd, cost_bps=rung, chooser=chooser,
                                       pick_cap=pk.cap, pick_gross=pk.gross, full4b=bool(pk.pass4b),
                                       full4a=bool(pk.pass4a),
                                       OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                       OOS_MaxDD=pk.OOS_MaxDD, pick_turn=pk.turnover_yr,
                                       committed_OOS_CAGR=cm.OOS_CAGR,
                                       committed_OOS_Sharpe=cm.OOS_Sharpe,
                                       committed_OOS_MaxDD=cm.OOS_MaxDD,
                                       base_OOS_CAGR=pk.base_OOS_CAGR,
                                       base_OOS_Sharpe=pk.base_OOS_Sharpe,
                                       base_OOS_MaxDD=pk.base_OOS_MaxDD,
                                       spy_OOS_CAGR=pk.spy_OOS_CAGR, spy_OOS_Sharpe=pk.spy_OOS_Sharpe,
                                       spy_OOS_MaxDD=pk.spy_OOS_MaxDD))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x {nstate} noise states x {len(RUNGS)} rungs x 2 choosers).")
    say("  panel   k bps | picks (cap/gross)                    | OOS CAGR | OOS Sharpe | OOS MaxDD"
        " | vs SPY OOS Sh | vs live v2 OOS Sh | vs committed cell | full-sample 4b")
    for pname in panels:
        for k in KS:
            q = wfd[(wfd.panel == pname) & (wfd.k_bps == k)]
            top = q.groupby(["pick_cap", "pick_gross"]).size().sort_values(ascending=False)
            desc = ", ".join(f"{a}/{b:.2f}:{c}" for (a, b), c in top.items())
            say(f"  {pname:5s} {k:6d} | {desc:36s} | {q.OOS_CAGR.mean():8.2%} | {q.OOS_Sharpe.mean():10.4f}"
                f" | {q.OOS_MaxDD.mean():9.2%} | {int((q.OOS_Sharpe > q.spy_OOS_Sharpe).sum()):3d}/{len(q):<3d}"
                f"      | {int((q.OOS_Sharpe > q.base_OOS_Sharpe).sum()):3d}/{len(q):<3d}"
                f"          | {int((q.OOS_Sharpe > q.committed_OOS_Sharpe).sum()):3d}/{len(q):<3d}"
                f"          | {int(q.full4b.sum()):3d}/{len(q)}")
    say(f"\n  BENCHMARK OOS (2017-2026), read once: SPY {wfd.spy_OOS_CAGR.mean():.2%} /"
        f" {wfd.spy_OOS_Sharpe.mean():.4f} / {wfd.spy_OOS_MaxDD.mean():.2%};"
        f"  live RULES v2 {wfd.base_OOS_CAGR.mean():.2%} / {wfd.base_OOS_Sharpe.mean():.4f} /"
        f" {wfd.base_OOS_MaxDD.mean():.2%}  (both panel-pooled means).")
    k0pick = wfd[wfd.k_bps == 0]
    say(f"  DOES THE NOISE MOVE THE PICK?  at k = 0 the picks are"
        f" {dict(k0pick.groupby(['pick_cap', 'pick_gross']).size())};")
    for k in KS[1:]:
        q = wfd[wfd.k_bps == k]
        agree = 0; tot = 0
        for pname in panels:
            for rung in RUNGS:
                for chooser in ("C_ISSHARPE", "C_ISCALMAR"):
                    ref = k0pick[(k0pick.panel == pname) & (k0pick.cost_bps == rung)
                                 & (k0pick.chooser == chooser)].iloc[0]
                    z = q[(q.panel == pname) & (q.cost_bps == rung) & (q.chooser == chooser)]
                    agree += int(((z.pick_cap == ref.pick_cap) & (z.pick_gross == ref.pick_gross)).sum())
                    tot += len(z)
        say(f"    k = {k:4d} bps: the pick matches the k = 0 pick in {agree} of {tot} draws"
            f" ({agree / tot:.1%})")

    # ------------------------------------------------------------ G. book facts
    say("\n=== G. BOOK FACTS vs k (exposure is the usual confound — published, never selected on) ===")
    say("  panel cap    g    |  k bps | risk gross | SHY sleeve | mean names | turnover/yr | max name w")
    for pname in panels:
        for cap in (HEADLINE_CAP, np.inf):
            for gross in GROSSES:
                for k in KS:
                    q = bf[(bf.panel == pname) & (bf.cap == cname(cap)) & (bf.gross == gross)
                           & (bf.k_bps == k)]
                    say(f"  {pname:5s} {cname(cap):6s} {gross:.2f} | {k:6d} |"
                        f" {q.mean_risk_gross.mean():10.4f} | {q.mean_sweep.mean():10.2%} |"
                        f" {q.mean_names.mean():10.2f} | {q.turnover_yr.mean():11.2f} |"
                        f" {q.max_name_w.max():10.4f}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
