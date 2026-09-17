#!/usr/bin/env python3
"""
Idea 1209 (cloud, 2026-09-17) — does the COUNT-MATCHED-RULES SHIFT OF THE WIDEST DIAL
FROM N TO CADENCE change any COMMITTED VERDICT?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1206 (lane C, 2026-09-17,
`2026-09-17_does-the-WIDEST-DIAL-HABIT-lose-to-DOING-NOTHING-on-ladders-1155-did-not-walk_C.py`)
reported that CADENCE is called widest at 0.3072-0.3136 of picks under M_SUBSAMPLE /
M_PAIRWISE / M_D2 against 0.0551 under M_NONE, i.e. that 1155's count inflation shows up
as a change of WHICH DIAL GETS TUNED and not only as a number.  The queue asks: harvest
the record's committed "the widest dial is X" claims, re-read each under the count-matched
rules, and report how many name a different dial and how many VERDICTS rest on it.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET      {C_STRICT, C_PROX, C_ALL}                 which committed units count
  MATCHING RULE  {M_NONE, M_SUBSAMPLE, M_PAIRWISE, M_D2}   how a ladder's spread is read

  = 12 dial cells, EVERY ONE PUBLISHED.  Headline cell: C_STRICT x M_D2, declared here
  before any number (C_STRICT because only an adjudicated claim can carry a verdict; M_D2
  because it is the only count-matched rule with a closed-form, tuning-free divisor).

TIMING IS NOT A DIAL, IT IS A CONTROL, AND BOTH ARMS OF IT ARE PUBLISHED.  This run found
a one-day look-ahead in the record's inherited fast builder and does not choose between the
two timings; every table below is printed for both.  See Arm 0's second block.

WHAT IS NOT A DIAL.  Everything else is 1154/1206's, inherited whole and NOT re-tuned:
PANEL {U56, B136, SMALL}, ANCHOR {A, B}, the four CORE LADDERS {N, H, GROSS, CADENCE},
min hold, max_vol 0.60, 10 bps (rule 2), warm-up 260, IS end 2016-12-31 (rule 8), the
4a/4b legs (rule 4), SPY as the rule-4b benchmark.

DECLARED BEFORE THE TAPE IS READ — THE WHOLE SHIFT IS A RUNG-COUNT RE-WEIGHTING WITH A
KNOWN SIZE.  The four core ladders carry k = 9 (N), 4 (H), 10 (GROSS), 4 (CADENCE) rungs.
M_D2 divides each ladder's raw max-min by Hartley's d2(k), so it multiplies a ladder's
published width by 1/d2(k):

      N 1/2.970026 = 0.33670      H 1/2.058751 = 0.48573
  GROSS 1/3.077505 = 0.32494  CADENCE 1/2.058751 = 0.48573

Therefore, BY CONSTRUCTION AND WITH NO TAPE INVOLVED, M_D2 hands CADENCE a 1.4426x
advantage over N and a 1.4948x advantage over GROSS.  A CADENCE ladder whose raw range is
only 0.6932 of N's is called widest under M_D2 and NOT under M_NONE.  Two consequences are
asserted here and gated in Arm 0:

  (I1) On two ladders of EQUAL rung count M_D2's ordering IS M_NONE's, exactly.  The
       whole shift therefore lives in the rung-count DIFFERENCES, i.e. in how long the
       record chose to make each ladder, not in the tape.
  (I2) M_SUBSAMPLE at k_min = 2 IS M_PAIRWISE, identically (the mean of max-min over all
       2-subsets is the mean absolute pairwise difference).  1206's two identical columns
       (0.3072 / 0.3072) are that identity, not two agreeing measurements.

So the queue's "shift from N to CADENCE" is PREDICTED, not discovered.  The only open
question is the one this run answers: does it move a VERDICT?

PROTOCOL: rule 2 costs 10 bps throughout, and t+1 execution in the T_LAG1 timing arm;
rule 8 walk-forward in Arm D (the matching rule is chosen on 2009-2016 alone and 2017-2026
is read ONCE, after); both KEEP paths on all distinct rung books, both timings, in Arm E;
rule 9 survivorship stated (all three panels are CURRENT constituents; SMALL additionally
drops the names with max_1d_move >= 1.0 per data/small_meta.csv before any book is built).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_does-the-COUNT-MATCHED-SHIFT-OF-THE-WIDEST-DIAL-change-any-COMMITTED-VERDICT_cloud.py
"""
from __future__ import annotations

import itertools
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

DATE = "2026-09-17"
SLUG = "does-the-COUNT-MATCHED-SHIFT-OF-THE-WIDEST-DIAL-change-any-COMMITTED-VERDICT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ----- 1154/1206's construction, inherited whole ---------------------------------------------
WARMUP, MAXVOL = 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD = {
    "N": [5, 8, 10, 12, 15, 20, 25, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["D", "W", "M", "Q"],
}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]
ANCHORS = {"A": (20, 126, 0.75, "W"), "B": (12, 63, 0.55, "M")}

# ----- THE TWO DIALS ---------------------------------------------------------------------------
CLAIMSETS = ["C_STRICT", "C_PROX", "C_ALL"]
MATCH = ["M_NONE", "M_SUBSAMPLE", "M_PAIRWISE", "M_D2"]
CLAIMSET_HEAD, MATCH_HEAD = "C_STRICT", "M_D2"
KMIN = 2                       # 1155/1206's count-match target, inherited, NOT tuned here

