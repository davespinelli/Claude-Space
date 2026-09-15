#!/usr/bin/env python3
"""
IDEA 944 -- is-the-4b-DD-CAP-the-binding-leg-for-EVERY-offset-fragile-book-in-the-record
    (lane B, 2026-09-15)
====================================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 938 found all 18 of 25 failing monthly offsets fail on L4_DD alone, never on a Sharpe
  leg, so the 60%-of-SPY cap is doing all the discriminating and MaxDD is the most
  offset-sensitive statistic in the 4b bar (support -22.95% to -14.89% over 21 phases, 8.06 pp,
  against a 1.95 pp CAGR spread).  Census the record's committed 4b FAIL rows for which leg
  binds, and measure each statistic's phase sensitivity, so the record knows which of its bars
  is a coin flip on the rebalance date.  Max 2 params (claim set, phase grid).

WHY IT MATTERS FOR CAPITAL
--------------------------
  PROTOCOL rule 4b is the ONLY path in this repo that can move real money.  It is a conjunction
  of five legs (H1 Sharpe > SPY, H2 Sharpe > SPY, OOS Sharpe > SPY, MaxDD <= 60% of SPY's,
  CAGR >= 70% of SPY's).  A conjunction is only as informative as its binding leg.  If one leg
  rejects nearly everything, the other four are decoration and the bar is really a one-statistic
  bar -- and if that one leg is also the statistic that moves most when you change a parameter
  NOBODY EVER TUNED (which day of the month the book trades), then 4b is partly a lottery on the
  rebalance date.  938 showed exactly that on ONE book.  This run asks whether it is a property
  of the RECORD or a property of TOP20.

THE TWO MECHANISMS, STATED SO THEY CAN FAIL
-------------------------------------------
  H_DDBINDS   the DD cap is THE binding leg of 4b.  Predictions: (a) in the record's committed
              4b FAIL rows, DD is among the binding legs in the overwhelming majority, and DD
              ALONE is the modal binding set; (b) on this run's own phase grid, every
              offset-fragile book fails on DD at every failing phase; (c) DD has the highest
              phase FLIP rate of the five legs.
  H_MIXED     938's 18-of-25 is a property of TOP20 at gross 0.75 on U56 -- a book whose Sharpe
              legs are comfortably clear of SPY and whose drawdown sits right on the cap -- and
              other books in the record bind on other legs.  Predictions: the census shows a
              mixed binding vocabulary with no leg near-universal, and the fragile books on this
              run's grid disagree about which leg binds.
  The two are separated by the pre-registered bars below, scored mechanically.

DESIGN
------
  TUNED (2, and only 2 -- every grid point is reported, none is selected for a headline)
    1. CLAIM SET   (a) CENSUS side: which committed rows count.  The census reads EVERY
                   `fail4b`-style column in EVERY committed CSV under research/backtests
                   (447 files, ~825k rows at the time of writing), normalises the record's
                   many spellings ("H1,H2,OOS,DD,CAGR", "H1+H2+...", "H1|H2|...", "DDCAP",
                   "CAGRFLOOR", ...) onto the five canonical legs, and reports the tally BOTH
                   row-weighted and file-weighted, because one 200k-row sweep would otherwise
                   speak for the whole record.  Unmappable spellings are counted and shown,
                   never silently dropped.
                   (b) PRICE side: the BOOK SET priced on the phase grid -- 9 books spanning
                   the record's modal constructions (TOP5/TOP10/TOP20/TOP40 ranked books at
                   gross 0.75, TOP20 at gross 1.00, BAND03 at 0.75 and 1.00, BAND03 at a
                   0.06 band, and RULES v2 itself).  All 9 are reported at every phase.
    2. PHASE GRID  the same 30 offsets as idea 938, so this run NESTS its predecessor:
                   DOM d (21) = d trading days before each calendar month's last trading day
                   (d = 0 IS the canonical convention, G0 asserts bit-identity with
                   engine.rebalance_mask); 4W o (4) = every 4th W-end, phase o; DOW d (5) =
                   the weekly family, d days before each week's last trading day (d = 0 is the
                   canonical weekly).
  NOT TUNED -- copied from idea 938 / the incumbent without change
    COST       10 bps, PROTOCOL rule 2.  Cost is NOT an axis in this run (938 already published
               the cost curve); every number below is at PROTOCOL's own rung.
    GATE       above the 200d MA and vol20 < 0.60 for the ranked books; the 200d +/-band with
               hysteresis for the band books.  Warm-up 260 rows.
    PANELS     U56 (BINDING) and B136 (labelled replication, no verdict taken from it).
    WINDOWS    IS <= 2016-12-31, OOS >= 2017-01-01 (PROTOCOL rule 8).
    COMPARANDS SPY buy-and-hold and RULES v2 (live) on the same tape (PROTOCOL rule 3).

  STATISTIC, NAMED WITH ITS n (idea 564's standing request).  Two populations, never pooled:
    CENSUS  n = the committed FAIL rows actually parsed, printed with its file count.  It is a
            census of a TEXT ARTEFACT, not a sample from a population, so no p-value is claimed
            and no confidence interval is printed -- only shares, with the row/file duality that
            shows how concentrated they are.
    PRICE   n = 21 DOM phases per book-cell (9 books x 2 panels = 18 cells).  A rank over 21
            points has resolution 1/21 = 4.8% and that is stated wherever a percentile prints.

PRE-REGISTERED BARS (printed before any new number is read; the verdict is mechanical)
---------------------------------------------------------------------------------------
  B1 CENSUS-AMONG   over the record's committed 4b FAIL rows, DD is AMONG the binding legs in
                    >= 90% (row-weighted AND file-weighted must both clear).
  B2 CENSUS-ALONE   DD ALONE is the modal binding set among those FAIL rows, with share >= 50%
                    (row-weighted AND file-weighted).
  B3 PRICE-EVERY    over the OFFSET-FRAGILE book-cells on U56 (cells whose 4b verdict is not
                    constant over the 21 DOM phases), DD is among the binding legs at EVERY
                    failing phase, in >= 90% of those cells.
  B4 FLIP-RANK      the DD leg's phase FLIP rate (share of book-cells where that leg's PASS/FAIL
                    is not constant over the 21 DOM phases) is STRICTLY the highest of the five
                    legs, evaluated over all 9 x 2 cells.
  B5 SENS-RANK      MaxDD's normalised phase spread ((max-min)/|median| over the 21 DOM phases)
                    is the largest of the five 4b statistics in >= 80% of book-cells.
  VERDICT RULE      H_DDBINDS requires B1 AND B2 AND B3 AND B4.  Any failure scores H_MIXED and
                    KILLS the generalisation of 938's 18-of-25 to the record.  B5 is the
                    separate "which statistic is a coin flip on the rebalance date" question and
                    is reported on its own; it moves no mechanism verdict, because a statistic
                    can be the most phase-sensitive WITHOUT its leg being the one that binds.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G0  offset_mask(.,per,0) == engine.rebalance_mask(.,per) on M and W          bar 0 rows
  G1  ctx.run == engine.backtest @10 bps on W and M                            bar 1e-12
  G2  band_book(0.03,0.75) == baseline.rules_v2_weights                        bar 0.0
  G3  idea 938's committed headline re-derived from this file's code path on U56/CORE/TOP20
      @10 bps: 18 of 25 monthly offsets FAIL, all on L4_DD alone; DOM MaxDD support
      -22.95%..-14.89% (8.06 pp); DOM CAGR spread 1.95 pp                      bar 5e-3 / exact
  G4  PHASE FAIRNESS: rebalances/yr printed for all 30 offsets; no DOM offset may trade fewer
      than 11.5 or more than 12.5 times a year                                 bar as stated
  G5  DETERMINISM: the canonical monthly stream re-derived twice               bar 0.0
  G6  baseline.compare() agrees with this file's fast runner on the two canonical books
      (the PROTOCOL rule-3 code path, run end to end)                          bar 5e-3
  G7  CENSUS COVERAGE: the share of parsed FAIL-row cells whose spelling maps onto the five
      canonical legs is printed; unmappable spellings are listed              bar >= 0.95

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  universe.json and universe_broad.json are CURRENT-CONSTITUENT lists.  Every CAGR, Sharpe and
  drawdown LEVEL below is therefore optimistic and none is a capital claim on its own.
  Direction for THIS run: the phase contrasts and the binding-leg tallies are SAME-TAPE,
  same-universe, same-weights comparisons that differ only in WHICH DAY the identical book
  trades, so they are unaffected by panel composition.  The 4b LEVELS are read against SPY,
  which is not survivorship-inflated, so a survivor panel makes books look BETTER and therefore
  makes 4b FAILURES rarer -- which cuts AGAINST this run finding a near-universal binding leg,
  not for it.  The census inherits whatever biases its source runs had and is reported as a
  census of the record's TEXT, not of the market.
"""
import os, sys, csv, gzip, glob, time, warnings, collections
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score, compare   # noqa: E402
from engine import backtest, rebalance_mask                                        # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HEAD_COST = 10.0                               # PROTOCOL rule 2 -- carries every verdict
DOM_N, NW_N, DOW_N = 21, 4, 5                  # TUNED axis 2 (three families, 30 offsets)
BINDING_PANEL = "U56"
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
B1_BAR, B2_BAR, B3_BAR, B5_BAR = 0.90, 0.50, 0.90, 0.80
G7_BAR = 0.95
# idea 938's committed anchors (G3)
PUB938 = dict(n_fail=18, n_monthly=25, dd_alone=18,
              dd_min=-0.2295, dd_max=-0.1489, dd_spread_pp=8.06, cagr_spread_pp=1.95)

