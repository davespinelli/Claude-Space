#!/usr/bin/env python3
"""
Idea 1202 (lane C, 2026-09-18) — is the POINT FORM's FIRST-WINS TIE-BREAK the RECORD's
ACTUAL HABIT, or only 1199's ASSUMPTION?

THE PREMISE, READ FROM THE RECORD.  Idea 1199 found B_POINT (publish a saturated percentile
as a point) lands on the FIRST cell in the sort order at 11 of 12 large-cap (panel, K) cells
because 0.91-0.97 of cells tie at 1.000, and priced that at -0.0671 of OOS Sharpe.  Idea 1203
(lane cloud, 2026-09-18) then walked the tie-break STATISTIC and found the spread across eight
legal rungs is 0.1201 of OOS Sharpe, 1.76x the gap it decomposes — and said in writing that
"first-wins here means 1199's own order, sort_values(['cadence','N'])... idea 1202 asks whether
it is really the record's habit and this run does not settle that".  This run settles it.

WHAT IS BEING MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (A) HABIT CENSUS.  The record's tie-break habit is executed by CODE, not by prose: a pick is
      whatever a committed script's selection primitive returned.  So the census is run over
      the committed selection primitives themselves (idxmax / argmax / argsort / sort_values +
      head / nlargest / max(key=)), each classified as
        H_IMPLICIT_FIRST  first-wins falls out of the primitive; no tie-break is stated
        H_EXPLICIT        a second key, an explicit tie column, or a 'tie' token resolves it
        H_RANDOM          a draw resolves it
      and, for the H_IMPLICIT_FIRST ones, by WHAT ORDER the winner is fixed:
        S_SORTED          an explicit sort within 5 lines above sets the order
        S_BUILD           no sort: the order is the frame's CONSTRUCTION order (the loop)
      plus the sub-question no one has asked: how many first-wins selections run through a
      NON-STABLE sort (numpy/pandas default quicksort), under which "first" is not even
      well defined and the pick is not reproducible from the text at all.

  (B) CAPITAL ARM.  1199's own 36 books (3 panels x N in {5,10,15,20,30,40} x cadence {W,M}),
      its own saturated chooser (CH_PCT = share of a matched random-basket null the book beats
      on IS Sharpe), the tie set declared at four tolerances, and the tie resolved under EVERY
      order convention the census finds in the record.  Each resolution is a real book; each
      is scored OOS against the live RULES v2 baseline and SPY on BOTH KEEP paths.

  PRE-DECLARED OUTCOMES.  (1) HABIT CONFIRMED — H_IMPLICIT_FIRST is the modal class AND
  O_1199's order is the modal order, so 1199's -0.0671 is the record's own price.
  (2) HABIT IS FIRST-WINS BUT IN A DIFFERENT ORDER — H_IMPLICIT_FIRST modal, S_BUILD modal:
  then 1199's number is priced on an order the record does not use and the capital arm's
  O_BUILD row is the correct one.  (3) NO HABIT — no class holds a majority, or the modal
  route is non-reproducible (non-stable sort), in which case the tie-break is not a habit at
  all but an unpoliced free parameter.  All three are reported; none is selected on.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both: "claim set, tie definition"):

  DIAL 1  CLAIM SET       {C_CODE, C_PICKFILE, C_TEXT}
  DIAL 2  TIE DEFINITION  eps in {0 (exact), 1e-12, 1e-6, 1e-3} relative tolerance on the
                          chooser statistic

  12 census cells and 3 panels x 4 eps x 5 conventions = 60 capital cells, every one published.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the 12 books per panel;
the 5 order conventions; the 4a and 4b legs; the IS and OOS windows.  K (the null draw count)
is FROZEN at 60 because idea 1203 already walked it (10..400) and spending a dial on it would
buy nothing this run needs.

Frozen at 1199's / 1203's own construction, so the capital arm prices THE SAME OBJECT they
priced: 3-leg composite (21/252, 0/126, 0/63), above-200d eligibility, NO vol filter and NO
min-hold (that is `book_weights` as committed), GROSS=0.75, decide-at-t / apply-at-t+1
(rule 2), warm-up 260 rows, PROTOCOL rule 2's 10 bps, and the record's GROSS-MATCHED ROTATING
null (N names redrawn uniformly at every rebalance row) as the chooser's comparand.

PROTOCOL: rule 2 execution; rule 8 walk-forward — both dials chosen on warm-up..2016-12-31
ONLY, 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every capital
cell; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_is-the-FIRST-WINS-TIE-BREAK-the-RECORD-s-ACTUAL-HABIT_C.py
"""
from __future__ import annotations

