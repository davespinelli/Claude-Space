#!/usr/bin/env python3
"""
IDEA 680 -- does-any-4b-pass-in-the-record-survive-a-ZERO-COST-BASE-RATE-clause   (lane B)
==========================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 502 found 78.1% of gross-matched coin flips clear 4b on U56 at 0 bps with the standing
  candidate at their 78th percentile, i.e. at zero cost the bar certifies the FAMILY, not the
  rule.  Re-score every committed 4b passer in the record against its own panel's zero-cost
  coin-flip base rate and report how many sit outside their null.
  Max 2 params (claim set, draws).

WHY IT MATTERS FOR CAPITAL
--------------------------
  A 4b pass is the record's only capital-worthy verdict.  If a coin flip drawn from the same
  panel at the same gross clears the same bar at a respectable rate, then the row certifies the
  admission family and the exposure, not the selection rule -- and no capital should follow the
  rule on the strength of that row.  A BASE-RATE CLAUSE is the cheapest possible repair: report
  the null's pass share beside every 4b pass, and only call a pass EVIDENCE when it is rare
  under its own null.  This run measures what that clause would cost the record.

THE TWO PARTS
-------------
  PART A  CENSUS of the record's own machine-readable 4b ledger.  Every committed
          research/backtests/*.csv is scanned for a 4b pass-flag column; every PASS row is
          counted and classified by the CONSTRUCTION of the book it belongs to (REAL rule /
          NULL-construction / UNLABELLED).  No simulation -- each row is read exactly as its
          own run published it.  This is the denominator the queue's "every committed 4b
          passer" needs, and it is reported before any new number is priced.
  PART B  the PRICE LEG.  The record's modal REAL 4b-pass book keys are rebuilt on their own
          panels and each is scored against a GROSS-MATCHED coin-flip null built by replacing
          its SELECTION with a draw and changing nothing else.  Reported per book: the 4b
          verdict, the null's 4b base rate, and the book's percentile inside its own null, at
          0 bps (the queue's object) and at 10 bps (PROTOCOL rule 2's rung).

THE NULLS -- one per book, gross-matched BY CONSTRUCTION (not re-grossed after the fact)
-----------------------------------------------------------------------------------------
  THE SHARED CONSTRUCTION.  On every rebalance row the book holds n(t) names at one common
  per-name weight w(t).  Its null holds n(t) names drawn UNIFORMLY from that family's POOL at
  the SAME w(t).  Count and per-name weight are COPIED FROM THE BOOK, so gross, cash drag and
  the whole de-grossing path are identical row by row and the only thing that changes is WHICH
  names are held.  That is why G5's gross match is exact rather than approximate.
  TOPk  (CAND20/CAND10/CAND05, the record's `TOP20`/`top20`/`CAND20` keys): the book holds the
        top k eligible names by the composite at gross/k each.  POOL = its own candidate set
        (eligible AND carrying a finite composite), i.e. the names the ranking is ranking.  The
        composite ranking becomes a coin flip and nothing else moves.
  EWELIG (the record's `EWALL`/`EWall` key; RECOMMENDATION Finding 2): equal-weight EVERY
        eligible name, re-spread to full gross.  Its selection IS the gate, so its null must be
        gate-free: POOL = every priced name.  Same breadth, admission by coin flip.
  BAND03 (RULES v2, the live baseline, de-gross convention): holds every name inside the 200d
        +/-3% band at gross/N_priced, gated-out weight to CASH.  POOL = every priced name, same
        reason -- identical gross path and cash drag, admission by coin flip.
  RANDFIX (secondary, binding cell only): one FIXED random list of 20 names held through the
        same gate.  Reported beside RANDROT on U56/TOP20 so the headline is not an artefact of
        the rotation convention; never mixed into a base-rate headline.

DESIGN
------
  TUNED (2, and only 2)
    1. CLAIM SET  CORE = the 5 rebuildable REAL book keys at gross 0.75 (the record's modal
                  convention and the live baseline's own gross);
                  EXT  = the same 5 at gross 1.00 (PROTOCOL 2's no-leverage ceiling, where a
                  large part of the record's committed 4b passes actually live).
                  Both reported in full at every cost rung; never averaged together.
    2. DRAWS      250 / 500 / 1000, NESTED (the 250 grid is the first 250 seeds of the 1000),
                  so the draw axis reports a convergence, not three samples.
  NOT TUNED
    COST          0 bps is fixed BY THE QUESTION (the queue asks for the zero-cost base rate);
                  10 bps is fixed by PROTOCOL rule 2; 25 bps is printed as a stress column.
                  Every book is reported at every rung -- no rung is chosen by outcome.
    FIXED         gate = above 200d MA and vol20 < 0.60; cadence W; warm-up 260 rows;
                  IS <= 2016-12-31 / OOS >= 2017-01-01 (PROTOCOL rule 8); seed base 680.
  PANELS          U56 is BINDING (the candidate's own panel and 502's).  B136 and SMALL439 are
                  run identically as a LABELLED REPLICATION; no headline verdict is taken from
                  them and they are not a third tuned axis.

  PERCENTILE convention: a book's percentile is the share of null draws it BEATS
  (Sharpe/CAGR: null < book; MaxDD: |null| > |book|).  The one-sided empirical p is
  (1 + #{null >= book}) / (1 + draws).  "OUTSIDE its null" is pre-registered as
  BASE RATE <= 0.05, i.e. fewer than one null draw in twenty clears the same 4b bar.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  ctx.run == engine.backtest @ 10 bps on a dense book                        bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                         bar 0.0
  G3  the standing 2026-09-04 KEEP-4b incumbent re-derived on U56 (top-20 EW, no vol scaler,
      gross 0.75, weekly, 10 bps): published 12.66% / 1.0921 / -18.31%           bar 5e-3
  G3b RECOMMENDATION Finding 2's EWELIG on U56 at 0.75 / weekly / 10 bps:
      published 10.4% / 1.05 / halves 1.07 / 1.03                                bar 1.5e-2
  G4  panel triples (SPY and RULES v2) printed for every panel, both windows
  G5  GROSS MATCH: every null family's mean realised gross within 0.01 of its book's
  G6  determinism: seed 680 re-run reproduces its return stream exactly           bar 0.0
  G7  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G8  census self-check: the pass-flag parser re-read on a 60-file sample by an independent
      code path returns the same PASS counts                                      bar 0 rows
  G9  NESTING: the 250- and 500-draw base rates are computed from prefixes of the same 1000
      draw streams (asserted on the stored per-draw pass vector)                  bar 0.0

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  universe.json / universe_broad.json / the SMALL screen are CURRENT-CONSTITUENT lists, so
  every CAGR and drawdown LEVEL below is optimistic.  The bias has a specific and reportable
  direction here: a coin flip drawn from a survivor panel is a BETTER book than a coin flip
  drawn in real time would have been, so the null's 4b base rate is an UPPER bound on the true
  base rate and each book's percentile inside it is a LOWER bound.  That direction favours the
  queue's suspicion and works AGAINST the incumbents, so it is stated rather than buried.  The
  base rates, percentiles and book-vs-null contrasts are same-tape comparisons; the 4b bar
  itself is against SPY, which is NOT survivorship-inflated, so the 4b LEVELS are not protected
  by the usual same-tape argument.
"""
import sys, re, csv, glob, time, warnings, collections
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

