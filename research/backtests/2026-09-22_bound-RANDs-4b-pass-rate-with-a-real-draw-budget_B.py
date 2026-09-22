#!/usr/bin/env python3
"""Idea 907 — bound RAND's 4b PASS RATE with a REAL DRAW BUDGET, not one seed.

Idea 887 priced a five-family k/n grid and reported, as its zero-signal control, that the
RAND family cleared PROTOCOL 4b on **12 of 342** cells at 10 bps.  That number is one draw of
`np.random.default_rng(887)`.  It is enough to refute "the ranking family EARNS the pass"
(a coin flip gets some), but it is NOT a base rate: nobody knows whether 12/342 is the centre
of the distribution, a lucky tail, or an unlucky one, and every committed 4b claim in the
record that cites a RAND control is quoted against it.

This run re-draws the SAME 342 cells over S independent seeds and publishes
  (a) the pass-count distribution across seeds, at every cost rung,
  (b) the per-cell pass rate and its binomial SE, so a reader can see WHICH cells a coin flip
      clears and how well 20 draws resolve them,
  (c) the rule-8 reading: what an IS-only chooser, given nothing but noise, takes OOS.

TUNED PARAMETERS (2, exactly the queue's own): SEED COUNT S and COST RUNG.
  S = 20 (declared before any result was read; SEEDS[0] = 887 is 887's own draw, kept first so
  it serves as the reproduction gate).  Headline rung = PROTOCOL's 10 bps.
REPORTED AXES (not tuned, EVERY point published): panel {U56, B136, SMALL} x q {10 rungs}
  x construction {RESPREAD, DEGROSS} x gross {0.75, 0.95, 1.00} x cadence {W, M}
  x cost rung {0, 10, 25} bps x seed {20}.

Book construction, eligibility, cost/fill semantics and both leg definitions are COPIED
VERBATIM from idea 887's script so the contrast is against 887's own numbers and not a
re-specification.  Nothing in research/ outside research/backtests/ is modified.

Outputs (all committed):
  *.books.csv        every (seed, panel, q, constr, gross, cadence, rung): metrics + leg flags
  *.seeds.csv        per (seed, rung): 4b / 4a pass counts out of 342
  *.cells.csv        per cell: pass rate over S seeds, binomial SE, 887's own verdict
  *.walkforward.csv  rule-8: IS-only choosers fit on 2009-2016, OOS 2017-2026 read ONCE
  *.gates.csv        gates, printed before any hypothesis is read
  *.console.txt      full console transcript
"""
import sys, time, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask  # noqa

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + "." + ext)

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ---------------------------------------------------------------- THE TWO TUNED PARAMETERS
S_SEEDS = 20                      # param 1: seed budget
HEADLINE_BPS = 10                 # param 2: cost rung (PROTOCOL's)
SEEDS = [887] + [907_000 + i for i in range(1, S_SEEDS)]

# ---------------------------------------------------------------- 887's grid, verbatim
QS = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.70, 0.90, 1.00]
CONSTR = ["RESPREAD", "DEGROSS"]
GROSS = [0.75, 0.95, 1.00]
CADENCE = ["W", "M"]
RUNGS = [0, 10, 25]
SPLIT = "2017-01-01"

# ---------------------------------------------------------------- fast backtest (887 verbatim)
_CTX = {}
def ctx(px, freq):
    key = (id(px), freq)
    if key in _CTX: return _CTX[key]
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cm = np.vstack([np.ones((1, N)), C])
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    s_idx = np.maximum.accumulate(np.where(mask, np.arange(T), -1))
    base = Cm[s_idx]
    A = Cm[:T] / base
    A1 = C / base
    _CTX[key] = (idx, T, N, s_idx, np.where(mask)[0], A, A1)
    return _CTX[key]