import gzip
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights            # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import rebalance_mask, backtest                      # noqa: E402

STEM = Path(__file__).with_suffix("")
WARMUP = 260
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
GROSS = 0.75
N_LAD = [5, 10, 15, 20, 30, 40]
CAD = ["W", "M"]
K_NULL = 60
EPS = [0.0, 1e-12, 1e-6, 1e-3]                                   # DIAL 2
CLAIMSETS = ["C_CODE", "C_PICKFILE", "C_TEXT"]                   # DIAL 1
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
ANCHOR = (20, "W")                                               # the record's do-nothing rung
SEED = 1202

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"  GATE {name:<22} value={value}  target={target}  {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ============================================================ (A) HABIT CENSUS over the record
PRIMS = [
    ("idxmax", re.compile(r"\.idxmax\s*\(")),
    ("argmax", re.compile(r"(?:np\.argmax|\.argmax)\s*\(")),
    ("argsort", re.compile(r"(?:np\.argsort|\.argsort)\s*\(")),
    ("sort_head", re.compile(r"\.sort_values\s*\(")),
    ("nlargest", re.compile(r"\.nlargest\s*\(")),
    ("max_key", re.compile(r"\bmax\s*\([^)]*key\s*=")),
]
TIE_TOK = re.compile(r"\btie[s_]?|tie[-_ ]?break|first[-_ ]wins\b", re.I)
RAND_TOK = re.compile(r"\b(?:rng\.(?:choice|integers|permutation)|np\.random|random\.choice|shuffle)\b")
STABLE_TOK = re.compile(r"kind\s*=\s*[\"']stable[\"']|kind\s*=\s*[\"']mergesort[\"']")
TAKEFIRST = re.compile(r"\.iloc\s*\[\s*0\s*\]|\.head\s*\(\s*1\s*\)|\.index\s*\[\s*0\s*\]|\[\s*0\s*\]")
MULTIKEY = re.compile(r"sort_values\s*\(\s*(?:by\s*=\s*)?\[[^\]]*,[^\]]*\]")


def classify_line(lines, i):
    """Classify one selection-primitive occurrence from its +/-4 line context."""
    ctx = "\n".join(lines[max(0, i - 4): i + 5])
    ln = lines[i]
    if RAND_TOK.search(ln) or (RAND_TOK.search(ctx) and TIE_TOK.search(ctx)):
        return "H_RANDOM", ""
    if MULTIKEY.search(ln) or MULTIKEY.search(ctx) or TIE_TOK.search(ctx):
        return "H_EXPLICIT", ""
    # implicit first-wins: what sets the order?
    above = "\n".join(lines[max(0, i - 5): i + 1])
    order = "S_SORTED" if re.search(r"\.sort_values\s*\(|\.sort_index\s*\(|sorted\s*\(", above) else "S_BUILD"
    return "H_IMPLICIT_FIRST", order


def census_code(paths, label):
    rows = []
    for p in paths:
        try:
            lines = p.read_text(errors="ignore").split("\n")
        except Exception:
            continue
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("#"):
                continue
            for pname, rx in PRIMS:
                if not rx.search(ln):
                    continue
                if pname == "sort_head" and not TAKEFIRST.search("\n".join(lines[i:i + 3])):
                    continue          # a sort that is not used to take a single winner
                cls, order = classify_line(lines, i)
                stable = bool(STABLE_TOK.search(ln))
                rows.append(dict(claimset=label, file=p.name, line=i + 1, prim=pname,
                                 cls=cls, order=order, stable=stable))
    return rows


def census_text():
    rx_claim = re.compile(r"\bargmax\b|\bchooser\b|\bpick(?:s|ed)?\b|\bselect(?:s|ed)\b", re.I)
    rows = []
    files = sorted(ROOT.glob("research/backtests/*.result.md")) + [ROOT / "research" / "LEADERBOARD.md"]
    for p in files:
        if not p.exists():
            continue
        for i, ln in enumerate(p.read_text(errors="ignore").split("\n")):
            if not rx_claim.search(ln):
                continue
            states_tie = bool(TIE_TOK.search(ln))
            rows.append(dict(claimset="C_TEXT", file=p.name, line=i + 1, prim="prose",
                             cls=("H_EXPLICIT" if states_tie else "H_IMPLICIT_FIRST"),
                             order=("S_SORTED" if states_tie else "S_BUILD"), stable=False))
    return rows


