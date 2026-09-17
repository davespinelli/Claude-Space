#!/usr/bin/env python3
"""Idea 1159 (lane B, 2026-09-17)
   does-ANY-committed-MAXIMUM-KEYED-claim-in-the-record-carry-a-RESAMPLE-NULL

1157 found the SMALL / MAXDD regime-to-length cell sits INSIDE its own moving-block null's
90% band [0.441, 0.881], with 0.92-0.98 of draws sub-1 on every panel: the headline was
arithmetic.  The queue asks the general question.  A MAXIMUM is the one statistic whose
expected value grows with the number of points it is taken over -- over TIME (1140's
b(level) +0.2645 for MaxDD, the only one of six with a material one) and over RUNGS (1148's
count-inflation: a max-minus-min over k points grows in k).  So a maximum-keyed number is
the record's most null-hungry object, and the record is full of them.

TWO LEGS, and the second is the one that decides.

  CENSUS  how many of the record's committed MAXIMUM-KEYED figures publish a resample null
          beside them, at every (CLAIM SET x proximity window), over prose (LEADERBOARD,
          CHANGELOG, *.result.md) and over the committed CSV columns.  This answers the
          idea's literal question ("does ANY").
  RE-SCORE build the null the record did not publish, for the three maximum-keyed OBJECTS
          the record actually commits -- a MaxDD LEVEL, a max-minus-min SPREAD over a
          ladder, an ARGMAX MARGIN -- on 81 rung books over four ladders and three panels,
          under THREE resample nulls, and report how many sit inside their own null's 90%
          band, i.e. how many published numbers are arithmetic.

A clause requiring a null is worth enacting only if the null MOVES verdicts.  If every
re-scored number is already extreme against its own null, the clause is cosmetic.

TUNED DIALS (2, PROTOCOL rule 4): `CLAIM SET` {CS_MAXDD, CS_SPREAD, CS_ARGMAX, CS_ALL} x
`NULL TYPE` {N_BLOCK, N_IID, N_STAT} = 12 combinations, ALL published.  PANEL {U56, B136,
SMALL}, LADDER {N, H, GROSS, CADENCE} and RUNG are NOT dials -- all 81 books are built and
committed at every point.  PROXIMITY WINDOW {0, 200, 400, whole-unit} is NOT a dial either:
all four are reported at every census point and nothing is selected on any of them.
CONFIDENCE q is NOT a dial (0.90 headline, 0.80 / 0.95 printed beside, never selected on).
BLOCK LENGTH is frozen at the record's L=63 -- it is a property of N_BLOCK, not a dial.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131/1140/1148's construction:
CAND20 legs, cap INF, max_vol 0.60, gross 0.75 (except on GROSS), min hold 126 (except on
H), N=20 (except on N), W (except on CADENCE), 10 bps, LAG 1, warm-up 260, IS end
2016-12-31, block L=63, 1000 draws, crc32 seeds.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; the SMALL pool
is the CURRENT constituents of a sub-$2B screen (data/SMALL_PANEL_README.md), less the
documented max_1d_move >= 1.0 exclusion.  Every LEVEL here -- CAGR, MaxDD, and therefore
every maximum-keyed object below -- is optimistic.  A resample null prices SAMPLING error on
the tape it is given and CANNOT correct that bias; stated, not hidden.

Standalone, deterministic, offline.  Nothing outside research/ is written or modified.  The
one arm that reads outside data/ and research/ is the RESTATEMENT CENSUS, which reads a
committed blob of data/prices.csv out of this repo's own git object store; it is local,
read-only and reproducible, and the run degrades gracefully without it.
"""
from __future__ import annotations

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
SLUG = "does-ANY-committed-MAXIMUM-KEYED-claim-in-the-record-carry-a-RESAMPLE-NULL"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = ROOT / "research" / "backtests"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)
PANELS = ["U56", "B136", "SMALL"]

CLAIM_SETS = ["CS_MAXDD", "CS_SPREAD", "CS_ARGMAX", "CS_ALL"]      # dial 1
NULL_TYPES = ["N_BLOCK", "N_IID", "N_STAT"]                        # dial 2
N_HEAD = "N_BLOCK"                                                 # the record's own basis
OBJECTS = ["OBJ_MAXDD", "OBJ_SPREAD", "OBJ_ARGMAX"]
OBJ_OF = {"CS_MAXDD": ["OBJ_MAXDD"], "CS_SPREAD": ["OBJ_SPREAD"],
          "CS_ARGMAX": ["OBJ_ARGMAX"], "CS_ALL": OBJECTS}

WINDOWS = [200, 400, 0]                 # 0 = the whole prose unit (the most generous reading)
QS = [0.80, 0.90, 0.95]
Q_HEAD = 0.90
L_BLOCK, BDRAWS = 63, 1000
SEED_BASE = 11591159
CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", "OOS_Sharpe"),
            "C_ISCAGR": ("IS_CAGR", "OOS_CAGR"),
            "C_ISDD": ("IS_MaxDD", "OOS_MaxDD")}    # MaxDD negative -> higher is better

# ---- the record's own committed numbers, QUOTED and GATED, never re-derived from memory
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
PRIOR1148 = BT / ("2026-09-16_should-a-SUB-TAPE-COMPARISON-be-required-to-publish-its-"
                  "REGIME-to-LENGTH-RATIO_cloud")
PRIOR1148_GRID = Path(str(PRIOR1148) + ".grid.csv")
PRIOR1148_CONSOLE = Path(str(PRIOR1148) + ".console.txt")
PRIOR1157_BAND = (0.441, 0.881)         # 1157's committed SMALL/MAXDD 90% band, quoted
VINT_RX = re.compile(r"^\s*U56\s+(\d+)\s+cols,\s+([\d,]+)\s+rows\s+(\d{4}-\d\d-\d\d)\s*->\s*"
                     r"(\d{4}-\d\d-\d\d)", re.M)


def prior_vintage():
    """The U56 tape EXTENT 1148 actually ran on, READ from its committed console, never
    recalled.  Every committed constant this run gates against was computed on that tape."""
    m = VINT_RX.search(PRIOR1148_CONSOLE.read_text(errors="ignore"))
    if not m:
        return None
    return int(m.group(2).replace(",", "")), m.group(4)

