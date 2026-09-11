#!/usr/bin/env python3
"""Idea 721 - "publish-a-MINIMUM-CLAIM-COUNT-beside-every-permutation-band-verdict"
(cloud lane, 2026-09-11).

The question
------------
Idea 717 (lane C, same day) found that its survival-share ladder cannot separate a real share
from its own permutation band below roughly 12 claims: at m = 4 and m = 6 BOTH drawdown outcomes
read INSIDE with excess exactly +0.0%, and idea 714's DDnorm INSIDE verdict (9 claims) flips to
BELOW once taken up to MaxDD's 19.  An INSIDE verdict at a small count is therefore not a
negative result, it is a NO-RESULT - and the record publishes INSIDE verdicts without ever
saying how many units the band was resolved over.

This run computes, for EVERY committed permutation / placebo band in the record, the MINIMUM
COUNT at which that band could have separated at all, and publishes it beside the verdict.

Two objects, both censused
--------------------------
CENSUS LEG   every committed band row in the record (12 files, enumerated in REGISTRY below -
             the complete set of committed CSVs carrying a (null-lo, null-hi) pair; the harvest
             rule is stated per file, nothing is inferred by keyword).  Each row yields
             (real, null_lo, null_med, null_hi, m, kind) where kind is
                 SHARE  the real value is a proportion over m discrete units (claims, draws,
                        cells) - idea 717's object;
                 LEVEL  the real value is a continuous statistic (a Sharpe gap, an absolute
                        deviation, a Dnet) whose null was resampled m times.
PRICE LEG    the same question asked of the thing that decides capital: a rule-8 selector's
             PASS-SHARE verdict on PROTOCOL's two KEEP paths.  How many picks does a 4a or 4b
             pass-share need before it can separate from the uniform random-pick null at all?

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. band   in {(5, 95), (2.5, 97.5)}          the percentile pair defining "inside"
    2. floor  in {FEAS, POW50}                   the floor definition
         FEAS   the smallest m at which ANY achievable value of the statistic lies outside the
                band, i.e. the smallest m at which a non-INSIDE verdict is READABLE at all.
                Defined for SHARE only (a LEVEL statistic is continuous, so FEAS is 1 by
                construction and is reported NA rather than 1, to avoid a fake pass).
         POW50  the smallest m at which, holding the OBSERVED effect size fixed, the real value
                lands outside the band with probability >= 0.5 (median power).
    Every band row is evaluated at all four cells and all four are written out.  Nothing below
    is selected on its outcome.  Panels, dials, cadences, gross, costs and windows on the price
    leg are REPORTED axes, never tuned.

How the answer is decided (pre-registered, before any number below was read)
    A published verdict is QUOTED BELOW ITS FLOOR when its own m is smaller than the floor its
    own band implies.  The headline is the share of committed band rows in that state, cut by
    verdict (INSIDE vs not) and by kind.  A high share among INSIDE rows means the record's
    "not distinguishable from the null" sentences are mostly count statements, not evidence.

Costs 10 bps per unit turnover, weights decided at close t applied at t+1, no shorting, no
leverage (PROTOCOL rules 1-2).  Walk-forward per PROTOCOL rule 8: every selector on the price
leg is fitted on <= 2016-12-31 ONLY and read once on the untouched remainder.

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): the broad and small panels are CURRENT
constituents of their screens, so every LEVEL on them is optimistic.  The object under test is
a count threshold and a selector's OOS ranking, neither of which is a level claim.  Tickers with
max_1d_move >= 1.0 in data/small_meta.csv are dropped from the small panel before any use.
No book here is a capital candidate.

Outputs: .census.csv .floors.csv .bookgrid.csv .picks.csv .walkforward.csv .pricefloor.csv
         .console.txt .result.md
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
OUT = Path(__file__).with_suffix("")
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


BANDS = {"5-95": (5.0, 95.0), "2.5-97.5": (2.5, 97.5)}      # tuned param 1
FLOORS = ["FEAS", "POW50"]                                   # tuned param 2
M_MAX = 4000                                                 # floor search ceiling
NSIM = 4000                                                  # simulation replicates per m
SEED = 721
IS_END = pd.Timestamp("2016-12-31")
WARMUP = 260
COST_BPS = 10

# ---------------------------------------------------------------------------------------------
# CENSUS LEG - the complete set of committed CSVs carrying a (null-lo, null-hi) pair.
# Each entry: file stem, and one or more band SPECS (label, real, lo, med, hi, m, kind, verdict).
# med=None -> midpoint of the band is used as the null centre and flagged.
# ---------------------------------------------------------------------------------------------
REGISTRY = [
    # idea 714 - per-family survival bands (two bands per row: the SHARE and the CLAIM RATE)
    ("2026-09-11_does-the-DRAWDOWN-vs-RETURN-survival-gap-hold-against-a-PER-FAMILY-null_C.bands.csv",
     [dict(label="714/share", real="real_share", lo="null_share_p5", med="null_share_med",
           hi="null_share_p95", m="real_defined", kind="SHARE", verdict="verdict"),
      dict(label="714/claimrate", real="real_claim_rate", lo="null_claim_rate_p5",
           med="null_claim_rate_med", hi="null_claim_rate_p95", m="cells", kind="SHARE",
           verdict=None)]),
    # idea 717 - matched-count survival bands
    ("2026-09-11_is-DDnorm-s-EDGE-OF-BAND-reading-a-NORMALISATION-fact-or-a-POWER-fact_C.matched.csv",
     [dict(label="717/matched", real="real_share", lo="null_p5", med="null_med", hi="null_p95",
           m="m", kind="SHARE", verdict="verdict")]),
    # idea 718-lineage - width-pinning rate against a binomial band
    ("2026-09-11_is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology_C.walkforward.csv",
     [dict(label="WIDTHMAX/pin", real="pin_rate_draws", lo="band_lo", med=None, hi="band_hi",
           m="n_ind", kind="SHARE", verdict="verdict")]),
    # abstention - chooser gain against a permuted-choice null
    ("2026-09-05_abstention-is-the-only-thing-that-ever-helps_cloud.gates.csv",
     [dict(label="abstain/gain", real="gain", lo="null_lo", med=None, hi="null_hi",
           m=("wins", "losses"), kind="LEVEL", verdict="null_side")]),
    ("2026-09-05_abstention-is-the-only-thing-that-ever-helps_cloud.walkforward.csv",
     [dict(label="abstainWF/gain", real="gain", lo="null_lo", med=None, hi="null_hi",
           m=("wins", "losses"), kind="LEVEL", verdict="null_side")]),
    # salted-seed audit - absolute reproduction deviation against a re-seeded band, 3 outcomes
    ("2026-09-05_audit-every-committed-null-for-a-salted-seed_C.exact.csv",
     [dict(label="salted/S", real="absd_S", lo="band_q05_S", med="band_q50_S", hi="band_q95_S",
           m="N_S", kind="LEVEL", verdict=None),
      dict(label="salted/DD", real="absd_DD", lo="band_q05_DD", med="band_q50_DD",
           hi="band_q95_DD", m="N_DD", kind="LEVEL", verdict=None),
      dict(label="salted/IS", real="absd_IS", lo="band_q05_IS", med="band_q50_IS",
           hi="band_q95_IS", m="N_IS", kind="LEVEL", verdict=None)]),
    ("2026-09-05_audit-every-committed-null-for-a-salted-seed_C.keep.csv",
     [dict(label="saltedK/S", real="absd_S", lo="band_q05_S", med="band_q50_S", hi="band_q95_S",
           m="N_S", kind="LEVEL", verdict=None)]),
    # random screen - realised dOOS against a random-screen null
    ("2026-09-05_does-a-random-screen-de-concentrate-just-as-well_B.null.csv",
     [dict(label="randscreen/agg", real="real_dOOS", lo="null_p5", med="null_p50", hi="null_p95",
           m="cells_live", kind="LEVEL", verdict="inside_90")]),
    ("2026-09-05_does-a-random-screen-de-concentrate-just-as-well_B.percell.csv",
     [dict(label="randscreen/cell", real="real_dOOS", lo="null_p5", med="null_mean",
           hi="null_p95", m="N", kind="LEVEL", verdict=None)]),
    # ROOM - D against a permuted-file null
    ("2026-09-08_publish-ROOM-beside-every-abstention-and-chooser-result_C.calgrid.csv",
     [dict(label="ROOM/cal", real="D", lo="perm_lo", med="perm_mean", hi="perm_hi", m="n",
           kind="LEVEL", verdict=None)]),
    ("2026-09-08_publish-ROOM-beside-every-abstention-and-chooser-result_C.livegrid.csv",
     [dict(label="ROOM/live", real="D", lo="perm_lo", med="perm_mean", hi="perm_hi", m="n",
           kind="LEVEL", verdict=None)]),
    ("2026-09-08_publish-ROOM-beside-every-abstention-and-chooser-result_C.taugrid.csv",
     [dict(label="ROOM/tau", real="D", lo="perm_lo", med="perm_mean", hi="perm_hi", m="n",
           kind="LEVEL", verdict=None)]),
]


def harvest():
    rows = []
    for stem, specs in REGISTRY:
        f = BT / stem
        if not f.exists():
            P(f"  MISSING {stem}")
            continue
        d = pd.read_csv(f)
        for sp in specs:
            need = [sp["real"], sp["lo"], sp["hi"]]
            if sp["med"]:
                need.append(sp["med"])
            mcol = sp["m"]
            need += list(mcol) if isinstance(mcol, tuple) else [mcol]
            if any(c not in d.columns for c in need):
                P(f"  SKIP {sp['label']} - column missing")
                continue
            m = d[list(mcol)].sum(axis=1) if isinstance(mcol, tuple) else d[mcol]
            med = d[sp["med"]] if sp["med"] else (d[sp["lo"]] + d[sp["hi"]]) / 2.0
            sub = pd.DataFrame(dict(
                file=stem, label=sp["label"], kind=sp["kind"],
                real=pd.to_numeric(d[sp["real"]], errors="coerce"),
                lo=pd.to_numeric(d[sp["lo"]], errors="coerce"),
                med=pd.to_numeric(med, errors="coerce"),
                hi=pd.to_numeric(d[sp["hi"]], errors="coerce"),
                m=pd.to_numeric(m, errors="coerce"),
                med_is_midpoint=sp["med"] is None,
                pub_verdict=(d[sp["verdict"]].astype(str) if sp["verdict"] else "")))
            sub["row"] = np.arange(len(sub))
            rows.append(sub)
    c = pd.concat(rows, ignore_index=True)
    c["usable"] = c[["real", "lo", "med", "hi", "m"]].notna().all(axis=1) & (c["m"] >= 1)
    c["width"] = c["hi"] - c["lo"]
    c["excess"] = c["real"] - c["med"]
    c["inside"] = (c["real"] >= c["lo"]) & (c["real"] <= c["hi"])
    c["degenerate"] = c["width"] <= 0
    return c


# ---------------------------------------------------------------------------------------------
# FLOORS
# ---------------------------------------------------------------------------------------------
def share_band(p0, m, disp, ql, qh, rng):
    """Null band of a share over m units with null rate p0, inflated by dispersion `disp`
    (published sd / plain binomial sd at the published m; >1 means the permutation null is
    wider than independent coin flips)."""
    k = rng.binomial(m, p0, NSIM).astype(float) / m
    if disp != 1.0:
        k = np.clip(p0 + (k - p0) * disp, 0.0, 1.0)
    return np.percentile(k, ql), np.percentile(k, qh)


def share_dispersion(row, ql, qh):
    """Calibrate the published band's width against a plain binomial at its own m."""
    m, p0 = int(row["m"]), float(np.clip(row["med"], 0, 1))
    rng = np.random.default_rng(SEED)
    lo, hi = share_band(p0, m, 1.0, ql, qh, rng)
    w_bin = hi - lo
    if w_bin <= 0:
        return 1.0
    return float(np.clip(row["width"] / w_bin, 0.25, 4.0))