SMOKE = bool(int(os.environ.get("IDEA944_SMOKE", "0")))
LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# (1) the phase machinery -- copied verbatim from idea 938 so this run NESTS it
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period (per in {'W','M'}).
    d = 0 reproduces engine.rebalance_mask(idx, per) exactly (G0)."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    clipped = int((last - d < first).sum())
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, clipped


def nweek_mask(idx, n, o):
    w = np.flatnonzero(rebalance_mask(idx, "W").values)
    keep = w[o::n]
    out = pd.Series(False, index=idx)
    out.iloc[keep] = True
    return out, 0


def offset_grid():
    g = [("DOM", f"DOM{d:02d}", ("M", d)) for d in range(DOM_N)]
    g += [("4W", f"4W{o}", ("NW", o)) for o in range(NW_N)]
    g += [("DOW", f"DOW{d}", ("W", d)) for d in range(DOW_N)]
    return g


def build_mask(idx, spec):
    kind, k = spec
    return nweek_mask(idx, NW_N, k) if kind == "NW" else offset_mask(idx, kind, k)


class Ctx:
    """Fast runner -- byte-identical to idea 938's (G1 asserts it against engine.backtest)."""
    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
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
                H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs4b(m, oos_s, ms, spy_oos):
    """PROTOCOL 4b, leg by leg.  Keys are the five canonical leg names used all run."""
    return dict(H1=m["H1"] > ms["H1"], H2=m["H2"] > ms["H2"], OOS=oos_s > spy_oos,
                DD=abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
                CAGR=m["CAGR"] >= 0.70 * ms["CAGR"])


def failstr(lg):
    f = [k for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


def pass4a(m, mb):
    return bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])


