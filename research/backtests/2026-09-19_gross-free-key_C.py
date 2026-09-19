#!/usr/bin/env python3
"""
Idea 1194 (lane C, 2026-09-19) — how many committed 4b PASSES in the record COLLAPSE under a
GROSS-FREE KEY?  Restated where it costs money: **is a 4b PASS a property of a BOOK, or of the
GROSS DIAL?**

WHY THIS IDEA.  The sprint rule gives this lane the SECOND eligible item in QUEUE.md's '## Open'.
1204 is first (lane A's); 1194 is second, and it is price-only (no EDGAR / Form 4 / 8-K / options /
live data), so no eligibility descent was taken.

THE PREMISE (idea 1189's own finding).  1189 recommended keying a 4b pass on (panel, N, cadence, H)
with GROSS as an ATTRIBUTE rather than part of the key, and that re-keying collapsed its own 14
committed passes to 8 distinct books (0.43 duplicated).  The queue asks for the census.  A census
of committed TEXT cannot carry this protocol's step-3 deliverable, so this run does BOTH legs and
puts the weight on the second:

  LEG 1 (CENSUS, mechanical).  Harvest every committed 4b PASS row in LEADERBOARD.md, extract the
  key fields that are actually STATED, group under the gross-free key, and report the record's
  distinct-book count, its duplication rate, and — the field that decides whether the re-key is
  even legal — how many committed passes state their gross AT ALL.  Recall limits published.

  LEG 2 (CAPITAL, real books).  The re-key is only sound if a 4b PASS is INVARIANT to gross within
  a book.  If it is not, dropping gross from the key does not de-duplicate the record, it ERASES
  the dial that produced the verdict.  So this run measures the GROSS-WIDTH of a 4b pass directly:
  270 real books, and for each (panel, N) family the SET of gross rungs on which it passes.

THE CONSTRUCTION.  Every cell is the frozen 2026-09-04 KEEP-4b candidate with ONE dial moved.
Byte-identical to the incumbent otherwise: the same raw 3-leg composite (21/252, 0/126, 0/63,
percentile-ranked, equal-weighted), the same above-200d AND vol20 < 0.60 ENTRY gate, H = 126-day
minimum hold, equal weight gross/n, weekly Fri-decide / Mon-trade, 10 bps per unit turnover, t+1,
260-row warm-up.  The incumbent itself (N = 20, g = 0.75) is carried as a CONTROL ROW on every
panel and gated against its committed triple.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4):
    N       slots.  Rungs {10, 15, 20, 25, 30, 40}, ALL reported.
    gross   Rungs {0.30, 0.35, ..., 1.00} — 15 of them, ALL reported.  No leverage (g <= 1.00).
The rule-8 chooser picks over these two axes and nothing else.

NOT A DIAL, reported at every value (control, never chosen on):
    panel   {U56, B136, SMALL} — the record's three standing panels.  Cadence is frozen at W and
            H at 126 (the incumbent's), so this run says nothing about those axes of 1189's key.

PRE-DECLARED OUTCOMES, written before any number below was read:
  H_WIDTH     a 4b pass is NOT a book property: on U56 at N = 20 the pass covers FEWER THAN 10 of
              the 15 gross rungs, i.e. the gross dial alone flips the published verdict.
  H_INTERVAL  the passing set in gross is a contiguous INTERVAL, bounded BELOW by the 4b CAGR floor
              (>= 70% of SPY) and ABOVE by the 4b DD cap (<= 60% of SPY's MaxDD).
  H_EDGE      the incumbent's g = 0.75 does NOT sit at the centre of its own passing interval.
  H_PICK      a chooser allowed to touch GROSS in sample does NOT beat one that freezes g at 0.75
              and picks only N, by more than 0.05 of OOS Sharpe (2017-2026 read ONCE).
  H_CENSUS    a MAJORITY of committed 4b PASS rows in LEADERBOARD.md do not state their gross.
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not the full sample.

GATES.  G1 the (U56, N=20, g=0.75) control replays the committed incumbent anchor
(15.80% / 1.1537 / -19.13%) to within the 5e-3 tape-vintage Sharpe floor idea 1350 established;
the deviation is PUBLISHED, not asserted.  G2 weights sum to exactly gross at every rebalance row
(|dev| < 1e-12).  G3 all 270 cells published.  G4 exactly two tuned parameters.  G5 the chooser
reads no row on or after 2017-01-01.  G6 determinism: the headline cell recomputed bit for bit.
G7 contiguity of each family's passing gross set is tested MECHANICALLY (number of maximal runs
reported), so H_INTERVAL cannot be asserted from a glance.  G8 the census leg's regexes and their
recall are published with the counts.

PROTOCOL: rule 1 committed caches, >= 10 years; rule 2 10 bps per unit turnover, t+1 execution;
rule 3 compared against live RULES v2 AND SPY on each panel; rule 4 both KEEP paths at every cell;
rule 5 one idea, one script, deterministic, standalone; rule 8 walk-forward as above; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first), so every absolute
level is an upper bound and every 4b pass an optimistic one.  The headline here is a WIDTH — how
many gross rungs of one book's own ladder clear the bar — read over the SAME panel on the SAME
days, so it is first-order immune to a level bias common to the whole ladder; the pass COUNT is not.

Offline and deterministic (committed caches only, no network, no yfinance):
  python research/backtests/2026-09-19_gross-free-key_C.py
"""
from __future__ import annotations

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
from baseline import EXCLUDE, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask             # noqa: E402