def floor_share(row, ql, qh, mode):
    p0 = float(np.clip(row["med"], 0, 1))
    p1 = float(np.clip(row["real"], 0, 1))
    disp = share_dispersion(row, ql, qh)
    rng = np.random.default_rng(SEED + 1)
    for m in MGRID:
        lo, hi = share_band(p0, m, disp, ql, qh, rng)
        if mode == "FEAS":
            # readable IN THE DIRECTION THE REAL VALUE SITS.  A real share below its null
            # median can only ever read BELOW, which needs lo > 0; above needs hi < 1.  A real
            # value sitting exactly on the null median indicates no direction, so both sides
            # are required.  A null median pinned at 0 (or 1) can NEVER read BELOW (ABOVE) at
            # any m - those rows come back floor = NaN and are counted as UNREADABLE.
            ok = (lo > 0.0) if p1 < p0 else ((hi < 1.0) if p1 > p0 else (lo > 0.0 and hi < 1.0))
            if ok:
                return m, disp
        else:
            draws = rng.binomial(m, p1, NSIM).astype(float) / m
            if float(np.mean((draws < lo) | (draws > hi))) >= 0.5:
                return m, disp
    return np.nan, disp


def floor_level(row, ql, qh, mode):
    """A LEVEL band's half-width scales as 1/sqrt(m).  FEAS is undefined (continuous support).
    POW50: the observed distance d = |real - med| grows as sqrt(m/m0) in band units, so the
    floor is the smallest m with |d| * sqrt(m/m0) >= half-width(m0)."""
    if mode == "FEAS":
        return np.nan, np.nan
    m0 = float(row["m"])
    half = float(row["width"]) / 2.0
    d = abs(float(row["excess"]))
    if half <= 0 or d <= 0 or not np.isfinite(m0):
        return np.nan, np.nan
    m_star = m0 * (half / d) ** 2
    return (int(np.ceil(m_star)) if m_star <= M_MAX else np.nan), np.nan


