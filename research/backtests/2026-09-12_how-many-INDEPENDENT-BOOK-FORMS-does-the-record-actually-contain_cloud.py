#!/usr/bin/env python3
"""Idea 838 (cloud, 2026-09-12) - how-many-INDEPENDENT-BOOK-FORMS-does-the-record-actually-contain.

QUESTION (QUEUE idea 838, verbatim)
    Idea 837 found its 39-arm corpus is 14 families of 2.8 near-duplicate arms, so the cluster
    bootstrap widens every OOS-Sharpe interval across zero and the effective n is ~14 (iid band
    0.5341) however many rungs are added.  Census the record's committed constructors for genuinely
    distinct book FORMS (not dials), measure the pairwise return correlation between family
    representatives, and publish the number of independent forms as the ceiling on every future
    cross-book n.

WHAT IS MEASURED
    A FORM is a constructor: a function from a price panel to a target-weight path.  A DIAL is a
    scalar inside a form (gross, n, cadence).  Idea 837 counted families by NAME.  This file counts
    them by RETURN: two arms are the same form if their net daily return series correlate at or
    above a threshold.  The number of INDEPENDENT FORMS at threshold tau is the number of
    single-linkage clusters of the arm x arm correlation matrix; it is the ceiling on the n any
    cross-book statistic may claim, because members of one cluster are not independent draws.
    Reported beside it: the participation ratio n_eff = (sum lambda)^2 / sum lambda^2 of the same
    correlation matrix, which needs no threshold at all.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
    1. FORM SET (2)
         WIDE  20 arms - every constructor this record commits, DIALS INCLUDED (gross 1.00/0.75/
               0.375, n = 5/10/20, weekly vs monthly cadence).  This is the corpus shape idea 837
               had: arms, not forms.
         CORE  10 arms - one arm per constructor whose MECHANISM differs by construction (no two
               differ only in a scalar).  This is the record's own optimistic reading of its
               corpus.
    2. CORRELATION WINDOW (3)
         FULL     one correlation over the whole common sample
         IS       <= 2016-12-31 only (the rule-8 in-sample window)
         ROLL252  median over rolling 252-day windows (robust to one regime)
    2 x 3 x 3 panels = 18 cells, ALL reported.  Everything else is PINNED: 10 bps, t+1, weekly
    cadence (except the one cadence-dial arm), gross 0.75 (except the two gross-dial arms), MA 200d,
    band 3%, vol window 20d, momentum 12-1, correlation lookback 120d.

REPORTED, NEVER SELECTED
    THRESHOLD LADDER tau in {0.80, 0.85, 0.90, 0.925, 0.95, 0.975, 0.99} - every rung published;
    no rung is chosen, so tau is not a tuned parameter.
    PANEL - U56 (ETF/mega-cap), B136 (136 large caps), SMALL664 (sub-$2B).  All three published.
    SURVIVORSHIP: B136 and SMALL664 are CURRENT constituents (PROTOCOL rule 9); SMALL664 drops
    every ticker with max_1d_move >= 1.0 in data/small_meta.csv before anything else runs.

PRE-REGISTERED HYPOTHESES (written before any number below was read)
    H_CEIL   : the independent-form count at tau = 0.95 is BELOW idea 837's 14 on all three panels
               under WIDE - i.e. the record's arm corpus is not 14 independent things.
    H_DIAL   : a pure dial never makes a new form - every dial pair (EW gross 1.00/0.75/0.375;
               TOP20/TOP10/TOP5; LOWVOL20/LOWVOL10; TOP20 weekly/monthly) is in ONE cluster at
               tau = 0.95, on all three panels.
    H_WINDOW : the count is not a window artefact - it moves by at most 1 between FULL, IS and
               ROLL252 at fixed (panel, form set, tau).
    H_STABLE : rule 8 on the ANSWER - the partition fitted on IS reproduces out of sample; pair
               agreement between the IS partition and the OOS partition is >= 0.90 at every tau.
    H_ENS    : the one-arm-per-cluster equal-weight ensemble is not a free lunch - it fails
               PROTOCOL 4b out of sample on at least one panel.

GATES (printed BEFORE any new number is read)
    G1 engine     : vectorised runner vs products/backtester/engine.backtest, 3 books (one per
                    panel), max |return difference|                                     bar 1e-12
    G2 no leverage: max daily target gross over every arm and every ensemble              bar 1.0
    G3 determinism: every arm rebuilt twice, bit-identical returns                          bar 0
    G4 dial anchor: the two pure gross dials of EW_ALL (1.00 vs 0.375) are the SAME FORM by
                    construction; their measured correlation must be >= 0.99 or the clustering
                    instrument cannot see a duplicate it is handed                       bar 0.99

RULE 8 WALK-FORWARD (required, PROTOCOL rule 8)
    Partition FITTED on IS (<= 2016-12-31) returns at each tau; EVALUATED on OOS (>= 2017-01-01):
      (a) pair agreement between the IS partition and the partition the OOS window would give;
      (b) the IS-fitted one-arm-per-cluster ensemble (representative = first arm of the cluster in
          the fixed catalogue order - NEVER the best performer) run on the OOS window and scored
          against RULES v2 and SPY on BOTH KEEP paths.
    Every arm also carries its own full / H1 / H2 / OOS CAGR, Sharpe, MaxDD and both KEEP verdicts.

OUTPUTS
    ..._cloud.arms.csv  ..._cloud.clusters.csv  ..._cloud.walkforward.csv  ..._cloud.console.txt
"""
import sys, json, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STEM = Path(__file__).with_suffix("")
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

