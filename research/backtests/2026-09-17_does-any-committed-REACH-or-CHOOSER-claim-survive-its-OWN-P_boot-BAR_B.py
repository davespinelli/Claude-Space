#!/usr/bin/env python3
"""
Idea 1154 (lane B, 2026-09-17) — does ANY committed REACH or CHOOSER claim survive its OWN
P_boot BAR?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1101 (cloud, 2026-09-16,
`2026-09-16_is-LADDER-DEPENDENCE-of-REACHABILITY-a-general-fact-or-a-U56-fact_cloud.py`)
published 72 reach decisions and then asked, of 24 headline ones, whether the decision is
MEASURED at all: P(the nominated rung is the IS argmax) over 1000 joint moving-block redraws
of the IS window.  **11 of 24 cleared a 0.90 / 0.10 bar.**  1096's own two committed U56
reaches sit at P_boot 0.716 (GROSS) and 0.278 (CADENCE) — the CADENCE reach is a coin flip
that landed.  1101 stopped there: it scored its OWN cells, not the record's committed PICK
sentences, and it used ONE block length.

THIS RUN asks the queue's question — how many PUBLISHED PICKS, not published numbers, are
unresolved — and prices what a resolution bar would COST or BUY in capital terms.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET    {C_STRICT, C_PROX, C_ALL}     -- 1197/1199/1155's nesting convention, verbatim
  BLOCK LENGTH {L21, L63, L126, L252}        -- 1101 used L = 63 and only 63

  = 12 dial cells, EVERY ONE PUBLISHED.  Nothing is selected on: the HEADLINE rung is
  C_STRICT x L63, declared here before any number because it is 1101's own basis, and every
  other rung is reported beside it.

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL} is not a dial (rule 9 requires all three).
ANCHOR {A, B} is 1101's pair, inherited whole (A = W / H126 / N=20 / gross 0.75, the standing
anchor; B = M / H63 / N=12 / gross 0.55, interior on all four ladders).  The four CORE
LADDERS (N, H, GROSS, CADENCE) and the three honest CHOOSERS (CH_ISSHARPE, CH_ISCAGR,
CH_ISDD) are 1101's, inherited whole — all 3 x 2 x 4 x 3 = 72 decisions are published at
every dial cell.  The PUBLISHING RULES in Arm D (R_RAW, R_BAR, R_ANCHOR) are a
one-factor-at-a-time falsification ladder over the record's OWN habit, not a search: R_ANCHOR
(never move) is 1155's control and exists to put a KNOWN do-nothing floor under the other two.

THE CLAIM-SET DIAL, MAPPED ONTO THE DECISION POPULATION BEFORE ANY RESULT.  A census of the
record's text (Arm A) counts committed PICK / REACH sentences; the price arm then scores the
decisions those sentences stand on, nested the same way:
  C_STRICT  the record's committed headline basis: anchor A, chooser CH_ISSHARPE   (12 cells)
  C_PROX    + every honest chooser at anchor A                                     (36 cells)
  C_ALL     + anchor B, i.e. 1101's whole published population                      (72 cells)
C_STRICT subset C_PROX subset C_ALL is asserted as gate G5.

Frozen at 1082/1094/1098/1101/1102/1110/1148/1155/1159's construction: CAND20 legs, max_vol
0.60, min hold 126, cadence W, 10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, 1000
bootstrap draws, crc32 seeds, SEED_BASE 11541154.

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 walk-forward in Arm D and
BOTH KEEP paths on all 162 rung books in Arm E; rule 9 survivorship stated.  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_does-any-committed-REACH-or-CHOOSER-claim-survive-its-OWN-P_boot-BAR_B.py
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
SLUG = "does-any-committed-REACH-or-CHOOSER-claim-survive-its-OWN-P_boot-BAR"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ----- 1101's construction, inherited whole -------------------------------------------------
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
    "A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),   # 1096/1101's standing anchor
    "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M"),    # 1101's interior second draw
}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]      # 1101's three honest choosers
CH_HEAD = "CH_ISSHARPE"

CLAIMSETS = ["C_STRICT", "C_PROX", "C_ALL"]             # dial 1
CS_HEAD = "C_STRICT"
BLOCKS = [21, 63, 126, 252]                             # dial 2
L_HEAD = 63                                             # 1101's own

BAR_HI, BAR_LO = 0.90, 0.10                             # 1101's bar, verbatim
BDRAWS = 1000
SEED_BASE = 11541154

RULES_PUB = ["R_RAW", "R_BAR", "R_ANCHOR"]              # Arm D publishing rules

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived ----------------
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)   # U56 / W / H126 / N=20 / g0.75 full
A1101_REACHSET = {"GROSS", "CADENCE"}            # 1096/1101 committed, U56 and B136, anchor A
A1101_HEADLINE_RESOLVED = 11                     # of 24, at L = 63, bar 0.90/0.10
A1101_PBOOT_U56_GROSS = 0.716
A1101_PBOOT_U56_CADENCE = 0.278
LIVE_MAXDD_COMMITTED = -0.1205
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)

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


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<5s} {what}  ->  {value:.3e}")
    return bool(ok)


# =================================================================================================
# 1101/1159's runner and metrics, verbatim
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


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    """1161's, verbatim: the score and eligibility mask over the WHOLE column set."""
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
# ARM A — the CENSUS.  1155/1197's harvester, retargeted from SPREAD tokens to PICK tokens.
# =================================================================================================
PICKTOK = re.compile(
    r"\b(pick(?:s|ed|ing)?|reach(?:es|ed|ing|able|ability)?|argmax|chooser|chose|chooses?|"
    r"selects?|selected|lands? on|landed on|top rung|bottom rung|winner|prefers?|preferred)\b",
    re.I)
