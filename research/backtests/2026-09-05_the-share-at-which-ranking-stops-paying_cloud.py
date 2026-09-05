#!/usr/bin/env python3
"""QUEUE idea 159 — the-share-at-which-ranking-stops-paying  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 159)
    "idea 153's regression gives a slope but PROTOCOL wants a NUMBER: the book share above
     which any cross-sectional key is arithmetic noise.  Fit the |dCAGR|-vs-share curve per
     panel and report the share at which the tilt's realised magnitude falls below the 10 bps
     cost of running it, with a bootstrap interval.  Bears on ideas 124 (book-size floor) and
     82 (ranking subtracts value).  Max 2 params."

WHAT IS AT STAKE.  Idea 153 established that book share q = n / n_eligible governs how much of
    a cross-sectional key a book can express (|dSharpe| on overlap: b -0.428, t -6.60,
    R2 0.429) and that the key's own Fama-MacBeth t does not (R2 0.028).  A slope is not a
    rule.  What PROTOCOL can actually write down is a THRESHOLD: above share q*, ranking on a
    key moves the book by less than the extra trading it costs, so the honest instruction is
    "do not rank, equal-weight the eligible set".  Idea 82 already found the gross-matched
    ranking premium NEGATIVE in 16 of 21 cells; idea 124 wants a book-size floor as a number.
    q* is the same object seen from the other end, and it is panel-relative rather than a raw
    name count, which is what makes it portable across universes.

THE TWO READINGS OF "FALLS BELOW THE COST", both pre-registered, R1 is the headline
    Let dCAGR_net(q) be the realised CAGR difference between a tilted book and its no-tilt
    control at the same share, at 10 bps, and let
        cost_tilt(q) = [Turnover(tilt) - Turnover(NONE)] x 10 bps    (annualised)
    be the extra trading bill the tilt runs up.
      R1 (idea 159's literal wording)  q* solves  mean_k |dCAGR_net|(q) = cost_tilt(q)
          "the tilt's realised magnitude falls below the 10 bps cost of running it".
      R2 (the breakeven reading)       q* solves  mean_k |dCAGR_gross|(q) = cost_tilt(q),
          with dCAGR_gross = dCAGR_net + cost_tilt, i.e. the pre-cost edge no longer covers
          its own bill.  R2 is mechanically the looser bar and is reported alongside.
    |.| is the pre-registered functional (idea 153): share can only govern the MAGNITUDE a key
    is able to express; the SIGN belongs to the panel's own premium.  Signed means are printed.

CORPUS — 3 panels x 14 shares x 7 keys, weekly, t+1, 10 bps, gross normalised to 0.75 across
the names actually held (idea 153's `norm` construction, which removes idea 73/81's de-grossing
confound).  294 backtests.
    Panels: u56 (universe.json), broad (universe_broad.json), small (sub-$2B, the 44 tickers
      with max_1d_move >= 1.0 dropped per data/small_meta.csv).
    Shares m: 0.03 0.05 0.075 0.10 0.15 0.20 0.27 0.35 0.45 0.53 0.65 0.75 0.90 1.00, realised
      as n = max(2, round(m x mean weekly eligible count)) — idea 153's convention verbatim, and
      a superset of its 7 points so its grid is reproducible cell-for-cell.
    Keys, all as a multiplicative tilt on idea 81's composite control (`NONE` = the composite
      alone, which is the no-extra-key book):
        INV  comp / sqrt(vol20)        (RULES v1's live tilt)
        POS  comp * sqrt(vol20)
        MOM  comp * pct-rank(12-1)     |
        R6   comp * pct-rank(6m)       |  the composite's own three legs (idea 158's ask)
        R3   comp * pct-rank(3m)       |
        RND  comp * pct-rank(fixed per-name random draw, seed 159_000)  — the NULL key.
      RND is drawn ONCE per panel and held constant in time, so it is a pure cross-sectional
      scramble with negligible turnover cost: whatever |dCAGR| it shows at a given share is the
      arithmetic noise floor that a real key has to beat.  It is pre-registered, not chosen.

TUNED PARAMETERS — exactly two, both swept exhaustively, ALL grid points reported:
    1. the book share m (14 values above).  This is the axis the answer is expressed in.
    2. the curve family fitted to |dCAGR| vs share, 3 values, all three reported and none
       preferred after the fact:  LIN  y = a + b q
                                  LOG  y = a + b ln q
                                  POW  ln y = a + b ln q
    Panels, keys, the cost rung, the construction and the OOS window are REPORTED corpus axes
    carried from idea 153, never selected on.

BOOTSTRAP — circular block bootstrap, block 21 trading days, B = 400 draws, seed 159_001.
    Within a panel every book is resampled on the SAME block index, so dCAGR stays paired and
    the interval is about sampling variation in the return path, not about which books were
    compared.  Turnover (and therefore cost_tilt) is held at its realised value and NOT
    resampled — stated, not hidden: the interval is on the edge, not on the bill.

REPRODUCTION, asserted before any new number is read
    [a] at idea 153's 7 shared shares, this script's NONE/INV/POS books at 10 bps must
        reproduce its committed `.grid.csv` `norm` rows cell-for-cell on CAGR, Sharpe, MaxDD,
        H1 and H2.  If [a] fails, this is not idea 153's curve and no q* below is comparable.
    [b] idea 153's headline sign must survive the finer grid: |dCAGR| falling in share.

WALK-FORWARD (PROTOCOL rule 8) — everything chosen on 2009-2016 (2011-2016 on small) only:
    q*_IS is fitted on the IS window alone and read ONCE against the untouched 2017-2026
    window.  Three arms, fixed before the OOS window is read:
        A_BELOW  best IS-Sharpe (key, share) among shares <= q*_IS
        A_ABOVE  best IS-Sharpe (key, share) among shares >  q*_IS
        A_NONE   the NONE control at A_BELOW's share  (do-nothing on ranking)
    Reported OOS CAGR / Sharpe / MaxDD against RULES v1 on the same panel and against SPY.
    Also reported: q*_OOS refitted on the OOS window, and whether it agrees with q*_IS.
BOTH KEEP PATHS (4a and 4b) are evaluated on all 294 books, full sample and OOS window.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a] reproduces exactly.
    P2  |dCAGR| falls monotonically in share on every panel and every key, RND included.
    P3  RND's curve sits BELOW the real keys' at small share and CONVERGES with them as share
        rises — that convergence point is q* by another route, and the two should roughly agree.
    P4  q* under R1 lands between 0.20 and 0.50 on the large-cap panels: well below idea 153's
        0.53 anchor and well below idea 2's standing KEEP (top-20 of ~37 eligible on u56 = 0.53).
        If so, the standing KEEP is ranking at a share where ranking has stopped paying, and its
        edge is the eligibility gate, not the ranking — idea 82's finding, reached independently.
    P5  The bootstrap interval is WIDE (a factor of two or more), because q* is the crossing of
        two shallow curves and a crossing angle that small is badly determined.  A wide interval
        is the honest answer and does not invalidate the point estimate.
    P6  The small panel's q* is much lower or undefined, because its keys pay so little that the
        curve is under the cost line at every share.
    P7  Nothing here is a KEEP; this run prices a PROTOCOL clause.

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are current-constituent lists (idea 54).  The small panel
      is the worst case (data/SMALL_PANEL_README.md): every sub-$2B name that delisted, was
      acquired or went to zero is absent, which inflates the measured payoff of ANY key there
      (the names that would have punished a ranking are the ones missing).  q* on `small` is
      therefore an upper bound on the true q*, and no small-panel number here is tradable.
    * Idea 49/39: the eligibility gate is INVERTED on the small panel, so n_eligible there is a
      count produced by a gate that does not work; its share axis is nominal.
    * q* is a crossing of two fitted curves and inherits the fit family.  Three families are
      reported; where they disagree the disagreement IS the result.
    * The cost side is realised turnover x 10 bps, a modelled bill, not a measured one; slippage
      and impact are not in it, so cost_tilt is a LOWER bound and q* is biased HIGH.
    * Idea 144: a re-shared book is a different book (n changes), unlike a re-grossed one, so
      the share axis is a real axis — but idea 153's confound (i) still holds: at m -> 1.00 the
      tilted and control books hold the same set and dCAGR -> 0 mechanically.  That endpoint is
      reported and every fit is run twice, with and without it.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution) carry over unchanged.

HARNESS
    Idea 153's committed script is IMPORTED and its `parts`, `eligible_mask`, `overlap`, `ols`
    and its panel/bar machinery (ideas 94/129) are called verbatim, so the control arm, the
    share convention and the 4a/4b bars are literally the committed ones.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .curve.csv, .qstar.csv,
.bootstrap.csv, .walkforward.csv.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_the-share-at-which-ranking-stops-paying_cloud"
OUT = ROOT / "research" / "backtests"
I153P = OUT / "2026-09-05_does-book-share-price-a-tilt_C.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I153 = _load(I153P, "i153")
C, H = I153.C, I153.H

FREQ, COST, GROSS, MAX_VOL = "W", 10.0, 0.75, 0.60
PANELS = ["u56", "broad", "small"]
IS_END, OOS_START = "2016-12-31", I153.OOS_START
SHARES = [0.03, 0.05, 0.075, 0.10, 0.15, 0.20, 0.27, 0.35, 0.45, 0.53, 0.65, 0.75, 0.90, 1.00]
KEYS = ["NONE", "INV", "POS", "MOM", "R6", "R3", "RND"]
TILTS = [k for k in KEYS if k != "NONE"]
FAMILIES = ["LIN", "LOG", "POW"]
B_BOOT, BLOCK, SEED_BOOT, SEED_RND = 400, 21, 159_001, 159_000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 800)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the books
_SC = {}


def score_of(px, key, pk):
    """idea 81's composite (imported verbatim), tilted by one cross-sectional key."""
    ck = (pk, key)
    if ck in _SC:
        return _SC[ck]
    comp, above, v = I153.parts(px)
    vv = v.clip(lower=0.08) ** 0.5
    if key == "NONE":
        s = comp
    elif key == "INV":
        s = comp / vv
    elif key == "POS":
        s = comp * vv
    elif key in ("MOM", "R6", "R3"):
        raw = {"MOM": px.shift(21) / px.shift(252) - 1,
               "R6": px / px.shift(126) - 1,
               "R3": px / px.shift(63) - 1}[key]
        s = comp * raw.rank(axis=1, pct=True)
    elif key == "RND":
        rng = np.random.default_rng(SEED_RND + PANELS.index(pk))   # deterministic, not hash()
        draw = pd.Series(rng.random(px.shape[1]), index=px.columns)
        s = comp * draw.rank(pct=True)          # fixed per-name scramble, no turnover cost
    else:
        raise ValueError(key)
    _SC[ck] = (s, above, v)
    return _SC[ck]


