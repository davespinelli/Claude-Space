#!/usr/bin/env python3
"""Idea 384: price the no-trade BAND's DRAWDOWN TAX across the record.

Idea 333 pinned idea 329's whole B136 4b drawdown failure on the no-trade BAND: at
(B136, n=20, gross 0.75, weekly) the m=0 anchor clears 4b's DD cap by +0.0018 while the
m=20 cell misses it by -0.0020, i.e. dMaxDD(m=20) is roughly -38 bp of NAV on that one
book.  The band is a pure TURNOVER dial (idea 359 measured its holdings identical to the
last decimal at every m), so if it also moves drawdown it is buying turnover WITH
drawdown, and 4b's DD cap prices that trade.

THE QUESTION, exactly as filed: measure dMaxDD(m) on every committed grid CSV that
carries both a band dial and a MaxDD column, and report whether the tax is

    H_const   a CONSTANT of m           dMaxDD ~ a(m)            (a bp figure per rung)
    H_scale   SCALES with the book's DD dMaxDD ~ b(m) * |DD_0|   (a percentage of the book)

The two hypotheses are not decorative: under H_const the band's DD cost is a fixed
subtraction any book can be pre-screened against; under H_scale it is a multiplier and a
deep book pays more for the same turnover saving, so the band can never rescue exactly the
books that need rescuing.  A third possibility the queue's wording assumes away is tested
first: that dMaxDD(m) is not consistently signed at all, in which case there is no tax.

[A] ARCHIVE CENSUS.  Every committed research/backtests/*.csv carrying a column named
    exactly `m` together with a MaxDD-like column.  The record OVERLOADS `m` (idea 103's
    share multiplier is also written `m`, fractional), so only files whose `m` is
    integral are the no-trade band.  Rows are grouped by their remaining low-cardinality
    axis columns; each group with >= 2 distinct m yields dMaxDD(m) = DD(m) - DD(m_min).
    The `band` column (the 200d MA band WIDTH, a different instrument) is censused
    separately as a labelled contrast, never pooled.

[B] DIRECT MEASUREMENT, with rule 8.  The archive cannot answer a question about the
    shape of a curve if the record only ever wrote two points of it, so the same question
    is re-measured on a clean grid.

    Family, pre-registered and fixed before anything is run (idea 331/333's convention):
        book      top-n of the v1 composite with the VOL SCALER OFF, among RULES v1
                  eligible names (200d MA up, vol20 < 0.60); NORM weights g / k_t
        band      sel_band (idea 273/331): enter at rank <= n, hold until rank passes
                  n + m; free slots refill best-rank-first; slot count is the parent's
                  own k_t so m is name-count matched and a pure turnover dial
        gross     0.75, NOT swept          cadence  weekly, NOT swept
    THE TWO TUNED PARAMETERS, and the only two:
        n  in {10, 20, 40}          m  in {0, 5, 10, 20, 40}
    = 15 cells per panel, ALL reported.  Panel {U56, B136, SMALL439} and cost rung
    {0, 10, 25} bps are REPORTED AXES, not choices; 10 bps is PROTOCOL's.

    Both KEEP paths are evaluated at every one of the 45 cells: 4a against the LIVE
    RULES v2 book on the same panel, 4b against SPY.  Rule 8: (n, m) chosen on 2008-2016
    IS Sharpe at 10 bps, 2017-2026 read ONCE, against SPY, RULES v2 and the OOS-best cell.

GATES, all exact, run before any new number is read:
    G1  fast_backtest vs products/backtester/engine.backtest (returns AND turnover).
    G2  the derived cost rungs vs live cost_bps runs.
    G3  sel_band(m=0) nests sel_hard(n) exactly on every rebalance day.
    G4  the (B136, n=20, g=0.75, m=0, W) cell reproduces idea 333's committed grid row.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so CAGR
levels are optimistic and 4b's CAGR floor is tested in the book's favour.  (2) The 4a
comparand RULES v2 runs at its own live weekly cadence and gross, so the dials move the
idea arm only.  (3) SMALL439 starts 2010-01-04 and drops the 44 tickers with
max_1d_move >= 1.0.  (4) The archive census is a census of what the record WROTE; a file
that swept m but committed no CSV cannot enter it, and that shortfall is reported.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_price-the-no-trade-BANDs-DRAWDOWN-TAX-across-the-record_B"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, FREQ = 0.60, 0.75, "W"
NS, MS, COSTS = [10, 20, 40], [0, 5, 10, 20, 40], [0, 10, 25]
IS_END, OOS_START, WARMUP = "2016-12-31", "2017-01-01", 260
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


# ================================================================ [A] archive census
METRIC = re.compile(
    r"(cagr|sharpe|maxdd|max_dd|calmar|sortino|sortino|vol\b|volatility|^h1|^h2|_h1|_h2|oos|"
    r"^is_|_is$|turn|^to$|names|reb_per|avg_gross|breakeven|margin|m4a|m4b|corr|spear|"
    r"rate|frac|slope|r2|delta|^d[A-Z]|equity|total|winrate|bestday|worstday|years|"
    r"mean|median|std|count|ic$|_ic|tstat|pval|p_)", re.I)
AXISKILL = re.compile(r"(pass|fail|keep|adm|verdict|note|why|reason|first_fail)", re.I)
DDCOL = re.compile(r"maxdd|max_dd", re.I)


def census_file(path, dial):
    """Return long-form (dial, DD0, dDD) records recoverable from one committed CSV."""
    try:
        df = pd.read_csv(path)
    except Exception:
        return [], None
    if dial not in df.columns:
        return [], None
    dds = [c for c in df.columns if DDCOL.search(c) and c != dial]
    if not dds:
        return [], None
    v = pd.to_numeric(df[dial], errors="coerce")
    if v.isna().all():
        return [], None
    df = df.loc[v.notna()].copy(); df[dial] = v[v.notna()]      # numeric dial values only
    v = df[dial]
    integral = bool(np.all(np.isclose(v.dropna() % 1, 0)))
    kind = "INT" if integral else "FRAC"
    if v.nunique() < 2 or v.nunique() > 12:
        # <2: not swept here.  >12: this is a computed OUTPUT column that happens to be
        # called `band` (e.g. the "admissible gross band" WIDTH), not a swept dial.
        return [], kind
    keys = []
    for c in df.columns:
        if c == dial or c in dds:
            continue
        if df[c].dtype == bool or AXISKILL.search(c) or METRIC.search(c):
            continue
        nu = df[c].nunique(dropna=False)
        num = pd.api.types.is_numeric_dtype(df[c])
        if (num and nu <= 12) or (not num and nu <= 40):
            keys.append(c)
    recs = []
    grouper = df.groupby([df[c].astype(str) for c in keys], dropna=False) if keys \
        else [((), df)]
    for gk, g in grouper:
        g = g.dropna(subset=[dial])
        if g[dial].nunique() < 2 or g[dial].duplicated().any():
            continue
        g = g.sort_values(dial)
        m0 = g[dial].iloc[0]
        for dd in dds:
            y = pd.to_numeric(g[dd], errors="coerce")
            if y.isna().any() or not np.isfinite(y).all():
                continue
            base = y.iloc[0]
            if not (-1.0 < base < 0.0):          # MaxDD is a negative fraction
                continue
            for mv, yv in zip(g[dial], y):
                if mv == m0:
                    continue
                recs.append(dict(file=path.name, dial=dial, kind=kind,
                                 group="|".join(map(str, gk if isinstance(gk, tuple) else (gk,))),
                                 ddcol=dd, m0=m0, m=mv, DD0=base, DD=yv, dDD=yv - base))
    return recs, kind


def archive_census():
    P("\n[A] ARCHIVE CENSUS — dMaxDD(m) recovered from committed grid CSVs")
    files = [f for f in sorted(OUT.glob("*.csv")) if not f.name.startswith(SLUG)]
    P(f"    committed CSVs scanned: {len(files)}")
    rows, kinds = [], {"m": [], "band": []}
    for f in files:
        for dial in ("m", "band"):
            r, k = census_file(f, dial)
            if k:
                kinds[dial].append((f.name, k))
            rows += r
    cen = pd.DataFrame(rows)
    for dial in ("m", "band"):
        ks = kinds[dial]
        ni = sum(1 for _, k in ks if k == "INT")
        P(f"    files with a `{dial}` column and a MaxDD column: {len(ks)}"
          f"  (integral dial {ni}, fractional {len(ks)-ni})")
    if cen.empty:
        P("    NOTHING RECOVERABLE — census empty."); return cen
    band_int = cen[(cen.dial == "m") & (cen.kind == "INT")].copy()
    P(f"    dMaxDD observations recovered: {len(cen)} total; "
      f"NO-TRADE BAND (`m`, integral) {len(band_int)} from "
      f"{band_int.file.nunique()} scripts / {band_int.groupby(['file','group']).ngroups} ladders")
    P(f"    excluded as the OVERLOADED fractional `m` (idea 103's share dial): "
      f"{len(cen[(cen.dial=='m') & (cen.kind=='FRAC')])} observations")
    P(f"    `band` (200d MA WIDTH — a DIFFERENT instrument, reported only as contrast): "
      f"{len(cen[cen.dial=='band'])} observations")
    cen.to_csv(OUT / f"{SLUG}.census.csv", index=False)
    return cen


def tax_shape(d, label):
    """The run's core test: is dDD a constant of m, or proportional to the book's own DD?"""
    if d.empty or len(d) < 6:
        P(f"    [{label}] too few observations ({len(d)}) to fit."); return None
    d = d.copy()
    d["ratio"] = d.dDD / d.DD0.abs()
    neg, pos, zer = (d.dDD < -1e-12).mean(), (d.dDD > 1e-12).mean(), (d.dDD.abs() <= 1e-12).mean()
    P(f"    [{label}] n={len(d)}  SIGN: worsens DD {neg:.1%} | improves {pos:.1%} | exact 0 {zer:.1%}"
      f"  median dMaxDD {d.dDD.median():+.4f} ({d.dDD.median()*1e4:+.1f} bp)")
    # per-m level table, and the two competing fits
    lev = []
    for mv, g in d.groupby("m"):
        a = g.dDD.median()                     # H_const coefficient at this m
        b = g.ratio.median()                   # H_scale coefficient at this m
        rc = float(np.nanmedian(np.abs(g.dDD - a)))
        rs = float(np.nanmedian(np.abs(g.dDD - b * g.DD0.abs())))
        # dispersion of each model's own coefficient across books (the crisp test)
        disp_c = float(np.nanmedian(np.abs(g.dDD - a))) / (abs(a) if abs(a) > 1e-9 else np.nan)
        disp_s = float(np.nanmedian(np.abs(g.ratio - b))) / (abs(b) if abs(b) > 1e-9 else np.nan)
        # does the tax correlate with the book's own DD at this m?
        r = g[["dDD", "DD0"]].corr().iloc[0, 1] if len(g) > 2 and g.DD0.nunique() > 2 else np.nan
        lev.append(dict(m=mv, n=len(g), a_const=a, b_scale=b, mae_const=rc, mae_scale=rs,
                        reldisp_const=disp_c, reldisp_scale=disp_s, corr_dDD_DD0=r))
    lv = pd.DataFrame(lev)
    P(lv.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    tc, ts = lv.mae_const.sum(), lv.mae_scale.sum()
    P(f"    [{label}] pooled MAE  H_const {tc:.5f}  vs  H_scale {ts:.5f}  -> "
      f"{'H_scale' if ts < tc else 'H_const'} fits better by {abs(tc-ts)/max(tc,ts,1e-12):.1%}")
    ok = lv.dropna(subset=["reldisp_const", "reldisp_scale"])
    if len(ok):
        w = (ok.reldisp_scale < ok.reldisp_const).sum()
        P(f"    [{label}] relative coefficient dispersion: the SCALE coefficient is tighter "
          f"than the CONSTANT one at {w}/{len(ok)} m-levels")
    cc = d[["dDD", "DD0"]].corr().iloc[0, 1]
    P(f"    [{label}] pooled corr(dMaxDD, DD0) = {cc:+.3f}  "
      f"(H_scale predicts a POSITIVE corr: a deeper book, DD0 more negative, pays a more "
      f"negative tax)")
    # LADDER-level sign test: one vote per ladder, read at its LARGEST m.  Immune to the
    # pooled count being dominated by whichever script swept the most cells.
    gcols = [c for c in ("file", "group", "ddcol", "panel", "n") if c in d.columns]
    if gcols:
        tips = d.sort_values("m").groupby(gcols, dropna=False).tail(1)
        w = (tips.dDD < -1e-12).mean(); b_ = (tips.dDD > 1e-12).mean()
        P(f"    [{label}] LADDER-level (one vote per ladder at its largest m): "
          f"{len(tips)} ladders, worsens DD {w:.1%} | improves {b_:.1%} | "
          f"median {tips.dDD.median():+.4f} ({tips.dDD.median()*1e4:+.1f} bp)")
        if "file" in d.columns and d.file.nunique() > 1:
            per = d.groupby("file").dDD.agg(["count", "median"]).sort_values("count",
                                                                            ascending=False)
            per["median_bp"] = per["median"] * 1e4
            P(f"    [{label}] per-script medians (no single script drives the pooled sign):")
            P(per[["count", "median_bp"]].to_string(float_format=lambda x: f"{x:.1f}"))
    return lv


# ================================================================ [B] direct measurement
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    return px[keep]


def rank_frame(px):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    return s.where(above & (vol20 < MAX_VOL) & px.notna()).rank(axis=1, ascending=False)


def sel_hard(rk, n):
    return rk <= n


def sel_band(px, rk, n, m, freq=FREQ):
    """idea 273/331's no-trade band, verbatim.  m = 0 nests sel_hard(n) (gated in G3)."""
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    held, last = [], np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n + m]
            held.sort(key=lambda j: r[j])
            if len(held) > cap:
                held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs = set(held)
                for j in order:
                    if len(held) >= cap:
                        break
                    if r[j] != r[j]:
                        break
                    if j not in hs:
                        held.append(j); hs.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols)); last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel, gross=GROSS):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, freq=FREQ):
    """Clone of engine.backtest returning GROSS returns and turnover so every cost rung is
    derived from one run (gated exactly against engine.backtest in G1/G2)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT); cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(np.nansum(held * rets, axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series((held > 0).sum(axis=1), index=idx))


def stats(gross_r, turn, bps, start):
    r = (gross_r - turn * bps / 1e4).loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o, i_ = r.loc[OOS_START:], r.loc[:IS_END]
    mo, mi = metrics(o), metrics(i_)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"], IS_Sharpe=mi["Sharpe"])


def keeps(s, v2, spy):
    """PROTOCOL 4a and 4b, evaluated as conjunctions; returns (pass4a, pass4b, failed bars)."""
    a = s["H1"] > v2["H1"] and s["H2"] > v2["H2"] and s["MaxDD"] >= v2["MaxDD"]
    fb = []
    if not s["H1"] > spy["H1"]: fb.append("H1")
    if not s["H2"] > spy["H2"]: fb.append("H2")
    if not s["OOS_Sharpe"] > spy["OOS_Sharpe"]: fb.append("OOS")
    if not s["MaxDD"] >= -0.60 * abs(spy["MaxDD"]): fb.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fb.append("CAGR")
    return a, len(fb) == 0, ",".join(fb)


def main():
    P(f"# {SLUG}")
    cen = archive_census()
    if not cen.empty:
        P("\n[A1] SHAPE OF THE TAX — no-trade band `m` (the question's instrument)")
        lv_m = tax_shape(cen[(cen.dial == "m") & (cen.kind == "INT")], "archive m")
        P("\n[A2] CONTRAST — `band` (200d MA width; a different instrument, NOT pooled)")
        tax_shape(cen[(cen.dial == "band") & (cen.kind == "FRAC")], "archive band (MA width)")
        if lv_m is not None:
            lv_m.to_csv(OUT / f"{SLUG}.archive_shape.csv", index=False)

    P("\n[B] DIRECT MEASUREMENT — 3 panels x n{10,20,40} x m{0,5,10,20,40}, g=0.75, weekly")
    u = load_universe(); b = load_universe(broad=True); sm = small_panel()
    panels = [("U56", u), ("B136", b), ("SMALL439", sm)]
    for nm, px in panels:
        P(f"    {nm}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}")

    # ---- gates on U56
    P("\n[0] GATES")
    rk_u = rank_frame(u)
    w_g = weights_from(sel_hard(rk_u, 20))
    gr, tn, _ = fast_backtest(u, w_g)
    for bps in (0, 25):
        eng = backtest(u, w_g, cost_bps=bps, freq=FREQ)
        d1 = float((eng["returns"] - (gr - tn * bps / 1e4)).abs().max())
        d2 = float((eng["turnover"] - tn).abs().max())
        P(f"    G1/G2 cost_bps={bps:>2}: |d returns| {d1:.3e}   |d turnover| {d2:.3e}")
        assert d1 < 1e-12 and d2 < 1e-12
    reb = rebalance_mask(u.index, FREQ)
    sb0 = sel_band(u, rk_u, 20, 0)
    dh = int((sb0.loc[reb.values] != sel_hard(rk_u, 20).fillna(False).loc[reb.values]).values.sum())
    P(f"    G3 sel_band(m=0) vs sel_hard on every rebalance day: {dh} disagreements")
    assert dh == 0

    rk_b = rank_frame(b)
    grb, tnb, nmb = fast_backtest(b, weights_from(sel_hard(rk_b, 20)))
    s_ref = stats(grb, tnb, 10, b.index[WARMUP])
    tgt = dict(CAGR=0.12992958836952506, Sharpe=0.9431848997615343, MaxDD=-0.2005204833110832,
               H1=1.1047866702854354, H2=0.8025166021122436, OOS_Sharpe=0.8836022780725372)
    dmax = max(abs(s_ref[k] - v) for k, v in tgt.items())
    P(f"    G4 (B136,n=20,g=0.75,m=0,W) vs idea 333's committed grid row: max |d| {dmax:.3e} "
      f"over {len(tgt)} statistics")
    assert dmax < 1e-9

    # ---- comparands
    comp = {}
    for nm, px in panels:
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        h = len(spy) // 2
        sp = dict(CAGR=metrics(spy)["CAGR"], Sharpe=metrics(spy)["Sharpe"],
                  MaxDD=metrics(spy)["MaxDD"], H1=metrics(spy.iloc[:h])["Sharpe"],
                  H2=metrics(spy.iloc[h:])["Sharpe"],
                  OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                  OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                  OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"])
        v2r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"]
        v2 = stats(v2r, pd.Series(0.0, index=px.index), 0, start)
        comp[nm] = (sp, v2, start)
        P(f"    {nm} comparands @10bps: SPY Sharpe {sp['Sharpe']:.3f} (H1 {sp['H1']:.3f} / "
          f"H2 {sp['H2']:.3f}, OOS {sp['OOS_Sharpe']:.3f}, MaxDD {sp['MaxDD']:.3f}, "
          f"CAGR {sp['CAGR']:.3%}) | RULES v2 Sharpe {v2['Sharpe']:.3f} "
          f"(H1 {v2['H1']:.3f} / H2 {v2['H2']:.3f}, MaxDD {v2['MaxDD']:.3f})")

    # ---- degeneracy: on a narrow panel a large m is not a band at all
    P("\n[B0] DEGENERACY CHECK — n + m vs the panel's own eligible-name ceiling")
    ranks = {"U56": rk_u, "B136": rk_b, "SMALL439": rank_frame(sm)}
    ceil = {}
    for nm, px in panels:
        ceil[nm] = float(ranks[nm].max(axis=1).loc[px.index[WARMUP]:].max())
        P(f"    {nm}: max eligible names on any day = {ceil[nm]:.0f}; cells with "
          f"n + m > {ceil[nm]:.0f} are the HOLD-UNTIL-INELIGIBLE limit (m = inf), not a band")

    # ---- the grid
    P("\n[B1] the 45-cell grid (all cells, all three rungs, in the .grid.csv)")
    rows = []
    for nm, px in panels:
        sp, v2, start = comp[nm]
        yrs = len(px.loc[start:]) / 252
        for n in NS:
            for m in MS:
                sel = sel_band(px, ranks[nm], n, m)
                gr, tn, nmz = fast_backtest(px, weights_from(sel))
                row = dict(panel=nm, n=n, m=m, gross=GROSS, cadence=FREQ,
                           degenerate=bool(n + m > ceil[nm]),
                           turn_per_yr=float(tn.loc[start:].sum() / yrs),
                           names=float(nmz.loc[start:].mean()))
                for bps in COSTS:
                    s = stats(gr, tn, bps, start)
                    a, bkeep, fb = keeps(s, v2, sp)
                    for k, v in s.items():
                        row[f"{k}_{bps}"] = v
                    row[f"pass4a_{bps}"], row[f"pass4b_{bps}"], row[f"fail4b_{bps}"] = a, bkeep, fb
                    row[f"m4b_DD_{bps}"] = s["MaxDD"] - (-0.60 * abs(sp["MaxDD"]))
                    row[f"m4b_CAGR_{bps}"] = s["CAGR"] - 0.70 * sp["CAGR"]
                rows.append(row)
        P(f"    {nm} done")
    g = pd.DataFrame(rows)
    g.to_csv(OUT / f"{SLUG}.grid.csv", index=False)

    # ---- the tax on the clean grid
    P("\n[B2] dMaxDD(m) on the clean grid (vs the m=0 anchor of the same panel and n), 10 bps")
    tx = []
    for (nm, n), gg in g.groupby(["panel", "n"]):
        gg = gg.sort_values("m")
        base = gg[gg.m == 0].iloc[0]
        for _, r in gg[gg.m > 0].iterrows():
            tx.append(dict(panel=nm, n=n, m=r.m, DD0=base.MaxDD_10, DD=r.MaxDD_10,
                           dDD=r.MaxDD_10 - base.MaxDD_10,
                           ratio=(r.MaxDD_10 - base.MaxDD_10) / abs(base.MaxDD_10),
                           dTO=r.turn_per_yr - base.turn_per_yr,
                           dSharpe=r.Sharpe_10 - base.Sharpe_10,
                           dCAGR=r.CAGR_10 - base.CAGR_10,
                           dOOS_DD=r.OOS_MaxDD_10 - base.OOS_MaxDD_10))
    tx = pd.DataFrame(tx)
    tx["bp_per_turn"] = np.where(tx.dTO.abs() > 1e-9, tx.dDD * 1e4 / -tx.dTO, np.nan)
    tx.to_csv(OUT / f"{SLUG}.tax.csv", index=False)
    P(tx.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    tax_shape(tx.rename(columns={"dDD": "dDD"}), "fresh grid @10bps")
    P(f"\n    EXCHANGE RATE (the band buys turnover with drawdown): median "
      f"{np.nanmedian(tx.bp_per_turn):+.2f} bp of MaxDD per 1.0x/yr of turnover removed; "
      f"IQR [{np.nanpercentile(tx.bp_per_turn,25):+.2f}, {np.nanpercentile(tx.bp_per_turn,75):+.2f}]")
    P(f"    turnover actually removed: median {tx.dTO.median():+.2f}x/yr "
      f"(range {tx.dTO.min():+.2f} .. {tx.dTO.max():+.2f})")
    P(f"    CONTRAST — what the band DOES do: dSharpe > 0 at "
      f"{int((tx.dSharpe > 0).sum())}/{len(tx)} cells (median {tx.dSharpe.median():+.4f}, "
      f"min {tx.dSharpe.min():+.4f}); dCAGR > 0 at {int((tx.dCAGR > 0).sum())}/{len(tx)} "
      f"(median {tx.dCAGR.median():+.4f}); dMaxDD > 0 at "
      f"{int((tx.dDD > 0).sum())}/{len(tx)}.  A SIGNED cost instrument with an UNSIGNED "
      f"drawdown effect.")
    dg = tx.merge(g[["panel", "n", "m", "degenerate"]], on=["panel", "n", "m"], how="left")
    P(f"    of the {len(dg)} band cells, {int(dg.degenerate.sum())} are DEGENERATE "
      f"(n + m past the panel's eligible ceiling); on the non-degenerate "
      f"{int((~dg.degenerate).sum())}: dMaxDD > 0 at {int((dg[~dg.degenerate].dDD > 0).sum())}"
      f", median {dg[~dg.degenerate].dDD.median()*1e4:+.1f} bp, dSharpe > 0 at "
      f"{int((dg[~dg.degenerate].dSharpe > 0).sum())}")

    # idea 333's own cell, re-priced
    c = tx[(tx.panel == "B136") & (tx.n == 20) & (tx.m == 20)]
    if len(c):
        r = c.iloc[0]
        P(f"    idea 333's own cell (B136, n=20, m=0 -> m=20): dMaxDD {r.dDD:+.4f} "
          f"({r.dDD*1e4:+.1f} bp), DD0 {r.DD0:.4f} -> {r.DD:.4f}")
    b136 = g[(g.panel == "B136") & (g.n == 20)][["m", "MaxDD_10", "m4b_DD_10", "turn_per_yr"]]
    P("    idea 333's DD-cap margin along m (B136, n=20, @10bps):")
    P(b136.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- KEEP paths
    P("\n[B3] KEEP paths over all 45 cells")
    for bps in COSTS:
        P(f"    @{bps:>2} bps: 4a {int(g[f'pass4a_{bps}'].sum())}/{len(g)}   "
          f"4b {int(g[f'pass4b_{bps}'].sum())}/{len(g)}")
    k4b = g[g.pass4b_10]
    if len(k4b):
        P("    4b passes @10 bps:")
        P(k4b[["panel", "n", "m", "CAGR_10", "Sharpe_10", "MaxDD_10", "H1_10", "H2_10",
               "OOS_Sharpe_10", "turn_per_yr"]].to_string(index=False,
                                                          float_format=lambda x: f"{x:.4f}"))
    else:
        P("    no cell passes 4b at 10 bps")

    # ---- rule 8
    P("\n[B4] RULE 8 WALK-FORWARD — (n, m) chosen on IS 2008-2016 Sharpe @10bps, OOS read once")
    wf = []
    for nm, px in panels:
        sp, v2, start = comp[nm]
        sub = g[g.panel == nm]
        pick = sub.loc[sub.IS_Sharpe_10.idxmax()]
        best = sub.loc[sub.OOS_Sharpe_10.idxmax()]
        anchor = sub[(sub.n == 20) & (sub.m == 0)].iloc[0]
        wf.append(dict(panel=nm, pick_n=pick.n, pick_m=pick.m, IS_Sharpe=pick.IS_Sharpe_10,
                       OOS_Sharpe=pick.OOS_Sharpe_10, OOS_CAGR=pick.OOS_CAGR_10,
                       OOS_MaxDD=pick.OOS_MaxDD_10, anchor_OOS_Sharpe=anchor.OOS_Sharpe_10,
                       best_n=best.n, best_m=best.m, best_OOS_Sharpe=best.OOS_Sharpe_10,
                       regret=best.OOS_Sharpe_10 - pick.OOS_Sharpe_10,
                       spy_OOS_Sharpe=sp["OOS_Sharpe"], spy_OOS_CAGR=sp["OOS_CAGR"],
                       spy_OOS_MaxDD=sp["OOS_MaxDD"], v2_OOS_Sharpe=v2["OOS_Sharpe"],
                       v2_OOS_CAGR=v2["OOS_CAGR"], v2_OOS_MaxDD=v2["OOS_MaxDD"],
                       pick_pass4b=bool(pick.pass4b_10), pick_fail4b=pick.fail4b_10))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    P(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"    the IS chooser picks m={list(wfd.pick_m)} on {list(wfd.panel)} "
      f"(m=0 means the band is NOT chosen out of sample)")
    P("    ROBUSTNESS (reported, not a re-tune): the same chooser restricted to "
      "NON-DEGENERATE cells only")
    for nm, px in panels:
        sub = g[(g.panel == nm) & (~g.degenerate)]
        if not len(sub):
            P(f"      {nm}: no non-degenerate cell"); continue
        pk = sub.loc[sub.IS_Sharpe_10.idxmax()]
        P(f"      {nm}: picks n={pk.n} m={pk.m} -> OOS Sharpe {pk.OOS_Sharpe_10:.4f}, "
          f"OOS CAGR {pk.OOS_CAGR_10:.4f}, OOS MaxDD {pk.OOS_MaxDD_10:.4f}, "
          f"4b {'PASS' if pk.pass4b_10 else 'FAIL (' + pk.fail4b_10 + ')'}")

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {SLUG}.{{census,archive_shape,grid,tax,walkforward}}.csv + console.txt")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