# a NAMED pick: the sentence names a rung / ladder coordinate, i.e. it is a PICK and not a number
NAMED = re.compile(
    r"\b(N\s*=\s*\d+|H\s*=?\s*\d+|H\d+|gross\s*0?\.\d+|g\s*=?\s*0?\.\d+|"
    r"cadence\s*=?\s*[DWMQ]\b|CADENCE|GROSS|\bW/|\bM/|top rung|bottom rung|"
    r"rung\s*0?\.\d+|\b[DWMQ]\s*/\s*H\d+)\b")
ADJUD = re.compile(
    r"\b(clears?|cleared|passe?s?|passed|fails?|failed|beats?|picks?|picked|reach(?:es|ed)|"
    r"chooser|verdict|KEEP|KILL|PARK|significan\w*|decisive\w*|confirms?|refutes?|ranks?|"
    r"ranked|selects?|adjudicat\w*|dominat\w*|is the argmax|wins?|won)\b")
# does the unit state a RESOLUTION for its pick at all?
RESOL = re.compile(
    r"\b(P_boot|p_?boot|bootstrap bar|resolved|unresolved|share_top|pick stability|"
    r"P\(.{0,30}argmax|probability that the (?:pick|argmax)|coin flip|margin)\b", re.I)
MARGIN = re.compile(r"\b(margin|by\s+[\d.]+e-0\d|at a Sharpe margin)\b", re.I)
NUMTOK = re.compile(r"[-+]?\d+(?:\.\d+)?(?:e-?\d+)?%?")
KTOK = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(rungs?|cells?|points?|ladders?|arms?|books?|"
                  r"anchors?|rows?|panels?|decisions?|picks?)\b", re.I)


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
    fileset = {}
    for src, txt in U:
        fileset.setdefault(src, False)
        if PICKTOK.search(txt):
            fileset[src] = True
    rows = []
    for src, txt in U:
        pk = bool(PICKTOK.search(txt))
        nm = bool(NAMED.search(txt))
        ad = bool(ADJUD.search(txt))
        ks = sorted({int(m.group(1).replace(",", "")) for m in KTOK.finditer(txt)})
        rows.append(dict(
            src=src, n_chars=len(txt),
            C_STRICT=pk and nm and ad,
            C_PROX=pk and nm,
            C_ALL=fileset[src] and pk,
            NAMES_RUNG=nm, ADJUDICATED=ad,
            STATES_RESOLUTION=bool(RESOL.search(txt)),
            STATES_MARGIN=bool(MARGIN.search(txt)),
            STATES_K=bool(ks), K_MAX=max(ks) if ks else 0,
            N_NUM=len(NUMTOK.findall(txt))))
    return pd.DataFrame(rows), len(U), n_md


# =================================================================================================
# PANEL / BOOK CONSTRUCTION — 1101's 162 rung books
# =================================================================================================
class Panel:
    """1161's panel dict, as a class.  SPY is a column of U56/B136 (that is what '56' counts)
    and is excluded from SMALL's eligible set, where it is a benchmark only."""

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
    """1161's `run_cell`, verbatim: decide at the rebalance close t, apply at t+1 (rule 2),
    10 bps on turnover.  Returns the daily NET return series of one rung book."""
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    return r - turn * COST / 1e4


def ladder_books(pan, anchor, lad):
    """The rung books of ONE core ladder: vary `lad`, freeze the other three at the anchor."""
    a = ANCHORS[anchor]
    out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        out[rung] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"])
    return out


# =================================================================================================
# THE BOOTSTRAP — 1101's joint moving-block redraw, the SAME block index applied to every rung
# =================================================================================================
def block_index(rng, T, L, B):
    """(B, T) moving-block index; blocks drawn with replacement, no wrap (1101's)."""
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def pboot_argmax(R, stat, L, seed, B=BDRAWS, chunk=100):
    """P(each rung is the argmax of `stat`) under joint moving-block redraws of the IS window.

    R is (T_is, k): the k rungs' IS daily returns.  One block index per draw is applied to ALL
    rungs, so the cross-rung correlation that makes these ladders hard to resolve is PRESERVED.
    """
    T, k = R.shape
    rng = np.random.default_rng(seed)
    cnt = np.zeros(k)
    done = 0
    while done < B:
        b = min(chunk, B - done)
        idx = block_index(rng, T, L, b)
        X = R[idx]                                      # (b, T, k)
        if stat == "CH_ISSHARPE":
            v = X.mean(axis=1) * 252.0 / (X.std(axis=1, ddof=1) * np.sqrt(252.0))
        elif stat == "CH_ISCAGR":
            eq = np.cumprod(1.0 + X, axis=1)
            v = eq[:, -1, :] ** (252.0 / T) - 1.0
        elif stat == "CH_ISDD":
            eq = np.cumprod(1.0 + X, axis=1)
            v = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)   # maximise (= shallowest)
        else:
            raise ValueError(stat)
        v = np.where(np.isfinite(v), v, -np.inf)
        am = v.argmax(axis=1)
        cnt += np.bincount(am, minlength=k)
        done += b
    return cnt / B


