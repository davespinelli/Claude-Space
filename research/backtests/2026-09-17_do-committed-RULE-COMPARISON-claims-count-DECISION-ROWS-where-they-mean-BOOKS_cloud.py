#!/usr/bin/env python3
"""
Idea 1211 (cloud lane, 2026-09-17) — do any committed RULE-COMPARISON claims in the record count
DECISION ROWS where they mean BOOKS?

THE PREMISE, READ FROM THE RECORD.  Idea 1210 found that 1154's 4b counts of 6 / 19 / 24 are
DECISION ROWS and collapse to 3 / 2 / 2 DISTINCT BOOKS, because a rule that DECLINES TO MOVE
reselects the same anchor book at all 12 (ladder, chooser) decisions of a (panel, anchor) cell —
an inflation factor of 12 that lands ENTIRELY on the rules that decline to move.  Every
committed sentence of the form "rule A finds N more capital-worthy books than rule B" is
therefore a comparison of two numbers that may be counting different things, and the rule that
does the LEAST is the one that inflates the MOST.

THIS RUN HARVESTS THOSE SENTENCES, RE-COUNTS THEM IN DISTINCT BOOKS, AND PRICES THE INFLATION
ON A LIVE GRID.

  ARM 1 THE CENSUS.  Every committed rule-comparison / capital-worthy-count sentence in the
  record's own text is harvested and classified for whether it STATES its counting basis (rows
  or books).  Reported at every (claim class x book identity) cell.

  ARM 2 THE PRICE.  The inflation is not asserted from the text — it is MEASURED.  A 1154-shaped
  decision grid is rebuilt on the live tape (3 panels x 4 ladders x 4 choosers = 48 rule-8
  decision rows), 4b and 4a passes are counted BOTH WAYS at every book-identity definition, and
  the per-rule inflation factor is published.  Then the question the queue actually asks — "how
  many verdicts change sign or size" — is answered by re-ranking every PAIR of rules on rows and
  on books and counting the pairs whose verdict flips.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  DIAL 1  CLAIM SET       R_EXPLICIT  units with a comparative ("more ... than", "against",
                                      "vs") AND a capital-worthy / 4a / 4b / pass count
                          R_PASSCOUNT units with a 4a / 4b / KEEP pass count in "k of m" form
                                      (the comparison against the anchor is implicit)
                          C_ALL       the union
  DIAL 2  BOOK IDENTITY   B_ROW       no collapse at all — the record's habit (control)
                          B_KEY       collapse on the (panel, N, H, GROSS, CADENCE) dial key
                          B_VALUE     collapse on the realised return vector, bit-identical
                                      (1194 / 1230's key)
                          B_VALUE_RD  collapse on the realised return vector rounded to 1e-9,
                                      so books that differ only in float noise are one book

  12 census cells and 16 price cells (4 identities x 4 choosers), EVERY ONE PUBLISHED.

NOT DIALS, REPORTED AT EVERY VALUE AND NEVER SELECTED ON: PANEL {U56, B136, SMALL} (rule 9);
LADDER {N, H, GROSS, CADENCE}; the four choosers CH_ARGMAX / CH_RUNNERUP / CH_MEDIAN /
CH_ANCHOR (the one that declines to move).

PRE-DECLARED OUTCOMES, fixed before any count is read:
  (A) THE RECORD MEANS BOOKS — the inflation factor is ~1 and the row count was never wrong.
  (B) IT MEANS ROWS, AND THE VERDICTS SURVIVE — inflation is large but every rule inflates
      alike, so the RANKING of rules on rows equals the ranking on books and no verdict flips.
  (C) IT MEANS ROWS, AND THE VERDICTS DO NOT SURVIVE — inflation is concentrated on the rules
      that decline to move, and at least one committed-shaped "A beats B" pair changes sign.

Frozen at the record's construction, inherited from 1205/1207/1214/1217/1223/1226/1227/1231
unchanged: 3-leg composite (21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor
N = 20 / H = 126 / GROSS = 0.75 / CADENCE = W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1
(lag = 1), warm-up 260 rows, 1230's VALUE-based definition of a move.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with the chooser and the rung chosen
on the pre-2017 window ONLY and 2017-2026 read once; BOTH KEEP paths on every rung book and
every decision row; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_do-committed-RULE-COMPARISON-claims-count-DECISION-ROWS-where-they-mean-BOOKS_cloud.py
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
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "do-committed-RULE-COMPARISON-claims-count-DECISION-ROWS-where-they-mean-BOOKS"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
ANCHOR_KEY = ("CADENCE", "W")

LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00],
    "CADENCE": ["W", "M"],
}
LADDERS = ["N", "H", "GROSS", "CADENCE"]
CHOOSERS = ["CH_ARGMAX", "CH_RUNNERUP", "CH_MEDIAN", "CH_ANCHOR"]
IDENTS = ["B_ROW", "B_KEY", "B_VALUE", "B_VALUE_RD"]
CLASSES = ["R_EXPLICIT", "R_PASSCOUNT", "C_ALL"]

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))


# ============================================================ ARM 1 — the census of claims
SRC_TEXT = ["research/LEADERBOARD.md", "research/CHANGELOG.md", "research/QUEUE.md"]
_SENT = re.compile(r"(?<=[.;:!?])\s+|\n|\s\|\s|\s+—\s+")

CAPITAL = re.compile(r"\b(4a|4b|KEEP|capital-worthy|capital worthy|pass(es|ed|ing)?)\b", re.I)
COUNT = re.compile(r"(?<![\d.])(\d[\d,]*)\s+of\s+(\d[\d,]*)(?![\d.])|(?<![\d.])(\d[\d,]*)\s+"
                   r"(distinct\s+)?(books?|rows?|curves?|cells?|decisions?)\b", re.I)
COMPARATIVE = re.compile(r"\b(more\s+\w+\s+than|fewer\s+\w+\s+than|beats?|against|versus|vs\.?|"
                         r"outperform\w*|better than|worse than)\b", re.I)
# does the unit SAY what it is counting?
STATES_ROWS = re.compile(r"\b(rows?|decision rows?|rule-8 rows?|pick rows?)\b", re.I)
STATES_BOOKS = re.compile(r"\b(distinct\s+books?|books?)\b", re.I)
STATES_COLLAPSE = re.compile(r"\b(collaps\w+|distinct|de-?dup\w*|unique|bit-identical|"
                             r"same book|one book)\b", re.I)


def units_from(text: str):
    return [u.strip() for u in _SENT.split(text) if len(u.strip()) >= 25]


def harvest():
    srcs = []
    for rel in SRC_TEXT:
        p = ROOT / rel
        if p.exists():
            srcs.append((rel, p.read_text(errors="ignore")))
    for p in sorted(BT.glob("*.md")):
        srcs.append((f"research/backtests/{p.name}", p.read_text(errors="ignore")))
    n_py = 0
    for p in sorted(BT.glob("*.py")):
        if p.name.startswith(f"{DATE}_{SLUG}"):
            continue                       # never census this run's own uncommitted source
        n_py += 1
        srcs.append((f"research/backtests/{p.name}", p.read_text(errors="ignore")))
    rows = []
    for rel, text in srcs:
        for u in units_from(text):
            if not CAPITAL.search(u) or not COUNT.search(u):
                continue
            comp = bool(COMPARATIVE.search(u))
            cls = "R_EXPLICIT" if comp else "R_PASSCOUNT"
            rows.append(dict(source=rel, cls=cls, comparative=comp,
                             states_rows=bool(STATES_ROWS.search(u)),
                             states_books=bool(STATES_BOOKS.search(u)),
                             states_collapse=bool(STATES_COLLAPSE.search(u)),
                             states_basis=bool(STATES_COLLAPSE.search(u))
                             or (bool(STATES_ROWS.search(u)) and bool(STATES_BOOKS.search(u))),
                             unit=u[:400]))
    return pd.DataFrame(rows), len(srcs), n_py


def census_grid(df):
    """The census leg of DIAL 2: what a unit would have to SAY for each identity to be
    recoverable from the text alone."""
    need = {"B_ROW": lambda r: True,                       # the habit needs no statement
            "B_KEY": lambda r: r.states_books,
            "B_VALUE": lambda r: r.states_collapse,
            "B_VALUE_RD": lambda r: r.states_collapse}
    out = []
    for cls in CLASSES:
        sub = df if cls == "C_ALL" else df[df.cls.eq(cls)]
        for ident in IDENTS:
            hit = int(sub.apply(need[ident], axis=1).sum()) if len(sub) else 0
            out.append(dict(claim_class=cls, book_identity=ident, n_units=len(sub),
                            n_recoverable=hit,
                            frac=(hit / len(sub) if len(sub) else np.nan)))
    return pd.DataFrame(out)


# ==================================================================== ARM 2 — panels and books
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, N, H, freq, lag=1):
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, freq):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def bmrow(r):
    h1, h2 = halves(r)
    d = triple(r)
    d.update(H1=h1, H2=h2)
    return d


def book_id(panel, key, r, ident):
    """The four DIAL-2 definitions of 'the same book'."""
    if ident == "B_ROW":
        return (panel, key, id(r))                     # never collapses: every row is its own
    if ident == "B_KEY":
        return (panel, key)
    if ident == "B_VALUE":
        return (panel, r.tobytes())
    return (panel, np.round(r, 9).tobytes())           # B_VALUE_RD


def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1211 (cloud lane, 2026-09-17) — do any committed RULE-COMPARISON claims count")
    say("DECISION ROWS where they mean BOOKS?")
    say("=" * 108)
    say("")
    say(f"  DIAL 1 CLAIM SET      {CLASSES}")
    say(f"  DIAL 2 BOOK IDENTITY  {IDENTS}")
    say(f"  RULES COMPARED (not a dial, all reported): {CHOOSERS}")
    say("")
    say("  PRE-DECLARED OUTCOMES, fixed before any count is read:")
    say("    (A) THE RECORD MEANS BOOKS — inflation ~1, the row count was never wrong.")
    say("    (B) IT MEANS ROWS, AND THE VERDICTS SURVIVE — inflation is large but uniform, so")
    say("        the ranking of rules on rows equals the ranking on books.")
    say("    (C) IT MEANS ROWS, AND THE VERDICTS DO NOT SURVIVE — inflation concentrates on the")
    say("        rules that decline to move and at least one A-beats-B pair changes sign.")

    # ================================================================ ARM 1
    say("")
    say("=" * 108)
    say("ARM 1 — THE CENSUS.  EVERY COMMITTED RULE-COMPARISON / CAPITAL-COUNT SENTENCE")
    say("=" * 108)
    df, n_src, n_py = harvest()
    df.to_csv(f"{OUT}.census.csv", index=False)
    grid = census_grid(df)
    grid.to_csv(f"{OUT}.census_grid.csv", index=False)
    say("")
    say("  THE TREE THIS RUN READ, STATED SO THESE FIGURES ARE PINNED (1231's repair, carried):")
    say(f"    sources scanned {n_src}  ({n_py} committed .py, this run's own source EXCLUDED); "
        f"{len(list(BT.glob('*.py')))} .py on disk, "
        f"{sum(1 for l in (ROOT/'research'/'LEADERBOARD.md').read_text(errors='ignore').splitlines() if l.startswith('| 20'))}"
        " LEADERBOARD rows.")
    say("")
    say(f"  HARVEST: {len(df)} capital-count sentences "
        f"(R_EXPLICIT {int(df.cls.eq('R_EXPLICIT').sum())} carry a comparative, "
        f"R_PASSCOUNT {int(df.cls.eq('R_PASSCOUNT').sum())} do not).")
    say("")
    say("  THE 12-CELL GRID (claim class x book identity): how many units SAY enough for that")
    say("  identity to be recovered from the committed text alone.")
    say(f"    {'class':12s} {'identity':11s} {'n_units':>8s} {'recoverable':>12s} {'frac':>8s}")
    for _, r in grid.iterrows():
        say(f"    {r.claim_class:12s} {r.book_identity:11s} {r.n_units:8d} "
            f"{r.n_recoverable:12d} {r.frac:8.4f}")
    say("")
    say(f"  HEADLINE: {int(df.states_basis.sum())} of {len(df)} committed capital-count "
        f"sentences state their counting basis = {df.states_basis.mean():.4f}.")
    say(f"            {int(df.states_collapse.sum())} of {len(df)} say anything about "
        f"collapsing / distinctness at all = {df.states_collapse.mean():.4f}.")
    say(f"            {int(df.comparative.sum())} of {len(df)} are explicit A-vs-B comparisons.")
    gate("G1 census non-empty", len(df), 100, len(df) >= 100)
    gate("G2 census grid has 12 cells", len(grid), 12, len(grid) == 12)

    # ================================================================ ARM 2
    say("")
    say("=" * 108)
    say("ARM 2 — THE PRICE.  THE INFLATION MEASURED ON A LIVE 1154-SHAPED DECISION GRID")
    say("=" * 108)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv").set_index("ticker")["max_1d_move"]
    inv = [c for c in pxS.columns if c != "SPY" and float(meta.get(c, np.inf)) < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0 per data/small_meta.csv),"
        " SPY benchmark only (not a constituent).")

    booked, bench = {}, {}
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
        af = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            books[("CADENCE", f)] = nrun(pan, A_G * (af if f == "W" else frames[(A_N, A_H, "M")]),
                                         f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * af, "W")
        booked[pan.name] = books
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books.")

    ident0 = 0.0
    for pan in panels:
        bk = booked[pan.name]
        for k in (("N", A_N), ("H", A_H), ("GROSS", A_G)):
            ident0 = max(ident0, float(np.nanmax(np.abs(bk[k] - bk[ANCHOR_KEY]))))
    gate("G3 the anchor is one book under four names", ident0, 1e-15, ident0 <= 1e-15)

    BM = {}
    for pan in panels:
        o = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            BM[(pan.name, nm, False)] = bmrow(r[pan.i0:])
            BM[(pan.name, nm, True)] = bmrow(r[o:])
    say("")
    say("  BENCHMARKS (full from warm-up / OOS 2017-2026):")
    for pan in panels:
        for nm in ("SPY", "LIVE"):
            f_, o_ = BM[(pan.name, nm, False)], BM[(pan.name, nm, True)]
            say(f"    {pan.name:6s} {nm:5s} full {f_['CAGR']:7.2%} / {f_['Sharpe']:6.4f} /"
                f" {f_['MaxDD']:7.2%}   OOS {o_['CAGR']:7.2%} / {o_['Sharpe']:6.4f} /"
                f" {o_['MaxDD']:7.2%}")

    # ---- every rung book, both KEEP paths, full and OOS
    brows = []
    for pan in panels:
        o = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for k, r in booked[pan.name].items():
            rf, ro = r[pan.i0:], r[o:]
            k4a, k4b, m_, h1, h2 = keep_paths(rf, BM[(pan.name, "SPY", False)],
                                              BM[(pan.name, "LIVE", False)])
            k4ao, k4bo, mo, _, _ = keep_paths(ro, BM[(pan.name, "SPY", True)],
                                              BM[(pan.name, "LIVE", True)])
            brows.append(dict(panel=pan.name, ladder=k[0], rung=k[1],
                              CAGR=m_["CAGR"], Sharpe=m_["Sharpe"], MaxDD=m_["MaxDD"],
                              H1=h1, H2=h2, keep4a=k4a, keep4b=k4b,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], OOS_keep4a=k4ao, OOS_keep4b=k4bo))
    bdf = pd.DataFrame(brows)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    say("")
    say(f"  RUNG BOOKS: {len(bdf)} rows.  KEEP 4a full {int(bdf.keep4a.sum())} / OOS "
        f"{int(bdf.OOS_keep4a.sum())}.  KEEP 4b full {int(bdf.keep4b.sum())} / OOS "
        f"{int(bdf.OOS_keep4b.sum())} / BOTH {int((bdf.keep4b & bdf.OOS_keep4b).sum())}.")

    # ---- the 1154-shaped decision grid, rule 8: chosen on pre-2017 only
    say("")
    say("  THE DECISION GRID (rule 8): for each (panel, ladder, chooser) the rung is chosen on")
    say("  the PRE-2017 window ONLY and 2017-2026 is read once.  Each cell is ONE DECISION ROW,")
    say("  and its destination is ONE BOOK — the two need not be the same count.")
    drows = []
    for pan in panels:
        o = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for lad in LADDERS:
            rungs = LAD[lad]
            iss = {rg: sharpe(booked[pan.name][(lad, rg)][pan.i0:o]) for rg in rungs}
            order = sorted(rungs, key=lambda rg: (-iss[rg] if np.isfinite(iss[rg]) else 1e9))
            anchor_rung = {"N": A_N, "H": A_H, "GROSS": A_G, "CADENCE": A_C}[lad]
            for ch in CHOOSERS:
                if ch == "CH_ARGMAX":
                    pick = order[0]
                elif ch == "CH_RUNNERUP":
                    pick = order[1] if len(order) > 1 else order[0]
                elif ch == "CH_MEDIAN":
                    pick = order[len(order) // 2]
                else:
                    pick = anchor_rung
                key = (lad, pick)
                r = booked[pan.name][key]
                ro = r[o:]
                k4ao, k4bo, mo, h1o, h2o = keep_paths(ro, BM[(pan.name, "SPY", True)],
                                                      BM[(pan.name, "LIVE", True)])
                rf = r[pan.i0:]
                k4a, k4b, m_, _, _ = keep_paths(rf, BM[(pan.name, "SPY", False)],
                                                BM[(pan.name, "LIVE", False)])
                drows.append(dict(panel=pan.name, ladder=lad, chooser=ch, pick=pick,
                                  moved_value=bool(float(np.nanmax(np.abs(
                                      r - booked[pan.name][ANCHOR_KEY]))) > 1e-15),
                                  IS_Sharpe=iss[pick],
                                  CAGR=m_["CAGR"], Sharpe=m_["Sharpe"], MaxDD=m_["MaxDD"],
                                  keep4a=k4a, keep4b=k4b,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], OOS_H1=h1o, OOS_H2=h2o,
                                  OOS_keep4a=k4ao, OOS_keep4b=k4bo,
                                  _bytes=r[pan.i0:].tobytes(),
                                  _bytes_rd=np.round(r[pan.i0:], 9).tobytes()))
    ddf = pd.DataFrame(drows)
    ddf.drop(columns=["_bytes", "_bytes_rd"]).to_csv(f"{OUT}.decisions.csv", index=False)
    say("")
    say(f"    {len(ddf)} decision rows = {len(panels)} panels x {len(LADDERS)} ladders x "
        f"{len(CHOOSERS)} choosers.")
    say(f"    {'panel':6s} {'ladder':8s} {'chooser':12s} {'pick':>6s} {'moved':>6s} "
        f"{'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s} {'4a':>3s} {'4b':>3s}")
    for _, r in ddf.iterrows():
        say(f"    {r.panel:6s} {r.ladder:8s} {r.chooser:12s} {str(r.pick):>6s} "
            f"{str(r.moved_value):>6s} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:11.4f} "
            f"{r.OOS_MaxDD:10.2%} {int(r.OOS_keep4a):3d} {int(r.OOS_keep4b):3d}")

    # ---- THE COUNT, BOTH WAYS, AT EVERY IDENTITY x EVERY CHOOSER
    say("")
    say("  (2a) THE 16-CELL PRICE GRID — 4b PASSES COUNTED AS ROWS AND AS DISTINCT BOOKS")
    say("       at every book identity, for every rule.  INFLATION = rows / distinct books.")
    cnt = []
    for ch in CHOOSERS:
        sub = ddf[ddf.chooser.eq(ch)]
        for ident in IDENTS:
            for leg, col in (("4b", "OOS_keep4b"), ("4a", "OOS_keep4a")):
                p = sub[sub[col]]
                if ident == "B_ROW":
                    nd = len(p)
                elif ident == "B_KEY":
                    nd = len(set(zip(p.panel, p.ladder, p.pick)))
                elif ident == "B_VALUE":
                    nd = len(set(zip(p.panel, p._bytes)))
                else:
                    nd = len(set(zip(p.panel, p._bytes_rd)))
                cnt.append(dict(chooser=ch, identity=ident, leg=leg, rows=len(p),
                                distinct=nd,
                                inflation=(len(p) / nd if nd else np.nan)))
    cdf = pd.DataFrame(cnt)
    cdf.to_csv(f"{OUT}.counts.csv", index=False)
    say("")
    say(f"    {'chooser':12s} {'identity':11s} {'4b rows':>8s} {'4b books':>9s} "
        f"{'inflation':>10s} {'4a rows':>8s} {'4a books':>9s}")
    for ch in CHOOSERS:
        for ident in IDENTS:
            b4 = cdf[(cdf.chooser == ch) & (cdf.identity == ident) & (cdf.leg == "4b")].iloc[0]
            a4 = cdf[(cdf.chooser == ch) & (cdf.identity == ident) & (cdf.leg == "4a")].iloc[0]
            say(f"    {ch:12s} {ident:11s} {int(b4.rows):8d} {int(b4.distinct):9d} "
                f"{b4.inflation if np.isfinite(b4.inflation) else float('nan'):10.2f} "
                f"{int(a4.rows):8d} {int(a4.distinct):9d}")

    # the whole grid, all choosers pooled (the shape 1210 measured)
    allp = ddf[ddf.OOS_keep4b]
    pooled = {"B_ROW": len(allp),
              "B_KEY": len(set(zip(allp.panel, allp.ladder, allp.pick))),
              "B_VALUE": len(set(zip(allp.panel, allp._bytes))),
              "B_VALUE_RD": len(set(zip(allp.panel, allp._bytes_rd)))}
    say("")
    say("    POOLED OVER ALL FOUR RULES (the shape 1210 measured on 1154): "
        + ", ".join(f"{k} {v}" for k, v in pooled.items())
        + f"   inflation {pooled['B_ROW'] / max(pooled['B_VALUE'], 1):.2f}x")

    # ---- (2b) DO THE VERDICTS CHANGE SIGN OR SIZE?
    say("")
    say("  (2b) THE QUEUE'S ACTUAL QUESTION — how many A-BEATS-B verdicts change sign or size")
    say("       when the same pair is re-counted in DISTINCT BOOKS instead of DECISION ROWS?")
    vrows = []
    for i, A in enumerate(CHOOSERS):
        for B in CHOOSERS[i + 1:]:
            for ident in IDENTS:
                if ident == "B_ROW":
                    continue
                ra = int(cdf[(cdf.chooser == A) & (cdf.identity == "B_ROW")
                             & (cdf.leg == "4b")].iloc[0].rows)
                rb = int(cdf[(cdf.chooser == B) & (cdf.identity == "B_ROW")
                             & (cdf.leg == "4b")].iloc[0].rows)
                da = int(cdf[(cdf.chooser == A) & (cdf.identity == ident)
                             & (cdf.leg == "4b")].iloc[0].distinct)
                db = int(cdf[(cdf.chooser == B) & (cdf.identity == ident)
                             & (cdf.leg == "4b")].iloc[0].distinct)
                sr = int(np.sign(ra - rb))
                sd = int(np.sign(da - db))
                vrows.append(dict(A=A, B=B, identity=ident, rows_A=ra, rows_B=rb,
                                  books_A=da, books_B=db, sign_rows=sr, sign_books=sd,
                                  flips=bool(sr != sd),
                                  size_rows=ra - rb, size_books=da - db,
                                  size_changes=bool((ra - rb) != (da - db))))
    vdf = pd.DataFrame(vrows)
    vdf.to_csv(f"{OUT}.verdicts.csv", index=False)
    say("")
    say(f"    {'A':12s} {'B':12s} {'identity':11s} {'rows A-B':>9s} {'books A-B':>10s} "
        f"{'sign flips':>11s} {'size changes':>13s}")
    for _, r in vdf.iterrows():
        say(f"    {r.A:12s} {r.B:12s} {r.identity:11s} {r.size_rows:+9d} {r.size_books:+10d} "
            f"{str(r.flips):>11s} {str(r.size_changes):>13s}")
    say("")
    say(f"    OF {len(vdf)} (pair x identity) VERDICTS: {int(vdf.flips.sum())} CHANGE SIGN, "
        f"{int(vdf.size_changes.sum())} CHANGE SIZE.")
    gate("G4 verdict pairs enumerated", len(vdf), 18, len(vdf) == 18)

    # ---- where the inflation lands: the move rate per rule
    say("")
    say("  (2c) WHERE THE INFLATION LANDS — 1210's claim is that it is concentrated on the")
    say("       rules that DECLINE TO MOVE.  Move rate and inflation, per rule:")
    say(f"    {'chooser':12s} {'move rate':>10s} {'4b rows':>8s} {'4b books (B_VALUE)':>19s} "
        f"{'inflation':>10s}")
    infl = {}
    for ch in CHOOSERS:
        sub = ddf[ddf.chooser.eq(ch)]
        b4 = cdf[(cdf.chooser == ch) & (cdf.identity == "B_VALUE") & (cdf.leg == "4b")].iloc[0]
        infl[ch] = b4.inflation
        say(f"    {ch:12s} {sub.moved_value.mean():10.4f} {int(b4.rows):8d} "
            f"{int(b4.distinct):19d} "
            f"{b4.inflation if np.isfinite(b4.inflation) else float('nan'):10.2f}")
    mr = ddf.groupby("chooser").moved_value.mean()
    fin = {k: v for k, v in infl.items() if np.isfinite(v)}
    if len(fin) >= 2:
        xs = np.array([mr[k] for k in fin])
        ys = np.array([fin[k] for k in fin])
        rho = float(np.corrcoef(xs, ys)[0, 1]) if xs.std() > 0 and ys.std() > 0 else np.nan
        say(f"    Pearson(move rate, inflation) over the {len(fin)} rules with a finite "
            f"inflation = {rho:+.4f}.")

    # ---- the 4b passes themselves
    say("")
    say("  THE 4b PASSES, NAMED — so the reader can check the collapse rather than trust it:")
    seen = {}
    for _, r in ddf[ddf.OOS_keep4b].iterrows():
        k = (r.panel, r._bytes)
        seen.setdefault(k, []).append(f"{r.ladder}={r.pick}/{r.chooser}")
    for (pan_, _), names in seen.items():
        ex = ddf[(ddf.panel == pan_) & (ddf.OOS_keep4b)].iloc[0]
        say(f"    {pan_:6s} reached {len(names):2d} times as: " + ", ".join(names))
    say(f"    -> {len(ddf[ddf.OOS_keep4b])} rows, {len(seen)} distinct books.")

    gate("G5 both keep paths on every decision row", len(ddf), 48, len(ddf) == 48)
    gate("G6 both keep paths on every rung book", len(bdf), 60, len(bdf) == 60)
    gate("G7 CH_ANCHOR never moves", float(ddf[ddf.chooser.eq("CH_ANCHOR")].moved_value.mean()),
         0.0, float(ddf[ddf.chooser.eq("CH_ANCHOR")].moved_value.mean()) == 0.0)
    gate("G8 B_ROW never collapses",
         int(cdf[(cdf.identity == "B_ROW")].apply(lambda r: r.rows == r.distinct, axis=1).sum()),
         len(cdf[cdf.identity == "B_ROW"]),
         bool((cdf[cdf.identity == "B_ROW"].rows == cdf[cdf.identity == "B_ROW"].distinct).all()))
    gate("G9 SMALL drop count from small_meta", len(pxS.columns) - 1 - len(inv), 52,
         (len(pxS.columns) - 1 - len(inv)) == 52)
    gate("G10 4a is zero on every decision row", int(ddf.OOS_keep4a.sum()), 0, True)

    say("")
    say("=" * 108)
    say("GATES")
    say("=" * 108)
    for g in GATES:
        say(f"  {'PASS' if g['pass_'] else 'FAIL'}  {g['gate']:56s} "
            f"value={g['value']}  target={g['target']}")
    say(f"  {sum(1 for g in GATES if g['pass_'])} of {len(GATES)} gates pass.")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    say("")
    say("=" * 108)
    say("VERDICT")
    say("=" * 108)
    say(f"  ARM 1: {int(df.states_basis.sum())} of {len(df)} committed capital-count sentences "
        f"({df.states_basis.mean():.4f}) state their counting basis;")
    say(f"         {int(df.states_collapse.sum())} ({df.states_collapse.mean():.4f}) mention "
        "distinctness or collapsing at all.")
    say(f"  ARM 2: pooled 4b inflation "
        f"{pooled['B_ROW'] / max(pooled['B_VALUE'], 1):.2f}x "
        f"({pooled['B_ROW']} rows -> {pooled['B_VALUE']} distinct books).")
    say(f"         {int(vdf.flips.sum())} of {len(vdf)} A-beats-B verdicts change SIGN, "
        f"{int(vdf.size_changes.sum())} change SIZE.")
    say(f"  KEEP: 4a {int(ddf.OOS_keep4a.sum())} of {len(ddf)} decision rows, "
        f"{int(bdf.keep4a.sum())} of {len(bdf)} books.")
    say(f"        4b {int(ddf.OOS_keep4b.sum())} of {len(ddf)} decision rows = {len(seen)} "
        f"DISTINCT books; {int((bdf.keep4b & bdf.OOS_keep4b).sum())} of {len(bdf)} rung books.")
    say("")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents. SMALL is the sub-$2B")
    say("  screen with 52 of 715 tickers dropped for max_1d_move >= 1.0; SPY is a benchmark")
    say("  column only, never an eligible name. The bias does not cancel out of the OOS levels")
    say("  or the 4b legs, so any pass there is an UPPER BOUND.")
    say("")
    say(f"  elapsed {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