FREQ = "W"
BAND0 = 0.03
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED0 = 680
COSTS = [0.0, 10.0, 25.0]           # NOT tuned: 0 = the question, 10 = PROTOCOL, 25 = stress
HEAD_COST = 0.0                     # the queue's object
DRAW_GRID = [250, 500, 1000]        # TUNED axis 2 (nested)
DRAWS = max(DRAW_GRID)
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}   # TUNED axis 1
BINDING_PANEL = "U56"
BASE_RATE_BAR = 0.05                # pre-registered "outside its null"

KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)
EWELIG_F2 = dict(CAGR=0.104, Sharpe=1.05, H1=1.07, H2=1.03)

# SMOKE=1 runs the identical code path on a 12-draw grid and the binding panel only, purely to
# exercise every branch before the full run; it is never the source of a published number (the
# console header prints the grid actually used).
SMOKE = bool(int(__import__("os").environ.get("IDEA680_SMOKE", "0")))
if SMOKE:
    DRAW_GRID = [4, 8, 12]
    DRAWS = max(DRAW_GRID)

NULLKEY = re.compile(r"(shuff|rand|perm|placebo|coin|flip|null|block|scramble|boot|resamp)", re.I)
FLAGCOLS = {"pass4b", "p4b", "4b", "pass_4b", "is4b", "keep4b", "path4b", "verdict4b",
            "v4b", "oos4b"}
TRUEVALS = {"1", "1.0", "true", "yes", "y", "pass", "keep", "t"}
BOOKCOLS = ["book", "arm", "key", "book_key", "spec", "strategy", "name", "cand"]
PANELCOLS = ["panel", "universe", "panel_name"]

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# fast runner (same construction as idea 502's Ctx; G1 asserts it against engine.backtest)
# ==========================================================================================
class Ctx:
    def __init__(self, px, freq=FREQ):
        self.idx = px.index
        self.cols = list(px.columns)
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
        self.dec = np.maximum(self.reb - 1, 0)      # close at which each rebalance is decided

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def run(self, wt):
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

    def gross(self, wt, i0):
        reb = self.reb[self.reb >= i0]
        return float(wt[reb].sum(axis=1).mean())


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mets(r):
    """r: 1-d ndarray of daily returns."""
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252)
    dd = float((eq / np.maximum.accumulate(eq) - 1).min())
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd,
                H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs4b(m, oos_s, ms, spy_oos):
    """the five 4b legs as BOOLEANS, in PROTOCOL order."""
    return dict(L1_H1=m["H1"] > ms["H1"], L2_H2=m["H2"] > ms["H2"], L3_OOS=oos_s > spy_oos,
                L4_DD=abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
                L5_CAGR=m["CAGR"] >= 0.70 * ms["CAGR"])


def pass4b(m, oos_s, ms, spy_oos):
    return all(legs4b(m, oos_s, ms, spy_oos).values())


def pass4a(m, mb):
    return bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])


def pass4b_is(mi, msi):
    """The 4b LEVEL legs read INSIDE the 2009-2016 window only (rule 8's IS side).  No OOS leg
    exists in-sample by construction, so this is the four legs that can be read there."""
    return bool(mi["H1"] > msi["H1"] and mi["H2"] > msi["H2"] and
                abs(mi["MaxDD"]) <= 0.60 * abs(msi["MaxDD"]) and
                mi["CAGR"] >= 0.70 * msi["CAGR"])


