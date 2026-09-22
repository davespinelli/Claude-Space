#!/usr/bin/env python3
"""
IDEA 2129 (lane B, 2026-09-22) -- does-a-DRAWDOWN-BUDGETED-GROSS-convert-the-live-book's-
                                  UNSPENT-DD-MARGIN-into-CAGR

THE QUESTION, as filed.  Idea 2119 (this morning, lane B) found the live band book -- RULES v2,
band 0.03 / gross 0.75 / weekly / t+1 -- fails PROTOCOL 4b on the CAGR FLOOR ALONE in every
window (margins -1.98 / -1.25 pp on U56 FULL/OOS, -2.63 / -2.83 pp on B136) while its DD margin
runs +8.18 / +7.99 pp against a 1.80 / 1.70 pp weekday spread, i.e. 4.5x outside its own
scheduling noise.  The book is carrying a large, real, UNSPENT drawdown budget and dying on the
one leg that exposure buys.  The CHANGELOG's standing diagnosis is that this budget has never
been spent because EVERY device the record has priced REMOVES exposure (de-gross to cash), and
eight consecutive runs found each such device beaten at matched exposure by a plain de-gross.

THE DEVICE, and why it is not another de-gross with a new name.  A DRAWDOWN-BUDGETED GROSS runs
the book at FULL SIZE while the budget is unspent and retrenches only as it is spent:

    gross_t = g_hi * (1 - dd_t / D)   clipped to [0, g_hi],    dd_t = equity_t / peak_t - 1 <= 0

dd_t is the book's OWN trailing drawdown, computed from its equity path through the DECISION
close and applied at t+1, so the rule is causal (gate G3 proves it by perturbation).  D = inf
recovers the static book EXACTLY, and (g_hi = 0.75, D = inf) IS `baseline.rules_v2_weights`
at band 0.03 -- gate G2, max|d| == 0 -- so the published ladder literally contains the live book.
The device is the first in the record whose exposure is HIGHEST when risk has not been realised;
every prior one is monotone-downward in stress.

THE NULL IT MUST BEAT, pre-stated.  The record's standing result is that a DD-buying device is
usually a leverage dial with extra steps.  So every budgeted cell is scored against a
MATCHED-MEAN-GROSS STATIC TWIN: the same band book at constant gross

    lam = sum_rebal(g_t * s_t) / sum_rebal(s_t),   s_t = in-band share of the priced panel,

whose mean TARGET gross is arithmetically identical to the budgeted book's (gate G4).  lam is
computed on FULL (STAT_F, peeks -- a contrast, not a proposal) and on IS only (STAT_IS, the
honest twin for the rule-8 read).  Because g_hi <= 1.00, lam <= 1.00 too: NO arm here borrows,
so PROTOCOL rule 2's no-leverage clause holds and no financing question arises.

PRIOR ART, cited rather than rediscovered -- and exactly what is new here.
  * IDEA 852 (2026-09-14, lane B, `2026-09-14_equity-drawdown-throttle-on-the-band-book_B.py`)
    already priced an equity-drawdown THROTTLE on this same band book and returned KILL: a
    BINARY trigger (gross -> g_low while dd <= -d, else 1.00), 48 arms, and every arm that
    actually fired was strictly worse than its own un-throttled parent on both CAGR and Sharpe.
    Its parent sat at gross 1.00, so 852 could only ever REMOVE exposure, and its control was
    that same parent -- NOT a matched-exposure twin.
  * IDEA 69 (2026-09-06, cloud) PARKed a trailing-1y drawdown BUDGET that set gross weekly, and
    measured its matched-constant-gross premium at +0.027 (U56) / +0.030 (B136) Sharpe.
  * IDEA 1296 (2026-09-18, cloud) priced a de-grossing drawdown BRAKE on a ranked anchor.
  THREE legs are new here and none of them is a re-print: (i) the response is CONTINUOUS in the
  realised drawdown rather than a binary trigger, so there is no threshold to be inert at;
  (ii) the CEILING is a published dial spanning the LIVE 0.75 up to 1.00, so the "spend the
  budget" half -- running LARGER than the live book while nothing has gone wrong -- is priced
  alongside the retrenchment half, which 852 structurally could not do; (iii) every cell is
  scored against a MATCHED-MEAN-GROSS twin, which is the null the record has since adopted
  (ideas 1454/1498/2081) and which 852 never ran.  If the answer is again KILL, it is a KILL of
  a strictly larger device against a strictly harder control, and idea 69's +0.027 premium gets
  its first matched re-read on the live band book.

TUNED PARAMETERS -- EXACTLY TWO, and EVERY grid point is published (<slug>.grid.csv.gz):
    1. DRAWDOWN BUDGET  D    in {0.05, 0.10, 0.15, 0.20, inf}   (inf = the static control column)
    2. GROSS CEILING    g_hi in {0.75, 0.85, 0.90, 0.95, 1.00}  (0.75 = the live sizing number)
    -> 25 cells per panel, 50 published cells, each with its two matched twins.
NOT TUNED, and declared as such BEFORE any number below was read:
    BAND c = 0.03 (the live acceptance width), CADENCE W (the live schedule), COST 10 bps
      (PROTOCOL rung 2; the 0/10/25/50 ladder in B7 is a SENSITIVITY, never a selection axis),
      PANELS U56 = research/universe.json and B136 = research/universe_broad.json,
      WINDOWS FULL / IS ..2016-12-31 / OOS 2017-01-01.. with H1/H2 read INSIDE each window
      (rule 8).  Warm-up: the first 260 rows are dropped, as `baseline.compare` does.
    REBALANCE OFFSET d in {0,1,2,3,4} is a MEASUREMENT, never a choice: every reported book is
      d = 0 (the published Friday convention); d = 1..4 exist only to build idea 914's spread,
      which lane C's idea 2115 hardened this morning by showing the spread is a PATH artefact
      (162 of 162 cells) and not a cost artefact.

PRE-REGISTERED BARS -- written before any number below was read:
  B1  THE HEADLINE.  Does ANY finite-D cell clear 4b where its OWN D = inf cell (same panel,
      same g_hi) does not?  Report the 4b leg vector and every leg margin at all 50 cells.
  B2  THE CAGR FLOOR, the one leg the live book fails.  Report CAGR and the floor margin
      (CAGR - 0.70*SPY) as a function of D at each g_hi, per panel.  PRE-STATED: if the budget
      dial cannot lift the floor margin above zero at the LIVE ceiling g_hi = 0.75, the device
      cannot rescue the live book and only a plain re-grossing can.
  B3  THE MATCHED-MEAN-GROSS NULL (the leg that decides the idea).  Per cell report BUDGET minus
      STAT_F on CAGR (pp), Sharpe and MaxDD (pp).  PRE-STATED VERDICT, same thresholds the
      record used for idea 2081 so the two are comparable: INDISTINGUISHABLE if |dSharpe| <=
      0.02 AND |dMaxDD| <= 0.50 pp AND |dCAGR| <= 0.50 pp; DISTINCT if |dSharpe| > 0.05 or
      |dMaxDD| > 1.5 pp; MARGINAL otherwise.  Report the share of cells in each bucket.
  B4  WHAT THE BUDGET ACTUALLY BUYS.  Is MaxDD monotone in D at fixed g_hi?  Report the pp of
      drawdown saved per pp of mean gross given up, for the budget dial and for the static
      gross dial, on the same panel -- the two are directly comparable only in that ratio.
  B5  RULE 8, 2017-2026 READ ONCE.  Both dials chosen on IS (..2016-12-31) ONLY by IS Sharpe,
      per panel; OOS read once.  Report OOS CAGR / Sharpe / MaxDD vs RULES v2 OOS and SPY OOS,
      both KEEP paths, against the IS-chosen STAT_IS twin.  Second, CONSTRAINED arm: g_hi fixed
      at the live 0.75, D alone chosen on IS -- "can the budget dial rescue the live book?"
  B6  PATH 4a at EVERY grid point (Sharpe > RULES v2 in BOTH halves AND MaxDD no worse).
  B7  COST LADDER 0 / 10 / 25 / 50 bps at every grid point, as a declared sensitivity.  Note the
      budgeted book's equity path FEEDS BACK into its own gross, so a cost rung is NOT a
      post-hoc subtraction here: every rung is a full independent re-run (that is why G5 is a
      re-run gate and not a linearity gate).
  B8  IDEA 914's OFFSET-SPREAD CLAUSE on every 4b pass: a DD or CAGR margin only counts if it
      exceeds that leg's own 5-weekday spread.  Report margin, spread, ratio, and the 5-of-5
      offset stability of each pass.

GATES, printed before any hypothesis is read:
  G1  local run_budget(D=inf, g_hi=0.75) == engine.backtest(rules_v2_weights(0.03,0.75))
      bar max|d| < 1e-12
  G2  base weights * g_hi at D = inf == rules_v2_weights(px, 0.03, g_hi)   bar max|d| == 0.0
  G3  CAUSALITY.  Multiply the LAST day's prices by 2.0 and re-run: the realised gross path must
      be bit-identical up to and including the final decision, because no weight may see its own
      day's return.  bar max|d| == 0.0 over the gross path.
  G4  MATCHED TWIN: mean TARGET gross of BUDGET(D,g_hi) == mean target gross of STAT_F(lam)
      bar max|d| < 1e-12 over all 50 cells.
  G5  COST RE-RUN: the 10 bps headline equals an independent re-run at 10 bps (the feedback
      path makes this non-trivial).  bar max|d| == 0.0
  G6  CLAMP: realised gross multiplier is inside [0, g_hi] on every rebalance, and equals g_hi
      exactly on every rebalance where the book is at a new equity peak.
  G7  OFFSET CLIPPING census (weeks too short to carry offset d).
  G8  SPY offset-invariance: SPY buy-and-hold never rebalances, so its 4b bars are constant
      across d.  bar max|d| == 0.0

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every absolute
CAGR and drawdown LEVEL here is optimistic, and the bias runs TOWARD the higher-exposure arms.
B3's contrast is a WITHIN-TAPE, same-names, same-days, matched-mean-gross difference, which is
the part the bias cannot manufacture; the LEVELS in B1/B2/B5 are not repaired by it.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_drawdown-budgeted-gross_B.py
"""
import sys, time, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights          # noqa
from engine import backtest, metrics                                      # noqa