# ==========================================================================================
# (2) the book set -- TUNED axis 1(b).  Every book is reported at every phase.
# ==========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ranked_book(px, g, k):
    """The 2026-09-04 KEEP-4b incumbent's construction, copied from idea 938 unchanged."""
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    rank = sc.where(elig).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {
    "TOP05_g075": lambda p: ranked_book(p, 0.75, 5),
    "TOP10_g075": lambda p: ranked_book(p, 0.75, 10),
    "TOP20_g075": lambda p: ranked_book(p, 0.75, 20),    # idea 938's book -- the G3 anchor
    "TOP40_g075": lambda p: ranked_book(p, 0.75, 40),
    "TOP20_g100": lambda p: ranked_book(p, 1.00, 20),
    "BAND03_g075": lambda p: band_book(p, 0.03, 0.75),   # == RULES v2 weights (G2)
    "BAND03_g100": lambda p: band_book(p, 0.03, 1.00),
    "BAND06_g075": lambda p: band_book(p, 0.06, 0.75),
    "RULESV2": lambda p: rules_v2_weights(p, BAND0, 0.75),
}


def panel_context(px, mask):
    ctx = Ctx(px, mask)
    idx = px.index
    i0 = WARM
    oos = np.asarray(idx >= pd.Timestamp(OOS_START))[i0:]
    is_ = np.asarray(idx <= pd.Timestamp(IS_END))[i0:]
    spy = px["SPY"].pct_change().fillna(0.0).values[i0:]
    return dict(ctx=ctx, i0=i0, oos=oos, is_=is_, spy=mets(spy), spy_oos=mets(spy[oos]),
                spy_is=mets(spy[is_]))


def score_stream(gr, tn, pc, c):
    i0, oos, is_ = pc["i0"], pc["oos"], pc["is_"]
    r = (gr - tn * c / 1e4)[i0:]
    return mets(r), mets(r[oos]), mets(r[is_])


def pct_rank(x, arr):
    arr = np.asarray(arr, float)
    return float((arr <= x).sum() / len(arr))


# ==========================================================================================
# (3) THE CENSUS -- read the record's committed FAIL rows and normalise their spellings
# ==========================================================================================
CANON = {
    "H1": "H1", "L1": "H1", "L1_H1": "H1", "H1SHARPE": "H1", "SH1": "H1", "HALF1": "H1",
    "H2": "H2", "L2": "H2", "L2_H2": "H2", "H2SHARPE": "H2", "SH2": "H2", "HALF2": "H2",
    "OOS": "OOS", "L3": "OOS", "L3_OOS": "OOS", "OOSSHARPE": "OOS", "OOS_SHARPE": "OOS",
    "WF": "OOS", "OOSSH": "OOS",
    "DD": "DD", "L4": "DD", "L4_DD": "DD", "MAXDD": "DD", "DDCAP": "DD", "DD_CAP": "DD",
    "DRAWDOWN": "DD",
    "CAGR": "CAGR", "L5": "CAGR", "L5_CAGR": "CAGR", "CAGRFLOOR": "CAGR",
    "CAGR_FLOOR": "CAGR", "RET": "CAGR",
}
SEPS = [",", "+", "|", ";", "/", "&", " "]
PASSTOK = {"-", "", "NONE", "PASS", "OK", "NAN", "0", "FALSE", "NA", "PASS4B", "-NONE-"}


def norm_failcell(v):
    """Map one committed fail-string onto a frozenset of canonical legs.
    Returns (legs, status) with status in {'pass','fail','unmappable'}."""
    s = str(v).strip()
    if s.upper() in PASSTOK:
        return frozenset(), "pass"
    t = s.upper()
    for sep in SEPS[1:]:
        t = t.replace(sep, ",")
    toks = [x.strip() for x in t.split(",") if x.strip()]
    if not toks:
        return frozenset(), "pass"
    out = set()
    for tk in toks:
        tk2 = tk.replace("-", "_") if tk.startswith("L") else tk
        hit = CANON.get(tk) or CANON.get(tk2) or CANON.get(tk.replace("_", ""))
        if hit is None:
            return frozenset(), "unmappable"
        out.add(hit)
    return frozenset(out), "fail"


def run_census():
    """Every `fail4b`-like column in every committed CSV under research/backtests."""
    files = sorted(glob.glob(str(OUT / "*.csv"))) + sorted(glob.glob(str(OUT / "*.csv.gz")))
    rows = collections.Counter()        # frozenset(legs) -> row count  (FAIL rows only)
    per_file = {}                       # file -> Counter of legsets
    n_pass = n_fail = n_unmap = 0
    unmap_examples = collections.Counter()
    nfiles = 0
    for f in files:
        try:
            op = gzip.open(f, "rt", newline="") if f.endswith(".gz") else open(f, "r", newline="")
            with op as fh:
                rd = csv.DictReader(fh)
                cols = [c for c in (rd.fieldnames or []) if c and "fail4b" in c.lower()]
                if not cols:
                    continue
                nfiles += 1
                loc = collections.Counter()
                for row in rd:
                    for c in cols:
                        v = row.get(c)
                        if v is None or str(v).strip() == "":
                            continue
                        legs, st = norm_failcell(v)
                        if st == "pass":
                            n_pass += 1
                        elif st == "fail":
                            n_fail += 1
                            rows[legs] += 1
                            loc[legs] += 1
                        else:
                            n_unmap += 1
                            unmap_examples[str(v).strip()[:40]] += 1
                if loc:
                    per_file[Path(f).name] = loc
        except Exception as e:                                   # a malformed CSV is reported
            unmap_examples[f"<unreadable {Path(f).name}: {type(e).__name__}>"] += 1
    return dict(rows=rows, per_file=per_file, n_pass=n_pass, n_fail=n_fail,
                n_unmap=n_unmap, unmap=unmap_examples, nfiles=nfiles)