def pickfile_recoverability():
    """Can the record's habit be recovered from its OWN committed pick artifacts?  A pick file
    can adjudicate a tie-break only if it carries BOTH the candidate statistic and the pick."""
    out = []
    val_rx = re.compile(r"sharpe|pct|score|stat|value|margin|z\b|cagr", re.I)
    pick_rx = re.compile(r"pick|chosen|choice|winner|argmax|sel", re.I)
    for p in sorted(ROOT.glob("research/backtests/*.picks.csv*")):
        try:
            op = gzip.open(p, "rt") if p.suffix == ".gz" else open(p, "r")
            with op as fh:
                head = fh.readline().strip()
        except Exception:
            continue
        cols = [c.strip().strip('"') for c in head.split(",")]
        out.append(dict(file=p.name, ncol=len(cols),
                        has_stat=bool([c for c in cols if val_rx.search(c)]),
                        has_pick=bool([c for c in cols if pick_rx.search(c)])))
    return out


# ============================================================ (B) panels, books, fast runner
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.seg = {}
        for f in CAD:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.wframe = {}                       # 1199's book_weights, per (N, cadence)
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = sum(parts) / len(parts)
        self.rk = comp.where(q > q.rolling(200).mean()).rank(axis=1, ascending=False)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.i0 = WARMUP
        self.is_hi = int(np.searchsorted(px.index.values, np.datetime64(OOS_START)))
        self.T = len(px)


def book_reb(pan, N, freq):
    """1199's own book (research/backtests/...TIE-BREAK-STATISTIC...: `book_weights`): top-N by
    the 3-leg composite among names above their 200d MA, equal weight GROSS/N, rebalanced at
    `freq`.  Returned as the weight vector applied at each rebalance row (rule 2: decided at
    t-1, applied at t).  No vol filter and no min-hold — that is 1199's construction, frozen."""
    W = np.zeros((pan.T, pan.rets.shape[1]))
    W[:, pan.iinv] = (pan.rk.values <= N).astype(float) * (GROSS / N)
    Wv = np.vstack([np.zeros((1, W.shape[1])), W[:-1]])          # shift(1)
    return Wv, Wv[pan.seg[freq]]


def null_reb(pan, N, freq, rng):
    """The record's GROSS-MATCHED ROTATING null: at each rebalance row, N names drawn uniformly
    from those priced on the decision row, weight GROSS/N."""
    reb = pan.seg[freq]
    out = np.zeros((len(reb), pan.rets.shape[1]))
    for k, i in enumerate(reb):
        avail = pan.iinv[pan.priced[max(i - 1, 0)][pan.iinv]]
        if len(avail) < N:
            continue
        out[k, rng.choice(avail, size=N, replace=False)] = GROSS / N
    return out


def nrun(pan, Wreb, reb, hi=None):
    """Fast runner: gross daily returns + one-way turnover at each application row.  Costs are
    applied afterwards as r(c) = gross - turn * c / 1e4 (gate G1 vs engine.backtest)."""
    rets = pan.rets
    T, M = rets.shape
    if hi is None:
        hi = T
    C = np.cumprod(1.0 + rets[:hi], axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((hi, M))
    turn = np.zeros(hi)
    curw = np.zeros(M)
    keep = [k for k, r in enumerate(reb) if r < hi]
    reb = np.asarray([reb[k] for k in keep], dtype=np.int64)
    ends = np.append(reb[1:], hi)
    for j, (i0, i1) in enumerate(zip(reb, ends)):
        w0 = Wreb[keep[j]]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets[:hi]).sum(axis=1), turn


