#!/usr/bin/env python3
"""QUEUE idea 203 — A TURNOVER-MATCHED NULL FOR SUPPRESSING OVERLAYS  (cloud, 2026-09-08).

QUESTION (verbatim, QUEUE.md idea 203)
    "idea 191 measured the rotation null's turnover fidelity on BUDGET-skip at 1782.7% mean on a
     widened threshold grid (idea 186 published 25.4%/213.8%), i.e. the null is not turnover-matched
     for an overlay that suppresses a trade and degrades without bound in on-share.  Build and
     validate a null that resamples SKIP DECISIONS at matched count rather than rotating the state,
     and re-price idea 186's BUDGET family against it.  Max 2 params."

THE OBSTRUCTION THE QUEUE DID NOT NOTICE, STATED BEFORE ANY NUMBER IS READ
    BUDGET's ON indicator is not an arbitrary state series.  It is

        s_j = 1{ tt_j > tau },    tt_j = the turnover the base book would trade at rebalance j,

    a THRESHOLD ON THE VERY QUANTITY THE NULL IS BEING ASKED TO MATCH.  So the ON set is exactly
    the top-K rebalance dates ranked by tt, K = sum(s).  It follows immediately that

        the only matched-count draw whose skipped turnover equals the real overlay's
        IS THE REAL OVERLAY.

    A matched-count null with exact turnover fidelity is therefore DEGENERATE for this family: it
    has one element and zero entropy.  Turnover fidelity and independence-from-the-real-overlay are
    not two properties to be optimised — they are THE SAME DIAL read from two ends.  Idea 203 asks
    for a null that has both.  It cannot exist, and this run proves it constructively by building
    the dial and reading both ends of it.

    That is a real answer, not a dodge: the useful object is not "the turnover-matched null" but the
    FIDELITY-ENTROPY FRONTIER, and a published overlay result should quote where on it the null sits.

THE NULLS (p2, all reported)
    ROT      idea 186's incumbent: circular rotation of s by a random offset.  Preserves on-count
             and CIRCULAR switch count exactly; preserves NOTHING about turnover.
    MC       matched count, uniform: draw K of the J rebalance dates at random.  Preserves on-count
             exactly; destroys clustering; preserves nothing about turnover.  (This is the null the
             queue literally asks for.)
    RUN      matched count AND matched clustering: permute the run-length decomposition of s (the
             ON-run lengths and OFF-gap lengths are kept as multisets and re-ordered at random).
             Preserves on-count and circular switch count exactly, like ROT, without ROT's rigid
             one-offset-one-draw structure.
    STRAT(f) THE FRONTIER, p1.  Draw K dates at random from the TOP-M rebalance dates ranked by
             tt, M = ceil(K/f).  f = 1.0 -> M = K -> the draw IS the real overlay (fidelity perfect,
             entropy zero).  f = K/J -> M = J -> exactly MC.  Everything between is the frontier.

PARAMETERS (2, swept, ALL grid points reported)
    p1  f     in {1.00, 0.75, 0.50, 0.25}   the STRAT concentration
    p2  null  in {ROT, MC, RUN, STRAT}      the null family
    tau and mode are the overlay family's ARMS, not tuned: the full idea-186 grid
    tau {0.10, 0.20, 0.30} is carried plus idea 191's widened points {0.05, 0.50}, and both
    modes {skip, half}, every cell reported.

WHAT IS MEASURED, PER (panel x tau x mode x null x draw)
    FIDELITY   |TO_null - TO_real| / TO_real on realised annualised turnover  (idea 186's own
               definition, so its 25.4% / 213.8% is reproducible here as gate G3)
    ENTROPY    overlap = |S_null ^ S_real| / K.  A null at overlap 1.0 is the overlay itself.
    STRUCTURE  on-count fidelity (exact for all four by construction) and circular switch-count
               fidelity (exact for ROT and RUN, broken by MC and STRAT)
    PRICE      dSharpe = Sharpe(overlaid) - Sharpe(base), real vs the null band, and whether the
               real overlay clears the null's 95th percentile — idea 186's clause, re-priced.

RULE 8 (required)
    The null (family and f) is chosen on 2010-2016 by IS turnover fidelity alone — never by any
    performance number — and 2017-2026 is read ONCE with that choice.  Reported: OOS clause clear
    rate under the chosen null vs under the incumbent ROT, and OOS CAGR / Sharpe / MaxDD of the
    real BUDGET books against RULES v2 (live), RULES v1 and SPY.

BOTH KEEP PATHS (4a vs the live book, 4b vs SPY) are scored on every real BUDGET book, full sample
and OOS.  Idea 203 is a methods idea and nominates nothing; PROTOCOL rule 4 requires the paths be
scored, so they are.

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are current-constituent lists; SMALL439 contains no
      delistings at all.  Real and null draws inherit it identically, so the null COMPARISON is
      unaffected; the LEVEL of every number is not.
    * SMALL439 drops the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv first.
    * Seeds are derived from a stable md5 of the cell key, not Python's randomised hash(), so
      two runs of this file agree bit for bit.
    * 20 draws per cell gives the clause a nominal one-sided size of 1/21 = 4.8%, approximate.
    * Idea 126 (t+1 only) and idea 38 (calendar-day index) carry.

Outputs: .console.txt .grid.csv .fidelity.csv .frontier.csv .walkforward.csv .keep.csv .result.md
Deterministic; no network.
"""
import sys, time, math, hashlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = "2026-09-08_a-turnover-matched-null-for-suppressing-overlays_cloud"
OUT = Path(__file__).resolve().parent

