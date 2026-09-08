#!/usr/bin/env python3
"""QUEUE idea 150 — the-DD-cap-is-what-cuts-risk-adjusted-argmaxes  (cloud, 2026-09-08).

QUESTION (verbatim from QUEUE.md idea 150)
    "idea 141's exclusion attribution shows every risk-adjusted selector's weakest bar alignment
     is with IS_MaxDD (rho -0.011 to -0.361) and that 4b's DRAWDOWN cap accounts for 0.39-0.55 of
     the exclusions of a Sharpe/Calmar/Sortino argmax, against the CAGR floor's 0.88-0.93 for
     K_MaxDD/K_NegVol.  Test whether replacing 4b's DD cap with a Calmar-style joint bar (CAGR
     and MaxDD scored together, not barred separately) changes which books pass 4b at all."

WHAT IS BEING TESTED
    PROTOCOL 4b bars CAGR and MaxDD SEPARATELY:  |MaxDD| <= 0.60|SPY MaxDD|  AND
    CAGR >= 0.70 * SPY CAGR.  A book that is 1 pp too deep is rejected however much CAGR it has,
    and a book that is 1 pp short on CAGR is rejected however shallow it is.  Idea 150 asks
    whether SCORING THE PAIR JOINTLY — one bar in which drawdown can be paid for with return —
    changes the admitted SET.  Two joint forms, each with exactly one coefficient:

      JOINT-C(kappa)   Calmar-style ratio bar:
                       CAGR / |MaxDD|  >=  kappa * (SPY CAGR / |SPY MaxDD|)
      JOINT-L(lambda)  half-plane through PROTOCOL's own corner, so it NESTS both current bars:
                       CAGR - lambda*|MaxDD|  >=  0.70*SPY_CAGR - lambda*0.60*|SPY MaxDD|
                       lambda = 0    -> the CAGR floor alone (DD cap deleted)
                       lambda -> inf -> the DD cap alone (CAGR floor deleted)
                       lambda finite -> "you may exceed the DD cap if you pay for it in CAGR at
                                         rate lambda pp of CAGR per pp of drawdown"

    The three Sharpe legs (H1, H2, OOS vs SPY) are held IDENTICAL under every rule, so any change
    in the admitted set is attributable to the DD/CAGR pair and to nothing else.

TUNED PARAMETERS — exactly two, one per form, ALL grid points reported
    1. kappa  in {0.4, 0.5, ..., 2.0}                                 (17 points, JOINT-C)
    2. lambda in {0, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 5, 10, inf}  (12 points, JOINT-L)
    Panel, book, cost rung, arm, source file and window are REPORTED axes, never selected on.

CORPUS — the record's OWN committed numbers, with a reconciliation gate
    Every `research/backtests/*.grid.csv` in the repository is scanned.  A file enters the census
    only if it carries a resolvable panel label, CAGR, MaxDD, H1, H2 and an OOS Sharpe column,
    AND passes the gate below.  Panel labels are mapped by an explicit alias table
    (U56/u56/universe.json* -> u56; B136/broad/universe_broad* -> broad; SMALL*/small -> small;
    BSTK100 -> bstk100); anything unmapped is DROPPED and counted, never guessed.

    RECONCILIATION GATE (this is what makes a re-scoring census honest).  For every row, this
    script recomputes the five 4b margins from the row's own CAGR/MaxDD/H1/H2/OOS columns and
    THIS repository's SPY bars, then compares its 4b verdict against the verdict the parent file
    committed.  A file is admitted only if its committed verdict is reproduced on EVERY row.
    Numeric agreement is reported separately and graded (idea 401: data/prices.csv was restated
    after many of these files were written, so exact numeric agreement is not expected on u56;
    verdict agreement is the bar that matters and it is checked at full strength).

WALK-FORWARD (PROTOCOL rule 8) — required, and it is the real test
    A coefficient chosen to fit the admitted set is worthless.  Both coefficients are calibrated
    on the IN-SAMPLE window ONLY (<= 2016-12-31) by equal-admission: pick the kappa (and lambda)
    whose IS admitted count is closest to the IS admitted count of PROTOCOL's own separate pair,
    using IS_CAGR / IS_MaxDD and IS-window SPY bars.  Those coefficients are then applied
    UNTOUCHED to the full sample and to the 2017-2026 OOS window, and the admitted sets are
    compared on churn and on realised OOS CAGR / Sharpe / MaxDD against RULES v2 (live) and SPY.

BOTH KEEP PATHS are scored: 4a is carried from each parent file wherever it committed one
    (pass4a / p4a / pass4a_v2 / 4a), and BOTH-paths counts are reported under SEP and under each
    joint rule, so the question "does the joint bar create a candidate" is answered directly.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): every panel in this census is CURRENT constituents (the small panel
      is the sub-$2B screen's survivors since 2010 with max_1d_move >= 1.0 dropped).  CAGR is
      inflated on every row, so the CAGR side of every joint bar is flattered relative to the
      drawdown side; a rule that trades drawdown for CAGR is therefore biased TOWARD admitting
      more here than it would on a delisting-complete panel.  No level here is achievable.
    * Idea 401's restatement means older files' committed numbers were computed on a slightly
      different data/prices.csv.  Handled by the gate above, and the per-file numeric deltas are
      printed rather than hidden.
    * This is a RE-SCORING census: it changes the bar, not the books.  It cannot discover a new
      book and does not try.  It can only say which of the record's existing rows move.
    * Rows within a parent file are not independent (arms and books overlap heavily); counts are
      reported per file and per panel so the clustering is visible.

Deterministic, standalone.  Writes .console.txt, .grid.csv (every rule x every coefficient x
every row's verdict), .sweep.csv, .churn.csv and .walkforward.csv next to itself.  Modifies
nothing.
"""
import glob
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_the-DD-cap-is-what-cuts-risk-adjusted-argmaxes_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"

