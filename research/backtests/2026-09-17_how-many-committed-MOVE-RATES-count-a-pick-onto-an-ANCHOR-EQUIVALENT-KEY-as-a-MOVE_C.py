#!/usr/bin/env python3
"""
Idea 1230 (lane C, 2026-09-17) — how many committed MOVE RATES count a pick onto an
ANCHOR-EQUIVALENT KEY as a MOVE?

THE PREMISE, READ FROM THE RECORD.  Idea 1227 (lane C, same day) gated that in the record's
standing four-ladder grid the keys ("N", 20), ("H", 126), ("GROSS", 0.75) and ("CADENCE", "W")
are ONE book bit for bit — max |Delta| over the whole tape is exactly 0.0 on all three panels.
A chooser that "moves" onto one of those keys has not moved, and a null that draws one as a
destination has drawn a NO-OP.  1227 measured the damage on its own grid: 0.0280 of all
pick-cells are key-moves that are value-holds, and 1223's null destination pool held 4 no-ops
in 22 books.  1223 published its move rates on the KEY definition and so does, as far as anyone
has checked, the rest of the record.

THIS RUN CENSUSES THE ERROR AND RE-PRICES WHAT TURNS ON IT.

  ARM A  Harvest every committed MOVE RATE in the record, attribute each to its emitting
         script, and decide from that script whether the figure counts an anchor-equivalent
         key as a move.  Three answers per unit: CLEAN (value-aware), EXPOSED (key-based on a
         grid whose anchor is degenerate), UNRECOVERABLE.  NOT_MOVE_RATE candidates are
         published separately and folded into neither pass nor fail.
  ARM B  Rebuild 1223/1227's grid and re-price it: move rate, null destination pool, null
         p-value and publish decision under each equivalence test.  The BOOKS do not change,
         so every Sharpe and every delta is identical by construction (gate G12) — what moves
         is the move rate, the null, and therefore the publish decision.
  ARM C  Rule 8 and both KEEP paths, including the price of the publish rule itself: deploy a
         chooser when its IS gain clears its own matched null under a CONTAMINATED pool vs
         under a CLEAN one, and read 2017-2026 once.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM CLASS      {C_HEAD, C_MEMO, C_ALL, C_SCRIPT}
                   C_HEAD    LEADERBOARD.md + CHANGELOG.md  (the record's result sentences)
                   C_MEMO    C_HEAD + every backtests/*.result.md memo
                   C_ALL     C_MEMO + QUEUE.md + every backtests/*.console.txt
                   C_SCRIPT  the move-rate COMPUTATIONS in backtests/*.py, at source level
  EQUIVALENCE TEST {E_KEY, E_EXACT, E_FP12, E_RET8, E_DEC6, E_DEC3}
                   E_KEY     a move is any pick whose KEY differs from the anchor's — the
                             record's own implicit test, and the thing under audit
                   E_EXACT   equal iff max |Delta r| == 0.0 over the tape (1227's test)
                   E_FP12    max |Delta r| <= 1e-12          E_RET8  max |Delta r| <= 1e-8
                   E_DEC6    every fold Sharpe equal to 1e-6 (decision-identical, not
                             path-identical)                 E_DEC3  the same to 5e-4

  24 cells, EVERY ONE PUBLISHED.

NOT DIALS, REPORTED AT EVERY VALUE AND NEVER SELECTED ON: PANEL {U56, B136, SMALL} (rule 9);
COMPARISON SET {ALL4, NG}; IS WINDOW {252, 504, 756, 1260, 2520, EXPANDING}; FOLD CADENCE
{QUARTER, YEAR}.  The verdict is read off ALL4 / QUARTER, 1227's primary.

Frozen at the record's construction, inherited from 1207/1214/1223/1227 unchanged: 3-leg
composite (21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 /
GROSS=0.75 / CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 (lag=1), warm-up 260 rows,
the conditional two-sided band B_IID95 and its Monte-Carlo construction (seed 12141214), the
two matched nulls NL_COUNT / NL_PERM at 2,000 reps.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with the publish rule chosen on the
IS folds ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on
every rung book, every stitched chooser curve and every rule-8 pick; rule 9 survivorship
stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_how-many-committed-MOVE-RATES-count-a-pick-onto-an-ANCHOR-EQUIVALENT-KEY-as-a-MOVE_C.py
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

DATE = "2026-09-17"
SLUG = "how-many-committed-MOVE-RATES-count-a-pick-onto-an-ANCHOR-EQUIVALENT-KEY-as-a-MOVE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
BT = ROOT / "research" / "backtests"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
ANCHOR_KEY = ("CADENCE", "W")

LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
LADK = {"N": 6, "H": 4, "GROSS": 10, "CADENCE": 2}

HFORMS = ["H_RUNNERUP", "H_NARROWEST", "H_ANY"]
CHOOSERS = HFORMS + ["CH_RAW", "CH_ANCHOR"]
WINDOWS = [252, 504, 756, 1260, 2520, None]


def wname(L):
    return "EXPAND" if L is None else f"L{L}"


NG4 = ["N", "H", "CADENCE"]
ALL4 = ["N", "H", "GROSS", "CADENCE"]
SETS = {"ALL4": ALL4, "NG": NG4}
CADENCES = ["QUARTER", "YEAR"]
MIN_IS, MIN_FOLD = 252, 40

NMC, MC_SEED = 1_500_000, 12141214
NULL_REPS, NULL_SEED = 2000, 12301230
LIVE_MAXDD_COMMITTED = -0.1205

# ---- DIAL 2: the equivalence tests.  (kind, tolerance); E_KEY is the record's implicit one.
ETESTS = [("E_KEY", None), ("E_EXACT", 0.0), ("E_FP12", 1e-12), ("E_RET8", 1e-8),
          ("E_DEC6", 1e-6), ("E_DEC3", 5e-4)]
EPATH = {"E_EXACT", "E_FP12", "E_RET8"}      # tested on the return PATH
EDEC = {"E_DEC6", "E_DEC3"}                  # tested on the DECISION statistic (fold Sharpe)

D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}
KMAXD2 = 12

# 1223's committed numbers at (YEAR folds, EXPANDING window) — replication gate.
REP1223 = {("ALL4", "CH_ANCHOR"): (0.000, 1.0362), ("ALL4", "H_RUNNERUP"): (0.048, 1.0179),
           ("ALL4", "H_NARROWEST"): (0.881, 0.9875), ("ALL4", "H_ANY"): (0.881, 0.9875),
           ("ALL4", "CH_RAW"): (1.000, 0.9677), ("NG", "H_NARROWEST"): (0.024, 1.0368),
           ("NG", "H_ANY"): (0.095, 1.0394), ("NG", "H_RUNNERUP"): (0.048, 1.0179)}
REP1227_OVERSTATEMENT = 0.0280   # 1227's committed key-minus-value pick-cell gap, all cells

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def d2(k):
    return D2[min(max(int(k), 2), KMAXD2)]


# ============================================================== ARM A: the census machinery
# A committed MOVE RATE is a figure stating how often a chooser / rule / argmax LEAVES its
# incumbent.  The harvest is deliberately wide and then split; nothing is silently dropped.
MOVEPHR = re.compile(r"(move[_ -]?rate|movement rate|moves? (?:at|on|in|onto)\b|"
                     r"moved (?:at|on|onto)\b|move[sd]? off\b|rate of movement)", re.I)
CHOOSERCTX = re.compile(r"chooser|pick|argmax|rung|ladder|anchor|tune|tuned|hold|holding|"
                        r"dial|incumbent|do[- ]nothing|CH_|H_RUNNERUP|H_NARROWEST|H_ANY|"
                        r"destination|fold", re.I)
NUMTOK = re.compile(r"(?<![\w.])(\d+\s+of\s+\d+|\d*\.\d+|\d+(?:\.\d+)?%|\d+)(?![\w])")
# text that itself names the equivalence basis
STATES_BASIS = re.compile(r"anchor[- ]equivalent|bit[ -]for[ -]bit|by value|value definition|"
                          r"key definition|no[- ]op|value-based|key-based|is the anchor", re.I)
SCRIPTCOL = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2}_[^|\s]+?)(?:\.py)?\s*\|?\s*$")
PYNAME = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[A-Za-z0-9_\-]+")

# script-level signatures
SIG_VALUE = re.compile(r"ANCHOR_EQ|anchor_eq|anchor[- ]equivalent", re.I)
SIG_KEY = re.compile(r"!=\s*ANCHOR_I\b|!=\s*ANCHOR_KEY\b|!=\s*anchor_i\b|"
                     r"moved\s*=\s*bool\(\s*\w+\s*!=|moved_key", re.I)
# a source file COMPUTES a move rate only if it assigns one, not if its prose mentions moving
SIG_MOVECALC = re.compile(r"move_rate|\bmoved\s*=|\bmoves\s*=|moved_key|\bmoved\[", re.I)
IDEANUM = re.compile(r"\bidea\s+(\d{2,4})\b", re.I)
LANETAG = re.compile(r"\blane\s+([ABCD])\b|\bcloud\b", re.I)


def anchor_degenerate_source(txt):
    """True when the script builds a ladder grid in which the anchor book appears under two or
    more keys — i.e. the grid where a key-based move rate is actually wrong."""
    if not re.search(r"A_N\s*,\s*A_H\s*,\s*A_G", txt) and "ANCHOR_KEY" not in txt:
        return False
    hits = 0
    for pat in (r"\"N\"\s*:\s*\[[^\]]*\b20\b", r"'N'\s*:\s*\[[^\]]*\b20\b",
                r"\"H\"\s*:\s*\[[^\]]*\b126\b", r"'H'\s*:\s*\[[^\]]*\b126\b",
                r"\"GROSS\"\s*:\s*\[[^\]]*0\.75", r"'GROSS'\s*:\s*\[[^\]]*0\.75",
                r"\"CADENCE\"\s*:\s*\[[^\]]*\"W\"", r"'CADENCE'\s*:\s*\[[^\]]*'W'"):
        if re.search(pat, txt):
            hits += 1
    return hits >= 2


def harvest(path, label):
    """Every candidate move-rate unit in one committed file.  `cue` carries everything the
    attribution step may use: the line itself plus, for CHANGELOG, its enclosing '## ' header
    (the record writes one entry per idea under such a header)."""
    out = []
    try:
        lines = Path(path).read_text(errors="ignore").split("\n")
    except OSError:
        return out
    header = ""
    for i, ln in enumerate(lines):
        if ln.startswith("## "):
            header = ln
        if not MOVEPHR.search(ln):
            continue
        for m in MOVEPHR.finditer(ln):
            lo, hi = max(0, m.start() - 160), min(len(ln), m.end() + 160)
            span = ln[lo:hi]
            nums = NUMTOK.findall(span)
            out.append(dict(source=label, file=Path(path).name, line=i + 1,
                            phrase=m.group(0).lower(), span=span.strip(),
                            has_number=bool(nums), number=nums[0] if nums else "",
                            is_moverate=bool(nums) and bool(CHOOSERCTX.search(span)),
                            states_basis=bool(STATES_BASIS.search(span)),
                            cue=ln + " || " + header,
                            raw_line=ln.strip()[:400]))
    return out


# ============================================================== panels / runner (1207/1214/1227)
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
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


# ============================================================== the null band machinery (1214)
_RDRAW: dict[int, np.ndarray] = {}


def rdraw(k, n=NMC):
    k = int(k)
    if k in _RDRAW:
        return _RDRAW[k]
    rng = np.random.default_rng(MC_SEED + 1000 * k)
    out = np.empty(n, dtype=np.float64)
    step = 250_000
    for i in range(0, n, step):
        m = min(step, n - i)
        x = rng.standard_normal((m, k))
        out[i:i + m] = x.max(1) - x.min(1)
    _RDRAW[k] = out
    return out


_BAND: dict[tuple, dict] = {}


def nullband(kw, kn):
    key = (int(kw), int(kn))
    if key in _BAND:
        return _BAND[key]
    a, b = rdraw(kw), rdraw(kn)
    b = np.roll(b, 7919)
    m = a >= b
    va = (a[m] / d2(kw)) / (b[m] / d2(kn))
    out = dict(k_w=int(kw), k_n=int(kn), median=float(np.median(va)),
               L95=float(np.quantile(va, 0.025)), U95=float(np.quantile(va, 0.975)))
    _BAND[key] = out
    return out


_MEDR: dict[int, float] = {}


def medrange(k):
    k = int(k)
    if k not in _MEDR:
        _MEDR[k] = float(np.median(rdraw(k)))
    return _MEDR[k]


def call_iid95(M, I, band):
    V = (M / I) if I > 0 else np.inf
    return "W" if V > band["U95"] else ("N" if V < band["L95"] else "TIE")


# ==================================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1230 (lane C, 2026-09-17) — how many committed MOVE RATES count a pick onto an")
    say("ANCHOR-EQUIVALENT KEY as a MOVE?")
    say("=" * 108)
    say("")
    say("  DIAL 1 CLAIM CLASS       C_HEAD / C_MEMO / C_ALL / C_SCRIPT")
    say("  DIAL 2 EQUIVALENCE TEST  " + " / ".join(e for e, _ in ETESTS))
    say("  24 cells, every one published.  Panel, comparison set, IS window and fold cadence")
    say("  are NOT dials: reported at every value, never selected on.")
    say("")
    say("  PRE-DECLARED OUTCOMES, fixed before any file or price is read:")
    say("    (A) THE RECORD IS CLEAN — no committed move rate is key-based on a degenerate grid.")
    say("    (B) THE RECORD IS EXPOSED — some committed move rates are key-based, and the")
    say("        re-pricing changes at least one publish decision.")
    say("    (C) EXPOSED BUT INERT — key-based figures exist, no publish decision moves.")

    # ---------------------------------------------------------------- ARM A: the census
    say("")
    say("=" * 108)
    say("ARM A — THE CENSUS.  EVERY COMMITTED MOVE RATE IN THE RECORD, AND WHAT DEFINED IT")
    say("=" * 108)

    units = []
    units += harvest(ROOT / "research" / "LEADERBOARD.md", "LEADERBOARD")
    units += harvest(ROOT / "research" / "CHANGELOG.md", "CHANGELOG")
    units += harvest(ROOT / "research" / "QUEUE.md", "QUEUE")
    memos = sorted(BT.glob("*.result.md"))
    consoles = sorted(BT.glob("*.console.txt"))
    scripts = sorted(BT.glob("*.py"))
    for p in memos:
        units += harvest(p, "MEMO")
    for p in consoles:
        units += harvest(p, "CONSOLE")

    # --- script-level facts, computed once per source file
    SRC, IDEA2 = {}, {}
    for p in scripts:
        txt = p.read_text(errors="ignore")
        SRC[p.stem] = dict(
            value_aware=bool(SIG_VALUE.search(txt)),
            key_based=bool(SIG_KEY.search(txt)),
            computes_move=bool(SIG_MOVECALC.search(txt)),
            degenerate=anchor_degenerate_source(txt))
        # the record writes "Idea NNNN (lane X, DATE) — ..." as the script's first docstring line
        head = "\n".join(txt.split("\n")[:60])
        for n in IDEANUM.findall(head):
            IDEA2.setdefault(n, []).append(p.stem)

    def lane_of(s):
        for tag in ("_A", "_B", "_C", "_D", "_cloud"):
            if s.endswith(tag):
                return tag.lstrip("_")
        return ""

    def attribute(u):
        """Map a committed text unit to the .py that emitted it.  Three routes, in order of
        strength: (1) the unit IS a script artefact (memo / console share its stem); (2) the
        committed line names a script file (PROTOCOL rule 5 puts it in the leaderboard's last
        column); (3) the line names an idea number, resolved through the scripts' own docstring
        headers and, when several lanes ran that idea, through the lane tag on the same line."""
        stem = Path(u["file"]).name
        for suf in (".result.md", ".console.txt"):
            if stem.endswith(suf):
                return [stem[: -len(suf)]], "ARTEFACT"
        cue = u["cue"]
        cands = PYNAME.findall(cue)
        for c in reversed(cands):
            if c in SRC:
                return [c], "NAMED"
            hit = [s for s in SRC if s.startswith(c)]
            if hit:
                return sorted(hit), "NAMED"
        nums = IDEANUM.findall(cue)
        m = re.match(r"\|\s*[0-9]{4}-[0-9]{2}-[0-9]{2}\s*\|\s*(\d{2,4})\b", cue)
        if m:
            nums = [m.group(1)] + nums
        for n in nums:
            hit = IDEA2.get(n, [])
            if not hit:
                continue
            lt = LANETAG.search(cue)
            if lt and len(hit) > 1:
                want = (lt.group(1) or "cloud")
                nar = [s for s in hit if lane_of(s) == want]
                if nar:
                    hit = nar
            return sorted(hit), "IDEA"
        return [], ""

    for u in units:
        ss, route = attribute(u)
        fs = [SRC[s] for s in ss if s in SRC]
        u["script"] = ";".join(ss)
        u["route"] = route
        u["script_found"] = bool(fs)
        u["script_value_aware"] = bool(fs) and all(f["value_aware"] for f in fs)
        u["script_key_based"] = bool(fs) and all(f["key_based"] for f in fs)
        u["script_degenerate"] = bool(fs) and all(f["degenerate"] for f in fs)
        ambiguous = len(fs) > 1 and len({(f["value_aware"], f["key_based"], f["degenerate"])
                                         for f in fs}) > 1
        u["ambiguous"] = bool(ambiguous)
        if not u["is_moverate"]:
            u["verdict"] = "NOT_MOVE_RATE"
        elif u["states_basis"] or u["script_value_aware"]:
            u["verdict"] = "CLEAN"
        elif not fs or ambiguous:
            u["verdict"] = "UNRECOVERABLE"
        elif u["script_key_based"] and u["script_degenerate"]:
            u["verdict"] = "EXPOSED"
        elif u["script_degenerate"]:
            u["verdict"] = "EXPOSED_IMPLICIT"
        else:
            u["verdict"] = "NOT_DEGENERATE"

    # C_SCRIPT is a source-level population, not a text one.
    srows = []
    for stem, f in SRC.items():
        if not f["computes_move"]:
            continue
        v = ("CLEAN" if f["value_aware"] else
             ("EXPOSED" if (f["key_based"] and f["degenerate"]) else
              ("EXPOSED_IMPLICIT" if f["degenerate"] else "NOT_DEGENERATE")))
        srows.append(dict(source="SCRIPT", file=stem + ".py", line=0, phrase="source",
                          span="", has_number=True, number="", is_moverate=True,
                          states_basis=False, cue="", raw_line="", script=stem,
                          route="SOURCE", script_found=True, ambiguous=False,
                          script_value_aware=f["value_aware"], script_key_based=f["key_based"],
                          script_degenerate=f["degenerate"], verdict=v))
    cdf = pd.DataFrame(units)
    sdf_src = pd.DataFrame(srows)
    pd.concat([cdf, sdf_src], ignore_index=True).drop(columns=["cue"]).to_csv(
        f"{OUT}.census.csv", index=False)

    CLASSES = {"C_HEAD": cdf[cdf.source.isin(["LEADERBOARD", "CHANGELOG"])],
               "C_MEMO": cdf[cdf.source.isin(["LEADERBOARD", "CHANGELOG", "MEMO"])],
               "C_ALL": cdf,
               "C_SCRIPT": sdf_src}
    say("")
    say(f"  Sources scanned: LEADERBOARD.md, CHANGELOG.md, QUEUE.md, {len(memos)} memos, "
        f"{len(consoles)} console logs, {len(scripts)} scripts.")
    say(f"  {len(cdf)} candidate text units carry a move phrase; "
        f"{int(cdf.is_moverate.sum())} are MOVE RATES by the pre-declared test (a number AND a "
        f"chooser context),")
    say(f"  {int((~cdf.is_moverate).sum())} are NOT_MOVE_RATE and are published separately, "
        f"folded into neither pass nor fail.")
    say("")
    say("  (A1) DIAL 1, EVERY CLAIM CLASS.  'EXPOSED' = the emitting script defines a move by")
    say("       KEY on a grid whose anchor book appears under two or more keys.")
    say("       class      units  CLEAN  EXPOSED  EXP_IMPL  NOT_DEGEN  UNRECOV  states_basis")
    crows = []
    for cn, sub in CLASSES.items():
        mr = sub[sub.is_moverate] if len(sub) else sub
        cnt = {k: int((mr.verdict == k).sum()) for k in
               ("CLEAN", "EXPOSED", "EXPOSED_IMPLICIT", "NOT_DEGENERATE", "UNRECOVERABLE")}
        sb = int(mr.states_basis.sum()) if len(mr) else 0
        crows.append(dict(claim_class=cn, units=len(mr), **cnt, states_basis=sb,
                          exposed_rate=(cnt["EXPOSED"] + cnt["EXPOSED_IMPLICIT"]) / max(len(mr), 1),
                          states_basis_rate=sb / max(len(mr), 1)))
        say(f"       {cn:9s}  {len(mr):5d}  {cnt['CLEAN']:5d}  {cnt['EXPOSED']:7d}  "
            f"{cnt['EXPOSED_IMPLICIT']:8d}  {cnt['NOT_DEGENERATE']:9d}  "
            f"{cnt['UNRECOVERABLE']:7d}  {sb:12d}")
    pd.DataFrame(crows).to_csv(f"{OUT}.claims.csv", index=False)
    head = crows[0]
    GATES.append(dict(gate="G13 the census population is non-empty at every claim class",
                      value=float(min(r["units"] for r in crows)), target=1.0,
                      pass_=bool(min(r["units"] for r in crows) >= 1)))

    say("")
    say("  (A2) WHERE THE COMMITTED MOVE RATES LIVE (text classes, MOVE RATE units only):")
    for src in ["LEADERBOARD", "CHANGELOG", "QUEUE", "MEMO", "CONSOLE"]:
        s = cdf[(cdf.source == src) & cdf.is_moverate]
        if not len(s):
            say(f"       {src:12s}     0")
            continue
        say(f"       {src:12s} {len(s):5d}   CLEAN {int((s.verdict=='CLEAN').sum()):4d}   "
            f"EXPOSED {int(s.verdict.isin(['EXPOSED','EXPOSED_IMPLICIT']).sum()):4d}   "
            f"UNRECOV {int((s.verdict=='UNRECOVERABLE').sum()):4d}   "
            f"attributed to a script {int(s.script_found.sum()):4d}")

    # ---------------------------------------------------------------- books
    say("")
    say("=" * 108)
    say("ARM B — THE RE-PRICING.  THE SAME BOOKS, SIX EQUIVALENCE TESTS")
    say("=" * 108)
    mc_err = max(abs(rdraw(k).mean() - D2[k]) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants", value=mc_err,
                      target=5e-3, pass_=bool(mc_err < 5e-3)))
    unb = max(abs(rdraw(k).mean() / d2(k) - 1.0) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G1 R_k/d2(k) unbiased for sigma under the iid null", value=unb,
                      target=5e-3, pass_=bool(unb < 5e-3)))

    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mvv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mvv[c] < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0), SPY benchmark only.")

    booked, bench, BOOKKEY = {}, {}, []
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
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)

    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g2 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    GATES.append(dict(gate="G2 fast runner == engine.backtest on the decision-time frame",
                      value=g2, target=1e-10, pass_=bool(g2 < 1e-10)))
    lm = mdd(bench["U56"]["live"][WARMUP:])
    GATES.append(dict(gate="G3 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                      value=lm, target=LIVE_MAXDD_COMMITTED,
                      pass_=bool(abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)))

    RM = {p: np.column_stack([booked[p][k] for k in BOOKKEY]) for p in booked}
    BIDX = {k: i for i, k in enumerate(BOOKKEY)}
    LADIDX = {lad: [BIDX[(lad, r)] for r in LAD[lad]] for lad in LAD}
    ANCHOR_I = BIDX[ANCHOR_KEY]
    NB = len(BOOKKEY)

    # ---- folds (needed before E_DEC* can be evaluated: they are decision-statistic tests)
    folds = {}
    for cad in CADENCES:
        for pan in panels:
            keyv = (pan.idx.year.values * 10 + pan.idx.quarter.values) if cad == "QUARTER" \
                else pan.idx.year.values
            out, cover = [], []
            for v in sorted(set(keyv.tolist())):
                oo = np.flatnonzero(keyv == v)
                oo = oo[oo >= pan.i0 + MIN_IS]
                if len(oo) < MIN_FOLD:
                    continue
                o0, o1 = int(oo[0]), int(oo[-1]) + 1
                if o0 - pan.i0 < MIN_IS:
                    continue
                out.append((v, o0, o1))
                cover.append((o0, o1))
            cover = sorted(set(cover))
            gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
            GATES.append(dict(gate=f"G4 {cad} folds tile {pan.name} with no overlap and no gap",
                              value=float(gap), target=0.0, pass_=bool(gap == 0)))
            folds[(cad, pan.name)] = out

    FS, FSUM, FSQ, FN, FOL = {}, {}, {}, {}, {}
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            M = RM[pan.name]
            S = np.empty((len(fl), M.shape[1]))
            SU = np.empty_like(S)
            SQ = np.empty_like(S)
            NN = np.empty(len(fl))
            for i, (v, o0, o1) in enumerate(fl):
                sl = M[o0:o1]
                SU[i] = sl.sum(0)
                SQ[i] = (sl * sl).sum(0)
                NN[i] = o1 - o0
                mu = SU[i] / NN[i]
                sd = np.sqrt(np.maximum(SQ[i] / NN[i] - mu * mu, 0.0))
                S[i] = np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)
            FS[(cad, pan.name)] = S
            FSUM[(cad, pan.name)] = SU
            FSQ[(cad, pan.name)] = SQ
            FN[(cad, pan.name)] = NN
            FOL[(cad, pan.name)] = fl

    # ---- DIAL 2: the anchor-equivalent class under each test
    say("")
    say("  (B1) THE ANCHOR-EQUIVALENT CLASS, DIAL 2.  22 keys over 4 ladders; the anchor is")
    say("       ('CADENCE','W').  A pick landing inside the class is NOT a move, and a null")
    say("       drawing from inside it has drawn a NO-OP.")
    pathmax = np.zeros(NB)
    for i in range(NB):
        pathmax[i] = max(float(np.nanmax(np.abs(RM[p][:, i] - RM[p][:, ANCHOR_I]))) for p in RM)
    decmax = np.zeros(NB)
    for i in range(NB):
        decmax[i] = max(float(np.nanmax(np.abs(FS[(cad, p.name)][:, i]
                                               - FS[(cad, p.name)][:, ANCHOR_I])))
                        for cad in CADENCES for p in panels)

    AEQ = {}
    for ename, tol in ETESTS:
        if ename == "E_KEY":
            s = {ANCHOR_I}
        elif ename in EPATH:
            s = {i for i in range(NB) if pathmax[i] <= tol}
        else:
            s = {i for i in range(NB) if decmax[i] <= tol}
        AEQ[ename] = np.array(sorted(s))
    say("")
    say("       test     |class|  members")
    erows = []
    for ename, tol in ETESTS:
        mem = sorted(BOOKKEY[i] for i in AEQ[ename])
        erows.append(dict(etest=ename, tol=(np.nan if tol is None else tol), size=len(mem),
                          members="; ".join(f"{a}={b}" for a, b in mem)))
        say(f"       {ename:8s} {len(mem):6d}  " + ", ".join(f"{a}={b}" for a, b in mem))
    pd.DataFrame(erows).to_csv(f"{OUT}.equiv.csv", index=False)
    say("")
    say(f"       max |Delta r| to the anchor, non-equivalent books: "
        f"{np.min(pathmax[pathmax > 0]):.3e} (nearest) .. {pathmax.max():.3e} (farthest)")
    say(f"       max |Delta fold Sharpe| to the anchor, GROSS rungs only: "
        f"{max(decmax[BIDX[('GROSS', g)]] for g in LAD['GROSS'] if g != A_G):.3e}")
    GATES.append(dict(gate="G10 the E_EXACT class is exactly {N=20, H=126, GROSS=0.75, "
                           "CADENCE=W} (1227's G10)", value=float(len(AEQ["E_EXACT"])),
                      target=4.0,
                      pass_=bool(sorted(BOOKKEY[i] for i in AEQ["E_EXACT"])
                                 == sorted([("N", A_N), ("H", A_H), ("GROSS", A_G), ANCHOR_KEY]))))
    _s = {e: set(AEQ[e].tolist()) for e, _ in ETESTS}
    nested = all(_s[a] <= _s[b] for a, b in
                 (("E_KEY", "E_EXACT"), ("E_EXACT", "E_FP12"), ("E_FP12", "E_RET8"),
                  ("E_EXACT", "E_DEC6"), ("E_DEC6", "E_DEC3")))
    GATES.append(dict(gate="G14 the equivalence tests are nested: E_KEY c E_EXACT c E_FP12 c "
                           "E_RET8 and E_EXACT c E_DEC6 c E_DEC3",
                      value=float(nested), target=1.0, pass_=bool(nested)))

    # ---- chooser machinery (frozen, 1223/1227 verbatim)
    pan_i0 = {p.name: p.i0 for p in panels}
    _SP: dict = {}

    def spread_of(p, lad, lo, hi):
        key = (p, lad, lo, hi)
        if key in _SP:
            return _SP[key]
        v = [sharpe(RM[p][lo:hi, i]) for i in LADIDX[lad]]
        v = [x for x in v if np.isfinite(x)]
        s = (max(v) - min(v)) if len(v) > 1 else np.nan
        _SP[key] = s
        return s

    def pick_of(p, lad, lo, hi):
        v = [(sharpe(RM[p][lo:hi, i]), i) for i in LADIDX[lad]]
        v = [(s, i) for s, i in v if np.isfinite(s)]
        return max(v)[1] if v else ANCHOR_I

    def headline(p, lo, hi, lads):
        sp = {lad: spread_of(p, lad, lo, hi) for lad in lads}
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        if len(good) < 2:
            return {hf: None for hf in HFORMS} | {"_widest": None}
        order = sorted(good, key=lambda k: good[k] / medrange(LADK[k]), reverse=True)
        w = order[0]
        out = {}
        for hf, comparand in (("H_RUNNERUP", order[1]), ("H_NARROWEST", order[-1])):
            if comparand == w:
                out[hf] = None
                continue
            a, b = (w, comparand) if good[w] >= good[comparand] else (comparand, w)
            M_ = (good[a] / good[b]) if good[b] > 0 else (np.inf if good[a] > 0 else 1.0)
            I_ = d2(LADK[a]) / d2(LADK[b])
            c = call_iid95(M_, I_, nullband(LADK[a], LADK[b]))
            out[hf] = None if c == "TIE" else (a if c == "W" else b)
        anyd = False
        for a in lads:
            for b in lads:
                if a == b or not (np.isfinite(sp.get(a, np.nan))
                                  and np.isfinite(sp.get(b, np.nan))):
                    continue
                if sp[a] < sp[b] or (sp[a] == sp[b] and a > b):
                    continue
                M_ = (sp[a] / sp[b]) if sp[b] > 0 else (np.inf if sp[a] > 0 else 1.0)
                I_ = d2(LADK[a]) / d2(LADK[b])
                if call_iid95(M_, I_, nullband(LADK[a], LADK[b])) != "TIE":
                    anyd = True
        out["H_ANY"] = w if anyd else None
        out["_widest"] = w
        return out

    def choose(p, o0, L, sname):
        lads = SETS[sname]
        lo = pan_i0[p] if L is None else max(pan_i0[p], o0 - L)
        hi = o0
        hd = headline(p, lo, hi, lads)
        sp = {lad: spread_of(p, lad, lo, hi) for lad in lads}
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        raw_w = max(good, key=good.get) if good else None
        out = {"CH_ANCHOR": ANCHOR_I,
               "CH_RAW": ANCHOR_I if raw_w is None else pick_of(p, raw_w, lo, hi)}
        for hf in HFORMS:
            named = hd[hf]
            out[hf] = ANCHOR_I if named is None else pick_of(p, named, lo, hi)
        return out, (hi - lo)

    # ---- the walk
    prows, picks = [], {}
    for cad in CADENCES:
        for pan in panels:
            for (v, o0, o1) in folds[(cad, pan.name)]:
                for sname in SETS:
                    for L in WINDOWS:
                        sel, islen = choose(pan.name, o0, L, sname)
                        for ch in CHOOSERS:
                            bi = sel[ch]
                            r = RM[pan.name][o0:o1, bi]
                            picks.setdefault((cad, pan.name, sname, wname(L), ch), []).append(
                                (v, o0, o1, bi))
                            row = dict(cadence=cad, panel=pan.name, fold=v, SET=sname,
                                       window=wname(L), IS_len=islen, chooser=ch,
                                       ladder=BOOKKEY[bi][0], rung=BOOKKEY[bi][1],
                                       OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r), OOS_MaxDD=mdd(r))
                            for ename, _ in ETESTS:
                                row[f"moved_{ename}"] = bool(bi not in set(AEQ[ename].tolist()))
                            prows.append(row)
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)

    say("")
    say("  (B2) THE MOVE RATE ITSELF, DIAL 2 x every pick-cell in the grid "
        f"({len(pdf):,} pick-cells).")
    say("       test      move rate   overstatement vs E_EXACT   pool size   no-ops in pool")
    mrows = []
    for ename, _ in ETESTS:
        mr = float(pdf[f"moved_{ename}"].mean())
        pool = NB - len(AEQ[ename])
        noop = len(AEQ["E_EXACT"]) - len(AEQ[ename]) if ename == "E_KEY" else 0
        mrows.append(dict(etest=ename, move_rate=mr, pool=pool, noops_in_pool=max(noop, 0)))
        say(f"       {ename:8s}  {mr:9.4f}   {mr - float(pdf['moved_E_EXACT'].mean()):+22.4f}   "
            f"{pool:9d}   {max(noop,0):14d}")
    pd.DataFrame(mrows).to_csv(f"{OUT}.moverates.csv", index=False)
    over = float(pdf["moved_E_KEY"].mean() - pdf["moved_E_EXACT"].mean())
    GATES.append(dict(gate="G11 a value-based move rate never exceeds the key-based one",
                      value=over, target=0.0, pass_=bool(over >= 0.0)))
    GATES.append(dict(gate="G15 the key-minus-value overstatement reproduces 1227's committed "
                           "0.0280", value=abs(over - REP1227_OVERSTATEMENT), target=2e-3,
                      pass_=bool(abs(over - REP1227_OVERSTATEMENT) < 2e-3)))
    mv = float(pdf[pdf.chooser == "CH_ANCHOR"][[f"moved_{e}" for e, _ in ETESTS]].values.mean())
    GATES.append(dict(gate="G5 CH_ANCHOR move rate == 0 under every equivalence test", value=mv,
                      target=0.0, pass_=bool(mv == 0.0)))

    # ---- deltas and nulls, per equivalence test
    say("")
    say("  (B3) THE NULLS.  NL_COUNT draws m destinations uniformly from the pool; NL_PERM")
    say("       re-deals the chooser's OWN destinations to random folds.  Both are functions of")
    say("       the equivalence test through m and through the pool.  2,000 reps, seed fixed.")

    def stitched_sharpe_from(cad, p, idxs):
        SU, SQ, NN = FSUM[(cad, p)], FSQ[(cad, p)], FN[(cad, p)]
        rows = np.arange(len(idxs))
        tot = SU[rows, idxs].sum()
        totq = SQ[rows, idxs].sum()
        n = NN.sum()
        mu = tot / n
        sd = np.sqrt(max(totq / n - mu * mu, 0.0))
        return float(mu * np.sqrt(252) / sd) if sd > 0 else np.nan

    cad0, p0 = "QUARTER", panels[0].name
    ii = np.array([ANCHOR_I] * len(FOL[(cad0, p0)]))
    direct = sharpe(np.concatenate([RM[p0][o0:o1, ANCHOR_I] for (_, o0, o1) in FOL[(cad0, p0)]]))
    g7 = abs(stitched_sharpe_from(cad0, p0, ii) - direct)
    GATES.append(dict(gate="G7 stitched Sharpe from per-fold aggregates == direct Sharpe",
                      value=g7, target=1e-12, pass_=bool(g7 < 1e-12)))

    def _m(v):
        v = [x for x in v if np.isfinite(x)]
        return float(np.mean(v)) if v else np.nan

    def nulls(rng, cad, pn, idxs, ename, fold_sel=None):
        """(p_NL_COUNT, p_NL_PERM, m) for one (panel, chooser) cell under equivalence test."""
        S = FS[(cad, pn)]
        F = len(idxs)
        rows = np.arange(F)
        if fold_sel is None:
            fold_sel = rows
        aeq = set(AEQ[ename].tolist())
        pool = np.array([i for i in range(NB) if i not in aeq])
        mask = np.array([b not in aeq for b in idxs])
        sub = np.asarray(fold_sel)
        base = S[rows, np.full(F, ANCHOR_I)]
        obs = float(np.nanmean(S[rows, idxs][sub] - base[sub]))
        m = int(mask[sub].sum())
        if m == 0 or len(pool) == 0:
            return np.nan, np.nan, 0, obs
        dests = np.asarray(idxs)[sub][mask[sub]]
        pos = np.argsort(rng.random((NULL_REPS, len(sub))), axis=1)[:, :m]
        posr = sub[pos]
        dd = rng.choice(pool, size=(NULL_REPS, m))
        draw = np.tile(base[sub], (NULL_REPS, 1))
        draw[np.arange(NULL_REPS)[:, None], pos] = S[posr, dd]
        p_count = float((np.nanmean(draw - base[sub][None, :], axis=1) >= obs).mean())
        perm = rng.permuted(np.tile(dests, (NULL_REPS, 1)), axis=1)
        draw2 = np.tile(base[sub], (NULL_REPS, 1))
        draw2[np.arange(NULL_REPS)[:, None], pos] = S[posr, perm]
        p_perm = float((np.nanmean(draw2 - base[sub][None, :], axis=1) >= obs).mean())
        return p_count, p_perm, m, obs

    rng = np.random.default_rng(NULL_SEED)
    drows = []
    for ename, _ in ETESTS:
        for cad in CADENCES:
            for sname in SETS:
                for L in WINDOWS:
                    w = wname(L)
                    for ch in CHOOSERS:
                        dels, ms, mvr = [], [], []
                        pc, pp, mcount = [], [], 0
                        per_panel = {}
                        for pan in panels:
                            idxs = np.array([b for (_, _, _, b) in
                                             picks[(cad, pan.name, sname, w, ch)]])
                            S = FS[(cad, pan.name)]
                            rows = np.arange(len(idxs))
                            so = S[rows, idxs]
                            sa = S[rows, np.full(len(idxs), ANCHOR_I)]
                            dels.append(so - sa)
                            ms.append(so)
                            mvr.append(np.array([b not in set(AEQ[ename].tolist())
                                                 for b in idxs]))
                            per_panel[pan.name] = idxs
                            a, b_, m_, _o = nulls(rng, cad, pan.name, idxs, ename)
                            pc.append(a)
                            pp.append(b_)
                            mcount += m_
                        d = np.concatenate(dels)
                        maxf = max(len(x) for x in dels)
                        byf = np.full((len(dels), maxf), np.nan)
                        for i, x in enumerate(dels):
                            byf[i, -len(x):] = x
                        fm = np.nanmean(byf, axis=0)
                        fm = fm[np.isfinite(fm)]
                        se = fm.std(ddof=1) / np.sqrt(len(fm)) if len(fm) > 1 else np.nan
                        t = (np.nanmean(d) / se) if (se and se > 0) else 0.0
                        delta = float(np.nanmean(d))
                        p_c, p_p = _m(pc), _m(pp)
                        drows.append(dict(
                            etest=ename, cadence=cad, SET=sname, window=w, chooser=ch,
                            npicks=len(d), moves=mcount,
                            move_rate=float(np.concatenate(mvr).mean()),
                            mean_OOS_Sharpe=float(np.nanmean(np.concatenate(ms))),
                            delta_vs_ANCHOR=delta, SE=se, t=t, p_NL_COUNT=p_c, p_NL_PERM=p_p,
                            publish_COUNT=bool(delta > 0 and np.isfinite(p_c) and p_c <= 0.05),
                            publish_PERM=bool(delta > 0 and np.isfinite(p_p) and p_p <= 0.05),
                            publish_BOTH=bool(delta > 0 and np.isfinite(p_c) and p_c <= 0.05
                                              and np.isfinite(p_p) and p_p <= 0.05)))
    ddf = pd.DataFrame(drows)
    ddf.to_csv(f"{OUT}.deltas.csv", index=False)

    # G12: the books do not change, so nothing about the RETURNS may move with the dial
    key_ = ["cadence", "SET", "window", "chooser"]
    a = ddf[ddf.etest == "E_KEY"].set_index(key_)
    b = ddf[ddf.etest == "E_EXACT"].set_index(key_).reindex(a.index)
    g12 = float(np.nanmax(np.abs(a["delta_vs_ANCHOR"].values - b["delta_vs_ANCHOR"].values)))
    g12 = max(g12, float(np.nanmax(np.abs(a["mean_OOS_Sharpe"].values
                                          - b["mean_OOS_Sharpe"].values))))
    GATES.append(dict(gate="G12 every Sharpe and every delta is identical across the "
                           "equivalence dial (the books do not change)", value=g12, target=0.0,
                      pass_=bool(g12 == 0.0)))

    # replication of 1223 at (YEAR, EXPAND) on the KEY definition it published
    rep_err = 0.0
    for (sname, ch), (mv23, ms23) in REP1223.items():
        s = pdf[(pdf.cadence == "YEAR") & (pdf.window == "EXPAND") & (pdf.SET == sname)
                & (pdf.chooser == ch) & (pdf.fold >= 2013)]
        if not len(s):
            continue
        rep_err = max(rep_err, abs(float(s.moved_E_KEY.mean()) - mv23),
                      abs(float(s.OOS_Sharpe.mean()) - ms23))
    GATES.append(dict(gate="G8 (YEAR, EXPAND) replicates 1223's committed KEY move rates and "
                           "mean OOS Sharpes", value=rep_err, target=2e-2,
                      pass_=bool(rep_err < 2e-2)))

    say("")
    say("  (B4) PUBLISH DECISIONS AT ALL4 / QUARTER.  A cell PUBLISHES when its gain over")
    say("       holding is positive AND clears its own matched null at p <= 0.05.")
    say("       test      cells  pub_COUNT  pub_PERM  pub_BOTH   mean p_COUNT  mean p_PERM")
    for ename, _ in ETESTS:
        q = ddf[(ddf.etest == ename) & (ddf.cadence == "QUARTER") & (ddf.SET == "ALL4")
                & (ddf.chooser.isin(HFORMS + ["CH_RAW"]))]
        say(f"       {ename:8s} {len(q):6d}  {int(q.publish_COUNT.sum()):9d}  "
            f"{int(q.publish_PERM.sum()):8d}  {int(q.publish_BOTH.sum()):8d}   "
            f"{q.p_NL_COUNT.mean():11.4f}  {q.p_NL_PERM.mean():11.4f}")

    say("")
    say("  (B5) FLIPS.  Every (cadence, set, window, chooser) cell, KEY against each test.")
    say("       test      cells  p_COUNT flips  p_PERM flips   worst |dp_COUNT|  worst |dp_PERM|")
    frows = []
    ak = ddf[ddf.etest == "E_KEY"].set_index(key_)
    for ename, _ in ETESTS:
        if ename == "E_KEY":
            continue
        bb = ddf[ddf.etest == ename].set_index(key_).reindex(ak.index)
        f1 = int((ak.publish_COUNT.values != bb.publish_COUNT.values).sum())
        f2 = int((ak.publish_PERM.values != bb.publish_PERM.values).sum())
        d1 = float(np.nanmax(np.abs(ak.p_NL_COUNT.values - bb.p_NL_COUNT.values)))
        d2_ = float(np.nanmax(np.abs(ak.p_NL_PERM.values - bb.p_NL_PERM.values)))
        frows.append(dict(etest=ename, cells=len(ak), flips_COUNT=f1, flips_PERM=f2,
                          worst_dp_COUNT=d1, worst_dp_PERM=d2_,
                          mean_dp_COUNT=float(np.nanmean(ak.p_NL_COUNT.values
                                                         - bb.p_NL_COUNT.values)),
                          mean_dp_PERM=float(np.nanmean(ak.p_NL_PERM.values
                                                        - bb.p_NL_PERM.values))))
        say(f"       {ename:8s} {len(ak):6d}  {f1:13d}  {f2:12d}   {d1:16.4f}  {d2_:14.4f}")
    pd.DataFrame(frows).to_csv(f"{OUT}.flips.csv", index=False)
    say("")
    say("       SIGN OF THE CONTAMINATION.  p(KEY) - p(EXACT), averaged over the same cells:")
    for r in frows:
        say(f"       {r['etest']:8s} NL_COUNT {r['mean_dp_COUNT']:+.4f}   "
            f"NL_PERM {r['mean_dp_PERM']:+.4f}")
    say("")
    say("       ZERO FLIPS AT 0.05 IS NOT THE SAME AS AN INERT DIAL, SO THE BAR IS WALKED.")
    say("       Flips between the CONTAMINATED (E_KEY) and CLEAN (E_EXACT) pool at every alpha,")
    say("       over all 120 (cadence, set, window, chooser) cells.  Alpha is NOT a dial: the")
    say("       verdict is read at 0.05 and the whole ladder is published.")
    say("       alpha   pub_KEY  pub_EXACT   flips_COUNT  flips_PERM")
    arows = []
    pk_c, pe_c = ak.p_NL_COUNT.values, ddf[ddf.etest == "E_EXACT"].set_index(key_)\
        .reindex(ak.index).p_NL_COUNT.values
    pk_p, pe_p = ak.p_NL_PERM.values, ddf[ddf.etest == "E_EXACT"].set_index(key_)\
        .reindex(ak.index).p_NL_PERM.values
    dpos = ak.delta_vs_ANCHOR.values > 0
    for al in [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]:
        a1 = dpos & np.isfinite(pk_c) & (pk_c <= al)
        b1 = dpos & np.isfinite(pe_c) & (pe_c <= al)
        a2 = dpos & np.isfinite(pk_p) & (pk_p <= al)
        b2 = dpos & np.isfinite(pe_p) & (pe_p <= al)
        arows.append(dict(alpha=al, pub_KEY=int(a1.sum()), pub_EXACT=int(b1.sum()),
                          flips_COUNT=int((a1 != b1).sum()), flips_PERM=int((a2 != b2).sum())))
        say(f"       {al:5.2f}   {int(a1.sum()):7d}  {int(b1.sum()):9d}   "
            f"{int((a1 != b1).sum()):11d}  {int((a2 != b2).sum()):10d}")
    adf = pd.DataFrame(arows)
    pd.DataFrame(arows).to_csv(f"{OUT}.alpha.csv", index=False)
    maxflip = int(max(adf.flips_COUNT.max(), adf.flips_PERM.max()))
    say(f"       WORST CASE OVER THE LADDER: {maxflip} of {len(ak)} cells change their publish")
    say(f"       decision at some alpha; at the record's own 0.05 it is "
        f"{int(adf[adf.alpha == 0.05].flips_COUNT.iloc[0] + adf[adf.alpha == 0.05].flips_PERM.iloc[0])}.")

    # ---------------------------------------------------------------- ARM C: capital
    say("")
    say("=" * 108)
    say("ARM C — THE CAPITAL LEG.  RULE 8, BOTH KEEP PATHS, AND THE PRICE OF THE PUBLISH RULE")
    say("=" * 108)
    say("")
    say("  BENCHMARKS over each panel's QUARTER fold span (10 bps, t+1):")
    BM = {}
    for pan in panels:
        fl = folds[("QUARTER", pan.name)]
        a0, a1 = fl[0][1], fl[-1][2]
        ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[a0:a1]
            h1, h2 = halves(full)
            o = r[max(a0, ioos):a1]
            oh1, oh2 = halves(o)
            BM[(pan.name, nm)] = dict(**triple(full), H1=h1, H2=h2, OOS_CAGR=cagr(o),
                                      OOS_Sharpe=sharpe(o), OOS_MaxDD=mdd(o), OH1=oh1, OH2=oh2)
            d = BM[(pan.name, nm)]
            say(f"    {pan.name:6s} {nm:5s} {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / "
                f"{d['MaxDD']:8.2%}  halves {d['H1']:.4f}/{d['H2']:.4f}  "
                f"OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    def bm_of(p, nm, oos=False):
        d = BM[(p, nm)]
        if not oos:
            return dict(H1=d["H1"], H2=d["H2"], CAGR=d["CAGR"], MaxDD=d["MaxDD"])
        return dict(H1=d["OH1"], H2=d["OH2"], CAGR=d["OOS_CAGR"], MaxDD=d["OOS_MaxDD"])

    say("")
    say("  (C1) BOTH KEEP PATHS ON EVERY RUNG BOOK (nothing selected on):")
    brows = []
    for pan in panels:
        fl = folds[("QUARTER", pan.name)]
        a0, a1 = fl[0][1], fl[-1][2]
        ioos = max(a0, pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        for k, i in BIDX.items():
            r = RM[pan.name][a0:a1, i]
            k4a, k4b, m, h1, h2 = keep_paths(r, bm_of(pan.name, "SPY"), bm_of(pan.name, "LIVE"))
            ro = RM[pan.name][ioos:a1, i]
            _, k4bo, mo, _, _ = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                           bm_of(pan.name, "LIVE", True))
            brows.append(dict(panel=pan.name, ladder=k[0], rung=k[1],
                              anchor_equivalent=bool(i in set(AEQ["E_EXACT"].tolist())), **m,
                              H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4bo))
    bdf = pd.DataFrame(brows)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"    {len(bdf)} rung books ({len(bdf.drop_duplicates(subset=['panel','CAGR','Sharpe']))} "
        f"DISTINCT by value): 4a {int(bdf.KEEP_4a.sum())}; 4b full {int(bdf.KEEP_4b.sum())}; "
        f"4b OOS {int(bdf.KEEP_4b_OOS.sum())}; BOTH {int((bdf.KEEP_4b & bdf.KEEP_4b_OOS).sum())}")
    bb = bdf[bdf.KEEP_4b & bdf.KEEP_4b_OOS]
    if len(bb):
        z = bb.loc[bb.OOS_Sharpe.idxmax()]
        say(f"    Best book passing 4b FULL and OOS: {z.panel} {z.ladder}={z.rung}  full "
            f"{z.CAGR:.2%} / {z.Sharpe:.4f} / {z.MaxDD:.2%} (halves {z.H1:.4f}/{z.H2:.4f}), "
            f"OOS {z.OOS_CAGR:.2%} / {z.OOS_Sharpe:.4f} / {z.OOS_MaxDD:.2%}")

    say("")
    say("  (C2) STITCHED DEPLOYABLE CURVES, BOTH KEEP PATHS:")
    srows2 = []
    stitch_len_err = 0.0
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            a0, a1 = fl[0][1], fl[-1][2]
            ioos = max(a0, pan.idx.searchsorted(pd.Timestamp(OOS_START)))
            for sname in SETS:
                for L in WINDOWS:
                    for ch in CHOOSERS:
                        pk = picks[(cad, pan.name, sname, wname(L), ch)]
                        r = np.concatenate([RM[pan.name][o0:o1, b] for (_, o0, o1, b) in pk])
                        ro = np.concatenate([RM[pan.name][max(o0, ioos):o1, b]
                                             for (_, o0, o1, b) in pk if o1 > ioos])
                        stitch_len_err = max(stitch_len_err,
                                             abs(len(r) - sum(o1 - o0 for (_, o0, o1, _) in pk)))
                        k4a, k4b, m, h1, h2 = keep_paths(r, bm_of(pan.name, "SPY"),
                                                         bm_of(pan.name, "LIVE"))
                        _, k4bo, mo, _, _ = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                                       bm_of(pan.name, "LIVE", True))
                        srows2.append(dict(cadence=cad, panel=pan.name, SET=sname,
                                           window=wname(L), chooser=ch, ndays=len(r), **m,
                                           H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                           OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                           KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4bo))
    sdf = pd.DataFrame(srows2)
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    GATES.append(dict(gate="G6 each stitched curve's length == the sum of its folds'",
                      value=stitch_len_err, target=0.0, pass_=bool(stitch_len_err == 0)))
    say(f"    {len(sdf)} stitched curves: 4a {int(sdf.KEEP_4a.sum())}; 4b full "
        f"{int(sdf.KEEP_4b.sum())}; 4b OOS {int(sdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((sdf.KEEP_4b & sdf.KEEP_4b_OOS).sum())}")

    say("")
    say("  (C3) RULE 8 — THE PRICE OF THE PUBLISH RULE.  For every (cadence, panel, set, window,")
    say("       chooser) the IS folds (closing before 2017-01-01) decide DEPLOY vs HOLD: deploy")
    say("       iff the IS gain is positive AND clears the matched null at p <= 0.05 under the")
    say("       named equivalence test.  2017-2026 is then read ONCE.")
    rng8 = np.random.default_rng(NULL_SEED + 8)
    wrows = []
    for ename, _ in ETESTS:
        for cad in CADENCES:
            for pan in panels:
                fl = folds[(cad, pan.name)]
                ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
                isf = np.array([i for i, (_, o0, o1) in enumerate(fl) if o1 <= ioos])
                oof = np.array([i for i, (_, o0, o1) in enumerate(fl) if o0 >= ioos])
                if not len(isf) or not len(oof):
                    continue
                S = FS[(cad, pan.name)]
                for sname in SETS:
                    for L in WINDOWS:
                        for ch in CHOOSERS:
                            pk = picks[(cad, pan.name, sname, wname(L), ch)]
                            idxs = np.array([b for (_, _, _, b) in pk])
                            pc, pp, m_, obs_is = nulls(rng8, cad, pan.name, idxs, ename,
                                                       fold_sel=isf)
                            deploy = bool(obs_is > 0 and np.isfinite(pc) and pc <= 0.05)
                            used = idxs.copy()
                            if not deploy:
                                used[:] = ANCHOR_I
                            oos_mean = float(np.nanmean(S[oof, used[oof]]))
                            anch_mean = float(np.nanmean(S[oof, np.full(len(oof), ANCHOR_I)]))
                            ro = np.concatenate([RM[pan.name][fl[i][1]:fl[i][2], used[i]]
                                                 for i in oof])
                            k4a, k4b, mo, h1, h2 = keep_paths(
                                ro, bm_of(pan.name, "SPY", True), bm_of(pan.name, "LIVE", True))
                            wrows.append(dict(etest=ename, cadence=cad, panel=pan.name,
                                              SET=sname, window=wname(L), chooser=ch,
                                              IS_gain=obs_is, IS_p=pc, IS_moves=m_,
                                              deploy=deploy, OOS_mean_fold_Sharpe=oos_mean,
                                              anchor_mean_fold_Sharpe=anch_mean,
                                              OOS_delta=oos_mean - anch_mean, **mo, H1=h1, H2=h2,
                                              KEEP_4a=k4a, KEEP_4b=k4b))
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say("       test      deploys/decisions   mean OOS fold Sharpe   vs ALWAYS-HOLD   4a  4b")
    for ename, _ in ETESTS:
        q = wdf[wdf.etest == ename]
        say(f"       {ename:8s} {int(q.deploy.sum()):6d} / {len(q):-6d}        "
            f"{q.OOS_mean_fold_Sharpe.mean():14.4f}   {q.OOS_delta.mean():+14.4f}   "
            f"{int(q.KEEP_4a.sum()):3d} {int(q.KEEP_4b.sum()):3d}")
    hold = wdf[wdf.etest == "E_KEY"].anchor_mean_fold_Sharpe.mean()
    say(f"       ALWAYS-HOLD (do nothing) mean OOS fold Sharpe {hold:.4f}")

    say("")
    say("  (C4) THE CLASSIC RULE-8 PICK (window, chooser chosen on IS mean fold Sharpe at ALL4,")
    say("       2017-2026 read once) — unchanged by the dial, because the books are unchanged:")
    say("       panel  IS-chosen (window, form)   OOS CAGR / Sharpe / MaxDD   halves       4a 4b")
    c4 = []
    for cad in ["QUARTER", "YEAR"]:
        say(f"       --- {cad} folds ---")
        for pan in panels:
            fl = folds[(cad, pan.name)]
            ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
            isf = [i for i, (_, o0, o1) in enumerate(fl) if o1 <= ioos]
            oof = [i for i, (_, o0, o1) in enumerate(fl) if o0 >= ioos]
            S = FS[(cad, pan.name)]
            best, bestv = None, -np.inf
            for L in WINDOWS:
                for ch in CHOOSERS:
                    idxs = np.array([b for (_, _, _, b) in
                                     picks[(cad, pan.name, "ALL4", wname(L), ch)]])
                    v = float(np.nanmean(S[isf, idxs[isf]])) if isf else np.nan
                    if np.isfinite(v) and v > bestv:
                        bestv, best = v, (L, ch)
            for tag, (L, ch) in (("IS-CHOSEN", best), ("ANCHOR", (None, "CH_ANCHOR"))):
                pk = picks[(cad, pan.name, "ALL4", wname(L), ch)]
                ro = np.concatenate([RM[pan.name][o0:o1, b]
                                     for i, (_, o0, o1, b) in enumerate(pk) if i in oof])
                k4a, k4b, m, h1, h2 = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                                 bm_of(pan.name, "LIVE", True))
                c4.append(dict(cadence=cad, panel=pan.name, tag=tag, window=wname(L), chooser=ch,
                               **m, H1=h1, H2=h2, KEEP_4a=k4a, KEEP_4b=k4b))
                say(f"       {pan.name if tag=='IS-CHOSEN' else '':6s} {wname(L):7s} {ch:12s}  "
                    f"{m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:8.2%}  "
                    f"{h1:.4f}/{h2:.4f}   {'T' if k4a else 'F'}  {'T' if k4b else 'F'}")
            d = BM[(pan.name, "SPY")]
            say(f"       {'':6s} SPY                    {d['OOS_CAGR']:7.2%} / "
                f"{d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")
            d = BM[(pan.name, "LIVE")]
            say(f"       {'':6s} LIVE RULES v2          {d['OOS_CAGR']:7.2%} / "
                f"{d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")
    pd.DataFrame(c4).to_csv(f"{OUT}.rule8.csv", index=False)

    # ---------------------------------------------------------------- verdict
    say("")
    say("=" * 108)
    say("VERDICT")
    say("=" * 108)
    hd = crows[0]
    exposed_head = hd["EXPOSED"] + hd["EXPOSED_IMPLICIT"]
    tot_flips = sum(r["flips_COUNT"] + r["flips_PERM"] for r in frows)
    say(f"  CENSUS (C_HEAD, the record's result sentences): {exposed_head} of {hd['units']} "
        f"committed move rates are EXPOSED — key-based on a grid whose")
    say(f"  anchor is degenerate; {hd['CLEAN']} CLEAN, {hd['UNRECOVERABLE']} UNRECOVERABLE, "
        f"{hd['NOT_DEGENERATE']} on a non-degenerate grid. "
        f"{hd['states_basis']} state their basis in the sentence.")
    say(f"  RE-PRICING: the key definition overstates the move rate by {over:.4f} of pick-cells; "
        f"{tot_flips} publish decisions flip at the record's 0.05,")
    say(f"  {maxflip} of {len(ak)} cells flip at some alpha on the published ladder, and the "
        f"p-value itself moves by up to {max(r['worst_dp_COUNT'] for r in frows):.4f}.")
    if exposed_head == 0:
        outcome = "(A) THE RECORD IS CLEAN"
    elif tot_flips > 0:
        outcome = "(B) THE RECORD IS EXPOSED AND THE RE-PRICING MOVES PUBLISH DECISIONS"
    else:
        outcome = "(C) EXPOSED BUT INERT"
    say(f"  PRE-DECLARED OUTCOME: {outcome}")
    say("")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents; SMALL is the sub-$2B")
    say(f"  screen with {len(pxS.columns)-1-len(inv)} of {len(pxS.columns)-1} tickers dropped for")
    say("  max_1d_move >= 1.0, SPY excluded from its eligible set.  The census arms scan")
    say("  committed text and source and carry no market bias; the bias does NOT cancel out of")
    say("  the OOS levels or the 4b legs, so any pass there is an upper bound.")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say(f"  GATES {int(gdf.pass_.sum())} of {len(gdf)}:")
    for _, g in gdf.iterrows():
        say(f"    [{'PASS' if g.pass_ else 'FAIL'}] {g.gate}  value={g.value:.3e} "
            f"target={g.target:.3e}")
    say("")
    say(f"  Runtime {time.time()-t0:.0f}s, offline, deterministic.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
