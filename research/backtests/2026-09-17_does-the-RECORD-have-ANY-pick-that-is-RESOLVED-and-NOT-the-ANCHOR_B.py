#!/usr/bin/env python3
"""Idea 1233 (lane B, 2026-09-17)
   does-the-RECORD-have-ANY-pick-that-is-RESOLVED-and-NOT-the-ANCHOR

THE QUEUE'S PREMISE, QUOTED.  Idea 1209 found all 4 resolved picks in a 168-pick census name
rung GROSS=0.75, which IS the anchor's gross (gate G3: N=20 / H=126 / GROSS=0.75 / CADENCE=W
are one book bit for bit), at an IS Sharpe gap of 0.0004.  A chooser acting only on resolved
picks is therefore the do-nothing rule BY MEASUREMENT.  The queue asks for EVERY committed
resolved / decisive pick in the record to be harvested, for each destination to be tested
against its anchor on the REALISED-RETURN key (1211's B_VALUE), and for the count of
non-anchor resolved picks to be published.

WHY THE IDENTITY KEY IS THE WHOLE QUESTION.  "The pick is not the anchor" is a claim about
LABELS: rung 0.75 on the GROSS ladder is a different string from rung 0.75 on nothing at all,
and a pick that names the anchor's own rung is trivially the anchor.  But two DIFFERENT labels
can also be one book -- a min-hold H that never binds, a cadence the mask never separates --
so a label-different pick need not be a different portfolio either.  This run prices every
harvested destination and every harvested anchor as a BOOK and asks the question three ways:
by label, by bit-identical realised net return vector (B_VALUE), and by that vector rounded to
1e-9 (B_VALUE_RD).

TUNED DIALS (2, PROTOCOL rule 4) -- and the queue names both:

  `CLAIM SET`     S_STRICT  rows whose source file carries an EXPLICIT committed resolution
                            boolean (resolved / decided / decisive / resolved_boot /
                            own_resolved / transfer_resolved / resolvable).
                  S_PROXY   rows whose file carries no such boolean but does carry the
                            record's own resolution ARITHMETIC (p_boot, margin+se, gap+floor,
                            gap+largest_unresolved, sigmas, t), re-applied at the record's own
                            published bars (below).
                  S_ALL     the union.
  `IDENTITY KEY`  B_LABEL / B_VALUE / B_VALUE_RD (above).
  = 9 cells, EVERY ONE PUBLISHED in `.dialgrid.csv` and printed in ARM 3.

  NOT dials, reported at every value: PANEL {U56, B136, SMALL}; ANCHOR CONTEXT {CTX_A, CTX_B}
  and, where a harvested row names its own `anchor_rung`, that rung; the four mappable ladders
  {N, H, GROSS, CADENCE} and every rung harvested on them; the acting rules of ARM 4; the 4a
  and 4b legs; the rule-8 arm's three choosers.

  THE PROXY BARS ARE THE RECORD'S OWN, NOT NEW DIALS: p_boot <= 0.10 (1154's memo / 1210-cloud
  90th-percentile non-certifying bar), |margin| / se > 1.9600, gap > floor, gap >
  largest_unresolved, |sigmas| > 1.9600, |t| > 1.9600, and bare `margin` > 0.013 (the record's
  own "013 margin rule", 2026-09-08).  Each row publishes WHICH bar decided it.

DECLARED BEFORE ANY NUMBER (see ARM 0).
  H_ANCHOR : every resolved pick in the record collapses to its own anchor under B_VALUE --
             the non-anchor resolved count is 0 in all 9 cells.  A single resolved non-anchor
             pick REFUTES this and is a real finding.
  H_LABEL  : the LABEL key finds strictly MORE non-anchor resolved picks than B_VALUE, i.e.
             part of the record's non-anchor count is a labelling fact and not a book fact.
  H_DONOTHING : R_RESOLVED (act only on resolved picks) is not distinguishable from R_ANCHOR
             (do nothing) -- their paired OOS Sharpe gap does not clear 2 of its own block
             bootstrap SE.
  H_OOS    : the rule-8 arm's resolved-only chooser does not beat the do-nothing anchor OOS.

ONE ARM WAS ADDED AFTER THE FIRST FULL RUN, AND SAYS SO.  ARM 3b (row-level agreement of the
three identity keys, and each resolved non-anchor pick measured against the ANCHOR's OWN
block-bootstrap SE of Sharpe) was written after the first full run returned identical
non-anchor counts at all three keys and a median |dSharpe| of 0.004 on the largest axis.
Neither test introduces a dial: the key set is ARM 3's own, fixed in ARM 0 before any number,
and the bar is the anchor book's own SE on the record's own block length L = 63.

FROZEN at the 2026-09-04 KEEP-4b candidate's construction: composite = mean of the percentile
ranks of (12-1, 6m, 3m), NO VOL SCALER, eligibility = above own 200d MA and vol20 < 0.60,
top-N equal weight at gross/N of NAV, min hold H, gated-out weight to CASH at 0%, 10 bps per
unit turnover (PROTOCOL rule 2), next-day execution (LAG 1, gate G3), warm-up 260 rows, IS
ends 2016-12-31 and 2017-2026 is read ONCE (PROTOCOL rule 8).

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
current output of a sub-$2B screen (data/SMALL_PANEL_README.md) less the documented
max_1d_move >= 1.0 exclusion.  Harvested rows whose panel label is a SMALL VARIANT (SMALL663,
SMALL439, small) are priced on THIS run's SMALL panel and stamped as such in `.claims.csv`:
the pool is not bit-identical to the pool that produced the committed row, which is a reason
to read the LEVELS as upper bounds, not the identity verdicts, which are differences of two
books drawn from the same pool.

Standalone, deterministic, offline.  Nothing outside research/ is written or modified.
"""
from __future__ import annotations

import csv
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-the-RECORD-have-ANY-pick-that-is-RESOLVED-and-NOT-the-ANCHOR"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_B"

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

