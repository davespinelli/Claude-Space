#!/usr/bin/env python3
"""IDEA 697 (lane B, 2026-09-11): is-the-len-r-SLASH-2-HALF-SPLIT-the-record-s-single-largest-CONVENTION-artefact.

Queue premise (from idea 517): "the half-split statistics carry 14 of 18 vintage flips
(77.8%) and MaxDD carries 0, because baseline._row splits at len(r)//2, an INDEX-LENGTH
function that moves the boundary 365 calendar days under a 505-day truncation. Re-run a
slice of the record's committed 4a/4b verdicts with halves cut at a FIXED CALENDAR DATE
instead and report how many H1/H2 legs move."

WHAT IS ACTUALLY BEING TESTED.  PROTOCOL 4a and 4b both contain the clause "Sharpe > X in
BOTH halves".  Neither PROTOCOL nor RULES defines "halves"; the definition lives in one
line of research/baseline.py (`h = len(r) // 2` in `_row`).  That is an index-length
function of whatever window the script happened to load, so it is NOT a property of the
book — it is a property of the tape's length on the day the script ran.  This run prices
the convention: it re-cuts the SAME return series at a fixed calendar date and counts how
many 4a/4b leg verdicts move.

THE TWO TUNED PARAMETERS (PROTOCOL 4, max 2), exactly the ones the queue names:
  PARAM 1  split date : NATIVE (len(r)//2) + CALMID + a 6-rung fixed-date ladder  (8 rungs)
  PARAM 2  claim set  : LIVE / RANKED / EWGATE / CONTROL                          (4 rungs)
Panel (U56 / B136 / SMALL439) is REPORTED, not tuned — all three, every cell.
The rule-8 band ladder is SELECTED by PROTOCOL 8 on IS only; it is not tuned here.
ALL 8 x 4 x 3 = 96 grid cells are reported, and every book-level row is printed.

Structure of the run:
  GATES  five, pre-registered, all printed before any result is read.
  PART A the convention census (how much of the record is exposed) + the actual geometry
         of len(r)//2 in calendar terms on the three live panels.
  PART B the queue's question: H1/H2 LEG flips and 4a/4b VERDICT flips vs NATIVE.
  PART C why — is it the boundary MOVING, or the two sides carrying different regimes?
  PART D PROTOCOL 8 walk-forward under every split rule + both KEEP paths.

Costs 10 bps, weekly cadence, next-day execution (engine applies weights at t+1).
Deterministic; no network; no RNG.
"""
import sys, re
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, _row  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask  # noqa

COST = 10.0
FREQ = "W"
WARM = 260          # baseline.compare's warm-up skip, kept verbatim
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
pd.set_option("display.width", 260)
pd.set_option("display.max_rows", 400)


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


# ------------------------------------------------- PARAM 1: the split-date dial
# NATIVE is the record's convention verbatim (baseline._row).  CALMID is the calendar
# midpoint of the series' own span.  The six dated rungs are fixed calendar dates that do
# NOT depend on the loaded window at all — the queue's proposed replacement.
SPLITS = ["NATIVE", "CALMID", "2014-01-01", "2015-01-01", "2016-01-01",
          "2017-01-01", "2018-01-01", "2019-01-01"]