COST_BPS = 10.0
GROSS = 0.75
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
TAUS = [0.80, 0.85, 0.90, 0.925, 0.95, 0.975, 0.99]
WINDOWS = ["FULL", "IS", "ROLL252"]
FORMSETS = ["WIDE", "CORE"]

# ----------------------------------------------------------------- runner ---
def run(px, W, cost_bps=COST_BPS, freq="W"):
    """Vectorised twin of engine.backtest: target weights decided at t, applied at t+1, drift
    between rebalances, cost_bps per unit turnover.  Gated against the engine in G1."""
    rets = px.pct_change().fillna(0.0).to_numpy()
    w_t = W.reindex(px.index).fillna(0.0).shift(1).to_numpy()
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).to_numpy()
    n = len(px.index); cur = np.zeros(px.shape[1]); port = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = w_t[i]; to = np.abs(new - cur).sum(); cur = new.copy()
        else:
            to = 0.0
        port[i] = cur @ rets[i] - to * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(port, index=px.index)

# ------------------------------------------------------------ constructors ---
def _priced(px): return px.notna().astype(float)
def _ew(mask_df, g):
    c = mask_df.sum(axis=1).replace(0, np.nan)
    return (g * mask_df).div(c, axis=0).fillna(0.0)
def _topn(scores, n, g, priced):
    r = scores.where(priced > 0).rank(axis=1, ascending=False)
    return ((r <= n).astype(float) * (g / n)).fillna(0.0)
def _mom(px): return px.shift(21) / px.shift(252) - 1.0
def _vol20(px): return px.pct_change().rolling(20).std() * np.sqrt(252)
def _ma(px): return px > px.rolling(200).mean()
def _corr120(px):
    r = px.pct_change()
    idx = r.mean(axis=1)
    m, mi = r.rolling(120).mean(), idx.rolling(120).mean()
    cov = r.mul(idx, axis=0).rolling(120).mean() - m.mul(mi, axis=0)
    sd, sdi = r.rolling(120).std(ddof=0), idx.rolling(120).std(ddof=0)
    return cov.div(sd.mul(sdi, axis=0)).replace([np.inf, -np.inf], np.nan)

def _rand20(px, g, seed=0):
    """Deterministic null form: 20 names drawn without replacement from the priced set on each
    weekly rebalance date, seeded once.  Present so the census has a constructor with no signal."""
    rng = np.random.default_rng(seed)
    W = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    reb = rebalance_mask(px.index, "W")
    cols = np.arange(px.shape[1]); last = None
    ok = px.notna().to_numpy()
    for i, d in enumerate(px.index):
        if reb.iloc[i] or last is None:
            avail = cols[ok[i]]
            if len(avail) == 0: last = np.array([], dtype=int)
            else: last = rng.choice(avail, size=min(20, len(avail)), replace=False)
        if len(last): W.iloc[i, last] = g / len(last)
    return W

