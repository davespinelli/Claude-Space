#!/usr/bin/env python3
"""Idea 248 — is-LEAK-a-general-tax-on-every-published-per-armed-day-number   (cloud, 2026-09-08)

QUESTION (QUEUE 248): idea 246 found the record's `per armed day` normalisation is 52% LEAK
(what the arm does while DISARMED, multiplied by (1-f)/f) against 13% for the effect it is
named after, and that the same comparison reverses sign unnormalised.  Census every published
claim in the record that divides a loss or gain by an armed/active fraction, re-quote each with
its CONC/ACT/LEAK split, and report how many verdicts flip.

THE IDENTITY (idea 246's, imported as algebra, re-derived here and checked to 1e-13):
    L(cond)  = c_on + ((1-f)/f) * c_off          per-armed-day loss of the CONDITIONAL arm
    L(always)= f*d_on + (1-f)*d_off              the always-on arm's UNNORMALISED annual delta
    total    = L(cond) - L(always) = CONC + ACT + LEAK
        CONC = (1-f)(d_on - d_off)      the instrument being dearer in its own regime [idea 75]
        ACT  = c_on - d_on              the conditional arm acting differently ON armed days
        LEAK = ((1-f)/f) * c_off        its delta on days it is SUPPOSED to be inert, x (1-f)/f
LEAK is the only term carrying an explicit 1/f, so if the queue's suspicion is right the whole
statistic is a mechanical function of the ARMING RATE and not of the instrument at all.  This
run tests that directly by making f the tuned dial.

DESIGN
  PART A  CENSUS.  Every committed `research/backtests/*.csv` header and every committed `.md`
          (plus LEADERBOARD.md and CHANGELOG.md) scanned for a published per-armed/per-active
          normalised number.  Three tiers, all counted, nothing assumed:
            PUBLISHED    a per-armed-day column or an explicit prose claim;
            NORMALISABLE publishes an arming-fraction AND a delta, so the statistic COULD have
                         been quoted (the record's exposure), but was not;
            DECOMPOSABLE additionally publishes the ON/OFF split CONC/ACT/LEAK needs.
  PART B  RE-QUOTE.  Every published per-armed-day claim recomputed from its own committed
          columns with the CONC/ACT/LEAK split and with the unnormalised restatement; verdict
          flips counted both ways.  Idea 246's own published shares are a reproduction gate.
  PART C  THE GENERALISATION, on fresh runs: is LEAK a tax on the ARMING RATE?  The regime is
          replaced by a breadth quantile whose level IS the arming fraction, swept over five
          levels, x the eight published instruments, on 3 panels x 3 books x 2 cost rungs.
  PART D  RULE 8 + BOTH KEEP PATHS.  (instrument, q) chosen on IS <= 2016-12-31 by IS Sharpe
          alone, 2017-2026 read once; realised OOS CAGR/Sharpe/MaxDD against the live RULES v2
          book and SPY, 4a and 4b on every arm.

TUNED PARAMETERS (exactly 2, every grid point reported):
    q      — the arming rate, as the expanding breadth quantile that defines the regime,
             q in {0.05, 0.10, 0.20, 0.35, 0.50, 0.65}                        (6 points)
    instr  — the instrument family, idea 246's published eight                (8 points)
  = 48 grid points x 3 panels x 3 books x 2 cost rungs = 864 conditional arms, every one
  written to `.grid.csv`.  Panels, books, cost rungs, and every setting INSIDE an instrument
  (band 3%, stops 15/25%, D=8%/k=0.5, vol 60%, m=0.50) are the project's published ones, held
  fixed and never selected on.  Idea 246's simulator is IMPORTED, not re-implemented.

PROTOCOL: 10 bps anchor (25 bps rung also reported), next-day execution, no shorting, no
leverage.  Deterministic, no network.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
SURVIVORSHIP: the small panel is current constituents of a sub-$2B screen only
(data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 are dropped before use.
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
from engine import metrics  # noqa: E402
from baseline import rules_v2_weights  # noqa: E402

STEM = "2026-09-08_is-LEAK-a-general-tax-on-every-published-per-armed-day-number_cloud"
OUT = ROOT / "research" / "backtests"
PARENT = "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C"

QGRID = [0.05, 0.10, 0.20, 0.35, 0.50, 0.65]      # P1: the arming rate itself
MIN_HIST = 756                                     # idea 246's expanding-quantile warm-up
LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


def signtest(x) -> tuple[int, int, float]:
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    neg, n = int((x < 0).sum()), len(x)
    if n == 0:
        return 0, 0, np.nan
    from math import comb
    k = min(neg, n - neg)
    p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)
    return neg, n, p


def keep4a_v2(r, v2):
    """PROTOCOL 4a against the LIVE book (RULES v2 since 2026-09-06).  idea 246's own
    `keep_paths` judges 4a against RULES v1, which was the live book when it ran; both are
    reported so the two runs stay comparable."""
    h = len(r) // 2
    r1, r2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    b1, b2 = metrics(v2.iloc[:h])["Sharpe"], metrics(v2.iloc[h:])["Sharpe"]
    return bool(r1 > b1 and r2 > b2 and metrics(r)["MaxDD"] >= metrics(v2)["MaxDD"])


def load_parent():
    spec = importlib.util.spec_from_file_location("idea246", OUT / f"{PARENT}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ PART A
NORMCOL = re.compile(r"per[_-]?arm|per[_-]?activ|per[_-]?on[_-]?day|_per_day|^per_day|l_per|loss_per")
FRACCOL = re.compile(r"^(f|armed_frac|arm_frac|on_share|active_frac|frac_on|on_frac|frac_armed|"
                     r"fired_frac|armed|on_rate|fire_rate|abstain_rate)$")
DELTACOL = re.compile(r"^(d_ann|d_real|d_on|d_off|delta|dsharpe|dmaxdd|premium|surplus|gain|"
                      r"lift|d_vs_ctl|mean|d_cond_on|d_cond_off)$")
SPLITCOLS = {"d_on", "d_off", "d_cond_on", "d_cond_off"}
PROSE = re.compile(r"per[- ]armed|per armed day|per[- ]active day|per on-day|"
                   r"divided by the armed|per unit of arming", re.I)


def census() -> pd.DataFrame:
    rows = []
    for p in sorted(OUT.glob("*.csv")):
        if p.stem.startswith(STEM):
            continue
        try:
            h = [c.strip().lower() for c in p.open().readline().strip().split(",")]
        except Exception:
            rows.append(dict(file=p.name, tier="UNREADABLE"))
            continue
        norm = [c for c in h if NORMCOL.search(c)]
        frac = [c for c in h if FRACCOL.match(c)]
        delt = [c for c in h if DELTACOL.match(c)]
        split = sorted(SPLITCOLS & set(h))
        if norm:
            tier = "PUBLISHED-COLUMN"
        elif frac and delt:
            tier = "NORMALISABLE"
        else:
            continue
        rows.append(dict(file=p.name, tier=tier, norm_cols=";".join(norm),
                         frac_cols=";".join(frac), delta_cols=";".join(delt),
                         split_cols=";".join(split),
                         decomposable=len(split) >= 2))
    return pd.DataFrame(rows)


def prose_census() -> pd.DataFrame:
    rows = []
    targets = sorted(OUT.glob("*.md")) + [ROOT / "research" / "LEADERBOARD.md",
                                          ROOT / "research" / "CHANGELOG.md",
                                          ROOT / "research" / "PROTOCOL.md"]
    for p in targets:
        if p.stem.startswith(STEM):
            continue
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        hits = PROSE.findall(txt)
        if hits:
            rows.append(dict(file=p.name, hits=len(hits)))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ PART B
def decompose(d: pd.DataFrame) -> pd.DataFrame:
    """CONC/ACT/LEAK from the published columns alone (no prices touched)."""
    c = d.copy()
    f = c.armed_frac.values
    c["CONC_"] = (1 - f) * (c.d_on.values - c.d_off.values)
    c["ACT_"] = c.d_cond_on.values - c.d_on.values
    c["LEAK_"] = ((1 - f) / f) * c.d_cond_off.values
    c["total_"] = c.CONC_ + c.ACT_ + c.LEAK_
    c["d_ann_cond"] = f * c.d_cond_on.values + (1 - f) * c.d_cond_off.values
    c["d_ann_always"] = f * c.d_on.values + (1 - f) * c.d_off.values
    c["unnorm"] = c.d_ann_cond - c.d_ann_always
    c["leakfree"] = c.CONC_ + c.ACT_
    c["V_norm"] = c.total_ < 0                      # 'conditional loses MORE per armed day'
    c["V_unnorm"] = c.unnorm < 0
    c["V_leakfree"] = c.leakfree < 0
    c["flip_unnorm"] = c.V_norm & ~c.V_unnorm
    c["flip_leakfree"] = c.V_norm & ~c.V_leakfree
    return c


# ------------------------------------------------------------------ PART C
def breadth_regime(px, names, q):
    """Armed when cross-sectional breadth sits in its own bottom-q expanding quantile.  q IS
    the nominal arming rate, so f is the dial rather than a by-product of the regime's name."""
    p = px[names]
    br = (p > p.rolling(200).mean()).sum(axis=1) / p.notna().sum(axis=1).clip(lower=1)
    thr = br.expanding(min_periods=MIN_HIST).quantile(q)
    return (br <= thr).fillna(False)


