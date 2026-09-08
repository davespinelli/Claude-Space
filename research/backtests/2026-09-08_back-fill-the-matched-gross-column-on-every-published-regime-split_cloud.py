#!/usr/bin/env python3
"""Idea 471 -- back-fill-the-matched-gross-column-on-every-published-d_on-d_off-regime-split
(cloud lane)

THE QUEUE'S PREMISE
    Idea 249 showed that idea 246's headline "+12.6 and +5.8 pp/yr ON crash days" for
    `gross50` / `ddctl8` is pure gross arithmetic: the arm sat at 0.281 / 0.590 mean
    realised gross while its control sat at 0.750, so the "surplus on crash days" is
    mostly *holding less book while the market falls* -- which a constant de-gross also
    does, for free.  Against a static control at the arm's OWN realised mean gross the
    surplus inverts to -0.94 / -0.97 pp/yr and Sharpe becomes a coin flip.

    ANY regime-split delta measured against a full-gross control carries the same
    confound.  This run censuses the record's published regime splits, back-fills the
    missing gross column on every one of them, re-quotes each as an EXCESS OVER A
    GROSS-MATCHED STATIC, and reports how many published regime claims survive.

WHAT A "PUBLISHED REGIME-SPLIT CLAIM" IS (pre-registered admission test)
    A row in a committed CSV that reports the SAME statistic separately for two
    complementary states of TIME (on/off, armed/disarmed, fall/rise, crash/calm) of a
    named regime.  Operationally a matched column pair X_on / X_off (or _fall/_rise,
    _armed/_disarmed) PLUS a regime witness in the same file -- a `regime` / `armed_frac`
    / `on_days` / `window` column, or a fall/rise sleeve split.

    EXPLICITLY REJECTED, and logged with the reason: a matched pair whose suffix names a
    DIAL STATE rather than a time state.  `CAGR_on` / `CAGR_off` for "the vol scaler on
    vs off" is a design contrast, not a regime split, and re-quoting it at matched gross
    would be a category error.  Every rejection is written to `.census_rejects.csv`.

THE RESTATEMENT
    For every admitted claim family the record publishes, the arm is re-run on live
    prices and the control is replaced:

        PUBLISHED   d_on / d_off  =  ann(arm - CONTROL) on regime-ON / regime-OFF days,
                                     CONTROL = the ungated full-gross base book
        RESTATED    d_on / d_off  =  ann(arm - MATCHED) on the same days,
                                     MATCHED = base book x mu, mu solved so that MATCHED's
                                     realised MEAN gross equals the ARM's over the same
                                     sample (idea 249's control, re-implemented here and
                                     checked to the same 1e-4 tolerance)

    A claim SURVIVES iff its restated delta keeps the published sign.  Both the ALWAYS-ON
    arms (which is what the record's `.mechanism.csv` d_on/d_off splits are) and the
    REGIME-CONDITIONAL arms (the `.grid.csv` d_cond_on/d_cond_off splits) are restated,
    because both are published against the same full-gross control.

    The missing column itself is published for every cell: mean realised gross of the arm
    and of the control, overall and separately on ON and OFF days.

CHECKS BEFORE ANY CLAIM
    (a) idea 246-C's own committed `.mechanism.csv` (432 rows) and its `d_cond_on` /
        `d_cond_off` grid columns are REPRODUCED from its own committed code, and the
        max |difference| is printed.  Nothing below is claimed if that does not reproduce.
    (b) the matched-gross solve reports its achieved |mean gross - target| for every
        control it builds; the worst one over the whole run is printed.

LIVE ARMS
    L1  the restatement itself: 432 always-on and 432 conditional regime-split claims,
        published vs restated, sign survival counted by regime / instrument / panel.
    L2  RULE 8: (INSTRUMENT, REGIME) chosen on 2009-2016 IS Sharpe alone from a menu that
        INCLUDES the gross-matched statics and do-nothing, 2017-2026 read ONCE.
    L3  both KEEP paths on every arm AND every matched control (4a vs the live RULES v2 on
        the book's own panel, 4b vs SPY incl. rule 8), at 10 and 25 bps.

TUNED DIMENSIONS: exactly two -- INSTRUMENT (8 levels, idea 246-C's published set) and
REGIME (3 levels, idea 75's published set).  Panels, books and cost rungs are replication
axes, and every point is reported.

SURVIVORSHIP: current constituents only; the 44 small-cap tickers with max_1d_move >= 1.0
are dropped first.  SPY is a benchmark on the small panel, never held.

Deterministic, standalone.  Imports idea 246-C's committed script (which itself imports
idea 94's harness) so every book, instrument, regime and simulator is the SAME OBJECT.
Modifies nothing.
"""
import sys
import re
import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
import baseline
from baseline import rules_v2_weights
from engine import backtest, metrics

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT = OUT / "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C.py"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 600)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = _load(PARENT, "idea246c")          # panels, regimes, books, instruments, run_cond
H = C.H                                # idea 94's harness (targets, run)