# catalogue: name -> (builder, cadence, mechanism-key, is_core)
def catalogue(px):
    p = _priced(px); mom = _mom(px); v20 = _vol20(px); ma = _ma(px); bs = band_state(px, 0.03)
    c120 = _corr120(px); rev = -(px / px.shift(20) - 1.0)
    invv = (1.0 / v20.clip(lower=0.08)).where(p > 0)
    C = {}
    C["EW_ALL"]       = (_ew(p, GROSS), "W", "EW", True)
    C["EW_G100"]      = (_ew(p, 1.00),  "W", "EW", False)
    C["EW_G0375"]     = (_ew(p, 0.375), "W", "EW", False)
    C["TOP20_MOM"]    = (_topn(mom, 20, GROSS, p), "W", "MOM", True)
    C["TOP10_MOM"]    = (_topn(mom, 10, GROSS, p), "W", "MOM", False)
    C["TOP5_MOM"]     = (_topn(mom,  5, GROSS, p), "W", "MOM", False)
    C["TOP20_MOM_M"]  = (_topn(mom, 20, GROSS, p), "M", "MOM", False)
    C["LOWVOL20"]     = (_topn(-v20, 20, GROSS, p), "W", "LOWVOL", True)
    C["LOWVOL10"]     = (_topn(-v20, 10, GROSS, p), "W", "LOWVOL", False)
    C["INVVOL_ALL"]   = ((GROSS * invv.div(invv.sum(axis=1), axis=0)).fillna(0.0), "W", "INVVOL", True)
    C["MA_RS"]        = (_ew(ma.astype(float).where(p > 0, 0.0), GROSS), "W", "MA_RS", True)
    C["MA_DG"]        = ((GROSS * ma.astype(float).where(p > 0, 0.0)).div(
                             p.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0), "W", "MA_DG", True)
    C["BAND_RS"]      = (_ew(bs.astype(float).where(p > 0, 0.0), GROSS), "W", "BAND_RS", False)
    C["BAND_DG_V2"]   = (rules_v2_weights(px), "W", "BAND_DG", True)
    C["VOLCAP_DG"]    = ((GROSS * (v20 < 0.60).astype(float).where(p > 0, 0.0)).div(
                             p.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0), "W", "VOLCAP", True)
    C["RULES_V1"]     = (rules_v1_weights(px), "W", "RULESV1", True)
    C["MOM_MA_DG"]    = ((_topn(mom, 20, GROSS, p) * ma.astype(float)).fillna(0.0), "W", "MOM_MA", False)
    C["REV20"]        = (_topn(rev, 20, GROSS, p), "W", "REV", True)
    C["CORRLO20"]     = (_topn(-c120, 20, GROSS, p), "W", "CORRLO", True)
    C["RAND20"]       = (_rand20(px, GROSS), "W", "RAND", False)
    return C

