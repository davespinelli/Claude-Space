#!/usr/bin/env python3
"""
Idea 1215 (lane C, 2026-09-18) — how many committed CENSUS HEADLINES in the record have
NEVER BEEN TRACED TO A VERDICT?

THE PREMISE, READ FROM THE RECORD.  Idea 1207 traced 1155's "36 failures" to ZERO verdict
changes.  Idea 1209 traced its own widest-dial shift to 3 of 36, then 0 at t+1.  Both
headlines had stood in the record as ALARMS — a published fraction of the form "N of M
committed claims fail X" — and both, when someone finally followed them to the verdicts
they implicate, moved nothing.  The queue asks for the base rate: of every such headline the
record has committed, how many were EVER followed, and how many SURVIVED being followed.

WHAT IS BEING MEASURED, STATED BEFORE ANY NUMBER IS READ.

  ARM A (the census the queue asks for).  Over every committed unit under research/
  (LEADERBOARD.md rows, CHANGELOG.md paragraphs, every research/backtests/**/*.md paragraph):

     HEADLINES  H = units containing "<n> of <m>" in a failure frame (see the three
                HEADLINE SETs below).
     TRACED     a headline from idea i is TRACED iff a STRICTLY LATER committed unit both
                (a) points back at it (by idea number, or by quoting its exact fraction)
                and (b) carries a VERDICT-FOLLOW phrase — a verdict/KEEP/KILL/PARK/4a/4b
                token within 120 characters of a change-or-no-change token.
     SURVIVED   of the traced headlines, those whose tracing text reports a NON-ZERO
                verdict move ("3 of 36 changed"), against those reporting ZERO
                ("zero verdict changes", "none", "unchanged").  Ties/both -> AMBIGUOUS.

  PRE-DECLARED OUTCOMES for the reference cell (H_STRICT x T_IDNUM), fixed before the run:
     (A) MOSTLY UNTRACED   traced share <  0.25
     (B) PARTLY TRACED     0.25 <= traced share < 0.60
     (C) MOSTLY TRACED     traced share >= 0.60
  and, independently, SURVIVAL = non-zero share among the traced.  Both are reported at all
  nine cells; the verdict is read at the reference cell only.

  ARM B (the capital arm; PROTOCOL rule 3/4/8).  A census fraction is a bookkeeping object
  until someone prices what it implicates, so this run also builds the CAPITAL-DOMAIN
  version of the same base rate.  198 REAL BOOKS (3 panels x 6 N x 11 gross), both KEEP
  paths at every cell, and then: an ALARM is a cell whose IN-SAMPLE joint 4b margin sits
  within a band of zero (the thin-margin alarm the record publishes constantly); FOLLOWING
  it means reading the SAME cell out of sample.  The question ARM A asks of text is asked of
  money: does following a thin-margin alarm to its out-of-sample verdict change anything?

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  HEADLINE SET  {H_STRICT, H_LOOSE, H_NUM}   which "<n> of <m>" counts as a census headline
  TRACE RULE    {T_IDNUM, T_FRAC, T_ANY}     what counts as having followed it

  9 cells, every one published in `.trace.csv`.  ARM B's grid is NOT a third and fourth dial:
  N and GROSS are the record's own two published axes and ARM B is reported at EVERY one of
  its 66 cells per panel, never argmaxed except by the frozen rule-8 chooser below.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the alarm band
{0.5, 1.0, 2.0} pp; the 4a and 4b legs; the IS and OOS windows.

FROZEN, NEVER TUNED HERE (the incumbent's construction): H = 126 min hold, weekly cadence,
decide-at-t / apply-at-t+1 (rule 2), 10 bps (rule 2), above-200d eligibility with
vol20 < 0.60, 3-leg composite (21/252, 0/126, 0/63), equal weights, 260-row warm-up.  The
rule-8 chooser is idea 1294's, inherited verbatim and not re-tuned: among cells clearing the
IN-SAMPLE 4b-analogue legs, highest IS joint margin J = min(DD margin, CAGR margin), ties to
lower gross then lower N.

PROTOCOL: rule 2 execution; rule 8 walk-forward with both dials chosen on warm-up..2016-12-31
ONLY and 2017-2026 read ONCE; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) at every one
of the 198 cells and on every rule-8 row; rule 9 survivorship stated.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_how-many-committed-CENSUS-HEADLINES-have-NEVER-BEEN-TRACED-TO-A-VERDICT_C.py
"""
from __future__ import annotations

