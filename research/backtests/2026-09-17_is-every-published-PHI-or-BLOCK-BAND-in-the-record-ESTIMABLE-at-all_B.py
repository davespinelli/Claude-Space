#!/usr/bin/env python3
"""Idea 1170 (lane B, 2026-09-17)
   is-every-published-PHI-or-BLOCK-BAND-in-the-record-ESTIMABLE-at-all

THE QUEUE'S PREMISE, QUOTED.  Idea 1164 found that phi's denominator (OBSERVED - N_IID)
passes through zero, so 16 of 72 books gave an interpolation weight outside [0, 1] by up
to two orders of magnitude (-31.55 to +13.17) until a resolution rule was imposed.  The
queue filed this idea to CENSUS every committed phi, L* and moving-block band in the
record for whether its own denominator clears its own cross-seed noise, and to PRICE the
cheapest repair -- publish the denominator beside the ratio, or refuse the ratio.

WHAT THIS RUN CHANGES ABOUT THE QUESTION, STATED UP FRONT.

  The queue's phrase is "every published PHI ... in the record".  That phrase presumes the
  record's `phi` NAMES ONE OBJECT.  It does not.  `phi` is the record's most overloaded
  token: it is the 4b-screen threshold in the 2026-09-05..09-08 calibration work and it is
  1162/1164's block-null INTERPOLATION WEIGHT, and the two share no denominator, no units
  and no failure mode.  A census that keys on the TOKEN therefore inherits a false-positive
  rate this run measures and pre-registers a bar for (H_TOKEN) rather than assuming away.
  The same holds for L*: the record carries at least three unrelated L-stars (1162/1164's
  ladder CROSSING, 1112's shortest CALLABLE sub-window, 1146's POOL START).  The census
  below is therefore built in two layers -- TOKEN match, then OBJECT classification by the
  columns that a denominator needs -- and both counts are published.

  The second thing the queue's phrasing hides: "clears its own cross-seed noise" is not
  one bar.  1164's rule (3 x the larger cross-seed spread, 0.25 pp floor) was written AFTER
  seeing its own first cut, and needs S SEEDS PER CELL -- it is the EXPENSIVE repair.  A
  one-seed t-rule reading the denominator against the bootstrap SE of its own null median
  costs NOTHING extra and is the cheapest candidate repair in the queue's sense.  Whether
  the two agree is the load-bearing question this run answers, because if they do, the
  record can have the repair for free.

TUNED DIALS (2, PROTOCOL rule 4) -- the queue names both:

  `RESOLUTION`  {R_1164, R_STRICT, R_LOOSE, R_TSTAT}
  `STATISTIC`   {S_PHI, S_LSTAR, S_BAND}

  = 12 combinations, EVERY ONE PUBLISHED in `.dialgrid.csv`, whatever the headline says.

  RESOLUTION RULES (all applied to the same measured quantities):
    R_1164   the INCUMBENT, 1164's own rule, quoted: the object is estimable when
             |denominator| >= max(3 x the larger cross-seed spread of the two null
             medians, 0.25 percentage points).  Needs S seeds.
    R_STRICT 5 x, 0.50 pp floor.  Needs S seeds.
    R_LOOSE  1 x, 0.10 pp floor.  Needs S seeds.
    R_TSTAT  THE CHEAP REPAIR: |denominator| >= 2 x the bootstrap SE of the null median it
             is measured against, computed from ONE seed's own draws by the DISTRIBUTION-
             FREE order-statistic median SE (half the spacing between the ranks sqrt(n)/2
             either side of the middle).  Costs NO extra bootstrap.  A first cut of this
             run used (IQR / 1.349) / sqrt(n) and was wrong by the gaussian 1.2533 factor;
             gate G4 caught it before a single R_TSTAT verdict was read, and the correction
             is recorded in `median_se` rather than quietly patched.

  STATISTICS (the three object classes the queue names):
    S_PHI    the interpolation weight phi = (N_BLOCK - N_IID) / (OBSERVED - N_IID) at the
             record's frozen L = 63.  Denominator = OBSERVED - N_IID.  Noise = the null
             medians' cross-seed spread (R_1164/R_STRICT/R_LOOSE) or the iid median's own
             bootstrap SE (R_TSTAT).
    S_LSTAR  the ladder CROSSING L*, the first rung of the L ladder at which the block
             null reaches the observed value.  Its denominator is the SAME gap the
             crossing must traverse, so the rules apply unchanged; SEED STABILITY of the
             crossing rung is measured and published beside it as the direct check.
    S_BAND   the committed MOVING-BLOCK BAND on |MaxDD|: the [q05, q95] interval of the
             L = 63 block null.  Denominator analogue = the band's own WIDTH; noise = the
             cross-seed spread of its ENDPOINTS.

  NOT DIALS.  PANEL (all three built), the 132-CELL POPULATION -- 117 BOOKS (the N / HOLD /
  CADENCE axes and the anchor GROSS ladder, a population, not a search) plus 1162's 15
  ANCHOR CONTROL cells -- every one published, the
  L LADDER (9 rungs, all published, headline frozen at the record's L = 63 and nothing is
  ever selected on it), the 15 ANCHOR CONTROL cells (1162's own five, on three panels),
  SEED (5 per headline cell, 3 per ladder rung, spread published, never selected on), the
  BAND LEVEL (0.80 / 0.90 / 0.95 all published, headline 0.90), and the CENSUS SCAN, which
  is exhaustive over research/backtests/*.csv and the record's committed prose.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131/1140/1148/1159/1162/
1164's construction: CAND20 legs, max_vol 0.60, gross 0.75, 10 bps (PROTOCOL rule 2),
LAG 1, warm-up 260, IS end 2016-12-31, block L = 63, 1000 draws, crc32 seeds, DD cap 0.60,
CAGR floor 0.70.

CROSS-RUN GATES.  1164's 72 population cells AND 1162's 15 anchor cells are REPLAYED BIT
FOR BIT out of this run's own code path, using each parent's seed base and its exact seed
parts, and checked against their committed `.cells.csv`.  If either replay fails, nothing
below is comparable to the record and the run says so.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
CURRENT constituents of a sub-$2B screen (data/SMALL_PANEL_README.md) less the documented
max_1d_move >= 1.0 exclusion.  Every LEVEL here -- CAGR, |MaxDD| and every null median and
band built on them -- is optimistic.  It largely CANCELS out of the headline, which is a
COUNT of how many committed objects clear their own noise (a within-cell comparison of one
construction against itself), and it does NOT cancel out of the 4a / 4b legs in ARM F.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
"""
from __future__ import annotations

import csv
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

DATE = "2026-09-17"
SLUG = "is-every-published-PHI-or-BLOCK-BAND-in-the-record-ESTIMABLE-at-all"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136", "SMALL"]
RESOLUTIONS = ["R_1164", "R_STRICT", "R_LOOSE", "R_TSTAT"]          # dial 1
STATISTICS = ["S_PHI", "S_LSTAR", "S_BAND"]                         # dial 2
RES_PARAM = {"R_1164": (3.0, 0.25), "R_STRICT": (5.0, 0.50), "R_LOOSE": (1.0, 0.10)}
TSTAT_K = 2.0

L_BLOCK, BDRAWS = 63, 1000
L_LADDER = [1, 5, 21, 63, 126, 252, 504, 1008]        # + T, appended per cell
SEEDS = [0, 1, 2, 3, 4]                               # 5 per headline cell
LAD_SEEDS = [0, 1, 2]                                 # 3 per ladder rung
BAND_LEVELS = [0.80, 0.90, 0.95]
BAND_HEAD = 0.90
SEED_BASE = 11701170
SEED_1162, SEED_1164 = 11621162, 11641164             # the parents' bases, for the replays

