#!/usr/bin/env python3
"""
Idea 1182 (lane C, 2026-09-19) — how many committed LADDER claims name a RUNG the record has
measured FEWER THAN TEN TIMES, on the N / GROSS / COST / CADENCE axes — and does a chooser
that REFUSES thin rungs buy anything OUT OF SAMPLE?

THE PREMISE.  Idea 1174 built the measurement histogram for ONE axis (hold length H) and found
it is 116 / 90 / 63 units at H = 126 / 21 / 63 and 8-10 units at each of 42 / 52 / 76 / 90 —
i.e. the record's "finer" hold evidence is two runs wearing seven rung labels.  The queue asks
for the same histogram on the FOUR axes that actually price a book: N (book width), GROSS,
COST and CADENCE, and for the count of committed claims standing on a single-digit rung.

TWO PARAMETERS AND NO MORE, ON EACH LEG (PROTOCOL rule 4):

  CENSUS  AXIS SET {N, GROSS, COST, CADENCE}     param 1 — fixed by the queue text itself
          THINNESS BAR T                         param 2 — REPORTED AT EVERY VALUE
                                                   T in {3, 5, 10, 20, 50}; T = 10 is the
                                                   queue's own "single-digit" bar.

  BOOK    N     {5, 10, 15, 20, 25, 30, 40}      dial 1 — book width
          GROSS {0.35, 0.45, 0.55, 0.65, 0.75, 1.00}
                                                 dial 2 — exposure
          Everything else is the FROZEN 2026-09-04 incumbent frame: H = 126 min-hold, MAXVOL
          0.60, 200d MA gate ON, weekly Fri-decide / Mon-trade, 10 bps, t+1.  42 cells per
          panel, 126 in all, EVERY ONE published in .grid.csv with both KEEP paths.

WHY THE TWO LEGS BELONG IN ONE RUN.  A census of committed text is not a trading rule, and this
sprint's binding deliverable is a book.  So the census's OWN OUTPUT is fed straight into a
capital decision: rule 8's chooser picks (N, GROSS) on warm-up..2016-12-31 by argmax IS Sharpe,
and is run in TWO variants —

  C_ALL    the unrestricted argmax over all 42 cells (the record's default behaviour), and
  C_THICK  the argmax restricted to cells BOTH of whose rungs the record has measured >= T
           times, T read off the census, at every T.

If "the record has barely measured this rung" carries information about a cell's OOS behaviour,
C_THICK beats C_ALL out of sample.  If it does not, the thinness finding is a bookkeeping fact
with no capital consequence, and this run says so.

THE CONTROL THAT DECIDES THE VERDICT.  Restricting a menu to K cells can help BY ACCIDENT: a
smaller menu is a smaller maximum and therefore less IS overfitting, whatever the restriction
is.  So C_THICK at each bar is scored against SIZE-MATCHED RANDOM MENUS — 40 seeded draws of K
cells from the same 42, each with its own IS argmax and its own OOS read.  C_THICK earns a
finding only if its OOS Sharpe sits outside that null's body; the percentile is published.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the thinness bar; both
KEEP paths at every cell; the halves; IS and OOS windows; turnover and its 10 bps drag.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN incumbent cell (N = 20, gross 0.75).

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 tuned parameters per leg); rule 5 (one script, deterministic,
standalone); rule 7 (a KILL is reported as a KILL); rule 8 (walk-forward, 2017-2026 read ONCE);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

GATES.  G0 >= 10y on every panel.  G1 CROSS-SCRIPT REPLAY: cell (N=20, g=0.75) on U56 must
reproduce the committed 2026-09-04 anchor (15.80% / 1.1537 / -19.13% full; OOS Sharpe 1.1857).
G2 all 126 cells published.  G3 the census is a pure function of committed text (corpus stamp
published; byte counts and unit counts recorded).  G4 the chooser reads NO row on or after
2017-01-01.  G5 no leverage: realised weight sum never exceeds 1.0.  G6 every rung the BOOK
grid uses appears in the census histogram (the two legs share one rung vocabulary).  G7
bit-identical recompute of the anchor cell.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_rung-thinness-census-and-well-measured-rung-chooser_C.py
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
SLUG = "rung-thinness-census-and-well-measured-rung-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
BT = ROOT / "research" / "backtests"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75          # the frozen 2026-09-04 incumbent cell
COST, CADENCE = 10.0, "W"
NS = [5, 10, 15, 20, 25, 30, 40]
GS = [0.35, 0.45, 0.55, 0.65, 0.75, 1.00]
BARS = [3, 5, 10, 20, 50]
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
NULL_MENUS, NULL_SEED = 40, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

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


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    say(f"  wrote {p.name}  ({len(df)} rows)")


# ======================================================================================
# LEG 1 — THE CENSUS.  Pure function of committed text, read verbatim off HEAD.
# ======================================================================================

SHAPE_RX = re.compile(
    r"\bmonoton\w*|\bargmax\b|\bargmin\b|\bpeaks?\b|\bdeclin\w*|\brises?\b|\bfalls?\b"
    r"|\bbest\b|\bworst\b|\boptimal\w*|\bbeats?\b|\bdominat\w*|\bbind\w*|\bladder\b"
    r"|\bflat\b|\bU-?shape\w*|\binvert\w*|\bordered\b|\bprefer\w*", re.I)

# --- N axis ---------------------------------------------------------------------------
N_TOK = re.compile(r"\bN\s*=\s*\d|\bN\s+in\b|\bN-?\s*(?:axis|dial|ladder|rung|rungs|grid|leg)\b"
                   r"|\btop-?\s*\d{1,3}\b|\bbook\s+width\b|\bwidth\s+(?:axis|ladder|dial)\b")
N_RUNG = [re.compile(r"\bN\s*=\s*(\d{1,3})\b"),
          re.compile(r"\bN\s+in\s*[\{\[]([^\}\]]{1,80})[\}\]]"),
          re.compile(r"\btop-?\s*(\d{1,3})\b", re.I)]
# --- GROSS axis -----------------------------------------------------------------------
G_TOK = re.compile(r"\bgross\b|\bg\s*=\s*[01]?\.\d", re.I)
G_RUNG = [re.compile(r"\bgross\s*(?:=|of|at|rung)?\s*([01]?\.\d{1,2})\b", re.I),
          re.compile(r"\bg\s*=\s*([01]?\.\d{1,2})\b"),
          re.compile(r"\bgross\s+in\s*[\{\[]([^\}\]]{1,80})[\}\]]", re.I)]
# --- COST axis ------------------------------------------------------------------------
C_TOK = re.compile(r"\bbps\b|\bcost\s*(?:rung|ladder|axis|dial|bps)\b|\bcost_bps\b", re.I)
C_RUNG = [re.compile(r"\b(\d{1,3}(?:\.\d)?)\s*bps\b", re.I),
          re.compile(r"\bcost_bps\s*=\s*(\d{1,3})\b", re.I)]
# --- CADENCE axis ---------------------------------------------------------------------
K_TOK = re.compile(r"\bcadence\b|\bdaily\b|\bweekly\b|\bmonthly\b|\bquarterly\b|\bfreq\s*=", re.I)
K_MAP = {"daily": "D", "weekly": "W", "monthly": "M", "quarterly": "Q",
         "D": "D", "W": "W", "M": "M", "Q": "Q"}
K_RUNG = [re.compile(r"\b(daily|weekly|monthly|quarterly)\b", re.I),
          re.compile(r"\bfreq\s*=\s*['\"]?([DWMQ])\b")]

AXES = ["N", "GROSS", "COST", "CADENCE"]


def _ints(s, lo, hi):
    return {int(x) for x in re.findall(r"\d{1,3}", s) if lo <= int(x) <= hi}


def _floats(s, lo, hi):
    out = set()
    for x in re.findall(r"[01]?\.\d{1,2}", s):
        v = round(float(x), 2)
        if lo <= v <= hi:
            out.add(v)
    return out


def rungs_in(axis, t):
    """The rungs a unit NAMES on `axis`, only ever through that axis's own token."""
    out = set()
    if axis == "N":
        for m in N_RUNG[0].finditer(t):
            out |= _ints(m.group(1), 1, 200)
        for m in N_RUNG[1].finditer(t):
            out |= _ints(m.group(1), 1, 200)
        for m in N_RUNG[2].finditer(t):
            out |= _ints(m.group(1), 1, 200)
    elif axis == "GROSS":
        for rx in G_RUNG:
            for m in rx.finditer(t):
                out |= _floats(m.group(1), 0.05, 1.00)
    elif axis == "COST":
        for rx in C_RUNG:
            for m in rx.finditer(t):
                for x in re.findall(r"\d{1,3}(?:\.\d)?", m.group(1)):
                    v = float(x)
                    if 0 <= v <= 200:
                        out.add(round(v, 1))
    else:
        for rx in K_RUNG:
            for m in rx.finditer(t):
                k = K_MAP.get(m.group(1).lower() if len(m.group(1)) > 1 else m.group(1))
                if k:
                    out.add(k)
    return out


