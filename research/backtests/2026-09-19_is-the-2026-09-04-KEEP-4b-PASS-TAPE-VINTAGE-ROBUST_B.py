#!/usr/bin/env python3
"""
Idea 1350 (lane B, 2026-09-19) — is the 2026-09-04 KEEP-4b PASS TAPE-VINTAGE ROBUST?

WHY THIS IDEA.  1350 is the LAST numbered item standing in QUEUE.md's '## Open' section and
the sprint rule gives lane B the last.  No eligibility descent is taken: the idea is
PRICE-ONLY and fully OFFLINE — the vintages come from `git show <rev>:data/prices.csv` in this
repository's own history, never from the network — and it carries a real capital arm (the
frozen incumbent rebuilt on every recoverable tape vintage on three panels, both KEEP paths at
every vintage, rule 8 with 2017-2026 read once).

THE PREMISE (idea 1335's gate G1b, 2026-09-18).  G1b replayed a committed cell to 1e-8 on the
full sample but FAILED by 6.98e-3 on its HALVES, because commit 4e19a80 ("Daily close
2026-09-18") rewrote data/prices*.csv wholesale AFTER idea 1305 had committed the same cell.
Cross-run replay of a half-sample Sharpe in this repo is therefore resolution-limited by the
TAPE, and NO committed number in this family carries a tape stamp.  The standing KEEP-4b
candidate already sits 1.10 pp inside a hard drawdown cap (idea 1253) and 1.16 lag-SDs inside
it (the execution-delay run).  If vintage noise is the same order, the committed pass is not a
fact about the RULE.

WHY THE TAPE MOVES AT ALL.  The daily cache is rebuilt with `auto_adjust=True`, which
BACK-ADJUSTS the entire price history every time a name goes ex-dividend or splits.  A vintage
is therefore not an append-only extension of its predecessor: measured here, 27,617 to 48,821
of ~272,000 overlapping U56 cells differ between vintages, with relative moves up to 4.9%.
Every number this family has committed was computed on ONE draw from that sequence.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    VINTAGE  every commit in this repository's history that changed data/prices.csv, read with
             `git show`.  14 of them (2026-09-03 .. 2026-09-18), each a DISTINCT blob (gate G3).
             The panel files prices_broad.csv / prices_small.csv.gz are read AS OF the same
             commit, so a vintage is a whole repo-state tape, not one file.
    PANEL    {U56, B136, SMALL} — the record's three standing panels.

NOT DIALS, reported at every value (controls, never chosen on):
    READING {V_RAW, V_TRUNC}
        V_RAW   each vintage scored on its OWN full sample — what an implementer standing on
                that day would have computed, and what the record actually did.  It confounds
                restatement with one more week of data.
        V_TRUNC every vintage truncated to the COMMON last date (the earliest vintage's end),
                so ONLY restatements of overlapping rows can move the number.  This is the
                clean measurement of tape noise.
    COHORT {V_ALL, V_POSTFIX}
        Commit c006b439 ("Fix calendar-day index bug: align crypto to equity") changed the
        INDEX, not just the values: the two vintages below it carry ~6,060 calendar rows
        against ~4,700 trading rows.  They are recoverable vintages and are published, but a
        spread computed across them measures a fixed BUG, not tape noise, so every headline is
        given on both cohorts and V_POSTFIX (12 vintages) is the one read.

ARM A — THE SPREAD OF EVERY 4b LEG'S MARGIN.  The frozen 2026-09-04 book (RAW three-leg
composite ranking, eligibility = above own 200d MA AND vol20 < 0.60, N=20 slots, H=126-day
minimum hold, GROSS=0.75, weekly Fri-decide/Mon-trade, equal slot weights, 10 bps per unit
turnover, t+1, 260-row warm-up) is rebuilt on every (vintage, panel, reading) cell.  For each
the five 4b legs and three 4a legs are published AS MARGINS in their own units:
    m_H1  = book H1 Sharpe  - SPY H1 Sharpe          m_OOS = book OOS Sharpe - SPY OOS Sharpe
    m_H2  = book H2 Sharpe  - SPY H2 Sharpe
    m_DD  = book MaxDD - 0.60 x SPY MaxDD            (pp; >= 0 passes, the cap is a floor)
    m_CAGR= book CAGR  - 0.70 x SPY CAGR             (pp; >= 0 passes)
The deliverable is each margin's SPREAD (max - min) and SD across vintages BESIDE the margin
the record quotes, i.e. the number a reader would have to beat for the committed verdict to be
a fact about the rule rather than about the draw.

ARM B — THE CAPITAL ARM AND RULE 8 (required).  Both structural dials of the frozen book are
walked on every vintage: N {10, 16, 20, 25} x H {63, 126, 252} = 12 cells, 504 books.  The
record's standing chooser (argmax IS Sharpe, parameters chosen on warm-up..2016-12-31 ONLY,
2017-2026 read ONCE) is run SEPARATELY ON EACH VINTAGE and its pick compared across vintages,
against the do-nothing anchor (N=20, H=126).  The question this answers for capital is not
"which cell" but "how much of the committed choice is the draw": if the pick moves between two
tapes that differ only by a dividend re-adjustment, the committed pick is vintage luck of that
size.  Both KEEP paths are evaluated at every one of the 504 cells.

PRE-DECLARED OUTCOMES, written before any number in ARM A or ARM B was read:
  H_SMALL    the full-sample Sharpe spread across V_POSTFIX vintages is below 7.0e-3 (idea
             1335's own replay residual), i.e. the residual it found is NOT tape vintage.
  H_DD_SAFE  the U56 drawdown-cap margin exceeds its own vintage spread — the leg the record
             calls the binder survives the tape.
  H_NOFLIP   no 4b leg flips verdict on any V_POSTFIX vintage of U56.
  H_PICK     the IS-Sharpe chooser picks the same cell on at least 0.90 of V_POSTFIX vintages
             per panel.  The IS window ENDS in 2016 and every vintage covers it, so this can
             only fail through restatement — it is a direct test of whether the tape is an
             append or a rewrite.
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not ARM A.

GATES.  G0 every vintage carries >= 10 years.  G1 the 2026-09-16 vintage replays the committed
U56 anchor triple 15.7147% / 1.14804 / -19.1276% (idea 1265's gate G1, vintage-pinned to the
2026-09-16 cache) — the deviation is PUBLISHED, not asserted.  G2 determinism: the headline
cell recomputed bit for bit.  G3 the 14 vintages are 14 distinct blob hashes.  G4 all 504 ARM B
cells and all 84 ARM A cells published.  G5 exactly two tuned parameters (vintage, panel).
G6 the chooser reads no row at or after 2017-01-01, and OOS starts at the first index row on
or after it.  G7 under V_TRUNC every vintage of a panel ends on the same date.

PROTOCOL: rule 1 data and minimum sample; rule 2 costs (10 bps) and t+1 execution; rule 3
compare against the live RULES v2 baseline AND SPY, both rebuilt on each vintage; rule 4 both
KEEP paths at every cell; rule 5 one idea, one script, deterministic, standalone; rule 8 as
above; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before
anything is computed), so every absolute level here is optimistic and every 4b pass is an UPPER
bound.  The headline is a SPREAD ACROSS VINTAGES of the same book on the same names, so a level
bias common to the vintages cancels to first order; the pass COUNT does not.

Runs standalone and offline (this repository's own git objects and committed caches only):
  python research/backtests/2026-09-19_is-the-2026-09-04-KEEP-4b-PASS-TAPE-VINTAGE-ROBUST_B.py
"""
from __future__ import annotations

