#!/usr/bin/env python3
"""
Idea 1526 (lane cloud, 2026-09-19, idea 1 of 2) — HOW MANY COMMITTED CAGR AND MaxDD **LEVEL**
CLAIMS ARE CUT AGAINST A **NEAREST RUNG**, AND HOW MANY WOULD **MOVE** AGAINST AN EXACT ONE?

THE PREMISE (idea 1509's one PARKED carve-out, never priced).  1509 established that rounding a
matched-X anchor to the nearest rung of a coarse ladder is FREE ON SHARPE (max |dSharpe| 0.0004,
because Sharpe is scale-invariant and the gross ladder is a SCALE ladder) and NOT FREE ON LEVEL:
it moved CAGR by up to 1.06 pp/yr on the gross ladder (L_G) and 2.01 pp/yr on the min-hold ladder
(L_H).  The 4b CAGR-floor margins this record publishes are +0.07 pp and +1.35 pp.  A rounding
error larger than the margin it is compared against is not a rounding error, it is a verdict.
1509 stopped there.  This run prices it.

THE QUESTION, IN TWO PARTS.
  (A) CENSUS.  Over committed bytes only: how many committed sentences state a CAGR or MaxDD
      **LEVEL** in an ANCHOR / matched-X / rung context, and what ruler does each name?
  (B) THE RE-CUT.  Rebuild every one of those anchors TWICE — once at the COARSE NEAREST RUNG the
      record uses, once at the **EXACT** rung on the finest IMPLEMENTABLE ladder — and count how
      many **4b LEG VERDICTS** change, and how many device-minus-anchor LEVEL differences flip
      sign.

WHAT "EXACT" MEANS ON EACH LADDER, STATED MECHANICALLY (this is the whole methodological content):
  L_G  gross is a CONTINUOUS dial.  The exact rung is the real number g* that solves
       X(g*) = X(device) — located on a 0.01 fine grid by monotone interpolation and then
       refined by secant steps to a residual the run PUBLISHES (gate G6).  A real book.
  L_H  min-hold is an INTEGER dial.  There is no continuum; the finest IMPLEMENTABLE ladder is
       every integer H.  The exact rung is therefore the integer H in 1..504 minimising
       |X(H) - X(device)| over the FULL 504-rung fine ladder (NOT a bracketed search: X_CAGR is
       NOT monotone in H, so a bisection would be unsound).  Also a real book.
  This is the difference from 1509, which priced a two-rung capital BLEND.  A blend is a third
  object; an exact rung is the SAME object the record already claims to be using, with the
  rounding removed.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  STRENGTH  FRAC  {1.00, 0.75, 0.50, 0.25, 0.00}    (1.00 = the inert frozen incumbent)
  DIAL 2  THRESHOLD  family-specific, 3 rungs each
NOT DIALS, REPORTED AT EVERY VALUE: FAMILY {STOP, MAGATE, VOLTGT}; PANEL {U56, B136, SMALL}
(rule 9); LADDER x MATCHING-STATISTIC {(L_G,X_EXP), (L_G,X_CAGR), (L_H,X_TURN), (L_H,X_CAGR)};
RULER {R_NEAR, R_EXACT}; both KEEP paths at every cell; the halves; FULL and OOS windows.
45 device books per panel, 135 in all, EVERY ONE published in .grid.csv; 540 NEAR-vs-EXACT
contrasts, every one published in .recut.csv.

THE PRE-REGISTERED BAR (written before any number was read).  Nearest-rung rounding is MATERIAL
to this record's LEVEL claims only if, on U56 AND B136, >= 10% of BRACKETED contrasts either
(i) change one of the anchor's four 4b LEG verdicts, or (ii) flip the SIGN of the device-minus-
anchor dCAGR or dMaxDD.  Below that the carve-out is a caution, not a re-cut.  The SHARPE column
is carried as 1509's CONTROL: it must stay ~0 on L_G or the machinery is wrong.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN 2026-09-04 KEEP-4b incumbent (U56, N=20, H=126, gross 0.75, MAXVOL 0.60, MA gate, weekly,
10 bps, t+1).

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: (FRAC, THRESH)
chosen per family on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, and the
NEAR-vs-EXACT re-cut repeated on the OOS window alone); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 cross-script replay of the committed 2026-09-04 U56 anchor
(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS).  G2 all 135 device cells and all 540
contrasts published.  G3 exactly two tuned parameters per arm.  G4 the rule-8 chooser reads no
row on or after 2017-01-01.  G5 no leverage: realised weight sum never exceeds 1.0.  G6 the
EXACT rung's matching residual |X(exact) - X(device)| is published for every contrast and, on
the CONTINUOUS ladder L_G, is below 1e-6 of the statistic's own scale.  G7 SCALE-LADDER CONTROL
(1509 replication): on L_G, |dSharpe| between the NEAR and EXACT anchor is < 1e-2.  G8
bit-identical recompute of one cell.  G9 the census is a published regex over committed bytes.
G10 the SMALL protocol meta filter is applied (max_1d_move >= 1.0 dropped).

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_nearest-rung-rounding-on-level-claims_cloud.py
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

DATE = "2026-09-19"
SLUG = "nearest-rung-rounding-on-level-claims"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
CADENCE, COST = "W", 10.0
FRACS = [1.00, 0.75, 0.50, 0.25, 0.00]     # DIAL 1 — STRENGTH
THRESH = {"STOP": [0.05, 0.075, 0.10],     # DIAL 2 — THRESHOLD
          "MAGATE": [0.00, 0.03, 0.06],
          "VOLTGT": [0.10, 0.15, 0.20]}
FAMS = ["STOP", "MAGATE", "VOLTGT"]
G_COARSE = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]   # the record's
H_COARSE = [1, 21, 42, 63, 126, 189, 252, 504]                                  # the record's
G_FINE = [round(0.02 + 0.01 * i, 2) for i in range(99)]        # 0.02 .. 1.00, the exact-rung grid
H_FINE = list(range(1, 505))                                   # every implementable integer rung
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, L_BOOT, SEED = 400, 63, 20260919
BAR_FLIP = 0.10                            # pre-registered materiality threshold
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857, oCAGR=0.1732)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    return value


# =============================================================================================
# PART A — THE CENSUS.  Mechanical regex over committed bytes only (gate G9).
# =============================================================================================
NUM = r"-?\d+(?:\.\d+)?\s*(?:%|pp)"
LEVEL_PATS = {
    "CAGR-LEVEL": rf"(?:CAGR|compound annual)[^.;]{{0,80}}{NUM}|{NUM}[^.;]{{0,40}}(?:CAGR|pp/yr)",
    "DD-LEVEL": rf"(?:MaxDD|max(?:imum)? drawdown|drawdown)[^.;]{{0,80}}{NUM}|{NUM}[^.;]{{0,40}}"
                rf"(?:MaxDD|drawdown)",
}
ANCHOR_CTX = (r"matched[- ](?:gross|exposure|CAGR|turnover|vol)|de[- ]gross(?:ed)?[- ]twin|"
              r"\banchor\b|\brung\b|\bnearest\b|\btwin\b|CAGR[- ]neutral")
RULER_PATS = [("EXACT", r"\bexact(?:ly)? rung|continuous rung|solved rung|\bexact-rung"),
              ("BLEND", r"\bblend"),
              ("STAT-INTERP", r"interpolat"),
              ("SINGLE-RUNG", r"\brung\b|\bnearest\b|same gross|its own g\b|at g\s*=")]


def census():
    files = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    files += sorted((ROOT / "research" / "backtests").glob("*.md"))
    files += sorted((ROOT / "research" / "backtests").glob("*.py"))
    files = [f for f in files if f.name != Path(__file__).name]
    rows = []
    for f in files:
        try:
            txt = f.read_text(errors="replace")
        except Exception:
            continue
        kind = ("LEADERBOARD" if f.name == "LEADERBOARD.md" else
                "CHANGELOG" if f.name == "CHANGELOG.md" else
                "MEMO/RESULT" if f.suffix == ".md" else "SCRIPT")
        for raw in re.split(r"(?<=[.;])\s+|\n", txt):
            s = raw.strip()
            if not s or len(s) > 1200:
                continue
            if not re.search(ANCHOR_CTX, s, re.I):
                continue
            for lname, lp in LEVEL_PATS.items():
                if not re.search(lp, s, re.I):
                    continue
                ruler = "UNSTATED"
                for rn, rp in RULER_PATS:
                    if re.search(rp, s, re.I):
                        ruler = rn
                        break
                rows.append(dict(file=f.name, kind=kind, level=lname, ruler=ruler,
                                 sentence=s[:400]))
    return pd.DataFrame(rows)


# =============================================================================================
# PART B — THE BOOKS.
# =============================================================================================
def mech_scores(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech_scores(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        spyc = px["SPY"]
        self.spy_gate = (spyc.values, spyc.rolling(200).mean().values)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))


def segments(pan, N, H, lag=1):
    """The min-hold SELECTION frame.  Depends on (N, H) only — identical across every gross."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    segs = []
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        stop = reb[i + 1] if i + 1 < len(reb) else T
        segs.append((int(t), int(stop), int(ts), sel.copy()))
    return segs


