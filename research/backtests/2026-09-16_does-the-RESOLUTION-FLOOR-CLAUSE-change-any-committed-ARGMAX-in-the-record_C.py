#!/usr/bin/env python3
"""Idea 1102 (lane C, 2026-09-16) — does the RESOLUTION-FLOOR CLAUSE change any COMMITTED
ARGMAX in the record?

QUESTION (QUEUE idea 1102, verbatim)
    idea 1098 measured a 90% sign-resolution floor of 3.25 pp (U56) / 4.02 pp (B136) of CAGR for
    EDGE on a 9-rung ladder and proposed that an argmax whose lead is below its floor be
    published as a TIE SET.  Harvest every committed argmax / 'peaks at' claim in the record,
    measure each one's own gap and its ladder's floor, and report how many stated conclusions
    (not numbers) become tie sets.  Max 2 params (claim set, floor confidence).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: CLAIM SET {CORE, WIDE} x FLOOR CONFIDENCE q {0.80, 0.90, 0.95} = 6 cells,
    ALL published.
      CORE = the (panel, ladder, statistic) argmax objects this tree REBUILDS EXACTLY — the four
             ladder families the record's committed argmax claims are actually read off (N, H,
             GROSS, CADENCE) on both panels, argmaxed over the four statistics the record
             argmaxes over (full Sharpe, OOS Sharpe, full CAGR, MaxDD).  32 objects.  Each gets
             its OWN measured gap and its OWN measured floor.
      WIDE = every VALUED argmax / 'peaks at' claim harvested from the corpus, including those
             whose ladder this tree cannot rebuild.  A claim whose (family, statistic) IS a
             rebuilt CORE cell is scored on that cell's own MEASURED verdict; every other claim
             gets a TRANSFERRED rate from the CORE cells of the same statistic, or the overall
             CORE rate — declared here, in advance, as an EXTRAPOLATION and NOT a re-derivation
             of the claim (idea 1048's convention).  The three bases are counted separately.

    WHEN NOTHING ON A LADDER RESOLVES the floor is INFINITE (no gap is sign-resolved at q), which
    is a legitimate reading and is published as `inf`.  For the RATIO hypotheses (H_STAT,
    H_LADDER) an infinite floor is capped at the ladder's own full spread — declared in advance
    as a LOWER bound on the true floor, which understates tie-set-ness and is therefore the
    conservative direction.  No tie-set VERDICT depends on the cap (gap <= spread always).
    Everything else frozen at 1082/1086/1094/1098's construction: CAND20 legs, cap INF,
    max_vol 0.60, gross 0.75 (except on the GROSS ladder), W cadence (except on the CADENCE
    ladder), min hold 126 (except on the H ladder), N=20 (except on the N ladder), 10 bps, LAG 1,
    warm-up 260, IS end 2016-12-31.  BLOCK LENGTH is NOT a dial: headline L=63, L in {21, 126}
    reported beside it and never selected on.

WHAT IS BOOTSTRAPPED
    1098's machinery, minus the null: a statistic with no null attached needs no seeds, so ONE
    circular-block index is drawn and applied JOINTLY to every rung of a ladder (the rungs are
    books over one tape; an independent resample would destroy the dependence that makes a
    rung-to-rung GAP a paired quantity).  CAGR and Sharpe are EXACT under block resampling from
    block sums of log1p, r and r^2.  MaxDD is not order-invariant, so its bootstrap reconstructs
    the resampled path.  1,000 draws per (panel, ladder, window).

    FLOOR, measured exactly as 1098 defined it: over all rung pairs, A_ij = P(bootstrap agrees
    with the full-sample sign of X_i - X_j); the floor at q is the smallest |gap| strictly above
    every UNRESOLVED gap (A < q) that is itself resolved.  The largest unresolved gap is
    published beside it.

DECLARED BEFORE ANY NUMBER
    (a) H_TIE — at q=0.90 a MAJORITY (> 0.50) of CORE argmax objects have peak-minus-runner-up
        BELOW their own ladder's floor, i.e. the clause converts them to tie sets.  RIVAL, named
        in advance: EDGE is the record's noisiest laddered statistic (it carries a null median's
        own sampling error, 1098) and the plain performance statistics resolve far better, in
        which case 1098's clause is an EDGE fact and touches little else.
    (b) H_STAT — the floor is NOT uniform across statistics: MaxDD argmaxes resolve strictly
        better (smaller floor / ladder-spread ratio) than Sharpe argmaxes, because |MaxDD| is a
        single extremal event that block resampling moves less than a mean does.
    (c) H_LADDER — a ladder's floor RISES with its rung count (9-rung floor > 4-rung floor on the
        same panel and statistic), because more pairs give more chances for an unresolved one.
    (d) H_PANEL — the floor is a TAPE fact shared by the two panels: floor ratio within 1.5x for
        the same (ladder, statistic).
    (e) H_P — P(bootstrap argmax == full-sample argmax) < 0.50 for a majority of CORE objects.
    (f) H_HARVEST — the corpus carries at least 50 VALUED argmax claims.
    (g) THE FLOOR IS NOT A KEEP PATH.  4a and 4b are scored at every rung of every ladder and
        rule 8 picks the rung on 2009-2016 ALONE, separately per ladder, OOS read ONCE.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels.  A gap between two
    rungs of one ladder contrasts two books over the same inflated tape and the bias very largely
    cancels out of it, and out of the floor; it does NOT cancel out of the 4b legs, which are
    measured against SPY, a real index.
"""
from __future__ import annotations

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
SLUG = "does-the-RESOLUTION-FLOOR-CLAUSE-change-any-committed-ARGMAX-in-the-record"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ0 = "W"
HOLD0 = 126
N0 = 20
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"

