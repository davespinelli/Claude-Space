#!/usr/bin/env python3
"""
Idea 1139 (lane B, 2026-09-18) — should a committed FLOOR-KEYED CLAIM be required to quote its
RUNG LIST rather than its RUNG COUNT?

WHY THIS IDEA.  1139 is the LAST numbered item standing in QUEUE.md's '## Open' section
(everything below it is lane annotation, not an idea) and the sprint's lane rule gives lane B the
last.  No eligibility skip is taken: the idea is price-only, answerable offline from the committed
caches, and lane B's own 1265 correction applies — a census CAN carry a rule-8 capital arm.  ARM C
is one, and it is not decorative: the floor-keyed trigger is rebuilt as an ACTUAL capital gate over
the record's own 9-rung H ladder on three panels, the pick is made on warm-up..2016-12-31 only and
2017-2026 is read ONCE.

THE PREMISE (idea 1131).  A whole-ladder INF_FLOOR trigger — a claim of the form "the floor of
statistic S over ladder L clears bar b" — is not merely rung-COUNT dependent (1118) but rung-CHOICE
dependent and NON-MONOTONE: U56 H/S_OOS fires on the full 9-rung ladder yet falls silent when
H=210 alone is added, and at matched k=4 only 0.6925 of C(9,4) subsets fire while 1110/1116's CORE
fires 16 of 16.  If that is right, a claim that publishes only "a 9-rung ladder" is UNCHECKABLE: a
reader cannot reconstruct the trigger, and two honest readers with different 9-rung lists get
different verdicts.

THE THREE ARMS, IN THE QUEUE'S OWN ORDER:
  A.  CENSUS — how many committed floor-keyed rows would the proposed clause make checkable?
      Mechanical, over the committed prose record.  The queue quotes 2,571 floor-keyed rows with
      935 stating no rung set; this run builds its OWN detector and publishes its OWN denominator
      beside the queue's figure rather than inheriting it (idea 894's stamp request is honoured).
  B.  MECHANISM ON REAL BOOKS — is the COUNT sufficient?  Rebuild the H ladder on three panels and
      measure, at every matched k, the SHARE of C(9,k) rung subsets that fire the trigger.  If that
      share is strictly between 0 and 1 the count does not determine the verdict and the clause is
      NECESSARY; if it is 0 or 1 everywhere the count suffices and the clause is unnecessary.
      The ADD-ONE-RUNG test (H=210, 1131's own rung) is run separately.
  C.  CAPITAL (PROTOCOL rule 8, required) — is a floor-keyed trigger worth money?  The trigger is
      used as a real GO / NO-GO gate: floor of IS Sharpe over rung subset R >= SPY's IS Sharpe ->
      allocate to the IS-argmax H rung inside R; else DO NOTHING (hold the live RULES v2 book).
      Every one of the 511 non-empty subsets is a decision, made IS-only, read OOS once.  Both KEEP
      paths at every rung and for every chooser outcome.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    CLAIM_SET {CORE, WIDE}
        CORE  research/LEADERBOARD.md + research/CHANGELOG.md — the record's two committed ledgers.
        WIDE  CORE plus every committed research/*.md and research/backtests/*.md memo.
    REQUIRED_COLS {R_LIST, R_LIST_PLUS}
        R_LIST       the clause requires the rung LIST (the explicit rung values) beside the claim.
        R_LIST_PLUS  the rung LIST *and* the ladder's AXIS name *and* the STATISTIC the floor is
                     taken over — the three fields a reader needs to re-solve the trigger.
    2 x 2 = 4 census cells, EVERY ONE published.

NOT A DIAL, reported at every value (controls): PANEL {U56, B136, SMALL663}; ladder = the
record's committed 9-rung H ladder H in {5,10,21,42,63,90,126,189,252} (1277's own list), EXT
adds 1131's H=210.  FLOOR STATISTIC, six values, each carrying PROTOCOL 4b's OWN bar for that
leg so that nothing here is tuned: S_IS / S_OOS / S_FULL (Sharpe vs SPY's on the same window),
S_DD (MaxDD vs the 0.60 x SPY cap), S_CAGR (CAGR vs the 0.70 x SPY floor) and S_4B (the whole
4b verdict; the floor is the AND over rungs).  ARM C GATE KEY, two values, both IS-only and both
reported: G_SHARPE (floor of IS Sharpe vs SPY's IS Sharpe) and G_DD (floor of IS MaxDD vs the
0.60 x SPY IS cap).  A FIRST RUN of this script keyed the trigger on the Sharpe legs alone and
found every one of them SATURATED — every rung of the ladder clears SPY on every Sharpe window,
so the floor fires at 100% of subsets and the rung COUNT trivially determines the verdict.  That
saturation is a RESULT and is published below; the drawdown and verdict legs are the ones with
any discrimination in them, and they are what the clause has to be priced on.

PRE-DECLARED OUTCOMES, written before any number was read:
  H_UNCHECKABLE  a MAJORITY of the record's committed floor-keyed claims state neither a rung LIST
                 nor a rung COUNT, i.e. cannot be checked at all.
  H_COUNT_INSUFF in ARM B the matched-k fire share is strictly inside (0,1) at some k on some
                 (panel, statistic) cell — the rung COUNT does not determine the verdict.
  H_NONMONOTONE  adding H=210 to a firing full ladder silences it on at least one cell.
  H_CAPITAL      the gate is worth nothing: mean OOS Sharpe of gate-minus-do-nothing <= +0.02 and
                 no subset's chosen book passes 4b.
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not ARM A.

GATES.  G1 fast runner == engine.backtest on the anchor book.  G2 determinism: the anchor cell is
rebuilt and re-run from scratch on every panel and compared BIT FOR BIT (the scope is one cell
per panel, not the whole table — stated rather than overclaimed).  G3 IS and OOS windows are disjoint and OOS starts on or after 2017-01-01.
G4 the IS chooser reads NO OOS row (recomputed on a return vector whose OOS tail is NaN).  G5 the
BASE ladder is a subset of the EXT ladder and the anchor H=126 lies on both.  G6 every census share
lies in [0,1] and every denominator is > 0.  G7 the floor is MONOTONE in the rung set: floor over a
superset <= floor over any of its subsets, checked on all 511 subsets x 3 panels x 3 statistics.
G8 census denominator stamped with (file count, tree sha) per idea 894.

PROTOCOL: rule 2 costs (10 bps) and t+1 execution; rule 4 both KEEP paths at EVERY rung; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).  Every
absolute level in ARM B/C is optimistic and every 4b pass is an UPPER bound.  The ARM B headline is
a CONTRAST between rung SUBSETS of one ladder on one tape, so a level bias common to the panel moves
every subset together and the rung-choice finding is first-order immune; the 4b counts are not, and
are quoted as upper bounds.  ARM A re-reads committed prose and changes no number in it.

Runs standalone and offline (committed caches and committed prose only):
  python research/backtests/2026-09-18_should-a-committed-FLOOR-KEYED-CLAIM-be-required-to-quote-its-RUNG-LIST-rather-than-its-RUNG-COUNT_B.py
"""
from __future__ import annotations

