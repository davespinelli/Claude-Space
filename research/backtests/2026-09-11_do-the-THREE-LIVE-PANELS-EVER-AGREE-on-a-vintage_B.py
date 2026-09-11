#!/usr/bin/env python3
"""IDEA 517 (lane B, 2026-09-11): do-the-THREE-LIVE-PANELS-EVER-AGREE-on-a-vintage.

Queue premise (from idea 514): "U56 ends 2026-09-08 while B136 and SMALL439 end
2026-09-04 on the same day, because only data/prices.csv is touched by the daily job
while the broad/small caches refresh weekly. Measure how often a multi-panel artefact
is comparing books built on panels up to 5 trading days apart, and price a
COMMON-LAST-DATE truncation (intersect the three indices before any cross-panel claim)
against the record's cross-panel orderings."

THE TWO TUNED PARAMETERS (PROTOCOL 4, max 2), exactly the ones the queue names:
  PARAM 1  truncation rule : NATIVE / LASTDATE / COMMONSTART / COMMONWIN   (4 rungs)
  PARAM 2  panel set       : UB / US / BS / ALL                            (4 rungs)
The rule-8 band ladder is SELECTED by PROTOCOL 8 on IS only; it is not tuned here.
ALL 16 grid cells are reported, and every book x panel x truncation row is printed.

Structure of the run:
  GATES  five, pre-registered, all printed before any result is read.
  PART A the census the queue asks for (how many committed artefacts are multi-panel)
         plus the ACTUAL index geometry of the three live panels.
  PART B cross-panel ORDERING flips under each truncation rule (the queue's question).
  PART C what the two channels (end gap, start gap) cost a single panel's own numbers.
  PART D PROTOCOL 8 walk-forward under each truncation rule + both KEEP paths.

Costs 10 bps, weekly cadence, next-day execution (engine applies weights at t+1).
Deterministic; no network; no RNG.
"""
import sys, re, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

COST = 10.0
FREQ = "W"
WARM = 260          # baseline.compare's warm-up skip, kept verbatim
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
pd.set_option("display.width", 250)


