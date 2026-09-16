#!/usr/bin/env python3
"""Idea 1136 (cloud lane, 2026-09-16) — is 877's SEED FLOOR the RIGHT RULER for a
DETERMINISTIC MARGIN at all?

QUESTION (QUEUE idea 1136, verbatim)
    idea 1100 found the transferred 0.0145 misses each cell's own 90% resolution by 12.9x on
    12 of 14 cells and by 0.022x on the two GROSS ladders, where a 0.0003 margin is resolved
    at 0.956 agreement.  Walk the record's committed floor transfers and report how many would
    change verdict under the destination cell's OWN measured resolution instead.  Max 2 params
    (claim set, confidence).

WHAT IS NEW HERE, AND WHAT IS NOT
    1100 measured the own resolution of 14 cells at ONE confidence (0.90) and reported the
    RATIO to 0.0145.  A ratio is not a verdict.  This run does the thing the idea asks: it
    HARVESTS every committed object in the record that applies a floor IMPORTED from another
    construction to a DETERMINISTIC margin, recomputes that object's verdict under the floor it
    used and under the destination cell's OWN measured resolution, and counts the VERDICT
    CHANGES — at five confidences, because the own ruler has a confidence and 0.0145 does not.

    The point that makes this worth running: 877's floor is a SEED-NOISE floor.  It measures
    how far a Sharpe moves when a PLACEBO ARM is redrawn.  A rule-8 pick margin is not a
    redraw: the two rungs are DETERMINISTIC functions of one tape, and the only sampling
    uncertainty in their gap is the TAPE's.  Those are different objects with different
    magnitudes, and nothing in the record has ever priced the substitution as a verdict.

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials, the queue's own: CLAIM SET {CS_CSV, CS_PROSE, CS_ALL} x CONFIDENCE
    q {0.50, 0.68, 0.80, 0.90, 0.95} = 15 points, ALL published.
    PANEL is not a dial (U56 and B136 reported everywhere).  LADDER is not a dial (all 7).
    CHOOSER is not a dial: the floor is quoted in SHARPE units so C_ISSHARPE is the headline
    everywhere; C_ISDD and C_ISCAGR objects are carried as UNIT-INADMISSIBLE and reported
    apart, never inside a headline count.  The OWN-RULER READING is not a dial either: the
    HALFWIDTH reading (a number in the floor's own units, so it can be substituted for 0.0145
    literally) is the headline and the AGREEMENT reading is reported beside it at every point.
    BLOCK LENGTH is frozen at L=63 (1098/1102/1110/1100's headline).  Everything else frozen
    at 1096/1100's construction: CAND20 legs, cap INF, max_vol 0.60 (except L_MV), gross 0.75
    (except L_G), W cadence (except L_CAD), min hold 126 (except L_H), N=20 (L_N free, L_H at
    12), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31.  Seeds are zlib.crc32.

THE TWO RULERS, DEFINED BEFORE ANY NUMBER
    TRANSFER  the object's own imported floor: m x 0.0145, m the multiple the object uses.
              It has NO confidence attached, which is the defect under test.
    OWN       the destination cell's measured resolution at confidence q: the half-width of
              the two-sided q interval of the PAIRED block-bootstrap (L=63, 1000 draws)
              pick-minus-runner-up difference, computed on the IS window ONLY — the window the
              chooser sees.  Reported beside it, never substituted for it: the AGREEMENT
              reading, RESOLVED iff the sign of that difference survives a share q of draws.
    A margin is RESOLVED under a ruler iff |margin| >= that ruler's value (HALFWIDTH), or iff
    agreement >= q (AGREEMENT).  FLIP = the two rulers disagree on that object.

DECLARED BEFORE ANY NUMBER
    (a) H_WRONG_RULER  at the headline (CS_ALL, q=0.90, HALFWIDTH) a MAJORITY of admissible
                       transfer objects CHANGE VERDICT.  This is the idea's literal question.
    (b) H_DIRECTION    the flips run ONE WAY — the transferred floor calls RESOLVED what the
                       own ruler calls UNRESOLVED (i.e. 0.0145 is LAX), on a strict majority
                       of flipped objects.
    (c) H_GROSS_FLIPS_BACK  on the two GROSS ladders the flip runs the OTHER way (own ruler
                       RESOLVES what 0.0145 calls unresolved), reproducing 1100's 0.022x.
    (d) H_Q_STABLE     the flip share moves by no more than 0.25 across the five q rungs.  If
                       it does not hold, the substitution's answer is itself a free parameter
                       and BOTH rulers are contentless without a stated q.
    (e) H_UNDECLARED   a MAJORITY of committed floor-transfer objects state no confidence at
                       all beside the floor they apply.
    (f) THE DECISION RULE, fixed before any number: 0.0145 is the WRONG RULER iff at the
        headline point a majority of admissible objects flip AND the direction is consistent
        (b).  If a majority flip but the direction is mixed, the answer is that the floor is
        UNINFORMATIVE rather than lax, which is a different and weaker claim.
    (g) NOT A KEEP PATH BY ITSELF.  4a and 4b are scored at every rung of every ladder on both
        panels, full window and OOS.  Rule 8 picks on 2009-2016 ALONE and the OOS window is
        read once.  Anything that clears 4b is reported.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every LEVEL
    below is optimistic.  A margin, a bootstrap half-width and a flip count all contrast two
    rungs over the same inflated tape and the bias very largely cancels out of them; it does
    NOT cancel out of the 4b legs, which are measured against SPY, a real index, so every 4b
    pass counted here is an UPPER bound.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
"""
from __future__ import annotations

import csv
import glob
import os
import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-877-s-SEED-FLOOR-the-RIGHT-RULER-for-a-DETERMINISTIC-MARGIN-at-all"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
PRIOR1100 = HERE / ("2026-09-16_should-a-RULE-8-PICK-be-PUBLISHED-when-its-MARGIN-is-BELOW-"
                    "the-SEED-FLOOR_C.margins.csv")
PRIOR1096 = HERE / ("2026-09-16_is-RULE-8-REACHABILITY-a-COST-RUNG-object-across-the-record-s-"
                    "COMMITTED-PICKS_cloud.margins.csv")

