#!/usr/bin/env python3
"""QUEUE idea 248 — is-LEAK-a-general-tax-on-every-published-per-armed-day-number
(lane B, 2026-09-08)

QUESTION (pre-registered, verbatim from QUEUE.md idea 248)
    "idea 246 found the record's `per armed day` normalisation is 52% LEAK (what the arm does
    while DISARMED, multiplied by (1-f)/f) against 13% for the effect it is named after, and
    that the same comparison reverses sign unnormalised.  Census every published claim in the
    record that divides a loss or gain by an armed/active fraction, re-quote each with its
    CONC/ACT/LEAK split, and report how many verdicts flip.  Max 2 params."

THE OBJECT.  For one cell (panel, book, cost, instrument I) and one regime R:
    control      the base book, instrument off
    always       I armed every day                       L_always     = ann(always) - ann(control)
    cond(R)      I armed only on R days, f = frac armed   L_per_armed  = [ann(cond)-ann(control)]/f
    total        = L_per_armed - L_always                 <- THE PUBLISHED STATISTIC's content
and idea 246's exact 3-way split of that total (identity verified at machine precision here):
    CONC = (1-f)*(d_on - d_off)          the instrument being dearer inside its own regime
                                         (idea 75's named mechanism — what the number CLAIMS)
    ACT  = d_cond_on - d_on              the conditional arm acting differently on ARMED days
    LEAK = ((1-f)/f) * d_cond_off        the conditional arm's delta on days it is DISARMED,
                                         amplified by (1-f)/f = 4.9-10.6x by the normaliser
LEAK is the part that should not exist: on a disarmed day the arm is supposed to BE the control.
It is non-zero because holdings, turnover and instrument state carried over from the last armed
rebalance, and the per-armed-day divisor multiplies that residue by (1-f)/f.

TWO PARTS, BOTH REQUIRED
    PART A (census, backtest-free).  Every committed research/backtests/*.csv is scanned for a
        published per-armed/per-active normalisation (D1 explicit column, D2 latent ingredients),
        and every committed *.result.md plus LEADERBOARD.md for the PROSE form of the claim (D3).
        For each hit the only question is: can its CONC/ACT/LEAK split be computed from the
        COMMITTED artefacts at all — i.e. are armed_frac, d_on, d_off, d_cond_on, d_cond_off and
        the always-on sibling all published?  Rejections are logged with a reason.  Rates over
        the unauditable remainder are reported as BOUNDS, never as points.
    PART B (live).  The decidable set is restated exactly, and — because part A's decidable set
        is one parent script's output — a fresh corpus in the record's own shape (idea 246's
        8 instruments x 3 conditional regimes x 3 panels x 3 books x 3 cost rungs, 891 runs) is
        built from scratch, decomposed, and the flip rates are counted on it.

PRE-REGISTERED HYPOTHESES (fixed before any number was read)
H1 (LEAK is a general TAX)  A tax is a systematic, same-signed drag.  CONFIRMED only if BOTH
        (a) LEAK < 0 in >= 2/3 of live cells with exact two-sided sign-test p < 0.01, AND
        (b) median |LEAK| >= median(|CONC| + |ACT|)  — it dominates the terms it is added to.
        Reported pooled, per regime, per instrument, and per cost rung.  If (a) holds and (b)
        fails, LEAK is a tax but not the dominant one; if (a) fails it is noise, not a tax.
H2 (verdict flips)   The verdict a per-armed-day number carries is sign(total): "conditioning
        makes the instrument dearer per armed day" (idea 246's H1).  A verdict FLIPS iff
        sign(total) != sign(total - LEAK).  Counted over every live cell, and separately for
        the UNNORMALISED comparison ann(cond) - ann(always), which is the same claim without
        the divisor.  Reported pooled and per regime.
H3 (magnitude, idea 261's convention)  A claim is LEAK-DOMINATED iff |total - LEAK| < 0.5|total|
        — i.e. the majority of the published magnitude is the disarmed-day residue.  Counted.
H4 (does the named mechanism survive alone)  CONC is the only term idea 75's mechanism predicts.
        How often does sign(CONC) equal sign(total), and what is CONC's share?  If CONC's sign
        agrees with the published verdict in only ~half of cells, the published statistic is not
        measuring the mechanism it is named after even where its sign happens to be right.
H5 (KEEP paths)  PROTOCOL rule 4a (vs the LIVE RULES v2 book on the same panel; v1 also
        recorded) and rule 4b (vs SPY, incl. the OOS leg) evaluated on EVERY one of the 891
        rows — conditional arms, always-on siblings and the do-nothing control — so a pass the
        always-on sibling or the control already has is never credited to the conditioning.
RULE 8 (walk-forward, required)  In each (panel, book, cost) cell the pair (INSTRUMENT, REGIME)
        is chosen on 2009-2016 IS ALONE by the PUBLISHED statistic (IS L_per_armed) and read
        ONCE, untouched, on 2017-2026.  The same pick is repeated under the LEAK-PURGED
        statistic (IS L_per_armed - IS LEAK) and under the record's usual IS-Sharpe convention.
        OOS CAGR / Sharpe / MaxDD of every selected book are reported against the live RULES v2
        baseline and against SPY, with regret vs do-nothing and vs that cell's OOS oracle.

GRID — exactly TWO tuned parameters (INSTRUMENT, REGIME).  Every grid point printed and written.
      INSTRUMENT  idea 246's 8, unchanged: g200-dg, band3-dg, abs12-dg, vol60-dg (per-name
                  gates, de-gross), stop15, stop25 (per-name trailing stops), ddctl8 (book DD
                  control), gross50 (parameter-free de-gross lever)
      REGIME      always (f=1, the unconditional sibling) + spy200, breadth20, hivol80
      panels      u56 (56), broad (136), small (439 sub-$2B after idea 130's bad-split drop;
                  SPY held as benchmark only)                        [reported, not tuned]
      books       V1u, TOP20, EWall — idea 94's three ungated base books  [reported, not tuned]
      costs       0, 10 (the PROTOCOL rung), 25 bps; every arm RE-RUN at each rung, never
                  derived from a turnover identity, because the stop and DD state machines read
                  NET equity and so their BOOKS are cost-dependent.   [reported, not tuned]
      The 0 bps rung is new: the record's per-armed corpus has only 10 and 25, so whether LEAK
      is a cost artefact or a holdings artefact has never been separable.  It is here.

ARMING MECHANICS: idea 94's harness and idea 246's `run_cond`, imported, not re-implemented.
    Arming gates the instrument's ACTION, never its STATE.  The regime is read at close t-1 and
    applied at t; breadth20 / hivol80 use EXPANDING quantiles with a 3y minimum, so no
    full-sample threshold enters anywhere.  Cost of that honesty (idea 247): the expanding
    regimes arm fewer IS than OOS days; stated in the coverage table, never corrected.

SURVIVORSHIP: all three panels are current-constituent lists (idea 54), so every absolute CAGR
    is optimistic.  H1-H4 are paired differences inside one cell on the same days and are far
    less exposed; the KEEP-path and rule-8 LEVELS are fully exposed and are upper bounds.

Deterministic, standalone.  Imports research/baseline.py, idea 94's harness and idea 246's
simulator; modifies nothing outside research/backtests/.
"""
import importlib.util
import re
import sys
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_is-LEAK-a-general-tax-on-every-published-per-armed-day-number_B"
OUT = ROOT / "research" / "backtests"

