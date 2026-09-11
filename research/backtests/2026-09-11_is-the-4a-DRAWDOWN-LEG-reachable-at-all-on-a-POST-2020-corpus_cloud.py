#!/usr/bin/env python3
"""Idea 731 — is the 4a DRAWDOWN leg reachable at all on a POST-2020 corpus?

Idea 727's fresh 162-book corpus passes PROTOCOL rule 4a at 1/162 (0.62%) WIDE and
0/108 NARROW, against idea 721's 3.17% on 126 books.  The queue's reading is that the
record's 4a base rate is falling *as the live book's own MaxDD improves* -- i.e. the
binding quantity is a property of the COMPARAND, not of the candidate book.  This
script measures the 4a rate as a function of the comparand's drawdown.

METHOD
  Corpus: 162 price-only books = 3 panels x 54 books.  Per panel, families
    CAND n  -- top-n by baseline.score composite among names inside the 200d +/-3% band
    IVOL n  -- n lowest 20d-vol names inside the same band
    EWALL   -- every in-band name (== baseline.rules_v2_weights)
  with n in {10,20,30,40}, gross g in {0.50,0.75,1.00}, cadence in {W,M}.  All books
  DE-GROSS (gated-out weight goes to cash, never re-spread), matching RULES v2.

  Comparand LADDER (the x-axis, not a tuned parameter): RULES v2 at gross
  0.10/0.25/0.40/0.50/0.60/0.75/0.90/1.00 on the same panel and calendar, weekly.
  De-grossing makes MaxDD roughly linear in gross, so the ladder sweeps comparand
  drawdown from ~-3% to ~-30% while holding the comparand's SIGNAL fixed.  RULES v1
  and SPY are carried as two further (off-ladder) comparand points.

  TUNED PARAMETERS (exactly 2, both reported at every grid point):
    P1 window in {FULL, POST2020}   P2 panel in {U56, B136, SMALL439}

  4a leg (PROTOCOL rule 4): Sharpe > comparand in BOTH halves AND MaxDD no worse than
  the comparand.  The two legs are scored SEPARATELY as well as jointly, because the
  whole question is which leg binds.
  4b leg: Sharpe > SPY in both halves and OOS, MaxDD <= 60% of SPY's, CAGR >= 70%.

  RULE 8 walk-forward: every selector reads ONLY 2009-2016 (SMALL: 2010-2016), picks
  one book, and that book is read ONCE on 2017-01-01 onward against RULES v2 and SPY.

COSTS 10 bps/unit turnover, weights at t decided, applied t+1 (engine convention).
SURVIVORSHIP: all three panels are CURRENT constituent lists (idea 54).  Pass-rate
LEVELS are therefore optimistic; the bias runs against 4a's reachability, not for it.
Deterministic; no network; no RULES/PROTOCOL/scan/bot/baseline edits.
"""
import sys, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, band_state, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask  # noqa

STEM = Path(__file__).with_suffix("")
COST = 10.0
OOS_START = pd.Timestamp("2017-01-01")
PANELS = ["U56", "B136", "SMALL439"]
WINDOWS = ["FULL", "POST2020"]
GROSS = [0.50, 0.75, 1.00]
NS = [10, 20, 30, 40]
CADENCE = ["W", "M"]
LADDER = [0.10, 0.25, 0.40, 0.50, 0.60, 0.75, 0.90, 1.00]

# ---------------------------------------------------------------- fast backtest
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Numpy re-implementation of engine.backtest (gated below at 0.0 tolerance)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); held = np.empty_like(rets); turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=prices.index)

def met(r):
    if len(r) < 30: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    dd = (eq / eq.cummax() - 1).min(); vol = r.std() * np.sqrt(252)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1, MaxDD=dd,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan)

def halves(r):
    h = len(r) // 2
    return met(r.iloc[:h])["Sharpe"], met(r.iloc[h:])["Sharpe"]

def stats(r):
    m = met(r); h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)

# ---------------------------------------------------------------- books
def w_ewall(px, g, band=0.03):
    return rules_v2_weights(px, band=band, gross=g)

def _topn_from(rankable, inband, px, n, g, ascending):
    """Top-n by `rankable` among in-band names; g/n each; de-gross (no re-spread)."""
    elig = rankable.where(inband & px.notna())
    rk = elig.rank(axis=1, ascending=ascending)
    return (rk <= n).astype(float) * (g / n)