POP_N = [5, 10, 20, 40]
POP_H = [63, 126, 252]
POP_F = ["W", "M"]
ANCHOR_CONTROLS = ["C_BOOK", "C_GATEOFF", "C_NOREBAL", "C_SHUFFLE", "C_SPY"]
GROSS_LADDER = [round(0.30 + 0.05 * i, 3) for i in range(15)]
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}

PRIOR1162 = BT / ("2026-09-17_why-does-an-IID-RESAMPLE-produce-DEEPER-drawdowns-than-a-"
                  "BLOCK-one_B.cells.csv")
PRIOR1164 = BT / ("2026-09-17_what-sets-PHI-once-the-EPISODE-LENGTH-is-only-a-LOWER-BOUND-"
                  "on-L-STAR_B.cells.csv")
PRIOR1164_LAD = BT / ("2026-09-17_what-sets-PHI-once-the-EPISODE-LENGTH-is-only-a-LOWER-"
                      "BOUND-on-L-STAR_B.lstar.csv")
COMMITTED_1164_ESTIMABLE = 56          # 72 books less the 16 the queue quotes as outside [0,1]

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts, base=SEED_BASE):
    return base + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<66s} {value:.3e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, bar, measured, supported):
    HYP.append(dict(hypothesis=name, bar=bar, measured=measured, supported=bool(supported)))
    P(f"  {name:<11s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


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


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ======================================================== the two resample nulls
def null_index(kind, rng, T, ndraws, L=L_BLOCK):
    if kind == "N_IID":
        return rng.integers(0, T, size=(ndraws, T))
    if kind == "N_BLOCK":
        nb = int(np.ceil(T / L))
        st = rng.integers(0, T, size=(ndraws, nb))
        idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
        return idx.reshape(ndraws, nb * L)[:, :T]
    raise ValueError(kind)


def boot_maxdd(r, idx, chunk=100):
    """|MaxDD| (positive, in %) of ONE return series under every resample row of idx."""
    LG = np.log1p(np.asarray(r, float))
    out = np.empty(idx.shape[0])
    for a in range(0, idx.shape[0], chunk):
        ix = idx[a:a + chunk]
        cum = np.cumsum(LG[ix], axis=1)
        run = np.maximum.accumulate(cum, axis=1)
        out[a:a + chunk] = -np.expm1(cum - run).min(axis=1) * 100.0
    return out


def null_draws(r, kind, seed_parts, L=L_BLOCK, base=SEED_BASE, ndraws=BDRAWS):
    rng = np.random.default_rng(seed_of(*seed_parts, base=base))
    return boot_maxdd(r, null_index(kind, rng, len(r), ndraws, L))


def median_se(x):
    """SE of a sample median read off the draws themselves, DISTRIBUTION-FREE: half the
    spacing between the order statistics sqrt(n)/2 ranks either side of the middle, which
    is the binomial one-sigma interval for a median and recovers the gaussian
    1.2533 * sd / sqrt(n) exactly (gate G4).  Distribution-free matters here because a
    bootstrap |MaxDD| distribution is right-skewed, not normal.  Needs ONE seed -- this
    is what makes R_TSTAT the free repair.

    A FIRST CUT OF THIS RUN USED (IQR / 1.349) / sqrt(n) AND WAS WRONG BY THE 1.2533
    FACTOR; gate G4 caught it before a single R_TSTAT verdict was read.  Recorded here
    rather than quietly patched."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    half = 0.5 * np.sqrt(n)
    lo = int(np.clip(np.floor(n / 2.0 - half), 0, n - 1))
    hi = int(np.clip(np.ceil(n / 2.0 + half), 0, n - 1))
    return float((x[hi] - x[lo]) / 2.0)


def rule_bar(rule, spread_iid, spread_block, se_iid):
    """The resolution BAR a |denominator| must clear, per dial-1 rung."""
    if rule == "R_TSTAT":
        return TSTAT_K * se_iid
    k, floor = RES_PARAM[rule]
    return max(k * max(spread_iid, spread_block), floor)


# ---------------------------------------------------------- observed-path diagnostics
def obs_maxdd(r):
    cum = np.cumsum(np.log1p(np.asarray(r, float)))
    run = np.maximum.accumulate(cum)
    dd = np.expm1(cum - run)
    tr = int(dd.argmin())
    pk = int(np.argmax(cum[:tr + 1]))
    return -float(dd[tr]) * 100.0, pk, tr


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# ================================================================ ARM A — THE CENSUS
TOK_PHI = re.compile(r"(^|_)phi(\b|_|$)", re.I)
TOK_LSTAR = re.compile(r"l[_]?star", re.I)
TOK_BANDPAIR = [("lo", "hi"), ("_lo", "_hi"), ("lower", "upper"), ("ci_lo", "ci_hi"),
                ("q05", "q95"), ("boot_lo", "boot_hi")]
CTX_INTERP = {"n_iid", "n_block", "null_median", "n_stat"}
CTX_BLOCK = re.compile(r"(block|boot|resample|null|perm)", re.I)
OBS_COL = re.compile(r"^(observed|obs|obs_maxdd|obs_band|real|book)(_|$)", re.I)


def band_pairs(cols):
    """Committed lo/hi column PAIRS: a band is published as an interval or it is not one."""
    low = [c.lower() for c in cols]
    pairs = []
    for c in low:
        for a, b in [("lo", "hi"), ("lower", "upper"), ("q05", "q95"), ("q025", "q975")]:
            if c.endswith(a) or c == a:
                cand = (c[: len(c) - len(a)] + b) if c.endswith(a) else b
                if cand in low and (c, cand) not in pairs:
                    pairs.append((c, cand))
    return pairs


def census_scan():
    """Exhaustive scan of every committed CSV in research/backtests for the three object
    classes, in TWO layers: TOKEN match, then OBJECT classification by the columns a
    denominator needs.  Returns one row per (file, object class)."""
    rows = []
    files = sorted(BT.glob("*.csv"))
    for f in files:
        try:
            with open(f, newline="") as fh:
                rd = csv.reader(fh)
                hdr = next(rd)
                n = sum(1 for _ in rd)
        except Exception:
            continue
        cols = [c.strip() for c in hdr]
        low = {c.lower() for c in cols}
        interp_ctx = bool(low & CTX_INTERP)
        block_ctx = interp_ctx or bool(CTX_BLOCK.search(f.name)) or any(
            CTX_BLOCK.search(c) for c in cols)
        has_obs = any(OBS_COL.search(c) for c in cols)
        # ---- S_PHI
        phicols = [c for c in cols if TOK_PHI.search(c)]
        if phicols:
            obj = "S_PHI" if interp_ctx else "S_PHI_OTHER"
            pub_denom = ("denom" in low) or (has_obs and "n_iid" in low)
            pub_res = ("resolution" in low) or any("seed_spread" in c.lower() for c in cols)
            rows.append(dict(file=f.name, object=obj, token="phi", n_rows=n,
                             columns="|".join(phicols), interp_ctx=interp_ctx,
                             publishes_denominator=bool(pub_denom),
                             publishes_resolution=bool(pub_res)))
        # ---- S_LSTAR
        lcols = [c for c in cols if TOK_LSTAR.search(c)]
        if lcols:
            is_cross = interp_ctx or ("l" in low and "null_median" in low) or (
                "episode_bars" in low and "l_star" in low)
            obj = "S_LSTAR" if is_cross else "S_LSTAR_OTHER"
            pub_denom = ("gap" in low) or (has_obs and ("n_iid" in low or
                                                        "median_at_l1" in low))
            rows.append(dict(file=f.name, object=obj, token="L*", n_rows=n,
                             columns="|".join(lcols), interp_ctx=interp_ctx,
                             publishes_denominator=bool(pub_denom),
                             publishes_resolution=bool(any("seed" in c.lower() for c in cols))))
        # ---- S_BAND
        bp = band_pairs(cols)
        if bp:
            obj = "S_BAND" if block_ctx else "S_BAND_OTHER"
            pub_res = any(("seed" in c.lower()) or ("draw" in c.lower()) or
                          ("sd" == c.lower()) or ("_sd" in c.lower()) for c in cols)
            rows.append(dict(file=f.name, object=obj, token="band", n_rows=n,
                             columns="|".join(f"{a}/{b}" for a, b in bp[:6]),
                             interp_ctx=block_ctx,
                             publishes_denominator=True,      # a band publishes its own width
                             publishes_resolution=bool(pub_res)))
    return pd.DataFrame(rows), len(files)


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
NUMBER = re.compile(r"-?\d+\.\d+|-?\d+")
S_PHI_W = re.compile(r"\bphi\b", re.I)
S_LSTAR_W = re.compile(r"\bL\*|\bL_star|\bLSTAR", re.I)
S_BAND_W = re.compile(r"(moving[- ]block|block bootstrap|block band|bootstrap band)", re.I)
DENOM_W = re.compile(r"(denominator|N_IID|iid null|observed|gap|resolution|estimable|"
                     r"seed spread|cross-seed)", re.I)


def sentence_census():
    """The reader-facing layer: committed PROSE that quotes one of the three objects with a
    NUMBER, and whether the same sentence carries anything a reader could check it with."""
    rows = []
    srcs = sorted(BT.glob("*.md")) + [ROOT / "research" / "LEADERBOARD.md",
                                      ROOT / "research" / "CHANGELOG.md",
                                      ROOT / "research" / "QUEUE.md"]
    nsent = 0
    for f in srcs:
        try:
            txt = f.read_text(errors="replace")
        except Exception:
            continue
        for s in SENT_SPLIT.split(txt.replace("\n", " ")):
            nsent += 1
            if len(s) > 1200:
                s = s[:1200]
            cls = None
            if S_PHI_W.search(s):
                cls = "S_PHI"
            elif S_LSTAR_W.search(s):
                cls = "S_LSTAR"
            elif S_BAND_W.search(s):
                cls = "S_BAND"
            if cls is None or not NUMBER.search(s):
                continue
            rows.append(dict(file=f.name, object=cls, has_denominator_token=
                             bool(DENOM_W.search(s)), sentence=s.strip()[:400]))
    return pd.DataFrame(rows), nsent


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1170 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P("")
    head_bytes = (ROOT / "data" / "prices.csv").read_bytes()
    P("## PRICE-VINTAGE STAMP (PROTOCOL draft rule 12, proposed by 1163 — complied with, "
      "not enacted)")
    P(f"  data/prices.csv @HEAD  crc32={format(zlib.crc32(head_bytes) & 0xFFFFFFFF, '08x')}  "
      f"{len(head_bytes):,} bytes")
    P("")

    P("## PRE-REGISTRATION — declared before a single result number")
    P("  DIAL 1 RESOLUTION : R_1164 (3x spread, 0.25pp), R_STRICT (5x, 0.50),")
    P("                      R_LOOSE (1x, 0.10), R_TSTAT (2 x median SE, ONE seed, FREE)")
    P("  DIAL 2 STATISTIC  : S_PHI, S_LSTAR, S_BAND")
    P("  NOT DIALS         : PANEL (3), the 132-cell POPULATION (117 books + 15 anchor")
    P("                      controls), the L ladder (9 rungs), SEED (5 / 3), BAND LEVEL (3),")
    P("                      and the CENSUS, which is exhaustive.")
    P("  H_TOKEN    the queue's phrase 'every published PHI in the record' is well posed:")
    P("             >= 90% of the committed rows carrying a `phi` column are the")
    P("             INTERPOLATION object 1164 defined.  FALSIFICATION of the framing.")
    P("  H_CENSUS   the record is already self-checkable: >= 90% of committed INTERPOLATION")
    P("             phi rows publish their own denominator (or both its ingredients).")
    P("  H_ESTIM    under the incumbent R_1164, >= 50% of the rebuildable phi cells are")
    P("             ESTIMABLE.")
    P("  H_RULE     the verdict is ROBUST to the resolution rule: R_1164 and R_STRICT and")
    P("             R_LOOSE agree on >= 90% of cells.")
    P("  H_CHEAP    THE PRICE OF THE REPAIR: the FREE one-seed R_TSTAT agrees with the")
    P("             5-seed incumbent R_1164 on >= 90% of cells, for all three statistics.")
    P("  H_LSTAR    the committed crossing L* is SEED-STABLE (same rung at 3 of 3 seeds) at")
    P("             >= 90% of cells.")
    P("  H_BAND     the committed moving-block band is estimable (endpoint cross-seed spread")
    P("             <= 10% of band width) at >= 90% of cells.")
    P("  H_CAPITAL  the repair has CAPITAL content: restricting an IS chooser to ESTIMABLE-")
    P("             phi books moves OOS Sharpe by >= 0.05 at >= half the (panel, chooser,")
    P("             rule) cells.  If it does not, the repair is a DISCLOSURE device only.")
    P("")

    # --------------------------------------------------------------------- panels
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
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, spy_i=spy_i,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm, ins=ins, oos=oos,
                             sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY.")
    P("")

    # ------------------------------------------------------- book constructors
    _WCACHE: dict = {}

    def weights_pop(panel, N, H, freq):
        key = (panel, "POP", N, H, freq)
        if key not in _WCACHE:
            d = panels[panel]
            mk = rebalance_mask(d["idx"], freq).values
            _WCACHE[key] = (build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N, H,
                                  d["T"], d["K"], 1.0), mk)
        return _WCACHE[key]

    def weights_anchor(panel, control):
        key = (panel, "ANC", control)
        if key in _WCACHE:
            return _WCACHE[key]
        d = panels[panel]
        T, K = d["T"], d["K"]
        if control == "C_SPY":
            mk = rebalance_mask(d["idx"], FREQ0).values
            W = np.zeros((T, K))
            W[WARMUP:, d["spy_i"]] = 1.0
        elif control == "C_NOREBAL":
            mk_full = rebalance_mask(d["idx"], FREQ0).values
            first = int(np.flatnonzero(mk_full & (np.arange(T) >= WARMUP))[0])
            mk = np.zeros(T, dtype=bool)
            mk[first] = True
            W = build(-d["sc"], d["elig"], d["priced"], np.array([first]), N0, HOLD0, T, K, 1.0)
        else:
            mk = rebalance_mask(d["idx"], FREQ0).values
            elig = d["priced"] if control == "C_GATEOFF" else d["elig"]
            if control == "C_GATEOFF" and panel == "SMALL":
                elig = elig.copy()
                elig[:, d["spy_i"]] = False
            W = build(-d["sc"], elig, d["priced"], np.flatnonzero(mk), N0, HOLD0, T, K, 1.0)
        _WCACHE[key] = (W, mk)
        return _WCACHE[key]

    def run_weights(panel, W1, mk, gross):
        d = panels[panel]
        W = W1 * gross
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return (g - tn * COST / 1e4)[d["warm"]]

    def pop_returns(panel, N, H, freq, gross=GROSS0):
        W1, mk = weights_pop(panel, N, H, freq)
        return run_weights(panel, W1, mk, gross)

    def anchor_returns(panel, control, gross=GROSS0):
        base = "C_BOOK" if control == "C_SHUFFLE" else control
        W1, mk = weights_anchor(panel, base)
        r = run_weights(panel, W1, mk, gross)
        if control == "C_SHUFFLE":
            rw = r.copy()
            np.random.default_rng(seed_of(panel, "C_SHUFFLE", gross, "",
                                          base=SEED_1162)).shuffle(rw)
            return rw
        return r

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_weights("U56", W / GROSS0, mk, GROSS0)
    v = float(np.abs(eng[d["warm"]] - rfast).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)

    Wfresh = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
                   d["T"], d["K"], 0.45)
    v = float(np.abs(Wfresh - (W / GROSS0) * 0.45).max())
    gate("G2", "gross ladder is an EXACT scale on the selection (built vs scaled W)", v,
         v < 1e-15)

    ix_b1 = null_index("N_BLOCK", np.random.default_rng(777), 500, 50, L=1)
    ix_i1 = null_index("N_IID", np.random.default_rng(777), 500, 50)
    v = float(np.abs(ix_b1 - ix_i1).max())
    gate("G3", "N_BLOCK at L=1 IS N_IID, bit for bit (same seed, same draw)", v, v == 0)

    z = np.random.default_rng(3).normal(0, 1, 20000)
    v = abs(median_se(z) - 1.2533 / np.sqrt(len(z))) / (1.2533 / np.sqrt(len(z)))
    gate("G4", "median_se (order statistics) == the gaussian median SE 1.2533*sd/sqrt(n)",
         v, v < 0.05)

    rr = np.random.default_rng(5).normal(0, 0.01, 3000)
    dr = null_draws(rr, "N_BLOCK", ("G5",))
    q = [np.percentile(dr, [50 * (1 - lv), 50 * (1 + lv)]) for lv in BAND_LEVELS]
    v = float(max(q[0][0] - q[1][0], q[1][0] - q[2][0], q[2][1] - q[1][1], q[1][1] - q[0][1]))
    gate("G5", "band levels NEST: [q(0.95)] contains [q(0.90)] contains [q(0.80)]", v, v >= 0)

    # ------------------------------ G6..G10: replay 1162's 15 and 1164's 72 bit for bit
    P("")
    P("## CROSS-RUN REPLAY — 1162's 15 anchor cells and 1164's 72 population cells")
    prior62 = pd.read_csv(PRIOR1162) if PRIOR1162.exists() else None
    rep_rows = []
    for panel in PANELS:
        for c in ANCHOR_CONTROLS:
            r = anchor_returns(panel, c)
            o, pk, tr = obs_maxdd(r)
            ni = float(np.median(null_draws(r, "N_IID", (panel, c, "N_IID", 0),
                                            base=SEED_1162)))
            nb_ = float(np.median(null_draws(r, "N_BLOCK", (panel, c, "N_BLOCK", 0),
                                             base=SEED_1162)))
            phi = (nb_ - ni) / (o - ni) if abs(o - ni) > 1e-12 else np.nan
            row = dict(parent="1162", cell=f"{panel}/{c}", panel=panel, control=c,
                       observed=o, N_IID=ni, N_BLOCK=nb_, phi_L63=phi)
            if prior62 is not None:
                q_ = prior62[(prior62.panel == panel) & (prior62.control == c)]
                if len(q_):
                    row["prior_observed"] = float(q_.observed.iloc[0])
                    row["prior_phi"] = float(q_.phi_L63.iloc[0])
            rep_rows.append(row)
    prior64 = pd.read_csv(PRIOR1164) if PRIOR1164.exists() else None
    for panel in PANELS:
        for N in POP_N:
            for H in POP_H:
                for f in POP_F:
                    r = pop_returns(panel, N, H, f)
                    o = obs_maxdd(r)[0]
                    ni = float(np.median(null_draws(r, "N_IID", (panel, N, H, f, "I", 0),
                                                    base=SEED_1164)))
                    nb_ = float(np.median(null_draws(r, "N_BLOCK", (panel, N, H, f, "B", 0),
                                                     base=SEED_1164)))
                    phi = (nb_ - ni) / (o - ni) if abs(o - ni) > 1e-12 else np.nan
                    row = dict(parent="1164", cell=f"{panel}/N{N}/H{H}/{f}", panel=panel,
                               control=f"N{N}/H{H}/{f}", observed=o, N_IID=ni, N_BLOCK=nb_,
                               phi_L63=phi)
                    if prior64 is not None:
                        q_ = prior64[(prior64.panel == panel) & (prior64.N == N) &
                                     (prior64.H == H) & (prior64.freq == f)]
                        if len(q_):
                            row["prior_observed"] = float(q_.obs_maxdd.iloc[0])
                            row["prior_phi"] = float(q_.phi_L63.iloc[0])
                    rep_rows.append(row)
    rep = pd.DataFrame(rep_rows)
    if "prior_phi" in rep:
        a = rep[rep.parent == "1162"].dropna(subset=["prior_phi"])
        b = rep[rep.parent == "1164"].dropna(subset=["prior_phi"])
        v = float(np.abs(a.observed - a.prior_observed).max())
        gate("G6", "1162's 15 observed |MaxDD| REPLAYED bit for bit", v, v < 1e-9)
        v = float(np.abs(a.phi_L63 - a.prior_phi).max())
        gate("G7", "1162's 15 phi_L63 REPLAYED bit for bit (its base, its seed parts)",
             v, v < 1e-9)
        v = float(np.abs(b.observed - b.prior_observed).max())
        gate("G8", "1164's 72 observed |MaxDD| REPLAYED bit for bit", v, v < 1e-9)
        v = float(np.abs(b.phi_L63 - b.prior_phi).max())
        gate("G9", "1164's 72 phi_L63 REPLAYED bit for bit (its base, its seed parts)",
             v, v < 1e-9)
        P(f"  replayed {len(a)} of 15 (1162) and {len(b)} of 72 (1164) committed phi cells")
    else:
        P("  a parent cells.csv was not found — the replay gates are SKIPPED and said so.")
    P("")

    # ================================================================ ARM A — THE CENSUS
    P("## ARM A — THE CENSUS: every committed CSV in research/backtests, two layers")
    cen, nfiles = census_scan()
    gate("G10", "census scanned EVERY committed csv in research/backtests (files seen)",
         nfiles, nfiles > 5000)
    P(f"  scanned {nfiles:,} committed CSV files; {len(cen):,} (file, object) hits")
    P("")
    P(f"  {'object':<16s} {'files':>6s} {'rows':>9s} {'publishes denom':>16s} "
      f"{'publishes resolution':>21s}")
    summ_rows = []
    for obj in ["S_PHI", "S_PHI_OTHER", "S_LSTAR", "S_LSTAR_OTHER", "S_BAND",
                "S_BAND_OTHER"]:
        s = cen[cen.object == obj]
        if not len(s):
            continue
        nr = int(s.n_rows.sum())
        pd_ = int(s[s.publishes_denominator].n_rows.sum())
        pr = int(s[s.publishes_resolution].n_rows.sum())
        summ_rows.append(dict(object=obj, files=len(s), rows=nr, rows_with_denominator=pd_,
                              rows_with_resolution=pr,
                              share_denominator=pd_ / nr if nr else np.nan,
                              share_resolution=pr / nr if nr else np.nan))
        P(f"  {obj:<16s} {len(s):6d} {nr:9,d} {pd_ / nr if nr else 0:15.3f} "
          f"{pr / nr if nr else 0:20.3f}")
    summ = pd.DataFrame(summ_rows)
    phi_tok = int(cen[cen.object.isin(["S_PHI", "S_PHI_OTHER"])].n_rows.sum())
    phi_int = int(cen[cen.object == "S_PHI"].n_rows.sum())
    lst_tok = int(cen[cen.object.isin(["S_LSTAR", "S_LSTAR_OTHER"])].n_rows.sum())
    lst_int = int(cen[cen.object == "S_LSTAR"].n_rows.sum())
    P("")
    P(f"  TOKEN vs OBJECT.  `phi` appears on {phi_tok:,} committed rows; only "
      f"{phi_int:,} ({phi_int / phi_tok:.4f}) are the INTERPOLATION weight.")
    P(f"                    `L*` appears on {lst_tok:,} committed rows; only "
      f"{lst_int:,} ({lst_int / lst_tok:.4f}) are the ladder CROSSING.")
    P("  The remainder are DIFFERENT OBJECTS under the same name (the 4b-screen threshold,")
    P("  the shortest callable sub-window, the pool start) with different denominators.")
    P("")
    sent, nsent = sentence_census()
    P(f"  PROSE LAYER: {nsent:,} committed sentences scanned; {len(sent):,} quote one of the")
    P("  three objects WITH a number.")
    for obj in STATISTICS:
        s = sent[sent.object == obj]
        if len(s):
            P(f"    {obj:<8s} {len(s):5d} sentences, {int(s.has_denominator_token.sum()):5d} "
              f"({s.has_denominator_token.mean():.3f}) carry a denominator / resolution token")
    P("")

    # =============================================== ARM B — THE 117 REBUILDABLE PHI CELLS
    P("## ARM B — THE REBUILDABLE CELLS: 1164's 72 books + 1162's 15 anchors + the 3 anchor")
    P(f"  GROSS ladders (15 rungs each) = the record's committed phi population.")
    P(f"  {BDRAWS:,} draws, block L={L_BLOCK}, seeds {SEEDS} (5 per cell), bands "
      f"{BAND_LEVELS} (headline {BAND_HEAD}).")
    series, cell_rows = {}, []

    def cell_measure(key, r, tag, panel, arm, book):
        o = obs_maxdd(r)[0]
        mi, mb, si_, sb_, blo, bhi = [], [], [], [], {lv: [] for lv in BAND_LEVELS}, \
            {lv: [] for lv in BAND_LEVELS}
        for s in SEEDS:
            xi = null_draws(r, "N_IID", (tag, "I", s))
            xb = null_draws(r, "N_BLOCK", (tag, "B", s))
            mi.append(float(np.median(xi)))
            mb.append(float(np.median(xb)))
            si_.append(median_se(xi))
            sb_.append(median_se(xb))
            for lv in BAND_LEVELS:
                lo_, hi_ = np.percentile(xb, [50 * (1 - lv), 50 * (1 + lv)])
                blo[lv].append(float(lo_))
                bhi[lv].append(float(hi_))
        ni, nb_ = mi[0], mb[0]
        denom = o - ni
        phi = (nb_ - ni) / denom if abs(denom) > 1e-12 else np.nan
        phis = [(b - i) / (o - i) for i, b in zip(mi, mb) if abs(o - i) > 1e-12]
        spi, spb = max(mi) - min(mi), max(mb) - min(mb)
        cagr, sh, dd = fmet(r)
        row = dict(cell=key, panel=panel, arm=arm, book=book, n_bars=len(r),
                   observed=o, N_IID=ni, N_BLOCK=nb_, phi_L63=phi, denom=denom,
                   iid_seed_spread=spi, block_seed_spread=spb,
                   se_iid=si_[0], se_block=sb_[0],
                   phi_seed_min=(min(phis) if phis else np.nan),
                   phi_seed_max=(max(phis) if phis else np.nan),
                   phi_seed_spread=(max(phis) - min(phis) if phis else np.nan),
                   CAGR=cagr, Sharpe=sh, MaxDD=dd)
        for lv in BAND_LEVELS:
            row[f"band_lo_{lv}"] = blo[lv][0]
            row[f"band_hi_{lv}"] = bhi[lv][0]
            row[f"band_width_{lv}"] = bhi[lv][0] - blo[lv][0]
            row[f"band_lo_spread_{lv}"] = max(blo[lv]) - min(blo[lv])
            row[f"band_hi_spread_{lv}"] = max(bhi[lv]) - min(bhi[lv])
        for rule in RESOLUTIONS:
            bar = rule_bar(rule, spi, spb, si_[0])
            row[f"bar_{rule}"] = bar
            row[f"phi_est_{rule}"] = bool(abs(denom) >= bar)
            wid = row[f"band_width_{BAND_HEAD}"]
            esp = max(row[f"band_lo_spread_{BAND_HEAD}"], row[f"band_hi_spread_{BAND_HEAD}"])
            bbar = (TSTAT_K * si_[0] if rule == "R_TSTAT"
                    else max(RES_PARAM[rule][0] * esp, RES_PARAM[rule][1]))
            row[f"band_bar_{rule}"] = bbar
            row[f"band_est_{rule}"] = bool(wid >= bbar)
        return row

    for panel in PANELS:
        for N in POP_N:
            for H in POP_H:
                for f in POP_F:
                    key = f"{panel}/N{N}/H{H}/{f}"
                    r = pop_returns(panel, N, H, f)
                    series[key] = r
                    cell_rows.append(cell_measure(key, r, key, panel, "POP",
                                                  f"N{N}/H{H}/{f}"))
        for c in ANCHOR_CONTROLS:
            key = f"{panel}/{c}"
            r = anchor_returns(panel, c)
            series[key] = r
            cell_rows.append(cell_measure(key, r, key, panel, "ANCHOR", c))
        W1, mk = weights_anchor(panel, "C_BOOK")
        for g in GROSS_LADDER:
            key = f"{panel}/g{g:.2f}"
            r = run_weights(panel, W1, mk, g)
            series[key] = r
            cell_rows.append(cell_measure(key, r, key, panel, "GROSS", f"anchor/g{g:.2f}"))
        P(f"  {panel} cells done  ({time.time() - t0:.0f}s)")
    cells = pd.DataFrame(cell_rows)
    P("")
    P(f"  {len(cells)} committed-form phi cells measured "
      f"({int((cells.arm == 'POP').sum())} POP + {int((cells.arm == 'ANCHOR').sum())} ANCHOR "
      f"+ {int((cells.arm == 'GROSS').sum())} GROSS)")
    P(f"  phi over ALL cells runs {cells.phi_L63.min():.2f} .. {cells.phi_L63.max():.2f} "
      f"— an interpolation weight is only meaningful inside [0, 1]")
    P(f"  {int(((cells.phi_L63 < 0) | (cells.phi_L63 > 1)).sum())} of {len(cells)} cells "
      f"({((cells.phi_L63 < 0) | (cells.phi_L63 > 1)).mean():.3f}) publish a phi OUTSIDE "
      f"[0, 1] before any rule is applied.")
    for rule in RESOLUTIONS:
        s = cells[f"phi_est_{rule}"]
        oob = ((cells.phi_L63 < 0) | (cells.phi_L63 > 1)) & s
        P(f"    {rule:<9s} ESTIMABLE {int(s.sum()):3d} of {len(cells)} "
          f"({s.mean():.3f}); of those, {int(oob.sum())} still lie outside [0, 1]")
    est = cells[cells.phi_est_R_1164]
    gate("G11", "every R_1164-ESTIMABLE cell's |denominator| clears its own bar",
         float((abs(est.denom) - est.bar_R_1164).min()),
         bool((abs(est.denom) - est.bar_R_1164).min() >= 0))
    b = cells[(cells.arm == "POP")]
    npop_est = int(b.phi_est_R_1164.sum())
    P(f"  1164's own 72 POP books re-measured with 5 seeds: ESTIMABLE {npop_est} of 72 "
      f"(1164 committed {COMMITTED_1164_ESTIMABLE} of 72 on 3 seeds)")
    P("")

    # ======================================== ARM C — THE LADDER, L* AND ITS SEED STABILITY
    P("## ARM C — THE L LADDER, the crossing L*, and whether the crossing is SEED-STABLE")
    P(f"  {len(L_LADDER) + 1} rungs x {len(LAD_SEEDS)} seeds on every one of the "
      f"{len(cells)} cells.")
    lad_rows, star_rows = [], []
    for _, cr in cells.iterrows():
        key = cr.cell
        r = series[key]
        Tn = len(r)
        rungs = sorted(set([L for L in L_LADDER if L < Tn] + [Tn]))
        o, ni = float(cr.observed), float(cr.N_IID)
        sgn = np.sign(o - ni)
        stars = []
        for s in LAD_SEEDS:
            meds = []
            for L in rungs:
                m = float(np.median(null_draws(r, "N_BLOCK", (key, "LAD", L, s), L=L)))
                meds.append(m)
                if s == LAD_SEEDS[0]:
                    lad_rows.append(dict(cell=key, panel=cr.panel, arm=cr.arm, L=L,
                                         null_median=m, observed=o, N_IID=ni,
                                         phi=((m - ni) / (o - ni)
                                              if abs(o - ni) > 1e-12 else np.nan)))
            reach = [L for L, m in zip(rungs, meds)
                     if sgn * (m - ni) >= sgn * (o - ni) - 1e-12]
            stars.append(float(min(reach)) if reach else np.nan)
        finite = [x for x in stars if np.isfinite(x)]
        stable = bool(len(finite) == len(stars) and len(set(finite)) == 1)
        row = dict(cell=key, panel=cr.panel, arm=cr.arm, L_star=stars[0],
                   L_star_seeds="|".join("NA" if not np.isfinite(x) else f"{x:g}"
                                         for x in stars),
                   L_star_n_distinct=len(set(stars)),
                   L_star_seed_stable=stable, reached=bool(np.isfinite(stars[0])),
                   denom=float(cr.denom))
        for rule in RESOLUTIONS:
            row[f"lstar_est_{rule}"] = bool(cr[f"phi_est_{rule}"] and stable)
            row[f"gap_est_{rule}"] = bool(cr[f"phi_est_{rule}"])
        star_rows.append(row)
    lad = pd.DataFrame(lad_rows)
    star = pd.DataFrame(star_rows)
    nreach = int(star.reached.sum())
    nstab = int(star.L_star_seed_stable.sum())
    P(f"  L* REACHES the observed value on the published ladder at {nreach} of {len(star)} "
      f"cells ({nreach / len(star):.3f})")
    P(f"  L* is SEED-STABLE (identical rung at 3 of 3 seeds) at {nstab} of {len(star)} "
      f"({nstab / len(star):.3f}); among REACHING cells "
      f"{int(star[star.reached].L_star_seed_stable.sum())} of {nreach} "
      f"({star[star.reached].L_star_seed_stable.mean():.3f})")
    P("")

    # =================================================== ARM D — THE BANDS AND THEIR NOISE
    P("## ARM D — THE COMMITTED MOVING-BLOCK BAND and its own endpoint noise")
    band_rows = []
    for _, cr in cells.iterrows():
        for lv in BAND_LEVELS:
            wid = float(cr[f"band_width_{lv}"])
            esp = max(float(cr[f"band_lo_spread_{lv}"]), float(cr[f"band_hi_spread_{lv}"]))
            band_rows.append(dict(cell=cr.cell, panel=cr.panel, arm=cr.arm, level=lv,
                                  lo=float(cr[f"band_lo_{lv}"]), hi=float(cr[f"band_hi_{lv}"]),
                                  width=wid, endpoint_seed_spread=esp,
                                  spread_over_width=(esp / wid if wid > 0 else np.nan),
                                  observed=float(cr.observed),
                                  observed_inside=bool(cr[f"band_lo_{lv}"] <= cr.observed
                                                       <= cr[f"band_hi_{lv}"]),
                                  tenth_rule=bool(wid > 0 and esp <= 0.10 * wid)))
    bands = pd.DataFrame(band_rows)
    bh = bands[bands.level == BAND_HEAD]
    P(f"  at the headline {BAND_HEAD:.0%} level over {len(bh)} cells: median width "
      f"{bh.width.median():.3f} pp, median endpoint cross-seed spread "
      f"{bh.endpoint_seed_spread.median():.3f} pp "
      f"(ratio {bh.spread_over_width.median():.4f})")
    P(f"  the band's own endpoints are resolved to <= 10% of its width at "
      f"{int(bh.tenth_rule.sum())} of {len(bh)} cells ({bh.tenth_rule.mean():.3f})")
    P(f"  the OBSERVED |MaxDD| lies INSIDE its own {BAND_HEAD:.0%} block band at "
      f"{int(bh.observed_inside.sum())} of {len(bh)} cells ({bh.observed_inside.mean():.3f}) "
      f"— a band that never contains the thing it brackets is not a band")
    for lv in BAND_LEVELS:
        s = bands[bands.level == lv]
        P(f"    level {lv:.2f}: width {s.width.median():7.3f} pp  spread/width "
          f"{s.spread_over_width.median():.4f}  inside {s.observed_inside.mean():.3f}")
    P("")

    # ============================================================ ARM E — THE 12-CELL GRID
    P("## ARM E — THE DIAL GRID: 4 RESOLUTION rules x 3 STATISTICS, all 12 published")
    grid_rows = []
    for rule in RESOLUTIONS:
        for stat in STATISTICS:
            if stat == "S_PHI":
                v = cells[f"phi_est_{rule}"].values
            elif stat == "S_LSTAR":
                v = star[f"lstar_est_{rule}"].values
            else:
                v = cells[f"band_est_{rule}"].values
            grid_rows.append(dict(resolution=rule, statistic=stat, n=len(v),
                                  n_estimable=int(v.sum()), share=float(v.mean())))
    grid = pd.DataFrame(grid_rows)
    P(f"  {'':<10s}" + "".join(f"{s:>12s}" for s in STATISTICS))
    for rule in RESOLUTIONS:
        s = grid[grid.resolution == rule].set_index("statistic")
        P(f"  {rule:<10s}" + "".join(f"{s.share[st]:12.3f}" for st in STATISTICS))
    P("")
    agree_rows = []
    for stat, cols in [("S_PHI", cells), ("S_LSTAR", star), ("S_BAND", cells)]:
        pre = "phi_est_" if stat == "S_PHI" else ("lstar_est_" if stat == "S_LSTAR"
                                                  else "band_est_")
        base = cols[f"{pre}R_1164"].values
        for rule in RESOLUTIONS:
            if rule == "R_1164":
                continue
            other = cols[f"{pre}{rule}"].values
            agree_rows.append(dict(statistic=stat, rule=rule,
                                   agree=float((base == other).mean()),
                                   n_disagree=int((base != other).sum()),
                                   n_extra=int((other & ~base).sum()),
                                   n_lost=int((base & ~other).sum())))
    agree = pd.DataFrame(agree_rows)
    P("  AGREEMENT with the incumbent R_1164 (the price of changing the rule):")
    for _, x in agree.iterrows():
        P(f"    {x.statistic:<8s} {x.rule:<9s} agree {x.agree:.3f}  "
          f"(+{int(x.n_extra)} admitted / -{int(x.n_lost)} refused)")
    P("")

    # ================================================================ ARM F' — THE REPAIRS
    P("## ARM F' — PRICING THE REPAIRS the queue names")
    rep_price = []
    n_cells = len(cells)
    draws_5seed = n_cells * len(SEEDS) * 2 * BDRAWS
    draws_1seed = n_cells * 1 * 2 * BDRAWS
    phi_rows_committed = phi_int
    denom_share = float(summ.loc[summ.object == "S_PHI", "share_denominator"].iloc[0]) \
        if (summ.object == "S_PHI").any() else np.nan
    res_share = float(summ.loc[summ.object == "S_PHI", "share_resolution"].iloc[0]) \
        if (summ.object == "S_PHI").any() else np.nan
    rep_price.append(dict(repair="P_NONE", extra_draws=0, extra_columns=0,
                          rows_retained=n_cells, rows_retained_share=1.0,
                          record_rows_already_compliant=phi_rows_committed,
                          note="status quo: the ratio is published alone"))
    rep_price.append(dict(repair="P_DENOM", extra_draws=0, extra_columns=1,
                          rows_retained=n_cells, rows_retained_share=1.0,
                          record_rows_already_compliant=int(denom_share * phi_rows_committed),
                          note=f"publish the denominator beside the ratio; "
                               f"{denom_share:.3f} of committed interp-phi rows already do"))
    rep_price.append(dict(repair="P_TSTAT", extra_draws=0, extra_columns=2,
                          rows_retained=int(cells.phi_est_R_TSTAT.sum()),
                          rows_retained_share=float(cells.phi_est_R_TSTAT.mean()),
                          record_rows_already_compliant=int(res_share * phi_rows_committed),
                          note="the FREE rule: bar = 2 x median SE from the SAME draws"))
    rep_price.append(dict(repair="P_REFUSE", extra_draws=draws_5seed - draws_1seed,
                          extra_columns=3,
                          rows_retained=int(cells.phi_est_R_1164.sum()),
                          rows_retained_share=float(cells.phi_est_R_1164.mean()),
                          record_rows_already_compliant=int(res_share * phi_rows_committed),
                          note="1164's rule: refuse the ratio when it fails the 5-seed bar"))
    rep_price.append(dict(repair="P_INTERVAL", extra_draws=draws_5seed - draws_1seed,
                          extra_columns=2, rows_retained=n_cells, rows_retained_share=1.0,
                          record_rows_already_compliant=int(res_share * phi_rows_committed),
                          note="publish phi as its own cross-seed interval, never a point"))
    rp = pd.DataFrame(rep_price)
    for _, x in rp.iterrows():
        P(f"  {x.repair:<11s} extra draws {int(x.extra_draws):>9,d}  extra cols "
          f"{int(x.extra_columns)}  rows kept {int(x.rows_retained):3d}/{n_cells} "
          f"({x.rows_retained_share:.3f})  {x.note}")
    P("")
    tst = cells.phi_est_R_TSTAT.values
    inc = cells.phi_est_R_1164.values
    P(f"  THE CHEAP-vs-EXPENSIVE COMPARISON: R_TSTAT agrees with R_1164 on "
      f"{(tst == inc).mean():.3f} of the {n_cells} cells "
      f"(+{int((tst & ~inc).sum())} admitted / -{int((inc & ~tst).sum())} refused).")
    P(f"  Median |denominator| {np.median(np.abs(cells.denom)):.3f} pp against a median "
      f"R_1164 bar of {cells.bar_R_1164.median():.3f} pp and a median R_TSTAT bar of "
      f"{cells.bar_R_TSTAT.median():.3f} pp.")
    P(f"  Median cross-seed phi spread over R_1164-estimable cells "
      f"{est.phi_seed_spread.median():.4f} — the RESOLUTION of every phi the record quotes.")
    P("")

    # ---------------------------------------------------------------- hypotheses
    P("## HYPOTHESES — scored against the bars declared before any result")
    hyp("H_TOKEN", ">=90% of committed `phi` rows are the INTERPOLATION object",
        f"{phi_int:,} of {phi_tok:,} = {phi_int / phi_tok:.4f}",
        bool(phi_int / phi_tok >= 0.90))
    hyp("H_CENSUS", ">=90% of committed INTERPOLATION-phi rows publish their denominator",
        f"{denom_share:.4f}", bool(denom_share >= 0.90))
    hyp("H_ESTIM", ">=50% of the rebuildable phi cells ESTIMABLE under R_1164",
        f"{int(inc.sum())} of {n_cells} = {inc.mean():.4f}", bool(inc.mean() >= 0.50))
    ag3 = agree[(agree.statistic == "S_PHI") & (agree.rule.isin(["R_STRICT", "R_LOOSE"]))]
    hyp("H_RULE", "R_1164 vs R_STRICT and R_LOOSE agree on >=90% of phi cells",
        "/".join(f"{x.rule} {x.agree:.3f}" for _, x in ag3.iterrows()),
        bool((ag3.agree >= 0.90).all()))
    ch = []
    for stat, cols in [("S_PHI", cells), ("S_LSTAR", star), ("S_BAND", cells)]:
        pre = "phi_est_" if stat == "S_PHI" else ("lstar_est_" if stat == "S_LSTAR"
                                                  else "band_est_")
        ch.append((stat, float((cols[f"{pre}R_1164"].values ==
                                cols[f"{pre}R_TSTAT"].values).mean())))
    hyp("H_CHEAP", "the FREE R_TSTAT agrees with R_1164 on >=90% of cells, all 3 statistics",
        "/".join(f"{s} {a:.3f}" for s, a in ch), bool(all(a >= 0.90 for _, a in ch)))
    hyp("H_LSTAR", "the committed crossing L* is seed-stable at >=90% of cells",
        f"{nstab} of {len(star)} = {nstab / len(star):.4f}",
        bool(nstab / len(star) >= 0.90))
    hyp("H_BAND", "band endpoint spread <= 10% of width at >=90% of cells",
        f"{int(bh.tenth_rule.sum())} of {len(bh)} = {bh.tenth_rule.mean():.4f}",
        bool(bh.tenth_rule.mean() >= 0.90))
    P("")

    # ================================ ARM F — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS
    P("## ARM F — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS (PROTOCOL rules 4 and 8)")
    P("  Every one of the 117 books at its own gross, ALL published (the 15 anchor")
    P("  control cells are NOT books and are excluded here).  Parameters are chosen")
    P("  on 2009-2016 ONLY by three IS choosers and scored on the untouched 2017-2026")
    P("  window.  The ESTIMABILITY RULE is then priced in CAPITAL terms: the same choosers")
    P("  restricted to the books whose phi is ESTIMABLE under each rule.")
    wf_rows, bench = [], {}
    for panel in PANELS:
        d = panels[panel]
        sp = d["px"]["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(sp, d["warm"], d["ins"], d["oos"])
        lv = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST,
                      freq="W")["returns"].values
        lb = blocks_m(lv, d["warm"], d["ins"], d["oos"])
        bench[panel] = (sb, lb)
        P(f"  {panel:<6s} SPY  {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%} "
          f"(H {sb['H1']:.4f}/{sb['H2']:.4f})  OOS {sb['OOS_CAGR']:7.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:7.2%}")
        P(f"  {panel:<6s} v2   {lb['CAGR']:7.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:7.2%} "
          f"(H {lb['H1']:.4f}/{lb['H2']:.4f})  OOS {lb['OOS_CAGR']:7.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:7.2%}")
        ins_t, oos_t = d["ins"][d["warm"]], d["oos"][d["warm"]]
        for _, cr in cells[(cells.panel == panel) & (cells.arm != "ANCHOR")].iterrows():
            r = series[cr.cell]
            b = blocks_m(r, np.ones(len(r), dtype=bool), ins_t, oos_t)
            l4b, l4o, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            row = dict(panel=panel, arm=cr.arm, cell=cr.cell, book=cr.book, **b, **l4b,
                       **l4o, **l4a, pass_4b_full=all(l4b.values()),
                       pass_4b_oos=all(l4o.values()), pass_4a=all(l4a.values()),
                       phi_L63=cr.phi_L63, denom=cr.denom)
            for rule in RESOLUTIONS:
                row[f"phi_est_{rule}"] = bool(cr[f"phi_est_{rule}"])
            wf_rows.append(row)
    wf = pd.DataFrame(wf_rows)
    a = wf[(wf.panel == "U56") & (wf.book == "N20/H126/W")].iloc[0]
    b_ = wf[(wf.panel == "U56") & (wf.book == "anchor/g0.75")].iloc[0]
    v = max(abs(a.CAGR - b_.CAGR), abs(a.Sharpe - b_.Sharpe), abs(a.MaxDD - b_.MaxDD))
    gate("G12", "the population's N20/H126/W IS the anchor book at gross 0.75", v, v < 1e-12)
    P("")
    P(f"  BASE RATES over all {len(wf)} books: 4b full {int(wf.pass_4b_full.sum())}, "
      f"4b OOS {int(wf.pass_4b_oos.sum())}, 4a {int(wf.pass_4a.sum())}")
    for panel in PANELS:
        s = wf[wf.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.pass_4b_full.sum()):3d}/{len(s)}  "
          f"4b OOS {int(s.pass_4b_oos.sum()):3d}/{len(s)}  4a {int(s.pass_4a.sum()):3d}/{len(s)}")
    pick_rows = []
    for panel in PANELS:
        sb, lb = bench[panel]
        pools = {"ALL": wf[wf.panel == panel]}
        for rule in RESOLUTIONS:
            pools[f"EST_{rule}"] = wf[(wf.panel == panel) & wf[f"phi_est_{rule}"]]
        for pname, s in pools.items():
            if not len(s):
                P(f"  {panel} {pname}: EMPTY pool — no book survives; no pick made.")
                continue
            for cname, key in CHOOSERS.items():
                x = s.loc[s[key].idxmax()]
                pick_rows.append(dict(panel=panel, pool=pname, n_pool=len(s), chooser=cname,
                                      pick=x.book, IS_Sharpe=x.IS_Sharpe, CAGR=x.CAGR,
                                      Sharpe=x.Sharpe, MaxDD=x.MaxDD, OOS_CAGR=x.OOS_CAGR,
                                      OOS_Sharpe=x.OOS_Sharpe, OOS_MaxDD=x.OOS_MaxDD,
                                      SPY_OOS_CAGR=sb["OOS_CAGR"],
                                      SPY_OOS_Sharpe=sb["OOS_Sharpe"],
                                      SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                                      v2_OOS_Sharpe=lb["OOS_Sharpe"],
                                      pass_4b_full=bool(x.pass_4b_full),
                                      pass_4b_oos=bool(x.pass_4b_oos),
                                      pass_4a=bool(x.pass_4a)))
    picks = pd.DataFrame(pick_rows)
    P("")
    P("  RULE-8 PICKS (chosen on 2009..2016 IS only, scored on the untouched OOS window):")
    P(f"  {'panel':<6s} {'pool':<14s} {'n':>4s} {'chooser':<11s} {'pick':<16s} "
      f"{'OOS CAGR':>9s} {'OOS Shrp':>9s} {'OOS DD':>8s} {'4bF':>5s} {'4bO':>5s} {'4a':>4s}")
    for _, x in picks.iterrows():
        P(f"  {x.panel:<6s} {x['pool']:<14s} {int(x.n_pool):4d} {x.chooser:<11s} "
          f"{x['pick']:<16s} {x.OOS_CAGR:9.2%} {x.OOS_Sharpe:9.4f} {x.OOS_MaxDD:8.2%} "
          f"{str(bool(x.pass_4b_full)):>5s} {str(bool(x.pass_4b_oos)):>5s} "
          f"{str(bool(x.pass_4a)):>4s}")
    P("")
    P("  THE CAPITAL CONTENT OF THE REPAIR — restricted pool vs ALL, same chooser:")
    cap_rows = []
    for panel in PANELS:
        for cname in CHOOSERS:
            base = picks[(picks.panel == panel) & (picks["pool"] == "ALL") &
                         (picks.chooser == cname)]
            if not len(base):
                continue
            b0 = base.iloc[0]
            for rule in RESOLUTIONS:
                s = picks[(picks.panel == panel) & (picks["pool"] == f"EST_{rule}") &
                          (picks.chooser == cname)]
                if not len(s):
                    continue
                x = s.iloc[0]
                cap_rows.append(dict(panel=panel, chooser=cname, rule=rule,
                                     pick_all=b0["pick"], pick_est=x["pick"],
                                     same_pick=bool(b0["pick"] == x["pick"]),
                                     dOOS_Sharpe=float(x.OOS_Sharpe - b0.OOS_Sharpe),
                                     dOOS_CAGR=float(x.OOS_CAGR - b0.OOS_CAGR),
                                     dOOS_MaxDD=float(x.OOS_MaxDD - b0.OOS_MaxDD)))
    cap = pd.DataFrame(cap_rows)
    if len(cap):
        nsame = int(cap.same_pick.sum())
        nmove = int((cap.dOOS_Sharpe.abs() >= 0.05).sum())
        P(f"    the restriction leaves the pick UNCHANGED at {nsame} of {len(cap)} "
          f"(panel, chooser, rule) cells ({nsame / len(cap):.3f})")
        P(f"    |dOOS Sharpe| >= 0.05 at {nmove} of {len(cap)} ({nmove / len(cap):.3f}); "
          f"median dOOS Sharpe {cap.dOOS_Sharpe.median():+.4f}, "
          f"max |d| {cap.dOOS_Sharpe.abs().max():.4f}")
        for _, x in cap[~cap.same_pick].iterrows():
            P(f"      MOVED {x.panel:<6s} {x.chooser:<11s} {x.rule:<9s} "
              f"{x.pick_all} -> {x.pick_est}   dOOS Sharpe {x.dOOS_Sharpe:+.4f}")
        hyp("H_CAPITAL", "|dOOS Sharpe| >= 0.05 at >= half the (panel, chooser, rule) cells",
            f"{nmove} of {len(cap)} = {nmove / len(cap):.4f}",
            bool(nmove / len(cap) >= 0.50))
    else:
        hyp("H_CAPITAL", "|dOOS Sharpe| >= 0.05 at >= half the cells",
            "no restricted pool was non-empty", False)
    best = wf[wf.pass_4b_full & wf.pass_4b_oos]
    P("")
    if len(best):
        for _, bb in best.sort_values("OOS_Sharpe", ascending=False).head(5).iterrows():
            reach = bool(((picks.panel == bb.panel) & (picks["pick"] == bb.book)).any())
            P(f"  4b FULL+OOS: {bb.panel:<6s} {bb.book:<16s} full {bb.CAGR:7.2%} / "
              f"{bb.Sharpe:.4f} / {bb.MaxDD:7.2%} (H {bb.H1:.4f}/{bb.H2:.4f})  OOS "
              f"{bb.OOS_CAGR:7.2%} / {bb.OOS_Sharpe:.4f} / {bb.OOS_MaxDD:7.2%}  "
              f"IS-chooser-reachable {'YES' if reach else 'NO'}")
    else:
        P("  NO book clears 4b FULL and 4b OOS anywhere on this grid.")
    P(f"  4a passes: {int(wf.pass_4a.sum())} of {len(wf)} books and "
      f"{int(picks.pass_4a.sum())} of {len(picks)} picks.")
    P("")

    # ---------------------------------------------------------------------- outputs
    P("## OUTPUTS")
    dump(pd.DataFrame(GATES), "gates")
    dump(pd.DataFrame(HYP), "hypotheses")
    dump(rep, "replay")
    dump(cen, "census")
    dump(summ, "census_summary")
    dump(sent, "sentences")
    dump(cells, "cells")
    dump(lad, "ladder")
    dump(star, "lstar")
    dump(bands, "bands")
    dump(grid, "dialgrid")
    dump(agree, "agreement")
    dump(rp, "repairs")
    dump(wf, "walkforward")
    dump(picks, "picks")
    if len(cap):
        dump(cap, "capital")
    P("")
    P(f"GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS   "
      f"HYPOTHESES {sum(h['supported'] for h in HYP)} of {len(HYP)} SUPPORTED")
    P(f"runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return cells, grid, wf, picks


if __name__ == "__main__":
    main()
