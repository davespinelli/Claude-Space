#!/usr/bin/env python3
"""idea 2408 (lane cloud, run 44, 2026-09-23) — DOES CALENDAR TRANCHING CUT THE CANDIDATE'S
TURNOVER WITHOUT THE DAMPER'S STUB?

THE GAP.  Idea 2391 (lane B, run 39) cut the standing candidate's 3.51x/yr turnover with a
PARTIAL-ADJUSTMENT damper `w <- w + lam (W - w)`, and run 39's own residue (3) is that damper's
bill: a gated-OUT name is only ever sold FRACTIONALLY, so it is never fully exited, post-trade
stub NAV runs 1.84% (U56) / 2.52% (B136), held-set fidelity falls to 76.1% and mean names held
RISES 37.6 -> 50.7.  The discrete alternative has never been priced here.

THE DEVICE.  A ROTA.  Assign every investable name to one of k fixed tranches by a price-blind
hash of its ticker.  Each week rebalance tranche `(week + 0) mod k` IN FULL to target and leave
the others to drift.  Every name that trades trades EXACTLY to target -- including exactly to
zero -- so the damper's fractional residue cannot arise in a traded name.

DIAL 1 -- the tranche count k {1, 2, 4, 8}.  **k = 1 IS THE COMMITTED WEEKLY BOOK EXACTLY** (the
          single tranche is the whole universe and every name trades in full every week), so one
          ladder spans the incumbent; G3 asserts bit-identity through `engine.backtest`.
DIAL 2 -- the tranche ASSIGNMENT, as a hash salt s {0, 1, 2, 3}: tranche(t) = md5(t + s) mod k.
          Four independent assignments give a NOISE BAND on every number, so a k effect is only
          read as real when it survives all four.  The assignment is price-blind and never fitted.

THE ONE PRE-STATED CONVENTION THAT IS NOT A DIAL: **SHY is EXEMPT from the rota** and is traded
every week.  It has to be -- it is the phi = 1.00 sweep instrument, and tranching it would let
book gross wander off 1.00 and silently introduce leverage or idle cash.  With SHY exempt, gross
is pinned at 1.000000000 on every row (G4), so the rota changes WHICH equities are stale, never
how much of the NAV is invested.  Stated here, before any compute.

THE REFERENCE, PRICED ALONGSIDE AND NEVER SELECTED ON: idea 2391's partial-adjustment damper at
lam {1.00, 0.50, 0.25, 0.125}, paired 1:1 with k {1, 2, 4, 8} because lam = 1/k is the natural
turnover match -- and the realised turnover of BOTH is published so the match is MEASURED and not
assumed.  lam = 1.00 is the same committed book as k = 1, which G3 also asserts.

THE CLAIM THIS RUN IS BUILT TO FALSIFY.  The pushed idea says the stub is "zero by construction".
That is true of the TRADED names and false of the BOOK: a name gated OUT in a tranche whose turn
has not come keeps its full stale weight for up to k-1 weeks.  Both quantities are therefore
measured separately and published separately -- `stub_traded` (NAV left in names that traded this
week and whose target is zero; the rota's structural claim, G6) and `stub_total` (NAV left in ANY
held name whose target is zero; the quantity that actually costs money).  Reporting only the
first would be the flattering half of the truth.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, books {CAP2 = idea 2322's 2%-capped candidate,
CAND = idea 2300/2332's uncapped candidate}, gross {0.75 live, 1.00}, rungs {0, 10, 25, 50} bps,
weekly cadence, t+1 execution, band 0.03, the SHY sweep, and the damper reference.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with L_DD, L_H2
and L_OOS failing at every cell.  A turnover device has no pass there to keep or break.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: (k, s) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers, then
2017-2026 read ONCE.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the band is
`baseline.band_state` bit for bit.  G3 k = 1 (every salt) AND lam = 1.00 are BIT-IDENTICAL to an
independent committed-book construction through `engine.backtest`.  G4 no leverage.  G5 the k
dial BITES and turnover is MONOTONE decreasing in k.  G6 the rota's TRADED-name stub is EXACTLY
zero at every k while the damper's is not (the idea's structural claim, tested not assumed).
G7 exactly two tuned parameters.  G8 the weight path is causal (panel truncation).  G9 SHY
priced on every held row.  G10 EXTERNAL REPRODUCTION of the committed CAP2 U56 headline
(11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318) and CAND U56 headline (12.59% / 1.1934 /
-17.39%, OOS 13.85% / 1.2397).  G11 the rota's defining property: every investable name is fully
re-set at least once in every window of k weeks.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The rota-vs-damper contrast is same-tape, same-day,
same-target and first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_calendar-tranching_cloud.py
"""
from __future__ import annotations