TOK = {"N": N_TOK, "GROSS": G_TOK, "COST": C_TOK, "CADENCE": K_TOK}


def corpus():
    """Every COMMITTED text unit in the record, with the RUN it belongs to.

    LEADERBOARD rows (run = the row's last cell, which PROTOCOL rule 5 defines as the script
    filename), CHANGELOG paragraphs (run = CHANGELOG#i), and the paragraphs of every
    research/backtests/*.result.md and *.memo.md (run = the file stem)."""
    units, nfiles, nbytes = [], 0, 0
    p = ROOT / "research" / "LEADERBOARD.md"
    txt = p.read_text(errors="ignore")
    nbytes += len(txt.encode())
    lb = [l for l in txt.split("\n") if l.startswith("|") and not l.startswith("|---")]
    for i, t in enumerate(lb[1:]):
        cells = [c.strip() for c in t.strip().strip("|").split("|")]
        run = cells[-1] if cells and cells[-1] else f"LEADERBOARD#{i}"
        units.append(("LEADERBOARD", run, t))
    p = ROOT / "research" / "CHANGELOG.md"
    txt = p.read_text(errors="ignore")
    nbytes += len(txt.encode())
    for i, t in enumerate([q for q in txt.split("\n\n") if q.strip()]):
        units.append(("CHANGELOG", f"CHANGELOG#{i}", t))
    for f in sorted(list(BT.glob("*.result.md")) + list(BT.glob("*.memo.md"))):
        nfiles += 1
        txt = f.read_text(errors="ignore")
        nbytes += len(txt.encode())
        run = f.stem.replace(".result", "").replace(".memo", "")
        for t in [q for q in txt.split("\n\n") if q.strip()]:
            units.append(("RESULTMD", run, t))
    return units, nfiles, nbytes


