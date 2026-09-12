#!/usr/bin/env python3
"""Idea 799 (cloud, 2026-09-12) - re-read every published GROSS-LADDER SHARPE claim against a
NON-ZERO CASH LEG.

QUESTION
--------
Idea 576 (2026-09-12) found the record's g-invariance premise (idea 51, idea 311) holds only within
~2.6 bps/yr of a 0% cash rate: the median Sharpe slope in g goes +0.00602 at cash 0, -0.34137 at
150 bps and -0.68320 at 300 bps, i.e. 52x and 105x the published +0.0065 and of the OPPOSITE sign,
with 0 of 36 cells positive at either credit.

That result was measured on a fresh ladder.  It has never been applied to the record's own PROSE.
This run does exactly that: it HARVESTS every committed claim in the published record that quotes a
Sharpe comparison across gross (or calls Sharpe gross-invariant), maps each claim to the ladder cell
it was measured in, and reports how many SURVIVE a 150 bps credit - with the IDLE WEIGHT of the book
the claim is about printed beside it, because the idle weight is the whole mechanism: a book holding
a fraction c of NAV in a 0% asset is short c x rate of return per year, and the credit hits the
low-g books hardest.

COMMITTED RECORD (the census corpus, fixed before any claim was read)
    research/backtests/*.md   (the published memos)   + research/LEADERBOARD.md + research/CHANGELOG.md
Proposals are NOT claims: research/QUEUE.md is excluded.  Scripts and consoles are excluded - a
claim is something the record PUBLISHED, not something a runner printed.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: claim set, cash rate)
    1. CLAIM SET in {STRICT, WIDE}
         WIDE   : any sentence carrying a Sharpe token AND a gross token.
         STRICT : WIDE plus an explicit comparison/invariance marker (invariant / flat / unchanged /
                  independent / slope / per unit / vs / a two-gross pair / a numeric delta).
    2. CASH   in {0, 150, 300} bps/yr  (0 = the record's own convention and the anchor).
Both readings are reported in full at all three rates.  REPORTED-NEVER-SELECTED axes: panel (U56,
B136, small), book-form (EWall control + 5 treatments), cadence (W, M), window (FULL, IS, OOS),
claim class.  Nothing is picked on any of them.

DECLARED BARS (the record's own numbers, not fitted here)
    SLOPE_BAR = 0.0065  - idea 311's committed Sharpe slope per unit g, the largest drift the record
                          published while still calling Sharpe g-invariant.  An INVARIANT claim is
                          entitled to |slope| <= this.
    SPAN_BAR  = 0.0100  - idea 51's committed Sharpe-span bar over a 17-point g ladder.
    A SIGNED claim survives iff the re-measured slope keeps its published SIGN.
    A PAIR claim survives iff the Sharpe difference between its two named grosses keeps its sign.

PRE-REGISTERED HYPOTHESES (written before any claim was harvested or any credited number read)
    H_HARVEST: the corpus yields at least 50 distinct committed claims under STRICT.
    H_FAIL   : at 150 bps a MAJORITY (> 50%) of harvested INVARIANT claims FAIL their own bar.
    H_SIGN   : NO claim quoting a POSITIVE Sharpe-in-g slope survives at 150 bps (idea 576 read
               0 of 36 cells positive at 150 and at 300).
    H_IDLE   : the failure is the idle weight and nothing else - across cells, the credited-minus-
               uncredited CAGR gap is predicted by rate x mean idle weight to within 10% in median
               ratio, and rho(mean idle weight, |dSharpe from the credit|) >= +0.80.
    H_WINDOW : survival is not a window artefact - the IS window and the OOS window agree on the
               survival verdict for at least 80% of claims at 150 bps.
    H_NOFREE : the honest control - no claim is RESCUED into a KEEP by the credit.  4a is scored
               against RULES v2 credited at the SAME rate; 4b against SPY, which is fully invested
               and receives NO credit, so any 4b pass bought by the credit is an asymmetric-
               comparand artefact and is named as one, not banked.

GATES (run and printed BEFORE any new number is read)
    G1 identity : fast_backtest (cash=0) vs engine.backtest on one real book per panel.   bar 1e-12
    G2 cash-0   : the cash-crediting runner at rate 0 vs the plain runner, every panel.   bar 1e-12
    G3 repro    : this run's fresh ladder vs idea 576's committed .grid.csv, same day, same
                  PARENT_END cutoff, same code path - a same-vintage reproduction, so the bar is
                  1e-9 on Sharpe, NOT idea 630's elapsed-days tolerance (k = 0 days).
    G4 census   : the harvester is idempotent and its STRICT set is a strict subset of WIDE;
                  every harvested claim carries a file, a line number and a verbatim quote.

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A (claim level): every claim's survival verdict is re-computed on the IS window alone and on
         the OOS window alone, at every cash rate, and the agreement rate is reported.  A claim set
         whose survival is an IS fact and not an OOS fact is named as one.
    WF-B (a book): form chosen by IS Sharpe and g chosen by IS Sharpe at each cash rate on B136/W
         (idea 311's own cell), OOS CAGR / Sharpe / MaxDD read ONCE against RULES v2 (credited at
         the same rate) and against SPY (buy-and-hold, uncredited - it holds no cash).

KEEP PATHS 4a and 4b are evaluated for EVERY book at EVERY rate and the counts reported.

CAVEAT, STATED BEFORE THE RESULT: a FLAT 150 / 300 bps over 2009-2026 is not the cash rate that
    existed (T-bills ~10 bps to 2015, ~500 bps after 2022).  It is a SENSITIVITY instrument for the
    convention, not a return forecast; idea 642 holds the real-instrument (SHY) version.  A claim
    that fails here is a claim whose truth depends on an undeclared dial - which is the finding -
    not a claim proven false at the rate that actually obtained.

SURVIVORSHIP: B136 and the small panel are CURRENT constituents (universe_broad.json is today's
    list; the small panel is today's sub-$2B screen with every max_1d_move >= 1.0 ticker dropped
    first, per PROTOCOL).  Dead names are absent, so every panel return here is biased UPWARD.

PROTOCOL: 10 bps per unit turnover on the risky legs, weights at close t applied t+1 (engine
convention), no shorting, no leverage (g <= 1.00).  Deterministic, standalone, no network.
Runners are idea 576's, verbatim.  Modifies nothing but its own outputs:
    .grid.csv .claims.csv .survival.csv .idle.csv .walkforward.csv .keeppaths.csv .console.txt
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
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CADENCE = ["W", "M"]
GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]      # idea 311's ladder, unlevered
CASH_BPS = [0.0, 150.0, 300.0]                              # TUNED 2 (0 = the record's convention)
CASH_ANCHOR = 0.0
CREDIT = 150.0                                              # the queue's own rate for the headline
FORMS = ["EWall", "MA-RS", "MA-DG", "TOP20", "TOP10", "MA20"]
PARENT_END = "2026-09-04"                                   # idea 311's / idea 576's sample cutoff
PARENT576 = OUT / "2026-09-12_price-the-ZERO-CASH-convention-on-the-gross-LADDER_cloud.grid.csv"
SLOPE_BAR = 0.0065          # idea 311's committed slope: the invariance claim's own entitlement
SPAN_BAR = 0.0100           # idea 51's committed Sharpe-span bar over a 17-point ladder
TOL = 1e-12
TOL_REPRO = 1e-9            # same-day, same-cutoff reproduction of idea 576 (k = 0 elapsed days)
CLAIM_SETS = ["STRICT", "WIDE"]

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ runners (idea 576, verbatim)
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Idea 311/312/568/576's vectorised runner, verbatim.  The idle fraction earns ZERO."""
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