def failstr(m, oos_s, ms, spy_oos):
    f = [k for k, v in legs4b(m, oos_s, ms, spy_oos).items() if not v]
    return "+".join(f) if f else "-"


# ==========================================================================================
# PART A -- the census of the record's own 4b ledger
# ==========================================================================================
def census():
    P("=" * 100)
    P("(A) CENSUS -- the record's own machine-readable 4b ledger, read exactly as published")
    P("=" * 100)
    files = sorted(glob.glob(str(OUT / "*.csv")))
    me = {str(OUT / f"{STEM}.{s}.csv") for s in
          ("census", "books", "nulls", "walkforward", "draws")}
    files = [f for f in files if f not in me]
    if SMOKE:
        files = files[:200]
    rows = []
    t0 = time.time()
    for f in files:
        try:
            with open(f, newline="") as fh:
                rd = csv.DictReader(fh)
                hdr = rd.fieldnames or []
                hit = [c for c in hdr if c.strip().lower() in FLAGCOLS]
                if not hit:
                    continue
                bc = next((c for c in hdr if c.strip().lower() in BOOKCOLS), None)
                pc = next((c for c in hdr if c.strip().lower() in PANELCOLS), None)
                cnt = collections.Counter()
                for row in rd:
                    cnt["rows"] += 1
                    if not any(str(row.get(c, "")).strip().lower() in TRUEVALS for c in hit):
                        continue
                    cnt["pass"] += 1
                    b = str(row.get(bc, "")).strip() if bc else ""
                    p = str(row.get(pc, "")).strip() if pc else ""
                    cls = ("UNLABELLED" if not b else
                           "NULL" if NULLKEY.search(b) else "REAL")
                    cnt[cls] += 1
                    if cls == "REAL":
                        cnt["key::" + p + "|" + b] += 1
            if cnt["rows"]:
                rows.append(dict(file=Path(f).name, rows=cnt["rows"], pass4b=cnt["pass"],
                                 REAL=cnt["REAL"], NULL=cnt["NULL"],
                                 UNLABELLED=cnt["UNLABELLED"],
                                 flagcols="+".join(hit), bookcol=bc or "", panelcol=pc or ""))
        except Exception:
            continue
    cen = pd.DataFrame(rows)
    tot = cen[["rows", "pass4b", "REAL", "NULL", "UNLABELLED"]].sum()
    P(f"  files scanned {len(files)}   files carrying a 4b pass-flag column {len(cen)}   "
      f"({time.time() - t0:.0f}s)")
    P(f"  committed rows in those files {int(tot['rows']):,}")
    P(f"  committed 4b PASS rows        {int(tot['pass4b']):,}")
    sh = lambda k: 100.0 * tot[k] / max(tot["pass4b"], 1)
    P(f"     of which REAL-rule books   {int(tot['REAL']):,}  ({sh('REAL'):.1f}%)")
    P(f"     of which NULL-construction {int(tot['NULL']):,}  ({sh('NULL'):.1f}%)"
      "   <- coin flips, permutations, shuffles and blocks")
    P(f"     of which UNLABELLED        {int(tot['UNLABELLED']):,}  ({sh('UNLABELLED'):.1f}%)"
      "   <- no book column, construction not recoverable from the CSV")
    dump(cen.sort_values("pass4b", ascending=False), "census")
    return cen, tot


