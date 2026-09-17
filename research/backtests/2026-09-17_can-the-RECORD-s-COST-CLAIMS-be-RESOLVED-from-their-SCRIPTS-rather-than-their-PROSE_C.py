#!/usr/bin/env python3
"""QUEUE idea 1149 (lane C, 2026-09-17) — can the RECORD's COST CLAIMS be RESOLVED from their
SCRIPTS rather than their PROSE?

QUESTION (QUEUE '## Open', verbatim)
    idea 1098 found R_STRICT resolves only 82 of 2,088 committed cost claims and 0 of the 28
    that assume the CAGR floor, because prose rarely states the cell; every claim does, however,
    cite a committed script whose constants pin panel, N, H, gross and cadence exactly.  Re-derive
    the cell from the cited script and report how many of the 28 become re-scorable, and what
    share of the 2,088 gains a cell.  Max 2 params (resolution source, claim set).

THE POPULATION IS A CENSUS, NOT A SAMPLE, AND IT IS 1098's OWN COMMITTED FILE.
    The claim set is read verbatim out of `2026-09-16_...-or-only-the-CAGR-FLOOR_C.claims.csv`
    — all 2,088 rows, 59 NARROW / 125 PROX / 2,088 WIDE, with 1098's own `resolved` (82) and
    `resolved_loose` (425) columns carried along as the thing to be reproduced.  Re-harvesting
    today's corpus would give a DIFFERENT and LARGER population (every lane has committed
    result.md files since), and then no number here would be comparable to the 82 and the 28 the
    queue asks about.  Idea 1163's finding applied to text instead of prices.  The current-corpus
    harvest is run anyway, as a CONTROL, and its size is published beside the census.

    Line numbers in that file index the corpus AS IT WAS, so `LEADERBOARD.md` and `CHANGELOG.md`
    are recovered from git at 1098's own commit `3c1e2af6` (the commit that ADDED the claims
    file).  Falling back to the on-disk HEAD copies would silently re-point 1,051 citations; the
    gate G6 states which source was used and fails the run if it is not the pinned vintage.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4, and the queue names both)
    RESOLUTION SOURCE {R_PROSE, R_SCRIPT, R_UNION, R_LOOSE} x CLAIM SET {NARROW, PROX, WIDE}
    = 12 cells, EVERY ONE PUBLISHED (.census.csv), and every one also reported on the 28-claim
    sub-population (.census.csv, columns `n28_*`).
      R_PROSE   1098's headline `R_STRICT`, verbatim: the claim's own prose must name the PANEL,
                name at least one CONSTRUCTION dimension (N, H, gross or cadence) and carry no
                out-of-family token.  Reproduced, not re-implemented from memory: G1 requires it
                to agree with 1098's committed `resolved` column on all 2,088 rows.
      R_SCRIPT  the queue's proposal taken literally: the prose is IGNORED ENTIRELY and panel, N,
                H, gross and cadence are read from the CITED SCRIPT's module-level constants.
      R_UNION   prose where the prose states a dimension, the cited script for the rest.  The
                claim is the prose; the script is its context.  HEADLINE.
      R_LOOSE   1098's FIRST CUT and rejected upper bound: panel from prose alone, every unstated
                dimension taking the frozen default, no in-family guard.  Carried because 1098
                published it (425) and because it bounds every count below it.
    NOT dials, all reported at every value: PANEL {U56, B136}; LADDER {N, H, GROSS, CADENCE} at
    1082/1086/1094/1097/1110's rung lists (9 + 4 + 10 + 4 = 27 rungs per panel, 54 books); the
    eight 4b legs; the four cost rungs {0, 10, 25, 50}; the three rule-8 choosers.  Frozen at
    936/1064/1071/1082/1086/1094/1097/1098's construction: CAND20 legs (21,252)/(0,126)/(0,63),
    cap INF, max_vol 0.60, gross 0.75 (except on the GROSS ladder), W cadence (except on the
    CADENCE ladder), min hold 126 (except on the H ladder), N = 20 (except on the N ladder),
    LAG 1, warm-up 260, IS end 2016-12-31, 4b constants 0.60 / 0.70.  The 1-bp ladder 0..200 is a
    MEASUREMENT AXIS, not a dial: no book is ever selected on it.

WHAT "THE SCRIPT PINS A DIMENSION" MEANS — DECLARED, AND IT IS THE WHOLE MEASUREMENT
    For each dimension d, collect every MODULE-LEVEL assignment (including tuple unpacking, which
    is how the record's own scripts write `GROSS0, FREQ0, HOLD0, N0 = 0.75, "W", 126, 20`) whose
    target name is in d's name set, and take the set of literal values on the right-hand side,
    flattening lists.  Then
        PINNED  exactly one distinct value        -> the script states the cell on this axis
        OPEN    two or more distinct values       -> the script WALKS A LADDER over this axis and
                                                    by construction cannot pin it
        SILENT  no matching assignment at all     -> the axis is not a named constant of this run
    PANEL additionally reads the call site, because the record's older scripts name no panel
    constant at all: `load_universe()` -> U56, `broad=True` / `prices_broad` -> B136,
    `small=True` / `prices_small` -> SMALL, unioned with any literal 'U56'/'B136'/'SMALL*' token
    in the source.  PINNED iff that union has exactly one member.
    A CALL-SITE default is NOT read as a pin (`def f(..., n=5)` is a signature, not a decision),
    and a right-hand side containing a function call is skipped unless it is a list literal.
    OPEN vs SILENT is reported separately at every dimension (.scripts.csv) because they are
    different failures: OPEN means the script is a LADDER RUN and no re-derivation can ever pin
    it from the script alone; SILENT means the constant is buried and a stamp could fix it.

DECLARED BEFORE ANY NUMBER, AND THE DISCLOSURE THAT GOES WITH IT
    CALIBRATED, NOT PREDICTED.  The census arm (the counts under each of the 12 cells) was built
    and run in a WIRING PROTOTYPE before this file was written, so H_CITE, H_SCRIPTWINS, H_GAIN,
    H_28 below are MEASUREMENTS reported against a stated bar, not forecasts, and they are
    labelled CALIBRATED wherever they are quoted.  Saying so is cheaper than pretending.
    Everything in the PRICE arm and the RE-SCORE arm below was unmeasured when this was written.
      (a) H_CITE [CALIBRATED] — >= 0.90 of the 2,088 claims resolve to a committed script that
          exists on disk.  This is the queue's own premise, first half.
      (b) H_SCRIPTWINS [CALIBRATED] — the queue's premise, second half, as a testable claim:
          R_SCRIPT ALONE re-scores MORE claims than R_PROSE does.  "every claim cites a script
          whose constants pin panel, N, H, gross and cadence exactly" predicts a large margin.
      (c) H_GAIN [CALIBRATED] — R_UNION re-scores strictly more than R_PROSE's 82.
      (d) H_28 [CALIBRATED] — a MAJORITY of the 28 CAGR-floor claims become re-scorable under
          R_UNION.  The queue's headline ask.
      (e) H_LADDERCAUSE [PRE-REGISTERED] — among (claim, dimension) pairs where the cited script
          does not pin the dimension, OPEN outnumbers SILENT.  If it holds, the failure is
          STRUCTURAL (the record runs ladders) and no stamp on the script can repair it.
      (f) H_REFUTE [PRE-REGISTERED] — among CAGR-floor claims that R_UNION makes re-scorable, a
          MAJORITY are REFUTED by their own cell's measured killer leg.  1098 could not test this
          at all (it resolved 0 of 28); its R_LOOSE upper bound read 0.8182 refuted and was
          published as a transfer, never as a re-derivation.
      (g) H_DDKILL [PRE-REGISTERED] — replicating 1098's answer on this run's own rebuild: among
          the 54 books a rising rung can kill, the modal killer leg is the DD cap.
      (h) THE DECISION RULE, fixed before any number.  The queue asks two counts and they are
          answered separately and never merged: SHARE THAT GAINS A CELL = re-scorable / 2,088
          under each source, and THE 28 = re-scorable of the 28 under each source.  A claim whose
          cell is stated but does not land on one of the 54 measured books is CELL-STATED and NOT
          re-scorable, and the two counts are printed side by side at every cell — a stated cell
          outside the family is a provenance gain, not a re-derivation.
      (i) NO CLAUSE, NO BOOK, NO RULES CHANGE IS PROPOSED unless a book clears a KEEP path under
          rule 8.  4a and 4b are scored at every book x every rung anyway (rule 4), and rule 8
          picks the ladder rung on 2009-2016 ALONE.

INHERITED, DECLARED.  1098's claims.csv is inherited as the POPULATION and as the gate target
    (82 / 425 / 2,088 / 28).  Nothing numeric from the price side is inherited: all 54 books are
    rebuilt from prices, and 936/1071/1082/1094/1097's committed figures are read only as gates.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every level is
    optimistic and every c* printed here is an UPPER BOUND on the true one; the bias does not
    cancel out of the 4b legs, which contrast a book against a real index.  The CENSUS and the
    RESOLUTION counts — this run's headline — are text and source-code scans and carry no market
    bias whatever.  The RE-SCORE arm inherits the price bias, because it reads a measured killer.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
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
SLUG = "can-the-RECORD-s-COST-CLAIMS-be-RESOLVED-from-their-SCRIPTS-rather-than-their-PROSE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
BT = Path(__file__).resolve().parent

# ---- the parent run, its committed population, and the commit that pinned the corpus
P1098_STEM = "2026-09-16_do-the-record-s-COMMITTED-COST-CLAIMS-PRICE-the-SHARPE-LEGS-or-only-the-CAGR-FLOOR_C"
P1098_CLAIMS = BT / f"{P1098_STEM}.claims.csv"
P1098_COMMIT = "3c1e2af61541685ad9deb457e6786e5575f5f439"
C1098_WIDE, C1098_PROX, C1098_NARROW = 2088, 125, 59
C1098_STRICT, C1098_LOOSE, C1098_N28 = 82, 425, 28
P1097 = BT / ("2026-09-16_is-the-BREAKEVEN-RUNG-c-star-PREDICTABLE-from-BINDING-LEG-MARGIN-"
              "over-TURNOVER-ALONE_C.cells.csv")

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0 = 0.75, "W", 126, 20
MOMLEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
PANELS = ["U56", "B136"]

FULL_LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
OOS_LEGS = ["O_S", "O_DD", "O_CAGR"]
ALL_LEGS = FULL_LEGS + OOS_LEGS
SHARPE_LEGS = {"L_H1", "L_H2", "L_OOS", "O_S"}
CAGR_LEGS = {"L_CAGR", "O_CAGR"}
DD_LEGS = {"L_DD", "O_DD"}

RUNGS = [0.0, 10.0, 25.0, 50.0]
PROTOCOL_RUNG = 10.0
CFINE = np.arange(0.0, 200.5, 1.0)

CLAIM_SETS = ["NARROW", "PROX", "WIDE"]                 # DIAL 2
SOURCES = ["R_PROSE", "R_SCRIPT", "R_UNION", "R_LOOSE"]  # DIAL 1
HEAD_SET, HEAD_SRC = "WIDE", "R_UNION"
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR"]

# committed cross-run anchors (quoted from committed result.md / CSV files)
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
C1094_CSTAR_FULL, C1094_CSTAR_OOS = 63.0, 64.0
C1094_TRIPLES = {0.0: (0.1764, 1.2131, -0.1945), 10.0: (0.1680, 1.1625, -0.1948),
                 25.0: (0.1554, 1.0865, -0.1951), 50.0: (0.1348, 0.9595, -0.1961)}

LOG: list[str] = []

if __import__("os").environ.get("SMOKE"):      # wiring check only; never used for a result
    LAD_N, LAD_H, LAD_G, LAD_C = [12, 20], [126, 252], [0.60, 0.75], ["W", "M"]
    LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
    CFINE = np.arange(0.0, 200.5, 20.0)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ---------------------------------------------- mechanics (1094/1097/1098's, verbatim)
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


def mech(px):
    parts = []
    for skip, look in MOMLEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel = []
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[priced[t, young]]
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
        nsel.append(len(sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W, np.asarray(nsel, float)


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


def margins(b, sb):
    """Each 4b leg's margin IN ITS OWN UNITS (1097/1098's, verbatim).  >= 0 means it passes."""
    return {"L_H1": b["H1"] - sb["H1"],
            "L_H2": b["H2"] - sb["H2"],
            "L_OOS": b["OOS_Sharpe"] - sb["OOS_Sharpe"],
            "L_DD": DD_CAP * abs(sb["MaxDD"]) - abs(b["MaxDD"]),
            "L_CAGR": b["CAGR"] - CAGR_FLOOR * sb["CAGR"],
            "O_S": b["OOS_Sharpe"] - sb["OOS_Sharpe"],
            "O_DD": DD_CAP * abs(sb["OOS_MaxDD"]) - abs(b["OOS_MaxDD"]),
            "O_CAGR": b["OOS_CAGR"] - CAGR_FLOOR * sb["OOS_CAGR"]}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def cstar_from_margin(mvec):
    ok = np.asarray(mvec) >= 0.0
    if not ok[0]:
        return np.nan, True, True
    run = int(np.argmin(ok)) if (~ok).any() else len(ok)
    contiguous = bool(ok[:run].all() and not ok[run:].any())
    return float(CFINE[run - 1]), contiguous, False


def ann_turn(tn, mask):
    n = int(mask.sum())
    return float(tn[mask].sum() / (n / 252.0)) if n else np.nan


# ============================================================ THE RESOLUTION LAYER
PYRX = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2}_[^\s`|,;)\"']+\.py)")

# 1098's out-of-family guard, verbatim.  A claim carrying one of these tokens is about a book
# outside the frozen family and is never re-derived onto a frozen cell, however well pinned.
OUT_OF_FAMILY = re.compile(
    r"ensemble|sleeve|overlay|tranche|\bband\b|trim|\bnull\b|coin[- ]flip|random key|QQQ|"
    r"spinoff|putwrite|option|deep ?value|MA-RS|scramble|shuffl|phase|rotat|"
    r"diversifier|equal[- ]weight control|BAND03|EWELIG|vol[- ]scal|min[- ]hold", re.I)

# --- the dimension name sets.  Declared here and nowhere else; matched case-insensitively
#     against MODULE-LEVEL assignment targets only.
DIM_NAMES = {
    "N":     r"(?:N0|NN|N|TOPN|TOP_N|NSEL|LAD_N|N_LAD|LADDER_N|N_GRID|NS|N_LIST|N_RUNGS)",
    "H":     r"(?:H0|HOLD0|HOLD|MINHOLD|MIN_HOLD|H|LAD_H|H_LAD|LADDER_H|H_GRID|HS|H_LIST|HOLDS)",
    "GROSS": r"(?:GROSS0|G0|GROSS|LAD_G|G_LAD|LADDER_G|GROSSES|G_GRID|GS|GROSS_LAD)",
    "CAD":   r"(?:FREQ0|FREQ|CADENCE|CAD|LAD_C|C_LAD|LADDER_C|FREQS|CADENCES|CAD_LAD)",
}
DIM_RX = {k: re.compile(r"^" + v + r"$", re.I) for k, v in DIM_NAMES.items()}
DIMS = ["PANEL", "N", "H", "GROSS", "CAD"]


def split_top(s, sep=","):
    """Split on SEP at bracket depth zero, so `[1, 2], 3` gives two fields, not three."""
    out, d, cur = [], 0, ""
    for ch in s:
        if ch in "([{":
            d += 1
        elif ch in ")]}":
            d -= 1
        if ch == sep and d == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out]


def assignments(src):
    """Yield (target, rhs) for every MODULE-LEVEL assignment, tuple unpacking included.
    Indented lines are skipped: a constant inside a function is a local, not the run's cell."""
    for line in src.split("\n"):
        if not line or line[0] in " \t#":
            continue
        if "=" not in line:
            continue
        lhs, _, rhs = line.partition("=")
        if rhs.startswith("=") or lhs.rstrip().endswith(("!", "<", ">", "+", "-", "*", "/", "%")):
            continue
        rhs = rhs.split("#")[0].strip()
        ln, rn = split_top(lhs.strip()), split_top(rhs)
        if len(ln) > 1 and len(ln) == len(rn):
            for a, b in zip(ln, rn):
                yield a.strip(), b.strip()
        else:
            yield lhs.strip(), rhs


