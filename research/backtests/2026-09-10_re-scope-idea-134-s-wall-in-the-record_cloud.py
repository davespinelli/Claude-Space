#!/usr/bin/env python3
"""Idea 410 — re-scope idea 134's wall in the record.

Idea 137 found that idea 134's headline, 'broad @ 25 bps admits 0 of 442 arm-rows', is true
of a RANKED-BASE WEEKLY corpus and false of the PANEL: 46 of 112 rows clear 4b once cadence
and lambda open.  The queue asks how much of the record does the same thing -- publishes a
CORPUS statement wearing a PANEL's (or a cost rung's) name.

PART A  CENSUS.  Every emptiness claim ('0 of N', 'admits nothing', 'not a single', ...) in
        the committed record (LEADERBOARD.md rows + CHANGELOG.md entries), classified by
        whether it names a PANEL or a RUNG, and -- for the panel/rung-named ones -- whether
        the script that produced it actually SWEPT cadence and gross, or fixed them.  A claim
        that names a panel but was established on one cadence and one gross is an
        over-generalisation CANDIDATE, exactly idea 134's error.  Per idea 623 PART B ('a grep
        is not a census') the automatic tiers are reported beside a 20-row HAND AUDIT.

PART B  RE-TEST.  Price the candidate class directly: take the record's ranked base on all
        three live panels at both live rungs, and measure the 4b admission rate under the
        NARROW corpus the record habitually sweeps against a WIDE one.

        TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
            CADENCE in {D, W, M, Q}      (the first dial idea 137 opened)
            GROSS   in {0.50, 0.75, 1.00} (the second)
        n in {5, 10, 20, 50} is NOT a tuned parameter of this script: it is the corpus axis
        the record's own wall claims already sweep, and it is held identical between the
        narrow and the wide reading so the comparison is like for like.
            NARROW = the record's convention, cadence W and gross 0.75  ->  4 arm-rows
            WIDE   = 4 cadences x 3 grosses x 4 n                      -> 48 arm-rows
        3 panels x 2 rungs x 48 = 288 grid points, every point written to .grid.csv.

PART C  RULE 8.  A wall that only falls when two dials open is worth nothing if the dials are
        fitted.  (cadence, gross) chosen at n=20 on 2010-2016 IS Sharpe alone, 2017-2026 read
        exactly once, against idea 621's NO-DIAL control (the record's own W / 0.75), on every
        panel x rung cell.  OOS CAGR/Sharpe/MaxDD reported against RULES v2 and SPY.

PROTOCOL-fixed throughout: weights decided at close t and applied at t+1, costs 10 or 25 bps
per unit turnover, long only, no leverage.
SURVIVORSHIP: broad136 and SMALL439 are CURRENT constituent lists; SMALL439 additionally drops
the 44 names with data/small_meta.csv max_1d_move >= 1.0 (idea 623's terminal-dated screen,
priced by idea 627 -- kept here so the re-test matches the record's published convention).

Run:  python3 research/backtests/2026-09-10_re-scope-idea-134-s-wall-in-the-record_cloud.py
"""
import re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

pd.set_option("display.width", 240)
OUT = Path(__file__).with_suffix("")
IS_END, OOS_START = "2016-12-31", "2017-01-01"


# ======================================================================= PART A: the census
# TIER 1 (naive): the pattern a first pass would write.  It is WRONG, and reported anyway,
# because the size of its error is one of this file's results (idea 623 PART B: a grep is not
# a census).  `0 of \d+` with no left boundary matches the trailing "0" of "10 of 48", and
# `0/\d+` matches "0/54" inside a published "0.76/0.54" Sharpe pair.
EMPTY_NAIVE = re.compile(
    r"(0 of \d+|0/\d+|0 out of \d+|admits? nothing|admits? no\b|admits? 0\b|"
    r"none of the \d+|not a single|zero (?:of the )?\w+ (?:pass|clear)|"
    r"no (?:arm|row|book|cell|point|passer)s? (?:pass|clear|survive))", re.I)
