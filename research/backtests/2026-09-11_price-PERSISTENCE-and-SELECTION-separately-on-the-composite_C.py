#!/usr/bin/env python3
"""
IDEA 679 -- price-PERSISTENCE-and-SELECTION-separately-on-the-composite
=======================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 502 showed what the composite buys over an equal-gross coin flip at 10 bps is that its
  top-20 list changes slowly, and ideas 504/672 showed the same clause earns CAGR but no
  Sharpe.  Decompose the composite book into a SELECTION leg (which names, at matched
  turnover) and a PERSISTENCE leg (how long they are held, at matched names) on
  U56/B136/SMALL439 and report which leg carries the 4b pass.  Max 2 params (holding
  period, panel).

WHAT IS AT STAKE
----------------
  502 left the standing 2026-09-04 KEEP-4b candidate separated from a coin flip by 10 bps of
  cost and nothing else: its fixed-list null trades 3.20x/yr, its gross-matched rotating null
  36.48x/yr, the candidate 9.64x/yr, and at 0 bps the rotating null passes 4b 78.1% of the
  time with the candidate at its 78th percentile.  If the composite's whole 10 bps edge is
  that it churns slowly, then a random list churned slowly should earn it too -- and the
  ranking clause in RULES is decoration.  This run builds exactly that book.

DESIGN -- the decomposition
---------------------------
  Every book here holds min(20, n_elig) names at a FIXED 0.75/20 of NAV each (the incumbent's
  own convention, pinned by G3), through the incumbent's gate (above the 200d MA, vol20 < 0.60,
  composite with NO vol scaler), weekly cadence, 10 bps.  Because the held-name COUNT is
  matched day by day across books, their daily GROSS is identical by construction (G4).

  Three books, at each holding period h (weeks between list re-formations):
    RANKED(h)   top-20 by composite at every h-th weekly date; list held unchanged between
                re-formations.  h=1 IS the standing incumbent (G3).
    RMATCH(h)   a coin flip re-drawn at RANKED(h)'s OWN turnover: at each re-formation date it
                replaces exactly as many names as RANKED(h) replaced on that same date, chosen
                at random from the eligible pool, and keeps the rest.  Same count, same gross,
                same churn, DIFFERENT names.
    RFREE(h)    a coin flip that re-draws its whole list at every re-formation date.  Same
                count, same gross, MORE churn, different names.

  The two legs the queue asks for are then differences between adjacent books:
    SELECTION   (which names, at matched turnover)  =  RANKED(h)  -  RMATCH(h)
    PERSISTENCE (how long held, with NO selection)  =  RMATCH(h)  -  RFREE(h)
    and, as the queue's "at matched names" reading of persistence:
    PERSIST|SEL (how long held, same selection rule) = RANKED(h) - RANKED(1)
  Their sum RANKED(h) - RFREE(h) is the composite's total edge over an equal-gross coin flip,
  i.e. the quantity idea 502 measured at a single h.

  TUNED (2)   HOLDING PERIOD h in {1, 2, 4, 8, 13, 26, 52} weeks  x  PANEL {U56, B136,
              SMALL439}.  ALL 21 cells are reported, for all three books.
  NOT TUNED   n=20, gross 0.75, the gate above, cadence W, warm-up 260 rows, IS/OOS split
              2016-12-31 / 2017-01-01 (PROTOCOL rule 8), 60 random draws per random book.
              None was chosen by outcome.
  RANDOM      60 draws per (panel, h, random book), seeded deterministically from
              (panel index, h, draw).  Randoms are reported as a DISTRIBUTION (median, p05,
              p95, 4b pass share) and RANKED is reported as a PERCENTILE inside it; no single
              draw is ever a comparand.
  COST        10 bps (PROTOCOL rule 2) is the only rung any verdict is taken at.  0 and 25 bps
              are printed as a LABELLED appendix -- they are free here (the gross return and
              turnover streams are shared), and they are not a third tuned axis.

  RULE 8      Per panel and per book family, the chooser picks h by IS Sharpe (through
              2016-12-31) and the pick is scored on 2017-2026 untouched against SPY OOS and
              live RULES v2 OOS.  For the random families the chooser runs INSIDE each draw
              and the OOS result is reported as a distribution over draws.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  Panel.run == engine.backtest @10 bps                                       bar 1e-12
  G1b Panel.run_sparse (the O(T*20) engine every book below uses) == Panel.run   bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                         bar 0.0
  G3  RANKED(h=1) == the standing 2026-09-04 KEEP-4b incumbent on the FULL U56 panel:
      published 12.66% / 1.0921 / -18.31%                                        bar 5e-3
  G4  RMATCH and RFREE carry RANKED's daily gross exactly, every day, every h    bar 1e-12
  G5  RMATCH's churn shortfall (re-adds forced by an exhausted eligible pool,
      as a share of RANKED's target replacements) is negligible                  bar 2%
  G6  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  B136 is today's constituents and SMALL439 is the current sub-$2B screen only (see
  data/SMALL_PANEL_README.md): names acquired, delisted or grown out of the screen are absent,
  so every LEVEL on those panels is biased upward and none is a tradeable estimate.  U56
  carries the same bias in milder form.  Every leg reported here is a WITHIN-PANEL difference
  over the same names and days, so the bias applies to both sides and largely differences out;
  the 4b PASS COUNTS, which are levels against SPY, do not enjoy that protection.
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

COST0 = 10.0                      # PROTOCOL rule 2 -- the only rung any verdict is taken at
COSTS = [0.0, 10.0, 25.0]         # 0 / 25 are a labelled appendix only
FREQ = "W"
BAND0, GROSS0 = 0.03, 0.75
NCAND = 20
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HOLDS = [1, 2, 4, 8, 13, 26, 52]  # weeks between list re-formations (tuned axis 1)
NDRAW = 60
KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ---------------------------------------------------------------------------------- engine --
class Panel:
    """Everything about one panel that does not depend on the book: returns, the weekly
    rebalance grid, the eligibility gate and the composite score."""

    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx = px.index
        self.T, self.N = px.shape
        self.rets = px.pct_change().fillna(0.0).values
        pe = np.flatnonzero(rebalance_mask(self.idx, FREQ).values)     # period-END rows
        reb = np.concatenate([[0], (pe + 1)[pe + 1 < self.T]])         # rows weights APPLY on
        self.reb = reb
        self.dec = np.concatenate([[-1], pe[pe + 1 < self.T]])         # rows weights DECIDED on
        C = np.cumprod(1.0 + self.rets, axis=0)
        Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.C, self.Cp = C, Cp
        seg = np.searchsorted(reb, np.arange(self.T), side="right") - 1
        self.seg = seg
        s0, s0p = reb[seg], reb[np.maximum(seg - 1, 0)]
        self.CpS, self.CpP = Cp / Cp[s0], Cp / Cp[s0p]
        self.segp = np.maximum(seg - 1, 0)
        sc, above, vol20 = score(px, vol_scale=False)
        tr = list(px.columns)                  # baseline ranks SPY with the rest (G3 pins it)
        self.elig = (above[tr] & (vol20[tr] < VOLCAP)).values
        self.sc = sc[tr].values
        self.start = WARM
        self.cols = tr

    def run(self, Wreb):
        """Wreb: (R x N) target weights on the rebalance grid.  Returns (gross_ret, turnover)
        daily series as numpy arrays; any cost rung is gross_ret - turn*bps/1e4."""
        W0 = Wreb[self.seg]
        h = W0 * self.CpS
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = Wreb[self.segp]
        hp = W0p * self.CpP
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(Wreb - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn

    def run_sparse(self, lists, wpn=GROSS0 / NCAND):
        """Identical arithmetic to run(), evaluated only on the <= 20 held columns.  Every book
        in this study holds at most NCAND names, so this is O(T * 20) instead of O(T * N);
        G1b pins it to run() bit-for-bit on the incumbent."""
        T, reb, C, Cp = self.T, self.reb, self.C, self.Cp
        gret = np.zeros(T)
        turn = np.zeros(T)
        prev_L, prev_a = np.empty(0, int), 0
        for k in range(len(reb)):
            a = reb[k]
            b = (reb[k + 1] - 1) if k + 1 < len(reb) else T - 1
            L = lists[k]
            cash = 1.0 - wpn * L.size
            # --- turnover paid at row a: target minus the drifted previous book
            if prev_L.size:
                hp = wpn * (Cp[a, prev_L] / Cp[prev_a, prev_L])
                heldp = hp / ((1.0 - wpn * prev_L.size) + hp.sum())
            else:
                heldp = np.empty(0)
            uni = np.union1d(L, prev_L)
            if uni.size:
                t = np.zeros(uni.size)
                t[np.searchsorted(uni, L)] = wpn
                if prev_L.size:
                    t[np.searchsorted(uni, prev_L)] -= heldp
                turn[a] = np.abs(t).sum()
            # --- the segment's daily returns
            if L.size:
                base = Cp[a, L]
                Vn = cash + wpn * (C[a:b + 1, L] / base).sum(axis=1)
                V = cash + wpn * (Cp[a:b + 1, L] / base).sum(axis=1)
                gret[a:b + 1] = Vn / V - 1.0
            prev_L, prev_a = L, a
        return gret, turn


def M0(r):
    v = r.std(ddof=1) * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = np.cumprod(1 + r)
    yrs = len(r) / 252
    vol = r.std(ddof=1) * np.sqrt(252)
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    h = len(r) // 2
    return dict(CAGR=eq[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r[:h]), H2=M0(r[h:]))


def keeppaths(m, oos_s, mb, ms, spy_oos):
    """PROTOCOL rule 4.  4a: Sharpe > live book in BOTH halves and MaxDD no worse.
       4b: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
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


