#!/usr/bin/env python3
"""Idea 378: back-fill the MEAN NAME COUNT column over every quoted price in the record.

WHY.  Idea 124 (three independent runs, 2026-09-07) killed the "book-size floor" as a
number but left two clauses standing that the record has never applied to itself:

  * SIGN.      Below ~20 names a published price's SIGN is not reproducible: idea 122's
               3-axis admissible share is 0.649/0.846/0.650/0.551 at n=3/5/10/20 against
               0.885/0.979 at n=40/ALL, and the 5-name V1u book fails 24 of 41 panel-axis
               points where the 56-name book fails 0 of 26.
  * ORDERING.  Below ~40 names the MENU'S ORDERING is not reproducible: mean
               spearman(IS rate, OOS rate) is +0.002/-0.321/+0.105/-0.529 at n<=20
               against +0.573/+0.442/+0.752 at n>=40.

Both clauses are conditions ON A BOOK'S WIDTH.  The LEADERBOARD has no width column, so
no reader can tell which of the record's ~2100 quoted prices are inside them.  Idea 359
already measured the same defect on a subset (11 of 206 band rows recoverable, 5.3%) and
proposed a `names` column.  This run does the whole record and asks the queue's literal
question: recover mean holdings for every quoted price, and count how many were measured
below 20 names and below 40.

THE TEST, pre-registered before any number was read:

  [G] GATES.  Three reproduction controls, asserted before any new number.
      G1  the TOP20 / V1u rungs of this ladder ARE idea 94's targets() (max|dw| == 0).
      G2  H.run with every instrument off == engine.backtest (machine precision).
      G3  the price grid reproduces idea 124's committed `_B2.grid.csv` on every shared
          (uni, book, cost, arm) key.  This is the gate that makes [B] a re-measurement
          of the record's OWN books rather than a look-alike.

  [A] CENSUS OF THE COMMITTED RECORD.  Parse every data row of LEADERBOARD.md.  A row is
      PRICED if any of its CAGR / Sharpe / MaxDD cells carries a number; otherwise, if its
      text quotes a "k of N" or "k/N" share, it is a RATE row.  Resolve the Script cell to
      the committed artefacts and assign a RECOVERY TIER, in this priority order:
        R1 MEASURED    some sibling CSV carries a holdings-like column (names / n_names /
                       mean_names / names_held / breadth) -> a real width is recoverable.
        R2 NOMINAL-COL some sibling CSV carries an `n` / `nkeep` / `topn` / `rung` column
                       -> only the DIAL is recoverable, not the width.
        R3 ROW-TEXT    the row's own text names a size (TOP20, n=20, 5-name, top-5) or a
                       whole-panel construction (EWall, RULES v2, U56/B136/SMALL).
        R0 UNDEFINED   nothing.
      Every tier and every classified row is written to `<slug>.census.csv` so the call
      can be audited.  The lexicon is printed in full.

  [B] WIDTH MAP (the part that makes the back-fill honest).  R2 and R3 recover a NOMINAL
      n, and idea 359 already showed nominal != width (a "n=20" RANKE cell holds 11.8).
      So re-measure, from scratch, the MEAN HOLDINGS of every book-form the record prices:
      TOP{3,5,10,20,40,ALL}, V1u and EWall, on three panels, under each of the record's
      11 (gate x convention) instruments.  Mean holdings := mean over WEEKLY rebalance
      days of #{|w| > 1e-9} in the TARGET book (pre-registered; de-grossing instruments
      change gross, not the name count, and are priced on their book's control).
      Report nominal, measured, the ratio, and the MISCLASSIFICATION RATE of the nominal
      proxy at each threshold -- how often nominal and measured fall on opposite sides.

  [C] THE BACK-FILL.  Give every PRICED row its best available width: R1's measured
      column, or R2/R3's nominal CORRECTED by [B]'s median ratio at that nominal level.
      Count the rows below each threshold of the ladder {5, 10, 20, 40, 56}, with 20 (the
      sign clause) and 40 (the ordering clause) pre-registered from idea 124.  Rows that
      stay R0 are reported as UNDEFINED, never imputed.

  [D] KEEP PATHS 4a and 4b at EVERY grid point (panel x book x arm), at cost rungs
      {0, 10, 25} bps, against RULES v2 (live) and SPY.

  [E] RULE 8 walk-forward, two readings, 2017-2026 read once:
      E1  rung chosen on IS (<= 2016-12-31) Sharpe @10bps per (panel x arm); OOS CAGR /
          Sharpe / MaxDD against the n=20 anchor, RULES v2, SPY and the OOS-best rung.
      E2  idea 124's ORDERING clause re-tested on MEASURED width instead of nominal n:
          spearman(IS rate list, OOS rate list) over the 16 arms, per (panel x rung),
          pooled by whether the rung's MEASURED width is < 20, in [20,40), or >= 40.

TUNED PARAMETERS: exactly TWO -- the rung `n` and the width threshold `thresh`.  Panel,
book-form, gate, convention, arm and cost rung are REPORTED axes: every point of every
axis is printed and written to CSV.

CAVEATS.  (1) All three panels are current-constituent lists -- SURVIVORSHIP -- which
flatters every momentum book; levels are optimistic, rung-DIFFERENCES much less so.
(2) SMALL is the 484-column sub-$2B panel as cached (SPY joined as a benchmark and
excluded from every book), not the record's SMALL439; it starts 2010-01-04, so its
halves are not the same calendar halves as U56/B136.  (3) [A] and [C] are TEXT and
ARTEFACT classifications of a hand-written leaderboard: reproducible, not authoritative,
and every classified row is committed.  (4) Mean holdings is measured on TARGET weights;
a per-name trailing stop can hold fewer names intraperiod than its target says.

Deterministic, standalone.  Reads baseline.py, engine and committed CSVs; modifies nothing.
"""
import csv
import importlib.util
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location(
    "i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)

STEM = Path(__file__).stem
OUT = BT / STEM
I124 = BT / "2026-09-07_book-size-floor-for-any-quoted-price_B2"

PCOST = 10.0
COSTS = [0.0, 10.0, 25.0]
RUNGS = [3, 5, 10, 20, 40, "ALL"]
BOOKS = [f"TOP{n}" for n in RUNGS] + ["V1u", "EWall"]
ARMS = H.arm_specs()                                   # 17, control first
NON_CTL = [a for a in ARMS if a[0] != "control"]
THRESHOLDS = [5, 10, 20, 40, 56]                       # tuned param 2; 20/40 pre-registered
T_SIGN, T_ORDER = 20, 40                               # idea 124's two clauses
IS_END, OOS_START = H.IS_END, H.OOS_START
EPS = 1e-9

PANELS = [("U56", "universe.json(56)", dict()),
          ("B136", "universe_broad.json", dict(broad=True)),
          ("SMALL484", None, dict(small=True))]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

_LOG = []


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    _LOG.append(line)


def fmt(df, f="{:.4f}"):
    return df.to_string(index=False, float_format=lambda x: f.format(x))


# ====================================================================== construction
def gmask(px, gate, S):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma, v = S["ma"], S["v20"]
    if gate == "g200":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * 1.03, 1.0)
        raw = raw.mask(px < ma * 0.97, 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "abs12":
        return (px > px.shift(252)).fillna(False)
    if gate == "vol60":
        return (v < H.MAX_VOL).fillna(False)
    if gate == "v1gate":
        return ((px > ma) & (v < H.MAX_VOL)).fillna(False)
    raise ValueError(gate)


def panel_signals(px):
    """Idea 124's cached panel signals, byte-identical (gate G3 asserts it)."""
    comp = H.composite(px)
    v20 = H.vol20(px)
    ma = px.rolling(200).mean()
    S = dict(comp=comp, v20=v20, ma=ma, v1s=comp / v20.clip(lower=0.08) ** 0.5)
    S["gates"] = {g: gmask(px, g, S) for g in H.GATES}
    S["rank"] = {}
    for skey in ("comp", "v1s"):
        s = S[skey]
        S["rank"][(skey, None)] = s.rank(axis=1, ascending=False)
        S["rank"][(skey, "cnt")] = s.notna().sum(axis=1)
        for g in H.GATES:
            sg = s.where(S["gates"][g])
            S["rank"][(skey, g)] = sg.rank(axis=1, ascending=False)
            S["rank"][(skey, g, "cnt")] = sg.notna().sum(axis=1)
    return S


def rung_of(book):
    return None if book in ("V1u", "EWall") else book[3:]


def nominal(book, px):
    """The name count the RECORD writes for this book -- the column being replaced."""
    if book == "V1u":
        return float(H.NV1)
    if book == "EWall":
        return float(px.shape[1])
    r = rung_of(book)
    return float(px.shape[1]) if r == "ALL" else float(int(r))


def _topw(rank, n, cnt):
    if n == "ALL":
        k = cnt.replace(0, np.nan)
        return rank.le(k, axis=0).astype(float).mul(H.GROSS / k, axis=0).fillna(0.0)
    return (rank <= n).astype(float) * (H.GROSS / n)


def targets(px, book, S, gate=None, conv="dg"):
    if book == "EWall":
        return H.targets(px, "EWall", gate, conv)
    skey = "v1s" if book == "V1u" else "comp"
    r = rung_of(book)
    if conv == "rw" and gate is not None:
        rank = S["rank"][(skey, gate)]
        if book == "V1u":
            return (rank <= H.NV1).astype(float) * H.WV1
        return _topw(rank, r if r == "ALL" else int(r), S["rank"][(skey, gate, "cnt")])
    rank = S["rank"][(skey, None)]
    base = ((rank <= H.NV1).astype(float) * H.WV1 if book == "V1u"
            else _topw(rank, r if r == "ALL" else int(r), S["rank"][(skey, "cnt")]))
    return base if gate is None else base.where(S["gates"][gate], 0.0)


def mean_names(W, mask):
    """Mean holdings/day := mean over WEEKLY rebalance days of #{|w| > EPS}."""
    held = (W.abs() > EPS).sum(axis=1)
    return float(held[mask.reindex(held.index, fill_value=False)].mean())


def dpair(rc, ra):
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd > 0.10 else np.nan)


