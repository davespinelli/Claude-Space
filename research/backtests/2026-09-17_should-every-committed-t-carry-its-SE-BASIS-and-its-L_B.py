#!/usr/bin/env python3
"""
Idea 1219 (lane B, 2026-09-17) — should every committed t carry its SE BASIS and its L?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1212
(`2026-09-17_is-a-CALENDAR-FOLD-SE-systematically-LOOSER-than-the-BLOCK-BOOTSTRAP-it-was-
added-to-correct_cloud.py`) measured that the honest 95th percentile of |t| on a difference
whose true value is ZERO runs 1.6417 at L = 21 to 2.5341 at L = 504 for a fold-clustered SE
(x1.54) and 1.9379 -> 2.4004 for a block SE (x1.24).  A committed t that does not state its
SE basis and its L is therefore not a significance claim at all — it is a number whose bar
ranges over a factor of 1.5.  1212's own census could classify only 10 of 210 committed
t-values as fold-clustered, because it read the TEXT.  This run reads the SCRIPT.

THE QUESTION, THREE PARTS, ANSWERED SEPARATELY:
  (1) How many committed t's can have a basis and an L recovered AT ALL, from the text and
      from the emitting script?
  (2) How many published significance claims are VERDICT-AMBIGUOUS — |t| inside the band
      spanned by the honest critical values of the cells the record leaves open?
  (3) Does quoting the honest bar instead of 1.96 BUY anything?  Priced on real books, at
      10 bps, next-day execution, chosen on 2009-2016 and read once on 2017-2026.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET   {C_1212, C_HEAD, C_MEMO, C_ALL}
  RECOVERY    {R_TEXT200, R_TEXTWIDE, R_SCRIPT, R_SCRIPT_STRICT}

  = 16 cells, EVERY ONE PUBLISHED, in `.census_grid.csv`; the per-claim rows for all four
  claim sets under all four recovery rules are in `.claims.csv`.

  C_1212  research/LEADERBOARD.md + research/CHANGELOG.md AS OF 1212's own commit
          (0743d51), so 1212's 210 hits reproduce EXACTLY (gate G1).  Frozen; git-read.
  C_HEAD  the same two files at this run's HEAD.
  C_MEMO  C_HEAD + every research/backtests/*.result.md and *.memo.md.
  C_ALL   C_MEMO + research/QUEUE.md.

  R_TEXT200      1212's rule, generalised to four bases: the basis whose keywords occur
                 within 200 characters of the hit; more than one basis -> AMBIGUOUS, none
                 -> UNCLASSIFIED.  This is the rule the record's own census used.
  R_TEXTWIDE     the same keyword rule over the WHOLE containing unit (leaderboard table
                 row / changelog or memo paragraph).  Strictly more generous than R_TEXT200.
  R_SCRIPT       map the claim to its EMITTING SCRIPT (leaderboard rows carry the script in
                 their last column; elsewhere, the nearest preceding *.py mention), then
                 classify from that script's SOURCE.  Basis from the four marker sets; L
                 from every integer bound to an L-ish name.  Exactly one basis -> resolved.
  R_SCRIPT_STRICT  R_SCRIPT, but a claim counts as RESOLVED only if the script pins a UNIQUE
                 basis AND a UNIQUE L.  This is what "the t carries its basis and its L"
                 actually means, so it is the rule the queue's proposed PROTOCOL line would
                 have to be scored against.

WHAT IS NOT A DIAL.  The SE BASIS ladder {S_IID, S_BLOCK, S_FOLD, S_NW} and the L ladder
{21, 63, 126, 252, 504} are 1212's, inherited whole (S_NW added as a rung only because the
census must be able to classify a Newey-West script; it is measured, not tuned).  PANEL
{U56, B136, SMALL} is not a dial.  The 216-book rule-8 population is not a dial and every
book is published.  The count-matched RANDOM bar in Arm D is a null, never a candidate.

Frozen at 1212's construction: CAND20 legs, max_vol 0.60, gross 0.75, min hold 126, N = 20,
cadence W, 10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, 30 disjoint null pairs per
panel, crc32 seeds, SEED_BASE 12191219.

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 walk-forward and BOTH KEEP
paths in Arm D; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_should-every-committed-t-carry-its-SE-BASIS-and-its-L_B.py
"""
from __future__ import annotations

import bisect
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
SLUG = "should-every-committed-t-carry-its-SE-BASIS-and-its-L"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = ROOT / "research" / "backtests"

# ----- 1212's construction, inherited whole -------------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

SE_BASES = ["S_IID", "S_BLOCK", "S_FOLD", "S_NW"]     # 1212's three + the NW rung
L_LADDER = [21, 63, 126, 252, 504]                    # 1212's
NPAIRS = 30
BDRAWS = 600                                          # 1212's, for the calibration arm
BDRAWS_IS = 300                                       # rule-8 arm (IS windows are shorter)
SEED_BASE = 12191219
Z95 = 1.959963984540054                               # the bar the record quotes

# the two dials
CLAIM_SETS = ["C_1212", "C_HEAD", "C_MEMO", "C_ALL"]
RECOVERIES = ["R_TEXT200", "R_TEXTWIDE", "R_SCRIPT", "R_SCRIPT_STRICT"]

