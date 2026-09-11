#!/usr/bin/env python3
"""IDEA 557  re-read idea 300's WF-C KILL as a PANEL FACT.

THE CLAIM UNDER AUDIT
---------------------
Idea 298 replaced the share-vs-c_bar discount curve with a zero-parameter rule: *"subtract the
gate's own timing residual (~0.0 pp/yr for a pure-exposure gate, 0.3-0.6 pp/yr for an MA gate),
independent of c_bar."*  That is **the constant-residual discount**.
Idea 300 then published, on SMALL439 alone, that *"WF-C KILLS idea 298's MA constant-residual
discount out of sample (IS -0.0201 vs OOS -0.5918 pp/yr; MAE 0.5975 zero -> 0.5789 constant)"*.
Idea 305 re-ran the same WF-C off SMALL439 and got the opposite: on U56 the constant walks
forward (IS -0.3162 -> OOS -0.3377; OOS MAE 0.2348 vs zero's 0.3382) and it beats zero on B136 too.

QUESTION (the queue's): how much of the record is quoting a SMALL439 result as a general one,
and is the SMALL439 kill itself a panel fact or a split artefact?

THE OBJECT
----------
Per (panel, gate family, theta, cadence) two books are run on the same gate:
    RESPREAD  gross re-spread over the gated names to GROSS      -> r_rs
    DEGROSS   gross/N, gated-out weight to CASH                  -> r_dg
    c_t = gross(DEGROSS) / gross(RESPREAD)          (the realised exposure path)
    gap0  = 100*(CAGR(r_dg^0bps) - CAGR(r_rs^0bps))              the whole cost of gating
    pred0 = 100*(CAGR(c_bar * r_rs^0bps) - CAGR(r_rs^0bps))      the pure LEVEL part
    resid0 = gap0 - pred0                                        the TIMING residual, pp/yr
The constant-residual discount predicts a cell's resid0 by ONE number fitted on the IS window.
WF-C scores three predictors of OOS resid0 by mean absolute error:
    ZERO          (idea 298's pure-exposure claim)
    IS-MEAN       (the constant-residual discount: the panel x family IS mean)
    OWN IS CELL   (the per-cell IS value; the most greedy reading)

TWO TUNED PARAMETERS (the queue's own)
--------------------------------------
  1. PANEL (3, all reported): U56, B136, SMALL439.
  2. WINDOW (5 splits, all reported): IS ends 2012-12-31 / 2014-12-31 / **2016-12-31** (the
     record's) / 2018-12-31 / 2020-12-31; OOS is the remainder, read once per split.
Everything else is INHERITED from ideas 300/305 and not searched: theta ladder (9 rungs),
cadence {W,M,Q}, families {MA-THRESH, QUANTILE-M, QUANTILE-F}, gross 0.75, 10 bps, next-day.

PRE-REGISTERED GATES
--------------------
G0 ENGINE.  The fast backtester reproduces engine.backtest's returns/turnover/gross on a live
   cell to < 1e-12.
G1 IDENTITY.  r_dg^0bps == c_t * r_rs^0bps to < 1e-9 (idea 300 published 5.55e-17).
G2 REPRODUCTION.  All nine of idea 305's committed WF-C cells (its walkforward.csv) reproduce
   at the record's 2016-12-31 split to < 1e-4 on all five published quantities.
G3 MATCHING.  |mask fraction(QUANTILE) - mask fraction(MA)| < 0.01 per cell, as idea 305 required.
G4 PURE-EXPOSURE ARM.  |mean QUANTILE resid0| < 0.05 pp/yr on every panel - the control must be
   the pure-drag arm it is claimed to be, or the whole decomposition is meaningless.

PRE-REGISTERED READINGS
-----------------------
B1 IS THE KILL A PANEL FACT?  At the record's split, does the IS-MEAN constant beat ZERO on OOS
   MAE, per panel?  A "kill" means ZERO wins.
B2 IS IT A SPLIT ARTEFACT TOO?  The same question over all 5 splits x 3 panels x 3 families.
B3 THE AUDIT.  Census of the record's committed text for uses of the claim, classified
   GENERAL (no panel named within the sentence's neighbourhood) vs PANEL-QUALIFIED.
B4 RULE 8 BOOK LEG (mandatory).  (theta, cadence) picked on the IS window alone by IS Sharpe,
   per panel x family x construction; OOS CAGR/Sharpe/MaxDD read once against RULES v2 and SPY;
   both KEEP paths scored on every grid cell.

SURVIVORSHIP.  All three panels are CURRENT constituents / a current screen; SMALL439 drops the
44 names with max_1d_move >= 1.0 from data/small_meta.csv.  Every absolute number is inflated;
the panel CONTRAST is the object here and is less exposed, but "SMALL439 behaves differently"
could in principle be a survivorship artefact of that screen rather than a small-cap fact.

Run: python3 research/backtests/2026-09-11_re-read-idea-300s-WF-C-KILL-as-a-panel-fact_cloud.py
"""
import sys, re, time, json
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v2_weights                       # noqa: E402
from engine import backtest, metrics, rebalance_mask                       # noqa: E402

OUT = Path(__file__).with_suffix("")
def out_path(ext): return Path(str(OUT) + ext)

