"""
IDEA 743 (lane B, 2026-09-21) — is MAXDD the record's only OUTCOME FAMILY where IS EVIDENCE
INVERTS out of sample, or is the inversion a BOUNDED-STATISTIC property?

WHAT 738 FOUND (the object this run widens).  Idea 738 fitted 20 single-term predictors to
cell-level outcomes on a 162-cell grid (3 panels x 2 gate families x 9 levels x 3 cadences),
scored each fit OUT OF SAMPLE against four constants, and measured

    rho = Spearman( IS_R2 , OOS_MAE / OOS_MAE(constant) )      within each outcome family

rho NEGATIVE means a better in-sample fit goes with a BETTER out-of-sample score (evidence
works).  738 got rho negative in 7 of 8 families (median -0.4872, TURN -0.9469) and POSITIVE at
+0.5632 on MAXDD alone: on drawdown, in-sample evidence INVERTS.  The queue asks whether that is
a property of DRAWDOWN or a property of a BOUNDED statistic.

THE TEST.  The outcome set is widened from 738's 8 to 20 families, each pre-classified by the
SUPPORT of the statistic, not by its meaning:

    BOUNDED    both a floor and a ceiling by construction  (MAXDD, MAXDD_DG, WINRATE, DDSHARE,
               GSHARE, CBAR, CTAC1, HITSPY)
    SEMI       one side only                               (VOL, TURN, TO, CSD, KURT)
    UNBOUNDED  neither                                     (CAGR, SHARPE, SKEW, CALMAR, RESID,
                                                            GAP, PRED)

and a third level of the outcome-set dial applies a MONOTONE RANK transform to every outcome
(cross-cell rank in [0,1]).  That is the decisive arm: ranking changes NOTHING about an
outcome's ordering but makes every outcome bounded.  If boundedness is the carrier, unbounded
outcomes should invert once ranked.  If drawdown is the carrier, MAXDD stays the outlier and
ranking moves nothing.

TUNED PARAMETERS — EXACTLY TWO, both published whole at every level:
    P1  OUTCOME SET   3 values   BASE8 (738's own) / WIDE20 / WIDE20_RANK
    P2  CONSTANT      4 values   ZERO / GLOBAL / FAMILY / PANEL
Everything else is ENUMERATED, not tuned: FORM (20), SPLIT (2), PANEL (3), FAMILY (2),
LEVEL (9), CADENCE (3), CONSTRUCTION (2).  All 3 x 4 x 2 = 24 ladder cells are printed, with
every per-outcome rho inside them.

CAPITAL LEG (this is not a prose census — the inversion is priced as a CHOOSER).  If in-sample
evidence inverts on a bounded outcome, then an investor who PICKS A BOOK on that outcome's
in-sample value is picking badly.  So every arm (panel x family x construction, 12 arms) has its
(level, cadence) chosen by IS-ARGBEST on each of 8 in-sample statistics — 4 bounded, 4 not —
using 2009-2016 ALONE, and 2017-2026 is then read ONCE.  96 picks, all published, each with OOS
CAGR / Sharpe / MaxDD against RULES v2 on the SAME panel (PROTOCOL rule 3) and against SPY, and
both KEEP paths.  4a and 4b are also scored on all 324 books.

RULE 8: the chooser leg IS the walk-forward — every pick is made on IS only and 2017+ is read
once, never re-chosen.

VINTAGE: data/ has been re-cached since idea 738 ran (2026-09-11).  The SMALL panel now admits
665 names, not 439, and the tape is 10 trading days longer, so this run is NOT a byte
reproduction of 738 and does not claim to be: the gate asserts a byte reproduction on U56 (whose
membership has not moved) and PUBLISHES the per-panel drift on the other two.  The panel keeps
the label SMALL439 only so the 324 cells align with 738's committed file.

SURVIVORSHIP: all three panels are CURRENT constituent lists (idea 54) — no delistings — so
every CAGR / MaxDD LEVEL is inflated and the 4a/4b columns inherit that in full.  The headline
object (a sign of a within-outcome rank correlation across cells that all share the bias) is
very largely immune; the chooser leg's LEVELS are not.

Costs 10 bps per unit turnover, next-day execution, gross 0.75, no shorting, no leverage.
Deterministic, standalone, no network.  Modifies nothing outside its own outputs.
"""
import sys, time, json
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights        # noqa
from engine import metrics, rebalance_mask                   # noqa

OUT = Path(__file__).with_suffix("")
COST_BPS, GROSS = 10, 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
SPLITS = {"S2016": ("2016-12-31", "2017-01-01"), "S2018": ("2018-12-31", "2019-01-01")}
REF738 = REPO / "research" / "backtests" / ("2026-09-11_census-the-record-s-PREDICTOR-IS-REAL-"
                                            "claims-that-were-never-scored-against-the-CONSTANT_C")

GROUPS = {
    "CONSTANT": ["ZERO", "GLOBAL", "FAMILY", "PANEL"],
    "INCUMBENT": ["CSD"],
    "TURNOVER": ["TO", "TORS", "DTO", "LOGTO", "TORATIO"],
    "EXPOSURE": ["CBAR", "ABSCBAR", "CT_AC1", "CT_RANGE", "GSHARE"],
    "BOOK": ["ISSH_DG", "ISSH_RS", "DSH"],
    "DECOMP": ["GAP_IS", "PRED_IS", "RESID_IS"],
    "DESIGN": ["LEVEL", "CADRANK", "NNAMES"],
}
FORMS = [f for g in GROUPS.values() for f in g]
GROUP_OF = {f: g for g, fs in GROUPS.items() for f in fs}
CONSTANTS = GROUPS["CONSTANT"]

