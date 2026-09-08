#!/usr/bin/env python3
"""Idea 470 - "does-the-matched-gross-control-belong-on-every-published-DIAL-not-just-count"
(lane C, 2026-09-08).

The question
------------
Idea 244 established, for COUNT dials, that (a) a sweep whose weighting convention is
`GROSS/n` is exactly the equal-weighted book times a breadth-timed exposure overlay
phi_t = n_held(t)/n, so a "width" sweep moves the book's average exposure as well as its
width, and (b) matching mean realised gross is NECESSARY but NOT SUFFICIENT: 7 of 10 4b
passes on a FIXED count grid do not survive the matched control.

QUEUE 470 asks whether that control belongs on every published DIAL, not only count:

    Q1 (CENSUS, the deliverable): census the record's NON-COUNT dials -- band width, vol
       cap, cadence, thresholds, partial-rebalance lambda -- for a realised-gross span
       across their own published grid.  How many carry the same confound, and how many
       cannot even be adjudicated because their own artefact never published a gross
       column?
    Q2 (LIVE MEASUREMENT): the census can only read what was written down.  So measure
       the gross span DIRECTLY on four non-count dial families implemented on three
       panels, under the live book's own de-gross-to-cash convention, and report the span
       family by family.
    Q3 (MATCHED CONTROL): re-price every one of those dial points against the idea-244
       control -- the ADOPTED book scaled by ONE scalar to the dial point's own mean
       realised gross -- and report how many published-style readings (dSharpe, dCAGR,
       dMaxDD, and the 4a/4b passes) survive it.
    Q4 (RULE 8): does an IS-chosen dial value beat its own matched-gross control, the
       adopted value, RULES v2 and SPY out of sample?

Pre-registered definitions (written before any number in this run was read)
--------------------------------------------------------------------------
REALISED GROSS g(t) = the row sum of `engine.backtest`'s HELD weight frame, i.e. after
    drift, not the target.  A cell's gross is the MEAN of g(t) over the evaluated sample
    (or over the IS window where stated).  Cash is credited at 0, the record's standing
    convention (see QUEUE 406, still open); the whole run is therefore a comparison of
    books at the SAME mean gross, which is the one comparison that convention cannot bias.

LABEL-DECIDABILITY: a census cell is label-decidable when its dial column names ONE
    object across the record.  The column `m` does not (it is a gross multiplier in
    `2026-09-05_gross-as-the-missing-third-bar_B` and a no-trade band in QUEUE 328), so it
    is carried as its own family `M?`, counted in every denominator, and the headline rate
    is quoted as a BOUND over it rather than guessed.  Margin columns (the record's `m_`
    prefix, e.g. `m_GROSS`) are NOT gross levels and are excluded from the gross-column
    list; reading one as a level is a mistake this run made on its first pass and corrected.

GROSS-LADDER POINT: a published dial sweep whose realised-gross SPAN across its own
    quoted grid is >= 0.05 of NAV (5 pp).  This is idea 244's threshold, adopted verbatim
    so the two censuses are comparable; the relative companion (span / mean gross >= 0.10)
    is reported beside it and the FULL span distribution is written to `.census.csv`, so
    any other threshold can be read off the table rather than taken on trust.

THE MATCHED PAIR (the idea-244 control, transported to a non-count dial).  For dial
    family F on panel P with ADOPTED value a and grid point p, the pair is
        PAIR-DIAL  the book at p,   scaled by min(1, meang(a)/meang(p))
        PAIR-CTRL  the book at a,   scaled by min(1, meang(p)/meang(a))
    i.e. whichever of the two runs at the HIGHER mean realised gross is scaled DOWN to the
    other's, and the lower one is left alone.  Both then sit at the same mean gross, so
    anything left between them is the dial's TIMING and SELECTION and not its exposure
    LEVEL.  Scaling down only is what keeps PROTOCOL rule 2 (no leverage) at gross 1.00,
    where scaling the adopted book UP to a wider point's gross would lever it; it also
    means no point is ever dropped for being unmatchable.  One scalar per (panel, gross,
    family, point), computed on the FULL sample for the full-sample tables and on the IS
    window ONLY for the rule-8 arm.  Realised match error is printed for every point.
    RAW is the point as a sweep would publish it -- unscaled -- and is what the 4a/4b
    pass counts are read from.

GROSS AXIS (declared, and declared as a change of mind).  This run's first pass fixed
    GROSS = 0.75, the live book's level, and returned 0 4b passes on all 63 points, which
    makes "how many 4b passes survive the control?" vacuous rather than answered -- the
    record's 4b passers are known to live at gross 1.00 (ideas 441/444: all 54 passes at
    gross 1.00, none at 0.75).  The grid was therefore re-run over gross in {0.75, 1.00}
    as a REPORTING axis, exactly as the cost rung is, with every point printed at both
    levels.  It is not a third tuned parameter: nothing is chosen on it, both levels are
    always reported, and the dial value and panel remain the only two things any arm in
    this run selects on.  Recording the reason here, rather than presenting the two-level
    grid as the original design, is the honest form.

ADOPTED values (the live book / RULES v2 and v1, fixed before the run): band 0.03,
    ma 200, max_vol 0.60, cadence W.

The four live dial families.  All four deform ONE base book -- the record's live shape:
every name inside the 200d +/-3% band held at GROSS/N of NAV, N = instruments priced that
day, gated-out weight to CASH (never re-spread), weekly, GROSS = 0.75.
    BAND     band in {0.00, 0.01, 0.03, 0.06, 0.10, 0.15}      (adopted 0.03)
    MA       trend-gate length in {50, 100, 150, 200, 300}      (adopted 200)
    VOLCAP   max_vol in {0.25, 0.40, 0.60, 0.90, 1.50, inf}     (adopted 0.60)
    CADENCE  freq in {D, W, M, Q}                               (adopted W)
CADENCE is carried deliberately as the family that CANNOT move mean target gross (it
changes only the rebalance schedule, so gross moves through drift alone).  It is the
run's negative control: if the confound is a property of dials in general rather than of
gating dials specifically, cadence must show a span too.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (3: U56, B136, SMALL439)      2. the dial value (4-6 levels per family)
FAMILY is a reported axis, not a third tuned dial: all four families are run on every
panel and ALL points are printed.  Cost rung (10 / 25 bps) is a reporting axis derived
from the same held/turnover paths, not a fitted choice.
Live grid = 3 panels x 2 gross x 21 dial points x 3 arms (RAW, PAIR-DIAL, PAIR-CTRL)
= 378 points, + references (RULES v2 and EWALL at each gross, RULES v1, SPY), ALL written
to `.grid.csv` at both cost rungs.

Walk-forward (PROTOCOL rule 8) -- arms and directions fixed before any OOS number
    IS = 2009-2016 (through 2016-12-31), OOS = 2017-2026, read once.
    ISARGMAX-RAW      dial value = argmax IS Sharpe within the family (the dial as published)
    ISARGMAX-PAIRDIAL the same pick, de-grossed to the adopted book's IS mean gross
    ISARGMAX-MATCHED  the adopted book, de-grossed to the pick's IS mean gross
    ADOPTED           the live dial value (do-nothing within the family)
    NOTHING           RULES v2 on the same panel (the live book)
    EWALL             un-gated equal weight at the same GROSS (no dial at all)
    SPY               buy and hold

Verdicts (both KEEP paths, every live point, PROTOCOL rule 4)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: every panel is CURRENT constituents (universe.json / universe_broad.json /
the sub-$2B screen), one-directional and hardest on SMALL439.  The census additionally
inherits the bias of every parent script it reads.  The headline of this run is a
CONVENTION statistic (gross span) and a CONTROL statistic (what survives matching), not a
return claim, which is what makes it readable despite the bias.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import re
import numpy as np
import pandas as pd
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state
from engine import backtest, metrics

COST_RUNGS = (10, 25)
COST_BPS = 10
GROSS = 0.75
ADOPTED = {"BAND": 0.03, "MA": 200, "VOLCAP": 0.60, "CADENCE": "W"}
GRIDS = {
    "BAND":    [0.00, 0.01, 0.03, 0.06, 0.10, 0.15],
    "MA":      [50, 100, 150, 200, 300],
    "VOLCAP":  [0.25, 0.40, 0.60, 0.90, 1.50, np.inf],
    "CADENCE": ["D", "W", "M", "Q"],
}
GROSS_AXIS = (0.75, 1.00)          # reporting axis, NOT a tuned parameter -- see docstring
CACHE, REFS = {}, {}               # (panel, gross, family, value) -> run; (panel, gross) -> refs
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SPAN_ABS = 0.05
SPAN_REL = 0.10
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- panels
def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    dropped = pxs.shape[1] - len(keep)
    pxs = pxs[keep]
    panels = {
        "U56":      (px56, set(px56.columns)),
        "B136":     (px136, set(px136.columns)),
        # idea 243's by-product: SPY is joined as a BENCHMARK on the small panel and is
        # excluded from the tradable set here, so it is never held.
        "SMALL439": (pxs, set(c for c in pxs.columns if c != "SPY")),
    }
    return panels, dropped


# ---------------------------------------------------------------- the four dial families
def _gate(px, band, ma_len):
    """200d-style band gate with hysteresis, generalised to an arbitrary MA length."""
    ma = px.rolling(ma_len).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def _vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def base_weights(px, tradable, band=0.03, ma_len=200, max_vol=np.inf, gross=GROSS):
    """The live shape: gross/N of NAV on every name inside the band (and under the vol
    cap), N = instruments priced that day; gated-out weight goes to CASH."""
    priced = px.notna()
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(priced, 0.0)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        e[drop] = 0.0
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    keep = _gate(px, band, ma_len)
    if np.isfinite(max_vol):
        keep = keep & (_vol20(px) < max_vol)
    return ew.where(keep, 0.0)


def ewall_weights(px, tradable, gross=GROSS):
    priced = px.notna()
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(priced, 0.0)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        e[drop] = 0.0
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def dial_weights(px, tradable, family, value, gross=GROSS):
    """One deformation of the base book per family; every other dial at its ADOPTED value."""
    kw = dict(band=ADOPTED["BAND"], ma_len=ADOPTED["MA"], max_vol=ADOPTED["VOLCAP"],
              gross=gross)
    if family == "BAND":
        kw["band"] = value
    elif family == "MA":
        kw["ma_len"] = value
    elif family == "VOLCAP":
        kw["max_vol"] = value
    elif family != "CADENCE":                 # CADENCE: weights identical, only the schedule moves
        raise ValueError(family)
    return base_weights(px, tradable, **kw)


def pick_val(family, key):
    """Map a stringified grid key back to the grid value it came from."""
    for v in GRIDS[family]:
        if str(v) == key:
            return v
    raise KeyError((family, key))


def dial_freq(family, value):
    return value if family == "CADENCE" else "W"


# ---------------------------------------------------------------- run harness
def run(px, w, freq="W"):
    """One backtest -> gross path, turnover, held gross. Cost applied afterwards because
    engine.backtest's held/turnover paths do not depend on cost_bps."""
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return dict(gret=res["returns"], turn=res["turnover"], hg=res["weights"].sum(axis=1))


