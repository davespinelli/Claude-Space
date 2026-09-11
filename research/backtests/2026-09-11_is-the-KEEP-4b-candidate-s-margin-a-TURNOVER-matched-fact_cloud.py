#!/usr/bin/env python3
"""
IDEA 678 -- is-the-KEEP-4b-candidate-s-margin-a-TURNOVER-matched-fact
=====================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 502 found the record has no turnover-matched null: its fixed-list null trades 3.20x/yr
  and its gross-matched rotating null 36.48x/yr, bracketing the candidate's 9.64x, and the
  candidate's entire 10 bps separation from a gross-matched coin flip is that gap (0/1000 pass
  at 10 bps, 781/1000 at 0 bps).  Build a coin flip that re-draws at the candidate's OWN
  turnover (hold each random name a geometric number of weeks calibrated to 9.64x/yr) and
  re-measure the 4b share and the candidate's percentile at 0/10/25 bps.
  Max 2 params (turnover target, cost rung).

WHY IT MATTERS FOR CAPITAL
--------------------------
  Idea 502 left the standing 2026-09-04 KEEP-4b candidate in an awkward place: it clears a bar
  that 0 of 1,000 coin flips clear at 10 bps, but at 0 bps 78.1% of gross-matched coin flips
  clear the same bar and the candidate sits at their 78.2nd percentile.  Both of 502's nulls
  differ from the candidate in TWO ways at once (which names, and how often the list turns
  over), so the 10 bps separation could be entirely the cost of the nulls' trading and not
  a property of the rule.  A null that matches the candidate's turnover isolates SELECTION.
  If the candidate still sits inside a turnover-matched null, the KEEP is a statement about a
  family of 20-name gated books, not about the composite, and no capital should follow it on
  the strength of the ranking.

THE NULL (RANDGEO): a coin flip with the candidate's own holding period
----------------------------------------------------------------------
  RANDGEO(p)  a book of up to 20 names, each weighted at exactly 0.75/20 (the candidate's own
              convention, de-grossing to cash below 20 eligible names), where at every weekly
              rebalance each held name
                 * is FORCED out if it left the eligible set (above the 200d MA, vol20 < 0.60)
                   -- the candidate can never hold an ineligible name either, so the null must
                   not be allowed to;
                 * otherwise leaves VOLUNTARILY with probability p,
              and the vacated slots are refilled uniformly at random from the eligible names
              not currently held.  Holding period is geometric with mean 1/p weeks, truncated
              by ineligibility.  p is the turnover dial: p -> 0 is 502's RANDFIX in its gated
              form (forced exits only) and p = 1 is exactly 502's RANDROT (a fresh random 20
              every week).  The candidate differs from RANDGEO(p*) in ONE way only: which of
              the eligible names it holds.

  CALIBRATION (pre-registered, outcome-blind): p is solved by bisection on log p so that the
  null's MEDIAN realised annualised turnover over 40 PILOT seeds equals the target.  Pilot
  seeds (base 678000) are DISJOINT from the evaluation seeds (base 678), so no evaluation book
  is used to choose p.  Turnover is the engine's own turnover (|target - drifted| summed on
  rebalance rows), the same number the cost rungs are charged on.

DESIGN
------
  CANDIDATE  the standing 2026-09-04 KEEP-4b book, pinned in code: composite score with NO vol
             scaler, top 20 eligible names, FIXED 0.75/20 per name, de-gross to cash below 20,
             vol20 cap 0.60, weekly cadence.  Identical to idea 502's G3 book.
  TUNED (2)  TURNOVER TARGET, as a multiple of the candidate's OWN realised turnover on that
             panel: {0.5x, 1.0x, 2.0x, 4.0x} (1.0x is the queue's ask), plus the two
             UNCALIBRATED reference rungs p=0 (forced exits only) and p=1 (= 502's RANDROT)
             reported beside them; and COST RUNG {0, 10, 25} bps.  Every point of the grid is
             reported.
  FIXED      n = 20, gross 0.75, the gate, cadence W, warm-up 260 rows, IS/OOS split
             2016-12-31 / 2017-01-01 (PROTOCOL rule 8), seed base 678.  Draws: 1,000 on the
             binding panel U56, 250 on the two replication panels (draws is NOT a tuned axis
             here -- idea 502 already showed the pass share is flat in draws from 250 to 1,000).
  PANELS     U56 is BINDING (the candidate's own panel, the one the queue names).  B136 and
             SMALL439 are run identically as a labelled replication; no verdict is taken from
             them and they are not a third tuned axis.

  PERCENTILE convention (same as idea 502): the candidate's percentile is the share of null
             books it BEATS (Sharpe/CAGR: null < candidate; MaxDD: |null| > |candidate|).

  RULE 8 (PROTOCOL 8, required): the turnover target is chosen on 2009-2016 ONLY, by the
             pre-registered MATCHING criterion (the rung whose median IS turnover is closest to
             the candidate's IS turnover), with p re-calibrated on IS data alone; 2017-2026 is
             then read once.  OOS CAGR/Sharpe/MaxDD are reported for the candidate, the null
             median, RULES v2 and SPY, together with the null's OOS 4b pass share.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  ctx.run == engine.backtest @10 bps on a dense book                          bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          bar 0.0
  G3  the standing 2026-09-04 KEEP-4b incumbent re-derived on the FULL U56 panel:
      published 12.66% / 1.0921 / -18.31%                                         bar 5e-3
  G4  every null book holds <= 20 names at exactly 0.75/20, gross == 0.75 x held/20  bar 1e-12
  G5  the cost rungs are one gross stream minus turnover x c/1e4                   bar 1e-15
  G6  the draws are reproducible: re-running seed 678+0 reproduces its book exactly
  G7  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G8  RANDGEO(p=1) reproduces idea 502's committed RANDROT: median gross 0.7195 (bar 0.01)
      and median annual turnover 36.48x (bar 1.5x)
  G9  turnover(p) is monotone increasing over the calibration ladder -- the bisection's
      own precondition, checked rather than assumed

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  B136 is today's constituents; SMALL439 is the current sub-$2B screen only (see
  data/SMALL_PANEL_README.md).  Names acquired, delisted or grown out of the screen are absent,
  so every LEVEL on those panels is biased upward.  The direction that matters here: a random
  list drawn from a survivor panel is a BETTER book than a random list drawn in real time would
  have been, so the null's pass share is an UPPER bound on the true coin-flip base rate and the
  candidate's percentile inside it is a LOWER bound -- the bias favours the queue's suspicion,
  not the incumbent.  U56 carries the same bias in milder form.
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

COSTS = [0.0, 10.0, 25.0]                 # TUNED axis 2
TURN_MULT = [0.5, 1.0, 2.0, 4.0]          # TUNED axis 1 (x the candidate's own turnover)
FREQ = "W"
BAND0, GROSS0 = 0.03, 0.75
NCAND = 20
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED0, PILOT_SEED0, N_PILOT = 678, 678000, 40
DRAWS = {"U56": 1000, "B136": 250, "SMALL439": 250}
BINDING_PANEL, BINDING_COST = "U56", 10.0
KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)
RANDROT_502 = dict(gross=0.7195, turnover=36.48)     # idea 502's committed RANDROT, U56

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ------------------------------------------------------------------------------------------
class Ctx:
    """Weights-independent part of the return calculation, hoisted out of the draw loop
    (construction follows idea 502's Ctx; G1 re-verifies it against engine.backtest here).
    ctx.run(W) -> (gross return stream, turnover stream); cost rungs are applied afterwards."""

    def __init__(self, px, freq=FREQ):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = rebalance_mask(self.idx, freq).values
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]

    def run(self, weights):
        wt = self.shift(weights) if isinstance(weights, pd.DataFrame) else weights
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values


def M0(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def ranked_w(sc, elig, n, gross):
    r = sc.where(elig).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def keeppaths(m, oos_s, mb, ms, spy_oos):
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > spy_oos)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b)


def fail4b(m, oos_s, ms, spy_oos):
    f = []
    if not m["H1"] > ms["H1"]: f.append("H1")
    if not m["H2"] > ms["H2"]: f.append("H2")
    if not oos_s > spy_oos: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return "+".join(f) if f else "-"


# ------------------------------------------------------------------------------------------
def load_panels():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL439"] = sm[keep]
    return panels, len(sm.columns) - len(keep)


def randgeo_sel(px, elig, ctx, p, seeds, i_stop=None):
    """The RANDGEO(p) name chain, vectorized across draws.

    Returns (reb, sel) with sel of shape (n_reb, D, 20) holding column indices (-1 = empty
    slot).  The chain is advanced on the rebalance rows; each row's holdings are decided at the
    previous close (`dec`), which is exactly the row `ctx.run` reads on `ctx.reb`.  i_stop
    truncates the chain (used by rule 8's IS-only calibration) without touching the seeds.

    At each rebalance: a held name is FORCED out if it is no longer eligible, otherwise leaves
    with probability p; the vacated slots are refilled uniformly from the eligible names not
    currently held.  The number of names held is min(20, n_eligible) for every draw, so the
    selection is a top-k over one key matrix: kept names get key 2.0 (always in), eligible-free
    names an independent uniform key, ineligible names -1.
    """
    D = len(seeds)
    reb = ctx.reb if i_stop is None else ctx.reb[ctx.reb <= i_stop]
    dec = np.maximum(reb - 1, 0)
    ev = elig.values.copy()
    ev[:, [i for i, c in enumerate(px.columns) if c == "SPY"]] = False   # SPY never held
    N = ev.shape[1]
    rng = np.random.default_rng([int(s) for s in seeds])
    sel = np.full((len(reb), D, NCAND), -1, dtype=np.int32)
    cur = np.full((D, NCAND), -1, dtype=np.int32)
    rowi = np.repeat(np.arange(D), NCAND).reshape(D, NCAND)
    for i, d in enumerate(dec):
        E = ev[d]
        k = min(NCAND, int(E.sum()))
        if k == 0:
            cur = np.full((D, NCAND), -1, dtype=np.int32)
            continue
        filled = cur >= 0
        ok = np.zeros_like(filled)
        ok[filled] = E[cur[filled]]
        stay = ok & (rng.random(cur.shape) >= p)
        R = rng.random((D, N))
        R[:, ~E] = -1.0
        R[rowi[stay], cur[stay]] = 2.0                    # kept names are guaranteed top-k
        top = np.argpartition(-R, k - 1, axis=1)[:, :k]
        cur = np.full((D, NCAND), -1, dtype=np.int32)
        cur[:, :k] = top
        sel[i] = cur
    return reb, sel


def book_from_sel(s, reb, T, N):
    """One draw's (T, N) SHIFTED weight array from its (n_reb, 20) selection."""
    wt = np.zeros((T, N))
    flat = s.ravel()
    m = flat >= 0
    wt[np.repeat(reb, NCAND)[m], flat[m]] = GROSS0 / NCAND
    return wt


def streams(px, elig, ctx, p, seeds, i_stop=None):
    """(gross return, turnover, mean rebalance-row gross) per draw for RANDGEO(p).  One gross
    stream per book; the cost rungs are subtracted from it afterwards (G5)."""
    reb, sel = randgeo_sel(px, elig, ctx, p, seeds, i_stop)
    T, N = ctx.T, ctx.N
    out = []
    for dd in range(len(seeds)):
        wt = book_from_sel(sel[:, dd, :], reb, T, N)
        g, tn = ctx.run(wt)
        out.append((g, tn, wt))
    return out


def calibrate_p(px, elig, ctx, target, i0, i_stop=None, lo=1e-4, hi=1.0, iters=12):
    """Bisection on log p so the null's MEDIAN pilot turnover == target.  Pilot seeds are
    disjoint from the evaluation seeds, so no evaluated book helps choose p."""
    seeds = [PILOT_SEED0 + i for i in range(N_PILOT)]
    hi_row = ctx.T if i_stop is None else i_stop
    yrs = (hi_row - i0) / 252.0

    def f(p):
        st = streams(px, elig, ctx, p, seeds, i_stop)
        return float(np.median([tn[i0:hi_row].sum() / yrs for _, tn, _ in st]))

    tlo, thi = f(lo), f(hi)
    if target <= tlo: return lo, tlo, 0
    if target >= thi: return hi, thi, 0
    a, b = np.log(lo), np.log(hi)
    for _ in range(iters):
        mid = 0.5 * (a + b)
        if f(np.exp(mid)) < target: a = mid
        else: b = mid
    p = float(np.exp(0.5 * (a + b)))
    return p, f(p), iters


# ------------------------------------------------------------------------------------------
def gates(panels, n_dropped):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]
    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights            : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= g2 == 0.0

    ctx = Ctx(px)
    gr, turn = ctx.run(w)
    fast = pd.Series(gr - turn * 10.0 / 1e4, index=px.index)
    slow = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"]
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 ctx.run == engine.backtest @10 bps                  : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    cand = ranked_w(sc, elig, NCAND, GROSS0)
    gr_c, turn_c = ctx.run(cand)
    m = M(pd.Series(gr_c - turn_c * 10.0 / 1e4, index=px.index).loc[j:])
    d = {k: abs(m[k] - v) for k, v in KEEP4B_INCUMBENT.items()}
    P("  G3 2026-09-04 KEEP-4b incumbent (U56 top-20 EW, no vol scaler) re-derived:")
    P(f"     got {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   published "
      f"{KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {max(d.values()):.3e}  "
      f"{'PASS' if max(d.values()) < 5e-3 else 'FAIL'}")
    ok &= max(d.values()) < 5e-3

    seeds3 = [SEED0 + i for i in range(3)]
    bk = [wt for _, _, wt in streams(px, elig, ctx, 0.2, seeds3)]
    g4 = True
    for wt in bk:
        held = (wt > 0).sum(axis=1)
        wmax = float(np.abs(wt[wt > 0] - GROSS0 / NCAND).max())
        gerr = float(np.abs(wt.sum(axis=1) - GROSS0 / NCAND * held).max())
        g4 &= (held.max() <= NCAND) and wmax < 1e-15 and gerr < 1e-12
    P(f"  G4 null books: max names {max((wt>0).sum(axis=1).max() for wt in bk)} (<= {NCAND}), "
      f"per-name weight dev {max(float(np.abs(wt[wt>0]-GROSS0/NCAND).max()) for wt in bk):.3e}, "
      f"gross == 0.75 x held/20  {'PASS' if g4 else 'FAIL'}")
    ok &= g4

    r0 = pd.Series(gr_c, index=px.index)
    r10 = pd.Series(gr_c - turn_c * 10.0 / 1e4, index=px.index)
    g5 = float(np.abs((r0 - r10) - turn_c * 10.0 / 1e4).max())
    P(f"  G5 cost rungs are ONE gross stream minus turnover x c   : {g5:.3e}  "
      f"{'PASS' if g5 < 1e-15 else 'FAIL'}")
    ok &= g5 < 1e-15

    bk2 = [wt for _, _, wt in streams(px, elig, ctx, 0.2, seeds3)]
    g6 = max(float(np.abs(a - b).max()) for a, b in zip(bk, bk2))
    P(f"  G6 draws reproducible (seed {SEED0} re-run)               : {g6:.3e}  "
      f"{'PASS' if g6 == 0.0 else 'FAIL'}")
    ok &= g6 == 0.0

    i0 = WARM
    yrs = (ctx.T - i0) / 252.0
    rebi = ctx.reb[ctx.reb >= i0]
    rot = streams(px, elig, ctx, 1.0, [SEED0 + i for i in range(60)])
    gmed = float(np.median([wt[rebi].sum(axis=1).mean() for _, _, wt in rot]))
    tmed = float(np.median([tn[i0:].sum() / yrs for _, tn, _ in rot]))
    g8 = abs(gmed - RANDROT_502["gross"]) < 0.01 and abs(tmed - RANDROT_502["turnover"]) < 1.5
    P(f"  G8 RANDGEO(p=1) == idea 502's RANDROT: gross {gmed:.4f} (pub "
      f"{RANDROT_502['gross']:.4f}), turnover {tmed:.2f}x (pub {RANDROT_502['turnover']:.2f}x)  "
      f"{'PASS' if g8 else 'FAIL'}")
    ok &= g8

    ladder = [(p, float(np.median([tn[i0:].sum() / yrs for _, tn, _ in
                                   streams(px, elig, ctx, p, [PILOT_SEED0 + i for i in range(12)])])))
              for p in (0.0, 0.02, 0.05, 0.15, 0.4, 1.0)]
    mono = all(ladder[i][1] < ladder[i + 1][1] for i in range(len(ladder) - 1))
    P("  G9 turnover(p) monotone: " + "  ".join(f"p={p:.2f}->{t:.2f}x" for p, t in ladder)
      + f"   {'PASS' if mono else 'FAIL'}")
    ok &= mono

    P(f"  G7 SMALL439 dropped {n_dropped} tickers with max_1d_move >= 1.0 : "
      f"{'PASS' if n_dropped > 0 else 'FAIL'}")
    ok &= n_dropped > 0
    P()
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- results below are not trustworthy'}")
    return ok


# ------------------------------------------------------------------------------------------
def comparands(px, ctx, i0, cost):
    """(RULES v2 metrics, SPY metrics, SPY OOS Sharpe, v2 OOS Sharpe) at one cost rung."""
    gr, turn = ctx.run(band_book(px, BAND0, GROSS0))
    b = pd.Series(gr - turn * cost / 1e4, index=px.index).iloc[i0:]
    spy = px["SPY"].pct_change().fillna(0.0).iloc[i0:]
    return M(b), M(spy), M0(spy.loc[OOS_START:]), M0(b.loc[OOS_START:]), b, spy


def panel_setup(name, px):
    ctx = Ctx(px)
    i0 = WARM
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    cand_w = ranked_w(sc, elig, NCAND, GROSS0)
    gr_c, turn_c = ctx.run(cand_w)
    yrs = (ctx.T - i0) / 252.0
    i_is = int(np.searchsorted(px.index, pd.Timestamp(IS_END)))
    d = dict(ctx=ctx, i0=i0, elig=elig, cand_w=cand_w, gr_c=gr_c, turn_c=turn_c, yrs=yrs,
             i_is=i_is, reb_i=ctx.reb[ctx.reb >= i0],
             cand_turn=float(turn_c[i0:].sum() / yrs),
             cand_turn_is=float(turn_c[i0:i_is].sum() / ((i_is - i0) / 252.0)),
             cand_gross=float(cand_w.values[ctx.reb[ctx.reb >= i0]].sum(axis=1).mean()),
             n_elig=float(elig.iloc[i0:].sum(axis=1).mean()))
    return d


def run_panel(name, px, S):
    """The turnover ladder x cost grid on one panel.  Each null is built ONCE and its single
    gross return stream is charged at all three cost rungs (G5), so the rungs differ by cost
    and by nothing else."""
    P()
    P("=" * 100)
    P(f"(B) PANEL {name}  ({px.shape[1]} columns, {px.index[0].date()} -> {px.index[-1].date()})"
      f"   draws = {DRAWS[name]}")
    P("=" * 100)
    ctx, i0, elig, yrs = S["ctx"], S["i0"], S["elig"], S["yrs"]
    P(f"  candidate realised turnover {S['cand_turn']:.2f}x/yr (IS {S['cand_turn_is']:.2f}x/yr), "
      f"mean gross {S['cand_gross']:.4f}, mean eligible names {S['n_elig']:.1f}")

    rungs = []
    for mlt in TURN_MULT:
        tgt = mlt * S["cand_turn"]
        p, got, it = calibrate_p(px, elig, ctx, tgt, i0)
        rungs.append(dict(rung=f"{mlt:g}x", p=p, target=tgt, pilot=got, iters=it))
        P(f"  calibrated {mlt:g}x: target {tgt:6.2f}x/yr -> p = {p:.4f}  "
          f"(pilot median {got:6.2f}x/yr, {it} bisection steps)")
    rungs.append(dict(rung="p=0 (forced only)", p=0.0, target=np.nan, pilot=np.nan, iters=0))
    rungs.append(dict(rung="p=1 (502 RANDROT)", p=1.0, target=np.nan, pilot=np.nan, iters=0))

    seeds = [SEED0 + i for i in range(DRAWS[name])]
    comp = {c: comparands(px, ctx, i0, c) for c in COSTS}
    cand = {}
    for c in COSTS:
        mb, ms, spy_oos, v2_oos, b_ret, spy_ret = comp[c]
        rc = pd.Series(S["gr_c"] - S["turn_c"] * c / 1e4, index=px.index).iloc[i0:]
        mc, mco = M(rc), M(rc.loc[OOS_START:])
        cand[c] = (mc, mco) + keeppaths(mc, mco["Sharpe"], mb, ms, spy_oos)
        P()
        P(f"  --- cost {c:.0f} bps ---")
        P(f"  CANDIDATE   {mc['CAGR']:7.2%} / {mc['Sharpe']:6.4f} / {mc['MaxDD']:7.2%}   "
          f"H1 {mc['H1']:.4f} H2 {mc['H2']:.4f}  OOS S {mco['Sharpe']:.4f}  "
          f"4a {'PASS' if cand[c][2] else 'fail'} 4b {'PASS' if cand[c][3] else 'fail'} "
          f"[{fail4b(mc, mco['Sharpe'], ms, spy_oos)}]")
        P(f"  RULES v2    {mb['CAGR']:7.2%} / {mb['Sharpe']:6.4f} / {mb['MaxDD']:7.2%}   "
          f"H1 {mb['H1']:.4f} H2 {mb['H2']:.4f}  OOS S {v2_oos:.4f}")
        P(f"  SPY         {ms['CAGR']:7.2%} / {ms['Sharpe']:6.4f} / {ms['MaxDD']:7.2%}   "
          f"H1 {ms['H1']:.4f} H2 {ms['H2']:.4f}  OOS S {spy_oos:.4f}")

    rows, drows = [], []
    for rg in rungs:
        st = streams(px, elig, ctx, rg["p"], seeds)
        turn_yr = np.array([tn[i0:].sum() / yrs for _, tn, _ in st])
        gross = np.array([wt[S["reb_i"]].sum(axis=1).mean() for _, _, wt in st])
        P()
        P(f"  {rg['rung']:>18s} p={rg['p']:.4f}  turnover median {np.median(turn_yr):6.2f}x/yr "
          f"(candidate {S['cand_turn']:.2f}x)  gross median {np.median(gross):.4f} "
          f"(candidate {S['cand_gross']:.4f})")
        for c in COSTS:
            mb, ms, spy_oos, v2_oos, _, _ = comp[c]
            mc, mco, c4a, c4b = cand[c]
            Sh, Cg, Dd, OS, H1, H2, F = [], [], [], [], [], [], []
            n4a = n4b = 0
            for g, tn, _ in st:
                r = pd.Series(g - tn * c / 1e4, index=px.index).iloc[i0:]
                m = M(r); os_ = M0(r.loc[OOS_START:])
                a, bb = keeppaths(m, os_, mb, ms, spy_oos)
                n4a += a; n4b += bb
                Sh.append(m["Sharpe"]); Cg.append(m["CAGR"]); Dd.append(m["MaxDD"])
                OS.append(os_); H1.append(m["H1"]); H2.append(m["H2"])
                F.append(fail4b(m, os_, ms, spy_oos))
            Sh, Cg, Dd, OS = map(np.array, (Sh, Cg, Dd, OS))
            nd = len(st)
            pS = float((Sh < mc["Sharpe"]).mean()); pC = float((Cg < mc["CAGR"]).mean())
            pD = float((np.abs(Dd) > abs(mc["MaxDD"])).mean())
            pO = float((OS < mco["Sharpe"]).mean())
            vc = pd.Series(F).value_counts()
            rows.append(dict(panel=name, rung=rg["rung"], p=rg["p"], cost=c, draws=nd,
                             null_turn_med=float(np.median(turn_yr)),
                             null_gross_med=float(np.median(gross)),
                             cand_turn=S["cand_turn"], cand_gross=S["cand_gross"],
                             pass4b=n4b, pass4a=n4a, share4b=n4b / nd, share4a=n4a / nd,
                             null_S_med=float(np.median(Sh)), null_C_med=float(np.median(Cg)),
                             null_D_med=float(np.median(Dd)), null_OOS_med=float(np.median(OS)),
                             null_S_p95=float(np.percentile(Sh, 95)),
                             cand_S=mc["Sharpe"], cand_C=mc["CAGR"], cand_D=mc["MaxDD"],
                             cand_OOS=mco["Sharpe"], cand_4a=c4a, cand_4b=c4b,
                             pctile_S=pS, pctile_C=pC, pctile_D=pD, pctile_OOS=pO,
                             top_fail=vc.index[0], top_fail_share=float(vc.iloc[0] / nd)))
            P(f"     cost {c:4.0f} bps  4b {n4b:4d}/{nd} ({n4b/nd:6.1%})  4a {n4a:4d}  "
              f"medS {np.median(Sh):6.4f} (cand {mc['Sharpe']:6.4f})  pctile S {pS:6.1%} "
              f"C {pC:6.1%} DD {pD:6.1%} OOS {pO:6.1%}  topfail {vc.index[0]} "
              f"({vc.iloc[0]/nd:.0%})")
            if c == BINDING_COST:
                for k in range(nd):
                    drows.append(dict(panel=name, rung=rg["rung"], seed=seeds[k], cost=c,
                                      Sharpe=Sh[k], CAGR=Cg[k], MaxDD=Dd[k], OOS=OS[k],
                                      H1=H1[k], H2=H2[k], turn=turn_yr[k], gross=gross[k],
                                      fail4b=F[k]))
        del st
    return pd.DataFrame(rows), pd.DataFrame(drows)


def walk_forward(name, px, S):
    """PROTOCOL 8: the turnover target is chosen on 2009-2016 ONLY, by the pre-registered
    MATCHING criterion (the rung whose median IS turnover is closest to the candidate's own IS
    turnover), with p re-calibrated on IS data alone.  The criterion reads no return and no
    cost, so the pick is one rung for all three cost rungs; 2017-2026 is then read once."""
    P()
    P("-" * 100)
    P(f"(C) RULE 8 WALK-FORWARD -- {name}: rung chosen on IS (<= {IS_END}), OOS read once")
    P("-" * 100)
    ctx, i0, elig, i_is = S["ctx"], S["i0"], S["elig"], S["i_is"]
    picks = []
    for mlt in TURN_MULT:
        p, got, _ = calibrate_p(px, elig, ctx, mlt * S["cand_turn_is"], i0, i_stop=i_is)
        picks.append((mlt, p, got, abs(got - S["cand_turn_is"])))
    mlt, p, got, gap = min(picks, key=lambda t: t[3])
    P(f"  IS candidate turnover {S['cand_turn_is']:.2f}x/yr; IS-calibrated rungs "
      + ", ".join(f"{m:g}x->{g:.2f}x" for m, _, g, _ in picks)
      + f"  => PICK {mlt:g}x (p={p:.4f}, IS null turnover {got:.2f}x, gap {gap:.2f}x)")
    seeds = [SEED0 + i for i in range(DRAWS[name])]
    st = streams(px, elig, ctx, p, seeds)
    out = []
    for c in COSTS:
        mb, ms, spy_oos, v2_oos, b_ret, spy_ret = comparands(px, ctx, i0, c)
        rc = pd.Series(S["gr_c"] - S["turn_c"] * c / 1e4, index=px.index)
        mci, mco = M(rc.iloc[i0:i_is]), M(rc.loc[OOS_START:])
        mbo, mso = M(b_ret.loc[OOS_START:]), M(spy_ret.loc[OOS_START:])
        Sh, Cg, Dd, n4b, ISh = [], [], [], 0, []
        for g, tn, _ in st:
            r = pd.Series(g - tn * c / 1e4, index=px.index)
            mf = M(r.iloc[i0:]); mo = M(r.loc[OOS_START:])
            a, bb = keeppaths(mf, mo["Sharpe"], mb, ms, spy_oos)
            n4b += bb
            Sh.append(mo["Sharpe"]); Cg.append(mo["CAGR"]); Dd.append(mo["MaxDD"])
            ISh.append(M0(r.iloc[i0:i_is]))
        Sh, Cg, Dd = map(np.array, (Sh, Cg, Dd))
        P(f"  cost {c:.0f} bps  OOS  CANDIDATE {mco['CAGR']:7.2%} / {mco['Sharpe']:6.4f} / "
          f"{mco['MaxDD']:7.2%}   (IS Sharpe {mci['Sharpe']:.4f})")
        P(f"                NULL med {np.median(Cg):7.2%} / {np.median(Sh):6.4f} / "
          f"{np.median(Dd):7.2%}   RULES v2 {mbo['CAGR']:7.2%} / {mbo['Sharpe']:6.4f} / "
          f"{mbo['MaxDD']:7.2%}   SPY {mso['CAGR']:7.2%} / {mso['Sharpe']:6.4f} / "
          f"{mso['MaxDD']:7.2%}")
        P(f"                candidate OOS percentile inside the picked null: Sharpe "
          f"{(Sh < mco['Sharpe']).mean():.1%}  CAGR {(Cg < mco['CAGR']).mean():.1%}  MaxDD "
          f"{(np.abs(Dd) > abs(mco['MaxDD'])).mean():.1%}   null 4b passes {n4b}/{len(st)}")
        out.append(dict(panel=name, cost=c, pick=f"{mlt:g}x", p=p, is_turn_null=got,
                        is_turn_cand=S["cand_turn_is"], cand_IS_S=mci["Sharpe"],
                        null_IS_S_med=float(np.median(ISh)),
                        cand_OOS_CAGR=mco["CAGR"], cand_OOS_S=mco["Sharpe"],
                        cand_OOS_DD=mco["MaxDD"], null_OOS_CAGR_med=float(np.median(Cg)),
                        null_OOS_S_med=float(np.median(Sh)), null_OOS_DD_med=float(np.median(Dd)),
                        null_OOS_S_p95=float(np.percentile(Sh, 95)),
                        v2_OOS_CAGR=mbo["CAGR"], v2_OOS_S=mbo["Sharpe"], v2_OOS_DD=mbo["MaxDD"],
                        spy_OOS_CAGR=mso["CAGR"], spy_OOS_S=mso["Sharpe"], spy_OOS_DD=mso["MaxDD"],
                        pct_OOS_S=float((Sh < mco["Sharpe"]).mean()),
                        pct_OOS_CAGR=float((Cg < mco["CAGR"]).mean()),
                        pct_OOS_DD=float((np.abs(Dd) > abs(mco["MaxDD"])).mean()),
                        null_4b=n4b, draws=len(st)))
    return pd.DataFrame(out)


def main():
    panels, n_dropped = load_panels()
    ok = gates(panels, n_dropped)
    grid, draws_all, wf = [], [], []
    for nm in ["U56", "B136", "SMALL439"]:
        S = panel_setup(nm, panels[nm])
        g, d = run_panel(nm, panels[nm], S)
        grid.append(g); draws_all.append(d)
        wf.append(walk_forward(nm, panels[nm], S))
    grid = pd.concat(grid, ignore_index=True)
    draws_all = pd.concat(draws_all, ignore_index=True)
    wf = pd.concat(wf, ignore_index=True)

    P()
    P("=" * 100)
    P("(D) THE ANSWER -- binding cell: U56 (the candidate's panel), 1.0x turnover, 10 bps")
    P("=" * 100)
    b = grid[(grid.panel == BINDING_PANEL) & (grid.cost == BINDING_COST)]
    for _, r in b.iterrows():
        P(f"  {r['rung']:>20s}  null turn {r['null_turn_med']:6.2f}x vs candidate "
          f"{r['cand_turn']:5.2f}x  |  4b {r['pass4b']:4d}/{r['draws']} ({r['share4b']:6.1%})  "
          f"|  candidate percentile: Sharpe {r['pctile_S']:6.1%}  CAGR {r['pctile_C']:6.1%}  "
          f"MaxDD {r['pctile_D']:6.1%}  OOS {r['pctile_OOS']:6.1%}")
    P()
    P("  4b pass share across the full grid (rows = turnover rung, cols = cost rung):")
    for nm in ["U56", "B136", "SMALL439"]:
        P(f"    {nm}")
        pv = grid[grid.panel == nm].pivot_table(index="rung", columns="cost", values="share4b")
        for line in pv.to_string(float_format=lambda x: f"{x:.3f}").split("\n"):
            P("      " + line)
    P()
    P("  candidate Sharpe percentile inside each null (rows = rung, cols = cost):")
    for nm in ["U56", "B136", "SMALL439"]:
        P(f"    {nm}")
        pv = grid[grid.panel == nm].pivot_table(index="rung", columns="cost", values="pctile_S")
        for line in pv.to_string(float_format=lambda x: f"{x:.3f}").split("\n"):
            P("      " + line)

    dump(grid, "grid")
    dump(draws_all, "draws")
    dump(wf, "walkforward")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"  wrote {STEM}.console.txt")
    return ok


if __name__ == "__main__":
    main()