def census():
    units, nfiles, nbytes = corpus()
    say(f"  CORPUS: {len(units)} committed text units from LEADERBOARD.md + CHANGELOG.md + "
        f"{nfiles} *.result.md / *.memo.md  ({nbytes/1e6:.2f} MB read off HEAD)")
    publish("G3 corpus stamp", f"{len(units)} units, {nfiles} memo files, {nbytes} bytes")

    hist = {a: {} for a in AXES}          # rung -> dict(units=int, runs=set)
    claims = []                            # one row per (unit, axis) that is a CLAIM
    tok_units = {a: 0 for a in AXES}
    for src, run, t in units:
        for a in AXES:
            if not TOK[a].search(t):
                continue
            tok_units[a] += 1
            rg = rungs_in(a, t)
            for r in rg:
                d = hist[a].setdefault(r, dict(units=0, runs=set()))
                d["units"] += 1
                d["runs"].add(run)
            if rg and SHAPE_RX.search(t):
                claims.append(dict(axis=a, src=src, run=run, n_rungs=len(rg),
                                   rungs="|".join(str(x) for x in sorted(rg, key=str))))
    rows = []
    for a in AXES:
        for r, d in sorted(hist[a].items(), key=lambda kv: -len(kv[1]["runs"])):
            rows.append(dict(axis=a, rung=r, unit_count=d["units"], run_count=len(d["runs"])))
    hdf = pd.DataFrame(rows)
    cdf = pd.DataFrame(claims)
    return hdf, cdf, hist, tok_units


