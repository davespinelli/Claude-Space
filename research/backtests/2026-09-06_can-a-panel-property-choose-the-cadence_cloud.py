#!/usr/bin/env python3
"""IDEA 188  can a PANEL PROPERTY choose the cadence?   (cloud lane, 2026-09-06)

COLLISION NOTICE, STATED FIRST.  A sibling cloud lane answered idea 188 on 2026-09-05 and
committed it as `2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud.*` while
this run was in flight; the queue read as open when this lane claimed it.  This run is NOT a
replacement.  It measures the same two properties independently (agreeing on both), and adds
the step the queue's last clause asks for and the sibling did not take: it turns each property
into an actual SELECTOR and prices it under rule 8 against the constants.  The `.result.md`
reconciles the two line by line.

QUESTION (QUEUE.md).  Idea 175's constant table splits cleanly: M is +0.0978 (t +3.91) on the
SMALL family where 6W is +0.0163 (n.s.), while on U56/ETF 6W is +0.164/+0.160 and Q is
-0.25/-0.29.  Turnover alone does not explain it (small turns 15.6x at D vs 12.7x on U56).
Decompose the M-vs-6W gap by HOLDING-EPISODE LENGTH (idea 76) and by REALISED SIGNAL DECAY per
panel; the output is the universe clause idea 77 wants.

WHAT A "UNIVERSE CLAUSE" HAS TO DO TO EXIST.  A family label is not a clause: "small caps want
M" cannot be written into RULES because a future panel carries no label.  A clause needs a
MEASURABLE PANEL PROPERTY, computable in-sample, that (a) explains the family split and (b)
chooses the cadence at least as well as writing a constant down.  This run therefore does three
things in order, and reports all three even where they disagree:

  1. MEASURE the two candidate properties per book, both cadence-free so neither can be a
     restatement of the dial under test:
       * SIGNAL DECAY -- the cross-sectional rank IC of the composite against forward return at
         horizons h = 5..126 trading days, and the horizon h* that maximises IC(h)/sqrt(h),
         which is the interval a rebalance rule should target (annualised IR of an h-day rule
         is proportional to IC(h)*sqrt(252/h)).
       * HOLDING-EPISODE LENGTH -- idea 76's measure, computed on DAILY membership of the top-20
         book so that it is a property of the panel's selection persistence and not of any
         cadence.
  2. DECOMPOSE idea 175's M-minus-6W gap on those properties, and ask whether they absorb the
     family dummy.  A property that only re-labels the family is not a clause.
  3. PRICE the clause under rule 8: choose the cadence per book from the IS window's own
     property value, read 2017-2026 once, against the incumbent constant W, idea 175's proposed
     constant M, the IS-Sharpe selector it beat, and an oracle.  If the property loses to
     writing M down, the honest output is "write the constant", not "write the clause".

TUNED PARAMETERS (exactly 2, all 6 grid points reported):
  1. horizon statistic in {IR (argmax IC(h)/sqrt(h)), IC (argmax IC(h)), HALF (IC half-life)}
  2. IC sampling stride in {21, 63} trading days (overlap control)
  Carried axes (not tuned): 115 books, 3 families, the 7-point cadence ladder D/2D/W/2W/M/6W/Q,
  the 8 horizons, IS/OOS windows.

PROTOCOL.
  * 2: t+1 and 10 bps inherited from idea 175's `fast_backtest`, asserted against the engine.
  * 3: RULES v1 and SPY reported over the same windows.
  * 4: both KEEP paths reported for all 805 (book, cadence) points and cross-tabulated by
    cadence and family.  This idea proposes NO book and claims neither path.
  * 5: one idea, one script, deterministic; the only randomness is idea 175's own sub-panel
    draws, imported with its seeds (zlib.crc32 elsewhere; no hash() of a str anywhere).
  * 8: the walk-forward IS the point of section 3 -- every property is computed on
    IS <= 2016-12-31 only and 2017-2026 is read once.
  * 9: SMALL439 and its sub-panels are CURRENT CONSTITUENTS of a sub-$2B screen (the 483-name
    panel less the 44 `max_1d_move >= 1.0` tickers per data/small_meta.csv).  Survivorship is
    one-directional, falls hardest on beaten-down names, and inflates every level below; the
    CONTRASTS between panels are what this run reads, and they are biased too because the small
    panel's bias is the largest.

Idea 175's corpus, book construction, cadence mask, backtest and KEEP evaluators are IMPORTED
VERBATIM, and its published 805-row ladder and its constants table are reproduced before any new
number is read.

Writes .console.txt, .props.csv, .ic.csv, .decomp.csv, .walkforward.csv, .keep.csv.
"""
import importlib.util
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-06_can-a-panel-property-choose-the-cadence_cloud"
OUT = ROOT / "research" / "backtests"
P175_STEM = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"

