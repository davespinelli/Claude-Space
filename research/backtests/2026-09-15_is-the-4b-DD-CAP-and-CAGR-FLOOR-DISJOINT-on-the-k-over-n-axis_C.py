#!/usr/bin/env python3
"""Idea 887 — is the 4b DD CAP and CAGR FLOOR disjoint on the k/n axis, generally?

Idea 769's 576-book FIXK grid failed 4b on DD alone 200 times and on CAGR alone 156 times
with ZERO reachable overlap, and all three IS-only DD-capped selectors landed on 2-4% CAGR
books.  This run walks k/n on FIVE book families (769's FIXK arm was one construction on one
ranking statistic) and asks whether the two LEVEL legs of PROTOCOL 4b

    CAGR  >= 0.70 x SPY CAGR          (the floor)
    MaxDD >= 0.60 x SPY MaxDD         (the cap, both negative)

are ever SIMULTANEOUSLY satisfiable, and if so whether that cell is reachable by a selector
that only ever sees 2009-2016.

TUNED PARAMETERS (2, the queue's own): FAMILY x k/n (q).
REPORTED AXES (not tuned, every point published): panel {U56, B136, SMALL} x construction
{RESPREAD, DEGROSS} x gross {0.75, 0.95, 1.00} x cadence {W, M} x cost rung {0, 10, 25} bps.

Headline rung is PROTOCOL's: 10 bps, next-day execution (engine semantics).

Outputs (all committed):
  *.books.csv       every book x cost rung: CAGR/Sharpe/MaxDD full, halves, IS, OOS, leg flags
  *.legs.csv        per (panel, family, constr, gross, cadence): the q-sets Q_DD, Q_CAGR, overlap
  *.walkforward.csv rule-8: IS-only selectors, OOS read once
  *.gates.csv       gates, printed before any hypothesis is read
  *.console.txt     full console transcript
"""
import sys, json, hashlib, itertools, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + "." + ext)

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ---------------------------------------------------------------- fast backtest
_CTX = {}
def ctx(px, freq):
    """Per-(panel, cadence) invariants of engine.backtest, computed once."""
    key = (id(px), freq)
    if key in _CTX: return _CTX[key]
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)                      # C[i] = prod_{u<=i}(1+r_u)
    Cm = np.vstack([np.ones((1, N)), C])                    # Cm[i] = C[i-1], Cm[0] = 1
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    s_idx = np.maximum.accumulate(np.where(mask, np.arange(T), -1))
    base = Cm[s_idx]
    A = Cm[:T] / base                                       # ratio C[i-1]/C[s-1]  (day i, pre-return)
    A1 = C / base                                           # ratio C[i]/C[s-1]     (day i, post-return)
    _CTX[key] = (idx, T, N, s_idx, np.where(mask)[0], A, A1)
    return _CTX[key]


def fast_run(px, W, cost_bps=10.0, freq="W"):
    """Vectorised re-implementation of engine.backtest (identical semantics):
    weights decided at close t applied at t+1, drift between rebalances, cash leg at 0,
    turnover charged on the rebalance day.  Gated against engine.backtest in G0/G1/G2."""
    idx, T, N, s_idx, rb, A, A1 = ctx(px, freq)
    Wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    Wb = Wt[s_idx]                                          # weights in force on day i
    E = Wb.sum(axis=1)
    V = (Wb * A).sum(axis=1) + (1.0 - E)                    # book value entering day i (=1 at s)
    V1 = (Wb * A1).sum(axis=1) + (1.0 - E)                  # book value after day i
    port = V1 / V - 1.0
    # turnover: on each rebalance day, |new - drifted current|
    prev = np.zeros((T, N))
    ent = Wb[rb - 1] * A1[rb - 1] / np.where(V1[rb - 1] > 0, V1[rb - 1], 1.0)[:, None]
    prev[rb] = np.where((rb - 1 >= 0)[:, None], ent, 0.0)   # holdings entering the rebalance day
    turn = np.zeros(T)
    turn[rb] = np.abs(Wt[rb] - prev[rb]).sum(axis=1)
    port = port - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