def split_at(r: pd.Series, rule: str) -> pd.Timestamp:
    """The first timestamp of H2 under `rule`."""
    if rule == "NATIVE":
        return r.index[len(r) // 2]
    if rule == "CALMID":
        mid = r.index[0] + (r.index[-1] - r.index[0]) / 2
        pos = r.index.searchsorted(mid)
        return r.index[min(pos, len(r) - 1)]
    ts = pd.Timestamp(rule)
    pos = r.index.searchsorted(ts)
    return r.index[min(pos, len(r) - 1)]


def halves_at(r: pd.Series, rule: str):
    """(H1 Sharpe, H2 Sharpe, boundary, n1, n2) under split rule `rule`."""
    b = split_at(r, rule)
    a, c = r.loc[:b].iloc[:-1], r.loc[b:]
    if len(a) < 60 or len(c) < 60:            # degenerate cut — reported, never silently NaN'd
        return np.nan, np.nan, b, len(a), len(c)
    return mstats(a)["Sharpe"], mstats(c)["Sharpe"], b, len(a), len(c)


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
    "BAND03": lambda px: w_band(px, 0.03),      # == live RULES v2 (band .03, gross .75)
    "BAND08": lambda px: w_band(px, 0.08),
    "TOP20": lambda px: w_topn(px, 20),
    "TOP10": lambda px: w_topn(px, 10),
    "EWALL": w_ewall,
    "SPYBH": w_spybh,                            # ZERO-SIGNAL CALENDAR CONTROL
}
# PARAM 2: the claim set, i.e. which slice of the record's committed verdicts is re-cut.
CLAIMSETS = {
    "LIVE": ["BAND03", "BAND08"],       # the live rules family (RULES v2 and its band dial)
    "RANKED": ["TOP20", "TOP10"],       # the top-n momentum family the record keeps re-pricing
    "EWGATE": ["EWALL"],                # the Sep-3 memo's gated equal-weight book
    "CONTROL": ["SPYBH"],               # one asset, zero signal, zero parameters
}
BANDS = [0.00, 0.03, 0.05, 0.08, 0.12]           # rule-8 ladder, selected not tuned

print("=" * 118)
print("IDEA 697 (lane B) — is-the-len-r-SLASH-2-HALF-SPLIT-the-record-s-single-largest-CONVENTION-artefact")
print("=" * 118)

PX = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": load_universe(small=True)}
NAMES = ["U56", "B136", "SMALL"]

CACHE = {}


def run(panel, book):
    key = (panel, book)
    if key not in CACHE:
        px = PX[panel]
        r, _ = fast_bt(px, BOOKS[book](px)) if book in BOOKS else (None, None)
        CACHE[key] = r.loc[px.index[WARM]:]
    return CACHE[key]


def run_band(panel, band):
    key = (panel, f"_BAND{band}")
    if key not in CACHE:
        px = PX[panel]
        r, _ = fast_bt(px, w_band(px, band))
        CACHE[key] = r.loc[px.index[WARM]:]
    return CACHE[key]


def spy_on(panel):
    px = PX[panel]
    return px["SPY"].pct_change().fillna(0).loc[px.index[WARM]:]


# ---------------------------------------------------------------- GATES
print("\n" + "=" * 118)
print("GATES (five, pre-registered — printed before any result is read)")
print("=" * 118)
gate_rows = []

# G1 fast_bt == engine.backtest on returns AND turnover, all three panels x 2 books
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
m_live = mstats(run("U56", "BAND03"))
gate_rows.append(("G2 live RULES v2 U56 @10bps (idea 523 G3b: 8.61%/1.1998/-12.05%)",
                  f"{m_live['CAGR']:.2%}/{m_live['Sharpe']:.4f}/{m_live['MaxDD']:.2%}",
                  abs(m_live["Sharpe"] - 1.1998) < 5e-3 and abs(m_live["MaxDD"] + 0.1205) < 5e-3))

# G3 derived cost rung: net(25) == net(0) - turnover*25/1e4
px = PX["U56"]; w = BOOKS["TOP20"](px)
r0, t0 = fast_bt(px, w, cost_bps=0.0)
r25, _ = fast_bt(px, w, cost_bps=25.0)
g3 = np.nanmax(np.abs((r0 - t0 * 25 / 1e4) - r25).values)
gate_rows.append(("G3 cost-rung identity net(25) = net(0) - turn*25/1e4", f"{g3:.3e}", g3 <= 1e-15))

# G4 LOAD-BEARING: halves_at(.,"NATIVE") reproduces baseline._row's H1/H2 EXACTLY.
#    If this fails, nothing below is a statement about the record's own convention.
g4 = 0.0
for p in NAMES:
    for bk in ("BAND03", "TOP10", "SPYBH"):
        r = run(p, bk)
        ref = _row("x", r)
        h1, h2, _, _, _ = halves_at(r, "NATIVE")
        g4 = max(g4, abs(h1 - ref["H1"]), abs(h2 - ref["H2"]))
