#!/usr/bin/env python3
"""Idea 417 — is IS-argmax CONFIDENCE an inverse signal?  (cloud lane, 2026-09-08)

QUESTION (QUEUE 417): idea 151's sharpest mechanism is rho(d, IS_argmax_margin) = -0.383
over 72 cells: the more decisively an arm wins IN SAMPLE, the worse its OUT-OF-SAMPLE
premium over do-nothing.  Is that inversion a general property of the record's committed
grids (every file carrying an IS metric and an OOS metric per arm), or a property of idea
94's one arm menu?

DESIGN
  Part A — CENSUS over every `research/backtests/*.csv` carrying, per arm, at least one
    matched (IS_M, OOS_M) pair.  Cells are discovered mechanically (see `id_cols`), every
    exclusion is counted in a ledger, and nothing is hand-picked.
      margin  = IS_M(argmax) - IS_M(runner-up)   [confidence]
      d_rand  = OOS_M(argmax) - mean OOS_M over the cell's arms   [premium over a RANDOM
                arm = idea 418's menu, defined on every cell]
      d_ctl   = OOS_M(argmax) - OOS_M(control)   [idea 151's own estimand, only on cells
                carrying a labelled control arm]
    Two tuned parameters, both fully reported: metric M in {Sharpe, CAGR, MaxDD, Calmar}
    and margin normalisation in {raw, z, rng}.  12 grid points, all printed.
    Pre-registered lineage split: idea 94's own corpus (files 132/142/151/416) vs the rest.
  Part B — FRESH OUT-OF-CORPUS replication on real prices: a 31-arm menu (band x gross x
    cadence, plus an ungated control) on three panels x two cost rungs, IS-chosen on
    2008/2010-2016 and read once on 2017-01-01.., with RULES v2 and SPY levels and both
    KEEP paths.  Same rho, computed on cells that did not exist when idea 151 ran.

RULE 8 everywhere: Part A's chooser is calibrated on the corpus's FIRST half by parent-file
date and read on the second half untouched; Part B's arms are chosen on the IS window only.
PROTOCOL: 10 bps anchor (25 bps also reported), next-day execution (engine), no shorting.
Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
from __future__ import annotations
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
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_is-IS-argmax-CONFIDENCE-an-inverse-signal_cloud"
OUT = ROOT / "research" / "backtests"
METRICS = ["Sharpe", "CAGR", "MaxDD", "Calmar"]      # all "higher is better" as stored
NORMS = ["raw", "z", "rng"]
CONTROL_LABELS = {"control", "ctl", "base", "baseline", "none", "off", "d_none", "nogate",
                  "ungated", "no_overlay", "plain"}
LINEAGE = ("why-the-IS-4b-screen-changes-no-pick", "selector-comparison-needs-more-cells",
           "does-any-selector-beat-doing-nothing", "pre-register-K_CAGR-as-the-rule-8-default")
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


# ------------------------------------------------------------------ statistics
def spearman(x, y):
    """Spearman rho, Fisher-z t and two-sided p, on the pairwise-complete rows."""
    d = pd.DataFrame({"x": pd.to_numeric(pd.Series(x), errors="coerce"),
                      "y": pd.to_numeric(pd.Series(y), errors="coerce")}).dropna()
    n = len(d)
    if n < 5 or d.x.nunique() < 2 or d.y.nunique() < 2:
        return dict(n=n, rho=np.nan, t=np.nan, p=np.nan)
    r = float(d.x.rank().corr(d.y.rank()))
    r = min(max(r, -0.999999), 0.999999)
    z = np.arctanh(r) * np.sqrt(n - 3)
    return dict(n=n, rho=r, t=float(z), p=float(2 * (1 - _ncdf(abs(z)))))


def _ncdf(z):
    import math
    return 0.5 * (1 + math.erf(z / np.sqrt(2)))


def paired_t(x):
    x = pd.Series(x).dropna().astype(float)
    n = len(x)
    if n < 2:
        return dict(n=n, mean=np.nan, t=np.nan, W=0, L=0)
    t = float(x.mean() / (x.std(ddof=1) / np.sqrt(n))) if x.std(ddof=1) > 0 else np.nan
    return dict(n=n, mean=float(x.mean()), t=t, W=int((x > 0).sum()), L=int((x < 0).sum()))


# ------------------------------------------------------------------ Part A: harvest
METRIC_PREFIX = re.compile(r"^(IS_|OOS_|pass|fail|adm_|m_|d_|uc_|sc_|U_|S_|C_|n_)")
METRIC_NAMES = {"CAGR", "Sharpe", "MaxDD", "Calmar", "Sortino", "Vol", "H1", "H2", "TO",
                "turnover", "Total", "Years", "WinRate", "breakeven", "cstar", "c_star"}


def id_columns(df: pd.DataFrame, armcol: str) -> list[str]:
    """Cell-identifying columns, found mechanically.

    A column qualifies when it is not the arm column, not a metric/mask column, has 2..40
    distinct values, and is NOT functionally determined by the arm (a column that takes one
    value per arm across the whole file is an arm PARAMETER, not a cell label).
    """
    out = []
    for c in df.columns:
        if c == armcol or METRIC_PREFIX.match(c) or c in METRIC_NAMES:
            continue
        nu = df[c].nunique(dropna=False)
        if nu < 2 or nu > 40:
            continue
        if df[c].dtype.kind == "f" and nu > 12:
            continue
        per_arm = df.groupby(armcol)[c].nunique(dropna=False)
        if (per_arm <= 1).all():          # one value per arm => arm parameter
            continue
        out.append(c)
    return out


def harvest() -> tuple[pd.DataFrame, pd.DataFrame]:
    """One row per (file, cell, metric).  Returns (census, ledger)."""
    rows, ledger = [], []
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM):       # never census this script's own output
            continue
        rec = dict(file=f.name, status="", n_cells=0, n_rows=0)
        try:
            df = pd.read_csv(f)
        except Exception as e:
            rec["status"] = f"unreadable:{type(e).__name__}"
            ledger.append(rec)
            continue
        armcol = "arm" if "arm" in df.columns else ("pick" if "pick" in df.columns else None)
        if armcol is None:
            rec["status"] = "no arm column"
            ledger.append(rec)
            continue
        mets = [m for m in METRICS if f"IS_{m}" in df.columns and f"OOS_{m}" in df.columns]
        if not mets:
            rec["status"] = "no matched IS_/OOS_ pair"
            ledger.append(rec)
            continue
        ids = id_columns(df, armcol)
        groups = df.groupby(ids, dropna=False, sort=True) if ids else [((), df)]
        n_cells = n_used = 0
        for key, cell in groups:
            n_cells += 1
            if cell[armcol].duplicated().any() or cell[armcol].nunique() < 3:
                continue
            arms = cell[armcol].astype(str)
            ctl = [a for a in arms if str(a).strip().lower() in CONTROL_LABELS]
            for m in mets:
                isv = pd.to_numeric(cell[f"IS_{m}"], errors="coerce")
                oov = pd.to_numeric(cell[f"OOS_{m}"], errors="coerce")
                ok = isv.notna() & oov.notna() & np.isfinite(isv) & np.isfinite(oov)
                if ok.sum() < 3 or isv[ok].nunique() < 2:
                    continue
                I, O, A = isv[ok].values, oov[ok].values, arms[ok].values
                order = np.argsort(-I, kind="stable")
                star, second = order[0], order[1]
                margin = float(I[star] - I[second])
                sd, rng = float(np.std(I, ddof=1)), float(I.max() - I.min())
                r = dict(file=f.name, date=f.name[:10], stem=f.name.split(".")[0],
                         lineage=any(t in f.name for t in LINEAGE), metric=m,
                         cell="|".join(map(str, key)) if ids else "ALL",
                         n_arms=int(ok.sum()), arm_star=str(A[star]),
                         margin_raw=margin,
                         margin_z=margin / sd if sd > 0 else np.nan,
                         margin_rng=margin / rng if rng > 0 else np.nan,
                         IS_star=float(I[star]), OOS_star=float(O[star]),
                         OOS_mean=float(O.mean()),
                         d_rand=float(O[star] - O.mean()))
                if ctl:
                    cm = np.array([str(a).strip().lower() in CONTROL_LABELS for a in A])
                    if cm.any():
                        r["OOS_ctl"] = float(O[cm][0])
                        r["d_ctl"] = float(O[star] - O[cm][0])
                        r["star_is_ctl"] = bool(cm[star])
                rows.append(r)
                n_used = n_used or 0
            n_used += 1
        rec.update(status="ADMITTED" if n_used else "no usable cell",
                   n_cells=n_cells, n_rows=sum(1 for x in rows if x["file"] == f.name))
        ledger.append(rec)
    return pd.DataFrame(rows), pd.DataFrame(ledger)


def rho_grid(cen: pd.DataFrame, dcol: str, label: str) -> pd.DataFrame:
    """rho(d, margin) at all 12 (metric x normalisation) grid points."""
    out = []
    for m in METRICS:
        sub = cen[cen.metric == m]
        for nm in NORMS:
            col = {"raw": "margin_raw", "z": "margin_z", "rng": "margin_rng"}[nm]
            s = spearman(sub[col], sub[dcol]) if dcol in sub.columns else dict(n=0, rho=np.nan, t=np.nan, p=np.nan)
            out.append(dict(scope=label, metric=m, norm=nm, **s))
    return pd.DataFrame(out)


# ------------------------------------------------------------------ Part B: fresh grid
def ew_band_weights(px, band, gross, gated=True):
    """EW over everything priced that day at gross/N; gated names go to CASH (RULES v2 shape).
    band is the 200d +/- band; gated=False is the ungated control (hold everything)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if not gated:
        return ew
    return ew.where(band_state(px, band), 0.0)