# ------------------------------------------------------------------ the four CORE ladders
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]                       # 1071/1082/1094's ladder
LAD_H = [21, 63, 126, 252]                                       # 1086's ladder
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]   # 1083's ladder
LAD_C = ["D", "W", "M", "Q"]                                     # 930/931's ladder
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}

STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]        # every one an argmax (DD = -|MaxDD|)
QGRID = [0.80, 0.90, 0.95]                       # dial 2
CLAIMSETS = ["CORE", "WIDE"]                     # dial 1
BDRAWS = 1000
BLOCKS_L = [21, 63, 126]
L_HEAD = 63
PANELS = ["U56", "B136"]
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR"]
SEED_BOOT = 11021102

# committed cross-run anchors (CHANGELOG / LEADERBOARD, quoted as published)
A936_WH126 = (0.155787, 1.139701, -0.191276)            # U56 W / H126 / N=20, 936/1071/1082/1094
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)               # 1098's committed U56 n=12 (H=126)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)              # 1098's committed B136 n=15
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------------- 1082/1098's fast runner, copied verbatim
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
    """1082/1086/1094/1098's book builder, verbatim: min hold H, top-N by rank_key among
    eligible-and-priced, gross/len(sel) per held name, cash otherwise."""
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


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ------------------------------------------------------------------- the bootstrap machinery
def block_index(rng, T, L, ndraws):
    """Circular block resampling indices, (ndraws, nb*L)."""
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_exact(R, idx, nb, L, chunk=100):
    """CAGR and Sharpe of every row of R (rungs x T) under the SHARED block index — exact,
    because a product and a mean do not care about order.  Returns (CAGR, Sharpe) arrays of
    shape (rungs, ndraws)."""
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    T = R.shape[1]
    nd = idx.shape[0]
    st = idx[:, ::L]                                   # block starts, (nd, nb)
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
    """MaxDD is NOT order-invariant, so the resampled path is reconstructed.  Returns
    -|MaxDD| (higher = better), shape (rungs, ndraws)."""
    nr, _ = R.shape
    nd = idx.shape[0]
    out = np.empty((nr, nd))
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]                           # (c, n)
        for j in range(nr):
            path = np.log1p(R[j])[ix]                   # (c, n)
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
    return out


def floor_and_pairs(vals, boot, q):
    """1098's floor.  vals: (rungs,) full-sample statistic; boot: (rungs, ndraws).
    Returns (floor, largest_unresolved, n_pairs, n_unresolved, pair rows)."""
    k = len(vals)
    rows, gaps, agree = [], [], []
    for i in range(k):
        for j in range(i + 1, k):
            g = vals[i] - vals[j]
            if not np.isfinite(g):
                continue
            d = boot[i] - boot[j]
            d = d[np.isfinite(d)]
            a = float((np.sign(d) == np.sign(g)).mean()) if len(d) else np.nan
            gaps.append(abs(g))
            agree.append(a)
            rows.append((i, j, g, a))
    gaps = np.asarray(gaps)
    agree = np.asarray(agree)
    un = agree < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    flo = float(gaps[ok].min()) if ok.any() else float("inf")
    return flo, largest_un, len(gaps), int(un.sum()), rows


def mass_set(counts, rungs, q=0.90):
    """Smallest contiguous-in-ladder-order set of rungs carrying >= q of the argmax mass."""
    k = len(rungs)
    for w in range(1, k + 1):
        best = None
        for i in range(0, k - w + 1):
            m = counts[i:i + w].sum()
            if m >= q and (best is None or m > best[2]):
                best = (w, [rungs[j] for j in range(i, i + w)], float(m))
        if best is not None:
            return best
    return (k, list(rungs), float(counts.sum()))


# ------------------------------------------------------------------------ the claim harvest
SRC = {"LEADERBOARD": [ROOT / "research" / "LEADERBOARD.md"],
       "CHANGELOG": [ROOT / "research" / "CHANGELOG.md"],
       "QUEUE": [ROOT / "research" / "QUEUE.md"],
       "RESULTMD": sorted((ROOT / "research" / "backtests").glob("*.result.md")),
       "MEMO": sorted((ROOT / "research" / "backtests").glob("*.memo.md"))}