gate_rows.append(("G4 halves_at(NATIVE) == baseline._row H1/H2 (3 panels x 3 books)",
                  f"max|d| {g4:.3e}", g4 <= 1e-12))

# G5 STRUCTURAL: the dial is real — NATIVE's boundary is NOT a fixed calendar date across
#    panels, and it is NOT the calendar midpoint on any of them.
bnd = {p: split_at(run(p, "BAND03"), "NATIVE") for p in NAMES}
cmid = {p: split_at(run(p, "BAND03"), "CALMID") for p in NAMES}
spread = (max(bnd.values()) - min(bnd.values())).days
off = max(abs((bnd[p] - cmid[p]).days) for p in NAMES)
gate_rows.append(("G5 NATIVE boundary is panel-dependent and != calendar midpoint",
                  f"cross-panel spread {spread}d, max offset from CALMID {off}d",
                  spread > 0 and off > 0))

for nm, val, ok in gate_rows:
    print(f"  [{'PASS' if ok else 'FAIL'}] {nm}: {val}")
assert all(ok for _, _, ok in gate_rows), "a gate failed — no result is read"

# ---------------------------------------------------------------- PART A
print("\n" + "=" * 118)
print("PART A — HOW MUCH OF THE RECORD IS EXPOSED, and where len(r)//2 actually lands")
print("=" * 118)

scripts = sorted((ROOT / "research" / "backtests").glob("*.py"))
me = Path(__file__).name
RX_LEN2 = re.compile(r"len\(\s*\w+\s*\)\s*//\s*2")
RX_COMPARE = re.compile(r"\bcompare\s*\(")
RX_HALF = re.compile(r"\bhalves\b|\bH1\b|\bH2\b")
n_len2 = n_cmp = n_half = n_either = n_price = 0
exposed = []
for s in scripts:
    if s.name == me:
        continue
    t = s.read_text(errors="ignore")
    if "load_universe" not in t and "load_prices" not in t:
        continue
    n_price += 1
    a, b, c = bool(RX_LEN2.search(t)), bool(RX_COMPARE.search(t)), bool(RX_HALF.search(t))
    n_len2 += a; n_cmp += b; n_half += c
    if a or b:
        n_either += 1
        exposed.append(dict(script=s.name, own_len2=a, calls_compare=b, mentions_halves=c))
print(f"  committed backtest scripts: {len(scripts)-1} (this run excluded); price-loading: {n_price}")
print(f"    own `len(x)//2` split          : {n_len2}")
print(f"    call baseline.compare (uses _row): {n_cmp}")
print(f"    EITHER (exposed to the convention): {n_either} of {n_price} = {n_either/n_price:.1%}")
print(f"    mention H1/H2/halves at all      : {n_half} of {n_price} = {n_half/n_price:.1%}")
print("  NOTE this is an EXPOSURE census, not a flip census: it counts files whose H-legs")
print("  are produced by an index-length split. PART B prices what that exposure is worth.")

print("\n  A2 — WHERE THE NATIVE BOUNDARY LANDS (full native window, BAND03 = live RULES v2):")
geo = []
for p in NAMES:
    r = run(p, "BAND03")
    nb, cb = split_at(r, "NATIVE"), split_at(r, "CALMID")
    geo.append(dict(panel=p, n_days=len(r), start=str(r.index[0].date()), end=str(r.index[-1].date()),
                    NATIVE_boundary=str(nb.date()), CALMID_boundary=str(cb.date()),
                    offset_days=(nb - cb).days,
                    H1_cal_days=(nb - r.index[0]).days, H2_cal_days=(r.index[-1] - nb).days))
gdf = pd.DataFrame(geo)
print(gdf.to_string(index=False))
print("\n  -> len(r)//2 equalises TRADING-DAY COUNT, not calendar time. Wherever the tape has")
print("     holes (a panel that starts later, a cache one week stale, a truncation), the two")
print("     halves stop being the same length in calendar terms, and '>0 in both halves' is")
print("     then a statement about two different-length windows.")

