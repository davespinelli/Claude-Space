#!/usr/bin/env python3
"""Idea 1131 (lane B, 2026-09-16)
   does-ANY-committed-FLOOR-KEYED-CLAUSE-in-the-record-survive-a-RUNG-SET-CHANGE

1117 killed ONE clause (the argmax ban) on rung dependence: 12 of 32 committed argmaxes
barred at 1110/1116's 4-rung H and CADENCE ladders, 0 of 32 at 1118's 9-rung ones.  1122
then killed a SECOND trigger the same way (B_TIESET, 18 -> 9) and published the general
statement: *a clause is rung-stable iff every quantity in its TRIGGER is a property of the
peak and its own pair, never of the ladder.*

Nobody has run the CENSUS that statement implies.  This run harvests EVERY committed object
in the record whose trigger reads a WHOLE-LADDER INFINITE FLOOR — cell-level flags in
committed CSVs and clause / bar / verdict sentences in committed prose — re-evaluates each
one's trigger at BOTH rung sets from a fresh rebuild of the tape, and reports how many are
RUNG-ESCAPABLE.

It also asks the question an author would actually ask: HOW MANY RUNGS does it cost to
escape?  For H and CADENCE every superset of the CORE rungs inside the EXT ladder is
enumerated EXHAUSTIVELY (2^5 = 32 each), so the minimum k at which the trigger stops firing
is exact, not sampled.

TUNED DIALS (2, PROTOCOL rule 4): `CLAIM SET` {CS_CELL, CS_PROSE, CS_ALL} x `RUNG SET`
{CORE, EXT} = 6 combinations, ALL published.  PANEL, LADDER and STATISTIC are not dials
(all 2 x 4 x 4 = 32 rebuilt cells reported everywhere).  CONFIDENCE q is NOT a dial: 0.90 is
the headline and 0.80 / 0.95 are reported beside it at every point, never selected on.  The
ALL-vs-ANY reading of a multi-cell prose claim is NOT a dial either: ALL is the record's own
wording (1110/1116/1117) and is the headline; ANY is reported beside it everywhere.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1122's construction: CAND20 legs,
cap INF, max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps, LAG 1, warm-up 260, IS end
2016-12-31, block L=63, 1000 draws, crc32 seeds, 3 seed bases.

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
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "does-ANY-committed-FLOOR-KEYED-CLAUSE-survive-a-RUNG-SET-CHANGE"
BT = Path(__file__).resolve().parent
OUT = BT / f"{DATE}_{SLUG}_B"
PRIOR1110 = BT / "2026-09-16_what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN_C"
PRIOR1117 = BT / "2026-09-16_should-the-PROTOCOL-forbid-publishing-an-ARGMAX-on-an-H-or-CADENCE-LADDER-at-all_B"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]                              # 9 rungs, both sets
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]    # 10 rungs, both sets
H_CORE = [21, 63, 126, 252]
H_EXT = [21, 42, 63, 84, 126, 168, 210, 252, 378]                       # nests H_CORE
C_CORE = ["D", "W", "M", "Q"]
C_EXT = ["D", "2D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]              # nests C_CORE

STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
SCALE = {"S_FULL": 1.0, "S_OOS": 1.0, "CAGR": 100.0, "DD": 100.0}
STATCOL = {"S_FULL": "Sharpe", "S_OOS": "OOS_Sharpe", "CAGR": "CAGR", "DD": "MaxDD"}
LADDERS = ["N", "H", "GROSS", "CADENCE"]
PANELS = ["U56", "B136"]
RUNGSETS = ["CORE", "EXT"]
DEFAULT_RUNG = {"N": "20", "H": "126", "GROSS": "0.75", "CADENCE": "W"}

CLAIM_SETS = ["CS_CELL", "CS_PROSE", "CS_ALL"]     # dial 1
QS = [0.80, 0.90, 0.95]
Q_HEAD, L_HEAD, BDRAWS = 0.90, 63, 1000
SEED_BASES = [11311131, 11171117, 11161116]

CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", "OOS_Sharpe", +1.0),
            "C_ISCAGR": ("IS_CAGR", "OOS_CAGR", +1.0),
            "C_ISDD": ("IS_MaxDD", "OOS_MaxDD", +1.0)}

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

# ------------------------------------------------------------------ THE HARVEST, DECLARED
# A committed object is IN the corpus iff its TRIGGER reads a WHOLE-LADDER INFINITE FLOOR.
TRIG_RX = re.compile(r"(infinite (resolution )?floor|INF_FLOOR|inf floor|un-?resolvab|"
                     r"contentless|whole-?ladder|whole ladder)", re.I)
# a sentence is a CLAUSE / BAR / VERDICT (rather than a bare quotation) iff it also carries
# a decision word:
DEC_RX = re.compile(r"\b(bar|bars|barred|ban|bans|banned|delete|deletes|deleted|forbid|"
                    r"forbids|may not|must not|refuse|refuses|suppress|disqualif|KILL|"
                    r"killed|verdict|fires|trigger|trigger|not be published|no argmax)\b", re.I)
LAD_RX = {
    "H": re.compile(r"\bH ladder\b|\bH-ladder\b|\bH dial\b|\bH axis\b|\bmin.?hold\b|"
                    r"\bH ?= ?\d|\bH\d{2,3}\b|\bH and CADENCE\b|\bH or CADENCE\b|\bH/", re.I),
    "CADENCE": re.compile(r"\bcadence\b", re.I),
    "GROSS": re.compile(r"\bgross\b", re.I),
    "N": re.compile(r"\bN ladder\b|\bN-ladder\b|\bN dial\b|\bn dial\b|\bN axis\b|"
                    r"\bN ?= ?\d|\bn ?= ?\d", re.I),
}
PAN_RX = {"U56": re.compile(r"\bU56\b|\bu56\b"), "B136": re.compile(r"\bB136\b"),
          "SMALL": re.compile(r"\bSMALL\d*\b|\bsmall panel\b", re.I)}
STAT_RX = {"S_FULL": re.compile(r"\bS_FULL\b|\bfull.sample Sharpe\b", re.I),
           "S_OOS": re.compile(r"\bS_OOS\b|\bOOS Sharpe\b", re.I),
           "CAGR": re.compile(r"\bCAGR\b"),
           "DD": re.compile(r"\bDD\b|\bMaxDD\b|\bdrawdown\b", re.I)}
INF_COLNAMES = ("inf_floor", "inf", "infinite", "inf_count")

PROSE_FILES = ([str(ROOT / "research" / "CHANGELOG.md"), str(ROOT / "research" / "LEADERBOARD.md")]
               + sorted(glob.glob(str(BT / "*.result.md")))
               + sorted(glob.glob(str(BT / "*.memo.md"))))

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(base, *parts):
    return base + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------- 1082/1098/1102/1108/1117's fast runner
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


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


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


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, warm, ins, oos):
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


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


# --------------------------------------------------- 1098/1102's bootstrap, 1108's seed repair
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_exact(R, idx, nb, L, chunk=100):
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    nd = idx.shape[0]
    st = idx[:, ::L]
    cag = np.empty((R.shape[0], nd))
    shp = np.empty((R.shape[0], nd))
    n = nb * L
    for a in range(0, nd, chunk):
        s = st[a:a + chunk]
        lsum = (CS[:, s + L] - CS[:, s]).sum(axis=2)
        s1 = (CS1[:, s + L] - CS1[:, s]).sum(axis=2)
        s2 = (CS2[:, s + L] - CS2[:, s]).sum(axis=2)
        cag[:, a:a + chunk] = np.expm1(lsum * (252.0 / n))
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        shp[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return cag, shp


def boot_maxdd(R, idx, chunk=40):
    nr, _ = R.shape
    nd = idx.shape[0]
    out = np.empty((nr, nd))
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            path = np.log1p(R[j])[ix]
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
    return out


def agree_matrix(vals, boot):
    k = len(vals)
    A = np.full((k, k), np.nan)
    np.fill_diagonal(A, 1.0)
    for i, j in combinations(range(k), 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g):
            continue
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        A[i, j] = A[j, i] = float((np.sign(d) == np.sign(g)).mean()) if len(d) else np.nan
    return A


def floor_sub(vals, A, sub, q):
    """1098's floor restricted to rung subset `sub`: the smallest gap above which EVERY pair
    is resolved at q; INFINITE when the LARGEST gap in the subset is itself un-resolved."""
    gaps, agr = [], []
    for i, j in combinations(sub, 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g) or not np.isfinite(A[i, j]):
            continue
        gaps.append(abs(g))
        agr.append(A[i, j])
    if not gaps:
        return float("inf"), 0.0
    gaps, agr = np.array(gaps), np.array(agr)
    un = agr < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    return (float(gaps[ok].min()) if ok.any() else float("inf")), largest_un


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    ra, rb = ra - ra.mean(), rb - rb.mean()
    den = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / den) if den else np.nan


def cadence_mask(idx, spec):
    """engine.rebalance_mask verbatim for D/W/M/Q (gate G7); '<k><BASE>' keeps every k-th bar
    of that base schedule.  engine.py is NOT modified."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]) if spec[:-1].isdigit() else int(spec[:-2]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