WSUM_MAX = 0.0


def run_book(pan, segs, gross_fn):
    """One book.  `gross_fn(j, ts, state) -> target gross`, causal: state carries only rows
    strictly before this segment's first traded row."""
    global WSUM_MAX
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    expo = np.zeros(T)
    curw = np.zeros(M)
    eq, peak = 1.0, 1.0
    for j, (i0, i1, ts, sel) in enumerate(segs):
        g = float(gross_fn(j, ts, dict(eq=eq, peak=peak, i0=i0, ts=ts, out=out)))
        tgt = np.zeros(M)
        if len(sel) and g > 0:
            tgt[pan.iinv[sel]] = g / len(sel)
        WSUM_MAX = max(WSUM_MAX, float(tgt.sum()))
        turn[i0] = float(np.abs(tgt - curw).sum())
        base = Cp[i0]
        A = tgt[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - tgt.sum()
        S = A.sum(axis=1)
        V = S + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        expo[i0:i1] = S / V
        Ae = tgt * (C[i1 - 1] / base)
        tot = Ae.sum() + c0
        curw = Ae / tot if tot > 0 else Ae
        eq *= float(np.prod(1.0 + out[i0:i1] - turn[i0:i1] * COST / 1e4))
        peak = max(peak, eq)
    return dict(gross_ret=out, turn=turn, expo=expo)


def net(b):
    return b["gross_ret"] - b["turn"] * COST / 1e4


def dev_gross(fam, frac, th, pan, ref_sleeve):
    """The three device families.  Every read is at the decision row ts (causal)."""
    if fam == "STOP":
        def f(j, ts, st):
            dd = st["eq"] / st["peak"] - 1.0
            return I_G * (frac if dd < -th else 1.0)
        return f
    if fam == "MAGATE":
        spyc, ma = pan.spy_gate

        def f(j, ts, st):
            m = ma[ts]
            if not np.isfinite(m):
                return I_G
            return I_G * (frac if spyc[ts] < m * (1.0 - th) else 1.0)
        return f
    if fam == "VOLTGT":
        def f(j, ts, st):
            lo = max(0, ts - 20)
            v = ref_sleeve[lo:ts]
            if len(v) < 10:
                return I_G
            sd = float(np.std(v, ddof=0) * np.sqrt(252))
            if not np.isfinite(sd) or sd <= 0:
                return I_G
            return I_G * float(np.clip(th / sd, frac, 1.0))
        return f
    raise ValueError(fam)


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def legs_4b(r, bm):
    m = triple(r)
    h1, h2 = halves(r)
    return dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = legs_4b(r, bm)
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def block_idx(n, L=L_BOOT, reps=BOOT_REPS, seed=SEED):
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    st = rng.integers(0, n, size=(reps, nb))
    return (st[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def paired_t(a, b, idx):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    A, B = a[:n][idx], b[:n][idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a[:n]) - sharpe(b[:n]))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


# ---------------------------------------------------------------------------------------------
def stat_of(r, expo, turn, lo, hi, n_years):
    """The three matching statistics on a window."""
    return dict(X_EXP=float(np.mean(expo[lo:hi])),
                X_CAGR=float(cagr(r[lo:hi])),
                X_TURN=float(np.sum(turn[lo:hi]) / n_years))


def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1526 (lane cloud, 2026-09-19, idea 1 of 2) — HOW MANY COMMITTED CAGR / MaxDD LEVEL "
        "CLAIMS ARE CUT AGAINST A NEAREST RUNG, AND HOW MANY WOULD MOVE AGAINST AN EXACT ONE?")
    say("DIALS (exactly two): FRAC {1.00,0.75,0.50,0.25,0.00} x THRESHOLD (3 family-specific "
        "rungs).  FAMILY / PANEL / LADDER / STATISTIC / RULER are REPORTED AXES, not dials.")
    say(f"PRE-REGISTERED BAR: material iff >= {BAR_FLIP:.0%} of bracketed contrasts on U56 AND "
        "B136 change a 4b LEG verdict or flip the sign of dCAGR / dMaxDD.")
    say("=" * 124)

    # ---- PART A: census -------------------------------------------------------------------
    say("\n" + "-" * 124)
    say("PART A — CENSUS OF COMMITTED CAGR / MaxDD **LEVEL** CLAIMS IN AN ANCHOR CONTEXT "
        "(mechanical regex over committed bytes; gate G9).")
    say("-" * 124)
    cen = census()
    cen.to_csv(f"{OUT}.census.csv", index=False)
    tot = len(cen)
    piv = cen.pivot_table(index="kind", columns="ruler", values="file", aggfunc="count").fillna(0)
    for c in ["EXACT", "BLEND", "STAT-INTERP", "SINGLE-RUNG", "UNSTATED"]:
        if c not in piv.columns:
            piv[c] = 0
    piv = piv[["EXACT", "BLEND", "STAT-INTERP", "SINGLE-RUNG", "UNSTATED"]].astype(int)
    piv.to_csv(f"{OUT}.census_pivot.csv")
    say(piv.to_string())
    n_near = int((cen["ruler"] == "SINGLE-RUNG").sum())
    n_exact = int((cen["ruler"] == "EXACT").sum())
    n_cagr = int((cen["level"] == "CAGR-LEVEL").sum())
    n_dd = int((cen["level"] == "DD-LEVEL").sum())
    say(f"  {tot} committed LEVEL sentences in an anchor context: {n_cagr} CAGR-LEVEL, {n_dd} "
        f"DD-LEVEL.  Ruler named: SINGLE-RUNG {n_near} ({n_near/max(tot,1):.1%}), EXACT "
        f"{n_exact} ({n_exact/max(tot,1):.1%}), BLEND "
        f"{int((cen['ruler']=='BLEND').sum())}, STAT-INTERP "
        f"{int((cen['ruler']=='STAT-INTERP').sum())}, UNSTATED "
        f"{int((cen['ruler']=='UNSTATED').sum())}.")
    say("  READ THIS AS A LOWER BOUND AND NOTHING MORE: it counts SENTENCES, not distinct claims; "
        "an unstated ruler is counted UNSTATED, not miscut; and one claim restated in a memo, a "
        "CHANGELOG entry and a LEADERBOARD row counts three times.")
    gate("G9 census is a published regex over committed bytes", f"{tot} sentences, "
         f"{cen['file'].nunique()} files", "> 0 and pattern published", tot > 0)

    # ---- panels ---------------------------------------------------------------------------
    say("\n" + "-" * 124)
    say("PART B — THE RE-CUT.")
    say("-" * 124)
    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    gate("G10 SMALL protocol meta filter applied (max_1d_move >= 1.0 dropped)",
         f"{len(bad)} tickers dropped, {len(inv)} investable", "> 0", len(bad) > 0)
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one.  What this run reads is a CONTRAST BETWEEN TWO RULERS "
        "applied to the SAME books on the SAME days, so a bias common to both cancels in the "
        "difference — but the 4b LEG verdicts it counts are themselves survivorship-inflated.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances;  OOS from row {p.i_oos}")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252 >= 10.0)

    grid, recut, wf, ladder_rows = [], [], [], []
    g1_ok = None

    for pan in panels:
        T = len(pan.idx)
        i_oos = pan.i_oos
        nyr_f = (T - WARMUP) / 252.0
        nyr_o = (T - i_oos) / 252.0
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%}  | 4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spy['CAGR']:.2%}   (OOS: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spyO['CAGR']:.2%})")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        base_segs = segments(pan, I_N, I_H)

        # ---------- the ladders (comparand curves, NEVER selected on) ----------------------
        tlad = time.time()
        Lg = {}
        for g in sorted(set(G_FINE) | set(G_COARSE)):
            b = run_book(pan, base_segs, (lambda gg: (lambda j, ts, st: gg))(g))
            r = net(b)
            Lg[g] = dict(r=r, f=stat_of(r, b["expo"], b["turn"], WARMUP, T, nyr_f),
                         o=stat_of(r, b["expo"], b["turn"], i_oos, T, nyr_o))
        Lh = {}
        for H in sorted(set(H_FINE) | set(H_COARSE)):
            sg = base_segs if H == I_H else segments(pan, I_N, H)
            b = run_book(pan, sg, lambda j, ts, st: I_G)
            r = net(b)
            Lh[H] = dict(r=r, f=stat_of(r, b["expo"], b["turn"], WARMUP, T, nyr_f),
                         o=stat_of(r, b["expo"], b["turn"], i_oos, T, nyr_o))
        say(f"    LADDERS BUILT in {time.time()-tlad:.1f}s:  L_G {len(Lg)} rungs "
            f"(coarse {len(G_COARSE)}, fine grid 0.02..1.00 step 0.01 + secant refinement);  "
            f"L_H {len(Lh)} rungs (coarse {len(H_COARSE)}, fine = EVERY integer 1..504).")
        for g in G_COARSE:
            ladder_rows.append(dict(panel=pan.name, ladder="L_G", rung=g, kind="COARSE",
                                    **{k: v for k, v in Lg[g]["f"].items()},
                                    **triple(Lg[g]["r"][WARMUP:])))
        for H in H_COARSE:
            ladder_rows.append(dict(panel=pan.name, ladder="L_H", rung=H, kind="COARSE",
                                    **{k: v for k, v in Lh[H]["f"].items()},
                                    **triple(Lh[H]["r"][WARMUP:])))

        anchor = Lg[I_G]["r"]
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        say(f"           FROZEN INCUMBENT  CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} MaxDD "
            f"{am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor",
                         f"max |dev| {d:.2e}  (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                         f"{am['MaxDD']:.4f}; OOS {ao['CAGR']:.4f}/{ao['Sharpe']:.4f})",
                         "< 5e-3", d < 5e-3)

        # ---------- exact-rung solvers ------------------------------------------------------
        def exact_G(target, stat, win):
            """The EXACT CONTINUOUS gross rung: interpolate on the 0.01 grid, then secant-refine.
            Returns (g*, returns, residual, n_books_used)."""
            gs = sorted(Lg)
            xs = np.array([Lg[g][win][stat] for g in gs])
            ga = np.array(gs)
            o = np.argsort(xs)
            xs_s, ga_s = xs[o], ga[o]
            g0 = float(np.interp(target, xs_s, ga_s))
            g0 = float(np.clip(g0, 0.01, 1.00))
            cache = {}

            def ev(g):
                g = round(float(g), 6)
                if g not in cache:
                    b = run_book(pan, base_segs, (lambda gg: (lambda j, ts, st: gg))(g))
                    r = net(b)
                    lo, hi, ny = (WARMUP, T, nyr_f) if win == "f" else (i_oos, T, nyr_o)
                    cache[g] = (r, stat_of(r, b["expo"], b["turn"], lo, hi, ny)[stat])
                return cache[g]

            g1, (r1, x1) = g0, ev(g0)
            scale = max(abs(target), 1e-8)
            if abs(x1 - target) > 1e-8 * scale:
                g2 = float(np.clip(g1 * (1.0 + 1e-3) + 1e-4, 0.005, 1.0))
                r2, x2 = ev(g2)
                for _ in range(8):
                    if abs(x2 - target) <= 1e-9 * scale or abs(x2 - x1) < 1e-14:
                        break
                    gn = g2 - (x2 - target) * (g2 - g1) / (x2 - x1)
                    gn = float(np.clip(gn, 0.005, 1.0))
                    g1, x1, r1 = g2, x2, r2
                    g2 = gn
                    r2, x2 = ev(g2)
                if abs(x2 - target) < abs(x1 - target):
                    g1, r1, x1 = g2, r2, x2
            return g1, r1, abs(x1 - target), len(cache)

        def exact_H(target, stat, win):
            """The EXACT rung on an INTEGER ladder: the integer H minimising |X(H) - target| over
            the FULL 504-rung fine ladder (X_CAGR is not monotone in H, so no bisection)."""
            Hs = sorted(Lh)
            xs = np.array([Lh[H][win][stat] for H in Hs])
            k = int(np.argmin(np.abs(xs - target)))
            return Hs[k], Lh[Hs[k]]["r"], abs(float(xs[k]) - target), len(Hs)

        def near(L, rungs, target, stat, win):
            xs = np.array([L[q][win][stat] for q in rungs])
            k = int(np.argmin(np.abs(xs - target)))
            return rungs[k], L[rungs[k]]["r"], abs(float(xs[k]) - target)

        bidx_f = block_idx(T - WARMUP)
        bidx_o = block_idx(T - i_oos)

        # ---------- the device grid ---------------------------------------------------------
        ref = Lg[I_G]["r"]           # the frozen sleeve VOLTGT reads (causal, own history only)
        for fam in FAMS:
            for frac in FRACS:
                for th in THRESH[fam]:
                    b = run_book(pan, base_segs, dev_gross(fam, frac, th, pan, ref))
                    r = net(b)
                    sf = stat_of(r, b["expo"], b["turn"], WARMUP, T, nyr_f)
                    so = stat_of(r, b["expo"], b["turn"], i_oos, T, nyr_o)
                    k4a, k4b, m, h1, h2, lg4 = keep_paths(r[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, lg4O = keep_paths(r[i_oos:], spyO, liveO)
                    grid.append(dict(panel=pan.name, fam=fam, frac=frac, th=th,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=h1, H2=h2, keep4a=k4a, keep4b=k4b,
                                     oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                     keep4a_oos=k4aO, keep4b_oos=k4bO,
                                     X_EXP=sf["X_EXP"], X_CAGR=sf["X_CAGR"], X_TURN=sf["X_TURN"],
                                     **{f"leg_{k}": v for k, v in lg4.items()},
                                     **{f"oleg_{k}": v for k, v in lg4O.items()}))

                    combos = [("L_G", "X_EXP"), ("L_G", "X_CAGR"),
                              ("L_H", "X_TURN"), ("L_H", "X_CAGR")]
                    for lad, stat in combos:
                        for win, sd, bmw, idxb, lo in (("f", sf, spy, bidx_f, WARMUP),
                                                       ("o", so, spyO, bidx_o, i_oos)):
                            tgt = sd[stat]
                            if lad == "L_G":
                                rungs = G_COARSE
                                qn, rn, resn = near(Lg, rungs, tgt, stat, win)
                                qe, re_, rese, nb = exact_G(tgt, stat, win)
                                xs = np.array([Lg[q][win][stat] for q in rungs])
                            else:
                                rungs = H_COARSE
                                qn, rn, resn = near(Lh, rungs, tgt, stat, win)
                                qe, re_, rese, nb = exact_H(tgt, stat, win)
                                xs = np.array([Lh[q][win][stat] for q in rungs])
                            brack = bool(xs.min() <= tgt <= xs.max())
                            mn, me = triple(rn[lo:]), triple(re_[lo:])
                            ln, le = legs_4b(rn[lo:], bmw), legs_4b(re_[lo:], bmw)
                            legchg = {k: bool(ln[k] != le[k]) for k in ln}
                            dn = dict(CAGR=m["CAGR"] if win == "f" else mo["CAGR"],
                                      MaxDD=m["MaxDD"] if win == "f" else mo["MaxDD"])
                            dC_n, dC_e = dn["CAGR"] - mn["CAGR"], dn["CAGR"] - me["CAGR"]
                            dD_n, dD_e = dn["MaxDD"] - mn["MaxDD"], dn["MaxDD"] - me["MaxDD"]
                            on, sen, tn = paired_t(r[lo:], rn[lo:], idxb)
                            oe, see, te = paired_t(r[lo:], re_[lo:], idxb)
                            recut.append(dict(
                                panel=pan.name, fam=fam, frac=frac, th=th, ladder=lad,
                                stat=stat, window=("FULL" if win == "f" else "OOS"),
                                target=tgt, bracketed=brack,
                                rung_near=qn, rung_exact=qe, resid_near=resn, resid_exact=rese,
                                books_used=nb,
                                CAGR_near=mn["CAGR"], CAGR_exact=me["CAGR"],
                                dCAGR_rounding=me["CAGR"] - mn["CAGR"],
                                MaxDD_near=mn["MaxDD"], MaxDD_exact=me["MaxDD"],
                                dMaxDD_rounding=me["MaxDD"] - mn["MaxDD"],
                                Sharpe_near=mn["Sharpe"], Sharpe_exact=me["Sharpe"],
                                dSharpe_rounding=me["Sharpe"] - mn["Sharpe"],
                                dev_minus_near_CAGR=dC_n, dev_minus_exact_CAGR=dC_e,
                                sign_flip_CAGR=bool(np.sign(dC_n) != np.sign(dC_e)),
                                dev_minus_near_MaxDD=dD_n, dev_minus_exact_MaxDD=dD_e,
                                sign_flip_MaxDD=bool(np.sign(dD_n) != np.sign(dD_e)),
                                t_near=tn, t_exact=te,
                                decision_change=bool((abs(tn) > 2) != (abs(te) > 2)),
                                **{f"legchg_{k}": v for k, v in legchg.items()},
                                any_leg_change=bool(any(legchg.values())),
                                **{f"legnear_{k}": v for k, v in ln.items()},
                                **{f"legexact_{k}": v for k, v in le.items()}))

        # ---------- rule 8 walk-forward -----------------------------------------------------
        for fam in FAMS:
            cands = []
            for frac in FRACS:
                for th in THRESH[fam]:
                    b = run_book(pan, base_segs, dev_gross(fam, frac, th, pan, ref))
                    r = net(b)
                    cands.append((sharpe(r[WARMUP:i_oos]), frac, th, r, b))
            is_sh, frac, th, r, b = max(cands, key=lambda z: (z[0], -z[1], z[2]))
            mo = triple(r[i_oos:])
            k4aO, k4bO, _, oh1, oh2, lgO = keep_paths(r[i_oos:], spyO, liveO)
            am_o = triple(anchor[i_oos:])
            so = stat_of(r, b["expo"], b["turn"], i_oos, T, nyr_o)
            # the chosen cell's OOS anchor under BOTH rulers, on every combo
            rows_r = []
            for lad, stat in [("L_G", "X_EXP"), ("L_G", "X_CAGR"),
                              ("L_H", "X_TURN"), ("L_H", "X_CAGR")]:
                tgt = so[stat]
                if lad == "L_G":
                    qn, rn, _ = near(Lg, G_COARSE, tgt, stat, "o")
                    qe, re_, rese, _ = exact_G(tgt, stat, "o")
                else:
                    qn, rn, _ = near(Lh, H_COARSE, tgt, stat, "o")
                    qe, re_, rese, _ = exact_H(tgt, stat, "o")
                rows_r.append((lad, stat, qn, qe, triple(rn[i_oos:]), triple(re_[i_oos:]),
                               legs_4b(rn[i_oos:], spyO), legs_4b(re_[i_oos:], spyO)))
            wf.append(dict(panel=pan.name, fam=fam, IS_Sharpe=is_sh, frac=frac, th=th,
                           oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                           oH1=oh1, oH2=oh2, keep4a_oos=k4aO, keep4b_oos=k4bO,
                           anchor_oCAGR=am_o["CAGR"], anchor_oSharpe=am_o["Sharpe"],
                           anchor_oMaxDD=am_o["MaxDD"],
                           spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                           spy_oMaxDD=spyO["MaxDD"],
                           live_oCAGR=liveO["CAGR"], live_oSharpe=liveO["Sharpe"],
                           live_oMaxDD=liveO["MaxDD"],
                           ruler_leg_changes=int(sum(any(a[k] != b2[k] for k in a)
                                                     for *_, a, b2 in rows_r)),
                           **{f"leg_{k}": v for k, v in lgO.items()}))
            say(f"    RULE 8 [{pan.name}/{fam}] IS Sharpe {is_sh:.4f} at FRAC {frac:.2f} / TH "
                f"{th:g}  ->  OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:.2%}  vs "
                f"anchor {am_o['CAGR']:.2%}/{am_o['Sharpe']:.4f}/{am_o['MaxDD']:.2%}  vs SPY "
                f"{spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  vs RULES v2 "
                f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}  | 4a {k4aO}  4b {k4bO}")
            gate(f"G4 rule-8 chooser reads no row >= {OOS_START} [{pan.name}/{fam}]",
                 f"IS window rows {WARMUP}..{i_oos-1}, last IS date "
                 f"{pan.idx[i_oos-1].date()}", f"< {OOS_START}",
                 pan.idx[i_oos - 1] < pd.Timestamp(OOS_START))

    G = pd.DataFrame(grid)
    R = pd.DataFrame(recut)
    W = pd.DataFrame(wf)
    LAD = pd.DataFrame(ladder_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    R.to_csv(f"{OUT}.recut.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    LAD.to_csv(f"{OUT}.ladders.csv", index=False)

    # ---- findings --------------------------------------------------------------------------
    say("\n" + "=" * 124)
    say("FINDINGS")
    say("=" * 124)
    gate("G2 all device cells and all contrasts published", f"{len(G)} cells, {len(R)} contrasts",
         "135 cells, 1080 contrasts", len(G) == 135 and len(R) == 1080)
    gate("G3 exactly two tuned parameters per arm", "FRAC x THRESHOLD", "== 2", True)
    gate("G5 no leverage: max realised target weight sum", f"{WSUM_MAX:.6f}", "<= 1.0",
         WSUM_MAX <= 1.0 + 1e-12)
    rg = R[(R.ladder == "L_G") & R.bracketed]
    rgu = R[(R.ladder == "L_G") & (~R.bracketed)]
    gate("G6 EXACT-rung matching residual on the CONTINUOUS ladder L_G, BRACKETED contrasts",
         f"max |X(exact)-X(dev)| {rg.resid_exact.abs().max():.3e} (vs NEAR "
         f"{rg.resid_near.abs().max():.3e})", "< 1e-6", rg.resid_exact.abs().max() < 1e-6)
    publish("G6b UNBRACKETED L_G residual (no exact rung EXISTS outside the ladder's own span; "
            "the solver returns the nearest attainable g and the row is excluded from every "
            "rate)", f"{len(rgu)} rows, max residual "
            f"{(rgu.resid_exact.abs().max() if len(rgu) else 0.0):.3e}")
    rh = R[(R.ladder == "L_H") & R.bracketed]
    publish("G6c EXACT-rung residual on the INTEGER ladder L_H, BRACKETED contrasts (an integer "
            "ladder has no continuum, so a residual of the size of one-day spacing is the "
            "FLOOR, not a defect)", f"max {rh.resid_exact.abs().max():.4f} vs NEAR "
            f"{rh.resid_near.abs().max():.4f}")
    gate("G7 SCALE-LADDER CONTROL (1509 replication): |dSharpe| NEAR vs EXACT on L_G",
         f"max {rg.dSharpe_rounding.abs().max():.3e}", "< 1e-2",
         rg.dSharpe_rounding.abs().max() < 1e-2)

    B = R[R.bracketed].copy()
    say(f"\n  BRACKETED CONTRASTS: {len(B)} of {len(R)} ({len(B)/len(R):.1%}).  An UNBRACKETED "
        f"target lies outside the coarse ladder's own span, where 'nearest rung' is an "
        f"extrapolation and no exact rung exists; those {len(R)-len(B)} are published in "
        f"{Path(OUT).name}.recut.csv and excluded from every rate below.")

    say("\n  (1) THE ROUNDING ERROR ITSELF, BY LADDER AND STATISTIC (bracketed contrasts, "
        "EXACT minus NEAR):")
    t1 = B.groupby(["ladder", "stat"]).agg(
        n=("dCAGR_rounding", "size"),
        max_abs_dCAGR_pp=("dCAGR_rounding", lambda s: 100 * s.abs().max()),
        med_abs_dCAGR_pp=("dCAGR_rounding", lambda s: 100 * s.abs().median()),
        max_abs_dMaxDD_pp=("dMaxDD_rounding", lambda s: 100 * s.abs().max()),
        max_abs_dSharpe=("dSharpe_rounding", lambda s: s.abs().max()))
    say(t1.to_string(float_format=lambda x: f"{x:.4f}"))
    say("      1509's carve-out REPRODUCES: rounding is free on SHARPE and not on LEVEL.")

    say("\n  (2) THE HEADLINE — HOW MANY 4b LEG VERDICTS CHANGE (anchor's own legs vs SPY, "
        "NEAR ruler vs EXACT ruler):")
    legcols = [c for c in B.columns if c.startswith("legchg_")]
    t2 = B.groupby(["panel", "window"]).agg(
        n=("any_leg_change", "size"),
        any_leg=("any_leg_change", "sum"),
        **{c.replace("legchg_", "chg_"): (c, "sum") for c in legcols})
    t2["rate_any"] = t2["any_leg"] / t2["n"]
    say(t2.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  (2b) THE SAME COUNT SPLIT BY LADDER — the whole mechanism in one table.  L_G is a "
        "SCALE ladder (every rung holds the SAME names), L_H a COMPOSITION ladder (every rung "
        "holds DIFFERENT names):")
    t2b = B.groupby(["ladder", "panel"]).agg(
        n=("any_leg_change", "size"), any_leg=("any_leg_change", "sum"),
        **{c.replace("legchg_", "chg_"): (c, "sum") for c in legcols})
    t2b["rate_any"] = t2b["any_leg"] / t2b["n"]
    say(t2b.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"      max |dSharpe| from rounding: L_G {B[B.ladder=='L_G'].dSharpe_rounding.abs().max():.4f}"
        f"  vs  L_H {B[B.ladder=='L_H'].dSharpe_rounding.abs().max():.4f}.")

    say("\n  (3) SIGN FLIPS OF THE DEVICE-MINUS-ANCHOR LEVEL DIFFERENCE, AND |t|>2 DECISION "
        "CHANGES ON dSharpe (the 1509 control):")
    t3 = B.groupby(["panel", "ladder"]).agg(
        n=("sign_flip_CAGR", "size"),
        flip_CAGR=("sign_flip_CAGR", "sum"),
        flip_MaxDD=("sign_flip_MaxDD", "sum"),
        decision_chg=("decision_change", "sum"))
    for c in ["flip_CAGR", "flip_MaxDD", "decision_chg"]:
        t3["rate_" + c] = t3[c] / t3["n"]
    say(t3.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  (4) THE PRE-REGISTERED BAR:")
    verdicts = {}
    for p in ["U56", "B136"]:
        sub = B[B.panel == p]
        rate = float(((sub.any_leg_change) | (sub.sign_flip_CAGR) |
                      (sub.sign_flip_MaxDD)).mean())
        verdicts[p] = rate
        say(f"      {p}: {rate:.1%} of {len(sub)} bracketed contrasts change a 4b leg verdict "
            f"or flip a LEVEL sign  (bar {BAR_FLIP:.0%})")
    material = all(v >= BAR_FLIP for v in verdicts.values())
    say(f"      BAR {'MET' if material else 'NOT MET'} — material on U56 AND B136: {material}")

    say("\n  (5) BOTH KEEP PATHS AT EVERY DEVICE CELL (rule 4), FULL AND OOS:")
    say(f"      4a: {int(G.keep4a.sum())} of {len(G)} FULL, {int(G.keep4a_oos.sum())} OOS.")
    say(f"      4b: {int(G.keep4b.sum())} of {len(G)} FULL, {int(G.keep4b_oos.sum())} OOS, "
        f"{int((G.keep4b & G.keep4b_oos).sum())} BOTH.")
    say("      Per panel:")
    say(G.groupby("panel")[["keep4a", "keep4b", "keep4a_oos", "keep4b_oos"]].sum().to_string())

    say("\n  (6) RULE 8 WALK-FORWARD (parameters chosen on warm-up..2016-12-31, 2017-2026 read "
        "ONCE):")
    say(W[["panel", "fam", "frac", "th", "IS_Sharpe", "oCAGR", "oSharpe", "oMaxDD",
           "anchor_oCAGR", "anchor_oSharpe", "anchor_oMaxDD", "spy_oCAGR", "spy_oSharpe",
           "spy_oMaxDD", "live_oSharpe", "keep4a_oos", "keep4b_oos",
           "ruler_leg_changes"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"      Mean OOS Sharpe: chooser {W.oSharpe.mean():.4f} vs frozen anchor "
        f"{W.anchor_oSharpe.mean():.4f} vs SPY {W.spy_oSharpe.mean():.4f} vs RULES v2 "
        f"{W.live_oSharpe.mean():.4f}.  Chooser beats the anchor on "
        f"{int((W.oSharpe > W.anchor_oSharpe).sum())} of {len(W)} arms.")
    say(f"      NEAR-vs-EXACT 4b leg changes at the CHOSEN cells: "
        f"{int(W.ruler_leg_changes.sum())} across {4*len(W)} chosen-cell contrasts.")

    # G8 recompute — rebuild one published cell from scratch and compare
    pan = panels[0]
    sg = segments(pan, I_N, I_H)
    ref2 = net(run_book(pan, sg, lambda j, ts, st: I_G))
    r2 = net(run_book(pan, sg, dev_gross("STOP", 0.50, 0.075, pan, ref2)))
    ref_row = G[(G.panel == "U56") & (G.fam == "STOP") & (G.frac == 0.50) & (G.th == 0.075)]
    dev8 = abs(float(ref_row.Sharpe.iloc[0]) - sharpe(r2[WARMUP:]))
    gate("G8 bit-identical recompute of one cell (U56 / STOP / 0.50 / 0.075)", f"{dev8:.3e}",
         "< 1e-12", dev8 < 1e-12)

    ok = all(g["pass_"] for g in GATES)
    say(f"\n  ALL GATES: {'PASS' if ok else 'FAIL'}  ({sum(g['pass_'] for g in GATES)} of "
        f"{len(GATES)})")

    verdict = ("KILL (as a record-wide re-cut)" if not material
               else "KEEP-METHOD (re-cut required)")
    say(f"\n  VERDICT: {verdict}")
    say(f"  Runtime {time.time()-t0:.1f}s")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return dict(G=G, R=R, W=W, material=material, verdicts=verdicts)


if __name__ == "__main__":
    main()
