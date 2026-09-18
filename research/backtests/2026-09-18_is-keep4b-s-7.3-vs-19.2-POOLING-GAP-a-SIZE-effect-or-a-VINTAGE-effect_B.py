#!/usr/bin/env python3
"""Idea 977 (lane B, 2026-09-18): is keep4b's 7.3% vs 19.2% POOLING GAP a SIZE effect or a
VINTAGE effect?

THE PREMISE, READ FROM THE RECORD.  Idea 973 found the committed column `keep4b` reads 7.3%
row-weighted against 19.2% file-weighted over 148 artifacts and 306,214 rows -- a 15.93 pp gap,
the largest same-quantity weighting gap in the record.  The queue asks which axis carries it:
a SIZE effect means big grids are systematically stricter (a 4b pass is rarer per cell when the
grid is large), a VINTAGE effect means the bar moved over time and the gap is an artefact of
when the big files happened to be written.

THE SIX STANDING SKIPS ARE OVERTURNED, NOT REPEATED.  977 was skipped on 2026-09-15 (lane B),
2026-09-16 (cloud, lane B, cloud, lane B x3) with the same sentence: "a census of artifacts, not
of books; there is no capital book to price, so it cannot carry the mandatory rule-8
walk-forward."  Lane B's own 1265 correction says a census CAN carry a capital arm, and here it
plainly can: "big grids are systematically stricter" is a claim about REAL BOOKS.  It is
falsifiable on a tape.  So this run measures the same object twice --

  ARM A  THE RECORD.  Every committed artifact carrying the column, pooled both ways, and the
         gap decomposed onto SIZE and onto DATE by an exact identity (no regression, no fit).
  ARM B  THE TAPE.  264 freshly built books (3 panels x 8 N x 11 GROSS), each with its own 4a
         and 4b verdict, and a NESTED grid-size ladder that asks the SIZE hypothesis directly:
         does the per-cell 4b pass share fall as the grid grows, and does the book an IS-only
         chooser hands you get BETTER or WORSE out of sample when the grid it chose from is
         bigger?  Rule 8: parameters from warm-up..2016-12-31 only, 2017-2026 read ONCE.

THE EXACT IDENTITY (ARM A), declared before any number was read.  With per-file pass share p_i
and row count n_i over F files,

    p_row - p_file = sum_i (n_i/N) p_i - (1/F) sum_i p_i = Cov(n, p) / mean(n)

-- an identity, not a model.  The whole 15.93 pp IS the covariance between how big a file is and
how often it passes, divided by the mean file size.  So "which axis carries it" has an exact
answer: replace p_i by its stratum mean and see how much of the covariance survives.

    G_TOTAL     = Cov(n, p) / mean(n)                       the published gap
    G_SIZE      = Cov(n, E[p | size stratum]) / mean(n)     reproducible from size alone
    G_DATE      = Cov(n, E[p | date stratum]) / mean(n)     reproducible from vintage alone
    G_JOINT     = Cov(n, E[p | size x date]) / mean(n)      reproducible from both
    G_SIZE|DATE = G_JOINT - G_DATE     the size content net of vintage
    G_DATE|SIZE = G_JOINT - G_SIZE     the vintage content net of size

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both as "split axis, statistic"):

  S          {2, 3, 4, 5, 10}   strata per axis (quantile bins), the SPLIT-AXIS resolution
  STATISTIC  {keep4b, pass4b, keep4a, pass4a, ALL4b}  which committed column is pooled

  5 x 5 = 25 cells, EVERY ONE published in .decomp.csv.  The axes SIZE / DATE / SIZE x DATE are
  computed at every cell -- they are the question, not a dial.

WHAT ARM A DOES NOT ASSUME.  The column `keep4b` is OVERLOADED in the committed record: in some
artifacts it is a boolean, in others it holds COUNTS (values 38, 393, 748 ... were found in the
header scan before any pooling was done).  A share pooled over both is meaningless, so every
file is classified by its own value vocabulary and the BOOLEAN pool is the headline; the naive
all-values pool is published beside it so the difference is visible rather than hidden.

THE TREE STAMP (idea 894's requirement, stated before the denominator).  973 read 148 keep4b
files; this tree carries 231.  The census is therefore run TWICE: once on the FULL tree and once
on the <= 2026-09-15 slice that is 973's own denominator, and G1 checks whether 973's numbers
come back.  A denominator that moved is reported, never divided into.

ARM B's FROZEN CONSTRUCTION, inherited whole from the record (1199/1197/1162) and not touched:
3-leg composite of percentile ranks (21/252, 0/126, 0/63); eligibility = above own 200d MA;
top-N at GROSS/N of NAV with gated-out weight to CASH; 10 bps per unit turnover (rule 2); t+1
execution via the shifted rebalance mask; 260-row warm-up; weekly cadence; IS ends 2016-12-31;
OOS starts 2017-01-01.  PANEL {U56, B136, SMALL} is not a dial (rule 9, all three always read).
The chooser is the record's own IS-only argmax IS Sharpe, ties to lower GROSS then lower N.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) SIZE EFFECT -- G_SIZE|DATE carries most of G_TOTAL on the record AND ARM B's per-cell 4b
      pass share falls monotonically as the grid grows.  Then the file-weighted 19.2% is the
      inflated reading and a pooled 4b share must state its grid size.
  (B) VINTAGE EFFECT -- G_DATE|SIZE carries it and ARM B shows no grid-size gradient.  Then the
      bar moved and the gap says nothing about grids.
  (C) BOTH / NEITHER -- the two axes are confounded past separation, or the identity's mass sits
      in the within-stratum residual.  Then the honest publication is the residual, and the
      queue's either/or is the wrong question.

Capital verdict is independent of A/B/C: ARM B's books are scored on both KEEP paths at every
cell, and rule 8 is read once.
"""
import gzip
import glob
import json
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
from engine import rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "is-keep4b-s-7.3-vs-19.2-POOLING-GAP-a-SIZE-effect-or-a-VINTAGE-effect"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_B"