# TIER 2 (strict): a zero that is genuinely a zero -- not a digit or a decimal point to its
# left, and not the numerator of a ratio whose denominator carries a decimal.
EMPTY_PAT = re.compile(
    r"((?<![\d.])0\s+of\s+\d+|(?<![\d.])0/\d+(?![\d.])|(?<![\d.])0 out of \d+|"
    r"admits? nothing|admits? no\b|admits? 0(?![\d.])|none of the \d+|not a single|"
    r"zero (?:of the )?\w+ (?:pass|clear)|no (?:arm|row|book|cell|point|passer)s? "
    r"(?:pass|clear|survive))", re.I)
PANEL_PAT = re.compile(r"\b(u56|universe\.json|broad136|broad|136|small439|SMALL\b|439|panel)\b", re.I)
RUNG_PAT = re.compile(r"\b\d+\s*bps\b", re.I)
# does the producing script sweep the two dials idea 137 opened?
SCRIPT_PAT = re.compile(r"(20\d\d-\d\d-\d\d_[^\s|`\"']+\.py)\s*$")
CAD_LIST = re.compile(r"""\[[^\]\n]*['"][DWMQ]['"][^\]\n]*['"][DWMQ]['"][^\]\n]*\]""")
GROSS_TOK = re.compile(r"gross", re.I)
FLOAT_TOK = re.compile(r"\b0\.\d+\b|\b1\.0+\b")


def sweeps(script_text):
    """(sweeps_cadence, sweeps_gross) for a committed backtest script."""
    cad = bool(CAD_LIST.search(script_text))
    gro = False
    for line in script_text.split("\n"):
        if GROSS_TOK.search(line) and len(set(FLOAT_TOK.findall(line))) >= 2:
            gro = True; break
    return cad, gro


def census():
    lb = [l for l in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
          if re.match(r"^\| 20\d\d-", l)]
    ch = [l for l in (ROOT / "research" / "CHANGELOG.md").read_text().split("\n")
          if l.startswith("- 20")]
    cache = {}

    def script_text(name):
        if name not in cache:
            p = ROOT / "research" / "backtests" / name
            cache[name] = p.read_text() if p.exists() else ""
        return cache[name]

    sites, naive = [], 0
    for src, lines in (("LEADERBOARD", lb), ("CHANGELOG", ch)):
        for l in lines:
            naive += len(EMPTY_NAIVE.findall(l))
            cells = [c.strip() for c in l.split("|") if c.strip()]
            m0 = SCRIPT_PAT.search(cells[-1]) if cells else None
            script = m0.group(1) if m0 else ""
            for m in EMPTY_PAT.finditer(l):
                seg = l[max(0, m.start() - 150): m.end() + 150]     # the claim's neighbourhood
                cad = gro = None; readable = False
                if script:
                    t = script_text(script)
                    if t: cad, gro = sweeps(t); readable = True
                sites.append(dict(src=src, script=script, hit=m.group(0)[:40],
                                  panel_named=bool(PANEL_PAT.search(seg)),
                                  rung_named=bool(RUNG_PAT.search(seg)), readable=readable,
                                  sweeps_cadence=bool(cad), sweeps_gross=bool(gro), seg=seg))
    return pd.DataFrame(sites), naive


# ======================================================================= shared machinery
def fast_backtest(prices, weights, freq):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def ranked_base(px, n, gross):
    """The record's ranked base: top-n of the scan.py composite, above its own 200d MA,
    equal weight at gross/n of NAV.  No vol scaler (the 2026-09-04 KEEP 4b family)."""
    s, above, _ = score(px, vol_scale=False)
    sel = (s.where(above & px.notna()).rank(axis=1, ascending=False) <= n).astype(float)
    return sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * gross


def legs(r, start):
    r = r.loc[start:]; h = len(r) // 2
    f, h1, h2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    oos, ins = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=h1["Sharpe"],
                H2=h2["Sharpe"], IS=ins["Sharpe"], OOS_CAGR=oos["CAGR"], OOS=oos["Sharpe"],
                OOS_DD=oos["MaxDD"])