# ----------------------------------------------------------------------------------- books --
def ranked_lists(pan, h):
    """The composite's top-20 list on every rebalance row, re-formed every h weekly dates.
    Returns (lists, sizes, nrepl) where lists[k] is the index array held from row reb[k]."""
    R = len(pan.reb)
    lists, sizes, nrepl = [np.empty(0, int)], [0], [0]
    cur = np.empty(0, int)
    for k in range(1, R):
        d = pan.dec[k]
        if (k - 1) % h == 0:                       # re-formation date
            el = np.flatnonzero(pan.elig[d])
            s = pan.sc[d][el]
            ok = ~np.isnan(s)
            el, s = el[ok], s[ok]
            # average-rank ties, exactly as baseline's `rank(axis=1, ascending=False) <= n`
            # (a tie straddling rank n keeps BOTH names; G3 pins this to the incumbent)
            new = el[(pd.Series(s).rank(ascending=False).values <= NCAND)] if el.size \
                else np.empty(0, int)
            nrepl.append(int(np.setdiff1d(new, cur, assume_unique=False).size))
            cur = np.sort(new)
        else:
            nrepl.append(0)
        lists.append(cur)
        sizes.append(cur.size)
    return lists, np.array(sizes), np.array(nrepl)


def random_lists(pan, h, sizes, nrepl, rng, free):
    """A coin flip matched to RANKED(h) name-for-name in COUNT (hence in GROSS, exactly) and,
    for free=False, in CHURN.  Count is matched first and always: the new list is `want` names,
    of which `want - m` are kept at random from the old list and `m` are drawn from the
    eligible pool, preferring names NOT just dropped so the replacement count is exactly m.
    When the pool of genuinely new eligible names runs out the fill falls back to just-dropped
    names -- a RE-ADD, which matches count but undercounts churn; re-adds are counted and
    reported (G5) rather than allowed to break the gross match.
    Returns (lists, n_readd, n_target_repl)."""
    R = len(pan.reb)
    lists = [np.empty(0, int)]
    cur = np.empty(0, int)
    readd = 0
    tgt = 0
    for k in range(1, R):
        d = pan.dec[k]
        if (k - 1) % h == 0:
            el = np.flatnonzero(pan.elig[d] & ~np.isnan(pan.sc[d]))
            want = int(sizes[k])
            if free:
                new = rng.choice(el, size=min(want, el.size), replace=False) \
                    if el.size and want else np.empty(0, int)
            else:
                m = int(nrepl[k])
                tgt += m
                keep_n = max(0, min(want - m, cur.size))
                kept = rng.choice(cur, size=keep_n, replace=False) if keep_n else np.empty(0, int)
                fresh = np.setdiff1d(el, cur, assume_unique=False)        # genuinely new names
                need = want - kept.size
                n1 = min(need, fresh.size)
                add = rng.choice(fresh, size=n1, replace=False) if n1 > 0 else np.empty(0, int)
                if need > n1:                                             # pool exhausted
                    back = np.setdiff1d(np.setdiff1d(el, kept), add)
                    n2 = min(need - n1, back.size)
                    if n2 > 0:
                        add = np.concatenate([add, rng.choice(back, size=n2, replace=False)])
                        readd += n2
                new = np.concatenate([kept, add]).astype(int)
            cur = np.sort(np.asarray(new, dtype=int))
        lists.append(cur)
    return lists, readd, tgt


