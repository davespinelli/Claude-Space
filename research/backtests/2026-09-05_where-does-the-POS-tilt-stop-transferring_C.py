#!/usr/bin/env python3
"""QUEUE idea 162 — where-does-the-POS-tilt-stop-transferring  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 162)
    "idea 152 found broad/POS passes 4b at m in [0.55,0.70], u56/POS only from m>=0.65, and
     small/POS fails all five bars at every gross, while idea 81 found each panel's winning
     tilt sign matches its own vol premium sign 3 of 3.  Build the intermediate panels (broad
     minus its ETFs, u56's 20 mega-caps, the small panel's top cap decile) and locate the
     market-cap boundary at which the vol premium's sign flips.  That boundary, not the tilt,
     is the universe clause.  Max 2 params."

THE ONE THING THIS RUN CANNOT DO, STATED FIRST
    **There is no market-capitalisation series committed to this repo.**  `data/` holds
    adjusted closes for three panels, share volume for the small panel only, and no shares
    outstanding anywhere.  So the boundary CANNOT be located in dollars of market cap, and any
    number in this file that looks like a cap threshold would be fabricated.  What the
    committed data does support is two orderings, and both are used and labelled:

      (A) a MEMBERSHIP ladder — the universes were built by size screens, so
          `mega20` (universe.json's own 'megacap' group) > `broad98` (universe_broad.json
          minus its ETFs) > `broad78` (broad98 minus the 20 megacaps) > the sub-$2B panel.
          This is an ordinal ladder from the universe files' construction, not a measurement.
      (B) a MEASURED liquidity ladder INSIDE the small panel — median daily dollar volume
          (adjusted close x share volume), which is the only continuous size-like variable
          the repo actually holds.  Deciles of it are real numbers in $/day.

    So the deliverable is: the sign flip is bracketed between two named rungs of (A), and
    (B) says whether the flip happens INSIDE the sub-$2B panel or at/above its ceiling.  The
    universe clause PROTOCOL can then state is a membership clause, not a dollar threshold —
    and that is the answer, not a workaround.

CORPUS
    11 panels (3 incumbents kept verbatim as reproduction anchors + 8 new), all price-only:
      u56      universe.json(56)                 anchor (20 megacap stocks + 36 ETFs)
      broad    universe_broad.json(136)          anchor (100 stocks + 36 ETFs)
      small    prices_small(439, SPY held out)   anchor
      mega20   universe.json['megacap']          "u56's 20 mega-caps"  (idea 162's words)
      broad98  broad minus its 36 ETFs (100)     "broad minus its ETFs" (idea 162's words)
      broad78  broad98 minus the 20 megacaps(80) the large-but-not-mega rung
      smADV5..smADV1  small split into 5 equal ADV quintiles (5 = most liquid)
    plus 10 ADV DECILES of the small panel, used for the premium statistic only (no books).
    2 cost rungs (10, 25 bps), weekly, t+1, long-only, gross held at 0.75, no leverage.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points in .grid.csv:
    1. the vol scaler, 3 values (idea 81's arms, its constructor IMPORTED verbatim):
           INV = composite / sqrt(vol20)   (RULES v1's live tilt)
           NONE = composite                (idea 2's standing book)
           POS = composite * sqrt(vol20)   (idea 81's near-miss)
    2. n, the book size, 2 values: 5 and 20.
    Panels, cost rungs, the ADV cut, the OOS window and every diagnostic are REPORTED axes,
    never selected on.  Gross 0.75, the 200d gate and vol20 < 0.60 are held at idea 81's /
    RULES v1's values throughout.

REPRODUCTION, asserted before any new number is read
    [a] INV / n=5 / w=0.15 must equal `baseline.rules_v1_weights` cell-for-cell on u56/broad.
    [b] idea 80's `fama_macbeth`, imported and called verbatim, must give idea 81's published
        bivariate vol20 slopes: u56 +0.00450 (t +3.90), broad +0.00294 (t +3.19),
        small -0.00084 (t -0.95); low-vol rank IC -0.0428 / -0.0332 / +0.0195.
    [c] the three new equity panels must be exact subsets of their parents by ticker.

THE WINDOW CONTROL (new here; idea 81 did not have it)
    The three anchors do not share a sample: prices.csv starts 2008, prices_small starts 2010.
    A premium that differs across panels could therefore be a WINDOW difference, not a size
    difference.  Every premium is reported TWICE — on each panel's own window and on the
    COMMON window (the latest of the 11 warm-up starts).  If the ladder only exists on own
    windows, there is no size boundary and the run says so.

WALK-FORWARD (PROTOCOL rule 8) — all selection rules fixed BEFORE any OOS number is read:
    Parameters chosen on the IS window only (start..2016-12-31), read ONCE on 2017-01-01..end.
      S1  plain IS Sharpe argmax over the 6 (scaler, n) points               [the incumbent]
      S2  SIGN selector: scaler = POS if the panel's IS-window vol20 slope > 0 else INV,
          then IS Sharpe argmax over n                                       [idea 162's rule]
      S3  do-nothing control: INV / n=5, i.e. the live tilt, never selected  [ideas 151/110]
      S4  do-nothing control: NONE / n=20, idea 2's standing book
    OOS CAGR / Sharpe / MaxDD reported for all four against RULES v1 (same panel, same cost)
    and SPY.  Both KEEP paths (4a and 4b) are evaluated at every grid point, on the full
    sample and again on the OOS window alone.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b], [c] all hold.
    P2  On the COMMON window the bivariate vol20 slope falls monotonically down membership
        ladder (A): mega20 >= broad98 >= broad78 >= smADV5 >= smADV1.
    P3  The flip is AT OR ABOVE the sub-$2B ceiling: no ADV decile of the small panel has a
        significantly positive (t >= +2) vol20 slope, i.e. the boundary is not inside (B).
    P4  The winning tilt's sign matches its panel's own premium sign in >= 6 of the 9
        book-carrying panels (idea 81 got 3 of 3 on the anchors).
    P5  The u56/broad premia stay positive on the COMMON window, so the ladder is not a
        sample-window artefact.
    P6  Cross-universe 4b stays 0: no (scaler, n) passes 4b on every equity panel, and any
        4b pass is confined to the broad family at 10 bps.
    P7  The SIGN selector S2 does NOT beat plain IS-Sharpe S1 on mean OOS Sharpe (ideas
        151/110 found no selector beats do-nothing).

CAVEATS carried, not buried
    * NO MARKET CAP DATA (above).  ADV is a liquidity proxy, and adjusted-close x raw share
      volume misstates dollar volume across splits; it is used only to ORDER names, never as
      a level, and the ordering is by the median over the common window.
    * Survivorship (idea 54): all panels are current-constituent lists.  The small panel drops
      the 44 tickers with max_1d_move >= 1.0 per data/small_meta.csv.  The bias runs AGAINST
      the small-panel result being conservative: the high-vol cohort a POS tilt buys is
      exactly where the delisted names would sit, so every POS number here is an upper bound.
    * The new equity panels have NO ETFs and therefore no cash-like or bond-like sleeve; their
      books are 100% equity by construction and are not comparable to u56/broad on drawdown.
    * SPY is the benchmark for every panel including the small ones (no IWM in the cache).
      Stated, not adjusted (idea 81's convention).
    * Idea 49/39: the eligibility gate is inverted on the small panel, so every small-family
      number describes a gate that does not work there.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so the IS
      drawdown bar admits too much, for every arm equally.
    * Idea 144: a de-grossed book is the same book.  Gross is held at 0.75 here, so no row is
      a gross-ladder claim; idea 152 already priced that ladder.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.

HARNESS
    `baseline` (the live rules), idea 94's window/halves/4a machinery, idea 129's panel and 4b
    bar machinery, idea 81's book constructor and idea 80's Fama-MacBeth are IMPORTED, so the
    arms are literally idea 81's arms, the premium is literally idea 80's premium, and the
    bars are literally 4b's.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .premium.csv, .adv.csv,
.walkforward.csv, .signmatch.csv.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_where-does-the-POS-tilt-stop-transferring_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I81 = OUT / "2026-09-05_vol20-as-the-hidden-ranking-key_cloud.py"
I80 = OUT / "2026-09-04_prox-inverted-signal_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
I81M = _load(I81, "i81")
I80M = _load(I80, "i80")

FREQ = "W"
COSTS = [10.0, 25.0]
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI0, DELTA0 = 0.70, 0.60
GROSS, MAX_VOL = 0.75, 0.60
SCALERS = ["INV", "NONE", "POS"]        # tuned parameter 1
NS = [5, 20]                            # tuned parameter 2

# the membership ladder (A), largest first; anchors are appended after it
LADDER = ["mega20", "broad98", "broad78", "smADV5", "smADV4", "smADV3", "smADV2", "smADV1"]
ANCHORS = ["u56", "broad", "small"]
BOOK_PANELS = ANCHORS + LADDER

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ panels
_PX = {}
_ADV = None


def _adv_table():
    """Median daily dollar volume per small-panel name.  ONLY size-like series in the repo."""
    global _ADV
    if _ADV is not None:
        return _ADV
    px, _, _ = C.panel("small")
    vol = load_volume(small=True)
    common = px.columns.intersection(vol.columns)
    dv = (px[common] * vol[common].reindex(px.index)).replace(0.0, np.nan)
    _ADV = dv.median(axis=0).dropna().sort_values(ascending=False)
    return _ADV


def _small_cut(k, q):
    """Bucket k (1 = least liquid .. q = most liquid) of the small panel by median ADV."""
    adv = _adv_table()
    names = list(adv.index)                       # descending ADV
    edges = np.linspace(0, len(names), q + 1).round().astype(int)
    lo, hi = edges[q - k], edges[q - k + 1]
    return names[lo:hi]


def etf_set():
    """ETFs = universe.json's three non-single-stock groups.  Data-derived, not hand-listed."""
    import json
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    return set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])