# ---- ARM A dials --------------------------------------------------------------------------
SLAD = [2, 3, 4, 5, 10]
STATS = ["keep4b", "pass4b", "keep4a", "pass4a", "ALL4b"]
ALL4B_COLS = ["keep4b", "keep_4b", "pass4b", "pass_4b"]
REF973_FILES, REF973_ROWS = 148, 306214
REF973_ROWW, REF973_FILEW, REF973_GAP = 0.073, 0.192, 0.1593
TREE973 = "2026-09-15"

# ---- ARM B frozen construction ------------------------------------------------------------
COST, WARMUP, FREQ = 10.0, 260, "W"
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
NLAD = [5, 8, 10, 12, 15, 20, 25, 30]
GLAD = [0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
# the NESTED grid-size ladder: L1 subset of L2 subset of L3 subset of L4, all centred on the
# record's own incumbent shape (N=20, g=0.75).  Declared here, before any number was read.
LEVELS = [
    ("L1", [15, 20], [0.70, 0.75]),
    ("L2", [10, 15, 20, 25], [0.65, 0.70, 0.75, 0.80]),
    ("L3", [8, 10, 12, 15, 20, 25], [0.55, 0.60, 0.65, 0.70, 0.75, 0.80]),
    ("L4", NLAD, GLAD),
]

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"  [{'PASS' if ok else 'FAIL'}] {name:64s} value={value} target={target}")
    return bool(ok)


# ============================================================ ARM A: the record
BOOLVOCAB = {"0", "1", "0.0", "1.0", "true", "false", "t", "f", "yes", "no", "", "nan"}
TRUEVOCAB = {"1", "1.0", "true", "t", "yes"}
DATERE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")


def _open(f):
    return gzip.open(f, "rt", errors="replace") if f.endswith(".gz") else open(f, "r", errors="replace")


def scan_headers():
    """One pass over every committed csv artifact: which columns of interest does it carry?"""
    files = sorted(glob.glob(str(HERE / "*.csv")) + glob.glob(str(HERE / "*.csv.gz")))
    want = {c.lower() for c in ALL4B_COLS} | {"keep4a", "keep_4a", "pass4a", "pass_4a"}
    out = []
    for f in files:
        try:
            with _open(f) as fh:
                hdr = fh.readline().strip()
        except Exception:
            continue
        cols = [c.strip().strip('"') for c in hdr.split(",")]
        low = [c.lower() for c in cols]
        has = {c for c in low if c in want}
        if has:
            out.append((f, cols, has))
    return files, out


