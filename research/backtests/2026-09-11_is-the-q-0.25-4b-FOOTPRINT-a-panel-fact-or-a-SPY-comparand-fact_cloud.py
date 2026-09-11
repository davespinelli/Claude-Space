#!/usr/bin/env python3
"""Idea 548 - "is-the-q-0.25-4b-FOOTPRINT-a-panel-fact-or-a-SPY-comparand-fact"
(cloud lane, 2026-09-11).

The question
------------
Idea 310-B built 540 fresh panels x 3 books = 1,620 cells and found **4b 46/1620, of which 41
sit at q=0.25, 5 at q=0.50 and 0 at q=0.75** - and 4a 0/1620.  In that design `q` is the
SMALL-CAP SHARE of the panel (n_small = round(q*k), the rest drawn from the large-cap pool), so
the 4b footprint lives entirely on the LARGE-CAP-HEAVY panels.

PROTOCOL rule 4's 4b path judges every book against **SPY**, a large-cap index, on all five
bars.  So a panel that is 75% large caps is being asked to beat a bar made of the same thing it
holds, while a panel that is 75% small caps is being asked to beat a bar made of something else.
The queue's question is whether the q-gradient is a PANEL fact (these panels really do earn more
per unit of risk) or a COMPARAND fact (the fixed SPY bar is simply easier for a panel that
resembles SPY).

The test the queue asks for: **re-run 4b against a CAP-MATCHED BLENDED benchmark instead of SPY
and report how many passers survive.**

Tuned parameters (PROTOCOL rule 4: at most two).  Every grid point reported.
    1. BENCHMARK BLEND - six definitions, every one scored on every cell:
         B_SPY     100% SPY.  The PROTOCOL bar.  THE CONTROL.
         B_LARGE   equal-weight of the LARGE-cap pool (the panels' own large-cap source).
         B_SMALL   equal-weight of the SMALL-cap pool (the panels' own small-cap source).
         B_MATCH   q*B_SMALL + (1-q)*B_LARGE - the exact cap match for a panel of small-cap
                   share q.  This is the queue's "cap-matched blended benchmark".
         B_HALF    0.5*B_SPY + 0.5*B_MATCH - halfway between the PROTOCOL bar and the match.
         B_OWN     equal-weight of THE PANEL'S OWN k names (seed-specific).  The strictest
                   reading: did the book beat the basket it was drawn from?
    2. q in {0.25, 0.50, 0.75} - the small-cap share, idea 310's own stratum variable.

k (20/40/80) and book (EWall/CAND10/CAND20) are INHERITED from idea 310's committed corpus, not
tuned here; the rule-8 gross is chosen inside the walk-forward and nowhere else.

4b is PROTOCOL rule 4b verbatim, with the benchmark swapped for the comparand under test:
    H1 > bm.H1  AND  H2 > bm.H2  AND  OOS_Sharpe > bm.OOS_Sharpe
    AND |MaxDD| <= 0.60*|bm.MaxDD|  AND  CAGR >= 0.70*bm.CAGR
4a is unchanged (its comparand is RULES v2, not SPY) and is reported as a control that must not
move.

Pre-registered gates, written before any survivor count was read
---------------------------------------------------------------
G1  WINDOW / SPY REPRODUCTION.  This run's SPY row, rebuilt on idea 310's own calendar and
    window, must restate the committed `spy_Sharpe` / `spy_CAGR` / `spy_MaxDD` /
    `spy_OOS_Sharpe` columns to < 1e-9.
G2  4b REPRODUCTION.  Scoring the committed 1,620 cells' own published metrics under B_SPY must
    reproduce idea 310-B's published counts EXACTLY: 4b 46/1620 with 41/5/0 by q, 4a 0/1620,
    and the published `fails4b` token set on every row.
G3  BLEND IS REALLY CAP-MATCHED.  B_MATCH at q=0 must equal B_LARGE and at q=1 must equal
    B_SMALL to < 1e-12, and the blend weights must sum to 1 at every q.
G4  THE BENCHMARKS ARE DISTINCT BOOKS.  Pairwise |dSharpe| between B_SPY, B_LARGE, B_SMALL must
    each exceed 0.01, else the contrast under test does not exist.

B1  IS THE FOOTPRINT A COMPARAND FACT?  PASS (comparand fact) iff the 41 q=0.25 passers do NOT
    survive B_MATCH at the same rate they survive B_SPY.  A footprint that survives cap-matching
    unchanged is a PANEL fact and the queue's premise is wrong.
B2  DOES THE GRADIENT REVERSE, VANISH, OR HOLD?  No bar - the per-q pass rate under each
    benchmark IS the answer, reported in full.
B3  WHAT DOES THE STRICTEST BAR SAY?  The B_OWN count: how many of the 1,620 books beat the
    equal-weight basket of their own names on all five 4b legs.

RULE 8 (mandatory).  A FRESH, DISJOINT seed block (seeds 300-319; idea 293 used 0-29 and idea
310-B used 100-159) x q in {0.25,0.50,0.75} x k=40, the band book at gross {0.50,0.75,1.00}.
Gross is chosen on IS Sharpe <= 2016-12-31 ALONE, pooled within a q, and 2017-01-01+ is read
ONCE.  OOS CAGR / Sharpe / MaxDD are reported against RULES v2 and SPY on the same calendar, and
4b is scored under BOTH B_SPY and B_MATCH.  This asks whether the comparand swap changes a
FRESH decision, not only a retrospective census.

CAVEATS.  (i) SURVIVORSHIP (idea 54): both pools are current constituents with no delistings.
The small pool is the sub-$2B screen minus the 44 names with max_1d_move >= 1.0 per PROTOCOL.
This bias is LARGER for the small pool than the large one, so B_SMALL - and therefore B_MATCH at
high q - is the MORE inflated bar: **any "the books fail the matched bar" finding is
conservative, and any "the books beat it" finding is not.**  (ii) The benchmarks are index
conventions, not tradable books: they are computed at 0 bps, so the books (at 10 bps) are being
held to a costless bar.  That too is conservative for a KILL and generous for a KEEP; a 10-bps
variant of every benchmark is reported beside the headline.  (iii) B_OWN peeks at the panel's
own draw and is therefore the strictest bar available, not a deployable one.  (iv) Six readings
of one corpus are not six independent pieces of evidence.
"""
import sys, json, time, zlib
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state                # noqa
from engine import metrics, rebalance_mask                                      # noqa

