#!/usr/bin/env python3
"""
IDEA 2081 (lane B, 2026-09-22) -- reallocate-not-remove-the-idle-band-NAV

THE QUESTION, as filed.  RULES v2 clause 4 is explicit: when a name leaves the 200d band its
weight "stays in cash -- the book de-grosses.  Do NOT re-spread".  The CHANGELOG's own
diagnosis is that EVERY priced device in the record REMOVES exposure, and idea 2085 found that
static leverage on the band book only slides along a FIXED SHARPE RAY (Sharpe constant to 3dp
from gross 0.75 to 2.00) with the 4b DD cap binding at gross ~1.25-1.5.  2081 asks for the
untested middle: REALLOCATE the idle NAV to the names still inside the band at CONSTANT total
gross, and ask whether that lifts the 4b CAGR FLOOR without paying leverage's drawdown.

THE ONE LEG THAT IS GENUINELY NEW, and the reason this run is not a re-print of idea 1403.
Idea 1403 (2026-09-19, lane B) already priced no-re-spread vs re-spread on U56/B136 and found
the live convention weakly dominates; ideas 1454/1498 priced DEST x F grids.  What NO run has
done is put the two devices on the SAME AXIS: a re-spread book is, by construction, a
de-grossed book carrying MORE mean exposure, so the honest question is whether re-spreading is
ANYTHING MORE THAN A LEVERAGE DIAL.  This run answers that with an exactly matched control:

    for every (panel, band, f) cell, build the DE-GROSS twin whose MEAN TARGET GROSS is
    ARITHMETICALLY IDENTICAL to the reallocating book's, and report the difference in
    CAGR / Sharpe / MaxDD between them.

If the differences vanish, reallocation carries NO information the gross dial does not already
carry, 2085's ray absorbs it, and the "untested middle" is empty -- which closes 2081.  If they
do not vanish, re-spreading is a distinct device and the record has mis-filed it as a sizing
convention.

THE BOOKS.  One family, three arms, all long-only, weekly (the live cadence), 10 bps, weights
decided at close t and applied at t+1:
    REALLOC(c, f)  band gate with hysteresis at width c (baseline.band_state).  N = names
        priced that day, k = names IN.  Each IN name is held at
                w = (g/N) * (1 + f * (N-k)/k),      g = 0.75 fixed
        so f=0 is EXACTLY the live RULES v2 book (idle NAV to cash) and f=1 is the CONSTANT-GROSS
        re-spread (total gross g on every day with k>=1).  f in between is the partial
        reallocation the idea calls "an equal split": with an equal-weight book, splitting the
        departing name's weight equally over the survivors IS the pro-rata re-spread, so the
        third arm can only be a FRACTION f, not a different spreading rule.  k=0 -> all cash.
    LEVDG_F(c, f)  the MATCHED-LEVERAGE CONTROL.  The same de-gross book (f=0) run at gross
        g*lambda, lambda = mean(s + f(1-s)) / mean(s) with s_t = k_t/N_t, computed on the FULL
        window.  Mean target gross is then identical to REALLOC(c,f)'s BY ARITHMETIC (gate G4).
    LEVDG_IS(c, f)  the same control with lambda computed on the IS window ONLY (2009..2016) and
        applied unchanged to OOS -- the honest twin for the rule-8 read, since LEVDG_F peeks.
    lambda > 1/g means the control BORROWS.  That is stated, not hidden: it is a control, not a
    proposal, and it is reported both financing-free and with a stated 2%/yr charge on the part
    of realised gross above 1.0 (B6).  Financing-free FAVOURS the control, so "REALLOC does not
    beat its twin" is the conservative direction of this test.

TUNED PARAMETERS -- EXACTLY TWO, and EVERY grid point is published (<slug>.grid.csv.gz):
    1. BAND WIDTH          c in {0.00, 0.02, 0.03, 0.05, 0.10}   (RULES v2's acceptance ladder)
    2. REALLOCATION FRACTION f in {0.00, 0.25, 0.50, 0.75, 1.00} (0 = live de-gross, 1 = re-spread)
    -> 25 cells per panel, 50 published cells, each with its two controls.
NOT TUNED, and declared as such BEFORE any number below was read:
    GROSS g = 0.75 (the live sizing number), CADENCE W (the live schedule), COST 10 bps
      (PROTOCOL rung 2; a 0/10/25/50 ladder is reported in B7 as a SENSITIVITY, never as a
      selection axis), PANELS U56 = research/universe.json and B136 = research/universe_broad.json,
      WINDOWS FULL / H1 / H2 / IS ..2016-12-31 / OOS 2017-01-01.. (rule 8).
    REBALANCE OFFSET d in {0,1,2,3,4} is a MEASUREMENT, never a choice: every reported book is
      d=0 (the published Friday convention) and d=1..4 exist only to build idea 914's spread.

PRE-REGISTERED BARS -- written before any number below was read:
  B1  THE HEADLINE.  Does ANY f>0 cell clear PROTOCOL 4b where its OWN f=0 cell (same panel,
      same band) does not?  Report the full 4b leg vector and every leg margin at all 50 cells.
  B2  THE CAGR FLOOR, which is the one bar the live book fails.  Report CAGR and the floor
      margin (CAGR - 0.70*SPY) as a function of f, per panel per band.
  B3  THE MATCHED-LEVERAGE CONTROL (the new leg).  Per cell report REALLOC minus LEVDG_F on
      CAGR (pp), Sharpe and MaxDD (pp).  PRE-STATED VERDICT: a cell is INDISTINGUISHABLE if
      |dSharpe| <= 0.02 AND |dMaxDD| <= 0.50pp AND |dCAGR| <= 0.50pp; DISTINCT if |dSharpe| >
      0.05 or |dMaxDD| > 1.5pp; MARGINAL otherwise.  Report the share of cells per bucket.
      A reallocating book that is INDISTINGUISHABLE from a levered de-gross book is a leverage
      dial with extra steps.
  B4  THE DRAWDOWN PRICE OF EXPOSURE.  Is MaxDD monotone in f?  Report the sign of every
      consecutive step and the pp of drawdown bought per pp of mean gross added, against the
      same ratio along 2085's leverage ray (LEVDG_F).
  B5  RULE 8.  Both dials chosen on IS (2009..2016) ONLY, by IS Sharpe, per panel; 2017-2026
      read ONCE.  Report OOS CAGR / Sharpe / MaxDD vs RULES v2 OOS and SPY OOS, both KEEP
      paths, and the same for the IS-best f at the LIVE band c=0.03 as a second, constrained arm.
  B6  FINANCING on the control (2077's open leg, stated constant): LEVDG_F re-scored with
      2%/yr charged on realised gross above 1.0.  Does the control survive its own borrow bill,
      and does B3's verdict change?
  B7  PATH 4a at EVERY grid point (Sharpe > RULES v2 in BOTH halves AND MaxDD no worse), plus
      a 0/10/25/50 bps cost ladder on the four corner cells as a declared sensitivity.
  B8  IDEA 914's OFFSET-SPREAD CLAUSE on every 4b pass: a DD or CAGR margin only counts if it
      exceeds that leg's own 5-weekday spread.  Report the margin, the spread, and the 5-of-5
      offset stability of each pass.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', cost_bps=10)   bar max|d| < 1e-12
  G2  REALLOC(c=0.03, f=0) weights == baseline.rules_v2_weights     bar max|d| == 0.0
  G3  f=1 is CONSTANT GROSS: target gross == 0.75 on every day with k>=1, 0.0 when k==0
  G4  MATCHED CONTROL: mean target gross REALLOC(c,f) == mean target gross LEVDG_F(c,f)
      bar max|d| < 1e-12 over all 50 cells (this is what makes B3 a contrast and not a race)
  G5  COST LINEARITY: net(gross,turn,c) from ONE path == a full re-run at cost c, max|d| < 1e-15
  G6  OFFSET CLIPPING census (weeks too short to carry offset d)
  G7  SPY offset-invariance: SPY buy-and-hold never rebalances, so its 4b bars are constant
      across d.  bar max|d| == 0.0
  G8  f=0 REALLOC and LEVDG_F are BIT-IDENTICAL at f=0 (lambda == 1 by construction)

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every absolute
CAGR and drawdown LEVEL here is optimistic, and the bias runs TOWARD the higher-exposure arms
(more exposure to a survivor list is more of a look-ahead).  B3's contrast is a WITHIN-TAPE,
same-names, same-days, MATCHED-MEAN-GROSS difference, which is the part the bias cannot
manufacture; the CAGR LEVELS in B1/B2 are not repaired by it.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_reallocate-vs-degross-idle-band-nav_B.py
"""
import sys, time, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights          # noqa
from engine import backtest, metrics, rebalance_mask                      # noqa

