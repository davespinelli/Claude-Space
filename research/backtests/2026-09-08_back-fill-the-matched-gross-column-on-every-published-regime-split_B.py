#!/usr/bin/env python3
"""QUEUE idea 471 — back-fill-the-matched-gross-column-on-every-published-d_on-d_off-regime-split
(lane B, 2026-09-08)

QUESTION (pre-registered, verbatim from QUEUE.md idea 471)
    "idea 249 showed idea 246's headline '+12.6 and +5.8 pp/yr ON crash days' for `gross50`/
    `ddctl8` is pure gross arithmetic: against a control at the arm's OWN realised mean gross
    the surplus inverts to -0.94/-0.97 pp/yr and Sharpe goes to a coin flip.  Any regime-split
    delta measured against a full-gross control carries the same confound.  Census the record's
    committed `.regime.csv` / `.mech.csv` files for d_on/d_off splits whose arm and control
    differ in mean realised gross, re-quote each as an excess over a gross-matched static, and
    report how many published regime claims survive the restatement.  Max 2 params."

TWO PARTS, BOTH REQUIRED
    PART A (census, backtest-free).  Every committed `research/backtests/*.csv` is scanned for a
        REGIME-SPLIT column set.  For each such file the question is only: does it publish a
        realised-gross column for the ARM *and* for the COMPARAND, so that the confound idea 249
        named can be adjudicated from the committed file at all?  Idea 470 found 64.1% of
        published non-count DIAL cells publish no gross column; the same measurement is made
        here for regime splits, and the record-wide ladder rate is reported as a BOUND, never as
        a point, over the undecidable remainder.
    PART B (live, by construction).  Because part A's decidable set is expected to be small, the
        restatement itself is done on a fresh corpus built to the record's own shape: idea 246's
        8 instruments x 3 regimes, priced on 3 panels x 3 base books x 3 cost rungs, every arm
        re-quoted against (i) the full-gross do-nothing control the record actually publishes and
        (ii) a gross-matched static.  SURVIVAL is pre-registered below and counted.

WHY A SECOND MATCHED CONTROL EXISTS HERE THAT IDEA 249 DID NOT NEED
    Idea 249 matched on FULL-SAMPLE mean realised gross.  For a regime-conditional arm the gross
    deficit is concentrated in the ARMED regime by construction: OFF the regime the instrument
    does not act, so the arm IS the base book there.  A full-sample match therefore still leaves
    an ON-regime gross gap (it spreads the arm's deficit over days on which the arm never
    de-grossed), which is exactly the quantity a d_on claim is measured in.  So two matched
    statics are solved for every arm and both are reported:
        MF   constant-gross static at the arm's FULL-SAMPLE mean realised gross  (idea 249's)
        MON  constant-gross static at the arm's ON-REGIME mean realised gross    (the strict one)
    MON is PRIMARY for d_on.  For d_off the arm's own gross equals the control's by construction,
    so the control IS the matched comparand there and both are reported to show it.

PRE-REGISTERED HYPOTHESES
H1 (the census)    What fraction of the record's committed regime-split rows can be adjudicated
        from the committed file — i.e. publish realised gross for both arm and comparand?
        Reported as a count and as a bound; no verdict is asserted over the undecidable part.
H2 (survival)      A published-style regime claim SURVIVES the restatement iff, at 10 bps,
        (a) sign(d_on) is preserved when the control is replaced by the matched static, AND
        (b) |d_on_restated| >= 0.5 * |d_on_published|   (idea 261's majority-cost convention).
        Counted over all live cells, against MON (primary) and MF (idea 249's convention).
H3 (the claim shape)  The record's regime claims are usually of the form "d_on > d_off — the
        armed regime is the one regime the instrument pays in".  How often does that ORDERING
        survive the restatement?  Falsified for the corpus if the ordering flips in a majority.
H4 (is anything left)  Is the restated d_on distinguishable from zero?  Exact two-sided sign
        test over cells, per instrument family and pooled.  If the restated d_on is a coin flip,
        regime-conditioning has no content beyond gross arithmetic.
H5 (KEEP paths)    PROTOCOL rule 4a (vs the LIVE RULES v2 book on the same panel) and rule 4b
        (vs SPY, incl. the OOS leg) evaluated on EVERY row — conditional arms, always-on
        siblings, the do-nothing control and BOTH matched statics — so a pass the matched static
        already has is never credited to the regime conditioning.
RULE 8 (required)  In each (panel, book, cost) cell the pair (INSTRUMENT, REGIME) is chosen on
        2009-2016 IS ALONE by the PUBLISHED statistic (IS d_on vs the full-gross control) and
        read ONCE on 2017-2026.  The same pick is repeated under the RESTATED statistic (IS d_on
        vs MON).  Regret is reported against do-nothing (0.0) and against that cell's OOS oracle.
        OOS CAGR / Sharpe / MaxDD of the selected book are reported against the live RULES v2
        baseline and against SPY, as PROTOCOL step 3 requires.

GRID — exactly TWO tuned parameters (INSTRUMENT, REGIME).  Every grid point printed and written.
      INSTRUMENT  idea 246's 8: g200-dg, band3-dg, abs12-dg, vol60-dg (per-name gates),
                  stop15, stop25 (trailing stops), ddctl8 (book DD control), gross50 (de-gross)
      REGIME      spy200 (SPY < its own 200d MA), breadth20 (panel breadth <= expanding 20th
                  pct, 3y min), hivol80 (SPY 20d vol >= expanding 80th pct, 3y min)
      panels      u56 (56), broad (136), small (439 sub-$2B after idea 130's bad-split drop;
                  SPY held as benchmark only)                        [reported, not tuned]
      books       V1u, TOP20, EWall — idea 94's three ungated base books  [reported, not tuned]
      costs       0, 10 (PROTOCOL rung), 25 bps; every arm re-run at each rung, never derived
                  from a turnover identity, because the stop and DD state machines read NET
                  equity and so their BOOKS are cost-dependent.       [reported, not tuned]

ARMING MECHANICS: idea 94's harness and idea 246's `run_cond`, imported, not re-implemented.
    Arming gates the instrument's ACTION, never its STATE.  The regime is read at close t-1 and
    applied at t; breadth20 / hivol80 use EXPANDING quantiles with a 3y minimum, so no
    full-sample threshold enters anywhere.

SURVIVORSHIP: all three panels are current-constituent lists (idea 54), so every absolute CAGR
    is optimistic.  H2-H4 are paired differences inside one cell on the same days and are far
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

STEM = "2026-09-08_back-fill-the-matched-gross-column-on-every-published-regime-split_B"
OUT = ROOT / "research" / "backtests"

_spec = importlib.util.spec_from_file_location(
    "i246", OUT / "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
H = M.H                                                    # idea 94's harness, via idea 246

FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START
PROTO_COST = 10.0
COSTS = [0.0, 10.0, 25.0]
PANELS = ["u56", "broad", "small"]
BOOKS = ["V1u", "TOP20", "EWall"]
REGIMES = ["spy200", "breadth20", "hivol80"]               # spy200 primary
INSTR = M.INSTR                                            # idea 246's 8, unchanged
SPEC = M.SPEC
MATCH_TOL = 1e-4
MATCH_ITERS = 8
SURVIVE_FRAC = 0.50                                        # idea 261's majority-cost convention
GROSS_GAP_BAR = 0.05                                       # idea 244's 5 pp realised-gross bar

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
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


# ==================================================================== PART A — the census
REG_TOK = re.compile(
    r"(?:^|_)(?:regime|armed|crash|fall|rise|bear|bull|stress|"
    r"spy200|breadth20|hivol80|risk_?on|risk_?off)(?:$|_)"
    r"|^(?:on|off)_|_(?:on|off)$", re.I)
GROSS_TOK = re.compile(r"gross", re.I)
ARMLAB_TOK = re.compile(r"^(arm|book|instr|instrument|variant|leg|label|name)$", re.I)
CTL_VAL = re.compile(r"(?:control|ctl|none|do.?nothing|base|always|ungated|full)", re.I)


def is_regime_col(c, cols):
    """Does this column name an ON/OFF REGIME split?

    Deliberately conservative, because two shapes in the record look like one and are not:
      * 'Calmar' contains 'calm'                                        -> never a regime column;
      * a BARE 'on' / 'off' column is a rebalance-PHASE offset far more often than a regime
        (e.g. the cadence-phase corpus, which publishes `shift` and `off` side by side), so a
        bare name counts only when its opposite number is present in the same file.
    Everything else must carry the affix form (`on_share`, `d_off`, `CAGR_on`, `FALL_Sharpe`,
    `armed_frac`, `regime`, ...).  Miscounts therefore run toward UNDER-counting the record's
    regime claims, which is the safe direction for a coverage bound."""
    if re.search(r"calmar", c, re.I):
        return False
    low = {x.lower() for x in cols}
    if c.lower() in ("on", "off"):
        return "on" in low and "off" in low
    return bool(REG_TOK.search(c))


def census():
    """Scan every committed research/backtests/*.csv for regime-split claims and ask whether the
    committed file itself carries enough gross columns to adjudicate idea 249's confound."""
    # this script's OWN outputs are excluded so the census is deterministic on re-run
    files = sorted(p for p in OUT.glob("*.csv") if not p.name.startswith(STEM))
    rows = []
    tot_rows = 0
    for p in files:
        try:
            with p.open() as fh:
                hdr = fh.readline().strip()
        except Exception:
            continue
        if not hdr:
            continue
        cols = [c.strip() for c in hdr.split(",")]
        nrow = max(0, sum(1 for _ in p.open()) - 1)
        tot_rows += nrow
        rc = [c for c in cols if is_regime_col(c, cols)]
        if not rc:
            continue
        gc = [c for c in cols if GROSS_TOK.search(c)]
        lab = [c for c in cols if ARMLAB_TOK.match(c)]
        # decidability: either >=2 gross columns (arm and comparand published side by side),
        # or exactly 1 gross column PLUS an arm-label column carrying a control-looking level
        # (so arm and control gross can be paired within the file).
        kind, gap, ncell = "UNDECIDABLE-no-gross", np.nan, 0
        if len(gc) >= 2:
            kind = "DECIDABLE-paired-columns"
        elif len(gc) == 1 and lab:
            try:
                df = pd.read_csv(p)
                for L in lab:
                    vals = df[L].astype(str)
                    if vals.str.contains(CTL_VAL).any() and vals.nunique() > 1:
                        kind = "DECIDABLE-within-file-label"
                        break
                else:
                    kind = "UNDECIDABLE-one-gross-no-control-level"
            except Exception:
                kind = "UNDECIDABLE-unreadable"
        elif len(gc) == 1:
            kind = "UNDECIDABLE-one-gross-no-arm-label"
        rows.append(dict(file=p.name, rows=nrow, regime_cols="|".join(rc),
                         gross_cols="|".join(gc), arm_labels="|".join(lab), decidable=kind))
    C = pd.DataFrame(rows)
    return C, len(files), tot_rows


def census_gaps(C):
    """For the DECIDABLE files, measure the realised-gross gap the claim carries."""
    out = []
    for _, r in C[C.decidable.str.startswith("DECIDABLE")].iterrows():
        p = OUT / r.file
        try:
            df = pd.read_csv(p)
        except Exception:
            continue
        gcols = [c for c in r.gross_cols.split("|") if c]
        if r.decidable == "DECIDABLE-paired-columns":
            num = [c for c in gcols if pd.api.types.is_numeric_dtype(df[c])]
            if len(num) < 2:
                continue
            G = df[num]
            gap = (G.max(axis=1) - G.min(axis=1)).abs()
            for v in gap:
                out.append(dict(file=r.file, mode="paired", gap=float(v)))
        else:
            lab = [c for c in r.arm_labels.split("|") if c]
            g = gcols[0]
            if not lab or not pd.api.types.is_numeric_dtype(df[g]):
                continue
            L = lab[0]
            key = [c for c in df.columns
                   if c not in (L, g) and df[c].dtype == object and df[c].nunique() <= 40]
            ctl = df[df[L].astype(str).str.contains(CTL_VAL)]
            if ctl.empty:
                continue
            if key:
                m = df.merge(ctl.groupby(key, as_index=False)[g].mean().rename(
                    columns={g: "_gctl"}), on=key, how="left")
            else:
                m = df.assign(_gctl=float(ctl[g].mean()))
            gap = (m[g] - m["_gctl"]).abs()
            for v in gap.dropna():
                out.append(dict(file=r.file, mode="label", gap=float(v)))
    return pd.DataFrame(out)


# ==================================================================== PART B — the live corpus
def base_and_gate(px, names, instr, book, TG):
    """(W_base, W_gate, kwargs) for one instrument on one base book, in de-gross form.

    TG is a per-panel target cache so the ranking is computed once per (book, gate), not once
    per (book, gate, instrument, regime, cost)."""
    sp = SPEC[instr]
    if (book, None) not in TG:
        TG[(book, None)] = H.targets(px[names], book).reindex(
            columns=px.columns).fillna(0.0)
    W_base = TG[(book, None)]
    W_gate, kw = None, {}
    if sp["kind"] == "gate":
        k = (book, sp["gate"])
        if k not in TG:
            TG[k] = (H.targets(px[names], book, gate=sp["gate"], conv="dg")
                     .reindex(columns=px.columns).fillna(0.0))
        W_gate = TG[k]
    elif sp["kind"] == "stop":
        kw = dict(stop=sp["stop"])
    elif sp["kind"] == "dd":
        kw = dict(D=sp["D"], k=sp["k"])
    else:
        kw = dict(m=sp["m"])
    return W_base, W_gate, kw


def solve_matched(px, W_base, target, bps, cache):
    """Constant multiplier mu on the base book whose realised MEAN gross equals `target`.

    The static book's gross path is cost-independent in HOLDINGS but its returns are not, so the
    solve is done per cost rung.  A per-(book,cost) two-point seed is cached and refined by
    secant to MATCH_TOL; the achieved gap is returned and reported for every match."""
    key = id(W_base), bps
    if key not in cache:
        g1 = float(M.run_cond(px, W_base, m=1.0, bps=bps)["gross"].mean())
        cache[key] = g1
    g1 = cache[key]
    if target <= 1e-9:
        res = M.run_cond(px, W_base, m=0.0, bps=bps)
        return 0.0, res, abs(float(res["gross"].mean()) - target)
    mu = float(np.clip(target / g1, 0.0, 4.0))
    res = M.run_cond(px, W_base, m=mu, bps=bps)
    g = float(res["gross"].mean())
    lo_mu, lo_g, it = 0.0, 0.0, 0
    while abs(g - target) > MATCH_TOL and it < MATCH_ITERS:
        it += 1
        den = g - lo_g
        mu_new = mu + (target - g) * (mu - lo_mu) / den if abs(den) > 1e-12 else mu
        lo_mu, lo_g = mu, g
        mu = float(np.clip(mu_new, 0.0, 4.0))
        res = M.run_cond(px, W_base, m=mu, bps=bps)
        g = float(res["gross"].mean())
    return mu, res, abs(g - target)


def rowstats(r, to, gross, start, v2r, bars, on, off):
    """Everything one book contributes to the grid, incl. the regime split and the KEEP paths."""
    rr = r.loc[start:]
    p4a_v2, p4b, h1, h2, mm, mo = M.keep_paths(rr, v2r, bars)
    return dict(ann=M.ann(rr), ann_on=M.ann(rr[on.loc[start:]]), ann_off=M.ann(rr[off.loc[start:]]),
                CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                IS_Sharpe=metrics(rr.loc[:IS_END])["Sharpe"],
                IS_ann_on=M.ann(rr.loc[:IS_END][on.loc[start:IS_END]]),
                OOS_ann_on=M.ann(rr.loc[OOS_START:][on.loc[OOS_START:]]),
                IS_ann_off=M.ann(rr.loc[:IS_END][off.loc[start:IS_END]]),
                OOS_ann_off=M.ann(rr.loc[OOS_START:][off.loc[OOS_START:]]),
                turnover=float(to.loc[start:].mean() * 252),
                gross=float(gross.loc[start:].mean()),
                gross_on=float(gross.loc[start:][on.loc[start:]].mean()),
                gross_off=float(gross.loc[start:][off.loc[start:]].mean()),
                pass4a=p4a_v2, pass4b=p4b)


def main():
    # ---------------------------------------------------------------- PART A
    say("=" * 118)
    say("PART A — CENSUS of the committed record: which regime-split claims can be adjudicated?")
    say("=" * 118)
    C, nfiles, totrows = census()
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say(f"committed research/backtests/*.csv scanned : {nfiles}  ({totrows:,} data rows)")
    say(f"files carrying a REGIME-SPLIT column       : {len(C)}  ({int(C['rows'].sum()):,} rows"
        f" = {100.0*C['rows'].sum()/max(totrows,1):.2f}% of the record's rows)")
    dec = C.groupby("decidable", as_index=False).agg(files=("file", "size"), rows=("rows", "sum"))
    dec["pct_rows"] = 100.0 * dec["rows"] / max(int(C["rows"].sum()), 1)
    say("\nDECIDABILITY (does the committed file publish realised gross for arm AND comparand?)")
    say(dec.sort_values("rows", ascending=False).to_string(index=False,
        float_format=lambda x: f"{x:.1f}"))
    ndec_f = int(C.decidable.str.startswith("DECIDABLE").sum())
    ndec_r = int(C.loc[C.decidable.str.startswith("DECIDABLE"), "rows"].sum())
    say(f"\nH1 ANSWER: {ndec_f} of {len(C)} regime-split files ({100.0*ndec_f/max(len(C),1):.1f}%) "
        f"and {ndec_r:,} of {int(C['rows'].sum()):,} rows "
        f"({100.0*ndec_r/max(int(C['rows'].sum()),1):.1f}%) are GROSS-DECIDABLE from the "
        f"committed file.  The remainder cannot be adjudicated at all without a re-run.")
    say("\nEvery regime-split file, with its columns:")
    say(C.sort_values("rows", ascending=False).to_string(index=False))
    GAP = census_gaps(C)
    if len(GAP):
        GAP.to_csv(OUT / f"{STEM}.censusgap.csv", index=False)
        nlad = int((GAP.gap >= GROSS_GAP_BAR).sum())
        say(f"\nDecidable cells with a realised-gross gap >= {GROSS_GAP_BAR:.2f} NAV between arm "
            f"and comparand: {nlad} of {len(GAP)} ({100.0*nlad/len(GAP):.1f}%)")
        say(GAP.groupby("file").gap.agg(["size", "mean", "max"]).to_string(
            float_format=lambda x: f"{x:.4f}"))
        lo = 100.0 * nlad / max(int(C["rows"].sum()), 1)
        hi = 100.0 * (nlad + int(C["rows"].sum()) - ndec_r) / max(int(C["rows"].sum()), 1)
        say(f"RECORD-WIDE BOUND on the share of published regime-split rows that carry the "
            f"confound: {lo:.1f}% - {hi:.1f}%  (point estimate undefined over the undecidable "
            f"remainder; NOT reported as a point).")
    else:
        say("\nNo decidable cell yielded a comparable gross pair.")

    # ---------------------------------------------------------------- PART B
    say("\n" + "=" * 118)
    say("PART B — LIVE RE-QUOTE.  Every regime split priced against the full-gross control the")
    say("record publishes AND against two gross-matched statics.  All grid points reported.")
    say("=" * 118)
    grid, match, live, checked = [], [], [], False

    for pname in PANELS:
        px, names = M.panel(pname)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bars = M.bars_of(spy)
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1w = rules_v1_weights(px[names]).reindex(columns=px.columns).fillna(0.0)
        v2w = rules_v2_weights(px[names]).reindex(columns=px.columns).fillna(0.0)
        v1 = {c: backtest(px, v1w, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        v2 = {c: backtest(px, v2w, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        RG = {r: M.regime(px, names, r) for r in REGIMES}
        for c in COSTS:
            for lab, rr in (("RULES v1", v1[c]), ("RULES v2 (LIVE)", v2[c]), ("SPY", spy)):
                mm, mo = metrics(rr), metrics(rr.loc[OOS_START:])
                hh1, hh2 = M.halves(rr)
                live.append(dict(panel=pname, cost=c, book=lab, CAGR=mm["CAGR"],
                                 Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=hh1, H2=hh2,
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                 OOS_MaxDD=mo["MaxDD"]))
        say(f"\n--- panel {pname}: {len(names)} names, {px.index[0].date()} .. "
            f"{px.index[-1].date()}, SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} "
            f"MaxDD {ms['MaxDD']:.2%} (OOS Sharpe {mso['Sharpe']:.3f})")
        for r in REGIMES:
            a = RG[r].loc[start:]
            say(f"    regime {r:10s} armed {a.mean():.4f} of days "
                f"(IS {a.loc[:IS_END].mean():.4f} / OOS {a.loc[OOS_START:].mean():.4f})")

        TG = {}
        for book in BOOKS:
            for c in COSTS:
                cache = {}
                W_base, _, _ = base_and_gate(px, names, "gross50", book, TG)
                ctl = M.run_cond(px, W_base, bps=c)
                if not checked:                     # CHECK: run_cond with no instrument == engine
                    eng = backtest(px, W_base, cost_bps=c, freq=FREQ)["returns"]
                    say(f"\nCHECK (a) run_cond(no instrument) vs engine.backtest: max |diff| = "
                        f"{float((ctl['r'] - eng).abs().max()):.3e}")
                    checked = True
                for instr in INSTR:
                    Wb, Wg, kw = base_and_gate(px, names, instr, book, TG)
                    alw = M.run_cond(px, Wb, W_gate=Wg, bps=c, **kw)
                    for reg in REGIMES:
                        armed = RG[reg]
                        on = armed.astype(bool)
                        off = ~on
                        cond = M.run_cond(px, Wb, W_gate=Wg, armed=armed, bps=c, **kw)
                        g_full = float(cond["gross"].loc[start:].mean())
                        g_on = float(cond["gross"].loc[start:][on.loc[start:]].mean())
                        a_full = float(alw["gross"].loc[start:].mean())
                        a_on = float(alw["gross"].loc[start:][on.loc[start:]].mean())
                        muF, resF, gapF = solve_matched(px, Wb, g_full, c, cache)
                        muON, resON, gapON = solve_matched(px, Wb, g_on, c, cache)
                        muFA, resFA, gapFA = solve_matched(px, Wb, a_full, c, cache)
                        muONA, resONA, gapONA = solve_matched(px, Wb, a_on, c, cache)
                        match.append(dict(panel=pname, book=book, cost=c, instr=instr,
                                          regime=reg, target_full=g_full, mu_full=muF,
                                          gap_full=gapF, target_on=g_on, mu_on=muON,
                                          gap_on=gapON, target_full_always=a_full,
                                          mu_full_always=muFA, gap_full_always=gapFA,
                                          target_on_always=a_on, mu_on_always=muONA,
                                          gap_on_always=gapONA))
                        for tag, res in (("cond", cond), ("always", alw), ("control", ctl),
                                         ("matchedF", resF), ("matchedON", resON),
                                         ("matchedFA", resFA), ("matchedONA", resONA)):
                            st = rowstats(res["r"], res["to"], res["gross"], start,
                                          v2[c], bars, on, off)
                            grid.append(dict(panel=pname, book=book, cost=c, instr=instr,
                                             regime=reg, arm=tag, kind=SPEC[instr]["kind"],
                                             armed_frac=float(on.loc[start:].mean()),
                                             mu={"matchedF": muF, "matchedON": muON,
                                                 "matchedFA": muFA,
                                                 "matchedONA": muONA}.get(tag, np.nan),
                                             **st))
        say(f"    panel {pname}: {len(grid)} grid rows so far")

    G = pd.DataFrame(grid)
    ML = pd.DataFrame(match)
    LV = pd.DataFrame(live)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    ML.to_csv(OUT / f"{STEM}.match.csv", index=False)
    LV.to_csv(OUT / f"{STEM}.livebase.csv", index=False)
    say(f"\nCHECK (b) gross-match quality: max |achieved - target| full {ML.gap_full.max():.3e}, "
        f"ON {ML.gap_on.max():.3e} over {len(ML)} matches (tol {MATCH_TOL:.0e})")
    say("CHECK (c) OFF-regime gross of the conditional arm vs the control.  The instrument does")
    say("    not ACT off the regime, but the arm carries the holdings its armed days left it, so")
    say("    the two are close rather than identical; the residue is reported, never assumed:")
    key = ["panel", "book", "cost", "instr", "regime"]
    P = G.pivot_table(index=key, columns="arm",
                      values=["ann_on", "ann_off", "gross", "gross_on", "gross_off", "Sharpe",
                              "CAGR", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD",
                              "IS_ann_on", "OOS_ann_on", "IS_ann_off", "OOS_ann_off",
                              "turnover", "pass4a", "pass4b"])
    P.columns = [f"{a}_{b}" for a, b in P.columns]
    P = P.reset_index()
    P["kind"] = P.instr.map({i: SPEC[i]["kind"] for i in INSTR})
    say(f"    max |gross_off(cond) - gross_off(control)| = "
        f"{float((P.gross_off_cond - P.gross_off_control).abs().max()):.3e}")

    # ---- the restatement -------------------------------------------------------------
    # TWO published shapes, both restated.  `A` is the record's HEADLINE object: an ALWAYS-ON
    # instrument's delta split by regime (idea 246's "+12.6 pp/yr ON crash days" is this).
    # `C` is the REGIME-CONDITIONAL arm's delta (idea 249's object).  Both are published as
    # d_on/d_off against the same full-gross do-nothing control.
    SHAPES = {"A": ("always", "matchedFA", "matchedONA"), "C": ("cond", "matchedF", "matchedON")}
    for s, (armc, mf, mon) in SHAPES.items():
        P[f"d_on_{s}_ctl"] = P[f"ann_on_{armc}"] - P.ann_on_control      # as published
        P[f"d_off_{s}_ctl"] = P[f"ann_off_{armc}"] - P.ann_off_control
        P[f"d_on_{s}_MF"] = P[f"ann_on_{armc}"] - P[f"ann_on_{mf}"]      # idea 249's convention
        P[f"d_off_{s}_MF"] = P[f"ann_off_{armc}"] - P[f"ann_off_{mf}"]
        P[f"d_on_{s}_MON"] = P[f"ann_on_{armc}"] - P[f"ann_on_{mon}"]    # strict, PRIMARY
        P[f"d_off_{s}_MON"] = P[f"ann_off_{armc}"] - P[f"ann_off_{mon}"]
        P[f"gap_on_{s}"] = P.gross_on_control - P[f"gross_on_{armc}"]    # the confound, in NAV
        P[f"gap_full_{s}"] = P.gross_control - P[f"gross_{armc}"]
        for v in ("ctl", "MF", "MON"):
            P[f"shape_{s}_{v}"] = P[f"d_on_{s}_{v}"] > P[f"d_off_{s}_{v}"]   # "pays when armed"
        for v in ("MF", "MON"):
            P[f"surv_{s}_{v}"] = (
                (np.sign(P[f"d_on_{s}_{v}"]) == np.sign(P[f"d_on_{s}_ctl"]))
                & (P[f"d_on_{s}_{v}"].abs() >= SURVIVE_FRAC * P[f"d_on_{s}_ctl"].abs()))
        P[f"pub_pos_{s}"] = P[f"d_on_{s}_ctl"] > 0           # the claim the record actually makes
        P[f"big_{s}"] = P[f"d_on_{s}_ctl"].abs() >= 1.0      # publishable magnitude, pp/yr
    # back-compat aliases: the unsuffixed names refer to the conditional shape
    for c0 in ("d_on", "d_off", "gap_on", "gap_full"):
        P[c0] = P[f"{c0}_C"] if c0.startswith("gap") else P[f"{c0}_C_ctl"]
    P.to_csv(OUT / f"{STEM}.restated.csv", index=False)
    Q = P[P.cost == PROTO_COST]

    say("\n" + "-" * 118)
    say("THE CONFOUND, MEASURED.  Realised-gross gap between the arm and the full-gross control")
    say("it is published against (NAV; positive = the arm holds LESS).  A = always-on arm (the")
    say("record's headline shape), C = regime-conditional arm.")
    say("-" * 118)
    say(P.groupby(["kind", "regime"]).agg(
        n=("gap_on_A", "size"),
        gapON_A=("gap_on_A", "mean"), gapFULL_A=("gap_full_A", "mean"),
        gapON_C=("gap_on_C", "mean"), gapFULL_C=("gap_full_C", "mean"),
        pct_ge_bar_A=("gap_on_A", lambda s: 100.0 * (s.abs() >= GROSS_GAP_BAR).mean()),
        pct_ge_bar_C=("gap_on_C", lambda s: 100.0 * (s.abs() >= GROSS_GAP_BAR).mean()),
    ).to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n" + "-" * 118)
    say(f"H2 — SURVIVAL of the published d_on claim at {PROTO_COST:.0f} bps.  A claim survives")
    say(f"     iff sign is preserved AND |restated| >= {SURVIVE_FRAC:.2f} x |published|.")
    say("     Reported for both published shapes, and restricted to claims with a publishable")
    say("     magnitude (|d_on| >= 1.0 pp/yr) and to the POSITIVE claims the record makes.")
    say("-" * 118)
    for s, lab in (("A", "ALWAYS-ON arm split by regime (the record's headline shape)"),
                   ("C", "REGIME-CONDITIONAL arm split by regime")):
        say(f"\n  shape {s} — {lab}")
        S = Q.groupby(["kind", "regime"]).agg(
            n=(f"surv_{s}_MON", "size"),
            d_on_ctl=(f"d_on_{s}_ctl", "mean"), d_on_MF=(f"d_on_{s}_MF", "mean"),
            d_on_MON=(f"d_on_{s}_MON", "mean"),
            surv_MF=(f"surv_{s}_MF", lambda x: 100.0 * x.mean()),
            surv_MON=(f"surv_{s}_MON", lambda x: 100.0 * x.mean()))
        say(S.to_string(float_format=lambda x: f"{x:.3f}"))
        say(f"    POOLED over {len(Q)} cells: mean d_on vs control "
            f"{Q[f'd_on_{s}_ctl'].mean():+.3f} pp/yr -> vs matchedF "
            f"{Q[f'd_on_{s}_MF'].mean():+.3f} -> vs matchedON {Q[f'd_on_{s}_MON'].mean():+.3f}")
        say(f"    SURVIVAL: matchedF {100.0*Q[f'surv_{s}_MF'].mean():5.1f}% "
            f"({int(Q[f'surv_{s}_MF'].sum())}/{len(Q)}),  matchedON "
            f"{100.0*Q[f'surv_{s}_MON'].mean():5.1f}% ({int(Q[f'surv_{s}_MON'].sum())}/{len(Q)})")
        B = Q[Q[f"big_{s}"]]
        if len(B):
            say(f"    SURVIVAL restricted to |d_on| >= 1.0 pp/yr ({len(B)} cells): matchedF "
                f"{100.0*B[f'surv_{s}_MF'].mean():5.1f}%,  matchedON "
                f"{100.0*B[f'surv_{s}_MON'].mean():5.1f}%")
        PP = Q[Q[f"pub_pos_{s}"]]
        if len(PP):
            say(f"    THE POSITIVE CLAIMS ({len(PP)} of {len(Q)} cells have d_on > 0 vs the "
                f"control): still positive vs matchedF "
                f"{100.0*(PP[f'd_on_{s}_MF']>0).mean():5.1f}%,  vs matchedON "
                f"{100.0*(PP[f'd_on_{s}_MON']>0).mean():5.1f}%")
        for c in COSTS:
            Qc = P[P.cost == c]
            say(f"    cost {c:5.1f} bps: survival MF {100.0*Qc[f'surv_{s}_MF'].mean():5.1f}%  MON "
                f"{100.0*Qc[f'surv_{s}_MON'].mean():5.1f}%   mean d_on ctl "
                f"{Qc[f'd_on_{s}_ctl'].mean():+7.3f} -> MON {Qc[f'd_on_{s}_MON'].mean():+7.3f}")

    say("\n" + "-" * 118)
    say("H3 — the CLAIM SHAPE 'd_on > d_off' (the armed regime is the one it pays in).")
    say("-" * 118)
    for s in ("A", "C"):
        say(f"\n  shape {s}:")
        for c in COSTS:
            Qc = P[P.cost == c]
            say(f"    cost {c:5.1f} bps: holds vs control "
                f"{100.0*Qc[f'shape_{s}_ctl'].mean():5.1f}%,  vs matchedF "
                f"{100.0*Qc[f'shape_{s}_MF'].mean():5.1f}%,  vs matchedON "
                f"{100.0*Qc[f'shape_{s}_MON'].mean():5.1f}%   (ordering FLIPS on "
                f"{100.0*(Qc[f'shape_{s}_ctl'] != Qc[f'shape_{s}_MON']).mean():5.1f}% of cells)")
        say(Q.groupby("kind").agg(
            n=(f"shape_{s}_ctl", "size"),
            shape_ctl=(f"shape_{s}_ctl", lambda x: 100.0 * x.mean()),
            shape_MON=(f"shape_{s}_MON", lambda x: 100.0 * x.mean()),
            d_off_ctl=(f"d_off_{s}_ctl", "mean"),
            d_off_MON=(f"d_off_{s}_MON", "mean")).to_string(float_format=lambda x: f"{x:.2f}"))

    say("\n" + "-" * 118)
    say("H4 — is the RESTATED d_on distinguishable from zero?  Exact two-sided sign test.")
    say("-" * 118)
    rows = []
    for s in ("A", "C"):
        cols = [f"d_on_{s}_ctl", f"d_on_{s}_MF", f"d_on_{s}_MON"]
        for k, g in Q.groupby("kind"):
            for col in cols:
                p, kneg, n = signtest(g[col])
                rows.append(dict(shape=s, kind=k, stat=col, n=n, n_neg=kneg,
                                 frac_pos=(n - kneg) / max(n, 1), mean=g[col].mean(),
                                 median=g[col].median(), p=p))
        for col in cols:
            p, kneg, n = signtest(Q[col])
            rows.append(dict(shape=s, kind="POOLED", stat=col, n=n, n_neg=kneg,
                             frac_pos=(n - kneg) / max(n, 1), mean=Q[col].mean(),
                             median=Q[col].median(), p=p))
    ST = pd.DataFrame(rows)
    ST.to_csv(OUT / f"{STEM}.signtests.csv", index=False)
    say(ST.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n" + "-" * 118)
    say("EVERY GRID POINT at the PROTOCOL rung (10 bps), spy200, by panel x book x instrument.")
    say("A = always-on arm split by regime, C = regime-conditional arm.")
    say("-" * 118)
    show = ["panel", "book", "instr", "gross_always", "gross_on_always", "gross_on_control",
            "gap_on_A", "ann_on_always", "ann_on_control", "ann_on_matchedONA",
            "d_on_A_ctl", "d_on_A_MF", "d_on_A_MON", "d_off_A_ctl", "d_off_A_MON",
            "surv_A_MON", "d_on_C_ctl", "d_on_C_MON", "surv_C_MON"]
    say(Q[Q.regime == "spy200"][show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\nThe other two regimes, same rung (breadth20, hivol80):")
    say(Q[Q.regime != "spy200"][["regime"] + show].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- H5 KEEP paths ---------------------------------------------------------------
    say("\n" + "-" * 118)
    say("H5 — PROTOCOL KEEP paths on EVERY row (4a vs the LIVE RULES v2 on the same panel,")
    say("     4b vs SPY including the OOS leg).  Matched statics included so a pass they")
    say("     already have is never credited to the regime conditioning.")
    say("-" * 118)
    K = G.groupby(["arm", "cost"]).agg(n=("pass4a", "size"), p4a=("pass4a", "sum"),
                                       p4b=("pass4b", "sum")).reset_index()
    say(K.to_string(index=False))
    say(f"\nTOTAL over {len(G)} rows: 4a {int(G.pass4a.sum())}/{len(G)}, "
        f"4b {int(G.pass4b.sum())}/{len(G)}")
    cond4b = G[(G.arm == "cond") & G.pass4b & (G.cost == PROTO_COST)]
    say(f"4b passes at 10 bps among CONDITIONAL arms: {len(cond4b)}")
    if len(cond4b):
        # does the arm's own matched static already pass?  If so the pass is not the regime's.
        mk = G[(G.arm == "matchedON") & G.pass4b][key].apply(tuple, axis=1)
        mkset = set(mk)
        cond4b = cond4b.copy()
        cond4b["matchedON_also_passes"] = [tuple(t) in mkset
                                           for t in cond4b[key].apply(tuple, axis=1)]
        say(cond4b[key + ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR",
                          "gross", "matchedON_also_passes"]].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
        say(f"    of which the arm's OWN matched static ALSO passes 4b: "
            f"{int(cond4b.matchedON_also_passes.sum())}/{len(cond4b)}")
    say("\nLIVE COMPARANDS (RULES v1, the LIVE RULES v2, SPY) on every panel and rung:")
    say(LV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- RULE 8 ----------------------------------------------------------------------
    say("\n" + "=" * 118)
    say("RULE 8 WALK-FORWARD.  (INSTRUMENT, REGIME) chosen on 2009-2016 IS ALONE, 2017-2026 read")
    say("ONCE.  Two choosers: the PUBLISHED statistic (IS d_on vs the full-gross control) and the")
    say("RESTATED statistic (IS d_on vs the arm's own matched static).  Regret vs do-nothing.")
    say("=" * 118)
    for s, (armc, _mf, mon) in SHAPES.items():
        P[f"IS_d_on_{s}_ctl"] = P[f"IS_ann_on_{armc}"] - P.IS_ann_on_control
        P[f"OOS_d_on_{s}_ctl"] = P[f"OOS_ann_on_{armc}"] - P.OOS_ann_on_control
        P[f"IS_d_on_{s}_MON"] = P[f"IS_ann_on_{armc}"] - P[f"IS_ann_on_{mon}"]
        P[f"OOS_d_on_{s}_MON"] = P[f"OOS_ann_on_{armc}"] - P[f"OOS_ann_on_{mon}"]
    wf = []
    for (pn, bk, c), g in P.groupby(["panel", "book", "cost"]):
        for s, (armc, _mf, mon) in SHAPES.items():
            for chooser in ("published", "restated"):
                iscol = f"IS_d_on_{s}_{'ctl' if chooser == 'published' else 'MON'}"
                ooscol = f"OOS_d_on_{s}_{'ctl' if chooser == 'published' else 'MON'}"
                pick = g.loc[g[iscol].idxmax()]
                oracle = g[ooscol].max()
                wf.append(dict(panel=pn, book=bk, cost=c, shape=s, chooser=chooser,
                               pick_instr=pick.instr, pick_regime=pick.regime,
                               IS_stat=pick[iscol], OOS_stat_same=pick[ooscol],
                               OOS_d_on_restated=pick[f"OOS_d_on_{s}_MON"],
                               beats_donothing=bool(pick[ooscol] > 0),
                               regret_vs_oracle=float(oracle - pick[ooscol]),
                               OOS_CAGR=pick[f"OOS_CAGR_{armc}"],
                               OOS_Sharpe=pick[f"OOS_Sharpe_{armc}"],
                               OOS_MaxDD=pick[f"OOS_MaxDD_{armc}"],
                               OOS_CAGR_matchedON=pick[f"OOS_CAGR_{mon}"],
                               OOS_Sharpe_matchedON=pick[f"OOS_Sharpe_{mon}"],
                               OOS_CAGR_control=pick.OOS_CAGR_control,
                               OOS_Sharpe_control=pick.OOS_Sharpe_control,
                               pass4a=bool(pick[f"pass4a_{armc}"]),
                               pass4b=bool(pick[f"pass4b_{armc}"])))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for s in ("A", "C"):
        for ch in ("published", "restated"):
            w = W[(W.chooser == ch) & (W["shape"] == s)]
            say(f"\n  shape={s} chooser={ch:10s}: OOS statistic > 0 (beats do-nothing) in "
                f"{int(w.beats_donothing.sum())}/{len(w)} cells; median OOS statistic "
                f"{w.OOS_stat_same.median():+.4f} pp/yr; median regret vs the OOS oracle "
                f"{w.regret_vs_oracle.median():.4f}")
            say(f"                            of those picks, OOS d_on RESTATED > 0 in "
                f"{int((w.OOS_d_on_restated > 0).sum())}/{len(w)}; 4a "
                f"{int(w.pass4a.sum())}/{len(w)}, 4b {int(w.pass4b.sum())}/{len(w)}")
    say("\n  OOS LEVELS of the rule-8 selected book vs its own matched static, the do-nothing")
    say("  control, the LIVE RULES v2 baseline and SPY (PROTOCOL rung, 10 bps):")
    w10 = W[W.cost == PROTO_COST]
    for _, r in w10.iterrows():
        b = LV[(LV.panel == r.panel) & (LV.cost == PROTO_COST)].set_index("book")
        say(f"    {r.panel:6s} {r.book:6s} shape={r['shape']} chooser={r.chooser:9s} "
            f"pick={r.pick_instr}/"
            f"{r.pick_regime:10s}  OOS CAGR {r.OOS_CAGR:7.2%} Sharpe {r.OOS_Sharpe:6.3f} MaxDD "
            f"{r.OOS_MaxDD:7.2%} | matchedON {r.OOS_CAGR_matchedON:7.2%}/"
            f"{r.OOS_Sharpe_matchedON:6.3f} | control {r.OOS_CAGR_control:7.2%}/"
            f"{r.OOS_Sharpe_control:6.3f} | RULES v2 "
            f"{b.loc['RULES v2 (LIVE)','OOS_CAGR']:7.2%}/"
            f"{b.loc['RULES v2 (LIVE)','OOS_Sharpe']:6.3f} | SPY "
            f"{b.loc['SPY','OOS_CAGR']:7.2%}/{b.loc['SPY','OOS_Sharpe']:6.3f}")

    # ---------------------------------------------------------------- verdict
    say("\n" + "=" * 118)
    say("VERDICT")
    say("=" * 118)
    say(f"H1 census   : {ndec_f}/{len(C)} regime-split files and {ndec_r:,}/"
        f"{int(C['rows'].sum()):,} rows are gross-decidable from the committed file.")
    for s, lab in (("A", "always-on split (the record's headline shape)"),
                   ("C", "regime-conditional split")):
        PP = Q[Q[f"pub_pos_{s}"]]
        p_pool, kneg, n = signtest(Q[f"d_on_{s}_MON"])
        say(f"H2 shape {s}  : {100.0*Q[f'surv_{s}_MON'].mean():.1f}% survive at 10 bps "
            f"(matchedON), {100.0*Q[f'surv_{s}_MF'].mean():.1f}% under idea 249's full-sample "
            f"match; of the {len(PP)} POSITIVE published claims, "
            f"{100.0*(PP[f'd_on_{s}_MON']>0).mean() if len(PP) else float('nan'):.1f}% stay "
            f"positive.   [{lab}]")
        say(f"H3 shape {s}  : the 'pays in the armed regime' ordering flips on "
            f"{100.0*(Q[f'shape_{s}_ctl'] != Q[f'shape_{s}_MON']).mean():.1f}% of cells.")
        say(f"H4 shape {s}  : restated d_on pooled mean {Q[f'd_on_{s}_MON'].mean():+.4f} pp/yr, "
            f"median {Q[f'd_on_{s}_MON'].median():+.4f}, positive in {n-kneg}/{n}, sign p "
            f"{p_pool:.4f}.")
    say(f"H5 KEEP     : 4a {int(G.pass4a.sum())}/{len(G)}, 4b {int(G.pass4b.sum())}/{len(G)} "
        f"over every row; conditional 4b at 10 bps {len(cond4b)}.")
    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.{{census,censusgap,grid,match,restated,signtests,walkforward,livebase}}"
        f".csv and .log.txt")
    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