PHI0, DELTA0 = 0.70, 0.60
FREQ = "W"
KAPPAS = [round(0.4 + 0.1 * i, 2) for i in range(17)]           # 0.40 .. 2.00
LAMBDAS = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, np.inf]
BAD_MOVE = 1.0

ALIAS = {}
for a in ("u56", "U56", "universe.json", "universe.json(56)", "universe.json (56)",
          "universe.json (56, control)"):
    ALIAS[a] = "u56"
for a in ("broad", "B136", "BROAD136", "broad136", "universe_broad.json",
          "universe_broad.json (136, PRIMARY)", "universe_broad(136)",
          "universe_broad.json (136, the H2-bound cell)"):
    ALIAS[a] = "broad"
for a in ("small", "SMALL", "SMALL439", "SMALL484", "SMALL480", "small484"):
    ALIAS[a] = "small"
ALIAS["BSTK100"] = "bstk100"

PANEL_COLS = ("panel", "universe", "uni")
OOS_S_COLS = ("OOS_Sharpe", "oos_Sharpe")
P4B_COLS = ("pass4b", "p4b", "4b")
P4A_COLS = ("pass4a_v2", "pass4a", "p4a", "4a")
BOOK_COLS = ("book", "arm", "point", "param", "grid", "kind", "spec", "cost", "cost_bps", "bps")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
IS_END, OOS_START = H.IS_END, H.OOS_START

pd.set_option("display.width", 320)
pd.set_option("display.max_columns", 140)
pd.set_option("display.max_rows", 4000)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def truthy(v):
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    s = str(v).strip().lower()
    return s in ("true", "1", "yes", "pass", "y", "t")


# ------------------------------------------------------------------ SPY bars per panel
def etf_set():
    import json
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    return {t for g, v in U.items() if g != "megacap" for t in v} - {"BTC-USD", "ETH-USD"}