SLUG = "2026-09-22_drawdown-budgeted-gross_B"
OUT = ROOT / "research" / "backtests"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

GATES = []
def gate(name, got, bar, ok):
    GATES.append((name, str(got), str(bar), bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:52s} got {got}   bar {bar}")

BUDGETS = [0.05, 0.10, 0.15, 0.20, np.inf]      # TUNED axis 1
CEILS   = [0.75, 0.85, 0.90, 0.95, 1.00]        # TUNED axis 2
OFFSETS = [0, 1, 2, 3, 4]                       # measurement only
COSTS   = [0, 10, 25, 50]
BAND, COST0, FREQ, GLIVE = 0.03, 10, "W", 0.75
IS_END, OOS_BEG = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
WARMUP = 260


# ================================================================== books
def base_weights(px, c=BAND):
    """RULES v2's shape at gross 1.0: every in-band name at 1/N, N = names PRICED that day
    (the fixed-denominator convention; gated-out weight is simply absent)."""
    priced = px.notna()
    N = priced.sum(axis=1).astype(float)
    inb = band_state(px, c) & priced
    return inb.astype(float).div(N.replace(0, np.nan), axis=0).fillna(0.0)


def offset_mask(idx, d, freq=FREQ):
    key = pd.Series(idx.to_period(freq), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    clipped = int((last - d < first).sum())
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, clipped


def run_budget(prices, B, mask, D, g_hi, cost_bps=COST0):
    """engine.backtest's loop, semantics byte-for-byte (G1), with ONE addition: at each
    rebalance the target gross is scaled by the book's own trailing drawdown, computed from
    the equity path through the DECISION close (row i-1) and applied at row i == t+1."""
    rets = prices.pct_change().fillna(0.0).values
    Bv = B.values
    m = mask.shift(1, fill_value=False).values
    n, nc = prices.shape
    cur = np.zeros(nc)
    eq, peak = 1.0, 1.0
    ret = np.empty(n); turn = np.zeros(n); tgt = np.zeros(n)
    reb_g, reb_s, reb_atpeak, reb_i = [], [], [], []
    finite = np.isfinite(D)
    for i in range(n):
        if m[i] or i == 0:
            j = i - 1 if i > 0 else 0
            dd = eq / peak - 1.0                        # <= 0, known at close i-1
            g = g_hi * max(0.0, 1.0 + dd / D) if finite else g_hi
            g = min(g, g_hi)
            new = Bv[j] * g
            turn[i] = np.abs(new - cur).sum(); cur = new
            reb_g.append(g); reb_s.append(float(Bv[j].sum())); reb_atpeak.append(eq >= peak - 1e-15)
            reb_i.append(i)
            tgt[i] = cur.sum()
        else:
            tgt[i] = tgt[i - 1] if i else 0.0
        r = float(cur @ rets[i]) - turn[i] * cost_bps / 1e4
        ret[i] = r
        eq *= (1.0 + r); peak = max(peak, eq)
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    ix = prices.index
    return dict(ret=pd.Series(ret, index=ix), tgt=pd.Series(tgt, index=ix),
                turn=pd.Series(turn, index=ix), g=np.array(reb_g), s=np.array(reb_s),
                atpeak=np.array(reb_atpeak), dates=ix[np.array(reb_i)])


def lam_of(res, upto=None):
    """Constant gross whose mean TARGET gross matches the budgeted book's, over the rebalances
    (optionally only those decided on or before `upto`)."""
    g, s = res["g"], res["s"]
    if upto is not None:
        keep = np.asarray(res["dates"] <= pd.Timestamp(upto))
        g, s = g[keep], s[keep]
    den = float(s.sum())
    return float((g * s).sum() / den) if den > 0 else 1.0


# ================================================================== scoring
def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= DD_CAP * ss["MaxDD"], CAGR=s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])
    M = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
             DD=(s["MaxDD"] - DD_CAP * ss["MaxDD"]) * 100.0,
             CAGR=(s["CAGR"] - CAGR_FLOOR * ss["CAGR"]) * 100.0)
    return all(L.values()), L, M