# ==========================================================================================
def gates_pre(panels):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok, px = {}, panels[BINDING_PANEL]

    bad = 0
    for per in ("M", "W"):
        m0, _ = offset_mask(px.index, per, 0)
        bad += int((m0.values != rebalance_mask(px.index, per).values).sum())
    ok["G0"] = bad == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on M and W : {bad} differing rows  "
      f"{'PASS' if ok['G0'] else 'FAIL'}")

    w = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    ok["G2"] = g2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights                 : {g2:.3e}  "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    g1 = 0.0
    for per in ("W", "M"):
        m0, _ = offset_mask(px.index, per, 0)
        ctx = Ctx(px, m0)
        gr, tn = ctx.run(ctx.shift(w))
        fast = pd.Series(gr - tn * HEAD_COST / 1e4, index=px.index)
        slow = backtest(px, w, cost_bps=HEAD_COST, freq=per)["returns"]
        j = px.index[WARM]
        g1 = max(g1, float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max()))
    ok["G1"] = g1 < 1e-12
    P(f"  G1 ctx.run == engine.backtest @10 bps, worse of W and M     : {g1:.3e}  "
      f"{'PASS' if ok['G1'] else 'FAIL'}")

    a_ = Ctx(px, offset_mask(px.index, "M", 0)[0])
    b_ = Ctx(px, offset_mask(px.index, "M", 0)[0])
    bk = ranked_book(px, 0.75, 20)
    g5 = float(np.abs(a_.run(a_.shift(bk))[0] - b_.run(b_.shift(bk))[0]).max())
    ok["G5"] = g5 == 0.0
    P(f"  G5 determinism (canonical monthly re-derived)                : {g5:.3e}  "
      f"{'PASS' if ok['G5'] else 'FAIL'}")
    P("  G3 (idea 938 re-derived), G4 (phase fairness), G6 (compare) and G7 (census coverage) "
      "are scored in sections (B), (C), (G) and (H).")
    return ok


