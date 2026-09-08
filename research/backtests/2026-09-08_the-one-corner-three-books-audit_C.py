#!/usr/bin/env python3
"""Idea 451 — the one-corner-three-books audit   (lane C, 2026-09-08)

QUESTION (QUEUE 451): idea 232's pre-check [b2] found idea 228's and idea 256's
`u56 n=20 max_vol=off` quoted as the SAME object across a +0.1522 Sharpe construction gap
(ranking key +0.1137, gross channel NORM-vs-RAW +0.0323, level +0.0001), i.e. 1.5x the
premium the corner was used to explain.  Census every cell the record quotes in two or more
scripts on (key, gross channel, gross level, drop_spy) and publish the construction
fingerprint beside each.

DESIGN — two independent legs, then they are put against each other.

  LEG A (the census, on committed artefacts, not prose).  Every committed CSV under
  research/backtests that carries a panel column AND an `n` column AND a LEVEL Sharpe column
  is a published quotation of a cell.  A cell is keyed by the MATCH RULE (tuned param 1):
      M1 = (panel, n)                       — the name a claim is usually quoted by
      M2 = (panel, n, cost rung)            — cost conditioned
      M3 = (panel, n, cost rung, gross)     — cost and gross level conditioned
  A cell is IN THE CENSUS if two or more distinct SCRIPTS quote it.  Its CROSS-SCRIPT SPREAD
  is max-over-scripts(median quoted Sharpe) - min-over-scripts(...); it DISAGREES if that
  exceeds the TOLERANCE (tuned param 2) in {0.02, 0.05, 0.10, 0.20}.  All 3 x 4 = 12 grid
  points reported.  CONTROL: the same cell's WITHIN-script spread — if a cell is already
  wide inside one script, the key is under-specified and the cross-script gap is not a
  discrepancy between scripts, it is the axes the key never named.  The construction
  fingerprint of every quoting script is published beside each cell, read off its source by
  a stated text rule (key / gross channel / gross level / drop_spy), with MIXED and UNSTATED
  reported as such and never guessed.

  LEG B (the price, by simulation).  The fingerprint axes idea 232 isolated at ONE corner
  are swept at 12 corners: 3 panels x n in {10, 20} x max_vol in {off, 0.60}, each built
  16 ways = key {COMP, V1KEY} x channel {NORM, RAW} x gross {0.75, 1.00} x SPY {OUT, IN}.
  192 books, every one reported.  Nothing here is chosen: the fingerprint is the census
  object, not a dial being tuned, so the run's only tuned parameters are the census's two.
  Cost rungs 0 / 10 / 25 bps come from the exact identity r_c = r_0 - turnover * c/1e4.

RULE 8 (required): per panel x cell the fingerprint with the best IS Sharpe (through
2016-12-31) is picked and read untouched on 2017-01-01.., against (a) the PRE-REGISTERED
live fingerprint V1KEY/NORM/g=0.75/SPY-out, (b) RULES v2 on the same panel, (c) SPY.  Both
KEEP paths (4a vs RULES v2, 4b vs SPY) are evaluated on all 576 points (192 books x 3 rungs).

PROTOCOL: 10 bps anchor (0 and 25 also reported), next-day execution (engine), no shorting,
no leverage.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
from __future__ import annotations

import gzip
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_the-one-corner-three-books-audit_C"
BT = ROOT / "research" / "backtests"
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
RUNGS = (0.0, 10.0, 25.0)
TOLS = (0.02, 0.05, 0.10, 0.20)
LINES: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LINES.append(s)


# ----------------------------------------------------------------------------- LEG A
PANEL_MAP = {
    "u56": "U56", "U56": "U56", "u_56": "U56", "universe56": "U56", "U": "U56",
    "b136": "B136", "B136": "B136", "broad": "B136", "broad136": "B136", "BROAD": "B136",
    "small": "SMALL", "SMALL": "SMALL", "SMALL439": "SMALL", "SMALL484": "SMALL",
    "SMALL480": "SMALL", "small439": "SMALL", "small484": "SMALL",
}
LEVEL_SHARPE = {"Sharpe": None, "full_Sharpe": None, "Sharpe_0": 0.0,
                "Sharpe_10": 10.0, "Sharpe_25": 25.0}
COST_COLS = ("cost", "cost_bps", "bps", "rung", "cost_rung")


def norm_panel(v) -> str | None:
    s = str(v).strip()
    if "~" in s:                      # synthetic sub-panels (MIX~s0.125~1) are not record cells
        return None
    return PANEL_MAP.get(s)


def read_csv_any(p: Path) -> pd.DataFrame | None:
    try:
        if p.name.endswith(".csv.gz"):
            with gzip.open(p, "rt") as fh:
                return pd.read_csv(fh)
        return pd.read_csv(p)
    except Exception:
        return None


def script_stem(p: Path) -> str:
    return p.name.split(".")[0]


def harvest_quotes() -> pd.DataFrame:
    """Every (script, panel, n, cost, gross, Sharpe) level quotation committed as a CSV."""
    rows = []
    files = sorted(list(BT.glob("*.csv")) + list(BT.glob("*.csv.gz")))
    scanned = 0
    for p in files:
        if p.name.startswith(STEM):       # this run's own artefacts are a harvest, not a quotation
            continue
        df = read_csv_any(p)
        if df is None or df.empty:
            continue
        cols = list(df.columns)
        pcol = "panel" if "panel" in cols else ("universe" if "universe" in cols else None)
        if pcol is None or "n" not in cols:
            continue
        scols = [c for c in LEVEL_SHARPE if c in cols]
        if not scols:
            continue
        scanned += 1
        ccol = next((c for c in COST_COLS if c in cols), None)
        gcol = "gross" if "gross" in cols else None
        for sc in scols:
            sub = df[[pcol, "n", sc] + ([ccol] if ccol else []) + ([gcol] if gcol else [])].copy()
            sub = sub.dropna(subset=[pcol, "n", sc])
            for _, r in sub.iterrows():
                pan = norm_panel(r[pcol])
                if pan is None:
                    continue
                try:
                    nn = int(float(r["n"]))
                except Exception:
                    continue
                sh = float(r[sc])
                if not np.isfinite(sh) or abs(sh) > 10:
                    continue
                cost = LEVEL_SHARPE[sc]
                if cost is None and ccol is not None:
                    try:
                        cost = float(r[ccol])
                    except Exception:
                        cost = None
                gross = None
                if gcol is not None:
                    try:
                        gross = round(float(r[gcol]), 4)
                    except Exception:
                        gross = None
                rows.append(dict(script=script_stem(p), file=p.name, panel=pan, n=nn,
                                 cost=cost, gross=gross, Sharpe=sh))
    say(f"[A] {len(files)} committed CSVs; {scanned} carry (panel, n, level Sharpe); "
        f"{len(rows)} quotations harvested.")
    return pd.DataFrame(rows)


FP_RULES = {
    "key": [("COMP", (r"vol_scale\s*=\s*False", r"\bCOMP\b")),
            ("V1KEY", (r"rules_v1_weights\s*\(", r"vol_scale\s*=\s*True", r"\bV1KEY\b",
                       r"\bscore\s*\(\s*px\s*\)"))],
    "channel": [("RAW", (r"gross\s*/\s*n\b", r"\bg\s*/\s*n\b", r"/\s*float\(\s*n\s*\)",
                         r"\bw\s*\*\s*gross\s*/\s*n\b")),
                ("NORM", (r"\.div\([^)]*sum\(axis=1\)", r"normalis", r"\bNORM\b"))],
    "drop_spy": [("DROPPED", (r"drop\(columns=\[?\"SPY\"", r"drop\(columns=\[?'SPY'",
                              r"!=\s*\"SPY\"", r"!=\s*'SPY'", r"drop\(\s*\"SPY\"",
                              r"\.difference\(\[\"SPY\"\]\)")),
                 ("HELD", (r"SPY\s+is\s+holdable", r"SPY investable", r"spy_investable\s*=\s*True"))],
}


def fingerprint(src: str) -> dict:
    out = {}
    for axis, opts in FP_RULES.items():
        hits = [name for name, pats in opts if any(re.search(p, src) for p in pats)]
        out[axis] = hits[0] if len(hits) == 1 else ("MIXED" if len(hits) > 1 else "UNSTATED")
    lv = sorted({round(float(x), 4) for x in re.findall(r"gross\s*[=:]\s*([01]?\.\d+|1\.0|1)", src)}
                | {round(float(x), 4) for x in re.findall(r"GROSS[A-Z_]*\s*=\s*\(([^)]*)\)", src)
                   for x in re.findall(r"[01]?\.\d+", x)})
    out["gross_levels"] = "|".join(f"{v:g}" for v in lv) if lv else "UNSTATED"
    return out


def build_census(q: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    fps = {}
    for s in sorted(q["script"].unique()):
        p = BT / f"{s}.py"
        fps[s] = fingerprint(p.read_text()) if p.exists() else dict(
            key="NO_SOURCE", channel="NO_SOURCE", drop_spy="NO_SOURCE", gross_levels="NO_SOURCE")
    fp = pd.DataFrame(fps).T.rename_axis("script").reset_index()

    recs = []
    for rule, keys in (("M1", ["panel", "n"]),
                       ("M2", ["panel", "n", "cost"]),
                       ("M3", ["panel", "n", "cost", "gross"])):
        sub = q.dropna(subset=[k for k in keys if k in ("cost", "gross")]) if len(keys) > 2 else q
        g = sub.groupby(keys + ["script"])["Sharpe"].agg(["median", "min", "max", "size"])
        g = g.reset_index()
        for cell, blk in g.groupby(keys):
            if blk["script"].nunique() < 2:
                continue
            cross = blk["median"].max() - blk["median"].min()
            within = (blk["max"] - blk["min"]).max()
            cellname = "|".join(f"{k}={v}" for k, v in zip(keys, cell if isinstance(cell, tuple) else (cell,)))
            scripts = sorted(blk["script"])
            f = fp.set_index("script").loc[scripts]
            recs.append(dict(rule=rule, cell=cellname, n_scripts=len(scripts),
                             n_quotes=int(blk["size"].sum()),
                             cross_spread=cross, within_spread=within,
                             lo=blk["median"].min(), hi=blk["median"].max(),
                             distinct_key=f["key"].nunique(), distinct_channel=f["channel"].nunique(),
                             distinct_spy=f["drop_spy"].nunique(),
                             keys="/".join(sorted(set(f["key"]))),
                             channels="/".join(sorted(set(f["channel"]))),
                             spys="/".join(sorted(set(f["drop_spy"]))),
                             scripts=";".join(scripts)))
    return pd.DataFrame(recs), fp


# ----------------------------------------------------------------------------- LEG B
PANELS = {"U56": dict(), "B136": dict(broad=True), "SMALL": dict(small=True)}
KEYS = ("COMP", "V1KEY")
CHANNELS = ("NORM", "RAW")
GROSSES = (0.75, 1.00)
SPYS = ("OUT", "IN")
NS = (10, 20)
MAXVOLS = (None, 0.60)
PRE_REG = ("V1KEY", "NORM", 0.75, "OUT")     # the LIVE book's construction


def ranked_weights(px, key, n, max_vol, channel, gross, spy):
    s, above, vol20 = score(px, vol_scale=(key == "V1KEY"))
    cols = [c for c in px.columns if not (spy == "OUT" and c == "SPY")]
    s, above, vol20 = s[cols], above[cols], vol20[cols]
    elig = s.where(above if max_vol is None else (above & (vol20 < max_vol)))
    hold = (elig.rank(axis=1, ascending=False) <= n).astype(float)
    if channel == "RAW":
        w = hold * (gross / n)
    else:
        w = gross * hold.div(hold.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def stats(r0: pd.Series, to: pd.Series, cost: float) -> dict:
    r = r0 - to * cost / 1e4
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ris), metrics(roos)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"],
                OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"], TO=to.mean() * 252)


def run_leg_b() -> tuple[pd.DataFrame, pd.DataFrame]:
    grid, refs = [], []
    for pan, kw in PANELS.items():
        px = load_universe(**kw)
        start = px.index[260]
        px = px.loc[start:]
        spy_r = px["SPY"].pct_change().fillna(0.0)
        zero_to = pd.Series(0.0, index=px.index)
        b = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
        for c in RUNGS:
            refs.append(dict(panel=pan, book="RULES v2", cost=c,
                             **stats(b["returns"], b["turnover"], c)))
            refs.append(dict(panel=pan, book="SPY", cost=c, **stats(spy_r, zero_to, 0.0)))
        say(f"[B] {pan}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}")
        for n in NS:
            for mv in MAXVOLS:
                for key in KEYS:
                    for ch in CHANNELS:
                        for g in GROSSES:
                            for spy in SPYS:
                                w = ranked_weights(px, key, n, mv, ch, g, spy)
                                res = backtest(px, w, cost_bps=0.0, freq="W")
                                for c in RUNGS:
                                    grid.append(dict(
                                        panel=pan, n=n, max_vol=("off" if mv is None else mv),
                                        key=key, channel=ch, gross=g, spy=spy, cost=c,
                                        **stats(res["returns"], res["turnover"], c)))
    return pd.DataFrame(grid), pd.DataFrame(refs)


def keep_paths(grid: pd.DataFrame, refs: pd.DataFrame) -> pd.DataFrame:
    r = refs.set_index(["panel", "book", "cost"])
    out = []
    for _, x in grid.iterrows():
        v2 = r.loc[(x["panel"], "RULES v2", x["cost"])]
        sp = r.loc[(x["panel"], "SPY", x["cost"])]
        p4a = bool(x["H1"] > v2["H1"] and x["H2"] > v2["H2"] and x["MaxDD"] >= v2["MaxDD"])
        p4b = bool(x["H1"] > sp["H1"] and x["H2"] > sp["H2"] and x["OOS_Sharpe"] > sp["OOS_Sharpe"]
                   and abs(x["MaxDD"]) <= 0.60 * abs(sp["MaxDD"]) and x["CAGR"] >= 0.70 * sp["CAGR"])
        out.append(dict(x, pass4a=p4a, pass4b=p4b, v2_H1=v2["H1"], v2_H2=v2["H2"],
                        v2_MaxDD=v2["MaxDD"], spy_H1=sp["H1"], spy_H2=sp["H2"],
                        spy_OOS_Sharpe=sp["OOS_Sharpe"], spy_MaxDD=sp["MaxDD"], spy_CAGR=sp["CAGR"]))
    return pd.DataFrame(out)


def walk_forward(keep: pd.DataFrame, refs: pd.DataFrame) -> pd.DataFrame:
    r = refs.set_index(["panel", "book", "cost"])
    rows = []
    for (pan, n, mv, c), blk in keep.groupby(["panel", "n", "max_vol", "cost"]):
        pick = blk.loc[blk["IS_Sharpe"].idxmax()]
        pre = blk[(blk["key"] == PRE_REG[0]) & (blk["channel"] == PRE_REG[1])
                  & (blk["gross"] == PRE_REG[2]) & (blk["spy"] == PRE_REG[3])].iloc[0]
        best_oos = blk["OOS_Sharpe"].max()
        v2, sp = r.loc[(pan, "RULES v2", c)], r.loc[(pan, "SPY", c)]
        for tag, row in (("IS_chooser", pick), ("pre_registered", pre)):
            rows.append(dict(panel=pan, n=n, max_vol=mv, cost=c, arm=tag,
                             fp=f"{row['key']}/{row['channel']}/{row['gross']:g}/{row['spy']}",
                             OOS_CAGR=row["OOS_CAGR"], OOS_Sharpe=row["OOS_Sharpe"],
                             OOS_MaxDD=row["OOS_MaxDD"],
                             regret=best_oos - row["OOS_Sharpe"],
                             v2_OOS_Sharpe=v2["OOS_Sharpe"], v2_OOS_CAGR=v2["OOS_CAGR"],
                             v2_OOS_MaxDD=v2["OOS_MaxDD"], spy_OOS_Sharpe=sp["OOS_Sharpe"],
                             spy_OOS_CAGR=sp["OOS_CAGR"], spy_OOS_MaxDD=sp["OOS_MaxDD"],
                             beats_spy=row["OOS_Sharpe"] > sp["OOS_Sharpe"],
                             beats_v2=row["OOS_Sharpe"] > v2["OOS_Sharpe"],
                             spread_of_cell=blk["OOS_Sharpe"].max() - blk["OOS_Sharpe"].min()))
    return pd.DataFrame(rows)


def axis_effects(grid: pd.DataFrame) -> pd.DataFrame:
    """Mean paired flip of each fingerprint axis, holding the other three + cell fixed."""
    idx = ["panel", "n", "max_vol", "cost"]
    rows = []
    for axis, a, b in (("key", "V1KEY", "COMP"), ("channel", "NORM", "RAW"),
                       ("gross", 0.75, 1.00), ("spy", "OUT", "IN")):
        others = [c for c in ("key", "channel", "gross", "spy") if c != axis]
        m = grid.set_index(idx + others + [axis])[["Sharpe", "CAGR", "MaxDD", "OOS_Sharpe"]]
        A = m.xs(a, level=axis); B = m.xs(b, level=axis)
        d = (B - A).dropna()
        for c, blk in d.groupby(level="cost"):
            rows.append(dict(axis=f"{axis}: {a}->{b}", cost=c, n=len(blk),
                             mean_dSharpe=blk["Sharpe"].mean(), sd=blk["Sharpe"].std(),
                             min=blk["Sharpe"].min(), max=blk["Sharpe"].max(),
                             frac_pos=(blk["Sharpe"] > 0).mean(),
                             mean_dOOS=blk["OOS_Sharpe"].mean(),
                             mean_dCAGR=blk["CAGR"].mean(), mean_dMaxDD=blk["MaxDD"].mean()))
    return pd.DataFrame(rows)


def reproduce_b2(grid: pd.DataFrame) -> None:
    """Idea 232 [b2]'s four builds at U56 n=20 max_vol=off, 10 bps — the run's control."""
    s = grid[(grid.panel == "U56") & (grid.n == 20) & (grid.max_vol == "off")
             & (grid.cost == 10.0) & (grid.spy == "IN") & (grid.gross == 0.75)]
    say("\n[control] idea 232 [b2]'s four builds, U56 n=20 max_vol=off g=0.75 @10 bps "
        "(SPY investable, idea 228's convention):")
    say(s[["key", "channel", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "TO"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    try:
        v1n = s[(s.key == "V1KEY") & (s.channel == "NORM")]["Sharpe"].iloc[0]
        cr = s[(s.key == "COMP") & (s.channel == "RAW")]["Sharpe"].iloc[0]
        say(f"[control] construction spread V1KEY/NORM -> COMP/RAW = {cr - v1n:+.4f} "
            f"(idea 232 published +0.1522 at g=0.75 with SPY investable)")
    except IndexError:
        pass


def main() -> None:
    say(f"# {STEM}\n")

    # ---------------- LEG A
    q = harvest_quotes()
    q.to_csv(BT / f"{STEM}.quotes.csv.gz", index=False, compression="gzip")
    census, fp = build_census(q)
    census.to_csv(BT / f"{STEM}.census.csv", index=False)
    fp.to_csv(BT / f"{STEM}.fingerprints.csv", index=False)

    say(f"\n[A] fingerprints read off {len(fp)} quoting scripts:")
    for axis in ("key", "channel", "drop_spy"):
        vc = fp[axis].value_counts()
        say(f"    {axis:9s} " + "  ".join(f"{k} {v}" for k, v in vc.items()))

    say("\n[A] CENSUS GRID — all 12 points (match rule x tolerance), "
        "cells quoted by >= 2 scripts:")
    say(f"{'rule':5s} {'cells':>6s} {'scripts':>8s} {'medSpread':>10s} {'medWithin':>10s} "
        + "  ".join(f"tol{t:g}" for t in TOLS))
    tbl = []
    for rule in ("M1", "M2", "M3"):
        c = census[census["rule"] == rule]
        if c.empty:
            say(f"{rule:5s} {0:>6d}")
            continue
        line = (f"{rule:5s} {len(c):>6d} {c['n_scripts'].sum():>8d} "
                f"{c['cross_spread'].median():>10.4f} {c['within_spread'].median():>10.4f} ")
        for t in TOLS:
            share = (c["cross_spread"] > t).mean()
            line += f"  {share:.3f}"
            tbl.append(dict(rule=rule, tol=t, cells=len(c), disagree=int((c["cross_spread"] > t).sum()),
                            share=share, median_cross=c["cross_spread"].median(),
                            median_within=c["within_spread"].median(),
                            share_within_gt_cross=float((c["within_spread"] >= c["cross_spread"]).mean())))
        say(line)
    pd.DataFrame(tbl).to_csv(BT / f"{STEM}.censusgrid.csv", index=False)

    for rule in ("M1", "M2", "M3"):
        c = census[census["rule"] == rule]
        if c.empty:
            continue
        say(f"\n[A] {rule}: widest 8 cells by cross-script spread "
            f"(within = same cell's spread INSIDE one script):")
        top = c.nlargest(8, "cross_spread")
        say(top[["cell", "n_scripts", "n_quotes", "lo", "hi", "cross_spread", "within_spread",
                 "keys", "channels"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------- LEG B
    say("\n[B] pricing the fingerprint at 12 corners x 16 builds ...")
    grid, refs = run_leg_b()
    grid.to_csv(BT / f"{STEM}.grid.csv", index=False)
    refs.to_csv(BT / f"{STEM}.refs.csv", index=False)
    reproduce_b2(grid)

    say("\n[B] CONSTRUCTION SPREAD per cell (max-min Sharpe over the 16 builds):")
    sp = (grid.groupby(["panel", "n", "max_vol", "cost"])
          .agg(spread=("Sharpe", lambda s: s.max() - s.min()),
               lo=("Sharpe", "min"), hi=("Sharpe", "max"),
               oos_spread=("OOS_Sharpe", lambda s: s.max() - s.min()),
               dd_spread=("MaxDD", lambda s: s.max() - s.min())).reset_index())
    sp.to_csv(BT / f"{STEM}.spread.csv", index=False)
    say(sp[sp.cost == 10.0].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"    all rungs: median spread {sp['spread'].median():.4f}, "
        f"min {sp['spread'].min():.4f}, max {sp['spread'].max():.4f}")

    ax = axis_effects(grid)
    ax.to_csv(BT / f"{STEM}.axes.csv", index=False)
    say("\n[B] PER-AXIS main effect (paired flips, other three axes + cell held fixed):")
    say(ax.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- KEEP paths + rule 8
    keep = keep_paths(grid, refs)
    keep.to_csv(BT / f"{STEM}.keep.csv", index=False)
    say(f"\n[KEEP] {len(keep)} points (192 books x 3 rungs): "
        f"4a {int(keep['pass4a'].sum())}, 4b {int(keep['pass4b'].sum())}")
    for c in RUNGS:
        k = keep[keep.cost == c]
        say(f"    @{c:g} bps: 4a {int(k['pass4a'].sum())}/{len(k)}, 4b {int(k['pass4b'].sum())}/{len(k)}")
    if keep["pass4b"].any():
        say("    4b passers by (panel, key, channel, gross, spy):")
        say(keep[keep.pass4b].groupby(["panel", "key", "channel", "gross", "spy"]).size()
            .to_string())
    k10 = keep[keep.cost == 10.0]
    bars = dict(H1=(k10["H1"] <= k10["spy_H1"]).sum(), H2=(k10["H2"] <= k10["spy_H2"]).sum(),
                OOS=(k10["OOS_Sharpe"] <= k10["spy_OOS_Sharpe"]).sum(),
                DD=(k10["MaxDD"].abs() > 0.60 * k10["spy_MaxDD"].abs()).sum(),
                CAGR=(k10["CAGR"] < 0.70 * k10["spy_CAGR"]).sum())
    say("    binding 4b bars @10 bps (of 64 points): " + "  ".join(f"{k} {v}" for k, v in bars.items()))

    wf = walk_forward(keep, refs)
    wf.to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    say("\n[RULE 8] IS chooser (picks the fingerprint on <= 2016) vs the PRE-REGISTERED live "
        "fingerprint V1KEY/NORM/0.75/SPY-out, read on 2017+:")
    say(wf[wf.cost == 10.0][["panel", "n", "max_vol", "arm", "fp", "OOS_CAGR", "OOS_Sharpe",
                             "OOS_MaxDD", "regret", "spread_of_cell"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for arm in ("IS_chooser", "pre_registered"):
        a = wf[wf.arm == arm]
        say(f"    {arm:15s} mean OOS Sharpe {a['OOS_Sharpe'].mean():.4f}  "
            f"mean regret {a['regret'].mean():.4f}  beats SPY {int(a['beats_spy'].sum())}/{len(a)}  "
            f"beats RULES v2 {int(a['beats_v2'].sum())}/{len(a)}")
    piv = wf.pivot_table(index=["panel", "n", "max_vol", "cost"], columns="arm", values="OOS_Sharpe")
    d = (piv["IS_chooser"] - piv["pre_registered"]).dropna()
    say(f"    IS chooser - pre-registered, OOS Sharpe: mean {d.mean():+.4f}, "
        f"positive {int((d > 0).sum())}/{len(d)}, min {d.min():+.4f}, max {d.max():+.4f}")
    say(f"    reference: mean OOS-Sharpe spread INSIDE a cell (the fingerprint's own range) "
        f"{wf['spread_of_cell'].mean():.4f}")

    # ---------------- A vs B
    say("\n[A x B] is the record's cross-script disagreement the SIZE of the fingerprint?")
    for rule in ("M1", "M2", "M3"):
        c = census[census["rule"] == rule]
        if c.empty:
            continue
        med_fp = sp["spread"].median()
        say(f"    {rule}: median cross-script spread {c['cross_spread'].median():.4f}; "
            f"cells wider than the median 16-build fingerprint span ({med_fp:.4f}): "
            f"{int((c['cross_spread'] > med_fp).sum())}/{len(c)}; "
            f"cells whose WITHIN-script spread already covers the cross gap: "
            f"{int((c['within_spread'] >= c['cross_spread']).sum())}/{len(c)}")

    (BT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