COST_BPS, GROSS = 10, 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
FAMILIES = ["MA-THRESH", "QUANTILE-M", "QUANTILE-F"]
PANELS = ["U56", "B136", "SMALL439"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
SPLITS = ["2012-12-31", "2014-12-31", "2016-12-31", "2018-12-31", "2020-12-31"]
RECORD_SPLIT = "2016-12-31"

BAR_ENGINE, BAR_IDENT, BAR_REPRO = 1e-12, 1e-9, 1e-4
BAR_MASK_TOL, BAR_Q_RESID = 0.01, 0.05

REF305 = (REPO / "research" / "backtests" /
          "2026-09-09_does-the-uncompensated-residual-finding-replicate-off-SMALL439_B.walkforward.csv")

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def flush_log(): out_path(".console.txt").write_text("\n".join(LOG) + "\n")
def fmt(df, p=4): return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------------------- machinery
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq="W"):
    """engine.backtest's arithmetic in numpy.  Returns (net returns, turnover, gross held)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); turn = np.zeros(n); pr = np.empty(n); grs = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        grs[i] = cur.sum()
        pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = prices.index
    return (pd.Series(pr - turn * cost_bps / 1e4, index=idx),
            pd.Series(turn, index=idx), pd.Series(grs, index=idx))


def cagr(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    return eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan


def live_mask(px): return px.notna() & px.shift(1).notna()

def dist_rank(px):
    live = live_mask(px)
    return (px / px.rolling(200).mean() - 1).where(live), live

def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)

def quantile_gate(px, x):
    dist, live = dist_rank(px)
    kt = np.ceil(x * live.sum(axis=1)).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live

def quantile_gate_frac(px, x):
    dist, live = dist_rank(px)
    kf = x * live.sum(axis=1); kfl = np.floor(kf)
    rank = dist.rank(axis=1, ascending=False, method="first")
    full = (rank.le(kfl, axis=0).fillna(False) & live).astype(float)
    marg = (rank.eq(kfl + 1, axis=0).fillna(False) & live).astype(float)
    return full + marg.mul(kf - kfl, axis=0)

def book(px, g, construction):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def cut(r, is_end):
    """IS = strictly on or before is_end; OOS = strictly after.  Matches idea 305's
    (IS_END='2016-12-31', OOS_START='2017-01-01') exactly, for any split date."""
    ts = pd.Timestamp(is_end)
    return r[r.index <= ts], r[r.index > ts]


def stat(r, is_end):
    h = len(r) // 2
    ri, ro = cut(r, is_end)
    m, mi, mo = metrics(r), metrics(ri), metrics(ro)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])

def fail_4b(s, spy):
    f = []
    if not s["H1"] > spy["H1"]: f.append("H1")
    if not s["H2"] > spy["H2"]: f.append("H2")
    if not s["oSharpe"] > spy["oSharpe"]: f.append("OOS")
    if not abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]): f.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: f.append("CAGR")
    return f


def panels():
    out = {}
    u = load_universe(); out["U56"] = (u.drop(columns=["SPY"]), u["SPY"])
    b = load_universe(broad=True); out["B136"] = (b.drop(columns=["SPY"], errors="ignore"), b["SPY"])
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    out["SMALL439"] = (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])
    return out, len(bad)


# ------------------------------------------------------------------------- B3: the audit
#
# The queue asks for "every committed use of 'the constant-residual discount is killed OOS'".
# A bare "WF-C" or a bare "resid0" is NOT that: later ideas reuse the WF-C label for a different
# test (539 cadence/gross, 735 turnover slopes), and LEADERBOARD rows carry a literal "KILL"
# verdict column that makes any nearby word look like a kill claim.  So a row is STRICT only if
# its +/-160-char neighbourhood carries ALL THREE of:
#     (i)  a DISCOUNT phrase   - constant-residual discount / IS-mean constant /
#                                "subtract the gate's own" / zero-parameter
#     (ii) the RESIDUAL object - the word residual or resid0
#     (iii) a KILL word
# Everything else is LOOSE and reported for completeness only.  Because STRICT is small, each
# STRICT row is then ADJUDICATED by hand against a published table below - the automated scope
# label and the adjudication are both in the .census.csv, so a reader can disagree with either.
OBJ_PAT = re.compile(r"(constant[- ]residual(?:[- ]discount)?|IS-mean constant|"
                     r"subtract the gate's own|zero-parameter)", re.I)
RESID_PAT = re.compile(r"(residual|resid0)", re.I)
LOOSE_PAT = re.compile(r"(WF-C|resid0|constant[- ]residual|IS-mean constant|timing residual)", re.I)
KILL_PAT = re.compile(r"(kill|killed|kills|useless|dead|does not walk forward|"
                      r"doesn't walk forward|fails out of sample|zero beats the constant|"
                      r"no longer holds)", re.I)
SMALL_PAT = re.compile(r"(SMALL4\d\d|SMALL48\d|small panel|small-cap panel|sub-\$2B|"
                       r"on this panel|idea 300)", re.I)
OTHER_PAT = re.compile(r"(U56|B136|universe_broad|broad panel)", re.I)
SELF = "re-read-idea-300s-WF-C-KILL-as-a-panel-fact"

# Hand adjudication of every STRICT row, published so it can be checked line by line.
# value = (is it a claim that THE CONSTANT-RESIDUAL DISCOUNT IS KILLED OOS?, one-line reason)
ADJUDICATION = {
    ("research/CHANGELOG.md", 214):
        (True, "idea 300's changelog entry - states the WF-C kill; says 'on this panel'"),
    ("research/CHANGELOG.md", 216):
        (False, "idea 298's entry - says the discount WALKS FORWARD; the kill is the share curve"),
    ("research/LEADERBOARD.md", 2890):
        (False, "idea 298's WF-B row - the kill is of the share-vs-c_bar CURVE, not the discount"),
    ("research/LEADERBOARD.md", 2901):
        (True, "idea 300's WF-C row - 'KILL of the MA-gate constant-residual discount out of "
               "sample', NO panel named in the reader's neighbourhood"),
    ("research/LEADERBOARD.md", 4274):
        (False, "idea 305's row - this IS the correction ('WF-C REVERSES idea 300's OOS KILL')"),
    ("research/QUEUE.md", 303):
        (False, "idea 305's Done entry - carries the reversal, names all three panels"),
    ("research/QUEUE.md", 563):
        (True, "idea 300's Done entry - 'WF-C KILLS idea 298's MA constant-residual discount out "
               "of sample', NO panel named in the reader's neighbourhood"),
    ("research/backtests/2026-09-06_does-a-pure-exposure-gate-exist-on-the-small-panel_C.result.md", 87):
        (True, "idea 300's own result.md, the WF-C heading - states the kill; SMALL439 is named "
               "on the NEXT wrapped line, so the GENERAL label here is a line-wrap artefact"),
    ("research/backtests/2026-09-06_does-a-pure-exposure-gate-exist-on-the-small-panel_C.result.md", 88):
        (True, "idea 300's own result.md - states the kill; the file name names the small panel"),
    ("research/backtests/2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud.result.md", 9):
        (False, "idea 298's result.md - says the discount 'does' walk forward"),
    ("research/backtests/2026-09-09_does-the-uncompensated-residual-finding-replicate-off-SMALL439_B.result.md", 89):
        (False, "idea 305's result.md - the correction itself"),
    ("research/backtests/2026-09-09_is-the-gate-timing-residual-a-constant-in-pp-per-year_B.result.md", 8):
        (False, "idea 551 - frames the prescription as untested OOS; not a kill claim"),
}


def census():
    """One row per (file, line).  A line can be thousands of characters (a LEADERBOARD row), so
    EVERY match on it is windowed and the line is STRICT if ANY window carries all three tokens;
    the reported context is that qualifying window.  Lines belonging to this run's own queue
    entry are excluded."""
    files = sorted(set(list((REPO / "research").glob("*.md"))
                       + list((REPO / "research" / "backtests").glob("*.md"))
                       + list((REPO / "research" / "backtests").glob("*.py"))))
    rows = []
    for f in files:
        if SELF in f.name: continue
        try: txt = f.read_text(errors="ignore")
        except Exception: continue
        rel = str(f.relative_to(REPO))
        kind = "CODE" if rel.endswith(".py") else "PROSE"
        lines = txt.split("\n")
        by_line = {}
        for m in LOOSE_PAT.finditer(txt):
            line = txt.count("\n", 0, m.start()) + 1
            lo, hi = max(0, m.start() - 160), min(len(txt), m.end() + 160)
            ctx = txt[lo:hi].replace("\n", " ")
            strict = bool(OBJ_PAT.search(ctx) and RESID_PAT.search(ctx) and KILL_PAT.search(ctx))
            prev = by_line.get(line)
            if prev is None or (strict and not prev[0]):
                by_line[line] = (strict, ctx, m.group(0))
        for line, (strict, ctx, mt) in sorted(by_line.items()):
            if lines[line - 1].lstrip().startswith("557."): continue      # this run's own entry
            scope = ("PANEL-QUALIFIED" if SMALL_PAT.search(ctx) else
                     ("OTHER-PANEL" if OTHER_PAT.search(ctx) else "GENERAL"))
            adj, why = ADJUDICATION.get((rel, line), (None, ""))
            rows.append(dict(file=rel, line=line, kind=kind,
                             tier="STRICT" if strict else "LOOSE", scope=scope,
                             match=mt, is_kill_claim=adj, adjudication=why,
                             context=ctx[:500]))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    P("=" * 150)
    P("IDEA 557  re-read idea 300's WF-C KILL as a PANEL FACT")
    P("cloud lane, 2026-09-11.  two tuned parameters: PANEL (3) x WINDOW SPLIT (5).")
    P("Everything else inherited from ideas 300/305: theta ladder (9), cadence (3),")
    P("families (3), gross 0.75, 10 bps, next-day.  Every grid point published.")
    P("=" * 150)
    P("pre-registered gates: G0 engine < 1e-12 | G1 identity < 1e-9 | G2 idea 305's nine WF-C")
    P("cells reproduce < 1e-4 | G3 |d mask frac| < 0.01 | G4 |mean QUANTILE resid0| < 0.05 pp/yr")
    P("=" * 150)

    PN, n_dropped = panels()
    for pn in PANELS:
        px, _ = PN[pn]
        P(f"  PANEL {pn:9s}: {px.shape[1]:3d} names, {px.index[0].date()}..{px.index[-1].date()}, "
          f"{len(px)} bars" + (f" ({n_dropped} dropped for max_1d_move >= 1.0)"
                               if pn == "SMALL439" else ""))

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    # ------------------------------------------------------------------- G0 ENGINE GATE
    pxg = PN["U56"][0]
    gg = ma_gate(pxg, 0.0)
    ref = backtest(pxg, book(pxg, gg, "DEGROSS"), cost_bps=COST_BPS, freq="W")
    fr, ft, fg = fast_backtest(pxg, book(pxg, gg, "DEGROSS"), COST_BPS, "W")
    e0 = max(float((ref["returns"] - fr).abs().max()),
             float((ref["turnover"] - ft).abs().max()),
             float((ref["weights"].sum(axis=1) - fg).abs().max()))
    G0 = e0 < BAR_ENGINE
    P(f"\n  G0 ENGINE      max|d| vs engine.backtest {e0:.3e} -> {'PASS' if G0 else 'FAIL'}")

    # -------------------------------------------------------------------- the grid
    P("\nbuilding the grid: 3 panels x 9 theta x 3 cadences x 3 families x 2 constructions "
      "= 486 books")
    rows, decomp, matchrows, RET = [], [], [], {}
    spy_by, live_by = {}, {}
    ident_max = 0.0
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        spy_by[pn] = stat(spy_px.pct_change().fillna(0.0).loc[start:], RECORD_SPLIT)
        live_by[pn] = stat(live_full.reindex(px.index).fillna(0.0).loc[start:], RECORD_SPLIT)
        live = live_mask(px).loc[start:]; nlive = live.sum(axis=1)
        for th in MA_THETA:
            gm = ma_gate(px, th)
            x = float((gm.loc[start:].sum(axis=1) / nlive).mean())
            gates = {"MA-THRESH": gm, "QUANTILE-M": quantile_gate(px, x),
                     "QUANTILE-F": quantile_gate_frac(px, x)}
            for fam in FAMILIES:
                fr_ = float((gates[fam].loc[start:].sum(axis=1) / nlive).mean())
                matchrows.append(dict(panel=pn, theta=th, family=fam, x=x, frac=fr_,
                                      d_frac=fr_ - x))
            for cad in CADENCES:
                for fam in FAMILIES:
                    arms = {}
                    for con in CONSTRUCTIONS:
                        r10, turn, grs = fast_backtest(px, book(px, gates[fam], con),
                                                       COST_BPS, cad)
                        r10 = r10.loc[start:]; turn = turn.loc[start:]; grs = grs.loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        arms[con] = dict(r10=r10, r0=r0, gross=grs)
                        RET[(pn, th, cad, fam, con)] = r10
                        s = stat(r10, RECORD_SPLIT)
                        rows.append(dict(panel=pn, theta=th, cad=cad, family=fam, con=con, **s,
                                         p4a=verdict_4a(s, live_by[pn]),
                                         f4b="|".join(fail_4b(s, spy_by[pn])),
                                         pass4b=len(fail_4b(s, spy_by[pn])) == 0))
                    dg, rs = arms["DEGROSS"], arms["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident_max = max(ident_max,
                                    float((dg["r0"] - c_t * rs["r0"]).abs().max()))
                    for sp in SPLITS:
                        for tag in ("IS", "OOS"):
                            k = 0 if tag == "IS" else 1
                            rr, rd = cut(rs["r0"], sp)[k], cut(dg["r0"], sp)[k]
                            ct = cut(c_t, sp)[k]
                            cb = float(ct.mean())
                            g0 = 100 * (cagr(rd) - cagr(rr))
                            p0 = 100 * (cagr(cb * rr) - cagr(rr))
                            decomp.append(dict(panel=pn, theta=th, cad=cad, family=fam,
                                               split=sp, window=tag, n=len(rr), c_bar=cb,
                                               gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0))
        P(f"  {pn} done ({time.time() - t0:.0f}s)")

    R = pd.DataFrame(rows); D = pd.DataFrame(decomp); M = pd.DataFrame(matchrows)
    R.to_csv(out_path(".grid.csv"), index=False)
    D.to_csv(out_path(".decomp.csv"), index=False)

    # --------------------------------------------------------------------- gates
    P("\n" + "=" * 150); P("GATES"); P("=" * 150)
    G1 = ident_max < BAR_IDENT
    P(f"  G1 IDENTITY    max|r_dg0 - c_t*r_rs0| over all 162 cells {ident_max:.3e} -> "
      f"{'PASS' if G1 else 'FAIL'}")
    dmax = float(M.loc[M.family != "MA-THRESH", "d_frac"].abs().max())
    G3 = dmax < BAR_MASK_TOL
    P(f"  G3 MATCHING    max |d mask frac| (QUANTILE vs MA) {dmax:.5f} -> "
      f"{'PASS' if G3 else 'FAIL'}")
    for fam in ["QUANTILE-M", "QUANTILE-F"]:
        sub = M[M.family == fam]
        P(f"                 {fam:<11} max |d frac| {sub.d_frac.abs().max():.5f}"
          + "".join(f" | {pn} {sub[sub.panel == pn].d_frac.abs().max():.5f}" for pn in PANELS))
    worst = M.loc[M.loc[M.family != "MA-THRESH", "d_frac"].abs().idxmax()]
    P(f"                 worst cell: {worst.panel} {worst.family} theta {worst.theta:+.2f} "
      f"d_frac {worst.d_frac:+.5f}  (1/n_live = {1 / PN[worst.panel][0].shape[1]:.5f})")
    qr = D[(D.family != "MA-THRESH") & (D.split == RECORD_SPLIT) & (D.window == "IS")]
    qmax = float(qr.groupby("panel").resid0_pp.mean().abs().max())
    G4 = qmax < BAR_Q_RESID
    P(f"  G4 PURE-EXPO   max |mean QUANTILE resid0| by panel {qmax:.4f} pp/yr -> "
      f"{'PASS' if G4 else 'FAIL'}")
    for pn in PANELS:
        v = D[(D.family != "MA-THRESH") & (D.split == RECORD_SPLIT) & (D.window == "IS")
              & (D.panel == pn)].resid0_pp.mean()
        P(f"                 {pn:9s} {v:+.4f} pp/yr")

    # ------------------------------------------------------- WF-C, the record's split (G2)
    def wfc(panel, fam, split):
        di = D[(D.panel == panel) & (D.family == fam) & (D.split == split) &
               (D.window == "IS")].set_index(["theta", "cad"]).resid0_pp
        do = D[(D.panel == panel) & (D.family == fam) & (D.split == split) &
               (D.window == "OOS")].set_index(["theta", "cad"]).resid0_pp
        return dict(panel=panel, family=fam, split=split,
                    is_mean=float(di.mean()), oos_mean=float(do.mean()),
                    mae_zero=float(do.abs().mean()),
                    mae_const=float((do - di.mean()).abs().mean()),
                    mae_cell=float((do - di).abs().mean()),
                    drift=float(do.mean() - di.mean()), n=int(len(do)))

    ref305 = pd.read_csv(REF305)
    ref305 = ref305[ref305.test == "WF-C"]
    P("\n" + "=" * 150)
    P(f"G2 REPRODUCTION of idea 305's nine committed WF-C cells at the record's "
      f"{RECORD_SPLIT} split")
    P("=" * 150)
    P(f"{'panel':<9} {'family':<11} {'IS mean':>9} {'OOS mean':>9} {'MAE zero':>9} "
      f"{'MAE const':>10} {'MAE cell':>9} | {'max|d| vs 305':>13}")
    g2err = 0.0
    for _, r in ref305.iterrows():
        c = wfc(r.panel, r.arm, RECORD_SPLIT)
        d = max(abs(c["is_mean"] - r.isSharpe), abs(c["oos_mean"] - r.oCAGR),
                abs(c["mae_const"] - r.oSharpe), abs(c["mae_zero"] - r.oMaxDD),
                abs(c["mae_cell"] - r.vs_RULESv2))
        g2err = max(g2err, d)
        P(f"{r.panel:<9} {r.arm:<11} {c['is_mean']:>9.4f} {c['oos_mean']:>9.4f} "
          f"{c['mae_zero']:>9.4f} {c['mae_const']:>10.4f} {c['mae_cell']:>9.4f} | {d:>13.3e}")
    G2 = g2err < BAR_REPRO
    P(f"\n  G2 REPRODUCTION max|d| over 9 cells x 5 quantities {g2err:.3e} -> "
      f"{'PASS' if G2 else 'FAIL'}")
    per = {}
    for _, r in ref305.iterrows():
        c = wfc(r.panel, r.arm, RECORD_SPLIT)
        per[r.panel] = max(per.get(r.panel, 0.0),
                           max(abs(c["is_mean"] - r.isSharpe), abs(c["oos_mean"] - r.oCAGR),
                               abs(c["mae_const"] - r.oSharpe), abs(c["mae_zero"] - r.oMaxDD),
                               abs(c["mae_cell"] - r.vs_RULESv2)))
    P("  per-panel max|d|: " + " | ".join(f"{k} {v:.3e}" for k, v in per.items()))

    # G2b  is the U56 residue a DATA-VINTAGE gap?  prices.csv is 2026-09-10 today; idea 305 ran
    # on 2026-09-09.  B136/SMALL439 read prices_broad/small, unchanged since 2026-09-04, and
    # reproduce to 1e-15.  Re-cut U56 MA-THRESH k trading days short and re-measure.
    P("\n  G2b VINTAGE DIAGNOSTIC — U56 MA-THRESH re-run on a panel truncated k trading days:")
    ref_u = ref305[(ref305.panel == "U56") & (ref305.arm == "MA-THRESH")].iloc[0]
    pxU = PN["U56"][0]
    for kk in (0, 1, 2, 3):
        pxk = pxU.iloc[:len(pxU) - kk] if kk else pxU
        startk = pxk.index[260]
        dis, dos = [], []
        for th in MA_THETA:
            gk = ma_gate(pxk, th)
            for cad in CADENCES:
                a = {}
                for con in CONSTRUCTIONS:
                    r10, turn, grs = fast_backtest(pxk, book(pxk, gk, con), COST_BPS, cad)
                    r10 = r10.loc[startk:]; turn = turn.loc[startk:]
                    a[con] = dict(r0=r10 + turn * COST_BPS / 1e4, gross=grs.loc[startk:])
                ct = (a["DEGROSS"]["gross"] /
                      a["RESPREAD"]["gross"].replace(0, np.nan)).fillna(0.0)
                for tag, j in (("IS", 0), ("OOS", 1)):
                    rr = cut(a["RESPREAD"]["r0"], RECORD_SPLIT)[j]
                    rd = cut(a["DEGROSS"]["r0"], RECORD_SPLIT)[j]
                    cb = float(cut(ct, RECORD_SPLIT)[j].mean())
                    v = 100 * (cagr(rd) - cagr(rr)) - 100 * (cagr(cb * rr) - cagr(rr))
                    (dis if tag == "IS" else dos).append(v)
        dis, dos = np.array(dis), np.array(dos)
        dk = max(abs(dis.mean() - ref_u.isSharpe), abs(dos.mean() - ref_u.oCAGR),
                 abs(np.abs(dos - dis.mean()).mean() - ref_u.oSharpe),
                 abs(np.abs(dos).mean() - ref_u.oMaxDD),
                 abs(np.abs(dos - dis).mean() - ref_u.vs_RULESv2))
        P(f"    k={kk} (ends {pxk.index[-1].date()}): IS {dis.mean():+.4f} OOS {dos.mean():+.4f} "
          f"MAEzero {np.abs(dos).mean():.4f} MAEconst {np.abs(dos - dis.mean()).mean():.4f} "
          f"-> max|d| vs idea 305 {dk:.3e}"
          + ("   <== REPRODUCES" if dk < BAR_REPRO else ""))

    P(f"\n  GATES: G0 {G0} G1 {G1} G2 {G2} G3 {G3} G4 {G4}")

    # ------------------------------------------------------------ B1 / B2: the WF-C ladder
    P("\n" + "=" * 150)
    P("B1 + B2  WF-C OVER PANEL x SPLIT x FAMILY (45 cells, ALL REPORTED).")
    P("'KILL' = ZERO beats the IS-mean constant on OOS MAE, i.e. the discount does not walk forward.")
    P("=" * 150)
    wf_rows = [wfc(pn, fam, sp) for pn in PANELS for fam in FAMILIES for sp in SPLITS]
    WF = pd.DataFrame(wf_rows)
    WF["verdict"] = np.where(WF.mae_const < WF.mae_zero, "CONSTANT WALKS", "KILL (zero wins)")
    WF["gain_pct"] = 100 * (WF.mae_zero - WF.mae_const) / WF.mae_zero
    WF.to_csv(out_path(".wfc.csv"), index=False)
    P(f"{'panel':<9} {'family':<11} {'split':<11} {'n':>3} {'IS mean':>9} {'OOS mean':>9} "
      f"{'drift':>8} {'MAE zero':>9} {'MAE const':>10} {'MAE cell':>9} {'gain %':>7}  verdict")
    for _, r in WF.iterrows():
        P(f"{r.panel:<9} {r.family:<11} {r.split:<11} {r.n:>3} {r.is_mean:>9.4f} "
          f"{r.oos_mean:>9.4f} {r.drift:>8.4f} {r.mae_zero:>9.4f} {r.mae_const:>10.4f} "
          f"{r.mae_cell:>9.4f} {r.gain_pct:>7.1f}  {r.verdict}")
    P("\nWF-C verdict counts (MA-THRESH = the family idea 298's discount is about):")
    ma = WF[WF.family == "MA-THRESH"]
    P(fmt(ma.pivot_table(index="panel", columns="split", values="gain_pct").reindex(PANELS), 1))
    P("\n  (cell value = % of OOS MAE the constant saves over zero; negative = the KILL)")
    for pn in PANELS:
        s = ma[ma.panel == pn]
        P(f"  {pn:9s} MA-THRESH: constant walks forward on {int((s.gain_pct > 0).sum())}/"
          f"{len(s)} splits; mean gain {s.gain_pct.mean():+.1f}%, "
          f"IS->OOS drift {s.drift.mean():+.4f} pp/yr "
          f"(|drift| range {s.drift.abs().min():.4f}..{s.drift.abs().max():.4f})")
    q = WF[WF.family != "MA-THRESH"]
    P(f"  QUANTILE arms (idea 298's ZERO claim): |OOS mean resid0| max "
      f"{q.oos_mean.abs().max():.4f} pp/yr over {len(q)} cells; zero wins "
      f"{int((q.gain_pct <= 0).sum())}/{len(q)}")

    # ---------------------------------------------------------------------- B3 the audit
    P("\n" + "=" * 150)
    P("B3  THE AUDIT — committed uses of \'the constant-residual discount is killed OOS\'")
    P("=" * 150)
    C = census()
    C.to_csv(out_path(".census.csv"), index=False)
    P(f"  {len(C)} deduped mentions (one row per file x line) in {C.file.nunique()} files.")
    P("  tier x kind:"); P(fmt(pd.crosstab(C.tier, C.kind), 0))
    S = C[C.tier == "STRICT"].copy()
    SP = S[S.kind == "PROSE"]
    P(f"\n  STRICT (discount phrase AND the residual object AND a kill word, all within the same")
    P(f"  +/-160-char neighbourhood): {len(S)} rows, {len(SP)} of them in committed PROSE.")
    P("  automated scope of the STRICT prose rows: "
      + ", ".join(f"{sc} {int((SP.scope == sc).sum())}"
                  for sc in ["PANEL-QUALIFIED", "OTHER-PANEL", "GENERAL"]))
    P("\n  HAND ADJUDICATION of every STRICT prose row (the automated label over-counts: a")
    P("  LEADERBOARD 'KILL' verdict column, idea 298's share-CURVE kill and idea 305's own")
    P("  CORRECTION all trip the regex).  Table is in the source and in .census.csv:")
    P(f"\n{'file:line':<105} {'scope':<16} {'claim?':<7} why")
    for _, r in SP.sort_values(["file", "line"]).iterrows():
        tag = {True: "YES", False: "no", None: "?"}[r.is_kill_claim]
        P(f"{r.file + ':' + str(r.line):<105} {r.scope:<16} {tag:<7} {r.adjudication}")
    real = SP[SP.is_kill_claim == True]
    real_gen = real[real.scope == "GENERAL"]
    P(f"\n  ADJUDICATED: {len(real)} of {len(SP)} STRICT prose rows are genuine statements that")
    P(f"  the constant-residual discount is killed OOS.  ALL {len(real)} originate with IDEA 300.")
    P(f"  Of those, {len(real_gen)} are stated with NO panel named in the reader's "
      f"neighbourhood:  <== the queue's question")
    for _, r in real_gen.iterrows():
        P(f"    {r.file}:{r.line}")
        P(f"      ...{r.context[:320]}...")
    P(f"  and {len(real) - len(real_gen)} name the panel (one of those, result.md:87, is a")
    P("  line-wrap artefact of the classifier, not a real omission — see the table).")
    P(f"\n  The record has ALREADY published the correction in "
      f"{int((SP.adjudication.str.contains('correction|reversal', case=False, na=False)).sum())} "
      f"places (idea 305: LEADERBOARD row 4274, QUEUE 303, its own result.md) — so the exposure")
    P("  is the two idea-300 artefacts that were never restated, not a general mis-citation.")
    P("\n  LOOSE rows (the WF-C label reused by later ideas for a DIFFERENT test, and resid0")
    P("  table cells) are in .census.csv and are not claims about idea 298's discount.")

    # ------------------------------------------------------- B4 rule-8 book leg (mandatory)
    P("\n" + "=" * 150)
    P("B4  RULE 8 WALK-FORWARD, BOOK LEG (mandatory).  (theta, cadence) picked on the IS")
    P("window ALONE by IS Sharpe, per panel x family x construction x split; OOS read once.")
    P("=" * 150)
    P("  (re-cutting the cached 486 books at each of the 5 splits)")
    picks = []
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        for sp in SPLITS:
            spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:], sp)
            live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:], sp)
            for fam in FAMILIES:
                for con in CONSTRUCTIONS:
                    best, bk = -np.inf, None
                    allc = []
                    for th in MA_THETA:
                        for cad in CADENCES:
                            s = stat(RET[(pn, th, cad, fam, con)], sp)
                            allc.append((th, cad, s))
                            if s["isSharpe"] > best: best, bk = s["isSharpe"], (th, cad, s)
                    th, cad, s = bk
                    f4 = fail_4b(s, spy_s)
                    picks.append(dict(split=sp, panel=pn, family=fam, con=con,
                                      pick_theta=th, pick_cad=cad, isSharpe=s["isSharpe"],
                                      oCAGR=s["oCAGR"], oSharpe=s["oSharpe"],
                                      oMaxDD=s["oMaxDD"],
                                      spy_oCAGR=spy_s["oCAGR"], spy_oSharpe=spy_s["oSharpe"],
                                      spy_oMaxDD=spy_s["oMaxDD"],
                                      live_oCAGR=live_s["oCAGR"], live_oSharpe=live_s["oSharpe"],
                                      live_oMaxDD=live_s["oMaxDD"],
                                      d_SPY=s["oSharpe"] - spy_s["oSharpe"],
                                      d_RULESv2=s["oSharpe"] - live_s["oSharpe"],
                                      p4a=verdict_4a(s, live_s), pass4b=len(f4) == 0,
                                      f4b="|".join(f4)))
    PK = pd.DataFrame(picks)
    PK.to_csv(out_path(".walkforward.csv"), index=False)
    P(f"\n{'split':<11} {'panel':<9} {'family':<11} {'con':<9} {'pick':<14} {'OOS CAGR':>9} "
      f"{'OOS Sh':>8} {'OOS DD':>8} | {'vs SPY':>8} {'vs v2':>8} | 4a  4b")
    for _, r in PK[PK.split == RECORD_SPLIT].iterrows():
        P(f"{r.split:<11} {r.panel:<9} {r.family:<11} {r.con:<9} "
          f"th{r.pick_theta:+.2f}/{r.pick_cad:<8} {r.oCAGR:>8.2%} {r.oSharpe:>8.4f} "
          f"{r.oMaxDD:>8.2%} | {r.d_SPY:>+8.4f} {r.d_RULESv2:>+8.4f} | "
          f"{'Y' if r.p4a else 'n'}   {'PASS' if r.pass4b else r.f4b}")
    P("\n  comparands OOS at the record's split:")
    for pn in PANELS:
        r = PK[(PK.split == RECORD_SPLIT) & (PK.panel == pn)].iloc[0]
        P(f"    {pn:9s} SPY {r.spy_oCAGR:.2%} / {r.spy_oSharpe:.4f} / {r.spy_oMaxDD:.2%}   "
          f"RULES v2 {r.live_oCAGR:.2%} / {r.live_oSharpe:.4f} / {r.live_oMaxDD:.2%}")
    P(f"\n  over ALL {len(PK)} walk-forward picks (5 splits x 3 panels x 3 families x 2 con): "
      f"4a {int(PK.p4a.sum())}/{len(PK)}, 4b {int(PK.pass4b.sum())}/{len(PK)}")
    P(f"  over the full {len(R)}-cell grid at the record's split: 4a {int(R.p4a.sum())}/{len(R)}, "
      f"4b {int(R.pass4b.sum())}/{len(R)}")
    if int(R.pass4b.sum()):
        P("  4b passers:")
        P(fmt(R[R.pass4b][["panel", "theta", "cad", "family", "con", "CAGR", "Sharpe",
                           "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD"]]))
    P("  binding 4b legs over the grid:")
    from collections import Counter
    cnt = Counter(l for s in R.loc[~R.pass4b, "f4b"] for l in s.split("|") if l)
    for k, v in cnt.most_common(): P(f"    {k:<5} {v}")

    # -------------------------- appendix: the 4b passers under an EQUAL-WEIGHT bar (idea 742)
    # Same run, same day: idea 742 established that a 4b pass against cap-weighted SPY on a
    # large-cap panel is largely a COMPARAND fact (the standing candidate survives 0 of 9
    # equal-weight bars).  Every 4b passer below is therefore re-scored against an equal-weight
    # basket of its own panel.  This is a robustness READING, not a third tuned parameter.
    P("\n" + "=" * 150)
    P("APPENDIX — the 4b passers re-scored against an EQUAL-WEIGHT bar (idea 742, same run)")
    P("=" * 150)
    ew_by = {}
    for pn in PANELS:
        px, _ = PN[pn]
        start = px.index[260]
        rr = px.pct_change().fillna(0.0)
        lv = live_mask(px)
        w = lv.astype(float); w = w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        ew_by[pn] = stat(((rr * w).sum(axis=1)).loc[start:], RECORD_SPLIT)
        e = ew_by[pn]
        P(f"  {pn:9s} EW bar: CAGR {e['CAGR']:.2%} Sharpe {e['Sharpe']:.4f} MaxDD {e['MaxDD']:.2%} "
          f"halves {e['H1']:.4f}/{e['H2']:.4f} OOS Sharpe {e['oSharpe']:.4f} | "
          f"4b floors CAGR {0.70 * e['CAGR']:.2%} DD {0.60 * abs(e['MaxDD']):.2%}")
    PASS = R[R.pass4b].copy()
    surv = 0
    P(f"\n{'panel':<9} {'theta':>6} {'cad':<4} {'family':<11} {'con':<9} {'CAGR':>7} "
      f"{'Sharpe':>7} | vs EW bar")
    for _, r in PASS.iterrows():
        s = dict(H1=r.H1, H2=r.H2, oSharpe=r.oSharpe, MaxDD=r.MaxDD, CAGR=r.CAGR)
        f = fail_4b(s, ew_by[r.panel])
        surv += len(f) == 0
        P(f"{r.panel:<9} {r.theta:>+6.2f} {r.cad:<4} {r.family:<11} {r.con:<9} {r.CAGR:>6.2%} "
          f"{r.Sharpe:>7.4f} | {'4b PASS' if not f else 'FAIL ' + ','.join(f)}")
    P(f"\n  {surv} of {len(PASS)} SPY-4b passers also clear an equal-weight bar on their own panel.")

    # --------------------------------------------------------------------------- answer
    P("\n" + "=" * 150); P("ANSWER"); P("=" * 150)
    rec = ma[ma.split == RECORD_SPLIT].set_index("panel")
    for pn in PANELS:
        r = rec.loc[pn]
        P(f"  {pn:9s} at the record's split: MAE zero {r.mae_zero:.4f} vs constant "
          f"{r.mae_const:.4f} -> {r.verdict} ({r.gain_pct:+.1f}%)")
    nkill = int((ma.gain_pct <= 0).sum())
    P(f"\n  Over all 15 MA-THRESH panel x split cells the constant walks forward in "
      f"{15 - nkill} and is killed in {nkill}.")
    P(f"  ADJUDICATED kill-claims in committed prose: {len(real)} (all idea 300's), of which "
      f"{len(real_gen)} state it with no panel named.")

    json.dump(dict(gates=dict(G0=bool(G0), G1=bool(G1), G2=bool(G2), G3=bool(G3), G4=bool(G4)),
                   engine_err=float(e0), ident_max=float(ident_max), g2_err=float(g2err),
                   mask_err=float(dmax), q_resid=float(qmax),
                   wfc_ma_kill_cells=int(nkill), wfc_ma_cells=int(len(ma)),
                   census_total=int(len(C)), strict_claims=int(len(S)),
                   strict_prose_claims=int(len(SP)),
                   adjudicated_kill_claims=int(len(real)),
                   adjudicated_general=int(len(real_gen)),
                   p4a_grid=int(R.p4a.sum()), p4b_grid=int(R.pass4b.sum()), n_grid=int(len(R)),
                   p4a_wf=int(PK.p4a.sum()), p4b_wf=int(PK.pass4b.sum()), n_wf=int(len(PK))),
              out_path(".summary.json").open("w"), indent=2)
    P(f"\nwrote .grid.csv .decomp.csv .wfc.csv .census.csv .walkforward.csv .summary.json")
    P(f"elapsed {time.time() - t0:.1f}s")
    flush_log()


if __name__ == "__main__":
    main()