MGRID = sorted(set(list(range(1, 41)) + list(range(42, 101, 2)) + list(range(105, 301, 5))
                   + list(range(320, 1001, 20)) + list(range(1050, M_MAX + 1, 50))))


def compute_floors(cen):
    out = []
    for bname, (ql, qh) in BANDS.items():
        for mode in FLOORS:
            # FEAS is undefined for a LEVEL band (continuous support), reported NOT APPLICABLE
            # rather than as a floor of 1, which would be a fake pass.
            applicable = not (mode == "FEAS")
            for _, r in cen[cen["usable"]].iterrows():
                app = applicable or r["kind"] == "SHARE"
                if not app:
                    fl, disp = np.nan, np.nan
                elif r["kind"] == "SHARE":
                    fl, disp = floor_share(r, ql, qh, mode)
                else:
                    fl, disp = floor_level(r, ql, qh, mode)
                out.append(dict(band=bname, floor_def=mode, file=r["file"], label=r["label"],
                                kind=r["kind"], row=r["row"], m=r["m"], real=r["real"],
                                lo=r["lo"], med=r["med"], hi=r["hi"], width=r["width"],
                                excess=r["excess"], inside=r["inside"],
                                pub_verdict=r["pub_verdict"], dispersion=disp, floor=fl,
                                applicable=app,
                                unreadable=(app and not np.isfinite(fl)),
                                below_floor=(np.nan if not app else
                                             (True if not np.isfinite(fl) else r["m"] < fl))))
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------------------------
# PRICE LEG
# ---------------------------------------------------------------------------------------------
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