def fail_4b(L, Ls):
    f = []
    if not L["H1"] > Ls["H1"]: f.append("H1")
    if not L["H2"] > Ls["H2"]: f.append("H2")
    if not L["OOS"] > Ls["OOS"]: f.append("OOS")
    if not L["MaxDD"] >= 0.60 * Ls["MaxDD"]: f.append("DD")
    if not L["CAGR"] >= 0.70 * Ls["CAGR"]: f.append("CAGR")
    return f


CADENCES, GROSSES, NS = ["D", "W", "M", "Q"], [0.50, 0.75, 1.00], [5, 10, 20, 50]
RUNGS = [10.0, 25.0]


def load_panels():
    P = {}
    P["U56"] = load_universe()
    P["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["SMALL439"] = sm.drop(columns=[c for c in sm.columns if c in bad])
    return P


def gate_g1(px):
    """G1: fast_backtest == engine.backtest (returns AND turnover) on a live arm."""
    w = ranked_base(px.drop(columns=["SPY"]), 20, 0.75)
    fr, ft = fast_backtest(px.drop(columns=["SPY"]), w, "W")
    eng = backtest(px.drop(columns=["SPY"]), w, cost_bps=0.0, freq="W")
    st = px.index[260]
    dr = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    dt_ = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    print(f"G1 fast_backtest vs engine.backtest (U56 ranked base n=20 g=0.75 W): "
          f"max|dret| {dr:.3e}  max|dturnover| {dt_:.3e}")
    assert dr < 1e-10 and dt_ < 1e-10, "G1 FAILED"


def main():
    print(__doc__.split("Run:")[0])

    # ------------------------------------------------------------------ PART A
    C, naive = census()
    print("=== PART A: CENSUS of emptiness claims in the committed record ===")
    print(f"TIER 1 (naive pattern) {naive} sites -> TIER 2 (boundary-correct) {len(C)}: "
          f"the naive pattern over-counts by {naive-len(C)} ({(naive-len(C))/naive:.1%}), because "
          f"'0 of N' with no left boundary eats the tail of '10 of 48' and '0/N' eats '0.76/0.54'. "
          f"Every number below is TIER 2.")
    print(f"{len(C)} emptiness sites: {(C.src=='LEADERBOARD').sum()} in LEADERBOARD.md, "
          f"{(C.src=='CHANGELOG').sum()} in CHANGELOG.md; "
          f"{int(C.readable.sum())} trace to a committed, readable producing script "
          f"({C[C.readable].script.nunique()} distinct).")
    scoped = C[C.panel_named | C.rung_named]
    print(f"  names a PANEL {int(C.panel_named.sum())} ({C.panel_named.mean():.1%}), "
          f"names a RUNG {int(C.rung_named.sum())} ({C.rung_named.mean():.1%}), "
          f"names either {len(scoped)} ({len(scoped)/len(C):.1%}).")
    trace = scoped[scoped.readable]
    both = trace[trace.sweeps_cadence & trace.sweeps_gross]
    neither = trace[~trace.sweeps_cadence & ~trace.sweeps_gross]
    onedial = trace[trace.sweeps_cadence ^ trace.sweeps_gross]
    assert len(both) + len(onedial) + len(neither) == len(trace)
    print(f"  of the {len(trace)} scoped sites whose script is committed and readable: "
          f"sweeps BOTH dials {len(both)} ({len(both)/len(trace):.1%}), ONE {len(onedial)} "
          f"({len(onedial)/len(trace):.1%}), NEITHER {len(neither)} ({len(neither)/len(trace):.1%}).")
    print(f"  OVER-GENERALISATION CANDIDATES (panel/rung-named, neither dial swept): "
          f"**{len(neither)}** sites across {neither.script.nunique()} scripts.")
    C.to_csv(OUT.with_name(OUT.name + ".census.csv"), index=False)

    print("\n  HAND AUDIT (idea 623 PART B: a grep is not a census) — 20 candidate sites, "
          "deterministic sample, window centred on the hit:")
    audit = neither.sort_values(["script", "hit"]).head(20)
    for _, r in audit.iterrows():
        seg = re.sub(r"\s+", " ", r.seg)
        print(f"    [{r.script[:46]:46s}] {r.hit[:18]:18s} :: {seg[110:250]}")

    # ------------------------------------------------------------------ PART B
    print("\n=== PART B: RE-TEST — NARROW (the record's W/0.75 corpus) vs WIDE (cadence x gross) ===")
    P = load_panels()
    gate_g1(P["U56"])
    for k, v in P.items():
        print(f"  {k}: {v.shape[1]-1} names, {v.index[0].date()} -> {v.index[-1].date()}")
    rows = []
    for pname, px in P.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0)
        Ls = legs(spy_r, start)
        base_g, base_t = fast_backtest(px, rules_v2_weights(px), "W")
        for n in NS:
            for g in GROSSES:
                w = ranked_base(px.drop(columns=["SPY"]), n, g)
                for cad in CADENCES:
                    gr, tu = fast_backtest(px.drop(columns=["SPY"]), w, cad)
                    for c in RUNGS:
                        L = legs(gr - tu * c / 1e4, start)
                        Lb = legs(base_g - base_t * c / 1e4, start)
                        f4b = fail_4b(L, Ls)
                        a = (L["H1"] > Lb["H1"]) and (L["H2"] > Lb["H2"]) and (L["MaxDD"] >= Lb["MaxDD"])
                        rows.append(dict(panel=pname, n=n, gross=g, cadence=cad, bps=c,
                                         narrow=(cad == "W" and g == 0.75), pass4b=not f4b,
                                         pass4a=a, fail4b="/".join(f4b) or "-",
                                         turnover_yr=tu.loc[start:].sum() / (len(tu.loc[start:]) / 252),
                                         **L))
    G = pd.DataFrame(rows)
    G.to_csv(OUT.with_name(OUT.name + ".grid.csv"), index=False)
    print(f"{len(G)} grid points written to {OUT.name}.grid.csv")

    tab = []
    for pname in P:
        for c in RUNGS:
            s = G[(G.panel == pname) & (G.bps == c)]
            nw, wd = s[s.narrow], s
            tab.append(dict(panel=pname, bps=int(c),
                            narrow_4b=f"{int(nw.pass4b.sum())} of {len(nw)}",
                            wide_4b=f"{int(wd.pass4b.sum())} of {len(wd)}",
                            wall_falls=(nw.pass4b.sum() == 0) and (wd.pass4b.sum() > 0),
                            narrow_4a=f"{int(nw.pass4a.sum())} of {len(nw)}",
                            wide_4a=f"{int(wd.pass4a.sum())} of {len(wd)}",
                            best_wide_Sharpe=wd.Sharpe.max(), best_wide_arm=(
                                f"{wd.loc[wd.Sharpe.idxmax(),'cadence']}/g{wd.loc[wd.Sharpe.idxmax(),'gross']}"
                                f"/n{wd.loc[wd.Sharpe.idxmax(),'n']}")))
    T = pd.DataFrame(tab)
    print(T.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  every 4b PASSER in the wide corpus (arm | full Sharpe | OOS Sharpe | MaxDD):")
    pas = G[G.pass4b]
    if pas.empty:
        print("    none")
    for _, r in pas.sort_values(["panel", "bps", "Sharpe"], ascending=[True, True, False]).iterrows():
        print(f"    {r.panel:9s} {int(r.bps):2d}bps  {r.cadence}/g{r.gross}/n{int(r.n):<3d}"
              f"  {r.Sharpe:.3f}  {r.OOS:.3f}  {r.MaxDD:.1%}"
              f"{'   <- NARROW corpus' if r.narrow else ''}")
    print("\n4b fail-leg frequency over all 288 points: " +
          ", ".join(f"{k} {v}" for k, v in
                    pd.Series([x for s in G.fail4b for x in s.split("/") if x != "-"]).value_counts().items()))
    print("marginal 4b pass rate by cadence: " +
          ", ".join(f"{k} {v:.1%}" for k, v in G.groupby('cadence').pass4b.mean().items()) +
          " | by gross: " + ", ".join(f"{k} {v:.1%}" for k, v in G.groupby('gross').pass4b.mean().items()) +
          " | by n: " + ", ".join(f"{k} {v:.1%}" for k, v in G.groupby('n').pass4b.mean().items()) +
          " | by rung: " + ", ".join(f"{int(k)} {v:.1%}" for k, v in G.groupby('bps').pass4b.mean().items()))

    # ------------------------------------------------------------------ PART C
    print("\n=== PART C: RULE 8 — (cadence, gross) chosen at n=20 on 2010-2016 IS Sharpe, "
          "2017-2026 read once, vs idea 621's NO-DIAL control (W / 0.75) ===")
    wf = []
    for pname, px in P.items():
        start = px.index[260]
        Ls = legs(px["SPY"].pct_change().fillna(0.0), start)
        base_g, base_t = fast_backtest(px, rules_v2_weights(px), "W")
        for c in RUNGS:
            s = G[(G.panel == pname) & (G.bps == c) & (G.n == 20)]
            pick = s.loc[s.IS.idxmax()]
            ctrl = s[(s.cadence == "W") & (s.gross == 0.75)].iloc[0]
            orc = s.loc[s.OOS.idxmax()]
            Lb = legs(base_g - base_t * c / 1e4, start)
            wf.append(dict(panel=pname, bps=int(c), pick=f"{pick.cadence}/g{pick.gross}",
                           IS=pick.IS, OOS_CAGR=pick.OOS_CAGR, OOS=pick.OOS, OOS_DD=pick.OOS_DD,
                           nodial_OOS=ctrl.OOS, d_vs_nodial=pick.OOS - ctrl.OOS,
                           pick_is_4b=bool(pick.pass4b), pick_fail4b=pick.fail4b,
                           oracle=f"{orc.cadence}/g{orc.gross}", oracle_OOS=orc.OOS,
                           SPY_OOS=Ls["OOS"], v2_OOS=Lb["OOS"]))
    W = pd.DataFrame(wf)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    beat = int((W.d_vs_nodial > 0).sum())
    print(f"  The chooser beats the NO-DIAL control in **{beat} of {len(W)}** cells, "
          f"median d {W.d_vs_nodial.median():+.4f}; the OOS oracle IS the no-dial arm in "
          f"{int((W.oracle == 'W/g0.75').sum())} of {len(W)}.")
    print(f"  Cells whose rule-8 pick beats SPY out of sample: "
          f"{int((W.OOS > W.SPY_OOS).sum())} of {len(W)}; beats RULES v2: "
          f"{int((W.OOS > W.v2_OOS).sum())} of {len(W)}.")
    print(f"  Cells whose rule-8 pick is itself a 4b PASSER: **{int(W.pick_is_4b.sum())} of "
          f"{len(W)}** — failing legs {sorted(set(W.pick_fail4b))}. The IS-Sharpe chooser and "
          f"the 4b bar want OPPOSITE ends of the gross dial (chooser g=1.00 everywhere; the 4b "
          f"pass rate is {G[G.gross==0.5].pass4b.mean():.1%} at g=0.50 and "
          f"{G[G.gross==1.0].pass4b.mean():.1%} at g=1.00).")
    T.to_csv(OUT.with_name(OUT.name + ".walls.csv"), index=False)
    W.to_csv(OUT.with_name(OUT.name + ".walkforward.csv"), index=False)
    print(f"\nwrote {OUT.name}.census.csv / .grid.csv / .walls.csv / .walkforward.csv")


if __name__ == "__main__":
    main()