OUT = Path(str(__file__)[:-3])          # NB: the slug contains "0.25", so Path.with_suffix
                                        # would truncate at that dot -- build names by hand.
def out_path(ext): return Path(str(OUT) + ext)
REF310 = (REPO / "research" / "backtests" /
          "2026-09-09_is-EVOL-the-real-survivor-not-DISP_B.keeppaths.csv")
COST_BPS, FREQ, GROSS, BAND_V2 = 10, "W", 0.75, 0.03
QS = [0.250, 0.500, 0.750]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BENCHES = ["B_SPY", "B_LARGE", "B_SMALL", "B_MATCH", "B_HALF", "B_OWN"]
WF_SEED0, WF_NSEED, WF_K = 300, 20, 40
WF_GROSS = [0.50, 0.75, 1.00]
TOL, TOL_TIGHT = 1e-9, 1e-12

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def flush_log(): out_path(".console.txt").write_text("\n".join(LOG) + "\n")


# ------------------------------------------------------------------ machinery (record's own)
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return (pd.Series(pr - turn * cost_bps / 1e4, index=prices.index),
            pd.Series(turn, index=prices.index))


def stat_block(r):
    """idea 310-B's stat_block, verbatim."""
    h = len(r) // 2
    m = metrics(r)
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
               H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
    out["IS_Sharpe"] = metrics(ris)["Sharpe"] if len(ris) > 60 else np.nan
    mo = metrics(ros) if len(ros) > 60 else dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    out["OOS_CAGR"], out["OOS_Sharpe"], out["OOS_MaxDD"] = mo["CAGR"], mo["Sharpe"], mo["MaxDD"]
    return out


def fails4b(row, bm):
    """PROTOCOL 4b's five legs, in idea 310-B's own order and wording."""
    f = []
    if not row["H1"] > bm["H1"]: f.append("H1")
    if not row["H2"] > bm["H2"]: f.append("H2")
    if not row["OOS_Sharpe"] > bm["OOS_Sharpe"]: f.append("OOS")
    if not abs(row["MaxDD"]) <= 0.60 * abs(bm["MaxDD"]): f.append("DD")
    if not row["CAGR"] >= 0.70 * bm["CAGR"]: f.append("CAGR")
    return f


def draw_panel(pxs_c, pxb_c, small_pool, large_pool, q, k, sd):
    """idea 310-B's draw_panel VERBATIM (seed key STRAT|{q:.3f}|{sd}, k absent)."""
    n_s = int(round(q * k)); n_l = k - n_s
    seed = zlib.crc32(f"STRAT|{q:.3f}|{sd}".encode()) % (2 ** 32)
    rng = np.random.default_rng(seed)
    sc = sorted(rng.choice(small_pool, size=n_s, replace=False).tolist()) if n_s else []
    lc = sorted(rng.choice(large_pool, size=n_l, replace=False).tolist()) if n_l else []
    parts = []
    if lc: parts.append(pxb_c[lc])
    if sc: parts.append(pxs_c[sc])
    px = pd.concat(parts + [pxb_c["SPY"].rename("SPY")], axis=1).dropna(how="all").ffill()
    return px, set(sc) | set(lc)