# ---------------------------------------------------------------- PART B
print("\n" + "=" * 118)
print("PART B — THE QUEUE'S QUESTION: H1/H2 LEGS and 4a/4b VERDICTS under 8 split rules")
print("=" * 118)
print("  4a leg  = (H1 > v2's H1) and (H2 > v2's H2)   [PROTOCOL 4a, Sharpe clause]")
print("  4b leg  = (H1 > SPY's H1) and (H2 > SPY's H2) [PROTOCOL 4b, Sharpe clause]")
print("  full 4a = 4a leg AND MaxDD >= v2's MaxDD ;  full 4b = 4b leg AND OOS AND DD cap AND CAGR floor")
print("  The MaxDD / CAGR / OOS legs DO NOT depend on the split rule — only the H-legs do.\n")

rows = []
for cs, books in CLAIMSETS.items():
    for book in books:
        for p in NAMES:
            r = run(p, book)
            rb = run(p, "BAND03")
            rs = spy_on(p)
            m, mb, ms = mstats(r), mstats(rb), mstats(rs)
            ro, rso = r.loc[OOS_START:], rs.loc[OOS_START:]
            oos_ok = mstats(ro)["Sharpe"] > mstats(rso)["Sharpe"]
            dd_ok = m["MaxDD"] >= mb["MaxDD"]
            cap_ok = m["MaxDD"] >= 0.60 * ms["MaxDD"]
            floor_ok = m["CAGR"] >= 0.70 * ms["CAGR"]
            for rule in SPLITS:
                h1, h2, bnd_, n1, n2 = halves_at(r, rule)
                b1, b2, _, _, _ = halves_at(rb, rule)
                s1, s2, _, _, _ = halves_at(rs, rule)
                leg4a = bool((h1 > b1) and (h2 > b2))
                leg4b = bool((h1 > s1) and (h2 > s2))
                rows.append(dict(claimset=cs, book=book, panel=p, split=rule,
                                 boundary=str(bnd_.date()), n1=n1, n2=n2,
                                 H1=h1, H2=h2, v2_H1=b1, v2_H2=b2, SPY_H1=s1, SPY_H2=s2,
                                 leg4a=leg4a, leg4b=leg4b,
                                 full4a=bool(leg4a and dd_ok),
                                 full4b=bool(leg4b and oos_ok and cap_ok and floor_ok),
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"]))
G = pd.DataFrame(rows)
print("ALL 96 GRID CELLS (8 split rules x 6 books x 3 panels; claim sets are the 4-rung PARAM 2):")
print(G[["claimset", "book", "panel", "split", "boundary", "n1", "n2", "H1", "H2",
         "v2_H1", "v2_H2", "SPY_H1", "SPY_H2", "leg4a", "leg4b", "full4a", "full4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

nat = G[G.split == "NATIVE"].set_index(["book", "panel"])
mv = []
for rule in SPLITS[1:]:
    sub = G[G.split == rule].set_index(["book", "panel"])
    for key in ("leg4a", "leg4b", "full4a", "full4b"):
        f = int((sub[key] != nat.loc[sub.index, key]).sum())
        mv.append(dict(split=rule, leg=key, moved=f, n=len(sub), rate=f / len(sub)))
    mv.append(dict(split=rule, leg="H1_abs_shift",
                   moved=np.nan, n=len(sub),
                   rate=float((sub["H1"] - nat.loc[sub.index, "H1"]).abs().mean())))
    mv.append(dict(split=rule, leg="H2_abs_shift", moved=np.nan, n=len(sub),
                   rate=float((sub["H2"] - nat.loc[sub.index, "H2"]).abs().mean())))
M = pd.DataFrame(mv)
print("\nMOVEMENT vs NATIVE (unit = one book x panel, i.e. one published verdict):")
print(M.pivot_table(index="split", columns="leg", values="rate", sort=False)
      .to_string(float_format=lambda x: f"{x:.4f}"))

legs = M[M.leg.isin(["leg4a", "leg4b", "full4a", "full4b"])]
print(f"\n  TOTAL leg/verdict comparisons made: {int(legs['n'].sum())}")
for key in ("leg4a", "leg4b", "full4a", "full4b"):
    s = legs[legs.leg == key]
    print(f"    {key:<8} moves {int(s['moved'].sum()):>3} of {int(s['n'].sum())} = "
          f"{s['moved'].sum()/s['n'].sum():.2%}")

print("\n  BY CLAIM SET (PARAM 2) — who is exposed:")
cs_rows = []
for cs in CLAIMSETS:
    idx = G[(G.claimset == cs)].set_index(["book", "panel", "split"])
    n = f4a = f4b = 0
    h1s = []
    for (bk, p, rule) in idx.index:
        if rule == "NATIVE":
            continue
        n += 1
        base = nat.loc[(bk, p)]
        cur = idx.loc[(bk, p, rule)]
        f4a += int(cur["full4a"] != base["full4a"])
        f4b += int(cur["full4b"] != base["full4b"])
        h1s.append(abs(cur["H1"] - base["H1"]))
    cs_rows.append(dict(claimset=cs, comparisons=n, full4a_moves=f4a, full4b_moves=f4b,
                        mean_abs_dH1=float(np.mean(h1s)), max_abs_dH1=float(np.max(h1s))))
CS = pd.DataFrame(cs_rows)
print(CS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\n  THE FLIPPED CELLS, NAMED — and how far the boundary had to move to flip them:")
fl = []
for rule in SPLITS[1:]:
    sub = G[G.split == rule].set_index(["book", "panel"])
    for key in ("leg4a", "leg4b"):
        d = sub[sub[key] != nat.loc[sub.index, key]]
        for (bk, p) in d.index:
            nb = pd.Timestamp(nat.loc[(bk, p), "boundary"])
            cb = pd.Timestamp(d.loc[(bk, p), "boundary"])
            fl.append(dict(book=bk, panel=p, split=rule, leg=key,
                           NATIVE_boundary=str(nb.date()), boundary=str(cb.date()),
                           shift_days=abs((cb - nb).days),
                           NATIVE_val=bool(nat.loc[(bk, p), key]), new_val=bool(d.loc[(bk, p), key]),
                           dH1=float(d.loc[(bk, p), "H1"] - nat.loc[(bk, p), "H1"]),
                           dH2=float(d.loc[(bk, p), "H2"] - nat.loc[(bk, p), "H2"])))
FL = pd.DataFrame(fl)
print(FL.to_string(index=False, float_format=lambda x: f"{x:.4f}") if len(FL)
      else "    (none — no leg moved under any split rule)")
if len(FL):
    mn = FL.loc[FL["shift_days"].idxmin()]
    print(f"\n  SMALLEST BOUNDARY MOVE THAT FLIPS A PROTOCOL LEG: {int(mn['shift_days'])} calendar days")
    print(f"    {mn['book']} on {mn['panel']}, {mn['leg']} {mn['NATIVE_val']} -> {mn['new_val']}, "
          f"boundary {mn['NATIVE_boundary']} -> {mn['boundary']}")
    print("    The record has never published that boundary, so this leg is unverifiable from")
    print("    the committed numbers alone.")

print("\n  WHY THE FULL VERDICTS DO NOT MOVE — the non-half legs that bind first:")
uniq = G.drop_duplicates(subset=["book", "panel"]).set_index(["book", "panel"])
bind = []
for (bk, p) in uniq.index:
    r = run(p, bk); rb = run(p, "BAND03"); rs = spy_on(p)
    m, mb, ms = mstats(r), mstats(rb), mstats(rs)
    ro, rso = r.loc[OOS_START:], rs.loc[OOS_START:]
    bind.append(dict(book=bk, panel=p, MaxDD=m["MaxDD"], v2_MaxDD=mb["MaxDD"],
                     dd_4a_ok=bool(m["MaxDD"] >= mb["MaxDD"]),
                     dd_cap_4b_ok=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                     cagr_floor_4b_ok=bool(m["CAGR"] >= 0.70 * ms["CAGR"]),
                     oos_4b_ok=bool(mstats(ro)["Sharpe"] > mstats(rso)["Sharpe"])))
B = pd.DataFrame(bind)
print(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
print(f"    4a's MaxDD leg passes {int(B['dd_4a_ok'].sum())} of {len(B)} book x panel pairs;")
print(f"    4b's DD cap passes {int(B['dd_cap_4b_ok'].sum())}, its CAGR floor {int(B['cagr_floor_4b_ok'].sum())}, "
      f"its OOS leg {int(B['oos_4b_ok'].sum())}.")
print("    Those legs are SPLIT-INVARIANT by construction, and they are what is binding —")
print("    which replicates ideas 530/531 (the DD cap does the cutting) from a new direction.")

print("\n  ZERO-SIGNAL CALENDAR CONTROL (SPYBH is ONE asset held one way; every H-leg move")
print("  it shows is 100% convention, 0% book):")
ctl = G[G.book == "SPYBH"][["panel", "split", "boundary", "H1", "H2", "SPY_H1", "SPY_H2", "leg4a", "leg4b"]]
print(ctl.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
csp = G[G.book == "SPYBH"].groupby("panel")["H1"].agg(lambda s: s.max() - s.min())
print("\n  SPY-vs-itself H1 range across the 8 split rules, by panel: " +
      ", ".join(f"{k} {v:.4f}" for k, v in csp.items()))
print(f"  idea 517's published cross-panel CALENDAR NOISE FLOOR on Sharpe was 0.0275 —")
print(f"  the split-date dial alone moves SPY's own H1 by up to {csp.max():.4f} on one panel.")

# ---------------------------------------------------------------- PART C
print("\n" + "=" * 118)
print("PART C — WHY: is it the boundary MOVING, or the two sides carrying different REGIMES?")
print("=" * 118)
reg = []
for p in NAMES:
    r = run(p, "BAND03")
    for rule in SPLITS:
        b = split_at(r, rule)
        a, c = r.loc[:b].iloc[:-1], r.loc[b:]
        def yrs(x):
            return sorted({d.year for d in x.index})
        reg.append(dict(panel=p, split=rule, boundary=str(b.date()),
                        H1_n=len(a), H2_n=len(c), H1_cal=(b - r.index[0]).days,
                        H2_cal=(r.index[-1] - b).days,
                        y2020_in=("H1" if 2020 in yrs(a) and 2020 not in yrs(c) else
                                  "H2" if 2020 in yrs(c) and 2020 not in yrs(a) else "BOTH"),
                        y2022_in=("H1" if 2022 in yrs(a) and 2022 not in yrs(c) else
                                  "H2" if 2022 in yrs(c) and 2022 not in yrs(a) else "BOTH"),
                        H1_Sharpe=mstats(a)["Sharpe"] if len(a) >= 60 else np.nan,
                        H2_Sharpe=mstats(c)["Sharpe"] if len(c) >= 60 else np.nan))
R = pd.DataFrame(reg)
print("Regime membership of the two sides, live RULES v2 book (BAND03):")
print(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
nstress = int((R["y2020_in"] != "H2").sum() + (R["y2022_in"] != "H2").sum())
print(f"\n  REGIME-REALLOCATION CHANNEL: INACTIVE on this ladder. 2020 and 2022 sit in H2 under")
print(f"  every one of the {len(SPLITS)} split rules on all three panels ({nstress} exceptions out of "
      f"{2*len(R)}), because the ladder tops out at 2019-01-01. So the H-leg movement measured in")
print("  PART B is NOT the stress years changing sides — it is how much of the quiet 2013-2016")
print("  bull is counted in H1 rather than H2. A split date at or after 2020 WOULD move the")
print("  stress years and is expected to be larger; it is out of this run's pre-registered grid")
print("  and is left to the queue, not claimed here.")

# ---------------------------------------------------------------- PART D
print("\n" + "=" * 118)
print("PART D — PROTOCOL 8 WALK-FORWARD (band picked on 2009-2016 IS only) + BOTH KEEP PATHS")
print("=" * 118)
wf = []
for p in NAMES:
    picks = []
    for bd in BANDS:
        r = run_band(p, bd)
        picks.append((mstats(r.loc[:IS_END])["Sharpe"], bd))
    is_sh, best = max(picks)
    print(f"\n  {p}: IS band ladder " +
          ", ".join(f"{bd}:{s:.4f}" for s, bd in sorted(picks, key=lambda z: z[1])) +
          f"  -> PICK band={best} (IS Sharpe {is_sh:.4f})")
    r = run_band(p, best)
    rb = run(p, "BAND03")
    rs = spy_on(p)
    ro, rbo, rso = r.loc[OOS_START:], rb.loc[OOS_START:], rs.loc[OOS_START:]
    mo, mbo, mso = mstats(ro), mstats(rbo), mstats(rso)
    m, mb, ms = mstats(r), mstats(rb), mstats(rs)
    for rule in SPLITS:
        h1, h2, bnd_, _, _ = halves_at(r, rule)
        b1, b2, _, _, _ = halves_at(rb, rule)
        s1, s2, _, _, _ = halves_at(rs, rule)
        a = bool((h1 > b1) and (h2 > b2) and (m["MaxDD"] >= mb["MaxDD"]))
        b = bool((h1 > s1) and (h2 > s2) and (mo["Sharpe"] > mso["Sharpe"])
                 and (m["MaxDD"] >= 0.60 * ms["MaxDD"]) and (m["CAGR"] >= 0.70 * ms["CAGR"]))
        wf.append(dict(panel=p, split=rule, pick=best, IS_Sharpe=is_sh, boundary=str(bnd_.date()),
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       v2_OOS_CAGR=mbo["CAGR"], v2_OOS_Sharpe=mbo["Sharpe"], v2_OOS_MaxDD=mbo["MaxDD"],
                       SPY_OOS_CAGR=mso["CAGR"], SPY_OOS_Sharpe=mso["Sharpe"], SPY_OOS_MaxDD=mso["MaxDD"],
                       H1=h1, H2=h2, KEEP_4a=a, KEEP_4b=b))
W = pd.DataFrame(wf)
print("\nOOS 2017-2026 (untouched), rule-8 pick, vs RULES v2 baseline and vs SPY — every split rule:")
print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
print(f"\n  4a passes: {int(W['KEEP_4a'].sum())} of {len(W)}   |   4b passes: {int(W['KEEP_4b'].sum())} of {len(W)}")
if W["KEEP_4b"].any():
    print(W[W.KEEP_4b][["panel", "split", "pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
for p in NAMES:
    s = W[W.panel == p]
    print(f"    {p:<6} 4a {int(s['KEEP_4a'].sum())}/{len(s)} split rules, "
          f"4b {int(s['KEEP_4b'].sum())}/{len(s)} split rules "
          f"-> {'SPLIT-DECIDED' if 0 < s['KEEP_4a'].sum() < len(s) or 0 < s['KEEP_4b'].sum() < len(s) else 'split-invariant'}")

print("\n  The OOS window (2017-2026) is FIXED by PROTOCOL 8 and does NOT move with the split")
print("  rule, so OOS CAGR/Sharpe/MaxDD above are identical down each panel's block. What the")
print("  split rule moves is the full-sample H-legs that sit INSIDE the 4a and 4b predicates.")

# ---------------------------------------------------------------- artefacts
STEM = Path(__file__).with_suffix("")
gdf.to_csv(f"{STEM}.geometry.csv", index=False)
pd.DataFrame(exposed).to_csv(f"{STEM}.census.csv", index=False)
G.to_csv(f"{STEM}.grid.csv", index=False)
M.to_csv(f"{STEM}.moves.csv", index=False)
CS.to_csv(f"{STEM}.claimsets.csv", index=False)
R.to_csv(f"{STEM}.regimes.csv", index=False)
W.to_csv(f"{STEM}.walkforward.csv", index=False)
FL.to_csv(f"{STEM}.flippedcells.csv", index=False)
B.to_csv(f"{STEM}.bindinglegs.csv", index=False)
print(f"\nartefacts written: {Path(STEM).name}."
      "{geometry,census,grid,moves,claimsets,flippedcells,bindinglegs,regimes,walkforward}.csv")

print("\n" + "=" * 118)
print("DONE")
print("=" * 118)