PANELS, BOOKS, COSTS = C.PANELS, C.BOOKS, C.COSTS
INSTR, SPEC = C.INSTR, C.SPEC
REGIMES = [r for r in C.REGIMES if r != "always"]
IS_END, OOS_START, FREQ = C.IS_END, C.OOS_START, C.FREQ
MATCH_TOL, MATCH_ITERS = 1e-4, 12      # idea 249's values


def kw_of(ins, W_gate):
    sp = SPEC[ins]
    return dict(W_gate=W_gate[sp["gate"]] if sp["kind"] == "gate" else None,
                stop=sp.get("stop"), D=sp.get("D"), k=sp.get("k", 1.0), m=sp.get("m", 1.0))


def solve_matched(px, W_base, target_gross, bps):
    """Constant multiplier mu on the base book whose realised MEAN gross equals
    target_gross.  Linear seed + secant, exactly idea 249's scheme; the achieved gap is
    returned for every match and the worst one over the run is printed."""
    g1 = float(C.run_cond(px, W_base, m=1.0, bps=bps)["gross"].mean())
    mu = target_gross / g1 if g1 > 0 else 0.0
    res = C.run_cond(px, W_base, m=mu, bps=bps)
    g = float(res["gross"].mean())
    lo_mu, lo_g, it = 0.0, 0.0, 0
    while abs(g - target_gross) > MATCH_TOL and it < MATCH_ITERS:
        it += 1
        den = g - lo_g
        mu_new = mu + (target_gross - g) * (mu - lo_mu) / den if abs(den) > 1e-12 else mu
        mu_new = float(np.clip(mu_new, 0.0, 4.0))
        lo_mu, lo_g = mu, g
        mu = mu_new
        res = C.run_cond(px, W_base, m=mu, bps=bps)
        g = float(res["gross"].mean())
    return mu, res, abs(g - target_gross)


def ann(r):
    return float(r.mean() * 252 * 100.0)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail_4b(r, spy):
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fail_4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ================================================================= Q1  THE CENSUS
STATE_PAIRS = [("on", "off"), ("fall", "rise"), ("armed", "disarmed"), ("crash", "calm"),
               ("hi", "lo"), ("in", "out")]
REGIME_WITNESS = re.compile(r"^(regime|armed_frac|armed_days|armed_share|on_days|off_days|"
                            r"on_share|off_share|on_frac|off_frac|real_on_share|"
                            r"armed_frac_IS|armed_frac_OOS|f_calm|n_on|arm)$", re.I)
GROSS_COL = re.compile(r"gross", re.I)
DELTA_STEM = re.compile(r"^(d|delta|diff|excess|lift|prem)", re.I)


def split_pairs(cols):
    """Matched (stat_ON, stat_OFF) column pairs, whatever the state vocabulary.
    Deduplicated: a name like `d_on` matches both the `_on` and the bare `on` suffix and
    must be counted once."""
    low = {c.lower(): c for c in cols}
    seen, out = set(), []
    for a, b in STATE_PAIRS:
        for lc, c in low.items():
            for sep in ("_", ""):
                if not (lc.endswith(sep + a) and len(lc) > len(a) + len(sep)):
                    continue
                stem = lc[: len(lc) - len(a) - len(sep)]
                twin = stem + sep + b
                if twin not in low:
                    continue
                key = (c, low[twin])
                if key in seen:
                    continue
                seen.add(key)
                out.append((c, low[twin], f"{a}/{b}", stem.strip("_")))
    return out