def net(r, bps, sl=None):
    x = r["gret"] - r["turn"] * bps / 1e4
    return x if sl is None else x.loc[sl]


def half_sharpes(x):
    h = len(x) // 2
    return metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"]


def fail_4a(r, base):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


# ================================================================ Q1: the census
# Pre-registered NON-COUNT dial columns, by family.  COUNT columns (idea 244's list) and
# bare GROSS-LEVEL columns are EXCLUDED by construction: the gross dial is the confound
# itself, not a candidate for it, and it is reported separately as a positive control.
#
# `m` is NOT in BAND.  A pre-check on this run's own first pass found the record uses the
# column name `m` for at least two different objects: a GROSS MULTIPLIER (verified in
# `2026-09-05_gross-as-the-missing-third-bar_B.ladder.csv`, where m runs 0.10 -> 1.00 and
# the file's own `gross` column runs 0.075 -> 0.750 beside it) and a no-trade BAND in bps
# (QUEUE 328).  Two pre-registered source regexes were tried and BOTH mislabel the
# verified instance, so `m` is carried as its own UNDECIDABLE family, counted in every
# denominator and EXCLUDED from the headline, which is quoted as a bound over it.  This is
# idea 469's open problem in a second column and it is reported, not guessed away.
DIAL_COLS = {
    "BAND":    ("band", "band_pct", "bandwidth", "width", "hyst"),
    "M?":      ("m",),
    "VOLCAP":  ("max_vol", "volcap", "vol_cap", "vol_max", "maxvol"),
    "CADENCE": ("freq", "cadence", "rebal", "rebal_freq", "every_n", "period"),
    "THRESH":  ("q", "quantile", "tau", "thresh", "threshold", "floor", "dd_cap",
                "DD_cap", "stop", "budget", "ebud", "cut"),
    "PARTIAL": ("lam", "lambda", "lam_", "partial"),
    "MALEN":   ("ma", "ma_len", "malen", "ma_days", "lookback", "win", "w"),
}
COUNT_COLS = ("n", "top_n", "topn", "n_names", "npos", "n_pos", "count", "nn", "k", "K")
GROSS_DIAL_COLS = ("gross", "g", "gross_level", "target_gross", "nominal_gross", "max_gross")
# Columns that are unambiguously a REALISED (post-drift) gross measurement.
# `m_GROSS` / `IS_m_GROSS` are deliberately NOT here: the record's `m_` prefix is a MARGIN
# against a bar, not a level (verified: `2026-09-05_gross-as-the-missing-third-bar_B`
# publishes m_GROSS = -0.425 .. +0.250 beside gross = 0.075 .. 0.750).  Reading a margin
# as a level is what a first pass of this run did, and it inflated the ladder count.
REALISED_GROSS_COLS = ("mean_gross", "gross_mean", "realised_gross", "real_gross",
                       "gross_real", "held_gross", "hg", "realized_gross",
                       "IS_gross", "gross_mean_IS", "OOS_gross", "gross_mean_OOS",
                       "pick_gross", "ctl_gross", "lad_gross", "parent_gross",
                       "gross_parent")
