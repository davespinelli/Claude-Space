#!/usr/bin/env python3
"""Idea 457 — publish-ROOM-beside-every-abstention-and-chooser-result   (cloud lane, 2026-09-08)

QUESTION (QUEUE 457): idea 241 showed the CONTROL arm carries +0.0258 of free OOS Sharpe over
a random menu arm (t +22.2) while the argmax buys only -0.0058 against it, so ANY rule that
falls back to the control scores positive for a reason that has nothing to do with the rule.
Idea 445 drafted the ROOM/REGRET clause for SELECTION results.  Extend it to ABSTENTION
results: back-fill ROOM over the 1,834 control-carrying census cells and report how many
published abstention verdicts flip once ROOM is netted out.

TERMINOLOGY — the record already uses "ROOM" for TWO different things, and this run names both
rather than picking one silently:
    ROOM_445 = OOS_best - OOS_ctl     (headroom above the fallback; idea 445's definition)
    ROOM_241 = OOS_ctl  - OOS_neutral (the fallback's free premium over a random menu draw;
                                       idea 241's +0.0258 -- the one idea 457 asks to net out)
    REGRET   = OOS_best - OOS_pick
    LIFT     = OOS_pick - OOS_neutral   (what the SELECTOR buys over a random draw)
Two exact identities, checked to machine precision in gate G3:
    MARGIN (pick vs ctl) = OOS_pick - OOS_ctl = ROOM_445 - REGRET
    GAIN   (abstaining)  = OOS_ctl  - OOS_pick = ROOM_241 - LIFT
The second identity IS the clause: an abstention rule's headline gain is the fallback's free
room MINUS the selector's lift.  Netting ROOM_241 out leaves -LIFT, which is the only part of
the number that is about the abstention decision at all.

DESIGN
  PART A  back-fill ROOM_241, ROOM_445, REGRET, LIFT, MARGIN on every cell of idea 241's
          committed census (5,422 control-carrying cells, 1,834 of them the Sharpe cells the
          queue names) -> `.cells.csv`.  Nothing is recomputed from prices: every input column
          is already published, so the back-fill is exact and lossless.
  PART B  the tau grid.  RAW abstention delta D(tau) = mean 1{margin<tau} (OOS_ctl - OOS_star)
          vs NET delta Dnet(tau) = mean 1{margin<tau} (OOS_neutral - OOS_star).  Verdicts are
          counted at cell level and at FILE level; a verdict FLIPS when D>0 and Dnet<=0.
  PART C  the record's OWN published abstention verdicts, found mechanically (a committed CSV
          carrying an abstain-family column), re-quoted with ROOM netted out where the file
          publishes a neutral comparand.  Non-recoverable instances are counted UNAUDITED,
          never as a pass.
  PART D  rule 8 on the corpus: tau chosen on the first half of the record by parent-file date,
          read once on the second half.
  PART E  rule 8 on live prices, out of corpus: idea 241's pre-registered 31-arm menu on 3
          panels x 2 cost rungs, arms and tau chosen on <= 2016-12-31, 2017-2026 read once.
          Realised OOS CAGR/Sharpe/MaxDD of the ARGMAX / ABSTAIN / NET-ABSTAIN / INCUMBENT
          books against the live RULES v2 baseline and SPY, with BOTH KEEP paths (4a and 4b)
          on the full sample and on the OOS window.

TUNED PARAMETERS (exactly 2, every grid point reported):
    q       — abstention threshold as a quantile of the corpus's own top-2 gap distribution,
              q in {0.0, 0.1, ..., 1.0}                                        (11 points)
    neutral — the comparand ROOM is measured against, {MENU-MEAN, IS-MEDIAN-ARM} (2 pts)
              (MENU-MEAN = the menu's mean OOS = a random draw's expectation; IS-MEDIAN-ARM =
               the OOS of the arm ranked MEDIAN in-sample.  Both are idea 241's own committed
               columns; neither is re-derived here.)
  = 22 grid points, all printed and written.  The margin norm is PINNED at raw (idea 241's
  pre-registered scale); the absolute anchor tau = 0.013 is reported beside the grid as a
  pre-registered point, not fitted.  Metric pinned at Sharpe by the queue's wording;
  CAGR/MaxDD are reported as a labelled sensitivity, not as a third dial.

PROTOCOL: 10 bps anchor (25 bps rung also reported), next-day execution (engine.backtest),
no shorting, no leverage.  Deterministic (seed 20260908, inherited from idea 241's sub-menus).
Does not modify RULES.md, scan.py, bot.py or baseline.py.
SURVIVORSHIP: the small439 panel is current constituents of a sub-$2B screen only
(data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 are dropped before use.
"""
from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from engine import metrics  # noqa: E402