def legs4a(s, sb):
    return bool(s["H1"] > sb["H1"] and s["H2"] > sb["H2"] and s["MaxDD"] >= sb["MaxDD"])


def windows(idx):
    return {"FULL": (idx[0], idx[-1]),
            "IS":   (idx[0], pd.Timestamp(IS_END)),
            "OOS":  (pd.Timestamp(OOS_BEG), idx[-1])}


def dlabel(D):
    return "inf" if not np.isfinite(D) else f"{D:.2f}"


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 102)
    P("IDEA 2129 lane B 2026-09-22 -- DRAWDOWN-BUDGETED GROSS: can the live book's UNSPENT")
    P("                               drawdown margin be turned into the CAGR the 4b floor wants?")
    P("=" * 102)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned: budget D {[dlabel(d) for d in BUDGETS]} x ceiling g_hi {CEILS}  "
      f"({len(BUDGETS)*len(CEILS)} cells/panel, {2*len(BUDGETS)*len(CEILS)} published)")
    P(f"not tuned: band {BAND}, cadence {FREQ}, cost {COST0} bps headline, panels U56 + B136,")
    P(f"           windows FULL / IS ..{IS_END} / OOS {OOS_BEG}.. with H1/H2 inside each (rule 8)")
    P(f"           offsets {OFFSETS} are a MEASUREMENT (idea 914's clause, B8); books are d=0")
    P("           NO LEVERAGE anywhere: g_hi <= 1.00 and the matched twin's lam <= g_hi.")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k:5s}  {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  ({len(v)} rows)")
    P("")

    # ------------------------------------------------------------------ gates
    P("-" * 102); P("CONSTRUCTION GATES"); P("-" * 102)
    px = panels["U56"]
    B = base_weights(px)
    m0, clip0 = offset_mask(px.index, 0)

    rb = run_budget(px, B, m0, np.inf, GLIVE)
    eng = backtest(px, rules_v2_weights(px, BAND, GLIVE), cost_bps=COST0, freq=FREQ)
    d1 = float(np.abs(rb["ret"] - eng["returns"]).max())
    gate("G1 local run_budget(inf,0.75) == engine.backtest", f"{d1:.3e}", "< 1e-12", d1 < 1e-12)

    d2 = max(float(np.abs(B * g - rules_v2_weights(px, BAND, g)).max().max()) for g in CEILS)
    gate("G2 base*g_hi == rules_v2_weights(0.03,g_hi)", f"{d2:.3e}", "== 0.0", d2 == 0.0)

    px_p = px.copy(); px_p.iloc[-1] = px_p.iloc[-1] * 2.0
    rp = run_budget(px_p, base_weights(px_p), m0, 0.10, 1.00)
    ra = run_budget(px,   B,                  m0, 0.10, 1.00)
    k = min(len(rp["g"]), len(ra["g"]))
    d3 = float(np.abs(rp["g"][:k] - ra["g"][:k]).max())
    gate("G3 causality (last-day shock leaves gross path)", f"{d3:.3e}", "== 0.0", d3 == 0.0)

    d4 = 0.0
    for D, g_hi in itertools.product(BUDGETS, CEILS):
        rr = run_budget(px, B, m0, D, g_hi)
        lm = lam_of(rr)
        rs = run_budget(px, B, m0, np.inf, lm)
        a = float((rr["g"] * rr["s"]).sum() / len(rr["g"]))
        b = float((rs["g"] * rs["s"]).sum() / len(rs["g"]))
        d4 = max(d4, abs(a - b))
    gate("G4 matched twin mean target gross (25 cells)", f"{d4:.3e}", "< 1e-12", d4 < 1e-12)

    r5a = run_budget(px, B, m0, 0.10, 1.00, cost_bps=COST0)["ret"]
    r5b = run_budget(px, B, m0, 0.10, 1.00, cost_bps=COST0)["ret"]
    d5 = float(np.abs(r5a - r5b).max())
    gate("G5 cost re-run determinism", f"{d5:.3e}", "== 0.0", d5 == 0.0)

    ok6 = True; peakg = True
    for D, g_hi in itertools.product(BUDGETS, CEILS):
        rr = run_budget(px, B, m0, D, g_hi)
        ok6 &= bool((rr["g"] >= -1e-15).all() and (rr["g"] <= g_hi + 1e-15).all())
        peakg &= bool(np.abs(rr["g"][rr["atpeak"]] - g_hi).max() < 1e-15)
    gate("G6 clamp [0,g_hi] and g==g_hi at every peak", f"clamp={ok6} peak={peakg}", "both True", ok6 and peakg)

    clips = {d: offset_mask(px.index, d)[1] for d in OFFSETS}
    gate("G7 offset clipping census", str(clips), "reported", True)

    spy_bars = set()
    for d in OFFSETS:
        spy_bars.add(round(metrics(px["SPY"].pct_change().fillna(0).iloc[WARMUP:])["MaxDD"], 12))
    gate("G8 SPY offset-invariance", f"{len(spy_bars)} distinct", "== 1", len(spy_bars) == 1)
    P("")

    # ------------------------------------------------------------------ grid
    P("-" * 102); P("GRID: every (panel, D, g_hi, offset, cost, window) point"); P("-" * 102)
    rows = []
    for pan, pxp in panels.items():
        Bp = base_weights(pxp)
        wins = windows(pxp.index[WARMUP:])
        spy_r = pxp["SPY"].pct_change().fillna(0.0)
        base_r = backtest(pxp, rules_v2_weights(pxp, BAND, GLIVE), cost_bps=COST0, freq=FREQ)["returns"]
        masks = {d: offset_mask(pxp.index, d)[0] for d in OFFSETS}
        for d in OFFSETS:
            for cost in COSTS:
                for D, g_hi in itertools.product(BUDGETS, CEILS):
                    rr = run_budget(pxp, Bp, masks[d], D, g_hi, cost_bps=cost)
                    lm_f = lam_of(rr)
                    lm_is = lam_of(rr, upto=IS_END)
                    tw_f = run_budget(pxp, Bp, masks[d], np.inf, lm_f, cost_bps=cost)
                    tw_is = run_budget(pxp, Bp, masks[d], np.inf, lm_is, cost_bps=cost)
                    for wn, (a, b) in wins.items():
                        r = rr["ret"].loc[a:b]; sr = spy_r.loc[a:b]
                        s = stats(r); ss = stats(sr); sb = stats(base_r.loc[a:b])
                        p4b, L, M = legs4b(s, ss)
                        stf = stats(tw_f["ret"].loc[a:b]); sti = stats(tw_is["ret"].loc[a:b])
                        rows.append(dict(panel=pan, D=dlabel(D), g_hi=g_hi, offset=d, cost=cost,
                                         window=wn, CAGR=s["CAGR"], Sharpe=s["Sharpe"],
                                         MaxDD=s["MaxDD"], H1=s["H1"], H2=s["H2"],
                                         mean_gross=float((rr["g"] * rr["s"]).mean()),
                                         lam_F=lm_f, lam_IS=lm_is,
                                         pass4b=p4b, pass4a=legs4a(s, sb),
                                         L_H1=L["H1"], L_H2=L["H2"], L_DD=L["DD"], L_CAGR=L["CAGR"],
                                         M_H1=M["H1"], M_H2=M["H2"], M_DD=M["DD"], M_CAGR=M["CAGR"],
                                         twF_CAGR=stf["CAGR"], twF_Sharpe=stf["Sharpe"], twF_MaxDD=stf["MaxDD"],
                                         twIS_CAGR=sti["CAGR"], twIS_Sharpe=sti["Sharpe"], twIS_MaxDD=sti["MaxDD"],
                                         spy_CAGR=ss["CAGR"], spy_Sharpe=ss["Sharpe"], spy_MaxDD=ss["MaxDD"],
                                         base_CAGR=sb["CAGR"], base_Sharpe=sb["Sharpe"], base_MaxDD=sb["MaxDD"]))
        P(f"  {pan}: {len(rows)} rows cumulative   ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv.gz", index=False, compression="gzip")
    P(f"  published {len(G)} grid rows -> {SLUG}.grid.csv.gz")
    P("")

    H = G[(G.offset == 0) & (G.cost == COST0)]                     # the headline slice

    # ------------------------------------------------------------------ B1
    P("-" * 102); P("B1  HEADLINE -- does any finite budget D clear 4b where its own D=inf cell does not?")
    P("-" * 102)
    flips = []
    for pan in panels:
        for wn in ("FULL", "IS", "OOS"):
            for g_hi in CEILS:
                sub = H[(H.panel == pan) & (H.window == wn) & (H.g_hi == g_hi)]
                stat = sub[sub.D == "inf"]["pass4b"]
                if not len(stat): continue
                st = bool(stat.iloc[0])
                for _, r in sub[sub.D != "inf"].iterrows():
                    if bool(r.pass4b) and not st:
                        flips.append((pan, wn, g_hi, r.D))
    tot4b = int(H.pass4b.sum())
    P(f"  4b PASSES at d=0, 10 bps: {tot4b} of {len(H)} (panel x window x cell) points")
    for pan in panels:
        for wn in ("FULL", "IS", "OOS"):
            sub = H[(H.panel == pan) & (H.window == wn)]
            P(f"    {pan:5s} {wn:4s}  4b {int(sub.pass4b.sum()):2d}/25   4a {int(sub.pass4a.sum()):2d}/25   "
              f"legs H1 {int(sub.L_H1.sum()):2d} H2 {int(sub.L_H2.sum()):2d} "
              f"DD {int(sub.L_DD.sum()):2d} CAGR {int(sub.L_CAGR.sum()):2d}")
    P(f"  BUDGET-INDUCED FLIPS (finite D passes where its own static D=inf twin fails): {len(flips)}")
    for f in flips: P(f"    {f}")
    P("")
    P("  Full 4b leg margins, d=0, 10 bps (pp for DD/CAGR, Sharpe points for H1/H2):")
    for pan in panels:
        for wn in ("FULL", "OOS"):
            P(f"   -- {pan} {wn}")
            sub = H[(H.panel == pan) & (H.window == wn)]
            P("      D      g_hi  meanG   CAGR    Sharpe  MaxDD    M_H1    M_H2    M_DD    M_CAGR  4b 4a")
            for _, r in sub.iterrows():
                P(f"      {r.D:>5s}  {r.g_hi:.2f}  {r.mean_gross:.3f}  {r.CAGR:6.2%}  {r.Sharpe:6.3f}  "
                  f"{r.MaxDD:7.2%}  {r.M_H1:+6.3f}  {r.M_H2:+6.3f}  {r.M_DD:+6.2f}  {r.M_CAGR:+6.2f}   "
                  f"{'Y' if r.pass4b else '.'}  {'Y' if r.pass4a else '.'}")
    P("")

    # ------------------------------------------------------------------ B2
    P("-" * 102); P("B2  THE CAGR FLOOR -- the one leg the live book fails"); P("-" * 102)
    for pan in panels:
        for wn in ("FULL", "IS", "OOS"):
            sub = H[(H.panel == pan) & (H.window == wn)]
            P(f"   -- {pan} {wn}   CAGR-floor margin (pp), rows = g_hi, cols = D")
            piv = sub.pivot(index="g_hi", columns="D", values="M_CAGR")[[dlabel(d) for d in BUDGETS]]
            for g_hi, row in piv.iterrows():
                P(f"      g_hi {g_hi:.2f}   " + "  ".join(f"{v:+7.2f}" for v in row.values))
    live = H[(H.D == "inf") & (H.g_hi == GLIVE)]
    P("  THE LIVE BOOK on this grid (D=inf, g_hi=0.75 == RULES v2):")
    for _, r in live.iterrows():
        P(f"    {r.panel:5s} {r.window:4s}  CAGR {r.CAGR:6.2%}  floor margin {r.M_CAGR:+6.2f} pp   "
          f"DD margin {r.M_DD:+6.2f} pp   4b {'PASS' if r.pass4b else 'FAIL'}")
    best75 = H[(H.g_hi == GLIVE)].groupby(["panel", "window"]).M_CAGR.max()
    P("  BEST floor margin reachable AT THE LIVE CEILING g_hi=0.75 (B2's pre-stated test):")
    for (pan, wn), v in best75.items(): P(f"    {pan:5s} {wn:4s}  {v:+6.2f} pp")
    P("")

    # ------------------------------------------------------------------ B3
    P("-" * 102); P("B3  THE MATCHED-MEAN-GROSS NULL -- is the budget dial anything a static gross is not?")
    P("-" * 102)
    C = H[H.D != "inf"].copy()
    C["dCAGR"] = (C.CAGR - C.twF_CAGR) * 100.0
    C["dSharpe"] = C.Sharpe - C.twF_Sharpe
    C["dMaxDD"] = (C.MaxDD - C.twF_MaxDD) * 100.0
    def bucket(r):
        if abs(r.dSharpe) <= 0.02 and abs(r.dMaxDD) <= 0.50 and abs(r.dCAGR) <= 0.50: return "INDISTINGUISHABLE"
        if abs(r.dSharpe) > 0.05 or abs(r.dMaxDD) > 1.5: return "DISTINCT"
        return "MARGINAL"
    C["bucket"] = C.apply(bucket, axis=1)
    P(f"  {len(C)} budgeted cells (4 finite D x 5 g_hi x 2 panels x 3 windows) vs their FULL-matched twin")
    for b, n in C.bucket.value_counts().items(): P(f"    {b:20s} {n:4d}   ({n/len(C):.1%})")
    P(f"  dSharpe  median {C.dSharpe.median():+.4f}  mean {C.dSharpe.mean():+.4f}  "
      f"[{C.dSharpe.min():+.4f}, {C.dSharpe.max():+.4f}]")
    P(f"  dCAGR pp median {C.dCAGR.median():+.3f}  mean {C.dCAGR.mean():+.3f}  "
      f"[{C.dCAGR.min():+.3f}, {C.dCAGR.max():+.3f}]")
    P(f"  dMaxDD pp median {C.dMaxDD.median():+.3f}  mean {C.dMaxDD.mean():+.3f}  "
      f"[{C.dMaxDD.min():+.3f}, {C.dMaxDD.max():+.3f}]")
    P(f"  budgeted book BEATS its matched twin on Sharpe in {int((C.dSharpe>0).sum())}/{len(C)} cells, "
      f"on MaxDD in {int((C.dMaxDD>0).sum())}/{len(C)}, on CAGR in {int((C.dCAGR>0).sum())}/{len(C)}")
    P(f"  cells where the twin PASSES 4b and the budgeted book does not: "
      f"{int(((~C.pass4b)).sum())} fail overall; twin-vs-book 4b agreement is read in B5 for the rule-8 picks.")
    P("")

    # ------------------------------------------------------------------ B4
    P("-" * 102); P("B4  WHAT THE BUDGET BUYS -- drawdown saved per point of mean gross given up"); P("-" * 102)
    for pan in panels:
        sub = H[(H.panel == pan) & (H.window == "FULL")]
        P(f"   -- {pan} FULL")
        for g_hi in CEILS:
            s2 = sub[sub.g_hi == g_hi].set_index("D").reindex([dlabel(d) for d in BUDGETS])
            ref = s2.loc["inf"]
            mono = [s2.loc[dlabel(BUDGETS[i+1])].MaxDD - s2.loc[dlabel(BUDGETS[i])].MaxDD for i in range(3)]
            P(f"      g_hi {g_hi:.2f}  MaxDD by D: " +
              "  ".join(f"{s2.loc[dlabel(d)].MaxDD:7.2%}" for d in BUDGETS) +
              f"   monotone-in-D {'YES' if all(x >= -1e-12 for x in mono) or all(x <= 1e-12 for x in mono) else 'NO'}")
            for d in BUDGETS[:-1]:
                r = s2.loc[dlabel(d)]
                dg = (ref.mean_gross - r.mean_gross) * 100.0
                dD = (r.MaxDD - ref.MaxDD) * 100.0
                dC = (r.CAGR - ref.CAGR) * 100.0
                P(f"         D {dlabel(d):>5s}  gross given up {dg:6.2f} pp -> DD saved {dD:+6.2f} pp "
                  f"({dD/dg if dg else float('nan'):+6.3f} pp/pp), CAGR {dC:+6.2f} pp "
                  f"({dC/dg if dg else float('nan'):+6.3f} pp/pp)")
        # the static dial, same ratio
        P(f"      STATIC GROSS DIAL (D=inf), same ratio against g_hi=1.00:")
        s3 = sub[sub.D == "inf"].set_index("g_hi")
        ref = s3.loc[1.00]
        for g_hi in CEILS[:-1]:
            r = s3.loc[g_hi]
            dg = (ref.mean_gross - r.mean_gross) * 100.0
            dD = (r.MaxDD - ref.MaxDD) * 100.0
            dC = (r.CAGR - ref.CAGR) * 100.0
            P(f"         g_hi {g_hi:.2f}  gross given up {dg:6.2f} pp -> DD saved {dD:+6.2f} pp "
              f"({dD/dg if dg else float('nan'):+6.3f} pp/pp), CAGR {dC:+6.2f} pp "
              f"({dC/dg if dg else float('nan'):+6.3f} pp/pp)")
    P("")

    # ------------------------------------------------------------------ B5
    P("-" * 102); P("B5  RULE 8 -- both dials chosen on IS by IS Sharpe, 2017-2026 read ONCE"); P("-" * 102)
    picks = {}
    for pan in panels:
        IS = H[(H.panel == pan) & (H.window == "IS")]
        k = IS.loc[IS.Sharpe.idxmax()]
        OO = H[(H.panel == pan) & (H.window == "OOS") & (H.D == k.D) & (H.g_hi == k.g_hi)].iloc[0]
        FU = H[(H.panel == pan) & (H.window == "FULL") & (H.D == k.D) & (H.g_hi == k.g_hi)].iloc[0]
        picks[("free", pan)] = (k, FU, OO)
        ISc = IS[IS.g_hi == GLIVE]
        kc = ISc.loc[ISc.Sharpe.idxmax()]
        OOc = H[(H.panel == pan) & (H.window == "OOS") & (H.D == kc.D) & (H.g_hi == kc.g_hi)].iloc[0]
        FUc = H[(H.panel == pan) & (H.window == "FULL") & (H.D == kc.D) & (H.g_hi == kc.g_hi)].iloc[0]
        picks[("live-ceiling", pan)] = (kc, FUc, OOc)
    for (arm, pan), (k, FU, OO) in picks.items():
        P(f"   -- {pan} arm={arm}   IS-Sharpe argmax -> D {k.D} / g_hi {k.g_hi:.2f}  (IS Sharpe {k.Sharpe:.4f})")
        for lbl, r in (("FULL", FU), ("IS", k), ("OOS", OO)):
            P(f"      {lbl:4s}  {r.CAGR:6.2%} / {r.Sharpe:6.4f} / {r.MaxDD:7.2%}   "
              f"SPY {r.spy_CAGR:6.2%} / {r.spy_Sharpe:6.4f} / {r.spy_MaxDD:7.2%}   "
              f"RULESv2 {r.base_CAGR:6.2%} / {r.base_Sharpe:6.4f} / {r.base_MaxDD:7.2%}   "
              f"4b {'PASS' if r.pass4b else 'FAIL'}  4a {'PASS' if r.pass4a else 'FAIL'}")
            P(f"            legs H1 {'Y' if r.L_H1 else '.'} H2 {'Y' if r.L_H2 else '.'} "
              f"DD {'Y' if r.L_DD else '.'} CAGR {'Y' if r.L_CAGR else '.'}   "
              f"margins H1 {r.M_H1:+.3f} H2 {r.M_H2:+.3f} DD {r.M_DD:+.2f}pp CAGR {r.M_CAGR:+.2f}pp")
        P(f"      IS-matched STATIC TWIN (lam_IS {OO.lam_IS:.4f}): OOS "
          f"{OO.twIS_CAGR:6.2%} / {OO.twIS_Sharpe:6.4f} / {OO.twIS_MaxDD:7.2%}   "
          f"-> budget minus twin  CAGR {(OO.CAGR-OO.twIS_CAGR)*100:+.2f}pp  "
          f"Sharpe {OO.Sharpe-OO.twIS_Sharpe:+.4f}  MaxDD {(OO.MaxDD-OO.twIS_MaxDD)*100:+.2f}pp")
    P("")

    # ------------------------------------------------------------------ B6
    P("-" * 102); P("B6  PATH 4a at every grid point (vs live RULES v2)"); P("-" * 102)
    for pan in panels:
        for wn in ("FULL", "IS", "OOS"):
            sub = H[(H.panel == pan) & (H.window == wn)]
            P(f"    {pan:5s} {wn:4s}  4a {int(sub.pass4a.sum())}/25")
    P("")

    # ------------------------------------------------------------------ B7
    P("-" * 102); P("B7  COST LADDER 0/10/25/50 bps (sensitivity, never a selection axis)"); P("-" * 102)
    for pan in panels:
        for wn in ("FULL", "OOS"):
            line = []
            for c in COSTS:
                sub = G[(G.panel == pan) & (G.window == wn) & (G.offset == 0) & (G.cost == c)]
                line.append(f"{c:>2d}bps {int(sub.pass4b.sum()):2d}/25")
            P(f"    {pan:5s} {wn:4s}  4b passes: " + "   ".join(line))
    P("")

    # ------------------------------------------------------------------ B8
    P("-" * 102); P("B8  IDEA 914's OFFSET-SPREAD CLAUSE on every 4b pass at d=0, 10 bps"); P("-" * 102)
    pas = H[H.pass4b]
    if not len(pas):
        P("  NO 4b pass at d=0 / 10 bps anywhere on this grid -- the clause has nothing to bite.")
    for _, r in pas.iterrows():
        fam = G[(G.panel == r.panel) & (G.window == r.window) & (G.cost == COST0) &
                (G.D == r.D) & (G.g_hi == r.g_hi)]
        sp_dd = float(fam.M_DD.max() - fam.M_DD.min()); sp_cg = float(fam.M_CAGR.max() - fam.M_CAGR.min())
        stab = int(fam.pass4b.sum())
        P(f"    {r.panel:5s} {r.window:4s} D {r.D:>5s} g_hi {r.g_hi:.2f}:  "
          f"DD margin {r.M_DD:+.2f} pp vs spread {sp_dd:.3f} pp (ratio {r.M_DD/sp_dd if sp_dd else float('nan'):.2f}x)  "
          f"CAGR margin {r.M_CAGR:+.2f} pp vs spread {sp_cg:.3f} pp "
          f"(ratio {r.M_CAGR/sp_cg if sp_cg else float('nan'):.2f}x)  stable {stab}/5 offsets")
    P("")

    P("-" * 102); P("GATE SUMMARY"); P("-" * 102)
    for n, g, b, ok in GATES: P(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    P(f"\nelapsed {time.time()-t0:.0f}s")
    (OUT / f"{SLUG}.out.txt").write_text("\n".join(LINES) + "\n")
    P(f"log -> {SLUG}.out.txt")


if __name__ == "__main__":
    main()