def build_books(px):
    """dict name -> weights DataFrame builder (lazy: returns callables)."""
    s, _, vol20 = score(px, vol_scale=True)
    inband = band_state(px, 0.03)
    out = {}
    for g in GROSS:
        for c in CADENCE:
            out[f"EWALL|g{g:.2f}|{c}"] = (lambda g=g: w_ewall(px, g), c)
            for n in NS:
                out[f"CAND{n}|g{g:.2f}|{c}"] = (lambda n=n, g=g: _topn_from(s, inband, px, n, g, False), c)
                out[f"IVOL{n}|g{g:.2f}|{c}"] = (lambda n=n, g=g: _topn_from(vol20, inband, px, n, g, True), c)
    return out

def load_panel(tag):
    if tag == "U56":  return load_universe()
    if tag == "B136": return load_universe(broad=True)
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    tcol = [c for c in meta.columns if c.lower() in ("ticker", "symbol")][0]
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, tcol].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"  SMALL: dropped {px.shape[1] - len(keep)} tickers with max_1d_move >= 1.0")
    return px[keep]

def window_slice(r, px, win):
    r = r.loc[px.index[260]:]
    return r if win == "FULL" else r.loc["2020-01-01":]

# ================================================================= GATES
print("=" * 78); print("GATES (pre-registered, printed before any corpus number is read)")
gx = load_universe().iloc[:900]
def _gate(w, freq):
    """engine leaves a NaN prefix before its first rebalance (weights .shift(1) with no
    fill); fast_backtest carries 0.0 there.  Assert the disagreement is CONFINED to that
    prefix and that the two agree EXACTLY from the read window (index[260]) onward."""
    a = engine_backtest(gx, w, cost_bps=COST, freq=freq)["returns"]
    b = fast_backtest(gx, w, COST, freq)
    nan_idx = np.flatnonzero(a.isna().values)
    last = int(nan_idx.max()) if len(nan_idx) else -1
    d = float(np.abs(a.iloc[260:].values - b.iloc[260:].values).max())
    return d, last, len(nan_idx)
g1, p1, k1 = _gate(rules_v2_weights(gx, gross=0.75), "W")
print(f"  G1 fast_backtest == engine.backtest, read window : {g1:.3e}  "
      f"(engine NaN rows: {k1}, last at position {p1} < 260)")
gw2 = _topn_from(score(gx)[0], band_state(gx, 0.03), gx, 20, 0.75, False)
g2, p2, k2 = _gate(gw2, "M")
print(f"  G2 same, ranked book / monthly cadence          : {g2:.3e}  "
      f"(engine NaN rows: {k2}, last at position {p2} < 260)")
assert p1 < 260 and p2 < 260, "engine NaNs reach the read window"
ew = w_ewall(gx, 0.75); v2 = rules_v2_weights(gx, gross=0.75)
g3 = float(np.abs(ew.values - v2.values).max())
print(f"  G3 EWALL(g=0.75) == baseline.rules_v2_weights   : {g3:.3e}")
spy_full = load_universe()["SPY"].pct_change().fillna(0.0)
g4 = met(spy_full.loc[OOS_START:])
print(f"  G4 SPY OOS 2017+ CAGR/Sharpe/MaxDD             : {g4['CAGR']:.2%} / {g4['Sharpe']:.4f} / {g4['MaxDD']:.2%}")
assert g1 < 1e-12 and g2 < 1e-12 and g3 == 0.0, "gate failure"
print("  ALL GATES PASS\n")