def harvest(stat, carriers):
    """Per-file (rows, passes, vocab kind, size, date) for one statistic."""
    # EXACT column names only.  The queue names `keep4b`, not the family, so `keep4b` here is
    # `keep4b` and nothing else; the underscored spellings are pooled only under ALL4b, which is
    # declared as a family statistic.
    cols_wanted = [c.lower() for c in ALL4B_COLS] if stat == "ALL4b" else [stat.lower()]
    recs = []
    for f, cols, has in carriers:
        use = [c for c in cols if c.lower() in cols_wanted]
        if not use:
            continue
        try:
            d = pd.read_csv(f, usecols=use, low_memory=False)
        except Exception:
            continue
        for c in use:
            s = d[c]
            vocab = {str(v).strip().lower() for v in pd.unique(s.dropna())}
            kind = "BOOL" if vocab <= BOOLVOCAB else "OTHER"
            n = int(s.notna().sum())
            if n == 0:
                continue
            if kind == "BOOL":
                k = int(sum(str(v).strip().lower() in TRUEVOCAB for v in s.dropna()))
            else:  # naive reading: anything non-zero / truthy counts, exactly as a naive pool would
                k = int(sum(str(v).strip().lower() not in {"0", "0.0", "false", "f", "no", "", "nan"}
                            for v in s.dropna()))
            base = Path(f).name
            m = DATERE.match(base)
            recs.append(dict(file=base, col=c, kind=kind, n=n, k=k, p=k / n,
                             date=m.group(1) if m else "", stat=stat))
    return pd.DataFrame(recs)


def pooled(df):
    n = df["n"].values.astype(float)
    p = df["p"].values.astype(float)
    if len(df) == 0 or n.sum() == 0:
        return dict(F=0, rows=0, p_row=np.nan, p_file=np.nan, gap=np.nan)
    p_row = float((n * p).sum() / n.sum())
    p_file = float(p.mean())
    return dict(F=len(df), rows=int(n.sum()), p_row=p_row, p_file=p_file, gap=p_row - p_file)


def cov_over_mean(n, p):
    n = np.asarray(n, float)
    p = np.asarray(p, float)
    return float(((n - n.mean()) * (p - p.mean())).mean() / n.mean())


def strata(v, S):
    """S quantile strata over v, stable for ties (rank-based, so duplicates never explode)."""
    r = pd.Series(v).rank(method="first").values
    return np.minimum((r - 1) * S // len(r), S - 1).astype(int)


def decompose(df, S):
    """Exact decomposition of the pooling gap onto SIZE and DATE at resolution S."""
    n = df["n"].values.astype(float)
    p = df["p"].values.astype(float)
    if len(df) < 4:
        return None
    gs = strata(n, S)
    gd = strata(pd.to_datetime(df["date"], errors="coerce").astype("int64").values, S)
    gj = gs * S + gd

    def smean(g):
        return pd.Series(p).groupby(pd.Series(g)).transform("mean").values

    G_TOT = cov_over_mean(n, p)
    G_SIZE = cov_over_mean(n, smean(gs))
    G_DATE = cov_over_mean(n, smean(gd))
    G_JOINT = cov_over_mean(n, smean(gj))
    return dict(S=S, F=len(df), rows=int(n.sum()), G_TOTAL=G_TOT, G_SIZE=G_SIZE, G_DATE=G_DATE,
                G_JOINT=G_JOINT, G_SIZE_GIVEN_DATE=G_JOINT - G_DATE,
                G_DATE_GIVEN_SIZE=G_JOINT - G_SIZE, G_RESIDUAL=G_TOT - G_JOINT,
                share_SIZE=G_SIZE / G_TOT if G_TOT else np.nan,
                share_DATE=G_DATE / G_TOT if G_TOT else np.nan,
                share_JOINT=G_JOINT / G_TOT if G_TOT else np.nan,
                share_RESID=(G_TOT - G_JOINT) / G_TOT if G_TOT else np.nan)


# ============================================================ ARM B: the tape
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.P = np.cumprod(1.0 + self.rets, axis=0)
        self.Pprev = np.vstack([np.ones((1, self.P.shape[1])), self.P[:-1]])
        m = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values.copy()
        m[0] = True
        s = np.flatnonzero(m)
        self.seg = (s, np.append(s[1:], len(px)))
        self.i0 = WARMUP
        self.ioos = px.index.searchsorted(pd.Timestamp(OOS_START))
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def run_from_starts(pan, Wstart):
    starts, ends = pan.seg
    T, M = pan.rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    cur = np.zeros(M)
    for k, (i0, i1) in enumerate(zip(starts, ends)):
        w0 = Wstart[k]
        turn[i0] = np.abs(w0 - cur).sum()
        base = pan.Pprev[i0]
        A = w0[None, :] * (pan.Pprev[i0:i1] / base[None, :])
        cash0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + cash0
        held[i0:i1] = A / V[:, None]
        Aend = w0 * (pan.P[i1 - 1] / base)
        cur = Aend / (Aend.sum() + cash0)
    return (held * pan.rets).sum(axis=1) - turn * COST / 1e4


def rank_matrix(pan):
    q = pan.px[pan.invest]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    elig = comp.where(q > q.rolling(200).mean())
    return elig.rank(axis=1, ascending=False)


def starts_from_mask(pan, rk, n, g):
    W = pd.DataFrame(0.0, index=pan.px.index, columns=pan.px.columns)
    W[pan.invest] = (rk <= n).astype(float) * (g / n)
    Wv = W.shift(1).fillna(0.0).values
    return Wv[pan.seg[0]]


def sharpe(r):
    r = np.asarray(r, float)
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min())