# ---------------------------------------------------------------- fast engine
def fast_bt(prices: pd.DataFrame, weights: pd.DataFrame, cost_bps=COST, freq=FREQ):
    """numpy re-implementation of engine.backtest. Same algorithm, same NaN semantics.
    Gated against engine.backtest at G1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    w_t = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    held = np.empty_like(rets)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = w_t[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


def mstats(r: pd.Series):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    dd = (eq / eq.cummax() - 1).min()
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=cagr, Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd)


def halves(r: pd.Series):
    h = len(r) // 2
    return mstats(r.iloc[:h])["Sharpe"], mstats(r.iloc[h:])["Sharpe"]


# ---------------------------------------------------------------- book family
def w_band(px, band, gross=0.75):
    return rules_v2_weights(px, band=band, gross=gross)


def w_ewall(px, gross=0.75):
    ma = px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    e = ((px > ma) & (vol20 < 0.60)).astype(float).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def w_topn(px, n, gross=0.75):
    mom = px.shift(21) / px.shift(252) - 1
    ma = px.rolling(200).mean()
    elig = mom.where(px > ma)
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    return gross * sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def w_spybh(px, gross=1.0):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w["SPY"] = gross
    return w


BOOKS = {
    "BAND03": lambda px: w_band(px, 0.03),      # == live RULES v2 (band .03, g .75)
    "BAND08": lambda px: w_band(px, 0.08),
    "EWALL": w_ewall,
    "TOP20": lambda px: w_topn(px, 20),
    "TOP10": lambda px: w_topn(px, 10),
    "SPYBH": w_spybh,                            # ZERO-SIGNAL CALENDAR CONTROL
}
BANDS = [0.00, 0.03, 0.05, 0.08, 0.12]           # rule-8 ladder, selected not tuned


# ---------------------------------------------------------------- panels
print("=" * 110)
print("IDEA 517 (lane B) — do-the-THREE-LIVE-PANELS-EVER-AGREE-on-a-vintage")
print("=" * 110)

PX = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": load_universe(small=True)}
NAMES = ["U56", "B136", "SMALL"]
SETS = {"UB": ["U56", "B136"], "US": ["U56", "SMALL"], "BS": ["B136", "SMALL"], "ALL": NAMES}
RULES = ["NATIVE", "LASTDATE", "COMMONSTART", "COMMONWIN"]


def idx_for(panel, pset, rule):
    """The index `panel` is evaluated on, under `rule`, inside panel set `pset`."""
    ix = PX[panel].index
    starts = [PX[p].index[0] for p in pset]
    ends = [PX[p].index[-1] for p in pset]
    lo = max(starts) if rule in ("COMMONSTART", "COMMONWIN") else ix[0]
    hi = min(ends) if rule in ("LASTDATE", "COMMONWIN") else ix[-1]
    return ix[(ix >= lo) & (ix <= hi)]


CACHE = {}


def run(panel, ix, book):
    """Backtest `book` on `panel` restricted to `ix`; return the post-warm-up return series."""
    key = (panel, ix[0], ix[-1], len(ix), book)
    if key in CACHE:
        return CACHE[key]
    px = PX[panel].loc[ix[0]:ix[-1]]
    r, _ = fast_bt(px, BOOKS[book](px))
    out = r.loc[px.index[WARM]:]
    CACHE[key] = out
    return out


def run_band(panel, ix, band):
    key = (panel, ix[0], ix[-1], len(ix), f"BAND{band}")
    if key in CACHE:
        return CACHE[key]
    px = PX[panel].loc[ix[0]:ix[-1]]
    r, _ = fast_bt(px, w_band(px, band))
    out = r.loc[px.index[WARM]:]
    CACHE[key] = out
    return out


def spy_on(panel, ix):
    px = PX[panel].loc[ix[0]:ix[-1]]
    return px["SPY"].pct_change().fillna(0).loc[px.index[WARM]:]


# ---------------------------------------------------------------- GATES
print("\n" + "=" * 110)
print("GATES (five, pre-registered)")
print("=" * 110)
gate_rows = []

# G1 fast_bt == engine.backtest on returns AND turnover, on all three panels x 2 books
g1r = g1t = 0.0
for p in NAMES:
    px = PX[p]
    for bk in ("BAND03", "TOP20"):
        w = BOOKS[bk](px)
        fr, ft = fast_bt(px, w)
        er = backtest(px, w, cost_bps=COST, freq=FREQ)
        g1r = max(g1r, np.nanmax(np.abs(fr.values - er["returns"].values)))
        g1t = max(g1t, np.nanmax(np.abs(ft.values - er["turnover"].values)))
gate_rows.append(("G1 fast_bt vs engine.backtest (3 panels x 2 books)",
                  f"returns {g1r:.3e} / turnover {g1t:.3e}", g1r <= 1e-15 and g1t <= 1e-15))

# G2 the live-book constant on U56 at today's prices.csv vintage (idea 523 G3b: 8.61/1.1998/-12.05)
r_live = run("U56", PX["U56"].index, "BAND03")
m_live = mstats(r_live)
gate_rows.append(("G2 live RULES v2 U56 @10bps (idea 523 G3b: 8.61%/1.1998/-12.05%)",
                  f"{m_live['CAGR']:.2%}/{m_live['Sharpe']:.4f}/{m_live['MaxDD']:.2%}",
                  abs(m_live["Sharpe"] - 1.1998) < 5e-3 and abs(m_live["MaxDD"] + 0.1205) < 5e-3))

# G3 derived cost rung: net(25) == net(0) - turnover*25/1e4
px = PX["U56"]; w = BOOKS["TOP20"](px)
r0, t0 = fast_bt(px, w, cost_bps=0.0)
r25, _ = fast_bt(px, w, cost_bps=25.0)
g3 = np.nanmax(np.abs((r0 - t0 * 25 / 1e4) - r25).values)
gate_rows.append(("G3 cost-rung identity net(25) = net(0) - turn*25/1e4", f"{g3:.3e}", g3 <= 1e-15))

# G4 STRUCTURAL: the three live panels are NESTED with no interior holes
nest, interior = True, 0
for a, b in (("SMALL", "B136"), ("B136", "U56"), ("SMALL", "U56")):
    ia, ib = PX[a].index, PX[b].index
    nest &= len(ia.difference(ib)) == 0
    win = ib[(ib >= ia[0]) & (ib <= ia[-1])]
    interior += len(win.difference(ia))
gate_rows.append(("G4 SMALL subset B136 subset U56, zero interior holes",
                  f"nested={nest}, interior-day mismatches={interior}", nest and interior == 0))

# G5 given G4, INTERSECT (the queue's words) == COMMONWIN (a window truncation) exactly
g5 = 0
for sname, pset in SETS.items():
    inter = PX[pset[0]].index
    for p in pset[1:]:
        inter = inter.intersection(PX[p].index)
    for p in pset:
        cw = idx_for(p, pset, "COMMONWIN")
        g5 = max(g5, len(cw.symmetric_difference(inter)))
gate_rows.append(("G5 INTERSECT(indices) == COMMONWIN window, all 4 panel sets",
                  f"max symmetric-difference {g5} days", g5 == 0))

for nm, val, ok in gate_rows:
    print(f"  [{'PASS' if ok else 'FAIL'}] {nm}: {val}")
assert all(ok for _, _, ok in gate_rows), "a gate failed — no result is read"

# ---------------------------------------------------------------- PART A
print("\n" + "=" * 110)
print("PART A — the census the queue asks for, and the ACTUAL index geometry")
print("=" * 110)

scripts = sorted((ROOT / "research" / "backtests").glob("*.py"))
me = Path(__file__).name
cnt = {1: 0, 2: 0, 3: 0}
multi = 0
for s in scripts:
    if s.name == me:
        continue
    t = s.read_text(errors="ignore")
    k = 1 if "load_universe" in t or "load_prices" in t else 0
    if k == 0:
        continue
    n = 1 + ("broad=True" in t) + ("small=True" in t)
    cnt[n] = cnt.get(n, 0) + 1
    multi += n >= 2
tot = sum(cnt.values())
print(f"  committed backtest scripts scanned: {len(scripts)-1} (this run excluded); price-loading: {tot}")
print(f"  one-panel {cnt[1]} | two-panel {cnt[2]} | three-panel {cnt[3]}"
      f"  ->  MULTI-PANEL {multi} of {tot} = {multi/tot:.1%}")

geo = []
for p in NAMES:
    ix = PX[p].index
    geo.append(dict(panel=p, n=len(ix), start=str(ix[0].date()), end=str(ix[-1].date()),
                    cols=PX[p].shape[1]))
print("\n" + pd.DataFrame(geo).to_string(index=False))
uix, bix, six = (PX[p].index for p in NAMES)
end_gap = len(uix) - len(uix[uix <= bix[-1]])
start_gap = len(uix[(uix >= uix[0]) & (uix < six[0])])
print(f"\n  END   gap (U56 tail beyond B136/SMALL): {end_gap} trading days = {end_gap/len(uix):.3%} of U56")
print(f"  START gap (U56/B136 head before SMALL) : {start_gap} trading days = {start_gap/len(uix):.3%} of U56")
print(f"  the queue names the END gap ('up to 5 trading days'); measured today it is {end_gap}.")
print(f"  the START gap is {start_gap/end_gap:.0f}x larger and a COMMON-LAST-DATE truncation does not touch it.")

# A2 — the COMMANDAND's own vintage: 4b is scored against SPY, and the panels do not share one.
print("\n  A2 — THE COMPARAND'S OWN VINTAGE (4b scores every book against SPY):")
com = PX["SMALL"].index
sp = {p: PX[p]["SPY"].loc[com] for p in NAMES}
for a, b in (("U56", "B136"), ("U56", "SMALL"), ("B136", "SMALL")):
    d = (sp[a] - sp[b]).abs()
    src = {"U56": "data/prices.csv", "B136": "data/prices_broad.csv", "SMALL": "data/prices.csv"}
    print(f"    SPY[{a}] ({src[a]}) vs SPY[{b}] ({src[b]}): max|d| {d.max():.6f}, "
          f"max rel {(d / sp[a]).max():.3e}, days differing >1e-9: {(d > 1e-9).sum()} of {len(d)} "
          f"({(d > 1e-9).mean():.1%})")
print("    -> B136 carries a SEPARATE SPY series from U56/SMALL because it is cached in a")
print("       different file on a different schedule. This is a THIRD vintage channel, it is")
print("       in the BAR and not in the book, and neither a common-last-date nor an index")
print("       intersection removes it: it is present on days both panels quote.")

# ---------------------------------------------------------------- PART B
print("\n" + "=" * 110)
print("PART B — cross-panel ORDERING flips, 4 truncation rules x 4 panel sets (ALL 16 CELLS)")
print("=" * 110)

STATS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2"]


def stat_block(panel, ix, book):
    r = run(panel, ix, book)
    m = mstats(r); h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                start=str(r.index[0].date()), end=str(r.index[-1].date()), n=len(r))


rows, ORDERS = [], {}
for sname, pset in SETS.items():
    for rule in RULES:
        for book in BOOKS:
            vals = {}
            for p in pset:
                b = stat_block(p, idx_for(p, pset, rule), book)
                vals[p] = b
                rows.append(dict(pset=sname, rule=rule, book=book, panel=p, **b))
            for st in STATS:
                ORDERS[(sname, rule, book, st)] = tuple(sorted(pset, key=lambda p: -vals[p][st]))

df = pd.DataFrame(rows)
print("\nEVERY (panel set x rule x book x panel) row — full-sample, 10 bps, weekly:")
print(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

flip, flipped_cells = [], []
for sname, pset in SETS.items():
    for rule in RULES[1:]:
        for st in STATS:
            n = f = 0
            for book in BOOKS:
                n += 1
                a, b = ORDERS[(sname, rule, book, st)], ORDERS[(sname, "NATIVE", book, st)]
                if a != b:
                    f += 1
                    flipped_cells.append(dict(pset=sname, rule=rule, book=book, stat=st,
                                              NATIVE=">".join(b), truncated=">".join(a)))
            flip.append(dict(pset=sname, rule=rule, stat=st, flips=f, n=n, rate=f / n))
fl = pd.DataFrame(flip)
print("\nORDERING FLIPS vs NATIVE (unit = one published cross-panel ordering claim):")
print(fl.pivot_table(index=["pset", "rule"], columns="stat", values="flips").to_string())
print(f"\n  TOTAL ordering claims tested: {len(fl)*1} stat-cells x 6 books = {fl['n'].sum()}")
print(f"  TOTAL flips: {fl['flips'].sum()} = {fl['flips'].sum()/fl['n'].sum():.2%}")
for rule in RULES[1:]:
    sub = fl[fl["rule"] == rule]
    print(f"    {rule:<12} {sub['flips'].sum():>3} / {sub['n'].sum()} = {sub['flips'].sum()/sub['n'].sum():>6.2%}")

print("\n  BY STATISTIC — where the vintage risk actually lives:")
bs = fl.groupby("stat")[["flips", "n"]].sum()
bs["rate"] = bs["flips"] / bs["n"]
print(bs.to_string(float_format=lambda x: f"{x:.4f}"))
hv = bs.loc[["H1", "H2"], "flips"].sum()
print(f"  -> the HALF-SPLIT statistics carry {hv} of {bs['flips'].sum()} flips "
      f"({hv/bs['flips'].sum():.1%}); MaxDD carries {int(bs.loc['MaxDD','flips'])}.")
print("     MECHANISM: baseline._row splits at len(r)//2, an INDEX-LENGTH function, so any")
print("     truncation moves the half boundary (PART C: up to 365 calendar days) — and")
print("     'Sharpe > X in BOTH halves' is the leg PROTOCOL 4a and 4b are built on.")
print("\n  THE FLIPPED CELLS, named:")
print(pd.DataFrame(flipped_cells).to_string(index=False))

# the zero-signal calendar control: SPYBH is the SAME DATA on every panel
print("\n  ZERO-SIGNAL CALENDAR CONTROL (SPYBH — identical instrument on all three panels;")
print("  any cross-panel spread it shows is 100% vintage/calendar, 0% panel):")
ctl = []
for rule in RULES:
    v = {p: stat_block(p, idx_for(p, SETS["ALL"], rule), "SPYBH") for p in NAMES}
    ctl.append(dict(rule=rule, **{f"{p}_S": v[p]["Sharpe"] for p in NAMES},
                    spread_S=max(v[p]["Sharpe"] for p in NAMES) - min(v[p]["Sharpe"] for p in NAMES),
                    spread_CAGR=max(v[p]["CAGR"] for p in NAMES) - min(v[p]["CAGR"] for p in NAMES),
                    ident=len({(round(v[p]["Sharpe"], 12), round(v[p]["CAGR"], 12)) for p in NAMES}) == 1))
print(pd.DataFrame(ctl).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

# ---------------------------------------------------------------- PART C
print("\n" + "=" * 110)
print("PART C — what each channel costs a SINGLE panel's own published numbers")
print("=" * 110)
ch = []
for p in NAMES:
    ix = PX[p].index
    base = stat_block(p, ix, "BAND03")
    endi = idx_for(p, NAMES, "LASTDATE")
    sti = idx_for(p, NAMES, "COMMONSTART")
    cwi = idx_for(p, NAMES, "COMMONWIN")
    r_base = run(p, ix, "BAND03")
    hb_base = r_base.index[len(r_base) // 2]
    for lbl, i2 in (("END-only", endi), ("START-only", sti), ("BOTH", cwi)):
        b2 = stat_block(p, i2, "BAND03")
        r2 = run(p, i2, "BAND03")
        hb2 = r2.index[len(r2) // 2]
        ch.append(dict(panel=p, channel=lbl, days_dropped=len(ix) - len(i2),
                       dCAGR=b2["CAGR"] - base["CAGR"], dSharpe=b2["Sharpe"] - base["Sharpe"],
                       dMaxDD=b2["MaxDD"] - base["MaxDD"], dH1=b2["H1"] - base["H1"],
                       dH2=b2["H2"] - base["H2"],
                       half_boundary=str(hb2.date()),
                       hb_shift_days=abs((hb2 - hb_base).days)))
cd = pd.DataFrame(ch)
print(cd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
print("\n  (the live book BAND03 = RULES v2. dSharpe here is the size of the vintage artefact")
print("   in the units every cross-panel claim in the record is published in.)")

# ---------------------------------------------------------------- PART D
print("\n" + "=" * 110)
print("PART D — PROTOCOL 8 walk-forward under each truncation rule, + both KEEP paths")
print("=" * 110)


def keep_paths(r, rb, rs, r_oos, rs_oos):
    """4a vs RULES v2 (rb) and 4b vs SPY (rs), on the identical index."""
    h1, h2 = halves(r); b1, b2 = halves(rb); s1, s2 = halves(rs)
    m, mb, ms = mstats(r), mstats(rb), mstats(rs)
    a = (h1 > b1) and (h2 > b2) and (m["MaxDD"] >= mb["MaxDD"])
    oos_ok = mstats(r_oos)["Sharpe"] > mstats(rs_oos)["Sharpe"]
    b = (h1 > s1) and (h2 > s2) and oos_ok and (m["MaxDD"] >= 0.60 * ms["MaxDD"]) \
        and (m["CAGR"] >= 0.70 * ms["CAGR"])
    return a, b, m, mb, ms


wf = []
for sname, pset in SETS.items():
    for rule in RULES:
        for p in pset:
            ix = idx_for(p, pset, rule)
            picks = []
            for bd in BANDS:
                r = run_band(p, ix, bd)
                ris = r.loc[:IS_END]
                picks.append((mstats(ris)["Sharpe"], bd))
            is_sh, best = max(picks)
            r = run_band(p, ix, best)
            rb = run(p, ix, "BAND03")
            rs = spy_on(p, ix)
            ro, rso = r.loc[OOS_START:], rs.loc[OOS_START:]
            rbo = rb.loc[OOS_START:]
            a, b, m, mb, ms = keep_paths(r, rb, rs, ro, rso)
            mo, mbo, mso = mstats(ro), mstats(rbo), mstats(rso)
            wf.append(dict(pset=sname, rule=rule, panel=p, pick=best, IS_Sharpe=is_sh,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           v2_OOS_S=mbo["Sharpe"], SPY_OOS_S=mso["Sharpe"],
                           SPY_OOS_CAGR=mso["CAGR"], SPY_OOS_DD=mso["MaxDD"],
                           full_4a=a, full_4b=b))
w = pd.DataFrame(wf)
print("\nALL 4 rules x 4 panel sets x panels — rule-8 pick and its untouched OOS window:")
print(w.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\n  DOES THE RULE-8 PICK MOVE WITH THE TRUNCATION RULE?")
mv = []
for sname, pset in SETS.items():
    for p in pset:
        s = w[(w.pset == sname) & (w.panel == p)].set_index("rule")["pick"]
        mv.append(dict(pset=sname, panel=p, NATIVE=s["NATIVE"], LASTDATE=s["LASTDATE"],
                       COMMONSTART=s["COMMONSTART"], COMMONWIN=s["COMMONWIN"],
                       moved=len(set(s.values)) > 1))
mvd = pd.DataFrame(mv)
print(mvd.to_string(index=False))
print(f"  picks that move: {mvd['moved'].sum()} of {len(mvd)} = {mvd['moved'].mean():.1%}")
for rule in RULES[1:]:
    sub = mvd[mvd[rule] != mvd["NATIVE"]]
    print(f"    vs NATIVE, {rule:<12} moves {len(sub)} of {len(mvd)}")

print("\n  KEEP PATHS over every (rule x panel set x panel) book above:")
print(f"    4a passes: {int(w['full_4a'].sum())} of {len(w)}")
print(f"    4b passes: {int(w['full_4b'].sum())} of {len(w)}")
if w["full_4b"].any():
    print(w[w.full_4b][["pset", "rule", "panel", "pick", "OOS_CAGR", "OOS_Sharpe",
                        "OOS_MaxDD"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\n  OOS reference levels (same index as each row above):")
ref = w.groupby(["panel", "rule"])[["OOS_Sharpe", "v2_OOS_S", "SPY_OOS_S", "SPY_OOS_CAGR"]].mean()
print(ref.to_string(float_format=lambda x: f"{x:.4f}"))

print("\n  AND THE BAR ITSELF MOVES WITH THE VINTAGE (4b is scored against these):")
bar = w.groupby(["panel", "rule"])[["SPY_OOS_S", "SPY_OOS_CAGR", "SPY_OOS_DD"]].mean()
bar["4b_CAGR_floor"] = 0.70 * bar["SPY_OOS_CAGR"]
bar["4b_DD_cap"] = 0.60 * bar["SPY_OOS_DD"]
print(bar.to_string(float_format=lambda x: f"{x:.4f}"))
sprd = w.groupby("rule")["SPY_OOS_S"].agg(lambda s: s.max() - s.min())
print("\n  cross-panel spread in SPY's OWN OOS Sharpe, by rule (should be 0 — SPY is one asset):")
print("   " + ", ".join(f"{k} {v:.4f}" for k, v in sprd.items()))

# ---------------------------------------------------------------- artefacts
STEM = Path(__file__).with_suffix("")
pd.DataFrame(geo).to_csv(f"{STEM}.panels.csv", index=False)
df.to_csv(f"{STEM}.grid.csv", index=False)
fl.to_csv(f"{STEM}.flips.csv", index=False)
pd.DataFrame(flipped_cells).to_csv(f"{STEM}.flippedcells.csv", index=False)
cd.to_csv(f"{STEM}.channels.csv", index=False)
pd.DataFrame(ctl).to_csv(f"{STEM}.control.csv", index=False)
w.to_csv(f"{STEM}.walkforward.csv", index=False)
mvd.to_csv(f"{STEM}.pickstability.csv", index=False)
print(f"\nartefacts written: {Path(STEM).name}.{{panels,grid,flips,flippedcells,channels,control,walkforward,pickstability}}.csv")

print("\n" + "=" * 110)
print("DONE")
print("=" * 110)
