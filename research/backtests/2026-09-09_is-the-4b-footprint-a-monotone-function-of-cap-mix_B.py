#!/usr/bin/env python3
"""Idea 285 (lane B, 2026-09-09): is the 4b footprint a monotone function of cap mix?

The question
------------
Idea 276 mixed small-cap and large-cap names in one k=40 panel at small-cap share
q in {0.0, 0.1, ..., 1.0} (6 draws each = 66 panels) and ran idea 2's CAND-n book on
every one.  PROTOCOL 4b passed 3/66 at n=10 and 16/66 at n=20, and EVERY pass sat at
q <= 0.5.  So the KEEP path's own eligibility tracks the panel's capitalisation.  That
is a per-panel verdict.  The queue asks for the ADMISSIBILITY CURVE instead: sweep q at
finer resolution with more draws, and report the q at which each 4b bar (H1, H2, OOS,
DD cap, CAGR floor) FIRST BINDS.

Three things follow, and this run does all three.

  PART A (the curve)      21 q rungs x 12 draws x 2 book sizes = 504 book cells.  Per q
                          and per book size, the pass rate of each of the five 4b legs
                          separately and of the joint path, plus each leg's mean SLACK
                          in raw units and in that leg's own cross-draw sd (idea 253's
                          two units, now along the cap axis instead of the k axis).
                          "First binds" is published two ways: the smallest q at which
                          a leg's pass rate first leaves 1.0, and the smallest q at
                          which it first falls below 0.5.

  PART B (monotonicity)   The queue's own word.  Spearman(q, joint 4b), Spearman(q,
                          slack) per leg, and a direct count of monotonicity violations
                          in the per-q pass-rate curve.  A curve with violations is not
                          publishable as an admissibility THRESHOLD, only as a gradient.

  PART C (rule 8)         An admissibility curve is only worth publishing if its SHAPE
                          replicates.  Re-derive the curve on IS 2010-2016 alone and on
                          OOS 2017-2026 alone (four legs; the OOS leg is not defined
                          inside a window) and compare where each leg first binds.  Plus
                          the ordinary rule-8 book test: q chosen on IS by argmax mean
                          IS Sharpe, OOS 2017-2026 read once against RULES v2 on the
                          same panel, SPY, and the do-nothing anchor (mean OOS over all
                          q).  Both KEEP paths evaluated on every cell.

TUNED PARAMETERS (max 2, PROTOCOL rule 4): q (21 rungs) and n (book size, 2 values).
ALL 504 mix cells + 10 named-panel cells are reported (console aggregates, .grid.csv
carries every row).  k=40, 12 draws, the RULES v1 eligibility gate, 75% gross, weekly
cadence, 10 bps and next-day execution are fixed at the record's published conventions
and are NOT tuned here.

GATES
  G0  fast_backtest (vectorised twin) vs engine.backtest, on two real mix panels.
  G1  idea 276 reproduced at ITS OWN settings (seed 2026, q step 0.1, 6 draws, k=40,
      n in {10,20}): its published 4b footprint is 3/66 and 16/66.

SURVIVORSHIP (PROTOCOL rule 9): the small panel and broad136 are CURRENT constituents of
their screens, so every small-cap number is biased upward by an unknown amount.  The
object under test is the SHAPE of the 4b footprint along the cap axis, which survivorship
moves through the level of small-cap returns, not obviously through the ordering; the
curve below should be read as an admissibility curve for THIS corpus, not for the market.

Deterministic (seeded).  Writes .grid.csv .curve.csv .binding.csv .walkforward.csv
.console.txt .result.md
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score            # noqa: E402
from engine import backtest, metrics, rebalance_mask                   # noqa: E402

STEM = Path(__file__).resolve().with_suffix("")
COST, FREQ, GROSS = 10.0, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
K_MIX, N_DRAWS = 40, 12
QS = [round(0.05 * i, 2) for i in range(21)]
NS = [10, 20]
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
BARS4 = ["H1", "H2", "DD", "CAGR"]
SEED = 285

_LOG = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ---------------------------------------------------------------- engine twin
def fast_backtest(px, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost; gated against it in G0."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        T = u.sum(axis=1) + (1.0 - w.sum())
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def run_net(px, wfn, cost=COST):
    r0, turn = fast_backtest(px, wfn(px))
    return r0 - turn * cost / 1e4


# ---------------------------------------------------------------- books
def cand_weights(n):
    """Idea 2's KEEP-candidate book, verbatim from idea 276: RULES v1 gate, composite
    score (no vol scaler), top n equal-weighted at 75% gross."""
    def f(px):
        tradables = [c for c in px.columns if c != "SPY"]
        s, above, vol20 = score(px[tradables], vol_scale=False)
        elig = s.where(above & (vol20 < 0.60))
        rank = elig.rank(axis=1, ascending=False)
        w = (rank <= n).astype(float) * (GROSS / n)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f


def v2_weights(px):
    return (rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
            .reindex(columns=px.columns).fillna(0.0))


# ---------------------------------------------------------------- metrics
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r); h1, h2 = hs(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"])


def slacks5(r, spy):
    """PROTOCOL 4b legs as SLACKS, positive = passing (idea 306's sign convention)."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    return {"H1": h1 - s1, "H2": h2 - s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"],
            "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
            "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}


def slacks4(r, spy):
    """The four legs that are computable INSIDE an arbitrary window (no OOS leg)."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    return {"H1": h1 - s1, "H2": h2 - s2,
            "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
            "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}


def pass4a(row, v2):
    return bool(row["H1"] > v2["H1"] and row["H2"] > v2["H2"] and row["MaxDD"] >= v2["MaxDD"])


# ---------------------------------------------------------------- panels
def sources():
    import json
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    px56, pxb = load_universe(), load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    pxs = load_universe(small=True)
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    b_all = [c for c in pxb.columns if c != "SPY"]
    b_stk = [c for c in b_all if c not in etfs]
    b_etf = [c for c in b_all if c in etfs]
    u_all = [c for c in px56.columns if c != "SPY"]
    P(f"SMALL: {len(pxs.columns)-1} screened names, dropped {len(bad)} with max_1d_move>=1.0 "
      f"-> {len(s_stk)};  B136 {len(b_all)} = BSTK{len(b_stk)} + ETF{len(b_etf)};  U56 {len(u_all)}")
    return dict(px56=px56, pxb=pxb, pxs=pxs, s_stk=s_stk, b_stk=b_stk, b_etf=b_etf, u_all=u_all)


def mix_panel(pxs_c, pxb_c, spy, sc, lc):
    parts = [p for p in (pxs_c[sc] if sc else None, pxb_c[lc] if lc else None) if p is not None]
    px = pd.concat(parts + [spy.rename("SPY")], axis=1).dropna(how="all").ffill()
    return px[list(sc) + list(lc) + ["SPY"]]


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none): Pearson of the ranks."""
    x, y = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = x.notna() & y.notna()
    if ok.sum() < 3: return float("nan")
    return float(x[ok].rank().corr(y[ok].rank()))


def pava_decreasing(y):
    """Pool-adjacent-violators: the least-squares best NON-INCREASING fit to y."""
    vals = list(map(float, y)); wts = [1.0] * len(y)
    i = 0
    while i < len(vals) - 1:
        if vals[i] < vals[i + 1] - 1e-15:                     # violation of non-increasing
            w = wts[i] + wts[i + 1]
            v = (vals[i] * wts[i] + vals[i + 1] * wts[i + 1]) / w
            vals[i:i + 2] = [v]; wts[i:i + 2] = [w]
            i = max(i - 1, 0)
        else:
            i += 1
    out = []
    for v, w in zip(vals, wts): out.extend([v] * int(round(w)))
    return np.array(out)


def first_binding(qs, rate, thr):
    """Smallest q whose pass rate is < thr; None if the leg never binds on the grid."""
    for q in qs:
        if rate[q] < thr:
            return q
    return None


# ---------------------------------------------------------------- gates
def gate_G0(px):
    for tag, wfn in (("CAND20", cand_weights(20)), ("v2", v2_weights)):
        W = wfn(px)
        ref = backtest(px, W, cost_bps=0.0, freq=FREQ)
        r0, t0 = fast_backtest(px, W)
        # engine.backtest leaves the rows BEFORE the first rebalance undefined (its
        # w_target is shift(1)ed, so row 0 is all-NaN and turnover is NaN there); the twin
        # zero-fills them.  Those rows sit far outside every evaluation window (which all
        # start at px.index[260]).  Compare where the reference is defined and say how
        # many rows that excludes.
        ok = np.isfinite(ref["returns"].values) & np.isfinite(ref["turnover"].values)
        dr = float(np.abs(ref["returns"].values[ok] - r0.values[ok]).max())
        dt = float(np.abs(ref["turnover"].values[ok] - t0.values[ok]).max())
        P(f"  G0 {tag:6s}  max|dret| {dr:.3e}   max|dturnover| {dt:.3e}   "
          f"over {int(ok.sum())}/{len(ok)} rows ({int((~ok).sum())} undefined in the reference, "
          f"all before {px.index[int((~ok).sum())].date()})   "
          f"{'PASS' if dr < 1e-12 and dt < 1e-9 else 'FAIL'}")


def gate_G1(src, pxs_c, pxb_c, spy):
    """Idea 276 at its own settings: seed 2026, q step 0.1, 6 draws, k=40, n in {10,20}.
    Its published footprint is 4b 3/66 (n=10) and 16/66 (n=20), every pass at q <= 0.5."""
    rng = np.random.default_rng(2026)
    cnt = {10: 0, 20: 0}; qmax = {10: -1.0, 20: -1.0}; tot = 0
    for q in [round(0.1 * i, 1) for i in range(11)]:
        ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
        for _ in range(6):
            sc = list(rng.choice(src["s_stk"], size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(src["b_stk"], size=nl_, replace=False)) if nl_ else []
            px = mix_panel(pxs_c, pxb_c, spy, sc, lc)
            st = px.index[260]
            sp = px["SPY"].pct_change().fillna(0).loc[st:]
            tot += 1
            for n in NS:
                r = run_net(px, cand_weights(n)).loc[st:]
                if all(v >= 0 for v in slacks5(r, sp).values()):
                    cnt[n] += 1; qmax[n] = max(qmax[n], q)
    P(f"  G1 idea 276 replay ({tot} panels): 4b n=10 {cnt[10]}/66 (published 3/66), "
      f"n=20 {cnt[20]}/66 (published 16/66); max q of a pass "
      f"n=10 {qmax[10]:.1f} n=20 {qmax[20]:.1f} (published <= 0.5)")
    return cnt


# ---------------------------------------------------------------- main
def main():
    src = sources()
    pxs, pxb, px56 = src["pxs"], src["pxb"], src["px56"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days)")

    P("\n=== GATES ===")
    rng0 = np.random.default_rng(SEED)
    g0px = mix_panel(pxs_c, pxb_c, spy,
                     list(rng0.choice(src["s_stk"], 20, replace=False)),
                     list(rng0.choice(src["b_stk"], 20, replace=False)))
    gate_G0(g0px)
    gate_G1(src, pxs_c, pxb_c, spy)

    # ---------------- PART A: the sweep
    P(f"\n=== PART A: MIX SWEEP  q in {QS[0]}..{QS[-1]} step 0.05 ({len(QS)} rungs) "
      f"x {N_DRAWS} draws x n in {NS} = {len(QS)*N_DRAWS*len(NS)} book cells, ALL reported ===")
    rng = np.random.default_rng(SEED)
    rows = []
    for q in QS:
        ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
        for d in range(N_DRAWS):
            sc = list(rng.choice(src["s_stk"], size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(src["b_stk"], size=nl_, replace=False)) if nl_ else []
            px = mix_panel(pxs_c, pxb_c, spy, sc, lc)
            st = px.index[260]
            sp = px["SPY"].pct_change().fillna(0).loc[st:]
            v2r = mrow(run_net(px, v2_weights).loc[st:])
            for n in NS:
                r = run_net(px, cand_weights(n)).loc[st:]
                m = mrow(r)
                s5 = slacks5(r, sp)
                s4_is = slacks4(r.loc[:IS_END], sp.loc[:IS_END])
                s4_oos = slacks4(r.loc[OOS_START:], sp.loc[OOS_START:])
                rows.append(dict(kind="mix", q=q, draw=d, n=n, k_small=ns_, k_large=nl_, **m,
                                 **{f"s_{b}": s5[b] for b in BARS5},
                                 **{f"is_{b}": s4_is[b] for b in BARS4},
                                 **{f"oos_{b}": s4_oos[b] for b in BARS4},
                                 pass4b=all(v >= 0 for v in s5.values()),
                                 pass4a=pass4a(m, v2r),
                                 v2_S=v2r["Sharpe"], v2_H1=v2r["H1"], v2_H2=v2r["H2"],
                                 v2_DD=v2r["MaxDD"], v2_OOS_S=v2r["OOS_Sharpe"],
                                 spy_S=metrics(sp)["Sharpe"], spy_CAGR=metrics(sp)["CAGR"],
                                 spy_DD=metrics(sp)["MaxDD"],
                                 spy_OOS_S=metrics(sp.loc[OOS_START:])["Sharpe"]))
    # named reference panels
    named = {"U56": (px56, src["u_all"]), "B136": (pxb, [c for c in pxb.columns if c != "SPY"]),
             "BSTK100": (pxb, src["b_stk"]), "ETF36": (pxb, src["b_etf"]),
             "SMALL": (pxs, src["s_stk"])}
    for tag, (pxn, cols) in named.items():
        px = pxn[list(cols) + (["SPY"] if "SPY" in pxn.columns else [])].copy()
        if "SPY" not in px.columns:
            px["SPY"] = pxb["SPY"].reindex(px.index).ffill()
        px = px.dropna(how="all").ffill()
        st = px.index[260]
        sp = px["SPY"].pct_change().fillna(0).loc[st:]
        v2r = mrow(run_net(px, v2_weights).loc[st:])
        for n in NS:
            r = run_net(px, cand_weights(n)).loc[st:]
            m = mrow(r); s5 = slacks5(r, sp)
            rows.append(dict(kind="named", panel=tag, q=np.nan, draw=np.nan, n=n,
                             k_small=len(cols), k_large=0, **m,
                             **{f"s_{b}": s5[b] for b in BARS5},
                             pass4b=all(v >= 0 for v in s5.values()), pass4a=pass4a(m, v2r),
                             v2_S=v2r["Sharpe"], v2_H1=v2r["H1"], v2_H2=v2r["H2"],
                             v2_DD=v2r["MaxDD"], v2_OOS_S=v2r["OOS_Sharpe"],
                             spy_S=metrics(sp)["Sharpe"], spy_CAGR=metrics(sp)["CAGR"],
                             spy_DD=metrics(sp)["MaxDD"],
                             spy_OOS_S=metrics(sp.loc[OOS_START:])["Sharpe"]))
    G = pd.DataFrame(rows)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    mix = G[G.kind == "mix"]

    curve_rows = []
    for n in NS:
        sub = mix[mix.n == n]
        g = sub.groupby("q")
        rate = {b: (g[f"s_{b}"].apply(lambda x: float((x >= 0).mean()))) for b in BARS5}
        joint = g.pass4b.mean(); joint4a = g.pass4a.mean()
        mean_sl = {b: g[f"s_{b}"].mean() for b in BARS5}
        sd_sl = {b: sub[f"s_{b}"].std() for b in BARS5}         # one noise unit per leg
        P(f"\n-- CAND{n}: per-q PASS RATE of each 4b leg ({N_DRAWS} draws per rung) --")
        tab = pd.DataFrame({b: rate[b] for b in BARS5})   # leg pass rates, one column each
        tab["4b joint"] = joint; tab["4a"] = joint4a
        # mean book metrics get distinct names so they cannot overwrite the CAGR LEG column
        tab["mSharpe"] = g.Sharpe.mean(); tab["mCAGR"] = g.CAGR.mean(); tab["mMaxDD"] = g.MaxDD.mean()
        P(tab.to_string(float_format=lambda x: f"{x:.3f}"))
        P(f"\n-- CAND{n}: per-q MEAN SLACK per leg, in that leg's own cross-draw sd "
          f"(sd: {', '.join(f'{b} {sd_sl[b]:.4f}' for b in BARS5)}) --")
        z = pd.DataFrame({b: mean_sl[b] / sd_sl[b] for b in BARS5})
        P(z.to_string(float_format=lambda x: f"{x:+.2f}"))
        for q in QS:
            curve_rows.append(dict(n=n, q=q, **{f"rate_{b}": rate[b][q] for b in BARS5},
                                   **{f"z_{b}": mean_sl[b][q] / sd_sl[b] for b in BARS5},
                                   rate_4b=joint[q], rate_4a=joint4a[q]))
        P(f"\n-- CAND{n}: WHERE EACH LEG FIRST BINDS --")
        bind = []
        for b in BARS5:
            bind.append(dict(leg=b, first_below_1=first_binding(QS, rate[b], 1.0),
                             first_below_half=first_binding(QS, rate[b], 0.5),
                             rate_q0=rate[b][0.0], rate_q1=rate[b][1.0],
                             z_q0=mean_sl[b][0.0] / sd_sl[b], z_q1=mean_sl[b][1.0] / sd_sl[b]))
        bd = pd.DataFrame(bind).set_index("leg")
        P(bd.to_string(float_format=lambda x: f"{x:.3f}"))
        first = bd.first_below_1.dropna()
        if len(first):
            P(f"   FIRST leg to leave a perfect pass rate: "
              f"{', '.join(first[first == first.min()].index)} at q = {first.min():.2f}")
        firsth = bd.first_below_half.dropna()
        if len(firsth):
            P(f"   FIRST leg to fall below 50%: "
              f"{', '.join(firsth[firsth == firsth.min()].index)} at q = {firsth.min():.2f}")
        jb = first_binding(QS, joint, 1.0); jh = first_binding(QS, joint, 0.5)
        P(f"   joint 4b: first below 1.0 at q = {jb}, first below 0.5 at q = {jh}, "
          f"last q with any pass = "
          f"{max([q for q in QS if joint[q] > 0], default=None)}; total passes "
          f"{int(sub.pass4b.sum())}/{len(sub)}   4a {int(sub.pass4a.sum())}/{len(sub)}")
    pd.DataFrame(curve_rows).to_csv(f"{STEM}.curve.csv", index=False)

    # ---------------- PART B: monotonicity
    P("\n=== PART B: IS THE FOOTPRINT MONOTONE IN q? ===")
    mono_rows = []
    for n in NS:
        sub = mix[mix.n == n]
        joint = sub.groupby("q").pass4b.mean()
        d = joint.diff().dropna()
        viol = int((d > 1e-12).sum())
        rho_j = sub[["q", "pass4b"]].astype(float).corr(method="spearman").iloc[0, 1]
        P(f"\n CAND{n}: joint-4b pass rate by q, {viol} of {len(d)} steps INCREASE "
          f"(monotone non-increasing = {viol == 0});  Spearman(q, 4b) = {rho_j:+.4f}")
        P("   " + "  ".join(f"{q:.2f}:{joint[q]:.2f}" for q in QS))
        for b in BARS5:
            r_ = sub[["q", f"s_{b}"]].corr(method="spearman").iloc[0, 1]
            rr = sub.groupby("q")[f"s_{b}"].apply(lambda x: float((x >= 0).mean()))
            dv = int((rr.diff().dropna() > 1e-12).sum())
            mono_rows.append(dict(n=n, leg=b, spearman_q_slack=r_, rate_up_steps=dv,
                                  monotone=dv == 0))
            P(f"   leg {b:5s} Spearman(q, slack) {r_:+.4f}   rate-increasing steps {dv}/{len(d)}")
        mono_rows.append(dict(n=n, leg="4b joint", spearman_q_slack=rho_j,
                              rate_up_steps=viol, monotone=viol == 0))

    # which leg is the binding one, per q, in raw and in noise units
    P("\n=== PART B2: WHICH LEG IS CLOSEST TO BINDING, raw units vs noise units ===")
    bind_rows = []
    for n in NS:
        sub = mix[mix.n == n].copy()
        sd = {b: sub[f"s_{b}"].std() for b in BARS5}
        raw = sub[[f"s_{b}" for b in BARS5]].values
        zz = raw / np.array([sd[b] for b in BARS5])[None, :]
        sub["argmin_raw"] = [BARS5[i] for i in raw.argmin(axis=1)]
        sub["argmin_z"] = [BARS5[i] for i in zz.argmin(axis=1)]
        agree = float((sub.argmin_raw == sub.argmin_z).mean())
        P(f"\n CAND{n}: raw-unit argmin {dict(sub.argmin_raw.value_counts())}")
        P(f"          noise-unit argmin {dict(sub.argmin_z.value_counts())}   "
          f"the two units agree on {agree:.1%} of {len(sub)} cells")
        tabr = pd.crosstab(sub.q, sub.argmin_z)
        P("   noise-unit binding leg by q:")
        P(tabr.to_string())
        for q in QS:
            row = dict(n=n, q=q)
            for b in BARS5:
                row[f"raw_{b}"] = int((sub[sub.q == q].argmin_raw == b).sum())
                row[f"z_{b}"] = int((sub[sub.q == q].argmin_z == b).sum())
            bind_rows.append(row)
    pd.DataFrame(bind_rows).to_csv(f"{STEM}.binding.csv", index=False)

    # ---------------- PART B3: is the wiggle real, and how sharp is a binding point?
    P("\n=== PART B3: IS THE NON-MONOTONICITY REAL, OR 12-DRAW BINOMIAL NOISE? ===")
    P("PAVA fits the best monotone NON-INCREASING pass-rate curve; then 2000 binomial")
    P("re-draws from that fit (12 per rung) say how many up-steps a TRULY monotone curve")
    P("would show at this sample size.  p = P(sim up-steps >= observed).")
    brng = np.random.default_rng(SEED + 1)
    b3 = []
    for n in NS:
        sub = mix[mix.n == n]
        series = {b: sub.groupby("q")[f"s_{b}"].apply(lambda x: float((x >= 0).mean()))
                  for b in BARS5}
        series["4b"] = sub.groupby("q").pass4b.mean()
        for lab, rate in series.items():
            y = rate.values.astype(float)
            fit = pava_decreasing(y)
            obs_up = int((np.diff(y) > 1e-12).sum())
            sims = brng.binomial(N_DRAWS, np.tile(fit, (2000, 1))) / N_DRAWS
            sim_up = (np.diff(sims, axis=1) > 1e-12).sum(axis=1)
            pval = float((sim_up >= obs_up).mean())
            maxdev = float(np.abs(y - fit).max())
            P(f"  CAND{n} {lab:5s}  observed up-steps {obs_up:2d}   monotone-fit sim "
              f"median {int(np.median(sim_up))} (p10 {int(np.percentile(sim_up,10))}, "
              f"p90 {int(np.percentile(sim_up,90))})   p = {pval:.3f}   "
              f"max|obs-fit| {maxdev:.3f}   "
              f"{'consistent with monotone' if pval > 0.05 else 'REJECTS monotone'}")
            b3.append(dict(n=n, leg=lab, obs_up=obs_up, sim_median=float(np.median(sim_up)),
                           p_monotone=pval, max_dev=maxdev))
    P(f"\n  binomial sd of a pass rate at {N_DRAWS} draws and p=0.5 is "
      f"{0.5/np.sqrt(N_DRAWS):.3f} — bigger than most single steps of the fitted curve, "
      f"which is why the LEVEL curve wiggles even where the trend does not.")

    P("\n  BOOTSTRAP on the binding points (resample the 12 draws within each rung, "
      "1000 reps): the q at which each leg's pass rate first falls below 0.5.")
    boot_rows = []
    for n in NS:
        sub = mix[mix.n == n]
        by_q = {q: sub[sub.q == q] for q in QS}
        for b in BARS5 + ["4b"]:
            col = "pass4b" if b == "4b" else f"s_{b}"
            vals = {q: (by_q[q][col].values if b == "4b" else (by_q[q][col].values >= 0))
                    for q in QS}
            point = first_binding(QS, {q: float(np.mean(vals[q])) for q in QS}, 0.5)
            draws = []
            for _ in range(1000):
                rr = {}
                for q in QS:
                    v = vals[q]
                    rr[q] = float(np.mean(brng.choice(v, size=len(v), replace=True)))
                fb = first_binding(QS, rr, 0.5)
                draws.append(np.nan if fb is None else fb)
            d = np.array(draws, float)
            fin = d[np.isfinite(d)]
            lo = float(np.percentile(fin, 10)) if len(fin) else np.nan
            hi = float(np.percentile(fin, 90)) if len(fin) else np.nan
            P(f"    CAND{n} {b:5s}  point q* = {point}   bootstrap p10-p90 "
              f"[{lo:.2f}, {hi:.2f}]   never binds in {int((~np.isfinite(d)).sum())}/1000 reps")
            boot_rows.append(dict(n=n, leg=b, q_first_below_half=point, boot_p10=lo,
                                  boot_p90=hi, never_binds=int((~np.isfinite(d)).sum())))
    pd.DataFrame(b3).merge(pd.DataFrame(boot_rows), on=["n", "leg"], how="outer") \
        .to_csv(f"{STEM}.monotone.csv", index=False)

    # ---------------- PART C: rule 8
    P("\n=== PART C: RULE 8 WALK-FORWARD ===")
    P("C1  Does the CURVE replicate?  Four-leg admissibility re-derived inside IS 2010-2016 "
      "and inside OOS 2017-2026 (the OOS leg is undefined inside a window).")
    wf_rows = []
    for n in NS:
        sub = mix[mix.n == n]
        for b in BARS4:
            ri = sub.groupby("q")[f"is_{b}"].apply(lambda x: float((x >= 0).mean()))
            ro = sub.groupby("q")[f"oos_{b}"].apply(lambda x: float((x >= 0).mean()))
            bi1, bo1 = first_binding(QS, ri, 1.0), first_binding(QS, ro, 1.0)
            bih, boh = first_binding(QS, ri, 0.5), first_binding(QS, ro, 0.5)
            rho = spearman(ri.values, ro.values)
            P(f"  CAND{n} leg {b:5s}  first<1.0 IS {bi1} / OOS {bo1}   "
              f"first<0.5 IS {bih} / OOS {boh}   Spearman(IS curve, OOS curve) {rho:+.4f}")
            wf_rows.append(dict(part="C1", n=n, leg=b, is_first_below_1=bi1,
                                oos_first_below_1=bo1, is_first_below_half=bih,
                                oos_first_below_half=boh, curve_spearman=rho))
        ji = sub.groupby("q").apply(
            lambda x: float((x[[f"is_{b}" for b in BARS4]] >= 0).all(axis=1).mean()),
            include_groups=False)
        jo = sub.groupby("q").apply(
            lambda x: float((x[[f"oos_{b}" for b in BARS4]] >= 0).all(axis=1).mean()),
            include_groups=False)
        rho = spearman(ji.values, jo.values)
        P(f"  CAND{n} JOINT 4-leg   first<1.0 IS {first_binding(QS, ji, 1.0)} / "
          f"OOS {first_binding(QS, jo, 1.0)}   first<0.5 IS {first_binding(QS, ji, 0.5)} / "
          f"OOS {first_binding(QS, jo, 0.5)}   Spearman(IS, OOS) {rho:+.4f}")
        P(f"      IS  " + "  ".join(f"{q:.2f}:{ji[q]:.2f}" for q in QS))
        P(f"      OOS " + "  ".join(f"{q:.2f}:{jo[q]:.2f}" for q in QS))
        wf_rows.append(dict(part="C1", n=n, leg="JOINT4",
                            is_first_below_1=first_binding(QS, ji, 1.0),
                            oos_first_below_1=first_binding(QS, jo, 1.0),
                            is_first_below_half=first_binding(QS, ji, 0.5),
                            oos_first_below_half=first_binding(QS, jo, 0.5),
                            curve_spearman=rho))

    P("\nC2  The book test: q chosen on IS 2010-2016 by argmax mean IS Sharpe, "
      "OOS 2017-2026 read once.")
    for n in NS:
        sub = mix[mix.n == n]
        is_by_q = sub.groupby("q").IS_Sharpe.mean()
        qstar = float(is_by_q.idxmax())
        sel = sub[sub.q == qstar]
        anchor = sub.OOS_Sharpe.mean()
        P(f"\n  CAND{n}: IS argmax q* = {qstar:.2f}  (IS Sharpe {is_by_q[qstar]:.4f}; "
          f"IS curve {', '.join(f'{q:.2f}:{is_by_q[q]:.3f}' for q in QS)})")
        P(f"    OOS at q*  CAGR {sel.OOS_CAGR.mean():.2%}  Sharpe {sel.OOS_Sharpe.mean():.4f}  "
          f"MaxDD {sel.OOS_MaxDD.mean():.2%}   (12 draws, sd of OOS Sharpe {sel.OOS_Sharpe.std():.4f})")
        P(f"    vs anchor (mean OOS Sharpe over all {len(QS)} rungs) {anchor:.4f}   "
          f"vs RULES v2 same-panel {sel.v2_OOS_S.mean():.4f}   vs SPY {sel.spy_OOS_S.mean():.4f}")
        beat_v2 = int((sel.OOS_Sharpe > sel.v2_OOS_S).sum())
        beat_spy = int((sel.OOS_Sharpe > sel.spy_OOS_S).sum())
        P(f"    draws beating RULES v2 OOS {beat_v2}/{len(sel)}   beating SPY OOS {beat_spy}/{len(sel)}")
        P(f"    4b passes at q* {int(sel.pass4b.sum())}/{len(sel)}   "
          f"4a passes {int(sel.pass4a.sum())}/{len(sel)}")
        # does the IS argmax pick the OOS argmax?
        oos_by_q = sub.groupby("q").OOS_Sharpe.mean()
        P(f"    OOS argmax q = {float(oos_by_q.idxmax()):.2f} (Sharpe {oos_by_q.max():.4f}); "
          f"Spearman(IS q-curve, OOS q-curve) = "
          f"{spearman(is_by_q.values, oos_by_q.values):+.4f}")
        wf_rows.append(dict(part="C2", n=n, leg="book", qstar=qstar,
                            IS_Sharpe=is_by_q[qstar], OOS_CAGR=sel.OOS_CAGR.mean(),
                            OOS_Sharpe=sel.OOS_Sharpe.mean(), OOS_MaxDD=sel.OOS_MaxDD.mean(),
                            anchor_OOS_Sharpe=anchor, v2_OOS_Sharpe=sel.v2_OOS_S.mean(),
                            spy_OOS_Sharpe=sel.spy_OOS_S.mean(), beat_v2=beat_v2,
                            beat_spy=beat_spy, pass4b=int(sel.pass4b.sum()),
                            pass4a=int(sel.pass4a.sum()),
                            oos_argmax_q=float(oos_by_q.idxmax())))
    pd.DataFrame(wf_rows).to_csv(f"{STEM}.walkforward.csv", index=False)

    # ---------------- named reference
    P("\n=== NAMED REFERENCE PANELS (not part of the sweep) ===")
    nm = G[G.kind == "named"]
    P(nm.set_index(["panel", "n"])[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                                    "spy_S", "v2_S", "pass4a", "pass4b"]]
      .to_string(float_format=lambda x: f"{x:.3f}"))

    P("\n=== TOTALS ===")
    P(f"mix cells {len(mix)}  4b {int(mix.pass4b.sum())}  4a {int(mix.pass4a.sum())}")
    P(f"named cells {len(nm)}  4b {int(nm.pass4b.sum())}  4a {int(nm.pass4a.sum())}")
    (Path(f"{STEM}.console.txt")).write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