def held_mask(px, key, n, pk):
    s, above, v = score_of(px, key, pk)
    return s.where(above & (v < MAX_VOL)).rank(axis=1, ascending=False) <= n


def weights(px, key, n, pk):
    """idea 153's `norm` construction: gross 0.75 spread over the names actually held."""
    m = held_mask(px, key, n, pk).astype(float)
    k = m.sum(axis=1).replace(0, np.nan)
    return m.div(k, axis=0).fillna(0.0) * GROSS


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fit(x, y, fam):
    """Return f(q) for the fitted family, or None if the family cannot take these data."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if fam == "LIN":
        b = np.polyfit(x, y, 1)
        return lambda q: np.polyval(b, q)
    if fam == "LOG":
        b = np.polyfit(np.log(x), y, 1)
        return lambda q: np.polyval(b, np.log(q))
    ok = y > 0
    if ok.sum() < 3:
        return None
    b = np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)
    return lambda q: np.exp(np.polyval(b, np.log(q)))


# the crossing is searched ONLY over the range of shares actually backtested — never
# extrapolated below the smallest one, which is where a log fit misbehaves.
QQ = np.linspace(min(SHARES), 1.00, 971)
Q_LEFT = float(QQ[0])


def crossing(fedge, fcost):
    """Smallest q in [min(SHARES), 1.00] at which the edge curve drops below the cost curve.
    Returns Q_LEFT if the edge is ALREADY below at the smallest share tested (read as 'noise
    at every share measured', not as a located threshold), NaN if it never crosses."""
    if fedge is None or fcost is None:
        return np.nan
    d = fedge(QQ) - fcost(QQ)
    neg = np.where(d < 0)[0]
    if len(neg) == 0:
        return np.nan                     # edge never falls below cost on the grid
    i = neg[0]
    if i == 0:
        return Q_LEFT                     # already below at the smallest share tested
    q0, q1, d0, d1 = QQ[i - 1], QQ[i], d[i - 1], d[i]
    return float(q0 + (q1 - q0) * d0 / (d0 - d1))


def main():
    t0 = time.time()
    say("=" * 195)
    say(f"IDEA 159 — the-share-at-which-ranking-stops-paying   ({STEM})")
    say("Fit |dCAGR| vs book share per panel; report the share at which a cross-sectional key's "
        "realised magnitude falls below the 10 bps cost of running it, with a block-bootstrap "
        "interval.")
    say("PRE-REGISTERED: exactly 2 tuned params (share x 14, curve family x 3). Panels, keys, "
        "cost rung, construction and the OOS window are carried corpus axes.")
    say(f"R1 (headline, idea 159's wording): |dCAGR_net| = cost_tilt.   "
        f"R2 (breakeven): |dCAGR_net| + cost_tilt = cost_tilt.")
    say("=" * 195)

    rows, rets, ref, nmap = [], {}, {}, {}
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        el = I153.eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        ref[pk] = dict(px=px, start=start, spy=ms, spy_oos=mso, spy_r=spy, bfull=bfull,
                       bIS=bIS, bOOS=bOOS, v1=v1, n_elig=n_elig, desc=desc)
        nmap[pk] = {m: max(2, int(round(m * n_elig))) for m in SHARES}
        m1, mo1 = metrics(v1), metrics(v1.loc[OOS_START:])
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval from {start.date()}, mean "
            f"weekly eligible names {n_elig:.1f}")
        say("    share -> n:  " + ", ".join(f"{m:.3g}->{nmap[pk][m]}" for m in SHARES))
        say(f"    SPY  {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso['CAGR']:.2%}/{mso['Sharpe']:.3f}/"
            f"{mso['MaxDD']:.2%}")
        say(f"    RULES v1 @10bps {m1['CAGR']:.2%}/{m1['Sharpe']:.3f}/{m1['MaxDD']:.2%} | OOS "
            f"{mo1['CAGR']:.2%}/{mo1['Sharpe']:.3f}/{mo1['MaxDD']:.2%}")

        for m in SHARES:
            n = nmap[pk][m]
            for key in KEYS:
                res = backtest(px, weights(px, key, n, pk), cost_bps=COST, freq=FREQ)
                r = res["returns"].loc[start:]
                rets[(pk, m, key)] = r
                mm, mo = metrics(r), metrics(r.loc[OOS_START:])
                h1, h2 = halves(r)
                to = float(res["turnover"].loc[start:].sum() / mm["Years"])
                hm = held_mask(px, key, n, pk).loc[start:]
                rows.append(dict(
                    panel=pk, m=m, n=n, key=key, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                    MaxDD=mm["MaxDD"], H1=h1, H2=h2, TO=to,
                    n_held=float(hm.sum(axis=1).mean()),
                    realised_share=float((hm.sum(axis=1) / el.sum(axis=1).replace(0, np.nan))
                                         .mean()),
                    IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                    IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                    IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
        say(f"    {len(KEYS) * len(SHARES)} books done ({time.time() - t0:.0f}s)")

    G = pd.DataFrame(rows)
    # 4a / 4b via idea 129's committed bars
    v4a, v4b, v4bo = [], [], []
    PHI0, DELTA0 = 0.70, 0.60          # 4b as published
    for _, r0 in G.iterrows():
        R = rets[(r0.panel, r0.m, r0.key)]
        b = ref[r0.panel]
        v4a.append(H.pass4a(R, b["v1"]))
        f = C.fails(C.margins_at(R, b["bfull"], PHI0, DELTA0, "full"))
        fo = C.fails(C.margins_at(R, b["bOOS"], PHI0, DELTA0, "OOS"))
        v4b.append(",".join(f) if f else "-")
        v4bo.append(",".join(fo) if fo else "-")
    G["pass4a"] = v4a
    G["fail4b"] = v4b
    G["fail4b_oos"] = v4bo
    G["pass4b"] = G.fail4b.astype(str).eq("-")
    G["pass4b_oos"] = G.fail4b_oos.astype(str).eq("-")
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n  {len(G)} books written to {STEM}.grid.csv")
    say(f"  KEEP paths across all {len(G)} books: 4a passes {int(G.pass4a.sum())}, "
        f"4b passes {int(G.pass4b.sum())}, 4b on the OOS window {int(G.pass4b_oos.sum())}")

    # ============================================================ [a] reproduction of idea 153
    say("\n" + "=" * 195)
    say("[a] REPRODUCTION — idea 153's committed grid.csv, `norm` construction, 10 bps, its 7 "
        "shared shares x INV/NONE/POS")
    say("=" * 195)
    ok_a = False
    ref153 = OUT / "2026-09-05_does-book-share-price-a-tilt_C.grid.csv"
    if ref153.exists():
        R153 = pd.read_csv(ref153)
        R153 = R153[(R153.constr == "norm") & (R153.cost == 10.0)]
        R153 = R153.rename(columns={"tilt": "key"}).set_index(["panel", "m", "key"]).sort_index()
        mine = G[G.key.isin(["INV", "NONE", "POS"]) & G.m.isin(sorted(set(R153.index.get_level_values("m"))))]
        mine = mine.set_index(["panel", "m", "key"]).sort_index()
        common = mine.index.intersection(R153.index)
        say(f"    overlapping cells: {len(common)} (expect 63 = 3 panels x 7 shares x 3 keys)")
        ok_a = len(common) == 63
        for c in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
            dmax = float((mine.loc[common, c] - R153.loc[common, c]).abs().max())
            ok_a &= dmax < 1e-9
            say(f"    max|diff| {c:<7} = {dmax:.3e}")
        say(f"[a] REPRODUCED EXACTLY: {ok_a}")
    else:
        say("    idea 153's grid.csv absent — reproduction skipped")

    # ============================================================ the curve
    say("\n" + "=" * 195)
    say("THE CURVE — |dCAGR| and the tilt's own trading bill, per panel x share (mean over the "
        "6 keys; RND printed separately as the noise floor)")
    say("=" * 195)
    crows = []
    for pk in PANELS:
        for m in SHARES:
            base = G[(G.panel == pk) & (G.m == m) & (G.key == "NONE")].iloc[0]
            per = {}
            for k in TILTS:
                t = G[(G.panel == pk) & (G.m == m) & (G.key == k)].iloc[0]
                per[k] = dict(dCAGR=t.CAGR - base.CAGR, dSharpe=t.Sharpe - base.Sharpe,
                              dTO=t.TO - base.TO, cost=(t.TO - base.TO) * COST / 1e4)
            real = [v for k, v in per.items() if k != "RND"]
            crows.append(dict(
                panel=pk, m=m, n=int(base.n),
                absdC=float(np.mean([abs(v["dCAGR"]) for v in real])),
                dC_signed=float(np.mean([v["dCAGR"] for v in real])),
                absdS=float(np.mean([abs(v["dSharpe"]) for v in real])),
                cost=float(np.mean([max(v["cost"], 0.0) for v in real])),
                dTO=float(np.mean([v["dTO"] for v in real])),
                absdC_RND=abs(per["RND"]["dCAGR"]), cost_RND=max(per["RND"]["cost"], 0.0),
                **{f"dC_{k}": per[k]["dCAGR"] for k in TILTS}))
    CU = pd.DataFrame(crows)
    CU["absdC_gross"] = CU.absdC + CU.cost
    CU.to_csv(OUT / f"{STEM}.curve.csv", index=False)
    for pk in PANELS:
        say(f"\n  {pk}:")
        say(CU[CU.panel == pk][["m", "n", "absdC", "cost", "absdC_gross", "dC_signed", "absdS",
                                "dTO", "absdC_RND", "cost_RND"]
                               + [f"dC_{k}" for k in TILTS]]
            .to_string(index=False, float_format=lambda x: f"{x:.5f}"))
        s = CU[CU.panel == pk]
        mono = bool((np.diff(s.absdC.values) <= 1e-12).all())
        sp = float(pd.Series(s.m.values).rank().corr(pd.Series(s.absdC.values).rank()))
        sp_r = float(pd.Series(s.m.values).rank().corr(pd.Series(s.absdC_RND.values).rank()))
        say(f"    [b] |dCAGR| monotonically NON-INCREASING in share: {mono};  "
            f"Spearman(share, |dCAGR|) = {sp:+.3f};  same for the RANDOM key = {sp_r:+.3f}")
        say(f"    RND noise floor vs the real keys: |dCAGR| ratio real/RND at m=0.05 "
            f"{s[s.m == 0.05].absdC.iloc[0] / max(s[s.m == 0.05].absdC_RND.iloc[0], 1e-9):.2f}x, "
            f"at m=0.53 "
            f"{s[s.m == 0.53].absdC.iloc[0] / max(s[s.m == 0.53].absdC_RND.iloc[0], 1e-9):.2f}x")

    # ============================================================ q*
    say("\n" + "=" * 195)
    say("q* — THE NUMBER.  Crossing of the fitted |dCAGR| curve with the fitted cost curve, all "
        "3 families, with and without the mechanical m = 1.00 endpoint")
    say("=" * 195)
    qrows = []
    for pk in PANELS:
        for drop in (False, True):
            s = CU[(CU.panel == pk) & ((CU.m < 1.0) if drop else True)]
            for fam in FAMILIES:
                fc = fit(s.m, s.cost, fam)
                q1 = crossing(fit(s.m, s.absdC, fam), fc)
                q2 = crossing(fit(s.m, s.absdC_gross, fam), fc)
                qn = crossing(fit(s.m, s.absdC, fam), fit(s.m, s.absdC_RND, fam))
                qrows.append(dict(panel=pk, family=fam, drop_m1=drop,
                                  q_star_R1=q1, q_star_R2=q2, q_cross_RND=qn,
                                  n_at_q_R1=(np.nan if not np.isfinite(q1)
                                             else round(q1 * ref[pk]["n_elig"]))))
    Q = pd.DataFrame(qrows)
    Q.to_csv(OUT / f"{STEM}.qstar.csv", index=False)
    say(Q.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n    q_star_R1 = idea 159's literal bar (net edge below the tilt's own bill)")
    say("    q_star_R2 = the breakeven bar (pre-cost edge below the bill) — looser by construction")
    say("    q_cross_RND = the share at which the real keys' |dCAGR| falls to the RANDOM key's, "
        "i.e. becomes arithmetic noise on its own terms (P3's independent route to the same "
        "number)")
    say(f"    a value of exactly {Q_LEFT:.2f} means the edge was ALREADY below the bar at the "
        f"smallest share backtested — read it as 'noise everywhere measured', NOT as a located "
        f"threshold.  NaN means the curves never cross inside [{Q_LEFT:.2f}, 1.00].")

    # ============================================================ bootstrap
    say("\n" + "=" * 195)
    say(f"BOOTSTRAP — circular block bootstrap, block {BLOCK}d, B = {B_BOOT}, seed {SEED_BOOT}; "
        "books within a panel share the block index so dCAGR stays paired.  Turnover is NOT "
        "resampled.")
    say("=" * 195)
    brows = []
    rng = np.random.default_rng(SEED_BOOT)
    for pk in PANELS:
        idx = rets[(pk, SHARES[0], "NONE")].index
        T = len(idx)
        cols = [(m, k) for m in SHARES for k in KEYS]
        L = np.column_stack([np.log1p(rets[(pk, m, k)].to_numpy()) for m, k in cols])
        nb = int(np.ceil(T / BLOCK))
        yrs = T / 252.0
        cost_by_m = CU[CU.panel == pk].set_index("m")["cost"].to_dict()
        qs = {(f, r): [] for f in FAMILIES for r in ("R1", "R2")}
        for _ in range(B_BOOT):
            starts = rng.integers(0, T, size=nb)
            take = ((starts[:, None] + np.arange(BLOCK)[None, :]) % T).ravel()[:T]
            tot = L[take].sum(axis=0)
            cagr = np.exp(tot / yrs) - 1.0
            cm = {c: cagr[i] for i, c in enumerate(cols)}
            ad, ag = [], []
            for m in SHARES:
                real = [abs(cm[(m, k)] - cm[(m, "NONE")]) for k in TILTS if k != "RND"]
                ad.append(float(np.mean(real)))
                ag.append(float(np.mean(real)) + cost_by_m[m])
            ms_ = np.array(SHARES)
            cs_ = np.array([cost_by_m[m] for m in SHARES])
            for f in FAMILIES:
                fc = fit(ms_, cs_, f)
                qs[(f, "R1")].append(crossing(fit(ms_, np.array(ad), f), fc))
                qs[(f, "R2")].append(crossing(fit(ms_, np.array(ag), f), fc))
        for f in FAMILIES:
            for rd in ("R1", "R2"):
                a = np.array(qs[(f, rd)], float)
                fin = a[np.isfinite(a)]
                brows.append(dict(panel=pk, family=f, reading=rd, B=B_BOOT,
                                  frac_defined=float(len(fin) / len(a)),
                                  q_p05=float(np.percentile(fin, 5)) if len(fin) else np.nan,
                                  q_p50=float(np.percentile(fin, 50)) if len(fin) else np.nan,
                                  q_p95=float(np.percentile(fin, 95)) if len(fin) else np.nan,
                                  q_point=float(Q[(Q.panel == pk) & (Q.family == f)
                                                  & (~Q.drop_m1)][f"q_star_{rd}"].iloc[0])))
        say(f"  {pk} bootstrapped ({time.time() - t0:.0f}s)")
    BS = pd.DataFrame(brows)
    BS.to_csv(OUT / f"{STEM}.bootstrap.csv", index=False)
    say("")
    say(BS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n    `frac_defined` is the share of draws in which the edge curve crosses the cost "
        "curve inside (0.02, 1.00] at all.  A low value means the curves do not cross on that "
        "panel — which is itself an answer (P6).")

    # ============================================================ rule 8 walk-forward
    say("\n" + "=" * 195)
    say(f"RULE 8 WALK-FORWARD — q* fitted on <= {IS_END} only, read ONCE on {OOS_START} ->")
    say("A_BELOW = best IS-Sharpe (key, share) with share <= q*_IS.  A_ABOVE = best with share > "
        "q*_IS.  A_NONE = the NONE control at A_BELOW's share.")
    say("=" * 195)
    wf = []
    for pk in PANELS:
        # IS and OOS curves, built the same way as the full-sample one
        def curve(win):
            out = []
            for m in SHARES:
                b = rets[(pk, m, "NONE")]
                b = b.loc[:IS_END] if win == "IS" else b.loc[OOS_START:]
                cb = metrics(b)["CAGR"]
                real = []
                for k in TILTS:
                    if k == "RND":
                        continue
                    t = rets[(pk, m, k)]
                    t = t.loc[:IS_END] if win == "IS" else t.loc[OOS_START:]
                    real.append(abs(metrics(t)["CAGR"] - cb))
                out.append((m, float(np.mean(real))))
            return np.array([o[0] for o in out]), np.array([o[1] for o in out])
        cost_arr = CU[CU.panel == pk].sort_values("m")["cost"].to_numpy()
        m_is, y_is = curve("IS")
        m_oo, y_oo = curve("OOS")
        def rnd_curve(win):
            out = []
            for m in SHARES:
                b = rets[(pk, m, "NONE")]
                t = rets[(pk, m, "RND")]
                b = b.loc[:IS_END] if win == "IS" else b.loc[OOS_START:]
                t = t.loc[:IS_END] if win == "IS" else t.loc[OOS_START:]
                out.append(abs(metrics(t)["CAGR"] - metrics(b)["CAGR"]))
            return np.array(out)
        q_is = crossing(fit(m_is, y_is, "LOG"), fit(m_is, cost_arr, "LOG"))
        q_oo = crossing(fit(m_oo, y_oo, "LOG"), fit(m_oo, cost_arr, "LOG"))
        # the RANDOM-key crossing, the bar that actually binds (see the curve section)
        qn_is = crossing(fit(m_is, y_is, "LOG"), fit(m_is, rnd_curve("IS"), "LOG"))
        qn_oo = crossing(fit(m_oo, y_oo, "LOG"), fit(m_oo, rnd_curve("OOS"), "LOG"))
        say(f"\n  {pk}: cost bar  q*_IS = {q_is:.4f} (n ~ "
            f"{q_is * ref[pk]['n_elig'] if np.isfinite(q_is) else float('nan'):.0f})   "
            f"q*_OOS = {q_oo:.4f}   |   RANDOM bar  qN_IS = {qn_is:.4f} (n ~ "
            f"{qn_is * ref[pk]['n_elig'] if np.isfinite(qn_is) else float('nan'):.0f})   "
            f"qN_OOS = {qn_oo:.4f}   [LOG family]")
        sub = G[(G.panel == pk) & (G.key != "NONE")]
        # an UNDEFINED crossing means the edge never falls below the bar: everything is "below"
        lo = sub[sub.m <= q_is] if np.isfinite(q_is) else sub
        hi = sub[sub.m > q_is] if np.isfinite(q_is) else sub.iloc[0:0]
        nlo = sub[sub.m <= qn_is] if np.isfinite(qn_is) else sub
        nhi = sub[sub.m > qn_is] if np.isfinite(qn_is) else sub.iloc[0:0]
        picks = {}
        if len(lo):
            picks["A_BELOW"] = lo.loc[lo.IS_Sharpe.idxmax()]
        if len(hi):
            picks["A_ABOVE"] = hi.loc[hi.IS_Sharpe.idxmax()]
        if len(nlo):
            picks["N_BELOW"] = nlo.loc[nlo.IS_Sharpe.idxmax()]
        if len(nhi):
            picks["N_ABOVE"] = nhi.loc[nhi.IS_Sharpe.idxmax()]
        if "A_BELOW" in picks:
            mm = picks["A_BELOW"].m
            picks["A_NONE"] = G[(G.panel == pk) & (G.m == mm) & (G.key == "NONE")].iloc[0]
        if "N_BELOW" in picks:
            mm = picks["N_BELOW"].m
            picks["N_NONE"] = G[(G.panel == pk) & (G.m == mm) & (G.key == "NONE")].iloc[0]
        b = ref[pk]
        for arm, p in picks.items():
            wf.append(dict(panel=pk, arm=arm, key=p.key, m=p.m, n=int(p.n),
                           q_star_IS=q_is, q_star_OOS=q_oo, qN_IS=qn_is, qN_OOS=qn_oo,
                           IS_Sharpe=p.IS_Sharpe, IS_CAGR=p.IS_CAGR,
                           OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                           full_CAGR=p.CAGR, full_Sharpe=p.Sharpe, full_MaxDD=p.MaxDD,
                           H1=p.H1, H2=p.H2, pass4a=p.pass4a, fail4b=p.fail4b,
                           fail4b_oos=p.fail4b_oos,
                           SPY_OOS_CAGR=b["spy_oos"]["CAGR"],
                           SPY_OOS_Sharpe=b["spy_oos"]["Sharpe"],
                           SPY_OOS_MaxDD=b["spy_oos"]["MaxDD"],
                           V1_OOS_CAGR=metrics(b["v1"].loc[OOS_START:])["CAGR"],
                           V1_OOS_Sharpe=metrics(b["v1"].loc[OOS_START:])["Sharpe"],
                           V1_OOS_MaxDD=metrics(b["v1"].loc[OOS_START:])["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("")
    say(WF[["panel", "arm", "key", "m", "n", "q_star_IS", "qN_IS", "qN_OOS", "IS_Sharpe",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "full_Sharpe", "pass4a", "fail4b",
            "fail4b_oos", "SPY_OOS_Sharpe", "V1_OOS_Sharpe"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  arm means over the 3 panels (OOS window):")
    say(WF.groupby("arm")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))
    for tag, arm, ctl in (("BELOW the COST bar", "A_BELOW", "A_NONE"),
                          ("ABOVE the COST bar", "A_ABOVE", "A_NONE"),
                          ("BELOW the RANDOM bar", "N_BELOW", "N_NONE"),
                          ("ABOVE the RANDOM bar", "N_ABOVE", "N_NONE")):
        if not {arm, ctl} <= set(WF.arm):
            say(f"  DOES RANKING {tag} PAY OOS?  arm empty on every panel — no comparison")
            continue
        a = WF[WF.arm == arm].set_index("panel")
        c = WF[WF.arm == ctl].set_index("panel")
        j = a.index.intersection(c.index)
        say(f"  DOES RANKING {tag} PAY OOS?  mean dOOS_Sharpe = "
            f"{float((a.loc[j].OOS_Sharpe - c.loc[j].OOS_Sharpe).mean()):+.4f}, mean dOOS_CAGR = "
            f"{float((a.loc[j].OOS_CAGR - c.loc[j].OOS_CAGR).mean()):+.4f}, wins "
            f"{int((a.loc[j].OOS_Sharpe > c.loc[j].OOS_Sharpe).sum())}/{len(j)} panels")

    say("\n  KEEP-path census over all 294 books:")
    say(G.groupby("panel")[["pass4a", "pass4b", "pass4b_oos"]].sum().to_string())
    if int(G.pass4b.sum()):
        say("\n  the 4b passes in full:")
        say(G[G.pass4b][["panel", "m", "n", "key", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe", "pass4a", "pass4b_oos"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 195)
    say(f"done in {time.time() - t0:.0f}s")
    say("=" * 195)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
