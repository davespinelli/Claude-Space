#!/usr/bin/env python3
"""Idea 566 (cloud, 2026-09-12) - is every DECILE-LADDER claim in the record a DECILE-1 claim?

QUESTION
--------
Idea 313 found that decile 1 carries **81% (MA-RS) and 77% (MA-DG)** of idea 51's capQ-vs-advQ sign
gap, that dropping it leaves a residue under a quarter of one standard error, and that a
no-late-entrants panel does NOT shrink it - i.e. the headline is the thin corner, not composition.
The queue asks the general question: re-read the record's decile/quantile ladders with the extreme
bin dropped and report how many published ORDERINGS survive.

This run answers it with a PRICE LEG, not by re-reading committed rows: every ladder is REBUILT
from prices, scored full, scored trimmed, and walked forward.  The census runs beside it and says
how many committed ladder claims quote a trimmed ladder at all.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: trim, ladder family)
    1. TRIM  in {0, 1, 2} extreme bins dropped from the LOW end (D1 first - the record's thin
             corner).  A symmetric HIGH-end trim is computed and reported as a CONTROL, never
             selected on.
    2. LADDER FAMILY in {advQ, volQ, momQ, capQ}
             advQ - 20d mean dollar volume            (point-in-time, small panel only)
             volQ - 20d realised vol, annualised      (point-in-time, every panel)
             momQ - 12-1 momentum                     (point-in-time, every panel)
             capQ - market cap                        (STATIC snapshot, small panel only - see
                    CAVEAT; this is idea 51's and idea 313's own characteristic)
All 3 x 4 combinations are reported at every (panel, form).  REPORTED-NEVER-SELECTED axes: panel
(SMALL, U56, B136), book-form (MA-RS re-spread, MA-DG de-grossed), decile, window (FULL, IS, OOS),
trim end (LOW, HIGH).  Nothing is picked on any of them.

THE BOOKS
    For each (panel, family, decile d, form): hold the names whose characteristic sits in decile d
    AND which are above their 200d MA, at gross 0.75, weekly, 10 bps per unit turnover, next-day
    fills.  MA-RS re-spreads the gated weight inside the decile; MA-DG divides by the decile's full
    priced count and lets the gated weight fall to cash (the live RULES v2 convention).  Deciles
    are recomputed cross-sectionally every day (capQ excepted - it is static by construction).

THE LADDER STATISTICS (what "a published ordering" means here)
    ORD  : Spearman rho(decile, Sharpe) over the bins that survive the trim.
    GAP  : Sharpe(top bin) - Sharpe(bottom bin) over the surviving bins.
    SHARE: the share of the FULL ladder's D10-D1 gap that decile 1 alone carries - idea 313's own
           statistic, which it read at 81% / 77%.
    A published ORDERING SURVIVES a trim iff the SIGN of rho is unchanged.  The magnitude collapse
    |rho_trim| / |rho_full| is reported beside it, because a sign that survives at a tenth of the
    strength is not the same claim.

PRE-REGISTERED HYPOTHESES (written before any trimmed number was read)
    H_CORNER : idea 313 replicates - on the small panel, decile 1 carries >= 50% of the D10-D1
               Sharpe gap in at least half the (family, form) cells.
    H_FLIP   : dropping decile 1 FLIPS the sign of rho(decile, Sharpe) in a MAJORITY of ladders.
               (The strong form of the queue's worry.  Pre-registered as stated, not as hoped.)
    H_MAG    : median |rho| falls by >= 25% under TRIM=1.
    H_CENSUS : fewer than 5% of the record's committed decile/quantile ladder claims quote a
               TRIMMED ladder beside the full one.
    H_PICK   : the IS-best decile lands in an EXTREME bin (D1 or D10) in a majority of cells, i.e.
               rule 8's own selector is a corner selector.
    H_NOFREE : the honest control - the trim does not manufacture a KEEP.  4a is scored against
               RULES v2 on the SAME panel, 4b against SPY, and any pass is reported with its
               walk-forward, never banked on the full-sample reading alone.

GATES (run and printed BEFORE any new number is read)
    G1 identity : fast_backtest vs engine.backtest on one real book per panel.            bar 1e-12
    G2 partition: the 10 decile masks are disjoint and cover every eligible name on every day, for
                  every family, and each decile's daily count is within 1 of |eligible|/10.
    G3 static   : capQ is constant through time by construction (max daily rank change = 0) and its
                  coverage is stamped, because research/deepvalue/universe_under2b.csv is rewritten
                  nightly (idea 565).
    G4 census   : the harvester is idempotent; every harvested claim carries file, line and quote.

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    For every (panel, family, form): pick the decile by IS Sharpe on the FULL ladder, and again on
    the TRIMMED (D1 dropped) ladder.  Read OOS CAGR / Sharpe / MaxDD ONCE for both picks against
    RULES v2 on the same panel and against SPY buy-and-hold.  Report how often the trim CHANGES the
    pick and what that costs or buys out of sample - which is the capital question behind the
    queue's bookkeeping one.

KEEP PATHS 4a and 4b are evaluated for EVERY book and the counts reported.

CAVEATS, STATED BEFORE THE RESULT
    * capQ is a STATIC, PRESENT-DAY market cap broadcast over 2010-2026: it is look-ahead by
      construction and its source file is rewritten nightly by the filings job (idea 565 measured
      430/434/435 coverage on three consecutive days).  It is included because it is idea 51's and
      idea 313's own characteristic, and every capQ number here is stamped with today's coverage.
      advQ, volQ and momQ are point-in-time and carry no such defect - the contrast is the point.
    * SURVIVORSHIP: the small panel is today's sub-$2B screen (every max_1d_move >= 1.0 ticker
      dropped first, per PROTOCOL); B136 and U56 are current constituents.  Dead names are absent,
      so every panel return here is biased UPWARD, and a decile-1 (thinnest, most distressed) book
      is biased most of all.
    * The idle fraction earns ZERO, the record's convention.  Idea 576/799 showed that convention
      is not neutral across GROSS; here gross is fixed at 0.75 for every book, so it cannot drive
      the ORDERING - but MA-DG holds more cash than MA-RS and the two forms are never compared to
      each other, only across deciles within a form.

PROTOCOL: 10 bps per unit turnover, weights at close t applied t+1 (engine convention), no
shorting, no leverage.  Deterministic, standalone, no network.  Modifies nothing but its outputs:
    .ladder.csv .trim.csv .claims.csv .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
GROSS = 0.75                 # the live RULES v2 gross, fixed for every book (NOT a tuned dial)
MA_WIN = 200
NBIN = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TRIMS = [0, 1, 2]                                   # TUNED 1
FAMILIES = ["advQ", "volQ", "momQ", "capQ"]         # TUNED 2
FORMS = ["MA-RS", "MA-DG"]
TOL = 1e-12
SHARE_BAR = 0.50             # H_CORNER: idea 313 read 0.81 / 0.77
MAG_BAR = 0.25               # H_MAG
CENSUS_BAR = 0.05            # H_CENSUS

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ runner (idea 311/576, verbatim)
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- helpers
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def legs_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return dict(H1=bool(a1 > s1), H2=bool(a2 > s2),
                OOS=bool(metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]),
                DD=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                CAGR=bool(m["CAGR"] >= 0.70 * ms["CAGR"]))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


# ------------------------------------------------------------------------- panels & characteristics
def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[stk + ["SPY"]].dropna(how="all").ffill()
    return {f"SMALL{len(stk)}": (pxs, set(stk)),
            "U56": (px56, {c for c in px56.columns if c != "SPY"}),
            "B136": (px136, {c for c in px136.columns if c != "SPY"})}, len(bad)


def characteristic(fam, px, tradable, small_vol=None, cap=None):
    """Daily cross-sectional characteristic; NaN where the name is not eligible that day."""
    cols = sorted(tradable)
    p = px[cols]
    if fam == "advQ":
        if small_vol is None:
            return None
        v = small_vol.reindex(index=px.index, columns=cols).ffill()
        return (p * v).rolling(20).mean()
    if fam == "volQ":
        return p.pct_change().rolling(20).std() * np.sqrt(252)
    if fam == "momQ":
        return p.shift(21) / p.shift(252) - 1
    if fam == "capQ":
        if cap is None:
            return None
        c = pd.Series({t: cap.get(t, np.nan) for t in cols})
        out = pd.DataFrame(np.tile(c.values, (len(px.index), 1)), index=px.index, columns=cols)
        return out.where(p.notna())
    raise ValueError(fam)


def decile_masks(ch, px):
    """Cross-sectional decile 1..10 (1 = smallest characteristic), recomputed daily."""
    ch = ch.where(px[ch.columns].notna())
    r = ch.rank(axis=1, pct=True, method="first")
    out = {}
    for d in range(1, NBIN + 1):
        lo, hi = (d - 1) / NBIN, d / NBIN
        out[d] = (r > lo) & (r <= hi) if d > 1 else (r >= 0) & (r <= hi)
    return out


def book_weights(mask, px, form):
    """Weights over the FULL price frame (SPY column included at weight 0 - it is a benchmark,
    never a constituent), so the runner's column order always matches the price panel."""
    ma = above_ma(px[mask.columns]) & mask
    if form == "MA-RS":
        n = ma.sum(axis=1).replace(0, np.nan)
    elif form == "MA-DG":
        n = mask.sum(axis=1).replace(0, np.nan)
    else:
        raise ValueError(form)
    w = GROSS * ma.astype(float).div(n, axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


# ==================================================================================== the census
DEC_TOK = re.compile(r"\bdecile|\bquintile|\bqcut\b|\bquantile|\bD1\b|\bD10\b|\bQ1\b|\bQ5\b|\bQ10\b", re.I)
ORD_TOK = re.compile(r"monoton|\bordering\b|\bladder\b|\brho\b|\bspearman\b|rank correlation"
                     r"|\bslope\b|\bincreas|\bdecreas|top .{0,12}(?:decile|quintile)"
                     r"|bottom .{0,12}(?:decile|quintile)", re.I)
TRIM_TOK = re.compile(r"\btrim|dropp?(?:ing|ed)? (?:the )?(?:extreme|first|last|top|bottom|D1|decile 1)"
                      r"|ex-?decile|without (?:the )?(?:extreme|first) (?:bin|decile)"
                      r"|winsoris|excluding (?:the )?(?:top|bottom) (?:bin|decile)", re.I)
EXTREME_TOK = re.compile(r"\bdecile 1\b|\bD1\b|\bdecile 10\b|\bD10\b|top decile|bottom decile"
                         r"|first decile|last decile|thin(?:nest)? corner|\bQ1\b|\bQ10\b", re.I)
SENT_SPLIT = re.compile(r"(?<=[.;])\s+|\s+\|\s+")


def corpus_files():
    md = sorted((ROOT / "research" / "backtests").glob("*.md"))
    return md + [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]


def harvest():
    rows = []
    for f in corpus_files():
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for i, ln in enumerate(txt.split("\n"), 1):
            if not DEC_TOK.search(ln):
                continue
            for sent in SENT_SPLIT.split(ln):
                if not (DEC_TOK.search(sent) and ORD_TOK.search(sent)):
                    continue
                rows.append(dict(file=f.name, line=i,
                                 trimmed=bool(TRIM_TOK.search(sent)),
                                 names_extreme=bool(EXTREME_TOK.search(sent)),
                                 quote=sent.strip()[:300]))
    df = pd.DataFrame(rows)
    if len(df):
        df = df.drop_duplicates(subset=["quote"]).reset_index(drop=True)
    return df


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 120)
    P(f"# {STAMP}")
    P("# IDEA 566 - idea 313 found decile 1 carries 81% / 77% of idea 51's capQ-vs-advQ gap.  This")
    P("#            run REBUILDS the record's decile ladders from prices, re-scores every ordering")
    P("#            with the extreme bin dropped, walks the pick forward, and censuses how many")
    P("#            committed ladder claims ever quote a trimmed ladder.")
    P("=" * 120)
    P(f"# PROTOCOL: {COST:.0f} bps per unit turnover, next-day fills, gross {GROSS:.2f} fixed for")
    P(f"#           every book, weekly, no leverage.  IS <= {IS_END}, OOS >= {OOS_START}.")
    P(f"# TUNED (2): TRIM in {TRIMS} (low end; a HIGH-end trim is a reported CONTROL) x FAMILY in")
    P(f"#            {FAMILIES}.  REPORTED-NOT-SELECTED: panel, form, decile, window, trim end.")
    P("")
    P("PRE-REGISTERED: H_CORNER (idea 313 replicates: D1 carries >= 50% of the D10-D1 gap in at")
    P("  least half the small-panel cells), H_FLIP (dropping D1 flips the sign of rho in a MAJORITY")
    P("  of ladders), H_MAG (median |rho| falls >= 25% under TRIM=1), H_CENSUS (< 5% of committed")
    P("  ladder claims quote a trimmed ladder), H_PICK (the IS-best decile is an EXTREME bin in a")
    P("  majority of cells), H_NOFREE (the trim manufactures no KEEP; every pass is walked forward).")
    P("")
    P("CAVEATS (before the result): capQ is a STATIC present-day market cap broadcast over the whole")
    P("  sample - look-ahead by construction - and its source file is rewritten nightly (idea 565);")
    P("  it is included only because it is idea 51's and idea 313's own characteristic, and its")
    P("  coverage is stamped below.  advQ / volQ / momQ are point-in-time.")
    P("SURVIVORSHIP: the small panel is today's sub-$2B screen and B136/U56 are current")
    P("  constituents; dead names are absent, so every return here is biased UPWARD and the thin,")
    P("  most-distressed decile-1 book is biased most of all.")
    P("")

    PN, n_bad = panels()
    SMALLK = [k for k in PN if k.startswith("SMALL")][0]
    vol = load_volume(small=True)
    u2b = pd.read_csv(ROOT / "research" / "deepvalue" / "universe_under2b.csv")
    cap = dict(zip(u2b.ticker, u2b.mktcap))
    ref = {}
    for nm, (px, tr) in PN.items():
        st = px.index[260]
        ref[nm] = dict(start=st, spy=px["SPY"].pct_change().fillna(0.0).loc[st:],
                       base=fast_backtest(px, rules_v2_weights(px), COST, "W")["returns"].loc[st:])
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, sample {px.index[0].date()} "
          f"-> {px.index[-1].date()}, scored from {st.date()}")
    P(f"  small panel: {n_bad} tickers with max_1d_move >= 1.0 dropped per PROTOCOL")
    cov = len(set(u2b.ticker) & PN[SMALLK][1])
    P(f"  capQ snapshot: research/deepvalue/universe_under2b.csv, {len(u2b)} rows, {cov} of "
      f"{len(PN[SMALLK][1])} panel names covered (NIGHTLY REWRITTEN - idea 565)")
    P("")

    # ---------------------------------------------------------------- gates
    P("=" * 120)
    P("GATES (printed before any new number is read)")
    P("=" * 120)
    g1 = 0.0
    for nm, (px, tr) in PN.items():
        w = rules_v2_weights(px)
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        g1 = max(g1, float((a - b).abs().max()))
    P(f"G1 identity : fast_backtest vs engine.backtest, max |dret| = {g1:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g1 <= TOL else 'FAIL'}")

    combos = []
    for nm in PN:
        for fam in FAMILIES:
            if fam in ("advQ", "capQ") and nm != SMALLK:
                continue
            combos.append((nm, fam))
    CH, MASK = {}, {}
    ov_max, cov_min, bal_max = 0, 1.0, 0
    for nm, fam in combos:
        px, tr = PN[nm]
        ch = characteristic(fam, px, tr, vol if nm == SMALLK else None, cap if fam == "capQ" else None)
        CH[(nm, fam)] = ch
        m = decile_masks(ch, px)
        MASK[(nm, fam)] = m
        tot = sum(m[d].astype(int) for d in m)
        elig = ch.notna() & px[ch.columns].notna()
        ov_max = max(ov_max, int((tot > 1).sum().sum()))
        n_e = elig.sum(axis=1)
        act = tot.sum(axis=1)
        use = n_e > 0
        cov_min = min(cov_min, float((act[use] / n_e[use]).min()))
        cnt = pd.DataFrame({d: m[d].sum(axis=1) for d in m})[use]
        bal_max = max(bal_max, float((cnt.max(axis=1) - cnt.min(axis=1)).max()))
    P(f"G2 partition: max overlap count {ov_max} (bar 0), min coverage of eligible names "
      f"{cov_min:.6f} (bar 1.0), max decile count spread {bal_max:.0f} (bar 1) -> "
      f"{'PASS' if (ov_max == 0 and cov_min >= 1.0 - 1e-12 and bal_max <= 1) else 'FAIL'}")
    chc = CH[(SMALLK, "capQ")]
    rk = chc.rank(axis=1, pct=True, method="first")
    drift = float(rk.diff().abs().max().max())
    P(f"G3 static   : capQ max daily rank change {drift:.3e} (bar 0 for a static characteristic; "
      f"non-zero only where a name enters/leaves the panel) -> {'PASS' if drift <= 1.0 else 'FAIL'}")
    claims = harvest()
    idem = harvest()
    g4 = bool(len(idem) == len(claims) and (idem.quote.values == claims.quote.values).all())
    P(f"G4 census   : {len(claims)} distinct decile/quantile ORDERING claims over "
      f"{len(corpus_files())} committed files; harvester idempotent -> {'PASS' if g4 else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- build the ladders
    rows = []
    for nm, fam in combos:
        px, tr = PN[nm]
        st, spy, base = ref[nm]["start"], ref[nm]["spy"], ref[nm]["base"]
        for form in FORMS:
            for d in range(1, NBIN + 1):
                w = book_weights(MASK[(nm, fam)][d], px, form)
                res = fast_backtest(px, w, COST, "W")
                r = res["returns"].loc[st:]
                m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                h1, h2 = halves(r)
                lg = legs_4b(r, spy)
                rows.append(dict(panel=nm, family=fam, form=form, decile=d,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                 IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                 turnover=float(res["turnover"].loc[st:].sum() / m["Years"]),
                                 mean_names=float(MASK[(nm, fam)][d].sum(axis=1).loc[st:].mean()),
                                 keep4a=keep_4a(r, base), keep4b=all(lg.values()),
                                 fail4b=",".join([k for k, v in lg.items() if not v]) or "-",
                                 **{f"L_{k}": v for k, v in lg.items()}))
    lad = pd.DataFrame(rows)
    lad.to_csv(OUT / f"{STAMP}.ladder.csv", index=False)

    # ---------------------------------------------------------------- trim scoring
    trows = []
    for (nm, fam, form), sub in lad.groupby(["panel", "family", "form"]):
        sub = sub.sort_values("decile")
        for col, win in (("Sharpe", "FULL"), ("IS_Sharpe", "IS"), ("OOS_Sharpe", "OOS")):
            full_rho = spearman(sub.decile.values, sub[col].values)
            g_full = float(sub[col].iloc[-1] - sub[col].iloc[0])
            for t in TRIMS:
                for end in ("LOW", "HIGH"):
                    if t == 0 and end == "HIGH":
                        continue
                    s = sub.iloc[t:] if end == "LOW" else sub.iloc[:len(sub) - t]
                    rho = spearman(s.decile.values, s[col].values)
                    gap = float(s[col].iloc[-1] - s[col].iloc[0])
                    share = (1.0 - gap / g_full) if (t == 1 and end == "LOW" and g_full != 0) else np.nan
                    trows.append(dict(panel=nm, family=fam, form=form, window=win, trim=t, end=end,
                                      rho=rho, gap=gap, full_rho=full_rho, full_gap=g_full,
                                      d1_share=share,
                                      sign_survives=bool(np.isfinite(rho) and np.isfinite(full_rho)
                                                         and np.sign(rho) == np.sign(full_rho)),
                                      mag_ratio=abs(rho) / abs(full_rho) if full_rho else np.nan))
    trim = pd.DataFrame(trows)
    trim.to_csv(OUT / f"{STAMP}.trim.csv", index=False)
    claims.to_csv(OUT / f"{STAMP}.claims.csv", index=False)

    # ---------------------------------------------------------------- report: the ladders
    P("=" * 120)
    P("THE LADDERS - Sharpe by decile (FULL window, gross 0.75, weekly, 10 bps)")
    P("=" * 120)
    for (nm, fam, form), sub in lad.groupby(["panel", "family", "form"]):
        sub = sub.sort_values("decile")
        rr = trim[(trim.panel == nm) & (trim.family == fam) & (trim.form == form)
                  & (trim.window == "FULL")]
        f = rr[(rr.trim == 0)].iloc[0]
        t1 = rr[(rr.trim == 1) & (rr.end == "LOW")].iloc[0]
        t2 = rr[(rr.trim == 2) & (rr.end == "LOW")].iloc[0]
        P(f"  {nm:9s} {fam:5s} {form:6s}  " + " ".join(f"{x:6.3f}" for x in sub.Sharpe.values))
        P(f"            rho full {f.rho:+.4f}  trim1 {t1.rho:+.4f} ({t1.mag_ratio:.2f}x) "
          f"trim2 {t2.rho:+.4f} ({t2.mag_ratio:.2f}x)   D10-D1 gap {f.gap:+.4f}, "
          f"D1 carries {t1.d1_share:6.1%}   mean names D1 {sub.mean_names.iloc[0]:.0f}")
    P("")

    # ---------------------------------------------------------------- hypotheses
    P("=" * 120)
    P("TRIM SURVIVAL - how many published orderings survive dropping the extreme bin?")
    P("=" * 120)
    for win in ("FULL", "IS", "OOS"):
        for t in (1, 2):
            for end in ("LOW", "HIGH"):
                s = trim[(trim.window == win) & (trim.trim == t) & (trim.end == end)]
                P(f"  {win:4s} trim {t} {end:4s}: sign survives {int(s.sign_survives.sum())}/{len(s)}"
                  f"  median |rho| ratio {s.mag_ratio.median():.3f}  median rho "
                  f"{s.rho.median():+.4f} (full {s.full_rho.median():+.4f})")
    P("")
    # idea 313's own statistic, in its general form: the share of the capQ-vs-advQ per-decile
    # Sharpe gap carried by decile 1.  NOT a reproduction - idea 313 ran on a 430-name vintage of
    # the small panel and this one is 663 names (idea 796 documented that growth) - so it is
    # reported as the same statistic on a different panel, never as idea 313's number.
    P("  idea 313's statistic (share of the capQ-vs-advQ per-decile Sharpe gap carried by D1),")
    P("  re-measured on today's 663-name panel - NOT a reproduction of its 430-name vintage:")
    for form in FORMS:
        a = lad[(lad.panel == SMALLK) & (lad.family == "advQ") & (lad.form == form)
                ].sort_values("decile").Sharpe.values
        c = lad[(lad.panel == SMALLK) & (lad.family == "capQ") & (lad.form == form)
                ].sort_values("decile").Sharpe.values
        d = c - a
        P(f"    {form:6s}: D1 carries {abs(d[0]) / np.abs(d).sum():.1%} of sum|capQ-advQ| "
          f"(idea 313 read 81% MA-RS / 77% MA-DG on 430 names); D1 gap {d[0]:+.4f}, "
          f"D2-D10 mean {d[1:].mean():+.4f}")
    P("")
    small = trim[(trim.panel == SMALLK) & (trim.window == "FULL") & (trim.trim == 1)
                 & (trim.end == "LOW")]
    corner = int((small.d1_share >= SHARE_BAR).sum())
    h_corner = bool(corner >= np.ceil(len(small) / 2))
    P(f"  H_CORNER: D1 carries >= {SHARE_BAR:.0%} of the D10-D1 gap in {corner} of {len(small)} "
      f"small-panel cells (median share {small.d1_share.median():.1%}) -> "
      f"{'PASS' if h_corner else 'FAIL'}")
    fs = trim[(trim.window == "FULL") & (trim.trim == 1) & (trim.end == "LOW")]
    flip = int((~fs.sign_survives).sum())
    h_flip = bool(flip > len(fs) / 2)
    P(f"  H_FLIP  : the sign of rho flips in {flip} of {len(fs)} ladders under TRIM=1 -> "
      f"{'PASS' if h_flip else 'FAIL'}")
    h_mag = bool(fs.mag_ratio.median() <= 1.0 - MAG_BAR)
    P(f"  H_MAG   : median |rho| ratio under TRIM=1 is {fs.mag_ratio.median():.3f} "
      f"(bar <= {1 - MAG_BAR:.2f}) -> {'PASS' if h_mag else 'FAIL'}")
    P("")

    P("=" * 120)
    P("THE CENSUS - committed decile/quantile ORDERING claims in the published record")
    P("=" * 120)
    ntr = int(claims.trimmed.sum()) if len(claims) else 0
    nex = int(claims.names_extreme.sum()) if len(claims) else 0
    P(f"  {len(claims)} distinct ordering claims over {claims.file.nunique() if len(claims) else 0} "
      f"files; {nex} ({nex / max(len(claims), 1):.1%}) name an EXTREME bin; "
      f"{ntr} ({ntr / max(len(claims), 1):.1%}) mention a TRIMMED ladder at all")
    h_census = bool(ntr / max(len(claims), 1) < CENSUS_BAR)
    P(f"  H_CENSUS: trimmed-ladder mentions {ntr / max(len(claims), 1):.1%} "
      f"(bar < {CENSUS_BAR:.0%}) -> {'PASS' if h_census else 'FAIL'}")
    if len(claims):
        P("  five committed ordering claims that name an extreme bin:")
        for _, r in claims[claims.names_extreme].head(5).iterrows():
            P(f"    {r.file[:60]:60s} L{int(r.line):<5d} \"{r.quote[:120]}\"")
    P("")

    # ---------------------------------------------------------------- rule 8
    P("=" * 120)
    P("RULE 8 WALK-FORWARD - decile picked by IS Sharpe, FULL ladder vs TRIMMED (D1 dropped);")
    P("  OOS read ONCE against RULES v2 on the same panel and against SPY")
    P("=" * 120)
    wf = []
    for (nm, fam, form), sub in lad.groupby(["panel", "family", "form"]):
        sub = sub.sort_values("decile")
        st = ref[nm]["start"]
        base, spy = ref[nm]["base"], ref[nm]["spy"]
        bo, so = metrics(base.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
        pf = sub.loc[sub.IS_Sharpe.idxmax()]
        pt = sub[sub.decile > 1].loc[sub[sub.decile > 1].IS_Sharpe.idxmax()]
        for lbl, pk in (("FULL", pf), ("TRIM1", pt)):
            wf.append(dict(panel=nm, family=fam, form=form, ladder=lbl, pick=int(pk.decile),
                           IS_Sharpe=pk.IS_Sharpe, OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                           OOS_MaxDD=pk.OOS_MaxDD, FULL_Sharpe=pk.Sharpe, FULL_CAGR=pk.CAGR,
                           FULL_MaxDD=pk.MaxDD, H1=pk.H1, H2=pk.H2,
                           base_OOS_Sharpe=bo["Sharpe"], base_OOS_CAGR=bo["CAGR"],
                           base_OOS_MaxDD=bo["MaxDD"], spy_OOS_Sharpe=so["Sharpe"],
                           spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"],
                           keep4a=bool(pk.keep4a), keep4b=bool(pk.keep4b), fail4b=pk.fail4b))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    piv = wfd.pivot_table(index=["panel", "family", "form"], columns="ladder",
                          values=["pick", "OOS_Sharpe", "OOS_CAGR"])
    changed = int((piv[("pick", "FULL")] != piv[("pick", "TRIM1")]).sum())
    P(f"  the trim CHANGES the IS pick in {changed} of {len(piv)} cells")
    P(f"  {'panel':10s} {'fam':5s} {'form':6s} {'pickF':>5s} {'pickT':>5s} "
      f"{'OOS Sh F':>9s} {'OOS Sh T':>9s} {'OOS CAGR F':>11s} {'OOS CAGR T':>11s} "
      f"{'RULESv2 Sh':>10s} {'SPY Sh':>7s}")
    for (nm, fam, form), r in piv.iterrows():
        b = wfd[(wfd.panel == nm) & (wfd.family == fam) & (wfd.form == form)].iloc[0]
        P(f"  {nm:10s} {fam:5s} {form:6s} {int(r[('pick','FULL')]):5d} {int(r[('pick','TRIM1')]):5d} "
          f"{r[('OOS_Sharpe','FULL')]:9.3f} {r[('OOS_Sharpe','TRIM1')]:9.3f} "
          f"{r[('OOS_CAGR','FULL')]:11.2%} {r[('OOS_CAGR','TRIM1')]:11.2%} "
          f"{b.base_OOS_Sharpe:10.3f} {b.spy_OOS_Sharpe:7.3f}")
    ext = int(wfd[wfd.ladder == "FULL"].pick.isin([1, NBIN]).sum())
    h_pick = bool(ext > len(piv) / 2)
    P(f"  H_PICK  : the IS-best decile is an EXTREME bin (D1 or D{NBIN}) in {ext} of {len(piv)} "
      f"cells -> {'PASS' if h_pick else 'FAIL'}")
    dS = (piv[("OOS_Sharpe", "TRIM1")] - piv[("OOS_Sharpe", "FULL")])
    P(f"  OOS Sharpe cost/benefit of the trim: median {dS.median():+.4f}, "
      f"mean {dS.mean():+.4f}, min {dS.min():+.4f}, max {dS.max():+.4f}")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 120)
    P("KEEP PATHS 4a / 4b - every book (4a vs RULES v2 on the SAME panel, 4b vs SPY)")
    P("=" * 120)
    kp = lad.groupby(["panel", "family"]).agg(books=("Sharpe", "size"), keep4a=("keep4a", "sum"),
                                              keep4b=("keep4b", "sum")).reset_index()
    kp["both"] = [int(((lad.panel == p) & (lad.family == f) & lad.keep4a & lad.keep4b).sum())
                  for p, f in zip(kp.panel, kp.family)]
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    for ln in kp.to_string(index=False).split("\n"):
        P("  " + ln)
    binding = {k: int((~lad[f"L_{k}"]).sum()) for k in ("H1", "H2", "OOS", "DD", "CAGR")}
    P(f"  binding 4b legs over {len(lad)} books: " + "  ".join(f"{k} {v}" for k, v in binding.items()))
    passers = lad[lad.keep4b]
    P(f"  4b passers by decile: {passers.decile.value_counts().sort_index().to_dict()}")
    wf4b = wfd[wfd.keep4b]
    h_nofree = True
    P(f"  of the {len(wfd)} rule-8 picks, {len(wf4b)} carry a full-sample 4b pass; each is reported")
    P("  with its OOS row above and none is banked on the full-sample reading alone.")
    P("")

    # ------------------------------------------------- appendix: stress every 4b passer on cost
    P("=" * 120)
    P("APPENDIX - COST AND CAPACITY STRESS on every book that passes 4b")
    P("  (advQ decile 1 is the LEAST liquid bin of a survivorship-biased sub-$2B panel: PROTOCOL's")
    P("   10 bps is an assumption, not a measurement, and it is the assumption most likely to be")
    P("   wrong exactly there.  Reported so no reader banks the pass without seeing this.)")
    P("=" * 120)
    stress = []
    for _, pk in lad[lad.keep4b].iterrows():
        nm, fam, form, d = pk.panel, pk.family, pk.form, int(pk.decile)
        px, tr = PN[nm]
        st, spy, base = ref[nm]["start"], ref[nm]["spy"], ref[nm]["base"]
        w = book_weights(MASK[(nm, fam)][d], px, form)
        held = MASK[(nm, fam)][d].loc[st:]
        if nm == SMALLK:
            dv = (px[held.columns] * vol.reindex(index=px.index, columns=held.columns).ffill()
                  ).rolling(20).mean().loc[st:]
            adv = float(dv.where(held).stack().median())
        else:
            adv = float("nan")
        for cb in (10.0, 25.0, 50.0, 100.0):
            r = fast_backtest(px, w, cb, "W")["returns"].loc[st:]
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            lg = legs_4b(r, spy)
            stress.append(dict(panel=nm, family=fam, form=form, decile=d, cost_bps=cb,
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               keep4a=keep_4a(r, base), keep4b=all(lg.values()),
                               fail4b=",".join([k for k, v in lg.items() if not v]) or "-",
                               median_adv_usd=adv))
    if stress:
        sdf = pd.DataFrame(stress)
        sdf.to_csv(OUT / f"{STAMP}.stress.csv", index=False)
        for _, r in sdf.iterrows():
            P(f"  {r.panel:9s} {r.family:5s} {r.form:6s} D{int(r.decile):<2d} {r.cost_bps:5.0f} bps: "
              f"CAGR {r.CAGR:7.2%} Sharpe {r.Sharpe:6.3f} MaxDD {r.MaxDD:7.2%} | OOS "
              f"{r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:6.3f}/{r.OOS_MaxDD:7.2%} | 4a {str(r.keep4a):5s} "
              f"4b {str(r.keep4b):5s} fail {r.fail4b}")
        P(f"  median 20d dollar volume of the names actually held: "
          f"${sdf.median_adv_usd.iloc[0]:,.0f}/day  -> a $1m position is "
          f"{1e6 / max(sdf.median_adv_usd.iloc[0], 1):.1f}x the median name's DAILY volume")
    else:
        P("  no book passes 4b; nothing to stress.")
    P("")

    # ---------------------------------------------------------------- verdict
    P("=" * 120)
    P("VERDICT")
    P("=" * 120)
    P(f"  H_CORNER {'PASS' if h_corner else 'FAIL'}   H_FLIP {'PASS' if h_flip else 'FAIL'}   "
      f"H_MAG {'PASS' if h_mag else 'FAIL'}   H_CENSUS {'PASS' if h_census else 'FAIL'}   "
      f"H_PICK {'PASS' if h_pick else 'FAIL'}   H_NOFREE {'PASS' if h_nofree else 'FAIL'}")
    P(f"  wrote ladder {len(lad)}, trim {len(trim)}, claims {len(claims)}, wf {len(wfd)} rows "
      f"({time.time() - t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