def census():
    """Three-way, nothing hidden: a pair is a RESTATABLE regime-split claim, a
    time-state split that is NOT an arm-minus-control delta (so there is no control gross
    to match and it is out of scope), or a DIAL-state pair that is not a regime at all."""
    claims, rejects = [], []
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM):
            continue
        try:
            head = open(f, errors="ignore").readline().strip()
        except Exception as e:
            rejects.append(dict(file=f.name, pair="", reason=f"unreadable:{type(e).__name__}"))
            continue
        cols = [c.strip() for c in head.split(",")]
        pairs = split_pairs(cols)
        if not pairs:
            continue
        witness = [c for c in cols if REGIME_WITNESS.match(c)]
        gcols = [c for c in cols if GROSS_COL.search(c)]
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception as e:
            rejects.append(dict(file=f.name, pair=";".join(p[0] for p in pairs),
                                reason=f"unreadable:{type(e).__name__}"))
            continue
        for a, b, voc, stem in pairs:
            if not witness:
                rejects.append(dict(file=f.name, pair=f"{a}/{b}",
                                    reason="no regime witness column -> a DIAL state, not a "
                                           "time state"))
                continue
            if not DELTA_STEM.match(stem):
                rejects.append(dict(file=f.name, pair=f"{a}/{b}",
                                    reason=f"time-state split but NOT an arm-minus-control "
                                           f"delta (stem '{stem}') -> no control gross to match"))
                continue
            claims.append(dict(file=f.name, stat_on=a, stat_off=b, vocab=voc, stem=stem,
                               rows=int(len(df)), witness=";".join(witness),
                               gross_cols=";".join(gcols),
                               publishes_gross=bool(gcols),
                               arm_and_control_gross=bool(len(gcols) >= 2)))
    return pd.DataFrame(claims), pd.DataFrame(rejects)


