#!/usr/bin/env python3
"""Idea 1741 (lane cloud, 2026-09-20): is the BAND'S DRAWDOWN CREDIT a CONSTANT OF THE
CONSTRUCTION rather than a result?

1632 found the 200d-band book's MaxDD advantage over its REALISED-GROSS-MATCHED de-gross twin
is near panel-invariant and flat in name count above N=56 (c=0.03: U56 +4.34 pp, B136 +5.93,
SMALL +6.45), while the CAGR cost is a ~3x PANEL effect.  If the DD credit is a constant of the
construction, every committed per-panel band DD claim in the record is ONE number quoted many
times.

Test: hold the construction fixed (band c = 0.03, gated weight to CASH, next-day execution) and
vary what CANNOT change a constant -- PANEL, NAME COUNT, CADENCE, COST RUNG, GROSS -- then score
the credit's spread against its OWN PAIRED BLOCK-BOOTSTRAP SE.  Then ask the constructive half:
does a single scalar closed form in (realised gate-out rate, realised vol) reproduce it?

TUNED PARAMETERS (max 2, per PROTOCOL rule 4): PANEL AXIS and BLOCK LENGTH.  Everything else
(N, cadence, gross, cost) is a reported grid axis, every point published.

Protocol: 10 bps headline costs, next-day execution (engine), both KEEP paths at every cell,
rule-8 walk-forward with 2017-2026 read ONCE.  Offline, deterministic, seed 20260920.

SURVIVORSHIP: U56 / B136 are CURRENT constituents; SMALL is a CURRENT sub-$2B screen with the
house filter (data/small_meta.csv max_1d_move >= 1.0 dropped).  The headline is a WITHIN-CELL
paired contrast (band minus its own matched twin on the same names) and is first-order immune;
the 4a/4b pass COUNTS are not.
"""
import sys, itertools, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask, metrics   # noqa: E402

SEED      = 20260920
BAND      = 0.03          # the construction, HELD FIXED
WARMUP    = 260
IS_END    = "2016-12-31"
OOS_START = "2017-01-01"
COSTS     = [0, 10, 25, 50]
GROSSES   = [0.50, 0.75, 1.00]
CADENCES  = ["W", "M", "Q"]
NDRAWS    = 5
BLOCKS    = [21, 63]      # tuned parameter 2
NBOOT     = 500
OUT       = Path(__file__).with_suffix(".txt")
_log_lines = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); _log_lines.append(s)

# ---------------------------------------------------------------- panels (tuned parameter 1)
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    return px[keep]

def panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}

# ---------------------------------------------------------------- vectorised engine replay
def bt_np(px, w, freq):
    """numpy replay of engine.backtest at cost 0, returning (returns, turnover, gross).
    Gated against engine.backtest in G1."""
    P = px.values
    R = np.nan_to_num(px.pct_change().values, nan=0.0)
    W = np.nan_to_num(w.reindex(px.index).values, nan=0.0)
    W = np.vstack([np.zeros((1, W.shape[1])), W[:-1]])                    # decided t, applied t+1
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(P)
    cur = np.zeros(P.shape[1]); held = np.empty_like(R); turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = W[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1.0 + R[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    rets = (held * R).sum(axis=1)
    return (pd.Series(rets, index=px.index), pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index))

def net(r0, turn, cost_bps):
    return r0 - turn * cost_bps / 1e4

def mets(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    dd = (eq / eq.cummax() - 1).min()
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=cagr, Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd, Vol=vol)

def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]

# ---------------------------------------------------------------- books
def eq_weights(px, cols, gross):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    e[cols] = px[cols].notna().astype(float)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

_BS = {}
def bs_of(pname, px):
    """band_state(px, BAND) cached per panel — the construction, computed once."""
    if pname not in _BS: _BS[pname] = band_state(px, BAND)
    return _BS[pname]

def band_book(px, cols, gross, freq, bs):
    return bt_np(px, eq_weights(px, cols, gross).where(bs, 0.0), freq)