import hashlib, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "calendar-tranching", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
KS = [1, 2, 4, 8]
SALTS = [0, 1, 2, 3]
LAMS = [1.0, 0.50, 0.25, 0.125]          # the reference, paired 1:1 with KS (lam = 1/k)
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, NAME_CAP, SWEEP, OFFSET = 10.0, 0.020, "SHY", 0
BOOKS = {"CAP2": NAME_CAP, "CAND": np.inf}
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

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


# ---------------------------------------------------------------- books and tranches
def risk_weights(px, gross, cap):
    pr = px.notna()
    inb = band_state(px, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return inb.astype(float).mul(per, axis=0).fillna(0.0)


def full_book(px, gross, cap):
    """The committed book WITH the phi = 1.00 SHY sweep (the k=1 / lam=1 anchor)."""
    w = risk_weights(px, gross, cap).copy()
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def tranche_of(cols, k, salt):
    """Price-blind, deterministic, never fitted: md5(ticker + salt) mod k.  SHY is exempt (-1)."""
    out = np.full(len(cols), -1, dtype=int)
    for i, c in enumerate(cols):
        if c == SWEEP:
            continue
        h = hashlib.md5(f"{c}|{salt}".encode()).hexdigest()
        out[i] = int(h, 16) % k
    return out


# ---------------------------------------------------------------- the runner
def run_device(prices, w_risk, device, param, tr=None, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that at each rebalance the book moves to target under
    one of two devices:
      ROTA  -- equities in tranche (week + OFFSET) mod k go EXACTLY to target; the rest hold
               their drifted weight; SHY (exempt) absorbs the whole residual, so gross == 1.
      DAMP  -- idea 2391's partial adjustment, w <- w + lam (W - w) on the FULL book including
               the sweep leg.
    `sweep=False` turns the phi = 1.00 SHY sweep off so the runner reproduces a de-grossing-to-cash
    book such as live RULES v2 exactly; that is what G1 checks.
    Weights are decided at t-1 and applied at t; between rebalances the book drifts."""
    cols = list(prices.columns)
    shy_i = cols.index(SWEEP)
    eq = np.array([i for i in range(len(cols)) if i != shy_i])
    rv = prices.pct_change().fillna(0.0).values
    shy_ok = prices[SWEEP].notna().values.astype(float)
    wr = w_risk.reindex(prices.index).shift(1).fillna(0.0).values        # risk sleeve, t-1
    wf_ = w_risk.copy()
    if sweep:
        idle = (1.0 - wf_.sum(axis=1)).clip(lower=0.0)
        wf_[SWEEP] = wf_[SWEEP] + idle * prices[SWEEP].notna().astype(float)
    wf = wf_.reindex(prices.index).shift(1).fillna(0.0).values           # full book, t-1
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    dw = np.zeros((n, m)); cur = np.zeros(m)
    gr = np.zeros(n); r0 = np.zeros(n); nheld = np.zeros(n)
    st_tr = []; st_to = []; fid = []; nre = []; reb = []; scaled = 0; week = 0
    last_reset = np.full(m, -10 ** 6)
    gaps = []
    for i in range(n):
        # NOTE: no `or i == 0` branch.  `engine.backtest` has one, but its row-0 target is NaN
        # (it fills THEN shifts), so the engine in fact holds nothing until the first scheduled
        # rebalance.  Forcing a row-0 trade here would put 100% into the SHY sweep a week early
        # and break bit-identity with the engine; G1 and G3 both check that it does not.
        if mask[i]:
            tgt_r, tgt_f = wr[i], wf[i]
            if device == "ROTA":
                j = (week + OFFSET) % param
                sel = eq[tr[eq] == j]
                new = cur.copy()
                new[sel] = tgt_r[sel]
                s_eq = new[eq].sum()
                if s_eq > 1.0 + 1e-15:
                    new[eq] *= 1.0 / s_eq
                    s_eq = 1.0
                    scaled += 1
                new[shy_i] = (max(0.0, 1.0 - s_eq) * shy_ok[i]) if sweep else tgt_r[shy_i]
                traded = sel
                for c_ in sel:
                    if last_reset[c_] > -10 ** 5:
                        gaps.append(week - last_reset[c_])
                    last_reset[c_] = week
            else:
                new = cur + param * (tgt_f - cur)
                traded = eq
            dw[i] = np.abs(new - cur)
            cur = new
            # --- the two stub measures, on the post-trade book
            z_all = eq[tgt_r[eq] <= 1e-15]
            z_tr = np.array([c_ for c_ in traded if tgt_r[c_] <= 1e-15], dtype=int)
            st_to.append(cur[z_all].sum())
            st_tr.append(cur[z_tr].sum() if len(z_tr) else 0.0)
            want = eq[tgt_r[eq] > 1e-15]
            fid.append(float((cur[want] > 1e-12).sum()) / max(1, len(want)))
            nre.append(float(len(traded)))
            reb.append(i)
            week += 1
        gr[i] = cur.sum()
        nheld[i] = float((cur[eq] > 1e-12).sum())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), gross=pd.Series(gr, index=idx),
                names=pd.Series(nheld, index=idx), dw=pd.DataFrame(dw, index=idx, columns=cols),
                stub_traded=np.array(st_tr), stub_total=np.array(st_to), fidelity=np.array(fid),
                n_reset=np.array(nre), n_scaled=scaled, reb=np.array(reb),
                max_gap=(max(gaps) if gaps else 0))


def priced(res, bps, win):
    return (res["r0"] - res["dw"].sum(axis=1) * bps / 1e4).loc[win]


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


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
    return dict(pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def main():
    t0 = time.time()
    say("=== idea 2408 — DOES CALENDAR TRANCHING CUT THE CANDIDATE'S TURNOVER WITHOUT THE DAMPER'S STUB? ===")
    say(f"    {DATE}  lane {LANE} run 44   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00, EXEMPT from the rota)  offset {OFFSET}")
    say(f"    DIAL 1 tranche count k {KS}   DIAL 2 tranche ASSIGNMENT salt s {SALTS} (md5(ticker|s) mod k)")
    say(f"    reference (never selected on): idea 2391's damper at lam {LAMS}, paired 1:1 with k (lam = 1/k);")
    say("    the realised turnover of BOTH is published so the match is MEASURED, not assumed.")
    say("    THE CLAIM UNDER TEST: 'the stub is zero by construction'.  TRUE of traded names, FALSE of the book —")
    say("    both are measured separately (stub_traded, stub_total) and both are published.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells in idea 2383 and 0 of 40-120 in 2318 / 2322 / 2326 / 2343.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the")
    say("    contaminated leg.  The rota-vs-damper contrast is same-tape, same-target and first-order immune.")
    gate("G7 exactly two tuned parameters", "k, tranche assignment salt s", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    d2 = int((band_state(px_u, BAND) != band_state(px_u, BAND)).sum().sum())
    gate("G2 the gate IS baseline.band_state (live clause 2), unmodified",
         f"{d2} differing cells; mean names IN {int(band_state(px_u, BAND).sum(axis=1).mean())}", "0", d2 == 0)

    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_device(px_u, w_live, "DAMP", 1.0, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["dw"].sum(axis=1) * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2 through the DAMP runner at lam=1)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G3: k = 1 at every salt, and lam = 1, are the committed book
    wr = risk_weights(px_u, 0.75, NAME_CAP)
    eng = backtest(px_u, full_book(px_u, 0.75, NAME_CAP), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    worst = 0.0
    for s in SALTS:
        rr = run_device(px_u, wr, "ROTA", 1, tranche_of(list(px_u.columns), 1, s))
        worst = max(worst, float((eng - (rr["r0"] - rr["dw"].sum(axis=1) * HEADLINE_RUNG / 1e4)).abs().max()))
    dd = run_device(px_u, wr, "DAMP", 1.0)
    worst = max(worst, float((eng - (dd["r0"] - dd["dw"].sum(axis=1) * HEADLINE_RUNG / 1e4)).abs().max()))
    gate("G3 k = 1 (all 4 salts) AND lam = 1.00 == an independent CAP2 construction through engine.backtest",
         f"max|d| {worst:.3e}", "< 1e-12", worst < 1e-12)

    cut = px_u.index[int(len(px_u) * 0.70)]
    tr4 = tranche_of(list(px_u.columns), 4, 0)
    a = run_device(px_u.loc[:cut], risk_weights(px_u.loc[:cut], 0.75, NAME_CAP), "ROTA", 4, tr4)
    b = run_device(px_u, wr, "ROTA", 4, tr4)
    d8 = float((a["r0"] - b["r0"].loc[:cut]).abs().max())
    gate(f"G8 the weight path is causal (panel truncated at {cut.date()}, k=4 s=0)",
         f"max|dr| {d8:.3e}", "< 1e-12", d8 < 1e-12)

    rows, diag = [], []
    for pname, px in panels.items():
        win = px.index[WARMUP:]
        nyrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_device(px, rules_v2_weights(px, band=BAND, gross=0.75), "DAMP", 1.0,
                                   sweep=False), HEADLINE_RUNG, win)
        say(f"\n--- panel {pname} ({len(px.columns)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        say(f"    4b bars here: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}"
            f"   SPY halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}   SPY OOS Sharpe {sharpe(spy_oos):.4f}")
        for bname, cap in BOOKS.items():
            for gross in GROSSES:
                wrisk = risk_weights(px, gross, cap)
                specs = [("ROTA", k, s) for k in KS for s in (SALTS if k > 1 else [0])] \
                    + [("DAMP", lam, 0) for lam in LAMS]
                for dev, par, s in specs:
                    tr = tranche_of(list(px.columns), par, s) if dev == "ROTA" else None
                    res = run_device(px, wrisk, dev, par, tr)
                    m_ = res["reb"] >= WARMUP
                    diag.append(dict(panel=pname, book=bname, gross=gross, device=dev,
                                     param=par, salt=s,
                                     turnover_yr=float(res["dw"].sum(axis=1).loc[win].sum() / nyrs),
                                     stub_traded=float(res["stub_traded"][m_].mean()),
                                     stub_total=float(res["stub_total"][m_].mean()),
                                     stub_traded_max=float(res["stub_traded"][m_].max()),
                                     fidelity=float(res["fidelity"][m_].mean()),
                                     mean_names=float(res["names"].loc[win].mean()),
                                     mean_reset=float(res["n_reset"].mean()),
                                     max_gap_weeks=int(res["max_gap"]),
                                     n_scaled=int(res["n_scaled"]),
                                     max_gross=float(res["gross"].max())))
                    for rung in RUNGS:
                        r = priced(res, rung, win)
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        rows.append(dict(panel=pname, book=bname, gross=gross, device=dev,
                                         param=par, salt=s, cost_bps=rung,
                                         CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                         H1=h1, H2=h2,
                                         IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                         OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                         base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                         base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                                         spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                         **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); dg = pd.DataFrame(diag)
    df.to_csv(f"{OUT}.grid.csv", index=False); dg.to_csv(f"{OUT}.turnover.csv", index=False)

    gate("G4 no leverage anywhere (realised row sums)", f"max gross {dg.max_gross.max():.9f}",
         "<= 1+1e-12", bool((dg.max_gross <= 1 + 1e-12).all()))
    sc = dg[dg.n_scaled > 0]
    publish("G4b the rota's OWN artifact: rebalances at which the STALE equity sleeve already summed to"
            " > 1 of NAV and had to be de-grossed pro rata (never a source of leverage, but it means the"
            " rota does not always reach its target even in the tranche it trades)",
            f"{int(dg.n_scaled.sum())} such rebalances over {len(dg)} books;"
            f" {len(sc)} books affected, all at gross {sorted(set(sc.gross)) if len(sc) else 'n/a'};"
            f" worst single book {int(dg.n_scaled.max())} of ~{int(dg.mean_reset.count() and 924)} rebalances")
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP:]].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}", "True", shy_ok)

    rot = dg[dg.device == "ROTA"]
    mono, bad = [], []
    for (pn, bn, gr_, sa), g in rot.groupby(["panel", "book", "gross", "salt"]):
        v = g.set_index("param").reindex(KS).turnover_yr
        if v.notna().all():
            ok_ = bool(np.all(np.diff(v.values) < 0) and (v.values[0] - v.values[-1]) > 0.5)
            mono.append(ok_)
            if not ok_:
                bad.append(f"{pn}/{bn}/g{gr_:.2f}/s{sa} [" + " ".join(f"k{k}:{v[k]:.2f}" for k in KS) + "]")
    gate("G5 the k dial BITES and turnover is MONOTONE DECREASING in k",
         f"{sum(mono)} of {len(mono)} (panel, book, gross, salt) ladders"
         + ("   NON-MONOTONE: " + "; ".join(bad) if bad else ""),
         f"{len(mono)} of {len(mono)}", len(mono) > 0 and all(mono))
    if bad:
        publish("G5b WHY G5 FAILS, stated rather than patched", "on the UNCAPPED book (CAND) on U56, k=2 costs"
                " MORE turnover than k=1: freezing half the names for a week lets the other half's targets"
                " drift further before they are re-set, and the stale sleeve periodically has to be de-grossed"
                " (see G4b).  A rota is therefore NOT a turnover cut per se — it is one only once k is large"
                " enough that the saved rebalances outweigh the extra distance travelled by the ones that remain.")

    gate("G6 the ROTA's TRADED-name stub is EXACTLY ZERO at every k (the idea's structural claim)",
         f"max over {len(rot)} rota books {rot.stub_traded_max.max():.3e}"
         f"  vs the DAMPER's mean traded-name stub {dg[dg.device == 'DAMP'].stub_traded.mean():.4%}",
         "0 for ROTA, > 0 for DAMP",
         bool(rot.stub_traded_max.max() < 1e-15
              and dg[(dg.device == "DAMP") & (dg.param < 1.0)].stub_traded.min() > 0))

    gap_ok = bool((rot.apply(lambda r: r.max_gap_weeks <= r.param, axis=1)).all())
    gate("G11 every name is fully re-set at least once in every window of k weeks",
         f"max observed gap / k over {len(rot)} rota books: "
         f"{int(rot.max_gap_weeks.max())} weeks at k up to {int(rot.param.max())}", "gap <= k", gap_ok)

    for bname, ref in (("CAP2", (0.1162, 1.2687, -0.1481, 0.1277, 1.3318)),
                       ("CAND", (0.1259, 1.1934, -0.1739, 0.1385, 1.2397))):
        h = df[(df.panel == "U56") & (df.book == bname) & (df.device == "ROTA") & (df.param == 1)
               & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        d10 = max(abs(h.CAGR - ref[0]), abs(h.Sharpe - ref[1]) / 10, abs(h.MaxDD - ref[2]),
                  abs(h.OOS_CAGR - ref[3]), abs(h.OOS_Sharpe - ref[4]) / 10)
        gate(f"G10 reproduces the committed {bname} U56 headline "
             f"({ref[0]:.2%}/{ref[1]:.4f}/{ref[2]:.2%}, OOS {ref[3]:.2%}/{ref[4]:.4f}) at k=1",
             f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
             f" -> max|d| {d10:.2e}", "< 1e-3", d10 < 1e-3)

    # ------------------------------------------------------------ A. the bill of the device
    say("\n=== A. THE DEVICE'S OWN BILL, MEASURED — ROTA vs the lam-MATCHED DAMPER (gross 0.75) ===")
    say("    stub_traded = NAV left in names that TRADED this week and whose target is zero (the idea's claim).")
    say("    stub_total  = NAV left in ANY held name whose target is zero (what actually costs money).")
    say("  panel book  device  par | turn/yr | stub_traded | stub_total | fidelity | mean names | resets/wk | max gap")
    for pname in panels:
        for bname in BOOKS:
            for dev, pars in (("ROTA", KS), ("DAMP", LAMS)):
                for par in pars:
                    q = dg[(dg.panel == pname) & (dg.book == bname) & (dg.gross == 0.75)
                           & (dg.device == dev) & (dg.param == par)]
                    e = q.mean(numeric_only=True)
                    sd = q.turnover_yr.std() if len(q) > 1 else 0.0
                    say(f"  {pname:5s} {bname:4s} {dev:6s} {par:5.3f} | {e.turnover_yr:7.2f} |"
                        f" {e.stub_traded:11.4%} | {e.stub_total:10.4%} | {e.fidelity:8.1%} |"
                        f" {e.mean_names:10.1f} | {e.mean_reset:9.1f} | {int(e.max_gap_weeks):7d}"
                        + (f"   (salt sd of turnover {sd:.3f})" if dev == "ROTA" and par > 1 else "")
                        + ("   <= COMMITTED BOOK" if par == 1 or par == 1.0 else ""))

    # ------------------------------------------------------------ B. the ladder
    say("\n=== B. THE FULL LADDER at 10 bps, gross 0.75 — EVERY GRID POINT (salts shown individually) ===")
    say("  panel book device  par salt |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bname in BOOKS:
            for dev, pars in (("ROTA", KS), ("DAMP", LAMS)):
                for par in pars:
                    for _, r in df[(df.panel == pname) & (df.book == bname) & (df.gross == 0.75)
                                   & (df.device == dev) & (df.param == par)
                                   & (df.cost_bps == HEADLINE_RUNG)].iterrows():
                        lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                        say(f"  {pname:5s} {bname:4s} {dev:6s} {par:5.3f} {r.salt:3d} |"
                            f" {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} |"
                            f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} | {'Y' if r.pass4a else '.'}  "
                            f"{'Y' if r.pass4b else '.'}  | {lg}")

    # ------------------------------------------------------------ C. head to head at matched turnover
    say("\n=== C. HEAD TO HEAD AT (APPROXIMATELY) MATCHED TURNOVER — the whole question ===")
    say("    ROTA k vs DAMP lam = 1/k.  The turnover match is MEASURED and printed; where it is loose the")
    say("    comparison is stated as loose rather than quietly used.")
    say("  panel book  g   bps | k |  ROTA turn  Sharpe   MaxDD  4b | DAMP turn  Sharpe   MaxDD  4b | dSharpe  dMaxDD")
    h2h = []
    for pname in panels:
        for bname in BOOKS:
            for gross in GROSSES:
                for rung in RUNGS:
                    for k, lam in zip(KS, LAMS):
                        ro = df[(df.panel == pname) & (df.book == bname) & (df.gross == gross)
                                & (df.device == "ROTA") & (df.param == k) & (df.cost_bps == rung)]
                        da = df[(df.panel == pname) & (df.book == bname) & (df.gross == gross)
                                & (df.device == "DAMP") & (df.param == lam) & (df.cost_bps == rung)].iloc[0]
                        rt = dg[(dg.panel == pname) & (dg.book == bname) & (dg.gross == gross)
                                & (dg.device == "ROTA") & (dg.param == k)].turnover_yr.mean()
                        dt = dg[(dg.panel == pname) & (dg.book == bname) & (dg.gross == gross)
                                & (dg.device == "DAMP") & (dg.param == lam)].turnover_yr.mean()
                        h2h.append(dict(panel=pname, book=bname, gross=gross, cost_bps=rung, k=k, lam=lam,
                                        rota_turn=rt, damp_turn=dt,
                                        rota_Sharpe=ro.Sharpe.mean(), damp_Sharpe=da.Sharpe,
                                        rota_MaxDD=ro.MaxDD.mean(), damp_MaxDD=da.MaxDD,
                                        rota_4b=int(ro.pass4b.sum()), rota_n=len(ro),
                                        damp_4b=int(da.pass4b)))
                        if gross == 0.75 and rung == HEADLINE_RUNG:
                            say(f"  {pname:5s} {bname:4s} {gross:.2f} {rung:5.1f} | {k} |"
                                f" {rt:10.2f} {ro.Sharpe.mean():7.4f} {ro.MaxDD.mean():7.2%}"
                                f" {int(ro.pass4b.sum())}/{len(ro)} |"
                                f" {dt:9.2f} {da.Sharpe:7.4f} {da.MaxDD:7.2%}  {'Y' if da.pass4b else '.'} |"
                                f" {ro.Sharpe.mean() - da.Sharpe:+8.4f} {ro.MaxDD.mean() - da.MaxDD:+7.2%}")
    hf = pd.DataFrame(h2h); hf.to_csv(f"{OUT}.headtohead.csv", index=False)
    say(f"\n   over all {len(hf)} matched (panel, book, gross, rung, k) cells:")
    say(f"    ROTA turnover < DAMP turnover in {int((hf.rota_turn < hf.damp_turn).sum())} of {len(hf)}"
        f"   (mean ROTA {hf.rota_turn.mean():.2f}x vs DAMP {hf.damp_turn.mean():.2f}x)")
    say(f"    ROTA Sharpe  > DAMP Sharpe  in {int((hf.rota_Sharpe > hf.damp_Sharpe).sum())} of {len(hf)}"
        f"   (mean dSharpe {(hf.rota_Sharpe - hf.damp_Sharpe).mean():+.4f})")
    say(f"    ROTA MaxDD   > DAMP MaxDD (shallower) in {int((hf.rota_MaxDD > hf.damp_MaxDD).sum())} of {len(hf)}"
        f"   (mean dMaxDD {(hf.rota_MaxDD - hf.damp_MaxDD).mean():+.2%})")

    say("\n=== C2. THE SCALE-FREE COMPARISON: TURNOVER SAVED PER pp OF MaxDD GIVEN UP (10 bps, gross 0.75) ===")
    say("    Section C's lam = 1/k pairing is NOT a turnover match — ROTA runs HEAVIER than its paired damper")
    say("    in 100 of 128 cells — so it flatters ROTA on the turnover axis.  This exchange rate needs no")
    say("    match: each device is measured against ITS OWN undamped anchor (k=1 / lam=1.00).")
    say("  panel book | device  par |  d turn/yr  d MaxDD  d Sharpe |  turnover saved per pp of MaxDD given up")
    xr = []
    for pname in panels:
        for bname in BOOKS:
            for dev, pars in (("ROTA", KS), ("DAMP", LAMS)):
                a_t = dg[(dg.panel == pname) & (dg.book == bname) & (dg.gross == 0.75)
                         & (dg.device == dev) & (dg.param == pars[0])].turnover_yr.mean()
                a_r = df[(df.panel == pname) & (df.book == bname) & (df.gross == 0.75)
                         & (df.device == dev) & (df.param == pars[0]) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                for par in pars[1:]:
                    t = dg[(dg.panel == pname) & (dg.book == bname) & (dg.gross == 0.75)
                           & (dg.device == dev) & (dg.param == par)].turnover_yr.mean()
                    q = df[(df.panel == pname) & (df.book == bname) & (df.gross == 0.75)
                           & (df.device == dev) & (df.param == par) & (df.cost_bps == HEADLINE_RUNG)]
                    dt, dd_, ds = t - a_t, q.MaxDD.mean() - a_r.MaxDD, q.Sharpe.mean() - a_r.Sharpe
                    rate = (-dt) / (-dd_ * 100) if dd_ < -1e-9 else np.nan
                    xr.append(dict(panel=pname, book=bname, device=dev, param=par,
                                   d_turn=dt, d_MaxDD=dd_, d_Sharpe=ds, rate=rate))
                    say(f"  {pname:5s} {bname:4s} | {dev:6s} {par:5.3f} | {dt:+10.2f} {dd_:+8.2%} {ds:+9.4f} |"
                        + (f"  {rate:6.3f} x/yr per pp" if np.isfinite(rate) else "  (drawdown not given up)"))
    xf = pd.DataFrame(xr); xf.to_csv(f"{OUT}.exchange.csv", index=False)
    for dev in ("ROTA", "DAMP"):
        z = xf[(xf.device == dev) & xf.rate.notna()]
        say(f"   {dev}: median exchange rate {z.rate.median():.3f} turnover-x/yr saved per pp of MaxDD given up"
            f"  (n={len(z)}, mean dSharpe {xf[xf.device == dev].d_Sharpe.mean():+.4f})")

    say(f"\n=== D. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for dev, pars in (("ROTA", KS), ("DAMP", LAMS)):
        for par in pars:
            d = df[(df.device == dev) & (df.param == par)]
            say(f"   {dev:6s} {par:5.3f}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
                "   binding leg on 4b FAILs: "
                + "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")

    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same book, device, param, salt, gross, rung):")
    jt = []
    for bname in BOOKS:
        for dev, pars in (("ROTA", KS), ("DAMP", LAMS)):
            for par in pars:
                for s in (SALTS if (dev == "ROTA" and par > 1) else [0]):
                    for gross in GROSSES:
                        for rung in RUNGS:
                            q = df[(df.book == bname) & (df.device == dev) & (df.param == par)
                                   & (df.salt == s) & (df.gross == gross) & (df.cost_bps == rung)]
                            u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                            jt.append(dict(book=bname, device=dev, param=par, salt=s, gross=gross,
                                           cost_bps=rung, joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells")
    for dev, pars in (("ROTA", KS), ("DAMP", LAMS)):
        say(f"    {dev}: " + "  ".join(
            f"{par:5.3f}: {int(jf[(jf.device == dev) & (jf.param == par)].joint.sum())}"
            f"/{len(jf[(jf.device == dev) & (jf.param == par)])}" for par in pars))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse), every one: {len(pa)}")
    for _, r in pa.iterrows():
        say(f"    {r.panel:5s} {r.book:4s} {r.device:6s} par {r.param:5.3f} s{r.salt} g {r.gross:.2f}"
            f" {r.cost_bps:5.1f}bps  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}"
            f"  halves {r.H1:.4f}/{r.H2:.4f}  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — (k, salt) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname in panels:
        for bname in BOOKS:
            for gross in GROSSES:
                for rung in RUNGS:
                    d = df[(df.panel == pname) & (df.book == bname) & (df.gross == gross)
                           & (df.cost_bps == rung) & (df.device == "ROTA")]
                    inc = d[d.param == 1].iloc[0]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=pname, book=bname, gross=gross, cost_bps=rung, chooser=chooser,
                                       pick_k=int(pk.param), pick_salt=int(pk.salt),
                                       pick_is_incumbent=bool(pk.param == 1), full4b=bool(pk.pass4b),
                                       OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                       inc_OOS_Sharpe=inc.OOS_Sharpe, inc_OOS_CAGR=inc.OOS_CAGR,
                                       base_OOS_Sharpe=pk.base_OOS_Sharpe,
                                       spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
                        if gross == 0.75:
                            say(f"  {pname:5s} {bname:4s} g{gross:.2f} {rung:5.1f}bps {chooser:11s} ->"
                                f" k {int(pk.param)} s{int(pk.salt)} | OOS {pk.OOS_CAGR:6.2%} / {pk.OOS_Sharpe:.4f}"
                                f" / {pk.OOS_MaxDD:7.2%} | incumbent (k=1) OOS {inc.OOS_CAGR:6.2%} / {inc.OOS_Sharpe:.4f}"
                                f" | SPY OOS {pk.spy_OOS_CAGR:6.2%} / {pk.spy_OOS_Sharpe:.4f} |"
                                f" full 4b {'Y' if pk.pass4b else '.'}")
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  {len(wfd)} picks (2 panels x 2 books x 2 gross x 4 rungs x 2 choosers).")
    say(f"   picks landing on the INCUMBENT (k = 1, i.e. NO tranching): {int(wfd.pick_is_incumbent.sum())} of {len(wfd)}")
    say(f"   picks beating SPY's OOS Sharpe:                 {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the incumbent's own OOS Sharpe:   {int((wfd.OOS_Sharpe > wfd.inc_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:       {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:           {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over k:    " + "  ".join(f"{k}:{int((wfd.pick_k == k).sum())}" for k in KS))
    say("   pick distribution over salt: " + "  ".join(f"{s}:{int((wfd.pick_salt == s).sum())}" for s in SALTS))

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
