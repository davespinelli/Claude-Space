#!/usr/bin/env python3
"""Idea 259 - "does-the-sharpe-cagr-reversal-sit-under-every-EWall-claim" (lane C, 2026-09-06).

The question
------------
Idea 82 measured the SAME eight cells twice and got opposite headlines:

    EWall - CANDg-n   Sharpe  +0.0467   t +4.03   7/8 cells   ("no-ranking wins")
    FWD   - EWall     CAGR    +1.28pp   t +4.93   8/8 cells   ("ranking wins")

The record quotes "EWall beats the ranked book" on SHARPE in several places (ideas 10,
72, 73, 77, 82).  The queue asks: back-fill the CAGR column beside every published
EWall-vs-ranked comparison whose parent committed a grid CSV, and report how many are
Sharpe-only verdicts that REVERSE.

Design (three legs, the first is the queue's literal ask)
--------------------------------------------------------
A. CENSUS.  Walk every research/backtests/*.csv the project has committed.  A file
   enters the census if it has BOTH a `Sharpe` and a `CAGR` column and a label column
   carrying an EWall-type arm (`EWall`/`EWALL`/`ewall`/`EW`/`ew-all`) alongside at
   least one other arm.  Inside a file, a CELL is defined by the label column's
   FULLY-CROSSED co-columns only: a key column is kept iff its value set on the EWall
   rows equals its value set on the non-EWall rows (so panel/universe/cost/convention
   are keys, while a dial the EWall arm does not have - `n`, `param`, `g` - is not, and
   the EWall row is paired against EVERY value of it).  Each (cell, comparand) pair is
   one published comparison point; dSharpe and dCAGR are both computed EWall-minus-
   comparand, and the pair REVERSES when the two disagree in sign.

   Comparands are classified: RANKED (a composite/momentum-ranked book - CAND, FWD,
   top-n, v1, V1C, REV, band, frac...) vs OTHER (RAND draws, sleeves, overlays, other
   un-ranked books).  The headline count is the RANKED subset, which is what the queue
   names; the OTHER subset is reported beside it.

   Pre-registered epsilons, chosen before any count was read: a pair counts as a
   reversal only if |dSharpe| > 0.005 AND |dCAGR| > 0.0005 (5 bps/yr).  Both counts are
   ALSO reported at eps = 0 so the choice is visible.

B. CONTROLLED RE-READ.  The census pools heterogeneous constructions, so the same
   question is asked once more under ONE construction, idea 82's, imported verbatim
   (weekly, next-day, 10 bps, gate = above-200d AND vol20 < 0.60, key = composite
   without the vol scaler, EVERY arm gross-matched at 0.75):

       EWall   every eligible name, equal weight     (the un-ranked book)
       FWD-n   top-n by the composite key            (the ranked book)

   on four panels x six n, with idea 82's own eight cells re-run as the reproduction
   gate.  0 bps is carried as a DIAGNOSTIC column (not selected on, never a headline)
   because idea 260 showed a turnover-mismatched difference is part cost.

C. THE PREDICTOR.  Sharpe = mean/vol and CAGR is a level, so a reversal is arithmetic:
   EWall can win on Sharpe and lose on CAGR exactly when its volatility falls by more
   than its return does.  Pre-registered rule, tested on both A and B:

       predict REVERSE  <=>  sign(dCAGR) != sign(dSharpe) implied by
                             (ret ratio) and (vol ratio) straddling 1.0,
       i.e. REVERSE  <=>  (CAGR_ew/CAGR_cmp - 1) and (Sharpe_ew/Sharpe_cmp - 1)
                          have opposite signs, which for positive arms holds iff
                          vol_ew/vol_cmp lies between CAGR_ew/CAGR_cmp and 1.
   Reported as accuracy/precision/recall against the realised reversals wherever a Vol
   column exists, so the record can flag a reversal-prone comparison BEFORE re-running it.

Tuned parameters (PROTOCOL rule 4: at most two) - leg B only
    1. panel (4)      2. n (6)
The arm axis (EWall vs FWD) is the hypothesis, not a dial; the cost rung is fixed at
PROTOCOL's 10 bps with 0 bps reported as a diagnostic.  Leg A tunes nothing - it reads
committed files.  ALL grid points are written to the .csv outputs.

Walk-forward (PROTOCOL rule 8), pre-registered with direction before any OOS read
    IS = 2009-01-01..2016-12-31 chooses; OOS = 2017-01-01..end read ONCE.
    S_SHARPE  arm = argmax IS Sharpe within the panel   (the metric the record quotes)
    S_CAGR    arm = argmax IS CAGR within the panel     (the metric it does not)
    EWALL     EWall, no ranking, no n                   (do-nothing / the recommendation)
    FWD20     FWD n=20                                  (the incumbent construction)
    If the Sharpe/CAGR reversal is a REPORTING artefact, S_SHARPE and S_CAGR pick the
    same arm and rule 8 is silent.  If it is a DECISION, they pick different books and
    the OOS gap between them is the price of quoting one metric.

Verdicts (both KEEP paths, on every leg-B point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: universe_broad.json, the megacap cut and the small panel are CURRENT
constituents.  On a list of known survivors the un-ranked book that holds EVERYTHING
inherits the full survivorship premium while any selection rule can only redistribute
it, so the bias runs TOWARD the pro-EWall side of every comparison counted here.

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import re
import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
DIAG_BPS = 0
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS = [5, 10, 20, 30, 40, 60]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
SAT_CAP = 0.25
EPS_S, EPS_C = 0.005, 0.0005
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 500)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ==================================================================== LEG A: census
EW_LABEL = re.compile(r"^(ewall|ewall_s|ew_all|ew-all|ew)$", re.I)
RANKED_LABEL = re.compile(
    r"(cand|fwd|top\d|top-|^rev$|^v1|v1c|band\d|frac|rank|^ranked|^n\d+$|^stk|comp)", re.I)
# metric-ish column names: never a cell key
METRIC = re.compile(
    r"^(cagr|sharpe|maxdd|vol|calmar|sortino|h1|h2|turn|turnover|to|gross|gross_reb|flips|"
    r"elig|names|point|d[a-z]+|m_[a-z0-9]+|p4a|p4b|f4a|f4b|f4b_oos|4a|4b|4b_oos|is4b|oos4b|"
    r"fails|failing|bind|binds|z|resid|held|sat_share|verdict|dominated|artefact|lever|rate|"
    r"skill|regret|rho|r2|weight|t|se|p|pval|n_[a-z]+|y2020|y2022|total|years|winrate|"
    r"bestday|worstday|equity)$", re.I)
METRIC_PREFIX = re.compile(r"^(is_|oos_|d_|m_|sh_y_|spy_|base_|v1_|ctl_|gm_|vs_|md_|null_|band_)", re.I)


def is_metric_col(c):
    return bool(METRIC.match(str(c)) or METRIC_PREFIX.match(str(c)))


def pick_col(df, name):
    for c in df.columns:
        if str(c).lower() == name:
            return c
    return None


def census():
    # .csv AND .csv.gz (24 of the record's committed grids are gzipped); this run's OWN
    # outputs are excluded, so the census is a function of the record only
    files = [f for f in sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz")))
             if not f.name.startswith(STEM)]
    pairs, skipped = [], []
    for f in files:
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception as e:
            skipped.append((f.name, f"unreadable: {type(e).__name__}"))
            continue
        c_s, c_c = pick_col(df, "sharpe"), pick_col(df, "cagr")
        if c_s is None or c_c is None:
            continue
        c_v = pick_col(df, "vol")
        c_dd = pick_col(df, "maxdd")
        c_os, c_oc = pick_col(df, "oos_sharpe"), pick_col(df, "oos_cagr")
        for lab in df.columns:
            if is_metric_col(lab):
                continue
            if pd.api.types.is_numeric_dtype(df[lab]) or pd.api.types.is_bool_dtype(df[lab]):
                continue
            vals = [str(v) for v in df[lab].dropna().unique()]
            if len(vals) < 2:
                continue
            ewv = [v for v in vals if EW_LABEL.match(v.strip())]
            if not ewv:
                continue
            sub = df.copy()
            sub["_lab"] = sub[lab].astype(str)
            is_ew = sub["_lab"].str.strip().str.lower().isin([v.strip().lower() for v in ewv])
            # fully-crossed key columns only
            keys = []
            for c in df.columns:
                if c == lab or is_metric_col(c):
                    continue
                s = sub[c]
                if s.isna().all():
                    continue
                a = set(map(str, s[is_ew].dropna().unique()))
                b = set(map(str, s[~is_ew].dropna().unique()))
                if a and a == b and len(a) <= 60:
                    keys.append(c)
            ew_rows = sub[is_ew]
            ot_rows = sub[~is_ew]
            if ew_rows.empty or ot_rows.empty:
                continue
            if keys:
                gk = [tuple(map(str, r)) for r in ew_rows[keys].astype(str).values]
                ew_rows = ew_rows.assign(_cell=gk)
                ot_rows = ot_rows.assign(_cell=[tuple(map(str, r)) for r in ot_rows[keys].astype(str).values])
            else:
                ew_rows = ew_rows.assign(_cell=[("_all",)] * len(ew_rows))
                ot_rows = ot_rows.assign(_cell=[("_all",)] * len(ot_rows))
            for cell, og in ot_rows.groupby("_cell", sort=False):
                eg = ew_rows[ew_rows["_cell"] == cell]
                if eg.empty:
                    continue
                if len(eg) > 1:                       # several EWall rows share the cell -> average
                    ew_s = eg[c_s].astype(float).mean()
                    ew_c = eg[c_c].astype(float).mean()
                    ew_v = eg[c_v].astype(float).mean() if c_v else np.nan
                    ew_dd = eg[c_dd].astype(float).mean() if c_dd else np.nan
                    ew_os = eg[c_os].astype(float).mean() if c_os else np.nan
                    ew_oc = eg[c_oc].astype(float).mean() if c_oc else np.nan
                else:
                    r0 = eg.iloc[0]
                    ew_s, ew_c = float(r0[c_s]), float(r0[c_c])
                    ew_v = float(r0[c_v]) if c_v and pd.notna(r0[c_v]) else np.nan
                    ew_dd = float(r0[c_dd]) if c_dd and pd.notna(r0[c_dd]) else np.nan
                    ew_os = float(r0[c_os]) if c_os and pd.notna(r0[c_os]) else np.nan
                    ew_oc = float(r0[c_oc]) if c_oc and pd.notna(r0[c_oc]) else np.nan
                for _, r in og.iterrows():
                    try:
                        s2, c2 = float(r[c_s]), float(r[c_c])
                    except Exception:
                        continue
                    if not (np.isfinite(s2) and np.isfinite(c2) and np.isfinite(ew_s) and np.isfinite(ew_c)):
                        continue
                    cmp_lab = str(r["_lab"])
                    pairs.append(dict(
                        file=f.name, label_col=str(lab), cell="|".join(cell),
                        keys="|".join(map(str, keys)), ew_arm=str(eg.iloc[0]["_lab"]), cmp_arm=cmp_lab,
                        cmp_class="RANKED" if RANKED_LABEL.search(cmp_lab) else "OTHER",
                        S_ew=ew_s, S_cmp=s2, C_ew=ew_c, C_cmp=c2,
                        V_ew=ew_v, V_cmp=(float(r[c_v]) if c_v and pd.notna(r[c_v]) else np.nan),
                        DD_ew=ew_dd, DD_cmp=(float(r[c_dd]) if c_dd and pd.notna(r[c_dd]) else np.nan),
                        OS_ew=ew_os, OS_cmp=(float(r[c_os]) if c_os and pd.notna(r[c_os]) else np.nan),
                        OC_ew=ew_oc, OC_cmp=(float(r[c_oc]) if c_oc and pd.notna(r[c_oc]) else np.nan),
                    ))
    cp = pd.DataFrame(pairs)
    if cp.empty:
        return cp, skipped, len(files)
    cp["dS"] = cp.S_ew - cp.S_cmp
    cp["dC"] = cp.C_ew - cp.C_cmp
    cp["dOS"] = cp.OS_ew - cp.OS_cmp
    cp["dOC"] = cp.OC_ew - cp.OC_cmp
    cp["rev"] = (np.sign(cp.dS) != np.sign(cp.dC)) & (cp.dS.abs() > EPS_S) & (cp.dC.abs() > EPS_C)
    cp["rev_eps0"] = (np.sign(cp.dS) != np.sign(cp.dC)) & (cp.dS != 0) & (cp.dC != 0)
    cp["rev_EWonS"] = cp.rev & (cp.dS > 0) & (cp.dC < 0)      # the queue's direction
    cp["rev_EWonC"] = cp.rev & (cp.dS < 0) & (cp.dC > 0)
    cp["rev_oos"] = ((np.sign(cp.dOS) != np.sign(cp.dOC)) & (cp.dOS.abs() > EPS_S)
                     & (cp.dOC.abs() > EPS_C))
    # leg C predictor: for arms with positive CAGR, reversal <=> vol ratio between CAGR ratio and 1
    rr = cp.C_ew / cp.C_cmp
    vr = cp.V_ew / cp.V_cmp
    ok = np.isfinite(rr) & np.isfinite(vr) & (cp.C_ew > 0) & (cp.C_cmp > 0) & (cp.V_cmp > 0)
    pred = ((vr < np.minimum(rr, 1.0)) | (vr > np.maximum(rr, 1.0)))
    cp["pred_rev"] = np.where(ok, pred, np.nan)
    return cp, skipped, len(files)


# ==================================================================== LEG B: controlled re-read
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56": sub(px56, [c for c in px56.columns]),
        "B136": sub(px136, [c for c in px136.columns]),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL439": sub(pxs, s_stk, tradable=s_stk),
    }


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights(px, tradable, arm, n=None):
    elig = eligible_mask(px, tradable)
    if arm == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        key = score(px, vol_scale=False)[0]
        rank = key.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def v4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def paired_t(d):
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=float)
    if len(d) < 2:
        return np.nan, np.nan, 0
    se = d.std(ddof=1) / np.sqrt(len(d))
    return d.mean(), (d.mean() / se if se > 0 else np.nan), int((d > 0).sum())


def run_leg_b(panels):
    rows = []
    for pname, (px, tr) in panels.items():
        elig = eligible_mask(px, tr)
        m = rebalance_mask(px.index, FREQ)
        nel = elig[m.values].sum(axis=1)
        spy = px["SPY"].pct_change().fillna(0)
        base_w = None
        arms = [("EWall", None), ("v1", None)] + [("FWD", n) for n in NS]
        cache = {}
        for arm, n in arms:
            w = weights(px, tr, arm, n)
            for bps in (COST_BPS, DIAG_BPS):
                res = backtest(px, w, cost_bps=bps, freq=FREQ)
                start = px.index[260]
                r = res["returns"].loc[start:]
                sp = spy.loc[start:]
                r_is, r_oos = r.loc[IS_START:IS_END], r.loc[OOS_START:]
                sp_is, sp_oos = sp.loc[IS_START:IS_END], sp.loc[OOS_START:]
                mm, mo = metrics(r), metrics(r_oos)
                h1, h2 = half_sharpes(r)
                sat = float((nel.loc[start:] <= (n if n else 0)).mean()) if n else 0.0
                cache[(arm, n, bps)] = dict(r=r, sp=sp, r_is=r_is, r_oos=r_oos)
                rows.append(dict(
                    panel=pname, arm=arm, n=(n if n else np.nan), bps=bps,
                    CAGR=mm["CAGR"], Vol=mm["Vol"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                    H1=h1, H2=h2,
                    IS_CAGR=metrics(r_is)["CAGR"], IS_Sharpe=metrics(r_is)["Sharpe"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    turn=float(res["turnover"].loc[start:].sum() / (len(r) / 252)),
                    gross=float(w.loc[start:].sum(axis=1).mean()),
                    sat_share=sat,
                    SPY_CAGR=metrics(sp)["CAGR"], SPY_Sharpe=metrics(sp)["Sharpe"],
                    SPY_MaxDD=metrics(sp)["MaxDD"],
                ))
        # verdict columns need the v1 baseline of the SAME panel at the same rung
        for bps in (COST_BPS, DIAG_BPS):
            b = cache[("v1", None, bps)]
            for arm, n in arms:
                c = cache[(arm, n, bps)]
                sel = [i for i, rr in enumerate(rows)
                       if rr["panel"] == pname and rr["arm"] == arm
                       and (np.isnan(rr["n"]) if n is None else rr["n"] == n) and rr["bps"] == bps]
                for i in sel:
                    rows[i]["p4a"] = v4a(c["r"], b["r"])
                    rows[i]["f4b"] = fail4b(c["r"], c["sp"], c["r_oos"], c["sp"].loc[OOS_START:])
                    rows[i]["p4b"] = rows[i]["f4b"] == "-"
    return pd.DataFrame(rows)


def rule8(grid):
    """IS 2009-2016 chooses; OOS 2017+ read once.  S_SHARPE vs S_CAGR is the test."""
    out = []
    for (pname, bps), g in grid.groupby(["panel", "bps"]):
        pool = g[g.arm.isin(["EWall", "FWD"])].copy()
        pool = pool[(pool.arm == "EWall") | (pool.sat_share <= SAT_CAP)]
        if pool.empty:
            continue
        picks = {
            "S_SHARPE": pool.loc[pool.IS_Sharpe.idxmax()],
            "S_CAGR": pool.loc[pool.IS_CAGR.idxmax()],
            "EWALL": pool[pool.arm == "EWall"].iloc[0],
            "FWD20": pool[(pool.arm == "FWD") & (pool.n == 20)].iloc[0]
            if ((pool.arm == "FWD") & (pool.n == 20)).any() else pool.iloc[0],
        }
        v1 = g[g.arm == "v1"].iloc[0]
        for sname, r in picks.items():
            out.append(dict(panel=pname, bps=bps, selector=sname,
                            pick=f"{r.arm}{'' if np.isnan(r.n) else int(r.n)}",
                            IS_Sharpe=r.IS_Sharpe, IS_CAGR=r.IS_CAGR,
                            OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                            v1_OOS_Sharpe=v1.OOS_Sharpe, v1_OOS_CAGR=v1.OOS_CAGR,
                            v1_OOS_MaxDD=v1.OOS_MaxDD,
                            SPY_OOS_Sharpe=np.nan, full_4a=r.p4a, full_4b=r.p4b))
    return pd.DataFrame(out)


# ==================================================================== main
def main():
    P("=" * 190)
    P(f"Idea 259 does-the-sharpe-cagr-reversal-sit-under-every-EWall-claim (lane C) | {SCRIPT}")
    P(f"Leg A census over committed CSVs | Leg B fresh grid at {COST_BPS} bps (0 bps diagnostic), "
      f"weekly, next-day, gross matched at {GROSS}")
    P("=" * 190)

    # ---------------------------------------------------------------- LEG A
    P("\n" + "=" * 100 + "\nLEG A - CENSUS: every committed EWall-vs-arm comparison, CAGR back-filled\n" + "=" * 100)
    cp, skipped, n_scanned = census()
    cp.to_csv(OUT / f"{STEM}.census.csv.gz", index=False)   # 18k+ rows, gzipped
    P(f"files scanned: {n_scanned} committed CSVs incl. .csv.gz (this run's own outputs excluded), unreadable: {len(skipped)}")
    P(f"census pairs: {len(cp)} from {cp.file.nunique()} committed CSVs "
      f"({cp.groupby('file').size().describe()['50%']:.0f} pairs/file median)")
    P(f"comparand classes: {cp.cmp_class.value_counts().to_dict()}")

    for cls in ["RANKED", "OTHER"]:
        s = cp[cp.cmp_class == cls]
        if s.empty:
            continue
        P(f"\n--- {cls} comparands: {len(s)} pairs, {s.file.nunique()} files")
        P(f"    EWall wins on Sharpe: {int((s.dS > EPS_S).sum())}  loses: {int((s.dS < -EPS_S).sum())}  "
          f"ties(|d|<=eps): {int((s.dS.abs() <= EPS_S).sum())}")
        P(f"    EWall wins on CAGR  : {int((s.dC > EPS_C).sum())}  loses: {int((s.dC < -EPS_C).sum())}  "
          f"ties: {int((s.dC.abs() <= EPS_C).sum())}")
        P(f"    REVERSALS (eps {EPS_S}/{EPS_C}): {int(s.rev.sum())} of {len(s)} = {s.rev.mean():.1%}"
          f"   [at eps=0: {int(s.rev_eps0.sum())} = {s.rev_eps0.mean():.1%}]")
        P(f"      of which EWall-wins-Sharpe-loses-CAGR (the queue's direction): {int(s.rev_EWonS.sum())}"
          f"  |  EWall-loses-Sharpe-wins-CAGR: {int(s.rev_EWonC.sum())}")
        won_s = int((s.dS > EPS_S).sum())
        P(f"    HEADLINE - conditional on EWall winning on Sharpe ({won_s} pairs), it LOSES on CAGR in "
          f"{int(s.rev_EWonS.sum())} = {s.rev_EWonS.sum()/max(won_s,1):.1%} of them")
        oos = s[np.isfinite(s.dOS) & np.isfinite(s.dOC)]
        if len(oos):
            P(f"    OOS columns present on {len(oos)} pairs: OOS reversals {int(oos.rev_oos.sum())} "
              f"= {oos.rev_oos.mean():.1%}")
        byf = s.groupby("file").agg(pairs=("rev", "size"), rev=("rev", "sum"))
        byf["frac"] = byf.rev / byf.pairs
        P(f"    files with >=1 reversal: {int((byf.rev > 0).sum())} of {len(byf)}; "
          f"files where a MAJORITY of pairs reverse: {int((byf.frac > 0.5).sum())}")
        P("    top files by reversal count:")
        P(fmt(byf.sort_values(['rev', 'frac'], ascending=False).head(12), 3))

    # sign-of-verdict table on the ranked subset
    s = cp[cp.cmp_class == "RANKED"]
    tab = pd.crosstab(np.sign(s.dS.where(s.dS.abs() > EPS_S, 0)),
                      np.sign(s.dC.where(s.dC.abs() > EPS_C, 0)))
    P("\nRANKED pairs: sign(dSharpe) [rows] x sign(dCAGR) [cols], EWall minus ranked, 0 = inside eps")
    P(fmt(tab, 0))

    # leg C predictor on the census
    pr = s[np.isfinite(s.pred_rev)]
    if len(pr):
        tp = int(((pr.pred_rev == 1) & pr.rev).sum()); fp = int(((pr.pred_rev == 1) & ~pr.rev).sum())
        fn = int(((pr.pred_rev == 0) & pr.rev).sum()); tn = int(((pr.pred_rev == 0) & ~pr.rev).sum())
        P(f"\nLEG C on the census ({len(pr)} RANKED pairs with a Vol column): "
          f"accuracy {(tp+tn)/len(pr):.3f}  precision {tp/max(tp+fp,1):.3f}  recall {tp/max(tp+fn,1):.3f} "
          f"(TP {tp} FP {fp} FN {fn} TN {tn})")

    # ---------------------------------------------------------------- LEG B
    P("\n" + "=" * 100 + "\nLEG B - CONTROLLED RE-READ: one construction, EWall vs FWD-n\n" + "=" * 100)
    panels = build_panels()
    for k, (p, tr) in panels.items():
        e = eligible_mask(p, tr)
        m = rebalance_mask(p.index, FREQ)
        nel = e[m.values].sum(axis=1)
        P(f"  {k}: {len(tr)} tradable, {p.index[0].date()}..{p.index[-1].date()}, "
          f"mean eligible {nel.mean():.1f}")
    yrs = panels['U56'][0].index.to_series().groupby(panels['U56'][0].index.year).count()
    P(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    grid = run_leg_b(panels)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"\ngrid points: {len(grid)} (all written to {STEM}.grid.csv)")
    P(fmt(grid[grid.bps == COST_BPS][["panel", "arm", "n", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2",
                                      "OOS_CAGR", "OOS_Sharpe", "turn", "gross", "sat_share",
                                      "p4a", "p4b", "f4b"]], 4))

    # harness reproduction checks against two rows the record published verbatim
    g10 = grid[grid.bps == COST_BPS]
    b136ew = g10[(g10.panel == "B136") & (g10.arm == "EWall")].iloc[0]
    u56ew = g10[(g10.panel == "U56") & (g10.arm == "EWall")].iloc[0]
    P(f"\nHARNESS REPRODUCTION (rows the record published verbatim):")
    P(f"  B136/EWall  here {b136ew.CAGR:.1%}/{b136ew.Sharpe:.3f}/{b136ew.MaxDD:.1%}, OOS "
      f"{b136ew.OOS_Sharpe:.3f}  vs idea 82/10 published 10.7%/1.026/-17.7%, OOS 1.019")
    P(f"  U56/EWall   here {u56ew.CAGR:.1%}/{u56ew.Sharpe:.3f}/{u56ew.MaxDD:.1%}, 4b fails on "
      f"'{u56ew.f4b}'  vs idea 82 published 'fails 4b on the CAGR floor alone'")

    # paired EWall - FWD differences
    P("\nEWall minus FWD-n, per cell (headline rung 10 bps; 0 bps diagnostic beside it)")
    drows = []
    for (pname, bps), g in grid.groupby(["panel", "bps"]):
        ew = g[g.arm == "EWall"].iloc[0]
        for _, r in g[g.arm == "FWD"].iterrows():
            drows.append(dict(panel=pname, n=int(r.n), bps=bps,
                              dSharpe=ew.Sharpe - r.Sharpe, dCAGR=ew.CAGR - r.CAGR,
                              dMaxDD=ew.MaxDD - r.MaxDD, dVol=ew.Vol - r.Vol,
                              dTurn=ew.turn - r.turn, sat_share=r.sat_share,
                              reverse=bool((np.sign(ew.Sharpe - r.Sharpe) != np.sign(ew.CAGR - r.CAGR))
                                           and abs(ew.Sharpe - r.Sharpe) > EPS_S
                                           and abs(ew.CAGR - r.CAGR) > EPS_C),
                              dOOS_Sharpe=ew.OOS_Sharpe - r.OOS_Sharpe,
                              dOOS_CAGR=ew.OOS_CAGR - r.OOS_CAGR))
    dd = pd.DataFrame(drows)
    dd["rev_OOS"] = ((np.sign(dd.dOOS_Sharpe) != np.sign(dd.dOOS_CAGR))
                     & (dd.dOOS_Sharpe.abs() > EPS_S) & (dd.dOOS_CAGR.abs() > EPS_C))
    dd.to_csv(OUT / f"{STEM}.paired.csv", index=False)
    P(fmt(dd.sort_values(["bps", "panel", "n"]), 4))

    for bps in (COST_BPS, DIAG_BPS):
        u = dd[(dd.bps == bps) & (dd.sat_share <= SAT_CAP)]
        mS, tS, pS = paired_t(u.dSharpe.values)
        mC, tC, pC = paired_t(u.dCAGR.values)
        P(f"\n[{bps} bps, {len(u)} unsaturated cells] EWall-FWD  Sharpe mean {mS:+.4f} t {tS:+.2f} "
          f"{pS}/{len(u)} positive | CAGR mean {mC*100:+.2f} pp/yr t {tC:+.2f} {pC}/{len(u)} positive "
          f"| reversals {int(u.reverse.sum())}/{len(u)}  (OOS reversals {int(u.rev_OOS.sum())}/{len(u)})")

    # reproduction gate: idea 82's own eight cells
    rep = dd[(dd.bps == COST_BPS) & (dd.panel.isin(["U56", "B136", "BSTK100"]))
             & (dd.n.isin([20, 30, 40, 60])) & (dd.sat_share <= SAT_CAP)]
    mS, tS, pS = paired_t(rep.dSharpe.values)
    mC, tC, pC = paired_t((-rep.dCAGR).values)
    P(f"\nREPRODUCTION GATE (idea 82's 3 panels x n in 20/30/40/60, unsaturated = {len(rep)} cells):")
    P(f"  EWall-FWD Sharpe {mS:+.4f} (idea 82 published +0.0467), t {tS:+.2f} (+4.03), "
      f"{pS}/{len(rep)} positive (7/8)")
    P(f"  FWD-EWall CAGR {mC*100:+.2f} pp/yr (published +1.28), t {tC:+.2f} (+4.93), "
      f"{pC}/{len(rep)} positive (8/8)")

    # leg C predictor on the fresh grid
    pv = []
    for (pname, bps), g in grid.groupby(["panel", "bps"]):
        ew = g[g.arm == "EWall"].iloc[0]
        for _, r in g[g.arm == "FWD"].iterrows():
            rr, vr = ew.CAGR / r.CAGR, ew.Vol / r.Vol
            pv.append(dict(panel=pname, n=int(r.n), bps=bps, ret_ratio=rr, vol_ratio=vr,
                           pred=bool((vr < min(rr, 1.0)) or (vr > max(rr, 1.0))),
                           actual=bool((np.sign(ew.Sharpe - r.Sharpe) != np.sign(ew.CAGR - r.CAGR))
                                       and abs(ew.Sharpe - r.Sharpe) > EPS_S
                                       and abs(ew.CAGR - r.CAGR) > EPS_C)))
    pv = pd.DataFrame(pv)
    pv.to_csv(OUT / f"{STEM}.predictor.csv", index=False)
    acc = (pv.pred == pv.actual).mean()
    P(f"\nLEG C on the fresh grid: {len(pv)} cells, predictor accuracy {acc:.3f} "
      f"(TP {int((pv.pred & pv.actual).sum())} FP {int((pv.pred & ~pv.actual).sum())} "
      f"FN {int((~pv.pred & pv.actual).sum())} TN {int((~pv.pred & ~pv.actual).sum())})")
    P(fmt(pv[pv.bps == COST_BPS], 4))

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 100 + "\nRULE 8 WALK-FORWARD: does the metric you quote change the book you run?\n" + "=" * 100)
    wf = rule8(grid)
    # SPY OOS per panel
    spy_oos = {}
    for pname, (px, tr) in panels.items():
        sp = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        m = metrics(sp.loc[OOS_START:])
        spy_oos[pname] = m
    wf["SPY_OOS_Sharpe"] = wf.panel.map(lambda p: spy_oos[p]["Sharpe"])
    wf["SPY_OOS_CAGR"] = wf.panel.map(lambda p: spy_oos[p]["CAGR"])
    wf["SPY_OOS_MaxDD"] = wf.panel.map(lambda p: spy_oos[p]["MaxDD"])
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(wf.sort_values(["bps", "panel", "selector"]), 4))
    for bps in (COST_BPS, DIAG_BPS):
        w = wf[wf.bps == bps]
        P(f"\n[{bps} bps] pooled (equal weight over {w.panel.nunique()} panels):")
        pool = w.groupby("selector")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
        pool["picks"] = w.groupby("selector")["pick"].apply(lambda s: ",".join(s))
        P(fmt(pool, 4))
        agree = w[w.selector.isin(["S_SHARPE", "S_CAGR"])].pivot(index="panel", columns="selector",
                                                                 values="pick")
        P(f"  S_SHARPE vs S_CAGR pick the SAME arm in "
          f"{int((agree.S_SHARPE == agree.S_CAGR).sum())} of {len(agree)} panels: "
          f"{agree.to_dict(orient='index')}")
        d = (w[w.selector == 'S_CAGR'].set_index('panel').OOS_Sharpe
             - w[w.selector == 'S_SHARPE'].set_index('panel').OOS_Sharpe)
        dc = (w[w.selector == 'S_CAGR'].set_index('panel').OOS_CAGR
              - w[w.selector == 'S_SHARPE'].set_index('panel').OOS_CAGR)
        P(f"  S_CAGR minus S_SHARPE OOS: Sharpe {d.mean():+.4f} (per panel {d.round(4).to_dict()}), "
          f"CAGR {dc.mean()*100:+.2f} pp/yr")
        P(f"  RULES v1 OOS Sharpe by panel: "
          f"{w.groupby('panel').v1_OOS_Sharpe.first().round(4).to_dict()}")
        P(f"  SPY OOS Sharpe by panel: {w.groupby('panel').SPY_OOS_Sharpe.first().round(4).to_dict()}")

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 100 + "\nKEEP PATHS over every leg-B point\n" + "=" * 100)
    for bps in (COST_BPS, DIAG_BPS):
        g = grid[grid.bps == bps]
        P(f"[{bps} bps] 4a {int(g.p4a.sum())}/{len(g)}   4b {int(g.p4b.sum())}/{len(g)}")
        P(fmt(g.groupby("arm")[["p4a", "p4b"]].sum().astype(int), 0))
        if g.p4b.any():
            P("  4b passes:")
            P(fmt(g[g.p4b][["panel", "arm", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]], 4))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
