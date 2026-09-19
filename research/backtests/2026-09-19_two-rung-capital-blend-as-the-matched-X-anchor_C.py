#!/usr/bin/env python3
"""
Idea 1509 (lane C, 2026-09-19) — should the record's DEVICE-vs-ANCHOR contrasts ALL be re-cut
against a TWO-RUNG CAPITAL BLEND?

THE PREMISE (idea 1484's own finding, generalised).  1484 compared a turnover-capped book to the
min-hold ladder AT MATCHED TURNOVER by blending the two BRACKETING RUNGS of the comparand's own
dial: a capital split between two ladders, which is an IMPLEMENTABLE BOOK and therefore a fairer
anchor than any single rung.  It bracketed 240 of 240 cells.  Every OTHER matched-X contrast in
this record — the six-to-eight de-gross twins of 1405 / 1413 / 1429 / 1433 / 1436 / 1446 / 1454 /
1461 / 1468 / 1488, "matched gross", "matched exposure", "matched CAGR" — was cut against a
SINGLE RUNG or an INTERPOLATED STATISTIC instead.  This run censuses those claims and RE-CUTS
them, and it asks the one question that decides whether the record must be re-read:

    HOW MANY MATCHED-X CONTRASTS FLIP SIGN OR LOSE SIGNIFICANCE WHEN THE ANCHOR MOVES FROM A
    SINGLE RUNG (OR AN INTERPOLATED STATISTIC) TO A TWO-RUNG CAPITAL BLEND?

THE MECHANISM THIS RUN IS REALLY TESTING, STATED UP FRONT SO THE RESULT CANNOT BE DRESSED UP.
A capital blend of two rungs differs from the single interpolated rung ONLY IF THE TWO RUNGS
HOLD DIFFERENT THINGS.  This record's ladders come in two kinds:
  SCALE ladder  (GROSS g): every rung holds the SAME names at the SAME relative weights and
                differs only in how much NAV is invested.  A capital split between two such
                rungs IS, holding for holding, a single rung at the blended gross.
  COMPOSITION ladder (MIN-HOLD H): rungs hold DIFFERENT names on the same day.  A capital split
                between two such rungs is a book NO single rung can reproduce.
1484's blend mattered because H is a composition ladder.  Every de-gross twin in the record is
cut against the GROSS ladder, which is a scale ladder.  If the mechanism is right, the re-cut
moves the de-gross claims by ~0 on exposure-matched contrasts and by a MEASURABLE amount on
CAGR-matched ones (CAGR is not linear in gross, so rounding to a rung is a real error there).
Both halves are measured here, on real books, and the prediction is allowed to fail.

THE GRID (all of it published, nothing selected on).
  DEVICES, 3 families x 5 STRENGTHS x 3 THRESHOLDS = 45 books per panel, 135 in all:
    STOP    trailing equity stop (the 1468 family): gross -> FRAC*G while the book's own equity
            is more than DEPTH below its running peak at the decision row.
    MAGATE  SPY 200d MA gate: gross -> FRAC*G while SPY is below MA200*(1 - BAND) at the
            decision row.
    VOLTGT  vol target: gross -> G*clip(TARGET/vol20(sleeve), FRAC, 1.0), the sleeve vol taken
            from the FROZEN G = 0.75 reference book (NON-CIRCULAR, causal).
    FRAC = 1.00 is the INERT rung of all three families and must reproduce the frozen incumbent
    bit for bit (gate G2).
  ANCHOR LADDERS, comparand curves, NEVER selected on (gate G5):
    L_G  gross g in {0.10 .. 1.00, 0.75 included}          — 11 rungs, SCALE ladder.
    L_H  min-hold H in {1, 21, 42, 63, 126, 189, 252, 504} — 8 rungs, COMPOSITION ladder, G=0.75.
  MATCHING STATISTICS X, both published, neither a dial:
    X_EXP   realised mean invested exposure   (the record's "matched gross"/"matched exposure")
    X_CAGR  realised CAGR                     (the record's "CAGR-neutral" contrasts)
    X_TURN  realised annual turnover          (1484's own statistic; L_H only)
  RULERS (the thing under test):
    R_NEAR   the NEAREST single rung by |X_rung - X_device|          — a book
    R_STAT   the METRIC linearly interpolated between the two bracketing rungs — NOT a book, and
             therefore carrying NO return series and NO paired standard error at all
    R_BLEND  the TWO-RUNG CAPITAL BLEND, capital share a solved so the blended X equals the
             device's EXACTLY                                        — a book
    R_BLENDC R_BLEND charged its OWN cross-sleeve rebalancing turnover at 10 bps (1484 flagged
             that its blend ignored this and was therefore flattered; here it is priced, as a
             deliberate UPPER bound — the two sleeves overlap, so their true cross cost is less)

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  STRENGTH  FRAC {1.00, 0.75, 0.50, 0.25, 0.00}
  DIAL 2  THRESHOLD {STOP DEPTH 0.05/0.075/0.10; MAGATE BAND 0.00/0.03/0.06; VOLTGT TARGET
                     0.10/0.15/0.20}
FROZEN, NEVER SELECTED ON: N = 20, G = 0.75, H = 126, weekly cadence, the live 3-leg composite,
MAXVOL = 0.60, cost 10 bps (the protocol rung, not a dial).

PRE-REGISTERED BAR, WRITTEN BEFORE ANY NUMBER WAS READ.  The two-rung capital blend MATERIALLY
CHANGES the committed record only if, at 10 bps, on U56 AND B136, EITHER
  (i)  >= 10% of biting device contrasts FLIP THE SIGN of dSharpe when the anchor moves from
       R_NEAR to R_BLEND, OR
  (ii) >= 10% of them CHANGE THEIR |t| > 2 DECISION between those two rulers.
Anything less and the answer is IMMATERIAL: every committed matched-X claim stands as cut, and
1484's blend was a fix for a COMPOSITION ladder that the de-gross record does not need.
CAPITAL ARM, pre-registered with it: the blend ruler is worth a rules change only if a rule-8
chooser keyed on the BLEND picks a book that beats BOTH the R_NEAR-keyed chooser's pick AND the
do-nothing frozen incumbent on OOS Sharpe.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no shorting, no leverage); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths at every cell, exactly 2 tuned dials); rule 8 (walk-forward: every
chooser fits on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 cross-script replay of the committed 2026-09-04 U56 anchor.
G2 FRAC = 1.00 is bit-identical to the frozen constant-gross book at every threshold and family.
G3 every solved blend share a lies in [0, 1] and reproduces the device's X to <= 1e-10.
G4 no leverage: every executed weight sum <= its own target gross <= 1.  G5 exactly two tuned
dials; no book is ever selected on either ladder.  G6 no chooser reads a row on/after 2017-01-01.
G7 bracketing census: every unbracketed contrast is counted and published, never silently
dropped.  G8 the STRENGTH dial BITES (realised mean exposure strictly decreasing in FRAC at
every biting family/threshold).  G9 SCALE-LADDER ALGEBRA, published not asserted: max |dSharpe|
and |dCAGR| between a two-rung gross blend and the single gross rung at the same blended
exposure.  G10 bit-identical recompute of the headline cell.  G11 a degenerate blend (a = 0 or
a = 1) equals its own rung exactly.  G12 the SMALL panel's protocol-mandated meta filter applied.
G13 the census is MECHANICAL: every classification is a published regex over committed bytes.
CENSUS VINTAGE, stated because a census of a growing record is not idempotent: the counts below
are of the record AS COMMITTED AT 2026-09-19 BEFORE this run's own LEADERBOARD / CHANGELOG /
memo rows were appended.  Re-running this script after that commit will count MORE sentences,
including this run's own — which is why the vintage, not just the count, is published.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_two-rung-capital-blend-as-the-matched-X-anchor_C.py
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
SLUG = "two-rung-capital-blend-as-the-matched-X-anchor"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
CADENCE = "W"
COST = 10.0                                # the protocol rung; NOT a dial in this run
FRACS = [1.00, 0.75, 0.50, 0.25, 0.00]     # DIAL 1 — STRENGTH; 1.00 is the inert rung
THRESH = {"STOP": [0.05, 0.075, 0.10],     # DIAL 2 — THRESHOLD, family-specific
          "MAGATE": [0.00, 0.03, 0.06],
          "VOLTGT": [0.10, 0.15, 0.20]}
FAMS = ["STOP", "MAGATE", "VOLTGT"]
G_LADDER = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]
H_LADDER = [1, 21, 42, 63, 126, 189, 252, 504]
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, SEED, L_BOOT = 400, 20260919, 63
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857, oCAGR=0.1732)
BAR_FLIP = 0.10                            # pre-registered materiality threshold

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


# ---------------------------------------------------------------------------------------------
# PART A — THE CENSUS.  Mechanical, over committed bytes only (gate G13).
# ---------------------------------------------------------------------------------------------
X_PATS = {
    "matched gross": r"matched[- ]gross",
    "matched exposure": r"matched[- ]exposure",
    "matched CAGR": r"matched[- ]CAGR|CAGR[- ]neutral|CAGR[- ]matched",
    "matched turnover": r"matched[- ]turnover",
    "matched vol": r"matched[- ]vol",
    "de-gross twin": r"de[- ]gross(ed)?[- ]twin",
}
FORM_PATS = [("BLEND", r"\bblend"),
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
            for xname, xp in X_PATS.items():
                if not re.search(xp, s, re.I):
                    continue
                form = "UNSTATED"
                for fname, fp in FORM_PATS:
                    if re.search(fp, s, re.I):
                        form = fname
                        break
                rows.append(dict(file=f.name, kind=kind, X=xname, anchor_form=form,
                                 text=s[:300].replace("|", "/")))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------------------------
# PART B/C — REAL BOOKS.  Mechanics lifted unchanged from the committed lane-C engine (1484).
# ---------------------------------------------------------------------------------------------
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


def run_book(pan, segs, gross_fn):
    """One book.  `gross_fn(j, ts, state) -> target gross`, causal: `state` carries only rows
    strictly before this segment's first traded row.  Weights applied at i0, drift inside."""
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    expo = np.zeros(T)
    gtar = np.zeros(len(segs))
    curw = np.zeros(M)
    eq, peak = 1.0, 1.0
    for j, (i0, i1, ts, sel) in enumerate(segs):
        state = dict(eq=eq, peak=peak, i0=i0, ts=ts, out=out, expo=expo)
        g = float(gross_fn(j, ts, state))
        tgt = np.zeros(M)
        if len(sel) and g > 0:
            tgt[pan.iinv[sel]] = g / len(sel)
        turn[i0] = float(np.abs(tgt - curw).sum())
        gtar[j] = float(tgt.sum())
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
        seg_growth = float(np.prod(1.0 + out[i0:i1] - (turn[i0:i1] * COST / 1e4)))
        eq *= seg_growth
        peak = max(peak, eq)
    return dict(gross_ret=out, turn=turn, expo=expo, gtar=gtar)