def megacap_list():
    import json
    return json.loads((ROOT / "research" / "universe.json").read_text())["megacap"]


def panel(name):
    """Returns (px_constituents, spy_daily_returns, description).  New panels exclude SPY as a
    tradable name; the three anchors are C.panel() verbatim so idea 81/152 reproduce."""
    if name in _PX:
        return _PX[name]
    if name in ANCHORS:
        _PX[name] = C.panel(name)
        return _PX[name]
    if name in ("mega20", "broad98", "broad78"):
        base = load_universe(broad=True) if name != "mega20" else load_universe()
        spy = base["SPY"].pct_change().fillna(0.0)
        etfs, mega = etf_set(), set(megacap_list())
        if name == "mega20":
            cols = [c for c in base.columns if c in mega]
            desc = "universe.json['megacap'](20 mega-cap stocks, no ETFs)"
        elif name == "broad98":
            cols = [c for c in base.columns if c not in etfs and c != "SPY"]
            desc = "universe_broad minus its ETFs (large-cap stocks only)"
        else:
            cols = [c for c in base.columns if c not in etfs and c not in mega and c != "SPY"]
            desc = "universe_broad minus ETFs minus the 20 megacaps (large-but-not-mega)"
        _PX[name] = (base[sorted(cols)], spy, f"{desc} [{len(cols)}]")
        return _PX[name]
    if name.startswith("smADV"):
        k = int(name[-1])
        px, spy, _ = C.panel("small")
        cols = _small_cut(k, 5)
        _PX[name] = (px[sorted(cols)], spy,
                     f"small panel ADV quintile {k}/5 ({'most' if k == 5 else 'least' if k == 1 else 'mid'} liquid) [{len(cols)}]")
        return _PX[name]
    if name.startswith("smDEC"):
        k = int(name[5:])
        px, spy, _ = C.panel("small")
        cols = _small_cut(k, 10)
        _PX[name] = (px[sorted(cols)], spy, f"small panel ADV decile {k}/10 [{len(cols)}]")
        return _PX[name]
    raise ValueError(name)