def arm_menu():
    arms = [("control", dict(band=None, gross=1.0, freq="W", gated=False))]
    for band in (0.0, 0.015, 0.03, 0.045, 0.06):
        for gross in (0.50, 0.75, 1.00):
            for freq in ("W", "M"):
                arms.append((f"b{band:g}-g{gross:.2f}-{freq}",
                             dict(band=band, gross=gross, freq=freq, gated=True)))
    return arms


def win_metrics(r, lo=None, hi=None, prefix=""):
    x = r.loc[lo:hi] if (lo or hi) else r
    m = metrics(x)
    h = len(x) // 2
    return {f"{prefix}CAGR": m["CAGR"], f"{prefix}Sharpe": m["Sharpe"], f"{prefix}MaxDD": m["MaxDD"],
            f"{prefix}Calmar": m["Calmar"],
            f"{prefix}H1": metrics(x.iloc[:h])["Sharpe"], f"{prefix}H2": metrics(x.iloc[h:])["Sharpe"]}


def load_panels():
    P = {}
    P["u56"] = load_universe()
    P["broad136"] = load_universe(broad=True)
    small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in small.columns if c not in bad]
    P["small439"] = small[keep]
    return P


def fresh_grid(panels, costs=(10.0, 25.0)):
    rows, curves = [], {}
    arms = arm_menu()
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        univ = px.drop(columns=["SPY"], errors="ignore") if pname == "small439" else px
        base_r = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        raw = {}
        for name, a in arms:
            w = ew_band_weights(univ, a["band"] if a["band"] is not None else 0.0,
                                a["gross"], gated=a["gated"])
            w = w.reindex(columns=px.columns).fillna(0.0)
            res = backtest(px, w, cost_bps=0.0, freq=a["freq"])
            raw[name] = (res["returns"], res["turnover"])
        for c in costs:
            for name, a in arms:
                r0, to = raw[name]
                r = (r0 - to * c / 1e4).loc[start:]          # rung identity (idea 352)
                curves[(pname, c, name)] = r
                row = dict(panel=pname, cost=c, arm=name, band=a["band"], gross=a["gross"],
                           freq=a["freq"], gated=a["gated"], TO=float(to.loc[start:].sum() / (len(r) / 252)))
                row.update(win_metrics(r, prefix=""))                    # full sample
                row.update(win_metrics(r, hi=IS_END, prefix="IS_"))
                row.update(win_metrics(r, lo=OOS_START, prefix="OOS_"))
                rows.append(row)
            curves[(pname, c, "__SPY__")] = spy
            curves[(pname, c, "__V2__")] = base_r
    return pd.DataFrame(rows), curves