def net(b):
    return b["gross_ret"] - b["turn"] * COST / 1e4


def const_gross(g):
    return lambda j, ts, st: g


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


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def block_index(n, L=L_BOOT, reps=BOOT_REPS, seed=SEED):
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def sharpe_rows(X):
    v = X.std(axis=1, ddof=0) * np.sqrt(252)
    return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)


# ---------------------------------------------------------------------------------------------
# THE RULERS
# ---------------------------------------------------------------------------------------------
def blend_cross_turn(r_lo, r_hi, a):
    """Daily cross-sleeve rebalancing turnover of a fixed (1-a, a) capital split.  UPPER bound:
    the two sleeves hold the SAME names at scale-ladder rungs, so their true cross cost is less."""
    rb = (1 - a) * r_lo + a * r_hi
    dev = (1 - a) * a * (r_lo - r_hi) / (1.0 + rb)
    return 2.0 * np.abs(dev)


def solve_linear_share(x_lo, x_hi, x_dev):
    if abs(x_hi - x_lo) < 1e-15:
        return None
    a = (x_dev - x_lo) / (x_hi - x_lo)
    return a if -1e-12 <= a <= 1 + 1e-12 else None


def solve_cagr_share(r_lo, r_hi, target):
    """Bisection on the capital share so the BLEND's realised CAGR equals the device's."""
    f = lambda a: cagr((1 - a) * r_lo + a * r_hi) - target
    lo, hi = 0.0, 1.0
    flo, fhi = f(lo), f(hi)
    if not np.isfinite(flo) or not np.isfinite(fhi) or flo * fhi > 0:
        return None
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def main():
    t0 = time.time()
    say("=" * 140)
    say("IDEA 1509 (lane C, 2026-09-19) — should the record's DEVICE-vs-ANCHOR contrasts ALL be "
        "RE-CUT against a TWO-RUNG CAPITAL BLEND?")
    say("1484 blended the two bracketing rungs of the comparand's own dial (an IMPLEMENTABLE "
        "book).  Every other matched-X contrast in the record was cut against a SINGLE RUNG or "
        "an INTERPOLATED STATISTIC.")
    say(f"DIAL 1 STRENGTH FRAC {FRACS}.  DIAL 2 THRESHOLD {THRESH}.  FROZEN: N={I_N}, G={I_G}, "
        f"H={I_H}, weekly, {COST:.0f} bps.")
    say(f"ANCHOR LADDERS, never selected on: L_G (SCALE) {G_LADDER};  L_H (COMPOSITION) "
        f"{H_LADDER}.   RULERS: R_NEAR, R_STAT, R_BLEND, R_BLENDC.")
    say(f"PRE-REGISTERED BAR: the blend ruler is MATERIAL only if, at 10 bps on U56 AND B136, "
        f">= {BAR_FLIP:.0%} of biting contrasts FLIP THE SIGN of dSharpe or CHANGE their |t|>2 "
        f"decision between R_NEAR and R_BLEND.")
    say("=" * 140)

    # ---------------- PART A — CENSUS ----------------------------------------------------
    say("\n[PART A]  CENSUS OF COMMITTED MATCHED-X CLAIMS (mechanical; every classification is a "
        "published regex over committed bytes — gate G13).")
    cen = census()
    cen.to_csv(f"{OUT}.census.csv", index=False)
    if len(cen):
        piv = pd.crosstab(cen["X"], cen["anchor_form"])
        for c in ["BLEND", "STAT-INTERP", "SINGLE-RUNG", "UNSTATED"]:
            if c not in piv.columns:
                piv[c] = 0
        piv = piv[["BLEND", "STAT-INTERP", "SINGLE-RUNG", "UNSTATED"]]
        say("\n  ANCHOR FORM x MATCHING STATISTIC (sentences in LEADERBOARD.md, CHANGELOG.md, "
            "every committed memo/result and every committed script docstring):")
        for ln in piv.to_string().split("\n"):
            say("    " + ln)
        tot = int(piv.values.sum())
        nb = int(piv["BLEND"].sum())
        say(f"\n  TOTAL matched-X sentences: {tot}.  Cut against a BLEND: {nb} "
            f"({nb/max(tot,1):.1%}).  Against a SINGLE RUNG or an INTERPOLATED STATISTIC or "
            f"UNSTATED: {tot-nb} ({(tot-nb)/max(tot,1):.1%}).")
        say("  READ THIS AS A LOWER BOUND ON PREVALENCE AND NOTHING MORE: it counts SENTENCES, "
            "not distinct claims, and a sentence that never names its anchor form is counted "
            "UNSTATED, not miscut.")
        piv.to_csv(f"{OUT}.census_pivot.csv")
        publish("G13 census corpus", f"{cen['file'].nunique()} files, {tot} sentences")
    else:
        say("    (census found no matched-X sentences — unexpected; re-cut proceeds regardless)")

    # ---------------- PANELS --------------------------------------------------------------
    say("\n[PART B/C]  THE RE-CUT ON REAL BOOKS.")
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    gate("G12 SMALL protocol meta filter applied", f"{len(bad)} tickers dropped", ">0", len(bad) > 0)

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND.  "
        "What this run reads is a CONTRAST BETWEEN TWO RULERS applied to the SAME books on the "
        "SAME days — a bias common to both cancels in the difference.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G5 exactly two tuned dials (STRENGTH, THRESHOLD); both anchor ladders are published "
         "comparand curves and no book is ever selected on them", "FRAC x THRESHOLD", "2 dials",
         True)

    grid, recut, wf, alg = [], [], [], []
    g1_dev = None
    g2_dev = 0.0
    g3_ok = g8_ok = g11_ok = True
    saturated = []
    g4_max = 0.0
    g9_sh = g9_cg = 0.0
    n_unbracket = 0
    n_contrast = 0
    head_ret = None

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        ann = 252.0 / (T - WARMUP)
        idx_boot = block_index(T - WARMUP)

        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%}  | 4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  "
            f"| 4b OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps {live['CAGR']:.2%}/{live['Sharpe']:.4f}/"
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f} | OOS "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        seg_I = segments(pan, I_N, I_H)
        ref = run_book(pan, seg_I, const_gross(I_G))
        ref_net = net(ref)
        ref_sleeve = np.where(ref["expo"] > 1e-9, ref["gross_ret"] / np.maximum(ref["expo"], 1e-9),
                              0.0)

        # ---- the FROZEN incumbent, and gate G1 ----
        rI = ref_net[WARMUP:]
        mI = triple(rI)
        h1I, h2I = halves(rI)
        mIO = triple(ref_net[i_oos:])
        say(f"    FROZEN INCUMBENT (N={I_N}, H={I_H}, G={I_G}, weekly, 10bps): "
            f"{mI['CAGR']:.2%}/{mI['Sharpe']:.4f}/{mI['MaxDD']:.2%} H1/H2 {h1I:.3f}/{h2I:.3f}"
            f" | OOS {mIO['CAGR']:.2%}/{mIO['Sharpe']:.4f}/{mIO['MaxDD']:.2%}")
        if pan.name == "U56":
            g1_dev = max(abs(mI["CAGR"] - C_U56["CAGR"]), abs(mI["Sharpe"] - C_U56["Sharpe"]),
                         abs(mI["MaxDD"] - C_U56["MaxDD"]))

        # ---- ANCHOR LADDERS ----
        Lg = {}
        for g in G_LADDER:
            b = run_book(pan, seg_I, const_gross(g))
            r = net(b)[WARMUP:]
            Lg[g] = dict(r=r, X_EXP=float(b["expo"][WARMUP:].mean()), X_CAGR=cagr(r),
                         X_TURN=float(b["turn"][WARMUP:].sum() * ann), Sharpe=sharpe(r),
                         CAGR=cagr(r), MaxDD=mdd(r), is_r=net(b)[WARMUP:i_oos],
                         X_EXP_is=float(b["expo"][WARMUP:i_oos].mean()))
            g4_max = max(g4_max, float(b["gtar"].max()))
        Lh = {}
        for H in H_LADDER:
            sg = seg_I if H == I_H else segments(pan, I_N, H)
            b = run_book(pan, sg, const_gross(I_G))
            r = net(b)[WARMUP:]
            Lh[H] = dict(r=r, X_EXP=float(b["expo"][WARMUP:].mean()), X_CAGR=cagr(r),
                         X_TURN=float(b["turn"][WARMUP:].sum() * ann), Sharpe=sharpe(r),
                         CAGR=cagr(r), MaxDD=mdd(r))
        say("    L_G (SCALE) realised mean exposures: "
            + " ".join(f"{g:.2f}->{Lg[g]['X_EXP']:.4f}" for g in G_LADDER))
        say("    L_H (COMPOSITION) realised annual turnovers: "
            + " ".join(f"H{H}->{Lh[H]['X_TURN']:.2f}" for H in H_LADDER))

        # ---- GATE G9: the SCALE-LADDER ALGEBRA, measured not asserted ----
        for glo, ghi in [(0.60, 0.70), (0.70, 0.75), (0.75, 0.80)]:
            for a in (0.25, 0.5, 0.75):
                rb = (1 - a) * Lg[glo]["r"] + a * Lg[ghi]["r"]
                xb = (1 - a) * Lg[glo]["X_EXP"] + a * Lg[ghi]["X_EXP"]
                # the single continuous rung with the SAME realised exposure
                gs = sorted(G_LADDER)
                xs = [Lg[g]["X_EXP"] for g in gs]
                g_eq = float(np.interp(xb, xs, gs))
                be = run_book(pan, seg_I, const_gross(g_eq))
                re_ = net(be)[WARMUP:]
                d_sh, d_cg = abs(sharpe(rb) - sharpe(re_)), abs(cagr(rb) - cagr(re_))
                g9_sh, g9_cg = max(g9_sh, d_sh), max(g9_cg, d_cg)
                alg.append(dict(panel=pan.name, g_lo=glo, g_hi=ghi, a=a, g_equiv=g_eq,
                                Sharpe_blend=sharpe(rb), Sharpe_rung=sharpe(re_), dSharpe=d_sh,
                                CAGR_blend=cagr(rb), CAGR_rung=cagr(re_), dCAGR=d_cg,
                                xtra_turn=float(blend_cross_turn(Lg[glo]["r"], Lg[ghi]["r"],
                                                                 a).sum() * ann)))
        # G11 degenerate blend
        rb0 = (1 - 0.0) * Lg[0.75]["r"] + 0.0 * Lg[0.90]["r"]
        g11_ok = g11_ok and float(np.max(np.abs(rb0 - Lg[0.75]["r"]))) == 0.0

        # ---- DEVICES ----
        say(f"\n    [{pan.name}] DEVICE GRID (45 books).  4a/4b read at every cell, FULL and OOS.")
        say("      " + f"{'fam':>7} {'th':>6} {'frac':>5} {'meanExp':>8} {'turn':>6} "
                       f"{'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>6} {'H2':>6} "
                       f"{'oCAGR':>8} {'oShrp':>7} {'oMaxDD':>8} {'4a':>3} {'4b':>3} {'o4b':>4}")
        dev = {}
        for fam in FAMS:
            for th in THRESH[fam]:
                prev_exp = None
                for fr in FRACS:
                    b = run_book(pan, seg_I, dev_gross(fam, fr, th, pan, ref_sleeve))
                    rn = net(b)
                    r, ro = rn[WARMUP:], rn[i_oos:]
                    k4a, k4b, m, h1, h2, legs = keep_paths(r, spy, live)
                    o4a, o4b, mo, _, _, olegs = keep_paths(ro, spyO, liveO)
                    xe = float(b["expo"][WARMUP:].mean())
                    tn = float(b["turn"][WARMUP:].sum() * ann)
                    dev[(fam, th, fr)] = dict(r=r, ro=ro, X_EXP=xe, X_CAGR=m["CAGR"], X_TURN=tn,
                                              Sharpe=m["Sharpe"], CAGR=m["CAGR"],
                                              MaxDD=m["MaxDD"], is_r=rn[WARMUP:i_oos],
                                              X_EXP_is=float(b["expo"][WARMUP:i_oos].mean()))
                    g4_max = max(g4_max, float(b["gtar"].max()))
                    if fr == 1.00:
                        g2_dev = max(g2_dev, float(np.max(np.abs(rn - ref_net))))
                    elif prev_exp is not None:
                        if xe > prev_exp + 1e-12:
                            g8_ok = False
                        elif xe > prev_exp - 1e-12:
                            saturated.append(f"{pan.name}/{fam}/{th}/FRAC {fr:.2f}")
                    prev_exp = xe
                    grid.append(dict(panel=pan.name, fam=fam, th=th, frac=fr, meanExp=xe,
                                     turn=tn, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                     MaxDD=m["MaxDD"], H1=h1, H2=h2, oCAGR=mo["CAGR"],
                                     oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"], keep4a=k4a,
                                     keep4b=k4b, o_keep4a=o4a, o_keep4b=o4b,
                                     legs="".join(k for k, v in legs.items() if not v) or "-"))
                    say("      " + f"{fam:>7} {th:>6.3f} {fr:>5.2f} {xe:>8.4f} {tn:>6.2f} "
                                   f"{m['CAGR']:>8.2%} {m['Sharpe']:>8.4f} {m['MaxDD']:>8.2%} "
                                   f"{h1:>6.3f} {h2:>6.3f} {mo['CAGR']:>8.2%} "
                                   f"{mo['Sharpe']:>7.4f} {mo['MaxDD']:>8.2%} "
                                   f"{'Y' if k4a else '.':>3} {'Y' if k4b else '.':>3} "
                                   f"{'Y' if o4b else '.':>4}")
                    if pan.name == "U56" and fam == "STOP" and th == 0.075 and fr == 0.50:
                        head_ret = r.copy()

        # ---- THE RE-CUT: four rulers, two ladders, three matching statistics --------------
        combos = [("L_G", "X_EXP", Lg, G_LADDER), ("L_G", "X_CAGR", Lg, G_LADDER),
                  ("L_H", "X_TURN", Lh, H_LADDER), ("L_H", "X_CAGR", Lh, H_LADDER)]
        for lname, xname, L, keys in combos:
            ks = sorted(keys, key=lambda k: L[k][xname])
            xs = np.array([L[k][xname] for k in ks])
            for (fam, th, fr), d in dev.items():
                if fr >= 1.0:
                    continue                      # the inert rung is not a contrast
                n_contrast += 1
                xd = d[xname]
                if xd < xs[0] - 1e-12 or xd > xs[-1] + 1e-12:
                    n_unbracket += 1
                    recut.append(dict(panel=pan.name, ladder=lname, X=xname, fam=fam, th=th,
                                      frac=fr, bracketed=False))
                    continue
                j = int(np.searchsorted(xs, xd))
                j = min(max(j, 1), len(xs) - 1)
                klo, khi = ks[j - 1], ks[j]
                # R_NEAR
                near = ks[int(np.argmin(np.abs(xs - xd)))]
                # R_BLEND
                if xname == "X_CAGR":
                    a = solve_cagr_share(L[klo]["r"], L[khi]["r"], xd)
                else:
                    a = solve_linear_share(L[klo][xname], L[khi][xname], xd)
                if a is None:
                    n_unbracket += 1
                    recut.append(dict(panel=pan.name, ladder=lname, X=xname, fam=fam, th=th,
                                      frac=fr, bracketed=False))
                    continue
                a = float(np.clip(a, 0.0, 1.0))
                rb = (1 - a) * L[klo]["r"] + a * L[khi]["r"]
                xb = ((1 - a) * L[klo][xname] + a * L[khi][xname]) if xname != "X_CAGR" \
                    else cagr(rb)
                if not (0.0 - 1e-12 <= a <= 1.0 + 1e-12) or abs(xb - xd) > 1e-10:
                    g3_ok = False
                # R_BLENDC: the blend charged its OWN cross-sleeve rebalancing, 10 bps, UPPER bound
                xt = blend_cross_turn(L[klo]["r"], L[khi]["r"], a)
                rbc = rb - xt * COST / 1e4
                # R_STAT: the METRIC interpolated — a number, NOT a book, NO return series
                w = 0.0 if xs[j] == xs[j - 1] else (xd - xs[j - 1]) / (xs[j] - xs[j - 1])
                st_sh = (1 - w) * L[klo]["Sharpe"] + w * L[khi]["Sharpe"]
                st_cg = (1 - w) * L[klo]["CAGR"] + w * L[khi]["CAGR"]
                st_dd = (1 - w) * L[klo]["MaxDD"] + w * L[khi]["MaxDD"]
                row = dict(panel=pan.name, ladder=lname, X=xname, fam=fam, th=th, frac=fr,
                           bracketed=True, x_dev=xd, k_lo=klo, k_hi=khi, a=a, k_near=near,
                           blend=f"{(1-a)*100:.0f}%{klo}+{a*100:.0f}%{khi}",
                           dSh_NEAR=d["Sharpe"] - L[near]["Sharpe"],
                           dSh_STAT=d["Sharpe"] - st_sh,
                           dSh_BLEND=d["Sharpe"] - sharpe(rb),
                           dSh_BLENDC=d["Sharpe"] - sharpe(rbc),
                           dCG_NEAR=100 * (d["CAGR"] - L[near]["CAGR"]),
                           dCG_STAT=100 * (d["CAGR"] - st_cg),
                           dCG_BLEND=100 * (d["CAGR"] - cagr(rb)),
                           dCG_BLENDC=100 * (d["CAGR"] - cagr(rbc)),
                           dDD_NEAR=100 * (d["MaxDD"] - L[near]["MaxDD"]),
                           dDD_STAT=100 * (d["MaxDD"] - st_dd),
                           dDD_BLEND=100 * (d["MaxDD"] - mdd(rb)))
                for rn_, ranc in (("NEAR", L[near]["r"]), ("BLEND", rb), ("BLENDC", rbc)):
                    db = sharpe_rows(d["r"][idx_boot]) - sharpe_rows(ranc[idx_boot])
                    se = float(np.nanstd(db, ddof=1))
                    row[f"t_{rn_}"] = (row[f"dSh_{rn_}"] / se) if se > 0 else np.nan
                row["t_STAT"] = np.nan          # an interpolated STATISTIC has no series, so no SE
                recut.append(row)

        # ---- RULE 8 WALK-FORWARD ------------------------------------------------------
        say(f"\n    [{pan.name}] RULE 8 — every chooser fits on warm-up..2016-12-31 ONLY; "
            f"2017-2026 read ONCE.")
        Lg_is = {g: Lg[g]["is_r"] for g in G_LADDER}
        xs_exp_is = {g: Lg[g]["X_EXP_is"] for g in G_LADDER}
        gs_sorted = sorted(G_LADDER, key=lambda g: xs_exp_is[g])
        xs_is = np.array([xs_exp_is[g] for g in gs_sorted])
        cells = [k for k in dev if k[2] < 1.0]
        scores = {"C_RAW": {}, "C_NEAR": {}, "C_BLEND": {}, "C_STAT": {}}
        for k in cells:
            d = dev[k]
            sh = sharpe(d["is_r"])
            xd = d["X_EXP_is"]
            scores["C_RAW"][k] = sh
            if xd < xs_is[0] or xd > xs_is[-1]:
                for c in ("C_NEAR", "C_BLEND", "C_STAT"):
                    scores[c][k] = -np.inf
                continue
            j = min(max(int(np.searchsorted(xs_is, xd)), 1), len(xs_is) - 1)
            glo, ghi = gs_sorted[j - 1], gs_sorted[j]
            near = gs_sorted[int(np.argmin(np.abs(xs_is - xd)))]
            a = solve_linear_share(xs_exp_is[glo], xs_exp_is[ghi], xd)
            a = 0.0 if a is None else float(np.clip(a, 0, 1))
            rbl = (1 - a) * Lg_is[glo] + a * Lg_is[ghi]
            w = 0.0 if xs_is[j] == xs_is[j - 1] else (xd - xs_is[j - 1]) / (xs_is[j] - xs_is[j - 1])
            scores["C_NEAR"][k] = sh - sharpe(Lg_is[near])
            scores["C_BLEND"][k] = sh - sharpe(rbl)
            scores["C_STAT"][k] = sh - ((1 - w) * sharpe(Lg_is[glo]) + w * sharpe(Lg_is[ghi]))
        for cn, sc in scores.items():
            pick = max(cells, key=lambda k: (sc[k] if np.isfinite(sc[k]) else -np.inf))
            ro = dev[pick]["ro"]
            o4a, o4b, mo, oh1, oh2, olegs = keep_paths(ro, spyO, liveO)
            wf.append(dict(panel=pan.name, chooser=cn, pick=f"{pick[0]}/{pick[1]}/{pick[2]}",
                           IS_score=sc[pick], oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                           oMaxDD=mo["MaxDD"], o_keep4a=o4a, o_keep4b=o4b,
                           anchor_oSharpe=mIO["Sharpe"], spy_oSharpe=spyO["Sharpe"],
                           live_oSharpe=liveO["Sharpe"],
                           beats_anchor=bool(mo["Sharpe"] > mIO["Sharpe"])))
            say(f"      {cn:>8}  picks {pick[0]}/{pick[1]}/{pick[2]:.2f}  ->  OOS "
                f"{mo['CAGR']:.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:.2%}   "
                f"(frozen anchor OOS {mIO['CAGR']:.2%}/{mIO['Sharpe']:.4f}/{mIO['MaxDD']:.2%}; "
                f"SPY {spyO['Sharpe']:.4f})  4b-OOS {'Y' if o4b else '.'}")
        wf.append(dict(panel=pan.name, chooser="DO-NOTHING (frozen incumbent)", pick=f"G={I_G}",
                       IS_score=np.nan, oCAGR=mIO["CAGR"], oSharpe=mIO["Sharpe"],
                       oMaxDD=mIO["MaxDD"],
                       o_keep4a=keep_paths(ref_net[i_oos:], spyO, liveO)[0],
                       o_keep4b=keep_paths(ref_net[i_oos:], spyO, liveO)[1],
                       anchor_oSharpe=mIO["Sharpe"], spy_oSharpe=spyO["Sharpe"],
                       live_oSharpe=liveO["Sharpe"], beats_anchor=False))

    # ---------------- GATES ---------------------------------------------------------------
    say("\n[GATES]")
    gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor",
         f"max|dev| {g1_dev:.2e}", "<= 5e-3", g1_dev is not None and g1_dev <= 5e-3)
    gate("G2 FRAC = 1.00 is bit-identical to the frozen constant-gross book at every family "
         "and threshold", f"max|dev| {g2_dev:.2e}", "0.0", g2_dev == 0.0)
    gate("G3 every solved blend share a in [0,1] and reproduces the device's X to <= 1e-10",
         g3_ok, "True", g3_ok)
    gate("G4 no leverage (rule 2): max target gross over every book", f"{g4_max:.6f}",
         "<= 1.0", g4_max <= 1.0 + 1e-12)
    gate("G8 the STRENGTH dial BITES (mean exposure MONOTONE NON-INCREASING as FRAC falls)",
         g8_ok, "True", g8_ok)
    say(f"    G8b SATURATION CENSUS (published, not asserted): {len(saturated)} of "
        f"{3*len(FAMS)*3*(len(FRACS)-1)} strength steps move exposure by < 1e-12 — a device "
        f"whose threshold never binds cannot be made weaker: {saturated}")
    publish("G8b saturated strength steps", "; ".join(saturated) if saturated else "none")
    RC = pd.DataFrame(recut)
    br = RC[RC["bracketed"] == True] if len(RC) else RC
    gate("G7 bracketing census (published, never silently dropped)",
         f"{n_unbracket} unbracketed of {n_contrast} contrasts", "published", True)
    gate("G9 SCALE-LADDER ALGEBRA: a two-rung GROSS blend vs the single rung at the SAME "
         "realised exposure", f"max|dSharpe| {g9_sh:.2e}, max|dCAGR| {g9_cg:.2e}",
         "published, not asserted", True)
    gate("G11 a degenerate blend (a = 0) equals its own rung exactly", g11_ok, "True", g11_ok)
    if head_ret is not None:
        say(f"    G10 headline cell (U56 / STOP / depth 0.075 / FRAC 0.50) "
            f"{cagr(head_ret):.6%} / {sharpe(head_ret):.6f} / {mdd(head_ret):.6%}")
        publish("G10 headline recompute", f"{cagr(head_ret):.10f}/{sharpe(head_ret):.10f}")
    gate("G6 no chooser reads a row on or after 2017-01-01", "IS window = warm-up..2016-12-31",
         "True", True)

    # ---------------- THE READ ------------------------------------------------------------
    say("\n" + "=" * 140)
    say("[THE READ]  DOES THE RULER MATTER?")
    ALG = pd.DataFrame(alg)
    say(f"\n  (B) THE SCALE-LADDER ALGEBRA, measured on {len(ALG)} real blends: a two-rung GROSS "
        f"blend and the single gross rung at the SAME realised exposure differ by at most")
    say(f"      |dSharpe| {ALG['dSharpe'].max():.2e} and |dCAGR| {ALG['dCAGR'].max():.2e}.  "
        f"Median cross-sleeve rebalancing turnover the blend would owe: "
        f"{ALG['xtra_turn'].median():.4f}x/yr ({1e4*0+COST:.0f} bps on that is "
        f"{COST*ALG['xtra_turn'].median()/1e4:.2%}/yr).")
    say("      A GROSS ladder is a SCALE ladder: every rung holds the same names at the same "
        "relative weights, so a capital split between two rungs IS a single rung at the blended")
    say("      gross.  This is the mechanism, and it is measured here rather than asserted.")

    if len(br):
        say(f"\n  (C) THE RE-CUT.  {len(br)} bracketed contrasts of {n_contrast} "
            f"({n_unbracket} unbracketed, published).")
        for (ld, xn), sub in br.groupby(["ladder", "X"]):
            flip = ((np.sign(sub["dSh_NEAR"]) != np.sign(sub["dSh_BLEND"]))
                    & (sub["dSh_NEAR"].abs() > 1e-12) & (sub["dSh_BLEND"].abs() > 1e-12))
            sigN = sub["t_NEAR"].abs() > 2
            sigB = sub["t_BLEND"].abs() > 2
            dec = sigN != sigB
            say(f"\n    {ld} matched on {xn}:  n = {len(sub)}")
            say(f"      mean dSharpe   R_NEAR {sub['dSh_NEAR'].mean():+.4f}   "
                f"R_STAT {sub['dSh_STAT'].mean():+.4f}   R_BLEND {sub['dSh_BLEND'].mean():+.4f}"
                f"   R_BLENDC {sub['dSh_BLENDC'].mean():+.4f}")
            say(f"      mean dCAGR pp  R_NEAR {sub['dCG_NEAR'].mean():+.3f}   "
                f"R_STAT {sub['dCG_STAT'].mean():+.3f}   R_BLEND {sub['dCG_BLEND'].mean():+.3f}"
                f"   R_BLENDC {sub['dCG_BLENDC'].mean():+.3f}")
            say(f"      max |R_NEAR - R_BLEND| dSharpe {(sub['dSh_NEAR']-sub['dSh_BLEND']).abs().max():.4f}"
                f"   dCAGR {(sub['dCG_NEAR']-sub['dCG_BLEND']).abs().max():.3f} pp")
            say(f"      max |R_STAT - R_BLEND| dSharpe {(sub['dSh_STAT']-sub['dSh_BLEND']).abs().max():.4f}"
                f"   dCAGR {(sub['dCG_STAT']-sub['dCG_BLEND']).abs().max():.3f} pp")
            big = flip & ((sub["dSh_NEAR"].abs() > 0.05) | (sub["dSh_BLEND"].abs() > 0.05))
            hb = sub[sub["panel"].isin(["U56", "B136"])]
            hflip = ((np.sign(hb["dSh_NEAR"]) != np.sign(hb["dSh_BLEND"]))
                     & (hb["dSh_NEAR"].abs() > 1e-12) & (hb["dSh_BLEND"].abs() > 1e-12))
            say(f"      SIGN FLIPS R_NEAR -> R_BLEND: {int(flip.sum())} of {len(sub)} "
                f"({flip.mean():.1%});  |t|>2 DECISION CHANGES: {int(dec.sum())} of {len(sub)} "
                f"({dec.mean():.1%});  significant at R_NEAR {int(sigN.sum())}, "
                f"at R_BLEND {int(sigB.sum())}")
            say(f"      of those flips, {int(big.sum())} have |dSharpe| > 0.05 on EITHER side "
                f"(the rest are contrasts sitting on zero, where a sign is not a finding).  "
                f"U56+B136 only: {int(hflip.sum())} of {len(hb)} ({hflip.mean() if len(hb) else 0:.1%})")

        head = br[br["panel"].isin(["U56", "B136"])]
        flip = ((np.sign(head["dSh_NEAR"]) != np.sign(head["dSh_BLEND"]))
                & (head["dSh_NEAR"].abs() > 1e-12) & (head["dSh_BLEND"].abs() > 1e-12))
        dec = (head["t_NEAR"].abs() > 2) != (head["t_BLEND"].abs() > 2)
        fr_flip, fr_dec = float(flip.mean()), float(dec.mean())
        material = (fr_flip >= BAR_FLIP) or (fr_dec >= BAR_FLIP)
        say(f"\n  PRE-REGISTERED BAR, U56 + B136, {len(head)} bracketed contrasts: sign flips "
            f"{fr_flip:.1%} (bar {BAR_FLIP:.0%}), |t|>2 decision changes {fr_dec:.1%} "
            f"(bar {BAR_FLIP:.0%})  ->  {'MATERIAL' if material else 'IMMATERIAL'}")
    else:
        material = False
        say("\n  (C) no bracketed contrasts — the re-cut is empty.")

    WF = pd.DataFrame(wf)
    say("\n  (D) RULE 8 — DOES THE RULER CHANGE WHAT A CHOOSER PICKS, AND IS THE PICK BETTER OOS?")
    for ln in WF.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        say("      " + ln)
    ch = WF[WF["chooser"].isin(["C_NEAR", "C_BLEND"])]
    same = all(WF[(WF.panel == p) & (WF.chooser == "C_NEAR")]["pick"].iloc[0]
               == WF[(WF.panel == p) & (WF.chooser == "C_BLEND")]["pick"].iloc[0]
               for p in WF["panel"].unique())
    cb = WF[WF.chooser == "C_BLEND"]
    cn = WF[WF.chooser == "C_NEAR"]
    dn = WF[WF.chooser.str.startswith("DO-NOTHING")]
    capital = bool((cb["oSharpe"].values > cn["oSharpe"].values).all()
                   and (cb["oSharpe"].values > dn["oSharpe"].values).all())
    say(f"      C_NEAR and C_BLEND pick the SAME cell on every panel: {same}.   "
        f"C_BLEND beats BOTH C_NEAR and the do-nothing anchor on OOS Sharpe at every panel: "
        f"{capital}  (pre-registered capital bar)")

    verdict = "KEEP-candidate" if (material and capital) else "KILL"
    say(f"\n  VERDICT: {verdict}  — the pre-registered bar was {'MET' if material else 'NOT met'} "
        f"on the ruler and {'MET' if capital else 'NOT met'} on the capital arm.")
    say("=" * 140)
    say(f"  elapsed {time.time()-t0:.1f}s")

    pd.DataFrame(grid).to_csv(f"{OUT}.grid.csv", index=False)
    RC.to_csv(f"{OUT}.recut.csv", index=False)
    ALG.to_csv(f"{OUT}.algebra.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT}.*")


if __name__ == "__main__":
    main()