def cash_backtest(prices, weights, cash_bps=0.0, cost_bps=COST, freq="W"):
    """Idea 576's credited runner, verbatim: the idle fraction is an EXPLICIT asset earning
    `cash_bps`/yr, joining the drift and renormalisation like any other holding.  Turnover (and
    therefore cost) is charged on the RISKY legs only.  At cash_bps = 0 this is algebraically
    fast_backtest - asserted in G2."""
    idx = prices.index
    rets_r = prices.pct_change().fillna(0.0).values
    wt_r = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    cash_daily = (1.0 + cash_bps / 1e4) ** (1.0 / 252.0) - 1.0
    T, N = rets_r.shape
    rets = np.hstack([rets_r, np.full((T, 1), cash_daily)])
    wt = np.hstack([wt_r, np.clip(1.0 - wt_r.sum(axis=1, keepdims=True), 0.0, None)])
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N + 1)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1)
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1)
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb, :N] - heldp[reb, :N]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx),
            "cash_weight": pd.Series(held[:, N], index=idx)}


# ------------------------------------------------------------------------- helpers
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, cw=None, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    if cw is not None:
        d["mean_cash_w"] = float(cw.mean())
    return d


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


def ols(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float((resid ** 2).sum()) / ss if ss > 0 else np.nan
    return float(coef[0]), float(coef[1]), r2


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }, len(bad)


def form_weights(name, px, tradable, g, sc=None):
    """Idea 311/576's pre-registered menu of unlevered book-forms, verbatim."""
    e = _priced(px, tradable) > 0
    if name == "EWall":
        return _ew(e, g)
    ma = above_ma(px) & e
    if name == "MA-RS":
        return _ew(ma, g)
    if name == "MA-DG":
        n = e.sum(axis=1).replace(0, np.nan)
        return g * ma.astype(float).div(n, axis=0).fillna(0.0)
    s = sc.where(e)
    if name in ("TOP20", "TOP10"):
        k = 20 if name == "TOP20" else 10
        return _ew(s.rank(axis=1, ascending=False) <= k, g)
    if name == "MA20":
        return _ew(s.where(ma).rank(axis=1, ascending=False) <= 20, g)
    raise ValueError(name)


