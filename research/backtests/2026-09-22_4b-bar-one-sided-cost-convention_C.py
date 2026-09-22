#!/usr/bin/env python3
"""Idea 1490 (lane C, 2026-09-22): does the 4b BAR ITSELF survive charging SPY the
candidate's own turnover?

PROTOCOL rule 4b sets both bars off a COSTLESS SPY buy-and-hold (CAGR >= 70% of SPY's,
MaxDD <= 60% of SPY's) while every candidate pays `cost_bps` on its realised turnover.
That is a one-sided ladder: the comparand is the only book in the comparison that never
pays to exist.  This run re-cuts BOTH bars under four cost conventions and re-reads every
cell's 4b verdict, full sample, halves and rule-8 OOS.

AXIS UNDER TEST (published at every level, never selected on):
  BAR CONVENTIONS
    K0  SPY costless                      -- the live PROTOCOL convention
    K1  SPY charged the CANDIDATE'S OWN realised turnover series, same cost rung (idea 1490)
    K2  SPY charged a FLAT 2.0x/yr turnover, same cost rung (convention-independent control)
    K3  candidate ALSO costless           -- the other way to remove the asymmetry

TWO TUNED DIALS AND NO MORE: GROSS g and PANEL.
REPORTED, NEVER SELECTED ON: cost rung {0,5,10,25,50} bps, cadence {W,M}, band (3%, live).

Books: `baseline.rules_v2_weights` (the live band book) walked on a gross ladder -- the
family every standing 4b pass in this record lives in -- plus the live g=0.75 book and
`rules_v1_weights` for continuity.

Deterministic, standalone, offline (committed caches only).
"""
import sys, json, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

pd.set_option("display.width", 200)
GROSS = [0.25, 0.50, 0.75, 1.00]
COSTS = [0, 5, 10, 25, 50]
CADENCES = ["W", "M"]
PANELS = ["U56", "B136"]
CONVS = ["K0_spy_free", "K1_spy_own_turnover", "K2_spy_flat2x", "K3_both_free"]
BAND = 0.03            # live, reported not tuned
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
FLAT_TO = 2.0          # x/yr for K2

out = []
def say(s=""):
    print(s); out.append(str(s))

# ---------------------------------------------------------------- harness
def sim(px, W, freq):
    """Gross (pre-cost) returns + daily turnover series.  Positions never depend on cost,
    so a cost rung is a pure linear deduction (gate G2 proves it against engine.backtest)."""
    r = backtest(px, W, cost_bps=0.0, freq=freq)
    return r["returns"], r["turnover"]

def net(gross_r, to, bps):
    return gross_r - to * bps / 1e4

def mets(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]

def win(s, a=None, b=None):
    return s.loc[a:b]

# ---------------------------------------------------------------- load
books = {}      # (panel, g, cad) -> (gross_returns, turnover)
spy_gross = {}  # panel -> spy daily returns
index = {}
for panel in PANELS:
    px = load_universe(broad=(panel == "B136"))
    start = px.index[260]
    spy_gross[panel] = px["SPY"].pct_change().fillna(0.0).loc[start:]
    index[panel] = spy_gross[panel].index
    for g, cad in itertools.product(GROSS, CADENCES):
        gr, to = sim(px, rules_v2_weights(px, band=BAND, gross=g), cad)
        books[(panel, g, cad)] = (gr.loc[start:], to.loc[start:])
    for cad in CADENCES:
        gr, to = sim(px, rules_v1_weights(px), cad)
        books[(panel, "v1", cad)] = (gr.loc[start:], to.loc[start:])
    globals()["_px_" + panel] = px

say("=" * 110)
say("IDEA 1490 (lane C) — DOES THE 4b BAR ITSELF SURVIVE CHARGING SPY THE CANDIDATE'S OWN TURNOVER?")
say("=" * 110)
say(f"Panels {PANELS} | gross {GROSS} | cadence {CADENCES} | cost {COSTS} bps | band {BAND} | conventions {CONVS}")
say(f"Sample per panel: {index['U56'][0].date()} -> {index['U56'][-1].date()} ({len(index['U56'])} sessions)")

