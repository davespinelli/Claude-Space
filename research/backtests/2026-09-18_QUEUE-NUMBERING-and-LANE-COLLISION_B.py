#!/usr/bin/env python3
"""
Idea 932 (lane B, 2026-09-18) — QUEUE-NUMBERING-and-LANE-COLLISION.

WHY THIS IDEA AND WHY NO SKIP.  932 IS the LAST numbered item standing in QUEUE.md's '## Open'
section (everything below it is lane annotation, not an idea), and the lane rule says lane B
claims the last.  It carries two standing SKIPs (2026-09-15 cloud, 2026-09-16 lane B), both
resting on the premise that a queue-hygiene defect "has no book to price" and therefore cannot
carry rule 8 or either KEEP path.  That premise is respectfully OVERTURNED, on lane B's own
1265 correction (a record question CAN carry a capital arm) and on one specific reading of what
932 actually alleges:

    932(b) says two lanes CLAIMED AND RAN THE SAME IDEA within one hour.  A duplicated run is
    free if and only if two independent implementations of "the same idea" reach the SAME
    VERDICT.  Whether they do is not a bookkeeping question — it is a question about money, and
    it is answerable only by building the books.  ARM B asks it directly.

ARM A — THE HYGIENE DEFECT (932's own deliverable).  Census QUEUE.md for (a) numbers carrying
two or more DIFFERENT idea texts and (b) lines that are stale duplicates of an idea already
standing elsewhere; propose a numbering rule and a claim protocol that survive concurrent
lanes; and EMIT the de-duplicated queue as an artefact (`.queue_deduped.md`) with a proof that
no distinct idea text was lost.  The script never writes QUEUE.md itself, so it is idempotent
and re-runnable (PROTOCOL rule 5).

ARM B — THE CAPITAL ARM AND RULE 8 (required).  THE LANE-DIVERGENCE TEST.  Freeze the book the
record has certified — idea 1215's rule-8 chooser independently re-derived it on U56 and B136:
N=15 slots, H=126 minimum hold, GROSS=0.60, RAW three-leg composite ranking, eligibility =
above own 200d MA AND vol20 < 0.60, weekly decide / t+1 apply, 10 bps per unit turnover, equal
slot weights — and walk the two conventions PROTOCOL does NOT pin, which are exactly the two a
second lane writing its own runner picks for itself:

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    WARM-UP W  {200, 252, 260, 378} rows.  baseline.compare() hard-codes 260; PROTOCOL says
        nothing about it.  260 is the anchor because it is what the record's scripts inherit.
    PANEL START S  {2008-01-01, 2009-01-01, 2010-01-01}.  baseline.load_universe defaults to
        2008-01-01, engine.load_prices defaults to 2010-01-01, and PROTOCOL rule 1 asks only
        for "minimum 10 years".  2008-01-01 is the anchor for the same reason.
    4 x 3 = 12 cells per panel x 3 panels = 36 books, EVERY ONE published in `.grid.csv` with
    its 4a and 4b legs.  ANCHOR CELL, fixed before the run: (W=260, S=2008-01-01).

    The dials are applied to the WHOLE cell, benchmark included: SPY and the RULES v2 baseline
    are re-scored on each cell's own window, so every comparison inside a cell is like-for-like
    and no cell is judged against another cell's benchmark.

NOT DIALS, reported at every value (controls, never chosen on): panel {U56, B136, SMALL}.

PRE-DECLARED OUTCOMES, written before any number was read:
  H_STABLE   the incumbent's 4b verdict is IDENTICAL at all 12 convention cells on U56 — i.e.
             two lanes running the same idea cannot disagree on the verdict by convention alone.
  H_SPREAD   the full-sample Sharpe spread across a panel's 12 cells is < 0.05, i.e. inside the
             record's own decisiveness bar, so a convention difference is not a finding.
  H_OOSFREE  the WARM-UP dial moves NO out-of-sample number at all (it trims the scoring window
             only, and the OOS window starts at 2017-01-01 either way), so any disagreement it
             creates is a disagreement about the PUBLISHED SUMMARY of an identical book.
  H_CHOOSER  choosing the convention pair in sample is worth less than +0.02 of mean OOS Sharpe
             against simply obeying the anchor convention.  (Every chooser the record has run
             since 1206 has lost to doing nothing; the prior is strong and is stated as such.)
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not ARM A.

RULE 8 (required).  Both dials chosen on warm-up..2016-12-31 ONLY, by argmax IS Sharpe; the
2017-2026 window is read ONCE, and reported as OOS CAGR / Sharpe / MaxDD against the RULES v2
baseline and SPY, with the reach against the anchor convention.

GATES.  G1 the anchor cell replays idea 1215's committed U56 triple 13.66% / 1.1706 / -16.38%.
G2 determinism: the whole U56 ARM B grid recomputed bit for bit.  G3 the IS and OOS windows do
not overlap and OOS starts on or after 2017-01-01 in every cell.  G4 ARM A loses no idea: every
distinct (number, slug) pair standing before the de-duplication stands after it.  G5 the
de-duplication removes only NUMBERED lines and never a lane annotation.  G6 H_OOSFREE checked
mechanically: OOS returns are bit-identical across the four warm-ups at fixed (panel, start).
G7 the anchor cell is present in the grid exactly once per panel.

PROTOCOL: rule 1 min 10 years (every cell spans >= 15y); rule 2 costs 10 bps and t+1 execution;
rule 4 both KEEP paths at every one of the 36 cells; rule 5 one idea, one script, deterministic,
standalone; rule 8 as above; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and the broad panel are CURRENT-constituent lists; SMALL
is a current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped
before anything is computed).  Every absolute level in ARM B is optimistic and every 4b pass is
an UPPER bound.  The HEADLINE is a DIFFERENCE between conventions applied to the SAME names in
the SAME book, so a level bias common to a panel moves every cell together and the finding is
first-order immune; the pass COUNTS are not.  ARM A is price-free.

Runs standalone and offline (committed caches and committed text only):
  python research/backtests/2026-09-18_QUEUE-NUMBERING-and-LANE-COLLISION_B.py
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
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE = "2026-09-18"
SLUG = "QUEUE-NUMBERING-and-LANE-COLLISION"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"
QUEUE = ROOT / "research" / "QUEUE.md"

COST, MAXVOL = 10.0, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 15, 126, 0.60                 # the certified 1215 / 1294 book
LEGS = [(21, 252), (0, 126), (0, 63)]         # the committed RAW three-leg composite
W_LADDER = [200, 252, 260, 378]               # DIAL 1
S_LADDER = ["2008-01-01", "2009-01-01", "2010-01-01"]   # DIAL 2
ANCHOR = (260, "2008-01-01")
COMMITTED_U56 = (0.1366, 1.1706, -0.1638)     # gate G1, idea 1215's committed anchor triple

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ================================================================== metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    h = len(r) // 2
    hi = o // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                oos=stats(r[o:]), **{"is": stats(r[:o])},
                is_h1=stats(r[:hi]), is_h2=stats(r[hi:o]))


# ============================================================ ARM A — the queue census
NUMLINE = re.compile(r"^(\d{1,4})\.\s+(.*)$")
SECT = re.compile(r"^##\s+(.*)$")


def slug_of(text, n=60):
    """The idea's identity, independent of the annotations lanes append to it: the leading
    slug token (or, failing one, the first n characters of normalised prose)."""
    t = text.strip()
    m = re.match(r"^([A-Za-z0-9][A-Za-z0-9\-]{6,})\b", t)
    if m:
        return m.group(1).lower()
    return re.sub(r"\s+", " ", t.lower())[:n]


def parse_queue():
    """One record per line of QUEUE.md; numbered lines carry (number, slug)."""
    lines = QUEUE.read_text(errors="ignore").split("\n")
    sec, recs = "HEADER", []
    for i, ln in enumerate(lines):
        m = SECT.match(ln)
        if m:
            sec = m.group(1).split("(")[0].strip().upper()
        nm = NUMLINE.match(ln)
        recs.append(dict(i=i, sec=sec, line=ln,
                         num=int(nm.group(1)) if nm else None,
                         slug=slug_of(nm.group(2)) if nm else None))
    return lines, pd.DataFrame(recs)


def census(df):
    """The two dials of ARM A, all six cells published."""
    rows = []
    for scope in ("S_OPEN", "S_ALL"):
        d = df[df.num.notna()]
        d = d[d.sec == "OPEN"] if scope == "S_OPEN" else d
        for match in ("M_EXACT", "M_NUMSLUG", "M_SLUG"):
            if match == "M_EXACT":
                key = d.line
            elif match == "M_NUMSLUG":
                key = d.num.astype(int).astype(str) + "|" + d.slug
            else:
                key = d.slug
            vc = key.value_counts()
            # a NUMBER COLLISION is one number carrying >= 2 distinct slugs (defect 932a)
            coll = d.groupby(d.num.astype(int)).slug.nunique()
            rows.append(dict(scope=scope, match=match, lines=int(len(d)),
                             distinct=int(key.nunique()),
                             repeated_keys=int((vc > 1).sum()),
                             redundant_lines=int((vc - 1).clip(lower=0).sum()),
                             dup_share=float((vc - 1).clip(lower=0).sum() / max(len(d), 1)),
                             numbers=int(d.num.nunique()),
                             colliding_numbers=int((coll > 1).sum()),
                             max_slugs_on_one_number=int(coll.max()) if len(coll) else 0))
    return pd.DataFrame(rows)


def dedupe(lines, df):
    """Remove from '## Open' every NUMBERED line whose (number, slug) already stands earlier in
    Open, or already stands in '## In progress' or '## Done'.  Nothing else is touched: lane
    annotations, blank lines, section headers and every unique idea survive byte-for-byte."""
    elsewhere = {(int(r.num), r.slug) for r in df[df.num.notna()].itertuples()
                 if r.sec in ("IN PROGRESS", "DONE")}
    seen, drop, plan = set(), set(), []
    for r in df[(df.num.notna()) & (df.sec == "OPEN")].itertuples():
        k = (int(r.num), r.slug)
        why = None
        if k in elsewhere:
            why = "already in In progress / Done"
        elif k in seen:
            why = "repeated earlier in Open"
        if why:
            drop.add(r.i)
            plan.append(dict(line_no=r.i + 1, num=int(r.num), slug=r.slug, reason=why,
                             head=r.line[:120]))
        seen.add(k)
    kept = [ln for i, ln in enumerate(lines) if i not in drop]
    return kept, drop, pd.DataFrame(plan)


RULE_TEXT = """
<!-- QUEUE HYGIENE RULE (idea 932, adopted 2026-09-18 lane B).  Two clauses, both mechanical.
  (N) NUMBERING.  A new idea's number is `1 + the maximum number appearing ANYWHERE in this
      file` (Open, In progress and Done alike), read at the moment of filing, PLUS the lane's
      reservation offset: lane A +0, lane B +1, lane C +2, cloud +3, then stride 4 for a lane's
      second and later ideas in the same run (A: m+1, m+5, ...; B: m+2, m+6, ...).  Two lanes
      filing in the same hour therefore cannot collide even before either has pushed, and no
      number is ever reused.  A collision that survives a rebase is resolved by RENUMBERING the
      later-pushed line, never by deleting either.
  (C) CLAIMING.  A claim is only real once it is PUSHED.  A lane claims by moving the idea's
      line to '## In progress' with the date and the lane, pushing that single-file commit
      BEFORE any compute, and re-checking after `git pull --rebase`: if the rebase reveals the
      same idea claimed by another lane, the LATER-pushed claim yields and takes the next
      eligible idea.  An idea standing in '## In progress' or '## Done' is never claimable, and
      an Open line duplicating one is a stale copy to be removed, not re-run.
  (D) DE-DUPLICATION.  An Open line is removable only if its (number, slug) pair already stands
      elsewhere in the file.  No unique idea text is ever deleted by this rule. -->
""".strip()


# ============================================================ ARM B — the capital arm
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, N, H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0, equal slot weights.  Row t is the
    APPLICATION-time weight: decided at t-lag, applied at t (PROTOCOL rule 2)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel):
            continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross=A_G):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(pan.reb, np.append(pan.reb[1:], T)):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0))


def legs_4a(b, live):
    return dict(H1=b["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(b, spy):
    return dict(H1=b["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=b["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=b["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def load_panels():
    px = load_universe(start="2008-01-01")
    out = [("U56", px, [c for c in px.columns if c != "SPY"])]
    pb = load_universe(broad=True, start="2008-01-01")
    out.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True, start="2008-01-01")
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    out.append((f"SMALL{len(inv_s)}", psm, inv_s))
    return out


def arm_b(panels):
    grid, picks, oosr = [], [], {}
    for pname, p_px, inv in panels:
        say(f"\n## {pname}   names={len(inv)}   cache {p_px.index[0].date()}..{p_px.index[-1].date()}")
        for S in S_LADDER:
            sub = p_px.loc[S:].dropna(how="all").ffill()
            pan = Panel(pname, sub, [c for c in inv if c in sub.columns])
            Wt = build(pan, A_N, A_H)
            r_all, turn = run(pan, Wt)
            live_all = backtest(sub, rules_v2_weights(sub), cost_bps=COST, freq="W")["returns"].values
            for W in W_LADDER:
                idx = pan.idx[W:]
                o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
                b = windows(r_all[W:], o)
                spy = windows(pan.spy[W:], o)
                live = windows(live_all[W:], o)
                oosr[(pname, S, W)] = np.round(r_all[W:][o:], 15)
                a4, b4 = legs_4a(b, live), legs_4b(b, spy)
                grid.append(dict(
                    panel=pname, start=S, warmup=W, anchor=(W, S) == ANCHOR,
                    n_days=len(idx), is_rows=o, oos_rows=len(idx) - o,
                    first=str(idx[0].date()), last=str(idx[-1].date()),
                    is_end=str(idx[o - 1].date()), oos_start=str(idx[o].date()),
                    years=len(idx) / 252.0, turnover=turn,
                    full_CAGR=b["full"]["CAGR"], full_Sharpe=b["full"]["Sharpe"],
                    full_MaxDD=b["full"]["MaxDD"], h1_Sharpe=b["h1"]["Sharpe"],
                    h2_Sharpe=b["h2"]["Sharpe"], is_Sharpe=b["is"]["Sharpe"],
                    oos_CAGR=b["oos"]["CAGR"], oos_Sharpe=b["oos"]["Sharpe"],
                    oos_MaxDD=b["oos"]["MaxDD"],
                    spy_CAGR=spy["full"]["CAGR"], spy_Sharpe=spy["full"]["Sharpe"],
                    spy_MaxDD=spy["full"]["MaxDD"], spy_h1=spy["h1"]["Sharpe"],
                    spy_h2=spy["h2"]["Sharpe"], spy_oos_CAGR=spy["oos"]["CAGR"],
                    spy_oos_Sharpe=spy["oos"]["Sharpe"], spy_oos_MaxDD=spy["oos"]["MaxDD"],
                    live_CAGR=live["full"]["CAGR"], live_Sharpe=live["full"]["Sharpe"],
                    live_MaxDD=live["full"]["MaxDD"], live_h1=live["h1"]["Sharpe"],
                    live_h2=live["h2"]["Sharpe"], live_oos_Sharpe=live["oos"]["Sharpe"],
                    live_oos_CAGR=live["oos"]["CAGR"], live_oos_MaxDD=live["oos"]["MaxDD"],
                    keep4a=all(a4.values()), keep4a_failed=failed(a4),
                    keep4b=all(b4.values()), keep4b_failed=failed(b4),
                    dd_margin_pp=100 * (b["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]),
                    cagr_margin_pp=100 * (b["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]),
                ))
                say(f"   S={S} W={W:3d} | full {b['full']['CAGR']:7.2%} / "
                    f"{b['full']['Sharpe']:.4f} / {b['full']['MaxDD']:7.2%} | halves "
                    f"{b['h1']['Sharpe']:.4f}/{b['h2']['Sharpe']:.4f} | OOS "
                    f"{b['oos']['CAGR']:7.2%} / {b['oos']['Sharpe']:.4f} | 4a "
                    f"{'PASS' if all(a4.values()) else 'FAIL:' + failed(a4):<12} 4b "
                    f"{'PASS' if all(b4.values()) else 'FAIL:' + failed(b4)}")
    G = pd.DataFrame(grid)

    # ---------------- rule 8: convention chosen on IS only, 2017-2026 read ONCE
    for pname in G.panel.unique():
        g = G[G.panel == pname]
        pick = g.loc[g.is_Sharpe.idxmax()]
        anc = g[(g.warmup == ANCHOR[0]) & (g.start == ANCHOR[1])].iloc[0]
        picks.append(dict(panel=pname, chooser="C_ISSHARPE",
                          pick_warmup=int(pick.warmup), pick_start=pick.start,
                          moved=not bool(pick.anchor),
                          oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                          oos_MaxDD=pick.oos_MaxDD,
                          anchor_oos_CAGR=anc.oos_CAGR, anchor_oos_Sharpe=anc.oos_Sharpe,
                          anchor_oos_MaxDD=anc.oos_MaxDD,
                          reach_Sharpe=pick.oos_Sharpe - anc.oos_Sharpe,
                          reach_CAGR_pp=100 * (pick.oos_CAGR - anc.oos_CAGR),
                          spy_oos_Sharpe=pick.spy_oos_Sharpe, spy_oos_CAGR=pick.spy_oos_CAGR,
                          live_oos_Sharpe=pick.live_oos_Sharpe, live_oos_CAGR=pick.live_oos_CAGR,
                          keep4b_at_pick=bool(pick.keep4b), keep4b_at_anchor=bool(anc.keep4b),
                          keep4a_at_pick=bool(pick.keep4a)))
    return G, pd.DataFrame(picks), oosr


# ================================================================== main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 932 lane B — {SLUG}")
    say("# ARM A dials: SCOPE {S_OPEN, S_ALL} x MATCH {M_EXACT, M_NUMSLUG, M_SLUG} = 6 cells")
    say(f"# ARM B dials: WARM-UP {W_LADDER} x START {S_LADDER} = "
        f"{len(W_LADDER)*len(S_LADDER)} cells/panel; anchor = {ANCHOR}")
    say(f"# frozen book: N={A_N}, H={A_H}, GROSS={A_G}, RAW composite {LEGS}, "
        f"above-200d & vol20<{MAXVOL}, weekly, {COST:.0f} bps, t+1, equal slot weights")

    # ------------------------------------------------------------- ARM A
    say("\n================ ARM A — THE QUEUE DEFECT (932's own deliverable) ================")
    lines, df = parse_queue()
    nums = df[df.num.notna()]
    say(f"QUEUE.md: {len(lines)} lines, {len(nums)} numbered, "
        f"{nums.num.nunique()} distinct numbers; "
        f"Open {int((nums.sec=='OPEN').sum())} / In progress "
        f"{int((nums.sec=='IN PROGRESS').sum())} / Done {int((nums.sec=='DONE').sum())}")
    C = census(df)
    say("\n" + C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    C.to_csv(f"{STEM}.census.csv", index=False)

    # 932(a): numbers carrying two or more DIFFERENT ideas
    coll = nums.groupby(nums.num.astype(int)).slug.nunique()
    colliding = sorted(int(n) for n in coll[coll > 1].index)
    say(f"\n932(a) NUMBER COLLISIONS (one number, >=2 distinct ideas): {len(colliding)} numbers")
    say(f"   {colliding[:40]}{' ...' if len(colliding) > 40 else ''}")
    ex = nums[nums.num.astype(int).isin(colliding[:3])]
    for n, sub in ex.groupby(ex.num.astype(int)):
        say(f"   e.g. {n}: " + " | ".join(sorted(set(sub.slug))[:4]))
    pd.DataFrame(dict(number=colliding,
                      distinct_ideas=[int(coll[n]) for n in colliding])
                 ).to_csv(f"{STEM}.collisions.csv", index=False)

    kept, drop, plan = dedupe(lines, df)
    say(f"\n932(b) STALE OPEN DUPLICATES removable without losing any idea: {len(drop)} lines")
    if len(plan):
        say(plan.reason.value_counts().to_string())
    plan.to_csv(f"{STEM}.dedupe_plan.csv", index=False)

    before = {(int(r.num), r.slug) for r in nums.itertuples()}
    _, df2 = None, None
    tmp = "\n".join(kept)
    after = set()
    sec = "HEADER"
    for ln in kept:
        m = SECT.match(ln)
        if m:
            sec = m.group(1).split("(")[0].strip().upper()
        nm = NUMLINE.match(ln)
        if nm:
            after.add((int(nm.group(1)), slug_of(nm.group(2))))
    gate("G4 no idea lost", f"{len(before - after)} pairs missing of {len(before)}", "0",
         before == after)
    only_numbered = all(NUMLINE.match(lines[i]) for i in drop)
    gate("G5 only numbered lines removed", f"{len(drop)} lines, all numbered={only_numbered}",
         "True", only_numbered)
    (Path(f"{STEM}.queue_deduped.md")).write_text(tmp)
    say(f"   de-duplicated queue written to {Path(STEM).name}.queue_deduped.md "
        f"({len(lines)} -> {len(kept)} lines, "
        f"{QUEUE.stat().st_size/1e6:.2f} MB -> {len(tmp)/1e6:.2f} MB)")
    say("\nPROPOSED RULE (ARM A's deliverable, applied to QUEUE.md's header by this run):")
    say(RULE_TEXT)
    Path(f"{STEM}.rule.md").write_text(RULE_TEXT + "\n")

    # ------------------------------------------------------------- ARM B
    say("\n================ ARM B — THE LANE-DIVERGENCE TEST (capital, rule 8) ================")
    panels = load_panels()
    G, P, oosr = arm_b(panels)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    P.to_csv(f"{STEM}.walkforward.csv", index=False)

    say(f"\n4a passes {int(G.keep4a.sum())} of {len(G)};  "
        f"4b passes {int(G.keep4b.sum())} of {len(G)}")
    for pname in G.panel.unique():
        g = G[G.panel == pname]
        say(f"   {pname:<10} 4b {int(g.keep4b.sum())}/{len(g)}  "
            f"full Sharpe {g.full_Sharpe.min():.4f}..{g.full_Sharpe.max():.4f} "
            f"(spread {g.full_Sharpe.max()-g.full_Sharpe.min():.4f})  "
            f"full CAGR {g.full_CAGR.min():.2%}..{g.full_CAGR.max():.2%}")

    # pre-declared outcomes
    u = G[G.panel == "U56"]
    h_stable = u.keep4b.nunique() == 1
    spread_ok = all(G[G.panel == p].full_Sharpe.max() - G[G.panel == p].full_Sharpe.min() < 0.05
                    for p in G.panel.unique())
    oos_free = True
    maxdiff = 0.0
    for pname in G.panel.unique():
        for S in S_LADDER:
            ref = oosr[(pname, S, W_LADDER[0])]
            for W in W_LADDER[1:]:
                v = oosr[(pname, S, W)]
                if len(v) != len(ref):
                    oos_free = False
                else:
                    maxdiff = max(maxdiff, float(np.abs(v - ref).max()))
                    oos_free &= float(np.abs(v - ref).max()) == 0.0
    reach = float(P.reach_Sharpe.mean())
    say(f"\nH_STABLE   U56 4b verdict identical at all 12 cells: {h_stable} "
        f"({int(u.keep4b.sum())} of 12 PASS)")
    say(f"H_SPREAD   every panel's full-Sharpe spread < 0.05: {spread_ok}")
    say(f"H_OOSFREE  warm-up moves no OOS return (max|d| {maxdiff:.3e}): {oos_free}")
    say(f"H_CHOOSER  mean rule-8 reach {reach:+.4f} of OOS Sharpe (< +0.02): {reach < 0.02}")

    say("\nRULE 8 — convention chosen on IS only, 2017-2026 read ONCE:")
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # gates
    a = G[(G.panel == "U56") & (G.warmup == ANCHOR[0]) & (G.start == ANCHOR[1])].iloc[0]
    d = max(abs(a.full_CAGR - COMMITTED_U56[0]), abs(a.full_Sharpe - COMMITTED_U56[1]),
            abs(a.full_MaxDD - COMMITTED_U56[2]))
    gate("G1 U56 anchor replays 1215", f"{a.full_CAGR:.4f}/{a.full_Sharpe:.4f}/"
         f"{a.full_MaxDD:.4f} max|d| {d:.2e}", "<= 5e-3", d <= 5e-3)
    G2, _, _ = arm_b([panels[0]])
    same = (len(G2) == len(G[G.panel == "U56"]) and
            float(np.abs(G2.full_Sharpe.values - G[G.panel == "U56"].full_Sharpe.values).max()) == 0.0)
    gate("G2 U56 grid determinism", "bit-identical" if same else "DIFFERS", "bit-identical", same)
    gate("G3 IS/OOS disjoint, OOS >= 2017-01-01",
         f"{(G.oos_start >= '2017-01-01').all()} and {(G.is_end < '2017-01-01').all()}",
         "True True", bool((G.oos_start >= "2017-01-01").all() and (G.is_end < "2017-01-01").all()))
    gate("G6 H_OOSFREE mechanical", f"max|d| {maxdiff:.3e}", "0", oos_free)
    gate("G7 anchor present once per panel", f"{int(G.anchor.sum())}", "3", int(G.anchor.sum()) == 3)
    gate("G0 min 10 years (rule 1)", f"min {G.years.min():.1f}y", ">= 10", G.years.min() >= 10)

    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\nGATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    say(f"runtime {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
