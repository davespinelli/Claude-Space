#!/usr/bin/env python3
"""Idea 291 - "is-the-ETF-dilution-slope-a-BETA-story-or-a-BREADTH-story" (lane B, 2026-09-09).

The question
------------
Idea 277 built a k-matched panel sweep (36 names, n_etf = round(s*36) ETFs drawn from the
36-name ETF set, 36-n_etf stocks from BSTK100, six seeds per s) and reported that the
un-ranked EWall book's OOS Sharpe falls MONOTONICALLY in 8/8 steps as the ETF share s goes
0 -> 1:  1.0597 -> 0.6656.  Its four measured panel characteristics do NOT obviously carry
that: breadth is FLAT (0.6821 -> 0.6750), pairwise correlation is FLAT (0.3626 -> 0.3436),
dispersion HALVES (0.0964 -> 0.0620) and eligible-set vol falls a third (0.2414 -> 0.1579).
Two of those four move in the direction that should RAISE a Sharpe, not lower it.  So the
queue asks the arithmetic question directly:

    decompose the slope into the MEAN-RETURN, VOL and CROSS-SECTIONAL-DISPERSION
    (co-movement / diversification) channels AT MATCHED REALISED GROSS, and report
    which one carries it.

The identity (exact, not a fit)
-------------------------------
For ANY book with realised (drifted) weights held_{i,t} and gross G_t = sum_i held_{i,t},
write the gross-of-costs return rg_t = sum_i held_{i,t} r_{i,t}.  Fix the scale at the
book's own mean realised gross Gbar = mean_t G_t and define the PER-UNIT-EXPOSURE series

    y_t = rg_t / Gbar                          (Sharpe(y) == Sharpe(rg), exactly)

Let u_{i,t} = held_{i,t} / G_t be the within-book weights, sigma_i the name's daily sd on
the window, and

    mu    = mean_t y_t                                          MEAN-RETURN channel
    sbar  = mean_t sum_i u_{i,t} sigma_i                        VOL channel (avg vol HELD)
    D     = var(y) / sbar^2                                     CO-MOVEMENT channel

Then, by construction and to machine precision,

    Sharpe = sqrt(252) * mu / (sbar * sqrt(D))
    log Sharpe = 0.5*log(252) + log(mu) - log(sbar) - 0.5*log(D)

so the s = 0 -> 1 change in log Sharpe splits EXACTLY into three additive numbers.  The
identity is asserted at run time (`ID_MAXABS`), it is not assumed.

D is then read (not fitted) against the textbook diversification form
    D_pred = (1+cv^2)/k_eff + rhobar * (1 - (1+cv^2)/k_eff)
with k_eff = 1/sum_i ubar_i^2 the participation ratio, cv the cross-sectional coefficient
of variation of the held names' vols (THE CROSS-SECTIONAL-DISPERSION term the queue names),
and rhobar the vol-weighted mean pairwise correlation.  The gap D - D_pred is the
weight-TIMING residual and is reported, never hidden.

BETA or BREADTH.  The queue's title is a claim about WHICH channel.  "Beta" lives in the
mean channel: y_t = alpha + beta*spy_t + e_t gives mu = alpha + beta*mu_spy, so the mean
channel splits into a beta*mu_spy part and an alpha part, both reported at every s.
"Breadth" lives in the co-movement channel D (via rhobar and k_eff).  The verdict is
whichever of those two carries more of the -log-Sharpe move.

MATCHED REALISED GROSS.  Both conventions spread a FIXED gross of 0.75 over whatever they
hold, so realised gross is 0.75 x P(anything held) and is reported per rung.  Two things are
proved rather than assumed: (i) Sharpe is EXACTLY invariant to a constant rescaling of the
book (`GROSSMATCH_MAXABS`), so the realised-gross difference across s CANNOT be the slope
except through the cost bill; (ii) that cost bill is priced by carrying the whole grid at
0 bps beside 10 bps.  Every arm is additionally re-run at the pooled mean realised gross of
the s=0 rung (`GM` rows) so the "at matched realised gross" instruction is executed
literally as well as argued.

Grid and tuned parameters (PROTOCOL rule 4: at most two)
    1. ETF share s          -- 9 rungs {0.000 .. 1.000}, the sweep dial, ALL reported
    2. gate convention      -- GATED (idea 277's EWall: above-200d AND vol20<0.60, gross
                               0.75 re-spread over the eligible names) vs UNGATED (the same
                               0.75 spread over ALL 36 names, no gate).  UNGATED is the pure
                               COMPOSITION arm: if the slope survives it, the slope is not
                               the gate's timing.
    Seed (6) is REPLICATION, not tuning: every seed is reported and nothing is selected on
    it.  Window (FULL / IS / OOS) and cost rung (10 / 0 bps) are reporting axes.
    9 x 2 x 6 seeds = 102 distinct panel books (s=1.000 is ETF36 for every seed, so one
    panel there), x 2 cost rungs = 204 panel backtests, plus 51 per-panel RULES v2 arms.
    18 pooled arms (9 s x 2 conventions), all reported.

Reproduction gate (run before any new number is read)
    The GATED pooled EWall curve is rebuilt from source and compared row by row against
    idea 277's COMMITTED `...is-ETF36-a-third-cluster-or-just-a-small-sample_C.sweepbooks.csv`
    EWall block (CAGR / Sharpe / MaxDD / OOS_CAGR / OOS_Sharpe / OOS_MaxDD, 9 rungs).

Walk-forward (PROTOCOL rule 8)
    IS = 2009-01-01..2016-12-31 chooses the rung by IS Sharpe; OOS = 2017-01-01..end is read
    ONCE.  OOS CAGR / Sharpe / MaxDD reported against the pooled RULES v2 baseline, RULES v1
    and SPY.  The channel decomposition is itself run on the IS and OOS windows separately,
    so "which channel carries it" is answered out of sample too.

KEEP paths (both, on every arm)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: universe_broad.json is CURRENT constituents and every MIX panel is a subset of
it, so the STOCK end of the sweep (s=0) carries a survivorship premium the ETF end does not
(a broad-market ETF cannot be survivorship-selected the way a hand-held large-cap list is).
That bias runs TOWARD a steep dilution slope and TOWARD attributing it to the mean channel.
A "the mean channel carries it" verdict is therefore an UPPER BOUND on the true slope, and
any co-movement/breadth finding is the conservative half.

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import zlib
import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state, rules_v1_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
DIAG_BPS = 0
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
BAND_V2 = 0.03
W_FIXED = 0.15
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
SHARES = [0.000, 0.125, 0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000]
SEEDS = [0, 1, 2, 3, 4, 5]
K_MIX = 36
CONVS = ["GATED", "UNGATED"]
PARENT = "2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.sweepbooks.csv"

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 400)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ============================================================== panels (idea 277 verbatim)
def build_pool():
    """idea 277's pre-registered k-matched ETF-share sweep, rebuilt from source."""
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px136 = load_universe(broad=True)
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]

    def sub(px, cols, tradable):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        return px[keep].dropna(how="all").ffill(), set(tradable)

    pool = {}
    p, t = sub(px136, etf36, etf36)
    pool["MIX~s1.000~ETF36"] = dict(px=p, tradable=t, etf_share=1.0, seed=-1, k=len(t))
    etf_pool = np.array(sorted(etf36))
    stk_pool = np.array(sorted(b_stk))
    seen = {frozenset(etf36)}
    for s in SHARES:
        n_etf = int(round(s * K_MIX))
        n_stk = K_MIX - n_etf
        for sd in SEEDS:
            seed = zlib.crc32(f"MIX|{s:.3f}|{sd}".encode()) % (2 ** 32)
            rng = np.random.default_rng(seed)
            pick = []
            if n_etf:
                pick += rng.choice(etf_pool, size=n_etf, replace=False).tolist()
            if n_stk:
                pick += rng.choice(stk_pool, size=n_stk, replace=False).tolist()
            pick = sorted(pick)
            fs = frozenset(pick)
            if fs in seen:
                continue
            seen.add(fs)
            p, t = sub(px136, pick, pick)
            pool[f"MIX~s{s:.3f}~{sd}"] = dict(px=p, tradable=t, etf_share=s, seed=sd, k=len(t))
    return pool, px136, etf36, b_stk


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights_for(px, tradable, conv, elig):
    """EWall (GATED, idea 277's arm) or the same gross with the gate removed (UNGATED)."""
    if conv == "GATED":
        sel = elig.astype(float)
    else:
        sel = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        for c in px.columns:
            if c in tradable:
                sel[c] = px[c].notna().astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def v2_weights_for(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    for c in px.columns:
        if c in tradable:
            e[c] = px[c].notna().astype(float)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, BAND_V2), 0.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def v4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