def census_selfcheck(cen):
    """G8: re-count PASS rows on a 60-file sample with an independent (pandas) code path."""
    samp = cen.sort_values("file").iloc[::max(len(cen) // 60, 1)].head(60)
    bad = 0
    for _, r in samp.iterrows():
        df = pd.read_csv(OUT / r["file"], low_memory=False)
        cols = [c for c in df.columns if c.strip().lower() in FLAGCOLS]
        m = np.zeros(len(df), bool)
        for c in cols:
            m |= df[c].astype(str).str.strip().str.lower().isin(TRUEVALS).values
        if int(m.sum()) != int(r["pass4b"]):
            bad += 1
    return len(samp), bad


# ==========================================================================================
# PART B -- panels, books, nulls
# ==========================================================================================
def load_panels():
    if SMOKE:
        return {"U56": load_universe()}, 0
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL439"] = sm[keep]
    return panels, len(sm.columns) - len(keep)


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def build_books(px, g):
    """The record's modal REAL 4b-pass book keys, at gross g, weekly.

    Returns (books, cand) where `cand` is the TOPk books' own CANDIDATE SET -- eligible AND
    carrying a finite composite score, i.e. exactly the names a coin flip would be choosing
    among under the same gate.  Matching the null's pool to `cand` (rather than to `elig`) is
    what makes the gross match EXACT rather than approximate; G5 asserts it.
    """
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    cand = elig & sc.notna()
    rank = sc.where(elig).rank(axis=1, ascending=False)
    bk = {}
    for k in (5, 10, 20):
        bk[f"TOP{k}"] = (rank <= k).astype(float) * (g / k)
    n_el = elig.sum(axis=1).replace(0, np.nan)
    bk["EWELIG"] = elig.astype(float).div(n_el, axis=0).fillna(0.0) * g     # re-spread to g
    bk["BAND03"] = band_book(px, BAND0, g)                                  # de-gross to cash
    return bk, cand


def null_streams(ctx, px, cand, draws, seed0=SEED0):
    """One generator per null family, yielding the SHIFTED weight ndarray for each draw.

    The construction is the same for all three families and is what makes the gross match
    EXACT: on each rebalance row the book holds `n(t)` names at a common per-name weight
    `w(t)`; the null holds `n(t)` names drawn UNIFORMLY from that family's POOL at the SAME
    `w(t)`.  Count and per-name weight are copied from the book, so gross, cash drag and
    de-grossing path are identical and the ONLY thing that changes is WHICH names are held.

      ROT{k} (-> TOP{k})  POOL = the book's own candidate set (eligible AND scored), i.e. the
                          names the composite is ranking.  The ranking becomes a coin flip.
      EW     (-> EWELIG)  POOL = every priced name.  EWELIG's selection IS the gate, so its
                          null must be gate-free: same breadth, admission by coin flip.
      BD     (-> BAND03)  POOL = every priced name, same reason.
    """
    T, N = ctx.T, ctx.N
    cv = cand.values
    priced = px.notna().values
    reb, dec = ctx.reb, ctx.dec
    POOL = {"ROT": cv[dec], "EW": priced[dec], "BD": priced[dec]}

    def topmask(E, take, rng):
        R = rng.random(E.shape)
        R[~E] = -1.0
        order = np.argsort(-R, axis=1)
        pos = np.argsort(order, axis=1)
        return (pos < take[:, None]) & E

    def gen(kind, wt_book, k=None):
        """wt_book: the BOOK's shifted weight ndarray -- the source of n(t) and w(t)."""
        wrow = wt_book[reb]
        cnt = (wrow > 0).sum(axis=1)
        tot = wrow.sum(axis=1)
        perw = np.where(cnt > 0, tot / np.maximum(cnt, 1), 0.0)
        E = POOL[kind]
        take = np.minimum(E.sum(axis=1), cnt)
        for d in range(draws):
            rng = np.random.default_rng(seed0 + 1_000_000 * {"ROT": 0, "EW": 1, "BD": 2}[kind]
                                        + 10_000 * (k or 0) + d)
            W = np.zeros((T, N))
            W[reb] = topmask(E, take, rng) * perw[:, None]
            yield d, W
    return gen


def randfix_stream(ctx, px, cand, g, k, draws, seed0=SEED0 + 777):
    """RANDFIX: one FIXED random list of k names held through the SAME gate (secondary null).
    Unlike the rotating nulls this one is NOT count-matched day by day -- a fixed list drifts
    in and out of the gate on its own -- which is exactly why it is reported as a secondary
    comparand and never mixed into a base-rate headline."""
    T, N = ctx.T, ctx.N
    ev = cand.values
    pool = np.flatnonzero(ev.any(axis=0))
    for d in range(draws):
        rng = np.random.default_rng(seed0 + d)
        pick = rng.permutation(pool)[:k]
        dense = np.zeros((T, N))
        dense[:, pick] = ev[:, pick] * (g / k)
        yield d, np.vstack([np.zeros((1, N)), dense[:-1]])


# ==========================================================================================
def gates(panels, n_dropped):
    P("=" * 100)
    P("(B) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = {}
    px = panels[BINDING_PANEL]
    w = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    ok["G2"] = g2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights      : {g2:.3e}  "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    ctx = Ctx(px)
    gr, turn = ctx.run(ctx.shift(w))
    fast = pd.Series(gr - turn * 10.0 / 1e4, index=px.index)
    slow = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"]
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    ok["G1"] = g1 < 1e-12
    P(f"  G1 ctx.run == engine.backtest @10 bps            : {g1:.3e}  "
      f"{'PASS' if ok['G1'] else 'FAIL'}")

    bks, cand = build_books(px, 0.75)
    grc, tnc = ctx.run(ctx.shift(bks["TOP20"]))
    m = mets((grc - tnc * 10.0 / 1e4)[WARM:])
    d3 = max(abs(m[k] - v) for k, v in KEEP4B_INCUMBENT.items())
    ok["G3"] = d3 < 5e-3
    P(f"  G3 2026-09-04 KEEP-4b incumbent (U56 TOP20 EW, no vol scaler):")
    P(f"     got {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   published "
      f"{KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {d3:.3e}  "
      f"{'PASS' if ok['G3'] else 'FAIL'}")

    gre, tne = ctx.run(ctx.shift(bks["EWELIG"]))
    me = mets((gre - tne * 10.0 / 1e4)[WARM:])
    d3b = max(abs(me[k] - v) for k, v in EWELIG_F2.items())
    ok["G3b"] = d3b < 1.5e-2
    P(f"  G3b RECOMMENDATION Finding 2 EWELIG (U56, 0.75, W, 10 bps):")
    P(f"     got {me['CAGR']:.2%} / {me['Sharpe']:.3f} / halves {me['H1']:.2f}/{me['H2']:.2f}"
      f"   published {EWELIG_F2['CAGR']:.1%} / {EWELIG_F2['Sharpe']:.2f} / "
      f"{EWELIG_F2['H1']:.2f}/{EWELIG_F2['H2']:.2f}   max|d| {d3b:.3e}  "
      f"{'PASS' if ok['G3b'] else 'FAIL'}")

    wt20 = ctx.shift(bks["TOP20"])
    g6a, _ = ctx.run(next(null_streams(ctx, px, cand, 1)("ROT", wt20, 20))[1])
    g6b, _ = ctx.run(next(null_streams(ctx, px, cand, 1)("ROT", wt20, 20))[1])
    g6 = float(np.abs(g6a - g6b).max())
    ok["G6"] = g6 == 0.0
    P(f"  G6 determinism (seed {SEED0} re-drawn)             : {g6:.3e}  "
      f"{'PASS' if ok['G6'] else 'FAIL'}")
    if "SMALL439" in panels:
        P(f"  G7 SMALL439 screen: {n_dropped} tickers with max_1d_move >= 1.0 dropped  "
          f"({panels['SMALL439'].shape[1] - 1} names + SPY)  PASS")
        ok["G7"] = True
    return ok


def panel_context(px):
    """SPY and RULES v2 comparands for one panel, at every cost rung, both windows."""
    ctx = Ctx(px)
    idx = px.index
    i0 = WARM
    oos_mask = np.asarray(idx >= pd.Timestamp(OOS_START))[i0:]
    is_mask = np.asarray(idx <= pd.Timestamp(IS_END))[i0:]
    spy = px["SPY"].pct_change().fillna(0.0).values[i0:]
    out = dict(ctx=ctx, i0=i0, idx=idx, oos=oos_mask, is_=is_mask,
               spy=mets(spy), spy_oos=mets(spy[oos_mask]), spy_is=mets(spy[is_mask]))
    v2 = rules_v2_weights(px, BAND0, 0.75)
    gr, tn = ctx.run(ctx.shift(v2))
    out["v2"] = {}
    for c in COSTS:
        r = (gr - tn * c / 1e4)[i0:]
        out["v2"][c] = dict(full=mets(r), oos=mets(r[oos_mask]), is_=mets(r[is_mask]))
    return out


def score_stream(gr, tn, pc, c):
    i0, oos, is_ = pc["i0"], pc["oos"], pc["is_"]
    r = (gr - tn * c / 1e4)[i0:]
    return mets(r), mets(r[oos]), mets(r[is_])


# ==========================================================================================
def main():
    t_start = time.time()
    P(f"IDEA 680  does-any-4b-pass-in-the-record-survive-a-ZERO-COST-BASE-RATE-clause  (lane B)")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   seed base {SEED0}   "
      f"draws {DRAW_GRID}   claim sets {list(CLAIM_SETS)}   costs {COSTS} bps")
    P()
    cen, tot = census()
    n_s, n_bad = census_selfcheck(cen)
    P(f"  G8 census self-check on {n_s} files by an independent pandas path: "
      f"{n_bad} disagreements  {'PASS' if n_bad == 0 else 'FAIL'}")
    P()
    panels, n_dropped = load_panels()
    gk = gates(panels, n_dropped)
    gk["G8"] = n_bad == 0
    P()
    P("=" * 100)
    P("(C) PANEL TRIPLES (G4) -- full sample from row 260, and the rule-8 OOS window")
    P("=" * 100)
    PC = {}
    for name, px in panels.items():
        pc = panel_context(px)
        PC[name] = pc
        s, so = pc["spy"], pc["spy_oos"]
        v = pc["v2"][10.0]
        P(f"  {name:9s} n={px.shape[1]:4d}  {px.index[WARM].date()}..{px.index[-1].date()}")
        P(f"     SPY        full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:7.2%}  "
          f"(halves {s['H1']:.3f}/{s['H2']:.3f})   OOS {so['CAGR']:7.2%} / "
          f"{so['Sharpe']:.4f} / {so['MaxDD']:7.2%}")
        P(f"     RULES v2   full {v['full']['CAGR']:7.2%} / {v['full']['Sharpe']:.4f} / "
          f"{v['full']['MaxDD']:7.2%}  (halves {v['full']['H1']:.3f}/{v['full']['H2']:.3f})"
          f"   OOS {v['oos']['CAGR']:7.2%} / {v['oos']['Sharpe']:.4f} / {v['oos']['MaxDD']:7.2%}")
    P()

    # ----------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) THE BOOKS -- the record's modal REAL 4b-pass keys, rebuilt on their own panels")
    P("=" * 100)
    BOOKROWS, CAND, BKS, WTS = [], {}, {}, {}
    for pn, px in panels.items():
        pc = PC[pn]
        for cs, g in CLAIM_SETS.items():
            bks, cand = build_books(px, g)
            BKS[(pn, cs)] = bks
            CAND[(pn, cs)] = cand
            for bn, W in bks.items():
                wt = pc["ctx"].shift(W)
                WTS[(pn, cs, bn)] = wt
                gr, tn = pc["ctx"].run(wt)
                gross = pc["ctx"].gross(wt, pc["i0"])
                for c in COSTS:
                    m, mo, mi = score_stream(gr, tn, pc, c)
                    mb = pc["v2"][c]["full"]
                    BOOKROWS.append(dict(
                        panel=pn, claim_set=cs, book=bn, gross_nom=g, cost=c,
                        mean_gross=gross, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=m["H1"], H2=m["H2"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                        OOS_MaxDD=mo["MaxDD"], IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                        IS_MaxDD=mi["MaxDD"], IS_H1=mi["H1"], IS_H2=mi["H2"],
                        pass4b=pass4b(m, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"]),
                        pass4a=pass4a(m, mb),
                        fail4b=failstr(m, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"]),
                        turn=float(tn[pc["i0"]:].sum() / ((len(tn) - pc["i0"]) / 252.0))))
    books = pd.DataFrame(BOOKROWS)
    for cs in CLAIM_SETS:
        for c in (HEAD_COST, 10.0):
            sub = books[(books.claim_set == cs) & (books.cost == c)]
            P(f"  claim set {cs} (gross {CLAIM_SETS[cs]:.2f}), cost {c:.0f} bps  -- "
              f"4b passes {int(sub.pass4b.sum())} of {len(sub)}, "
              f"4a passes {int(sub.pass4a.sum())} of {len(sub)}")
            for _, r in sub.iterrows():
                P(f"     {r.panel:9s} {r.book:7s} g~{r.mean_gross:4.2f}  "
                  f"{r.CAGR:7.2%} / {r.Sharpe:6.3f} / {r.MaxDD:7.2%}  "
                  f"halves {r.H1:5.2f}/{r.H2:5.2f}  OOS {r.OOS_Sharpe:5.2f}  "
                  f"4b {'PASS' if r.pass4b else 'FAIL(' + r.fail4b + ')':22s} "
                  f"4a {'PASS' if r.pass4a else 'fail'}  turn {r.turn:5.2f}x")
        P()
    dump(books, "books")

    # ----------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) THE NULLS -- gross-matched coin flips, and the base rate each book must clear")
    P("=" * 100)
    FAM = {"TOP5": ("ROT", 5), "TOP10": ("ROT", 10), "TOP20": ("ROT", 20),
           "EWELIG": ("EW", None), "BAND03": ("BD", None)}
    NULLROWS, DRAWROWS = [], []
    for pn, px in panels.items():
        pc = PC[pn]
        for cs, g in CLAIM_SETS.items():
            gen = null_streams(pc["ctx"], px, CAND[(pn, cs)], DRAWS)
            for bn, (kind, k) in FAM.items():
                t0 = time.time()
                pv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                iv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                sv = {c: np.zeros(DRAWS) for c in COSTS}
                cv = {c: np.zeros(DRAWS) for c in COSTS}
                dv = {c: np.zeros(DRAWS) for c in COSTS}
                ov = {c: np.zeros(DRAWS) for c in COSTS}
                isv = {c: np.zeros(DRAWS) for c in COSTS}
                gsum = 0.0
                for d, W in gen(kind, WTS[(pn, cs, bn)], k):
                    gr, tn = pc["ctx"].run(W)
                    gsum += pc["ctx"].gross(W, pc["i0"])
                    for c in COSTS:
                        m, mo, mi = score_stream(gr, tn, pc, c)
                        pv[c][d] = pass4b(m, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"])
                        iv[c][d] = pass4b_is(mi, pc["spy_is"])
                        sv[c][d], cv[c][d], dv[c][d] = m["Sharpe"], m["CAGR"], m["MaxDD"]
                        ov[c][d], isv[c][d] = mo["Sharpe"], mi["Sharpe"]
                mg_null = gsum / DRAWS
                brow = books[(books.panel == pn) & (books.claim_set == cs) &
                             (books.book == bn)]
                mg_book = float(brow.mean_gross.iloc[0])
                gmatch = abs(mg_null - mg_book)
                for c in COSTS:
                    b = brow[brow.cost == c].iloc[0]
                    for nd in DRAW_GRID:
                        base = float(pv[c][:nd].mean())
                        pct_s = float((sv[c][:nd] < b.Sharpe).mean())
                        pct_c = float((cv[c][:nd] < b.CAGR).mean())
                        pct_d = float((np.abs(dv[c][:nd]) > abs(b.MaxDD)).mean())
                        pct_o = float((ov[c][:nd] < b.OOS_Sharpe).mean())
                        p_emp = float((1 + (sv[c][:nd] >= b.Sharpe).sum()) / (1 + nd))
                        NULLROWS.append(dict(
                            panel=pn, claim_set=cs, book=bn, null=kind, gross_nom=g, cost=c,
                            draws=nd, null_base_rate_4b=base,
                            is_base_rate_4b=float(iv[c][:nd].mean()),
                            book_pass4b=bool(b.pass4b),
                            outside_null=bool(b.pass4b and base <= BASE_RATE_BAR),
                            pct_Sharpe=pct_s, pct_CAGR=pct_c, pct_MaxDD=pct_d,
                            pct_OOS_Sharpe=pct_o, p_emp_Sharpe=p_emp,
                            null_mean_Sharpe=float(sv[c][:nd].mean()),
                            null_p95_Sharpe=float(np.quantile(sv[c][:nd], 0.95)),
                            book_Sharpe=float(b.Sharpe), book_CAGR=float(b.CAGR),
                            book_MaxDD=float(b.MaxDD), mean_gross_null=mg_null,
                            mean_gross_book=mg_book, gross_match=gmatch))
                    if c == HEAD_COST:
                        for d in range(DRAWS):
                            DRAWROWS.append(dict(panel=pn, claim_set=cs, book=bn, draw=d,
                                                 pass4b=bool(pv[c][d]),
                                                 Sharpe=sv[c][d], CAGR=cv[c][d],
                                                 MaxDD=dv[c][d], OOS_Sharpe=ov[c][d],
                                                 IS_Sharpe=isv[c][d]))
                P(f"  {pn:9s} {cs:4s} {bn:7s} null={kind:3s}  gross book {mg_book:.3f} vs "
                  f"null {mg_null:.3f} (|d| {gmatch:.4f})   "
                  f"4b base rate @0bps {float(pv[0.0].mean()):6.1%}  @10bps "
                  f"{float(pv[10.0].mean()):6.1%}   [{time.time() - t0:.0f}s]")
        P()
    nulls = pd.DataFrame(NULLROWS)
    draws_df = pd.DataFrame(DRAWROWS)
    dump(nulls, "nulls")
    dump(draws_df, "draws")

    g5 = float(nulls.gross_match.max())
    gk["G5"] = g5 < 0.01
    P(f"  G5 gross match, worst over all {nulls[['panel','claim_set','book']].drop_duplicates().shape[0]} "
      f"(panel,claim set,book) families: {g5:.4f}  {'PASS' if gk['G5'] else 'FAIL'}")
    nest_ok = True
    for (pn, cs, bn), gdf in draws_df.groupby(["panel", "claim_set", "book"]):
        v = gdf.sort_values("draw").pass4b.values
        for nd in DRAW_GRID:
            want = float(v[:nd].mean())
            got = float(nulls[(nulls.panel == pn) & (nulls.claim_set == cs) &
                              (nulls.book == bn) & (nulls.cost == HEAD_COST) &
                              (nulls.draws == nd)].null_base_rate_4b.iloc[0])
            nest_ok &= abs(want - got) == 0.0
    gk["G9"] = nest_ok
    P(f"  G9 nesting: the 250/500 base rates are prefixes of the same 1000 draw streams  "
      f"{'PASS' if nest_ok else 'FAIL'}")
    P()

    # ----------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) THE ANSWER -- how many committed 4b passers sit OUTSIDE their own zero-cost null")
    P("=" * 100)
    for cs in CLAIM_SETS:
        for c in COSTS:
            sub = nulls[(nulls.claim_set == cs) & (nulls.cost == c) &
                        (nulls.draws == DRAWS)]
            npass = int(sub.book_pass4b.sum())
            nout = int(sub.outside_null.sum())
            P(f"  claim set {cs} @ {c:4.0f} bps, {DRAWS} draws:  4b passes {npass:2d} of "
              f"{len(sub)}   OUTSIDE their null (base rate <= {BASE_RATE_BAR:.2f}) "
              f"{nout:2d}   median null base rate {sub.null_base_rate_4b.median():6.1%}")
        P()
    P(f"  per-cell detail at the queue's own cost rung ({HEAD_COST:.0f} bps), {DRAWS} draws:")
    P(f"     {'panel':9s} {'set':4s} {'book':7s} {'4b':4s} {'base rate':>9s} {'pct(Sh)':>8s} "
      f"{'pct(CAGR)':>9s} {'pct(DD)':>8s} {'pct(OOS)':>9s} {'p_emp':>7s}  outside?")
    for _, r in nulls[(nulls.cost == HEAD_COST) & (nulls.draws == DRAWS)].iterrows():
        P(f"     {r.panel:9s} {r.claim_set:4s} {r.book:7s} "
          f"{'PASS' if r.book_pass4b else 'fail':4s} {r.null_base_rate_4b:9.1%} "
          f"{r.pct_Sharpe:8.1%} {r.pct_CAGR:9.1%} {r.pct_MaxDD:8.1%} {r.pct_OOS_Sharpe:9.1%} "
          f"{r.p_emp_Sharpe:7.3f}  {'YES' if r.outside_null else 'no'}")
    P()
    P("  draw-axis convergence of the 4b base rate (0 bps, binding panel U56):")
    for cs in CLAIM_SETS:
        for bn in FAM:
            row = [float(nulls[(nulls.panel == BINDING_PANEL) & (nulls.claim_set == cs) &
                               (nulls.book == bn) & (nulls.cost == HEAD_COST) &
                               (nulls.draws == nd)].null_base_rate_4b.iloc[0])
                   for nd in DRAW_GRID]
            P(f"     {cs:4s} {bn:7s}  " +
              "  ".join(f"n={nd}: {v:6.1%}" for nd, v in zip(DRAW_GRID, row)))
    P()

    # RANDFIX secondary null, binding cell only
    P("  SECONDARY NULL (RANDFIX, binding cell U56/TOP20 only, never mixed into a headline):")
    for cs, g in CLAIM_SETS.items():
        pc = PC[BINDING_PANEL]
        cand = CAND[(BINDING_PANEL, cs)]
        pvf = {c: np.zeros(DRAWS, bool) for c in COSTS}
        svf = {c: np.zeros(DRAWS) for c in COSTS}
        for d, W in randfix_stream(pc["ctx"], panels[BINDING_PANEL], cand, g, 20, DRAWS):
            gr, tn = pc["ctx"].run(W)
            for c in COSTS:
                m, mo, mi = score_stream(gr, tn, pc, c)
                pvf[c][d] = pass4b(m, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"])
                svf[c][d] = m["Sharpe"]
        b = books[(books.panel == BINDING_PANEL) & (books.claim_set == cs) &
                  (books.book == "TOP20") & (books.cost == HEAD_COST)].iloc[0]
        P(f"     {cs:4s} g={g:.2f}  RANDFIX 4b base rate @0bps {float(pvf[0.0].mean()):6.1%} "
          f"@10bps {float(pvf[10.0].mean()):6.1%}   TOP20 Sharpe percentile "
          f"{float((svf[0.0] < b.Sharpe).mean()):6.1%}")
    P()

    # ----------------------------------------------------------------------------------
    P("=" * 100)
    P("(G) RULE 8 WALK-FORWARD -- parameters chosen on 2009-2016 only, OOS 2017-2026 read once")
    P("=" * 100)
    P("  Three IS-only choosers over the 5 books x 2 claim sets on each panel:")
    P("    CH_SHARPE   best IS Sharpe                       (no base-rate clause)")
    P("    CH_4bIS     best IS Sharpe among books passing the IS 4b LEVEL legs")
    P("    CH_BASE     best IS Sharpe among books whose IS-window 4b base rate <= 0.05")
    P("                (the clause this run exists to price)")
    WF = []
    for pn, px in panels.items():
        pc = PC[pn]
        isb = draws_df[draws_df.panel == pn]
        for c in COSTS:
            cand = books[(books.panel == pn) & (books.cost == c)].copy()
            # CH_BASE must be IS-only: it uses `is_base_rate_4b`, the null's pass share on the
            # 2009-2016 window's own 4b LEVEL legs at the SAME cost.  The full-sample
            # `null_base_rate_4b` is carried alongside for reporting only and is NEVER used to
            # choose -- it reads the OOS window and would be look-ahead.
            br = nulls[(nulls.panel == pn) & (nulls.cost == c) & (nulls.draws == DRAWS)]
            cand = cand.merge(br[["claim_set", "book", "null_base_rate_4b",
                                  "is_base_rate_4b"]],
                              on=["claim_set", "book"], how="left")
            cand["IS_ok"] = (cand.IS_H1 > pc["spy_is"]["H1"]) & \
                            (cand.IS_H2 > pc["spy_is"]["H2"]) & \
                            (cand.IS_CAGR >= 0.70 * pc["spy_is"]["CAGR"]) & \
                            (cand.IS_MaxDD.abs() <= 0.60 * abs(pc["spy_is"]["MaxDD"]))
            picks = {}
            picks["CH_SHARPE"] = cand.sort_values("IS_Sharpe", ascending=False).iloc[0]
            s4 = cand[cand.IS_ok].sort_values("IS_Sharpe", ascending=False)
            picks["CH_4bIS"] = s4.iloc[0] if len(s4) else None
            sb = cand[cand.is_base_rate_4b <= BASE_RATE_BAR].sort_values(
                "IS_Sharpe", ascending=False)
            picks["CH_BASE"] = sb.iloc[0] if len(sb) else None
            for ch, r in picks.items():
                if r is None:
                    WF.append(dict(panel=pn, cost=c, chooser=ch, pick="EMPTY"))
                    continue
                v2o = pc["v2"][c]["oos"]
                so = pc["spy_oos"]
                oos_pass4b = bool(r.OOS_Sharpe > so["Sharpe"] and
                                  abs(r.OOS_MaxDD) <= 0.60 * abs(so["MaxDD"]) and
                                  r.OOS_CAGR >= 0.70 * so["CAGR"])
                oos_pass4a = bool(r.OOS_Sharpe > v2o["Sharpe"] and
                                  r.OOS_MaxDD >= v2o["MaxDD"])
                WF.append(dict(panel=pn, cost=c, chooser=ch,
                               pick=f"{r.claim_set}/{r.book}", IS_Sharpe=r.IS_Sharpe,
                               base_rate=r.null_base_rate_4b,
                               is_base_rate=r.is_base_rate_4b,
                               OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                               OOS_MaxDD=r.OOS_MaxDD, OOS_4b=oos_pass4b, OOS_4a=oos_pass4a,
                               SPY_OOS_CAGR=so["CAGR"], SPY_OOS_Sharpe=so["Sharpe"],
                               SPY_OOS_MaxDD=so["MaxDD"], V2_OOS_CAGR=v2o["CAGR"],
                               V2_OOS_Sharpe=v2o["Sharpe"], V2_OOS_MaxDD=v2o["MaxDD"]))
    wf = pd.DataFrame(WF)
    dump(wf, "walkforward")
    for pn in panels:
        P(f"  {pn}:")
        for _, r in wf[wf.panel == pn].iterrows():
            if r["pick"] == "EMPTY":
                P(f"     {r.cost:4.0f} bps  {r.chooser:10s}  IS set EMPTY -- no pick")
                continue
            P(f"     {r.cost:4.0f} bps  {r.chooser:10s}  pick {r['pick']:12s} "
              f"(IS Sh {r.IS_Sharpe:5.2f}, IS base rate {r.is_base_rate:5.1%}, "
              f"full-sample base rate {r.base_rate:5.1%})  OOS "
              f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:5.3f} / {r.OOS_MaxDD:7.2%}   "
              f"4b {'PASS' if r.OOS_4b else 'fail'}  4a {'PASS' if r.OOS_4a else 'fail'}   "
              f"[SPY {r.SPY_OOS_CAGR:6.2%}/{r.SPY_OOS_Sharpe:5.3f}/{r.SPY_OOS_MaxDD:7.2%}"
              f" | v2 {r.V2_OOS_CAGR:6.2%}/{r.V2_OOS_Sharpe:5.3f}/{r.V2_OOS_MaxDD:7.2%}]")
    live = wf[wf["pick"] != "EMPTY"]
    P()
    P(f"  rule-8 totals: 4b {int(live.OOS_4b.sum())} of {len(live)} live picks, "
      f"4a {int(live.OOS_4a.sum())} of {len(live)}   (EMPTY on {int((wf['pick'] == 'EMPTY').sum())})")
    P()

    P("=" * 100)
    P("(H) GATES")
    P("=" * 100)
    for k in sorted(gk):
        P(f"  {k}: {'PASS' if gk[k] else 'FAIL'}")
    P(f"  {sum(gk.values())} of {len(gk)} pass")
    P()
    P(f"total runtime {time.time() - t_start:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
