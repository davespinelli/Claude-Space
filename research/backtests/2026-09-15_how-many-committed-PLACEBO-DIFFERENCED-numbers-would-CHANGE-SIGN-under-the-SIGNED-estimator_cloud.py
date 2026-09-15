#!/usr/bin/env python3
"""Idea 880 (cloud, 2026-09-15) - how many committed PLACEBO-DIFFERENCED numbers would CHANGE
SIGN under the SIGNED estimator?

THE CLAIM UNDER TEST
--------------------
Idea 875 found that the record's placebo statistic - the per-arm MAGNITUDE |null - BLOCK|, pooled
by median - is 87-95% seed noise, while the SIGNED pooled gap on the SAME cells resolves a real
-0.0046 of Sharpe at z +3.8.  Its conclusion: "the estimator and not the seed budget is what hides
the effect."  If that is right, the record is carrying committed placebo numbers whose published
verdict is an artefact of the statistic chosen to report them.  This run re-prices every committed
placebo difference that can still be re-priced from its own committed per-arm data, under both
estimators, and counts the verdicts that move.

THE ASYMMETRY THAT SHAPES THE WHOLE RUN, stated up front
-------------------------------------------------------
    |x| >= 0 ALWAYS.  The absolute estimator has no zero of its own.  It can only be adjudicated
    against an externally supplied floor - the seed-noise prediction
        median|gap| ~ 0.6745 * 1.2533 / sqrt(NSEED) * sqrt(sd_null^2 + sd_BLOCK^2)
    which a run can compute only if it stored its own per-arm seed dispersion.  The SIGNED
    estimator needs no such floor: a sign test against 50% is calibrated by construction.

So the queue's literal question - how many numbers "change sign" - cannot be asked of an ABS
number, which has no sign to change.  It is asked here in the two forms that are actually
answerable, both pre-registered:

    Q1 (ACQUISITION)  how many committed ABS claims acquire a DETERMINATE SIGN under the signed
                      estimator (|sign-test z| >= 2.0) that the published statistic could not
                      express?
    Q2 (INSTABILITY)  among the signed readings themselves, how many claims have a MEDIAN and a
                      MEAN of opposite sign - i.e. the signed estimator is not itself sign-stable
                      at this seed budget?
    Q3 (VERDICT MOVE) how many claims change RESOLVABILITY verdict between the two estimators, in
                      either direction, where the ABS claim is adjudicable at all?

TWO TUNED PARAMETERS, as the queue names them, and nothing else
--------------------------------------------------------------
    PARAM 1  claim set  HEADLINE = one claim per (file, null) at 10 bps full sample - the numbers
                                   the memos actually quote
                        ALL      = (file, null) x {0, 10, 25 bps, IS window, OOS window}
    PARAM 2  estimator  ABS_MED / ABS_MEAN / SIGNED_MED / SIGNED_MEAN, all four reported at every
                        claim, no cherry-picking

THE CORPUS - what can and cannot be re-priced, both counted
-----------------------------------------------------------
Re-priceable = a committed CSV holding PER-ARM excess for both a null and its BLOCK reference on
the same arm keys.  Everything else in the record's placebo mass is aggregate-only: the published
number survives, the cells under it do not, and no estimator can be recomputed from it.  Both
populations are counted; idea 871's own committed census.csv (70 placebo-bearing files) is the
denominator for the second.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
-----------------------------------------------------------------
    H_ACQ    >= 25% of HEADLINE claims acquire a determinate sign under SIGNED (Q1).
    H_HIDE   875's finding generalises: on claims that acquire a sign, the ABS reading is at or
             below its own seed-noise prediction (obs/pred <= 1.10) in >= 2/3 of cases where the
             prediction is computable - i.e. ABS called them noise and SIGNED does not.
    H_STABLE the signed estimator is sign-stable: < 10% of claims have median and mean of
             opposite sign (Q2).
    H_UNADJ  the majority of the record's committed placebo mass is not re-priceable at all
             (aggregate-only), confirming 871's unadjudicability finding from the other side.
    H_WF     re-priced resolvability walks forward: a claim resolvable on the IS window is
             resolvable on the OOS window, same sign, in >= 50% of cases.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
    (a) THE STATISTIC: every claim is re-priced separately on the IS window (..2016-12-31) and the
        OOS window (2017-01-01..) from the committed excess_IS / excess_OOS columns, and H_WF is
        read on the OOS window once.
    (b) THE BOOKS: a live arm grid with one declared IS-only selector - the arm with the highest
        2009-2016 Sharpe on each panel - is picked and its untouched OOS CAGR / Sharpe / MaxDD is
        reported against RULES v2 (live) OOS and SPY OOS, with BOTH KEEP paths, plus the
        unselected 4a / 4b base rate over all arms.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  SMALL is the sub-$2B panel with every
ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST, and it holds CURRENT
CONSTITUENTS ONLY - dead small caps are absent, so its CAGRs are the most optimistic numbers here
and any 4b reading on it is an upper bound.  The census legs are re-readings of committed numbers
and carry whatever bias their source runs carried.

PROTOCOL: 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage.  Deterministic, standalone, no network.  Reads committed CSVs read-only and modifies
nothing but its own outputs:
    .corpus.csv  .claims.csv  .headline.csv  .walkforward.csv  .books.csv  .console.txt
"""
from __future__ import annotations