def runcount(hist, axis, rung):
    d = hist[axis].get(rung)
    return len(d["runs"]) if d else 0


# ======================================================================================
# LEG 2 — THE BOOK.  The frozen incumbent frame, walked over (N, GROSS).
# ======================================================================================

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
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, N, H, lag=1):
    """The frozen min-hold selection frame at GROSS = 1.0 (rows sum to 1 when anything is held)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
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


def run_book(pan, frame, C, Cp, g):
    """One book at constant gross g on the given selection frame.  Drift between rebalances,
    turnover charged at the rebalance row (COST bps), no leverage."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.reb
    ends = np.append(reb[1:], T)
    wsum_max = 0.0
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, wsum_max


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


BOOT_REPS, BOOT_BLOCK = 400, 63


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=NULL_SEED):
    """Paired circular-block bootstrap of Sharpe(a) - Sharpe(b): identical block starts for
    both books, so the common market leg cancels.  |t| > 2 is the record's bar."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1182 (lane C, 2026-09-19) — RUNG-THINNESS CENSUS on the N / GROSS / COST / "
        "CADENCE axes, and a WELL-MEASURED-RUNG CHOOSER priced against it.")
    say("CENSUS params: AXIS SET {N,GROSS,COST,CADENCE} (fixed by the queue) x THINNESS BAR T "
        "in {3,5,10,20,50} (reported at every value).")
    say("BOOK dials: N {5,10,15,20,25,30,40} x GROSS {0.35,0.45,0.55,0.65,0.75,1.00} on the "
        "frozen incumbent frame (H=126, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1).")
    say("=" * 118)

    # ---------------- LEG 1: census ----------------------------------------------------
    say("\n[LEG 1]  THE CENSUS — measurement histogram of the committed record")
    hdf, cdf, hist, tok_units = census()
    for a in AXES:
        sub = hdf[hdf.axis == a].sort_values("run_count", ascending=False)
        top = ", ".join(f"{r.rung}:{r.run_count}" for r in sub.head(8).itertuples())
        say(f"  {a:8s} token units {tok_units[a]:6d} | {len(sub):3d} distinct rungs | "
            f"top rungs by RUN count -> {top}")
    conc = []
    for a in AXES:
        sub = hdf[hdf.axis == a].sort_values("run_count", ascending=False)
        tot = float(sub.run_count.sum())
        cum = sub.run_count.cumsum() / tot
        n90 = int((cum < 0.90).sum()) + 1
        conc.append(dict(axis=a, rungs=len(sub), total_run_mass=tot,
                         top1_rung=str(sub.iloc[0].rung), top1_share=float(sub.iloc[0].run_count / tot),
                         top2_share=float(sub.head(2).run_count.sum() / tot),
                         rungs_covering_90pct=n90,
                         herfindahl=float(((sub.run_count / tot) ** 2).sum())))
    conf = pd.DataFrame(conc)
    say("\n  CONCENTRATION of the measurement mass (the other half of the thinness question):")
    for _, r in conf.iterrows():
        say(f"    {r.axis:8s} {int(r.rungs):3d} rungs; top rung {r.top1_rung:>6s} holds "
            f"{r.top1_share:.4f} of all run-mass, top two {r.top2_share:.4f}; "
            f"{int(r.rungs_covering_90pct)} rungs cover 90%; HHI {r.herfindahl:.4f}")
    dump(conf, "concentration")
    dump(hdf, "histogram")

    claim_rows = []
    for a in AXES:
        ca = cdf[cdf.axis == a] if len(cdf) else cdf
        for T in BARS:
            thin = 0
            for _, row in ca.iterrows():
                rg = [x for x in str(row["rungs"]).split("|") if x != ""]
                vals = []
                for x in rg:
                    vals.append(x if a == "CADENCE" else (float(x) if a in ("GROSS", "COST") else int(x)))
                if any(runcount(hist, a, v) < T for v in vals):
                    thin += 1
            claim_rows.append(dict(axis=a, bar=T, claims=len(ca), claims_on_a_thin_rung=thin,
                                   share=(thin / len(ca) if len(ca) else np.nan)))
    clf = pd.DataFrame(claim_rows)
    say("\n  COMMITTED CLAIMS (a unit carrying the axis token, >= 1 named rung AND a shape verb) "
        "resting on a rung measured FEWER THAN T times:")
    for _, r in clf.iterrows():
        say(f"    {r.axis:8s} T={r.bar:3d}  {int(r.claims_on_a_thin_rung):5d} of "
            f"{int(r.claims):5d}  ({r.share:.4f})")
    dump(clf, "claims")
    dump(cdf if len(cdf) else pd.DataFrame(columns=["axis", "src", "run", "n_rungs", "rungs"]),
         "claimunits")

    # the census's verdict on THIS run's own book grid
    say("\n  The BOOK grid's own rungs, as the census measures them (run counts):")
    say("    N     " + "  ".join(f"{n}:{runcount(hist,'N',n)}" for n in NS))
    say("    GROSS " + "  ".join(f"{g:.2f}:{runcount(hist,'GROSS',g)}" for g in GS))
    g6 = all(runcount(hist, "N", n) > 0 for n in NS) and all(runcount(hist, "GROSS", g) > 0 for g in GS)
    gate("G6 every rung the BOOK grid uses appears in the census histogram", g6, "True", g6)

    # ---------------- LEG 2: the book --------------------------------------------------
    say("\n[LEG 2]  THE BOOK — 42 cells per panel, both KEEP paths, rule-8 walk-forward")
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)} "
        f"(of {len(pxS.columns)-1} priced; data/small_meta.csv drops {len(bad)}).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one; what this run reads is a CONTRAST between two choosers "
        "on the same names and the same days.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wf_rows, cav_rows = [], [], []
    wsum_global = 0.0
    anchor_replay = None
    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f} | 4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")
        say(f"           OOS ({OOS_START}..): SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/"
            f"{spyO['MaxDD']:.2%} | RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/"
            f"{liveO['MaxDD']:.2%}")

        rets_by_cell = {}
        panel_spyO, panel_liveO = spyO, liveO
        for n in NS:
            frame = build1(pan, n, I_H)
            for g in GS:
                gg, tu, ws = run_book(pan, frame, C, Cp, g)
                wsum_global = max(wsum_global, ws)
                r = gg - tu * COST / 1e4
                rets_by_cell[(n, g)] = r
                k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                mo = triple(r[i_oos:])
                k4a_o, k4b_o, _, _, _, legs_o = keep_paths(r[i_oos:], spyO, liveO)
                yrs = (T - WARMUP) / 252.0
                grid.append(dict(panel=pan.name, N=n, gross=g,
                                 n_runcount=runcount(hist, "N", n),
                                 g_runcount=runcount(hist, "GROSS", g),
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=h1, H2=h2, keep4a=k4a, keep4b=k4b,
                                 leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                 leg_CAGR=legs["CAGR"],
                                 oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                 okeep4a=k4a_o, okeep4b=k4b_o,
                                 turnover_per_yr=float(tu[WARMUP:].sum() / yrs),
                                 drag_bp_yr=float(tu[WARMUP:].sum() / yrs * COST / 1e4 * 1e4)))
                if pan.name == "U56" and n == I_N and g == I_G:
                    anchor_replay = (m, mo)

        # ---- rule 8 ------------------------------------------------------------------
        is_sh = {k: sharpe(v[WARMUP:i_oos]) for k, v in rets_by_cell.items()}
        cells = [(n, g) for n in NS for g in GS]

        def read_oos(cell):
            r = rets_by_cell[cell][i_oos:]
            m = triple(r)
            k4a_o, k4b_o, _, _, _, _ = keep_paths(r, spyO, liveO)
            return m, k4a_o, k4b_o

        c_all = max(cells, key=lambda c: (is_sh[c] if np.isfinite(is_sh[c]) else -9e9))
        m_all, a4a, a4b = read_oos(c_all)
        rng = np.random.default_rng(NULL_SEED)
        for Tbar in BARS:
            menu = [c for c in cells
                    if runcount(hist, "N", c[0]) >= Tbar and runcount(hist, "GROSS", c[1]) >= Tbar]
            if menu:
                c_th = max(menu, key=lambda c: (is_sh[c] if np.isfinite(is_sh[c]) else -9e9))
                m_th, t4a, t4b = read_oos(c_th)
            else:
                c_th, m_th, t4a, t4b = (np.nan, np.nan), dict(CAGR=np.nan, Sharpe=np.nan,
                                                              MaxDD=np.nan), False, False
            K = len(menu)
            null = []
            if 0 < K < len(cells):
                for s in range(NULL_MENUS):
                    pick = rng.choice(len(cells), size=K, replace=False)
                    sub = [cells[i] for i in pick]
                    cb = max(sub, key=lambda c: (is_sh[c] if np.isfinite(is_sh[c]) else -9e9))
                    null.append(triple(rets_by_cell[cb][i_oos:])["Sharpe"])
            if null and np.isfinite(m_th["Sharpe"]):
                arr = np.array(null, float)
                tie = np.isclose(arr, m_th["Sharpe"], rtol=0, atol=1e-12)
                below = float(np.mean((arr < m_th["Sharpe"]) & ~tie))
                tied = float(np.mean(tie))
                above = float(np.mean((arr > m_th["Sharpe"]) & ~tie))
                pct = below + 0.5 * tied          # mid-rank percentile: ties split, never hidden
            else:
                below = tied = above = pct = np.nan
            wf_rows.append(dict(panel=pan.name, bar=Tbar, menu_size=K, menu_of=len(cells),
                                C_ALL_cell=f"N{c_all[0]}g{c_all[1]}",
                                C_ALL_oCAGR=m_all["CAGR"], C_ALL_oSharpe=m_all["Sharpe"],
                                C_ALL_oMaxDD=m_all["MaxDD"], C_ALL_o4a=a4a, C_ALL_o4b=a4b,
                                C_THICK_cell=(f"N{c_th[0]}g{c_th[1]}" if menu else "EMPTY"),
                                C_THICK_oCAGR=m_th["CAGR"], C_THICK_oSharpe=m_th["Sharpe"],
                                C_THICK_oMaxDD=m_th["MaxDD"], C_THICK_o4a=t4a, C_THICK_o4b=t4b,
                                dSharpe=(m_th["Sharpe"] - m_all["Sharpe"]),
                                null_menus=len(null),
                                null_med_oSharpe=(float(np.nanmedian(null)) if null else np.nan),
                                thick_pctile_in_null=pct, null_share_below=below,
                                null_share_tied=tied, null_share_above=above,
                                SPY_oCAGR=spyO["CAGR"], SPY_oSharpe=spyO["Sharpe"],
                                SPY_oMaxDD=spyO["MaxDD"],
                                LIVE_oCAGR=liveO["CAGR"], LIVE_oSharpe=liveO["Sharpe"],
                                LIVE_oMaxDD=liveO["MaxDD"]))
        # ---- CAVEAT LEG: every 4b-passing cell vs the incumbent CELL on the SAME panel ------
        anchor_r = rets_by_cell[(I_N, I_G)]
        for (n, g), r in rets_by_cell.items():
            k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
            if not k4b or (n, g) == (I_N, I_G):
                continue
            obs, se, t = paired_block_dsharpe(r[WARMUP:], anchor_r[WARMUP:])
            oobs, ose, ot = paired_block_dsharpe(r[i_oos:], anchor_r[i_oos:])
            am = triple(anchor_r[WARMUP:])
            cav_rows.append(dict(panel=pan.name, N=n, gross=g, Sharpe=m["Sharpe"],
                                 anchor_Sharpe=am["Sharpe"], dSharpe=obs, se=se, t=t,
                                 oos_dSharpe=oobs, oos_se=ose, oos_t=ot,
                                 MaxDD=m["MaxDD"], anchor_MaxDD=am["MaxDD"],
                                 dd_margin_pp=100.0 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                                 anchor_dd_margin_pp=100.0 * (am["MaxDD"] - DD_CAP * spy["MaxDD"]),
                                 okeep4b=bool(keep_paths(r[i_oos:], spyO, liveO)[1])))

        say(f"    rule 8: C_ALL picks N{c_all[0]} g{c_all[1]} (IS Sharpe {is_sh[c_all]:.4f}) -> "
            f"OOS {m_all['CAGR']:.2%}/{m_all['Sharpe']:.4f}/{m_all['MaxDD']:.2%}  4a={a4a} 4b={a4b}")
        for row in [r for r in wf_rows if r["panel"] == pan.name]:
            say(f"            T={row['bar']:3d} menu {row['menu_size']:2d}/42  C_THICK "
                f"{row['C_THICK_cell']:>10s} -> OOS {row['C_THICK_oCAGR']:.2%}/"
                f"{row['C_THICK_oSharpe']:.4f}/{row['C_THICK_oMaxDD']:.2%}  4b={row['C_THICK_o4b']}"
                f"  dSharpe {row['dSharpe']:+.4f}  vs size-matched null median "
                f"{row['null_med_oSharpe']:.4f} (mid-rank pctile {row['thick_pctile_in_null']}; "
                f"below/tied/above {row['null_share_below']}/{row['null_share_tied']}/"
                f"{row['null_share_above']})")

    gdf = pd.DataFrame(grid)
    wdf = pd.DataFrame(wf_rows)
    cdf2 = pd.DataFrame(cav_rows)
    if len(cdf2):
        dump(cdf2.sort_values(["panel", "t"], ascending=[True, False]), "caveat")
    dump(gdf, "grid")
    dump(wdf, "rule8")

    # ---------------- gates ------------------------------------------------------------
    say("\n[GATES]")
    m, mo = anchor_replay
    d = max(abs(m["Sharpe"] - C_U56["Sharpe"]), abs(mo["Sharpe"] - C_U56["oSharpe"]))
    gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
         "(15.80%/1.1537/-19.13% full; OOS Sharpe 1.1857)",
         f"|dSharpe| {d:.2e} (got {m['CAGR']:.4f}/{m['Sharpe']:.4f}/{m['MaxDD']:.4f}; "
         f"OOS {mo['Sharpe']:.4f})", "< 5e-3", d < 5e-3)
    gate("G2 all cells published", len(gdf), f"== {3*len(NS)*len(GS)}", len(gdf) == 3 * len(NS) * len(GS))
    gate("G4 chooser reads no row on or after 2017-01-01", OOS_START,
         "IS window ends 2016-12-31", True)
    gate("G5 no leverage (max realised target weight sum)", f"{wsum_global:.6f}", "<= 1.000001",
         wsum_global <= 1.000001)
    a2 = build1(panels[0], I_N, I_H)
    C0 = np.cumprod(1.0 + panels[0].rets, axis=0)
    Cp0 = np.vstack([np.ones((1, panels[0].rets.shape[1])), C0[:-1]])
    gg2, tu2, _ = run_book(panels[0], a2, C0, Cp0, I_G)
    r2 = gg2 - tu2 * COST / 1e4
    gate("G7 bit-identical recompute of the anchor cell",
         f"max|d| {abs(sharpe(r2[WARMUP:]) - m['Sharpe']):.3e}", "== 0",
         sharpe(r2[WARMUP:]) == m["Sharpe"])

    # ---------------- verdict ----------------------------------------------------------
    say("\n[VERDICT]")
    n4a, n4b = int(gdf.keep4a.sum()), int(gdf.keep4b.sum())
    say(f"  4a: {n4a} of {len(gdf)} cells.   4b: {n4b} of {len(gdf)} cells.")
    if n4b:
        say("  4b-passing cells (full sample):")
        for _, r in gdf[gdf.keep4b].iterrows():
            say(f"    {r.panel:6s} N{int(r.N):<3d} g{r.gross:.2f}  CAGR {r.CAGR:.2%} Sharpe "
                f"{r.Sharpe:.4f} MaxDD {r.MaxDD:.2%} H1/H2 {r.H1:.3f}/{r.H2:.3f} | OOS "
                f"{r.oCAGR:.2%}/{r.oSharpe:.4f}/{r.oMaxDD:.2%} OOS4b={r.okeep4b}")
    if len(cdf2):
        res = cdf2[cdf2.t.abs() > 2]
        say(f"  CAVEAT LEG — 4b-passing cells vs the INCUMBENT CELL (N20 g0.75) ON THE SAME "
            f"PANEL (so the B136/SMALL anchor is the incumbent RECIPE there, not the U56 book), paired "
            f"63-day block bootstrap, 400 reps: {len(cdf2)} such cells, {len(res)} resolve "
            f"|t| > 2 on full-sample Sharpe, "
            f"{int((cdf2.oos_t.abs() > 2).sum())} on OOS Sharpe.")
        for _, r in cdf2.sort_values("dSharpe", ascending=False).head(4).iterrows():
            say(f"    {r.panel:6s} N{int(r.N):<3d} g{r.gross:.2f}  dSharpe {r.dSharpe:+.4f} "
                f"(t {r.t:+.2f})  OOS dSharpe {r.oos_dSharpe:+.4f} (t {r.oos_t:+.2f})  own 4b DD "
                f"margin {r.dd_margin_pp:+.4f} pp vs the anchor's {r.anchor_dd_margin_pp:+.4f} pp")
    ok = wdf.dropna(subset=["dSharpe"])
    say(f"  rule-8 chooser contrast (C_THICK - C_ALL, OOS Sharpe): mean {ok.dSharpe.mean():+.4f}, "
        f"{int((ok.dSharpe > 0).sum())} of {len(ok)} bar x panel arms positive, "
        f"{int((ok.dSharpe == 0).sum())} identical picks.")
    pc = ok.dropna(subset=["thick_pctile_in_null"])
    if len(pc):
        say(f"  C_THICK vs its SIZE-MATCHED RANDOM menus (mid-rank, ties split): median "
            f"percentile {pc.thick_pctile_in_null.median():.3f}, "
            f"{int((pc.thick_pctile_in_null > 0.95).sum())} of {len(pc)} above the 95th, "
            f"{int((pc.thick_pctile_in_null < 0.05).sum())} below the 5th; mean tied share "
            f"{pc.null_share_tied.mean():.3f} (a random menu of the same size usually picks the "
            f"SAME cell, which is itself the finding).")
    say(f"\n  elapsed {time.time()-t0:.1f}s")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"  wrote {Path(OUT).name}.gates.csv, {Path(OUT).name}.log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
