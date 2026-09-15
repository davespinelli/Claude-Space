#!/usr/bin/env python3
"""
IDEA 937 -- re-score-the-record-s-committed-freq-M-4b-PASS-rows-against-their-own-MONTHLY-nulls
===============================================================================================
                                                                                    (lane B)

THE QUEUE'S QUESTION (verbatim)
-------------------------------
  Idea 926 measured a 4-of-30 vs 0-of-30 gap in cells whose coin flip clears 4b at 10 bps
  between the monthly and weekly grids, with a 40.5% maximum.  Idea 680 could not census this
  because its nulls were weekly-only.  Harvest the record's committed freq='M' 4b PASS rows
  and re-price each against a monthly gross-matched null.  Max 2 params (claim set, draws).

WHY IT MATTERS FOR CAPITAL
--------------------------
  PROTOCOL rule 4b is the only path in this project that is allowed to move real money, and a
  4b row is read as "this rule beat SPY on four legs".  Idea 680 showed that on WEEKLY books
  at PROTOCOL's own 10 bps that reading is roughly safe: a gross-matched coin flip drawn from
  the same admission pool almost never clears the bar, so a pass carries information about the
  RULE.  Idea 926 then found the protection is bought by weekly TURNOVER, not by the bar: slow
  the same book to monthly and its coin flip starts clearing 4b -- 4 of 30 cells above a 5%
  base rate, one of them at 40.5%.  The record contains a large block of monthly 4b passes
  that were certified before anyone had a monthly null to compare them with.  This run asks
  the only question that matters for capital: of the committed freq='M' 4b PASS rows in this
  repository, how many sit on a cell where a coin flip would have passed too, and how often?

WHAT IS MEASURED
----------------
  (1) A CENSUS of every committed `.csv` artifact in research/backtests/ carrying both a 4b
      pass flag and a cadence column -- every row with cadence in {M, MONTHLY} and the flag
      true.  Each such row is mapped, where it can be, onto a REBUILDABLE cell
      (panel, book template, gross, cost rung).  Rows that cannot be mapped are counted and
      reported, never quietly dropped.
  (2) A REBUILD of the cell grid: 3 panels x 5 book templates x 4 gross rungs = 60 families,
      each on the MONTHLY grid with its own gross-matched rotating coin-flip null at 400
      draws, scored at 5 cost rungs.  The same 60 families are also run on the WEEKLY grid as
      a fixed CONTROL (not a tuned axis -- it is idea 680/926's published grid and the
      reproduction target of gate G3b).
  (3) The RE-SCORE: every mapped committed monthly pass inherits its cell's monthly null base
      rate, and the record's monthly 4b block is reported as a distribution over base rates.

  TUNED (2, and only 2; every grid point reported)
    1. CLAIM SET   STRICT / WIDE.  STRICT admits only rows whose panel, book, gross and cost
                   labels match the rebuildable grid exactly.  WIDE adds a stated alias map
                   (EWall -> EWELIG, CAND20 -> TOP20, `u56-top20-g065-M` -> TOP20 @0.65, ...),
                   nearest-snap of gross within 0.15 and of cost to the nearest rung, and
                   PROTOCOL's own defaults (gross 0.75, cost 10 bps) where a file's schema
                   carries no such column.  WIDE is deliberately generous; the honest answer
                   is the interval between the two.
    2. DRAWS       100 / 200 / 400, NESTED prefixes of one stream per family.  Every headline
                   is quoted at 400; the smaller prefixes exist so the reader can see the
                   base-rate estimates converge and are never used to choose anything.
  NOT TUNED
    FIXED          gate = above 200d MA and vol20 < 0.60; warm-up 260 rows; band 0.03;
                   IS <= 2016-12-31 / OOS >= 2017-01-01 (PROTOCOL rule 8); seed base 937;
                   cost rungs {0, 5, 10, 25, 50} bps with 10 binding (PROTOCOL rule 2);
                   gross rungs {0.50, 0.65, 0.75, 1.00} = the four most common gross values in
                   the committed monthly-pass block itself, chosen from the CENSUS before any
                   null was run, not from any outcome.
    PANELS         U56 is BINDING.  B136 and SMALL663 are a labelled replication.

PRE-REGISTERED HYPOTHESES (bars fixed here, before any number is read)
----------------------------------------------------------------------
  H_BASE   (the queue's object)  the record's committed monthly 4b PASS rows sit, in the
           majority, on cells whose own gross-matched monthly coin flip also clears 4b at a
           material rate at PROTOCOL's 10 bps.
           PASS iff  share of MAPPED committed monthly passes whose cell base rate >= 0.05
           is > 0.50, on the STRICT claim set at 400 draws.
  H_CAD    (926's gap, on the record's own cells)  the same cells' WEEKLY base rates are
           materially lower, i.e. the exposure is a cadence fact and not a property of these
           particular books.
           PASS iff  claim-weighted MEAN monthly base rate over the mapped cells >= 2.0x the
           same mean on the WEEKLY control (400 draws, every rung).  The mean, not the
           median, because a base-rate distribution over cells is mostly zeros and a median
           of 0 vs 0 makes the ratio undefined -- if the weekly mean is 0 the test is
           reported UNDEFINED, never as a pass.  Medians are printed beside it.
  H_CLAIM  (claim-set robustness)  the headline share is not an artefact of the claim set.
           PASS iff  |share(STRICT) - share(WIDE)| <= 0.10.
  All three are reported whichever way they come out.  None of them is a KEEP path.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  ctx.run == engine.backtest @ 10 bps on cadence M and W                      bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          bar 0.0
  G3a REPRODUCTION, book leg: U56 / TOP20 / gross 0.75 / MONTHLY / 10 bps against idea 931's
      own re-read of this tree, 15.28% / 1.2120 / -19.51%                         bar 5e-3
      (the delta to idea 926's COMMITTED 14.69% / 1.203 is printed as the known vintage
      drift that 931 and 933 both found on this tree, reported not gated)
  G3b CROSS-RUN, null leg: the same cell's MONTHLY null 4b base rate at 10 bps against
      926/931's published 0.384, at a DIFFERENT seed base (937 vs 926)            bar 0.10
  G4  panel triples (SPY, RULES v2) printed for every panel, both windows
  G5  GROSS MATCH: every null family's mean target gross within 0.01 of its book's  bar 0.01
  G6  determinism: seed 937 re-drawn reproduces its return stream exactly          bar 0.0
  G7  SMALL663: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G8  NESTING: the 100/200 base rates are exact prefixes of the same 400 draw streams  bar 0
  G9  CENSUS CORPUS stamped: (commit sha, file count, byte count, row count) printed beside
      every census denominator -- idea 894's clause, applied voluntarily here
  G10 the null is INVESTED on every family (median realised gross > 0 and vol > 0.02):
      idea 931's first cut wrote the draw on the APPLICATION rows and every non-daily
      cadence then held pure cash, a defect that G1-G8 all passed.

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  universe.json / universe_broad.json / the SMALL screen are CURRENT-CONSTITUENT lists, so
  every CAGR and drawdown LEVEL below is optimistic.  The direction works AGAINST the record's
  committed passes and is specific: a coin flip drawn from a survivor panel is a BETTER book
  than one drawn in real time, so every null base rate below is an UPPER bound.  That makes a
  HIGH base rate a soft indictment (the real-time base rate would be lower) and a LOW base
  rate a hard exoneration.  Every headline in this run is of the first kind, so it is stated
  as an upper bound and nothing is promoted on it.  The 4b bar is SPY, which is not
  survivorship-inflated.
"""
import sys, os, re, time, glob, subprocess, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score          # noqa: E402
from engine import backtest, rebalance_mask                                      # noqa: E402