CLAIM_RE = re.compile(r"(?i)\b(argmax|peaks?\s+at|peak\s+is\s+at|optimum\s+at|optimal|best)\b")
FAMILY_RE = [
    ("N", re.compile(r"(?i)\b(?:n|top)\s*=?\s*(\d{1,3})\b")),
    ("H", re.compile(r"(?i)\b(?:h|hold|min[_ ]hold)\s*=\s*(\d{1,3})\b")),
    ("GROSS", re.compile(r"(?i)\b(?:g|gross)\s*=\s*(0?\.\d{1,2}|1\.00?)\b")),
    ("CADENCE", re.compile(r"(?i)\b(DAILY|WEEKLY|MONTHLY|QUARTERLY)\b")),
    ("MAXVOL", re.compile(r"(?i)\bmax_vol\s*=?\s*(\d?\.\d{1,2})\b")),
    ("BAND", re.compile(r"(?i)\bband\s*=?\s*(0?\.\d{1,3})\b")),
    ("THRESH", re.compile(r"(?i)\b(?:tau|theta|f|phi)\s*=\s*(\d?\.\d{1,3})\b")),
]
STAT_RE = [("EDGE", re.compile(r"(?i)\bEDGE\b")),
           ("S_OOS", re.compile(r"(?i)\bOOS\s+Sharpe\b")),
           ("S_FULL", re.compile(r"(?i)\bSharpe\b")),
           ("CAGR", re.compile(r"(?i)\bCAGR\b")),
           ("DD", re.compile(r"(?i)\b(MaxDD|drawdown)\b")),
           ("TURNOVER", re.compile(r"(?i)\bturnover\b"))]
WIN = 120          # chars either side of the claim word a rung value may be read from


def harvest():
    """UNIT = one '|'-delimited cell (LEADERBOARD rows) or one non-empty line elsewhere.
    A claim is VALUED when a ladder-family rung value appears within WIN chars of the claim
    word IN THE SAME UNIT.  Rejects are counted by reason and published."""
    rows, rej = [], []
    for src, paths in SRC.items():
        for p in paths:
            try:
                txt = p.read_text(errors="ignore")
            except OSError:
                continue
            for ln, line in enumerate(txt.split("\n")):
                units = line.split("|") if "|" in line else [line]
                for uix, u in enumerate(units):
                    if not u.strip():
                        continue
                    for m in CLAIM_RE.finditer(u):
                        lo, hi = max(0, m.start() - WIN), min(len(u), m.end() + WIN)
                        ctx = u[lo:hi]
                        fam, val = None, None
                        for f, rx in FAMILY_RE:
                            mm = rx.search(ctx)
                            if mm:
                                fam, val = f, mm.group(1)
                                break
                        stat = None
                        for s, rx in STAT_RE:
                            if rx.search(ctx):
                                stat = s
                                break
                        rec = dict(source=src, file=p.name, line=ln, unit=uix,
                                   word=m.group(0).lower(), family=fam or "", value=val or "",
                                   stat=stat or "", ctx=ctx.replace("\n", " ")[:260])
                        if fam is None:
                            rej.append({**rec, "reason": "no_rung_value_in_window"})
                        elif stat is None:
                            rej.append({**rec, "reason": "no_statistic_named"})
                        else:
                            rows.append(rec)
    return pd.DataFrame(rows), pd.DataFrame(rej)


