#!/usr/bin/env python3
"""QUEUE idea 348 — is-the-U56-6W-m20-c*-of-104-bps-a-DRAWDOWN-CAP-artefact
    (research sprint, lane C, 2026-09-07)

QUESTION (pre-registered, from QUEUE.md idea 348)
    "idea 331's record breakeven fails first on the H1 bar, not on cost, meaning c* measures
     distance to a Sharpe bar rather than cost tolerance.  Recompute c* for every cell in the
     record's committed breakeven CSVs with the DD cap and CAGR floor removed, and report how
     much of the c* spread is cost tolerance versus bar slack.  If c* is mostly bar slack, the
     record's whole 'breakeven' column is mislabelled.  Max 2 params."

WHAT c* IS, STATED BEFORE IT IS MEASURED
    The record's breakeven is  c* = max{c : every 4b bar still holds at cost c}, scanned upward
    and stopped at the FIRST failure.  Because r(c) = r0 - turnover * c/1e4, every bar margin
    m_k(c) falls (near-)linearly in c, so per bar

        c*_k + 1 = slack_k / sens_k ,   slack_k = m_k(0),   sens_k = mean slope of m_k in bps

    and the published number is  c* = min_k c*_k.  So c* is a RATIO of two things: how much room
    a bar had at zero cost (SLACK, a property of the book's edge) and how fast cost eats that bar
    (SENSITIVITY, a property of turnover — the only part that is genuinely "cost tolerance").
    A c* column is correctly labelled "breakeven cost" only if its cross-cell SPREAD is driven by
    the sens term.  If the spread is driven by slack, the column is ranking edge, not cost.

HYPOTHESES, both falsifiable
    H-A ("DRAWDOWN-CAP artefact", the title):  the record's top breakeven, U56 6W m=20 c*=104,
        is set by the DD cap.  -> tested by the per-bar c*_k of that exact cell.
    H-B ("mislabelled column"):  across the record's committed breakeven cells the spread of
        log c* is mostly Var(log slack), not Var(log sens).

METHOD (no new book; nothing is tuned)
    The only two tuned parameters are idea 331's own: cadence x m.  This run does NOT search
    them — it re-prices the SAME 36 cells and re-reads their c*.  Two committed breakeven
    families are censused:
      A  2026-09-07_is-CADENCE-the-real-dial-behind-the-band_cloud.grid.csv  (36 cells, integer
         bps, 5 bars, "stop at first failure").  Re-run from idea 331's own committed module so
         the engine is identical by construction; gate = its committed breakeven_bps column.
      B  2026-09-05_cross-universe-breakeven-as-a-KEEP-bar_cloud.grid.csv.gz (64 cells, 0.5 bp
         rungs 0..30, committed per-bar margins).  c* is recomputed ARITHMETICALLY from those
         committed margins under each bar subset; gate = its committed `be` column.
    Bar subsets reported for every cell: FULL(5) / noDD(4) / noCAGR(4) / SHARPE-ONLY(3), plus
    the five single-bar c*_k.
    Rule 8 walk-forward: c* recomputed on 2009-2016 ONLY under each bar subset, the argmax cell
    picked per panel, evaluated untouched on 2017-2026 against RULES v2 and SPY.

OUTPUTS
    <slug>.familyA.csv       36 cells x {c*_k, subset c*, slack, sens, turnover}
    <slug>.familyB.csv       64 cells x {be under each subset, binding bar}
    <slug>.decomp.csv        the Var(log c*) decomposition, per panel and pooled
    <slug>.walkforward.csv   IS-chosen cell per (panel, subset) and its OOS numbers
    <slug>.keeppaths.csv     4a / 4b for all 36 cells at 0 / 10 / 25 bps
    <slug>.console.txt       everything printed
"""
import importlib.util, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                              # noqa
from engine import backtest, metrics                                              # noqa

SLUG = "2026-09-07_is-the-U56-6W-m20-cstar-of-104-bps-a-DRAWDOWN-CAP-artefact_C"
OUT = ROOT / "research" / "backtests"
SRC331 = OUT / "2026-09-07_is-CADENCE-the-real-dial-behind-the-band_cloud.py"
GRID331 = OUT / "2026-09-07_is-CADENCE-the-real-dial-behind-the-band_cloud.grid.csv"
GRID82 = OUT / "2026-09-05_cross-universe-breakeven-as-a-KEEP-bar_cloud.grid.csv.gz"
BE82 = OUT / "2026-09-05_cross-universe-breakeven-as-a-KEEP-bar_cloud.breakevens.csv"

# idea 331's committed script, imported as a module: identical book, identical backtester,
# identical bars_4b — this run re-uses them rather than re-implementing them.
_spec = importlib.util.spec_from_file_location("idea331", SRC331)
I331 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(I331)