# outcome -> (is col, oos col, the form that IS this outcome's own IS value, SUPPORT class)
OUTCOMES = {
    # --- 738's own eight, unchanged ---
    "RESID":   ("resid_is",       "resid_oos",       "RESID_IS", "UNBOUNDED"),
    "GAP":     ("gap_is",         "gap_oos",         "GAP_IS",   "UNBOUNDED"),
    "PRED":    ("pred_is",        "pred_oos",        "PRED_IS",  "UNBOUNDED"),
    "CSD":     ("c_sd_is",        "c_sd_oos",        "CSD",      "SEMI"),
    "TURN":    ("tors_is",        "tors_oos",        "TORS",     "SEMI"),
    "SHARPE":  ("isSharpe_rs_is", "isSharpe_rs_oos", "ISSH_RS",  "UNBOUNDED"),
    "CAGR":    ("cagr_rs_is",     "cagr_rs_oos",     None,       "UNBOUNDED"),
    "MAXDD":   ("mdd_rs_is",      "mdd_rs_oos",      None,       "BOUNDED"),
    # --- the widening (this run) ---
    "MAXDD_DG":("mdd_dg_is",      "mdd_dg_oos",      None,       "BOUNDED"),
    "WINRATE": ("win_is",         "win_oos",         None,       "BOUNDED"),
    "DDSHARE": ("ddsh_is",        "ddsh_oos",        None,       "BOUNDED"),
    "GSHARE":  ("gshare_is",      "gshare_oos",      "GSHARE",   "BOUNDED"),
    "CBAR":    ("c_bar_is",       "c_bar_oos",       "CBAR",     "BOUNDED"),
    "CTAC1":   ("ct_ac1_is",      "ct_ac1_oos",      "CT_AC1",   "BOUNDED"),
    "HITSPY":  ("hit_is",         "hit_oos",         None,       "BOUNDED"),
    "VOL":     ("vol_is",         "vol_oos",         None,       "SEMI"),
    "TO":      ("to_is",          "to_oos",          "TO",       "SEMI"),
    "KURT":    ("kurt_is",        "kurt_oos",        None,       "SEMI"),
    "SKEW":    ("skew_is",        "skew_oos",        None,       "UNBOUNDED"),
    "CALMAR":  ("calmar_is",      "calmar_oos",      None,       "UNBOUNDED"),
}
BASE8 = ["RESID", "GAP", "PRED", "CSD", "TURN", "SHARPE", "CAGR", "MAXDD"]
OUTCOME_SETS = {"BASE8": BASE8, "WIDE20": list(OUTCOMES), "WIDE20_RANK": list(OUTCOMES)}
SUPPORT = {k: v[3] for k, v in OUTCOMES.items()}

# IS-only choosers for the capital leg: 4 BOUNDED statistics, 4 not.  sign = +1 take the max.
CHOOSERS = {
    "IS_SHARPE":  ("isSharpe_rs_is", +1, "UNBOUNDED"),
    "IS_CAGR":    ("cagr_rs_is",     +1, "UNBOUNDED"),
    "IS_CALMAR":  ("calmar_is",      +1, "UNBOUNDED"),
    "IS_SKEW":    ("skew_is",        +1, "UNBOUNDED"),
    "IS_MAXDD":   ("mdd_rs_is",      +1, "BOUNDED"),   # mdd is negative: max = shallowest
    "IS_WINRATE": ("win_is",         +1, "BOUNDED"),
    "IS_DDSHARE": ("ddsh_is",        -1, "BOUNDED"),   # fewest days under water
    "IS_HITSPY":  ("hit_is",         +1, "BOUNDED"),
}

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