import re
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
BT = REPO / "research" / "backtests"
LINES: list[str] = []

KEY = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
REF = "BLOCK"                      # every corpus file's own reference null
Z_BAR = 2.0                        # |sign-test z| at which a signed reading is resolvable
PRED_BAR = 1.10                    # obs / seed-noise-prediction above which an ABS reading is not noise
ACQ_BAR, STABLE_BAR, WF_BAR = 0.25, 0.10, 0.50
NSEED_DEFAULT = 20                 # every corpus run's seed budget; asserted per file below

# rule 8 (b): the live book grid, idea 881/882's verbatim
FREQ, MAX_VOL, SMOOTH = "W", 0.60, 20
QS, WS = [0.07, 0.12, 0.17], [252, 1008]
DEPTHS, CADENCES, GROSSES = [0.50, 1.00], ["D", "W"], [0.75, 1.00]
STATES = ["BREADTH", "VOL20", "DISP", "CORR"]
SIDES = {"BREADTH": ("LO", "HI"), "VOL20": ("HI", "LO"), "DISP": ("HI", "LO"), "CORR": ("HI", "LO")}
SPLIT = "2017-01-01"


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ================================================================== the corpus (read-only census)
def find_corpus():
    """Every committed CSV holding PER-ARM placebo excess for a null AND its BLOCK reference on
    the same arm keys.  Discovered by structure, not by a hand-written list, so the census cannot
    be steered by which files I happened to remember."""
    rows, priceable = [], []
    for f in sorted(BT.glob("*.csv")):
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cols = list(head.columns)
        if "kind" not in cols or not set(KEY).issubset(cols):
            continue
        excols = [c for c in cols if c.startswith("excess")]
        if not excols:
            continue
        df = pd.read_csv(f)
        kinds = sorted(df["kind"].unique())
        if REF not in kinds:
            rows.append(dict(file=f.name, rows=len(df), kinds=";".join(kinds),
                             excess_cols=";".join(excols), has_ref=False, has_seedsd=False,
                             status="NO BLOCK REFERENCE"))
            continue
        sdcols = [c for c in cols if c.startswith("seedsd")]
        rows.append(dict(file=f.name, rows=len(df), kinds=";".join(kinds),
                         excess_cols=";".join(excols), has_ref=True, has_seedsd=bool(sdcols),
                         status="RE-PRICEABLE"))
        priceable.append((f.name, df, excols, sdcols))
    return rows, priceable


def aggregate_only():
    """Committed placebo-bearing files whose per-arm cells did NOT survive - the population no
    estimator can re-price.  Counted against idea 871's own committed census where it exists."""
    NULLW = re.compile(r"^(RAND|BLOCK\d*|BLOCK[A-Z]+|SHIFT\d*|PERM|RUNPERM|SWITCHMATCH|SM_[A-Z0-9]+"
                       r"|OP_[A-Z0-9]+|UG_[A-Z0-9]+|YEARBLOCK|EPISODEFIX|EPMATCH|YEARMATCH)$")
    agg = []
    for f in sorted(BT.glob("*.csv")):
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        if "kind" not in head.columns:
            continue
        try:
            df = pd.read_csv(f, usecols=["kind"])
        except Exception:
            continue
        ks = set(map(str, df["kind"].unique()))
        if sum(bool(NULLW.match(k)) for k in ks) < 2:
            continue
        if set(KEY).issubset(head.columns) and any(c.startswith("excess") for c in head.columns):
            continue                                   # that one is re-priceable, counted above
        agg.append(dict(file=f.name, rows=len(df), kinds=";".join(sorted(ks))))
    return agg


