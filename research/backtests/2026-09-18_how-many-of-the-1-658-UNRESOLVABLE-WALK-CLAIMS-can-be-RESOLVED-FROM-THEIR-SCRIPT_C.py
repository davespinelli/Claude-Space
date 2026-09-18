#!/usr/bin/env python3
"""QUEUE idea 1246 (lane C, 2026-09-18) — how many of the 1,658 UNRESOLVABLE WALK CLAIMS can be
RESOLVED FROM THEIR SCRIPT?

QUESTION (QUEUE '## Open', verbatim)
    idea 1239 could rebuild the candidate set of only 358 of 2,016 adjudicated walk claims
    because the other 1,658 name no ladder in their text, and gave those NO number rather than
    a transferred one.  Resolve each to the committed script that produced it and report how
    many candidate sets are recoverable from code where the prose lost them.  Max 2 params
    (claim set, resolution rule).

WHY THE QUESTION IS WORTH A RUN.  1239's headline — MEDIAN STATED N = 51, MEDIAN EFFECTIVE N = 3
— is computed on 358 claims, 0.178 of its own adjudicated population, because its resolvability
test is TEXTUAL: a claim is rebuildable only if its own sentence names one of the record's four
ladders (N / H / GROSS / CADENCE).  1,658 claims were given NO number.  That silence is not
evidence that those walks had wide candidate sets; it is evidence about the PROSE.  Every one of
those units was emitted by a committed script, and a script that walked a ladder had to write
that ladder down in order to run it.  If the code kept what the sentence dropped, 1239's
population is ~5x larger than it published and the "median effective N = 3" claim is either
confirmed on the full census or exposed as a property of the writing-it-down subset.  This run
measures which.

THE POPULATION IS A CENSUS, PINNED TO 1239's OWN TREE.
    1230 (lane C, 2026-09-17) proved the record's censuses are REFLEXIVE: a census committed to
    the record changes the record it censused, so re-harvesting today CANNOT return 2,016 and no
    number here would be comparable to the one the queue asks about.  The corpus is therefore
    recovered from git at `d8729f9^`, the PARENT of the commit that added 1239's outputs, i.e.
    the tree 1239's census actually read.  G1/G2 require this run to reproduce 1239's committed
    `.census.csv` EXACTLY — all 34,089 unit ids, all three claim sets, the axis-naming counts —
    before any number below is trusted.  Today's HEAD corpus is harvested as a CONTROL and its
    size published beside the pinned one.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4; the queue names both)
    CLAIM SET {CS_STRICT, CS_PROX, CS_ALL} x RESOLUTION RULE {R_STRICT, R_LADDER, R_ANY,
    R_UNION} = 12 cells, EVERY ONE PUBLISHED (.recovery.csv) and every one also carried through
    the capital arm (.walkforward.csv).
      CLAIM SET — 1239's own three claim sets, each intersected with 1239's OWN unresolvability
      test (the unit's text names none of the four ladders).  Nested by construction; G5 checks.
        CS_STRICT   walk language + explicit candidate count + verdict word   (committed: 2,016
                    adjudicated, of which 1,658 unresolvable)   HEADLINE
        CS_PROX     walk language + explicit candidate count                  (4,349 / 3,697)
        CS_ALL      walk language                                             (13,049 / 11,646)
      RESOLUTION RULE — what counts as "the script carries a recoverable candidate set".  A
      candidate set in this record is a LADDER: one or more of the four axes plus its rungs.
      Nested by construction; G4 checks.
        R_STRICT  a module-level binding of an AXIS-NAMED target (LAD_N / NS / GROSSES /
                  CADENCES / ...) to a list or tuple of >= 2 literals, or an axis-keyed
                  ladder dict (`LADDERS = {"N": [...], ...}`).  The script NAMES the axis it
                  walked.  A tuple-unpacking binding (`LAG, WARMUP = 1, 260`) binds ONE constant
                  per name and is NOT a ladder; it is read as a POINT and reported separately.
        R_LADDER  R_STRICT plus CONTENT-INFERRED axes: an axis-free container (`RUNGS = [...]`,
                  `ARMS = [...]`) whose literals are typed to an axis by their own values —
                  cadence tokens to CADENCE, fractional 0.05..1.5 to GROSS, small integers to
                  N, day counts > 60 to H.  The script walks a ladder without naming it in the
                  identifier.  HEADLINE.
        R_ANY     R_LADDER plus any axis evidence anywhere in the file: a `for N in [...]` loop
                  over a literal list, an axis keyword argument given a literal list, or a
                  comprehension over one.  The ladder is in the code but not as a named
                  module-level constant.
        R_UNION   R_ANY plus the SIBLING PROSE: 1239's own four AXIS regexes applied to the
                  emitting script's module docstring and to every OTHER paragraph of the .md
                  file the unit came from.  This is the honest upper bound on "the prose lost
                  it" — a neighbouring sentence may have kept what this one dropped.
      A POINT IS NOT A CANDIDATE SET.  `GROSS = 0.75` tells you the axis was FIXED, not walked;
      it is counted as POINT, never as recovered, under every rule.  The count is published so
      the reader can see how much of the archive pins rather than walks.

ATTRIBUTION IS NOT A DIAL.  All four paths run on every unit in this fixed precedence, and each
path's marginal reach is published (.attrib.csv):
      A_STEM  the unit's own source file `X.result.md` / `X.memo.md` -> `X.py`.  The record's
              artefact convention and the only path that is an identity rather than a lookup.
      A_COL   a LEADERBOARD row's last column — PROTOCOL rule 5's script column.
      A_NAME  any `*.py` filename token appearing in the unit's own text.
      A_IDEA  a LEADERBOARD row opening `NNNN lane X` -> the committed script for idea NNNN in
              lane X.  Restricted to that pattern ON PURPOSE: an "idea 1239 found ..." mention
              inside a body paragraph names the PARENT idea, not the emitter, and attributing on
              it would silently mis-credit.  The count it would have added is published.
    Every unit gets AT MOST ONE script (G3) and the script must exist at the pinned vintage.

THE VALIDATION THAT DECIDES WHETHER A TRANSFER IS HONEST (ARM D).  A number recovered from code
is worth having only if code agrees with prose WHERE PROSE SPOKE.  1239's 358 resolvable claims
are exactly that control: each states its own axis set.  This run recovers the axis set from
their scripts too and reports containment, exact agreement and disagreement rates.  If code
disagrees with prose on the claims where prose is available, the 1,658 transfers are NOT
publishable and the run says so.  That check is pre-registered as H_AGREE and it is the gate the
answer to the queue's question hangs on.

PRE-DECLARED OUTCOMES (fixed before ARMS D and E were run; the verdict is read off, in order)
    (A) THE SCRIPT KEPT IT — >= 0.50 of the headline claim set recovers a candidate set under
        R_LADDER AND code agrees with prose on >= 0.80 of 1239's 358.  1239's population is
        then ~5x larger than it published and the transfer is a STAMP on committed text.
    (B) THE SCRIPT LOST IT TOO — < 0.25 recoverable.  The record did not drop a ladder it had;
        1239's silence stands as written.
    (C) RECOVERABLE BUT NOT TRANSFERABLE — recovery clears 0.50 and the prose-vs-code agreement
        does NOT clear 0.80.  The code carries A ladder but not THIS claim's ladder, and the
        honest answer to the queue is that attribution is too coarse to transfer a number.
    (D) ATTRIBUTION IS THE BINDING CONSTRAINT — more units fail for want of an identifiable
        emitting script than for want of a ladder inside the script they do have.

HYPOTHESES, PRE-REGISTERED
    HONESTY LABEL: ARMS A, B and C were wired and run in a prototype before this file was
    written, so H_REACH, H_CODE and H_STRICT below are MEASUREMENTS reported against 1239's
    committed file and are labelled CALIBRATED wherever quoted.  H_AGREE, H_NEFF, H_TAIL and
    H_CAPITAL were UNMEASURED when this file was written and are pre-registered.
      H_REACH   [CALIBRATED] >= 0.90 of the headline population resolves to a committed script
                that exists at the pinned vintage.
      H_CODE    [CALIBRATED] >= 0.50 of the headline population carries a recoverable candidate
                set under R_LADDER.  This is outcome (A)'s first leg.
      H_STRICT  [CALIBRATED] R_STRICT alone recovers strictly less than half of what R_LADDER
                does, i.e. the record mostly walks ladders it does not name in the identifier.
      H_AGREE   [PRE-REGISTERED] on 1239's 358 prose-resolvable claims the code-recovered axis
                set CONTAINS the prose-named axis set for >= 0.80 of them.
      H_NEFF    [PRE-REGISTERED] the median transferred N_eff^PR over the newly resolved claims
                is <= 2.0, i.e. 1239's "median effective N = 3" is not an artefact of the
                writing-it-down subset and the wider census is no less degenerate.
      H_TAIL    [PRE-REGISTERED] the transferred median STATED N over the newly resolved claims
                exceeds the transferred median effective N by at least 10x, reproducing 1239's
                51-vs-3 gap on the population it could not read.
      H_CAPITAL [PRE-REGISTERED] no (claim set, rule) cell moves mean OOS Sharpe by more than
                0.02 against BOTH references.  A recoverability rule is a DISCLOSURE about the
                archive, not a filter on capital; if it does move money that is the finding.

DISCOVERED IN THE RUN, NOT PRE-DECLARED, AND STATED HERE BECAUSE IT DECIDES HOW ARM E READS:
the cite-map's ANY quantifier is SATURATED.  With 793 / 599 / 487 headline claims citing U56 /
B136 / SMALL and at least one of them recovering every one of the four ladders, "some citing
claim recovers this ladder" is TRUE at all 72 decisions in all 12 cells, so those twelve rows
are BIT-IDENTICAL to ACT ON ALL and H_CAPITAL is satisfied trivially rather than earned.  The
12 cells are still published (1071's declaration: an inert dial is reported inert, not counted
as twelve points), and a MAJORITY / ALL quantifier control is added alongside them — reported,
never a third dial, with no book selected on it — so the arm carries a non-degenerate reading
of what a recoverability rule would do to capital.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); ANCHOR {A, B}; the four
ladders N / H / GROSS / CADENCE; the three choosers CH_ISSHARPE / CH_ISCAGR / CH_ISDD; 1239's
three degeneracy bars B_TIGHT 0.0040 / B_MID 0.0100 / B_LOOSE 0.0171; the 4a and 4b legs; the
attribution paths.

FROZEN AT THE RECORD'S CONSTRUCTION (1101/1239): 3-leg composite (21/252, 0/126, 0/63),
above-200d eligibility, max_vol 0.60, 10 bps (rule 2), decide-at-t / apply-at-t+1, warm-up 260
rows, IS end 2016-12-31 (rule 8), 4b constants 0.60 / 0.70.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every pick made on the IS window
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book and every grid cell; rule 9 survivorship stated in the verdict.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches and committed git history only).
"""
from __future__ import annotations