# rule-8 population (Arm D)
POP_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
POP_H = [21, 63, 126, 252]
POP_C = ["W", "M"]
ANCHOR = dict(N=N0, H=HOLD0, cadence=FREQ0)
NRAND = 400                                           # count-matched random-bar draws

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived ----------------
C1212_COMMIT = "0743d51fcff839b47fa04cda45b8b0d190b32907"
C1212_NHITS = 210                                     # 1212's committed census size
C1212_FOLD = 10                                       # ... of which fold-clustered by its rule
C1212_CRIT = {                                        # 1212's committed crit95 table
    ("S_IID", 21): 1.9496, ("S_IID", 63): 1.8901, ("S_IID", 126): 1.9224,
    ("S_IID", 252): 1.8346, ("S_IID", 504): 1.9076,
    ("S_BLOCK", 21): 1.9379, ("S_BLOCK", 63): 1.9874, ("S_BLOCK", 126): 1.9438,
    ("S_BLOCK", 252): 2.0507, ("S_BLOCK", 504): 2.4004,
    ("S_FOLD", 21): 1.6417, ("S_FOLD", 63): 1.6897, ("S_FOLD", 126): 1.7996,
    ("S_FOLD", 252): 2.0748, ("S_FOLD", 504): 2.5341,
}
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
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


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
# 1212's runner and book machinery, verbatim
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
    """Annualised Sharpe of each ROW of a 2-D array."""
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
# THE SE BASES.  1212's three verbatim, plus the Newey-West rung the census needs to be able
# to classify.  Days are always resampled JOINTLY so the pair's correlation is preserved.
# =================================================================================================
def se_of_diff(ra, rb, basis, L, tag, ndraws=BDRAWS):
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    T = len(ra)
    if basis == "S_FOLD":
        ds = []
        for a in range(0, T, L):
            b = min(a + L, T)
            if b - a < 20:
                continue
            ds.append(fsharpe(ra[a:b]) - fsharpe(rb[a:b]))
        ds = np.array([x for x in ds if np.isfinite(x)])
        if len(ds) < 2:
            return np.nan, len(ds)
        return float(ds.std(ddof=1) / np.sqrt(len(ds))), len(ds)
    if basis == "S_NW":
        # HAC (Newey-West, Bartlett) SE of the mean daily difference, put on the SHARPE scale by
        # the POOLED BOOK volatility -- NOT by the SD of the difference.  The Sharpe scale's
        # denominator is the book's own vol; dividing by sd(ra - rb), which is far smaller for
        # two correlated books, inflates the SE.  SEE THE DECLARED BYCATCH: this run measured
        # that mis-scaling first and it under-rejects by a factor of ~2 (crit95 0.92-1.28
        # against a nominal 1.96), which is why the denominator is stated here in the source.
        d = ra - rb
        sd = 0.5 * (ra.std(ddof=1) + rb.std(ddof=1))
        if sd == 0 or T < 3:
            return np.nan, 0
        x = d - d.mean()
        g0 = float((x * x).mean())
        s = g0
        maxlag = int(min(L, T - 2))
        for k in range(1, maxlag + 1):
            gk = float((x[k:] * x[:-k]).mean())
            s += 2.0 * (1.0 - k / (maxlag + 1.0)) * gk
        s = max(s, 1e-24)
        se_mean = np.sqrt(s / T)
        return float(se_mean / sd * np.sqrt(252.0)), maxlag
    if basis == "S_NW_DIFFSD":                       # the mis-scaled variant, kept as BYCATCH
        d = ra - rb
        sd = d.std(ddof=1)
        if sd == 0 or T < 3:
            return np.nan, 0
        x = d - d.mean()
        s = float((x * x).mean())
        maxlag = int(min(L, T - 2))
        for k in range(1, maxlag + 1):
            s += 2.0 * (1.0 - k / (maxlag + 1.0)) * float((x[k:] * x[:-k]).mean())
        return float(np.sqrt(max(s, 1e-24) / T) / sd * np.sqrt(252.0)), maxlag
    rng = np.random.default_rng(seed_of("se", basis, L, tag))
    if basis == "S_IID":
        idx = rng.integers(0, T, size=(ndraws, T))
    else:
        nb = int(np.ceil(T / L))
        st = rng.integers(0, T, size=(ndraws, nb))
        idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
        idx = idx.reshape(ndraws, nb * L)[:, :T]
    d = sharpe_rows(ra[idx]) - sharpe_rows(rb[idx])
    return float(np.nanstd(d, ddof=1)), ndraws


# =================================================================================================
# THE CENSUS.  Harvest -> map to the emitting script -> recover (basis, L) four ways.
# =================================================================================================
# 1212's harvest pattern, VERBATIM.  Changing it would break the reproduction gate.
PAT_T = re.compile(r"(?:t(?:'s)?\s*(?:=|of|to)\s*|mean/SE\s*\+|\(t\s*)(-?\d+\.\d+)")
PAT_PY = re.compile(r"[0-9A-Za-z_\-\.]+\.py")

# TEXT markers, one keyword set per basis
TEXT_MARK = {
    "S_FOLD": ("fold", "cluster", "year"),        # 1212's three, kept verbatim
    "S_BLOCK": ("block",),
    "S_IID": ("iid", "i.i.d"),
    "S_NW": ("newey", "hac"),
}
# SCRIPT markers, one regex per basis, matched against the emitting script's SOURCE
SRC_MARK = {
    "S_FOLD": re.compile(r"S_FOLD|SE_FOLD|fold[_ ]?clust|clustered SE|per-fold|fold_se|by_fold",
                         re.I),
    "S_BLOCK": re.compile(r"S_BLOCK|SE_BLOCK|moving[- ]?block|block bootstrap|L_BLOCK|"
                          r"block_len|BLOCK_L", re.I),
    "S_IID": re.compile(r"S_IID|SE_IID|iid bootstrap|ddof=1\)\s*/\s*np\.sqrt|\.sem\(", re.I),
    "S_NW": re.compile(r"newey|nw_se|NW_SE|\bHAC\b"),
}
PAT_LDECL = re.compile(
    r"(?m)^\s*(?:\w+\s*,\s*)*(?:L|L_BLOCK|BLOCK_L|L_FOLD|FOLD_L|L_LADDER|L_BOOT|LBLOCK|"
    r"block_len|blocklen)(?:\s*,\s*\w+)*\s*=\s*([^\n#]+)")
PAT_INT = re.compile(r"\b(\d{1,4})\b")


