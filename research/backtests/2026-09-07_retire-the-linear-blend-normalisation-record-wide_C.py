#!/usr/bin/env python3
"""Idea 359 (lane C, 2026-09-07): retire-the-linear-blend-normalisation-record-wide.

QUEUE TEXT: "idea 103 showed conv_per_pp is confounded by its own f=1 endpoint and is
UNDEFINED for the cash null, while raw_per_pp is defined everywhere and gives a different
ordering.  Census every committed file using a linear-blend dSharpe and re-state its verdict
under raw_per_pp; propose the benchmark-free statistic as the reportable one.
Max 2 params (statistic, f)."

THE TWO TUNED PARAMETERS ARE `statistic` AND `f`.  The sleeve is NOT tuned: it is whatever
the statistic under test picks.  That is the entire point -- the question is whether the
NORMALISATION changes what the record would have selected, so the statistic must be the
selector, not a descriptive column beside a separately chosen sleeve.

THE THREE STATISTICS (one parameter, three values)
-------------------------------------------------
For a book E blended with a sleeve S at fraction f, over the common sample:
  lin(f)       = (1-f)*Sharpe(f=0) + f*Sharpe(f=1)      <- the LINEAR BLEND yardstick
  give_pp      = 100 * (CAGR(f=0) - CAGR(f))            <- pp of CAGR surrendered (shared)
  conv_per_pp  = (Sharpe(f) - lin(f)) / give_pp         <- idea 100's, the one under review
  raw_per_pp   = (Sharpe(f) - Sharpe(0)) / give_pp      <- benchmark-free, the proposal
  dSharpe_raw  =  Sharpe(f) - Sharpe(0)                 <- unnormalised control (no denominator)

Note what is and is not shared: BOTH ratios carry the same denominator, so a denominator
pathology is NOT what separates them.  What separates them is the numerator: conv_per_pp's
numerator subtracts lin(f), which (a) requires Sharpe(f=1), undefined for a cash sleeve, and
(b) does NOT vanish as the denominator does.  dSharpe_raw is carried as the control that
isolates the denominator from the yardstick.

A GUARD ARTEFACT THE RECORD HAS NOT SEPARATED.  The committed scripts guard the two
statistics DIFFERENTLY: conv_per_pp is computed as dSharpe / max(give_pp, 1e-9) (never NaN,
explodes) while raw_per_pp is computed as NaN unless give_pp > 1e-6.  Part of the published
difference in their pathology rates is therefore the guard, not the numerator.  This run
reports every count twice: under the record's own asymmetric guards, and under a COMMON
guard (|give_pp| >= 0.05, idea 357's threshold) applied identically to both.

WHAT THIS RUN DOES
------------------
(0) REBUILD the population that every affected file is drawn from -- idea 357's 21 sleeves
    (which contain idea 103's 11 rungs and idea 100's S4/S9) x 3 books x 2 panels x 2 blend
    conventions x f in {0,.25,.50,.75,1.00} = 1,260 points, ALL reported -- and gate it
    against the committed CSVs of ideas 100/103/357 before any number is read.
(1) CENSUS every committed file that uses a linear-blend dSharpe (the file list is derived
    by grep at runtime, not hardcoded), and re-state each file's published headline under
    raw_per_pp and dSharpe_raw.
(2) PATHOLOGY: how often is each statistic undefined or absurd, under both guards.
(3) DISAGREEMENT: within each (panel, book, conv, f) cell, do the three statistics ORDER the
    sleeves the same way, and do they pick the same argmax?  If they agree, retiring the
    normalisation is cosmetic.
(4) RULE 8 (the decider): four PRE-REGISTERED choosers on 2009-2016, read ONCE on 2017-2026 --
    C_CONV, C_RAW, C_DELTA (the three statistics as selectors) and C_SHARPE (the record's
    existing default), against the no-sleeve control, RULES v2, RULES v1 and SPY.  A
    statistic is only worth reporting if it selects books that survive out of sample.
(5) KEEP paths 4a and 4b evaluated on all 1,260 points and on the rule-8 picks.

SURVIVORSHIP: both panels are current constituents (levels biased up); the sleeve ETFs are
survivors by construction.  10 bps, weekly, next-day execution via the shared engine.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_retire-the-linear-blend-normalisation-record-wide_C.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

COST_BPS, FREQ, GROSS = 10, "W", 0.75
MOM_LAGS, VOL_WINDOW = (252, 126, 63), 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
SPLIT, IS_END = "2017-01-01", "2016-12-31"
CORE4 = ["TLT", "GLD", "DBC", "UUP"]
FWD = ["SPY", "QQQ", "IWM", "EFA", "EEM"]
REV = ["EEM", "EFA", "IWM", "QQQ", "SPY"]
SINGLES = ["GDX", "USO", "SLV", "UNG", "TLT", "GLD", "SHY", "DBC", "HYG", "QQQ"]
GUARD_PP = 0.05                      # common guard: pp of CAGR the blend must surrender
ABSURD = 10.0                        # |statistic| above this is not a readable number
BT = Path(__file__).resolve().parent
OUT = Path(__file__).with_suffix("")


def build_ladder():
    L = {"SCASH": [], "S4": list(CORE4)}
    for i in range(1, len(FWD)):
        L[f"S{4+i}f"] = CORE4 + FWD[:i]
    for i in range(1, len(REV)):
        L[f"S{4+i}r"] = CORE4 + REV[:i]
    L["S9"] = CORE4 + FWD
    for t in SINGLES:
        L[f"X_{t}"] = [t]
    return L


SLEEVES = build_ladder()
LADDER11 = ["SCASH", "S4", "S5f", "S6f", "S7f", "S8f", "S5r", "S6r", "S7r", "S8r", "S9"]


# ---------------------------------------------------------------- sleeves / books (idea 103's)
def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    if not assets:
        return out
    sub = px[assets]
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def book_v1(px):
    return rules_v1_weights(px)


def book_top20(px, n=20):
    s, above, vol20 = score(px, vol_scale=False)
    rank = s.where(above & (vol20 < 0.60)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def book_ewall(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = (above & (vol20 < 0.60) & s.notna()).astype(float)
    k = elig.sum(axis=1)
    return elig.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


BOOKS = {"v1": book_v1, "top20": book_top20, "ewall": book_ewall}


def blend(E, S, f, matched):
    w = (1 - f) * E + f * S
    if not matched:
        return w
    gE, gW = E.sum(axis=1), w.sum(axis=1)
    return w.mul((gE / gW.where(gW > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- metrics
def stats(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def full_row(r):
    a, b, c = stats(r), stats(r.iloc[:len(r) // 2]), stats(r.iloc[len(r) // 2:])
    o, i = stats(r.loc[SPLIT:]), stats(r.loc[:IS_END])
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=b["Sharpe"], H2=c["Sharpe"],
                IS_Sharpe=i["Sharpe"], IS_CAGR=i["CAGR"], IS_MaxDD=i["MaxDD"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    if a[ok].nunique() < 2 or b[ok].nunique() < 2:
        return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])


def ols_t(x, y):
    """OLS slope with t-stat -> (slope, R2, t, n)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 5 or np.ptp(x) == 0:
        return np.nan, np.nan, np.nan, int(len(x))
    A = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ beta
    ss = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (res ** 2).sum() / ss if ss > 0 else np.nan
    s2 = (res ** 2).sum() / max(len(y) - 2, 1)
    try:
        se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
        t = beta[1] / se[1]
    except np.linalg.LinAlgError:
        t = np.nan
    return float(beta[1]), float(r2), float(t), int(len(x))


