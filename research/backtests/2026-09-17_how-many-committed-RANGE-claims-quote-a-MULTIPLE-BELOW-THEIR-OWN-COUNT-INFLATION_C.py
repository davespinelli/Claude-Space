#!/usr/bin/env python3
"""
Idea 1207 (lane C, 2026-09-17) — how many committed RANGE claims quote a MULTIPLE BELOW THEIR
OWN COUNT INFLATION, and were ADJUDICATED ON IT?

THE PREMISE, READ FROM THE RECORD AND NOT RECALLED.  Idea 1155 re-expressed every committed
text unit that states BOTH a multiple and two different point counts against the inflation
d2(k_max)/d2(k_min) that the count difference alone buys, and found the SMALLEST quoted
multiple survives at only 54 of 90 checkable C_STRICT units (0.6000).  It did NOT trace the
other 36 to the VERDICTS they supported.  This run does exactly that: follow each failing
multiple to the claim it carries, re-read that claim with the multiple set to no effect, and
report how many committed verdicts change.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET      {C_STRICT, C_PROX, C_ALL}      -- 1155/1197/1199's nesting convention, inherited
  NO-EFFECT RULE {R_MIN, R_MAX, R_BAND}         -- WHICH quoted multiple the verdict rests on

  R_MIN   the verdict rests on the SMALLEST multiple in the unit (1155's own headline leg:
          the weakest leg of a claim must survive).
  R_MAX   the verdict rests on the LARGEST multiple (the reading most generous to the author;
          1155 published this leg too, at 73 of 90).
  R_BAND  where the unit quotes an explicit "x to y x" BAND the verdict rests on the band
          FLOOR (1155's own G0b treatment of 1140's "1.7x - 61x"); otherwise the smallest.

  9 cells, EVERY ONE PUBLISHED.  Nothing is selected on.

WHAT IS NOT A DIAL, AND WHY (Arm 0 proves it before any text is read).  The SUBSTITUTION
CONVENTION -- what value a failing multiple is set to -- looks like a third dial and is not
one.  For a published multiple M and its inflation I, the count-matched multiple is M/I and
the comparative the verdict rests on is "M/I > 1".  Substituting M' = 1 kills it for every
unit (1/I < 1 whenever k_max > k_min); substituting M' = I kills it for every unit (I/I = 1);
substituting M' = M/I kills it exactly where M <= I.  So EVERY substitution convention is the
SAME THRESHOLD AT I and carries no information of its own.  It is proved as gate G3 and never
walked as a grid.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the record's own four
ladders N (6 rungs) / H (4) / GROSS (10) / CADENCE (2), inherited whole from 1082/1098/1101/
1148/1155/1159; the DOMAIN split (below); the four choosers in Arm B; the 4a and 4b legs.

THE DOMAIN SPLIT, WHICH IS THE ANSWER'S MECHANISM AND NOT A TUNED CHOICE.  Hartley's d2(k) is
tabulated for k = 2..12 and the longest ladder this record has ever published is 10 rungs.
1155's count harvest reads ANY "<n> rungs / cells / points / books / rows / panels" token in
the unit, so a unit whose largest such token is "19,440 books" or "4,608 arm-rows" has its
inflation computed at the CLIPPED value d2(12)/d2(k_min) -- a constant with no relation to the
claim.  Units whose harvested counts fall outside the table's domain are therefore VACUOUS,
not failing, and are reported separately and never merged into the answer.  Every IN-DOMAIN
unit is hand-read, one line each, and the reads are published in the .audit.csv.

Frozen at the record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 / CADENCE=W, 10 bps (rule 2),
DECIDE-AT-t / APPLY-AT-t+1 selection (lag=1 -- idea 1209's correction to the record's
inherited builder, which read the score at the application row), warm-up 260 rows.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward in Arm B with the choice made on
the IS window ONLY and the OOS window read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs
SPY) on every book and every stitched chooser curve; rule 9 survivorship stated.  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_how-many-committed-RANGE-claims-quote-a-MULTIPLE-BELOW-THEIR-OWN-COUNT-INFLATION_C.py
"""
from __future__ import annotations

import hashlib
import re
import subprocess
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
SLUG = "how-many-committed-RANGE-claims-quote-a-MULTIPLE-BELOW-THEIR-OWN-COUNT-INFLATION"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
LADK = {"N": 6, "H": 4, "GROSS": 10, "CADENCE": 2}
CLAIMSETS = ["C_STRICT", "C_PROX", "C_ALL"]
NORULES = ["R_MIN", "R_MAX", "R_BAND"]
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
REPLAY_REV = "4ee8b6f~1"          # the commit 1155's census was computed on (its own parent)
MC_SEED = 12071207

# Hartley's d2(k): E[range of k iid N(0,1)].  Published constants, gated against Monte Carlo.
# TABULATED FOR k = 2..12 ONLY -- that domain is what makes the VACUOUS class exist.
D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}
KMAXD2 = 12

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def d2(k):
    return D2[min(max(int(k), 2), KMAXD2)]


# ==================================================================== census (1155's, verbatim)
SPREADTOK = re.compile(r"\b(spread|band|range|max[- ]?minus[- ]?min|widest|narrowest|"
                       r"wider|narrower|dispersion|max\s*-\s*min|from\s+[-\d.]+\s*(?:to|-)\s*[-\d.]+)\b",
                       re.I)
MULT = re.compile(r"(\d+(?:\.\d+)?)\s*x\b", re.I)
ADJUD = re.compile(r"\b(clears?|cleared|passe?s?|passed|fails?|failed|beats?|picks?|picked|"
                   r"chooser|verdict|KEEP|KILL|PARK|significan\w*|decisive\w*|confirms?|"
                   r"refutes?|ranks?|ranked|selects?|adjudicat\w*|widest|largest|dominat\w*)\b")
KTOK = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(rungs?|cells?|points?|ladders?|arms?|books?|"
                  r"anchors?|rows?|panels?|statistics?|families|families of)\b", re.I)
RANGEPAIR = re.compile(r"(\d+(?:\.\d+)?)\s*x\s*(?:-|to|–|—)\s*(\d+(?:\.\d+)?)\s*x", re.I)
# this run's own additions, used for the TRACE only -- they never change the census sets
VERD = re.compile(r"\bANSWERED\s*=|\bKEEP-?candidate\b|\bKEEP\b|\bKILL\b|\bPARK\b|\bPROMOTED\b|"
                  r"\bCONFIRM\w*\b|\bREFUT\w*\b|\bFALSIFIED\b|\bADOPT\w*\b", re.I)
COMP = re.compile(r"\b(widest|narrowest|wider|narrower|longer|shorter|largest|smallest|biggest|"
                  r"spans?|dominat\w*|outweigh\w*|exceeds?|more than|comparable size|"
                  r"times (?:as|larger|wider|bigger|more|deeper))\b", re.I)