CONTEXTS = {                                        # the record's own two anchor contexts
    "CTX_A": dict(N=20, H=126, g=0.75, freq="W"),   # gate G3 anchor (1154, 1209, 1212)
    "CTX_B": dict(N=12, H=63, g=0.55, freq="M"),    # the second context the reach files name
}
AXES = {"N": "N", "H": "H", "GROSS": "g", "CADENCE": "freq"}

# harvest vocabulary ------------------------------------------------------------------
DEST_COLS = ["pick", "pick_rung", "peak", "argmax", "chosen", "choice", "dest", "destination"]
RES_COLS = ["resolved", "decided", "decisive", "resolved_boot", "own_resolved",
            "transfer_resolved", "resolvable"]
LAD_COLS = ["ladder", "axis", "dial", "family", "param"]
PANEL_COLS = ["panel"]
LADDER_MAP = {"N": "N", "L_N": "N", "LAD_N": "N", "n": "N",
              "H": "H", "L_H": "H", "LAD_H": "H", "h": "H", "hold": "H",
              "GROSS": "GROSS", "gross": "GROSS", "L_G": "GROSS", "LAD_GROSS": "GROSS",
              "G": "GROSS", "g": "GROSS",
              "CADENCE": "CADENCE", "cadence": "CADENCE", "L_CAD": "CADENCE",
              "LAD_CADENCE": "CADENCE", "freq": "CADENCE", "C": "CADENCE"}
PANEL_MAP = {"U56": "U56", "u56": "U56", "U": "U56",
             "B136": "B136", "broad": "B136", "B": "B136", "b136": "B136",
             "SMALL": "SMALL", "small": "SMALL", "SMALL663": "SMALL", "SMALL439": "SMALL",
             "SMALL485": "SMALL", "S": "SMALL"}
LEGAL_N = list(range(2, 61))
LEGAL_H = [0, 5, 10, 21, 42, 63, 84, 126, 189, 252, 378, 504, 756]
LEGAL_FREQ = ["D", "W", "M", "Q"]
P_BOOT_BAR, TBAR, MARGIN_BAR = 0.10, 1.9600, 0.013

CLAIMSETS = ["S_STRICT", "S_PROXY", "S_ALL"]
IDENTS = ["B_LABEL", "B_VALUE", "B_VALUE_RD"]

BOOT_B, L_BLOCK = 600, 63
SEED_BASE = 12331233
ROW_CAP = 200_000                       # per-file row cap; every file's usage is published

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


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<64s} {value:.4e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, declared, bar, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, bar=bar, measured=str(measured),
                    supported=bool(supported)))
    P(f"  {name:<12s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


# ================================================================= the record's runner
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


def sharpe_rows(x):
    mu = x.mean(axis=1) * 252.0
    sg = x.std(axis=1, ddof=1) * np.sqrt(252.0)
    return np.where(sg > 0, mu / sg, np.nan)


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


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, ins_m, oos_m):
    c, s, d = fmet(r)
    h = len(r) // 2
    oc, os_, od = fmet(r[oos_m])
    ic, is_, idd = fmet(r[ins_m])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
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


def se_block_diff(ra, rb, tag, L=L_BLOCK):
    """SE of Sharpe(ra) - Sharpe(rb), PAIRED moving-block bootstrap (one index for both)."""
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    T = len(ra)
    rng = np.random.default_rng(seed_of("se", tag, L))
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(BOOT_B, nb))
    idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
    idx = idx.reshape(BOOT_B, nb * L)[:, :T]
    d = sharpe_rows(ra[idx]) - sharpe_rows(rb[idx])
    return float(np.nanstd(d, ddof=1))


def se_block_one(r, tag, L=L_BLOCK):
    """Moving-block bootstrap SE of ONE book's Sharpe (the anchor's own ruler, ARM 3b)."""
    r = np.asarray(r, float)
    T = len(r)
    rng = np.random.default_rng(seed_of("se1", tag, L))
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(BOOT_B, nb))
    idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
    idx = idx.reshape(BOOT_B, nb * L)[:, :T]
    return float(np.nanstd(sharpe_rows(r[idx]), ddof=1))


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# ----------------------------------------------------------------------- harvest helpers
def _f(x):
    try:
        v = float(str(x).strip())
        return v if np.isfinite(v) else None
    except Exception:
        return None


def _b(x):
    s = str(x).strip().lower()
    if s in ("true", "1", "1.0", "yes", "y", "t"):
        return True
    if s in ("false", "0", "0.0", "no", "n", "f"):
        return False
    return None


def parse_rung(axis, raw):
    """Map a committed rung LABEL to a legal value on `axis`, or None if unmappable."""
    s = str(raw).strip()
    if s == "" or s.lower() in ("nan", "none", "inf", "-inf", "na"):
        return None
    if axis == "CADENCE":
        u = s.upper()
        return u if u in LEGAL_FREQ else None
    v = _f(s)
    if v is None:
        return None
    if axis == "N":
        return int(round(v)) if abs(v - round(v)) < 1e-9 and int(round(v)) in LEGAL_N else None
    if axis == "H":
        return int(round(v)) if abs(v - round(v)) < 1e-9 and int(round(v)) in LEGAL_H else None
    if axis == "GROSS":
        return round(v, 4) if 0.05 <= v <= 2.0 else None
    return None


def resolution_of(low, rescols):
    """(resolved, bar_name) for one harvested row.  Explicit boolean first, then the record's
    own published arithmetic.  Returns (None, '') when the row states no resolution at all."""
    for c in rescols:
        b = _b(low.get(c))
        if b is not None:
            return b, f"COL:{c}"
    p = _f(low.get("p_boot_pick", low.get("p_boot")))
    if p is not None:
        return bool(p <= P_BOOT_BAR), "P_BOOT<=0.10"
    m, se = _f(low.get("margin")), _f(low.get("se", low.get("se_pp")))
    if m is not None and se is not None and se > 0:
        return bool(abs(m) / se > TBAR), "|MARGIN|/SE>1.96"
    g, fl = _f(low.get("gap", low.get("gap_pp"))), _f(low.get("floor", low.get("floor_pp")))
    if g is not None and fl is not None:
        return bool(abs(g) > abs(fl)), "GAP>FLOOR"
    lu = _f(low.get("largest_unresolved", low.get("largest_unresolved_gap_pp")))
    if g is not None and lu is not None:
        return bool(abs(g) > abs(lu)), "GAP>LARGEST_UNRESOLVED"
    sg = _f(low.get("sigmas"))
    if sg is not None:
        return bool(abs(sg) > TBAR), "|SIGMAS|>1.96"
    t = _f(low.get("t"))
    if t is not None:
        return bool(abs(t) > TBAR), "|T|>1.96"
    if m is not None:
        return bool(m > MARGIN_BAR), "MARGIN>0.013"
    return None, ""