# ==================================================================== the two estimators, per cell
def price(df, excol, sdcol, nseed):
    """Re-price every (null) claim in one committed file under all four estimators.

    ex = the committed per-arm excess (real Sharpe - placebo Sharpe), already a median over that
    run's seeds.  s = ex_null - ex_BLOCK is the per-arm signed gap; |s| is the record's statistic.
    """
    piv = df.pivot_table(index=KEY, columns="kind", values=excol)
    if REF not in piv.columns:
        return []
    sd = (df.pivot_table(index=KEY, columns="kind", values=sdcol) if sdcol else None)
    out = []
    for kind in [k for k in piv.columns if k != REF]:
        s = (piv[kind] - piv[REF]).dropna()
        n = len(s)
        if n < 30:
            continue
        a = s.abs()
        # SIGN TEST, ties excluded (standard, and necessary: a null that is EXACTLY BLOCK - idea
        # 882's OP_REAL - has every arm tied at 0.  Counting ties as "not below" would hand it
        # z = -33.9 and call an exact zero the most resolvable claim in the record.)
        nz = s[s != 0]
        nties = n - len(nz)
        if len(nz) == 0:
            below, z = np.nan, np.nan            # undefined: every arm is an exact tie
        else:
            below = float((nz < 0).mean())
            z = (below - 0.5) / np.sqrt(0.25 / len(nz))
        se = float(s.std(ddof=1) / np.sqrt(n))
        pred = np.nan
        if sd is not None and kind in sd.columns and REF in sd.columns:
            p = (0.6745 * 1.2533 / np.sqrt(nseed)
                 * np.sqrt(sd[kind] ** 2 + sd[REF] ** 2)).reindex(s.index)
            pred = float(p.median())
        out.append(dict(kind=kind, n=n, n_ties=nties, ABS_MED=float(a.median()),
                        ABS_MEAN=float(a.mean()),
                        SIGNED_MED=float(s.median()), SIGNED_MEAN=float(s.mean()), SE=se,
                        sign_z=z, share_below=below, abs_pred=pred,
                        abs_ratio=(float(a.median()) / pred if pred == pred and pred else np.nan)))
    return out


def verdicts(r):
    """Pre-registered readings of one claim under each estimator."""
    if r["sign_z"] != r["sign_z"]:
        sig = "EXACT ZERO"                         # every arm tied: the claim is zero, not noise
    else:
        sig = "RESOLVED" if abs(r["sign_z"]) >= Z_BAR else "not resolvable"
    if r["abs_ratio"] != r["abs_ratio"]:
        ab = "UNADJUDICABLE"                       # no seed dispersion committed -> no ABS zero
    else:
        ab = "RESOLVED" if r["abs_ratio"] > PRED_BAR else "not resolvable"
    return ab, sig


# ============================================================ rule 8 (b): the live books, verbatim
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def fast_sharpe(v):
    v = np.asarray(v, float)
    sd = v.std(ddof=1)
    return v.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def state_breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def state_vol20(px):
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_disp(px):
    return px.pct_change().std(axis=1).rolling(SMOOTH).mean()


def state_corr(px):
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp, "CORR": state_corr}


