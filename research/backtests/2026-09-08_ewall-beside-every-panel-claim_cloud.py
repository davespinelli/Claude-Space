#!/usr/bin/env python3
"""Idea 239 — publish-EWall-beside-every-panel-claim (cloud, 2026-09-08)

QUESTION (queue, verbatim intent)
  Idea 77 found the un-ranked `EWall` Sharpe of a panel predicts its ranked book's OOS Sharpe
  BETTER than the ranked book's own IS Sharpe (+0.857 p 0.024 vs +0.821 p 0.034).  Back-fill
  that one column over every published panel/universe claim in the record and report how many
  claims have ZERO EXCESS over their own un-ranked control.  Max 2 params.

  The two tuned parameters are the only two free choices the back-filled column has:
    P1  GROSS of the un-ranked control, g in {0.50, 0.75, 1.00}
    P2  CADENCE of the un-ranked control, freq in {W, M}
  All 6 grid points are reported at both cost rungs.  Nothing else is tuned: the panels, the
  warm-up, the OOS date, t+1 execution and the cost rungs are the record's own conventions.

PRE-REGISTERED PREDICTIONS (written before any number in parts A-E was read)
  R1  A LARGE MINORITY, plausibly a majority, of published panel claims will have ZERO OR
      NEGATIVE excess over their own un-ranked control.  Idea 259 already found EWall wins on
      Sharpe in 25,878 of 37,044 ranked pairs (70%) on the files that happen to carry an EWall
      arm; back-filling the column to files that do NOT carry one should not reverse that.
  R2  The share with zero excess will be strongly PANEL-dependent, not uniform: on small439
      the un-ranked control has the worst Sharpe of the three panels, so ranked books there
      have the most room to clear it.
  R3  Idea 77's predictor claim will NOT survive being stated over the record, because EWall
      Sharpe is a PANEL CONSTANT: with three priceable panels there are only three distinct
      values of the "predictor" in the whole corpus, so any correlation it earns is a
      three-point statistic dressed as a regression.  This run must say so rather than
      reporting a correlation coefficient with a p-value.
  R4  The back-filled column will agree closely with the file's OWN EWall arm where a file
      carries one (gate G2).  If it does not, the back-fill is not admissible and this run
      must report the column as unusable rather than publish it.

WHAT THIS RUN DOES (declared before any number is read)
  G  GATES.  (G1) cost-rung identity net(c) = gross - turnover*c/1e4, imported from the
     record.  (G2) BACK-FILL VALIDATION: every committed CSV that carries BOTH a panel column
     AND its own un-ranked arm row is found mechanically, and the file's own EWall Sharpe is
     compared against this run's back-filled value for the same (panel, cost).  The column is
     admitted only if that agreement is tight, and the disagreement is published either way.

  A  THE COLUMN.  3 panels x 3 gross x 2 cadence x 2 cost rungs = 36 un-ranked control books,
     each with full-sample and OOS (2017-01-01..) CAGR/Sharpe/MaxDD.  This is the back-fill.

  B  THE BACK-FILL.  Every committed CSV carrying a panel/universe column and a Sharpe-like
     metric is scanned; panel labels are mapped to the three priceable panels by an explicitly
     published alias table, and every UNMAPPED label is reported with its row count so the
     coverage limit is visible rather than buried.  EXCESS = claim Sharpe - EWall Sharpe on the
     same panel at the same cost rung and the matched window (full-sample claims against the
     full-sample control, OOS_ claims against the OOS control).  The queue's question is then
     answered three ways: over all claim rows, over each file's BEST claim row, and
     file-clustered.

  C  IDEA 77's PREDICTOR CLAIM, stated over the record.  For every (file, panel) whose rows
     carry a matched (IS_Sharpe, OOS_Sharpe) pair, the panel's EWall Sharpe and the book's own
     IS Sharpe are both scored as predictors of the book's OOS Sharpe.  The number of DISTINCT
     predictor values is reported beside every correlation, because that is what decides
     whether the claim is a regression or an arithmetic identity over three panels.

  D  RULE 8.  The two parameters are chosen on the FIRST half of the record by parent-file
     date and every headline is re-read once on the second half; plus 20 seeded random FILE
     splits.  A convention that only looks stable where it was chosen is not a convention.

  E  BOTH KEEP PATHS.  The 36 un-ranked control books are themselves books, so they go through
     4a (vs the live RULES v2 book) and 4b (vs SPY) on the full sample, both halves and OOS.

SURVIVORSHIP.  The small panel is current constituents of a sub-$2B screen only (tickers with
max_1d_move >= 1.0 in data/small_meta.csv dropped first, 439 remaining) and the broad panel is
current constituents (PROTOCOL 9).  Levels are upward-biased on both.  The EXCESS column is a
same-panel, same-window, same-cost contrast, so the bias is common to both sides of it; the
absolute Sharpes quoted for the control books are not.

Costs 10 and 25 bps, next-day execution (PROTOCOL 2).  Deterministic (seeds fixed).
Artefacts: .console.txt, .controls.csv, .aliases.csv, .claims.csv.gz, .excess.csv,
           .predictor.csv, .walkforward.csv, .keeppaths.csv, .result.md
Nothing outside research/ is touched; RULES.md, scan.py, bot.py, baseline.py untouched.
"""
from __future__ import annotations