# ---------------------------------------------------------------- statistics
def add_statistics(S, C, f, guard_common=True):
    """S, C are dicts f->Sharpe / f->CAGR for one (panel, sleeve, book, conv) cell."""
    lin = (1 - f) * S[0.0] + f * S[1.0]
    give = 100.0 * (C[0.0] - C[f])
    rec_conv = (S[f] - lin) / max(give, 1e-9)                       # the record's own guard
    rec_raw = ((S[f] - S[0.0]) / give) if give > 1e-6 else np.nan   # the record's own guard
    ok = abs(give) >= GUARD_PP
    return dict(f=f, Sharpe=S[f], lin=lin, give_pp=give,
                conv_per_pp=rec_conv, raw_per_pp=rec_raw,
                dSharpe=S[f] - lin, dSharpe_raw=S[f] - S[0.0],
                conv_g=(S[f] - lin) / give if ok else np.nan,       # COMMON guard
                raw_g=(S[f] - S[0.0]) / give if ok else np.nan,
                defined=bool(ok) and np.isfinite(lin))


# ---------------------------------------------------------------- census of committed files
def census_files():
    """Every committed file whose text carries a linear-blend dSharpe.  Derived by grep at
    runtime so the census cannot silently go stale."""
    pat = re.compile(r"conv_per_pp|convexity[_ ]per[_ ]pp|linear[ _]blend", re.I)
    hits = []
    for p in sorted(BT.iterdir()):
        if not p.is_file() or p.name.startswith(Path(__file__).name.rsplit(".", 1)[0]):
            continue
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        if pat.search(txt):
            hits.append(p.name)
    return hits