# ------------------------------------------------------------------ panels ---
def panels():
    P = {}
    P["U56"] = load_universe()
    P["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c not in bad]
    P["SMALL664"] = sm[keep]
    return P

def investable(px, panel):
    """SPY is a constituent of the ETF/large-cap panels (as in baseline) and a BENCHMARK ONLY on
    the small panel."""
    return px.drop(columns=["SPY"]) if panel == "SMALL664" else px

# ----------------------------------------------------------------- metrics ---
def stats(r):
    m = metrics(r); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def keep_paths(r, b, spy):
    """PROTOCOL rule 4.  4a vs RULES v2 (live), 4b vs SPY.  Halves on the FULL sample, OOS per
    rule 8."""
    h = len(r) // 2
    s1, s2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    b1, b2 = metrics(b.iloc[:h])["Sharpe"], metrics(b.iloc[h:])["Sharpe"]
    p1, p2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    dd_r, dd_b, dd_s = metrics(r)["MaxDD"], metrics(b)["MaxDD"], metrics(spy)["MaxDD"]
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    sO, pO = metrics(ro)["Sharpe"], metrics(so)["Sharpe"]
    cagr, cagr_s = metrics(r)["CAGR"], metrics(spy)["CAGR"]
    a = bool(s1 > b1 and s2 > b2 and dd_r >= dd_b)
    b4 = bool(s1 > p1 and s2 > p2 and sO > pO and dd_r >= 0.60 * dd_s and cagr >= 0.70 * cagr_s)
    return a, b4, dict(H1=s1, H2=s2, OOS_Sharpe=sO, b_H1=b1, b_H2=b2, spy_H1=p1, spy_H2=p2,
                       spy_OOS=pO, MaxDD=dd_r, spy_MaxDD=dd_s, CAGR=cagr, spy_CAGR=cagr_s)

# --------------------------------------------------------------- clustering ---
def clusters_at(C, names, tau):
    """Single linkage: arms joined if corr >= tau.  Returns list of sorted index lists."""
    k = len(names); parent = list(range(k))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(k):
        for j in range(i + 1, k):
            if C[i, j] >= tau:
                a, b = find(i), find(j)
                if a != b: parent[a] = b
    groups = {}
    for i in range(k): groups.setdefault(find(i), []).append(i)
    return sorted((sorted(v) for v in groups.values()), key=lambda g: g[0])

def label_vec(groups, k):
    lab = np.empty(k, dtype=int)
    for gi, g in enumerate(groups):
        for i in g: lab[i] = gi
    return lab

def pair_agreement(l1, l2):
    k = len(l1); same = 0; tot = 0
    for i in range(k):
        for j in range(i + 1, k):
            tot += 1; same += int((l1[i] == l1[j]) == (l2[i] == l2[j]))
    return same / tot if tot else np.nan

def n_eff_pr(C):
    lam = np.linalg.eigvalsh(C); lam = np.clip(lam, 0, None)
    return float(lam.sum() ** 2 / (lam ** 2).sum())

def corr_matrix(R, window):
    if window == "FULL": X = R
    elif window == "IS": X = R.loc[:IS_END]
    else:
        rc = R.rolling(252).corr()           # MultiIndex (date, arm) x arm
        med = rc.groupby(level=1).median()
        med = med.reindex(index=R.columns, columns=R.columns)
        M = med.to_numpy().copy(); np.fill_diagonal(M, 1.0)
        return M
    return X.corr().to_numpy()

# --------------------------------------------------------------------- run ---
def main():
    say("=" * 100)
    say("IDEA 838  how-many-INDEPENDENT-BOOK-FORMS-does-the-record-actually-contain   (cloud, 2026-09-12)")
    say("costs 10 bps | t+1 | weekly (one monthly cadence-dial arm) | gross 0.75 (two gross-dial arms)")
    say("=" * 100)

    P = panels()
    for k, v in P.items():
        say(f"panel {k:9s} cols={v.shape[1]:4d} rows={len(v):5d} {v.index[0].date()} .. {v.index[-1].date()}")
    say("SURVIVORSHIP: B136 and SMALL664 are CURRENT constituents only (PROTOCOL rule 9); SMALL664 has")
    say("already dropped every ticker with max_1d_move >= 1.0 in data/small_meta.csv.")

    arms_rows, clus_rows, wf_rows = [], [], []
    g1 = g2 = 0.0; g3_ok = True; g4 = {}
    RET, CAT = {}, {}

    for panel, px_raw in P.items():
        px = investable(px_raw, panel)
        start = px.index[260]
        spy_all = px_raw["SPY"].pct_change().fillna(0.0)
        C = catalogue(px); CAT[panel] = C
        base = run(px_raw if panel != "SMALL664" else px, rules_v2_weights(
            px_raw if panel != "SMALL664" else px), freq="W")
        R = {}
        for name, (W, freq, mech, core) in C.items():
            r = run(px, W, freq=freq)
            r2 = run(px, W, freq=freq)
            if not np.array_equal(r.to_numpy(), r2.to_numpy(), equal_nan=True): g3_ok = False
            g2 = max(g2, float(W.sum(axis=1).max()))
            R[name] = r.loc[start:]
        base = base.loc[start:]; spy = spy_all.loc[start:]
        RET[panel] = (pd.DataFrame(R), base, spy)

        # G1: one book per panel against the engine
        nm = "BAND_DG_V2"
        eng = engine_backtest(px, C[nm][0], cost_bps=COST_BPS, freq="W")["returns"]
        g1 = max(g1, float(np.abs(eng - run(px, C[nm][0])).max()))

        for name in C:
            r = R[name]
            cg, sh, dd = stats(r); ro = r.loc[OOS_START:]
            cgo, sho, ddo = stats(ro)
            a, b4, d = keep_paths(r, base, spy)
            arms_rows.append(dict(panel=panel, arm=name, mech=C[name][2], core=C[name][3],
                                  CAGR=cg, Sharpe=sh, MaxDD=dd, H1=d["H1"], H2=d["H2"],
                                  IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                  OOS_CAGR=cgo, OOS_Sharpe=sho, OOS_MaxDD=ddo,
                                  pass4a=a, pass4b=b4))

    # G4 dial anchor
    for panel in P:
        df = RET[panel][0]
        g4[panel] = float(np.corrcoef(df["EW_G100"], df["EW_G0375"])[0, 1])

    say("")
    say("GATES")
    say(f"  G1 engine vs vectorised runner  max|dret| = {g1:.3e}   bar 1e-12   "
        f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    say(f"  G2 no leverage                  max gross = {g2:.6f}    bar <= 1.0  "
        f"{'PASS' if g2 <= 1.0 + 1e-12 else 'FAIL'}")
    say(f"  G3 determinism                  rebuilt twice identical  {'PASS' if g3_ok else 'FAIL'}")
    say("  G4 dial anchor  corr(EW_G100, EW_G0375) = " +
        "  ".join(f"{k} {v:.6f}" for k, v in g4.items()) +
        f"   bar >= 0.99  {'PASS' if min(g4.values()) >= 0.99 else 'FAIL'}")

    # ------------------------------------------------------------- clusters ---
    say("")
    say("SECTION 1  INDEPENDENT FORMS  (all 18 cells x 7 tau rungs, every rung reported)")
    for panel in P:
        df, base, spy = RET[panel]
        for fs in FORMSETS:
            names = [n for n in df.columns if (CAT[panel][n][3] or fs == "WIDE")]
            sub = df[names]
            for win in WINDOWS:
                M = corr_matrix(sub, win)
                off = M[np.triu_indices(len(names), 1)]
                ne = n_eff_pr(M)
                counts = []
                for tau in TAUS:
                    g = clusters_at(M, names, tau)
                    counts.append(len(g))
                    clus_rows.append(dict(panel=panel, formset=fs, window=win, tau=tau,
                                          n_arms=len(names), n_forms=len(g), n_eff_pr=ne,
                                          mean_rho=float(np.nanmean(off)),
                                          max_rho=float(np.nanmax(off)),
                                          min_rho=float(np.nanmin(off)),
                                          partition="|".join(",".join(names[i] for i in c) for c in g)))
                say(f"  {panel:9s} {fs:4s} {win:7s} n_arms={len(names):2d} n_eff={ne:5.2f} "
                    f"mean_rho={np.nanmean(off):+.4f}  forms@tau " +
                    " ".join(f"{t:g}:{c}" for t, c in zip(TAUS, counts)))

    cl = pd.DataFrame(clus_rows)
    say("")
    say("  H_CEIL   (WIDE, tau=0.95, FULL): " + "  ".join(
        f"{p} {int(cl[(cl.panel==p)&(cl.formset=='WIDE')&(cl.window=='FULL')&(cl.tau==0.95)].n_forms.iloc[0])}"
        for p in P) + "   vs idea 837's 14")
    h_ceil = all(int(cl[(cl.panel==p)&(cl.formset=='WIDE')&(cl.window=='FULL')&(cl.tau==0.95)].n_forms.iloc[0]) < 14 for p in P)
    say(f"  H_CEIL   {'PASSES' if h_ceil else 'FAILS'}")

    # H_DIAL: dial pairs in one cluster at tau 0.95
    DIALS = [("EW_ALL", "EW_G100"), ("EW_ALL", "EW_G0375"), ("TOP20_MOM", "TOP10_MOM"),
             ("TOP20_MOM", "TOP5_MOM"), ("TOP20_MOM", "TOP20_MOM_M"), ("LOWVOL20", "LOWVOL10")]
    dial_fail = []
    for panel in P:
        row = cl[(cl.panel == panel) & (cl.formset == "WIDE") & (cl.window == "FULL") & (cl.tau == 0.95)].iloc[0]
        parts = [set(x.split(",")) for x in row.partition.split("|")]
        for a, b in DIALS:
            if not any(a in s and b in s for s in parts): dial_fail.append((panel, a, b))
    say(f"  H_DIAL   {'PASSES' if not dial_fail else 'FAILS'}  dial pairs split across clusters: "
        f"{len(dial_fail)} of {len(DIALS)*len(P)}" + ("  " + "; ".join(f"{p}:{a}/{b}" for p, a, b in dial_fail) if dial_fail else ""))

    wmov = []
    for panel in P:
        for fs in FORMSETS:
            for tau in TAUS:
                v = cl[(cl.panel == panel) & (cl.formset == fs) & (cl.tau == tau)].n_forms
                wmov.append(int(v.max() - v.min()))
    say(f"  H_WINDOW {'PASSES' if max(wmov) <= 1 else 'FAILS'}  max spread of n_forms across "
        f"{{FULL,IS,ROLL252}} at fixed (panel, form set, tau) = {max(wmov)}")

    # ------------------------------------- the threshold the DIALS calibrate ---
    say("")
    say("SECTION 1b  THE DIAL-CALIBRATED CEILING  (no arbitrary tau: the ladder rung is fixed by")
    say("            the known duplicates.  tau_dial = the HIGHEST rung at which all six pure-dial")
    say("            pairs are still one cluster; the form count there is the ceiling on cross-book n.)")
    say("            dial pairs: " + ", ".join(f"{a}/{b}" for a, b in DIALS))
    for panel in P:
        df = RET[panel][0]
        rho = {f"{a}/{b}": float(np.corrcoef(df[a], df[b])[0, 1]) for a, b in DIALS}
        say(f"  {panel:9s} dial-pair rho  " + "  ".join(f"{k}={v:.4f}" for k, v in rho.items()))
        say(f"  {panel:9s} weakest dial pair rho = {min(rho.values()):.4f}"
            f"  ({min(rho, key=rho.get)})")
        for win in WINDOWS:
            td, nf = None, None
            for tau in TAUS:
                row = cl[(cl.panel == panel) & (cl.formset == "WIDE") & (cl.window == win) & (cl.tau == tau)].iloc[0]
                parts = [set(x.split(",")) for x in row.partition.split("|")]
                if all(any(a in s and b in s for s in parts) for a, b in DIALS):
                    td, nf = tau, int(row.n_forms)
            say(f"  {panel:9s} {win:7s} tau_dial = {td if td is not None else 'NONE (no rung merges every dial pair)'}"
                f"   independent forms there = {nf if nf is not None else 'n/a'}   of 20 arms")

    # --------------------------------------------------------- walk-forward ---
    say("")
    say("SECTION 2  RULE 8 WALK-FORWARD  (partition fitted on IS <= 2016-12-31, evaluated 2017+)")
    agrees = []
    for panel in P:
        df, base, spy = RET[panel]
        for fs in FORMSETS:
            names = [n for n in df.columns if (CAT[panel][n][3] or fs == "WIDE")]
            sub = df[names]
            Mis = sub.loc[:IS_END].corr().to_numpy()
            Moos = sub.loc[OOS_START:].corr().to_numpy()
            for tau in TAUS:
                gis, goos = clusters_at(Mis, names, tau), clusters_at(Moos, names, tau)
                ag = pair_agreement(label_vec(gis, len(names)), label_vec(goos, len(names)))
                agrees.append(ag)
                reps = [names[c[0]] for c in gis]          # first in catalogue order, NEVER the best
                Wens = sum(CAT[panel][r][0] for r in reps) / len(reps)
                px = investable(P[panel], panel)
                rens = run(px, Wens, freq="W").loc[df.index[0]:]
                a, b4, d = keep_paths(rens, base, spy)
                cg, sh, dd = stats(rens); cgo, sho, ddo = stats(rens.loc[OOS_START:])
                bo = base.loc[OOS_START:]; so = spy.loc[OOS_START:]
                wf_rows.append(dict(panel=panel, formset=fs, tau=tau, n_forms_IS=len(gis),
                                    n_forms_OOS=len(goos), pair_agreement=ag, reps="|".join(reps),
                                    ens_CAGR=cg, ens_Sharpe=sh, ens_MaxDD=dd,
                                    ens_H1=d["H1"], ens_H2=d["H2"],
                                    ens_OOS_CAGR=cgo, ens_OOS_Sharpe=sho, ens_OOS_MaxDD=ddo,
                                    base_OOS_Sharpe=metrics(bo)["Sharpe"], base_OOS_CAGR=metrics(bo)["CAGR"],
                                    base_OOS_MaxDD=metrics(bo)["MaxDD"],
                                    spy_OOS_Sharpe=metrics(so)["Sharpe"], spy_OOS_CAGR=metrics(so)["CAGR"],
                                    spy_OOS_MaxDD=metrics(so)["MaxDD"],
                                    pass4a=a, pass4b=b4))
                say(f"  {panel:9s} {fs:4s} tau={tau:<5g} IS_forms={len(gis):2d} OOS_forms={len(goos):2d} "
                    f"agree={ag:.4f}  ens OOS CAGR {cgo:+.2%} Sharpe {sho:+.3f} MaxDD {ddo:+.2%}  "
                    f"4a={'Y' if a else 'n'} 4b={'Y' if b4 else 'n'}")
    say(f"  H_STABLE {'PASSES' if min(agrees) >= 0.90 else 'FAILS'}  min pair agreement "
        f"{min(agrees):.4f} over {len(agrees)} (panel, form set, tau) cells")

    wf = pd.DataFrame(wf_rows)
    h_ens = bool((~wf.pass4b).any())
    say(f"  H_ENS    {'PASSES' if h_ens else 'FAILS'}  ensemble 4b passes {int(wf.pass4b.sum())} of {len(wf)} cells")

    # ---------------------------------------------------------------- arms ---
    am = pd.DataFrame(arms_rows)
    say("")
    say("SECTION 3  EVERY ARM, EVERY PANEL  (full / halves / OOS, both KEEP paths)")
    for panel in P:
        df, base, spy = RET[panel]
        bo, so = base.loc[OOS_START:], spy.loc[OOS_START:]
        say(f"  --- {panel} ---   RULES v2 baseline: CAGR {metrics(base)['CAGR']:+.2%} Sharpe "
            f"{metrics(base)['Sharpe']:+.3f} MaxDD {metrics(base)['MaxDD']:+.2%} | OOS Sharpe "
            f"{metrics(bo)['Sharpe']:+.3f} CAGR {metrics(bo)['CAGR']:+.2%}   "
            f"SPY: CAGR {metrics(spy)['CAGR']:+.2%} Sharpe {metrics(spy)['Sharpe']:+.3f} "
            f"MaxDD {metrics(spy)['MaxDD']:+.2%} | OOS Sharpe {metrics(so)['Sharpe']:+.3f} "
            f"CAGR {metrics(so)['CAGR']:+.2%}")
        sub = am[am.panel == panel]
        for _, r in sub.iterrows():
            say(f"    {r.arm:12s} CAGR {r.CAGR:+.2%} Sharpe {r.Sharpe:+.3f} MaxDD {r.MaxDD:+.2%} "
                f"H {r.H1:+.2f}/{r.H2:+.2f}  OOS CAGR {r.OOS_CAGR:+.2%} Sharpe {r.OOS_Sharpe:+.3f} "
                f"MaxDD {r.OOS_MaxDD:+.2%}  4a={'Y' if r.pass4a else 'n'} 4b={'Y' if r.pass4b else 'n'}")

    am.to_csv(f"{STEM}.arms.csv", index=False)
    cl.to_csv(f"{STEM}.clusters.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)
    say("")
    say("WROTE  .arms.csv  .clusters.csv  .walkforward.csv")
    Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
