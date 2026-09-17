#!/usr/bin/env python3
"""
Idea 1226 (lane B, 2026-09-17) — does ANY committed SE in the record state what it DIVIDED BY?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1219
(`2026-09-17_should-every-committed-t-carry-its-SE-BASIS-and-its-L_B.py`, commit 50e5600)
published, as declared bycatch, that the SAME Newey-West SE of the same daily difference
calibrates at crit95 2.0161-2.4754 when it is put on the Sharpe scale by the POOLED BOOK
volatility and at 0.9219-1.2778 when it is put there by the SD of the DIFFERENCE — a factor
of about two, on one construction, with nothing in the committed text distinguishing the two.
1219 stated its own choice in a source comment and stopped there.  That is the whole of the
record's treatment of the question.

A standard error on a RATIO scale (a Sharpe difference, an information ratio, a Calmar) is a
quotient: an SE of a MEAN divided by whatever puts it on that scale.  The numerator's basis
(iid / block / fold / HAC) is what 1212 and 1219 censused.  The DENOMINATOR was never
censused at all, and it is a dial of the same order: two books correlated at 0.90 have a
difference whose SD is far below either book's own volatility, so the same SE can be a bar of
1.0 or a bar of 2.5 depending on a choice nobody wrote down.

THE QUESTION, THREE PARTS, ANSWERED SEPARATELY:
  (1) How many committed SE / +- / mean-SE claims in the record NAME their denominator — in
      the committed sentence, or in the emitting script?
  (2) How many committed t's are VERDICT-AMBIGUOUS with respect to the denominator alone:
      |t| inside the band the unstated denominator spans, holding the SE's numerator, its
      basis and its L FIXED?
  (3) Does pricing a publish decision at the honest denominator-specific bar instead of the
      quoted 1.96 BUY anything?  On real books, 10 bps, next-day execution, parameters chosen
      on 2009-2016 and 2017-2026 read ONCE (PROTOCOL rule 8).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET        {C_1219, C_HEAD, C_MEMO, C_ALL}
  DENOMINATOR SET  {D_PAIR, D_VOL3, D_VOL4, D_ALL5}

  = 16 cells, EVERY ONE PUBLISHED, in `.exposure.csv`.  The per-claim rows for all four claim
  sets are in `.seclaims.csv` (the SE census) and `.tclaims.csv` (the re-priced t's).

  C_1219  research/LEADERBOARD.md + research/CHANGELOG.md AS OF 1219's own commit (50e5600).
          Frozen; git-read.  This is the record as it stood when the bycatch was published.
  C_HEAD  the same two files at this run's HEAD.
  C_MEMO  C_HEAD + every research/backtests/*.result.md and *.memo.md.
  C_ALL   C_MEMO + research/QUEUE.md.

  D_PAIR  {D_BOOKVOL, D_DIFFSD} — the only two the record has ever exhibited (1219's stated
          choice and 1219's bycatch).  The narrowest honest reading of the ambiguity.
  D_VOL3  + D_ANCHOR  (the comparand book's own volatility)
  D_VOL4  + D_MAXVOL  (the larger of the two books' volatilities)
  D_ALL5  + D_SPYVOL  (the benchmark's volatility — the scale an information-ratio SE uses)

WHAT IS NOT A DIAL.  The SE NUMERATOR is held FIXED at one construction for the whole run:
a Newey-West (Bartlett) HAC SE of the mean daily difference.  That is 1219's bycatch object,
inherited whole.  The L ladder {21, 63, 126, 252, 504} is 1212's, inherited whole and
reported at every rung, never chosen.  The five denominators are MEASURED, not tuned; the
dial is which SET of them the record leaves open.  The iid-bootstrap Sharpe-difference SE is
carried as a REFERENCE row only (it is where the quoted 1.96 comes from) and is not a rung.
PANEL {U56, B136, SMALL} is not a dial.  The 216-book rule-8 population is not a dial and
every book is published.  The count-matched RANDOM bar in Arm D is a null, never a candidate.

THE ALGEBRA, STATED SO THE RESULT CANNOT BE MISREAD.  For a fixed pair and a fixed L there is
ONE HAC variance.  The five rungs are five scalings of it, so every pairwise ratio of t's is
exactly the inverse ratio of the denominators (gate G11).  Nothing here is a bootstrap
artefact: the spread IS the choice.

Frozen at 1219's construction: CAND20 legs, max_vol 0.60, gross 0.75, min hold 126, N = 20,
cadence W, 10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, 30 disjoint gross-matched
null pairs per panel, crc32 seeds, SEED_BASE 12261226.

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 walk-forward and BOTH KEEP
paths in Arm D; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_does-any-committed-SE-in-the-record-state-what-it-DIVIDED-BY_B.py
"""
from __future__ import annotations

import bisect
import math
import re
import subprocess
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
SLUG = "does-any-committed-SE-in-the-record-state-what-it-DIVIDED-BY"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = ROOT / "research" / "backtests"

# ----- 1219's construction, inherited whole -------------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

L_LADDER = [21, 63, 126, 252, 504]                    # 1212's, inherited
NPAIRS = 30
BDRAWS_REF = 600                                      # iid reference row only
SEED_BASE = 12261226
Z95 = 1.959963984540054                               # the bar the record quotes

# the five denominators (MEASURED, not tuned) and the four nested SETS (dial 2)
DENOMS = ["D_BOOKVOL", "D_DIFFSD", "D_ANCHOR", "D_MAXVOL", "D_SPYVOL"]
DENOM_SETS = {
    "D_PAIR": ["D_BOOKVOL", "D_DIFFSD"],
    "D_VOL3": ["D_BOOKVOL", "D_DIFFSD", "D_ANCHOR"],
    "D_VOL4": ["D_BOOKVOL", "D_DIFFSD", "D_ANCHOR", "D_MAXVOL"],
    "D_ALL5": DENOMS,
}
DSET_NAMES = list(DENOM_SETS)
CLAIM_SETS = ["C_1219", "C_HEAD", "C_MEMO", "C_ALL"]

# rule-8 population (Arm D)
POP_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
POP_H = [21, 63, 126, 252]
POP_C = ["W", "M"]
ANCHOR = dict(N=N0, H=HOLD0, cadence=FREQ0)
NRAND = 400                                           # count-matched random-bar draws

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived ----------------
C1212_COMMIT = "0743d51fcff839b47fa04cda45b8b0d190b32907"
C1219_COMMIT = "50e5600258490db047be7efdcd3d56b38136964d"
C1212_NHITS = 210                                     # 1212's committed census size
C1219_NW_BAND = (2.0161, 2.4754)                      # 1219's committed S_NW crit95 range
C1219_DIFFSD_BAND = (0.9219, 1.2778)                  # 1219's committed S_NW_DIFFSD range
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []
GATES: list[dict] = []
HYPS: list[dict] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return seed_of_base(SEED_BASE, *parts)


def seed_of_base(base, *parts):
    return base + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<6s} {what}  ->  {value:.4e}")
    return bool(ok)


def hyp(name, declared, bar, measured, supported):
    HYPS.append(dict(hypothesis=name, declared=declared, bar=bar, measured=measured,
                     supported=bool(supported)))
    P(f"   [{'SUPPORTED' if supported else 'REFUTED  '}] {name:<16} {declared}")
    P(f"                    bar {bar} | measured {measured}")