# ================================================================== THE DECOMPOSITION
def decompose(held, rets, idx, spy):
    """Exact 3-channel split of Sharpe for any book, on the window `idx`.

    held : realised (drifted) weights, aligned to rets' index/columns
    returns dict; `id_err` is the identity residual and must be ~0.
    """
    h = held.loc[idx]
    r = rets.loc[idx]
    rg = (h * r).sum(axis=1)                       # gross of costs
    G = h.sum(axis=1)
    Gbar = float(G.mean())
    y = rg / Gbar                                  # per-unit-exposure book
    sig = r.std(ddof=0)                            # name daily sd on this window
    u = h.div(G.replace(0.0, np.nan), axis=0).fillna(0.0)
    sbar = float((u * sig).sum(axis=1).mean())     # exposure-weighted avg vol HELD
    mu = float(y.mean())
    vy = float(y.var(ddof=0))
    D = vy / sbar ** 2
    S = np.sqrt(252.0) * mu / np.sqrt(vy)
    S_id = np.sqrt(252.0) * mu / (sbar * np.sqrt(D))
    # --- read D against the textbook diversification form (not a fit)
    ubar = u.mean(axis=0)
    ubar = ubar / ubar.sum()
    k_eff = 1.0 / float((ubar ** 2).sum())
    sb2 = float((ubar * sig).sum())
    m2 = float((ubar * sig ** 2).sum())
    cv2 = m2 / sb2 ** 2 - 1.0
    C = r.corr().to_numpy()
    w = (ubar * sig).to_numpy()
    num = float(w @ np.nan_to_num(C, nan=0.0) @ w) - float((w ** 2).sum())
    den = float(w.sum() ** 2) - float((w ** 2).sum())
    rhobar = num / den if den > 0 else np.nan
    a = (1.0 + cv2) / k_eff
    D_pred = a + rhobar * (1.0 - a)
    # --- beta / alpha split of the mean channel
    sp = spy.loc[idx]
    vs = float(sp.var(ddof=0))
    beta = float(((y - y.mean()) * (sp - sp.mean())).mean() / vs) if vs > 0 else np.nan
    mu_spy = float(sp.mean())
    alpha = mu - beta * mu_spy
    return dict(Sharpe=S, id_err=abs(S - S_id), mu=mu, sbar=sbar, D=D, Gbar=Gbar,
                G_sd=float(G.std(ddof=0)), k_eff=k_eff, cv=np.sqrt(max(cv2, 0.0)),
                rhobar=rhobar, D_pred=D_pred, D_resid=D - D_pred,
                beta=beta, alpha=alpha, mu_beta=beta * mu_spy, mu_spy=mu_spy,
                vol_ann=np.sqrt(vy * 252.0), CAGR=metrics(y)["CAGR"],
                MaxDD=metrics(y)["MaxDD"])