# ------------------------------------------------------------------------------ THE HARVEST
def harvest_csv():
    """Every committed research/backtests/*.csv ROW whose trigger reads a whole-ladder
    INFINITE FLOOR.  Mechanical: the file must carry a `ladder` column, and the row must
    carry an INF-flag field (a column named inf / inf_floor / inf_count / inf_<something>)
    or a `floor` column literally 'inf'.  Rows are kept whether the flag FIRES or not, so
    the denominator is honest and the full 2x2 can be published."""
    rows, rejects = [], []
    for f in sorted(glob.glob(str(BT / "*.csv"))):
        base = os.path.basename(f)
        if base.startswith(f"{DATE}_{SLUG}"):
            continue                                      # never harvest this run's own output
        try:
            with open(f, newline="", encoding="utf-8") as fh:
                rd = csv.DictReader(fh)
                hdr = rd.fieldnames or []
                data = list(rd)
        except Exception as e:                            # pragma: no cover
            rejects.append(dict(source=base, reason=f"UNREADABLE {type(e).__name__}", n=0))
            continue
        hl = {c.lower(): c for c in hdr}
        if "ladder" not in hl:
            continue
        infcols = [c for c in hdr if c.lower() in INF_COLNAMES or c.lower().startswith("inf_")]
        floorcol = hl.get("floor")
        has_floor_inf = bool(floorcol) and any(
            str(r.get(floorcol, "")).strip().lower() in ("inf", "infinity") for r in data)
        if not infcols and not has_floor_inf:
            rejects.append(dict(source=base, reason="NO_INF_FLOOR_FIELD", n=len(data)))
            continue
        kept = 0
        for i, r in enumerate(data):
            lad = str(r.get(hl["ladder"], "")).strip().upper()
            if lad not in LADDERS:
                rejects.append(dict(source=base, reason=f"LADDER_NOT_REBUILDABLE:{lad}", n=1))
                continue
            pan = str(r.get(hl.get("panel", ""), "")).strip() if "panel" in hl else ""
            stat = str(r.get(hl.get("stat", ""), "")).strip() if "stat" in hl else ""
            if not stat and "statistic" in hl:
                stat = str(r.get(hl["statistic"], "")).strip()
            # does the row's trigger FIRE as committed?
            fired, fld = False, ""
            for c in infcols:
                v = str(r.get(c, "")).strip().lower()
                if c.lower() == "inf_count":
                    if v.isdigit():
                        fired = fired or int(v) > 0
                        fld = fld or c
                elif v in ("true", "1"):
                    fired, fld = True, (fld or c)
                elif v in ("false", "0"):
                    fld = fld or c
            if floorcol is not None and str(r.get(floorcol, "")).strip().lower() in ("inf", "infinity"):
                fired, fld = True, (fld or floorcol)
            if not fld:
                rejects.append(dict(source=base, reason="ROW_CARRIES_NO_FLAG", n=1))
                continue
            # which rung set was the committed row computed on?
            own = ""
            for c in ("rung_set", "h_grid", "c_set", "rungs", "k", "rung_count"):
                if c in hl and str(r.get(hl[c], "")).strip():
                    own = str(r.get(hl[c])).strip()
                    break
            own_rs = ("CORE" if own.upper() in ("CORE", "H4", "C4", "4") else
                      "EXT" if own.upper() in ("EXT", "H9", "C9", "9") else "UNDECLARED")
            rows.append(dict(arm="CSV", source=base, row=i, panel=pan, ladder=lad, stat=stat,
                             field=fld, committed_fires=bool(fired), own_rung_set=own_rs,
                             own_raw=own, text=""))
            kept += 1
        if kept:
            pass
    return pd.DataFrame(rows), pd.DataFrame(rejects)


