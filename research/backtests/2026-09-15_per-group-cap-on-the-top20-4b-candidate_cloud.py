#!/usr/bin/env python3
"""QUEUE idea 897 — does-a-PER-GROUP-CAP-keep-the-TOP20-4b-pass   (cloud, 2026-09-15).

QUESTION (pre-registered, verbatim from QUEUE.md idea 897)
    "the standing 4b candidate (u56 TOP20 composite no-vol-scaler, monthly, gross g, cash never
     respread) has never been priced under a diversification constraint, and no allocator funds a
     20-name book that may sit 14 deep in one sleeve.  Cap admissions at m names per group,
     weight unchanged at g/20 with the shortfall to cash, and report every cell.
     Max 2 params (cap m, group scheme)."

THE HYPOTHESES, written out in full BEFORE any number below was read
    H_BINDS  the cap is a real constraint on this book: at some m <= 6 the parent's realised
             holdings are cut materially (median admitted names < 20 on >= 20% of rebalances).
             If the cap never binds the whole question is empty and everything else is moot.
    H_KEEP   the capped book still clears PROTOCOL 4b (Sharpe > SPY in BOTH halves AND out of
             sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) at the PROTOCOL cell
             (10 bps, next-day fills, monthly) for at least one cap that BINDS under H_BINDS.
    H_FREE   diversification is free on this book: the median CAGR give-up of a binding cap
             versus the uncapped parent is <= 1.00 pp/yr at matched gross.
    Declared before running: H_KEEP is the one that matters for capital.  H_FREE is the price tag.

THE BOOK B*, IMPORTED not re-typed (2026-09-04 shelf KEEP, re-published by idea 879 lane B)
    signal    baseline.score(px, vol_scale=False) — mean of the cross-sectional percentile ranks
              of (px[t-21]/px[t-252]-1), (px/px[t-126]-1), (px/px[t-63]-1), times 1.0 if the close
              is above its 200d mean and 0.5 if not.  NO vol scaler.
    gate      px > 200d MA  AND  vol20 (annualised, 20d) < 0.60
    book      top 20 eligible by signal, equal weight g/20, shortfall to CASH, NEVER respread
    cadence   MONTHLY (engine's calendar-month-end mask), fills t+1, 10 bps
    gross     g = 0.65 is IMPORTED from idea 879's published pass rung and is NOT tuned here.
              g = 0.75 (the 2026-09-04 shelf's own rung) is carried as a reported AUDIT axis.

THE TWO TUNED PARAMETERS (the only two; every value of both is reported)
    CAP m     {2, 3, 4, 5, 6, 8, 10, 20}.  m = 20 cannot bind (no group is larger than 20) and is
              therefore the reproduction control: it must equal the uncapped parent EXACTLY.
    SCHEME    JSON4   research/universe.json's own four groups: broad / sectors /
                      bonds_fx_commod / megacap.  Mechanical, no judgement.
              SLEEVE2 ETF vs single stock: the 20 megacap names against the 36 funds.
                      Also mechanical — it is the megacap group against its complement.
    Nothing else is chosen.  COST {10, 25} bps and GROSS {0.65, 0.75} are AUDIT axes: every cell
    is printed and no cell is selected for reporting.

CAP MECHANICS (stated before the run; the honest analogue of the book's own cash clause)
    On each rebalance date, walk the eligible names in descending composite and admit a name only
    if its group already holds fewer than m admitted names; stop at 20 admitted.  Each admitted
    name is held at g/20 — the SAME weight as in the parent — so a binding cap leaves the residual
    in CASH and never respreads it, exactly as the parent does when fewer than 20 names are
    eligible.  Respreading would be a different, unpriced book (idea 81).

PROTOCOL rule 8 walk-forward (required, and read once)
    Parameters chosen on 2009-01-13..2016-12-31 ONLY, by a selector declared here before the run:
        IS-PICK   the (SCHEME, m) cell with the highest IS Sharpe at the PROTOCOL cell
                  (g = 0.65, 10 bps, monthly).  Ties broken by the smaller m (more constrained).
    OOS 2017-01-01.. is then read ONCE for that cell, against
        PARENT    m = 20 (the uncapped book) — the do-nothing control
        RULES v2  the live book (baseline.rules_v2_weights, weekly)
        SPY       buy and hold
    Both KEEP paths (4a against RULES v2 live, 4b against SPY) are evaluated on every cell,
    full sample and both halves, and again on the OOS window.

GATES, printed before any hypothesis is read
    G1  m = 20 (which cannot bind) reproduces the uncapped parent to 0.0 on weights and returns,
        both schemes.
    G2  the cap is monotone: admitted-name count is non-decreasing in m, every rebalance date.
    G3  the record's published parent reproduces its own committed triple from idea 879's memo
        (12.69% / 1.201 / -17.11% at g=0.65, 10 bps, monthly) to within 0.02pp / 0.01.

A TIE CONVENTION, disclosed because the run had to pick one and the pick moves the parent
    The composite is a mean of three cross-sectional PERCENTILE ranks, so exact ties at the
    20th place are common: on 20 of 225 rebalance dates the record's published cut
    (`rank(ascending=False) <= 20`, pandas' average-tie ranks) admits only 19 names, because a
    straddling pair both score 20.5.  A cap has to walk names in a strict order, so this run's
    book uses SORT-TIE: descending composite, ties broken by pandas' stable sort (ticker order in
    the frame), first 20 admitted.  Both parents are run and both are printed:
        RANKPAR  rank <= 20  — the record's convention, the G3 reference
        SORTPAR  sort-tie top 20 — this run's uncapped arm, the G1 reference and the m = 20 cell
    The gap between them is a published number below, not a rounding difference to wave at.

CAVEATS carried, not buried
    * SURVIVORSHIP.  research/universe.json is the CURRENT constituent list (idea 54), so every
      level here is optimistic and both 4b level bars are easier on this panel than on a
      point-in-time one.  The cap comparison is a same-names, same-days difference and is much
      less exposed than the levels.
    * The group labels are a static, present-day classification.  They are not future data (the
      groups are fixed for the whole sample) but they are not point-in-time either.
    * 2020 and 2022 are the only real stress episodes in the window.
    * Rule 6: nothing here is a rules change; a rules change is a Sunday-review decision.
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, metrics                                  # noqa: E402

SLUG = "2026-09-15_per-group-cap-on-the-top20-4b-candidate_cloud"
OUT = ROOT / "research" / "backtests"
pd.set_option("display.width", 200)

N_BOOK, MAX_VOL = 20, 0.60
CAPS = [2, 3, 4, 5, 6, 8, 10, 20]
GROSSES = [0.65, 0.75]
COSTS = [10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
EXCLUDE = {"BTC-USD", "ETH-USD"}

# ---------------------------------------------------------------- groups
U = json.loads((ROOT / "research" / "universe.json").read_text())
JSON4 = {t: g for g, names in U.items() for t in names if t not in EXCLUDE}
SLEEVE2 = {t: ("stock" if g == "megacap" else "etf") for t, g in JSON4.items()}
SCHEMES = {"JSON4": JSON4, "SLEEVE2": SLEEVE2}

# ---------------------------------------------------------------- the book
px = load_universe()
comp, above, vol20 = score(px, vol_scale=False)
elig = comp.where(above & (vol20 < MAX_VOL))
REBAL = (lambda idx: (pd.Series(idx.to_period("M"), index=idx) != pd.Series(idx.to_period("M"), index=idx).shift(-1)))(px.index)
REBAL_DATES = px.index[REBAL.values]


def admitted(d, m, groups):
    """Names admitted on rebalance date d under cap m; descending composite, cap per group."""
    s = elig.loc[d].dropna().sort_values(ascending=False)
    cnt, out = {}, []
    for t in s.index:
        g = groups.get(t)
        if g is None:
            continue
        if cnt.get(g, 0) >= m:
            continue
        cnt[g] = cnt.get(g, 0) + 1
        out.append(t)
        if len(out) == N_BOOK:
            break
    return out


def weights_for(m, scheme, gross):
    """Daily weight frame; correct on every rebalance date (the only rows engine reads)."""
    groups = SCHEMES[scheme]
    W = pd.DataFrame(0.0, index=REBAL_DATES, columns=px.columns)
    for d in REBAL_DATES:
        names = admitted(d, m, groups)
        if names:
            W.loc[d, names] = gross / N_BOOK
    return W.reindex(px.index).ffill().fillna(0.0)


def counts_frame(m, scheme):
    groups = SCHEMES[scheme]
    return pd.Series({d: len(admitted(d, m, groups)) for d in REBAL_DATES})


def legs(r, spy):
    """PROTOCOL 4b legs on a return series against SPY over the same index."""
    a, s = metrics(r), metrics(spy)
    h = len(r) // 2
    a1, a2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    s1, s2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=a1, H2=a2,
                spyH1=s1, spyH2=s2, spyCAGR=s["CAGR"], spyMaxDD=s["MaxDD"],
                dd_ok=a["MaxDD"] >= 0.60 * s["MaxDD"], cagr_ok=a["CAGR"] >= 0.70 * s["CAGR"],
                h1_ok=a1 > s1, h2_ok=a2 > s2)


def four_b(r, spy):
    L = legs(r, spy)
    return L["h1_ok"] and L["h2_ok"] and L["dd_ok"] and L["cagr_ok"], L


def four_a(r, base):
    """4a: Sharpe > live baseline in BOTH halves and MaxDD no worse."""
    h = len(r) // 2
    return (metrics(r.iloc[:h])["Sharpe"] > metrics(base.iloc[:h])["Sharpe"]
            and metrics(r.iloc[h:])["Sharpe"] > metrics(base.iloc[h:])["Sharpe"]
            and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# ---------------------------------------------------------------- gates
print("=" * 100)
print("GATES (printed before any hypothesis is read)")
print("=" * 100)

W20_j, W20_s = weights_for(20, "JSON4", 0.65), weights_for(20, "SLEEVE2", 0.65)
rank = elig.rank(axis=1, ascending=False)
W_rankpar = ((rank <= N_BOOK).astype(float) * (0.65 / N_BOOK)).loc[REBAL_DATES] \
    .reindex(px.index).ffill().fillna(0.0)
# SORTPAR: the uncapped arm of this run — an unreachable cap is the same walk with no cap
W_sortpar = weights_for(10 ** 6, "JSON4", 0.65)
g1a = float((W20_j - W_sortpar).abs().to_numpy().max())
g1b = float((W20_s - W_sortpar).abs().to_numpy().max())
r20 = backtest(px, W20_j, cost_bps=10, freq="M")["returns"]
rsp = backtest(px, W_sortpar, cost_bps=10, freq="M")["returns"]
rpa = backtest(px, W_rankpar, cost_bps=10, freq="M")["returns"]
g1c = float((r20 - rsp).abs().max())
print(f"G1 m=20 reproduces the uncapped SORTPAR: max|dw| JSON4 {g1a:.3e}  SLEEVE2 {g1b:.3e}  "
      f"max|dr| {g1c:.3e}   -> {'PASS' if max(g1a, g1b, g1c) == 0.0 else 'FAIL'}")
n_tie = int(sum(1 for d in REBAL_DATES
                if set(elig.loc[d].dropna().sort_values(ascending=False).index[:N_BOOK])
                != set(rank.loc[d][rank.loc[d] <= N_BOOK].index)))
print(f"   tie convention: RANKPAR and SORTPAR differ on {n_tie} of {len(REBAL_DATES)} "
      f"rebalance dates (boundary ties in the composite)")

cnt_by_m = {m: counts_frame(m, "JSON4") for m in CAPS}
mono = all((cnt_by_m[CAPS[i + 1]] >= cnt_by_m[CAPS[i]]).all() for i in range(len(CAPS) - 1))
print(f"G2 admitted-count monotone in m on all {len(REBAL_DATES)} rebalance dates: "
      f"{'PASS' if mono else 'FAIL'}")

start = px.index[260]
spy = px["SPY"].pct_change().fillna(0).loc[start:]
pm, sm_par = metrics(rpa.loc[start:]), metrics(rsp.loc[start:])
print(f"G3 RANKPAR vs idea 879 memo (12.69% / 1.201 / -17.11%): "
      f"{pm['CAGR']:.2%} / {pm['Sharpe']:.3f} / {pm['MaxDD']:.2%}   -> "
      f"{'PASS' if abs(pm['CAGR']-0.1269) < 2e-4 and abs(pm['Sharpe']-1.201) < 0.01 and abs(pm['MaxDD']+0.1711) < 2e-4 else 'FAIL'}")
print(f"   PUBLISHED COST OF THE TIE CONVENTION: SORTPAR (this run's m=20 arm) "
      f"{sm_par['CAGR']:.2%} / {sm_par['Sharpe']:.3f} / {sm_par['MaxDD']:.2%}  "
      f"= {100*(sm_par['CAGR']-pm['CAGR']):+.3f} pp CAGR, {sm_par['Sharpe']-pm['Sharpe']:+.4f} Sharpe "
      f"vs the record's convention")

# ---------------------------------------------------------------- H_BINDS
print()
print("=" * 100)
print("H_BINDS — does the cap actually constrain this book?")
print("=" * 100)
bind_rows = []
for scheme in SCHEMES:
    for m in CAPS:
        c = counts_frame(m, scheme)
        bind_rows.append(dict(scheme=scheme, m=m, median_names=c.median(),
                              share_short=float((c < N_BOOK).mean()), min_names=int(c.min())))
bind = pd.DataFrame(bind_rows)
print(bind.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
BINDS = {(r.scheme, r.m) for r in bind.itertuples() if r.share_short >= 0.20 and r.m <= 6}
h_binds = len(BINDS) > 0
print(f"\nH_BINDS: {'PASS' if h_binds else 'FAIL'} — {len(BINDS)} of 16 cells cut the book on "
      f">=20% of rebalances at m<=6: {sorted(BINDS)}")

# ---------------------------------------------------------------- full grid
print()
print("=" * 100)
print("FULL GRID — every cell, nothing selected  (2 tuned params x 2 audit axes)")
print("=" * 100)
base_r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
rows, ret_cache = [], {}
for scheme in SCHEMES:
    for m in CAPS:
        W = weights_for(m, scheme, 1.0)          # gross scales the weights linearly
        for g in GROSSES:
            for c in COSTS:
                res = backtest(px, W * g, cost_bps=c, freq="M")
                r = res["returns"].loc[start:]
                ret_cache[(scheme, m, g, c)] = r
                ok4b, L = four_b(r, spy)
                rows.append(dict(scheme=scheme, m=m, gross=g, bps=c, CAGR=L["CAGR"],
                                 Sharpe=L["Sharpe"], MaxDD=L["MaxDD"], H1=L["H1"], H2=L["H2"],
                                 h1=L["h1_ok"], h2=L["h2_ok"], dd=L["dd_ok"], cagr=L["cagr_ok"],
                                 KEEP4b=ok4b, KEEP4a=four_a(r, base_r),
                                 turn_yr=res["turnover"].loc[start:].sum() / metrics(r)["Years"]))
grid = pd.DataFrame(rows)
grid.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
for c in COSTS:
    for g in GROSSES:
        sub = grid[(grid.bps == c) & (grid.gross == g)]
        print(f"\n--- gross {g}, {c} bps ---")
        print(sub[["scheme", "m", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "h1", "h2", "dd",
                   "cagr", "KEEP4b", "KEEP4a", "turn_yr"]].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
sm = metrics(spy)
print(f"\nSPY over the same sample: CAGR {sm['CAGR']:.2%}  Sharpe {sm['Sharpe']:.3f}  "
      f"MaxDD {sm['MaxDD']:.2%}  halves {metrics(spy.iloc[:len(spy)//2])['Sharpe']:.3f} / "
      f"{metrics(spy.iloc[len(spy)//2:])['Sharpe']:.3f}   "
      f"[4b bars: CAGR floor {0.70*sm['CAGR']:.2%}, DD cap {0.60*sm['MaxDD']:.2%}]")
bm = metrics(base_r)
print(f"RULES v2 (live): CAGR {bm['CAGR']:.2%}  Sharpe {bm['Sharpe']:.3f}  MaxDD {bm['MaxDD']:.2%}")

# ---------------------------------------------------------------- H_KEEP / H_FREE
print()
print("=" * 100)
print("H_KEEP and H_FREE")
print("=" * 100)
proto = grid[(grid.bps == 10) & (grid.gross == 0.65)]
keep_binding = [(r.scheme, r.m) for r in proto.itertuples()
                if r.KEEP4b and (r.scheme, r.m) in BINDS]
print(f"H_KEEP: {'PASS' if keep_binding else 'FAIL'} — binding caps that still clear 4b at the "
      f"PROTOCOL cell: {keep_binding}")
gaps = []
for g in GROSSES:
    par_cagr = {s: proto_g.CAGR for s, proto_g in
                grid[(grid.bps == 10) & (grid.gross == g) & (grid.m == 20)].set_index("scheme").iterrows()}
    for r in grid[(grid.bps == 10) & (grid.gross == g)].itertuples():
        if (r.scheme, r.m) in BINDS:
            gaps.append(dict(scheme=r.scheme, m=r.m, gross=g,
                             dCAGR_pp=100 * (r.CAGR - par_cagr[r.scheme])))
gapdf = pd.DataFrame(gaps)
if len(gapdf):
    print(gapdf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    med = gapdf.dCAGR_pp.median()
    print(f"H_FREE: {'PASS' if abs(med) <= 1.00 else 'FAIL'} — median CAGR give-up of a binding "
          f"cap {med:+.3f} pp/yr (bar: |median| <= 1.00 pp)")

# ------------------------------------------------- H_DEGROSS (control, declared with the others)
# A binding cap holds FEWER than 20 names at the SAME g/20 weight, so it de-grosses.  The record
# has priced the pure gross dial on this exact book (idea 879: Sharpe moves 0.005 over the whole
# 0.50 -> 1.00 ladder).  So: is the cap's damage just de-grossing, or does it cost Sharpe on top?
# Control: the UNCAPPED parent re-run at each capped cell's own realised mean gross.
print()
print("=" * 100)
print("H_DEGROSS control — capped cell vs the UNCAPPED parent at its OWN realised mean gross")
print("=" * 100)
W_un = weights_for(10 ** 6, "JSON4", 1.0)
ctrl = []
for scheme in SCHEMES:
    for m in CAPS:
        r = ret_cache[(scheme, m, 0.65, 10)]
        W = weights_for(m, scheme, 0.65)
        gbar = float(backtest(px, W, cost_bps=10, freq="M")["weights"].sum(axis=1).loc[start:].mean())
        rc = backtest(px, W_un * gbar, cost_bps=10, freq="M")["returns"].loc[start:]
        mc, mr = metrics(rc), metrics(r)
        ctrl.append(dict(scheme=scheme, m=m, gbar=gbar, cap_Sharpe=mr["Sharpe"],
                         matched_parent_Sharpe=mc["Sharpe"], dSharpe=mr["Sharpe"] - mc["Sharpe"],
                         cap_CAGR=mr["CAGR"], matched_parent_CAGR=mc["CAGR"],
                         dCAGR_pp=100 * (mr["CAGR"] - mc["CAGR"])))
ctrldf = pd.DataFrame(ctrl)
print(ctrldf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
ctrldf.to_csv(OUT / f"{SLUG}.degross_control.csv", index=False)
bind_ctrl = ctrldf[[(r.scheme, r.m) in BINDS for r in ctrldf.itertuples()]]
print(f"\nH_DEGROSS: over the {len(bind_ctrl)} BINDING cells the cap costs "
      f"{bind_ctrl.dSharpe.median():+.4f} Sharpe (median) and {bind_ctrl.dCAGR_pp.median():+.3f} pp "
      f"CAGR against a gross-matched uncapped parent.  Reference: idea 879's pure gross dial moves "
      f"Sharpe by 0.005 over 0.50->1.00 on this same book.")

# ---------------------------------------------------------------- rule 8
print()
print("=" * 100)
print("PROTOCOL RULE 8 — walk-forward.  Selector declared before the run; OOS read ONCE.")
print("=" * 100)
is_rows = []
for (scheme, m, g, c), r in ret_cache.items():
    if g != 0.65 or c != 10:
        continue
    is_rows.append(dict(scheme=scheme, m=m, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"]))
isdf = pd.DataFrame(is_rows).sort_values(["IS_Sharpe", "m"], ascending=[False, True])
print(isdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
pick = isdf.iloc[0]
print(f"\nIS-PICK (highest IS Sharpe, ties to smaller m): scheme={pick.scheme}  m={int(pick.m)}")

oos_spy = spy.loc[OOS_START:]
wf = []
for label, r in [(f"IS-PICK {pick.scheme} m={int(pick.m)}", ret_cache[(pick.scheme, int(pick.m), 0.65, 10)]),
                 ("SORTPAR m=20 (do-nothing)", ret_cache[("JSON4", 20, 0.65, 10)]),
                 ("RANKPAR (record's parent)", rpa.loc[start:]),
                 ("RULES v2 (live)", base_r), ("SPY", spy)]:
    o = r.loc[OOS_START:]
    mo = metrics(o)
    h = len(o) // 2
    wf.append(dict(arm=label, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                   oosH1=metrics(o.iloc[:h])["Sharpe"], oosH2=metrics(o.iloc[h:])["Sharpe"]))
wfdf = pd.DataFrame(wf).set_index("arm")
print()
print(wfdf.to_string(float_format=lambda x: f"{x:.4f}"))
wfdf.to_csv(OUT / f"{SLUG}.walkforward.csv")

pick_oos = ret_cache[(pick.scheme, int(pick.m), 0.65, 10)].loc[OOS_START:]
ok_oos, L_oos = four_b(pick_oos, oos_spy)
print(f"\nOOS 4b on the IS-PICK: h1 {L_oos['h1_ok']}  h2 {L_oos['h2_ok']}  "
      f"dd {L_oos['dd_ok']} ({L_oos['MaxDD']:.2%} vs cap {0.60*L_oos['spyMaxDD']:.2%})  "
      f"cagr {L_oos['cagr_ok']} ({L_oos['CAGR']:.2%} vs floor {0.70*L_oos['spyCAGR']:.2%})  "
      f"-> 4b {'PASS' if ok_oos else 'FAIL'}")
print(f"OOS 4a on the IS-PICK vs RULES v2 live: {four_a(pick_oos, base_r.loc[OOS_START:])}")

bind.to_csv(OUT / f"{SLUG}.binding.csv", index=False)
print("\nWrote: .grid.csv  .binding.csv  .walkforward.csv")