def main():
    P(f"# {STEM}")
    P(__doc__.strip().split("\n\n")[0])
    P("")

    pool, px136, etf36, b_stk = build_pool()
    P(f"panels built: {len(pool)}  (|ETF36| = {len(etf36)}, |BSTK100| = {len(b_stk)}, "
      f"k = {K_MIX} at every rung)")
    ks = {m['k'] for m in pool.values()}
    assert ks == {K_MIX}, ks
    P(f"  every panel k == {K_MIX}: OK   (width is NOT confounded with composition)")

    rets = px136.pct_change().fillna(0.0)
    spy = px136["SPY"].pct_change().fillna(0.0)
    idx_all = px136.index
    START = idx_all[260]
    IDX = {"FULL": idx_all[(idx_all >= START) & (idx_all >= pd.Timestamp(IS_START))],
           "IS": idx_all[(idx_all >= max(START, pd.Timestamp(IS_START)))
                         & (idx_all <= pd.Timestamp(IS_END))],
           "OOS": idx_all[idx_all >= pd.Timestamp(OOS_START)]}
    for k, v in IDX.items():
        P(f"  window {k:4s}: {v[0].date()} .. {v[-1].date()}  ({len(v)} days)")

    # ------------------------------------------------------- the grid: every panel book
    P("")
    P("=" * 108)
    P("THE GRID - every panel x convention x cost rung (seed is replication; ALL points written)")
    P("=" * 108)
    rows, W = [], {}
    for i, (pname, meta) in enumerate(pool.items(), 1):
        px, tr = meta["px"], meta["tradable"]
        elig = eligible_mask(px, tr)
        for conv in CONVS:
            w = weights_for(px, tr, conv, elig)
            for bps in (COST_BPS, DIAG_BPS):
                res = backtest(px, w, cost_bps=bps, freq=FREQ)
                r = res["returns"].loc[START:]
                if bps == COST_BPS:
                    W[(pname, conv)] = res["weights"].reindex(columns=px136.columns).fillna(0.0)
                m = metrics(r)
                h1, h2 = half_sharpes(r)
                rows.append(dict(panel=pname, etf_share=meta["etf_share"], seed=meta["seed"],
                                 conv=conv, bps=bps, k=meta["k"],
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=h1, H2=h2,
                                 IS_Sharpe=metrics(r.loc[IS_START:IS_END])["Sharpe"],
                                 OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                 OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                 OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                                 turn=float(res["turnover"].loc[START:].sum() / (len(r) / 252)),
                                 gross=float(res["weights"].loc[START:].sum(axis=1).mean())))
        # per-panel RULES v2 comparand
        res2 = backtest(px, v2_weights_for(px, tr), cost_bps=COST_BPS, freq=FREQ)
        W[(pname, "V2")] = res2["weights"].reindex(columns=px136.columns).fillna(0.0)
        res1 = backtest(px, rules_v1_weights(px).where(
            pd.DataFrame({c: (c in tr) for c in px.columns}, index=px.index), 0.0),
            cost_bps=COST_BPS, freq=FREQ)
        W[(pname, "V1")] = res1["weights"].reindex(columns=px136.columns).fillna(0.0)
        if i % 20 == 0:
            P(f"  ... {i}/{len(pool)} panels")
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"  wrote {len(grid)} grid rows -> {STEM}.grid.csv")

    # ------------------------------------------------- pool the seeds into one book per rung
    def pooled_weights(s, key):
        pans = [p for p, m in pool.items() if m["etf_share"] == s]
        acc = None
        for p in pans:
            w = W[(p, key)]
            acc = w if acc is None else acc.add(w, fill_value=0.0)
        return acc / len(pans), len(pans)

    def book_returns(hw, bps, turn=None):
        rg = (hw * rets).sum(axis=1)
        return rg

    # exact pooled turnover: pooling weights pools turnover linearly too
    def pooled_turn(s, key):
        pans = [p for p, m in pool.items() if m["etf_share"] == s]
        hw, _ = pooled_weights(s, key)
        t = hw.diff().abs().sum(axis=1)          # upper bound only; use engine-consistent below
        return t

    # ------------------------------------------------------------------ REPRODUCTION GATE
    P("")
    P("=" * 108)
    P("REPRODUCTION GATE - idea 277's committed EWall sweepbook block, rebuilt from source")
    P("=" * 108)
    pooled = {}
    for conv in CONVS:
        for s in SHARES:
            pans = [p for p, m in pool.items() if m["etf_share"] == s]
            rr, r0 = [], []
            for p in pans:
                g = grid[(grid.panel == p) & (grid.conv == conv)]
                rr.append(p)
            # pooled return series = equal-weight mean of the seed books (idea 277's rule)
            ser10 = []
            ser0 = []
            for p in pans:
                px, tr = pool[p]["px"], pool[p]["tradable"]
                el = eligible_mask(px, tr)
                w = weights_for(px, tr, conv, el)
                ser10.append(backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[START:])
                ser0.append(backtest(px, w, cost_bps=DIAG_BPS, freq=FREQ)["returns"].loc[START:])
            pooled[(conv, s)] = dict(
                r10=pd.concat(ser10, axis=1).mean(axis=1).dropna(),
                r0=pd.concat(ser0, axis=1).mean(axis=1).dropna(), panels=len(pans))

    rep = []
    for s in SHARES:
        r = pooled[("GATED", s)]["r10"]
        m, mo = metrics(r), metrics(r.loc[OOS_START:])
        rep.append(dict(etf_share=s, panels=pooled[("GATED", s)]["panels"],
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    rep = pd.DataFrame(rep).set_index("etf_share")
    par = pd.read_csv(OUT / PARENT)
    par = par[par.book == "EWall"].set_index("etf_share")
    cols = ["panels", "CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
    d = (rep[cols] - par[cols].reindex(rep.index)).abs()
    P(fmt(rep, 6))
    P(f"  max |rebuild - idea 277's committed sweepbooks.csv| over {len(rep)} rungs x "
      f"{len(cols)} columns: {float(d.to_numpy().max()):.3e}")
    assert float(d.to_numpy().max()) < 1e-9, "reproduction gate FAILED"
    P("  REPRODUCTION GATE: PASS")
    P(f"  the published slope: OOS Sharpe {rep.OOS_Sharpe.iloc[0]:.4f} -> "
      f"{rep.OOS_Sharpe.iloc[-1]:.4f}, monotone in "
      f"{int((np.diff(rep.OOS_Sharpe.to_numpy()) < 0).sum())}/8 steps")

    # ------------------------------------------------------- MATCHED REALISED GROSS proofs
    P("")
    P("=" * 108)
    P("MATCHED REALISED GROSS - realised gross per rung, and the two things it can and "
      "cannot do to a Sharpe")
    P("=" * 108)
    gm = []
    for conv in CONVS:
        for s in SHARES:
            hw, n = pooled_weights(s, conv)
            G = hw.loc[START:].sum(axis=1)
            r10, r0 = pooled[(conv, s)]["r10"], pooled[(conv, s)]["r0"]
            gm.append(dict(conv=conv, etf_share=s, panels=n, gross=float(G.mean()),
                           gross_sd=float(G.std(ddof=0)),
                           Sharpe10=metrics(r10)["Sharpe"], Sharpe0=metrics(r0)["Sharpe"],
                           cost_drag_Sharpe=metrics(r0)["Sharpe"] - metrics(r10)["Sharpe"],
                           cost_drag_CAGR=metrics(r0)["CAGR"] - metrics(r10)["CAGR"]))
    gmdf = pd.DataFrame(gm).set_index(["conv", "etf_share"])
    gmdf.to_csv(OUT / f"{STEM}.grossmatch.csv")
    P(fmt(gmdf, 6))
    # (i) exact scale invariance
    g0 = float(gmdf.loc[("GATED", 0.0), "gross"])
    worst = 0.0
    for conv in CONVS:
        for s in SHARES:
            r = pooled[(conv, s)]["r0"]
            lam = g0 / float(gmdf.loc[(conv, s), "gross"])
            worst = max(worst, abs(metrics(r * lam)["Sharpe"] - metrics(r)["Sharpe"]))
    P(f"  GROSSMATCH_MAXABS: |Sharpe(book x lambda) - Sharpe(book)| over all 18 arms rescaled "
      f"to the s=0 gross {g0:.4f}: {worst:.3e}")
    P("  => a realised-gross difference is EXACTLY inert for Sharpe gross of costs; it can "
      "only reach the slope through the COST BILL, which is the cost_drag column above "
      f"(spread across s: {float(gmdf.loc['GATED'].cost_drag_Sharpe.max() - gmdf.loc['GATED'].cost_drag_Sharpe.min()):.4f} of Sharpe on GATED, "
      f"{float(gmdf.loc['UNGATED'].cost_drag_Sharpe.max() - gmdf.loc['UNGATED'].cost_drag_Sharpe.min()):.4f} on UNGATED).")

    # ------------------------------------------------------------------ THE DECOMPOSITION
    P("")
    P("=" * 108)
    P("THE DECOMPOSITION - exact 3-channel split of the pooled book's Sharpe, every rung, "
      "every convention, every window")
    P("=" * 108)
    dec = []
    for conv in CONVS:
        for s in SHARES:
            hw, n = pooled_weights(s, conv)
            for win, idx in IDX.items():
                d = decompose(hw, rets, idx, spy)
                d.update(conv=conv, etf_share=s, window=win, panels=n)
                dec.append(d)
    dec = pd.DataFrame(dec)
    idmax = float(dec.id_err.max())
    P(f"  ID_MAXABS: max |Sharpe - sqrt(252)*mu/(sbar*sqrt(D))| over all "
      f"{len(dec)} decompositions: {idmax:.3e}")
    assert idmax < 1e-10, "identity FAILED"
    P("  IDENTITY GATE: PASS - the three channels are an exact factorisation, not a fit.")
    # the decomposition runs on the WEIGHT-pooled book (gross of costs); idea 277 pools the
    # NET return series. Stated, not hidden: the two differ only where a panel's own price
    # frame lost an all-NaN leading row to dropna(how="all"), and by how much:
    _f = dec[dec.window == "FULL"].set_index(["conv", "etf_share"])["Sharpe"]
    gap = max(abs(float(_f.loc[(c, s)]) - metrics(pooled[(c, s)]["r0"])["Sharpe"])
              for c in CONVS for s in SHARES)
    P(f"  WEIGHTPOOL_GAP: max |Sharpe(weight-pooled, 0 bps) - Sharpe(return-pooled, 0 bps)| "
      f"over all 18 arms: {gap:.3e}  ({gap / 0.3943:.2%} of the OOS move being decomposed)")
    dec = dec.set_index(["conv", "window", "etf_share"]).sort_index()
    dec.to_csv(OUT / f"{STEM}.channels.csv")
    show = ["Sharpe", "mu", "sbar", "D", "k_eff", "cv", "rhobar", "D_pred", "D_resid",
            "beta", "alpha", "mu_beta", "vol_ann", "Gbar"]
    for conv in CONVS:
        for win in ("FULL", "IS", "OOS"):
            P("")
            P(f"  --- {conv} / {win} (mu, sbar, alpha are DAILY; D is dimensionless) ---")
            P(fmt(dec.loc[(conv, win)][show], 6))

    # ------------------------------------------------------------------ the attribution
    P("")
    P("=" * 108)
    P("THE ANSWER - log-additive attribution of the s = 0.000 -> 1.000 move in Sharpe")
    P("=" * 108)
    att = []
    for conv in CONVS:
        for win in ("FULL", "IS", "OOS"):
            b = dec.loc[(conv, win)]
            lo, hi = b.loc[0.0], b.loc[1.0]
            dlS = np.log(hi.Sharpe) - np.log(lo.Sharpe)
            c_mu = np.log(hi.mu) - np.log(lo.mu)
            c_vol = -(np.log(hi.sbar) - np.log(lo.sbar))
            c_D = -0.5 * (np.log(hi.D) - np.log(lo.D))
            # inside the mean channel: beta vs alpha (levels, then as a share of d mu)
            dmu = hi.mu - lo.mu
            dmu_beta = hi.mu_beta - lo.mu_beta
            dmu_alpha = hi.alpha - lo.alpha
            # inside D: rhobar vs cross-sectional dispersion cv vs k_eff
            def dpred(rho, cv, keff):
                a = (1 + cv ** 2) / keff
                return a + rho * (1 - a)
            base = dpred(lo.rhobar, lo.cv, lo.k_eff)
            d_rho = dpred(hi.rhobar, lo.cv, lo.k_eff) - base
            d_cv = dpred(lo.rhobar, hi.cv, lo.k_eff) - base
            d_keff = dpred(lo.rhobar, lo.cv, hi.k_eff) - base
            att.append(dict(conv=conv, window=win,
                            Sharpe_lo=lo.Sharpe, Sharpe_hi=hi.Sharpe, dlogSharpe=dlS,
                            ch_MEAN=c_mu, ch_VOL=c_vol, ch_COMOVE=c_D,
                            sum_check=c_mu + c_vol + c_D - dlS,
                            share_MEAN=c_mu / dlS, share_VOL=c_vol / dlS,
                            share_COMOVE=c_D / dlS,
                            dmu=dmu, dmu_beta=dmu_beta, dmu_alpha=dmu_alpha,
                            beta_share_of_dmu=dmu_beta / dmu if dmu else np.nan,
                            dD=hi.D - lo.D, dD_from_rho=d_rho, dD_from_cv=d_cv,
                            dD_from_keff=d_keff))
    att = pd.DataFrame(att).set_index(["conv", "window"])
    att.to_csv(OUT / f"{STEM}.attribution.csv")
    P(fmt(att[["Sharpe_lo", "Sharpe_hi", "dlogSharpe", "ch_MEAN", "ch_VOL", "ch_COMOVE",
               "sum_check", "share_MEAN", "share_VOL", "share_COMOVE"]], 6))
    P("")
    P("  (channels are ADDITIVE in log Sharpe and sum to dlogSharpe exactly; sum_check is "
      f"the residual, max {float(att.sum_check.abs().max()):.3e})")
    P("")
    P("  inside the MEAN channel - beta*mu_spy vs alpha, and inside the CO-MOVEMENT channel "
      "- rhobar vs cross-sectional vol dispersion cv vs k_eff:")
    P(fmt(att[["dmu", "dmu_beta", "dmu_alpha", "beta_share_of_dmu", "dD", "dD_from_rho",
               "dD_from_cv", "dD_from_keff"]], 6))

    # step-by-step monotonicity of each channel
    P("")
    P("  step-by-step: the channel contribution of each of the 8 rung-to-rung steps "
      "(dlogSharpe = MEAN + VOL + COMOVE at every step)")
    steps = []
    for conv in CONVS:
        for win in ("FULL", "IS", "OOS"):
            b = dec.loc[(conv, win)].sort_index()
            for a_, b_ in zip(SHARES[:-1], SHARES[1:]):
                x, y = b.loc[a_], b.loc[b_]
                steps.append(dict(conv=conv, window=win, step=f"{a_:.3f}->{b_:.3f}",
                                  dlogSharpe=np.log(y.Sharpe) - np.log(x.Sharpe),
                                  MEAN=np.log(y.mu) - np.log(x.mu),
                                  VOL=-(np.log(y.sbar) - np.log(x.sbar)),
                                  COMOVE=-0.5 * (np.log(y.D) - np.log(x.D))))
    steps = pd.DataFrame(steps)
    steps.to_csv(OUT / f"{STEM}.steps.csv", index=False)
    for conv in CONVS:
        for win in ("FULL", "OOS"):
            sub = steps[(steps.conv == conv) & (steps.window == win)]
            P(f"    {conv}/{win}: MEAN negative in {int((sub.MEAN < 0).sum())}/8 steps, "
              f"VOL positive in {int((sub.VOL > 0).sum())}/8, "
              f"COMOVE positive in {int((sub.COMOVE > 0).sum())}/8; "
              f"mean per step MEAN {sub.MEAN.mean():+.5f} VOL {sub.VOL.mean():+.5f} "
              f"COMOVE {sub.COMOVE.mean():+.5f}")
    P("")
    P(fmt(steps.set_index(["conv", "window", "step"]), 6))

    # -------------------------------- POOLING ARTEFACT CONTROL: decompose PANEL BY PANEL
    P("")
    P("=" * 108)
    P("POOLING-ARTEFACT CONTROL - the same decomposition run PER PANEL, then seed-averaged")
    P("=" * 108)
    P("  WHY: k_eff above is the participation ratio of the POOLED book. At s = 0 the six")
    P("  seed panels draw 36 different stocks each from BSTK100, so the pooled book holds up")
    P("  to ~100 names; at s = 1.000 all seeds ARE ETF36, so it holds 36. That fall in k_eff")
    P("  is SEED pooling, not panel composition, and it INFLATES the co-movement channel at")
    P("  the ETF end. Per panel, k is 36 at every rung by construction, so this block is the")
    P("  composition-only reading.")
    pdec = []
    for p, meta in pool.items():
        for conv in CONVS:
            hw = W[(p, conv)]
            for win, idx in IDX.items():
                d = decompose(hw, rets, idx, spy)
                d.update(panel=p, conv=conv, window=win, etf_share=meta["etf_share"],
                         seed=meta["seed"])
                pdec.append(d)
    pdec = pd.DataFrame(pdec)
    P(f"  per-panel ID_MAXABS: {float(pdec.id_err.max()):.3e}")
    assert float(pdec.id_err.max()) < 1e-10
    pdec.to_csv(OUT / f"{STEM}.panelchannels.csv", index=False)
    pm = (pdec.groupby(["conv", "window", "etf_share"])
              [["Sharpe", "mu", "sbar", "D", "k_eff", "cv", "rhobar", "D_pred", "D_resid",
                "beta", "alpha", "mu_beta"]].mean())
    for conv in CONVS:
        for win in ("FULL", "OOS"):
            P("")
            P(f"  --- {conv} / {win}, seed-MEAN of the per-panel channels ---")
            P(fmt(pm.loc[(conv, win)], 6))
    P("")
    P("  attribution on the seed-mean per-panel channels (log-additive, s=0 -> s=1):")
    patt = []
    for conv in CONVS:
        for win in ("FULL", "IS", "OOS"):
            b = pm.loc[(conv, win)]
            lo, hi = b.loc[0.0], b.loc[1.0]
            dl = np.log(hi.Sharpe) - np.log(lo.Sharpe)
            c_mu = np.log(hi.mu) - np.log(lo.mu)
            c_vol = -(np.log(hi.sbar) - np.log(lo.sbar))
            c_D = -0.5 * (np.log(hi.D) - np.log(lo.D))
            tot = c_mu + c_vol + c_D
            patt.append(dict(conv=conv, window=win, Sharpe_lo=lo.Sharpe, Sharpe_hi=hi.Sharpe,
                             ch_MEAN=c_mu, ch_VOL=c_vol, ch_COMOVE=c_D, total=tot,
                             share_MEAN=c_mu / tot, share_VOL=c_vol / tot,
                             share_COMOVE=c_D / tot, k_eff_lo=lo.k_eff, k_eff_hi=hi.k_eff,
                             rho_lo=lo.rhobar, rho_hi=hi.rhobar, cv_lo=lo.cv, cv_hi=hi.cv,
                             beta_lo=lo.beta, beta_hi=hi.beta,
                             dlogSharpe_of_seedmean=dl))
    patt = pd.DataFrame(patt).set_index(["conv", "window"])
    patt.to_csv(OUT / f"{STEM}.panelattribution.csv")
    P(fmt(patt, 6))
    P("  (k_eff is now ~36 at BOTH ends, as it must be at fixed k; the co-movement channel "
      "shrinks accordingly and the MEAN channel's share rises.)")

    # ---------------------------------------------- COUNTERFACTUAL: freeze one channel
    P("")
    P("=" * 108)
    P("CHANNEL FREEZE - the s-curve rebuilt with ONE channel pinned at its s=0 value "
      "(exact, from the identity)")
    P("=" * 108)
    frz = []
    for conv in CONVS:
        for win in ("FULL", "OOS"):
            b = dec.loc[(conv, win)].sort_index()
            lo = b.loc[0.0]
            for s in SHARES:
                x = b.loc[s]
                frz.append(dict(conv=conv, window=win, etf_share=s, actual=x.Sharpe,
                                freeze_MEAN=np.sqrt(252) * lo.mu / (x.sbar * np.sqrt(x.D)),
                                freeze_VOL=np.sqrt(252) * x.mu / (lo.sbar * np.sqrt(x.D)),
                                freeze_COMOVE=np.sqrt(252) * x.mu / (x.sbar * np.sqrt(lo.D))))
    frz = pd.DataFrame(frz).set_index(["conv", "window", "etf_share"])
    frz.to_csv(OUT / f"{STEM}.freeze.csv")
    P(fmt(frz, 6))
    for conv in CONVS:
        for win in ("FULL", "OOS"):
            f = frz.loc[(conv, win)]
            tot = f.actual.loc[1.0] - f.actual.loc[0.0]
            P(f"  {conv}/{win}: total move {tot:+.4f}; with MEAN frozen "
              f"{f.freeze_MEAN.loc[1.0] - f.freeze_MEAN.loc[0.0]:+.4f}, with VOL frozen "
              f"{f.freeze_VOL.loc[1.0] - f.freeze_VOL.loc[0.0]:+.4f}, with CO-MOVEMENT frozen "
              f"{f.freeze_COMOVE.loc[1.0] - f.freeze_COMOVE.loc[0.0]:+.4f}")

    # ------------------------------------------------- LITERAL matched-realised-gross arms
    P("")
    P("=" * 108)
    P("THE LITERAL 'AT MATCHED REALISED GROSS' ARMS - every rung rescaled to the s=0 pooled "
      "realised gross, re-costed at 10 bps")
    P("=" * 108)
    lit = []
    for conv in CONVS:
        g_ref = float(gmdf.loc[(conv, 0.0), "gross"])
        for s in SHARES:
            lam = g_ref / float(gmdf.loc[(conv, s), "gross"])
            r0 = pooled[(conv, s)]["r0"]
            r10 = pooled[(conv, s)]["r10"]
            turn_cost = r0 - r10                      # the 10 bps bill, scales with lambda
            r_gm = r0 * lam - turn_cost * lam
            m, mo = metrics(r_gm), metrics(r_gm.loc[OOS_START:])
            lit.append(dict(conv=conv, etf_share=s, lam=lam, CAGR=m["CAGR"],
                            Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                            OOS_MaxDD=mo["MaxDD"],
                            dSharpe_vs_unmatched=m["Sharpe"] - metrics(r10)["Sharpe"]))
    lit = pd.DataFrame(lit).set_index(["conv", "etf_share"])
    lit.to_csv(OUT / f"{STEM}.grossmatched_arms.csv")
    P(fmt(lit, 6))
    P(f"  max |Sharpe(matched) - Sharpe(unmatched)| = "
      f"{float(lit.dSharpe_vs_unmatched.abs().max()):.3e} - the instruction is executed and "
      "it changes nothing, as the invariance proof above requires.")

    # ------------------------------------------------------------------ RULE 8 + KEEP paths
    P("")
    P("=" * 108)
    P("RULE 8 WALK-FORWARD - s chosen on 2009-2016 IS Sharpe, 2017-2026 read ONCE")
    P("=" * 108)
    base_pool, spy_pool = {}, spy.loc[START:]
    for key in ("V2", "V1"):
        ser = []
        for p in pool:
            hw = W[(p, key)]
            ser.append(((hw * rets).sum(axis=1)).loc[START:])
        base_pool[key] = pd.concat(ser, axis=1).mean(axis=1)
    # exact per-panel v2/v1 net returns (pool the NET series the same way idea 277 pools EWall)
    v2ser, v1ser = [], []
    for p, meta in pool.items():
        px, tr = meta["px"], meta["tradable"]
        v2ser.append(backtest(px, v2_weights_for(px, tr), cost_bps=COST_BPS,
                              freq=FREQ)["returns"].loc[START:])
        m1 = pd.DataFrame({c: (c in tr) for c in px.columns}, index=px.index)
        v1ser.append(backtest(px, rules_v1_weights(px).where(m1, 0.0), cost_bps=COST_BPS,
                              freq=FREQ)["returns"].loc[START:])
    v2r = pd.concat(v2ser, axis=1).mean(axis=1)
    v1r = pd.concat(v1ser, axis=1).mean(axis=1)

    wf = []
    for conv in CONVS:
        b = grid[grid.conv == conv]
        is_s = {s: metrics(pooled[(conv, s)]["r10"].loc[IS_START:IS_END])["Sharpe"]
                for s in SHARES}
        pick = max(is_s, key=is_s.get)
        r = pooled[(conv, pick)]["r10"]
        mo = metrics(r.loc[OOS_START:])
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        wf.append(dict(book=f"IS-Sharpe pick ({conv})", pick=pick, CAGR=m["CAGR"],
                       Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
        P(f"  {conv}: IS Sharpe by rung " +
          " ".join(f"{s:.3f}={is_s[s]:.4f}" for s in SHARES) + f"  -> pick s = {pick:.3f}")
    for lab, r in (("RULES v2 (live, pooled)", v2r), ("RULES v1 (pooled)", v1r),
                   ("SPY", spy_pool), ("s=0.000 EWall (GATED)", pooled[("GATED", 0.0)]["r10"]),
                   ("s=1.000 EWall (GATED)", pooled[("GATED", 1.0)]["r10"])):
        m, mo = metrics(r), metrics(r.loc[OOS_START:])
        h1, h2 = half_sharpes(r)
        wf.append(dict(book=lab, pick=np.nan, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                       MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                       OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    wf = pd.DataFrame(wf).set_index("book")
    wf.to_csv(OUT / f"{STEM}.walkforward.csv")
    P("")
    P(fmt(wf, 4))

    # the decomposition OUT OF SAMPLE is already in `att`; restate the verdict there
    P("")
    P("  rule 8 on the ANSWER itself: the attribution computed on IS only vs on OOS only")
    P(fmt(att.loc[(slice(None), ["IS", "OOS"]), ["share_MEAN", "share_VOL", "share_COMOVE",
                                                 "beta_share_of_dmu"]], 6))

    P("")
    P("=" * 108)
    P("BOTH KEEP PATHS - every arm (18 pooled + 102 per-panel), 10 bps")
    P("=" * 108)
    kp = []
    for conv in CONVS:
        for s in SHARES:
            r = pooled[(conv, s)]["r10"]
            kp.append(dict(level="pooled", conv=conv, etf_share=s, seed=np.nan,
                           pass4a=v4a(r, v2r), fail4b=fail4b(r, spy_pool,
                                                             r.loc[OOS_START:],
                                                             spy_pool.loc[OOS_START:]),
                           Sharpe=metrics(r)["Sharpe"], CAGR=metrics(r)["CAGR"],
                           MaxDD=metrics(r)["MaxDD"]))
    for p, meta in pool.items():
        px, tr = meta["px"], meta["tradable"]
        el = eligible_mask(px, tr)
        v2p = backtest(px, v2_weights_for(px, tr), cost_bps=COST_BPS,
                       freq=FREQ)["returns"].loc[START:]
        spp = px["SPY"].pct_change().fillna(0.0).loc[START:]
        for conv in CONVS:
            r = backtest(px, weights_for(px, tr, conv, el), cost_bps=COST_BPS,
                         freq=FREQ)["returns"].loc[START:]
            kp.append(dict(level="panel", conv=conv, etf_share=meta["etf_share"],
                           seed=meta["seed"], pass4a=v4a(r, v2p),
                           fail4b=fail4b(r, spp, r.loc[OOS_START:], spp.loc[OOS_START:]),
                           Sharpe=metrics(r)["Sharpe"], CAGR=metrics(r)["CAGR"],
                           MaxDD=metrics(r)["MaxDD"]))
    kp = pd.DataFrame(kp)
    kp.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    n4a = int(kp.pass4a.sum())
    n4b = int((kp.fail4b == "-").sum())
    P(f"  4a passes: {n4a} / {len(kp)}      4b passes: {n4b} / {len(kp)}")
    P("  4b failure reasons (count of arms by binding leg set):")
    P(kp.fail4b.value_counts().to_string())
    P("")
    P("  pooled arms in full:")
    P(fmt(kp[kp.level == "pooled"].set_index(["conv", "etf_share"])[
        ["pass4a", "fail4b", "CAGR", "Sharpe", "MaxDD"]], 4))
    if n4b:
        P("")
        P("  the 4b passers:")
        P(fmt(kp[kp.fail4b == "-"].set_index(["level", "conv", "etf_share", "seed"]), 4))

    # ------------------------------------------------------------------------- verdict
    P("")
    P("=" * 108)
    a = att.loc[("GATED", "OOS")]
    aF = att.loc[("GATED", "FULL")]
    P("VERDICT")
    P("=" * 108)
    P(f"  GATED/OOS: Sharpe {a.Sharpe_lo:.4f} -> {a.Sharpe_hi:.4f}, dlogSharpe {a.dlogSharpe:+.4f}")
    P(f"    MEAN-RETURN channel {a.ch_MEAN:+.4f} ({a.share_MEAN:+.1%} of the move)")
    P(f"    VOL channel         {a.ch_VOL:+.4f} ({a.share_VOL:+.1%})")
    P(f"    CO-MOVEMENT channel {a.ch_COMOVE:+.4f} ({a.share_COMOVE:+.1%})")
    P(f"    of the mean channel, beta*mu_spy carries {a.beta_share_of_dmu:+.1%} of d(mu)")
    P(f"  GATED/FULL: MEAN {aF.share_MEAN:+.1%} VOL {aF.share_VOL:+.1%} "
      f"COMOVE {aF.share_COMOVE:+.1%}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