def ew_index(px, cols, cost_bps=0.0, drift=False):
    """Equal-weight index over `cols`.  drift=False -> daily-rebalanced fixed weights (the
    standard EW-index convention); drift=True -> buy-and-hold from the first day."""
    sub = px[list(cols)]
    r = sub.pct_change().fillna(0.0)
    live = sub.notna() & sub.shift(1).notna()
    if not drift:
        w = live.astype(float)
        w = w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        out = (r * w).sum(axis=1)
        turn = w.diff().abs().sum(axis=1).fillna(0.0)
        return out - turn * cost_bps / 1e4
    eq = (1.0 + r.where(live, 0.0)).cumprod()
    tot = eq.mean(axis=1)
    return tot.pct_change().fillna(0.0)


def blend(series_map, weights):
    """Fixed-weight daily-rebalanced blend of benchmark return series."""
    out = None
    for k, w in weights.items():
        s = series_map[k] * w
        out = s if out is None else out + s
    return out


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 548  is the q=0.25 4b FOOTPRINT a PANEL fact or a SPY-COMPARAND fact?")
    P("cloud lane, 2026-09-11.  q = the SMALL-CAP SHARE of the panel (idea 310's own variable).")
    P("two tuned parameters: BENCHMARK BLEND (6 definitions) x q (3 levels). every grid point")
    P("published; k and book inherited from idea 310's corpus; gross chosen only inside rule 8.")
    P("=" * 100)
    P("pre-registered gates:")
    P(f"  G1 WINDOW/SPY   this run's SPY row restates idea 310-B's committed spy_* to < {TOL}")
    P("  G2 4b REPRO     the committed 1,620 cells under B_SPY reproduce 46/1620 (41/5/0 by q),")
    P("                  4a 0/1620, and the published `fails4b` token set on EVERY row")
    P(f"  G3 CAP-MATCHED  B_MATCH(q=0)==B_LARGE and B_MATCH(q=1)==B_SMALL to < {TOL_TIGHT}")
    P("  G4 DISTINCT     pairwise |dSharpe| among B_SPY / B_LARGE / B_SMALL each > 0.01")
    P("  B1 COMPARAND?   PASS iff the q=0.25 passers do NOT survive B_MATCH at the B_SPY rate")
    P("  B2 GRADIENT     no bar - the per-q pass rate under each benchmark is the answer")
    P("  B3 STRICTEST    the B_OWN count (beat the basket you were drawn from)")
    flush_log()

    # ---------------------------------------------------------------- sources (310-B verbatim)
    pxs, px136 = load_universe(small=True), load_universe(broad=True)
    etf36 = set(json.loads((REPO / "research" / "universe.json").read_text()).get("etf", []))
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in etf36 and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    idx = pxs.index.intersection(px136.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), px136.reindex(idx).ffill()
    small_pool, large_pool = np.array(sorted(s_stk)), np.array(sorted(b_stk))
    P(f"\nsources: LARGE pool {len(large_pool)} stocks, SMALL pool {len(small_pool)} stocks "
      f"({len(bad)} dropped for max_1d_move >= 1.0); common calendar {idx[0].date()}.."
      f"{idx[-1].date()} ({len(idx)} days)")

    # the panels all share one calendar, so one window serves every cell (idea 310-B line 306)
    px0, _ = draw_panel(pxs_c, pxb_c, small_pool, large_pool, 0.25, 20, 100)
    start = px0.index[260]
    P(f"evaluation window: {start.date()} .. {px0.index[-1].date()} "
      f"({len(px0.loc[start:])} days), from px.index[260] as idea 310-B does")
    flush_log()

    # ---------------------------------------------------------------- the benchmark library
    P("\n" + "=" * 100)
    P("PARAM 1: THE BENCHMARK LIBRARY (6 definitions, 0 bps; a 10-bps variant reported beside)")
    P("=" * 100)
    spy_r = pxb_c["SPY"].pct_change().fillna(0.0)
    base = {
        "SPY":   spy_r,
        "LARGE": ew_index(pxb_c, large_pool),
        "SMALL": ew_index(pxs_c, small_pool),
    }
    base10 = {
        "SPY":   spy_r,                                    # single asset, buy-and-hold: no cost
        "LARGE": ew_index(pxb_c, large_pool, cost_bps=10.0),
        "SMALL": ew_index(pxs_c, small_pool, cost_bps=10.0),
    }
    base_drift = {
        "SPY":   spy_r,
        "LARGE": ew_index(pxb_c, large_pool, drift=True),
        "SMALL": ew_index(pxs_c, small_pool, drift=True),
    }

    def bench_stats(bm_base, q):
        BM = {}
        BM["B_SPY"]   = stat_block(bm_base["SPY"].loc[start:])
        BM["B_LARGE"] = stat_block(bm_base["LARGE"].loc[start:])
        BM["B_SMALL"] = stat_block(bm_base["SMALL"].loc[start:])
        m = blend(bm_base, {"SMALL": q, "LARGE": 1.0 - q})
        BM["B_MATCH"] = stat_block(m.loc[start:])
        h = blend({"SPY": bm_base["SPY"], "M": m}, {"SPY": 0.5, "M": 0.5})
        BM["B_HALF"] = stat_block(h.loc[start:])
        return BM

    BMQ = {q: bench_stats(base, q) for q in QS}
    BMQ10 = {q: bench_stats(base10, q) for q in QS}
    BMQD = {q: bench_stats(base_drift, q) for q in QS}
    P(f"  {'q':>5} {'benchmark':10} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>9} {'H1':>8} {'H2':>8} "
      f"{'oSharpe':>8} | {'4b CAGR floor':>13} {'4b DD cap':>10}")
    brows = []
    for q in QS:
        for b in ["B_SPY", "B_LARGE", "B_SMALL", "B_MATCH", "B_HALF"]:
            c = BMQ[q][b]
            P(f"  {q:5.2f} {b:10} {c['CAGR']:8.4f} {c['Sharpe']:8.4f} {c['MaxDD']:9.4f} "
              f"{c['H1']:8.4f} {c['H2']:8.4f} {c['OOS_Sharpe']:8.4f} | "
              f"{0.70*c['CAGR']:13.4f} {-0.60*abs(c['MaxDD']):10.4f}")
            brows.append(dict(q=q, bench=b, variant="0bps", **c))
        for b in ["B_LARGE", "B_SMALL", "B_MATCH", "B_HALF"]:
            brows.append(dict(q=q, bench=b, variant="10bps", **BMQ10[q][b]))
            brows.append(dict(q=q, bench=b, variant="drift", **BMQD[q][b]))
    pd.DataFrame(brows).to_csv(out_path(".benchmarks.csv"), index=False)
    flush_log()

    # G3 / G4
    m0 = stat_block(blend(base, {"SMALL": 0.0, "LARGE": 1.0}).loc[start:])
    m1 = stat_block(blend(base, {"SMALL": 1.0, "LARGE": 0.0}).loc[start:])
    d0 = max(abs(m0[k] - BMQ[0.25]["B_LARGE"][k]) for k in ["CAGR", "Sharpe", "MaxDD", "H1", "H2"])
    d1 = max(abs(m1[k] - BMQ[0.25]["B_SMALL"][k]) for k in ["CAGR", "Sharpe", "MaxDD", "H1", "H2"])
    G3 = d0 < TOL_TIGHT and d1 < TOL_TIGHT
    P(f"\n  G3 CAP-MATCHED: |B_MATCH(0) - B_LARGE| {d0:.3e}, |B_MATCH(1) - B_SMALL| {d1:.3e} "
      f"vs bar {TOL_TIGHT} -> {'PASS' if G3 else 'FAIL'}")
    pairs = [("B_SPY", "B_LARGE"), ("B_SPY", "B_SMALL"), ("B_LARGE", "B_SMALL")]
    dmin = min(abs(BMQ[0.25][a]["Sharpe"] - BMQ[0.25][b]["Sharpe"]) for a, b in pairs)
    G4 = dmin > 0.01
    P("  G4 DISTINCT: " + ", ".join(
        f"|{a}-{b}| {abs(BMQ[0.25][a]['Sharpe']-BMQ[0.25][b]['Sharpe']):.4f}" for a, b in pairs) +
      f" -> min {dmin:.4f} vs bar 0.01 -> {'PASS' if G4 else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------------------- G1 SPY reproduction
    K = pd.read_csv(REF310)
    P("\n" + "=" * 100)
    P("G1 WINDOW / SPY REPRODUCTION against idea 310-B's committed keeppaths.csv")
    P("=" * 100)
    sp = BMQ[0.25]["B_SPY"]
    ref = K[["spy_Sharpe", "spy_CAGR", "spy_MaxDD", "spy_OOS_Sharpe"]].drop_duplicates()
    assert len(ref) == 1, f"committed spy columns are not unique ({len(ref)} rows)"
    r0 = ref.iloc[0]
    g1 = {"Sharpe": abs(sp["Sharpe"] - r0.spy_Sharpe), "CAGR": abs(sp["CAGR"] - r0.spy_CAGR),
          "MaxDD": abs(sp["MaxDD"] - r0.spy_MaxDD),
          "OOS_Sharpe": abs(sp["OOS_Sharpe"] - r0.spy_OOS_Sharpe)}
    for k, v in g1.items():
        P(f"  {k:11} this run {sp[k if k!='OOS_Sharpe' else 'OOS_Sharpe']:.10f} vs committed "
          f"{float(r0['spy_'+('OOS_Sharpe' if k=='OOS_Sharpe' else k)]):.10f}  |d| {v:.3e}")
    G1 = max(g1.values()) < TOL
    P(f"  G1: max |d| {max(g1.values()):.3e} vs bar {TOL} -> {'PASS' if G1 else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------------------- B_OWN (seed-specific)
    P("\n" + "=" * 100)
    P("B_OWN: the equal-weight basket of EACH panel's OWN k names (540 panels)")
    P("=" * 100)
    OWN = {}
    for key in K["panel"].unique():
        k_, q_, s_ = key.split("~")
        k_i, q_f, sd = int(k_[1:]), float(q_[1:]), int(s_[1:])
        px, tr = draw_panel(pxs_c, pxb_c, small_pool, large_pool, q_f, k_i, sd)
        OWN[key] = stat_block(ew_index(px, sorted(tr)).loc[start:])
    P(f"  built {len(OWN)} own-basket benchmarks ({time.time()-t0:.0f}s)")
    ow = pd.DataFrame([dict(panel=k, **v) for k, v in OWN.items()])
    ow.to_csv(out_path(".ownbaskets.csv"), index=False)
    P(f"  B_OWN Sharpe by q: " + ", ".join(
        f"q{q:.2f} mean {ow[ow.panel.str.contains(f'~q{q:.3f}~')].Sharpe.mean():.4f}" for q in QS))
    flush_log()

    # ---------------------------------------------------------------- G2 + the census
    P("\n" + "=" * 100)
    P("G2 4b REPRODUCTION, then the census: all 1,620 committed cells x 6 benchmarks")
    P("=" * 100)
    rows = []
    n_tok_ok = 0
    for r in K.itertuples():
        row = dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                   OOS_Sharpe=r.OOS_Sharpe)
        rec = dict(panel=r.panel, k=r.k, q=r.q, book=r.book, CAGR=r.CAGR, Sharpe=r.Sharpe,
                   MaxDD=r.MaxDD, H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe,
                   pub_keep4b=bool(r.keep4b), pub_keep4a=bool(r.keep4a))
        for b in BENCHES:
            bm = OWN[r.panel] if b == "B_OWN" else BMQ[r.q][b]
            f = fails4b(row, bm)
            rec[f"p4b_{b}"] = (len(f) == 0)
            rec[f"fail_{b}"] = ",".join(f) if f else "-"
        # G2 token check against the committed column
        if rec["fail_B_SPY"] == str(r.fails4b): n_tok_ok += 1
        rows.append(rec)
    D = pd.DataFrame(rows)
    n_spy = int(D.p4b_B_SPY.sum())
    byq = D.groupby("q").p4b_B_SPY.sum()
    g2_counts = (n_spy == 46 and int(byq.get(0.25, 0)) == 41 and int(byq.get(0.50, 0)) == 5
                 and int(byq.get(0.75, 0)) == 0 and int(D.pub_keep4a.sum()) == 0)
    g2_tok = n_tok_ok == len(D)
    G2 = g2_counts and g2_tok
    P(f"  under B_SPY: 4b {n_spy}/1620 (committed 46), by q "
      f"{int(byq.get(0.25,0))}/{int(byq.get(0.50,0))}/{int(byq.get(0.75,0))} (committed 41/5/0); "
      f"4a {int(D.pub_keep4a.sum())}/1620 (committed 0)")
    P(f"  published `fails4b` token set reproduced on {n_tok_ok}/{len(D)} rows")
    P(f"  keep4b column agrees with this run's B_SPY scoring on "
      f"{int((D.p4b_B_SPY == D.pub_keep4b).sum())}/{len(D)} rows")
    P(f"  G2: {'PASS' if G2 else 'FAIL'} (counts {'ok' if g2_counts else 'FAIL'}, "
      f"tokens {'ok' if g2_tok else 'FAIL'})")
    D.to_csv(out_path(".census.csv"), index=False)
    flush_log()

    # ---------------------------------------------------------------- PARAM 1 x PARAM 2 grid
    P("\n" + "=" * 100)
    P("THE GRID (param 1 x param 2): 4b pass count by BENCHMARK x q, all 18 cells reported")
    P("=" * 100)
    P(f"  {'benchmark':10} " + " ".join(f"{'q'+format(q,'.2f'):>10}" for q in QS) +
      f" {'ALL':>8} {'rate':>8}")
    grid = []
    for b in BENCHES:
        per = D.groupby("q")[f"p4b_{b}"].sum()
        tot = int(D[f"p4b_{b}"].sum())
        P(f"  {b:10} " + " ".join(f"{int(per.get(q,0)):10d}" for q in QS) +
          f" {tot:8d} {tot/len(D):8.2%}")
        for q in QS:
            grid.append(dict(bench=b, q=q, n=int(per.get(q, 0)), of=int((D.q == q).sum())))
    pd.DataFrame(grid).to_csv(out_path(".grid.csv"), index=False)

    P("\n  SURVIVAL of idea 310's 46 B_SPY passers under each benchmark:")
    pas = D[D.p4b_B_SPY]
    P(f"  {'benchmark':10} {'survivors':>10} {'of 46':>7} {'rate':>8} | "
      + " ".join(f"{'q'+format(q,'.2f'):>8}" for q in QS))
    surv = []
    for b in BENCHES:
        s = int(pas[f"p4b_{b}"].sum())
        per = pas.groupby("q")[f"p4b_{b}"].sum()
        P(f"  {b:10} {s:10d} {len(pas):7d} {s/max(len(pas),1):8.1%} | " +
          " ".join(f"{int(per.get(q,0)):8d}" for q in QS))
        surv.append(dict(bench=b, survivors=s, of=len(pas)))
    pd.DataFrame(surv).to_csv(out_path(".survival.csv"), index=False)

    s_match = int(pas.p4b_B_MATCH.sum())
    B1 = s_match < len(pas)
    P(f"\n  B1: {s_match} of {len(pas)} B_SPY passers survive the CAP-MATCHED bar -> "
      f"{'PASS - the footprint is (at least partly) a COMPARAND fact' if B1 else 'FAIL - it survives cap-matching, so it is a PANEL fact'}")
    P(f"  B3: B_OWN (beat the equal-weight basket of your own names) passes "
      f"{int(D.p4b_B_OWN.sum())}/1620 = {D.p4b_B_OWN.mean():.2%}")

    P("\n  WHICH 4b LEG BINDS, by benchmark (first-listed failing leg, all 1,620 cells):")
    P(f"  {'benchmark':10} " + " ".join(f"{l:>7}" for l in ["H1", "H2", "OOS", "DD", "CAGR"]) +
      f" {'none':>7}")
    for b in BENCHES:
        cnt = {l: 0 for l in ["H1", "H2", "OOS", "DD", "CAGR"]}
        none = 0
        for v in D[f"fail_{b}"]:
            if v == "-": none += 1
            else: cnt[v.split(",")[0]] += 1
        P(f"  {b:10} " + " ".join(f"{cnt[l]:7d}" for l in ["H1", "H2", "OOS", "DD", "CAGR"]) +
          f" {none:7d}")
    flush_log()

    P("\n  ROBUSTNESS: the same survival count under a 10-bps and a buy-and-hold (drifting)")
    P("  reading of the SAME benchmarks (the books stay at 10 bps throughout):")
    P(f"  {'benchmark':10} {'0bps':>8} {'10bps':>8} {'drift':>8}   (survivors of the 46)")
    rob = []
    for b in ["B_LARGE", "B_SMALL", "B_MATCH", "B_HALF"]:
        c = {}
        for tag, LIBQ in (("0bps", BMQ), ("10bps", BMQ10), ("drift", BMQD)):
            n = 0
            for r in pas.itertuples():
                row = dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                           OOS_Sharpe=r.OOS_Sharpe)
                if not fails4b(row, LIBQ[r.q][b]): n += 1
            c[tag] = n
        P(f"  {b:10} {c['0bps']:8d} {c['10bps']:8d} {c['drift']:8d}")
        rob.append(dict(bench=b, **c))
    pd.DataFrame(rob).to_csv(out_path(".robustness.csv"), index=False)
    flush_log()

    # ---------------------------------------------------------------- RULE 8 WALK-FORWARD
    P("\n" + "=" * 100)
    P(f"RULE 8 WALK-FORWARD - FRESH, DISJOINT seed block (seeds {WF_SEED0}-{WF_SEED0+WF_NSEED-1};")
    P("  idea 293 used 0-29 and idea 310-B used 100-159).  k=40, band book, gross ladder.")
    P(f"  gross chosen on IS Sharpe <= {IS_END} ALONE (pooled within a q); {OOS_START}+ read ONCE.")
    P("=" * 100)
    warms = []
    for q in QS:
        for sd in range(WF_SEED0, WF_SEED0 + WF_NSEED):
            px, tr = draw_panel(pxs_c, pxb_c, small_pool, large_pool, q, WF_K, sd)
            inv = [c for c in px.columns if c in tr]
            for g in WF_GROSS:
                e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
                for c in inv: e[c] = px[c].notna().astype(float)
                ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
                w = ew.where(band_state(px, BAND_V2), 0.0)
                r, _ = fast_backtest(px, w, COST_BPS, FREQ)
                warms.append(dict(q=q, seed=sd, gross=g, **stat_block(r.loc[start:])))
        P(f"    q={q:.2f} done ({time.time()-t0:.0f}s)")
        flush_log()
    A = pd.DataFrame(warms)
    A.to_csv(out_path(".wfarms.csv"), index=False)
    P(f"\n  the fresh grid: {len(A)} arms = 3 q x {WF_NSEED} seeds x {len(WF_GROSS)} gross, "
      "every point in .wfarms.csv.  IS Sharpe by (q, gross), the SELECTION table:")
    P(f"  {'q':>5} " + " ".join(f"{'g'+format(g,'.2f'):>9}" for g in WF_GROSS) + "   pick")
    picks = {}
    for q in QS:
        mm = A[A.q == q].groupby("gross").IS_Sharpe.mean()
        pick = float(mm.idxmax()); picks[q] = pick
        P(f"  {q:5.2f} " + " ".join(f"{mm.get(g, np.nan):9.4f}" for g in WF_GROSS) +
          f"   g={pick:.2f}")

    # the record's own comparands on the same calendar
    v2_r, _ = fast_backtest(pxb_c, rules_v2_weights(pxb_c), COST_BPS, FREQ)
    V2 = stat_block(v2_r.loc[start:])
    SPY = BMQ[0.25]["B_SPY"]
    P(f"\n  comparands, same calendar and window: RULES v2 (B136) CAGR {V2['CAGR']:.2%} "
      f"Sharpe {V2['Sharpe']:.4f} MaxDD {V2['MaxDD']:.2%} OOS Sharpe {V2['OOS_Sharpe']:.4f};  "
      f"SPY CAGR {SPY['CAGR']:.2%} Sharpe {SPY['Sharpe']:.4f} MaxDD {SPY['MaxDD']:.2%} "
      f"OOS Sharpe {SPY['OOS_Sharpe']:.4f}")

    P(f"\n  OOS, read ONCE at the chosen gross ({WF_NSEED} seeds per q, every seed scored):")
    P(f"  {'q':>5} {'pick':>6} {'oCAGR':>8} {'oSharpe':>8} {'oMaxDD':>8} | {'4b SPY':>8} "
      f"{'4b MATCH':>9} {'4b OWN':>8} | {'>v2 oS':>7} {'>SPY oS':>8}")
    wf = []
    for q in QS:
        sub = A[(A.q == q) & (A.gross == picks[q])]
        n4s = n4m = n4o = nv2 = nspy = 0
        for r in sub.itertuples():
            row = dict(CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                       OOS_Sharpe=r.OOS_Sharpe)
            key = f"k{WF_K}~q{q:.3f}~s{r.seed}"
            px, tr = draw_panel(pxs_c, pxb_c, small_pool, large_pool, q, WF_K, r.seed)
            own = stat_block(ew_index(px, sorted(tr)).loc[start:])
            n4s += not fails4b(row, BMQ[q]["B_SPY"])
            n4m += not fails4b(row, BMQ[q]["B_MATCH"])
            n4o += not fails4b(row, own)
            nv2 += r.OOS_Sharpe > V2["OOS_Sharpe"]
            nspy += r.OOS_Sharpe > SPY["OOS_Sharpe"]
        P(f"  {q:5.2f} {picks[q]:6.2f} {sub.OOS_CAGR.mean():8.4f} {sub.OOS_Sharpe.mean():8.4f} "
          f"{sub.OOS_MaxDD.mean():8.4f} | {n4s:3d}/{len(sub):<4d} {n4m:4d}/{len(sub):<4d} "
          f"{n4o:3d}/{len(sub):<4d} | {nv2:3d}/{len(sub):<3d} {nspy:4d}/{len(sub):<3d}")
        wf.append(dict(q=q, gross=picks[q], n=len(sub), oCAGR=sub.OOS_CAGR.mean(),
                       oSharpe=sub.OOS_Sharpe.mean(), oMaxDD=sub.OOS_MaxDD.mean(),
                       CAGR=sub.CAGR.mean(), Sharpe=sub.Sharpe.mean(), MaxDD=sub.MaxDD.mean(),
                       p4b_SPY=n4s, p4b_MATCH=n4m, p4b_OWN=n4o, beats_v2_oos=nv2,
                       beats_spy_oos=nspy, v2_oSharpe=V2["OOS_Sharpe"],
                       spy_oSharpe=SPY["OOS_Sharpe"], spy_CAGR=SPY["CAGR"],
                       spy_MaxDD=SPY["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(out_path(".walkforward.csv"), index=False)
    tot = int(W.n.sum())
    P(f"\n  fresh-block totals: 4b under SPY {int(W.p4b_SPY.sum())}/{tot}, under the CAP-MATCHED "
      f"bar {int(W.p4b_MATCH.sum())}/{tot}, under the OWN basket {int(W.p4b_OWN.sum())}/{tot}; "
      f"beats RULES v2 OOS {int(W.beats_v2_oos.sum())}/{tot}, beats SPY OOS "
      f"{int(W.beats_spy_oos.sum())}/{tot}")
    P(f"  the fresh block {'REPRODUCES' if int(W.p4b_SPY.sum()) > int(W.p4b_MATCH.sum()) else 'DOES NOT REPRODUCE'} "
      "the census direction out of sample.")
    flush_log()

    # ---------------------------------------------------------------- both KEEP paths
    P("\n" + "=" * 100)
    P("BOTH KEEP PATHS")
    P("=" * 100)
    P(f"  4a: {int(D.pub_keep4a.sum())}/1620 on the committed corpus - UNCHANGED by this run, "
      "and unchangeable: 4a's comparand is RULES v2, not SPY, so no benchmark swap touches it.")
    P(f"  4b on the committed corpus: B_SPY {int(D.p4b_B_SPY.sum())}/1620, B_LARGE "
      f"{int(D.p4b_B_LARGE.sum())}, B_SMALL {int(D.p4b_B_SMALL.sum())}, B_MATCH "
      f"{int(D.p4b_B_MATCH.sum())}, B_HALF {int(D.p4b_B_HALF.sum())}, B_OWN "
      f"{int(D.p4b_B_OWN.sum())}")
    P(f"  4b on the fresh rule-8 block: B_SPY {int(W.p4b_SPY.sum())}/{tot}, B_MATCH "
      f"{int(W.p4b_MATCH.sum())}/{tot}, B_OWN {int(W.p4b_OWN.sum())}/{tot}")
    P("  NO KEEP-CANDIDATE IS CLAIMED and no memo is written: every 4b passer here is a random "
      "seed panel, not a rule, and 4a is 0 everywhere.")

    P("\nGATES: G1 %s | G2 %s | G3 %s | G4 %s | B1 %s" %
      tuple("PASS" if x else "FAIL" for x in (G1, G2, G3, G4, B1)))
    summ = dict(G1=G1, G2=G2, G3=G3, G4=G4, B1=B1,
                cells=len(D), spy_4b=n_spy,
                byq_spy={str(q): int(byq.get(q, 0)) for q in QS},
                census={b: dict(total=int(D[f"p4b_{b}"].sum()),
                                byq={str(q): int(D[D.q == q][f"p4b_{b}"].sum()) for q in QS},
                                survivors_of_46=int(pas[f"p4b_{b}"].sum())) for b in BENCHES},
                wf_n=tot, wf_picks={str(q): picks[q] for q in QS},
                wf_4b_spy=int(W.p4b_SPY.sum()), wf_4b_match=int(W.p4b_MATCH.sum()),
                wf_4b_own=int(W.p4b_OWN.sum()),
                wf_beats_v2=int(W.beats_v2_oos.sum()), wf_beats_spy=int(W.beats_spy_oos.sum()),
                keep4a=int(D.pub_keep4a.sum()), runtime_s=round(time.time() - t0, 1))
    out_path(".summary.json").write_text(json.dumps(summ, indent=2, default=str))
    P(f"\nruntime {summ['runtime_s']}s")
    flush_log()
    return summ


if __name__ == "__main__":
    main()
