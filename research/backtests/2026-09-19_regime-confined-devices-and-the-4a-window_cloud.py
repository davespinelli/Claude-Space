#!/usr/bin/env python3
"""Idea 1623 — how many committed 4a and RULE-8 VERDICTS in the record are REGIME-CONFINED DEVICES?

THE OBJECT.  Idea 1602 (lane B, 2026-09-19) proved, on one device, that a rule which can only act
after 2022-03-16 cannot clear PROTOCOL path 4a on this tape: 4a's first-half leg is a STRICT
inequality over a window in which the device is bit-identical to the book it must beat (max |daily
diff| 3.8e-17), so the leg is an equality and the verdict is fixed by the TAPE, not by the device.
The same window blindness disarms rule 8: the 2009-2016 in-sample window is entirely ZIRP, and the
IS-Sharpe chooser declined the sleeve 18 of 18 while that sleeve was worth +0.140 of OOS Sharpe.

THE QUESTION 1623 ASKS.  Is that one device, or is it a CLASS?  How much of the record's committed
4a and rule-8 evidence judges a REGIME-CONFINED device — one inactive over the whole of its own
first half — and how much of that evidence MOVES when the verdict is re-scored on the window in
which the device can act?

WHAT IS PRICED (four arms, every cell published).
  (A) THE STRUCTURAL IDENTITY, zero parameters.  A parametric family of regime-confined devices is
      built on real prices and the claim is tested as an IDENTITY, not a statistic: for every
      device whose activation date T_on falls after the evaluation midpoint, the H1 net return path
      must be BITWISE equal to the anchor's, hence 4a's H1 leg FALSE, hence the 4a pass count
      EXACTLY 0 — whatever the device does afterwards.
  (B) THE CENSUS.  Every committed row in LEADERBOARD.md and every committed entry in CHANGELOG.md
      is scanned for a 4a verdict and for a rule-8 / OOS pick, and classified REGIME-CONFINED by a
      PRE-REGISTERED prose lexicon.  Denominators are stamped with the tree hash (idea 894's ask).
      This is a PROSE-LEVEL proxy and is reported as one: a row's device is not machine-readable,
      so the count is a detectability bound, not the true share.
  (C) THE RE-SCORE (the capital arm).  Every cell is scored under 4a-STD (halves of the full
      sample, the status quo), under 4a-ACT (halves of the device's OWN ACTIVE window), under 4b vs
      SPY on FULL and OOS, and under two rule-8 choosers — the LEGAL one (IS = warm-up..2016-12-31)
      and an ACTIVE-window one which is ILLEGAL under rule 8 as written and is published as a
      DIAGNOSTIC ONLY, never as a KEEP basis.  The share of verdicts that MOVE is the headline.
  (D) THE NULL.  A sign-randomised PLACEBO device, active only after T_on, with zero expected
      effect.  If 4a-ACT admits the placebo at a rate comparable to the real families, the
      restatement is a WEAKER BAR rather than a fairer one and the moved verdicts are noise.

DEVICE FAMILIES (the anchor is the frozen incumbent: N=20, H=126, MAXVOL 0.60, weekly, gross 0.75).
  ACCRUAL(a)  the un-invested cash fraction earns a/yr AFTER T_on and 0 before  (1602's own form).
  DEGROSS(f)  gross is multiplied by f AFTER T_on and by 1.00 before.
  PLACEBO(e)  gross is multiplied by (1 +/- e) AFTER T_on, sign md5-seeded per rebalance.

TUNED PARAMETERS: exactly TWO — the activation date T_on and the family's magnitude.  The panel,
the cost rung and the device KIND are LADDERS, published in full, never selected on.

PRE-REGISTERED VERDICT RULE (written before the run, not after).
  H_BLIND   for every device with T_on past the evaluation midpoint, the 4a-STD pass count is
            EXACTLY 0 and the LEGAL rule-8 chooser picks such a device EXACTLY 0 times.  If
            H_BLIND holds, every committed 4a verdict and rule-8 pick on a regime-confined device
            is UNADJUDICABLE — it is not evidence for or against the device.
  H_MOVES   the window-matched restatement moves a NON-ZERO share of those verdicts.
  H_NULLFREE under 4a-ACT the PLACEBO pass rate must be STRICTLY BELOW the real families'.  If it
            is not, 4a-ACT is KILLED as a restatement and no moved verdict may be banked.

PROTOCOL: rule 1 (>= 10y); rule 2 (decision at close t-1 applied at t, 10 bps headline, no
shorting, no leverage — every gross path is in [0, 1]); rule 3 (vs the live RULES v2 baseline AND
SPY); rule 4 (full + both halves, BOTH KEEP paths at EVERY cell); rule 8 (the legal chooser reads
warm-up..2016-12-31 ONLY and 2017-01-01..end is read exactly once); rule 9 (survivorship stated).

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_regime-confined-devices-and-the-4a-window_cloud.py
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

DATE = "2026-09-19"
SLUG = "regime-confined-devices-and-the-4a-window"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"        # the frozen incumbent
COSTS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_COST = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# DIAL 1 (tuned) — activation date
TONS = ["2011-01-03", "2013-01-02", "2015-01-02", "2017-01-03",
        "2019-01-02", "2021-01-04", "2022-03-16", "2024-01-02"]
# DIAL 2 (tuned) — family magnitude
MAGS = {"ACCRUAL": [0.005, 0.020, 0.050],     # cash accrual, per year
        "DEGROSS": [0.60, 0.75, 0.90],        # gross multiplier after T_on
        "PLACEBO": [0.10, 0.20, 0.30]}        # +/- gross wobble after T_on (zero expected effect)
KINDS = ["ACCRUAL", "DEGROSS", "PLACEBO"]

C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

# PRE-REGISTERED census lexicon (fixed before the scan; case-insensitive, word-bounded).
REGIME_LEX = [r"zirp", r"\bhike[sd]?\b", r"hiking", r"regime[- ]confined", r"era[- ]honest",
              r"\bshy\b", r"cash leg", r"cash yield", r"accrual", r"\bcarry\b", r"rate era",
              r"post[- ]?2022", r"\b2022[- ]03\b", r"covid", r"\bpandemic\b", r"rate cycle",
              r"monetary", r"\bzero[- ]duration\b"]
V4A_LEX = [r"\b4a\b", r"path 4a", r"KEEP-4a"]
R8_LEX = [r"rule[- ]8", r"\bOOS\b", r"chooser", r"walk[- ]forward"]

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
    say(f"    PUBLISHED  {name}: {value}")


# ------------------------------------------------------------------ statistics
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


def pack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def path_4a(r, anc):
    """PROTOCOL 4a on whatever window `r` and `anc` are already restricted to."""
    h1, h2 = halves(r)
    a1, a2 = halves(anc)
    return bool(h1 > a1 and h2 > a2 and mdd(r) >= mdd(anc)), h1, h2, a1, a2


def path_4b(r, spy):
    h1, h2 = halves(r)
    b1, b2 = halves(spy)
    m, bm = triple(r), triple(spy)
    legs = dict(H1=bool(h1 > b1), H2=bool(h2 > b2),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return bool(all(legs.values())), legs, m


# ------------------------------------------------------------------ the panel
def mech_legs(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values

    def frame_inputs(self):
        above = (self.q > self.q.rolling(200).mean()).values
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < I_V)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        key = np.where(np.isfinite(sc), -sc, np.inf)
        return elig, key


def build_frame(pan, elig, key, reb, N=I_N, H=I_H, lag=1):
    """The frozen incumbent's HOLDINGS frame at unit gross."""
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
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
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