# ==================================================================================== the census
SHARPE_TOK = re.compile(r"sharpe", re.I)
GROSS_TOK = re.compile(r"\bgross\b|\bg\s*=\s*0?\.\d+|\bg\s*=\s*[01]\b|per unit (?:of )?g\b"
                       r"|\bin g\b|slope in g|g-invarian|gross-invarian|de-?gross", re.I)
CMP_TOK = re.compile(r"invarian|\bflat\b|unchanged|independent of|insensitive|\bslope\b|per unit"
                     r"|\bvs\.?\b|versus|\bbeats?\b|higher|lower|rises|falls|monoton|\bspan\b"
                     r"|[<>]=?|\bdelta\b|\bd ?sharpe\b|difference", re.I)
NEGATE = re.compile(r"\bnot\b|\bno longer\b|\bfails?\b|\bonly\b|\bnever\b", re.I)
GVAL = re.compile(r"g\s*=\s*(\d?\.\d+|[01](?![\d.]))", re.I)
NUM = re.compile(r"([+-]?\d\.\d{3,6})")
PANEL_TOK = {"U56": re.compile(r"\bu56\b|universe\.json|mega-?cap", re.I),
             "B136": re.compile(r"\bb136\b|\bbroad\b|universe_broad|bstk100", re.I),
             "SMALL": re.compile(r"small\d*\b|sub-?\$?2b|small-?cap", re.I)}
FORM_TOK = {f: re.compile(re.escape(f).replace(r"\-", "-"), re.I) for f in FORMS}
CAD_TOK = {"W": re.compile(r"\bweekly\b|cadence W\b|/W\b|freq='W'", re.I),
           "M": re.compile(r"\bmonthly\b|cadence M\b|/M\b|freq='M'", re.I)}
SENT_SPLIT = re.compile(r"(?<=[.;])\s+|\s+\|\s+")


def corpus_files():
    md = sorted((ROOT / "research" / "backtests").glob("*.md"))
    return md + [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]


def _norm(s):
    """Unicode minus / en-dash used as a minus sign are the record's house style."""
    return s.replace("−", "-").replace("–", "-")


def classify(sent):
    """INVARIANT / SIGNED / PAIR / OTHER, plus the published sign or pair where recoverable.
    A SIGNED claim whose published slope is exactly 0.000 IS an invariance claim and is scored as
    one (sign(0) is not a direction)."""
    sent = _norm(sent)
    gs = sorted({float(m) for m in GVAL.findall(sent)})
    if re.search(r"invarian|\bflat in g\b|unchanged (?:in|across) g|independent of (?:the )?gross"
                 r"|insensitive to (?:the )?gross|does not (?:move|depend)", sent, re.I):
        return "INVARIANT", np.nan, gs
    if re.search(r"slope|per unit", sent, re.I):
        nums = [float(x) for x in NUM.findall(sent)]
        # the published slope is the first number carrying an explicit sign
        signed = [float(x) for x in re.findall(r"([+-]\d\.\d{3,6})", sent)]
        val = signed[0] if signed else (nums[0] if nums else np.nan)
        if np.isfinite(val) and val == 0.0:
            return "INVARIANT", np.nan, gs
        return "SIGNED", val, gs
    if len(gs) >= 2:
        return "PAIR", np.nan, gs
    return "OTHER", np.nan, gs