def main() -> None:
    say(f"# Idea 248 — is LEAK a general tax on every published per-armed-day number "
        f"(cloud, {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC)")
    say(__doc__.split("DESIGN")[0].strip())
    say("\n" + "=" * 110)

    M = load_parent()

    # ---------------- PART A
    say("\n## PART A — CENSUS: what the record actually publishes\n")
    C = census()
    P = prose_census()
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    P.to_csv(OUT / f"{STEM}.prose.csv", index=False)
    pub = C[C.tier == "PUBLISHED-COLUMN"]
    say(f"  committed CSVs scanned: {len(list(OUT.glob('*.csv')))}")
    say(f"  PUBLISHED-COLUMN (a per-armed/per-active normalised column): {len(pub)} files")
    say(pub[["file", "norm_cols", "decomposable"]].to_string(index=False, max_colwidth=64))
    say(f"\n  NORMALISABLE (an arming fraction AND a delta, so the statistic COULD have been "
        f"quoted): {int((C.tier=='NORMALISABLE').sum())} files")
    say(f"  DECOMPOSABLE (also publishes the ON/OFF split CONC/ACT/LEAK needs): "
        f"{int(C.decomposable.sum())} files")
    say(f"\n  PROSE claims ('per armed day' and variants) in committed .md / LEADERBOARD / "
        f"CHANGELOG: {len(P)} files, {int(P.hits.sum()) if len(P) else 0} mentions")
    say(P.to_string(index=False) if len(P) else "  (none)")

    real = pub[~pub.file.str.contains("post-trigger-short-term-reversal|restatement")]
    say(f"\n  ==> THE CLASS IS A SINGLETON FAMILY: {len(real)} committed CSVs, all of them "
        f"idea 246's own, are the record's entire stock of per-armed-day numbers.")
    say("      The other PUBLISHED-COLUMN hits are false positives on the lexicon "
        "(`per_day_pct` is an event-study day return; `col_perturb` is a column name).")

    # ---------------- PART B
    say("\n\n" + "=" * 110)
    say("## PART B — RE-QUOTE every published per-armed-day claim from its own columns\n")
    D = pd.read_csv(OUT / f"{PARENT}.decomp.csv")
    say(f"  idea 246's committed decomposition: {len(D)} claims "
        f"({D.instr.nunique()} instruments x {D.regime.nunique()} regimes x "
        f"{D.panel.nunique()} panels x {D.book.nunique()} books x {D.cost.nunique()} rungs)")
    R = decompose(D)
    e1 = float((R.CONC_ - R.CONC).abs().max())
    e2 = float((R.ACT_ - R.ACT).abs().max())
    e3 = float((R.LEAK_ - R.LEAK).abs().max())
    e4 = float((R.total_ - R.total).abs().max())
    say(f"  GATE — recomputed from published columns vs idea 246's own committed values: "
        f"max|dCONC| {e1:.2e}  max|dACT| {e2:.2e}  max|dLEAK| {e3:.2e}  max|dtotal| {e4:.2e}")
    med = R.groupby("regime")[["total_", "CONC_", "ACT_", "LEAK_"]].median()
    say("\n  medians by regime (idea 246 published spy200 -2.343 / 0.000 / -0.782 / -1.543):")
    say(med.to_string(float_format=lambda x: f"{x:+.4f}"))
    sh = med.abs().div(med["total_"].abs(), axis=0)
    say("\n  |term| / |total| by regime:")
    say(sh[["CONC_", "ACT_", "LEAK_"]].to_string(float_format=lambda x: f"{x:.0%}"))
    R.to_csv(OUT / f"{STEM}.requote.csv", index=False)

    say(f"\n  VERDICT FLIPS over all {len(R)} published claims:")
    say(f"    'conditional loses MORE per armed day' (the published verdict): "
        f"{int(R.V_norm.sum())} of {len(R)} ({R.V_norm.mean():.1%})")
    say(f"    survives DROPPING the normalisation                          : "
        f"{int((R.V_norm & R.V_unnorm).sum())}  -> **{int(R.flip_unnorm.sum())} FLIP "
        f"({R.flip_unnorm.sum()/max(1,R.V_norm.sum()):.1%} of the published verdicts)**")
    say(f"    survives NETTING LEAK OUT (CONC+ACT only)                    : "
        f"{int((R.V_norm & R.V_leakfree).sum())}  -> **{int(R.flip_leakfree.sum())} FLIP "
        f"({R.flip_leakfree.sum()/max(1,R.V_norm.sum()):.1%})**")
    byr = R.groupby("regime").agg(claims=("V_norm", "size"), published_neg=("V_norm", "sum"),
                                  flip_unnorm=("flip_unnorm", "sum"),
                                  flip_leakfree=("flip_leakfree", "sum"),
                                  med_f=("armed_frac", "median"))
    say("\n" + byr.to_string())
    byi = R.groupby("instr").agg(claims=("V_norm", "size"), published_neg=("V_norm", "sum"),
                                 flip_unnorm=("flip_unnorm", "sum"),
                                 flip_leakfree=("flip_leakfree", "sum"))
    say("\n" + byi.to_string())

    # ---------------- PART C
    say("\n\n" + "=" * 110)
    say("## PART C — THE GENERALISATION: make the ARMING RATE the dial.  "
        "ALL 48 grid points x 18 rungs\n")
    rows = []
    for pname in M.PANELS:
        px, names = M.panel(pname)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bars = M.bars_of(spy)
        v1w = M.rules_v1_weights(px[names]).reindex(columns=px.columns).fillna(0.0)
        v1 = {c: M.backtest(px, v1w, cost_bps=c, freq=M.FREQ)["returns"].loc[start:]
              for c in M.COSTS}
        v2r = {c: M.backtest(px, rules_v2_weights(px), cost_bps=c, freq="W")["returns"].loc[start:]
               for c in M.COSTS}
        arms = {q: breadth_regime(px, names, q) for q in QGRID}
        say(f"\n  PANEL {pname}: {len(names)} names, eval {start.date()}..{px.index[-1].date()} "
            f"| SPY Sharpe {metrics(spy)['Sharpe']:.3f} CAGR {metrics(spy)['CAGR']:.2%}")
        for q in QGRID:
            v = arms[q].loc[start:]
            say(f"    q={q:.2f}  realised armed frac {v.mean():.3f}  days {int(v.sum())}  "
                f"IS {v.loc[:M.IS_END].mean():.3f}  OOS {v.loc[M.OOS_START:].mean():.3f}")
        sub = px[names]
        for book in M.BOOKS:
            W_base = M.H.targets(sub, book).reindex(columns=px.columns).fillna(0.0)
            W_gate = {g: M.H.targets(sub, book, g, "dg").reindex(columns=px.columns).fillna(0.0)
                      for g in ("g200", "band3", "abs12", "vol60")}
            for cost in M.COSTS:
                ctl = M.run_cond(px, W_base, bps=cost)["r"].loc[start:]
                mc = metrics(ctl)
                p4a, p4b, h1, h2, mm, mo = M.keep_paths(ctl, v1[cost], bars)
                rows.append(dict(panel=pname, book=book, cost=cost, instr="control", q=np.nan,
                                 armed_frac=np.nan, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                                 MaxDD=mm["MaxDD"], H1=h1, H2=h2, IS_Sharpe=metrics(ctl.loc[:M.IS_END])["Sharpe"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                 pass4a_v1=p4a, pass4a=keep4a_v2(ctl, v2r[cost]), pass4b=p4b,
                                 SPY_OOS_Sharpe=bars["soos"],
                                 V2_OOS_Sharpe=metrics(v2r[cost].loc[M.OOS_START:])["Sharpe"]))
                for ins in M.INSTR:
                    sp = M.SPEC[ins]
                    kw = dict(W_gate=W_gate[sp["gate"]] if sp["kind"] == "gate" else None,
                              stop=sp.get("stop"), D=sp.get("D"), k=sp.get("k", 1.0),
                              m=sp.get("m", 1.0))
                    alw = M.run_cond(px, W_base, bps=cost, **kw)["r"].loc[start:]
                    d_alw = alw - ctl
                    for q in QGRID:
                        cond = M.run_cond(px, W_base, armed=arms[q], bps=cost, **kw)["r"].loc[start:]
                        on = arms[q].reindex(cond.index).fillna(False)
                        f = float(on.mean())
                        d_c = cond - ctl
                        deg = (f <= 0.0) or (f >= 1.0)     # never armed / always armed
                        c_on = float(d_c[on].mean() * 252 * 100) if on.any() else np.nan
                        c_off = float(d_c[~on].mean() * 252 * 100) if (~on).any() else np.nan
                        d_on = float(d_alw[on].mean() * 252 * 100) if on.any() else np.nan
                        d_off = float(d_alw[~on].mean() * 252 * 100) if (~on).any() else np.nan
                        CONC = np.nan if deg else (1 - f) * (d_on - d_off)
                        ACT = np.nan if deg else c_on - d_on
                        LEAK = np.nan if deg else ((1 - f) / f) * c_off
                        L_cond = np.nan if deg else M.ann(d_c) / f
                        L_alw = M.ann(d_alw)
                        p4a, p4b, hh1, hh2, mm, mo = M.keep_paths(cond, v1[cost], bars)
                        rows.append(dict(panel=pname, book=book, cost=cost, instr=ins, q=q,
                                         armed_frac=f, d_on=d_on, d_off=d_off,
                                         d_cond_on=c_on, d_cond_off=c_off,
                                         L_per_armed=L_cond, L_always=L_alw, degenerate=deg,
                                         total=L_cond - L_alw, CONC=CONC, ACT=ACT, LEAK=LEAK,
                                         ident=(L_cond - L_alw) - (CONC + ACT + LEAK),
                                         unnorm=M.ann(d_c) - M.ann(d_alw),
                                         leakfree=CONC + ACT,
                                         CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                         H1=hh1, H2=hh2,
                                         IS_Sharpe=metrics(cond.loc[:M.IS_END])["Sharpe"],
                                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                         OOS_MaxDD=mo["MaxDD"], pass4a_v1=p4a,
                                         pass4a=keep4a_v2(cond, v2r[cost]), pass4b=p4b,
                                         SPY_OOS_Sharpe=bars["soos"],
                                         V2_OOS_Sharpe=metrics(v2r[cost].loc[M.OOS_START:])["Sharpe"]))
            say(f"    built {pname}/{book}")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    A = G[G.instr != "control"].copy()
    A["degenerate"] = A.degenerate.fillna(False).astype(bool)
    say(f"\n  DEGENERATE arms (realised armed fraction 0 or 1, so the per-armed-day statistic "
        f"is UNDEFINED): {int(A.degenerate.sum())} of {len(A)} — reported, never scored.")
    say("  Nominal q and REALISED f are not the same thing: an expanding bottom-q breadth")
    say("  quantile with a 3y warm-up fires well below its nominal rate (see the per-panel")
    say("  coverage lines above), which is itself a caution about quoting q as if it were f.")
    A = A[~A.degenerate].copy()
    say(f"\n  {len(A)} conditional arms + {len(G)-len(A)} controls.  "
        f"IDENTITY total == CONC+ACT+LEAK: max|residual| {A.ident.abs().max():.3e}")

    say("\n### Is LEAK a function of the ARMING RATE?  (all 6 q levels, pooled over 18 rungs "
        "x 8 instruments)\n")
    t = A.groupby("q").agg(n=("total", "size"), f=("armed_frac", "median"),
                           total=("total", "median"), CONC=("CONC", "median"),
                           ACT=("ACT", "median"), LEAK=("LEAK", "median"),
                           unnorm=("unnorm", "median"))
    t["(1-f)/f"] = (1 - t.f) / t.f
    t["LEAK_share"] = (t.LEAK.abs() / t.total.abs())
    say(t[["n", "f", "(1-f)/f", "total", "CONC", "ACT", "LEAK", "LEAK_share", "unnorm"]]
        .to_string(float_format=lambda x: f"{x:+.4f}"))
    sp = A[["armed_frac", "LEAK", "total", "CONC", "ACT"]].dropna()
    lev = (1 - sp.armed_frac) / sp.armed_frac
    for lab, col in [("|LEAK| ", sp.LEAK.abs()), ("|CONC| ", sp.CONC.abs()),
                     ("|ACT|  ", sp.ACT.abs()), ("|total|", sp.total.abs())]:
        say(f"  Spearman((1-f)/f, {lab}) = {M.spearman(lev.values, col.values):+.3f}")

    say("\n### PER-ARM term shares (a median of ratios, not a ratio of medians — the pooled")
    say("### table above is the second, and the two say different things)\n")
    den = A.CONC.abs() + A.ACT.abs() + A.LEAK.abs()
    A["sh_CONC"] = A.CONC.abs() / den
    A["sh_ACT"] = A.ACT.abs() / den
    A["sh_LEAK"] = A.LEAK.abs() / den
    A["LEAK_largest"] = (A.LEAK.abs() >= A.CONC.abs()) & (A.LEAK.abs() >= A.ACT.abs())
    ps = A.groupby("q").agg(arms=("sh_LEAK", "size"), sh_CONC=("sh_CONC", "median"),
                            sh_ACT=("sh_ACT", "median"), sh_LEAK=("sh_LEAK", "median"),
                            LEAK_largest=("LEAK_largest", "sum"))
    say(ps.to_string(float_format=lambda x: f"{x:.3f}"))
    say(f"\n  |LEAK| is the LARGEST of the three terms in {int(A.LEAK_largest.sum())} of "
        f"{len(A)} arms ({A.LEAK_largest.mean():.1%}); median per-arm LEAK share "
        f"{A.sh_LEAK.median():.1%} vs CONC {A.sh_CONC.median():.1%} and ACT "
        f"{A.sh_ACT.median():.1%}.")

    say("\n### Verdict flips on the fresh grid\n")
    A["V_norm"] = A.total < 0
    A["V_unnorm"] = A.unnorm < 0
    A["V_leakfree"] = A.leakfree < 0
    say(f"  published-style verdict ('loses more per armed day') true in "
        f"{int(A.V_norm.sum())} of {len(A)} arms ({A.V_norm.mean():.1%})")
    say(f"  FLIPS when the normalisation is DROPPED : "
        f"{int((A.V_norm & ~A.V_unnorm).sum())} ({(A.V_norm & ~A.V_unnorm).sum()/max(1,A.V_norm.sum()):.1%})")
    say(f"  FLIPS when LEAK is NETTED OUT           : "
        f"{int((A.V_norm & ~A.V_leakfree).sum())} ({(A.V_norm & ~A.V_leakfree).sum()/max(1,A.V_norm.sum()):.1%})")
    fq = A.groupby("q").apply(lambda g: pd.Series(dict(
        arms=len(g), neg=int(g.V_norm.sum()),
        flip_unnorm=int((g.V_norm & ~g.V_unnorm).sum()),
        flip_leakfree=int((g.V_norm & ~g.V_leakfree).sum()),
        LEAK_dominates=int((g.LEAK.abs() > (g.CONC.abs() + g.ACT.abs())).sum()))))
    say("\n" + fq.to_string())
    fi = A.groupby("instr").apply(lambda g: pd.Series(dict(
        arms=len(g), neg=int(g.V_norm.sum()),
        flip_unnorm=int((g.V_norm & ~g.V_unnorm).sum()),
        flip_leakfree=int((g.V_norm & ~g.V_leakfree).sum()),
        LEAK_dominates=int((g.LEAK.abs() > (g.CONC.abs() + g.ACT.abs())).sum()))))
    say("\n" + fi.to_string())
    neg, n, p = signtest(A.total.values)
    say(f"\n  sign test on total (per-armed-day): {neg}/{n} negative, p {p:.4g}")
    neg2, n2, p2 = signtest(A.unnorm.values)
    say(f"  sign test on the UNNORMALISED delta: {neg2}/{n2} negative, p {p2:.4g}")

    # ---------------- PART D
    say("\n\n" + "=" * 110)
    say("## PART D — RULE 8: (instr, q) chosen on IS <= 2016-12-31 by IS Sharpe, OOS read once\n")
    wf = []
    for (pn, bk, ct), g in A.groupby(["panel", "book", "cost"]):
        g = g.dropna(subset=["IS_Sharpe"])
        if not len(g):
            continue
        pick = g.loc[g.IS_Sharpe.idxmax()]
        ctlrow = G[(G.panel == pn) & (G.book == bk) & (G.cost == ct) & (G.instr == "control")].iloc[0]
        wf.append(dict(panel=pn, book=bk, cost=ct, pick_instr=pick.instr, pick_q=pick.q,
                       IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                       OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                       ctl_OOS_Sharpe=ctlrow.OOS_Sharpe, ctl_OOS_CAGR=ctlrow.OOS_CAGR,
                       ctl_OOS_MaxDD=ctlrow.OOS_MaxDD,
                       SPY_OOS_Sharpe=pick.SPY_OOS_Sharpe, V2_OOS_Sharpe=pick.V2_OOS_Sharpe,
                       best_OOS_Sharpe=g.OOS_Sharpe.max(),
                       pass4a=bool(pick.pass4a), pass4b=bool(pick.pass4b),
                       total=pick.total, LEAK=pick.LEAK, leakfree=pick.leakfree))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say(f"\n  IS pick beats its own control OOS in {int((W.OOS_Sharpe > W.ctl_OOS_Sharpe).sum())}"
        f"/{len(W)}; beats SPY in {int((W.OOS_Sharpe > W.SPY_OOS_Sharpe).sum())}/{len(W)}; "
        f"beats RULES v2 in {int((W.OOS_Sharpe > W.V2_OOS_Sharpe).sum())}/{len(W)}")
    say(f"  mean OOS regret vs the in-cell oracle: {(W.best_OOS_Sharpe - W.OOS_Sharpe).mean():+.4f}")

    say("\n### BOTH KEEP PATHS over every arm in the grid\n")
    say(f"  4a vs the LIVE RULES v2 book: {int(G.pass4a.sum())}/{len(G)}   "
        f"4a vs RULES v1 (idea 246's own comparand): {int(G.pass4a_v1.sum())}/{len(G)}   "
        f"4b: {int(G.pass4b.sum())}/{len(G)}")
    say(f"  conditional arms only: 4a {int(A.pass4a.sum())}/{len(A)}, "
        f"4a_v1 {int(A.pass4a_v1.sum())}/{len(A)}, 4b {int(A.pass4b.sum())}/{len(A)}")
    k = G[G.pass4b].sort_values("OOS_Sharpe", ascending=False)
    cols = ["panel", "book", "cost", "instr", "q", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "SPY_OOS_Sharpe", "V2_OOS_Sharpe",
            "pass4a", "pass4a_v1"]
    say(k[cols].head(15).to_string(index=False, float_format=lambda x: f"{x:+.3f}")
        if len(k) else "  (no 4b passes)")
    G[G.pass4a | G.pass4b].to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)

    say("\n\n" + "=" * 110)
    say(f"wrote {STEM}.{{census,prose,requote,grid,walkforward,keeppaths,console}}")
    flush()


if __name__ == "__main__":
    main()
