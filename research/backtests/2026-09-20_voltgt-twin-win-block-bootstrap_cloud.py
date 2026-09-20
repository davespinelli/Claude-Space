#!/usr/bin/env python3
"""Idea 1785 (lane cloud, 2026-09-20): DOES THE VOLTGT DIAL'S MATCHED-TWIN WIN SURVIVE A PAIRED
CIRCULAR-BLOCK BOOTSTRAP?

THE DEFECT THIS CLOSES
----------------------
Idea 1771 made vol-targeting the record's FIRST device to beat its own realised-mean-gross-matched
CONSTANT-GROSS twin: OOS +0.0587 of Sharpe and +6.16 pp of MaxDD on U56 (win share 0.810), +0.0503
/ +9.44 pp on B136 (0.790).  That sentence now carries the whole surviving claim of the standing
VOLTGT memo -- every addendum since has demoted the rung, the convention and the panel-sourcing,
and what is left is "the DIAL survives".  But the difference was published as a POINT ESTIMATE.
It has never been given a standard error, and idea 1537's paired circular-block bootstrap of
exactly this dMaxDD is still unrun.  A dial whose whole evidence is a mean difference of unknown
dispersion is not capital-worthy, and the win SHARE (0.810 of 100 cells) is not independent
evidence either: those 100 cells are 20 conventions x 5 targets on ONE 2,400-day tape, so their
"n" is the tape, not the cell count.

This run prices BOTH differences (dSharpe and dMaxDD) against their OWN block standard error, on
the paired daily return series of each book and its twin, and asks the only question that matters
for capital: is the win resolvable, and is it reachable under rule 8?

THE CONSTRUCTION
----------------
TUNED (2, the protocol maximum, ALL grid points reported):
    B   circular-block length in trading days   {5, 10, 21, 63}
    M   window the twin's gross is matched on   {IS, FULL, OOS}
PUBLISHED, NOT TUNED (carried from ideas 1730 / 1771 verbatim, not re-chosen here):
    target vol t   {0.08, 0.10, 0.12, 0.16, 0.20}
    panel          {U56, B136, SMALL665}     (SMALL: max_1d_move >= 1.0 dropped first)
    cost           {0, 10, 25, 50} bps       (exact: held/turnover do not depend on cost)
    sigma cell     (L = 20, d = 0)           the standing memo's own convention
    cadence        weekly, next-day execution, gross capped at 1.00, never levered
CONTROL: every VOLTGT book is paired with its own CONSTANT-GROSS twin, gross k bisected so the
    twin carries the SAME REALISED MEAN GROSS over window M.  M = IS makes the pairing legal for
    rule 8 (nothing after 2016-12-31 is read); M = FULL / OOS are reporting-only comparands and
    are labelled as such.
BOOTSTRAP: paired circular block resampling of the DAILY return series.  The same block start
    offsets are applied to book and twin, so the pairing (and therefore the difference) is
    preserved; 2,000 draws per cell from a fixed md5-derived seed stream (deterministic).
    Reported per cell: the observed difference, the bootstrap SE, a bootstrap t = obs / SE, and
    the two-sided share of draws on the wrong side of zero.

PRE-STATED VERDICT RULES (fixed before the run; no tuning-until-it-works)
------------------------------------------------------------------------
V1  RESOLVABILITY.  If |bootstrap t| < 2 for the headline U56 OOS dSharpe at a MAJORITY of the
    four block lengths, idea 1771's "first device to beat its matched twin" is NOT resolvable on
    this tape and the wording must not lean on it.
V2  THE TWO LEGS MAY DISAGREE, and that is a finding, not a failure: report dSharpe and dMaxDD
    separately and never average them.
V3  MaxDD IS A PATH STATISTIC.  A block bootstrap of daily returns destroys drawdown path
    structure at short blocks, so the dMaxDD SE is only interpretable if it is STABLE across the
    block ladder.  If the dMaxDD SE moves more than 2x from B=5 to B=63 the block bootstrap is
    the wrong instrument for that leg and this run says so rather than quoting a number.
V4  RULE 8 IS DECISIVE FOR CAPITAL.  A chooser that ranks targets by the IS bootstrap t of the
    book-minus-IS-matched-twin difference is 100% in-sample and therefore rule-8 legal.  If it
    does not land on a 4b-OOS-passing cell, the dial is not reachable whatever its SE.

Run: python research/backtests/2026-09-20_voltgt-twin-win-block-bootstrap_cloud.py
Deterministic, offline (committed caches only).  RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py are NOT modified by this run (rule 6).
"""
from __future__ import annotations
import sys, time, hashlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights      # noqa: E402
from engine import backtest, rebalance_mask                                  # noqa: E402