_spec = importlib.util.spec_from_file_location(
    "i246", OUT / "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
H = M.H                                                # idea 94's harness, via idea 246

FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START
PROTO_COST = 10.0
COSTS = [0.0, 10.0, 25.0]
PANELS = ["u56", "broad", "small"]
BOOKS = ["V1u", "TOP20", "EWall"]
CONDS = ["spy200", "breadth20", "hivol80"]
REGIMES = ["always"] + CONDS
INSTR = M.INSTR
SPEC = M.SPEC
STATEFUL = {"stop15", "stop25", "ddctl8"}              # instruments with carried internal state
DOM_FRAC = 0.50                                        # idea 261's majority convention
TAX_SHARE = 2.0 / 3.0                                  # H1(a) bar
TAX_P = 0.01                                           # H1(a) bar

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def signtest(x):
    """Exact two-sided binomial p for #(<0) vs #(>0), ties dropped.  Returns (p, nneg, n)."""
    x = np.asarray([v for v in np.asarray(x, float) if np.isfinite(v) and v != 0.0], float)
    n, kneg = len(x), int((x < 0).sum())
    if n == 0:
        return np.nan, 0, 0
    tail = sum(comb(n, i) for i in range(0, min(kneg, n - kneg) + 1)) / 2.0 ** n
    return float(min(1.0, 2 * tail)), kneg, n


def sgn(x):
    return 0 if (not np.isfinite(x) or x == 0.0) else (1 if x > 0 else -1)


# ==================================================================== PART A — the census
# D1: an EXPLICIT per-unit-of-armed-time column.  Conservative by design: `per_yr`, `per_day`
#     and `turn_yr` are calendar normalisations, not armed-fraction ones, and are NOT counted.
D1 = re.compile(r"per[_-]?(armed|active|on|arm|signal|event|crash|trigger|fire)", re.I)
# D2: the LATENT form — a file that publishes an armed/active FRACTION and a loss/gain column
#     has the ingredients to quote a per-armed number in its prose even with no such column.
D2_FRAC = re.compile(r"(armed|active|on)[_-]?(frac|share|rate|pct)$|^frac[_-]?(armed|on|active)"
                     r"|^(armed|active)_days$", re.I)
D2_DELTA = re.compile(r"^(d_|dCAGR|dSharpe|delta|loss|gain|surplus|ann_pp|excess)", re.I)
# ingredients the CONC/ACT/LEAK split needs, by committed column name
NEED = {"armed_frac": re.compile(r"armed[_-]?frac", re.I),
        "d_on": re.compile(r"^d_on$", re.I),
        "d_off": re.compile(r"^d_off$", re.I),
        "d_cond_on": re.compile(r"^d_cond_on$", re.I),
        "d_cond_off": re.compile(r"^d_cond_off$", re.I)}
# D3: the PROSE form, in committed result memos and in the leaderboard itself.
D3 = re.compile(r"per[- ]armed(?:[- ]day)?|per[- ]active[- ]day|per[- ]crash[- ]day|"
                r"per[- ]armed[- ]unit|L_per_armed", re.I)


def census_csv():
    """Scan every committed research/backtests/*.csv for a per-armed-day normalisation and ask
    whether the committed file itself carries the CONC/ACT/LEAK ingredients."""
    files = sorted(p for p in OUT.glob("*.csv") if not p.name.startswith(STEM))
    rows, tot_rows, tot_files = [], 0, 0
    for p in files:
        try:
            with p.open() as fh:
                hdr = fh.readline().strip()
            nrow = max(0, sum(1 for _ in p.open()) - 1)
        except Exception:
            continue
        tot_files += 1
        tot_rows += nrow
        if not hdr:
            continue
        cols = [c.strip() for c in hdr.split(",")]
        d1 = [c for c in cols if D1.search(c)]
        frac = [c for c in cols if D2_FRAC.search(c)]
        delt = [c for c in cols if D2_DELTA.search(c)]
        if not d1 and not (frac and delt):
            continue
        have = {k: any(rx.search(c) for c in cols) for k, rx in NEED.items()}
        missing = [k for k, v in have.items() if not v]
        kind = "D1-explicit-per-armed-column" if d1 else "D2-latent-ingredients-only"
        if not missing:
            dec = "DECIDABLE-all-five-ingredients"
        elif have["armed_frac"] and not missing == list(NEED):
            dec = "UNDECIDABLE-missing:" + "+".join(missing)
        else:
            dec = "UNDECIDABLE-missing:" + "+".join(missing)
        rows.append(dict(file=p.name, rows=nrow, detector=kind, stem=p.name.split(".")[0],
                         per_armed_cols="|".join(d1), frac_cols="|".join(frac),
                         delta_cols="|".join(delt[:6]), decidable=dec))
    A = pd.DataFrame(rows)
    if A.empty:
        return A, tot_files, tot_rows
    # SECOND PASS — a claim that is undecidable from its own file may still be decidable from
    # the SIBLING outputs of the same parent script (idea 246 publishes L_per_armed in .grid.csv
    # and d_on/d_off in .mechanism.csv, so neither file alone carries the split but the pair
    # does).  This is the honest denominator: an auditor has the whole commit, not one file.
    sibcols = {}
    for st in A.stem.unique():
        cols = set()
        for q in OUT.glob(f"{st}.*csv"):
            try:
                with q.open() as fh:
                    cols |= {c.strip() for c in fh.readline().strip().split(",")}
            except Exception:
                pass
        sibcols[st] = cols
    sib = []
    for _, r in A.iterrows():
        cols = sibcols[r.stem]
        miss = [k for k, rx in NEED.items() if not any(rx.search(c) for c in cols)]
        sib.append("DECIDABLE-via-siblings" if not miss
                   else "UNDECIDABLE-even-with-siblings-missing:" + "+".join(miss))
    A["decidable_siblings"] = sib
    return A, tot_files, tot_rows


def census_prose():
    """The prose form of the same claim: committed *.result.md memos and LEADERBOARD.md rows."""
    hits = []
    srcs = [p for p in sorted(OUT.glob("*.result.md")) if not p.name.startswith(STEM)]
    srcs += [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md",
             ROOT / "research" / "QUEUE.md"]
    for p in srcs:
        if not p.exists():
            continue
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(txt.split("\n"), 1):
            if D3.search(line):
                hits.append(dict(file=p.name, line=i, excerpt=line.strip()[:220]))
    return pd.DataFrame(hits)


def restate_committed():
    """Re-quote the record's DECIDABLE published per-armed rows with their CONC/ACT/LEAK split,
    recomputed here from the committed columns (never copied from a published split column)."""
    g = OUT / "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C.grid.csv"
    m = OUT / "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C.mechanism.csv"
    if not (g.exists() and m.exists()):
        return pd.DataFrame(), pd.DataFrame()
    G = pd.read_csv(g)
    Mm = pd.read_csv(m)
    key = ["panel", "book", "cost", "instr"]
    alw = (G[G.regime == "always"][key + ["d_ann"]].rename(columns={"d_ann": "L_always"}))
    C = G[G.regime.isin(CONDS)].merge(Mm, on=key + ["regime"], how="left").merge(alw, on=key,
                                                                                how="left")
    f = C.armed_frac
    C["total"] = C.L_per_armed - C.L_always
    C["CONC"] = (1.0 - f) * (C.d_on - C.d_off)
    C["ACT"] = C.d_cond_on - C.d_on
    C["LEAK"] = ((1.0 - f) / f) * C.d_cond_off
    C["ident"] = (C.total - C.CONC - C.ACT - C.LEAK).abs()
    C["total_ex"] = C.total - C.LEAK
    C["unnorm"] = C.d_ann - C.L_always
    C["flip_LEAK"] = [sgn(a) != sgn(b) for a, b in zip(C.total, C.total_ex)]
    C["flip_unnorm"] = [sgn(a) != sgn(b) for a, b in zip(C.total, C.unnorm)]
    C["dominated"] = C.total_ex.abs() < DOM_FRAC * C.total.abs()
    return G, C


# ==================================================================== PART B — the live corpus
def ann(r):
    return float(r.mean() * 252 * 100.0)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    ms = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=ms["MaxDD"], scagr=ms["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def keep_paths(r, live, bars):
    """4a against the LIVE book handed in (RULES v2 primary), 4b against SPY incl. the OOS leg."""
    h1, h2 = halves(r)
    b1, b2 = halves(live)
    mm, mo = metrics(r), metrics(r.loc[OOS_START:])
    mv = metrics(live)
    p4a = bool(h1 > b1 and h2 > b2 and mm["MaxDD"] >= mv["MaxDD"])
    p4b = bool(h1 > bars["s1"] and h2 > bars["s2"] and mo["Sharpe"] > bars["soos"]
               and abs(mm["MaxDD"]) <= 0.60 * abs(bars["sdd"])
               and mm["CAGR"] >= 0.70 * bars["scagr"])
    return p4a, p4b, h1, h2, mm, mo


def split(d, on, lo=None, hi=None):
    """(annualised mean on ON days, on OFF days, armed fraction) over an optional sub-window."""
    dd = d.loc[lo:hi] if (lo is not None or hi is not None) else d
    oo = on.reindex(dd.index).fillna(False)
    f = float(oo.mean())
    a = float(dd[oo].mean() * 252 * 100) if oo.any() else np.nan
    b = float(dd[~oo].mean() * 252 * 100) if (~oo).any() else np.nan
    return a, b, f, float(dd.mean() * 252 * 100)


def decompose(d_alw, d_cond, on, lo=None, hi=None):
    """idea 246's exact split, over any window.  Returns the full dict incl. the identity."""
    d_on, d_off, f, L_always = split(d_alw, on, lo, hi)
    c_on, c_off, f2, d_ann_c = split(d_cond, on, lo, hi)
    L_pa = d_ann_c / f if f > 0 else np.nan
    tot = L_pa - L_always
    conc = (1.0 - f) * (d_on - d_off)
    act = c_on - d_on
    leak = ((1.0 - f) / f) * c_off if f > 0 else np.nan
    return dict(armed_frac=f, d_on=d_on, d_off=d_off, d_cond_on=c_on, d_cond_off=c_off,
                d_ann=d_ann_c, L_always=L_always, L_per_armed=L_pa, total=tot,
                CONC=conc, ACT=act, LEAK=leak, ident=abs(tot - conc - act - leak),
                total_ex=tot - leak, unnorm=d_ann_c - L_always)


def main():
    grid, cover, dec, wf, checked = [], [], [], [], False

    # ---------------------------------------------------------------- PART A
    say("=" * 190)
    say("PART A — CENSUS OF THE RECORD'S PER-ARMED-DAY CLAIMS (backtest-free)")
    A, nfiles, nrows = census_csv()
    P = census_prose()
    A.to_csv(OUT / f"{STEM}.census.csv", index=False)
    P.to_csv(OUT / f"{STEM}.prose.csv", index=False)
    say(f"\nscanned {nfiles} committed research/backtests/*.csv files, {nrows:,} published rows")
    if A.empty:
        say("  NO file in the record publishes a per-armed/per-active normalisation.")
    else:
        say(f"  files with a per-armed-day normalisation: {len(A)} "
            f"({int(A.rows.sum()):,} rows)")
        say(A.to_string(index=False))
        say("\n  by detector / decidability FROM THE FILE ALONE:")
        say(A.groupby(["detector", "decidable"]).agg(files=("file", "size"),
                                                     rows=("rows", "sum")).to_string())
        say("\n  by detector / decidability WITH THE PARENT SCRIPT'S SIBLING FILES "
            "(the honest denominator — an auditor has the whole commit):")
        say(A.groupby(["detector", "decidable_siblings"]).agg(
            files=("file", "size"), rows=("rows", "sum")).to_string())
        d1n = A[A.detector.str.startswith("D1")]
        say(f"\n  EXPLICIT per-armed rows in the record: {int(d1n.rows.sum()):,} over "
            f"{len(d1n)} files; of these, restatable with siblings: "
            f"{int(d1n[d1n.decidable_siblings == 'DECIDABLE-via-siblings'].rows.sum()):,}")
        say(f"  LATENT (armed/active fraction + a delta, no split published): "
            f"{int(A[A.detector.str.startswith('D2')].rows.sum()):,} rows over "
            f"{len(A[A.detector.str.startswith('D2')])} files — an UPPER BOUND on the record's "
            f"unaudited exposure, since not every such file quotes a per-armed number")
    say(f"\nPROSE census (committed *.result.md + LEADERBOARD.md + CHANGELOG.md + QUEUE.md): "
        f"{len(P)} lines carry the per-armed phrasing")
    if not P.empty:
        say(P.groupby("file").size().sort_values(ascending=False).to_string())
        say("\n  every prose hit:")
        say(P.to_string(index=False))

    Graw, RC = restate_committed()
    if not RC.empty:
        RC.to_csv(OUT / f"{STEM}.restated_record.csv", index=False)
        say("\n--- THE RECORD RESTATED (every decidable published per-armed row, split "
            "recomputed here from the committed columns) ---")
        say(f"  rows restated: {len(RC)}   max|identity residual| = {RC.ident.max():.3e} "
            f"-> {'EXACT' if RC.ident.max() < 1e-8 else 'BROKEN'}")
        p, kneg, n = signtest(RC.LEAK)
        say(f"  LEAK  median {RC.LEAK.median():+.4f} pp/yr, negative {kneg}/{n}, sign p {p:.4g}")
        say(f"  |LEAK| median {RC.LEAK.abs().median():.4f} vs |CONC|+|ACT| median "
            f"{(RC.CONC.abs() + RC.ACT.abs()).median():.4f}")
        say(f"  published verdict sign(total) flips when LEAK is removed: "
            f"{int(RC.flip_LEAK.sum())}/{len(RC)} ({RC.flip_LEAK.mean():.1%})")
        say(f"  ... and vs the UNNORMALISED comparison: "
            f"{int(RC.flip_unnorm.sum())}/{len(RC)} ({RC.flip_unnorm.mean():.1%})")
        say(f"  LEAK-dominated (|total-LEAK| < 0.5|total|): {int(RC.dominated.sum())}/{len(RC)} "
            f"({RC.dominated.mean():.1%})")

    # ---------------------------------------------------------------- PART B
    say("\n" + "=" * 190)
    say("PART B — FRESH CORPUS IN THE RECORD'S SHAPE (891 runs, every point printed)")
    for pname in PANELS:
        px, names = M.panel(pname)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bars = bars_of(spy)
        sub = px[names]
        v1w = rules_v1_weights(sub).reindex(columns=px.columns).fillna(0.0)
        v2w = rules_v2_weights(sub).reindex(columns=px.columns).fillna(0.0)
        v1 = {c: backtest(px, v1w, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        v2 = {c: backtest(px, v2w, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        ms = metrics(spy)
        m2 = metrics(v2[PROTO_COST])
        say("\n" + "=" * 190)
        say(f"PANEL {pname}: {len(names)} tradable names, {px.index[0].date()} -> "
            f"{px.index[-1].date()} | eval {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
        say(f"  SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"OOS Sharpe {bars['soos']:.3f} | 4b bars: DD cap {0.60*abs(bars['sdd']):.2%}, "
            f"CAGR floor {0.70*bars['scagr']:.2%}")
        say(f"  LIVE RULES v2 @10bps: CAGR {m2['CAGR']:.2%} Sharpe {m2['Sharpe']:.3f} "
            f"MaxDD {m2['MaxDD']:.2%} OOS Sharpe "
            f"{metrics(v2[PROTO_COST].loc[OOS_START:])['Sharpe']:.3f}")

        arms = {r: M.regime(px, names, r) for r in REGIMES}
        for r in REGIMES:
            v = arms[r].loc[start:]
            cover.append(dict(panel=pname, regime=r, armed_frac=float(v.mean()),
                              armed_days=int(v.sum()), frac_IS=float(v.loc[:IS_END].mean()),
                              frac_OOS=float(v.loc[OOS_START:].mean())))

        for book in BOOKS:
            W_base = H.targets(sub, book).reindex(columns=px.columns).fillna(0.0)
            W_gate = {g: H.targets(sub, book, g, "dg").reindex(columns=px.columns).fillna(0.0)
                      for g in ("g200", "band3", "abs12", "vol60")}
            for cost in COSTS:
                ctl = M.run_cond(px, W_base, bps=cost)
                rc = ctl["r"].loc[start:]
                mc = metrics(rc)
                p4a, p4b, h1, h2, mm, mo = keep_paths(rc, v2[cost], bars)
                p4a1 = bool(h1 > halves(v1[cost])[0] and h2 > halves(v1[cost])[1]
                            and mm["MaxDD"] >= metrics(v1[cost])["MaxDD"])
                grid.append(dict(panel=pname, book=book, cost=cost, instr="control", regime="-",
                                 armed_frac=np.nan, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                                 MaxDD=mm["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=mo["Sharpe"],
                                 OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"], ann_pp=ann(rc),
                                 d_ann=0.0, L_per_armed=np.nan, total=np.nan, LEAK=np.nan,
                                 gross=float(ctl["gross"].loc[start:].mean()),
                                 turn_yr=float(ctl["to"].loc[start:].sum() / (len(rc) / 252)),
                                 pass4a_v2=p4a, pass4a_v1=p4a1, pass4b=p4b,
                                 IS_Sharpe=metrics(rc.loc[:IS_END])["Sharpe"]))

                for ins in INSTR:
                    sp = SPEC[ins]
                    kw = dict(W_gate=W_gate[sp["gate"]] if sp["kind"] == "gate" else None,
                              stop=sp.get("stop"), D=sp.get("D"), k=sp.get("k", 1.0),
                              m=sp.get("m", 1.0))
                    alw = M.run_cond(px, W_base, armed=arms["always"], bps=cost, **kw)
                    d_alw = (alw["r"] - ctl["r"]).loc[start:]

                    if not checked:                       # CHECK (b): always-on == idea 94's own
                        ref = H.run(px, W_gate[sp["gate"]] if sp["kind"] == "gate" else W_base,
                                    m=sp.get("m", 1.0), stop=sp.get("stop"), D=sp.get("D"),
                                    k=sp.get("k", 1.0), reset="recover", bps=cost)
                        w = float((alw["r"] - ref["r"]).abs().max())
                        say(f"  CHECK (b) {pname}/{book}/{ins}@{cost:g} always-on vs idea 94 "
                            f"`run`: max|d| = {w:.3e} -> {'EXACT' if w < 1e-12 else 'MISMATCH'}")
                        assert w < 1e-12, (ins, w)

                    for reg in REGIMES:
                        a = alw if reg == "always" else M.run_cond(px, W_base, armed=arms[reg],
                                                                  bps=cost, **kw)
                        ra = a["r"].loc[start:]
                        d = (ra - rc)
                        f = float(arms[reg].loc[start:].mean())
                        p4a, p4b, hh1, hh2, mmx, mox = keep_paths(ra, v2[cost], bars)
                        p4a1 = bool(hh1 > halves(v1[cost])[0] and hh2 > halves(v1[cost])[1]
                                    and mmx["MaxDD"] >= metrics(v1[cost])["MaxDD"])
                        row = dict(panel=pname, book=book, cost=cost, instr=ins, regime=reg,
                                   armed_frac=f, CAGR=mmx["CAGR"], Sharpe=mmx["Sharpe"],
                                   MaxDD=mmx["MaxDD"], H1=hh1, H2=hh2, OOS_Sharpe=mox["Sharpe"],
                                   OOS_CAGR=mox["CAGR"], OOS_MaxDD=mox["MaxDD"], ann_pp=ann(ra),
                                   d_ann=ann(ra) - ann(rc),
                                   L_per_armed=(ann(ra) - ann(rc)) / f if f > 0 else np.nan,
                                   gross=float(a["gross"].loc[start:].mean()),
                                   turn_yr=float(a["to"].loc[start:].sum() / (len(ra) / 252)),
                                   pass4a_v2=p4a, pass4a_v1=p4a1, pass4b=p4b,
                                   IS_Sharpe=metrics(ra.loc[:IS_END])["Sharpe"])
                        if reg in CONDS:
                            full = decompose(d_alw, d, arms[reg])
                            isw = decompose(d_alw, d, arms[reg], hi=IS_END)
                            oos = decompose(d_alw, d, arms[reg], lo=OOS_START)
                            row.update(total=full["total"], LEAK=full["LEAK"])
                            rec = dict(panel=pname, book=book, cost=cost, instr=ins, regime=reg,
                                       stateful=ins in STATEFUL, **full)
                            rec.update({f"IS_{k}": v for k, v in isw.items()
                                        if k in ("armed_frac", "L_per_armed", "total", "CONC",
                                                 "ACT", "LEAK", "total_ex")})
                            rec.update({f"OOS_{k}": v for k, v in oos.items()
                                        if k in ("armed_frac", "L_per_armed", "total", "CONC",
                                                 "ACT", "LEAK", "total_ex")})
                            rec["flip_LEAK"] = sgn(full["total"]) != sgn(full["total_ex"])
                            rec["flip_unnorm"] = sgn(full["total"]) != sgn(full["unnorm"])
                            rec["flip_CONC"] = sgn(full["total"]) != sgn(full["CONC"])
                            rec["dominated"] = (abs(full["total_ex"])
                                                < DOM_FRAC * abs(full["total"]))
                            rec["absLEAK"] = abs(full["LEAK"])
                            rec["absOTH"] = abs(full["CONC"]) + abs(full["ACT"])
                            rec["OOS_Sharpe"] = mox["Sharpe"]
                            rec["OOS_CAGR"] = mox["CAGR"]
                            rec["OOS_MaxDD"] = mox["MaxDD"]
                            dec.append(rec)
                        else:
                            row.update(total=np.nan, LEAK=np.nan)
                        grid.append(row)
                    checked = True
            say(f"  built {pname}/{book}")

        # ------------------------------------------------ RULE 8, per (panel, book, cost) cell
        D0 = pd.DataFrame(dec)
        for book in BOOKS:
            for cost in COSTS:
                sel = D0[(D0.panel == pname) & (D0.book == book) & (D0.cost == cost)]
                if sel.empty:
                    continue
                G0 = pd.DataFrame(grid)
                cell = G0[(G0.panel == pname) & (G0.book == book) & (G0.cost == cost)]
                ctlrow = cell[cell.instr == "control"].iloc[0]
                menu = cell[cell.regime.isin(CONDS)]
                oracle = menu.OOS_Sharpe.max()
                picks = {
                    "published(IS L_per_armed)": sel.loc[sel.IS_L_per_armed.idxmax()],
                    "LEAK-purged(IS L_pa - IS LEAK)":
                        sel.loc[(sel.IS_L_per_armed - sel.IS_LEAK).idxmax()],
                    "IS Sharpe (record convention)":
                        menu.loc[menu.IS_Sharpe.idxmax()],
                }
                for lab, r in picks.items():
                    m = menu[(menu.instr == r.instr) & (menu.regime == r.regime)].iloc[0]
                    wf.append(dict(panel=pname, book=book, cost=cost, rule=lab,
                                   pick=f"{r.instr}/{r.regime}", OOS_CAGR=m.OOS_CAGR,
                                   OOS_Sharpe=m.OOS_Sharpe, OOS_MaxDD=m.OOS_MaxDD,
                                   ctl_OOS_Sharpe=ctlrow.OOS_Sharpe,
                                   ctl_OOS_CAGR=ctlrow.OOS_CAGR,
                                   regret_vs_donothing=m.OOS_Sharpe - ctlrow.OOS_Sharpe,
                                   regret_vs_oracle=m.OOS_Sharpe - oracle,
                                   v2_OOS_Sharpe=metrics(v2[cost].loc[OOS_START:])["Sharpe"],
                                   v2_OOS_CAGR=metrics(v2[cost].loc[OOS_START:])["CAGR"],
                                   v2_OOS_MaxDD=metrics(v2[cost].loc[OOS_START:])["MaxDD"],
                                   spy_OOS_Sharpe=bars["soos"],
                                   spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                                   spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"]))

    G = pd.DataFrame(grid)
    C = pd.DataFrame(cover)
    D = pd.DataFrame(dec)
    W = pd.DataFrame(wf)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    C.to_csv(OUT / f"{STEM}.coverage.csv", index=False)
    D.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- reports
    say("\n" + "=" * 190)
    say("=== B1. REGIME COVERAGE (post-warm-up; idea 247's IS/OOS asymmetry, uncorrected) ===")
    say(C.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n=== B2. EVERY GRID POINT (891 rows; 4a/4b evaluated on each) ===")
    for cost in COSTS:
        say(f"\n--- cost {cost:g} bps ---")
        say(G[G.cost == cost].drop(columns=["cost"]).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 190)
    say("=== B3. THE IDENTITY (total = CONC + ACT + LEAK), every live cell ===")
    say(f"  cells {len(D)}   max|residual| = {D.ident.max():.3e} "
        f"-> {'EXACT' if D.ident.max() < 1e-8 else 'BROKEN'}")

    say("\n=== H1 — IS LEAK A GENERAL TAX?  (a) systematic sign  (b) dominance ===")
    p, kneg, n = signtest(D.LEAK)
    share = kneg / n if n else np.nan
    a_ok = bool(share >= TAX_SHARE and p < TAX_P)
    b_ok = bool(D.absLEAK.median() >= D.absOTH.median())
    say(f"  (a) LEAK negative in {kneg}/{n} = {share:.1%} of live cells, exact sign p {p:.4g} "
        f"-> bar (>= {TAX_SHARE:.1%} and p < {TAX_P}) {'MET' if a_ok else 'NOT MET'}")
    say(f"  (b) median |LEAK| {D.absLEAK.median():.4f} vs median (|CONC|+|ACT|) "
        f"{D.absOTH.median():.4f} -> dominance {'MET' if b_ok else 'NOT MET'}")
    say(f"  median LEAK {D.LEAK.median():+.4f} pp/yr, mean {D.LEAK.mean():+.4f}, "
        f"IQR [{D.LEAK.quantile(.25):+.4f}, {D.LEAK.quantile(.75):+.4f}]")
    say(f"  median share of |total| carried by |LEAK|: "
        f"{(D.absLEAK / (D.absLEAK + D.absOTH)).median():.1%}")
    say(f"  H1 VERDICT: {'CONFIRMED' if (a_ok and b_ok) else ('PARTIAL — sign systematic, not dominant' if a_ok else ('PARTIAL — dominant, sign not systematic' if b_ok else 'REFUTED'))}")

    for by in ("regime", "instr", "cost", "panel", "stateful"):
        agg = D.groupby(by).agg(n=("LEAK", "size"), med_LEAK=("LEAK", "median"),
                                neg=("LEAK", lambda s: int((s < 0).sum())),
                                med_absLEAK=("absLEAK", "median"),
                                med_absOTH=("absOTH", "median"),
                                med_total=("total", "median"),
                                med_total_ex=("total_ex", "median"),
                                med_CONC=("CONC", "median"), med_ACT=("ACT", "median"))
        agg["LEAK_share"] = (agg.med_absLEAK / (agg.med_absLEAK + agg.med_absOTH))
        say(f"\n  by {by}:")
        say(agg.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n=== H2 — VERDICT FLIPS (sign(total) vs sign(total - LEAK), and vs unnormalised) ===")
    say(f"  LEAK removed:      {int(D.flip_LEAK.sum())}/{len(D)} verdicts flip "
        f"({D.flip_LEAK.mean():.1%})")
    say(f"  unnormalised:      {int(D.flip_unnorm.sum())}/{len(D)} flip "
        f"({D.flip_unnorm.mean():.1%})")
    say(f"  CONC alone (H4):   {int(D.flip_CONC.sum())}/{len(D)} flip "
        f"({D.flip_CONC.mean():.1%})")
    say(f"  pooled medians: total {D.total.median():+.4f} -> total-LEAK "
        f"{D.total_ex.median():+.4f} -> unnormalised {D.unnorm.median():+.4f} pp/yr "
        f"(POOLED SIGN {'INVERTS' if sgn(D.total.median()) != sgn(D.total_ex.median()) else 'SURVIVES'} "
        f"on LEAK removal)")
    pt, kt, nt = signtest(D.total)
    pe, ke, ne = signtest(D.total_ex)
    say(f"  sign test: total negative {kt}/{nt} p {pt:.4g}   |   total-LEAK negative "
        f"{ke}/{ne} p {pe:.4g}")
    fl = D.groupby(["regime"]).agg(n=("flip_LEAK", "size"), flip_LEAK=("flip_LEAK", "sum"),
                                   flip_unnorm=("flip_unnorm", "sum"),
                                   flip_CONC=("flip_CONC", "sum"),
                                   dominated=("dominated", "sum"))
    say("\n  by regime:")
    say(fl.to_string())
    fi = D.groupby(["instr"]).agg(n=("flip_LEAK", "size"), flip_LEAK=("flip_LEAK", "sum"),
                                  flip_unnorm=("flip_unnorm", "sum"),
                                  dominated=("dominated", "sum"))
    say("\n  by instrument:")
    say(fi.to_string())

    say("\n=== H3 — LEAK DOMINANCE (idea 261's majority convention) ===")
    say(f"  |total - LEAK| < 0.5|total| in {int(D.dominated.sum())}/{len(D)} cells "
        f"({D.dominated.mean():.1%})")
    small = D[D.total.abs() < 0.02]
    say(f"  cells with no publishable magnitude (|total| < 0.02 pp/yr): {len(small)}; "
        f"excluding them, dominated {int(D[D.total.abs() >= 0.02].dominated.sum())}/"
        f"{len(D[D.total.abs() >= 0.02])}")

    say("\n=== H4 — DOES THE NAMED MECHANISM (CONC) CARRY THE VERDICT? ===")
    say(f"  sign(CONC) == sign(total) in {len(D) - int(D.flip_CONC.sum())}/{len(D)} cells "
        f"({1 - D.flip_CONC.mean():.1%})")
    say(f"  median CONC {D.CONC.median():+.4f}, ACT {D.ACT.median():+.4f}, "
        f"LEAK {D.LEAK.median():+.4f}, total {D.total.median():+.4f} pp/yr")
    say(f"  median |CONC| share of (|CONC|+|ACT|+|LEAK|): "
        f"{(D.CONC.abs() / (D.CONC.abs() + D.ACT.abs() + D.LEAK.abs())).median():.1%}")

    say("\n=== B4. THE 0 BPS RUNG — is LEAK a COST artefact or a HOLDINGS artefact? ===")
    z = D.groupby("cost").agg(n=("LEAK", "size"), med_LEAK=("LEAK", "median"),
                              med_absLEAK=("absLEAK", "median"),
                              neg=("LEAK", lambda s: int((s < 0).sum())),
                              med_total=("total", "median"))
    say(z.to_string(float_format=lambda x: f"{x:.4f}"))
    say("  If LEAK survives at 0 bps it is carried-over HOLDINGS, not the switching bill.")

    say("\n=== H5 — KEEP PATHS, all 891 rows ===")
    kp = G.groupby(G.regime.map(lambda r: "control" if r == "-"
                                else ("always" if r == "always" else "conditional"))).agg(
        n=("pass4b", "size"), pass4a_v2=("pass4a_v2", "sum"), pass4a_v1=("pass4a_v1", "sum"),
        pass4b=("pass4b", "sum"))
    say(kp.to_string())
    best = G[G.pass4b].sort_values("CAGR", ascending=False).head(12)
    if best.empty:
        say("  NO row passes 4b.")
    else:
        say("\n  best 4b passers by CAGR:")
        say(best[["panel", "book", "cost", "instr", "regime", "CAGR", "Sharpe", "MaxDD",
                  "H1", "H2", "OOS_Sharpe", "pass4a_v2"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
        cond_only = 0
        for _, r in G[G.pass4b & G.regime.isin(CONDS)].iterrows():
            sib = G[(G.panel == r.panel) & (G.book == r.book) & (G.cost == r.cost)
                    & (G.instr == r.instr) & (G.regime == "always")]
            ctl = G[(G.panel == r.panel) & (G.book == r.book) & (G.cost == r.cost)
                    & (G.instr == "control")]
            if not bool(sib.pass4b.any()) and not bool(ctl.pass4b.any()):
                cond_only += 1
        say(f"  conditional 4b passes whose OWN always-on sibling AND control both FAIL: "
            f"{cond_only}")

    say("\n=== RULE 8 — WALK-FORWARD (params chosen on IS 2009-2016, read once on OOS) ===")
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  pooled by selection rule:")
    ws = W.groupby("rule").agg(n=("OOS_Sharpe", "size"), med_OOS_Sharpe=("OOS_Sharpe", "median"),
                               med_OOS_CAGR=("OOS_CAGR", "median"),
                               med_OOS_MaxDD=("OOS_MaxDD", "median"),
                               med_regret_donothing=("regret_vs_donothing", "median"),
                               beat_donothing=("regret_vs_donothing", lambda s: int((s > 0).sum())),
                               med_regret_oracle=("regret_vs_oracle", "median"))
    say(ws.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"\n  benchmarks (median over cells): live RULES v2 OOS Sharpe "
        f"{W.v2_OOS_Sharpe.median():.4f} CAGR {W.v2_OOS_CAGR.median():.2%} MaxDD "
        f"{W.v2_OOS_MaxDD.median():.2%} | SPY OOS Sharpe {W.spy_OOS_Sharpe.median():.4f} "
        f"CAGR {W.spy_OOS_CAGR.median():.2%} MaxDD {W.spy_OOS_MaxDD.median():.2%}")
    agree = (W[W.rule.str.startswith("published")].reset_index(drop=True).pick
             == W[W.rule.str.startswith("LEAK")].reset_index(drop=True).pick)
    say(f"  published pick == LEAK-purged pick in {int(agree.sum())}/{len(agree)} cells "
        f"({agree.mean():.1%}) — the normaliser CHANGES the chosen arm in "
        f"{len(agree) - int(agree.sum())}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG))
    say(f"\nwrote {STEM}.{{census,prose,restated_record,grid,coverage,decomp,walkforward}}.csv "
        f"+ .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