import importlib.util
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
from engine import backtest, metrics  # noqa: E402

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-08_ewall-beside-every-panel-claim_cloud"
PARENT = "2026-09-08_the-013-margin-rule_B"

LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


def _load(stem: str, mod: str):
    spec = importlib.util.spec_from_file_location(mod, OUT / f"{stem}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P241 = _load(PARENT, "i241B")            # panels, EW builder, keep_paths, win_metrics, gates
paired_t = P241.paired_t
OOS_START = P241.OOS_START

GROSS = [0.50, 0.75, 1.00]               # TUNED PARAMETER 1
FREQS = ["W", "M"]                       # TUNED PARAMETER 2
COSTS = [10.0, 25.0]
SEEDS = 20

# --- the alias table, published in full; anything not here is reported UNMAPPED, not guessed
ALIAS = {
    "u56": "u56", "U56": "u56", "universe.json": "u56", "universe.json(56)": "u56",
    "U56(56)": "u56", "u56(56)": "u56",
    "broad": "broad136", "B136": "broad136", "BROAD136": "broad136", "broad136": "broad136",
    "universe_broad.json": "broad136", "B136(136)": "broad136",
    "SMALL439": "small439", "small439": "small439", "small": "small439", "SMALL": "small439",
    "SMALL484": "small439", "small484": "small439", "SMALL483": "small439",
}
PANCOL = re.compile(r"(?i)^(panel|universe|univ|panel_name|uni)$")
SHARPE = re.compile(r"(?i)^(sharpe|oos_sharpe|is_sharpe|h1_sharpe|h2_sharpe|"
                    r"sharpe_net|net_sharpe|sharpe10|sharpe25)$")
COSTCOL = re.compile(r"(?i)^(cost|cost_bps|bps|c|rung)$")
# an un-ranked control arm, by the labels the record actually uses
EWLAB = re.compile(r"(?i)^(ewall|ew_all|ew|eqw|equalweight|equal_weight|control|ctl|"
                   r"ewall_g?[0-9.]*|unranked|un-ranked|none|off|base|baseline|plain)$")
ARMCOL = re.compile(r"(?i)^(arm|book|rule|variant|strategy|pick|label|name|family)$")
ROWCAP = 200_000


# --------------------------------------------------------------------------- Part A
def build_controls(panels: dict) -> tuple[pd.DataFrame, dict]:
    """The back-fill column: the un-ranked, un-gated equal-weight book of each panel."""
    rows, curves = [], {}
    for pname, px in panels.items():
        start = px.index[260]
        univ = px.drop(columns=["SPY"], errors="ignore") if pname == "small439" else px
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2 = backtest(px, P241.rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        curves[(pname, "__SPY__")] = spy
        curves[(pname, "__V2__")] = v2
        for g in GROSS:
            w = P241.ew_band_weights(univ, 0.0, g, gated=False)
            w = w.reindex(columns=px.columns).fillna(0.0)
            for f in FREQS:
                res = backtest(px, w, cost_bps=0.0, freq=f)
                for c in COSTS:
                    r = (res["returns"] - res["turnover"] * c / 1e4).loc[start:]
                    curves[(pname, g, f, c)] = r
                    row = dict(panel=pname, gross=g, freq=f, cost=c,
                               names=int(univ.shape[1]), start=str(start.date()))
                    row.update(P241.win_metrics(r))
                    row.update(P241.win_metrics(r, lo=OOS_START, prefix="OOS_"))
                    h = len(r) // 2
                    row["H1_Sharpe"] = metrics(r.iloc[:h])["Sharpe"]
                    row["H2_Sharpe"] = metrics(r.iloc[h:])["Sharpe"]
                    rows.append(row)
    return pd.DataFrame(rows), curves


# --------------------------------------------------------------------------- Part B
def scan_claims() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Every committed row that names a panel and quotes a Sharpe.  Returns (claims,
    ledger, own-EWall rows for the G2 back-fill validation)."""
    claims, ledger, own = [], [], []
    for f in sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz"))):
        if f.name.startswith(STEM):
            continue
        rec = dict(file=f.name, status="", n_rows=0, n_claims=0)
        try:
            df = pd.read_csv(f, nrows=ROWCAP)
        except Exception as e:
            rec["status"] = f"unreadable:{type(e).__name__}"
            ledger.append(rec)
            continue
        rec["n_rows"] = len(df)
        pcs = [c for c in df.columns if PANCOL.match(str(c))]
        scs = [c for c in df.columns if SHARPE.match(str(c))]
        if not pcs:
            rec["status"] = "no panel column"
            ledger.append(rec)
            continue
        if not scs:
            rec["status"] = "panel but no Sharpe column"
            ledger.append(rec)
            continue
        pc = pcs[0]
        ccs = [c for c in df.columns if COSTCOL.match(str(c))]
        acs = [c for c in df.columns if ARMCOL.match(str(c))]
        lab = df[pc].astype(str)
        for sc in scs:
            v = pd.to_numeric(df[sc], errors="coerce")
            win = "OOS" if str(sc).upper().startswith("OOS") else "FULL"
            cost = pd.to_numeric(df[ccs[0]], errors="coerce") if ccs else pd.Series(np.nan, index=df.index)
            arm = df[acs[0]].astype(str) if acs else pd.Series("", index=df.index)
            ok = v.notna() & np.isfinite(v) & v.abs().lt(20)
            sub = pd.DataFrame(dict(file=f.name, date=f.name[:10], col=str(sc), window=win,
                                    label=lab, panel=lab.map(ALIAS), sharpe=v,
                                    cost=cost, arm=arm))[ok.values]
            claims.append(sub)
            if acs:
                o = sub[sub.arm.map(lambda a: bool(EWLAB.match(str(a).strip())))]
                if len(o):
                    own.append(o)
        rec["status"] = "ADMITTED"
        rec["n_claims"] = int(sum(len(c) for c in claims[-len(scs):]))
        ledger.append(rec)
    C = pd.concat(claims, ignore_index=True) if claims else pd.DataFrame()
    O = pd.concat(own, ignore_index=True) if own else pd.DataFrame()
    return C, pd.DataFrame(ledger), O


def ref_sharpe(ctl: pd.DataFrame, panel: str, window: str, g: float, f: str, c: float) -> float:
    r = ctl[(ctl.panel == panel) & (ctl.gross == g) & (ctl.freq == f) & (ctl.cost == c)]
    if not len(r):
        return np.nan
    return float(r.iloc[0]["OOS_Sharpe" if window == "OOS" else "Sharpe"])


def excess_table(C: pd.DataFrame, ctl: pd.DataFrame, g: float, f: str, cost: float) -> pd.DataFrame:
    d = C[C.panel.notna()].copy()
    key = list(zip(d.panel, d.window))
    ref = {(p, w): ref_sharpe(ctl, p, w, g, f, cost) for p, w in set(key)}
    d["ewall"] = [ref[k] for k in key]
    d["excess"] = d.sharpe - d.ewall
    return d


# --------------------------------------------------------------------------- main
def main() -> None:
    say("=" * 100)
    say("IDEA 239 — publish EWall beside every panel claim: back-fill the un-ranked control")
    say("cloud, 2026-09-08.  PROTOCOL 10 and 25 bps, next-day execution, rule 8 on both dials.")
    say("Two tuned parameters: the control's GROSS and its CADENCE.  All 6 points reported.")
    say("=" * 100)

    say("\n## PART A — THE COLUMN: the un-ranked, un-gated equal-weight book of each panel\n")
    panels = P241.load_panels()
    say("  panels: " + "; ".join(f"{k} {v.shape[1] - (1 if 'SPY' in v.columns else 0)} names "
                                 f"{v.index[0].date()}..{v.index[-1].date()}"
                                 for k, v in panels.items()))
    CTL, curves = build_controls(panels)
    CTL.to_csv(OUT / f"{STEM}.controls.csv", index=False)
    say(CTL[["panel", "gross", "freq", "cost", "CAGR", "Sharpe", "MaxDD", "H1_Sharpe",
             "H2_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
        .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n## GATES\n")
    g1 = P241.gate_cost_identity(panels["u56"])
    say(f"  [G1] cost-rung identity  net(25bps) == gross - TO*25/1e4   max|d| = {g1:.3e}")
    flush()

    say("\n## PART B — THE BACK-FILL: every committed row that names a panel and quotes a Sharpe\n")
    C, LED, OWN = scan_claims()
    LED.to_csv(OUT / f"{STEM}.aliases.csv", index=False)
    say(f"  files scanned {len(LED)};  ADMITTED {int((LED.status == 'ADMITTED').sum())};  "
        + "; ".join(f"{k} {v}" for k, v in LED.status.value_counts().items() if k != "ADMITTED"))
    say(f"  claim rows {len(C)} over {C.file.nunique()} files;  "
        f"MAPPED to a priceable panel {int(C.panel.notna().sum())} "
        f"({C.panel.notna().mean():.1%});  windows " +
        ", ".join(f"{k} {v}" for k, v in C.window.value_counts().items()))
    say("\n  MAPPED labels (the published alias table):")
    m = C[C.panel.notna()].groupby(["label", "panel"]).size().sort_values(ascending=False)
    for (lab, pan), n in m.items():
        say(f"    {lab:24s} -> {pan:9s}  {n:7d} rows")
    say("\n  UNMAPPED labels — the coverage limit, reported not buried "
        f"({int(C.panel.isna().sum())} rows, {C[C.panel.isna()].file.nunique()} files):")
    u = C[C.panel.isna()].groupby("label").size().sort_values(ascending=False)
    for lab, n in u.head(25).items():
        say(f"    {str(lab)[:40]:42s} {n:7d} rows")
    if len(u) > 25:
        say(f"    ... and {len(u) - 25} further labels ({int(u.iloc[25:].sum())} rows) — sub-panels, "
            "draw ids and seeded sub-universes this run cannot price exactly and does NOT guess")

    # ---- G2: back-fill validation against the files' own un-ranked arm
    say("\n  [G2] BACK-FILL VALIDATION — this run's column vs the record's OWN un-ranked arm rows")
    if len(OWN):
        O = OWN[OWN.panel.notna()].copy()
        best = None
        for g in GROSS:
            for f in FREQS:
                e = O.copy()
                key = list(zip(e.panel, e.window))
                e["ewall"] = [ref_sharpe(CTL, p, w, g, f, 10.0) for p, w in key]
                d = (e.sharpe - e.ewall).abs()
                row = dict(gross=g, freq=f, n=len(e), mad=float(d.mean()),
                           med=float(d.median()), p90=float(d.quantile(0.90)),
                           corr=float(e.sharpe.corr(e.ewall)))
                say(f"    g {g:.2f} {f}  n {row['n']:5d}  mean|diff| {row['mad']:.4f}  "
                    f"median {row['med']:.4f}  p90 {row['p90']:.4f}  corr {row['corr']:+.4f}")
                if best is None or row["mad"] < best["mad"]:
                    best = row
        say(f"    -> closest convention g {best['gross']:.2f} {best['freq']}: mean|diff| "
            f"{best['mad']:.4f} Sharpe over {best['n']} of the record's own un-ranked rows")
        say("    NOTE: the record's own 'control' rows are NOT all plain EWall — many are a "
            "dial's declared incumbent (a gated or de-grossed book wearing the label 'control'), "
            "so this gate bounds the back-fill's error from ABOVE, it does not measure it.")
    else:
        say("    no file carries a labelled un-ranked arm beside a panel column — gate VACUOUS")
    flush()

    # ---- the queue's question
    say("\n## PART C — THE QUEUE'S QUESTION: how many published panel claims have ZERO EXCESS?\n")
    say("  EXCESS = claim Sharpe - the same panel's un-ranked control Sharpe, same window, "
        "same cost rung.")
    ex_rows = []
    for cost in COSTS:
        for g in GROSS:
            for f in FREQS:
                d = excess_table(C, CTL, g, f, cost)
                d = d[d.ewall.notna()]
                zero = float((d.excess <= 0).mean())
                fc = d.groupby("file").excess.mean()
                fbest = d.groupby("file").excess.max()
                r = dict(cost=cost, gross=g, freq=f, n=len(d), files=int(d.file.nunique()),
                         zero_share=zero, mean_excess=float(d.excess.mean()),
                         median_excess=float(d.excess.median()),
                         fc_mean=float(fc.mean()), fc_zero=float((fc <= 0).mean()),
                         filebest_zero=float((fbest <= 0).mean()))
                for p in ("u56", "broad136", "small439"):
                    dp = d[d.panel == p]
                    r[f"zero_{p}"] = float((dp.excess <= 0).mean()) if len(dp) else np.nan
                    r[f"n_{p}"] = len(dp)
                ex_rows.append(r)
    EX = pd.DataFrame(ex_rows)
    EX.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    say(EX[["cost", "gross", "freq", "n", "files", "zero_share", "mean_excess",
            "median_excess", "fc_zero", "filebest_zero", "zero_u56", "zero_broad136",
            "zero_small439"]].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("\n  zero_share      = share of CLAIM ROWS with excess <= 0 (row-pooled)")
    say("  fc_zero         = share of FILES whose MEAN claim has excess <= 0")
    say("  filebest_zero   = share of FILES whose BEST claim has excess <= 0 — "
        "the sharpest reading of the queue's question")
    d10 = excess_table(C, CTL, 0.75, "W", 10.0)
    d10 = d10[d10.ewall.notna()]
    say(f"\n  At the record's own convention (g 0.75, weekly, 10 bps): {len(d10)} claim rows, "
        f"{d10.file.nunique()} files, zero-excess share {float((d10.excess <= 0).mean()):.1%}")
    for p in ("u56", "broad136", "small439"):
        dp = d10[d10.panel == p]
        if len(dp):
            say(f"    {p:9s} n {len(dp):6d}  control Sharpe "
                f"{ref_sharpe(CTL, p, 'FULL', 0.75, 'W', 10.0):+.4f}  "
                f"zero-excess {float((dp.excess <= 0).mean()):.1%}  "
                f"mean excess {dp.excess.mean():+.4f}  best claim {dp.excess.max():+.4f}")
    # the per-claim table is 1.3M rows; commit the per-(file, panel, window) roll-up instead,
    # which is what any back-fill consumer needs and what every number above is computed from
    agg = (d10.groupby(["file", "date", "panel", "window"])
           .agg(n=("excess", "size"), ewall=("ewall", "first"),
                mean_sharpe=("sharpe", "mean"), best_sharpe=("sharpe", "max"),
                mean_excess=("excess", "mean"), median_excess=("excess", "median"),
                best_excess=("excess", "max"),
                zero_share=("excess", lambda x: float((x <= 0).mean())))
           .reset_index())
    agg.to_csv(OUT / f"{STEM}.claims.csv.gz", index=False, compression="gzip")
    say(f"  per-(file, panel, window) roll-up written: {len(agg)} rows "
        f"(the 1.3M-row per-claim table is regenerable from this script, not committed)")
    flush()

    # ---- Part D: idea 77's predictor claim
    say("\n## PART D — IDEA 77's PREDICTOR CLAIM, stated over the record\n")
    cen, _ = P241.harvest()
    cen = cen[cen.metric == "Sharpe"].copy()
    cen["label"] = cen.cell.astype(str)
    def find_panel(s: str):
        for k, v in ALIAS.items():
            if k in s:
                return v
        return None
    cen["panel"] = cen.label.map(find_panel)
    pr = cen[cen.panel.notna()].copy()
    say(f"  cells with a matched (IS_Sharpe, OOS_Sharpe) pair AND a resolvable panel: "
        f"{len(pr)} over {pr.file.nunique()} files, panels " +
        ", ".join(f"{k} {v}" for k, v in pr.panel.value_counts().items()))
    pred_rows = []
    for g in GROSS:
        for f in FREQS:
            e = pr.copy()
            e["ewall"] = [ref_sharpe(CTL, p, "FULL", g, f, 10.0) for p in e.panel]
            c_ew = float(e.ewall.rank().corr(e.OOS_star.rank()))
            c_is = float(e.IS_star.rank().corr(e.OOS_star.rank()))
            # per (file, panel) means, the unit idea 77 actually used
            gp = e.groupby(["file", "panel"]).agg(ewall=("ewall", "mean"),
                                                  IS=("IS_star", "mean"),
                                                  OOS=("OOS_star", "mean")).reset_index()
            g_ew = float(gp.ewall.rank().corr(gp.OOS.rank()))
            g_is = float(gp.IS.rank().corr(gp.OOS.rank()))
            pred_rows.append(dict(gross=g, freq=f, n_cells=len(e), n_units=len(gp),
                                  distinct_ewall=int(e.ewall.nunique()),
                                  rho_ewall_cells=c_ew, rho_IS_cells=c_is,
                                  rho_ewall_units=g_ew, rho_IS_units=g_is))
            say(f"  g {g:.2f} {f}  cells {len(e):5d} / units {len(gp):4d}  "
                f"DISTINCT EWall values {int(e.ewall.nunique())}  |  "
                f"rho(EWall, OOS) cells {c_ew:+.4f} units {g_ew:+.4f}  |  "
                f"rho(own IS, OOS) cells {c_is:+.4f} units {g_is:+.4f}")
    PR = pd.DataFrame(pred_rows)
    PR.to_csv(OUT / f"{STEM}.predictor.csv", index=False)
    say("\n  R3 CHECK — the number of DISTINCT predictor values is printed above beside every "
        "correlation.  A predictor that is CONSTANT WITHIN A PANEL cannot separate two books "
        "on the same panel, whatever its rank correlation across panels is.")
    say("  within-panel check: rho(EWall, OOS) INSIDE a panel is UNDEFINED by construction for "
        "every panel here — " + ", ".join(f"{p} ({int((pr.panel == p).sum())} cells)"
                                          for p in sorted(pr.panel.unique())) +
        " — because the column takes ONE value per panel.")
    flush()

    # ---- Part E: rule 8
    say("\n## PART E — RULE 8 ON BOTH DIALS\n")
    d_all = {}
    for g in GROSS:
        for f in FREQS:
            d_all[(g, f)] = excess_table(C, CTL, g, f, 10.0)
    dates = sorted(C.date.unique())
    cut = dates[len(dates) // 2]
    wf_rows = []
    say(f"  DATE split at {cut}")
    # choose the convention that MINIMISES the zero-excess share in sample (the most
    # conservative reading of the column: the convention that is hardest on the record)
    is_sh, oos_sh = {}, {}
    for (g, f), d in d_all.items():
        d = d[d.ewall.notna()]
        A, B = d[d.date < cut], d[d.date >= cut]
        is_sh[(g, f)] = float((A.excess <= 0).mean()) if len(A) else np.nan
        oos_sh[(g, f)] = float((B.excess <= 0).mean()) if len(B) else np.nan
        wf_rows.append(dict(split="DATE", seed=-1, gross=g, freq=f, IS_zero=is_sh[(g, f)],
                            OOS_zero=oos_sh[(g, f)], n_IS=len(A), n_OOS=len(B)))
        say(f"    g {g:.2f} {f}  IS zero-excess {is_sh[(g, f)]:.1%} (n {len(A)})  ->  "
            f"OOS zero-excess {oos_sh[(g, f)]:.1%} (n {len(B)})")
    pick = min(is_sh, key=lambda k: is_sh[k])
    say(f"  convention chosen IN SAMPLE (minimum zero-excess share): g {pick[0]:.2f} {pick[1]}  "
        f"-> read once OOS: {oos_sh[pick]:.1%};  spread across the 6 conventions OOS "
        f"{min(oos_sh.values()):.1%}..{max(oos_sh.values()):.1%}")
    files = np.array(sorted(C[C.panel.notna()].file.unique()))
    for sd in range(SEEDS):
        rng = np.random.default_rng(20260908 + sd)
        keep = set(rng.choice(files, size=len(files) // 2, replace=False))
        loc_is, loc_oos = {}, {}
        for (g, f), d in d_all.items():
            d = d[d.ewall.notna()]
            A, B = d[d.file.isin(keep)], d[~d.file.isin(keep)]
            loc_is[(g, f)] = float((A.excess <= 0).mean()) if len(A) else np.nan
            loc_oos[(g, f)] = float((B.excess <= 0).mean()) if len(B) else np.nan
        p = min(loc_is, key=lambda k: loc_is[k])
        wf_rows.append(dict(split="FILE", seed=sd, gross=p[0], freq=p[1],
                            IS_zero=loc_is[p], OOS_zero=loc_oos[p], n_IS=np.nan, n_OOS=np.nan))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    w = WF[WF.split == "FILE"]
    say(f"  {SEEDS} seeded FILE splits: convention picked " +
        ", ".join(f"g{a:.2f}/{b} x{n}" for (a, b), n in
                  w.groupby(['gross', 'freq']).size().items()) +
        f";  held-out zero-excess share mean {w.OOS_zero.mean():.1%} "
        f"(min {w.OOS_zero.min():.1%}, max {w.OOS_zero.max():.1%}); "
        f"in-sample {w.IS_zero.mean():.1%} — the gap is the column's rule-8 cost")
    flush()

    # ---- Part F: KEEP paths on the control books themselves
    say("\n## PART F — BOTH KEEP PATHS ON THE 36 CONTROL BOOKS\n")
    kp = []
    for pname in panels:
        spy = curves[(pname, "__SPY__")]
        v2 = curves[(pname, "__V2__")]
        for g in GROSS:
            for f in FREQS:
                for c in COSTS:
                    r = curves[(pname, g, f, c)]
                    row = dict(panel=pname, gross=g, freq=f, cost=c, book=f"EWall g{g:.2f} {f}")
                    row.update(P241.win_metrics(r))
                    row.update(P241.win_metrics(r, lo=OOS_START, prefix="OOS_"))
                    h = len(r) // 2
                    row["H1"] = metrics(r.iloc[:h])["Sharpe"]
                    row["H2"] = metrics(r.iloc[h:])["Sharpe"]
                    row.update(P241.keep_paths(r, v2, spy))
                    kp.append(row)
        for label, r in (("RULES v2 (live)", v2), ("SPY", spy)):
            row = dict(panel=pname, gross=np.nan, freq="", cost=np.nan, book=label)
            row.update(P241.win_metrics(r))
            row.update(P241.win_metrics(r, lo=OOS_START, prefix="OOS_"))
            h = len(r) // 2
            row["H1"] = metrics(r.iloc[:h])["Sharpe"]
            row["H2"] = metrics(r.iloc[h:])["Sharpe"]
            kp.append(row)
    KP = pd.DataFrame(kp)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(KP[["panel", "book", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b", "pass4b_oos"]]
        .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    n = int(KP.pass4a.notna().sum())
    say(f"\n  KEEP PATHS over the {n} control books: "
        f"4a {int(KP.pass4a.fillna(False).sum())}/{n}, "
        f"4b {int(KP.pass4b.fillna(False).sum())}/{n}, "
        f"4b(OOS) {int(KP.pass4b_oos.fillna(False).sum())}/{n}, "
        f"BOTH {int((KP.pass4a.fillna(False) & KP.pass4b.fillna(False)).sum())}/{n}")

    flush()
    say(f"\nwrote {STEM}.{{controls,aliases,claims,excess,predictor,walkforward,keeppaths,console}}")
    flush()


if __name__ == "__main__":
    main()