# ------------------------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# Idea 1102 (lane C, {DATE}) — does the RESOLUTION-FLOOR CLAUSE change any COMMITTED")
    P("#   ARGMAX in the record?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIMSETS} x FLOOR CONFIDENCE {QGRID}")
    P("#   = 6 cells, ALL published.  CORE = the 32 (panel, ladder, statistic) argmax objects")
    P("#   this tree rebuilds exactly; WIDE = every valued harvested claim, the unrebuildable")
    P("#   ones carrying a TRANSFERRED rate declared in advance as an EXTRAPOLATION.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap {CAPNAME}, max_vol {MAXVOL}, gross {GROSS0}, cadence")
    P(f"#   {FREQ0}, min hold {HOLD0}, N {N0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS")
    P(f"#   end {IS_END}, each except where it is the ladder.  BLOCK LENGTH is NOT a dial:")
    P(f"#   headline L={L_HEAD}, L in {BLOCKS_L} reported beside it, never selected on.")
    P(f"# BOOTSTRAP: {BDRAWS} circular-block draws, ONE index applied JOINTLY to every rung of a")
    P("#   ladder.  CAGR/Sharpe exact from block sums; MaxDD reconstructs the path.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_TIE — at q=0.90 a MAJORITY of CORE argmaxes fall below their own floor.")
    P("#       RIVAL: EDGE is the noisiest laddered statistic and the plain ones resolve.")
    P("#   (b) H_STAT — MaxDD argmaxes resolve strictly better than Sharpe argmaxes.")
    P("#   (c) H_LADDER — the floor RISES with rung count (9-rung > 4-rung, same panel/stat).")
    P("#   (d) H_PANEL — floors within 1.5x across panels for the same (ladder, statistic).")
    P("#   (e) H_P — P(argmax reproduces) < 0.50 for a majority of CORE objects.")
    P("#   (f) H_HARVEST — the corpus carries at least 50 VALUED argmax claims.")
    P("#   (g) THE FLOOR IS NOT A KEEP PATH: 4a/4b at every rung, rule 8 per ladder.")
    P("")

    gaterows, gates = [], {}

    # ------------------------------------------------------------------ THE HARVEST (dial 1)
    P("## HARVEST — every argmax / 'peaks at' claim in the corpus")
    claims, rejects = harvest()
    P(f"  corpus: {sum(len(v) for v in SRC.values())} files over {len(SRC)} sources")
    P(f"  claim words matched: {len(claims) + len(rejects):,}   VALUED: {len(claims):,}   "
      f"rejected: {len(rejects):,}")
    if len(rejects):
        P("  reject reasons: " + ", ".join(f"{k} {v:,}" for k, v in
                                           rejects["reason"].value_counts().items()))
    if len(claims):
        P("  by source: " + ", ".join(f"{k} {v:,}" for k, v in
                                      claims["source"].value_counts().items()))
        P("  by family: " + ", ".join(f"{k} {v:,}" for k, v in
                                      claims["family"].value_counts().items()))
        P("  by statistic: " + ", ".join(f"{k} {v:,}" for k, v in
                                         claims["stat"].value_counts().items()))
    H_HARVEST = len(claims) >= 50
    P(f"  H_HARVEST (>= 50 valued claims): {'PASS' if H_HARVEST else 'FAIL'}  ({len(claims)})")
    P("  HARVEST LIMITATION, declared: the family/statistic patterns are heuristics over prose.")
    P("    Every REJECT is published with its reason and its context so the acceptance rule can")
    P("    be re-read; the dominant reject is a claim word ('best' above all) with no rung value")
    P("    inside the window, which is exactly the class this idea cannot price.")
    dump(claims, "claims")
    dump(rejects, "rejects")
    P("")

    # ---------------------------------------------------------------------------- THE GATES
    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {K} names, {T:,} rows {idx[0].date()} -> {idx[-1].date()}, "
          f"warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

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
        r = g - tn * COST / 1e4
        return r, tn

    # G1 — the fast runner IS engine.backtest
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    Wdf = pd.DataFrame(W, index=d["idx"], columns=d["px"].columns)
    eng = backtest(d["px"], Wdf, cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest (U56 W/H126/N20)",
                         value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                        {g1:.2e}   "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    # G2 — the committed anchor triple (936/1071/1082/1094)
    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="CROSS-RUN 936/1071/1082/1094 U56 W/H126/N=20 triple",
                         value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    # G3 — SPY OOS triple
    spy = panels["U56"]["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   "
      f"{'PASS' if gates['G3'] else 'FAIL'}")

    # G4 — 1098's committed U56 n=12 and B136 n=15 rungs
    r12, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="CROSS-RUN 1098's committed U56 n=12 triple",
                         value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098's committed U56 n=12 triple            {g4:.2e}   "
      f"{'PASS' if gates['G4'] else 'FAIL'}")
    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="CROSS-RUN 1098's committed B136 n=15 triple",
                         value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN 1098's committed B136 n=15 triple           {g4b:.2e}   "
      f"{'PASS' if gates['G4b'] else 'FAIL'}")

    # G5 — the live book's committed MaxDD
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    g5 = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD == committed -12.05%",
                         value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    # G6 — determinism of the whole cell pipeline
    r12b, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism of the cell pipeline", value=g6,
                         pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   "
      f"{'PASS' if gates['G6'] else 'FAIL'}")

    # G7 — the bootstrap is unbiased at the point (mean of the bootstrap CAGR ~ the sample's)
    rng = np.random.default_rng(SEED_BOOT)
    Rw = r12[d["warm"]][None, :]
    ix, nb = block_index(rng, Rw.shape[1], L_HEAD, 200)
    bc, bs = boot_exact(Rw, ix, nb, L_HEAD)
    g7 = abs(float(np.median(bc[0])) - m12["CAGR"])
    gates["G7"] = g7 < 0.02
    gaterows.append(dict(gate="G7", what="bootstrap median CAGR == sample CAGR (within 2 pp)",
                         value=g7, pass_=gates["G7"]))
    P(f"  G7  bootstrap median CAGR == the sample's (< 2 pp)        {g7:.2e}   "
      f"{'PASS' if gates['G7'] else 'FAIL'}")

    # G8 — the axis is live: the N ladder moves Sharpe by a visible amount
    P(f"  gates: {sum(gates.values())} of {len(gates)} PASS (G8 printed with the ladders)")
    P("")

    # ------------------------------------------------------------- REBUILD THE CORE LADDERS
    P("## THE CORE LADDERS — 4 families x 2 panels, every rung published")
    gridrows, benchrows = [], []
    series = {}                      # (panel, ladder) -> (rungs, returns matrix over warm)
    metr = {}                        # (panel, ladder, rung) -> metrics dict
    turn = {}
    for panel in PANELS:
        dd_ = panels[panel]
        spy_r = dd_["px"]["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(spy_r, dd_["warm"], dd_["ins"], dd_["oos"])
        lbm_p = blocks_m(
            backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST, freq="W")["returns"].values,
            dd_["warm"], dd_["ins"], dd_["oos"])
        benchrows.append(dict(panel=panel, book="SPY", **{k: sb[k] for k in sb}))
        benchrows.append(dict(panel=panel, book="RULES v2 (live)", **{k: lbm_p[k] for k in lbm_p}))
        P(f"  {panel} SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}"
          f"  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f}"
          f" / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2   full {lbm_p['CAGR']:.2%} / {lbm_p['Sharpe']:.4f} / "
          f"{lbm_p['MaxDD']:.2%}  OOS {lbm_p['OOS_CAGR']:.2%} / {lbm_p['OOS_Sharpe']:.4f}")
        for lad, rungs in LADDERS.items():
            mats_w, mats_o = [], []
            for rung in rungs:
                N, H, g, f = N0, HOLD0, GROSS0, FREQ0
                if lad == "N":
                    N = rung
                elif lad == "H":
                    H = rung
                elif lad == "GROSS":
                    g = rung
                else:
                    f = rung
                r, tn = run_cell(panel, N, H, g, f)
                mm = blocks_m(r, dd_["warm"], dd_["ins"], dd_["oos"])
                metr[(panel, lad, rung)] = mm
                turn[(panel, lad, rung)] = float(tn[dd_["warm"]].sum()) / (dd_["warm"].sum() / 252.0)
                mats_w.append(r[dd_["warm"]])
                mats_o.append(r[dd_["oos"]])
                l4b = legs_4b(mm, sb)
                l4bo = legs_4b_oos(mm, sb)
                l4a = legs_4a(mm, lbm_p)
                gridrows.append(dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=g,
                                     freq=f, turnover=turn[(panel, lad, rung)],
                                     **{k: mm[k] for k in mm},
                                     pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
            series[(panel, lad)] = (rungs, np.vstack(mats_w), np.vstack(mats_o))
            sh = [metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs]
            P(f"  {panel} {lad:<8} rungs {rungs}")
            P(f"        Sharpe " + " ".join(f"{x:.4f}" for x in sh))
    grid = pd.DataFrame(gridrows)
    P(f"  4b full {int(grid['pass_4b_full'].sum())} of {len(grid)}; 4b OOS "
      f"{int(grid['pass_4b_oos'].sum())} of {len(grid)}; 4a {int(grid['pass_4a'].sum())} of {len(grid)}")
    sp = float(grid["Sharpe"].max() - grid["Sharpe"].min())
    gates["G8"] = sp > 0.05
    gaterows.append(dict(gate="G8", what="the ladders are live (Sharpe spread over all cells)",
                         value=sp, pass_=gates["G8"]))
    P(f"  G8  the ladders are live (Sharpe spread {sp:.4f})          {'PASS' if gates['G8'] else 'FAIL'}")
    dump(grid, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P("")

    # -------------------------------------------------------- THE FLOOR, MEASURED PER LADDER
    P("## THE FLOOR — measured on every (panel, ladder, statistic), at all three confidences")
    floorrows, argrows, pairrows = [], [], []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            _, Rw, Ro = series[(panel, lad)]
            for Lb in BLOCKS_L:
                rng = np.random.default_rng(SEED_BOOT + hash((panel, lad, Lb)) % 10_000)
                ixw, nbw = block_index(rng, Rw.shape[1], Lb, BDRAWS)
                ixo, nbo = block_index(rng, Ro.shape[1], Lb, BDRAWS)
                bcw, bsw = boot_exact(Rw, ixw, nbw, Lb)
                _, bso = boot_exact(Ro, ixo, nbo, Lb)
                bdd = boot_maxdd(Rw, ixw)
                boots = {"S_FULL": bsw, "S_OOS": bso, "CAGR": bcw * 100.0, "DD": bdd * 100.0}
                fulls = {"S_FULL": np.array([metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs]),
                         "S_OOS": np.array([metr[(panel, lad, r_)]["OOS_Sharpe"] for r_ in rungs]),
                         "CAGR": np.array([metr[(panel, lad, r_)]["CAGR"] for r_ in rungs]) * 100.0,
                         "DD": np.array([metr[(panel, lad, r_)]["MaxDD"] for r_ in rungs]) * 100.0}
                for stat in STATS:
                    v, b = fulls[stat], boots[stat]
                    order = np.argsort(-v, kind="stable")
                    peak, runner = order[0], order[1]
                    gap = float(v[peak] - v[runner])
                    am = np.nanargmax(b, axis=0)
                    counts = np.bincount(am, minlength=len(rungs)) / b.shape[1]
                    pstab = float(counts[peak])
                    w, tset, mass = mass_set(counts, rungs, 0.90)
                    for q in QGRID:
                        flo, lun, npair, nun, prs = floor_and_pairs(v, b, q)
                        tie = bool(gap < flo)
                        floorrows.append(dict(panel=panel, ladder=lad, stat=stat, L=Lb, q=q,
                                              rungs=len(rungs), peak=rungs[peak],
                                              runner_up=rungs[runner], gap=gap, floor=flo,
                                              largest_unresolved=lun, n_pairs=npair,
                                              n_unresolved=nun, tie_set_verdict=tie,
                                              P_argmax=pstab, tie_set_width=w,
                                              tie_set=str(tset), tie_mass=mass,
                                              spread=float(v.max() - v.min()),
                                              floor_capped=min(flo, float(v.max() - v.min()))))
                        if Lb == L_HEAD and q == 0.90:
                            for (i, j, g_, a_) in prs:
                                pairrows.append(dict(panel=panel, ladder=lad, stat=stat,
                                                     rung_i=rungs[i], rung_j=rungs[j],
                                                     gap=g_, agree=a_, resolved=bool(a_ >= q)))
                    if Lb == L_HEAD:
                        argrows.append(dict(panel=panel, ladder=lad, stat=stat,
                                            peak=rungs[peak], P_argmax=pstab,
                                            mass=str({rungs[k]: round(float(counts[k]), 3)
                                                      for k in range(len(rungs))}),
                                            set90_width=w, set90=str(tset), set90_mass=mass))
    fl = pd.DataFrame(floorrows)
    ar = pd.DataFrame(argrows)
    dump(fl, "floor")
    dump(ar, "argmax")
    dump(pd.DataFrame(pairrows), "pairs")

    head = fl[fl.L == L_HEAD]
    P(f"  headline L={L_HEAD}:")
    for panel in PANELS:
        for lad in LADDERS:
            sub = head[(head.panel == panel) & (head.ladder == lad) & (head.q == 0.90)]
            for _, r_ in sub.iterrows():
                P(f"    {panel:<5} {lad:<8} {r_['stat']:<7} peak {str(r_['peak']):<6} "
                  f"gap {r_['gap']:+8.4f}  floor(0.90) {r_['floor']:8.4f}  "
                  f"{'TIE SET' if r_['tie_set_verdict'] else 'RESOLVED':<9} "
                  f"P(argmax) {r_['P_argmax']:.3f}  90% set {r_['tie_set']}")
    P("  BLOCK LENGTH, reported and never selected on — tie-set share at q=0.90:")
    for Lb in BLOCKS_L:
        s = fl[(fl.L == Lb) & (fl.q == 0.90)]
        P(f"    L={Lb:<4} {int(s['tie_set_verdict'].sum())} of {len(s)} "
          f"({s['tie_set_verdict'].mean():.3f}), median P(argmax) {s['P_argmax'].median():.3f}")
    P("")

    # --------------------------------------------------------------- THE 6 CELLS (both dials)
    P("## THE 6 CELLS — CLAIM SET x FLOOR CONFIDENCE, all published")
    cellrows, claimscored = [], []
    core_head = head[head.L == L_HEAD]
    for q in QGRID:
        sub = core_head[core_head.q == q]
        n_core = len(sub)
        n_tie = int(sub["tie_set_verdict"].sum())
        overall = n_tie / n_core if n_core else np.nan
        rate_fam = sub.groupby(["ladder", "stat"])["tie_set_verdict"].mean().to_dict()
        rate_stat = sub.groupby("stat")["tie_set_verdict"].mean().to_dict()
        wide_n = len(claims)
        wide_tie, basis_n = 0.0, {"MEASURED_FAMILY": 0, "TRANSFERRED_STAT": 0,
                                  "TRANSFERRED_OVERALL": 0}
        for _, c in claims.iterrows():
            k = (c["family"], c["stat"])
            if k in rate_fam:
                rate, basis = float(rate_fam[k]), "MEASURED_FAMILY"
            elif c["stat"] in rate_stat:
                rate, basis = float(rate_stat[c["stat"]]), "TRANSFERRED_STAT"
            else:
                rate, basis = float(overall), "TRANSFERRED_OVERALL"
            wide_tie += rate
            basis_n[basis] += 1
            if q == 0.90:
                claimscored.append(dict(source=c["source"], file=c["file"], line=c["line"],
                                        family=c["family"], value=c["value"], stat=c["stat"],
                                        word=c["word"], rate=rate, basis=basis,
                                        ctx=c["ctx"]))
        cellrows.append(dict(q=q, claimset="CORE", n_claims=n_core, n_tie=float(n_tie),
                             share=overall, basis="MEASURED", measured_family=n_core,
                             transferred_stat=0, transferred_overall=0))
        cellrows.append(dict(q=q, claimset="WIDE", n_claims=wide_n, n_tie=wide_tie,
                             share=wide_tie / wide_n if wide_n else np.nan, basis="MIXED",
                             measured_family=basis_n["MEASURED_FAMILY"],
                             transferred_stat=basis_n["TRANSFERRED_STAT"],
                             transferred_overall=basis_n["TRANSFERRED_OVERALL"]))
        P(f"  q={q:.2f}  CORE {n_tie:2d} of {n_core} become TIE SETS ({overall:.3f})   "
          f"WIDE {wide_tie:.1f} of {wide_n} ({wide_tie / wide_n if wide_n else float('nan'):.3f}) "
          f"[{basis_n['MEASURED_FAMILY']} measured-by-family, {basis_n['TRANSFERRED_STAT']} "
          f"transferred-by-statistic, {basis_n['TRANSFERRED_OVERALL']} transferred-overall]")
    cells = pd.DataFrame(cellrows)
    dump(cells, "cells")
    dump(pd.DataFrame(claimscored), "claimscored")
    ninf = int(np.isinf(core_head[core_head.q == 0.90]["floor"]).sum())
    P(f"  floors that are INFINITE at q=0.90 (nothing on the ladder resolves): {ninf} of "
      f"{len(core_head[core_head.q == 0.90])}")
    P("")

    # ------------------------------------------------ D1/D2, labelled POST-HOC, no hypothesis
    P("## D1 / D2 — post-hoc diagnostics, labelled as such and excluded from every count above")
    q90d = core_head[core_head.q == 0.90].copy()
    edge = []
    for _, r_ in q90d.iterrows():
        rungs = LADDERS[r_["ladder"]]
        edge.append(str(r_["peak"]) in (str(rungs[0]), str(rungs[-1])))
    q90d["peak_is_grid_edge"] = edge
    res = q90d[~q90d["tie_set_verdict"]]
    P(f"  D1 — WHERE AN ARGMAX RESOLVES AT ALL.  {len(res)} of {len(q90d)} CORE objects are")
    P("     RESOLVED at q=0.90.  Of those:")
    for _, r_ in res.iterrows():
        P(f"       {r_['panel']:<5} {r_['ladder']:<8} {r_['stat']:<7} peak {str(r_['peak']):<6} "
          f"grid EDGE {str(bool(r_['peak_is_grid_edge'])):<5}  ladder spread {r_['spread']:.4f}  "
          f"gap {r_['gap']:.4f}")
    P(f"     grid-edge share among RESOLVED {res['peak_is_grid_edge'].mean() if len(res) else float('nan'):.3f}"
      f" vs among TIE SETS "
      f"{q90d[q90d['tie_set_verdict']]['peak_is_grid_edge'].mean():.3f}")
    P(f"     ladders carrying every RESOLVED object: "
      f"{sorted(set(res['ladder']))}; its whole-ladder Sharpe spread is "
      f"{float(q90d[(q90d.ladder == 'GROSS') & (q90d.stat == 'S_FULL')]['spread'].max()):.4f}")
    P("  D2 — WHAT THE CLAUSE ACTUALLY REWRITES (tie-set WIDTH, not just the verdict):")
    tie = q90d[q90d["tie_set_verdict"]]
    wid = tie["tie_set_width"].astype(float)
    P(f"     {int((wid > 1).sum())} of {len(q90d)} CORE objects get a 90% tie set WIDER than one")
    P(f"     rung; mean width {wid.mean():.2f} rungs, median {wid.median():.1f}, max "
      f"{wid.max():.0f}; as a share of their own ladder's rungs, mean "
      f"{float((tie['tie_set_width'] / tie['rungs']).mean()):.3f}.")
    P(f"     WHOLE-LADDER tie sets (the clause leaves the argmax with no content at all): "
      f"{int((tie['tie_set_width'] == tie['rungs']).sum())} of {len(q90d)}")
    dump(q90d, "d1d2")
    P("")

    # ------------------------------------------------------------------------- HYPOTHESES
    P("## HYPOTHESES — declared before any number above was read")
    hyp = []
    q90 = core_head[core_head.q == 0.90]
    share = float(q90["tie_set_verdict"].mean())
    hyp.append(("H_TIE", share > 0.50, f"share of CORE argmaxes below their own floor at "
                                       f"q=0.90 = {share:.3f} ({int(q90['tie_set_verdict'].sum())} of {len(q90)})"))
    rel = q90.assign(rel=q90["floor_capped"] / q90["spread"].replace(0, np.nan))
    dd_rel = float(rel[rel.stat == "DD"]["rel"].median())
    sh_rel = float(rel[rel.stat == "S_FULL"]["rel"].median())
    hyp.append(("H_STAT", dd_rel < sh_rel,
                f"median CAPPED floor/spread DD {dd_rel:.3f} vs S_FULL {sh_rel:.3f} "
                f"(cap = the ladder's own spread where nothing resolves)"))
    ok9 = []
    for panel in PANELS:
        for stat in STATS:
            f9 = q90[(q90.panel == panel) & (q90.ladder == "N") & (q90.stat == stat)]["floor_capped"]
            f4 = q90[(q90.panel == panel) & (q90.ladder == "H") & (q90.stat == stat)]["floor_capped"]
            s9 = q90[(q90.panel == panel) & (q90.ladder == "N") & (q90.stat == stat)]["spread"]
            s4 = q90[(q90.panel == panel) & (q90.ladder == "H") & (q90.stat == stat)]["spread"]
            if len(f9) and len(f4) and min(float(s9.iloc[0]), float(s4.iloc[0])) > 0:
                ok9.append((float(f9.iloc[0]) / float(s9.iloc[0])) >
                           (float(f4.iloc[0]) / float(s4.iloc[0])))
    hyp.append(("H_LADDER", bool(np.mean(ok9) > 0.5) if ok9 else False,
                f"9-rung capped floor/spread > 4-rung's in {int(np.sum(ok9))} of {len(ok9)} "
                f"(panel, stat) pairs"))
    ratios = []
    for lad in LADDERS:
        for stat in STATS:
            a = q90[(q90.panel == "U56") & (q90.ladder == lad) & (q90.stat == stat)]["floor_capped"]
            b = q90[(q90.panel == "B136") & (q90.ladder == lad) & (q90.stat == stat)]["floor_capped"]
            if len(a) and len(b) and np.isfinite(a.iloc[0]) and np.isfinite(b.iloc[0]) and min(a.iloc[0], b.iloc[0]) > 0:
                ratios.append(max(a.iloc[0], b.iloc[0]) / min(a.iloc[0], b.iloc[0]))
    hyp.append(("H_PANEL", bool(np.median(ratios) <= 1.5) if ratios else False,
                f"median cross-panel floor ratio {np.median(ratios) if ratios else float('nan'):.3f} "
                f"over {len(ratios)} (ladder, stat) pairs"))
    pshare = float((q90["P_argmax"] < 0.50).mean())
    hyp.append(("H_P", pshare > 0.50, f"P(argmax reproduces) < 0.50 in {pshare:.3f} of CORE objects "
                                      f"(median P {q90['P_argmax'].median():.3f})"))
    hyp.append(("H_HARVEST", H_HARVEST, f"{len(claims)} valued claims harvested"))
    for k, v, why in hyp:
        P(f"  {k:<11} {'PASS' if v else 'FAIL'}   {why}")
    P(f"  {sum(1 for _, v, _ in hyp if v)} of {len(hyp)} hypotheses PASS")
    dump(pd.DataFrame([dict(hypothesis=k, result="PASS" if v else "FAIL", detail=w)
                       for k, v, w in hyp]), "hypotheses")
    P("")

    # ------------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 — rung chosen on IS 2009-2016 ALONE, per ladder, OOS read ONCE")
    pickrows = []
    for panel in PANELS:
        dd_ = panels[panel]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values, dd_["warm"], dd_["ins"], dd_["oos"])
        lbm_p = blocks_m(
            backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST, freq="W")["returns"].values,
            dd_["warm"], dd_["ins"], dd_["oos"])
        for lad, rungs in LADDERS.items():
            for ch in CHOOSERS:
                key = {"C_ISSHARPE": "IS_Sharpe", "C_ISDD": "IS_MaxDD", "C_ISCAGR": "IS_CAGR"}[ch]
                vals = [metr[(panel, lad, r_)][key] for r_ in rungs]
                pick = rungs[int(np.argmax(vals))]
                mm = metr[(panel, lad, pick)]
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                srt = np.sort(vals)[::-1]
                pickrows.append(dict(panel=panel, ladder=lad, chooser=ch, pick=pick,
                                     margin=float(srt[0] - srt[1]),
                                     OOS_CAGR=mm["OOS_CAGR"], OOS_Sharpe=mm["OOS_Sharpe"],
                                     OOS_MaxDD=mm["OOS_MaxDD"], CAGR=mm["CAGR"],
                                     Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                     pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
    pk = pd.DataFrame(pickrows)
    dump(pk, "picks")
    for panel in PANELS:
        s = pk[pk.panel == panel]
        P(f"  {panel}: 4b full {int(s['pass_4b_full'].sum())} of {len(s)}, 4b OOS "
          f"{int(s['pass_4b_oos'].sum())} of {len(s)}, 4a {int(s['pass_4a'].sum())} of {len(s)}")
    P(f"  ALL PICKS: 4b full {int(pk['pass_4b_full'].sum())} of {len(pk)}, 4b OOS "
      f"{int(pk['pass_4b_oos'].sum())} of {len(pk)}, 4a {int(pk['pass_4a'].sum())} of {len(pk)}")
    P(f"  WHOLE GRID: 4b full {int(grid['pass_4b_full'].sum())} of {len(grid)}, 4b OOS "
      f"{int(grid['pass_4b_oos'].sum())} of {len(grid)}, 4a {int(grid['pass_4a'].sum())} of {len(grid)}")
    if int(grid["pass_4b_oos"].sum()):
        P("  4b-OOS passing cells:")
        for _, r_ in grid[grid.pass_4b_oos].iterrows():
            P(f"    {r_['panel']:<5} {r_['ladder']:<8} rung {str(r_['rung']):<6} "
              f"full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%}  "
              f"OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:.2%}")
    P("")

    dump(pd.DataFrame(gaterows), "gates")
    P(f"# GATES {sum(gates.values())} of {len(gates)} PASS")
    P(f"# elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT}.console.txt")


if __name__ == "__main__":
    main()