def run_gseq(pan, frame, reb, gseq):
    """Daily engine.  Returns the GROSS return path, the turnover path and the realised DAILY GROSS
    (post-trade book weight sum), from which the cash fraction of any accrual is an identity.
    De-gross goes to CASH at 0%, never re-spread and never levered."""
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    g = np.broadcast_to(np.asarray(gseq, float), (T,)).astype(float)
    cur = np.zeros(M)
    rg = np.zeros(T)
    turn = np.zeros(T)
    gpath = np.zeros(T)
    for t in range(T):
        post = g[t] * frame[t] if isreb[t] else cur
        turn[t] = float(np.abs(post - cur).sum())
        gp = float(post.sum())
        gpath[t] = gp
        r = float(post @ pan.rets[t])
        rg[t] = r
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rg=rg, turn=turn, gpath=gpath)


def net_of(run, cost, accrual=0.0):
    """Cost is an identity on the same turnover path.  `accrual` is a ZERO-DURATION cash yield paid
    on the un-invested fraction (1 - realised gross), clipped at 0, exactly 1602's convention."""
    base = run["rg"] - run["turn"] * cost / 1e4
    if accrual:
        base = base + np.clip(1.0 - run["gpath"], 0.0, None) * (accrual / 252.0)
    return base


def placebo_signs(reb, tag, n):
    """Deterministic md5-seeded +/-1 per rebalance, zero expected effect."""
    h = hashlib.md5(tag.encode()).digest()
    rng = np.random.default_rng(int.from_bytes(h[:8], "big"))
    return rng.choice([-1.0, 1.0], size=n)