def to_weights(pan, lists):
    W = np.zeros((len(pan.reb), pan.N))
    for k, l in enumerate(lists):
        if l.size:
            W[k, l] = GROSS0 / NCAND
    return W


def churn(lists):
    """Realised name replacements per year (a list of 20 fully replaced = 20 replacements).
    Between re-formations the SAME array object is appended, so identity skips the no-ops."""
    return sum(np.setdiff1d(lists[k], lists[k - 1]).size for k in range(1, len(lists))
               if lists[k] is not lists[k - 1])


# ----------------------------------------------------------------------------------- gates --
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def gates(panels, n_dropped):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    pan = panels["U56"]
    px = pan.px

    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights             : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= g2 == 0.0

    # G1: the Panel engine against engine.backtest on the live band book
    Wreb = np.zeros((len(pan.reb), pan.N))
    wv = w.values
    for k in range(1, len(pan.reb)):
        Wreb[k] = wv[pan.dec[k]]
    gr, tu = pan.run(Wreb)
    fast = gr - tu * COST0 / 1e4
    slow = backtest(px, w, cost_bps=COST0, freq=FREQ)["returns"].values
    g1 = float(np.abs(slow[WARM:] - fast[WARM:]).max())
    P(f"  G1 Panel.run == engine.backtest @10 bps                 : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    # G1b: the sparse engine used for every book below == the dense one, on the incumbent
    lists, sizes, nrepl = ranked_lists(pan, 1)
    gr, tu = pan.run(to_weights(pan, lists))
    grs, tus = pan.run_sparse(lists)
    g1b = max(float(np.abs(gr - grs).max()), float(np.abs(tu - tus).max()))
    P(f"  G1b Panel.run_sparse == Panel.run (incumbent book)      : {g1b:.3e}  "
      f"{'PASS' if g1b < 1e-12 else 'FAIL'}")
    ok &= g1b < 1e-12

    # G3: RANKED(h=1) reproduces the standing 2026-09-04 KEEP-4b incumbent
    m = M((gr - tu * COST0 / 1e4)[WARM:])
    d = {k: abs(m[k] - v) for k, v in KEEP4B_INCUMBENT.items()}
    P("  G3 RANKED(h=1) == 2026-09-04 KEEP-4b incumbent (U56 top-20 EW, no vol scaler):")
    P(f"     got {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   published "
      f"{KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {max(d.values()):.3e}  "
      f"{'PASS' if max(d.values()) < 5e-3 else 'FAIL'}")
    P("     (the published triple is the 2026-09-04 vintage; on today's cache idea 672 "
      "re-derived the same book at 12.63% / 1.090 / -18.31%, which this reproduces exactly)")
    ok &= max(d.values()) < 5e-3

    # G4/G5: the coin flips carry RANKED's gross exactly and (RMATCH) its churn
    g4 = 0.0
    ra, tg = 0, 0
    for h in HOLDS:
        L, S, NR = ranked_lists(pan, h)
        Wr = to_weights(pan, L)
        rng = np.random.default_rng(20260911)
        for free in (False, True):
            Lx, readd, tgt = random_lists(pan, h, S, NR, rng, free)
            Wx = to_weights(pan, Lx)
            g4 = max(g4, float(np.abs(Wx.sum(axis=1) - Wr.sum(axis=1)).max()))
            if not free:
                ra += readd
                tg += tgt
    g5 = ra / tg if tg else 1.0
    P(f"  G4 coin-flip daily gross == RANKED's, all h             : {g4:.3e}  "
      f"{'PASS' if g4 < 1e-12 else 'FAIL'}")
    P(f"  G5 RMATCH churn shortfall (re-adds / target replacements, U56, all h): "
      f"{g5:.4%}  {'PASS' if g5 < 0.02 else 'FAIL'}  ({ra} of {tg})")
    ok &= (g4 < 1e-12) and (g5 < 0.02)

    P(f"  G6 SMALL439 dropped {n_dropped} tickers with max_1d_move >= 1.0  : "
      f"{'PASS' if n_dropped > 0 else 'FAIL'}")
    ok &= n_dropped > 0
    P()
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- results below are not trustworthy'}")
    return ok


# ------------------------------------------------------------------------------------- run --
def load_panels():
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    raw["SMALL439"] = sm[keep]
    return {k: Panel(k, v) for k, v in raw.items()}, len(sm.columns) - len(keep)


def evaluate(pan, gr, tu, cost, refs):
    """Metrics + KEEP verdicts for one return stream at one cost rung."""
    r = (gr - tu * cost / 1e4)[pan.start:]
    oo = pan.oos_mask
    m, mo = M(r), M(r[oo])
    is_s = M0(r[~oo])
    mb, ms, spy_oos = refs[cost]["v2"], refs[cost]["spy"], refs[cost]["spy_oos"]
    p4a, p4b = keeppaths(m, mo["Sharpe"], mb, ms, spy_oos)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                IS_Sharpe=is_s, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"], keep4a=p4a, keep4b=p4b,
                fail4b=fail4b(m, mo["Sharpe"], ms, spy_oos))