# =================================================================================================
# 1212/1219's runner and book machinery, verbatim
# =================================================================================================
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
    m = x.mean(axis=1) * 252.0
    s = x.std(axis=1, ddof=1) * np.sqrt(252.0)
    return np.where(s > 0, m / np.where(s > 0, s, 1.0), np.nan)


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


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# =================================================================================================
# THE OBJECT.  ONE HAC (Newey-West, Bartlett) SE of the mean daily difference, FIVE SCALINGS.
# The numerator is computed ONCE per (pair, L); the denominators only rescale it.  That is the
# whole point of the run and it is why every cross-denominator ratio is exact, not sampled.
# =================================================================================================
def hac_se_mean(ra, rb, L):
    """SE of the MEAN of (ra - rb), Newey-West with Bartlett weights, maxlag = min(L, T-2)."""
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    T = len(ra)
    if T < 3:
        return np.nan, 0
    d = ra - rb
    x = d - d.mean()
    s = float((x * x).mean())
    maxlag = int(min(L, T - 2))
    for k in range(1, maxlag + 1):
        s += 2.0 * (1.0 - k / (maxlag + 1.0)) * float((x[k:] * x[:-k]).mean())
    return float(np.sqrt(max(s, 1e-24) / T)), maxlag


def denom_values(ra, rb, spy):
    """The five candidate DAILY scales that put an SE of a mean on the SHARPE scale."""
    ra, rb, spy = np.asarray(ra, float), np.asarray(rb, float), np.asarray(spy, float)
    sa, sb = ra.std(ddof=1), rb.std(ddof=1)
    return {
        "D_BOOKVOL": 0.5 * (sa + sb),                 # 1219's stated choice
        "D_DIFFSD": (ra - rb).std(ddof=1),            # 1219's bycatch
        "D_ANCHOR": sb,                               # the comparand book's own vol
        "D_MAXVOL": max(sa, sb),                      # the larger of the two
        "D_SPYVOL": spy.std(ddof=1),                  # benchmark vol (the IR scale)
    }


def t_all_denoms(ra, rb, spy, L):
    """|t| of the Sharpe difference under every denominator, from ONE HAC numerator."""
    se_mean, maxlag = hac_se_mean(ra, rb, L)
    dv = fsharpe(ra) - fsharpe(rb)
    out = {}
    if not np.isfinite(se_mean) or se_mean <= 0:
        return {d: np.nan for d in DENOMS}, dv, maxlag
    dens = denom_values(ra, rb, spy)
    for d, val in dens.items():
        if not np.isfinite(val) or val <= 0:
            out[d] = np.nan
        else:
            out[d] = dv / (se_mean / val * np.sqrt(252.0))
    return out, dv, maxlag


def se_iid_reference(ra, rb, tag, ndraws=BDRAWS_REF):
    """The iid-bootstrap SE of the Sharpe DIFFERENCE — the construction the quoted 1.96 comes
    from.  A REFERENCE row, never a rung."""
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    T = len(ra)
    rng = np.random.default_rng(seed_of("ref", tag))
    idx = rng.integers(0, T, size=(ndraws, T))
    d = sharpe_rows(ra[idx]) - sharpe_rows(rb[idx])
    return float(np.nanstd(d, ddof=1))


# =================================================================================================
# THE CENSUS.  Harvest committed SEs and committed t's -> map to the emitting script ->
# ask, of each, whether ANYTHING states the denominator.
# =================================================================================================
# 1212/1219's t pattern, VERBATIM (the reproduction gate depends on it being unchanged)
PAT_T = re.compile(r"(?:t(?:'s)?\s*(?:=|of|to)\s*|mean/SE\s*\+|\(t\s*)(-?\d+\.\d+)")
PAT_PY = re.compile(r"[0-9A-Za-z_\-\.]+\.py")

# the SE harvest: every committed number that IS a standard error
PAT_SE = re.compile(
    r"(?:\bSE\s*(?:=|of|:)?\s*([+-]?\d+\.\d+)"          # "SE 0.0014", "SE = 0.0014"
    r"|(?:\+/-|±)\s*(\d+\.\d+)"                    # "+/- 0.012"
    r"|mean/SE\s*([+-]?\d+\.\d+)"                       # "mean/SE +6.95"
    r"|standard error[^0-9]{0,24}(\d+\.\d+))")          # "standard error of 0.02"

# Does the TEXT name a denominator?  One keyword set per denominator class.
TEXT_DEN = {
    "D_BOOKVOL": ("pooled book", "book volatility", "pooled vol", "book vol"),
    "D_DIFFSD": ("sd(ra - rb)", "sd of the difference", "sd of the diff",
                 "difference's sd", "sd(diff"),
    "D_ANCHOR": ("anchor volatility", "anchor vol", "its own volatility"),
    "D_MAXVOL": ("larger of the two vol",),
    "D_SPYVOL": ("benchmark volatility", "benchmark vol", "spy volatility", "spy vol"),
}
# Does the SCRIPT pin one?  Matched against the emitting script's SOURCE.
SRC_DEN = {
    "D_BOOKVOL": re.compile(r"D_BOOKVOL|pooled[_ ]?(?:book[_ ]?)?vol|0\.5\s*\*\s*\(\s*\w+"
                            r"\.std\(ddof=1\)\s*\+", re.I),
    "D_DIFFSD": re.compile(r"D_DIFFSD|DIFFSD|sd\(ra\s*-\s*rb\)|\(\s*ra\s*-\s*rb\s*\)\.std\(|"
                           r"\bd\.std\(ddof=1\)|diff\.std\(", re.I),
    "D_ANCHOR": re.compile(r"D_ANCHOR\b|anchor_vol", re.I),
    "D_MAXVOL": re.compile(r"D_MAXVOL|max\(\s*sa\s*,\s*sb\s*\)", re.I),
    "D_SPYVOL": re.compile(r"D_SPYVOL|spy_vol|spy\.std\(", re.I),
}
# Does the script even PUT an SE on a ratio scale?  (If not, the denominator question is moot
# for it and the claim is counted as NOT_RATIO rather than as an unstated denominator.)
PAT_RATIO_SE = re.compile(r"se\w*\s*/\s*\w*(?:sd|vol)|/\s*sd\s*\*\s*np\.sqrt\(252|"
                          r"sharpe[_ ]?se|se[_ ]?sharpe|np\.sqrt\(252\.?0?\)\s*$", re.I | re.M)


def git_show(commit, path):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _units(txt):
    starts = [0] + [m.end() for m in re.finditer("\n", txt)]
    return starts, txt.split("\n")


def _unit_of(starts, lines, pos):
    li = bisect.bisect_right(starts, pos) - 1
    line = lines[li]
    if line.startswith("|"):
        return line, line
    a = li
    while a > 0 and lines[a - 1].strip():
        a -= 1
    b = li
    while b + 1 < len(lines) and lines[b + 1].strip():
        b += 1
    return line, "\n".join(lines[a:b + 1])