def win(r, w):
    return r if w == "full" else (r.loc[:IS_END] if w == "IS" else r.loc[OOS_START:])


def bars(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS_CAGR=metrics(win(r, "OOS"))["CAGR"],
                OOS_Sharpe=metrics(win(r, "OOS"))["Sharpe"],
                OOS_MaxDD=metrics(win(r, "OOS"))["MaxDD"],
                IS_Sharpe=metrics(win(r, "IS"))["Sharpe"])


def keep_paths(b, v2, spy):
    """PROTOCOL rule 4.  Returns (pass4a, pass4b, first failing 4b bar)."""
    p4a = (b["H1"] > v2["H1"]) and (b["H2"] > v2["H2"]) and (b["MaxDD"] >= v2["MaxDD"])
    f = None
    if not (b["H1"] > spy["H1"]):
        f = "H1"
    elif not (b["H2"] > spy["H2"]):
        f = "H2"
    elif not (b["OOS_Sharpe"] > spy["OOS_Sharpe"]):
        f = "OOS"
    elif not (abs(b["MaxDD"]) <= 0.60 * abs(spy["MaxDD"])):
        f = "DD"
    elif not (b["CAGR"] >= 0.70 * spy["CAGR"]):
        f = "CAGR"
    return bool(p4a), f is None, (f or "")


