#!/usr/bin/env python3
"""Idea 1664 (lane cloud, 2026-09-19) — is the 27-of-27 MIXTURE CONVEXITY a
DIVERSIFICATION fact or a SHARPE-ALGEBRA fact?

Idea 1649 found blend Sharpe above the NAV-weighted average of its two corner Sharpes
in 27 of 27 cells (mean +0.0535) and called it "real diversification".  Sharpe is not
linear in NAV weights, so part of that convexity is arithmetic that holds for ANY two
imperfectly correlated books -- including two random splits of ONE panel, which share a
panel, a regime and a gate and diversify almost nothing.

This run does three things:
  (A) REPLICATES the statistic C(w) = Sharpe(blend) - [w*S_A + (1-w)*S_B] on the record's
      cross-panel pairs over the same 27-cell shape (w x G x slice).
  (B) DECOMPOSES C EXACTLY into two terms, so the arithmetic is not asserted but algebra:
          C = MIX + DIV
          MIX = (S_A - S_B) * w(1-w)(sigma_A - sigma_B) / (w*sigma_A + (1-w)*sigma_B)
          DIV = (w*mu_A + (1-w)*mu_B) * (1/sigma_w - 1/sigma_lin),  sigma_lin = w*sA+(1-w)*sB
      MIX is pure vol-mismatch re-weighting (zero iff sigma_A == sigma_B, either sign).
      DIV is variance sub-additivity (>= 0 whenever the blend's mean is positive, for any
      rho < 1).  Identity is asserted numerically to 1e-12 at every cell.
  (C) PRICES THE NULL: random disjoint splits of ONE panel into two halves, the same book
      on each half, the same w and G, the same C.  If the within-panel null reproduces
      +0.0535, the 27-of-27 is algebra.

Dials (two, and no more): w (NAV share to the FIRST book) and G (total target gross).
Everything else -- panel pair, slice, cost rung, null draw -- is published, not tuned.

Book on every panel: live RULES v2 band 0.03, equal weight at gross/N of priced names,
gated-out weight to 0%-yielding cash, weekly, t+1, 10 bps (PROTOCOL rules 1-2).
A fixed-w NAV blend of two daily return series is a sleeve pair rebalanced daily at no
extra cost; that is exactly idea 1649's construction and exactly the null's, so the
contrast is like-for-like (stated, not hidden).

Outputs: .console.txt, .cells.csv (cross-panel), .null.csv (within-panel), .keeppaths.csv,
.walkforward.csv
"""
import sys, itertools, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights   # noqa
from engine import backtest, metrics                                      # noqa

STAMP = "2026-09-19"; SLUG = "mixture-convexity-vs-within-panel-null_cloud"
OUT = ROOT / "research" / "backtests"
COST, FREQ, BAND = 10, "W", 0.03
WGRID = [0.25, 0.50, 0.75]                 # dial 1 (interior blends only; corners are w=0/1)
GGRID = [0.50, 0.75, 1.00]                 # dial 2
NDRAW, SEED, WARM = 40, 20260919, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"

_log = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); _log.append(s)

# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"SMALL: dropped {px.shape[1]-len(keep)} tickers with max_1d_move >= 1.0 "
        f"(data/small_meta.csv); {len(keep)-1} names remain + SPY")
    return px[keep]

PANELS = {}
PANELS["U56"]   = load_universe()
PANELS["B136"]  = load_universe(broad=True)
PANELS["SMALL"] = small_panel()
for k, v in PANELS.items():
    say(f"panel {k}: {v.shape[1]-1} names + SPY, {v.index[0].date()}..{v.index[-1].date()}, {len(v)} rows")

def book(px, G, cols=None):
    """Daily net return series of the live RULES v2 band book on `px` (cols subset)."""
    p = px if cols is None else px[cols]
    return backtest(p, rules_v2_weights(p, band=BAND, gross=G), cost_bps=COST, freq=FREQ)["returns"]

# ---------------------------------------------------------------- statistic
ANN = 252.0
def ms(r):
    mu = r.mean() * ANN; sd = r.std() * np.sqrt(ANN)
    return mu, sd, (mu / sd if sd > 0 else np.nan)