FREQ = "W"
BASE_N, BASE_GROSS, MAX_VOL = 20, 0.75, 0.60
COST_RUNGS = [10, 25]
TAUS = [0.05, 0.10, 0.20, 0.30, 0.50]        # idea 186's 3 + idea 191's widened 2
MODES = ["skip", "half"]
PHIS = [1.00, 0.75, 0.50, 0.25]              # p1
NULLS = ["ROT", "MC", "RUN", "STRAT"]        # p2
N_NULL = 20
SEED = 203_000
IS_END, OOS_START = "2016-12-31", "2017-01-01"

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ---------------------------------------------------------------- fast backtest (idea 186's, gated)
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ, mask=None):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values if mask is None else np.asarray(mask, bool)
    m = np.concatenate([[False], m[:-1]])
    m = m.copy(); m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


def net(res, bps):
    return res["returns"] - res["turnover"] * bps / 1e4


def cell_seed(*key):
    """A STABLE per-cell seed.  Python's built-in hash() is randomised per process
    (PYTHONHASHSEED), so seeding an RNG with it makes a script non-reproducible across runs —
    PROTOCOL rule 5 requires deterministic.  md5 of the key's repr is stable everywhere."""
    d = hashlib.md5(repr(key).encode()).digest()
    return SEED + int.from_bytes(d[:4], "big") % 100_000


def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Panel:
    def __init__(self, name, px, tradable):
        self.name, self.px = name, px
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        elig = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
        drop = [c for c in px.columns if c not in set(tradable)]
        if drop: elig[drop] = False
        rank = comp_score(px).where(elig).rank(axis=1, ascending=False)
        self.W = (rank <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)
        self.start = px.index[260]
        self.mask = rebalance_mask(px.index, FREQ).values
        self.reb = np.flatnonzero(self.mask)
        self.spy = px["SPY"].pct_change().fillna(0.0)
        # tt_j: the turnover the base book WOULD trade at each rebalance date (the BUDGET statistic)
        w = self.W.values[self.reb]
        prev = np.vstack([np.zeros((1, w.shape[1])), w[:-1]])
        self.tt = np.abs(w - prev).sum(axis=1)