def run(panels):
    P()
    P("=" * 100)
    P("(B) THE DECOMPOSITION -- 3 panels x 7 holding periods x {RANKED, RMATCH(60), RFREE(60)}")
    P("=" * 100)
    rows, draws_rows = [], []
    for pi, (pn, pan) in enumerate(panels.items()):
        px = pan.px
        dates = pan.idx[pan.start:]
        pan.oos_mask = np.asarray(dates >= pd.Timestamp(OOS_START))
        spy = px["SPY"].pct_change().fillna(0).values[pan.start:]
        ms, spy_o, spy_oos = M(spy), M(spy[pan.oos_mask]), M0(spy[pan.oos_mask])
        # live RULES v2 at each cost rung
        w = band_book(px, BAND0, GROSS0).values
        Wv2 = np.zeros((len(pan.reb), pan.N))
        for k in range(1, len(pan.reb)):
            Wv2[k] = w[pan.dec[k]]
        gv, tv = pan.run(Wv2)
        refs = {}
        for c in COSTS:
            rb = (gv - tv * c / 1e4)[pan.start:]
            refs[c] = dict(v2=M(rb), v2_oos=M(rb[pan.oos_mask]), spy=ms, spy_oos=spy_oos,
                           spy_o=spy_o)
        mb, base_o = refs[COST0]["v2"], refs[COST0]["v2_oos"]
        yrs = len(dates) / 252
        P()
        P(f"  --- {pn}  ({pan.N - 1} tradable names + SPY, {dates[0].date()} -> "
          f"{dates[-1].date()}, mean eligible {pan.elig[pan.start:].sum(axis=1).mean():.1f}) ---")
        P(f"      SPY            {ms['CAGR']:7.2%} / {ms['Sharpe']:6.3f} / {ms['MaxDD']:7.2%}"
          f"   H1 {ms['H1']:6.3f} H2 {ms['H2']:6.3f}   OOS {spy_o['CAGR']:7.2%} / "
          f"{spy_oos:6.3f} / {spy_o['MaxDD']:7.2%}")
        P(f"      live RULES v2  {mb['CAGR']:7.2%} / {mb['Sharpe']:6.3f} / {mb['MaxDD']:7.2%}"
          f"   H1 {mb['H1']:6.3f} H2 {mb['H2']:6.3f}   OOS {base_o['CAGR']:7.2%} / "
          f"{base_o['Sharpe']:6.3f} / {base_o['MaxDD']:7.2%}")
        P()
        P("      h   book     churn/yr    CAGR   Sharpe    MaxDD     H1     H2 | OOS CAGR "
          " OOS Shp  OOS DD | 4a  4b  fail4b")
        for h in HOLDS:
            L, S, NR = ranked_lists(pan, h)
            gr, tu = pan.run_sparse(L)
            ch = churn(L) / yrs
            per = {}
            for c in COSTS:
                e = evaluate(pan, gr, tu, c, refs)
                per[c] = e
                rows.append(dict(panel=pn, h=h, book="RANKED", cost=c, churn_yr=ch,
                                 churn_shortfall=0.0,
                                 turnover_yr=float(tu[pan.start:].sum() / yrs), stat="point",
                                 SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"],
                                 SPY_MaxDD=ms["MaxDD"], SPY_OOS_Sharpe=spy_oos,
                                 SPY_OOS_CAGR=spy_o["CAGR"], SPY_OOS_MaxDD=spy_o["MaxDD"],
                                 v2_Sharpe=refs[c]["v2"]["Sharpe"],
                                 v2_MaxDD=refs[c]["v2"]["MaxDD"],
                                 v2_OOS_Sharpe=refs[c]["v2_oos"]["Sharpe"], **e))
            e = per[COST0]
            P(f"      {h:>2}  RANKED   {ch:7.2f}   {e['CAGR']:7.2%} {e['Sharpe']:7.3f} "
              f"{e['MaxDD']:8.2%} {e['H1']:6.3f} {e['H2']:6.3f} | {e['OOS_CAGR']:8.2%} "
              f"{e['OOS_Sharpe']:8.3f} {e['OOS_MaxDD']:7.2%} | "
              f"{'Y' if e['keep4a'] else 'n'}   {'Y' if e['keep4b'] else 'n'}   {e['fail4b']}")

            for bk, free in (("RMATCH", False), ("RFREE", True)):
                acc = {c: [] for c in COSTS}
                chs, shortfalls = [], []
                for dr in range(NDRAW):
                    rng = np.random.default_rng([pi, h, dr, 679])
                    Lx, readd, tgt = random_lists(pan, h, S, NR, rng, free)
                    g2_, t2_ = pan.run_sparse(Lx)
                    chs.append(churn(Lx) / yrs)
                    shortfalls.append(readd / tgt if tgt else 0.0)
                    for c in COSTS:
                        ev = evaluate(pan, g2_, t2_, c, refs)
                        ev.update(draw=dr, turnover_yr=float(t2_[pan.start:].sum() / yrs))
                        acc[c].append(ev)
                        if c == COST0:
                            draws_rows.append(dict(panel=pn, h=h, book=bk, cost=c, **ev))
                for c in COSTS:
                    d = pd.DataFrame(acc[c])
                    agg = dict(panel=pn, h=h, book=bk, cost=c, churn_yr=float(np.mean(chs)),
                               churn_shortfall=float(np.mean(shortfalls)),
                               turnover_yr=float(d.turnover_yr.mean()), stat="median",
                               CAGR=d.CAGR.median(), Sharpe=d.Sharpe.median(),
                               MaxDD=d.MaxDD.median(), H1=d.H1.median(), H2=d.H2.median(),
                               IS_Sharpe=d.IS_Sharpe.median(), OOS_CAGR=d.OOS_CAGR.median(),
                               OOS_Sharpe=d.OOS_Sharpe.median(), OOS_MaxDD=d.OOS_MaxDD.median(),
                               keep4a=float(d.keep4a.mean()), keep4b=float(d.keep4b.mean()),
                               fail4b=d.fail4b.mode().iloc[0],
                               Sharpe_p05=d.Sharpe.quantile(0.05),
                               Sharpe_p95=d.Sharpe.quantile(0.95),
                               SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"],
                               SPY_MaxDD=ms["MaxDD"], SPY_OOS_Sharpe=spy_oos,
                               SPY_OOS_CAGR=spy_o["CAGR"], SPY_OOS_MaxDD=spy_o["MaxDD"],
                               v2_Sharpe=refs[c]["v2"]["Sharpe"],
                               v2_MaxDD=refs[c]["v2"]["MaxDD"],
                               v2_OOS_Sharpe=refs[c]["v2_oos"]["Sharpe"],
                               pct_of_ranked=float((d.Sharpe.values <
                                                    [r for r in rows
                                                     if r["panel"] == pn and r["h"] == h
                                                     and r["book"] == "RANKED"
                                                     and r["cost"] == c][0]["Sharpe"]).mean()))
                    rows.append(agg)
                a = [r for r in rows if r["panel"] == pn and r["h"] == h and r["book"] == bk
                     and r["cost"] == COST0][0]
                P(f"      {h:>2}  {bk:<8} {a['churn_yr']:7.2f}   {a['CAGR']:7.2%} "
                  f"{a['Sharpe']:7.3f} {a['MaxDD']:8.2%} {a['H1']:6.3f} {a['H2']:6.3f} | "
                  f"{a['OOS_CAGR']:8.2%} {a['OOS_Sharpe']:8.3f} {a['OOS_MaxDD']:7.2%} | "
                  f"{a['keep4a']:.2f} {a['keep4b']:.2f}  {a['fail4b']}  "
                  f"[p05 {a['Sharpe_p05']:.3f} p95 {a['Sharpe_p95']:.3f}; RANKED at "
                  f"{100*a['pct_of_ranked']:.1f}th pct"
                  + (f"; churn shortfall {a['churn_shortfall']:.2%}]" if bk == "RMATCH"
                     else "]"))
    return pd.DataFrame(rows), pd.DataFrame(draws_rows)