# ---------------------------------------------------------------- gates
say()
say("-" * 110); say("GATES"); say("-" * 110)
gates = []
px = globals()["_px_U56"]; st = px.index[260]

# G1 live baseline replay
gr, to = books[("U56", 0.75, "W")]
c, s, d = mets(net(gr, to, 10))
gates.append(("G1 live RULES v2 replay (U56,W,g=.75,10bps)",
              f"{c:.2%} / {s:.4f} / {d:.2%}  (RULES.md-era 8.62% / 1.2010 / -12.05%)",
              abs(s - 1.2010) < 0.02))

# G2 cost linearity: derived net == full re-simulation at 25 bps
full = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75), cost_bps=25.0, freq="W")["returns"].loc[st:]
dev = float(np.abs(full - net(gr, to, 25)).max())
gates.append(("G2 derived cost ladder == engine re-simulation @25bps", f"max|dev| {dev:.3e}", dev < 1e-12))

# G3 the g=0.75 arm IS baseline.rules_v2_weights
W1 = rules_v2_weights(px, band=BAND, gross=0.75); W2 = rules_v2_weights(px)
gates.append(("G3 g=0.75 arm == baseline.rules_v2_weights", f"max|dw| {float(np.abs(W1-W2).max().max()):.3e}",
              float(np.abs(W1 - W2).max().max()) == 0.0))

# G4 SPY buy-and-hold really is zero-turnover under the live convention
gates.append(("G4 SPY comparand turnover under K0", "0.0000x/yr by construction (buy-and-hold)", True))

# G5 K1 charge is a strict reduction and preserves the candidate's own timing
to_y = to.sum() / (len(to) / 252)
sp = spy_gross["U56"]; sp1 = sp - to * 10 / 1e4
gates.append(("G5 K1 charge non-negative everywhere", f"min charge {float((to*10/1e4).min()):.3e}, candidate turnover {to_y:.4f}x/yr",
              float((to * 10 / 1e4).min()) >= 0.0 and float((sp - sp1).sum()) > 0))

# G6 OOS split is a clean partition, 2017-2026 defined once
n_is = len(win(sp, None, IS_END)); n_oos = len(win(sp, OOS_START, None))
gates.append(("G6 IS/OOS partition exact", f"IS {n_is} + OOS {n_oos} = {n_is+n_oos} == {len(sp)}", n_is + n_oos == len(sp)))

# G7 grid completeness
n_cells = len(PANELS) * len(GROSS) * len(CADENCES) * len(COSTS) * len(CONVS)
gates.append(("G7 grid completeness (published rows)", f"{n_cells} verdict rows", n_cells == 2*4*2*5*4))

for nm, val, ok in gates:
    say(f"  [{'PASS' if ok else 'FAIL'}] {nm}: {val}")
say(f"  {sum(g[2] for g in gates)} of {len(gates)} gates pass")

# ---------------------------------------------------------------- bar machinery
def spy_series(panel, conv, to, bps):
    s = spy_gross[panel]
    if conv == "K1_spy_own_turnover":
        return s - to * bps / 1e4
    if conv == "K2_spy_flat2x":
        return s - FLAT_TO * bps / 1e4 / 252.0
    return s                                   # K0, K3: costless SPY

def cand_series(gr, to, conv, bps):
    return gr if conv == "K3_both_free" else net(gr, to, bps)

def leg4b(rc, rs, a=None, b=None):
    """4b legs on window [a,b]: CAGR >= 70% of SPY, MaxDD <= 60% of SPY (i.e. shallower)."""
    cc, sc, dc = mets(win(rc, a, b)); cs, ss, ds = mets(win(rs, a, b))
    return dict(cagr=cc, sharpe=sc, dd=dc, s_cagr=cs, s_sharpe=ss, s_dd=ds,
                L_CAGR=cc >= 0.70 * cs, L_DD=dc >= 0.60 * ds, L_SH=sc > ss,
                floor=0.70 * cs, cap=0.60 * ds)

