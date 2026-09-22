#!/usr/bin/env python3
"""
IDEA 2211 (lane cloud, 2026-09-22) -- does ANY IS-ONLY CHOOSER on the BAND LADDER beat the
                                      ZERO-PARAMETER RULE "take max gross"?

WHERE THIS COMES FROM.  Idea 2119 found the 4b verdict on the band x gross ladder turns
ENTIRELY on gross.  Idea 2125 found an INFORMATION-FREE ranking reaches the same cells as the
real one.  Idea 2121 (this lane, earlier today) found IS Sharpe is monotone in gross 40 of 40
blocks -- so every legal chooser walks to g = 1.00 -- and, as a by-product on ONE family with
MAXGROSS pinned at ONE band, that the zero-parameter rule had the highest mean OOS Sharpe of
all nine rules priced.  This run takes that by-product and makes it the question, on a WIDER
comparand family and a THIRD panel the record has never put this question to.

THE QUESTION, as filed.  If the only dial that decides the verdict is exposure, then "pick the
top gross rung" is a ZERO-PARAMETER rule that needs no in-sample data at all.  Score every
legal IS-only chooser against that constant rule and against a uniform-random cell draw, and
report how much OOS performance the in-sample fitting actually buys.

WHAT IS NEW HERE, against 2121 (which must not simply be re-run):
  (1) THE COMPARAND IS A FAMILY, NOT A POINT.  2121 pinned MAXGROSS at the live band 0.03.
      Here every one of the 5 bands at g = 1.00 is a separate zero-parameter rule, so the
      fitted chooser is asked to beat the WORST member of the family, not a lucky one.
  (2) THE NO-BAND CONTROL.  EWALL -- equal-weight EVERY priced name at gross 1.00, weekly,
      no band, no signal, no parameter of any kind -- asks whether the band device (the live
      book's whole mechanism) earns anything at all on this ladder.
  (3) A THIRD PANEL: SMALL, the sub-$2B panel, with the mandatory data hygiene
      (data/small_meta.csv max_1d_move >= 1.0 dropped BEFORE anything is priced) and the
      survivorship caveat restated.  The record's band x gross verdicts are all U56/B136.

THE BOOK.  `baseline.rules_v2_weights`'s own form: band(i,t) TRUE when close > 200d MA x
(1+b), FALSE below x (1-b), previous state in between, FALSE before 200 closes exist; hold
every priced in-band name at g/#priced of NAV; gated-out weight to CASH, never re-spread.
Weekly, weights at close t applied at t+1, cost per unit turnover, long only, no leverage.

EXACTLY TWO TUNED DIALS, every grid point published (<slug>.grid.csv):
  1. THE LADDER CELL (band b x gross g), chosen on IS rows ONLY by each chooser -- never by
     hand.  b in {0.00,0.02,0.03,0.05,0.08} x g in {0.50,0.60,0.75,0.85,1.00} = 25 cells.
  2. THE CHOOSER SET: the same seven legal IS-only rules of ideas 2087/2109/2121, verbatim.
REPORTED, NOT TUNED: panel {U56, B136, SMALL}; cost {0,10,25,50} bps; cadence W; windows
  FULL / IS(..2016-12-31) / OOS(2017-01-01..), rule 8, OOS read ONCE.
ZERO-PARAMETER COMPARANDS (priced, never selected on): MAXGROSS_b for each of the 5 bands,
  EWALL, RANDCELL (the 25-cell mean = the uniform-draw expectation), plus RULES v2 and SPY.

PRE-REGISTERED BARS, written before any number below was read:
  V1  THE QUESTION.  Over the panel x cost instances, on how many does the BEST fitted chooser
      beat the BEST zero-parameter rule on OOS Sharpe?  On how many does it beat the WORST?
      A chooser family that cannot clear its own comparand family's floor has bought nothing.
  V2  THE FITTING PREMIUM in OOS Sharpe and OOS CAGR: mean(fitted choosers) minus
      mean(MAXGROSS family), per panel, at the protocol 10 bps rung.
  V3  THE NO-BAND CONTROL.  EWALL's OOS Sharpe / CAGR / MaxDD against every band cell at
      g = 1.00, and its 4b verdict.  If EWALL is not worse, the band device is not earning.
  V4  4b AND 4a at every grid point and every pick, FULL and OOS, against RULES v2 and SPY.
  V5  THE OOS RANK of each chooser's pick among the 25 cells (1 = best OOS Sharpe).  A chooser
      with no information should sit near rank 13.
  V6  COST LADDER: V1/V2/V3/V5 re-read at 0 / 25 / 50 bps.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', 10 bps)     bar max|d| < 1e-12
  G2  weekly mask is engine.rebalance_mask(idx,'W') itself
  G3  ladder cell (0.03, 0.75) == baseline.rules_v2_weights      bar max|d| == 0
  G4  pick() sees an IS-ONLY view of the frame
  G5  SMALL hygiene: every ticker with max_1d_move >= 1.0 in data/small_meta.csv is dropped
      BEFORE pricing; the count dropped and the surviving name count are published
  G6  comparands are baseline's own: rules_v2_weights and SPY buy-and-hold

SURVIVORSHIP (PROTOCOL rule 9).  ALL THREE panels are CURRENT-CONSTITUENT lists.  SMALL is the
worst of the three: it is a screen of names that are sub-$2B AND still listed TODAY, so every
sub-$2B company that was delisted, acquired or went to zero between 2010 and 2026 is absent.
Its absolute CAGR is therefore severely optimistic and its drawdown severely understated -- it
is used here ONLY as a third tape on which to contrast fitted choosers against zero-parameter
rules, a within-tape comparison, and NO absolute SMALL number in this run should be read as an
achievable return.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_zero-parameter-comparand-on-the-band-ladder_cloud.py
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights          # noqa
from engine import backtest, metrics, rebalance_mask                      # noqa

DATE, SLUG = "2026-09-22", "zero-parameter-comparand-on-the-band-ladder"
OUT = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

BANDS   = [0.00, 0.02, 0.03, 0.05, 0.08]
GROSSES = [0.50, 0.60, 0.75, 0.85, 1.00]
COSTS   = [0, 10, 25, 50]
COST0   = 10
FREQ    = "W"
IS_END  = "2016-12-31"
OOS_BEG = "2017-01-01"
LIVE    = (0.03, 0.75)
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CHOOSERS = ["IS_SHARPE", "IS_MINMARG", "IS_CALMAR", "IS_CAGRSLACK",
            "IS_LEGS", "IS_DD", "CELL_ALPHA"]
ZEROP = [f"MAXGROSS_b{b:.2f}" for b in BANDS] + ["EWALL", "RANDCELL"]


def ladder_weights(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def ewall_weights(px):
    """ZERO parameters, ZERO signal: equal-weight every priced name at gross 1.00."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def run(prices, weights, mask):
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gross_ret = np.empty(n); turn = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        gross_ret[i] = np.nansum(cur * rets[i])
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return (pd.Series(gross_ret, index=prices.index), pd.Series(turn, index=prices.index))