def panel_ref():
    ref = {}
    for pk in ("u56", "broad", "bstk100", "small"):
        if pk == "small":
            px = load_universe(small=True)
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad = set(meta.loc[meta["max_1d_move"] >= BAD_MOVE, "ticker"])
            inv = [c for c in px.columns if c != "SPY" and c not in bad]
            spy_full, px = px["SPY"].pct_change().fillna(0.0), px[inv]
        elif pk == "bstk100":
            px = load_universe(broad=True)
            spy_full = px["SPY"].pct_change().fillna(0.0)
            px = px[[c for c in px.columns if c not in etf_set()]]
        else:
            px = load_universe(broad=(pk == "broad"))
            spy_full = px["SPY"].pct_change().fillna(0.0)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in (10.0, 25.0)}
        ref[pk] = dict(full=C.bars_win(spy, "full"), IS=C.bars_win(spy, "IS"),
                       OOS=C.bars_win(spy, "OOS"), m=metrics(spy),
                       m_oos=metrics(spy.loc[OOS_START:]),
                       v2_oos={c: metrics(H.window(v2[c], "OOS")) for c in v2}, n=px.shape[1],
                       start=start)
        b, mo = ref[pk]["full"], ref[pk]["m_oos"]
        say(f"[panel] {pk:8s} {px.shape[1]:3d} cols, eval from {start.date()} | SPY full "
            f"CAGR {ref[pk]['m']['CAGR']:.2%} MaxDD {ref[pk]['m']['MaxDD']:.2%} "
            f"Calmar {ref[pk]['m']['CAGR']/abs(ref[pk]['m']['MaxDD']):.3f} | bars H1>{b['s1']:.3f}"
            f" H2>{b['s2']:.3f} OOS>{b['soos']:.3f} DD<={DELTA0*abs(b['sdd']):.2%} "
            f"CAGR>={PHI0*b['scagr']:.2%} | SPY OOS {mo['Sharpe']:.3f}/{mo['CAGR']:.2%}/"
            f"{mo['MaxDD']:.2%} | RULES v2 OOS Sharpe @10 "
            f"{ref[pk]['v2_oos'][10.0]['Sharpe']:.3f}")
    return ref