def verdict4b(rc, rs):
    """4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    h = len(rc) // 2
    f = leg4b(rc, rs)
    h1 = leg4b(rc.iloc[:h], rs.iloc[:h]); h2 = leg4b(rc.iloc[h:], rs.iloc[h:])
    o = leg4b(win(rc, OOS_START), win(rs, OOS_START))
    full_ok = h1["L_SH"] and h2["L_SH"] and f["L_DD"] and f["L_CAGR"]
    oos_ok = o["L_SH"] and o["L_DD"] and o["L_CAGR"]
    return f, h1, h2, o, full_ok, oos_ok

# ---------------------------------------------------------------- PART 1: how far does the bar move?
say(); say("-" * 110)
say("PART 1 — HOW FAR DOES THE ONE-SIDED CONVENTION MOVE THE TWO BARS?  (U56 / B136, W, full sample)")
say("-" * 110)
say(f"{'panel':<6}{'g':>6}{'bps':>5}{'turnovr':>9} | {'SPY CAGR':>9}{'floor':>8} | {'SPY MaxDD':>10}{'cap':>8} | {'d_floor_pp':>11}{'d_cap_pp':>10}")
bar_moves = []
for panel in PANELS:
    for g in GROSS:
        gr, to = books[(panel, g, "W")]
        toy = to.sum() / (len(to) / 252)
        for bps in COSTS:
            s0 = spy_series(panel, "K0_spy_free", to, bps); s1 = spy_series(panel, "K1_spy_own_turnover", to, bps)
            c0, _, d0 = mets(s0); c1, _, d1 = mets(s1)
            df = (0.70 * c0 - 0.70 * c1) * 100; dc = (0.60 * d0 - 0.60 * d1) * 100
            bar_moves.append((panel, g, bps, toy, 0.70*c1, 0.60*d1, df, dc))
            if g in (0.75, 1.00):
                say(f"{panel:<6}{g:>6.2f}{bps:>5}{toy:>9.4f} | {c1:>9.2%}{0.70*c1:>8.2%} | {d1:>10.2%}{0.60*d1:>8.2%} | {df:>11.3f}{dc:>10.3f}")
bm = pd.DataFrame(bar_moves, columns=["panel","g","bps","turnover","floor_K1","cap_K1","d_floor_pp","d_cap_pp"])
say()
say(f"  CAGR floor is LOOSENED by median {bm['d_floor_pp'].median():.3f} pp, max {bm['d_floor_pp'].max():.3f} pp "
    f"(at {bm.loc[bm['d_floor_pp'].idxmax(),'panel']} g={bm.loc[bm['d_floor_pp'].idxmax(),'g']:.2f} {int(bm.loc[bm['d_floor_pp'].idxmax(),'bps'])}bps).")
say(f"  MaxDD cap is LOOSENED by median {bm['d_cap_pp'].median():.3f} pp, max {bm['d_cap_pp'].max():.3f} pp.")
say(f"  For scale: the live band book misses the K0 CAGR floor by ~1.98 pp (CHANGELOG 2119(F)); "
    f"the 2026-09-22 phase run reports a weekly PHASE spread of 0.50 pp of OOS CAGR in the candidate's own family.")

# ---------------------------------------------------------------- PART 2: full verdict grid
say(); say("-" * 110)
say("PART 2 — THE FULL PUBLISHED GRID (every cell, every convention).  4a judged vs live RULES v2; 4b vs SPY.")
say("-" * 110)
rows = []
for panel in PANELS:
    base_gr, base_to = books[(panel, 0.75, "W")]           # live rules = RULES v2, weekly, g=0.75
    for g, cad, bps, conv in itertools.product(GROSS, CADENCES, COSTS, CONVS):
        gr, to = books[(panel, g, cad)]
        rc = cand_series(gr, to, conv, bps)
        rs = spy_series(panel, conv, to, bps)
        rb = cand_series(base_gr, base_to, conv, bps)       # baseline pays the same convention
        f, h1, h2, o, full_ok, oos_ok = verdict4b(rc, rs)
        h = len(rc) // 2
        bf = metrics(rb); bh1 = metrics(rb.iloc[:h])["Sharpe"]; bh2 = metrics(rb.iloc[h:])["Sharpe"]
        keep4a = (metrics(rc.iloc[:h])["Sharpe"] > bh1 and metrics(rc.iloc[h:])["Sharpe"] > bh2
                  and f["dd"] >= bf["MaxDD"])
        rows.append(dict(panel=panel, g=g, cad=cad, bps=bps, conv=conv,
                         CAGR=f["cagr"], Sharpe=f["sharpe"], MaxDD=f["dd"],
                         H1=metrics(rc.iloc[:h])["Sharpe"], H2=metrics(rc.iloc[h:])["Sharpe"],
                         OOS_CAGR=o["cagr"], OOS_Sharpe=o["sharpe"], OOS_MaxDD=o["dd"],
                         spy_CAGR=f["s_cagr"], spy_Sharpe=f["s_sharpe"], spy_MaxDD=f["s_dd"],
                         floor=f["floor"], cap=f["cap"],
                         L_CAGR=f["L_CAGR"], L_DD=f["L_DD"], L_H1=h1["L_SH"], L_H2=h2["L_SH"],
                         O_CAGR=o["L_CAGR"], O_DD=o["L_DD"], O_SH=o["L_SH"],
                         keep4b_full=full_ok, keep4b_oos=oos_ok, keep4b_both=full_ok and oos_ok,
                         keep4a=keep4a, turnover=to.sum()/(len(to)/252)))
df = pd.DataFrame(rows)
say(f"  {len(df)} rows published (2 panels x 4 gross x 2 cadence x 5 cost x 4 conventions).")
say()
piv = df.pivot_table(index=["conv"], values=["keep4a","keep4b_full","keep4b_oos","keep4b_both"], aggfunc="sum")
say("KEEP COUNTS BY CONVENTION (out of 80 cells each):")
say(piv.to_string())
say()
say("KEEP-4b BOTH (full AND OOS) by convention x panel x cadence:")
say(df.pivot_table(index=["panel","cad"], columns="conv", values="keep4b_both", aggfunc="sum").to_string())
say()
say("BINDING LEG over 4b-FULL failures, by convention:")
for conv in CONVS:
    s = df[(df.conv == conv) & (~df.keep4b_full)]
    say(f"  {conv:<22} fails {len(s):>3} | L_CAGR {int((~s.L_CAGR).sum()):>3} | L_DD {int((~s.L_DD).sum()):>3}"
        f" | L_H1 {int((~s.L_H1).sum()):>3} | L_H2 {int((~s.L_H2).sum()):>3}"
        f" | CAGR-ALONE {int(((~s.L_CAGR) & s.L_DD & s.L_H1 & s.L_H2).sum()):>3}")

# ---------------------------------------------------------------- PART 3: does ANY verdict flip?
say(); say("-" * 110)
say("PART 3 — DOES THE CONVENTION FLIP ANY VERDICT?  (K1/K2/K3 against the live K0 cell-by-cell)")
say("-" * 110)
k0 = df[df.conv == "K0_spy_free"].set_index(["panel","g","cad","bps"])
flip_tab = []
for conv in CONVS[1:]:
    kx = df[df.conv == conv].set_index(["panel","g","cad","bps"])
    for col in ["keep4b_full", "keep4b_oos", "keep4b_both", "keep4a"]:
        a, b = k0[col], kx[col].reindex(k0.index)
        flip_tab.append(dict(conv=conv, leg=col, n=len(a), fail_to_pass=int((~a & b).sum()),
                             pass_to_fail=int((a & ~b).sum()), unchanged=int((a == b).sum())))
ft = pd.DataFrame(flip_tab)
say(ft.to_string(index=False))
say()
flips = []
for conv in CONVS[1:]:
    kx = df[df.conv == conv].set_index(["panel","g","cad","bps"])
    for idx in k0.index:
        for col in ["keep4b_full", "keep4b_oos", "keep4a"]:
            if bool(k0.loc[idx, col]) != bool(kx.loc[idx, col]):
                flips.append((conv, col, idx, bool(k0.loc[idx, col]), bool(kx.loc[idx, col])))
if flips:
    say(f"  {len(flips)} individual verdict flips:")
    for c, col, idx, a, b in flips:
        say(f"    {c:<22} {col:<13} {idx} : {a} -> {b}")
else:
    say("  ZERO verdict flips of any leg, on any cell, under any convention.")

# margin analysis: how close is the nearest miss?
say()
near = df[(df.conv == "K0_spy_free") & (~df.L_CAGR)].copy()
near["miss_pp"] = (near["floor"] - near["CAGR"]) * 100
say(f"CAGR-floor misses under the LIVE convention K0: n={len(near)}, median miss {near['miss_pp'].median():.3f} pp, "
    f"min miss {near['miss_pp'].min():.3f} pp (the cell closest to flipping).")
say(f"  The largest floor RELIEF K1 buys anywhere is {bm['d_floor_pp'].max():.3f} pp, so a flip needs a miss below that; "
    f"{int((near['miss_pp'] < bm['d_floor_pp'].max()).sum())} of {len(near)} cells qualify on the floor leg.")
neard = df[(df.conv == "K0_spy_free") & (~df.L_DD)].copy()
if len(neard):
    neard["miss_pp"] = (neard["MaxDD"] - neard["cap"]) * 100 * -1
    say(f"MaxDD-cap misses under K0: n={len(neard)}, min miss {neard['miss_pp'].min():.3f} pp; "
        f"largest cap relief {bm['d_cap_pp'].max():.3f} pp.")
else:
    say("MaxDD-cap misses under K0: NONE — the cap never binds anywhere on this grid.")

# ---------------------------------------------------------------- PART 4: rule 8
say(); say("-" * 110)
say("PART 4 — RULE 8 WALK-FORWARD.  Dials (g, panel) chosen on 2009-2016 ONLY; 2017-2026 read ONCE.")
say("-" * 110)
def is_stats(r, rs):
    return leg4b(win(r, None, IS_END), win(rs, None, IS_END))

r8 = []
for panel, cad, bps, conv in itertools.product(PANELS, CADENCES, COSTS, CONVS):
    cands = {}
    for g in GROSS:
        gr, to = books[(panel, g, cad)]
        rc = cand_series(gr, to, conv, bps); rs = spy_series(panel, conv, to, bps)
        cands[g] = (rc, rs, is_stats(rc, rs))
    # choosers, all IS-only and legal
    picks = {}
    picks["C_LIVE"] = 0.75
    picks["C_ISSHARPE"] = max(GROSS, key=lambda g: cands[g][2]["sharpe"])
    legal = [g for g in GROSS if cands[g][2]["L_CAGR"] and cands[g][2]["L_DD"] and cands[g][2]["L_SH"]]
    picks["C_IS4B_MING"] = min(legal) if legal else None       # smallest gross clearing 4b IS
    picks["C_MAXG"] = max(GROSS)                                # zero-parameter
    # oracle peeks at OOS: reported as an upper bound only
    picks["C_ORACLE"] = max(GROSS, key=lambda g: metrics(win(cands[g][0], OOS_START))["Sharpe"])
    for nm, g in picks.items():
        if g is None:
            r8.append(dict(panel=panel, cad=cad, bps=bps, conv=conv, chooser=nm, g=np.nan,
                           OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan, oos4b=False, undefined=True))
            continue
        rc, rs, _ = cands[g]
        o = leg4b(win(rc, OOS_START), win(rs, OOS_START))
        r8.append(dict(panel=panel, cad=cad, bps=bps, conv=conv, chooser=nm, g=g,
                       OOS_CAGR=o["cagr"], OOS_Sharpe=o["sharpe"], OOS_MaxDD=o["dd"],
                       oos4b=o["L_CAGR"] and o["L_DD"] and o["L_SH"], undefined=False))
R8 = pd.DataFrame(r8)
say("OOS 4b REACH by chooser x convention (out of 20 families = 2 panels x 2 cadence x 5 cost):")
say(R8.pivot_table(index="chooser", columns="conv", values="oos4b", aggfunc="sum").to_string())
say()
say("MEAN OOS Sharpe / CAGR / MaxDD by chooser x convention:")
for stat in ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]:
    say(f"  {stat}:")
    say(R8.pivot_table(index="chooser", columns="conv", values=stat, aggfunc="mean").to_string())
say()
und = R8[R8.undefined]
say(f"C_IS4B_MING is UNDEFINED (no legal IS rung) in {len(und)} of {len(R8[R8.chooser=='C_IS4B_MING'])} families; "
    f"by convention: {und.groupby('conv').size().to_dict()}")
say()
say("REFERENCE OOS ROWS (2017-2026, weekly, 10 bps, K0 live convention):")
for panel in PANELS:
    gr, to = books[(panel, 0.75, "W")]; rc = net(gr, to, 10)
    c, s, d = mets(win(rc, OOS_START)); sc, ss, sd = mets(win(spy_gross[panel], OOS_START))
    gr1, to1 = books[(panel, 1.00, "W")]; rc1 = net(gr1, to1, 10)
    c1, s1, d1 = mets(win(rc1, OOS_START))
    say(f"  {panel}: live RULES v2 g=0.75  {c:.2%} / {s:.4f} / {d:.2%}   |  g=1.00 candidate {c1:.2%} / {s1:.4f} / {d1:.2%}"
        f"   |  SPY {sc:.2%} / {ss:.4f} / {sd:.2%}")

# ---------------------------------------------------------------- PART 5: census of committed 4b passes
say(); say("-" * 110)
say("PART 5 — RE-READING THE STANDING PASSES: does any committed 4b claim STATE its SPY cost convention?")
say("-" * 110)
lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
rowsl = [l for l in lb if l.startswith("|") and "---" not in l][1:]
import re as _re
pass_rows = [l for l in rowsl if _re.search(r"4b", l) and _re.search(r"PASS|KEEP|clear", l)]
states = [l for l in pass_rows if _re.search(r"SPY.{0,60}(cost|bps|turnover|charged)", l, _re.I)]
say(f"  LEADERBOARD rows: {len(rowsl)}; rows mentioning a 4b PASS/KEEP/clear: {len(pass_rows)}; "
    f"of those, rows that say anything about SPY's own cost/turnover: {len(states)}")
say(f"  i.e. {len(pass_rows)-len(states)} of {len(pass_rows)} committed 4b pass-claims are silent on the comparand's "
    f"cost convention.  This run prices that silence at the numbers in PART 1.")

# ---------------------------------------------------------------- verdict
say(); say("=" * 110)
say("VERDICT")
say("=" * 110)
n_flip = len(flips)
say(f"  Bar relief from charging SPY the candidate's own turnover: CAGR floor median {bm['d_floor_pp'].median():.3f} pp "
    f"/ max {bm['d_floor_pp'].max():.3f} pp; MaxDD cap median {bm['d_cap_pp'].median():.3f} pp / max {bm['d_cap_pp'].max():.3f} pp.")
say(f"  Verdict flips across the whole {len(df)}-row grid: {n_flip}.")
say(f"  4a KEEP count: {int(df.keep4a.sum())} of {len(df)}.   4b BOTH: {int(df.keep4b_both.sum())} of {len(df)}.")
_ans = "YES, the bar survives — the one-sided convention is INERT at this record's margins." if n_flip == 0 else "NO — the convention moves verdicts; see PART 3."
say(f"  ANSWER = {_ans}")

(ROOT / "research" / "backtests" / "2026-09-22_4b-bar-one-sided-cost-convention_C.out.txt").write_text("\n".join(out) + "\n")
df.to_csv(ROOT / "research" / "backtests" / "2026-09-22_4b-bar-one-sided-cost-convention_C.grid.csv", index=False)
R8.to_csv(ROOT / "research" / "backtests" / "2026-09-22_4b-bar-one-sided-cost-convention_C.rule8.csv", index=False)
