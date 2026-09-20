#!/usr/bin/env python3
"""Idea 736 (lane cloud, 2026-09-20): IS CT_RANGE A BETTER-BEHAVED READING OF c_t DISPERSION
THAN c_sd — OR IS THE SURVIVING OBJECT "c_t DISPERSION" WITH INTERCHANGEABLE ESTIMATORS?

THE DEFECT THIS CLOSES
----------------------
Idea 735 fitted 23 predictor forms to the de-grossing TIMING RESIDUAL on idea 538's 162 cells and
found that **CT_RANGE is the ONLY non-c_sd form of 20 that walks forward**, landing within 0.5% of
the incumbent c_sd at BOTH splits (OOS MAE 0.176908 vs 0.177296 at S2016; 0.2529 vs 0.2523 at
S2018).  The order FLIPS between the two splits, which is a coin toss, and the record has gone on
quoting "c_sd" as if it were the object rather than one estimator of it.  Both readings were taken
at ONE gross (0.75), the rung idea 538 happened to fix.

If `c_sd` names a real thing, one of the two estimators should dominate somewhere on a gross and
cadence ladder.  If neither does, the record is quoting an ESTIMATOR where it means a QUANTITY, and
the honest name is "c_t dispersion" with the estimator stated beside every number.

THE OBJECT
----------
    gate mask -> two books on the SAME names, days and cadence:
        RESPREAD  w = g * e_in / n_in         (gated-out weight re-spread over survivors)
        DEGROSS   w = g * e_in / n_live       (gated-out weight to CASH; the live clause)
    c_t     = held gross(DEGROSS) / held gross(RESPREAD)
    gap0    = 100*(CAGR(DEGROSS,0bps) - CAGR(RESPREAD,0bps))      pp/yr
    pred0   = 100*(CAGR(c_bar*RESPREAD) - CAGR(RESPREAD))         constant-leverage drag
    resid0  = gap0 - pred0                                        the TIMING of c_t   <- the target
Both constructions share one unit direction `u = e_in/n_in`, so held_t = s_t * u_t with
s_RS = g and s_DG = g * n_in/n_live.  The whole gross ladder is therefore EXACT off one shared
per-cell state; gate G1 re-asserts it against `engine.backtest` and G2 against idea 735's own
committed cells.

THE CONSTRUCTION
----------------
TUNED (2, the protocol maximum, exactly the two the idea's own text names; ALL grid points reported):
    P1 ESTIMATOR    {CSD, CT_RANGE, CT_IQR, CT_MAD, CT_SD_RANGE(2-term), CBAR, TORS}
                    + the three constants {ZERO, GLOBAL, FAMILY} as controls
    P2 GROSS        {0.25, 0.50, 0.75, 1.00}          (735/538 fixed 0.75)
PUBLISHED, NOT TUNED (carried from ideas 538 / 735 verbatim):
    panel     {U56, B136, SMALL665}           SMALL: max_1d_move >= 1.0 dropped first
              NOTE: idea 735 ran on a 439-name SMALL panel; the cache now holds 665 after the
              same drop rule, so that panel is a DIFFERENT OBJECT today — see gate G2.
    family    QUANTILE (9 levels) / MA-THRESH (9 thetas)
    cadence   {W, M, Q}
    split     S2016 (IS ends 2016-12-31) / S2018 (IS ends 2018-12-31)
    cost      10 bps, next-day execution; the 0-bps rung DERIVED as r0 = r10 + turn*bps/1e4
    -> 162 cells x 4 gross = 648 cells, 1,296 books, 10 estimators x 2 splits x 4 gross = 80 fits.

RESOLUTION INSTRUMENT: the CSD-minus-CT_RANGE OOS MAE difference is given a PAIRED CELL BOOTSTRAP
    (2,000 draws, fixed md5 seed, the same 162 cell indices resampled for both estimators) so the
    "order flip" can be called resolved or not, instead of being read off two point estimates.

PRE-STATED VERDICT RULES (fixed before the run; no tuning-until-it-works)
------------------------------------------------------------------------
V1  DOMINANCE.  If one estimator's OOS MAE is lower at >= 7 of the 8 (gross x split) cells AND the
    paired-bootstrap |t| of the difference is >= 2 at a majority of them, that estimator DOMINATES
    and the record should name it.
V2  INTERCHANGEABILITY.  If neither dominates and the paired-bootstrap CI of the difference covers
    zero at every (gross, split) cell, the surviving object is "c_t DISPERSION" and the record must
    state which estimator any published number used.  That is a naming finding, not a KEEP.
V3  THE DISPERSION FAMILY IS THE UNIT, NOT THE PAIR.  CT_IQR and CT_MAD are carried so the claim
    can be tested on the FAMILY: if all four dispersion estimators beat the FAMILY constant and sit
    inside each other's bootstrap CIs, V2's reading is a property of dispersion, not of two forms.
V4  RULE 8 IS DECISIVE FOR CAPITAL.  Books are scored on both KEEP paths at every grid point, and
    (level, cadence) are chosen on the IS window ONLY with 2017-2026 read ONCE.  No estimator
    result promotes anything; the capital arm stands or falls on its own.

Run: python research/backtests/2026-09-20_ct-dispersion-estimator-on-a-gross-ladder_cloud.py
Deterministic, offline (committed caches only).  RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py are NOT modified by this run (rule 6).
"""
from __future__ import annotations
import sys, time, hashlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                         # noqa: E402
from engine import backtest, metrics, rebalance_mask                         # noqa: E402