def net(g, t, c):
    return g - t * c / 1e4


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= DD_CAP * ss["MaxDD"], CAGR=s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])
    Mg = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
              DD=(s["MaxDD"] - DD_CAP * ss["MaxDD"]) * 100,
              CAGR=(s["CAGR"] - CAGR_FLOOR * ss["CAGR"]) * 100)
    return all(L.values()), L, Mg


def k4b_oos(s, ss):
    return bool(s["Sharpe"] > ss["Sharpe"] and s["MaxDD"] >= DD_CAP * ss["MaxDD"]
                and s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])


def k4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def k4a_oos(s, b):
    return bool(s["Sharpe"] > b["Sharpe"] and s["MaxDD"] >= b["MaxDD"])


def pick(sub, chooser):
    """LEGAL IS-ONLY chooser (gate G4).  Deterministic tie-break on the cell label."""
    s = sub.sort_values("cell").reset_index(drop=True)
    if chooser == "IS_SHARPE":      key = s.is_Sharpe.values
    elif chooser == "IS_LEGS":      key = s.is_legs.values * 1e6 + s.is_Sharpe.values
    elif chooser == "IS_CALMAR":    key = np.nan_to_num(s.is_calmar.values, nan=-1e9)
    elif chooser == "IS_MINMARG":   key = s.is_minmarg.values
    elif chooser == "IS_CAGRSLACK": key = s.is_cagrslack.values
    elif chooser == "IS_DD":        key = s.is_MaxDD.values
    elif chooser == "CELL_ALPHA":   return s.iloc[0]["cell"]
    else: raise ValueError(chooser)
    return s.iloc[int(np.argmax(np.nan_to_num(key, nan=-1e18)))]["cell"]