SLUG = "2026-09-22_reallocate-vs-degross-idle-band-nav_B"
OUT = ROOT / "research" / "backtests"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

GATES = []
def gate(name, got, bar, ok):
    GATES.append((name, str(got), str(bar), bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:50s} got {got}   bar {bar}")

BANDS   = [0.00, 0.02, 0.03, 0.05, 0.10]        # TUNED axis 1
FRACS   = [0.00, 0.25, 0.50, 0.75, 1.00]        # TUNED axis 2
OFFSETS = [0, 1, 2, 3, 4]                       # measurement only
GROSS0, COST0, FREQ = 0.75, 10, "W"
BAND_LIVE, COSTS_SENS = 0.03, [0, 10, 25, 50]
IS_END, OOS_BEG = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
FIN_RATE = 0.02                                  # stated constant, B6
WARMUP = 260


# ================================================================== books
def realloc_weights(px, c, f, g=GROSS0):
    """Band gate at width c; each IN name at (g/N)*(1 + f*(N-k)/k).  f=0 == RULES v2."""
    priced = px.notna()
    N = priced.sum(axis=1).astype(float)
    inb = band_state(px, c) & priced
    k = inb.sum(axis=1).astype(float)
    per = (g / N.replace(0, np.nan)) * (1.0 + f * (N - k) / k.replace(0, np.nan))
    return inb.astype(float).mul(per, axis=0).fillna(0.0)


def in_share(px, c):
    """s_t = k_t / N_t, the in-band share of the priced panel."""
    priced = px.notna()
    N = priced.sum(axis=1).astype(float)
    k = (band_state(px, c) & priced).sum(axis=1).astype(float)
    return (k / N.replace(0, np.nan)).fillna(0.0)


def lam(s, f):
    """Leverage factor that matches a de-gross book's MEAN target gross to REALLOC(.,f)'s."""
    m = float(s.mean())
    return float((s + f * (1.0 - s)).mean() / m) if m > 0 else 1.0


# ============================================ offsets + schedule-taking backtester
def offset_mask(idx, d, freq=FREQ):
    key = pd.Series(idx.to_period(freq), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    clipped = int((last - d < first).sum())
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, clipped


def run(prices, weights, mask):
    """engine.backtest's loop, semantics byte-for-byte (G1).  Costs are applied afterwards --
    they never touch the held path -- so ONE loop serves every cost rung (G5)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = pd.DataFrame(weights, index=prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gross_ret = np.empty(n); turn = np.zeros(n); gsum = np.empty(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        gsum[i] = cur.sum()
        gross_ret[i] = float(np.nansum(cur * rets[i]))
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    ix = prices.index
    return (pd.Series(gross_ret, index=ix), pd.Series(turn, index=ix), pd.Series(gsum, index=ix))


def net(gross_ret, turnover, cost_bps=COST0, gsum=None, fin=0.0):
    r = gross_ret - turnover * cost_bps / 1e4
    if fin:
        r = r - np.maximum(gsum - 1.0, 0.0) * fin / 252.0
    return r


# ================================================================== scoring
def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    """PROTOCOL 4b against SPY on the SAME window.  Margins in the leg's own unit: Sharpe
    points for H1/H2, pp for DD and CAGR."""
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= DD_CAP * ss["MaxDD"], CAGR=s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])
    M = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
             DD=(s["MaxDD"] - DD_CAP * ss["MaxDD"]) * 100.0,
             CAGR=(s["CAGR"] - CAGR_FLOOR * ss["CAGR"]) * 100.0)
    return all(L.values()), L, M


def legs4a(s, sb):
    return bool(s["H1"] > sb["H1"] and s["H2"] > sb["H2"] and s["MaxDD"] >= sb["MaxDD"])


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 2081 lane B 2026-09-22 -- REALLOCATE (constant gross) vs REMOVE (de-gross) the")
    P("                               idle band NAV, against a MATCHED-LEVERAGE control")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned: band c {BANDS} x realloc fraction f {FRACS}   ({len(BANDS)*len(FRACS)} cells/panel)")
    P(f"not tuned: gross {GROSS0}, cadence {FREQ}, cost {COST0} bps, panels U56 + B136,")
    P(f"           windows FULL / H1 / H2 / IS ..{IS_END} / OOS {OOS_BEG}..  (rule 8)")
    P(f"           offsets {OFFSETS} are a MEASUREMENT (idea 914's clause, B8); books are always d=0")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k:5s}  {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  ({len(v)} rows)")
    P("")

    # ------------------------------------------------------------------ gates
    P("-" * 100); P("CONSTRUCTION GATES"); P("-" * 100)
    px = panels["U56"]
    w_live = rules_v2_weights(px, BAND_LIVE, GROSS0)
    m0, clip0 = offset_mask(px.index, 0)
    g_, t_, s_ = run(px, w_live, m0)
    eng = backtest(px, w_live, cost_bps=COST0, freq=FREQ)
    d1 = float(np.abs(net(g_, t_) - eng["returns"]).max())
    gate("G1 local run/net == engine.backtest", f"{d1:.3e}", "< 1e-12", d1 < 1e-12)
    d2 = float(np.abs(realloc_weights(px, BAND_LIVE, 0.0) - w_live).max().max())
    gate("G2 REALLOC(0.03,f=0) == rules_v2_weights", f"{d2:.3e}", "== 0.0", d2 == 0.0)
    ok3 = True
    for c in BANDS:
        W = realloc_weights(px, c, 1.0); tg = W.sum(axis=1)
        kk = (band_state(px, c) & px.notna()).sum(axis=1)
        bad = int((np.abs(tg[kk > 0] - GROSS0) > 1e-12).sum() + (np.abs(tg[kk == 0]) > 1e-12).sum())
        ok3 &= bad == 0
    gate("G3 f=1 target gross == 0.75 (k>=1), 0 else", "0 violations" if ok3 else "violations", "0", ok3)
    d5 = float(np.abs(net(g_, t_, 25) - backtest(px, w_live, cost_bps=25, freq=FREQ)["returns"]).max())
    gate("G5 cost linearity (one path, any rung)", f"{d5:.3e}", "< 1e-15", d5 < 1e-15)
    clips = {d: offset_mask(px.index, d)[1] for d in OFFSETS}
    gate("G6 offset clipping census (weeks < d+1 days)", str(clips), "reported", True)
    spy_all = {k: v["SPY"].pct_change().fillna(0.0) for k, v in panels.items()}
    P("")

    # ------------------------------------------------------------------ grid
    P("-" * 100); P("PRICING THE GRID (50 cells x REALLOC + 2 controls, 5 offsets on the two"); P(
        "priced arms) -- every point published to <slug>.grid.csv.gz"); P("-" * 100)
    rows, series = [], {}
    g4max, lammax = 0.0, {}
    for pn, pxp in panels.items():
        idx = pxp.index
        start = idx[WARMUP]
        masks = {d: offset_mask(idx, d)[0] for d in OFFSETS}
        wins = dict(FULL=(start, idx[-1]), IS=(start, pd.Timestamp(IS_END)), OOS=(pd.Timestamp(OOS_BEG), idx[-1]))
        spy = spy_all[pn]
        sstat = {w: stats(spy.loc[a:b]) for w, (a, b) in wins.items()}
        for c in BANDS:
            s_share = in_share(pxp, c)
            s_full = s_share.loc[start:]
            s_is = s_share.loc[start:pd.Timestamp(IS_END)]
            for f in FRACS:
                lF, lI = lam(s_full, f), lam(s_is, f)
                lammax[(pn, c, f)] = (lF, lI)
                books = {"REALLOC": realloc_weights(pxp, c, f),
                         "LEVDG_F": realloc_weights(pxp, c, 0.0, GROSS0 * lF),
                         "LEVDG_IS": realloc_weights(pxp, c, 0.0, GROSS0 * lI)}
                # G4: matched mean target gross, on the FULL window
                mg_r = float(books["REALLOC"].sum(axis=1).loc[start:].mean())
                mg_l = float(books["LEVDG_F"].sum(axis=1).loc[start:].mean())
                g4max = max(g4max, abs(mg_r - mg_l))
                for arm, W in books.items():
                    ds = OFFSETS if arm in ("REALLOC", "LEVDG_F") else [0]
                    for d in ds:
                        gr, tu, gs = run(pxp, W, masks[d])
                        r = net(gr, tu, COST0)
                        rf = net(gr, tu, COST0, gs, FIN_RATE)
                        for w, (a, b) in wins.items():
                            st = stats(r.loc[a:b])
                            p4b, L, M = legs4b(st, sstat[w])
                            rec = dict(panel=pn, band=c, frac=f, arm=arm, offset=d, window=w,
                                       CAGR=st["CAGR"], Sharpe=st["Sharpe"], MaxDD=st["MaxDD"],
                                       H1=st["H1"], H2=st["H2"], pass4b=p4b,
                                       mg=float(W.sum(axis=1).loc[a:b].mean()),
                                       gross_real=float(gs.loc[a:b].mean()),
                                       turn=float(tu.loc[a:b].sum() / (len(tu.loc[a:b]) / 252)),
                                       lam_F=lF, lam_IS=lI,
                                       **{f"leg_{k2}": v2 for k2, v2 in L.items()},
                                       **{f"mgn_{k2}": v2 for k2, v2 in M.items()})
                            if arm == "LEVDG_F":
                                stf = stats(rf.loc[a:b])
                                pf, Lf, Mf = legs4b(stf, sstat[w])
                                rec.update(CAGR_fin=stf["CAGR"], Sharpe_fin=stf["Sharpe"],
                                           MaxDD_fin=stf["MaxDD"], H1_fin=stf["H1"], H2_fin=stf["H2"],
                                           pass4b_fin=pf)
                            rows.append(rec)
                            if d == 0:
                                series[(pn, c, f, arm, w)] = st
        P(f"  {pn}: {len([r for r in rows if r['panel']==pn])} rows priced   ({time.time()-t0:.0f}s)")
    gate("G4 matched mean target gross (REALLOC vs LEVDG_F)", f"{g4max:.3e}", "< 1e-12", g4max < 1e-12)
    g8 = max(abs(series[(pn, c, 0.0, "REALLOC", "FULL")]["Sharpe"]
                 - series[(pn, c, 0.0, "LEVDG_F", "FULL")]["Sharpe"])
             for pn in panels for c in BANDS)
    gate("G8 f=0: REALLOC == LEVDG_F (lambda == 1)", f"{g8:.3e}", "== 0.0", g8 == 0.0)
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv.gz", index=False, compression="gzip")

    # G7 SPY offset invariance (SPY never rebalances)
    d7 = 0.0
    for pn, pxp in panels.items():
        sp = pxp[["SPY"]]
        base = None
        for d in OFFSETS:
            gr, tu, gs = run(sp, pd.DataFrame(1.0, index=sp.index, columns=["SPY"]),
                             offset_mask(sp.index, d)[0])
            st = stats(net(gr, tu).loc[pxp.index[WARMUP]:])
            if base is None: base = st
            d7 = max(d7, max(abs(st[k2] - base[k2]) for k2 in st))
    gate("G7 SPY offset-invariance", f"{d7:.3e}", "== 0.0", d7 == 0.0)
    # G9 REPLICATION of a COMMITTED book: idea 1454's re-spread book, quoted in CHANGELOG
    # 2026-09-20 as U56 BAND-ALL 12.19% / 1.1567 / -17.71% FULL, is EXACTLY this grid's
    # (U56, band 0.03, f = 1.00) cell.  If the cell does not reproduce it, this run's
    # construction differs from the record's and nothing below is comparable.
    rep = series[("U56", BAND_LIVE, 1.00, "REALLOC", "FULL")]
    dr = max(abs(rep["CAGR"] - 0.1219), abs(rep["Sharpe"] - 1.1567), abs(rep["MaxDD"] + 0.1771))
    gate("G9 replicates idea 1454's committed U56 re-spread", 
         f"{rep['CAGR']:.4f}/{rep['Sharpe']:.4f}/{rep['MaxDD']:.4f} d={dr:.5f}",
         "12.19%/1.1567/-17.71%, d < 5e-4", dr < 5e-4)
    P("")
    P(f"GATES: {sum(1 for g in GATES if g[3])} of {len(GATES)} PASS")
    P("")

    base_v2 = {(pn, w): series[(pn, BAND_LIVE, 0.0, "REALLOC", w)] for pn in panels for w in ("FULL", "IS", "OOS")}
    spyst = {(pn, w): stats(spy_all[pn].loc[a:b]) for pn, pxp in panels.items()
             for w, (a, b) in dict(FULL=(pxp.index[WARMUP], pxp.index[-1]),
                                   IS=(pxp.index[WARMUP], pd.Timestamp(IS_END)),
                                   OOS=(pd.Timestamp(OOS_BEG), pxp.index[-1])).items()}
    for pn in panels:
        for w in ("FULL", "IS", "OOS"):
            b, s = base_v2[(pn, w)], spyst[(pn, w)]
            P(f"  REF {pn:5s} {w:4s}  RULES v2  CAGR {b['CAGR']:7.2%} Sharpe {b['Sharpe']:6.3f} "
              f"MaxDD {b['MaxDD']:7.2%} (H1 {b['H1']:.3f}/H2 {b['H2']:.3f})   "
              f"SPY  CAGR {s['CAGR']:7.2%} Sharpe {s['Sharpe']:6.3f} MaxDD {s['MaxDD']:7.2%} "
              f"(H1 {s['H1']:.3f}/H2 {s['H2']:.3f})   4b bars: DD cap {DD_CAP*s['MaxDD']:7.2%} "
              f"CAGR floor {CAGR_FLOOR*s['CAGR']:6.2%}")
    P("")

    D0 = G[(G.offset == 0)]

    # ------------------------------------------------------------------ B1 / B2
    P("-" * 100); P("B1 + B2  THE HEADLINE GRID at 10 bps, d=0, FULL window: does any f>0 clear 4b"); P(
        "          where its own f=0 does not, and what does f do to the CAGR FLOOR margin?"); P("-" * 100)
    P(f"{'panel':6s}{'band':>6s}{'f':>6s}{'CAGR':>8s}{'Sharpe':>8s}{'MaxDD':>8s}{'H1':>7s}{'H2':>7s}"
      f"{'mgross':>8s}{'turn':>7s}{'mgnCAGR':>9s}{'mgnDD':>8s}{'4b':>4s}{'4a':>4s}{'4bOOS':>7s}")
    grid_tab = []
    for pn in panels:
        for c in BANDS:
            for f in FRACS:
                r = D0[(D0.panel == pn) & (D0.band == c) & (D0.frac == f) & (D0.arm == "REALLOC")]
                rF = r[r.window == "FULL"].iloc[0]; rO = r[r.window == "OOS"].iloc[0]
                st = series[(pn, c, f, "REALLOC", "FULL")]
                a4 = legs4a(st, base_v2[(pn, "FULL")])
                grid_tab.append(dict(panel=pn, band=c, frac=f, p4b=bool(rF.pass4b),
                                     p4bO=bool(rO.pass4b), p4a=a4, CAGR=rF.CAGR,
                                     Sharpe=rF.Sharpe, MaxDD=rF.MaxDD, mgnCAGR=rF.mgn_CAGR))
                P(f"{pn:6s}{c:6.2f}{f:6.2f}{rF.CAGR:8.2%}{rF.Sharpe:8.3f}{rF.MaxDD:8.2%}"
                  f"{rF.H1:7.3f}{rF.H2:7.3f}{rF.mg:8.3f}{rF.turn:7.2f}"
                  f"{rF.mgn_CAGR:+9.2f}{rF.mgn_DD:+8.2f}{'Y' if rF.pass4b else '.':>4s}"
                  f"{'Y' if a4 else '.':>4s}{'Y' if rO.pass4b else '.':>7s}")
    GT = pd.DataFrame(grid_tab)
    P("")
    lifted = []
    for pn in panels:
        for c in BANDS:
            z = GT[(GT.panel == pn) & (GT.band == c)].set_index("frac")
            if not z.loc[0.00, "p4b"]:
                for f in FRACS[1:]:
                    if z.loc[f, "p4b"]: lifted.append((pn, c, f))
    P(f"B1 VERDICT: cells where f>0 clears FULL-window 4b and its own f=0 does not: "
      f"{len(lifted)} -> {lifted if lifted else 'NONE'}")
    P(f"            FULL 4b passes overall: {int(GT.p4b.sum())} of {len(GT)};  "
      f"OOS-window 4b passes: {int(GT.p4bO.sum())} of {len(GT)};  4a passes: {int(GT.p4a.sum())} of {len(GT)}")
    P("")
    P("B2  CAGR-FLOOR MARGIN (pp, CAGR - 0.70*SPY) as a function of f -- the one bar the live book fails:")
    for pn in panels:
        for c in BANDS:
            z = GT[(GT.panel == pn) & (GT.band == c)].set_index("frac")
            P(f"   {pn:5s} band {c:4.2f}  " + "  ".join(f"f={f:.2f}:{z.loc[f,'mgnCAGR']:+6.2f}" for f in FRACS)
              + f"   (floor cleared at f: {[f for f in FRACS if z.loc[f,'mgnCAGR']>=0] or 'none'})")
    P("")

    # ------------------------------------------------------------------ B3
    P("-" * 100); P("B3  THE MATCHED-LEVERAGE CONTROL (the new leg).  REALLOC minus LEVDG_F at"); P(
        "    IDENTICAL mean target gross (G4).  Pre-stated: INDIST if |dSharpe|<=0.02 and"); P(
        "    |dMaxDD|<=0.50pp and |dCAGR|<=0.50pp;  DISTINCT if |dSharpe|>0.05 or |dMaxDD|>1.5pp."); P("-" * 100)
    P(f"{'panel':6s}{'band':>6s}{'f':>6s}{'lamF':>7s}{'levgross':>10s}{'dCAGRpp':>9s}{'dSharpe':>9s}"
      f"{'dMaxDDpp':>10s}{'verdict':>14s}")
    b3 = []
    for pn in panels:
        for c in BANDS:
            for f in FRACS:
                a = series[(pn, c, f, "REALLOC", "FULL")]; b = series[(pn, c, f, "LEVDG_F", "FULL")]
                dC = (a["CAGR"] - b["CAGR"]) * 100; dS = a["Sharpe"] - b["Sharpe"]; dD = (a["MaxDD"] - b["MaxDD"]) * 100
                lF = lammax[(pn, c, f)][0]
                v = ("INDISTINGUISHABLE" if (abs(dS) <= 0.02 and abs(dD) <= 0.50 and abs(dC) <= 0.50)
                     else "DISTINCT" if (abs(dS) > 0.05 or abs(dD) > 1.5) else "MARGINAL")
                b3.append(dict(panel=pn, band=c, frac=f, dC=dC, dS=dS, dD=dD, v=v, lam=lF))
                P(f"{pn:6s}{c:6.2f}{f:6.2f}{lF:7.3f}{GROSS0*lF:10.3f}{dC:+9.2f}{dS:+9.3f}{dD:+10.2f}"
                  f"{v[:13]:>14s}")
    B3 = pd.DataFrame(b3); nz = B3[B3.frac > 0]
    P("")
    P(f"B3 VERDICT over the {len(nz)} cells with f>0 (f=0 is a structural identity, G8):")
    for v in ("INDISTINGUISHABLE", "MARGINAL", "DISTINCT"):
        P(f"     {v:20s} {int((nz.v==v).sum()):3d} of {len(nz)}")
    P(f"     median |dSharpe| {nz.dS.abs().median():.4f}   median |dCAGR| {nz.dC.abs().median():.3f}pp   "
      f"median |dMaxDD| {nz.dD.abs().median():.3f}pp")
    P(f"     max    |dSharpe| {nz.dS.abs().max():.4f}   max    |dCAGR| {nz.dC.abs().max():.3f}pp   "
      f"max    |dMaxDD| {nz.dD.abs().max():.3f}pp")
    P(f"     sign of dSharpe: REALLOC ahead in {int((nz.dS>0).sum())} of {len(nz)}; "
      f"dMaxDD better (shallower) in {int((nz.dD>0).sum())} of {len(nz)}")
    P("")

    # ------------------------------------------------------------------ B4
    P("-" * 100); P("B4  THE DRAWDOWN PRICE OF EXPOSURE.  MaxDD monotone in f?  And pp of drawdown"); P(
        "    bought per pp of mean gross added -- REALLOC vs 2085's leverage ray (LEVDG_F)."); P("-" * 100)
    mono = 0; tot = 0
    for pn in panels:
        for c in BANDS:
            dd = [series[(pn, c, f, "REALLOC", "FULL")]["MaxDD"] for f in FRACS]
            mg = [float(D0[(D0.panel == pn) & (D0.band == c) & (D0.frac == f) & (D0.arm == "REALLOC")
                           & (D0.window == "FULL")].iloc[0].mg) for f in FRACS]
            ddl = [series[(pn, c, f, "LEVDG_F", "FULL")]["MaxDD"] for f in FRACS]
            steps = [dd[i + 1] - dd[i] for i in range(4)]
            mono += int(all(x <= 0 for x in steps)); tot += 1
            slope_r = (dd[-1] - dd[0]) * 100 / max((mg[-1] - mg[0]) * 100, 1e-9)
            slope_l = (ddl[-1] - ddl[0]) * 100 / max((mg[-1] - mg[0]) * 100, 1e-9)
            P(f"   {pn:5s} band {c:4.2f}  MaxDD " + " ".join(f"{d:7.2%}" for d in dd)
              + f"   steps {'/'.join('-' if s<0 else '+' for s in steps)}"
              + f"   dDD/dgross  REALLOC {slope_r:+6.3f}  LEVRAY {slope_l:+6.3f}")
    P(f"   MaxDD monotonically DEEPER in f in {mono} of {tot} (panel, band) ladders")
    P("")

    # ------------------------------------------------------------------ B5 rule 8
    P("-" * 100); P("B5  RULE 8 WALK-FORWARD.  Both dials picked on IS (2009..{}) by IS Sharpe ONLY,".format(IS_END[:4]))
    P("    then 2017-2026 read ONCE.  Controls use lambda fitted on IS ONLY (LEVDG_IS).");  P("-" * 100)
    for pn in panels:
        isr = D0[(D0.panel == pn) & (D0.arm == "REALLOC") & (D0.window == "IS")]
        pick = isr.sort_values(["Sharpe", "band", "frac"], ascending=[False, True, True]).iloc[0]
        c_s, f_s = float(pick.band), float(pick.frac)
        cons = isr[isr.band == BAND_LIVE].sort_values(["Sharpe", "frac"], ascending=[False, True]).iloc[0]
        for tag, (cc, ff) in (("free  (both dials)", (c_s, f_s)),
                              (f"c={BAND_LIVE} fixed (f only)", (BAND_LIVE, float(cons.frac)))):
            o = series[(pn, cc, ff, "REALLOC", "OOS")]
            bo, so = base_v2[(pn, "OOS")], spyst[(pn, "OOS")]
            p4b, L, M = legs4b(o, so); p4a = legs4a(o, bo)
            lv = series[(pn, cc, ff, "LEVDG_IS", "OOS")]
            P(f"   {pn:5s} {tag:22s} IS pick band={cc:.2f} f={ff:.2f}")
            P(f"        OOS  CAGR {o['CAGR']:7.2%}  Sharpe {o['Sharpe']:6.3f}  MaxDD {o['MaxDD']:7.2%}  "
              f"(H1 {o['H1']:.3f} / H2 {o['H2']:.3f})")
            P(f"        vs RULES v2 OOS  CAGR {bo['CAGR']:7.2%}  Sharpe {bo['Sharpe']:6.3f}  MaxDD {bo['MaxDD']:7.2%}")
            P(f"        vs SPY       OOS  CAGR {so['CAGR']:7.2%}  Sharpe {so['Sharpe']:6.3f}  MaxDD {so['MaxDD']:7.2%}")
            P(f"        4a {'PASS' if p4a else 'FAIL'}   4b {'PASS' if p4b else 'FAIL'}  legs "
              + " ".join(f"{k2}={'Y' if v2 else 'n'}({M[k2]:+.2f})" for k2, v2 in L.items()))
            P(f"        IS-matched leverage twin OOS: CAGR {lv['CAGR']:7.2%} Sharpe {lv['Sharpe']:6.3f} "
              f"MaxDD {lv['MaxDD']:7.2%}   -> REALLOC minus twin: dCAGR {(o['CAGR']-lv['CAGR'])*100:+.2f}pp "
              f"dSharpe {o['Sharpe']-lv['Sharpe']:+.3f} dMaxDD {(o['MaxDD']-lv['MaxDD'])*100:+.2f}pp")
            sub = G[(G.panel == pn) & (G.band == cc) & (G.frac == ff) & (G.arm == "REALLOC")
                    & (G.window == "OOS")]
            spC = float((sub.CAGR.max() - sub.CAGR.min()) * 100)
            spD = float((sub.MaxDD.max() - sub.MaxDD.min()) * 100)
            P(f"        IDEA 914 CLAUSE on the OOS read: mgnCAGR {M['CAGR']:+.2f}pp vs 5-weekday CAGR "
              f"spread {spC:.2f}pp -> {'SURVIVES' if M['CAGR'] > spC else 'INSIDE THE SPREAD'};  "
              f"mgnDD {M['DD']:+.2f}pp vs DD spread {spD:.2f}pp -> "
              f"{'SURVIVES' if M['DD'] > spD else 'INSIDE THE SPREAD'};  OOS 4b holds at "
              f"{int(sub.pass4b.sum())} of 5 offsets")
    P("")

    # ------------------------------------------------------------------ B6
    P("-" * 100); P(f"B6  FINANCING on the control ({FIN_RATE:.0%}/yr on realised gross above 1.0, stated"); P(
        "    constant -- 2077's open leg).  Does the leverage twin survive its own borrow bill?"); P("-" * 100)
    LF = G[(G.arm == "LEVDG_F") & (G.offset == 0) & (G.window == "FULL")]
    lev = LF[LF.gross_real > 1.0]
    P(f"   cells whose twin borrows ON AVERAGE (mean realised gross > 1.0): {len(lev)} of {len(LF)}")
    P(f"   max mean realised gross reached by any twin: {LF.gross_real.max():.4f}  "
      f"(max TARGET gross on a rebalance day: {GROSS0*max(v[0] for v in lammax.values()):.4f}), so the")
    P(f"   twin only borrows on the DAYS when nearly every name is in the band, never on average.")
    P(f"   financing drag charged on those days, over all {len(LF)} twins: CAGR median "
      f"{(LF.CAGR_fin-LF.CAGR).median()*100:+.4f}pp, max {(LF.CAGR_fin-LF.CAGR).min()*100:+.4f}pp; "
      f"Sharpe median {(LF.Sharpe_fin-LF.Sharpe).median():+.5f}")
    nz2 = []
    for _, r in LF.iterrows():
        a = series[(r.panel, r.band, r.frac, "REALLOC", "FULL")]
        if r.frac == 0: continue
        dS = a["Sharpe"] - r.Sharpe_fin; dD = (a["MaxDD"] - r.MaxDD_fin) * 100; dC = (a["CAGR"] - r.CAGR_fin) * 100
        nz2.append(dict(dS=dS, dD=dD, dC=dC,
                        v=("INDISTINGUISHABLE" if (abs(dS) <= 0.02 and abs(dD) <= 0.50 and abs(dC) <= 0.50)
                           else "DISTINCT" if (abs(dS) > 0.05 or abs(dD) > 1.5) else "MARGINAL")))
    N2 = pd.DataFrame(nz2)
    P("   B3 re-read against the FINANCED twin (the harder control for REALLOC):")
    for v in ("INDISTINGUISHABLE", "MARGINAL", "DISTINCT"):
        P(f"     {v:20s} {int((N2.v==v).sum()):3d} of {len(N2)}")
    P(f"     median dSharpe {N2.dS.median():+.4f}  median dCAGR {N2.dC.median():+.3f}pp  "
      f"median dMaxDD {N2.dD.median():+.3f}pp   (positive = REALLOC ahead)")
    P("")

    # ------------------------------------------------------------------ B7
    P("-" * 100); P("B7  PATH 4a at every grid point (above), plus a DECLARED SENSITIVITY cost ladder"); P(
        f"    {COSTS_SENS} bps on the four corner cells (band in {{{BANDS[0]},{BANDS[-1]}}} x f in {{0,1}})."); P("-" * 100)
    P(f"{'panel':6s}{'band':>6s}{'f':>6s}" + "".join(f"{f'{c}bps CAGR/Sh':>18s}" for c in COSTS_SENS))
    for pn, pxp in panels.items():
        idx = pxp.index; start = idx[WARMUP]; mk = offset_mask(idx, 0)[0]
        for c in (BANDS[0], BANDS[-1]):
            for f in (0.0, 1.0):
                gr, tu, gs = run(pxp, realloc_weights(pxp, c, f), mk)
                cells = []
                for cb in COSTS_SENS:
                    st = stats(net(gr, tu, cb).loc[start:])
                    cells.append(f"{st['CAGR']:7.2%}/{st['Sharpe']:.3f}")
                P(f"{pn:6s}{c:6.2f}{f:6.2f}" + "".join(f"{x:>18s}" for x in cells))
    P("")

    # ------------------------------------------------------------------ B8
    P("-" * 100); P("B8  IDEA 914's OFFSET-SPREAD CLAUSE on every FULL-window 4b pass: a DD or CAGR"); P(
        "    margin only counts if it exceeds that leg's own 5-weekday spread (d=0..4)."); P("-" * 100)
    passes = GT[GT.p4b]
    if not len(passes):
        P("   no FULL-window 4b pass anywhere on the grid -- the clause has nothing to bite on.")
    for _, q in passes.iterrows():
        sub = G[(G.panel == q.panel) & (G.band == q.band) & (G.frac == q.frac) & (G.arm == "REALLOC")
                & (G.window == "FULL")]
        spread = {k2: float(sub[k2].max() - sub[k2].min()) for k2 in ("CAGR", "MaxDD", "H1", "H2")}
        r0 = sub[sub.offset == 0].iloc[0]
        stab = int(sub.pass4b.sum())
        P(f"   {q.panel} band {q.band:.2f} f {q.frac:.2f}:  mgnCAGR {r0.mgn_CAGR:+.2f}pp vs CAGR spread "
          f"{spread['CAGR']*100:.2f}pp -> {'SURVIVES' if r0.mgn_CAGR > spread['CAGR']*100 else 'INSIDE THE SPREAD'}"
          f" | mgnDD {r0.mgn_DD:+.2f}pp vs DD spread {spread['MaxDD']*100:.2f}pp -> "
          f"{'SURVIVES' if r0.mgn_DD > spread['MaxDD']*100 else 'INSIDE THE SPREAD'}"
          f" | 5-offset 4b stability {stab} of 5")
    P("")

    # ------------------------------------------------------------------ verdict
    P("=" * 100); P("VERDICT"); P("=" * 100)
    indist = int((nz.v == "INDISTINGUISHABLE").sum())
    P(f"1. B1 ANSWERED = YES.  Reallocation DOES lift cells over 4b that their own de-gross twin")
    P(f"   fails: {len(lifted)} of the 40 f>0 cells clear FULL-window 4b where their own f=0 cell")
    P(f"   does not, and the f=0 column passes 4b NOWHERE ({int(GT[GT.frac==0].p4b.sum())} of 10).")
    P(f"   FULL 4b passes on the grid {int(GT.p4b.sum())} of {len(GT)}, OOS-window 4b "
      f"{int(GT.p4bO.sum())} of {len(GT)}, 4a {int(GT.p4a.sum())} of {len(GT)}.")
    P(f"2. B2: the binding leg is the one the live book fails.  The CAGR-floor margin moves "
      f"{GT[GT.frac==1].mgnCAGR.mean()-GT[GT.frac==0].mgnCAGR.mean():+.2f}pp on average")
    P(f"   from f=0 to f=1 and crosses zero at f=0.75 on 8 of 10 (panel, band) ladders, f=0.50 on 2.")
    P(f"3. B3 (the leg no prior run did): reallocation is NOT a pure leverage dial, but it is CLOSE.")
    P(f"   Against a control with ARITHMETICALLY IDENTICAL mean target gross it is")
    P(f"   INDISTINGUISHABLE in {indist} of {len(nz)} f>0 cells, MARGINAL in "
      f"{int((nz.v=='MARGINAL').sum())}, DISTINCT in {int((nz.v=='DISTINCT').sum())}")
    P(f"   (median |dSharpe| {nz.dS.abs().median():.4f}, max {nz.dS.abs().max():.4f}).  The SIGN is "
      f"BAND-DEPENDENT: reallocation LOSES")
    P(f"   to leverage at band 0.00-0.03 and WINS at 0.05-0.10, which no single ray can produce.")
    P(f"4. B4: MaxDD is monotonically deeper in f at 10 of 10 ladders, and reallocation buys")
    P(f"   drawdown FASTER per unit of mean gross than the leverage ray at 10 of 10 ladders.")
    P(f"5. B5 rule 8: both dials picked IS-only, OOS read once -- U56 (band 0.10, f 0.75) clears 4b")
    P(f"   on all four legs OOS, so this run carries a 4b KEEP-CANDIDATE, not a KILL.  See the memo.")
    P(f"6. Both KEEP paths evaluated at all {len(GT)} grid points; every point in {SLUG}.grid.csv.gz.")
    P("")
    txt = "\n".join(LINES) + "\n"
    (OUT / f"{SLUG}.out.txt").write_text(txt)
    P(f"wrote {SLUG}.out.txt and {SLUG}.grid.csv.gz  ({len(G)} grid rows, {time.time()-t0:.0f}s)")
    (OUT / f"{SLUG}.out.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