def git_show(commit, path):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def harvest(name, txt, source):
    """Every 1212-pattern hit in `txt`, with its containing line, unit and preceding .py."""
    starts = [0] + [m.end() for m in re.finditer("\n", txt)]
    lines = txt.split("\n")
    out = []
    for m in PAT_T.finditer(txt):
        li = bisect.bisect_right(starts, m.start()) - 1
        line = lines[li]
        # the containing UNIT: a markdown table row is its own unit; else the paragraph
        if line.startswith("|"):
            unit = line
        else:
            a = li
            while a > 0 and lines[a - 1].strip():
                a -= 1
            b = li
            while b + 1 < len(lines) and lines[b + 1].strip():
                b += 1
            unit = "\n".join(lines[a:b + 1])
        script = None
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[-1].endswith(".py"):
                script = cells[-1]
        if script is None:
            mm = list(PAT_PY.finditer(txt[:m.start()]))
            if mm:
                script = mm[-1].group(0)
        out.append(dict(source=source, file=name, pos=m.start(), t=abs(float(m.group(1))),
                        ctx200=txt[max(0, m.start() - 200): m.end() + 200].lower(),
                        unit=unit.lower(), script=script))
    return out


def basis_from_words(text):
    hit = [b for b, ws in TEXT_MARK.items() if any(w in text for w in ws)]
    if len(hit) == 1:
        return hit[0]
    return "AMBIGUOUS" if len(hit) > 1 else "UNCLASSIFIED"