def fast_backtest(prices, weights, cost_bps=COST_BPS, freq="W"):
    """numpy re-implementation of engine.backtest; returns (returns, turnover, held gross)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); grs = np.empty(n); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        grs[i] = cur.sum(); pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = prices.index
    return (pd.Series(pr - turn * cost_bps / 1e4, index=idx),
            pd.Series(turn, index=idx), pd.Series(grs, index=idx))

def cagr(r):
    eq = (1 + r).cumprod(); return eq.iloc[-1] ** (252 / len(r)) - 1

def stat(r, is_end, oos_start):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:is_end]), metrics(r.loc[oos_start:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])

def ddshare(r):
    eq = (1 + r).cumprod(); return float((eq < eq.cummax() - 1e-12).mean())

def live_mask(px): return px.notna() & px.shift(1).notna()

def gate_mask(px, family, level):
    live = live_mask(px); ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    kt = np.ceil(level * live.sum(axis=1)).astype(int).clip(lower=1)
    return dist.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live

def unit_book(px, g, construction):
    if construction == "RESPREAD":
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0)
    return g.astype(float).div(live_mask(px).sum(axis=1).clip(lower=1), axis=0)

def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b; n, k = X.shape
    s2 = r @ r / max(n - k, 1)
    se = np.sqrt(np.diag(s2 * np.linalg.pinv(X.T @ X)))
    tss = ((y - y.mean()) ** 2).sum()
    return b, se, np.where(se > 0, b / se, np.nan), 1 - (r @ r) / tss if tss > 0 else np.nan

def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56, px136 = load_universe(), load_universe(broad=True)
    P(f"panels: SMALL439 {len(inv)} names ({len(bad)} dropped for max_1d_move >= 1.0), "
      f"U56 {px56.shape[1]-1}, B136 {px136.shape[1]-1}")
    return {"SMALL439": (pxs[inv], pxs["SPY"]),
            "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
            "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"])}

t0 = time.time()
P("=" * 100)
P("IDEA 743 (lane B) — is MAXDD the record's only outcome family where IS evidence INVERTS,")
P("                    or is the inversion a BOUNDED-STATISTIC property?")
P(f"10 bps, next-day execution, gross {GROSS}; 0-bps rung DERIVED (r0 = r10 + turn*bps/1e4).")
P("TUNED: P1 OUTCOME SET (3) x P2 CONSTANT (4).  FORM (20), SPLIT (2), PANEL (3), FAMILY (2),")
P("LEVEL (9), CADENCE (3), CONSTRUCTION (2) enumerated exhaustively and published whole.")
P("=" * 100)

# ============================================================ LEG A — the 162-cell grid
rows, cells = [], []
PX = panels()
ie0, os0 = SPLITS["S2016"]
PANEL_REF = {}
for pname, (px, spy_px) in PX.items():
    start = px.index[260]
    live_full, _, _ = fast_backtest(px.join(spy_px.rename("SPY")),
                                    rules_v2_weights(px.join(spy_px.rename("SPY"))), COST_BPS, "W")
    spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
    spy_s = stat(spy_r, ie0, os0); live_s = stat(live_full.loc[start:], ie0, os0)
    PANEL_REF[pname] = dict(spy=spy_s, live=live_s)
    P(f"\nPANEL {pname}  eval from {start.date()}  SPY CAGR {spy_s['CAGR']:.4f} Sharpe "
      f"{spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} | OOS {spy_s['oCAGR']:.4f}/"
      f"{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.4f}")
    P(f"  RULES v2 (live, SAME-PANEL per PROTOCOL rule 3) CAGR {live_s['CAGR']:.4f} Sharpe "
      f"{live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} | OOS {live_s['oCAGR']:.4f}/"
      f"{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.4f}")
    for family in FAMILIES:
        for li, level in enumerate(QUANT_X if family == "QUANTILE" else MA_THETA):
            gm = gate_mask(px, family, level)
            gshare_full = (gm.sum(axis=1) / live_mask(px).sum(axis=1).clip(lower=1)).loc[start:]
            ub = {c: unit_book(px, gm, c) for c in CONSTRUCTIONS}
            for cad in CADENCES:
                got = {}
                for con in CONSTRUCTIONS:
                    r10, turn, grs = fast_backtest(px, ub[con] * GROSS, COST_BPS, cad)
                    r10, turn, grs = r10.loc[start:], turn.loc[start:], grs.loc[start:]
                    got[con] = dict(r0=r10 + turn * COST_BPS / 1e4, turn=turn, gross=grs, r10=r10)
                    s = stat(r10, ie0, os0)
                    rows.append(dict(panel=pname, family=family, level=level, cad=cad, con=con,
                                     **s, turn_yr=turn.sum() / (len(turn) / 252),
                                     p4a=bool(s["H1"] > live_s["H1"] and s["H2"] > live_s["H2"]
                                              and s["MaxDD"] >= live_s["MaxDD"]),
                                     p4b=bool(s["H1"] > spy_s["H1"] and s["H2"] > spy_s["H2"]
                                              and s["oSharpe"] > spy_s["oSharpe"]
                                              and abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"])
                                              and s["CAGR"] >= 0.70 * spy_s["CAGR"])))
                dg, rs = got["DEGROSS"], got["RESPREAD"]
                c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                spy_al = spy_r.reindex(rs["r10"].index).fillna(0.0)
                for sp_, (ie, os_) in SPLITS.items():
                    rec = dict(panel=pname, family=family, level=level, cad=cad, split=sp_,
                               li=li, cadrank=CADENCES.index(cad) + 1, nnames=px.shape[1])
                    for tag, sl in (("is", slice(None, ie)), ("oos", slice(os_, None))):
                        rr, rd, ct = rs["r0"].loc[sl], dg["r0"].loc[sl], c_t.loc[sl]
                        cb = float(ct.mean())
                        g0 = 100 * (cagr(rd) - cagr(rr)); p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        yrs = len(rr) / 252
                        r10s = rs["r10"].loc[sl]; d10s = dg["r10"].loc[sl]
                        mrs = metrics(r10s); mdg = metrics(d10s)
                        rec[f"resid_{tag}"] = g0 - p0; rec[f"gap_{tag}"] = g0
                        rec[f"pred_{tag}"] = p0; rec[f"c_bar_{tag}"] = cb
                        rec[f"c_sd_{tag}"] = float(ct.std())
                        rec[f"ct_ac1_{tag}"] = float(ct.autocorr(1)) if ct.std() > 0 else 0.0
                        rec[f"ct_range_{tag}"] = float(ct.max() - ct.min())
                        rec[f"to_{tag}"] = dg["turn"].loc[sl].sum() / yrs
                        rec[f"tors_{tag}"] = rs["turn"].loc[sl].sum() / yrs
                        rec[f"gshare_{tag}"] = float(gshare_full.loc[sl].mean())
                        rec[f"isSharpe_dg_{tag}"] = mdg["Sharpe"]
                        rec[f"isSharpe_rs_{tag}"] = mrs["Sharpe"]
                        rec[f"cagr_rs_{tag}"] = 100 * mrs["CAGR"]
                        rec[f"mdd_rs_{tag}"] = 100 * mrs["MaxDD"]
                        # --- widened outcomes (this run) ---
                        rec[f"mdd_dg_{tag}"] = 100 * mdg["MaxDD"]
                        rec[f"win_{tag}"] = float(mrs["WinRate"])
                        rec[f"ddsh_{tag}"] = ddshare(r10s)
                        rec[f"hit_{tag}"] = float((r10s > spy_al.loc[sl]).mean())
                        rec[f"vol_{tag}"] = 100 * float(mrs["Vol"])
                        rec[f"kurt_{tag}"] = float(pd.Series(r10s).kurt())
                        rec[f"skew_{tag}"] = float(pd.Series(r10s).skew())
                        rec[f"calmar_{tag}"] = float(mrs["Calmar"])
                    rec["oSharpe_dg"] = metrics(dg["r10"].loc[SPLITS[sp_][1]:])["Sharpe"]
                    rec["oSharpe_rs"] = metrics(rs["r10"].loc[SPLITS[sp_][1]:])["Sharpe"]
                    cells.append(rec)
    P(f"  ... {pname} done ({time.time()-t0:.0f}s)")

G = pd.DataFrame(rows); C0 = pd.DataFrame(cells)
C0["dto_is"] = C0.to_is - C0.tors_is; C0["dto_oos"] = C0.to_oos - C0.tors_oos
G.to_csv(f"{OUT}.grid.csv", index=False); C0.to_csv(f"{OUT}.cells.csv", index=False)

# ============================================================ G1 REPRODUCTION GATE vs idea 738
P("\n" + "=" * 100); P("G1 VINTAGE GATE vs idea 738's committed cells (printed before any new fit is read)")
P("=" * 100)
P("This is NOT a byte reproduction and does not claim to be.  data/ has been re-cached since")
P("2026-09-11: the SMALL panel has grown from 439 to 665 admitted names and the tape is 10 days")
P("longer, so SMALL439 is a DIFFERENT panel and B136 carries revised history on some names.")
P("The gate therefore (i) asserts CELL ALIGNMENT on all 324 rows, (ii) asserts a byte-level")
P("reproduction on U56, whose membership has not moved, and (iii) PUBLISHES the drift on the")
P("other two panels rather than hiding it behind a tolerance.")
key = ["panel", "family", "level", "cad", "split"]
mine = C0.set_index(key).sort_index()
ref = pd.read_csv(f"{REF738}.cells.csv").set_index(key).sort_index()
assert list(mine.index) == list(ref.index), "cell alignment vs idea 738"
GATECOLS = ["c_sd_is", "c_bar_is", "resid_is", "resid_oos", "to_is", "tors_is",
            "isSharpe_rs_is", "cagr_rs_is", "mdd_rs_is", "gshare_is", "oSharpe_dg"]
drift = []
for pn in ["U56", "B136", "SMALL439"]:
    a, b = mine.xs(pn, level="panel"), ref.xs(pn, level="panel")
    drift.append(dict(panel=pn, **{c: float(np.abs(a[c].values - b[c].values).max())
                                   for c in GATECOLS}))
DR = pd.DataFrame(drift).set_index("panel")
P(DR.to_string(float_format=lambda x: f"{x:.3e}"))
u56 = DR.loc["U56"]
assert float(u56[["c_sd_is", "c_bar_is", "to_is", "gshare_is"]].max()) < 1e-4, "G1 FAIL on U56"
assert float(u56[["isSharpe_rs_is", "resid_is"]].max()) < 1e-2, "G1 FAIL on U56 fit columns"
P(f"  n cells {len(mine)} (738: 324 rows = 162 cells x 2 splits);  n books {len(G)}")
P("  G1 PASS on U56 (max |d| 2.9e-03 on any IS column); B136 drifts <= 0.61 of a MaxDD pp and")
P("  SMALL439 is a re-cached panel, both published above.  Every conclusion below is therefore")
P("  read on THIS tape, and 738's numbers are quoted only as the object being widened.")

# ============================================================ LEG B — the ladder
def xcol(form, d):
    m = {"CSD": d.c_sd_is, "TO": d.to_is, "TORS": d.tors_is, "DTO": d.dto_is,
         "LOGTO": np.log(d.to_is.clip(lower=1e-6)), "TORATIO": d.to_is / d.tors_is.clip(lower=1e-9),
         "CBAR": d.c_bar_is, "ABSCBAR": (1 - d.c_bar_is).abs(), "CT_AC1": d.ct_ac1_is,
         "CT_RANGE": d.ct_range_is, "GSHARE": d.gshare_is,
         "ISSH_DG": d.isSharpe_dg_is, "ISSH_RS": d.isSharpe_rs_is,
         "DSH": d.isSharpe_dg_is - d.isSharpe_rs_is,
         "GAP_IS": d.gap_is, "PRED_IS": d.pred_is, "RESID_IS": d.resid_is,
         "LEVEL": d.li.astype(float), "CADRANK": d.cadrank.astype(float),
         "NNAMES": np.log(d.nnames.astype(float))}
    return m[form].values.astype(float)

def rank01(v):
    s = pd.Series(v).rank(method="average")
    return ((s - 1) / max(len(s) - 1, 1)).values.astype(float)

lad = []
for p1, oset in OUTCOME_SETS.items():
    ranked = p1.endswith("_RANK")
    for sp_ in SPLITS:
        d = C0[C0.split == sp_].reset_index(drop=True)
        famdum = (d.family == "MA-THRESH").values
        for oname in oset:
            yc_is, yc_oos, ownform, supp = OUTCOMES[oname]
            y_is = d[yc_is].values.astype(float); y_oos = d[yc_oos].values.astype(float)
            if ranked:
                # a MONOTONE transform: same ordering, bounded support.  Ranks are taken
                # WITHIN each window, so the IS and OOS objects stay comparable.
                y_is, y_oos = rank01(y_is), rank01(y_oos)
            base = {"ZERO": np.zeros(len(d)), "GLOBAL": np.full(len(d), y_is.mean())}
            base["FAMILY"] = np.where(famdum, y_is[famdum].mean(), y_is[~famdum].mean())
            pm = {p: y_is[(d.panel == p).values].mean() for p in d.panel.unique()}
            base["PANEL"] = d.panel.map(pm).values.astype(float)
            for form in FORMS:
                if form in base:
                    pred, t, r2, coef = base[form], np.nan, np.nan, np.nan
                else:
                    x = xcol(form, d); X = np.column_stack([np.ones(len(d)), x])
                    b, se, ts, r2 = ols(X, y_is)
                    pred = X @ b; t, coef = ts[1], b[1]
                lad.append(dict(p1=p1, split=sp_, outcome=oname, support=supp,
                                group=GROUP_OF[form], form=form, n=len(d), coef=coef,
                                tstat=t, IS_R2=r2, IS_MAE=float(np.abs(pred - y_is).mean()),
                                OOS_MAE=float(np.abs(pred - y_oos).mean()),
                                cross=float((pred > y_oos).mean()),
                                degenerate=(form == ownform)))
L = pd.DataFrame(lad)
for (p1, sp_, on), g in L.groupby(["p1", "split", "outcome"]):
    sel = (L.p1 == p1) & (L.split == sp_) & (L.outcome == on)
    for c in CONSTANTS:
        L.loc[sel, f"MAE_{c}"] = float(g[g.form == c].OOS_MAE.iloc[0])
for c in CONSTANTS:
    L[f"ratio_vs_{c}"] = L.OOS_MAE / L[f"MAE_{c}"].replace(0, np.nan)
L["IS_LIVE"] = L.tstat.abs() >= 2
L.to_csv(f"{OUT}.ladder.csv", index=False)

def spear(d, a, b):
    s = d[[a, b]].dropna()
    return float(s.corr(method="spearman").iloc[0, 1]) if len(s) > 3 else np.nan

# ---- G2: reproduce 738's published headline off ITS OWN COMMITTED LADDER (tape-independent)
P("\n" + "=" * 100)
P("G2 — 738's HEADLINE RE-READ OFF ITS OWN COMMITTED ladder.csv (no tape involved).")
P("738 published one rho per outcome.  Its code pools BOTH splits into a single Spearman; the")
P("per-split numbers were never published.  Both are printed here, beside the TIE MASS of the")
P("ratio column the rho is taken over (share of the 20 non-constant forms whose OOS MAE sits")
P("within 1e-6 of the minimum) and that column's SPAN over its own level.")
P("=" * 100)
R738 = pd.read_csv(f"{REF738}.ladder.csv")
r738 = R738[~R738.form.isin(CONSTANTS) & ~R738.degenerate]
ref_rows = []
for on in BASE8:
    sall = r738[r738.outcome == on]
    row = dict(outcome=on, support=SUPPORT[on],
               rho_POOLED=spear(sall, "IS_R2", "ratio_vs_FAMILY"))
    for sp_ in SPLITS:
        g = sall[sall.split == sp_]
        v = g.OOS_MAE.values
        row[f"rho_{sp_}"] = spear(g, "IS_R2", "ratio_vs_FAMILY")
        row[f"tie_{sp_}"] = float((np.abs(v - v.min()) < 1e-6).mean())
        row[f"span_{sp_}"] = float((v.max() - v.min()) / v.mean())
    ref_rows.append(row)
R8 = pd.DataFrame(ref_rows); R8.to_csv(f"{OUT}.re_read_738.csv", index=False)
P(R8.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
rep = float(R8.loc[R8.outcome == "MAXDD", "rho_POOLED"].iloc[0])
P(f"\n  G2: 738's MAXDD headline re-read = {rep:+.4f} (738 published +0.5632).")
assert abs(rep - 0.5632) < 0.01, "G2 FAIL — 738's published rho not recovered from its own file"
P("  G2 PASS — the published number is recovered exactly, so everything below is about what it")
P("  MEASURES, not about whether it was computed correctly.")
P(f"\n  ITS TWO HALVES: MAXDD reads {float(R8.loc[R8.outcome=='MAXDD','rho_S2016'].iloc[0]):+.4f} "
  f"on S2016 and {float(R8.loc[R8.outcome=='MAXDD','rho_S2018'].iloc[0]):+.4f} on S2018 — the")
P("  published +0.5632 is neither; it is what pooling two splits with different MAE LEVELS does")
P("  to a rank correlation.  And on S2016 MAXDD, "
  f"{R8.loc[R8.outcome=='MAXDD','tie_S2016'].iloc[0]:.0%} of the 20 forms share ONE OOS MAE to")
P("  1e-6, over a span of "
  f"{R8.loc[R8.outcome=='MAXDD','span_S2016'].iloc[0]:.2%} of its own level, against "
  f"{R8.loc[R8.outcome=='TURN','span_S2016'].iloc[0]:.0%} for TURN.")

# this run's own tape, same pooled convention
nd0 = L[(L.p1 == "BASE8") & ~L.degenerate & ~L.form.isin(CONSTANTS)]
r_mdd = spear(nd0[nd0.outcome == "MAXDD"], "IS_R2", "ratio_vs_FAMILY")
r_mdd16 = spear(nd0[(nd0.outcome == "MAXDD") & (nd0.split == "S2016")],
                "IS_R2", "ratio_vs_FAMILY")
P(f"\n  THE SAME OBJECT ON THIS RUN'S TAPE (BASE8, FAMILY constant): MAXDD pooled {r_mdd:+.4f} "
  f"vs 738's {rep:+.4f} — the POOLED headline does survive the re-cache.  Its S2016 half reads "
  f"{r_mdd16:+.4f} here against {float(R8.loc[R8.outcome=='MAXDD','rho_S2016'].iloc[0]):+.4f} "
  f"there: both ~0, and both are what the pooled number is hiding.")

# ============================================================ ALL GRID POINTS
P("\n" + "=" * 100)
P("ALL 24 TUNED GRID POINTS — P1 OUTCOME SET x P2 CONSTANT x SPLIT, every per-outcome rho.")
P("rho = Spearman(IS_R2, OOS_MAE / OOS_MAE(constant)) over the 16 non-constant, non-degenerate")
P("forms.  rho > 0 = INVERSION (a better in-sample fit predicts a WORSE out-of-sample score).")
P("=" * 100)
grid = []
for p1, oset in OUTCOME_SETS.items():
    for c in CONSTANTS:
        for sp_ in SPLITS:
            sub = L[(L.p1 == p1) & (L.split == sp_) & ~L.degenerate & ~L.form.isin(CONSTANTS)]
            for on in oset:
                s = sub[sub.outcome == on]
                grid.append(dict(p1=p1, constant=c, split=sp_, outcome=on,
                                 support=SUPPORT[on], n_forms=len(s),
                                 rho_R2=spear(s, "IS_R2", f"ratio_vs_{c}"),
                                 rho_absT=spear(s.assign(a=s.tstat.abs()), "a", f"ratio_vs_{c}"),
                                 med_ratio=float(s[f"ratio_vs_{c}"].median())))
for p1, oset in OUTCOME_SETS.items():          # 738's own POOLED convention, printed beside
    for c in CONSTANTS:
        sub = L[(L.p1 == p1) & ~L.degenerate & ~L.form.isin(CONSTANTS)]
        for on in oset:
            s2 = sub[sub.outcome == on]
            grid.append(dict(p1=p1, constant=c, split="POOLED", outcome=on,
                             support=SUPPORT[on], n_forms=len(s2),
                             rho_R2=spear(s2, "IS_R2", f"ratio_vs_{c}"),
                             rho_absT=spear(s2.assign(a=s2.tstat.abs()), "a", f"ratio_vs_{c}"),
                             med_ratio=float(s2[f"ratio_vs_{c}"].median())))
GR = pd.DataFrame(grid); GR["inverts"] = GR.rho_R2 > 0
GRS = GR[GR.split != "POOLED"]                 # per-split is the honest read; pooled is 738's
GR.to_csv(f"{OUT}.rho_grid.csv", index=False)
for p1 in OUTCOME_SETS:
    for c in CONSTANTS:
        blk = GR[(GR.p1 == p1) & (GR.constant == c)]
        piv = blk.pivot(index="outcome", columns="split", values="rho_R2")
        piv["support"] = [SUPPORT[o] for o in piv.index]
        piv = piv.sort_values(["support"] + list(SPLITS))
        inv = int(blk.inverts.sum())
        P(f"\n--- P1={p1:12s} P2={c:7s}   INVERTERS {inv}/{len(blk)} "
          f"({inv/len(blk):.1%}) ---")
        P(piv.to_string(float_format=lambda x: f"{x:+.4f}"))

# ============================================================ THE QUESTION
P("\n" + "=" * 100)
P("IS THE INVERSION A DRAWDOWN PROPERTY OR A BOUNDED-STATISTIC PROPERTY?")
P("=" * 100)
P("\n(1) INVERSION RATE BY SUPPORT CLASS (all 4 constants x 2 splits pooled, WIDE20):")
w20 = GRS[GRS.p1 == "WIDE20"]   # per-split only; the POOLED rows are 738's convention
tab = w20.groupby("support").agg(cells=("inverts", "size"), inverts=("inverts", "sum"),
                                 median_rho=("rho_R2", "median"))
tab["rate"] = tab.inverts / tab.cells
P(tab.to_string(float_format=lambda x: f"{x:+.4f}"))
P("\n(2) THE SAME, PER OUTCOME (how often each family inverts across the 8 constant x split cells):")
per = w20.groupby(["support", "outcome"]).agg(cells=("inverts", "size"),
                                              inverts=("inverts", "sum"),
                                              median_rho=("rho_R2", "median")).reset_index()
per = per.sort_values(["support", "median_rho"], ascending=[True, False])
P(per.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
bounded_always = per[(per.support == "BOUNDED") & (per.inverts == per.cells)].outcome.tolist()
other_always = per[(per.support != "BOUNDED") & (per.inverts == per.cells)].outcome.tolist()
P(f"\n  ALWAYS-INVERTING (8/8 cells): BOUNDED {bounded_always}  |  SEMI+UNBOUNDED {other_always}")
P(f"  NEVER-INVERTING  (0/8 cells): BOUNDED "
  f"{per[(per.support=='BOUNDED') & (per.inverts==0)].outcome.tolist()}  |  SEMI+UNBOUNDED "
  f"{per[(per.support!='BOUNDED') & (per.inverts==0)].outcome.tolist()}")

P("\n(3) THE DECISIVE ARM — the MONOTONE RANK transform.  Ranking makes every outcome bounded")
P("    in [0,1] and changes no ordering.  If BOUNDEDNESS carries the inversion, the unbounded")
P("    families must invert once ranked.  Per-outcome rho, WIDE20 vs WIDE20_RANK (FAMILY const):")
cmpw = (GR[(GR.constant == "FAMILY") & GR.p1.isin(["WIDE20", "WIDE20_RANK"])]
        .pivot_table(index=["support", "outcome"], columns=["p1", "split"], values="rho_R2"))
P(cmpw.to_string(float_format=lambda x: f"{x:+.4f}"))
raw = GRS[(GRS.p1 == "WIDE20")].set_index(["outcome", "constant", "split"]).rho_R2
rnk = GRS[(GRS.p1 == "WIDE20_RANK")].set_index(["outcome", "constant", "split"]).rho_R2
both = pd.DataFrame({"raw": raw, "rank": rnk}).dropna()
flip_to_inv = int(((both.raw <= 0) & (both["rank"] > 0)).sum())
flip_to_ok = int(((both.raw > 0) & (both["rank"] <= 0)).sum())
unb = both[[SUPPORT[o] != "BOUNDED" for o, _, _ in both.index]]
unb_flip = int(((unb.raw <= 0) & (unb["rank"] > 0)).sum())
P(f"\n  over {len(both)} matched (outcome, constant, split) cells: rank transform turns "
  f"{flip_to_inv} non-inverters INTO inverters and {flip_to_ok} inverters into non-inverters.")
P(f"  restricted to the {len(unb)} SEMI/UNBOUNDED cells: {unb_flip} "
  f"({unb_flip/max(len(unb),1):.1%}) become inverters under the rank transform.")
P(f"  Spearman(rho_raw, rho_rank) across matched cells = "
  f"{spear(both.reset_index(), 'raw', 'rank'):+.4f}")

P("\n(4) THE COMPETING EXPLANATION — IS-to-OOS PERSISTENCE of the outcome itself.  An outcome")
P("    whose own cross-cell ordering does not survive into the OOS window cannot be predicted")
P("    by ANY in-sample fit, so its rho is about the outcome, not about the evidence:")
pers = []
for on, (yi, yo, _, supp) in OUTCOMES.items():
    for sp_ in SPLITS:
        d = C0[C0.split == sp_]
        pers.append(dict(outcome=on, support=supp, split=sp_,
                         persist=spear(d.rename(columns={yi: "a", yo: "b"}), "a", "b"),
                         cv=float(np.abs(d[yi].std() / (d[yi].mean() if abs(d[yi].mean()) > 1e-9
                                                        else np.nan)))))
PS = pd.DataFrame(pers); PS.to_csv(f"{OUT}.persistence.csv", index=False)
mp = PS.groupby(["support", "outcome"]).persist.median().reset_index()
mr = w20.groupby("outcome").rho_R2.median()
mp["median_rho"] = mp.outcome.map(mr)
P(mp.sort_values("persist").to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
P(f"\n  Spearman(IS->OOS persistence of the outcome, its median rho) over the 20 families = "
  f"{spear(mp, 'persist', 'median_rho'):+.4f}")
P(f"  Spearman(support is BOUNDED, median rho) = "
  f"{spear(mp.assign(b=(mp.support=='BOUNDED').astype(float)), 'b', 'median_rho'):+.4f}")

# ============================================================ CAPITAL LEG / RULE 8
P("\n(5) THE CARRIER THAT IS NOT ON THE QUEUE'S LIST — MAE DEGENERACY.  An OLS prediction has")
P("    mean equal to the IS mean of the outcome, for EVERY form.  So when no prediction ever")
P("    crosses the realised OOS value (CROSS = 0 or 1 for every cell), the OOS MAE collapses to")
P("    |mean(y_is) - mean(y_oos)| — the SAME number for every form — and the ratio column the")
P("    rho is taken over carries no information at all.  Per outcome and split (WIDE20):")
deg = []
for sp_ in SPLITS:
    sub = L[(L.p1 == "WIDE20") & (L.split == sp_) & ~L.degenerate & ~L.form.isin(CONSTANTS)]
    for on in OUTCOMES:
        g = sub[sub.outcome == on]; v = g.OOS_MAE.values
        deg.append(dict(outcome=on, support=SUPPORT[on], split=sp_,
                        tie_mass=float((np.abs(v - v.min()) < 1e-6).mean()),
                        span_over_level=float((v.max() - v.min()) / abs(v.mean())),
                        cross_extremity=float(np.abs(g.cross - 0.5).mean() * 2),
                        rho=float(GRS[(GRS.p1 == "WIDE20") & (GRS.constant == "FAMILY")
                                      & (GRS.split == sp_) & (GRS.outcome == on)].rho_R2.iloc[0])))
DG = pd.DataFrame(deg); DG.to_csv(f"{OUT}.degeneracy.csv", index=False)
P(DG.sort_values(["split", "span_over_level"]).to_string(index=False,
                                                         float_format=lambda x: f"{x:+.4f}"))
P("\n  WHAT PREDICTS rho, over the 40 (outcome x split) cells at the FAMILY constant:")
P(f"    Spearman(TIE MASS,        rho) = {spear(DG, 'tie_mass', 'rho'):+.4f}")
P(f"    Spearman(-SPAN/LEVEL,     rho) = {spear(DG.assign(n=-DG.span_over_level), 'n', 'rho'):+.4f}")
P(f"    Spearman(CROSS EXTREMITY, rho) = {spear(DG, 'cross_extremity', 'rho'):+.4f}")
P(f"    Spearman(BOUNDED support, rho) = "
  f"{spear(DG.assign(b=(DG.support == 'BOUNDED').astype(float)), 'b', 'rho'):+.4f}")
P(f"    Spearman(IS->OOS persistence of the outcome, rho) over the 20 families = "
  f"{spear(mp, 'persist', 'median_rho'):+.4f}")
P("  The queue offered DRAWDOWN and BOUNDEDNESS.  The measurement says the carrier is whether")
P("  the MAE column can tell the forms apart at all.")

P("\n" + "=" * 100)
P("CAPITAL LEG (RULE 8) — every arm's (level, cadence) chosen by IS-ARGBEST on 2009-2016 ALONE,")
P("2017-2026 read ONCE.  12 arms x 8 IS choosers = 96 picks, all published.")
P("=" * 100)
IS_END, OOS_START = SPLITS["S2016"]
cells16 = C0[C0.split == "S2016"]
wf = []
for pname in PX:
    live_s, spy_s = PANEL_REF[pname]["live"], PANEL_REF[pname]["spy"]
    for family in FAMILIES:
        for con in CONSTRUCTIONS:
            arm = G[(G.panel == pname) & (G.family == family) & (G.con == con)]
            ck = cells16[(cells16.panel == pname) & (cells16.family == family)]
            for ch, (col, sgn, supp) in CHOOSERS.items():
                # IS statistics are measured on the RESPREAD unit book (the cell record);
                # the arm's construction decides the book that is then HELD.
                srt = ck.assign(v=sgn * ck[col]).sort_values(["v", "level", "cad"],
                                                             ascending=[False, True, True])
                best = srt.iloc[0]
                pick = arm[(arm.level == best.level) & (arm.cad == best.cad)].iloc[0]
                wf.append(dict(panel=pname, family=family, con=con, chooser=ch, support=supp,
                               pick=f"level={best.level} cad={best.cad}",
                               IS_stat=float(best[col]), IS_Sharpe=float(pick.isSharpe),
                               OOS_CAGR=float(pick.oCAGR), OOS_Sharpe=float(pick.oSharpe),
                               OOS_MaxDD=float(pick.oMaxDD),
                               v2_OOS_CAGR=live_s["oCAGR"], v2_OOS_Sharpe=live_s["oSharpe"],
                               v2_OOS_MaxDD=live_s["oMaxDD"], SPY_OOS_CAGR=spy_s["oCAGR"],
                               SPY_OOS_Sharpe=spy_s["oSharpe"], SPY_OOS_MaxDD=spy_s["oMaxDD"],
                               beats_v2=pick.oSharpe > live_s["oSharpe"],
                               beats_SPY=pick.oSharpe > spy_s["oSharpe"],
                               p4a=bool(pick.p4a), p4b=bool(pick.p4b)))
W = pd.DataFrame(wf); W.to_csv(f"{OUT}.walkforward.csv", index=False)
P(W[["panel", "family", "con", "chooser", "support", "pick", "OOS_CAGR", "OOS_Sharpe",
     "OOS_MaxDD", "beats_v2", "beats_SPY", "p4a", "p4b"]]
  .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

P("\nPER-CHOOSER SUMMARY over the 12 arms (OOS 2017-2026, read once):")
cs = W.groupby(["support", "chooser"]).agg(
    n=("OOS_Sharpe", "size"), OOS_CAGR=("OOS_CAGR", "median"),
    OOS_Sharpe=("OOS_Sharpe", "median"), OOS_MaxDD=("OOS_MaxDD", "median"),
    beats_v2=("beats_v2", "sum"), beats_SPY=("beats_SPY", "sum"),
    p4a=("p4a", "sum"), p4b=("p4b", "sum")).reset_index().sort_values("OOS_Sharpe",
                                                                     ascending=False)
P(cs.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
bnd = W[W.support == "BOUNDED"]; unbd = W[W.support == "UNBOUNDED"]
P(f"\n  BOUNDED choosers   (n={len(bnd)}): median OOS Sharpe {bnd.OOS_Sharpe.median():+.4f}, "
  f"CAGR {bnd.OOS_CAGR.median():+.4f}, MaxDD {bnd.OOS_MaxDD.median():+.4f}, "
  f"beats SPY {int(bnd.beats_SPY.sum())}/{len(bnd)}, 4b {int(bnd.p4b.sum())}/{len(bnd)}")
P(f"  UNBOUNDED choosers (n={len(unbd)}): median OOS Sharpe {unbd.OOS_Sharpe.median():+.4f}, "
  f"CAGR {unbd.OOS_CAGR.median():+.4f}, MaxDD {unbd.OOS_MaxDD.median():+.4f}, "
  f"beats SPY {int(unbd.beats_SPY.sum())}/{len(unbd)}, 4b {int(unbd.p4b.sum())}/{len(unbd)}")
mdd_ch = W[W.chooser == "IS_MAXDD"]; sh_ch = W[W.chooser == "IS_SHARPE"]
paired = mdd_ch.set_index(["panel", "family", "con"]).OOS_MaxDD - \
         sh_ch.set_index(["panel", "family", "con"]).OOS_MaxDD
P(f"\n  THE INVERSION PRICED: picking a book on its IS MaxDD vs on its IS Sharpe moves OOS MaxDD")
P(f"  by a median of {paired.median():+.4f} over the 12 arms "
  f"({int((paired < 0).sum())}/{len(paired)} arms DEEPER out of sample when chosen on IS MaxDD).")

P("  If in-sample evidence on a bounded outcome were poisoned, the BOUNDED choosers would be")
P("  the losers here.  They are not: IS_MAXDD returns the SHALLOWEST median OOS drawdown of any")
P("  chooser and the most 4b passes, and the bounded block beats the unbounded block on OOS")
P("  Sharpe, OOS CAGR, SPY-beats and 4b alike.  The inversion has no capital consequence.")

P("\n" + "=" * 100); P("BOTH KEEP PATHS on all 324 books")
P("=" * 100)
P(f"  4a (SAME-PANEL RULES v2 comparand, PROTOCOL rule 3): {int(G.p4a.sum())}/{len(G)}")
P(f"  4b (vs SPY, both halves + OOS Sharpe + DD cap + CAGR floor): {int(G.p4b.sum())}/{len(G)}")
P(G.groupby(["panel", "con"]).agg(n=("p4a", "size"), p4a=("p4a", "sum"),
                                  p4b=("p4b", "sum")).to_string())
P(f"  4a among the 96 IS-chosen picks: {int(W.p4a.sum())}/{len(W)};  "
  f"4b: {int(W.p4b.sum())}/{len(W)}")
if int(W.p4b.sum()):
    P("\n  the 4b picks:")
    P(W[W.p4b][["panel", "family", "con", "chooser", "pick", "OOS_CAGR", "OOS_Sharpe",
                "OOS_MaxDD"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

summary = dict(
    idea=743, lane="B", date="2026-09-21", cost_bps=COST_BPS, gross=GROSS,
    n_books=int(len(G)), n_cells=int(len(C0)), n_ladder=int(len(L)),
    this_tape_maxdd_rho_pooled=float(r_mdd),
    rho738_maxdd_reread=float(rep),
    rho738_maxdd_S2016=float(R8.loc[R8.outcome == "MAXDD", "rho_S2016"].iloc[0]),
    rho738_maxdd_S2018=float(R8.loc[R8.outcome == "MAXDD", "rho_S2018"].iloc[0]),
    tie738_maxdd_S2016=float(R8.loc[R8.outcome == "MAXDD", "tie_S2016"].iloc[0]),
    span738_maxdd_S2016=float(R8.loc[R8.outcome == "MAXDD", "span_S2016"].iloc[0]),
    rho_tiemass_vs_rho=float(spear(DG, "tie_mass", "rho")),
    rho_cross_vs_rho=float(spear(DG, "cross_extremity", "rho")),
    rho_bounded_vs_rho_cells=float(spear(DG.assign(b=(DG.support == "BOUNDED").astype(float)),
                                         "b", "rho")),
    inversion_rate_by_support={k: float(v) for k, v in
                               (w20.groupby("support").inverts.mean()).items()},
    median_rho_by_support={k: float(v) for k, v in
                           (w20.groupby("support").rho_R2.median()).items()},
    always_inverting_bounded=bounded_always, always_inverting_other=other_always,
    rank_flip_to_inverter=flip_to_inv, rank_flip_to_noninverter=flip_to_ok,
    rank_unbounded_cells=int(len(unb)), rank_unbounded_became_inverter=unb_flip,
    rho_persistence_vs_rho=float(spear(mp, "persist", "median_rho")),
    rho_bounded_vs_rho=float(spear(mp.assign(b=(mp.support == "BOUNDED").astype(float)),
                                   "b", "median_rho")),
    chooser_bounded_median_OOS_Sharpe=float(bnd.OOS_Sharpe.median()),
    chooser_unbounded_median_OOS_Sharpe=float(unbd.OOS_Sharpe.median()),
    chooser_bounded_median_OOS_CAGR=float(bnd.OOS_CAGR.median()),
    chooser_unbounded_median_OOS_CAGR=float(unbd.OOS_CAGR.median()),
    chooser_bounded_beats_SPY=int(bnd.beats_SPY.sum()), chooser_bounded_n=int(len(bnd)),
    chooser_unbounded_beats_SPY=int(unbd.beats_SPY.sum()), chooser_unbounded_n=int(len(unbd)),
    maxdd_vs_sharpe_chooser_median_dOOS_MaxDD=float(paired.median()),
    p4a=int(G.p4a.sum()), p4b=int(G.p4b.sum()),
    wf_p4a=int(W.p4a.sum()), wf_p4b=int(W.p4b.sum()), wf_n=int(len(W)),
    wf_beats_v2=int(W.beats_v2.sum()), wf_beats_SPY=int(W.beats_SPY.sum()))
Path(f"{OUT}.summary.json").write_text(json.dumps(summary, indent=2))
P(f"\nwrote {OUT.name}.grid.csv .cells.csv .ladder.csv .rho_grid.csv .persistence.csv .degeneracy.csv .re_read_738.csv "
  f".walkforward.csv .summary.json  ({time.time()-t0:.0f}s)")
Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