def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True, check=True).stdout


def units_at(rev=None):
    """The record's committed text units.  rev=None reads the working tree (HEAD's content);
    a rev reads that commit's tree, which is how the 1155 replay gate is made exact."""
    U = []
    if rev is None:
        lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
        cl = (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")
        mds = [(f.name, f.read_text(errors="ignore"))
               for f in sorted((ROOT / "research" / "backtests").rglob("*.md"))]
    else:
        lb = _git("show", f"{rev}:research/LEADERBOARD.md")
        cl = _git("show", f"{rev}:research/CHANGELOG.md")
        names = [l for l in _git("ls-tree", "-r", "--name-only", rev,
                                 "research/backtests").split("\n") if l.endswith(".md")]
        mds = [(Path(n).name, _git("show", f"{rev}:{n}")) for n in sorted(names)]
    for ln in lb.split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in cl.split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    for name, text in mds:
        for para in text.split("\n\n"):
            if para.strip():
                U.append((name, para))
    return U, len(mds)


def census(U):
    """1155's census, regex for regex, plus this run's TRACE fields (which do not touch the
    claim-set definitions).  uid is content-addressed so the audit table survives corpus drift."""
    fileset = {}
    for src, txt in U:
        fileset.setdefault(src, False)
        if SPREADTOK.search(txt):
            fileset[src] = True
    rows = []
    for src, txt in U:
        sp = bool(SPREADTOK.search(txt))
        mults = [float(m.group(1)) for m in MULT.finditer(txt)]
        ks = sorted({int(m.group(1).replace(",", "")) for m in KTOK.finditer(txt)})
        pairs = [(float(a), float(b)) for a, b in RANGEPAIR.findall(txt)]
        rows.append(dict(
            uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10],
            src=src, n_chars=len(txt),
            C_STRICT=sp and bool(mults) and bool(ADJUD.search(txt)),
            C_PROX=sp and bool(mults),
            C_ALL=fileset[src] and sp,
            N_MULT=len(mults), MAX_MULT=max(mults) if mults else np.nan,
            MIN_MULT=min(mults) if mults else np.nan,
            STATES_K=bool(ks), N_DISTINCT_K=len(ks),
            K_MIN=min(ks) if ks else 0, K_MAX=max(ks) if ks else 0,
            VARYING_K=len(ks) > 1,
            IS_BAND=bool(pairs), BAND_LO=pairs[0][0] if pairs else np.nan,
            BAND_HI=pairs[0][1] if pairs else np.nan,
            ADJUDICATED=bool(ADJUD.search(txt)),
            HAS_VERDICT=bool(VERD.search(txt)),
            COMPARATIVE=bool(COMP.search(txt)),
            text=txt))
    return pd.DataFrame(rows)


def checkable(cdf, cs):
    """1155's checkable set for a claim set: states a multiple AND two different counts."""
    return cdf[cdf[cs] & cdf.VARYING_K & cdf.N_MULT.gt(0)].copy()


def load_bearing(u, rule):
    """The multiple the verdict is read as resting on, under each NO-EFFECT rule."""
    if rule == "R_MIN":
        return float(u.MIN_MULT)
    if rule == "R_MAX":
        return float(u.MAX_MULT)
    if rule == "R_BAND":
        return float(u.BAND_LO) if np.isfinite(u.BAND_LO) else float(u.MIN_MULT)
    raise ValueError(rule)


# ==================================================================== THE HAND READ
# One line per IN-DOMAIN unit (K_MAX <= 12), read by this run against the committed text it
# came from.  KIND: A_PAIR  = a genuine range-vs-range comparison over two DIFFERENT counts,
#                             i.e. the object d2 was built for;
#                   A_OTHER = a range compared to something that is not a range (a gap, a
#                             point difference, an SD), or two ranges over the SAME count --
#                             d2 does not apply either way;
#                   A_NOTMULT = the harvested token is not a comparative multiple at all
#                             (a portfolio weight, a protocol bar, a tolerance, a count).
# CHANGES: does the unit's committed VERDICT change when its load-bearing multiple is set to
#          no effect?  Reasons are one line and are published verbatim.
AUDIT = {
    # ---- C_STRICT, in-domain
    "d1eff3e1a0": ("A_NOTMULT", False, "the 0.25x is the sleeve's PORTFOLIO WEIGHT (0.75 x top20 + 0.25 x sleeve); no range is being compared and the row carries no verdict token"),
    "08505a00dd": ("A_OTHER", False, "the 10x is a cost/turnover level in a rule-8 row; the 12 cells are OOS picks, not rungs of two ladders"),
    "d1e45a7a60": ("A_PAIR", False, "GROSS span 0.0009..0.0049 vs CADENCE 0.1241, '39x wider' — a genuine range-vs-range pair, and 39x clears any inflation two ladders of <=10 rungs can buy (max d2(10)/d2(2)=2.7274); CONFIRMED stands"),
    "389bc03035": ("A_OTHER", False, "'spread -0.0828 = -0.85 x GAP' compares a RANGE to a POINT GAP, not to another range; the verdict (H_ETF/H_FLAT FALSE, slope runs backwards) rests on the fitted sign, not on 0.85"),
    "d6206b7d66": ("A_OTHER", False, "'within-rung sd is 0.76 x GAP' compares an SD to a point gap; d2 is a RANGE constant and does not apply, and the verdict rests on 65 of 165 seed pairs (39.4%)"),
    "cbfbf9aeb3": ("A_NOTMULT", False, "the 4x is the GAP DIAL's step count ('gap dialled 4x'), not a spread ratio"),
    "d6d199b336": ("A_OTHER", False, "the 5.39x is a turnover level on an 8-rung control ladder read against itself; no second count enters, and the verdict rests on the median +0.0143 band-minus-cadence gap"),
    "d5d3a4d1d0": ("A_NOTMULT", False, "a GATES row: the tokens are tolerances (6.4e-16 etc) and cadence counts; no multiple is adjudicated and the row carries no verdict token"),
    "ca229253f8": ("A_PAIR", False, "'lambda spans a median 2.39x of turnover against cadence's 6.38x' IS range-vs-range over two dials — but lambda's ladder is the LONGER of the two (13-rung coverage + 10-rung absolute-n against cadence's D/W/M/Q), so count inflation runs AGAINST cadence and the ADOPT CADENCE verdict is if anything understated"),
    "bb0878c1e1": ("A_OTHER", False, "the 2.0x is a gross rung ('de-grosses at 1.00'), not a spread ratio; the verdict rests on the 8 measured per-book gaps"),
    "a5001741b0": ("A_PAIR", False, "1209's OWN row: 1.4426x IS d2(9)/d2(4), published BY that run as a data-free count artefact — the committed verdict (ANSWERED = NO, the shift changes no verdict) ALREADY IS the no-effect reading"),
    "69a03404d9": ("A_OTHER", False, "3.6x/9.0x are block-length and decision counts in a 0.90-bar census; no range pair"),
    "5996f24561": ("A_OTHER", False, "2.35x/6.4x are cost and panel-rung levels; the verdict (4a 13/270, 12 of them a self-tie) rests on an identity gate at 0.00e+00"),
    "cf9e45f17e": ("A_OTHER", False, "the 4.8x sits in a retire-the-premise memo about rho, not in a spread comparison"),
    "97f64224ae": ("A_PAIR", False, "the memo form of ca229253f8 ('lambda's entire ladder spans only 1.08x to 1.39x'); same object, same reading, and the count difference runs against cadence — REFUTED stands"),
    "5202e93727": ("A_OTHER", False, "'the base book with 11-16x the turnover has the WIDER window' compares two WIDTHS at the SAME 16 native cells; equal counts, inflation 1.0 by construction"),
    "f8febbcdba": ("A_NOTMULT", False, "1.0x/2.79x are gross and yield levels in a de-grossed-cash memo; the 4a PASS rests on the halves, not on a multiple"),
    "9b73db6237": ("A_OTHER", False, "'3 x the larger cross-seed spread' is a RESOLUTION BAR, not a comparison of two ranges"),
    # ---- the extra in-domain units the wider claim sets add
    "b5fd35fbeb": ("A_NOTMULT", False, "0.23x is a DD median in a matched-grid row; no verdict token and no range pair"),
    "05d6fd1eb4": ("A_PAIR", False, "'Q5 (3 rungs) 0.0801 = 0.41x idea 568 -> Q9 (7 rungs) 0.1080 = 0.55x' IS count-exposed: the growth 1.348x sits BELOW d2(7)/d2(3)=1.598, which STRENGTHENS the committed verdict that the +0.0801 is a rung-selection artefact"),
    "1170373ce5": ("A_NOTMULT", False, "a GATES row; 6.47x is a benchmark-mismatch ratio and the row carries no adjudicated multiple"),
    "8c0dab2bd1": ("A_NOTMULT", False, "the CHANGELOG form of 1170373ce5; same gate, same reading"),
    "b374f7d5cf": ("A_PAIR", False, "'the 9-rung N ladder resolves relatively BETTER than the 4-rung H ladder in 8 of 8' is explicitly a COUNT claim and the row publishes both counts; the 1.5x survives d2(9)/d2(4)=1.4426 and the verdict stands"),
    "f97ee49a51": ("A_NOTMULT", False, "the memo form of 1170373ce5; same gate, same reading"),
}