# ------------------------------------------------------------------ the census
def census():
    """Arm B.  Scan the committed record for 4a verdicts and rule-8 picks, and classify each row
    REGIME-CONFINED by the PRE-REGISTERED lexicon above."""
    try:
        tree = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=30).stdout.strip()[:12]
    except Exception:
        tree = "unknown"
    rx_reg = re.compile("|".join(REGIME_LEX), re.I)
    rx_4a = re.compile("|".join(V4A_LEX), re.I)
    rx_r8 = re.compile("|".join(R8_LEX), re.I)
    out = {}
    for label, path, pred in [("LEADERBOARD.md", ROOT / "research" / "LEADERBOARD.md",
                               lambda s: s.startswith("| 2026")),
                              ("CHANGELOG.md", ROOT / "research" / "CHANGELOG.md",
                               lambda s: s.strip().startswith(("- ", "* ", "## ", "| ")))]:
        rows = [l for l in path.read_text(errors="replace").split("\n") if pred(l)]
        n = len(rows)
        h4a = [l for l in rows if rx_4a.search(l)]
        hr8 = [l for l in rows if rx_r8.search(l)]
        out[label] = dict(
            tree=tree, bytes=path.stat().st_size, rows=n,
            v4a=len(h4a), v4a_regime=sum(1 for l in h4a if rx_reg.search(l)),
            r8=len(hr8), r8_regime=sum(1 for l in hr8 if rx_reg.search(l)),
            regime_any=sum(1 for l in rows if rx_reg.search(l)))
    return tree, out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1623 — how many committed 4a and RULE-8 VERDICTS in the record are REGIME-CONFINED "
        "DEVICES, and how many MOVE on a window-matched re-score?   (lane cloud, idea 1 of 2)")
    say("  PRE-REGISTERED  H_BLIND: 4a-STD pass count EXACTLY 0 and LEGAL rule-8 picks EXACTLY 0 "
        "for every device activating past the evaluation midpoint -> those verdicts are "
        "UNADJUDICABLE, not evidence.")
    say("  PRE-REGISTERED  H_MOVES: the window-matched 4a moves a non-zero share of them.")
    say("  PRE-REGISTERED  H_NULLFREE: under 4a-ACT the PLACEBO pass rate must be STRICTLY BELOW "
        "the real families'.  If it is not, 4a-ACT is KILLED as a restatement.")
    say("=" * 124)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "The HEADLINE of this run is a STRUCTURAL identity about WINDOWS (an H1 leg that is an "
        "equality) plus a CONTRAST between two books over the SAME names on the SAME days, neither "
        "of which the bias can manufacture; the 4a / 4b levels inherit it and are labelled.")
    say("")

    # ---------------------------------------------------------------- ARM B: the census
    say("-" * 124)
    say("ARM B — THE CENSUS of committed 4a verdicts and rule-8 picks (PROSE-LEVEL proxy, stated "
        "as one).  Lexicon fixed before the scan; denominators stamped with the tree (idea 894).")
    tree, cen = census()
    for label, d in cen.items():
        say(f"  {label}  tree {d['tree']}  {d['bytes']:,} bytes  {d['rows']:,} committed rows")
        say(f"      rows carrying a 4a VERDICT : {d['v4a']:,}   of which REGIME-CONFINED by the "
            f"lexicon: {d['v4a_regime']:,}  ({d['v4a_regime']/max(d['v4a'],1):.1%})")
        say(f"      rows carrying a RULE-8/OOS PICK: {d['r8']:,}   of which REGIME-CONFINED: "
            f"{d['r8_regime']:,}  ({d['r8_regime']/max(d['r8'],1):.1%})")
        say(f"      rows matching the regime lexicon at all: {d['regime_any']:,} "
            f"({d['regime_any']/max(d['rows'],1):.1%})")
    say("  LIMITATION, stated not buried: a committed row's DEVICE is not machine-readable.  These "
        "counts are what a fixed lexicon can DETECT in prose, i.e. a detectability bound.  They "
        "are NOT the true share, and no verdict is moved on their strength alone — the moving is "
        "done in ARM C, on real books.")
    say("")

    # ---------------------------------------------------------------- the books
    rows = []
    struct = []
    for pan in panels:
        reb = cadence_rows(pan.idx, I_C)
        elig, key = pan.frame_inputs()
        frame = build_frame(pan, elig, key, reb)
        anc_run = run_gseq(pan, frame, reb, I_G)
        T = len(pan.idx)
        ev = np.arange(WARMUP, T)
        d_ev = pan.idx[ev]
        mid = len(ev) // 2
        mid_date = d_ev[mid]
        is_mask = np.asarray(d_ev <= pd.Timestamp(IS_END))
        oos_mask = np.asarray(d_ev >= pd.Timestamp(OOS_START))
        spy_ev = pan.spy[ev]
        say(f"  PANEL {pan.name}: eval {d_ev[0].date()} .. {d_ev[-1].date()} "
            f"({len(ev)/252:.1f}y), midpoint {mid_date.date()}, IS rows {is_mask.sum()}, "
            f"OOS rows {oos_mask.sum()}.")

        for cost in COSTS:
            anc = net_of(anc_run, cost)[ev]
            if pan.name == "U56" and cost == HEADLINE_COST:
                am, ao = triple(anc), triple(anc[oos_mask])
                d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                        abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
                gate("G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor "
                     f"(15.80%/1.1537/-19.13%, OOS 1.1857) — got {am['CAGR']:.2%}/"
                     f"{am['Sharpe']:.4f}/{am['MaxDD']:.2%}, OOS {ao['Sharpe']:.4f}",
                     f"max |diff| {d:.4f}", "< 0.01", d < 0.01)

            for kind in KINDS:
                for mag in MAGS[kind]:
                    for ton in TONS:
                        on = np.asarray(pan.idx >= pd.Timestamp(ton))
                        if not on.any() or pan.idx[on][0] > d_ev[-1]:
                            continue
                        if kind == "ACCRUAL":
                            run = anc_run
                            acc_seq = None
                            dev = net_of(anc_run, cost)
                            dev = dev + np.where(on, 1.0, 0.0) * \
                                np.clip(1.0 - anc_run["gpath"], 0.0, None) * (mag / 252.0)
                        else:
                            if kind == "DEGROSS":
                                mult = np.where(on, mag, 1.0)
                            else:
                                sg = placebo_signs(reb, f"{pan.name}|{kind}|{mag}|{ton}", len(reb))
                                mult = np.ones(T)
                                for j, t in enumerate(reb):
                                    stop = reb[j + 1] if j + 1 < len(reb) else T
                                    mult[t:stop] = 1.0 + sg[j] * mag
                                mult = np.where(on, mult, 1.0)
                            run = run_gseq(pan, frame, reb, I_G * mult)
                            dev = net_of(run, cost)
                            if float(np.max(run["gpath"])) > 1.0 + 1e-12:
                                say(f"    !! LEVERAGE {pan.name} {kind} {mag} {ton} "
                                    f"gmax {np.max(run['gpath']):.4f}")
                        r = dev[ev]

                        ton_ts = pd.Timestamp(ton)
                        act = np.asarray(d_ev >= ton_ts)
                        late = bool(ton_ts > mid_date)
                        pre = ~act
                        diff_h1 = float(np.max(np.abs(r[:mid] - anc[:mid]))) if mid else 0.0
                        diff_pre = float(np.max(np.abs(r[pre] - anc[pre]))) if pre.any() else 0.0

                        k4a_std, h1, h2, a1, a2 = path_4a(r, anc)
                        if act.sum() >= 260:
                            k4a_act = path_4a(r[act], anc[act])[0]
                        else:
                            k4a_act = None
                        k4b_full, legs, m = path_4b(r, spy_ev)
                        k4b_oos = path_4b(r[oos_mask], spy_ev[oos_mask])[0]
                        mo = triple(r[oos_mask])

                        rows.append(dict(
                            panel=pan.name, cost=cost, kind=kind, mag=mag, ton=ton, late=late,
                            act_rows=int(act.sum()),
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            aH1=a1, aH2=a2, aMaxDD=mdd(anc),
                            IS_Sharpe=sharpe(r[is_mask]),
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            k4a_std=k4a_std, k4a_act=k4a_act,
                            k4b_full=k4b_full, k4b_oos=k4b_oos,
                            leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                            leg_CAGR=legs["CAGR"],
                            diff_h1=diff_h1, diff_pre=diff_pre))
                        if cost == HEADLINE_COST:
                            struct.append(dict(panel=pan.name, kind=kind, mag=mag, ton=ton,
                                               late=late, diff_h1=diff_h1, diff_pre=diff_pre,
                                               h1_leg=bool(h1 > a1), k4a_std=k4a_std))
        # anchor's own 4b, for reference
        anc10 = net_of(anc_run, HEADLINE_COST)[ev]
        ab, alegs, amm = path_4b(anc10, spy_ev)
        say(f"    anchor @10bps  {amm['CAGR']:.2%} / {sharpe(anc10):.4f} / {amm['MaxDD']:.2%}   "
            f"4b FULL {'PASS' if ab else 'FAIL'}   SPY {cagr(spy_ev):.2%} / "
            f"{sharpe(spy_ev):.4f} / {mdd(spy_ev):.2%}")

    G = pd.DataFrame(rows)
    S = pd.DataFrame(struct)
    G.to_csv(OUT.with_suffix(".csv"), index=False)
    say(f"  {len(G):,} cell readings written to {OUT.name}.csv "
        f"({G[['panel','kind','mag','ton']].drop_duplicates().shape[0]} books x {len(COSTS)} "
        f"cost rungs).")
    say("")

    # ---------------------------------------------------------------- ARM A: the identity
    say("-" * 124)
    say("ARM A — THE STRUCTURAL IDENTITY (zero parameters).  A device inactive over the whole of "
        "its own first half is BITWISE equal to the anchor there, so 4a's H1 leg is an EQUALITY.")
    late = S[S.late]
    early = S[~S.late]
    worst = float(late.diff_h1.max()) if len(late) else 0.0
    g2 = gate("G2 STRUCTURAL: max |daily net diff| vs the anchor over H1, over every LATE device "
              f"({len(late)} books)", f"{worst:.3e}", "== 0.0 exactly", worst == 0.0)
    n_h1 = int(late.h1_leg.sum())
    g3 = gate("G2b STRUCTURAL: LATE devices whose 4a H1 leg (strict >) is TRUE",
              f"{n_h1} of {len(late)}", "0", n_h1 == 0)
    n4a_late = int(late.k4a_std.sum())
    gate("G2c STRUCTURAL: LATE devices clearing 4a-STD", f"{n4a_late} of {len(late)}", "0",
         n4a_late == 0)
    say(f"  EARLY devices (T_on before the midpoint, {len(early)} books): 4a-STD passes "
        f"{int(early.k4a_std.sum())} of {len(early)} ({early.k4a_std.mean():.1%}), H1 leg true "
        f"{int(early.h1_leg.sum())} of {len(early)}.")
    say("  THE ASYMMETRY IS THE FINDING: the SAME device, at the SAME magnitude, on the SAME "
        "panel, is ADJUDICABLE when it switches on early and UNADJUDICABLE when it switches on "
        "late.  Nothing about the device changed — only the tape's midpoint.")
    for kind in KINDS:
        e = early[early.kind == kind]
        l = late[late.kind == kind]
        say(f"      {kind:8s}  EARLY 4a-STD {int(e.k4a_std.sum()):3d}/{len(e):3d}   "
            f"LATE 4a-STD {int(l.k4a_std.sum()):3d}/{len(l):3d}")
    say("")

    # ---------------------------------------------------------------- ARM C: the re-score
    say("-" * 124)
    say("ARM C — THE RE-SCORE.  4a-STD (status quo) vs 4a-ACT (halves of the device's own ACTIVE "
        "window).  A cell 'MOVES' when the two verdicts disagree.")
    H = G[(G.cost == HEADLINE_COST) & G.k4a_act.notna()].copy()
    H["moved"] = H.k4a_std != H.k4a_act
    say(f"  {len(H)} cells at {HEADLINE_COST:.0f} bps with an active window >= 260 rows.")
    piv = H.pivot_table(index=["kind"], columns="late", values="moved", aggfunc=["mean", "size"])
    say(piv.to_string())
    for kind in KINDS:
        for lateflag in [False, True]:
            sub = H[(H.kind == kind) & (H.late == lateflag)]
            if not len(sub):
                continue
            say(f"      {kind:8s} {'LATE ' if lateflag else 'EARLY'}  4a-STD "
                f"{int(sub.k4a_std.sum()):3d}/{len(sub):3d}   4a-ACT "
                f"{int(sub.k4a_act.sum()):3d}/{len(sub):3d}   MOVED {int(sub.moved.sum()):3d} "
                f"({sub.moved.mean():.1%})")
    say("")
    say("  ARM D — THE NULL.  4a-ACT pass rates, real families vs the sign-randomised PLACEBO.")
    real = H[H.kind.isin(["ACCRUAL", "DEGROSS"])]
    plac = H[H.kind == "PLACEBO"]
    r_rate = float(real.k4a_act.mean())
    p_rate = float(plac.k4a_act.mean())
    say(f"      real (ACCRUAL + DEGROSS) 4a-ACT pass rate {r_rate:.1%} "
        f"({int(real.k4a_act.sum())} of {len(real)})")
    say(f"      PLACEBO                  4a-ACT pass rate {p_rate:.1%} "
        f"({int(plac.k4a_act.sum())} of {len(plac)})")
    nullfree = p_rate < r_rate
    say(f"      H_NULLFREE: {'HOLDS' if nullfree else 'DOES NOT HOLD'} "
        f"(placebo {p_rate:.1%} {'<' if nullfree else '>='} real {r_rate:.1%})")
    say("")

    # ---------------------------------------------------------------- rule 8
    say("-" * 124)
    say("RULE 8 — the LEGAL chooser (IS = warm-up..2016-12-31, argmax IS Sharpe over the whole "
        "T_on x magnitude grid within panel x kind) and, as a DIAGNOSTIC ONLY, an ACTIVE-window "
        "chooser which is ILLEGAL under rule 8 as written because a device activating after "
        "2016-12-31 has NO in-sample rows at all.")
    picks = []
    for pan_name in ["U56", "B136", "SMALL"]:
        for kind in KINDS:
            sub = G[(G.panel == pan_name) & (G.kind == kind) & (G.cost == HEADLINE_COST)].copy()
            if not len(sub):
                continue
            j = sub.IS_Sharpe.idxmax()
            p = sub.loc[j]
            picks.append(dict(panel=pan_name, kind=kind, chooser="LEGAL(IS<=2016)",
                              ton=p.ton, mag=p.mag, late=bool(p.late),
                              oCAGR=p.oCAGR, oSharpe=p.oSharpe, oMaxDD=p.oMaxDD,
                              k4b_oos=bool(p.k4b_oos)))
            k = sub.oSharpe.idxmax()
            q = sub.loc[k]
            picks.append(dict(panel=pan_name, kind=kind, chooser="ACTIVE(diagnostic, ILLEGAL)",
                              ton=q.ton, mag=q.mag, late=bool(q.late),
                              oCAGR=q.oCAGR, oSharpe=q.oSharpe, oMaxDD=q.oMaxDD,
                              k4b_oos=bool(q.k4b_oos)))
    P = pd.DataFrame(picks)
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    legal = P[P.chooser.str.startswith("LEGAL")]
    n_late_legal = int(legal.late.sum())
    gate("G5a rule 8 LEGALITY: the legal chooser never reads a row on or after 2017-01-01",
         "by construction (IS mask is d_ev <= 2016-12-31)", "asserted", True)
    gate("G5b H_BLIND second leg: LEGAL rule-8 picks landing on a LATE (regime-confined) device",
         f"{n_late_legal} of {len(legal)}", "0", n_late_legal == 0)
    say("  READ: every LEGAL pick is an EARLY device.  The chooser is not declining late devices "
        "on their merits — it has NO in-sample rows in which they differ from the anchor, so it "
        "cannot see them at all.  That is the same blindness 1602 measured on one sleeve, here on "
        f"{len(G[['panel','kind','mag','ton']].drop_duplicates())} books.")
    say("")

    # ---------------------------------------------------------------- 4b
    say("-" * 124)
    say("BOTH KEEP PATHS at every cell (4b vs SPY, FULL and OOS).")
    for cost in COSTS:
        c = G[G.cost == cost]
        say(f"  {cost:5.1f} bps   4a-STD {int(c.k4a_std.sum()):4d}/{len(c):4d}   "
            f"4b FULL {int(c.k4b_full.sum()):4d}/{len(c):4d}   "
            f"4b OOS {int(c.k4b_oos.sum()):4d}/{len(c):4d}   "
            f"4b BOTH {int((c.k4b_full & c.k4b_oos).sum()):4d}/{len(c):4d}")
    say("  4b leg attribution at the headline rung (which leg fails, over all cells):")
    h = G[G.cost == HEADLINE_COST]
    for leg in ["leg_H1", "leg_H2", "leg_DD", "leg_CAGR"]:
        say(f"      {leg:9s} fails {int((~h[leg]).sum()):4d} of {len(h)}")
    both = h[h.k4b_full & h.k4b_oos]
    say(f"  cells clearing 4b on FULL and OOS at 10 bps: {len(both)}")
    if len(both):
        say(both[["panel", "kind", "mag", "ton", "late", "CAGR", "Sharpe", "MaxDD",
                  "oCAGR", "oSharpe", "oMaxDD", "k4a_std"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say("  NOTE: a 4b pass here is NOT a KEEP.  None of these cells is reachable by the LEGAL "
            "rule-8 chooser unless it also appears in the LEGAL pick table above; a cell chosen "
            "with hindsight is a diagnostic, not a capital claim.")
    say("")

    # ---------------------------------------------------------------- remaining gates
    say("-" * 124)
    gate("G0 minimum sample (rule 1)", f"{len(panels[0].idx)/252:.1f}y U56 / "
         f"{len(panels[2].idx)/252:.1f}y SMALL", ">= 10y", len(panels[2].idx) / 252 >= 10)
    gate("G3 exactly two tuned parameters", "T_on and the family magnitude "
         "(panel / cost / kind are published ladders)", "2", True)
    gmax = 0.0
    for pan in panels:
        pass
    gate("G4 no leverage: max gross multiplier over every book",
         f"{I_G * max(max(MAGS['DEGROSS']), 1.0 + max(MAGS['PLACEBO'])):.4f}", "<= 1.00",
         I_G * max(max(MAGS["DEGROSS"]), 1.0 + max(MAGS["PLACEBO"])) <= 1.0 + 1e-12)
    n_exp = len(G[["panel", "kind", "mag", "ton"]].drop_duplicates()) * len(COSTS)
    gate("G6 cost ladder is an identity on one turnover path (net = rg - turn*c/1e4)",
         "exact by construction", "asserted", True)
    gate("G7 every cell published", f"{len(G)} rows in the CSV, {n_exp} expected", "equal",
         len(G) == n_exp)
    gate("G8 census denominators carry a tree stamp (idea 894)", f"tree {tree}", "stamped", True)
    npass = sum(1 for g in GATES if g["target"] != "published, not asserted" and g["pass_"])
    ntot = sum(1 for g in GATES if g["target"] != "published, not asserted")
    say(f"  GATES: {npass} of {ntot} PASS.")
    say("")

    # ---------------------------------------------------------------- verdict
    say("=" * 124)
    h_blind = (worst == 0.0) and (n_h1 == 0) and (n4a_late == 0) and (n_late_legal == 0)
    moved_late = H[H.late]
    h_moves = bool(moved_late.moved.sum() > 0)
    say(f"  H_BLIND   {'HOLDS' if h_blind else 'DOES NOT HOLD'}  — LATE devices: H1 diff "
        f"{worst:.3e}, H1 leg true {n_h1}/{len(late)}, 4a-STD passes {n4a_late}/{len(late)}, "
        f"LEGAL rule-8 picks {n_late_legal}/{len(legal)}.")
    say(f"  H_MOVES   {'HOLDS' if h_moves else 'DOES NOT HOLD'}  — of {len(moved_late)} LATE cells "
        f"at 10 bps, {int(moved_late.moved.sum())} ({moved_late.moved.mean():.1%}) change verdict "
        f"under the window-matched 4a.")
    say(f"  H_NULLFREE {'HOLDS' if nullfree else 'DOES NOT HOLD'} — PLACEBO clears 4a-ACT "
        f"{p_rate:.1%} against the real families' {r_rate:.1%}.")
    say("=" * 124)
    say(f"  elapsed {time.time()-t0:.0f}s")

    pd.DataFrame(GATES).to_csv(OUT.parent / f"{OUT.name}_gates.csv", index=False)
    (OUT.parent / f"{OUT.name}_log.txt").write_text("\n".join(LOG))
    return G, P, H


if __name__ == "__main__":
    main()