# ==========================================================================================
def main():
    t0 = time.time()
    P("IDEA 944  is-the-4b-DD-CAP-the-binding-leg-for-EVERY-offset-fragile-book  (lane B)")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   books {len(BOOKS)}   "
      f"phases {DOM_N} DOM + {NW_N} 4W + {DOW_N} DOW = {DOM_N + NW_N + DOW_N}   "
      f"cost {HEAD_COST:.0f} bps (PROTOCOL rule 2, not an axis)")
    P("the two tuned axes are CLAIM SET (census scope + book set) and PHASE GRID; every grid "
      "point is reported, none chosen")
    P()
    P("PRE-REGISTERED BARS (all at 10 bps; U56 is binding, B136 is a labelled replication)")
    P(f"  B1 CENSUS-AMONG  DD among the binding legs in >= {B1_BAR:.0%} of committed 4b FAIL "
      f"rows (row- AND file-weighted)")
    P(f"  B2 CENSUS-ALONE  DD alone is the MODAL binding set with share >= {B2_BAR:.0%} "
      f"(row- AND file-weighted)")
    P(f"  B3 PRICE-EVERY   over offset-fragile U56 book-cells, DD binds at EVERY failing phase "
      f"in >= {B3_BAR:.0%} of them")
    P(f"  B4 FLIP-RANK     DD's phase flip rate is STRICTLY the highest of the five legs over "
      f"all {len(BOOKS)} x 2 cells")
    P(f"  B5 SENS-RANK     MaxDD's normalised phase spread is largest of the five statistics "
      f"in >= {B5_BAR:.0%} of cells (reported separately; moves no mechanism verdict)")
    P("  VERDICT          H_DDBINDS requires B1+B2+B3+B4; any failure is H_MIXED and KILLS the "
      "generalisation of 938's 18-of-25 to the record.")
    P()

    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
    gk = gates_pre(panels)
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(B) THE PHASE GRID ITSELF (G4) -- fairness before performance")
    P("=" * 100)
    px = panels[BINDING_PANEL]
    GRID = offset_grid()
    yrs = (len(px.index) - WARM) / 252.0
    GRIDROWS, g4_bad = [], 0
    for fam, lab, spec in GRID:
        m, clipped = build_mask(px.index, spec)
        n = int(m.values[WARM:].sum())
        rpy = n / yrs
        if fam == "DOM" and not (11.5 <= rpy <= 12.5):
            g4_bad += 1
        GRIDROWS.append(dict(family=fam, offset=lab, reb_per_yr=rpy,
                             clipped_periods=clipped, n_rebalances=n))
    gk["G4"] = g4_bad == 0
    gd = pd.DataFrame(GRIDROWS)
    for fam in ("DOM", "4W", "DOW"):
        s = gd[gd.family == fam]
        P(f"     {fam:4s} n={len(s):2d}  reb/yr {s.reb_per_yr.min():.2f} .. "
          f"{s.reb_per_yr.max():.2f}   clipped periods {int(s.clipped_periods.sum())}")
    P(f"  G4 every DOM offset trades 11.5-12.5 times a year: {g4_bad} violations  "
      f"{'PASS' if gk['G4'] else 'FAIL'}")
    dump(gd, "grid")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P(f"(C) EVERY GRID POINT -- {len(BOOKS)} books x {len(GRID)} phases x {len(panels)} panels "
      f"@ {HEAD_COST:.0f} bps")
    P("=" * 100)
    ROWS = []
    for pn, ppx in panels.items():
        wts = {bn: fn(ppx) for bn, fn in BOOKS.items()}
        v2 = rules_v2_weights(ppx, BAND0, 0.75)
        for fam, lab, spec in GRID:
            m, _ = build_mask(ppx.index, spec)
            pc = panel_context(ppx, m)
            grv, tnv = pc["ctx"].run(pc["ctx"].shift(v2))
            mb, _, _ = score_stream(grv, tnv, pc, HEAD_COST)
            for bn, W in wts.items():
                gr, tn = pc["ctx"].run(pc["ctx"].shift(W))
                turn_yr = float(tn[pc["i0"]:].sum() / ((len(tn) - pc["i0"]) / 252.0))
                mm, mo, mi = score_stream(gr, tn, pc, HEAD_COST)
                lg = legs4b(mm, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"])
                ROWS.append(dict(
                    panel=pn, book=bn, family=fam, offset=lab, cost=HEAD_COST,
                    turn_yr=turn_yr, drag_bp_yr=turn_yr * HEAD_COST,
                    CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                    H1=mm["H1"], H2=mm["H2"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                    **{f"leg_{k}": bool(v) for k, v in lg.items()},
                    pass4b=bool(all(lg.values())), fail4b=failstr(lg),
                    pass4a=pass4a(mm, mb),
                    spy_CAGR=pc["spy"]["CAGR"], spy_Sharpe=pc["spy"]["Sharpe"],
                    spy_MaxDD=pc["spy"]["MaxDD"],
                    spy_oos_CAGR=pc["spy_oos"]["CAGR"],
                    spy_oos_Sharpe=pc["spy_oos"]["Sharpe"],
                    v2_Sharpe=mb["Sharpe"], v2_MaxDD=mb["MaxDD"]))
    off = pd.DataFrame(ROWS)
    dump(off, "phases")

    # ---- G3: idea 938's committed headline, re-derived from THIS file's code path ----
    B = off[(off.panel == BINDING_PANEL) & (off.book == "TOP20_g075")]
    mon = B[B.family != "DOW"]
    dom = B[B.family == "DOM"]
    n_fail938 = int((~mon.pass4b).sum())
    dd_alone938 = int((mon.fail4b == "DD").sum())
    dd_spread = (dom.MaxDD.max() - dom.MaxDD.min()) * 100
    cagr_spread = (dom.CAGR.max() - dom.CAGR.min()) * 100
    g3 = (n_fail938 == PUB938["n_fail"] and len(mon) == PUB938["n_monthly"]
          and dd_alone938 == PUB938["dd_alone"]
          and abs(dom.MaxDD.min() - PUB938["dd_min"]) < 5e-3
          and abs(dom.MaxDD.max() - PUB938["dd_max"]) < 5e-3
          and abs(dd_spread - PUB938["dd_spread_pp"]) < 0.5
          and abs(cagr_spread - PUB938["cagr_spread_pp"]) < 0.5)
    gk["G3"] = g3
    P(f"  G3 idea 938 re-derived on U56/TOP20_g075 @10 bps: {n_fail938} of {len(mon)} monthly "
      f"phases FAIL, {dd_alone938} of them on DD ALONE (published {PUB938['n_fail']} of "
      f"{PUB938['n_monthly']}, all DD-alone);")
    P(f"     DOM MaxDD support {dom.MaxDD.min():.2%} .. {dom.MaxDD.max():.2%} "
      f"({dd_spread:.2f} pp, published {PUB938['dd_spread_pp']:.2f}); DOM CAGR spread "
      f"{cagr_spread:.2f} pp (published {PUB938['cagr_spread_pp']:.2f})   "
      f"{'PASS' if g3 else 'FAIL'}")
    P()

    P(f"  the {len(BOOKS)} books at the CANONICAL month-end (DOM00), U56, for orientation:")
    P(f"     {'book':12s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
      f"{'turn/yr':>8s} {'OOSsh':>6s}  4b 4a  binding legs")
    for _, r in off[(off.panel == BINDING_PANEL) & (off.offset == "DOM00")].iterrows():
        P(f"     {r.book:12s} {r.CAGR:8.2%} {r.Sharpe:7.3f} {r.MaxDD:8.2%} {r.H1:6.3f} "
          f"{r.H2:6.3f} {r.turn_yr:8.2f} {r.OOS_Sharpe:6.3f}  "
          f"{'Y' if r.pass4b else 'n'}  {'Y' if r.pass4a else 'n'}   {r.fail4b}")
    sp = off[off.panel == BINDING_PANEL].iloc[0]
    P(f"     {'SPY':12s} {sp.spy_CAGR:8.2%} {sp.spy_Sharpe:7.3f} {sp.spy_MaxDD:8.2%}"
      f"     (4b bars: DD cap {0.60 * abs(sp.spy_MaxDD):.2%}, CAGR floor "
      f"{0.70 * sp.spy_CAGR:.2%}, OOS Sharpe bar {sp.spy_oos_Sharpe:.3f})")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) PER-CELL PHASE BEHAVIOUR -- fragility, binding legs, and leg FLIP rates")
    P("=" * 100)
    CELLS, FLIP = [], []
    for (pn, bn), g in off[off.family == "DOM"].groupby(["panel", "book"], sort=False):
        g = g.sort_values("offset")
        npass = int(g.pass4b.sum())
        fragile = 0 < npass < len(g)
        fails = g[~g.pass4b]
        dd_every = bool(len(fails) > 0 and fails.fail4b.map(lambda s: "DD" in s.split(",")).all())
        dd_alone_share = float((fails.fail4b == "DD").mean()) if len(fails) else np.nan
        flips = {k: bool(g[f"leg_{k}"].nunique() > 1) for k in LEGS}
        sens = {}
        for stat in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
            med = float(g[stat].median())
            sens[stat] = float((g[stat].max() - g[stat].min()) / abs(med)) if med != 0 else np.nan
        most = max(sens, key=lambda k: (sens[k] if np.isfinite(sens[k]) else -1))
        CELLS.append(dict(
            panel=pn, book=bn, n_phases=len(g), n_pass4b=npass, n_fail4b=len(fails),
            fragile=fragile, verdict_constant=not fragile,
            dd_binds_every_failing_phase=dd_every, dd_alone_share_of_fails=dd_alone_share,
            modal_fail_set=(fails.fail4b.mode().iloc[0] if len(fails) else "-"),
            n_distinct_fail_sets=int(fails.fail4b.nunique()) if len(fails) else 0,
            canon_pass4b=bool(g[g.offset == "DOM00"].pass4b.iloc[0]),
            canon_fail4b=str(g[g.offset == "DOM00"].fail4b.iloc[0]),
            canon_MaxDD_pctile=pct_rank(float(g[g.offset == "DOM00"].MaxDD.iloc[0]),
                                        g.MaxDD.values),
            **{f"flip_{k}": flips[k] for k in LEGS},
            **{f"sens_{k}": sens[k] for k in sens},
            most_sensitive=most,
            CAGR_spread_pp=float((g.CAGR.max() - g.CAGR.min()) * 100),
            MaxDD_spread_pp=float((g.MaxDD.max() - g.MaxDD.min()) * 100),
            Sharpe_spread=float(g.Sharpe.max() - g.Sharpe.min()),
            n_pass4a=int(g.pass4a.sum())))
    cells = pd.DataFrame(CELLS)
    dump(cells, "cells")

    P(f"     {'panel':5s} {'book':12s} {'4b pass/21':>10s} {'fragile':>7s} "
      f"{'DD@everyfail':>12s} {'DDalone':>8s} {'modal fail set':18s} "
      f"{'flips (H1 H2 OOS DD CAGR)':26s} {'most sens':>9s}")
    for _, r in cells.iterrows():
        fl = " ".join("Y" if r[f"flip_{k}"] else "." for k in LEGS)
        da = "-" if not np.isfinite(r.dd_alone_share_of_fails) else f"{r.dd_alone_share_of_fails:.2f}"
        P(f"     {r.panel:5s} {r.book:12s} {r.n_pass4b:5d}/{r.n_phases:<4d} "
          f"{'Y' if r.fragile else 'n':>7s} {'Y' if r.dd_binds_every_failing_phase else 'n':>12s} "
          f"{da:>8s} {r.modal_fail_set:18s} {fl:26s} {r.most_sensitive:>9s}")
    P()
    U = cells[cells.panel == BINDING_PANEL]
    for k in LEGS:
        P(f"     flip rate, leg {k:5s}: {cells[f'flip_{k}'].mean():.3f} over "
          f"{len(cells)} cells   (U56 only {U[f'flip_{k}'].mean():.3f} over {len(U)})")
    P()
    P("     normalised phase spread (max-min)/|median| over the 21 DOM phases, per statistic:")
    P(f"     {'panel':5s} {'book':12s} " + " ".join(f"{s:>8s}" for s in
                                                    ("CAGR", "Sharpe", "MaxDD", "H1", "H2")))
    for _, r in cells.iterrows():
        P(f"     {r.panel:5s} {r.book:12s} " +
          " ".join(f"{r[f'sens_{s}']:8.3f}" for s in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")))
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) THE CENSUS -- every committed 4b FAIL row in research/backtests, by binding leg")
    P("=" * 100)
    cen = run_census()
    tot = cen["n_fail"]
    P(f"  parsed {cen['nfiles']} committed CSVs carrying a fail4b-style column: "
      f"{tot:,} FAIL cells, {cen['n_pass']:,} PASS cells, {cen['n_unmap']:,} unmappable")
    cov = (tot + cen["n_pass"]) / max(1, tot + cen["n_pass"] + cen["n_unmap"])
    gk["G7"] = cov >= G7_BAR
    P(f"  G7 census coverage (mappable share of parsed cells): {cov:.4f}  "
      f"bar >= {G7_BAR:.2f}  {'PASS' if gk['G7'] else 'FAIL'}")
    if cen["unmap"]:
        P("     unmappable spellings (top 10, reported not dropped): " +
          "; ".join(f"{k!r} x{v}" for k, v in cen["unmap"].most_common(10)))
    P()
    CROWS = []
    for legs, n in cen["rows"].most_common():
        CROWS.append(dict(fail_set=",".join(k for k in LEGS if k in legs) or "-",
                          n_rows=n, row_share=n / tot, n_legs=len(legs),
                          **{f"has_{k}": (k in legs) for k in LEGS}))
    cdf = pd.DataFrame(CROWS)
    dump(cdf, "census")
    P(f"     {'binding set':22s} {'rows':>10s} {'share':>7s}   (top 15 of "
      f"{len(cdf)} distinct sets)")
    for _, r in cdf.head(15).iterrows():
        P(f"     {r.fail_set:22s} {r.n_rows:10,d} {r.row_share:7.3f}")
    P()
    among_rows = {k: float(cdf.loc[cdf[f"has_{k}"], "n_rows"].sum() / tot) for k in LEGS}
    alone_rows = {k: float(cdf.loc[(cdf.fail_set == k), "n_rows"].sum() / tot) for k in LEGS}
    # file-weighted: each file votes once with ITS OWN share, then average over files
    fw_among, fw_alone = {k: [] for k in LEGS}, {k: [] for k in LEGS}
    for fn, loc in cen["per_file"].items():
        t = sum(loc.values())
        for k in LEGS:
            fw_among[k].append(sum(n for s, n in loc.items() if k in s) / t)
            fw_alone[k].append(sum(n for s, n in loc.items() if s == frozenset({k})) / t)
    fw_among = {k: float(np.mean(v)) for k, v in fw_among.items()}
    fw_alone = {k: float(np.mean(v)) for k, v in fw_alone.items()}
    P(f"     {'leg':6s} {'among (rows)':>13s} {'among (files)':>14s} {'alone (rows)':>13s} "
      f"{'alone (files)':>14s}")
    for k in LEGS:
        P(f"     {k:6s} {among_rows[k]:13.3f} {fw_among[k]:14.3f} {alone_rows[k]:13.3f} "
          f"{fw_alone[k]:14.3f}")
    P(f"     (row-weighted n = {tot:,} FAIL cells; file-weighted n = "
      f"{len(cen['per_file'])} files, each voting once)")
    pd.DataFrame([dict(leg=k, among_rows=among_rows[k], among_files=fw_among[k],
                       alone_rows=alone_rows[k], alone_files=fw_alone[k]) for k in LEGS]
                 ).to_csv(OUT / f"{STEM}.censusleg.csv", index=False)
    P(f"  wrote {STEM}.censusleg.csv  (5 rows)")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) THE PRE-REGISTERED BARS, SCORED MECHANICALLY")
    P("=" * 100)
    HYP = []

    def bar(name, val, ok, detail):
        HYP.append(dict(bar=name, value=val, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"  {name:16s} {'PASS' if ok else 'FAIL'}   {detail}")
        return ok

    b1 = bar("B1 CENSUS-AMONG", among_rows["DD"],
             among_rows["DD"] >= B1_BAR and fw_among["DD"] >= B1_BAR,
             f"DD among the binding legs in {among_rows['DD']:.1%} of FAIL rows "
             f"({fw_among['DD']:.1%} file-weighted); bar >= {B1_BAR:.0%} on both. "
             f"largest leg by rows is "
             f"{max(among_rows, key=among_rows.get)} at {max(among_rows.values()):.1%}")
    modal = cdf.iloc[0].fail_set
    b2 = bar("B2 CENSUS-ALONE", alone_rows["DD"],
             modal == "DD" and alone_rows["DD"] >= B2_BAR and fw_alone["DD"] >= B2_BAR,
             f"DD alone is {alone_rows['DD']:.1%} of FAIL rows ({fw_alone['DD']:.1%} "
             f"file-weighted); the MODAL binding set is {modal!r} at "
             f"{cdf.iloc[0].row_share:.1%}; bar: modal == DD and share >= {B2_BAR:.0%} on both")
    frag = U[U.fragile]
    b3v = float(frag.dd_binds_every_failing_phase.mean()) if len(frag) else np.nan
    b3 = bar("B3 PRICE-EVERY", b3v,
             bool(len(frag) > 0 and b3v >= B3_BAR),
             f"{int(frag.dd_binds_every_failing_phase.sum())} of {len(frag)} offset-fragile "
             f"U56 cells have DD binding at EVERY failing phase "
             f"({b3v if np.isfinite(b3v) else float('nan'):.1%}); bar >= {B3_BAR:.0%}"
             + ("" if len(frag) else "  [no fragile cell exists -- bar cannot be met]"))
    fr = {k: float(cells[f"flip_{k}"].mean()) for k in LEGS}
    b4 = bar("B4 FLIP-RANK", fr["DD"],
             all(fr["DD"] > fr[k] for k in LEGS if k != "DD"),
             "flip rates " + " ".join(f"{k}={fr[k]:.2f}" for k in LEGS) +
             f"; bar: DD strictly highest (argmax = {max(fr, key=fr.get)})")
    b5v = float((cells.most_sensitive == "MaxDD").mean())
    b5 = bar("B5 SENS-RANK", b5v, b5v >= B5_BAR,
             f"MaxDD has the largest normalised phase spread in {b5v:.1%} of "
             f"{len(cells)} cells; bar >= {B5_BAR:.0%}. modal most-sensitive statistic = "
             f"{cells.most_sensitive.mode().iloc[0]}")
    mech = "H_DDBINDS" if (b1 and b2 and b3 and b4) else "H_MIXED"
    HYP.append(dict(bar="MECHANISM", value=np.nan, verdict=mech,
                    detail="H_DDBINDS requires B1+B2+B3+B4; any failure is H_MIXED"))
    P()
    P(f"  MECHANISM VERDICT: {mech}")
    dump(pd.DataFrame(HYP), "hypotheses")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(G) PROTOCOL RULE 8 -- WALK-FORWARD: phase AND book chosen on 2009-2016 ONLY, "
      "2017-2026 read once")
    P("=" * 100)
    WF = []
    for pn in panels:
        s = off[off.panel == pn]
        spy_o = dict(CAGR=float(s.spy_oos_CAGR.iloc[0]), Sharpe=float(s.spy_oos_Sharpe.iloc[0]))
        monly = s[s.family != "DOW"]
        choosers = {
            "CH_CANON_TOP20": s[(s.book == "TOP20_g075") & (s.offset == "DOM00")].iloc[0],
            "CH_CANON_RULESV2_W": s[(s.book == "RULESV2") & (s.offset == "DOW0")].iloc[0],
            "CH_IS_SHARPE_ANY": s.sort_values("IS_Sharpe", ascending=False).iloc[0],
            "CH_IS_SHARPE_MONTHLY": monly.sort_values("IS_Sharpe", ascending=False).iloc[0],
            "CH_IS_CAGR_ANY": s.sort_values("IS_CAGR", ascending=False).iloc[0],
            "CH_IS_MINDD_ANY": s.sort_values("IS_MaxDD", ascending=False).iloc[0],
        }
        oos_sorted = s.OOS_Sharpe.sort_values(ascending=False).values
        for nm, pick in choosers.items():
            rank = int((oos_sorted > pick.OOS_Sharpe).sum() + 1)
            WF.append(dict(panel=pn, chooser=nm, picked_book=pick.book, picked_phase=pick.offset,
                           IS_Sharpe=pick.IS_Sharpe, IS_CAGR=pick.IS_CAGR,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD, oos_rank=rank, n_grid=int(len(s)),
                           spy_oos_CAGR=spy_o["CAGR"], spy_oos_Sharpe=spy_o["Sharpe"],
                           beats_spy_oos=bool(pick.OOS_Sharpe > spy_o["Sharpe"]),
                           pass4b=bool(pick.pass4b), pass4a=bool(pick.pass4a)))
        # the phase-blind investor: mean over the whole DOM family, per book
        for bn in BOOKS:
            d = s[(s.book == bn) & (s.family == "DOM")]
            WF.append(dict(panel=pn, chooser=f"MEAN_DOM_{bn}", picked_book=bn,
                           picked_phase="(mean of 21)",
                           IS_Sharpe=float(d.IS_Sharpe.mean()), IS_CAGR=float(d.IS_CAGR.mean()),
                           OOS_CAGR=float(d.OOS_CAGR.mean()),
                           OOS_Sharpe=float(d.OOS_Sharpe.mean()),
                           OOS_MaxDD=float(d.OOS_MaxDD.mean()), oos_rank=-1, n_grid=int(len(d)),
                           spy_oos_CAGR=spy_o["CAGR"], spy_oos_Sharpe=spy_o["Sharpe"],
                           beats_spy_oos=bool(d.OOS_Sharpe.mean() > spy_o["Sharpe"]),
                           pass4b=bool(d.pass4b.mean() >= 0.5),
                           pass4a=bool(d.pass4a.mean() >= 0.5)))
    wf = pd.DataFrame(WF)
    dump(wf, "walkforward")
    sub = wf[wf.panel == BINDING_PANEL]
    P(f"  U56 @{HEAD_COST:.0f} bps, IS = 2009..2016 (choice), OOS = 2017..2026 (read once):")
    P(f"     {'chooser':26s} {'book':12s} {'phase':12s} {'IS Sh':>6s} {'OOS CAGR':>9s} "
      f"{'OOS Sh':>7s} {'OOS MaxDD':>10s} {'rank':>8s}  4b 4a")
    for _, q in sub.iterrows():
        rk = "n/a" if q.oos_rank < 0 else f"{q.oos_rank}/{q.n_grid}"
        P(f"     {q.chooser:26s} {q.picked_book:12s} {q.picked_phase:12s} {q.IS_Sharpe:6.3f} "
          f"{q.OOS_CAGR:9.2%} {q.OOS_Sharpe:7.3f} {q.OOS_MaxDD:10.2%} {rk:>8s}  "
          f"{'Y' if q.pass4b else 'n'}  {'Y' if q.pass4a else 'n'}")
    q0 = sub.iloc[0]
    P(f"     {'SPY (OOS)':26s} {'-':12s} {'-':12s} {'-':>6s} {q0.spy_oos_CAGR:9.2%} "
      f"{q0.spy_oos_Sharpe:7.3f}")
    v2o = off[(off.panel == BINDING_PANEL) & (off.book == "RULESV2") & (off.offset == "DOW0")].iloc[0]
    P(f"     {'RULES v2 baseline (OOS)':26s} {'-':12s} {'-':12s} {'-':>6s} "
      f"{v2o.OOS_CAGR:9.2%} {v2o.OOS_Sharpe:7.3f} {v2o.OOS_MaxDD:10.2%}")
    P()
    P("     OOS phase sensitivity of the binding leg, per book (U56, 21 DOM phases):")
    P(f"     {'book':12s} {'OOS CAGR min..max':>24s} {'OOS Sh min..max':>20s} "
      f"{'OOS MaxDD min..max':>22s}")
    for bn in BOOKS:
        d = off[(off.panel == BINDING_PANEL) & (off.book == bn) & (off.family == "DOM")]
        P(f"     {bn:12s} {d.OOS_CAGR.min():11.2%} ..{d.OOS_CAGR.max():10.2%} "
          f"{d.OOS_Sharpe.min():9.3f} ..{d.OOS_Sharpe.max():9.3f} "
          f"{d.OOS_MaxDD.min():11.2%} ..{d.OOS_MaxDD.max():9.2%}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(H) PROTOCOL RULE 3 CODE PATH -- baseline.compare() end to end (G6)")
    P("=" * 100)
    cmpres = {}
    for bn, per in (("TOP20_g075", "M"), ("BAND03_g075", "W")):
        d = compare(f"944 U56 {bn} {per} canonical", BOOKS[bn], panels[BINDING_PANEL],
                    freq=per, cost_bps=HEAD_COST)
        cmpres[(bn, per)] = d
        P(d["table"].to_string(float_format=lambda x: f"{x:.3f}"))
        P(f"  compare() verdict (4a, vs RULES v2): {d['verdict']}")
        P(d["row"])
        P()
    g6 = 0.0
    for (bn, per), d in cmpres.items():
        t = d["table"].iloc[0]
        lab = "DOM00" if per == "M" else "DOW0"
        f_ = off[(off.panel == BINDING_PANEL) & (off.book == bn) & (off.offset == lab)].iloc[0]
        g6 = max(g6, abs(float(t["CAGR"]) - float(f_.CAGR)),
                 abs(float(t["Sharpe"]) - float(f_.Sharpe)))
    gk["G6"] = g6 < 5e-3
    P(f"  G6 baseline.compare() == this file's fast runner on both canonical books: "
      f"max|d| {g6:.3e}  {'PASS' if gk['G6'] else 'FAIL'}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(I) SUMMARY")
    P("=" * 100)
    P(f"  gates: {sum(bool(v) for v in gk.values())} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failed'})")
    P(f"  MECHANISM: {mech}   (B1 {'PASS' if b1 else 'FAIL'}, B2 {'PASS' if b2 else 'FAIL'}, "
      f"B3 {'PASS' if b3 else 'FAIL'}, B4 {'PASS' if b4 else 'FAIL'}; "
      f"B5 {'PASS' if b5 else 'FAIL'} reported separately)")
    P(f"  CENSUS  {tot:,} committed FAIL cells over {cen['nfiles']} files: DD binds in "
      f"{among_rows['DD']:.1%} of them, alone in {alone_rows['DD']:.1%}; the modal binding set "
      f"is {modal!r} ({cdf.iloc[0].row_share:.1%}); "
      + ", ".join(f"{k} {among_rows[k]:.0%}" for k in LEGS))
    P(f"  PRICE   {int(cells.fragile.sum())} of {len(cells)} book-cells are offset-fragile; "
      f"leg flip rates " + " ".join(f"{k}={fr[k]:.2f}" for k in LEGS))
    P(f"  SENSITIVITY  MaxDD is the most phase-sensitive statistic in {b5v:.0%} of cells "
      f"(938's finding on TOP20: MaxDD spread {dd_spread:.2f} pp vs CAGR {cagr_spread:.2f} pp)")
    P(f"  NOTHING PROMOTED: no RULES change, no PROTOCOL edit, no version bump (rule 6).")
    P(f"  elapsed {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
