#!/usr/bin/env python3
"""QUEUE idea 1098 (lane C, 2026-09-16) — do the record's COMMITTED COST CLAIMS price the
SHARPE LEGS, or only the CAGR FLOOR?

QUESTION (QUEUE '## Open' line 1098, verbatim)
    idea 1094 declared in advance that a rising rung would kill a 4b pass on L_CAGR and was
    wrong: it killed it on L_H1, because SPY pays no turnover and the book's vol barely moves,
    so the halves-Sharpe legs bind first.  Census the record's committed cost-ladder claims for
    which leg they reported as binding and re-score those that assumed the CAGR floor.
    Max 2 params (claim set, cost rung).

NUMBERING COLLISION, DECLARED.  This is the idea filed as 1098 under '## Open' on 2026-09-16.
    An EARLIER idea also carries the number 1098 in the record (its block bootstrap is cited by
    1102/1108/1110 as "1098's bootstrap") — idea 932's filing defect again.  Everything below
    refers to the QUEUE line quoted above; the older 1098 is never re-run here.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4)
    CLAIM SET {NARROW, PROX, WIDE} x COST RUNG {0, 10, 25, 50} bps = 12 points, ALL published
    (.census.csv, .rescore.csv, .grid.csv).  Nothing else is selected.  The three claim sets are
    the three readings of "a committed cost claim that names its binding leg":
      NARROW  cost token + binding word + an EXPLICIT leg NAME (`L_CAGR`, `CAGR floor`, `DD cap`,
              `H2 leg`, `L4_DD`, ...).  The record's own vocabulary, read literally.
      PROX    NARROW's names PLUS a bare statistic word (CAGR / H1 / H2 / halves / OOS Sharpe /
              MaxDD / drawdown) within 40 characters of a binding word — the record's commonest
              phrasing ("the binding bar is H2", "dies on the CAGR floor").  HEADLINE.
      WIDE    every cost-and-verdict sentence, whether or not it names a leg; its naming shares
              are read on the PROX lexicon.  This is the set that measures how often the record
              prices NO leg at all.
    NOT dials, all reported at every value: PANEL {U56, B136}; LADDER {N, H, GROSS, CADENCE} at
    1082/1086/1094/1097/1110's rung lists (9 + 4 + 10 + 4 = 27 rungs per panel, 54 books); the
    eight 4b legs; the three rule-8 choosers.  Frozen at 936/1064/1071/1082/1086/1094/1097's
    construction: CAND20 legs (21,252)/(0,126)/(0,63), cap INF, max_vol 0.60, gross 0.75 (except
    on the GROSS ladder), W cadence (except on the CADENCE ladder), min hold 126 (except on the
    H ladder), N = 20 (except on the N ladder), LAG 1, warm-up 260, IS end 2016-12-31, 4b
    constants 0.60 / 0.70.  The 1-bp fine ladder 0..200 bps is a MEASUREMENT AXIS, not a dial:
    no book is selected on it, and the four dial rungs are quoted separately.

WHAT "BINDING" MEANS HERE — PRE-REGISTERED, BEFORE ANY NUMBER
    A cost claim is a claim about an axis measured in bps, so the legs are compared ON THAT AXIS
    and in no other units: for each leg L, c*_L is the last rung of the 1-bp ladder at which L
    still passes, counting only the run that starts at 0 bps (1094/1097's convention, verbatim).
      KILLER(book)   = argmin_L c*_L over the five FULL-sample 4b legs — the leg that actually
                       ends the book's 4b pass as cost rises.  Ties are published as MULTI.
      HEADROOM(L, c) = c*_L - c, the bps of cost the leg has left at rung c.  The BINDING leg at
                       rung c is the smallest headroom.  This is the only cross-leg comparison
                       made here and it needs no fitted constant: the cost axis IS the ruler.
    A book that fails a leg already at 0 bps has no c* on that leg (DEAD0) and is excluded from
    the killer population, which is declared in advance to be exactly the books the queue's
    question is about: those that HAVE a 4b pass for a rising rung to kill.

DECLARED BEFORE ANY NUMBER
    (a) H_SHARPE_FIRST — among books with a finite full-sample c*, the KILLER is a SHARPE leg
        (L_H1, L_H2 or L_OOS) in a MAJORITY.  This is 1094's single-cell correction as a rate.
    (b) H_CAGR_LAST — the strong form: L_CAGR is the LAST of the five full legs to die (largest
        c*_L, DEAD0 counting as first) in a MAJORITY of those books.
    (c) H_DD_INERT — the L_DD verdict is unchanged between 0 and 50 bps at >= 0.90 of the 54
        books: cost moves drawdown almost not at all, so a book binding on DD is cost-immune.
    (d) H_CAGR_ASSUMED — among the record's committed cost claims that NAME a binding leg
        (headline claim set PROX), the CAGR floor is named in a MAJORITY.  This is the queue's
        binary: "only the CAGR floor" is the majority reading.
    (e) H_RESCORE_FLIPS — among CAGR-naming claims that RESOLVE to a measured cell, a MAJORITY
        are REFUTED by their own cell's measured killer leg.
    (f) THE DECISION RULE, fixed before any number.  The queue's binary is answered by the
        headline (PROX) census: the record "prices the Sharpe legs" iff the Sharpe-naming
        share exceeds the CAGR-naming share, and "only the CAGR floor" iff the reverse.  The RE-SCORE is
        reported as three counts that never merge: CONFIRMED / REFUTED / UNDECIDED on resolved
        claims, and TRANSFERRED on the rest — a transferred rate is an EXTRAPOLATION and is
        NOT a re-derivation of the claim (1048/1102/1110's convention).
    (g) NO CLAUSE, NO BOOK, NO RULES CHANGE IS PROPOSED BY THIS RUN unless a book clears a KEEP
        path under rule 8.  4a and 4b are scored at every book x every dial rung anyway, because
        rule 4 requires it, and rule 8 picks the ladder rung on 2009-2016 ALONE.

A DEFECT IN THIS RUN'S OWN FIRST CUT, FIXED AND PUBLISHED.  The first cut resolved a claim to a
    measured cell on the PANEL token alone, letting unstated dimensions take the frozen defaults
    (R_LOOSE).  Reading its 11 resolved claims showed nine of them were about ENSEMBLE, SLEEVE,
    TRIMMED or BAND books that merely mention `u56`: scoring those against the frozen cell's
    killer leg is a TRANSFER wearing a re-derivation's clothes.  The headline rule is therefore
    R_STRICT — panel AND at least one explicitly stated construction dimension AND no
    out-of-family token — and R_LOOSE's count is published beside it as an upper bound.

INHERITED, DECLARED.  Nothing numeric is inherited.  1094's and 1097's committed CSVs are read
    ONLY as cross-run gates (G5, G6): this run rebuilds every book from prices.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every level is
    optimistic.  A breakeven RUNG contrasts one book against SPY, a real index, so the bias does
    NOT cancel out of c* and every c* printed here is an upper bound on the true one.  The
    CENSUS layer is a text scan and carries no market bias at all.
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

DATE = "2026-09-16"
SLUG = "do-the-record-s-COMMITTED-COST-CLAIMS-PRICE-the-SHARPE-LEGS-or-only-the-CAGR-FLOOR"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
BT = Path(__file__).resolve().parent

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, CAPNAME = 0.75, "W", 126, 20, "INF"
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

CFINE = np.arange(0.0, 200.5, 1.0)          # 1094's 201-rung measurement axis
RUNGS = [0.0, 10.0, 25.0, 50.0]             # DIAL 2, all four published
PROTOCOL_RUNG = 10.0
CLAIM_SETS = ["NARROW", "PROX", "WIDE"]     # DIAL 1, all three published
HEAD_SET = "PROX"
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR"]

# committed cross-run anchors (all quoted from committed result.md / CSV files)
A936_WH126 = (0.155787, 1.139701, -0.191276)     # U56 W/H126 N=20 @10 bps full triple
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
C1094_CSTAR_FULL, C1094_CSTAR_OOS = 63.0, 64.0   # 1094's U56 n=12 H=21 breakeven rungs
C1094_TRIPLES = {                                 # 1094's committed U56 n=12/H=21 ladder
    0.0: (0.1764, 1.2131, -0.1945), 10.0: (0.1680, 1.1625, -0.1948),
    25.0: (0.1554, 1.0865, -0.1951), 50.0: (0.1348, 0.9595, -0.1961)}
P1097 = BT / ("2026-09-16_is-the-BREAKEVEN-RUNG-c-star-PREDICTABLE-from-BINDING-LEG-MARGIN-"
              "over-TURNOVER-ALONE_C.cells.csv")

LOG: list[str] = []

if __import__("os").environ.get("SMOKE"):          # wiring check only; never used for a result
    LAD_N, LAD_H, LAD_G, LAD_C = [12, 20], [126, 252], [0.60, 0.75], ["W", "M"]
    LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
    CFINE = np.arange(0.0, 200.5, 10.0)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------------------- mechanics (1094/1097's, verbatim)
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
    """Each 4b leg's margin IN ITS OWN UNITS (1097's, verbatim).  >= 0 means the leg passes."""
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
    """(c*, contiguous, dead_at_0) from a margin array over CFINE (1097's, verbatim)."""
    ok = np.asarray(mvec) >= 0.0
    if not ok[0]:
        return np.nan, True, True
    run = int(np.argmin(ok)) if (~ok).any() else len(ok)
    contiguous = bool(ok[:run].all() and not ok[run:].any())
    return float(CFINE[run - 1]), contiguous, False


def ann_turn(tn, mask):
    n = int(mask.sum())
    return float(tn[mask].sum() / (n / 252.0)) if n else np.nan


# =========================================================== THE CENSUS LAYER (the record)
SENT_SPLIT = re.compile(r"(?<=[\w\)\*\"%])[.;]\s+(?=[^\d])|\s\|\s|\n")
TOK_COSTNUM = re.compile(r"(\d+(?:\.\d+)?)\s*(?:bps|basis points?|bp\b)", re.I)
TOK_COST = re.compile(r"\bbps\b|basis points?|cost rung|cost ladder|cost axis|"
                      r"breakeven rung|c\*|cstar", re.I)
TOK_VERDICT = re.compile(r"\b4b\b|\b4a\b|KEEP path|pass(?:es|ed)?\b|fail(?:s|ed|ure)?\b|"
                         r"clear(?:s|ed)?\b|survive[sd]?\b|die[sd]?\b|kill(?:s|ed)?\b|"
                         r"break(?:s|even)?\b|binding|binds\b", re.I)
TOK_BINDVERB = re.compile(r"\bbind(?:s|ing)?\b|\bkill(?:s|ed)?\b|\bdie[sd]?\b|\bdeath\b|"
                          r"first to fail|fails first|\bbreaks?\b|breakeven|"
                          r"limiting|load-bearing|\bfail(?:s|ed)\b on|\bon\s+L_", re.I)
# --- leg lexicon.  NAME tokens are unambiguous leg names; STAT tokens are bare statistic words
#     that name a leg only when they sit within PROX_CHARS of a binding word (the PROX reading).
TOK_CAGRLEG = re.compile(r"L\d?_CAGR|O_CAGR|CAGR[ -](?:floor|leg|bar)|CAGR-floor", re.I)
TOK_SHARPELEG = re.compile(r"L\d?_H1|L\d?_H2|L\d?_OOS|\bO_S\b|halves[ -]Sharpe|"
                           r"(?:H1|H2|OOS|halves)[ -](?:Sharpe[ -])?(?:leg|bar)|"
                           r"Sharpe[ -](?:leg|bar)", re.I)
TOK_DDLEG = re.compile(r"L\d?_DD|O_DD|(?:DD|drawdown|MaxDD)[ -](?:cap|leg|bar)", re.I)
STAT_CAGR = re.compile(r"\bCAGR\b", re.I)
STAT_SHARPE = re.compile(r"\bH1\b|\bH2\b|\bhalves\b|\bOOS Sharpe\b|\bSharpe\b", re.I)
STAT_DD = re.compile(r"\bMaxDD\b|\bdrawdown\b|\bDD\b", re.I)
PROX_CHARS = 40
TOK_PANEL = re.compile(r"\bU56\b|\bB136\b|\bSMALL\d*\b", re.I)
TOK_N = re.compile(r"\bN\s*=\s*(\d+)|\bn\s*=\s*(\d+)|\bTOP(\d+)\b|\bn(\d+)\b")
TOK_H = re.compile(r"\bH\s*=\s*(\d+)|\bH(\d+)\b")
TOK_G = re.compile(r"gross\s*=?\s*(0\.\d+)|\bg\s*=\s*(0\.\d+)|\bg(0\.\d+)\b", re.I)
TOK_CAD = re.compile(r"\b(daily|weekly|monthly|quarterly)\b", re.I)
CAD_MAP = {"daily": "D", "weekly": "W", "monthly": "M", "quarterly": "Q"}


def sentences(text):
    out = []
    for raw in SENT_SPLIT.split(text):
        if raw is None:
            continue
        s = raw.strip()
        if len(s) >= 25:
            out.append(s)
    return out


def corpus_sources():
    """LEADERBOARD + CHANGELOG + every committed backtest result.md, EXCLUDING this run's own
    outputs.  Deterministic order; stamped by count, bytes and a sha256 of the file list."""
    srcs = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    srcs += sorted(p for p in BT.glob("*.result.md") if not p.name.startswith(f"{DATE}_{SLUG}"))
    return srcs


def _first_int(m):
    for g in m.groups():
        if g:
            return int(g)
    return None


def _first_float(m):
    for g in m.groups():
        if g:
            return float(g)
    return None


def _near(stat_rx, s, bind_spans):
    """A bare statistic word names a leg only when it sits within PROX_CHARS of a binding word."""
    if not bind_spans:
        return False
    for m in stat_rx.finditer(s):
        a, b = m.span()
        for (x, y) in bind_spans:
            if min(abs(a - y), abs(x - b)) <= PROX_CHARS or (x <= a and b <= y):
                return True
    return False


def classify(s):
    """One committed sentence -> its cost-claim fields.  Pure text, no market data."""
    has_cost, has_verdict = bool(TOK_COST.search(s)), bool(TOK_VERDICT.search(s))
    if not (has_cost and has_verdict):
        return None
    bind_spans = [m.span() for m in TOK_BINDVERB.finditer(s)]
    bind = bool(bind_spans)
    n_nc = bool(TOK_CAGRLEG.search(s))
    n_ns = bool(TOK_SHARPELEG.search(s))
    n_nd = bool(TOK_DDLEG.search(s))
    nc = n_nc or _near(STAT_CAGR, s, bind_spans)
    ns = n_ns or _near(STAT_SHARPE, s, bind_spans)
    nd = n_nd or _near(STAT_DD, s, bind_spans)
    named = nc or ns or nd
    named_narrow = n_nc or n_ns or n_nd
    nums = [float(x) for x in TOK_COSTNUM.findall(s)]
    mN, mH, mG, mC = TOK_N.search(s), TOK_H.search(s), TOK_G.search(s), TOK_CAD.search(s)
    mp = TOK_PANEL.search(s)
    kinds = sorted({k for k, f in (("CAGR", nc), ("SHARPE", ns), ("DD", nd)) if f})
    return dict(
        NARROW=bool(named_narrow and bind), PROX=bool(named and bind), WIDE=True,
        NUMERIC=bool(named and bind and nums),
        names_CAGR=nc, names_SHARPE=ns, names_DD=nd, names_any=named, has_bindverb=bind,
        narrow_CAGR=n_nc, narrow_SHARPE=n_ns, narrow_DD=n_nd, names_any_narrow=named_narrow,
        leg_kinds=",".join(kinds) if kinds else "NONE",
        leg_kind_n=len(kinds),
        n_rungs=len(nums), rungs=";".join(f"{x:g}" for x in nums[:6]),
        panel=(mp.group(0).upper() if mp else ""),
        cell_N=(_first_int(mN) if mN else np.nan), cell_H=(_first_int(mH) if mH else np.nan),
        cell_G=(_first_float(mG) if mG else np.nan),
        cell_C=(CAD_MAP[mC.group(1).lower()] if mC else ""),
        text=s[:400].replace("\n", " "))


def harvest(sources):
    rows = []
    for src in sources:
        txt = src.read_text(errors="replace")
        for ln, line in enumerate(txt.split("\n"), 1):
            for s in sentences(line):
                d = classify(s)
                if d is None:
                    continue
                d["src"], d["line"] = src.name, ln
                rows.append(d)
    return pd.DataFrame(rows)


OUT_OF_FAMILY = re.compile(
    r"ensemble|sleeve|overlay|tranche|\bband\b|trim|\bnull\b|coin[- ]flip|random key|QQQ|"
    r"spinoff|putwrite|option|deep ?value|MA-RS|scramble|shuffl|phase|rotat|"
    r"diversifier|equal[- ]weight control|BAND03|EWELIG|vol[- ]scal|min[- ]hold", re.I)


def resolve_strict(row):
    """R_STRICT (HEADLINE): a claim is re-derivable from its own prose only if it names the
    PANEL, names at least one CONSTRUCTION dimension explicitly (N, H, gross or cadence), and
    contains no token placing it outside the frozen family.  R_LOOSE below — panel alone, with
    unstated dimensions taking the frozen defaults — was this run's FIRST CUT and is kept only
    as an UPPER BOUND: inspection of its output showed it attributing ensemble, sleeve and band
    claims to the frozen cell, which is a transfer, not a re-derivation."""
    if row["panel"] not in PANELS:
        return False
    has_dim = any(np.isfinite(row[k]) for k in ("cell_N", "cell_H", "cell_G")) or bool(row["cell_C"])
    return bool(has_dim and not OUT_OF_FAMILY.search(row["text"]))


def resolve_cell(row, book_keys):
    """A claim RESOLVES to a measured book iff its panel is named and the (N, H, gross,
    cadence) it states — unstated dimensions taking the frozen defaults — is one of the 54
    books.  Declared before any number; nothing is fitted here."""
    pan = row["panel"]
    if pan not in PANELS:
        return None
    N = int(row["cell_N"]) if np.isfinite(row["cell_N"]) else N0
    H = int(row["cell_H"]) if np.isfinite(row["cell_H"]) else HOLD0
    G = float(row["cell_G"]) if np.isfinite(row["cell_G"]) else GROSS0
    C = row["cell_C"] or FREQ0
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


# ======================================================================================= main
def main():
    t0 = time.time()
    P(f"# QUEUE idea 1098 (lane C, {DATE}) — do the record's COMMITTED COST CLAIMS price the")
    P("#   SHARPE LEGS, or only the CAGR FLOOR?")
    P(f"# TWO DIALS: CLAIM SET {CLAIM_SETS} x COST RUNG {[int(c) for c in RUNGS]} bps = 12 points,")
    P("#   ALL published.  Panels, ladders, legs and choosers are NOT dials — all reported.")
    P(f"# FROZEN: CAND20 legs {MOMLEGS}; cap {CAPNAME}; max_vol {MAXVOL}; gross {GROSS0}; cadence")
    P(f"#   {FREQ0}; min hold {HOLD0}; N {N0}; LAG {LAG}; warm-up {WARMUP}; IS end {IS_END};")
    P(f"#   4b constants {DD_CAP}/{CAGR_FLOOR}.  Fine ladder 0..200 bps is a MEASUREMENT AXIS.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_SHARPE_FIRST  killer leg is a SHARPE leg in a MAJORITY of books with finite c*.")
    P("#   H_CAGR_LAST     L_CAGR is the LAST full leg to die in a MAJORITY of those books.")
    P("#   H_DD_INERT      L_DD's verdict is unchanged 0->50 bps at >= 0.90 of 54 books.")
    P("#   H_CAGR_ASSUMED  among committed cost claims naming a leg (headline set PROX), CAGR")
    P("#                   is named in a MAJORITY — the queue's 'only the CAGR floor' reading.")
    P("#   H_RESCORE_FLIPS among CAGR-naming claims that RESOLVE to a measured cell, a MAJORITY")
    P("#                   are REFUTED by their own cell's measured killer leg.")
    P("#   DECISION RULE   the binary is answered by the PROX census shares; the re-score is")
    P("#                   published as CONFIRMED / REFUTED / UNDECIDED (resolved) and")
    P("#                   TRANSFERRED (unresolved, an EXTRAPOLATION, never a re-derivation).")
    P("")

    gates: dict[str, tuple] = {}
    bookrows, gridrows, picks, benchrows, ladrows = [], [], [], [], []
    book_keys: dict[str, list] = {p: [] for p in PANELS}
    store: dict[tuple, dict] = {}

    # ------------------------------------------------------------------ PART A: the tape
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        yrs = warm.sum() / 252.0

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        benchrows.append(dict(panel=panel, series="SPY", **sb))
        P(f"## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{yrs:.2f} scored years")
        P(f"   SPY (uncharged 4b bar)  full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / "
          f"{sb['MaxDD']:.2%}  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")

        # live RULES v2 baseline, charged at each dial rung (4a comparand)
        live = {}
        for freq in sorted({FREQ0} | set(LAD_C)):
            r0 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=freq)
            live[freq] = (r0["returns"].values, r0["turnover"].values)
        lg, lt = live[FREQ0]
        lb_by_rung = {c: blocks(lg - lt * c / 1e4, warm, ins, oos) for c in RUNGS}
        benchrows.append(dict(panel=panel, series=f"RULESv2@{int(PROTOCOL_RUNG)}bps",
                              **lb_by_rung[PROTOCOL_RUNG]))
        P(f"   RULES v2 @10 bps  full {lb_by_rung[10.0]['CAGR']:.2%} / "
          f"{lb_by_rung[10.0]['Sharpe']:.4f} / {lb_by_rung[10.0]['MaxDD']:.2%}"
          f"  OOS {lb_by_rung[10.0]['OOS_CAGR']:.2%} / {lb_by_rung[10.0]['OOS_Sharpe']:.4f} / "
          f"{lb_by_rung[10.0]['OOS_MaxDD']:.2%}")

        if panel == "U56":
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN committed SPY OOS triple"] = (d3, d3 < 5e-4)
            d4 = abs(lb_by_rung[PROTOCOL_RUNG]["MaxDD"] - LIVE_MAXDD_COMMITTED)
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

                # ---- gates that need the incumbent book, computed once, on U56
                if panel == "U56" and lad == "N" and rung == 20:
                    wdf = pd.DataFrame(W, index=idx, columns=px.columns)
                    for cg, nm in ((0.0, "G1"), (10.0, "G1b"), (25.0, "G1c")):
                        eng = backtest(px, wdf, cost_bps=cg, freq=C)["returns"].values
                        d = float(np.abs((g - tn * cg / 1e4)[WARMUP:] - eng[WARMUP:]).max())
                        gates[f"{nm} r(c)=g-tn*c/1e4 == engine.backtest @{cg:.0f} bps"] = (d, d < 1e-12)
                    m = fmet((g - tn * PROTOCOL_RUNG / 1e4)[warm])
                    d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
                    gates["G2 CROSS-RUN committed U56 W/H126 N=20 triple @10 bps"] = (d2, d2 < 5e-3)

                # ---- the fine cost ladder, exact
                M = {L: np.empty(len(CFINE)) for L in ALL_LEGS}
                for j, c in enumerate(CFINE):
                    mm = margins(blocks(g - tn * c / 1e4, warm, ins, oos), sb)
                    for L in ALL_LEGS:
                        M[L][j] = mm[L]
                cst, dead0, contig, surv, eff = {}, {}, {}, {}, {}
                for L in ALL_LEGS:
                    cst[L], contig[L], dead0[L] = cstar_from_margin(M[L])
                    # a leg still passing at the LAST rung of the ladder never dies on it:
                    # cstar_from_margin caps such a leg at 200 bps, which would fake a death.
                    surv[L] = bool((not dead0[L]) and M[L][-1] >= 0.0)
                    eff[L] = (np.inf if surv[L] else cst[L])

                pass0_full = not any(dead0[L] for L in FULL_LEGS)
                cstar_full_raw = (min(cst[L] for L in FULL_LEGS) if pass0_full else np.nan)  # 1097's
                cstar_full = (min(eff[L] for L in FULL_LEGS) if pass0_full else np.nan)
                killer = (sorted(L for L in FULL_LEGS if eff[L] == cstar_full)
                          if pass0_full and np.isfinite(cstar_full) else [])
                last_leg = (sorted(FULL_LEGS, key=lambda L: eff[L])[-1] if pass0_full else "")
                pass0_oos = not any(dead0[L] for L in OOS_LEGS)
                cstar_oos = (min(eff[L] for L in OOS_LEGS) if pass0_oos else np.nan)
                killer_oos = (sorted(L for L in OOS_LEGS if eff[L] == cstar_oos)
                              if pass0_oos and np.isfinite(cstar_oos) else [])

                b_by_rung = {c: blocks(g - tn * c / 1e4, warm, ins, oos) for c in RUNGS}
                lgc, ltc = live[C]
                lbc = {c: blocks(lgc - ltc * c / 1e4, warm, ins, oos) for c in RUNGS}
                dd0 = margins(b_by_rung[0.0], sb)["L_DD"] >= 0
                dd50 = margins(b_by_rung[50.0], sb)["L_DD"] >= 0

                row = dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=G, cadence=C,
                           mean_nsel=float(nsel.mean()), turnover=turn,
                           pass0_full=pass0_full, cstar_full=cstar_full,
                           cstar_full_raw=cstar_full_raw,
                           alive200=bool(pass0_full and not np.isfinite(cstar_full)),
                           killer=",".join(killer) if killer else ("DEAD0" if not pass0_full else "NONE<=200"),
                           killer_kind=("SHARPE" if killer and set(killer) <= SHARPE_LEGS else
                                        "CAGR" if killer and set(killer) <= CAGR_LEGS else
                                        "DD" if killer and set(killer) <= DD_LEGS else
                                        "MULTI" if killer else "NONE"),
                           last_leg=last_leg, pass0_oos=pass0_oos, cstar_oos=cstar_oos,
                           killer_oos=",".join(killer_oos) if killer_oos else
                           ("DEAD0" if not pass0_oos else "NONE<=200"),
                           dd_verdict_stable=bool(dd0 == dd50))
                for L in ALL_LEGS:
                    row[f"cstar_{L}"] = cst[L]
                    row[f"dead0_{L}"] = dead0[L]
                    row[f"contig_{L}"] = contig[L]
                    row[f"surv200_{L}"] = surv[L]
                for c in RUNGS:
                    b = b_by_rung[c]
                    mm = margins(b, sb)
                    l4a = legs_4a(b, lbc[c])
                    p4b = all(mm[L] >= 0 for L in FULL_LEGS)
                    p4bo = all(mm[L] >= 0 for L in OOS_LEGS)
                    row[f"CAGR{int(c)}"] = b["CAGR"]
                    row[f"Sharpe{int(c)}"] = b["Sharpe"]
                    row[f"MaxDD{int(c)}"] = b["MaxDD"]
                    row[f"OOS_Sharpe{int(c)}"] = b["OOS_Sharpe"]
                    row[f"OOS_CAGR{int(c)}"] = b["OOS_CAGR"]
                    row[f"OOS_MaxDD{int(c)}"] = b["OOS_MaxDD"]
                    row[f"pass4b{int(c)}"] = p4b
                    row[f"pass4bOOS{int(c)}"] = p4bo
                    row[f"pass4a{int(c)}"] = all(l4a.values())
                    # binding leg at this rung = smallest positive headroom on the cost axis
                    hr = {L: (eff[L] - c) for L in FULL_LEGS if not dead0[L] and eff[L] >= c}
                    row[f"binding{int(c)}"] = (min(hr, key=hr.get) if hr else "DEAD")
                    row[f"headroom{int(c)}"] = (min(hr.values()) if hr else np.nan)
                    gridrows.append(dict(panel=panel, ladder=lad, rung=rung, cost_rung=c,
                                         pass4b=p4b, pass4b_oos=p4bo, pass4a=all(l4a.values()),
                                         binding=row[f"binding{int(c)}"],
                                         headroom_bps=row[f"headroom{int(c)}"],
                                         CAGR=b["CAGR"], Sharpe=b["Sharpe"], MaxDD=b["MaxDD"],
                                         OOS_CAGR=b["OOS_CAGR"], OOS_Sharpe=b["OOS_Sharpe"],
                                         OOS_MaxDD=b["OOS_MaxDD"], turnover=turn, **l4a))
                bookrows.append(row)
                book_keys[panel].append((lad, rung))
                store[(panel, lad, rung)] = dict(
                    IS_S={c: b_by_rung[c]["IS_Sharpe"] for c in RUNGS},
                    IS_DD={c: b_by_rung[c]["IS_MaxDD"] for c in RUNGS},
                    IS_CAGR={c: b_by_rung[c]["IS_CAGR"] for c in RUNGS},
                    OOS={c: (b_by_rung[c]["OOS_CAGR"], b_by_rung[c]["OOS_Sharpe"],
                             b_by_rung[c]["OOS_MaxDD"]) for c in RUNGS},
                    FULL={c: (b_by_rung[c]["CAGR"], b_by_rung[c]["Sharpe"], b_by_rung[c]["MaxDD"])
                          for c in RUNGS},
                    p4b={c: all(margins(b_by_rung[c], sb)[L] >= 0 for L in FULL_LEGS) for c in RUNGS},
                    p4bo={c: all(margins(b_by_rung[c], sb)[L] >= 0 for L in OOS_LEGS) for c in RUNGS},
                    p4a={c: all(legs_4a(b_by_rung[c], lbc[c]).values()) for c in RUNGS},
                    turn=turn)

                # 1094's candidate and 1097's overlap gates
                if panel == "U56" and lad == "H" and rung == 21:
                    pass  # H ladder is at N=20; 1094's candidate is N=12/H=21, built below

                ladrows.append(dict(panel=panel, ladder=lad, rung=rung,
                                    **{f"cstar_{L}": cst[L] for L in ALL_LEGS}))

        # ---- G5: 1094's U56 n=12 / H=21 candidate, rebuilt from prices
        if panel == "U56":
            W, _ = build(rank_key, elig, priced, rebs[FREQ0], 12, 21, T, K, GROSS0)
            g, tn = nrun(rets, lagmat(W), masks[FREQ0])
            trip = {}
            for c in RUNGS:
                b = blocks(g - tn * c / 1e4, warm, ins, oos)
                trip[c] = (b["CAGR"], b["Sharpe"], b["MaxDD"])
            d5 = max(max(abs(trip[c][i] - C1094_TRIPLES[c][i]) for i in range(3)) for c in RUNGS)
            gates["G5 CROSS-RUN 1094's committed n=12/H=21 ladder (0/10/25/50 bps triples)"] = (d5, d5 < 5e-4)
            Mc = {L: np.empty(len(CFINE)) for L in ALL_LEGS}
            for j, c in enumerate(CFINE):
                mm = margins(blocks(g - tn * c / 1e4, warm, ins, oos), sb)
                for L in ALL_LEGS:
                    Mc[L][j] = mm[L]
            cs = {L: cstar_from_margin(Mc[L]) for L in ALL_LEGS}
            cf = min(cs[L][0] for L in FULL_LEGS)
            co = min(cs[L][0] for L in OOS_LEGS)
            kill94 = sorted(L for L in FULL_LEGS if cs[L][0] == cf)
            d6 = max(abs(cf - C1094_CSTAR_FULL), abs(co - C1094_CSTAR_OOS))
            gates[f"G5b 1094's c* full/OOS == 63/64 (got {cf:.0f}/{co:.0f}, killer {','.join(kill94)})"] = (d6, d6 < 1e-9)
            gates["G5c 1094's killer leg is L_H1"] = (0.0 if kill94 == ["L_H1"] else 1.0, kill94 == ["L_H1"])

    books = pd.DataFrame(bookrows)
    grid = pd.DataFrame(gridrows)

    # G6: cross-run 1097's committed 54-cell c* where the grids overlap
    if P1097.exists():
        c97 = pd.read_csv(P1097)
        mine = books[(books.ladder == "N") & (books.H == HOLD0)][["panel", "N", "cstar_full_raw"]] \
            .rename(columns={"cstar_full_raw": "cstar_full"})
        ov = c97[c97.H == HOLD0][["panel", "N", "cstar_full"]].merge(mine, on=["panel", "N"],
                                                                     suffixes=("_97", "_now"))
        both = ov.dropna()
        d7 = float(np.abs(both.cstar_full_97 - both.cstar_full_now).max()) if len(both) else np.nan
        nan_agree = bool((ov.cstar_full_97.isna() == ov.cstar_full_now.isna()).all())
        gates[f"G6 CROSS-RUN 1097's committed c*_full on the {len(ov)} shared N/H126 cells"] = (
            (d7 if np.isfinite(d7) else 0.0), (nan_agree and (not np.isfinite(d7) or d7 < 1e-9)))
    else:
        gates["G6 CROSS-RUN 1097 cells.csv present"] = (1.0, False)

    # G7 monotone CAGR in the rung; G8 DD-inertness is a RESULT not a gate
    mono = all(books[f"CAGR{int(RUNGS[i])}"].values[k] >= books[f"CAGR{int(RUNGS[i+1])}"].values[k] - 1e-12
               for i in range(len(RUNGS) - 1) for k in range(len(books)))
    gates["G7 CAGR non-increasing in the cost rung at every book"] = (0.0 if mono else 1.0, mono)

    # ---------------------------------------------------------- PART B: the record's claims
    srcs = corpus_sources()
    nbytes = sum(p.stat().st_size for p in srcs)
    sha = hashlib.sha256("\n".join(p.name for p in srcs).encode()).hexdigest()[:16]
    P("")
    P(f"## CORPUS STAMP: {len(srcs)} files, {nbytes:,} bytes, sha256(file list)[:16] = {sha}")
    cen = harvest(srcs)
    cen2 = harvest(srcs)
    same = len(cen) == len(cen2) and bool((cen.text.values == cen2.text.values).all())
    gates["G9 harvest is reproducible (two scans identical)"] = (0.0 if same else 1.0, same)
    gates[f"G10 corpus stamp ({len(srcs)} files / {nbytes:,} bytes / {sha})"] = (0.0, True)

    P(f"   harvested {len(cen):,} cost-and-verdict sentences "
      f"({cen.NARROW.sum():,} NARROW, {cen.PROX.sum():,} PROX, {cen.WIDE.sum():,} WIDE, "
      f"{cen.NUMERIC.sum():,} carry a numeric rung)")

    cen["cell"] = [resolve_cell(r, book_keys) for _, r in cen.iterrows()]
    cen["resolved_loose"] = cen.cell.notna()
    cen["strict_ok"] = [resolve_strict(r) for _, r in cen.iterrows()]
    cen["resolved"] = cen.resolved_loose & cen.strict_ok      # HEADLINE = R_STRICT
    cen["cell_str"] = [f"{c[0]}/{c[1]}={c[2]}" if c else "" for c in cen.cell]

    kill_by_cell = {(r.panel, r.ladder, r.rung): (r.killer, r.killer_kind)
                    for r in books.itertuples()}
    base_kind = books[books.pass0_full].killer_kind.value_counts(normalize=True).to_dict()

    resc, censusrows = [], []
    for cs in CLAIM_SETS:
        sub = cen[cen[cs]]
        # NARROW reads only explicit leg NAMES; PROX and WIDE also read the proximity rule.
        nm = "names_any_narrow" if cs == "NARROW" else "names_any"
        cc, sc_, dc = (("narrow_CAGR", "narrow_SHARPE", "narrow_DD") if cs == "NARROW"
                       else ("names_CAGR", "names_SHARPE", "names_DD"))
        sub = sub.assign(_named=sub[nm], _C=sub[cc], _S=sub[sc_], _D=sub[dc])
        named = sub[sub._named]
        for c in RUNGS:
            at_rung = sub[[bool(re.search(rf"\b{int(c)}(?:\.0)?\s*(?:bps|basis)", t, re.I))
                           for t in sub.text]] if c else sub[[bool(re.search(r"\b0\s*(?:bps|basis)", t, re.I))
                                                              for t in sub.text]]
            ar = at_rung[at_rung[nm]] if len(at_rung) else at_rung
            censusrows.append(dict(
                claim_set=cs, cost_rung=c, n_claims=len(sub), n_named=len(named),
                share_unnamed=float(1.0 - len(named) / len(sub)) if len(sub) else np.nan,
                n_at_rung=len(at_rung),
                share_CAGR=float(named._C.mean()) if len(named) else np.nan,
                share_SHARPE=float(named._S.mean()) if len(named) else np.nan,
                share_DD=float(named._D.mean()) if len(named) else np.nan,
                share_CAGR_only=float((named._C & ~named._S & ~named._D).mean())
                if len(named) else np.nan,
                share_SHARPE_only=float((named._S & ~named._C & ~named._D).mean())
                if len(named) else np.nan,
                n_resolved=int(sub.resolved.sum()), n_resolved_loose=int(sub.resolved_loose.sum()),
                share_CAGR_at_rung=float(ar[cc].mean()) if len(ar) else np.nan,
                share_SHARPE_at_rung=float(ar[sc_].mean()) if len(ar) else np.nan))

        # ---- re-score the CAGR-assuming claims
        cag = sub[sub._C & ~sub._S & ~sub._D]
        def _verdict(cell):
            killer, kind = kill_by_cell[cell]
            if killer == "DEAD0":
                return killer, kind, "UNDECIDED_DEAD0"      # the cell fails 4b already at 0 bps
            if killer == "NONE<=200" or kind == "NONE":
                return killer, kind, "UNDECIDED_NO_CSTAR"   # never dies on the 0..200 ladder
            if set(killer.split(",")) & CAGR_LEGS:
                return killer, kind, "CONFIRMED"
            return killer, kind, "REFUTED"

        for _, r in cag.iterrows():
            has_cell = r["cell"] is not None and r["cell"] in kill_by_cell
            if has_cell and r["strict_ok"]:
                killer, kind, v = _verdict(r["cell"])
                basis = "MEASURED"
            else:
                killer, kind, v, basis = "", "", "TRANSFERRED", "TRANSFERRED"
            lv = _verdict(r["cell"])[2] if has_cell else ""   # R_LOOSE upper bound, flagged
            resc.append(dict(claim_set=cs, src=r["src"], line=r["line"],
                             cell=r["cell_str"], loose_cell=bool(r["resolved_loose"]),
                             strict_ok=bool(r["strict_ok"]), basis=basis, verdict=v,
                             loose_verdict=lv, measured_killer=killer, measured_kind=kind,
                             text=r["text"][:240]))
    census = pd.DataFrame(censusrows)
    rescore = pd.DataFrame(resc)

    # -------------------------------------------------- PART C: rule 8 + both KEEP paths
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            for c in RUNGS:
                for ch in CHOOSERS:
                    key = {"C_ISSHARPE": "IS_S", "C_ISDD": "IS_DD", "C_ISCAGR": "IS_CAGR"}[ch]
                    vals = {rg: store[(panel, lad, rg)][key][c] for rg in rungs}
                    pick = max(vals, key=lambda k: vals[k])       # IS_DD: larger (less negative)
                    st = store[(panel, lad, pick)]
                    oc, os_, od = st["OOS"][c]
                    fc, fs, fd = st["FULL"][c]
                    picks.append(dict(panel=panel, ladder=lad, cost_rung=c, chooser=ch,
                                      pick=pick, IS_stat=vals[pick], turnover=st["turn"],
                                      OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                                      CAGR=fc, Sharpe=fs, MaxDD=fd,
                                      pass4b=st["p4b"][c], pass4b_oos=st["p4bo"][c],
                                      pass4a=st["p4a"][c]))
    pick_df = pd.DataFrame(picks)

    # ------------------------------------------------------------------------ G8 determinism
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
    d8 = max(abs(b["CAGR"] - ref.CAGR10), abs(b["Sharpe"] - ref.Sharpe10), abs(b["MaxDD"] - ref.MaxDD10))
    gates["G8 determinism (incumbent book rebuilt end-to-end)"] = (d8, d8 < 1e-12)

    # ---------------------------------------------------------------------------- printing
    P("")
    P("## GATES")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}   ({v:.2e})")
    P(f"   {sum(1 for _, (_, ok) in gates.items() if ok)} of {len(gates)} PASS")

    P("")
    P("## PART A — WHICH LEG ACTUALLY BINDS AS COST RISES (54 books, 1-bp ladder 0..200)")
    liv = books[books.pass0_full]
    dyn = liv[np.isfinite(liv.cstar_full)]          # the books a rising rung can kill
    P(f"   books clearing all five FULL 4b legs at 0 bps: {len(liv)} of {len(books)}"
      f"   (of which {int(liv.alive200.sum())} survive the whole 0..200 bps ladder)")
    P(f"   KILLER POPULATION (declared): the {len(dyn)} books that both pass at 0 bps and die by 200")
    for k, v in dyn.killer_kind.value_counts().items():
        P(f"     killer kind {k:<7} {v:3d}  ({v/len(dyn):.3f})")
    P("   killer leg (exact):  " + "  ".join(f"{k}={v}" for k, v in dyn.killer.value_counts().items()))
    sh_any = float(dyn.killer.apply(lambda s: bool(set(s.split(",")) & SHARPE_LEGS)).mean()) if len(dyn) else np.nan
    cg_any = float(dyn.killer.apply(lambda s: bool(set(s.split(",")) & CAGR_LEGS)).mean()) if len(dyn) else np.nan
    dd_any = float(dyn.killer.apply(lambda s: bool(set(s.split(",")) & DD_LEGS)).mean()) if len(dyn) else np.nan
    P(f"   killer contains a SHARPE leg {sh_any:.3f} | a CAGR leg {cg_any:.3f} | a DD leg {dd_any:.3f}")
    P("   LAST full leg to die: " + "  ".join(f"{k}={v}" for k, v in liv.last_leg.value_counts().items()))
    ddst = float(books.dd_verdict_stable.mean())
    P(f"   L_DD verdict unchanged 0->50 bps at {ddst:.3f} of {len(books)} books")
    if len(dyn):
        P(f"   median c*_full over the {len(dyn)} dying books = {dyn.cstar_full.median():.0f} bps  "
          f"(min {dyn.cstar_full.min():.0f}, max {dyn.cstar_full.max():.0f})")
    for lad in LADDERS:
        s = dyn[dyn.ladder == lad]
        if len(s):
            P(f"     ladder {lad:<8} n={len(s):2d}  killer kinds " +
              ", ".join(f"{k}:{v}" for k, v in s.killer_kind.value_counts().items()))

    P("")
    P("## PART A2 — THE BINDING LEG AT EACH DIAL RUNG (headroom on the cost axis, bps)")
    for c in RUNGS:
        s = grid[(grid.cost_rung == c) & grid.binding.ne("DEAD")]
        if len(s):
            vc = s.binding.value_counts()
            P(f"   {int(c):>2} bps: " + "  ".join(f"{k}={v}" for k, v in vc.items()) +
              f"   median headroom {s.headroom_bps.median():.0f} bps")

    P("")
    P("## PART B — THE RECORD'S COMMITTED COST CLAIMS (census, 12 dial points)")
    P(census.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    wide0 = census[(census.claim_set == "WIDE") & (census.cost_rung == PROTOCOL_RUNG)].iloc[0]
    P(f"   OF EVERY COMMITTED COST-AND-VERDICT SENTENCE, {wide0.share_unnamed:.4f} "
      f"({int(wide0.n_claims - wide0.n_named):,} of {int(wide0.n_claims):,}) NAMES NO LEG AT ALL.")
    P("")
    P("## PART B2 — RE-SCORING THE CLAIMS THAT ASSUMED THE CAGR FLOOR")
    for cs in CLAIM_SETS:
        s = rescore[rescore.claim_set == cs]
        vc = s.verdict.value_counts()
        res = s[s.basis == "MEASURED"]
        P(f"   {cs:<8} CAGR-only claims {len(s):4d}  resolved {len(res):3d}  " +
          "  ".join(f"{k}={v}" for k, v in vc.items()))
        if len(res):
            P(f"            of the resolved: REFUTED {float((res.verdict=='REFUTED').mean()):.3f}, "
              f"CONFIRMED {float((res.verdict=='CONFIRMED').mean()):.3f}")
    P(f"   RESOLUTION, both rules: R_STRICT (headline) resolves {int(cen.resolved.sum())} of "
      f"{len(cen)} harvested claims; R_LOOSE — panel alone, unstated dimensions taking the frozen "
      f"defaults — resolves {int(cen.resolved_loose.sum())}.  R_LOOSE was this run's FIRST CUT and "
      f"is published as an UPPER BOUND only: reading its output showed it re-scoring ensemble, "
      f"sleeve and band claims against the frozen cell, which is a TRANSFER, not a re-derivation.")
    if len(rescore):
        for cs in CLAIM_SETS:
            lo = rescore[(rescore.claim_set == cs) & rescore.loose_cell]
            if len(lo):
                vc = lo.loose_verdict.value_counts()
                P(f"   R_LOOSE UPPER BOUND, {cs}: {len(lo)} CAGR-only claims would have been "
                  f"re-scored — " + "  ".join(f"{k}={v}" for k, v in vc.items()) +
                  "  — every one is published above as TRANSFERRED instead.")
    P(f"   TRANSFERRED basis (an EXTRAPOLATION, not a re-derivation): the measured killer-kind "
      f"base rate is " + ", ".join(f"{k} {v:.3f}" for k, v in base_kind.items()))

    P("")
    P("## PART C — BOTH KEEP PATHS AT EVERY GRID POINT, AND RULE 8")
    for c in RUNGS:
        s = grid[grid.cost_rung == c]
        P(f"   {int(c):>2} bps: 4b full {int(s.pass4b.sum()):2d}/{len(s)}   "
          f"4b OOS {int(s.pass4b_oos.sum()):2d}/{len(s)}   4a {int(s.pass4a.sum()):2d}/{len(s)}")
    P(f"   rule-8 picks: {len(pick_df)} (panel x ladder x rung x chooser); "
      f"4b full {int(pick_df.pass4b.sum())}, 4b OOS {int(pick_df.pass4b_oos.sum())}, "
      f"4a {int(pick_df.pass4a.sum())}")
    ph = pick_df[pick_df.cost_rung == PROTOCOL_RUNG]
    P("   at PROTOCOL's 10 bps, OOS of each pick (CAGR / Sharpe / MaxDD):")
    for _, r in ph.iterrows():
        P(f"     {r.panel:<5}{r.ladder:<8}{r.chooser:<11} pick={str(r['pick']):<5} "
          f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.4f} / {r.OOS_MaxDD:7.2%}  "
          f"4b={bool(r.pass4b)} 4bOOS={bool(r.pass4b_oos)} 4a={bool(r.pass4a)}")
    bench = pd.DataFrame(benchrows)
    for _, r in bench.iterrows():
        P(f"   BENCH {r.panel:<5}{r.series:<16} full {r.CAGR:7.2%} / {r.Sharpe:6.4f} / "
          f"{r.MaxDD:7.2%}   OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.4f} / {r.OOS_MaxDD:7.2%}")

    # ----------------------------------------------------------------------- hypotheses
    hyp = []

    def H(name, stat, ok, note):
        hyp.append(dict(hypothesis=name, statistic=stat, verdict="PASS" if ok else "FAIL",
                        note=note))

    H("H_SHARPE_FIRST", sh_any, bool(np.isfinite(sh_any) and sh_any > 0.5),
      f"share of the {len(dyn)} dying books whose killer set contains a SHARPE leg")
    H("H_CAGR_LAST", float((liv.last_leg == "L_CAGR").mean()) if len(liv) else np.nan,
      bool(len(liv) and (liv.last_leg == "L_CAGR").mean() > 0.5),
      f"share of the {len(liv)} live books where L_CAGR is the LAST full leg to die")
    H("H_DD_INERT", ddst, bool(ddst >= 0.90), "share of books whose L_DD verdict is 0->50 stable")
    hs = census[(census.claim_set == HEAD_SET) & (census.cost_rung == PROTOCOL_RUNG)].iloc[0]
    H("H_CAGR_ASSUMED", float(hs.share_CAGR), bool(hs.share_CAGR > 0.5),
      f"{HEAD_SET} claims naming a leg that name the CAGR floor (n={int(hs.n_named)})")
    rs = rescore[(rescore.claim_set == HEAD_SET) & (rescore.basis == "MEASURED")]
    rf = float((rs.verdict == "REFUTED").mean()) if len(rs) else np.nan
    rl = rescore[(rescore.claim_set == HEAD_SET) & rescore.loose_cell]
    rlf = float((rl.loose_verdict == "REFUTED").mean()) if len(rl) else np.nan
    if len(rs):
        H("H_RESCORE_FLIPS", rf, bool(rf > 0.5),
          f"resolved CAGR-only claims refuted by their own cell (n={len(rs)})")
    else:
        hyp.append(dict(hypothesis="H_RESCORE_FLIPS", statistic=rlf, verdict="UNRESOLVABLE",
                        note=("NO CAGR-only cost claim in the record states enough of its own "
                              f"cell to be re-derived (n=0 under R_STRICT); the statistic shown "
                              f"is R_LOOSE's upper bound over n={len(rl)}, a TRANSFER")))
    hyp_df = pd.DataFrame(hyp)
    P("")
    P("## HYPOTHESES (all declared before any number)")
    P(hyp_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("")
    P(f"## THE QUEUE'S BINARY, by the decision rule: {HEAD_SET} naming shares — "
      f"CAGR {hs.share_CAGR:.4f} vs SHARPE {hs.share_SHARPE:.4f} vs DD {hs.share_DD:.4f}")

    dump(books, "books")
    dump(grid, "grid")
    dump(pd.DataFrame(ladrows), "ladder")
    dump(census, "census")
    dump(rescore, "rescore")
    dump(cen.drop(columns=["cell"]), "claims")
    dump(pick_df, "walkforward")
    dump(bench, "benchmarks")
    dump(hyp_df, "hypotheses")
    dump(pd.DataFrame([dict(gate=k, value=v, passed=ok) for k, (v, ok) in gates.items()]), "gates")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\n[{time.time()-t0:.1f}s]")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
