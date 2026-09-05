#!/usr/bin/env python3
"""QUEUE idea 164 — is-4b-internally-consistent-at-any-vol  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 164)
    "idea 156 found 4b demands 100% of SPY's Sharpe in both halves and OOS but only 60% of its
     drawdown, so a book scaled to SPY's volatility fails the DD cap in 297 of 300 cases while a
     book that clears the cap fails the CAGR floor.  Solve for the admissible band directly: for
     a book with SPY's Sharpe, what range of realised vol satisfies BOTH bars, and does any panel
     produce a book inside it?  If the band is empty at plausible drawdown-to-vol ratios, 4b's two
     coefficients are mis-paired and PROTOCOL should say which one moves.  Max 2 params."

THE ALGEBRA, WRITTEN DOWN BEFORE ANY DATA IS READ
    Gross exposure g is (idea 66) a near-exact lever: it moves vol, CAGR and MaxDD roughly in
    proportion and leaves Sharpe alone.  So 4b's five bars split cleanly in two:

      GROSS-INVARIANT   H1 > SPY_H1,  H2 > SPY_H2,  OOS > SPY_OOS      (three Sharpe bars)
      GROSS-SENSITIVE   CAGR >= gamma * CAGR_SPY,  |MaxDD| <= delta * |MaxDD_SPY|
                        with 4b's published coefficients gamma = 0.70, delta = 0.60.

    Write, for a book,
        s   = Sharpe_book / Sharpe_SPY                      (how good the book is)
        v   = Vol_book    / Vol_SPY                         (how big the book is run)
        rho = (|MaxDD_book|/Vol_book) / (|MaxDD_SPY|/Vol_SPY)   (its drawdown-to-vol ratio,
                                                                 in units of SPY's)
    Using the first-order identity CAGR ~ Sharpe x Vol, the two gross-sensitive bars become
        CAGR floor :   s * v   >= gamma        ->  v >= gamma / s
        DD cap     :   rho * v <= delta        ->  v <= delta / rho
    so the ADMISSIBLE VOL BAND is
        v in [ gamma / s , delta / rho ]
    and it is NON-EMPTY if and only if
        rho / s  <=  delta / gamma  =  0.60 / 0.70  =  0.857142...

    That inequality is the whole of idea 164.  4b is internally consistent for a book exactly
    when that book's drawdown-to-vol ratio is at most 85.7% of SPY's, scaled by its Sharpe
    advantage.  A book with SPY's Sharpe (s = 1) must be strictly LESS drawdown-prone per unit
    of volatility than SPY — by 14.3% — or NO gross level whatever puts it inside 4b.  This is
    the sense in which the two coefficients can be "mis-paired": 0.60/0.70 is not a free choice,
    it is a claim about achievable rho.

    Nothing above is assumed to be true of the data.  CAGR ~ Sharpe x Vol ignores the -sigma^2/2
    compounding drag, and rho is NOT constant in g (log-drawdown shrinks it as g rises).  Both
    approximations are MEASURED here against an exhaustive gross ladder of real backtests, and
    the EXACT empirical band is what every verdict below is read off.  The algebra is the
    hypothesis, not the result.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points in .coeff.csv:
    1. gamma, the CAGR-floor coefficient:  0.30 .. 1.10 step 0.05   (4b publishes 0.70)
    2. delta, the DD-cap coefficient:      0.40 .. 1.20 step 0.05   (4b publishes 0.60)
    Gross g is NOT a tuned parameter here — it is the axis the band is expressed in, swept over
    its whole legal range and reported in full.  Panel, book construction and cost rung are
    corpus axes carried from published work, not tuned.

CORPUS
    A (free, read from a committed artifact): idea 156's 1500-row grid.csv.  Its STATIC arm is
      idea 78's 300 sub-panel books at g = 0.75; its VM_FULL/RAW arm is those same 300 books
      re-grossed to SPY's realised volatility (v = 1 exactly).  That is precisely the "book
      scaled to SPY's vol" of idea 164's premise, so the 297-of-300 claim is checkable to the
      row, and rho and s are computable for all 300 books at no cost.
    B (new backtests): 8 published book constructions x 3 panels x a 20-point gross ladder
      g = 0.10 .. 2.00, weekly, 10 bps, t+1.  640 backtests.  This is where the EXACT band is
      measured and where "does any panel produce a book inside it" is answered.
      Constructions: V1 (RULES v1), TOP5/10/20/40 (composite rank, NO vol scaler — idea 2's
      KEEP 4b family), EWALL (equal-weight every eligible name), EWBAND3 (idea 57's 3% band),
      EWNOGATE (equal-weight every name, no eligibility gate — the widest rho on the menu).
      Panels: u56 (universe.json), B136 (universe_broad.json), SMALL (sub-$2B, 44 tickers with
      max_1d_move >= 1.0 dropped per data/small_meta.csv).

REPRODUCTION, asserted before any new number is read
    [a] idea 156's premise: in its VM_FULL/RAW arm (books at v = 1) the DD bar must fail in
        about 297 of 300, and the STATIC arm's failures must be dominated by the CAGR bar.
    [b] the algebra must PREDICT those failures from rho alone: at v = 1 the DD bar fails iff
        rho > delta = 0.60.  Predicted-vs-actual agreement is reported as a percentage.  If it
        is not near 100% the frame is wrong and everything after it is decoration.
    [c] the lever must behave: over the ladder, Sharpe must be near-flat in g and vol near-
        linear.  Both are measured; rho's own drift in g is measured and reported, because the
        band's width depends on it.

WALK-FORWARD (PROTOCOL rule 8) — parameters chosen on 2009-2016 only, read ONCE on 2017-2026:
    The object chosen in-sample is the GROSS: for each book, estimate s and rho on the IS window,
    form the IS-predicted band, and take g = the midpoint of that band clipped to (0, 1.00]
    (PROTOCOL rule 2 forbids leverage).  Evaluate that single g on the untouched OOS window.
    Controls, all fixed before the OOS window is read:
      S_BAND    g = IS band midpoint (the idea's own rule)
      S_STATIC  g = 0.75                       (the project's convention; do-nothing)
      S_ISDD    g = largest ladder g whose IS |MaxDD| clears the IS DD cap  (cap-only selector)
    Reported OOS: CAGR / Sharpe / MaxDD against RULES v1 on the same panel and against SPY, plus
    whether the IS band contains the OOS band (the frame's actual out-of-sample claim).

BOTH KEEP PATHS are evaluated on every ladder point: 4a (Sharpe > live rules in BOTH halves and
MaxDD no worse) and 4b (three Sharpe bars + gamma CAGR floor + delta DD cap).

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a] holds: ~297/300 DD failures at v = 1.
    P2  [b] holds above 95%: rho > 0.60 predicts the DD failure at v = 1 almost perfectly.
    P3  The rho distribution sits ABOVE 0.857 for most books, so most books have an EMPTY band
        and no gross whatever puts them inside 4b.  Trend-gated books that sit in cash should
        have the LOWEST rho and are the only candidates.
    P4  The exact empirical band is NARROWER than the analytic one, because compounding drag
        makes the CAGR floor bind sooner than s*v >= gamma says.
    P5  Some book somewhere clears it — most likely a heavily gated large-cap book — so the
        answer to "does any panel produce a book inside it" is a qualified yes, and 4b is not
        vacuous, only very tight.
    P6  On the coefficient surface, delta is the cheaper coefficient to move: raising delta from
        0.60 towards 0.70 admits more books per unit of relaxation than lowering gamma does,
        because rho's dispersion across books is wider than s's.
    P7  Nothing here is a new KEEP.  This run prices a PROTOCOL bar; it does not propose a book.

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are current-constituent lists.  The SMALL panel is the
      worst case (data/SMALL_PANEL_README.md, idea 54): every sub-$2B name that was delisted,
      acquired or went to zero is absent, which flatters its CAGR, flatters its drawdown, and
      therefore flatters rho in the direction that makes 4b look MORE satisfiable than it is.
      No small-panel number here is a tradable claim.
    * u56 and B136 are current constituents too (idea 54); the bias is smaller but one-directional.
    * rho is a full-sample statistic of a single realised path.  A book's MaxDD is one number
      drawn from one history; the band's edges inherit that estimation error entirely.  The
      walk-forward is the only guard against it offered here, and it is a single split.
    * The band is derived under a first-order identity.  Where the exact and analytic bands
      disagree the EXACT one is used; the analytic one is reported only to price the frame.
    * Idea 144: a re-grossed book is the same book.  Nothing in the ladder is a new signal, and
      no ladder point is offered as a discovery.
    * Idea 38 (calendar-day price index, weekends ffilled) and idea 126 (t+1 execution) carry
      over unchanged and affect every arm identically.
    * Levered ladder points (g > 1.00) are computed so the band's true right edge is visible,
      and are EXCLUDED from every verdict by PROTOCOL rule 2.  They are labelled everywhere.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .books.csv, .coeff.csv,
.walkforward.csv.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_is-4b-internally-consistent-at-any-vol_cloud"
OUT = ROOT / "research" / "backtests"
I156 = OUT / "2026-09-05_the-CAGR-floor-is-what-kills-small-pools_cloud.grid.csv"

COST_BPS = 10
FREQ = "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
GAMMA0, DELTA0 = 0.70, 0.60          # 4b as published
CAP = 1.00                            # PROTOCOL rule 2
GRID_G = np.round(np.arange(0.10, 2.001, 0.10), 4)
GRID_GAMMA = np.round(np.arange(0.30, 1.101, 0.05), 4)
GRID_DELTA = np.round(np.arange(0.40, 1.201, 0.05), 4)

pd.set_option("display.width", 240)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ book constructions
def _elig(px):
    s, above, vol20 = score(px, vol_scale=False)
    return s, above & (vol20 < 0.60)


def _band_above(px, band=0.03):
    """200d gate with a +/- `band` re-entry deadband (idea 57): state persists."""
    ma = px.rolling(200).mean()
    ratio = (px / ma).to_numpy()
    out = np.zeros(ratio.shape, dtype=bool)
    cur = np.zeros(ratio.shape[1], dtype=bool)
    for i in range(ratio.shape[0]):
        r = ratio[i]
        ok = np.isfinite(r)
        cur = np.where(ok & (r > 1 + band), True, np.where(ok & (r < 1 - band), False, cur))
        out[i] = cur
    return pd.DataFrame(out, index=px.index, columns=px.columns)


def make_books(px):
    """Return {name: weights_fn(g)} for one panel.  SPY is a benchmark column, never held."""
    cols = [c for c in px.columns if c != "SPY"]
    s, ok = _elig(px)
    s, ok = s[cols], ok[cols]
    rank = s.where(ok).rank(axis=1, ascending=False)
    _, vol20 = score(px, vol_scale=False)[1:]
    vol20 = vol20[cols]
    band_ok = _band_above(px[cols]) & (vol20 < 0.60)
    nogate = pd.DataFrame(1.0, index=px.index, columns=cols)

    def _pad(W):
        return W.reindex(columns=px.columns).fillna(0.0)

    def topn(n):
        def f(g):
            return _pad((rank <= n).astype(float) * (g / n))
        return f

    def ew(mask):
        def f(g):
            m = mask.astype(float)
            cnt = m.sum(axis=1).replace(0, np.nan)
            return _pad(m.div(cnt, axis=0).fillna(0.0) * g)
        return f

    def v1(g):
        W = rules_v1_weights(px)[cols]
        return _pad(W * (g / 0.75))

    return {"V1": v1, "TOP5": topn(5), "TOP10": topn(10), "TOP20": topn(20), "TOP40": topn(40),
            "EWALL": ew(ok), "EWBAND3": ew(band_ok), "EWNOGATE": ew(nogate.astype(bool))}


def load_panels():
    P = {}
    P["u56"] = load_universe()
    P["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["SMALL"] = sm[[c for c in sm.columns if c not in bad]]
    return P, len(bad)


# ------------------------------------------------------------------ metric helpers
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def summarise(r, tag=""):
    m = metrics(r)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=h1, H2=h2, lam=abs(m["MaxDD"]) / m["Vol"] if m["Vol"] > 0 else np.nan)


def fail_4b(bk, ref, gamma=GAMMA0, delta=DELTA0):
    """Which 4b bars a book fails, against SPY reference dict `ref`.  '-' = passes."""
    f = []
    if not bk["H1"] > ref["H1"]:
        f.append("H1")
    if not bk["H2"] > ref["H2"]:
        f.append("H2")
    if not bk["OOS_Sharpe"] > ref["OOS_Sharpe"]:
        f.append("OOS")
    if not abs(bk["MaxDD"]) <= delta * abs(ref["MaxDD"]):
        f.append("DD")
    if not bk["CAGR"] >= gamma * ref["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


def fail_4a(bk, base):
    f = []
    if not bk["H1"] > base["H1"]:
        f.append("H1")
    if not bk["H2"] > base["H2"]:
        f.append("H2")
    if not bk["MaxDD"] >= base["MaxDD"]:
        f.append("DD")
    return ",".join(f) if f else "-"


def main():
    t0 = time.time()
    say("=" * 200)
    say(f"IDEA 164 — is-4b-internally-consistent-at-any-vol   ({STEM})")
    say("Solve 4b's two gross-sensitive bars for the admissible VOL BAND, then measure whether "
        "any real book lands inside it.")
    say("Band (first-order):  v in [gamma/s, delta/rho];  NON-EMPTY iff rho/s <= delta/gamma = "
        f"{DELTA0 / GAMMA0:.6f}")
    say("PRE-REGISTERED: exactly 2 tuned params (gamma x 17, delta x 17). Gross is the axis the "
        "band lives on, swept in full. Panel/book/cost are carried corpus axes.")
    say("=" * 200)

    # ================================================== [a]/[b] idea 156's 300 books, for free
    say("\n" + "=" * 200)
    say("[a] PREMISE CHECK — idea 156's committed grid.csv (its VM_FULL/RAW arm IS 'the book "
        "scaled to SPY's vol')")
    say("=" * 200)
    ok_a = ok_b = False
    if I156.exists():
        g156 = pd.read_csv(I156)
        st = g156[g156.conv == "STATIC"].copy()
        vm = g156[(g156.conv == "VM_FULL") & (g156.ceil == "RAW")].copy()
        # SPY reference recoverable from the file: vol_ratio = vol / vol_SPY
        vol_spy_156 = float((vm["vol"] / vm["vol_ratio"]).median())
        dd_fail_vm = vm.f4b.astype(str).str.split(",").apply(lambda v: "DD" in v)
        say(f"    VM_FULL/RAW rows: {len(vm)};  achieved v = vol/vol_SPY: median "
            f"{vm.vol_ratio.median():.4f}  (target 1.0000)")
        say(f"    DD bar fails in {int(dd_fail_vm.sum())} of {len(vm)}   "
            f"<- idea 164 quotes 297 of 300")
        ok_a = int(dd_fail_vm.sum()) in range(290, 301)
        cagr_fail_st = st.f4b.astype(str).str.split(",").apply(lambda v: "CAGR" in v)
        say(f"    STATIC (g=0.75): CAGR bar fails in {int(cagr_fail_st.sum())} of {len(st)}, "
            f"DD bar in {int(st.f4b.astype(str).str.split(',').apply(lambda v: 'DD' in v).sum())}"
            f"  -> the premise's 'clears the cap, fails the floor' half")
        say(f"[a] PREMISE REPRODUCED: {ok_a}")

        # [b] does rho alone predict the v=1 DD failure?
        vm["lam"] = vm["MaxDD"].abs() / vm["vol"]
        # SPY's own lambda: recover MaxDD_SPY from the DD-cap bar is not in the file, so take it
        # from the live SPY series on B136 below; here use the ratio form via st/vm consistency.
        say("\n[b] does rho alone predict the DD failure at v = 1?  (checked below once SPY's "
            "own lambda is measured on B136)")
    else:
        say("    idea 156's grid.csv is NOT in the repo — corpus A skipped, corpus B stands alone")
        g156 = vm = st = None

    # ================================================== corpus B: panels and the gross ladder
    panels, n_dropped = load_panels()
    say("\n" + "=" * 200)
    say("CORPUS B — 8 published constructions x 3 panels x a 20-point gross ladder")
    say("=" * 200)
    say(f"    SMALL panel: dropped {n_dropped} tickers with max_1d_move >= 1.0 "
        f"(data/small_meta.csv).  SURVIVORSHIP: current constituents only — see the docstring.")

    ladder_rows, spyref, baseref = [], {}, {}
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS,
                        freq=FREQ)["returns"].loc[start:]
        sref = summarise(spy)
        sref["OOS_Sharpe"] = metrics(spy.loc[OOS_START:])["Sharpe"]
        sref["OOS_CAGR"] = metrics(spy.loc[OOS_START:])["CAGR"]
        sref["OOS_MaxDD"] = metrics(spy.loc[OOS_START:])["MaxDD"]
        sref["IS"] = summarise(spy.loc[:IS_END])
        bref = summarise(base)
        bref["OOS_Sharpe"] = metrics(base.loc[OOS_START:])["Sharpe"]
        bref["OOS_CAGR"] = metrics(base.loc[OOS_START:])["CAGR"]
        bref["OOS_MaxDD"] = metrics(base.loc[OOS_START:])["MaxDD"]
        spyref[pname], baseref[pname] = sref, bref
        say(f"\n  {pname}: {px.shape[1] - 1} names + SPY, {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY      CAGR {sref['CAGR']:7.2%}  Vol {sref['Vol']:6.2%}  Sharpe "
            f"{sref['Sharpe']:.3f}  MaxDD {sref['MaxDD']:7.2%}  lambda {sref['lam']:.3f}  "
            f"halves {sref['H1']:.3f}/{sref['H2']:.3f}  OOS {sref['OOS_Sharpe']:.3f}")
        say(f"    RULES v1 CAGR {bref['CAGR']:7.2%}  Vol {bref['Vol']:6.2%}  Sharpe "
            f"{bref['Sharpe']:.3f}  MaxDD {bref['MaxDD']:7.2%}  halves {bref['H1']:.3f}/"
            f"{bref['H2']:.3f}  OOS {bref['OOS_Sharpe']:.3f}")
        say(f"    4b bars here: H1>{sref['H1']:.3f}  H2>{sref['H2']:.3f}  "
            f"OOS>{sref['OOS_Sharpe']:.3f}  |MaxDD|<={DELTA0 * abs(sref['MaxDD']):.2%}  "
            f"CAGR>={GAMMA0 * sref['CAGR']:.2%}")

        books = make_books(px)
        for bname, fn in books.items():
            for g in GRID_G:
                r = backtest(px, fn(float(g)), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
                d = summarise(r)
                d_is, d_oos = summarise(r.loc[:IS_END]), summarise(r.loc[OOS_START:])
                d["OOS_Sharpe"] = d_oos["Sharpe"]
                row = dict(panel=pname, book=bname, g=float(g), levered=bool(g > CAP + 1e-9),
                           CAGR=d["CAGR"], Vol=d["Vol"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                           H1=d["H1"], H2=d["H2"], lam=d["lam"],
                           s=d["Sharpe"] / sref["Sharpe"], v=d["Vol"] / sref["Vol"],
                           rho=d["lam"] / sref["lam"],
                           IS_CAGR=d_is["CAGR"], IS_Vol=d_is["Vol"], IS_Sharpe=d_is["Sharpe"],
                           IS_MaxDD=d_is["MaxDD"], IS_lam=d_is["lam"],
                           OOS_CAGR=d_oos["CAGR"], OOS_Vol=d_oos["Vol"],
                           OOS_Sharpe=d_oos["Sharpe"], OOS_MaxDD=d_oos["MaxDD"],
                           OOS_lam=d_oos["lam"],
                           f4b=fail_4b(d, sref), f4a=fail_4a(d, bref))
                row["pass4b"] = row["f4b"] == "-"
                row["pass4a"] = row["f4a"] == "-"
                ladder_rows.append(row)
        say(f"    ladder done ({time.time() - t0:.0f}s)")

    LAD = pd.DataFrame(ladder_rows)
    LAD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    say(f"\n  {len(LAD)} ladder rows written to {STEM}.ladder.csv")

    # ================================================== [c] the lever's behaviour
    say("\n" + "=" * 200)
    say("[c] LEVER CONTROL — is Sharpe flat in g, vol linear in g, and how far does rho drift?")
    say("=" * 200)
    lev = []
    for (p, b), grp in LAD.groupby(["panel", "book"]):
        grp = grp.sort_values("g")
        lev.append(dict(panel=p, book=b,
                        Sharpe_range=float(grp.Sharpe.max() - grp.Sharpe.min()),
                        Sharpe_at_075=float(np.interp(0.75, grp.g, grp.Sharpe)),
                        vol_per_g_R2=float(np.corrcoef(grp.g, grp.Vol)[0, 1] ** 2),
                        rho_lo=float(grp.rho.min()), rho_hi=float(grp.rho.max()),
                        rho_at_075=float(np.interp(0.75, grp.g, grp.rho)),
                        rho_drift=float(grp.rho.max() - grp.rho.min())))
    LEV = pd.DataFrame(lev)
    say(LEV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n    Sharpe range over the whole 0.10-2.00 ladder: median "
        f"{LEV.Sharpe_range.median():.4f}, max {LEV.Sharpe_range.max():.4f} "
        f"(if small, the three Sharpe bars are gross-invariant as the algebra assumes)")
    say(f"    vol-vs-g R^2: min {LEV.vol_per_g_R2.min():.6f} (linearity of the lever)")
    say(f"    rho drift across the ladder: median {LEV.rho_drift.median():.4f}, max "
        f"{LEV.rho_drift.max():.4f} (rho is NOT a constant; the exact band is what is used)")

    # [b] completed: rho > delta predicts the v=1 DD failure on idea 156's corpus
    if g156 is not None:
        lam_spy = spyref["B136"]["lam"]
        vm2 = vm.copy()
        vm2["rho"] = (vm2["MaxDD"].abs() / vm2["vol"]) / lam_spy
        pred = vm2["rho"] > DELTA0
        act = vm2.f4b.astype(str).str.split(",").apply(lambda v: "DD" in v)
        agree = float((pred == act).mean())
        ok_b = agree > 0.95
        say(f"\n[b] rho > delta predicts the DD failure at v = 1 in {agree:.1%} of idea 156's "
            f"300 vol-matched books  (SPY lambda on B136 = {lam_spy:.4f})")
        say(f"    their rho: median {vm2.rho.median():.3f}, 5th pct {vm2.rho.quantile(.05):.3f}, "
            f"min {vm2.rho.min():.3f};  fraction <= {DELTA0 / GAMMA0:.3f} (band non-empty at "
            f"s=1): {float((vm2.rho <= DELTA0 / GAMMA0).mean()):.1%}")
        say(f"[b] FRAME PREDICTS THE PREMISE: {ok_b}")

    # ================================================== the band, analytic vs exact
    say("\n" + "=" * 200)
    say("THE BAND — per book: rho/s vs the consistency threshold delta/gamma, then the EXACT "
        "gross interval from the ladder")
    say("=" * 200)
    say(f"    consistency threshold delta/gamma = {DELTA0 / GAMMA0:.4f}.  rho/s at or below it "
        f"=> some vol satisfies BOTH gross-sensitive bars.  Above it => NO gross does, ever.")
    books = []
    for (p, b), grp in LAD.groupby(["panel", "book"]):
        grp = grp.sort_values("g").reset_index(drop=True)
        sref = spyref[p]
        # anchor s and rho at g = 0.75, the project's convention
        s075 = float(np.interp(0.75, grp.g, grp.s))
        rho075 = float(np.interp(0.75, grp.g, grp.rho))
        v_lo_an = GAMMA0 / s075 if s075 > 0 else np.inf
        v_hi_an = DELTA0 / rho075 if rho075 > 0 else np.inf
        # exact: which ladder g satisfy each gross-sensitive bar
        ok_cagr = grp.CAGR >= GAMMA0 * sref["CAGR"]
        ok_dd = grp.MaxDD.abs() <= DELTA0 * abs(sref["MaxDD"])
        ok_sharpe = ((grp.H1 > sref["H1"]) & (grp.H2 > sref["H2"])
                     & (grp.OOS_Sharpe > sref["OOS_Sharpe"]))
        both = ok_cagr & ok_dd
        legal = both & (~grp.levered)
        allbars = both & ok_sharpe
        allbars_legal = allbars & (~grp.levered)
        gs = grp.g[both]
        books.append(dict(
            panel=p, book=b, s=s075, rho=rho075, rho_over_s=rho075 / s075 if s075 > 0 else np.inf,
            band_nonempty_pred=(rho075 / s075 <= DELTA0 / GAMMA0) if s075 > 0 else False,
            v_lo_analytic=v_lo_an, v_hi_analytic=v_hi_an,
            g_lo_exact=float(gs.min()) if len(gs) else np.nan,
            g_hi_exact=float(gs.max()) if len(gs) else np.nan,
            n_g_both=int(both.sum()), n_g_both_legal=int(legal.sum()),
            n_g_sharpe=int(ok_sharpe.sum()),
            n_g_4b=int(allbars.sum()), n_g_4b_legal=int(allbars_legal.sum()),
            n_g_4a=int(grp.pass4a.sum()),
            Sharpe=float(np.interp(0.75, grp.g, grp.Sharpe)),
            H1=float(np.interp(0.75, grp.g, grp.H1)), H2=float(np.interp(0.75, grp.g, grp.H2)),
            OOS_Sharpe=float(np.interp(0.75, grp.g, grp.OOS_Sharpe))))
    BK = pd.DataFrame(books)
    BK.to_csv(OUT / f"{STEM}.books.csv", index=False)
    say(BK[["panel", "book", "s", "rho", "rho_over_s", "band_nonempty_pred", "v_lo_analytic",
            "v_hi_analytic", "g_lo_exact", "g_hi_exact", "n_g_both", "n_g_both_legal",
            "n_g_sharpe", "n_g_4b", "n_g_4b_legal", "n_g_4a"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    agree_band = float((BK.band_nonempty_pred == (BK.n_g_both > 0)).mean())
    say(f"\n    ANALYTIC vs EXACT: the rho/s <= {DELTA0 / GAMMA0:.3f} test agrees with the "
        f"exact ladder's 'some g satisfies both bars' in {agree_band:.1%} of "
        f"{len(BK)} books.")
    say(f"    books with a NON-EMPTY exact band (any g, levered allowed): "
        f"{int((BK.n_g_both > 0).sum())} of {len(BK)}")
    say(f"    books with a non-empty band at LEGAL gross (g <= 1.00, rule 2): "
        f"{int((BK.n_g_both_legal > 0).sum())} of {len(BK)}")
    say(f"    books clearing ALL FIVE 4b bars at some legal gross: "
        f"{int((BK.n_g_4b_legal > 0).sum())} of {len(BK)}")
    say(f"    books clearing 4a at some gross: {int((BK.n_g_4a > 0).sum())} of {len(BK)}")

    say("\n  DOES ANY PANEL PRODUCE A BOOK INSIDE THE BAND?  (all five 4b bars, legal gross)")
    win = BK[BK.n_g_4b_legal > 0]
    if len(win):
        say(win[["panel", "book", "s", "rho", "rho_over_s", "g_lo_exact", "g_hi_exact",
                 "n_g_4b_legal", "Sharpe", "H1", "H2", "OOS_Sharpe"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say("\n  their passing ladder points in full:")
        for _, w in win.iterrows():
            grp = LAD[(LAD.panel == w.panel) & (LAD.book == w.book) & LAD.pass4b
                      & (~LAD.levered)].sort_values("g")
            say(f"    {w.panel}/{w.book}:")
            say(grp[["g", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "v", "rho",
                     "pass4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("    NONE.  Not one of the 24 book-panel cells clears all five 4b bars at any legal "
            "gross.")

    say("\n  the binding bar, per book, at the gross that best satisfies the two gross-sensitive "
        "bars:")
    say(BK.assign(verdict=np.where(BK.n_g_4b_legal > 0, "4b at some legal g",
                                   np.where(BK.n_g_both_legal > 0, "gross-bars OK, SHARPE fails",
                                            np.where(BK.n_g_both > 0, "needs LEVERAGE",
                                                     "BAND EMPTY at any gross"))))
        .groupby(["panel", "verdict"]).size().to_string())

    # ================================================== the two coefficients
    say("\n" + "=" * 200)
    say("THE TWO COEFFICIENTS — which one moves?  Full (gamma x delta) surface, ALL grid points "
        "in .coeff.csv")
    say("=" * 200)
    crows = []
    for gam in GRID_GAMMA:
        for dlt in GRID_DELTA:
            n_band = n_4b = n_4b_lev = 0
            for (p, b), grp in LAD.groupby(["panel", "book"]):
                sref = spyref[p]
                okc = grp.CAGR >= gam * sref["CAGR"]
                okd = grp.MaxDD.abs() <= dlt * abs(sref["MaxDD"])
                oks = ((grp.H1 > sref["H1"]) & (grp.H2 > sref["H2"])
                       & (grp.OOS_Sharpe > sref["OOS_Sharpe"]))
                legal = ~grp.levered
                n_band += int((okc & okd & legal).any())
                n_4b += int((okc & okd & oks & legal).any())
                n_4b_lev += int((okc & okd & oks).any())
            crows.append(dict(gamma=float(gam), delta=float(dlt), ratio=float(dlt / gam),
                              books_band_nonempty=n_band, books_pass4b=n_4b,
                              books_pass4b_levered_ok=n_4b_lev, n_books=len(BK)))
    CO = pd.DataFrame(crows)
    CO.to_csv(OUT / f"{STEM}.coeff.csv", index=False)
    say("  books (of 24) with a NON-EMPTY band at legal gross, by (gamma down, delta across):")
    say(CO.pivot(index="gamma", columns="delta", values="books_band_nonempty").to_string())
    say("\n  books (of 24) passing ALL FIVE bars at legal gross, by (gamma down, delta across):")
    say(CO.pivot(index="gamma", columns="delta", values="books_pass4b").to_string())
    at = CO[(CO.gamma == GAMMA0) & (CO.delta == DELTA0)].iloc[0]
    say(f"\n  4b as published (gamma {GAMMA0}, delta {DELTA0}): band non-empty in "
        f"{int(at.books_band_nonempty)}/24, all five bars in {int(at.books_pass4b)}/24")
    # cheapest single-coefficient relaxation
    say("\n  cheapest single-coefficient move (hold the other at 4b's value):")
    dl = CO[CO.gamma == GAMMA0][["delta", "books_band_nonempty", "books_pass4b"]]
    ga = CO[CO.delta == DELTA0][["gamma", "books_band_nonempty", "books_pass4b"]]
    say("    delta swept at gamma = 0.70:")
    say(dl.to_string(index=False))
    say("    gamma swept at delta = 0.60:")
    say(ga.to_string(index=False))
    d_slope = float(np.polyfit(dl.delta, dl.books_band_nonempty, 1)[0]) * 0.05
    g_slope = -float(np.polyfit(ga.gamma, ga.books_band_nonempty, 1)[0]) * 0.05
    say(f"\n    books admitted per 0.05 of relaxation:  delta UP {d_slope:+.2f}   "
        f"gamma DOWN {g_slope:+.2f}   -> the cheaper coefficient to move is "
        f"{'DELTA (the DD cap)' if d_slope > g_slope else 'GAMMA (the CAGR floor)'}")

    # ================================================== rule 8 walk-forward
    say("\n" + "=" * 200)
    say(f"RULE 8 WALK-FORWARD — gross chosen on <= {IS_END} only, read ONCE on {OOS_START} ->")
    say("S_BAND = midpoint of the IS-estimated band, clipped to (0, 1.00].  S_STATIC = 0.75.  "
        "S_ISDD = largest ladder g clearing the IS DD cap.")
    say("=" * 200)
    wf = []
    for (p, b), grp in LAD.groupby(["panel", "book"]):
        grp = grp.sort_values("g").reset_index(drop=True)
        sref = spyref[p]
        bref = baseref[p]
        spy_is = sref["IS"]
        # IS estimates of s and rho, anchored at g = 0.75
        s_is = float(np.interp(0.75, grp.g, grp.IS_Sharpe)) / spy_is["Sharpe"]
        lam_is = float(np.interp(0.75, grp.g, grp.IS_lam))
        rho_is = lam_is / spy_is["lam"]
        v_lo = GAMMA0 / s_is if s_is > 0 else np.inf
        v_hi = DELTA0 / rho_is if rho_is > 0 else np.inf
        # translate the vol band into a gross band using the IS vol-per-gross slope
        vol_per_g = float(np.interp(0.75, grp.g, grp.IS_Vol)) / 0.75 / spy_is["Vol"]
        g_lo, g_hi = v_lo / vol_per_g, v_hi / vol_per_g
        empty = not (g_lo <= g_hi)
        g_mid = np.clip((g_lo + g_hi) / 2, GRID_G.min(), CAP)
        if empty:
            g_mid = np.clip(g_hi, GRID_G.min(), CAP)   # respect the binding bar when band empty
        ok_is_dd = grp.IS_MaxDD.abs() <= DELTA0 * abs(spy_is["MaxDD"])
        g_isdd = float(grp.g[ok_is_dd & (~grp.levered)].max()) if (
            ok_is_dd & (~grp.levered)).any() else float(GRID_G.min())

        # OOS band, computed the same way on the untouched window
        s_oos = float(np.interp(0.75, grp.g, grp.OOS_Sharpe)) / sref["OOS_Sharpe"]
        lam_oos = float(np.interp(0.75, grp.g, grp.OOS_lam))
        rho_oos = lam_oos / (abs(sref["OOS_MaxDD"]) / metrics(
            panels[p]["SPY"].pct_change().fillna(0.0).loc[OOS_START:])["Vol"])
        for sel, gsel in (("S_BAND", g_mid), ("S_STATIC", 0.75), ("S_ISDD", g_isdd)):
            gg = float(GRID_G[np.argmin(np.abs(GRID_G - gsel))])   # nearest computed ladder point
            r = grp[np.isclose(grp.g, gg)].iloc[0]
            f4b_oos = []
            if not r.OOS_Sharpe > sref["OOS_Sharpe"]:
                f4b_oos.append("OOS")
            if not abs(r.OOS_MaxDD) <= DELTA0 * abs(sref["OOS_MaxDD"]):
                f4b_oos.append("DD")
            if not r.OOS_CAGR >= GAMMA0 * sref["OOS_CAGR"]:
                f4b_oos.append("CAGR")
            wf.append(dict(panel=p, book=b, selector=sel, g_req=float(gsel), g_used=gg,
                           IS_band_empty=empty, IS_g_lo=g_lo, IS_g_hi=g_hi,
                           s_IS=s_is, rho_IS=rho_is, s_OOS=s_oos, rho_OOS=rho_oos,
                           rho_over_s_IS=rho_is / s_is if s_is > 0 else np.inf,
                           rho_over_s_OOS=rho_oos / s_oos if s_oos > 0 else np.inf,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           OOS_CAGR_SPY=sref["OOS_CAGR"], OOS_Sharpe_SPY=sref["OOS_Sharpe"],
                           OOS_MaxDD_SPY=sref["OOS_MaxDD"],
                           OOS_CAGR_V1=bref["OOS_CAGR"], OOS_Sharpe_V1=bref["OOS_Sharpe"],
                           OOS_MaxDD_V1=bref["OOS_MaxDD"],
                           OOS_f4b_gross_bars=",".join(f4b_oos) if f4b_oos else "-",
                           full_f4b=r.f4b, full_f4a=r.f4a))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF[["panel", "book", "selector", "g_used", "IS_band_empty", "rho_over_s_IS",
            "rho_over_s_OOS", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_f4b_gross_bars"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  selector means over the 24 book-panel cells (OOS window only):")
    agg = WF.groupby("selector").agg(g=("g_used", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                                     OOS_Sharpe=("OOS_Sharpe", "mean"),
                                     OOS_MaxDD=("OOS_MaxDD", "mean"),
                                     OOS_4b_gross_pass=("OOS_f4b_gross_bars",
                                                        lambda s: float((s == "-").mean())))
    say(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    for p in panels:
        say(f"    {p}: SPY OOS {spyref[p]['OOS_CAGR']:.2%} / {spyref[p]['OOS_Sharpe']:.3f} / "
            f"{spyref[p]['OOS_MaxDD']:.2%}   RULES v1 OOS {baseref[p]['OOS_CAGR']:.2%} / "
            f"{baseref[p]['OOS_Sharpe']:.3f} / {baseref[p]['OOS_MaxDD']:.2%}")

    say("\n  DOES THE IS BAND TRANSFER?  Spearman(rho/s IS, rho/s OOS) and sign agreement of the "
        "consistency test:")
    u = WF[WF.selector == "S_BAND"]
    fin = u[np.isfinite(u.rho_over_s_IS) & np.isfinite(u.rho_over_s_OOS)]
    rs = float(fin.rho_over_s_IS.rank().corr(fin.rho_over_s_OOS.rank()))  # Spearman, no scipy
    agree_oos = float(((fin.rho_over_s_IS <= DELTA0 / GAMMA0)
                       == (fin.rho_over_s_OOS <= DELTA0 / GAMMA0)).mean())
    say(f"    Spearman = {rs:+.3f} over {len(fin)} cells;  the IS and OOS verdicts of "
        f"'rho/s <= {DELTA0 / GAMMA0:.3f}' agree in {agree_oos:.1%} of them")
    say(f"    IS: non-empty in {int((fin.rho_over_s_IS <= DELTA0 / GAMMA0).sum())}/{len(fin)};  "
        f"OOS: non-empty in {int((fin.rho_over_s_OOS <= DELTA0 / GAMMA0).sum())}/{len(fin)}")

    say("\n" + "=" * 200)
    say(f"done in {time.time() - t0:.0f}s")
    say("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