def dim_values(src, dim):
    """The set of literal values the script assigns to DIM at module level."""
    vals: set[str] = set()
    for name, rhs in assignments(src):
        if not DIM_RX[dim].match(name):
            continue
        if dim == "CAD":
            vals |= set(re.findall(r"['\"]([DWMQ])['\"]", rhs))
        else:
            if re.search(r"[a-zA-Z_]\w*\s*\(", rhs) and not rhs.startswith("["):
                continue           # a computed RHS is not a stated constant
            vals |= set(re.findall(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])", rhs))
    return vals


def panel_values(src):
    """Literal panel tokens UNIONED with the call site, because the record's older scripts name
    no panel constant at all and choose their universe at `load_universe(...)`."""
    p = {("SMALL" if t.upper().startswith("SMALL") else t.upper())
         for t in re.findall(r"['\"](U56|B136|SMALL\d*)['\"]", src)}
    q = set()
    if re.search(r"broad\s*=\s*True|prices_broad|universe_broad", src):
        q.add("B136")
    if re.search(r"small\s*=\s*True|prices_small", src):
        q.add("SMALL")
    if re.search(r"load_universe\s*\(\s*\)|load_universe\s*\(\s*start", src):
        q.add("U56")
    return p | q


def script_facts(path: Path):
    src = path.read_text(errors="replace")
    pv = panel_values(src)
    out = {"PANEL": sorted(pv)}
    for d in ("N", "H", "GROSS", "CAD"):
        out[d] = sorted(dim_values(src, d))
    out["_bytes"] = len(src)
    return out