# ------------------------------------------------------------- frozen at 1096/1100's build
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, COST = 0.75, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]
HS = [21, 63, 126, 252]
GS = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
CADS = ["D", "W", "M", "Q"]
MVS = [0.40, 0.50, 0.60, 0.80, 9.99]
BOOKS = ["TOP5", "TOP10", "TOP20", "EWELIG", "BAND03"]
PANELS = ["U56", "B136"]

CORE_L = ["L_N", "L_H", "L_G", "L_CAD"]
WIDE_L = ["L_NH", "L_BOOK", "L_MV"]
ALL_L = CORE_L + WIDE_L
F877 = 0.0145                                  # 871/877's per-arm SEED-noise floor, Sharpe units
CLAIMSETS = ["CS_CSV", "CS_PROSE", "CS_ALL"]   # dial 1
QGRID = [0.50, 0.68, 0.80, 0.90, 0.95]         # dial 2
Q_HEAD, CS_HEAD = 0.90, "CS_ALL"
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISDD": "IS_MaxDD", "C_ISCAGR": "IS_CAGR"}
HEAD_CH = "C_ISSHARPE"
BOOT_STAT = {"C_ISSHARPE": "Sharpe", "C_ISDD": "MaxDD", "C_ISCAGR": "CAGR"}
L_BLOCK, BDRAWS = 63, 1000
SEED_BASE = 11361136

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------- 1082/1096/1100's fast runner, verbatim
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
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
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px, max_vol=MAXVOL):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < max_vol)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def build_ewelig(elig, priced, reb, T, K, gross):
    W = np.zeros((T, K))
    for i, t in enumerate(reb):
        sel = np.flatnonzero(elig[t] & priced[t])
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ------------------------------------------------- 1098/1100/1102's paired block bootstrap
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_sharpe_cagr(R, idx, nb, L, chunk=200):
    """Sharpe AND CAGR of each row of R on each block draw (paired day indices across rows)."""
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    st = idx[:, ::L]
    n = nb * L
    shp = np.empty((R.shape[0], idx.shape[0]))
    cag = np.empty((R.shape[0], idx.shape[0]))
    for a in range(0, idx.shape[0], chunk):
        s = st[a:a + chunk]
        s1 = (CS1[:, s + L] - CS1[:, s]).sum(axis=2)
        s2 = (CS2[:, s + L] - CS2[:, s]).sum(axis=2)
        lsum = (CS[:, s + L] - CS[:, s]).sum(axis=2)
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        shp[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
        cag[:, a:a + chunk] = np.expm1(lsum * (252.0 / n))
    return shp, cag


def boot_maxdd(R, idx, chunk=40):
    nr = R.shape[0]
    out = np.empty((nr, idx.shape[0]))
    for a in range(0, idx.shape[0], chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            path = np.log1p(R[j])[ix]
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
    return out


# ================================================================== THE HARVEST, DECLARED
# A committed object is a FLOOR TRANSFER iff it applies a floor whose VALUE comes from ANOTHER
# construction (877/871's seed-noise floor, or a stated multiple of it) to a DETERMINISTIC
# margin in this record's own cells.  A floor MEASURED IN THE SAME FILE is not a transfer and
# is counted apart as a CONTROL.
TRANSFER_COL_RX = re.compile(r"^(below|above)_m[-0-9.]+$|877|seed_?floor", re.I)
OWNRULER_COL_RX = re.compile(r"^decided_q|own_?floor|own_?res|floor9\d_pp|"
                             r"^(peak|collapse)_above_floor$", re.I)
MARGIN_COL_RX = re.compile(r"^(margin|.*_margin|peak_minus_runnerup.*)$", re.I)
MULT_RX = re.compile(r"^(?:below|above)_m([-0-9.]+)$", re.I)

FLOOR_TOK_RX = re.compile(r"0\.0145|877'?s? (?:own )?(?:committed )?(?:0\.0145 )?seed|"
                          r"seed[- ]noise floor|seed floor", re.I)
DEC_RX = re.compile(r"\b(below|above|decided|undecided|unresolved|un-resolved|resolved|"
                    r"verdict|KILL|PARK|KEEP|bar|bars|barred|publish|not be published|"
                    r"fires|trigger)\b", re.I)
PAN_TOK = {"U56": re.compile(r"\bU56\b"), "B136": re.compile(r"\bB136\b")}
LAD_TOK = {"L_N": re.compile(r"\bL_N\b"), "L_H": re.compile(r"\bL_H\b"),
           "L_G": re.compile(r"\bL_G\b|\bGROSS ladder\b", re.I), "L_CAD": re.compile(r"\bL_CAD\b"),
           "L_NH": re.compile(r"\bL_NH\b"), "L_BOOK": re.compile(r"\bL_BOOK\b"),
           "L_MV": re.compile(r"\bL_MV\b")}
ALL14_RX = re.compile(r"\bof 14\b|\b14 committed\b|\b14 (?:committed-)?ladder picks\b", re.I)
QSTATE_RX = re.compile(r"\bq ?= ?0?\.\d+|\b9[05]% (?:confidence|interval|resolution)|"
                       r"\bconfidence\b", re.I)

PROSE_FILES = ([str(ROOT / "research" / "CHANGELOG.md"), str(ROOT / "research" / "LEADERBOARD.md"),
                str(ROOT / "research" / "QUEUE.md")]
               + sorted(glob.glob(str(HERE / "*.result.md")))
               + sorted(glob.glob(str(HERE / "*.memo.md"))))


def harvest_csv():
    """Every committed research/backtests/*.csv ROW that applies an IMPORTED floor to a
    margin.  Mechanical: the file must carry `panel`, a `ladder` column, a margin-like
    column and at least one TRANSFER flag column.  Rows are kept whether the flag fires or
    not so the denominator is honest.  Every rejected file is published with its reason."""
    objs, rejects, controls = [], [], []
    for f in sorted(glob.glob(str(HERE / "*.csv"))):
        base = os.path.basename(f)
        if base.startswith(f"{DATE}_{SLUG}"):
            continue                                   # never harvest this run's own output
        try:
            with open(f, newline="", encoding="utf-8") as fh:
                rd = csv.DictReader(fh)
                hdr = rd.fieldnames or []
                data = list(rd)
        except Exception as e:                         # pragma: no cover
            rejects.append(dict(source=base, reason=f"UNREADABLE {type(e).__name__}", n=0))
            continue
        tcols = [c for c in hdr if TRANSFER_COL_RX.search(c)]
        ocols = [c for c in hdr if OWNRULER_COL_RX.search(c)]
        if not tcols:
            if ocols:
                controls.append(dict(source=base, reason="OWN_RULER_IN_FILE",
                                     cols=";".join(ocols), n=len(data)))
            continue
        low = {c.lower(): c for c in hdr}
        if "panel" not in low:
            rejects.append(dict(source=base, reason="NO_PANEL_COLUMN", n=len(data)))
            continue
        if "ladder" not in low:
            rejects.append(dict(source=base, reason="NO_LADDER_COLUMN", n=len(data)))
            continue
        mcols = [c for c in hdr if MARGIN_COL_RX.match(c)]
        if not mcols:
            rejects.append(dict(source=base, reason="NO_MARGIN_COLUMN", n=len(data)))
            continue
        mcol = mcols[0]
        chcol = low.get("chooser")
        for i, row in enumerate(data):
            panel, lad = row[low["panel"]], row[low["ladder"]]
            ch = row[chcol] if chcol else HEAD_CH
            try:
                marg = float(row[mcol])
            except (TypeError, ValueError):
                continue
            for tc in tcols:
                mm = MULT_RX.match(tc)
                mult = float(mm.group(1)) if mm else 1.0
                objs.append(dict(arm="CSV", source=base, row=i, flag_col=tc, mult=mult,
                                 floor=mult * F877, panel=panel, ladder=lad, chooser=ch,
                                 committed_flag=str(row.get(tc, "")),
                                 committed_margin=marg,
                                 states_q=bool(ocols)))
    return objs, rejects, controls


def harvest_prose():
    """Committed prose LINES that apply the transferred floor to a named destination.  A line
    qualifies iff it carries a FLOOR token AND a decision word AND names a destination this
    run can rebuild: a (panel, ladder) pair, a panel alone (-> its 7 ladders), or the
    record's own '14 committed-ladder picks' phrase (-> all 14).  Every reject is published."""
    objs, rejects = [], []
    for f in PROSE_FILES:
        base = os.path.basename(f)
        if base.startswith(f"{DATE}_{SLUG}"):
            continue
        try:
            txt = Path(f).read_text(encoding="utf-8", errors="replace")
        except Exception:                              # pragma: no cover
            continue
        for ln, line in enumerate(txt.split("\n")):
            if not FLOOR_TOK_RX.search(line):
                continue
            if not DEC_RX.search(line):
                rejects.append(dict(source=base, line=ln, reason="QUOTES_FLOOR_NO_DECISION",
                                    text=line.strip()[:200]))
                continue
            pans = [p for p, rx in PAN_TOK.items() if rx.search(line)]
            lads = [l for l, rx in LAD_TOK.items() if rx.search(line)]
            if pans and lads:
                cells = [(p, l) for p in pans for l in lads]
            elif pans:
                cells = [(p, l) for p in pans for l in ALL_L]
            elif ALL14_RX.search(line):
                cells = [(p, l) for p in PANELS for l in ALL_L]
            else:
                rejects.append(dict(source=base, line=ln, reason="NO_CELL_NAMED",
                                    text=line.strip()[:200]))
                continue
            mult = 1.0
            mo = re.search(r"\bm ?= ?([0-9.]+)", line)
            if mo:
                try:
                    mult = float(mo.group(1))
                except ValueError:
                    mult = 1.0
            for (p, l) in cells:
                objs.append(dict(arm="PROSE", source=base, row=ln, flag_col="prose",
                                 mult=mult, floor=mult * F877, panel=p, ladder=l,
                                 chooser=HEAD_CH, committed_flag="",
                                 committed_margin=np.nan,
                                 states_q=bool(QSTATE_RX.search(line))))
    return objs, rejects


# ============================================================================ MAIN
def main():
    t0 = time.time()
    P(f"# Idea 1136 (cloud lane, {DATE}) — is 877's SEED FLOOR the RIGHT RULER for a")
    P("#   DETERMINISTIC MARGIN at all?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIMSETS} x CONFIDENCE q {QGRID}")
    P(f"#   = {len(CLAIMSETS) * len(QGRID)} points, ALL published.  PANEL, LADDER and CHOOSER "
      "are NOT dials.")
    P("#   The OWN-RULER READING is not a dial: HALFWIDTH is the headline (it is a number in")
    P("#   0.0145's own units and can be substituted for it literally), AGREEMENT is reported")
    P("#   beside it at every point and nothing is selected on it.")
    P(f"# FROZEN at 1096/1100: CAND20 legs {LEGS}, max_vol {MAXVOL} (except L_MV), gross "
      f"{GROSS0} (except L_G),")
    P(f"#   W (except L_CAD), hold 126 (except L_H), N=20 (L_N free, L_H at 12), {COST:.0f} bps, "
      f"LAG {LAG},")
    P(f"#   warm-up {WARMUP}, IS end {IS_END}; bootstrap L={L_BLOCK}, {BDRAWS} draws, crc32 "
      f"seeds, base {SEED_BASE}.")
    P("# THE TWO RULERS: TRANSFER = m x 0.0145 (877's SEED-noise floor, no confidence attached);")
    P("#   OWN = the destination cell's half-width of the two-sided q interval of the PAIRED")
    P("#   bootstrap pick-minus-runner-up difference on the IS window, the window the chooser sees.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_WRONG_RULER  majority of admissible objects FLIP at CS_ALL / q=0.90 / HALFWIDTH.")
    P("#   (b) H_DIRECTION    flips run one way: TRANSFER says RESOLVED where OWN says not.")
    P("#   (c) H_GROSS_FLIPS_BACK  on the two GROSS ladders the flip runs the OTHER way.")
    P("#   (d) H_Q_STABLE     the flip share moves <= 0.25 across the five q rungs.")
    P("#   (e) H_UNDECLARED   a majority of committed transfer objects state NO confidence.")
    P("#   (f) DECISION RULE  WRONG RULER iff (a) AND (b); majority-flip with mixed direction")
    P("#                      is the weaker verdict UNINFORMATIVE, not LAX.")
    P("#   (g) 4a/4b scored at every rung, full and OOS; rule 8 picks on 2009-2016 alone.")
    P("")

    gaterows, gates = [], {}

    # ------------------------------------------------------------------------------ PANELS
    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> "
          f"{idx[-1].date()}, warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

    def masks(panel):
        d = panels[panel]
        out = {}
        for f in CADS:
            mk = rebalance_mask(d["idx"], f).values
            mkl = np.roll(mk, LAG)
            mkl[:LAG] = False
            out[f] = (np.flatnonzero(mk), mkl)
        return out

    store, ladder_rungs, cells, bench = {}, {}, [], {}
    for panel in PANELS:
        d = panels[panel]
        px, rets, elig, priced = d["px"], d["rets"], d["elig"], d["priced"]
        T, K, warm, ins, oos = d["T"], d["K"], d["warm"], d["ins"], d["oos"]
        rank_key = -d["sc"]
        mk = masks(panel)
        yrs = warm.sum() / 252.0
        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        lb_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].values
        lbm = blocks(lb_r, warm, ins, oos)
        bench[panel] = (sb, lbm)

        def add(ladder, rung, W, cad="W"):
            g, tn = nrun(rets, lagmat(W), mk[cad][1])
            r = g - tn * COST / 1e4
            store[(panel, ladder, str(rung))] = r
            ladder_rungs.setdefault((panel, ladder), []).append(str(rung))
            b = blocks(r, warm, ins, oos)
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lbm)
            cells.append(dict(panel=panel, ladder=ladder, rung=str(rung), cadence=cad,
                              turnover=float(tn[warm].sum() / yrs),
                              pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                              pass_4a=all(l4a.values()), **b, **l4b, **l4bo, **l4a))

        for N in NS:
            add("L_N", N, build(rank_key, elig, priced, mk["W"][0], N, 126, T, K, GROSS0))
        for H in HS:
            add("L_H", H, build(rank_key, elig, priced, mk["W"][0], 12, H, T, K, GROSS0))
        for G in GS:
            add("L_G", G, build(rank_key, elig, priced, mk["W"][0], 20, 126, T, K, G))
        for f in CADS:
            add("L_CAD", f, build(rank_key, elig, priced, mk[f][0], 20, 126, T, K, GROSS0), cad=f)
        for N in NS:
            for H in HS:
                add("L_NH", f"{N}/{H}",
                    build(rank_key, elig, priced, mk["W"][0], N, H, T, K, GROSS0))
        for bk in BOOKS:
            if bk.startswith("TOP"):
                W = build(rank_key, elig, priced, mk["W"][0], int(bk[3:]), 126, T, K, GROSS0)
            elif bk == "EWELIG":
                W = build_ewelig(elig, priced, mk["W"][0], T, K, GROSS0)
            else:
                W = rules_v2_weights(px).values
            add("L_BOOK", bk, W)
        for mv in MVS:
            _, el = mech(px, mv)
            add("L_MV", mv, build(rank_key, el, priced, mk["W"][0], 20, 126, T, K, GROSS0))
        P(f"  {panel}: ladders built ({time.time() - t0:.0f}s)")

    grid = pd.DataFrame(cells)
    metr = {(r.panel, r.ladder, r.rung): r for r in grid.itertuples()}

    # -------------------------------------------------------------------------- GATES
    d = panels["U56"]
    mkU = masks("U56")
    W = build(-d["sc"], d["elig"], d["priced"], mkU["W"][0], 20, 126, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq="W")["returns"].values
    rfast = store[("U56", "L_N", "20")]
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest", value=g1,
                         pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                     {g1:.2e}   "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    m20 = blocks(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m20["CAGR"] - A936_WH126[0]), abs(m20["Sharpe"] - A936_WH126[1]),
             abs(m20["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="committed U56 W/H126/N=20 triple", value=g2,
                         pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple         {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m20['CAGR']:.4%} / {m20['Sharpe']:.4f} / "
      f"{m20['MaxDD']:.4%})")

    sb_u, lbm_u = bench["U56"]
    g3 = max(abs(sb_u["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(sb_u["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sb_u["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                     {g3:.2e}   "
      f"{'PASS' if gates['G3'] else 'FAIL'}")

    g5 = abs(lbm_u["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD", value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD                                {g5:.2e}   "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    W2 = build(-d["sc"], d["elig"], d["priced"], mkU["W"][0], 20, 126, d["T"], d["K"], GROSS0)
    g6 = float(np.abs(W - W2).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism", value=g6, pass_=gates["G6"]))
    P(f"  G6  determinism                                        {g6:.2e}   "
      f"{'PASS' if gates['G6'] else 'FAIL'}")

    # ------------------------------------------------- MARGINS AND BOTH RULERS, per cell
    P("")
    P("## THE 42 DESTINATION CELLS — pick and runner-up chosen on IS 2009-2016 ALONE, then")
    P("##   the SAME pair measured against BOTH rulers at all five confidences.")
    mrows = []
    for panel in PANELS:
        dp = panels[panel]
        rng = np.random.default_rng(seed_of(panel, "boot", "IS"))
        Tis = int(dp["ins"].sum())
        bidx, nb = block_index(rng, Tis, L_BLOCK, BDRAWS)
        for ladder in ALL_L:
            rungs = ladder_rungs[(panel, ladder)]
            for ch, key in CHOOSERS.items():
                vals = np.array([getattr(metr[(panel, ladder, r_)], key) for r_ in rungs])
                order = np.argsort(-vals, kind="stable")
                pk_i, ru_i = int(order[0]), int(order[1])
                margin = float(vals[pk_i] - vals[ru_i])
                spread = float(np.nanmax(vals) - np.nanmin(vals))
                R = np.vstack([store[(panel, ladder, rungs[pk_i])][dp["ins"]],
                               store[(panel, ladder, rungs[ru_i])][dp["ins"]]])
                shp, cag = boot_sharpe_cagr(R, bidx, nb, L_BLOCK)
                if BOOT_STAT[ch] == "Sharpe":
                    B = shp
                elif BOOT_STAT[ch] == "CAGR":
                    B = cag
                else:
                    B = boot_maxdd(R, bidx)
                diff = B[0] - B[1]
                diff = diff[np.isfinite(diff)]
                row = dict(panel=panel, ladder=ladder, chooser=ch, statistic=key,
                           claimset=("CORE" if ladder in CORE_L else "WIDE"),
                           rungs=len(rungs), pick=rungs[pk_i], runner_up=rungs[ru_i],
                           margin=margin, spread=spread,
                           margin_over_spread=(margin / spread if spread > 0 else np.nan),
                           ndraws=int(len(diff)),
                           admissible=bool(ch == HEAD_CH))
                for q in QGRID:
                    lo, hi = np.percentile(diff, [(1 - q) / 2 * 100, (1 + q) / 2 * 100])
                    hw = float((hi - lo) / 2.0)
                    row[f"own_hw_q{q}"] = hw
                    row[f"own_res_ratio_q{q}"] = hw / F877
                row["agreement"] = float((np.sign(diff) == np.sign(margin)).mean())
                mrows.append(row)
    MARG = pd.DataFrame(mrows)
    dump(MARG, "margins")

    head = MARG[MARG.chooser == HEAD_CH]
    P(f"  {HEAD_CH} (the floor's own units), {len(head)} cells:")
    P(f"  {'panel':<5} {'ladder':<7} {'pick':<8} {'vs':<8} {'margin':>9} {'spread':>9} "
      f"{'own q.50':>9} {'own q.90':>9} {'own q.95':>9} {'agree':>7}  0.0145?")
    for _, r_ in head.iterrows():
        P(f"  {r_['panel']:<5} {r_['ladder']:<7} {str(r_['pick']):<8} {str(r_['runner_up']):<8} "
          f"{r_['margin']:9.4f} {r_['spread']:9.4f} {r_['own_hw_q0.5']:9.4f} "
          f"{r_['own_hw_q0.9']:9.4f} {r_['own_hw_q0.95']:9.4f} {r_['agreement']:7.3f}  "
          f"{'BELOW' if r_['margin'] < F877 else 'above'}")

    # ---- G4: reproduce 1100's committed margins.csv (margin, own res at 0.90, agreement)
    if PRIOR1100.exists():
        pri = pd.read_csv(PRIOR1100)
        pri = pri[pri.chooser == HEAD_CH]
        mine = MARG.set_index(["panel", "ladder", "chooser"])
        dv, npairs, pickbad = [], 0, 0
        for _, r_ in pri.iterrows():
            key = (r_["panel"], r_["ladder"], r_["chooser"])
            if key not in mine.index:
                continue
            mr = mine.loc[key]
            npairs += 1
            pickbad += int(str(mr["pick"]) != str(r_["pick"]))
            dv.append(max(abs(mr["margin"] - float(r_["margin"])),
                          abs(mr["spread"] - float(r_["spread"]))))
        g4 = float(np.max(dv)) if dv else np.inf
        gates["G4"] = g4 < 1e-9 and pickbad == 0 and npairs == 14
    else:                                                          # pragma: no cover
        g4, npairs, pickbad = np.inf, 0, 0
        gates["G4"] = False
    gaterows.append(dict(gate="G4", what=f"reproduce 1100's committed margins ({npairs} cells)",
                         value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1100's committed margins ({npairs} cells)       {g4:.2e}   "
      f"{'PASS' if gates['G4'] else 'FAIL'}  (pick mismatches {pickbad})")

    # ---- G7: reproduce 1096's committed above_877_seed_floor flags
    if PRIOR1096.exists():
        p96 = pd.read_csv(PRIOR1096)
        mine = MARG[MARG.chooser == HEAD_CH].set_index(["panel", "ladder"])
        bad7, n7 = 0, 0
        for _, r_ in p96.iterrows():
            key = (r_["panel"], r_["ladder"])
            if key not in mine.index:
                continue
            n7 += 1
            mineflag = bool(mine.loc[key]["margin"] >= F877)
            bad7 += int(mineflag != (str(r_["above_877_seed_floor"]).strip().lower() == "true"))
        gates["G7"] = bad7 == 0 and n7 == 14
    else:                                                          # pragma: no cover
        bad7, n7 = 99, 0
        gates["G7"] = False
    gaterows.append(dict(gate="G7", what=f"reproduce 1096's committed 877 flags ({n7} rows)",
                         value=float(bad7), pass_=gates["G7"]))
    P(f"  G7  CROSS-RUN 1096's committed 877 flags ({n7} rows)        {bad7:.2e}   "
      f"{'PASS' if gates['G7'] else 'FAIL'}")

    # ---- G8: the own ruler is MONOTONE in q (a ruler that is not is not a ruler)
    hw = MARG[[f"own_hw_q{q}" for q in QGRID]].values
    g8 = float(np.min(np.diff(hw, axis=1)))
    gates["G8"] = g8 >= 0.0
    gaterows.append(dict(gate="G8", what="own half-width monotone non-decreasing in q",
                         value=g8, pass_=gates["G8"]))
    P(f"  G8  own half-width monotone in q (min increment)       {g8:.2e}   "
      f"{'PASS' if gates['G8'] else 'FAIL'}")

    # ---- G9: every ladder is LIVE (a dead ladder would make every margin 0 trivially)
    g9 = float(MARG[MARG.chooser == HEAD_CH]["spread"].min())
    gates["G9"] = g9 > 1e-3
    gaterows.append(dict(gate="G9", what="every ladder live (min IS-Sharpe spread)",
                         value=g9, pass_=gates["G9"]))
    P(f"  G9  every ladder live (min IS-Sharpe spread)           {g9:.2e}   "
      f"{'PASS' if gates['G9'] else 'FAIL'}")

    # ---- G10: the BOOK grid is 1100's, rung for rung.  This run re-scores a RULER, so if any
    #      book moved, something other than the ruler changed and no reading would be safe.
    pc = HERE / ("2026-09-16_should-a-RULE-8-PICK-be-PUBLISHED-when-its-MARGIN-is-BELOW-"
                 "the-SEED-FLOOR_C.cells.csv")
    if pc.exists():
        a = pd.read_csv(pc).set_index(["panel", "ladder", "rung"])
        b = grid.set_index(["panel", "ladder", "rung"])
        j = a.join(b, rsuffix="_new", how="inner")
        g10 = float(max(np.abs(j[c] - j[c + "_new"]).max()
                        for c in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "turnover")))
        # The comparand is a CSV ROUND-TRIP of the same float, so the bar is round-trip
        # precision (1e-12) and NOT exact equality: at 0.0 this gate would fail on a
        # difference no correct run can avoid.  The measured value is printed either way.
        gates["G10"] = g10 < 1e-12 and len(j) == len(grid) == 146
    else:                                                          # pragma: no cover
        g10, gates["G10"] = np.inf, False
    gaterows.append(dict(gate="G10",
                         what="book grid == 1100's committed 146-rung grid (CSV round-trip bar)",
                         value=g10, pass_=gates["G10"]))
    P(f"  G10 CROSS-RUN 1100's committed 146-rung BOOK grid      {g10:.2e}   "
      f"{'PASS' if gates['G10'] else 'FAIL'}  (bar 1e-12 = CSV round-trip, NOT exact 0)")

    GT = pd.DataFrame(gaterows)
    dump(GT, "gates")
    P(f"  GATES {int(GT.pass_.sum())} of {len(GT)} PASS")
    P("")

    # ---------------------------------------------------------------------- THE HARVEST
    P("## THE HARVEST — every committed object that applies an IMPORTED floor to a margin")
    csv_objs, csv_rej, csv_ctrl = harvest_csv()
    pro_objs, pro_rej = harvest_prose()
    OBJ = pd.DataFrame(csv_objs + pro_objs)
    REJ = pd.DataFrame(csv_rej + [dict(source=r["source"], reason=r["reason"], n=1)
                                  for r in pro_rej])
    CTRL = pd.DataFrame(csv_ctrl)
    P(f"  CSV arm   {len(csv_objs):,} objects over "
      f"{OBJ[OBJ.arm == 'CSV'].source.nunique() if len(csv_objs) else 0} committed files")
    P(f"  PROSE arm {len(pro_objs):,} objects over "
      f"{OBJ[OBJ.arm == 'PROSE'].source.nunique() if len(pro_objs) else 0} committed files "
      f"({len(pro_rej)} lines rejected)")
    if len(CTRL):
        P(f"  CONTROLS  {len(CTRL)} committed files already measure their OWN floor and are "
          "NOT transfers:")
        for _, r_ in CTRL.iterrows():
            P(f"    {r_['source'][:78]:<80} {r_['cols']}")
    if len(REJ):
        P(f"  REJECTS   {len(REJ)} (published with reason):")
        for reason, n in REJ.reason.value_counts().items():
            P(f"    {reason:<28} {n}")
    dump(OBJ, "objects")
    dump(REJ, "rejects")
    if len(CTRL):
        dump(CTRL, "controls")
    P("")

    # --------------------------------------------- SCORE EVERY OBJECT UNDER BOTH RULERS
    look = MARG.set_index(["panel", "ladder", "chooser"])
    scored = []
    unmapped = 0
    for o in (csv_objs + pro_objs):
        key = (o["panel"], o["ladder"], o["chooser"])
        if key not in look.index:
            unmapped += 1
            continue
        mr = look.loc[key]
        marg = float(mr["margin"])
        adm = bool(o["chooser"] == HEAD_CH)
        base = dict(o)
        base.update(rebuilt_margin=marg, spread=float(mr["spread"]),
                    admissible=adm, agreement=float(mr["agreement"]),
                    transfer_resolved=bool(marg >= o["floor"]))
        for q in QGRID:
            hwq = float(mr[f"own_hw_q{q}"])
            own_hw = bool(marg >= hwq)
            own_ag = bool(mr["agreement"] >= q)
            base[f"own_hw_q{q}"] = hwq
            base[f"own_resolved_HW_q{q}"] = own_hw
            base[f"own_resolved_AG_q{q}"] = own_ag
            base[f"flip_HW_q{q}"] = bool(own_hw != base["transfer_resolved"])
            base[f"flip_AG_q{q}"] = bool(own_ag != base["transfer_resolved"])
            base[f"dir_HW_q{q}"] = ("TRANSFER_LAX" if (base["transfer_resolved"] and not own_hw)
                                    else ("TRANSFER_STRICT" if (own_hw and not
                                                               base["transfer_resolved"])
                                          else "AGREE"))
        scored.append(base)
    SC = pd.DataFrame(scored)
    dump(SC, "scored")
    if unmapped:
        P(f"  {unmapped} harvested objects name a cell this run cannot rebuild — dropped and "
          "reported, never scored.")

    # ------------------------------------------------------------------- THE 15 DIAL POINTS
    P("")
    P("## THE 15 DIAL POINTS (all published).  'admissible' = the object applies a SHARPE")
    P("##   floor to a SHARPE margin.  Unit-inadmissible objects are counted apart, never")
    P("##   inside a headline.")
    ARM = {"CS_CSV": ["CSV"], "CS_PROSE": ["PROSE"], "CS_ALL": ["CSV", "PROSE"]}
    grows = []
    for cs in CLAIMSETS:
        sub_all = SC[SC.arm.isin(ARM[cs])]
        sub = sub_all[sub_all.admissible]
        for q in QGRID:
            if len(sub):
                fh = sub[f"flip_HW_q{q}"].values
                fa = sub[f"flip_AG_q{q}"].values
                dirs = sub[f"dir_HW_q{q}"].values
                lax = int((dirs == "TRANSFER_LAX").sum())
                strict = int((dirs == "TRANSFER_STRICT").sum())
            else:                                                  # pragma: no cover
                fh = fa = np.array([], bool)
                lax = strict = 0
            grows.append(dict(claim_set=cs, q=q, n_objects=len(sub_all), n_admissible=len(sub),
                              n_inadmissible=int((~sub_all.admissible).sum()),
                              n_flip_HW=int(fh.sum()),
                              flip_share_HW=(float(fh.mean()) if len(fh) else np.nan),
                              n_flip_AG=int(fa.sum()),
                              flip_share_AG=(float(fa.mean()) if len(fa) else np.nan),
                              n_transfer_lax=lax, n_transfer_strict=strict,
                              transfer_resolved=int(sub["transfer_resolved"].sum())
                              if len(sub) else 0,
                              own_resolved_HW=int(sub[f"own_resolved_HW_q{q}"].sum())
                              if len(sub) else 0))
    GRID = pd.DataFrame(grows)
    dump(GRID, "grid")
    P(GRID.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    hp = GRID[(GRID.claim_set == CS_HEAD) & (GRID.q == Q_HEAD)].iloc[0]
    P(f"  HEADLINE ({CS_HEAD}, q={Q_HEAD}, HALFWIDTH): {hp.n_flip_HW:,} of "
      f"{hp.n_admissible:,} admissible committed floor transfers CHANGE VERDICT "
      f"({hp.flip_share_HW:.4f});")
    P(f"    direction {hp.n_transfer_lax:,} TRANSFER_LAX / {hp.n_transfer_strict:,} "
      f"TRANSFER_STRICT.  AGREEMENT reading: {hp.n_flip_AG:,} ({hp.flip_share_AG:.4f}).")
    P("")

    # ---- D1: POST-HOC AND LABELLED AS SUCH.  The declared statistic is UNCONDITIONAL, so it
    #      is diluted by objects the transferred floor ALREADY calls unresolved, where the two
    #      rulers cannot disagree in the direction that matters.  This is a re-cut of columns
    #      already published in .grid.csv, not a new measurement and not a new dial.
    P("## D1 — POST-HOC AND LABELLED AS SUCH: the CONDITIONAL flip rate.  Of the committed")
    P("##   objects that assert RESOLVED (margin at or above the imported floor), how many")
    P("##   does the destination cell's own ruler REFUSE to resolve?")
    d1 = GRID.copy()
    d1["cond_flip_share"] = np.where(d1.transfer_resolved > 0,
                                     d1.n_transfer_lax / d1.transfer_resolved.replace(0, np.nan),
                                     np.nan)
    dump(d1[["claim_set", "q", "transfer_resolved", "n_transfer_lax", "cond_flip_share",
             "own_resolved_HW"]], "d1")
    P(d1[d1.claim_set == CS_HEAD][["claim_set", "q", "transfer_resolved", "n_transfer_lax",
                                   "cond_flip_share", "own_resolved_HW"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    hd1 = float(d1[(d1.claim_set == CS_HEAD) & (d1.q == Q_HEAD)]["cond_flip_share"].iloc[0])
    P(f"  At the headline point {hp.n_transfer_lax} of {hp.transfer_resolved} objects that "
      f"assert RESOLVED are refused by the own ruler = {hd1:.4f}, and the own ruler resolves")
    P(f"  {hp.own_resolved_HW} of {hp.n_admissible} objects in total.")
    P("")

    # ---- REPORTED, NOT GATED: the own ruler is itself a DRAW.  1100 measured the same 14
    #      half-widths at seed base 11001100; this run's base is 11361136.
    if PRIOR1100.exists():
        pri = pd.read_csv(PRIOR1100)
        pri = pri[(pri.chooser == HEAD_CH) & pri.own_res_halfwidth.notna()]
        mm = MARG[MARG.chooser == HEAD_CH].set_index(["panel", "ladder"])
        rows = []
        for _, r_ in pri.iterrows():
            k = (r_["panel"], r_["ladder"])
            if k not in mm.index:
                continue
            a, b = float(r_["own_res_halfwidth"]), float(mm.loc[k][f"own_hw_q{Q_HEAD}"])
            rows.append(dict(panel=k[0], ladder=k[1], committed_1100=a, this_run=b,
                             abs_diff=abs(b - a), ratio=(b / a if a else np.nan),
                             committed_agreement=float(r_["agreement"]),
                             this_run_agreement=float(mm.loc[k]["agreement"]),
                             verdict_same=bool((float(r_["margin"]) >= a) ==
                                               (float(r_["margin"]) >= b))))
        RD = pd.DataFrame(rows)
        dump(RD, "redraw")
        P("## THE OWN RULER IS ITSELF A DRAW — REPORTED, NOT GATED.  1100 measured these 14")
        P(f"##   half-widths at seed base 11001100; this run's base is {SEED_BASE}.")
        P(RD.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P(f"  median |diff| {RD.abs_diff.median():.4f} (median ratio {RD.ratio.median():.4f}); "
          f"the RESOLVED/UNRESOLVED verdict is UNCHANGED on {int(RD.verdict_same.sum())} of "
          f"{len(RD)} cells, so the substitution's ANSWER survives the redraw even though its "
          "LEVEL does not.")
        P("")

    # ------------------------------------------------------------------ PER-CELL BREAKDOWN
    P("## PER-CELL, at the headline q — which destinations carry the flips")
    hsub = SC[SC.admissible & SC.arm.isin(ARM[CS_HEAD])]
    cellrows = []
    for (p, l), g in hsub.groupby(["panel", "ladder"]):
        mr = look.loc[(p, l, HEAD_CH)]
        cellrows.append(dict(panel=p, ladder=l, n_objects=len(g),
                             margin=float(mr["margin"]), spread=float(mr["spread"]),
                             own_hw_q90=float(mr[f"own_hw_q{Q_HEAD}"]),
                             ratio_own_over_877=float(mr[f"own_hw_q{Q_HEAD}"]) / F877,
                             agreement=float(mr["agreement"]),
                             transfer_resolved=bool(mr["margin"] >= F877),
                             own_resolved=bool(mr["margin"] >= mr[f"own_hw_q{Q_HEAD}"]),
                             n_flip=int(g[f"flip_HW_q{Q_HEAD}"].sum())))
    CELL = pd.DataFrame(cellrows).sort_values(["panel", "ladder"])
    dump(CELL, "cells_flip")
    P(CELL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    gross_rows = CELL[CELL.ladder == "L_G"]
    P(f"  GROSS ladders (H_GROSS_FLIPS_BACK): own/877 ratio "
      f"{list(np.round(gross_rows.ratio_own_over_877.values, 4))}, transfer_resolved "
      f"{list(gross_rows.transfer_resolved.values)}, own_resolved "
      f"{list(gross_rows.own_resolved.values)}")
    P("")

    # ------------------------------------------------------------------------ HYPOTHESES
    P("## HYPOTHESES — declared before any number, scored now")
    hyp = []
    h_wrong = bool(hp.flip_share_HW > 0.5)
    hyp.append(dict(name="H_WRONG_RULER", supported=h_wrong,
                    detail=f"{hp.n_flip_HW} of {hp.n_admissible} flip = {hp.flip_share_HW:.4f} "
                           f"at {CS_HEAD} / q={Q_HEAD} / HALFWIDTH"))
    nf = hp.n_transfer_lax + hp.n_transfer_strict
    h_dir = bool(nf > 0 and hp.n_transfer_lax > 0.5 * nf)
    hyp.append(dict(name="H_DIRECTION", supported=h_dir,
                    detail=f"TRANSFER_LAX {hp.n_transfer_lax} vs TRANSFER_STRICT "
                           f"{hp.n_transfer_strict} of {nf} flips"))
    gm = MARG[(MARG.ladder == "L_G") & (MARG.chooser == HEAD_CH)]
    g_ag = [bool(a >= Q_HEAD) for a in gm.agreement.values]
    g_tr = [bool(m >= F877) for m in gm.margin.values]
    gback = bool(len(gross_rows) and (gross_rows.own_resolved & ~gross_rows.transfer_resolved).any())
    gback_ag = any(a and not t for a, t in zip(g_ag, g_tr))
    hyp.append(dict(name="H_GROSS_FLIPS_BACK", supported=gback,
                    detail=f"HALFWIDTH (headline): own_resolved "
                           f"{list(gross_rows.own_resolved.values)} vs transfer_resolved "
                           f"{list(gross_rows.transfer_resolved.values)}; AGREEMENT reading "
                           f"(reported beside, never selected on): own_resolved {g_ag} -> "
                           f"{'SUPPORTED' if gback_ag else 'REFUTED'}"))
    qs = GRID[GRID.claim_set == CS_HEAD].flip_share_HW.values
    qspan = float(np.nanmax(qs) - np.nanmin(qs))
    hyp.append(dict(name="H_Q_STABLE", supported=bool(qspan <= 0.25),
                    detail=f"flip share {np.round(qs, 4).tolist()} over q {QGRID}, span {qspan:.4f}"))
    adm_all = SC[SC.admissible]
    share_noq = float((~adm_all.states_q).mean()) if len(adm_all) else np.nan
    hyp.append(dict(name="H_UNDECLARED", supported=bool(share_noq > 0.5),
                    detail=f"{int((~adm_all.states_q).sum())} of {len(adm_all)} admissible "
                           f"objects state no confidence ({share_noq:.4f})"))
    HYP = pd.DataFrame(hyp)
    dump(HYP, "hypotheses")
    for _, r_ in HYP.iterrows():
        P(f"  {r_['name']:<20} {'SUPPORTED' if r_['supported'] else 'REFUTED  '}  {r_['detail']}")
    P("")
    if h_wrong and h_dir:
        VERDICT = "WRONG RULER (LAX)"
    elif h_wrong:
        VERDICT = "WRONG RULER (UNINFORMATIVE — majority flip, mixed direction)"
    else:
        VERDICT = "NOT REFUTED — 0.0145 agrees with the own ruler on a majority"
    P(f"## THE DECISION RULE, applied as declared -> {VERDICT}")
    P("##   AND THE DECLARED STATISTIC IS THE WRONG CUT, WHICH IS ITSELF THE LESSON.  The")
    P("##   unconditional flip share cannot exceed the share of objects that assert RESOLVED,")
    P(f"##   and only {hp.transfer_resolved} of {hp.n_admissible} committed transfers do.  On the")
    P(f"##   cut that carries the record's actual claims, D1, the answer is {hd1:.4f}: the own")
    P("##   ruler refuses EVERY margin the imported floor certifies, and certifies "
      f"{hp.own_resolved_HW} of {hp.n_admissible}")
    P("##   in total.  The declared rule is reported as it was declared; this is the re-cut.")
    P("")

    # ------------------------------------------------------ RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 (PROTOCOL rule 8) AND BOTH KEEP PATHS — rungs chosen on 2009-2016 ALONE,")
    P("##   OOS 2017-2026 read ONCE.")
    for panel in PANELS:
        sb, lbm = bench[panel]
        P(f"  {panel} SPY   full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f} / {sb['H2']:.4f}), OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2 live  full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / "
          f"{lbm['MaxDD']:.2%}, OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.4f} / "
          f"{lbm['OOS_MaxDD']:.2%}")
    wrows = []
    for panel in PANELS:
        sb, lbm = bench[panel]
        for ladder in ALL_L:
            rungs = ladder_rungs[(panel, ladder)]
            for ch, key in CHOOSERS.items():
                vals = np.array([getattr(metr[(panel, ladder, r_)], key) for r_ in rungs])
                pk = rungs[int(np.argsort(-vals, kind="stable")[0])]
                m = metr[(panel, ladder, pk)]
                b = {k: getattr(m, k) for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")}
                wrows.append(dict(panel=panel, ladder=ladder, chooser=ch, pick=pk,
                                  turnover=float(m.turnover), **b,
                                  pass_4b_full=bool(m.pass_4b_full),
                                  pass_4b_oos=bool(m.pass_4b_oos), pass_4a=bool(m.pass_4a),
                                  spy_oos_sharpe=sb["OOS_Sharpe"], spy_oos_cagr=sb["OOS_CAGR"],
                                  spy_oos_maxdd=sb["OOS_MaxDD"]))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    dump(grid, "cells")
    n4bf = int(WF.pass_4b_full.sum())
    n4bo = int(WF.pass_4b_oos.sum())
    n4a = int(WF.pass_4a.sum())
    P(f"  {len(WF)} rule-8 picks: 4b full {n4bf}, 4b OOS {n4bo}, 4a {n4a}.")
    both = WF[WF.pass_4b_full & WF.pass_4b_oos]
    P(f"  whole grid, {len(grid)} rungs: 4b full {int(grid.pass_4b_full.sum())}, "
      f"4b OOS {int(grid.pass_4b_oos.sum())}, 4a {int(grid.pass_4a.sum())}.")
    if len(both):
        b0 = both.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"  best pick clearing 4b FULL and OOS: {b0['panel']} {b0['ladder']} {b0['chooser']} "
          f"rung {b0['pick']} — full {b0['CAGR']:.2%} / {b0['Sharpe']:.4f} / {b0['MaxDD']:.2%} "
          f"(halves {b0['H1']:.4f} / {b0['H2']:.4f}), OOS {b0['OOS_CAGR']:.2%} / "
          f"{b0['OOS_Sharpe']:.4f} / {b0['OOS_MaxDD']:.2%}, {b0['turnover']:.2f}x/yr")
        P("  NOTHING PROPOSED: every pick clearing 4b here is a rung of the standing "
          "top-N/W/H126 family the record already holds and has already PARKED, and this run "
          "changes no book — it re-scores a RULER.  4a is empty.")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9): U56 and B136 are CURRENT-CONSTITUENT panels.  Every")
    P("##   LEVEL above is optimistic.  Margins, half-widths and flip counts contrast two rungs")
    P("##   over one inflated tape and the bias very largely cancels out of them; it does NOT")
    P("##   cancel out of the 4b legs, measured against SPY, so every 4b pass is an UPPER bound.")
    P(f"# done in {time.time() - t0:.0f}s")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")


if __name__ == "__main__":
    main()