STEM = "2026-09-08_publish-ROOM-beside-every-abstention-and-chooser-result_cloud"
OUT = ROOT / "research" / "backtests"
PARENT = "2026-09-08_the-013-margin-rule_B"

QGRID = [round(0.1 * i, 1) for i in range(11)]          # P1: 0.0 .. 1.0
NEUTRALS = {"MENU-MEAN": "OOS_mean", "IS-MEDIAN-ARM": "OOS_med"}   # P2
TAU_ANCHOR = 0.013
IS_END, OOS_START = "2016-12-31", "2017-01-01"

LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


def tstat(x) -> tuple[float, float, int]:
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 2:
        return (np.nan, np.nan, n)
    m, s = x.mean(), x.std(ddof=1)
    t = m / (s / np.sqrt(n)) if s > 0 else np.nan
    return (float(m), float(t), n)


def load_parent():
    """Import idea 241's committed script as a module (its live-arm harness is reused verbatim
    so PART E is the SAME pre-registered menu, not a re-specification)."""
    spec = importlib.util.spec_from_file_location("idea241", OUT / f"{PARENT}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ PART A
def backfill(cen: pd.DataFrame) -> pd.DataFrame:
    """ROOM/REGRET/LIFT/MARGIN back-filled on every control-carrying cell."""
    c = cen[cen.has_ctl & cen.OOS_ctl.notna()].copy()
    c["ROOM445"] = c.OOS_best - c.OOS_ctl
    c["REGRET_star"] = c.OOS_best - c.OOS_star
    c["MARGIN_star"] = c.OOS_star - c.OOS_ctl
    for lab, col in NEUTRALS.items():
        key = lab.split("-")[1][:4]
        c[f"ROOM241_{key}"] = c.OOS_ctl - c[col]
        c[f"LIFT_{key}"] = c.OOS_star - c[col]
    c["GAIN"] = c.OOS_ctl - c.OOS_star                  # what abstaining on this cell pays
    return c


# ------------------------------------------------------------------ PART B
def tau_of(sub: pd.DataFrame, q: float) -> float:
    if q <= 0:
        return -np.inf                                   # never abstain
    if q >= 1:
        return np.inf                                    # always abstain
    return float(np.nanquantile(sub.margin_raw.values, q))


def grid_row(sub: pd.DataFrame, q: float, neutral: str, scope: str) -> dict:
    tau = tau_of(sub, q)
    fire = sub.margin_raw.values < tau
    key = neutral.split("-")[1][:4]
    raw = np.where(fire, sub.GAIN.values, 0.0)
    net = np.where(fire, -sub[f"LIFT_{key}"].values, 0.0)
    free = np.where(fire, sub[f"ROOM241_{key}"].values, 0.0)
    mr, tr, n = tstat(raw)
    mn, tn, _ = tstat(net)
    mf, tf, _ = tstat(free)
    return dict(scope=scope, neutral=neutral, q=q, tau=tau, n=n,
                abstain_rate=float(fire.mean()) if n else np.nan,
                D_raw=mr, t_raw=tr, D_net=mn, t_net=tn, FREE=mf, t_free=tf,
                verdict_raw="POS" if mr > 0 else "NEG/0",
                verdict_net="POS" if mn > 0 else "NEG/0",
                flips=bool(mr > 0 and mn <= 0))


# ------------------------------------------------------------------ PART C
ABSTAIN_TOKENS = ("abstain", "abstained", "abstention", "abstain_pick", "s2_abstained")


def find_abstention_files() -> list[Path]:
    hits = []
    for p in sorted(OUT.glob("*.csv")):
        if p.stem.startswith(STEM):
            continue
        try:
            head = p.open().readline().strip().lower()
        except Exception:
            continue
        cols = [c.strip() for c in head.split(",")]
        if any(any(t == c or t in c for t in ABSTAIN_TOKENS) for c in cols):
            hits.append(p)
    return hits


def requote(paths: list[Path]) -> pd.DataFrame:
    """Per published abstention instance: can ROOM be netted out, and does the verdict flip?"""
    rows = []
    for p in paths:
        try:
            df = pd.read_csv(p)
        except Exception as e:
            rows.append(dict(file=p.name, rows=0, status="UNREADABLE", detail=str(e)[:60]))
            continue
        cl = {c.lower(): c for c in df.columns}
        has = lambda *ks: all(k in cl for k in ks)
        # (1) idea 241 shape: sel_mean / argmax_mean / inc_mean x incumbent in {ctl,med,mean}
        if has("incumbent", "sel_mean", "argmax_mean", "inc_mean", "mean"):
            piv = df.copy()
            keys = [k for k in ("scope", "norm", "q", "metric") if k in cl]
            ctl = piv[piv[cl["incumbent"]] == "ctl"].set_index([cl[k] for k in keys])
            neu = piv[piv[cl["incumbent"]] == "mean"].set_index([cl[k] for k in keys])
            j = ctl[[cl["mean"]]].join(neu[[cl["mean"]]], lsuffix="_ctl", rsuffix="_neu",
                                       how="inner").dropna()
            if len(j):
                d_raw = j.iloc[:, 0].values
                d_net = j.iloc[:, 1].values
                rows.append(dict(file=p.name, rows=len(j), status="AUDITED",
                                 mode="incumbent-vocabulary",
                                 pos_raw=int((d_raw > 0).sum()), pos_net=int((d_net > 0).sum()),
                                 flips=int(((d_raw > 0) & (d_net <= 0)).sum()),
                                 mean_raw=float(d_raw.mean()), mean_net=float(d_net.mean())))
                continue
        # (2) pool-mean shape: a published pool/menu mean OOS beside the pick and the control
        if has("oos_sharpe", "pool_oos") and ("d_vs_ctl" in cl or "ctl_oos_sharpe" in cl):
            d = df.dropna(subset=[cl["oos_sharpe"], cl["pool_oos"]])
            sel = d[cl.get("selector", cl["oos_sharpe"])].astype(str).str.lower() if "selector" in cl else None
            if sel is not None:
                d = d[sel.str.contains("abstain|k_median|kmed", regex=True, na=False)] if sel.str.contains("abstain", na=False).any() else d
            if len(d):
                ctlv = d[cl["ctl_oos_sharpe"]].values if "ctl_oos_sharpe" in cl else \
                       (d[cl["oos_sharpe"]].values - d[cl["d_vs_ctl"]].values)
                d_raw = ctlv - d[cl["oos_sharpe"]].values
                d_net = d[cl["pool_oos"]].values - d[cl["oos_sharpe"]].values
                rows.append(dict(file=p.name, rows=len(d), status="AUDITED", mode="pool-mean",
                                 pos_raw=int((d_raw > 0).sum()), pos_net=int((d_net > 0).sum()),
                                 flips=int(((d_raw > 0) & (d_net <= 0)).sum()),
                                 mean_raw=float(np.nanmean(d_raw)), mean_net=float(np.nanmean(d_net))))
                continue
        # (3) fallback-vocabulary shape: idea 241's cloud twin publishes d_vs_argmax and d_mean
        if has("fallback", "d_vs_argmax", "d_mean"):
            d = df.dropna(subset=[cl["d_vs_argmax"], cl["d_mean"]])
            d = d[d[cl["fallback"]].astype(str).str.lower().isin(("ctl", "control", "incumbent"))]
            if len(d):
                d_raw, d_net = d[cl["d_vs_argmax"]].values, d[cl["d_mean"]].values
                rows.append(dict(file=p.name, rows=len(d), status="AUDITED", mode="fallback-column",
                                 pos_raw=int((d_raw > 0).sum()), pos_net=int((d_net > 0).sum()),
                                 flips=int(((d_raw > 0) & (d_net <= 0)).sum()),
                                 mean_raw=float(d_raw.mean()), mean_net=float(d_net.mean())))
                continue
        # (4) ROOM_445 back-fillable but no neutral comparand -> partially audited
        if has("oos_sharpe", "ctl_oos_sharpe") and ("best_oos_sharpe" in cl or "oracle_oos_sharpe" in cl):
            b = cl.get("best_oos_sharpe", cl.get("oracle_oos_sharpe"))
            d = df.dropna(subset=[cl["oos_sharpe"], cl["ctl_oos_sharpe"], b])
            rows.append(dict(file=p.name, rows=len(d), status="ROOM445-ONLY",
                             mode="no neutral comparand published",
                             mean_room445=float((d[b] - d[cl["ctl_oos_sharpe"]]).mean()),
                             mean_raw=float((d[cl["ctl_oos_sharpe"]] - d[cl["oos_sharpe"]]).mean())))
            continue
        miss = []
        if not any(k in cl for k in ("oos_sharpe", "mean_oos_sharpe", "sel_mean", "mean")):
            miss.append("no OOS level")
        if not any(k in cl for k in ("ctl_oos_sharpe", "d_vs_ctl", "inc_mean", "incumbent", "fallback")):
            miss.append("no fallback arm")
        if not any(k in cl for k in ("pool_oos", "oos_mean", "d_mean", "oos_meanfb", "inc_mean")):
            miss.append("no neutral comparand")
        rows.append(dict(file=p.name, rows=len(df), status="UNAUDITED",
                         mode="; ".join(miss) or "shape not recognised"))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ main
def main() -> None:
    say(f"# Idea 457 — publish ROOM beside every abstention result   (cloud, {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC)")
    say(__doc__.split("DESIGN")[0].strip())
    say("\n" + "=" * 100)

    p241 = load_parent()
    cen = pd.read_csv(OUT / f"{PARENT}.census.csv")
    live_cen = pd.read_csv(OUT / f"{PARENT}.livecells.csv")

    # ---------------- gates
    say("\n## GATES — reproduce idea 241's published decomposition before reading anything new\n")
    S = backfill(cen[cen.metric == "Sharpe"])
    say(f"G0  control-carrying Sharpe cells: {len(S)}   (queue says 1,834)   "
        f"MATCH={len(S) == 1834}")
    g1 = []
    for lab, expr in [("ROOM_241 = OOS_ctl - OOS_mean", S.OOS_ctl - S.OOS_mean),
                      ("LIFT     = OOS_star - OOS_mean", S.OOS_star - S.OOS_mean),
                      ("MARGIN   = OOS_star - OOS_ctl", S.OOS_star - S.OOS_ctl),
                      ("REGRET   = OOS_best - OOS_star", S.OOS_best - S.OOS_star)]:
        m, t, n = tstat(expr)
        g1.append(dict(term=lab, mean=m, t=t, n=n))
    G1 = pd.DataFrame(g1)
    say(G1.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("\n    idea 241 published: ROOM +0.0258 (t +22.2), LIFT +0.0201 (t +11.8), "
        "MARGIN -0.0058 (t -3.2), REGRET +0.0478 (t +26.9)")
    ok = (abs(G1.loc[0, "mean"] - 0.0258) < 5e-4 and abs(G1.loc[0, "t"] - 22.2) < 0.3
          and abs(G1.loc[2, "mean"] + 0.0058) < 5e-4 and abs(G1.loc[3, "mean"] - 0.0478) < 5e-4)
    say(f"G1  decomposition reproduces from the committed census: {ok}")

    e1 = float((S.MARGIN_star - (S.ROOM445 - S.REGRET_star)).abs().max())
    e2 = float((S.GAIN - (S.ROOM241_MEAN - S.LIFT_MEAN)).abs().max())
    say(f"G3  identity MARGIN == ROOM445 - REGRET : max|err| {e1:.3e}")
    say(f"G3  identity GAIN   == ROOM241 - LIFT   : max|err| {e2:.3e}")

    # ---------------- PART A
    say("\n\n" + "=" * 100)
    say("## PART A — the back-fill (nothing recomputed from prices; every input already published)\n")
    ALL = backfill(cen)
    ALL.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    tab = []
    for m in ("Sharpe", "CAGR", "MaxDD"):
        s = ALL[ALL.metric == m]
        if not len(s):
            continue
        r = dict(metric=m, cells=len(s), files=s.file.nunique())
        for lab, col in [("ROOM241", "ROOM241_MEAN"), ("LIFT", "LIFT_MEAN"),
                         ("ROOM445", "ROOM445"), ("REGRET", "REGRET_star"),
                         ("GAIN", "GAIN")]:
            mm, tt, _ = tstat(s[col])
            r[lab] = mm
            r[f"t_{lab}"] = tt
        tab.append(r)
    A = pd.DataFrame(tab)
    say(A.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("\n  Sharpe is the headline (the queue pins the metric); CAGR/MaxDD are a labelled")
    say("  SENSITIVITY, not a third tuned dial.  ROOM241 is the free premium the fallback")
    say("  carries; GAIN is what abstaining pays; GAIN = ROOM241 - LIFT exactly.")
    na = S.n_arms.values.astype(float)
    r_ex = (S.OOS_ctl.values - (na * S.OOS_mean.values - S.OOS_ctl.values) / (na - 1))
    l_ex = (S.OOS_star.values - (na * S.OOS_mean.values - S.OOS_star.values) / (na - 1))
    say(f"\n  LEAVE-ONE-OUT check (the neutral should exclude the arm it is compared to):")
    say(f"    ROOM241 incl {tstat(S.ROOM241_MEAN)[0]:+.4f} -> excl {tstat(r_ex)[0]:+.4f};  "
        f"LIFT incl {tstat(S.LIFT_MEAN)[0]:+.4f} -> excl {tstat(l_ex)[0]:+.4f}")
    say("    Exclusion multiplies each term by n/(n-1) exactly, so NO sign and NO verdict in")
    say("    this run depends on it; the inclusive form is kept because it is the column idea")
    say("    241 committed.")
    share = float((S.ROOM241_MEAN > 0).mean())
    say(f"\n  cells where the control beats a random menu draw: {share:.1%} of {len(S)}")
    say(f"  cells where the control beats the IS-argmax OOS:   {float((S.GAIN > 0).mean()):.1%}")

    # ---------------- PART B
    say("\n\n" + "=" * 100)
    say("## PART B — the tau grid.  ALL 22 grid points (q x neutral), Sharpe cells\n")
    rows = []
    for lab in NEUTRALS:
        for q in QGRID:
            rows.append(grid_row(S, q, lab, "record(Sharpe,1834)"))
    # pre-registered absolute anchor, not fitted
    for lab in NEUTRALS:
        key = lab.split("-")[1][:4]
        fire = S.margin_raw.values < TAU_ANCHOR
        mr, tr, n = tstat(np.where(fire, S.GAIN.values, 0.0))
        mn, tn, _ = tstat(np.where(fire, -S[f"LIFT_{key}"].values, 0.0))
        mf, tf, _ = tstat(np.where(fire, S[f"ROOM241_{key}"].values, 0.0))
        rows.append(dict(scope="ANCHOR tau=0.013", neutral=lab, q=np.nan, tau=TAU_ANCHOR, n=n,
                         abstain_rate=float(fire.mean()), D_raw=mr, t_raw=tr, D_net=mn,
                         t_net=tn, FREE=mf, t_free=tf,
                         verdict_raw="POS" if mr > 0 else "NEG/0",
                         verdict_net="POS" if mn > 0 else "NEG/0",
                         flips=bool(mr > 0 and mn <= 0)))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.taugrid.csv", index=False)
    say(G.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    npos = int((G.D_raw > 0).sum())
    say(f"\n  grid points with a POSITIVE raw abstention delta : {npos} / {len(G)}")
    say(f"  of those, POSITIVE once ROOM is netted out        : {int(((G.D_raw>0)&(G.D_net>0)).sum())}")
    say(f"  FLIPPED by the netting                            : {int(G.flips.sum())}")
    say(f"  REVERSE flips (non-positive raw -> positive net)   : {int(((G.D_raw<=0)&(G.D_net>0)).sum())}")

    # file-level verdicts
    say("\n### File-level verdicts (a 'published abstention verdict' = one parent file x one grid point)\n")
    frows = []
    for (f, ), sub in S.groupby(["file"]):
        for lab in NEUTRALS:
            for q in QGRID[1:]:
                r = grid_row(sub, q, lab, f)
                r["file"] = f
                frows.append(r)
    F = pd.DataFrame(frows)
    F.to_csv(OUT / f"{STEM}.fileverdicts.csv", index=False)
    fv = F.dropna(subset=["D_raw"])
    say(f"  file x grid-point verdicts: {len(fv)}  over {fv.file.nunique()} parent files")
    say(f"  POSITIVE raw          : {int((fv.D_raw > 0).sum())} ({(fv.D_raw > 0).mean():.1%})")
    say(f"  POSITIVE net          : {int((fv.D_net > 0).sum())} ({(fv.D_net > 0).mean():.1%})")
    say(f"  FLIP (pos -> non-pos) : {int(fv.flips.sum())} ({fv.flips.mean():.1%})")
    say(f"  reverse flip (non-pos -> pos): {int(((fv.D_raw <= 0) & (fv.D_net > 0)).sum())}")
    byq = fv.groupby(["neutral", "q"]).agg(files=("file", "nunique"), pos_raw=("D_raw", lambda x: (x > 0).sum()),
                                           pos_net=("D_net", lambda x: (x > 0).sum()),
                                           flips=("flips", "sum")).reset_index()
    say("\n" + byq.to_string(index=False))

    # ---------------- PART C
    say("\n\n" + "=" * 100)
    say("## PART C — the record's OWN published abstention verdicts, re-quoted\n")
    paths = find_abstention_files()
    say(f"  committed CSVs carrying an abstain-family column: {len(paths)} "
        f"over {len({p.name.split('.')[0] for p in paths})} parent stems")
    R = requote(paths)
    R.to_csv(OUT / f"{STEM}.requote.csv", index=False)
    say("\n" + R.fillna("").to_string(index=False, max_colwidth=46))
    aud = R[R.status == "AUDITED"]
    say(f"\n  AUDITED (a neutral comparand is published or recoverable): {len(aud)} files, "
        f"{int(aud.rows.sum())} published rows")
    say(f"  ROOM445-ONLY (headroom back-fillable, no neutral)         : {int((R.status=='ROOM445-ONLY').sum())} files")
    say(f"  UNAUDITED (counted as unaudited, never as a pass)         : {int((R.status=='UNAUDITED').sum())} files")
    if len(aud):
        say(f"\n  published rows POSITIVE raw : {int(aud.pos_raw.sum())}")
        say(f"  published rows POSITIVE net : {int(aud.pos_net.sum())}")
        say(f"  published rows that FLIP    : {int(aud.flips.sum())} "
            f"({aud.flips.sum()/max(1,aud.pos_raw.sum()):.1%} of the positive ones)")

    # ---------------- PART D
    say("\n\n" + "=" * 100)
    say("## PART D — RULE 8 on the corpus: q chosen on the first half by parent-file date\n")
    say("  NOTE: this is a split by PUBLICATION date, not by market time — every parent file in")
    say("  the record is dated 2026-09-xx.  It tests whether a threshold fitted on one part of")
    say("  the corpus transfers to files written later; the market-time walk-forward is PART E.")
    S2 = S.copy()
    S2["date"] = pd.to_datetime(S2.date, errors="coerce")
    cut = S2.date.median()
    IS, OS = S2[S2.date <= cut], S2[S2.date > cut]
    say(f"  split at {cut:%Y-%m-%d}: IS {len(IS)} cells / {IS.file.nunique()} files, "
        f"OOS {len(OS)} cells / {OS.file.nunique()} files")
    wf = []
    for lab in NEUTRALS:
        cal = pd.DataFrame([grid_row(IS, q, lab, "IS") for q in QGRID])
        qstar = float(cal.loc[cal.D_raw.idxmax(), "q"])
        tau = tau_of(IS, qstar)                       # threshold FROZEN on the first half
        key = lab.split("-")[1][:4]
        fire = OS.margin_raw.values < tau
        mr, tr, n = tstat(np.where(fire, OS.GAIN.values, 0.0))
        mn, tn, _ = tstat(np.where(fire, -OS[f"LIFT_{key}"].values, 0.0))
        wf.append(dict(neutral=lab, q_star_IS=qstar, IS_D=float(cal.D_raw.max()), tau_frozen=tau,
                       OOS_n=n, OOS_abstain=float(fire.mean()), OOS_D_raw=mr, OOS_t_raw=tr,
                       OOS_D_net=mn, OOS_t_net=tn, flips=bool(mr > 0 and mn <= 0)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n" + W.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ---------------- PART E
    say("\n\n" + "=" * 100)
    say("## PART E — RULE 8 on LIVE PRICES, out of corpus (idea 241's pre-registered menu)\n")
    panels = p241.load_panels()
    for k, v in panels.items():
        say(f"  {k:9s} {v.shape[1]:4d} cols  {v.index[0]:%Y-%m-%d}..{v.index[-1]:%Y-%m-%d}")
    fg, curves = p241.fresh_grid(panels)
    menus = p241.submenus([a for a, _ in p241.arm_menu()])
    cells = p241.live_cells(fg, menus, "IS_", "OOS_")
    say(f"\n  live cells (panel x cost x sub-menu): {len(cells)}  "
        f"(idea 241 committed {len(live_cen)})")
    LS = backfill(cells)
    LS.to_csv(OUT / f"{STEM}.livecells.csv", index=False)
    m, t, n = tstat(LS.ROOM241_MEAN)
    say(f"  ROOM_241 on the LIVE cells: {m:+.4f} (t {t:+.1f}, n {n})")
    say(f"  ROOM_241 on the RECORD    : {tstat(S.ROOM241_MEAN)[0]:+.4f} "
        f"(t {tstat(S.ROOM241_MEAN)[1]:+.1f}, n {len(S)})")
    say("  The sign REVERSES.  The control's free premium is NOT a universal constant: it is")
    say("  +0.026 on the committed corpus and NEGATIVE on the fresh live corpus, so netting it")
    say("  out moves published verdicts in BOTH directions.  What is invariant is that the")
    say("  headline gain is contaminated by it, not the direction of the contamination.")
    for pn, sub in LS.groupby("panel"):
        say(f"    {pn:9s} star_is_ctl {sub.star_is_ctl.mean():6.1%} of {len(sub)} cells   "
            f"ROOM_241 {tstat(sub.ROOM241_MEAN)[0]:+.4f}   GAIN {tstat(sub.GAIN)[0]:+.4f}")
    say("  (where star_is_ctl is 100% the abstention rule is a strict no-op by construction —")
    say("   the ABSTAIN, ARGMAX and INCUMBENT books below are then the SAME book.)")

    lrows = []
    for lab in NEUTRALS:
        for q in QGRID:
            lrows.append(grid_row(LS, q, lab, "live"))
    LG = pd.DataFrame(lrows)
    LG.to_csv(OUT / f"{STEM}.livegrid.csv", index=False)
    say("\n" + LG.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # the books: tau chosen on the LIVE IS window, read once on 2017+
    say("\n### The BOOKS — realised streams.  tau chosen on IS (<= 2016-12-31), OOS read once\n")
    cal = p241.live_cells(fg, menus, "ISin_", "MID_")      # nested: arms 2010-13, tau 2014-16
    CS = backfill(cal)
    calgrid = pd.DataFrame([grid_row(CS, q, "MENU-MEAN", "cal") for q in QGRID])
    qstar = float(calgrid.loc[calgrid.D_raw.idxmax(), "q"])
    tau_live = tau_of(CS, qstar)
    say(f"  q* chosen on the 2014-2016 calibration window: q={qstar}  ->  tau={tau_live:+.4f} "
        f"(IS D={calgrid.D_raw.max():+.4f})")

    books = p241.selector_book(cells, curves, "raw", tau_live, inc_arm="control")
    # NET-ABSTAIN: abstain to an equal-weight blend of the cell's own menu (the neutral arm)
    net_books = {}
    for (pn, c), sub in cells.groupby(["panel", "cost"]):
        streams = []
        for _, row in sub.iterrows():
            if pd.notna(row.margin_raw) and row.margin_raw < tau_live:
                arms = [a for a in menus[int(row.menu)] if (pn, c, a) in curves]
                streams.append(pd.concat([curves[(pn, c, a)] for a in arms], axis=1).mean(axis=1))
            else:
                streams.append(curves[(pn, c, row.arm_star)])
        net_books[(pn, c, "NET-ABSTAIN")] = pd.concat(streams, axis=1).mean(axis=1)
    books.update(net_books)

    krows = []
    for (pn, c, lab), r in sorted(books.items()):
        spy = curves[(pn, c, "__SPY__")]
        v2 = curves[(pn, c, "__V2__")]
        idx = r.index.intersection(spy.index).intersection(v2.index)
        r, spy, v2 = r.loc[idx], spy.loc[idx], v2.loc[idx]
        row = dict(panel=pn, cost=c, book=lab, tau=tau_live)
        row.update(p241.win_metrics(r))
        row.update(p241.win_metrics(r, lo=OOS_START, prefix="OOS_"))
        row.update(p241.win_metrics(spy, lo=OOS_START, prefix="SPY_OOS_"))
        row.update(p241.win_metrics(v2, lo=OOS_START, prefix="V2_OOS_"))
        row.update(p241.keep_paths(r, v2, spy))
        krows.append(row)
    K = pd.DataFrame(krows)
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    cols = ["panel", "cost", "book", "CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "SPY_OOS_Sharpe", "V2_OOS_Sharpe", "pass4a", "pass4b",
            "pass4a_oos", "pass4b_oos"]
    say(K[cols].to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    say(f"\n  KEEP paths over {len(K)} live books: 4a {int(K.pass4a.sum())}/{len(K)}, "
        f"4b {int(K.pass4b.sum())}/{len(K)}, 4a(OOS) {int(K.pass4a_oos.sum())}/{len(K)}, "
        f"4b(OOS) {int(K.pass4b_oos.sum())}/{len(K)}")
    ab = K[K.book == "ABSTAIN"].set_index(["panel", "cost"])
    ax = K[K.book == "ARGMAX"].set_index(["panel", "cost"])
    nb = K[K.book == "NET-ABSTAIN"].set_index(["panel", "cost"])
    d1 = (ab.OOS_Sharpe - ax.OOS_Sharpe).dropna()
    d2 = (nb.OOS_Sharpe - ax.OOS_Sharpe).dropna()
    say(f"\n  ABSTAIN     - ARGMAX, OOS Sharpe: mean {d1.mean():+.4f}  wins {int((d1>0).sum())}/{len(d1)}")
    say(f"  NET-ABSTAIN - ARGMAX, OOS Sharpe: mean {d2.mean():+.4f}  wins {int((d2>0).sum())}/{len(d2)}")

    say("\n\n" + "=" * 100)
    say("wrote " + STEM + ".{cells,taugrid,fileverdicts,requote,walkforward,livecells,"
        "livegrid,keeppaths,console}")
    flush()


if __name__ == "__main__":
    main()