import ast
import hashlib
import io
import re
import subprocess
import sys
import tarfile
import tempfile
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

DATE = "2026-09-18"
SLUG = "how-many-of-the-1-658-UNRESOLVABLE-WALK-CLAIMS-can-be-RESOLVED-FROM-THEIR-SCRIPT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

# ------------------------------------------------------------------ 1101/1239 construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]

ANCHORS = {
    "A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
    "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M"),
}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]
BARS = {"B_TIGHT": 0.0040, "B_MID": 0.0100, "B_LOOSE": 0.0171}   # 1239's own three bars

SEED_BASE = 12461246

# ------------------------------------------------------------------ the two dials
CLAIMSETS = ["CS_STRICT", "CS_PROX", "CS_ALL"]
CS_HEAD = "CS_STRICT"
RULES = ["R_STRICT", "R_LADDER", "R_ANY", "R_UNION"]
R_HEAD = "R_LADDER"

# ------------------------------------------------------------------ the pinned corpus
PIN_COMMIT = "d8729f9^"          # the PARENT of 1239's commit: the tree 1239's census read
PIN_LABEL = "d8729f9^ (parent of 1239's commit)"

# ------------------------------------------------------------------ 1239's committed numbers
A1239_CENSUS = ROOT / "research" / "backtests" / (
    "2026-09-17_is-the-record-s-CANDIDATE-SET-half-CLONES-on-every-axis-it-has-ever-WALKED"
    "_cloud.census.csv")
A1239_UNITS = 34089
A1239_MD = 1166
A1239_SETS = {"CS_ALL": dict(units=13049, axis=1403, gross=746),
              "CS_PROX": dict(units=4349, axis=652, gross=360),
              "CS_STRICT": dict(units=2016, axis=358, gross=185)}
A1239_UNRESOLVABLE = 1658
A1239_MED_STATED_N = 51.0
A1239_MED_NEFF = 3.0
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<74s} {value:.4e}")
    return bool(ok)


# ================================================================== the record's runner (1101)
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


class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if name == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG)
            m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def book(pan, N, H, gross, freq):
    """Decide at the rebalance close t, apply at t+1 (rule 2), 10 bps on turnover."""
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    return r - turn * COST / 1e4


def ladder_books(pan, anchor, lad, cache):
    a = ANCHORS[anchor]
    out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        key = (pan.name, kw["N"], kw["H"], kw["gross"], kw["freq"])
        if key not in cache:
            cache[key] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"])
        out[rung] = cache[key]
    return out


def is_stat(r, ins, stat):
    c, s, d = fmet(np.asarray(r)[ins])
    return {"CH_ISSHARPE": s, "CH_ISCAGR": c, "CH_ISDD": -abs(d)}[stat]


# ================================================================== 1239's degeneracy readings
def n_eff_sl(vals, bar):
    """Single-linkage components of the |dSharpe| <= bar graph — 1239's function, verbatim."""
    v = np.sort(np.asarray([x for x in vals if np.isfinite(x)], float))
    if len(v) == 0:
        return 0
    return len(np.split(v, np.flatnonzero(np.diff(v) > bar) + 1))


def n_eff_pr(mat):
    """Participation ratio of the candidates' correlation matrix — 1239's bar-free reading."""
    X = np.asarray(mat, float)
    X = X[:, np.isfinite(X).all(axis=0)]
    sd = X.std(axis=0, ddof=0)
    X = X[:, sd > 0]
    if X.shape[1] == 0:
        return np.nan
    R = np.atleast_2d(np.corrcoef(X, rowvar=False))
    lam = np.clip(np.linalg.eigvalsh(R), 0, None)
    s1, s2 = lam.sum(), (lam ** 2).sum()
    return float(s1 * s1 / s2) if s2 > 0 else np.nan


# ================================================================== ARM A: 1239's census, pinned
WALK = re.compile(r"\b(walk\w*|swept|sweep\w*|ladder\w*|grid|candidate set|candidate-set|"
                  r"comparison set|comparison-set|alternatives?|rungs?|arms?|variants?)\b", re.I)
COUNT = re.compile(r"\b(\d{1,4})\s+(?:distinct\s+|candidate\s+|rung\s+|non-incumbent\s+)?"
                   r"(alternatives?|candidates?|books?|rungs?|arms?|variants?|cells?|ladders?)\b",
                   re.I)
VERDICT = re.compile(r"\b(KEEP|KILL|PARK|PASS|FAIL|decisive|refuted|confirmed|survives?|"
                     r"does not survive|verdict)\b")
AXIS = {a: re.compile(rf"\b{a}\b") for a in ("GROSS", "CADENCE")}
AXIS["N"] = re.compile(r"\bN\s*=\s*\d+|\bN LADDER|\bN ladder|\bthe N axis\b")
AXIS["H"] = re.compile(r"\bH\s*=\s*\d+|\bH LADDER|\bH ladder|\bthe H axis\b")


def units_of(rroot):
    """1239's unit definition, verbatim: LEADERBOARD rows, CHANGELOG paragraphs, md paragraphs."""
    U = []
    for ln in (rroot / "LEADERBOARD.md").read_text(errors="ignore").split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in (rroot / "CHANGELOG.md").read_text(errors="ignore").split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    nmd = 0
    for f in sorted((rroot / "backtests").rglob("*.md")):
        nmd += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, nmd