CADENCES, MS, COSTS = I331.CADENCES, I331.MS, I331.COSTS
N, GROSS, WARMUP = I331.N, I331.GROSS, I331.WARMUP
IS_END, OOS_START, BASE_FREQ = I331.IS_END, I331.OOS_START, I331.BASE_FREQ
BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARS4_IS = ("H1", "H2", "DD", "CAGR")           # no OOS term inside the IS window
SUBSETS = {"FULL": BARS5, "noDD": ("H1", "H2", "OOS", "CAGR"),
           "noCAGR": ("H1", "H2", "OOS", "DD"), "SHARPEONLY": ("H1", "H2", "OOS")}
SUBSETS_IS = {"FULL": BARS4_IS, "noDD": ("H1", "H2", "CAGR"),
              "noCAGR": ("H1", "H2", "DD"), "SHARPEONLY": ("H1", "H2")}
HI = 1000                                        # bps ceiling for the scan; censoring reported
PHI, DELTA = 0.70, 0.60                          # 4b's CAGR floor and DD cap coefficients

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


# ---------------------------------------------------------------- vectorised 4b bars
def _sharpe(X):
    mu = X.mean(axis=1) * 252
    sd = X.std(axis=1, ddof=1) * np.sqrt(252)
    return np.where(sd > 0, mu / sd, np.nan)


def _cagr_dd(X):
    eq = np.cumprod(1.0 + X, axis=1)
    cagr = eq[:, -1] ** (252.0 / X.shape[1]) - 1.0
    dd = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
    return cagr, dd


def spy_ref(spy):
    """SPY's side of the five bars (constant in cost)."""
    S = spy.values[None, :]
    h = S.shape[1] // 2
    o = int(np.searchsorted(spy.index.values, np.datetime64(OOS_START)))
    c, d = _cagr_dd(S)
    return dict(s1=_sharpe(S[:, :h])[0], s2=_sharpe(S[:, h:])[0], soos=_sharpe(S[:, o:])[0],
                cagr=c[0], dd=d[0], h=h, o=o)


def margins_matrix(r0, t0, ref, cs):
    """m_k(c) for k in BARS5 and every c in cs, in one numpy pass.  Same arithmetic as
    idea331.bars_4b — asserted equal to it in [0]."""
    R = r0.values[None, :] - np.asarray(cs, float)[:, None] * t0.values[None, :] / 1e4
    h, o = ref["h"], ref["o"]
    cagr, dd = _cagr_dd(R)
    return {"H1": _sharpe(R[:, :h]) - ref["s1"], "H2": _sharpe(R[:, h:]) - ref["s2"],
            "OOS": _sharpe(R[:, o:]) - ref["soos"],
            "DD": DELTA * abs(ref["dd"]) - np.abs(dd), "CAGR": cagr - PHI * ref["cagr"]}


def margins_matrix_win(r0, t0, ref, cs):
    """The IS-window form: halves of the window, no OOS term (rule-8 chooser)."""
    R = r0.values[None, :] - np.asarray(cs, float)[:, None] * t0.values[None, :] / 1e4
    h = ref["h"]
    cagr, dd = _cagr_dd(R)
    return {"H1": _sharpe(R[:, :h]) - ref["s1"], "H2": _sharpe(R[:, h:]) - ref["s2"],
            "DD": DELTA * abs(ref["dd"]) - np.abs(dd), "CAGR": cagr - PHI * ref["cagr"]}


def spy_ref_win(spy):
    S = spy.values[None, :]
    h = S.shape[1] // 2
    c, d = _cagr_dd(S)
    return dict(s1=_sharpe(S[:, :h])[0], s2=_sharpe(S[:, h:])[0], cagr=c[0], dd=d[0], h=h)


def per_bar_cstar(M, keys):
    """c*_k = (first integer cost at which bar k is < 0) - 1, on the scan 0..HI.
    -1 = fails already at 0 bps.  HI = censored (never failed inside the scan)."""
    out, cens = {}, {}
    for k in keys:
        v = np.asarray(M[k])
        bad = np.flatnonzero(v < 0)
        if bad.size == 0:
            out[k], cens[k] = HI, True
        else:
            out[k], cens[k] = int(bad[0]) - 1, False
    return out, cens