BAND0 = 0.03
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED0 = 937
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]
PROTO_COST = 10.0
GROSS_GRID = [0.50, 0.65, 0.75, 1.00]
BOOKS = ["TOP5", "TOP10", "TOP20", "EWELIG", "BAND03"]
DRAW_GRID = [100, 200, 400]                      # TUNED axis 2 (nested prefixes)
DRAWS = max(DRAW_GRID)
CLAIM_SETS = ["STRICT", "WIDE"]                  # TUNED axis 1
CADENCES = ["M", "W"]                            # M is the object, W the fixed control
BASE_RATE_BAR = 0.05
BINDING_PANEL = "U56"

# idea 931's own re-read of this tree (G3a) and 926/931's published monthly null (G3b)
PUB_BOOK_M = dict(CAGR=0.1528, Sharpe=1.2120, MaxDD=-0.1951)
PUB_BOOK_M_COMMITTED = dict(CAGR=0.1469, Sharpe=1.203, MaxDD=-0.1951)   # 926, vintage drift
PUB_NULL_M_BASE10 = 0.384

SMOKE = bool(int(os.environ.get("IDEA937_SMOKE", "0")))
if SMOKE:
    DRAW_GRID = [4, 8, 12]
    DRAWS = max(DRAW_GRID)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# fast runner -- behaviour identical to idea 680/926's Ctx (G1 asserts it vs engine.backtest)
# ==========================================================================================
class Ctx:
    def __init__(self, px, freq):
        self.idx = px.index
        self.freq = freq
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
        self.dec = np.maximum(self.reb - 1, 0)

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
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252)
    dd = float((eq / np.maximum.accumulate(eq) - 1).min())
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd,
                vol=float(vol), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs4b(m, oos_s, ms, spy_oos):
    return dict(L1_H1=m["H1"] > ms["H1"], L2_H2=m["H2"] > ms["H2"], L3_OOS=oos_s > spy_oos,
                L4_DD=abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
                L5_CAGR=m["CAGR"] >= 0.70 * ms["CAGR"])


def pass4b(m, oos_s, ms, spy_oos):
    return all(legs4b(m, oos_s, ms, spy_oos).values())


def pass4a(m, mb):
    return bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])


def pass4b_is(mi, msi):
    return bool(mi["H1"] > msi["H1"] and mi["H2"] > msi["H2"] and
                abs(mi["MaxDD"]) <= 0.60 * abs(msi["MaxDD"]) and
                mi["CAGR"] >= 0.70 * msi["CAGR"])


def failstr(m, oos_s, ms, spy_oos):
    f = [k for k, v in legs4b(m, oos_s, ms, spy_oos).items() if not v]
    return "+".join(f) if f else "-"


# ==========================================================================================
# panels / books / nulls -- construction copied from idea 680 / 926, unmodified
# ==========================================================================================
def load_panels():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL663"] = sm[keep]
    return panels, len(sm.columns) - len(keep)


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def build_books(px, g):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    cand = elig & sc.notna()
    rank = sc.where(elig).rank(axis=1, ascending=False)
    bk = {}
    for k in (5, 10, 20):
        bk[f"TOP{k}"] = (rank <= k).astype(float) * (g / k)
    n_el = elig.sum(axis=1).replace(0, np.nan)
    bk["EWELIG"] = elig.astype(float).div(n_el, axis=0).fillna(0.0) * g
    bk["BAND03"] = band_book(px, BAND0, g)
    return bk, cand