import hashlib
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

DATE = "2026-09-18"
SLUG = "how-many-committed-CENSUS-HEADLINES-have-NEVER-BEEN-TRACED-TO-A-VERDICT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_H, A_FREQ = 126, "W"
NS = [5, 10, 15, 20, 25, 30]
GROSSES = [round(0.30 + 0.05 * i, 2) for i in range(11)]        # 0.30 .. 0.80
BANDS = [0.5, 1.0, 2.0]                                          # pp, all published
HEADLINE_SETS = ["H_STRICT", "H_LOOSE", "H_NUM"]                 # DIAL 1
TRACE_RULES = ["T_IDNUM", "T_FRAC", "T_ANY"]                     # DIAL 2
REF_CELL = ("H_STRICT", "T_IDNUM")

# committed anchors replayed as gates (idea 1290/1294's published U56 books)
ANCHORS = {
    (20, 0.75): dict(CAGR=0.1579, Sharpe=1.1529, MaxDD=-0.1913, oCAGR=0.1730, oSharpe=1.1837),
    (20, 0.65): dict(CAGR=0.1366, Sharpe=1.1526, MaxDD=-0.1673, oCAGR=0.1495, oSharpe=1.1833),
    (15, 0.60): dict(CAGR=0.1367, Sharpe=1.1712, MaxDD=-0.1638, oCAGR=0.1514, oSharpe=1.1952),
}
LIVE_MAXDD_COMMITTED = -0.1205

LOG = []
GATES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, PASS=bool(ok)))
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} (target {target})")


# ============================================================ ARM A: the record's own text
DATE_R = re.compile(r"(20\d\d-\d\d-\d\d)")
IDEA_R = re.compile(r"\bidea[s]?\s+(\d{2,4})\b", re.I)
LBIDEA_R = re.compile(r"^\|\s*20\d\d-\d\d-\d\d\s*\|\s*(\d{2,4})\b")
PAIR_R = re.compile(r"\b(\d[\d,]{0,6})\s+of\s+(\d[\d,]{0,6})\b")
FAIL_R = re.compile(
    r"\b(fail\w*|miss\w*|lack\w*|omit\w*|never|unstated|untraced|unresolved|silent|stale|"
    r"wrong|broke\w*|broken|violat\w*|short of|below|do not|does not|don't|doesn't|"
    r"no longer|without)\b", re.I)
COMMITTED_R = re.compile(r"\b(committed|claim\w*|unit\w*|row\w*|cell\w*|figure\w*|reading\w*)\b",
                         re.I)
VERD_R = re.compile(r"\b(verdict\w*|KEEP|KILL|PARK|4a|4b|pass\w*|fail\w*)\b")
MOVE_R = re.compile(r"\b(chang\w*|mov\w*|flip\w*|unchanged|survive\w*|stood|stand\w*|zero|"
                    r"none|no change|held|hold\w*)\b", re.I)
ZERO_R = re.compile(r"\b(zero|none|not one|unchanged|0 of|no verdict\w*|nothing)\b", re.I)
NONZERO_R = re.compile(r"\b([1-9]\d*) of \d", re.I)

WIN = 160          # characters either side of a pair that count as "the same frame"