# ------------------------------------------------------------------ corpus + gate
def harvest(ref):
    say("\n" + "=" * 118)
    say("CORPUS HARVEST + RECONCILIATION GATE — every research/backtests/*.grid.csv in the repo")
    say("=" * 118)
    keep, notes = [], []
    for path in sorted(OUT.glob("*.grid.csv")):
        if path.name.startswith(STEM):
            continue
        try:
            g = pd.read_csv(path)
        except Exception as e:
            notes.append(dict(file=path.name, rows=0, status=f"unreadable: {type(e).__name__}"))
            continue
        pc = next((c for c in PANEL_COLS if c in g.columns), None)
        oc = next((c for c in OOS_S_COLS if c in g.columns), None)
        vc = next((c for c in P4B_COLS if c in g.columns), None)
        need = {"CAGR", "MaxDD", "H1", "H2"}
        if pc is None or oc is None or vc is None or not need <= set(g.columns):
            notes.append(dict(file=path.name, rows=len(g), status="schema: missing "
                              + ",".join(sorted(need - set(g.columns))
                                         + ([] if pc else ["panel"]) + ([] if oc else ["OOS_Sharpe"])
                                         + ([] if vc else ["pass4b"]))))
            continue
        g = g.copy()
        g["panel_"] = g[pc].astype(str).map(ALIAS)
        n_unmapped = int(g.panel_.isna().sum())
        g = g[g.panel_.notna()]
        if not len(g):
            notes.append(dict(file=path.name, rows=0,
                              status=f"panel labels unmapped ({n_unmapped} rows dropped)"))
            continue
        b = g.panel_.map(lambda p: ref[p]["full"])
        g["m_H1_"] = g.H1 - b.map(lambda x: x["s1"])
        g["m_H2_"] = g.H2 - b.map(lambda x: x["s2"])
        g["m_OOS_"] = g[oc] - b.map(lambda x: x["soos"])
        g["m_DD_"] = DELTA0 * b.map(lambda x: abs(x["sdd"])) - g.MaxDD.abs()
        g["m_CAGR_"] = g.CAGR - PHI0 * b.map(lambda x: x["scagr"])
        g["sep_"] = ((g.m_H1_ > 0) & (g.m_H2_ > 0) & (g.m_OOS_ > 0) & (g.m_DD_ > 0)
                     & (g.m_CAGR_ > 0))
        committed = g[vc].map(truthy)
        agree = int((g.sep_ == committed).sum())
        num = np.nan
        if "m_DD" in g.columns and "m_CAGR" in g.columns:
            num = float(max((g.m_DD_ - g.m_DD).abs().max(), (g.m_CAGR_ - g.m_CAGR).abs().max()))
        st = "ADMITTED" if agree == len(g) else f"REJECTED ({len(g)-agree} verdict mismatches)"
        notes.append(dict(file=path.name, rows=len(g), dropped=n_unmapped, verdict_agree=agree,
                          committed_pass=int(committed.sum()), recomputed_pass=int(g.sep_.sum()),
                          max_margin_delta=num, status=st))
        if agree != len(g):
            continue
        ac = next((c for c in P4A_COLS if c in g.columns), None)
        g["pass4a_"] = g[ac].map(truthy) if ac else False
        g["has4a_"] = ac is not None
        g["src_"] = path.name
        idc = [c for c in BOOK_COLS if c in g.columns]
        if idc:
            rid = g[idc[0]].map(str)
            for c in idc[1:]:
                rid = rid + "|" + g[c].map(str)
            g["rowid_"] = rid
        else:
            g["rowid_"] = g.index.astype(str)
        cols = ["src_", "panel_", "rowid_", "CAGR", "MaxDD", "H1", "H2", oc,
                "m_H1_", "m_H2_", "m_OOS_", "m_DD_", "m_CAGR_", "sep_", "pass4a_", "has4a_"]
        for c in ("IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_MaxDD"):
            g[c] = g[c] if c in g.columns else np.nan
        keep.append(g[cols + ["IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_MaxDD"]]
                    .rename(columns={oc: "OOS_Sharpe"}))
    N = pd.DataFrame(notes)
    adm = N[N.status == "ADMITTED"]
    say(f"scanned {len(N)} grid files: {len(adm)} ADMITTED, "
        f"{int((N.status.astype(str).str.startswith('REJECTED')).sum())} REJECTED on the verdict "
        f"gate, {len(N) - len(adm) - int((N.status.astype(str).str.startswith('REJECTED')).sum())}"
        f" excluded on schema/panel labels.")
    say("\nADMITTED files (verdict reproduced on EVERY row):")
    say(adm[["file", "rows", "dropped", "committed_pass", "recomputed_pass",
             "max_margin_delta"]].to_string(index=False))
    rej = N[N.status.astype(str).str.startswith("REJECTED")]
    if len(rej):
        say("\nREJECTED on the verdict gate (excluded from every number below):")
        say(rej[["file", "rows", "verdict_agree", "committed_pass", "recomputed_pass",
                 "max_margin_delta", "status"]].to_string(index=False))
    N.to_csv(OUT / f"{STEM}.harvest.csv", index=False)
    df = pd.concat(keep, ignore_index=True)
    df["Calmar"] = df.CAGR / df.MaxDD.abs().replace(0, np.nan)
    df["L3"] = (df.m_H1_ > 0) & (df.m_H2_ > 0) & (df.m_OOS_ > 0)
    say(f"\nCORPUS: {len(df)} rows from {df.src_.nunique()} files over "
        f"{df.panel_.nunique()} panels {sorted(df.panel_.unique())}; "
        f"{int(df.sep_.sum())} clear PROTOCOL 4b as written; "
        f"{int(df.L3.sum())} clear the three Sharpe legs alone; "
        f"{int(df.has4a_.sum())} rows carry a committed 4a verdict.")
    say("  rows per panel: " + df.panel_.value_counts().to_dict().__str__())
    return df


