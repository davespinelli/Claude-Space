#!/usr/bin/env python3
"""IDEA 2101 (lane cloud, 2026-09-22) — IS ANY LEGAL IS-ONLY CHOOSER PORTABLE ACROSS PANELS,
OR IS EVERY COMMITTED RULE-8 PICK A PANEL ARTEFACT?

THE QUESTION.  Every rule-8 verdict in this record is published as "reached by a legal IS-only
chooser", i.e. as if the chooser were neutral machinery that merely implements PROTOCOL rule 8.
Idea 2087 ran SEVEN legal IS-only choosers over ONE family's 30-cell grid and found (a) a 157x
spread in reach (IS_LEGS 0.785, CELL_ALPHA 0.005) and (b) a cross-panel INVERSION of the top two
(IS_LEGS 0.785 -> 0.300 and IS_SHARPE 0.680 -> 0.983 going U56 -> B136) at Spearman rho +0.5357.
If that is general, then "a legal chooser reaches it" is a claim about the PANEL, not the book.

WHAT THIS RUN DOES.  Score the SAME seven choosers on THREE panels (U56 / B136 / SMALL) over
THREE book families the record owns (BAND, TOPN, VOLTGT), 12 cells each, and report:
  (1) each chooser's OOS-Sharpe PERCENTILE inside its own shelf (0.5 = a uniform draw),
  (2) the cross-panel SPEARMAN rho of the seven choosers' ranks, per family and pooled,
  (3) whether ANY chooser is stable in SIGN, i.e. above the uniform-draw 0.5 on ALL THREE panels
      and above the no-information CELL_ALPHA control on all three,
  (4) both KEEP paths (4a vs live RULES v2, 4b vs SPY) on FULL and OOS for every picked book.

TUNED DIALS — EXACTLY TWO, as PROTOCOL rule 4 allows: CHOOSER (7 rules) and PANEL (3).
REPORTED, NOT TUNED: the three families and their 12-cell ladders (the record's own), the cost
ladder 0/10/25/50 bps (headline 10 per PROTOCOL rule 2), execution at t+1 (rule 2), the
IS/OOS split (rule 8: parameters chosen on <= 2016-12-31, 2017-01-01 onward read exactly once),
warm-up 260 rows.  ALL grid points are written to <slug>.grid.csv; nothing is reported
selectively.

SURVIVORSHIP — READ THIS BEFORE THE NUMBERS.  All three panels are CURRENT-constituent lists.
SMALL is a screen of names that are sub-$2B *today* and have priced continuously since 2010, so
every name that was delisted, acquired or wiped out is absent; its CAGR and drawdown LEVELS are
materially optimistic, more so than U56's or B136's.  Per this sprint's standing rule the 54
SMALL tickers with `max_1d_move >= 1.0` in data/small_meta.csv are dropped before anything is
priced.  The PORTABILITY statistic this run publishes is a CONTRAST between panels and is
therefore less exposed to the bias than any level would be, but it is not immune: a chooser
could be stable across three biased panels and unstable across three honest ones.  Stated as a
limit of the test, not argued away.

PROTOCOL: rule 2 (10 bps, t+1), rule 3 (vs RULES v2 live baseline and SPY), rule 4 (both KEEP
paths, 2 tuned params), rule 5 (one idea, deterministic, standalone), rule 7 (a KILL is a
result), rule 8 (walk-forward), rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-22_chooser-portability-across-panels_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask            # noqa: E402

DATE, SLUG = "2026-09-22", "chooser-portability-across-panels"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# ---- TUNED DIAL 1: the chooser set (2087's seven, copied unchanged) --------------------------
CHOOSERS = ["IS_SHARPE", "IS_LEGS", "IS_CALMAR", "IS_MINMARG", "IS_CAGRSLACK", "IS_DD",
            "CELL_ALPHA"]
# ---- TUNED DIAL 2: the panel ----------------------------------------------------------------
PANEL_NAMES = ["U56", "B136", "SMALL"]

# ---- REPORTED, NOT TUNED: three families the record owns, 12 cells each ---------------------
BANDS = [0.00, 0.03, 0.06, 0.10]
GROSSES = [0.50, 0.75, 1.00]
TOPNS = [5, 10, 20, 40]
TARGETS = [0.08, 0.12, 0.16, 0.20]
SIG_L = 20

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ----------------------------------------------------------------------------- fast engine
def bt_fast(R, W, mask):
    """Numpy transcription of products/backtester/engine.backtest with cost_bps=0: target
    weights decided at close t are applied at t+1 (W and mask are pre-shifted by the caller),
    positions drift between rebalances, cash earns zero.  Returns (gross returns, turnover)."""
    T, N = R.shape
    cur = np.zeros(N)
    held = np.empty((T, N))
    turn = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = W[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        g = cur * (1.0 + R[i])
        tot = g.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = g / tot
    return (held * R).sum(axis=1), turn


def run_weights(px, W, freq):
    R = np.nan_to_num(px.pct_change().values, nan=0.0)
    Wv = np.nan_to_num(W.reindex(px.index).fillna(0.0).values, nan=0.0)
    Wv = np.vstack([np.zeros((1, Wv.shape[1])), Wv[:-1]])                 # .shift(1)
    m = np.asarray(rebalance_mask(px.index, freq).values, bool)
    m = np.concatenate([[False], m[:-1]])                                 # .shift(1)
    r, t = bt_fast(R, Wv, m)
    return pd.Series(r, index=px.index), pd.Series(t, index=px.index)


# ----------------------------------------------------------------------------- families
def eq_over(mask_df, gross):
    e = mask_df.astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return gross * e.div(n, axis=0).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    return pr.rolling(L).std() * np.sqrt(252.0)


def family_cells(px, cols, fam):
    """(cell label, weights DataFrame over `cols`, rebalance freq) for each of a family's 12."""
    sub = px[cols]
    priced = sub.notna()
    out = []
    if fam == "BAND":
        for b in BANDS:
            st = band_state(sub, b) & priced
            for g in GROSSES:
                out.append((f"band{b:.2f}_g{g:.2f}", eq_over(st, g), "W"))
    elif fam == "TOPN":
        mom = sub.shift(21) / sub.shift(252) - 1.0
        rank = mom.rank(axis=1, ascending=False)
        for n in TOPNS:
            sel = (rank <= n) & priced
            for g in GROSSES:
                out.append((f"top{n}_g{g:.2f}", eq_over(sel, g), "M"))
    elif fam == "VOLTGT":
        st = band_state(sub, 0.03) & priced
        sig = panel_sigma(px, cols)
        for t in TARGETS:
            scale = (t / sig.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            for g in GROSSES:
                out.append((f"volt{t:.2f}_g{g:.2f}", eq_over(st, g).mul(scale, axis=0), "M"))
    else:
        raise ValueError(fam)
    return out


# ----------------------------------------------------------------------------- metrics
def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=float(eq.iloc[-1] ** (1 / yrs) - 1) if yrs else np.nan,
                Sharpe=float((r.mean() * 252.0) / vol) if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def bars(r):
    """Every window a leg or a chooser is allowed to read, for one return stream."""
    h1, h2 = halves(r)
    ir = r.loc[:IS_END]
    ih1, ih2 = halves(ir)
    return dict(full=mets(r), oos=mets(r.loc[OOS_START:]), is_=mets(ir),
                h1=h1, h2=h2, ish1=ih1, ish2=ih2)


def score_cell(r0, t0, S, LV):
    """All 4a/4b legs plus every IS-only quantity a legal chooser may read, per cost rung."""
    rows = []
    for c in COSTS:
        r = net(r0, t0, c)
        B = bars(r)
        mf, mo, mi = B["full"], B["oos"], B["is_"]
        lv = LV[c]
        k4b_full = (B["h1"] > S["h1"] and B["h2"] > S["h2"]
                    and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                    and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
        k4b_oos = (mo["Sharpe"] > S["oos"]["Sharpe"]
                   and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                   and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
        k4a_full = (B["h1"] > lv["h1"] and B["h2"] > lv["h2"]
                    and mf["MaxDD"] >= lv["full"]["MaxDD"])
        k4a_oos = (mo["Sharpe"] > lv["oos"]["Sharpe"] and mo["MaxDD"] >= lv["oos"]["MaxDD"])
        is_legs = (int(B["ish1"] > S["ish1"]) + int(B["ish2"] > S["ish2"])
                   + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
                   + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
        is_minmarg = min(B["ish1"] - S["ish1"], B["ish2"] - S["ish2"],
                         mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                         mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])
        rows.append(dict(
            cost=c, turn_py=float(t0.sum() / (len(r0) / 252.0)),
            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=B["h1"], H2=B["h2"],
            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
            is_legs=is_legs, is_minmarg=float(is_minmarg),
            is_calmar=float(mi["CAGR"] / abs(mi["MaxDD"])) if mi["MaxDD"] < 0 else np.nan,
            is_cagrslack=float(mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"]),
            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
            keep4b_full=k4b_full, keep4b_oos=k4b_oos, keep4b=(k4b_full and k4b_oos),
            keep4a_full=k4a_full, keep4a_oos=k4a_oos, keep4a=(k4a_full and k4a_oos)))
    return rows


def pick(sub, chooser):
    """A LEGAL IS-ONLY chooser: it may read only columns computed on <= IS_END.  Deterministic
    tie-break on the cell label ascending, so no chooser wins on ordering luck.  Definitions
    copied unchanged from idea 2087."""
    s = sub.sort_values("cell").reset_index(drop=True)
    if chooser == "IS_SHARPE":
        key = s.is_Sharpe.values
    elif chooser == "IS_LEGS":
        key = s.is_legs.values * 1e6 + s.is_Sharpe.values
    elif chooser == "IS_CALMAR":
        key = np.nan_to_num(s.is_calmar.values, nan=-1e9)
    elif chooser == "IS_MINMARG":
        key = s.is_minmarg.values
    elif chooser == "IS_CAGRSLACK":
        key = s.is_cagrslack.values
    elif chooser == "IS_DD":
        key = s.is_MaxDD.values
    elif chooser == "CELL_ALPHA":                      # no-information control
        return s.iloc[0]
    else:
        raise ValueError(chooser)
    return s.iloc[int(np.argmax(key))]


def pctile(value, pool):
    """Fraction of the shelf strictly below, plus half the ties.  A uniform draw scores 0.5."""
    pool = np.asarray(pool, float)
    return float(((pool < value).sum() + 0.5 * (pool == value).sum()) / len(pool))


def spearman(a, b):
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    if np.std(ra) == 0 or np.std(rb) == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ----------------------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    log(f"  SMALL: dropped {len(px.columns) - len(keep)} tickers with max_1d_move >= 1.0 "
        f"(data/small_meta.csv); {len(keep) - 1} names + SPY benchmark remain")
    return px[keep].dropna(how="all").ffill()


def main():
    log(f"# Idea 2101 (lane cloud, {DATE}) — is ANY legal IS-ONLY chooser PORTABLE ACROSS "
        f"PANELS, or is every committed rule-8 pick a PANEL ARTEFACT?")
    log(f"# TUNED DIALS (2): CHOOSER {CHOOSERS}; PANEL {PANEL_NAMES}.")
    log(f"# REPORTED, NOT TUNED: families BAND {BANDS} x gross {GROSSES} (W), TOPN {TOPNS} x "
        f"gross {GROSSES} (M), VOLTGT {TARGETS} x gross {GROSSES} (M, band 0.03); costs "
        f"{COSTS} bps (headline {COST0}); warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START} "
        f"read ONCE.  Execution t+1 (PROTOCOL rule 2).")

    panels = {"U56": load_universe().dropna(how="all").ffill(),
              "B136": load_universe(broad=True).dropna(how="all").ffill(),
              "SMALL": small_panel()}

    # ---- G1 SANITY: the fast engine is the committed engine ---------------------------------
    p0 = panels["U56"]
    w0 = rules_v2_weights(p0, 0.03, 0.75)
    ref = engine_backtest(p0, w0, cost_bps=0.0, freq="W")
    r1, t1 = run_weights(p0, w0, "W")
    dr = float(np.nanmax(np.abs(ref["returns"].values - r1.values)))
    dt = float(np.nanmax(np.abs(ref["turnover"].values - t1.values)))
    gate("G1_ENGINE_IDENTITY", f"max|dret| {dr:.3e}, max|dturn| {dt:.3e}", "< 1e-12",
         dr < 1e-12 and dt < 1e-12)

    grid, picks = [], []
    for pname in PANEL_NAMES:
        px = panels[pname]
        cols = [c for c in px.columns if c != "SPY"]
        st = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        S = bars(spy)
        # live RULES v2 on the same panel = the matched 4a comparand, at every cost rung
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lr0, lt0 = run_weights(px, lw, "W")
        lr0, lt0 = lr0.loc[st:], lt0.loc[st:]
        LV = {c: bars(net(lr0, lt0, c)) for c in COSTS}
        log(f"\n## PANEL {pname}  ({len(cols)} names, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, scored from {st.date()})")
        log(f"   SPY      FULL {S['full']['CAGR']:7.2%} / {S['full']['Sharpe']:.3f} / "
            f"{S['full']['MaxDD']:7.2%}   OOS {S['oos']['CAGR']:7.2%} / "
            f"{S['oos']['Sharpe']:.3f} / {S['oos']['MaxDD']:7.2%}")
        lvc = LV[COST0]
        log(f"   RULES v2 FULL {lvc['full']['CAGR']:7.2%} / {lvc['full']['Sharpe']:.3f} / "
            f"{lvc['full']['MaxDD']:7.2%}   OOS {lvc['oos']['CAGR']:7.2%} / "
            f"{lvc['oos']['Sharpe']:.3f} / {lvc['oos']['MaxDD']:7.2%}   (at {COST0} bps)")

        for fam in ["BAND", "TOPN", "VOLTGT"]:
            for cell, W, freq in family_cells(px, cols, fam):
                Wfull = W.reindex(columns=px.columns).fillna(0.0)
                r0, t0 = run_weights(px, Wfull, freq)
                for row in score_cell(r0.loc[st:], t0.loc[st:], S, LV):
                    grid.append(dict(panel=pname, family=fam, cell=cell, freq=freq, **row))
        gdf = pd.DataFrame(grid)

        for fam in ["BAND", "TOPN", "VOLTGT"]:
            for c in COSTS:
                shelf = gdf[(gdf.panel == pname) & (gdf.family == fam) & (gdf.cost == c)]
                pool = shelf.oos_Sharpe.values
                for ch in CHOOSERS:
                    row = pick(shelf, ch)
                    picks.append(dict(
                        panel=pname, family=fam, cost=c, chooser=ch, cell=row.cell,
                        oos_Sharpe=row.oos_Sharpe, oos_CAGR=row.oos_CAGR,
                        oos_MaxDD=row.oos_MaxDD, CAGR=row.CAGR, Sharpe=row.Sharpe,
                        MaxDD=row.MaxDD, H1=row.H1, H2=row.H2,
                        pct=pctile(row.oos_Sharpe, pool),
                        shelf_best=float(np.max(pool)), shelf_med=float(np.median(pool)),
                        keep4a=bool(row.keep4a), keep4a_full=bool(row.keep4a_full),
                        keep4b=bool(row.keep4b), keep4b_full=bool(row.keep4b_full),
                        keep4b_oos=bool(row.keep4b_oos),
                        spy_oos_S=S["oos"]["Sharpe"], v2_oos_S=LV[c]["oos"]["Sharpe"]))

    gdf = pd.DataFrame(grid)
    pdf = pd.DataFrame(picks)
    gdf.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    pdf.to_csv(OUT.with_suffix(".choosers.csv"), index=False)
    log(f"\n# ALL GRID POINTS WRITTEN: {len(gdf)} cell-cost rows -> {OUT.name}.grid.csv; "
        f"{len(pdf)} chooser picks -> {OUT.name}.choosers.csv")

    # ------------------------------------------------------------------ (1) the chooser spread
    h = pdf[pdf.cost == COST0]
    log(f"\n## (1) THE CHOOSER SPREAD AT {COST0} BPS — OOS-Sharpe PERCENTILE inside the shelf "
        f"(0.500 = a uniform draw from the same 12 cells)")
    tab = h.pivot_table(index="chooser", columns=["panel", "family"], values="pct")
    tab = tab.reindex(CHOOSERS)
    log(tab.to_string(float_format=lambda x: f"{x:.3f}"))
    worst_spread = 0.0
    for (pn, fm), sub in h.groupby(["panel", "family"]):
        sp = float(sub.pct.max() - sub.pct.min())
        worst_spread = max(worst_spread, sp)
        log(f"   spread {pn:5s} {fm:6s}: {sp:.3f}   "
            f"(best {sub.loc[sub.pct.idxmax(), 'chooser']}, "
            f"worst {sub.loc[sub.pct.idxmin(), 'chooser']})")
    gate("G2_CHOOSER_MATTERS", f"max within-shelf percentile spread {worst_spread:.3f}",
         "> 0.25 (the choice of chooser moves the pick)", worst_spread > 0.25)

    # ------------------------------------------------------------- (2) cross-panel portability
    log(f"\n## (2) PORTABILITY — SPEARMAN rho of the SEVEN choosers' ranks, panel vs panel")
    rows = []
    for fm in ["BAND", "TOPN", "VOLTGT", "POOLED"]:
        for a, b in [("U56", "B136"), ("U56", "SMALL"), ("B136", "SMALL")]:
            if fm == "POOLED":
                va = [h[(h.panel == a) & (h.chooser == ch)].pct.mean() for ch in CHOOSERS]
                vb = [h[(h.panel == b) & (h.chooser == ch)].pct.mean() for ch in CHOOSERS]
            else:
                va = [float(h[(h.panel == a) & (h.family == fm) & (h.chooser == ch)].pct.iloc[0])
                      for ch in CHOOSERS]
                vb = [float(h[(h.panel == b) & (h.family == fm) & (h.chooser == ch)].pct.iloc[0])
                      for ch in CHOOSERS]
            rho = spearman(va, vb)
            rows.append(dict(family=fm, pair=f"{a}-{b}", rho=rho))
            log(f"   {fm:7s} {a:5s} vs {b:5s}: rho = {rho:+.4f}")
    rhos = pd.DataFrame(rows)
    med_rho = float(np.nanmedian(rhos.rho.values))
    gate("G3_PORTABLE", f"median cross-panel Spearman rho over 12 (family, pair) readings "
                        f"{med_rho:+.4f}", ">= +0.50 => choosers are portable machinery",
         med_rho >= 0.50)

    # ---------------------------------------------------------------- (3) sign stability
    log(f"\n## (3) SIGN STABILITY — pooled mean OOS percentile per panel (3 families)")
    stab = h.pivot_table(index="chooser", columns="panel", values="pct").reindex(CHOOSERS)
    stab = stab[PANEL_NAMES]
    alpha = stab.loc["CELL_ALPHA"]
    stab["all>0.5"] = (stab[PANEL_NAMES] > 0.5).all(axis=1)
    stab["beats_ALPHA_3of3"] = [bool((stab.loc[ch, PANEL_NAMES] > alpha).all())
                                for ch in stab.index]
    log(stab.to_string(float_format=lambda x: f"{x:.3f}"))
    stable = [ch for ch in CHOOSERS if ch != "CELL_ALPHA"
              and stab.loc[ch, "all>0.5"] and stab.loc[ch, "beats_ALPHA_3of3"]]
    gate("G4_ANY_STABLE_RULE", f"choosers above 0.5 AND above CELL_ALPHA on 3 of 3 panels: "
                               f"{stable if stable else 'NONE'}",
         ">= 1 rule stable in sign", len(stable) >= 1)

    # ------------------------------------------------------------------ (4) both KEEP paths
    log(f"\n## (4) BOTH KEEP PATHS for every chooser-picked book (rule 8: OOS read once)")
    n4a = int(h.keep4a.sum()); n4b = int(h.keep4b.sum())
    n4bf = int(h.keep4b_full.sum()); n4bo = int(h.keep4b_oos.sum())
    log(f"   at {COST0} bps, over {len(h)} picks (7 choosers x 3 panels x 3 families): "
        f"4a FULL+OOS {n4a}; 4b FULL {n4bf}; 4b OOS {n4bo}; 4b FULL+OOS {n4b}")
    log(f"   over ALL {len(gdf[gdf.cost == COST0])} grid cells at {COST0} bps: 4a "
        f"{int(gdf[gdf.cost == COST0].keep4a.sum())}; 4b FULL+OOS "
        f"{int(gdf[gdf.cost == COST0].keep4b.sum())}")
    log(f"\n   every pick at {COST0} bps (OOS CAGR / Sharpe / MaxDD vs SPY OOS and RULES v2 OOS):")
    log(h[["panel", "family", "chooser", "cell", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
           "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "pct", "keep4a", "keep4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    gate("G5_ANY_KEEP", f"4a {n4a}, 4b FULL+OOS {n4b} of {len(h)} chooser-picked books",
         ">= 1 book clears a KEEP path", (n4a + n4b) >= 1)

    # ------------------------------------------------------------------ cost robustness
    log(f"\n## COST LADDER — median cross-panel rho and the stable-rule count at every rung")
    for c in COSTS:
        hc = pdf[pdf.cost == c]
        rr = []
        for a, b in [("U56", "B136"), ("U56", "SMALL"), ("B136", "SMALL")]:
            va = [hc[(hc.panel == a) & (hc.chooser == ch)].pct.mean() for ch in CHOOSERS]
            vb = [hc[(hc.panel == b) & (hc.chooser == ch)].pct.mean() for ch in CHOOSERS]
            rr.append(spearman(va, vb))
        sc = hc.pivot_table(index="chooser", columns="panel", values="pct").reindex(CHOOSERS)
        al = sc.loc["CELL_ALPHA"]
        ns = sum(1 for ch in CHOOSERS if ch != "CELL_ALPHA"
                 and bool((sc.loc[ch, PANEL_NAMES] > 0.5).all())
                 and bool((sc.loc[ch, PANEL_NAMES] > al[PANEL_NAMES]).all()))
        log(f"   {c:3d} bps: pooled rho {np.nanmedian(rr):+.4f}  "
            f"(U56-B136 {rr[0]:+.3f}, U56-SMALL {rr[1]:+.3f}, B136-SMALL {rr[2]:+.3f})   "
            f"stable rules {ns} of 6   4a {int(hc.keep4a.sum())}  4b {int(hc.keep4b.sum())}")

    pd.DataFrame(_gates).to_csv(OUT.with_suffix(".gates.csv"), index=False)
    rhos.to_csv(OUT.with_suffix(".rho.csv"), index=False)
    OUT.with_suffix(".log.txt").write_text("\n".join(_log) + "\n")
    log(f"\n# wrote {OUT.name}.{{grid,choosers,rho,gates}}.csv and .log.txt")


if __name__ == "__main__":
    main()