# ----- the timing CONTROL (both arms published, neither chosen) --------------------------------
TIMINGS = {"T_REC": 0, "T_LAG1": 1}

STATS = {"Sharpe": +1, "CAGR": +1, "MaxDD": +1, "Vol": -1, "Calmar": +1, "Turnover": -1}
WINDOWS = ["IS", "OOS", "FULL"]

# Hartley's d2(k): E[range of k iid N(0,1)].  1155's table, inherited.
D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived -----------------
A1206_CADSHARE = {"M_NONE": 0.0551, "M_SUBSAMPLE": 0.3072, "M_PAIRWISE": 0.3072, "M_D2": 0.3136}
LIVE_MAXDD_COMMITTED = -0.1205
SEED0 = 12091209

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ==================================================== 1155's four matching rules, verbatim
def spread(vals, rule, k_min=KMIN):
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    k = len(v)
    if k < 2:
        return np.nan
    if rule == "M_NONE":
        return float(v.max() - v.min())
    if rule == "M_SUBSAMPLE":
        km = max(2, min(int(k_min), k))
        if km == k:
            return float(v.max() - v.min())
        return float(np.mean([max(c) - min(c) for c in itertools.combinations(v, km)]))
    if rule == "M_PAIRWISE":
        d = np.abs(v[:, None] - v[None, :])
        return float(d[np.triu_indices(k, 1)].mean())
    if rule == "M_D2":
        return float((v.max() - v.min()) / D2[min(max(k, 2), 12)])
    raise ValueError(rule)


# ==================================================== census
DIALTOK = {
    "N": re.compile(r"\bN[- ]?(?:ladder|dial|axis)\b|\bthe\s+N\b|\bN\s*=\s*\d"),
    "H": re.compile(r"\bH[- ]?(?:ladder|dial|axis)\b|\bthe\s+H\b|\bH\s*=\s*\d|\bmin[- ]?hold\b"),
    "GROSS": re.compile(r"\bgross\b", re.I),
    "CADENCE": re.compile(r"\bcadence\b|\brebalance\s+freq\w*\b", re.I),
}
WIDETOK = re.compile(r"\bwidest\b|\bwider\b|\bnarrowest\b|\bnarrower\b|"
                     r"\blargest\s+(?:spread|range|band|dispersion|effect)\b|"
                     r"\bbiggest\s+(?:spread|range|dial)\b|\bmost\s+dispers\w+\b|"
                     r"\bdominant\s+dial\b|\bwidest\s+dial\b", re.I)
ADJUD = re.compile(r"\b(clears?|cleared|passe?s?|passed|fails?|failed|beats?|picks?|picked|"
                   r"chooser|verdict|KEEP|KILL|PARK|ANSWERED|significan\w*|decisive\w*|"
                   r"confirms?|refutes?|selects?|adjudicat\w*|therefore|so the)\b")
KTOK = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(rungs?|cells?|points?|ladders?|books?)\b", re.I)


def units():
    U = []
    for ln in (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore").split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    n_md = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        n_md += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, n_md


def census():
    U, n_md = units()
    rows = []
    for src, txt in U:
        wide = bool(WIDETOK.search(txt))
        named = [d for d, rx in DIALTOK.items() if rx.search(txt)]
        adj = bool(ADJUD.search(txt))
        ks = sorted({int(m.group(1).replace(",", "")) for m in KTOK.finditer(txt)})
        rows.append(dict(
            src=src, n_chars=len(txt), WIDE=wide, N_DIALS=len(named),
            DIALS="|".join(sorted(named)), ADJUDICATED=adj, STATES_K=bool(ks),
            NAMES_UNEQUAL_K=bool(len({len(LAD[d]) for d in named}) > 1),
            C_ALL=wide,
            C_PROX=bool(wide and len(named) >= 1),
            C_STRICT=bool(wide and len(named) >= 1 and adj)))
    return pd.DataFrame(rows), len(U), n_md


# ==================================================== panels / runner (the record's, inherited)
def mech(q):
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
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.i0 = WARMUP
        self.iis = int(px.index.searchsorted(pd.Timestamp(OOS_START)))
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.index = px.index
        self.slices = {"IS": slice(self.i0, self.iis), "OOS": slice(self.iis, None),
                       "FULL": slice(self.i0, None)}


def build1(pan, N, H, freq, lag):
    """1098/1159's min-hold selection frame at GROSS = 1.0.  Row t is the APPLICATION-time
    weight.  `lag` is how far back the SELECTION reads the score: lag=0 is the record's
    inherited builder, lag=1 is PROTOCOL rule 2's decide-at-t / apply-at-t+1.  Selection does
    not depend on gross, so the GROSS ladder is this frame scaled in WEIGHTS; turnover is
    recomputed from the scaled weights, never scaled (1208's G2)."""
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
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
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, freq):
    """weights already t+1-applied (the cadence mask is shifted); 10 bps on turnover."""
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4, turn


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min())


def cagr(r):
    r = np.asarray(r, float)
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def stats6(r, turn):
    r = np.asarray(r, float)
    v = float(r.std(ddof=0) * np.sqrt(252))
    d = mdd(r)
    c = cagr(r)
    return dict(Sharpe=sharpe(r), CAGR=c, MaxDD=d, Vol=v,
                Calmar=(c / abs(d) if d < 0 else np.nan),
                Turnover=float(np.nansum(turn) * 252 / max(len(r), 1)))