AMBIG_GROSS_COLS = ("gross", "Gross")            # design level OR realised, unknowable
SHARPE_COLS = ("Sharpe", "OOS_Sharpe", "IS_Sharpe", "mean_OOS_Sharpe", "sharpe",
               "Sharpe_10", "Sharpe_25", "dSharpe")
PANEL_COLS = ("panel", "universe", "corpus", "book", "panel_name", "uni")


def census():
    cells, rejects = [], []
    files_scanned = 0
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM):
            continue
        files_scanned += 1
        try:
            df = pd.read_csv(f)
        except Exception as e:
            rejects.append(dict(file=f.name, col="", reason=f"unreadable:{type(e).__name__}"))
            continue
        if df.empty:
            rejects.append(dict(file=f.name, col="", reason="empty"))
            continue
        fam_of = {}
        for fam, cols in DIAL_COLS.items():
            for c in cols:
                if c in df.columns and c not in COUNT_COLS and c not in GROSS_DIAL_COLS:
                    fam_of.setdefault(c, fam)
        if not fam_of:
            continue
        scols = [c for c in SHARPE_COLS if c in df.columns]
        rg = [c for c in REALISED_GROSS_COLS if c in df.columns]
        ag = [c for c in AMBIG_GROSS_COLS if c in df.columns]
        pcol = next((p for p in PANEL_COLS if p in df.columns), None)
        for c, fam in sorted(fam_of.items()):
            vals = df[c].astype(str)
            nuniq = vals.nunique()
            if nuniq < 3:
                rejects.append(dict(file=f.name, col=c, reason=f"<3 distinct values ({nuniq})"))
                continue
            if not scols:
                rejects.append(dict(file=f.name, col=c, reason="no Sharpe column beside it"))
                continue
            groups = df.groupby(df[pcol].astype(str)) if pcol else [("(all)", df)]
            for pk, g in groups:
                if g[c].astype(str).nunique() < 3:
                    continue
                row = dict(file=f.name, dial_col=c, family=fam, panel_raw=str(pk),
                           n_levels=int(g[c].astype(str).nunique()),
                           sharpe_cols=",".join(scols))
                for tag, cand in (("real", rg), ("ambig", ag)):
                    if cand:
                        gc = cand[0]
                        s = pd.to_numeric(g[gc], errors="coerce")
                        per = pd.DataFrame({"d": g[c].astype(str), "gr": s}).dropna()
                        if per["d"].nunique() >= 3:
                            mu = per.groupby("d")["gr"].mean()
                            row[f"{tag}_col"] = gc
                            row[f"{tag}_span"] = float(mu.max() - mu.min())
                            row[f"{tag}_mean"] = float(mu.mean())
                            continue
                    row[f"{tag}_col"] = ""
                    row[f"{tag}_span"] = np.nan
                    row[f"{tag}_mean"] = np.nan
                row["status"] = ("QUOTED-REAL" if row["real_col"] else
                                 "QUOTED-AMBIG" if row["ambig_col"] else "UNQUOTED")
                cells.append(row)
    return pd.DataFrame(cells), pd.DataFrame(rejects), files_scanned