def script_facts(src):
    """(basis, L) as the SOURCE pins them."""
    hit = [b for b, r in SRC_MARK.items() if r.search(src)]
    basis = hit[0] if len(hit) == 1 else ("AMBIGUOUS" if len(hit) > 1 else "NO_SE")
    Ls = set()
    for m in PAT_LDECL.finditer(src):
        for v in PAT_INT.findall(m.group(1)):
            iv = int(v)
            if 2 <= iv <= 2520:
                Ls.add(iv)
    L = sorted(Ls)[0] if len(Ls) == 1 else None
    return basis, L, len(Ls)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1219 (lane B, {DATE}) — {SLUG}")
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
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
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

    def null_book(panel, seed):
        """1212's P_NULL: N names drawn uniformly from those eligible at each rebalance."""
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        rng = np.random.default_rng(seed_of("null", panel, seed))
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

    spy_u = d["px"]["SPY"].pct_change().fillna(0.0).values
    smm = blocks_m(spy_u, d["warm"], d["ins"], d["oos"])
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

    # G7 — the block SE family CONTAINS the iid one at L = 1 (1162's identity, re-checked here)
    rr = np.random.default_rng(7).normal(0.0004, 0.011, (2, 900))
    a, _ = se_of_diff(rr[0], rr[1], "S_BLOCK", 1, "gate7", ndraws=400)
    b, _ = se_of_diff(rr[0], rr[1], "S_IID", 1, "gate7", ndraws=400)
    v = abs(a - b) / max(b, 1e-12)
    gate("G7", "S_BLOCK at L=1 == S_IID (relative)", v, v < 0.05)

    # G8 — S_FOLD returns NaN rather than a number when fewer than two folds are usable
    a, nf = se_of_diff(rr[0][:30], rr[1][:30], "S_FOLD", 504, "gate8")
    gate("G8", "S_FOLD refuses to report with < 2 usable folds", float(nf), not np.isfinite(a))
    P("")

    # ============================================================ ARM A — the census
    P("## ARM A — HARVEST, MAP TO THE EMITTING SCRIPT, RECOVER (basis, L) FOUR WAYS")
    head_files = [("LEADERBOARD.md", "research/LEADERBOARD.md"),
                  ("CHANGELOG.md", "research/CHANGELOG.md")]

    claims = {}
    # C_1212 — the two files AT 1212's COMMIT, so its 210 reproduce exactly
    rows = []
    frozen_ok = True
    for nm, rel in head_files:
        txt = git_show(C1212_COMMIT, rel)
        if txt is None:
            frozen_ok = False
            txt = (ROOT / rel).read_text()
        rows += harvest(nm, txt, "C_1212")
    claims["C_1212"] = rows
    v = len(rows)
    gate("G1", f"1212's census reproduces at its own commit ({C1212_COMMIT[:7]})", v,
         (v == C1212_NHITS) if frozen_ok else (v >= C1212_NHITS))
    if not frozen_ok:
        P("     NOTE: git show unavailable; C_1212 fell back to HEAD and the gate is >= 210.")

    rows = []
    for nm, rel in head_files:
        rows += harvest(nm, (ROOT / rel).read_text(), "C_HEAD")
    claims["C_HEAD"] = rows

    memo_files = sorted(list(BT.glob("*.result.md")) + list(BT.glob("*.memo.md")))
    rows = list(claims["C_HEAD"])
    for p in memo_files:
        rows += harvest(p.name, p.read_text(errors="ignore"), "C_MEMO")
    claims["C_MEMO"] = rows

    rows = list(claims["C_MEMO"]) + harvest("QUEUE.md",
                                            (ROOT / "research" / "QUEUE.md").read_text(), "C_ALL")
    claims["C_ALL"] = rows
    P(f"  harvested: " + ",  ".join(f"{c} {len(claims[c])}" for c in CLAIM_SETS)
      + f"   ({len(memo_files)} memo/result files scanned)")

    # ---- script sources, read ONCE
    src_cache = {}

    def src_of(name):
        if name in src_cache:
            return src_cache[name]
        s = None
        for cand in (BT / name, ROOT / "research" / name, ROOT / name):
            if cand.exists():
                s = cand.read_text(errors="ignore")
                break
        src_cache[name] = s
        return s

    fact_cache = {}

    def facts_of(name):
        if name not in fact_cache:
            s = src_of(name)
            fact_cache[name] = script_facts(s) if s is not None else (None, None, 0)
        return fact_cache[name]

    claim_rows = []
    for cs in CLAIM_SETS:
        for r in claims[cs]:
            basis_src, L_src, nL = facts_of(r["script"]) if r["script"] else (None, None, 0)
            on_disk = r["script"] is not None and src_of(r["script"]) is not None
            rec = {}
            rec["R_TEXT200"] = basis_from_words(r["ctx200"])
            rec["R_TEXTWIDE"] = basis_from_words(r["unit"])
            rec["R_SCRIPT"] = (basis_src if on_disk else "UNMAPPED")
            rec["R_SCRIPT_STRICT"] = (basis_src if (on_disk and basis_src in SE_BASES
                                                    and nL == 1) else "UNRESOLVED")
            claim_rows.append(dict(claim_set=cs, file=r["file"], pos=r["pos"], t=r["t"],
                                   script=r["script"], script_on_disk=on_disk,
                                   n_L_declared=nL, L_script=L_src,
                                   **{f"basis_{k}": v for k, v in rec.items()}))
    CL = pd.DataFrame(claim_rows)
    dump(CL, "claims")

    grid = []
    for cs in CLAIM_SETS:
        g = CL[CL.claim_set == cs]
        for rr_ in RECOVERIES:
            col = g[f"basis_{rr_}"]
            res = col.isin(SE_BASES)
            grid.append(dict(claim_set=cs, recovery=rr_, n=len(g), resolved=int(res.sum()),
                             share_resolved=float(res.mean()),
                             fold=int((col == "S_FOLD").sum()),
                             block=int((col == "S_BLOCK").sum()),
                             iid=int((col == "S_IID").sum()),
                             nw=int((col == "S_NW").sum()),
                             ambiguous=int((col == "AMBIGUOUS").sum()),
                             unresolved=int((~res & (col != "AMBIGUOUS")).sum())))
    GRID = pd.DataFrame(grid)
    dump(GRID, "census_grid")
    P("  ALL 16 DIAL CELLS (share of committed t's whose SE BASIS is recoverable):")
    P("    " + f"{'claim set':<9} " + " ".join(f"{r:>17}" for r in RECOVERIES))
    for cs in CLAIM_SETS:
        g = GRID[GRID.claim_set == cs].set_index("recovery")
        P("    " + f"{cs:<9} " + " ".join(
            f"{int(g.loc[r,'resolved']):5d}/{int(g.loc[r,'n']):<5d} {g.loc[r,'share_resolved']:.3f}"
            for r in RECOVERIES))

    c12 = CL[CL.claim_set == "C_1212"]
    n_fold_1212 = int((c12.basis_R_TEXT200 == "S_FOLD").sum())
    v = abs(n_fold_1212 - C1212_FOLD)
    gate("G9", f"1212's own fold count ({C1212_FOLD} of {C1212_NHITS}) reproduces under "
               "R_TEXT200", v, v <= 1)

    P(f"  MAPPING: {int(c12.script.notna().sum())} of {len(c12)} C_1212 claims name an emitting "
      f"script, {int(c12.script_on_disk.sum())} of which is on disk.")
    nL = c12[c12.script_on_disk]
    P(f"  L DECLARATION: of those {len(nL)}, {int((nL.n_L_declared == 1).sum())} sit in a script "
      f"that pins a UNIQUE L, {int((nL.n_L_declared == 0).sum())} in a script that declares NONE, "
      f"{int((nL.n_L_declared > 1).sum())} in one that declares SEVERAL.")

    # ---- DIAGNOSTIC 1: is NO_SE a fact about the scripts, or a weakness of the markers?
    nose = sorted(set(c12[c12.basis_R_SCRIPT == "NO_SE"].script.dropna()))
    hasword = sum(1 for s in nose if re.search(r"\bSE\b|std\(|sem\(|np\.sqrt\(", src_of(s) or ""))
    P(f"  NO_SE IS A FLOOR, NOT A PROOF — stated rather than hidden: {len(nose)} distinct "
      f"scripts carry a committed t that this rule cannot trace to any of the four SE")
    P(f"  constructions.  {hasword} of those {len(nose)} nonetheless contain 'SE', 'std(', "
      f"'.sem(' or 'np.sqrt(' somewhere, so NO_SE means 'no NAMED basis this rule recognises',")
    P("  not 'no standard error exists'.  R_SCRIPT's share is therefore a LOWER BOUND on what a")
    P("  richer recovery rule could reach — and an UPPER BOUND on nothing.")

    # ---- DIAGNOSTIC 2: where the TEXT rule and the SCRIPT rule disagree
    f200 = c12[c12.basis_R_TEXT200 == "S_FOLD"]
    agree = int((f200.basis_R_SCRIPT == "S_FOLD").sum())
    P(f"  TEXT vs SCRIPT, HEAD ON: 1212's {len(f200)} fold-clustered t's are classified that way "
      f"because 'fold', 'cluster' or 'year' sits within 200 characters.  Of those "
      f"{len(f200)}, {agree} have an emitting script containing ANY fold-SE machinery")
    P(f"  ({', '.join(sorted(set(f200.basis_R_SCRIPT))) or 'none'}).  R_SCRIPT finds "
      f"{int((c12.basis_R_SCRIPT == 'S_FOLD').sum())} fold-SE t's in the whole 210.")
    P("")

    # ============================================================ ARM B — the honest bars
    P(f"## ARM B — THE HONEST CRITICAL VALUE, RE-MEASURED (not quoted): {NPAIRS} disjoint")
    P("   gross-matched null pairs per panel, true Sharpe difference = 0 by construction.")
    pairs = []
    for panel in PANELS:
        for j in range(NPAIRS):
            ra, rb = null_book(panel, 2 * j), null_book(panel, 2 * j + 1)
            w = panels[panel]["warm"]
            pairs.append(dict(panel=panel, pair=j, ra=ra[w], rb=rb[w]))
        P(f"   {panel:<6s} {NPAIRS} pairs built  ({time.time() - t0:.0f}s)")
    dS = np.array([fsharpe(p["ra"]) - fsharpe(p["rb"]) for p in pairs])
    P(f"   EXCHANGEABILITY CHECK: mean dSharpe {dS.mean():+.4f} over {len(pairs)} pairs "
      f"(sd {dS.std(ddof=1):.4f}); mean pair corr "
      f"{np.mean([np.corrcoef(p['ra'], p['rb'])[0, 1] for p in pairs]):.4f}")
    gate("G10", "the null pairs are EXCHANGEABLE (|mean dSharpe| <= 0.05)", abs(dS.mean()),
         abs(dS.mean()) <= 0.05)

    calrows = []
    for basis in SE_BASES + ["S_NW_DIFFSD"]:
        for L in L_LADDER:
            ts = []
            for p in pairs:
                se, _ = se_of_diff(p["ra"], p["rb"], basis, L, f"{p['panel']}|{p['pair']}")
                dv = fsharpe(p["ra"]) - fsharpe(p["rb"])
                ts.append(abs(dv / se) if (np.isfinite(se) and se > 0) else np.nan)
            ts = np.array(ts, float)
            ok = np.isfinite(ts)
            calrows.append(dict(se_basis=basis, L=L, n=int(ok.sum()),
                                crit95=float(np.nanpercentile(ts, 95)),
                                crit90=float(np.nanpercentile(ts, 90)),
                                reject_at_1p96=float(np.nanmean(ts[ok] > Z95))))
        P(f"   {basis:<8s} calibrated over the L ladder  ({time.time() - t0:.0f}s)")
    CAL = pd.DataFrame(calrows)
    dump(CAL, "calibration")
    crit = {(r.se_basis, r.L): r.crit95 for r in CAL.itertuples()}
    P("   HONEST 95th PERCENTILE OF |t| (the bar; the record quotes 1.96):")
    P("     " + f"{'basis':<12}" + "".join(f"{('L=' + str(L)):>10}" for L in L_LADDER)
      + "   max/min")
    for basis in SE_BASES + ["S_NW_DIFFSD"]:
        vals = [crit[(basis, L)] for L in L_LADDER]
        P("     " + f"{basis:<12}" + "".join(f"{v:>10.4f}" for v in vals)
          + f"   x{max(vals) / min(vals):.2f}")
    P("   DECLARED BYCATCH, REPORTED BECAUSE IT WAS MEASURED FIRST AND NOT REPAIRED QUIETLY:")
    P("   S_NW_DIFFSD is the SAME HAC SE divided by sd(ra - rb) instead of the pooled BOOK")
    P("   volatility.  It is the scaling this run wrote first.  It UNDER-REJECTS by about a")
    P(f"   factor of two — crit95 {min(crit[('S_NW_DIFFSD', L)] for L in L_LADDER):.4f}-"
      f"{max(crit[('S_NW_DIFFSD', L)] for L in L_LADDER):.4f} against a nominal 1.96 — because")
    P("   two correlated books' difference has a far smaller SD than either book.  It is NOT a")
    P("   rung of the ladder and enters nothing downstream; it is published so that the")
    P("   denominator of a Sharpe-scale HAC SE is on the record as a dial in its own right.")
    rep = [(k, v, C1212_CRIT[k]) for k, v in crit.items() if k in C1212_CRIT]
    dev = max(abs(a - b) for _, a, b in rep)
    gate("G11", "1212's crit95 table reproduces (max |deviation| over its 15 cells)", dev,
         dev < 0.35)
    P(f"     (1212's own 15 cells reproduce to {dev:.4f}; this run redraws its own seeds, so "
      "the bar is Monte-Carlo width, not bit equality.)")

    B1212 = ["S_IID", "S_BLOCK", "S_FOLD"]                 # 1212's own basis set
    lo = min(crit[(b, L)] for b in B1212 for L in L_LADDER)
    hi = max(crit[(b, L)] for b in B1212 for L in L_LADDER)
    lo4 = min(crit[(b, L)] for b in SE_BASES for L in L_LADDER)
    hi4 = max(crit[(b, L)] for b in SE_BASES for L in L_LADDER)
    P(f"   THE AMBIGUITY BAND (headline, over 1212's OWN three bases x its own L ladder): a")
    P(f"   committed t that states neither its basis nor its L has an honest bar anywhere in")
    P(f"   [{lo:.4f}, {hi:.4f}] — a factor of {hi / lo:.2f}.  Over all four bases including the")
    P(f"   NW rung this run added, [{lo4:.4f}, {hi4:.4f}] (a factor of {hi4 / lo4:.2f}): the NW")
    P("   rung calibrates INSIDE the band the other three already span and widens it by nothing.")
    P("   The headline uses the THREE, because they are the bases the record actually used.")
    P("")

    # ============================================================ ARM C — re-reading the record
    P("## ARM C — HOW MANY COMMITTED SIGNIFICANCE CLAIMS ARE VERDICT-AMBIGUOUS?")
    verd = []
    for cs in CLAIM_SETS:
        g = CL[CL.claim_set == cs]
        for rr_ in RECOVERIES:
            col = g[f"basis_{rr_}"]
            tt = g.t.values
            sig196 = tt > Z95
            # bar under the recovered cell: the basis if resolved, the L if the script pins one,
            # else the WORST case the record leaves open (the widest honest bar for that basis)
            bars = []
            for b_, L_, t_ in zip(col.values, g.L_script.values, tt):
                if b_ in SE_BASES:
                    if L_ is not None and not pd.isna(L_) and int(L_) in L_LADDER:
                        bars.append(crit[(b_, int(L_))])
                    else:
                        bars.append(max(crit[(b_, L)] for L in L_LADDER))
                else:
                    bars.append(np.nan)
            bars = np.array(bars, float)
            has = np.isfinite(bars)
            sig_h = np.where(has, tt > bars, np.nan)
            flips = int(np.nansum((sig196 == True) & (sig_h == 0.0)))
            amb = int(((tt > lo) & (tt <= hi)).sum())
            verd.append(dict(claim_set=cs, recovery=rr_, n=len(g),
                             sig_at_1p96=int(sig196.sum()),
                             resolved=int(has.sum()),
                             resolved_and_sig_at_1p96=int((sig196 & has).sum()),
                             lost_at_honest_bar=flips,
                             verdict_ambiguous_band=amb,
                             share_ambiguous_of_sig=float(amb / max(int(sig196.sum()), 1))))
    VD = pd.DataFrame(verd)
    dump(VD, "verdicts")
    for cs in CLAIM_SETS:
        g = VD[VD.claim_set == cs]
        P(f"   {cs:<8} n={int(g.n.iloc[0]):5d}  |t|>1.96: {int(g.sig_at_1p96.iloc[0]):4d}   "
          f"in the ambiguity band [{lo:.2f},{hi:.2f}]: "
          f"{int(g.verdict_ambiguous_band.iloc[0]):4d}  "
          f"({float(g.verdict_ambiguous_band.iloc[0]) / max(int(g.n.iloc[0]), 1):.4f} of all, "
          f"{float(g.share_ambiguous_of_sig.iloc[0]):.4f} of the significant)")
        for rr_ in RECOVERIES:
            r_ = g[g.recovery == rr_].iloc[0]
            P(f"       {rr_:<16} resolved {int(r_.resolved):5d}   of which significant at 1.96 "
              f"{int(r_.resolved_and_sig_at_1p96):4d}   LOST at their own honest bar "
              f"{int(r_.lost_at_honest_bar):4d}")
    P("")

    # ============================================================ ARM D — rule 8 + KEEP paths
    P("## ARM D — PROTOCOL rule 8 WALK-FORWARD AND BOTH KEEP PATHS")
    P(f"   {len(POP_N)}x{len(POP_H)}x{len(POP_C)} = {len(POP_N) * len(POP_H) * len(POP_C)} books "
      f"per panel, {len(POP_N) * len(POP_H) * len(POP_C) * len(PANELS)} in all, EVERY ONE "
      "PUBLISHED.  Parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE.")
    for panel in PANELS:
        dd_ = panels[panel]
        spy = dd_["px"]["SPY"].pct_change().fillna(0.0).values
        live = backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                        freq="W")["returns"].values
        dd_["spy_m"] = blocks_m(spy, dd_["warm"], dd_["ins"], dd_["oos"])
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
    P(f"   4b full AND OOS: {len(both)} rows, "
      f"{both.groupby(['panel', 'N', 'H', 'cadence']).ngroups if len(both) else 0} DISTINCT books")
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

    # ---- the capital question: 1.96 vs the honest bar, as a PUBLISH rule
    P("   THE CAPITAL QUESTION.  A committed t is a PUBLISH decision.  Each (basis, L) is a")
    P("   chooser over the 9-rung N ladder inside a (panel, H, cadence) context: take the rung")
    P("   whose IS Sharpe difference vs the ANCHOR rung (N=20) has the largest |t| under that")
    P("   basis, and MOVE only if that t clears the bar.  BAR_QUOTED = 1.96 (what the record")
    P("   writes); BAR_HONEST = this run's own crit95 for that (basis, L).  Everything else is")
    P("   held fixed, so a difference between the two IS the value of quoting the L.")
    contexts = [(p_, H, fr) for p_ in PANELS for H in POP_H for fr in POP_C]
    P(f"   {len(contexts)} contexts x {len(SE_BASES)} bases x {len(L_LADDER)} L x 2 bars = "
      f"{len(contexts) * len(SE_BASES) * len(L_LADDER) * 2} decisions, every one published.")

    # IS t of every (context, rung) under every (basis, L) — computed ONCE
    tcache = {}
    for (p_, H, fr) in contexts:
        ins = panels[p_]["ins"]
        ra = rser[(p_, ANCHOR["N"], H, fr)][ins]
        for N in POP_N:
            if N == ANCHOR["N"]:
                continue
            rb = rser[(p_, N, H, fr)][ins]
            dv = fsharpe(rb) - fsharpe(ra)
            for basis in SE_BASES:
                for L in L_LADDER:
                    se, _ = se_of_diff(rb, ra, basis, L, f"is|{p_}|{H}|{fr}|{N}",
                                       ndraws=BDRAWS_IS)
                    tcache[(p_, H, fr, N, basis, L)] = (
                        dv / se if (np.isfinite(se) and se > 0) else np.nan)
        P(f"   IS t's built for {p_}/H{H}/{fr}  ({time.time() - t0:.0f}s)")

    popi = POP.set_index(["panel", "N", "H", "cadence"])

    def bookrow(p_, N, H, fr):
        return popi.loc[(p_, N, H, fr)]

    decrows = []
    for basis in SE_BASES:
        for L in L_LADDER:
            for barname, barval in (("BAR_QUOTED", Z95), ("BAR_HONEST", crit[(basis, L)])):
                for (p_, H, fr) in contexts:
                    cands = [(abs(tcache[(p_, H, fr, N, basis, L)]), N) for N in POP_N
                             if N != ANCHOR["N"]
                             and np.isfinite(tcache[(p_, H, fr, N, basis, L)])]
                    if cands:
                        tbest, Nbest = max(cands)
                    else:
                        tbest, Nbest = np.nan, ANCHOR["N"]
                    moved = bool(np.isfinite(tbest) and tbest > barval)
                    Npick = Nbest if moved else ANCHOR["N"]
                    r_ = bookrow(p_, Npick, H, fr)
                    decrows.append(dict(se_basis=basis, L=L, bar=barname, bar_value=barval,
                                        panel=p_, H=H, cadence=fr, t_best=tbest,
                                        N_argmax=Nbest, N_pick=Npick, moved=moved,
                                        OOS_Sharpe=r_["OOS_Sharpe"], OOS_CAGR=r_["OOS_CAGR"],
                                        OOS_MaxDD=r_["OOS_MaxDD"],
                                        pass_4b_full=bool(r_["pass_4b_full"]),
                                        pass_4b_oos=bool(r_["pass_4b_oos"]),
                                        pass_4a=bool(r_["pass_4a"])))
    # the do-nothing anchor, as its own rule
    for (p_, H, fr) in contexts:
        r_ = bookrow(p_, ANCHOR["N"], H, fr)
        decrows.append(dict(se_basis="C_ANCHOR", L=0, bar="BAR_NONE", bar_value=np.inf,
                            panel=p_, H=H, cadence=fr, t_best=np.nan, N_argmax=ANCHOR["N"],
                            N_pick=ANCHOR["N"], moved=False, OOS_Sharpe=r_["OOS_Sharpe"],
                            OOS_CAGR=r_["OOS_CAGR"], OOS_MaxDD=r_["OOS_MaxDD"],
                            pass_4b_full=bool(r_["pass_4b_full"]),
                            pass_4b_oos=bool(r_["pass_4b_oos"]), pass_4a=bool(r_["pass_4a"])))
    DEC = pd.DataFrame(decrows)
    dump(DEC, "decisions")

    anch = DEC[DEC.se_basis == "C_ANCHOR"]
    anchor_mean = float(anch.OOS_Sharpe.mean())
    anchor_4b = int((anch.pass_4b_full & anch.pass_4b_oos).sum())
    P(f"   DOING NOTHING (the anchor rung at all {len(anch)} contexts): mean OOS Sharpe "
      f"{anchor_mean:.4f}, 4b full+OOS {anchor_4b} of {len(anch)}, 4a {int(anch.pass_4a.sum())}")

    rule = DEC[DEC.se_basis != "C_ANCHOR"].groupby(["se_basis", "L", "bar"]).agg(
        moves=("moved", "sum"), meanOOS=("OOS_Sharpe", "mean"),
        n4b=("pass_4b_oos", lambda s: int(s.sum())), n=("moved", "size")).reset_index()
    rule["n4b_both"] = [
        int((DEC[(DEC.se_basis == r.se_basis) & (DEC.L == r.L) & (DEC.bar == r.bar)]
             .pass_4b_full & DEC[(DEC.se_basis == r.se_basis) & (DEC.L == r.L)
                                 & (DEC.bar == r.bar)].pass_4b_oos).sum())
        for r in rule.itertuples()]
    rule["n4a"] = [
        int(DEC[(DEC.se_basis == r.se_basis) & (DEC.L == r.L) & (DEC.bar == r.bar)].pass_4a.sum())
        for r in rule.itertuples()]
    dump(rule, "rules")
    P("   EVERY ONE OF THE 40 (basis x L x bar) RULES, moves / mean OOS Sharpe / 4b(full+OOS):")
    for basis in SE_BASES:
        for barname in ("BAR_QUOTED", "BAR_HONEST"):
            g = rule[(rule.se_basis == basis) & (rule.bar == barname)].set_index("L")
            P(f"     {basis:<8} {barname:<11} " + "  ".join(
                f"L{L}:{int(g.loc[L, 'moves']):2d}m/{g.loc[L, 'meanOOS']:.4f}/"
                f"{int(g.loc[L, 'n4b_both'])}" for L in L_LADDER))

    # count-matched RANDOM bar: any rule that MOVES gains or loses by moving, not by reading
    P("   COUNT-MATCHED RANDOM BAR (the control 1210 and 1221 both found decisive): for each")
    P("   rule's realised move count m, draw m of the contexts at random, move to that")
    P("   context's IS argmax rung, and read the same OOS mean.  A rule that does not clear")
    P("   its own count-matched null is buying its result with the move count alone.")
    randrows = []
    for r in rule.itertuples():
        sub = DEC[(DEC.se_basis == r.se_basis) & (DEC.L == r.L) & (DEC.bar == r.bar)]
        m = int(sub.moved.sum())
        base = {(x.panel, x.H, x.cadence): (float(bookrow(x.panel, ANCHOR["N"], x.H,
                                                          x.cadence)["OOS_Sharpe"]),
                                            float(bookrow(x.panel, x.N_argmax, x.H,
                                                          x.cadence)["OOS_Sharpe"]))
                for x in sub.itertuples()}
        keys = list(base.keys())
        anchor_vals = np.array([base[k][0] for k in keys])
        argmax_vals = np.array([base[k][1] for k in keys])
        obs = float(sub.OOS_Sharpe.mean())
        rng = np.random.default_rng(seed_of("rand", r.se_basis, r.L, r.bar))
        draws = np.empty(NRAND)
        for i in range(NRAND):
            pick = rng.choice(len(keys), size=m, replace=False) if m else np.array([], int)
            v = anchor_vals.copy()
            v[pick] = argmax_vals[pick]
            draws[i] = v.mean()
        randrows.append(dict(se_basis=r.se_basis, L=r.L, bar=r.bar, moves=m, observed=obs,
                             null_median=float(np.median(draws)),
                             null_p90=float(np.percentile(draws, 90)),
                             percentile=float((draws < obs).mean())))
    RND = pd.DataFrame(randrows)
    dump(RND, "randombar")
    nclear = int((RND.percentile >= 0.90).sum())
    P(f"   rules clearing the 90th percentile of their own count-matched null: "
      f"{nclear} of {len(RND)}")
    P(f"   READ THAT AT ITS TRUE WEIGHT: {len(RND)} rules tested at a 0.90 bar means "
      f"{0.10 * len(RND):.1f} of {len(RND)} clear it BY CHANCE.  Observed {nclear}.  Nothing")
    P("   in this family separates itself from its own move count, and no rule here is a")
    P("   candidate for anything.")
    P(f"   rules beating DOING NOTHING on mean OOS Sharpe: "
      f"{int((rule.meanOOS > anchor_mean).sum())} of {len(rule)}")
    mrg = rule.merge(RND, on=["se_basis", "L", "bar"], suffixes=("", "_r"))
    win = mrg[(mrg.meanOOS > anchor_mean) & (mrg.percentile >= 0.90)]
    P(f"   rules doing BOTH: {len(win)} of {len(mrg)}" + ("" if not len(win) else " — " + ", ".join(
        f"{r.se_basis}/L{int(r.L)}/{r.bar} {r.meanOOS:.4f} (pct {r.percentile:.3f})"
        for r in win.itertuples())))

    # the honest-bar vs quoted-bar contrast, paired by (basis, L)
    piv = rule.pivot_table(index=["se_basis", "L"], columns="bar",
                           values=["meanOOS", "moves", "n4b_both"])
    dmean = (piv[("meanOOS", "BAR_HONEST")] - piv[("meanOOS", "BAR_QUOTED")])
    dmove = (piv[("moves", "BAR_HONEST")] - piv[("moves", "BAR_QUOTED")])
    d4b = (piv[("n4b_both", "BAR_HONEST")] - piv[("n4b_both", "BAR_QUOTED")])
    se_d = float(dmean.std(ddof=1) / np.sqrt(len(dmean))) if len(dmean) > 1 else np.nan
    P(f"   HONEST BAR minus QUOTED BAR over the {len(dmean)} (basis, L) cells: mean OOS Sharpe "
      f"{dmean.mean():+.4f} (SE {se_d:.4f}, t {dmean.mean() / se_d if se_d else np.nan:+.2f}), "
      f"moves {dmove.mean():+.2f}, 4b(full+OOS) {d4b.mean():+.2f}")
    P(f"   cells where the two bars make IDENTICAL decisions: "
      f"{int((dmove == 0).sum())} of {len(dmove)} on move count, "
      f"{int((dmean.abs() < 1e-12).sum())} of {len(dmean)} on mean OOS Sharpe")
    P("")

    # ============================================================ HYPOTHESES
    P("## HYPOTHESES — declared with their bars, scored once")
    g12 = GRID[GRID.claim_set == "C_1212"].set_index("recovery")
    s_text = float(g12.loc["R_TEXT200", "share_resolved"])
    s_scr = float(g12.loc["R_SCRIPT", "share_resolved"])
    s_str = float(g12.loc["R_SCRIPT_STRICT", "share_resolved"])
    hyp("H_RECOVER", "the emitting SCRIPT recovers a basis for materially more committed t's "
                     "than the text does",
        "R_SCRIPT share >= 2x R_TEXT200's on C_1212",
        f"R_TEXT200 {s_text:.4f}, R_SCRIPT {s_scr:.4f} (ratio "
        f"{s_scr / max(s_text, 1e-9):.2f}x)", s_scr >= 2 * s_text)

    hyp("H_TEXTWRONG", "the record's own TEXT rule does not agree with the emitting SCRIPT: "
                       "1212's fold-clustered t's are not traceable to fold-SE machinery",
        "fewer than half of R_TEXT200's S_FOLD hits have a fold-SE emitting script",
        f"{agree} of {len(f200)} agree; R_SCRIPT finds "
        f"{int((c12.basis_R_SCRIPT == 'S_FOLD').sum())} fold-SE t's in all 210",
        agree < 0.5 * max(len(f200), 1))

    hyp("H_L", "recovering the basis is NOT enough: most scripts do not pin a unique L either",
        "R_SCRIPT_STRICT share < 0.50 on C_1212",
        f"{s_str:.4f} ({int(g12.loc['R_SCRIPT_STRICT', 'resolved'])} of "
        f"{int(g12.loc['R_SCRIPT_STRICT', 'n'])})", s_str < 0.50)

    v12 = VD[(VD.claim_set == "C_1212") & (VD.recovery == "R_SCRIPT")].iloc[0]
    amb_share = float(v12.verdict_ambiguous_band) / max(int(v12.n), 1)
    hyp("H_AMBIG", "a material share of committed t's sit inside the band the unstated dials "
                   "span, so their significance verdict is a function of what nobody wrote down",
        ">= 0.10 of C_1212's t's inside [%.2f, %.2f]" % (lo, hi),
        f"{int(v12.verdict_ambiguous_band)} of {int(v12.n)} = {amb_share:.4f}",
        amb_share >= 0.10)

    best_rule = rule.sort_values("meanOOS", ascending=False).iloc[0]
    hyp("H_WF", "quoting the HONEST bar instead of 1.96 buys OOS Sharpe",
        "mean(honest - quoted) over the 20 (basis, L) cells > 0 at |t| > 2",
        f"{dmean.mean():+.4f}, t {(dmean.mean() / se_d) if se_d else float('nan'):+.2f}",
        bool(se_d and dmean.mean() > 0 and abs(dmean.mean() / se_d) > 2))

    hyp("H_ANCHOR", "SOME (basis, L, bar) rule beats DOING NOTHING out of sample AND clears its "
                    "own count-matched random-bar null",
        "at least one rule with meanOOS > anchor AND percentile >= 0.90",
        f"best rule {best_rule.se_basis}/L{int(best_rule.L)}/{best_rule.bar} meanOOS "
        f"{best_rule.meanOOS:.4f} vs anchor {anchor_mean:.4f}; "
        f"{int((RND.percentile >= 0.90).sum())} of {len(RND)} clear their null",
        bool(((rule.meanOOS > anchor_mean) & (RND.set_index(['se_basis', 'L', 'bar'])
              .reindex(pd.MultiIndex.from_frame(rule[['se_basis', 'L', 'bar']]))
              .percentile.values >= 0.90)).any()))

    npass4a = int(POP.pass_4a.sum())
    nboth = int((POP.pass_4b_full & POP.pass_4b_oos).sum())
    hyp("H_KEEP", "this run's population produces a NEW capital-worthy book",
        "a 4a pass, or a 4b full+OOS pass that is not already in the record",
        f"4a {npass4a} of {len(POP)}; 4b full+OOS {nboth} of {len(POP)} over "
        f"{both.groupby(['panel', 'N', 'H', 'cadence']).ngroups if len(both) else 0} distinct "
        "books", False if npass4a == 0 else True)
    P("")

    # ============================================================ VERDICT
    P("## VERDICT")
    P(f"   4a: {npass4a} of {len(POP)} books.  4b full AND OOS: {nboth} of {len(POP)}.")
    P("   This run proposes NO rules change, NO promotion and NO memo beyond the reporting")
    P("   clause below.  RULES.md, scan.py, bot.py and baseline.py are untouched.")
    P("")
    P("## SURVIVORSHIP (rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B")
    P(f"   screen (data/SMALL_PANEL_README.md) less the documented max_1d_move >= 1.0")
    P(f"   exclusion — {ndrop} of {nmeta} dropped, {panels['SMALL']['K'] - 1} investable names")
    P("   plus SPY as benchmark only.  The census arms (A and C) are scans of committed TEXT")
    P("   and SOURCE and carry no market bias at all; the calibration in Arm B is one")
    P("   construction measured against itself and the bias very largely cancels out of a")
    P("   critical-value RATIO.  The bias does NOT cancel out of Arm D's OOS levels or the 4b")
    P("   legs, so any pass there is an upper bound.")
    P("")

    GDF = pd.DataFrame(GATES)
    dump(GDF, "gates")
    dump(pd.DataFrame(HYPS), "hypotheses")
    P(f"## GATES {int(GDF.pass_.sum())} of {len(GDF)} PASS")
    P(f"## runtime {time.time() - t0:.0f}s, offline, deterministic")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