def census_of(U):
    """1239's census(), verbatim (uid included, so G2 can compare unit for unit)."""
    rows = []
    for src, txt in U:
        w = bool(WALK.search(txt))
        cs = [int(m.group(1)) for m in COUNT.finditer(txt)]
        cs = [c for c in cs if 2 <= c <= 2000]
        ver = bool(VERDICT.search(txt))
        ax = [a for a, p in AXIS.items() if p.search(txt)]
        rows.append(dict(uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10], src=src,
                         WALK=w, n_counts=len(cs), stated_N=(max(cs) if cs else np.nan),
                         VERDICT=ver, axes="|".join(sorted(ax)), n_axes=len(ax),
                         names_GROSS=("GROSS" in ax),
                         CS_ALL=bool(w), CS_PROX=bool(w and cs),
                         CS_STRICT=bool(w and cs and ver), _txt=txt))
    return pd.DataFrame(rows)


# ================================================================== ARM B: attribution
PYTOK = re.compile(r"[0-9A-Za-z_][0-9A-Za-z_.\-]*\.py\b")
LBROW_IDEA = re.compile(r"^\|\s*20\d\d-\d\d-\d\d\s*\|\s*\**\s*(\d{3,4})\s+lane\s+([A-Za-z]+)")
BODY_IDEA = re.compile(r"\bidea\s+(\d{3,4})\b", re.I)
MDSTEM = re.compile(r"^(?P<stem>.+?)\.(result|memo|MEMO|README|notes)\.md$")
APATHS = ("A_STEM", "A_COL", "A_NAME", "A_IDEA")


def script_index(sroot):
    byname, byidea = {}, {}
    for f in sorted(sroot.glob("*.py")):
        byname[f.name] = f
        m = re.search(r"_(C|B|A|D|cloud|local)\.py$", f.name)
        lane = m.group(1) if m else None
        head = "\n".join(f.read_text(errors="ignore").split("\n")[:8])
        mi = BODY_IDEA.search(head)
        if mi and lane:
            byidea.setdefault((mi.group(1), lane.lower()), f)
    return byname, byidea


def attribute(C, byname, byidea):
    recs = []
    body_only = 0
    for i, row in C.iterrows():
        src, txt = row["src"], row["_txt"]
        hit = {p: None for p in APATHS}
        m = MDSTEM.match(src)
        if m:
            cand = m.group("stem") + ".py"
            if cand in byname:
                hit["A_STEM"] = cand
        if src == "LEADERBOARD":
            cells = [c.strip() for c in txt.strip().strip("|").split("|")]
            if cells:
                last = cells[-1].strip().strip("`* ")
                if last in byname:
                    hit["A_COL"] = last
            mi = LBROW_IDEA.match(txt)
            if mi and (mi.group(1), mi.group(2).lower()) in byidea:
                hit["A_IDEA"] = byidea[(mi.group(1), mi.group(2).lower())].name
        for tok in PYTOK.findall(txt):
            t = tok.strip("`*")
            if t in byname:
                hit["A_NAME"] = t
                break
        chosen, path = None, "NONE"
        for p in APATHS:
            if hit[p]:
                chosen, path = hit[p], p
                break
        if chosen is None:
            mb = BODY_IDEA.search(txt)
            if mb and any(k[0] == mb.group(1) for k in byidea):
                body_only += 1
        recs.append(dict(uid=i, src=src, script=chosen, path=path,
                         **{f"hit_{p}": (hit[p] or "") for p in APATHS}))
    return pd.DataFrame(recs).set_index("uid"), body_only


# ================================================================== ARM C: candidate set in code
AXNAME = {
    "N": re.compile(r"^(NS|N_LAD|LAD_N|N_GRID|GRID_N|N_RUNGS|NVALS|N_LIST|NSET|N_LADDER|"
                    r"LADDER_N|TOPN|N_VALUES|NLAD|N_SET|NN|NS_ALL|N_ALL)$"),
    "H": re.compile(r"^(HS|LAD_H|H_LAD|H_GRID|GRID_H|HOLDS|HOLD_LAD|H_RUNGS|HVALS|H_LIST|"
                    r"H_LADDER|LADDER_H|MINHOLDS|HLAD|H_SET|H_ALL|HOLD_RUNGS)$"),
    "GROSS": re.compile(r"^(GROSSES|GS|LAD_G|LAD_GROSS|G_GRID|GRID_G|GROSS_RUNGS|GVALS|G_LIST|"
                        r"GROSS_LAD|LADDER_G|GROSS_GRID|GLAD|GROSS_SET|GROSS_LADDER|G_ALL)$"),
    "CADENCE": re.compile(r"^(CADENCES|CADS|FREQS|LAD_C|CAD_LAD|CADENCE_LAD|FREQ_GRID|LADDER_C|"
                          r"C_LIST|FREQ_LAD|CLAD|CADENCE_SET|CADENCE_GRID|FREQ_SET|FREQS_ALL)$"),
}
AXKW = {"N": {"n", "N", "topn", "nsel"}, "H": {"h", "H", "hold", "minhold"},
        "GROSS": {"gross", "GROSS", "g"}, "CADENCE": {"freq", "cadence", "FREQ", "CADENCE"}}
DICTNAME = re.compile(r"^(LADDERS?|LAD|LADK|LADDER|DEFAULT_RUNG|LAD_ALL|LADDERS_ALL|GRIDS?)$")
CADTOK = {"D", "W", "M", "Q", "2W", "W-FRI", "BM", "2M", "A", "Y", "B", "SM"}


def const_list(v):
    if isinstance(v, (ast.List, ast.Tuple)) and len(v.elts) >= 2 \
            and all(isinstance(e, ast.Constant) for e in v.elts):
        return [e.value for e in v.elts]
    return None


def axis_by_content(vals):
    """Type a bare container to one of the record's four axes by its own literals."""
    if not vals:
        return None
    if all(isinstance(x, str) for x in vals):
        S = {x.upper() for x in vals}
        return "CADENCE" if S and S <= CADTOK else None
    if all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in vals):
        f = [float(x) for x in vals]
        if all(0.05 <= x <= 1.5 for x in f) and any(not float(x).is_integer() for x in f):
            return "GROSS"
        if all(float(x).is_integer() for x in f):
            iv = [int(x) for x in f]
            if all(2 <= x <= 60 for x in iv):
                return "N"
            if all(5 <= x <= 756 for x in iv) and max(iv) > 60:
                return "H"
    return None