# ------------------------------------------------------------------ the book (idea 81's, verbatim)
def weights(px, scaler, n, pk):
    s, above, v = I81M.score_of(px, scaler, pk)
    elig = s.where(above & (v < MAX_VOL))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


# ------------------------------------------------------------------ the premium (idea 80's, verbatim)
def premium(px, pk, start):
    """Idea 80's Fama-MacBeth + low-vol rank IC on one panel from `start`.  The 'vol premium'
    is the BIVARIATE vol20 slope (idea 81's published statistic); the univariate slope and the
    low-vol IC are reported alongside so the sign is not read off one number."""
    el = I80M.eligible_mask(px)
    fm = I80M.fama_macbeth(px, el, start)
    wk, fwd, elw = I80M.weekly_panel(px, el, start)
    ic = I80M.ic_line(pd.Series(I80M.rank_ic(-I80M.vol20_of(px), wk.index, fwd, elw)))
    return dict(panel=pk, n_names=px.shape[1], n_weeks=fm["vol20_biv"][2],
                slope_biv=fm["vol20_biv"][0], t_biv=fm["vol20_biv"][1],
                slope_uni=fm["vol20_uni"][0], t_uni=fm["vol20_uni"][1],
                lowvol_IC=ic[0], t_IC=ic[1])