def keep_paths(r, spy, base):
    """4a vs the LIVE RULES v2 book and 4b vs SPY, on the full sample and on the OOS window."""
    def bars(x, b, s):
        mx, mb, ms = metrics(x), metrics(b), metrics(s)
        h = len(x) // 2
        xh = (metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"])
        bh = (metrics(b.iloc[:h])["Sharpe"], metrics(b.iloc[h:])["Sharpe"])
        sh = (metrics(s.iloc[:h])["Sharpe"], metrics(s.iloc[h:])["Sharpe"])
        p4a = xh[0] > bh[0] and xh[1] > bh[1] and mx["MaxDD"] >= mb["MaxDD"]
        p4b = (xh[0] > sh[0] and xh[1] > sh[1] and mx["Sharpe"] > ms["Sharpe"]
               and mx["MaxDD"] >= 0.60 * ms["MaxDD"] and mx["CAGR"] >= 0.70 * ms["CAGR"])
        return p4a, p4b
    a_full, b_full = bars(r, base, spy)
    a_oos, b_oos = bars(r.loc[OOS_START:], base.loc[OOS_START:], spy.loc[OOS_START:])
    return dict(pass4a=a_full, pass4b=b_full, pass4a_oos=a_oos, pass4b_oos=b_oos)


# ------------------------------------------------------------------ main
def main():
    say("=" * 100)
    say("IDEA 417 — is IS-argmax CONFIDENCE an inverse signal?   (cloud, 2026-09-08)")
    say("=" * 100)

    # ---------------- Part A
    say("\n## PART A — census of every committed grid carrying a matched (IS_M, OOS_M) pair per arm\n")
    cen, led = harvest()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    led.to_csv(OUT / f"{STEM}.ledger.csv", index=False)
    adm = led[led.status == "ADMITTED"]
    say(f"files scanned {len(led)} -> ADMITTED {len(adm)}; "
        + "; ".join(f"{k} {v}" for k, v in led.status.value_counts().items() if k != "ADMITTED"))
    say(f"census rows (file x cell x metric): {len(cen)}; distinct cells "
        f"{cen.groupby(['file', 'cell']).ngroups}; files {cen.file.nunique()}; "
        f"metrics {sorted(cen.metric.unique())}")
    say(f"cells carrying a labelled control arm: {int(cen.d_ctl.notna().sum()) if 'd_ctl' in cen else 0} rows")
    say(f"lineage (idea 94 corpus: 132/142/151/416) rows {int(cen.lineage.sum())}, "
        f"out-of-lineage rows {int((~cen.lineage).sum())}")

    grids = []
    for dcol in ("d_rand", "d_ctl"):
        if dcol not in cen.columns:
            continue
        for lab, sub in (("ALL", cen), ("LINEAGE(94)", cen[cen.lineage]), ("OUT-OF-LINEAGE", cen[~cen.lineage])):
            g = rho_grid(sub, dcol, f"{dcol}/{lab}")
            grids.append(g)
    G = pd.concat(grids, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.rhogrid.csv", index=False)
    say("\nALL 12 grid points (metric x normalisation) x scope — rho(d, margin):\n")
    piv = G.pivot_table(index=["metric", "norm"], columns="scope", values="rho")
    say(piv.to_string(float_format=lambda x: f"{x:+.3f}"))
    say("\nsample sizes (cells) per scope:")
    say(G.pivot_table(index=["metric", "norm"], columns="scope", values="n").to_string())
    say("\nfull table with t (Fisher z) and p:")
    say(G.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # headline: idea 151's own configuration (metric Sharpe, raw margin, d over control)
    say("\n### The queue's own number, reproduced and then widened")
    for dcol in ("d_ctl", "d_rand"):
        if dcol not in cen.columns:
            continue
        for lab, sub in (("LINEAGE(94)", cen[cen.lineage]), ("OUT-OF-LINEAGE", cen[~cen.lineage]), ("ALL", cen)):
            s = spearman(sub[sub.metric == "Sharpe"]["margin_raw"], sub[sub.metric == "Sharpe"][dcol])
            say(f"  Sharpe/raw/{dcol:7s} {lab:15s} n {s['n']:5d}  rho {s['rho']:+.3f}  t {s['t']:+.2f}  p {s['p']:.4f}")

    # the degeneracy check the d_ctl estimand needs: when the argmax IS the control,
    # d_ctl == 0 by construction, so a rho computed over those cells prices arithmetic.
    say("\n### DEGENERACY CHECK — d_ctl is identically 0 whenever the IS-argmax IS the control")
    if "star_is_ctl" in cen.columns:
        sc = cen[cen.d_ctl.notna()].copy()
        sc["star_is_ctl"] = sc.star_is_ctl.fillna(False).astype(bool)
        say(f"  cells with a labelled control: {len(sc)}; argmax == control in "
            f"{int(sc.star_is_ctl.sum())} ({sc.star_is_ctl.mean():.1%}) — those rows carry d_ctl = 0 "
            f"(max |d_ctl| there {sc[sc.star_is_ctl].d_ctl.abs().max():.2e})")
        mv = sc[~sc.star_is_ctl]
        for lab, sub in (("ALL", sc), ("MOVED only (argmax != control)", mv)):
            for m in METRICS[:3]:
                s = spearman(sub[sub.metric == m]["margin_z"], sub[sub.metric == m]["d_ctl"])
                say(f"  {lab:32s} {m:6s}/z: n {s['n']:5d}  rho {s['rho']:+.3f}  t {s['t']:+.2f}  p {s['p']:.4f}")
        for lab, sub in (("LINEAGE(94), MOVED", mv[mv.lineage]), ("OUT-OF-LINEAGE, MOVED", mv[~mv.lineage])):
            s = spearman(sub[sub.metric == "Sharpe"]["margin_raw"], sub[sub.metric == "Sharpe"]["d_ctl"])
            say(f"  {lab:32s} Sharpe/raw: n {s['n']:5d}  rho {s['rho']:+.3f}  t {s['t']:+.2f}  p {s['p']:.4f}")

    # per-file distribution (is it one file or many?)
    say("\n### Per-file rho (Sharpe/z/d_rand), files with >= 8 cells")
    pf = []
    for (f, ), sub in cen[cen.metric == "Sharpe"].groupby(["file"]):
        if len(sub) >= 8:
            s = spearman(sub.margin_z, sub.d_rand)
            pf.append(dict(file=f, lineage=bool(sub.lineage.iloc[0]), **s))
    PF = pd.DataFrame(pf).sort_values("rho")
    PF.to_csv(OUT / f"{STEM}.perfile.csv", index=False)
    if len(PF):
        say(f"  files {len(PF)}; rho < 0 in {int((PF.rho < 0).sum())} of {int(PF.rho.notna().sum())}; "
            f"median {PF.rho.median():+.3f}; mean {PF.rho.mean():+.3f}")
        say("  most negative 5:\n" + PF.head(5).to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
        say("  most positive 5:\n" + PF.tail(5).to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
        say(f"  lineage files: {PF[PF.lineage].rho.round(3).tolist()}")

    # rule 8 on the corpus itself: choose the grid point on the first half by parent-file date
    say("\n### RULE 8 on the corpus — choose the (metric, normalisation) on the FIRST half of "
        "the record by parent-file date, read the SECOND half untouched")
    dates = sorted(cen.date.unique())
    cut = dates[len(dates) // 2]
    A, B = cen[cen.date < cut], cen[cen.date >= cut]
    say(f"  files dated < {cut}: {A.file.nunique()} files / {len(A)} rows (IS);  "
        f">= {cut}: {B.file.nunique()} files / {len(B)} rows (OOS)")
    wf = []
    for m in METRICS:
        for nm in NORMS:
            col = {"raw": "margin_raw", "z": "margin_z", "rng": "margin_rng"}[nm]
            a = spearman(A[A.metric == m][col], A[A.metric == m]["d_rand"])
            b = spearman(B[B.metric == m][col], B[B.metric == m]["d_rand"])
            wf.append(dict(metric=m, norm=nm, IS_n=a["n"], IS_rho=a["rho"], IS_t=a["t"],
                           OOS_n=b["n"], OOS_rho=b["rho"], OOS_t=b["t"], OOS_p=b["p"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    pick = W.loc[W.IS_rho.idxmin()]
    say(f"  CHOSEN on IS (most negative rho): {pick.metric}/{pick['norm']}  IS rho {pick.IS_rho:+.3f} "
        f"(n {int(pick.IS_n)})  ->  OOS rho {pick.OOS_rho:+.3f} (n {int(pick.OOS_n)}, t {pick.OOS_t:+.2f}, "
        f"p {pick.OOS_p:.4f})")

    # decision-rule form: does abstaining when confident pay?
    say("\n### The inversion as a DECISION RULE — 'skip the argmax when the IS margin is wide'")
    say("  tau = median margin_z on the IS half; on the OOS half compare the argmax pick against "
        "the cell's mean arm, split by margin_z < tau (narrow) vs >= tau (wide).")
    dec = []
    for m in METRICS:
        a = A[(A.metric == m) & A.margin_z.notna()]
        b = B[(B.metric == m) & B.margin_z.notna()]
        if len(a) < 10 or len(b) < 10:
            continue
        tau = float(a.margin_z.median())
        nar, wid = b[b.margin_z < tau], b[b.margin_z >= tau]
        dec.append(dict(metric=m, tau=tau,
                        **{f"narrow_{k}": v for k, v in paired_t(nar.d_rand).items()},
                        **{f"wide_{k}": v for k, v in paired_t(wid.d_rand).items()}))
    D = pd.DataFrame(dec)
    if len(D):
        D.to_csv(OUT / f"{STEM}.decision.csv", index=False)
        say(D.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ---------------- Part B
    say("\n\n## PART B — FRESH OUT-OF-CORPUS grid on real prices (31 arms x 3 panels x 2 rungs)\n")
    panels = load_panels()
    for k, v in panels.items():
        say(f"  panel {k:9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    say("  SMALL439 = the sub-$2B panel with the 44 names whose max 1d move >= 1.0 dropped; "
        "SURVIVORSHIP: current constituents of the screen only (data/SMALL_PANEL_README.md), "
        "and universe_broad.json is likewise today's list — read the CONTRASTS, not the levels.")
    fg, curves = fresh_grid(panels)
    # KEEP paths per arm
    kp = []
    for _, row in fg.iterrows():
        r = curves[(row.panel, row.cost, row.arm)]
        kp.append(keep_paths(r, curves[(row.panel, row.cost, "__SPY__")],
                             curves[(row.panel, row.cost, "__V2__")]))
    fg = pd.concat([fg.reset_index(drop=True), pd.DataFrame(kp)], axis=1)
    fg.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"  fresh grid: {len(fg)} arm-rows, {fg.groupby(['panel', 'cost']).ngroups} cells")

    say("\n### Levels (freshly computed, not quoted from the record)")
    for pname in panels:
        spy = curves[(pname, 10.0, "__SPY__")]
        v2 = curves[(pname, 10.0, "__V2__")]
        ms, mv = metrics(spy.loc[OOS_START:]), metrics(v2.loc[OOS_START:])
        say(f"  {pname:9s} OOS  SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%}   "
            f"RULES v2@10bps {mv['CAGR']:.2%} / {mv['Sharpe']:.4f} / {mv['MaxDD']:.2%}   "
            f"[4b OOS bars: CAGR >= {0.70 * ms['CAGR']:.2%}, MaxDD >= {0.60 * ms['MaxDD']:.2%}]")

    say("\n### The same rho on cells that did not exist when idea 151 ran")
    frows = []
    for (pname, c), cell in fg.groupby(["panel", "cost"]):
        for m in METRICS:
            I, O = cell[f"IS_{m}"].values, cell[f"OOS_{m}"].values
            ok = np.isfinite(I) & np.isfinite(O)
            I, O, A_ = I[ok], O[ok], cell.arm.values[ok]
            order = np.argsort(-I, kind="stable")
            margin = float(I[order[0]] - I[order[1]])
            sd = float(np.std(I, ddof=1))
            ctl = float(O[A_ == "control"][0])
            frows.append(dict(panel=pname, cost=c, metric=m, arm_star=str(A_[order[0]]),
                              margin_raw=margin, margin_z=margin / sd if sd else np.nan,
                              margin_rng=margin / (I.max() - I.min()) if I.max() > I.min() else np.nan,
                              IS_star=float(I[order[0]]), OOS_star=float(O[order[0]]),
                              OOS_mean=float(O.mean()), OOS_ctl=ctl,
                              d_rand=float(O[order[0]] - O.mean()), d_ctl=float(O[order[0]] - ctl)))
    F = pd.DataFrame(frows)
    F.to_csv(OUT / f"{STEM}.freshcells.csv", index=False)
    say(F.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("  per metric (6 cells each — under-powered, reported for completeness):")
    for m in METRICS:
        sub = F[F.metric == m]
        say(f"    {m:6s} d_rand rho(z) {sub.margin_z.rank().corr(sub.d_rand.rank()):+.3f}   "
            f"d_ctl rho(z) {sub.margin_z.rank().corr(sub.d_ctl.rank()):+.3f}   "
            f"argmax == control in {int((sub.arm_star == 'control').sum())} of {len(sub)} cells")
    for dcol in ("d_rand", "d_ctl"):
        for nm, col in (("raw", "margin_raw"), ("z", "margin_z"), ("rng", "margin_rng")):
            s = spearman(F[col], F[dcol])
            mv = F[F.arm_star != "control"]
            s2 = spearman(mv[col], mv[dcol])
            say(f"  fresh corpus, all metrics pooled, {nm:3s}/{dcol}: n {s['n']}  rho {s['rho']:+.3f}  p {s['p']:.3f}"
                f"   | MOVED only: n {s2['n']}  rho {s2['rho']:+.3f}  p {s2['p']:.3f}")
    say("  NOTE: pooling metrics of different units in one rho is the artefact class idea 400 flags; "
        "the per-metric lines above are the honest reading, and d_ctl is degenerate wherever the "
        "argmax IS the control (d_ctl == 0 by construction).")

    say("\n### What the fresh IS-argmax actually bought, per cell (rule 8: chosen on IS only)")
    for (pname, c), cell in fg.groupby(["panel", "cost"]):
        star = cell.loc[cell.IS_Sharpe.idxmax()]
        ctl = cell[cell.arm == "control"].iloc[0]
        say(f"  {pname:9s}@{c:>4.0f}bps  IS-Sharpe argmax = {star.arm:16s} "
            f"OOS {star.OOS_CAGR:6.2%} / {star.OOS_Sharpe:.4f} / {star.OOS_MaxDD:7.2%}   "
            f"control OOS {ctl.OOS_CAGR:6.2%} / {ctl.OOS_Sharpe:.4f} / {ctl.OOS_MaxDD:7.2%}   "
            f"menu-mean OOS Sharpe {cell.OOS_Sharpe.mean():.4f}   "
            f"4a {bool(star.pass4a)} 4b {bool(star.pass4b)} 4b(OOS) {bool(star.pass4b_oos)}")

    say("\n### KEEP paths over the whole fresh grid")
    for c, sub in fg.groupby("cost"):
        say(f"  @{c:.0f} bps: 4a(v2) {int(sub.pass4a.sum())}/{len(sub)}   4b(full) {int(sub.pass4b.sum())}/{len(sub)}   "
            f"4b(OOS window) {int(sub.pass4b_oos.sum())}/{len(sub)}   "
            f"BOTH PATHS {int((sub.pass4a & sub.pass4b).sum())}/{len(sub)}")
    for pname, sub in fg.groupby("panel"):
        say(f"  {pname:9s}: 4a {int(sub.pass4a.sum())}/{len(sub)}  4b {int(sub.pass4b.sum())}/{len(sub)}  "
            f"4b(OOS) {int(sub.pass4b_oos.sum())}/{len(sub)}  BOTH {int((sub.pass4a & sub.pass4b).sum())}/{len(sub)}")
    both = fg[fg.pass4a & fg.pass4b]
    if len(both):
        say("  BOTH-PATHS rows:\n" + both[["panel", "cost", "arm", "CAGR", "Sharpe", "MaxDD",
                                           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(index=False))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    say(f"\nwrote {STEM}.{{census,ledger,rhogrid,perfile,walkforward,decision,grid,freshcells,console}}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