def one_of(vals, cast):
    if len(vals) != 1:
        return None
    try:
        return cast(vals[0])
    except (TypeError, ValueError):
        return None


def cell_of(pan, N, H, G, C, book_keys):
    """A (panel, N, H, gross, cadence) tuple RESOLVES to a measured book iff it is one of the 54
    one-factor-at-a-time rungs.  1098's `resolve_cell`, with the tuple handed in rather than
    re-parsed."""
    if pan not in PANELS:
        return None
    for lad, rung in book_keys.get(pan, []):
        if lad == "N" and (N, H, G, C) == (rung, HOLD0, GROSS0, FREQ0):
            return (pan, lad, rung)
        if lad == "H" and (N, H, G, C) == (N0, rung, GROSS0, FREQ0):
            return (pan, lad, rung)
        if lad == "GROSS" and (N, H, G, C) == (N0, HOLD0, rung, FREQ0):
            return (pan, lad, rung)
        if lad == "CADENCE" and (N, H, G, C) == (N0, HOLD0, GROSS0, rung):
            return (pan, lad, rung)
    return None


def git_show(commit, relpath):
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{relpath}"],
                          capture_output=True, text=True, check=True).stdout


# ======================================================================================= main
def main():
    t0 = time.time()
    P(f"# QUEUE idea 1149 (lane C, {DATE}) — can the RECORD's COST CLAIMS be RESOLVED from")
    P("#   their SCRIPTS rather than their PROSE?")
    P("#")
    P("# POPULATION: 1098's OWN committed claims.csv, all 2,088 rows — a CENSUS, not a sample.")
    P("# DIAL 1 RESOLUTION SOURCE {R_PROSE, R_SCRIPT, R_UNION, R_LOOSE}")
    P("# DIAL 2 CLAIM SET {NARROW, PROX, WIDE};  12 cells, all published.")
    P("# TWO COUNTS, NEVER MERGED: CELL-STATED (the source pins panel + >=1 dimension) and")
    P("#   RE-SCORABLE (that cell is one of the 54 measured books).  A stated cell outside the")
    P("#   family is a PROVENANCE gain, not a re-derivation.")
    P("# CALIBRATED, NOT PREDICTED: the census arm was run in a wiring prototype before this")
    P("#   file was written.  H_CITE / H_SCRIPTWINS / H_GAIN / H_28 are MEASUREMENTS against a")
    P("#   stated bar and are labelled CALIBRATED everywhere.  H_LADDERCAUSE, H_REFUTE and")
    P("#   H_DDKILL were unmeasured when this was written.")
    P("")
    gates: dict[str, tuple] = {}

    # ------------------------------------------------- PART 0: the pinned corpus vintage
    if not P1098_CLAIMS.exists():
        raise SystemExit(f"population file missing: {P1098_CLAIMS}")
    cen = pd.read_csv(P1098_CLAIMS)
    okpop = (len(cen) == C1098_WIDE and int(cen.PROX.sum()) == C1098_PROX
             and int(cen.NARROW.sum()) == C1098_NARROW
             and int(cen.resolved.sum()) == C1098_STRICT
             and int(cen.resolved_loose.sum()) == C1098_LOOSE)
    gates["G0 POPULATION is 1098's committed claims.csv (2088/125/59, resolved 82, loose 425)"] = (
        0.0 if okpop else 1.0, okpop)

    vintage_ok = True
    try:
        LB = git_show(P1098_COMMIT, "research/LEADERBOARD.md").split("\n")
        CL = git_show(P1098_COMMIT, "research/CHANGELOG.md").split("\n")
        vsrc = f"git {P1098_COMMIT[:8]}"
    except Exception as e:                                        # noqa: BLE001
        LB = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="replace").split("\n")
        CL = (ROOT / "research" / "CHANGELOG.md").read_text(errors="replace").split("\n")
        vsrc, vintage_ok = f"ON-DISK HEAD FALLBACK ({e})", False
    vh = hashlib.sha256(("\n".join(LB) + "\n".join(CL)).encode()).hexdigest()[:16]
    P(f"## CORPUS VINTAGE: {vsrc}  LEADERBOARD {len(LB):,} lines, CHANGELOG {len(CL):,} lines, "
      f"sha256[:16] {vh}")
    gates["G6 corpus recovered at 1098's own commit (not HEAD)"] = (0.0 if vintage_ok else 1.0,
                                                                    vintage_ok)
    # HEAD sizes, published as the control: the corpus is not the same object today
    lb_head = len((ROOT / "research" / "LEADERBOARD.md").read_text(errors="replace").split("\n"))
    cl_head = len((ROOT / "research" / "CHANGELOG.md").read_text(errors="replace").split("\n"))
    nres_1098 = len([p for p in BT.glob("*.result.md")])
    P(f"   CONTROL, today's corpus: LEADERBOARD {lb_head:,} lines (+{lb_head - len(LB):,}), "
      f"CHANGELOG {cl_head:,} (+{cl_head - len(CL):,}), {nres_1098:,} result.md on disk — "
      f"a re-harvest TODAY would not be 1098's population, which is why it is read from file.")

    # -------------------------------------------------- PART 1: which script does a claim cite?
    def cite(src, line):
        line = int(line)
        if src == "LEADERBOARD.md":
            if 1 <= line <= len(LB):
                ln = LB[line - 1]
                if ln.startswith("|"):
                    cells = [c.strip().strip("`") for c in ln.strip().strip("|").split("|")]
                    m = PYRX.search(cells[-1])          # PROTOCOL rule 5: last column = script
                    if m:
                        return m.group(1), "LB_LASTCOL"
                m = PYRX.search(ln)
                if m:
                    return m.group(1), "LB_INLINE"
            return "", "NONE"
        if src == "CHANGELOG.md":
            fwd = range(line - 1, min(line + 40, len(CL)))
            bwd = range(max(line - 2, 0), max(line - 40, 0), -1)
            for j in list(fwd) + list(bwd):
                m = PYRX.search(CL[j])
                if m:
                    return m.group(1), "CL_ENTRY"
            return "", "NONE"
        if src.endswith(".result.md"):
            return src[: -len(".result.md")] + ".py", "SIBLING"
        return "", "NONE"

    cited = [cite(r.src, r.line) for r in cen.itertuples()]
    cen["script"] = [c[0] for c in cited]
    cen["cite_route"] = [c[1] for c in cited]
    cen["script_exists"] = [bool(s) and (BT / s).exists() for s in cen.script]
    n_cited, n_exists = int((cen.script != "").sum()), int(cen.script_exists.sum())
    P("")
    P(f"## PART 1 — DOES A CLAIM CITE A COMMITTED SCRIPT?  {n_exists:,} of {len(cen):,} "
      f"({n_exists / len(cen):.4f}) resolve to a script that EXISTS on disk "
      f"({n_cited:,} carry a citation).")
    for route, g in cen.groupby("cite_route"):
        P(f"   {route:<11s} n={len(g):5,d}  exists {int(g.script_exists.sum()):5,d}")

    # -------------------------------------------------- PART 2: what does that script pin?
    facts: dict[str, dict] = {}
    for s in sorted(set(cen.script[cen.script_exists])):
        facts[s] = script_facts(BT / s)
    P("")
    P(f"## PART 2 — WHAT DO THOSE {len(facts):,} DISTINCT SCRIPTS PIN?  "
      "PINNED = exactly one literal value; OPEN = two or more (the script WALKS A LADDER over "
      "the axis); SILENT = no module-level constant of that name at all.")
    srows = []
    for s, f in facts.items():
        row = dict(script=s, bytes=f["_bytes"])
        for d in DIMS:
            v = f[d]
            row[f"{d}_state"] = "PINNED" if len(v) == 1 else ("OPEN" if len(v) > 1 else "SILENT")
            row[f"{d}_n"] = len(v)
            row[f"{d}_vals"] = ";".join(str(x) for x in v[:8])
        srows.append(row)
    scripts = pd.DataFrame(srows)
    for d in DIMS:
        vc = scripts[f"{d}_state"].value_counts()
        P(f"   {d:<6s} PINNED {int(vc.get('PINNED', 0)):4d}   OPEN {int(vc.get('OPEN', 0)):4d}"
          f"   SILENT {int(vc.get('SILENT', 0)):4d}   (of {len(scripts)} scripts)")

    # weighted by CLAIM, which is the population the queue asks about
    P("   weighted by CLAIM (the population under census):")
    open_pairs = silent_pairs = 0
    for d in DIMS:
        st = [(facts[s][d] if e else None) for s, e in zip(cen.script, cen.script_exists)]
        pin = sum(1 for v in st if v is not None and len(v) == 1)
        opn = sum(1 for v in st if v is not None and len(v) > 1)
        sil = sum(1 for v in st if v is not None and len(v) == 0) + int((~cen.script_exists).sum())
        cen[f"s{d}_state"] = ["PINNED" if (v is not None and len(v) == 1) else
                              "OPEN" if (v is not None and len(v) > 1) else "SILENT" for v in st]
        if d != "PANEL":
            open_pairs += opn
            silent_pairs += sil
        P(f"     {d:<6s} PINNED {pin:5,d}   OPEN {opn:5,d}   SILENT {sil:5,d}")
    P(f"   H_LADDERCAUSE population (the four CONSTRUCTION dimensions, claim-weighted): "
      f"OPEN {open_pairs:,} vs SILENT {silent_pairs:,}")

    # -------------------------------------------------- PART 3: the 54 books (the price leg)
    P("")
    P("## PART 3 — THE PRICE LEG: 54 books rebuilt from prices, 1-bp cost ladder 0..200")
    bookrows, gridrows, picks, benchrows, ladrows = [], [], [], [], []
    book_keys: dict[str, list] = {p: [] for p in PANELS}
    store: dict[tuple, dict] = {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        benchrows.append(dict(panel=panel, series="SPY", **sb))
        P(f"   {panel}: {K} cols, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{warm.sum() / 252.0:.2f} scored years")
        P(f"     SPY  full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%}")

        live = {}
        for freq in sorted({FREQ0} | set(LAD_C)):
            r0 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=freq)
            live[freq] = (r0["returns"].values, r0["turnover"].values)
        lg, lt = live[FREQ0]
        lb_by_rung = {c: blocks(lg - lt * c / 1e4, warm, ins, oos) for c in RUNGS}
        benchrows.append(dict(panel=panel, series=f"RULESv2@{int(PROTOCOL_RUNG)}bps",
                              **lb_by_rung[PROTOCOL_RUNG]))
        b10 = lb_by_rung[PROTOCOL_RUNG]
        P(f"     RULES v2 @10 bps  full {b10['CAGR']:.2%} / {b10['Sharpe']:.4f} / "
          f"{b10['MaxDD']:.2%}  OOS {b10['OOS_CAGR']:.2%} / {b10['OOS_Sharpe']:.4f} / "
          f"{b10['OOS_MaxDD']:.2%}")

        if panel == "U56":
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN committed SPY OOS triple (HEAD tape — CARRIED, see G3b/G11)"] = (d3, d3 < 5e-4)
            d4 = abs(b10["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G4 live RULES v2 MaxDD @10 bps == committed -12.05%"] = (d4, d4 < 5e-4)

        masks = {f: np.roll(rebalance_mask(idx, f).values, LAG) for f in set(LAD_C) | {FREQ0}}
        rebs = {f: np.flatnonzero(rebalance_mask(idx, f).values) for f in set(LAD_C) | {FREQ0}}

        for lad, rungs in LADDERS.items():
            for rung in rungs:
                N = rung if lad == "N" else N0
                H = rung if lad == "H" else HOLD0
                G = rung if lad == "GROSS" else GROSS0
                C = rung if lad == "CADENCE" else FREQ0
                W, nsel = build(rank_key, elig, priced, rebs[C], N, H, T, K, G)
                g, tn = nrun(rets, lagmat(W), masks[C])
                turn = ann_turn(tn, warm)

                if panel == "U56" and lad == "N" and rung == 20:
                    wdf = pd.DataFrame(W, index=idx, columns=px.columns)
                    for cg, nm in ((0.0, "G1a"), (10.0, "G1b")):
                        eng = backtest(px, wdf, cost_bps=cg, freq=C)["returns"].values
                        d = float(np.abs((g - tn * cg / 1e4)[WARMUP:] - eng[WARMUP:]).max())
                        gates[f"{nm} r(c)=g-tn*c/1e4 == engine.backtest @{cg:.0f} bps"] = (d, d < 1e-12)
                    m = fmet((g - tn * PROTOCOL_RUNG / 1e4)[warm])
                    d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
                    gates["G2 CROSS-RUN committed U56 W/H126 N=20 triple @10 bps (HEAD tape — CARRIED, see G2b/G11)"] = (d2, d2 < 5e-3)

                M = {L: np.empty(len(CFINE)) for L in ALL_LEGS}
                for j, c in enumerate(CFINE):
                    mm = margins(blocks(g - tn * c / 1e4, warm, ins, oos), sb)
                    for L in ALL_LEGS:
                        M[L][j] = mm[L]
                cst, dead0, contig, surv, eff = {}, {}, {}, {}, {}
                for L in ALL_LEGS:
                    cst[L], contig[L], dead0[L] = cstar_from_margin(M[L])
                    surv[L] = bool((not dead0[L]) and M[L][-1] >= 0.0)
                    eff[L] = (np.inf if surv[L] else cst[L])

                pass0_full = not any(dead0[L] for L in FULL_LEGS)
                cstar_full_raw = (min(cst[L] for L in FULL_LEGS) if pass0_full else np.nan)
                cstar_full = (min(eff[L] for L in FULL_LEGS) if pass0_full else np.nan)
                killer = (sorted(L for L in FULL_LEGS if eff[L] == cstar_full)
                          if pass0_full and np.isfinite(cstar_full) else [])
                last_leg = (sorted(FULL_LEGS, key=lambda L: eff[L])[-1] if pass0_full else "")
                pass0_oos = not any(dead0[L] for L in OOS_LEGS)
                cstar_oos = (min(eff[L] for L in OOS_LEGS) if pass0_oos else np.nan)

                b_by_rung = {c: blocks(g - tn * c / 1e4, warm, ins, oos) for c in RUNGS}
                lgc, ltc = live[C]
                lbc = {c: blocks(lgc - ltc * c / 1e4, warm, ins, oos) for c in RUNGS}

                row = dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=G, cadence=C,
                           mean_nsel=float(nsel.mean()), turnover=turn,
                           pass0_full=pass0_full, cstar_full=cstar_full,
                           cstar_full_raw=cstar_full_raw,
                           alive200=bool(pass0_full and not np.isfinite(cstar_full)),
                           killer=",".join(killer) if killer else
                           ("DEAD0" if not pass0_full else "NONE<=200"),
                           killer_kind=("SHARPE" if killer and set(killer) <= SHARPE_LEGS else
                                        "CAGR" if killer and set(killer) <= CAGR_LEGS else
                                        "DD" if killer and set(killer) <= DD_LEGS else
                                        "MULTI" if killer else "NONE"),
                           last_leg=last_leg, pass0_oos=pass0_oos, cstar_oos=cstar_oos)
                for L in ALL_LEGS:
                    row[f"cstar_{L}"] = cst[L]
                    row[f"dead0_{L}"] = dead0[L]
                for c in RUNGS:
                    b = b_by_rung[c]
                    mm = margins(b, sb)
                    l4a = legs_4a(b, lbc[c])
                    p4b = all(mm[L] >= 0 for L in FULL_LEGS)
                    p4bo = all(mm[L] >= 0 for L in OOS_LEGS)
                    row[f"CAGR{int(c)}"] = b["CAGR"]
                    row[f"Sharpe{int(c)}"] = b["Sharpe"]
                    row[f"MaxDD{int(c)}"] = b["MaxDD"]
                    row[f"H1_{int(c)}"] = b["H1"]
                    row[f"H2_{int(c)}"] = b["H2"]
                    row[f"OOS_Sharpe{int(c)}"] = b["OOS_Sharpe"]
                    row[f"OOS_CAGR{int(c)}"] = b["OOS_CAGR"]
                    row[f"OOS_MaxDD{int(c)}"] = b["OOS_MaxDD"]
                    row[f"pass4b{int(c)}"] = p4b
                    row[f"pass4bOOS{int(c)}"] = p4bo
                    row[f"pass4a{int(c)}"] = all(l4a.values())
                    hr = {L: (eff[L] - c) for L in FULL_LEGS if not dead0[L] and eff[L] >= c}
                    row[f"binding{int(c)}"] = (min(hr, key=hr.get) if hr else "DEAD")
                    gridrows.append(dict(panel=panel, ladder=lad, rung=rung, cost_rung=c,
                                         pass4b=p4b, pass4b_oos=p4bo, pass4a=all(l4a.values()),
                                         binding=row[f"binding{int(c)}"],
                                         CAGR=b["CAGR"], Sharpe=b["Sharpe"], MaxDD=b["MaxDD"],
                                         H1=b["H1"], H2=b["H2"], OOS_CAGR=b["OOS_CAGR"],
                                         OOS_Sharpe=b["OOS_Sharpe"], OOS_MaxDD=b["OOS_MaxDD"],
                                         turnover=turn, **l4a))
                bookrows.append(row)
                book_keys[panel].append((lad, rung))
                store[(panel, lad, rung)] = dict(
                    IS_S={c: b_by_rung[c]["IS_Sharpe"] for c in RUNGS},
                    IS_DD={c: b_by_rung[c]["IS_MaxDD"] for c in RUNGS},
                    IS_CAGR={c: b_by_rung[c]["IS_CAGR"] for c in RUNGS},
                    OOS={c: (b_by_rung[c]["OOS_CAGR"], b_by_rung[c]["OOS_Sharpe"],
                             b_by_rung[c]["OOS_MaxDD"]) for c in RUNGS},
                    FULL={c: (b_by_rung[c]["CAGR"], b_by_rung[c]["Sharpe"], b_by_rung[c]["MaxDD"],
                              b_by_rung[c]["H1"], b_by_rung[c]["H2"]) for c in RUNGS},
                    p4b={c: all(margins(b_by_rung[c], sb)[L] >= 0 for L in FULL_LEGS) for c in RUNGS},
                    p4bo={c: all(margins(b_by_rung[c], sb)[L] >= 0 for L in OOS_LEGS) for c in RUNGS},
                    p4a={c: all(legs_4a(b_by_rung[c], lbc[c]).values()) for c in RUNGS},
                    turn=turn)
                ladrows.append(dict(panel=panel, ladder=lad, rung=rung,
                                    **{f"cstar_{L}": cst[L] for L in ALL_LEGS}))

        if panel == "U56":
            W, _ = build(rank_key, elig, priced, rebs[FREQ0], 12, 21, T, K, GROSS0)
            g, tn = nrun(rets, lagmat(W), masks[FREQ0])
            trip = {}
            for c in RUNGS:
                b = blocks(g - tn * c / 1e4, warm, ins, oos)
                trip[c] = (b["CAGR"], b["Sharpe"], b["MaxDD"])
            d5 = max(max(abs(trip[c][i] - C1094_TRIPLES[c][i]) for i in range(3)) for c in RUNGS)
            gates["G5 CROSS-RUN 1094's committed n=12/H=21 ladder, 0/10/25/50 bps (HEAD tape — CARRIED, see G5d/G11)"] = (d5, d5 < 5e-4)
            Mc = {L: np.empty(len(CFINE)) for L in ALL_LEGS}
            for j, c in enumerate(CFINE):
                mm = margins(blocks(g - tn * c / 1e4, warm, ins, oos), sb)
                for L in ALL_LEGS:
                    Mc[L][j] = mm[L]
            cs = {L: cstar_from_margin(Mc[L]) for L in ALL_LEGS}
            cf = min(cs[L][0] for L in FULL_LEGS)
            co = min(cs[L][0] for L in OOS_LEGS)
            k94 = sorted(L for L in FULL_LEGS if cs[L][0] == cf)
            d6 = max(abs(cf - C1094_CSTAR_FULL), abs(co - C1094_CSTAR_OOS))
            gates[f"G5b 1094's c* full/OOS == 63/64 (got {cf:.0f}/{co:.0f}, killer "
                  f"{','.join(k94)})"] = (d6, d6 < 1e-9)

    books = pd.DataFrame(bookrows)
    grid = pd.DataFrame(gridrows)

    if P1097.exists():
        c97 = pd.read_csv(P1097)
        mine = books[(books.ladder == "N") & (books.H == HOLD0)][["panel", "N", "cstar_full_raw"]] \
            .rename(columns={"cstar_full_raw": "cstar_full"})
        ov = c97[c97.H == HOLD0][["panel", "N", "cstar_full"]].merge(
            mine, on=["panel", "N"], suffixes=("_97", "_now"))
        both = ov.dropna()
        d7 = float(np.abs(both.cstar_full_97 - both.cstar_full_now).max()) if len(both) else np.nan
        agree = bool((ov.cstar_full_97.isna() == ov.cstar_full_now.isna()).all())
        gates[f"G7 CROSS-RUN 1097's committed c*_full on the {len(ov)} shared N/H126 cells"] = (
            (d7 if np.isfinite(d7) else 0.0), (agree and (not np.isfinite(d7) or d7 < 1e-9)))
    else:
        gates["G7 CROSS-RUN 1097 cells.csv present"] = (1.0, False)

    kill_by_cell = {(r.panel, r.ladder, r.rung): (r.killer, r.killer_kind)
                    for r in books.itertuples()}

    # ------------------------------------------- PART 3c: the price VINTAGE, carried not absorbed
    # G2/G3/G5 are cross-run gates against constants 936/1094/1098 computed on the tape as it
    # stood at 1098's own commit.  `data/prices.csv` is REWRITTEN NIGHTLY (idea 1163: 0 of 11
    # transitions append-only, ~10% of an 18-year tape restated every night), so those gates are
    # run TWICE and BOTH readings are published: once on HEAD, where they may fail, and once on
    # the tape recovered from git at 1098's own commit, which is the tape the constants were
    # computed on.  Nothing is widened; the defect is measured.
    P("")
    P("## PART 3c — THE PRICE VINTAGE (idea 1163's defect, carried and measured)")
    try:
        import io
        pv = pd.read_csv(io.StringIO(git_show(P1098_COMMIT, "data/prices.csv")),
                         index_col=0, parse_dates=True).sort_index()
        head = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()
        shared_i = pv.index.intersection(head.index)
        shared_c = pv.columns.intersection(head.columns)
        a = pv.loc[shared_i, shared_c].values.astype(float)
        b = head.loc[shared_i, shared_c].values.astype(float)
        fin = np.isfinite(a) & np.isfinite(b)
        diff = fin & (a != b)
        rel = np.abs(a[diff] - b[diff]) / np.maximum(np.abs(a[diff]), 1e-12) if diff.any() else np.array([0.0])
        first_row = (np.flatnonzero(diff.any(axis=1))[0] if diff.any() else -1)
        P(f"   pinned tape {P1098_COMMIT[:8]}: {pv.shape[0]:,} rows x {pv.shape[1]} cols; "
          f"HEAD: {head.shape[0]:,} x {head.shape[1]}  (extra bars at HEAD: "
          f"{len(head.index.difference(pv.index))})")
        P(f"   shared cells {int(fin.sum()):,}; RESTATED {int(diff.sum()):,} "
          f"({diff.sum() / max(fin.sum(), 1):.4f}); max |relative move| {rel.max():.3e}; "
          f"earliest restated bar {shared_i[first_row].date() if first_row >= 0 else 'none'}")
        gates[f"G11 price tape RESTATED between 1098's commit and HEAD "
              f"({int(diff.sum()):,} of {int(fin.sum()):,} cells, "
              f"{len(head.index.difference(pv.index))} extra bar(s)) — MEASURED, not asserted"] = (
            float(diff.sum() / max(fin.sum(), 1)), True)

        # --- re-read the three cross-run anchors on the PINNED tape
        import json as _json
        U = _json.loads((ROOT / "research" / "universe.json").read_text())
        tk = sorted({t for g in U.values() for t in g} - {"BTC-USD", "ETH-USD"})
        pxv = pv[[c for c in tk if c in pv.columns]].loc["2008-01-01":].dropna(how="all").ffill()
        iv, Kv, Tv = pxv.index, len(pxv.columns), len(pxv)
        rv = pxv.pct_change().fillna(0.0).values
        prv = pxv.notna().values
        wv, inv, ov = windows(iv)
        scv, elv = mech(pxv)
        rkv = -np.nan_to_num(scv, nan=-np.inf)
        rkv[np.isnan(scv)] = np.inf
        mkv = rebalance_mask(iv, FREQ0).values
        sbv = blocks(pxv["SPY"].pct_change().fillna(0.0).values, wv, inv, ov)
        d3p = max(abs(sbv["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                  abs(sbv["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                  abs(sbv["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
        gates["G3b CROSS-RUN committed SPY OOS triple ON THE PINNED TAPE"] = (d3p, d3p < 5e-4)
        Wv, _ = build(rkv, elv, prv, np.flatnonzero(mkv), N0, HOLD0, Tv, Kv, GROSS0)
        gv, tv = nrun(rv, lagmat(Wv), np.roll(mkv, LAG))
        mv = fmet((gv - tv * PROTOCOL_RUNG / 1e4)[wv])
        d2p = max(abs(mv[i] - A936_WH126[i]) for i in range(3))
        gates["G2b CROSS-RUN committed U56 W/H126 N=20 triple @10 bps ON THE PINNED TAPE"] = (
            d2p, d2p < 5e-4)
        Wc, _ = build(rkv, elv, prv, np.flatnonzero(mkv), 12, 21, Tv, Kv, GROSS0)
        gc, tc = nrun(rv, lagmat(Wc), np.roll(mkv, LAG))
        d5p = max(max(abs(blocks(gc - tc * c / 1e4, wv, inv, ov)[k] - C1094_TRIPLES[c][i])
                      for i, k in enumerate(("CAGR", "Sharpe", "MaxDD"))) for c in RUNGS)
        gates["G5d CROSS-RUN 1094's n=12/H=21 ladder ON THE PINNED TAPE"] = (d5p, d5p < 5e-4)
        P(f"   anchors on the PINNED tape: SPY OOS {d3p:.2e}, 936 triple {d2p:.2e}, "
          f"1094 ladder {d5p:.2e}   — compare the same three on HEAD in the GATES block.")
    except Exception as e:                                        # noqa: BLE001
        gates[f"G11 price vintage recoverable from git ({type(e).__name__}: {e})"] = (1.0, False)

    # -------------------------------------------------- PART 4: the 12 resolution cells
    P("")
    P("## PART 4 — THE 12 CELLS (RESOLUTION SOURCE x CLAIM SET)")

    def resolve(row, mode, guard_script=False):
        """-> (stated, cell, panel, N, H, G, C, why).  `stated` means the SOURCE pins the panel
        and (except under R_LOOSE) at least one construction dimension, and the claim carries no
        out-of-family token.  `cell` is non-None only when that tuple is one of the 54 books."""
        f = facts.get(row["script"]) if row["script_exists"] else None
        pP = row["panel"] if row["panel"] in PANELS else ""
        pN = int(row["cell_N"]) if np.isfinite(row["cell_N"]) else None
        pH = int(row["cell_H"]) if np.isfinite(row["cell_H"]) else None
        pG = float(row["cell_G"]) if np.isfinite(row["cell_G"]) else None
        pC = row["cell_C"] if isinstance(row["cell_C"], str) and row["cell_C"] else None
        sP = (f["PANEL"][0] if f and len(f["PANEL"]) == 1 else "")
        sN = one_of(f["N"], int) if f else None
        sH = one_of(f["H"], int) if f else None
        sG = one_of(f["GROSS"], float) if f else None
        sC = (f["CAD"][0] if f and len(f["CAD"]) == 1 else None)
        if mode == "R_PROSE":
            Pn, N, H, G, C = pP, pN, pH, pG, pC
        elif mode == "R_SCRIPT":
            Pn, N, H, G, C = sP, sN, sH, sG, sC
        elif mode == "R_UNION":
            Pn = pP or sP
            N = pN if pN is not None else sN
            H = pH if pH is not None else sH
            G = pG if pG is not None else sG
            C = pC or sC
        else:                                  # R_LOOSE — 1098's rejected first cut, verbatim:
            # the PROSE's dimensions with the frozen defaults filling the rest, panel from prose,
            # NO dimension requirement and NO in-family guard.  (An all-defaults reading would be
            # a different and looser rule and would not reproduce 1098's committed 425.)
            Pn, N, H, G, C = pP, pN, pH, pG, pC
        ndim = sum(x is not None for x in (N, H, G, C))
        infam = not OUT_OF_FAMILY.search(str(row["text"]))
        if guard_script:
            # A DEFECT IN THE INHERITED GUARD, FOUND BY THIS RUN AND PRICED RATHER THAN HIDDEN.
            # 1098's OUT_OF_FAMILY guard reads the CLAIM'S PROSE, which was right when the cell
            # also came from the prose.  Once the cell comes from the CITED SCRIPT the guard and
            # the resolution read different objects, and a claim whose prose says nothing
            # suspicious can be attributed to a cell derived from an `ensemble-` or `sleeve-`
            # script.  R_UNION_G applies the same guard to the SCRIPT NAME as well.  It is a
            # REPAIR reported beside the headline, not a third tuned parameter: nothing is ever
            # selected on it and both readings are published at every cell.
            infam = infam and not OUT_OF_FAMILY.search(str(row["script"]))
        if mode == "R_LOOSE":
            stated = bool(Pn in PANELS)        # no dim requirement, NO in-family guard
        else:
            stated = bool(Pn in PANELS and ndim >= 1 and infam)
        cell = (cell_of(Pn, N if N is not None else N0, H if H is not None else HOLD0,
                        G if G is not None else GROSS0, C or FREQ0, book_keys)
                if Pn in PANELS else None)
        return stated, cell, Pn, N, H, G, C

    for mode in SOURCES + ["R_UNION_G"]:
        base, gs = (("R_UNION", True) if mode == "R_UNION_G" else (mode, False))
        res = [resolve(r, base, gs) for _, r in cen.iterrows()]
        cen[f"{mode}_stated"] = [r[0] for r in res]
        cen[f"{mode}_cell"] = [f"{r[1][0]}/{r[1][1]}={r[1][2]}" if r[1] else "" for r in res]
        cen[f"{mode}_scorable"] = [bool(r[0] and r[1] is not None) for r in res]
        cen[f"{mode}_key"] = [r[1] for r in res]

    agree = int((cen.R_PROSE_scorable == cen.resolved.astype(bool)).sum())
    gates[f"G1 R_PROSE reproduces 1098's committed R_STRICT on all {len(cen):,} rows"] = (
        float(len(cen) - agree), agree == len(cen))
    d_loose = abs(int(cen.R_LOOSE_scorable.sum()) - C1098_LOOSE)
    gates["G1b R_LOOSE reproduces 1098's committed resolved_loose (425)"] = (float(d_loose),
                                                                             d_loose == 0)

    is28 = cen.PROX & cen.names_CAGR & ~cen.names_SHARPE & ~cen.names_DD
    gates["G8 the 28 CAGR-floor claims are recovered as 1098 defined them"] = (
        float(abs(int(is28.sum()) - C1098_N28)), int(is28.sum()) == C1098_N28)
    cen["is28"] = is28

    censusrows = []
    for mode in SOURCES + ["R_UNION_G"]:
        for cs in CLAIM_SETS:
            sub = cen[cen[cs]]
            s28 = cen[cen.is28] if cs != "NARROW" else cen[cen.is28 & cen.NARROW]
            censusrows.append(dict(
                resolution_source=mode, claim_set=cs, n_claims=len(sub),
                n_cited=int((sub.script != "").sum()), n_script_exists=int(sub.script_exists.sum()),
                n_cell_stated=int(sub[f"{mode}_stated"].sum()),
                n_rescorable=int(sub[f"{mode}_scorable"].sum()),
                share_cell_stated=float(sub[f"{mode}_stated"].mean()) if len(sub) else np.nan,
                share_rescorable=float(sub[f"{mode}_scorable"].mean()) if len(sub) else np.nan,
                n28=len(s28), n28_cell_stated=int(s28[f"{mode}_stated"].sum()),
                n28_rescorable=int(s28[f"{mode}_scorable"].sum())))
    census = pd.DataFrame(censusrows)
    P("   source     set      claims   cited   cell-stated   RE-SCORABLE      share | 28: "
      "stated  RE-SCORABLE")
    for r in census.itertuples():
        P(f"   {r.resolution_source:<10s} {r.claim_set:<7s} {r.n_claims:6,d}  {r.n_cited:6,d}   "
          f"{r.n_cell_stated:9,d}   {r.n_rescorable:11,d}   {r.share_rescorable:8.4f} | "
          f"{r.n28_cell_stated:6d}  {r.n28_rescorable:9d}")

    # -------------------------------------------------- PART 5: re-score the CAGR-floor claims
    def verdict_of(cell):
        killer, kind = kill_by_cell[cell]
        if killer == "DEAD0":
            return killer, kind, "UNDECIDED_DEAD0"
        if killer == "NONE<=200" or kind == "NONE":
            return killer, kind, "UNDECIDED_NO_CSTAR"
        if set(killer.split(",")) & CAGR_LEGS:
            return killer, kind, "CONFIRMED"
        return killer, kind, "REFUTED"

    resc = []
    for mode in SOURCES + ["R_UNION_G"]:
        for _, r in cen[cen.is28].iterrows():
            key = r[f"{mode}_key"]
            ok = bool(r[f"{mode}_scorable"]) and key in kill_by_cell
            if ok:
                killer, kind, v = verdict_of(key)
                basis = "MEASURED"
            else:
                killer, kind, v, basis = "", "", "TRANSFERRED", "TRANSFERRED"
            resc.append(dict(resolution_source=mode, src=r["src"], line=r["line"],
                             script=r["script"], cell=r[f"{mode}_cell"],
                             cell_stated=bool(r[f"{mode}_stated"]), basis=basis, verdict=v,
                             measured_killer=killer, measured_kind=kind,
                             text=str(r["text"])[:240]))
    rescore = pd.DataFrame(resc)
    P("")
    P("## PART 5 — RE-SCORING THE 28 CAGR-FLOOR CLAIMS AGAINST THEIR OWN CELL'S KILLER LEG")
    for mode in SOURCES + ["R_UNION_G"]:
        m = rescore[(rescore.resolution_source == mode) & (rescore.basis == "MEASURED")]
        vc = m.verdict.value_counts().to_dict()
        P(f"   {mode:<10s} measured {len(m):3d} of {C1098_N28}   "
          f"CONFIRMED {vc.get('CONFIRMED', 0):3d}   REFUTED {vc.get('REFUTED', 0):3d}   "
          f"UNDECIDED {vc.get('UNDECIDED_DEAD0', 0) + vc.get('UNDECIDED_NO_CSTAR', 0):3d}"
          f"   TRANSFERRED {C1098_N28 - len(m):3d}")

    # -------------------------------------------------- PART 6: rule 8 + both KEEP paths
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            for c in RUNGS:
                for ch in CHOOSERS:
                    key = {"C_ISSHARPE": "IS_S", "C_ISDD": "IS_DD", "C_ISCAGR": "IS_CAGR"}[ch]
                    vals = {rg: store[(panel, lad, rg)][key][c] for rg in rungs}
                    pick = max(vals, key=lambda k: vals[k])
                    st = store[(panel, lad, pick)]
                    oc, os_, od = st["OOS"][c]
                    fc, fs, fd, f1, f2 = st["FULL"][c]
                    picks.append(dict(panel=panel, ladder=lad, cost_rung=c, chooser=ch,
                                      pick=pick, IS_stat=vals[pick], turnover=st["turn"],
                                      CAGR=fc, Sharpe=fs, MaxDD=fd, H1=f1, H2=f2,
                                      OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                                      pass4b=st["p4b"][c], pass4b_oos=st["p4bo"][c],
                                      pass4a=st["p4a"][c]))
    pick_df = pd.DataFrame(picks)

    # determinism gate
    px = load_universe().dropna(how="all").ffill()
    idx, K, T = px.index, len(px.columns), len(px)
    rets = px.pct_change().fillna(0.0).values
    priced = px.notna().values
    warm, ins, oos = windows(idx)
    sc, elig = mech(px)
    rk = -np.nan_to_num(sc, nan=-np.inf)
    rk[np.isnan(sc)] = np.inf
    mk = rebalance_mask(idx, FREQ0).values
    W, _ = build(rk, elig, priced, np.flatnonzero(mk), N0, HOLD0, T, K, GROSS0)
    g, tn = nrun(rets, lagmat(W), np.roll(mk, LAG))
    b = blocks(g - tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)
    ref = books[(books.panel == "U56") & (books.ladder == "N") & (books.rung == N0)].iloc[0]
    d8 = max(abs(b["CAGR"] - ref.CAGR10), abs(b["Sharpe"] - ref.Sharpe10),
             abs(b["MaxDD"] - ref.MaxDD10))
    gates["G9 determinism (incumbent book rebuilt end-to-end)"] = (d8, d8 < 1e-12)

    # the resolver itself is reproducible
    res2 = [resolve(r, HEAD_SRC)[1] for _, r in cen.iterrows()]
    same = all(a == b_ for a, b_ in zip(cen.R_UNION_key, res2))
    gates["G10 the resolver is reproducible (two passes identical)"] = (0.0 if same else 1.0, same)
    # G13: this run's independent rebuild must reproduce 1098's committed killer-kind table.
    _l = books[books.pass0_full]
    _d = _l[np.isfinite(_l.cstar_full)]
    _kk = _d.killer_kind.value_counts().to_dict()
    _want = {"SHARPE": 10, "CAGR": 4, "DD": 3}
    _ok = (len(_d) == 17 and all(_kk.get(k, 0) == v for k, v in _want.items()))
    gates["G13 CROSS-RUN 1098's committed killer-kind table (17 books: SHARPE 10 / CAGR 4 / DD 3)"] = (
        float(sum(abs(_kk.get(k, 0) - v) for k, v in _want.items()) + abs(len(_d) - 17)), _ok)
    subset = bool((cen.R_UNION_G_scorable & ~cen.R_UNION_scorable).sum() == 0)
    gates["G12 the script-name guard repair is a strict SUBSET of R_UNION (removes only)"] = (
        float((cen.R_UNION_G_scorable & ~cen.R_UNION_scorable).sum()), subset)

    # ------------------------------------------------------------------------------ printing
    P("")
    P("## GATES")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}   ({v:.2e})")
    npass = sum(1 for _, (_, ok) in gates.items() if ok)
    P(f"   {npass} of {len(gates)} PASS")

    P("")
    P("## PART 3b — WHICH LEG KILLS A BOOK AS COST RISES (H_DDKILL)")
    liv = books[books.pass0_full]
    dyn = liv[np.isfinite(liv.cstar_full)]
    P(f"   books clearing all five FULL 4b legs at 0 bps: {len(liv)} of {len(books)}; "
      f"of those, {len(dyn)} die on the 0..200 bps ladder")
    kk = dyn.killer_kind.value_counts()
    for k, v in kk.items():
        P(f"     killer kind {k:<7s} {v:3d}  ({v / max(len(dyn), 1):.4f})")
    modal_kind = (kk.index[0] if len(kk) else "NONE")

    P("")
    P("## BOTH KEEP PATHS (rule 4) AND RULE 8")
    for c in RUNGS:
        sub = grid[grid.cost_rung == c]
        P(f"   @{int(c):2d} bps  4b full {int(sub.pass4b.sum()):3d} / {len(sub)}   "
          f"4b OOS {int(sub.pass4b_oos.sum()):3d} / {len(sub)}   "
          f"4a {int(sub.pass4a.sum()):3d} / {len(sub)}")
    p10 = pick_df[pick_df.cost_rung == PROTOCOL_RUNG]
    P(f"   rule 8 @10 bps: {len(p10)} IS-only picks   4b full {int(p10.pass4b.sum())}   "
      f"4b OOS {int(p10.pass4b_oos.sum())}   4a {int(p10.pass4a.sum())}")
    for r in p10.itertuples():
        P(f"     {r.panel:<5s} {r.ladder:<7s} {r.chooser:<11s} pick {str(r.pick):<6s} "
          f"full {r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}   "
          f"OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}   "
          f"4b {int(r.pass4b)}/{int(r.pass4b_oos)} 4a {int(r.pass4a)}")
    both = pick_df[(pick_df.cost_rung == PROTOCOL_RUNG) & pick_df.pass4b & pick_df.pass4b_oos]
    P(f"   rule-8 picks clearing 4b FULL AND OOS at 10 bps: {len(both)}")

    # ---------------------------------------------------------------------------- hypotheses
    hyp = []

    def H(name, stat, ok, note, kind):
        hyp.append(dict(hypothesis=name, kind=kind, statistic=stat,
                        verdict=("SUPPORTED" if ok else "REFUTED"), note=note))
        P(f"   {'SUPPORTED' if ok else 'REFUTED  '}  {name:<15s} {stat:<26s} [{kind}]  {note}")

    P("")
    P("## HYPOTHESES")
    cr = n_exists / len(cen)
    H("H_CITE", f"{cr:.4f}", cr >= 0.90,
      f"{n_exists:,} of {len(cen):,} claims cite a committed script that exists", "CALIBRATED")
    ws = int(cen[cen[HEAD_SET]].R_SCRIPT_scorable.sum())
    wp = int(cen[cen[HEAD_SET]].R_PROSE_scorable.sum())
    H("H_SCRIPTWINS", f"{ws} vs {wp}", ws > wp,
      f"R_SCRIPT alone re-scores {ws} of {len(cen):,}, R_PROSE {wp} — the queue's premise",
      "CALIBRATED")
    wu = int(cen[cen[HEAD_SET]].R_UNION_scorable.sum())
    H("H_GAIN", f"{wu} vs {wp}", wu > wp,
      f"R_UNION re-scores {wu} of {len(cen):,} against R_PROSE's {wp} "
      f"({wu / max(wp, 1):.2f}x)", "CALIBRATED")
    n28u = int(cen[cen.is28].R_UNION_scorable.sum())
    H("H_28", f"{n28u} of {C1098_N28}", n28u > C1098_N28 / 2,
      f"the queue's headline ask: {n28u} of the 28 CAGR-floor claims become re-scorable "
      f"(1098: 0)", "CALIBRATED")
    H("H_LADDERCAUSE", f"{open_pairs:,} vs {silent_pairs:,}", open_pairs > silent_pairs,
      "OPEN (the cited script walks a ladder over the axis) vs SILENT, claim-weighted over the "
      "four construction dimensions", "PRE-REGISTERED")
    mm = rescore[(rescore.resolution_source == HEAD_SRC) & (rescore.basis == "MEASURED")]
    nref = int((mm.verdict == "REFUTED").sum())
    H("H_REFUTE", f"{nref} of {len(mm)}", len(mm) > 0 and nref > len(mm) / 2,
      f"of the {len(mm)} CAGR-floor claims R_UNION makes re-scorable, {nref} are REFUTED by "
      "their own cell's measured killer leg", "PRE-REGISTERED")
    ng = int(cen[cen[HEAD_SET]].R_UNION_G_scorable.sum())
    n28g = int(cen[cen.is28].R_UNION_G_scorable.sum())
    H("H_GUARD", f"{ng} vs {wu}", ng > wp,
      f"THE REPAIR, PRICED: applying 1098's out-of-family guard to the SCRIPT NAME too leaves "
      f"{ng} of {len(cen):,} re-scorable (R_UNION {wu}, R_PROSE {wp}) and {n28g} of the 28 "
      f"(R_UNION {n28u}) — the gain survives its own correction", "POST-HOC REPAIR")
    H("H_DDKILL", f"{modal_kind}", modal_kind == "DD",
      f"modal killer kind over the {len(dyn)} books a rising rung can kill.  THE BAR WAS "
      f"MIS-SPECIFIED BY THIS RUN AND IS RECORDED REFUTED AS DECLARED, NOT RE-CUT: 1098's "
      f"'DD cap most often' is its CLAIM-side census (0.4880 of the 125 claims that name a "
      f"leg), while its TAPE-side answer was already SHARPE at 10 of 17.  The measurement "
      f"REPRODUCES that table exactly (G13), so the verdict is a defect in this run's bar and "
      f"an independent replication of 1098's finding at once", "PRE-REGISTERED")
    hypo = pd.DataFrame(hyp)

    # ------------------------------------------------------------------------------- outputs
    P("")
    P("## OUTPUTS")
    keep_cols = ["src", "line", "script", "cite_route", "script_exists", "NARROW", "PROX", "WIDE",
                 "is28", "panel", "cell_N", "cell_H", "cell_G", "cell_C", "resolved",
                 "resolved_loose", "sPANEL_state", "sN_state", "sH_state", "sGROSS_state",
                 "sCAD_state"] + \
        [f"{m}_{k}" for m in SOURCES + ["R_UNION_G"] for k in ("stated", "scorable", "cell")] + ["text"]
    dump(cen[keep_cols], "claims")
    dump(census, "census")
    dump(scripts, "scripts")
    dump(rescore, "rescore")
    dump(books, "books")
    dump(grid, "grid")
    dump(pd.DataFrame(ladrows), "ladder")
    dump(pick_df, "walkforward")
    dump(pd.DataFrame(benchrows), "benchmarks")
    dump(pd.DataFrame([dict(gate=k, value=v, passed=ok) for k, (v, ok) in gates.items()]), "gates")
    dump(hypo, "hypotheses")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"  wrote {Path(f'{OUT}.console.txt').name}")
    P(f"\n# done in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