# ------------------------------------------------------------------ the two joint rules
def joint_c(df, kappa, ref, win="full", cagr="CAGR", dd="MaxDD"):
    sc = df.panel_.map(lambda p: ref[p][win]["scagr"] / abs(ref[p][win]["sdd"]))
    return (df[cagr] / df[dd].abs().replace(0, np.nan)) >= kappa * sc


def joint_l(df, lam, ref, win="full", cagr="CAGR", dd="MaxDD"):
    b = df.panel_.map(lambda p: ref[p][win])
    if not np.isfinite(lam):                      # DD cap alone
        return df[dd].abs() <= DELTA0 * b.map(lambda x: abs(x["sdd"]))
    rhs = PHI0 * b.map(lambda x: x["scagr"]) - lam * DELTA0 * b.map(lambda x: abs(x["sdd"]))
    return (df[cagr] - lam * df[dd].abs()) >= rhs


def sep_pair(df, ref, win="full", cagr="CAGR", dd="MaxDD"):
    b = df.panel_.map(lambda p: ref[p][win])
    return ((df[dd].abs() <= DELTA0 * b.map(lambda x: abs(x["sdd"])))
            & (df[cagr] >= PHI0 * b.map(lambda x: x["scagr"])))


def churn(a, b):
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    inter, union = int((a & b).sum()), int((a | b).sum())
    return dict(n_a=int(a.sum()), n_b=int(b.sum()), both=inter,
                swap_in=int((b & ~a).sum()), swap_out=int((a & ~b).sum()),
                jaccard=(inter / union if union else np.nan))