def gate_weights(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def rank_weights(px, n, gross):
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above)
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def keep_paths(mr, mb, ms):
    """PROTOCOL rule 4.  mr/mb/ms are dicts of window -> metrics for idea, RULES v2, SPY."""
    a = (mr["H1"]["Sharpe"] > mb["H1"]["Sharpe"] and mr["H2"]["Sharpe"] > mb["H2"]["Sharpe"]
         and mr["full"]["MaxDD"] >= mb["full"]["MaxDD"])
    b = (mr["H1"]["Sharpe"] > ms["H1"]["Sharpe"] and mr["H2"]["Sharpe"] > ms["H2"]["Sharpe"]
         and mr["OOS"]["Sharpe"] > ms["OOS"]["Sharpe"]
         and mr["full"]["MaxDD"] >= 0.60 * ms["full"]["MaxDD"]
         and mr["full"]["CAGR"] >= 0.70 * ms["full"]["CAGR"])
    return bool(a), bool(b)


def windows(r):
    h = len(r) // 2
    return {"full": metrics(r), "H1": metrics(r.iloc[:h]), "H2": metrics(r.iloc[h:]),
            "IS": metrics(r.loc[:IS_END]), "OOS": metrics(r.loc[IS_END:].iloc[1:])}


def build_corpus():
    panels = {}
    px_u = load_universe()
    panels["U56"] = px_u
    panels["B136"] = load_universe(broad=True)
    ps, ndrop = small_panel()
    panels["SMALL"] = ps
    P(f"  small panel: dropped {ndrop} tickers with max_1d_move >= 1.0 -> {ps.shape[1] - 1} names + SPY")

    dials = ([dict(fam="GATE", band=b, n=np.nan) for b in (0.00, 0.03, 0.06)]
             + [dict(fam="RANK", band=np.nan, n=n) for n in (5, 10, 20, 50)])
    rows, rets, bench = [], {}, {}
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        bench[pname] = (windows(base), windows(spy))
        mb, ms = bench[pname]
        for k in ("full", "H1", "H2", "IS", "OOS"):
            rows.append(dict(panel=pname, fam="BENCH", book=f"RULES v2 ({pname})", band=np.nan,
                             n=np.nan, gross=np.nan, freq="W", window=k, **mb[k]))
            rows.append(dict(panel=pname, fam="BENCH", book=f"SPY ({pname})", band=np.nan,
                             n=np.nan, gross=np.nan, freq="W", window=k, **ms[k]))
        for d in dials:
            for gross in (0.50, 0.75, 1.00):
                for freq in ("W", "M"):
                    w = (gate_weights(px, d["band"], gross) if d["fam"] == "GATE"
                         else rank_weights(px, int(d["n"]), gross))
                    r = backtest(px, w, cost_bps=COST_BPS, freq=freq)["returns"].loc[start:]
                    mr = windows(r)
                    a, b = keep_paths(mr, mb, ms)
                    bid = (f"{pname}|{d['fam']}|"
                           f"{('b%.2f' % d['band']) if d['fam'] == 'GATE' else ('n%d' % d['n'])}"
                           f"|g{gross:.2f}|{freq}")
                    rets[bid] = r
                    rows.append(dict(panel=pname, fam=d["fam"], book=bid, band=d["band"],
                                     n=d["n"], gross=gross, freq=freq, window="ALL",
                                     pass4a=a, pass4b=b,
                                     IS_Sharpe=mr["IS"]["Sharpe"], IS_CAGR=mr["IS"]["CAGR"],
                                     IS_MaxDD=mr["IS"]["MaxDD"],
                                     IS_Calmar=mr["IS"]["CAGR"] / abs(mr["IS"]["MaxDD"]),
                                     OOS_Sharpe=mr["OOS"]["Sharpe"], OOS_CAGR=mr["OOS"]["CAGR"],
                                     OOS_MaxDD=mr["OOS"]["MaxDD"],
                                     full_Sharpe=mr["full"]["Sharpe"], full_CAGR=mr["full"]["CAGR"],
                                     full_MaxDD=mr["full"]["MaxDD"],
                                     H1_Sharpe=mr["H1"]["Sharpe"], H2_Sharpe=mr["H2"]["Sharpe"]))
    return pd.DataFrame(rows), bench, panels