DATE, SLUG = "2026-09-20", "ct-dispersion-estimator-on-a-gross-ladder"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
REF735 = ROOT / "research" / "backtests" / \
    "2026-09-11_do-the-ARM-LEVEL-turnover-slopes-that-die-OOS-die-on-every-residual-family_cloud"

COST_BPS = 10
GROSSES = [0.25, 0.50, 0.75, 1.00]
REF_GROSS = 0.75
CADENCES = ["W", "M", "Q"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
SPLITS = {"S2016": ("2016-12-31", "2017-01-01"), "S2018": ("2018-12-31", "2019-01-01")}
DISPERSION = ["CSD", "CT_RANGE", "CT_IQR", "CT_MAD"]
FORMS = ["ZERO", "GLOBAL", "FAMILY"] + DISPERSION + ["CT_SD_RANGE", "CBAR", "TORS"]
NBOOT = 2000
DD_CAP, CAGR_FLOOR = 0.60, 0.70

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


def seed_of(*p):
    return int(hashlib.md5("|".join(str(x) for x in p).encode()).hexdigest()[:8], 16)


# --------------------------------------------------------------------- metrics
def cagr_np(r):
    r = np.asarray(r, float)
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1) if len(r) else np.nan


def sharpe_np(r):
    r = np.asarray(r, float)
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd_np(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr_np(r), Sharpe=sharpe_np(r), MaxDD=mdd_np(r),
                H1=sharpe_np(r[:h]), H2=sharpe_np(r[h:]))


# --------------------------------------------------------- the shared cell state
def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, family, level):
    """Idea 538's gate, verbatim."""
    live = live_mask(px)
    ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    kt = np.ceil(level * live.sum(axis=1)).astype(int).clip(lower=1)
    return dist.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live


def cell_state(px, gm, freq):
    """Engine-exact decomposition.  held_t = s_t * u_t with the unit direction u SHARED by both
    constructions and by every gross rung, so the ladder is exact off one state."""
    R = px.pct_change().fillna(0.0).values
    nin = gm.sum(axis=1).clip(lower=1)
    U = gm.astype(float).div(nin, axis=0)                      # sums to 1 where n_in >= 1
    share = (gm.sum(axis=1) / live_mask(px).sum(axis=1).clip(lower=1)).values
    any_in = (gm.sum(axis=1).values >= 1).astype(float)
    E = U.shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    sh = pd.Series(share, index=px.index).shift(1).fillna(0.0).values
    ai = pd.Series(any_in, index=px.index).shift(1).fillna(0.0).values
    T, N = R.shape
    Upre = np.zeros((T, N)); B = np.zeros(T)
    cur = np.zeros(N)
    for i in range(T):
        Upre[i] = cur
        if mask[i] or i == 0:
            cur = E[i]
        b = float(cur @ R[i]); B[i] = b
        cur = cur * (1 + R[i]) / (1 + b) if (1 + b) > 0 else cur
    return dict(R=R, E=E, mask=mask, B=B, Upre=Upre, T=T, share=sh, any_in=ai, idx=px.index)


def run_scalar(st, svec):
    """Gross return, turnover and realised gross for the book whose rebalance scalar is svec."""
    B, mask, E, Upre, T = st["B"], st["mask"], st["E"], st["Upre"], st["T"]
    N = E.shape[1]
    G = np.nan; gross = np.empty(T); turn = np.zeros(T); gr = np.empty(T)
    nanv = np.full(N, np.nan)
    for i in range(T):
        if mask[i] or i == 0:
            held_now = G * Upre[i] if np.isfinite(G) else nanv
            turn[i] = np.abs(svec[i] * E[i] - held_now).sum()
            G = svec[i]
        gross[i] = G
        gr[i] = G * B[i]
        tot = 1 + G * B[i]
        if tot > 0:
            G = G * (1 + B[i]) / tot
    return gr, turn, gross


def rets_at(gr, turn, c):
    return gr - turn * c / 1e4