# ====================================================================== [A] census
SPLIT = re.compile(r"(?<!\\)\|")
HOLD_COL = re.compile(
    r"(^|_)(mean_)?names?(_held|_sel|_all|_gate)?$|^n_names$|^breadth\w*$|^m_names$"
    r"|^npos$|^positions$", re.I)
NOM_COL = re.compile(r"^(n|nkeep|topn|n_top|rung)$", re.I)
TXT_N = [re.compile(p, re.I) for p in
         (r"\bTOP\s?-?(\d+)\b", r"\bn\s?=\s?(\d+)\b", r"\b(\d+)-name\b",
          r"\btop-(\d+)\b", r"\bn(\d+)\b")]
TXT_PANEL = {"u56": 56, "universe.json": 56, "b136": 136, "universe_broad": 136,
             "small439": 439, "small484": 484, "ewall": None, "rules v2": None}
RATE_PAT = re.compile(r"\b\d+\s*(?:of|/)\s*\d+\b")


def _cells(line):
    return [x.strip() for x in SPLIT.split(line)[1:-1]]


def _isnum(x):
    x = x.strip().replace("*", "")
    return x.lower() not in ("n/a", "", "-", "—", "na") and bool(re.search(r"\d", x))


def census():
    lines = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    raw = [l for l in lines if l.startswith("|") and not re.match(r"^\|[-|\s]+\|$", l)]
    sib = defaultdict(list)
    for f in BT.glob("*.csv"):
        sib[f.name.split(".")[0]].append(f)
    hcache, vcache = {}, {}

    def header(f):
        if f not in hcache:
            try:
                with open(f) as fh:
                    hcache[f] = [c.strip() for c in next(csv.reader(fh))]
            except Exception:
                hcache[f] = []
        return hcache[f]

    def colvals(f, cols):
        key = (f, tuple(cols))
        if key not in vcache:
            try:
                d = pd.read_csv(f, usecols=lambda c: c.strip() in cols)
                v = pd.to_numeric(d.stack(), errors="coerce").dropna()
                vcache[key] = float(v.median()) if len(v) else np.nan
            except Exception:
                vcache[key] = np.nan
        return vcache[key]

    rows, malformed = [], 0
    for line in raw:
        c = _cells(line)
        if len(c) < 9 or c[0] == "Date":
            malformed += 1
            continue
        idea, verdict, script = c[1], c[-2], c[-1]
        priced = any(_isnum(x) for x in c[2:5])
        rate = (not priced) and bool(RATE_PAT.search(idea + " " + verdict))
        if not (priced or rate):
            continue
        sc = script.replace("`", "").split("/")[-1].strip()
        stem = sc[:-3] if sc.endswith(".py") else sc
        fs = sorted(sib.get(stem, []))
        tier, width, nom, src = "R0", np.nan, np.nan, ""
        hcols, ncols = set(), set()
        for f in fs:
            for col in header(f):
                if HOLD_COL.search(col):
                    hcols.add(col)
                if NOM_COL.match(col):
                    ncols.add(col)
        if hcols:
            vals = [colvals(f, hcols) for f in fs]
            vals = [v for v in vals if np.isfinite(v)]
            if vals:
                tier, width, src = "R1", float(np.median(vals)), ",".join(sorted(hcols))
        if tier == "R0" and ncols:
            vals = [colvals(f, ncols) for f in fs]
            vals = [v for v in vals if np.isfinite(v)]
            if vals:
                tier, nom, src = "R2", float(np.median(vals)), ",".join(sorted(ncols))
        if tier == "R0":
            hits = []
            for pat in TXT_N:
                hits += [int(m) for m in pat.findall(idea) if 0 < int(m) <= 1000]
            if hits:
                tier, nom, src = "R3", float(np.median(hits)), "row-text:size"
            else:
                low = idea.lower()
                for tok, n in TXT_PANEL.items():
                    if tok in low and n:
                        tier, nom, src = "R3", float(n), f"row-text:panel({tok})"
                        break
        rows.append(dict(kind="PRICED" if priced else "RATE", date=c[0], script=stem,
                         tier=tier, width_R1=width, nominal=nom, evidence=src,
                         idea=idea[:180]))
    return pd.DataFrame(rows), malformed, len(raw)


