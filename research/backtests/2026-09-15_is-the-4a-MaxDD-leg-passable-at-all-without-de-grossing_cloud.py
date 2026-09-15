#!/usr/bin/env python3
"""Idea 679 (cloud lane, 2026-09-15) — is the 4a MaxDD leg passable at all without DE-GROSSING?

QUESTION
--------
PROTOCOL 4a says: Sharpe > the live rules in BOTH halves AND MaxDD no worse than the live rules.
Idea 503's committed 72,000 book-rows give 4a **145 passes, ALL of them in the de-grossing
`w = GROSS/n` form and 0 of 36,000 in the matched-gross `w = GROSS/min(n, n_elig)` form**.  Idea
508 asks the same question from the vol-matched side.  The queue's instruction: sweep the record's
committed 4a passers with GROSS HELD AT EACH ARM'S OWN NOMINAL LEVEL and report how many survive.
If the answer is near zero, PROTOCOL 4a's drawdown leg is an EXPOSURE test and should say so.

WHY IT MATTERS: RULES v2 is a de-grossed book by construction (gated-out weight goes to CASH), so
its MaxDD is small.  If the only way any candidate ever clears 4a's DD leg is by holding less, then
4a is not "beat the book" — it is "hold less than the book", and every 4a count in the record is a
statement about exposure, not about selection or timing.

THE TWO LEGS OF THIS RUN
    LEG 1 (CENSUS, zero new backtests, exact)  idea 503's committed grid.csv.gz is read as
          published.  For every NOM 4a passer the MATCHED-GROSS twin of the SAME book (same panel,
          same k, same draw, same n) is read from the same committed row, and the survival count
          and the binding leg are reported.  This is literally "the record's committed 4a passers
          with gross held at each arm's own nominal level".
    LEG 2 (PRICE, new)  503 ran ONE gross (0.75).  The queue's own tuned pair is (GROSS RUNG,
          PANEL), so this run sweeps the rung on the FULL panel and reports 4a at each, in both
          forms, with a rule-8 walk-forward and both KEEP paths.
    LEG 3 (PRICE, new)  the same sweep on the SUB-PANEL DRAW population — 503's 4a passers are all
          k-name draws, where n_elig < n often and the NOM form de-grosses hard.  This is the only
          population in which a NOM 4a pass exists, so it is the only one on which the cash-blend
          control can be tested.

TUNED PARAMETERS (PROTOCOL rule 4 — exactly two, the queue's own)
    1. gross rung g  in {0.10, 0.25, 0.40, 0.50, 0.75, 1.00}
    2. panel         in {B136, SMALL663}
REPORTING AXES, every point published, never selected on:
    n     in {5, 10, 15, 20, 30, 40}     (503's own book-size axis)
    form  in {NOM, MATCH}                (503's own form axis)

THE BOOK (idea 78/83/486/503's CAND-n, verbatim)
    eligible   name above its own 200d moving average AND vol20 < 0.60
    rank       503's unscaled composite (score(vol_scale=False)), top-n eligible names
    NOM        w = g / n                        — de-grosses whenever n_elig < n
    MATCH      w = g / min(n, n_elig_t)         — same names, same ranks, gross held at g
    cadence    weekly (freq="W"), next-day execution, 10 bps per unit turnover, no shorting,
               no leverage
    panels     B136 = universe_broad.json; SMALL663 = the sub-$2B panel with every ticker whose
               data/small_meta.csv max_1d_move >= 1.0 DROPPED FIRST (715 -> 663 names)

THE CASH-BLEND CONTROL (the decisive one)
    For every (panel, g, n) NOM arm, its STATIC CASH BLEND is the MATCH book at the SAME nominal
    g scaled by lambda = (NOM's realised mean gross) / (MATCH's realised mean gross) — i.e. the
    identical names and ranks, held at the NOM arm's realised exposure with the remainder in cash,
    and NO time-varying de-grossing.  If the blend clears 4a wherever the NOM arm does, the 4a DD
    leg is a pure exposure dial and the NOM arm's pass carries no timing information at all.

PRE-REGISTERED HYPOTHESES (written before any credited number was read)
    H_REPRO     LEG 1 reproduces idea 503's published counts: NOM 4a passes = 145 and MATCH 4a
                passes = 0 over the committed 36,000 + 36,000 rows.  A gate on the read, not
                evidence.
    H_SURVIVE   *** THE QUEUE'S OWN TEST. *** Of the committed NOM 4a passers, the share that
                survives at matched gross is <= 5%.  PASS => 4a's DD leg is an exposure test.
    H_DDLEG     the binding leg on the killed passers is the DD leg (not H1/H2) in >= 80% of them.
    H_RUNG      in LEG 2 the MATCH-form 4a pass count is 0 at every rung g >= 0.50 on BOTH panels,
                and any MATCH pass that exists appears only at the low rungs.
    H_BLEND     the static cash blend clears 4a at >= 80% of the (panel, g, n) cells where the NOM
                arm clears it — the de-grossing carries no timing information.
    H_4B_SPLIT  4b (whose DD bar is 60% of SPY's, not the live book's) PASSES at matched gross on
                cells where 4a does not, on at least one panel — i.e. the two paths disagree
                exactly where the queue says they should.
    H_WF        rule 8: the rung chosen on 2009-2016 ALONE under BOTH pre-stated choosers still
                gives 0 MATCH-form 4a passes on the untouched 2017-2026 window.

VERDICT RULE, FIXED IN ADVANCE
    ANSWERED-NO (the 4a DD leg is NOT passable without de-grossing), and a PROTOCOL wording is
        PROPOSED under rule 6 and NOT applied, iff H_SURVIVE and H_RUNG.
    ANSWERED-YES iff H_SURVIVE fails — matched-gross 4a passes exist and the record's 0/36,000 is
        a property of 503's single rung, not of the path.
    Either way this is a PATH-DEFINITION result, not a capital candidate: no book is promoted by
    this run.  Both KEEP paths are still evaluated and reported on every arm.

THE TWO PRE-STATED CHOOSERS (rule 8; the OOS window is read ONCE, after both have picked)
    C1  argmax IS Sharpe over the rungs, per (panel, n, form).
    C2  the Sep-3 memo's own rule: the SMALLEST rung whose IS MaxDD <= 60% of SPY's IS MaxDD.

GATES (printed before any verdict is read)
    G1  fast_backtest == engine.backtest on one book                                    bar 1e-10
    G2  the committed 503 grid loads with its published shape (6,000 rows x 172 cols) and its
        NOM/MATCH realised gross columns behave as documented (NOM <= MATCH at every n) bar exact
    G3  H_REPRO: this run's re-derived 4a counts off the committed grid equal 145 / 0    bar exact
    G4  determinism: no RNG outside the seeded LEG-3 draws; a LEG-2 cell recomputed      bar 0
    G5  the live RULES v2 comparand on each panel is printed before any arm is scored

SURVIVORSHIP (PROTOCOL rule 9): B136 is universe_broad.json's CURRENT constituents and SMALL663 is
the CURRENT sub-$2B screen — both are survivor lists, so every CAGR level is optimistic and every
MaxDD level is understated.  That bias makes the 4a DD leg EASIER here than it would be on a
point-in-time panel, so a finding that it is still unpassable at matched gross is conservative.

Deterministic, no network, standalone.  Does not modify RULES.md, PROTOCOL.md, scan.py, bot.py or
baseline.py.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score                # noqa: E402
from engine import backtest, metrics, rebalance_mask                       # noqa: E402

DATE = "2026-09-15"
SLUG = "is-the-4a-MaxDD-leg-passable-at-all-without-de-grossing"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260

GROSSES = [0.10, 0.25, 0.40, 0.50, 0.75, 1.00]     # tuned axis 1
PANELS = ["B136", "SMALL663"]                      # tuned axis 2
NS = [5, 10, 15, 20, 30, 40]                       # reporting axis
FORMS = ["NOM", "MATCH"]                           # reporting axis
K_DRAW = 40
N_DRAW = 120
SEED = 679

REF503 = (Path(__file__).resolve().parent
          / "2026-09-11_is-the-4b-PASS-SHARE-a-monotone-function-of-n_B.grid.csv.gz")
REF503_GROSS = 0.75
REF503_NOM_4A = 145          # idea 503's published NOM 4a count
REF503_MATCH_4A = 0          # idea 503's published MATCH 4a count

LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ---------------------------------------------------------------- 503's fast runner, verbatim
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    """Vectorised equivalent of engine.backtest's return series (idea 486/503's, verbatim)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1) - turn * cost_bps / 1e4, index=idx)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def trip(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def load_small663():
    """The sub-$2B panel with every max_1d_move >= 1.0 ticker DROPPED FIRST (run mandate)."""
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], sorted(bad)