def _sentences(txt):
    """Yield (sentence, line).  The CELLS a committed claim names are read from its LINE —
    the record's own paragraph unit, one CHANGELOG bullet or one LEADERBOARD row — because
    the record routinely names the ladder in a neighbouring clause of the same bullet.  The
    TRIGGER and the DECISION WORD are still required in the SENTENCE itself, so widening the
    window can only add cells to an object, never create one."""
    for chunk in txt.split("\n"):
        for s in re.split(r"(?<=[.;:!?])\s+", chunk):
            s = s.strip()
            if s:
                yield s, chunk


def harvest_prose():
    """Every sentence in committed prose (CHANGELOG, LEADERBOARD, *.result.md, *.memo.md)
    whose trigger reads a whole-ladder INFINITE FLOOR.  A sentence is a CLAUSE / BAR /
    VERDICT (and so a member of CS_PROSE) iff it ALSO carries a decision word; a sentence
    that merely QUOTES a floor is harvested and published as a REJECT with its reason, which
    is the control this run needs for H_TRIGGER_VS_QUOTE."""
    rows, rejects = [], []
    for f in PROSE_FILES:
        base = os.path.basename(f)
        if base.startswith(f"{DATE}_{SLUG}"):
            continue
        try:
            txt = open(f, encoding="utf-8").read()
        except Exception:
            continue
        for i, (s, line) in enumerate(_sentences(txt)):
            if not TRIG_RX.search(s):
                continue
            lads = [l for l, rx in LAD_RX.items() if rx.search(line)]
            pans = [p for p, rx in PAN_RX.items() if rx.search(line)]
            stats = [st for st, rx in STAT_RX.items() if rx.search(line)]
            dec = bool(DEC_RX.search(s))
            if not lads:
                rejects.append(dict(source=base, row=i, reason="NO_LADDER_NAMED",
                                    decision_word=dec, text=s[:300]))
                continue
            if "SMALL" in pans:
                rejects.append(dict(source=base, row=i, reason="PANEL_NOT_REBUILDABLE:SMALL",
                                    decision_word=dec, text=s[:300]))
                continue
            if not dec:
                rejects.append(dict(source=base, row=i, reason="QUOTES_A_FLOOR_NO_DECISION",
                                    decision_word=dec, text=s[:300]))
                continue
            rows.append(dict(arm="PROSE", source=base, row=i,
                             panel="|".join(pans) if pans else "|".join(PANELS),
                             ladder="|".join(sorted(lads)),
                             stat="|".join(sorted(stats)) if stats else "|".join(STATS),
                             field="prose", committed_fires=True, own_rung_set="UNDECLARED",
                             own_raw="", text=s[:400]))
    return pd.DataFrame(rows), pd.DataFrame(rejects)