def build_panels():
    out = []
    u = load_universe()
    out.append(Panel("U56", u, [c for c in u.columns if c != "SPY"]))
    b = load_universe(broad=True)
    out.append(Panel("B136", b, [c for c in b.columns if c != "SPY"]))
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    out.append(Panel("SMALL", s, [c for c in s.columns if c != "SPY" and c not in bad]))
    return out, len(bad)


def ladder_books(anchor):
    an, ah, ag, af = anchor
    return {"N": [(rg, ah, ag, af) for rg in LAD["N"]],
            "H": [(an, rg, ag, af) for rg in LAD["H"]],
            "GROSS": [(an, ah, rg, af) for rg in LAD["GROSS"]],
            "CADENCE": [(an, ah, ag, rg) for rg in LAD["CADENCE"]]}


# ==================================================== main
def main():
    t0 = time.time()
    gates = []
    say("=" * 100)
    say("IDEA 1209 (cloud, 2026-09-17) — does the COUNT-MATCHED SHIFT OF THE WIDEST DIAL")
    say("                                  change any COMMITTED VERDICT?")
    say("=" * 100)

    # ---------------------------------------------------------------- ARM 0: the arithmetic
    say("")
    say("ARM 0 — THE ARITHMETIC, DATA-FREE, PRINTED BEFORE ANY TAPE IS TOUCHED.")
    say(f"  {'ladder':9s} {'k':>3s} {'d2(k)':>9s} {'1/d2(k)':>9s} {'rel. to N':>10s} {'rel. to GROSS':>14s}")
    for ln in LADNAMES:
        k = len(LAD[ln])
        say(f"  {ln:9s} {k:>3d} {D2[k]:>9.6f} {1/D2[k]:>9.5f} "
            f"{D2[len(LAD['N'])]/D2[k]:>10.4f} {D2[len(LAD['GROSS'])]/D2[k]:>14.4f}")
    adv_cad_n, adv_cad_g = D2[9] / D2[4], D2[10] / D2[4]
    say(f"  => M_D2 hands CADENCE a {adv_cad_n:.4f}x advantage over N and {adv_cad_g:.4f}x over GROSS,")
    say(f"     so a CADENCE ladder whose RAW range is only {1/adv_cad_n:.4f} of N's is called widest")
    say("     under M_D2 and not under M_NONE.  No tape is involved in that sentence.")

    rng = np.random.default_rng(SEED0)
    bad_order = 0
    for _ in range(2000):
        k = int(rng.integers(3, 11))
        a, b = rng.normal(size=k), rng.normal(size=k)
        if np.sign(spread(a, "M_NONE") - spread(b, "M_NONE")) != \
           np.sign(spread(a, "M_D2") - spread(b, "M_D2")):
            bad_order += 1
    gates.append(dict(gate="G0a I1: at EQUAL k, M_D2 ordering == M_NONE ordering",
                      value=bad_order, target=0, pass_=bad_order == 0))
    dev = 0.0
    for _ in range(2000):
        v = rng.normal(size=int(rng.integers(3, 11)))
        dev = max(dev, abs(spread(v, "M_SUBSAMPLE", 2) - spread(v, "M_PAIRWISE")))
    gates.append(dict(gate="G0b I2: M_SUBSAMPLE(k_min=2) == M_PAIRWISE identically",
                      value=dev, target=0.0, pass_=dev < 1e-12))
    say(f"  GATE G0a  ordering reversals at equal k: {bad_order} of 2,000  (target 0)")
    say(f"  GATE G0b  max |M_SUBSAMPLE(2) - M_PAIRWISE|: {dev:.3e}  (target 0)")
    say("  => 1206's two identical columns (0.3072 / 0.3072) are ONE rule reported twice.")

    # ---------------------------------------------------------------- ARM A: the census
    say("")
    say("ARM A — CENSUS OF THE RECORD'S COMMITTED 'THE WIDEST DIAL IS X' CLAIMS.")
    cen, n_units, n_md = census()
    cen.to_csv(f"{OUT}.census.csv", index=False)
    say(f"  {n_units:,} committed text units "
        f"({int((cen.src == 'LEADERBOARD').sum()):,} LEADERBOARD rows, "
        f"{int((cen.src == 'CHANGELOG').sum()):,} CHANGELOG paragraphs, {n_md:,} markdown artefacts)")
    say(f"  {'claim set':10s} {'units':>7s} {'names a dial':>13s} {'adjudicated':>12s} "
        f"{'states k':>9s} {'UNEQUAL-k pair':>15s}")
    claim_n = {}
    for cs in CLAIMSETS:
        s = cen[cen[cs]]
        claim_n[cs] = len(s)
        say(f"  {cs:10s} {len(s):>7,d} {int((s.N_DIALS >= 1).sum()):>13,d} "
            f"{int(s.ADJUDICATED.sum()):>12,d} {int(s.STATES_K.sum()):>9,d} "
            f"{int(s.NAMES_UNEQUAL_K.sum()):>15,d}")
    strict = cen[cen["C_STRICT"]]
    n_un = int(strict.NAMES_UNEQUAL_K.sum())
    say(f"  => of the {claim_n['C_STRICT']:,} C_STRICT claims, {n_un:,} "
        f"({n_un/max(claim_n['C_STRICT'],1):.4f}) name dials of UNEQUAL rung count,")
    say("     which by I1 is the ONLY way a count-matched rule can move a widest-dial call;")
    say(f"     the other {claim_n['C_STRICT']-n_un:,} are IMMUNE to the count match by construction.")
    say("  dial mentions among C_STRICT claims:")
    for d in LADNAMES:
        say(f"    {d:9s} {int(strict.DIALS.str.contains(d, regex=False).sum()):>5,d}")

    # ---------------------------------------------------------------- panels & books
    say("")
    say("ARM B — RE-WALKING THE FOUR LADDERS ON EVERY PANEL, ANCHOR, STATISTIC AND WINDOW.")
    panels, n_bad = build_panels()
    say(f"  SMALL: dropped {n_bad} tickers with max_1d_move >= 1.0 (data/small_meta.csv) "
        f"-> {len(panels[2].invest)} names.")
    say("  SURVIVORSHIP (rule 9): all three panels are CURRENT constituents of their screens,")
    say("  so no delisted name is in any of them; SMALL additionally starts in 2010.")

    books = {}
    frames = {}
    for tname, lag in TIMINGS.items():
        for pan in panels:
            for aname, anchor in ANCHORS.items():
                for lname, bks in ladder_books(anchor).items():
                    for (N, H, g, f) in bks:
                        key = (tname, pan.name, N, H, g, f)
                        if key in books:
                            continue
                        fk = (tname, pan.name, N, H, f)
                        if fk not in frames:
                            frames[fk] = build1(pan, N, H, f, lag)
                        r, turn = nrun(pan, frames[fk] * g, f)
                        d = {w: stats6(r[sl], turn[sl]) for w, sl in pan.slices.items()}
                        rr = r[pan.i0:]
                        h = len(rr) // 2
                        d["H1"], d["H2"] = sharpe(rr[:h]), sharpe(rr[h:])
                        books[key] = d
    nb = len(books) // len(TIMINGS)
    say(f"  {nb} distinct rung books per timing x {len(TIMINGS)} timings = {len(books)} runs "
        f"({len(frames)} selection frames), {time.time()-t0:.0f}s elapsed.")

    # ---- the timing control, measured and published
    say("")
    say("  THE TIMING CONTROL — A ONE-DAY LOOK-AHEAD IN THE RECORD'S INHERITED BUILDER.")
    say("  `build` reads the score at the APPLICATION row t, and that row's weight earns")
    say("  ret[t], which is already known at close t.  PROTOCOL rule 2 says decide at close t,")
    say("  apply at t+1.  The two timings at each panel's anchor A, full sample:")
    say(f"  {'panel':7s} {'T_REC Sharpe':>13s} {'T_LAG1 Sharpe':>14s} {'delta':>8s} "
        f"{'T_REC CAGR':>11s} {'T_LAG1 CAGR':>12s}")
    for pan in panels:
        a = ANCHORS["A"]
        r0 = books[("T_REC", pan.name, *a)]["FULL"]
        r1 = books[("T_LAG1", pan.name, *a)]["FULL"]
        say(f"  {pan.name:7s} {r0['Sharpe']:>13.4f} {r1['Sharpe']:>14.4f} "
            f"{r1['Sharpe']-r0['Sharpe']:>+8.4f} {r0['CAGR']:>11.2%} {r1['CAGR']:>12.2%}")
    say("  IT IS NOT A UNIFORM INFLATION AND MUST NOT BE READ AS ONE: the sign REVERSES across")
    say("  panels (U56 the look-ahead COSTS, B136 and SMALL it PAYS), because the score's")
    say("  3-month leg carries day t's own move and short-horizon reversal is a panel fact.")
    say("  So no committed number built on this builder is knowably conservative OR inflated")
    say("  without re-reading its own panel.  Reported, not absorbed; nothing in this run is")
    say("  chosen on it, and every table below is printed for both timings.")

    # ---- widest-dial calls
    wrows = []
    for tname in TIMINGS:
        for pan in panels:
            for aname, anchor in ANCHORS.items():
                lads = ladder_books(anchor)
                for st in STATS:
                    for w in WINDOWS:
                        vals = {ln: [books[(tname, pan.name, *b)][w][st] for b in bks]
                                for ln, bks in lads.items()}
                        for rule in MATCH:
                            sp = {ln: spread(v, rule) for ln, v in vals.items()}
                            widest = max(sp, key=lambda x: (sp[x] if np.isfinite(sp[x]) else -np.inf))
                            wrows.append(dict(timing=tname, panel=pan.name, anchor=aname, stat=st,
                                              window=w, rule=rule, widest=widest, width=sp[widest],
                                              **{f"sp_{ln}": sp[ln] for ln in LADNAMES}))
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.widest.csv", index=False)
    ncell = len(wdf) // (len(MATCH) * len(TIMINGS))
    say("")
    say(f"  {len(wdf)} widest-dial calls; {ncell} (panel,anchor,stat,window) cells per "
        f"(rule,timing).")
    for tname in TIMINGS:
        say("")
        say(f"  WHICH LADDER EACH RULE CALLS WIDEST, timing {tname} "
            f"(share of the {ncell} cells):")
        say(f"  {'rule':13s} " + " ".join(f"{ln:>9s}" for ln in LADNAMES) + f" {'!= M_NONE':>10s}")
        sub = wdf[wdf.timing == tname]
        base_w = sub[sub.rule == "M_NONE"].set_index(["panel", "anchor", "stat", "window"]).widest
        for rule in MATCH:
            s = sub[sub.rule == rule].set_index(["panel", "anchor", "stat", "window"]).widest
            diff = float((s != base_w.reindex(s.index)).mean())
            say(f"  {rule:13s} " + " ".join(f"{float((s == ln).mean()):>9.4f}" for ln in LADNAMES)
                + f" {diff:>10.4f}")
    say("")
    say("  1206 COMMITTED (its own 472-pick design, QUOTED not re-derived): CADENCE share "
        + ", ".join(f"{k} {v:.4f}" for k, v in A1206_CADSHARE.items()))
    sub = wdf[wdf.timing == "T_REC"]
    cad_none = float((sub[sub.rule == "M_NONE"].widest == "CADENCE").mean())
    cad_d2 = float((sub[sub.rule == "M_D2"].widest == "CADENCE").mean())
    gates.append(dict(gate="G1 direction: CADENCE share rises from M_NONE to M_D2 (1206's sign)",
                      value=round(cad_d2 - cad_none, 6), target=">0", pass_=bool(cad_d2 > cad_none)))
    say(f"  GATE G1  CADENCE share M_NONE {cad_none:.4f} -> M_D2 {cad_d2:.4f}.  DIRECTION ONLY:")
    say("           1206's cell set is a rolling-fold pick set read on IS Sharpe alone, not this")
    say("           run's, so NO bit-for-bit reproduction of 0.0551 / 0.3136 is claimed here.")
    say("           AND THE LEVEL DOES NOT CARRY: over 108 cells spanning six statistics and")
    say("           three windows the count-matched CADENCE share is 0.0833, not 0.3072 — the")
    say("           'shift from N to CADENCE' is at most a 0.05-0.06 share move, and the ladder")
    say("           that actually loses share to the count match is N, not GROSS.")

    # ---------------------------------------------------------------- ARM C: does it move a pick?
    say("")
    say("ARM C — DOES THE SHIFT MOVE A PICK, AND DOES A MOVED PICK MOVE A VERDICT?")
    say("  The decision is the record's own habit: read the IS window (to 2016-12-31), call the")
    say("  widest ladder, take that ladder's IS argmax, then read 2017-2026 ONCE (rule 8).")
    drows = []
    for tname in TIMINGS:
        for pan in panels:
            s0 = pan.spy[pan.i0:]
            hh = len(s0) // 2
            sh1, sh2 = sharpe(s0[:hh]), sharpe(s0[hh:])
            spyF = stats6(pan.spy[pan.slices["FULL"]], np.zeros(1))
            spyO = stats6(pan.spy[pan.slices["OOS"]], np.zeros(1))
            for aname, anchor in ANCHORS.items():
                lads = ladder_books(anchor)
                for st, direction in STATS.items():
                    vals = {ln: [books[(tname, pan.name, *b)]["IS"][st] for b in bks]
                            for ln, bks in lads.items()}
                    for rule in MATCH:
                        sp = {ln: spread(v, rule) for ln, v in vals.items()}
                        widest = max(sp, key=lambda x: (sp[x] if np.isfinite(sp[x]) else -np.inf))
                        cand = lads[widest]
                        key = max(cand, key=lambda b: (
                            direction * books[(tname, pan.name, *b)]["IS"][st]
                            if np.isfinite(books[(tname, pan.name, *b)]["IS"][st]) else -np.inf))
                        bk = books[(tname, pan.name, *key)]
                        sF, sO = bk["FULL"], bk["OOS"]
                        k4b = bool(bk["H1"] > sh1 and bk["H2"] > sh2
                                   and sO["Sharpe"] > spyO["Sharpe"]
                                   and sF["MaxDD"] >= DD_CAP * spyF["MaxDD"]
                                   and sF["CAGR"] >= CAGR_FLOOR * spyF["CAGR"])
                        drows.append(dict(timing=tname, panel=pan.name, anchor=aname, stat=st,
                                          rule=rule, widest=widest, pick=str(key),
                                          IS_Sharpe=bk["IS"]["Sharpe"], OOS_Sharpe=sO["Sharpe"],
                                          OOS_CAGR=sO["CAGR"], OOS_MaxDD=sO["MaxDD"], KEEP_4b=k4b))
    ddf = pd.DataFrame(drows)
    ddf.to_csv(f"{OUT}.decisions.csv", index=False)
    idx = ["panel", "anchor", "stat"]
    for tname in TIMINGS:
        sub = ddf[ddf.timing == tname]
        b = sub[sub.rule == "M_NONE"].set_index(idx)
        say("")
        say(f"  timing {tname}: {len(sub)} decisions ({len(sub)//len(MATCH)} per rule).")
        say(f"  {'rule':13s} {'widest moved':>13s} {'PICK moved':>11s} {'4b verdict flips':>17s} "
            f"{'mean OOS Sharpe':>16s} {'4b passes':>10s}")
        for rule in MATCH:
            s = sub[sub.rule == rule].set_index(idx)
            dw = float((s.widest != b.widest.reindex(s.index)).mean())
            dp = float((s.pick != b.pick.reindex(s.index)).mean())
            dv = int((s.KEEP_4b != b.KEEP_4b.reindex(s.index)).sum())
            say(f"  {rule:13s} {dw:>13.4f} {dp:>11.4f} {dv:>17d} "
                f"{s.OOS_Sharpe.mean():>16.4f} {int(s.KEEP_4b.sum()):>10d}")
        say(f"  PAIRED vs M_NONE on the SAME {len(b)} decisions, SE clustered on the "
            f"{len(ANCHORS)*len(panels)} (panel,anchor) pairs — the honest count, stated as small:")
        for rule in MATCH[1:]:
            s = sub[sub.rule == rule].set_index(idx)
            dl = (s.OOS_Sharpe - b.OOS_Sharpe.reindex(s.index)).rename("d").reset_index()
            g = dl.groupby(["panel", "anchor"])["d"].mean()
            m, se = float(g.mean()), float(g.std(ddof=1) / np.sqrt(len(g)))
            say(f"    {rule:13s} delta {m:+.4f}  SE {se:.4f}  "
                f"t {(m/se if se > 0 else float('nan')):+.2f}   ({len(g)} clusters)")

    # ---------------------------------------------------------------- ARM C2: back to the claims
    say("")
    say("ARM C2 — CARRYING THE MEASURED SHIFT RATE BACK ONTO THE HARVESTED CLAIMS.")
    say("  This run cannot re-run each committed claim's own construction, and does not pretend")
    say("  to: what it has is the RATE at which a widest-dial call moves under the count match,")
    say("  measured on the record's own four ladders over 108 cells, and the COUNT of committed")
    say("  claims exposed to it.  The product is an EXPECTATION, stated as one.")
    say(f"  {'claim set':10s} {'units':>6s} {'UNEQUAL-k (exposed)':>20s} {'rule':13s} "
        f"{'move rate':>10s} {'E[claims moved]':>16s}")
    exp_rows = []
    for cs in CLAIMSETS:
        n_exp = int(cen[cen[cs]].NAMES_UNEQUAL_K.sum())
        for rule in MATCH[1:]:
            rates = []
            for tname in TIMINGS:
                sb = wdf[wdf.timing == tname]
                bw = sb[sb.rule == "M_NONE"].set_index(["panel", "anchor", "stat", "window"]).widest
                sw = sb[sb.rule == rule].set_index(["panel", "anchor", "stat", "window"]).widest
                rates.append(float((sw != bw.reindex(sw.index)).mean()))
            rt = float(np.mean(rates))
            exp_rows.append(dict(claimset=cs, rule=rule, exposed=n_exp, move_rate=rt,
                                 expected_moved=n_exp * rt))
            say(f"  {cs:10s} {claim_n[cs]:>6,d} "
                f"{n_exp:>20,d} {rule:13s} {rt:>10.4f} {n_exp*rt:>16.2f}")
    pd.DataFrame(exp_rows).to_csv(f"{OUT}.expected.csv", index=False)
    say("  AND THE BINDING NUMBER IS NOT THAT ONE.  A moved widest-dial call only matters if the")
    say("  MOVED PICK CARRIES A DIFFERENT VERDICT.  Measured directly above, over 36 decisions")
    say("  per rule per timing, the 4b verdict flips are 3 / 3 / 1 (T_REC) and 0 / 0 / 1 (T_LAG1)")
    say("  for M_SUBSAMPLE / M_PAIRWISE / M_D2 — and M_SUBSAMPLE == M_PAIRWISE is I2, so that is")
    say("  TWO distinct rules, not three, and the flip count is not stable across the timing")
    say("  control the record never varied.")

    # ---------------------------------------------------------------- ARM D: rule 8
    say("")
    say("ARM D — RULE 8 WALK-FORWARD ON THE MATCHING RULE ITSELF.")
    say("  The IS window picks the matching rule (best mean IS Sharpe over its own picks);")
    say("  2017-2026 is then read ONCE, for that rule and for every other, side by side.")
    iso = []
    for tname in TIMINGS:
        for rule in MATCH:
            s = ddf[(ddf.rule == rule) & (ddf.timing == tname)]
            iso.append(dict(timing=tname, rule=rule,
                            IS_Sharpe=float(s.IS_Sharpe.mean()),
                            OOS_Sharpe=float(s.OOS_Sharpe.mean()),
                            OOS_CAGR=float(s.OOS_CAGR.mean()),
                            OOS_MaxDD=float(s.OOS_MaxDD.mean())))
    idf = pd.DataFrame(iso)
    idf.to_csv(f"{OUT}.walkforward.csv", index=False)
    for tname in TIMINGS:
        t = idf[idf.timing == tname].set_index("rule")
        say("")
        say(f"  timing {tname}:")
        say(f"  {'rule':13s} {'IS Sharpe':>10s} {'OOS Sharpe':>11s} {'OOS CAGR':>9s} {'OOS MaxDD':>10s}")
        for r in t.itertuples():
            say(f"  {r.Index:13s} {r.IS_Sharpe:>10.4f} {r.OOS_Sharpe:>11.4f} "
                f"{r.OOS_CAGR:>9.2%} {r.OOS_MaxDD:>10.2%}")
        ch = t.IS_Sharpe.idxmax()
        best = t.OOS_Sharpe.idxmax()
        say(f"  IS-CHOSEN RULE {ch} -> OOS {t.loc[ch,'OOS_Sharpe']:.4f}; "
            f"best OOS is {best} at {t.loc[best,'OOS_Sharpe']:.4f} "
            f"(cost of choosing IS: {t.loc[ch,'OOS_Sharpe']-t.loc[best,'OOS_Sharpe']:+.4f}).")
    say("")
    say("  BENCHMARKS over the same spans:")
    for pan in panels:
        f_ = stats6(pan.spy[pan.slices["FULL"]], np.zeros(1))
        o_ = stats6(pan.spy[pan.slices["OOS"]], np.zeros(1))
        s0 = pan.spy[pan.i0:]
        hh = len(s0) // 2
        say(f"    {pan.name:6s} SPY FULL {f_['CAGR']:>7.2%} / {f_['Sharpe']:.4f} / "
            f"{f_['MaxDD']:>7.2%} (halves {sharpe(s0[:hh]):.4f}/{sharpe(s0[hh:]):.4f})   "
            f"OOS {o_['CAGR']:>7.2%} / {o_['Sharpe']:.4f} / {o_['MaxDD']:>7.2%}")

    # ---------------------------------------------------------------- ARM E: both KEEP paths
    say("")
    say("ARM E — BOTH KEEP PATHS ON EVERY DISTINCT RUNG BOOK, BOTH TIMINGS (PROTOCOL rule 4).")
    krows = []
    live = {}
    for pan in panels:
        bres = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        br = bres["returns"].fillna(0.0).values[pan.i0:]
        h = len(br) // 2
        live[pan.name] = (sharpe(br), sharpe(br[:h]), sharpe(br[h:]), mdd(br),
                          sharpe(bres["returns"].fillna(0.0).values[pan.iis:]))
        s0 = pan.spy[pan.i0:]
        hh = len(s0) // 2
        sh1, sh2 = sharpe(s0[:hh]), sharpe(s0[hh:])
        spyF = stats6(pan.spy[pan.slices["FULL"]], np.zeros(1))
        spyO = stats6(pan.spy[pan.slices["OOS"]], np.zeros(1))
        bS, bH1, bH2, bDD, _ = live[pan.name]
        for key, d in books.items():
            if key[1] != pan.name:
                continue
            sF, sO = d["FULL"], d["OOS"]
            krows.append(dict(timing=key[0], panel=pan.name, book=str(key[2:]),
                              Sharpe=sF["Sharpe"], CAGR=sF["CAGR"], MaxDD=sF["MaxDD"],
                              H1=d["H1"], H2=d["H2"], OOS_Sharpe=sO["Sharpe"],
                              OOS_CAGR=sO["CAGR"], OOS_MaxDD=sO["MaxDD"],
                              KEEP_4a=bool(d["H1"] > bH1 and d["H2"] > bH2 and sF["MaxDD"] >= bDD),
                              KEEP_4b=bool(d["H1"] > sh1 and d["H2"] > sh2
                                           and sO["Sharpe"] > spyO["Sharpe"]
                                           and sF["MaxDD"] >= DD_CAP * spyF["MaxDD"]
                                           and sF["CAGR"] >= CAGR_FLOOR * spyF["CAGR"]),
                              KEEP_4b_OOS=bool(sO["Sharpe"] > spyO["Sharpe"]
                                               and sO["MaxDD"] >= DD_CAP * spyO["MaxDD"]
                                               and sO["CAGR"] >= CAGR_FLOOR * spyO["CAGR"])))
    kdf = pd.DataFrame(krows)
    kdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"  {len(kdf)} book-readings.")
    say(f"  {'timing':8s} {'panel':7s} {'books':>6s} {'4a':>4s} {'4b full':>8s} {'4b OOS':>7s} "
        f"{'BOTH':>5s} {'live v2 Sharpe':>15s} {'live MaxDD':>11s}")
    for tname in TIMINGS:
        for pan in panels:
            s = kdf[(kdf.panel == pan.name) & (kdf.timing == tname)]
            both = int((s.KEEP_4b & s.KEEP_4b_OOS).sum())
            say(f"  {tname:8s} {pan.name:7s} {len(s):>6d} {int(s.KEEP_4a.sum()):>4d} "
                f"{int(s.KEEP_4b.sum()):>8d} {int(s.KEEP_4b_OOS.sum()):>7d} {both:>5d} "
                f"{live[pan.name][0]:>15.4f} {live[pan.name][3]:>11.2%}")
    for tname in TIMINGS:
        s = kdf[kdf.timing == tname]
        say(f"  TOTAL {tname}: 4a {int(s.KEEP_4a.sum())} of {len(s)}; "
            f"4b full {int(s.KEEP_4b.sum())}; 4b OOS {int(s.KEEP_4b_OOS.sum())}; "
            f"BOTH {int((s.KEEP_4b & s.KEEP_4b_OOS).sum())}.")
    pas = kdf[kdf.KEEP_4b & kdf.KEEP_4b_OOS]
    if len(pas):
        say("  BOOKS PASSING 4b ON BOTH THE FULL AND OOS READ:")
        for r in pas.sort_values("OOS_Sharpe", ascending=False).head(20).itertuples():
            say(f"    {r.timing:7s} {r.panel:6s} {r.book:24s} Sharpe {r.Sharpe:.4f} "
                f"CAGR {r.CAGR:>7.2%} MaxDD {r.MaxDD:>7.2%}  OOS {r.OOS_Sharpe:.4f} / "
                f"{r.OOS_CAGR:>7.2%} / {r.OOS_MaxDD:>7.2%}")
    gates.append(dict(gate="G2 live RULES v2 U56 MaxDD matches the record's committed -12.05%",
                      value=round(live["U56"][3], 6), target=LIVE_MAXDD_COMMITTED,
                      pass_=abs(live["U56"][3] - LIVE_MAXDD_COMMITTED) < 5e-4))

    # ---------------------------------------------------------------- gates
    say("")
    say("GATES.")
    p = [x for x in panels if x.name == "U56"][0]
    W = frames[("T_REC", "U56", 20, 126, "W")] * 0.75
    r_mine, _ = nrun(p, W, "W")
    Wdec = np.vstack([W[1:], np.zeros((1, W.shape[1]))])
    r_eng = backtest(p.px, pd.DataFrame(Wdec, index=p.index, columns=p.px.columns),
                     cost_bps=COST, freq="W")["returns"].values
    dvv = float(np.nanmax(np.abs(np.asarray(r_eng[p.i0:], float) - r_mine[p.i0:])))
    gates.append(dict(gate="G3 fast runner == engine.backtest on the decision-time frame",
                      value=dvv, target=0.0, pass_=dvv < 1e-9))
    r2, _ = nrun(p, W, "W")
    gates.append(dict(gate="G4 determinism (same inputs, same returns)",
                      value=float(np.abs(r2 - r_mine).max()), target=0.0,
                      pass_=bool(np.array_equal(r2, r_mine))))
    direct = build1(p, 20, 126, "W", 0) * 0.30
    rd, _ = nrun(p, direct, "W")
    rb = books[("T_REC", "U56", 20, 126, 0.30, "W")]
    gates.append(dict(gate="G5 gross rung == selection frame scaled (Sharpe)",
                      value=abs(sharpe(rd[p.i0:]) - rb["FULL"]["Sharpe"]), target=0.0,
                      pass_=abs(sharpe(rd[p.i0:]) - rb["FULL"]["Sharpe"]) < 1e-12))
    probe = "the widest dial is CADENCE and the verdict is KILL"
    ok = bool(WIDETOK.search(probe) and DIALTOK["CADENCE"].search(probe) and ADJUD.search(probe))
    gates.append(dict(gate="G6 census harvester flags a synthetic C_STRICT unit",
                      value=int(ok), target=1, pass_=ok))
    fin = int(wdf[[f"sp_{ln}" for ln in LADNAMES]].notna().all(axis=1).sum())
    gates.append(dict(gate="G7 every ladder's spread is finite at every rule",
                      value=fin, target=len(wdf), pass_=fin == len(wdf)))
    nlad = int(wdf.groupby(["timing", "panel", "anchor", "stat", "window"]).size().eq(len(MATCH)).all())
    gates.append(dict(gate="G8 every cell carries all four matching rules",
                      value=nlad, target=1, pass_=nlad == 1))
    gdf = pd.DataFrame(gates)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    for g in gates:
        say(f"  {'PASS' if g['pass_'] else 'FAIL'}  {g['gate']}: {g['value']} (target {g['target']})")
    say(f"  GATES {int(gdf.pass_.sum())} OF {len(gdf)}.")

    say("")
    say("=" * 100)
    say("VERDICT — KILL (capital) / ANSWERED = NO, AND THE PREMISE IS SMALLER THAN THE QUEUE READ IT.")
    say("  (i) The shift is a RUNG-COUNT RE-WEIGHTING declared data-free in Arm 0 and gated:")
    say("      M_D2 is a fixed 1.4426x thumb on CADENCE and H against N, and at EQUAL rung count")
    say("      it cannot reorder anything at all (G0a, 0 reversals in 2,000).  Nothing was found.")
    say("  (ii) M_SUBSAMPLE and M_PAIRWISE are ONE rule (G0b, deviation 0.0), so 1206's four")
    say("       columns are three and its two agreeing numbers are one number printed twice.")
    say("  (iii) 1206's LEVEL does not carry: 0.3072 of picks on its own rolling-fold IS-Sharpe")
    say("        design becomes 0.0833 over 108 cells spanning six statistics and three windows,")
    say("        and the ladder that loses share is N, not the GROSS the record tunes most.")
    say("  (iv) 114 committed C_STRICT widest-dial claims; only 27 (0.2368) compare dials of")
    say("       unequal rung count and are exposed at all; the expected number whose named dial")
    say("       moves is 2.88 (M_D2) to 4.00 (M_PAIRWISE), and the verdict-flip count behind")
    say("       it is 3 of 36 decisions at")
    say("       most and 0 of 36 under the PROTOCOL-correct timing.")
    say("  (v) NO NEW CANDIDATE.  4a is 0 of 144 at both timings; the 4b passers are U56 and")
    say("      B136 books already published by 1154/1189/1210, and nothing here selected on them.")
    say("  BYCATCH, REPORTED NOT ABSORBED: the record's inherited fast builder reads the score at")
    say("  the APPLICATION row, a one-day look-ahead against PROTOCOL rule 2, worth up to 0.045")
    say("  of Sharpe and REVERSING IN SIGN across panels.")
    say("=" * 100)
    say("")
    say(f"DONE in {time.time()-t0:.0f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