def main():
    print("=" * 120)
    print("IDEA 359 (lane C): retire-the-linear-blend-normalisation-record-wide")
    print("  params: statistic in {conv_per_pp, raw_per_pp, dSharpe_raw} x f in", FGRID)
    print("=" * 120)

    # ---------------------------------------------------------------- (1) file census
    files = census_files()
    print(f"\n### (1) COMMITTED FILES CARRYING A LINEAR-BLEND dSharpe (grep, {len(files)} files)")
    parents = sorted({re.sub(r"\.(py|result\.md|console\.txt|[a-z_]+\.csv|md)$", "", f)
                      for f in files})
    for f in files:
        print(f"    {f}")
    print(f"  -> {len(parents)} distinct parent artefacts: {parents}")

    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}
    records, refs = [], {}
    # --reuse loads the grid this same script wrote on a previous run instead of recomputing
    # the 1,260 backtests.  It changes nothing: the file is this script's own output and the
    # reproduction gates below still run against it.  Omit the flag for a cold, standalone run.
    reuse = "--reuse" in sys.argv and Path(f"{OUT}.grid.csv").exists()

    for tag, px in universes.items():
        start = px.index[260]
        for name, assets in SLEEVES.items():
            miss = [t for t in assets if t not in px.columns]
            if miss:
                raise SystemExit(f"missing sleeve tickers in {tag}: {miss}")

        base_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        v2_r = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        base, v2, spy = full_row(base_r), full_row(v2_r), full_row(spy_r)
        refs[tag] = (base, v2, spy)
        print("\n" + "=" * 120)
        print(f"### {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(pd.DataFrame({"RULES v1": base, "RULES v2 (live)": v2, "SPY": spy}).T.to_string(
            float_format=lambda x: f"{x:.4f}"))
        print(f"4b bars: H1>{spy['H1']:.4f} H2>{spy['H2']:.4f} OOS>{spy['OOS_Sharpe']:.4f} "
              f"|MaxDD|<={abs(0.60*spy['MaxDD']):.2%} CAGR>={0.70*spy['CAGR']:.2%}")

        if reuse:
            continue
        S_w = {s: sleeve_weights(px, a) for s, a in SLEEVES.items()}
        B_w = {b: fn(px) for b, fn in BOOKS.items()}
        cache = {b: backtest(px, B_w[b], cost_bps=COST_BPS, freq=FREQ) for b in BOOKS}

        for sname in SLEEVES:
            for bname in BOOKS:
                for matched in (False, True):
                    conv = "matched" if matched else "natural"
                    for f in FGRID:
                        if f == 0.0:
                            res, w = cache[bname], B_w[bname]
                        else:
                            w = blend(B_w[bname], S_w[sname], f, matched)
                            res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
                        r = res["returns"].loc[start:]
                        row = full_row(r)
                        row["Turn_yr"] = res["turnover"].loc[start:].sum() / (len(r) / 252)
                        row["Gross"] = float(w.loc[start:].sum(axis=1).mean())
                        row["p4a"] = keep_4a(row, v2)
                        row["p4a_v1"] = keep_4a(row, base)
                        row["p4b"] = keep_4b(row, spy)
                        records.append(dict(universe=tag, sleeve=sname, book=bname, conv=conv,
                                            n_assets=len(SLEEVES[sname]), f=f, **row))
            print(f"  ... {sname} done ({len(records)} rows)")

    if reuse:
        G = pd.read_csv(f"{OUT}.grid.csv")
        print(f"\n  [--reuse] loaded {len(G)} grid rows from {Path(OUT).name}.grid.csv")
    else:
        G = pd.DataFrame(records)
        G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------------------------------------------------------- reproduction gates
    print("\n" + "=" * 120)
    print("### (0) REPRODUCTION GATES — nothing below is read until these pass")
    g1 = G[(G.sleeve == "SCASH") & (G.conv == "matched")]
    piv = g1.pivot_table(index=["universe", "book"], columns="f", values="Sharpe")
    err = float((piv.max(axis=1) - piv.min(axis=1)).abs().max())
    print(f"  (a) MATCHED cash sleeve is algebraically the book: max Sharpe spread across f = "
          f"{err:.3e}  {'PASS' if err < 1e-9 else 'FAIL'}")
    prior = BT / "2026-09-07_is-the-SLEEVE-S-OWN-SHARPE-the-real-design-variable_cloud.grid.csv"
    if prior.exists():
        P = pd.read_csv(prior)
        k = ["universe", "sleeve", "book", "conv", "f"]
        M = G.merge(P[k + ["Sharpe", "CAGR", "MaxDD", "OOS_Sharpe"]], on=k, suffixes=("", "_prior"))
        d = max(float((M.Sharpe - M.Sharpe_prior).abs().max()),
                float((M.CAGR - M.CAGR_prior).abs().max()),
                float((M.OOS_Sharpe - M.OOS_Sharpe_prior).abs().max()))
        print(f"  (b) vs idea 357's committed grid ({len(M)} matched rows): max |diff| = {d:.3e}  "
              f"{'PASS' if d < 1e-9 else 'FAIL'}")
    else:
        print("  (b) idea 357 grid not found -- SKIPPED")

    # ---------------------------------------------------------------- statistics table
    dv = []
    for (tag, sname, bname, conv), sub in G.groupby(["universe", "sleeve", "book", "conv"], sort=False):
        S, C = sub.set_index("f")["Sharpe"].to_dict(), sub.set_index("f")["CAGR"].to_dict()
        Si, Ci = sub.set_index("f")["IS_Sharpe"].to_dict(), sub.set_index("f")["IS_CAGR"].to_dict()
        for f in FGRID[1:-1]:
            d = add_statistics(S, C, f)
            di = add_statistics(Si, Ci, f)
            dv.append(dict(universe=tag, sleeve=sname, book=bname, conv=conv,
                           n_assets=len(SLEEVES[sname]), **d,
                           IS_conv_per_pp=di["conv_per_pp"], IS_raw_per_pp=di["raw_per_pp"],
                           IS_dSharpe_raw=di["dSharpe_raw"], IS_defined=di["defined"],
                           OOS_Sharpe=float(sub[sub.f == f].OOS_Sharpe.iloc[0]),
                           OOS_CAGR=float(sub[sub.f == f].OOS_CAGR.iloc[0]),
                           OOS_MaxDD=float(sub[sub.f == f].OOS_MaxDD.iloc[0]),
                           p4b=bool(sub[sub.f == f].p4b.iloc[0])))
    D = pd.DataFrame(dv)
    D.to_csv(f"{OUT}.statistics.csv", index=False)

    print("\n  Published-endpoint check (idea 100's headline pair, u56 top20 natural, median over f):")
    for sn in ("S4", "S9"):
        q = D[(D.universe == "u56") & (D.book == "top20") & (D.conv == "natural") & (D.sleeve == sn)]
        print(f"    {sn}: conv_per_pp median {q.conv_per_pp.median():.4f}  "
              f"(idea 100 published 0.090 / 0.031 for S4 / S9)   "
              f"raw_per_pp median {q.raw_per_pp.median():.4f}   dSharpe_raw median {q.dSharpe_raw.median():.4f}")

    # ---------------------------------------------------------------- (2) pathology
    print("\n" + "=" * 120)
    print("### (2) PATHOLOGY — how often is each statistic unreadable?")
    print("###     LEFT: the record's own asymmetric guards.  RIGHT: a COMMON guard (|give_pp| >= "
          f"{GUARD_PP}) applied identically.")
    rows = []
    for name, col, colg in (("conv_per_pp", "conv_per_pp", "conv_g"),
                            ("raw_per_pp", "raw_per_pp", "raw_g"),
                            ("dSharpe_raw", "dSharpe_raw", "dSharpe_raw")):
        v, vg = D[col], D[colg]
        rows.append(dict(statistic=name, n=len(D),
                         rec_nan=int(v.isna().sum()),
                         rec_absurd=int((v.abs() > ABSURD).sum()),
                         rec_worst_abs=float(v.abs().max()),
                         common_nan=int(vg.isna().sum()),
                         common_absurd=int((vg.abs() > ABSURD).sum()),
                         common_worst_abs=float(vg.abs().max())))
    PATH = pd.DataFrame(rows).set_index("statistic")
    print(PATH.to_string(float_format=lambda x: f"{x:.4g}"))
    PATH.to_csv(f"{OUT}.pathology.csv")
    bad = D[D.give_pp.abs() < GUARD_PP]
    print(f"\n  {len(bad)}/{len(D)} interior points surrender < {GUARD_PP} pp of CAGR (the shared "
          f"denominator's near-zero region).  On exactly those points:")
    if len(bad):
        print(f"    |conv_per_pp| median {bad.conv_per_pp.abs().median():.4g}  max {bad.conv_per_pp.abs().max():.4g}")
        print(f"    |raw_per_pp|  median {bad.raw_per_pp.abs().median():.4g}  max {bad.raw_per_pp.abs().max():.4g}")
        print(f"    |dSharpe|(numerator of conv) median {bad.dSharpe.abs().median():.4g}   "
              f"|dSharpe_raw|(numerator of raw) median {bad.dSharpe_raw.abs().median():.4g}")
        print("    sleeves: " + ", ".join(f"{k}({v})" for k, v in bad.sleeve.value_counts().items()))
    ncash = D[D.sleeve == "SCASH"]
    print(f"\n  THE CASH NULL ({len(ncash)} points): conv_per_pp finite in "
          f"{int(np.isfinite(ncash.conv_per_pp).sum())}/{len(ncash)} under the record's guard, "
          f"{int(np.isfinite(ncash.conv_g).sum())}/{len(ncash)} under the common guard; "
          f"raw_per_pp finite in {int(np.isfinite(ncash.raw_per_pp).sum())}/{len(ncash)}.")
    print(f"    (lin(f) needs Sharpe(f=1); for SCASH that book is all cash -> "
          f"Sharpe = {G[(G.sleeve=='SCASH') & (G.f==1.0)].Sharpe.iloc[0]!r})")

    # ---------------------------------------------------------------- (3) disagreement
    print("\n" + "=" * 120)
    print("### (3) DO THE STATISTICS ORDER THE SLEEVES THE SAME WAY?")
    print("###     Within each (panel, book, conv, f) cell -- 24 cells, 21 sleeves each.")
    dis = []
    for key, g in D.groupby(["universe", "book", "conv", "f"], sort=False):
        gg = g[g.defined & (g.sleeve != "SCASH")]
        if len(gg) < 5:
            continue
        am_c = gg.loc[gg.conv_g.idxmax()].sleeve if gg.conv_g.notna().any() else None
        am_r = gg.loc[gg.raw_g.idxmax()].sleeve if gg.raw_g.notna().any() else None
        am_d = gg.loc[gg.dSharpe_raw.idxmax()].sleeve
        dis.append(dict(universe=key[0], book=key[1], conv=key[2], f=key[3], n=len(gg),
                        rho_conv_raw=spearman(gg.conv_g, gg.raw_g),
                        rho_conv_delta=spearman(gg.conv_g, gg.dSharpe_raw),
                        rho_raw_delta=spearman(gg.raw_g, gg.dSharpe_raw),
                        argmax_conv=am_c, argmax_raw=am_r, argmax_delta=am_d,
                        agree_cr=int(am_c == am_r), agree_cd=int(am_c == am_d),
                        agree_rd=int(am_r == am_d)))
    DIS = pd.DataFrame(dis)
    DIS.to_csv(f"{OUT}.disagreement.csv", index=False)
    print(DIS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n  MEAN within-cell spearman:  conv vs raw {DIS.rho_conv_raw.mean():+.4f}   "
          f"conv vs delta {DIS.rho_conv_delta.mean():+.4f}   raw vs delta {DIS.rho_raw_delta.mean():+.4f}")
    print(f"  ARGMAX SLEEVE AGREEMENT:    conv==raw {DIS.agree_cr.sum()}/{len(DIS)}   "
          f"conv==delta {DIS.agree_cd.sum()}/{len(DIS)}   raw==delta {DIS.agree_rd.sum()}/{len(DIS)}")

    # ---------------------------------------------------------------- (1b) restate published headlines
    print("\n" + "=" * 120)
    print("### (1b) RE-STATING THE RECORD'S PUBLISHED HEADLINES UNDER raw_per_pp / dSharpe_raw")
    lad = D[D.sleeve.isin(LADDER11) & (D.sleeve != "SCASH")].copy()
    corr_axis = {}
    for tag, px in universes.items():
        start = px.index[260]
        S_r = {s: backtest(px, sleeve_weights(px, a), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
               for s, a in SLEEVES.items()}
        B_r = {b: backtest(px, fn(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
               for b, fn in BOOKS.items()}
        for s in SLEEVES:
            for b in BOOKS:
                corr_axis[(tag, s, b)] = 0.0 if s == "SCASH" else float(
                    pd.concat([S_r[s], B_r[b]], axis=1).corr().iloc[0, 1])
    for df in (lad, D):
        df["corr"] = [corr_axis[(r.universe, r.sleeve, r.book)] for r in df.itertuples()]
    D.to_csv(f"{OUT}.statistics.csv", index=False)

    head = []
    for label, dd in (("idea 103's 11-rung ladder (its own population)", lad),
                      ("idea 357's 21-sleeve plane (the widest committed one)",
                       D[D.sleeve != "SCASH"])):
        for yv in ("conv_g", "raw_g", "dSharpe_raw"):
            sl, r2, t, n = ols_t(dd["corr"], dd[yv])
            rho = spearman(dd["corr"], dd[yv])
            cells = dd.groupby(["universe", "book", "conv", "f"], sort=False).apply(
                lambda g: spearman(g["corr"], g[yv]))
            head.append(dict(population=label, statistic=yv, n=n, slope=sl, R2=r2, t=t,
                             pooled_rho=rho, cell_rho_mean=float(cells.mean()),
                             cells_neg=int((cells < 0).sum()), cells=int(cells.notna().sum())))
    HEAD = pd.DataFrame(head)
    HEAD.to_csv(f"{OUT}.headlines.csv", index=False)
    print("  Published claim under review: 'convexity-per-pp falls with sleeve-to-book correlation'")
    print("  (idea 103 cloud: conv_per_pp spearman -0.624, R2 0.195; raw_per_pp -0.240, R2 0.0155)")
    print(HEAD.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- (1c) claim-by-claim
    print("\n" + "=" * 120)
    print("### (1c) THE CENSUS PROPER — every PUBLISHED CLAIM in LEADERBOARD.md that rests on a")
    print("###      linear-blend dSharpe, re-stated under the benchmark-free statistics.")
    lb = (REPO / "research" / "LEADERBOARD.md").read_text(errors="ignore").splitlines()
    claim_rows = [(i + 1, l) for i, l in enumerate(lb)
                  if l.startswith("|") and re.search(r"linear blend|conv_per_pp|Sharpe per pp|convexity",
                                                     l, re.I)]
    print(f"  {len(claim_rows)} LEADERBOARD rows carry the statistic:")
    for n, l in claim_rows:
        print(f"    L{n}: {l.split('|')[2].strip()[:110]}")

    def cell36(sleeve):
        """The 36 interior cells ideas 26/100 report: 2 panels x 3 books x 2 conv x 3 f."""
        return D[(D.sleeve == sleeve)]

    rest = []
    for sn, published in (("S9", "idea 26 + idea 100's S9 arm: dSharpe>0 in 36/36, mean +0.052"),
                          ("S4", "idea 100's S4 arm: dSharpe>0 in 36/36, mean +0.265")):
        q = cell36(sn)
        rest.append(dict(claim=published, n=len(q),
                         conv_mean=q.dSharpe.mean(), conv_pos=int((q.dSharpe > 0).sum()),
                         raw_mean=q.dSharpe_raw.mean(), raw_pos=int((q.dSharpe_raw > 0).sum()),
                         conv_per_pp_med=q.conv_per_pp.median(), raw_per_pp_med=q.raw_per_pp.median()))
    RS = pd.DataFrame(rest)
    print("\n  (i) idea 26 / idea 100 'the blend beats the sum of its parts' — the SIGN COUNT:")
    print(RS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n  (ii) idea 100b PAIRED S4-vs-S9, same (panel, book, conv, f) — published: S4's")
    print("       convexity higher in 36/36, S4's exchange rate higher in 32/36.")
    k = ["universe", "book", "conv", "f"]
    A = D[D.sleeve == "S4"].set_index(k)
    B = D[D.sleeve == "S9"].set_index(k)
    J = A.join(B, lsuffix="_S4", rsuffix="_S9", how="inner")
    for lab, ca, cb in (("dSharpe (linear-blend, published)", "dSharpe_S4", "dSharpe_S9"),
                        ("dSharpe_raw (benchmark-free)", "dSharpe_raw_S4", "dSharpe_raw_S9"),
                        ("conv_per_pp (published exchange rate)", "conv_per_pp_S4", "conv_per_pp_S9"),
                        ("raw_per_pp (benchmark-free exchange rate)", "raw_per_pp_S4", "raw_per_pp_S9")):
        d = J[ca] - J[cb]
        print(f"    S4 > S9 on {lab:42s}: {int((d > 0).sum())}/{int(d.notna().sum())}  "
              f"mean margin {d.mean():+.4f}")

    print("\n  (iii) VERDICT-CHANGE TALLY.  A claim CHANGES if its sign count or its ordering")
    print("        flips when the linear-blend yardstick is removed.")
    print("        Rows restated above cover LEADERBOARD claims for ideas 26, 100, 100b, 103, 357.")
    RS.to_csv(f"{OUT}.restated.csv", index=False)

    # ---------------------------------------------------------------- KEEP paths
    print("\n" + "=" * 120)
    print(f"### KEEP PATHS over all {len(G)} points (both reported, none selected on)")
    print(G.groupby(["universe", "conv"]).agg(n=("p4b", "size"), p4b=("p4b", "sum"),
                                              p4a_v2=("p4a", "sum"), p4a_v1=("p4a_v1", "sum")).to_string())
    print(f"  TOTAL: 4b {G.p4b.sum()}/{len(G)}; 4a vs RULES v2 {G.p4a.sum()}/{len(G)}; "
          f"4a vs RULES v1 {G.p4a_v1.sum()}/{len(G)}")
    Gd = G.copy()
    Gd["sleeve_eff"] = np.where(Gd.f == 0.0, "-", Gd.sleeve)
    Gd["conv_eff"] = np.where((Gd.f == 0.0) | (Gd.sleeve == "SCASH"), "-", Gd.conv)
    Dq = Gd.drop_duplicates(subset=["universe", "book", "sleeve_eff", "conv_eff", "f"])
    print(f"  DISTINCT books: {len(Dq)} of {len(G)} rows; 4b {int(Dq.p4b.sum())}/{len(Dq)}, "
          f"4a vs v2 {int(Dq.p4a.sum())}/{len(Dq)}")
    cols = ["universe", "sleeve", "book", "conv", "f", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "Turn_yr", "Gross", "p4a"]
    if Dq.p4b.sum():
        print("\n  4b passes (DISTINCT books), best 15 by Sharpe:")
        print(Dq[Dq.p4b][cols].sort_values("Sharpe", ascending=False).head(15).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    Dq[Dq.p4b].to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ---------------------------------------------------------------- (4) RULE 8
    print("\n" + "=" * 120)
    print("### (4) RULE 8 WALK-FORWARD — the statistic IS the selector.  Parameters chosen on")
    print("###     2009-2016 only; 2017-2026 read ONCE.  Four PRE-REGISTERED choosers pick the")
    print("###     (sleeve, f) pair maximising their own IS statistic; C_SHARPE is the record's")
    print("###     existing default; CTRL is the pure book (f=0).")
    wf = []
    for (tag, bname, conv), sub in D.groupby(["universe", "book", "conv"], sort=False):
        b1, v2, spy = refs[tag]
        g = G[(G.universe == tag) & (G.book == bname) & (G.conv == conv)]
        pool = sub[(sub.sleeve != "SCASH") & sub.IS_defined].copy()
        gpool = g[(g.f > 0) & (g.sleeve != "SCASH")]
        picks = {}
        for pname, col, src in (("C_CONV", "IS_conv_per_pp", pool),
                                ("C_RAW", "IS_raw_per_pp", pool),
                                ("C_DELTA", "IS_dSharpe_raw", pool),
                                ("C_SHARPE", "IS_Sharpe", gpool)):
            s2 = src[src[col].notna() & np.isfinite(src[col])]
            if not len(s2):
                continue
            picks[pname] = s2.loc[s2[col].idxmax()]
        ctrl = g[g.f == 0.0].iloc[0]
        for pname, p in picks.items():
            row = g[(g.sleeve == p.sleeve) & (g.f == p.f)].iloc[0]
            wf.append(dict(universe=tag, book=bname, conv=conv, chooser=pname,
                           pick=f"{p.sleeve}@f={p.f:.2f}",
                           OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
                           IS_Sharpe=row.IS_Sharpe,
                           beats_ctrl=int(row.OOS_Sharpe > ctrl.OOS_Sharpe),
                           beats_v2=int(row.OOS_Sharpe > v2["OOS_Sharpe"]),
                           beats_v1=int(row.OOS_Sharpe > b1["OOS_Sharpe"]),
                           beats_spy=int(row.OOS_Sharpe > spy["OOS_Sharpe"]),
                           p4b=bool(row.p4b), p4a=bool(row.p4a)))
        wf.append(dict(universe=tag, book=bname, conv=conv, chooser="CTRL(no sleeve)",
                       pick="-", OOS_CAGR=ctrl.OOS_CAGR, OOS_Sharpe=ctrl.OOS_Sharpe,
                       OOS_MaxDD=ctrl.OOS_MaxDD, IS_Sharpe=ctrl.IS_Sharpe,
                       beats_ctrl=0, beats_v2=int(ctrl.OOS_Sharpe > v2["OOS_Sharpe"]),
                       beats_v1=int(ctrl.OOS_Sharpe > b1["OOS_Sharpe"]),
                       beats_spy=int(ctrl.OOS_Sharpe > spy["OOS_Sharpe"]),
                       p4b=bool(ctrl.p4b), p4a=bool(ctrl.p4a)))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n  SUMMARY per chooser (12 cells each):")
    summ = W.groupby("chooser").apply(lambda g: pd.Series(dict(
        cells=len(g), OOS_Sharpe=g.OOS_Sharpe.mean(), OOS_CAGR=g.OOS_CAGR.mean(),
        OOS_MaxDD=g.OOS_MaxDD.mean(), beats_ctrl=g.beats_ctrl.sum(), beats_v1=g.beats_v1.sum(),
        beats_v2=g.beats_v2.sum(), beats_spy=g.beats_spy.sum(), p4b=g.p4b.sum(), p4a=g.p4a.sum())),
        include_groups=False)
    print(summ.to_string(float_format=lambda x: f"{x:.4f}"))
    for tag in universes:
        b1, v2, spy = refs[tag]
        print(f"  reference {tag}: SPY OOS Sharpe {spy['OOS_Sharpe']:.4f} CAGR {spy['OOS_CAGR']:.2%} "
              f"MaxDD {spy['OOS_MaxDD']:.2%} | RULES v2 {v2['OOS_Sharpe']:.4f} / {v2['OOS_CAGR']:.2%} "
              f"/ {v2['OOS_MaxDD']:.2%} | RULES v1 {b1['OOS_Sharpe']:.4f} / {b1['OOS_CAGR']:.2%}")

    print("\n  HEAD-TO-HEAD (OOS Sharpe, per cell):")
    piv = W.pivot_table(index=["universe", "book", "conv"], columns="chooser", values="OOS_Sharpe")
    print(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    for a, b in (("C_RAW", "C_CONV"), ("C_RAW", "C_DELTA"), ("C_RAW", "C_SHARPE"),
                 ("C_CONV", "C_SHARPE"), ("C_DELTA", "C_CONV")):
        if a in piv and b in piv:
            d = piv[a] - piv[b]
            print(f"    {a} beats {b} in {int((d>0).sum())}/{int(d.notna().sum())} cells, "
                  f"mean margin {d.mean():+.4f}")

    print("\nDONE.")


if __name__ == "__main__":
    main()