HORIZONS = [5, 10, 21, 30, 42, 63, 90, 126]
STRIDES = [21, 63]                       # tuned parameter 2
HSTATS = ["IR", "IC", "HALF"]            # tuned parameter 1
CAD_DAYS = {"D": 1, "2D": 2, "W": 5, "2W": 10, "M": 21, "6W": 30, "Q": 63}
SEED = zlib.crc32(b"idea-188-cadence-universe-clause") % (2 ** 31)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


spec = importlib.util.spec_from_file_location("p175", OUT / f"{P175_STEM}.py")
p175 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p175)
p175.P = P

LADDER = p175.LADDER
IS_END, OOS_START = p175.IS_END, p175.OOS_START


# ------------------------------------------------------------------ the two panel properties
def rank_ic(book, horizons, stride, upto=None):
    """Cross-sectional Spearman IC of the composite against forward return, per horizon.
    Sampled every `stride` trading days so overlapping windows cannot inflate the t-stat.
    Restricted to ELIGIBLE names, because that is the set the book ever ranks."""
    px = book.px[book.tradable]
    comp = book.comp[book.tradable]
    elig = book.elig[book.tradable]
    idx = px.index
    end = len(idx) if upto is None else int(np.searchsorted(idx, pd.Timestamp(upto), "right"))
    out = {}
    for h in horizons:
        fwd = px.shift(-h) / px - 1.0
        rows = np.arange(260, end - h, stride)
        if len(rows) < 12:
            out[h] = (np.nan, np.nan, 0)
            continue
        c = comp.iloc[rows].where(elig.iloc[rows])
        f = fwd.iloc[rows].where(elig.iloc[rows])
        ok = c.notna() & f.notna()
        c, f = c.where(ok), f.where(ok)
        rc = c.rank(axis=1)
        rf = f.rank(axis=1)
        n = ok.sum(axis=1).values.astype(float)
        rc, rf = rc.values, rf.values
        mc = np.nanmean(rc, axis=1, keepdims=True)
        mf = np.nanmean(rf, axis=1, keepdims=True)
        dc, df = rc - mc, rf - mf
        num = np.nansum(dc * df, axis=1)
        den = np.sqrt(np.nansum(dc ** 2, axis=1) * np.nansum(df ** 2, axis=1))
        with np.errstate(invalid="ignore", divide="ignore"):
            ic = np.where((den > 0) & (n >= 5), num / den, np.nan)
        ic = ic[np.isfinite(ic)]
        t = (ic.mean() / (ic.std(ddof=1) / np.sqrt(len(ic)))) if len(ic) > 2 and ic.std(ddof=1) > 0 else np.nan
        out[h] = (float(ic.mean()) if len(ic) else np.nan, float(t) if t == t else np.nan, len(ic))
    return out


def h_star(ics, stat):
    """Turn an IC(h) curve into a target holding horizon in trading days."""
    hs = [h for h in HORIZONS if np.isfinite(ics[h][0])]
    if not hs:
        return np.nan
    if stat == "IR":                      # argmax IC(h)/sqrt(h): the interval an h-day rule wants
        return float(max(hs, key=lambda h: ics[h][0] / np.sqrt(h)))
    if stat == "IC":                      # argmax raw IC(h)
        return float(max(hs, key=lambda h: ics[h][0]))
    peak = max(hs, key=lambda h: ics[h][0])   # HALF: where IC falls to half its peak
    half = ics[peak][0] / 2.0
    if ics[peak][0] <= 0:
        return float(peak)
    for h in hs:
        if h > peak and ics[h][0] < half:
            return float(h)
    return float(hs[-1])