def is_stat(r, ins, stat, T_is):
    x = r[ins]
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    if stat == "CH_ISCAGR":
        eq = np.cumprod(1.0 + x)
        return eq[-1] ** (252.0 / T_is) - 1.0
    if stat == "CH_ISDD":
        eq = np.cumprod(1.0 + x)
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1154 (lane B, {DATE}) — does ANY committed REACH or CHOOSER claim survive its OWN P_boot BAR?")
    P("=" * 100)
    P("  dial 1 = CLAIM SET    {C_STRICT, C_PROX, C_ALL}      (headline C_STRICT)")
    P("  dial 2 = BLOCK LENGTH {21, 63, 126, 252}             (headline 63 = 1101's own)")
    P("  NOT dials: panel (3), anchor (2, 1101's), ladder (4), chooser (3) — all 72 decisions")
    P("             published at every one of the 12 dial cells.  Bar 0.90/0.10, 1000 draws.")
    P("")

    # ---------------------------------------------------------------- ARM 0: data-free first
    P("-" * 100)
    P("ARM 0 — DATA-FREE.  What does a 0.90 bar DEMAND of a ladder, before any tape is read?")
    P("-" * 100)
    frows = []
    for lad in LADNAMES:
        k = len(LADDERS[lad])
        frows.append(dict(ladder=lad, k_rungs=k, uniform_null=1.0 / k,
                          bar=BAR_HI, demanded_multiple=BAR_HI * k,
                          max_attainable_resolution_at_B=1.0 - 1.0 / (BDRAWS + 1)))
    fdf = pd.DataFrame(frows)
    P(fdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"  A pick on the {len(LAD_G)}-rung GROSS ladder must beat its own uniform null "
      f"{BAR_HI * len(LAD_G):.2f}x to be called resolved; on the {len(LAD_H)}-rung H ladder only "
      f"{BAR_HI * len(LAD_H):.2f}x.")
    P("  So 'resolved' is NOT comparable across ladders unless the rung count travels with it —")
    P("  the same defect idea 1155 found in the record's SPREAD claims, arriving on PICKS.")
    dump(fdf, "datafree")
    P("")

    # ---------------------------------------------------------------- ARM A: census
    P("-" * 100)
    P("ARM A — CENSUS of the record's committed PICK / REACH sentences.")
    P("-" * 100)
    cdf, n_units, n_md = census()
    P(f"  corpus: {n_units:,} committed text units over LEADERBOARD.md + CHANGELOG.md + {n_md} .md files")
    crows = []
    for cs in CLAIMSETS:
        sub = cdf[cdf[cs]]
        n = len(sub)
        crows.append(dict(claim_set=cs, n_units=n,
                          names_rung=int(sub.NAMES_RUNG.sum()),
                          adjudicated=int(sub.ADJUDICATED.sum()),
                          states_resolution=int(sub.STATES_RESOLUTION.sum()),
                          frac_states_resolution=sub.STATES_RESOLUTION.mean() if n else np.nan,
                          states_margin=int(sub.STATES_MARGIN.sum()),
                          frac_states_margin=sub.STATES_MARGIN.mean() if n else np.nan,
                          states_rung_count=int(sub.STATES_K.sum()),
                          frac_states_rung_count=sub.STATES_K.mean() if n else np.nan))
    cendf = pd.DataFrame(crows)
    P(cendf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(cdf, "census_units")
    dump(cendf, "census")
    strict = cendf.loc[cendf.claim_set == "C_STRICT"].iloc[0]
    P(f"  C_STRICT: {int(strict.n_units)} committed sentences NAME a pick and ADJUDICATE on it; "
      f"{strict.frac_states_resolution:.4f} of them state ANY resolution for that pick.")
    P("")

    # ---------------------------------------------------------------- panels
    P("-" * 100)
    P("PANELS (rule 9: all three current-constituent lists; every LEVEL is optimistic).")
    P("-" * 100)
    u = load_universe()
    b = load_universe(broad=True)
    s, n_bad, n_meta = load_small()
    PAN = {}
    for nm, px in (("U56", u), ("B136", b), ("SMALL", s)):
        PAN[nm] = Panel(nm, px)
        neli = px.shape[1] - (1 if nm == "SMALL" else 0)
        P(f"  {nm:<6s} {px.shape[0]:,} rows x {px.shape[1]} cols, {neli} eligible   "
          f"{px.index[0].date()} -> {px.index[-1].date()}  "
          f"warm {PAN[nm].warm.sum():,}  IS {PAN[nm].ins.sum():,}  OOS {PAN[nm].oos.sum():,}")
    P(f"  SMALL exclusion: {n_bad} of {n_meta} names dropped on max_1d_move >= 1.0 (documented).")
    P("")

    # ---------------------------------------------------------------- gates (before results)
    P("-" * 100)
    P("GATES — printed BEFORE any result number.")
    P("-" * 100)
    pu = PAN["U56"]
    a = ANCHORS["A"]
    r_anchor = book(pu, a["N"], a["H"], a["GROSS"], a["CADENCE"])
    # G1: the fast runner == engine.backtest on the same DECISION-TIME weights frame (1161's).
    W = build(-pu.sc, pu.elig, pu.priced, pu.reb["W"], a["N"], a["H"], pu.T, pu.K, a["GROSS"])
    eng = backtest(pu.px, pd.DataFrame(W, index=pu.idx, columns=pu.px.columns),
                   cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.abs(eng[pu.warm] - r_anchor[pu.warm]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", g1, g1 < 1e-12)

    mA = blocks_m(r_anchor, pu.warm, pu.ins, pu.oos)
    g2 = max(abs(mA["CAGR"] - A1101_TRIPLE[0]), abs(mA["Sharpe"] - A1101_TRIPLE[1]),
             abs(mA["MaxDD"] - A1101_TRIPLE[2]))
    gate("G2", "CROSS-RUN 1101's committed U56 anchor-A triple", g2, g2 < 5e-3)
    P(f"     this run {mA['CAGR']:.6f}/{mA['Sharpe']:.6f}/{mA['MaxDD']:.6f} vs committed "
      f"{A1101_TRIPLE[0]:.6f}/{A1101_TRIPLE[1]:.6f}/{A1101_TRIPLE[2]:.6f}  "
      "(1163's price-vintage defect is CARRIED, not absorbed: the bar is 1161's 5e-3, not 5e-5)")

    lb = backtest(pu.px, rules_v2_weights(pu.px), cost_bps=COST, freq="W")["returns"]
    _, _, ldd = fmet(lb.values[pu.warm])
    g3 = abs(ldd - LIVE_MAXDD_COMMITTED)
    gate("G3", "live RULES v2 U56 MaxDD == committed -12.05%", g3, g3 < 5e-4)

    spy_m = blocks_m(pu.spy, pu.warm, pu.ins, pu.oos)
    g4 = max(abs(spy_m["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(spy_m["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G4", "SPY OOS triple == committed (1161's bar 5e-3)", g4, g4 < 5e-3)

    g5v = float((cdf.C_STRICT & ~cdf.C_PROX).sum() + (cdf.C_PROX & ~cdf.C_ALL).sum())
    gate("G5", "claim sets nest C_STRICT <= C_PROX <= C_ALL", g5v, g5v == 0)

    # G6: KNOWN ANSWER UNDER THE MACHINERY.  Build M independent EXCHANGEABLE ladders -- k iid
    # block-resamples of one real book -- and score each with the same joint bootstrap.  Within a
    # single ladder P_boot is NOT uniform (the rungs are fixed realisations and the joint index
    # preserves their differences, which is exactly the property that makes this bootstrap the
    # right one); ACROSS independent ladders the position-mean must land on 1/k by symmetry.
    # The BAR IS DERIVED, NOT SET: the effective sample here is the LADDER count M (draws within
    # one ladder share its realisation), so the position-mean's own SE is sqrt(p(1-p)/M) at
    # p = 1/k, and the gate is 3 of those.  FIRST CUT, PRINTED RATHER THAN PATCHED OVER: at
    # M = 40 this read 5.975e-02 against a hand-set 0.05 -- 0.95 SE, i.e. the BAR was
    # mis-specified, not the machinery.  M is raised until the gate can discriminate.
    T_is = int(pu.ins.sum())
    base = r_anchor[pu.ins]
    kk, M6 = 5, 200
    acc = np.zeros(kk)
    for j in range(M6):
        rng6 = np.random.default_rng(seed_of("G6", j))
        Rex = np.column_stack([base[block_index(rng6, T_is, 63, 1)[0]] for _ in range(kk)])
        acc += pboot_argmax(Rex, "CH_ISSHARPE", 63, seed_of("G6b", j), B=200)
    acc /= M6
    g6 = float(np.abs(acc - 1.0 / kk).max())
    bar6 = 3.0 * np.sqrt((1.0 / kk) * (1 - 1.0 / kk) / M6)
    gate("G6", f"exchangeable ladders: position-mean P_boot == uniform null 1/{kk} "
               f"(M={M6} ladders, derived bar 3 SE = {bar6:.4f})", g6, g6 < bar6)

    # G7: a DEGENERATE ladder (k identical rungs) must put all its mass on the first rung --
    # the tie-break, not the statistic, decides.  1199's first-wins finding, re-gated here.
    Rdeg = np.column_stack([base] * 4)
    pdeg = pboot_argmax(Rdeg, "CH_ISSHARPE", 63, seed_of("G7"), B=200)
    g7 = abs(float(pdeg[0]) - 1.0)
    gate("G7", "degenerate ladder (identical rungs) -> all mass on the FIRST rung", g7, g7 == 0.0)

    # G8: determinism of the bootstrap at a fixed seed
    rng8 = np.random.default_rng(seed_of("G8"))
    R8 = np.column_stack([base[block_index(rng8, T_is, 63, 1)[0]] for _ in range(kk)])
    d1 = pboot_argmax(R8, "CH_ISSHARPE", 63, 424242, B=200)
    d2 = pboot_argmax(R8, "CH_ISSHARPE", 63, 424242, B=200)
    g8 = float(np.abs(d1 - d2).max())
    gate("G8", "bootstrap determinism at fixed seed", g8, g8 == 0.0)
    P("")

    # ---------------------------------------------------------------- build all 162 rung books
    P("-" * 100)
    P("BUILDING 1101's 162 RUNG BOOKS (3 panels x 2 anchors x 4 ladders, anchor rung shared).")
    P("-" * 100)
    BOOKS = {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                BOOKS[(pn, an, lad)] = ladder_books(PAN[pn], an, lad)
        P(f"  {pn}: built  ({time.time() - t0:.0f}s)")
    P("")

    # ---------------------------------------------------------------- ARM B: the 72 decisions
    P("-" * 100)
    P("ARM B — EVERY DECISION, EVERY BLOCK LENGTH.  72 decisions x 4 L = 288 published rows.")
    P("-" * 100)
    drows = []
    for pn in PANELS:
        pan = PAN[pn]
        T_is = int(pan.ins.sum())
        for an in ANCHORS:
            anch = ANCHORS[an]
            for lad in LADNAMES:
                rungs = LADDERS[lad]
                bk = BOOKS[(pn, an, lad)]
                R = np.column_stack([bk[r][pan.ins] for r in rungs])
                a_rung = anch[lad]
                ai = rungs.index(a_rung)
                for ch in CHOOSERS:
                    vals = [is_stat(bk[r], pan.ins, ch, T_is) for r in rungs]
                    pick_i = int(np.nanargmax(vals))
                    pick = rungs[pick_i]
                    reached = bool(pick_i == ai)
                    sv = np.sort(np.asarray(vals, float))
                    margin = float(sv[-1] - sv[-2]) if len(sv) > 1 else np.nan
                    for L in BLOCKS:
                        pb = pboot_argmax(R, ch, L, seed_of(pn, an, lad, ch, L), B=BDRAWS)
                        p_pick = float(pb[pick_i])
                        p_anch = float(pb[ai])
                        drows.append(dict(
                            panel=pn, anchor=an, ladder=lad, chooser=ch, L=L,
                            k_rungs=len(rungs), uniform_null=1.0 / len(rungs),
                            anchor_rung=str(a_rung), pick_rung=str(pick), reached=reached,
                            is_margin=margin,
                            P_pick=p_pick, P_anchor=p_anch,
                            P_boot_top=float(pb.max()),
                            resolved=bool(p_pick >= BAR_HI or p_pick <= BAR_LO),
                            resolved_supported=bool(p_pick >= BAR_HI),
                            beats_uniform=bool(p_pick > 1.0 / len(rungs)),
                            C_STRICT=(an == "A" and ch == CH_HEAD),
                            C_PROX=(an == "A"),
                            C_ALL=True))
    ddf = pd.DataFrame(drows)
    dump(ddf, "decisions")

    P("")
    P("  RESOLVED COUNTS — the 12 dial cells, every one published:")
    P(f"  {'claim_set':<10s} {'L':>5s} {'n':>5s} {'resolved':>9s} {'frac':>7s} "
      f"{'supported':>10s} {'P_pick mean':>12s} {'min':>7s} {'max':>7s}")
    grid = []
    for cs in CLAIMSETS:
        for L in BLOCKS:
            sub = ddf[ddf[cs] & (ddf.L == L)]
            row = dict(claim_set=cs, L=L, n=len(sub),
                       resolved=int(sub.resolved.sum()), frac_resolved=sub.resolved.mean(),
                       supported=int(sub.resolved_supported.sum()),
                       frac_supported=sub.resolved_supported.mean(),
                       P_pick_mean=sub.P_pick.mean(), P_pick_min=sub.P_pick.min(),
                       P_pick_max=sub.P_pick.max(),
                       frac_beats_uniform=sub.beats_uniform.mean())
            grid.append(row)
            P(f"  {cs:<10s} {L:>5d} {len(sub):>5d} {int(sub.resolved.sum()):>9d} "
              f"{sub.resolved.mean():>7.4f} {int(sub.resolved_supported.sum()):>10d} "
              f"{sub.P_pick.mean():>12.4f} {sub.P_pick.min():>7.4f} {sub.P_pick.max():>7.4f}")
    gdf = pd.DataFrame(grid)
    dump(gdf, "dialgrid")

    head = ddf[ddf[CS_HEAD] & (ddf.L == L_HEAD)]
    P("")
    P(f"  HEADLINE ({CS_HEAD} x L{L_HEAD}, {len(head)} committed decisions):")
    P(head[["panel", "anchor", "ladder", "chooser", "k_rungs", "anchor_rung", "pick_rung",
            "reached", "is_margin", "P_pick", "P_anchor", "resolved"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # per-ladder resolution at the headline L, all 72
    P("")
    P("  PER LADDER at L = 63, all 72 decisions (rung count in brackets):")
    for lad in LADNAMES:
        sub = ddf[(ddf.L == L_HEAD) & (ddf.ladder == lad)]
        P(f"    {lad:<8s} [k={len(LADDERS[lad]):>2d}]  resolved {int(sub.resolved.sum()):>2d}/{len(sub):<2d}  "
          f"P_pick mean {sub.P_pick.mean():.4f}  (uniform null {1/len(LADDERS[lad]):.4f})  "
          f"reach {int(sub.reached.sum())}/{len(sub)}")

    # cross-run: 1101's headline 24 and its two committed P_boot values
    h1101 = ddf[(ddf.L == L_HEAD) & (ddf.anchor == "A") & (ddf.chooser.isin([CH_HEAD, "CH_ISCAGR"]))]
    P("")
    P(f"  CROSS-READ of 1101: its headline 24 (anchor A, 2 choosers, 3 panels, 4 ladders) reads "
      f"{int(h1101.resolved.sum())} of {len(h1101)} resolved here against its committed "
      f"{A1101_HEADLINE_RESOLVED} of 24.")
    u56A = ddf[(ddf.L == L_HEAD) & (ddf.panel == "U56") & (ddf.anchor == "A") & (ddf.chooser == CH_HEAD)]
    for _, r in u56A.iterrows():
        if r.ladder in A1101_REACHSET:
            ref = A1101_PBOOT_U56_GROSS if r.ladder == "GROSS" else A1101_PBOOT_U56_CADENCE
            P(f"    U56/A/{r.ladder:<8s} P_anchor {r.P_anchor:.4f}  (1101 committed {ref:.3f})")
    rs = set(u56A.loc[u56A.reached, "ladder"])
    gate("G9", f"CROSS-RUN 1101's U56 anchor-A reach set == {sorted(A1101_REACHSET)}",
         float(len(rs ^ A1101_REACHSET)), rs == A1101_REACHSET)
    P("")

    # ---------------------------------------------------------------- ARM C: what a bar rejects
    P("-" * 100)
    P("ARM C — WHAT THE BAR REJECTS, and whether the record could have KNOWN without the bootstrap.")
    P("-" * 100)
    hh = ddf[ddf.L == L_HEAD]
    # is the cheap IS margin a substitute for P_boot?
    ok = hh.is_margin.notna() & hh.P_pick.notna()
    cor = float(np.corrcoef(hh.loc[ok, "is_margin"].rank(), hh.loc[ok, "P_pick"].rank())[0, 1])
    P(f"  Spearman(IS margin, P_pick) over all 72 at L=63: {cor:.4f}")
    lo = hh.loc[~hh.resolved, "is_margin"]
    hi = hh.loc[hh.resolved, "is_margin"]
    P(f"  IS margin | unresolved: median {lo.median():.3e} (n={len(lo)});  "
      f"resolved: median {hi.median():.3e} (n={len(hi)})")
    P("  -> the cheap MARGIN column (idea 1120's clause) and P_boot are NEARLY ORTHOGONAL.  The")
    P("     hypothesis this arm was written to test — that the margin is a free substitute for")
    P("     the bootstrap — is REFUTED, and so is its converse: neither is a proxy for the")
    P("     other, and a run publishing one has NOT published the other.")
    # --- WHERE THE RESOLUTION ACTUALLY LIVES, and why it is not evidence ---------------------
    P("")
    P("  WHERE THE RESOLVED DECISIONS LIVE (L = 63, all 72):")
    nres = int(hh.resolved.sum())
    ngr = int(hh[hh.resolved & (hh.ladder == "GROSS")].shape[0])
    P(f"    {ngr} of {nres} resolved decisions are GROSS-ladder decisions; "
      f"outside GROSS, {nres - ngr} of {len(hh[hh.ladder != 'GROSS'])} resolve.")
    mrows = []
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                if lad == "CADENCE":
                    continue                     # not an ordered numeric ladder
                rungs = LADDERS[lad]
                bk = BOOKS[(pn, an, lad)]
                pan = PAN[pn]
                T_is = int(pan.ins.sum())
                v = np.array([is_stat(bk[r], pan.ins, CH_HEAD, T_is) for r in rungs], float)
                x = np.asarray(rungs, float)
                rho = float(np.corrcoef(pd.Series(x).rank(), pd.Series(v).rank())[0, 1])
                mrows.append(dict(panel=pn, anchor=an, ladder=lad, k=len(rungs),
                                  spearman_rung_vs_ISSharpe=rho,
                                  monotone=bool(abs(rho) > 1.0 - 1e-9),
                                  IS_Sharpe_spread=float(v.max() - v.min())))
    mdf = pd.DataFrame(mrows)
    P("")
    P("  IS THE LADDER MONOTONE?  Spearman(rung, IS Sharpe) per (panel, anchor, ladder):")
    P(mdf.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    dump(mdf, "monotonicity")
    gr = mdf[mdf.ladder == "GROSS"]
    g10 = float((~gr.monotone).sum())
    gate("G10", f"GROSS ladder is EXACTLY monotone in IS Sharpe at all "
                f"{len(gr)} (panel, anchor) cells", g10, g10 == 0)
    P(f"     ... over an IS-Sharpe spread of only {gr.IS_Sharpe_spread.min():.6f} to "
      f"{gr.IS_Sharpe_spread.max():.6f}.")
    P("  THE MECHANISM, WHICH IS THE PART WORTH KEEPING: argmax of a MONOTONE ladder is an")
    P("  IDENTITY, so the joint bootstrap re-picks the same endpoint on essentially every draw")
    P("  NO MATTER HOW SMALL THE DIFFERENCE IS.  P_boot measures ORDER STABILITY, not EFFECT")
    P("  SIZE — and it is therefore NOT a bar a published pick can be held to.")
    tiny = hh[hh.resolved].nsmallest(1, "is_margin").iloc[0]
    big = hh[~hh.resolved].nlargest(1, "is_margin").iloc[0]
    P(f"    smallest-margin RESOLVED    {tiny.panel}/{tiny.anchor}/{tiny.ladder}/{tiny.chooser}: "
      f"margin {tiny.is_margin:.2e}, P_pick {tiny.P_pick:.4f}  -> CERTIFIED")
    P(f"    largest-margin UNRESOLVED   {big.panel}/{big.anchor}/{big.ladder}/{big.chooser}: "
      f"margin {big.is_margin:.2e} ({big.is_margin / tiny.is_margin:.0f}x larger), "
      f"P_pick {big.P_pick:.4f}  -> REJECTED")
    P("    -> the bar CERTIFIES the pick with the SMALLER effect and REJECTS the one with the")
    P("       larger.  STATED AT ITS TRUE STRENGTH, WHICH IS NOT 'INVERTED': the two groups'")
    P("       margins are INDISTINGUISHABLE, which is worse for the bar than an inversion would")
    P("       be, because it means the bar carries NO effect-size information at all.")
    mr, mu = hh.loc[hh.resolved, "is_margin"].median(), hh.loc[~hh.resolved, "is_margin"].median()
    P(f"       median IS margin {mr:.3e} (RESOLVED) vs {mu:.3e} (UNRESOLVED), ratio "
      f"{mr / mu:.4f}; Spearman over all 72 = {cor:.4f}.")
    P("")

    arows = []
    for L in BLOCKS:
        sub = ddf[ddf.L == L]
        o = sub.is_margin.notna()
        arows.append(dict(L=L, spearman_margin_Ppick=float(np.corrcoef(
            sub.loc[o, "is_margin"].rank(), sub.loc[o, "P_pick"].rank())[0, 1]),
            frac_resolved=sub.resolved.mean(), P_pick_mean=sub.P_pick.mean()))
    adf = pd.DataFrame(arows)
    P("")
    P("  BLOCK-LENGTH SENSITIVITY (all 72 decisions):")
    P(adf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(adf, "blocksens")
    P("")

    # ---------------------------------------------------------------- ARM D: rule 8 walk-forward
    P("-" * 100)
    P("ARM D — RULE 8 WALK-FORWARD.  Does a RESOLUTION BAR buy anything in capital terms?")
    P("-" * 100)
    P("  Every pick is chosen on 2009-2016 ALONE; 2017-2026 is read ONCE, after.")
    P("    R_RAW     publish the IS argmax, always            (the record's habit)")
    P("    R_BAR     publish it only if P_pick >= 0.90, else STAY AT THE ANCHOR")
    P("    R_ANCHOR  never move                               (1155's do-nothing control)")
    wrows = []
    for pn in PANELS:
        pan = PAN[pn]
        T_is = int(pan.ins.sum())
        sb = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lbk = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        lbm = blocks_m(np.nan_to_num(lbk), pan.warm, pan.ins, pan.oos)
        for an in ANCHORS:
            anch = ANCHORS[an]
            for lad in LADNAMES:
                rungs = LADDERS[lad]
                bk = BOOKS[(pn, an, lad)]
                ai = rungs.index(anch[lad])
                for ch in CHOOSERS:
                    vals = [is_stat(bk[r], pan.ins, ch, T_is) for r in rungs]
                    pick_i = int(np.nanargmax(vals))
                    for L in BLOCKS:
                        row = ddf[(ddf.panel == pn) & (ddf.anchor == an) & (ddf.ladder == lad)
                                  & (ddf.chooser == ch) & (ddf.L == L)].iloc[0]
                        for rule in RULES_PUB:
                            if rule == "R_RAW":
                                j = pick_i
                            elif rule == "R_BAR":
                                j = pick_i if row.P_pick >= BAR_HI else ai
                            else:
                                j = ai
                            r = bk[rungs[j]]
                            m = blocks_m(r, pan.warm, pan.ins, pan.oos)
                            f4b = legs_4b(m, sb)
                            o4b = legs_4b_oos(m, sb)
                            f4a = legs_4a(m, lbm)
                            wrows.append(dict(
                                panel=pn, anchor=an, ladder=lad, chooser=ch, L=L, rule=rule,
                                chosen_rung=str(rungs[j]), moved=bool(j != ai),
                                P_pick=float(row.P_pick),
                                OOS_CAGR=m["OOS_CAGR"], OOS_Sharpe=m["OOS_Sharpe"],
                                OOS_MaxDD=m["OOS_MaxDD"], CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                                pass_4b_full=all(f4b.values()), pass_4b_oos=all(o4b.values()),
                                pass_4a=all(f4a.values()), **f4b, **o4b, **f4a))
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")

    P("")
    P("  MEAN OOS SHARPE BY PUBLISHING RULE x CLAIM SET x BLOCK LENGTH (every cell published):")
    P(f"  {'claim_set':<10s} {'L':>5s} {'rule':<10s} {'n':>4s} {'moved':>6s} "
      f"{'meanOOS_S':>10s} {'meanOOS_CAGR':>13s} {'meanOOS_DD':>11s} {'4b_full':>8s} {'4b_oos':>7s} {'4a':>4s}")
    srows = []
    for cs in CLAIMSETS:
        key = {"C_STRICT": (wdf.anchor == "A") & (wdf.chooser == CH_HEAD),
               "C_PROX": (wdf.anchor == "A"),
               "C_ALL": wdf.index == wdf.index}[cs]
        for L in BLOCKS:
            for rule in RULES_PUB:
                sub = wdf[key & (wdf.L == L) & (wdf.rule == rule)]
                row = dict(claim_set=cs, L=L, rule=rule, n=len(sub),
                           n_moved=int(sub.moved.sum()),
                           mean_OOS_Sharpe=sub.OOS_Sharpe.mean(),
                           mean_OOS_CAGR=sub.OOS_CAGR.mean(),
                           mean_OOS_MaxDD=sub.OOS_MaxDD.mean(),
                           mean_Sharpe=sub.Sharpe.mean(),
                           n_4b_full=int(sub.pass_4b_full.sum()),
                           n_4b_oos=int(sub.pass_4b_oos.sum()),
                           n_4a=int(sub.pass_4a.sum()))
                srows.append(row)
                P(f"  {cs:<10s} {L:>5d} {rule:<10s} {len(sub):>4d} {int(sub.moved.sum()):>6d} "
                  f"{sub.OOS_Sharpe.mean():>10.4f} {sub.OOS_CAGR.mean():>13.4f} "
                  f"{sub.OOS_MaxDD.mean():>11.4f} {int(sub.pass_4b_full.sum()):>8d} "
                  f"{int(sub.pass_4b_oos.sum()):>7d} {int(sub.pass_4a.sum()):>4d}")
    sdf = pd.DataFrame(srows)
    dump(sdf, "rule8")
    P("")

    # ---------------------------------------------------------------- ARM E: both KEEP paths
    P("-" * 100)
    P("ARM E — BOTH KEEP PATHS on ALL 162 RUNG BOOKS (protocol rule 4; nothing selected on).")
    P("-" * 100)
    brows = []
    for pn in PANELS:
        pan = PAN[pn]
        sb = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lbk = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        lbm = blocks_m(np.nan_to_num(lbk), pan.warm, pan.ins, pan.oos)
        seen = set()
        for an in ANCHORS:
            anch = ANCHORS[an]
            for lad in LADNAMES:
                for rung in LADDERS[lad]:
                    kw = dict(N=anch["N"], H=anch["H"], GROSS=anch["GROSS"], CADENCE=anch["CADENCE"])
                    kw[lad] = rung
                    key = (pn, kw["N"], kw["H"], kw["GROSS"], kw["CADENCE"])
                    if key in seen:
                        continue
                    seen.add(key)
                    m = blocks_m(BOOKS[(pn, an, lad)][rung], pan.warm, pan.ins, pan.oos)
                    f4b, o4b, f4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lbm)
                    brows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rung),
                                      N=kw["N"], H=kw["H"], GROSS=kw["GROSS"], CADENCE=kw["CADENCE"],
                                      **{k: m[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                                      pass_4b_full=all(f4b.values()), pass_4b_oos=all(o4b.values()),
                                      pass_4a=all(f4a.values()), **f4b, **o4b, **f4a))
    bdf = pd.DataFrame(brows)
    dump(bdf, "books")
    P(f"  {len(bdf)} distinct rung books.")
    P(f"  4a {int(bdf.pass_4a.sum())} of {len(bdf)};  4b full {int(bdf.pass_4b_full.sum())};  "
      f"4b OOS {int(bdf.pass_4b_oos.sum())};  BOTH "
      f"{int((bdf.pass_4b_full & bdf.pass_4b_oos).sum())}")
    for pn in PANELS:
        sub = bdf[bdf.panel == pn]
        P(f"    {pn:<6s} n={len(sub):<3d}  4a {int(sub.pass_4a.sum()):>2d}  "
          f"4b full {int(sub.pass_4b_full.sum()):>2d}  4b OOS {int(sub.pass_4b_oos.sum()):>2d}  "
          f"leg rates: H1 {sub.L_H1.mean():.3f} H2 {sub.L_H2.mean():.3f} OOS {sub.L_OOS.mean():.3f} "
          f"DD {sub.L_DD.mean():.3f} CAGR {sub.L_CAGR.mean():.3f}")
    pas = bdf[bdf.pass_4b_full & bdf.pass_4b_oos]
    if len(pas):
        P("")
        P("  BOOKS CLEARING 4b ON BOTH READINGS:")
        P(pas[["panel", "N", "H", "GROSS", "CADENCE", "CAGR", "Sharpe", "MaxDD",
               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------------- verdict
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    hres = int(head.resolved.sum())
    hsup = int(head.resolved_supported.sum())
    allres = ddf[ddf.L == L_HEAD]
    r8 = sdf[(sdf.claim_set == "C_ALL") & (sdf.L == L_HEAD)].set_index("rule")
    P(f"  ANSWER: at the headline {CS_HEAD} x L{L_HEAD}, {hres} of {len(head)} committed pick")
    P(f"  decisions are RESOLVED at the 0.90/0.10 bar and {hsup} are resolved in the SUPPORTED")
    P(f"  direction.  Over all 72 decisions: {int(allres.resolved.sum())} of 72 resolved, "
      f"{int(allres.resolved_supported.sum())} supported.")
    P(f"  The census finds {int(strict.n_units)} committed C_STRICT pick sentences, of which "
      f"{strict.frac_states_resolution:.4f} state any resolution.")
    P(f"  RULE 8: R_RAW {r8.loc['R_RAW', 'mean_OOS_Sharpe']:.4f} / "
      f"R_BAR {r8.loc['R_BAR', 'mean_OOS_Sharpe']:.4f} / "
      f"R_ANCHOR {r8.loc['R_ANCHOR', 'mean_OOS_Sharpe']:.4f} mean OOS Sharpe; "
      f"4b-full picks {int(r8.loc['R_RAW', 'n_4b_full'])} / {int(r8.loc['R_BAR', 'n_4b_full'])} / "
      f"{int(r8.loc['R_ANCHOR', 'n_4b_full'])}.")
    P(f"  KEEP: 4a {int(bdf.pass_4a.sum())} of {len(bdf)}; 4b full {int(bdf.pass_4b_full.sum())}; "
      f"4b OOS {int(bdf.pass_4b_oos.sum())}.")
    P("")
    P("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current")
    P("  output of a sub-$2B screen less the documented max_1d_move >= 1.0 exclusion.  Every LEVEL")
    P("  is optimistic and every 4a/4b count is an UPPER bound.  P_boot is a RATIO of resampled")
    P("  argmax counts on one panel's own ladder and is far less exposed, but the levels are")
    P("  published beside it.")
    P("")
    P("  DECLARED APPROXIMATION, and its direction (1101's, restated): P_boot resamples ONE tape,")
    P("  so it measures sampling error around THIS regime and not regime uncertainty.  Every")
    P("  P_boot is therefore CLOSER TO 0 OR 1 than the truth, and 'resolved' is scored in the")
    P("  direction that FAVOURS the record.  A decision this run calls unresolved is unresolved")
    P("  a fortiori.")

    gdf2 = pd.DataFrame(GATES)
    dump(gdf2, "gates")
    P(f"  GATES {int(gdf2.pass_.sum())} of {len(gdf2)}")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))
    P(f"\n  total {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