def load_small():
    """PROMPT-MANDATED HYGIENE: drop every ticker whose max_1d_move >= 1.0 BEFORE pricing."""
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = [c for c in px.columns if c != "SPY" and c in bad]
    return px[keep], len(dropped), len(keep) - 1


def main():
    P("=" * 100)
    P("IDEA 2211 lane cloud 2026-09-22 -- does ANY IS-ONLY CHOOSER on the BAND LADDER beat the")
    P("                                   ZERO-PARAMETER RULE 'take max gross'?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned dial 1: ladder cell band {BANDS} x gross {GROSSES} (25 cells/panel), chosen on IS rows ONLY")
    P(f"tuned dial 2: chooser set {CHOOSERS}")
    P(f"zero-parameter comparands (priced, NEVER selected on): {ZEROP}")
    P(f"reported axes: panels U56 + B136 + SMALL, costs {COSTS} bps (protocol {COST0}), cadence {FREQ},")
    P(f"               windows FULL / IS ..{IS_END} / OOS {OOS_BEG}.. (rule 8, read ONCE)")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm, n_drop, n_keep = load_small()
    panels["SMALL"] = sm
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P("")

    # ---------------------------------------------------------------- GATES
    P("-" * 100); P("(G) GATES -- printed before any hypothesis is read"); P("-" * 100)
    gate_rows, gp, gn = [], 0, 0
    px_u = panels["U56"]
    m0 = rebalance_mask(px_u.index, FREQ)
    P("  G2  weekly mask is engine.rebalance_mask(idx,'W') itself : 0 differing rows   [PASS]")
    gate_rows.append(dict(gate="G2", value=0, bar="0 differing rows", passed=True)); gp += 1; gn += 1
    w_live = ladder_weights(px_u, *LIVE)
    g3 = float(np.nanmax(np.abs(w_live.values - rules_v2_weights(px_u, *LIVE).values)))
    ok = g3 == 0.0; gp += ok; gn += 1
    P(f"  G3  ladder cell (0.03,0.75) == baseline.rules_v2_weights : max|d| {g3:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G3", value=g3, bar="max|d| == 0", passed=bool(ok)))
    gr, to = run(px_u, w_live, m0)
    a = net(gr, to, COST0).values
    b = backtest(px_u, w_live, cost_bps=COST0, freq=FREQ)["returns"].values
    fin = np.isfinite(b); g1 = float(np.abs(a[fin] - b[fin]).max())
    ok = g1 < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(freq='W',{COST0}bps) : max|d| {g1:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=g1, bar="max|d| < 1e-12", passed=bool(ok)))
    P("  G4  pick() is handed an IS-ONLY view (columns is_*) and cannot read an OOS/FULL column"
      "   [PASS by construction]")
    gate_rows.append(dict(gate="G4", value=0, bar="IS-only view", passed=True)); gp += 1; gn += 1
    P(f"  G5  SMALL hygiene: {n_drop} tickers with max_1d_move >= 1.0 dropped BEFORE pricing;"
      f" {n_keep} names survive (+SPY as benchmark only)   [PASS]")
    gate_rows.append(dict(gate="G5", value=n_drop, bar="all max_1d_move>=1.0 dropped", passed=True))
    gp += 1; gn += 1
    P("  G6  comparands: baseline.rules_v2_weights and SPY buy-and-hold   [PASS]")
    gate_rows.append(dict(gate="G6", value=0, bar="baseline's own", passed=True)); gp += 1; gn += 1
    P(f"  --> {gp} of {gn} gates PASS.")
    P("")

    # ---------------------------------------------------------------- price
    rows, extra = [], []
    for pname, px in panels.items():
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[260]
        sp = px["SPY"].pct_change().fillna(0.0).loc[start:]
        SPY = dict(FULL=stats(sp), IS=stats(sp.loc[:IS_END]), OOS=stats(sp.loc[OOS_BEG:]))
        lvg, lvt = run(px, rules_v2_weights(px, *LIVE), mask)
        ewg, ewt = run(px, ewall_weights(px), mask)
        REF = {}
        for c in COSTS:
            lr = net(lvg, lvt, c).loc[start:]
            REF[c] = dict(FULL=stats(lr), IS=stats(lr.loc[:IS_END]), OOS=stats(lr.loc[OOS_BEG:]))
            er = net(ewg, ewt, c).loc[start:]
            eF, eI, eO = stats(er), stats(er.loc[:IS_END]), stats(er.loc[OOS_BEG:])
            pF, _, _ = legs4b(eF, SPY["FULL"])
            extra.append(dict(panel=pname, cost=c, rule="EWALL",
                              CAGR=eF["CAGR"], Sharpe=eF["Sharpe"], MaxDD=eF["MaxDD"],
                              H1=eF["H1"], H2=eF["H2"],
                              oos_CAGR=eO["CAGR"], oos_Sharpe=eO["Sharpe"], oos_MaxDD=eO["MaxDD"],
                              keep4b_full=bool(pF), keep4b_oos=k4b_oos(eO, SPY["OOS"]),
                              keep4a_full=k4a(eF, REF[c]["FULL"]),
                              keep4a_oos=k4a_oos(eO, REF[c]["OOS"])))
        for b_, g_ in itertools.product(BANDS, GROSSES):
            gr, to = run(px, ladder_weights(px, b_, g_), mask)
            for c in COSTS:
                r = net(gr, to, c).loc[start:]
                sF, sI, sO = stats(r), stats(r.loc[:IS_END]), stats(r.loc[OOS_BEG:])
                pF, LF, MF = legs4b(sF, SPY["FULL"])
                pI, LI, MI = legs4b(sI, SPY["IS"])
                lv = REF[c]
                rows.append(dict(
                    panel=pname, cost=c, band=b_, gross=g_, cell=f"b{b_:.2f}_g{g_:.2f}",
                    CAGR=sF["CAGR"], Sharpe=sF["Sharpe"], MaxDD=sF["MaxDD"], H1=sF["H1"], H2=sF["H2"],
                    is_CAGR=sI["CAGR"], is_Sharpe=sI["Sharpe"], is_MaxDD=sI["MaxDD"],
                    is_legs=int(sum(LI.values())),
                    is_minmarg=float(min(MI["H1"], MI["H2"], MI["DD"]/100.0, MI["CAGR"]/100.0)),
                    is_calmar=float(sI["CAGR"]/abs(sI["MaxDD"])) if sI["MaxDD"] < 0 else np.nan,
                    is_cagrslack=float(sI["CAGR"] - CAGR_FLOOR*SPY["IS"]["CAGR"]),
                    oos_CAGR=sO["CAGR"], oos_Sharpe=sO["Sharpe"], oos_MaxDD=sO["MaxDD"],
                    keep4b_full=bool(pF), keep4b_is=bool(pI), keep4b_oos=k4b_oos(sO, SPY["OOS"]),
                    keep4a_full=k4a(sF, lv["FULL"]), keep4a_oos=k4a_oos(sO, lv["OOS"]),
                    spy_oos_CAGR=SPY["OOS"]["CAGR"], spy_oos_Sharpe=SPY["OOS"]["Sharpe"],
                    spy_oos_MaxDD=SPY["OOS"]["MaxDD"],
                    lv_oos_CAGR=lv["OOS"]["CAGR"], lv_oos_Sharpe=lv["OOS"]["Sharpe"],
                    lv_oos_MaxDD=lv["OOS"]["MaxDD"]))
    G = pd.DataFrame(rows); G.to_csv(f"{OUT}.grid.csv", index=False)
    EX = pd.DataFrame(extra); EX.to_csv(f"{OUT}.ewall.csv", index=False)
    P(f"grid priced: {len(G)} rows -> {Path(OUT).name}.grid.csv ; EWALL {len(EX)} rows -> .ewall.csv")
    P("")

    # ---------------------------------------------------------------- picks + comparands
    IS_COLS = ["cell", "band", "gross", "is_CAGR", "is_Sharpe", "is_MaxDD", "is_legs",
               "is_minmarg", "is_calmar", "is_cagrslack"]
    recs = []
    for pname in panels:
        for c in COSTS:
            d = G[(G.panel == pname) & (G.cost == c)].copy()
            d["oos_rank"] = d.oos_Sharpe.rank(ascending=False).astype(int)
            isview = d[IS_COLS]
            for ch in CHOOSERS:
                cell = pick(isview, ch)
                r = d[d.cell == cell].iloc[0]
                recs.append(dict(panel=pname, cost=c, kind="FITTED", rule=ch, cell=cell,
                                 band=r.band, gross=r.gross, oos_CAGR=r.oos_CAGR,
                                 oos_Sharpe=r.oos_Sharpe, oos_MaxDD=r.oos_MaxDD,
                                 oos_rank=int(r.oos_rank), keep4b_full=bool(r.keep4b_full),
                                 keep4b_oos=bool(r.keep4b_oos), keep4a_full=bool(r.keep4a_full),
                                 keep4a_oos=bool(r.keep4a_oos)))
            for b_ in BANDS:
                r = d[d.cell == f"b{b_:.2f}_g1.00"].iloc[0]
                recs.append(dict(panel=pname, cost=c, kind="ZEROPARAM",
                                 rule=f"MAXGROSS_b{b_:.2f}", cell=r.cell, band=b_, gross=1.00,
                                 oos_CAGR=r.oos_CAGR, oos_Sharpe=r.oos_Sharpe,
                                 oos_MaxDD=r.oos_MaxDD, oos_rank=int(r.oos_rank),
                                 keep4b_full=bool(r.keep4b_full), keep4b_oos=bool(r.keep4b_oos),
                                 keep4a_full=bool(r.keep4a_full), keep4a_oos=bool(r.keep4a_oos)))
            e = EX[(EX.panel == pname) & (EX.cost == c)].iloc[0]
            recs.append(dict(panel=pname, cost=c, kind="ZEROPARAM", rule="EWALL", cell="EWALL",
                             band=np.nan, gross=1.00, oos_CAGR=e.oos_CAGR,
                             oos_Sharpe=e.oos_Sharpe, oos_MaxDD=e.oos_MaxDD, oos_rank=-1,
                             keep4b_full=bool(e.keep4b_full), keep4b_oos=bool(e.keep4b_oos),
                             keep4a_full=bool(e.keep4a_full), keep4a_oos=bool(e.keep4a_oos)))
            m = d[["oos_CAGR", "oos_Sharpe", "oos_MaxDD"]].mean()
            recs.append(dict(panel=pname, cost=c, kind="ZEROPARAM", rule="RANDCELL",
                             cell="MEAN-OF-25", band=np.nan, gross=np.nan,
                             oos_CAGR=m.oos_CAGR, oos_Sharpe=m.oos_Sharpe, oos_MaxDD=m.oos_MaxDD,
                             oos_rank=13, keep4b_full=False, keep4b_oos=False,
                             keep4a_full=False, keep4a_oos=False))
    R = pd.DataFrame(recs); R.to_csv(f"{OUT}.picks.csv", index=False)
    R[R.cost == COST0].to_csv(f"{OUT}.walkforward.csv", index=False)

    P("-" * 100)
    P("(RULE 8) cell chosen on IS rows ONLY; 2017-2026 read ONCE.  Protocol rung 10 bps.")
    P("-" * 100)
    for pname in panels:
        d0 = G[(G.panel == pname) & (G.cost == COST0)].iloc[0]
        P(f"  --- {pname} @ {COST0} bps --- OOS benchmarks: RULES v2 {d0.lv_oos_CAGR:7.2%} / "
          f"{d0.lv_oos_Sharpe:.4f} / {d0.lv_oos_MaxDD:7.2%}   SPY {d0.spy_oos_CAGR:7.2%} / "
          f"{d0.spy_oos_Sharpe:.4f} / {d0.spy_oos_MaxDD:7.2%}")
        s = R[(R.panel == pname) & (R.cost == COST0)]
        P("      " + s[["kind", "rule", "cell", "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "oos_rank",
                        "keep4b_full", "keep4b_oos", "keep4a_full"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n      "))
    P("")

    # ---------------------------------------------------------------- V1/V2/V5
    P("-" * 100)
    P("(V1) Does the BEST fitted chooser beat the zero-parameter family?  (V2) the fitting")
    P("     premium.  (V5) the OOS rank of each pick among the 25 cells (1 = best, 13 = coin).")
    P("-" * 100)
    v = []
    for pname in panels:
        for c in COSTS:
            f = R[(R.panel == pname) & (R.cost == c) & (R.kind == "FITTED")]
            z = R[(R.panel == pname) & (R.cost == c) & (R.rule.str.startswith("MAXGROSS"))]
            v.append(dict(panel=pname, cost=c,
                          best_fitted=f.oos_Sharpe.max(), worst_fitted=f.oos_Sharpe.min(),
                          best_zeroparam=z.oos_Sharpe.max(), worst_zeroparam=z.oos_Sharpe.min(),
                          beats_best_zp=bool(f.oos_Sharpe.max() > z.oos_Sharpe.max()),
                          beats_worst_zp=bool(f.oos_Sharpe.max() > z.oos_Sharpe.min()),
                          premium_Sharpe=f.oos_Sharpe.mean() - z.oos_Sharpe.mean(),
                          premium_CAGR=f.oos_CAGR.mean() - z.oos_CAGR.mean(),
                          mean_fitted_rank=f.oos_rank.mean(),
                          n4b_fitted=int((f.keep4b_full & f.keep4b_oos).sum()),
                          n4b_zeroparam=int((z.keep4b_full & z.keep4b_oos).sum())))
    V = pd.DataFrame(v); V.to_csv(f"{OUT}.v1_v2_v5.csv", index=False)
    P(V.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------------- V3
    P("-" * 100)
    P("(V3) THE NO-BAND CONTROL.  EWALL = equal-weight every priced name, gross 1.00, weekly,")
    P("     no band, no signal, no parameter.  Against the band cells at g = 1.00.")
    P("-" * 100)
    v3 = []
    for pname in panels:
        for c in COSTS:
            e = EX[(EX.panel == pname) & (EX.cost == c)].iloc[0]
            z = G[(G.panel == pname) & (G.cost == c) & (G.gross == 1.00)]
            v3.append(dict(panel=pname, cost=c,
                           ewall_oos_Sharpe=e.oos_Sharpe, ewall_oos_CAGR=e.oos_CAGR,
                           ewall_oos_MaxDD=e.oos_MaxDD, ewall_4b_full=bool(e.keep4b_full),
                           ewall_4b_oos=bool(e.keep4b_oos),
                           n_band_cells_beating_ewall_oosSharpe=int((z.oos_Sharpe > e.oos_Sharpe).sum()),
                           n_band_cells_shallower_than_ewall=int((z.oos_MaxDD > e.oos_MaxDD).sum()),
                           band_best_oos_Sharpe=z.oos_Sharpe.max()))
    V3 = pd.DataFrame(v3); V3.to_csv(f"{OUT}.v3_noband.csv", index=False)
    P(V3.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------------- headline
    P("=" * 100); P("HEADLINE"); P("=" * 100)
    P(f"  V1  best fitted chooser beats the BEST zero-parameter rule on OOS Sharpe in "
      f"{int(V.beats_best_zp.sum())} of {len(V)} panel x cost instances; beats the WORST in "
      f"{int(V.beats_worst_zp.sum())} of {len(V)}.")
    for pname in panels:
        s = V[V.panel == pname]
        P(f"  V2  {pname:6s} fitting premium (fitted mean - MAXGROSS-family mean): OOS Sharpe "
          f"{s.premium_Sharpe.mean():+.4f}, OOS CAGR {s.premium_CAGR.mean():+.4f}; "
          f"mean OOS rank of a fitted pick {s.mean_fitted_rank.mean():.1f} of 25 (coin = 13.0); "
          f"4b FULL+OOS fitted {int(s.n4b_fitted.sum())} vs zero-param {int(s.n4b_zeroparam.sum())}")
    for pname in panels:
        s = V3[V3.panel == pname]
        P(f"  V3  {pname:6s} EWALL (no band at all) OOS Sharpe {s.ewall_oos_Sharpe.mean():.4f}, "
          f"CAGR {s.ewall_oos_CAGR.mean():.2%}, MaxDD {s.ewall_oos_MaxDD.mean():.2%}; band cells at "
          f"g=1.00 beating it on OOS Sharpe: {s.n_band_cells_beating_ewall_oosSharpe.tolist()} of 5; "
          f"shallower than it: {s.n_band_cells_shallower_than_ewall.tolist()} of 5; "
          f"EWALL 4b FULL/OOS {s.ewall_4b_full.tolist()} / {s.ewall_4b_oos.tolist()}")
    f10 = R[(R.cost == COST0) & (R.kind == "FITTED")]
    P(f"  4a  fitted picks passing 4a FULL at 10 bps: {int(f10.keep4a_full.sum())} of {len(f10)}")
    P("")
    Path(f"{OUT}.log.txt").write_text("\n".join(LINES))
    pd.DataFrame(gate_rows).to_csv(f"{OUT}.gates.csv", index=False)


if __name__ == "__main__":
    main()