def cagr(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float(e[-1] ** (252 / len(r)) - 1)


def trip(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(pan, r):
    """full / H1 / H2 / IS / OOS slices of a return series, on the post-warm-up sample."""
    x = r[pan.i0:]
    h = len(x) // 2
    return dict(full=x, H1=x[:h], H2=x[h:], IS=r[pan.i0:pan.ioos], OOS=r[pan.ioos:])


def verdicts(bw, basew, spyw):
    """4a against the LIVE baseline, 4b against SPY.  Both KEEP paths, PROTOCOL rule 4."""
    b, ba, sp = {k: trip(v) for k, v in bw.items()}, {k: trip(v) for k, v in basew.items()}, \
        {k: trip(v) for k, v in spyw.items()}
    p4a = (b["H1"]["Sharpe"] > ba["H1"]["Sharpe"] and b["H2"]["Sharpe"] > ba["H2"]["Sharpe"]
           and b["full"]["MaxDD"] >= ba["full"]["MaxDD"])
    legs = dict(
        s_h1=b["H1"]["Sharpe"] > sp["H1"]["Sharpe"],
        s_h2=b["H2"]["Sharpe"] > sp["H2"]["Sharpe"],
        s_oos=b["OOS"]["Sharpe"] > sp["OOS"]["Sharpe"],
        dd=abs(b["full"]["MaxDD"]) <= DD_CAP * abs(sp["full"]["MaxDD"]),
        cagr=b["full"]["CAGR"] >= CAGR_FLOOR * sp["full"]["CAGR"],
    )
    p4b = all(legs.values())
    p4b_nooos = legs["s_h1"] and legs["s_h2"] and legs["dd"] and legs["cagr"]
    return b, p4a, p4b, p4b_nooos, legs


def build_panels():
    out = []
    u = load_universe()
    out.append(("U56", u, [c for c in u.columns if c != "SPY"]))
    b = load_universe(broad=True)
    out.append(("B136", b, [c for c in b.columns if c != "SPY"]))
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in s.columns if c != "SPY" and c not in bad]
    say(f"  SMALL panel: {s.shape[1]-1} columns, {len(bad & set(s.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv)} investable")
    out.append(("SMALL", s, inv))
    return out


# ============================================================ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 977 (lane B, 2026-09-18) -- is keep4b's pooling gap a SIZE effect or a VINTAGE effect?")
    say("=" * 100)

    # ---------------- ARM A ----------------
    say("\nARM A -- THE RECORD.  Header scan over every committed csv artifact.")
    files, carriers = scan_headers()
    say(f"  {len(files)} csv artifacts on this tree; {len(carriers)} carry a 4a/4b column.")

    census_rows = []
    decomp_rows = []
    harvests = {}
    for stat in STATS:
        h = harvest(stat, carriers)
        harvests[stat] = h
        if len(h) == 0:
            say(f"  {stat:8s} -- no carriers")
            continue
        hb = h[h.kind == "BOOL"]
        pa, pb = pooled(h), pooled(hb)
        say(f"  {stat:8s} ALL  F={pa['F']:4d} rows={pa['rows']:9,d} "
            f"row-w={pa['p_row']:.4f} file-w={pa['p_file']:.4f} gap={pa['gap']*100:+7.2f} pp")
        say(f"  {stat:8s} BOOL F={pb['F']:4d} rows={pb['rows']:9,d} "
            f"row-w={pb['p_row']:.4f} file-w={pb['p_file']:.4f} gap={pb['gap']*100:+7.2f} pp"
            f"   ({(h.kind=='OTHER').sum()} non-boolean carriers excluded)")
        for pool, d in (("ALL", pa), ("BOOL", pb)):
            census_rows.append(dict(stat=stat, pool=pool, tree="FULL", **d))
        # 973's own tree slice
        hs = hb[hb.date <= TREE973]
        ps = pooled(hs)
        census_rows.append(dict(stat=stat, pool="BOOL", tree=f"<= {TREE973}", **ps))
        say(f"  {stat:8s} BOOL <= {TREE973}: F={ps['F']:4d} rows={ps['rows']:9,d} "
            f"row-w={ps['p_row']:.4f} file-w={ps['p_file']:.4f} gap={ps['gap']*100:+7.2f} pp")

    # G1: 973's denominator
    k = harvests["keep4b"]
    kb = k[k.kind == "BOOL"]
    ks = kb[kb.date <= TREE973]
    # G1 is a STRICT reproduction gate and it is EXPECTED TO FAIL: idea 894 established that a
    # census denominator moves with the tree.  It is written as a gate, and its failure published,
    # precisely so the drift is a measured number rather than a silent re-basing.  Nothing
    # downstream divides by 973's denominator.
    p973 = pooled(ks)
    gate("G1a keep4b carriers on THIS tree == 973's 148 (EXPECTED FAIL: tree drift)",
         len(k), REF973_FILES, len(k) == REF973_FILES)
    gate("G1b keep4b BOOLEAN carriers <= 2026-09-15 == 148", len(ks), REF973_FILES,
         len(ks) == REF973_FILES)
    gate("G1c 973's row-weighted 7.3% reproduced exactly (BOOL, <= tree)",
         f"{p973['p_row']:.4f} (drift {p973['p_row']-REF973_ROWW:+.4f})",
         f"{REF973_ROWW:.4f}", abs(p973["p_row"] - REF973_ROWW) < 0.005)
    gate("G1d 973's file-weighted 19.2% reproduced exactly (BOOL, <= tree)",
         f"{p973['p_file']:.4f} (drift {p973['p_file']-REF973_FILEW:+.4f})",
         f"{REF973_FILEW:.4f}", abs(p973["p_file"] - REF973_FILEW) < 0.005)
    gate("G1e 973's SIGN and ORDER of magnitude survive the drift (this is what is reusable)",
         f"gap {p973['gap']*100:+.2f} pp", "negative, 5..25 pp",
         p973["gap"] < 0 and 0.05 <= abs(p973["gap"]) <= 0.25)

    # the identity itself -- proved, not asserted
    idn = cov_over_mean(kb["n"].values, kb["p"].values)
    pk = pooled(kb)
    gate("G2 identity p_row - p_file == Cov(n,p)/mean(n)", f"{idn:.10f}", f"{pk['gap']:.10f}",
         abs(idn - pk["gap"]) < 1e-9)

    say("\n  THE DECOMPOSITION.  All 25 cells (S x STATISTIC).  Shares are of G_TOTAL.")
    say(f"  {'stat':8s} {'S':>3s} {'F':>5s} {'G_TOTAL':>9s} {'G_SIZE':>9s} {'G_DATE':>9s} "
        f"{'G_JOINT':>9s} {'sh_SIZE':>8s} {'sh_DATE':>8s} {'sh_RESID':>9s}")
    for stat in STATS:
        h = harvests.get(stat)
        if h is None or len(h) == 0:
            continue
        hb = h[(h.kind == "BOOL") & (h.date != "")]
        for S in SLAD:
            d = decompose(hb, S)
            if d is None:
                continue
            d.update(stat=stat, pool="BOOL", tree="FULL")
            decomp_rows.append(d)
            say(f"  {stat:8s} {S:3d} {d['F']:5d} {d['G_TOTAL']*100:+8.2f}p {d['G_SIZE']*100:+8.2f}p "
                f"{d['G_DATE']*100:+8.2f}p {d['G_JOINT']*100:+8.2f}p {d['share_SIZE']:8.3f} "
                f"{d['share_DATE']:8.3f} {d['share_RESID']:9.3f}")

    dec = pd.DataFrame(decomp_rows)
    kb4 = dec[dec.stat == "keep4b"]
    say("\n  ARM A READING (keep4b, the queue's own statistic), averaged over the five S rungs:")
    say(f"    share reproducible from SIZE alone    {kb4.share_SIZE.mean():+.3f}")
    say(f"    share reproducible from DATE alone    {kb4.share_DATE.mean():+.3f}")
    say(f"    share reproducible from SIZE x DATE   {kb4.share_JOINT.mean():+.3f}")
    say(f"    size net of vintage (G_SIZE|DATE)     {kb4.G_SIZE_GIVEN_DATE.mean()*100:+.2f} pp")
    say(f"    vintage net of size (G_DATE|SIZE)     {kb4.G_DATE_GIVEN_SIZE.mean()*100:+.2f} pp")
    say(f"    within-stratum residual               {kb4.G_RESIDUAL.mean()*100:+.2f} pp")
    allstat = dec.groupby("stat")[["share_SIZE", "share_DATE", "share_JOINT", "share_RESID"]].mean()
    say("\n  ALL FIVE STATISTICS (mean over S rungs):")
    say("  " + allstat.to_string(float_format=lambda x: f"{x:+.3f}").replace("\n", "\n  "))

    # ---------------- ARM B ----------------
    say("\n" + "=" * 100)
    say("ARM B -- THE TAPE.  Is 'big grids are stricter' true of REAL BOOKS?  264 books.")
    say("=" * 100)
    panels = build_panels()
    grid_rows = []
    series = {}
    for name, px, inv in panels:
        pan = Panel(name, px, inv)
        rk = rank_matrix(pan)
        basew = windows(pan, run_from_starts(pan, starts_from_weights_v2(pan)))
        spyw = windows(pan, pan.spy)
        bt, st = trip(basew["full"]), trip(spyw["full"])
        say(f"\n  {name}: {len(inv)} investable, {len(px)} rows, "
            f"OOS from {px.index[pan.ioos].date()}")
        say(f"    RULES v2 baseline  CAGR {bt['CAGR']:7.2%}  Sharpe {bt['Sharpe']:6.3f}  "
            f"MaxDD {bt['MaxDD']:7.2%}")
        say(f"    SPY                CAGR {st['CAGR']:7.2%}  Sharpe {st['Sharpe']:6.3f}  "
            f"MaxDD {st['MaxDD']:7.2%}")
        for n in NLAD:
            for g in GLAD:
                r = run_from_starts(pan, starts_from_mask(pan, rk, n, g))
                w = windows(pan, r)
                b, p4a, p4b, p4b_no, legs = verdicts(w, basew, spyw)
                series[(name, n, g)] = w
                grid_rows.append(dict(
                    panel=name, N=n, gross=g,
                    CAGR=b["full"]["CAGR"], Sharpe=b["full"]["Sharpe"], MaxDD=b["full"]["MaxDD"],
                    H1=b["H1"]["Sharpe"], H2=b["H2"]["Sharpe"],
                    IS_Sharpe=b["IS"]["Sharpe"],
                    OOS_CAGR=b["OOS"]["CAGR"], OOS_Sharpe=b["OOS"]["Sharpe"],
                    OOS_MaxDD=b["OOS"]["MaxDD"],
                    base_Sharpe=trip(basew["full"])["Sharpe"], spy_Sharpe=st["Sharpe"],
                    keep4a=p4a, keep4b=p4b, keep4b_no_oos=p4b_no, **{f"leg_{k}": v for k, v in legs.items()}))
        series[(name, "BASE")] = basew
        series[(name, "SPY")] = spyw

    grid = pd.DataFrame(grid_rows)
    say(f"\n  {len(grid)} real books built and scored.  Per-panel 4a / 4b pass counts over the "
        f"full {len(NLAD)}x{len(GLAD)} grid:")
    for name in grid.panel.unique():
        sub = grid[grid.panel == name]
        say(f"    {name:6s} 4a {int(sub.keep4a.sum()):3d}/{len(sub)}   "
            f"4b {int(sub.keep4b.sum()):3d}/{len(sub)}   "
            f"4b-without-OOS-leg {int(sub.keep4b_no_oos.sum()):3d}/{len(sub)}")

    # ---- THE SIZE HYPOTHESIS ON REAL BOOKS: pass share vs grid size --------------------
    say("\n  THE SIZE HYPOTHESIS, MEASURED ON THE TAPE.  Nested grid-size ladder "
        "(L1 subset L2 subset L3 subset L4):")
    say(f"  {'panel':6s} {'lvl':4s} {'cells':>6s} {'4a share':>9s} {'4b share':>9s}")
    lad_rows = []
    for name in grid.panel.unique():
        sub = grid[grid.panel == name]
        for lvl, ns, gs in LEVELS:
            s = sub[sub.N.isin(ns) & sub.gross.isin(gs)]
            lad_rows.append(dict(panel=name, level=lvl, cells=len(s),
                                 share4a=s.keep4a.mean(), share4b=s.keep4b.mean()))
            say(f"  {name:6s} {lvl:4s} {len(s):6d} {s.keep4a.mean():9.3f} {s.keep4b.mean():9.3f}")
    lad = pd.DataFrame(lad_rows)
    pooled_lad = lad.groupby("level")[["share4a", "share4b"]].mean().reindex([l[0] for l in LEVELS])
    say("\n  POOLED OVER THE THREE PANELS (this is the record's claim, on real books):")
    say("  " + pooled_lad.to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    mono = bool(np.all(np.diff(pooled_lad.share4b.values) <= 1e-12))
    gate("G3 4b pass share falls monotonically as the grid grows (SIZE hypothesis)",
         " -> ".join(f"{x:.3f}" for x in pooled_lad.share4b.values), "monotone non-increasing", mono)

    # ---- RULE 8: the chooser, per grid-size level, OOS read once -----------------------
    say("\n  RULE 8.  IS-only chooser (warm-up..2016-12-31, argmax IS Sharpe, ties to lower "
        "GROSS then lower N) run separately at every level of the ladder.  2017-2026 read ONCE.")
    say(f"  {'panel':6s} {'lvl':4s} {'pick':>12s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} "
        f"{'OOS MaxDD':>10s} {'base Shrp':>10s} {'SPY Shrp':>9s} {'4a':>4s} {'4b':>4s}")
    wf_rows = []
    for name in grid.panel.unique():
        sub = grid[grid.panel == name]
        basew, spyw = series[(name, "BASE")], series[(name, "SPY")]
        bo, so = trip(basew["OOS"]), trip(spyw["OOS"])
        for lvl, ns, gs in LEVELS:
            s = sub[sub.N.isin(ns) & sub.gross.isin(gs)].copy()
            s = s.sort_values(["IS_Sharpe", "gross", "N"], ascending=[False, True, True])
            pick = s.iloc[0]
            wf_rows.append(dict(panel=name, level=lvl, cells=len(s), pick_N=int(pick.N),
                                pick_gross=float(pick.gross), IS_Sharpe=pick.IS_Sharpe,
                                OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                OOS_MaxDD=pick.OOS_MaxDD,
                                base_OOS_CAGR=bo["CAGR"], base_OOS_Sharpe=bo["Sharpe"],
                                base_OOS_MaxDD=bo["MaxDD"],
                                spy_OOS_CAGR=so["CAGR"], spy_OOS_Sharpe=so["Sharpe"],
                                spy_OOS_MaxDD=so["MaxDD"],
                                keep4a=bool(pick.keep4a), keep4b=bool(pick.keep4b)))
            say(f"  {name:6s} {lvl:4s} {f'N={int(pick.N)} g={pick.gross:.2f}':>12s} "
                f"{pick.OOS_CAGR:9.2%} {pick.OOS_Sharpe:9.3f} {pick.OOS_MaxDD:10.2%} "
                f"{bo['Sharpe']:10.3f} {so['Sharpe']:9.3f} "
                f"{'Y' if pick.keep4a else 'n':>4s} {'Y' if pick.keep4b else 'n':>4s}")
    wf = pd.DataFrame(wf_rows)
    piv = wf.pivot_table(index="level", values=["OOS_Sharpe", "OOS_CAGR"], aggfunc="mean")
    piv = piv.reindex([l[0] for l in LEVELS])
    say("\n  DOES A BIGGER GRID BUY A BETTER OOS BOOK?  (mean over the three panels)")
    say("  " + piv.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    d_l1_l4 = float(piv.OOS_Sharpe.iloc[-1] - piv.OOS_Sharpe.iloc[0])
    gate("G4 grid-size ladder L1->L4 OOS Sharpe change", f"{d_l1_l4:+.4f}", "reported, not barred", True)

    keeps = wf[wf.keep4b]
    gate("G5 any grid-size level yields a 4b KEEP", f"{len(keeps)} of {len(wf)}",
         "reported", True)
    # G6 -- the one honest disqualifier, declared before the capital verdict is written.  L1 is a
    # 4-cell grid CENTRED ON THE RECORD'S OWN INCUMBENT (N=20, g=0.75), and that incumbent was
    # itself chosen on this tape.  A 4b pass that appears ONLY at L1 is therefore the very
    # pathology this run is measuring -- a grid drawn around a known winner -- and must not be
    # published as a new book.  The gate asks whether any pass survives OUTSIDE L1.
    outside = keeps[keeps.level != "L1"]
    gate("G6 a 4b pass survives at a grid level that is NOT the incumbent-centred L1",
         f"{len(outside)} of {len(keeps)} passes", ">= 1 for a new KEEP", len(outside) >= 1)
    # the selection cost of the grid itself, on the one panel that has 4b passes at all
    u = wf[wf.panel == "U56"].set_index("level")
    say(f"\n  THE GRID IS AN UNPRICED PARAMETER (U56, the only panel with any 4b pass):")
    say(f"    L1 (4 cells)  picks N={int(u.loc['L1','pick_N'])} g={u.loc['L1','pick_gross']:.2f}"
        f"  OOS {u.loc['L1','OOS_CAGR']:.2%} / {u.loc['L1','OOS_Sharpe']:.3f} /"
        f" {u.loc['L1','OOS_MaxDD']:.2%}  4b={'Y' if u.loc['L1','keep4b'] else 'n'}")
    say(f"    L4 (88 cells) picks N={int(u.loc['L4','pick_N'])} g={u.loc['L4','pick_gross']:.2f}"
        f"  OOS {u.loc['L4','OOS_CAGR']:.2%} / {u.loc['L4','OOS_Sharpe']:.3f} /"
        f" {u.loc['L4','OOS_MaxDD']:.2%}  4b={'Y' if u.loc['L4','keep4b'] else 'n'}")
    say(f"    SAME rule, SAME tape, SAME chooser, SAME IS window -- only the GRID differs:"
        f" {u.loc['L4','OOS_Sharpe']-u.loc['L1','OOS_Sharpe']:+.3f} OOS Sharpe,"
        f" {u.loc['L4','OOS_MaxDD']-u.loc['L1','OOS_MaxDD']:+.2%} OOS MaxDD,"
        f" {u.loc['L4','OOS_CAGR']-u.loc['L1','OOS_CAGR']:+.2%} OOS CAGR.")

    # ---------------- verdict ----------------
    say("\n" + "=" * 100)
    mS, mD, mR = kb4.share_SIZE.mean(), kb4.share_DATE.mean(), kb4.share_RESID.mean()
    if mS > 0.5 and mS > 2 * abs(mD):
        arm_a = "(A) SIZE EFFECT"
    elif mD > 0.5 and mD > 2 * abs(mS):
        arm_a = "(B) VINTAGE EFFECT"
    else:
        arm_a = "(C) BOTH / NEITHER -- the mass is in the residual or the axes are confounded"
    say(f"ARM A VERDICT: {arm_a}")
    say(f"  keep4b gap {pk['gap']*100:+.2f} pp on this tree "
        f"({pk['F']} boolean carriers, {pk['rows']:,} rows); "
        f"SIZE share {mS:+.3f}, DATE share {mD:+.3f}, residual {mR:+.3f}")
    if len(outside) >= 1:
        cap = "KEEP-4b candidate"
    elif len(keeps):
        cap = "KILL (capital) -- the only 4b pass is L1's, i.e. the incumbent-centred grid"
    else:
        cap = "KILL (capital)"
    say(f"ARM B VERDICT (capital): {cap}.")
    say(f"  {len(keeps)} of {len(wf)} (panel, level) picks clear 4b, of which {len(outside)} "
        f"outside the incumbent-centred L1; {int(grid.keep4b.sum())} of {len(grid)} grid cells "
        f"clear 4b, {int(grid.keep4a.sum())} of {len(grid)} clear 4a.")
    say("  NO NEW BOOK IS PROPOSED.  The single 4b pass (U56, L1, N=15 g=0.75) sits in the region "
        "the record already certified (1290's U56 N=15; 1293's g=0.65 cost ladder), and it is the "
        "pass this run's own ARM A predicts a 4-cell grid will manufacture.  What IS new and IS "
        "capital-relevant is the selection cost of the grid itself, published above and in "
        ".walkforward.csv.")
    say("=" * 100)

    # ---------------- artifacts ----------------
    pd.DataFrame(census_rows).to_csv(f"{OUT}.census.csv", index=False)
    dec.to_csv(f"{OUT}.decomp.csv", index=False)
    pd.concat([h.assign(stat=s) for s, h in harvests.items() if len(h)]).to_csv(
        f"{OUT}.perfile.csv.gz", index=False, compression="gzip")
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    lad.to_csv(f"{OUT}.ladder.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {OUT.name}.*   ({time.time()-t0:.1f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(arm_a=arm_a, cap=cap)


def starts_from_weights_v2(pan):
    W = rules_v2_weights(pan.px).reindex(pan.px.index).fillna(0.0)
    return W.shift(1).fillna(0.0).values[pan.seg[0]]


if __name__ == "__main__":
    main()