def verdict_follow_spans(txt):
    """Spans of text where a verdict token sits within 120 chars of a change token."""
    out = []
    for vm in VERD_R.finditer(txt):
        lo, hi = max(0, vm.start() - 120), min(len(txt), vm.end() + 120)
        w = txt[lo:hi]
        if MOVE_R.search(w):
            out.append(w)
    return out


def load_units():
    """Every committed unit under research/, with its date and its idea number(s)."""
    U = []
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    for ln in lb.split("\n"):
        if ln.startswith("| 20"):
            m = LBIDEA_R.match(ln)
            d = DATE_R.search(ln)
            U.append(dict(src="LEADERBOARD.md", date=d.group(1) if d else None,
                          own=int(m.group(1)) if m else None, txt=ln))
    cl = (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")
    cur_date, cur_own = None, None
    for para in cl.split("\n\n"):
        if not para.strip():
            continue
        d = DATE_R.search(para)
        if d:
            cur_date = d.group(1)
        mi = IDEA_R.search(para)
        if mi:
            cur_own = int(mi.group(1))
        U.append(dict(src="CHANGELOG.md", date=cur_date, own=cur_own, txt=para))
    nmd = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        nmd += 1
        d = DATE_R.search(f.name)
        fdate = d.group(1) if d else None
        body = f.read_text(errors="ignore")
        mi = IDEA_R.search(body)
        fown = int(mi.group(1)) if mi else None
        for para in body.split("\n\n"):
            if para.strip():
                U.append(dict(src=f.name, date=fdate, own=fown, txt=para))
    for u in U:
        u["uid"] = hashlib.sha1((str(u["src"]) + u["txt"]).encode()).hexdigest()[:12]
    return U, nmd


def headline_set(txt, frame):
    """Every '<n> of <m>' in `txt` that qualifies as a census headline under `frame`."""
    out = []
    for m in PAIR_R.finditer(txt):
        lo, hi = max(0, m.start() - WIN), min(len(txt), m.end() + WIN)
        w = txt[lo:hi]
        try:
            n = int(m.group(1).replace(",", "")); d = int(m.group(2).replace(",", ""))
        except ValueError:
            continue
        if d <= 0 or n > d:
            continue
        if frame == "H_STRICT":
            ok = bool(FAIL_R.search(w) and COMMITTED_R.search(w))
        elif frame == "H_LOOSE":
            ok = bool(FAIL_R.search(w))
        else:                                       # H_NUM: failure frame anywhere in the unit
            ok = bool(FAIL_R.search(txt))
        if ok:
            out.append((n, d, w))
    return out


def build_index(U):
    """Inverted indices so tracing is a lookup, not a 2e8-pair scan."""
    by_idea, by_pair, meta = {}, {}, {}
    for k, u in enumerate(U):
        spans = verdict_follow_spans(u["txt"])
        meta[k] = spans
        if not spans:
            continue
        for m in IDEA_R.finditer(u["txt"]):
            by_idea.setdefault(int(m.group(1)), []).append(k)
        for m in PAIR_R.finditer(u["txt"]):
            try:
                key = (int(m.group(1).replace(",", "")), int(m.group(2).replace(",", "")))
            except ValueError:
                continue
            by_pair.setdefault(key, []).append(k)
    return by_idea, by_pair, meta


def later(a, b):
    """unit b is strictly later than unit a."""
    da, db = a["date"], b["date"]
    if da and db and db != da:
        return db > da
    oa, ob = a["own"], b["own"]
    if oa is not None and ob is not None:
        return ob > oa
    return False


def survival(spans):
    z = any(ZERO_R.search(s) for s in spans)
    nz = any(NONZERO_R.search(s) for s in spans)
    if nz and not z:
        return "NONZERO"
    if z and not nz:
        return "ZERO"
    if z and nz:
        return "AMBIGUOUS"
    return "AMBIGUOUS"


def arm_a():
    U, nmd = load_units()
    say(f"ARM A units: {len(U)} committed units "
        f"(LEADERBOARD rows + CHANGELOG paragraphs + {nmd} memo/result .md files)")
    by_idea, by_pair, meta = build_index(U)
    say(f"ARM A index: {len(by_idea)} idea numbers and {len(by_pair)} fractions appear inside a "
        f"verdict-follow frame")

    rows, cells = [], []
    for hs in HEADLINE_SETS:
        heads = []
        for k, u in enumerate(U):
            for (n, d, w) in headline_set(u["txt"], hs):
                heads.append(dict(k=k, uid=u["uid"], src=u["src"], date=u["date"],
                                  own=u["own"], n=n, m=d, frac=f"{n} of {d}",
                                  text=w.replace("\n", " ")[:300]))
        for tr in TRACE_RULES:
            ntr = nsurv = nzero = namb = 0
            for h in heads:
                u = U[h["k"]]
                cands = []
                if tr in ("T_IDNUM", "T_ANY") and u["own"] is not None:
                    cands += by_idea.get(u["own"], [])
                if tr in ("T_FRAC", "T_ANY"):
                    cands += by_pair.get((h["n"], h["m"]), [])
                spans = []
                for c in set(cands):
                    if c == h["k"]:
                        continue
                    if later(u, U[c]):
                        spans += meta[c]
                if spans:
                    ntr += 1
                    s = survival(spans)
                    nsurv += s == "NONZERO"
                    nzero += s == "ZERO"
                    namb += s == "AMBIGUOUS"
                if hs == REF_CELL[0] and tr == REF_CELL[1]:
                    h2 = dict(h); h2.pop("k")
                    h2["TRACED"] = bool(spans)
                    h2["SURVIVAL"] = survival(spans) if spans else ""
                    rows.append(h2)
            share = ntr / len(heads) if heads else np.nan
            cells.append(dict(HEADLINE_SET=hs, TRACE_RULE=tr, headlines=len(heads),
                              traced=ntr, traced_share=share, untraced=len(heads) - ntr,
                              surv_NONZERO=nsurv, surv_ZERO=nzero, surv_AMBIG=namb,
                              nonzero_share_of_traced=(nsurv / ntr if ntr else np.nan)))
    cen = pd.DataFrame(rows)
    grid = pd.DataFrame(cells)
    cen.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    grid.to_csv(f"{OUT}.trace.csv", index=False)
    say("\nARM A — all nine cells (both dials, every grid point published):")
    say(grid.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    r = grid[(grid.HEADLINE_SET == REF_CELL[0]) & (grid.TRACE_RULE == REF_CELL[1])].iloc[0]
    sh = float(r.traced_share)
    ans = "(A) MOSTLY UNTRACED" if sh < 0.25 else ("(B) PARTLY TRACED" if sh < 0.60
                                                   else "(C) MOSTLY TRACED")
    say(f"\nARM A reference cell {REF_CELL}: {int(r.headlines)} headlines, "
        f"{int(r.traced)} traced ({sh:.4f}), {int(r.untraced)} NEVER traced -> {ans}")
    say(f"ARM A survival among the traced: NONZERO {int(r.surv_NONZERO)} / "
        f"ZERO {int(r.surv_ZERO)} / AMBIGUOUS {int(r.surv_AMBIG)}")
    gate("G1 census non-empty", int(r.headlines), "> 100", int(r.headlines) > 100)
    gate("G2 monotone in headline set (STRICT <= LOOSE <= NUM)",
         "|".join(str(int(x)) for x in
                  grid[grid.TRACE_RULE == "T_IDNUM"].sort_values("HEADLINE_SET").headlines),
         "H_STRICT <= H_LOOSE <= H_NUM",
         int(grid[(grid.HEADLINE_SET == "H_STRICT") & (grid.TRACE_RULE == "T_IDNUM")].headlines.iloc[0])
         <= int(grid[(grid.HEADLINE_SET == "H_LOOSE") & (grid.TRACE_RULE == "T_IDNUM")].headlines.iloc[0])
         <= int(grid[(grid.HEADLINE_SET == "H_NUM") & (grid.TRACE_RULE == "T_IDNUM")].headlines.iloc[0]))
    t_i = float(grid[(grid.HEADLINE_SET == "H_STRICT") & (grid.TRACE_RULE == "T_IDNUM")].traced.iloc[0])
    t_a = float(grid[(grid.HEADLINE_SET == "H_STRICT") & (grid.TRACE_RULE == "T_ANY")].traced.iloc[0])
    gate("G3 T_ANY dominates T_IDNUM", f"{t_a:.0f} >= {t_i:.0f}", "T_ANY >= T_IDNUM", t_a >= t_i)
    return grid, cen, ans


# ============================================================ ARM B: the capital arm
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        m = rebalance_mask(px.index, A_FREQ).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.seg = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.i_oos = int(np.searchsorted(px.index.values,
                                         np.datetime64(pd.Timestamp(OOS_START))))


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


def build1(pan, N, H):
    """The record's min-hold selection frame at GROSS = 1.0; decide at t-1, apply at t."""
    reb, T, M = pan.seg, pan.rets.shape[0], pan.rets.shape[1]
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - 1, 0)
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


def nrun(pan, Wt):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.seg
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
    return (held * rets).sum(axis=1), turn


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


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def pack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def legs_4b(m, bm):
    """The five 4b legs and the joint margin J = min(DD margin, CAGR margin), in pp."""
    dd_m = 100.0 * (m["MaxDD"] - DD_CAP * bm["MaxDD"])          # >= 0 passes
    cg_m = 100.0 * (m["CAGR"] - CAGR_FLOOR * bm["CAGR"])        # >= 0 passes
    ok = (m["H1"] > bm["H1"] and m["H2"] > bm["H2"] and dd_m >= 0 and cg_m >= 0)
    return bool(ok), dd_m, cg_m, float(min(dd_m, cg_m))


def keep_4a(m, live):
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


def arm_b():
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"\nARM B panels: U56 {pxU.shape}, B136 {pxB.shape}, SMALL {pxS.shape} "
        f"({len(inv)} investable)")

    rows, wf, alarms, curves = [], [], [], {}
    for pan in panels:
        live_r = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                          freq=A_FREQ)["returns"].fillna(0.0).values
        i0, io = pan.i0, pan.i_oos
        FULL, ISW, OOSW = slice(i0, None), slice(i0, io), slice(io, None)
        bm = {w: pack(pan.spy[s]) for w, s in (("F", FULL), ("I", ISW), ("O", OOSW))}
        live = {w: pack(live_r[s]) for w, s in (("F", FULL), ("I", ISW), ("O", OOSW))}
        curves[pan.name] = dict(spy=bm, live=live)
        say(f"\n  {pan.name}: SPY full {bm['F']['CAGR']:.2%} / {bm['F']['Sharpe']:.4f} / "
            f"{bm['F']['MaxDD']:.2%}  OOS {bm['O']['CAGR']:.2%} / {bm['O']['Sharpe']:.4f} / "
            f"{bm['O']['MaxDD']:.2%}")
        say(f"  {pan.name}: RULES v2 (live) full {live['F']['CAGR']:.2%} / "
            f"{live['F']['Sharpe']:.4f} / {live['F']['MaxDD']:.2%}  OOS "
            f"{live['O']['CAGR']:.2%} / {live['O']['Sharpe']:.4f} / {live['O']['MaxDD']:.2%}")
        for N in NS:
            W1 = build1(pan, N, A_H)
            for g in GROSSES:
                gr, tu = nrun(pan, g * W1)
                net = gr - tu * COST / 1e4
                mF, mI, mO = pack(net[FULL]), pack(net[ISW]), pack(net[OOSW])
                p4bF, ddF, cgF, jF = legs_4b(mF, bm["F"])
                p4bI, ddI, cgI, jI = legs_4b(mI, bm["I"])
                p4bO, ddO, cgO, jO = legs_4b(mO, bm["O"])
                rows.append(dict(
                    panel=pan.name, N=N, GROSS=g,
                    CAGR=mF["CAGR"], Sharpe=mF["Sharpe"], MaxDD=mF["MaxDD"],
                    H1=mF["H1"], H2=mF["H2"],
                    IS_CAGR=mI["CAGR"], IS_Sharpe=mI["Sharpe"], IS_MaxDD=mI["MaxDD"], IS_J=jI,
                    OOS_CAGR=mO["CAGR"], OOS_Sharpe=mO["Sharpe"], OOS_MaxDD=mO["MaxDD"], OOS_J=jO,
                    KEEP_4a=keep_4a(mF, live["F"]), KEEP_4b_full=p4bF,
                    KEEP_4b_IS=p4bI, KEEP_4b_OOS=p4bO,
                    J_full=jF, dd_margin_pp=ddF, cagr_margin_pp=cgF,
                    ann_turnover=float(tu[FULL].sum() * 252.0 / len(tu[FULL])),
                ))
        say(f"  {pan.name}: {len(NS) * len(GROSSES)} cells built")

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    say(f"\nARM B: {len(grid)} books published (3 panels x {len(NS)} N x {len(GROSSES)} gross)")
    say(f"ARM B KEEP paths over all {len(grid)} cells: 4a passes {int(grid.KEEP_4a.sum())}, "
        f"4b(full) passes {int(grid.KEEP_4b_full.sum())}")
    say(grid.groupby("panel")[["KEEP_4a", "KEEP_4b_full", "KEEP_4b_IS", "KEEP_4b_OOS"]]
        .sum().to_string())

    # ------------------------------------------------ gates: replay the committed anchors
    u = grid[grid.panel == "U56"].set_index(["N", "GROSS"])
    for (N, g), a in ANCHORS.items():
        r = u.loc[(N, g)]
        err = max(abs(r.CAGR - a["CAGR"]), abs(r.Sharpe - a["Sharpe"]),
                  abs(r.MaxDD - a["MaxDD"]), abs(r.OOS_CAGR - a["oCAGR"]),
                  abs(r.OOS_Sharpe - a["oSharpe"]))
        gate(f"G4 replay U56 N={N} g={g:.2f}", f"max|err| {err:.2e}", "< 1e-3", err < 1e-3)
    lm = curves["U56"]["live"]["F"]["MaxDD"]
    gate("G5 live RULES v2 MaxDD (U56, full)", f"{lm:.4f}",
         f"~{LIVE_MAXDD_COMMITTED:.4f} (+/-0.01)", abs(lm - LIVE_MAXDD_COMMITTED) < 0.01)

    # ------------------------------------------------ rule 8: chooser on IS only, OOS once
    say("\nARM B — RULE 8 (both dials chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE):")
    for pname in ["U56", "B136", "SMALL"]:
        sub = grid[grid.panel == pname]
        strict = sub[sub.KEEP_4b_IS]
        pool, how = (strict, "IS-4b-strict") if len(strict) else (sub, "FALLBACK: IS 4b empty")
        pick = pool.sort_values(["IS_J", "GROSS", "N"],
                                ascending=[False, True, True]).iloc[0]
        bm, live = curves[pname]["spy"], curves[pname]["live"]
        wf.append(dict(panel=pname, chooser=how, IS_pool=len(pool),
                       N=int(pick.N), GROSS=float(pick.GROSS), IS_J=float(pick.IS_J),
                       FULL_CAGR=float(pick.CAGR), FULL_Sharpe=float(pick.Sharpe),
                       FULL_MaxDD=float(pick.MaxDD), H1=float(pick.H1), H2=float(pick.H2),
                       OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                       OOS_MaxDD=float(pick.OOS_MaxDD), OOS_J=float(pick.OOS_J),
                       KEEP_4a=bool(pick.KEEP_4a), KEEP_4b_full=bool(pick.KEEP_4b_full),
                       KEEP_4b_OOS=bool(pick.KEEP_4b_OOS),
                       SPY_OOS_CAGR=bm["O"]["CAGR"], SPY_OOS_Sharpe=bm["O"]["Sharpe"],
                       SPY_OOS_MaxDD=bm["O"]["MaxDD"],
                       LIVE_OOS_CAGR=live["O"]["CAGR"], LIVE_OOS_Sharpe=live["O"]["Sharpe"],
                       LIVE_OOS_MaxDD=live["O"]["MaxDD"]))
        say(f"  {pname}: pick N={int(pick.N)} g={pick.GROSS:.2f} ({how}, pool {len(pool)}) | "
            f"FULL {pick.CAGR:.2%} / {pick.Sharpe:.4f} / {pick.MaxDD:.2%} "
            f"(halves {pick.H1:.4f} / {pick.H2:.4f}) | OOS {pick.OOS_CAGR:.2%} / "
            f"{pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:.2%} | SPY OOS {bm['O']['CAGR']:.2%} / "
            f"{bm['O']['Sharpe']:.4f} / {bm['O']['MaxDD']:.2%} | RULES v2 OOS "
            f"{live['O']['CAGR']:.2%} / {live['O']['Sharpe']:.4f} / {live['O']['MaxDD']:.2%} | "
            f"4a {bool(pick.KEEP_4a)} 4b(full) {bool(pick.KEEP_4b_full)} "
            f"4b(OOS) {bool(pick.KEEP_4b_OOS)}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------ the capital-domain trace base rate
    say("\nARM B — ALARM -> VERDICT base rate (the capital version of ARM A's question).\n"
        "  ALARM  = |IS joint 4b margin| <= band, i.e. the thin-margin headline the record "
        "publishes.\n  FOLLOWED = read the SAME cell out of sample.  MOVED = IS 4b verdict "
        "!= OOS 4b verdict.")
    for band in BANDS:
        for pname in ["U56", "B136", "SMALL", "ALL"]:
            sub = grid if pname == "ALL" else grid[grid.panel == pname]
            al = sub[sub.IS_J.abs() <= band]
            na = sub[sub.IS_J.abs() > band]
            mv_a = (al.KEEP_4b_IS != al.KEEP_4b_OOS).mean() if len(al) else np.nan
            mv_n = (na.KEEP_4b_IS != na.KEEP_4b_OOS).mean() if len(na) else np.nan
            alarms.append(dict(band_pp=band, panel=pname, n_alarm=len(al), n_calm=len(na),
                               moved_alarm=mv_a, moved_calm=mv_n,
                               lift=(mv_a - mv_n) if len(al) and len(na) else np.nan))
    ald = pd.DataFrame(alarms)
    ald.to_csv(f"{OUT}.alarm.csv", index=False)
    say(ald.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return grid, wfd, ald, curves


def main():
    t0 = time.time()
    say(f"# Idea 1215 (lane C, {DATE}) — {SLUG}")
    say(f"# pandas {pd.__version__} numpy {np.__version__}; offline, deterministic\n")
    say("=" * 78); say("ARM A — the census (both dials, nine cells)"); say("=" * 78)
    tgrid, cen, ans = arm_a()
    say("\n" + "=" * 78); say("ARM B — the capital arm (198 books, both KEEP paths, rule 8)")
    say("=" * 78)
    bgrid, wfd, ald, curves = arm_b()

    say("\n" + "=" * 78); say("GATES"); say("=" * 78)
    gd = pd.DataFrame(GATES)
    gd.to_csv(f"{OUT}.gates.csv", index=False)
    say(gd.to_string(index=False))
    say(f"\nRUNTIME {time.time() - t0:.1f}s")
    say(f"ARM A ANSWER: {ans}")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