def harvest():
    """Every committed pick row in research/backtests/*.csv that names a DESTINATION and
    states a RESOLUTION (explicitly, or by the record's own arithmetic)."""
    rows, filelog = [], []
    for f in sorted(HERE.glob("*.csv")):
        if f.name.startswith(f"{DATE}_{SLUG}_B."):
            continue                                  # never harvest this run's own output
        try:
            with f.open(newline="") as fh:
                rd = csv.reader(fh)
                header = next(rd)
        except Exception:
            continue
        hs = [(c or "").strip() for c in header]
        low = [c.lower() for c in hs]
        dest = next((hs[low.index(c)] for c in DEST_COLS if c in low), None)
        if dest is None:
            continue
        rescols = [hs[low.index(c)] for c in RES_COLS if c in low]
        lad = next((hs[low.index(c)] for c in LAD_COLS if c in low), None)
        pan = next((hs[low.index(c)] for c in PANEL_COLS if c in low), None)
        nrow = nstate = nmap = 0
        try:
            with f.open(newline="") as fh:
                for i, row in enumerate(csv.DictReader(fh)):
                    if i >= ROW_CAP:
                        break
                    nrow += 1
                    r = {(k or "").strip().lower(): v for k, v in row.items()}
                    res, bar = resolution_of(r, [c.lower() for c in rescols])
                    if res is None:
                        continue
                    nstate += 1
                    axis = LADDER_MAP.get(str(r.get(lad.lower(), "")).strip()) if lad else None
                    panel_raw = str(r.get(pan.lower(), "")).strip() if pan else ""
                    panel = PANEL_MAP.get(panel_raw)
                    d_raw = r.get(dest.lower(), "")
                    a_raw = r.get("anchor_rung", r.get("anchor", ""))
                    d_val = parse_rung(axis, d_raw) if axis else None
                    a_val = parse_rung(axis, a_raw) if axis else None
                    ctx = "CTX_B" if str(a_raw).strip().upper() == "B" else "CTX_A"
                    if axis and a_val is None:
                        a_val = CONTEXTS[ctx][AXES[axis]]
                        a_src = f"CTX:{ctx}"
                    else:
                        a_src = "ROW"
                    mappable = bool(axis and panel and d_val is not None)
                    nmap += int(mappable)
                    rows.append(dict(file=f.name, dest_col=dest, ladder_col=(lad or ""),
                                     ladder_raw=str(r.get(lad.lower(), "")) if lad else "",
                                     axis=(axis or ""), panel_raw=panel_raw,
                                     panel=(panel or ""), dest_raw=str(d_raw),
                                     dest=("" if d_val is None else d_val),
                                     anchor_raw=str(a_raw), anchor=("" if a_val is None else a_val),
                                     anchor_src=a_src, ctx=ctx,
                                     chooser=str(r.get("chooser", r.get("stat", ""))),
                                     resolved=bool(res), bar=bar,
                                     claimset=("S_STRICT" if bar.startswith("COL:") else "S_PROXY"),
                                     mappable=mappable,
                                     small_variant=bool(panel == "SMALL" and panel_raw != "SMALL")))
        except Exception as e:
            filelog.append(dict(file=f.name, rows=nrow, stated=nstate, mappable=nmap,
                                error=type(e).__name__))
            continue
        if nstate:
            filelog.append(dict(file=f.name, rows=nrow, stated=nstate, mappable=nmap, error=""))
    return pd.DataFrame(rows), pd.DataFrame(filelog)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1233 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P("")

    # ------------------------------------------------------------------ ARM 0: declarations
    P("## ARM 0 — DECLARED BEFORE ANY NUMBER IS COMPUTED")
    P("  H_ANCHOR    : the non-anchor RESOLVED pick count is 0 in all 9 (claim set x identity) cells.")
    P("  H_LABEL     : B_LABEL finds strictly MORE non-anchor resolved picks than B_VALUE.")
    P("  H_DONOTHING : R_RESOLVED's paired OOS Sharpe gap vs R_ANCHOR does not clear 2 of its own")
    P("                block-bootstrap SE (L = 63, B = 600).")
    P("  H_OOS       : the rule-8 resolved-only chooser does not beat the do-nothing anchor OOS.")
    P("  BARS        : explicit committed boolean first; else p_boot <= 0.10, |margin|/se > 1.96,")
    P("                gap > floor, gap > largest_unresolved, |sigmas| > 1.96, |t| > 1.96,")
    P("                bare margin > 0.013.  Every row publishes which bar decided it.")
    P("  IDENTITY    : B_LABEL = same rung label; B_VALUE = bit-identical realised NET daily")
    P("                return vector over the warm-up-stripped sample; B_VALUE_RD = same at 1e-9.")
    P("")

    # ------------------------------------------------------------------ ARM 1: the harvest
    P("## ARM 1 — HARVEST: every committed pick row in the record that states a resolution")
    cl, fl = harvest()
    P(f"  scanned {len(list(HERE.glob('*.csv'))):,} committed CSVs; {len(fl)} state a resolution "
      f"beside a destination")
    P(f"  harvested rows: {len(cl):,}   S_STRICT {int((cl.claimset == 'S_STRICT').sum()):,}   "
      f"S_PROXY {int((cl.claimset == 'S_PROXY').sum()):,}")
    P(f"  mappable to a priceable book: {int(cl.mappable.sum()):,} of {len(cl):,} "
      f"({cl.mappable.mean():.1%});  resolved rows: {int(cl.resolved.sum()):,}")
    P("  UNMAPPABLE BREAKDOWN (published, not dropped silently):")
    un = cl[~cl.mappable]
    if len(un):
        for (ax, pn), n in un.groupby([un.axis.replace("", "AXIS_UNMAPPED"),
                                       un.panel.replace("", "PANEL_UNMAPPED")]).size() \
                             .sort_values(ascending=False).head(12).items():
            P(f"    axis={ax:<18s} panel={pn:<16s} {n:6d}")
    P("  ROWS BY (claim set, axis, panel):")
    for k, n in cl[cl.mappable].groupby(["claimset", "axis", "panel"]).size().items():
        P(f"    {k[0]:<9s} {k[1]:<8s} {k[2]:<6s} {n:6d}")
    P("  BARS USED:")
    for k, n in cl.bar.value_counts().items():
        P(f"    {k:<26s} {n:6d}")
    dump(cl, "claims")
    dump(fl.sort_values("stated", ascending=False), "files")
    gate("G1", "harvested mappable rows > 0", int(cl.mappable.sum()), int(cl.mappable.sum()) > 0)
    P("")

    M = cl[cl.mappable].copy()

    # ------------------------------------------------------------------ panels
    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    small, ndrop, nmeta = load_small()
    raw["SMALL"] = small
    panels = {}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        elig = elig.copy()
        elig[:, spy_i] = False                       # SPY is the benchmark, never a holding
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, spy_i=spy_i,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm,
                             ins_m=ins[warm], oos_m=oos[warm],
                             nis=int(np.asarray(idx <= pd.Timestamp(IS_END)).sum()),
                             sc=sc, elig=elig,
                             spy=px["SPY"].pct_change().fillna(0.0).values[warm])
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P(f"  SMALL-VARIANT ROWS (panel label not exactly 'SMALL'): {int(M.small_variant.sum()):,} "
      f"— priced on THIS SMALL panel, stamped in .claims.csv")
    P("")

    def run_W(panel, W, mk, upto=None, lag=LAG):
        d = panels[panel]
        n = d["T"] if upto is None else upto
        rets, warm = d["rets"][:n], d["warm"][:n]
        m = np.asarray(mk[:n]).copy()
        ml = np.roll(m, lag)
        ml[:lag] = False
        Wl = np.zeros((n, d["K"]))
        if lag:
            Wl[lag:] = W[:n - lag]
        else:
            Wl[:] = W[:n]
        g, tn = nrun(rets, Wl, ml)
        return (g - tn * COST / 1e4)[warm]

    BOOKS: dict = {}

    def book(panel, N, H, g, freq, upto=None):
        key = (panel, int(N), int(H), round(float(g), 4), str(freq), upto)
        if key in BOOKS:
            return BOOKS[key]
        d = panels[panel]
        n = d["T"] if upto is None else upto
        mk = rebalance_mask(d["idx"], freq).values
        reb = np.flatnonzero(mk[:n])
        W = build(-d["sc"], d["elig"], d["priced"], reb, int(N), int(H), n, d["K"], float(g))
        r = run_W(panel, W, mk, upto=upto)
        BOOKS[key] = r
        return r

    def cfg_of(ctx, axis, rung):
        c = dict(CONTEXTS[ctx])
        c[AXES[axis]] = rung
        return c

    # ------------------------------------------------------------------ ARM 2: price the books
    P("## ARM 2 — PRICE EVERY HARVESTED DESTINATION AND EVERY HARVESTED ANCHOR AS A BOOK")
    need = set()
    for _, r in M.iterrows():
        for rung in (r.dest, r.anchor):
            c = cfg_of(r.ctx, r.axis, rung)
            need.add((r.panel, c["N"], c["H"], round(float(c["g"]), 4), c["freq"]))
    P(f"  distinct (panel, N, H, gross, cadence) books required: {len(need)}")
    brows = []
    for i, (panel, N, H, g, fq) in enumerate(sorted(need, key=lambda x: (x[0], x[1], x[2], x[3], x[4])), 1):
        r = book(panel, N, H, g, fq)
        d = panels[panel]
        m = blocks_m(r, d["ins_m"], d["oos_m"])
        brows.append(dict(panel=panel, N=N, H=H, gross=g, cadence=fq,
                          hash=zlib.crc32(np.asarray(r, float).tobytes()),
                          **{k: m[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                               "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")}))
        if i % 25 == 0:
            P(f"    {i}/{len(need)} books priced  ({time.time() - t0:.0f}s)")
    bdf = pd.DataFrame(brows)
    dump(bdf, "books")
    nuniq_val = bdf.groupby("panel")["hash"].nunique().to_dict()
    P(f"  distinct realised-return vectors per panel: {nuniq_val}  "
      f"(vs {bdf.groupby('panel').size().to_dict()} labelled books)")
    P("")

    # ------------------------------------------------------------------ ARM 3: the identity grid
    P("## ARM 3 — IS A COMMITTED RESOLVED PICK THE ANCHOR?  9 CELLS (claim set x identity key)")

    def vec(panel, ctx, axis, rung):
        c = cfg_of(ctx, axis, rung)
        return book(panel, c["N"], c["H"], round(float(c["g"]), 4), c["freq"])

    idrows = []
    for _, r in M.iterrows():
        rd, ra = vec(r.panel, r.ctx, r.axis, r.dest), vec(r.panel, r.ctx, r.axis, r.anchor)
        same_label = str(r.dest) == str(r.anchor)
        same_val = rd.tobytes() == ra.tobytes()
        same_rd = np.round(rd, 9).tobytes() == np.round(ra, 9).tobytes()
        dS = fsharpe(rd) - fsharpe(ra)
        d = panels[r.panel]
        dS_oos = fsharpe(rd[d["oos_m"]]) - fsharpe(ra[d["oos_m"]])
        idrows.append(dict(file=r.file, panel=r.panel, ctx=r.ctx, axis=r.axis, chooser=r.chooser,
                           dest=r.dest, anchor=r.anchor, resolved=r.resolved, bar=r.bar,
                           claimset=r.claimset, same_B_LABEL=same_label, same_B_VALUE=same_val,
                           same_B_VALUE_RD=same_rd, dSharpe=dS, dSharpe_OOS=dS_oos,
                           maxabsdiff=float(np.abs(rd - ra).max()),
                           corr=(float(np.corrcoef(rd, ra)[0, 1]) if rd.std() and ra.std() else np.nan)))
    idf = pd.DataFrame(idrows)
    dump(idf, "identity")

    grid = []
    for cs in CLAIMSETS:
        sub = idf if cs == "S_ALL" else idf[idf.claimset == cs]
        for ident in IDENTS:
            col = f"same_{ident}"
            res = sub[sub.resolved]
            na = res[~res[col]]
            grid.append(dict(claimset=cs, identity=ident, n_picks=len(sub),
                             n_resolved=len(res), n_resolved_anchor=int(res[col].sum()),
                             n_resolved_nonanchor=len(na),
                             share_nonanchor=(len(na) / len(res) if len(res) else np.nan),
                             n_unresolved=len(sub) - len(res),
                             n_unresolved_nonanchor=int((~sub[~sub.resolved][col]).sum()),
                             max_abs_dSharpe_nonanchor=(float(na.dSharpe.abs().max()) if len(na) else 0.0),
                             median_abs_dSharpe_nonanchor=(float(na.dSharpe.abs().median()) if len(na) else np.nan)))
    gdf = pd.DataFrame(grid)
    dump(gdf, "dialgrid")
    P(f"  {'claim set':<9s} {'identity':<12s} {'picks':>7s} {'resolved':>9s} {'=anchor':>8s} "
      f"{'NON-ANCHOR':>11s} {'share':>7s} {'max|dS|':>8s}")
    for _, r in gdf.iterrows():
        P(f"  {r.claimset:<9s} {r.identity:<12s} {r.n_picks:7d} {r.n_resolved:9d} "
          f"{r.n_resolved_anchor:8d} {r.n_resolved_nonanchor:11d} "
          f"{(r.share_nonanchor if np.isfinite(r.share_nonanchor) else -1):7.3f} "
          f"{r.max_abs_dSharpe_nonanchor:8.4f}")
    P("")
    P("  THE RESOLVED NON-ANCHOR PICKS UNDER B_VALUE (the queue's question), by axis:")
    rv = idf[idf.resolved & ~idf.same_B_VALUE]
    if len(rv):
        for k, n in rv.groupby(["axis", "panel"]).size().sort_values(ascending=False).items():
            sl = rv[(rv.axis == k[0]) & (rv.panel == k[1])]
            P(f"    axis={k[0]:<8s} panel={k[1]:<6s} {n:5d} rows  median |dSharpe| "
              f"{sl.dSharpe.abs().median():.4f}  max {sl.dSharpe.abs().max():.4f}  "
              f"median |dSharpe_OOS| {sl.dSharpe_OOS.abs().median():.4f}")
        P(f"    destination rungs named: "
          f"{dict(rv.groupby('axis').dest.apply(lambda s: sorted(set(map(str, s)))[:8]))}")
    else:
        P("    NONE — the record has no resolved pick that is a different book from its anchor.")
    P("")
    # ---------------- ARM 3b, ADDED AFTER THE FIRST FULL RUN, AND SAYING SO --------------
    P("## ARM 3b — ADDED AFTER THE FIRST FULL RUN (and declared as such): the first run found")
    P("  the three identity keys returning the SAME cell counts, and a non-anchor pick whose")
    P("  median |dSharpe| is 0.004.  Counts can agree while rows disagree, and a book can be a")
    P("  different book and still be indistinguishable from the anchor.  Neither test is a new")
    P("  dial: the key set is ARM 3's own and the bar is the ANCHOR's OWN block-bootstrap SE.")
    dis = pd.DataFrame([dict(pair=f"{a} vs {b}",
                             n_rows=len(idf),
                             n_disagree=int((idf[f"same_{a}"] != idf[f"same_{b}"]).sum()))
                        for a, b in (("B_LABEL", "B_VALUE"), ("B_LABEL", "B_VALUE_RD"),
                                     ("B_VALUE", "B_VALUE_RD"))])
    for _, r in dis.iterrows():
        P(f"    {r.pair:<24s} rows disagreeing on identity: {r.n_disagree:6d} of {r.n_rows}")
    dump(dis, "keydisagree")
    sers = []
    for panel in PANELS:
        d = panels[panel]
        anc = vec(panel, "CTX_A", "N", CONTEXTS["CTX_A"]["N"])
        se_full = se_block_one(anc, f"selfSE|{panel}")
        se_oos = se_block_one(anc[d["oos_m"]], f"selfSE|{panel}|oos")
        sub = idf[(idf.panel == panel) & idf.resolved & ~idf.same_B_VALUE]
        sers.append(dict(panel=panel, anchor_Sharpe=fsharpe(anc), se_anchor_Sharpe=se_full,
                         se_anchor_Sharpe_OOS=se_oos, n_resolved_nonanchor=len(sub),
                         share_within_1SE=(float((sub.dSharpe.abs() < se_full).mean()) if len(sub) else np.nan),
                         share_within_2SE=(float((sub.dSharpe.abs() < 2 * se_full).mean()) if len(sub) else np.nan),
                         share_within_1SE_OOS=(float((sub.dSharpe_OOS.abs() < se_oos).mean()) if len(sub) else np.nan),
                         median_abs_dSharpe=(float(sub.dSharpe.abs().median()) if len(sub) else np.nan),
                         max_abs_dSharpe=(float(sub.dSharpe.abs().max()) if len(sub) else np.nan)))
    sdf = pd.DataFrame(sers)
    dump(sdf, "indistinguishable")
    P(f"  {'panel':<6s} {'anchor S':>9s} {'own SE':>8s} {'nonanchor':>10s} {'<1SE':>7s} {'<2SE':>7s} "
      f"{'<1SE OOS':>9s} {'med|dS|':>8s} {'max|dS|':>8s}")
    for _, r in sdf.iterrows():
        P(f"  {r.panel:<6s} {r.anchor_Sharpe:9.3f} {r.se_anchor_Sharpe:8.4f} "
          f"{int(r.n_resolved_nonanchor):10d} {r.share_within_1SE:7.3f} {r.share_within_2SE:7.3f} "
          f"{r.share_within_1SE_OOS:9.3f} {r.median_abs_dSharpe:8.4f} {r.max_abs_dSharpe:8.4f}")
    hyp("H_KEYINERT", "the three identity keys disagree on 0 rows (the key is INERT here)", "0",
        f"disagreements {list(dis.n_disagree)}", int(dis.n_disagree.sum()) == 0)
    hyp("H_INSIDE_SE", "most resolved non-anchor picks sit inside the anchor's own 1 SE of Sharpe",
        "share_within_1SE > 0.50 on every panel",
        f"shares {[round(float(x), 3) for x in sdf.share_within_1SE]}",
        bool((sdf.share_within_1SE > 0.50).all()))
    P("")
    hyp("H_ANCHOR", "non-anchor resolved count == 0 in all 9 cells", "0",
        f"max over cells = {int(gdf.n_resolved_nonanchor.max())} "
        f"(B_VALUE cells: {list(gdf[gdf.identity == 'B_VALUE'].n_resolved_nonanchor)})",
        int(gdf.n_resolved_nonanchor.max()) == 0)
    lab = int(gdf[(gdf.claimset == 'S_ALL') & (gdf.identity == 'B_LABEL')].n_resolved_nonanchor.iloc[0])
    val = int(gdf[(gdf.claimset == 'S_ALL') & (gdf.identity == 'B_VALUE')].n_resolved_nonanchor.iloc[0])
    hyp("H_LABEL", "B_LABEL non-anchor count > B_VALUE non-anchor count", "strict >",
        f"S_ALL: B_LABEL {lab} vs B_VALUE {val}", lab > val)
    gate("G2", "every mappable row priced at both ends", len(idf), len(idf) == len(M))
    P("")

    # ------------------------------------------------------------------ ARM 4: the price leg
    P("## ARM 4 — THE PRICE LEG: WHAT DOES ACTING ON THE RECORD'S RESOLVED PICKS BUY?")
    P("  Each acting rule holds EQUAL CAPITAL in the destination books of the picks it acts on.")
    P("  WEIGHTING is reported at BOTH values (not a dial, 1211's row-vs-book distinction):")
    P("    W_ROWS  one unit per committed DECISION ROW (the record's own habit)")
    P("    W_BOOKS one unit per DISTINCT destination book (row inflation collapsed out)")
    P("  R_ANCHOR is the do-nothing gate-G3 book (N=20 / H=126 / GROSS=0.75 / CADENCE=W).")
    rules = {}
    for panel in PANELS:
        sub = idf[idf.panel == panel]
        anc = vec(panel, "CTX_A", "N", CONTEXTS["CTX_A"]["N"])       # the gate-G3 anchor book

        def combo(rows, weighting):
            trip = [(r.ctx, r.axis, r.dest) for r in rows.itertuples()]
            if not trip:
                return None, 0
            if weighting == "W_BOOKS":
                trip = sorted({(c, a, str(v)) for c, a, v in trip})
                trip = [(c, a, parse_rung(a, v)) for c, a, v in trip]
            mats = [vec(panel, c, a, v) for c, a, v in trip]
            return np.mean(np.vstack(mats), axis=0), len(trip)

        sets = {"R_RESOLVED": sub[sub.resolved],
                "R_RESNONANCHOR": sub[sub.resolved & ~sub.same_B_VALUE],
                "R_UNRESOLVED": sub[~sub.resolved],
                "R_ALLPICKS": sub}
        cand = {("R_ANCHOR", "W_ROWS"): (anc, 1)}
        for nm, rws in sets.items():
            for wt in ("W_ROWS", "W_BOOKS"):
                cand[(nm, wt)] = combo(rws, wt)
        rules[panel] = {k: v for k, v in cand.items() if v[0] is not None}
        P(f"  {panel}: " + "  ".join(f"{k[0]}/{k[1]}={v[1]}" for k, v in rules[panel].items()))

    prows = []
    for panel in PANELS:
        d = panels[panel]
        px = d["px"]
        spy = d["spy"]
        b2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].values[d["warm"]]
        b1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq="W")["returns"].values[d["warm"]]
        bench = {"SPY": spy, "RULESv2": b2, "RULESv1": b1}
        for nm, r in list(bench.items()):
            m = blocks_m(np.asarray(r, float), d["ins_m"], d["oos_m"])
            prows.append(dict(panel=panel, rule=nm, weighting="-", n_books=0, **m,
                              **{k: None for k in ("A_H1", "A_H2", "A_DD")},
                              **{k: None for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")},
                              **{k: None for k in ("O_S", "O_DD", "O_CAGR")},
                              gap_vs_anchor=np.nan, se_gap=np.nan, t_gap=np.nan,
                              gap_oos=np.nan, se_gap_oos=np.nan, t_gap_oos=np.nan))
        msp, mv2 = blocks_m(spy, d["ins_m"], d["oos_m"]), blocks_m(b2, d["ins_m"], d["oos_m"])
        anc = rules[panel][("R_ANCHOR", "W_ROWS")][0]
        for (nm, wt), (r, nb) in rules[panel].items():
            m = blocks_m(r, d["ins_m"], d["oos_m"])
            a4, b4, b4o = legs_4a(m, mv2), legs_4b(m, msp), legs_4b_oos(m, msp)
            if nm == "R_ANCHOR":
                g = sg = tg = go = sgo = tgo = np.nan
            else:
                g = fsharpe(r) - fsharpe(anc)
                sg = se_block_diff(r, anc, f"{panel}|{nm}|{wt}")
                tg = g / sg if sg else np.nan
                go = fsharpe(r[d["oos_m"]]) - fsharpe(anc[d["oos_m"]])
                sgo = se_block_diff(r[d["oos_m"]], anc[d["oos_m"]], f"{panel}|{nm}|{wt}|oos")
                tgo = go / sgo if sgo else np.nan
            prows.append(dict(panel=panel, rule=nm, weighting=wt, n_books=nb, **m, **a4, **b4, **b4o,
                              gap_vs_anchor=g, se_gap=sg, t_gap=tg,
                              gap_oos=go, se_gap_oos=sgo, t_gap_oos=tgo))
    pdf = pd.DataFrame(prows)
    dump(pdf, "rules")
    P(f"  {'panel':<6s} {'rule':<15s} {'wt':<8s} {'n':>4s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
      f"{'H1':>6s} {'H2':>6s} {'OOS_S':>7s} {'OOS_CAGR':>9s} {'OOS_DD':>8s} {'4a':>4s} {'4b':>4s} {'t_oos':>6s}")
    for _, r in pdf.iterrows():
        a = "-" if r.A_H1 is None else f"{int(bool(r.A_H1)) + int(bool(r.A_H2)) + int(bool(r.A_DD))}/3"
        b = "-" if r.L_H1 is None else f"{sum(int(bool(r[k])) for k in ('L_H1','L_H2','L_OOS','L_DD','L_CAGR'))}/5"
        P(f"  {r.panel:<6s} {r.rule:<15s} {r.weighting:<8s} {int(r.n_books):4d} {r.CAGR:7.2%} {r.Sharpe:7.3f} "
          f"{r.MaxDD:8.2%} {r.H1:6.2f} {r.H2:6.2f} {r.OOS_Sharpe:7.3f} {r.OOS_CAGR:9.2%} "
          f"{r.OOS_MaxDD:8.2%} {a:>4s} {b:>4s} "
          f"{(r.t_gap_oos if np.isfinite(r.t_gap_oos) else 0):6.2f}")
    res_rows = pdf[(pdf.rule == "R_RESOLVED") & pdf.t_gap_oos.notna()]
    worst = float(res_rows.t_gap_oos.max()) if len(res_rows) else np.nan
    hyp("H_DONOTHING", "R_RESOLVED's OOS Sharpe gap vs R_ANCHOR < 2 SE on every panel", "t < 2",
        f"max t_oos = {worst:.2f} over panels {list(res_rows.panel)}", not (worst >= 2.0))
    P("")

    # ------------------------------------------------------------------ ARM 5: rule 8
    P("## ARM 5 — RULE 8 WALK-FORWARD: resolution re-decided on IS ONLY, 2017-2026 read once")
    P("  For each (panel, context, ladder) the chooser picks a rung from the IS window only and")
    P("  the pick is RESOLVED iff it beats the anchor by 1.96 of its own paired IS block-bootstrap")
    P("  SE.  C_RESOLVED trades the pick only when resolved, else the anchor (the record's own")
    P("  'act only on resolved picks' rule).  C_ALWAYS trades every pick.  C_ANCHOR does nothing.")
    CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISCALMAR"]
    LADDER_RUNGS = {"N": [5, 8, 10, 12, 15, 20, 25, 30, 40],
                    "H": [21, 42, 63, 126, 189, 252, 378],
                    "GROSS": [0.30, 0.45, 0.60, 0.75, 0.90, 1.00],
                    "CADENCE": ["W", "M", "Q"]}
    wrows = []
    for panel in PANELS:
        d = panels[panel]
        nis = d["nis"]
        is_mask, oos_mask = d["ins_m"], d["oos_m"]
        for ctx in CONTEXTS:
            anc_r = vec(panel, ctx, "N", CONTEXTS[ctx]["N"])
            for axis, rungs in LADDER_RUNGS.items():
                rung_r = {}
                for rg in rungs:
                    c = cfg_of(ctx, axis, rg)
                    rung_r[rg] = book(panel, c["N"], c["H"], round(float(c["g"]), 4), c["freq"],
                                      upto=nis)          # IS-ONLY book for the choosing
                a_is = book(panel, CONTEXTS[ctx]["N"], CONTEXTS[ctx]["H"],
                            round(float(CONTEXTS[ctx]["g"]), 4), CONTEXTS[ctx]["freq"], upto=nis)
                for ch in CHOOSERS:
                    def keyf(rg):
                        r = rung_r[rg]
                        c, s, dd = fmet(r)
                        return {"C_ISSHARPE": s, "C_ISCAGR": c,
                                "C_ISCALMAR": (c / abs(dd) if dd else np.nan)}[ch]
                    vals = [keyf(rg) for rg in rungs]
                    pick = rungs[int(np.nanargmax(vals))]
                    pr = rung_r[pick]
                    gap_is = fsharpe(pr) - fsharpe(a_is)
                    se_is = se_block_diff(pr, a_is, f"wf|{panel}|{ctx}|{axis}|{ch}")
                    t_is = gap_is / se_is if se_is else np.nan
                    resolved = bool(np.isfinite(t_is) and t_is > TBAR)
                    full_pick = vec(panel, ctx, axis, pick)
                    traded = full_pick if resolved else anc_r
                    for nm, rr in (("C_RESOLVED", traded), ("C_ALWAYS", full_pick),
                                   ("C_ANCHOR", anc_r)):
                        m = blocks_m(rr, is_mask, oos_mask)
                        wrows.append(dict(panel=panel, ctx=ctx, axis=axis, chooser=ch, rule=nm,
                                          pick=str(pick), anchor_rung=str(CONTEXTS[ctx][AXES[axis]]),
                                          label_same=(str(pick) == str(CONTEXTS[ctx][AXES[axis]])),
                                          value_same=(full_pick.tobytes() == anc_r.tobytes()),
                                          t_is=t_is, resolved=resolved,
                                          **{k: m[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")}))
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")
    dec = wdf[wdf.rule == "C_RESOLVED"]
    P(f"  rule-8 decisions: {len(dec)} = {len(PANELS)} panels x {len(CONTEXTS)} contexts x "
      f"{len(LADDER_RUNGS)} ladders x {len(CHOOSERS)} choosers")
    P(f"  IS-resolved decisions: {int(dec.resolved.sum())} of {len(dec)} "
      f"({dec.resolved.mean():.1%});  of those, label-different from the anchor "
      f"{int((dec.resolved & ~dec.label_same).sum())}, VALUE-different {int((dec.resolved & ~dec.value_same).sum())}")
    P(f"  {'panel':<6s} {'rule':<12s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
      f"{'OOS_S':>7s} {'OOS_CAGR':>9s} {'OOS_DD':>8s}")
    wf_agg = {}
    for panel in PANELS:
        d = panels[panel]
        for nm in ("C_RESOLVED", "C_ALWAYS", "C_ANCHOR"):
            sub = wdf[(wdf.panel == panel) & (wdf.rule == nm)]
            mats = []                      # DECISION-weighted: one unit per rule-8 decision
            for row in sub.itertuples():
                take_pick = (nm == "C_ALWAYS") or (nm == "C_RESOLVED" and row.resolved)
                if take_pick:
                    mats.append(vec(panel, row.ctx, row.axis, parse_rung(row.axis, row.pick)))
                else:
                    mats.append(vec(panel, row.ctx, "N", CONTEXTS[row.ctx]["N"]))
            r = np.mean(np.vstack(mats), axis=0)
            wf_agg[(panel, nm)] = r
            m = blocks_m(r, d["ins_m"], d["oos_m"])
            P(f"  {panel:<6s} {nm:<12s} {m['CAGR']:7.2%} {m['Sharpe']:7.3f} {m['MaxDD']:8.2%} "
              f"{m['H1']:6.2f} {m['H2']:6.2f} {m['OOS_Sharpe']:7.3f} {m['OOS_CAGR']:9.2%} "
              f"{m['OOS_MaxDD']:8.2%}")
    wf2 = []
    for panel in PANELS:
        d = panels[panel]
        msp = blocks_m(d["spy"], d["ins_m"], d["oos_m"])
        b2 = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values[d["warm"]]
        mv2 = blocks_m(b2, d["ins_m"], d["oos_m"])
        anc = wf_agg[(panel, "C_ANCHOR")]
        for nm in ("C_RESOLVED", "C_ALWAYS", "C_ANCHOR"):
            r = wf_agg[(panel, nm)]
            m = blocks_m(r, d["ins_m"], d["oos_m"])
            g = fsharpe(r[d["oos_m"]]) - fsharpe(anc[d["oos_m"]])
            se = se_block_diff(r[d["oos_m"]], anc[d["oos_m"]], f"wf8|{panel}|{nm}")
            wf2.append(dict(panel=panel, rule=nm, **m, **legs_4a(m, mv2), **legs_4b(m, msp),
                            **legs_4b_oos(m, msp), gap_oos_vs_anchor=g, se_oos=se,
                            t_oos=(g / se if se else np.nan),
                            spy_OOS_Sharpe=msp["OOS_Sharpe"], spy_OOS_CAGR=msp["OOS_CAGR"],
                            spy_OOS_MaxDD=msp["OOS_MaxDD"], v2_OOS_Sharpe=mv2["OOS_Sharpe"],
                            v2_OOS_CAGR=mv2["OOS_CAGR"], v2_OOS_MaxDD=mv2["OOS_MaxDD"]))
    w2 = pd.DataFrame(wf2)
    dump(w2, "wf_summary")
    P("  RULE-8 LEG COUNTS (4a vs live RULES v2, 4b vs SPY, OOS-only 4b):")
    for _, r in w2.iterrows():
        P(f"    {r.panel:<6s} {r.rule:<12s} 4a {sum(int(bool(r[k])) for k in ('A_H1','A_H2','A_DD'))}/3"
          f"  4b {sum(int(bool(r[k])) for k in ('L_H1','L_H2','L_OOS','L_DD','L_CAGR'))}/5"
          f"  4b-OOS {sum(int(bool(r[k])) for k in ('O_S','O_DD','O_CAGR'))}/3"
          f"  t_oos vs anchor {(r.t_oos if np.isfinite(r.t_oos) else 0):+6.2f}")
    rr = w2[(w2.rule == "C_RESOLVED")]
    hyp("H_OOS", "C_RESOLVED does not beat C_ANCHOR OOS by 2 SE on any panel", "t_oos < 2",
        f"max t_oos = {float(rr.t_oos.max()):.2f}", not (float(rr.t_oos.max()) >= 2.0))
    P("")

    # ------------------------------------------------------------------ verdict
    P("## VERDICT")
    keep4a = w2[(w2.rule == "C_RESOLVED")].apply(
        lambda r: bool(r.A_H1) and bool(r.A_H2) and bool(r.A_DD), axis=1)
    keep4b = w2[(w2.rule == "C_RESOLVED")].apply(
        lambda r: all(bool(r[k]) for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")), axis=1)
    P(f"  4a PASSES (C_RESOLVED, rule-8): {int(keep4a.sum())} of {len(keep4a)}")
    P(f"  4b PASSES (C_RESOLVED, rule-8): {int(keep4b.sum())} of {len(keep4b)}")
    nonanchor_val = int(gdf[(gdf.claimset == 'S_ALL') & (gdf.identity == 'B_VALUE')]
                        .n_resolved_nonanchor.iloc[0])
    verdict = "KILL (capital)" if (int(keep4b.sum()) == 0 and int(keep4a.sum()) == 0) else "KEEP-candidate"
    P(f"  COMMITTED RESOLVED NON-ANCHOR PICKS (S_ALL, B_VALUE): {nonanchor_val}")
    P(f"  VERDICT: {verdict}")
    gdf.to_csv(f"{OUT}.dialgrid.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    pd.DataFrame(HYP).to_csv(f"{OUT}.hypotheses.csv", index=False)
    P(f"  gates: {sum(g['pass_'] for g in GATES)}/{len(GATES)} PASS   "
      f"hypotheses: {sum(h['supported'] for h in HYP)}/{len(HYP)} supported")
    P(f"  elapsed {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