# ================================================================= CORPUS
rows, wf_rows = [], []
t0 = time.time()
for panel in PANELS:
    px = load_panel(panel)
    print(f"[{panel}] {px.shape[0]}d x {px.shape[1]}c  {px.index[0].date()}..{px.index[-1].date()}")
    spy = px["SPY"].pct_change().fillna(0.0)
    books = build_books(px)

    # comparand ladder + off-ladder points, returns cached once
    comp_ret = {}
    for g in LADDER:
        comp_ret[f"v2@g{g:.2f}"] = fast_backtest(px, rules_v2_weights(px, gross=g), COST, "W")
    comp_ret["RULESv1"] = fast_backtest(px, rules_v1_weights(px), COST, "W")
    comp_ret["SPY"] = spy

    book_ret = {}
    for name, (mk, cad) in books.items():
        book_ret[name] = fast_backtest(px, mk(), COST, cad)
    print(f"  {len(book_ret)} books, {len(comp_ret)} comparands  ({time.time()-t0:.0f}s)")

    for win in WINDOWS:
        bs = {k: stats(window_slice(v, px, win)) for k, v in book_ret.items()}
        cs = {k: stats(window_slice(v, px, win)) for k, v in comp_ret.items()}
        sp = cs["SPY"]
        for cname, c in cs.items():
            if cname == "SPY" and False: pass
            n4a = nSh = nDD = n4b = 0
            for bname, d in bs.items():
                sh = d["H1"] > c["H1"] and d["H2"] > c["H2"]
                dd = d["MaxDD"] >= c["MaxDD"]           # "no worse" (both negative)
                n4a += sh and dd; nSh += sh; nDD += dd
                n4b += (d["H1"] > sp["H1"] and d["H2"] > sp["H2"]
                        and d["MaxDD"] >= 0.60 * sp["MaxDD"] and d["CAGR"] >= 0.70 * sp["CAGR"])
            rows.append(dict(panel=panel, window=win, comparand=cname,
                             comp_gross=(float(cname.split("g")[1]) if cname.startswith("v2@") else np.nan),
                             comp_MaxDD=c["MaxDD"], comp_Sharpe=c["Sharpe"], comp_CAGR=c["CAGR"],
                             m=len(bs), pass4a=n4a, rate4a=n4a / len(bs),
                             passSharpeLeg=nSh, rateSharpeLeg=nSh / len(bs),
                             passDDleg=nDD, rateDDleg=nDD / len(bs),
                             pass4b_recordreading=n4b, rate4b=n4b / len(bs)))

    # ------------------------------------------------- RULE 8 walk-forward
    is_end = OOS_START - pd.Timedelta(days=1)
    is_b = {k: stats(v.loc[px.index[260]:is_end]) for k, v in book_ret.items()}
    oo_b = {k: stats(v.loc[OOS_START:]) for k, v in book_ret.items()}
    is_c = {k: stats(v.loc[px.index[260]:is_end]) for k, v in comp_ret.items()}
    oo_c = {k: stats(v.loc[OOS_START:]) for k, v in comp_ret.items()}
    live_is, live_oos, spy_oos = is_c["v2@g0.75"], oo_c["v2@g0.75"], oo_c["SPY"]
    sel = {}
    sel["S1_maxISsharpe"] = max(is_b, key=lambda k: is_b[k]["Sharpe"])
    sel["S2_maxISsharpe_among_IS4a"] = max(
        [k for k in is_b if is_b[k]["H1"] > live_is["H1"] and is_b[k]["H2"] > live_is["H2"]
         and is_b[k]["MaxDD"] >= live_is["MaxDD"]] or list(is_b), key=lambda k: is_b[k]["Sharpe"])
    sel["S3_minISmaxdd"] = max(is_b, key=lambda k: is_b[k]["MaxDD"])
    sel["S4_maxIScalmar"] = max(is_b, key=lambda k: is_b[k]["CAGR"] / abs(is_b[k]["MaxDD"]))
    for sname, pick in sel.items():
        o = oo_b[pick]
        wf_rows.append(dict(panel=panel, selector=sname, pick=pick,
                            IS_Sharpe=is_b[pick]["Sharpe"], IS_MaxDD=is_b[pick]["MaxDD"],
                            OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                            v2_OOS_CAGR=live_oos["CAGR"], v2_OOS_Sharpe=live_oos["Sharpe"],
                            v2_OOS_MaxDD=live_oos["MaxDD"],
                            SPY_OOS_CAGR=spy_oos["CAGR"], SPY_OOS_Sharpe=spy_oos["Sharpe"],
                            SPY_OOS_MaxDD=spy_oos["MaxDD"],
                            beats_v2_OOS_Sharpe=o["Sharpe"] > live_oos["Sharpe"],
                            beats_SPY_OOS_Sharpe=o["Sharpe"] > spy_oos["Sharpe"],
                            oos4a=(o["H1"] > live_oos["H1"] and o["H2"] > live_oos["H2"]
                                   and o["MaxDD"] >= live_oos["MaxDD"]),
                            oos4b=(o["H1"] > spy_oos["H1"] and o["H2"] > spy_oos["H2"]
                                   and o["Sharpe"] > spy_oos["Sharpe"]
                                   and o["MaxDD"] >= 0.60 * spy_oos["MaxDD"]
                                   and o["CAGR"] >= 0.70 * spy_oos["CAGR"])))
    del book_ret, comp_ret, books, px

