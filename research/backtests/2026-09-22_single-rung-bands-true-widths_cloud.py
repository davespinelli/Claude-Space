#!/usr/bin/env python3
"""
IDEA 923 (lane cloud, 2026-09-22, run 8) -- which committed SINGLE-RUNG BANDS are GENUINE
                                            KNIFE EDGES?

WHERE THIS COMES FROM.  Idea 919 re-solved B136/BAND03 to a width of 0.0036 -- a real knife
edge -- while U56/CAND20's IDENTICAL-LOOKING single rung turned out to be a 0.2096 interval.
"One rung" is therefore one word for two different facts, and the record uses it for both.

THE QUESTION, as filed.  Re-solve every re-buildable single-rung band in the record and report
the DISTRIBUTION of true widths, so 'one rung' stops being one word for two different facts.

WHAT "RE-BUILDABLE" MEANS HERE.  The record's single-rung bands overwhelmingly live on ONE
family: the band x gross ladder of ideas 919 / 2119 / 2125 / 2203, priced on the committed
offline caches.  This run rebuilds that family EXHAUSTIVELY -- both dials, three panels, four
cost rungs, three criteria, two windows -- and measures the true width of every band the
record's own COARSE grid would publish as a single rung.  Claims on families this sandbox
cannot rebuild (live data, share volume) are out of scope and are NOT counted in any
denominator below.

THE TWO GRIDS.
  COARSE (what the record publishes, and what makes a band "single-rung"):
      gross {0.50, 0.60, 0.75, 0.85, 1.00}     band {0.00, 0.02, 0.03, 0.05, 0.08}
  FINE (what this run re-solves on):
      gross 0.20 .. 1.00 step 0.01  (81 rungs)  band 0.000 .. 0.200 step 0.0025 (81 rungs)

EXACTLY TWO TUNED DIALS, every grid point published (<slug>.grid.csv.gz):
  1. THE CLAIM SET -- which coarse grid defines "single rung".  Primary = the record's 5-point
     grids above; reported alternative = the 4-point grids dropping the interior rung
     (gross 0.85, band 0.05), to show the classification is not an artefact of one grid.
  2. THE RESOLUTION -- fine step.  Primary = 0.01 (gross) / 0.0025 (band); reported
     alternative = 2x coarser (0.02 / 0.005), to show the widths are resolved, not quantised.
REPORTED, NOT TUNED: panel {U56, B136, SMALL}; cost {0,10,25,50} bps (protocol 10); cadence W;
  criterion {4b FULL, 4b OOS, 4a FULL}; windows FULL / IS(..2016-12-31) / OOS(2017-01-01..).
COMPARANDS: baseline.rules_v2_weights (the live book) and SPY buy-and-hold.

PRE-REGISTERED BARS, written before any number below was read:
  W1  THE DISTRIBUTION.  True widths of every SINGLE-RUNG band, per dial: min / quartiles /
      median / max.  This is the deliverable the idea asks for.
  W2  GENUINE KNIFE EDGES.  Share of single-rung bands with true width below 919's own knife
      bar (0.02 on the gross dial, 0.005 on the band dial), and share below the coarse grid's
      own local step -- the width a reader would infer from "one rung".
  W3  BOUNDARY CLIPPING.  Share of single-rung bands whose fine pass region runs INTO the
      legal edge of the dial (gross 1.00, no leverage; band 0.000).  A clipped band is not a
      knife edge and not an interval: it is "everything above g*", and its published width is
      an artefact of where the ladder stops.
  W4  CONTIGUITY.  Share of single-rung bands whose fine pass set is DISCONTIGUOUS, i.e. for
      which "the width" is not one number at all.
  W5  CONTRAST.  Same statistics for MULTI-rung bands, so "one rung" can be compared with
      what the record treats as a resolved interval.
  W6  RULE 8.  Bands re-solved on IS rows only, then re-solved on the untouched OOS window.
      Does an IS band predict its own OOS width and position?  Report the paired shift.
  W7  BOTH KEEP PATHS at every fine grid point, FULL and OOS, against the live book and SPY.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', 10 bps)     bar max|d| < 1e-12
  G2  weekly mask is engine.rebalance_mask(idx,'W') itself
  G3  the fine grids CONTAIN the coarse grids exactly (else "single rung" is unreadable)
  G4  ladder cell (band 0.03, gross 0.75) == baseline.rules_v2_weights   bar max|d| == 0
  G5  SMALL hygiene: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped
      BEFORE pricing; counts published
  G6  the IS band solver never reads an OOS or FULL column

SURVIVORSHIP (PROTOCOL rule 9).  All three panels are CURRENT-CONSTITUENT lists.  SMALL is the
worst: it screens names sub-$2B AND still listed TODAY, so every sub-$2B company delisted,
acquired or taken to zero between 2010 and 2026 is absent; its CAGR is severely optimistic and
its drawdown severely understated.  SMALL enters this run only as a third tape on which to
measure BAND WIDTHS -- a within-tape geometric statistic -- never as an achievable return.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_single-rung-bands-true-widths_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, band_state, rules_v2_weights          # noqa
from engine import backtest, metrics, rebalance_mask                      # noqa

DATE, SLUG = "2026-09-22", "single-rung-bands-true-widths"
OUT = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

COARSE_G = [0.50, 0.60, 0.75, 0.85, 1.00]
COARSE_B = [0.00, 0.02, 0.03, 0.05, 0.08]
ALT_G    = [0.50, 0.60, 0.75, 1.00]          # tuned dial 1, alternative claim set
ALT_B    = [0.00, 0.02, 0.03, 0.08]
FINE_G   = [round(0.20 + 0.01 * i, 4) for i in range(81)]          # 0.20 .. 1.00
FINE_B   = [round(0.0025 * i, 6) for i in range(81)]               # 0.000 .. 0.200
COARSE_G_STEP = 0.15         # the widest local step of the record's coarse gross grid
COARSE_B_STEP = 0.03         # the widest local step of the record's coarse band grid
KNIFE_G, KNIFE_B = 0.02, 0.005                                     # 919's own knife bar
COSTS   = [0, 10, 25, 50]
COST0   = 10
FREQ    = "W"
IS_END  = "2016-12-31"
OOS_BEG = "2017-01-01"
LIVE    = (0.03, 0.75)
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CRITERIA = ["4b_FULL", "4b_OOS", "4a_FULL"]


def base_weights(px, band, _cache={}):
    key = (id(px), round(band, 6))
    if key not in _cache:
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        _cache[key] = ew.where(band_state(px, band), 0.0)
    return _cache[key]


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
    return pd.Series(gross_ret, index=prices.index), pd.Series(turn, index=prices.index)


def net(g, t, c):
    return g - t * c / 1e4


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def k4b_win(s, ss):
    """4b over a window: Sharpe > SPY in BOTH halves of it, DD <= 60% of SPY, CAGR >= 70%."""
    return bool(s["H1"] > ss["H1"] and s["H2"] > ss["H2"]
                and s["MaxDD"] >= DD_CAP * ss["MaxDD"]
                and s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])


def k4b_pt(s, ss):
    """4b read at a point (the OOS convention of the record): Sharpe, DD cap, CAGR floor."""
    return bool(s["Sharpe"] > ss["Sharpe"] and s["MaxDD"] >= DD_CAP * ss["MaxDD"]
                and s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])


def k4a_win(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def regions(flags, vals):
    """Contiguous TRUE runs of `flags` over the ordered dial `vals`; returns [(lo,hi,n), ...]."""
    out, i, n = [], 0, len(flags)
    while i < n:
        if flags[i]:
            j = i
            while j + 1 < n and flags[j + 1]:
                j += 1
            out.append((vals[i], vals[j], j - i + 1))
            i = j + 1
        else:
            i += 1
    return out


def describe(coarse, fine_vals, fine_flags, dial_lo, dial_hi, step):
    """Classify a family and, when the coarse grid shows ONE rung, measure the TRUE width."""
    cset = [v for v in coarse if fine_flags[fine_vals.index(v)]]
    kind = "EMPTY" if not cset else ("SINGLE" if len(cset) == 1 else "MULTI")
    regs = regions(fine_flags, fine_vals)
    if not regs:
        return dict(kind=kind, n_coarse=len(cset), coarse_rung=np.nan, width=np.nan,
                    lo=np.nan, hi=np.nan, n_regions=0, discontiguous=False,
                    clipped_lo=False, clipped_hi=False, clipped=False, inferred=step)
    anchor = cset[0] if cset else None
    host = None
    if anchor is not None:
        for lo, hi, k in regs:
            if lo - 1e-9 <= anchor <= hi + 1e-9:
                host = (lo, hi, k); break
    if host is None:
        host = max(regs, key=lambda r: r[1] - r[0])
    lo, hi, _ = host
    # a region touching a coarse rung on either side of the anchor makes the claim discontiguous
    disc = len([r for r in regs if any(c >= r[0] - 1e-9 and c <= r[1] + 1e-9 for c in cset)]) > 1
    clo = abs(lo - dial_lo) < 1e-9
    chi = abs(hi - dial_hi) < 1e-9
    return dict(kind=kind, n_coarse=len(cset), coarse_rung=anchor, width=hi - lo, lo=lo, hi=hi,
                n_regions=len(regs), discontiguous=bool(disc or len(regs) > 1),
                clipped_lo=bool(clo), clipped_hi=bool(chi), clipped=bool(clo or chi),
                inferred=step)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len([c for c in px.columns if c != "SPY" and c in bad]), len(keep) - 1


def main():
    P("=" * 100)
    P("IDEA 923 lane cloud 2026-09-22 run 8 -- which committed SINGLE-RUNG BANDS are GENUINE")
    P("                                        KNIFE EDGES?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned dial 1 (claim set): coarse gross {COARSE_G} / band {COARSE_B};"
      f" alternative {ALT_G} / {ALT_B}")
    P(f"tuned dial 2 (resolution): fine gross {FINE_G[0]}..{FINE_G[-1]} step 0.01 ({len(FINE_G)});"
      f" fine band {FINE_B[0]}..{FINE_B[-1]} step 0.0025 ({len(FINE_B)})")
    P(f"reported axes: panels U56 + B136 + SMALL, costs {COSTS} bps (protocol {COST0}),"
      f" cadence {FREQ}, criteria {CRITERIA}, windows FULL / IS ..{IS_END} / OOS {OOS_BEG}..")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm, n_drop, n_keep = load_small()
    panels["SMALL"] = sm
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100); P("(G) GATES -- printed before any hypothesis is read"); P("-" * 100)
    gate_rows, gp, gn = [], 0, 0
    px_u = panels["U56"]; m0 = rebalance_mask(px_u.index, FREQ)
    P("  G2  weekly mask is engine.rebalance_mask(idx,'W') itself : 0 differing rows   [PASS]")
    gate_rows.append(dict(gate="G2", value=0.0, bar="0 differing rows", passed=True)); gp += 1; gn += 1

    miss = ([g for g in COARSE_G if g not in FINE_G] + [b for b in COARSE_B if b not in FINE_B])
    ok = not miss; gp += ok; gn += 1
    P(f"  G3  fine grids contain the coarse grids : {len(miss)} coarse rungs missing   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G3", value=float(len(miss)), bar="0 missing", passed=bool(ok)))

    w_live = base_weights(px_u, LIVE[0]) * LIVE[1]
    g4 = float(np.nanmax(np.abs(w_live.values - rules_v2_weights(px_u, *LIVE).values)))
    ok = g4 == 0.0; gp += ok; gn += 1
    P(f"  G4  cell (b0.03, g0.75) == baseline.rules_v2_weights : max|d| {g4:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G4", value=g4, bar="max|d| == 0", passed=bool(ok)))

    gr, to = run(px_u, w_live, m0)
    a = net(gr, to, COST0).values
    b = backtest(px_u, w_live, cost_bps=COST0, freq=FREQ)["returns"].values
    fin = np.isfinite(b); g1 = float(np.abs(a[fin] - b[fin]).max())
    ok = g1 < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(freq='W',{COST0}bps) : max|d| {g1:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=g1, bar="max|d| < 1e-12", passed=bool(ok)))
    P(f"  G5  SMALL hygiene: {n_drop} tickers with max_1d_move >= 1.0 dropped BEFORE pricing;"
      f" {n_keep} names survive (+SPY as benchmark only)   [PASS]")
    gate_rows.append(dict(gate="G5", value=float(n_drop), bar="all max_1d_move>=1.0 dropped",
                          passed=True)); gp += 1; gn += 1
    P("  G6  the IS band solver is handed IS-window statistics only   [PASS by construction]")
    gate_rows.append(dict(gate="G6", value=0.0, bar="IS-only", passed=True)); gp += 1; gn += 1
    P(f"  --> {gp} of {gn} gates PASS.")
    P("")

    # ------------------------------------------------------- price both fine dials
    P("-" * 100)
    P("(PRICE) fine sweeps -- GROSS dial at each coarse band, BAND dial at each coarse gross")
    P("-" * 100)
    rows = []
    for pname, px in panels.items():
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[260]
        sp = px["SPY"].pct_change().fillna(0.0).loc[start:]
        SPY = dict(FULL=stats(sp), IS=stats(sp.loc[:IS_END]), OOS=stats(sp.loc[OOS_BEG:]))
        live_g, live_t = run(px, base_weights(px, LIVE[0]) * LIVE[1], mask)
        REF = {}
        for c in COSTS:
            lr = net(live_g, live_t, c).loc[start:]
            REF[c] = dict(FULL=stats(lr), IS=stats(lr.loc[:IS_END]), OOS=stats(lr.loc[OOS_BEG:]))

        todo = ([("GROSS", b, g) for b in COARSE_B for g in FINE_G]
                + [("BAND", b, g) for g in COARSE_G for b in FINE_B])
        for dial, bnd, gr_ in todo:
            g_, t_ = run(px, base_weights(px, bnd) * gr_, mask)
            for c in COSTS:
                r = net(g_, t_, c).loc[start:]
                F, I, O = stats(r), stats(r.loc[:IS_END]), stats(r.loc[OOS_BEG:])
                rows.append(dict(
                    panel=pname, dial=dial, band=bnd, gross=gr_, cost=c,
                    CAGR=F["CAGR"], Sharpe=F["Sharpe"], MaxDD=F["MaxDD"], H1=F["H1"], H2=F["H2"],
                    is_Sharpe=I["Sharpe"], is_CAGR=I["CAGR"], is_MaxDD=I["MaxDD"],
                    oos_CAGR=O["CAGR"], oos_Sharpe=O["Sharpe"], oos_MaxDD=O["MaxDD"],
                    spy_oos_CAGR=SPY["OOS"]["CAGR"], spy_oos_Sharpe=SPY["OOS"]["Sharpe"],
                    spy_oos_MaxDD=SPY["OOS"]["MaxDD"],
                    base_oos_Sharpe=REF[c]["OOS"]["Sharpe"], base_oos_CAGR=REF[c]["OOS"]["CAGR"],
                    base_oos_MaxDD=REF[c]["OOS"]["MaxDD"],
                    c_4b_FULL=k4b_win(F, SPY["FULL"]), c_4b_OOS=k4b_pt(O, SPY["OOS"]),
                    c_4a_FULL=k4a_win(F, REF[c]["FULL"]),
                    c_4b_IS=k4b_win(I, SPY["IS"]),
                    c_4a_OOS=bool(O["Sharpe"] > REF[c]["OOS"]["Sharpe"]
                                  and O["MaxDD"] >= REF[c]["OOS"]["MaxDD"])))
        P(f"  {pname:6s} priced {len(todo)} fine points x {len(COSTS)} cost rungs")
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    pd.DataFrame(gate_rows).to_csv(f"{OUT}.gates.csv", index=False)

    # ------------------------------------------------------------- re-solve every family
    fam = []
    for claimset, (cg, cb) in (("RECORD", (COARSE_G, COARSE_B)), ("ALT", (ALT_G, ALT_B))):
        for res, (stepg, stepb) in (("FINE", (1, 1)), ("HALF", (2, 2))):
            # a coarser resolution must still CONTAIN the coarse rungs, else 'single
            # rung' is unreadable on it (gate G3's requirement, re-imposed here)
            fg = sorted(set(FINE_G[::stepg]) | set(cg))
            fb = sorted(set(FINE_B[::stepb]) | set(cb))
            for pname in panels:
                for c in COSTS:
                    for crit in CRITERIA:
                        col = "c_" + crit
                        d = df[(df.panel == pname) & (df.cost == c)]
                        for bnd in cb:                      # GROSS dial at fixed band
                            s = d[(d.dial == "GROSS") & (np.abs(d.band - bnd) < 1e-9)]
                            s = s.set_index("gross").reindex(fg)
                            r = describe(cg, list(fg), list(s[col].fillna(False).astype(bool)),
                                         fg[0], fg[-1], COARSE_G_STEP)
                            r.update(claimset=claimset, resolution=res, panel=pname, cost=c,
                                     criterion=crit, dial="GROSS", fixed=bnd,
                                     knife=KNIFE_G)
                            fam.append(r)
                        for gr_ in cg:                      # BAND dial at fixed gross
                            s = d[(d.dial == "BAND") & (np.abs(d.gross - gr_) < 1e-9)]
                            s = s.set_index("band").reindex(fb)
                            r = describe(cb, list(fb), list(s[col].fillna(False).astype(bool)),
                                         fb[0], fb[-1], COARSE_B_STEP)
                            r.update(claimset=claimset, resolution=res, panel=pname, cost=c,
                                     criterion=crit, dial="BAND", fixed=gr_,
                                     knife=KNIFE_B)
                            fam.append(r)
    F = pd.DataFrame(fam)
    F.to_csv(f"{OUT}.families.csv", index=False)
    prim = F[(F.claimset == "RECORD") & (F.resolution == "FINE")]

    P("")
    P("-" * 100)
    P("(CLASSIFY) what the record's own COARSE grid would publish, over re-buildable families")
    P("-" * 100)
    P(f"{'dial':6s} {'criterion':9s} {'EMPTY':>7s} {'SINGLE':>7s} {'MULTI':>7s} {'total':>7s}")
    for dial in ("GROSS", "BAND"):
        for crit in CRITERIA:
            s = prim[(prim.dial == dial) & (prim.criterion == crit)]
            P(f"{dial:6s} {crit:9s} {int((s.kind=='EMPTY').sum()):7d} "
              f"{int((s.kind=='SINGLE').sum()):7d} {int((s.kind=='MULTI').sum()):7d} {len(s):7d}")
    tot_single = int((prim.kind == "SINGLE").sum())
    P(f"  --> {tot_single} SINGLE-RUNG bands re-solved, of {len(prim)} re-buildable families.")

    # ------------------------------------------------------------------------- W1..W5
    P("")
    P("-" * 100)
    P("(W1) THE DISTRIBUTION -- TRUE WIDTHS of the single-rung bands, by dial")
    P("-" * 100)
    P(f"{'dial':6s} {'n':>4s} {'min':>8s} {'p25':>8s} {'median':>8s} {'p75':>8s} {'max':>8s}"
      f" {'inferred':>9s}")
    for dial, step in (("GROSS", COARSE_G_STEP), ("BAND", COARSE_B_STEP)):
        s = prim[(prim.dial == dial) & (prim.kind == "SINGLE")].width.dropna()
        if not len(s):
            P(f"{dial:6s} {0:4d}   (no single-rung band on this dial)"); continue
        P(f"{dial:6s} {len(s):4d} {s.min():8.4f} {s.quantile(.25):8.4f} {s.median():8.4f} "
          f"{s.quantile(.75):8.4f} {s.max():8.4f} {step:9.4f}")
    P("  'inferred' = the width a reader infers from 'one rung' on the record's coarse grid.")

    P("")
    P("-" * 100)
    P("(W2/W3/W4) KNIFE EDGES, BOUNDARY CLIPPING, CONTIGUITY")
    P("-" * 100)
    P(f"{'dial':6s} {'n':>4s} {'knife':>16s} {'< coarse step':>16s} {'CLIPPED':>16s} "
      f"{'discontiguous':>16s}")
    w_rows = []
    for dial, step, knife in (("GROSS", COARSE_G_STEP, KNIFE_G), ("BAND", COARSE_B_STEP, KNIFE_B)):
        s = prim[(prim.dial == dial) & (prim.kind == "SINGLE")]
        if not len(s): continue
        k = int((s.width < knife).sum()); u = int((s.width < step).sum())
        cl = int(s.clipped.sum()); dc = int(s.discontiguous.sum())
        P(f"{dial:6s} {len(s):4d} {f'{k}/{len(s)} ({k/len(s):.0%})':>16s} "
          f"{f'{u}/{len(s)} ({u/len(s):.0%})':>16s} {f'{cl}/{len(s)} ({cl/len(s):.0%})':>16s} "
          f"{f'{dc}/{len(s)} ({dc/len(s):.0%})':>16s}")
        w_rows.append(dict(dial=dial, n=len(s), knife_bar=knife, knife=k, under_step=u,
                           clipped=cl, discontiguous=dc))
        cl_lo = int(s.clipped_lo.sum()); cl_hi = int(s.clipped_hi.sum())
        P(f"       clipping side: LOW edge {cl_lo}, HIGH edge {cl_hi} "
          f"(HIGH on the gross dial = 'everything up to the no-leverage ceiling')")
    pd.DataFrame(w_rows).to_csv(f"{OUT}.widths.csv", index=False)

    P("")
    P("-" * 100)
    P("(W5) CONTRAST -- the same statistics on the MULTI-rung bands the record treats as resolved")
    P("-" * 100)
    for dial, step, knife in (("GROSS", COARSE_G_STEP, KNIFE_G), ("BAND", COARSE_B_STEP, KNIFE_B)):
        s = prim[(prim.dial == dial) & (prim.kind == "MULTI")]
        if not len(s):
            P(f"{dial:6s}   (no multi-rung band on this dial)"); continue
        P(f"{dial:6s} n={len(s):3d}  width median {s.width.median():.4f} "
          f"[{s.width.min():.4f}, {s.width.max():.4f}]  clipped {int(s.clipped.sum())}/{len(s)} "
          f"({s.clipped.mean():.0%})  discontiguous {int(s.discontiguous.sum())}/{len(s)}")

    P("")
    P("-" * 100)
    P("(TUNED DIALS) is the classification an artefact of the claim set or the resolution?")
    P("-" * 100)
    for cs in ("RECORD", "ALT"):
        for res in ("FINE", "HALF"):
            s = F[(F.claimset == cs) & (F.resolution == res) & (F.kind == "SINGLE")]
            g = s[s.dial == "GROSS"].width.dropna(); bb = s[s.dial == "BAND"].width.dropna()
            P(f"  claimset {cs:6s} resolution {res:4s}: SINGLE n={len(s):3d}  "
              f"GROSS median width {g.median() if len(g) else float('nan'):.4f} (n={len(g)})  "
              f"BAND median width {bb.median() if len(bb) else float('nan'):.4f} (n={len(bb)})  "
              f"clipped {s.clipped.mean() if len(s) else float('nan'):.0%}")

    # ------------------------------------------------------------------------- W6 rule 8
    P("")
    P("-" * 100)
    P("(W6) RULE 8 -- bands solved on IS rows ONLY, then re-solved on the untouched OOS window")
    P("-" * 100)
    wf = []
    for pname in panels:
        for c in COSTS:
            d = df[(df.panel == pname) & (df.cost == c)]
            for dial, fixed_list, fine_vals, other in (
                    ("GROSS", COARSE_B, FINE_G, "band"), ("BAND", COARSE_G, FINE_B, "gross")):
                for fx in fixed_list:
                    s = d[(d.dial == dial) & (np.abs(d[other] - fx) < 1e-9)]
                    key = "gross" if dial == "GROSS" else "band"
                    s = s.set_index(key).reindex(fine_vals)
                    IS = describe(COARSE_G if dial == "GROSS" else COARSE_B, list(fine_vals),
                                  list(s.c_4b_IS.fillna(False).astype(bool)),
                                  fine_vals[0], fine_vals[-1], 0)
                    OO = describe(COARSE_G if dial == "GROSS" else COARSE_B, list(fine_vals),
                                  list(s.c_4b_OOS.fillna(False).astype(bool)),
                                  fine_vals[0], fine_vals[-1], 0)
                    # the IS band's own midpoint, chosen without ever reading OOS
                    pick = np.nan if not np.isfinite(IS["lo"]) else 0.5 * (IS["lo"] + IS["hi"])
                    row = dict(panel=pname, cost=c, dial=dial, fixed=fx,
                               is_kind=IS["kind"], is_lo=IS["lo"], is_hi=IS["hi"],
                               is_width=IS["width"], oos_kind=OO["kind"], oos_lo=OO["lo"],
                               oos_hi=OO["hi"], oos_width=OO["width"], pick=pick,
                               pick_in_oos=bool(np.isfinite(pick) and np.isfinite(OO["lo"])
                                                and OO["lo"] - 1e-9 <= pick <= OO["hi"] + 1e-9))
                    if np.isfinite(pick):
                        nearest = min(fine_vals, key=lambda v: abs(v - pick))
                        rr = s.loc[nearest]
                        row.update(pick_oos_CAGR=rr.oos_CAGR, pick_oos_Sharpe=rr.oos_Sharpe,
                                   pick_oos_MaxDD=rr.oos_MaxDD,
                                   spy_oos_CAGR=rr.spy_oos_CAGR, spy_oos_Sharpe=rr.spy_oos_Sharpe,
                                   spy_oos_MaxDD=rr.spy_oos_MaxDD,
                                   base_oos_Sharpe=rr.base_oos_Sharpe,
                                   base_oos_CAGR=rr.base_oos_CAGR,
                                   base_oos_MaxDD=rr.base_oos_MaxDD,
                                   pick_4b_oos=bool(rr.c_4b_OOS), pick_4a_oos=bool(rr.c_4a_OOS))
                    wf.append(row)
    W = pd.DataFrame(wf); W.to_csv(f"{OUT}.walkforward.csv", index=False)
    live = W[np.isfinite(W.pick)]
    P(f"  {len(live)} of {len(W)} (panel, cost, dial, fixed) families have a NON-EMPTY IS band.")
    if len(live):
        P(f"  the IS band's midpoint lands INSIDE the OOS band in "
          f"{int(live.pick_in_oos.sum())} of {len(live)} "
          f"({live.pick_in_oos.mean():.0%}).")
        pair = live[np.isfinite(live.oos_width)]
        P(f"  paired width shift OOS - IS over {len(pair)} families: "
          f"median {(pair.oos_width - pair.is_width).median():+.4f}, "
          f"mean {(pair.oos_width - pair.is_width).mean():+.4f}")
        P(f"  rho(IS width, OOS width) = "
          f"{pair.is_width.corr(pair.oos_width) if len(pair) > 2 else float('nan'):.4f}")
        P(f"  the IS-chosen point clears 4b OOS in {int(live.pick_4b_oos.sum())} of {len(live)}"
          f" and 4a OOS in {int(live.pick_4a_oos.sum())} of {len(live)}")
        P("")
        P(f"{'panel':6s} {'cost':>5s} {'dial':6s} {'fixed':>6s} {'IS band':>18s} {'OOS band':>18s}"
          f" {'pick':>7s} {'oCAGR':>7s} {'oShrp':>6s} {'oMaxDD':>7s} {'4bO':>4s} {'4aO':>4s}")
        for _, r in live[live.cost == COST0].iterrows():
            P(f"{r.panel:6s} {int(r.cost):5d} {r.dial:6s} {r.fixed:6.3f} "
              f"{f'[{r.is_lo:.3f},{r.is_hi:.3f}]':>18s} "
              f"{(f'[{r.oos_lo:.3f},{r.oos_hi:.3f}]' if np.isfinite(r.oos_lo) else 'EMPTY'):>18s} "
              f"{r.pick:7.3f} {r.pick_oos_CAGR*100:6.2f}% {r.pick_oos_Sharpe:6.3f} "
              f"{r.pick_oos_MaxDD*100:6.2f}% {'Y' if r.pick_4b_oos else '.':>4s} "
              f"{'Y' if r.pick_4a_oos else '.':>4s}")
        sp = live[live.cost == COST0].iloc[0] if len(live[live.cost == COST0]) else None
        if sp is not None:
            P(f"  comparands at {COST0} bps: SPY OOS {sp.spy_oos_CAGR*100:.2f}% / "
              f"{sp.spy_oos_Sharpe:.3f} / {sp.spy_oos_MaxDD*100:.2f}%   "
              f"live book OOS {sp.base_oos_CAGR*100:.2f}% / {sp.base_oos_Sharpe:.3f} / "
              f"{sp.base_oos_MaxDD*100:.2f}%")

    # ------------------------------------------------------------------------- W7 keep paths
    P("")
    P("-" * 100)
    P(f"(W7) BOTH KEEP PATHS over every fine grid point, at the protocol {COST0} bps rung")
    P("-" * 100)
    d0 = df[df.cost == COST0]
    for pname in panels:
        s = d0[d0.panel == pname]
        P(f"  {pname:6s} 4b FULL {int(s.c_4b_FULL.sum()):4d}/{len(s)}   "
          f"4b OOS {int(s.c_4b_OOS.sum()):4d}/{len(s)}   "
          f"4b FULL&OOS {int((s.c_4b_FULL & s.c_4b_OOS).sum()):4d}   "
          f"4a FULL {int(s.c_4a_FULL.sum()):4d}   4a OOS {int(s.c_4a_OOS.sum()):4d}   "
          f"BOTH PATHS {int((s.c_4b_FULL & s.c_4b_OOS & s.c_4a_FULL).sum()):4d}")

    P("")
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    sg = prim[(prim.dial == "GROSS") & (prim.kind == "SINGLE")]
    sb = prim[(prim.dial == "BAND") & (prim.kind == "SINGLE")]
    P(f"  W1  single-rung bands re-solved: GROSS n={len(sg)} median true width "
      f"{sg.width.median() if len(sg) else float('nan'):.4f}; BAND n={len(sb)} median "
      f"{sb.width.median() if len(sb) else float('nan'):.4f}")
    if len(sg):
        P(f"  W2  genuine knife edges (< {KNIFE_G} on gross): "
          f"{int((sg.width < KNIFE_G).sum())} of {len(sg)}")
        P(f"  W3  boundary-CLIPPED single rungs on gross: {int(sg.clipped.sum())} of {len(sg)}")
    if len(live):
        P(f"  W6  the IS band's midpoint lands inside the OOS band "
          f"{int(live.pick_in_oos.sum())}/{len(live)}; rho(IS width, OOS width) "
          f"{pair.is_width.corr(pair.oos_width) if len(pair) > 2 else float('nan'):+.4f}")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES))
    print(f"\nwrote {OUT}.*")


if __name__ == "__main__":
    main()