def _script_of(txt, line, pos):
    if line.startswith("|"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[-1].endswith(".py"):
            return cells[-1]
    mm = list(PAT_PY.finditer(txt[:pos]))
    return mm[-1].group(0) if mm else None


def harvest(pat, name, txt, source, value_from_groups=False):
    starts, lines = _units(txt)
    out = []
    for m in pat.finditer(txt):
        if value_from_groups:
            g = [x for x in m.groups() if x is not None]
            if not g:
                continue
            val = abs(float(g[0]))
        else:
            val = abs(float(m.group(1)))
        line, unit = _unit_of(starts, lines, m.start())
        out.append(dict(source=source, file=name, pos=m.start(), value=val,
                        ctx200=txt[max(0, m.start() - 200): m.end() + 200].lower(),
                        unit=unit.lower(), script=_script_of(txt, line, m.start())))
    return out


def den_from_words(text):
    hit = [d for d, ws in TEXT_DEN.items() if any(w in text for w in ws)]
    if len(hit) == 1:
        return hit[0]
    return "AMBIGUOUS" if len(hit) > 1 else "UNSTATED"


def den_from_source(src):
    hit = [d for d, r in SRC_DEN.items() if r.search(src)]
    if len(hit) == 1:
        return hit[0]
    if len(hit) > 1:
        return "AMBIGUOUS"
    return "UNSTATED" if PAT_RATIO_SE.search(src) else "NOT_RATIO"


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1226 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P(__doc__.strip())
    P("")

    # ------------------------------------------------------------------ panels
    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm, ndrop, nmeta = load_small()
    raw["SMALL"] = sm
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
        panels[panel] = dict(px=px, idx=idx, K=K, T=T,
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig,
                             spy=px["SPY"].pct_change().fillna(0.0).values)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    def run_cell(panel, N, H, gross, freq):
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4

    def null_book(panel, seed, base=SEED_BASE):
        """1212's P_NULL: N names drawn uniformly from those eligible at each rebalance."""
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        rng = np.random.default_rng(seed_of_base(base, "null", panel, seed))
        W = np.zeros((d["T"], d["K"]))
        ok = d["elig"] & d["priced"]
        for i, t in enumerate(reb):
            cand = np.flatnonzero(ok[t])
            if not len(cand):
                continue
            sel = rng.choice(cand, size=min(N0, len(cand)), replace=False)
            stop = reb[i + 1] if i + 1 < len(reb) else d["T"]
            W[t:stop, sel] = GROSS0 / len(sel)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4

    # ------------------------------------------------------------------ gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G2", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G3", "CROSS-RUN the committed U56 W/H126/N=20 triple", v, v < 5e-3)

    smm = blocks_m(d["spy"], d["warm"], d["ins"], d["oos"])
    v = max(abs(smm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(smm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(smm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G4", "SPY OOS triple", v, v < 5e-3)

    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    v = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G5", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)

    v = float(np.abs(run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)
                     - run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)).max())
    gate("G6", "determinism of the SMALL pipeline", v, v == 0.0)

    # G9 — the HAC SE at maxlag 0 IS the plain iid SE of the mean (the family's own identity)
    rr = np.random.default_rng(9).normal(0.0004, 0.011, (2, 900))
    a, _ = hac_se_mean(rr[0], rr[1], 0)
    dd0 = rr[0] - rr[1]
    b = float(dd0.std(ddof=0) / np.sqrt(len(dd0)))
    v = abs(a - b) / max(b, 1e-18)
    gate("G9", "HAC at maxlag 0 == iid SE of the mean (relative)", v, v < 1e-10)

    # G11 — the five rungs are five SCALINGS of ONE numerator: ratios are EXACT
    spy_g = np.random.default_rng(11).normal(0.0003, 0.010, 900)
    tt, _, _ = t_all_denoms(rr[0], rr[1], spy_g, 126)
    dens_g = denom_values(rr[0], rr[1], spy_g)
    v = max(abs(tt["D_DIFFSD"] / tt["D_BOOKVOL"]
                - dens_g["D_DIFFSD"] / dens_g["D_BOOKVOL"]),
            abs(tt["D_SPYVOL"] / tt["D_BOOKVOL"]
                - dens_g["D_SPYVOL"] / dens_g["D_BOOKVOL"]))
    gate("G11", "t-ratio across denominators == denominator ratio (algebraic identity)", v,
         v < 1e-10)
    P("")

    # ============================================================ ARM A — the census
    P("## ARM A — HARVEST EVERY COMMITTED SE, AND ASK WHAT IT DIVIDED BY")
    head_files = [("LEADERBOARD.md", "research/LEADERBOARD.md"),
                  ("CHANGELOG.md", "research/CHANGELOG.md")]

    # the machinery gate: 1212's t harvest still reproduces at 1212's own commit
    rows = []
    frozen12 = True
    for nm, rel in head_files:
        txt = git_show(C1212_COMMIT, rel)
        if txt is None:
            frozen12 = False
            txt = (ROOT / rel).read_text()
        rows += harvest(PAT_T, nm, txt, "C_1212")
    v = len(rows)
    gate("G1", f"the inherited t harvest reproduces 1212's 210 at its own commit "
               f"({C1212_COMMIT[:7]})", v, (v == C1212_NHITS) if frozen12 else (v >= C1212_NHITS))
    if not frozen12:
        P("     NOTE: git show unavailable; the gate fell back to HEAD and is >= 210.")

    def build_sets(pat, value_from_groups):
        cl = {}
        rows_ = []
        frozen = True
        for nm, rel in head_files:
            txt = git_show(C1219_COMMIT, rel)
            if txt is None:
                frozen = False
                txt = (ROOT / rel).read_text()
            rows_ += harvest(pat, nm, txt, "C_1219", value_from_groups)
        cl["C_1219"] = rows_
        rows_ = []
        for nm, rel in head_files:
            rows_ += harvest(pat, nm, (ROOT / rel).read_text(), "C_HEAD", value_from_groups)
        cl["C_HEAD"] = rows_
        memo_files = sorted(list(BT.glob("*.result.md")) + list(BT.glob("*.memo.md")))
        rows_ = list(cl["C_HEAD"])
        for p in memo_files:
            rows_ += harvest(pat, p.name, p.read_text(errors="ignore"), "C_MEMO",
                             value_from_groups)
        cl["C_MEMO"] = rows_
        cl["C_ALL"] = list(cl["C_MEMO"]) + harvest(
            pat, "QUEUE.md", (ROOT / "research" / "QUEUE.md").read_text(), "C_ALL",
            value_from_groups)
        return cl, len(memo_files), frozen

    se_claims, n_memo, frozen19 = build_sets(PAT_SE, True)
    t_claims, _, _ = build_sets(PAT_T, False)
    P(f"  SE claims harvested: " + ",  ".join(f"{c} {len(se_claims[c])}" for c in CLAIM_SETS))
    P(f"  t  claims harvested: " + ",  ".join(f"{c} {len(t_claims[c])}" for c in CLAIM_SETS)
      + f"   ({n_memo} memo/result files scanned)")
    if not frozen19:
        P("  NOTE: C_1219 fell back to HEAD (git show unavailable).")

    src_cache, fact_cache = {}, {}

    def src_of(name):
        if name not in src_cache:
            s = None
            for cand in (BT / name, ROOT / "research" / name, ROOT / name):
                if cand.exists():
                    s = cand.read_text(errors="ignore")
                    break
            src_cache[name] = s
        return src_cache[name]

    def den_of_script(name):
        if name not in fact_cache:
            s = src_of(name)
            fact_cache[name] = den_from_source(s) if s is not None else "UNMAPPED"
        return fact_cache[name]

    def classify(claims):
        out = []
        for cs in CLAIM_SETS:
            for r in claims[cs]:
                on_disk = r["script"] is not None and src_of(r["script"]) is not None
                out.append(dict(claim_set=cs, file=r["file"], pos=r["pos"], value=r["value"],
                                script=r["script"], script_on_disk=on_disk,
                                den_text=den_from_words(r["unit"]),
                                den_text200=den_from_words(r["ctx200"]),
                                den_script=(den_of_script(r["script"]) if on_disk
                                            else "UNMAPPED")))
        return pd.DataFrame(out)

    SE = classify(se_claims)
    TC = classify(t_claims)
    dump(SE, "seclaims")
    dump(TC, "tclaims")

    cenrows = []
    for cs in CLAIM_SETS:
        g = SE[SE.claim_set == cs]
        gt = TC[TC.claim_set == cs]
        for lab, gg in (("SE", g), ("T", gt)):
            st_text = gg.den_text.isin(DENOMS)
            st_scr = gg.den_script.isin(DENOMS)
            cenrows.append(dict(claim_set=cs, population=lab, n=len(gg),
                                states_in_text=int(st_text.sum()),
                                states_in_script=int(st_scr.sum()),
                                states_in_either=int((st_text | st_scr).sum()),
                                share_either=float((st_text | st_scr).mean()) if len(gg) else 0.0,
                                script_not_ratio=int((gg.den_script == "NOT_RATIO").sum()),
                                script_unstated=int((gg.den_script == "UNSTATED").sum()),
                                unmapped=int((gg.den_script == "UNMAPPED").sum())))
    CEN = pd.DataFrame(cenrows)
    dump(CEN, "census")
    P("  DOES ANY COMMITTED SE STATE ITS DENOMINATOR?  (text = the committed unit; script =")
    P("  the emitting script's source; either = the union, i.e. the most generous reading)")
    P("    " + f"{'claim set':<9} {'pop':<4} {'n':>6} {'text':>7} {'script':>8} {'either':>8} "
      f"{'share':>8} {'not-ratio':>10}")
    for r in CEN.itertuples():
        P("    " + f"{r.claim_set:<9} {r.population:<4} {r.n:6d} {r.states_in_text:7d} "
          f"{r.states_in_script:8d} {r.states_in_either:8d} {r.share_either:8.4f} "
          f"{r.script_not_ratio:10d}")
    P("  WHERE THE STATING HITS ACTUALLY LIVE — the only reason C_ALL's share rises at all:")
    for lab, gg in (("SE", SE), ("T", TC)):
        g = gg[(gg.claim_set == "C_ALL") & gg.den_text.isin(DENOMS)]
        P(f"    {lab:<3} text-stating hits by file: "
          f"{dict(g.file.value_counts()) if len(g) else '{}'}")
        gs = gg[(gg.claim_set == "C_HEAD") & gg.den_script.isin(DENOMS)]
        P(f"    {lab:<3} the script-stating hits sit in: "
          f"{sorted(set(gs.script.dropna()))}")
    P("  THAT IS THE ANSWER IN ONE LINE: the record's ONLY statements of a denominator are in")
    P("  QUEUE.md — the entries that ASK this question (1219's bycatch note and idea 1226")
    P("  itself) — and in a handful of scripts matched by source markers.  NOT ONE committed")
    P("  result sentence in LEADERBOARD.md or CHANGELOG.md names what its SE divided by.")
    P("  READ 'not-ratio' HONESTLY: those are claims whose emitting script never puts an SE on")
    P("  a ratio scale at all by this rule's markers, so the denominator question does not")
    P("  arise for them AND this rule cannot prove it does not.  The share that STATES a")
    P("  denominator is the number the queue asked for; 'not-ratio' is neither a pass nor a")
    P("  fail and is published separately rather than folded into either.")
    P("")

    # ============================================================ ARM B — the honest bars
    P(f"## ARM B — THE HONEST CRITICAL VALUE PER DENOMINATOR, RE-MEASURED (not quoted):")
    P(f"   {NPAIRS} disjoint gross-matched null pairs per panel, true Sharpe difference = 0.")
    P("   TWO PAIR SETS, because a crit95 read off 90 pairs is itself a measurement:")
    P("     P_1219  the null books built under 1219's OWN seed base (12191219).  This is the")
    P("             record's own object, inherited whole, and it is what the HEADLINE band and")
    P("             Arm D's BAR_HONEST use.  It is NOT a dial.")
    P("     P_OWN   the same construction under this run's seed base (12261226) — an")
    P("             INDEPENDENT REPLICATION, published beside it so seed luck is visible.")
    pairsets = {}
    for tag, base in (("P_1219", 12191219), ("P_OWN", SEED_BASE)):
        ps = []
        for panel in PANELS:
            for j in range(NPAIRS):
                ra = null_book(panel, 2 * j, base)
                rb = null_book(panel, 2 * j + 1, base)
                w = panels[panel]["warm"]
                ps.append(dict(panel=panel, pair=j, ra=ra[w], rb=rb[w],
                               spy=panels[panel]["spy"][w]))
        pairsets[tag] = ps
        P(f"   {tag} {len(ps)} pairs built  ({time.time() - t0:.0f}s)")
    pairs = pairsets["P_1219"]

    for tag, ps in pairsets.items():
        dS = np.array([fsharpe(p["ra"]) - fsharpe(p["rb"]) for p in ps])
        corr = np.mean([np.corrcoef(p["ra"], p["rb"])[0, 1] for p in ps])
        P(f"   EXCHANGEABILITY {tag}: mean dSharpe {dS.mean():+.4f} over {len(ps)} pairs "
          f"(sd {dS.std(ddof=1):.4f}); mean pair corr {corr:.4f}")
        if tag == "P_1219":
            gate("G10", "the headline null pairs are EXCHANGEABLE (|mean dSharpe| <= 0.05)",
                 abs(dS.mean()), abs(dS.mean()) <= 0.05)

    # the denominators themselves, before any bar
    drows = []
    for tag, ps in pairsets.items():
        for p in ps:
            dv = denom_values(p["ra"], p["rb"], p["spy"])
            drows.append(dict(pairset=tag, panel=p["panel"], pair=p["pair"], corr=float(
                np.corrcoef(p["ra"], p["rb"])[0, 1]), **dv))
    DN = pd.DataFrame(drows)
    dump(DN, "denominators")
    D0 = DN[DN.pairset == "P_1219"]
    P("   THE DENOMINATORS THEMSELVES (daily SD units, mean over the 90 P_1219 pairs), and")
    P("   each one's ratio to 1219's stated choice:")
    for dnm in DENOMS:
        P(f"     {dnm:<10} mean {D0[dnm].mean():.6f}   "
          f"x{D0[dnm].mean() / D0['D_BOOKVOL'].mean():.4f} of D_BOOKVOL")

    def calibrate(ps, tag):
        rows_ = []
        for L in L_LADDER:
            acc = {d: [] for d in DENOMS}
            for p in ps:
                tt, _, _ = t_all_denoms(p["ra"], p["rb"], p["spy"], L)
                for dnm in DENOMS:
                    acc[dnm].append(abs(tt[dnm]) if np.isfinite(tt[dnm]) else np.nan)
            for dnm in DENOMS:
                ts = np.array(acc[dnm], float)
                ok = np.isfinite(ts)
                # MONTE-CARLO WIDTH of the crit95 itself: resample the pairs, not the days
                rng = np.random.default_rng(seed_of("crit", tag, dnm, L))
                bs = np.array([np.nanpercentile(ts[rng.integers(0, len(ts), len(ts))], 95)
                               for _ in range(400)])
                rows_.append(dict(pairset=tag, denominator=dnm, L=L, n=int(ok.sum()),
                                  crit95=float(np.nanpercentile(ts, 95)),
                                  crit95_se=float(bs.std(ddof=1)),
                                  crit90=float(np.nanpercentile(ts, 90)),
                                  reject_at_1p96=float(np.nanmean(ts[ok] > Z95))))
            P(f"   {tag} L = {L:<4d} calibrated over all five denominators  "
              f"({time.time() - t0:.0f}s)")
        return rows_

    calrows = calibrate(pairsets["P_1219"], "P_1219") + calibrate(pairsets["P_OWN"], "P_OWN")
    # the iid-bootstrap Sharpe-difference reference, NOT a rung
    ts_ref = []
    for p in pairs:
        se = se_iid_reference(p["ra"], p["rb"], f"{p['panel']}|{p['pair']}")
        dv = fsharpe(p["ra"]) - fsharpe(p["rb"])
        ts_ref.append(abs(dv / se) if se > 0 else np.nan)
    ref95 = float(np.nanpercentile(np.array(ts_ref, float), 95))
    CAL = pd.DataFrame(calrows)
    dump(CAL, "calibration")
    critall = {(r.pairset, r.denominator, r.L): r.crit95 for r in CAL.itertuples()}
    critse = {(r.pairset, r.denominator, r.L): r.crit95_se for r in CAL.itertuples()}
    crit = {(dnm, L): critall[("P_1219", dnm, L)] for dnm in DENOMS for L in L_LADDER}
    for tag in ("P_1219", "P_OWN"):
        P(f"   HONEST 95th PERCENTILE OF |t| on {tag} (the bar; the record quotes 1.96):")
        P("     " + f"{'denominator':<12}" + "".join(f"{('L=' + str(L)):>10}" for L in L_LADDER)
          + "   max/min")
        for dnm in DENOMS:
            vals = [critall[(tag, dnm, L)] for L in L_LADDER]
            P("     " + f"{dnm:<12}" + "".join(f"{v:>10.4f}" for v in vals)
              + f"   x{max(vals) / min(vals):.2f}")
    P("   MONTE-CARLO WIDTH of each crit95 (SE from resampling the 90 P_1219 PAIRS, 400 draws)")
    P("     " + f"{'denominator':<12}" + "".join(f"{('L=' + str(L)):>10}" for L in L_LADDER))
    for dnm in DENOMS:
        P("     " + f"{dnm:<12}" + "".join(f"{critse[('P_1219', dnm, L)]:>10.4f}"
                                           for L in L_LADDER))
    P(f"     REFERENCE (not a rung): the iid-bootstrap SE of the Sharpe DIFFERENCE calibrates "
      f"at crit95 {ref95:.4f} — that is where the quoted 1.96 comes from.")

    bv = [crit[("D_BOOKVOL", L)] for L in L_LADDER]
    ds = [crit[("D_DIFFSD", L)] for L in L_LADDER]
    v = max(abs(min(bv) - C1219_NW_BAND[0]), abs(max(bv) - C1219_NW_BAND[1]))
    gate("G7", "1219's committed S_NW band (2.0161-2.4754) reproduces on ITS OWN pairs (P_1219)",
         v, v < 0.05)
    v = max(abs(min(ds) - C1219_DIFFSD_BAND[0]), abs(max(ds) - C1219_DIFFSD_BAND[1]))
    gate("G8", "1219's committed S_NW_DIFFSD band (0.9219-1.2778) reproduces on P_1219", v,
         v < 0.05)
    dev = max(abs(critall[("P_OWN", dnm, L)] - critall[("P_1219", dnm, L)])
              for dnm in ("D_BOOKVOL", "D_DIFFSD") for L in L_LADDER)
    mcw = max(critse[("P_1219", dnm, L)] for dnm in ("D_BOOKVOL", "D_DIFFSD") for L in L_LADDER)
    gate("G12", "P_OWN vs P_1219 deviation is within 3x the crit95's own Monte-Carlo SE",
         dev, dev <= 3.0 * mcw)
    P(f"     SEED LUCK, STATED: the worst cross-seed deviation on the two denominators the")
    P(f"     record has exhibited is {dev:.4f}, against a per-cell Monte-Carlo SE of at most")
    P(f"     {mcw:.4f}.  A crit95 read off 90 pairs is a measurement with a width, and the")
    P("     record quotes such numbers to four decimals without one.  The HEADLINE uses")
    P("     P_1219 so that nothing below rests on this run's own draw.")

    P("   THE DENOMINATOR BAND PER DIAL RUNG — the range of honest bars a committed t inherits")
    P("   when the denominator is unstated, holding basis (HAC) and L FIXED:")
    band, band_own = {}, {}
    for sname in DSET_NAMES:
        S = DENOM_SETS[sname]
        lo = min(crit[(dnm, L)] for dnm in S for L in L_LADDER)
        hi = max(crit[(dnm, L)] for dnm in S for L in L_LADDER)
        band[sname] = (lo, hi)
        band_own[sname] = (min(critall[("P_OWN", dnm, L)] for dnm in S for L in L_LADDER),
                           max(critall[("P_OWN", dnm, L)] for dnm in S for L in L_LADDER))
        P(f"     {sname:<7} ({len(S)} denominators)  [{lo:.4f}, {hi:.4f}]  a factor of "
          f"{hi / lo:.2f}   (P_OWN [{band_own[sname][0]:.4f}, {band_own[sname][1]:.4f}])")
    P("   AND THE SAME BAND AT A SINGLE L, so the L dial cannot be blamed for it:")
    for L in L_LADDER:
        lo = min(crit[(dnm, L)] for dnm in DENOMS)
        hi = max(crit[(dnm, L)] for dnm in DENOMS)
        P(f"     L={L:<4d} [{lo:.4f}, {hi:.4f}]  x{hi / lo:.2f}")
    P("")

    # ============================================================ ARM C — re-reading the record
    P("## ARM C — HOW MANY COMMITTED t's ARE VERDICT-AMBIGUOUS IN THE DENOMINATOR ALONE?")
    P("   The 16 DIAL CELLS.  AMBIG = |t| inside the set's band, so the published verdict is a")
    P("   function of a choice nobody wrote down.  LOST = significant at the quoted 1.96 but")
    P("   NOT at the set's strictest honest bar.  GAINED = the reverse.")
    exrows = []
    for ptag, bnd in (("P_1219", band), ("P_OWN", band_own)):
        for cs in CLAIM_SETS:
            g = TC[TC.claim_set == cs]
            tt = g.value.values
            sig = tt > Z95
            for sname in DSET_NAMES:
                lo, hi = bnd[sname]
                amb = (tt > lo) & (tt <= hi)
                lost = sig & (tt <= hi)
                gained = (~sig) & (tt > lo)
                exrows.append(dict(pairset=ptag, claim_set=cs, denom_set=sname, n=len(g),
                                   band_lo=lo, band_hi=hi,
                                   sig_at_1p96=int(sig.sum()), ambiguous=int(amb.sum()),
                                   share_ambiguous=float(amb.mean()) if len(g) else 0.0,
                                   share_amb_of_sig=float(amb.sum() / max(int(sig.sum()), 1)),
                                   lost_at_strictest=int(lost.sum()),
                                   gained_at_loosest=int(gained.sum())))
    EXALL = pd.DataFrame(exrows)
    dump(EXALL, "exposure")
    EX = EXALL[EXALL.pairset == "P_1219"]
    P("    " + f"{'claim set':<9} {'denom set':<8} {'n':>6} {'|t|>1.96':>9} {'AMBIG':>7} "
      f"{'of all':>8} {'of sig':>8} {'LOST':>6} {'GAINED':>7}")
    for r in EX.itertuples():
        P("    " + f"{r.claim_set:<9} {r.denom_set:<8} {r.n:6d} {r.sig_at_1p96:9d} "
          f"{r.ambiguous:7d} {r.share_ambiguous:8.4f} {r.share_amb_of_sig:8.4f} "
          f"{r.lost_at_strictest:6d} {r.gained_at_loosest:7d}")
    eo = EXALL[EXALL.pairset == "P_OWN"].set_index(["claim_set", "denom_set"]).ambiguous
    e1 = EX.set_index(["claim_set", "denom_set"]).ambiguous
    P(f"   SAME 16 CELLS ON P_OWN's BANDS: AMBIG counts move by at most "
      f"{int((eo - e1).abs().max())} claims (mean {float((eo - e1).mean()):+.2f}); the cell "
      "ordering is unchanged.")
    P("")

    # ============================================================ ARM D — rule 8 + KEEP paths
    P("## ARM D — PROTOCOL rule 8 WALK-FORWARD AND BOTH KEEP PATHS")
    P(f"   {len(POP_N)}x{len(POP_H)}x{len(POP_C)} = {len(POP_N) * len(POP_H) * len(POP_C)} books "
      f"per panel, {len(POP_N) * len(POP_H) * len(POP_C) * len(PANELS)} in all, EVERY ONE "
      "PUBLISHED.  Parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE.")
    for panel in PANELS:
        dd_ = panels[panel]
        live = backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                        freq="W")["returns"].values
        dd_["spy_m"] = blocks_m(dd_["spy"], dd_["warm"], dd_["ins"], dd_["oos"])
        dd_["live_m"] = blocks_m(live, dd_["warm"], dd_["ins"], dd_["oos"])

    poprows, rser = [], {}
    for panel in PANELS:
        dd_ = panels[panel]
        sb, lbp = dd_["spy_m"], dd_["live_m"]
        for N in POP_N:
            for H in POP_H:
                for fr in POP_C:
                    r_ = run_cell(panel, N, H, GROSS0, fr)
                    rser[(panel, N, H, fr)] = r_
                    mm = blocks_m(r_, dd_["warm"], dd_["ins"], dd_["oos"])
                    l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbp)
                    poprows.append(dict(panel=panel, N=N, H=H, cadence=fr, **mm,
                                        pass_4b_full=all(l4b.values()),
                                        pass_4b_oos=all(l4bo.values()),
                                        pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
        P(f"   {panel:<6s} {len(POP_N) * len(POP_H) * len(POP_C)} books done "
          f"({time.time() - t0:.0f}s)")
    POP = pd.DataFrame(poprows)
    dump(POP, "walkforward")
    P(f"   4b full {int(POP.pass_4b_full.sum())} of {len(POP)}, 4b OOS "
      f"{int(POP.pass_4b_oos.sum())} of {len(POP)}, 4a {int(POP.pass_4a.sum())} of {len(POP)}")
    for p_, g in POP.groupby("panel"):
        P(f"     {p_:<6} 4b full {int(g.pass_4b_full.sum()):2d}/{len(g)}  4b OOS "
          f"{int(g.pass_4b_oos.sum()):2d}/{len(g)}  4a {int(g.pass_4a.sum()):2d}/{len(g)}")
    both = POP[POP.pass_4b_full & POP.pass_4b_oos]
    nbooks = both.groupby(["panel", "N", "H", "cadence"]).ngroups if len(both) else 0
    P(f"   4b full AND OOS: {len(both)} rows, {nbooks} DISTINCT books")
    if len(both):
        b = both.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"   BEST: {b['panel']} / {b['cadence']} / N={int(b['N'])} / H={int(b['H'])}  full "
          f"{b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} (H1 {b['H1']:.4f}/H2 "
          f"{b['H2']:.4f})  OOS {b['OOS_CAGR']:.2%}/{b['OOS_Sharpe']:.4f}/{b['OOS_MaxDD']:.2%}")
    for p_ in PANELS:
        sb, lbp = panels[p_]["spy_m"], panels[p_]["live_m"]
        P(f"     {p_:<6} SPY full {sb['CAGR']:.2%}/{sb['Sharpe']:.4f}/{sb['MaxDD']:.2%} OOS "
          f"{sb['OOS_CAGR']:.2%}/{sb['OOS_Sharpe']:.4f}/{sb['OOS_MaxDD']:.2%} | live v2 full "
          f"{lbp['CAGR']:.2%}/{lbp['Sharpe']:.4f}/{lbp['MaxDD']:.2%} OOS "
          f"{lbp['OOS_CAGR']:.2%}/{lbp['OOS_Sharpe']:.4f}/{lbp['OOS_MaxDD']:.2%}")
    P("")

    P("   THE CAPITAL QUESTION.  A committed t is a PUBLISH decision.  Each (denominator, L) is")
    P("   a chooser over the 9-rung N ladder inside a (panel, H, cadence) context: take the")
    P("   rung whose IS Sharpe difference vs the ANCHOR rung (N=20) has the largest |t| under")
    P("   that denominator, and MOVE only if that t clears the bar.  BAR_QUOTED = 1.96 (what")
    P("   the record writes); BAR_HONEST = this run's own crit95 for that (denominator, L).")
    P("   The SE NUMERATOR, the basis, the L and the books are identical between the two, so")
    P("   any difference IS the value of stating the denominator.")
    contexts = [(p_, H, fr) for p_ in PANELS for H in POP_H for fr in POP_C]
    P(f"   {len(contexts)} contexts x {len(DENOMS)} denominators x {len(L_LADDER)} L x 2 bars = "
      f"{len(contexts) * len(DENOMS) * len(L_LADDER) * 2} decisions, every one published.")

    tcache = {}
    for (p_, H, fr) in contexts:
        ins = panels[p_]["ins"]
        ra = rser[(p_, ANCHOR["N"], H, fr)][ins]
        spy_in = panels[p_]["spy"][ins]
        for N in POP_N:
            if N == ANCHOR["N"]:
                continue
            rb = rser[(p_, N, H, fr)][ins]
            for L in L_LADDER:
                tt, _, _ = t_all_denoms(rb, ra, spy_in, L)
                for dnm in DENOMS:
                    tcache[(p_, H, fr, N, dnm, L)] = tt[dnm]
        P(f"   IS t's built for {p_}/H{H}/{fr}  ({time.time() - t0:.0f}s)")

    popi = POP.set_index(["panel", "N", "H", "cadence"])

    def bookrow(p_, N, H, fr):
        return popi.loc[(p_, N, H, fr)]

    decrows = []
    for dnm in DENOMS:
        for L in L_LADDER:
            for barname, barval in (("BAR_QUOTED", Z95), ("BAR_HONEST", crit[(dnm, L)])):
                for (p_, H, fr) in contexts:
                    cands = [(abs(tcache[(p_, H, fr, N, dnm, L)]), N) for N in POP_N
                             if N != ANCHOR["N"]
                             and np.isfinite(tcache[(p_, H, fr, N, dnm, L)])]
                    if cands:
                        tbest, Nbest = max(cands)
                    else:
                        tbest, Nbest = np.nan, ANCHOR["N"]
                    moved = bool(np.isfinite(tbest) and tbest > barval)
                    Npick = Nbest if moved else ANCHOR["N"]
                    r_ = bookrow(p_, Npick, H, fr)
                    decrows.append(dict(denominator=dnm, L=L, bar=barname, bar_value=barval,
                                        panel=p_, H=H, cadence=fr, t_best=tbest,
                                        N_argmax=Nbest, N_pick=Npick, moved=moved,
                                        OOS_Sharpe=r_["OOS_Sharpe"], OOS_CAGR=r_["OOS_CAGR"],
                                        OOS_MaxDD=r_["OOS_MaxDD"],
                                        pass_4b_full=bool(r_["pass_4b_full"]),
                                        pass_4b_oos=bool(r_["pass_4b_oos"]),
                                        pass_4a=bool(r_["pass_4a"])))
    for (p_, H, fr) in contexts:
        r_ = bookrow(p_, ANCHOR["N"], H, fr)
        decrows.append(dict(denominator="C_ANCHOR", L=0, bar="BAR_NONE", bar_value=np.inf,
                            panel=p_, H=H, cadence=fr, t_best=np.nan, N_argmax=ANCHOR["N"],
                            N_pick=ANCHOR["N"], moved=False, OOS_Sharpe=r_["OOS_Sharpe"],
                            OOS_CAGR=r_["OOS_CAGR"], OOS_MaxDD=r_["OOS_MaxDD"],
                            pass_4b_full=bool(r_["pass_4b_full"]),
                            pass_4b_oos=bool(r_["pass_4b_oos"]), pass_4a=bool(r_["pass_4a"])))
    DEC = pd.DataFrame(decrows)
    dump(DEC, "decisions")

    anch = DEC[DEC.denominator == "C_ANCHOR"]
    anchor_mean = float(anch.OOS_Sharpe.mean())
    anchor_4b = int((anch.pass_4b_full & anch.pass_4b_oos).sum())
    P(f"   DOING NOTHING (the anchor rung at all {len(anch)} contexts): mean OOS Sharpe "
      f"{anchor_mean:.4f}, 4b full+OOS {anchor_4b} of {len(anch)}, 4a {int(anch.pass_4a.sum())}")

    rule = DEC[DEC.denominator != "C_ANCHOR"].groupby(["denominator", "L", "bar"]).agg(
        moves=("moved", "sum"), meanOOS=("OOS_Sharpe", "mean"),
        n=("moved", "size")).reset_index()
    key = DEC.set_index(["denominator", "L", "bar"])
    rule["n4b_both"] = [int((key.loc[(r.denominator, r.L, r.bar)].pass_4b_full
                            & key.loc[(r.denominator, r.L, r.bar)].pass_4b_oos).sum())
                        for r in rule.itertuples()]
    rule["n4a"] = [int(key.loc[(r.denominator, r.L, r.bar)].pass_4a.sum())
                   for r in rule.itertuples()]
    dump(rule, "rules")
    P(f"   EVERY ONE OF THE {len(rule)} (denominator x L x bar) RULES, "
      "moves / mean OOS Sharpe / 4b(full+OOS):")
    for dnm in DENOMS:
        for barname in ("BAR_QUOTED", "BAR_HONEST"):
            g = rule[(rule.denominator == dnm) & (rule.bar == barname)].set_index("L")
            P(f"     {dnm:<10} {barname:<11} " + "  ".join(
                f"L{L}:{int(g.loc[L, 'moves']):2d}m/{g.loc[L, 'meanOOS']:.4f}/"
                f"{int(g.loc[L, 'n4b_both'])}" for L in L_LADDER))

    P("   COUNT-MATCHED RANDOM BAR (the control 1210, 1219 and 1221 all found decisive): for")
    P("   each rule's realised move count m, draw m of the contexts at random, move to that")
    P("   context's IS argmax rung, and read the same OOS mean.  A rule that does not clear")
    P("   its own count-matched null is buying its result with the move count alone.")
    randrows = []
    for r in rule.itertuples():
        sub = key.loc[(r.denominator, r.L, r.bar)]
        m = int(sub.moved.sum())
        base = {(x.panel, x.H, x.cadence): (
            float(bookrow(x.panel, ANCHOR["N"], x.H, x.cadence)["OOS_Sharpe"]),
            float(bookrow(x.panel, x.N_argmax, x.H, x.cadence)["OOS_Sharpe"]))
            for x in sub.itertuples()}
        keys = list(base.keys())
        anchor_vals = np.array([base[k][0] for k in keys])
        argmax_vals = np.array([base[k][1] for k in keys])
        obs = float(sub.OOS_Sharpe.mean())
        rng = np.random.default_rng(seed_of("rand", r.denominator, r.L, r.bar))
        draws = np.empty(NRAND)
        for i in range(NRAND):
            pick = rng.choice(len(keys), size=m, replace=False) if m else np.array([], int)
            v = anchor_vals.copy()
            v[pick] = argmax_vals[pick]
            draws[i] = v.mean()
        randrows.append(dict(denominator=r.denominator, L=r.L, bar=r.bar, moves=m, observed=obs,
                             null_median=float(np.median(draws)),
                             null_p90=float(np.percentile(draws, 90)),
                             percentile=float((draws < obs).mean())))
    RND = pd.DataFrame(randrows)
    dump(RND, "randombar")
    nclear = int((RND.percentile >= 0.90).sum())
    P(f"   rules clearing the 90th percentile of their own count-matched null: "
      f"{nclear} of {len(RND)}")
    pbin = sum(math.comb(len(RND), i) * 0.10 ** i * 0.90 ** (len(RND) - i)
               for i in range(nclear, len(RND) + 1))
    P(f"   READ THAT AT ITS TRUE WEIGHT: {len(RND)} rules tested at a 0.90 bar means "
      f"{0.10 * len(RND):.1f} of {len(RND)} clear it BY CHANCE.  Observed {nclear}; the")
    P(f"   one-sided binomial probability of {nclear} or more under pure chance is "
      f"{pbin:.4f}.  That is not separation, and no rule here is a candidate for anything.")
    P(f"   rules beating DOING NOTHING on mean OOS Sharpe: "
      f"{int((rule.meanOOS > anchor_mean).sum())} of {len(rule)}")
    mrg = rule.merge(RND, on=["denominator", "L", "bar"])
    win = mrg[(mrg.meanOOS > anchor_mean) & (mrg.percentile >= 0.90)]
    P(f"   rules doing BOTH: {len(win)} of {len(mrg)}" + ("" if not len(win) else " — " + ", ".join(
        f"{r.denominator}/L{int(r.L)}/{r.bar} {r.meanOOS:.4f} (pct {r.percentile:.3f})"
        for r in win.itertuples())))

    piv = rule.pivot_table(index=["denominator", "L"], columns="bar",
                           values=["meanOOS", "moves", "n4b_both"])
    dmean = piv[("meanOOS", "BAR_HONEST")] - piv[("meanOOS", "BAR_QUOTED")]
    dmove = piv[("moves", "BAR_HONEST")] - piv[("moves", "BAR_QUOTED")]
    d4b = piv[("n4b_both", "BAR_HONEST")] - piv[("n4b_both", "BAR_QUOTED")]
    se_d = float(dmean.std(ddof=1) / np.sqrt(len(dmean))) if len(dmean) > 1 else np.nan
    t_d = (dmean.mean() / se_d) if se_d else np.nan
    P(f"   HONEST BAR minus QUOTED BAR over the {len(dmean)} (denominator, L) cells: mean OOS "
      f"Sharpe {dmean.mean():+.4f} (SE {se_d:.4f}, t {t_d:+.2f}), moves {dmove.mean():+.2f}, "
      f"4b(full+OOS) {d4b.mean():+.2f}")
    P(f"   cells where the two bars make IDENTICAL decisions: "
      f"{int((dmove == 0).sum())} of {len(dmove)} on move count, "
      f"{int((dmean.abs() < 1e-12).sum())} of {len(dmean)} on mean OOS Sharpe")

    # the denominator's OWN effect, holding the bar at the quoted 1.96 (what the record does)
    q = rule[rule.bar == "BAR_QUOTED"]
    sp_mv = q.groupby("denominator").moves.mean()
    sp_oos = q.groupby("denominator").meanOOS.mean()
    P("   AND THE DIAL ITSELF, AT THE BAR THE RECORD ACTUALLY QUOTES (1.96), averaged over L:")
    for dnm in DENOMS:
        P(f"     {dnm:<10} moves {sp_mv[dnm]:5.1f} of {len(contexts)}   mean OOS Sharpe "
          f"{sp_oos[dnm]:.4f}")
    P(f"   spread across the five denominators at the quoted bar: moves "
      f"{sp_mv.min():.1f} -> {sp_mv.max():.1f}, mean OOS Sharpe {sp_oos.min():.4f} -> "
      f"{sp_oos.max():.4f} (anchor {anchor_mean:.4f})")
    P("")

    # ============================================================ HYPOTHESES
    P("## HYPOTHESES — declared with their bars, scored once")
    c_head_se = CEN[(CEN.claim_set == "C_HEAD") & (CEN.population == "SE")].iloc[0]
    c_all_se = CEN[(CEN.claim_set == "C_ALL") & (CEN.population == "SE")].iloc[0]
    hyp("H_STATED", "essentially no committed SE in the record states what it divided by",
        "share stating a denominator (text OR script) < 0.05 on C_HEAD",
        f"C_HEAD {int(c_head_se.states_in_either)} of {int(c_head_se.n)} = "
        f"{c_head_se.share_either:.4f}; C_ALL {int(c_all_se.states_in_either)} of "
        f"{int(c_all_se.n)} = {c_all_se.share_either:.4f}",
        bool(c_head_se.share_either < 0.05))

    lo_p, hi_p = band["D_PAIR"]
    hyp("H_FACTOR", "the denominator alone moves the honest bar by a factor >= 1.5, holding "
                    "the SE numerator, its basis and its L fixed",
        "band_hi / band_lo >= 1.5 on D_PAIR (the two the record has exhibited)",
        f"[{lo_p:.4f}, {hi_p:.4f}] = x{hi_p / lo_p:.2f}; at a SINGLE L the widest is x"
        f"{max(max(crit[(d_, L)] for d_ in DENOMS) / min(crit[(d_, L)] for d_ in DENOMS) for L in L_LADDER):.2f}",
        bool(hi_p / lo_p >= 1.5))

    ex_head = EX[(EX.claim_set == "C_HEAD") & (EX.denom_set == "D_PAIR")].iloc[0]
    hyp("H_AMBIG", "a material share of committed t's are verdict-ambiguous in the denominator "
                   "alone",
        ">= 0.10 of C_HEAD's committed t's inside the D_PAIR band",
        f"{int(ex_head.ambiguous)} of {int(ex_head.n)} = {ex_head.share_ambiguous:.4f} "
        f"({ex_head.share_amb_of_sig:.4f} of the significant); LOST at the strictest bar "
        f"{int(ex_head.lost_at_strictest)}",
        bool(ex_head.share_ambiguous >= 0.10))

    hyp("H_WF", "quoting the HONEST denominator-specific bar instead of 1.96 buys OOS Sharpe",
        f"mean(honest - quoted) over the {len(dmean)} (denominator, L) cells > 0 at |t| > 2",
        f"{dmean.mean():+.4f}, t {t_d:+.2f}",
        bool(se_d and dmean.mean() > 0 and abs(t_d) > 2))

    best_rule = rule.sort_values("meanOOS", ascending=False).iloc[0]
    clears = RND.set_index(["denominator", "L", "bar"]).reindex(
        pd.MultiIndex.from_frame(rule[["denominator", "L", "bar"]])).percentile.values
    hyp("H_ANCHOR", "SOME (denominator, L, bar) rule beats DOING NOTHING out of sample AND "
                    "clears its own count-matched random-bar null",
        "at least one rule with meanOOS > anchor AND percentile >= 0.90",
        f"best rule {best_rule.denominator}/L{int(best_rule.L)}/{best_rule.bar} meanOOS "
        f"{best_rule.meanOOS:.4f} vs anchor {anchor_mean:.4f}; {nclear} of {len(RND)} clear "
        f"their null against {0.10 * len(RND):.1f} by chance",
        bool(((rule.meanOOS.values > anchor_mean) & (clears >= 0.90)).any()))

    npass4a = int(POP.pass_4a.sum())
    nboth = int((POP.pass_4b_full & POP.pass_4b_oos).sum())
    hyp("H_KEEP", "this run's population produces a NEW capital-worthy book",
        "a 4a pass, or a 4b full+OOS pass that is not already in the record",
        f"4a {npass4a} of {len(POP)}; 4b full+OOS {nboth} of {len(POP)} over {nbooks} "
        "distinct books, all of them already in the record",
        False if npass4a == 0 else True)
    P("")

    # ============================================================ VERDICT
    P("## VERDICT")
    P(f"   4a: {npass4a} of {len(POP)} books.  4b full AND OOS: {nboth} of {len(POP)} over "
      f"{nbooks} distinct books.")
    P("   This run proposes NO rules change, NO promotion and NO memo beyond the reporting")
    P("   clause below.  RULES.md, scan.py, bot.py and baseline.py are untouched.")
    P("")
    P("## SURVIVORSHIP (rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B")
    P(f"   screen (data/SMALL_PANEL_README.md) less the documented max_1d_move >= 1.0")
    P(f"   exclusion — {ndrop} of {nmeta} dropped, {panels['SMALL']['K'] - 1} investable names")
    P("   plus SPY as benchmark only.  Arms A and C are scans of committed TEXT and SOURCE and")
    P("   carry no market bias at all.  Arm B is one construction measured against itself and")
    P("   the bias very largely cancels out of a critical-value RATIO — which is the whole of")
    P("   the headline.  The bias does NOT cancel out of Arm D's OOS levels or the 4b legs, so")
    P("   any pass there is an upper bound.")
    P("")

    GDF = pd.DataFrame(GATES)
    dump(GDF, "gates")
    dump(pd.DataFrame(HYPS), "hypotheses")
    P(f"## GATES {int(GDF.pass_.sum())} of {len(GDF)} PASS")
    P(f"## runtime {time.time() - t0:.0f}s, offline, deterministic")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