def twin_matched(px, cols, freq, target_gross, tol=1e-6):
    """Plain de-gross twin (no band) re-scaled so its REALISED mean gross matches the band
    book's, by secant on nominal gross.  Returns (r0, turn, gross_series, g_nominal, gap)."""
    def run(g):
        r0, t, gs = bt_np(px, eq_weights(px, cols, g), freq)
        return r0, t, gs, gs.iloc[WARMUP:].mean()
    g0 = target_gross; r0, t0, s0, m0 = run(g0)
    if abs(m0 - target_gross) < tol: return r0, t0, s0, g0, abs(m0 - target_gross)
    g1 = g0 * (target_gross / m0); r1, t1, s1, m1 = run(g1)
    for _ in range(4):
        if abs(m1 - target_gross) < tol: break
        denom = (m1 - m0)
        g2 = g1 - (m1 - target_gross) * (g1 - g0) / denom if denom else g1
        g0, m0 = g1, m1
        g1 = float(np.clip(g2, 1e-4, 2.0)); r1, t1, s1, m1 = run(g1)
    return r1, t1, s1, g1, abs(m1 - target_gross)

# ---------------------------------------------------------------- run
def main():
    rng = np.random.default_rng(SEED)
    PX = panels()
    log("# Idea 1741 — is the band's drawdown credit a CONSTANT OF THE CONSTRUCTION?")
    log(f"# seed {SEED} | band c={BAND} | warm-up {WARMUP} rows | IS<= {IS_END} | OOS>= {OOS_START}")
    for k, v in PX.items():
        log(f"# panel {k}: {v.shape[1]} columns, {v.index[0].date()} -> {v.index[-1].date()}")

    # ---- G1: local bt_np replays engine.backtest exactly -------------------------------
    g1dev = 0.0
    for name in ("U56", "B136"):
        px = PX[name]
        w = rules_v2_weights(px, BAND, 0.75)
        st = px.index[WARMUP]
        a = bt_np(px, w, "W")[0].loc[st:]
        b = engine_backtest(px, w, cost_bps=0.0, freq="W")["returns"].loc[st:]
        g1dev = max(g1dev, float(np.abs(a.values - b.values).max()))
    log(f"G1  local bt_np vs engine.backtest max|d| = {g1dev:.3e}  ->  {'PASS' if g1dev < 1e-12 else 'FAIL'}")

    # ---- baselines --------------------------------------------------------------------
    base = {}
    for name, px in PX.items():
        st = px.index[WARMUP]
        r0, t0, _ = bt_np(px, rules_v2_weights(px, BAND, 0.75), "W")
        spy = px["SPY"].pct_change().fillna(0.0)
        base[name] = dict(px=px, start=st, r0=r0.loc[st:], t0=t0.loc[st:], spy=spy.loc[st:])
    for name, b in base.items():
        for c in COSTS:
            m = mets(net(b["r0"], b["t0"], c)); b[f"live{c}"] = m
        b["spym"] = mets(b["spy"])
        b["spym_oos"] = mets(b["spy"].loc[OOS_START:])
        b["live10_oos"] = mets(net(b["r0"], b["t0"], 10).loc[OOS_START:])
        log(f"# {name}: RULES v2 (live, 10bps) {b['live10']['CAGR']:.2%}/{b['live10']['Sharpe']:.4f}/"
            f"{b['live10']['MaxDD']:.2%} | SPY {b['spym']['CAGR']:.2%}/{b['spym']['Sharpe']:.4f}/{b['spym']['MaxDD']:.2%}"
            f" | SPY OOS {b['spym_oos']['CAGR']:.2%}/{b['spym_oos']['Sharpe']:.4f}/{b['spym_oos']['MaxDD']:.2%}")

    # ---- the grid ---------------------------------------------------------------------
    rows, keep_paired = [], {}
    for pname, px in PX.items():
        # SPY is a CONSTITUENT of U56 / B136 (the record's convention) but only a BENCHMARK on
        # the small panel (data/SMALL_PANEL_README.md), so it is excluded there.
        cols = [c for c in px.columns if not (pname == "SMALL" and c == "SPY")]
        FULL = len(cols)
        bh1, bh2 = {}, {}
        for c in COSTS:
            bh1[c], bh2[c] = halves(net(base[pname]["r0"], base[pname]["t0"], c))
        sh1, sh2 = halves(base[pname]["spy"])
        Ns = sorted({20, 40, FULL})
        st = base[pname]["start"]
        for N in Ns:
            draws = [np.array(cols)] if N >= FULL else [
                rng.choice(cols, size=N, replace=False) for _ in range(NDRAWS)]
            for di, sub in enumerate(draws):
                sub = list(sub)
                inband = bs_of(pname, px)[sub]
                priced = px[sub].notna()
                gate_out = float((1.0 - (inband & priced).sum(axis=1).div(
                    priced.sum(axis=1).replace(0, np.nan))).loc[st:].mean())
                for freq, gross in itertools.product(CADENCES, GROSSES):
                    br0, bt_, bg = band_book(px, sub, gross, freq, bs_of(pname, px))
                    gb = bg.loc[st:].mean()
                    tr0, tt_, tg, gnom, gap = twin_matched(px, sub, freq, gb)
                    br0, bt_, tr0, tt_ = br0.loc[st:], bt_.loc[st:], tr0.loc[st:], tt_.loc[st:]
                    for c in COSTS:
                        rb, rt = net(br0, bt_, c), net(tr0, tt_, c)
                        mb, mt = mets(rb), mets(rt)
                        b1, b2 = halves(rb)
                        mb_oos = mets(rb.loc[OOS_START:]); mb_is = mets(rb.loc[:IS_END])
                        mt_oos = mets(rt.loc[OOS_START:])
                        L, S = base[pname][f"live{c}"], base[pname]["spym"]
                        So = base[pname]["spym_oos"]
                        p4a = (b1 > bh1[c] and b2 > bh2[c] and mb["MaxDD"] >= L["MaxDD"])
                        p4b_full = (b1 > sh1 and b2 > sh2
                                    and mb["MaxDD"] >= 0.60 * S["MaxDD"] and mb["CAGR"] >= 0.70 * S["CAGR"])
                        p4b_oos = (mb_oos["Sharpe"] > So["Sharpe"] and mb_oos["MaxDD"] >= 0.60 * So["MaxDD"]
                                   and mb_oos["CAGR"] >= 0.70 * So["CAGR"])
                        rows.append(dict(panel=pname, N=N, draw=di, freq=freq, gross=gross, cost=c,
                                         gate_out=gate_out, gross_real=gb, gross_gap=gap, g_twin=gnom,
                                         band_CAGR=mb["CAGR"], band_Sharpe=mb["Sharpe"], band_MaxDD=mb["MaxDD"],
                                         band_H1=b1, band_H2=b2, band_vol=mb["Vol"],
                                         twin_CAGR=mt["CAGR"], twin_Sharpe=mt["Sharpe"], twin_MaxDD=mt["MaxDD"],
                                         credit_pp=100 * (mb["MaxDD"] - mt["MaxDD"]),
                                         dSharpe=mb["Sharpe"] - mt["Sharpe"],
                                         dCAGR_pp=100 * (mb["CAGR"] - mt["CAGR"]),
                                         is_Sharpe=mb_is["Sharpe"], is_CAGR=mb_is["CAGR"], is_MaxDD=mb_is["MaxDD"],
                                         oos_CAGR=mb_oos["CAGR"], oos_Sharpe=mb_oos["Sharpe"], oos_MaxDD=mb_oos["MaxDD"],
                                         is_credit_pp=100 * (mb_is["MaxDD"] - mets(rt.loc[:IS_END])["MaxDD"]),
                                         oos_credit_pp=100 * (mb_oos["MaxDD"] - mt_oos["MaxDD"]),
                                         keep4a=p4a, keep4b_full=p4b_full, keep4b_oos=p4b_oos))
                    if N >= FULL and freq == "W":
                        keep_paired[(pname, gross)] = (br0, bt_, bt_, tt_, tr0)
        log(f"# grid done: {pname} ({len(rows)} rows so far)")

    df = pd.DataFrame(rows)
    df.to_csv(Path(__file__).with_name(Path(__file__).stem + "_grid.csv"), index=False)
    log(f"G2  realised-gross match band vs twin: max gap = {df.gross_gap.max():.3e}"
        f"  ->  {'PASS' if df.gross_gap.max() < 1e-4 else 'FAIL'}")
    log(f"G3  grid rows = {len(df)}  (panels {df.panel.nunique()} x N x draws x cadence x gross x cost)")

    # ---- replication of 1632's anchor -------------------------------------------------
    log("\n## REPLICATION — 1632's anchor (c=0.03, full panel, weekly, 10 bps)")
    anc = df[(df.N == df.groupby('panel').N.transform('max')) & (df.freq == "W") &
             (df.cost == 10) & (df.gross == 0.75)]
    for _, r in anc.iterrows():
        log(f"  {r.panel:6s} credit = {r.credit_pp:+.2f} pp   (1632 published U56 +4.34 / B136 +5.93 / SMALL +6.45)")

    # ---- the headline: spread of the credit -------------------------------------------
    log("\n## THE CREDIT'S SPREAD ACROSS EVERY AXIS THAT CANNOT MOVE A CONSTANT")
    log(f"  ALL {len(df)} cells: mean {df.credit_pp.mean():+.2f} pp, sd {df.credit_pp.std():.2f}, "
        f"min {df.credit_pp.min():+.2f}, max {df.credit_pp.max():+.2f}, range {df.credit_pp.max()-df.credit_pp.min():.2f} pp")
    for ax in ("panel", "N", "freq", "gross", "cost"):
        g = df.groupby(ax).credit_pp.agg(["mean", "std", "min", "max"])
        log(f"  by {ax}:")
        for k, r in g.iterrows():
            log(f"     {ax}={k!s:>6s}  mean {r['mean']:+.2f}  sd {r['std']:.2f}  [{r['min']:+.2f}, {r['max']:+.2f}]")
    # within-axis spread holding everything else fixed
    for ax in ("panel", "N", "freq", "gross", "cost"):
        others = [c for c in ("panel", "N", "freq", "gross", "cost") if c != ax]
        sp = df.groupby(others + ["draw"]).credit_pp.agg(lambda x: x.max() - x.min())
        log(f"  WITHIN-cell spread moving only {ax:6s}: mean {sp.mean():.2f} pp, max {sp.max():.2f} pp")

    # ---- paired block bootstrap SE (tuned parameter 2) --------------------------------
    log("\n## PAIRED BLOCK-BOOTSTRAP SE OF THE CREDIT (anchor cells: full panel, W, gross 0.75, 10 bps)")
    def maxdd(r):
        eq = np.cumprod(1.0 + r); return float((eq / np.maximum.accumulate(eq) - 1).min())
    se_tbl = []
    for (pname, gross), (br0, bt_, _, tt_, tr0) in keep_paired.items():
        if gross != 0.75: continue
        rb = net(br0, bt_, 10).values; rt = net(tr0, tt_, 10).values
        point = 100 * (maxdd(rb) - maxdd(rt))
        for L in BLOCKS:
            rs = np.random.default_rng(SEED + L)
            nb = int(np.ceil(len(rb) / L)); draws = []
            for _ in range(NBOOT):
                starts = rs.integers(0, len(rb) - L, size=nb)
                idx = (starts[:, None] + np.arange(L)[None, :]).ravel()[:len(rb)]
                draws.append(100 * (maxdd(rb[idx]) - maxdd(rt[idx])))
            se = float(np.std(draws, ddof=1))
            se_tbl.append(dict(panel=pname, block=L, point=point, se=se))
            log(f"  {pname:6s} block={L:3d}  credit {point:+.2f} pp   paired SE {se:.2f} pp   t = {point/se:+.2f}")
    se_df = pd.DataFrame(se_tbl)
    ref_se = float(se_df.se.max())
    obs_sd = float(df.credit_pp.std())
    log(f"  >> observed cross-cell SD {obs_sd:.2f} pp vs largest paired SE {ref_se:.2f} pp "
        f"(ratio {obs_sd/ref_se:.2f}) -> {'THE SPREAD EXCEEDS THE NOISE: NOT A CONSTANT' if obs_sd > ref_se else 'INSIDE ITS OWN NOISE: CONSTANT-COMPATIBLE'}")

    # ---- the constructive half: a scalar closed form ----------------------------------
    log("\n## DOES A SCALAR CLOSED FORM IN (GATE-OUT RATE, VOL) REPRODUCE THE CREDIT?")
    d10 = df[df.cost == 10]
    def ols(X, y):
        cols = [np.asarray(c, float) for c in X]
        X = np.column_stack([np.ones(len(cols[0]))] + cols)
        beta, *_ = np.linalg.lstsq(X, np.asarray(y, float), rcond=None)
        pred = X @ beta; ss = ((y - y.mean()) ** 2).sum()
        return beta, 1 - ((y - pred) ** 2).sum() / ss
    for label, X in [("gate_out alone", [d10.gate_out]),
                     ("vol alone", [d10.band_vol]),
                     ("gate_out + vol", [d10.gate_out, d10.band_vol]),
                     ("gate_out x vol (product)", [d10.gate_out * d10.band_vol]),
                     ("gate_out + vol + gross", [d10.gate_out, d10.band_vol, d10.gross])]:
        beta, r2 = ols(X, d10.credit_pp.values)
        log(f"  {label:26s} R2 = {r2:+.4f}   beta = {np.round(beta,3).tolist()}")
    for p in d10.panel.unique():
        s = d10[d10.panel == p]
        _, r2 = ols([s.gate_out, s.band_vol], s.credit_pp.values)
        log(f"     within {p:6s}: R2(gate_out+vol) = {r2:+.4f}  (credit sd {s.credit_pp.std():.2f} pp)")

    # ---- both KEEP paths at every cell -------------------------------------------------
    log("\n## BOTH KEEP PATHS, EVERY CELL (band books; 4a vs live RULES v2, 4b vs SPY)")
    log(f"  4a FULL      : {int(df.keep4a.sum())} of {len(df)}")
    log(f"  4b FULL      : {int(df.keep4b_full.sum())} of {len(df)}")
    log(f"  4b OOS       : {int(df.keep4b_oos.sum())} of {len(df)}")
    both = df.keep4b_full & df.keep4b_oos
    log(f"  4b FULL & OOS: {int(both.sum())} of {len(df)}")
    for c in COSTS:
        s = df[df.cost == c]
        log(f"     cost {c:2d} bps: 4a {int(s.keep4a.sum()):3d} | 4b FULL {int(s.keep4b_full.sum()):3d} | "
            f"4b OOS {int(s.keep4b_oos.sum()):3d} | BOTH {int((s.keep4b_full & s.keep4b_oos).sum()):3d}  (of {len(s)})")
    for p in df.panel.unique():
        s = df[df.panel == p]
        log(f"     {p:6s}    : 4a {int(s.keep4a.sum()):3d} | 4b FULL {int(s.keep4b_full.sum()):3d} | "
            f"4b OOS {int(s.keep4b_oos.sum()):3d} | BOTH {int((s.keep4b_full & s.keep4b_oos).sum()):3d}  (of {len(s)})")
    if both.any():
        log("  4b FULL-and-OOS passers:")
        for _, r in df[both].iterrows():
            log(f"     {r.panel} N={r.N} draw={r.draw} {r.freq} g={r.gross} c={r.cost}bps  FULL "
                f"{r.band_CAGR:.2%}/{r.band_Sharpe:.4f}/{r.band_MaxDD:.2%}  OOS "
                f"{r.oos_CAGR:.2%}/{r.oos_Sharpe:.4f}/{r.oos_MaxDD:.2%}")
    # binding legs of 4b FULL
    S = {p: base[p]["spym"] for p in df.panel.unique()}
    fail = dict(H1=0, H2=0, DD=0, CAGR=0)
    for _, r in df.iterrows():
        s = S[r.panel]
        h1, h2 = halves(base[r.panel]["spy"])
        if not r.band_H1 > h1: fail["H1"] += 1
        if not r.band_H2 > h2: fail["H2"] += 1
        if not r.band_MaxDD >= 0.60 * s["MaxDD"]: fail["DD"] += 1
        if not r.band_CAGR >= 0.70 * s["CAGR"]: fail["CAGR"] += 1
    log(f"  4b FULL binding legs (fail counts of {len(df)}): {fail}")

    # ---- rule 8 walk-forward -----------------------------------------------------------
    log("\n## RULE 8 — dials chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE")
    d10 = df[df.cost == 10]
    picks = []
    for p in d10.panel.unique():
        s = d10[d10.panel == p]
        for cname, key in [("C_SHARPE", lambda x: x.is_Sharpe),
                           ("C_CALMAR", lambda x: x.is_CAGR / x.is_MaxDD.abs()),
                           ("C_CREDIT", lambda x: x.is_credit_pp)]:
            k = key(s); pick = s.loc[k.idxmax()]
            So = base[p]["spym_oos"]; Lo = base[p]["live10_oos"]
            ok4b = (pick.oos_Sharpe > So["Sharpe"] and pick.oos_MaxDD >= 0.60 * So["MaxDD"]
                    and pick.oos_CAGR >= 0.70 * So["CAGR"])
            ok4a = (pick.oos_Sharpe > Lo["Sharpe"] and pick.oos_MaxDD >= Lo["MaxDD"])
            picks.append(dict(panel=p, chooser=cname, N=pick.N, draw=pick.draw, freq=pick.freq,
                              gross=pick.gross, oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                              oos_MaxDD=pick.oos_MaxDD, oos_credit=pick.oos_credit_pp,
                              keep4a_oos=ok4a, keep4b_oos=ok4b))
            log(f"  {p:6s} {cname:9s} -> N={pick.N} {pick.freq} g={pick.gross} draw={pick.draw} | OOS "
                f"{pick.oos_CAGR:.2%}/{pick.oos_Sharpe:.4f}/{pick.oos_MaxDD:.2%} | credit OOS {pick.oos_credit_pp:+.2f} pp"
                f" | 4a {'PASS' if ok4a else 'fail'} 4b {'PASS' if ok4b else 'fail'}"
                f"   [live v2 OOS {Lo['CAGR']:.2%}/{Lo['Sharpe']:.4f}/{Lo['MaxDD']:.2%}; "
                f"SPY OOS {So['CAGR']:.2%}/{So['Sharpe']:.4f}/{So['MaxDD']:.2%}]")
    pk = pd.DataFrame(picks)
    pk.to_csv(Path(__file__).with_name(Path(__file__).stem + "_choosers.csv"), index=False)
    log(f"  >> picks clearing 4a OOS: {int(pk.keep4a_oos.sum())} of {len(pk)};"
        f" clearing 4b OOS: {int(pk.keep4b_oos.sum())} of {len(pk)}")

    # IS->OOS persistence of the credit itself
    r_is_oos = float(np.corrcoef(d10.is_credit_pp, d10.oos_credit_pp)[0, 1])
    log(f"  IS->OOS correlation of the CREDIT across {len(d10)} cells: rho = {r_is_oos:+.4f} "
        f"(IS mean {d10.is_credit_pp.mean():+.2f} pp, OOS mean {d10.oos_credit_pp.mean():+.2f} pp)")

    log("\n## SURVIVORSHIP CAVEAT")
    log("  U56 / B136 are CURRENT constituents; SMALL is a CURRENT sub-$2B screen, 54 names dropped at")
    log("  max_1d_move >= 1.0 (665 remain).  The credit is a WITHIN-CELL paired contrast on the SAME")
    log("  names and is first-order immune; the 4a/4b pass counts and the rule-8 picks are NOT.")
    OUT.write_text("\n".join(_log_lines) + "\n")

if __name__ == "__main__":
    main()