SELECTORS = {"IS_SHARPE": ("IS_Sharpe", True), "IS_CAGR": ("IS_CAGR", True),
             "IS_CALMAR": ("IS_Calmar", True), "IS_MINDD": ("IS_MaxDD", True)}


def run_picks(grid, bench):
    """Rule 8: within each (panel, gross, freq) stratum the selector picks the argmax of an
    IS-ONLY statistic over the 7 dial books, and the pick is read ONCE on OOS."""
    books = grid[grid["window"] == "ALL"].copy()
    strata = books.groupby(["panel", "gross", "freq"])
    picks, null_rows = [], []
    rng = np.random.default_rng(SEED + 2)
    for sname, (col, hi) in SELECTORS.items():
        for (pn, g, fr), sub in strata:
            mb, ms = bench[pn]
            i = sub[col].idxmax() if hi else sub[col].idxmin()
            r = books.loc[i]
            picks.append(dict(selector=sname, panel=pn, gross=g, freq=fr, book=r["book"],
                              n_cand=len(sub), pass4a=r["pass4a"], pass4b=r["pass4b"],
                              OOS_Sharpe=r["OOS_Sharpe"], OOS_CAGR=r["OOS_CAGR"],
                              OOS_MaxDD=r["OOS_MaxDD"],
                              v2_OOS_Sharpe=mb["OOS"]["Sharpe"], v2_OOS_CAGR=mb["OOS"]["CAGR"],
                              v2_OOS_MaxDD=mb["OOS"]["MaxDD"],
                              spy_OOS_Sharpe=ms["OOS"]["Sharpe"], spy_OOS_CAGR=ms["OOS"]["CAGR"],
                              spy_OOS_MaxDD=ms["OOS"]["MaxDD"],
                              beats_v2=r["OOS_Sharpe"] > mb["OOS"]["Sharpe"],
                              beats_spy=r["OOS_Sharpe"] > ms["OOS"]["Sharpe"]))
    # uniform random-pick null over the same strata, same pick count
    keys = list(strata.groups)
    for d in range(2000):
        sel = [strata.get_group(k).sample(1, random_state=int(rng.integers(1 << 31))).iloc[0]
               for k in keys]
        s = pd.DataFrame(sel)
        null_rows.append(dict(draw=d, share4a=s["pass4a"].mean(), share4b=s["pass4b"].mean(),
                              mean_OOS_Sharpe=s["OOS_Sharpe"].mean()))
    return pd.DataFrame(picks), pd.DataFrame(null_rows), books