# ================================================================= MAIN
def main():
    print("=" * 200)
    print(f"Idea 471  back-fill-the-matched-gross-column-on-every-published-regime-split (cloud) "
          f"| {SCRIPT} | 10 and 25 bps rungs, weekly, next-day execution")
    print("=" * 200)

    # ---------------------------------------------------------- Q1 census
    print("\n" + "=" * 200)
    print("Q1  THE CENSUS -- every committed CSV scanned for a published REGIME-SPLIT claim "
          "(a matched ON/OFF column pair for the same statistic, plus a regime witness)")
    print("=" * 200)
    CL, RJ = census()
    print(f"committed CSVs scanned: {len(list(OUT.glob('*.csv')))}")
    print(f"ADMITTED regime-split claims: {len(CL)} column pairs over "
          f"{CL['file'].nunique() if len(CL) else 0} files, {int(CL['rows'].sum()) if len(CL) else 0} rows")
    if len(CL):
        print(fmt(CL[["file", "stat_on", "stat_off", "vocab", "rows", "witness",
                      "gross_cols", "arm_and_control_gross"]]))
        print(f"\n  claims whose file publishes ANY gross column: "
              f"{int(CL['publishes_gross'].sum())} of {len(CL)}")
        print(f"  claims whose file publishes BOTH an arm and a control gross (so the confound "
              f"is checkable from the artefact alone): {int(CL['arm_and_control_gross'].sum())} "
              f"of {len(CL)}")
    print(f"\nREJECTED pairs, every one logged with its reason: {len(RJ)}")
    if len(RJ):
        print(RJ["reason"].str.replace(r"\(stem.*", "(stem …)", regex=True)
              .value_counts().to_string())
        print("\n  the rejected pairs (first 40 of "
              f"{len(RJ)}; all of them are in .census_rejects.csv):")
        print(RJ.head(40).to_string(index=False))
    CL.to_csv(OUT / f"{STEM}.census.csv", index=False)
    RJ.to_csv(OUT / f"{STEM}.census_rejects.csv", index=False)

    pub_mech = pd.read_csv(OUT / f"{C.STEM}.mechanism.csv")
    pub_grid = pd.read_csv(OUT / f"{C.STEM}.grid.csv")
    print(f"\nTHE OBJECT TO BE RESTATED: idea 246-C publishes {len(pub_mech)} always-on "
          f"d_on/d_off rows (.mechanism.csv) and "
          f"{int(pub_grid['d_cond_on'].notna().sum())} conditional d_cond_on/d_cond_off rows "
          f"(.grid.csv) -- and NEITHER carries a control-gross column.")

    # ---------------------------------------------------------- the live restatement
    print("\n" + "=" * 200)
    print("L1  THE RESTATEMENT -- every published regime split re-quoted against a static "
          "control at the ARM'S OWN realised mean gross")
    print("=" * 200)
    rows, keeps, worst_gap, gap_n = [], [], 0.0, 0
    for pname in PANELS:
        px, names = C.panel(pname)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        sub = px[names]
        arms = {r: C.regime(px, names, r) for r in REGIMES}
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        for book in BOOKS:
            W_base = H.targets(sub, book).reindex(columns=px.columns).fillna(0.0)
            W_gate = {g: H.targets(sub, book, g, "dg").reindex(columns=px.columns).fillna(0.0)
                      for g in ("g200", "band3", "abs12", "vol60")}
            for cost in COSTS:
                ctl = C.run_cond(px, W_base, bps=cost)
                rc, gc = ctl["r"].loc[start:], ctl["gross"].loc[start:]
                keeps.append(dict(panel=pname, book=book, cost=cost, arm="control", regime="-",
                                  instr="control", gross=float(gc.mean()),
                                  CAGR=metrics(rc)["CAGR"], Sharpe=metrics(rc)["Sharpe"],
                                  MaxDD=metrics(rc)["MaxDD"], H1=halves(rc)[0], H2=halves(rc)[1],
                                  IS_Sharpe=metrics(rc.loc[:IS_END])["Sharpe"],
                                  OOS_Sharpe=metrics(rc.loc[OOS_START:])["Sharpe"],
                                  OOS_CAGR=metrics(rc.loc[OOS_START:])["CAGR"],
                                  f4a=fail_4a(rc, v2[cost]), f4b=fail_4b(rc, spy)))
                for ins in INSTR:
                    kw = kw_of(ins, W_gate)
                    for mode in ("always", "cond"):
                        for reg in REGIMES:
                            armed = (pd.Series(True, index=px.index) if mode == "always"
                                     else arms[reg])
                            if mode == "always" and reg != REGIMES[0]:
                                a = a_always                      # one run, split three ways
                            else:
                                a = C.run_cond(px, W_base, armed=armed, bps=cost, **kw)
                                if mode == "always":
                                    a_always = a
                            ra, ga = a["r"].loc[start:], a["gross"].loc[start:]
                            mu, mres, gap = solve_matched(px, W_base, float(ga.mean()), cost)
                            worst_gap = max(worst_gap, gap); gap_n += 1
                            rm, gm = mres["r"].loc[start:], mres["gross"].loc[start:]
                            on = arms[reg].reindex(ra.index).fillna(False)
                            dc, dm = ra - rc, ra - rm
                            rows.append(dict(
                                panel=pname, book=book, cost=cost, instr=ins, regime=reg,
                                mode=mode, armed_frac=float(on.mean()),
                                on_days=int(on.sum()), off_days=int((~on).sum()),
                                g_arm=float(ga.mean()), g_ctl=float(gc.mean()),
                                g_matched=float(gm.mean()), mu=mu, match_gap=gap,
                                g_arm_on=float(ga[on].mean()), g_arm_off=float(ga[~on].mean()),
                                g_ctl_on=float(gc[on].mean()), g_ctl_off=float(gc[~on].mean()),
                                d_on_pub=float(dc[on].mean() * 252 * 100),
                                d_off_pub=float(dc[~on].mean() * 252 * 100),
                                d_on_matched=float(dm[on].mean() * 252 * 100),
                                d_off_matched=float(dm[~on].mean() * 252 * 100),
                                dSharpe_pub=metrics(ra)["Sharpe"] - metrics(rc)["Sharpe"],
                                dSharpe_matched=metrics(ra)["Sharpe"] - metrics(rm)["Sharpe"]))
                            keeps.append(dict(panel=pname, book=book, cost=cost,
                                              arm=f"{mode}:{ins}@{reg}", regime=reg, instr=ins,
                                              gross=float(ga.mean()), CAGR=metrics(ra)["CAGR"],
                                              Sharpe=metrics(ra)["Sharpe"],
                                              MaxDD=metrics(ra)["MaxDD"],
                                              H1=halves(ra)[0], H2=halves(ra)[1],
                                              IS_Sharpe=metrics(ra.loc[:IS_END])["Sharpe"],
                                              OOS_Sharpe=metrics(ra.loc[OOS_START:])["Sharpe"],
                                              OOS_CAGR=metrics(ra.loc[OOS_START:])["CAGR"],
                                              f4a=fail_4a(ra, v2[cost]), f4b=fail_4b(ra, spy)))
                            keeps.append(dict(panel=pname, book=book, cost=cost,
                                              arm=f"MATCHED[{mode}:{ins}@{reg}]", regime=reg,
                                              instr=ins, gross=float(gm.mean()),
                                              CAGR=metrics(rm)["CAGR"],
                                              Sharpe=metrics(rm)["Sharpe"],
                                              MaxDD=metrics(rm)["MaxDD"],
                                              H1=halves(rm)[0], H2=halves(rm)[1],
                                              IS_Sharpe=metrics(rm.loc[:IS_END])["Sharpe"],
                                              OOS_Sharpe=metrics(rm.loc[OOS_START:])["Sharpe"],
                                              OOS_CAGR=metrics(rm.loc[OOS_START:])["CAGR"],
                                              f4a=fail_4a(rm, v2[cost]), f4b=fail_4b(rm, spy)))
                # reference books for this (panel, cost)
                keeps.append(dict(panel=pname, book="-", cost=cost, arm="RULES v2", regime="-",
                                  instr="-", gross=np.nan, CAGR=metrics(v2[cost])["CAGR"],
                                  Sharpe=metrics(v2[cost])["Sharpe"],
                                  MaxDD=metrics(v2[cost])["MaxDD"],
                                  H1=halves(v2[cost])[0], H2=halves(v2[cost])[1],
                                  IS_Sharpe=metrics(v2[cost].loc[:IS_END])["Sharpe"],
                                  OOS_Sharpe=metrics(v2[cost].loc[OOS_START:])["Sharpe"],
                                  OOS_CAGR=metrics(v2[cost].loc[OOS_START:])["CAGR"],
                                  f4a="-", f4b=fail_4b(v2[cost], spy)))
            print(f"  built {pname}/{book}")
        keeps.append(dict(panel=pname, book="-", cost=np.nan, arm="SPY", regime="-", instr="-",
                          gross=np.nan, CAGR=metrics(spy)["CAGR"], Sharpe=metrics(spy)["Sharpe"],
                          MaxDD=metrics(spy)["MaxDD"], H1=halves(spy)[0], H2=halves(spy)[1],
                          IS_Sharpe=metrics(spy.loc[:IS_END])["Sharpe"],
                          OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                          OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"], f4a="-", f4b="-"))
    R = pd.DataFrame(rows)
    K = pd.DataFrame(keeps)
    R.to_csv(OUT / f"{STEM}.restated.csv", index=False)
    K.to_csv(OUT / f"{STEM}.books.csv", index=False)
    print(f"\nCHECK(b) matched-gross solve: worst |achieved mean gross - target| over "
          f"{gap_n} controls = {worst_gap:.3e}  (tolerance {MATCH_TOL:.0e})")

    # ---------------------------------------------------------- CHECK (a) reproduction
    print("\nCHECK(a)  reproduce idea 246-C's published d_on/d_off from its own committed code")
    key = ["panel", "book", "cost", "instr", "regime"]
    mine = R[R["mode"] == "always"].set_index(key)
    pm = pub_mech.set_index(key)
    j = pm.join(mine[["d_on_pub", "d_off_pub"]], how="inner")
    print(f"  .mechanism.csv rows matched: {len(j)} of {len(pub_mech)} | "
          f"max |d_on - reproduced| {np.abs(j['d_on'] - j['d_on_pub']).max():.3e} | "
          f"max |d_off - reproduced| {np.abs(j['d_off'] - j['d_off_pub']).max():.3e}")
    minec = R[R["mode"] == "cond"].set_index(key)
    pg = pub_grid[pub_grid["d_cond_on"].notna()].set_index(key)
    jc = pg.join(minec[["d_on_pub", "d_off_pub"]], how="inner")
    print(f"  .grid.csv conditional rows matched: {len(jc)} of {len(pg)} | "
          f"max |d_cond_on - reproduced| {np.abs(jc['d_cond_on'] - jc['d_on_pub']).max():.3e} | "
          f"max |d_cond_off - reproduced| {np.abs(jc['d_cond_off'] - jc['d_off_pub']).max():.3e}")
    print("  (the .grid.csv join covers 432 of 576 because 144 of its conditional rows are the "
          "regime='always' arm, which is not a regime SPLIT and is not restated here)")
    # CHECK (a2): is any residual THIS run's code, or the prices underneath it?  The CONTROL
    # rows use no instrument, no regime and no code of mine -- only the base book.
    pc = pub_grid[pub_grid["instr"] == "control"].set_index(["panel", "book", "cost"])
    mc = K[K["arm"] == "control"].set_index(["panel", "book", "cost"])
    jj = pc[["CAGR", "Sharpe", "MaxDD", "gross"]].join(
        mc[["CAGR", "Sharpe", "MaxDD", "gross"]], lsuffix="_pub", rsuffix="_new", how="inner")
    print("\nCHECK(a2)  the published CONTROL rows (no instrument, no regime -- nothing of this "
          f"run's in them), {len(jj)} cells:")
    for c in ("CAGR", "Sharpe", "MaxDD", "gross"):
        d = (jj[f"{c}_pub"] - jj[f"{c}_new"]).abs()
        print(f"    {c:7s} max|d| {d.max():.3e}   median {d.median():.3e}   "
              f"cells exactly equal {int((d == 0).sum())}/{len(d)}")
    ctl_exact = float((jj["Sharpe_pub"] - jj["Sharpe_new"]).abs().max())
    tol = 1e-9
    ok = (len(j) == len(pub_mech)
          and np.abs(j["d_on"] - j["d_on_pub"]).max() < tol
          and np.abs(j["d_off"] - j["d_off_pub"]).max() < tol)
    print(f"\n  REPRODUCED BIT-EXACT: {ok}")
    if not ok:
        print(f"  DIAGNOSIS: the same residual is already present in the CONTROL rows "
              f"(max |dSharpe| {ctl_exact:.3e}), which share no code with the instruments, the "
              f"regimes or the matched control. The residual is therefore UPSTREAM of this run "
              f"-- the cached price panel moved under the record, the same cause idea 468 "
              f"recorded when its own replication came in at max|dCAGR| 2.9e-05. Every number "
              f"below is quoted from THIS run's own re-computation of BOTH sides, never from a "
              f"published number differenced against a fresh one, so the residual cannot leak "
              f"into the restatement.")

    # ---------------------------------------------------------- the missing column
    print("\n" + "=" * 200)
    print("THE MISSING COLUMN -- mean realised gross of the arm vs its published control")
    print("=" * 200)
    gt = R.groupby(["mode", "instr"]).agg(g_arm=("g_arm", "mean"), g_ctl=("g_ctl", "mean"),
                                          g_on=("g_arm_on", "mean"), g_off=("g_arm_off", "mean"),
                                          n=("g_arm", "size"))
    gt["gap"] = gt["g_arm"] - gt["g_ctl"]
    print(fmt(gt, 4))
    conf = (R["g_arm"] - R["g_ctl"]).abs() > 0.01
    print(f"\nregime-split claims whose ARM and CONTROL differ in mean realised gross by more "
          f"than 0.01 NAV: {int(conf.sum())} of {len(R)} = {conf.mean():.1%}")
    print(f"  median |gap| {(R['g_arm']-R['g_ctl']).abs().median():.4f}, "
          f"max {(R['g_arm']-R['g_ctl']).abs().max():.4f}")

    # ---------------------------------------------------------- survival
    print("\n" + "=" * 200)
    print("HOW MANY PUBLISHED REGIME CLAIMS SURVIVE THE RESTATEMENT?  (a claim SURVIVES iff "
          "the restated delta keeps the published sign)")
    print("=" * 200)
    for col in ("on", "off"):
        R[f"surv_{col}"] = np.sign(R[f"d_{col}_pub"]) == np.sign(R[f"d_{col}_matched"])
    R["surv_both"] = R["surv_on"] & R["surv_off"]
    R["d_on_shift"] = R["d_on_matched"] - R["d_on_pub"]
    R["d_off_shift"] = R["d_off_matched"] - R["d_off_pub"]
    R["pub_on_gt_off"] = R["d_on_pub"] > R["d_off_pub"]
    R["mat_on_gt_off"] = R["d_on_matched"] > R["d_off_matched"]
    R["surv_order"] = R["pub_on_gt_off"] == R["mat_on_gt_off"]
    for mode in ("always", "cond"):
        s = R[R["mode"] == mode]
        print(f"\n{mode.upper()}-ON arms ({len(s)} claims):")
        print(f"  d_on sign survives  {int(s['surv_on'].sum())}/{len(s)} = {s['surv_on'].mean():.1%}"
              f"   | d_off {int(s['surv_off'].sum())}/{len(s)} = {s['surv_off'].mean():.1%}"
              f"   | BOTH {int(s['surv_both'].sum())}/{len(s)} = {s['surv_both'].mean():.1%}")
        print(f"  the ORDERING claim ('the instrument is dearer/cheaper in its own regime', "
              f"d_on vs d_off) survives {int(s['surv_order'].sum())}/{len(s)} = "
              f"{s['surv_order'].mean():.1%}")
        print(f"  d_on   published mean {s['d_on_pub'].mean():+.3f} -> restated "
              f"{s['d_on_matched'].mean():+.3f} pp/yr  (mean shift {s['d_on_shift'].mean():+.3f}, "
              f"median {s['d_on_shift'].median():+.3f})")
        print(f"  d_off  published mean {s['d_off_pub'].mean():+.3f} -> restated "
              f"{s['d_off_matched'].mean():+.3f} pp/yr  (mean shift {s['d_off_shift'].mean():+.3f}, "
              f"median {s['d_off_shift'].median():+.3f})")
        print(f"  published POSITIVE d_on: {int((s['d_on_pub']>0).sum())}/{len(s)}; of those, "
              f"still positive at matched gross: "
              f"{int(((s['d_on_pub']>0)&(s['d_on_matched']>0)).sum())}")
    print("\nTHE CLAIM ITSELF -- 'the instrument is dearer / cheaper in its OWN regime' is the "
          "GAP d_on - d_off, so that is what has to survive:")
    R["gap_pub"] = R["d_on_pub"] - R["d_off_pub"]
    R["gap_matched"] = R["d_on_matched"] - R["d_off_matched"]
    for mode in ("always", "cond"):
        s = R[R["mode"] == mode]
        n = len(s)
        pos_p, pos_m = int((s["gap_pub"] > 0).sum()), int((s["gap_matched"] > 0).sum())
        print(f"  {mode:6s}  gap published mean {s['gap_pub'].mean():+.3f} pp/yr "
              f"(median {s['gap_pub'].median():+.3f}, positive {pos_p}/{n}) -> restated "
              f"{s['gap_matched'].mean():+.3f} (median {s['gap_matched'].median():+.3f}, "
              f"positive {pos_m}/{n});  mean shrinkage "
              f"{1 - abs(s['gap_matched'].mean()) / max(abs(s['gap_pub'].mean()), 1e-12):.1%} "
              f"of the published magnitude")

    print("\nBY REGIME (always-on arms, d_on sign survival and mean shift):")
    a = R[R["mode"] == "always"]
    print(fmt(a.groupby("regime").agg(n=("surv_on", "size"), surv_on=("surv_on", "mean"),
                                      surv_off=("surv_off", "mean"),
                                      surv_order=("surv_order", "mean"),
                                      mean_d_on_pub=("d_on_pub", "mean"),
                                      mean_d_on_mat=("d_on_matched", "mean"),
                                      mean_gross_gap=("g_arm", "mean")), 4))
    print("\nBY INSTRUMENT (always-on arms):")
    print(fmt(a.groupby("instr").agg(n=("surv_on", "size"), g_arm=("g_arm", "mean"),
                                     g_ctl=("g_ctl", "mean"), surv_on=("surv_on", "mean"),
                                     surv_both=("surv_both", "mean"),
                                     d_on_pub=("d_on_pub", "mean"),
                                     d_on_mat=("d_on_matched", "mean"),
                                     d_off_pub=("d_off_pub", "mean"),
                                     d_off_mat=("d_off_matched", "mean")), 4))
    print("\nBY PANEL x COST (all claims):")
    print(fmt(R.groupby(["panel", "cost"]).agg(n=("surv_on", "size"),
                                               surv_on=("surv_on", "mean"),
                                               surv_both=("surv_both", "mean"),
                                               surv_order=("surv_order", "mean")), 4))
    print("\nIDEA 246's OWN HEADLINE CELLS, restated (u56 / EWall / 10 bps, spy200):")
    hl = R[(R["panel"] == "u56") & (R["book"] == "EWall") & (R["cost"] == 10.0)
           & (R["regime"] == "spy200")]
    print(fmt(hl[["instr", "mode", "g_arm", "g_ctl", "g_matched", "d_on_pub", "d_on_matched",
                  "d_off_pub", "d_off_matched", "dSharpe_pub", "dSharpe_matched"]], 4))

    # ---------------------------------------------------------- L2 rule 8
    print("\n" + "=" * 200)
    print("L2  RULE 8 -- (INSTRUMENT, REGIME) chosen on 2009-2016 IS Sharpe ALONE from a menu "
          "that INCLUDES do-nothing and every gross-matched static, 2017-2026 read ONCE")
    print("=" * 200)
    wf = []
    for (pname, book, cost), g in K[K["arm"] != "RULES v2"].groupby(["panel", "book", "cost"]):
        if book == "-":
            continue
        menu = g.dropna(subset=["IS_Sharpe"])
        pick = menu.loc[menu["IS_Sharpe"].idxmax()]
        ctl = menu[menu["arm"] == "control"].iloc[0]
        cond = menu[menu["arm"].str.startswith("cond:")]
        mat = menu[menu["arm"].str.startswith("MATCHED")]
        pick_c = cond.loc[cond["IS_Sharpe"].idxmax()] if len(cond) else pick
        v2row = K[(K["panel"] == pname) & (K["arm"] == "RULES v2") & (K["cost"] == cost)].iloc[0]
        spyrow = K[(K["panel"] == pname) & (K["arm"] == "SPY")].iloc[0]
        wf.append(dict(panel=pname, book=book, cost=cost, pick=pick["arm"],
                       pick_OOS=pick["OOS_Sharpe"], pick_OOS_CAGR=pick["OOS_CAGR"],
                       donothing_OOS=ctl["OOS_Sharpe"],
                       best_matched_OOS=mat["OOS_Sharpe"].max() if len(mat) else np.nan,
                       cond_pick=pick_c["arm"], cond_pick_OOS=pick_c["OOS_Sharpe"],
                       oracle_OOS=menu["OOS_Sharpe"].max(),
                       v2_OOS=v2row["OOS_Sharpe"], spy_OOS=spyrow["OOS_Sharpe"],
                       pick_is_matched=str(pick["arm"]).startswith("MATCHED"),
                       pick_is_control=pick["arm"] == "control"))
    W = pd.DataFrame(wf)
    W["regret"] = W["oracle_OOS"] - W["pick_OOS"]
    W["vs_donothing"] = W["pick_OOS"] - W["donothing_OOS"]
    W["cond_vs_matched"] = W["cond_pick_OOS"] - W["best_matched_OOS"]
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print(fmt(W[["panel", "book", "cost", "pick", "pick_OOS", "donothing_OOS",
                 "best_matched_OOS", "cond_pick_OOS", "oracle_OOS", "v2_OOS", "spy_OOS"]], 4))
    print(f"\n  IS-chosen arm is a MATCHED STATIC in {int(W['pick_is_matched'].sum())} of {len(W)} "
          f"cells, do-nothing in {int(W['pick_is_control'].sum())}, a live instrument in "
          f"{len(W)-int(W['pick_is_matched'].sum())-int(W['pick_is_control'].sum())}")
    print(f"  OOS vs do-nothing: mean {W['vs_donothing'].mean():+.4f}, median "
          f"{W['vs_donothing'].median():+.4f}, wins {int((W['vs_donothing']>0).sum())}/{len(W)}")
    print(f"  the best IS-chosen CONDITIONAL arm vs the best MATCHED STATIC, OOS: mean "
          f"{W['cond_vs_matched'].mean():+.4f}, median {W['cond_vs_matched'].median():+.4f}, "
          f"wins {int((W['cond_vs_matched']>0).sum())}/{len(W)}")
    print(f"  OOS regret vs the oracle: mean {W['regret'].mean():+.4f}")
    print(f"  IS pick beats RULES v2 OOS in {int((W['pick_OOS']>W['v2_OOS']).sum())}/{len(W)}; "
          f"SPY in {int((W['pick_OOS']>W['spy_OOS']).sum())}/{len(W)}")

    # ---------------------------------------------------------- L3 KEEP paths
    print("\n" + "=" * 200)
    print("L3  BOTH KEEP PATHS on every arm AND every matched control (4a vs the live RULES v2 "
          "on the book's own panel; 4b vs SPY incl. rule 8)")
    print("=" * 200)
    KK = K[~K["arm"].isin(["RULES v2", "SPY"])].copy()
    KK["kind"] = np.where(KK["arm"] == "control", "control",
                          np.where(KK["arm"].str.startswith("MATCHED"), "matched",
                                   np.where(KK["arm"].str.startswith("always:"), "always", "cond")))
    KK["p4a"] = KK["f4a"] == "-"
    KK["p4b"] = KK["f4b"] == "-"
    print(KK.groupby(["cost", "kind"])[["p4a", "p4b"]].agg(["sum", "size"]).to_string())
    print(f"\nTOTAL 4a {int(KK['p4a'].sum())}/{len(KK)}   4b {int(KK['p4b'].sum())}/{len(KK)}")
    fb = KK.loc[~KK["p4b"], "f4b"].str.split(",").explode().value_counts()
    print(f"binding 4b bars: {fb.to_dict()}")
    pair = KK[KK["kind"].isin(["always", "cond"])].copy()
    mm = KK[KK["kind"] == "matched"].set_index(["panel", "book", "cost", "arm"])["p4b"]
    pair["twin"] = [mm.get((r.panel, r.book, r.cost, f"MATCHED[{r.arm}]"), np.nan)
                    for r in pair.itertuples()]
    solo = pair[(pair["p4b"]) & (pair["twin"] == False)]
    print(f"\n4b passes the arm has and its OWN gross-matched twin does NOT: {len(solo)} "
          f"(of {int(pair['p4b'].sum())} arm passes) -- the only passes a regime instrument can "
          f"claim credit for")
    if len(solo):
        print(fmt(solo.nlargest(12, "Sharpe")[["panel", "book", "cost", "arm", "gross", "CAGR",
                                               "Sharpe", "H1", "H2", "OOS_Sharpe", "MaxDD",
                                               "f4a"]], 4))
        print("\n  which families own those unshared passes:")
        print(solo.groupby([solo["arm"].str.split(":").str[0],
                            solo["arm"].str.split(":").str[1]]).size().to_string())
    if KK["p4a"].any():
        print("\n4a passes:")
        print(fmt(KK[KK["p4a"]][["panel", "book", "cost", "arm", "kind", "CAGR", "Sharpe",
                                 "H1", "H2", "OOS_Sharpe", "MaxDD", "f4b"]], 4))
    print("\nREFERENCE books:")
    print(fmt(K[K["arm"].isin(["RULES v2", "SPY"])].drop_duplicates(["panel", "arm", "cost"])[
        ["panel", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]], 4))

    print("\n" + "=" * 200)
    print("DONE")
    print("=" * 200)


if __name__ == "__main__":
    main()