import gzip
import io
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import EXCLUDE, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-19"
SLUG = "is-the-2026-09-04-KEEP-4b-PASS-TAPE-VINTAGE-ROBUST"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                    # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]            # the committed RAW three-leg composite
N_LADDER = [10, 16, 20, 25]                      # ARM B structural dial 1
H_LADDER = [63, 126, 252]                        # ARM B structural dial 2
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)   # gate G1, pinned to the 2026-09-16 vintage
G1_VINTAGE_DATE = "2026-09-16"
FIXREV = "c006b439"                              # the calendar-day index fix
REPLAY_RESIDUAL = 7.0e-3                         # idea 1335's G1b half-sample residual

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
    n = len(r)
    h = n // 2
    hi = o // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                oos=stats(r[o:]), **{"is": stats(r[:o])},
                is_h1=stats(r[:hi]), is_h2=stats(r[hi:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ================================================================== the tape vintages
def git(*args) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True).stdout


def have(rev, path) -> bool:
    return subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{rev}:{path}"],
                          capture_output=True).returncode == 0


def blob(rev, path) -> str:
    return git("rev-parse", f"{rev}:{path}").decode().strip() if have(rev, path) else ""


def read_csv_rev(rev, path, gz=False) -> pd.DataFrame:
    raw = git("show", f"{rev}:{path}")
    if gz:
        raw = gzip.decompress(raw)
    return pd.read_csv(io.BytesIO(raw), index_col=0, parse_dates=True).sort_index()


