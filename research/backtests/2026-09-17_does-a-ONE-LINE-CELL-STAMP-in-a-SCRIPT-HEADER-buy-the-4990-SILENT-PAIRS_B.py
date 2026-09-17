#!/usr/bin/env python3
"""QUEUE idea 1167 (lane B, 2026-09-17) — does a ONE-LINE CELL STAMP in a SCRIPT HEADER buy
the 4,990 SILENT pairs?

THE QUESTION.  Idea 1149 measured that the record's scripts fail to pin a claim's cell by
SILENCE (4,990 claim-dimension pairs over the four CONSTRUCTION dimensions N/H/GROSS/CADENCE)
far more often than by LADDERING (1,472), and remarked: "a ladder run can never be pinned from
its own source, but a silent constant is one nobody wrote down."  The queue asks this run to
PRICE a one-line header stamp against the record:
  (i)   how many of the 4,990 SILENT pairs it CONVERTS,
  (ii)  how many claims move from CELL-STATED to RE-SCORABLE,
  (iii) what it costs a run that ALREADY HAS the constants.

THE MEASUREMENT, AND WHY IT IS A MEASUREMENT AND NOT A GUESS.  Nobody can know what a stamp
WOULD have said on a script whose author is gone.  What IS measurable, exactly, is whether the
value is RECOVERABLE FROM THE AUTHOR'S OWN SOURCE at a deeper reading than 1149's.  1149's
classifier reads MODULE-LEVEL ASSIGNMENTS ONLY.  A one-line header stamp is written by an author
looking at their own file, so the right ladder is reading depth into that same file:

  D0_MODULE  1149's reading, INHERITED VERBATIM (module-level assignments).  The NULL: a stamp
             that only restates what a module constant already says buys nothing by construction.
  D1_DEF     + `def f(..., N=20, ...)` parameter defaults.
  D2_ASSIGN  + ANY `NAME = value` occurrence anywhere (indented assignments, call-site kwargs).
  D3_DOC     + `NAME=value` / `NAME: value` adjacency inside the script's OWN module docstring
             and leading comment block — an author literally reading their own header.

Nested by construction (each is a strictly larger text region of the SAME file), so the ladder
is monotone and G4 checks it.  For each (script, axis) pair every depth yields PINNED (exactly
one distinct value), OPEN (two or more -> the run WALKS the axis and the stamp can only honestly
write LADDER), or ABSENT (no value at all -> the axis DOES NOT EXIST for that run and the stamp
can only honestly write NA).  A SILENT pair is CONVERTED only when it becomes PINNED.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
  DIAL 1  STAMP FORM   {D0_MODULE, D1_DEF, D2_ASSIGN, D3_DOC}
  DIAL 2  CLAIM SET    {NARROW, PROX, WIDE}          (1149's, verbatim)
= 12 cells, EVERY ONE PUBLISHED in `.census.csv`, each with its own 28-claim sub-population.
NOT dials, all reported at every value: the five dimensions; PANEL {U56, B136}; LADDER
{N, H, GROSS, CADENCE} at 1082/1086/1094/1097/1110's rung lists (9+4+10+4 = 27 rungs per panel,
54 books); the eight 4b legs; the four cost rungs {0, 10, 25, 50}; the three rule-8 choosers.

PRE-REGISTERED HYPOTHESES — written before the census arm was run, and none of them is a
measurement dressed up as a forecast.  (1149 flagged four of its own as CALIBRATED because its
census had been run in a prototype first; this run's census arm had NOT been run when this
docstring was written, and `.hypotheses.csv` records every one as PRE-REGISTERED.)
  H_ABSENT    a MAJORITY (> 0.50) of the 4,990 SILENT pairs are STILL ABSENT at the DEEPEST
              reading D3_DOC — i.e. the axis does not exist in that run at all and NO stamp
              converts them.  This is the queue's own framing ("a constant nobody wrote down")
              put at risk.
  H_CONVERT   the stamp CONVERTS at least 1,000 of the 4,990 at D2_ASSIGN.
  H_RESCORE   R_STAMP at D2_ASSIGN re-scores STRICTLY MORE than 1149's committed R_UNION (291).
  H_28        the stamp takes the 28 CAGR-floor claims ABOVE R_UNION's 9.
  H_DEFAULT   a MAJORITY of R_UNION's committed 291 re-scorable claims are DEFAULT-REACHED (at
              least one construction dimension supplied by the frozen default N0/HOLD0/GROSS0/
              FREQ0 rather than by prose or script) rather than PINNED-REACHED.  1149 published
              291 without this split; if the majority are default-reached, the "3.55x gain" is
              substantially the DEFAULTS talking and the stamp's job is different from the one
              the queue states.
  H_NOTAPPLICABLE  ABSENT-at-D3 concentrates in scripts that RUN NO BOOK AT ALL (census/corpus
              scripts): the ABSENT share among CENSUS_ONLY scripts exceeds that among
              RUNS_A_BOOK scripts by more than 0.20.  This is the run's OWN GUARD on its OWN
              headline: if instead ABSENT is high among scripts that DO run books, the limit is
              this run's DIMENSION NAME SET and not the record, and the headline is void.
  H_FREE      for at least 0.95 of the pairs 1149 classed PINNED at module level, the deepest
              reading returns the SAME single value — i.e. for a run that already has the
              constants the stamp is TRANSCRIPTION, not derivation, and costs no decision.

WHAT THIS RUN DOES NOT DO.  It proposes a PROTOCOL clause and does not enact it (rule 6).  It
modifies no RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py or engine.py.  SURVIVORSHIP:
universe.json / universe_broad.json are current constituents; inherited, not repaired here.

Standalone:  python3 research/backtests/2026-09-17_does-a-ONE-LINE-CELL-STAMP-in-a-SCRIPT-HEADER-buy-the-4990-SILENT-PAIRS_B.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                       # noqa: E402
from engine import backtest, rebalance_mask                                # noqa: E402

BT = ROOT / "research" / "backtests"
OUT = BT / Path(__file__).stem

# ---- the parent run (1149) and its committed, machine-readable population
P1149 = BT / ("2026-09-17_can-the-RECORD-s-COST-CLAIMS-be-RESOLVED-from-their-SCRIPTS-"
              "rather-than-their-PROSE_C")
C1149_SILENT, C1149_OPEN = 4990, 1472          # the four construction dims, claim-weighted
C1149_UNION, C1149_PROSE, C1149_LOOSE = 291, 82, 425
C1149_N28, C1149_28_UNION = 28, 9
C1149_WIDE, C1149_PROX, C1149_NARROW = 2088, 125, 59
C1149_SCRIPTS = 561

# ---- mechanics frozen at 936/1064/1071/1082/1086/1094/1097/1098/1149's construction
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
RUNGS = [0.0, 10.0, 25.0, 50.0]
PROTOCOL_RUNG = 10.0
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR"]

DEPTHS = ["D0_MODULE", "D1_DEF", "D2_ASSIGN", "D3_DOC"]        # DIAL 1
CLAIM_SETS = ["NARROW", "PROX", "WIDE"]                        # DIAL 2
HEAD_DEPTH, HEAD_SET = "D2_ASSIGN", "WIDE"
DIMS4 = ["N", "H", "GROSS", "CAD"]                             # the CONSTRUCTION dimensions

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ============================================================ PRICE MECHANICS
# 1094/1097/1098/1149's, verbatim.  Copied rather than imported because 1149's script is a
# result file, not a library; G9/G11/G12 check this copy against its committed output.
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
    """Each 4b leg's margin IN ITS OWN UNITS (1097/1098/1149's, verbatim); >= 0 passes."""
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


def ann_turn(tn, mask):
    n = int(mask.sum())
    return float(tn[mask].sum() / (n / 252.0)) if n else np.nan


# ============================================================ THE RESOLUTION LAYER
# 1098's out-of-family guard, INHERITED VERBATIM through 1149.
OUT_OF_FAMILY = re.compile(
    r"ensemble|sleeve|overlay|tranche|\bband\b|trim|\bnull\b|coin[- ]flip|random key|QQQ|"
    r"spinoff|putwrite|option|deep ?value|MA-RS|scramble|shuffl|phase|rotat|"
    r"diversifier|equal[- ]weight control|BAND03|EWELIG|vol[- ]scal|min[- ]hold", re.I)

# 1149's dimension name sets, INHERITED VERBATIM.  Declared here and nowhere else; NOT a dial,
# and deliberately NOT extended by this run — extending them would confound the DEPTH ladder
# with an ALIAS ladder, and H_NOTAPPLICABLE is the guard that tells us whether they are enough.
DIM_NAMES = {
    "N":     r"(?:N0|NN|N|TOPN|TOP_N|NSEL|LAD_N|N_LAD|LADDER_N|N_GRID|NS|N_LIST|N_RUNGS)",
    "H":     r"(?:H0|HOLD0|HOLD|MINHOLD|MIN_HOLD|H|LAD_H|H_LAD|LADDER_H|H_GRID|HS|H_LIST|HOLDS)",
    "GROSS": r"(?:GROSS0|G0|GROSS|LAD_G|G_LAD|LADDER_G|GROSSES|G_GRID|GS|GROSS_LAD)",
    "CAD":   r"(?:FREQ0|FREQ|CADENCE|CAD|LAD_C|C_LAD|LADDER_C|FREQS|CADENCES|CAD_LAD)",
}
DIM_RX = {k: re.compile(r"^" + v + r"$", re.I) for k, v in DIM_NAMES.items()}
# the same alphabet as an inline `NAME = ...` / `NAME: ...` matcher, for D1/D2/D3
DIM_INLINE = {k: re.compile(r"(?<![\w.])" + v + r"\s*=\s*([^,)\]\n#]+)", re.I)
              for k, v in DIM_NAMES.items()}
DIM_DOC = {k: re.compile(r"(?<![\w.])" + v + r"\s*[=:]\s*([^\s,;)\]]+)", re.I)
           for k, v in DIM_NAMES.items()}
RUNS_A_BOOK = re.compile(r"\bnrun\s*\(|\bbacktest\s*\(|rules_v[12]_weights|\bbuild\s*\(")


def split_top(s, sep=","):
    """Split on SEP at bracket depth zero (1149's, verbatim)."""
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


def assignments(src, indented=False):
    """1149's module-level assignment walker, verbatim; `indented=True` yields the INDENTED
    assignments it deliberately skipped (D2's extra text region)."""
    for line in src.split("\n"):
        if not line:
            continue
        ind = line[0] in " \t"
        if line.lstrip().startswith("#"):
            continue
        if ind != indented:
            continue
        line = line.strip() if indented else line
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


def _vals_from_rhs(dim, rhs):
    """1149's literal extractor, verbatim."""
    if dim == "CAD":
        return set(re.findall(r"['\"]([DWMQ])['\"]", rhs))
    if re.search(r"[a-zA-Z_]\w*\s*\(", rhs) and not rhs.startswith("["):
        return set()                     # a computed RHS is not a stated constant
    return set(re.findall(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])", rhs))


def dim_values_module(src, dim):
    """D0: exactly 1149's `dim_values` — module-level assignment constants."""
    vals: set[str] = set()
    for name, rhs in assignments(src):
        if DIM_RX[dim].match(name):
            vals |= _vals_from_rhs(dim, rhs)
    return vals


DEF_RX = re.compile(r"^\s*def\s+\w+\s*\(([^)]*)\)", re.M | re.S)


def dim_values_defaults(src, dim):
    """D1's extra region: `def f(..., NAME=literal, ...)` parameter defaults."""
    vals: set[str] = set()
    for sig in DEF_RX.findall(src):
        for part in split_top(sig):
            if "=" not in part:
                continue
            nm, _, rhs = part.partition("=")
            nm = nm.split(":")[0].strip()
            if DIM_RX[dim].match(nm):
                vals |= _vals_from_rhs(dim, rhs.strip())
    return vals


def dim_values_inline(src, dim):
    """D2's extra region: ANY `NAME = value` occurrence — indented assignments and call-site
    keyword arguments alike.  Comment lines are excluded (they are D3's region)."""
    vals: set[str] = set()
    for name, rhs in assignments(src, indented=True):
        if DIM_RX[dim].match(name):
            vals |= _vals_from_rhs(dim, rhs)
    code = "\n".join(l for l in src.split("\n") if not l.lstrip().startswith("#"))
    code = re.sub(r'"""[\s\S]*?"""', "", code)
    for rhs in DIM_INLINE[dim].findall(code):
        vals |= _vals_from_rhs(dim, rhs.strip())
    return vals


def header_text(src):
    """The script's OWN module docstring plus its leading comment block — the text an author
    writing a one-line header stamp is literally looking at."""
    m = re.search(r'^\s*(?:#!.*\n)?(?:#.*\n)*\s*(?:r?"""([\s\S]*?)""")', src)
    doc = m.group(1) if m else ""
    lead = []
    for line in src.split("\n"):
        s = line.strip()
        if s.startswith("#"):
            lead.append(s)
        elif s and not s.startswith(('"""', "'''", "from ", "import ")):
            break
    return doc + "\n" + "\n".join(lead)


def dim_values_doc(src, dim):
    """D3's extra region: `NAME=value` / `NAME: value` adjacency inside the header text only.
    Bare numbers in prose are NOT harvested — only an explicit name-value adjacency."""
    vals: set[str] = set()
    for rhs in DIM_DOC[dim].findall(header_text(src)):
        vals |= _vals_from_rhs(dim, rhs.strip())
    return vals


def panel_values(src):
    """1149's, verbatim.  NOT depth-laddered: it already scans the whole source, so the panel
    axis reads identically at every depth.  Stated, not hidden: the depth ladder can only move
    the four CONSTRUCTION dimensions, which is exactly the 4,990 the queue asks about."""
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


def script_facts_all_depths(path: Path):
    """-> {depth: {dim: sorted values}} plus the script's own metadata."""
    src = path.read_text(errors="replace")
    pv = sorted(panel_values(src))
    reg = {d: {} for d in DEPTHS}
    for dim in DIMS4:
        v0 = dim_values_module(src, dim)
        v1 = v0 | dim_values_defaults(src, dim)
        v2 = v1 | dim_values_inline(src, dim)
        v3 = v2 | dim_values_doc(src, dim)
        for d, v in zip(DEPTHS, (v0, v1, v2, v3)):
            reg[d][dim] = sorted(v)
    for d in DEPTHS:
        reg[d]["PANEL"] = pv
    return reg, dict(bytes=len(src), runs_a_book=bool(RUNS_A_BOOK.search(src)))


def state_of(vals):
    return "PINNED" if len(vals) == 1 else ("OPEN" if len(vals) > 1 else "SILENT")


def one_of(vals, cast):
    if len(vals) != 1:
        return None
    try:
        return cast(vals[0])
    except (TypeError, ValueError):
        return None


def cell_of(pan, N, H, G, C, book_keys):
    """1098/1149's `resolve_cell`, verbatim: a (panel, N, H, gross, cadence) tuple resolves to a
    measured book iff it is one of the 54 one-factor-at-a-time rungs."""
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


def main():
    gates: dict[str, tuple[float, bool]] = {}
    hyp: list[dict] = []

    P("=" * 100)
    P("QUEUE idea 1167 (lane B, 2026-09-17) — does a ONE-LINE CELL STAMP in a SCRIPT HEADER")
    P("buy the 4,990 SILENT pairs?")
    P("=" * 100)
    P("DIAL 1 STAMP FORM (reading depth into the author's own file)  " + " ".join(DEPTHS))
    P("DIAL 2 CLAIM SET  " + " ".join(CLAIM_SETS) + "   -> 12 cells, all published")
    P("")

    # ---------------------------------------------------------- PART 1: the population
    P("## PART 1 — THE POPULATION IS 1149's COMMITTED FILE, READ VERBATIM")
    cen = pd.read_csv(f"{P1149}.claims.csv")
    s1149 = pd.read_csv(f"{P1149}.scripts.csv")
    gates["G0a population 2,088 / 125 / 59 claims (WIDE/PROX/NARROW)"] = (
        float(abs(len(cen) - C1149_WIDE) + abs(int(cen.PROX.sum()) - C1149_PROX)
              + abs(int(cen.NARROW.sum()) - C1149_NARROW)),
        len(cen) == C1149_WIDE and int(cen.PROX.sum()) == C1149_PROX
        and int(cen.NARROW.sum()) == C1149_NARROW)
    gates["G0b 1149's committed R_PROSE(82) / R_UNION(291) / R_LOOSE(425) / 28 carried"] = (
        float(abs(int(cen.R_PROSE_scorable.sum()) - C1149_PROSE)
              + abs(int(cen.R_UNION_scorable.sum()) - C1149_UNION)
              + abs(int(cen.R_LOOSE_scorable.sum()) - C1149_LOOSE)
              + abs(int(cen.is28.sum()) - C1149_N28)),
        int(cen.R_PROSE_scorable.sum()) == C1149_PROSE
        and int(cen.R_UNION_scorable.sum()) == C1149_UNION
        and int(cen.R_LOOSE_scorable.sum()) == C1149_LOOSE
        and int(cen.is28.sum()) == C1149_N28)
    P(f"   {len(cen):,} claims; {int(cen.script_exists.sum()):,} cite a script that exists; "
      f"{int(cen.is28.sum())} CAGR-floor claims.")

    # the 561 scripts, and whether the corpus drifted under 1149's feet
    drift, missing, facts, meta = 0, 0, {}, {}
    for r in s1149.itertuples():
        p = BT / r.script
        if not p.exists():
            missing += 1
            continue
        reg, md = script_facts_all_depths(p)
        if md["bytes"] != r.bytes:
            drift += 1
        facts[r.script] = reg
        meta[r.script] = md
    gates[f"G1 all {C1149_SCRIPTS} scripts 1149 scanned are on disk BYTE-IDENTICAL "
          f"(missing {missing}, drift {drift})"] = (float(missing + drift),
                                                    missing == 0 and drift == 0)
    P(f"   {len(s1149):,} scripts; missing {missing}; byte-drift vs 1149's scan {drift}. "
      f"The script corpus is APPEND-ONLY, unlike data/prices.csv (idea 1163).")

    # G2: D0 must reproduce 1149's committed per-script states EXACTLY
    bad = 0
    for r in s1149.itertuples():
        if r.script not in facts:
            continue
        for dim, col in (("N", r.N_state), ("H", r.H_state), ("GROSS", r.GROSS_state),
                         ("CAD", r.CAD_state), ("PANEL", r.PANEL_state)):
            if state_of(facts[r.script]["D0_MODULE"][dim]) != col:
                bad += 1
    gates[f"G2 D0_MODULE reproduces 1149's committed script states on all "
          f"{len(s1149) * 5:,} (script, dim) pairs"] = (float(bad), bad == 0)

    # ---------------------------------------------------------- PART 2: the 4,990, at depth
    P("")
    P("## PART 2 — THE 4,990 SILENT PAIRS, RE-READ AT FOUR DEPTHS INTO THE SAME FILE")
    sil_cols = {"N": "sN_state", "H": "sH_state", "GROSS": "sGROSS_state", "CAD": "sCAD_state",
                "PANEL": "sPANEL_state"}
    pairrows = []
    for _, r in cen.iterrows():
        f = facts.get(r["script"]) if r["script_exists"] else None
        for dim in DIMS4:
            st0 = r[sil_cols[dim]]
            row = dict(src=r["src"], line=r["line"], script=r["script"], dim=dim,
                       state_1149=st0, is28=bool(r["is28"]),
                       NARROW=bool(r["NARROW"]), PROX=bool(r["PROX"]), WIDE=bool(r["WIDE"]),
                       runs_a_book=bool(meta.get(r["script"], {}).get("runs_a_book", False)))
            for d in DEPTHS:
                row[d] = state_of(f[d][dim]) if f else "SILENT"
            pairrows.append(row)
    pairs = pd.DataFrame(pairrows)
    o1149 = int((pairs.state_1149 == "OPEN").sum())
    s1149n = int((pairs.state_1149 == "SILENT").sum())
    gates[f"G3 1149's claim-weighted SILENT/OPEN over the 4 construction dims "
          f"({s1149n:,}/{o1149:,}) reproduced"] = (
        float(abs(s1149n - C1149_SILENT) + abs(o1149 - C1149_OPEN)),
        s1149n == C1149_SILENT and o1149 == C1149_OPEN)
    P(f"   SILENT {s1149n:,} vs OPEN {o1149:,} — 1149's committed {C1149_SILENT:,} / "
      f"{C1149_OPEN:,} reproduced from its own claims file.")

    # depth monotonicity
    order = {"SILENT": 0, "OPEN": 1, "PINNED": 1}
    nonmono = 0
    for a, b in zip(DEPTHS, DEPTHS[1:]):
        nonmono += int((pairs[a].map(order) > pairs[b].map(order)).sum())
    gates["G4 depth ladder is MONOTONE (a pair never loses a value going deeper)"] = (
        float(nonmono), nonmono == 0)

    sil = pairs[pairs.state_1149 == "SILENT"]
    P("")
    P("   THE HEADLINE TABLE — what a one-line header stamp does to the 4,990 SILENT pairs")
    P("   CONVERTED = becomes PINNED (the stamp writes a value, and the pair is bought)")
    P("   DECLARED-OPEN = becomes OPEN (the stamp can only honestly write LADDER: NOT bought)")
    P("   STILL ABSENT = no value at any reading (the stamp writes NA: the axis does not exist)")
    P("")
    P(f"   {'depth':<12s} {'CONVERTED':>10s} {'share':>8s} {'DECL-OPEN':>10s} "
      f"{'STILL ABSENT':>13s} {'share':>8s}")
    convrows = []
    for d in DEPTHS:
        conv = int((sil[d] == "PINNED").sum())
        opn = int((sil[d] == "OPEN").sum())
        ab = int((sil[d] == "SILENT").sum())
        P(f"   {d:<12s} {conv:10,d} {conv / len(sil):8.4f} {opn:10,d} {ab:13,d} "
          f"{ab / len(sil):8.4f}")
        convrows.append(dict(depth=d, n_silent=len(sil), converted=conv,
                             share_converted=conv / len(sil), declared_open=opn,
                             still_absent=ab, share_absent=ab / len(sil)))
    # per-dimension detail at every depth (not a dial: reported at every value)
    for d in DEPTHS:
        for dim in DIMS4:
            s = sil[sil.dim == dim]
            convrows.append(dict(depth=d, dim=dim, n_silent=len(s),
                                 converted=int((s[d] == "PINNED").sum()),
                                 declared_open=int((s[d] == "OPEN").sum()),
                                 still_absent=int((s[d] == "SILENT").sum()),
                                 share_converted=float((s[d] == "PINNED").mean()),
                                 share_absent=float((s[d] == "SILENT").mean())))
    conv_df = pd.DataFrame(convrows)
    dump(conv_df, "conversion")

    P("")
    P("   per-dimension at the deepest reading D3_DOC:")
    for dim in DIMS4:
        s = sil[sil.dim == dim]
        if not len(s):
            continue
        P(f"     {dim:<6s} SILENT {len(s):5,d} -> CONVERTED {int((s.D3_DOC == 'PINNED').sum()):5,d}"
          f"   DECL-OPEN {int((s.D3_DOC == 'OPEN').sum()):5,d}"
          f"   STILL ABSENT {int((s.D3_DOC == 'SILENT').sum()):5,d}")

    # ---- H_NOTAPPLICABLE: the run's guard on its own headline
    ab_book = float((sil[sil.runs_a_book].D3_DOC == "SILENT").mean()) if sil.runs_a_book.any() \
        else np.nan
    ab_cens = float((sil[~sil.runs_a_book].D3_DOC == "SILENT").mean()) \
        if (~sil.runs_a_book).any() else np.nan
    P("")
    P(f"   H_NOTAPPLICABLE probe — STILL-ABSENT share at D3_DOC, split by whether the cited")
    P(f"   script RUNS A BOOK at all:  RUNS_A_BOOK {ab_cens if False else ab_book:.4f} "
      f"(n={int(sil.runs_a_book.sum()):,})   CENSUS_ONLY {ab_cens:.4f} "
      f"(n={int((~sil.runs_a_book).sum()):,})")

    # ---------------------------------------------------------- PART 3: the price leg
    P("")
    P("## PART 3 — THE PRICE LEG: 54 books rebuilt from prices at 4 cost rungs")
    bookrows, gridrows, benchrows = [], [], []
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
        P(f"   {panel}: {K} cols, {T} days {idx[0].date()}..{idx[-1].date()}")
        P(f"     SPY  full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%}")

        live = {}
        for freq in sorted({FREQ0} | set(LAD_C)):
            r0 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=freq)
            live[freq] = (r0["returns"].values, r0["turnover"].values)
        lg, lt = live[FREQ0]
        lb0 = {c: blocks(lg - lt * c / 1e4, warm, ins, oos) for c in RUNGS}
        benchrows.append(dict(panel=panel, series=f"RULESv2@{int(PROTOCOL_RUNG)}bps",
                              **lb0[PROTOCOL_RUNG]))
        b10 = lb0[PROTOCOL_RUNG]
        P(f"     RULES v2 @10 bps  full {b10['CAGR']:.2%} / {b10['Sharpe']:.4f} / "
          f"{b10['MaxDD']:.2%}  halves {b10['H1']:.4f}/{b10['H2']:.4f}  "
          f"OOS {b10['OOS_CAGR']:.2%} / {b10['OOS_Sharpe']:.4f} / {b10['OOS_MaxDD']:.2%}")

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

                if panel == "U56" and lad == "N" and rung == N0:
                    wdf = pd.DataFrame(W, index=idx, columns=px.columns)
                    for cg, nm in ((0.0, "G10a"), (10.0, "G10b")):
                        eng = backtest(px, wdf, cost_bps=cg, freq=C)["returns"].values
                        d = float(np.abs((g - tn * cg / 1e4)[WARMUP:] - eng[WARMUP:]).max())
                        gates[f"{nm} r(c)=g-tn*c/1e4 == engine.backtest @{cg:.0f} bps"] = (
                            d, d < 1e-12)

                b_by = {c: blocks(g - tn * c / 1e4, warm, ins, oos) for c in RUNGS}
                lgc, ltc = live[C]
                lbc = {c: blocks(lgc - ltc * c / 1e4, warm, ins, oos) for c in RUNGS}
                row = dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=G, cadence=C,
                           mean_nsel=float(nsel.mean()), turnover=turn)
                for c in RUNGS:
                    b = b_by[c]
                    mm = margins(b, sb)
                    l4a = legs_4a(b, lbc[c])
                    p4b = all(mm[L] >= 0 for L in FULL_LEGS)
                    p4bo = all(mm[L] >= 0 for L in OOS_LEGS)
                    ic = int(c)
                    row.update({f"CAGR{ic}": b["CAGR"], f"Sharpe{ic}": b["Sharpe"],
                                f"MaxDD{ic}": b["MaxDD"], f"H1_{ic}": b["H1"],
                                f"H2_{ic}": b["H2"], f"OOS_CAGR{ic}": b["OOS_CAGR"],
                                f"OOS_Sharpe{ic}": b["OOS_Sharpe"],
                                f"OOS_MaxDD{ic}": b["OOS_MaxDD"], f"pass4b{ic}": p4b,
                                f"pass4bOOS{ic}": p4bo, f"pass4a{ic}": all(l4a.values()),
                                f"bind{ic}": min(mm, key=lambda L: mm[L])})
                    gridrows.append(dict(panel=panel, ladder=lad, rung=rung, cost_rung=c,
                                         pass4b=p4b, pass4b_oos=p4bo, pass4a=all(l4a.values()),
                                         CAGR=b["CAGR"], Sharpe=b["Sharpe"], MaxDD=b["MaxDD"],
                                         H1=b["H1"], H2=b["H2"], OOS_CAGR=b["OOS_CAGR"],
                                         OOS_Sharpe=b["OOS_Sharpe"], OOS_MaxDD=b["OOS_MaxDD"],
                                         turnover=turn, **l4a,
                                         **{f"m_{L}": mm[L] for L in FULL_LEGS + OOS_LEGS}))
                bookrows.append(row)
                book_keys[panel].append((lad, rung))
                store[(panel, lad, rung)] = dict(
                    IS_S={c: b_by[c]["IS_Sharpe"] for c in RUNGS},
                    IS_DD={c: b_by[c]["IS_MaxDD"] for c in RUNGS},
                    IS_CAGR={c: b_by[c]["IS_CAGR"] for c in RUNGS},
                    OOS={c: (b_by[c]["OOS_CAGR"], b_by[c]["OOS_Sharpe"], b_by[c]["OOS_MaxDD"])
                         for c in RUNGS},
                    FULL={c: (b_by[c]["CAGR"], b_by[c]["Sharpe"], b_by[c]["MaxDD"],
                              b_by[c]["H1"], b_by[c]["H2"]) for c in RUNGS},
                    p4b={c: all(margins(b_by[c], sb)[L] >= 0 for L in FULL_LEGS) for c in RUNGS},
                    p4bo={c: all(margins(b_by[c], sb)[L] >= 0 for L in OOS_LEGS) for c in RUNGS},
                    p4a={c: all(legs_4a(b_by[c], lbc[c]).values()) for c in RUNGS},
                    turn=turn)

    books = pd.DataFrame(bookrows)
    grid = pd.DataFrame(gridrows)
    dump(books, "books")
    dump(grid, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")

    # G9: this run's independent rebuild vs 1149's committed books.csv at 10 bps
    b49 = pd.read_csv(f"{P1149}.books.csv")
    mg = books.merge(b49, on=["panel", "ladder", "rung"], suffixes=("", "_49"))
    d9 = float(np.nanmax(np.abs(np.c_[mg.CAGR10 - mg.CAGR10_49, mg.Sharpe10 - mg.Sharpe10_49,
                                      mg.MaxDD10 - mg.MaxDD10_49])))
    gates[f"G9 CROSS-RUN 1149's committed 54 books @10 bps (HEAD tape; prices.csv is rewritten "
          f"nightly — idea 1163)"] = (d9, d9 < 5e-3)
    vflip = int((mg.pass4b10 != mg.pass4b10_49).sum() + (mg.pass4a10 != mg.pass4a10_49).sum())
    gates["G9b ... and NO 4a/4b VERDICT moves under that drift"] = (float(vflip), vflip == 0)
    P(f"   replay of 1149's 54 books @10 bps: max |delta| {d9:.3e} over CAGR/Sharpe/MaxDD, "
      f"{vflip} verdict flips.")

    # ---------------------------------------------------------- PART 4: the 12 cells
    P("")
    P("## PART 4 — THE 12 CELLS (STAMP FORM x CLAIM SET), AND THE DEFAULT-REACHED SPLIT")

    def resolve(row, depth):
        """R_STAMP(depth): 1149's R_UNION with the SCRIPT side read at `depth`.  At D0_MODULE it
        IS R_UNION, which G5 checks.  Returns (stated, cell, n_from_default)."""
        f = facts.get(row["script"]) if row["script_exists"] else None
        fd = f[depth] if f else None
        pP = row["panel"] if row["panel"] in PANELS else ""
        pN = int(row["cell_N"]) if np.isfinite(row["cell_N"]) else None
        pH = int(row["cell_H"]) if np.isfinite(row["cell_H"]) else None
        pG = float(row["cell_G"]) if np.isfinite(row["cell_G"]) else None
        pC = row["cell_C"] if isinstance(row["cell_C"], str) and row["cell_C"] else None
        sP = (fd["PANEL"][0] if fd and len(fd["PANEL"]) == 1 else "")
        sN = one_of(fd["N"], int) if fd else None
        sH = one_of(fd["H"], int) if fd else None
        sG = one_of(fd["GROSS"], float) if fd else None
        sC = (fd["CAD"][0] if fd and len(fd["CAD"]) == 1 else None)
        Pn = pP or sP
        N = pN if pN is not None else sN
        H = pH if pH is not None else sH
        G = pG if pG is not None else sG
        C = pC or sC
        ndim = sum(x is not None for x in (N, H, G, C))
        infam = not OUT_OF_FAMILY.search(str(row["text"]))
        stated = bool(Pn in PANELS and ndim >= 1 and infam)
        cell = (cell_of(Pn, N if N is not None else N0, H if H is not None else HOLD0,
                        G if G is not None else GROSS0, C or FREQ0, book_keys)
                if Pn in PANELS else None)
        return stated, cell, 4 - ndim

    for d in DEPTHS:
        res = [resolve(r, d) for _, r in cen.iterrows()]
        cen[f"{d}_stated"] = [x[0] for x in res]
        cen[f"{d}_key"] = [x[1] for x in res]
        cen[f"{d}_cell"] = [f"{x[1][0]}/{x[1][1]}={x[1][2]}" if x[1] else "" for x in res]
        cen[f"{d}_scorable"] = [bool(x[0] and x[1] is not None) for x in res]
        cen[f"{d}_ndefault"] = [x[2] for x in res]

    nd0 = int((cen.D0_MODULE_scorable != cen.R_UNION_scorable.astype(bool)).sum())
    gates["G5 R_STAMP at D0_MODULE reproduces 1149's committed R_UNION on all 2,088 rows"] = (
        float(nd0), nd0 == 0)

    # H_DEFAULT: how much of 1149's committed 291 is reached only by the frozen defaults
    u = cen[cen.R_UNION_scorable]
    n_pin = int((u.D0_MODULE_ndefault == 0).sum())
    n_def = int((u.D0_MODULE_ndefault > 0).sum())
    P(f"   1149's committed {len(u)} re-scorable claims: PINNED-REACHED {n_pin} "
      f"({n_pin / len(u):.4f})  DEFAULT-REACHED {n_def} ({n_def / len(u):.4f}) — a")
    P(f"   DEFAULT-REACHED claim reaches its cell only because the unstated dimensions were")
    P(f"   FILLED with the frozen defaults N={N0}/H={HOLD0}/gross={GROSS0}/cadence={FREQ0}.")

    cenrows = []
    for d in DEPTHS:
        for cs in CLAIM_SETS:
            sub = cen[cen[cs]]
            s28 = sub[sub.is28]
            sc_ = sub[f"{d}_scorable"]
            cenrows.append(dict(
                stamp_form=d, claim_set=cs, n_claims=len(sub),
                n_cell_stated=int(sub[f"{d}_stated"].sum()),
                n_rescorable=int(sc_.sum()),
                share_cell_stated=float(sub[f"{d}_stated"].mean()) if len(sub) else np.nan,
                share_rescorable=float(sc_.mean()) if len(sub) else np.nan,
                n_rescorable_pinned=int((sc_ & (sub[f"{d}_ndefault"] == 0)).sum()),
                n_rescorable_default=int((sc_ & (sub[f"{d}_ndefault"] > 0)).sum()),
                n28=len(s28), n28_cell_stated=int(s28[f"{d}_stated"].sum()),
                n28_rescorable=int(s28[f"{d}_scorable"].sum()),
                n28_rescorable_pinned=int((s28[f"{d}_scorable"]
                                           & (s28[f"{d}_ndefault"] == 0)).sum())))
    census = pd.DataFrame(cenrows)
    dump(census, "census")
    P("")
    P(f"   {'stamp form':<12s} {'set':<7s} {'claims':>7s} {'STATED':>7s} {'RESCORABLE':>11s} "
      f"{'share':>7s} | {'of which PINNED':>15s} {'DEFAULT':>8s} | {'28:RESC':>8s} {'PIN':>4s}")
    for r in census.itertuples():
        P(f"   {r.stamp_form:<12s} {r.claim_set:<7s} {r.n_claims:7,d} {r.n_cell_stated:7,d} "
          f"{r.n_rescorable:11,d} {r.share_rescorable:7.4f} | {r.n_rescorable_pinned:15,d} "
          f"{r.n_rescorable_default:8,d} | {r.n28_rescorable:8d} {r.n28_rescorable_pinned:4d}")

    # ---------------------------------------------------------- PART 5: the cost of the stamp
    P("")
    P("## PART 5 — WHAT THE STAMP COSTS A RUN THAT ALREADY HAS THE CONSTANTS")
    same, tot, moved = 0, 0, []
    for scr, reg in facts.items():
        for dim in DIMS4:
            v0 = reg["D0_MODULE"][dim]
            if len(v0) != 1:
                continue
            tot += 1
            v3 = reg["D3_DOC"][dim]
            if len(v3) == 1 and v3[0] == v0[0]:
                same += 1
            else:
                moved.append(dict(script=scr, dim=dim, module=v0[0], deepest=";".join(v3)))
    share_free = same / tot if tot else np.nan
    gates["G6 H_FREE basis: module-PINNED (script,dim) pairs exist to measure"] = (
        float(tot), tot > 0)
    P(f"   of {tot:,} (script, dim) pairs 1149 classed PINNED at module level, the DEEPEST")
    P(f"   reading returns the SAME single value for {same:,} ({share_free:.4f}) — for those the")
    P(f"   stamp is TRANSCRIPTION and costs NO decision.  The other {tot - same:,} turn OPEN at")
    P(f"   depth: the module constant is not the only value in the file, so the author must")
    P(f"   CHOOSE, which is the stamp's real price.  All of them are published in .cost.csv.")
    dump(pd.DataFrame(moved) if moved else
         pd.DataFrame(columns=["script", "dim", "module", "deepest"]), "cost")

    # fields an author must think about, per script
    fieldrows = []
    for scr, reg in facts.items():
        for d in DEPTHS:
            n_val = sum(len(reg[d][dim]) == 1 for dim in DIMS4)
            n_lad = sum(len(reg[d][dim]) > 1 for dim in DIMS4)
            n_na = sum(len(reg[d][dim]) == 0 for dim in DIMS4)
            fieldrows.append(dict(script=scr, stamp_form=d, fields_VALUE=n_val,
                                  fields_LADDER=n_lad, fields_NA=n_na,
                                  runs_a_book=meta[scr]["runs_a_book"]))
    fields = pd.DataFrame(fieldrows)
    dump(fields, "fields")
    P("")
    P(f"   {'stamp form':<12s} {'mean VALUE':>11s} {'mean LADDER':>12s} {'mean NA':>8s}  "
      f"(per script, out of 4 construction fields)")
    for d in DEPTHS:
        s = fields[fields.stamp_form == d]
        P(f"   {d:<12s} {s.fields_VALUE.mean():11.3f} {s.fields_LADDER.mean():12.3f} "
          f"{s.fields_NA.mean():8.3f}")

    # ---------------------------------------------------------- PART 6: rule 8 + KEEP paths
    P("")
    P("## PART 6 — PROTOCOL RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    picks = []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            for c in RUNGS:
                for ch in CHOOSERS:
                    key = {"C_ISSHARPE": "IS_S", "C_ISDD": "IS_DD", "C_ISCAGR": "IS_CAGR"}[ch]
                    vals = {rg: store[(panel, lad, rg)][key][c] for rg in rungs}
                    pick = max(vals, key=lambda k: vals[k])
                    st = store[(panel, lad, pick)]
                    oc, os_, od = st["OOS"][c]
                    fc, fs, fd_, f1, f2 = st["FULL"][c]
                    picks.append(dict(panel=panel, ladder=lad, cost_rung=c, chooser=ch,
                                      pick=pick, IS_stat=vals[pick], turnover=st["turn"],
                                      CAGR=fc, Sharpe=fs, MaxDD=fd_, H1=f1, H2=f2,
                                      OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                                      pass4b=st["p4b"][c], pass4b_oos=st["p4bo"][c],
                                      pass4a=st["p4a"][c]))
    pick_df = pd.DataFrame(picks)
    dump(pick_df, "walkforward")
    p10 = pick_df[pick_df.cost_rung == PROTOCOL_RUNG]
    n4b = int((p10.pass4b & p10.pass4b_oos).sum())
    n4a = int(p10.pass4a.sum())
    P(f"   96 rule-8 picks published (2 panels x 4 ladders x 4 cost rungs x 3 IS-only choosers;")
    P(f"   every chooser reads 2009..{IS_END} ONLY and is evaluated on 2017-2026 untouched).")
    P(f"   At PROTOCOL's 10 bps: 4b full+OOS {n4b} of {len(p10)}   4a {n4a} of {len(p10)}")

    # ---- THE NOMINATED BOOK: does the stamp move it?
    P("")
    P("   THE NOMINATED BOOK — the cell most cited by the claims each reading makes")
    P("   re-scorable.  This is the only channel by which a STAMP can move a book, and it is")
    P("   the one the record's sibling runs report.  Ties are published, never broken silently.")
    nomrows = []
    for d in DEPTHS:
        for cs in CLAIM_SETS:
            sub = cen[cen[cs] & cen[f"{d}_scorable"]]
            if not len(sub):
                nomrows.append(dict(stamp_form=d, claim_set=cs, n=0, nominated="",
                                    tie=False, **{k: np.nan for k in
                                                  ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                   "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                                    pass4b=False, pass4b_oos=False, pass4a=False))
                continue
            vc = sub[f"{d}_cell"].value_counts()
            top = vc.index[0]
            tie = bool(len(vc) > 1 and vc.iloc[1] == vc.iloc[0])
            pan, rest = top.split("/")
            lad, rg = rest.split("=")
            rung = rg if lad == "CADENCE" else (float(rg) if "." in rg else int(rg))
            st = store[(pan, lad, rung)]
            fc, fs, fd_, f1, f2 = st["FULL"][PROTOCOL_RUNG]
            oc, os_, od = st["OOS"][PROTOCOL_RUNG]
            nomrows.append(dict(stamp_form=d, claim_set=cs, n=len(sub), nominated=top,
                                n_cites=int(vc.iloc[0]), tie=tie, CAGR=fc, Sharpe=fs,
                                MaxDD=fd_, H1=f1, H2=f2, OOS_CAGR=oc, OOS_Sharpe=os_,
                                OOS_MaxDD=od, pass4b=st["p4b"][PROTOCOL_RUNG],
                                pass4b_oos=st["p4bo"][PROTOCOL_RUNG],
                                pass4a=st["p4a"][PROTOCOL_RUNG]))
    nom = pd.DataFrame(nomrows)
    dump(nom, "nominations")
    P("")
    P(f"   {'stamp form':<12s} {'set':<7s} {'nominated book':<20s} {'cites':>6s} {'CAGR':>7s} "
      f"{'Sharpe':>7s} {'MaxDD':>7s} {'OOS S':>7s} {'4b':>4s} {'4bOOS':>6s} {'4a':>4s}")
    for r in nom.itertuples():
        if not r.nominated:
            P(f"   {r.stamp_form:<12s} {r.claim_set:<7s} {'(none re-scorable)':<20s}")
            continue
        P(f"   {r.stamp_form:<12s} {r.claim_set:<7s} {r.nominated:<20s} {r.n_cites:6d} "
          f"{r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} {r.OOS_Sharpe:7.4f} "
          f"{str(r.pass4b):>4s} {str(r.pass4b_oos):>6s} {str(r.pass4a):>4s}")
    base_nom = {r.claim_set: r.nominated for r in nom.itertuples()
                if r.stamp_form == "D0_MODULE"}
    moves = {cs: sorted({r.nominated for r in nom.itertuples() if r.claim_set == cs}
                        - {base_nom.get(cs, "")}) for cs in CLAIM_SETS}
    n_moved = sum(1 for cs in CLAIM_SETS if moves[cs])
    P("")
    P(f"   the stamp MOVES the nominated book at {n_moved} of {len(CLAIM_SETS)} claim sets: "
      + "; ".join(f"{cs}: {base_nom.get(cs, '-')} -> {moves[cs] or ['(unmoved)']}"
                  for cs in CLAIM_SETS))

    # ---------------------------------------------------------- determinism + gates
    r2 = [resolve(r, HEAD_DEPTH)[1] for _, r in cen.iterrows()]
    det = all(a == b for a, b in zip(cen[f"{HEAD_DEPTH}_key"], r2))
    gates["G7 determinism: the resolver gives an identical second pass"] = (
        0.0 if det else 1.0, det)
    f2, _ = script_facts_all_depths(BT / s1149.script.iloc[0])
    det2 = f2 == facts[s1149.script.iloc[0]]
    gates["G8 determinism: the depth scanner gives an identical second pass"] = (
        0.0 if det2 else 1.0, det2)
    # the incumbent book, rebuilt end to end
    px = load_universe().dropna(how="all").ffill()
    idx, K, T = px.index, len(px.columns), len(px)
    sc, elig = mech(px)
    rk = -np.nan_to_num(sc, nan=-np.inf)
    rk[np.isnan(sc)] = np.inf
    mk = rebalance_mask(idx, FREQ0).values
    W, _ = build(rk, elig, px.notna().values, np.flatnonzero(mk), N0, HOLD0, T, K, GROSS0)
    g, tn = nrun(px.pct_change().fillna(0.0).values, lagmat(W), np.roll(mk, LAG))
    warm, ins, oos = windows(idx)
    b = blocks(g - tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)
    ref = books[(books.panel == "U56") & (books.ladder == "N") & (books.rung == N0)].iloc[0]
    d11 = max(abs(b["CAGR"] - ref.CAGR10), abs(b["Sharpe"] - ref.Sharpe10),
              abs(b["MaxDD"] - ref.MaxDD10))
    gates["G11 determinism: the incumbent book rebuilt end-to-end"] = (d11, d11 < 1e-12)

    # ---------------------------------------------------------- hypotheses
    sh_abs = float((sil.D3_DOC == "SILENT").mean())
    hyp.append(dict(hypothesis="H_ABSENT", kind="PRE-REGISTERED",
                    statistic=f"STILL-ABSENT share of the 4,990 at D3_DOC = {sh_abs:.4f}",
                    verdict="CONFIRMED" if sh_abs > 0.50 else "REFUTED",
                    note="bar: a MAJORITY of the SILENT pairs have no value in the file at all"))
    cv2 = int((sil[HEAD_DEPTH] == "PINNED").sum())
    hyp.append(dict(hypothesis="H_CONVERT", kind="PRE-REGISTERED",
                    statistic=f"CONVERTED at {HEAD_DEPTH} = {cv2:,} of {len(sil):,}",
                    verdict="CONFIRMED" if cv2 >= 1000 else "REFUTED",
                    note="bar: >= 1,000 of the 4,990"))
    rs = int(census[(census.stamp_form == HEAD_DEPTH)
                    & (census.claim_set == HEAD_SET)].n_rescorable.iloc[0])
    hyp.append(dict(hypothesis="H_RESCORE", kind="PRE-REGISTERED",
                    statistic=f"R_STAMP({HEAD_DEPTH}, WIDE) re-scores {rs} vs R_UNION's "
                              f"{C1149_UNION}",
                    verdict="CONFIRMED" if rs > C1149_UNION else "REFUTED",
                    note="bar: strictly more than 1149's committed 291"))
    r28 = int(census[(census.stamp_form == HEAD_DEPTH)
                     & (census.claim_set == HEAD_SET)].n28_rescorable.iloc[0])
    hyp.append(dict(hypothesis="H_28", kind="PRE-REGISTERED",
                    statistic=f"the 28 CAGR-floor claims: {r28} re-scorable vs R_UNION's "
                              f"{C1149_28_UNION}",
                    verdict="CONFIRMED" if r28 > C1149_28_UNION else "REFUTED",
                    note="bar: strictly more than 1149's committed 9"))
    sh_def = n_def / len(u) if len(u) else np.nan
    hyp.append(dict(hypothesis="H_DEFAULT", kind="PRE-REGISTERED",
                    statistic=f"DEFAULT-REACHED share of 1149's committed 291 = {sh_def:.4f} "
                              f"({n_def} of {len(u)})",
                    verdict="CONFIRMED" if sh_def > 0.50 else "REFUTED",
                    note="bar: a MAJORITY of the parent's re-scorable claims reach their cell "
                         "only via the frozen defaults"))
    gap = (ab_cens - ab_book) if np.isfinite(ab_cens) and np.isfinite(ab_book) else np.nan
    hyp.append(dict(hypothesis="H_NOTAPPLICABLE", kind="PRE-REGISTERED",
                    statistic=f"STILL-ABSENT at D3_DOC: CENSUS_ONLY {ab_cens:.4f} vs "
                              f"RUNS_A_BOOK {ab_book:.4f}, gap {gap:+.4f}",
                    verdict=("CONFIRMED" if np.isfinite(gap) and gap > 0.20 else "REFUTED"),
                    note="THE RUN'S GUARD ON ITS OWN HEADLINE. REFUTED means the ABSENT bucket "
                         "is NOT explained by 'the axis does not exist' and this run's inherited "
                         "DIMENSION NAME SET is the binding limit — say so, do not widen it."))
    hyp.append(dict(hypothesis="H_FREE", kind="PRE-REGISTERED",
                    statistic=f"module-PINNED pairs whose deepest reading is the SAME value = "
                              f"{share_free:.4f} ({same:,} of {tot:,})",
                    verdict="CONFIRMED" if share_free >= 0.95 else "REFUTED",
                    note="bar: >= 0.95, i.e. for a run that already has the constants the stamp "
                         "is transcription and costs no decision"))
    hy = pd.DataFrame(hyp)
    dump(hy, "hypotheses")
    P("")
    P("## HYPOTHESES (all PRE-REGISTERED; the census arm had not been run when they were written)")
    for r in hy.itertuples():
        P(f"   {r.hypothesis:<17s} {r.verdict:<10s} {r.statistic}")

    dump(cen.drop(columns=[c for c in cen.columns if c.endswith("_key")]), "claims")
    dump(pairs, "pairs")

    g = pd.DataFrame([dict(gate=k, value=v[0], passed=v[1]) for k, v in gates.items()])
    dump(g, "gates")
    P("")
    P(f"## GATES {int(g.passed.sum())} of {len(g)} PASS")
    for r in g.itertuples():
        P(f"   [{'PASS' if r.passed else 'FAIL'}] {r.gate}   value={r.value:.6g}")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {Path(f'{OUT}.console.txt').name}")


if __name__ == "__main__":
    main()