# ================================================================ main
def main():
    panels, small_dropped = build_panels()
    print("=" * 200)
    print(f"Idea 470 does-the-matched-gross-control-belong-on-every-published-DIAL-not-just-count "
          f"(lane C) | {SCRIPT}")
    print(f"{COST_BPS} bps headline (+25 bps rung), next-day execution, GROSS={GROSS}, "
          f"cash credited at 0 (record convention)")
    print("=" * 200)
    px0 = panels["U56"][0]
    yrs = px0.index.to_series().groupby(px0.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, "
          f"2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
    print(f"small panel hygiene: dropped {small_dropped} tickers with max_1d_move >= 1.0; "
          f"{len(panels['SMALL439'][1])} tradable remain (SPY joined as benchmark only)")

    # ------------------------------------------------------------ HARNESS CHECKS
    print("\n" + "=" * 200)
    print("HARNESS CHECKS (run before any result is read)")
    print("=" * 200)
    pxc, trc = panels["U56"]
    w_ours = base_weights(pxc, trc, band=0.03, ma_len=200, max_vol=np.inf)
    w_lib = rules_v2_weights(pxc, band=0.03, gross=GROSS)
    d1 = float((w_ours - w_lib).abs().to_numpy().max())
    print(f"[c1] base_weights(band=.03, ma=200, volcap=off) == baseline.rules_v2_weights : "
          f"max|dW| = {d1:.3e}   (must be ~0)")
    b_ours = _gate(pxc, 0.03, 200)
    b_lib = band_state(pxc, 0.03)
    print(f"[c2] _gate(band=.03, ma=200) == baseline.band_state                          : "
          f"disagreements = {int((b_ours != b_lib).to_numpy().sum())}   (must be 0)")
    r_free = run(pxc, w_lib)
    r_paid = backtest(pxc, w_lib, cost_bps=10.0, freq="W")["returns"]
    d3 = float((net(r_free, 10) - r_paid).abs().max())
    print(f"[c3] cost applied post-hoc == engine.backtest(cost_bps=10)                    : "
          f"max|dr| = {d3:.3e}   (must be ~0)")
    sc = 0.6
    r_sc = run(pxc, w_lib * sc)
    d4 = float((r_sc["hg"] - r_free["hg"] * sc).abs().max())
    print(f"[c4] scaling TARGET weights by c scales HELD gross by c EXACTLY at rebalance, "
          f"approximately under drift (cash is held at 0 and does not drift): "
          f"max|dg(t)| = {d4:.3e}")
    print(f"     the operative quantity is the MEAN gross the matched arm actually "
          f"realises; its error against the RAW point it matches is printed in Q3 "
          f"(and is in .grid.csv as match_err) rather than assumed.")

    # ------------------------------------------------------------ Q1 CENSUS
    print("\n" + "=" * 200)
    print("Q1 CENSUS - every committed CSV in research/backtests/ scanned for a NON-COUNT dial")
    print("=" * 200)
    cen, rej, nfiles = census()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    rej.to_csv(OUT / f"{STEM}.census_rejects.csv", index=False)
    print(f"files scanned {nfiles} | dial cells admitted {len(cen)} | rejections {len(rej)}")
    if len(rej):
        print("\nrejection reasons (top 12):")
        print(rej["reason"].str.replace(r"\(\d+\)", "(k)", regex=True).value_counts().head(12).to_string())
    if len(cen):
        print("\nadmitted cells by FAMILY x gross-column STATUS:")
        print(pd.crosstab(cen["family"], cen["status"], margins=True).to_string())
        q = cen[cen["status"] == "QUOTED-REAL"]
        a = cen[cen["status"] == "QUOTED-AMBIG"]
        for tag, sub, col in (("QUOTED-REAL", q, "real_span"), ("QUOTED-AMBIG", a, "ambig_span")):
            if len(sub):
                s = sub[col].dropna()
                lad = int((s >= SPAN_ABS).sum())
                rel = sub.dropna(subset=[col])
                relhit = int((rel[col] / rel[col.replace("span", "mean")].abs().replace(0, np.nan)
                              >= SPAN_REL).sum())
                print(f"\n{tag}: {len(sub)} cells, span measurable on {len(s)} | "
                      f"GROSS-LADDER (span >= {SPAN_ABS:.2f}) {lad}/{len(s)} = "
                      f"{lad/max(len(s),1):.1%} | relative (>= {SPAN_REL:.0%} of mean) "
                      f"{relhit}/{len(s)}")
                print(f"  span distribution: min {s.min():.4f} p25 {s.quantile(.25):.4f} "
                      f"median {s.median():.4f} p75 {s.quantile(.75):.4f} max {s.max():.4f}")
                if len(s):
                    by = sub.dropna(subset=[col]).groupby("family")[col].agg(
                        ["count", "median", "max", lambda x: (x >= SPAN_ABS).sum()])
                    by.columns = ["cells", "median_span", "max_span", "ladder"]
                    print(by.to_string(float_format=lambda x: f"{x:.4f}"))
        unq = int((cen["status"] == "UNQUOTED").sum())
        print(f"\nHEADLINE Q1: {unq} of {len(cen)} admitted non-count dial cells "
              f"({unq/max(len(cen),1):.1%}) publish NO gross column of any kind and cannot be "
              f"adjudicated from their own artefact. That is why Q2 measures the span directly.")
        dec = cen[cen["family"] != "M?"]
        und = cen[cen["family"] == "M?"]
        qd = dec[dec["status"] == "QUOTED-REAL"]["real_span"].dropna()
        qu = und[und["status"] == "QUOTED-REAL"]["real_span"].dropna()
        lo = int((qd >= SPAN_ABS).sum())
        hi = lo + int((qu >= SPAN_ABS).sum())
        den_lo, den_hi = len(qd), len(qd) + len(qu)
        print(f"HEADLINE Q1 (label-decidable only, `m` excluded): GROSS-LADDER "
              f"{lo}/{den_lo} = {lo/max(den_lo,1):.1%} of adjudicable cells; "
              f"including the {len(und)} UNDECIDABLE `m` cells the record-wide rate is "
              f"BOUNDED at {lo/max(den_hi,1):.1%}-{hi/max(den_hi,1):.1%} "
              f"({lo}-{hi} of {den_hi}).")

    # ------------------------------------------------------------ Q2/Q3 LIVE GRID
    print("\n" + "=" * 200)
    print("Q2/Q3 LIVE GRID - realised-gross span per dial family, and the idea-244 matched control")
    print("=" * 200)
    rows = []
    for pname, (px, tradable) in panels.items():
        start = px.index[260]
        sl = slice(start, None)
        oos = slice(OOS_START, None)
        ins = slice(start, IS_END)
        spy = px["SPY"].pct_change().fillna(0.0)
        r_v1 = run(px, rules_v1_weights(px))
        for G in GROSS_AXIS:
            ref = {}
            for fam in GRIDS:
                a = ADOPTED[fam]
                ref[fam] = run(px, dial_weights(px, tradable, fam, a, gross=G),
                               dial_freq(fam, a))
                CACHE[(pname, G, fam, str(a))] = ref[fam]
            r_v2 = run(px, rules_v2_weights(px, band=0.03, gross=G))
            r_ew = run(px, ewall_weights(px, tradable, gross=G))
            REFS[(pname, G)] = dict(v2=r_v2, ew=r_ew)
            for fam, grid in GRIDS.items():
                for v in grid:
                    key = (pname, G, fam, str(v))
                    rr = CACHE.get(key)
                    if rr is None:
                        rr = run(px, dial_weights(px, tradable, fam, v, gross=G),
                                 dial_freq(fam, v))
                        CACHE[key] = rr
                    g_p = float(rr["hg"].loc[sl].mean())
                    g_a = float(ref[fam]["hg"].loc[sl].mean())
                    # LEVERAGE-SAFE ANCHOR (PROTOCOL rule 2): both members of the matched
                    # pair are scaled DOWN to the LOWER of the two mean grosses, never up,
                    # so no control is ever levered and no point is dropped for being
                    # unmatchable.  The published-style reading (RAW) is the unscaled point.
                    c_dial = min(1.0, g_a / g_p) if g_p > 0 else np.nan
                    c_ctrl = min(1.0, g_p / g_a) if g_a > 0 else np.nan
                    rd = rr if c_dial >= 1.0 - 1e-12 else run(
                        px, dial_weights(px, tradable, fam, v, gross=G) * c_dial,
                        dial_freq(fam, v))
                    rc = ref[fam] if c_ctrl >= 1.0 - 1e-12 else run(
                        px, dial_weights(px, tradable, fam, ADOPTED[fam], gross=G) * c_ctrl,
                        dial_freq(fam, ADOPTED[fam]))
                    g_d = float(rd["hg"].loc[sl].mean())
                    g_c = float(rc["hg"].loc[sl].mean())
                    for arm, r_, gmean, merr in (("RAW", rr, g_p, 0.0),
                                                 ("PAIR-DIAL", rd, g_d, abs(g_d - g_c)),
                                                 ("PAIR-CTRL", rc, g_c, abs(g_d - g_c))):
                        for bps in COST_RUNGS:
                            x = net(r_, bps).loc[sl]
                            xo = net(r_, bps).loc[oos]
                            xi = net(r_, bps).loc[ins]
                            m = metrics(x)
                            h1, h2 = half_sharpes(x)
                            rows.append(dict(
                                panel=pname, gross=G, family=fam, value=str(v), arm=arm,
                                cost_bps=bps, mean_gross=gmean,
                                gross_sd=float(r_["hg"].loc[sl].std()), match_err=merr,
                                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                H1=h1, H2=h2,
                                IS_Sharpe=metrics(xi)["Sharpe"],
                                OOS_CAGR=metrics(xo)["CAGR"], OOS_Sharpe=metrics(xo)["Sharpe"],
                                OOS_MaxDD=metrics(xo)["MaxDD"],
                                turnover_yr=float(r_["turn"].loc[sl].sum() / m["Years"]),
                                fail4a=fail_4a(x, net(REFS[(pname, GROSS)]["v2"], bps).loc[sl]),
                                fail4b=fail_4b(x, spy.loc[sl], xo, spy.loc[oos]),
                                adopted=(str(v) == str(ADOPTED[fam]))))
            for nm, r_ in (("RULESv2", r_v2), ("EWALL", r_ew)):
                for bps in COST_RUNGS:
                    x = net(r_, bps).loc[sl]; xo = net(r_, bps).loc[oos]
                    m = metrics(x); h1, h2 = half_sharpes(x)
                    rows.append(dict(panel=pname, gross=G, family="REF", value=nm, arm="REF",
                                     cost_bps=bps, mean_gross=float(r_["hg"].loc[sl].mean()),
                                     gross_sd=float(r_["hg"].loc[sl].std()), match_err=0.0,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=h1, H2=h2,
                                     IS_Sharpe=metrics(net(r_, bps).loc[ins])["Sharpe"],
                                     OOS_CAGR=metrics(xo)["CAGR"],
                                     OOS_Sharpe=metrics(xo)["Sharpe"],
                                     OOS_MaxDD=metrics(xo)["MaxDD"],
                                     turnover_yr=float(r_["turn"].loc[sl].sum() / m["Years"]),
                                     fail4a=fail_4a(x, net(REFS[(pname, GROSS)]["v2"], bps).loc[sl]),
                                     fail4b=fail_4b(x, spy.loc[sl], xo, spy.loc[oos]),
                                     adopted=False))
        r_v2 = REFS[(pname, GROSS)]["v2"]
        for nm, r_ in (("RULESv1", r_v1),):
            for bps in COST_RUNGS:
                x = net(r_, bps).loc[sl]; xo = net(r_, bps).loc[oos]
                m = metrics(x); h1, h2 = half_sharpes(x)
                rows.append(dict(panel=pname, gross=GROSS, family="REF", value=nm, arm="REF",
                                 cost_bps=bps, mean_gross=float(r_["hg"].loc[sl].mean()),
                                 gross_sd=float(r_["hg"].loc[sl].std()), match_err=0.0,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                 IS_Sharpe=metrics(net(r_, bps).loc[ins])["Sharpe"],
                                 OOS_CAGR=metrics(xo)["CAGR"], OOS_Sharpe=metrics(xo)["Sharpe"],
                                 OOS_MaxDD=metrics(xo)["MaxDD"],
                                 turnover_yr=float(r_["turn"].loc[sl].sum() / m["Years"]),
                                 fail4a=fail_4a(x, net(r_v2, bps).loc[sl]),
                                 fail4b=fail_4b(x, spy.loc[sl], xo, spy.loc[oos]), adopted=False))
        ms = metrics(spy.loc[sl]); h1, h2 = half_sharpes(spy.loc[sl])
        rows.append(dict(panel=pname, gross=GROSS, family="REF", value="SPY", arm="REF",
                         cost_bps=0,
                         mean_gross=1.0, gross_sd=0.0, match_err=0.0, CAGR=ms["CAGR"],
                         Sharpe=ms["Sharpe"], MaxDD=ms["MaxDD"], H1=h1, H2=h2,
                         IS_Sharpe=metrics(spy.loc[ins])["Sharpe"],
                         OOS_CAGR=metrics(spy.loc[oos])["CAGR"],
                         OOS_Sharpe=metrics(spy.loc[oos])["Sharpe"],
                         OOS_MaxDD=metrics(spy.loc[oos])["MaxDD"], turnover_yr=0.0,
                         fail4a="", fail4b="", adopted=False))
        print(f"  {pname}: {px.shape[1]} cols, sample {start.date()} -> {px.index[-1].date()}")
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    g10 = grid[(grid["cost_bps"] == COST_BPS)]
    live = g10[(g10["arm"] == "RAW")]
    print("\nQ2 REALISED-GROSS SPAN per (panel, gross, family), 10 bps, full sample:")
    span = (live.groupby(["panel", "gross", "family"])["mean_gross"]
            .agg(["min", "max", "mean"]))
    span["span"] = span["max"] - span["min"]
    span["rel"] = span["span"] / span["mean"]
    span["LADDER"] = span["span"] >= SPAN_ABS
    print(span.to_string(float_format=lambda x: f"{x:.4f}"))
    nl = int(span["LADDER"].sum())
    print(f"\nHEADLINE Q2: {nl} of {len(span)} (panel x gross x family) non-count dials move "
          f">= {SPAN_ABS:.0%} of NAV of realised gross across their own grid.")
    print("per-family ladder count: " +
          ", ".join(f"{f} {int(span.xs(f, level='family')['LADDER'].sum())}/"
                    f"{len(span.xs(f, level='family'))}" for f in GRIDS))

    print("\nFULL LIVE TABLE (10 bps), every grid point, RAW beside its matched PAIR:")
    piv = g10[g10["arm"].isin(("RAW", "PAIR-DIAL", "PAIR-CTRL"))].pivot_table(
        index=["panel", "gross", "family", "value"], columns="arm",
        values=["mean_gross", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"])
    print(piv.to_string(float_format=lambda x: f"{x:.4f}"))

    print("\nQ3 THE MATCHED CONTROL - RAW minus MATCHED at the SAME mean realised gross:")
    IDX = ["panel", "gross", "family", "value", "cost_bps"]
    COLS = ["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "mean_gross"]
    gall = grid[grid["arm"].isin(("PAIR-DIAL", "PAIR-CTRL"))]
    d = (gall[gall["arm"] == "PAIR-DIAL"].set_index(IDX)[COLS]
         - gall[gall["arm"] == "PAIR-CTRL"].set_index(IDX)[COLS])
    d = d.rename(columns=lambda c: "d" + c).reset_index()
    d.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    merr = gall["match_err"].abs().max()
    print(f"max |mean_gross(PAIR-DIAL) - mean_gross(PAIR-CTRL)| over all points: {merr:.3e}")
    d = d[d["cost_bps"] == COST_BPS]
    off = d[~d.apply(lambda r: str(r["value"]) == str(ADOPTED[r["family"]]), axis=1)]
    print(f"\noff-adopted dial points (the ones a sweep is read from): {len(off)}")
    by = off.groupby("family")[["dCAGR", "dSharpe", "dMaxDD", "dOOS_Sharpe"]].agg(["mean", "median"])
    print(by.to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nsign counts (dial BEATS its own matched-gross control):")
    sg = pd.DataFrame({
        "n": off.groupby("family").size(),
        "dSharpe>0": off.assign(x=off["dSharpe"] > 0).groupby("family")["x"].sum(),
        "dCAGR>0": off.assign(x=off["dCAGR"] > 0).groupby("family")["x"].sum(),
        "dMaxDD>0(shallower)": off.assign(x=off["dMaxDD"] > 0).groupby("family")["x"].sum(),
        "dOOS>0": off.assign(x=off["dOOS_Sharpe"] > 0).groupby("family")["x"].sum()})
    print(sg.to_string())

    print("\n4a / 4b pass counts, RAW vs MATCHED, both rungs (all live points):")
    kp = (grid[grid["arm"].isin(("RAW", "PAIR-DIAL", "PAIR-CTRL"))]
          .assign(p4a=lambda x: x["fail4a"] == "-", p4b=lambda x: x["fail4b"] == "-")
          .groupby(["arm", "gross", "cost_bps"])[["p4a", "p4b"]].agg(["sum", "count"]))
    print(kp.to_string())
    KEY = ("panel", "gross", "family", "value", "cost_bps")
    r4 = grid[(grid["arm"] == "PAIR-DIAL") & (grid["fail4b"] == "-")]
    m4 = set(zip(*[grid[(grid["arm"] == "PAIR-CTRL") & (grid["fail4b"] == "-")][c] for c in KEY]))
    surv = [t for t in zip(*[r4[c] for c in KEY]) if t in m4]
    raw4 = grid[(grid["arm"] == "RAW") & (grid["fail4b"] == "-")]
    print(f"\nHEADLINE Q3: {len(raw4)} of {int((grid['arm'] == 'RAW').sum())} published-style "
          f"(RAW, unscaled) dial points pass 4b. Of the {len(r4)} matched-pair DIAL arms that "
          f"pass 4b, {len(surv)} have a matched-gross CONTROL that ALSO passes; "
          f"{len(r4) - len(surv)} are the dial's own, i.e. NOT explained by exposure alone.")
    if len(raw4):
        print("\nthe RAW 4b passers (10 bps only):")
        print(raw4[raw4["cost_bps"] == COST_BPS][list(KEY) + ["mean_gross", "CAGR", "Sharpe",
              "H1", "H2", "MaxDD", "OOS_Sharpe", "fail4a"]].to_string(
              index=False, float_format=lambda x: f"{x:.4f}"))
    if len(r4):
        print("binding 4b bars on RAW failures: " +
              str(pd.Series([b for s in grid[(grid['arm'] == 'RAW') & (grid['fail4b'] != '-')]['fail4b']
                             for b in s.split(",")]).value_counts().to_dict()))

    # ------------------------------------------------------------ Q4 RULE 8
    print("\n" + "=" * 200)
    print("Q4 RULE 8 WALK-FORWARD - dial value chosen on IS (<= 2016-12-31) Sharpe alone, "
          "2017-2026 read ONCE")
    print("=" * 200)
    wf = []
    for pname, (px, tradable) in panels.items():
        start = px.index[260]
        sl, ins, oos = slice(start, None), slice(start, IS_END), slice(OOS_START, None)
        spy = px["SPY"].pct_change().fillna(0.0)
        for G in GROSS_AXIS:
            r_v2, r_ew = REFS[(pname, G)]["v2"], REFS[(pname, G)]["ew"]
            for fam, gridv in GRIDS.items():
                cand = {str(v): CACHE[(pname, G, fam, str(v))] for v in gridv}
                for bps in COST_RUNGS:
                    is_sh = {k: metrics(net(r, bps).loc[ins])["Sharpe"] for k, r in cand.items()}
                    pick = max(is_sh, key=is_sh.get)
                    oos_sh = {k: metrics(net(r, bps).loc[oos])["Sharpe"] for k, r in cand.items()}
                    oracle = max(oos_sh, key=oos_sh.get)
                    rp = cand[pick]
                    ra = cand[str(ADOPTED[fam])]
                    # matched control for the PICK, scalar fitted on the IS window ONLY, and
                    # scaled DOWN only (leverage-safe anchor, as in the full-sample grid)
                    gi_p = float(rp["hg"].loc[ins].mean())
                    gi_a = float(ra["hg"].loc[ins].mean())
                    c_dial = min(1.0, gi_a / gi_p) if gi_p > 0 else np.nan
                    c_ctrl = min(1.0, gi_p / gi_a) if gi_a > 0 else np.nan
                    rpd = rp if c_dial >= 1.0 - 1e-12 else run(
                        px, dial_weights(px, tradable, fam, pick_val(fam, pick), gross=G) * c_dial,
                        dial_freq(fam, pick_val(fam, pick)))
                    rm = ra if c_ctrl >= 1.0 - 1e-12 else run(
                        px, dial_weights(px, tradable, fam, ADOPTED[fam], gross=G) * c_ctrl,
                        dial_freq(fam, ADOPTED[fam]))
                    arms = {"ISARGMAX-RAW": rp, "ISARGMAX-PAIRDIAL": rpd,
                            "ISARGMAX-MATCHED": rm, "ADOPTED": ra,
                            "NOTHING(RULESv2)": r_v2, "EWALL": r_ew,
                            "SPY": None}
                    for arm, r_ in arms.items():
                        if arm == "SPY":
                            xo = spy.loc[oos]; gm = 1.0
                        else:
                            xo = net(r_, bps).loc[oos]
                            gm = float(r_["hg"].loc[oos].mean())
                        wf.append(dict(panel=pname, gross=G, family=fam, cost_bps=bps, arm=arm,
                                       pick=pick, is_pick_sharpe=is_sh[pick],
                                       oos_oracle=oracle, pick_is_oracle=(pick == oracle),
                                       OOS_CAGR=metrics(xo)["CAGR"],
                                       OOS_Sharpe=metrics(xo)["Sharpe"],
                                       OOS_MaxDD=metrics(xo)["MaxDD"], OOS_gross=gm))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print("\nOOS by arm (mean over 3 panels x 2 gross x 4 families x 2 rungs = 48 cells):")
    print(wfd.groupby("arm")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_gross"]].mean()
          .to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nOOS Sharpe by arm x family (10 bps, mean over panels and gross levels):")
    print(wfd[wfd["cost_bps"] == COST_BPS].pivot_table(index="arm", columns="family",
          values="OOS_Sharpe").to_string(float_format=lambda x: f"{x:.4f}"))
    WFI = ["panel", "gross", "family", "cost_bps"]
    base = wfd[wfd["arm"] == "ISARGMAX-RAW"].set_index(WFI)["OOS_Sharpe"]
    for arm in ("ISARGMAX-PAIRDIAL", "ISARGMAX-MATCHED", "ADOPTED", "NOTHING(RULESv2)",
                "EWALL", "SPY"):
        o = wfd[wfd["arm"] == arm].set_index(WFI)["OOS_Sharpe"]
        d_ = (base - o).dropna()
        print(f"  ISARGMAX-RAW - {arm:<19}: mean {d_.mean():+.4f}  median {d_.median():+.4f}  "
              f"wins {int((d_ > 0).sum())}/{len(d_)}")
    po = wfd[wfd["arm"] == "ISARGMAX-RAW"]
    print(f"\nIS pick == OOS oracle in {int(po['pick_is_oracle'].sum())} of {len(po)} cells")
    print("\npicks by (family, panel, rung):")
    print(po.pivot_table(index=["family", "panel"], columns=["gross", "cost_bps"],
                         values="pick", aggfunc="first").to_string())
    print("\nthe PAIRDIAL arm is the IS pick de-grossed to the ADOPTED book's IS mean gross; "
          "MATCHED is the ADOPTED book de-grossed to the pick's. Exactly one of the two is "
          "rescaled at each cell (the higher-gross one), so no control is ever levered.")

    print("\n" + "=" * 200)
    print("Artefacts: .census.csv .census_rejects.csv .grid.csv .matched.csv .walkforward.csv")
    print("=" * 200)


if __name__ == "__main__":
    main()