grid = pd.DataFrame(rows); wf = pd.DataFrame(wf_rows)
grid.to_csv(f"{STEM}.grid.csv", index=False)
wf.to_csv(f"{STEM}.walkforward.csv", index=False)

# ================================================================= REPORT
pd.set_option("display.width", 200)
print("\n" + "=" * 78)
print("ALL GRID POINTS — 4a rate as a function of the COMPARAND's drawdown")
print("=" * 78)
for panel in PANELS:
    for win in WINDOWS:
        sub = grid[(grid.panel == panel) & (grid.window == win)].copy()
        print(f"\n--- {panel} / {win}  (m = {int(sub.m.iloc[0])} books) ---")
        show = sub[["comparand", "comp_MaxDD", "comp_Sharpe", "comp_CAGR",
                    "pass4a", "rate4a", "passSharpeLeg", "passDDleg", "pass4b_recordreading"]]
        print(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

lad = grid[grid.comp_gross.notna()]
print("\n" + "=" * 78)
print("LADDER ONLY — is the DD leg the binding one?  (pooled over panels)")
print("=" * 78)
piv = lad.groupby(["window", "comp_gross"]).agg(
    comp_MaxDD=("comp_MaxDD", "mean"), m=("m", "sum"), pass4a=("pass4a", "sum"),
    SharpeLeg=("passSharpeLeg", "sum"), DDleg=("passDDleg", "sum")).reset_index()
piv["rate4a"] = piv.pass4a / piv.m
piv["rateSharpe"] = piv.SharpeLeg / piv.m
piv["rateDD"] = piv.DDleg / piv.m
print(piv.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

# correlation of 4a rate with comparand MaxDD across the ladder
for win in WINDOWS:
    s = lad[lad.window == win]
    r_dd = np.corrcoef(s.comp_MaxDD, s.rate4a)[0, 1]
    r_sh = np.corrcoef(s.comp_MaxDD, s.rateSharpeLeg)[0, 1]
    print(f"\n{win}: corr(comparand MaxDD, 4a rate) = {r_dd:+.4f} ; "
          f"corr(comparand MaxDD, Sharpe-leg rate) = {r_sh:+.4f}   (n={len(s)} ladder cells)")

# feasibility floor implied by each observed rate (idea 727 closed form)
print("\n" + "=" * 78)
print("FEASIBILITY FLOOR m* = ceil(ln 0.05 / ln(1 - p_bar)) implied by each 4a rate")
print("=" * 78)
fl = []
for win in WINDOWS:
    for panel in PANELS + ["POOLED"]:
        s = grid[(grid.window == win) & ((grid.panel == panel) if panel != "POOLED" else True)]
        s = s[s.comparand == "v2@g0.75"]
        k, m = int(s.pass4a.sum()), int(s.m.sum())
        p = k / m
        floor = "INFINITE" if p == 0 else int(np.ceil(np.log(0.05) / np.log(1 - p)))
        fl.append(dict(window=win, panel=panel, k=k, m=m, p_bar=p, FEAS_floor=floor))
fdf = pd.DataFrame(fl); print(fdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
fdf.to_csv(f"{STEM}.floors.csv", index=False)

print("\n" + "=" * 78)
print("RULE 8 WALK-FORWARD — selectors read 2009-2016 only, each pick read ONCE on 2017+")
print("=" * 78)
print(wf[["panel", "selector", "pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
          "v2_OOS_Sharpe", "SPY_OOS_Sharpe", "beats_v2_OOS_Sharpe", "beats_SPY_OOS_Sharpe",
          "oos4a", "oos4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
print(f"\nOOS 4a passes: {int(wf.oos4a.sum())}/{len(wf)}   OOS 4b passes: {int(wf.oos4b.sum())}/{len(wf)}")
print(f"beats RULES v2 OOS Sharpe: {int(wf.beats_v2_OOS_Sharpe.sum())}/{len(wf)}   "
      f"beats SPY OOS Sharpe: {int(wf.beats_SPY_OOS_Sharpe.sum())}/{len(wf)}")
print(f"\nwrote {STEM.name}.grid.csv / .walkforward.csv / .floors.csv   ({time.time()-t0:.0f}s)")