DATE, SLUG = "2026-09-20", "voltgt-twin-win-block-bootstrap"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, CAD = 260, "W"
MEMO_L, MEMO_D, MEMO_T = 20, 0, 0.16
GRID_T = [0.08, 0.10, 0.12, 0.16, 0.20]
GRID_B = [5, 10, 21, 63]                      # tuned dial 1
GRID_M = ["IS", "FULL", "OOS"]                # tuned dial 2
COSTS = [0.0, 10.0, 25.0, 50.0]
PRIMARY_COST = 10.0
NBOOT = 2000
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
# the convention surface, used ONLY to replicate idea 1771's pooled headline (gate G3)
SURF_L, SURF_D = [5, 10, 20, 40, 60], [0, 1, 2, 5]

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
    say(f"    PUBLISHED  {name}: {value}")


def seed_of(*parts):
    h = hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:8], 16)


# --------------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def keep_paths(r, bm, live):
    """4a against the LIVE RULES v2 book; 4b against SPY."""
    m = pack(r)
    k4a = bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(L1_H1=bool(m["H1"] > bm["H1"]), L2_H2=bool(m["H2"] > bm["H2"]),
                L4_DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                L5_CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, legs


# ---------------------------------------------------- vectorised bootstrap stats
def sharpe_rows(X):
    v = X.std(axis=1, ddof=0) * np.sqrt(252)
    out = np.full(X.shape[0], np.nan)
    ok = v > 0
    out[ok] = X[ok].mean(axis=1) * 252 / v[ok]
    return out


def mdd_rows(X):
    e = np.cumprod(1.0 + X, axis=1)
    return (e / np.maximum.accumulate(e, axis=1) - 1.0).min(axis=1)


def block_index(n, B, nboot, rng):
    """Circular block bootstrap index matrix (nboot x n).  ceil(n/B) blocks, wrapped, truncated."""
    nb = int(np.ceil(n / B))
    starts = rng.integers(0, n, size=(nboot, nb))
    off = np.arange(B)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(nboot, nb * B) % n
    return idx[:, :n]


def paired_boot(rb, rt, B, nboot, seed):
    """Paired circular-block bootstrap of (Sharpe, MaxDD) differences.  Book and twin are resampled
    with the SAME block offsets, so the difference keeps its pairing."""
    rng = np.random.default_rng(seed)
    n = len(rb)
    idx = block_index(n, B, nboot, rng)
    Xb, Xt = rb[idx], rt[idx]
    ds = sharpe_rows(Xb) - sharpe_rows(Xt)
    dd = mdd_rows(Xb) - mdd_rows(Xt)
    return ds, dd


def boot_row(obs, draws):
    """SE, bootstrap t and the two-sided wrong-side share for one difference."""
    d = draws[np.isfinite(draws)]
    if len(d) < 50:
        return dict(SE=np.nan, t=np.nan, p2=np.nan, lo=np.nan, hi=np.nan)
    se = float(d.std(ddof=1))
    centred = d - d.mean()
    p2 = float(2.0 * min((centred >= abs(obs)).mean(), (centred <= -abs(obs)).mean()))
    qlo, qhi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return dict(SE=se, t=float(obs / se) if se > 0 else np.nan, p2=min(1.0, p2),
                mean=float(d.mean()), lo=qlo, hi=qhi,
                plo=float(2 * obs - qhi), phi=float(2 * obs - qlo))


# --------------------------------------------------------- shared panel state
def ew_unit(px):
    e = px.notna().astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def panel_state(px, freq=CAD):
    """Engine-exact decomposition (verbatim from idea 1771's runner, gate G1 re-asserts it)."""
    R = px.pct_change().fillna(0.0).values
    E = ew_unit(px).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    T, N = R.shape
    Upre = np.zeros((T, N)); B = np.zeros(T)
    cur = np.zeros(N)
    for i in range(T):
        Upre[i] = cur
        if mask[i] or i == 0:
            cur = E[i]
        b = float(cur @ R[i]); B[i] = b
        cur = cur * (1 + R[i]) / (1 + b) if (1 + b) > 0 else cur
    return dict(R=R, E=E, mask=mask, B=B, Upre=Upre, T=T, idx=px.index)


def gross_path(st, gvec):
    B, mask, T = st["B"], st["mask"], st["T"]
    G = np.nan; out = np.empty(T)
    for i in range(T):
        if mask[i] or i == 0:
            G = gvec[i]
        out[i] = G
        tot = 1 + G * B[i]
        if tot > 0:
            G = G * (1 + B[i]) / tot
    return out


def run(st, gvec):
    B, mask, E, Upre, T = st["B"], st["mask"], st["E"], st["Upre"], st["T"]
    N = E.shape[1]
    G = np.nan; gross = np.empty(T); turn = np.zeros(T); gr = np.empty(T)
    nanv = np.full(N, np.nan)
    for i in range(T):
        if mask[i] or i == 0:
            held_now = G * Upre[i] if np.isfinite(G) else nanv
            turn[i] = np.abs(gvec[i] * E[i] - held_now).sum()
            G = gvec[i]
        gross[i] = G
        gr[i] = G * B[i]
        tot = 1 + G * B[i]
        if tot > 0:
            G = G * (1 + B[i]) / tot
    return gr, turn, gross


def rets_at(gr, turn, c):
    return gr - turn * c / 1e4


def voltgt_gvec(px, t, L=MEMO_L, d=MEMO_D):
    base = ew_unit(px)
    pr = (base.shift(1) * px.pct_change()).sum(axis=1)
    rv = pr.rolling(L).std() * np.sqrt(252)
    if d:
        rv = rv.shift(d)
    k = (t / rv.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return k.shift(1).fillna(0.0).values


def const_gvec(st, k):
    return np.full(st["T"], float(k))


def solve_twin(st, target_mean_gross, sl):
    lo, hi = 0.0, 1.0
    f = lambda k: float(np.nanmean(gross_path(st, const_gvec(st, k))[sl])) - target_mean_gross
    if f(hi) < 0:
        return 1.0, f(1.0)
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    k = 0.5 * (lo + hi)
    return k, f(k)


def small_panel():
    px = load_universe(small=True)
    mx = px.drop(columns=["SPY"]).pct_change().abs().max()
    keep = [c for c in px.columns if c == "SPY" or mx.get(c, 0.0) < 1.0]
    return px[keep], int(px.shape[1] - len(keep))


# ============================================================================ main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1785 (lane cloud, 2026-09-20) — DOES THE VOLTGT DIAL'S MATCHED-TWIN WIN SURVIVE A")
    say("PAIRED CIRCULAR-BLOCK BOOTSTRAP?")
    say("=" * 108)
    say(__doc__.split("Run:")[0].strip())
    say("=" * 108)

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sp, ndrop = small_panel()
    panels["SMALL665"] = sp
    say(f"\n  SMALL panel: dropped {ndrop} tickers with max_1d_move >= 1.0 (data/small_meta.csv rule)")
    say("  SURVIVORSHIP: U56 / B136 / SMALL are CURRENT constituents of their screens. Every number")
    say("  below is the optimistic read; delisted names are absent from all three panels.")
    for nm, px in panels.items():
        say(f"  panel {nm:9s} {px.shape[1]:4d} cols x {len(px):5d} days  "
            f"{px.index[0].date()} -> {px.index[-1].date()}")

    book_rows, boot_rows, wf_rows, surf_rows = [], [], [], []

    for pname, px in panels.items():
        say("\n" + "-" * 108)
        say(f"PANEL {pname}")
        say("-" * 108)
        st = panel_state(px)
        i0 = WARMUP
        ioos = int(px.index.searchsorted(pd.Timestamp(OOS_START)))
        iis = int(px.index.searchsorted(pd.Timestamp(IS_END), side="right"))
        SL = dict(FULL=slice(i0, None), OOS=slice(ioos, None), IS=slice(i0, iis))

        spy = px["SPY"].pct_change().fillna(0.0).values
        bm = {w: pack(spy[s]) for w, s in SL.items()}
        lv = backtest(px, rules_v2_weights(px), cost_bps=PRIMARY_COST, freq=CAD)["returns"].values
        v1 = backtest(px, rules_v1_weights(px), cost_bps=PRIMARY_COST, freq=CAD)["returns"].values
        live = {w: pack(lv[s]) for w, s in SL.items()}
        say(f"  SPY      FULL {bm['FULL']['CAGR']:7.2%} / {bm['FULL']['Sharpe']:.4f} / {bm['FULL']['MaxDD']:7.2%}"
            f"   OOS {bm['OOS']['CAGR']:7.2%} / {bm['OOS']['Sharpe']:.4f} / {bm['OOS']['MaxDD']:7.2%}")
        say(f"  RULES v2 FULL {live['FULL']['CAGR']:7.2%} / {live['FULL']['Sharpe']:.4f} / {live['FULL']['MaxDD']:7.2%}"
            f"   OOS {live['OOS']['CAGR']:7.2%} / {live['OOS']['Sharpe']:.4f} / {live['OOS']['MaxDD']:7.2%}")
        say(f"  RULES v1 FULL {pack(v1[SL['FULL']])['CAGR']:7.2%} / {pack(v1[SL['FULL']])['Sharpe']:.4f}"
            f" / {pack(v1[SL['FULL']])['MaxDD']:7.2%}")
        say(f"  4b bars FULL: H1>{bm['FULL']['H1']:.4f} H2>{bm['FULL']['H2']:.4f} "
            f"MaxDD>={DD_CAP*bm['FULL']['MaxDD']:.2%} CAGR>={CAGR_FLOOR*bm['FULL']['CAGR']:.2%}")
        say(f"  4b bars OOS : H1>{bm['OOS']['H1']:.4f} H2>{bm['OOS']['H2']:.4f} "
            f"MaxDD>={DD_CAP*bm['OOS']['MaxDD']:.2%} CAGR>={CAGR_FLOOR*bm['OOS']['CAGR']:.2%}")

        # -------- G1: the fast runner is engine-exact, at the memo cell
        gv = voltgt_gvec(px, MEMO_T)
        gr, turn, gpath = run(st, gv)
        W = ew_unit(px).mul(pd.Series(gv, index=px.index).shift(-1).fillna(0.0), axis=0)
        d1 = 0.0
        for c in (PRIMARY_COST, 25.0):
            eng = backtest(px, W, cost_bps=c, freq=CAD)["returns"].values
            d1 = max(d1, float(np.abs(rets_at(gr, turn, c)[i0:] - eng[i0:]).max()))
        gate(f"G1[{pname}] fast_run == engine.backtest (10 & 25 bps)", f"{d1:.3e}", "<= 1e-15", d1 <= 1e-15)

        # -------- the 15 books on this panel (5 targets x 3 matching windows)
        cache = {}
        for t in GRID_T:
            gvb = voltgt_gvec(px, t)
            grb, turnb, gpb = run(st, gvb)
            cache[t] = (grb, turnb, gpb)
            for M in GRID_M:
                mg = float(np.nanmean(gpb[SL[M]]))
                k, resid = solve_twin(st, mg, SL[M])
                grt, turnt, gpt = run(st, const_gvec(st, k))
                for c in COSTS:
                    rb_, rt_ = rets_at(grb, turnb, c), rets_at(grt, turnt, c)
                    for w in ("FULL", "OOS", "IS"):
                        a4b, b4b, mb, legsb = keep_paths(rb_[SL[w]], bm[w], live[w])
                        a4t, b4t, mt, legst = keep_paths(rt_[SL[w]], bm[w], live[w])
                        book_rows.append(dict(
                            panel=pname, t=t, M=M, cost=c, window=w, k_twin=k, twin_resid=resid,
                            mean_gross=float(np.nanmean(gpb[SL[w]])),
                            turn_yr=float(turnb[SL[w]].sum() * 252 / len(turnb[SL[w]])),
                            bk_CAGR=mb["CAGR"], bk_Sharpe=mb["Sharpe"], bk_MaxDD=mb["MaxDD"],
                            bk_H1=mb["H1"], bk_H2=mb["H2"], bk_4a=a4b, bk_4b=b4b, **{f"bk_{x}": y for x, y in legsb.items()},
                            tw_CAGR=mt["CAGR"], tw_Sharpe=mt["Sharpe"], tw_MaxDD=mt["MaxDD"],
                            tw_4a=a4t, tw_4b=b4t,
                            dSharpe=mb["Sharpe"] - mt["Sharpe"], dMaxDD=mb["MaxDD"] - mt["MaxDD"],
                            spy_CAGR=bm[w]["CAGR"], spy_Sharpe=bm[w]["Sharpe"], spy_MaxDD=bm[w]["MaxDD"],
                            live_CAGR=live[w]["CAGR"], live_Sharpe=live[w]["Sharpe"], live_MaxDD=live[w]["MaxDD"]))

                # -------- the bootstrap, at the primary cost rung, on FULL / OOS / IS
                rbp, rtp = rets_at(grb, turnb, PRIMARY_COST), rets_at(grt, turnt, PRIMARY_COST)
                for w in ("FULL", "OOS", "IS"):
                    x, y = rbp[SL[w]], rtp[SL[w]]
                    obs_s, obs_d = sharpe(x) - sharpe(y), mdd(x) - mdd(y)
                    for Bl in GRID_B:
                        ds, dd = paired_boot(x, y, Bl, NBOOT, seed_of(pname, t, M, w, Bl))
                        bs, bd = boot_row(obs_s, ds), boot_row(obs_d, dd)
                        boot_rows.append(dict(
                            panel=pname, t=t, M=M, window=w, block=Bl, n_days=len(x), nboot=NBOOT,
                            obs_dSharpe=obs_s, se_dSharpe=bs["SE"], t_dSharpe=bs["t"], p_dSharpe=bs["p2"],
                            ci_lo_dSharpe=bs["lo"], ci_hi_dSharpe=bs["hi"],
                            pv_lo_dSharpe=bs["plo"], pv_hi_dSharpe=bs["phi"], boot_mean_dSharpe=bs["mean"],
                            obs_dMaxDD=obs_d, se_dMaxDD=bd["SE"], t_dMaxDD=bd["t"], p_dMaxDD=bd["p2"],
                            ci_lo_dMaxDD=bd["lo"], ci_hi_dMaxDD=bd["hi"],
                            pv_lo_dMaxDD=bd["plo"], pv_hi_dMaxDD=bd["phi"], boot_mean_dMaxDD=bd["mean"],
                            boot_win_share_S=float(np.mean(ds > 0)), boot_win_share_D=float(np.mean(dd > 0))))

        # -------- G3 replication: idea 1771's pooled surface headline (large panels only)
        if pname in ("U56", "B136"):
            for L in SURF_L:
                for d_ in SURF_D:
                    for t in GRID_T:
                        gvs = voltgt_gvec(px, t, L, d_)
                        grs, turns, gps = run(st, gvs)
                        mg = float(np.nanmean(gps[SL["OOS"]]))
                        k, _ = solve_twin(st, mg, SL["OOS"])
                        grt, turnt, _ = run(st, const_gvec(st, k))
                        xs = rets_at(grs, turns, PRIMARY_COST)[SL["OOS"]]
                        ys = rets_at(grt, turnt, PRIMARY_COST)[SL["OOS"]]
                        surf_rows.append(dict(panel=pname, L=L, d=d_, t=t,
                                              dSharpe=sharpe(xs) - sharpe(ys),
                                              dMaxDD=mdd(xs) - mdd(ys)))

        # -------- rule 8: IS-only choosers over t, evaluated ONCE on 2017-2026
        say(f"\n  RULE 8 on {pname} — parameters chosen on 2009-2016 only, 2017-2026 read once")
        bk = pd.DataFrame(book_rows)
        bk = bk[(bk.panel == pname) & (bk.cost == PRIMARY_COST)]
        bt = pd.DataFrame(boot_rows)
        bt = bt[(bt.panel == pname)]
        for chooser in ("C_ISSHARPE", "C_GXS_IS", "C_GXDD_IS", "C_BOOTT_S", "C_BOOTT_D"):
            for Bl in GRID_B if chooser.startswith("C_BOOTT") else [None]:
                isr = bk[(bk.window == "IS") & (bk.M == "IS")].set_index("t")
                if chooser == "C_ISSHARPE":
                    score = isr["bk_Sharpe"]
                elif chooser == "C_GXS_IS":
                    score = isr["dSharpe"]
                elif chooser == "C_GXDD_IS":
                    score = isr["dMaxDD"]
                else:
                    sub = bt[(bt.window == "IS") & (bt.M == "IS") & (bt.block == Bl)].set_index("t")
                    score = sub["t_dSharpe"] if chooser == "C_BOOTT_S" else sub["t_dMaxDD"]
                pick = float(score.astype(float).idxmax())
                o = bk[(bk.window == "OOS") & (bk.M == "IS") & (bk.t == pick)].iloc[0]
                f = bk[(bk.window == "FULL") & (bk.M == "IS") & (bk.t == pick)].iloc[0]
                wf_rows.append(dict(panel=pname, chooser=chooser, block=Bl, pick_t=pick,
                                    oos_CAGR=o.bk_CAGR, oos_Sharpe=o.bk_Sharpe, oos_MaxDD=o.bk_MaxDD,
                                    oos_4a=o.bk_4a, oos_4b=o.bk_4b,
                                    full_4a=f.bk_4a, full_4b=f.bk_4b,
                                    full_CAGR=f.bk_CAGR, full_Sharpe=f.bk_Sharpe, full_MaxDD=f.bk_MaxDD,
                                    full_H1=f.bk_H1, full_H2=f.bk_H2,
                                    spy_oos_CAGR=o.spy_CAGR, spy_oos_Sharpe=o.spy_Sharpe, spy_oos_MaxDD=o.spy_MaxDD,
                                    live_oos_CAGR=o.live_CAGR, live_oos_Sharpe=o.live_Sharpe,
                                    live_oos_MaxDD=o.live_MaxDD))
                tag = chooser + (f"[B={Bl}]" if Bl else "")
                say(f"    {tag:16s} -> t={pick:.2f}   OOS {o.bk_CAGR:7.2%} / {o.bk_Sharpe:.4f} / "
                    f"{o.bk_MaxDD:7.2%}   4b OOS {'PASS' if o.bk_4b else 'FAIL'}   "
                    f"4a OOS {'PASS' if o.bk_4a else 'FAIL'}")

    BK = pd.DataFrame(book_rows); BT = pd.DataFrame(boot_rows)
    WF = pd.DataFrame(wf_rows); SF = pd.DataFrame(surf_rows)

    # ======================================================== gates & replication
    say("\n" + "=" * 108); say("GATES"); say("=" * 108)
    memo = BK[(BK.panel == "U56") & (BK.t == MEMO_T) & (BK.M == "FULL") & (BK.cost == PRIMARY_COST)]
    mf = memo[memo.window == "FULL"].iloc[0]
    mo = memo[memo.window == "OOS"].iloc[0]
    d2 = max(abs(mf.bk_CAGR - 0.1561), abs(mf.bk_Sharpe - 1.2027), abs(mf.bk_MaxDD + 0.1986),
             abs(mo.bk_CAGR - 0.1594), abs(mo.bk_Sharpe - 1.2193), abs(mo.bk_MaxDD + 0.1986))
    gate("G2 memo sections 2-4 (U56 t=0.16) reproduced", f"max|d| {d2:.3e}", "< 5e-3", d2 < 5e-3)

    for pn, tgt_s, tgt_d, tgt_w in (("U56", 0.0587, 0.0616, 0.810), ("B136", 0.0503, 0.0944, 0.790)):
        s = SF[SF.panel == pn]
        gs, gd, gw = s.dSharpe.mean(), s.dMaxDD.mean(), float((s.dSharpe > 0).mean())
        ok = abs(gs - tgt_s) < 0.01 and abs(gd - tgt_d) < 0.015 and abs(gw - tgt_w) < 0.06
        gate(f"G3[{pn}] idea 1771 pooled OOS twin win reproduced",
             f"dSharpe {gs:+.4f} (1771 {tgt_s:+.4f}), dMaxDD {gd:+.4f} ({tgt_d:+.4f}), win {gw:.3f} ({tgt_w:.3f})",
             "within 0.01 / 0.015 / 0.06", ok)

    rz = BK[(BK.M == "IS") & (BK.window == "IS")]
    gate("G4 IS-matched twins solved to machine precision", f"max|resid| {rz.twin_resid.abs().max():.3e}",
         "< 1e-9", rz.twin_resid.abs().max() < 1e-9)
    ss = BK[(BK.panel == "SMALL665") & (BK.cost == PRIMARY_COST)]
    gate("G5 SMALL665 4b share (memo addendum A2)", f"{ss.bk_4b.mean():.3f} of {len(ss)} rows",
         "0.000 (A2, fourth confirmation)", ss.bk_4b.sum() == 0)
    publish("G6 grid size", f"{len(BK)} book rows, {len(BT)} bootstrap rows, {len(SF)} surface rows, "
                            f"{len(WF)} walk-forward picks, {NBOOT} draws/cell")

    # ======================================================== V1 / V2 / V3
    say("\n" + "=" * 108); say("VERDICT RULES"); say("=" * 108)
    hd = BT[(BT.panel == "U56") & (BT.window == "OOS") & (BT.M == "OOS") & (BT.t == MEMO_T)]
    say("\n  V1 — HEADLINE U56 OOS, memo rung t=0.16, twin matched OOS (idea 1771's own comparand):")
    say(f"      observed dSharpe {hd.obs_dSharpe.iloc[0]:+.4f}   dMaxDD {hd.obs_dMaxDD.iloc[0]:+.4f}")
    for _, r in hd.sort_values("block").iterrows():
        say(f"      B={r.block:3.0f}  dSharpe SE {r.se_dSharpe:.4f} t {r.t_dSharpe:+6.2f} p {r.p_dSharpe:.3f} "
            f"pct [{r.ci_lo_dSharpe:+.3f},{r.ci_hi_dSharpe:+.3f}] pivotal [{r.pv_lo_dSharpe:+.3f},{r.pv_hi_dSharpe:+.3f}] "
            f"bootmean {r.boot_mean_dSharpe:+.4f}")
        say(f"             dMaxDD  SE {r.se_dMaxDD:.4f} t {r.t_dMaxDD:+6.2f} p {r.p_dMaxDD:.3f} "
            f"pct [{r.ci_lo_dMaxDD:+.3f},{r.ci_hi_dMaxDD:+.3f}] pivotal [{r.pv_lo_dMaxDD:+.3f},{r.pv_hi_dMaxDD:+.3f}] "
            f"bootmean {r.boot_mean_dMaxDD:+.4f}")
    nres = int((hd.t_dSharpe.abs() < 2).sum())
    gate("V1 U56 OOS dSharpe UNRESOLVED (|t|<2) at a majority of blocks",
         f"{nres} of {len(hd)} block lengths", "reported, not asserted", True)

    ddse = hd.set_index("block").se_dMaxDD
    ratio = float(ddse.max() / ddse.min())
    gate("V3 dMaxDD SE stability across the block ladder", f"max/min = {ratio:.2f}x "
         f"(B=5 {ddse.loc[5]:.4f} -> B=63 {ddse.loc[63]:.4f})", "< 2x for the leg to be quotable",
         ratio < 2.0)

    # per-leg resolvability census across the whole grid
    say("\n  V2 — the two legs, censused separately (OOS window, 10 bps, all panels x targets x M):")
    for leg, tcol, ocol in (("dSharpe", "t_dSharpe", "obs_dSharpe"), ("dMaxDD", "t_dMaxDD", "obs_dMaxDD")):
        g = BT[BT.window == "OOS"]
        say(f"      {leg:8s}  mean obs {g[ocol].mean():+.4f}   share obs>0 {float((g[ocol]>0).mean()):.3f}   "
            f"share |t|>=2 {float((g[tcol].abs()>=2).mean()):.3f}   share t<=-2 {float((g[tcol]<=-2).mean()):.3f}")
        for pn in panels:
            gp = g[g.panel == pn]
            say(f"        {pn:9s} mean obs {gp[ocol].mean():+.4f}  share obs>0 {float((gp[ocol]>0).mean()):.3f}"
                f"  share t>=2 {float((gp[tcol]>=2).mean()):.3f}  share t<=-2 {float((gp[tcol]<=-2).mean()):.3f}")

    say("\n  CI COVERAGE OF ZERO — the conservative read (OOS window, all panels x targets x M x B):")
    for leg in ("dSharpe", "dMaxDD"):
        g = BT[BT.window == "OOS"]
        pct0 = float(((g[f"ci_lo_{leg}"] <= 0) & (g[f"ci_hi_{leg}"] >= 0)).mean())
        pv0 = float(((g[f"pv_lo_{leg}"] <= 0) & (g[f"pv_hi_{leg}"] >= 0)).mean())
        say(f"      {leg:8s} 95% percentile CI covers 0 in {pct0:.3f} of {len(g)} cells; "
            f"pivotal CI covers 0 in {pv0:.3f}")
        for pn in panels:
            gp = g[g.panel == pn]
            a = float(((gp[f"ci_lo_{leg}"] <= 0) & (gp[f"ci_hi_{leg}"] >= 0)).mean())
            b = float(((gp[f"pv_lo_{leg}"] <= 0) & (gp[f"pv_hi_{leg}"] >= 0)).mean())
            say(f"        {pn:9s} percentile {a:.3f}   pivotal {b:.3f}")

    say("\n  BLOCK LADDER — how the SE moves with the tuned dial B (U56 OOS, pooled over t and M):")
    g = BT[(BT.panel == "U56") & (BT.window == "OOS")]
    for Bl in GRID_B:
        gb = g[g.block == Bl]
        say(f"      B={Bl:3d}  mean SE dSharpe {gb.se_dSharpe.mean():.4f}  mean |t| {gb.t_dSharpe.abs().mean():5.2f}"
            f"   |   mean SE dMaxDD {gb.se_dMaxDD.mean():.4f}  mean |t| {gb.t_dMaxDD.abs().mean():5.2f}")

    say("\n  MATCHING WINDOW M — the other tuned dial (U56 OOS, B=21, all targets):")
    for M in GRID_M:
        gm = BT[(BT.panel == "U56") & (BT.window == "OOS") & (BT.block == 21) & (BT.M == M)]
        say(f"      M={M:5s} mean obs dSharpe {gm.obs_dSharpe.mean():+.4f} (mean t {gm.t_dSharpe.mean():+5.2f})"
            f"   mean obs dMaxDD {gm.obs_dMaxDD.mean():+.4f} (mean t {gm.t_dMaxDD.mean():+5.2f})")

    # ======================================================== full grid + KEEP paths
    say("\n" + "=" * 108); say("EVERY GRID POINT — books vs SPY and vs live RULES v2 (10 bps)"); say("=" * 108)
    for pn in panels:
        for w in ("FULL", "OOS"):
            say(f"\n  {pn} / {w}")
            g = BK[(BK.panel == pn) & (BK.window == w) & (BK.cost == PRIMARY_COST) & (BK.M == "IS")]
            for _, r in g.sort_values("t").iterrows():
                say(f"    t={r.t:.2f}  book {r.bk_CAGR:7.2%} / {r.bk_Sharpe:.4f} / {r.bk_MaxDD:7.2%}"
                    f"  (H1 {r.bk_H1:.3f} H2 {r.bk_H2:.3f})  gross {r.mean_gross:.3f} turn {r.turn_yr:.2f}/yr"
                    f"   4a {'P' if r.bk_4a else '.'} 4b {'P' if r.bk_4b else '.'}"
                    f"   | twin k={r.k_twin:.4f} {r.tw_CAGR:7.2%} / {r.tw_Sharpe:.4f} / {r.tw_MaxDD:7.2%}"
                    f" 4b {'P' if r.tw_4b else '.'}   d {r.dSharpe:+.4f} / {r.dMaxDD:+.4f}")
            say(f"    SPY      {g.spy_CAGR.iloc[0]:7.2%} / {g.spy_Sharpe.iloc[0]:.4f} / {g.spy_MaxDD.iloc[0]:7.2%}")
            say(f"    RULES v2 {g.live_CAGR.iloc[0]:7.2%} / {g.live_Sharpe.iloc[0]:.4f} / {g.live_MaxDD.iloc[0]:7.2%}")

    say("\n  COST LADDER — 4b pass counts by cost rung (M=IS books, all panels x targets):")
    for c in COSTS:
        g = BK[(BK.cost == c) & (BK.M == "IS")]
        say(f"      {c:5.1f} bps   4b FULL {int(g[g.window=='FULL'].bk_4b.sum()):2d}/{len(g[g.window=='FULL']):2d}"
            f"   4b OOS {int(g[g.window=='OOS'].bk_4b.sum()):2d}/{len(g[g.window=='OOS']):2d}"
            f"   4a FULL {int(g[g.window=='FULL'].bk_4a.sum()):2d}   4a OOS {int(g[g.window=='OOS'].bk_4a.sum()):2d}")

    say("\n  BINDING 4b LEGS (M=IS, 10 bps, OOS, all panels x targets):")
    g = BK[(BK.window == "OOS") & (BK.cost == PRIMARY_COST) & (BK.M == "IS")]
    for leg in ("bk_L1_H1", "bk_L2_H2", "bk_L4_DD", "bk_L5_CAGR"):
        say(f"      {leg:10s} fails {int((~g[leg]).sum()):2d} of {len(g)}")

    # ======================================================== V4
    say("\n" + "=" * 108); say("V4 — RULE 8 (parameters on 2009-2016 only; 2017-2026 read once)"); say("=" * 108)
    for pn in panels:
        w = WF[WF.panel == pn]
        say(f"    {pn:9s} legal IS-only picks clearing 4b OOS: {int(w.oos_4b.sum())} of {len(w)}"
            f"   4a OOS: {int(w.oos_4a.sum())} of {len(w)}")
    say(f"    ALL PANELS  4b OOS {int(WF.oos_4b.sum())} of {len(WF)}   4a OOS {int(WF.oos_4a.sum())} of {len(WF)}")
    for ch in WF.chooser.unique():
        w = WF[WF.chooser == ch]
        say(f"      {ch:12s} 4b OOS {int(w.oos_4b.sum())}/{len(w)}   4b FULL {int(w.full_4b.sum())}/{len(w)}"
            f"   picks {sorted(set(w.pick_t))}")
    boot_ch = WF[WF.chooser.isin(["C_BOOTT_S", "C_BOOTT_D"])]
    plain = WF[WF.chooser == "C_ISSHARPE"]
    gate("V4 bootstrap-t chooser beats plain IS Sharpe on 4b OOS",
         f"BOOT-t {int(boot_ch.oos_4b.sum())}/{len(boot_ch)} vs C_ISSHARPE {int(plain.oos_4b.sum())}/{len(plain)}",
         "reported, not asserted", True)

    # the OOS oracle, for the reachability gap
    say("\n    OOS ORACLE (hindsight, NOT a chooser) — best OOS Sharpe per panel, M=IS, 10 bps:")
    for pn in panels:
        g = BK[(BK.panel == pn) & (BK.window == "OOS") & (BK.cost == PRIMARY_COST) & (BK.M == "IS")]
        r = g.loc[g.bk_Sharpe.idxmax()]
        say(f"      {pn:9s} t={r.t:.2f}  OOS {r.bk_CAGR:7.2%} / {r.bk_Sharpe:.4f} / {r.bk_MaxDD:7.2%}"
            f"   4b {'PASS' if r.bk_4b else 'FAIL'}")

    # ======================================================== write
    BK.to_csv(f"{OUT}.books.csv", index=False)
    BT.to_csv(f"{OUT}.bootstrap.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    SF.to_csv(f"{OUT}.surface.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in GATES)
    say(f"\n  GATES {npass} of {len(GATES)}   runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