# ---------------------------------------------------------------- family A
def family_A():
    say("\n" + "=" * 100)
    say("[A] FAMILY A — idea 331's 36 committed breakeven cells, re-run and decomposed")
    say("=" * 100)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": I331.small_panel()}
    committed = pd.read_csv(GRID331)
    cs = np.arange(0, HI + 1)
    rows, keeprows = [], []
    gate_be, gate_m = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ref = spy_ref(spy)
        rk, _ = I331.rank_frame(px, drop_spy=(pname == "SMALL439"))
        br, bt, _, _ = I331.fast_backtest(px, rules_v2_weights(px), 0.0, BASE_FREQ)
        br, bt = br.loc[start:], bt.loc[start:]
        ms = metrics(spy); so = metrics(spy.loc[OOS_START:])
        say(f"\n  ---- {pname}: {px.shape[1]-1} names + SPY, eval from {start.date()} "
            f"({len(spy)} days)")
        say(f"       SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%} MaxDD {so['MaxDD']:.2%}")
        say(f"       4b bar levels: H1>{ref['s1']:.3f} H2>{ref['s2']:.3f} OOS>{ref['soos']:.3f} "
            f"|MaxDD|<{DELTA*abs(ref['dd']):.2%} CAGR>{PHI*ref['cagr']:.2%}")

        # IS-window references (rule 8 chooser)
        spy_is = spy.loc[:IS_END]
        ref_is = spy_ref_win(spy_is)
        ref_oos = spy_ref_win(spy.loc[OOS_START:])
        n_is = len(spy_is)

        say(f"\n       {'cad':>4} {'m':>3} {'turn/yr':>8} | "
            + " ".join(f"{'c*'+k:>8}" for k in BARS5)
            + " | " + " ".join(f"{s:>10}" for s in SUBSETS) + " | binding  committed")
        for fq in CADENCES:
            for m in MS:
                sel = I331.sel_hard(rk, N) if m == 0 else I331.sel_band(px, rk, N, m, fq)
                r0, t0, gr, kk = I331.fast_backtest(px, I331.weights_from(sel), 0.0, fq)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                M = margins_matrix(r0, t0, ref, cs)
                cst, cens = per_bar_cstar(M, BARS5)
                subs = {s: min(cst[k] for k in ks) for s, ks in SUBSETS.items()}
                binding = ",".join(k for k in BARS5 if cst[k] == subs["FULL"])
                cm = committed[(committed.panel == pname) & (committed.cadence == fq)
                               & (committed.m == m)].iloc[0]
                gate_be.append((pname, fq, m, subs["FULL"], int(cm.breakeven_bps)))
                for k in BARS5:
                    gate_m.append(abs(M[k][0] - cm[f"m4b_{k}_0"]))
                    gate_m.append(abs(M[k][10] - cm[f"m4b_{k}_10"]))
                    gate_m.append(abs(M[k][25] - cm[f"m4b_{k}_25"]))

                rec = dict(panel=pname, cadence=fq, m=m, turn_per_yr=tpy,
                           names=kk.loc[start:].mean(), committed_cstar=int(cm.breakeven_bps),
                           committed_first_fail=cm.breakeven_first_fail, binding_bar=binding)
                for k in BARS5:
                    rec[f"cstar_{k}"] = cst[k]
                    rec[f"censored_{k}"] = cens[k]
                    rec[f"slack_{k}"] = float(M[k][0])
                    # continuous breakeven: linear root of m_k between the last passing rung and
                    # the first failing one.  sens = slack / croot is then the AVERAGE rate at
                    # which one bp of cost consumes the bar, and log croot = log slack - log sens
                    # holds exactly (no integer-rung residual).
                    if cst[k] < 0:
                        rec[f"croot_{k}"], rec[f"sens_{k}"] = np.nan, np.nan
                    elif cens[k]:
                        rec[f"croot_{k}"] = float(HI)
                        rec[f"sens_{k}"] = float(M[k][0] / HI)
                    else:
                        a, b_ = float(M[k][cst[k]]), float(M[k][cst[k] + 1])
                        root = cst[k] + a / (a - b_)
                        rec[f"croot_{k}"] = root
                        rec[f"sens_{k}"] = float(M[k][0]) / root if root > 0 else np.nan
                    rec[f"sens1_{k}"] = float(M[k][0] - M[k][1])     # local slope at 0, per bp
                for s, ks in SUBSETS.items():
                    rec[f"cstar_{s}"] = subs[s]
                    roots = {k: rec[f"croot_{k}"] for k in ks}
                    if subs[s] < 0:
                        rec[f"croot_{s}"], rec[f"binding_{s}"] = np.nan, \
                            ",".join(k for k in ks if cst[k] == subs[s])
                    else:
                        rec[f"croot_{s}"] = min(roots.values())
                        rec[f"binding_{s}"] = ",".join(k for k in ks
                                                       if roots[k] == rec[f"croot_{s}"])
                rows.append(rec)

                # -------- rule-8 IS chooser inputs: c* measured on 2009-2016 ONLY
                r_is, t_is = r0.loc[:IS_END], t0.loc[:IS_END]
                assert len(r_is) == n_is
                Mi = margins_matrix_win(r_is, t_is, ref_is, cs)
                cst_is, _ = per_bar_cstar(Mi, BARS4_IS)
                r_oo, t_oo = r0.loc[OOS_START:], t0.loc[OOS_START:]
                Mo = margins_matrix_win(r_oo, t_oo, ref_oos, cs)
                cst_oo, _ = per_bar_cstar(Mo, BARS4_IS)
                for s, ks in SUBSETS_IS.items():
                    rows[-1][f"IScstar_{s}"] = min(cst_is[k] for k in ks)
                    rows[-1][f"OOScstar_{s}"] = min(cst_oo[k] for k in ks)

                # -------- both KEEP paths at the three published rungs
                krec = dict(panel=pname, cadence=fq, m=m, turn_per_yr=tpy)
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    basec = (br - bt * c / 1e4)
                    ok4b, d4b, f4b = I331.bars_4b(r, spy)
                    ok4a, d4a, f4a = I331.bars_4a(r, basec)
                    mt = metrics(r); h1, h2 = I331.hs(r); oo = metrics(r.loc[OOS_START:])
                    krec.update({f"CAGR_{c}": mt["CAGR"], f"Sharpe_{c}": mt["Sharpe"],
                                 f"MaxDD_{c}": mt["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                                 f"OOS_Sharpe_{c}": oo["Sharpe"], f"OOS_CAGR_{c}": oo["CAGR"],
                                 f"OOS_MaxDD_{c}": oo["MaxDD"],
                                 f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                 f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a)})
                keeprows.append(krec)

                say(f"       {fq:>4} {m:>3} {tpy:>8.2f} | "
                    + " ".join(f"{cst[k]:>8}" for k in BARS5) + " | "
                    + " ".join(f"{subs[s]:>10}" for s in SUBSETS)
                    + f" | {binding:<9} {int(cm.breakeven_bps):>4}")
        say(f"       (c* = -1 the bar already fails at 0 bps; {HI} = censored at the scan ceiling)")

    A = pd.DataFrame(rows); K = pd.DataFrame(keeprows)

    say("\n  [0] REPRODUCTION GATES (idea 331 is reproduced, not re-derived)")
    bad = [g for g in gate_be if g[3] != g[4]]
    say(f"      c*_FULL vs committed breakeven_bps, all 36 cells: {len(gate_be)-len(bad)}/{len(gate_be)} exact"
        + ("" if not bad else f"  MISMATCHES {bad}"))
    assert not bad
    say(f"      margins m_k(c) vs committed m4b_* at c=0/10/25, {len(gate_m)} values: "
        f"max|d| {max(gate_m):.3e}")
    assert max(gate_m) < 1e-12
    ff = A[A.committed_cstar >= 0]
    agree = int((ff.binding_bar == ff.committed_first_fail).sum())
    say(f"      binding bar at c*+1 vs committed breakeven_first_fail: {agree}/{len(ff)} agree")
    kk = K.merge(pd.read_csv(GRID331), on=["panel", "cadence", "m"], suffixes=("", "_c"))
    dmax = max(abs(kk[f"{col}_{c}"] - kk[f"{col}_{c}_c"]).max()
               for c in COSTS for col in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"))
    say(f"      full 4a/4b metric block vs committed grid, {6*len(COSTS)} columns: max|d| {dmax:.3e}")
    assert dmax < 1e-12
    n4b = {c: int(kk[f"keep4b_{c}"].sum()) for c in COSTS}
    n4a = {c: int(kk[f"keep4a_{c}"].sum()) for c in COSTS}
    say(f"      KEEP paths reproduced: 4b {n4b} of 36, 4a {n4a} of 36 "
        f"(idea 331 published 8/6/4 and 0/0/0)")
    return A, K


# ---------------------------------------------------------------- family B
def family_B():
    say("\n" + "=" * 100)
    say("[B] FAMILY B — idea 82's 64 committed breakeven cells, recomputed from its own margins")
    say("=" * 100)
    F = pd.read_csv(GRID82)
    BE = pd.read_csv(BE82)
    say(f"      committed grid {F.shape[0]} rows x {F.shape[1]} cols, "
        f"{F.cost.nunique()} cost rungs {F.cost.min()}..{F.cost.max()} bps")

    # idea 82's own convention: strict '> 0', and be = the LARGEST passing rung (not first-fail)
    ok = {"H1": F.full_H1 - F.full_b_s1 > 0, "H2": F.full_H2 - F.full_b_s2 > 0,
          "OOS": F.full_OOSs - F.full_b_soos > 0,
          "DD": DELTA * F.full_b_sdd.abs() - F.full_MaxDD.abs() > 0,
          "CAGR": F.full_CAGR - PHI * F.full_b_scagr > 0}
    OK = pd.DataFrame(ok)
    key = F[["panel", "book", "arm", "cost"]].copy()
    rows = []
    for (p, b, a), idx in key.groupby(["panel", "book", "arm"], sort=False).groups.items():
        d = key.loc[idx].sort_values("cost"); o = OK.loc[d.index]
        rec = dict(panel=p, book=b, arm=a)
        for s, ks in SUBSETS.items():
            passes = o[list(ks)].all(axis=1).values
            rec[f"be_{s}"] = float(d.cost.values[np.flatnonzero(passes).max()]) if passes.any() else np.nan
            rec[f"censored_{s}"] = bool(passes.any() and passes[-1])
        # which bar is first to fail above be_FULL
        passes = o[list(BARS5)].all(axis=1).values
        if passes.any() and not passes[-1]:
            j = np.flatnonzero(passes).max() + 1
            rec["binding_bar"] = ",".join(k for k in BARS5 if not o[k].values[j])
        else:
            rec["binding_bar"] = "" if passes.any() else "fails at 0"
        for k in BARS5:                                   # single-bar breakevens
            pk = o[k].values
            rec[f"be_{k}"] = float(d.cost.values[np.flatnonzero(pk).max()]) if pk.any() else np.nan
        i0 = d.index[0]
        rec["slack_H1"] = float(F.full_H1[i0] - F.full_b_s1[i0])
        rec["slack_H2"] = float(F.full_H2[i0] - F.full_b_s2[i0])
        rec["slack_OOS"] = float(F.full_OOSs[i0] - F.full_b_soos[i0])
        rec["slack_DD"] = float(DELTA * abs(F.full_b_sdd[i0]) - abs(F.full_MaxDD[i0]))
        rec["slack_CAGR"] = float(F.full_CAGR[i0] - PHI * F.full_b_scagr[i0])
        rows.append(rec)
    B = pd.DataFrame(rows)
    m = B.merge(BE[["panel", "book", "arm", "be"]], on=["panel", "book", "arm"], how="left")
    same = ((m.be_FULL.isna() & m.be.isna()) | (m.be_FULL == m.be)).sum()
    say(f"      GATE  be_FULL vs idea 82's committed `be` column: {same}/{len(m)} exact")
    assert same == len(m)
    live = B[B.be_FULL.notna()]
    say(f"      {len(live)} of {len(B)} cells pass 4b at 0 bps and therefore have a breakeven")
    say(f"      of those, censored at the 30 bps grid ceiling: {int(live.censored_FULL.sum())}")
    for s in SUBSETS:
        moved = int((live[f"be_{s}"].fillna(-1) != live.be_FULL.fillna(-1)).sum())
        say(f"      subset {s:<11}: median be {live[f'be_{s}'].median():>6.2f} bps, "
            f"cells whose be MOVES vs FULL: {moved}/{len(live)}")
    say("\n      binding bar just above be (idea 82 family):")
    say("        " + str(live.binding_bar.value_counts().to_dict()))
    return B


# ---------------------------------------------------------------- decomposition
def _decomp_one(A, sub, rows):
    """Decomposition for one bar subset's c* column.  Returns the live frame."""
    cc, bb = f"croot_{sub}", f"binding_{sub}"
    live = A[A[f"cstar_{sub}"] >= 0].copy()
    say(f"\n  ---- target: c*_{sub}   ({len(live)} of {len(A)} cells have a breakeven under it)")
    if len(live) < 3:
        say("      too few cells to decompose"); return live
    b = live[bb].str.split(",").str[0]
    live["slack_b"] = [r[f"slack_{k}"] for r, k in zip(live.to_dict("records"), b)]
    live["sens_b"] = [r[f"sens_{k}"] for r, k in zip(live.to_dict("records"), b)]
    live["ls"], live["lz"] = np.log(live.slack_b), np.log(live.sens_b)
    live["lc"] = np.log(live[cc])
    ident = float(np.abs(live.lc - (live.ls - live.lz)).max())
    lin = float(np.abs(live.sens_b / [r[f"sens1_{k}"] for r, k in
                                      zip(live.to_dict("records"), b)] - 1).median())
    say(f"      identity residual max|log croot - (log slack - log sens)| = {ident:.2e} "
        f"(exact by construction); median |avg sens / local sens at 0 - 1| = {lin:.1%} "
        f"(linearity of the bar in cost)")
    for label, d in [("pooled", live)] + [(p, g) for p, g in live.groupby("panel")]:
        if len(d) < 3:
            say(f"      {label:<9} n={len(d)} — skipped (n<3)"); continue
        vs, vz = d.ls.var(ddof=1), d.lz.var(ddof=1)
        cov = d.ls.cov(d.lz); vc = d.lc.var(ddof=1)
        sl = np.polyfit(np.log(d.turn_per_yr), d.lc, 1)
        r2 = float(np.corrcoef(np.log(d.turn_per_yr), d.lc)[0, 1] ** 2)
        rows.append(dict(subset=sub, scope=label, n=len(d), var_logc=vc, var_logslack=vs,
                         var_logsens=vz, cov=cov, share_slack=vs / vc, share_sens=vz / vc,
                         share_cov=-2 * cov / vc,
                         spearman_c_slack=float(d.lc.rank().corr(d.ls.rank())),
                         spearman_c_sens=float(d.lc.rank().corr(d.lz.rank())),
                         spearman_c_turnover=float(d.lc.rank().corr(d.turn_per_yr.rank())),
                         spearman_slack_turnover=float(d.ls.rank().corr(d.turn_per_yr.rank())),
                         loglog_slope_vs_turnover=float(sl[0]), loglog_r2=r2))
        r = rows[-1]
        say(f"      {label:<9} n={r['n']:>2}  Var(log c*) {vc:.4f} = slack {vs:.4f} ({vs/vc:+.0%})"
            f" + sens {vz:.4f} ({vz/vc:+.0%}) - 2cov {-2*cov:+.4f} ({-2*cov/vc:+.0%})")
        say(f"                 spearman(log c*, log slack) {r['spearman_c_slack']:+.3f} | "
            f"(log c*, log sens) {r['spearman_c_sens']:+.3f} | "
            f"(log c*, turnover) {r['spearman_c_turnover']:+.3f} | "
            f"log-log slope on turnover {r['loglog_slope_vs_turnover']:+.3f} (R2 {r2:.3f})")
    med_s, med_z = live.slack_b.median(), live.sens_b.median()
    cf_slack, cf_sens = live.slack_b / med_z, med_s / live.sens_b
    say(f"      counterfactual IQR of c* (bps): actual "
        f"{live[cc].quantile(.25):.1f}..{live[cc].quantile(.75):.1f} "
        f"({live[cc].quantile(.75)/max(live[cc].quantile(.25),1e-9):.2f}x) | "
        f"slack varies only {cf_slack.quantile(.25):.1f}..{cf_slack.quantile(.75):.1f} "
        f"({cf_slack.quantile(.75)/cf_slack.quantile(.25):.2f}x) | "
        f"sens varies only {cf_sens.quantile(.25):.1f}..{cf_sens.quantile(.75):.1f} "
        f"({cf_sens.quantile(.75)/cf_sens.quantile(.25):.2f}x)")
    return live


def decompose(A):
    say("\n" + "=" * 100)
    say("[C] IS c* COST TOLERANCE OR BAR SLACK?  Var(log c*) decomposition")
    say("=" * 100)
    say("      Per cell, for the binding bar b:  c*+1 ~ slack_b / sens_b,  so")
    say("          log(c*+1) = log slack_b - log sens_b")
    say("      => Var(log c*) = Var(log slack) + Var(log sens) - 2 Cov(log slack, log sens).")
    say("      SLACK = the book's edge over the 4b bar at zero cost (NOT a cost quantity).")
    say("      SENS  = how fast cost eats that bar; it is the turnover term, i.e. the only")
    say("              genuine 'cost tolerance' in c*.  A correctly labelled breakeven column")
    say("              has its cross-cell spread driven by SENS, and ranks cells by turnover.")
    say("      Reported on two targets: the published c*_FULL (n is small because the DD cap")
    say("      censors 28 of 36 cells at 0 bps) and c*_noDD, which restores 13 of them.")
    rows = []
    live = _decomp_one(A, "FULL", rows)
    _decomp_one(A, "noDD", rows)
    return pd.DataFrame(rows), live


# ---------------------------------------------------------------- the title question
def title_question(A):
    say("\n" + "=" * 100)
    say("[D] H-A: is the record's top breakeven (U56 6W m=20, c*=104) a DRAWDOWN-CAP artefact?")
    say("=" * 100)
    r = A[(A.panel == "U56") & (A.cadence == "6W") & (A.m == 20)].iloc[0]
    say(f"      committed c* = {int(r.committed_cstar)} bps, committed first fail = "
        f"{r.committed_first_fail}; reproduced c* = {int(r.cstar_FULL)}")
    say(f"      {'bar':<6} {'slack@0':>10} {'sens/bp':>11} {'c*_k (bps)':>11} {'exact root':>11}")
    for k in BARS5:
        say(f"      {k:<6} {r[f'slack_{k}']:>10.4f} {r[f'sens_{k}']:>11.6f} "
            f"{int(r[f'cstar_{k}']):>11} {r[f'croot_{k}']:>11.2f}")
    say(f"      subset c*: " + "  ".join(f"{s}={int(r[f'cstar_{s}'])}" for s in SUBSETS))
    dd_rank = sorted([(int(r[f"cstar_{k}"]), k) for k in BARS5])
    say(f"      order of failure as cost rises: " + " < ".join(f"{k}({c})" for c, k in dd_rank))
    say(f"      => the DD cap binds at {int(r['cstar_DD'])} bps vs the binding bar at "
        f"{int(r.cstar_FULL)} bps; removing the DD cap moves c* to {int(r['cstar_noDD'])} bps "
        f"({int(r['cstar_noDD']) - int(r.cstar_FULL):+d}).")
    say("\n      the same question for every cell that HAS a breakeven:")
    live = A[A.cstar_FULL >= 0]
    for s in SUBSETS:
        moved = int((live[f"cstar_{s}"] != live.cstar_FULL).sum())
        say(f"        drop to {s:<11}: c* moves on {moved}/{len(live)} cells, "
            f"median c* {live[f'cstar_{s}'].median():>7.1f} vs FULL {live.cstar_FULL.median():.1f}")
    say(f"      binding-bar census over the {len(live)} cells with a breakeven: "
        f"{live.binding_bar.value_counts().to_dict()}")
    say(f"      DD is the binding bar at c* in {int(live.binding_bar.str.contains('DD').sum())} "
        f"of {len(live)} cells; DD kills at 0 bps in "
        f"{int((A.cstar_DD < 0).sum())} of {len(A)} cells overall.")
    cens = A[(A.cstar_FULL < 0) & (A.cstar_noDD >= 0)]
    say(f"\n      WHAT THE DD CAP ACTUALLY DOES: it CENSORS the column rather than setting it.")
    say(f"      {len(cens)} of the {int((A.cstar_FULL < 0).sum())} cells with NO published "
        f"breakeven have one as soon as the cap is dropped:")
    for _, r in cens.iterrows():
        say(f"        {r.panel:<9} {r.cadence:>2} m={int(r.m):<2} turn {r.turn_per_yr:>5.2f}/yr  "
            f"c*_noDD {int(r.cstar_noDD):>4} bps (binding {r.binding_noDD}), DD margin at 0 bps "
            f"{r.slack_DD:+.4f}")
    say(f"      so the c* column's HOLES are the DD cap's; its VALUES are the Sharpe bars'.")


# ---------------------------------------------------------------- rule 8
def walk_forward(A, K):
    say("\n" + "=" * 100)
    say("[E] RULE 8 WALK-FORWARD — c* chosen on 2009-2016 only, judged on 2017-2026 untouched")
    say("=" * 100)
    say("      chooser: per panel take the cell with the highest IS c* under each bar subset")
    say("      (ties -> lowest turnover, deterministic).  Then read its OOS numbers at 10 bps.")
    rows = []
    for pname, g in A.groupby("panel"):
        kk = K[K.panel == pname]
        for s in SUBSETS_IS:
            col = f"IScstar_{s}"
            gg = g.sort_values([col, "turn_per_yr"], ascending=[False, True])
            pick = gg.iloc[0]
            kr = kk[(kk.cadence == pick.cadence) & (kk.m == pick.m)].iloc[0]
            rows.append(dict(panel=pname, subset=s, pick=f"{pick.cadence} m={int(pick.m)}",
                             IS_cstar=int(pick[col]), full_cstar=int(pick.cstar_FULL),
                             OOS_CAGR=kr["OOS_CAGR_10"], OOS_Sharpe=kr["OOS_Sharpe_10"],
                             OOS_MaxDD=kr["OOS_MaxDD_10"], keep4b_10=kr["keep4b_10"],
                             keep4a_10=kr["keep4a_10"], turn=pick.turn_per_yr))
    W = pd.DataFrame(rows)
    # comparands
    ctx = pd.read_csv(OUT / "2026-09-07_is-CADENCE-the-real-dial-behind-the-band_cloud.ctx.csv").set_index("panel")
    say(f"\n      {'panel':<9} {'subset':<11} {'pick':<9} {'ISc*':>5} {'c*':>5} {'turn':>6} "
        f"{'OOS CAGR':>9} {'OOS Shrp':>9} {'OOS MaxDD':>10}  4b  4a")
    for _, r in W.iterrows():
        say(f"      {r.panel:<9} {r.subset:<11} {r['pick']:<9} {r.IS_cstar:>5} {r.full_cstar:>5} "
            f"{r.turn:>6.2f} {r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>9.3f} {r.OOS_MaxDD:>10.2%}  "
            f"{'Y' if r.keep4b_10 else 'n'}   {'Y' if r.keep4a_10 else 'n'}")
    say("")
    for p in W.panel.unique():
        c = ctx.loc[p]
        say(f"      {p:<9} comparands OOS: SPY Sharpe {c.spy_oos_sharpe:.3f} CAGR {c.spy_oos_cagr:.2%} "
            f"MaxDD {c.spy_oos_dd:.2%} | RULES v2 Sharpe {c.base_oos_sharpe:.3f} "
            f"CAGR {c.base_oos_cagr:.2%} MaxDD {c.base_oos_dd:.2%}")
    for p, g in W.groupby("panel"):
        picks = g["pick"].unique()
        say(f"      {p:<9}: the four bar subsets pick {len(picks)} distinct cell(s): {list(picks)}")
    say("\n      does the c* COLUMN itself survive out of sample?  spearman(IS c*, OOS c*) over")
    say("      the 12 cells of each panel (-1 = no breakeven, ranked lowest):")
    for p, g in A.groupby("panel"):
        for s in ("FULL", "noDD"):
            both = g[(g[f"IScstar_{s}"] >= 0) & (g[f"OOScstar_{s}"] >= 0)]
            rho = float(g[f"IScstar_{s}"].rank().corr(g[f"OOScstar_{s}"].rank()))
            rho2 = (float(both[f"IScstar_{s}"].rank().corr(both[f"OOScstar_{s}"].rank()))
                    if len(both) >= 3 else float("nan"))
            say(f"        {p:<9} {s:<6} all 12 cells rho {rho:+.3f} | both-defined n={len(both):>2} "
                f"rho {rho2:+.3f} | median IS c* {g[f'IScstar_{s}'].median():>6.1f} "
                f"vs OOS c* {g[f'OOScstar_{s}'].median():>6.1f} bps")
    beat_spy = sum(1 for _, r in W.iterrows() if r.OOS_Sharpe > ctx.loc[r.panel].spy_oos_sharpe)
    beat_base = sum(1 for _, r in W.iterrows() if r.OOS_Sharpe > ctx.loc[r.panel].base_oos_sharpe)
    say(f"      of the {len(W)} (panel, subset) picks: OOS Sharpe > SPY in {beat_spy}, "
        f"> RULES v2 in {beat_base}")
    return W


# ---------------------------------------------------------------- keep paths
def keep_paths(K):
    say("\n" + "=" * 100)
    say("[F] BOTH KEEP PATHS — all 36 cells at 0 / 10 / 25 bps (this run adds no new book)")
    say("=" * 100)
    for c in COSTS:
        say(f"      {c:>2} bps: 4b {int(K[f'keep4b_{c}'].sum())}/36   4a {int(K[f'keep4a_{c}'].sum())}/36")
    p = K[K["keep4b_10"]]
    say(f"      the {len(p)} cells passing 4b at 10 bps:")
    for _, r in p.iterrows():
        say(f"        {r.panel:<9} {r.cadence:>2} m={int(r.m):<2} CAGR {r['CAGR_10']:>7.2%} "
            f"Sharpe {r['Sharpe_10']:.3f} MaxDD {r['MaxDD_10']:>7.2%} "
            f"H1/H2 {r['H1_10']:.3f}/{r['H2_10']:.3f} OOS {r['OOS_Sharpe_10']:.3f}")
    say("      4a passes at any rung: "
        f"{sum(int(K[f'keep4a_{c}'].sum()) for c in COSTS)} of {3*len(K)} cell-rungs")
    say("      NOTE: no cell here is new — every one is idea 331's, reproduced exactly.  This run")
    say("      re-prices the c* COLUMN, not the book, so it proposes no KEEP of its own.")


def main():
    say(f"=== {SLUG}")
    say("QUEUE idea 348.  Tuned parameters: idea 331's own cadence x m (2), NOT re-searched.")
    say(f"Cost scan 0..{HI} bps, integer rungs; 4b coefficients phi={PHI} (CAGR) delta={DELTA} (DD).")
    A, K = family_A()
    B = family_B()
    D, live = decompose(A)
    title_question(A)
    W = walk_forward(A, K)
    keep_paths(K)

    A.to_csv(OUT / f"{SLUG}.familyA.csv", index=False)
    B.to_csv(OUT / f"{SLUG}.familyB.csv", index=False)
    D.to_csv(OUT / f"{SLUG}.decomp.csv", index=False)
    W.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    K.to_csv(OUT / f"{SLUG}.keeppaths.csv", index=False)

    say("\n" + "=" * 100)
    say("[G] VERDICT")
    say("=" * 100)
    liveA = A[A.cstar_FULL >= 0]
    ddbind = int(liveA.binding_bar.str.contains("DD").sum())
    moved_noDD = int((liveA.cstar_noDD != liveA.cstar_FULL).sum())
    moved_noCAGR = int((liveA.cstar_noCAGR != liveA.cstar_FULL).sum())
    say(f"      H-A (DD-cap artefact): DD binds at c* in {ddbind}/{len(liveA)} family-A cells; "
        f"dropping the cap moves c* on {moved_noDD}/{len(liveA)}.")
    say(f"      dropping the CAGR floor moves c* on {moved_noCAGR}/{len(liveA)}.")
    say(f"      the DD cap instead CENSORS: {int(((A.cstar_FULL < 0) & (A.cstar_noDD >= 0)).sum())} "
        f"of {int((A.cstar_FULL < 0).sum())} cells with no published c* acquire one without it.")
    for sub in ("FULL", "noDD"):
        p = D[(D.scope == "pooled") & (D.subset == sub)]
        if len(p):
            p = p.iloc[0]
            say(f"      H-B ({sub}, n={int(p.n)}): Var(log c*) shares slack {p.share_slack:+.0%} / "
                f"sens {p.share_sens:+.0%} / cov {p.share_cov:+.0%}; "
                f"spearman(c*, turnover) {p.spearman_c_turnover:+.3f}, "
                f"log-log slope {p.loglog_slope_vs_turnover:+.2f} (R2 {p.loglog_r2:.2f}).")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