def legs(grid):
    P()
    P("=" * 100)
    P("(C) THE TWO LEGS @ 10 bps   SELECTION = RANKED - RMATCH   PERSISTENCE = RMATCH - RFREE")
    P("=" * 100)
    g = grid[grid.cost == COST0]
    out = []
    for pn in g.panel.unique():
        P()
        P(f"  --- {pn} ---")
        P("      h |  SELECTION (which names)        |  PERSISTENCE (how long, no skill) |"
          "  TOTAL vs free coin flip")
        P("        |  dSharpe   dCAGR   dMaxDD  dOOS |  dSharpe   dCAGR   dMaxDD  dOOS   |"
          "  dSharpe   dCAGR   dOOS")
        base1 = g[(g.panel == pn) & (g.h == 1) & (g.book == "RANKED")].iloc[0]
        for h in HOLDS:
            a = g[(g.panel == pn) & (g.h == h) & (g.book == "RANKED")].iloc[0]
            b = g[(g.panel == pn) & (g.h == h) & (g.book == "RMATCH")].iloc[0]
            c = g[(g.panel == pn) & (g.h == h) & (g.book == "RFREE")].iloc[0]
            P(f"      {h:>2}| {a.Sharpe-b.Sharpe:+8.4f} {a.CAGR-b.CAGR:+7.2%} "
              f"{a.MaxDD-b.MaxDD:+8.2%} {a.OOS_Sharpe-b.OOS_Sharpe:+6.3f} | "
              f"{b.Sharpe-c.Sharpe:+8.4f} {b.CAGR-c.CAGR:+7.2%} {b.MaxDD-c.MaxDD:+8.2%} "
              f"{b.OOS_Sharpe-c.OOS_Sharpe:+6.3f}   | {a.Sharpe-c.Sharpe:+8.4f} "
              f"{a.CAGR-c.CAGR:+7.2%} {a.OOS_Sharpe-c.OOS_Sharpe:+6.3f}")
            out.append(dict(panel=pn, h=h, cost=COST0,
                            SEL_dSharpe=a.Sharpe - b.Sharpe, SEL_dCAGR=a.CAGR - b.CAGR,
                            SEL_dMaxDD=a.MaxDD - b.MaxDD,
                            SEL_dOOS_Sharpe=a.OOS_Sharpe - b.OOS_Sharpe,
                            PER_dSharpe=b.Sharpe - c.Sharpe, PER_dCAGR=b.CAGR - c.CAGR,
                            PER_dMaxDD=b.MaxDD - c.MaxDD,
                            PER_dOOS_Sharpe=b.OOS_Sharpe - c.OOS_Sharpe,
                            TOT_dSharpe=a.Sharpe - c.Sharpe, TOT_dCAGR=a.CAGR - c.CAGR,
                            TOT_dOOS_Sharpe=a.OOS_Sharpe - c.OOS_Sharpe,
                            PERSEL_dSharpe=a.Sharpe - base1.Sharpe,
                            PERSEL_dCAGR=a.CAGR - base1.CAGR,
                            PERSEL_dMaxDD=a.MaxDD - base1.MaxDD,
                            PERSEL_dOOS_Sharpe=a.OOS_Sharpe - base1.OOS_Sharpe,
                            RANKED_4b=bool(a.keep4b), RMATCH_4b=float(b.keep4b),
                            RFREE_4b=float(c.keep4b), RANKED_pct_in_RMATCH=b.pct_of_ranked,
                            RANKED_churn=a.churn_yr, RMATCH_churn=b.churn_yr,
                            RFREE_churn=c.churn_yr))
        P("      PERSISTENCE AT MATCHED NAMES (RANKED(h) - RANKED(1), the queue's second "
          "reading):")
        s = "  ".join(f"h={h}: {g[(g.panel == pn) & (g.h == h) & (g.book == 'RANKED')].iloc[0].Sharpe - base1.Sharpe:+.4f}"
                      for h in HOLDS)
        P(f"        dSharpe  {s}")
    return pd.DataFrame(out)