def vintages():
    """Every commit that changed data/prices.csv, oldest first, with its co-committed panels."""
    revs = git("log", "--format=%H|%ad", "--date=short", "--", "data/prices.csv").decode().strip().split("\n")
    out = []
    order = list(reversed(revs))
    fix_i = next(i for i, x in enumerate(order) if x.split("|")[0].startswith(FIXREV))
    for i, line in enumerate(order):
        rev, d = line.split("|")
        out.append(dict(i=i, rev=rev, short=rev[:8], commit_date=d,
                        blob_px=blob(rev, "data/prices.csv"),
                        blob_broad=blob(rev, "data/prices_broad.csv"),
                        blob_small=blob(rev, "data/prices_small.csv.gz"),
                        postfix=i >= fix_i))
    return out


# ================================================================== panels, rebuilt per vintage
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


UNIV = sorted({t for g in json.loads((ROOT / "research" / "universe.json").read_text()).values()
               for t in g} - set(EXCLUDE))
_meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD_SMALL = set(_meta.loc[_meta.max_1d_move >= 1.0, "ticker"])


def panels_for(v, end=None):
    """The three standing panels as they stood at vintage v.  The universe DEFINITIONS
    (universe.json, small_meta.csv) are held at HEAD so the only thing that moves is the TAPE."""
    out = []
    raw = read_csv_rev(v["rev"], "data/prices.csv")
    keep = [c for c in UNIV if c in raw.columns]
    px = raw[keep].loc["2008-01-01":].dropna(how="all").ffill()
    if end is not None:
        px = px.loc[:end]
    out.append(("U56", px, [c for c in px.columns if c != "SPY"], len(UNIV) - len(keep),
                v["blob_px"][:8]))

    if v["blob_broad"]:
        rb = read_csv_rev(v["rev"], "data/prices_broad.csv")
        pb = rb.loc["2008-01-01":].dropna(how="all").ffill()
        if end is not None:
            pb = pb.loc[:end]
        if "SPY" in pb.columns:
            out.append(("BROAD", pb, [c for c in pb.columns if c != "SPY"], 0, v["blob_broad"][:8]))
    if v["blob_small"]:
        rs = read_csv_rev(v["rev"], "data/prices_small.csv.gz", gz=True)
        ps = rs.loc["2008-01-01":].dropna(how="all").ffill()
        spy = raw["SPY"].reindex(ps.index, method="ffill").rename("SPY")
        ps = pd.concat([ps.drop(columns=["SPY"], errors="ignore"), spy], axis=1)
        if end is not None:
            ps = ps.loc[:end]
        inv = [c for c in ps.columns if c != "SPY" and c not in BAD_SMALL]
        out.append(("SMALL", ps, inv, 0, v["blob_small"][:8]))
    return out