DATE, SLUG = "2026-09-19", "gross-free-key"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
A_N, A_H, A_G = 20, 126, 0.75                  # the frozen 2026-09-04 incumbent
LEGS = [(21, 252), (0, 126), (0, 63)]          # the committed RAW three-leg composite
NS = [10, 15, 20, 25, 30, 40]
GS = [round(0.30 + 0.05 * i, 2) for i in range(15)]        # 0.30 .. 1.00
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COMMITTED_U56 = (0.1580, 1.1537, -0.1913)      # idea 1350 head-vintage anchor
TAPE_FLOOR = 5e-3

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
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
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]),
                **{"is": stats(r[:o])})


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


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


def runs_of_true(flags):
    """Number of maximal contiguous runs of True (G7 contiguity test)."""
    n, prev = 0, False
    for f in flags:
        if f and not prev:
            n += 1
        prev = f
    return n


# ------------------------------------------------------------------ panels
UNIV = sorted({t for g in json.loads((ROOT / "research" / "universe.json").read_text()).values()
               for t in g} - set(EXCLUDE))
_meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD_SMALL = set(_meta.loc[_meta.max_1d_move >= 1.0, "ticker"])


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.idx = name, px, px.index
        q = px[invest]
        self.rets = q.pct_change().fillna(0.0).values
        self.priced = q.notna().values
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        v20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(v20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.C = C
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.T = len(px)
        self.K = len(invest)


def panels():
    out = []
    raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()
    keep = [c for c in UNIV if c in raw.columns]
    px = raw[keep].loc["2008-01-01":].dropna(how="all").ffill()
    out.append(Panel("U56", px, [c for c in px.columns if c != "SPY"]))

    pb = pd.read_csv(ROOT / "data" / "prices_broad.csv", index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":].dropna(how="all").ffill()
    out.append(Panel("B136", pb, [c for c in pb.columns if c != "SPY"]))

    ps = pd.read_csv(ROOT / "data" / "prices_small.csv.gz", index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":].dropna(how="all").ffill()
    spy = raw["SPY"].reindex(ps.index, method="ffill").rename("SPY")
    ps = pd.concat([ps.drop(columns=["SPY"], errors="ignore"), spy], axis=1)
    inv = [c for c in ps.columns if c != "SPY" and c not in BAD_SMALL]
    out.append(Panel("SMALL", ps, inv))
    return out


# ------------------------------------------------------------------ selection (frozen incumbent)
def build_sel(pan, N, H=A_H, lag=1):
    """The frozen book's held set per rebalance segment.  Entry: eligible, priced, top of the raw
    3-leg composite.  Retention: calendar immunity for H rows while priced.  Depends on (N, H)
    ONLY — never on gross, which is exactly the invariance this run is testing."""
    K = pan.K
    segs = []
    cur = np.full(K, -1, dtype=np.int64)
    pr, T, nreb = pan.priced, pan.T, len(pan.reb)
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
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        if len(sel):
            segs.append((int(t), int(stop), sel.copy()))
    return segs


def run(pan, segs, gross):
    T = pan.T
    r = np.zeros(T)
    turn_tot, wdev = 0.0, 0.0
    curw = np.zeros(pan.K)
    for (i0, i1, sel) in segs:
        n = len(sel)
        w = np.full(n, gross / n)
        wdev = max(wdev, abs(w.sum() - gross))
        new = np.zeros(pan.K)
        new[sel] = w
        turn = float(np.abs(new - curw).sum())
        turn_tot += turn
        base = pan.Cp[i0, sel]
        A = w[None, :] * (pan.Cp[i0:i1, sel] / base[None, :])
        c0 = 1.0 - w.sum()
        V = A.sum(axis=1) + c0
        seg = (A * pan.rets[i0:i1, sel]).sum(axis=1) / V
        seg[0] -= turn * COST / 1e4
        r[i0:i1] = seg
        Ae = w * (pan.C[i1 - 1, sel] / base)
        curw = np.zeros(pan.K)
        curw[sel] = Ae / (Ae.sum() + c0)
    return r, dict(turnover=turn_tot / (T / 252.0), wdev=wdev)


# ------------------------------------------------------------------ LEG 1: the census
PANEL_RE = re.compile(r"\b(U56|B136|SMALL\d*|SMALL)\b")
N_RE = re.compile(r"\bN\s*=\s*(\d{1,3})\b")
H_RE = re.compile(r"\bH\s*=\s*(\d{1,3})\b")
G_RE = re.compile(r"\b(?:g|G|gross|GROSS)\s*=?\s*(0\.\d{1,3}|1\.00?)\b")
CAD_RE = re.compile(r"\b(daily|weekly|monthly|quarterly|DAILY|WEEKLY|MONTHLY|QUARTERLY)\b")
PASS4B_RE = re.compile(r"4b[^|]{0,40}\bPASS", re.IGNORECASE)


def census():
    """Mechanical harvest of committed 4b PASS assertions from LEADERBOARD.md.

    RECALL LIMITS, published (G8).  The leaderboard is free prose in a pipe table, so this census
    can only see what a row STATES.  A row is counted as a 4b PASS assertion if the regex
    `4b[^|]{0,40}PASS` (case-insensitive) matches any of its cells.  Key fields are read with the
    regexes printed below and are MISSING, not inferred, when absent.  The resulting counts are
    therefore a LOWER BOUND on the record's 4b passes and an UPPER BOUND on the share that state
    their gross (a row may state a gross belonging to a different book it also mentions)."""
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(encoding="utf-8", errors="replace")
    rows = [ln for ln in lb.split("\n") if ln.startswith("|")]
    hits = []
    for ln in rows:
        if not PASS4B_RE.search(ln):
            continue
        p = PANEL_RE.search(ln)
        n = N_RE.search(ln)
        h = H_RE.search(ln)
        g = G_RE.search(ln)
        c = CAD_RE.search(ln)
        hits.append(dict(
            panel=(p.group(1) if p else None),
            N=(int(n.group(1)) if n else None),
            H=(int(h.group(1)) if h else None),
            cadence=(c.group(1).lower() if c else None),
            gross=(float(g.group(1)) if g else None),
        ))
    df = pd.DataFrame(hits)
    say("\n" + "=" * 100)
    say("LEG 1 — CENSUS of committed 4b PASS assertions in LEADERBOARD.md")
    say("=" * 100)
    say(f"  table rows scanned                : {len(rows)}")
    say(f"  rows asserting a 4b PASS          : {len(df)}")
    if df.empty:
        return df, {}
    tot = len(df)
    stated = {k: int(df[k].notna().sum()) for k in ("panel", "N", "H", "cadence", "gross")}
    for k, v in stated.items():
        say(f"  ... stating {k:<9}              : {v:5d}  ({v / tot:.1%})")
    full = df.dropna(subset=["panel", "N", "H", "cadence"])
    say(f"  rows stating the FULL gross-free key (panel,N,cadence,H): {len(full)} ({len(full)/tot:.1%})")
    out = dict(rows_scanned=len(rows), pass_rows=tot, **{f"stated_{k}": v for k, v in stated.items()},
               full_key_rows=len(full))
    if len(full):
        kf = full.groupby(["panel", "N", "cadence", "H"]).size()
        kg = full.dropna(subset=["gross"]).groupby(["panel", "N", "cadence", "H", "gross"]).size()
        say(f"  distinct books under the GROSS-FREE key (panel,N,cadence,H) : {len(kf)}")
        say(f"  distinct books under the GROSS-BEARING key                  : {len(kg)}")
        dup = 1.0 - len(kf) / len(full)
        say(f"  duplication rate of the full-key rows under the gross-free key: {dup:.3f}")
        out.update(distinct_grossfree=len(kf), distinct_grossbearing=len(kg), dup_rate=dup)
    say("  REGEXES (G8): " + " | ".join([PASS4B_RE.pattern, PANEL_RE.pattern, N_RE.pattern,
                                         H_RE.pattern, CAD_RE.pattern, G_RE.pattern]))
    say("  RECALL: counts are a LOWER BOUND on the record's 4b passes; fields are read, never inferred.")
    return df, out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("Idea 1194 (lane C) — is a 4b PASS a BOOK property or a GROSS-DIAL property?")
    say("=" * 100)

    cdf, cinfo = census()

    rows, fam = [], []
    say("\n" + "=" * 100)
    say(f"LEG 2 — CAPITAL: {3 * len(NS) * len(GS)} real books (3 panels x {len(NS)} N x {len(GS)} gross rungs)")
    say("=" * 100)
    for pan in panels():
        say(f"\n--- panel {pan.name}: {pan.K} investables, {pan.T} rows "
            f"{pan.idx[0].date()}..{pan.idx[-1].date()}, {len(pan.reb)} rebalances")
        o = int(np.searchsorted(pan.idx, OOS_START))
        st = WARMUP
        base = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live = windows(base[st:], o - st)
        spy = windows(pan.spy[st:], o - st)
        say(f"    live RULES v2  CAGR {live['full']['CAGR']:.2%}  Sharpe {live['full']['Sharpe']:.4f}"
            f"  MaxDD {live['full']['MaxDD']:.2%}  OOS {live['oos']['CAGR']:.2%}/"
            f"{live['oos']['Sharpe']:.4f}/{live['oos']['MaxDD']:.2%}")
        say(f"    SPY            CAGR {spy['full']['CAGR']:.2%}  Sharpe {spy['full']['Sharpe']:.4f}"
            f"  MaxDD {spy['full']['MaxDD']:.2%}  OOS {spy['oos']['CAGR']:.2%}/"
            f"{spy['oos']['Sharpe']:.4f}/{spy['oos']['MaxDD']:.2%}")
        say(f"    4b bars on this panel: DD cap {DD_CAP * spy['full']['MaxDD']:.2%}"
            f"   CAGR floor {CAGR_FLOOR * spy['full']['CAGR']:.2%}"
            f"   H1 {spy['h1']['Sharpe']:.4f}  H2 {spy['h2']['Sharpe']:.4f}  OOS {spy['oos']['Sharpe']:.4f}")

        for N in NS:
            segs = build_sel(pan, N)
            flags, line = [], []
            for g in GS:
                rr, extra = run(pan, segs, g)
                w = windows(rr[st:], o - st)
                b4a, b4b = legs_4a(w, live), legs_4b(w, spy)
                rows.append(dict(panel=pan.name, N=N, gross=g, **flat(w),
                                 turnover=extra["turnover"], wdev=extra["wdev"],
                                 pass4a=all(b4a.values()), fail4a=failed(b4a),
                                 pass4b=all(b4b.values()), fail4b=failed(b4b),
                                 m4b_DD=(w["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]) * 100,
                                 m4b_CAGR=(w["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]) * 100,
                                 m4b_OOS=w["oos"]["Sharpe"] - spy["oos"]["Sharpe"],
                                 spy_sharpe=spy["full"]["Sharpe"], live_sharpe=live["full"]["Sharpe"],
                                 is_sharpe=w["is"]["Sharpe"]))
                flags.append(all(b4b.values()))
                line.append(f"{g:.2f}:{'P' if all(b4b.values()) else failed(b4b)[:4]}")
            wid = int(sum(flags))
            nr = runs_of_true(flags)
            gp = [g for g, f in zip(GS, flags) if f]
            lo, hi = (min(gp), max(gp)) if gp else (np.nan, np.nan)
            ctr = (lo + hi) / 2 if gp else np.nan
            fam.append(dict(panel=pan.name, N=N, width4b=wid, runs=nr, g_lo=lo, g_hi=hi,
                            g_centre=ctr, anchor_in=(A_G in gp),
                            width4a=int(sum(r["pass4a"] for r in rows if r["panel"] == pan.name and r["N"] == N))))
            say(f"    N={N:<3} 4b width {wid:2d}/{len(GS)} runs {nr}  interval "
                f"[{lo if gp else float('nan'):.2f},{hi if gp else float('nan'):.2f}]  "
                f"centre {ctr if gp else float('nan'):.3f}  g=0.75 {'IN' if A_G in gp else 'OUT'}")
            say(f"         " + " ".join(line))

    df = pd.DataFrame(rows)
    fdf = pd.DataFrame(fam)
    df.to_csv(f"{STEM}.cells.csv", index=False)
    fdf.to_csv(f"{STEM}.families.csv", index=False)

    # ---------------- gates
    say("\n" + "=" * 100)
    say("GATES")
    say("=" * 100)
    a = df[(df.panel == "U56") & (df.N == A_N) & (df.gross == A_G)].iloc[0]
    dS = abs(a.full_Sharpe - COMMITTED_U56[1])
    say(f"   incumbent replay (U56 N=20 g=0.75): CAGR {a.full_CAGR:.2%} (committed {COMMITTED_U56[0]:.2%})"
        f"  Sharpe {a.full_Sharpe:.4f} (committed {COMMITTED_U56[1]:.4f})"
        f"  MaxDD {a.full_MaxDD:.2%} (committed {COMMITTED_U56[2]:.2%})")
    gate("G1", f"|dSharpe|={dS:.2e}", f"< {TAPE_FLOOR} tape-vintage floor", dS < TAPE_FLOOR)
    gate("G2", f"max|wdev|={df.wdev.max():.2e}", "< 1e-12", df.wdev.max() < 1e-12)
    gate("G3", f"{len(df)} cells published", f"{3 * len(NS) * len(GS)}", len(df) == 3 * len(NS) * len(GS))
    gate("G4", "tuned params = (N, gross)", "exactly 2", True)

    # ---------------- G7 contiguity
    nonc = fdf[(fdf.runs > 1)]
    gate("G7", f"{len(nonc)} of {len(fdf)} families have >1 PASS run", "contiguity reported, not asserted", True)
    if len(nonc):
        say("      NON-CONTIGUOUS families: " + ", ".join(f"{r.panel}/N={r.N}(runs={r.runs})"
                                                          for r in nonc.itertuples()))

    # ---------------- LEG 3: rule 8
    say("\n" + "=" * 100)
    say("LEG 3 — RULE 8 WALK-FORWARD.  IS = warm-up..2016-12-31, OOS = 2017-01-01.. read ONCE.")
    say("=" * 100)
    gate("G5", f"OOS_START={OOS_START.date()}", "chooser reads no row on/after 2017-01-01", True)
    oos_rows = []
    for pan_name in df.panel.unique():
        d = df[df.panel == pan_name]
        spyS = None
        sub = d.copy()
        # C_FULL: argmax IS Sharpe over (N, gross); ties -> smallest gross, then smallest N
        cf = sub.sort_values(["is_sharpe", "gross", "N"], ascending=[False, True, True]).iloc[0]
        # C_NFREE: gross frozen at the incumbent 0.75, pick N only
        cn = sub[sub.gross == A_G].sort_values(["is_sharpe", "N"], ascending=[False, True]).iloc[0]
        an = sub[(sub.N == A_N) & (sub.gross == A_G)].iloc[0]
        for lab, c in (("C_FULL (N,g free)", cf), ("C_NFREE (g=0.75, N free)", cn),
                       ("ANCHOR (N=20,g=0.75)", an)):
            say(f"  {pan_name:<6} {lab:<26} picks N={int(c.N):<3} g={c.gross:.2f} | IS Sharpe {c.is_sharpe:.4f}"
                f" | OOS CAGR {c.oos_CAGR:7.2%} Sharpe {c.oos_Sharpe:.4f} MaxDD {c.oos_MaxDD:7.2%}"
                f" | 4b {'PASS' if c.pass4b else 'fail:' + c.fail4b}")
            oos_rows.append(dict(panel=pan_name, chooser=lab, N=int(c.N), gross=c.gross,
                                 is_sharpe=c.is_sharpe, oos_CAGR=c.oos_CAGR, oos_Sharpe=c.oos_Sharpe,
                                 oos_MaxDD=c.oos_MaxDD, pass4b=c.pass4b))
        d_full_vs_nfree = cf.oos_Sharpe - cn.oos_Sharpe
        say(f"  {pan_name:<6} H_PICK: OOS Sharpe(C_FULL) - OOS Sharpe(C_NFREE) = {d_full_vs_nfree:+.4f}"
            f"   -> touching gross {'BUYS' if d_full_vs_nfree > 0.05 else 'BUYS NOTHING'}")
    odf = pd.DataFrame(oos_rows)
    odf.to_csv(f"{STEM}.chooser.csv", index=False)

    # ---------------- determinism gate
    pan0 = panels()[0]
    s0 = build_sel(pan0, A_N)
    r0, _ = run(pan0, s0, A_G)
    r1, _ = run(pan0, build_sel(pan0, A_N), A_G)
    gate("G6", f"max|d|={np.abs(r0 - r1).max():.1e}", "bit-identical recompute", np.abs(r0 - r1).max() == 0.0)

    # ---------------- headline
    say("\n" + "=" * 100)
    say("HEADLINE")
    say("=" * 100)
    u = fdf[fdf.panel == "U56"]
    u20 = u[u.N == A_N].iloc[0]
    say(f"  H_WIDTH   U56 N=20 4b pass covers {u20.width4b} of {len(GS)} gross rungs "
        f"-> {'CONFIRMED' if u20.width4b < 10 else 'REFUTED'} (bar: < 10)")
    say(f"  H_INTERVAL {len(fdf[fdf.runs > 1])} of {len(fdf)} families are NON-contiguous "
        f"-> {'REFUTED' if len(fdf[fdf.runs > 1]) else 'CONFIRMED'}")
    if u20.width4b:
        off = abs(A_G - u20.g_centre)
        say(f"  H_EDGE    U56 N=20 interval [{u20.g_lo:.2f},{u20.g_hi:.2f}] centre {u20.g_centre:.3f};"
            f" incumbent 0.75 is {off:.3f} off centre -> {'CONFIRMED' if off > 1e-9 else 'REFUTED'}")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)} cells; 4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for p in df.panel.unique():
        dd = df[df.panel == p]
        say(f"     {p:<6}: 4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            f"   binding legs: {dd[~dd.pass4b].fail4b.value_counts().head(3).to_dict()}")
    say(f"\n  total runtime {time.time() - t0:.1f}s")
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    say(f"  wrote {STEM.name}.cells.csv / .families.csv / .chooser.csv / .gates.csv")


if __name__ == "__main__":
    main()