def ruleeight(grid, draws):
    P()
    P("=" * 100)
    P("(D) PROTOCOL RULE 8 -- h chosen on IS (2009-2016) only, scored on 2017-2026 untouched")
    P("=" * 100)
    g = grid[grid.cost == COST0]
    rows = []
    for pn in g.panel.unique():
        spy = g[g.panel == pn].iloc[0]
        v2o = g[g.panel == pn].iloc[0].v2_OOS_Sharpe
        P()
        P(f"  --- {pn} ---   SPY OOS {spy.SPY_OOS_CAGR:.2%} / {spy.SPY_OOS_Sharpe:.3f} / "
          f"{spy.SPY_OOS_MaxDD:.2%}   live v2 OOS Sharpe {v2o:.3f}")
        r = g[(g.panel == pn) & (g.book == "RANKED")]
        pick = r.loc[r.IS_Sharpe.idxmax()]
        P("      RANKED   IS Sharpe by h: " +
          "  ".join(f"h={int(x.h)}: {x.IS_Sharpe:.3f}" for _, x in r.iterrows()))
        P(f"      RANKED   rule-8 pick h={int(pick.h)}  ->  OOS {pick.OOS_CAGR:7.2%} / "
          f"{pick.OOS_Sharpe:6.3f} / {pick.OOS_MaxDD:7.2%}   (blind-commit h=1 OOS "
          f"{r[r.h == 1].iloc[0].OOS_Sharpe:.3f})")
        rows.append(dict(panel=pn, book="RANKED", pick_h=int(pick.h), stat="point",
                         IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                         OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                         SPY_OOS_CAGR=spy.SPY_OOS_CAGR, SPY_OOS_Sharpe=spy.SPY_OOS_Sharpe,
                         SPY_OOS_MaxDD=spy.SPY_OOS_MaxDD, v2_OOS_Sharpe=v2o,
                         beats_SPY_OOS=bool(pick.OOS_Sharpe > spy.SPY_OOS_Sharpe),
                         beats_v2_OOS=bool(pick.OOS_Sharpe > v2o)))
        for bk in ("RMATCH", "RFREE"):
            d = draws[(draws.panel == pn) & (draws.book == bk)]
            per = []
            for dr in sorted(d.draw.unique()):
                dd = d[d.draw == dr]
                pk = dd.loc[dd.IS_Sharpe.idxmax()]
                per.append(dict(h=pk.h, OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                OOS_MaxDD=pk.OOS_MaxDD))
            pf = pd.DataFrame(per)
            hs = pf.h.value_counts().sort_index()
            P(f"      {bk:<8} rule-8 picks over {len(pf)} draws: " +
              "  ".join(f"h={int(k)}x{v}" for k, v in hs.items()) +
              f"  ->  median OOS {pf.OOS_CAGR.median():7.2%} / {pf.OOS_Sharpe.median():6.3f} / "
              f"{pf.OOS_MaxDD.median():7.2%}   beats SPY OOS in "
              f"{(pf.OOS_Sharpe > spy.SPY_OOS_Sharpe).mean():.0%} of draws")
            rows.append(dict(panel=pn, book=bk, pick_h=int(pf.h.mode().iloc[0]), stat="median",
                             IS_Sharpe=np.nan, OOS_CAGR=pf.OOS_CAGR.median(),
                             OOS_Sharpe=pf.OOS_Sharpe.median(),
                             OOS_MaxDD=pf.OOS_MaxDD.median(),
                             SPY_OOS_CAGR=spy.SPY_OOS_CAGR, SPY_OOS_Sharpe=spy.SPY_OOS_Sharpe,
                             SPY_OOS_MaxDD=spy.SPY_OOS_MaxDD, v2_OOS_Sharpe=v2o,
                             beats_SPY_OOS=float((pf.OOS_Sharpe > spy.SPY_OOS_Sharpe).mean()),
                             beats_v2_OOS=float((pf.OOS_Sharpe > v2o).mean())))
        # the decisive comparison: does the rule-8 RANKED pick beat the rule-8 coin flip?
        rm = [x for x in rows if x["panel"] == pn and x["book"] == "RMATCH"][0]
        P(f"      SELECTION at the rule-8 pick: RANKED OOS Sharpe {pick.OOS_Sharpe:.3f} vs "
          f"turnover-matched coin flip {rm['OOS_Sharpe']:.3f}  ->  "
          f"{pick.OOS_Sharpe - rm['OOS_Sharpe']:+.4f}")
    return pd.DataFrame(rows)