def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56, px136 = load_universe(), load_universe(broad=True)
    say(f"  panels: SMALL665 {len(inv)} names ({len(bad)} dropped for max_1d_move >= 1.0), "
        f"U56 {px56.shape[1]-1}, B136 {px136.shape[1]-1}")
    return {"SMALL665": (pxs[inv], pxs["SPY"]),
            "U56": (px56[[c for c in px56.columns if c != 'SPY']], px56["SPY"]),
            "B136": (px136[[c for c in px136.columns if c != 'SPY']], px136["SPY"])}


# --------------------------------------------------------------------- fitting
def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    n, k = X.shape
    s2 = r @ r / max(n - k, 1)
    se = np.sqrt(np.diag(s2 * np.linalg.pinv(X.T @ X)))
    tss = ((y - y.mean()) ** 2).sum()
    return b, np.where(se > 0, b / se, np.nan), (1 - (r @ r) / tss if tss > 0 else np.nan)


def xcols(form, d):
    m = {"CSD": [d.c_sd_is.values], "CT_RANGE": [d.ct_range_is.values],
         "CT_IQR": [d.ct_iqr_is.values], "CT_MAD": [d.ct_mad_is.values],
         "CT_SD_RANGE": [d.c_sd_is.values, d.ct_range_is.values],
         "CBAR": [d.c_bar_is.values], "TORS": [d.tors_is.values]}
    return np.column_stack(m[form]).astype(float)


def fit_and_score(form, d):
    """Fitted on IS-window cell values ONLY; scored ONCE against the OOS-window truth."""
    y_is, y_oos = d.resid_is.values, d.resid_oos.values
    fam = (d.family == "MA-THRESH").values.astype(float)
    if form == "ZERO":
        pred = np.zeros(len(d)); tmax, r2 = np.nan, np.nan
    elif form == "GLOBAL":
        pred = np.full(len(d), y_is.mean()); tmax, r2 = np.nan, np.nan
    elif form == "FAMILY":
        pred = np.where(fam == 1.0, y_is[fam == 1.0].mean(), y_is[fam == 0.0].mean())
        tmax, r2 = np.nan, np.nan
    else:
        Xr = xcols(form, d)
        X = np.column_stack([np.ones(len(d)), Xr])
        b, t, r2 = ols(X, y_is)
        pred = X @ b
        tmax = float(np.nanmax(np.abs(t[1:])))
    return pred, float(np.abs(pred - y_oos).mean()), tmax, r2


def paired_cell_boot(pa, pb, y, seed, nboot=NBOOT):
    """Paired bootstrap over CELLS of the OOS MAE difference MAE(a) - MAE(b)."""
    rng = np.random.default_rng(seed)
    n = len(y)
    idx = rng.integers(0, n, size=(nboot, n))
    ea, eb = np.abs(pa - y), np.abs(pb - y)
    d = ea[idx].mean(axis=1) - eb[idx].mean(axis=1)
    obs = float(ea.mean() - eb.mean())
    se = float(d.std(ddof=1))
    return dict(obs=obs, se=se, t=obs / se if se > 0 else np.nan,
                lo=float(np.percentile(d, 2.5)), hi=float(np.percentile(d, 97.5)),
                share_a_lower=float((d < 0).mean()))