# ------------------------------------------------------------------ main
def main():
    say("=" * 118)
    say("IDEA 150 — does a JOINT (Calmar-style) bar change which books pass 4b at all?")
    say(f"PROTOCOL 4b as written: 3 Sharpe legs AND |MaxDD| <= {DELTA0}|SPY DD| AND "
        f"CAGR >= {PHI0}*SPY CAGR.  The 3 Sharpe legs are held IDENTICAL under every rule.")
    say(f"kappa grid {KAPPAS}")
    say(f"lambda grid {LAMBDAS}")
    say("=" * 118)
    ref = panel_ref()
    df = harvest(ref)

    # ---------------------------------------------------------- premise audit (idea 141)
    say("\n" + "=" * 118)
    say("PREMISE AUDIT — is the DD cap really what cuts?  Exclusion attribution over the corpus.")
    say("=" * 118)
    L3 = df[df.L3]
    dd_only = (~sep_pair(L3, ref)) & (L3.m_CAGR_ > 0)
    cg_only = (~sep_pair(L3, ref)) & (L3.m_DD_ > 0)
    both_f = (L3.m_DD_ <= 0) & (L3.m_CAGR_ <= 0)
    say(f"of {len(L3)} rows clearing the three Sharpe legs, {int(L3.sep_.sum())} clear 4b.")
    say(f"  excluded by the DD CAP ALONE    : {int(dd_only.sum()):5d} "
        f"({dd_only.mean():.1%} of the Sharpe-clearing rows)")
    say(f"  excluded by the CAGR FLOOR ALONE: {int(cg_only.sum()):5d} ({cg_only.mean():.1%})")
    say(f"  excluded by BOTH                : {int(both_f.sum()):5d} ({both_f.mean():.1%})")
    say("  per panel (DD-alone / CAGR-alone / both / pass):")
    for pk, s in L3.groupby("panel_"):
        d = (~sep_pair(s, ref)) & (s.m_CAGR_ > 0)
        c = (~sep_pair(s, ref)) & (s.m_DD_ > 0)
        bt = (s.m_DD_ <= 0) & (s.m_CAGR_ <= 0)
        say(f"    {pk:8s} n={len(s):5d}  DD {int(d.sum()):5d} ({d.mean():5.1%})  "
            f"CAGR {int(c.sum()):5d} ({c.mean():5.1%})  both {int(bt.sum()):5d} "
            f"({bt.mean():5.1%})  pass {int(s.sep_.sum()):4d}")

    # ---------------------------------------------------------- the full sweep (ALL points)
    say("\n" + "=" * 118)
    say("FULL SWEEP — every coefficient reported, full-sample window, 3 Sharpe legs held fixed")
    say("=" * 118)
    base = df.sep_.values
    rows = []
    for lam in LAMBDAS:
        m = (df.L3 & joint_l(df, lam, ref)).values
        rows.append(dict(rule="JOINT-L", coef=lam, **churn(base, m),
                         mean_OOS_Sharpe=float(df.OOS_Sharpe[m].mean()),
                         mean_OOS_CAGR=float(df.OOS_CAGR[m].mean()),
                         mean_OOS_MaxDD=float(df.OOS_MaxDD[m].mean()),
                         both_paths=int((m & df.pass4a_.values).sum())))
    for k in KAPPAS:
        m = (df.L3 & joint_c(df, k, ref)).values
        rows.append(dict(rule="JOINT-C", coef=k, **churn(base, m),
                         mean_OOS_Sharpe=float(df.OOS_Sharpe[m].mean()),
                         mean_OOS_CAGR=float(df.OOS_CAGR[m].mean()),
                         mean_OOS_MaxDD=float(df.OOS_MaxDD[m].mean()),
                         both_paths=int((m & df.pass4a_.values).sum())))
    S = pd.DataFrame(rows)
    S.insert(0, "n_SEP", int(base.sum()))
    S.to_csv(OUT / f"{STEM}.sweep.csv", index=False)
    say(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  SEP (PROTOCOL as written): n {int(base.sum())}, mean OOS Sharpe "
        f"{df.OOS_Sharpe[base].mean():.4f}, mean OOS CAGR {df.OOS_CAGR[base].mean():.4f}, "
        f"mean OOS MaxDD {df.OOS_MaxDD[base].mean():.4f}, both-paths "
        f"{int((base & df.pass4a_.values).sum())}")

    # ---------------------------------------------------------- rule 8
    say("\n" + "=" * 118)
    say("RULE 8 — coefficients calibrated on the IS window ONLY (equal IS admission), then "
        "applied UNTOUCHED to the full sample and to 2017-2026")
    say("=" * 118)
    IS = df[df.IS_CAGR.notna() & df.IS_MaxDD.notna()].copy()
    say(f"  {len(IS)} of {len(df)} rows carry IS_CAGR and IS_MaxDD and can be calibrated on "
        f"({IS.src_.nunique()} files).")
    is_sep = sep_pair(IS, ref, "IS", "IS_CAGR", "IS_MaxDD")
    target = int(is_sep.sum())
    say(f"  IS admission of PROTOCOL's separate pair: {target} of {len(IS)} "
        f"({target/len(IS):.1%}) — this is the calibration target.")
    cal = []
    for lam in LAMBDAS:
        n = int(joint_l(IS, lam, ref, "IS", "IS_CAGR", "IS_MaxDD").sum())
        cal.append(dict(rule="JOINT-L", coef=lam, IS_n=n, gap=abs(n - target)))
    for k in KAPPAS:
        n = int(joint_c(IS, k, ref, "IS", "IS_CAGR", "IS_MaxDD").sum())
        cal.append(dict(rule="JOINT-C", coef=k, IS_n=n, gap=abs(n - target)))
    CAL = pd.DataFrame(cal)
    say(CAL.to_string(index=False))
    picks = {r: CAL[CAL.rule == r].sort_values(["gap", "coef"]).iloc[0].coef
             for r in ("JOINT-L", "JOINT-C")}
    say(f"\n  IS-calibrated coefficients (equal admission, ties -> smaller coefficient): "
        f"lambda* = {picks['JOINT-L']}, kappa* = {picks['JOINT-C']}")

    say("\n  applied UNTOUCHED to the full sample, on the calibratable rows:")
    wf = []
    masks = {"SEP": IS.sep_.values,
             f"JOINT-L(lam={picks['JOINT-L']})": (IS.L3 & joint_l(IS, picks["JOINT-L"],
                                                                  ref)).values,
             f"JOINT-C(kap={picks['JOINT-C']})": (IS.L3 & joint_c(IS, picks["JOINT-C"],
                                                                  ref)).values}
    for nm, m in masks.items():
        c = churn(masks["SEP"], m)
        wf.append(dict(rule=nm, admitted=c["n_b"], swap_in=c["swap_in"], swap_out=c["swap_out"],
                       jaccard=c["jaccard"],
                       OOS_Sharpe=float(IS.OOS_Sharpe[m].mean()),
                       OOS_CAGR=float(IS.OOS_CAGR[m].mean()),
                       OOS_MaxDD=float(IS.OOS_MaxDD[m].mean()),
                       full_Sharpe_H2=float(IS.H2[m].mean()),
                       both_paths=int((m & IS.pass4a_.values).sum())))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  reference OOS: SPY " + " | ".join(
        f"{p} {ref[p]['m_oos']['Sharpe']:.3f}/{ref[p]['m_oos']['CAGR']:.2%}/"
        f"{ref[p]['m_oos']['MaxDD']:.2%}" for p in sorted(ref)))
    say("  reference OOS: RULES v2 (live) @10bps " + " | ".join(
        f"{p} {ref[p]['v2_oos'][10.0]['Sharpe']:.3f}/{ref[p]['v2_oos'][10.0]['CAGR']:.2%}/"
        f"{ref[p]['v2_oos'][10.0]['MaxDD']:.2%}" for p in sorted(ref)))

    say("\n  the SWAPPED rows — what the joint bar buys and sells (means over the swapped sets):")
    sw = []
    for nm, m in masks.items():
        if nm == "SEP":
            continue
        for tag, mm in (("swap_IN (joint admits, SEP rejects)", m & ~masks["SEP"]),
                        ("swap_OUT (SEP admits, joint rejects)", masks["SEP"] & ~m)):
            if mm.sum() == 0:
                sw.append(dict(rule=nm, set=tag, n=0))
                continue
            s = IS[mm]
            sw.append(dict(rule=nm, set=tag, n=int(mm.sum()), CAGR=s.CAGR.mean(),
                           MaxDD=s.MaxDD.mean(), Calmar=s.Calmar.mean(),
                           OOS_Sharpe=s.OOS_Sharpe.mean(), OOS_CAGR=s.OOS_CAGR.mean(),
                           OOS_MaxDD=s.OOS_MaxDD.mean()))
    say(pd.DataFrame(sw).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------- which BOOKS move
    say("\n" + "=" * 118)
    say("THE QUEUE'S LITERAL QUESTION — does the admitted set of BOOKS change?")
    say("=" * 118)
    ch = []
    for nm, m in masks.items():
        if nm == "SEP":
            continue
        d = IS.assign(sep=masks["SEP"], jnt=m)
        g = d.groupby(["src_", "panel_", "rowid_"]).agg(sep=("sep", "any"), jnt=("jnt", "any"))
        ch.append(dict(rule=nm, books=len(g), sep_books=int(g.sep.sum()),
                       joint_books=int(g.jnt.sum()), books_in=int((g.jnt & ~g.sep).sum()),
                       books_out=int((g.sep & ~g.jnt).sum())))
    say(pd.DataFrame(ch).to_string(index=False))
    d = IS.assign(sep=masks["SEP"])
    for nm, m in masks.items():
        if nm != "SEP":
            d[nm] = m
    d.to_csv(OUT / f"{STEM}.churn.csv", index=False)

    say("\n  IS THE JOINT-C RESULT ONE FILE OR ONE PANEL?  Same comparison, per panel and "
        "per parent file (full-sample corpus, kappa* held at the IS-calibrated value).")
    kstar = picks["JOINT-C"]
    jm = (df.L3 & joint_c(df, kstar, ref)).values
    per = []
    for pk, s in df.assign(sep=base, jnt=jm).groupby("panel_"):
        per.append(dict(cut=f"panel={pk}", n=len(s), SEP_n=int(s.sep.sum()),
                        JC_n=int(s.jnt.sum()),
                        SEP_OOS_S=s.OOS_Sharpe[s.sep].mean(), JC_OOS_S=s.OOS_Sharpe[s.jnt].mean(),
                        SEP_OOS_C=s.OOS_CAGR[s.sep].mean(), JC_OOS_C=s.OOS_CAGR[s.jnt].mean(),
                        SEP_OOS_D=s.OOS_MaxDD[s.sep].mean(), JC_OOS_D=s.OOS_MaxDD[s.jnt].mean()))
    say(pd.DataFrame(per).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    fb = []
    for f, s in df.assign(sep=base, jnt=jm).groupby("src_"):
        if s.sep.sum() < 5 or s.jnt.sum() < 5:
            continue
        fb.append(dict(file=f, SEP_n=int(s.sep.sum()), JC_n=int(s.jnt.sum()),
                       d_OOS_Sharpe=float(s.OOS_Sharpe[s.jnt].mean()
                                          - s.OOS_Sharpe[s.sep].mean())))
    FB = pd.DataFrame(fb).dropna()
    say(f"    per-file (files with >=5 admitted rows under BOTH rules, n={len(FB)}): "
        f"JOINT-C's mean OOS Sharpe beats SEP's in {int((FB.d_OOS_Sharpe>0).sum())} of {len(FB)} "
        f"files, median d {FB.d_OOS_Sharpe.median():+.4f}, mean d {FB.d_OOS_Sharpe.mean():+.4f}")
    FB.sort_values("d_OOS_Sharpe").to_csv(OUT / f"{STEM}.perfile.csv", index=False)

    say("\n  the DD-cap-deleted corner (lambda = 0, i.e. CAGR floor only) and the "
        "CAGR-floor-deleted corner (lambda = inf, i.e. DD cap only), full sample:")
    for lam, nm in ((0.0, "lambda=0   CAGR floor ALONE (DD cap deleted)"),
                    (np.inf, "lambda=inf DD cap ALONE (CAGR floor deleted)")):
        m = (df.L3 & joint_l(df, lam, ref)).values
        c = churn(base, m)
        say(f"    {nm:48s} admits {c['n_b']:5d} (SEP {c['n_a']}), +{c['swap_in']} / "
            f"-{c['swap_out']}, OOS Sharpe {df.OOS_Sharpe[m].mean():.4f}, "
            f"OOS CAGR {df.OOS_CAGR[m].mean():.4f}, OOS MaxDD {df.OOS_MaxDD[m].mean():.4f}")

    df.assign(sep=base).to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say("\n" + "=" * 118)
    say("SURVIVORSHIP CAVEAT (idea 54): every panel in this census is CURRENT constituents — the "
        "small panel is the sub-$2B screen's survivors since 2010 (max_1d_move >= 1.0 dropped), "
        "u56/broad/bstk100 are today's large caps.  CAGR is inflated on every row, so the CAGR "
        "side of any joint bar is flattered relative to the drawdown side and a rule that lets "
        "return pay for drawdown is biased TOWARD admitting more here than it would on a "
        "delisting-complete panel.  No level in this file is an achievable return.")
    say("=" * 118)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