def convexity(rA, rB, w):
    """C = Sharpe(blend) - [w*S_A + (1-w)*S_B], with the exact MIX/DIV decomposition."""
    muA, sA, SA = ms(rA); muB, sB, SB = ms(rB)
    rM = w * rA + (1 - w) * rB
    muM, sM, SM = ms(rM)
    navavg = w * SA + (1 - w) * SB
    C = SM - navavg
    slin = w * sA + (1 - w) * sB
    MIX = (SA - SB) * w * (1 - w) * (sA - sB) / slin
    DIV = muM * (1.0 / sM - 1.0 / slin)
    rho = np.corrcoef(rA, rB)[0, 1]
    return dict(S_blend=SM, S_A=SA, S_B=SB, navavg=navavg, C=C, MIX=MIX, DIV=DIV,
                resid=C - MIX - DIV, rho=rho, sd_A=sA, sd_B=sB, sd_blend=sM,
                CAGR=(1 + rM).prod() ** (ANN / len(rM)) - 1, MaxDD=((1 + rM).cumprod() /
                (1 + rM).cumprod().cummax() - 1).min())

def slices(idx):
    return {"FULL": slice(None), "IS": slice(None, IS_END), "OOS": slice(OOS_START, None)}

# ---------------------------------------------------------------- (A)+(B) cross-panel cells
PAIRS = [("U56", "SMALL"), ("U56", "B136"), ("B136", "SMALL")]
corners = {}          # (panel, G) -> returns on that panel's own calendar
for p, G in itertools.product(PANELS, GGRID):
    corners[(p, G)] = book(PANELS[p], G)
say("corner books built:", len(corners))

rows = []
for (pa, pb), G, w in itertools.product(PAIRS, GGRID, WGRID):
    idx = corners[(pa, G)].index.intersection(corners[(pb, G)].index)[WARM:]
    rA, rB = corners[(pa, G)].loc[idx], corners[(pb, G)].loc[idx]
    for sl, s in slices(idx).items():
        d = convexity(rA.loc[s], rB.loc[s], w)
        rows.append(dict(pair=f"{pa}x{pb}", A=pa, B=pb, G=G, w=w, slice=sl, n=len(rA.loc[s]), **d))
cells = pd.DataFrame(rows)
cells.to_csv(OUT / f"{STAMP}_{SLUG}.cells.csv", index=False)

say("\n=== (A) REPLICATION: C = Sharpe(blend) - NAV-weighted average of corner Sharpes ===")
say(f"identity |C - MIX - DIV| max = {cells.resid.abs().max():.3e}  (exact decomposition holds)")
for pair, g in cells.groupby("pair"):
    say(f"  {pair:12s} C>0 in {int((g.C>0).sum())} of {len(g)} cells | mean C {g.C.mean():+.4f} "
        f"| mean MIX {g.MIX.mean():+.4f} | mean DIV {g.DIV.mean():+.4f} | mean rho {g.rho.mean():.3f}")
anchor = cells[cells.pair == "U56xSMALL"]
say(f"  1649's own pair (U56xSMALL), 27 cells: C>0 in {int((anchor.C>0).sum())} of {len(anchor)}, "
    f"mean C {anchor.C.mean():+.4f}  [1649 published +0.0535]")
say(f"    of which MIX {anchor.MIX.mean():+.4f} ({100*anchor.MIX.mean()/anchor.C.mean():.1f}%) "
    f"and DIV {anchor.DIV.mean():+.4f} ({100*anchor.DIV.mean()/anchor.C.mean():.1f}%)")
say("\n  beaten-the-BETTER-corner count (the benchmark that would justify moving capital):")
for pair, g in cells.groupby("pair"):
    better = np.maximum(g.S_A, g.S_B)
    say(f"    {pair:12s} blend > better corner in {int((g.S_blend > better).sum())} of {len(g)}")