def spear(a, b):
    """Spearman without scipy (pandas' own `method='spearman'` imports scipy)."""
    a = pd.Series(np.asarray(a, float)); b = pd.Series(np.asarray(b, float))
    m = a.notna() & b.notna()
    if m.sum() < 3: return np.nan
    return a[m].rank().corr(b[m].rank())


def mets(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252.0
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    dd = (eq / eq.cummax() - 1).min()
    vol = r.std() * np.sqrt(252)
    return cagr, (r.mean() * 252 / vol if vol else np.nan), dd


# ---------------------------------------------------------------- panels
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


# ---------------------------------------------------------------- families
def _md5u(seed, s):
    return int(hashlib.md5(f"{seed}|{s}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF

def signals(px):
    """Ranking statistics for the five families + the shared eligibility mask."""
    ma = px.rolling(200).mean()
    above = (px > ma) & px.notna()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    madist = px / ma - 1
    rev = -(px / px.shift(21) - 1)                       # short-term reversal: lowest 1m return first
    rnd = pd.DataFrame(np.random.default_rng(887).random(px.shape),   # deterministic: fixed seed, fixed shape
                       index=px.index, columns=px.columns)
    return above, dict(MOM=comp, MADIST=madist, VOLLO=-vol20, VOLHI=vol20, RAND=rnd)


def weights(px, above, stat, q, constr, gross):
    """k_t = max(1, round(q * n_elig_t)) names, equal weight.  The eligible set n_elig is the
    RANKABLE one: priced, above its 200d MA, AND carrying a finite ranking statistic that day.
    RESPREAD: each of the k gets gross/k   -> book always at full gross.
    DEGROSS : each of the k gets gross/n_e -> book exposure = gross * k/n_e, rest to CASH."""
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


# ---------------------------------------------------------------- grid
QS = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.70, 0.90, 1.00]
FAMS = ["MOM", "MADIST", "VOLLO", "VOLHI", "RAND"]
CONSTR = ["RESPREAD", "DEGROSS"]
GROSS = [0.75, 0.95, 1.00]
CADENCE = ["W", "M"]
RUNGS = [0, 10, 25]
SPLIT = "2017-01-01"


def main():
    t0 = time.time()
    pan = get_panels()
    say("# Idea 887 — is the 4b DD CAP and CAGR FLOOR disjoint on the k/n axis, generally?")
    say(f"# grid: {len(pan)} panels x {len(FAMS)} families x {len(QS)} q x {len(CONSTR)} constr "
        f"x {len(GROSS)} gross x {len(CADENCE)} cadence = "
        f"{len(pan)*len(FAMS)*len(QS)*len(CONSTR)*len(GROSS)*len(CADENCE)} books, "
        f"each at {len(RUNGS)} cost rungs; 2 tuned params (FAMILY x q).")

    # ---------------- gates, printed before any hypothesis is read
    gates = []
    gp = pan["U56"]
    above_g, sg = signals(gp)
    Wg = weights(gp, above_g, sg["MOM"], 0.30, "RESPREAD", 0.75)
    # engine.backtest emits NaN on exactly two warm-up days (its `w_target` is shift(1)ed, so
    # row 0 is NaN and the first rebalance's turnover differences against it); both sit ~250
    # trading days before the evaluation start.  The gate is read on the finite days and the
    # excluded count is printed.
    ref = backtest(gp, Wg, cost_bps=10, freq="W")
    fr, ft = fast_run(gp, Wg, 10, "W")
    fin = np.isfinite(ref["returns"].values)
    d0 = float(np.abs(ref["returns"].values[fin] - fr.values[fin]).max())
    gates.append(dict(gate=f"G0 fast_run vs engine.backtest (MOM q0.30 RESPREAD g0.75 W); "
                           f"{int((~fin).sum())} engine-NaN warm-up days excluded", value=d0, bar="< 1e-12",
                      passed=d0 < 1e-12))
    fint = np.isfinite(ref["turnover"].values)
    d0t = float(np.abs(ref["turnover"].values[fint] - ft.values[fint]).max())
    gates.append(dict(gate="G1 turnover fast_run vs engine.backtest", value=d0t, bar="< 1e-12", passed=d0t < 1e-12))
    Wb = rules_v2_weights(gp)
    rb_e = backtest(gp, Wb, cost_bps=10, freq="W")["returns"]
    rb_f, _ = fast_run(gp, Wb, 10, "W")
    fin2 = np.isfinite(rb_e.values)
    d1 = float(np.abs(rb_e.values[fin2] - rb_f.values[fin2]).max())
    gates.append(dict(gate="G2 fast_run vs engine.backtest on the LIVE book (RULES v2)", value=d1, bar="< 1e-12",
                      passed=d1 < 1e-12))
    # G3: at q=1.00 RESPREAD == DEGROSS by construction (k = n_e)
    w1 = weights(gp, above_g, sg["MOM"], 1.00, "RESPREAD", 0.75)
    w2 = weights(gp, above_g, sg["MOM"], 1.00, "DEGROSS", 0.75)
    d2 = float(np.abs(w1.values - w2.values).max())
    gates.append(dict(gate="G3 q=1.00 RESPREAD == DEGROSS (k == n_elig)", value=d2, bar="< 1e-12", passed=d2 < 1e-12))
    # G4: RESPREAD book exposure is exactly `gross` whenever anything is rankable-eligible
    okg = above_g & sg["MOM"].notna()
    e = w1.sum(axis=1)[okg.sum(axis=1) > 0]
    d3 = float(np.abs(e - 0.75).max())
    gates.append(dict(gate="G4 RESPREAD gross exact (on rankable-eligible days)", value=d3, bar="< 1e-12",
                      passed=d3 < 1e-12))
    # G5: DEGROSS exposure == gross * k/n_e
    wd = weights(gp, above_g, sg["MOM"], 0.30, "DEGROSS", 0.75)
    kk = (wd > 0).sum(axis=1).astype(float); ne = okg.sum(axis=1).astype(float)
    pred = 0.75 * kk / ne.replace(0, np.nan)
    d4 = float(np.abs((wd.sum(axis=1) - pred).dropna()).max())
    gates.append(dict(gate="G5 DEGROSS exposure == gross*k/n_elig", value=d4, bar="< 1e-12", passed=d4 < 1e-12))
    # G6: cost rungs are derivable (10 bps run == 0 bps run - turnover*10/1e4)
    r0, tu = fast_run(gp, Wg, 0, "W")
    d5 = float(np.abs((r0 - tu * 10 / 1e4) - fr).max())
    gates.append(dict(gate="G6 cost rungs derivable from the 0 bps path", value=d5, bar="< 1e-12", passed=d5 < 1e-12))
    G = pd.DataFrame(gates); G.to_csv(OUT("gates.csv"), index=False)
    say("\n## GATES (printed before any hypothesis is read)")
    say(G.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    say(f"GATES {int(G.passed.sum())} of {len(G)} PASS")

    # ---------------- comparands, per panel, on that panel's own window
    comps = {}
    for pn, px in pan.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        rv2, _ = fast_run(px, rules_v2_weights(px), 10, "W"); rv2 = rv2.loc[start:]
        rv1, _ = fast_run(px, rules_v1_weights(px), 10, "W"); rv1 = rv1.loc[start:]
        c = dict(start=start, spy=spy, v2=rv2, v1=rv1)
        for nm, r in (("SPY", spy), ("RULESv2", rv2), ("RULESv1", rv1)):
            cg, sh, dd = mets(r)
            h = len(r) // 2
            c[nm] = dict(CAGR=cg, Sharpe=sh, MaxDD=dd,
                         H1=mets(r.iloc[:h])[1], H2=mets(r.iloc[h:])[1],
                         IS=mets(r.loc[:SPLIT])[:], OOS=mets(r.loc[SPLIT:])[:])
        comps[pn] = c
    say("\n## COMPARANDS (10 bps, weekly, each panel's own window)")
    for pn, c in comps.items():
        say(f"  {pn}  [{c['start'].date()} .. {pan[pn].index[-1].date()}]")
        for nm in ("SPY", "RULESv2", "RULESv1"):
            m = c[nm]
            say(f"    {nm:8s} full {m['CAGR']:7.2%} / {m['Sharpe']:6.3f} / {m['MaxDD']:7.2%}"
                f"   halves {m['H1']:.3f}/{m['H2']:.3f}"
                f"   IS {m['IS'][0]:7.2%}/{m['IS'][1]:6.3f}/{m['IS'][2]:7.2%}"
                f"   OOS {m['OOS'][0]:7.2%}/{m['OOS'][1]:6.3f}/{m['OOS'][2]:7.2%}")
        s = c["SPY"]
        say(f"    -> 4b bars on {pn}: CAGR floor {0.70*s['CAGR']:.2%}, DD cap {0.60*s['MaxDD']:.2%};"
            f"  IS floor {0.70*s['IS'][0]:.2%} cap {0.60*s['IS'][2]:.2%};"
            f"  OOS floor {0.70*s['OOS'][0]:.2%} cap {0.60*s['OOS'][2]:.2%}")

    # ---------------- the grid  (re-uses a committed books.csv when it is already complete,
    # so the analysis below can be re-read without re-pricing; delete the file to force a re-run)
    rows = []
    n_expect = len(pan) * (len(FAMS) * len(QS) * len(CONSTR) * len(GROSS)
                           - len(FAMS) * len(GROSS)) * len(CADENCE) * len(RUNGS)
    if OUT("books.csv").exists():
        D0 = pd.read_csv(OUT("books.csv"))
        if len(D0) == n_expect:
            say(f"\n(re-using committed {OUT('books.csv').name}: {len(D0)} rows == expected {n_expect})")
            rows = D0.to_dict("records")
    for pn, px in ([] if rows else pan.items()):
        above, stats = signals(px)
        c = comps[pn]; start = c["start"]; spy = c["SPY"]
        for fam, q, constr, g in itertools.product(FAMS, QS, CONSTR, GROSS):
            if q == 1.00 and constr == "DEGROSS":
                continue                                   # identical to RESPREAD (G3)
            W = weights(px, above, stats[fam], q, constr, g)
            for cad in CADENCE:
                r0, tu = fast_run(px, W, 0.0, cad)
                r0 = r0.loc[start:]; tu = tu.loc[start:]
                for bps in RUNGS:
                    r = r0 - tu * bps / 1e4
                    cg, sh, dd = mets(r)
                    h = len(r) // 2
                    h1, h2 = mets(r.iloc[:h])[1], mets(r.iloc[h:])[1]
                    icg, ish, idd = mets(r.loc[:SPLIT])
                    ocg, osh, odd = mets(r.loc[SPLIT:])
                    leg_dd = dd >= 0.60 * spy["MaxDD"]
                    leg_cg = cg >= 0.70 * spy["CAGR"]
                    leg_sh = (h1 > spy["H1"]) and (h2 > spy["H2"]) and (osh > spy["OOS"][1])
                    b = c["RULESv2"]
                    rows.append(dict(panel=pn, family=fam, q=q, constr=constr, gross=g, cadence=cad, bps=bps,
                                     CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                                     IS_CAGR=icg, IS_Sharpe=ish, IS_MaxDD=idd,
                                     OOS_CAGR=ocg, OOS_Sharpe=osh, OOS_MaxDD=odd,
                                     turn_yr=tu.sum() / (len(r) / 252.0),
                                     leg_DD=leg_dd, leg_CAGR=leg_cg, leg_SHARPE=leg_sh,
                                     pass4b=bool(leg_dd and leg_cg and leg_sh),
                                     pass4a=bool(h1 > b["H1"] and h2 > b["H2"] and dd >= b["MaxDD"])))
        say(f"  [{time.time()-t0:6.1f}s] panel {pn} done ({sum(1 for x in rows if x['panel']==pn)} rows)")
    D = pd.DataFrame(rows)
    # numpy's bool `+` is logical OR, so an object-dtype flag column would reduce to True/False
    # under .sum() instead of counting.  Coerce every flag to a real bool dtype.
    for c in ("leg_DD", "leg_CAGR", "leg_SHARPE", "pass4b", "pass4a"):
        D[c] = D[c].astype(bool)
    D.to_csv(OUT("books.csv"), index=False)
    say(f"\n{len(D)} book-rows written ({len(D[D.bps==10])} books at the headline 10 bps rung)")

    D["both_level"] = D.leg_DD & D.leg_CAGR
    H = D[D.bps == 10].copy()

    # ---------------- THE ANSWER: leg sets on the k/n axis
    say("\n## 1. THE TWO LEVEL LEGS ON THE k/n AXIS (10 bps, headline rung)")
    legs = []
    for key, gdf in H.groupby(["panel", "family", "constr", "gross", "cadence"]):
        gdf = gdf.sort_values("q")
        qdd = sorted(gdf.loc[gdf.leg_DD, "q"].tolist())
        qcg = sorted(gdf.loc[gdf.leg_CAGR, "q"].tolist())
        both = sorted(set(qdd) & set(qcg))
        gap = np.nan
        if qdd and qcg and not both:
            gap = min(abs(a - b) for a in qdd for b in qcg)
        legs.append(dict(panel=key[0], family=key[1], constr=key[2], gross=key[3], cadence=key[4],
                         n_q=len(gdf), n_DD=len(qdd), n_CAGR=len(qcg), n_BOTH=len(both),
                         n_4b=int(gdf.pass4b.sum()), n_4a=int(gdf.pass4a.sum()),
                         q_DD=";".join(f"{x:g}" for x in qdd), q_CAGR=";".join(f"{x:g}" for x in qcg),
                         q_BOTH=";".join(f"{x:g}" for x in both), q_gap=gap))
    Lg = pd.DataFrame(legs); Lg.to_csv(OUT("legs.csv"), index=False)
    say(f"  slices (panel x family x constr x gross x cadence): {len(Lg)}")
    say(f"  DD leg alone reachable in {int((Lg.n_DD>0).sum())} slices; CAGR leg alone in {int((Lg.n_CAGR>0).sum())};"
        f"  BOTH at some q in {int((Lg.n_BOTH>0).sum())} slices")
    say(f"  book-level: DD leg {int(H.leg_DD.sum())}/{len(H)}, CAGR leg {int(H.leg_CAGR.sum())}/{len(H)},"
        f" BOTH LEVEL LEGS {int((H.leg_DD & H.leg_CAGR).sum())}/{len(H)},"
        f" full 4b {int(H.pass4b.sum())}/{len(H)}, 4a {int(H.pass4a.sum())}/{len(H)}")
    say(f"  769's own counts restated on this grid: DD-alone fail {int((H.leg_CAGR & ~H.leg_DD).sum())},"
        f" CAGR-alone fail {int((H.leg_DD & ~H.leg_CAGR).sum())},"
        f" both-fail {int((~H.leg_DD & ~H.leg_CAGR).sum())}")
    say("\n  slices where BOTH legs are satisfiable at some q (n_BOTH > 0):")
    hit = Lg[Lg.n_BOTH > 0]
    if len(hit) == 0:
        say("    NONE — the two legs are disjoint on the k/n axis in every slice.")
    else:
        say(hit.to_string(index=False))
    say("\n  where the two leg-sets sit on the q axis (median q of each set, by construction):")
    for constr in CONSTR:
        sub = Lg[Lg.constr == constr]
        md = [np.median([float(x) for x in s.split(";")]) for s in sub.q_DD if s]
        mc = [np.median([float(x) for x in s.split(";")]) for s in sub.q_CAGR if s]
        n_ov = int((sub.n_BOTH > 0).sum()); n_dis = int(((sub.n_DD > 0) & (sub.n_CAGR > 0) & (sub.n_BOTH == 0)).sum())
        say(f"    {constr:9s} DD-leg median q {np.median(md) if md else float('nan'):.3f} (n={len(md)}),"
            f"  CAGR-leg median q {np.median(mc) if mc else float('nan'):.3f} (n={len(mc)});"
            f"  slices with overlap {n_ov}/{len(sub)}, both-legs-reachable-but-DISJOINT {n_dis},"
            f"  median q-gap when disjoint {sub.loc[sub.n_BOTH == 0, 'q_gap'].median():.3f}")

    # monotonicity of each leg in q (the mechanism the queue nominated)
    say("\n## 2. IS THE DISJOINTNESS A MONOTONICITY FACT? (Spearman of each leg's statistic on q)")
    mon = []
    for key, gdf in H.groupby(["panel", "family", "constr", "gross", "cadence"]):
        gdf = gdf.sort_values("q")
        if len(gdf) < 4: continue
        mon.append(dict(panel=key[0], constr=key[2], gross=key[3],
                        rho_CAGR=spear(gdf["q"], gdf["CAGR"]),
                        rho_MaxDD=spear(gdf["q"], gdf["MaxDD"]),
                        rho_Sharpe=spear(gdf["q"], gdf["Sharpe"])))
    M = pd.DataFrame(mon)
    say(M.groupby(["constr", "gross"])[["rho_CAGR", "rho_MaxDD", "rho_Sharpe"]].median().to_string(
        float_format=lambda x: f"{x:+.3f}"))
    say("  (MaxDD is negative: rho_MaxDD > 0 means the drawdown SHRINKS as the book widens.)")
    say("  the two legs pull the SAME way on q when sign(rho_CAGR) == sign(rho_MaxDD) — count by construction:")
    for c in CONSTR:
        s = M[M.constr == c]
        agree = int((np.sign(s.rho_CAGR) == np.sign(s.rho_MaxDD)).sum())
        say(f"    {c:9s} {agree}/{len(s)} slices agree in sign  "
            f"(median rho_CAGR {s.rho_CAGR.median():+.3f}, rho_MaxDD {s.rho_MaxDD.median():+.3f})")

    # 2b. does the SIGNAL earn the pass, or the exposure? — every family against its own RAND twin
    say("\n## 2b. THE ZERO-SIGNAL CONTROL — every family against RAND at the SAME (panel,q,constr,gross,cadence)")
    key = ["panel", "q", "constr", "gross", "cadence"]
    rnd = H[H.family == "RAND"].set_index(key)
    ctl = []
    for fam in [f for f in FAMS if f != "RAND"]:
        s = H[H.family == fam].set_index(key)
        j = s.join(rnd, rsuffix="_R", how="inner")
        ctl.append(dict(family=fam, n=len(j),
                        win_Sharpe=float((j.Sharpe > j.Sharpe_R).mean()),
                        win_CAGR=float((j.CAGR > j.CAGR_R).mean()),
                        win_MaxDD=float((j.MaxDD > j.MaxDD_R).mean()),
                        d_Sharpe_med=float((j.Sharpe - j.Sharpe_R).median()),
                        d_CAGR_med=float((j.CAGR - j.CAGR_R).median()),
                        n_4b=int(j.pass4b.sum()), n_4b_RAND=int(j.pass4b_R.sum())))
    say(pd.DataFrame(ctl).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"  RAND's own 4b count at 10 bps: {int(H[H.family=='RAND'].pass4b.sum())} of {len(H[H.family=='RAND'])}")

    # ---------------- rule 8
    say("\n## 3. RULE 8 — parameters chosen on 2009-2016 ONLY, OOS 2017-2026 read once")
    say("  selectors, all pre-registered and IS-only over the (FAMILY x q) plane inside each")
    say("  (panel, constr, gross, cadence) slice:")
    say("    SEL-SHARPE  argmax IS Sharpe")
    say("    SEL-DDCAP   argmax IS CAGR s.t. IS MaxDD <= 0.60 x SPY IS MaxDD   (769's selector)")
    say("    SEL-4bIS    argmax IS Sharpe among cells clearing BOTH IS level legs (idea 712's")
    say("                bar-shaped oracle — reported as such, not as an honest selector)")
    say("    SEL-NULL    md5-seeded uniform pick over the same plane (zero-signal control)")
    wf = []
    for key, gdf in H.groupby(["panel", "constr", "gross", "cadence"]):
        pn = key[0]; c = comps[pn]; spy = c["SPY"]; b = c["RULESv2"]
        isfloor, iscap = 0.70 * spy["IS"][0], 0.60 * spy["IS"][2]
        picks = {}
        picks["SEL-SHARPE"] = gdf.loc[gdf.IS_Sharpe.idxmax()]
        sub = gdf[gdf.IS_MaxDD >= iscap]
        picks["SEL-DDCAP"] = sub.loc[sub.IS_CAGR.idxmax()] if len(sub) else None
        sub2 = gdf[(gdf.IS_MaxDD >= iscap) & (gdf.IS_CAGR >= isfloor)]
        picks["SEL-4bIS"] = sub2.loc[sub2.IS_Sharpe.idxmax()] if len(sub2) else None
        j = int(_md5u(887, f"null|{key}") * len(gdf)) % len(gdf)
        picks["SEL-NULL"] = gdf.iloc[j]
        for sn, p in picks.items():
            if p is None:
                wf.append(dict(panel=pn, constr=key[1], gross=key[2], cadence=key[3], selector=sn,
                               family="(empty)", q=np.nan)); continue
            wf.append(dict(panel=pn, constr=key[1], gross=key[2], cadence=key[3], selector=sn,
                           family=p.family, q=p.q,
                           IS_CAGR=p.IS_CAGR, IS_Sharpe=p.IS_Sharpe, IS_MaxDD=p.IS_MaxDD,
                           OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                           OOS_leg_DD=p.OOS_MaxDD >= 0.60 * spy["OOS"][2],
                           OOS_leg_CAGR=p.OOS_CAGR >= 0.70 * spy["OOS"][0],
                           OOS_leg_SHARPE=p.OOS_Sharpe > spy["OOS"][1],
                           OOS_4b=bool(p.OOS_MaxDD >= 0.60 * spy["OOS"][2] and p.OOS_CAGR >= 0.70 * spy["OOS"][0]
                                       and p.OOS_Sharpe > spy["OOS"][1]),
                           beat_SPY_OOS_Sharpe=p.OOS_Sharpe > spy["OOS"][1],
                           beat_LIVE_OOS_Sharpe=p.OOS_Sharpe > b["OOS"][1],
                           full_4b=bool(p.pass4b), full_4a=bool(p.pass4a)))
    WF = pd.DataFrame(wf)
    for c in ("OOS_leg_DD", "OOS_leg_CAGR", "OOS_leg_SHARPE", "OOS_4b",
              "beat_SPY_OOS_Sharpe", "beat_LIVE_OOS_Sharpe", "full_4b", "full_4a"):
        WF[c] = WF[c].map(lambda v: bool(v) if v is not None and v == v else None)
    WF.to_csv(OUT("walkforward.csv"), index=False)
    nb = lambda col: int(col.fillna(False).astype(bool).sum())   # count, never numpy-bool OR
    for sn, s in WF.groupby("selector"):
        s2 = s.dropna(subset=["OOS_Sharpe"])
        if not len(s2):
            say(f"  {sn:11s} n={len(s)} all empty"); continue
        say(f"  {sn:11s} n={len(s):3d} (empty {int(s.family.eq('(empty)').sum())})"
            f"  OOS 4b {nb(s2.OOS_4b)}/{len(s2)}"
            f"  | OOS legs DD {nb(s2.OOS_leg_DD)} CAGR {nb(s2.OOS_leg_CAGR)} SHARPE {nb(s2.OOS_leg_SHARPE)}"
            f"  | beats SPY OOS Sharpe {nb(s2.beat_SPY_OOS_Sharpe)}"
            f", beats LIVE {nb(s2.beat_LIVE_OOS_Sharpe)}"
            f"  | median OOS CAGR {s2.OOS_CAGR.median():.2%} Sharpe {s2.OOS_Sharpe.median():.3f}"
            f" MaxDD {s2.OOS_MaxDD.median():.2%}")
    say("\n  every rule-8 pick (all points, no selection on the OOS window):")
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- cost rungs
    say("\n## 4. COST RUNGS (the whole grid, both level legs and the full 4b verdict)")
    for bps in RUNGS:
        S = D[D.bps == bps]
        say(f"  {bps:2d} bps: DD {int(S.leg_DD.sum()):5d}  CAGR {int(S.leg_CAGR.sum()):5d}"
            f"  BOTH-LEVEL {int(S.both_level.sum()):5d}  4b {int(S.pass4b.sum()):4d}"
            f"  4a {int(S.pass4a.sum()):4d}   of {len(S)}"
            f"   | RESPREAD BOTH-LEVEL {int(S[S.constr=='RESPREAD'].both_level.sum()):4d},"
            f" DEGROSS {int(S[S.constr=='DEGROSS'].both_level.sum()):4d}")

    # ---------------- per-family / per-panel decomposition
    say("\n## 5. WHERE THE BOTH-LEVEL CELLS LIVE (10 bps)")
    AGG = dict(n=("q", "size"), DD=("leg_DD", "sum"), CAGR=("leg_CAGR", "sum"),
               BOTH_LEVEL=("both_level", "sum"), p4b=("pass4b", "sum"), p4a=("pass4a", "sum"))
    say(H.groupby(["panel", "family"]).agg(**AGG).to_string())
    say("\n  by construction x gross:")
    say(H.groupby(["constr", "gross"]).agg(**AGG).to_string())
    say("\n  by construction x q (the axis the idea names):")
    say(H.groupby(["constr", "q"]).agg(**AGG).to_string())

    bl = H[H.both_level]
    say(f"\n  WHERE ON THE q AXIS the overlap sits: of {len(bl)} BOTH-LEVEL books,"
        f" {int((bl.q >= 0.7).sum())} are at q >= 0.7 and {int((bl.q <= 0.3).sum())} at q <= 0.3"
        f" (median q {bl.q.median():.2f});"
        f" the q-axis itself is {QS[0]}..{QS[-1]}.")
    say(f"  gross of the BOTH-LEVEL books: " +
        ", ".join(f"g{g:.2f} {int((bl.gross==g).sum())}" for g in GROSS))
    say(f"\n  the {len(bl)} BOTH-LEVEL books at 10 bps (before the Sharpe legs are applied):")
    if len(bl):
        say(bl[["panel", "family", "q", "constr", "gross", "cadence", "CAGR", "Sharpe", "MaxDD",
                "H1", "H2", "OOS_Sharpe", "pass4b", "pass4a"]].to_string(index=False,
                                                                         float_format=lambda x: f"{x:.4f}"))
    say(f"\n  the {int(H.pass4b.sum())} FULL 4b passes at 10 bps:")
    if int(H.pass4b.sum()):
        say(H[H.pass4b][["panel", "family", "q", "constr", "gross", "cadence", "CAGR", "Sharpe", "MaxDD",
                         "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turn_yr"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    say(f"\n[{time.time()-t0:.1f}s] done")
    OUT("console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