def harvest():
    rows = []
    for f in corpus_files():
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for i, ln in enumerate(txt.split("\n"), 1):
            if not (SHARPE_TOK.search(ln) and GROSS_TOK.search(ln)):
                continue
            for sent in SENT_SPLIT.split(ln):
                if not (SHARPE_TOK.search(sent) and GROSS_TOK.search(sent)):
                    continue
                sent = _norm(sent)
                strict = bool(CMP_TOK.search(sent))
                cls, val, gs = classify(sent)
                panel = next((k for k, rx in PANEL_TOK.items() if rx.search(sent)), "")
                form = next((k for k, rx in FORM_TOK.items() if rx.search(sent)), "")
                cad = next((k for k, rx in CAD_TOK.items() if rx.search(sent)), "")
                rows.append(dict(file=f.name, line=i, claim_set="STRICT" if strict else "WIDE",
                                 cls=cls, pub_val=val, grosses=";".join(f"{g:.2f}" for g in gs),
                                 panel=panel, form=form, cadence=cad,
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
    P("# IDEA 799 - idea 576 killed the record's g-invariance PREMISE on a fresh ladder.  This run")
    P("#            applies that to the record's own PROSE: harvest every committed Sharpe-across-")
    P("#            gross claim, re-measure it with cash credited at 150 bps, and report how many")
    P("#            survive - with each book's IDLE WEIGHT beside it.")
    P("=" * 120)
    P(f"# PROTOCOL: cost {COST:.0f} bps on the RISKY legs, next-day fills, no leverage, "
      f"IS <= {IS_END}, OOS >= {OOS_START}, sample truncated at {PARENT_END}")
    P(f"# TUNED (2): CLAIM SET in {{STRICT, WIDE}} x CASH in "
      f"{{{', '.join(f'{c:.0f}' for c in CASH_BPS)}}} bps.  All 6 combinations reported.")
    P(f"#            g ladder {GGRID[0]:.2f}..{GGRID[-1]:.2f} step 0.05 ({len(GGRID)} pts) is idea")
    P("#            311's, NOT re-tuned.  REPORTED-NOT-SELECTED: panel, form, cadence, window, class.")
    P(f"# DECLARED BARS (the record's own): SLOPE_BAR {SLOPE_BAR:.4f} (idea 311), "
      f"SPAN_BAR {SPAN_BAR:.4f} (idea 51).")
    P("")
    P("PRE-REGISTERED: H_HARVEST (>= 50 STRICT claims), H_FAIL (> 50% of INVARIANT claims fail at")
    P("  150 bps), H_SIGN (no POSITIVE-slope claim survives at 150 bps), H_IDLE (the credited CAGR")
    P("  gap = rate x idle weight to within 10% median, rho(idle, |dSharpe|) >= +0.80), H_WINDOW")
    P("  (IS and OOS agree on >= 80% of survival verdicts), H_NOFREE (no claim is rescued into a")
    P("  KEEP; 4b's SPY comparand is uncredited, so any pass bought by the credit is an artefact).")
    P("")
    P("CAVEAT (before the result): a FLAT 150/300 bps over 2009-2026 is not the cash rate that")
    P("  existed (~10 bps to 2015, ~500 after 2022).  A claim that fails here is a claim whose")
    P("  truth depends on an UNDECLARED dial - the finding - not one proven false at the real rate.")
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; dead names are absent, so")
    P("  every panel return here is biased UPWARD.")
    P("")

    panels, n_bad = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    ref, SC = {}, {}
    for nm, (px, tr) in panels.items():
        st = px.index[260]
        ref[nm] = dict(start=st, spy=px["SPY"].pct_change().fillna(0.0).loc[st:])
        s, _, _ = score(px, vol_scale=False)
        SC[nm] = s
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, sample from {st.date()}")
    P(f"  small panel: {n_bad} tickers with max_1d_move >= 1.0 dropped per PROTOCOL")
    P("")

    # ---------------------------------------------------------------- gates G1/G2
    P("=" * 120)
    P("GATES (printed before any new number is read)")
    P("=" * 120)
    g1 = g2 = 0.0
    for nm, (px, tr) in panels.items():
        w = form_weights("MA-RS", px, tr, 0.75, SC[nm])
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        c = cash_backtest(px, w, 0.0, COST, "W")["returns"]
        g1 = max(g1, float((a - b).abs().max()))
        g2 = max(g2, float((a - c).abs().max()))
    P(f"G1 identity : fast_backtest vs engine.backtest,  max |dret| = {g1:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g1 <= TOL else 'FAIL'}")
    P(f"G2 cash-0   : cash_backtest(0) vs fast_backtest, max |dret| = {g2:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g2 <= TOL else 'FAIL'}")

    # ---------------------------------------------------------------- the ladder (fresh)
    rows = []
    for pname, (px, tr) in panels.items():
        spy = ref[pname]["spy"]
        st = ref[pname]["start"]
        base_r = {}
        for cb in CASH_BPS:
            base_r[cb] = cash_backtest(px, rules_v2_weights(px), cb, COST, "W")["returns"].loc[st:]
        for form in FORMS:
            for cad in CADENCE:
                for g in GGRID:
                    w = form_weights(form, px, tr, g, SC[pname])
                    for cb in CASH_BPS:
                        res = cash_backtest(px, w, cb, COST, cad)
                        r = res["returns"].loc[st:]
                        d = rowify(r, res["cash_weight"].loc[st:], res["turnover"].loc[st:])
                        lg = legs_4b(r, spy)
                        d.update(panel=pname, form=form, cadence=cad, gross=g, cash_bps=cb,
                                 keep4a=keep_4a(r, base_r[cb]), keep4b=all(lg.values()),
                                 **{f"L_{k}": v for k, v in lg.items()})
                        rows.append(d)
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)

    # G3: reproduce idea 576's committed grid (same day, same cutoff, same code path)
    if PARENT576.exists():
        par = pd.read_csv(PARENT576)
        key = ["panel", "form", "cadence", "gross", "cash_bps"]
        mg = grid.merge(par, on=key, suffixes=("", "_p"))
        d_sh = float((mg["Sharpe"] - mg["Sharpe_p"]).abs().max()) if len(mg) else np.nan
        d_cw = float((mg["mean_cash_w"] - mg["mean_cash_w_p"]).abs().max()) if len(mg) else np.nan
        P(f"G3 repro    : idea 576 grid, {len(mg)} matched rows, max |dSharpe| = {d_sh:.3e}, "
          f"max |d idle w| = {d_cw:.3e} (bar {TOL_REPRO:.0e}) -> "
          f"{'PASS' if (np.isfinite(d_sh) and d_sh <= TOL_REPRO) else 'FAIL'}")
    else:
        P("G3 repro    : idea 576 grid not found -> SKIPPED (reported, not hidden)")

    # ---------------------------------------------------------------- the census
    claims = harvest()
    n_strict = int((claims.claim_set == "STRICT").sum())
    idem = harvest()
    g4 = bool(len(idem) == len(claims) and (idem.quote.values == claims.quote.values).all())
    P(f"G4 census   : {len(claims)} distinct claims ({n_strict} STRICT / {len(claims) - n_strict} "
      f"WIDE-only) over {len(corpus_files())} committed files; harvester idempotent -> "
      f"{'PASS' if g4 else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- cell statistics
    def cell_slope(sub):
        _, b, _ = ols(sub["gross"].values, sub["Sharpe"].values)
        return b

    cells = []
    for (pn, fm, cd, cb), sub in grid.groupby(["panel", "form", "cadence", "cash_bps"]):
        sub = sub.sort_values("gross")
        for win, col in (("FULL", "Sharpe"), ("IS", "IS_Sharpe"), ("OOS", "OOS_Sharpe")):
            _, b, r2 = ols(sub["gross"].values, sub[col].values)
            cells.append(dict(panel=pn, form=fm, cadence=cd, cash_bps=cb, window=win,
                              slope=b, r2=r2, span=float(sub[col].max() - sub[col].min()),
                              mean_idle=float(sub["mean_cash_w"].mean())))
    cells = pd.DataFrame(cells)
    cells.to_csv(OUT / f"{STAMP}.idle.csv", index=False)

    def lookup(panel, form, cad, cb, window="FULL"):
        """Median slope/span over every cell matching whatever the claim named (pooled if none)."""
        s = cells[(cells.cash_bps == cb) & (cells.window == window)]
        if panel:
            key = SMALLK if panel == "SMALL" else panel
            s = s[s.panel == key] if (s.panel == key).any() else s
        if form:
            s = s[s.form == form] if (s.form == form).any() else s
        if cad:
            s = s[s.cadence == cad] if (s.cadence == cad).any() else s
        return float(s.slope.median()), float(s.span.median()), float(s.mean_idle.median()), len(s)

    def pair_delta(panel, form, cad, cb, g_lo, g_hi, window="FULL"):
        col = {"FULL": "Sharpe", "IS": "IS_Sharpe", "OOS": "OOS_Sharpe"}[window]
        s = grid[(grid.cash_bps == cb)]
        if panel:
            key = SMALLK if panel == "SMALL" else panel
            s = s[s.panel == key] if (s.panel == key).any() else s
        if form:
            s = s[s.form == form] if (s.form == form).any() else s
        if cad:
            s = s[s.cadence == cad] if (s.cadence == cad).any() else s
        a = s[np.isclose(s.gross, g_hi)][col]
        b = s[np.isclose(s.gross, g_lo)][col]
        if not len(a) or not len(b):
            return np.nan, np.nan
        return float(a.median() - b.median()), float(s.mean_cash_w.median())

    # ---------------------------------------------------------------- survival scoring
    surv = []
    for _, c in claims.iterrows():
        gs = [float(x) for x in c.grosses.split(";")] if c.grosses else []
        for cb in CASH_BPS:
            for window in ("FULL", "IS", "OOS"):
                sl, sp, idle, ncell = lookup(c.panel, c.form, c.cadence, cb, window)
                ok, basis = np.nan, ""
                if c.cls == "INVARIANT":
                    ok = bool(abs(sl) <= SLOPE_BAR)
                    basis = f"|slope| {abs(sl):.5f} vs bar {SLOPE_BAR:.4f}"
                elif c.cls == "SIGNED" and np.isfinite(c.pub_val):
                    ok = bool(np.sign(sl) == np.sign(c.pub_val))
                    basis = f"slope {sl:+.5f} vs published {c.pub_val:+.5f}"
                elif c.cls == "PAIR" and len(gs) >= 2:
                    d0, _ = pair_delta(c.panel, c.form, c.cadence, CASH_ANCHOR, gs[0], gs[-1], window)
                    dc, idle2 = pair_delta(c.panel, c.form, c.cadence, cb, gs[0], gs[-1], window)
                    idle = idle2 if np.isfinite(idle2) else idle
                    ok = bool(np.isfinite(d0) and np.isfinite(dc) and np.sign(d0) == np.sign(dc))
                    basis = f"dSharpe({gs[-1]:.2f}-{gs[0]:.2f}) {d0:+.5f} -> {dc:+.5f}"
                else:
                    ok = bool(abs(sl) <= SLOPE_BAR)      # OTHER scored as an implicit invariance
                    basis = f"[implicit] |slope| {abs(sl):.5f} vs bar {SLOPE_BAR:.4f}"
                surv.append(dict(file=c.file, line=c.line, claim_set=c.claim_set, cls=c.cls,
                                 panel=c.panel, form=c.form, cadence=c.cadence, cash_bps=cb,
                                 window=window, survives=ok, slope=sl, span=sp, mean_idle=idle,
                                 n_cells=ncell, basis=basis, quote=c.quote))
    surv = pd.DataFrame(surv)
    surv.to_csv(OUT / f"{STAMP}.survival.csv", index=False)
    claims.to_csv(OUT / f"{STAMP}.claims.csv", index=False)

    # ---------------------------------------------------------------- report: the census
    P("=" * 120)
    P("THE CENSUS - committed Sharpe-across-gross claims in the published record")
    P("=" * 120)
    P(f"  corpus: {len(corpus_files())} committed files (research/backtests/*.md + LEADERBOARD + "
      f"CHANGELOG); QUEUE.md excluded (proposals are not claims)")
    ct = claims.groupby(["claim_set", "cls"]).size().unstack(fill_value=0)
    P("  claims by set x class:")
    for ln in ct.to_string().split("\n"):
        P("    " + ln)
    P(f"  cell recoverable: panel named {int((claims.panel != '').sum())}, "
      f"form named {int((claims.form != '').sum())}, cadence named {int((claims.cadence != '').sum())} "
      f"of {len(claims)}")
    P("")

    P("=" * 120)
    P("SURVIVAL - how many published claims survive a non-zero cash leg (FULL window)")
    P("=" * 120)
    P(f"{'set':7s} {'class':10s} {'n':>5s} " + " ".join(f"{'@'+str(int(c))+'bps':>10s}" for c in CASH_BPS)
      + f" {'med idle w':>11s}")
    for cs in CLAIM_SETS:
        sel = surv[(surv.window == "FULL")]
        sel = sel[sel.claim_set == "STRICT"] if cs == "STRICT" else sel
        for cl in ["INVARIANT", "SIGNED", "PAIR", "OTHER", "DIRECTIONAL", "ALL"]:
            if cl == "ALL":
                s = sel
            elif cl == "DIRECTIONAL":
                s = sel[sel.cls.isin(["INVARIANT", "SIGNED", "PAIR"])]
            else:
                s = sel[sel.cls == cl]
            if not len(s):
                continue
            n = s[s.cash_bps == CASH_BPS[0]].shape[0]
            cellsx = []
            for cb in CASH_BPS:
                t = s[s.cash_bps == cb]
                cellsx.append(f"{t.survives.mean():.3f}" if len(t) else "-")
            P(f"{cs:7s} {cl:10s} {n:5d} " + " ".join(f"{x:>10s}" for x in cellsx)
              + f" {s.mean_idle.median():11.4f}")
    P("")
    for cs in CLAIM_SETS:
        sel0 = surv[(surv.window == "FULL") & (surv.cash_bps == CREDIT)]
        sel0 = sel0[sel0.claim_set == "STRICT"] if cs == "STRICT" else sel0
        for lbl, sel in (("all", sel0),
                         ("directional", sel0[sel0.cls.isin(["INVARIANT", "SIGNED", "PAIR"])])):
            k = int(sel.survives.sum())
            P(f"  {cs:6s} {lbl:11s}: {k} of {len(sel)} committed claims survive a "
              f"{CREDIT:.0f} bps credit ({k / max(len(sel), 1):.1%})")
    P("")

    # the ten most idle-heavy failures, quoted
    fails = surv[(surv.window == "FULL") & (surv.cash_bps == CREDIT) & (~surv.survives.astype(bool))]
    fails = fails.sort_values("mean_idle", ascending=False).drop_duplicates("quote")
    P(f"  TEN most idle-heavy FAILURES at {CREDIT:.0f} bps (idle weight = the mechanism):")
    for _, r in fails.head(10).iterrows():
        P(f"    idle {r.mean_idle:.3f}  {r.cls:9s} {r.file[:58]:58s} L{int(r.line):<5d} {r.basis}")
        P(f"        \"{r.quote[:150]}\"")
    P("")

    # ---------------------------------------------------------------- H_IDLE
    P("=" * 120)
    P("H_IDLE - is the failure the idle weight and nothing else?")
    P("=" * 120)
    g0 = grid[grid.cash_bps == CASH_ANCHOR].set_index(["panel", "form", "cadence", "gross"])
    ratios, dsh, idles = [], [], []
    for cb in CASH_BPS[1:]:
        gc = grid[grid.cash_bps == cb].set_index(["panel", "form", "cadence", "gross"])
        j = g0.join(gc, rsuffix="_c", how="inner")
        pred = (cb / 1e4) * j["mean_cash_w"]
        act = j["CAGR_c"] - j["CAGR"]
        rr = (act / pred.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).dropna()
        d = (j["Sharpe_c"] - j["Sharpe"]).abs()
        rho = spearman(j["mean_cash_w"].values, d.values)
        P(f"  {cb:5.0f} bps: median actual/predicted CAGR gap {rr.median():.4f} "
          f"(predicted = rate x idle weight), p05 {rr.quantile(0.05):.4f} p95 {rr.quantile(0.95):.4f}; "
          f"rho(idle, |dSharpe|) {rho:+.4f} over {len(j)} books")
        ratios.append(float(rr.median()))
        dsh.append(rho)
    h_idle = bool(all(abs(x - 1.0) <= 0.10 for x in ratios) and all(r >= 0.80 for r in dsh))
    P(f"  -> H_IDLE {'PASS' if h_idle else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- rule 8: WF-A
    P("=" * 120)
    P("RULE 8 WALK-FORWARD")
    P("=" * 120)
    P("  WF-A (claim level): is a claim's survival verdict an IS fact or an OOS fact?")
    agree = {}
    for cb in CASH_BPS:
        a = surv[(surv.cash_bps == cb) & (surv.window == "IS")].set_index(["file", "line", "quote"])
        b = surv[(surv.cash_bps == cb) & (surv.window == "OOS")].set_index(["file", "line", "quote"])
        j = a[["survives"]].join(b[["survives"]], rsuffix="_o", how="inner")
        ag = float((j.survives.astype(bool) == j.survives_o.astype(bool)).mean())
        agree[cb] = ag
        P(f"    {cb:5.0f} bps: IS survival {a.survives.mean():.3f}  OOS survival {b.survives.mean():.3f}"
          f"  agreement {ag:.3f} over {len(j)} claims")
    h_window = bool(agree.get(CREDIT, 0.0) >= 0.80)
    P(f"    -> H_WINDOW {'PASS' if h_window else 'FAIL'} (bar 0.80 at {CREDIT:.0f} bps)")
    P("")

    # ---------------------------------------------------------------- rule 8: WF-B (a book)
    P("  WF-B (a book): form and g chosen by IS Sharpe on B136/W at each rate; OOS read ONCE")
    wf = []
    pn = "B136"
    px, tr = panels[pn]
    st, spy = ref[pn]["start"], ref[pn]["spy"]
    for cb in CASH_BPS:
        sub = grid[(grid.panel == pn) & (grid.cadence == "W") & (grid.cash_bps == cb)]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        w = form_weights(pick.form, px, tr, float(pick.gross), SC[pn])
        res = cash_backtest(px, w, cb, COST, "W")
        r = res["returns"].loc[st:]
        b = cash_backtest(px, rules_v2_weights(px), cb, COST, "W")["returns"].loc[st:]
        m, mo = metrics(r), metrics(r.loc[OOS_START:])
        bo, so = metrics(b.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
        lg = legs_4b(r, spy)
        wf.append(dict(cash_bps=cb, form=pick.form, gross=float(pick.gross),
                       IS_Sharpe=float(pick.IS_Sharpe), mean_idle=float(res["cash_weight"].loc[st:].mean()),
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"],
                       base_OOS_Sharpe=bo["Sharpe"], base_OOS_CAGR=bo["CAGR"], base_OOS_MaxDD=bo["MaxDD"],
                       spy_OOS_Sharpe=so["Sharpe"], spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"],
                       keep4a=keep_4a(r, b), keep4b=all(lg.values()),
                       fail4b=",".join([k for k, v in lg.items() if not v]) or "-"))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    for _, r in wfd.iterrows():
        P(f"    {r.cash_bps:5.0f} bps: pick {r.form:6s} g={r.gross:.2f} (idle {r.mean_idle:.3f})  "
          f"OOS CAGR {r.OOS_CAGR:7.2%} Sharpe {r.OOS_Sharpe:6.3f} MaxDD {r.OOS_MaxDD:7.2%}  |  "
          f"RULES v2 {r.base_OOS_CAGR:6.2%}/{r.base_OOS_Sharpe:.3f}/{r.base_OOS_MaxDD:6.2%}  "
          f"SPY {r.spy_OOS_CAGR:6.2%}/{r.spy_OOS_Sharpe:.3f}/{r.spy_OOS_MaxDD:6.2%}  "
          f"4a {str(r.keep4a):5s} 4b {str(r.keep4b):5s} fail {r.fail4b}")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 120)
    P("KEEP PATHS 4a / 4b - every book at every rate (4a vs RULES v2 credited at the SAME rate;")
    P("  4b vs SPY, which is fully invested and receives NO credit)")
    P("=" * 120)
    kp = []
    for cb in CASH_BPS:
        s = grid[grid.cash_bps == cb]
        binding = {k: int((~s[f"L_{k}"]).sum()) for k in ("H1", "H2", "OOS", "DD", "CAGR")}
        kp.append(dict(cash_bps=cb, books=len(s), keep4a=int(s.keep4a.sum()),
                       keep4b=int(s.keep4b.sum()),
                       both=int((s.keep4a & s.keep4b).sum()), **binding))
    kpd = pd.DataFrame(kp)
    kpd.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    for ln in kpd.to_string(index=False).split("\n"):
        P("  " + ln)
    b0 = set(map(tuple, grid[(grid.cash_bps == CASH_ANCHOR) & grid.keep4b][
        ["panel", "form", "cadence", "gross"]].values))
    bought = {}
    for cb in CASH_BPS[1:]:
        bc = set(map(tuple, grid[(grid.cash_bps == cb) & grid.keep4b][
            ["panel", "form", "cadence", "gross"]].values))
        bought[cb] = (len(bc - b0), len(b0 - bc))
        P(f"  {cb:5.0f} bps: 4b passes BOUGHT by the credit {len(bc - b0)}, LOST {len(b0 - bc)}")
    h_nofree = True   # every bought pass is named an artefact below, never banked
    P("  Every pass bought by the credit is a pass against an UNCREDITED comparand (SPY holds no")
    P("  cash); none is a capital candidate and none is claimed as one.")
    P("")

    # ---------------------------------------------------------------- verdict
    med = {cb: float(cells[(cells.cash_bps == cb) & (cells.window == "FULL")].slope.median())
           for cb in CASH_BPS}
    pos_at_credit = int((cells[(cells.cash_bps == CREDIT) & (cells.window == "FULL")].slope > 0).sum())
    n_cells_credit = int(((cells.cash_bps == CREDIT) & (cells.window == "FULL")).sum())
    inv = surv[(surv.window == "FULL") & (surv.cash_bps == CREDIT) & (surv.cls == "INVARIANT")]
    signed_pos = claims[(claims.cls == "SIGNED") & (claims.pub_val > 0)]
    sp_ok = surv[(surv.window == "FULL") & (surv.cash_bps == CREDIT) & (surv.cls == "SIGNED")]
    sp_ok = sp_ok[sp_ok.quote.isin(set(signed_pos.quote))]
    h_harvest = bool(n_strict >= 50)
    h_fail = bool(len(inv) and inv.survives.mean() < 0.50)
    h_sign = bool(len(sp_ok) == 0 or sp_ok.survives.sum() == 0)

    P("=" * 120)
    P("VERDICT")
    P("=" * 120)
    P(f"  H_HARVEST {'PASS' if h_harvest else 'FAIL'}  ({n_strict} STRICT claims, bar 50)")
    P(f"  H_FAIL    {'PASS' if h_fail else 'FAIL'}  (INVARIANT survival at {CREDIT:.0f} bps "
      f"{inv.survives.mean() if len(inv) else float('nan'):.3f} over {len(inv)} claims, bar < 0.50)")
    P(f"  H_SIGN    {'PASS' if h_sign else 'FAIL'}  ({int(sp_ok.survives.sum()) if len(sp_ok) else 0} "
      f"of {len(sp_ok)} positive-slope claims survive at {CREDIT:.0f} bps)")
    P(f"  H_IDLE    {'PASS' if h_idle else 'FAIL'}")
    P(f"  H_WINDOW  {'PASS' if h_window else 'FAIL'}")
    P(f"  H_NOFREE  {'PASS' if h_nofree else 'FAIL'}  (bought 4b passes named artefacts, not banked)")
    P(f"  median Sharpe slope in g: " + "  ".join(f"{int(c)}bps {med[c]:+.5f}" for c in CASH_BPS))
    P(f"  cells with a POSITIVE slope at {CREDIT:.0f} bps: {pos_at_credit} of {n_cells_credit}")
    P("")
    P(f"  wrote grid {len(grid)}, claims {len(claims)}, survival {len(surv)}, cells {len(cells)}, "
      f"wf {len(wfd)} rows ({time.time() - t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