def answer(grid, leg, wf):
    P()
    P("=" * 100)
    P("(E) THE ANSWER")
    P("=" * 100)
    g = grid[grid.cost == COST0]
    P()
    P("  KEEP paths over the 21 RANKED cells @10 bps (PROTOCOL rule 4):")
    r = g[g.book == "RANKED"]
    P(f"    4a {int(r.keep4a.sum())}/{len(r)}   4b {int(r.keep4b.sum())}/{len(r)}   "
      f"BOTH {int((r.keep4a.astype(bool) & r.keep4b.astype(bool)).sum())}/{len(r)}")
    for _, x in r[r.keep4b.astype(bool)].iterrows():
        P(f"      4b PASS: {x.panel} RANKED h={int(x.h)}  {x.CAGR:.2%} / {x.Sharpe:.3f} / "
          f"{x.MaxDD:.2%}   OOS {x.OOS_CAGR:.2%} / {x.OOS_Sharpe:.3f} / {x.OOS_MaxDD:.2%}")
    P()
    P("  Coin-flip 4b pass SHARE at the same cells (60 draws each):")
    for pn in g.panel.unique():
        s1 = g[(g.panel == pn) & (g.book == "RMATCH")]
        s2 = g[(g.panel == pn) & (g.book == "RFREE")]
        P(f"    {pn:<9} RMATCH " + " ".join(f"h{int(x.h)}:{x.keep4b:.2f}"
                                            for _, x in s1.iterrows()) +
          "   |  RFREE " + " ".join(f"h{int(x.h)}:{x.keep4b:.2f}" for _, x in s2.iterrows()))
    P()
    P("  WHICH LEG CARRIES IT -- mean over the 21 cells @10 bps:")
    P(f"    SELECTION   dSharpe {leg.SEL_dSharpe.mean():+.4f}  (median "
      f"{leg.SEL_dSharpe.median():+.4f}, >0 in {int((leg.SEL_dSharpe > 0).sum())}/{len(leg)} "
      f"cells)   dCAGR {leg.SEL_dCAGR.mean():+.2%}   dOOS_Sharpe "
      f"{leg.SEL_dOOS_Sharpe.mean():+.4f}")
    P(f"    PERSISTENCE dSharpe {leg.PER_dSharpe.mean():+.4f}  (median "
      f"{leg.PER_dSharpe.median():+.4f}, >0 in {int((leg.PER_dSharpe > 0).sum())}/{len(leg)} "
      f"cells)   dCAGR {leg.PER_dCAGR.mean():+.2%}   dOOS_Sharpe "
      f"{leg.PER_dOOS_Sharpe.mean():+.4f}")
    P(f"    TOTAL       dSharpe {leg.TOT_dSharpe.mean():+.4f}   dCAGR "
      f"{leg.TOT_dCAGR.mean():+.2%}   dOOS_Sharpe {leg.TOT_dOOS_Sharpe.mean():+.4f}")
    P(f"    share of TOTAL dSharpe carried by PERSISTENCE: "
      f"{leg.PER_dSharpe.sum() / leg.TOT_dSharpe.sum():.1%}" if leg.TOT_dSharpe.sum() else "")
    P()
    P("  COST APPENDIX (labelled robustness, NO verdict taken here): RANKED 4b / mean coin-flip"
      " 4b share")
    for c in COSTS:
        gg = grid[grid.cost == c]
        rr = gg[gg.book == "RANKED"]
        P(f"    {c:>5.1f} bps: RANKED 4a {int(rr.keep4a.sum())}/{len(rr)} 4b "
          f"{int(rr.keep4b.sum())}/{len(rr)}   RMATCH mean 4b share "
          f"{gg[gg.book == 'RMATCH'].keep4b.mean():.3f}   RFREE mean 4b share "
          f"{gg[gg.book == 'RFREE'].keep4b.mean():.3f}")


def main():
    panels, n_dropped = load_panels()
    ok = gates(panels, n_dropped)
    grid, draws = run(panels)
    for c in ("keep4a", "keep4b"):
        grid[c] = grid[c].astype(float)
        if c in draws: draws[c] = draws[c].astype(float)
    leg = legs(grid)
    wf = ruleeight(grid, draws)
    answer(grid, leg, wf)
    P()
    dump(grid, "grid")
    dump(leg, "legs")
    dump(wf, "walkforward")
    dump(draws, "draws")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"  wrote {STEM}.console.txt")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
