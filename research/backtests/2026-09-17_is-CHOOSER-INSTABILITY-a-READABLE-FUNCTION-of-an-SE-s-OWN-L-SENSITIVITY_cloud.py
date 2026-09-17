#!/usr/bin/env python3
"""QUEUE idea 1220 - is CHOOSER INSTABILITY a READABLE FUNCTION of an SE's OWN L-SENSITIVITY?

Idea 1212 found the fold-clustered SE lands on 6 distinct N over 15 (panel, L) cells against
the block SE's 4 and a naive IS-Sharpe chooser's 3, and that the fold SE is also the basis
whose critical value moves most with L (x1.54 against the block's x1.24).  If those two are
the SAME fact, then the L-SENSITIVITY CURVE - which costs one in-sample pass and no OOS data
at all - predicts the expensive thing (pick instability), and a fragile chooser can be spotted
without a walk-forward.  This run tests the relation across the record's chooser family and
asks whether it holds out of sample.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    CHOOSER SET {K_SE3, K_SE3_NAIVE, K_ALL}
  x L LADDER    {L_SHORT, L_WIDE, L_LONG}
  = 9 cells, EVERY ONE PUBLISHED.

NOT dials, reported at every value: PANEL {U56, B136, SMALL}; ANCHOR (N, cadence)
{(20,W), (12,W), (20,M), (10,M)}; the N ladder {5,10,12,20,30,40,60} (k=7, inside d2's
domain); the six L rungs {21,42,63,126,252,504}; the 4a and 4b legs; the rule-8 split.
10 bps, t+1 execution (engine), 260-row warm-up, IS 2009-2016, OOS 2017-2026 read ONCE.
Book construction frozen at the 2026-09-04 KEEP-4b candidate's: composite (12-1 + 6m + 3m
percentile ranks), NO vol scaler, above-own-200d-MA eligibility, top-N equal weight at
g/N of NAV with g = 0.75, gated-out weight to CASH at 0%.

SURVIVORSHIP: universe.json / universe_broad.json are CURRENT constituents; the small panel
is the current output of a sub-$2B screen (data/SMALL_PANEL_README.md).  Names with
max_1d_move >= 1.0 are dropped before anything is computed.

Run:  python3 research/backtests/2026-09-17_is-CHOOSER-INSTABILITY-a-READABLE-FUNCTION-of-an-SE-s-OWN-L-SENSITIVITY_cloud.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, metrics                           # noqa: E402

OUT = Path(__file__).with_suffix("")
SEED = 1220
COST_BPS = 10
WARMUP = 260
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
GROSS = 0.75
N_RUNGS = [5, 10, 12, 20, 30, 40, 60]
ANCHORS = [(20, "W"), (12, "W"), (20, "M"), (10, "M")]
L_RUNGS = [21, 42, 63, 126, 252, 504]
L_LADDERS = {"L_SHORT": [21, 42, 63], "L_WIDE": L_RUNGS, "L_LONG": [126, 252, 504]}
BOOT = 400
BAR_T = 2.0          # a move needs |gap| > 2 SE.  Fixed, NOT a dial (PROTOCOL rule 4).

# Choosers.  `L_dep` says whether the basis reads L at all.
CHOOSERS = {
    "SE_IID":    dict(L_dep=False, kind="se"),
    "SE_BLOCK":  dict(L_dep=True,  kind="se"),
    "SE_FOLD":   dict(L_dep=True,  kind="se"),
    "C_NAIVE":   dict(L_dep=False, kind="argmax"),   # IS argmax, no SE at all
    "C_CALMAR":  dict(L_dep=False, kind="calmar"),   # IS Calmar argmax, 1189's control
    "C_ANCHOR":  dict(L_dep=False, kind="anchor"),   # do nothing (1221's winner)
}
SETS = {
    "K_SE3":       ["SE_IID", "SE_BLOCK", "SE_FOLD"],
    "K_SE3_NAIVE": ["SE_IID", "SE_BLOCK", "SE_FOLD", "C_NAIVE"],
    "K_ALL":       ["SE_IID", "SE_BLOCK", "SE_FOLD", "C_NAIVE", "C_CALMAR", "C_ANCHOR"],
}


# ---------------------------------------------------------------------------
# (0) THE ARITHMETIC, PRINTED BEFORE ANY PRICE IS READ
# ---------------------------------------------------------------------------
# SE_IID, C_NAIVE, C_CALMAR and C_ANCHOR do not read L, so their POPULATION L-sensitivity
# ratio is 1 and their distinct-pick count over any L ladder is 1, at every panel and every
# anchor.  They are therefore a DEGENERATE point of the relation under test: including them
# manufactures a positive correlation out of a definition.  Every correlation below is
# reported TWICE - over all choosers in the set, and over the L-DEPENDENT ones only.  That is
# a gate, not a dial.
#
# SE_IID is ALSO the run's noise floor, and its REALISED ratio is NOT 1: it is re-bootstrapped
# independently at each L rung, so whatever it reads above 1 is pure Monte-Carlo dispersion at
# BOOT draws.  SE_BLOCK's and SE_FOLD's L-sensitivity must be read against that floor, not
# against 1.  The floor is measured and printed below before any relation is fitted.

def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def calmar(r):
    m = metrics(r)
    return float(m["Calmar"]) if m["MaxDD"] else np.nan


def mstats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# ---------------------------------------------------------------------------
# The three SE bases, all PAIRED (idea 1042: the paired basis is the honest yardstick
# for a leg margin; the comparand basis overstates it 1.83x at rho 0.8521).
# ---------------------------------------------------------------------------
def se_iid(a, b, rng):
    """Paired iid bootstrap of the Sharpe DIFFERENCE.  Reads no L."""
    x, y = a.values, b.values
    n = len(x)
    idx = rng.integers(0, n, size=(BOOT, n))
    return float(np.nanstd(_sh(x[idx]) - _sh(y[idx])))


def se_block(a, b, L, rng):
    """Paired moving-block bootstrap of the Sharpe DIFFERENCE at block length L."""
    x, y = a.values, b.values
    n = len(x)
    L = min(L, n)
    nb = int(np.ceil(n / L))
    st = rng.integers(0, n - L + 1, size=(BOOT, nb))
    idx = (st[:, :, None] + np.arange(L)[None, None, :]).reshape(BOOT, -1)[:, :n]
    return float(np.nanstd(_sh(x[idx]) - _sh(y[idx])))


def se_fold(a, b, L):
    """Calendar-fold-clustered SE: the tape is cut into contiguous folds of L days, the
    Sharpe difference is computed WITHIN each fold, and the SE is sd(fold diffs)/sqrt(F).
    Reads L as a fold length, deterministically - no resampling."""
    x, y = a.values, b.values
    n = len(x)
    F = n // L
    if F < 2:
        return np.nan
    d = []
    for f in range(F):
        xs, ys = x[f * L:(f + 1) * L], y[f * L:(f + 1) * L]
        sx, sy = xs.std(), ys.std()
        if sx <= 0 or sy <= 0:
            continue
        d.append(xs.mean() * np.sqrt(252) / sx - ys.mean() * np.sqrt(252) / sy)
    d = np.asarray(d)
    return float(d.std(ddof=1) / np.sqrt(len(d))) if len(d) >= 2 else np.nan


def _sh(s):
    mu, sd = s.mean(axis=1), s.std(axis=1)
    return np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b))
    a, b = a[ok], b[ok]
    if len(a) < 3 or np.ptp(a) == 0 or np.ptp(b) == 0:
        return np.nan
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


# ---------------------------------------------------------------------------
def panels():
    P = {"U56": load_universe(), "B136": load_universe(broad=True)}
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    drop = [c for c in ps.columns if c in bad]
    ps = ps.drop(columns=drop)
    print(f"[0] SMALL: dropped {len(drop)} names with max_1d_move >= 1.0; "
          f"{ps.shape[1] - 1} tradable + SPY benchmark")
    P["SMALL"] = ps
    return P


def book_weights(px, N, tradable):
    q = px[tradable]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = q > q.rolling(200).mean()
    rank = comp.where(above).rank(axis=1, ascending=False)
    w = (rank <= N).astype(float) * (GROSS / N)
    return w.reindex(columns=px.columns).fillna(0.0)


def main():
    print(__doc__.split("Run:")[0])
    print("[0] DEGENERACY GATE, stated before any price is read: SE_IID / C_NAIVE / C_CALMAR /"
          " C_ANCHOR do not read L, so their POPULATION L-sensitivity ratio is 1 and their"
          " distinct-pick count is 1. Every correlation is reported twice - over the whole set,"
          " and over the L-DEPENDENT choosers only. SE_IID's REALISED ratio is the run's"
          f" Monte-Carlo floor at BOOT={BOOT} and is measured, not assumed.")
    rng = np.random.default_rng(SEED)
    P = panels()

    # ---- books -------------------------------------------------------------
    books, bench = {}, {}
    for pname, px in P.items():
        tradable = [c for c in px.columns if c != "SPY"] if pname == "SMALL" else list(px.columns)
        start = px.index[WARMUP]
        for N in N_RUNGS:
            w = book_weights(px, N, tradable)
            for cad in ("W", "M"):
                books[(pname, N, cad)] = backtest(px, w, cost_bps=COST_BPS,
                                                  freq=cad)["returns"].loc[start:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        live = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        bench[pname] = dict(SPY=spy, LIVE=live)
        print(f"[1] {pname}: {len(N_RUNGS) * 2} books built")

    brows = []
    for pname, b in bench.items():
        for bn, r in b.items():
            for win, s in (("FULL", r), ("IS", r.loc[:IS_END]), ("OOS", r.loc[OOS_START:])):
                d = mstats(s); d.update(panel=pname, series=bn, window=win); brows.append(d)
    B = pd.DataFrame(brows)[["panel", "series", "window", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
    B.to_csv(OUT.with_suffix(".benchmarks.csv"), index=False)
    print("\n[1] BENCHMARKS (10 bps, t+1):")
    print(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- the SE surface: one SE per (panel, anchor, basis, L) --------------
    # The gap under test is always IS-argmax-rung MINUS anchor-rung, paired on the same tape.
    serows, pickrows = [], []
    for pname in P:
        for (aN, cad) in ANCHORS:
            iss = {N: sharpe(books[(pname, N, cad)].loc[:IS_END]) for N in N_RUNGS}
            isc = {N: calmar(books[(pname, N, cad)].loc[:IS_END]) for N in N_RUNGS}
            argmax_N = max(N_RUNGS, key=lambda N: iss[N])
            calmax_N = max(N_RUNGS, key=lambda N: isc[N])
            a = books[(pname, argmax_N, cad)].loc[:IS_END]
            b = books[(pname, aN, cad)].loc[:IS_END]
            gap = iss[argmax_N] - iss[aN]
            # OOS replica of the SAME measurement, for "does the relation hold OOS"
            a_o = books[(pname, argmax_N, cad)].loc[OOS_START:]
            b_o = books[(pname, aN, cad)].loc[OOS_START:]
            for L in L_RUNGS:
                s_iid = se_iid(a, b, rng)
                s_blk = se_block(a, b, L, rng)
                s_fld = se_fold(a, b, L)
                s_iid_o = se_iid(a_o, b_o, rng)
                s_blk_o = se_block(a_o, b_o, L, rng)
                s_fld_o = se_fold(a_o, b_o, L)
                for basis, se, se_o in (("SE_IID", s_iid, s_iid_o),
                                        ("SE_BLOCK", s_blk, s_blk_o),
                                        ("SE_FOLD", s_fld, s_fld_o)):
                    serows.append(dict(panel=pname, anchor_N=aN, cadence=cad, L=L,
                                       basis=basis, se_IS=se, se_OOS=se_o, gap=gap,
                                       t=gap / se if se and not np.isnan(se) else np.nan,
                                       argmax_N=argmax_N))
                for ch, spec in CHOOSERS.items():
                    if spec["kind"] == "anchor":
                        pick = aN
                    elif spec["kind"] == "argmax":
                        pick = argmax_N
                    elif spec["kind"] == "calmar":
                        pick = calmax_N
                    else:
                        se = {"SE_IID": s_iid, "SE_BLOCK": s_blk, "SE_FOLD": s_fld}[ch]
                        pick = argmax_N if (se and not np.isnan(se) and abs(gap) > BAR_T * se) else aN
                    r_full = books[(pname, pick, cad)]
                    mf, mo = mstats(r_full), mstats(r_full.loc[OOS_START:])
                    msf = mstats(bench[pname]["SPY"]); mso = mstats(bench[pname]["SPY"].loc[OOS_START:])
                    mlf = mstats(bench[pname]["LIVE"])
                    keep4a = (mf["H1"] > mlf["H1"] and mf["H2"] > mlf["H2"] and mf["MaxDD"] >= mlf["MaxDD"])
                    keep4b = (mf["H1"] > msf["H1"] and mf["H2"] > msf["H2"]
                              and mo["Sharpe"] > mso["Sharpe"]
                              and mf["MaxDD"] >= 0.60 * msf["MaxDD"]
                              and mf["CAGR"] >= 0.70 * msf["CAGR"])
                    pickrows.append(dict(panel=pname, anchor_N=aN, cadence=cad, L=L, chooser=ch,
                                         pick=pick, moved=pick != aN, gap=gap,
                                         CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                         H1=mf["H1"], H2=mf["H2"], oos_CAGR=mo["CAGR"],
                                         oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                                         spy_Sharpe=msf["Sharpe"], spy_oos_Sharpe=mso["Sharpe"],
                                         live_Sharpe=mlf["Sharpe"], KEEP_4a=keep4a, KEEP_4b=keep4b))
    SE = pd.DataFrame(serows); PK = pd.DataFrame(pickrows)
    SE.to_csv(OUT.with_suffix(".se_surface.csv"), index=False)
    PK.to_csv(OUT.with_suffix(".picks.csv"), index=False)
    print(f"\n[2] SE SURFACE: {len(SE)} (panel, anchor, basis, L) rows; "
          f"PICKS: {len(PK)} (panel, anchor, chooser, L) decisions.")

    med = SE.groupby("basis").se_IS.median()
    print("[2] median IS SE of the Sharpe gap by basis: "
          + ", ".join(f"{k} {v:.4f}" for k, v in med.items())
          + "   (1212 reported FOLD smallest: reproduced = "
          + f"{med.idxmin() == 'SE_FOLD'})")

    # ---- the two quantities under test, per (panel, anchor, chooser) ------
    rel = []
    for pname in P:
        for (aN, cad) in ANCHORS:
            for ch, spec in CHOOSERS.items():
                sub = PK[(PK.panel == pname) & (PK.anchor_N == aN) & (PK.cadence == cad)
                         & (PK.chooser == ch)]
                if ch in ("SE_IID", "SE_BLOCK", "SE_FOLD"):
                    s = SE[(SE.panel == pname) & (SE.anchor_N == aN) & (SE.cadence == cad)
                           & (SE.basis == ch)]
                    lo, hi = s.se_IS.min(), s.se_IS.max()
                    lsens = float(hi / lo) if lo and lo > 0 else np.nan
                    lo_o, hi_o = s.se_OOS.min(), s.se_OOS.max()
                    lsens_o = float(hi_o / lo_o) if lo_o and lo_o > 0 else np.nan
                else:
                    lsens = lsens_o = 1.0          # reads no L, by construction
                rel.append(dict(panel=pname, anchor_N=aN, cadence=cad, chooser=ch,
                                L_dep=CHOOSERS[ch]["L_dep"],
                                L_sens_IS=lsens, L_sens_OOS=lsens_o,
                                distinct_picks=int(sub.pick.nunique()),
                                moved_rungs=int(sub.moved.sum()),
                                oos_Sharpe_mean=float(sub.oos_Sharpe.mean()),
                                oos_Sharpe_spread=float(sub.oos_Sharpe.max() - sub.oos_Sharpe.min()),
                                n4b=int(sub.KEEP_4b.sum()), n4a=int(sub.KEEP_4a.sum())))
    R = pd.DataFrame(rel)
    R.to_csv(OUT.with_suffix(".relation.csv"), index=False)

    # ---- the Monte-Carlo floor, measured before any relation is fitted ----
    floor = float(R[R.chooser == "SE_IID"].L_sens_IS.median())
    floor_max = float(R[R.chooser == "SE_IID"].L_sens_IS.max())
    print(f"\n[3a] MONTE-CARLO FLOOR: SE_IID reads no L, yet its realised L-sensitivity ratio "
          f"is median {floor:.4f} (max {floor_max:.4f}) at BOOT={BOOT}. "
          f"Excess over the floor: "
          + ", ".join(
              f"{ch} {(float(R[R.chooser == ch].L_sens_IS.median()) - 1) / (floor - 1):.2f}x"
              for ch in ("SE_BLOCK", "SE_FOLD"))
          + " the floor's own excess. A ratio below ~"
          f"{floor_max:.2f} is NOT evidence that a basis reads L.")

    # ---- what actually predicts OOS Sharpe: HOW OFTEN THE CHOOSER MOVES ---
    mv = R.groupby("chooser").agg(moved=("moved_rungs", "sum"),
                                  oos=("oos_Sharpe_mean", "mean")).reset_index()
    rho_move = spearman(mv.moved, mv.oos)
    print(f"\n[3b] THE CHEAP STATISTIC THAT DOES WORK: Spearman(move count, mean OOS Sharpe) "
          f"over the {len(mv)} choosers = {rho_move:.4f}")
    print(mv.sort_values("moved").to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    mv.to_csv(OUT.with_suffix(".movecount.csv"), index=False)

    print(f"\n[3c] RESOLUTION OF THE 'EXPENSIVE' QUANTITY: distinct_picks takes the values "
          f"{sorted(R.distinct_picks.unique())} over all 72 (panel, anchor, chooser) cells — "
          f"it is effectively BINARY, so any rho fitted on it is fitted on 2 levels.")
    print("\n[3] THE TWO QUANTITIES, per (panel, anchor, chooser) - 72 cells "
          "(full table in .relation.csv):")
    print(R.groupby("chooser").agg(
        L_sens_IS_med=("L_sens_IS", "median"), L_sens_OOS_med=("L_sens_OOS", "median"),
        distinct_picks_tot=("distinct_picks", "sum"), max_distinct=("distinct_picks", "max"),
        moved=("moved_rungs", "sum"), oos_Sharpe=("oos_Sharpe_mean", "mean"),
        n4b=("n4b", "sum"), n4a=("n4a", "sum")).to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- the 9 cells -------------------------------------------------------
    cells = []
    for sname, chs in SETS.items():
        for lname, Ls in L_LADDERS.items():
            sub_pk = PK[PK.chooser.isin(chs) & PK.L.isin(Ls)]
            sub_se = SE[SE.L.isin(Ls)]
            rows = []
            for pname in P:
                for (aN, cad) in ANCHORS:
                    for ch in chs:
                        s = sub_pk[(sub_pk.panel == pname) & (sub_pk.anchor_N == aN)
                                   & (sub_pk.cadence == cad) & (sub_pk.chooser == ch)]
                        if ch in ("SE_IID", "SE_BLOCK", "SE_FOLD"):
                            q = sub_se[(sub_se.panel == pname) & (sub_se.anchor_N == aN)
                                       & (sub_se.cadence == cad) & (sub_se.basis == ch)]
                            lo, hi = q.se_IS.min(), q.se_IS.max()
                            ls = float(hi / lo) if lo and lo > 0 else np.nan
                            lo_o, hi_o = q.se_OOS.min(), q.se_OOS.max()
                            ls_o = float(hi_o / lo_o) if lo_o and lo_o > 0 else np.nan
                        else:
                            ls = ls_o = 1.0
                        rows.append((ch, CHOOSERS[ch]["L_dep"], ls, ls_o,
                                     s.pick.nunique(), s.oos_Sharpe.mean()))
            D = pd.DataFrame(rows, columns=["chooser", "L_dep", "ls", "ls_o", "dp", "oos"])
            Ld = D[D.L_dep]
            cells.append(dict(
                chooser_set=sname, L_ladder=lname, n_L=len(Ls), n_cells=len(D),
                rho_all=spearman(D.ls, D.dp),
                rho_Ldep_only=spearman(Ld.ls, Ld.dp),
                rho_OOS_all=spearman(D.ls_o, D.dp),
                rho_OOS_Ldep_only=spearman(Ld.ls_o, Ld.dp),
                mean_L_sens=float(D.ls.mean()), mean_distinct=float(D.dp.mean()),
                mean_oos_Sharpe=float(D.oos.mean()),
                n_4b=int(sub_pk.KEEP_4b.sum()), n_4a=int(sub_pk.KEEP_4a.sum()),
                decisions=len(sub_pk)))
    C = pd.DataFrame(cells)
    C.to_csv(OUT.with_suffix(".cells.csv"), index=False)
    print("\n[4] THE 9 CELLS, EVERY ONE PUBLISHED "
          "(rho = Spearman between a chooser's IS L-sensitivity and its distinct-pick count):")
    print(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- rule 8 walk-forward ----------------------------------------------
    print("\n[5] RULE-8 WALK-FORWARD, both KEEP paths. Picks made on 2009-2016, "
          "2017-2026 read ONCE.")
    wf = PK.groupby("chooser").agg(
        decisions=("pick", "size"), moved=("moved", "sum"), distinct=("pick", "nunique"),
        CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "min"),
        oos_CAGR=("oos_CAGR", "mean"), oos_Sharpe=("oos_Sharpe", "mean"),
        oos_MaxDD=("oos_MaxDD", "min"), n4a=("KEEP_4a", "sum"), n4b=("KEEP_4b", "sum"))
    wf.to_csv(OUT.with_suffix(".walkforward.csv"))
    print(wf.to_string(float_format=lambda x: f"{x:.4f}"))

    best = PK.loc[PK.KEEP_4b].sort_values("oos_Sharpe", ascending=False)
    print(f"\n[5] 4b passers: {len(best)} of {len(PK)} decisions over "
          f"{best[['panel', 'anchor_N', 'cadence', 'pick']].drop_duplicates().shape[0]} "
          f"DISTINCT (panel, cadence, N) books (1211's decision-row vs book correction).")
    if len(best):
        print(best[["panel", "anchor_N", "cadence", "L", "chooser", "pick", "CAGR", "Sharpe",
                    "MaxDD", "H1", "H2", "oos_CAGR", "oos_Sharpe", "oos_MaxDD"]]
              .drop_duplicates(subset=["panel", "cadence", "pick"])
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- the verdict -------------------------------------------------------
    rho_ld = C.rho_Ldep_only.dropna()
    rho_all = C.rho_all.dropna()
    print("\n" + "=" * 100)
    print(f"RELATION over ALL choosers:      rho in [{rho_all.min():.4f}, {rho_all.max():.4f}], "
          f"median {rho_all.median():.4f} over {len(rho_all)} of 9 cells")
    print(f"RELATION over L-DEPENDENT only:  rho in "
          f"[{rho_ld.min() if len(rho_ld) else float('nan'):.4f}, "
          f"{rho_ld.max() if len(rho_ld) else float('nan'):.4f}], "
          f"median {rho_ld.median() if len(rho_ld) else float('nan'):.4f} "
          f"over {len(rho_ld)} of 9 cells")
    print(f"4a {int(PK.KEEP_4a.sum())} of {len(PK)}; 4b {int(PK.KEEP_4b.sum())} of {len(PK)}.")
    print("=" * 100)
    for f in sorted(OUT.parent.glob(OUT.name + ".*")):
        print("wrote", f.relative_to(ROOT))


if __name__ == "__main__":
    main()