import itertools
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "should-a-committed-FLOOR-KEYED-CLAIM-be-required-to-quote-its-RUNG-LIST-rather-than-its-RUNG-COUNT"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"

COST, WARMUP = 10.0, 260
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_MV, A_G = 20, 126, 0.60, 0.75           # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]               # committed RAW three-leg composite
H_BASE = [5, 10, 21, 42, 63, 90, 126, 189, 252]     # 1277's committed 9-rung H ladder
H_EXT = sorted(H_BASE + [210])                      # 1131's added rung
STATS6 = ["S_IS", "S_OOS", "S_FULL", "S_DD", "S_CAGR", "S_4B"]
CLAIM_SETS = ["CORE", "WIDE"]
REQ_COLS = ["R_LIST", "R_LIST_PLUS"]

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
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                oos=stats(r[o:]), **{"is": stats(r[:o])})


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


# ================================================================== book machinery
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
        self.above = (q > q.rolling(200).mean()).values
        self.vol20 = np.nan_to_num((q.pct_change().rolling(20).std() * np.sqrt(252)).values,
                                   nan=1e9)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)

    def elig(self, maxvol):
        return self.above & (self.vol20 < maxvol)


def build(pan, N, H, maxvol, lag=1):
    """Selection frame at GROSS = 1.0, equal slot weights.  Row t = APPLICATION-time weight
    (decided t-lag, applied t).  Minimum hold H trading days."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    el = pan.elig(maxvol)
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
            k[~(el[ts] & pr[ts])] = np.inf
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
    gr = (held * rets).sum(axis=1)
    r = gr - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0))


# ================================================================== ARM A — the census
# A FLOOR-KEYED sentence: it asserts something about the WORST / MINIMUM / EVERY member of a
# ladder, or names a floor/INF trigger explicitly.
FLOOR_RE = re.compile(
    r"[^.\n]*\b("
    r"inf_floor|floor|worst rung|worst[- ]case rung|every rung|all rungs|at every rung|"
    r"no rung|minimum over|min over|infimum|floor of|holds at (?:all|every)|"
    r"at \d+ of \d+ rungs|monotone (?:in|over) the ladder"
    r")\b[^.\n]*", re.I)
# a RUNG LIST: two or more explicit rung values, slash- comma- or brace-separated, or a bracketed
# python-style list.
LIST_RE = re.compile(
    r"(\[[^\]\n]*[,][^\]\n]*\]|\{[^}\n]*,[^}\n]*\}|"
    r"\b\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?)")
# a RUNG COUNT only: "9-rung", "all 9 rungs", "9 of 9", "16 of 16", "C(9,4)"
COUNT_RE = re.compile(r"(\b\d+[- ]rung\b|\ball \d+ rungs?\b|\b\d+ of \d+\b|\bC\(\d+\s*,\s*\d+\))",
                      re.I)
AXIS_RE = re.compile(r"\b(H|N|k|n/k|GROSS|MAXVOL|BAND|COST|CADENCE|LADDER|q|L)\b")
# RUNG CONTEXT: the sentence is about a LADDER, not merely about a bar that happens to be
# called a "floor" (the record calls 4b's CAGR leg "the CAGR floor" and 877's seed bar "the
# seed floor" — neither is a ladder claim).  Reported as a STRICT denominator beside the wide
# one; the clause can only bind on sentences that name a ladder at all.
RUNGCTX_RE = re.compile(r"\b(rungs?|ladder|grid|sweep|every (?:cell|point)|all \d+ (?:cells|points))\b",
                        re.I)
STATF_RE = re.compile(r"\b(sharpe|cagr|maxdd|dd|calmar|turnover|drag|s_oos|s_is|rho|b_sd|ulcer)\b",
                      re.I)


def census_files(claim_set):
    core = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    core = [f for f in core if f.exists()]
    if claim_set == "CORE":
        return core
    wide = sorted(set(core) | set((ROOT / "research").glob("*.md"))
                  | set(OUT.glob("*.md")))
    return sorted(wide)


def census(claim_set):
    rows = []
    files = census_files(claim_set)
    for f in files:
        try:
            txt = f.read_text(errors="replace")
        except Exception:
            continue
        for ln, line in enumerate(txt.split("\n"), 1):
            for m in FLOOR_RE.finditer(line):
                s = m.group(0).strip()
                if len(s) < 25:
                    continue
                rows.append(dict(file=f.name, line=ln,
                                 has_list=bool(LIST_RE.search(s)),
                                 has_count=bool(COUNT_RE.search(s)),
                                 has_axis=bool(AXIS_RE.search(s)),
                                 has_stat=bool(STATF_RE.search(s)),
                                 has_rungctx=bool(RUNGCTX_RE.search(s)),
                                 text=s[:300]))
    return pd.DataFrame(rows), files


def tree_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                       text=True).strip()[:12]
    except Exception:
        return "unknown"


# ================================================================== main
def main():
    say(f"# Idea 1139 — {SLUG}")
    say(f"# lane B, {DATE}.  Costs {COST:.0f} bps, t+1 execution, warm-up {WARMUP} rows, "
        f"OOS from {OOS_START.date()} read ONCE.")

    # ---------------------------------------------------------------- ARM A
    say("\n================ ARM A — CENSUS OF COMMITTED FLOOR-KEYED CLAIMS ================")
    sha = tree_sha()
    cen_rows = []
    cen_tables = {}
    for cs in CLAIM_SETS:
        df, files = census(cs)
        cen_tables[cs] = df
        n = len(df)
        gate(f"G8 {cs} census stamp", f"{len(files)} files, tree {sha}", "> 0 files", len(files) > 0)
        if n == 0:
            say(f"   {cs}: NO floor-keyed sentences detected — nothing to price.")
            continue
        for rq in REQ_COLS:
            if rq == "R_LIST":
                ok = df.has_list
            else:
                ok = df.has_list & df.has_axis & df.has_stat
            checkable = int(ok.sum())
            count_only = int((~df.has_list & df.has_count).sum())
            nothing = int((~df.has_list & ~df.has_count).sum())
            share = checkable / n
            lad = df[df.has_rungctx]
            nl = len(lad)
            ok_l = (lad.has_list if rq == "R_LIST"
                    else (lad.has_list & lad.has_axis & lad.has_stat))
            cen_rows.append(dict(claim_set=cs, required=rq, n_files=len(files), n_claims=n,
                                 n_ladder_claims=nl,
                                 ladder_checkable=int(ok_l.sum()) if nl else 0,
                                 ladder_share_checkable=(float(ok_l.mean()) if nl else float("nan")),
                                 ladder_count_only=(int((~lad.has_list & lad.has_count).sum())
                                                    if nl else 0),
                                 checkable=checkable, share_checkable=share,
                                 count_only=count_only, share_count_only=count_only / n,
                                 nothing=nothing, share_nothing=nothing / n,
                                 would_become_checkable=n - checkable,
                                 share_would=(n - checkable) / n))
            say(f"   {cs:5s} {rq:12s}  claims {n:6d}  checkable NOW {checkable:6d} "
                f"({share:6.1%})  COUNT-only {count_only:6d} ({count_only/n:6.1%})  "
                f"NEITHER {nothing:6d} ({nothing/n:6.1%})  clause would newly require "
                f"{n-checkable:6d} ({(n-checkable)/n:6.1%})")
            if nl:
                say(f"         STRICT (sentence names a ladder/rung at all): {nl:6d} claims  "
                    f"checkable NOW {int(ok_l.sum()):5d} ({ok_l.mean():6.1%})  COUNT-only "
                    f"{int((~lad.has_list & lad.has_count).sum()):5d} "
                    f"({float((~lad.has_list & lad.has_count).mean()):6.1%})")
    cen = pd.DataFrame(cen_rows)
    if len(cen):
        cen.to_csv(f"{STEM}.census.csv", index=False)
        good = bool(((cen.share_checkable >= 0) & (cen.share_checkable <= 1)).all()
                    and (cen.n_claims > 0).all())
        gate("G6 census shares in [0,1], denominators > 0", "all cells", "True", good)
        maj = float(cen.loc[cen.required == "R_LIST", "share_nothing"].max())
        say(f"   H_UNCHECKABLE (majority state NEITHER list nor count): "
            f"max share_nothing {maj:.1%} -> {'FIRES' if maj > 0.5 else 'DOES NOT FIRE'}")
    for cs, df in cen_tables.items():
        if len(df):
            df.to_csv(f"{STEM}.claims_{cs}.csv.gz", index=False, compression="gzip")

    # ---------------------------------------------------------------- panels
    say("\n================ PANELS ================")
    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    gate("G5 BASE ladder subset of EXT, anchor on both",
         f"base {H_BASE} ext {H_EXT} anchor {A_H}", "True",
         set(H_BASE).issubset(set(H_EXT)) and A_H in H_BASE and A_H in H_EXT)

    grid, subrows, decisions = [], [], []
    g1_done = False
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        spy = windows(pan.spy[WARMUP:], o)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].values[WARMUP:]
        live = windows(live_r, o)
        gate(f"G3 {pname} IS/OOS split",
             f"IS ends {idx[o-1].date()}, OOS starts {idx[o].date()}", ">= 2017-01-01",
             idx[o] >= OOS_START and idx[o - 1] < OOS_START)

        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"{idx[0].date()}..{idx[-1].date()}  IS {o} / OOS {len(idx)-o} rows")
        say(f"   SPY       full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}  halves {spy['h1']['Sharpe']:.4f}/"
            f"{spy['h2']['Sharpe']:.4f}  IS {spy['is']['Sharpe']:.4f}  OOS "
            f"{spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   RULESv2   full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}  halves {live['h1']['Sharpe']:.4f}/"
            f"{live['h2']['Sharpe']:.4f}  IS {live['is']['Sharpe']:.4f}  OOS "
            f"{live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")

        # G2 determinism: the anchor cell, rebuilt and re-run from scratch, bit for bit.
        r_a1 = run(pan, build(pan, A_N, A_H, A_MV), A_G)[0]
        r_a2 = run(pan, build(pan, A_N, A_H, A_MV), A_G)[0]
        gate(f"G2 {pname} anchor cell deterministic (rebuild + rerun)",
             f"{int((r_a1 != r_a2).sum())} differing rows of {len(r_a1)}", "0 (bit for bit)",
             bool((r_a1 == r_a2).all()))

        rungs = {}
        say(f"\n   {'H':>5s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
            f"{'IS_S':>7s} {'OOS_S':>7s} {'OOS_CAGR':>9s} {'OOS_DD':>8s} {'turn':>6s} "
            f"{'4a':>4s} {'4b':>4s}  fails4b")
        for H in H_EXT:
            W = build(pan, A_N, H, A_MV)
            r, tn = run(pan, W, A_G)
            r = r[WARMUP:]
            w = windows(r, o)
            if not g1_done and H == A_H:
                wdf = pd.DataFrame(A_G * W, index=pan.idx, columns=pan.px.columns)
                eng = backtest(pan.px, wdf.shift(-1), cost_bps=COST, freq="W")["returns"].values
                d = float(np.nanmax(np.abs(eng[1:] - (run(pan, W, A_G)[0])[1:])))
                gate("G1 fast runner == engine.backtest (anchor H=126)", f"{d:.2e}", "< 1e-9",
                     d < 1e-9)
                g1_done = True
            a = legs_4a(w, live)
            b = legs_4b(w, spy)
            rungs[H] = w
            grid.append(dict(panel=pname, H=H, **{f"{k}_{m}": v[m] for k, v in w.items()
                                                  for m in ("CAGR", "Sharpe", "MaxDD")},
                             turnover=tn, pass4a=all(a.values()), pass4b=all(b.values()),
                             fails4a=failed(a), fails4b=failed(b),
                             in_base=H in H_BASE))
            say(f"   {H:5d} {w['full']['CAGR']:8.2%} {w['full']['Sharpe']:8.4f} "
                f"{w['full']['MaxDD']:8.2%} {w['h1']['Sharpe']:7.4f} {w['h2']['Sharpe']:7.4f} "
                f"{w['is']['Sharpe']:7.4f} {w['oos']['Sharpe']:7.4f} {w['oos']['CAGR']:9.2%} "
                f"{w['oos']['MaxDD']:8.2%} {tn:6.2f} "
                f"{'Y' if all(a.values()) else 'n':>4s} {'Y' if all(b.values()) else 'n':>4s}"
                f"  {failed(b)}")

        # ------------------------------------------------ ARM B: rung-subset fire shares
        # Each floor statistic carries PROTOCOL 4b's OWN bar for that leg.  Nothing here is
        # tuned: S_IS/S_OOS/S_FULL are the Sharpe legs, S_DD the 0.60 x SPY drawdown cap,
        # S_CAGR the 0.70 x SPY CAGR floor, S_4B the whole verdict (floor = AND over rungs).
        bar = {"S_IS": spy["is"]["Sharpe"], "S_OOS": spy["oos"]["Sharpe"],
               "S_FULL": spy["full"]["Sharpe"],
               "S_DD": DD_CAP * spy["full"]["MaxDD"],
               "S_CAGR": CAGR_FLOOR * spy["full"]["CAGR"],
               "S_4B": 0.5}
        allH = H_BASE + [210]
        val = {"S_IS": {H: rungs[H]["is"]["Sharpe"] for H in allH},
               "S_OOS": {H: rungs[H]["oos"]["Sharpe"] for H in allH},
               "S_FULL": {H: rungs[H]["full"]["Sharpe"] for H in allH},
               "S_DD": {H: rungs[H]["full"]["MaxDD"] for H in allH},
               "S_CAGR": {H: rungs[H]["full"]["CAGR"] for H in allH},
               "S_4B": {H: float(all(legs_4b(rungs[H], spy).values())) for H in allH}}
        say(f"\n   ARM B — INF_FLOOR trigger, bar = SPY's own Sharpe on the same window")
        mono_ok = True
        for st in STATS6:
            v = {h: val[st][h] for h in H_BASE}
            full_floor = min(v.values())
            fires_full = full_floor > bar[st]
            ext_floor = min(val[st][h] for h in H_EXT)
            fires_ext = ext_floor > bar[st]
            say(f"    {st:7s} bar {bar[st]:7.4f}  FULL-9 floor {full_floor:7.4f} -> "
                f"{'FIRES' if fires_full else 'silent':6s} | +H210 floor {ext_floor:7.4f} -> "
                f"{'FIRES' if fires_ext else 'silent':6s}"
                f"{'   *** NON-MONOTONE SILENCING ***' if fires_full and not fires_ext else ''}")
            for k in range(1, 10):
                subs = list(itertools.combinations(H_BASE, k))
                fl = np.array([min(v[h] for h in s) for s in subs])
                fire = fl > bar[st]
                subrows.append(dict(panel=pname, stat=st, k=k, n_subsets=len(subs),
                                    n_fire=int(fire.sum()), share_fire=float(fire.mean()),
                                    floor_min=float(fl.min()), floor_max=float(fl.max()),
                                    bar=bar[st], count_determines=bool(fire.all() or not fire.any())))
                say(f"       k={k}  C(9,{k})={len(subs):3d}  fire {int(fire.sum()):3d} "
                    f"({fire.mean():6.1%})  floor range [{fl.min():.4f}, {fl.max():.4f}]  "
                    f"COUNT {'determines' if (fire.all() or not fire.any()) else 'DOES NOT determine'}")
            # G7 monotonicity: floor over superset <= floor over subset
            for k in range(1, 9):
                for s in itertools.combinations(H_BASE, k):
                    sup = min(v[h] for h in s)
                    for h2 in H_BASE:
                        if h2 in s:
                            continue
                        if min(v[h] for h in (s + (h2,))) > sup + 1e-12:
                            mono_ok = False
        gate(f"G7 {pname} floor monotone in the rung set", "all 511 subsets x 6 statistics",
             "True", mono_ok)

        # ------------------------------------------------ ARM C: the capital gate
        say(f"\n   ARM C — CAPITAL GATE (rule 8).  Gate key K: floor over rung subset R of an "
            f"IS-ONLY statistic clears its 4b bar -> allocate to the IS-Sharpe-argmax H in R; "
            f"else DO NOTHING (hold the live RULES v2 book).  Both keys reported.")
        isv = {H: rungs[H]["is"]["Sharpe"] for H in H_BASE}
        isdd = {H: rungs[H]["is"]["MaxDD"] for H in H_BASE}
        GKEYS = {"G_SHARPE": (isv, spy["is"]["Sharpe"]),
                 "G_DD": (isdd, DD_CAP * spy["is"]["MaxDD"])}
        # G4: the chooser reads no OOS row
        chk = []
        for H in H_BASE:
            W = build(pan, A_N, H, A_MV)
            r_all = run(pan, W, A_G)[0][WARMUP:]
            masked = r_all.copy().astype(float)
            masked[o:] = np.nan
            chk.append(abs(sharpe(masked[:o]) - isv[H]))
        gate(f"G4 {pname} IS chooser reads no OOS row", f"{max(chk):.2e}", "< 1e-12",
             max(chk) < 1e-12)

        nothing = live
        rows_p = []
        for gk, (gv, gbar) in GKEYS.items():
            for k in range(1, 10):
                for sset in itertools.combinations(H_BASE, k):
                    floor = min(gv[h] for h in sset)
                    go = floor >= gbar
                    pick = max(sset, key=lambda h: isv[h]) if go else None
                    bk = rungs[pick] if go else nothing
                    a = legs_4a(bk, live)
                    b = legs_4b(bk, spy)
                    rows_p.append(dict(panel=pname, gate_key=gk, k=k,
                                       subset="|".join(str(x) for x in sset),
                                       is_floor=floor, bar=gbar, go=go, pick=pick if go else 0,
                                       oos_CAGR=bk["oos"]["CAGR"], oos_Sharpe=bk["oos"]["Sharpe"],
                                       oos_MaxDD=bk["oos"]["MaxDD"],
                                       full_CAGR=bk["full"]["CAGR"],
                                       full_Sharpe=bk["full"]["Sharpe"],
                                       full_MaxDD=bk["full"]["MaxDD"],
                                       h1=bk["h1"]["Sharpe"], h2=bk["h2"]["Sharpe"],
                                       pass4a=all(a.values()), pass4b=all(b.values()),
                                       fails4b=failed(b),
                                       d_oos_vs_nothing=bk["oos"]["Sharpe"] - nothing["oos"]["Sharpe"],
                                       d_oos_vs_anchor=bk["oos"]["Sharpe"] - rungs[A_H]["oos"]["Sharpe"]))
        dp = pd.DataFrame(rows_p)
        decisions.append(dp)
        always = max(H_BASE, key=lambda h: isv[h])       # ignore the gate, always act
        say(f"    do-nothing OOS {nothing['oos']['Sharpe']:.4f} | always-act (IS-argmax "
            f"H={always}) {rungs[always]['oos']['Sharpe']:.4f} | anchor H={A_H} "
            f"{rungs[A_H]['oos']['Sharpe']:.4f} | SPY {spy['oos']['Sharpe']:.4f}")
        for gk in GKEYS:
            d = dp[dp.gate_key == gk]
            say(f"    {gk:9s} decisions {len(d):3d}  GO {int(d.go.sum()):3d} ({d.go.mean():6.1%})"
                f"  picks {sorted(set(int(x) for x in d.loc[d.go, 'pick']))}"
                f"  OOS Sharpe mean {d.oos_Sharpe.mean():.4f}"
                f"  gate-minus-do-nothing mean {d.d_oos_vs_nothing.mean():+.4f} "
                f"[{d.d_oos_vs_nothing.min():+.4f}, {d.d_oos_vs_nothing.max():+.4f}] "
                f"pos {int((d.d_oos_vs_nothing>0).sum())}/{len(d)}"
                f"  4a {int(d.pass4a.sum())}/{len(d)}  4b {int(d.pass4b.sum())}/{len(d)}")

    gdf = pd.DataFrame(grid)
    gdf.to_csv(f"{STEM}.grid.csv", index=False)
    sdf = pd.DataFrame(subrows)
    sdf.to_csv(f"{STEM}.subsets.csv", index=False)
    ddf = pd.concat(decisions, ignore_index=True)
    ddf.to_csv(f"{STEM}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- summary
    say("\n================ SUMMARY ================")
    ndet = int((~sdf.count_determines).sum())
    say(f"ARM B  (panel,stat,k) cells where the rung COUNT does NOT determine the verdict: "
        f"{ndet} of {len(sdf)} ({ndet/len(sdf):.1%})  -> H_COUNT_INSUFF "
        f"{'FIRES' if ndet > 0 else 'DOES NOT FIRE'}")
    for gk, d in ddf.groupby("gate_key"):
        say(f"ARM C  {gk:9s} 4a PASS {int(d.pass4a.sum())} of {len(d)};  4b PASS "
            f"{int(d.pass4b.sum())} of {len(d)};  mean gate-minus-do-nothing OOS Sharpe "
            f"{d.d_oos_vs_nothing.mean():+.4f};  GO {int(d.go.sum())} of {len(d)}")
    say(f"ARM C  H_CAPITAL (mean gate-minus-do-nothing <= +0.02 AND no 4b pass): "
        f"{'FIRES' if ddf.d_oos_vs_nothing.mean() <= 0.02 and ddf.pass4b.sum() == 0 else 'DOES NOT FIRE'}")
    say(f"ARM C  grid rungs passing 4b outright: {int(gdf.pass4b.sum())} of {len(gdf)}; "
        f"4a: {int(gdf.pass4a.sum())} of {len(gdf)}")
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    say(f"GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} passing")
    say(f"artefacts -> {STEM.name}.*")


if __name__ == "__main__":
    main()