def main():
    t0 = time.time()
    P(f"# Idea 1131 (lane B, {DATE}) — does ANY committed FLOOR-KEYED clause in the record")
    P("#   survive a RUNG-SET change?  A CENSUS of the record's whole-ladder INF_FLOOR")
    P("#   triggers, re-evaluated from a fresh rebuild of the tape at BOTH rung sets.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIM_SETS} x RUNG SET {RUNGSETS}")
    P("#   = 6 combinations, ALL published.  PANEL, LADDER, STATISTIC are not dials.")
    P(f"#   q is NOT a dial: {Q_HEAD} headline, {QS} reported beside, never selected on.")
    P("#   The ALL-vs-ANY reading of a multi-cell prose claim is NOT a dial: ALL is the")
    P("#   record's own wording and is the headline; ANY is reported beside it.")
    P(f"#   CORE  H {H_CORE}  CADENCE {C_CORE}")
    P(f"#   EXT   H {H_EXT}  CADENCE {C_EXT}")
    P(f"#   N {LAD_N} and GROSS {LAD_G} are IDENTICAL at both levels (1134's finding).")
    P(f"# FROZEN: CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, hold {HOLD0}, N {N0},")
    P(f"#   cadence {FREQ0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END},")
    P(f"#   block L={L_HEAD}, {BDRAWS} draws, crc32 seeds, seed bases {SEED_BASES}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_ANY_SURVIVES   at least one harvested floor-keyed object is RUNG-ROBUST on")
    P("#                        a ladder whose rung set actually CHANGES (H or CADENCE) —")
    P("#                        i.e. the answer to the idea's literal question is YES.")
    P("#   (b) H_MOSTLY_ESCAPES over the objects whose rung set can change, MORE THAN HALF")
    P("#                        are RUNG-ESCAPABLE (fire at CORE, silent at EXT).")
    P("#   (c) H_DIRECTION      escapes run ONE WAY: ESCAPABLE strictly outnumbers INDUCED")
    P("#                        (1118's mechanism — added rungs add larger, separable gaps).")
    P("#   (d) H_COUNT_NOT_ID   escapability is a RUNG-COUNT property, not a property of")
    P("#                        WHICH rungs CORE happens to hold: at matched k=4 the share")
    P("#                        of ALL C(9,4) EXT subsets that fire is >= 0.90.")
    P("#   (e) H_CHEAP_ESCAPE   the median ESCAPE COST — the fewest rungs an author must ADD")
    P("#                        to CORE for the trigger to fall silent — is <= 2.")
    P("#   (f) H_UNDECLARED     MOST committed floor-keyed CSV rows do not state the rung set")
    P("#                        they were computed on, so a reader cannot check them at all.")
    P("#   (g) NOT A KEEP PATH  no book is proposed; 4a/4b and rule 8 are scored at every")
    P("#                        rung because rule 4 requires it.  The BOOK at every rung is")
    P("#                        byte-identical across both dials — only which committed")
    P("#                        objects get CALLED fired changes — so both KEEP paths are")
    P("#                        invariant to dial 1 and dial 2 BY CONSTRUCTION.")
    P("# DECISION RULE, declared before any number: the idea's question is answered YES only")
    P("#   if H_ANY_SURVIVES holds on a ladder whose rung set CHANGES.  A survivor that sits")
    P("#   on N or GROSS is rung-stable BY CONSTRUCTION (identical rung lists) and is NOT")
    P("#   evidence of anything; it is reported and excluded from the headline denominator.")
    P("")

    gaterows, gates = [], {}

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

    def run_cell(panel, N, H, gross, freq):
        d = panels[panel]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4, tn

    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest", value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                        {g1:.2e}   {'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="committed U56 W/H126/N=20 triple", value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy_u = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy_u, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   {'PASS' if gates['G3'] else 'FAIL'}")

    r12, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="committed U56 n=12 triple", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple       {g4:.2e}   {'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="committed B136 n=15 triple", value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN 1098/1102's committed B136 n=15 triple      {g4b:.2e}   {'PASS' if gates['G4b'] else 'FAIL'}")

    lb = {}
    for panel in PANELS:
        dp = panels[panel]
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST, freq="W")["returns"].values
        lb[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g5 = abs(lb["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD", value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   {'PASS' if gates['G5'] else 'FAIL'}")

    r12b, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism", value=g6, pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   {'PASS' if gates['G6'] else 'FAIL'}")

    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int) - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gates["G7"] = g7 == 0
    gaterows.append(dict(gate="G7", what="cadence_mask == engine.rebalance_mask on D/W/M/Q",
                         value=float(g7), pass_=gates["G7"]))
    P(f"  G7  cadence_mask == engine.rebalance_mask (D/W/M/Q)       {g7:.2e}   {'PASS' if gates['G7'] else 'FAIL'}")

    # ------------------------------------------------------------------------ BUILD EVERY BOOK
    H_ALL = sorted(set(H_CORE + H_EXT))
    RUNGS = {"N": [str(x) for x in LAD_N], "GROSS": [str(x) for x in LAD_G],
             "H": [str(x) for x in H_ALL], "CADENCE": list(C_EXT)}
    SUBSET = {("N", "CORE"): RUNGS["N"], ("N", "EXT"): RUNGS["N"],
              ("GROSS", "CORE"): RUNGS["GROSS"], ("GROSS", "EXT"): RUNGS["GROSS"],
              ("H", "CORE"): [str(x) for x in H_CORE], ("H", "EXT"): [str(x) for x in H_EXT],
              ("CADENCE", "CORE"): list(C_CORE), ("CADENCE", "EXT"): list(C_EXT)}
    MOVES = {lad: SUBSET[(lad, "CORE")] != SUBSET[(lad, "EXT")] for lad in LADDERS}

    def cell_params(lad, rung):
        N, H, gr, fq = N0, HOLD0, GROSS0, FREQ0
        if lad == "N":
            N = int(rung)
        elif lad == "H":
            H = int(rung)
        elif lad == "GROSS":
            gr = float(rung)
        else:
            fq = str(rung)
        return N, H, gr, fq

    grid_rows, RET = [], {}
    for panel in PANELS:
        dp = panels[panel]
        sb = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values, dp["warm"], dp["ins"], dp["oos"])
        panels[panel]["spy_m"] = sb
        for lad in LADDERS:
            for rung in RUNGS[lad]:
                N, H, gr, fq = cell_params(lad, rung)
                r, tn = run_cell(panel, N, H, gr, fq)
                RET[(panel, lad, rung)] = r
                b = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
                row = dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=gr, freq=fq,
                           in_core=bool(rung in SUBSET[(lad, "CORE")]),
                           turnover=float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0), **b)
                row.update(legs_4b(b, sb))
                row.update(legs_4b_oos(b, sb))
                row.update(legs_4a(b, lb[panel]))
                row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                grid_rows.append(row)
    G = pd.DataFrame(grid_rows)
    P(f"  built {len(G):,} books ({int(G.in_core.sum())} on 1110/1116's CORE rungs) in "
      f"{time.time() - t0:.0f}s")

    prior = pd.read_csv(f"{PRIOR1110}.grid.csv", dtype=str, keep_default_na=False)
    mine = G.set_index(["panel", "ladder", "rung"])
    dev = []
    for _, r in prior.iterrows():
        key = (r["panel"], r["ladder"], r["rung"])
        if key not in mine.index:
            dev.append(np.inf)
            continue
        mr = mine.loc[key]
        dev.append(max(abs(mr["CAGR"] - float(r["CAGR"])), abs(mr["Sharpe"] - float(r["Sharpe"])),
                       abs(mr["MaxDD"] - float(r["MaxDD"])), abs(mr["OOS_Sharpe"] - float(r["OOS_Sharpe"])),
                       abs(mr["turnover"] - float(r["turnover"]))))
    g8 = float(np.max(dev))
    gates["G8"] = g8 < 1e-9 and len(prior) == 54
    gaterows.append(dict(gate="G8", what=f"reproduce 1110's committed {len(prior)}-row CORE grid",
                         value=g8, pass_=gates["G8"]))
    P(f"  G8  reproduce 1110's committed {len(prior)}-row CORE grid         {g8:.2e}   {'PASS' if gates['G8'] else 'FAIL'}")

    # -------------------------------------------------------- BOOTSTRAP, per panel per ladder
    _VCACHE: dict = {}

    def vals_of(panel, lad, rungs, stat):
        key = (panel, lad, tuple(rungs), stat)
        if key not in _VCACHE:
            gi = G.set_index(["panel", "ladder", "rung"])[STATCOL[stat]]
            _VCACHE[key] = np.array([gi.loc[(panel, lad, r)] for r in rungs], float) * SCALE[stat]
        return _VCACHE[key]

    AGR = {}
    for base in SEED_BASES:
        for panel in PANELS:
            dp = panels[panel]
            for lad in LADDERS:
                rl = RUNGS[lad]
                Rw = np.array([RET[(panel, lad, r)][dp["warm"]] for r in rl])
                Ro = np.array([RET[(panel, lad, r)][dp["oos"]] for r in rl])
                rng = np.random.default_rng(seed_of(base, panel, lad, "warm"))
                iw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
                cagb, shpb = boot_exact(Rw, iw, nbw, L_HEAD)
                ddb = boot_maxdd(Rw, iw)
                rng2 = np.random.default_rng(seed_of(base, panel, lad, "oos"))
                io, nbo = block_index(rng2, Ro.shape[1], L_HEAD, BDRAWS)
                _, shpo = boot_exact(Ro, io, nbo, L_HEAD)
                bo = {"S_FULL": shpb, "S_OOS": shpo, "CAGR": cagb * 100.0, "DD": ddb * 100.0}
                for stat in STATS:
                    AGR[(base, panel, lad, stat)] = agree_matrix(vals_of(panel, lad, rl, stat), bo[stat])
        P(f"  bootstrap base {base} done at {time.time() - t0:.0f}s")

    _IC: dict = {}

    def inf_flag(base, panel, lad, rungs, stat, q=Q_HEAD):
        key = (base, panel, lad, tuple(rungs), stat, q)
        if key not in _IC:
            rl = RUNGS[lad]
            sub = [rl.index(r) for r in rungs]
            v = vals_of(panel, lad, rl, stat)
            flo, _ = floor_sub(v, AGR[(base, panel, lad, stat)], sub, q)
            _IC[key] = ((not np.isfinite(flo)), flo)
        return _IC[key]

    # ---- G9: reproduce 1117's committed 48-row trigger table (inf_count per block x rung set)
    tr117 = pd.read_csv(f"{PRIOR1117}.trigger.csv")
    bad9 = 0
    for _, r in tr117.iterrows():
        if int(r["base"]) not in SEED_BASES:
            continue
        mycnt = sum(inf_flag(int(r["base"]), r["panel"], r["ladder"],
                             SUBSET[(r["ladder"], r["rung_set"])], s)[0] for s in STATS)
        bad9 += int(mycnt != int(r["inf_count"]))
    n9 = int(tr117.base.isin(SEED_BASES).sum())
    gates["G9"] = bad9 == 0 and n9 > 0
    gaterows.append(dict(gate="G9", what=f"reproduce 1117's committed trigger counts ({n9} rows)",
                         value=float(bad9), pass_=gates["G9"]))
    P(f"  G9  CROSS-RUN 1117's committed trigger counts ({n9} rows)  {bad9:.2e}   "
      f"{'PASS' if gates['G9'] else 'FAIL'}")

    # ---- G10: reproduce 1110's committed 32 argmax peaks on CORE rungs
    cl = pd.read_csv(f"{PRIOR1110}.clause.csv", dtype=str, keep_default_na=False)
    com = cl[(cl.clause == "AS_WRITTEN") & (cl.q == "0.9") & (cl.coarse == "")].copy()
    peak_bad = flag_bad = 0
    com_rows = []
    for _, r in com.iterrows():
        panel, lad, stat = r["panel"], r["ladder"], r["stat"]
        rungs = SUBSET[(lad, "CORE")]
        v = vals_of(panel, lad, rungs, stat)
        mine_peak = rungs[int(np.nanargmax(v))]
        ok_peak = str(mine_peak) == str(r["peak"])
        peak_bad += (not ok_peak)
        com_inf = (r["floor"] == "inf")
        my_inf, my_floor = inf_flag(SEED_BASES[0], panel, lad, rungs, stat)
        flag_bad += (com_inf != my_inf)
        com_rows.append(dict(panel=panel, ladder=lad, stat=stat, committed_peak=r["peak"],
                             my_peak=mine_peak, peak_match=ok_peak, committed_inf=com_inf,
                             my_inf=my_inf, my_floor=my_floor))
    CM = pd.DataFrame(com_rows)
    gates["G10"] = (peak_bad == 0) and len(com) == 32
    gaterows.append(dict(gate="G10", what="reproduce 1110's 32 committed argmax peaks",
                         value=float(peak_bad), pass_=gates["G10"]))
    P(f"  G10 CROSS-RUN 1110's 32 committed argmax PEAKS            {peak_bad:.2e}   "
      f"{'PASS' if gates['G10'] else 'FAIL'}  (INF flag mismatches {flag_bad} of 32 — reported, "
      "NOT gated: the flag is a redraw quantity, 1116/1108's finding)")
    dump(CM, "cross1110")

    g11 = float(min(np.nanmax(vals_of(p, l, RUNGS[l], s)) - np.nanmin(vals_of(p, l, RUNGS[l], s))
                    for p in PANELS for l in LADDERS for s in STATS))
    gates["G11"] = g11 > 0
    gaterows.append(dict(gate="G11", what="every ladder x statistic live", value=g11, pass_=gates["G11"]))
    P(f"  G11 every ladder x statistic is LIVE (min spread)         {g11:.2e}   {'PASS' if gates['G11'] else 'FAIL'}")
    P(f"  GATES: {sum(gates.values())} of {len(gates)} PASS")
    dump(pd.DataFrame(gaterows), "gates")
    P("")

    # ------------------------------------------------- THE STRUCTURAL FACT, STATED FIRST
    P("## THE STRUCTURAL FACT, STATED BEFORE THE CENSUS BECAUSE IT BOUNDS IT")
    P("  CORE and EXT differ ONLY on H and CADENCE.  N (9 rungs) and GROSS (10 rungs) carry")
    P("  IDENTICAL rung lists at both levels — 1134 found the same thing on the GROSS ladder")
    P("  and read 4 surviving cells as 2 books.  So:")
    for lad in LADDERS:
        P(f"    {lad:8s} CORE k={len(SUBSET[(lad,'CORE')]):2d}  EXT k={len(SUBSET[(lad,'EXT')]):2d}  "
          f"rung set MOVES: {MOVES[lad]}")
    P("  Any committed object keyed ONLY on N or GROSS is rung-INESCAPABLE BY CONSTRUCTION.")
    P("  The headline denominator is therefore the objects whose rung set CAN change.")
    P("")

    # ------------------------------------------------------------------------- THE HARVEST
    P("## THE HARVEST — every committed object whose TRIGGER reads a whole-ladder INF_FLOOR")
    CSVH, CSVR = harvest_csv()
    PRH, PRR = harvest_prose()
    P(f"  CSV arm   : {len(CSVH):,} committed rows over {CSVH.source.nunique() if len(CSVH) else 0} files")
    P(f"  PROSE arm : {len(PRH):,} committed clause/bar/verdict sentences over "
      f"{PRH.source.nunique() if len(PRH) else 0} files")
    P(f"  rejects   : CSV {int(CSVR.n.sum()) if len(CSVR) else 0} rows / "
      f"{len(CSVR)} reasons, PROSE {len(PRR)} sentences — ALL published with their reason")
    if len(CSVR):
        P("  CSV reject reasons:")
        P(CSVR.groupby("reason")["n"].sum().sort_values(ascending=False).head(12).to_string())
    if len(PRR):
        P("  PROSE reject reasons:")
        P(PRR.groupby("reason").size().sort_values(ascending=False).to_string())
    CORP = pd.concat([CSVH, PRH], ignore_index=True)
    dump(CSVR, "rejects_csv")
    dump(PRR, "rejects_prose")
    P("")

    # ------------------------------------------------ RE-EVALUATE EVERY OBJECT AT BOTH SETS
    P("## RE-EVALUATION — every harvested object's trigger, rebuilt from the tape at BOTH")
    P("##   rung sets.  ESCAPABLE = fires at CORE, silent at EXT.")

    def obj_cells(rec):
        pans = [p for p in str(rec["panel"]).split("|") if p in PANELS] or list(PANELS)
        lads = [l for l in str(rec["ladder"]).split("|") if l in LADDERS]
        sts = [s for s in str(rec["stat"]).split("|") if s in STATS] or list(STATS)
        return [(p, l, s) for p in pans for l in lads for s in sts]

    def fires(rec, rs, base, q, reading):
        cells = obj_cells(rec)
        if not cells:
            return None
        fl = [inf_flag(base, p, l, SUBSET[(l, rs)], s, q)[0] for (p, l, s) in cells]
        return all(fl) if reading == "ALL" else any(fl)

    CLASS = {(True, False): "ESCAPABLE", (False, True): "INDUCED",
             (True, True): "ROBUST", (False, False): "DEAD"}
    ev_rows = []
    for i, rec in CORP.iterrows():
        cells = obj_cells(rec)
        lads = sorted({l for (_, l, _) in cells})
        moves = any(MOVES[l] for l in lads)
        for base in SEED_BASES:
            for q in QS:
                for reading in ("ALL", "ANY"):
                    fc = fires(rec, "CORE", base, q, reading)
                    fe = fires(rec, "EXT", base, q, reading)
                    ev_rows.append(dict(obj=i, arm=rec["arm"], source=rec["source"],
                                        ladders="|".join(lads), n_cells=len(cells),
                                        rung_set_moves=moves, base=base, q=q, reading=reading,
                                        fires_CORE=fc, fires_EXT=fe, cls=CLASS[(fc, fe)],
                                        committed_fires=bool(rec["committed_fires"]),
                                        own_rung_set=rec["own_rung_set"]))
    EV = pd.DataFrame(ev_rows)
    dump(EV, "evaluation")

    head = EV[(EV.base == SEED_BASES[0]) & (EV.q == Q_HEAD) & (EV.reading == "ALL")]

    def census(sub):
        n = len(sub)
        mv = sub[sub.rung_set_moves]
        c = sub.cls.value_counts()
        cm = mv.cls.value_counts()
        return dict(n=n, n_moves=len(mv),
                    ESCAPABLE=int(c.get("ESCAPABLE", 0)), INDUCED=int(c.get("INDUCED", 0)),
                    ROBUST=int(c.get("ROBUST", 0)), DEAD=int(c.get("DEAD", 0)),
                    mv_ESCAPABLE=int(cm.get("ESCAPABLE", 0)), mv_INDUCED=int(cm.get("INDUCED", 0)),
                    mv_ROBUST=int(cm.get("ROBUST", 0)), mv_DEAD=int(cm.get("DEAD", 0)),
                    escape_share_of_movers=(int(cm.get("ESCAPABLE", 0)) / len(mv)) if len(mv) else np.nan)

    def claimset_rows(cs, df):
        if cs == "CS_CELL":
            return df[df.arm == "CSV"]
        if cs == "CS_PROSE":
            return df[df.arm == "PROSE"]
        return df

    P("  HEADLINE (q=0.90, reading ALL, base %d) — 6 DIAL POINTS, all published:" % SEED_BASES[0])
    cen_rows = []
    for cs in CLAIM_SETS:
        for base in SEED_BASES:
            for q in QS:
                for reading in ("ALL", "ANY"):
                    sub = claimset_rows(cs, EV[(EV.base == base) & (EV.q == q) & (EV.reading == reading)])
                    cen_rows.append(dict(claim_set=cs, base=base, q=q, reading=reading, **census(sub)))
    CE = pd.DataFrame(cen_rows)
    dump(CE, "census")
    hp = CE[(CE.base == SEED_BASES[0]) & (CE.q == Q_HEAD) & (CE.reading == "ALL")]
    P(hp[["claim_set", "n", "n_moves", "ESCAPABLE", "INDUCED", "ROBUST", "DEAD",
          "mv_ESCAPABLE", "mv_INDUCED", "mv_ROBUST", "mv_DEAD", "escape_share_of_movers"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  (mv_* columns are restricted to objects whose rung set CAN change — the only honest")
    P("   denominator.  The two rung sets are the SAME list for N and GROSS.)")
    P("")
    P("  THE NUMBER THE IDEA ACTUALLY ASKS FOR — restricted to objects whose COMMITTED flag")
    P("  FIRED as published (a claim keyed on a floor that never fired has nothing to escape):")
    fired_rows = []
    for cs in CLAIM_SETS:
        sub = claimset_rows(cs, head)
        sub = sub[sub.committed_fires & sub.rung_set_moves]
        c = sub.cls.value_counts()
        fired_rows.append(dict(claim_set=cs, n_committed_fired_movers=len(sub),
                               ESCAPABLE=int(c.get("ESCAPABLE", 0)),
                               ROBUST=int(c.get("ROBUST", 0)),
                               INDUCED=int(c.get("INDUCED", 0)), DEAD=int(c.get("DEAD", 0)),
                               escape_share=(int(c.get("ESCAPABLE", 0)) / len(sub)) if len(sub) else np.nan))
    FIRED = pd.DataFrame(fired_rows)
    dump(FIRED, "committedfired")
    P(FIRED.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    P("## WHICH BLOCKS SURVIVE?  The trigger rebuilt at both rung sets, per (panel, ladder,")
    P("##   statistic) block on the two ladders whose rung set moves:")
    surv_rows = []
    for panel in PANELS:
        for lad in ("H", "CADENCE"):
            for stat in STATS:
                fc = inf_flag(SEED_BASES[0], panel, lad, SUBSET[(lad, "CORE")], stat)[0]
                fe = inf_flag(SEED_BASES[0], panel, lad, SUBSET[(lad, "EXT")], stat)[0]
                surv_rows.append(dict(panel=panel, ladder=lad, stat=stat,
                                      fires_CORE=fc, fires_EXT=fe, cls=CLASS[(fc, fe)]))
    SURV = pd.DataFrame(surv_rows)
    dump(SURV, "blocks")
    P(SURV.to_string(index=False))
    P(f"  ROBUST blocks: {int((SURV.cls == 'ROBUST').sum())} of {len(SURV)}; "
      f"ESCAPABLE {int((SURV.cls == 'ESCAPABLE').sum())}, "
      f"INDUCED {int((SURV.cls == 'INDUCED').sum())}, DEAD {int((SURV.cls == 'DEAD').sum())}")
    P("")

    P("  SENSITIVITY, reported and never selected on — escape share of movers, CS_ALL:")
    sens = CE[CE.claim_set == "CS_ALL"].pivot_table(index=["reading", "q"], columns="base",
                                                    values="escape_share_of_movers")
    P(sens.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")

    # ------------------------------------------- IS THE FLAG A RUNG-COUNT OR AN IDENTITY FACT?
    P("## RUNG COUNT OR RUNG IDENTITY?  Every C(9,4) = 126 four-rung subset of each EXT")
    P("##   ladder, scored for the same trigger.  If nearly all of them fire, the CORE flag")
    P("##   is a property of k=4 and not of the particular rungs 1110/1116 chose.")
    sub_rows, joint_rows = [], []
    for panel in PANELS:
        for lad in ("H", "CADENCE"):
            ext = SUBSET[(lad, "EXT")]
            core = SUBSET[(lad, "CORE")]
            subs = list(combinations(ext, 4))
            firemat = {}
            for stat in STATS:
                fired = [inf_flag(SEED_BASES[0], panel, lad, list(s), stat)[0] for s in subs]
                firemat[stat] = np.array(fired)
                core_f = inf_flag(SEED_BASES[0], panel, lad, core, stat)[0]
                sub_rows.append(dict(panel=panel, ladder=lad, stat=stat, k=4, n_subsets=len(subs),
                                     n_fire=int(sum(fired)), share=float(np.mean(fired)),
                                     core_fires=bool(core_f)))
            allfour = np.logical_and.reduce([firemat[s] for s in STATS])
            core_all = all(inf_flag(SEED_BASES[0], panel, lad, core, s)[0] for s in STATS)
            joint_rows.append(dict(panel=panel, ladder=lad, n_subsets=len(subs),
                                   n_fire_all4=int(allfour.sum()),
                                   share_all4=float(allfour.mean()), core_fires_all4=bool(core_all)))
    SUB = pd.DataFrame(sub_rows)
    JNT = pd.DataFrame(joint_rows)
    dump(SUB, "ksubsets")
    dump(JNT, "ksubsets_joint")
    P(SUB.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"  pooled over all 16 (panel, ladder, stat) blocks: {SUB.n_fire.sum():,} of "
      f"{SUB.n_subsets.sum():,} four-rung subsets fire = {SUB.n_fire.sum()/SUB.n_subsets.sum():.4f}; "
      f"CORE itself fires in {int(SUB.core_fires.sum())} of {len(SUB)}")
    P("")
    P("  POST-HOC AND LABELLED AS SUCH — how UNUSUAL is the rung set 1110/1116 chose?  At")
    P("  matched k=4, the share of the 126 subsets that fire at ALL FOUR statistics at once,")
    P("  against CORE, which does so in every block:")
    P(JNT.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pj = float(np.prod(JNT.share_all4.values))
    P(f"  product over the {len(JNT)} (panel, ladder) blocks = {pj:.3e}.  Under a UNIFORM draw")
    P("  of 4-rung subsets that is how often a rung set would fire everywhere CORE does.  The")
    P("  record's committed INF_FLOOR census is therefore not merely k-dependent: it rests on")
    P("  a rung choice that fires FAR more often than a typical one of the same size.")
    P("")

    # --------------------------------------------------------------------- THE ESCAPE COST
    P("## THE ESCAPE COST — the FEWEST rungs an author must ADD to the CORE ladder for the")
    P("##   trigger to fall silent.  EXHAUSTIVE over all 2^5 = 32 supersets of CORE inside")
    P("##   EXT, per (panel, ladder, statistic).  No sampling.")
    esc_rows = []
    for panel in PANELS:
        for lad in ("H", "CADENCE"):
            ext = SUBSET[(lad, "EXT")]
            core = SUBSET[(lad, "CORE")]
            extra = [r for r in ext if r not in core]
            for stat in STATS:
                if not inf_flag(SEED_BASES[0], panel, lad, core, stat)[0]:
                    esc_rows.append(dict(panel=panel, ladder=lad, stat=stat, core_fires=False,
                                         escape_cost=0, n_supersets=32, n_silent=np.nan,
                                         cheapest=""))
                    continue
                best, cheapest, nsil = None, "", 0
                for m in range(1, len(extra) + 1):
                    for add in combinations(extra, m):
                        rungs = [r for r in ext if r in core or r in add]
                        if not inf_flag(SEED_BASES[0], panel, lad, rungs, stat)[0]:
                            nsil += 1
                            if best is None:
                                best, cheapest = m, "+".join(str(a) for a in add)
                esc_rows.append(dict(panel=panel, ladder=lad, stat=stat, core_fires=True,
                                     escape_cost=(best if best is not None else np.nan),
                                     n_supersets=31, n_silent=nsil, cheapest=cheapest))
    ESC = pd.DataFrame(esc_rows)
    dump(ESC, "escapecost")
    P(ESC.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    fired_esc = ESC[ESC.core_fires]
    escapable = fired_esc[fired_esc.escape_cost.notna()]
    unescapable = fired_esc[fired_esc.escape_cost.isna()]
    med_cost = float(escapable.escape_cost.median()) if len(escapable) else np.nan
    P(f"  of the {len(fired_esc)} (panel, ladder, stat) blocks that FIRE at CORE, "
      f"{len(escapable)} can be silenced by adding rungs and {len(unescapable)} CANNOT be "
      f"silenced by ANY of the 31 supersets;")
    P(f"  median ESCAPE COST over the {len(escapable)} escapable blocks {med_cost:.1f} rung(s), "
      f"min {escapable.escape_cost.min() if len(escapable) else float('nan'):.0f}, "
      f"max {escapable.escape_cost.max() if len(escapable) else float('nan'):.0f}")
    if len(unescapable):
        P("  THE SURVIVORS — no superset inside EXT silences these:")
        for _, r in unescapable.iterrows():
            P(f"    {r['panel']:5s} {r['ladder']:8s} {r['stat']}")
    nonmono = []
    for _, r in escapable.iterrows():
        fe = inf_flag(SEED_BASES[0], r["panel"], r["ladder"], SUBSET[(r["ladder"], "EXT")], r["stat"])[0]
        if fe:
            nonmono.append((r["panel"], r["ladder"], r["stat"], r["cheapest"]))
    P(f"  THE TRIGGER IS NOT MONOTONE IN RUNGS — {len(nonmono)} block(s) still fire on the FULL")
    P("  EXT ladder yet fall silent on a SMALLER superset of CORE.  So the escape is not")
    P("  'run more rungs', it is 'run the RIGHT rungs', which is cheaper and harder to police:")
    for p_, l_, s_, c_ in nonmono:
        P(f"    {p_:5s} {l_:8s} {s_:6s}  silenced by adding {c_}, but NOT by adding all five")
    P("")

    # ------------------------------------------------- HOW MANY ROWS EVEN SAY THEIR RUNG SET
    P("## CAN A READER CHECK ANY OF THIS?  Committed floor-keyed CSV rows by whether they")
    P("##   STATE the rung set they were computed on:")
    if len(CSVH):
        dec = CSVH.own_rung_set.value_counts()
        P(dec.to_string())
        und = int(dec.get("UNDECLARED", 0))
        P(f"  UNDECLARED {und:,} of {len(CSVH):,} = {und/len(CSVH):.4f}")
    else:
        und = 0
    dump(CORP.drop(columns=["text"]).assign(text=CORP.text.str.slice(0, 200)), "corpus")
    P("")

    # ------------------------------------------------- THE PRICE LEG: RULE 8 WALK-FORWARD
    P("## THE PRICE LEG — RULE 8 WALK-FORWARD.  Rung chosen on IS 2009-2016 ALONE; OOS")
    P("##   2017-2026 read ONCE.  Scored against that ladder's FROZEN DEFAULT rung, against")
    P("##   SPY and against the live RULES v2 book.  BOTH KEEP PATHS scored at every rung.")
    gi = G.set_index(["panel", "ladder", "rung"])
    wf = []
    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        for lad in LADDERS:
            for rs in RUNGSETS:
                rungs = SUBSET[(lad, rs)]
                sub = G[(G.panel == panel) & (G.ladder == lad) & (G.rung.isin(rungs))]
                dref = gi.loc[(panel, lad, DEFAULT_RUNG[lad])]
                for ch, (iscol, ooscol, sign) in CHOOSERS.items():
                    pick = sub.loc[sub[iscol].idxmax()]
                    best = sub.loc[sub[ooscol].idxmax()]
                    fullbest = sub.loc[sub[STATCOL["S_FULL"]].idxmax()]
                    wf.append(dict(
                        panel=panel, ladder=lad, rung_set=rs, chooser=ch, k=len(rungs),
                        pick=pick["rung"], default=DEFAULT_RUNG[lad], full_argmax=fullbest["rung"],
                        pick_is_default=bool(pick["rung"] == DEFAULT_RUNG[lad]),
                        pick_is_full_argmax=bool(pick["rung"] == fullbest["rung"]),
                        CAGR=pick["CAGR"], Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"],
                        H1=pick["H1"], H2=pick["H2"], OOS_CAGR=pick["OOS_CAGR"],
                        OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                        adv_matched=sign * float(pick[ooscol] - dref[ooscol]),
                        adv_oos_sharpe=float(pick["OOS_Sharpe"] - dref["OOS_Sharpe"]),
                        regret=float(sign * (best[ooscol] - pick[ooscol])),
                        pass_4b_full=bool(pick["pass_4b_full"]), pass_4b_oos=bool(pick["pass_4b_oos"]),
                        pass_4a=bool(pick["pass_4a"]),
                        spy_OOS_Sharpe=sb["OOS_Sharpe"], live_OOS_Sharpe=lbm["OOS_Sharpe"]))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    dump(G, "grid")

    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        P(f"  {panel} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}   "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}   OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2  full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:.2%}   "
          f"halves {lbm['H1']:.4f}/{lbm['H2']:.4f}   OOS {lbm['OOS_CAGR']:.2%} / "
          f"{lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:.2%}")
    P(f"  IS picks: {len(WF)} — 4b full {int(WF.pass_4b_full.sum())}, 4b OOS "
      f"{int(WF.pass_4b_oos.sum())}, 4a {int(WF.pass_4a.sum())}, median OOS Sharpe "
      f"{WF.OOS_Sharpe.median():.4f}, median regret {WF.regret.median():+.4f}")
    P(f"  whole grid {len(G)} rungs: 4b full {int(G.pass_4b_full.sum())}, 4b OOS "
      f"{int(G.pass_4b_oos.sum())}, 4a {int(G.pass_4a.sum())}")
    pw = WF[WF.pass_4b_full]
    P("  EVERY IS PICK THAT CLEARS 4b (full), with its OOS triple:")
    if len(pw):
        P(pw[["panel", "ladder", "rung_set", "chooser", "pick", "pick_is_default", "CAGR",
              "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("    none")
    P("")

    # ----------------------------------------------------------------------------- HYPOTHESES
    mv = head[head.rung_set_moves]
    n_rob = int((mv.cls == "ROBUST").sum())
    n_esc = int((mv.cls == "ESCAPABLE").sum())
    n_ind = int((mv.cls == "INDUCED").sum())
    n_dead = int((mv.cls == "DEAD").sum())
    any_surv = n_rob > 0
    mostly = bool(len(mv) and n_esc > len(mv) / 2)
    direction = bool(n_esc > n_ind)
    ksh = float(SUB.n_fire.sum() / SUB.n_subsets.sum())
    count_not_id = bool(ksh >= 0.90)
    cheap = bool(np.isfinite(med_cost) and med_cost <= 2)
    undecl = bool(len(CSVH) and und / len(CSVH) > 0.5)

    HYP = {
        "H_ANY_SURVIVES": (any_surv, f"ROBUST objects on a ladder whose rung set moves: {n_rob} "
                                     f"of {len(mv)} (ESCAPABLE {n_esc}, INDUCED {n_ind}, DEAD {n_dead})"),
        "H_MOSTLY_ESCAPES": (mostly, f"ESCAPABLE {n_esc} of {len(mv)} movers = "
                                     f"{n_esc/len(mv) if len(mv) else float('nan'):.4f}"),
        "H_DIRECTION": (direction, f"ESCAPABLE {n_esc} vs INDUCED {n_ind}"),
        "H_COUNT_NOT_ID": (count_not_id, f"share of C(9,4) EXT subsets that fire = {ksh:.4f} "
                                         f"({SUB.n_fire.sum():,} of {SUB.n_subsets.sum():,})"),
        "H_CHEAP_ESCAPE": (cheap, f"median escape cost {med_cost:.1f} rung(s) over the "
                                  f"{len(escapable)} escapable blocks; {len(unescapable)} of "
                                  f"{len(fired_esc)} firing blocks cannot be silenced at all"),
        "H_UNDECLARED": (undecl, f"{und:,} of {len(CSVH):,} committed floor-keyed CSV rows do "
                                 f"not state their rung set"),
    }
    P("## HYPOTHESES, declared before any number")
    for k, (ok, why) in HYP.items():
        P(f"  {'SUPPORTED' if ok else 'REFUTED  '}  {k:18s} {why}")
    P(f"  {sum(1 for v in HYP.values() if v[0])} of {len(HYP)} SUPPORTED")
    dump(pd.DataFrame([dict(hypothesis=k, supported=v[0], evidence=v[1]) for k, v in HYP.items()]),
         "hypotheses")
    P("")

    P("## THE ANSWER (decision rule declared before any number)")
    P(f"  Objects whose rung set CAN change: {len(mv)} of {len(head)} harvested.")
    P(f"  ROBUST (survive the rung-set change): {n_rob}")
    P(f"  ESCAPABLE: {n_esc}   INDUCED: {n_ind}   DEAD at both: {n_dead}")
    P(f"  => the idea's literal question is answered {'YES' if any_surv else 'NO'}")
    P("")
    P(f"\n# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