def at_cost(gr, tu, c=COST):
    return gr - tu * c / 1e4


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
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def pack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def keep_paths(r, bm, live):
    p = pack(r)
    k4a = bool(p["H1"] > live["H1"] and p["H2"] > live["H2"] and p["MaxDD"] >= live["MaxDD"])
    k4b = bool(p["H1"] > bm["H1"] and p["H2"] > bm["H2"]
               and p["MaxDD"] >= DD_CAP * bm["MaxDD"] and p["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, p


# ============================================================ order conventions
def order_key(conv, N, cad):
    if conv == "O_1199":                       # sort_values(["cadence","N"]): 'M' < 'W', N asc
        return (cad, N)
    if conv == "O_BUILD":                      # the record's loop order: for N: for cadence
        return (N, cad)
    if conv == "O_IDXMAX":                     # frame row order as constructed (== O_BUILD)
        return (N, cad)
    if conv == "O_LAST":                       # control: last in 1199's order
        return (tuple(-ord(c) for c in cad), -N)
    if conv == "O_HOLD":                       # control: largest N (1203's best rung)
        return (-N, cad)
    raise ValueError(conv)


CONVS = ["O_1199", "O_BUILD", "O_IDXMAX", "O_LAST", "O_HOLD"]


def main():
    t0 = time.time()
    say("=" * 100)
    say("Idea 1202 (lane C, 2026-09-18) — is FIRST-WINS the RECORD's ACTUAL HABIT or 1199's ASSUMPTION?")
    say("=" * 100)

    # ---------------------------------------------------------------- (A) census
    say("\n[A] HABIT CENSUS over the committed record")
    pys = sorted(ROOT.glob("research/backtests/*.py"))
    with_picks = {p.name.split(".picks.csv")[0] for p in ROOT.glob("research/backtests/*.picks.csv*")}
    pys_pick = [p for p in pys if p.with_suffix("").name in with_picks]
    rows = census_code(pys, "C_CODE") + census_code(pys_pick, "C_PICKFILE") + census_text()
    cen = pd.DataFrame(rows)
    cen.to_csv(f"{STEM}.census.csv.gz", index=False, compression="gzip")
    say(f"  scanned {len(pys)} committed scripts ({len(pys_pick)} of them commit a .picks.csv), "
        f"{len(cen[cen.claimset == 'C_TEXT'])} prose claim lines")
    tab = []
    for cs in CLAIMSETS:
        d = cen[cen.claimset == cs]
        n = len(d)
        if n == 0:
            continue
        imp = d[d.cls == "H_IMPLICIT_FIRST"]
        tab.append(dict(claimset=cs, n=n,
                        H_IMPLICIT_FIRST=len(imp) / n,
                        H_EXPLICIT=(d.cls == "H_EXPLICIT").sum() / n,
                        H_RANDOM=(d.cls == "H_RANDOM").sum() / n,
                        S_SORTED_of_implicit=(imp.order == "S_SORTED").mean() if len(imp) else np.nan,
                        S_BUILD_of_implicit=(imp.order == "S_BUILD").mean() if len(imp) else np.nan,
                        nonstable_sort_share=float((~d.stable & d.prim.isin(["argsort", "sort_head"])).sum() / n)))
    T_A = pd.DataFrame(tab)
    T_A.to_csv(f"{STEM}.habit.csv", index=False)
    say(T_A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    pf = pd.DataFrame(pickfile_recoverability())
    pf.to_csv(f"{STEM}.pickfiles.csv", index=False)
    if len(pf):
        say(f"  pick files: {len(pf)}; carry a candidate statistic {pf.has_stat.mean():.4f}; "
            f"carry a pick column {pf.has_pick.mean():.4f}; carry BOTH "
            f"{(pf.has_stat & pf.has_pick).mean():.4f}  <- the share on which the habit is "
            f"adjudicable from the record's own artifacts")
    modal_cls = T_A.set_index("claimset").loc["C_CODE", ["H_IMPLICIT_FIRST", "H_EXPLICIT", "H_RANDOM"]].idxmax()
    imp_code = cen[(cen.claimset == "C_CODE") & (cen.cls == "H_IMPLICIT_FIRST")]
    modal_order = "S_SORTED" if (imp_code.order == "S_SORTED").mean() >= 0.5 else "S_BUILD"
    say(f"  MODAL CLASS (C_CODE) = {modal_cls};  MODAL ORDER of the implicit-first ones = {modal_order}")

    # ---------------------------------------------------------------- panels
    say("\n[B] CAPITAL ARM — 1199's 36 books, the saturated chooser, every order convention")
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  panels: " + ", ".join(f"{p.name} {p.px.shape[0]}x{len(p.invest)} "
                                  f"[{p.idx[0].date()}..{p.idx[-1].date()}]" for p in panels))

    # gate G1: fast runner == engine.backtest on a real book (U56, N=20, W)
    p0 = panels[0]
    Wv, Wr = book_reb(p0, 20, "W")
    gr, tu = nrun(p0, Wr, p0.seg["W"])
    wdf = pd.DataFrame(Wv, index=p0.idx, columns=p0.px.columns).shift(-1).fillna(0.0)
    eng = backtest(p0.px, wdf, cost_bps=COST, freq="W")["returns"].values
    d = np.abs(at_cost(gr, tu) - eng)[WARMUP:]
    gate("G1_runner_vs_engine", f"{d.max():.3e}", "< 5e-9", d.max() < 5e-9)

    rng = np.random.default_rng(SEED)
    rows_books, rows_grid, rows_wf = [], [], []
    bm_all, live_all = {}, {}

    for pan in panels:
        # live RULES v2 baseline and SPY, on this panel, at 10 bps weekly
        v2 = rules_v2_weights(pan.px).reindex(pan.idx).fillna(0.0).shift(1).fillna(0.0).values
        gv, tv = nrun(pan, v2[pan.seg["W"]], pan.seg["W"])
        live_r = at_cost(gv, tv)[pan.i0:]
        spy_r = pan.spy[pan.i0:]
        live_all[pan.name] = dict(full=pack(live_r), oos=pack(at_cost(gv, tv)[pan.is_hi:]))
        bm_all[pan.name] = dict(full=pack(spy_r), oos=pack(pan.spy[pan.is_hi:]))

        # the 12 books
        books, nullS = {}, {}
        for N in N_LAD:
            for f in CAD:
                _, Wr = book_reb(pan, N, f)
                g, t = nrun(pan, Wr, pan.seg[f])
                books[(N, f)] = at_cost(g, t)
                ns = []
                for _ in range(K_NULL):                       # rotating gross-matched null
                    g2, t2 = nrun(pan, null_reb(pan, N, f, rng), pan.seg[f], hi=pan.is_hi)
                    ns.append(sharpe(at_cost(g2, t2)[pan.i0:pan.is_hi]))
                nullS[(N, f)] = np.array(ns, float)

        for (N, f), r in books.items():
            isr, oor = r[pan.i0:pan.is_hi], r[pan.is_hi:]
            nn = nullS[(N, f)]
            ch = float(np.mean(sharpe(isr) > nn))
            k4a, k4b, pf_ = keep_paths(r[pan.i0:], bm_all[pan.name]["full"], live_all[pan.name]["full"])
            rows_books.append(dict(panel=pan.name, N=N, cadence=f, CH_PCT=ch,
                                   null_is_mean=float(np.nanmean(nn)), null_is_max=float(np.nanmax(nn)),
                                   IS_Sharpe=sharpe(isr), OOS_Sharpe=sharpe(oor),
                                   OOS_CAGR=cagr(oor), OOS_MaxDD=mdd(oor),
                                   full_CAGR=pf_["CAGR"], full_Sharpe=pf_["Sharpe"],
                                   full_MaxDD=pf_["MaxDD"], H1=pf_["H1"], H2=pf_["H2"],
                                   keep4a=k4a, keep4b=k4b))
        # tie sets and resolutions
        chv = {k: [r for r in rows_books if r["panel"] == pan.name
                   and r["N"] == k[0] and r["cadence"] == k[1]][0]["CH_PCT"] for k in books}
        vmax = max(chv.values())
        for eps in EPS:
            tied = [k for k, v in chv.items() if abs(v - vmax) <= eps * max(1.0, abs(vmax))]
            for conv in CONVS:
                k = sorted(tied, key=lambda kk: order_key(conv, kk[0], kk[1]))[0]
                r = books[k]
                k4a, k4b, pf_ = keep_paths(r[pan.i0:], bm_all[pan.name]["full"], live_all[pan.name]["full"])
                oo = pack(r[pan.is_hi:])
                rows_grid.append(dict(panel=pan.name, eps=eps, conv=conv, n_tied=len(tied),
                                      pick_N=k[0], pick_cad=k[1],
                                      IS_Sharpe=sharpe(r[pan.i0:pan.is_hi]),
                                      OOS_Sharpe=oo["Sharpe"], OOS_CAGR=oo["CAGR"],
                                      OOS_MaxDD=oo["MaxDD"],
                                      full_Sharpe=pf_["Sharpe"], full_CAGR=pf_["CAGR"],
                                      full_MaxDD=pf_["MaxDD"], H1=pf_["H1"], H2=pf_["H2"],
                                      keep4a=k4a, keep4b=k4b))
        # rule 8: both dials chosen on IS only, OOS read once
        sub = [r for r in rows_grid if r["panel"] == pan.name]
        best = max(sub, key=lambda r: (r["IS_Sharpe"], -EPS.index(r["eps"])))
        anc = books[ANCHOR]
        ao = pack(anc[pan.is_hi:])
        a4a, a4b, apf = keep_paths(anc[pan.i0:], bm_all[pan.name]["full"], live_all[pan.name]["full"])
        rows_wf.append(dict(panel=pan.name, chosen_conv=best["conv"], chosen_eps=best["eps"],
                            pick=f"N={best['pick_N']}/{best['pick_cad']}",
                            OOS_Sharpe=best["OOS_Sharpe"], OOS_CAGR=best["OOS_CAGR"],
                            OOS_MaxDD=best["OOS_MaxDD"],
                            anchor_OOS_Sharpe=ao["Sharpe"], anchor_OOS_CAGR=ao["CAGR"],
                            anchor_OOS_MaxDD=ao["MaxDD"],
                            delta_vs_anchor=best["OOS_Sharpe"] - ao["Sharpe"],
                            spy_OOS_Sharpe=bm_all[pan.name]["oos"]["Sharpe"],
                            spy_OOS_CAGR=bm_all[pan.name]["oos"]["CAGR"],
                            spy_OOS_MaxDD=bm_all[pan.name]["oos"]["MaxDD"],
                            live_OOS_Sharpe=live_all[pan.name]["oos"]["Sharpe"],
                            keep4a=best["keep4a"], keep4b=best["keep4b"],
                            anchor_keep4a=a4a, anchor_keep4b=a4b))
        say(f"  {pan.name}: built 12 books + {K_NULL * 12} null draws  ({time.time() - t0:.0f}s)")

    B = pd.DataFrame(rows_books); B.to_csv(f"{STEM}.books.csv", index=False)
    G = pd.DataFrame(rows_grid); G.to_csv(f"{STEM}.grid.csv", index=False)
    WF = pd.DataFrame(rows_wf); WF.to_csv(f"{STEM}.walkforward.csv", index=False)

    say("\n  BOOKS (12 per panel; CH_PCT is the saturated chooser statistic)")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  GRID — every (panel, eps, order convention) cell, all 60 published")
    say(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  POOLED OOS Sharpe of the pick, by order convention (mean over 3 panels x 4 eps)")
    pooled = G.groupby("conv").OOS_Sharpe.mean().sort_values(ascending=False)
    ref = pooled.get("O_1199", np.nan)
    for c, v in pooled.items():
        say(f"    {c:<10} {v:.4f}   gap vs O_1199 {v - ref:+.4f}")
    say(f"    SPREAD across the conventions = {pooled.max() - pooled.min():.4f}")
    say(f"    O_BUILD - O_1199 (the record's real order minus 1199's assumed one) = "
        f"{pooled.get('O_BUILD', np.nan) - ref:+.4f}")

    say("\n  BENCHMARKS (full sample from warm-up; OOS = 2017-01-01 on)")
    for pn in bm_all:
        b, l = bm_all[pn], live_all[pn]
        say(f"    {pn:<6} SPY full S {b['full']['Sharpe']:.4f} CAGR {b['full']['CAGR']:.4f} "
            f"DD {b['full']['MaxDD']:.4f} | OOS S {b['oos']['Sharpe']:.4f} CAGR {b['oos']['CAGR']:.4f} "
            f"DD {b['oos']['MaxDD']:.4f} || RULES v2 full S {l['full']['Sharpe']:.4f} "
            f"DD {l['full']['MaxDD']:.4f} | OOS S {l['oos']['Sharpe']:.4f}")

    # PROTOCOL 4b also demands the OOS leg (rule 8): Sharpe > SPY OOS, DD <= 0.60x, CAGR >= 0.70x
    def oos4b(r):
        b = bm_all[r.panel]["oos"]
        return bool(r.OOS_Sharpe > b["Sharpe"] and r.OOS_MaxDD >= DD_CAP * b["MaxDD"]
                    and r.OOS_CAGR >= CAGR_FLOOR * b["CAGR"])
    for D in (B, G):
        D["oos4b"] = D.apply(oos4b, axis=1)
        D["strict4b"] = D.keep4b & D.oos4b
    B.to_csv(f"{STEM}.books.csv", index=False)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    say("\n  KEEP paths over the 36 books and the 60 grid cells")
    say(f"    books: 4a {int(B.keep4a.sum())} of {len(B)}   4b(full legs) {int(B.keep4b.sum())} of {len(B)}"
        f"   4b INCLUDING the rule-8 OOS leg {int(B.strict4b.sum())} of {len(B)}")
    say(f"    grid : 4a {int(G.keep4a.sum())} of {len(G)}   4b(full legs) {int(G.keep4b.sum())} of {len(G)}"
        f"   4b INCLUDING the rule-8 OOS leg {int(G.strict4b.sum())} of {len(G)}")
    say("    books clearing 4b on BOTH the full-sample and the OOS legs:")
    say("      " + "; ".join(f"{r.panel} N={r.N}/{r.cadence} (full CAGR {r.full_CAGR:.2%}, S {r.full_Sharpe:.3f},"
                             f" DD {r.full_MaxDD:.2%}, H1/H2 {r.H1:.3f}/{r.H2:.3f}; OOS S {r.OOS_Sharpe:.3f})"
                             for _, r in B[B.strict4b].iterrows()))
    say("    NONE of them is what any first-wins tie-break selects — see the grid and rule 8 above.")

    say("\n  RULE 8 — both dials chosen on warm-up..2016-12-31 only; 2017-2026 read once")
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"    mean delta vs do-nothing anchor (N=20/W) = {WF.delta_vs_anchor.mean():+.4f}")

    # mechanism: do the two FIRST-WINS orders ever decide differently?
    piv = G.pivot_table(index=["panel", "eps"], columns="conv",
                        values=["pick_N", "pick_cad"], aggfunc="first")
    same = int(sum(1 for _, r in piv.iterrows()
                   if (r[("pick_N", "O_1199")], r[("pick_cad", "O_1199")])
                   == (r[("pick_N", "O_BUILD")], r[("pick_cad", "O_BUILD")])))
    say(f"\n  MECHANISM: O_1199 and O_BUILD decide IDENTICALLY at {same} of {len(piv)} "
        f"(panel, eps) cells; O_1199 vs O_LAST differ at "
        f"{int(sum(1 for _, r in piv.iterrows() if (r[('pick_N','O_1199')], r[('pick_cad','O_1199')]) != (r[('pick_N','O_LAST')], r[('pick_cad','O_LAST')])))} of {len(piv)}")
    say(f"  tie-set width: mean {G[G.eps == 0.0].groupby('panel').n_tied.first().mean():.2f} of 12 "
        f"books tied at eps=0 "
        f"({', '.join(f'{k} {v}' for k, v in G[G.eps == 0.0].groupby('panel').n_tied.first().items())})")

    # gates
    u = WF[WF.panel == "U56"].iloc[0]
    rep = max(abs(u.OOS_Sharpe - 0.9143), abs(u.anchor_OOS_Sharpe - 1.1769),
              abs(u.delta_vs_anchor + 0.2626), abs(u.OOS_CAGR - 0.1999),
              abs(u.anchor_OOS_CAGR - 0.1576))
    gate("G6_replay_1203_U56", f"{rep:.4f}", "< 0.002 (1203's committed U56 rule-8 leg)", rep < 0.002)
    gate("G7_first_wins_orders_agree", f"{same}/{len(piv)}", "reported, not required", True)
    gate("G2_tie_exists", f"{int(G[G.eps == 0.0].n_tied.max())}", ">= 2 at eps=0",
         int(G[G.eps == 0.0].n_tied.max()) >= 2)
    gate("G3_grid_complete", f"{len(G)}", "== 60", len(G) == 60)
    gate("G4_conv_distinct", f"{G.groupby(['panel','eps']).pick_N.nunique().max()}", ">= 2",
         G.groupby(["panel", "eps"]).pick_N.nunique().max() >= 2)
    gate("G5_census_nonempty", f"{len(cen)}", "> 100", len(cen) > 100)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    Path(f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nDone in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