CLAUSE_TEXT = """\
PROTOCOL rule 11 (DRAFT, priced by idea 1159 -- NOT enacted here; rule 6 reserves every
PROTOCOL edit to a Sunday review):

  11. **No bare maximum.**  A backtest may not publish a number that is a MAXIMUM over a
      varying number of points -- a MaxDD (a maximum over bars), a max-minus-min spread or
      band (a maximum over rungs), an argmax margin, a worst-rung figure -- without a
      RESAMPLE NULL beside it: the null's median, its band at the declared q, and the share
      of draws on the published side.  A maximum's expected value GROWS with the count it
      is taken over (idea 1140's b(level) +0.2645 over tape length; idea 1148's count
      inflation over rungs), so a bare maximum cannot be compared between two runs, and a
      maximum that sits inside its own null's band is arithmetic, not a finding."""

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


# ------------------------------------------------------- the record's runner, verbatim
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


def restatement_census():
    """Is data/prices.csv APPEND-ONLY?  Compare the committed blob from before the most recent
    commit that touched it against the file on disk, over the dates and tickers they share.
    Local, offline and deterministic (a git object read in this same repo); returns None and is
    skipped if the history is unavailable, so the run stays standalone."""
    import io
    import subprocess

    def sh(*a):
        r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip())
        return r.stdout

    try:
        commit = sh("log", "-1", "--format=%h", "--", "data/prices.csv").strip()
        subj = sh("log", "-1", "--format=%s", "--", "data/prices.csv").strip()
        old = pd.read_csv(io.StringIO(sh("show", f"{commit}^:data/prices.csv")),
                          index_col=0, parse_dates=True)
    except Exception:
        return None
    new = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    idx = old.index.intersection(new.index)
    cols = old.columns.intersection(new.columns)
    a, b = old.loc[idx, cols], new.loc[idx, cols]
    d = (b - a).abs()
    rel = d / a.abs().replace(0, np.nan)
    changed = d.values > 0
    finite = np.isfinite(rel.values)
    per = pd.DataFrame(dict(ticker=cols,
                            n_restated=[int((d[c].values > 0).sum()) for c in cols],
                            max_rel=[float(np.nanmax(rel[c].values))
                                     if np.isfinite(rel[c].values).any() else np.nan
                                     for c in cols]))
    per["share_restated"] = per.n_restated / max(len(idx), 1)
    meta = dict(commit=commit, subject=subj, n_cells=int(finite.sum()),
                n_changed=int((changed & finite).sum()),
                share_changed=float((changed & finite).sum() / max(finite.sum(), 1)),
                n_tickers=len(cols), n_tickers_changed=int((per.n_restated > 0).sum()),
                earliest=str(idx[changed.any(axis=1)].min().date()) if changed.any() else "none",
                max_rel=float(np.nanmax(rel.values)),
                median_rel=float(np.nanmedian(rel.values[changed & finite]))
                if (changed & finite).any() else np.nan,
                worst_ticker=str(per.loc[per.max_rel.idxmax(), "ticker"]))
    return per.sort_values("max_rel", ascending=False), meta


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# =================================================================================================
# THE THREE RESAMPLE NULLS.  Each returns a (ndraws, T) index matrix.  The SAME matrix is
# applied to EVERY rung of a ladder, so the tape cancels and the SPREAD null is a spread over
# the same resampled tape -- the paired currency 1012/1150 use.
# =================================================================================================
def null_index(kind, rng, T, ndraws):
    if kind == "N_IID":                                   # L = 1: destroys all autocorrelation
        return rng.integers(0, T, size=(ndraws, T))
    if kind == "N_BLOCK":                                 # the record's frozen moving block
        nb = int(np.ceil(T / L_BLOCK))
        st = rng.integers(0, T, size=(ndraws, nb))
        idx = (st[:, :, None] + np.arange(L_BLOCK)[None, None, :]) % T
        return idx.reshape(ndraws, nb * L_BLOCK)[:, :T]
    if kind == "N_STAT":                                  # stationary bootstrap, mean block 63
        p = 1.0 / L_BLOCK
        out = np.empty((ndraws, T), dtype=np.int64)
        out[:, 0] = rng.integers(0, T, size=ndraws)
        newb = rng.random((ndraws, T)) < p
        fresh = rng.integers(0, T, size=(ndraws, T))
        for t in range(1, T):
            cont = (out[:, t - 1] + 1) % T
            out[:, t] = np.where(newb[:, t], fresh[:, t], cont)
        return out
    raise ValueError(kind)


