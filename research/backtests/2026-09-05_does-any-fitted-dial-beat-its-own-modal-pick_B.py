#!/usr/bin/env python3
"""QUEUE idea 189 — does-any-fitted-dial-beat-its-own-modal-pick  (lane B, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 189)
    "idea 175 found the pre-registered constant M beats the IS selector that picks M in 79% of
     books (+0.0761 vs +0.0388), because the selector's rare off-modal picks are catastrophic.
     Generalise it: for every dial in idea 171's five, compare the selector against a constant
     fixed at the selector's OWN modal pick.  If the constant wins on all five, 'fit the dial'
     is dominated by 'read the mode once and write it down', which is a PROTOCOL clause, not a
     backtest."

WHY THIS IS NOT IDEA 171 AGAIN.
    Idea 171 asked: does an IS-fitted dial beat the INHERITED constant (the incumbent)?  Answer:
    ahead on 3/5, significant on 2/5, and both of those explained away by ladder geometry.
    Idea 175 asked a sharper question on ONE dial: the selector picks M in 79% of books, so what
    does it buy over just WRITING M DOWN?  Answer there: nothing — the constant M (+0.0761) beat
    the selector that mostly picks M (+0.0388), because the selector's 21% off-modal picks lost
    more than its modal picks won.  This run generalises that to all five dials.
    The comparison is therefore MODE vs SELECTOR, not MODE vs INCUMBENT.  MODE vs INCUMBENT is
    also reported, because a mode arm that beats the selector but loses to the incumbent changes
    nothing for RULES.

THE MODE ARM, and the one honest way to build it.
    The naive mode ("modal pick of the selector across the corpus") is read on the same 53 books
    it is then scored on, so it borrows corpus-level hindsight even though every underlying pick
    is IS-only.  Both versions are reported and the LEAVE-ONE-OUT one is the headline:
        MODE-IC   the modal pick over ALL books                          (in-corpus; upper read)
        MODE-LOO  for book b, the modal pick over the other 52 books     (honest; headline)
    Ties in the mode are broken by ladder order (lowest index), deterministically.
    Note what MODE-LOO is NOT: it is not a selector.  It reads no property of the book it is
    applied to.  It is a single number a human could write into RULES.md once.

THE FIVE DIALS — identical to idea 171 (same ladders, same incumbents, same corpus), because
    this run must reproduce that table before it may add a row to it.
    GROSS    g in {0.20..1.00}, 10 points, incumbent 0.75
    N        n in {3..50},      10 points, incumbent 20
    BAND     b in {0.00..0.08},  5 points, incumbent 0.00
    CADENCE  f in {D,W,M,Q},     4 points, incumbent W
    SLEEVE   f in {0.00..0.30},  7 points, incumbent 0.00
    36 ladder points x 53 books = 1908 ladder rows, every one reported in .ladder.csv.

TUNED PARAMETERS — exactly two, per PROTOCOL rule 4, unchanged from idea 171.
    1. the SELECTOR, 2 values, both reported, neither preferred: SEL-SHARPE (IS Sharpe argmax)
       and SEL-4B (IS 4b relative min-margin argmax).
    2. the LADDER POINT, swept exhaustively (36 points), ALL reported.
    The MODE is DERIVED from the selector's picks, not tuned: it has no free parameter.
    Controls (not tuned): CONST (incumbent), RANDOM (seeded uniform ladder point), ORACLE (OOS
    argmax, not implementable).

CORPUS — idea 171's 53 books exactly: 5 fixed panels (U56, B136, BSTK100, ETF36, SMALL484) plus
    48 sub-panels of B136 (k in {20,40,80} x 16 draws, rng seed 171500+k).  Books inside a family
    are correlated draws, so the pooled t OVERSTATES significance (idea 175's own criticism of
    idea 171, which applies to this run too): per-family tables are printed beside every pooled
    number and the family count, not the book count, is the honest sample size.

WALK-FORWARD (PROTOCOL rule 8).  The design IS the walk-forward: every selector and every mode
    reads the <= 2016-12-31 window only; 2017-01-01..2026 is read once, at the end.
    .walkforward.csv reports per dial and arm the mean OOS CAGR/Sharpe/MaxDD over the 53 books
    and the classic S1 pick, both against RULES v1 and SPY.

REPRODUCTION, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        turnover at all four cadences.
    [b] at BAND=0 this script's CAND-n weights equal idea 78's weights_cand exactly.
    [c] the 1908-row ladder reproduces idea 171's COMMITTED .ladder.csv to < 1e-10 on every
        numeric column.  Without [c] this is a different experiment wearing idea 171's name.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b] and [c] all hold.
    P2  MODE-LOO beats SEL-SHARPE (mean d > 0) on at least 4 of the 5 dials.  Idea 175's
        mechanism — rare off-modal picks that lose more than the modal picks win — is a property
        of argmax noise, not of the cadence ladder.
    P3  On the dials whose ladder is monotone and truncated (GROSS, SLEEVE) the selector's
        deviation rate is LOW (it runs to the same endpoint every time), so MODE-LOO ~ SEL-SHARPE
        there, |mean d| < 0.01.  The action is on N, BAND and CADENCE.
    P4  Decomposition: on books where the selector agrees with its own LOO mode the paired
        difference is exactly 0.0, so 100% of any MODE-vs-SEL gap comes from deviating books.
        This is arithmetic, and it is stated so the size of the per-deviation loss is the number
        that carries the finding.
    P5  MODE-LOO does NOT beat the INCUMBENT constant on all five dials: on GROSS the mode is the
        ladder endpoint g=1.00 and idea 166/171 already priced that as a loss.  So "read the mode
        and write it down" is better than fitting, and still not better than doing nothing.
    P6  MODE-IC and MODE-LOO differ on few books (the mode is stable), so the in-corpus version's
        hindsight is worth < 0.01 Sharpe.
    P7  No arm produces a new 4b KEEP; this is a methodology run.  (Idea 171 found 250 of 1908
        rows pass 4b, 214 of them on sub-panels which are a corpus device and not tradable.)

CAVEATS carried, not buried
    * Survivorship: B136, U56 and SMALL484 are current-constituent lists (idea 54).  All arms
      inherit it equally, so the paired comparison is unaffected; the LEVEL of every number is
      not.
    * Idea 144: a re-grossed/re-cadenced/re-sleeved book is the SAME book.  Nothing on a ladder
      here is a new signal.
    * Idea 38 (calendar-day price index: D and Q rebalance on some non-trading days after
      2014-09-17) and idea 126 (t+1 execution only) carry over.
    * Idea 183: the SLEEVE and GROSS ladders are truncated at their incumbent-favouring end; the
      anchor's rank on its own ladder is printed for every dial.
    * The mode is read from THIS corpus.  A mode is only worth writing into RULES if it is stable
      across corpora; idea 175's second corpus (115 disjoint books) agreed on CADENCE=M, which is
      one replication, not a guarantee.  Stated, not assumed.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .choices.csv, .paired.csv,
.modes.csv, .deviations.csv, .walkforward.csv, .keep.csv.
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_does-any-fitted-dial-beat-its-own-modal-pick_B"
REF_LADDER = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C.ladder.csv"
OUT = ROOT / "research" / "backtests"

COST_BPS = 10
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
EPS = 0.05
SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]

DIALS = {
    "GROSS":   ([0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00], 0.75),
    "N":       ([3, 5, 8, 10, 15, 20, 25, 30, 40, 50], 20),
    "BAND":    ([0.00, 0.02, 0.03, 0.05, 0.08], 0.00),
    "CADENCE": (["D", "W", "M", "Q"], "W"),
    "SLEEVE":  ([0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], 0.00),
}
DIAL_ORDER = ["GROSS", "N", "BAND", "CADENCE", "SLEEVE"]
INC = {d: DIALS[d][1] for d in DIALS}
ARMS = ["CONST", "SEL-SHARPE", "MODE-SHARPE-IC", "MODE-SHARPE-LOO",
        "SEL-4B", "MODE-4B-LOO", "RANDOM", "ORACLE"]

KS = [20, 40, 80]
N_DRAWS = 16
SEED = 171_500          # idea 171's corpus seed, unchanged so the corpus is identical

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- fast backtest (idea 171's)
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq="W"):
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


# ---------------------------------------------------------------- book construction (idea 171's)
def above_band(px, b):
    ma = px.rolling(200).mean()
    if b == 0.0:
        return px > ma
    st = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    st = st.mask(px > ma * (1 + b), 1.0).mask(px < ma * (1 - b), 0.0)
    return st.ffill().fillna(0.0) > 0.5


def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Book:
    def __init__(self, name, px, tradable, parent):
        self.name, self.px, self.parent = name, px, parent
        self.tradable = [c for c in px.columns if c in tradable]
        self.comp = comp_score(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = {}
        drop = [c for c in px.columns if c not in set(self.tradable)]
        for b in DIALS["BAND"][0]:
            m = (above_band(px, b) & (vol20 < MAX_VOL)).copy()
            if drop:
                m[drop] = False
            self.elig[b] = m
        self.sleeve_cols = [c for c in SLEEVE_ASSETS if c in px.columns]

    def core_weights(self, n, gross, band):
        elig = self.elig[band]
        rank = self.comp.where(elig).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (gross / n)

    def weights(self, gross, n, band, sleeve):
        w = self.core_weights(n, gross, band)
        if sleeve > 0.0 and self.sleeve_cols:
            w = w * (1.0 - sleeve)
            for c in self.sleeve_cols:
                w[c] = w[c] + sleeve / len(self.sleeve_cols)
        return w


def build_corpus():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    add = ref[SLEEVE_ASSETS].reindex(pxs.index, method="ffill")
    pxs = pd.concat([pxs.drop(columns=SLEEVE_ASSETS, errors="ignore"), add], axis=1)

    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c not in set(["SPY"] + SLEEVE_ASSETS)]

    def keep(px, cols):
        cols = [c for c in cols if c in px.columns]
        allc = list(dict.fromkeys(cols + ["SPY"] + [c for c in SLEEVE_ASSETS if c in px.columns]))
        return px[allc].dropna(how="all").ffill()

    books = []
    fixed = [
        ("U56", px56, [c for c in px56.columns if c != "SPY"], "U56"),
        ("B136", px136, [c for c in px136.columns if c != "SPY"], "B136"),
        ("BSTK100", px136, b_stk, "B136"),
        ("ETF36", px56, [c for c in etf36 if c in px56.columns], "U56"),
        ("SMALL484", pxs, s_stk, "SMALL"),
    ]
    for nm, px, tr, par in fixed:
        books.append(Book(nm, keep(px, tr), set(tr), par))

    pool = [c for c in px136.columns if c != "SPY"]
    for k in KS:
        rng = np.random.default_rng(SEED + k)
        for d in range(N_DRAWS):
            sub = sorted(rng.choice(pool, size=k, replace=False).tolist())
            books.append(Book(f"B136k{k}d{d:02d}", keep(px136, sub), set(sub), "B136"))
    return books, {"U56": px56, "B136": px136, "SMALL": pxs}


# ---------------------------------------------------------------- metric helpers (idea 171's)
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


def rel_margin(r, spy):
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    parts = {
        "H1": (h1 - s1) / max(abs(s1), EPS),
        "H2": (h2 - s2) / max(abs(s2), EPS),
        "S": (m["Sharpe"] - ms["Sharpe"]) / max(abs(ms["Sharpe"]), EPS),
        "DD": (DELTA * abs(ms["MaxDD"]) - abs(m["MaxDD"])) / max(DELTA * abs(ms["MaxDD"]), EPS),
        "CAGR": (m["CAGR"] - PHI * ms["CAGR"]) / max(abs(PHI * ms["CAGR"]), EPS),
    }
    worst = min(parts, key=parts.get)
    return min(parts.values()), worst


def keep_4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def keep_4b(r, spy, r_oos, spy_oos):
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= PHI * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


def sign_p(x):
    from math import comb
    x = np.asarray([v for v in x if np.isfinite(v) and v != 0.0], float)
    n = len(x)
    if n == 0:
        return 1.0, 0, 0
    w = int((x > 0).sum())
    k = max(w, n - w)
    tail = sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n
    return min(1.0, 2 * tail), w, n - w


def modal(points, ladder):
    """Deterministic mode: most frequent point; ties broken by ladder order (lowest index)."""
    c = Counter(points)
    best = max(c.values())
    for p in ladder:
        if c.get(p, 0) == best:
            return p
    return ladder[0]


# ---------------------------------------------------------------- reproduction controls
def check_a(book):
    P("  [a] fast_backtest vs engine.backtest (products/backtester/engine.py), same book:")
    w = book.weights(INC["GROSS"], INC["N"], INC["BAND"], INC["SLEEVE"])
    ok = True
    for fq in ["D", "W", "M", "Q"]:
        a = backtest(book.px, w, cost_bps=COST_BPS, freq=fq)
        b = fast_backtest(book.px, w, cost_bps=COST_BPS, freq=fq)
        dr = float((a["returns"] - b["returns"]).abs().max())
        dt = float((a["turnover"] - b["turnover"]).abs().max())
        P(f"      {book.name:9s} freq={fq}  max|dret|={dr:.3e}  max|dturn|={dt:.3e}")
        ok &= dr < 1e-12 and dt < 1e-10
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_b(book):
    _, above, vol20 = score(book.px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in book.px.columns if c not in set(book.tradable)]
    if drop:
        m[drop] = False
    s78 = score(book.px, vol_scale=False)[0]
    w78 = (s78.where(m).rank(axis=1, ascending=False) <= INC["N"]).astype(float) * (INC["GROSS"] / INC["N"])
    mine = book.core_weights(INC["N"], INC["GROSS"], 0.00)
    d = float((w78 - mine).abs().max().max())
    P(f"  [b] CAND-{INC['N']} weights vs idea 78 weights_cand on {book.name}: max|dw|={d:.3e}"
      f"  -> {'PASS' if d < 1e-12 else 'FAIL'}")
    return d < 1e-12


def check_c(lad):
    """The 1908-row ladder must reproduce idea 171's committed ladder.csv."""
    ref = OUT / REF_LADDER
    if not ref.exists():
        P(f"  [c] reference ladder {REF_LADDER} NOT FOUND -> cannot assert reproduction")
        return False
    a = pd.read_csv(ref)
    key = ["book", "dial", "point"]
    a["point"] = a["point"].astype(str)
    b = lad.copy()
    b["point"] = b["point"].astype(str)
    a = a.sort_values(key).reset_index(drop=True)
    b = b.sort_values(key).reset_index(drop=True)
    same_shape = len(a) == len(b) and (a[key].values == b[key].values).all()
    P(f"  [c] ladder vs idea 171 committed {REF_LADDER}: rows {len(b)} vs {len(a)}, "
      f"keys align={same_shape}")
    if not same_shape:
        return False
    worst, worstcol = 0.0, ""
    for c in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "turnover", "IS_Sharpe", "IS_margin",
              "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_margin"]:
        d = float(np.nanmax(np.abs(a[c].values - b[c].values)))
        if d > worst:
            worst, worstcol = d, c
    bars = float((a["fail4b"].fillna("-") == b["fail4b"].fillna("-")).mean())
    P(f"      max|delta| over 12 numeric columns = {worst:.3e} (worst: {worstcol});  "
      f"fail4b string identical in {bars:.1%}")
    ok = worst < 1e-10 and bars == 1.0
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 189 - does-any-fitted-dial-beat-its-own-modal-pick   (lane B, {pd.Timestamp.today().date()})")
    P("=" * 122)
    P("Does an IS-fitted dial beat a CONSTANT FIXED AT THAT SELECTOR'S OWN MODAL PICK, out of sample?")
    P("Five dials, paired over 53 books, leave-one-out mode as the headline arm.")
    P(f"Costs {COST_BPS} bps, t+1 execution, IS <= {IS_END}, OOS >= {OOS_START}.  "
      f"Two tuned params: SELECTOR (2) x LADDER POINT (36).")
    P("")

    books, panels = build_corpus()
    P(f"CORPUS: {len(books)} books "
      f"({len([b for b in books if not b.name.startswith('B136k')])} fixed panels + "
      f"{len([b for b in books if b.name.startswith('B136k')])} sub-panels, k in {KS} x {N_DRAWS} draws, "
      f"seed {SEED}+k) - idea 171's corpus, unchanged")
    for b in books[:5]:
        P(f"   {b.name:9s} {b.px.shape[0]}d x {b.px.shape[1]}c  tradable={len(b.tradable):3d}  "
          f"{b.px.index[0].date()}..{b.px.index[-1].date()}  sleeve={b.sleeve_cols}")
    P("")

    P("REPRODUCTION CONTROLS [a] and [b] (asserted before any new number is read)")
    okA = check_a(books[1])
    okB = all(check_b(b) for b in books[:3])
    if not (okA and okB):
        P("\n*** REPRODUCTION FAILED - this is not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    START, SPY, BASE = {}, {}, {}
    for b in books:
        if b.parent not in SPY:
            px = panels[b.parent]
            st = px.index[260]
            START[b.parent] = st
            SPY[b.parent] = px["SPY"].pct_change().fillna(0.0).loc[st:]
            BASE[b.parent] = fast_backtest(px, rules_v1_weights(px), COST_BPS, "W")["returns"].loc[st:]
    for k, v in SPY.items():
        m, mo = metrics(v), metrics(v.loc[OOS_START:])
        h1, h2 = halves(v)
        mb = metrics(BASE[k])
        P(f"  benchmark {k:6s} SPY  CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:7.2%} "
          f"halves {h1:.3f}/{h2:.3f}  OOS Sharpe {mo['Sharpe']:.3f} | RULES v1 Sharpe {mb['Sharpe']:.3f}")
    P("")

    P("RUNNING LADDERS ...")
    rows = []
    for bi, bk in enumerate(books):
        st = START[bk.parent]
        spy = SPY[bk.parent].reindex(bk.px.loc[st:].index).fillna(0.0)
        base = BASE[bk.parent].reindex(bk.px.loc[st:].index).fillna(0.0)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        for dial in DIAL_ORDER:
            ladder, _ = DIALS[dial]
            for pt in ladder:
                kw = dict(gross=INC["GROSS"], n=INC["N"], band=INC["BAND"], sleeve=INC["SLEEVE"])
                fq = INC["CADENCE"]
                if dial == "GROSS": kw["gross"] = pt
                elif dial == "N": kw["n"] = pt
                elif dial == "BAND": kw["band"] = pt
                elif dial == "SLEEVE": kw["sleeve"] = pt
                elif dial == "CADENCE": fq = pt
                res = fast_backtest(bk.px, bk.weights(**kw), COST_BPS, fq)
                r = res["returns"].loc[st:]
                r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                mf, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
                mg_is, wb_is = rel_margin(r_is, spy_is)
                mg_oos, wb_oos = rel_margin(r_oos, spy_oos)
                h1, h2 = halves(r)
                rows.append(dict(
                    book=bk.name, parent=bk.parent, dial=dial, point=pt,
                    is_incumbent=(pt == INC[dial]),
                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                    turnover=res["turnover"].loc[st:].sum() / mf["Years"],
                    IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"], IS_margin=mg_is,
                    IS_worstbar=wb_is,
                    OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                    OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                    fail4a=keep_4a(r, base), fail4b=keep_4b(r, spy, r_oos, spy_oos)))
        if (bi + 1) % 10 == 0:
            P(f"   ... {bi+1}/{len(books)} books  ({time.time()-t0:.0f}s)")
    lad = pd.DataFrame(rows)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    P(f"   {len(lad)} ladder rows -> {STEM}.ladder.csv   ({time.time()-t0:.0f}s)")
    P("")

    P("REPRODUCTION CONTROL [c]")
    okC = check_c(lad)
    if not okC:
        P("\n*** [c] FAILED: this corpus is not idea 171's.  Every comparison below would be to a")
        P("*** different experiment.  Numbers are still written out, but the run is NOT a")
        P("*** replication and no verdict may be read from it.")
    P("")

    # ---- ladder shape (idea 171's table, reproduced so the geometry is on the face of this run)
    P("LADDER SHAPE - mean over the 53 books of each point's OOS Sharpe (flat ladder => nothing to choose)")
    for dial in DIAL_ORDER:
        sub = lad[lad.dial == dial]
        g = sub.groupby("point", sort=False)[["OOS_Sharpe", "OOS_margin"]].mean()
        P(f"  {dial:8s} OOS Sharpe  " + " ".join(f"{p}:{g.loc[p,'OOS_Sharpe']:.3f}" for p in DIALS[dial][0]))
        sp = g["OOS_Sharpe"]
        P(f"  {'':8s} spread {sp.max()-sp.min():.3f};  incumbent {INC[dial]} ranks "
          f"{int(sp.rank(ascending=False).loc[INC[dial]])}/{len(sp)};  best point {sp.idxmax()}")
    P("")

    # ---- picks, then the modes derived from them
    picks = {}      # (dial, selector) -> {book: point}
    for dial in DIAL_ORDER:
        ladder = DIALS[dial][0]
        for sel, col in [("SHARPE", "IS_Sharpe"), ("4B", "IS_margin")]:
            d = {}
            for bk in books:
                sub = lad[(lad.dial == dial) & (lad.book == bk.name)].set_index("point").reindex(ladder)
                d[bk.name] = sub[col].idxmax()
            picks[(dial, sel)] = d

    P("=" * 122)
    P("THE MODE ARMS.  Every pick below is IS-only (<= 2016-12-31); the mode is a count over picks,")
    P("not a new fit.  MODE-LOO for book b excludes b's own pick, so no book scores its own mode.")
    P("")
    P(f"  {'dial':8s} {'sel':7s} {'modal pick':>11s} {'share':>7s} {'incumbent':>10s} "
      f"{'LOO mode differs from IC in':>29s} {'selector deviates from LOO mode in':>36s}")
    mode_rows = []
    modes_ic, modes_loo = {}, {}
    for dial in DIAL_ORDER:
        ladder = DIALS[dial][0]
        for sel in ["SHARPE", "4B"]:
            pk = picks[(dial, sel)]
            m_ic = modal(list(pk.values()), ladder)
            loo = {}
            for bk in books:
                others = [v for k, v in pk.items() if k != bk.name]
                loo[bk.name] = modal(others, ladder)
            modes_ic[(dial, sel)] = m_ic
            modes_loo[(dial, sel)] = loo
            share = np.mean([v == m_ic for v in pk.values()])
            n_loo_diff = sum(1 for b in books if loo[b.name] != m_ic)
            n_dev = sum(1 for b in books if pk[b.name] != loo[b.name])
            P(f"  {dial:8s} {sel:7s} {str(m_ic):>11s} {share:7.1%} {str(INC[dial]):>10s} "
              f"{n_loo_diff:20d}/{len(books)} {n_dev:27d}/{len(books)}")
            mode_rows.append(dict(dial=dial, selector=sel, mode_ic=m_ic, mode_share=share,
                                  incumbent=INC[dial], mode_eq_incumbent=(m_ic == INC[dial]),
                                  n_loo_differs=n_loo_diff, n_selector_deviates=n_dev, n=len(books)))
    pd.DataFrame(mode_rows).to_csv(OUT / f"{STEM}.modes.csv", index=False)
    P("")
    P("  full pick distributions (SEL-SHARPE):")
    for dial in DIAL_ORDER:
        vc = Counter(picks[(dial, "SHARPE")].values())
        P(f"    {dial:8s} " + " ".join(f"{p}:{vc.get(p,0)}" for p in DIALS[dial][0]))
    P("")

    # ---- assemble every arm's choice per book
    rng_rand = np.random.default_rng(189_900)
    choices = []
    for dial in DIAL_ORDER:
        ladder, const = DIALS[dial]
        for bk in books:
            sub = lad[(lad.dial == dial) & (lad.book == bk.name)].set_index("point").reindex(ladder)
            pick = {
                "CONST": const,
                "SEL-SHARPE": picks[(dial, "SHARPE")][bk.name],
                "MODE-SHARPE-IC": modes_ic[(dial, "SHARPE")],
                "MODE-SHARPE-LOO": modes_loo[(dial, "SHARPE")][bk.name],
                "SEL-4B": picks[(dial, "4B")][bk.name],
                "MODE-4B-LOO": modes_loo[(dial, "4B")][bk.name],
                "RANDOM": ladder[int(rng_rand.integers(len(ladder)))],
                "ORACLE": sub["OOS_Sharpe"].idxmax(),
            }
            for arm, pt in pick.items():
                r = sub.loc[pt]
                choices.append(dict(dial=dial, book=bk.name, parent=r.parent, arm=arm, point=pt,
                                    IS_Sharpe=r.IS_Sharpe, IS_margin=r.IS_margin,
                                    OOS_Sharpe=r.OOS_Sharpe, OOS_margin=r.OOS_margin,
                                    OOS_CAGR=r.OOS_CAGR, OOS_MaxDD=r.OOS_MaxDD,
                                    fail4a=r.fail4a, fail4b=r.fail4b))
    ch = pd.DataFrame(choices)
    ch.to_csv(OUT / f"{STEM}.choices.csv", index=False)

    # ---- THE HEADLINE TEST: mode minus selector
    paired = []
    P("=" * 122)
    P("HEADLINE - MODE MINUS SELECTOR, paired over 53 books.  Positive = 'write the mode down' beats 'fit the dial'.")
    P("")
    for scorenm in ["OOS_Sharpe", "OOS_margin"]:
        P(f"  --- OOS score = {scorenm} " + "-" * 88)
        P(f"  {'dial':8s} {'contrast':28s} {'mean d':>9s} {'median d':>9s} {'t':>7s} {'win':>4s} "
          f"{'loss':>5s} {'tie':>4s} {'sign p':>7s}  verdict")
        for dial in DIAL_ORDER:
            for mode_arm, sel_arm in [("MODE-SHARPE-LOO", "SEL-SHARPE"),
                                      ("MODE-SHARPE-IC", "SEL-SHARPE"),
                                      ("MODE-4B-LOO", "SEL-4B")]:
                a = ch[(ch.dial == dial) & (ch.arm == mode_arm)].set_index("book")[scorenm]
                b = ch[(ch.dial == dial) & (ch.arm == sel_arm)].set_index("book")[scorenm]
                d = (a - b).reindex(b.index)
                p, w, l = sign_p(d.values)
                md = d.mean()
                verd = ("MODE WINS" if (md > 0 and p < 0.05) else
                        "mode ahead (n.s.)" if md > 0 else
                        "MODE LOSES" if p < 0.05 else "mode behind (n.s.)")
                if abs(md) < 1e-12:
                    verd = "identical (selector never deviates)"
                P(f"  {dial:8s} {mode_arm + ' - ' + sel_arm:28s} {md:+9.4f} {d.median():+9.4f} "
                  f"{tstat(d.values):+7.2f} {w:4d} {l:5d} {len(d)-w-l:4d} {p:7.4f}  {verd}")
                paired.append(dict(family="MODE_vs_SEL", score=scorenm, dial=dial,
                                   arm=mode_arm, ref=sel_arm, mean_d=md, median_d=d.median(),
                                   t=tstat(d.values), wins=w, losses=l, ties=len(d) - w - l,
                                   sign_p=p, n=len(d), verdict=verd))
        P("")

    # ---- the idea's count
    pdf = pd.DataFrame(paired)
    hl = pdf[(pdf.family == "MODE_vs_SEL") & (pdf.arm == "MODE-SHARPE-LOO")
             & (pdf.ref == "SEL-SHARPE") & (pdf.score == "OOS_Sharpe")]
    n_ahead = int((hl.mean_d > 0).sum())
    n_sig = int(((hl.mean_d > 0) & (hl.sign_p < 0.05)).sum())
    n_tied = int((hl.mean_d.abs() < 1e-12).sum())
    n_behind = int((hl.mean_d < 0).sum())
    P(f"  THE COUNT (headline arm MODE-SHARPE-LOO vs SEL-SHARPE, OOS Sharpe, 5 dials):")
    P(f"     mode ahead on {n_ahead}/5   (significant {n_sig}/5)   tied {n_tied}/5   selector ahead on {n_behind}/5")
    P(f"     dials where the mode wins significantly: "
      f"{', '.join(hl[(hl.mean_d>0)&(hl.sign_p<0.05)].dial) or '(none)'}")
    P(f"     dials where the selector is ahead:        "
      f"{', '.join(hl[hl.mean_d<0].dial) or '(none)'}")
    P("")

    # ---- MODE and SELECTOR vs the INCUMBENT (idea 171's table, extended)
    P("=" * 122)
    P("CONTEXT - every arm MINUS THE INCUMBENT CONSTANT (idea 171's table, with the mode arms added).")
    P("A mode arm that beats the selector but loses to the incumbent changes nothing for RULES.")
    P("")
    for scorenm in ["OOS_Sharpe", "OOS_margin"]:
        P(f"  --- OOS score = {scorenm} " + "-" * 88)
        P(f"  {'dial':8s} {'arm':16s} {'mean d':>9s} {'t':>7s} {'win':>4s} {'loss':>5s} {'tie':>4s} "
          f"{'sign p':>7s} {'changes':>8s}  verdict")
        for dial in DIAL_ORDER:
            const = DIALS[dial][1]
            base_s = ch[(ch.dial == dial) & (ch.arm == "CONST")].set_index("book")[scorenm]
            for arm in ARMS:
                if arm == "CONST":
                    continue
                a = ch[(ch.dial == dial) & (ch.arm == arm)].set_index("book")
                d = (a[scorenm] - base_s).reindex(base_s.index)
                p, w, l = sign_p(d.values)
                md = d.mean()
                nchg = int((a["point"] != const).sum())
                verd = ("BEATS CONST" if (md > 0 and p < 0.05) else
                        "ahead (n.s.)" if md > 0 else
                        "LOSES TO CONST" if p < 0.05 else "behind (n.s.)")
                if arm == "ORACLE":
                    verd = "(upper bound)"
                elif arm == "RANDOM":
                    verd = "(control) " + verd
                P(f"  {dial:8s} {arm:16s} {md:+9.4f} {tstat(d.values):+7.2f} {w:4d} {l:5d} "
                  f"{len(d)-w-l:4d} {p:7.4f} {nchg:4d}/{len(d)}  {verd}")
                paired.append(dict(family="ARM_vs_CONST", score=scorenm, dial=dial, arm=arm,
                                   ref="CONST", mean_d=md, median_d=d.median(), t=tstat(d.values),
                                   wins=w, losses=l, ties=len(d) - w - l, sign_p=p, n=len(d),
                                   n_changed=nchg, verdict=verd))
        P("")
    pd.DataFrame(paired).to_csv(OUT / f"{STEM}.paired.csv", index=False)

    # ---- P4's arithmetic: the whole gap lives on deviating books
    P("=" * 122)
    P("DECOMPOSITION - where the MODE-vs-SELECTOR gap comes from (OOS Sharpe, MODE-SHARPE-LOO).")
    P("On books where the selector agrees with its own LOO mode the paired difference is 0 by")
    P("construction, so the finding is entirely the size and sign of the DEVIATIONS.")
    P("")
    P("  Sign convention, stated once: d = MODE minus SELECTOR.  d > 0 means the selector's")
    P("  off-mode pick LOST to the mode (the deviation hurt); d < 0 means it paid off.")
    P("")
    P(f"  {'dial':8s} {'deviations':>11s} {'mean d (all)':>13s} {'mean d | deviating':>19s} "
      f"{'dev paid off':>13s} {'dev hurt':>9s} {'min d':>9s} {'max d':>9s}")
    dev_rows = []
    for dial in DIAL_ORDER:
        a = ch[(ch.dial == dial) & (ch.arm == "MODE-SHARPE-LOO")].set_index("book")
        b = ch[(ch.dial == dial) & (ch.arm == "SEL-SHARPE")].set_index("book")
        d = (a["OOS_Sharpe"] - b["OOS_Sharpe"]).reindex(b.index)
        devmask = (a["point"] != b["point"]).reindex(b.index)
        nd = int(devmask.sum())
        dd = d[devmask]
        P(f"  {dial:8s} {nd:8d}/{len(d)} {d.mean():+13.4f} "
          f"{(dd.mean() if nd else np.nan):+19.4f} {int((dd<0).sum()):13d} {int((dd>0).sum()):9d} "
          f"{(dd.min() if nd else np.nan):+9.4f} {(dd.max() if nd else np.nan):+9.4f}")
        for bkn in d.index[devmask]:
            dev_rows.append(dict(dial=dial, book=bkn, parent=a.loc[bkn, "parent"],
                                 sel_point=b.loc[bkn, "point"], mode_point=a.loc[bkn, "point"],
                                 sel_OOS_Sharpe=b.loc[bkn, "OOS_Sharpe"],
                                 mode_OOS_Sharpe=a.loc[bkn, "OOS_Sharpe"],
                                 d=float(d.loc[bkn])))
    dv = pd.DataFrame(dev_rows)
    dv.to_csv(OUT / f"{STEM}.deviations.csv", index=False)
    if len(dv):
        P("")
        P("  the 10 deviations that COST THE SELECTOR most (largest d = mode beat the off-mode pick):")
        P("    " + dv.sort_values("d", ascending=False).head(10)
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
        P("")
        P("  the 10 deviations that PAID OFF most for the selector (most negative d):")
        P("    " + dv.sort_values("d").head(10)
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    P("")

    # ---- per-family reading (books within a family are correlated draws)
    P("=" * 122)
    P("PER-FAMILY (the pooled t OVERSTATES: sub-panels of B136 are correlated draws, idea 175's")
    P("criticism of idea 171, applied here to this run).  MODE-SHARPE-LOO minus SEL-SHARPE, OOS Sharpe.")
    P("")
    P(f"  {'dial':8s} " + " ".join(f"{p:>22s}" for p in ["U56", "B136", "SMALL"]))
    for dial in DIAL_ORDER:
        cells = []
        for par in ["U56", "B136", "SMALL"]:
            a = ch[(ch.dial == dial) & (ch.arm == "MODE-SHARPE-LOO") & (ch.parent == par)].set_index("book")
            b = ch[(ch.dial == dial) & (ch.arm == "SEL-SHARPE") & (ch.parent == par)].set_index("book")
            d = (a["OOS_Sharpe"] - b["OOS_Sharpe"]).reindex(b.index)
            t = tstat(d.values)
            cells.append(f"{d.mean():+.4f} (n{len(d)}, t{t:+.2f})" if len(d) else "n/a")
        P(f"  {dial:8s} " + " ".join(f"{c:>22s}" for c in cells))
    P("")

    # ---- rule 8 walk-forward
    P("=" * 122)
    P("PROTOCOL RULE 8 WALK-FORWARD.  Every arm above chose on IS only; OOS is read once, here.")
    P("(i) mean OOS metrics across the 53 books, per dial and arm")
    P(f"  {'dial':8s} {'arm':16s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} {'OOS MaxDD':>10s} "
      f"{'OOS margin':>11s} {'OOS-4b pass':>12s}")
    wf = []
    for dial in DIAL_ORDER:
        for arm in ARMS:
            a = ch[(ch.dial == dial) & (ch.arm == arm)]
            npass = int((a["OOS_margin"] > 0).sum())
            P(f"  {dial:8s} {arm:16s} {a.OOS_CAGR.mean():9.2%} {a.OOS_Sharpe.mean():9.3f} "
              f"{a.OOS_MaxDD.mean():10.2%} {a.OOS_margin.mean():+11.4f} {npass:6d}/{len(a)}")
            wf.append(dict(kind="mean_over_books", dial=dial, arm=arm, OOS_CAGR=a.OOS_CAGR.mean(),
                           OOS_Sharpe=a.OOS_Sharpe.mean(), OOS_MaxDD=a.OOS_MaxDD.mean(),
                           OOS_margin=a.OOS_margin.mean(), oos4b_pass=npass, n=len(a)))
    P("")
    P("  pooled over the five dials (the single number for 'fit' vs 'write the mode down' vs 'do nothing'):")
    for arm in ARMS:
        a = ch[ch.arm == arm]
        P(f"    {arm:16s} OOS CAGR {a.OOS_CAGR.mean():7.2%}  OOS Sharpe {a.OOS_Sharpe.mean():.4f}  "
          f"OOS MaxDD {a.OOS_MaxDD.mean():7.2%}")
        wf.append(dict(kind="pooled", dial="ALL", arm=arm, OOS_CAGR=a.OOS_CAGR.mean(),
                       OOS_Sharpe=a.OOS_Sharpe.mean(), OOS_MaxDD=a.OOS_MaxDD.mean(),
                       OOS_margin=a.OOS_margin.mean(), oos4b_pass=int((a.OOS_margin > 0).sum()), n=len(a)))
    for k in SPY:
        so, bo = SPY[k].loc[OOS_START:], BASE[k].loc[OOS_START:]
        ms, mb = metrics(so), metrics(bo)
        P(f"    {'SPY/'+k:16s} OOS CAGR {ms['CAGR']:7.2%}  OOS Sharpe {ms['Sharpe']:.4f}  OOS MaxDD {ms['MaxDD']:7.2%}")
        P(f"    {'RULESv1/'+k:16s} OOS CAGR {mb['CAGR']:7.2%}  OOS Sharpe {mb['Sharpe']:.4f}  OOS MaxDD {mb['MaxDD']:7.2%}")
        wf.append(dict(kind="benchmark", dial="-", arm=f"SPY/{k}", OOS_CAGR=ms["CAGR"],
                       OOS_Sharpe=ms["Sharpe"], OOS_MaxDD=ms["MaxDD"]))
        wf.append(dict(kind="benchmark", dial="-", arm=f"RULESv1/{k}", OOS_CAGR=mb["CAGR"],
                       OOS_Sharpe=mb["Sharpe"], OOS_MaxDD=mb["MaxDD"]))
    P("")
    P("(ii) the classic S1 pick: within each dial+arm, the single book with the best IS Sharpe, read once on OOS")
    P(f"  {'dial':8s} {'arm':16s} {'book':11s} {'point':>6s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} "
      f"{'OOS MaxDD':>10s}  vs SPY / RULES v1 (same parent)")
    for dial in DIAL_ORDER:
        for arm in ARMS:
            a = ch[(ch.dial == dial) & (ch.arm == arm)]
            r = a.loc[a["IS_Sharpe"].idxmax()]
            par = r.parent
            ms, mb = metrics(SPY[par].loc[OOS_START:]), metrics(BASE[par].loc[OOS_START:])
            P(f"  {dial:8s} {arm:16s} {r.book:11s} {str(r.point):>6s} {r.OOS_CAGR:9.2%} "
              f"{r.OOS_Sharpe:9.3f} {r.OOS_MaxDD:10.2%}   SPY {ms['Sharpe']:.3f} / v1 {mb['Sharpe']:.3f}"
              f"   {'beats both' if r.OOS_Sharpe > max(ms['Sharpe'], mb['Sharpe']) else 'does not beat both'}")
            wf.append(dict(kind="S1_pick", dial=dial, arm=arm, book=r.book, point=r.point,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           spy_OOS_Sharpe=ms["Sharpe"], v1_OOS_Sharpe=mb["Sharpe"]))
    pd.DataFrame(wf).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("")

    # ---- both KEEP paths
    P("=" * 122)
    P(f"BOTH KEEP PATHS (PROTOCOL rule 4), evaluated exactly on all {len(lad)} ladder rows")
    n4a = int((lad.fail4a == "-").sum())
    n4b = int((lad.fail4b == "-").sum())
    P(f"  4a (beat the book):  {n4a}/{len(lad)} rows pass")
    P(f"  4b (capital-worthy): {n4b}/{len(lad)} rows pass "
      f"({int(((lad.fail4b=='-') & lad.book.str.startswith('B136k')).sum())} of them on sub-panels, "
      f"which are a corpus device and NOT tradable books)")
    bars = pd.Series([b for s in lad.fail4b for b in s.split(",") if b != "-"]).value_counts()
    P(f"  4b binding bars across all failing rows: {dict(bars)}")
    kfixed = lad[(lad.fail4b == "-") & (~lad.book.str.startswith("B136k"))]
    if len(kfixed):
        P("  4b-passing rows on the FIXED (tradable) panels:")
        P("    " + kfixed[["book", "dial", "point", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                           "OOS_CAGR", "OOS_MaxDD", "turnover"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n    "))
        P("  NOTE (idea 144): every one is a re-parameterisation of an EXISTING book, not a new")
        P("  signal.  None is proposed.  This run is a methodology test.")
    else:
        P("  no fixed-panel row passes 4b.")
    P("")
    P("  do any of the ARMS land on a 4b pass?  (arm-level, fixed panels only)")
    for arm in ARMS:
        a = ch[(ch.arm == arm) & (~ch.book.str.startswith("B136k"))]
        P(f"    {arm:16s} {int((a.fail4b=='-').sum()):2d}/{len(a)} arm-cells pass 4b")
    lad[["book", "dial", "point", "fail4a", "fail4b", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
         "OOS_Sharpe"]].to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("")

    # ---- named-book view for a Sunday review
    P("=" * 122)
    P("NAMED-BOOK VIEW (post-hoc).  U56 is the live book's panel.  What would 'write the mode down'")
    P("actually write, dial by dial, and what did it earn there?")
    P("")
    for bkname in ["U56"]:
        par = next(b.parent for b in books if b.name == bkname)
        ms, mb = metrics(SPY[par]), metrics(BASE[par])
        s1b, s2b = halves(SPY[par])
        mso = metrics(SPY[par].loc[OOS_START:])
        P(f"  SPY(full) CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} halves {s1b:.3f}/{s2b:.3f} "
          f"MaxDD {ms['MaxDD']:.2%} -> 4b bars: H1>{s1b:.3f} H2>{s2b:.3f} OOS>{mso['Sharpe']:.3f} "
          f"|DD|<={DELTA*abs(ms['MaxDD']):.2%} CAGR>={PHI*ms['CAGR']:.2%}")
        P(f"  RULES v1(full) Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:.2%}")
        for dial in DIAL_ORDER:
            pk = ch[(ch.dial == dial) & (ch.book == bkname)].set_index("arm")["point"]
            P(f"    {dial}: incumbent {INC[dial]} | SEL-SHARPE {pk['SEL-SHARPE']} | "
              f"MODE-LOO {pk['MODE-SHARPE-LOO']} | oracle {pk['ORACLE']}")
            d = lad[(lad.book == bkname) & (lad.dial == dial)]
            P("      " + d[["point", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR",
                            "OOS_MaxDD", "turnover", "fail4a", "fail4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n      "))
        P("")

    # ---- predictions scorecard
    P("=" * 122)
    P("PREDICTIONS SCORECARD (all written before any number above was read)")
    dev_by_dial = {d: int((ch[(ch.dial == d) & (ch.arm == "MODE-SHARPE-LOO")].set_index("book")["point"]
                           != ch[(ch.dial == d) & (ch.arm == "SEL-SHARPE")].set_index("book")["point"]).sum())
                   for d in DIAL_ORDER}
    p3_ok = all(abs(hl[hl.dial == d].mean_d.iloc[0]) < 0.01 for d in ["GROSS", "SLEEVE"])
    agree_zero = True
    for dial in DIAL_ORDER:
        a = ch[(ch.dial == dial) & (ch.arm == "MODE-SHARPE-LOO")].set_index("book")
        b = ch[(ch.dial == dial) & (ch.arm == "SEL-SHARPE")].set_index("book")
        same = (a["point"] == b["point"])
        agree_zero &= bool(((a["OOS_Sharpe"] - b["OOS_Sharpe"])[same].abs() < 1e-12).all())
    ic_loo = max(abs(pdf[(pdf.arm == "MODE-SHARPE-IC") & (pdf.score == "OOS_Sharpe")
                         & (pdf.family == "MODE_vs_SEL")].mean_d.values
                     - hl.mean_d.values))
    mode_vs_const = pd.DataFrame(paired)
    mvc = mode_vs_const[(mode_vs_const.family == "ARM_vs_CONST") & (mode_vs_const.arm == "MODE-SHARPE-LOO")
                        & (mode_vs_const.score == "OOS_Sharpe")]
    P(f"  P1 reproduction [a]+[b]+[c]                 : {'HIT' if (okA and okB and okC) else 'MISS'}")
    P(f"  P2 mode beats selector on >= 4 of 5 dials    : {'HIT' if n_ahead >= 4 else 'MISS'}"
      f"  (ahead on {n_ahead}/5, tied {n_tied}/5, behind {n_behind}/5)")
    P(f"  P3 |mean d| < 0.01 on GROSS and SLEEVE       : {'HIT' if p3_ok else 'MISS'}"
      f"  (GROSS {hl[hl.dial=='GROSS'].mean_d.iloc[0]:+.4f}, SLEEVE {hl[hl.dial=='SLEEVE'].mean_d.iloc[0]:+.4f})")
    P(f"  P4 agreeing books contribute exactly 0       : {'HIT' if agree_zero else 'MISS'}"
      f"   (deviation counts: {dev_by_dial})")
    P(f"  P5 mode does NOT beat the incumbent on all 5 : "
      f"{'HIT' if int((mvc.mean_d > 0).sum()) < 5 else 'MISS'}"
      f"  (mode beats CONST on {int((mvc.mean_d>0).sum())}/5)")
    P(f"  P6 |MODE-IC - MODE-LOO| < 0.01 Sharpe        : {'HIT' if ic_loo < 0.01 else 'MISS'}"
      f"  (max over dials {ic_loo:.4f})")
    P(f"  P7 no new 4b KEEP                            : {'HIT' if len(kfixed)==0 else 'see note'}"
      f"  ({n4b} of {len(lad)} rows pass 4b; {len(kfixed)} on fixed panels, all re-parameterisations)")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