def episode_days(book, upto=None):
    """Idea 76's measure, made cadence-free: mean length in TRADING DAYS of a maximal run of
    consecutive days on which a name sits in the daily top-20 among eligible names."""
    rank = book.comp.where(book.elig).rank(axis=1, ascending=False)
    M = (rank <= p175.INC_N).values
    if upto is not None:
        M = M[:int(np.searchsorted(book.px.index, pd.Timestamp(upto), "right"))]
    M = M[260:]
    if M.shape[0] < 30:
        return np.nan, np.nan
    pad = np.zeros((1, M.shape[1]), bool)
    # column-major flattening, each column padded False at both ends, so runs cannot be
    # spliced across names (a 2-D diff plus flatnonzero silently would)
    A = np.vstack([pad, M, pad]).T.ravel()
    d = np.diff(A.astype(np.int8))
    starts = np.flatnonzero(d == 1)
    ends = np.flatnonzero(d == -1)
    if not len(starts):
        return np.nan, np.nan
    lens = (ends - starts).astype(float)
    return float(lens.mean()), float(np.median(lens))


def nearest_cad(days):
    """The ladder point whose nominal spacing is closest to `days` in log space."""
    if not np.isfinite(days):
        return p175.CONST_PT
    return min(LADDER, key=lambda c: abs(np.log(CAD_DAYS[c]) - np.log(max(days, 1.0))))


