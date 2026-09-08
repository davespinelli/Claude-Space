#!/usr/bin/env python3
"""Idea 456 — is-the-MID-TERCILE-peak-a-real-shape-or-a-menu-size-artefact (cloud, 2026-09-08)

QUESTION (queue, verbatim intent)
  Idea 241 found the abstention payoff is NON-MONOTONE in the top-2 IS gap on 1,203 record
  cells (narrow +0.0093, mid +0.0242, wide -0.0072) with rank correlation ~0, which no
  MINIMUM-threshold rule can exploit.  Test whether the mid-tercile peak survives conditioning
  on menu size |A| and on the ladder's own IS spread, and whether a BAND rule (abstain only in
  the middle) transfers under rule 8 where the threshold rule does not.
  Max 2 tuned params: (tercile cut low, tercile cut high) = the band's two edges.

PRE-REGISTERED PREDICTIONS (written before any number in parts A-D was read)
  R1  The pooled mid-tercile peak is a COMPOSITION artefact of menu size.  A wide menu has a
      mechanically smaller top-2 gap (more order statistics packed into the same IS spread)
      AND more room between the control and the argmax, so |A| moves the margin and the
      payoff together.  Within a fixed |A| stratum the peak should shrink or vanish.
  R2  If any shape survives within strata it will be the ordered half of the parent's finding
      — the WIDE tercile is negative — not the mid peak.
  R3  The BAND rule will look better than the threshold rule IN SAMPLE by construction (it is
      the threshold family plus one more degree of freedom, and it can buy the parent's own
      terciles) and will NOT transfer under rule 8, because idea 241 already showed
      Spearman(margin, gain) ~ 0 and idea 229/446 showed the payoff is ROOM the control
      carries, which the margin does not sort.
  R4  On the live frame the band will lose to the raw argmax on u56 (where idea 241 found gain
      negative in all three terciles) and be a strict NO-OP on broad136/small439 (idea 458:
      the ungated control is the IS argmax there, so abstention cannot move a cell).

WHAT THIS RUN DOES (declared before any number is read)
  G   GATES.  (G1) The parent's tercile table is REPRODUCED EXACTLY off its committed
      `2026-09-08_the-013-margin-rule_B.census.csv` before anything new is read; the run
      aborts its headline if the three means do not match `.sorting.csv` to 1e-12.
      (G2) The cost-rung identity net(c) = gross - turnover*c/1e4, imported from the parent.
      (G3) A FRESH re-harvest of the whole committed record is run beside the parent's frozen
      census and both corpora are carried through every table, so no result rests on the
      parent's file list alone.

  A   CONDITIONING (the queue's first question).  MOVED cells only (argmax != control; the
      abstention is a no-op elsewhere).  gain = OOS_ctl - OOS_star.  The pooled tercile shape
      is recomputed WITHIN strata of menu size |A| and WITHIN strata of the ladder's own IS
      spread (sd, recovered exactly as margin_raw/margin_z).  Then the decisive test: gain is
      demeaned within stratum and the margin is re-ranked within stratum, and the pooled
      terciles are read again.  A peak that is a composition artefact dies here; a peak that
      is a shape does not.  Strata: |A| bins, sd terciles, FILE, and FILE x |A|.

  B   THE BAND RULE (TUNED PARAMETERS 1 AND 2 = the band's two edges).  Abstain iff
      qlo <= F(margin) < qhi, where F is the corpus's own margin CDF.  All 55 grid points
      (qlo, qhi) on a 0.1 ladder are reported, with the threshold family (qlo = 0) and
      always-abstain (0, 1) marked inside the same table.  D = mean[OOS(rule) - OOS(argmax)],
      instance-pooled AND file-clustered.  `norm` in {raw, z, rng} is a LABELLED SENSITIVITY,
      not a third tuned dial: the headline is `raw`, the parent's own scale.

  C   RULE 8 ON THE CORPUS.  Edges chosen on the FIRST half of the record by parent-file date
      and read once on the second half; plus 20 seeded random FILE splits.  The band is scored
      against three comparands fitted the SAME way: the raw argmax (do nothing), the best
      threshold rule, and always-abstain.  A band that only wins where it was fitted is a KILL.

  D   RULE 8 ON LIVE PRICES, OUT OF CORPUS.  The parent's live frame is IMPORTED and re-run:
      31 arms x 3 panels x 2 cost rungs, 200 seeded sub-menus per (panel, cost), each menu
      containing the control so the abstention is defined.  Edges are chosen on the
      CALIBRATION frame (arms ranked on <= 2013, payoff read 2014-2016) and applied UNTOUCHED
      to the headline frame (arms ranked <= 2016, payoff 2017+); the edges chosen on the
      RECORD corpus in part C are ALSO applied untouched, a genuine out-of-universe transfer.
      Pooled equal-weight books for ARGMAX / BAND / INCUMBENT go through BOTH KEEP PATHS
      (4a vs the live RULES v2 book, 4b vs SPY), full sample + halves + OOS.

SURVIVORSHIP.  The small panel is current constituents of a sub-$2B screen only (483 names,
tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first) and the broad panel is
current constituents (PROTOCOL 9).  Levels are upward-biased; only same-cell contrasts (rule
minus argmax, on the same ladder and the same days) are read.  The record corpus inherits
whatever bias each source run carried; it is a re-reading, not new evidence about returns.

Costs 10 and 25 bps, next-day execution (PROTOCOL 2).  Deterministic (seeds fixed).
Artefacts: .console.txt, .strata.csv, .bandgrid.csv, .walkforward.csv, .livecells.csv,
           .livegrid.csv, .keeppaths.csv, .result.md
Nothing outside research/ is touched; RULES.md, scan.py, bot.py, baseline.py untouched.
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

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-08_the-mid-tercile-band_cloud"
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


P241 = _load(PARENT, "i241B")            # the parent: harvest, cell_row, live frame, keep_paths
paired_t = P241.paired_t
NORMCOL = P241.NORMCOL
NORMS = P241.NORMS
OOS_START = P241.OOS_START

QLADDER = [round(0.1 * i, 1) for i in range(11)]        # 0.0 .. 1.0
BAND_GRID = [(lo, hi) for lo in QLADDER[:-1] for hi in QLADDER if hi > lo]   # 55 points
SEEDS = 20


# --------------------------------------------------------------------------- corpus shaping
def moved(cen: pd.DataFrame) -> pd.DataFrame:
    """The cells on which an abstention can do anything at all: Sharpe cells that carry a
    labelled control arm which is NOT itself the IS argmax.  gain = what abstaining pays."""
    s = cen[(cen.metric == "Sharpe") & cen.OOS_ctl.notna() & cen.OOS_star.notna()].copy()
    s = s[~s.star_is_ctl.astype(bool)].copy()
    s["gain"] = s.OOS_ctl - s.OOS_star
    s["is_sd"] = s.margin_raw / s.margin_z.replace(0, np.nan)       # exact: margin_z = m/sd
    s["is_rng"] = s.margin_raw / s.margin_rng.replace(0, np.nan)
    return s


def abin(n: int) -> str:
    if n <= 4:
        return "A:3-4"
    if n <= 6:
        return "B:5-6"
    if n <= 10:
        return "C:7-10"
    if n <= 16:
        return "D:11-16"
    return "E:17+"


def terciles(x: pd.Series) -> pd.Series:
    return pd.qcut(x, 3, labels=["narrow", "mid", "wide"], duplicates="drop")


def shape_of(m: dict) -> str:
    n, mi, w = m["narrow"], m["mid"], m["wide"]
    if mi > n and mi > w:
        return "MID-PEAK"
    if n >= mi >= w:
        return "monotone-down"
    if n <= mi <= w:
        return "monotone-up"
    return "MID-TROUGH" if (mi < n and mi < w) else "other"


def tercile_table(d: pd.DataFrame, col: str, gaincol: str = "gain", scope: str = "") -> dict:
    if len(d) < 30 or d[col].nunique() < 3:
        return {}
    t = terciles(d[col])
    means, ts, ns = {}, {}, {}
    for lab, g in d.groupby(t, observed=True):
        r = paired_t(g[gaincol])
        means[str(lab)] = r["mean"]
        ts[str(lab)] = r["t"]
        ns[str(lab)] = r["n"]
    if set(means) != {"narrow", "mid", "wide"}:
        return {}
    rho = float(d[col].rank().corr(d[gaincol].rank()))
    return dict(scope=scope, n=len(d), narrow=means["narrow"], mid=means["mid"],
                wide=means["wide"], t_narrow=ts["narrow"], t_mid=ts["mid"], t_wide=ts["wide"],
                n_narrow=ns["narrow"], n_mid=ns["mid"], n_wide=ns["wide"],
                spearman=rho, shape=shape_of(means))


# --------------------------------------------------------------------------- the band rule
def band_delta(d: pd.DataFrame, col: str, lo: float, hi: float, gaincol: str = "gain") -> dict:
    """D = mean[ OOS(rule) - OOS(argmax) ].  Abstaining pays `gain` on that cell and 0
    elsewhere, so D = mean(gain * 1[abstain]) exactly."""
    q = d[col].rank(pct=True, method="average")
    ab = (q > lo) & (q <= hi) if lo > 0 else (q <= hi)
    dlt = np.where(ab, d[gaincol].values, 0.0)
    r = paired_t(dlt)
    # file-clustered: equal weight per parent file
    fc = pd.Series(dlt, index=d.index).groupby(d.file).mean()
    rf = paired_t(fc)
    r.update(abstain=float(ab.mean()), n_files=int(d.file.nunique()),
             fc_mean=rf["mean"], fc_t=rf["t"], fc_W=rf["W"], fc_L=rf["L"])
    return r


def band_grid(d: pd.DataFrame, norm: str = "raw", scope: str = "") -> pd.DataFrame:
    col = NORMCOL[norm]
    dd = d[d[col].notna()]
    rows = []
    for lo, hi in BAND_GRID:
        r = band_delta(dd, col, lo, hi)
        fam = "THRESHOLD" if lo == 0.0 else "BAND"
        if (lo, hi) == (0.0, 1.0):
            fam = "ALWAYS-ABSTAIN"
        rows.append(dict(scope=scope, norm=norm, qlo=lo, qhi=hi, family=fam, **r))
    return pd.DataFrame(rows)


def fit_band(cal: pd.DataFrame, norm: str, family: str) -> tuple[float, float]:
    """Argmax of in-sample D over the declared family.  Ties broken by the narrower band."""
    g = band_grid(cal, norm)
    g = g[g.family == family] if family != "ANY" else g[g.family != "ALWAYS-ABSTAIN"]
    if not len(g) or g["mean"].isna().all():
        return (0.0, 0.0)
    g = g.sort_values(["mean", "abstain"], ascending=[False, True])
    return float(g.iloc[0].qlo), float(g.iloc[0].qhi)


def apply_band(test: pd.DataFrame, norm: str, lo: float, hi: float) -> dict:
    col = NORMCOL[norm]
    dd = test[test[col].notna()]
    if not len(dd):
        return dict(n=0, mean=np.nan, t=np.nan, abstain=np.nan)
    return band_delta(dd, col, lo, hi)


# --------------------------------------------------------------------------- main
def main() -> None:
    say("=" * 100)
    say("IDEA 456 — is the MID-TERCILE peak a real shape or a MENU-SIZE artefact?")
    say("cloud, 2026-09-08.  PROTOCOL 10 bps anchor, next-day execution, rule 8 everywhere.")
    say("Two tuned parameters: the band's two edges (qlo, qhi).  All 55 grid points reported.")
    say("=" * 100)

    # ---------------------------------------------------------------- GATES
    say("\n## GATES (passed before any new number is read)\n")
    cen_frozen = pd.read_csv(OUT / f"{PARENT}.census.csv")
    S0 = moved(cen_frozen)
    ref = pd.read_csv(OUT / f"{PARENT}.sorting.csv")
    ref = ref[(ref.scope == "RECORD")]
    ok = True
    for norm in NORMS:
        tt = tercile_table(S0, NORMCOL[norm], scope=f"RECORD/{norm}")
        rr = ref[ref.norm == norm].set_index("tercile")["mean"]
        d = max(abs(tt[k] - rr[k]) for k in ("narrow", "mid", "wide"))
        ok &= (d < 1e-12) and (tt["n"] == int(ref[ref.norm == norm]["n"].sum()))
        say(f"  [G1/{norm:3s}] reproduce parent terciles  narrow {tt['narrow']:+.4f}  "
            f"mid {tt['mid']:+.4f}  wide {tt['wide']:+.4f}  rho {tt['spearman']:+.4f}  "
            f"n {tt['n']}  max|diff vs .sorting.csv| {d:.2e}")
    say(f"  [G1] EXACT REPRODUCTION: {'PASS' if ok else 'FAIL'}  "
        f"(MOVED cells {len(S0)}, files {S0.file.nunique()})")
    if not ok:
        say("  [G1] FAILED — the parent's own numbers do not reproduce; everything below is void.")

    g1 = P241.gate_cost_identity(P241.load_universe())
    say(f"  [G2] cost-rung identity  net(25bps) == gross - TO*25/1e4   max|d| = {g1:.3e}")

    cen_fresh, led = P241.harvest()
    S1 = moved(cen_fresh)
    say(f"  [G3] FRESH re-harvest of the committed record: files scanned {len(led)}, "
        f"ADMITTED {int((led.status == 'ADMITTED').sum())}, census rows {len(cen_fresh)}, "
        f"MOVED Sharpe cells {len(S1)} over {S1.file.nunique()} files "
        f"(parent's frozen corpus: {len(S0)} over {S0.file.nunique()})")
    say("\n[t-STAT CAVEAT, stated once] cells inside one file share an arm ladder, so a paired t "
        "over instances treats correlated cells as independent and is INFLATED.  Every headline "
        "is therefore quoted instance-pooled AND file-clustered (equal weight per file).")
    flush()

    CORPORA = {"FROZEN(parent)": S0, "FRESH(today)": S1}

    # ---------------------------------------------------------------- PART A
    say("\n\n## PART A — DOES THE MID PEAK SURVIVE CONDITIONING?\n")
    strata_rows = []

    say("### A1. The pooled shape, both corpora, all three margin scales")
    for cname, S in CORPORA.items():
        for norm in NORMS:
            tt = tercile_table(S, NORMCOL[norm], scope=f"{cname}/pooled/{norm}")
            strata_rows.append(dict(corpus=cname, stratum="POOLED", level="ALL",
                                    norm=norm, **tt))
            say(f"  {cname:15s} {norm:3s}  narrow {tt['narrow']:+.4f}  mid {tt['mid']:+.4f}  "
                f"wide {tt['wide']:+.4f}  rho {tt['spearman']:+.4f}  n {tt['n']:5d}  "
                f"-> {tt['shape']}")

    say("\n### A2. Is the margin CONFOUNDED with menu size |A| and with the ladder's IS spread?")
    for cname, S in CORPORA.items():
        for col, lab in ((NORMCOL["raw"], "margin_raw"), ("gain", "gain")):
            r1 = float(S["n_arms"].rank().corr(S[col].rank()))
            r2 = float(S["is_sd"].rank().corr(S[col].rank()))
            say(f"  {cname:15s} spearman(|A|, {lab:10s}) {r1:+.4f}    "
                f"spearman(IS sd, {lab:10s}) {r2:+.4f}")
    say("  -> if |A| moves BOTH the margin and the payoff, the pooled tercile shape is a "
        "composition statistic, not a shape.")

    say("\n### A3. The tercile shape WITHIN each menu-size stratum (terciles cut inside the stratum)")
    for cname, S in CORPORA.items():
        S = S.copy()
        S["Abin"] = S.n_arms.map(abin)
        for lev, g in S.groupby("Abin"):
            tt = tercile_table(g, NORMCOL["raw"], scope=f"{cname}/|A|={lev}")
            if not tt:
                say(f"  {cname:15s} |A| {lev:6s}  n {len(g):5d}  (too few cells / ties)")
                continue
            strata_rows.append(dict(corpus=cname, stratum="MENU_SIZE", level=lev,
                                    norm="raw", **tt))
            say(f"  {cname:15s} |A| {lev:6s}  n {tt['n']:5d}  narrow {tt['narrow']:+.4f}  "
                f"mid {tt['mid']:+.4f}  wide {tt['wide']:+.4f}  rho {tt['spearman']:+.4f}  "
                f"-> {tt['shape']}")

    say("\n### A4. The tercile shape WITHIN each IS-spread stratum (sd of the ladder's IS Sharpes)")
    for cname, S in CORPORA.items():
        S = S.copy()
        S["SDbin"] = pd.qcut(S.is_sd, 3, labels=["sd:low", "sd:mid", "sd:high"],
                             duplicates="drop")
        for lev, g in S.groupby("SDbin", observed=True):
            tt = tercile_table(g, NORMCOL["raw"], scope=f"{cname}/{lev}")
            if not tt:
                continue
            strata_rows.append(dict(corpus=cname, stratum="IS_SPREAD", level=str(lev),
                                    norm="raw", **tt))
            say(f"  {cname:15s} {str(lev):7s}  n {tt['n']:5d}  narrow {tt['narrow']:+.4f}  "
                f"mid {tt['mid']:+.4f}  wide {tt['wide']:+.4f}  rho {tt['spearman']:+.4f}  "
                f"-> {tt['shape']}")

    say("\n### A5. THE DECISIVE TEST — demean the payoff and re-rank the margin WITHIN strata")
    say("  If the pooled peak is composition, it dies once every comparison is inside a stratum.")
    for cname, S in CORPORA.items():
        S = S.copy()
        S["Abin"] = S.n_arms.map(abin)
        S["SDbin"] = pd.qcut(S.is_sd, 3, labels=False, duplicates="drop")
        S["FA"] = S.file.astype(str) + "|" + S.Abin
        for skey, slab in (("Abin", "within |A| bin"), ("SDbin", "within IS-sd tercile"),
                           ("file", "within FILE"), ("FA", "within FILE x |A|")):
            g = S.copy()
            g["gain_dm"] = g.gain - g.groupby(skey)["gain"].transform("mean")
            g["m_rk"] = g.groupby(skey)["margin_raw"].rank(pct=True, method="average")
            tt = tercile_table(g, "m_rk", gaincol="gain_dm", scope=f"{cname}/{slab}")
            if not tt:
                continue
            strata_rows.append(dict(corpus=cname, stratum="DEMEANED", level=slab,
                                    norm="raw", **tt))
            say(f"  {cname:15s} {slab:20s}  n {tt['n']:5d}  narrow {tt['narrow']:+.4f} "
                f"(t {tt['t_narrow']:+.1f})  mid {tt['mid']:+.4f} (t {tt['t_mid']:+.1f})  "
                f"wide {tt['wide']:+.4f} (t {tt['t_wide']:+.1f})  -> {tt['shape']}")

    ST = pd.DataFrame(strata_rows)
    ST.to_csv(OUT / f"{STEM}.strata.csv", index=False)
    flush()

    # ---------------------------------------------------------------- PART B
    say("\n\n## PART B — THE BAND RULE: ALL 55 GRID POINTS, IN SAMPLE ON THE WHOLE CORPUS\n")
    say("  D = mean[ OOS(rule) - OOS(argmax) ] in Sharpe units;  abstain iff qlo < F(margin) <= qhi.")
    grids = []
    for cname, S in CORPORA.items():
        for norm in NORMS:
            g = band_grid(S, norm, scope=cname)
            grids.append(g)
    BG = pd.concat(grids, ignore_index=True)
    BG.to_csv(OUT / f"{STEM}.bandgrid.csv", index=False)

    for cname in CORPORA:
        g = BG[(BG.scope == cname) & (BG.norm == "raw")]
        piv = g.pivot_table(index="qlo", columns="qhi", values="mean")
        say(f"\n  {cname}  norm=raw  D(qlo, qhi), instance-pooled:")
        say(piv.to_string(float_format=lambda x: f"{x:+.4f}"))
        pf = g.pivot_table(index="qlo", columns="qhi", values="fc_mean")
        say(f"  {cname}  norm=raw  D(qlo, qhi), FILE-CLUSTERED:")
        say(pf.to_string(float_format=lambda x: f"{x:+.4f}"))

    say("\n  Family bests IN SAMPLE (norm=raw), the number the queue's question turns on:")
    for cname in CORPORA:
        g = BG[(BG.scope == cname) & (BG.norm == "raw")]
        for fam in ("THRESHOLD", "BAND", "ALWAYS-ABSTAIN"):
            gg = g[g.family == fam]
            if not len(gg):
                continue
            b = gg.loc[gg["mean"].idxmax()]
            say(f"    {cname:15s} {fam:15s} best ({b.qlo:.1f},{b.qhi:.1f})  D {b['mean']:+.4f} "
                f"(t {b['t']:+.2f})  file-clustered {b['fc_mean']:+.4f} (t {b['fc_t']:+.2f})  "
                f"abstains {b['abstain']:.1%}")

    say("\n  SENSITIVITY (labelled, not a third tuned dial): the same family bests on z and rng")
    for cname in CORPORA:
        for norm in ("z", "rng"):
            g = BG[(BG.scope == cname) & (BG.norm == norm)]
            for fam in ("THRESHOLD", "BAND"):
                gg = g[g.family == fam]
                b = gg.loc[gg["mean"].idxmax()]
                say(f"    {cname:15s} {norm:3s} {fam:9s} ({b.qlo:.1f},{b.qhi:.1f})  "
                    f"D {b['mean']:+.4f}  fc {b['fc_mean']:+.4f}  abstains {b['abstain']:.1%}")
    flush()

    # ---------------------------------------------------------------- PART C
    say("\n\n## PART C — RULE 8 ON THE CORPUS: does the BAND transfer where the THRESHOLD does not?\n")
    wf_rows = []
    for cname, S in CORPORA.items():
        dates = sorted(S.date.unique())
        cut = dates[len(dates) // 2]
        A, B = S[S.date < cut], S[S.date >= cut]
        say(f"  {cname}: DATE split at {cut} — IS {A.file.nunique()} files / {len(A)} cells, "
            f"OOS {B.file.nunique()} files / {len(B)} cells")
        for norm in NORMS:
            for fam in ("THRESHOLD", "BAND"):
                lo, hi = fit_band(A, norm, fam)
                ins = apply_band(A, norm, lo, hi)
                oos = apply_band(B, norm, lo, hi)
                wf_rows.append(dict(corpus=cname, split="DATE", seed=-1, norm=norm, family=fam,
                                    qlo=lo, qhi=hi, IS_D=ins["mean"], OOS_D=oos["mean"],
                                    OOS_t=oos["t"], OOS_fc=oos["fc_mean"],
                                    OOS_abstain=oos["abstain"], n=oos["n"]))
                if norm == "raw":
                    say(f"    {fam:10s} fitted ({lo:.1f},{hi:.1f})  IS D {ins['mean']:+.4f}  "
                        f"-> OOS D {oos['mean']:+.4f} (t {oos['t']:+.2f}, file-clustered "
                        f"{oos['fc_mean']:+.4f}), abstains {oos['abstain']:.1%}")
            aa = apply_band(B, norm, 0.0, 1.0)
            wf_rows.append(dict(corpus=cname, split="DATE", seed=-1, norm=norm,
                                family="ALWAYS-ABSTAIN", qlo=0.0, qhi=1.0, IS_D=np.nan,
                                OOS_D=aa["mean"], OOS_t=aa["t"], OOS_fc=aa["fc_mean"],
                                OOS_abstain=aa["abstain"], n=aa["n"]))
            if norm == "raw":
                say(f"    {'ALWAYS-ABSTAIN':10s} (0.0,1.0)              "
                    f"-> OOS D {aa['mean']:+.4f} (t {aa['t']:+.2f}, file-clustered "
                    f"{aa['fc_mean']:+.4f})")
                say(f"    {'RAW ARGMAX':10s} (do nothing)              -> OOS D +0.0000 by definition")

        say(f"  {cname}: {SEEDS} seeded random FILE splits (half the files fit, half read once)")
        files = np.array(sorted(S.file.unique()))
        for sd in range(SEEDS):
            rng = np.random.default_rng(20260908 + sd)
            pick = set(rng.choice(files, size=len(files) // 2, replace=False))
            A = S[S.file.isin(pick)]
            B = S[~S.file.isin(pick)]
            for norm in NORMS:
                for fam in ("THRESHOLD", "BAND"):
                    lo, hi = fit_band(A, norm, fam)
                    oos = apply_band(B, norm, lo, hi)
                    wf_rows.append(dict(corpus=cname, split="FILE", seed=sd, norm=norm,
                                        family=fam, qlo=lo, qhi=hi, IS_D=np.nan,
                                        OOS_D=oos["mean"], OOS_t=oos["t"],
                                        OOS_fc=oos["fc_mean"], OOS_abstain=oos["abstain"],
                                        n=oos["n"]))
                aa = apply_band(B, norm, 0.0, 1.0)
                wf_rows.append(dict(corpus=cname, split="FILE", seed=sd, norm=norm,
                                    family="ALWAYS-ABSTAIN", qlo=0.0, qhi=1.0, IS_D=np.nan,
                                    OOS_D=aa["mean"], OOS_t=aa["t"], OOS_fc=aa["fc_mean"],
                                    OOS_abstain=aa["abstain"], n=aa["n"]))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    say("\n  20-seed FILE-split summary (norm=raw): OOS D of each family, and how often it beats "
        "the raw argmax (D > 0) and always-abstain")
    for cname in CORPORA:
        w = WF[(WF.corpus == cname) & (WF.split == "FILE") & (WF.norm == "raw")]
        aa = w[w.family == "ALWAYS-ABSTAIN"].set_index("seed").OOS_D
        for fam in ("THRESHOLD", "BAND", "ALWAYS-ABSTAIN"):
            f = w[w.family == fam].set_index("seed").OOS_D
            beat_aa = int((f > aa).sum()) if fam != "ALWAYS-ABSTAIN" else 0
            say(f"    {cname:15s} {fam:15s} mean OOS D {f.mean():+.4f}  median {f.median():+.4f}  "
                f"D>0 in {int((f > 0).sum())}/{len(f)}  beats always-abstain in {beat_aa}/{len(f)}")
        wb = w[w.family == "BAND"]
        say(f"    {cname:15s} BAND edges chosen: " +
            ", ".join(f"({a:.1f},{b:.1f})" for a, b in
                      sorted(set(zip(wb.qlo, wb.qhi)))[:12]))
    flush()

    # ---------------------------------------------------------------- PART D
    say("\n\n## PART D — RULE 8 ON LIVE PRICES (out of corpus)\n")
    panels = P241.load_panels()
    say("  panels: " + ", ".join(f"{k} {v.shape[1] - (1 if 'SPY' in v.columns else 0)} names, "
                                 f"{v.index[0].date()}..{v.index[-1].date()}"
                                 for k, v in panels.items()))
    fg, curves = P241.fresh_grid(panels, costs=(10.0, 25.0))
    menus = P241.submenus([a for a, _ in P241.arm_menu()])   # the parent's own call, verbatim
    LC = P241.live_cells(fg, menus, "IS_", "OOS_")          # arms <=2016, payoff 2017+
    CAL = P241.live_cells(fg, menus, "ISin_", "MID_")       # arms <=2013, payoff 2014-2016
    for d in (LC, CAL):
        d["gain"] = d.OOS_ctl - d.OOS_star
        d["is_sd"] = d.margin_raw / d.margin_z.replace(0, np.nan)
    LC.to_csv(OUT / f"{STEM}.livecells.csv", index=False)

    say(f"  live cells: headline {len(LC)} / calibration {len(CAL)} "
        f"(3 panels x 2 costs x 200 seeded sub-menus of 5-15 arms, each containing the control)")
    for pname in sorted(LC.panel.unique()):
        g = LC[LC.panel == pname]
        mv = g[~g.star_is_ctl.astype(bool)]
        say(f"    {pname:9s}: argmax IS the control in {int(g.star_is_ctl.sum())}/{len(g)} cells "
            f"-> only {len(mv)} MOVED cells; abstention is a strict NO-OP on the rest")

    say("\n  Live tercile shape on MOVED cells (the parent's live reading, re-run):")
    live_rows = []
    for pname in sorted(LC.panel.unique()):
        for c in sorted(LC.cost.unique()):
            g = LC[(LC.panel == pname) & (LC.cost == c) & ~LC.star_is_ctl.astype(bool)]
            g = g.copy()
            g["file"] = f"{pname}|{c:g}"
            tt = tercile_table(g, NORMCOL["raw"], scope=f"LIVE/{pname}/{c:g}")
            if not tt:
                say(f"    {pname:9s} {c:g}bps  n {len(g):4d}  (no usable terciles)")
                continue
            live_rows.append(dict(corpus="LIVE", stratum="PANEL", level=f"{pname}|{c:g}",
                                  norm="raw", **tt))
            say(f"    {pname:9s} {c:g}bps  n {tt['n']:4d}  narrow {tt['narrow']:+.4f}  "
                f"mid {tt['mid']:+.4f}  wide {tt['wide']:+.4f}  rho {tt['spearman']:+.4f}  "
                f"-> {tt['shape']}")
    if live_rows:
        pd.concat([ST, pd.DataFrame(live_rows)], ignore_index=True).to_csv(
            OUT / f"{STEM}.strata.csv", index=False)

    # edges: (i) fitted on the live CALIBRATION frame, (ii) imported from the RECORD corpus
    CALm = CAL[~CAL.star_is_ctl.astype(bool)].copy()
    CALm["file"] = CALm.panel + "|" + CALm.cost.astype(str)
    edges = {}
    for fam in ("THRESHOLD", "BAND"):
        edges[f"CAL/{fam}"] = fit_band(CALm, "raw", fam) if len(CALm) >= 30 else (0.0, 0.0)
    rec = WF[(WF.corpus == "FROZEN(parent)") & (WF.split == "DATE") & (WF.norm == "raw")]
    for fam in ("THRESHOLD", "BAND"):
        r = rec[rec.family == fam]
        edges[f"RECORD/{fam}"] = (float(r.iloc[0].qlo), float(r.iloc[0].qhi)) if len(r) else (0.0, 0.0)
    edges["ALWAYS-ABSTAIN"] = (0.0, 1.0)
    say("\n  Edges applied to the headline live frame, all chosen WITHOUT touching 2017+:")
    for k, (lo, hi) in edges.items():
        say(f"    {k:20s} ({lo:.1f}, {hi:.1f})")

    say("\n  Live grid: D = mean[OOS Sharpe(rule) - OOS Sharpe(argmax)] over each panel's cells")
    lg_rows = []
    for pname in sorted(LC.panel.unique()):
        for c in sorted(LC.cost.unique()):
            g = LC[(LC.panel == pname) & (LC.cost == c)].copy()
            g["file"] = f"{pname}|{c:g}"
            for k, (lo, hi) in edges.items():
                r = band_delta(g[g[NORMCOL["raw"]].notna()], NORMCOL["raw"], lo, hi)
                lg_rows.append(dict(panel=pname, cost=c, rule=k, qlo=lo, qhi=hi, **r))
    LG = pd.DataFrame(lg_rows)
    LG.to_csv(OUT / f"{STEM}.livegrid.csv", index=False)
    say(LG.pivot_table(index=["panel", "cost"], columns="rule", values="mean")
        .to_string(float_format=lambda x: f"{x:+.4f}"))

    # ---------------------------------------------------------------- books + KEEP paths
    say("\n  BOOKS — equal weight over each (panel, cost) cell's chosen arm, one decision per cell.")
    kp_rows = []
    for pname in sorted(LC.panel.unique()):
        for c in sorted(LC.cost.unique()):
            sub = LC[(LC.panel == pname) & (LC.cost == c)]
            q = sub[NORMCOL["raw"]].rank(pct=True, method="average")
            books = {}
            streams_arg = [curves[(pname, c, r.arm_star)] for _, r in sub.iterrows()]
            books["ARGMAX"] = pd.concat(streams_arg, axis=1).mean(axis=1)
            books["INCUMBENT"] = curves[(pname, c, "control")]
            for k, (lo, hi) in edges.items():
                ab = ((q > lo) & (q <= hi)) if lo > 0 else (q <= hi)
                streams = [curves[(pname, c, "control" if ab.iloc[i] else r.arm_star)]
                           for i, (_, r) in enumerate(sub.iterrows())]
                books[k] = pd.concat(streams, axis=1).mean(axis=1)
            spy = curves[(pname, c, "__SPY__")]
            v2 = curves[(pname, c, "__V2__")]
            for label, r in books.items():
                row = dict(panel=pname, cost=c, book=label)
                row.update(P241.win_metrics(r))
                row.update(P241.win_metrics(r, lo=OOS_START, prefix="OOS_"))
                row.update(P241.keep_paths(r, v2, spy))
                kp_rows.append(row)
            for label, r in (("RULES v2 (live)", v2), ("SPY", spy)):
                row = dict(panel=pname, cost=c, book=label)
                row.update(P241.win_metrics(r))
                row.update(P241.win_metrics(r, lo=OOS_START, prefix="OOS_"))
                kp_rows.append(row)
    KP = pd.DataFrame(kp_rows)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    cols = ["panel", "cost", "book", "CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "pass4a", "pass4b", "pass4a_oos", "pass4b_oos"]
    say(KP[cols].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    n4a = int(KP.pass4a.fillna(False).sum())
    n4b = int(KP.pass4b.fillna(False).sum())
    nb = int(KP.book.isin(list(edges) + ["ARGMAX", "INCUMBENT"]).sum())
    say(f"\n  KEEP PATHS over the {nb} rule books: 4a {n4a}/{nb}, 4b {n4b}/{nb}, "
        f"4b-OOS {int(KP.pass4b_oos.fillna(False).sum())}/{nb}, "
        f"BOTH {int((KP.pass4a.fillna(False) & KP.pass4b.fillna(False)).sum())}/{nb}")

    flush()
    say(f"\nwrote {STEM}.{{strata,bandgrid,walkforward,livecells,livegrid,keeppaths,console}}")
    flush()


if __name__ == "__main__":
    main()