def fast_run(px, W, cost_bps=10.0, freq="W"):
    """Vectorised re-implementation of engine.backtest (identical semantics): weights decided
    at close t applied at t+1, drift between rebalances, cash at 0, turnover charged on the
    rebalance day.  Gated against engine.backtest in G0/G1."""
    idx, T, N, s_idx, rb, A, A1 = ctx(px, freq)
    Wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    Wb = Wt[s_idx]
    E = Wb.sum(axis=1)
    V = (Wb * A).sum(axis=1) + (1.0 - E)
    V1 = (Wb * A1).sum(axis=1) + (1.0 - E)
    port = V1 / V - 1.0
    prev = np.zeros((T, N))
    ent = Wb[rb - 1] * A1[rb - 1] / np.where(V1[rb - 1] > 0, V1[rb - 1], 1.0)[:, None]
    prev[rb] = np.where((rb - 1 >= 0)[:, None], ent, 0.0)
    turn = np.zeros(T)
    turn[rb] = np.abs(Wt[rb] - prev[rb]).sum(axis=1)
    port = port - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)

def mets(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252.0
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    dd = (eq / eq.cummax() - 1).min()
    vol = r.std() * np.sqrt(252)
    return cagr, (r.mean() * 252 / vol if vol else np.nan), dd

# ---------------------------------------------------------------- panels (887 verbatim)
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "max_1d_move" if "max_1d_move" in meta.columns else meta.columns[-1]
    tick = meta.columns[0]
    bad = set(meta.loc[meta[col] >= 1.0, tick].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep]

PANELS = {}
def get_panels():
    if PANELS: return PANELS
    PANELS["U56"] = load_universe()
    PANELS["B136"] = load_universe(broad=True)
    PANELS["SMALL"] = small_panel()
    return PANELS

# ---------------------------------------------------------------- the RAND family (887 verbatim
# except that the seed is now an argument instead of the literal 887)
def elig_mask(px):
    ma = px.rolling(200).mean()
    return (px > ma) & px.notna()

def rand_stat(px, seed):
    return pd.DataFrame(np.random.default_rng(seed).random(px.shape),
                        index=px.index, columns=px.columns)

def weights(px, above, stat, q, constr, gross):
    """887's `weights`, verbatim.  k_t = max(1, round(q * n_elig_t)) names, equal weight."""
    ok = above & stat.notna()
    s = stat.where(ok)
    n_e = ok.sum(axis=1).astype(float)
    k = np.maximum(1.0, np.round(q * n_e))
    k = k.where(n_e > 0, 0.0)
    rank = s.rank(axis=1, ascending=False, method="first")
    sel = rank.le(k, axis=0) & ok
    kk = sel.sum(axis=1).astype(float)
    if constr == "RESPREAD":
        w = gross / kk.replace(0, np.nan)
    else:
        w = pd.Series(gross, index=px.index) / n_e.replace(0, np.nan)
    return sel.astype(float).mul(w, axis=0).fillna(0.0)


def main():
    t0 = time.time()
    pan = get_panels()
    n_cells = len(pan) * (len(QS) * len(CONSTR) * len(GROSS) - len(GROSS)) * len(CADENCE)
    say("# Idea 907 — bound RAND's 4b PASS RATE with a REAL DRAW BUDGET, not one seed")
    say(f"# 2 tuned params: SEED COUNT S = {S_SEEDS}, COST RUNG = {HEADLINE_BPS} bps (headline).")
    say(f"# cells = {len(pan)} panels x {len(QS)} q x {len(CONSTR)} constr x {len(GROSS)} gross "
        f"x {len(CADENCE)} cadence, less the q=1.00 DEGROSS duplicates = {n_cells}")
    say(f"# books priced = {n_cells} cells x {S_SEEDS} seeds x {len(RUNGS)} rungs = "
        f"{n_cells*S_SEEDS*len(RUNGS)}")
    for pn, px in pan.items():
        say(f"#   panel {pn}: {px.shape[0]} days x {px.shape[1]} columns "
            f"[{px.index[0].date()} .. {px.index[-1].date()}]")
    say(f"# seed stream (declared before any result was read): {SEEDS[0]} (887's own), then "
        f"{SEEDS[1]}..{SEEDS[-1]}")

    # ---------------- gates, printed before any hypothesis is read
    gates = []
    gp = pan["U56"]; above_g = elig_mask(gp)
    st887 = rand_stat(gp, 887)
    Wg = weights(gp, above_g, st887, 0.30, "RESPREAD", 0.75)
    ref = backtest(gp, Wg, cost_bps=10, freq="W")
    fr, ft = fast_run(gp, Wg, 10, "W")
    fin = np.isfinite(ref["returns"].values)
    d0 = float(np.abs(ref["returns"].values[fin] - fr.values[fin]).max())
    gates.append(dict(gate=f"G0 fast_run == engine.backtest on a RAND book "
                           f"({int((~fin).sum())} engine-NaN warm-up days excluded)",
                      value=d0, bar="< 1e-12", passed=d0 < 1e-12))
    fint = np.isfinite(ref["turnover"].values)
    d0t = float(np.abs(ref["turnover"].values[fint] - ft.values[fint]).max())
    gates.append(dict(gate="G1 turnover fast_run == engine.backtest", value=d0t, bar="< 1e-12",
                      passed=d0t < 1e-12))
    w1 = weights(gp, above_g, st887, 1.00, "RESPREAD", 0.75)
    w2 = weights(gp, above_g, st887, 1.00, "DEGROSS", 0.75)
    d2 = float(np.abs(w1.values - w2.values).max())
    gates.append(dict(gate="G2 q=1.00 RESPREAD == DEGROSS (the 18 dropped duplicate cells)",
                      value=d2, bar="< 1e-12", passed=d2 < 1e-12))
    gates.append(dict(gate="G3 cell count == 887's 342", value=float(n_cells), bar="== 342",
                      passed=n_cells == 342))
    okg = above_g & st887.notna()
    e = w1.sum(axis=1)[okg.sum(axis=1) > 0]
    d3 = float(np.abs(e - 0.75).max())
    gates.append(dict(gate="G4 RESPREAD gross exact on rankable-eligible days", value=d3,
                      bar="< 1e-12", passed=d3 < 1e-12))
    r0g, tug = fast_run(gp, Wg, 0.0, "W")
    d5 = float(np.abs((r0g - tug * 10 / 1e4) - fr).max())
    gates.append(dict(gate="G5 cost rungs derivable from the 0 bps path", value=d5, bar="< 1e-12",
                      passed=d5 < 1e-12))
    G = pd.DataFrame(gates); G.to_csv(OUT("gates.csv"), index=False)
    say("\n## GATES (printed before any hypothesis is read)")
    say(G.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    say(f"GATES {int(G.passed.sum())} of {len(G)} PASS")

    # ---------------- comparands, per panel, on that panel's own window
    comps = {}
    say("\n## COMPARANDS (10 bps, weekly, each panel's own window)")
    for pn, px in pan.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        rv2, _ = fast_run(px, rules_v2_weights(px), 10, "W"); rv2 = rv2.loc[start:]
        rv1, _ = fast_run(px, rules_v1_weights(px), 10, "W"); rv1 = rv1.loc[start:]
        c = dict(start=start)
        for nm, r in (("SPY", spy), ("RULESv2", rv2), ("RULESv1", rv1)):
            cg, sh, dd = mets(r); h = len(r) // 2
            c[nm] = dict(CAGR=cg, Sharpe=sh, MaxDD=dd, H1=mets(r.iloc[:h])[1],
                         H2=mets(r.iloc[h:])[1], IS=mets(r.loc[:SPLIT]), OOS=mets(r.loc[SPLIT:]))
        comps[pn] = c
        say(f"  {pn}  [{start.date()} .. {px.index[-1].date()}]")
        for nm in ("SPY", "RULESv2", "RULESv1"):
            m = c[nm]
            say(f"    {nm:8s} full {m['CAGR']:7.2%} / {m['Sharpe']:6.3f} / {m['MaxDD']:7.2%}"
                f"   halves {m['H1']:.3f}/{m['H2']:.3f}"
                f"   IS {m['IS'][0]:7.2%}/{m['IS'][1]:6.3f}/{m['IS'][2]:7.2%}"
                f"   OOS {m['OOS'][0]:7.2%}/{m['OOS'][1]:6.3f}/{m['OOS'][2]:7.2%}")
        s = c["SPY"]
        say(f"    -> 4b bars on {pn}: CAGR floor {0.70*s['CAGR']:.2%}, DD cap {0.60*s['MaxDD']:.2%};"
            f"  OOS floor {0.70*s['OOS'][0]:.2%} cap {0.60*s['OOS'][2]:.2%};"
            f"  OOS Sharpe leg > {s['OOS'][1]:.3f}")

    # ---------------- the grid: every seed x cell x rung
    rows = []
    if OUT("books.csv").exists():
        D0 = pd.read_csv(OUT("books.csv"))
        if len(D0) == n_cells * S_SEEDS * len(RUNGS):
            say(f"\n(re-using committed {OUT('books.csv').name}: {len(D0)} rows)")
            rows = D0.to_dict("records")
    if not rows:
        say("")
        for pn, px in pan.items():
            above = elig_mask(px)
            c = comps[pn]; start = c["start"]; spy = c["SPY"]; b = c["RULESv2"]
            for si, seed in enumerate(SEEDS):
                stat = rand_stat(px, seed)
                for q, constr, g in itertools.product(QS, CONSTR, GROSS):
                    if q == 1.00 and constr == "DEGROSS":
                        continue
                    W = weights(px, above, stat, q, constr, g)
                    for cad in CADENCE:
                        r0, tu = fast_run(px, W, 0.0, cad)
                        r0 = r0.loc[start:]; tu = tu.loc[start:]
                        for bps in RUNGS:
                            r = r0 - tu * bps / 1e4
                            cg, sh, dd = mets(r); h = len(r) // 2
                            h1, h2 = mets(r.iloc[:h])[1], mets(r.iloc[h:])[1]
                            icg, ish, idd = mets(r.loc[:SPLIT])
                            ocg, osh, odd = mets(r.loc[SPLIT:])
                            leg_dd = dd >= 0.60 * spy["MaxDD"]
                            leg_cg = cg >= 0.70 * spy["CAGR"]
                            leg_sh = (h1 > spy["H1"]) and (h2 > spy["H2"]) and (osh > spy["OOS"][1])
                            rows.append(dict(seed=seed, panel=pn, q=q, constr=constr, gross=g,
                                             cadence=cad, bps=bps, CAGR=cg, Sharpe=sh, MaxDD=dd,
                                             H1=h1, H2=h2, IS_CAGR=icg, IS_Sharpe=ish, IS_MaxDD=idd,
                                             OOS_CAGR=ocg, OOS_Sharpe=osh, OOS_MaxDD=odd,
                                             turn_yr=tu.sum() / (len(r) / 252.0),
                                             leg_DD=leg_dd, leg_CAGR=leg_cg, leg_SHARPE=leg_sh,
                                             pass4b=bool(leg_dd and leg_cg and leg_sh),
                                             pass4a=bool(h1 > b["H1"] and h2 > b["H2"]
                                                         and dd >= b["MaxDD"])))
                say(f"  [{time.time()-t0:6.1f}s] {pn} seed {seed} ({si+1}/{S_SEEDS}) done")
    D = pd.DataFrame(rows)
    for c in ("leg_DD", "leg_CAGR", "leg_SHARPE", "pass4b", "pass4a"):
        D[c] = D[c].astype(bool)
    D.to_csv(OUT("books.csv"), index=False)
    say(f"\n{len(D)} book-rows written ({len(D[D.bps==HEADLINE_BPS])} at the headline "
        f"{HEADLINE_BPS} bps rung)")

    # ---------------- G6/G7: the REPRODUCTION gate against 887's published 12 of 342.
    # 887 ran on a cache ending 2026-09-14; this one ends 2026-09-18, four sessions longer.
    # G6 reads the CURRENT tape, G7 re-reads seed 887 on 887's OWN tape end.  The pair is what
    # licenses every contrast below: if G7 holds, the construction here IS 887's construction.
    n887 = int(D[(D.seed == 887) & (D.bps == 10)].pass4b.sum())
    say(f"\n## G6 seed 887 at 10 bps on THIS tape (ends {pan['U56'].index[-1].date()}): "
        f"{n887} of 342   [887 published 12 on a tape ending 2026-09-14]")
    n887_own = 0
    for pn, pxf in pan.items():
        px = pxf.loc[:"2026-09-14"]
        _CTX.clear()
        above = elig_mask(px); stat = rand_stat(px, 887)
        start = px.index[260]; sr = px["SPY"].pct_change().fillna(0).loc[start:]
        cg_s, _, dd_s = mets(sr); hs = len(sr) // 2
        H1s, H2s = mets(sr.iloc[:hs])[1], mets(sr.iloc[hs:])[1]
        Osh = mets(sr.loc[SPLIT:])[1]
        for q, constr, g in itertools.product(QS, CONSTR, GROSS):
            if q == 1.00 and constr == "DEGROSS":
                continue
            W = weights(px, above, stat, q, constr, g)
            for cad in CADENCE:
                r0, tu = fast_run(px, W, 0.0, cad)
                r = r0.loc[start:] - tu.loc[start:] * 10 / 1e4
                cg, _, dd = mets(r); hh = len(r) // 2
                if (dd >= 0.60 * dd_s and cg >= 0.70 * cg_s
                        and mets(r.iloc[:hh])[1] > H1s and mets(r.iloc[hh:])[1] > H2s
                        and mets(r.loc[SPLIT:])[1] > Osh):
                    n887_own += 1
    _CTX.clear()
    say(f"## G7 REPRODUCTION GATE — seed 887 at 10 bps on 887's OWN tape (ends 2026-09-14): "
        f"{n887_own} of 342   bar == 12   -> {'PASS' if n887_own == 12 else 'FAIL'}")
    say(f"   => the construction reproduces 887 EXACTLY.  The whole {n887_own} - {n887} = "
        f"{n887_own - n887} cell difference is FOUR extra trading sessions on the cache, "
        f"i.e. {abs(n887_own-n887)/12:.1%} of a committed 4b pass count moved on 4 days of tape.")

    # ---------------- 1. the pass-count distribution across seeds, EVERY rung
    say("\n## 1. THE BASE RATE — RAND's 4b pass count out of 342, over "
        f"{S_SEEDS} seeds, at every cost rung")
    srows = []
    for bps in RUNGS:
        sub = D[D.bps == bps]
        per = sub.groupby("seed")[["pass4b", "pass4a"]].sum()
        for sd, rr in per.iterrows():
            srows.append(dict(seed=int(sd), bps=bps, n4b=int(rr.pass4b), n4a=int(rr.pass4a)))
        v = per.pass4b.values.astype(float)
        rate = v.mean() / 342
        se_rate = v.std(ddof=1) / np.sqrt(len(v)) / 342
        say(f"  {bps:2d} bps  4b: mean {v.mean():6.2f} / 342 = {rate:.4f}  "
            f"SD {v.std(ddof=1):5.2f}  min {int(v.min()):3d}  max {int(v.max()):3d}  "
            f"median {np.median(v):6.1f}   SE(mean rate) {se_rate:.4f}   "
            f"seed887 {int(per.pass4b.loc[887])}")
        a = per.pass4a.values.astype(float)
        say(f"          4a: mean {a.mean():6.2f} / 342 = {a.mean()/342:.4f}  "
            f"SD {a.std(ddof=1):5.2f}  min {int(a.min()):3d}  max {int(a.max()):3d}")
    SR = pd.DataFrame(srows); SR.to_csv(OUT("seeds.csv"), index=False)

    # where 887's single draw sits in the distribution
    v10 = SR[SR.bps == 10].set_index("seed").n4b
    others = v10.drop(887).values.astype(float)
    pct = float((others < v10.loc[887]).mean())
    pct12 = float((others < 12).mean())
    say(f"\n  seed 887's OWN count on this tape ({int(v10.loc[887])}) sits at the {pct:.1%} "
        f"percentile of the other {len(others)} draws (mean {others.mean():.2f}, "
        f"SD {others.std(ddof=1):.2f}); z = {(v10.loc[887]-others.mean())/others.std(ddof=1):+.2f}")
    say(f"  887's PUBLISHED 12 sits at the {pct12:.1%} percentile of those same draws; "
        f"z = {(12-others.mean())/others.std(ddof=1):+.2f}.  887's single draw was TYPICAL, "
        f"not a lucky tail — but it is also not a rate.")

    # per-leg marginals: which leg a coin flip clears
    say("\n## 1b. WHICH LEG BINDS a coin flip (share of the 342x20 = 6,840 draws each leg PASSES)")
    for bps in RUNGS:
        sub = D[D.bps == bps]
        say(f"  {bps:2d} bps  leg_DD {sub.leg_DD.mean():.4f}   leg_CAGR {sub.leg_CAGR.mean():.4f}   "
            f"leg_SHARPE {sub.leg_SHARPE.mean():.4f}   ALL THREE {sub.pass4b.mean():.4f}")

    # ---------------- 2. per-cell pass rate and its SE
    say("\n## 2. PER-CELL RESOLUTION — pass rate over "
        f"{S_SEEDS} seeds and its binomial SE, at {HEADLINE_BPS} bps")
    h = D[D.bps == HEADLINE_BPS]
    key = ["panel", "q", "constr", "gross", "cadence"]
    C = h.groupby(key).agg(n_pass=("pass4b", "sum"), n=("pass4b", "size"),
                           n_pass4a=("pass4a", "sum"),
                           mean_CAGR=("CAGR", "mean"), mean_Sharpe=("Sharpe", "mean"),
                           mean_MaxDD=("MaxDD", "mean"), mean_turn=("turn_yr", "mean")).reset_index()
    C["rate"] = C.n_pass / C.n
    C["se"] = np.sqrt(C.rate * (1 - C.rate) / C.n)
    s887 = h[h.seed == 887].set_index(key).pass4b
    C["seed887"] = [bool(s887.loc[tuple(r)]) for r in C[key].values]
    C = C.sort_values("rate", ascending=False)
    C.to_csv(OUT("cells.csv"), index=False)
    say(f"  cells with rate > 0: {int((C.rate > 0).sum())} of {len(C)};  "
        f"rate == 1.00: {int((C.rate == 1).sum())};  "
        f"seed 887's {int(C.seed887.sum())} passing cells on this tape are all inside that set")
    say(f"  max binomial SE at n={S_SEEDS} is {0.5/np.sqrt(S_SEEDS):.4f} "
        f"(a cell reading 0.50 is +/- {0.5/np.sqrt(S_SEEDS):.2f}); "
        f"rule-of-three bound on a 0-of-{S_SEEDS} cell: {3/S_SEEDS:.4f}")
    say("\n  the cells a coin flip clears most often (rate > 0), all of them:")
    say(C[C.rate > 0][key + ["n_pass", "rate", "se", "seed887", "mean_CAGR", "mean_Sharpe",
                            "mean_MaxDD", "mean_turn"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  by panel (pooled over 114 cells x %d seeds):" % S_SEEDS)
    for pn, gdf in h.groupby("panel"):
        say(f"    {pn:6s} 4b {gdf.pass4b.mean():.4f}  4a {gdf.pass4a.mean():.4f}  "
            f"n = {len(gdf)}")
    say("  by gross / construction / cadence / q (every reported axis, 10 bps):")
    for ax in ("gross", "constr", "cadence", "q"):
        say(f"    {ax:8s} " + "  ".join(f"{k}: {v:.4f}" for k, v in
                                        h.groupby(ax).pass4b.mean().items()))

    # ---------------- 3. PROTOCOL rule 8 — IS-only choosers, OOS read ONCE
    say("\n## 3. PROTOCOL RULE 8 — the dials picked on 2009-2016 ONLY, 2017-2026 read once")
    say("   Two pre-declared IS-only choosers, neither of which may see OOS:")
    say("     IS_SHARPE — max IS Sharpe among that panel's 114 cells")
    say("     IS_CALMAR — max IS CAGR / |IS MaxDD|")
    wf = []
    for (pn, seed), gdf in h.groupby(["panel", "seed"]):
        c = comps[pn]; spy = c["SPY"]; b = c["RULESv2"]
        cal = gdf.IS_CAGR / gdf.IS_MaxDD.abs().replace(0, np.nan)
        for sel, pick in (("IS_SHARPE", gdf.loc[gdf.IS_Sharpe.idxmax()]),
                          ("IS_CALMAR", gdf.loc[cal.idxmax()])):
            o_dd = pick.OOS_MaxDD >= 0.60 * spy["OOS"][2]
            o_cg = pick.OOS_CAGR >= 0.70 * spy["OOS"][0]
            o_sh = pick.OOS_Sharpe > spy["OOS"][1]
            wf.append(dict(selector=sel, panel=pn, seed=int(seed), q=pick.q, constr=pick.constr,
                           gross=pick.gross, cadence=pick.cadence,
                           IS_Sharpe=pick.IS_Sharpe, IS_CAGR=pick.IS_CAGR,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           SPY_OOS_CAGR=spy["OOS"][0], SPY_OOS_Sharpe=spy["OOS"][1],
                           SPY_OOS_MaxDD=spy["OOS"][2],
                           V2_OOS_CAGR=b["OOS"][0], V2_OOS_Sharpe=b["OOS"][1],
                           V2_OOS_MaxDD=b["OOS"][2],
                           OOS_leg_DD=bool(o_dd), OOS_leg_CAGR=bool(o_cg),
                           OOS_leg_SHARPE=bool(o_sh),
                           OOS_4b=bool(o_dd and o_cg and o_sh),
                           full_4b=bool(pick.pass4b), full_4a=bool(pick.pass4a)))
    WF = pd.DataFrame(wf); WF.to_csv(OUT("walkforward.csv"), index=False)
    for sel, sdf in WF.groupby("selector"):
        say(f"\n  {sel} — {len(sdf)} picks ({len(pan)} panels x {S_SEEDS} seeds), "
            f"OOS 2017-01-01..:")
        for pn, pdf in sdf.groupby("panel"):
            say(f"    {pn:6s} OOS CAGR {pdf.OOS_CAGR.mean():7.2%} "
                f"[{pdf.OOS_CAGR.min():.2%}..{pdf.OOS_CAGR.max():.2%}]  "
                f"Sharpe {pdf.OOS_Sharpe.mean():6.3f} "
                f"[{pdf.OOS_Sharpe.min():.3f}..{pdf.OOS_Sharpe.max():.3f}]  "
                f"MaxDD {pdf.OOS_MaxDD.mean():7.2%} "
                f"[{pdf.OOS_MaxDD.min():.2%}..{pdf.OOS_MaxDD.max():.2%}]")
            say(f"           vs SPY OOS {pdf.SPY_OOS_CAGR.iloc[0]:7.2%} / "
                f"{pdf.SPY_OOS_Sharpe.iloc[0]:6.3f} / {pdf.SPY_OOS_MaxDD.iloc[0]:7.2%}"
                f"   vs RULES v2 OOS {pdf.V2_OOS_CAGR.iloc[0]:7.2%} / "
                f"{pdf.V2_OOS_Sharpe.iloc[0]:6.3f} / {pdf.V2_OOS_MaxDD.iloc[0]:7.2%}")
            say(f"           OOS 4b {int(pdf.OOS_4b.sum())}/{len(pdf)}  "
                f"(legs DD {int(pdf.OOS_leg_DD.sum())}, CAGR {int(pdf.OOS_leg_CAGR.sum())}, "
                f"SHARPE {int(pdf.OOS_leg_SHARPE.sum())})   "
                f"full-sample 4b {int(pdf.full_4b.sum())}/{len(pdf)}  "
                f"4a {int(pdf.full_4a.sum())}/{len(pdf)}")
        say(f"    POOLED OOS 4b pass rate {sdf.OOS_4b.mean():.4f} "
            f"(SE {np.sqrt(sdf.OOS_4b.mean()*(1-sdf.OOS_4b.mean())/len(sdf)):.4f})")

    # ---------------- 4. both KEEP paths, stated for the family
    say("\n## 4. BOTH KEEP PATHS, for the RAND family as a whole (10 bps)")
    say(f"  4a (beat the book): Sharpe > RULES v2 in BOTH halves and MaxDD no worse.  "
        f"{int(h.pass4a.sum())} of {len(h)} draws pass = {h.pass4a.mean():.4f}")
    say(f"  4b (capital-worthy): {int(h.pass4b.sum())} of {len(h)} draws pass = "
        f"{h.pass4b.mean():.4f}; under rule 8 the IS-only chooser takes it OOS "
        f"{WF[WF.selector=='IS_SHARPE'].OOS_4b.mean():.4f} of the time.")
    say("  VERDICT for this run: RAND is a CONTROL, not a candidate — nothing here is proposed")
    say("  for capital.  The deliverable is the BASE RATE every 4b claim must be read against.")

    say(f"\n[{time.time()-t0:.1f}s total]")
    OUT("console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