def recover_set(path: Path):
    """rule -> {axis: rungs} recovered from this script's CODE, plus the POINT pins it states.
    R_STRICT c R_LADDER c R_ANY by construction (each starts from the previous)."""
    try:
        tree = ast.parse(path.read_text(errors="ignore"))
    except Exception:                                            # noqa: BLE001
        return {r: {} for r in ("R_STRICT", "R_LADDER", "R_ANY")}, {}
    strict, cont, anyv, points = {}, {}, {}, {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            unpack = any(isinstance(t, (ast.Tuple, ast.List)) for t in node.targets)
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            upnames = []
            if unpack:
                for t in node.targets:
                    if isinstance(t, (ast.Tuple, ast.List)):
                        upnames += [e.id for e in t.elts if isinstance(e, ast.Name)]
            v = node.value
            # a POINT pin: one constant bound to an axis-named target (scalar or unpacked)
            if isinstance(v, ast.Constant):
                for n in names:
                    for a, p in AXNAME.items():
                        if p.match(n):
                            points.setdefault(a, v.value)
            if unpack and isinstance(v, (ast.Tuple, ast.List)) \
                    and len(v.elts) == len(upnames) \
                    and all(isinstance(e, ast.Constant) for e in v.elts):
                for n, e in zip(upnames, v.elts):
                    for a, p in AXNAME.items():
                        if p.match(n):
                            points.setdefault(a, e.value)
                continue                                  # unpacking binds points, not ladders
            if unpack:
                continue
            cl = const_list(v)
            if cl:
                for n in names:
                    for a, p in AXNAME.items():
                        if p.match(n):
                            strict.setdefault(a, cl)
                ac = axis_by_content(cl)
                if ac:
                    cont.setdefault(ac, cl)
            if isinstance(v, ast.Dict):
                isladdict = any(DICTNAME.match(n) for n in names)
                for k, vv in zip(v.keys, v.values):
                    cl2 = const_list(vv)
                    if cl2 is None:
                        continue
                    kv = k.value if isinstance(k, ast.Constant) else None
                    if isladdict and isinstance(kv, str) and kv.upper() in LADDERS:
                        strict.setdefault(kv.upper(), cl2)
                    ac = axis_by_content(cl2)
                    if ac:
                        cont.setdefault(ac, cl2)
        # R_ANY: a literal ladder reached through a loop, a keyword argument or a comprehension
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            cl = const_list(node.iter)
            if cl:
                for a, p in AXNAME.items():
                    if p.match(node.target.id) or node.target.id in AXKW[a]:
                        anyv.setdefault(a, cl)
                ac = axis_by_content(cl)
                if ac:
                    anyv.setdefault(ac, cl)
        if isinstance(node, ast.comprehension) and isinstance(node.target, ast.Name):
            cl = const_list(node.iter)
            if cl:
                for a in LADNAMES:
                    if node.target.id in AXKW[a] or AXNAME[a].match(node.target.id):
                        anyv.setdefault(a, cl)
                ac = axis_by_content(cl)
                if ac:
                    anyv.setdefault(ac, cl)
        if isinstance(node, ast.Call):
            for kwn in node.keywords:
                cl = const_list(kwn.value) if kwn.arg else None
                if cl:
                    for a in LADNAMES:
                        if kwn.arg in AXKW[a]:
                            anyv.setdefault(a, cl)
    out = {}
    out["R_STRICT"] = dict(strict)
    r2 = dict(cont)
    r2.update(strict)
    out["R_LADDER"] = r2
    r3 = dict(anyv)
    r3.update(r2)
    out["R_ANY"] = r3
    return out, points


def prose_axes(text):
    return {a for a, p in AXIS.items() if p.search(text)}


def sibling_prose(src, script_path, mdcache):
    """R_UNION's extra evidence: the emitting script's docstring + every OTHER paragraph of the
    .md file the unit came from."""
    ax = set()
    if script_path is not None:
        try:
            doc = ast.get_docstring(ast.parse(script_path.read_text(errors="ignore"))) or ""
        except Exception:                                        # noqa: BLE001
            doc = ""
        ax |= prose_axes(doc)
    ax |= mdcache.get(src, set())
    return ax


# ================================================================== 4a / 4b legs
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


# ================================================================== the cite-map (capital arm)
PANTOK = {
    "U56": re.compile(r"\bU56\b|\buniverse\.json\b|\b56[- ]name", re.I),
    "B136": re.compile(r"\bB13[56]\b|\bbroad\b|prices_broad", re.I),
    "SMALL": re.compile(r"\bSMALL\d*\b|\bsmall[- ]cap", re.I),
}


def main():
    t_start = time.time()
    P("=" * 112)
    P(f"IDEA 1246 (lane C, {DATE}) — HOW MANY OF THE 1,658 UNRESOLVABLE WALK CLAIMS CAN BE")
    P("RESOLVED FROM THEIR SCRIPT?")
    P("=" * 112)
    P("")
    P("  DIALS (2, PROTOCOL rule 4): CLAIM SET {CS_STRICT, CS_PROX, CS_ALL} x")
    P("                              RESOLUTION RULE {R_STRICT, R_LADDER, R_ANY, R_UNION}")
    P(f"  HEADLINE CELL: {CS_HEAD} x {R_HEAD}.  All 12 cells published (.recovery.csv).")
    P("")

    # ---------------------------------------------------------------- ARM A: the pinned census
    P("=" * 112)
    P("ARM A — THE POPULATION, PINNED TO 1239's OWN TREE  [CALIBRATED: the counts in this arm")
    P("        were measured in a wiring prototype before this file was written]")
    P("=" * 112)
    P("")
    P("  1230 proved the record's censuses are REFLEXIVE, so the corpus is recovered")
    P(f"  from git at {PIN_LABEL} — the tree 1239's census actually read.")
    tmp = tempfile.mkdtemp()
    try:
        blob = subprocess.run(["git", "archive", PIN_COMMIT, "research"],
                              cwd=str(ROOT), capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(blob)) as tf:
            tf.extractall(tmp)
        got_pin = True
    except Exception as e:                                       # noqa: BLE001
        P(f"  !! git archive FAILED: {e}")
        got_pin = False
    gate("G0", f"the pinned corpus {PIN_LABEL} was recovered from git", float(got_pin), got_pin)
    if not got_pin:
        raise SystemExit("cannot pin the corpus; the population would not be 1239's")
    PR = Path(tmp) / "research"

    U, n_md = units_of(PR)
    C = census_of(U)
    C.drop(columns=["_txt"]).to_csv(f"{OUT}.census.csv.gz", index=False,
                                   compression={"method": "gzip", "mtime": 0})
    P("")
    P(f"  PINNED corpus: {len(U)} text units over {n_md} committed .md files + LEADERBOARD "
      f"+ CHANGELOG.")
    gate("G1", "pinned unit count == 1239's committed 34,089", abs(len(U) - A1239_UNITS),
         len(U) == A1239_UNITS)
    gate("G1b", "pinned .md file count == 1239's committed 1,166", abs(n_md - A1239_MD),
         n_md == A1239_MD)
    ref = pd.read_csv(A1239_CENSUS)
    same_uid = set(C.uid) == set(ref.uid)
    gate("G2", "this run's unit-id SET == 1239's committed census.csv, unit for unit",
         float(same_uid), same_uid)
    P("")
    P("    claim set    units   1239's   names an AXIS   1239's   UNRESOLVABLE (no axis named)")
    ok_sets = True
    for cs in CLAIMSETS:
        z = C[C[cs]]
        nax = int(z.n_axes.gt(0).sum())
        r = A1239_SETS[cs]
        ok_sets &= (len(z) == r["units"]) and (nax == r["axis"])
        P(f"    {cs:10s} {len(z):7d}  {r['units']:7d}   {nax:13d}  {r['axis']:7d}   "
          f"{len(z)-nax:7d}")
    gate("G3", "all three claim sets and their axis-naming counts == 1239's committed table",
         float(ok_sets), ok_sets)
    POP = {}
    for cs in CLAIMSETS:
        POP[cs] = C[C[cs] & (C.n_axes == 0)].copy()
    gate("G4", f"the headline unresolvable population == the queue's {A1239_UNRESOLVABLE:,}",
         abs(len(POP[CS_HEAD]) - A1239_UNRESOLVABLE),
         len(POP[CS_HEAD]) == A1239_UNRESOLVABLE)
    nest = (set(POP["CS_STRICT"].uid) <= set(POP["CS_PROX"].uid) <=
            set(POP["CS_ALL"].uid))
    gate("G5", "the three claim sets are NESTED as declared", float(nest), nest)
    RESOLVED_PROSE = C[C[CS_HEAD] & (C.n_axes > 0)].copy()      # 1239's own 358
    P("")
    P(f"  HEADLINE POPULATION: {len(POP[CS_HEAD])} unresolvable claims; 1239's own resolvable "
      f"control is {len(RESOLVED_PROSE)}.")
    # the CONTROL: today's HEAD corpus, published beside the pinned one, never used as data
    Uh, nmdh = units_of(ROOT / "research")
    Ch = census_of(Uh)
    P(f"  CONTROL (today's HEAD, {len(Uh)} units / {nmdh} .md files): CS_STRICT "
      f"{int(Ch.CS_STRICT.sum())}, unresolvable "
      f"{int((Ch.CS_STRICT & (Ch.n_axes == 0)).sum())} — reflexivity (1230), which is exactly")
    P("  why every number below is about the PINNED tree and says so.")

    # ---------------------------------------------------------------- ARM B: attribution
    P("")
    P("=" * 112)
    P("ARM B — ATTRIBUTION: DOES EACH CLAIM RESOLVE TO A COMMITTED SCRIPT?  [CALIBRATED]")
    P("=" * 112)
    byname, byidea = script_index(PR / "backtests")
    P("")
    P(f"  {len(byname)} committed .py at the pinned vintage; {len(byidea)} (idea, lane) keys.")
    ATT, ATTMAP = {}, {}
    arows = []
    for cs in CLAIMSETS:
        A, body_only = attribute(POP[cs], byname, byidea)
        ATT[cs] = A
        vc = A.path.value_counts().to_dict()
        marg = {p: int((A[f"hit_{p}"] != "").sum()) for p in APATHS}
        arows.append(dict(claim_set=cs, n=len(A), resolved=int(A.script.notna().sum()),
                          reach=float(A.script.notna().mean()),
                          **{f"chosen_{p}": int(vc.get(p, 0)) for p in APATHS},
                          none=int(vc.get("NONE", 0)),
                          **{f"reach_{p}": marg[p] for p in APATHS},
                          body_idea_would_add=body_only))
    AT = pd.DataFrame(arows)
    AT.to_csv(f"{OUT}.attrib.csv", index=False)
    P("")
    P("    claim set    units   resolved    reach   A_STEM  A_COL  A_NAME  A_IDEA   NONE   "
      "[body-idea would add]")
    for _, r in AT.iterrows():
        P(f"    {r.claim_set:10s} {int(r.n):7d} {int(r.resolved):10d}   {r.reach:.4f}   "
          f"{int(r.chosen_A_STEM):6d} {int(r.chosen_A_COL):6d} {int(r.chosen_A_NAME):7d} "
          f"{int(r.chosen_A_IDEA):7d} {int(r.none):6d}   {int(r.body_idea_would_add):6d}")
    hd = AT[AT.claim_set == CS_HEAD].iloc[0]
    H_REACH = bool(hd.reach >= 0.90)
    P("")
    P(f"  H_REACH [CALIBRATED] reach >= 0.90 on {CS_HEAD}: {hd.reach:.4f} -> "
      f"{'SUPPORTED' if H_REACH else 'REFUTED'}")
    P("  MARGINAL REACH (units each path could reach, before the precedence): " +
      "  ".join(f"{p} {int(hd[f'reach_{p}'])}" for p in APATHS))
    one = all((ATT[cs].script.notna() == (ATT[cs].path != "NONE")).all() for cs in CLAIMSETS)
    gate("G6", "every attributed unit gets AT MOST ONE script (precedence is a function)",
         float(one), one)

    # ---------------------------------------------------------------- ARM C: recovery from code
    P("")
    P("=" * 112)
    P("ARM C — RECOVERY: DOES THE EMITTING SCRIPT CARRY THE CANDIDATE SET THE PROSE LOST?")
    P("         [CALIBRATED]")
    P("=" * 112)
    need = sorted({s for cs in CLAIMSETS for s in ATT[cs].script.dropna().unique()})
    REC, PTS = {}, {}
    for s in need:
        REC[s], PTS[s] = recover_set(byname[s])
    P("")
    P(f"  {len(need)} distinct emitting scripts parsed with `ast` (no execution).")
    # sibling prose per .md source, for R_UNION
    mdcache = {}
    for src in sorted({s for cs in CLAIMSETS for s in POP[cs].src.unique()}):
        if src in ("LEADERBOARD", "CHANGELOG"):
            mdcache[src] = set()
            continue
        f = PR / "backtests" / src
        mdcache[src] = prose_axes(f.read_text(errors="ignore")) if f.exists() else set()

    AXSET = {}                       # (claim set, rule) -> per-unit recovered axis set
    rrows = []
    for cs in CLAIMSETS:
        A = ATT[cs]
        for rule in RULES:
            got = []
            for uid, row in POP[cs].iterrows():
                s = A.at[uid, "script"]
                if not isinstance(s, str):
                    got.append(frozenset())
                    continue
                ax = set(REC[s]["R_ANY" if rule == "R_UNION" else rule].keys())
                if rule == "R_UNION":
                    ax |= sibling_prose(row["src"], byname[s], mdcache)
                got.append(frozenset(ax))
            AXSET[(cs, rule)] = got
            n_rec = sum(1 for g in got if g)
            rrows.append(dict(claim_set=cs, rule=rule, n=len(got), recovered=n_rec,
                              share=n_rec / len(got) if len(got) else np.nan,
                              mean_axes=float(np.mean([len(g) for g in got])),
                              full4=sum(1 for g in got if len(g) == 4),
                              **{f"axis_{a}": sum(1 for g in got if a in g) for a in LADNAMES}))
    RC = pd.DataFrame(rrows)
    RC.to_csv(f"{OUT}.recovery.csv", index=False)
    P("")
    P("    claim set    rule       units   recovered    share   mean |axes|   all 4    "
      "N     H  GROSS   CADENCE")
    for _, r in RC.iterrows():
        P(f"    {r.claim_set:10s} {r.rule:10s} {int(r.n):7d} {int(r.recovered):11d}   "
          f"{r.share:.4f}   {r.mean_axes:11.3f}   {int(r.full4):5d} {int(r.axis_N):5d} "
          f"{int(r.axis_H):5d} {int(r.axis_GROSS):6d} {int(r.axis_CADENCE):9d}")
    h_strict = RC[(RC.claim_set == CS_HEAD) & (RC.rule == "R_STRICT")].iloc[0]
    h_head = RC[(RC.claim_set == CS_HEAD) & (RC.rule == R_HEAD)].iloc[0]
    H_CODE = bool(h_head.share >= 0.50)
    H_STRICT = bool(h_strict.recovered < 0.5 * h_head.recovered)
    P("")
    P(f"  H_CODE   [CALIBRATED] >= 0.50 recoverable under {R_HEAD} on {CS_HEAD}: "
      f"{h_head.share:.4f} -> {'SUPPORTED' if H_CODE else 'REFUTED'}")
    P(f"  H_STRICT [CALIBRATED] R_STRICT recovers < half of {R_HEAD}: "
      f"{int(h_strict.recovered)} vs {int(h_head.recovered)} -> "
      f"{'SUPPORTED' if H_STRICT else 'REFUTED'}")
    nested_ok = True
    for cs in CLAIMSETS:
        for a, b in zip(RULES, RULES[1:]):
            nested_ok &= all(x <= y for x, y in zip(AXSET[(cs, a)], AXSET[(cs, b)]))
    gate("G7", "the four resolution rules are NESTED unit by unit, as declared",
         float(nested_ok), nested_ok)
    npoint = sum(1 for uid in POP[CS_HEAD].index
                 if isinstance(ATT[CS_HEAD].at[uid, "script"], str)
                 and PTS[ATT[CS_HEAD].at[uid, "script"]])
    P("")
    P(f"  POINTS, NOT LADDERS: {npoint} of {len(POP[CS_HEAD])} headline claims resolve to a")
    P("  script that PINS at least one axis to a single constant.  A pin is not a candidate set")
    P("  and is never counted as recovered.")
    blocked = int(len(POP[CS_HEAD]) - h_head.recovered)
    no_script = int(hd.none)
    P(f"  WHAT BLOCKS THE REST under {R_HEAD}: {blocked} unrecovered, of which {no_script} have")
    P(f"  NO identifiable script at all and {blocked - no_script} have a script that carries no")
    P("  ladder.  OUTCOME (D) [attribution is the binding constraint] therefore reads "
      f"{'TRUE' if no_script > blocked - no_script else 'FALSE'}.")

    # ---------------------------------------------------------------- ARM D: does code == prose?
    P("")
    P("=" * 112)
    P("ARM D — THE VALIDATION THAT DECIDES WHETHER A TRANSFER IS HONEST, AND THE TRANSFER")
    P("=" * 112)
    P("")
    P(f"  1239's {len(RESOLVED_PROSE)} PROSE-RESOLVABLE claims are the control: each states its")
    P("  own axis set.  Recover the axis set from their scripts too and compare.")
    Actrl, _ = attribute(RESOLVED_PROSE, byname, byidea)
    vrows = []
    for rule in RULES:
        n_res, contain, exact, disj, n_cmp = 0, 0, 0, 0, 0
        for uid, row in RESOLVED_PROSE.iterrows():
            s = Actrl.at[uid, "script"]
            pr_ax = {a for a in LADNAMES if a in str(row["axes"]).split("|")}
            if not isinstance(s, str):
                continue
            n_res += 1
            ax = set(REC[s]["R_ANY" if rule == "R_UNION" else rule].keys()) \
                if s in REC else set()
            if s not in REC:
                REC[s], PTS[s] = recover_set(byname[s])
                ax = set(REC[s]["R_ANY" if rule == "R_UNION" else rule].keys())
            if rule == "R_UNION":
                ax |= sibling_prose(row["src"], byname[s], mdcache)
            if not ax:
                continue
            n_cmp += 1
            if pr_ax <= ax:
                contain += 1
            if pr_ax == ax:
                exact += 1
            if not (pr_ax & ax):
                disj += 1
        vrows.append(dict(rule=rule, n_control=len(RESOLVED_PROSE), attributed=n_res,
                          code_nonempty=n_cmp, contains_prose=contain,
                          containment=contain / n_cmp if n_cmp else np.nan,
                          exact=exact, exact_rate=exact / n_cmp if n_cmp else np.nan,
                          disjoint=disj, disjoint_rate=disj / n_cmp if n_cmp else np.nan))
    VA = pd.DataFrame(vrows)
    VA.to_csv(f"{OUT}.validation.csv", index=False)
    P("")
    P("    rule       control  attributed  code non-empty   contains prose   exact   disjoint")
    for _, r in VA.iterrows():
        P(f"    {r.rule:10s} {int(r.n_control):7d} {int(r.attributed):11d} "
          f"{int(r.code_nonempty):15d}   {int(r.contains_prose):6d} = {r.containment:.4f}   "
          f"{r.exact_rate:.4f}   {r.disjoint_rate:.4f}")
    vh = VA[VA.rule == R_HEAD].iloc[0]
    H_AGREE = bool(vh.containment >= 0.80)
    P("")
    P(f"  H_AGREE [PRE-REGISTERED] containment >= 0.80 under {R_HEAD}: {vh.containment:.4f} "
      f"-> {'SUPPORTED' if H_AGREE else 'REFUTED'}")

    P("")
    P("  THE TRANSFER.  For each recovered axis set the candidate set is REBUILT on this tape")
    P("  exactly as 1239 rebuilt its 358, and K / N_eff^PR / N_eff^SL are read off.  Books are")
    P("  built once per (panel, axis, rung); N_eff is a property of the SET, so it is computed")
    P("  per axis-subset and transferred, never re-fitted per claim.")
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pxs = load_universe(small=True)
    mv = pxs.pct_change().abs().max()
    drop = [c for c in pxs.columns if c != "SPY" and not (mv[c] < 1.0)]
    px["SMALL"] = pxs.drop(columns=drop)
    pans = {n: Panel(n, px[n]) for n in PANELS}
    P("")
    P(f"  CACHE VINTAGE: {px['U56'].index[-1].date()}.  PANELS: U56 "
      f"{len(px['U56'].columns)-1} names; B136 {len(px['B136'].columns)-1}; SMALL "
      f"{len(px['SMALL'].columns)-1} investable ({len(drop)} dropped for max_1d_move >= 1.0).")
    cache, BOOKS = {}, {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                BOOKS[(pn, an, lad)] = ladder_books(pans[pn], an, lad, cache)
    a = ANCHORS["A"]
    r0 = cache[("U56", a["N"], a["H"], a["GROSS"], a["CADENCE"])]
    c0, s0, d0 = fmet(r0[pans["U56"].warm])
    dv = max(abs(c0 - A1101_TRIPLE[0]), abs(s0 - A1101_TRIPLE[1]), abs(d0 - A1101_TRIPLE[2]))
    P("")
    P(f"  1101's committed U56 anchor triple {A1101_TRIPLE[0]:.6f} / {A1101_TRIPLE[1]:.6f} / "
      f"{A1101_TRIPLE[2]:.6f}; this run {c0:.6f} / {s0:.6f} / {d0:.6f}")
    gate("G8", "1101's committed U56 anchor triple replays within the vintage drift", dv,
         dv < 6e-3)
    lbv = backtest(px["U56"], rules_v2_weights(px["U56"]), cost_bps=COST,
                   freq="W")["returns"].values
    lmdd = fmet(lbv[WARMUP:])[2]
    gate("G9", "live RULES v2 U56 MaxDD == committed -12.05%", abs(lmdd - LIVE_MAXDD_COMMITTED),
         abs(lmdd - LIVE_MAXDD_COMMITTED) < 5e-4)

    # N_eff per axis subset, on the anchor-A ladders, median over the three panels (1239's read)
    SUBSETS = [frozenset(s) for s in
               [{"N"}, {"H"}, {"GROSS"}, {"CADENCE"}, {"N", "H"}, {"N", "GROSS"},
                {"H", "GROSS"}, {"N", "CADENCE"}, {"GROSS", "CADENCE"}, {"H", "CADENCE"},
                {"N", "H", "GROSS"}, {"N", "H", "CADENCE"}, {"N", "GROSS", "CADENCE"},
                {"H", "GROSS", "CADENCE"}, {"N", "H", "GROSS", "CADENCE"}]]
    SUB = {}
    srows = []
    for axs in SUBSETS:
        keys = [(ax, r) for ax in sorted(axs) for r in LADDERS[ax]]
        keys = list(dict.fromkeys(keys))
        prs, sls = [], {b: [] for b in BARS}
        for pn in PANELS:
            pan = pans[pn]
            mat = np.column_stack([BOOKS[(pn, "A", ax)][r][pan.warm] for ax, r in keys])
            prs.append(n_eff_pr(mat))
            shs = [fsharpe(BOOKS[(pn, "A", ax)][r][pan.warm]) for ax, r in keys]
            for b, bv in BARS.items():
                sls[b].append(n_eff_sl(shs, bv))
        SUB[axs] = dict(K=len(keys), PR=float(np.median(prs)),
                        **{b: float(np.median(sls[b])) for b in BARS})
        srows.append(dict(axis_subset="|".join(sorted(axs)), **SUB[axs]))
    SUBF = pd.DataFrame(srows)
    SUBF.to_csv(f"{OUT}.subsets.csv", index=False)
    P("")
    P("    axis subset               K   N_eff^PR   N_eff SL @0.0040 / 0.0100 / 0.0171")
    for _, r in SUBF.iterrows():
        P(f"    {r.axis_subset:24s} {int(r.K):3d}   {r.PR:8.3f}   {r.B_TIGHT:6.1f} / "
          f"{r.B_MID:6.1f} / {r.B_LOOSE:6.1f}")

    trows = []
    for cs in CLAIMSETS:
        for rule in RULES:
            got = AXSET[(cs, rule)]
            sN = POP[cs].stated_N.values
            K, pr, sl = [], [], {b: [] for b in BARS}
            for g in got:
                if not g:
                    continue
                d = SUB[frozenset(g)]
                K.append(d["K"])
                pr.append(d["PR"])
                for b in BARS:
                    sl[b].append(d[b])
            nn = len(K)
            trows.append(dict(
                claim_set=cs, rule=rule, newly_resolved=nn,
                med_stated_N=float(np.nanmedian([x for x, g in zip(sN, got) if g])
                                   if nn else np.nan),
                med_K=float(np.median(K)) if nn else np.nan,
                med_NeffPR=float(np.median(pr)) if nn else np.nan,
                **{f"med_Neff_{b}": (float(np.median(sl[b])) if nn else np.nan) for b in BARS}))
    TR = pd.DataFrame(trows)
    TR.to_csv(f"{OUT}.transfer.csv", index=False)
    P("")
    P("    claim set    rule       newly resolved   med stated N   med K   med N_eff^PR   "
      "med N_eff@0.0040")
    for _, r in TR.iterrows():
        P(f"    {r.claim_set:10s} {r.rule:10s} {int(r.newly_resolved):14d}   "
          f"{r.med_stated_N:12.1f}   {r.med_K:5.1f}   {r.med_NeffPR:12.3f}   "
          f"{r.med_Neff_B_TIGHT:15.1f}")
    th = TR[(TR.claim_set == CS_HEAD) & (TR.rule == R_HEAD)].iloc[0]
    H_NEFF = bool(th.med_NeffPR <= 2.0)
    H_TAIL = bool(th.med_stated_N >= 10.0 * th.med_NeffPR)
    P("")
    P(f"  1239 published, on its 358: median stated N {A1239_MED_STATED_N:.0f}, median "
      f"effective N {A1239_MED_NEFF:.0f}.")
    P(f"  THIS RUN transfers, on the {int(th.newly_resolved)} newly resolved claims of the "
      f"headline cell:")
    P(f"      median stated N {th.med_stated_N:.1f}, median K {th.med_K:.1f}, median N_eff^PR "
      f"{th.med_NeffPR:.3f}, median N_eff@0.0040 {th.med_Neff_B_TIGHT:.1f}")
    P(f"  H_NEFF [PRE-REGISTERED] median transferred N_eff^PR <= 2.0: {th.med_NeffPR:.3f} -> "
      f"{'SUPPORTED' if H_NEFF else 'REFUTED'}")
    P(f"  H_TAIL [PRE-REGISTERED] median stated N >= 10x median effective N: "
      f"{th.med_stated_N:.1f} vs {10*th.med_NeffPR:.1f} -> "
      f"{'SUPPORTED' if H_TAIL else 'REFUTED'}")

    # ---------------------------------------------------------------- ARM E: capital, rule 8
    P("")
    P("=" * 112)
    P("ARM E — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    P("=" * 112)
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    oos_clean = all(not bool((pans[pn].ins & pans[pn].oos).any()) for pn in PANELS)
    gate("G10", "rule 8: the OOS window shares NO row with the IS window", float(oos_clean),
         oos_clean)
    BM = {}
    for pn in PANELS:
        pan = pans[pn]
        BM[(pn, "SPY")] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lv = backtest(px[pn], rules_v2_weights(px[pn]), cost_bps=COST, freq="W")["returns"].values
        BM[(pn, "LIVE")] = blocks_m(lv, pan.warm, pan.ins, pan.oos)
    P("")
    P("  (E1) every rung book, full sample and 2017-2026, 4a vs live RULES v2, 4b vs SPY.")
    brows = []
    for (pn, an, lad) in sorted({(x, y, z) for (x, y, z, _) in DEC}):
        pan = pans[pn]
        for rung, r in BOOKS[(pn, an, lad)].items():
            m = blocks_m(r, pan.warm, pan.ins, pan.oos)
            brows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rung), **m,
                              KEEP_4a=all(legs_4a(m, BM[(pn, "LIVE")]).values()),
                              KEEP_4b=all(legs_4b(m, BM[(pn, "SPY")]).values()),
                              KEEP_4b_OOS=all(legs_4b_oos(m, BM[(pn, "SPY")]).values())))
    BK = pd.DataFrame(brows).drop_duplicates(subset=["panel", "anchor", "ladder", "rung"])
    BK.to_csv(f"{OUT}.books.csv", index=False)
    P(f"       {len(BK)} rung-book rows.  4a {int(BK.KEEP_4a.sum())}; 4b full "
      f"{int(BK.KEEP_4b.sum())}; 4b OOS {int(BK.KEEP_4b_OOS.sum())}; BOTH "
      f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}.")
    for pn in PANELS:
        s, l = BM[(pn, "SPY")], BM[(pn, "LIVE")]
        P(f"       {pn:6s} SPY  full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:8.2%}"
          f"   OOS {s['OOS_CAGR']:7.2%} / {s['OOS_Sharpe']:.4f} / {s['OOS_MaxDD']:8.2%}")
        P(f"       {pn:6s} LIVE full {l['CAGR']:7.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:8.2%}"
          f"   OOS {l['OOS_CAGR']:7.2%} / {l['OOS_Sharpe']:.4f} / {l['OOS_MaxDD']:8.2%}")
    if int(BK.KEEP_4b.sum()):
        z = BK[BK.KEEP_4b].sort_values("OOS_Sharpe", ascending=False).head(4)
        P("")
        P("       4b PASSES (full sample), best OOS Sharpe first:")
        for _, r in z.iterrows():
            P(f"         {r.panel:6s} {r.anchor} {r.ladder:8s} rung {r.rung:>5s}  full "
              f"{r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:8.2%}   OOS {r.OOS_CAGR:7.2%} / "
              f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}   4b_OOS {bool(r.KEEP_4b_OOS)}")

    P("")
    P("  (E2) THE CITE-MAP.  A decision (panel, anchor, ladder, chooser) is R-ADMITTED when at")
    P("       least one committed claim in the population that CITES its panel and whose")
    P("       emitting script recovers THAT LADDER under rule R exists.  Admitted -> act on the")
    P("       decision's IS argmax; otherwise hold the anchor rung (do nothing).  Every pick is")
    P("       made on warm-up..2016-12-31 ONLY and 2017-2026 is read once (rule 8).")
    citepan = {}
    for cs in CLAIMSETS:
        for pn in PANELS:
            citepan[(cs, pn)] = POP[cs]["_txt"].map(
                lambda t: bool(PANTOK[pn].search(t))).values
    P("")
    P("       claims citing each panel (headline population):")
    P("       " + "  ".join(f"{pn} {int(citepan[(CS_HEAD, pn)].sum()):5d}" for pn in PANELS))
    pickmap, anchmap = {}, {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        vals = [is_stat(BOOKS[(pn, an, lad)][r], pan.ins, ch) for r in rungs]
        obs = rungs[int(np.nanargmax(np.where(np.isfinite(vals), vals, -np.inf)))]
        pickmap[(pn, an, lad, ch)] = blocks_m(BOOKS[(pn, an, lad)][obs],
                                              pan.warm, pan.ins, pan.oos)
        anchmap[(pn, an, lad, ch)] = blocks_m(BOOKS[(pn, an, lad)][ANCHORS[an][lad]],
                                              pan.warm, pan.ins, pan.oos)
    PK = pd.DataFrame([dict(panel=pn, anchor=an, ladder=lad, chooser=ch,
                            **{f"pick_{k}": v for k, v in pickmap[(pn, an, lad, ch)].items()},
                            **{f"anch_{k}": v for k, v in anchmap[(pn, an, lad, ch)].items()})
                       for (pn, an, lad, ch) in DEC])
    PK.to_csv(f"{OUT}.picks.csv", index=False)

    def summarise(mets):
        ks = list(DEC)
        return dict(
            mean_OOS_Sharpe=float(np.mean([mets[k]["OOS_Sharpe"] for k in ks])),
            mean_OOS_CAGR=float(np.mean([mets[k]["OOS_CAGR"] for k in ks])),
            mean_OOS_MaxDD=float(np.mean([mets[k]["OOS_MaxDD"] for k in ks])),
            mean_full_Sharpe=float(np.mean([mets[k]["Sharpe"] for k in ks])),
            KEEP_4a=int(sum(all(legs_4a(mets[k], BM[(k[0], "LIVE")]).values()) for k in ks)),
            KEEP_4b=int(sum(all(legs_4b(mets[k], BM[(k[0], "SPY")]).values()) for k in ks)),
            KEEP_4b_OOS=int(sum(all(legs_4b_oos(mets[k], BM[(k[0], "SPY")]).values())
                                for k in ks)))

    wrows = [dict(claim_set="REF", rule="REF_ACT_ON_ALL", n_admitted=len(DEC),
                  **summarise(pickmap)),
             dict(claim_set="REF", rule="REF_DO_NOTHING", n_admitted=0, **summarise(anchmap))]
    # REF_PROSE: 1239's own resolvability rule — admit only where the PROSE named the ladder
    prose_cite = {}
    for pn in PANELS:
        prose_cite[pn] = RESOLVED_PROSE["_txt"].map(
            lambda t: bool(PANTOK[pn].search(t))).values
    prose_ax = [{a for a in LADNAMES if a in str(x).split("|")}
                for x in RESOLVED_PROSE["axes"].values]
    admP = []
    for k in DEC:
        pn, an, lad, ch = k
        admP.append(any(c and (lad in ax) for c, ax in zip(prose_cite[pn], prose_ax)))
    mixP = {k: (pickmap[k] if ok else anchmap[k]) for k, ok in zip(DEC, admP)}
    wrows.append(dict(claim_set="REF", rule="REF_PROSE_1239", n_admitted=int(sum(admP)),
                      **summarise(mixP)))
    MIX = {}
    for cs in CLAIMSETS:
        for rule in RULES:
            got = AXSET[(cs, rule)]
            adm = []
            for k in DEC:
                pn, an, lad, ch = k
                cit = citepan[(cs, pn)]
                adm.append(any(c and (lad in g) for c, g in zip(cit, got)))
            MIX[(cs, rule)] = {k: (pickmap[k] if ok else anchmap[k]) for k, ok in zip(DEC, adm)}
            wrows.append(dict(claim_set=cs, rule=rule, n_admitted=int(sum(adm)),
                              **summarise(MIX[(cs, rule)])))
    # THE ADMISSION QUANTIFIER IS SATURATED AND IS REPORTED SO, NOT COUNTED AS TWELVE POINTS.
    # With hundreds of citing claims per panel, "at least one citing claim recovers this
    # ladder" is true for every (panel, ladder) at every cell, so the 12 rows above are
    # BIT-IDENTICAL to ACT ON ALL by construction.  1071's declaration requires this be said.
    # The quantifier control below is REPORTED, NEVER A THIRD DIAL: no book is selected on it.
    P("")
    P("       (E2b) THE CITE-MAP, per (panel, ladder), at the headline cell "
      f"{CS_HEAD} x {R_HEAD}: how many of the claims citing that panel recover THAT ladder.")
    gotH = AXSET[(CS_HEAD, R_HEAD)]
    cmrows = []
    share = {}
    for pn in PANELS:
        cit = citepan[(CS_HEAD, pn)]
        line = []
        for lad in LADNAMES:
            n_c = int(cit.sum())
            n_r = int(sum(1 for c, g in zip(cit, gotH) if c and lad in g))
            share[(pn, lad)] = (n_r / n_c) if n_c else np.nan
            cmrows.append(dict(panel=pn, ladder=lad, citing=n_c, recovering=n_r,
                               share=share[(pn, lad)]))
            line.append(f"{lad} {n_r:4d}/{n_c:4d} = {share[(pn, lad)]:.3f}")
        P(f"             {pn:6s} " + "   ".join(line))
    pd.DataFrame(cmrows).to_csv(f"{OUT}.citemap.csv", index=False)
    for q, fn in [("Q_ANY", lambda s: s > 0.0),
                  ("Q_MAJORITY", lambda s: s > 0.5),
                  ("Q_ALL", lambda s: s >= 1.0)]:
        adm = [bool(fn(share[(k[0], k[2])])) for k in DEC]
        mm = {k: (pickmap[k] if ok else anchmap[k]) for k, ok in zip(DEC, adm)}
        wrows.append(dict(claim_set="CONTROL", rule=q, n_admitted=int(sum(adm)),
                          **summarise(mm)))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    P("       claim set    rule              admitted   mean OOS Sharpe   mean OOS CAGR   "
      "mean OOS MaxDD   4a / 4b / 4b_OOS")
    for _, r in W8.iterrows():
        P(f"       {r.claim_set:12s} {r.rule:16s} {int(r.n_admitted):8d}   "
          f"{r.mean_OOS_Sharpe:15.4f}   {r.mean_OOS_CAGR:13.4f}   {r.mean_OOS_MaxDD:14.4f}   "
          f"{int(r.KEEP_4a)} / {int(r.KEEP_4b)} / {int(r.KEEP_4b_OOS)}")
    ref_all = W8[W8.rule == "REF_ACT_ON_ALL"].iloc[0]
    ref_none = W8[W8.rule == "REF_DO_NOTHING"].iloc[0]
    ref_prose = W8[W8.rule == "REF_PROSE_1239"].iloc[0]
    cells = W8[~W8.claim_set.isin(["REF", "CONTROL"])]
    w_none = float(np.nanmax(np.abs(cells.mean_OOS_Sharpe - ref_none.mean_OOS_Sharpe).values))
    w_all = float(np.nanmax(np.abs(cells.mean_OOS_Sharpe - ref_all.mean_OOS_Sharpe).values))
    H_CAPITAL = (w_none <= 0.02) and (w_all <= 0.02)
    best = cells.sort_values("mean_OOS_Sharpe", ascending=False).iloc[0]
    P("")
    P(f"       ACT ON ALL {ref_all.mean_OOS_Sharpe:.4f} | DO NOTHING "
      f"{ref_none.mean_OOS_Sharpe:.4f} | 1239's PROSE RULE {ref_prose.mean_OOS_Sharpe:.4f} "
      f"on {int(ref_prose.n_admitted)} admitted")
    P(f"       BEST CELL: {best.claim_set} x {best.rule} = {best.mean_OOS_Sharpe:.4f} on "
      f"{int(best.n_admitted)} admitted decisions")
    P(f"       WORST |move| against DO NOTHING {w_none:.4f}; against ACT ON ALL {w_all:.4f}")
    P(f"  H_CAPITAL [PRE-REGISTERED] no cell moves mean OOS Sharpe by > 0.02 against both "
      f"references -> {'SUPPORTED' if H_CAPITAL else 'REFUTED'}")
    inert = bool((cells.n_admitted == len(DEC)).all())
    gate("G11", "the ANY-quantifier admission rule is SATURATED and is reported inert, not "
         "as twelve points", float(inert), True)
    ctrl = W8[W8.claim_set == "CONTROL"]
    P("")
    P("       QUANTIFIER CONTROL (reported, NEVER a third dial — no book is selected on it):")
    for _, r in ctrl.iterrows():
        P(f"         {r.rule:12s} admitted {int(r.n_admitted):3d} of {len(DEC)}   mean OOS "
          f"Sharpe {r.mean_OOS_Sharpe:.4f}   OOS CAGR {r.mean_OOS_CAGR:.4f}   OOS MaxDD "
          f"{r.mean_OOS_MaxDD:.4f}   4a/4b/4b_OOS {int(r.KEEP_4a)}/{int(r.KEEP_4b)}/"
          f"{int(r.KEEP_4b_OOS)}")
    hcell = W8[(W8.claim_set == CS_HEAD) & (W8.rule == R_HEAD)].iloc[0]
    P("")
    P(f"       THE QUEUE'S OWN CELL ({CS_HEAD} x {R_HEAD}) vs 1239's PROSE RULE:")
    P(f"         admitted {int(hcell.n_admitted)} vs {int(ref_prose.n_admitted)} of "
      f"{len(DEC)} decisions; mean OOS Sharpe {hcell.mean_OOS_Sharpe:.4f} vs "
      f"{ref_prose.mean_OOS_Sharpe:.4f} (d {hcell.mean_OOS_Sharpe-ref_prose.mean_OOS_Sharpe:+.4f})")
    P(f"         mean OOS CAGR {hcell.mean_OOS_CAGR:.4f} vs {ref_prose.mean_OOS_CAGR:.4f}; "
      f"mean OOS MaxDD {hcell.mean_OOS_MaxDD:.4f} vs {ref_prose.mean_OOS_MaxDD:.4f}")
    P(f"         4a / 4b / 4b_OOS  {int(hcell.KEEP_4a)}/{int(hcell.KEEP_4b)}/"
      f"{int(hcell.KEEP_4b_OOS)} vs {int(ref_prose.KEEP_4a)}/{int(ref_prose.KEEP_4b)}/"
      f"{int(ref_prose.KEEP_4b_OOS)}")

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 112)
    P("VERDICT")
    P("=" * 112)
    GT = pd.DataFrame(GATES)
    GT.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(GT.pass_.sum())
    P("")
    P(f"  GATES {npass} of {len(GT)}.")
    if outcome_A := (H_CODE and H_AGREE):
        verdict = "(A) THE SCRIPT KEPT IT"
    elif h_head.share < 0.25:
        verdict = "(B) THE SCRIPT LOST IT TOO"
    elif H_CODE and not H_AGREE:
        verdict = "(C) RECOVERABLE BUT NOT TRANSFERABLE"
    else:
        verdict = "(MIXED) recovery between 0.25 and 0.50"
    if no_script > blocked - no_script:
        verdict += " + (D) ATTRIBUTION IS THE BINDING CONSTRAINT"
    P(f"  OUTCOME: {verdict}")
    P(f"  ANSWER TO THE QUEUE: of 1239's {len(POP[CS_HEAD])} unresolvable adjudicated walk")
    P(f"  claims, {int(h_head.recovered)} ({h_head.share:.4f}) have a candidate set recoverable")
    P(f"  from their emitting script under the headline rule {R_HEAD}; {int(h_strict.recovered)}")
    P("  ({:.4f}) under the strict named-axis rule.".format(h_strict.share))
    P("  CAPITAL: 4a {} of {} rung books; 4b full {}; 4b OOS {}. No new book is proposed and "
      "nothing is enacted (rule 6).".format(int(BK.KEEP_4a.sum()), len(BK),
                                            int(BK.KEEP_4b.sum()), int(BK.KEEP_4b_OOS.sum())))
    hyp = dict(H_REACH=H_REACH, H_CODE=H_CODE, H_STRICT=H_STRICT, H_AGREE=H_AGREE,
               H_NEFF=H_NEFF, H_TAIL=H_TAIL, H_CAPITAL=H_CAPITAL)
    P("  HYPOTHESES: " + "  ".join(f"{k} {'Y' if v else 'N'}" for k, v in hyp.items())
      + f"  ({sum(hyp.values())} of {len(hyp)})")
    P("")
    P(f"  runtime {time.time()-t_start:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