# ================================================================== the frozen book
def build(pan, N, H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0, equal slot weights.  Row t is the
    APPLICATION-time weight: decided t-lag, applied t."""
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


def margins_4b(b, spy):
    """Every 4b leg as a signed margin in its own unit.  >= 0 passes, by construction."""
    return dict(m4b_H1=b["h1"]["Sharpe"] - spy["h1"]["Sharpe"],
                m4b_H2=b["h2"]["Sharpe"] - spy["h2"]["Sharpe"],
                m4b_OOS=b["oos"]["Sharpe"] - spy["oos"]["Sharpe"],
                m4b_DD=(b["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]) * 100.0,
                m4b_CAGR=(b["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]) * 100.0)


def margins_4a(b, live):
    return dict(m4a_H1=b["h1"]["Sharpe"] - live["h1"]["Sharpe"],
                m4a_H2=b["h2"]["Sharpe"] - live["h2"]["Sharpe"],
                m4a_DD=(b["full"]["MaxDD"] - live["full"]["MaxDD"]) * 100.0)


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


M4B = ["m4b_H1", "m4b_H2", "m4b_OOS", "m4b_DD", "m4b_CAGR"]
M4A = ["m4a_H1", "m4a_H2", "m4a_DD"]
UNITS = {"m4b_H1": "Sharpe", "m4b_H2": "Sharpe", "m4b_OOS": "Sharpe", "m4b_DD": "pp",
         "m4b_CAGR": "pp", "m4a_H1": "Sharpe", "m4a_H2": "Sharpe", "m4a_DD": "pp"}


# ================================================================== main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1350 lane B — {SLUG}")
    say("# DIAL 1 vintage (every commit that changed data/prices.csv) x DIAL 2 panel {U56,B136,SMALL}")
    say("# controls, never chosen on: READING {V_RAW, V_TRUNC}, COHORT {V_ALL, V_POSTFIX}")
    say(f"# frozen book: RAW composite {LEGS}, gate = above 200d MA AND vol20 < {MAXVOL}, "
        f"N={A_N}, H={A_H}, GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")

    V = vintages()
    VD = pd.DataFrame(V)
    say(f"\n================ VINTAGES ({len(V)}) ================")
    for v in V:
        say(f"   {v['i']:2d} {v['short']} {v['commit_date']}  px={v['blob_px'][:8]} "
            f"broad={v['blob_broad'][:8] or '-':8s} small={v['blob_small'][:8] or '-':8s} "
            f"{'POSTFIX' if v['postfix'] else 'PRE-INDEX-FIX'}")
    gate("G3 distinct tape blobs", len({v["blob_px"] for v in V}), len(V),
         len({v["blob_px"] for v in V}) == len(V))

    # ---- the common end date for V_TRUNC, per panel (computed from the tapes themselves)
    ends = {}
    for v in V:
        for pname, px, inv, miss, tb in panels_for(v):
            ends.setdefault(pname, []).append(px.index[-1])
    COMMON = {k: min(x) for k, x in ends.items()}
    say("\n   V_TRUNC common end dates: " + "  ".join(f"{k}={str(x.date())}" for k, x in COMMON.items()))

    rows, arm_b, vinfo = [], [], []
    det_ref = None
    for v in V:
        loaded = panels_for(v)
        for reading in ("V_RAW", "V_TRUNC"):
            for pname, px0, inv, miss, tapeblob in loaded:
                px = px0 if reading == "V_RAW" else px0.loc[:COMMON[pname]]
                pan = Panel(pname, px, [c for c in inv if c in px.columns])
                idx = pan.idx[WARMUP:]
                o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
                spy = windows(pan.spy[WARMUP:], o)
                live_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
                live = windows(live_r, o)
                years = (idx[-1] - idx[0]).days / 365.25
                vinfo.append(dict(vi=v["i"], vintage=v["short"], commit_date=v["commit_date"], panel=pname,
                                  reading=reading, postfix=v["postfix"], rows=len(pan.idx),
                                  names=len(pan.iinv), missing_univ=miss, tape_blob=tapeblob,
                                  first=str(idx[0].date()),
                                  last=str(idx[-1].date()), years=years, is_rows=o,
                                  oos_rows=len(idx) - o,
                                  spy_full_CAGR=spy["full"]["CAGR"], spy_full_Sharpe=spy["full"]["Sharpe"],
                                  spy_full_MaxDD=spy["full"]["MaxDD"], spy_oos_Sharpe=spy["oos"]["Sharpe"],
                                  live_full_Sharpe=live["full"]["Sharpe"], blob=v["blob_px"][:8]))

                cellmap = {}
                for N in N_LADDER:
                    for Hh in H_LADDER:
                        W = build(pan, N, Hh)
                        r, turn = run(pan, W)
                        r = r[WARMUP:]
                        w = windows(r, o)
                        a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                        rec = dict(vi=v["i"], vintage=v["short"], commit_date=v["commit_date"], postfix=v["postfix"],
                                   panel=pname, reading=reading, tape_blob=tapeblob,
                                   N=N, H=Hh, **flat(w), turnover=turn,
                                   **margins_4b(w, spy), **margins_4a(w, live),
                                   keep4a=all(a4.values()), keep4b=all(b4.values()),
                                   fail4a=failed(a4), fail4b=failed(b4),
                                   is_anchor=(N == A_N and Hh == A_H),
                                   spy_full_Sharpe=spy["full"]["Sharpe"], spy_full_CAGR=spy["full"]["CAGR"],
                                   spy_full_MaxDD=spy["full"]["MaxDD"], spy_oos_Sharpe=spy["oos"]["Sharpe"],
                                   live_full_Sharpe=live["full"]["Sharpe"], years=years, rows=len(idx),
                                   names=len(pan.iinv))
                        rows.append(rec)
                        cellmap[(N, Hh)] = rec
                        if (reading == "V_RAW" and pname == "U56" and N == A_N and Hh == A_H
                                and v["commit_date"] == G1_VINTAGE_DATE and det_ref is None):
                            det_ref = (w["full"]["CAGR"], w["full"]["Sharpe"], w["full"]["MaxDD"])
                            W2 = build(pan, N, Hh)
                            r2, _ = run(pan, W2)
                            r2 = r2[WARMUP:]
                            gate("G2 determinism (U56 anchor, 2026-09-16 vintage)",
                                 f"max|dr| {np.abs(r2 - r).max():.3e}", "0.0",
                                 float(np.abs(r2 - r).max()) == 0.0)
                            gate("G1 committed anchor replay",
                                 f"CAGR {w['full']['CAGR']:.6f} Sharpe {w['full']['Sharpe']:.5f} "
                                 f"MaxDD {w['full']['MaxDD']:.6f}",
                                 f"{COMMITTED_U56[0]:.6f} / {COMMITTED_U56[1]:.5f} / {COMMITTED_U56[2]:.6f}",
                                 abs(w["full"]["Sharpe"] - COMMITTED_U56[1]) < 5e-3)

                # ---- ARM B chooser on this vintage (rule 8): IS only, 2017-2026 read once
                ks = list(cellmap)
                pick = max(ks, key=lambda k: (cellmap[k]["is_Sharpe"], -k[0], -k[1]))
                anc = cellmap[(A_N, A_H)]
                ch = cellmap[pick]
                arm_b.append(dict(vi=v["i"], vintage=v["short"], commit_date=v["commit_date"], postfix=v["postfix"],
                                  panel=pname, reading=reading, tape_blob=tapeblob,
                                  pick_N=pick[0], pick_H=pick[1],
                                  pick_is_Sharpe=ch["is_Sharpe"], pick_oos_Sharpe=ch["oos_Sharpe"],
                                  pick_oos_CAGR=ch["oos_CAGR"], pick_oos_MaxDD=ch["oos_MaxDD"],
                                  pick_keep4b=ch["keep4b"], pick_keep4a=ch["keep4a"],
                                  anchor_is_Sharpe=anc["is_Sharpe"], anchor_oos_Sharpe=anc["oos_Sharpe"],
                                  anchor_oos_CAGR=anc["oos_CAGR"], anchor_oos_MaxDD=anc["oos_MaxDD"],
                                  anchor_keep4b=anc["keep4b"], anchor_keep4a=anc["keep4a"],
                                  spy_oos_Sharpe=anc["spy_oos_Sharpe"],
                                  edge_oos=ch["oos_Sharpe"] - anc["oos_Sharpe"],
                                  is_margin=ch["is_Sharpe"] - anc["is_Sharpe"],
                                  n_keep4b=sum(c["keep4b"] for c in cellmap.values()),
                                  n_keep4a=sum(c["keep4a"] for c in cellmap.values())))
        del loaded
        say(f"   vintage {v['short']} {v['commit_date']} done  [{time.time()-t0:5.1f}s]")

    G = pd.DataFrame(rows)
    B = pd.DataFrame(arm_b)
    VI = pd.DataFrame(vinfo)
    G.to_csv(f"{STEM}.grid.csv", index=False, float_format="%.8f")
    B.to_csv(f"{STEM}.rule8.csv", index=False, float_format="%.8f")
    VI.to_csv(f"{STEM}.vintages.csv", index=False, float_format="%.8f")
    VD.to_csv(f"{STEM}.blobs.csv", index=False)
    gate("G0 min sample years", f"{VI.years.min():.1f}", ">= 10", VI.years.min() >= 10)
    for pname, sub in VI[VI.reading == "V_RAW"].groupby("panel"):
        say(f"   {pname}: {sub.vintage.nunique()} vintages, names {sub.names.min()}..{sub.names.max()}, "
            f"rows {sub.rows.min()}..{sub.rows.max()}, ends {sub.last.min()}..{sub.last.max()}")
    tr = G[G.reading == "V_TRUNC"]
    ok_trunc = all(tr[tr.panel == p].rows.nunique() >= 1 for p in tr.panel.unique())
    gate("G7 V_TRUNC common end", "; ".join(f"{p}={COMMON[p].date()}" for p in COMMON), "one per panel", ok_trunc)
    gate("G4 cells published", f"{len(G)} grid rows / {len(B)} rule-8 rows",
         f"{len(VI)*len(N_LADDER)*len(H_LADDER)} expected", len(G) == len(VI) * len(N_LADDER) * len(H_LADDER))
    gate("G5 tuned parameters", 2, 2, True)
    gate("G6 OOS boundary", f"OOS first row >= {OOS_START.date()} on every cell", "all",
         bool((VI.oos_rows > 0).all()))

    # ================================================================== ARM A0 — tape churn
    say("\n================ ARM A0 — HOW MUCH THE TAPE ITSELF MOVES ================")
    say("# overlapping (row, column) cells of data/prices.csv between CONSECUTIVE vintages")
    churn = []
    prev = None
    for v in V:
        cur = read_csv_rev(v["rev"], "data/prices.csv")
        if prev is not None:
            pv, pc = prev
            idxc = cur.index.intersection(pv.index)
            for colset, cols in (("ALL_COLS", cur.columns.intersection(pv.columns)),
                                 ("U56_COLS", pd.Index([c for c in UNIV if c in cur.columns
                                                        and c in pv.columns]))):
                a, b = pv.loc[idxc, cols], cur.loc[idxc, cols]
                d = (a - b).abs()
                rel = d / a.abs().replace(0, np.nan)
                n_cells = int(d.notna().sum().sum())
                n_diff = int((d > 1e-9).sum().sum())
                mx = float(np.nanmax(rel.values)) if n_cells else np.nan
                # RETURN SPACE is what a book actually feels: a back-adjustment multiplies a
                # whole pre-event price column by a constant, which cancels in pct_change
                # everywhere except the event day.  Price churn is an UPPER bound on it.
                dr = (a.pct_change() - b.pct_change()).abs()
                vals = dr.values[np.isfinite(dr.values)]
                big = vals[vals > 1e-9]
                churn.append(dict(frm=pc, to=v["short"], to_date=v["commit_date"], colset=colset,
                                  overlap_rows=len(idxc), overlap_cols=len(cols), cells=n_cells,
                                  n_diff=n_diff, share_diff=n_diff / max(n_cells, 1), max_rel=mx,
                                  n_ret_diff=int(len(big)),
                                  share_ret_diff=len(big) / max(n_cells, 1),
                                  med_abs_dret=float(np.median(big)) if len(big) else 0.0,
                                  p99_abs_dret=float(np.quantile(big, 0.99)) if len(big) else 0.0,
                                  n_ret_gt_1bp=int((vals > 1e-4).sum()),
                                  max_abs_dret=float(vals.max()) if len(vals) else np.nan,
                                  new_rows=int(len(cur.index.difference(pv.index))),
                                  postfix=v["postfix"]))
                say(f"   {pc} -> {v['short']} ({v['commit_date']}) {colset}: overlap "
                    f"{len(idxc)}x{len(cols)}, restated {n_diff:7d} px cells "
                    f"({n_diff/max(n_cells,1):6.2%}, max |rel| {mx:8.5f}); RETURN |dr|: "
                    f"median {np.median(big) if len(big) else 0:9.2e}  p99 "
                    f"{np.quantile(big, 0.99) if len(big) else 0:9.2e}  max "
                    f"{vals.max() if len(vals) else np.nan:8.6f}  cells>1bp "
                    f"{int((vals > 1e-4).sum()):5d}; new rows "
                    f"{len(cur.index.difference(pv.index))}")
        prev = (cur, v["short"])
    CH = pd.DataFrame(churn)
    CH.to_csv(f"{STEM}.churn.csv", index=False, float_format="%.10f")
    for colset, pf_ch in CH[CH.postfix].groupby("colset"):
        say(f"   POSTFIX steps {colset}: median restated PRICE share {pf_ch.share_diff.median():.2%} "
            f"(max |rel| {pf_ch.max_rel.max():.5f}); RETURN |dr| median "
            f"{pf_ch.med_abs_dret.median():.2e}, p99 {pf_ch.p99_abs_dret.max():.2e}, max "
            f"{pf_ch.max_abs_dret.max():.6f}; return cells moved by more than 1 bp per step: "
            f"{pf_ch.n_ret_gt_1bp.min()}..{pf_ch.n_ret_gt_1bp.max()} of "
            f"{int(pf_ch.cells.max())}; new rows per step {pf_ch.new_rows.min()}..{pf_ch.new_rows.max()}")

    # ================================================================== ARM A
    say("\n================ ARM A — THE SPREAD OF EVERY 4b MARGIN ACROSS VINTAGES ================")
    A = G[G.is_anchor].copy()
    spread_rows = []
    for (pname, reading), sub in A.groupby(["panel", "reading"]):
        for cohort, s in (("V_ALL", sub), ("V_POSTFIX", sub[sub.postfix])):
            if len(s) < 2:
                continue
            head = s.sort_values("vi").iloc[-1]
            for m in M4B + M4A + ["full_Sharpe", "full_CAGR", "full_MaxDD", "oos_Sharpe"]:
                x = s[m].astype(float)
                spread_rows.append(dict(panel=pname, reading=reading, cohort=cohort, leg=m,
                                        unit=UNITS.get(m, "level"), n=len(s),
                                        n_blobs=int(s.tape_blob.nunique()), v_head=float(head[m]),
                                        v_mean=float(x.mean()), v_sd=float(x.std(ddof=0)),
                                        v_min=float(x.min()), v_max=float(x.max()),
                                        v_spread=float(x.max() - x.min()),
                                        n_neg=int((x < 0).sum()) if m in M4B + M4A else -1,
                                        head_over_spread=(float(head[m]) / float(x.max() - x.min())
                                                          if x.max() > x.min() else np.inf)))
    SP = pd.DataFrame(spread_rows)
    SP.to_csv(f"{STEM}.spread.csv", index=False, float_format="%.8f")

    for pname in sorted(A.panel.unique()):
        say(f"\n## {pname} — frozen anchor (N={A_N}, H={A_H}, gross {A_G}) on every vintage")
        say("  reading  vintage   date        CAGR   Sharpe    MaxDD |   m_H1    m_H2   m_OOS "
            "|  m_DD   m_CAGR | 4a 4b | fail4b")
        for reading in ("V_RAW", "V_TRUNC"):
            s = A[(A.panel == pname) & (A.reading == reading)].sort_values("vi")
            for _, r in s.iterrows():
                say(f"  {reading:8s} {r.vintage} {r.commit_date} {r.full_CAGR:7.2%} "
                    f"{r.full_Sharpe:8.4f} {r.full_MaxDD:8.2%} | {r.m4b_H1:7.4f} {r.m4b_H2:7.4f} "
                    f"{r.m4b_OOS:7.4f} | {r.m4b_DD:6.2f} {r.m4b_CAGR:6.2f} | "
                    f"{'Y' if r.keep4a else 'n'}  {'Y' if r.keep4b else 'n'} | {r.fail4b}"
                    + ("" if r.postfix else "   [PRE-INDEX-FIX]"))
        for reading in ("V_RAW", "V_TRUNC"):
            for cohort in ("V_ALL", "V_POSTFIX"):
                s = SP[(SP.panel == pname) & (SP.reading == reading) & (SP.cohort == cohort)]
                if s.empty:
                    continue
                say(f"   SPREAD {reading} {cohort} (n={int(s.n.iloc[0])} vintages, "
                    f"{int(s.n_blobs.iloc[0])} distinct panel tapes):")
                for _, r in s[s.leg.isin(M4B)].iterrows():
                    say(f"      {r['leg']:9s} head {r['v_head']:8.4f} {r['unit']:6s}  "
                        f"spread {r['v_spread']:8.4f}  sd {r['v_sd']:8.4f}  min {r['v_min']:8.4f}  "
                        f"max {r['v_max']:8.4f}  head/spread {r['head_over_spread']:7.2f}  "
                        f"fails {int(r['n_neg'])}/{int(r['n'])}")
                lv = s[s.leg == "full_Sharpe"].iloc[0]
                say(f"      full_Sharpe level spread {lv['v_spread']:.4f} (sd {lv['v_sd']:.4f}) "
                    f"vs idea 1335's replay residual {REPLAY_RESIDUAL:.1e}")

    # ================================================================== ARM B
    say("\n================ ARM B — RULE 8: THE CHOOSER RUN ON EVERY VINTAGE ================")
    say(f"# grid N {N_LADDER} x H {H_LADDER}; chooser = argmax IS Sharpe on warm-up..{IS_END.date()};"
        " 2017-2026 read ONCE; anchor = do nothing")
    for pname in sorted(B.panel.unique()):
        for reading in ("V_RAW", "V_TRUNC"):
            s = B[(B.panel == pname) & (B.reading == reading)].sort_values("vi")
            if s.empty:
                continue
            say(f"\n## {pname} {reading}")
            say("   vintage   date       pick  IS Sh  | pick OOS Sh  anchor OOS Sh   edge | "
                "SPY OOS Sh | 4b: pick/anchor | 4b cells")
            for _, r in s.iterrows():
                say(f"   {r.vintage} {r.commit_date}  ({r.pick_N:2d},{r.pick_H:3d}) {r.pick_is_Sharpe:6.4f} | "
                    f"{r.pick_oos_Sharpe:11.4f} {r.anchor_oos_Sharpe:14.4f} {r.edge_oos:+7.4f} | "
                    f"{r.spy_oos_Sharpe:9.4f} | {'Y' if r.pick_keep4b else 'n'}/"
                    f"{'Y' if r.anchor_keep4b else 'n'} | {int(r.n_keep4b)}/{len(N_LADDER)*len(H_LADDER)}"
                    + ("" if r.postfix else "   [PRE-INDEX-FIX]"))
            for cohort, ss in (("V_ALL", s), ("V_POSTFIX", s[s.postfix])):
                if ss.empty:
                    continue
                picks = ss.apply(lambda r: (r.pick_N, r.pick_H), axis=1)
                mode = picks.value_counts()
                say(f"   {cohort}: distinct picks {picks.nunique()} "
                    f"({', '.join(f'{k}x{v}' for k, v in mode.items())}); "
                    f"modal share {mode.iloc[0]/len(ss):.3f}; "
                    f"pick OOS Sharpe {ss.pick_oos_Sharpe.min():.4f}..{ss.pick_oos_Sharpe.max():.4f} "
                    f"(spread {ss.pick_oos_Sharpe.max()-ss.pick_oos_Sharpe.min():.4f}); "
                    f"anchor OOS spread {ss.anchor_oos_Sharpe.max()-ss.anchor_oos_Sharpe.min():.4f}; "
                    f"mean edge {ss.edge_oos.mean():+.4f}; "
                    f"4b anchor passes {int(ss.anchor_keep4b.sum())}/{len(ss)}, "
                    f"pick {int(ss.pick_keep4b.sum())}/{len(ss)}; "
                    f"4a cells {int(ss.n_keep4a.sum())}")

    # ================================================================== pre-declared outcomes
    say("\n================ PRE-DECLARED OUTCOMES ================")
    pf = A[A.postfix]
    u_tr = pf[(pf.panel == "U56") & (pf.reading == "V_TRUNC")]
    u_rw = pf[(pf.panel == "U56") & (pf.reading == "V_RAW")]
    sp_tr = float(u_tr.full_Sharpe.max() - u_tr.full_Sharpe.min())
    sp_rw = float(u_rw.full_Sharpe.max() - u_rw.full_Sharpe.min())
    say(f"  H_SMALL    U56 full-Sharpe spread across V_POSTFIX vintages: "
        f"V_TRUNC {sp_tr:.4f}, V_RAW {sp_rw:.4f}  vs 1335's residual {REPLAY_RESIDUAL:.1e} -> "
        f"{'HOLDS' if max(sp_tr, sp_rw) < REPLAY_RESIDUAL else 'FIRES (vintage is the larger effect)'}")
    dd = u_tr.m4b_DD.astype(float)
    say(f"  H_DD_SAFE  U56 V_TRUNC DD-cap margin {dd.min():.2f}..{dd.max():.2f} pp "
        f"(head {float(u_tr.sort_values('vi').m4b_DD.iloc[-1]):.2f}), spread "
        f"{dd.max()-dd.min():.2f} pp -> "
        f"{'HOLDS (margin > spread)' if float(u_tr.sort_values('vi').m4b_DD.iloc[-1]) > (dd.max()-dd.min()) else 'FIRES (spread >= margin)'}")
    flips = {m: int((pf[(pf.panel == 'U56')][m].astype(float) < 0).sum()) for m in M4B}
    say(f"  H_NOFLIP   U56 V_POSTFIX leg failures (both readings): {flips} -> "
        f"{'HOLDS' if sum(flips.values()) == 0 else 'FIRES'}")
    bp = B[B.postfix]
    shares = []
    for (pname, reading), s in bp.groupby(["panel", "reading"]):
        picks = s.apply(lambda r: (r.pick_N, r.pick_H), axis=1)
        shares.append((pname, reading, picks.value_counts().iloc[0] / len(s), picks.nunique()))
    say("  H_PICK     modal-pick share per (panel, reading): "
        + "; ".join(f"{p}/{rd} {sh:.3f} ({nu} distinct)" for p, rd, sh, nu in shares)
        + f" -> {'HOLDS' if min(s[2] for s in shares) >= 0.90 else 'FIRES'}")

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\nGATES {int(GD.pass_.sum())}/{len(GD)} pass")
    say(f"artefacts: {STEM.name}.grid.csv / .rule8.csv / .spread.csv / .vintages.csv / .blobs.csv / .gates.csv")
    say(f"total {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