def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL: {len([c for c in pxs.columns if c!='SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} tradable")
    pxs = pxs[s_stk + ["SPY"]]
    return [Panel("U56", px56, {c for c in px56.columns if c != "SPY"}),
            Panel("BROAD136", px136, {c for c in px136.columns if c != "SPY"}),
            Panel("SMALL439", pxs, set(s_stk))]


# ---------------------------------------------------------------- the overlay
def budget_on(pan, tau):
    """BUDGET's ON indicator over the rebalance dates: fire when the required turnover exceeds tau."""
    return pan.tt > tau


def apply_budget(pan, mode, s_reb):
    """Apply the BUDGET action on the ON rebalance dates.  Returns (weights, mask)."""
    idx = pan.px.index
    mask = pan.mask.copy()
    W = pan.W
    if mode == "skip":
        mask = mask & ~np.isin(np.arange(len(idx)), pan.reb[s_reb])
    else:                                    # 'half': move half way to the target
        w = pan.W.values.copy()
        wr = w[pan.reb]
        for j in np.flatnonzero(s_reb):
            prev = wr[j - 1] if j > 0 else np.zeros(wr.shape[1])
            wr[j] = 0.5 * wr[j] + 0.5 * prev
        w[pan.reb] = wr
        W = pd.DataFrame(w, index=idx, columns=pan.W.columns)
    return W, mask


# ---------------------------------------------------------------- the four nulls
def circ_switches(s):
    s = np.asarray(s)
    return int((s != np.roll(s, 1)).sum())


def draw_null(kind, s_real, tt, rng, phi=None):
    """One null draw of the ON indicator, matched to s_real in the way `kind` specifies."""
    J = len(s_real); K = int(s_real.sum())
    out = np.zeros(J, bool)
    if K == 0 or K == J:
        return s_real.copy()
    if kind == "ROT":
        return np.roll(s_real, int(rng.integers(1, J)))
    if kind == "MC":
        out[rng.choice(J, size=K, replace=False)] = True
        return out
    if kind == "RUN":
        # run-length decomposition of the circular state, re-ordered at random
        s = np.asarray(s_real)
        edges = np.flatnonzero(s != np.roll(s, 1))
        if len(edges) == 0:
            return s.copy()
        r = np.roll(s, -edges[0])                      # start at a transition
        runs, vals, i = [], [], 0
        while i < J:
            j = i
            while j < J and r[j] == r[i]: j += 1
            runs.append(j - i); vals.append(bool(r[i])); i = j
        on_runs = [runs[i] for i in range(len(runs)) if vals[i]]
        off_runs = [runs[i] for i in range(len(runs)) if not vals[i]]
        rng.shuffle(on_runs); rng.shuffle(off_runs)
        seq = []
        for a, b in zip(on_runs, off_runs + [0] * len(on_runs)):
            seq += [True] * a + [False] * b
        # any leftover OFF runs (unequal counts) go at the end
        for b in off_runs[len(on_runs):]:
            seq += [False] * b
        seq = np.array(seq[:J], bool)
        if len(seq) < J:
            seq = np.concatenate([seq, np.zeros(J - len(seq), bool)])
        return np.roll(seq, int(rng.integers(0, J)))
    if kind == "STRAT":
        M = min(J, int(math.ceil(K / max(phi, 1e-9))))
        pool = np.argsort(-np.asarray(tt))[:M]         # the top-M dates by required turnover
        out[rng.choice(pool, size=K, replace=False)] = True
        return out
    raise ValueError(kind)


# ---------------------------------------------------------------- metrics helpers
def sh(r): return metrics(r)["Sharpe"] if len(r) > 5 else np.nan
def halves(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])
def ann_turn(t, idx):
    return float(t.sum() / (len(idx) / 252.0))


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 120)
    P("IDEA 203 — A TURNOVER-MATCHED NULL FOR SUPPRESSING OVERLAYS")
    P("  p1 f in " + str(PHIS) + ";  p2 null in " + str(NULLS) + ".  All grid points reported.")
    P("  arms (not tuned): tau in " + str(TAUS) + " x mode in " + str(MODES) + " x 3 panels x 2 rungs")
    P("  PRE-REGISTERED OBSTRUCTION: BUDGET's ON set is the top-K rebalance dates by required")
    P("  turnover, so the ONLY exactly turnover-matched matched-count draw is the overlay itself.")
    P("  Fidelity and entropy are one dial; this run builds it and reads both ends.")
    P("=" * 120)

    P("\nPANELS")
    pans = build_panels()
    for pan in pans:
        P(f"  {pan.name:9s} {pan.px.shape[1]-1:4d} tradables, {len(pan.px):5d} days, "
          f"{len(pan.reb):4d} rebalance dates, required-turnover tt mean {pan.tt.mean():.4f} "
          f"max {pan.tt.max():.4f}")

    # ------------------------------------------------------------------ gates
    P("\n" + "=" * 120)
    P("GATES")
    P("=" * 120)
    pan = pans[0]
    eng = backtest(pan.px, pan.W, cost_bps=0.0, freq=FREQ)["returns"]
    fst = fast_backtest(pan.px, pan.W, 0.0, FREQ)["returns"]
    e1 = float(np.abs(eng - fst).max())
    P(f"  G1  fast_backtest == engine.backtest on U56 base book, 0 bps: max abs diff {e1:.3e} "
      f"-> {'PASS' if e1 < 1e-12 else 'FAIL'}")
    r0 = fast_backtest(pan.px, pan.W, 0.0, FREQ)
    r10 = fast_backtest(pan.px, pan.W, 10.0, FREQ)["returns"]
    e2 = float(np.abs(net(r0, 10.0) - r10).max())
    P(f"  G2  cost identity r(c) = r(0) - turnover*c/1e4: max abs diff {e2:.3e} "
      f"-> {'PASS' if e2 < 1e-15 else 'FAIL'}")
    # structural gates on the nulls themselves
    rng = np.random.default_rng(SEED)
    ok_cnt = ok_sw = tot = 0
    swk = {k: 0 for k in NULLS}
    for tau in TAUS:
        s_real = budget_on(pan, tau)
        if s_real.sum() in (0, len(s_real)): continue
        for kind in NULLS:
            for _ in range(5):
                d = draw_null(kind, s_real, pan.tt, rng, phi=0.50)
                tot += 1
                ok_cnt += int(d.sum() == s_real.sum())
                same_sw = int(circ_switches(d) == circ_switches(s_real))
                ok_sw += same_sw; swk[kind] += same_sw
    P(f"  G3  null STRUCTURE over {tot} draws: on-count preserved {ok_cnt}/{tot} "
      f"-> {'PASS' if ok_cnt == tot else 'FAIL'}")
    P(f"      circular switch count preserved: " +
      ", ".join(f"{k} {swk[k]}/{tot//len(NULLS)}" for k in NULLS) +
      "   (exact for ROT and RUN by construction; MC/STRAT are not clustering-matched and are")
    P(f"      not claimed to be — that is the price of matching the count on the turnover axis)")

    # ------------------------------------------------------------------ the frontier
    P("\n" + "=" * 120)
    P("Q1  THE FIDELITY-ENTROPY FRONTIER — every null, every arm, every panel (fidelity uses idea")
    P("    186's own definition: |TO_null - TO_real| / TO_real on realised annualised turnover)")
    P("=" * 120)
    P("    TWO DENOMINATORS ARE REPORTED.  Idea 186 divides by the OVERLAID book's own turnover —")
    P("    but a suppressing overlay drives that denominator toward ZERO as its on-share rises, so")
    P("    the published statistic is ill-conditioned exactly where idea 191 found it exploding.")
    P("    `fid_base` divides by the BASE book's turnover instead: overlay-independent and bounded.")
    rows = []
    for pan in pans:
        base0 = fast_backtest(pan.px, pan.W, 0.0, FREQ)
        idx0 = base0["returns"].index
        smp = idx0 >= pan.start
        isx = smp & (idx0 <= IS_END)
        osx = idx0 >= OOS_START
        tb = base0["turnover"]
        TO_base = ann_turn(tb[smp], idx0[smp])
        base_full = {c: net(base0, c)[smp] for c in COST_RUNGS}
        base_oos = {c: net(base0, c)[osx] for c in COST_RUNGS}
        for tau in TAUS:
            s_real = budget_on(pan, tau)
            K, J = int(s_real.sum()), len(s_real)
            if K == 0 or K == J: continue
            for mode in MODES:
                Wr, mr = apply_budget(pan, mode, s_real)
                rr = fast_backtest(pan.px, Wr, 0.0, FREQ, mask=mr)
                tr = rr["turnover"]
                TO_real = ann_turn(tr[smp], idx0[smp])
                TOr_is = ann_turn(tr[isx], idx0[isx])
                TOb_is = ann_turn(tb[isx], idx0[isx])
                variants = [(k, None) for k in ("ROT", "MC", "RUN")] + [("STRAT", f) for f in PHIS]
                for kind, phi in variants:
                    rng = np.random.default_rng(cell_seed(pan.name, tau, mode, kind, phi))
                    fid, fidb, fis, ov, swm = [], [], [], [], []
                    dS = {c: [] for c in COST_RUNGS}; dSo = {c: [] for c in COST_RUNGS}
                    for _ in range(N_NULL):
                        d = draw_null(kind, s_real, pan.tt, rng, phi=phi)
                        Wn, mn = apply_budget(pan, mode, d)
                        rn = fast_backtest(pan.px, Wn, 0.0, FREQ, mask=mn)
                        tn = rn["turnover"]
                        TO_n = ann_turn(tn[smp], idx0[smp])
                        fid.append(abs(TO_n - TO_real) / max(TO_real, 1e-12))
                        fidb.append(abs(TO_n - TO_real) / max(TO_base, 1e-12))
                        fis.append(abs(ann_turn(tn[isx], idx0[isx]) - TOr_is) / max(TOb_is, 1e-12))
                        ov.append(float((d & s_real).sum()) / K)
                        swm.append(int(circ_switches(d) == circ_switches(s_real)))
                        for c in COST_RUNGS:
                            dS[c].append(sh(net(rn, c)[smp]) - sh(base_full[c]))
                            dSo[c].append(sh(net(rn, c)[osx]) - sh(base_oos[c]))
                    for c in COST_RUNGS:
                        real_dS = sh(net(rr, c)[smp]) - sh(base_full[c])
                        real_os = sh(net(rr, c)[osx]) - sh(base_oos[c])
                        nb, nbo = np.array(dS[c], float), np.array(dSo[c], float)
                        rows.append(dict(
                            panel=pan.name, tau=tau, mode=mode, null=kind,
                            phi=(phi if phi is not None else np.nan), cost=c,
                            K=K, J=J, on_share=K / J,
                            TO_base=TO_base, TO_real=TO_real,
                            fid_mean=float(np.mean(fid)), fid_max=float(np.max(fid)),
                            fidb_mean=float(np.mean(fidb)), fidb_max=float(np.max(fidb)),
                            IS_fidb_mean=float(np.mean(fis)),
                            overlap_mean=float(np.mean(ov)), switch_match=float(np.mean(swm)),
                            real_dSharpe=float(real_dS), null_mean=float(nb.mean()),
                            null_sd=float(nb.std(ddof=1)), null_q95=float(np.quantile(nb, 0.95)),
                            clears=bool(real_dS > np.quantile(nb, 0.95)),
                            OOS_real_dSharpe=float(real_os),
                            OOS_q95=float(np.quantile(nbo, 0.95)),
                            OOS_clears=bool(real_os > np.quantile(nbo, 0.95))))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    P(f"  {len(G)} grid rows written ({G.panel.nunique()} panels x {G.tau.nunique()} tau x "
      f"{len(MODES)} modes x {len(PHIS)+3} null variants x {len(COST_RUNGS)} rungs)")

    fro = []
    for md in MODES:
        P(f"\n  POOLED BY NULL, mode = {md}"
          f"{'  (the suppressing overlay idea 203 is about)' if md == 'skip' else ''}:")
        P(f"  {'null':11s} {'fid/real':>9s} {'max':>9s} {'fid/base':>9s} {'max':>9s} "
          f"{'overlap':>8s} {'switch=':>8s} {'clears':>7s} {'n':>5s}")
        for kind in NULLS:
            for phi in (PHIS if kind == "STRAT" else [np.nan]):
                s = G[(G.null == kind) & (G["mode"] == md) &
                      (G.phi.isna() if not np.isfinite(phi) else (G.phi == phi))]
                if not len(s): continue
                lab = f"{kind}" + (f"({phi:.2f})" if np.isfinite(phi) else "")
                fro.append(dict(null=kind, phi=phi, label=lab, mode=md,
                                fid_mean=s.fid_mean.mean(), fid_max=s.fid_max.max(),
                                fidb_mean=s.fidb_mean.mean(), fidb_max=s.fidb_max.max(),
                                overlap=s.overlap_mean.mean(), switch_match=s.switch_match.mean(),
                                clear_rate=float(s.clears.mean()),
                                oos_clear_rate=float(s.OOS_clears.mean()), n=len(s)))
                P(f"  {lab:11s} {s.fid_mean.mean():9.1%} {s.fid_max.max():9.1%} "
                  f"{s.fidb_mean.mean():9.1%} {s.fidb_max.max():9.1%} "
                  f"{s.overlap_mean.mean():8.1%} {s.switch_match.mean():8.1%} "
                  f"{s.clears.mean():7.1%} {len(s):5d}")
    FRO = pd.DataFrame(fro)
    FRO.to_csv(OUT / f"{STAMP}.frontier.csv", index=False)
    P("\n  ('overlap' = share of the real overlay's own ON dates the null also fires on.  A null at")
    P("   overlap 100% IS the overlay: fidelity 0%, entropy 0%, and it tests nothing.  'fid/real' is")
    P("   idea 186's published denominator, 'fid/base' the overlay-independent one.)")

    P("\n  THE FRONTIER, read as one dial (skip mode, STRAT only): f -> overlap -> fidelity")
    P(f"  {'f':>6s} {'M/K':>6s} {'overlap':>8s} {'fid/base':>9s} {'null sd(dSharpe)':>17s}")
    for phi in PHIS:
        s = G[(G.null == "STRAT") & (G["mode"] == "skip") & (G.phi == phi)]
        if len(s):
            P(f"  {phi:6.2f} {1/phi:6.2f} {s.overlap_mean.mean():8.1%} {s.fidb_mean.mean():9.1%} "
              f"{s.null_sd.mean():17.4f}")
    P("  (monotone by construction: buying turnover fidelity spends the null's entropy one-for-one,")
    P("   and at f = 1.00 the 'null' is the overlay, sd 0.  There is no interior point that has both.)")

    # ------------------------------------------------------------------ idea 186 / 191 reproduction
    P("\n" + "=" * 120)
    P("Q2  REPRODUCING THE NUMBER IDEA 203 IS BUILT ON")
    P("=" * 120)
    r186 = G[(G.null == "ROT") & (G.tau.isin([0.10, 0.20, 0.30]))]
    r191 = G[(G.null == "ROT")]
    P(f"  ROT on idea 186's OWN tau grid {{0.10,0.20,0.30}}, both modes, 3 panels: "
      f"fid mean {r186.fid_mean.mean():.1%}  max {r186.fid_max.max():.1%}   "
      f"(idea 186 published 25.4% / 213.8%)")
    P(f"  ROT on the WIDENED grid {TAUS}: fid mean {r191.fid_mean.mean():.1%}  "
      f"max {r191.fid_max.max():.1%}   (idea 191 published 1782.7% mean)")
    rs = G[(G.null == "ROT") & (G["mode"] == "skip")]
    if len(rs) > 3:
        c = np.corrcoef(rs.on_share.values, rs.fid_mean.values)[0, 1]
        P(f"  ROT/skip fidelity vs on-share: Pearson r {c:+.4f} over {len(rs)} rows "
          f"-> the degradation idea 191 reported is {'CONFIRMED' if c > 0 else 'NOT CONFIRMED'} "
          f"as a function of on-share")
    P("  per-tau detail (ROT, skip, pooled over panels and rungs):")
    P(f"    {'tau':>6s} {'on-share':>9s} {'fid mean':>9s} {'fid max':>9s}")
    for tau in TAUS:
        s = rs[rs.tau == tau]
        if len(s):
            P(f"    {tau:6.2f} {s.on_share.mean():9.1%} {s.fid_mean.mean():9.1%} {s.fid_max.max():9.1%}")

    # ------------------------------------------------------------------ rule 8
    P("\n" + "=" * 120)
    P("Q3  RULE 8 — the null is chosen on 2010-2016 by TURNOVER FIDELITY ALONE, 2017-2026 read ONCE")
    P("=" * 120)
    # the choice is made on IS TURNOVER FIDELITY ALONE (never on a performance number), among
    # nulls that still have entropy: STRAT(1.00) is the overlay itself and is excluded a priori.
    key = ["panel", "tau", "mode", "cost"]
    elig = G[~((G.null == "STRAT") & (G.phi == 1.00))].copy()
    pick_idx = elig.groupby(key).IS_fidb_mean.idxmin()
    CH = elig.loc[pick_idx, key + ["null", "phi", "IS_fidb_mean", "OOS_real_dSharpe",
                                   "OOS_q95", "OOS_clears"]].rename(
        columns={"null": "chosen_null", "phi": "chosen_phi", "IS_fidb_mean": "IS_fid_chosen",
                 "OOS_q95": "OOS_q95_chosen", "OOS_clears": "clears_chosen"})
    RT = G[G.null == "ROT"][key + ["IS_fidb_mean", "OOS_q95", "OOS_clears"]].rename(
        columns={"IS_fidb_mean": "IS_fid_ROT", "OOS_q95": "OOS_q95_ROT", "OOS_clears": "clears_ROT"})
    W = CH.merge(RT, on=key, how="inner")
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P(f"  {len(W)} walk-forward cells.  The chosen null, by IS turnover fidelity alone:")
    for k, v in W.groupby(["chosen_null", "chosen_phi"], dropna=False).size().items():
        P(f"    {str(k):28s} {v:4d} cells")
    P(f"\n  OOS CLAUSE CLEAR RATE (does the real BUDGET overlay beat its own null's q95 OOS?)")
    P(f"  {'panel':10s} {'mode':6s} {'chosen':>10s} {'IS fid chosen':>14s} {'IS fid ROT':>11s} "
      f"{'clears chosen':>14s} {'clears ROT':>11s}")
    for (pn, md), s in W.groupby(["panel", "mode"]):
        P(f"  {pn:10s} {md:6s} {s.chosen_null.mode().iloc[0]:>10s} {s.IS_fid_chosen.mean():14.1%} "
          f"{s.IS_fid_ROT.mean():11.1%} {s.clears_chosen.mean():14.1%} {s.clears_ROT.mean():11.1%}")
    P(f"\n  POOLED: clears under the CHOSEN null {W.clears_chosen.mean():.1%} "
      f"({int(W.clears_chosen.sum())}/{len(W)}) vs under the incumbent ROT "
      f"{W.clears_ROT.mean():.1%} ({int(W.clears_ROT.sum())}/{len(W)}); "
      f"verdicts disagree on {(W.clears_chosen != W.clears_ROT).mean():.1%} of cells")

    # ------------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 120)
    P("Q4  BOTH KEEP PATHS on every REAL BUDGET book (full sample and OOS)")
    P("=" * 120)
    px = load_universe()
    startu = px.index[260]
    b2 = backtest(px, rules_v2_weights(px), cost_bps=10, freq=FREQ)["returns"].loc[startu:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=10, freq=FREQ)["returns"].loc[startu:]
    spyu = px["SPY"].pct_change().fillna(0).loc[startu:]
    ms, mso = metrics(spyu), metrics(spyu.loc[OOS_START:])
    mb, mb1, mb2 = metrics(b2), *halves(b2)
    s1, s2 = halves(spyu)
    P(f"  benchmarks (u56 sample, 10 bps): SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / "
      f"{ms['MaxDD']:.2%}  H {s1:.3f}/{s2:.3f}   OOS {mso['CAGR']:.2%} / {mso['Sharpe']:.4f} / "
      f"{mso['MaxDD']:.2%}")
    P(f"                                  RULES v2 {mb['CAGR']:.2%} / {mb['Sharpe']:.4f} / "
      f"{mb['MaxDD']:.2%}  H {mb1:.3f}/{mb2:.3f}   RULES v1 {metrics(v1)['Sharpe']:.4f}")
    keep = []
    P(f"\n  {'panel':10s} {'tau':>5s} {'mode':5s} {'c':>3s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>7s} "
      f"{'H1':>6s} {'H2':>6s} {'OOS_CAGR':>8s} {'OOS_Shp':>8s} {'OOS_DD':>7s} {'4a':>3s} {'4b':>3s}")
    for pan in pans:
        for tau in TAUS:
            s_real = budget_on(pan, tau)
            if s_real.sum() in (0, len(s_real)): continue
            for mode in MODES:
                Wr, mr = apply_budget(pan, mode, s_real)
                rr = fast_backtest(pan.px, Wr, 0.0, FREQ, mask=mr)
                for c in COST_RUNGS:
                    r = net(rr, c).loc[pan.start:]
                    m, mo = metrics(r), metrics(r.loc[OOS_START:])
                    h1, h2 = halves(r)
                    k4a = bool(h1 > mb1 and h2 > mb2 and m["MaxDD"] >= mb["MaxDD"])
                    k4b = bool(h1 > s1 and h2 > s2 and mo["Sharpe"] > mso["Sharpe"]
                               and m["MaxDD"] >= 0.60 * ms["MaxDD"] and m["CAGR"] >= 0.70 * ms["CAGR"])
                    keep.append(dict(panel=pan.name, tau=tau, mode=mode, cost=c, CAGR=m["CAGR"],
                                     Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                     OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                     OOS_MaxDD=mo["MaxDD"], keep4a=k4a, keep4b=k4b))
                    P(f"  {pan.name:10s} {tau:5.2f} {mode:5s} {c:3d} {m['CAGR']:7.2%} "
                      f"{m['Sharpe']:7.4f} {m['MaxDD']:7.2%} {h1:6.3f} {h2:6.3f} {mo['CAGR']:8.2%} "
                      f"{mo['Sharpe']:8.4f} {mo['MaxDD']:7.2%} {'Y' if k4a else '.':>3s} "
                      f"{'Y' if k4b else '.':>3s}")
    KP = pd.DataFrame(keep)
    KP.to_csv(OUT / f"{STAMP}.keep.csv", index=False)
    P(f"\n  KEEP PATHS: 4a {int(KP.keep4a.sum())}/{len(KP)}   4b {int(KP.keep4b.sum())}/{len(KP)}")
    P("  (4a/4b are judged on the u56 benchmark bars for every panel, as the record does; the")
    P("   BROAD/SMALL rows are therefore comparable to each other but their bars are u56's.)")

    # ------------------------------------------------------------------ Q5 arm-level rule 8
    P("\n" + "=" * 120)
    P("Q5  RULE 8 AT THE ARM LEVEL — for the 4b passers above.  (tau, mode) chosen on 2010-2016 by")
    P("    IS Sharpe, per panel and rung; 2017-2026 read ONCE.  No null is involved here.")
    P("=" * 120)
    P(f"  {'panel':10s} {'c':>3s} {'IS pick':>14s} {'IS_Shp':>7s} {'OOS_CAGR':>8s} {'OOS_Shp':>8s} "
      f"{'OOS_DD':>7s} {'4a':>3s} {'4b':>3s}   vs SPY OOS / v2 OOS")
    a8 = []
    for pan in pans:
        base0 = fast_backtest(pan.px, pan.W, 0.0, FREQ)
        idx0 = base0["returns"].index
        smp = idx0 >= pan.start
        isx = smp & (idx0 <= IS_END)
        cand = {}
        for tau in TAUS:
            s_real = budget_on(pan, tau)
            if s_real.sum() in (0, len(s_real)): continue
            for mode in MODES:
                Wr, mr = apply_budget(pan, mode, s_real)
                cand[(tau, mode)] = fast_backtest(pan.px, Wr, 0.0, FREQ, mask=mr)
        for c in COST_RUNGS:
            iss = {k: sh(net(v, c)[isx]) for k, v in cand.items()}
            # DEGENERATE ARMS.  On SMALL439 the tt distribution sits well above tau=0.05, so that
            # arm skips EVERY rebalance and the book holds its day-0 weights — which are all zero,
            # because no score exists before 252 closes.  The result is an all-cash book with zero
            # variance and an undefined Sharpe.  A chooser must not be allowed to "pick" a NaN, so
            # non-finite IS Sharpes are excluded from the argmax and counted here.
            fin = {k: v for k, v in iss.items() if np.isfinite(v)}
            n_deg = len(iss) - len(fin)
            if not fin:
                P(f"  {pan.name:10s} {c:3d}  every arm degenerate (all-cash) — no pick"); continue
            pick = max(fin, key=fin.get)
            r = net(cand[pick], c).loc[pan.start:]
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = halves(r)
            k4a = bool(h1 > mb1 and h2 > mb2 and m["MaxDD"] >= mb["MaxDD"])
            k4b = bool(h1 > s1 and h2 > s2 and mo["Sharpe"] > mso["Sharpe"]
                       and m["MaxDD"] >= 0.60 * ms["MaxDD"] and m["CAGR"] >= 0.70 * ms["CAGR"])
            a8.append(dict(panel=pan.name, cost=c, tau=pick[0], mode=pick[1], IS_Sharpe=fin[pick],
                           n_degenerate_arms=n_deg,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           keep4a=k4a, keep4b=k4b))
            P(f"  {pan.name:10s} {c:3d} {f'tau={pick[0]:.2f} {pick[1]}':>14s} {fin[pick]:7.4f} "
              f"{mo['CAGR']:8.2%} {mo['Sharpe']:8.4f} {mo['MaxDD']:7.2%} {'Y' if k4a else '.':>3s} "
              f"{'Y' if k4b else '.':>3s}   {mo['Sharpe']-mso['Sharpe']:+.4f} / "
              f"{mo['Sharpe']-metrics(b2.loc[OOS_START:])['Sharpe']:+.4f}"
              + (f"   [{n_deg} degenerate arm(s) excluded]" if n_deg else ""))
    pd.DataFrame(a8).to_csv(OUT / f"{STAMP}.armwalkforward.csv", index=False)
    P("  (this is the arm dial, not the idea's dial; it is reported because 4b passers appeared and")
    P("   PROTOCOL rule 8 requires a KEEP-candidate to survive an out-of-sample read of its own choice.)")

    G[["panel", "tau", "mode", "null", "phi", "cost", "on_share", "TO_base", "TO_real", "fid_mean",
       "fid_max", "fidb_mean", "fidb_max", "IS_fidb_mean", "overlap_mean",
       "switch_match"]].to_csv(OUT / f"{STAMP}.fidelity.csv", index=False)
    P(f"\nelapsed {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