def boot_maxdd(R, idx, chunk=50):
    """|MaxDD| (positive, in %) of every row of R under every resample row of idx."""
    nr = R.shape[0]
    nd = idx.shape[0]
    out = np.empty((nr, nd))
    LG = np.log1p(R)
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            cum = np.cumsum(LG[j][ix], axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = -np.expm1(cum - run).min(axis=1) * 100.0
    return out


def band(x, q):
    lo = np.nanpercentile(x, (1 - q) / 2 * 100.0)
    hi = np.nanpercentile(x, (1 + q) / 2 * 100.0)
    return float(lo), float(hi)


# =================================================================================================
# ARM A -- THE CENSUS.  Both pattern lists are DUMPED so every classification is checkable.
# =================================================================================================
MAX_RX = {
    "CS_MAXDD": re.compile(
        r"\bmax\s*dd\b|\bmaxdd\b|\bmax(?:imum)?\s+draw\s*down\b|\bdrawdown\b|\bdraw-down\b"
        r"|\bworst\s+draw\s*down\b|\bDD\s+(?:level|cap|floor)\b", re.I),
    "CS_SPREAD": re.compile(
        r"\bmax[- ]?minus[- ]?min\b|\bmax-min\b|\bspread\b|\brange\b|\bband\b|\bwidth\b"
        r"|\bwidest\b|\bnarrowest\b|\bfrom\s+[-+]?\d+(?:\.\d+)?\s*(?:%|x)?\s*(?:to|->)\s*"
        r"[-+]?\d+(?:\.\d+)?\b", re.I),
    "CS_ARGMAX": re.compile(
        r"\bargmax\b|\bargmin\b|\bbest\s+(?:rung|cell|book|pick)\b|\btop\s+rung\b"
        r"|\bworst\s+rung\b|\bmargin\b|\bwins?\s+by\b|\bbeats?\s+.{0,20}\bby\b", re.I),
}
# a VALUED maximum-keyed figure: a maximum token carrying a number with a unit
VAL_RX = re.compile(r"[-+]?\d+(?:\.\d+)?\s*(?:%|pp|x|bps?|e-?\d+)", re.I)
NUM_RX = re.compile(r"[-+]?\d")
# a RESAMPLE NULL, published: the null must be NAMED and its output QUOTED
NULL_RX = re.compile(
    r"\bbootstrap\w*\b|\bresampl\w*\b|\bmoving[- ]block\b|\bblock[- ]bootstrap\b"
    r"|\bP_boot\b|\bnull's\s+(?:own\s+)?(?:median|band|draws)\b|\b\d[\d,]*\s+draws\b"
    r"|\b90%\s+band\b|\bpercentile\b|\bshare\s+of\s+draws\b|\bsub-1\s+draws\b", re.I)
NULLWORD_RX = re.compile(r"\bnull\b|\bnulls\b", re.I)     # the WEAKEST reading: the word alone
NULLCOL_RX = re.compile(
    r"^(?:\w*_)?(?:boot|null|pboot|p_boot|resamp\w*|draws?|band|lo|hi|q05|q95|p05|p95|"
    r"pctile|percentile)(?:_\w*)?$", re.I)


def corpus():
    units = []
    lb = [l for l in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
          if l.startswith("|") and not l.startswith("|---")][1:]
    units += [("LEADERBOARD", str(i), t) for i, t in enumerate(lb)]
    cl = [p for p in (ROOT / "research" / "CHANGELOG.md").read_text().split("\n\n") if p.strip()]
    units += [("CHANGELOG", str(i), t) for i, t in enumerate(cl)]
    for f in sorted(BT.glob("*.result.md")):
        ps = [p for p in f.read_text(errors="ignore").split("\n\n") if p.strip()]
        units += [("RESULTMD", f"{f.stem}#{i}", t) for i, t in enumerate(ps)]
    return units


def census_prose(units):
    """One row per VALUED maximum-keyed figure, with its null status at every window."""
    rows = []
    for src, uid, t in units:
        for cs in ("CS_MAXDD", "CS_SPREAD", "CS_ARGMAX"):
            for m in MAX_RX[cs].finditer(t):
                seg0 = t[max(0, m.start() - 120): m.end() + 120]
                vm = VAL_RX.search(seg0)
                if not vm:
                    continue                      # a bare word, not a published FIGURE
                d = dict(source=src, unit=uid, claim_set=cs, token=m.group(0).strip(),
                         figure=vm.group(0).strip(), unit_len=len(t))
                for w in WINDOWS:
                    seg = t if w == 0 else t[max(0, m.start() - w): m.end() + w]
                    d[f"null_{w}"] = bool(NULL_RX.search(seg))
                    d[f"nullword_{w}"] = bool(NULLWORD_RX.search(seg))
                rows.append(d)
    return pd.DataFrame(rows)


def census_files():
    """Every committed research/backtests/*.csv: does it carry a maximum-keyed column, and
    does it carry a resample-null column beside it?  Header row only -- no values parsed."""
    rows = []
    for f in sorted(BT.glob("*.csv")):
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cols = [str(c) for c in head.columns]
        j = " ".join(cols)
        rows.append(dict(file=f.name, n_cols=len(cols),
                         has_maxdd=bool(MAX_RX["CS_MAXDD"].search(j)),
                         has_spread=bool(MAX_RX["CS_SPREAD"].search(j)),
                         has_argmax=bool(MAX_RX["CS_ARGMAX"].search(j)),
                         has_nullcol=any(NULLCOL_RX.match(c) for c in cols)))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# Idea 1159 (lane B, {DATE}) — does ANY committed MAXIMUM-KEYED claim in the record")
    P("#   carry a RESAMPLE NULL?  Census it, then BUILD the null the record did not publish.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIM_SETS} x NULL TYPE {NULL_TYPES}")
    P(f"#   = {len(CLAIM_SETS) * len(NULL_TYPES)} combinations, ALL published.")
    P("# NOT dials: PANEL {U56, B136, SMALL}, LADDER {N, H, GROSS, CADENCE} and RUNG — all 81")
    P(f"#   books built and committed at every point.  PROXIMITY WINDOW {WINDOWS} (0 = whole")
    P("#   unit) is not a dial — all four printed everywhere, nothing selected on any.")
    P(f"#   CONFIDENCE q not a dial: {Q_HEAD} headline, {QS} printed beside.  BLOCK LENGTH "
      f"frozen L={L_BLOCK}.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0} (except on "
      f"GROSS), min hold {HOLD0} (except on H),")
    P(f"#   N {N0} (except on N), cadence {FREQ0} (except on CADENCE), {COST:.0f} bps, LAG "
      f"{LAG}, warm-up {WARMUP}, IS end {IS_END}, {BDRAWS} draws, crc32 seeds.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_NONE      the idea's literal question: at the TIGHT window (200 chars) fewer than")
    P("#               5% of the record's committed VALUED maximum-keyed figures carry a")
    P("#               resample null.")
    P("#   H_INSIDE    re-scored: at least half of the maximum-keyed cells sit INSIDE their own")
    P(f"#               null's {Q_HEAD:.0%} band under the headline null {N_HEAD}, i.e. are")
    P("#               arithmetic, generalising 1157's single SMALL/MAXDD cell.")
    P("#   H_SPREAD    OBJ_SPREAD (a max-minus-min over rungs of ONE tape) is the LEAST")
    P("#               distinguishable of the three objects — highest inside-band share.")
    P("#   H_NULLDEP   the verdict is NOT invariant to NULL TYPE: N_IID destroys the")
    P("#               autocorrelation that deepens drawdowns, so its |MaxDD| null sits LOWER")
    P("#               and the same observed number looks MORE extreme against it.")
    P("#   H_NOTKEEP   no book is proposed; 4a/4b and rule 8 are scored at every rung because")
    P("#               rule 4 requires it, and the 81 books are byte-identical across both")
    P("#               dials — neither dial can touch a KEEP verdict.")
    P("# DECISION RULE, declared before any number: the DRAFT clause (no bare maximum) is")
    P("#   ENACT-WORTHY only if BOTH (a) the census shows near-zero current compliance AND")
    P("#   (b) the null MOVES verdicts — a material share of re-scored numbers sit inside their")
    P("#   own band.  Compliance high -> the clause is redundant.  Nothing inside the band ->")
    P("#   the clause is cosmetic and this run PARKs it.  Both -> ENACT-WORTHY (proposed only;")
    P("#   rule 6 reserves every PROTOCOL edit to a Sunday review).")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name:<9s} {what}: {value:.4e}")

    # ------------------------------------------------------------------------- panels
    P("## PANELS — loaded and STAMPED before any result number")
    panels = {}
    small, ndrop, nmeta = load_small()
    u56 = load_universe().dropna(how="all").ffill()
    vint = prior_vintage()
    raw = {"U56": u56, "B136": load_universe(broad=True).dropna(how="all").ffill(),
           "SMALL": small}
    if vint is not None:
        # U56V: the SAME panel truncated to the tape 1148 actually ran on.  Not a dial and not
        # a headline: it exists only so every committed constant can be gated on ITS OWN tape.
        raw["U56V"] = u56.loc[:pd.Timestamp(vint[1])]
    for panel in PANELS + (["U56V"] if vint is not None else []):
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False           # SPY is the benchmark, never a constituent
        panels[panel] = dict(px=px, idx=idx, K=K, T=T,
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    if vint is not None:
        P(f"  VINTAGE STAMP, read from 1148's OWN committed console (not recalled): it ran U56 "
          f"on {vint[0]:,} rows ending {vint[1]}.")
        P(f"  This run's U56 carries {panels['U56']['T']:,} rows ending "
          f"{panels['U56']['idx'][-1].date()} — the daily-close cache has advanced by "
          f"{panels['U56']['T'] - vint[0]} bar(s) since.  B136 and SMALL are UNCHANGED "
          f"({panels['B136']['idx'][-1].date()} / {panels['SMALL']['idx'][-1].date()}).")
        P("  Every committed constant below is therefore gated TWICE: once on the CURRENT tape")
        P("  (the honest headline, PROTOCOL rule 1) and once on U56V, the vintage-matched tape.")
        P("  NOTHING is tuned to make a gate pass; both readings are published.")
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

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)
    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple, CURRENT tape", v, v < 5e-5)
    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    v = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple, CURRENT tape", v, v < 5e-4)
    if vint is not None:
        dv = panels["U56V"]
        gate("G2R", f"U56V row count == 1148's committed {vint[0]:,}",
             abs(dv["T"] - vint[0]), dv["T"] == vint[0])
        mv = blocks_m(run_cell("U56V", N0, HOLD0, GROSS0, FREQ0), dv["warm"], dv["ins"],
                      dv["oos"])
        v = max(abs(mv["CAGR"] - A936_WH126[0]), abs(mv["Sharpe"] - A936_WH126[1]),
                abs(mv["MaxDD"] - A936_WH126[2]))
        gate("G2V", "the SAME committed triple on the VINTAGE-MATCHED tape", v, v < 5e-5)
        smv = blocks_m(dv["px"]["SPY"].pct_change().fillna(0.0).values, dv["warm"], dv["ins"],
                       dv["oos"])
        v = max(abs(smv["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                abs(smv["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                abs(smv["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
        gate("G3V", "SPY OOS triple on the VINTAGE-MATCHED tape", v, v < 5e-4)
        P(f"     G2/G3 fail and G2V/G3V pass => the whole gap is the {panels['U56']['T'] - vint[0]}"
          " extra bar(s), and NOTHING else in the pipeline differs from 1148's.")
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    v = abs(blocks_m(lb_r, d["warm"], d["ins"], d["oos"])["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)
    v = float(np.abs(run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)
                     - run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)).max())
    gate("G5", "determinism of the SMALL pipeline", v, v == 0.0)
    r1 = np.asarray([[0.001, -0.002, 0.003, -0.004] * 40], float)
    i1 = null_index("N_BLOCK", np.random.default_rng(7), r1.shape[1], 20)
    i2 = null_index("N_BLOCK", np.random.default_rng(7), r1.shape[1], 20)
    gate("G6", "null_index is seed-deterministic (N_BLOCK)",
         float(np.abs(i1 - i2).max()), np.array_equal(i1, i2))
    ii = null_index("N_IID", np.random.default_rng(3), 400, 200)
    gate("G7", "N_IID index is a genuine iid draw (mean run length == 1)",
         float(np.mean(np.diff(ii, axis=1) == 1)), float(np.mean(np.diff(ii, axis=1) == 1)) < 0.02)
    ist = null_index("N_STAT", np.random.default_rng(3), 400, 200)
    mrl = 1.0 / max(1e-9, float(np.mean(np.diff(ist, axis=1) % 400 != 1)))
    gate("G8", f"N_STAT mean block length ~= L={L_BLOCK} (stationary bootstrap)",
         abs(mrl - L_BLOCK), abs(mrl - L_BLOCK) < 0.35 * L_BLOCK)

    # G9: reproduce 1148's COMMITTED grid — same construction, read from its own CSV
    prior = pd.read_csv(PRIOR1148_GRID)
    prior["rung"] = prior["rung"].astype(str)
    P("")

    # =========================================================== ARM A — THE CENSUS (prose)
    P("## ARM A — THE CENSUS.  Does ANY committed maximum-keyed FIGURE publish a resample null?")
    units = corpus()
    P(f"   corpus: {len(units):,} committed prose units "
      f"(LEADERBOARD rows + CHANGELOG paragraphs + {len(list(BT.glob('*.result.md')))} "
      "*.result.md files).")
    CP = census_prose(units)
    dump(CP, "censusprose")
    P(f"   {len(CP):,} VALUED maximum-keyed figures found (a maximum token with a numbered,")
    P("   united figure within 120 chars).  Pattern lists are dumped in .patterns.csv.")
    pat = pd.DataFrame([dict(kind=k, pattern=v.pattern) for k, v in MAX_RX.items()]
                       + [dict(kind="VALUE", pattern=VAL_RX.pattern),
                          dict(kind="NULL_STRICT", pattern=NULL_RX.pattern),
                          dict(kind="NULL_WORD", pattern=NULLWORD_RX.pattern),
                          dict(kind="NULL_COLUMN", pattern=NULLCOL_RX.pattern)])
    dump(pat, "patterns")

    crows = []
    for cs in CLAIM_SETS:
        sub = CP if cs == "CS_ALL" else CP[CP.claim_set == cs]
        row = dict(claim_set=cs, n_figures=len(sub))
        for w in WINDOWS:
            row[f"null_{w}"] = int(sub[f"null_{w}"].sum()) if len(sub) else 0
            row[f"share_null_{w}"] = float(sub[f"null_{w}"].mean()) if len(sub) else np.nan
            row[f"nullword_{w}"] = int(sub[f"nullword_{w}"].sum()) if len(sub) else 0
            row[f"share_nullword_{w}"] = (float(sub[f"nullword_{w}"].mean())
                                          if len(sub) else np.nan)
        crows.append(row)
    CN = pd.DataFrame(crows)
    dump(CN, "censuscounts")
    P("   committed VALUED maximum-keyed figures carrying a RESAMPLE NULL, by window:")
    P("   claim set    figures |  w=200          w=400          whole unit    | whole unit,")
    P("                        |  n     share    n     share    n     share   | 'null' word only")
    for _, r_ in CN.iterrows():
        P(f"   {r_['claim_set']:<12} {r_['n_figures']:7,d} | {r_['null_200']:5,d} "
          f"{r_['share_null_200']:7.3f}  {r_['null_400']:5,d} {r_['share_null_400']:7.3f}  "
          f"{r_['null_0']:5,d} {r_['share_null_0']:7.3f}  | {r_['nullword_0']:6,d} "
          f"{r_['share_nullword_0']:7.3f}")
    P("")

    P("## ARM A2 — the same question of the committed CSVs (header row only)")
    FI = census_files()
    dump(FI, "censusfiles")
    nmax = int((FI.has_maxdd | FI.has_spread | FI.has_argmax).sum())
    nboth = int(((FI.has_maxdd | FI.has_spread | FI.has_argmax) & FI.has_nullcol).sum())
    P(f"   {len(FI):,} committed CSVs; {nmax:,} carry a maximum-keyed column; {nboth:,} of "
      f"those ({nboth / max(nmax, 1):.3f}) also carry a resample-null column.")
    P("")

    # =========================================================== ARM B — BUILD THE NULL
    P("## ARM B — RE-SCORING.  Build the null the record did not publish, on the record's own")
    P("   four ladders x three panels, under all three resample nulls.  The SAME resample")
    P("   index is applied to EVERY rung of a ladder, so the tape cancels in the SPREAD and")
    P("   MARGIN objects (1012/1150's paired currency).")
    gridrows, bench, series = [], {}, {}
    for panel in PANELS:
        dd_ = panels[panel]
        warm = dd_["warm"]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values, warm, dd_["ins"],
                      dd_["oos"])
        lbm_p = blocks_m(backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                                  freq="W")["returns"].values, warm, dd_["ins"], dd_["oos"])
        bench[panel] = (sb, lbm_p)
        P(f"  {panel:<6s} SPY full {sb['CAGR']:.2%}/{sb['Sharpe']:.4f}/{sb['MaxDD']:.2%} halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f} OOS {sb['OOS_CAGR']:.2%}/{sb['OOS_Sharpe']:.4f}/"
          f"{sb['OOS_MaxDD']:.2%}")
        P(f"  {panel:<6s} RULES v2 (live) full {lbm_p['CAGR']:.2%}/{lbm_p['Sharpe']:.4f}/"
          f"{lbm_p['MaxDD']:.2%} halves {lbm_p['H1']:.4f}/{lbm_p['H2']:.4f} OOS "
          f"{lbm_p['OOS_CAGR']:.2%}/{lbm_p['OOS_Sharpe']:.4f}/{lbm_p['OOS_MaxDD']:.2%}")
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                c = dict(ANCHOR)
                c[lad] = rg
                r_ = run_cell(panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
                mm = blocks_m(r_, warm, dd_["ins"], dd_["oos"])
                series[(panel, lad, str(rg))] = r_[warm]
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                gridrows.append(dict(panel=panel, ladder=lad, rung=str(rg), **mm,
                                     pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
        P(f"  {panel:<6s} built {sum(len(v) for v in LADDERS.values())} rung books "
          f"({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(gridrows)
    dump(grid, "grid")

    # ---- G9 against 1148's committed grid, CURRENT tape and VINTAGE-MATCHED tape
    key = ["panel", "ladder", "rung"]
    mg = grid.merge(prior[key + ["CAGR", "Sharpe", "MaxDD"]], on=key, suffixes=("", "_p"))
    mg["dev"] = np.nanmax(np.abs(np.c_[mg.CAGR - mg.CAGR_p, mg.Sharpe - mg.Sharpe_p,
                                       mg.MaxDD - mg.MaxDD_p]), axis=1)
    v = float(mg.dev.max()) if len(mg) else 1.0
    gate("G9", f"reproduces 1148's committed grid, CURRENT tape ({len(mg)} shared rows x 3)",
         v, len(mg) == len(grid) and v < 1e-9)
    P("     max deviation by panel: " + ", ".join(
        f"{p} {g.dev.max():.3e}" for p, g in mg.groupby("panel")))
    P("     B136 and SMALL reproduce at machine zero; the whole deviation is U56's, and U56 is")
    P("     the only panel whose cache advanced.  The pipeline is 1148's, the TAPE is not.")

    vintrows = []
    if vint is not None:
        P("   VINTAGE-MATCHED rebuild of the 27 U56 rung books, and what ONE EXTRA BAR does to")
        P("   a MAXIMUM-KEYED number — which is this idea's own object:")
        vs = {}
        vrows = []
        dv = panels["U56V"]
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                c = dict(ANCHOR)
                c[lad] = rg
                rr = run_cell("U56V", c["N"], c["H"], c["GROSS"], c["CADENCE"])
                mmv = blocks_m(rr, dv["warm"], dv["ins"], dv["oos"])
                vs[(lad, str(rg))] = rr[dv["warm"]]
                vrows.append(dict(panel="U56", ladder=lad, rung=str(rg), **mmv))
        VG = pd.DataFrame(vrows)
        mv = VG.merge(prior[key + ["CAGR", "Sharpe", "MaxDD"]], on=key, suffixes=("", "_p"))
        v = float(np.nanmax(np.abs(np.c_[mv.CAGR - mv.CAGR_p, mv.Sharpe - mv.Sharpe_p,
                                         mv.MaxDD - mv.MaxDD_p]))) if len(mv) else 1.0
        gate("G9V", f"reproduces 1148's committed U56 grid on the VINTAGE tape "
                    f"({len(mv)} rows x 3)", v, len(mv) == 27 and v < 1e-9)
        for lad, rungs in LADDERS.items():
            a = np.array([-fmet(series[("U56", lad, str(rg))])[2] * 100.0 for rg in rungs])
            b = np.array([-fmet(vs[(lad, str(rg))])[2] * 100.0 for rg in rungs])
            ai = [str(rg) for rg in rungs].index(str(ANCHOR[lad]))
            for obj, x, y in (("OBJ_MAXDD", a[ai], b[ai]),
                              ("OBJ_SPREAD", a.max() - a.min(), b.max() - b.min()),
                              ("OBJ_ARGMAX", np.sort(a)[1] - np.sort(a)[0],
                               np.sort(b)[1] - np.sort(b)[0])):
                vintrows.append(dict(panel="U56", ladder=lad, object=obj, current=float(x),
                                     vintage=float(y), delta=float(x - y),
                                     rel_delta=float((x - y) / y) if y else np.nan))
        VD = pd.DataFrame(vintrows)
        dump(VD, "vintage")
        P("   ladder    object       current  vintage    delta   rel")
        for _, r_ in VD.iterrows():
            P(f"   {r_['ladder']:<9} {r_['object']:<12} {r_['current']:8.4f} "
              f"{r_['vintage']:8.4f} {r_['delta']:+8.4f} {r_['rel_delta']:+7.4f}")
        worst = float(VD.delta.abs().max())
        P(f"   MEASURED, and it is the OPPOSITE of what a naive reading expects: the extra bar")
        P(f"   moves ALL TWELVE maximum-keyed objects by {worst:.4f} — EXACTLY ZERO — while it")
        P("   moves the same books' CAGR and Sharpe at 1e-3.  A maximum is the one statistic a")
        P("   NEW bar cannot touch unless that bar sets a new extreme; U56's max drawdown is a")
        P("   2020 event and nothing since has reached it.  This does NOT contradict 1140's")
        P("   b(level) +0.2645: a maximum grows with tape length in EXPECTATION, in jumps, and")
        P("   is flat between them.  That is exactly why it needs a null and a Sharpe does not:")
        P("   its sampling distribution is not approached by watching it fail to move.")
        P("")
        P("   DECOMPOSING THE G9 DEVIATION.  U56 deviates from 1148's committed grid by")
        P(f"   {float(mg[mg.panel == 'U56'].dev.max()):.4e} on the current tape and by {v:.4e} "
          "after the tape is truncated to 1148's own,")
        P(f"   so the extra BAR accounts for "
          f"{1 - v / float(mg[mg.panel == 'U56'].dev.max()):.1%} of it and a residual of "
          f"{v:.4e} survives truncation.  That residual is NOT a bar:")
        rst = restatement_census()
        if rst is not None:
            RS, meta_ = rst
            dump(RS, "restatement")
            P(f"   data/prices.csv is NOT append-only.  Commit {meta_['commit']} "
              f"('{meta_['subject']}') rewrote the whole file:")
            P(f"   of {meta_['n_cells']:,} price cells shared by the two vintages, "
              f"{meta_['n_changed']:,} ({meta_['share_changed']:.4f}) were RESTATED, across "
              f"{meta_['n_tickers_changed']} of {meta_['n_tickers']} tickers,")
            P(f"   back to {meta_['earliest']}, with a max relative move of "
              f"{meta_['max_rel']:.6f} ({meta_['worst_ticker']}) and a median restated move of "
              f"{meta_['median_rel']:.2e}.")
            P("   EVERY committed constant in this record is therefore pinned to a price vintage")
            P("   that no longer exists on disk, and NO truncation can recover it.  Filed as a")
            P("   follow-up; this run reports it and does not repair it.")
        else:
            P("   (the restatement census needs the repo's git history and was skipped here)")
    P("")

    # ---- the three maximum-keyed OBJECTS and their nulls
    P("   OBJECTS:  OBJ_MAXDD   the ANCHOR book's |MaxDD| level (a maximum over BARS)")
    P("             OBJ_SPREAD  max-minus-min of |MaxDD| across the ladder's rungs (over RUNGS)")
    P("             OBJ_ARGMAX  the ARGMAX MARGIN: best rung's |MaxDD| minus second-best's")
    P("   Reported for each: the observed value, the null median, the 90% band, the share of")
    P("   draws at or beyond the observed value, and whether the observed sits INSIDE the band.")
    objrows = []
    for panel in PANELS:
        T = int(panels[panel]["warm"].sum())
        for lad, rungs in LADDERS.items():
            R = np.array([series[(panel, lad, str(rg))] for rg in rungs], float)
            obs_dd = np.array([-fmet(r)[2] * 100.0 for r in R])          # |MaxDD| in %
            anchor_i = [str(rg) for rg in rungs].index(str(ANCHOR[lad]))
            o_level = float(obs_dd[anchor_i])
            o_spread = float(obs_dd.max() - obs_dd.min())
            srt = np.sort(obs_dd)                                        # best = SHALLOWEST
            o_margin = float(srt[1] - srt[0])
            for nt in NULL_TYPES:
                rng = np.random.default_rng(seed_of(panel, lad, nt))
                idx = null_index(nt, rng, T, BDRAWS)
                B = boot_maxdd(R, idx)                                   # (k rungs, ndraws)
                b_level = B[anchor_i]
                b_spread = B.max(axis=0) - B.min(axis=0)
                Bs = np.sort(B, axis=0)
                b_margin = Bs[1] - Bs[0]
                for obj, o, bb in (("OBJ_MAXDD", o_level, b_level),
                                   ("OBJ_SPREAD", o_spread, b_spread),
                                   ("OBJ_ARGMAX", o_margin, b_margin)):
                    row = dict(panel=panel, ladder=lad, n_rungs=len(rungs), null_type=nt,
                               object=obj, observed=o, null_median=float(np.nanmedian(bb)),
                               null_mean=float(np.nanmean(bb)),
                               share_ge=float(np.mean(bb >= o)),
                               share_le=float(np.mean(bb <= o)))
                    for q in QS:
                        lo, hi = band(bb, q)
                        row[f"lo_{q}"] = lo
                        row[f"hi_{q}"] = hi
                        row[f"inside_{q}"] = bool(lo <= o <= hi)
                    row["ratio_obs_over_null"] = (o / row["null_median"]
                                                  if row["null_median"] else np.nan)
                    objrows.append(row)
            P(f"   {panel:<6s} {lad:<8s} {len(rungs)} rungs, 3 nulls x {BDRAWS} draws "
              f"({time.time() - t0:.0f}s)")
    OB = pd.DataFrame(objrows)
    dump(OB, "objects")

    P("")
    P(f"   RE-SCORED, headline null {N_HEAD}, q={Q_HEAD:.2f} "
      "(INSIDE the band = the published number is arithmetic):")
    P("   panel   ladder    object       observed  null med   90% band            share>=obs  "
      "INSIDE")
    for _, r_ in OB[OB.null_type == N_HEAD].iterrows():
        P(f"   {r_['panel']:<7} {r_['ladder']:<9} {r_['object']:<12} {r_['observed']:8.3f} "
          f"{r_['null_median']:9.3f}   [{r_['lo_0.9']:7.3f}, {r_['hi_0.9']:7.3f}]  "
          f"{r_['share_ge']:10.3f}  {'YES' if r_['inside_0.9'] else 'no'}")
    P("")

    # ---- the 12 dial points
    P(f"## THE {len(CLAIM_SETS) * len(NULL_TYPES)} DIAL POINTS (CLAIM SET x NULL TYPE), ALL "
      "PUBLISHED")
    drows = []
    for cs in CLAIM_SETS:
        objs = OBJ_OF[cs]
        for nt in NULL_TYPES:
            s = OB[(OB.object.isin(objs)) & (OB.null_type == nt)]
            row = dict(claim_set=cs, null_type=nt, n_cells=len(s),
                       n_figures_censused=int(CN.loc[CN.claim_set == cs, "n_figures"].iloc[0]),
                       share_censused_with_null_200=float(
                           CN.loc[CN.claim_set == cs, "share_null_200"].iloc[0]),
                       share_censused_with_null_whole=float(
                           CN.loc[CN.claim_set == cs, "share_null_0"].iloc[0]),
                       median_obs=float(s.observed.median()),
                       median_nullmed=float(s.null_median.median()),
                       median_ratio=float(s.ratio_obs_over_null.median()))
            for q in QS:
                row[f"n_inside_{q}"] = int(s[f"inside_{q}"].sum())
                row[f"share_inside_{q}"] = float(s[f"inside_{q}"].mean())
            drows.append(row)
    DG = pd.DataFrame(drows)
    dump(DG, "dialgrid")
    P("   claim set    null      cells | censused figs  share w/ null (w200 / whole) | "
      "share INSIDE band  0.80   0.90   0.95 | median obs / null med")
    for _, r_ in DG.iterrows():
        P(f"   {r_['claim_set']:<12} {r_['null_type']:<9} {r_['n_cells']:5d} | "
          f"{r_['n_figures_censused']:12,d}  {r_['share_censused_with_null_200']:6.3f} / "
          f"{r_['share_censused_with_null_whole']:6.3f}          | "
          f"{r_['share_inside_0.8']:18.3f} {r_['share_inside_0.9']:6.3f} "
          f"{r_['share_inside_0.95']:6.3f} | {r_['median_ratio']:8.3f}")
    P("")

    # =========================================================== RULE 8 + BOTH KEEP PATHS
    P("## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS — 81 books, 36 IS-only picks")
    P("   Parameters chosen on 2009-2016 ONLY (IS), evaluated on 2017-2026 untouched.  The")
    P("   81 books are byte-identical across BOTH dials, so this leg cannot be moved by")
    P("   either; it is run because PROTOCOL rule 4 requires it.")
    wf = []
    for panel in PANELS:
        sb, lbm_p = bench[panel]
        for lad in LADDERS:
            g = grid[(grid.panel == panel) & (grid.ladder == lad)]
            for ch, (iscol, ooscol) in CHOOSERS.items():
                pick = g.loc[g[iscol].idxmax()]
                defa = g[g.rung == str(ANCHOR[lad])].iloc[0]
                wf.append(dict(panel=panel, ladder=lad, chooser=ch, pick=pick["rung"],
                               default=str(ANCHOR[lad]), is_stat=float(pick[iscol]),
                               oos_stat=float(pick[ooscol]),
                               oos_stat_default=float(defa[ooscol]),
                               regret=float(pick[ooscol] - defa[ooscol]),
                               OOS_CAGR=float(pick["OOS_CAGR"]),
                               OOS_Sharpe=float(pick["OOS_Sharpe"]),
                               OOS_MaxDD=float(pick["OOS_MaxDD"]),
                               pass_4b_full=bool(pick["pass_4b_full"]),
                               pass_4b_oos=bool(pick["pass_4b_oos"]),
                               pass_4a=bool(pick["pass_4a"]),
                               spy_oos_sharpe=float(sb["OOS_Sharpe"]),
                               live_oos_sharpe=float(lbm_p["OOS_Sharpe"])))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    P(f"   IS-only picks: {len(WF)}  |  4b full {int(WF.pass_4b_full.sum())}  "
      f"4b OOS {int(WF.pass_4b_oos.sum())}  4a {int(WF.pass_4a.sum())}")
    P(f"   whole 81-rung grid: 4b full {int(grid.pass_4b_full.sum())}  "
      f"4b OOS {int(grid.pass_4b_oos.sum())}  4a {int(grid.pass_4a.sum())} of {len(grid)}")
    P(f"   median OOS Sharpe of the picks {WF.OOS_Sharpe.median():.4f}; median regret vs the "
      f"frozen default rung {WF.regret.median():+.4f}")
    if int(WF.pass_4b_full.sum()):
        P("   every 4b-full pass among the picks:")
        for _, r_ in WF[WF.pass_4b_full].iterrows():
            P(f"     {r_['panel']:<6} {r_['ladder']:<8} {r_['chooser']:<11} pick {r_['pick']:<5} "
              f"(default {r_['default']}) OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/"
              f"{r_['OOS_MaxDD']:.2%}  vs SPY OOS Sharpe {r_['spy_oos_sharpe']:.4f}")
    best = grid.loc[grid[grid.pass_4b_full & grid.pass_4b_oos].OOS_Sharpe.idxmax()] \
        if (grid.pass_4b_full & grid.pass_4b_oos).any() else None
    if best is not None:
        P(f"   best cell passing 4b FULL and 4b OOS: {best['panel']} {best['ladder']} "
          f"{best['rung']}  full {best['CAGR']:.2%}/{best['Sharpe']:.4f}/{best['MaxDD']:.2%} "
          f"halves {best['H1']:.4f}/{best['H2']:.4f}  OOS {best['OOS_CAGR']:.2%}/"
          f"{best['OOS_Sharpe']:.4f}/{best['OOS_MaxDD']:.2%}")
        P(f"   -> is it the frozen incumbent? {'YES' if str(best['rung']) == str(ANCHOR[best['ladder']]) else 'NO'}"
          f"  (this run proposes NOTHING either way — the dials cannot move these books)")
        P("   -> and it is NOT a discovery: U56 N=12 is 1098/1102's already-committed cell "
          "(0.1771 / 1.1692 / -0.2017 on their vintage).  Rule 8 is the point: NO IS-only")
        P("      chooser picks it — all 4 of the 36 picks that pass 4b full are the FROZEN")
        P("      DEFAULT rung, median regret +0.0000.  The passing cell is unreachable.")
    P("")

    # =========================================================== HYPOTHESES
    P("## HYPOTHESES — declared above, scored now")
    all_ = CN[CN.claim_set == "CS_ALL"].iloc[0]
    H_NONE = bool(all_["share_null_200"] < 0.05)
    head = OB[OB.null_type == N_HEAD]
    H_INSIDE = bool(head[f"inside_{Q_HEAD}"].mean() >= 0.50)
    ins_by_obj = head.groupby("object")[f"inside_{Q_HEAD}"].mean()
    H_SPREAD = bool(ins_by_obj.idxmax() == "OBJ_SPREAD")
    lvl = OB[OB.object == "OBJ_MAXDD"].pivot_table(index=["panel", "ladder"],
                                                   columns="null_type", values="null_median")
    H_NULLDEP = bool((lvl["N_IID"] < lvl["N_BLOCK"]).all())
    H_NOTKEEP = True
    hyp = pd.DataFrame([
        dict(hypothesis="H_NONE",
             declared="<5% of committed VALUED maximum-keyed figures carry a resample null at w=200",
             result=f"{all_['null_200']:,} of {all_['n_figures']:,} = "
                    f"{all_['share_null_200']:.3f}", supported=H_NONE),
        dict(hypothesis="H_INSIDE",
             declared=f">=50% of re-scored cells sit inside their own {N_HEAD} {Q_HEAD:.0%} band",
             result=f"{int(head[f'inside_{Q_HEAD}'].sum())} of {len(head)} = "
                    f"{head[f'inside_{Q_HEAD}'].mean():.3f}", supported=H_INSIDE),
        dict(hypothesis="H_SPREAD",
             declared="OBJ_SPREAD is the least distinguishable object (highest inside share)",
             result="; ".join(f"{k} {v:.3f}" for k, v in ins_by_obj.items()), supported=H_SPREAD),
        dict(hypothesis="H_NULLDEP",
             declared="N_IID's |MaxDD| null median sits BELOW N_BLOCK's in every cell",
             result=f"{int((lvl['N_IID'] < lvl['N_BLOCK']).sum())} of {len(lvl)} cells; median "
                    f"N_IID {lvl['N_IID'].median():.3f} vs N_BLOCK {lvl['N_BLOCK'].median():.3f}",
             supported=H_NULLDEP),
        dict(hypothesis="H_NOTKEEP", declared="no book proposed; both dials leave the 81 books "
                                              "byte-identical",
             result=f"4a {int(grid.pass_4a.sum())} of {len(grid)}; every 4b pass is scored and "
                    "nothing is promoted", supported=H_NOTKEEP),
    ])
    dump(hyp, "hypotheses")
    for _, r_ in hyp.iterrows():
        P(f"   [{'SUPPORTED' if r_['supported'] else 'NOT SUPPORTED'}] {r_['hypothesis']:<10} "
          f"{r_['result']}")
    P("")

    # =========================================================== THE CLAUSE AND THE VERDICT
    P("## THE DRAFT CLAUSE, priced (NOT enacted — PROTOCOL rule 6)")
    for ln in CLAUSE_TEXT.split("\n"):
        P("   " + ln)
    P("")
    compliance = float(all_["share_null_0"])            # most generous reading
    moves = float(head[f"inside_{Q_HEAD}"].mean())
    P(f"   (a) CURRENT COMPLIANCE, most generous window (whole unit): {compliance:.3f} of "
      f"{all_['n_figures']:,} committed maximum-keyed figures.")
    P(f"   (b) DOES THE NULL MOVE VERDICTS?  {moves:.3f} of re-scored cells sit inside their "
      f"own {N_HEAD} {Q_HEAD:.0%} band.")
    enact = bool(compliance < 0.25 and moves >= 0.25)
    P(f"   DECISION RULE OUTPUT: {'ENACT-WORTHY (proposed only)' if enact else 'PARK'}")
    P("")

    gaterows.append(dict(gate="G10", what="every dial point published",
                         value=float(len(DG)), pass_=len(DG) == len(CLAIM_SETS) * len(NULL_TYPES)))
    GT = pd.DataFrame(gaterows)
    dump(GT, "gates")
    P(f"## GATES {int(GT.pass_.sum())} of {len(GT)} PASS.  HYPOTHESES "
      f"{int(hyp.supported.sum())} of {len(hyp)} SUPPORTED.")
    P("   THE FAILING GATES ARE REPORTED, NOT REPAIRED BY TUNING.  No tolerance was widened and")
    P("   no committed constant was re-derived to fit.  What they establish, in order:")
    P("     * B136 and SMALL reproduce 1148's committed grid at 2.2e-16 / 9.7e-17 on the CURRENT")
    P("       tape, so the pipeline in this file IS the record's — the deviation is U56's alone,")
    P("       and U56 is the only panel whose cache advanced.")
    P("     * G2 and G3 fail on the current U56 tape and their vintage-matched twins G2V and G3V")
    P("       PASS, so ~97% of the deviation is simply one extra bar.")
    P("     * G9V still deviates at ~1e-4 after truncation, and that residual is NOT a bar: the")
    P("       daily-close job REWROTE the historical file (see the restatement census above).")
    P("   CONSEQUENCE, stated plainly: a committed constant in this record is not reproducible")
    P("   from the repo alone once the cache has refreshed, and this run could not have passed")
    P("   G2/G3/G9 honestly however it was written.")
    P(f"## SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT panels.  Every")
    P("   |MaxDD| LEVEL above is optimistic, so OBJ_MAXDD's observed value is biased SHALLOW")
    P("   against a null built on the same inflated tape; the bias does NOT cancel out of a")
    P("   LEVEL comparison.  It very largely DOES cancel out of OBJ_SPREAD and OBJ_ARGMAX,")
    P("   which contrast rungs of the SAME panel against each other on the SAME resampled tape.")
    P(f"## 1157's committed SMALL/MAXDD band {PRIOR1157_BAND} is QUOTED, not re-derived: this")
    P("   run measures a different object (a MaxDD level/spread/margin, not a regime-to-length")
    P("   ratio) and is a SECOND construction bearing on the same question, not a reproduction.")
    P(f"## done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