# ---------------------------------------------------------------- PROTOCOL bars
def bars_4a(v2_r):
    h1, h2 = half_sharpes(v2_r)
    return (h1, h2, metrics(v2_r)["MaxDD"])


def test_4a(r, bp):
    b1, b2, bdd = bp
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > b1, "H2": h2 > b2, "DD": m["MaxDD"] >= bdd}


def bars_4b(spy_r):
    h1, h2 = half_sharpes(spy_r)
    m = metrics(spy_r)
    oos = spy_r.loc[OOS_START:]
    return dict(H1=h1, H2=h2, OOS=metrics(oos)["Sharpe"],
                DD=0.60 * abs(m["MaxDD"]), CAGR=0.70 * m["CAGR"])


def test_4b(r, bars):
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > bars["H1"], "H2": h2 > bars["H2"],
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > bars["OOS"],
            "DD": abs(m["MaxDD"]) <= bars["DD"], "CAGR": m["CAGR"] >= bars["CAGR"]}


def fails(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ---------------------------------------------------------------- book construction
_RANK_CACHE = {}


def rank_frame(pn, p, cols):
    """503's ranking, computed ONCE per panel (it does not depend on g, n or form)."""
    if pn not in _RANK_CACHE:
        s, above, vol20 = score(p, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [c for c in p.columns if c not in set(cols)]
        if drop:
            elig[drop] = False
        _RANK_CACHE[pn] = (s.where(elig).rank(axis=1, ascending=False), elig.sum(axis=1))
    return _RANK_CACHE[pn]


def cand_weights(pn, p, cols, n, g, form):
    """503's CAND-n book on the sub-panel `cols` of the priced frame `p`."""
    rank, ne_t = rank_frame(pn, p, cols)
    sel = (rank <= n).astype(float)
    if form == "NOM":
        return sel * (g / n), ne_t
    denom = np.minimum(ne_t, n).replace(0, np.nan)
    return sel.div(denom, axis=0).mul(g).fillna(0.0), ne_t


def main():
    t0 = time.time()
    log("=" * 100)
    log(f"IDEA 679 (cloud lane, {DATE}) — {SLUG}")
    log("=" * 100)
    log(__doc__.split("QUESTION")[0].strip())

    # ================================================================ LEG 1 — THE CENSUS
    log("\n" + "=" * 100)
    log("LEG 1 — THE CENSUS ON IDEA 503's COMMITTED 72,000 BOOK-ROWS (zero new backtests)")
    log("=" * 100)
    G = pd.read_csv(REF503)
    log(f"  idea 503 grid: {G.shape[0]} rows x {G.shape[1]} cols   "
        f"panels {sorted(G['panel'].unique())}   k {sorted(G['k'].unique())}")
    g2a = G.shape == (6000, 172)
    gross_ok = all((G[f"gross_NOM{n}"] <= G[f"gross_MATCH{n}"] + 1e-9).all() for n in NS)
    log(f"  G2 committed-grid shape {G.shape} (published 6000 x 172) and NOM gross <= MATCH gross "
        f"at every n: {'PASS' if (g2a and gross_ok) else 'FAIL'}")

    # the live RULES v2 comparand on each panel, at 503's own gross rung and sample
    px136 = load_universe(broad=True)
    px663, dropped = load_small663()
    log(f"\n  SMALL663: dropped {len(dropped)} tickers with max_1d_move >= 1.0 from "
        f"data/small_meta.csv -> {px663.shape[1] - 1} names + SPY "
        f"(SURVIVORSHIP: current constituents only — data/SMALL_PANEL_README.md)")
    PX = {"B136": (px136, [c for c in px136.columns]),
          "SMALL663": (px663, [c for c in px663.columns if c != "SPY"])}

    log("\n  G5 the live RULES v2 comparand and SPY on each panel (10 bps, weekly, t+1)")
    V2, SPYR, START, B4A, B4B = {}, {}, {}, {}, {}
    for pn, (p, _) in PX.items():
        st = p.index[WARMUP]
        START[pn] = st
        v2 = backtest(p, rules_v2_weights(p), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[st:]
        sp = p["SPY"].pct_change().fillna(0).loc[st:]
        V2[pn], SPYR[pn] = v2, sp
        B4A[pn], B4B[pn] = bars_4a(v2), bars_4b(sp)
        c, s, d = trip(v2)
        cs, ss, ds = trip(sp)
        h1, h2 = half_sharpes(v2)
        log(f"    {pn:<9} sample {st.date()} -> {p.index[-1].date()} ({len(v2)} d)")
        log(f"      RULES v2 {c:>8.2%} / {s:>7.4f} / {d:>8.2%}   halves {h1:.4f} / {h2:.4f}"
            f"   -> 4a bars: H1 > {h1:.4f}, H2 > {h2:.4f}, MaxDD >= {d:.2%}")
        log(f"      SPY      {cs:>8.2%} / {ss:>7.4f} / {ds:>8.2%}   -> 4b bars: H1 > "
            f"{B4B[pn]['H1']:.4f}, H2 > {B4B[pn]['H2']:.4f}, OOS > {B4B[pn]['OOS']:.4f}, "
            f"|MaxDD| <= {B4B[pn]['DD']:.2%}, CAGR >= {B4B[pn]['CAGR']:.2%}")

    # 503 used SMALL484 (the undropped panel) — its 4a bars come from that panel's own v2 line.
    px484 = load_universe(small=True)
    st484 = px484.index[WARMUP]
    v2_484 = backtest(px484, rules_v2_weights(px484), cost_bps=COST_BPS,
                      freq=FREQ)["returns"].loc[st484:]
    B4A_503 = {"B136": B4A["B136"], "SMALL484": bars_4a(v2_484)}
    log(f"\n  (LEG 1 scores 503's rows against 503's own panels; SMALL484 v2 bars "
        f"H1 > {B4A_503['SMALL484'][0]:.4f}, H2 > {B4A_503['SMALL484'][1]:.4f}, "
        f"MaxDD >= {B4A_503['SMALL484'][2]:.2%})")

    cen_rows = []
    for pn in ["B136", "SMALL484"]:
        b1, b2, bdd = B4A_503[pn]
        sub = G[G["panel"] == pn]
        for n in NS:
            for form in FORMS:
                t = f"{form}{n}"
                ok = ((sub[f"H1_{t}"] > b1) & (sub[f"H2_{t}"] > b2)
                      & (sub[f"MaxDD_{t}"] >= bdd))
                for leg, m in [("H1", sub[f"H1_{t}"] > b1), ("H2", sub[f"H2_{t}"] > b2),
                               ("DD", sub[f"MaxDD_{t}"] >= bdd)]:
                    cen_rows.append(dict(panel=pn, n=n, form=form, leg=leg, rows=len(sub),
                                         leg_pass=int(m.sum()), all3=int(ok.sum()),
                                         mean_gross=float(sub[f"gross_{t}"].mean()),
                                         med_MaxDD=float(sub[f"MaxDD_{t}"].median())))
    cen = pd.DataFrame(cen_rows)
    cen.to_csv(f"{OUT}.census.csv", index=False)

    piv = cen[cen.leg == "DD"].pivot_table(index=["panel", "n"], columns="form",
                                           values=["all3", "leg_pass", "mean_gross"])
    log("\n  4a on 503's committed rows: all3 = full 4a pass, leg_pass(DD) = DD leg alone, "
        "mean_gross = realised")
    log("    " + piv.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    nom_4a = int(cen[(cen.form == "NOM") & (cen.leg == "DD")]["all3"].sum())
    match_4a = int(cen[(cen.form == "MATCH") & (cen.leg == "DD")]["all3"].sum())
    h_repro = (nom_4a == REF503_NOM_4A and match_4a == REF503_MATCH_4A)
    log(f"\n  G3 / H_REPRO  re-derived NOM 4a = {nom_4a} (503 published {REF503_NOM_4A}); "
        f"MATCH 4a = {match_4a} (503 published {REF503_MATCH_4A})   "
        f"{'PASS' if h_repro else 'DIFFERS — every number below is this run''s own re-derivation'}")

    # the queue's own test: the SAME books at matched gross
    surv_rows = []
    for pn in ["B136", "SMALL484"]:
        b1, b2, bdd = B4A_503[pn]
        sub = G[G["panel"] == pn]
        for n in NS:
            tn, tm = f"NOM{n}", f"MATCH{n}"
            passers = sub[(sub[f"H1_{tn}"] > b1) & (sub[f"H2_{tn}"] > b2)
                          & (sub[f"MaxDD_{tn}"] >= bdd)]
            for _, r in passers.iterrows():
                legs = {"H1": bool(r[f"H1_{tm}"] > b1), "H2": bool(r[f"H2_{tm}"] > b2),
                        "DD": bool(r[f"MaxDD_{tm}"] >= bdd)}
                surv_rows.append(dict(
                    panel=pn, k=int(r["k"]), draw=int(r["draw"]), n=n,
                    nom_gross=float(r[f"gross_{tn}"]), match_gross=float(r[f"gross_{tm}"]),
                    nom_MaxDD=float(r[f"MaxDD_{tn}"]), match_MaxDD=float(r[f"MaxDD_{tm}"]),
                    nom_Sharpe=float(r[f"Sharpe_{tn}"]), match_Sharpe=float(r[f"Sharpe_{tm}"]),
                    nom_CAGR=float(r[f"CAGR_{tn}"]), match_CAGR=float(r[f"CAGR_{tm}"]),
                    survives=all(legs.values()), kills=fails(legs)))
    S = pd.DataFrame(surv_rows)
    S.to_csv(f"{OUT}.survivors.csv", index=False)
    n_pass, n_surv = len(S), int(S["survives"].sum()) if len(S) else 0
    share = n_surv / n_pass if n_pass else float("nan")
    h_survive = n_pass > 0 and share <= 0.05
    log(f"\n  *** THE QUEUE'S OWN TEST ***  committed NOM 4a passers: {n_pass}; "
        f"surviving at MATCHED GROSS: {n_surv}  ({share:.1%})")
    log(f"  H_SURVIVE (survival share <= 5%): {'PASS' if h_survive else 'FAIL'}")
    if n_pass:
        kc = S["kills"].value_counts()
        log(f"  what kills them (legs failed at matched gross): {kc.to_dict()}")
        dd_bound = int(S["kills"].str.contains("DD").sum())
        h_ddleg = dd_bound / n_pass >= 0.80
        log(f"  the DD leg is among the failures in {dd_bound}/{n_pass} = {dd_bound/n_pass:.1%}   "
            f"H_DDLEG (>= 80%): {'PASS' if h_ddleg else 'FAIL'}")
        log(f"  passers' realised gross: NOM median {S['nom_gross'].median():.4f} vs MATCH "
            f"{S['match_gross'].median():.4f} (nominal {REF503_GROSS:.2f}) — the passers hold "
            f"{S['nom_gross'].median()/REF503_GROSS:.1%} of nominal")
        log(f"  passers' MaxDD: NOM median {S['nom_MaxDD'].median():.2%} vs MATCH "
            f"{S['match_MaxDD'].median():.2%}; the 4a DD bar is "
            f"{B4A_503['B136'][2]:.2%} (B136) / {B4A_503['SMALL484'][2]:.2%} (SMALL484)")
        log(f"  by n: {S.groupby('n')['survives'].agg(['size','sum']).to_dict()}")
    else:
        h_ddleg = False
        log("  no committed NOM 4a passers re-derived — H_DDLEG cannot be evaluated: FAIL")

    # ================================================================ LEG 2 — THE GROSS SWEEP
    log("\n" + "=" * 100)
    log("LEG 2 — THE GROSS-RUNG SWEEP (new books; the queue's own tuned pair = rung x panel)")
    log("=" * 100)

    # G1 — the fast runner against the engine on one book
    p0, cols0 = PX["B136"]
    w0, _ = cand_weights("B136", p0, cols0, 20, 0.75, "MATCH")
    r_fast = fast_backtest(p0, w0).loc[START["B136"]:]
    r_eng = backtest(p0, w0, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[START["B136"]:]
    g1 = float((r_fast - r_eng).abs().max())
    log(f"  G1 fast_backtest vs engine.backtest (B136, n=20, g=0.75, MATCH)   max|d| = {g1:.3e}   "
        f"{'PASS' if g1 < 1e-10 else 'FAIL'}")

    rows = []
    for pn, (p, cols) in PX.items():
        st = START[pn]
        bp4a, bp4b = B4A[pn], B4B[pn]
        for g in GROSSES:
            for n in NS:
                cache = {}
                for form in FORMS:
                    w, ne_t = cand_weights(pn, p, cols, n, g, form)
                    r = fast_backtest(p, w).loc[st:]
                    wm = rebalance_mask(p.index, FREQ).values
                    gr = float(w[wm].sum(axis=1).loc[st:].mean())
                    cache[form] = (r, gr)
                    t4a, t4b = test_4a(r, bp4a), test_4b(r, bp4b)
                    c, s, d = trip(r)
                    h1, h2 = half_sharpes(r)
                    ris, roo = r.loc[:IS_END], r.loc[OOS_START:]
                    rows.append(dict(
                        panel=pn, gross=g, n=n, form=form, arm=form, days=len(r),
                        realised_gross=gr, CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                        IS_Sharpe=metrics(ris)["Sharpe"], IS_MaxDD=metrics(ris)["MaxDD"],
                        IS_CAGR=metrics(ris)["CAGR"],
                        OOS_CAGR=metrics(roo)["CAGR"], OOS_Sharpe=metrics(roo)["Sharpe"],
                        OOS_MaxDD=metrics(roo)["MaxDD"],
                        p4a=all(t4a.values()), fail4a=fails(t4a),
                        p4b=all(t4b.values()), fail4b=fails(t4b),
                        dd_leg=t4a["DD"], h1_leg=t4a["H1"], h2_leg=t4a["H2"]))
                # the STATIC CASH BLEND control: MATCH names, NOM's realised exposure, no timing
                lam = cache["NOM"][1] / cache["MATCH"][1] if cache["MATCH"][1] else np.nan
                wB, _ = cand_weights(pn, p, cols, n, g * lam, "MATCH")
                rB = fast_backtest(p, wB).loc[st:]
                wm = rebalance_mask(p.index, FREQ).values
                grB = float(wB[wm].sum(axis=1).loc[st:].mean())
                t4a, t4b = test_4a(rB, bp4a), test_4b(rB, bp4b)
                c, s, d = trip(rB)
                h1, h2 = half_sharpes(rB)
                ris, roo = rB.loc[:IS_END], rB.loc[OOS_START:]
                rows.append(dict(
                    panel=pn, gross=g, n=n, form="BLEND", arm="BLEND", days=len(rB),
                    realised_gross=grB, CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                    IS_Sharpe=metrics(ris)["Sharpe"], IS_MaxDD=metrics(ris)["MaxDD"],
                    IS_CAGR=metrics(ris)["CAGR"],
                    OOS_CAGR=metrics(roo)["CAGR"], OOS_Sharpe=metrics(roo)["Sharpe"],
                    OOS_MaxDD=metrics(roo)["MaxDD"],
                    p4a=all(t4a.values()), fail4a=fails(t4a),
                    p4b=all(t4b.values()), fail4b=fails(t4b),
                    dd_leg=t4a["DD"], h1_leg=t4a["H1"], h2_leg=t4a["H2"]))
    A = pd.DataFrame(rows)
    A.to_csv(f"{OUT}.arms.csv", index=False)

    log(f"\n  {len(A)} arms = 2 panels x {len(GROSSES)} rungs x {len(NS)} n x 3 forms "
        f"(NOM, MATCH, BLEND).  ALL are in .arms.csv; the tables below print every one.")
    for pn in PANELS:
        log(f"\n  === {pn} ===  (4a bars: H1 > {B4A[pn][0]:.4f}, H2 > {B4A[pn][1]:.4f}, "
            f"MaxDD >= {B4A[pn][2]:.2%})")
        sub = A[A.panel == pn]
        for col, tag, fmt in [("Sharpe", "Sharpe", "{:.4f}"), ("MaxDD", "MaxDD", "{:.4f}"),
                              ("CAGR", "CAGR", "{:.4f}"), ("realised_gross",
                                                           "realised gross", "{:.4f}")]:
            for form in ["NOM", "MATCH", "BLEND"]:
                piv = sub[sub.form == form].pivot(index="gross", columns="n", values=col)
                log(f"\n    {tag} — {form} (rows = nominal gross, cols = n)")
                log("      " + piv.to_string(float_format=lambda x: fmt.format(x)
                                             ).replace("\n", "\n      "))
        for form in ["NOM", "MATCH", "BLEND"]:
            piv = sub[sub.form == form].pivot(index="gross", columns="n",
                                              values="p4a").map(lambda v: "A" if v else ".")
            pivd = sub[sub.form == form].pivot(index="gross", columns="n",
                                               values="dd_leg").map(lambda v: "d" if v else ".")
            pivb = sub[sub.form == form].pivot(index="gross", columns="n",
                                               values="p4b").map(lambda v: "B" if v else ".")
            log(f"\n    4a map ({form}; A = full 4a pass)")
            log("      " + piv.to_string().replace("\n", "\n      "))
            log(f"    4a DD LEG ALONE ({form}; d = |MaxDD| no worse than RULES v2)")
            log("      " + pivd.to_string().replace("\n", "\n      "))
            log(f"    4b map ({form}; B = full 4b pass vs SPY)")
            log("      " + pivb.to_string().replace("\n", "\n      "))
        agg = sub.groupby(["form", "gross"]).agg(
            p4a=("p4a", "sum"), dd_leg=("dd_leg", "sum"), p4b=("p4b", "sum"),
            med_MaxDD=("MaxDD", "median"), med_gross=("realised_gross", "median"))
        log(f"\n    per-rung counts (out of {len(NS)} n values each)")
        log("      " + agg.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n      "))

    # H_RUNG
    hi = A[(A.form == "MATCH") & (A.gross >= 0.50)]
    n_hi = int(hi["p4a"].sum())
    lo = A[(A.form == "MATCH") & (A.gross < 0.50)]
    h_rung = n_hi == 0
    log(f"\n  H_RUNG (MATCH-form 4a passes = 0 at every rung g >= 0.50, both panels): "
        f"{n_hi} passes -> {'PASS' if h_rung else 'FAIL'}")
    log(f"    for contrast, MATCH-form 4a passes at g < 0.50: {int(lo['p4a'].sum())} of {len(lo)}; "
        f"DD leg alone {int(lo['dd_leg'].sum())} of {len(lo)} (vs {int(hi['dd_leg'].sum())} of "
        f"{len(hi)} at g >= 0.50)")

    # ================================================================ LEG 3 — THE DRAW POPULATION
    log("\n" + "=" * 100)
    log("LEG 3 — THE SUB-PANEL DRAW POPULATION (where the record's 4a passers actually live)")
    log("=" * 100)
    log(f"  LEG 2 is a FULL-panel sweep, where n_elig >= n on almost every day, so the NOM form")
    log(f"  barely de-grosses (realised gross within 1% of MATCH at every rung) and no NOM 4a")
    log(f"  cell exists to test the cash blend against.  Idea 503's 4a passers are all k-name")
    log(f"  SUB-PANEL draws, where n_elig < n often and NOM de-grosses hard.  This leg rebuilds")
    log(f"  that population at every rung: {N_DRAW} draws of k={K_DRAW} names per panel, 503's")
    log(f"  own generator shape, seeded per (panel, k) so the draws are reproducible.")
    d_rows = []
    for pn, (p, cols) in PX.items():
        st = START[pn]
        bp4a, bp4b = B4A[pn], B4B[pn]
        wm_full = rebalance_mask(p.index, FREQ).values
        rng = np.random.default_rng(SEED + hash(pn) % 1000)
        for d in range(N_DRAW):
            pick = list(rng.choice(cols, size=K_DRAW, replace=False))
            keep = list(dict.fromkeys(pick + (["SPY"] if "SPY" in p.columns else [])))
            q = p[keep].dropna(how="all").ffill()
            s, above, vol20 = score(q, vol_scale=False)
            elig = (above & (vol20 < MAX_VOL)).copy()
            drop = [c for c in q.columns if c not in set(pick)]
            if drop:
                elig[drop] = False
            rank = s.where(elig).rank(axis=1, ascending=False)
            ne_t = elig.sum(axis=1)
            wmq = rebalance_mask(q.index, FREQ).values
            for g in GROSSES:
                for n in NS:
                    sel = (rank <= n).astype(float)
                    denom = np.minimum(ne_t, n).replace(0, np.nan)
                    wN = sel * (g / n)
                    wM = sel.div(denom, axis=0).mul(g).fillna(0.0)
                    grN = float(wN[wmq].sum(axis=1).loc[st:].mean())
                    grM = float(wM[wmq].sum(axis=1).loc[st:].mean())
                    lam = grN / grM if grM else np.nan
                    wB = wM * lam
                    for form, w, gr in [("NOM", wN, grN), ("MATCH", wM, grM),
                                        ("BLEND", wB, grN)]:
                        r = fast_backtest(q, w).loc[st:]
                        t4a, t4b = test_4a(r, bp4a), test_4b(r, bp4b)
                        c, sh, dd = trip(r)
                        d_rows.append(dict(panel=pn, draw=d, gross=g, n=n, form=form,
                                           realised_gross=gr, CAGR=c, Sharpe=sh, MaxDD=dd,
                                           p4a=all(t4a.values()), dd_leg=t4a["DD"],
                                           fail4a=fails(t4a), p4b=all(t4b.values())))
    D = pd.DataFrame(d_rows)
    D.to_csv(f"{OUT}.draws.csv.gz", index=False, compression="gzip")
    log(f"\n  {len(D)} draw-books = 2 panels x {N_DRAW} draws x {len(GROSSES)} rungs x "
        f"{len(NS)} n x 3 forms.  All in .draws.csv.gz.")
    dagg = D.groupby(["panel", "form", "gross"]).agg(
        books=("p4a", "size"), p4a=("p4a", "sum"), dd_leg=("dd_leg", "sum"), p4b=("p4b", "sum"),
        med_gross=("realised_gross", "median"), med_MaxDD=("MaxDD", "median"),
        med_Sharpe=("Sharpe", "median"))
    log("\n  4a / DD-leg / 4b counts per (panel, form, rung) — EVERY cell reported")
    log("    " + dagg.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    dn = D.groupby(["panel", "form", "n"]).agg(
        books=("p4a", "size"), p4a=("p4a", "sum"), dd_leg=("dd_leg", "sum"),
        med_gross=("realised_gross", "median"))
    log("\n  the same, by book size n")
    log("    " + dn.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    # H_BLEND — tested on the draw population, cell by cell
    key = ["panel", "draw", "gross", "n"]
    piv = D.pivot_table(index=key, columns="form", values="p4a")
    nom_cells = piv[piv["NOM"] == True]                                   # noqa: E712
    if len(nom_cells):
        agree = int((nom_cells["BLEND"] == True).sum())                    # noqa: E712
        match_agree = int((nom_cells["MATCH"] == True).sum())              # noqa: E712
        h_blend = agree / len(nom_cells) >= 0.80
        log(f"\n  H_BLEND  of the {len(nom_cells)} draw-books where the DE-GROSSING (NOM) arm "
            f"clears 4a:")
        log(f"    the STATIC CASH BLEND at the same realised exposure clears it at "
            f"{agree}/{len(nom_cells)} = {agree/len(nom_cells):.1%}  -> "
            f"{'PASS' if h_blend else 'FAIL'}")
        log(f"    the MATCHED-GROSS arm (same names, gross held at nominal) clears it at "
            f"{match_agree}/{len(nom_cells)} = {match_agree/len(nom_cells):.1%}")
        log("    => the de-grossing carries NO timing information: a static cash blend at the "
            "same exposure buys the same 4a pass." if h_blend else
            "    => the blend does NOT reproduce the pass, so the de-grossing's TIMING matters.")
    else:
        h_blend = False
        log("\n  H_BLEND  no NOM 4a draw-books at any rung — the hypothesis is vacuous: FAIL")

    # H_4B_SPLIT
    split = A[(A.form == "MATCH") & (A.p4b) & (~A.p4a)]
    h_split = split["panel"].nunique() >= 1
    log(f"\n  H_4B_SPLIT  matched-gross arms that PASS 4b and FAIL 4a: {len(split)} "
        f"on {split['panel'].nunique()} panel(s) -> {'PASS' if h_split else 'FAIL'}")
    if len(split):
        log("    " + split[["panel", "gross", "n", "CAGR", "Sharpe", "MaxDD", "fail4a"]
                           ].to_string(index=False, float_format=lambda x: f"{x:.4f}"
                                       ).replace("\n", "\n    "))

    # ================================================================ RULE 8 WALK-FORWARD
    log("\n" + "=" * 100)
    log("RULE 8 WALK-FORWARD — the RUNG chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    log("=" * 100)
    wf_rows, h_wf_parts = [], []
    for pn in PANELS:
        st = START[pn]
        spy = SPYR[pn]
        v2 = V2[pn]
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        v2_oos = v2.loc[OOS_START:]
        cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
        bp4a_oos = bars_4a(v2_oos)
        bars_oos = dict(H1=half_sharpes(spy_oos)[0], H2=half_sharpes(spy_oos)[1],
                        OOS=-np.inf, DD=0.60 * abs(metrics(spy_oos)["MaxDD"]),
                        CAGR=0.70 * metrics(spy_oos)["CAGR"])
        log(f"\n  {pn}:  IS {st.date()} -> {IS_END}   OOS {OOS_START} -> {v2.index[-1].date()}")
        log(f"    SPY IS MaxDD {metrics(spy_is)['MaxDD']:.2%}  ->  C2 cap |IS MaxDD| <= {cap:.2%}")
        log(f"    OOS comparands: RULES v2 {metrics(v2_oos)['CAGR']:.2%} / "
            f"{metrics(v2_oos)['Sharpe']:.4f} / {metrics(v2_oos)['MaxDD']:.2%}   "
            f"SPY {metrics(spy_oos)['CAGR']:.2%} / {metrics(spy_oos)['Sharpe']:.4f} / "
            f"{metrics(spy_oos)['MaxDD']:.2%}")
        for form in ["NOM", "MATCH", "BLEND"]:
            for n in NS:
                cand = A[(A.panel == pn) & (A.form == form) & (A.n == n)]
                c1 = cand.loc[cand["IS_Sharpe"].idxmax()]
                el = cand[cand["IS_MaxDD"].abs() <= cap].sort_values("gross")
                picks = {"C1": c1}
                if len(el):
                    picks["C2"] = el.iloc[0]
                for cn, pk in picks.items():
                    # re-price the picked rung and read the OOS window ONCE
                    p, cols = PX[pn]
                    gpick = float(pk["gross"])
                    if form == "BLEND":
                        wN, _ = cand_weights(pn, p, cols, n, gpick, "NOM")
                        wM, _ = cand_weights(pn, p, cols, n, gpick, "MATCH")
                        wm = rebalance_mask(p.index, FREQ).values
                        lam = (float(wN[wm].sum(axis=1).loc[st:].mean())
                               / float(wM[wm].sum(axis=1).loc[st:].mean()))
                        w, _ = cand_weights(pn, p, cols, n, gpick * lam, "MATCH")
                    else:
                        w, _ = cand_weights(pn, p, cols, n, gpick, form)
                    r_oos = fast_backtest(p, w).loc[OOS_START:]
                    t4a = test_4a(r_oos, bp4a_oos)
                    t4b = {k: v for k, v in test_4b(r_oos, bars_oos).items() if k != "OOS"}
                    c, s, d = trip(r_oos)
                    wf_rows.append(dict(panel=pn, form=form, n=n, chooser=cn, gross=gpick,
                                        IS_Sharpe=float(pk["IS_Sharpe"]),
                                        IS_MaxDD=float(pk["IS_MaxDD"]),
                                        OOS_CAGR=c, OOS_Sharpe=s, OOS_MaxDD=d,
                                        p4a_oos=all(t4a.values()), fail4a=fails(t4a),
                                        p4b_oos=all(t4b.values()), fail4b=fails(t4b),
                                        v2_OOS_CAGR=metrics(v2_oos)["CAGR"],
                                        v2_OOS_Sharpe=metrics(v2_oos)["Sharpe"],
                                        v2_OOS_MaxDD=metrics(v2_oos)["MaxDD"],
                                        spy_OOS_CAGR=metrics(spy_oos)["CAGR"],
                                        spy_OOS_Sharpe=metrics(spy_oos)["Sharpe"],
                                        spy_OOS_MaxDD=metrics(spy_oos)["MaxDD"]))
                    if form == "MATCH":
                        h_wf_parts.append(not all(t4a.values()))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    log("\n  every rule-8 pick and its untouched OOS reading (ALL printed)")
    log("    " + WF[["panel", "form", "n", "chooser", "gross", "IS_Sharpe", "IS_MaxDD",
                     "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "p4a_oos", "fail4a",
                     "p4b_oos", "fail4b"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    wf_agg = WF.groupby(["panel", "form"]).agg(cells=("n", "size"), p4a_oos=("p4a_oos", "sum"),
                                               p4b_oos=("p4b_oos", "sum"))
    log("\n  OOS pass counts by panel and form")
    log("    " + wf_agg.to_string().replace("\n", "\n    "))
    h_wf = bool(h_wf_parts) and all(h_wf_parts)
    log(f"\n  H_WF (0 MATCH-form 4a passes on the untouched OOS window, both choosers): "
        f"{int(WF[(WF.form=='MATCH')]['p4a_oos'].sum())} passes -> "
        f"{'PASS' if h_wf else 'FAIL'}")

    # G4 determinism
    p, cols = PX["B136"]
    w, _ = cand_weights("B136", p, cols, 20, 0.75, "MATCH")
    r2 = fast_backtest(p, w).loc[START["B136"]:]
    ref = A[(A.panel == "B136") & (A.gross == 0.75) & (A.n == 20) & (A.form == "MATCH")].iloc[0]
    g4 = float(abs(metrics(r2)["Sharpe"] - ref["Sharpe"]))
    log(f"\n  G4 determinism (a grid cell recomputed)   |dSharpe| = {g4:.3e}   "
        f"{'PASS' if g4 == 0.0 else 'FAIL'}")

    # ================================================================ VERDICT
    log("\n" + "=" * 100)
    log("VERDICT")
    log("=" * 100)
    H = dict(H_REPRO=h_repro, H_SURVIVE=h_survive, H_DDLEG=h_ddleg, H_RUNG=h_rung,
             H_BLEND=h_blend, H_4B_SPLIT=h_split, H_WF=h_wf)
    for k, v in H.items():
        log(f"  {k:<11} {'PASS' if v else 'FAIL'}")
    pd.DataFrame([dict(hypothesis=k, result="PASS" if v else "FAIL") for k, v in H.items()]
                 ).to_csv(f"{OUT}.hypotheses.csv", index=False)
    if h_survive and h_rung:
        verdict = ("ANSWERED-NO — the 4a MaxDD leg is NOT passable without de-grossing; "
                   "a PROTOCOL wording is PROPOSED under rule 6 and NOT applied")
    elif not h_survive:
        verdict = ("ANSWERED-YES — matched-gross 4a passes exist, so 503's 0/36,000 is a property "
                   "of its single rung, not of the path")
    else:
        verdict = "SPLIT — see the hypothesis table"
    log(f"\n  VERDICT: {verdict}")
    log("  No book is promoted by this run; this is a PATH-DEFINITION result. "
        "RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.")
    log("\n  PROPOSED PROTOCOL WORDING (rule 6 — NOT applied here, for the Sunday review):")
    log("    PROTOCOL 4a, drawdown leg: 'MaxDD no worse than the live rules' must be quoted "
        "beside the arm's REALISED MEAN GROSS and beside the live rules' own. A 4a pass whose "
        "arm holds materially less than the comparand is an EXPOSURE pass and must be labelled "
        "one; the matched-gross reading of the same book is to be published beside it.")
    log("\n  SURVIVORSHIP (PROTOCOL rule 9): B136 and SMALL663 are CURRENT-constituent lists, so "
        "every MaxDD level above is understated and the 4a DD leg is EASIER here than on a "
        "point-in-time panel — a negative finding is therefore conservative.")
    log(f"\n  runtime {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