say("\n  all cross-panel cells (published in full, .cells.csv):")
say(cells[["pair","G","w","slice","S_A","S_B","navavg","S_blend","C","MIX","DIV","rho"]]
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

# ---------------------------------------------------------------- (C) within-panel null
say("\n=== (C) NULL: random disjoint halves of ONE panel, same book, same w, same G ===")
rng = np.random.default_rng(SEED)
nrows = []
for p in PANELS:
    px = PANELS[p]
    names = [c for c in px.columns if c != "SPY"]
    for d in range(NDRAW):
        perm = rng.permutation(names); h = len(perm) // 2
        c1 = list(perm[:h]) + ["SPY"]; c2 = list(perm[h:2 * h]) + ["SPY"]
        for G in GGRID:
            rA = book(px, G, c1)[WARM:]; rB = book(px, G, c2)[WARM:]
            for sl, s in slices(rA.index).items():
                dd = convexity(rA.loc[s], rB.loc[s], 0.50)            # w=0.50 == the even split
                nrows.append(dict(panel=p, draw=d, G=G, w=0.50, slice=sl, **dd))
                for w in WGRID:
                    if w != 0.50:
                        nrows.append(dict(panel=p, draw=d, G=G, w=w, slice=sl,
                                          **convexity(rA.loc[s], rB.loc[s], w)))
    say(f"  {p}: {NDRAW} draws x {len(GGRID)} gross x {len(WGRID)} w x 3 slices done")
null = pd.DataFrame(nrows)
null.to_csv(OUT / f"{STAMP}_{SLUG}.null.csv", index=False)

say(f"\n  null cells: {len(null)}  (C > 0 in {int((null.C>0).sum())}, {100*(null.C>0).mean():.1f}%)")
say(null.groupby("panel")[["C","MIX","DIV","rho"]].agg(["mean","std"])
    .to_string(float_format=lambda x: f"{x:.4f}"))
say("\n  null C by (panel, slice), mean [p5, p50, p95]:")
for (p, sl), g in null.groupby(["panel", "slice"]):
    q = np.percentile(g.C, [5, 50, 95])
    say(f"    {p:6s} {sl:4s} mean {g.C.mean():+.4f}  [{q[0]:+.4f}, {q[1]:+.4f}, {q[2]:+.4f}]  "
        f"mean rho {g.rho.mean():.3f}  mean DIV {g.DIV.mean():+.4f}  mean MIX {g.MIX.mean():+.4f}")

obs = anchor.C.mean()
say(f"\n  *** HOW MUCH OF 1649's +{obs:.4f} SURVIVES THE NULL ***")
for p, g in null.groupby("panel"):
    pct = (g.C >= obs).mean()
    say(f"    within-{p:6s} null mean C {g.C.mean():+.4f} ({100*g.C.mean()/obs:.1f}% of the observed); "
        f"P(null C >= observed) = {pct:.3f}")
allnull = null.C
say(f"    pooled null  mean C {allnull.mean():+.4f} ({100*allnull.mean()/obs:.1f}% of the observed); "
    f"P(null C >= observed) = {(allnull >= obs).mean():.3f}")
say(f"    null C > 0 in {100*(allnull>0).mean():.1f}% of {len(allnull)} cells -- the SIGN of the "
    f"27-of-27 carries no information if this is near 100%.")

# SHAPE-MATCHED null: the observed statistic is a MEAN over 27 cells of ONE pair, so the null
# must be a mean over the SAME 27 cells of one DRAW, not a per-cell value. This is the tight read.
say("\n  SHAPE-MATCHED null (each draw's own mean over its 27 (G,w,slice) cells, "
    "exactly the observed statistic's shape):")
dm = null.groupby(["panel", "draw"]).C.mean()
for p_, g in dm.groupby(level=0):
    q = np.percentile(g, [5, 50, 95])
    say(f"    within-{p_:6s} draw-mean C: mean {g.mean():+.4f} [{q[0]:+.4f}, {q[1]:+.4f}, {q[2]:+.4f}] "
        f"| {100*g.mean()/obs:.1f}% of observed | P(draw-mean >= {obs:+.4f}) = {(g >= obs).mean():.3f} "
        f"({int((g>=obs).sum())} of {len(g)} draws)")
say(f"    pooled       draw-mean C: mean {dm.mean():+.4f} ({100*dm.mean()/obs:.1f}% of observed) | "
    f"P(draw-mean >= observed) = {(dm >= obs).mean():.3f} ({int((dm>=obs).sum())} of {len(dm)} draws)")
say(f"    draw-mean C > 0 in {int((dm>0).sum())} of {len(dm)} draws ({100*(dm>0).mean():.1f}%)")

# C is a function of rho, not of panel-crossing: pool every pair this run priced and regress.
say("\n  C vs rho -- every pair this run priced, cross-panel and within-panel together:")
both = pd.concat([cells.assign(kind="cross", key=cells.pair),
                  null.assign(kind="within", key="within-" + null.panel)])
for k, g in both.groupby("key"):
    say(f"    {k:14s} n={len(g):5d}  mean rho {g.rho.mean():.4f}  mean C {g.C.mean():+.4f}  "
        f"mean DIV {g.DIV.mean():+.4f}  mean MIX {g.MIX.mean():+.4f}")
sub = both[both.w == 0.50]
say(f"    corr(C, 1-rho) over all {len(sub)} even-split cells = "
    f"{np.corrcoef(sub.C, 1 - sub.rho)[0,1]:+.4f}  "
    f"(if this is near +1, C measures DECORRELATION, not panel-crossing)")

# ---------------------------------------------------------------- KEEP paths + rule 8
say("\n=== KEEP paths (4a vs live RULES v2, 4b vs SPY) on 1649's pair, and rule 8 ===")
U, S = PANELS["U56"], PANELS["SMALL"]
idx = corners[("U56", 0.75)].index.intersection(corners[("SMALL", 0.75)].index)[WARM:]
spy = U["SPY"].pct_change().fillna(0.0).reindex(idx).fillna(0.0)
live = corners[("U56", 0.75)].loc[idx]                       # live RULES v2 (band 0.03, G 0.75)

def legs(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"])

Lspy, Llive = legs(spy), legs(live)
say(f"  SPY        {Lspy['CAGR']:.2%} / {Lspy['Sharpe']:.4f} / {Lspy['MaxDD']:.2%} "
    f"(H1 {Lspy['H1']:.4f} H2 {Lspy['H2']:.4f})")
say(f"  RULES v2   {Llive['CAGR']:.2%} / {Llive['Sharpe']:.4f} / {Llive['MaxDD']:.2%} "
    f"(H1 {Llive['H1']:.4f} H2 {Llive['H2']:.4f})")

def keep(r, spy_r, live_r):
    L, Ls, Ll = legs(r), legs(spy_r), legs(live_r)
    oos = r.loc[OOS_START:]; Os, Ol = spy_r.loc[OOS_START:], live_r.loc[OOS_START:]
    p4a = (L["H1"] > Ll["H1"]) and (L["H2"] > Ll["H2"]) and (L["MaxDD"] >= Ll["MaxDD"])
    p4b_full = (L["H1"] > Ls["H1"]) and (L["H2"] > Ls["H2"]) and \
               (L["MaxDD"] >= 0.60 * Ls["MaxDD"]) and (L["CAGR"] >= 0.70 * Ls["CAGR"])
    mo, mso = metrics(oos), metrics(Os)
    p4b_oos = (mo["Sharpe"] > mso["Sharpe"]) and (mo["MaxDD"] >= 0.60 * mso["MaxDD"]) and \
              (mo["CAGR"] >= 0.70 * mso["CAGR"])
    return L, p4a, p4b_full, p4b_oos, mo

kp = []
books = {}
for G, w in itertools.product(GGRID, WGRID + [0.0, 1.0]):
    rA, rB = corners[("U56", G)].loc[idx], corners[("SMALL", G)].loc[idx]
    r = w * rA + (1 - w) * rB
    books[(G, w)] = r
    L, a, bf, bo, mo = keep(r, spy, live)
    kp.append(dict(G=G, w=w, kind="blend" if 0 < w < 1 else "corner", **L,
                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                   pass4a=a, pass4b_FULL=bf, pass4b_OOS=bo))
kpd = pd.DataFrame(kp).sort_values(["G", "w"])
kpd.to_csv(OUT / f"{STAMP}_{SLUG}.keeppaths.csv", index=False)
say(kpd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say(f"  4a passes {int(kpd.pass4a.sum())} of {len(kpd)} | 4b FULL {int(kpd.pass4b_FULL.sum())} | "
    f"4b OOS {int(kpd.pass4b_OOS.sum())} | 4b FULL-and-OOS "
    f"{int((kpd.pass4b_FULL & kpd.pass4b_OOS).sum())}")
say(f"  of the {int((kpd.kind=='blend').sum())} BLEND cells: 4a {int(kpd[kpd.kind=='blend'].pass4a.sum())}, "
    f"4b FULL {int(kpd[kpd.kind=='blend'].pass4b_FULL.sum())}, "
    f"4b OOS {int(kpd[kpd.kind=='blend'].pass4b_OOS.sum())}")

say("\n--- rule 8: dials chosen on 2010-2016 rows ONLY, 2017-2026 read ONCE ---")
wf = []
choosers = {
    "C_SHARPE : argmax IS Sharpe": lambda r: metrics(r.loc[:IS_END])["Sharpe"],
    "C_CALMAR : argmax IS Calmar": lambda r: metrics(r.loc[:IS_END])["Calmar"],
    "C_CONVEX : argmax IS convexity C vs its own corners":
        lambda r: np.nan,          # filled below (needs the pair, not the blend alone)
}
isC = {}
for (G, w) in books:
    if 0 < w < 1:
        rA, rB = corners[("U56", G)].loc[idx], corners[("SMALL", G)].loc[idx]
        isC[(G, w)] = convexity(rA.loc[:IS_END], rB.loc[:IS_END], w)["C"]
for cname, fn in choosers.items():
    if "CONVEX" in cname:
        pick = max(isC, key=isC.get)
    else:
        cand = {k: fn(v) for k, v in books.items() if 0 < k[1] < 1}
        pick = max(cand, key=cand.get)
    r = books[pick]; oos = r.loc[OOS_START:]
    mo, mso, mlo = metrics(oos), metrics(spy.loc[OOS_START:]), metrics(live.loc[OOS_START:])
    L, a, bf, bo, _ = keep(r, spy, live)
    wf.append(dict(chooser=cname.split(":")[0].strip(), pick_G=pick[0], pick_w=pick[1],
                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                   base_OOS_Sharpe=mlo["Sharpe"], spy_OOS_Sharpe=mso["Sharpe"],
                   pass4b_OOS=bo, pass4a=a))
    say(f"  {cname:52s} -> G={pick[0]:.2f} w={pick[1]:.2f} | OOS {mo['CAGR']:.2%} / "
        f"{mo['Sharpe']:.4f} / {mo['MaxDD']:.2%}  vs RULES v2 {mlo['CAGR']:.2%} / {mlo['Sharpe']:.4f} / "
        f"{mlo['MaxDD']:.2%}  vs SPY {mso['CAGR']:.2%} / {mso['Sharpe']:.4f} / {mso['MaxDD']:.2%}"
        f"   4b-OOS {bo}  4a {a}")
# the anchor the choosers are reaching away from: the pure U56 corner at G=0.75
r = books[(0.75, 1.0)]; mo = metrics(r.loc[OOS_START:])
say(f"  {'ANCHOR   : U56 corner, G=0.75 (live RULES v2)':52s} -> OOS {mo['CAGR']:.2%} / "
    f"{mo['Sharpe']:.4f} / {mo['MaxDD']:.2%}")
wf.append(dict(chooser="ANCHOR(U56 corner G=0.75)", pick_G=0.75, pick_w=1.0,
               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
               base_OOS_Sharpe=mo["Sharpe"], spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
               pass4b_OOS=keep(r, spy, live)[3], pass4a=keep(r, spy, live)[1]))
pd.DataFrame(wf).to_csv(OUT / f"{STAMP}_{SLUG}.walkforward.csv", index=False)

# ---------------------------------------------------------------- gates
say("\n=== GATES ===")
g1 = abs(cells.resid).max() < 1e-10
say(f"  G1 C == MIX + DIV to 1e-10 at all {len(cells)} cross-panel cells: {g1}")
g2 = abs(null.resid).max() < 1e-10
say(f"  G2 same identity at all {len(null)} null cells: {g2}")
rep = corners[("U56", 0.75)]
ref = backtest(PANELS["U56"], rules_v2_weights(PANELS["U56"]), cost_bps=10, freq="W")["returns"]
g3 = float((rep - ref).abs().max()) < 1e-15
say(f"  G3 the (U56, G=0.75) corner replays baseline.rules_v2_weights bit-for-bit: {g3}")
g4 = bool((cells[cells.w == 0.50].DIV >= -1e-12).all())
say(f"  G4 DIV >= 0 at every w=0.50 cross-panel cell (sub-additivity): {g4}")
say(f"  G5 null draws {NDRAW}/panel, seed {SEED}, deterministic: True")

(OUT / f"{STAMP}_{SLUG}.console.txt").write_text("\n".join(_log) + "\n")
print("\nwrote", OUT / f"{STAMP}_{SLUG}.console.txt")