# ====================================================================== main
def main():
    t0 = time.time()
    say("=" * 150)
    say("IDEA 378  back-fill the mean-name-count column over every quoted price   "
        f"[{time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}]")
    say("=" * 150)

    # ---------------------------------------------------------------- [A] census
    say("\n" + "=" * 150)
    say("[A] CENSUS OF THE COMMITTED RECORD -- how much of the width column is recoverable")
    say("=" * 150)
    say("holdings-like column lexicon : " + HOLD_COL.pattern)
    say("nominal-dial column lexicon  : " + NOM_COL.pattern)
    say("row-text size patterns       : " + " | ".join(p.pattern for p in TXT_N))
    say("row-text panel tokens        : " + ", ".join(k for k, v in TXT_PANEL.items() if v))
    C, malformed, nraw = census()
    C.to_csv(f"{OUT}.census.csv", index=False)
    say(f"\nLEADERBOARD table lines {nraw}; skipped as header/malformed (<9 cells) {malformed}; "
        f"classified {len(C)}  (PRICED {int((C.kind=='PRICED').sum())}, "
        f"RATE {int((C.kind=='RATE').sum())})")
    for kind in ("PRICED", "RATE"):
        sub = C[C.kind == kind]
        t = sub.tier.value_counts().reindex(["R1", "R2", "R3", "R0"]).fillna(0).astype(int)
        say(f"\n  {kind} rows ({len(sub)}) by recovery tier:")
        for k, v in t.items():
            lbl = dict(R1="MEASURED (a holdings column exists)",
                       R2="NOMINAL-COL (only the dial `n`)",
                       R3="ROW-TEXT (size or panel named in the row)",
                       R0="UNDEFINED (nothing recoverable)")[k]
            say(f"      {k}  {v:5d}  {v/max(len(sub),1):6.1%}   {lbl}")
    P = C[C.kind == "PRICED"]
    say(f"\n  ==> the queue's literal method (R1 only) reaches "
        f"{int((P.tier=='R1').sum())} of {len(P)} priced rows "
        f"({(P.tier=='R1').mean():.1%}); it FAILS on {(P.tier!='R1').mean():.1%}.")
    say(f"      scripts with NO committed CSV at all: "
        f"{int((P.tier=='R0').sum())} priced rows are unresolvable by any artefact route.")

    # ---------------------------------------------------------------- [B]+[G]+[D] panels
    say("\n" + "=" * 150)
    say("[G] GATES + [B] WIDTH MAP + [D] KEEP PATHS -- re-measuring the record's own books")
    say("=" * 150)
    ref124 = pd.read_csv(f"{I124}.grid.csv")
    widths, grid, wf, order = [], [], [], []
    g3_err, g3_n = 0.0, 0

    for pname, uni124, kw in PANELS:
        px_all = load_universe(**kw)
        px = px_all
        drop_spy = bool(kw.get("small"))
        pxb = px.drop(columns=["SPY"]) if drop_spy else px          # book construction panel
        start = px.index[260]
        rmask = H.rebalance_mask(px.index, H.FREQ)
        S = panel_signals(pxb)
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        say("\n" + "-" * 150)
        say(f"PANEL {pname}: {pxb.shape[1]} book names ({px.shape[1]} columns"
            f"{', SPY excluded from every book' if drop_spy else ''}), "
            f"{px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()} "
            f"| IS <= {IS_END} | OOS >= {OOS_START}")
        sb = bars(spy_r)
        say(f"  SPY: CAGR {sb['CAGR']:.2%} Sharpe {sb['Sharpe']:.3f} MaxDD {sb['MaxDD']:.2%} "
            f"halves {sb['H1']:.3f}/{sb['H2']:.3f} OOS Sharpe {sb['OOS_Sharpe']:.3f}")

        # ---- G1: the rungs ARE idea 94's books
        worst = 0.0
        for bk in ("TOP20", "V1u", "EWall"):
            for g in [None] + H.GATES:
                for conv in (("dg",) if g is None else ("dg", "rw")):
                    a = targets(pxb, bk, S, g, conv).fillna(0.0)
                    e = H.targets(pxb, bk, g, conv).fillna(0.0)
                    worst = max(worst, float((a - e).abs().to_numpy().max()))
        say(f"  [G1] TOP20 / V1u / EWall vs idea 94 targets(): max|dw| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-15 else 'NOT EXACT -- unsafe'})")
        assert worst < 1e-12, "G1 failed"

        # ---- per (book, arm, cost) returns
        def W_of(b, g, conv):
            return targets(pxb, b, S, g, conv).reindex(columns=px.columns).fillna(0.0)

        rets, ctlW = {}, {}
        for b in BOOKS:
            ctlW[b] = W_of(b, None, "dg")
            for name, kind, kwargs, (g, conv) in ARMS:
                W = W_of(b, g, conv) if kind == "gate" else ctlW[b]
                for c in COSTS:
                    rets[(b, name, c)] = H.run(px, W, bps=c, **kwargs)["r"].loc[start:]

        # ---- G2: harness == engine
        wb = 0.0
        for b in BOOKS:
            wb = max(wb, float((H.run(px, ctlW[b], bps=PCOST)["r"].loc[start:]
                                - backtest(px, ctlW[b], cost_bps=PCOST,
                                           freq=H.FREQ)["returns"].loc[start:]).abs().max()))
        say(f"  [G2] H.run(all instruments off) vs engine.backtest @10bps: max|diff| = {wb:.3e} "
            f"({'EXACT' if wb < 1e-12 else 'NOT EXACT -- unsafe'})")
        assert wb < 1e-10, "G2 failed"

        # ---- G3: the grid reproduces idea 124's committed prices
        if uni124 is not None:
            R = ref124[ref124.uni == uni124]
            errs = []
            for _, rr in R.iterrows():
                if rr.book not in BOOKS or rr.cost not in COSTS:
                    continue
                dc, dd, _ = dpair(rets[(rr.book, "control", rr.cost)],
                                  rets[(rr.book, rr.arm, rr.cost)])
                errs += [abs(dc - rr.dCAGR), abs(dd - rr.dMaxDD)]
            if errs:
                g3_err = max(g3_err, max(errs))
                g3_n += len(errs) // 2
                say(f"  [G3] reproduces idea 124 `_B2.grid.csv` on {len(errs)//2} rows: "
                    f"max|err| = {max(errs):.3e}")

        # ---- [B] width map
        v2W = rules_v2_weights(pxb).reindex(columns=px.columns).fillna(0.0)
        v1W = rules_v1_weights(pxb).reindex(columns=px.columns).fillna(0.0)
        for b in BOOKS:
            for g in [None] + H.GATES:
                for conv in (("dg",) if g is None else ("dg", "rw")):
                    W = W_of(b, g, conv).loc[start:]
                    m = mean_names(W, rmask)
                    nom = nominal(b, pxb)
                    widths.append(dict(panel=pname, book=b, gate=g or "none", conv=conv,
                                       nominal=nom, measured=m, ratio=m / nom if nom else np.nan,
                                       lt20=m < T_SIGN, lt40=m < T_ORDER,
                                       nom_lt20=nom < T_SIGN, nom_lt40=nom < T_ORDER))
        for lbl, W in (("RULES v2 (LIVE)", v2W), ("RULES v1", v1W)):
            widths.append(dict(panel=pname, book=lbl, gate="own", conv="own",
                               nominal=float(pxb.shape[1]) if "v2" in lbl else float(H.NV1),
                               measured=mean_names(W.loc[start:], rmask), ratio=np.nan,
                               lt20=np.nan, lt40=np.nan, nom_lt20=np.nan, nom_lt40=np.nan))

        # ---- [D] KEEP paths, and the per-cell statistics
        v2r = {c: backtest(px, v2W, cost_bps=c, freq=H.FREQ)["returns"].loc[start:] for c in COSTS}
        v2names = mean_names(v2W.loc[start:], rmask)
        wm = {(b, g or "none", conv): mean_names(W_of(b, g, conv).loc[start:], rmask)
              for b in BOOKS for g in [None] + H.GATES
              for conv in (("dg",) if g is None else ("dg", "rw"))}
        for b in BOOKS:
            for name, kind, _, (g, conv) in ARMS:
                key = (b, (g or "none") if kind == "gate" else "none",
                       conv if kind == "gate" else "dg")
                for c in COSTS:
                    r = rets[(b, name, c)]
                    bb = bars(r)
                    p4a, p4b, fb = keep_paths(bb, bars(v2r[c]), sb)
                    dc, dd, rate = dpair(rets[(b, "control", c)], r)
                    dcI, ddI, rateI = dpair(win(rets[(b, "control", c)], "IS"), win(r, "IS"))
                    dcO, ddO, rateO = dpair(win(rets[(b, "control", c)], "OOS"), win(r, "OOS"))
                    grid.append(dict(panel=pname, book=b, rung=rung_of(b) or b, arm=name,
                                     kind=kind, cost=c, nominal=nominal(b, pxb),
                                     names=wm[key], v2_names=v2names, **bb,
                                     dCAGR=dc, dMaxDD=dd, rate=rate,
                                     rate_IS=rateI, rate_OOS=rateO,
                                     published=bool(np.isfinite(rate)),
                                     pass4a=p4a, pass4b=p4b, fail4b=fb,
                                     corr_v2=float(r.corr(v2r[c])),
                                     dw_vs_v2=float((W_of(b, g if kind == "gate" else None,
                                                          conv if kind == "gate" else "dg")
                                                     - v2W).abs().loc[start:].to_numpy().max())))

        # ---- [E1] rule 8: rung chosen on IS Sharpe @10bps, per arm
        for name, kind, _, _ in ARMS:
            cand = [b for b in BOOKS if b.startswith("TOP")]
            iss = {b: metrics(win(rets[(b, name, PCOST)], "IS"))["Sharpe"] for b in cand}
            pick = max(iss, key=lambda b: iss[b])
            best = max(cand, key=lambda b: metrics(win(rets[(b, name, PCOST)], "OOS"))["Sharpe"])
            po, bo = bars(rets[(pick, name, PCOST)]), bars(rets[(best, name, PCOST)])
            an = bars(rets[("TOP20", name, PCOST)])
            v2b = bars(v2r[PCOST])
            wf.append(dict(panel=pname, arm=name, pick=pick,
                           pick_names=wm[(pick, "none", "dg")] if kind != "gate" else np.nan,
                           IS_Sharpe=iss[pick], OOS_CAGR=po["OOS_CAGR"],
                           OOS_Sharpe=po["OOS_Sharpe"], OOS_MaxDD=po["OOS_MaxDD"],
                           anchor="TOP20", anchor_OOS_Sharpe=an["OOS_Sharpe"],
                           best=best, best_OOS_Sharpe=bo["OOS_Sharpe"],
                           regret=po["OOS_Sharpe"] - bo["OOS_Sharpe"],
                           beat_anchor=po["OOS_Sharpe"] > an["OOS_Sharpe"],
                           v2_OOS_Sharpe=v2b["OOS_Sharpe"], beat_v2=po["OOS_Sharpe"] > v2b["OOS_Sharpe"],
                           spy_OOS_Sharpe=sb["OOS_Sharpe"], beat_spy=po["OOS_Sharpe"] > sb["OOS_Sharpe"]))

        # ---- [E2] idea 124's ORDERING clause, on MEASURED width
        for b in BOOKS:
            rIS, rOOS = [], []
            for name, kind, _, _ in NON_CTL:
                _, _, a = dpair(win(rets[(b, "control", PCOST)], "IS"), win(rets[(b, name, PCOST)], "IS"))
                _, _, o = dpair(win(rets[(b, "control", PCOST)], "OOS"), win(rets[(b, name, PCOST)], "OOS"))
                rIS.append(a)
                rOOS.append(o)
            sp = H.spearman(rIS, rOOS)
            n_ok = int((np.isfinite(np.asarray(rIS, float))
                        & np.isfinite(np.asarray(rOOS, float))).sum())
            order.append(dict(panel=pname, book=b, nominal=nominal(b, pxb),
                              names=wm[(b, "none", "dg")], spearman_IS_OOS=sp,
                              n_priced_both=n_ok,
                              band=("<20" if wm[(b, "none", "dg")] < T_SIGN
                                    else ("20-40" if wm[(b, "none", "dg")] < T_ORDER else ">=40")),
                              nom_band=("<20" if nominal(b, pxb) < T_SIGN
                                        else ("20-40" if nominal(b, pxb) < T_ORDER else ">=40"))))
        say(f"  panel done in {time.time()-t0:.0f}s cumulative")

    Wd = pd.DataFrame(widths)
    G = pd.DataFrame(grid)
    WF = pd.DataFrame(wf)
    OR = pd.DataFrame(order)
    Wd.to_csv(f"{OUT}.widthmap.csv", index=False)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    OR.to_csv(f"{OUT}.ordering.csv", index=False)
    say(f"\n  [G3] TOTAL: reproduced idea 124's committed grid on {g3_n} (book x arm x cost) "
        f"rows, max|err| = {g3_err:.3e} "
        f"({'EXACT' if g3_err < 1e-12 else 'NOT EXACT -- unsafe'})")
    assert g3_err < 1e-10 and g3_n > 0, "G3 failed"

    # ---------------------------------------------------------------- [B] report
    say("\n" + "=" * 150)
    say("[B] WIDTH MAP -- what the record CALLS the book vs what the book HOLDS")
    say("=" * 150)
    ctl = Wd[Wd.gate.isin(["none", "own"])]
    piv = ctl.pivot_table(index="book", columns="panel", values="measured", aggfunc="first")
    piv.insert(0, "nominal(U56)",
               ctl[ctl.panel == "U56"].set_index("book").nominal.reindex(piv.index))
    say("\n  control books (no gate), mean holdings per weekly rebalance day, "
        "against the name count the record writes:")
    say(piv.to_string(float_format=lambda x: f"{x:.1f}"))
    lad = Wd[(Wd.gate != "own")]
    say(f"\n  over all {len(lad)} (panel x book x gate x conv) cells:")
    say(f"      nominal < {T_SIGN}: {int(lad.nom_lt20.sum())}   measured < {T_SIGN}: "
        f"{int(lad.lt20.sum())}   -> the nominal proxy MISCLASSIFIES "
        f"{int((lad.nom_lt20 != lad.lt20).sum())} of {len(lad)} "
        f"({(lad.nom_lt20 != lad.lt20).mean():.1%}) at the SIGN threshold")
    say(f"      nominal < {T_ORDER}: {int(lad.nom_lt40.sum())}   measured < {T_ORDER}: "
        f"{int(lad.lt40.sum())}   -> the nominal proxy MISCLASSIFIES "
        f"{int((lad.nom_lt40 != lad.lt40).sum())} of {len(lad)} "
        f"({(lad.nom_lt40 != lad.lt40).mean():.1%}) at the ORDERING threshold")
    say("\n  measured/nominal ratio by nominal level (the back-fill correction):")
    ratio = lad.groupby("nominal").ratio.agg(["count", "median", "min", "max"])
    say(ratio.to_string(float_format=lambda x: f"{x:.3f}"))
    RMAP = lad.groupby("nominal").ratio.median()
    live = Wd[Wd.book == "RULES v2 (LIVE)"]
    say("\n  THE LIVE BOOK: RULES v2 mean holdings " +
        ", ".join(f"{r.panel} {r.measured:.1f}" for _, r in live.iterrows()) +
        f"   (sign clause {T_SIGN}, ordering clause {T_ORDER})")

    # ---------------------------------------------------------------- [C] back-fill
    say("\n" + "=" * 150)
    say("[C] THE BACK-FILL -- every priced row given its best available width")
    say("=" * 150)

    def corrected(row):
        if row.tier == "R1":
            return row.width_R1
        if np.isfinite(row.nominal):
            keys = RMAP.index.to_numpy(float)
            k = keys[np.argmin(np.abs(keys - row.nominal))]
            return row.nominal * float(RMAP.loc[k])
        return np.nan

    P = C[C.kind == "PRICED"].copy()
    P["width"] = P.apply(corrected, axis=1)
    P["width_raw"] = np.where(P.tier == "R1", P.width_R1, P.nominal)
    P.to_csv(f"{OUT}.backfill.csv", index=False)
    known = P[np.isfinite(P.width)]
    ans = []
    for t in THRESHOLDS:
        ans.append(dict(threshold=t,
                        below_corrected=int((known.width < t).sum()),
                        below_raw=int((known.width_raw < t).sum()),
                        share_of_known=float((known.width < t).mean()),
                        share_of_all_priced=float((known.width < t).sum() / len(P))))
    A = pd.DataFrame(ans)
    A.to_csv(f"{OUT}.answer.csv", index=False)
    say(f"\n  priced rows {len(P)}; width recovered for {len(known)} ({len(known)/len(P):.1%}); "
        f"UNDEFINED {len(P)-len(known)} ({1-len(known)/len(P):.1%}) -- never imputed")
    say("\n  " + fmt(A).replace("\n", "\n  "))
    say(f"\n  ==> THE QUEUE'S QUESTION, answered on the {len(known)} recoverable rows:")
    say(f"      below {T_SIGN} names (idea 124's SIGN clause):     "
        f"{int((known.width<T_SIGN).sum()):d} of {len(known)} "
        f"({(known.width<T_SIGN).mean():.1%}) recoverable, "
        f"{(known.width<T_SIGN).sum()/len(P):.1%} of all priced rows")
    say(f"      below {T_ORDER} names (idea 124's ORDERING clause): "
        f"{int((known.width<T_ORDER).sum()):d} of {len(known)} "
        f"({(known.width<T_ORDER).mean():.1%}) recoverable, "
        f"{(known.width<T_ORDER).sum()/len(P):.1%} of all priced rows")
    say("\n  by recovery tier:")
    say(known.groupby("tier").agg(rows=("width", "size"), median_width=("width", "median"),
                                  below20=("width", lambda s: int((s < T_SIGN).sum())),
                                  below40=("width", lambda s: int((s < T_ORDER).sum()))
                                  ).to_string(float_format=lambda x: f"{x:.1f}"))

    # ---------------------------------------------------------------- [D] report
    say("\n" + "=" * 150)
    say("[D] KEEP PATHS 4a and 4b at every grid point")
    say("=" * 150)
    for c in COSTS:
        s = G[G.cost == c]
        say(f"  @{c:>4.0f} bps  cells {len(s):4d}   4a {int(s.pass4a.sum()):3d}/{len(s)}   "
            f"4b {int(s.pass4b.sum()):3d}/{len(s)}")
    s10 = G[G.cost == PCOST]
    say("\n  first-failing 4b bar @10 bps: " +
        ", ".join(f"{k} {v}" for k, v in Counter(s10[~s10.pass4b].fail4b).most_common()))
    say("\n  4b passers @10 bps by panel x measured-width band:")
    s10 = s10.copy()
    s10["band"] = np.where(s10.names < T_SIGN, "<20",
                           np.where(s10.names < T_ORDER, "20-40", ">=40"))
    say(s10.pivot_table(index="band", columns="panel", values="pass4b",
                        aggfunc=["sum", "size"]).to_string())
    p4a = G[G.pass4a]
    if len(p4a):
        say(f"\n  4a passers over all {len(G)} grid points, WITH their distance from the "
            "live book (a 4a pass that is the live RULES v2 under another denominator is "
            "not a new book):")
        say(fmt(p4a[["panel", "book", "arm", "cost", "names", "v2_names", "CAGR", "Sharpe",
                     "MaxDD", "H1", "H2", "OOS_Sharpe", "corr_v2", "dw_vs_v2"]]))
    else:
        say("\n  4a: NOTHING beats the live RULES v2 book at any of the "
            f"{len(G)} grid points, at any cost rung.")
    b4 = s10[s10.pass4b].sort_values("Sharpe", ascending=False)
    say(f"\n  the 10 strongest 4b passers @10 bps (of {len(b4)}), by Sharpe:")
    say(fmt(b4.head(10)[["panel", "book", "arm", "names", "CAGR", "Sharpe", "MaxDD",
                         "H1", "H2", "OOS_Sharpe", "corr_v2"]]))

    # ---------------------------------------------------------------- [E] rule 8
    say("\n" + "=" * 150)
    say("[E1] RULE 8 WALK-FORWARD -- rung chosen on IS (<=2016) Sharpe @10bps, 2017-2026 read once")
    say("=" * 150)
    say(fmt(WF[["panel", "arm", "pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                "anchor_OOS_Sharpe", "best", "best_OOS_Sharpe", "regret", "v2_OOS_Sharpe",
                "spy_OOS_Sharpe"]]))
    say(f"\n  IS chooser beats its TOP20 anchor OOS in {int(WF.beat_anchor.sum())}/{len(WF)}; "
        f"beats SPY OOS in {int(WF.beat_spy.sum())}/{len(WF)}; "
        f"beats RULES v2 OOS in {int(WF.beat_v2.sum())}/{len(WF)}; "
        f"mean regret {WF.regret.mean():+.4f}")
    say("  IS pick distribution: " + ", ".join(f"{k} {v}" for k, v in WF.pick.value_counts().items()))
    say("  OOS-best distribution: " + ", ".join(f"{k} {v}" for k, v in WF.best.value_counts().items()))

    say("\n" + "=" * 150)
    say("[E2] IDEA 124's ORDERING CLAUSE, re-tested on MEASURED width (not the nominal dial)")
    say("=" * 150)
    say(fmt(OR[["panel", "book", "nominal", "names", "band", "nom_band",
                "n_priced_both", "spearman_IS_OOS"]]))
    say("\n  mean spearman(IS rate list, OOS rate list) pooled by MEASURED width band:")
    say(OR.groupby("band").spearman_IS_OOS.agg(["count", "mean", "median"])
        .to_string(float_format=lambda x: f"{x:+.4f}"))
    say("\n  the same pooled by the NOMINAL band (what the record would have said):")
    say(OR.groupby("nom_band").spearman_IS_OOS.agg(["count", "mean", "median"])
        .to_string(float_format=lambda x: f"{x:+.4f}"))
    say(f"\n  rows whose band CHANGES when nominal is replaced by measured: "
        f"{int((OR.band != OR.nom_band).sum())} of {len(OR)}")

    say("\n" + "=" * 150)
    say(f"done in {time.time()-t0:.0f}s")
    say("=" * 150)
    (Path(f"{OUT}.console.txt")).write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