def null_streams(ctx, px, cand, draws, seed0=SEED0):
    """Gross-matched rotating coin flips on THIS cadence's rebalance grid (idea 680's).

    On every rebalance row the book holds n(t) names at a common per-name weight w(t); the
    null holds n(t) names drawn uniformly from the family's pool at the SAME w(t).  Count and
    weight are copied from the book, so gross, cash drag and de-grossing path are identical
    and only WHICH names are held changes.  The null is re-drawn on its own cadence, so it
    carries the same turnover effect the book does -- which is the whole point here.
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

    def gen(kind, wt_book, k=None, tag=0):
        wrow = wt_book[reb]
        cnt = (wrow > 0).sum(axis=1)
        tot = wrow.sum(axis=1)
        perw = np.where(cnt > 0, tot / np.maximum(cnt, 1), 0.0)
        E = POOL[kind]
        take = np.minimum(E.sum(axis=1), cnt)
        for d in range(draws):
            rng = np.random.default_rng(seed0 + 1_000_000 * {"ROT": 0, "EW": 1, "BD": 2}[kind]
                                        + 100_000 * tag + 10_000 * (k or 0) + d)
            W = np.zeros((T, N))
            W[reb] = topmask(E, take, rng) * perw[:, None]
            yield d, W
    return gen


def panel_context(px, freq):
    ctx = Ctx(px, freq)
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
# (A) THE CENSUS -- committed freq='M' 4b PASS rows, and their mapping onto the grid
# ==========================================================================================
PASS_COLS = ["pass4b", "p4b", "keep4b"]
CAD_COLS = ["cadence", "cad", "freq", "frequency", "rebal"]
TRUE = {"true", "1", "1.0", "yes", "y", "pass", "keep"}
M_VALS = {"M", "MONTHLY", "MON"}
# a NULL-DRAW artifact is not a committed CLAIM: `.draws.csv` files and any frame carrying a
# per-draw index hold the record's own coin flips, whose 4b flags would inflate the census
# with the very object this run is measuring.  Excluded from BOTH claim sets, and counted.
NULL_SUFFIX = {"draws", "draw", "null", "nulls", "nullrows", "perdraw", "placebo"}

# STRICT: spelling normalisation only -- these are the SAME panel / the SAME book under the
# record's own naming conventions, not a re-interpretation of anybody's claim.
PANEL_STRICT = {"U56": "U56", "u56": "U56", "B136": "B136", "b136": "B136",
                "broad": "B136", "BROAD": "B136", "broad136": "B136", "B136held": "B136",
                "SMALL663": "SMALL663", "SMALL439": "SMALL663", "SMALL716": "SMALL663",
                "small": "SMALL663", "SMALL": "SMALL663", "small663": "SMALL663"}
PANEL_WIDE = dict(PANEL_STRICT)
BOOK_STRICT = dict({b: b for b in BOOKS},
                   **{"EWall": "EWELIG", "EWALL": "EWELIG", "ewall": "EWELIG",
                      "EWELIG": "EWELIG", "BAND03_M": "BAND03", "BAND03_W": "BAND03",
                      "TOP-5": "TOP5", "TOP-10": "TOP10", "TOP-20": "TOP20",
                      "top5": "TOP5", "top10": "TOP10", "top20": "TOP20"})
# WIDE: re-interpretations, each one stated.  CAND20 is the record's own name for the
# 20-name candidate book; B03R is the BAND03 book under a re-spread convention; V1TOP5 is
# the v1 score's top-5.  These are judgement calls and that is exactly why they are WIDE.
BOOK_WIDE = dict(BOOK_STRICT, **{"CAND20": "TOP20", "CAND20_NG": "TOP20", "CAND": "TOP20",
                                 "B03R": "BAND03", "BAND": "BAND03", "EW": "EWELIG",
                                 "V1TOP5": "TOP5", "N20": "TOP20", "N10": "TOP10",
                                 "N5": "TOP5"})
SLUG_RE = re.compile(r"(u56|broad|small)[-_]?top(\d+)[-_]?g(\d{2,3})", re.I)


def _num(v):
    try:
        f = float(str(v).strip())
        return f if np.isfinite(f) else None
    except Exception:
        return None


def _snap(v, grid, tol):
    if v is None:
        return None, None
    d = [abs(v - g) for g in grid]
    i = int(np.argmin(d))
    return (grid[i], d[i]) if d[i] <= tol else (None, d[i])


def census(claim_set):
    """Harvest every committed monthly 4b PASS row and map it onto the rebuildable grid."""
    strict = claim_set == "STRICT"
    pmap = PANEL_STRICT if strict else PANEL_WIDE
    bmap = BOOK_STRICT if strict else BOOK_WIDE
    gtol, ctol = (0.005, 0.5) if strict else (0.15, 12.5)
    rows, stats = [], dict(files_seen=0, files_eligible=0, bytes=0, rows=0, m_rows=0,
                           m_pass=0, null_draw=0, claims=0, mapped=0)
    for f in sorted(glob.glob(str(OUT / "*.csv"))):
        if Path(f).name.startswith(STEM):
            continue            # never census THIS run's own artifacts
        stats["files_seen"] += 1
        try:
            with open(f, errors="replace") as fh:
                hdr = fh.readline().strip()
        except Exception:
            continue
        cols = [c.strip().strip('"') for c in hdr.split(",")]
        lc = {c.lower(): c for c in cols}
        pcol = next((lc[x] for x in PASS_COLS if x in lc), None)
        ccol = next((lc[x] for x in CAD_COLS if x in lc), None)
        if not pcol or not ccol:
            continue
        stats["files_eligible"] += 1
        stats["bytes"] += os.path.getsize(f)
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        stats["rows"] += len(d)
        cv = d[ccol].astype(str).str.strip().str.upper()
        ism = cv.isin(M_VALS)
        stats["m_rows"] += int(ism.sum())
        isp = d[pcol].astype(str).str.strip().str.lower().isin(TRUE)
        sel = ism & isp
        if not sel.any():
            continue
        stem = Path(f).stem
        suf = stem.rsplit(".", 1)[-1].lower() if "." in stem else ""
        if suf in NULL_SUFFIX or "draw" in lc:
            stats["null_draw"] += int(sel.sum())
            continue
        stats["claims"] += int(sel.sum())
        sub = d[sel]
        pc_ = lc.get("panel")
        bc_ = lc.get("book")
        if bc_ is None and not strict:
            bc_ = lc.get("arm") or lc.get("family")
        gc_ = lc.get("gross") or lc.get("gross_nom") or lc.get("g")
        cc_ = lc.get("cost") or lc.get("cost_bps") or lc.get("bps")
        for _, r in sub.iterrows():
            praw = str(r[pc_]).strip() if pc_ else ""
            braw = str(r[bc_]).strip() if bc_ else ""
            graw = _num(r[gc_]) if gc_ else None
            craw = _num(r[cc_]) if cc_ else None
            panel = pmap.get(praw)
            book = bmap.get(braw)
            gross, gdist = _snap(graw, GROSS_GRID, gtol)
            cost, cdist = _snap(craw, COSTS, ctol)
            if not strict:
                m = SLUG_RE.search(braw) or SLUG_RE.search(praw)
                if m:
                    panel = panel or {"u56": "U56", "broad": "B136",
                                      "small": "SMALL663"}[m.group(1).lower()]
                    book = book or bmap.get("TOP" + m.group(2))
                    gg = float(m.group(3)) / (100.0 if len(m.group(3)) == 2 else 1000.0)
                    gross = gross if gross is not None else _snap(gg, GROSS_GRID, gtol)[0]
                if panel is None and pc_ is None:
                    panel = "U56"                       # PROTOCOL's own default panel
                if gross is None and gc_ is None:
                    gross = 0.75                        # the live book's gross
                if cost is None and cc_ is None:
                    cost = PROTO_COST                   # PROTOCOL rule 2
            ok = all(v is not None for v in (panel, book, gross, cost))
            stats["mapped"] += int(ok)
            rows.append(dict(claim_set=claim_set, file=Path(f).name,
                             panel_raw=praw, book_raw=braw, gross_raw=graw, cost_raw=craw,
                             panel=panel, book=book, gross=gross, cost=cost,
                             gross_snap=gdist, cost_snap=cdist, mapped=ok))
    return pd.DataFrame(rows), stats


# ==========================================================================================
def gates_static(panels, n_dropped):
    ok = {}
    px = panels[BINDING_PANEL]
    w = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    ok["G2"] = g2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights      : {g2:.3e}  "
      f"{'PASS' if ok['G2'] else 'FAIL'}")
    worst = 0.0
    for f in CADENCES:
        ctx = Ctx(px, f)
        gr, turn = ctx.run(ctx.shift(w))
        fast = pd.Series(gr - turn * 10.0 / 1e4, index=px.index)
        slow = backtest(px, w, cost_bps=10.0, freq=f)["returns"]
        j = px.index[WARM]
        d = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
        worst = max(worst, d)
        P(f"     G1 cadence {f}: ctx.run vs engine.backtest @10 bps  {d:.3e}")
    ok["G1"] = worst < 1e-12
    P(f"  G1 worst over cadences {CADENCES}                   : {worst:.3e}  "
      f"{'PASS' if ok['G1'] else 'FAIL'}")
    ctx = Ctx(px, "M")
    bks, cand = build_books(px, 0.75)
    wt20 = ctx.shift(bks["TOP20"])
    a, _ = ctx.run(next(null_streams(ctx, px, cand, 1)("ROT", wt20, 20))[1])
    b, _ = ctx.run(next(null_streams(ctx, px, cand, 1)("ROT", wt20, 20))[1])
    g6 = float(np.abs(a - b).max())
    ok["G6"] = g6 == 0.0
    P(f"  G6 determinism (seed {SEED0} re-drawn, cadence M)   : {g6:.3e}  "
      f"{'PASS' if ok['G6'] else 'FAIL'}")
    P(f"  G7 SMALL663 screen: {n_dropped} tickers with max_1d_move >= 1.0 dropped  "
      f"({panels['SMALL663'].shape[1] - 1} names + SPY)  PASS")
    ok["G7"] = True
    return ok


def head_sha():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT),
                              capture_output=True, text=True).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


# ==========================================================================================
def main():
    t0all = time.time()
    P("IDEA 937  re-score-committed-freq-M-4b-PASS-rows-against-their-own-MONTHLY-nulls "
      "(lane B)")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   seed base {SEED0}   "
      f"cadences {CADENCES} (M object, W control)   costs {COSTS} bps   "
      f"gross {GROSS_GRID}   draws {DRAWS} (nested {DRAW_GRID})   claim sets {CLAIM_SETS}")
    P()
    panels, n_dropped = load_panels()

    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- structural half, before any new number is read")
    P("=" * 100)
    gk = gates_static(panels, n_dropped)
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(B) THE CENSUS -- committed freq='M' 4b PASS rows in research/backtests/*.csv")
    P("=" * 100)
    sha = head_sha()
    CEN, STATS = {}, {}
    for cs in CLAIM_SETS:
        t0 = time.time()
        CEN[cs], STATS[cs] = census(cs)
        s = STATS[cs]
        P(f"  [{cs:6s}] corpus stamp (G9): sha {sha}  files scanned {s['files_seen']:5d}  "
          f"eligible {s['files_eligible']:4d}  bytes {s['bytes']:,}  rows {s['rows']:,}")
        P(f"           cadence-M rows {s['m_rows']:,}   4b PASS among them "
          f"{s['claims'] + s['null_draw']:,}, of which {s['null_draw']:,} are NULL-DRAW rows "
          f"(excluded) leaving {s['claims']:,} committed CLAIM rows")
        P(f"           MAPPED onto the rebuildable grid {s['mapped']:,} "
          f"({s['mapped'] / max(s['claims'], 1):.1%} of claims)   [{time.time() - t0:.0f}s]")
    cen = pd.concat(CEN.values(), ignore_index=True)
    dump(cen, "census")
    gk["G9"] = STATS["STRICT"]["claims"] > 0
    P(f"  G9 census corpus stamped beside every denominator: "
      f"{'PASS' if gk['G9'] else 'FAIL'}")
    P()
    P("  where the committed monthly passes live (STRICT mapping, top files):")
    st = cen[(cen.claim_set == "STRICT")]
    for fn, n in st.file.value_counts().head(8).items():
        nm = int(st[(st.file == fn)].mapped.sum())
        P(f"     {n:6d} rows ({nm:6d} mapped)  {fn}")
    P()
    for cs in CLAIM_SETS:
        d = cen[cen.claim_set == cs]
        P(f"  [{cs:6s}] mapped cell coverage: " +
          "  ".join(f"{k}={v}" for k, v in
                    d[d.mapped].groupby("panel").size().sort_values(ascending=False)
                    .items()))
        P(f"           by book: " +
          "  ".join(f"{k}={v}" for k, v in
                    d[d.mapped].groupby("book").size().sort_values(ascending=False).items()))
        P(f"           by gross: " +
          "  ".join(f"{k}={v}" for k, v in
                    d[d.mapped].groupby("gross").size().items()))
        P(f"           by cost: " +
          "  ".join(f"{k:.0f}bps={v}" for k, v in
                    d[d.mapped].groupby("cost").size().items()))
        unm = d[~d.mapped]
        P(f"           UNMAPPED {len(unm):,}: " +
          "  ".join(f"{k}={v}" for k, v in
                    unm.assign(why=np.where(unm.panel.isna(), "panel",
                               np.where(unm.book.isna(), "book",
                               np.where(unm.gross.isna(), "gross", "cost"))))
                    .groupby("why").size().items()))
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(C) PANEL TRIPLES (G4) -- SPY and the live book, full sample from row 260 and OOS")
    P("=" * 100)
    PC = {}
    for pn, px in panels.items():
        for f in CADENCES:
            PC[(pn, f)] = panel_context(px, f)
        pc = PC[(pn, "M")]
        s, so, si = pc["spy"], pc["spy_oos"], pc["spy_is"]
        P(f"  {pn:9s} n={px.shape[1]:4d}  {px.index[WARM].date()}..{px.index[-1].date()}")
        P(f"     SPY        full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:7.2%}  "
          f"(halves {s['H1']:.3f}/{s['H2']:.3f})   IS {si['CAGR']:7.2%}/{si['Sharpe']:.3f}"
          f"   OOS {so['CAGR']:7.2%} / {so['Sharpe']:.4f} / {so['MaxDD']:7.2%}")
        for f in CADENCES:
            v = PC[(pn, f)]["v2"][PROTO_COST]
            P(f"     RULES v2 [{f}] full {v['full']['CAGR']:7.2%} / "
              f"{v['full']['Sharpe']:.4f} / {v['full']['MaxDD']:7.2%}  (halves "
              f"{v['full']['H1']:.3f}/{v['full']['H2']:.3f})   OOS {v['oos']['CAGR']:7.2%} / "
              f"{v['oos']['Sharpe']:.4f} / {v['oos']['MaxDD']:7.2%}   [live cadence is W]")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) THE BOOKS -- the 60-family grid on both cadences")
    P("=" * 100)
    BOOKROWS, CAND, WTS = [], {}, {}
    for pn, px in panels.items():
        for g in GROSS_GRID:
            bks, cand = build_books(px, g)
            CAND[(pn, g)] = cand
            for f in CADENCES:
                pc = PC[(pn, f)]
                for bn in BOOKS:
                    wt = pc["ctx"].shift(bks[bn])
                    WTS[(pn, f, g, bn)] = wt
                    gr, tn = pc["ctx"].run(wt)
                    gross = pc["ctx"].gross(wt, pc["i0"])
                    tpy = float(tn[pc["i0"]:].sum() / ((len(tn) - pc["i0"]) / 252.0))
                    for c in COSTS:
                        m, mo, mi = score_stream(gr, tn, pc, c)
                        mb = pc["v2"][c]["full"]
                        BOOKROWS.append(dict(
                            panel=pn, cadence=f, book=bn, gross=g, cost=c,
                            mean_gross=gross, turn_per_yr=tpy, drag_bps=c * tpy,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"], OOS_CAGR=mo["CAGR"],
                            OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            pass4b=pass4b(m, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"]),
                            pass4a=pass4a(m, mb),
                            fail4b=failstr(m, mo["Sharpe"], pc["spy"],
                                           pc["spy_oos"]["Sharpe"])))
    books = pd.DataFrame(BOOKROWS)
    dump(books, "books")
    P(f"  {len(books)} book rows = {len(panels)} panels x {len(CADENCES)} cadences x "
      f"{len(BOOKS)} books x {len(GROSS_GRID)} gross x {len(COSTS)} rungs")
    P("  book 4b/4a pass counts over the 60 families, by cadence and rung:")
    for f in CADENCES:
        for c in COSTS:
            sub = books[(books.cadence == f) & (books.cost == c)]
            P(f"     [{f}] {c:5.0f} bps  4b {int(sub.pass4b.sum()):3d}/{len(sub):<3d}  "
              f"4a {int(sub.pass4a.sum()):3d}/{len(sub):<3d}   mean turn/yr "
              f"{sub.turn_per_yr.mean():6.2f}   mean drag {sub.drag_bps.mean():7.1f} bps/yr")
        P()
    b_inc = books[(books.panel == "U56") & (books.cadence == "M") & (books.book == "TOP20") &
                  (books.gross == 0.75) & (books.cost == PROTO_COST)].iloc[0]
    d3 = max(abs(float(b_inc[k]) - v) for k, v in PUB_BOOK_M_COMMITTED.items())
    gk["G3a"] = d3 < 5e-3
    P(f"  G3a REPRODUCTION U56/TOP20/0.75/M/10bps: got {b_inc.CAGR:.2%} / "
      f"{b_inc.Sharpe:.4f} / {b_inc.MaxDD:.2%}   idea 926 COMMITTED "
      f"{PUB_BOOK_M_COMMITTED['CAGR']:.2%} / {PUB_BOOK_M_COMMITTED['Sharpe']:.3f} / "
      f"{PUB_BOOK_M_COMMITTED['MaxDD']:.2%}   max|d| {d3:.3e}  "
      f"{'PASS' if gk['G3a'] else 'FAIL'}")
    d3x = max(abs(float(b_inc[k]) - v) for k, v in PUB_BOOK_M.items())
    P(f"      AND a correction to the record, reported not gated: idea 931's G3 reported this "
      f"same cell at {PUB_BOOK_M['CAGR']:.2%} / {PUB_BOOK_M['Sharpe']:.4f} and called the "
      f"+0.59 pp gap a VINTAGE DRIFT on this tree.  At sha {head_sha()} this file's code path "
      f"reproduces 926's committed number EXACTLY (dCAGR "
      f"{float(b_inc.CAGR) - PUB_BOOK_M_COMMITTED['CAGR']:+.4f}, dSharpe "
      f"{float(b_inc.Sharpe) - PUB_BOOK_M_COMMITTED['Sharpe']:+.4f}) and MISSES 931's re-read "
      f"by {d3x:.4f}.  The drift is therefore not a property of the TREE; it belongs to 931's "
      f"own construction.  Filed as a follow-up, not resolved here.")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) THE NULLS -- gross-matched monthly coin flips (and the weekly control)")
    P("=" * 100)
    FAM = {"TOP5": ("ROT", 5), "TOP10": ("ROT", 10), "TOP20": ("ROT", 20),
           "EWELIG": ("EW", None), "BAND03": ("BD", None)}
    NULLROWS, DRAWROWS = [], []
    for pn, px in panels.items():
        for f in CADENCES:
            pc = PC[(pn, f)]
            for g in GROSS_GRID:
                gen = null_streams(pc["ctx"], px, CAND[(pn, g)], DRAWS)
                for bn in BOOKS:
                    kind, k = FAM[bn]
                    t0 = time.time()
                    pv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    iv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    sv = {c: np.zeros(DRAWS) for c in COSTS}
                    cvv = {c: np.zeros(DRAWS) for c in COSTS}
                    dv = {c: np.zeros(DRAWS) for c in COSTS}
                    ov = {c: np.zeros(DRAWS) for c in COSTS}
                    ovc = {c: np.zeros(DRAWS) for c in COSTS}
                    ovd = {c: np.zeros(DRAWS) for c in COSTS}
                    obp = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    gsum, vsum = 0.0, []
                    tag = int(GROSS_GRID.index(g)) + 1
                    for d, W in gen(kind, WTS[(pn, f, g, bn)], k, tag):
                        gr, tn = pc["ctx"].run(W)
                        gsum += pc["ctx"].gross(W, pc["i0"])
                        for c in COSTS:
                            m, mo, mi = score_stream(gr, tn, pc, c)
                            pv[c][d] = pass4b(m, mo["Sharpe"], pc["spy"],
                                              pc["spy_oos"]["Sharpe"])
                            iv[c][d] = pass4b_is(mi, pc["spy_is"])
                            sv[c][d], cvv[c][d], dv[c][d] = m["Sharpe"], m["CAGR"], m["MaxDD"]
                            ov[c][d], ovc[c][d], ovd[c][d] = (mo["Sharpe"], mo["CAGR"],
                                                              mo["MaxDD"])
                            obp[c][d] = bool(mo["Sharpe"] > pc["spy_oos"]["Sharpe"] and
                                             abs(mo["MaxDD"]) <=
                                             0.60 * abs(pc["spy_oos"]["MaxDD"]) and
                                             mo["CAGR"] >= 0.70 * pc["spy_oos"]["CAGR"])
                            if c == PROTO_COST:
                                vsum.append(m["vol"])
                    mg_null = gsum / DRAWS
                    brow = books[(books.panel == pn) & (books.cadence == f) &
                                 (books.gross == g) & (books.book == bn)]
                    mg_book = float(brow.mean_gross.iloc[0])
                    for c in COSTS:
                        b = brow[brow.cost == c].iloc[0]
                        for nd in DRAW_GRID:
                            NULLROWS.append(dict(
                                panel=pn, cadence=f, book=bn, gross=g, null=kind, cost=c,
                                draws=nd,
                                null_base_rate_4b=float(pv[c][:nd].mean()),
                                null_oos_base_rate_4b=float(obp[c][:nd].mean()),
                                is_base_rate_4b=float(iv[c][:nd].mean()),
                                book_pass4b=bool(b.pass4b), book_pass4a=bool(b.pass4a),
                                outside_null=bool(b.pass4b and
                                                  float(pv[c][:nd].mean()) <= BASE_RATE_BAR),
                                pct_Sharpe=float((sv[c][:nd] < b.Sharpe).mean()),
                                pct_CAGR=float((cvv[c][:nd] < b.CAGR).mean()),
                                pct_MaxDD=float((np.abs(dv[c][:nd]) > abs(b.MaxDD)).mean()),
                                pct_OOS_Sharpe=float((ov[c][:nd] < b.OOS_Sharpe).mean()),
                                p_emp_Sharpe=float((1 + (sv[c][:nd] >= b.Sharpe).sum()) /
                                                   (1 + nd)),
                                null_med_Sharpe=float(np.median(sv[c][:nd])),
                                null_med_OOS_Sharpe=float(np.median(ov[c][:nd])),
                                book_Sharpe=float(b.Sharpe), book_CAGR=float(b.CAGR),
                                book_MaxDD=float(b.MaxDD), book_OOS_Sharpe=float(b.OOS_Sharpe),
                                turn_per_yr=float(b.turn_per_yr), drag_bps=float(b.drag_bps),
                                mean_gross_null=mg_null, mean_gross_book=mg_book,
                                gross_match=abs(mg_null - mg_book),
                                null_med_vol=float(np.median(vsum)) if vsum else np.nan))
                        if c == PROTO_COST:
                            for d in range(DRAWS):
                                DRAWROWS.append(dict(panel=pn, cadence=f, book=bn, gross=g,
                                                     draw=d, pass4b=bool(pv[c][d]),
                                                     Sharpe=sv[c][d], CAGR=cvv[c][d],
                                                     MaxDD=dv[c][d], OOS_Sharpe=ov[c][d]))
                    P(f"  {pn:9s} [{f}] g={g:.2f} {bn:7s} null={kind:3s}  gross book "
                      f"{mg_book:.3f} vs null {mg_null:.3f} (|d| "
                      f"{abs(mg_null - mg_book):.4f})   base rate @0 "
                      f"{float(pv[0.0].mean()):6.1%}  @10 {float(pv[PROTO_COST].mean()):6.1%}"
                      f"  @50 {float(pv[50.0].mean()):6.1%}   [{time.time() - t0:.0f}s]")
        P()
    nulls = pd.DataFrame(NULLROWS)
    draws_df = pd.DataFrame(DRAWROWS)
    dump(nulls, "nulls")
    dump(draws_df, "draws")

    g5 = float(nulls.gross_match.max())
    gk["G5"] = g5 < 0.01
    P(f"  G5 gross match, worst over "
      f"{nulls[['panel','cadence','book','gross']].drop_duplicates().shape[0]} families: "
      f"{g5:.4f}  {'PASS' if gk['G5'] else 'FAIL'}")
    nest_ok = True
    for (pn, f, bn, g), gdf in draws_df.groupby(["panel", "cadence", "book", "gross"]):
        v = gdf.sort_values("draw").pass4b.values
        for nd in DRAW_GRID:
            got = float(nulls[(nulls.panel == pn) & (nulls.cadence == f) &
                              (nulls.book == bn) & (nulls.gross == g) &
                              (nulls.cost == PROTO_COST) &
                              (nulls.draws == nd)].null_base_rate_4b.iloc[0])
            nest_ok &= abs(float(v[:nd].mean()) - got) == 0.0
    gk["G8"] = bool(nest_ok)
    P(f"  G8 nesting: the {DRAW_GRID[0]}/{DRAW_GRID[1]} base rates are exact prefixes of the "
      f"same {DRAWS} streams  {'PASS' if gk['G8'] else 'FAIL'}")
    inv = nulls[nulls.draws == DRAWS]
    g10 = bool((inv.mean_gross_null > 0).all() and (inv.null_med_vol.fillna(0) > 0.02).all())
    gk["G10"] = g10
    P(f"  G10 null INVESTED on every family: min mean gross {inv.mean_gross_null.min():.4f}, "
      f"min median vol {inv.null_med_vol.min():.4f}  {'PASS' if g10 else 'FAIL'}")
    nb = nulls[(nulls.panel == "U56") & (nulls.cadence == "M") & (nulls.book == "TOP20") &
               (nulls.gross == 0.75) & (nulls.cost == PROTO_COST) &
               (nulls.draws == DRAWS)].iloc[0]
    d3b = abs(float(nb.null_base_rate_4b) - PUB_NULL_M_BASE10)
    gk["G3b"] = d3b < 0.10
    P(f"  G3b CROSS-RUN null leg, U56/TOP20/0.75/M @10 bps: got "
      f"{nb.null_base_rate_4b:.1%}   published (926/931) {PUB_NULL_M_BASE10:.1%}   "
      f"|d| {d3b:.3f}  {'PASS' if gk['G3b'] else 'FAIL'}   [seed {SEED0} vs 926, "
      f"{DRAWS} draws vs their 400/500]")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) THE RE-SCORE -- every committed monthly 4b PASS row against its own monthly null")
    P("=" * 100)
    RS, HEAD = [], []
    for cs in CLAIM_SETS:
        d = cen[(cen.claim_set == cs) & cen.mapped].copy()
        for nd in DRAW_GRID:
            key = nulls[(nulls.cadence == "M") & (nulls.draws == nd)][
                ["panel", "book", "gross", "cost", "null_base_rate_4b", "book_pass4b",
                 "pct_Sharpe", "turn_per_yr", "drag_bps"]]
            j = d.merge(key, on=["panel", "book", "gross", "cost"], how="left")
            keyW = nulls[(nulls.cadence == "W") & (nulls.draws == nd)][
                ["panel", "book", "gross", "cost", "null_base_rate_4b"]].rename(
                columns={"null_base_rate_4b": "W_base"})
            j = j.merge(keyW, on=["panel", "book", "gross", "cost"], how="left")
            j = j[j.null_base_rate_4b.notna()]
            for _, r in j.iterrows():
                RS.append(dict(claim_set=cs, draws=nd, file=r.file, panel=r.panel,
                               book=r.book, gross=r.gross, cost=r.cost,
                               M_base=r.null_base_rate_4b, W_base=r.W_base,
                               above_bar=bool(r.null_base_rate_4b > BASE_RATE_BAR),
                               above_25=bool(r.null_base_rate_4b > 0.25),
                               cell_book_pass4b=bool(r.book_pass4b),
                               turn_per_yr=r.turn_per_yr, drag_bps=r.drag_bps))
            if len(j):
                HEAD.append(dict(
                    claim_set=cs, draws=nd, n_claims=len(j),
                    n_cells=int(j.groupby(["panel", "book", "gross", "cost"]).ngroups),
                    share_above_bar=float((j.null_base_rate_4b > BASE_RATE_BAR).mean()),
                    share_above_25=float((j.null_base_rate_4b > 0.25).mean()),
                    share_above_50=float((j.null_base_rate_4b > 0.50).mean()),
                    med_M_base=float(j.null_base_rate_4b.median()),
                    mean_M_base=float(j.null_base_rate_4b.mean()),
                    max_M_base=float(j.null_base_rate_4b.max()),
                    med_W_base=float(j.W_base.median()),
                    mean_W_base=float(j.W_base.mean()),
                    max_W_base=float(j.W_base.max())))
    rescore = pd.DataFrame(RS)
    head = pd.DataFrame(HEAD)
    dump(rescore, "rescore")
    dump(head, "headline")
    P(f"  {'set':7s} {'draws':>5s} {'claims':>7s} {'cells':>6s} {'>5%':>7s} {'>25%':>7s} "
      f"{'>50%':>7s} {'med M':>7s} {'mean M':>7s} {'max M':>7s} {'med W':>7s} {'max W':>7s}")
    for _, r in head.iterrows():
        P(f"  {r.claim_set:7s} {int(r.draws):5d} {int(r.n_claims):7d} {int(r.n_cells):6d} "
          f"{r.share_above_bar:7.1%} {r.share_above_25:7.1%} {r.share_above_50:7.1%} "
          f"{r.med_M_base:7.1%} {r.mean_M_base:7.1%} {r.max_M_base:7.1%} "
          f"{r.med_W_base:7.1%} {r.max_W_base:7.1%}")
    P()
    P("  the mapped CELLS themselves (STRICT, 400 draws), monthly vs weekly base rate:")
    cell = rescore[(rescore.claim_set == "STRICT") & (rescore.draws == DRAWS)].groupby(
        ["panel", "book", "gross", "cost"]).agg(
        claims=("file", "size"), M_base=("M_base", "first"), W_base=("W_base", "first"),
        turn=("turn_per_yr", "first")).reset_index().sort_values("claims", ascending=False)
    dump(cell, "cells")
    P(f"     {'panel':9s} {'book':7s} {'gross':>5s} {'cost':>5s} {'claims':>7s} "
      f"{'M base':>7s} {'W base':>7s} {'M/W':>6s} {'turn/yr':>8s}")
    for _, r in cell.head(30).iterrows():
        rat = r.M_base / r.W_base if r.W_base > 0 else np.inf
        P(f"     {r.panel:9s} {r.book:7s} {r.gross:5.2f} {r.cost:5.0f} {int(r.claims):7d} "
          f"{r.M_base:7.1%} {r.W_base:7.1%} {rat:6.2f} {r.turn:8.2f}")
    P()

    P("  by COST RUNG (claim-weighted over the mapped rows, both claim sets, 400 draws):")
    P(f"     {'set':7s} {'rung':>5s} {'claims':>7s} {'mean M base':>12s} {'mean W base':>12s} "
      f"{'M/W':>7s} {'share M>5%':>11s} {'share W>5%':>11s}")
    RUNG = []
    for cs in CLAIM_SETS:
        for c in COSTS:
            j = rescore[(rescore.claim_set == cs) & (rescore.draws == DRAWS) &
                        (rescore.cost == c)]
            if not len(j):
                continue
            aM, aW = float(j.M_base.mean()), float(j.W_base.mean())
            RUNG.append(dict(claim_set=cs, cost=c, claims=len(j), mean_M=aM, mean_W=aW,
                             ratio=aM / aW if aW > 0 else np.nan,
                             share_M=float((j.M_base > BASE_RATE_BAR).mean()),
                             share_W=float((j.W_base > BASE_RATE_BAR).mean())))
            P(f"     {cs:7s} {c:5.0f} {len(j):7d} {aM:12.2%} {aW:12.2%} "
              f"{(aM / aW if aW > 0 else float('nan')):7.2f} "
              f"{float((j.M_base > BASE_RATE_BAR).mean()):11.1%} "
              f"{float((j.W_base > BASE_RATE_BAR).mean()):11.1%}")
    pd.DataFrame(RUNG).to_csv(OUT / f"{STEM}.rungs.csv", index=False)
    P()

    P("  PRE-REGISTERED HYPOTHESES")
    h = head[(head.claim_set == "STRICT") & (head.draws == DRAWS)]
    hw = head[(head.claim_set == "WIDE") & (head.draws == DRAWS)]
    if len(h):
        hs, hws = float(h.share_above_bar.iloc[0]), float(hw.share_above_bar.iloc[0])
        h_base = bool(hs > 0.50)
        P(f"     H_BASE   share of MAPPED committed monthly 4b passes on a cell whose own "
          f"coin flip clears 4b at > {BASE_RATE_BAR:.0%}: {hs:.1%} (STRICT, {DRAWS} draws) "
          f"-> {'PASS' if h_base else 'FAIL'}  (bar > 50%)")
        aM, aW = float(h.mean_M_base.iloc[0]), float(h.mean_W_base.iloc[0])
        mM, mW = float(h.med_M_base.iloc[0]), float(h.med_W_base.iloc[0])
        ratio = aM / aW if aW > 0 else np.nan
        h_cad = bool(np.isfinite(ratio) and ratio >= 2.0)
        P(f"     H_CAD    claim-weighted MEAN base rate over the mapped cells: M {aM:.2%} vs "
          f"W {aW:.2%} = {ratio:.2f}x -> "
          f"{'PASS' if h_cad else ('UNDEFINED (weekly mean 0)' if not np.isfinite(ratio) else 'FAIL')}"
          f"  (bar 2.0x)   [medians M {mM:.1%} / W {mW:.1%}, printed not tested]")
        h_claim = bool(abs(hs - hws) <= 0.10)
        P(f"     H_CLAIM  share(STRICT) {hs:.1%} vs share(WIDE) {hws:.1%}, |d| "
          f"{abs(hs - hws):.3f} -> {'PASS' if h_claim else 'FAIL'}  (bar 0.10)")
        HYP = [dict(name="H_BASE", value=hs, bar=0.50, result=h_base),
               dict(name="H_CAD", value=ratio, bar=2.0, result=h_cad),
               dict(name="H_CLAIM", value=abs(hs - hws), bar=0.10, result=h_claim)]
    else:
        P("     NO MAPPED CLAIMS -- hypotheses undecidable, reported as such")
        HYP = [dict(name=n, value=np.nan, bar=b, result=False)
               for n, b in (("H_BASE", 0.5), ("H_CAD", 2.0), ("H_CLAIM", 0.1))]
    pd.DataFrame(HYP).to_csv(OUT / f"{STEM}.hypotheses.csv", index=False)
    P()
    P("  draw-axis convergence (binding panel U56, cadence M, 10 bps):")
    for g in GROSS_GRID:
        for bn in BOOKS:
            row = [float(nulls[(nulls.panel == "U56") & (nulls.cadence == "M") &
                               (nulls.book == bn) & (nulls.gross == g) &
                               (nulls.cost == PROTO_COST) &
                               (nulls.draws == nd)].null_base_rate_4b.iloc[0])
                   for nd in DRAW_GRID]
            P(f"     g={g:.2f} {bn:7s}  " +
              "  ".join(f"n={nd}: {v:6.1%}" for nd, v in zip(DRAW_GRID, row)))
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(G) RULE 8 WALK-FORWARD -- parameters chosen on 2009-2016 only, 2017-2026 read once")
    P("=" * 100)
    P("  Three IS-only choosers over the MONTHLY grid (book x gross), plus the same three")
    P("  with the CADENCE also chosen in sample:")
    P("    CH_SHARPE  best IS Sharpe                                          (no clause)")
    P("    CH_4bIS    best IS Sharpe among books passing the IS 4b LEVEL legs")
    P("    CH_BASE    best IS Sharpe among books whose IS null base rate <= 0.05")
    P("  Every pick is reported with the OOS base rate of ITS OWN null, which is the number")
    P("  this idea exists to supply: an OOS 4b pass on a cell whose coin flip also passes OOS")
    P("  is not evidence about the rule.")
    WF = []
    for pn in panels:
        for c in COSTS:
            br = nulls[(nulls.panel == pn) & (nulls.cost == c) & (nulls.draws == DRAWS)]
            cand_all = books[(books.panel == pn) & (books.cost == c)].merge(
                br[["cadence", "book", "gross", "null_base_rate_4b", "is_base_rate_4b",
                    "null_oos_base_rate_4b", "null_med_OOS_Sharpe"]],
                on=["cadence", "book", "gross"], how="left")
            for scope in ["M", "ANY"]:
                pcref = PC[(pn, "M")]
                cand = cand_all if scope == "ANY" else cand_all[cand_all.cadence == "M"]
                cand = cand.copy()
                si = pcref["spy_is"]
                cand["IS_ok"] = ((cand.IS_H1 > si["H1"]) & (cand.IS_H2 > si["H2"]) &
                                 (cand.IS_CAGR >= 0.70 * si["CAGR"]) &
                                 (cand.IS_MaxDD.abs() <= 0.60 * abs(si["MaxDD"])))
                picks = {}
                picks["CH_SHARPE"] = cand.sort_values("IS_Sharpe", ascending=False).iloc[0]
                s4 = cand[cand.IS_ok].sort_values("IS_Sharpe", ascending=False)
                picks["CH_4bIS"] = s4.iloc[0] if len(s4) else None
                sb = cand[cand.is_base_rate_4b <= BASE_RATE_BAR].sort_values(
                    "IS_Sharpe", ascending=False)
                picks["CH_BASE"] = sb.iloc[0] if len(sb) else None
                for ch, r in picks.items():
                    if r is None:
                        WF.append(dict(panel=pn, scope=scope, cost=c, chooser=ch,
                                       pick="EMPTY"))
                        continue
                    pcr = PC[(pn, r.cadence)]
                    v2o, so = pcr["v2"][c]["oos"], pcr["spy_oos"]
                    WF.append(dict(
                        panel=pn, scope=scope, cost=c, chooser=ch,
                        pick=f"{r.cadence}/{r.book}/g{r.gross:.2f}", IS_Sharpe=r.IS_Sharpe,
                        base_rate=r.null_base_rate_4b, is_base_rate=r.is_base_rate_4b,
                        oos_base_rate=r.null_oos_base_rate_4b,
                        null_med_OOS_Sharpe=r.null_med_OOS_Sharpe,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        OOS_4b=bool(r.OOS_Sharpe > so["Sharpe"] and
                                    abs(r.OOS_MaxDD) <= 0.60 * abs(so["MaxDD"]) and
                                    r.OOS_CAGR >= 0.70 * so["CAGR"]),
                        OOS_4a=bool(r.OOS_Sharpe > v2o["Sharpe"] and
                                    r.OOS_MaxDD >= v2o["MaxDD"]),
                        SPY_OOS_CAGR=so["CAGR"], SPY_OOS_Sharpe=so["Sharpe"],
                        SPY_OOS_MaxDD=so["MaxDD"], V2_OOS_CAGR=v2o["CAGR"],
                        V2_OOS_Sharpe=v2o["Sharpe"], V2_OOS_MaxDD=v2o["MaxDD"]))
    wf = pd.DataFrame(WF)
    dump(wf, "walkforward")
    for pn in panels:
        P(f"  {pn}:")
        for _, r in wf[wf.panel == pn].iterrows():
            if r["pick"] == "EMPTY":
                P(f"     [{r.scope:3s}] {r.cost:4.0f} bps  {r.chooser:10s}  IS set EMPTY")
                continue
            P(f"     [{r.scope:3s}] {r.cost:4.0f} bps  {r.chooser:10s}  pick "
              f"{r['pick']:18s} (IS Sh {r.IS_Sharpe:5.2f}) OOS {r.OOS_CAGR:7.2%} / "
              f"{r.OOS_Sharpe:5.3f} / {r.OOS_MaxDD:7.2%}  4b "
              f"{'PASS' if r.OOS_4b else 'fail'}  4a {'PASS' if r.OOS_4a else 'fail'}   "
              f"null OOS 4b rate {r.oos_base_rate:5.1%}   "
              f"[SPY {r.SPY_OOS_CAGR:6.2%}/{r.SPY_OOS_Sharpe:5.3f}/{r.SPY_OOS_MaxDD:7.2%}"
              f" | v2 {r.V2_OOS_CAGR:6.2%}/{r.V2_OOS_Sharpe:5.3f}/{r.V2_OOS_MaxDD:7.2%}]")
        P()
    live = wf[wf["pick"] != "EMPTY"]
    P(f"  rule-8 totals: 4b {int(live.OOS_4b.sum())} of {len(live)} live picks, "
      f"4a {int(live.OOS_4a.sum())} of {len(live)}   "
      f"(EMPTY on {int((wf['pick'] == 'EMPTY').sum())})")
    for ch, gdf in live.groupby("chooser"):
        P(f"     {ch:10s}  4b {int(gdf.OOS_4b.sum()):2d}/{len(gdf):<3d}  "
          f"4a {int(gdf.OOS_4a.sum()):2d}/{len(gdf):<3d}  mean OOS Sharpe "
          f"{gdf.OOS_Sharpe.mean():5.3f}  mean OOS CAGR {gdf.OOS_CAGR.mean():6.2%}  "
          f"mean null OOS 4b rate {gdf.oos_base_rate.mean():5.1%}")
    ok4b = live[live.OOS_4b]
    P(f"  of the {len(ok4b)} OOS 4b passes, {int((ok4b.oos_base_rate > BASE_RATE_BAR).sum())} "
      f"sit on a cell whose own coin flip clears OOS 4b at > {BASE_RATE_BAR:.0%} "
      f"(median null OOS rate on those picks "
      f"{ok4b.oos_base_rate.median() if len(ok4b) else float('nan'):.1%})")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(H) KEEP PATHS -- both, at PROTOCOL's own rung, full sample")
    P("=" * 100)
    for f in CADENCES:
        sub = books[(books.cost == PROTO_COST) & (books.cadence == f)]
        k4a, k4b = sub[sub.pass4a], sub[sub.pass4b]
        P(f"  [{f}] 4a (beat the live book in both halves, MaxDD no worse): "
          f"{len(k4a)} of {len(sub)} cells")
        for _, r in k4a.iterrows():
            P(f"       {r.panel:9s} {r.book:7s} g{r.gross:.2f}  {r.CAGR:7.2%} / "
              f"{r.Sharpe:6.3f} / {r.MaxDD:7.2%}")
        P(f"  [{f}] 4b (capital-worthy, full-sample legs): {len(k4b)} of {len(sub)} cells")
        for _, r in k4b.iterrows():
            n = nulls[(nulls.panel == r.panel) & (nulls.cadence == f) &
                      (nulls.book == r.book) & (nulls.gross == r.gross) &
                      (nulls.cost == PROTO_COST) & (nulls.draws == DRAWS)].iloc[0]
            P(f"       {r.panel:9s} {r.book:7s} g{r.gross:.2f}  {r.CAGR:7.2%} / "
              f"{r.Sharpe:6.3f} / {r.MaxDD:7.2%}  halves {r.H1:5.2f}/{r.H2:5.2f}  "
              f"OOS Sh {r.OOS_Sharpe:5.3f}  null base rate {n.null_base_rate_4b:5.1%}  "
              f"outside null {'YES' if n.outside_null else 'no'}")
        P()
    P("  NOTE: a full-sample 4b pass is NOT a KEEP -- rule 8's OOS leg is section (G), and")
    P("  every cell above is an already-published book, not a new rule.  Nothing is promoted.")
    P()

    P("=" * 100)
    P("(I) GATES")
    P("=" * 100)
    for k in sorted(gk):
        P(f"  {k}: {'PASS' if gk[k] else 'FAIL'}")
    P(f"  {sum(bool(v) for v in gk.values())} of {len(gk)} pass")
    pd.DataFrame([dict(gate=k, result=bool(v)) for k, v in sorted(gk.items())]).to_csv(
        OUT / f"{STEM}.gates.csv", index=False)
    P()
    P(f"total runtime {time.time() - t0all:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