# ==================================================================== panels / runner
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
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


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


def build1(pan, N, H, freq, lag=1):
    """1098/1159's min-hold selection frame at GROSS = 1.0.  Row t is the APPLICATION-time
    weight; `lag` is how far back the SELECTION reads the score.  lag=1 is PROTOCOL rule 2's
    decide-at-t / apply-at-t+1 (1209's correction).  Selection does not depend on gross, so
    the GROSS ladder is this frame SCALED -- gate G5."""
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
    """weights are already t+1-applied (the cadence mask is shifted); 10 bps on turnover."""
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
    return (held * rets).sum(axis=1) - turn * COST / 1e4


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
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def keep_paths(r, bm, live):
    """Both KEEP paths.  bm/live are dicts with CAGR/Sharpe/MaxDD/H1/H2 on the SAME window."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1207 (lane C, 2026-09-17) — how many committed RANGE claims quote a MULTIPLE")
    say("BELOW THEIR OWN COUNT INFLATION, and were ADJUDICATED ON IT?")
    say("=" * 108)

    # ------------------------------------------------------------------ ARM 0
    say("")
    say("ARM 0 — THE ARITHMETIC, PRINTED BEFORE ANY TEXT OR ANY PRICE IS READ.")
    say("  A range is not an estimator of dispersion: for k iid N(0,1) draws E[max-min] = d2(k),")
    say("  tabulated for k = 2..12.  The longest ladder this record has ever published is 10.")
    rng = np.random.default_rng(MC_SEED)
    mc_err = 0.0
    for k in sorted(D2):
        x = rng.standard_normal((200_000, k))
        mc_err = max(mc_err, abs((x.max(1) - x.min(1)).mean() - D2[k]))
    say(f"  d2 Monte Carlo at 2e5 draws reproduces every published constant to {mc_err:.3e}.")
    GATES.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants", value=mc_err,
                      target=5e-3, pass_=bool(mc_err < 5e-3)))
    say("")
    say("  THE SUBSTITUTION CONVENTION IS NOT A DIAL, AND HERE IS WHY, WITH NO DATA IN IT.")
    say("  A verdict resting on a multiple M rests on the comparative M/I > 1, I being the")
    say("  inflation d2(k_max)/d2(k_min) the two counts alone buy.  Setting M to no effect:")
    say("    M' = 1      -> M'/I = 1/I  < 1 for every unit with k_max > k_min  -> flips ALL")
    say("    M' = I      -> M'/I = 1                                           -> flips ALL")
    say("    M' = M/I    -> (M/I) > 1 iff M > I                                -> flips {M <= I}")
    say("  Every convention is THE SAME THRESHOLD AT I.  It is gated (G3) and never walked.")
    say("")
    say("  PRE-DECLARED OUTCOMES (before the trace): (A) MANY — 10 or more committed verdicts")
    say("  change; (B) FEW — 1 to 9; (C) NONE — the failing multiples are not what the verdicts")
    say("  rest on; (D) UNTRACEABLE — the failing units carry no recoverable verdict at all.")

    # ------------------------------------------------------------------ ARM A1: the 1155 replay
    say("")
    say("=" * 108)
    say("ARM A — THE CENSUS, THE DOMAIN SPLIT, AND THE TRACE")
    say("=" * 108)
    say("")
    say(f"  (A1) 1155's census REPLAYED on the corpus it actually ran against ({REPLAY_REV}).")
    Ur, nmd_r = units_at(REPLAY_REV)
    cr = census(Ur)
    sr = checkable(cr, "C_STRICT")
    inflr = np.array([d2(a) / d2(b) for a, b in zip(sr.K_MAX, sr.K_MIN)])
    survr = (sr.MIN_MULT.values > inflr)
    rep = dict(units=len(Ur), md=nmd_r, C_STRICT=int(cr.C_STRICT.sum()), checkable=len(sr),
               survives=int(survr.sum()), share=float(survr.mean()),
               med_infl=float(np.median(inflr)))
    say(f"      units {rep['units']} (1155: 32,930) | md files {rep['md']} (1,137) | "
        f"C_STRICT {rep['C_STRICT']} (313) | checkable {rep['checkable']} (90)")
    say(f"      SMALLEST multiple survives at {rep['survives']} of {rep['checkable']} "
        f"({rep['share']:.4f}) — 1155 committed 54 of 90 (0.6000); median inflation "
        f"{rep['med_infl']:.4f} (1.8999)")
    ok = (rep["units"] == 32930 and rep["md"] == 1137 and rep["C_STRICT"] == 313
          and rep["checkable"] == 90 and rep["survives"] == 54
          and abs(rep["med_infl"] - 1.8999) < 1e-4)
    GATES.append(dict(gate="G1 1155 census replayed bit-for-bit at its own corpus",
                      value=float(rep["survives"]), target=54.0, pass_=bool(ok)))
    say(f"      GATE G1: {'PASS — bit for bit' if ok else 'FAIL'}")

    # ------------------------------------------------------------------ ARM A2: live census
    say("")
    say("  (A2) THE LIVE CENSUS at this run's HEAD, and the DIAL GRID — 9 cells, all published.")
    U, nmd = units_at(None)
    cdf = census(U)
    say(f"      corpus {len(U)} committed text units ({int((cdf.src=='LEADERBOARD').sum())} "
        f"LEADERBOARD rows, {int((cdf.src=='CHANGELOG').sum())} CHANGELOG paragraphs, "
        f"{nmd} markdown artefacts)")
    nest = int((cdf.C_STRICT & ~cdf.C_PROX).sum() + (cdf.C_PROX & ~cdf.C_ALL).sum())
    GATES.append(dict(gate="G2 claim sets nest C_STRICT<=C_PROX<=C_ALL", value=float(nest),
                      target=0.0, pass_=bool(nest == 0)))

    grid, allrows = [], []
    for cs in CLAIMSETS:
        sub = checkable(cdf, cs)
        sub["INFL"] = [d2(a) / d2(b) for a, b in zip(sub.K_MAX, sub.K_MIN)]
        sub["IN_DOMAIN"] = (sub.K_MAX <= KMAXD2) & (sub.K_MIN <= KMAXD2)
        for rule in NORULES:
            lb = np.array([load_bearing(u, rule) for _, u in sub.iterrows()])
            fails = lb <= sub.INFL.values
            ind = sub.IN_DOMAIN.values
            carried = sub.HAS_VERDICT.values & sub.COMPARATIVE.values
            grid.append(dict(
                CLAIM_SET=cs, NO_EFFECT_RULE=rule, checkable=len(sub),
                FAILS=int(fails.sum()), FAILS_share=float(fails.mean()) if len(sub) else np.nan,
                FAILS_VACUOUS=int((fails & ~ind).sum()),
                FAILS_IN_DOMAIN=int((fails & ind).sum()),
                FAILS_IND_CARRIED=int((fails & ind & carried).sum()),
                FAILS_IND_NO_VERDICT=int((fails & ind & ~sub.HAS_VERDICT.values).sum()),
                median_inflation=float(np.median(sub.INFL.values)) if len(sub) else np.nan))
            for (_, u), f, i_, c in zip(sub.iterrows(), fails, ind, carried):
                allrows.append(dict(CLAIM_SET=cs, NO_EFFECT_RULE=rule, uid=u.uid, src=u.src,
                                    load_bearing=load_bearing(u, rule), MIN_MULT=u.MIN_MULT,
                                    MAX_MULT=u.MAX_MULT, BAND_LO=u.BAND_LO, K_MIN=u.K_MIN,
                                    K_MAX=u.K_MAX, INFLATION=u.INFL, FAILS=bool(f),
                                    IN_DOMAIN=bool(i_), HAS_VERDICT=bool(u.HAS_VERDICT),
                                    COMPARATIVE=bool(u.COMPARATIVE), CARRIED=bool(c)))
    gdf = pd.DataFrame(grid)
    gdf.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(allrows).to_csv(f"{OUT}.reread.csv", index=False)
    say("")
    say("      claim set  rule     checkable  FAILS  (share)  of which VACUOUS  IN-DOMAIN  "
        "in-dom & carries a verdict")
    for _, g in gdf.iterrows():
        say(f"      {g.CLAIM_SET:9s}  {g.NO_EFFECT_RULE:7s}  {g.checkable:9d}  {g.FAILS:5d}  "
            f"({g.FAILS_share:.4f})   {g.FAILS_VACUOUS:14d}  {g.FAILS_IN_DOMAIN:9d}  "
            f"{g.FAILS_IND_CARRIED:26d}")

    # ------------------------------------------------------------------ ARM A3: the domain split
    say("")
    say("  (A3) THE DOMAIN SPLIT — WHY THE 36 IS NOT A 36.")
    cstr = checkable(cdf, "C_STRICT")
    cstr["INFL"] = [d2(a) / d2(b) for a, b in zip(cstr.K_MAX, cstr.K_MIN)]
    cstr["IN_DOMAIN"] = (cstr.K_MAX <= KMAXD2) & (cstr.K_MIN <= KMAXD2)
    nvac = int((~cstr.IN_DOMAIN).sum())
    say(f"      C_STRICT checkable {len(cstr)}: IN-DOMAIN (every harvested count <= {KMAXD2}, the")
    say(f"      d2 table's whole domain and 2 rungs beyond the record's longest ladder) "
        f"{int(cstr.IN_DOMAIN.sum())};")
    say(f"      VACUOUS {nvac} ({nvac/len(cstr):.4f}) — their inflation is the CLIPPED constant")
    say(f"      d2({KMAXD2})/d2(k_min), a number with no relation to the claim.")
    say(f"      Largest harvested count in the VACUOUS set: {int(cstr[~cstr.IN_DOMAIN].K_MAX.max()):,} "
        f"— median {int(cstr[~cstr.IN_DOMAIN].K_MAX.median()):,}.")
    part = int((cstr.IN_DOMAIN.sum() + (~cstr.IN_DOMAIN).sum()) == len(cstr))
    GATES.append(dict(gate="G10 the domain split partitions the checkable set exactly",
                      value=float(len(cstr) - cstr.IN_DOMAIN.sum() - (~cstr.IN_DOMAIN).sum()),
                      target=0.0, pass_=bool(part == 1)))

    # ------------------------------------------------------------------ ARM A4: the trace
    say("")
    say("  (A4) THE TRACE — every IN-DOMAIN unit across ALL claim sets, hand-read, one line each.")
    ind_all = cdf[(cdf.C_STRICT | cdf.C_PROX | cdf.C_ALL) & cdf.VARYING_K & cdf.N_MULT.gt(0)]
    ind_all = ind_all[(ind_all.K_MAX <= KMAXD2) & (ind_all.K_MIN <= KMAXD2)].copy()
    ind_all["INFL"] = [d2(a) / d2(b) for a, b in zip(ind_all.K_MAX, ind_all.K_MIN)]
    arows = []
    unaudited = []
    for _, u in ind_all.iterrows():
        if u.uid not in AUDIT:
            unaudited.append((u.uid, u.src))
            kind, chg, note = "UNAUDITED", None, "unit not in this run's hand-read table (corpus drift)"
        else:
            kind, chg, note = AUDIT[u.uid]
        row = dict(uid=u.uid, src=u.src, C_STRICT=bool(u.C_STRICT), C_PROX=bool(u.C_PROX),
                   C_ALL=bool(u.C_ALL), MIN_MULT=u.MIN_MULT, MAX_MULT=u.MAX_MULT,
                   BAND_LO=u.BAND_LO, K_MIN=u.K_MIN, K_MAX=u.K_MAX, INFLATION=u.INFL,
                   HAS_VERDICT=bool(u.HAS_VERDICT), COMPARATIVE=bool(u.COMPARATIVE),
                   KIND=kind, VERDICT_CHANGES=chg, READ=note,
                   excerpt=" ".join(u.text.split())[:300])
        for rule in NORULES:
            row["FAILS_" + rule] = bool(load_bearing(u, rule) <= u.INFL)
        arows.append(row)
    adf = pd.DataFrame(arows)
    adf.to_csv(f"{OUT}.audit.csv", index=False)
    GATES.append(dict(gate="G9 every in-domain unit carries a hand read",
                      value=float(len(unaudited)), target=0.0, pass_=bool(not unaudited)))
    say(f"      IN-DOMAIN units across all claim sets: {len(adf)}; hand-read {len(adf)-len(unaudited)}; "
        f"UNAUDITED {len(unaudited)}")
    say(f"      KINDS: " + ", ".join(f"{k} {v}" for k, v in adf.KIND.value_counts().items()))
    say("")
    say("      THE FAILING IN-DOMAIN UNITS, ONE LINE EACH (R_MIN, the headline leg):")
    fails_ind = adf[adf.FAILS_R_MIN]
    for _, r in fails_ind.iterrows():
        say(f"        {r.uid}  {r.KIND:9s} chg={r.VERDICT_CHANGES}  "
            f"min={r.MIN_MULT:g} vs I={r.INFLATION:.4f}  k={int(r.K_MIN)}/{int(r.K_MAX)}  "
            f"{r.src[:46]}")
        say(f"                    {r.READ}")
    say("")
    changed = {}
    for rule in NORULES:
        f = adf[adf["FAILS_" + rule]]
        ch = int((f.VERDICT_CHANGES == True).sum())  # noqa: E712
        changed[rule] = ch
        say(f"      {rule:7s}: {len(f):2d} IN-DOMAIN units fail; VERDICTS THAT CHANGE when the "
            f"load-bearing multiple is set to no effect: {ch}")
    say("")
    say(f"      ANSWER: {max(changed.values())} committed verdicts change at the most permissive "
        f"of the three no-effect rules.")

    # ------------------------------------------------------------------ G3: degeneracy proof
    say("")
    say("  (A5) GATE G3 — the substitution convention proved degenerate ON THE ACTUAL UNITS.")
    sub = checkable(cdf, "C_ALL")
    I = np.array([d2(a) / d2(b) for a, b in zip(sub.K_MAX, sub.K_MIN)])
    M = sub.MIN_MULT.values.astype(float)
    live = I > 1.0                       # the units where the two counts actually differ
    flip_unit = ((1.0 / I) <= 1.0)[live]
    flip_infl = ((I / I) <= 1.0)[live]
    flip_corr = ((M / I) <= 1.0)[live]
    mism = int((flip_corr != (M <= I)[live]).sum())
    say(f"      units with k_max > k_min: {int(live.sum())}   M'=1 flips {flip_unit.mean():.4f}   "
        f"M'=I flips {flip_infl.mean():.4f}   M'=M/I flips {flip_corr.mean():.4f}")
    say(f"      M'=M/I flips EXACTLY the set {{M <= I}}: mismatches {mism}")
    say("      Both degenerate conventions flip EVERY unit; only M/I discriminates.")
    g3 = float(mism + (1.0 - flip_unit.mean()) + (1.0 - flip_infl.mean()))
    GATES.append(dict(gate="G3 substitution convention is one threshold at I, not a dial",
                      value=g3, target=0.0,
                      pass_=bool(mism == 0 and flip_unit.all() and flip_infl.all())))

    # determinism of the census
    c2 = census(U)
    det = float((c2.drop(columns=["text"]).fillna(-9).values
                 != cdf.drop(columns=["text"]).fillna(-9).values).sum())
    GATES.append(dict(gate="G11 census is deterministic across two runs", value=det, target=0.0,
                      pass_=bool(det == 0)))

    # ------------------------------------------------------------------ ARM B: the price leg
    say("")
    say("=" * 108)
    say("ARM B — PRICING THE VERDICT CHANGE.  RULE 8 WALK-FORWARD AND BOTH KEEP PATHS.")
    say("=" * 108)
    say("")
    say("  The record's habit is 'this dial's spread is X times that one's, so tune this dial'.")
    say("  That IS a range multiple across two ladders of different rung counts — the object")
    say("  1207 is about — and it is made live here:")
    say("    CH_RAW     tune the ladder with the widest RAW max-min spread (the record's habit;")
    say("               licensed by M > 1, which is true by construction, so it ALWAYS tunes).")
    say("    CH_MATCHED tune it ONLY if M > I = d2(k_wide)/d2(k_narrow); otherwise STAY at the")
    say("               anchor.  This is CH_RAW with the failing verdicts SET TO NO EFFECT.")
    say("    CH_D2      tune the argmax of spread / d2(k) (1155's M_D2 repair) — always tunes.")
    say("    CH_ANCHOR  never move (the do-nothing control, 1155/1206's comparand).")
    say("  The paired CH_MATCHED - CH_RAW delta IS the price of changing the verdict.")

    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0), SPY benchmark only.")
    panels.append(Panel("SMALL", pxS, inv))

    booked, bench = {}, {}
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
        anchor_frame = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            fr = anchor_frame if f == "W" else frames[(A_N, A_H, "M")]
            books[("CADENCE", f)] = nrun(pan, A_G * fr, f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * anchor_frame, "W")
        booked[pan.name] = books
        # benchmarks on the same index
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books built "
            f"({len(frames)} distinct selection frames + {len(LAD['GROSS'])} gross scalings).")

    # ---- gates on the price machinery
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    Wdec = Wdf.shift(-1).fillna(0.0)            # engine shifts by 1; build writes application rows
    eb = backtest(pan.px, Wdec, cost_bps=COST, freq="W")["returns"].values
    fast = nrun(pan, Wt, "W")
    g4 = float(np.nanmax(np.abs(eb[WARMUP:] - fast[WARMUP:])))
    GATES.append(dict(gate="G4 fast runner == engine.backtest on the decision-time frame",
                      value=g4, target=1e-10, pass_=bool(g4 < 1e-10)))
    fr = build1(pan, A_N, A_H, "W")
    g5 = float(np.abs(0.5 * fr - (0.5 * fr)).max()
               + np.abs((0.30 * fr) - 0.30 * fr).max())
    g5 = float(max(np.abs(g * fr - g * fr).max() for g in LAD["GROSS"]))
    GATES.append(dict(gate="G5 the GROSS ladder is the anchor frame SCALED", value=g5,
                      target=0.0, pass_=bool(g5 == 0.0)))
    lm = mdd(bench["U56"]["live"][WARMUP:])
    GATES.append(dict(gate="G6 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                      value=lm, target=LIVE_MAXDD_COMMITTED, pass_=bool(abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)))
    say("")
    say(f"    G4 fast runner vs engine.backtest {g4:.3e}   G5 gross-scaling identity {g5:.3e}   "
        f"G6 live U56 MaxDD {lm:.4%}")

    # ---- benchmarks table
    say("")
    say("  BENCHMARKS (10 bps, t+1, post warm-up):")
    BM = {}
    for pan in panels:
        i0 = pan.i0
        ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[i0:]
            h1, h2 = halves(full)
            d = dict(**triple(full), H1=h1, H2=h2,
                     OOS_Sharpe=sharpe(r[ioos:]), OOS_CAGR=cagr(r[ioos:]), OOS_MaxDD=mdd(r[ioos:]))
            BM[(pan.name, nm)] = d
            say(f"    {pan.name:6s} {nm:5s} {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / {d['MaxDD']:8.2%}  "
                f"halves {d['H1']:.4f}/{d['H2']:.4f}  OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f}")

    # ---- both KEEP paths on every rung book
    say("")
    say("  BOTH KEEP PATHS ON EVERY RUNG BOOK (rule 4; nothing selected on):")
    brows = []
    for pan in panels:
        i0, ioos = pan.i0, pan.idx.searchsorted(pd.Timestamp(OOS_START))
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        spy_oos = dict(H1=halves(bench[pan.name]["spy"][ioos:])[0],
                       H2=halves(bench[pan.name]["spy"][ioos:])[1],
                       CAGR=spy["OOS_CAGR"], MaxDD=spy["OOS_MaxDD"])
        liv_oos = dict(H1=halves(bench[pan.name]["live"][ioos:])[0],
                       H2=halves(bench[pan.name]["live"][ioos:])[1],
                       CAGR=liv["OOS_CAGR"], MaxDD=liv["OOS_MaxDD"])
        for (lad, rung), r in booked[pan.name].items():
            k4a, k4b, m, h1, h2 = keep_paths(r[i0:], spy, liv)
            k4a_o, k4b_o, mo, _, _ = keep_paths(r[ioos:], spy_oos, liv_oos)
            brows.append(dict(panel=pan.name, ladder=lad, rung=rung, CAGR=m["CAGR"],
                              Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    bdf = pd.DataFrame(brows)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"    {len(bdf)} rung books: 4a {int(bdf.KEEP_4a.sum())} of {len(bdf)}; "
        f"4b full {int(bdf.KEEP_4b.sum())}; 4b OOS {int(bdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((bdf.KEEP_4b & bdf.KEEP_4b_OOS).sum())}")
    for p in bdf.panel.unique():
        s = bdf[bdf.panel == p]
        say(f"      {p:6s} 4a {int(s.KEEP_4a.sum())}/{len(s)}   4b full {int(s.KEEP_4b.sum())}   "
            f"4b OOS {int(s.KEEP_4b_OOS.sum())}   BOTH {int((s.KEEP_4b & s.KEEP_4b_OOS).sum())}")

    # ---- the choosers
    LADSETS = {"ALL4": ["N", "H", "GROSS", "CADENCE"], "NG": ["N", "H", "CADENCE"]}
    say("")
    say("  TWO LADDER SETS, AND THE ORDERING IS DECLARED RATHER THAN HIDDEN.  ALL4 is the")
    say("  record's own four ladders and is the HEADLINE.  NG (no GROSS) was added AFTER the")
    say("  ALL4 leg showed the bar cannot bind there, because GROSS is simultaneously the")
    say("  LONGEST ladder (10 rungs) and the one whose Sharpe spread is degenerate (idea 1189,")
    say("  reproduced by 1206 at 0 of 1,888 widest-calls) — so it is always the NARROWEST and")
    say("  the bar d2(k_wide)/d2(k_narrow) lands BELOW 1.  NG is a POST-HOC control, labelled")
    say("  as one, and no verdict in this run rests on it.")

    def spreads(pan, lo, hi, lads):
        out = {}
        for lad in lads:
            v = [sharpe(booked[pan.name][(lad, r)][lo:hi]) for r in LAD[lad]]
            v = [x for x in v if np.isfinite(x)]
            out[lad] = (max(v) - min(v)) if len(v) > 1 else np.nan
        return out

    def pick_of(pan, lad, lo, hi):
        v = [(sharpe(booked[pan.name][(lad, r)][lo:hi]), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    def choose(pan, lo, hi, lads):
        sp = spreads(pan, lo, hi, lads)
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        wide = max(good, key=good.get)
        narrow = min(good, key=good.get)
        Mult = good[wide] / good[narrow] if good[narrow] > 0 else np.inf
        Infl = d2(LADK[wide]) / d2(LADK[narrow])
        d2w = max(good, key=lambda k: good[k] / d2(LADK[k]))
        out = {}
        out["CH_RAW"] = (wide, pick_of(pan, wide, lo, hi))
        out["CH_MATCHED"] = out["CH_RAW"] if Mult > Infl else ("CADENCE", A_C)
        out["CH_D2"] = (d2w, pick_of(pan, d2w, lo, hi))
        out["CH_ANCHOR"] = ("CADENCE", A_C)
        return out, wide, narrow, Mult, Infl, sp

    def rets_of(pan, sel, lo, hi):
        lad, rung = sel
        if lad == "CADENCE" and rung == A_C:
            return booked[pan.name][("CADENCE", A_C)][lo:hi]
        return booked[pan.name][(lad, rung)][lo:hi]

    BASECH = ["CH_RAW", "CH_MATCHED", "CH_D2", "CH_ANCHOR"]
    CHOOSERS = [f"{c}/{s}" for s in LADSETS for c in BASECH]

    # ---- B1: the rolling walk (many picks; 1206's lesson that three cannot resolve anything)
    say("")
    say("  (B1) THE ROLLING WALK — one calendar year of OOS per fold, stepped one year,")
    say(f"       {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}, IS = everything from the warm-up to the day")
    say("       before the fold.  Folds tile the evaluation span with no overlap and no gap.")
    prows, stitched, pairrows = [], {}, []
    for pan in panels:
        yrs = pan.idx.year.values
        cover = []
        for y in FOLD_YEARS:
            oo = np.flatnonzero(yrs == y)
            oo = oo[oo >= pan.i0]
            if len(oo) < 60:
                continue
            lo, hi = pan.i0, int(oo[0])
            if hi - lo < 252:
                continue
            cover.append((int(oo[0]), int(oo[-1]) + 1))
            # every ORDERED ladder pair, so the bar's binding rate is reported un-selected
            spall = spreads(pan, lo, hi, LADSETS["ALL4"])
            for a in LADSETS["ALL4"]:
                for b in LADSETS["ALL4"]:
                    if a == b or not (np.isfinite(spall[a]) and np.isfinite(spall[b])):
                        continue
                    if spall[a] < spall[b]:
                        continue                      # a is the WIDER of the pair by definition
                    M_ = spall[a] / spall[b] if spall[b] > 0 else np.inf
                    I_ = d2(LADK[a]) / d2(LADK[b])
                    pairrows.append(dict(panel=pan.name, fold=y, wider=a, narrower=b,
                                         k_wider=LADK[a], k_narrower=LADK[b],
                                         MULTIPLE=M_, INFLATION=I_, SURVIVES=bool(M_ > I_),
                                         BAR_BELOW_ONE=bool(I_ < 1.0)))
            for sname, lads in LADSETS.items():
                sel, wide, narrow, Mult, Infl, sp = choose(pan, lo, hi, lads)
                for base_ch in BASECH:
                    ch = f"{base_ch}/{sname}"
                    r = rets_of(pan, sel[base_ch], int(oo[0]), int(oo[-1]) + 1)
                    stitched.setdefault((pan.name, ch), []).append((y, r))
                    prows.append(dict(panel=pan.name, fold=y, chooser=ch, ladder_set=sname,
                                      ladder=sel[base_ch][0], rung=sel[base_ch][1],
                                      widest=wide, narrowest=narrow,
                                      MULTIPLE=Mult, INFLATION=Infl, SURVIVES=bool(Mult > Infl),
                                      moved=bool(sel[base_ch] != ("CADENCE", A_C)),
                                      OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r), OOS_MaxDD=mdd(r)))
        cover = sorted(set(cover))
        gapover = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
        GATES.append(dict(gate=f"G7 folds tile {pan.name} with no overlap and no gap",
                          value=float(gapover), target=0.0, pass_=bool(gapover == 0)))
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    pairdf = pd.DataFrame(pairrows)
    pairdf.to_csv(f"{OUT}.pairs.csv", index=False)
    mv_anchor = float(pdf[pdf.chooser.str.startswith("CH_ANCHOR")].moved.mean())
    GATES.append(dict(gate="G8 CH_ANCHOR move rate == 0", value=mv_anchor, target=0.0,
                      pass_=bool(mv_anchor == 0.0)))

    say("")
    say(f"      {len(pdf)} pick-cells = {pdf.panel.nunique()} panels x "
        f"{pdf.fold.nunique()} folds x {len(CHOOSERS)} choosers "
        f"({len(pdf)//len(CHOOSERS)} picks per chooser).")
    say("")
    say("      EVERY ORDERED LADDER PAIR, UN-SELECTED — when does the count-inflation bar BIND?")
    say("      wider / narrower      k     n   multiple (median)   bar I    survives   bar < 1")
    for (a, b), g in pairdf.groupby(["wider", "narrower"]):
        say(f"        {a:8s}/{b:8s} {g.k_wider.iloc[0]:2d}/{g.k_narrower.iloc[0]:2d}  {len(g):4d}   "
            f"{g.MULTIPLE.median():16.4f}   {g.INFLATION.iloc[0]:.4f}   "
            f"{g.SURVIVES.mean():8.4f}   {g.BAR_BELOW_ONE.iloc[0]}")
    say(f"      OVER ALL {len(pairdf)} REALISED PAIRS: the bar sits BELOW 1 at "
        f"{pairdf.BAR_BELOW_ONE.mean():.4f} and the multiple survives at "
        f"{pairdf.SURVIVES.mean():.4f}.")
    for sname in LADSETS:
        surv = pdf[pdf.chooser == f"CH_RAW/{sname}"]
        flip = pdf[pdf.chooser == f"CH_MATCHED/{sname}"].reset_index(drop=True)
        raww = surv.reset_index(drop=True)
        nf = int(((flip.ladder != raww.ladder) | (flip.rung != raww.rung)).sum())
        say("")
        say(f"      [{sname}] the chooser's own comparison survives its count inflation at "
            f"{int(surv.SURVIVES.sum())} of {len(surv)} cells ({surv.SURVIVES.mean():.4f}); "
            f"median multiple {surv.MULTIPLE.median():.4f} vs median bar "
            f"{surv.INFLATION.median():.4f}.")
        say(f"      [{sname}] CH_MATCHED DIFFERS FROM CH_RAW AT {nf} of {len(raww)} CELLS — "
            f"the verdict flip made live.")
    say("")
    say("      mean OOS Sharpe over all picks, and the PAIRED delta vs that ladder set's own")
    say("      CH_RAW, SE clustered on the FOLD (folds tile the tape without overlap, so fold")
    say("      means are the independent units; panels inside a fold are not):")
    nflip_rows = []
    for sname in LADSETS:
        base = pdf[pdf.chooser == f"CH_RAW/{sname}"].set_index(["panel", "fold"]).OOS_Sharpe
        for base_ch in BASECH:
            ch = f"{base_ch}/{sname}"
            s = pdf[pdf.chooser == ch].set_index(["panel", "fold"]).OOS_Sharpe
            d = (s - base).dropna()
            fold_mean = d.groupby(level=1).mean()
            se = fold_mean.std(ddof=1) / np.sqrt(len(fold_mean)) if len(fold_mean) > 1 else np.nan
            t = d.mean() / se if se and se > 0 else 0.0
            say(f"        {ch:18s} mean OOS Sharpe {s.mean():.4f}   delta vs CH_RAW/{sname} "
                f"{d.mean():+.4f}   SE {se:.4f}   t {t:+.2f}")
            nflip_rows.append(dict(chooser=ch, mean_OOS_Sharpe=s.mean(), delta=d.mean(),
                                   SE=se, t=t))
    pd.DataFrame(nflip_rows).to_csv(f"{OUT}.deltas.csv", index=False)
    nflip = int(((pdf[pdf.chooser == "CH_MATCHED/NG"].reset_index(drop=True).ladder
                  != pdf[pdf.chooser == "CH_RAW/NG"].reset_index(drop=True).ladder)
                 | (pdf[pdf.chooser == "CH_MATCHED/NG"].reset_index(drop=True).rung
                    != pdf[pdf.chooser == "CH_RAW/NG"].reset_index(drop=True).rung)).sum())
    say("")
    say("      by panel (mean OOS Sharpe):")
    for p in pdf.panel.unique():
        for sname in LADSETS:
            line = f"        {p:6s} [{sname:5s}]"
            for base_ch in BASECH:
                line += (f"  {base_ch} "
                         f"{pdf[(pdf.panel==p)&(pdf.chooser==f'{base_ch}/{sname}')].OOS_Sharpe.mean():.4f}")
            say(line)

    # ---- B2: rule 8, the single split, read ONCE
    say("")
    say("  (B2) RULE 8 — the single split the PROTOCOL names.  Dials chosen on the IS window")
    say("       (to 2016-12-31) ONLY; 2017-2026 read ONCE.")
    wrows = []
    for pan in panels:
        iend = pan.idx.searchsorted(pd.Timestamp("2017-01-01"))
        ioos = iend
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        spy_oos = dict(H1=halves(bench[pan.name]["spy"][ioos:])[0],
                       H2=halves(bench[pan.name]["spy"][ioos:])[1],
                       CAGR=spy["OOS_CAGR"], MaxDD=spy["OOS_MaxDD"])
        liv_oos = dict(H1=halves(bench[pan.name]["live"][ioos:])[0],
                       H2=halves(bench[pan.name]["live"][ioos:])[1],
                       CAGR=liv["OOS_CAGR"], MaxDD=liv["OOS_MaxDD"])
        for sname, lads in LADSETS.items():
            sel, wide, narrow, Mult, Infl, sp = choose(pan, pan.i0, iend, lads)
            say(f"       {pan.name:6s} [{sname:5s}] IS spreads " +
                " ".join(f"{k} {sp[k]:.4f}" for k in lads) +
                f" | widest {wide} (k={LADK[wide]}) narrowest {narrow} (k={LADK[narrow]}) | "
                f"MULTIPLE {Mult:.4f} vs INFLATION {Infl:.4f} -> "
                f"{'SURVIVES' if Mult > Infl else 'FAILS (CH_MATCHED declines to move)'}")
            for base_ch in BASECH:
                ch = f"{base_ch}/{sname}"
                rf = rets_of(pan, sel[base_ch], pan.i0, len(pan.rets))
                ro = rets_of(pan, sel[base_ch], ioos, len(pan.rets))
                k4a, k4b, m, h1, h2 = keep_paths(rf, spy, liv)
                k4a_o, k4b_o, mo, oh1, oh2 = keep_paths(ro, spy_oos, liv_oos)
                wrows.append(dict(panel=pan.name, chooser=ch, ladder_set=sname,
                                  ladder=sel[base_ch][0], rung=sel[base_ch][1],
                                  widest=wide, MULTIPLE=Mult, INFLATION=Infl,
                                  CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                  H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                                  LIVE_OOS_Sharpe=liv["OOS_Sharpe"],
                                  KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
                say(f"         {ch:18s} -> {sel[base_ch][0]}={sel[base_ch][1]}   "
                    f"full {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:8.2%}  "
                    f"halves {h1:.4f}/{h2:.4f}   "
                    f"OOS {mo['CAGR']:7.2%} / {mo['Sharpe']:.4f} / {mo['MaxDD']:8.2%}   "
                    f"4a {k4a}  4b {k4b}  4b_OOS {k4b_o}")
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---- B3: the stitched deployable curves
    say("")
    say("  (B3) THE STITCHED DEPLOYABLE CURVES — each chooser's own fold picks, concatenated.")
    srows = []
    stitch_len_ok = 0
    for (p, ch), parts in stitched.items():
        parts = sorted(parts, key=lambda z: z[0])
        r = np.concatenate([x for _, x in parts])
        ro = np.concatenate([x for y, x in parts if y >= 2017])
        stitch_len_ok += int(len(r) == sum(len(x) for _, x in parts))
        ioos = [q for q in panels if q.name == p][0].idx.searchsorted(pd.Timestamp(OOS_START))
        spy, liv = BM[(p, "SPY")], BM[(p, "LIVE")]
        spy_oos = dict(H1=halves(bench[p]["spy"][ioos:])[0], H2=halves(bench[p]["spy"][ioos:])[1],
                       CAGR=spy["OOS_CAGR"], MaxDD=spy["OOS_MaxDD"])
        liv_oos = dict(H1=halves(bench[p]["live"][ioos:])[0], H2=halves(bench[p]["live"][ioos:])[1],
                       CAGR=liv["OOS_CAGR"], MaxDD=liv["OOS_MaxDD"])
        k4a, k4b, m, h1, h2 = keep_paths(r, spy, liv)
        k4a_o, k4b_o, mo, _, _ = keep_paths(ro, spy_oos, liv_oos)
        srows.append(dict(panel=p, chooser=ch, n_days=len(r), n_oos_days=len(ro),
                          CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                          MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                          OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                          KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    sdf = pd.DataFrame(srows).sort_values(["panel", "chooser"])
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    GATES.append(dict(gate="G12 each stitched curve's length == the sum of its folds'",
                      value=float(len(sdf) - stitch_len_ok), target=0.0,
                      pass_=bool(stitch_len_ok == len(sdf))))
    for _, r in sdf.iterrows():
        say(f"       {r.panel:6s} {r.chooser:18s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:8.2%}  "
            f"halves {r.H1:.4f}/{r.H2:.4f}  OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f}   "
            f"4a {r.KEEP_4a}  4b {r.KEEP_4b}  4b_OOS {r.KEEP_4b_OOS}")
    say("")
    say(f"     STITCHED CURVES ({len(sdf)}): 4a {int(sdf.KEEP_4a.sum())}; "
        f"4b full {int(sdf.KEEP_4b.sum())}; 4b OOS {int(sdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((sdf.KEEP_4b & sdf.KEEP_4b_OOS).sum())}")
    say(f"     RULE-8 PICKS ({len(wdf)}): 4a {int(wdf.KEEP_4a.sum())}; "
        f"4b full {int(wdf.KEEP_4b.sum())}; 4b OOS {int(wdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((wdf.KEEP_4b & wdf.KEEP_4b_OOS).sum())}")

    # ------------------------------------------------------------------ gates
    say("")
    say("=" * 108)
    say("GATES")
    say("=" * 108)
    gdf2 = pd.DataFrame(GATES)
    gdf2.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gdf2.iterrows():
        say(f"  {'PASS' if g.pass_ else 'FAIL'}  {g.gate:64s} {g.value:>14.6g} "
            f"(target {g.target:g})")
    say(f"  {int(gdf2.pass_.sum())} of {len(gdf2)} gates pass.")

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 108)
    ans = max(changed.values())
    label = ("(A) MANY" if ans >= 10 else "(B) FEW" if ans >= 1 else "(C) NONE")
    say(f"ANSWER: {label} — {ans} committed verdicts change.")
    say("=" * 108)
    say(f"runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(grid=gdf, audit=adf, picks=pdf, walk=wdf, stitched=sdf, books=bdf,
                gates=gdf2, changed=changed, BM=BM, rep=rep, nvac=nvac, cstr=len(cstr),
                nflip=nflip, surv=surv)


if __name__ == "__main__":
    main()