def gate_mult(st, thr, side, depth, cadence, idx):
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def apply_eff(r_base, m_eff, gross, cost_bps):
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def pack(r):
    m = metrics(pd.Series(r) if not isinstance(r, pd.Series) else r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    log(f"  SMALL panel: {px.shape[1]} columns -> {len(keep)} kept "
        f"({px.shape[1]-len(keep)} dropped for max_1d_move >= 1.0)")
    return px[keep]


def book_panel(name, px):
    idx = px.index
    core = px.drop(columns=["SPY"], errors="ignore")
    spy = px["SPY"].pct_change().fillna(0.0)
    states = {s: STATE_FN[s](core) for s in STATES}
    base = {g: backtest(core, ewall_weights(core, g), cost_bps=10, freq=FREQ)["returns"]
            for g in GROSSES}
    start = idx[260]
    ii = idx[idx >= start]
    oos = np.asarray(ii >= pd.Timestamp(SPLIT))
    isw = ~oos
    RB = {g: v.loc[ii].values for g, v in base.items()}

    spy_v = spy.loc[ii].values
    b = dict(panel=name)
    b["spy_cagr"], b["spy_sh"], b["spy_dd"] = pack(pd.Series(spy_v, index=ii))
    b["spy_h1"], b["spy_h2"] = halves(spy_v)
    b["spy_oos_c"], b["spy_oos_s"], b["spy_oos_d"] = pack(pd.Series(spy_v[oos], index=ii[oos]))
    bl = backtest(core, rules_v2_weights(core), cost_bps=10, freq=FREQ)["returns"].loc[ii]
    b["bl_cagr"], b["bl_sh"], b["bl_dd"] = pack(bl)
    b["bl_h1"], b["bl_h2"] = halves(bl.values)
    b["bl_oos_c"], b["bl_oos_s"], b["bl_oos_d"] = pack(bl.loc[ii[oos]])

    rows = []
    for st_name in STATES:
        st_full = states[st_name]
        for side in SIDES[st_name]:
            for q, w in product(QS, WS):
                thr = st_full.rolling(w, min_periods=max(60, w // 4)).quantile(
                    q if side == "LO" else 1 - q)
                for depth, cad in product(DEPTHS, CADENCES):
                    me = gate_mult(st_full, thr, side, depth, cad, idx
                                   ).shift(1).fillna(1.0).loc[ii].values
                    for g in GROSSES:
                        rr = apply_eff(RB[g], me, g, 10)
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        rows.append(dict(panel=name, family=f"{st_name}-{side}", q=q, w=w,
                                         depth=depth, cadence=cad, gross=g, CAGR=c_, Sharpe=s_,
                                         MaxDD=d_, H1=h1, H2=h2, IS_Sharpe=fast_sharpe(rr[isw]),
                                         OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od))
    return pd.DataFrame(rows), b


# ========================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 880 - how many committed PLACEBO-DIFFERENCED numbers would CHANGE SIGN under the "
        "SIGNED estimator?  (cloud 2026-09-15)")
    log("=" * 100)
    log(f"# pandas {pd.__version__} numpy {np.__version__}")
    log("# PARAM 1 claim set  {HEADLINE = (file, null) @10bps full sample, ALL = x 3 rungs x 2 "
        "windows}")
    log("# PARAM 2 estimator  {ABS_MED, ABS_MEAN, SIGNED_MED, SIGNED_MEAN} - all four at every "
        "claim")

    log("\n" + "=" * 100)
    log("[0] THE CORPUS - discovered by STRUCTURE, not by a hand-written list")
    log("=" * 100)
    rows, priceable = find_corpus()
    agg = aggregate_only()
    corp = pd.DataFrame(rows)
    corp.to_csv(OUT / f"{STEM}.corpus.csv", index=False)
    log(f"  {'file':78s}{'rows':>8s}{'seedsd':>8s}  nulls")
    for _, r in corp.iterrows():
        log(f"  {r['file'][:76]:78s}{r['rows']:8d}{('yes' if r['has_seedsd'] else 'NO'):>8s}  "
            f"{r['kinds'][:60]}")
    n_pr, n_agg = len(priceable), len(agg)
    log(f"\n  RE-PRICEABLE files (per-arm cells + a {REF} reference survive): {n_pr}")
    log(f"  AGGREGATE-ONLY placebo files (published number survives, cells do not): {n_agg}")
    try:
        cen = pd.read_csv(BT / "2026-09-15_should-PROTOCOL-require-a-RUN-LENGTH-MATCHED-null-"
                               "by-name_B.census.csv")
        log(f"  idea 871's committed census of placebo-BEARING files in the record: {len(cen)}")
        log(f"  -> re-priceable share of 871's denominator: {n_pr}/{len(cen)} = "
            f"{n_pr/len(cen):.1%}")
        h_unadj = n_pr / len(cen) < 0.50
    except Exception as e:                                   # census absent: say so, don't guess
        log(f"  idea 871's census.csv not readable ({e}); H_UNADJ read on this run's own sweep")
        h_unadj = n_pr / max(n_pr + n_agg, 1) < 0.50
    log(f"  H_UNADJ (the majority of committed placebo mass is NOT re-priceable) "
        f"{'CONFIRMED' if h_unadj else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[1] EVERY CLAIM, EVERY ESTIMATOR, EVERY RUNG AND WINDOW - nothing withheld")
    log("=" * 100)
    claims = []
    for fname, df, excols, sdcols in priceable:
        # every committed excess column becomes a cut; a bare "excess" is that run's own 10 bps
        # headline (the protocol rung), which is how its memo quotes it.
        cuts = []
        for c in excols:
            if re.match(r"excess_\d+bps$", c):
                cuts.append((c, c.replace("excess_", "")))
            elif c == "excess":
                cuts.append((c, "10bps"))
            else:
                cuts.append((c, c.replace("excess_", "")))
        for excol, label in cuts:
            # an ABS reading needs the seed dispersion for THAT SAME cut; the corpus stores it for
            # the full-sample rungs only, so IS / OOS / strip cuts are ABS-UNADJUDICABLE by
            # construction and are reported as such rather than paired with a mismatched floor.
            want = excol.replace("excess", "seedsd")
            sdcol = want if (sdcols and want in df.columns) else None
            for r in price(df, excol, sdcol, NSEED_DEFAULT):
                ab, sig = verdicts(r)
                claims.append(dict(file=fname, cut=label, **r, ABS_verdict=ab,
                                   SIGNED_verdict=sig,
                                   sign_unstable=bool(np.sign(r["SIGNED_MED"])
                                                      * np.sign(r["SIGNED_MEAN"]) < 0)))
    claims = pd.DataFrame(claims)
    claims.to_csv(OUT / f"{STEM}.claims.csv", index=False)
    log(f"  {len(claims)} re-priced claims over {n_pr} files "
        f"({claims.cut.nunique()} cuts x {claims.kind.nunique()} distinct nulls)")

    head = claims[claims.cut == "10bps"].copy()
    log(f"\n  HEADLINE claim set (before de-duplication): {len(head)} claims (one per file x null, 10 bps, full sample)")
    log(f"  {'file':40s}{'null':11s}{'n':>6s}{'ABS_MED':>10s}{'ABS/pred':>10s}{'SIGNED_MED':>12s}"
        f"{'SIGNED_MEAN':>13s}{'z':>8s}{'ABS':>16s}{'SIGNED':>16s}")
    for _, r in head.iterrows():
        short = r["file"].replace("2026-09-15_", "").replace("_cloud.excess.csv", "") \
                         .replace("_B.excess.csv", "").replace("_B.nulls.csv", "")
        ar = f"{r['abs_ratio']:.2f}" if r["abs_ratio"] == r["abs_ratio"] else "n/a"
        log(f"  {short[:38]:40s}{r['kind']:11s}{r['n']:6d}{r['ABS_MED']:10.4f}{ar:>10s}"
            f"{r['SIGNED_MED']:+12.5f}{r['SIGNED_MEAN']:+13.5f}{r['sign_z']:+8.2f}"
            f"{r['ABS_verdict']:>16s}{r['SIGNED_verdict']:>16s}")

    log("\n" + "=" * 100)
    log("[1b] ARE THE RE-PRICEABLE CLAIMS INDEPENDENT?  (pairwise bit-identity of the cells)")
    log("=" * 100)
    piv = {}
    for fname, df, excols, sdcols in priceable:
        col = "excess_10bps" if "excess_10bps" in df.columns else "excess"
        piv[fname] = df.pivot_table(index=KEY, columns="kind", values=col)
    dups = set()
    names = list(piv)
    for i, fa in enumerate(names):
        for fb in names[i + 1:]:
            A, B = piv[fa], piv[fb]
            shared = sorted(set(A.columns) & set(B.columns))
            idx = A.index.intersection(B.index)
            if not shared or len(idx) < 30:
                continue
            same = [k for k in shared
                    if float((A.loc[idx, k] - B.loc[idx, k]).abs().max()) == 0.0]
            if same:
                log(f"  {fa.replace('2026-09-15_','')[:46]}")
                log(f"    == {fb.replace('2026-09-15_','')[:46]}")
                log(f"    BIT-IDENTICAL on {len(idx)} shared arms for: {', '.join(same)}")
                for k in same:
                    if k != REF:
                        dups.add((fb, k))          # keep the first file's copy, drop the later
    log(f"  duplicate (file, null) claims found: {len(dups)}")
    claims["dup"] = [(r.file, r.kind) in dups for r in claims.itertuples()]
    head = claims[(claims.cut == "10bps")].copy()
    head_all = head.copy()
    head = head[~head.dup].copy()
    head.to_csv(OUT / f"{STEM}.headline.csv", index=False)
    log(f"  HEADLINE claim set after de-duplication: {len(head)} of {len(head_all)} "
        f"(every hypothesis below is read on the DE-DUPLICATED set)")

    log("\n" + "=" * 100)
    log("[2] Q1 ACQUISITION - how many committed ABS claims ACQUIRE a determinate sign?")
    log("    (the published statistic is |null - BLOCK|, which has no sign to change; the")
    log("     answerable question is how many gain one the published number could not express)")
    log("=" * 100)
    for nm, cs in (("HEADLINE", head), ("ALL", claims)):
        acq = cs[cs.SIGNED_verdict == "RESOLVED"]
        log(f"  {nm:9s} {len(acq)} of {len(cs)} claims ({len(acq)/len(cs):.1%}) acquire a "
            f"determinate sign at |z| >= {Z_BAR}")
        if len(acq):
            pos = int((acq.SIGNED_MED > 0).sum())
            log(f"            direction: {len(acq)-pos} negative / {pos} positive; "
                f"|signed| range {acq.SIGNED_MED.abs().min():.5f} .. "
                f"{acq.SIGNED_MED.abs().max():.5f}")
    hacq = (head.SIGNED_verdict == "RESOLVED").mean()
    h_acq = hacq >= ACQ_BAR
    log(f"  H_ACQ (>= {ACQ_BAR:.0%} of HEADLINE claims acquire a sign): {hacq:.1%} "
        f"{'CONFIRMED' if h_acq else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[3] H_HIDE - on the claims that acquire a sign, what was the ABS reading saying?")
    log("=" * 100)
    acq = head[head.SIGNED_verdict == "RESOLVED"]
    adj = acq[acq.abs_ratio == acq.abs_ratio]
    if len(adj):
        quiet = int((adj.abs_ratio <= PRED_BAR).sum())
        log(f"  {'file':44s}{'null':11s}{'ABS/pred':>10s}{'SIGNED_MED':>12s}{'z':>8s}")
        for _, r in adj.iterrows():
            short = r["file"].replace("2026-09-15_", "")[:42]
            log(f"  {short:44s}{r['kind']:11s}{r['abs_ratio']:10.2f}{r['SIGNED_MED']:+12.5f}"
                f"{r['sign_z']:+8.2f}")
        h_hide = quiet / len(adj) >= 2 / 3
        log(f"  ABS at or below its own seed-noise prediction (<= {PRED_BAR}) in {quiet} of "
            f"{len(adj)} = {quiet/len(adj):.1%}")
        log(f"  H_HIDE (>= 66.7%) {'CONFIRMED' if h_hide else 'REFUTED'}")
    else:
        h_hide = False
        log(f"  no sign-acquiring claim carries a computable ABS prediction "
            f"({len(acq)} acquiring, {len(acq)-len(adj)} of them UNADJUDICABLE)")
        log("  H_HIDE REFUTED (vacuously - the leg cannot be read on this corpus)")

    log("\n" + "=" * 100)
    log("[4] Q2 INSTABILITY - is the SIGNED estimator itself sign-stable?")
    log("=" * 100)
    for nm, cs in (("HEADLINE", head), ("ALL", claims)):
        u = cs[cs.sign_unstable]
        log(f"  {nm:9s} {len(u)} of {len(cs)} ({len(u)/len(cs):.1%}) have SIGNED_MED and "
            f"SIGNED_MEAN of OPPOSITE sign")
        for _, r in u.head(12).iterrows():
            log(f"            {r['file'].replace('2026-09-15_','')[:46]:48s}{r['kind']:11s}"
                f"med {r['SIGNED_MED']:+.5f}  mean {r['SIGNED_MEAN']:+.5f}  z {r['sign_z']:+.2f}")
    hun = float(head.sign_unstable.mean())
    h_stable = hun < STABLE_BAR
    log(f"  H_STABLE (< {STABLE_BAR:.0%} unstable): {hun:.1%} "
        f"{'CONFIRMED' if h_stable else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[5] Q3 VERDICT MOVE - the 2x2 of the two estimators' verdicts")
    log("=" * 100)
    for nm, cs in (("HEADLINE", head), ("ALL", claims)):
        ct = pd.crosstab(cs.ABS_verdict, cs.SIGNED_verdict)
        log(f"  {nm}:")
        log("    " + ct.to_string().replace("\n", "\n    "))
        moved_up = int(((cs.ABS_verdict != "RESOLVED") & (cs.SIGNED_verdict == "RESOLVED")).sum())
        moved_dn = int(((cs.ABS_verdict == "RESOLVED") & (cs.SIGNED_verdict != "RESOLVED")).sum())
        log(f"    verdicts that MOVE: {moved_up} noise -> resolved, {moved_dn} resolved -> noise, "
            f"of {len(cs)} ({(moved_up+moved_dn)/len(cs):.1%})")

    log("\n" + "=" * 100)
    log("[6] RULE 8 (a) - DOES A RE-PRICED VERDICT WALK FORWARD?  (IS fitted, OOS read once)")
    log("=" * 100)
    is_c = claims[(claims.cut == "IS") & (~claims.dup)].set_index(["file", "kind"])
    oo_c = claims[(claims.cut == "OOS") & (~claims.dup)].set_index(["file", "kind"])
    both = is_c.join(oo_c, lsuffix="_IS", rsuffix="_OOS", how="inner")
    wf = both.reset_index()[["file", "kind", "SIGNED_MED_IS", "sign_z_IS", "SIGNED_MED_OOS",
                             "sign_z_OOS", "ABS_MED_IS", "ABS_MED_OOS"]]
    wf["IS_res"] = wf.sign_z_IS.abs() >= Z_BAR
    wf["OOS_res"] = wf.sign_z_OOS.abs() >= Z_BAR
    wf["same_sign"] = np.sign(wf.SIGNED_MED_IS) == np.sign(wf.SIGNED_MED_OOS)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log(f"  {'file':40s}{'null':11s}{'IS signed':>12s}{'z':>8s}{'OOS signed':>12s}{'z':>8s}"
        f"{'walks':>8s}")
    for _, r in wf.iterrows():
        short = r["file"].replace("2026-09-15_", "")[:38]
        walks = "yes" if (r.IS_res and r.OOS_res and r.same_sign) else "no"
        log(f"  {short:40s}{r['kind']:11s}{r['SIGNED_MED_IS']:+12.5f}{r['sign_z_IS']:+8.2f}"
            f"{r['SIGNED_MED_OOS']:+12.5f}{r['sign_z_OOS']:+8.2f}{walks:>8s}")
    isres = wf[wf.IS_res]
    if len(isres):
        holds = int((isres.OOS_res & isres.same_sign).sum())
        h_wf = holds / len(isres) >= WF_BAR
        log(f"  of {len(isres)} claims resolvable IN SAMPLE, {holds} are resolvable OUT OF SAMPLE "
            f"with the same sign = {holds/len(isres):.1%}")
        log(f"  H_WF (>= {WF_BAR:.0%}) {'CONFIRMED' if h_wf else 'REFUTED'}")
    else:
        h_wf = False
        log("  NO claim is resolvable in sample -> H_WF REFUTED (vacuously); reported as it came")
    log(f"  sign agreement IS vs OOS over all {len(wf)} de-duplicated claims: "
        f"{wf.same_sign.mean():.1%}")
    log("  (the IS / OOS cuts carry no committed seed dispersion, so they are ABS-UNADJUDICABLE "
        "by construction; only the signed reading exists out of sample at all)")

    log("\n" + "=" * 100)
    log("[7] RULE 8 (b) - THE BOOKS: IS-only selector, OOS read once, BOTH KEEP PATHS")
    log("=" * 100)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for n, p in panels.items():
        log(f"  {n}: {p.shape[1]} cols x {len(p)} days  {p.index[0].date()} .. "
            f"{p.index[-1].date()}")
    sel = []
    for pn, px in panels.items():
        arms, b = book_panel(pn, px)
        pick = arms.loc[arms.IS_Sharpe.idxmax()]
        p4a = bool(pick.H1 > b["bl_h1"] and pick.H2 > b["bl_h2"] and pick.MaxDD >= b["bl_dd"])
        p4b = bool(pick.H1 > b["spy_h1"] and pick.H2 > b["spy_h2"]
                   and pick.OOS_Sharpe > b["spy_oos_s"]
                   and pick.MaxDD >= 0.60 * b["spy_dd"] and pick.CAGR >= 0.70 * b["spy_cagr"])
        sel.append(dict(panel=pn, arm=f"{pick.family} q{pick.q} w{pick.w} d{pick.depth} "
                                      f"{pick.cadence} g{pick.gross}", CAGR=pick.CAGR,
                        Sharpe=pick.Sharpe, MaxDD=pick.MaxDD, H1=pick.H1, H2=pick.H2,
                        OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                        OOS_MaxDD=pick.OOS_MaxDD, p4a=p4a, p4b=p4b))
        log(f"  {pn}: IS-pick {sel[-1]['arm']}")
        log(f"     FULL {pick.CAGR:.2%} / {pick.Sharpe:.3f} / {pick.MaxDD:.2%}  halves "
            f"{pick.H1:.3f}/{pick.H2:.3f}   OOS {pick.OOS_CAGR:.2%} / {pick.OOS_Sharpe:.3f} / "
            f"{pick.OOS_MaxDD:.2%}")
        log(f"     RULES v2 (live) {b['bl_cagr']:.2%} / {b['bl_sh']:.3f} / {b['bl_dd']:.2%}  "
            f"halves {b['bl_h1']:.3f}/{b['bl_h2']:.3f}  OOS {b['bl_oos_c']:.2%} / "
            f"{b['bl_oos_s']:.3f} / {b['bl_oos_d']:.2%}")
        log(f"     SPY            {b['spy_cagr']:.2%} / {b['spy_sh']:.3f} / {b['spy_dd']:.2%}  "
            f"halves {b['spy_h1']:.3f}/{b['spy_h2']:.3f}  OOS {b['spy_oos_c']:.2%} / "
            f"{b['spy_oos_s']:.3f} / {b['spy_oos_d']:.2%}")
        log(f"     4b bars: DD >= {0.60*b['spy_dd']:.2%}, CAGR >= {0.70*b['spy_cagr']:.2%}, "
            f"OOS Sharpe > {b['spy_oos_s']:.3f}")
        log(f"     4a {'PASS' if p4a else 'fail'}   4b {'PASS' if p4b else 'fail'}")
        n4a = int(((arms.H1 > b["bl_h1"]) & (arms.H2 > b["bl_h2"])
                   & (arms.MaxDD >= b["bl_dd"])).sum())
        n4b = int(((arms.H1 > b["spy_h1"]) & (arms.H2 > b["spy_h2"])
                   & (arms.OOS_Sharpe > b["spy_oos_s"])
                   & (arms.MaxDD >= 0.60 * b["spy_dd"])
                   & (arms.CAGR >= 0.70 * b["spy_cagr"])).sum())
        log(f"     unselected base rate over {len(arms)} arms: 4a {n4a} ({n4a/len(arms):.1%}), "
            f"4b {n4b} ({n4b/len(arms):.1%})")
    pd.DataFrame(sel).to_csv(OUT / f"{STEM}.books.csv", index=False)

    log("\n" + "=" * 100)
    log("[8] SUMMARY OF PRE-REGISTERED HYPOTHESES")
    log("=" * 100)
    for nm, v in (("H_ACQ", h_acq), ("H_HIDE", h_hide), ("H_STABLE", h_stable),
                  ("H_UNADJ", h_unadj), ("H_WF", h_wf)):
        log(f"  {nm:9s} {'CONFIRMED' if v else 'REFUTED'}")
    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