def main():
    say("=" * 215)
    say(f"IDEA 162 — where-does-the-POS-tilt-stop-transferring   ({STEM})")
    say("NO MARKET-CAP SERIES EXISTS IN THIS REPO.  The boundary is located on (A) a membership")
    say("ladder from the universe files and (B) a MEASURED median-dollar-volume ladder inside")
    say("the sub-$2B panel.  No dollar cap threshold is quoted, because none is derivable here.")
    say("PRE-REGISTERED: 2 tuned params (scaler x 3, n x 2).  Gross held 0.75.  All points reported.")
    say("=" * 215)

    # ---------------------------------------------------------------- panel construction + [c]
    say("\n" + "=" * 215)
    say("PANELS")
    say("=" * 215)
    starts = {}
    for pk in BOOK_PANELS:
        px, spy, desc = panel(pk)
        starts[pk] = px.index[260]
        say(f"  {pk:<8} {px.shape[1]:>4} cols  {px.index[0].date()}..{px.index[-1].date()}  "
            f"warm-up start {starts[pk].date()}  {desc}")
    COMMON = max(starts.values())
    say(f"\n  COMMON window for the cross-panel premium: {COMMON.date()} .. "
        f"{panel('small')[0].index[-1].date()}")

    mega, etfs = set(megacap_list()), etf_set()
    b_cols = set(panel("broad")[0].columns)
    ok_c = (set(panel("mega20")[0].columns) <= set(panel("u56")[0].columns)
            and set(panel("broad98")[0].columns) <= b_cols
            and set(panel("broad78")[0].columns) <= set(panel("broad98")[0].columns)
            and set(panel("broad98")[0].columns).isdisjoint(etfs)
            and set(panel("broad78")[0].columns).isdisjoint(mega)
            and set(panel("mega20")[0].columns) == mega & set(panel("u56")[0].columns))
    say(f"[c] new panels are exact subsets of their parents and ETF/mega-free as claimed: {ok_c}")
    sm_union = set()
    for k in range(1, 6):
        sm_union |= set(panel(f"smADV{k}")[0].columns)
    nsm = panel("small")[0].shape[1]
    say(f"[c] the 5 ADV quintiles partition the ADV-covered part of the small panel: "
        f"{len(sm_union)} names of {nsm} in the panel "
        f"({nsm - len(sm_union)} dropped for having no usable share-volume history); "
        f"disjoint quintiles: {len(sm_union) == sum(len(panel(f'smADV{k}')[0].columns) for k in range(1, 6))}")

    adv = _adv_table()
    advdf = adv.rename("median_daily_dollar_volume").to_frame()
    advdf["adv_rank"] = np.arange(1, len(adv) + 1)          # 1 = most liquid
    advdf["decile"] = 10 - np.minimum(9, (advdf.adv_rank - 1) * 10 // len(adv))
    advdf.to_csv(OUT / f"{STEM}.adv.csv")
    say(f"\n  ADV (median daily $ volume, adj close x share volume) over the small panel, "
        f"{len(adv)} names with volume:")
    q = adv.quantile([0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
    for k, v in q.items():
        say(f"      {int(k * 100):>3}th pct: ${v:,.0f}/day")

    # ---------------------------------------------------------------- [a] the INV arm IS the live book
    for pk in ("u56", "broad"):
        px, _, _ = panel(pk)
        d = float((I81M.weights(px, "INV", 5, fixedw=0.15, pk=pk) - rules_v1_weights(px))
                  .abs().max().max())
        say(f"[a] {pk}: INV/n=5/w=0.15 vs baseline.rules_v1_weights max|diff| = {d:.3e} "
            f"({'EXACT' if d < 1e-12 else 'NOT EXACT'})")

    # ---------------------------------------------------------------- the premium ladder
    say("\n" + "=" * 215)
    say("(1) THE VOL PREMIUM ON EVERY PANEL — own window and COMMON window")
    say("    'vol premium' = idea 80's BIVARIATE weekly Fama-MacBeth slope of next-week return")
    say("    on the percentile rank of vol20 among ELIGIBLE names.  Positive = high vol pays.")
    say("=" * 215)
    prows = []
    for pk in BOOK_PANELS + [f"smDEC{k}" for k in range(10, 0, -1)]:
        px, _, _ = panel(pk)
        for wname, st in (("own", px.index[260]), ("common", COMMON)):
            r = premium(px, pk, st)
            r.update(window=wname, start=str(st.date()),
                     ladder=(LADDER.index(pk) if pk in LADDER else -1))
            prows.append(r)
    P = pd.DataFrame(prows)
    P.to_csv(OUT / f"{STEM}.premium.csv", index=False)

    for wname in ("own", "common"):
        say(f"\n  --- {wname} window ---")
        say(f"  {'panel':<8} {'names':>5} {'weeks':>6} {'slope_biv':>11} {'t':>7} "
            f"{'slope_uni':>11} {'t':>7} {'lowvolIC':>9} {'t':>7}  sign")
        for _, r in P[P.window == wname].iterrows():
            say(f"  {r.panel:<8} {r.n_names:>5} {r.n_weeks:>6} {r.slope_biv:>+11.5f} "
                f"{r.t_biv:>+7.2f} {r.slope_uni:>+11.5f} {r.t_uni:>+7.2f} "
                f"{r.lowvol_IC:>+9.4f} {r.t_IC:>+7.2f}  "
                f"{'HIGH-VOL PAYS' if r.slope_biv > 0 else 'LOW-VOL PAYS'}")

    # [b] reproduction of idea 81's published slopes (own windows, its own panels)
    pub = {"u56": (0.00450, 3.90, -0.0428), "broad": (0.00294, 3.19, -0.0332),
           "small": (-0.00084, -0.95, 0.0195)}
    say("\n[b] REPRODUCTION of idea 81's published Fama-MacBeth (own windows):")
    ok_b = True
    for pk, (s, t, ic) in pub.items():
        r = P[(P.panel == pk) & (P.window == "own")].iloc[0]
        hit = abs(r.slope_biv - s) < 5e-5 and abs(r.t_biv - t) < 5e-3 and abs(r.lowvol_IC - ic) < 5e-4
        ok_b &= bool(hit)
        say(f"    {pk:<6} published {s:+.5f} (t {t:+.2f}), IC {ic:+.4f}  |  this run "
            f"{r.slope_biv:+.5f} (t {r.t_biv:+.2f}), IC {r.lowvol_IC:+.4f}  -> "
            f"{'MATCH' if hit else 'MISMATCH'}")
    say(f"[b] REPRODUCED: {ok_b}")

    # P2 / P3 / P5
    say("\n  P2 (monotone down membership ladder A, COMMON window):")
    lad = P[(P.window == "common") & (P.ladder >= 0)].sort_values("ladder")
    seq = list(lad.slope_biv)
    say("      " + " >= ".join(f"{p}:{s:+.5f}" for p, s in zip(lad.panel, seq)))
    mono = all(a >= b - 1e-12 for a, b in zip(seq, seq[1:]))
    say(f"      monotone non-increasing: {mono}  "
        f"(pairs in order: {sum(a >= b for a, b in zip(seq, seq[1:]))} of {len(seq) - 1})")
    dec = P[(P.window == "common") & (P.panel.str.startswith("smDEC"))]
    pos_sig = dec[(dec.slope_biv > 0) & (dec.t_biv >= 2.0)]
    say(f"\n  P3 (flip is at/above the sub-$2B ceiling): small-panel ADV deciles with a "
        f"significantly POSITIVE slope (t >= +2): {len(pos_sig)} of 10 "
        f"{list(pos_sig.panel) if len(pos_sig) else ''}")
    say(f"      decile slope range {dec.slope_biv.min():+.5f} .. {dec.slope_biv.max():+.5f}; "
        f"t range {dec.t_biv.min():+.2f} .. {dec.t_biv.max():+.2f}; "
        f"positive-signed deciles {int((dec.slope_biv > 0).sum())} of 10")
    u5 = P[(P.window == "common") & (P.panel.isin(["u56", "broad"]))]
    say(f"\n  P5 (large-cap premia survive the COMMON window): "
        f"u56 {u5[u5.panel == 'u56'].slope_biv.iloc[0]:+.5f} "
        f"(t {u5[u5.panel == 'u56'].t_biv.iloc[0]:+.2f}), "
        f"broad {u5[u5.panel == 'broad'].slope_biv.iloc[0]:+.5f} "
        f"(t {u5[u5.panel == 'broad'].t_biv.iloc[0]:+.2f})")

    # ---------------------------------------------------------------- the books
    say("\n" + "=" * 215)
    say("(2) THE BOOK GRID — 11 panels x 2 costs x 3 scalers x 2 n, every point reported")
    say("=" * 215)
    rows, rets, ref = [], {}, {}
    for pk in BOOK_PANELS:
        px, spy_full, desc = panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        ms_, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        Wv1 = rules_v1_weights(px)
        v1 = {c: backtest(px, Wv1, cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk] = dict(bfull=bfull, bIS=bIS, bOOS=bOOS, spy=ms_, spy_oos=mso, v1=v1, start=start)
        say(f"\n[panel] {pk}: {px.shape[1]} cols, eval from {start.date()} — {desc}")
        say(f"    SPY full {ms_['CAGR']:.2%}/{ms_['Sharpe']:.3f}/{ms_['MaxDD']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso['CAGR']:.2%}/{mso['Sharpe']:.3f}/"
            f"{mso['MaxDD']:.2%}")
        say(f"    4b bars here: H1 > {bfull['s1']:.3f}, H2 > {bfull['s2']:.3f}, OOS > "
            f"{bfull['soos']:.3f}, MaxDD shallower than {DELTA0 * abs(bfull['sdd']):.2%}, "
            f"CAGR >= {PHI0 * bfull['scagr']:.2%}")
        for c in COSTS:
            m_ = metrics(v1[c])
            say(f"    RULES v1 @{int(c)}bps: {m_['CAGR']:.2%}/{m_['Sharpe']:.3f}/{m_['MaxDD']:.2%}")
        for sc in SCALERS:
            for n in NS:
                W = weights(px, sc, n, pk)
                for c in COSTS:
                    res = backtest(px, W, cost_bps=c, freq=FREQ)
                    r = res["returns"].loc[start:]
                    to = res["turnover"].loc[start:]
                    rets[(pk, sc, n, c)] = r
                    mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
                    h1, h2 = H.halves(r)
                    ih1, ih2 = H.halves(H.window(r, "IS"))
                    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                    mgi = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    mgo = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                    rows.append(dict(
                        panel=pk, scaler=sc, n=n, cost=c,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        IS_H1=ih1, IS_H2=ih2,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        TO=to.sum() / mm["Years"],
                        gross=float(W.loc[start:].sum(axis=1).mean()),
                        mg_H1=mg["H1"], mg_H2=mg["H2"], mg_OOS=mg["OOS"],
                        mg_DD=mg["DD"], mg_CAGR=mg["CAGR"],
                        pass4a=H.pass4a(r, v1[c]),
                        pass4b=(len(C.fails(mg)) == 0), fail4b=",".join(C.fails(mg)) or "-",
                        pass4b_oos=all(mgo[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                        IS_adm=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR"))))
        sub = pd.DataFrame([x for x in rows if x["panel"] == pk])
        say("    " + sub[["scaler", "n", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                          "OOS_Sharpe", "TO", "pass4a", "pass4b", "fail4b"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n    "))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---------------------------------------------------------------- P4: sign match
    say("\n" + "=" * 215)
    say("(3) P4 — DOES THE WINNING TILT'S SIGN MATCH THE PANEL'S OWN VOL PREMIUM SIGN?")
    say("    winner = Sharpe argmax over the 3 scalers, at each (panel, n, cost); the panel's")
    say("    predicted tilt is POS/NONE when its own-window slope > 0 and INV when < 0.")
    say("=" * 215)
    srows = []
    for pk in BOOK_PANELS:
        sl = P[(P.panel == pk) & (P.window == "own")].iloc[0]
        for n in NS:
            for c in COSTS:
                sub = df[(df.panel == pk) & (df.n == n) & (df.cost == c)]
                win = sub.loc[sub.Sharpe.idxmax()]
                pred_high = sl.slope_biv > 0
                match = (win.scaler in ("POS", "NONE")) if pred_high else (win.scaler == "INV")
                srows.append(dict(panel=pk, n=n, cost=c, slope=sl.slope_biv, t=sl.t_biv,
                                  predicted=("POS/NONE" if pred_high else "INV"),
                                  winner=win.scaler, win_Sharpe=win.Sharpe,
                                  INV=sub[sub.scaler == "INV"].Sharpe.iloc[0],
                                  NONE=sub[sub.scaler == "NONE"].Sharpe.iloc[0],
                                  POS=sub[sub.scaler == "POS"].Sharpe.iloc[0],
                                  match=match))
    S = pd.DataFrame(srows)
    S.to_csv(OUT / f"{STEM}.signmatch.csv", index=False)
    say(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    bypanel = S.groupby("panel")["match"].mean()
    say(f"\n  cell-level match: {int(S.match.sum())} of {len(S)} "
        f"({S.match.mean():.1%})")
    say("  panel-level (majority of that panel's 4 cells):")
    pm = {}
    for pk in BOOK_PANELS:
        pm[pk] = bypanel[pk] > 0.5
        say(f"      {pk:<8} {bypanel[pk]:.0%} of cells match -> {'MATCH' if pm[pk] else 'MISS'}")
    say(f"  P4 (>= 6 of {len(BOOK_PANELS)} panels match): {sum(pm.values())} of {len(BOOK_PANELS)}"
        f" -> {'HELD' if sum(pm.values()) >= 6 else 'FAILED'}")

    # ---------------------------------------------------------------- 4a / 4b census, P6
    say("\n" + "=" * 215)
    say("(4) BOTH KEEP PATHS AT EVERY GRID POINT")
    say("=" * 215)
    say(f"  4a passes (beat the live book in BOTH halves, MaxDD no worse): "
        f"{int(df.pass4a.sum())} of {len(df)}")
    say(f"  4b passes (full sample):                                      "
        f"{int(df.pass4b.sum())} of {len(df)}")
    say(f"  4b passes on the OOS window alone:                            "
        f"{int(df.pass4b_oos.sum())} of {len(df)}")
    if df.pass4b.any():
        say("\n  every 4b pass:")
        say("  " + df[df.pass4b][["panel", "scaler", "n", "cost", "CAGR", "Sharpe", "MaxDD",
                                  "H1", "H2", "OOS_Sharpe", "mg_DD", "mg_CAGR"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    say("\n  which bar fails, by panel (10 bps, counts over 6 arms):")
    for pk in BOOK_PANELS:
        sub = df[(df.panel == pk) & (df.cost == 10.0)]
        fails = {}
        for f in sub.fail4b:
            for k in f.split(","):
                fails[k] = fails.get(k, 0) + 1
        say(f"      {pk:<8} " + ", ".join(f"{k}:{v}" for k, v in sorted(fails.items())))
    eq_panels = [p for p in BOOK_PANELS if p not in ("u56", "broad", "small")]
    cross = df[df.panel.isin(eq_panels)].groupby(["scaler", "n", "cost"]).pass4b.mean()
    say(f"\n  P6 (cross-universe 4b stays 0): arms passing 4b on EVERY equity panel: "
        f"{int((cross == 1.0).sum())} of {len(cross)} -> "
        f"{'HELD' if (cross == 1.0).sum() == 0 else 'FAILED'}")

    # ---------------------------------------------------------------- rule 8
    say("\n" + "=" * 215)
    say("(5) PROTOCOL RULE 8 — WALK-FORWARD.  Params on IS only; OOS read once.")
    say("=" * 215)
    wrows = []
    for pk in BOOK_PANELS:
        px, _, _ = panel(pk)
        # IS-window premium: computed on the IS window ONLY (selection may not see OOS)
        pxIS = px.loc[:IS_END]
        is_slope = premium(pxIS, pk + "_IS", pxIS.index[260])["slope_biv"]
        for c in COSTS:
            sub = df[(df.panel == pk) & (df.cost == c)]
            s1 = sub.loc[sub.IS_Sharpe.idxmax()]
            scal = "POS" if is_slope > 0 else "INV"
            s2sub = sub[sub.scaler == scal]
            s2 = s2sub.loc[s2sub.IS_Sharpe.idxmax()]
            s3 = sub[(sub.scaler == "INV") & (sub.n == 5)].iloc[0]
            s4 = sub[(sub.scaler == "NONE") & (sub.n == 20)].iloc[0]
            v1o = metrics(ref[pk]["v1"][c].loc[OOS_START:])
            spyo = ref[pk]["spy_oos"]
            for nm, pick in (("S1_ISsharpe", s1), ("S2_sign", s2), ("S3_INV5", s3),
                             ("S4_NONE20", s4)):
                wrows.append(dict(panel=pk, cost=c, selector=nm, IS_slope=is_slope,
                                  pick=f"{pick.scaler}/n={pick.n}",
                                  OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                  OOS_MaxDD=pick.OOS_MaxDD,
                                  v1_OOS_Sharpe=v1o["Sharpe"], v1_OOS_CAGR=v1o["CAGR"],
                                  v1_OOS_MaxDD=v1o["MaxDD"],
                                  spy_OOS_Sharpe=spyo["Sharpe"], spy_OOS_CAGR=spyo["CAGR"],
                                  spy_OOS_MaxDD=spyo["MaxDD"],
                                  beat_v1=pick.OOS_Sharpe > v1o["Sharpe"],
                                  beat_spy=pick.OOS_Sharpe > spyo["Sharpe"]))
    WF = pd.DataFrame(wrows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  mean OOS Sharpe by selector (over 22 panel x cost cells):")
    g = WF.groupby("selector").agg(OOS_Sharpe=("OOS_Sharpe", "mean"),
                                   OOS_CAGR=("OOS_CAGR", "mean"),
                                   OOS_MaxDD=("OOS_MaxDD", "mean"),
                                   beat_v1=("beat_v1", "mean"), beat_spy=("beat_spy", "mean"))
    say("  " + g.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    d = (WF[WF.selector == "S2_sign"].set_index(["panel", "cost"]).OOS_Sharpe
         - WF[WF.selector == "S1_ISsharpe"].set_index(["panel", "cost"]).OOS_Sharpe)
    say(f"\n  P7 (SIGN selector does NOT beat plain IS-Sharpe): mean dOOS_Sharpe "
        f"{d.mean():+.4f}, wins {int((d > 0).sum())} of {len(d)} -> "
        f"{'HELD' if d.mean() <= 0 else 'FAILED'}")
    say(f"  reference: RULES v1 mean OOS Sharpe {WF.v1_OOS_Sharpe.mean():.4f}, "
        f"SPY mean OOS Sharpe {WF.spy_OOS_Sharpe.mean():.4f}")

    # ---------------------------------------------------------------- verdict scaffold
    say("\n" + "=" * 215)
    say("PREDICTION SCORECARD")
    say("=" * 215)
    say(f"  P1 reproduction [a]/[b]/[c]     : b={ok_b}, c={ok_c}")
    say(f"  P2 monotone premium ladder      : {mono}")
    say(f"  P3 flip at/above the $2B ceiling: {len(pos_sig) == 0}")
    say(f"  P4 sign match >= 6 panels       : {sum(pm.values()) >= 6} ({sum(pm.values())}/11)")
    say(f"  P5 large-cap premia on common w : "
        f"{bool((u5.slope_biv > 0).all())}")
    say(f"  P6 cross-universe 4b = 0        : {(cross == 1.0).sum() == 0}")
    say(f"  P7 sign selector does not win   : {d.mean() <= 0}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.console.txt/.grid.csv/.premium.csv/.adv.csv/.walkforward.csv/.signmatch.csv")


if __name__ == "__main__":
    main()