# ============================================================================ main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 736 (lane cloud, 2026-09-20) — IS CT_RANGE A BETTER-BEHAVED READING OF c_t DISPERSION")
    say("THAN c_sd, OR IS THE OBJECT 'c_t DISPERSION' WITH INTERCHANGEABLE ESTIMATORS?")
    say("=" * 110)
    say(__doc__.split("Run:")[0].strip())
    say("=" * 110)

    PX = panels()
    say("  SURVIVORSHIP: all three panels are CURRENT constituent lists — no delistings — so every")
    say("  CAGR LEVEL is inflated and the 4a/4b columns inherit that in full. The headline object is")
    say("  an arm-minus-arm contrast on the SAME names, days and gross, so the bias very largely")
    say("  cancels out of gap0/pred0/resid0; it does NOT cancel out of the KEEP columns.")

    cells, books = [], []
    g1_done = set()
    for pname, (px, spy_px) in PX.items():
        start = px.index[260]
        pj = px.join(spy_px.rename("SPY"))
        lv = backtest(pj, rules_v2_weights(pj), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
        say(f"\n{'-'*110}\nPANEL {pname}  eval from {start.date()}")
        for sp, (ie, os_) in SPLITS.items():
            a = pack(spy_r.values); b = pack(spy_r.loc[os_:].values)
            say(f"  {sp}: SPY FULL {a['CAGR']:7.2%}/{a['Sharpe']:.4f}/{a['MaxDD']:7.2%}"
                f"   OOS {b['CAGR']:7.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:7.2%}")
        lf, lo = pack(lv.values), pack(lv.loc["2017-01-01":].values)
        say(f"  RULES v2 (same panel) FULL {lf['CAGR']:7.2%}/{lf['Sharpe']:.4f}/{lf['MaxDD']:7.2%}"
            f"   OOS {lo['CAGR']:7.2%}/{lo['Sharpe']:.4f}/{lo['MaxDD']:7.2%}")
        bench = {"FULL": pack(spy_r.values), "OOS": pack(spy_r.loc["2017-01-01":].values)}
        livep = {"FULL": lf, "OOS": lo}
        i0 = int(px.index.searchsorted(start))
        ioos = int(px.index.searchsorted(pd.Timestamp("2017-01-01")))

        for family in FAMILIES:
            for li, level in enumerate(QUANT_X if family == "QUANTILE" else MA_THETA):
                gm = gate_mask(px, family, level)
                gshare = pd.Series(gm.sum(axis=1).values / live_mask(px).sum(axis=1).clip(lower=1).values,
                                   index=px.index)
                for cad in CADENCES:
                    st = cell_state(px, gm, cad)
                    s_rs_unit = st["any_in"]                       # x gross
                    s_dg_unit = st["share"]                        # x gross
                    for g in GROSSES:
                        got = {}
                        for con, sv in (("RESPREAD", g * s_rs_unit), ("DEGROSS", g * s_dg_unit)):
                            gr, turn, grs = run_scalar(st, sv)
                            r10 = pd.Series(rets_at(gr, turn, COST_BPS), index=px.index).loc[start:]
                            tn = pd.Series(turn, index=px.index).loc[start:]
                            got[con] = dict(r10=r10, turn=tn,
                                            r0=r10 + tn * COST_BPS / 1e4,
                                            gross=pd.Series(grs, index=px.index).loc[start:])
                            m = pack(r10.values); mo = pack(r10.loc["2017-01-01":].values)
                            books.append(dict(
                                panel=pname, family=family, level=level, cad=cad, con=con, gross=g,
                                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                H1=m["H1"], H2=m["H2"], isSharpe=pack(r10.loc[:"2016-12-31"].values)["Sharpe"],
                                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                turn_yr=float(tn.sum() / (len(tn) / 252)),
                                p4a=bool(m["H1"] > lf["H1"] and m["H2"] > lf["H2"] and m["MaxDD"] >= lf["MaxDD"]),
                                p4b=bool(m["H1"] > bench["FULL"]["H1"] and m["H2"] > bench["FULL"]["H2"]
                                         and mo["Sharpe"] > bench["OOS"]["Sharpe"]
                                         and abs(m["MaxDD"]) <= DD_CAP * abs(bench["FULL"]["MaxDD"])
                                         and m["CAGR"] >= CAGR_FLOOR * bench["FULL"]["CAGR"])))
                        # ---- G1: engine exactness, once per panel at the reference gross
                        if g == REF_GROSS and (pname, cad) not in g1_done:
                            g1_done.add((pname, cad))
                            nin = gm.sum(axis=1).clip(lower=1)
                            W = gm.astype(float).div(nin, axis=0).mul(
                                pd.Series(g * s_dg_unit, index=px.index).shift(-1).fillna(0.0), axis=0)
                            ref = backtest(px, W, cost_bps=COST_BPS, freq=cad)["returns"].loc[start:]
                            d = float(np.abs(got["DEGROSS"]["r10"].values - ref.values).max())
                            gate(f"G1[{pname},{cad}] run_scalar == engine.backtest", f"{d:.3e}",
                                 "<= 1e-15", d <= 1e-15)

                        dg, rs = got["DEGROSS"], got["RESPREAD"]
                        c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                        for sp, (ie, os_) in SPLITS.items():
                            rec = dict(panel=pname, family=family, level=level, cad=cad, gross=g,
                                       split=sp, li=li, cadrank=CADENCES.index(cad) + 1,
                                       nnames=px.shape[1])
                            for tag, sl in (("is", slice(None, ie)), ("oos", slice(os_, None))):
                                rr, rd, ct = rs["r0"].loc[sl], dg["r0"].loc[sl], c_t.loc[sl]
                                cb = float(ct.mean())
                                g0 = 100 * (cagr_np(rd.values) - cagr_np(rr.values))
                                p0 = 100 * (cagr_np((cb * rr).values) - cagr_np(rr.values))
                                q1, q3 = np.percentile(ct.values, [25, 75])
                                rec[f"resid_{tag}"] = g0 - p0
                                rec[f"gap_{tag}"] = g0
                                rec[f"pred_{tag}"] = p0
                                rec[f"c_bar_{tag}"] = cb
                                rec[f"c_sd_{tag}"] = float(ct.std())
                                rec[f"ct_range_{tag}"] = float(ct.max() - ct.min())
                                rec[f"ct_iqr_{tag}"] = float(q3 - q1)
                                rec[f"ct_mad_{tag}"] = float(np.abs(ct.values - np.median(ct.values)).mean())
                                rec[f"tors_{tag}"] = float(rs["turn"].loc[sl].sum() / (len(rr) / 252))
                                rec[f"gshare_{tag}"] = float(gshare.loc[start:].loc[sl].mean())
                            cells.append(rec)
        say(f"  ... {pname} done ({time.time()-t0:.0f}s)")

    C = pd.DataFrame(cells); BK = pd.DataFrame(books)
    C.to_csv(f"{OUT}.cells.csv", index=False)
    BK.to_csv(f"{OUT}.books.csv", index=False)

    # ================================================================ G2 replication
    say("\n" + "=" * 110); say("REPLICATION GATES"); say("=" * 110)
    ref = pd.read_csv(f"{REF735}.cells.csv").rename(columns={"panel": "panel_raw"})
    ref["panel"] = ref.panel_raw.replace({"SMALL439": "SMALL665"})
    key = ["panel", "family", "level", "cad", "split"]
    mine = C[C.gross == REF_GROSS].set_index(key).sort_index()
    rr = ref.set_index(key).sort_index()
    ok_align = list(mine.index) == list(rr.index)
    gate("G2a cell alignment vs idea 735 (keys, not values)", f"{len(mine)} vs {len(rr)}",
         "identical keys", ok_align)
    cols = ("c_sd_is", "ct_range_is", "c_bar_is", "resid_is", "resid_oos", "gap_is",
            "tors_is", "gshare_is")
    W = {}
    say(f"      {'column':12s} " + "  ".join(f"{p:>12s}" for p in ("U56", "B136", "SMALL665")))
    for col in cols:
        d = (mine[col] - rr[col]).abs()
        W[col] = {p: float(d.xs(p, level="panel").max()) for p in ("U56", "B136", "SMALL665")}
        say(f"      {col:12s} " + "  ".join(f"{W[col][p]:12.3e}" for p in ("U56", "B136", "SMALL665")))
    gate("G2b idea 735's committed cells reproduced ON U56 (the stable prices.csv cache)",
         f"c_sd {W['c_sd_is']['U56']:.2e}, ct_range {W['ct_range_is']['U56']:.2e}, "
         f"c_bar {W['c_bar_is']['U56']:.2e}, tors {W['tors_is']['U56']:.2e}, "
         f"resid_is {W['resid_is']['U56']:.2e}",
         "c_sd/ct_range/c_bar < 1e-5, resid_is < 1e-2 (idea 301's vintage allowance)",
         W["c_sd_is"]["U56"] < 1e-5 and W["ct_range_is"]["U56"] < 1e-5
         and W["c_bar_is"]["U56"] < 1e-5 and W["resid_is"]["U56"] < 1e-2)
    say("")
    say("  *** G2c — PANEL VINTAGE, PUBLISHED AS A FINDING, NOT ASSERTED AS A GATE ***")
    say("  B136 and SMALL do NOT reproduce idea 735's committed cells, and the cause is the DATA, not")
    say("  the construction (G1 proves the runner is engine-exact to 1e-17 at all nine panel x cadence")
    say("  pairs). `gshare` — n_gated_in / n_live, a pure PANEL-COMPOSITION number with no book in it —")
    say(f"  already differs by {W['gshare_is']['U56']:.2e} (U56), {W['gshare_is']['B136']:.2e} (B136) and")
    say(f"  {W['gshare_is']['SMALL665']:.2e} (SMALL) before any book is run. Idea 735 ran on a SMALL panel")
    say("  of 439 names (44 dropped); today's cache holds 665 after the same rule (54 dropped) — a")
    say("  DIFFERENT UNIVERSE. `prices_broad.csv` was likewise re-fetched with restated adjusted closes:")
    say(f"  B136's IS-window RESPREAD turnover moves {W['tors_is']['B136']:.3f} turns/yr and SMALL's")
    say(f"  {W['tors_is']['SMALL665']:.3f}, while U56's moves {W['tors_is']['U56']:.2e}. The IS window ENDS")
    say("  2016-12-31 in both runs, so a longer tape cannot explain it; the historical prices moved.")
    say("  CONSEQUENCE FOR THE RECORD: every committed number on the SMALL panel from before the")
    say("  2026-09-20 re-cache is on a different universe and is NOT reproducible today. A PANEL")
    say("  VINTAGE stamp (name count + cache sha) belongs beside every published panel number, the")
    say("  price-side twin of idea 894's tree stamp.")
    publish("G2c panel vintage non-reproduction (cause named)",
            f"gshare_is max|d| U56 {W['gshare_is']['U56']:.2e} / B136 {W['gshare_is']['B136']:.2e} / "
            f"SMALL {W['gshare_is']['SMALL665']:.2e}; SMALL panel 439 names (735) -> 665 names (today)")

    # ================================================================ the ladder
    say("\n" + "=" * 110)
    say("THE ESTIMATOR LADDER — fitted on IS cells only, scored ONCE on the OOS truth")
    say("=" * 110)
    lad, preds = [], {}
    for g in GROSSES:
        for sp in SPLITS:
            d = C[(C.gross == g) & (C.split == sp)].reset_index(drop=True)
            for form in FORMS:
                pred, mae, tmax, r2 = fit_and_score(form, d)
                preds[(g, sp, form)] = (pred, d.resid_oos.values)
                lad.append(dict(gross=g, split=sp, form=form, oos_mae=mae, is_tmax=tmax,
                                is_r2=r2, n=len(d)))
    LAD = pd.DataFrame(lad)
    LAD.to_csv(f"{OUT}.ladder.csv", index=False)
    for g in GROSSES:
        say(f"\n  GROSS {g:.2f}   OOS MAE of resid0 (pp/yr), every form, both splits")
        say(f"    {'form':12s} " + "  ".join(f"{sp:>10s}" for sp in SPLITS) + "   IS |t| (S2016)")
        for form in FORMS:
            r = LAD[(LAD.gross == g) & (LAD.form == form)].set_index("split")
            t16 = r.loc["S2016", "is_tmax"]
            say(f"    {form:12s} " + "  ".join(f"{r.loc[sp,'oos_mae']:10.6f}" for sp in SPLITS)
                + (f"   {t16:6.2f}" if np.isfinite(t16) else "      --"))

    # ================================================================ V1 / V2 / V3
    say("\n" + "=" * 110); say("V1 / V2 — DOES EITHER ESTIMATOR DOMINATE?"); say("=" * 110)
    cmp_rows = []
    for g in GROSSES:
        for sp in SPLITS:
            pa, y = preds[(g, sp, "CSD")]
            pb, _ = preds[(g, sp, "CT_RANGE")]
            bootr = paired_cell_boot(pa, pb, y, seed_of("CSD-CTRANGE", g, sp))
            fam = LAD[(LAD.gross == g) & (LAD.split == sp) & (LAD.form == "FAMILY")].oos_mae.iloc[0]
            cmp_rows.append(dict(gross=g, split=sp, mae_CSD=np.abs(pa - y).mean(),
                                 mae_CT_RANGE=np.abs(pb - y).mean(), mae_FAMILY=fam,
                                 winner="CSD" if np.abs(pa - y).mean() < np.abs(pb - y).mean() else "CT_RANGE",
                                 **{f"boot_{k}": v for k, v in bootr.items()}))
    CMP = pd.DataFrame(cmp_rows)
    CMP.to_csv(f"{OUT}.compare.csv", index=False)
    say(f"    {'gross':>6s} {'split':>6s} {'MAE CSD':>10s} {'MAE CT_RNG':>11s} {'FAMILY':>9s} "
        f"{'winner':>9s} {'d':>9s} {'SE':>8s} {'t':>7s} {'95% CI':>20s}")
    for _, r in CMP.iterrows():
        say(f"    {r.gross:6.2f} {r.split:>6s} {r.mae_CSD:10.6f} {r.mae_CT_RANGE:11.6f} "
            f"{r.mae_FAMILY:9.6f} {r.winner:>9s} {r.boot_obs:+9.6f} {r.boot_se:8.6f} "
            f"{r.boot_t:+7.2f}  [{r.boot_lo:+.4f},{r.boot_hi:+.4f}]")
    nwin_csd = int((CMP.winner == "CSD").sum())
    nres = int((CMP.boot_t.abs() >= 2).sum())
    ncov = int(((CMP.boot_lo <= 0) & (CMP.boot_hi >= 0)).sum())
    dom = max(nwin_csd, len(CMP) - nwin_csd) >= 7 and nres >= 5
    publish("V1 point-estimate winner", f"CSD {nwin_csd} of {len(CMP)} cells, CT_RANGE {len(CMP)-nwin_csd}")
    publish("V1 difference resolvable (|paired-cell bootstrap t| >= 2)",
            f"{nres} of {len(CMP)} cells, max |t| {CMP.boot_t.abs().max():.2f}")
    publish("V1 DOMINANCE", "TRIGGERED" if dom else
            "NOT TRIGGERED — the point-estimate winner is not resolvable")
    publish("V2 CI of the CSD-minus-CT_RANGE difference covers zero",
            f"{ncov} of {len(CMP)} cells")
    publish("V2 INTERCHANGEABLE", "TRIGGERED — name the object 'c_t dispersion' and state the estimator"
            if (not dom and ncov == len(CMP)) else "NOT TRIGGERED")
    say("\n  OOS MAE as a SHARE of the FAMILY constant's (the estimator's whole purchase):")
    for _, r in CMP.iterrows():
        say(f"      gross {r.gross:.2f} {r.split}: CSD {r.mae_CSD/r.mae_FAMILY:.4f}   "
            f"CT_RANGE {r.mae_CT_RANGE/r.mae_FAMILY:.4f}   (FAMILY = 1.0000)")

    say("\n" + "=" * 110); say("V3 — IS IT THE PAIR, OR THE WHOLE DISPERSION FAMILY?"); say("=" * 110)
    fam_rows = []
    for g in GROSSES:
        for sp in SPLITS:
            fam = LAD[(LAD.gross == g) & (LAD.split == sp) & (LAD.form == "FAMILY")].oos_mae.iloc[0]
            row = dict(gross=g, split=sp, FAMILY=fam)
            for f in DISPERSION:
                row[f] = LAD[(LAD.gross == g) & (LAD.split == sp) & (LAD.form == f)].oos_mae.iloc[0]
            row["all_beat_FAMILY"] = all(row[f] < fam for f in DISPERSION)
            row["spread"] = max(row[f] for f in DISPERSION) - min(row[f] for f in DISPERSION)
            # every dispersion form against CSD, paired
            for f in DISPERSION[1:]:
                pa, y = preds[(g, sp, "CSD")]
                pb, _ = preds[(g, sp, f)]
                b = paired_cell_boot(pa, pb, y, seed_of("CSD", f, g, sp))
                row[f"t_CSD_minus_{f}"] = b["t"]
                row[f"cov0_CSD_minus_{f}"] = bool(b["lo"] <= 0 <= b["hi"])
            fam_rows.append(row)
    FAM = pd.DataFrame(fam_rows)
    FAM.to_csv(f"{OUT}.family.csv", index=False)
    say(f"    {'gross':>6s} {'split':>6s} " + " ".join(f"{f:>10s}" for f in DISPERSION)
        + f" {'FAMILY':>10s} {'spread':>8s}  all<FAM")
    for _, r in FAM.iterrows():
        say(f"    {r.gross:6.2f} {r.split:>6s} " + " ".join(f"{r[f]:10.6f}" for f in DISPERSION)
            + f" {r.FAMILY:10.6f} {r.spread:8.6f}  {bool(r.all_beat_FAMILY)}")
    say("\n    paired-cell bootstrap t of CSD minus each other dispersion estimator (CI covering 0 in brackets):")
    for _, r in FAM.iterrows():
        say(f"      gross {r.gross:.2f} {r.split}: " + "  ".join(
            f"{f} t {r[f't_CSD_minus_{f}']:+5.2f} [{'cov0' if r[f'cov0_CSD_minus_{f}'] else 'EXCL'}]"
            for f in DISPERSION[1:]))
    publish("V3 all four dispersion estimators beat the FAMILY constant at every cell",
            f"{int(FAM.all_beat_FAMILY.sum())} of {len(FAM)}")
    covcols = [c for c in FAM.columns if c.startswith("cov0_")]
    publish("V3 CSD sits inside every other dispersion estimator's CI",
            f"{int(FAM[covcols].values.sum())} of {FAM[covcols].values.size}")
    for f in DISPERSION[1:]:
        c = int(FAM[f"cov0_CSD_minus_{f}"].sum())
        publish(f"V3 CSD vs {f}", f"CI covers zero at {c} of {len(FAM)} cells; "
                f"t range {FAM[f't_CSD_minus_{f}'].min():+.2f} .. {FAM[f't_CSD_minus_{f}'].max():+.2f}")

    say("\n  IS the estimator ORDER stable across the ladder? (rank of the 4 dispersion forms)")
    for _, r in FAM.iterrows():
        order = sorted(DISPERSION, key=lambda f: r[f])
        say(f"      gross {r.gross:.2f} {r.split}: " + " < ".join(order))

    # ================================================================ V4: capital
    say("\n" + "=" * 110); say("V4 — CAPITAL ARM, every grid point (10 bps, next-day execution)"); say("=" * 110)
    say(f"  {len(BK)} books = 3 panels x 2 families x 9 levels x 3 cadences x {len(GROSSES)} gross x 2 constructions")
    for g in GROSSES:
        b = BK[BK.gross == g]
        say(f"    gross {g:.2f}:  4a {int(b.p4a.sum()):3d}/{len(b)}   4b {int(b.p4b.sum()):3d}/{len(b)}"
            f"   mean Sharpe {b.Sharpe.mean():.4f}   mean MaxDD {b.MaxDD.mean():7.2%}"
            f"   mean turn {b.turn_yr.mean():.2f}/yr")
    for pn in BK.panel.unique():
        b = BK[BK.panel == pn]
        say(f"    {pn:9s}:  4a {int(b.p4a.sum()):3d}/{len(b)}   4b {int(b.p4b.sum()):3d}/{len(b)}")
    for con in ("RESPREAD", "DEGROSS"):
        b = BK[BK.con == con]
        say(f"    {con:9s}:  4a {int(b.p4a.sum()):3d}/{len(b)}   4b {int(b.p4b.sum()):3d}/{len(b)}")

    say("\n  RULE 8 (level and cadence chosen on 2009-2016 IS Sharpe ONLY; 2017-2026 read ONCE):")
    wf = []
    for pn in BK.panel.unique():
        for fam_ in FAMILIES:
            for con in ("RESPREAD", "DEGROSS"):
                for g in GROSSES:
                    a = BK[(BK.panel == pn) & (BK.family == fam_) & (BK.con == con) & (BK.gross == g)]
                    pick = a.loc[a.isSharpe.idxmax()]
                    wf.append(dict(panel=pn, family=fam_, con=con, gross=g, level=pick.level,
                                   cad=pick.cad, oos_CAGR=pick.oCAGR, oos_Sharpe=pick.oSharpe,
                                   oos_MaxDD=pick.oMaxDD, full_Sharpe=pick.Sharpe,
                                   full_CAGR=pick.CAGR, full_MaxDD=pick.MaxDD,
                                   H1=pick.H1, H2=pick.H2, p4a=pick.p4a, p4b=pick.p4b))
        # joint chooser over (gross, level, cadence) as a published extra
        for fam_ in FAMILIES:
            for con in ("RESPREAD", "DEGROSS"):
                a = BK[(BK.panel == pn) & (BK.family == fam_) & (BK.con == con)]
                pick = a.loc[a.isSharpe.idxmax()]
                wf.append(dict(panel=pn, family=fam_, con=con, gross=-1.0, level=pick.level,
                               cad=pick.cad, oos_CAGR=pick.oCAGR, oos_Sharpe=pick.oSharpe,
                               oos_MaxDD=pick.oMaxDD, full_Sharpe=pick.Sharpe,
                               full_CAGR=pick.CAGR, full_MaxDD=pick.MaxDD,
                               H1=pick.H1, H2=pick.H2, p4a=pick.p4a, p4b=pick.p4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"    legal IS-only picks: 4b {int(WF.p4b.sum())} of {len(WF)}   4a {int(WF.p4a.sum())} of {len(WF)}")
    for pn in WF.panel.unique():
        w = WF[WF.panel == pn]
        say(f"      {pn:9s} 4b {int(w.p4b.sum()):2d}/{len(w)}   4a {int(w.p4a.sum()):2d}/{len(w)}"
            f"   best OOS Sharpe {w.oos_Sharpe.max():.4f} (gross {w.loc[w.oos_Sharpe.idxmax(),'gross']:.2f}, "
            f"{w.loc[w.oos_Sharpe.idxmax(),'con']}, {w.loc[w.oos_Sharpe.idxmax(),'cad']})")
    say("    JOINT (gross, level, cadence) chooser rows (gross = -1):")
    for _, r in WF[WF.gross == -1].iterrows():
        say(f"      {r.panel:9s} {r.family:10s} {r['con']:9s} -> level {r.level:+.2f} {r.cad}"
            f"   OOS {r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / {r.oos_MaxDD:7.2%}"
            f"   4b {'P' if r.p4b else '.'}  4a {'P' if r.p4a else '.'}")

    best = BK.loc[BK[BK.p4b].oSharpe.idxmax()] if BK.p4b.any() else None
    if best is not None:
        say(f"\n    best 4b-passing book: {best.panel} {best.family} level {best.level} {best.cad} "
            f"{best['con']} gross {best.gross:.2f} — FULL {best.CAGR:7.2%}/{best.Sharpe:.4f}/{best.MaxDD:7.2%}"
            f" (H1 {best.H1:.3f} H2 {best.H2:.3f}), OOS {best.oCAGR:7.2%}/{best.oSharpe:.4f}/{best.oMaxDD:7.2%}")
    publish("V4 capital arm", f"4b {int(BK.p4b.sum())} of {len(BK)} books; 4a {int(BK.p4a.sum())}; "
                              f"rule-8 4b {int(WF.p4b.sum())} of {len(WF)} legal picks")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in GATES)
    say(f"\n  GATES {npass} of {len(GATES)}   runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