def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 188  why-does-the-small-panel-want-M-and-the-large-caps-6W   (cloud, 2026-09-06)")
    P("=" * 118)

    books, pxmap = p175.build_corpus()
    P(f"  corpus: {len(books)} books "
      f"({sum(p175.family_of(b.name) == 'SMALL' for b in books)} SMALL / "
      f"{sum(p175.family_of(b.name) == 'U56' for b in books)} U56 / "
      f"{sum(p175.family_of(b.name) == 'ETF' for b in books)} ETF)")

    # -------------------------------------------------------------- reproduction, first
    P("\n" + "=" * 118)
    P("REPRODUCTION, asserted before any new number is read")
    P("=" * 118)
    ok = True
    ref = books[0]
    for nm, fn in (("[a] cad_mask == engine.rebalance_mask", p175.check_a),
                   ("[b] fast_backtest == engine.backtest", p175.check_b),
                   ("[c] CAND-20 weights == idea 78/171 weights_cand", p175.check_c)):
        r = fn(ref)
        P(f"  {nm}: {'PASS' if r else 'FAIL'}")
        ok &= bool(r)

    LAD = []
    for b in books:
        W = b.weights()
        spy = b.px["SPY"].pct_change().fillna(0.0)
        for cad in LADDER:
            res = p175.fast_backtest(b.px, W, cad=cad)
            r = res["returns"].loc[b.px.index[260]:]
            m = metrics(r)
            LAD.append(dict(book=b.name, family=p175.family_of(b.name), point=cad,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            turnover=res["turnover"].loc[b.px.index[260]:].sum()
                            / m["Years"],
                            IS_Sharpe=p175._sh(r.loc[:IS_END]),
                            OOS_Sharpe=p175._sh(r.loc[OOS_START:]),
                            OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                            OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                            spy_oos_sharpe=p175._sh(spy.loc[OOS_START:])))
    L = pd.DataFrame(LAD)
    PUB = pd.read_csv(OUT / f"{P175_STEM}.ladder.csv")
    j = L.merge(PUB, on=["book", "point"], suffixes=("", "_pub"))
    P(f"\n  [d] vs idea 175's published ladder.csv: matched {len(j)}/{len(PUB)} rows")
    for c in ("Sharpe", "CAGR", "MaxDD", "IS_Sharpe", "OOS_Sharpe", "turnover"):
        d = float((j[c] - j[f"{c}_pub"]).abs().max())
        P(f"      max|d {c:<11s}| = {d:.3e}  -> {'PASS' if d < 1e-10 else 'FAIL'}")
        ok &= d < 1e-10

    # idea 175's headline constants table, re-derived from this run's own ladder
    piv = L.pivot(index="book", columns="point", values="OOS_Sharpe")
    fam = L.groupby("book").family.first()
    CON = []
    for f_ in ["ALL", "SMALL", "U56", "ETF"]:
        sel = piv.index if f_ == "ALL" else fam[fam == f_].index
        for pt in LADDER:
            d = (piv.loc[sel, pt] - piv.loc[sel, p175.CONST_PT]).dropna()
            CON.append(dict(family=f_, point=pt, n=len(d), mean_d=float(d.mean()),
                            t=p175.tstat(list(d)), wins=int((d > 0).sum()),
                            losses=int((d < 0).sum())))
    C = pd.DataFrame(CON)
    CPUB = pd.read_csv(OUT / f"{P175_STEM}.constants.csv")
    jc = C.merge(CPUB, on=["family", "point"], suffixes=("", "_pub"))
    dd = float((jc.mean_d - jc.mean_d_pub).abs().max())
    P(f"\n  [e] idea 175's constants table ({len(jc)} cells) re-derived: max|d mean_d| = "
      f"{dd:.3e} -> {'PASS' if dd < 1e-10 else 'FAIL'}")
    ok &= dd < 1e-10
    P("\n  the split this idea exists to explain (mean OOS Sharpe minus the W incumbent):")
    P(C[C.point.isin(["M", "6W", "Q"])].pivot(index="family", columns="point",
      values="mean_d").to_string(float_format=lambda x: f"{x:+.4f}"))
    P(f"\n  REPRODUCTION: {'ALL PASS' if ok else 'FAILURE -- STOP'}")
    if not ok:
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # -------------------------------------------------------------- (1) the panel properties
    P("\n" + "=" * 118)
    P("(1) THE TWO CANDIDATE PANEL PROPERTIES, measured cadence-free")
    P("=" * 118)
    props, icrows = [], []
    for b in books:
        f_ = p175.family_of(b.name)
        ep_full, epm_full = episode_days(b)
        ep_is, _ = episode_days(b, upto=IS_END)
        rec = dict(book=b.name, family=f_, n_names=len(b.tradable),
                   episode_days=ep_full, episode_days_median=epm_full,
                   episode_days_IS=ep_is)
        for stride in STRIDES:
            ic_full = rank_ic(b, HORIZONS, stride)
            ic_is = rank_ic(b, HORIZONS, stride, upto=IS_END)
            for h in HORIZONS:
                icrows.append(dict(book=b.name, family=f_, stride=stride, h=h,
                                   IC=ic_full[h][0], t=ic_full[h][1], obs=ic_full[h][2],
                                   IC_over_sqrt_h=ic_full[h][0] / np.sqrt(h),
                                   IC_IS=ic_is[h][0]))
            for st in HSTATS:
                rec[f"hstar_{st}_s{stride}"] = h_star(ic_full, st)
                rec[f"hstarIS_{st}_s{stride}"] = h_star(ic_is, st)
            rec[f"IC5_s{stride}"] = ic_full[5][0]
            rec[f"IC21_s{stride}"] = ic_full[21][0]
            rec[f"IC126_s{stride}"] = ic_full[126][0]
        props.append(rec)
    PR = pd.DataFrame(props)
    IC = pd.DataFrame(icrows)
    PR.to_csv(OUT / f"{STEM}.props.csv", index=False)
    IC.to_csv(OUT / f"{STEM}.ic.csv", index=False)

    P("\n  realised signal decay -- mean cross-sectional rank IC by family and horizon "
      "(stride 21):")
    P(IC[IC.stride == 21].pivot_table(index="family", columns="h", values="IC")
      .to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n  the same curve scaled as an h-day rule's information ratio, IC(h)/sqrt(h) "
      "(x100, stride 21):")
    q = IC[IC.stride == 21].pivot_table(index="family", columns="h",
                                        values="IC_over_sqrt_h") * 100
    P(q.to_string(float_format=lambda x: f"{x:+.3f}"))
    P("  family argmax of IC(h)/sqrt(h): " + ", ".join(f"{i} -> h={q.loc[i].idxmax()}d"
                                                       for i in q.index))
    P("\n  holding-episode length (idea 76's measure on DAILY top-20 membership) and h*, "
      "by family:")
    cols = ["episode_days", "episode_days_median"] + [f"hstar_{st}_s21" for st in HSTATS] \
        + [f"hstar_{st}_s63" for st in HSTATS]
    P(PR.groupby("family")[cols].mean().to_string(float_format=lambda x: f"{x:.2f}"))
    P("\n  ...and the same, per fixed book (the three un-sampled panels):")
    P(PR[PR.book.isin(["SMALL439", "U56", "ETF36"])][["book", "n_names"] + cols]
      .to_string(index=False, float_format=lambda x: f"{x:.2f}"))

    # -------------------------------------------------------------- (2) the decomposition
    P("\n" + "=" * 118)
    P("(2) DECOMPOSING IDEA 175's M-MINUS-6W GAP -- does either property absorb the family?")
    P("=" * 118)
    gap = (piv["M"] - piv["6W"]).rename("gap")
    D = PR.set_index("book").join(gap).join(
        L[L.point == "W"].set_index("book")[["turnover"]].rename(columns={"turnover": "turn_W"}))
    D = D.dropna(subset=["gap"])
    P(f"\n  gap = OOS Sharpe(M) - OOS Sharpe(6W), {len(D)} books; by family:")
    P(D.groupby("family").gap.agg(["size", "mean", "std",
                                   lambda x: p175.tstat(list(x))])
      .rename(columns={"<lambda_0>": "t"}).to_string(float_format=lambda x: f"{x:+.4f}"))

    def ols(y, X):
        X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
        b, *_ = np.linalg.lstsq(X, np.asarray(y, float), rcond=None)
        r = np.asarray(y, float) - X @ b
        ss = ((np.asarray(y, float) - np.mean(y)) ** 2).sum()
        return b, 1 - (r ** 2).sum() / ss if ss > 0 else np.nan

    famd = [(D.family == f_).astype(float) for f_ in ("SMALL", "ETF")]
    specs = {
        "family dummies only": famd,
        "log h* (IR, stride 21)": [np.log(D["hstar_IR_s21"])],
        "log episode_days": [np.log(D["episode_days"])],
        "log turnover at W": [np.log(D["turn_W"].clip(lower=1e-6))],
        "log h* + log episode": [np.log(D["hstar_IR_s21"]), np.log(D["episode_days"])],
        "log h* + log episode + family": [np.log(D["hstar_IR_s21"]),
                                          np.log(D["episode_days"])] + famd,
    }
    drows = []
    for nm, X in specs.items():
        b, r2 = ols(D.gap, X)
        drows.append(dict(spec=nm, k=len(X), R2=r2,
                          coef=" ".join(f"{v:+.4f}" for v in b[1:])))
    DEC = pd.DataFrame(drows)
    P("\n  OLS of the gap on candidate explanators (all 115 books):")
    P(DEC.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    DEC.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    P("")
    for c, lab in (("hstar_IR_s21", "h* (IR)"), ("hstar_HALF_s21", "h* (half-life)"),
                   ("episode_days", "episode_days"), ("turn_W", "turnover at W")):
        within = ", ".join(f"{f_} {_spear(g.gap, g[c]):+.4f}" for f_, g in D.groupby("family"))
        P(f"  Spearman(gap, {lab:<16s}) = {_spear(D.gap, D[c]):+.4f}   |  within-family: "
          f"{within}")

    # -------------------------------------------------------------- (3) rule 8
    P("\n" + "=" * 118)
    P("(3) RULE 8 -- can the property CHOOSE the cadence better than writing a constant down?")
    P("=" * 118)
    P("  Every property recomputed on IS <= 2016-12-31 only; 2017-2026 read once.")
    isp = L.pivot(index="book", columns="point", values="IS_Sharpe")
    wrows = []
    for b in books:
        nm, f_ = b.name, p175.family_of(b.name)
        row = PR.set_index("book").loc[nm]
        arms = {"A0 constant W": "W", "A1 constant M": "M", "A2 constant 6W": "6W",
                "A3 SEL-SHARPE (IS argmax)": isp.loc[nm].idxmax()}
        for st in HSTATS:
            for stride in STRIDES:
                arms[f"A4 DECAY {st}/s{stride}"] = nearest_cad(row[f"hstarIS_{st}_s{stride}"])
        arms["A5 EPISODE (IS)"] = nearest_cad(row["episode_days_IS"])
        arms["ORACLE (OOS argmax)"] = piv.loc[nm].idxmax()
        for a, pt in arms.items():
            wrows.append(dict(book=nm, family=f_, arm=a, pick=pt,
                              OOS_Sharpe=piv.loc[nm, pt],
                              OOS_CAGR=L[(L.book == nm) & (L.point == pt)].OOS_CAGR.iloc[0],
                              OOS_MaxDD=L[(L.book == nm) & (L.point == pt)].OOS_MaxDD.iloc[0],
                              base_W=piv.loc[nm, "W"], base_M=piv.loc[nm, "M"]))
    WF = pd.DataFrame(wrows)
    WF["dW"] = WF.OOS_Sharpe - WF.base_W
    WF["dM"] = WF.OOS_Sharpe - WF.base_M
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    agg = WF.groupby("arm").agg(
        n=("dW", "size"), mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
        mean_OOS_CAGR=("OOS_CAGR", "mean"), mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
        d_vs_W=("dW", "mean"), t_vs_W=("dW", lambda x: p175.tstat(list(x))),
        d_vs_M=("dM", "mean"), t_vs_M=("dM", lambda x: p175.tstat(list(x))),
        win_vs_M=("dM", lambda x: float((np.asarray(x) > 1e-12).mean()))
    ).sort_values("mean_OOS_Sharpe", ascending=False)
    P("\n  all 115 books:")
    P(agg.to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n  by family (mean OOS Sharpe):")
    P(WF.pivot_table(index="arm", columns="family", values="OOS_Sharpe")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  what each arm actually picks (share of books):")
    for a in sorted(WF.arm.unique()):
        vc = WF[WF.arm == a].pick.value_counts(normalize=True)
        P(f"    {a:<26s} " + "  ".join(f"{k} {v:.0%}" for k, v in vc.items()))

    spy_oos = float(L.spy_oos_sharpe.iloc[0])
    rv = {}
    for k, px in pxmap.items():
        r = backtest(px, rules_v1_weights(px), cost_bps=10.0,
                     freq="W")["returns"].loc[px.index[260]:]
        rv[k] = (metrics(r.loc[OOS_START:])["CAGR"], p175._sh(r.loc[OOS_START:]),
                 metrics(r.loc[OOS_START:])["MaxDD"])
    P(f"\n  references, same OOS window: SPY Sharpe {spy_oos:.4f}; "
      + "; ".join(f"RULES v1 on {k} {v[0]:.2%}/{v[1]:.4f}/{v[2]:.2%}" for k, v in rv.items()))

    # -------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 118)
    P("PROTOCOL 4 -- KEEP paths across all 805 (book, cadence) points")
    P("=" * 118)
    K = PUB.copy()
    K["pass4a"] = K.fail4a == "-"
    K["pass4b"] = K.fail4b == "-"
    P("\n  4a passes by family x cadence:")
    P(K.pivot_table(index="family", columns="point", values="pass4a",
                    aggfunc="sum").reindex(columns=LADDER).to_string())
    P("\n  4b passes by family x cadence:")
    P(K.pivot_table(index="family", columns="point", values="pass4b",
                    aggfunc="sum").reindex(columns=LADDER).to_string())
    P(f"\n  totals: 4a {int(K.pass4a.sum())}/{len(K)}, 4b {int(K.pass4b.sum())}/{len(K)}")
    K[["book", "family", "point", "pass4a", "pass4b", "fail4a", "fail4b"]].to_csv(
        OUT / f"{STEM}.keep.csv", index=False)
    P("  (the 4a/4b columns are idea 175's own, carried unchanged; this idea proposes no book "
      "and claims neither path)")

    # -------------------------------------------------------------- predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    hs = PR.groupby("family").hstar_IR_s21.mean()
    ed = PR.groupby("family").episode_days.mean()
    p1 = bool(hs.get("SMALL", np.inf) < hs.get("U56", 0) and hs.get("SMALL", np.inf) < hs.get("ETF", 0))
    p2 = bool(ed.get("SMALL", np.inf) < ed.get("U56", 0))
    r2f = float(DEC[DEC.spec == "family dummies only"].R2.iloc[0])
    r2p = float(DEC[DEC.spec == "log h* + log episode"].R2.iloc[0])
    p3 = bool(r2p >= 0.5 * r2f)
    best = agg.d_vs_M[[i for i in agg.index if i.startswith(("A4", "A5"))]]
    p4 = bool((best <= 1e-12).all())
    icf = IC[(IC.stride == 21)].pivot_table(index="family", columns="h", values="IC")
    p5 = bool((icf[126] < icf[21]).all())
    for tag, hit, note in (
        ("P1 SMALL's IR-optimal horizon is the shortest of the three families", p1,
         ", ".join(f"{k} {v:.1f}d" for k, v in hs.items())),
        ("P2 SMALL's holding episodes are shorter than U56's", p2,
         ", ".join(f"{k} {v:.1f}d" for k, v in ed.items())),
        ("P3 the two properties recover >=50% of the family dummies' R2", p3,
         f"properties R2 {r2p:.4f} vs family R2 {r2f:.4f}"),
        ("P4 no property-chosen cadence beats the constant M", p4,
         f"best d vs M {best.max():+.4f} ({best.idxmax() if len(best) else 'n/a'})"),
        ("P5 IC decays over the horizon grid in every family", p5,
         ", ".join(f"{k}: {icf.loc[k,21]:+.4f}@21d -> {icf.loc[k,126]:+.4f}@126d"
                   for k in icf.index))):
        P(f"  {'HIT ' if hit else 'MISS'}  {tag:<66s} {note}")
    P(f"\n  {sum([p1, p2, p3, p4, p5])} of 5 predictions hit.")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


def _spear(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


if __name__ == "__main__":
    main()