def price_floor(books, m_grid=(4, 6, 9, 12, 15, 18, 24, 36, 54, 90, 180, 360)):
    """How many picks does a pass-share verdict need before it can separate from the uniform
    random-pick null?  The null is the record's own corpus: draw m books uniformly from the
    72 dial-book rows (all strata pooled) and read the pass share."""
    rng = np.random.default_rng(SEED + 3)
    p4a = books["pass4a"].values.astype(float)
    p4b = books["pass4b"].values.astype(float)
    out = []
    for path, arr in (("4a", p4a), ("4b", p4b)):
        base = arr.mean()
        for bname, (ql, qh) in BANDS.items():
            for m in m_grid:
                draws = rng.choice(arr, size=(NSIM, m), replace=True).mean(axis=1)
                lo, hi = np.percentile(draws, ql), np.percentile(draws, qh)
                out.append(dict(path=path, band=bname, m=m, corpus_rate=base, null_lo=lo,
                                null_hi=hi, feasible_below=lo > 0.0, feasible_above=hi < 1.0,
                                min_detectable_below=lo, min_detectable_above=hi))
    return pd.DataFrame(out)


def main():
    P("=" * 100)
    P("IDEA 721 - publish a MINIMUM CLAIM COUNT beside every permutation band verdict (cloud)")
    P("=" * 100)

    # ---- GATES -------------------------------------------------------------------------
    P("\n[GATES] committed numbers re-read before anything new is computed")
    g = {}
    d714 = pd.read_csv(BT / REGISTRY[0][0])
    f5 = d714[(d714["scheme"] == "FAM5") & (d714["resid"] == "logx") & (d714["draws"] == 400)]
    mx = f5[f5["family"] == "MaxDD"]
    g["G1 714 MaxDD share == 2/19"] = (len(mx) == 1
                                       and abs(float(mx["real_share"].iloc[0]) - 2 / 19) < 5e-4)
    d717 = pd.read_csv(BT / REGISTRY[1][0])
    b19 = d717[(d717["outcome"] == "DDnorm") & (d717["device"] == "BAR") & (d717["m"] == 19)]
    g["G2 717 DDnorm@m=19 reads BELOW"] = (len(b19) == 1
                                           and b19["verdict"].iloc[0].strip() == "BELOW")
    s4 = d717[d717["outcome"].isin(["MaxDD", "DDnorm"]) & (d717["device"] == "BAR")
              & (d717["m"].isin([4, 6]))]
    g["G3 717 BAR m=4,6 both DD outcomes read INSIDE"] = bool(
        len(s4) == 4 and (s4["verdict"] == "INSIDE").all())
    # RECORD CORRECTION, checked not asserted: 717's prose says these four rows carry
    # "excess exactly +0.0%".  Three do; DDnorm at m=6 does not.
    EXC = s4.set_index(["outcome", "m"])["excess"].to_dict()
    P("  [check] 717's 'excess exactly +0.0%' at BAR m=4,6: "
      + ", ".join(f"{k[0]}@m={k[1]} {v:+.4f}" for k, v in sorted(EXC.items())))
    g["G3b 717 BAR m=4 excess is exactly 0.0 for both"] = (
        abs(EXC.get(("MaxDD", 4), 9)) == 0.0 and abs(EXC.get(("DDnorm", 4), 9)) == 0.0)
    px = load_universe()
    spy = px["SPY"].pct_change().fillna(0.0).loc[px.index[WARMUP]:]
    g["G4 SPY full Sharpe finite from baseline loader"] = np.isfinite(metrics(spy)["Sharpe"])
    for k, v in g.items():
        P(f"  {'PASS' if v else 'FAIL'}  {k}")
    if not all(g.values()):
        P("  GATES FAILED - stopping before any new number is read")
        return

    # ---- CENSUS ------------------------------------------------------------------------
    P("\n[CENSUS] harvesting every committed permutation / placebo band in the record")
    cen = harvest()
    cen.to_csv(f"{OUT}.census.csv", index=False)
    P(f"  band rows harvested: {len(cen)}  usable: {int(cen['usable'].sum())}  "
      f"files: {cen['file'].nunique()}")
    P(cen.groupby(["kind"])["usable"].agg(["size", "sum"]).to_string())
    P("\n  by file:")
    P(cen.groupby(["label", "kind"]).agg(rows=("usable", "size"), usable=("usable", "sum"),
                                         med_m=("m", "median")).to_string())

    # ---- FLOORS ------------------------------------------------------------------------
    P("\n[FLOORS] separation floor of every usable band, all 2 x 2 grid points")
    fl = compute_floors(cen)
    fl.to_csv(f"{OUT}.floors.csv", index=False)
    piv = fl.groupby(["band", "floor_def", "kind"]).agg(
        rows=("floor", "size"), applicable=("applicable", "sum"),
        floor_defined=("floor", lambda s: int(s.notna().sum())),
        unreadable=("unreadable", "sum"), med_floor=("floor", "median"), med_m=("m", "median"),
        below_floor=("below_floor", lambda s: int(pd.Series(s).fillna(False).sum())))
    piv["share_below_floor"] = piv["below_floor"] / piv["applicable"].replace(0, np.nan)
    P(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    P("\n  ('unreadable' = the band's own null median is pinned at 0 or 1 in the direction the"
      " real value sits, so NO count could ever produce that verdict.)")

    P("\n  cut by whether the published verdict was INSIDE:")
    fl["pub_inside"] = fl["inside"]
    cut = fl[fl["applicable"]].groupby(["band", "floor_def", "pub_inside"]).agg(
        rows=("floor", "size"), med_m=("m", "median"), med_floor=("floor", "median"),
        unreadable=("unreadable", "sum"),
        below=("below_floor", lambda s: int(pd.Series(s).fillna(False).sum())))
    cut["share_below_floor"] = cut["below"] / cut["rows"]
    P(cut.to_string(float_format=lambda x: f"{x:.3f}"))

    P("\n  the two focal lineage files, row by row (band 5-95, FEAS):")
    foc = fl[(fl["band"] == "5-95") & (fl["floor_def"] == "FEAS")
             & fl["label"].isin(["714/share", "717/matched"])]
    P(foc[["label", "row", "m", "real", "lo", "hi", "excess", "pub_verdict", "dispersion",
           "floor", "below_floor"]].head(40).to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- PRICE LEG ---------------------------------------------------------------------
    P("\n[PRICE LEG] building the book corpus (10 bps, t+1 execution, no leverage)")
    grid, bench, _ = build_corpus()
    grid.to_csv(f"{OUT}.bookgrid.csv", index=False)
    books = grid[grid["window"] == "ALL"]
    P(f"  books: {len(books)}  4a passes: {int(books['pass4a'].sum())}  "
      f"4b passes: {int(books['pass4b'].sum())}")
    P(books.groupby(["panel", "fam"])[["pass4a", "pass4b"]].sum().to_string())

    P("\n  benchmarks (OOS window, > 2016-12-31):")
    bm = grid[(grid["fam"] == "BENCH") & (grid["window"] == "OOS")]
    P(bm[["panel", "book", "CAGR", "Sharpe", "MaxDD"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n[RULE 8] IS-only selectors (<= 2016-12-31), each pick read ONCE on OOS")
    picks, nulls, books = run_picks(grid, bench)
    picks.to_csv(f"{OUT}.picks.csv", index=False)
    wf = picks.groupby("selector").agg(
        picks=("book", "size"), pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"),
        beats_v2=("beats_v2", "sum"), beats_spy=("beats_spy", "sum"),
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), v2_OOS_Sharpe=("v2_OOS_Sharpe", "mean"),
        spy_OOS_Sharpe=("spy_OOS_Sharpe", "mean"), spy_OOS_CAGR=("spy_OOS_CAGR", "mean"),
        spy_OOS_MaxDD=("spy_OOS_MaxDD", "mean"))
    wf["share4a"] = wf["pass4a"] / wf["picks"]
    wf["share4b"] = wf["pass4b"] / wf["picks"]
    wf.to_csv(f"{OUT}.walkforward.csv")
    P(wf.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  uniform random-pick null over the same {picks['selector'].value_counts().iloc[0]} "
      f"strata, 2000 draws:")
    for c in ("share4a", "share4b", "mean_OOS_Sharpe"):
        q = np.percentile(nulls[c], [5, 50, 95])
        P(f"    {c:18s} null [5,50,95] = [{q[0]:.4f}, {q[1]:.4f}, {q[2]:.4f}]")

    P("\n[PRICE FLOOR] the separation floor of a KEEP-path pass-share verdict")
    pf = price_floor(books)
    pf.to_csv(f"{OUT}.pricefloor.csv", index=False)
    P(pf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for path in ("4a", "4b"):
        for bname in BANDS:
            s = pf[(pf["path"] == path) & (pf["band"] == bname)]
            fb = s[s["feasible_below"]]["m"]
            P(f"  {path} band {bname}: corpus rate {s['corpus_rate'].iloc[0]:.4f}; "
              f"a BELOW verdict is readable from m = "
              f"{int(fb.min()) if len(fb) else 'never (<= 360)'} picks")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {OUT.name}.*")


if __name__ == "__main__":
    main()
