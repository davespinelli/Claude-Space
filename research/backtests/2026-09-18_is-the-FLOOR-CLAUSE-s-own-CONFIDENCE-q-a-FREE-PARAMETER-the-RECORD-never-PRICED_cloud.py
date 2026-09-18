#!/usr/bin/env python3
"""Idea 1114 (lane cloud, 2026-09-18): is the FLOOR CLAUSE's own CONFIDENCE q a FREE PARAMETER
the RECORD never PRICED?

THE PREMISE.  The record commits confidence levels all over the place -- 0.90 floors, 0.95 nulls,
a 0.90 non-certifying bar -- and idea 1110 found the floor clause retains 0.516 / 0.359 / 0.293 of
the record's CORE argmax content at q = 0.80 / 0.90 / 0.95 while 1102's committed tie sets never
consulted q at all.  Nothing in the record says which bar is the record's.  A number that changes
what gets adopted and that nobody has justified is a FREE PARAMETER, and this repo's own
PROTOCOL rule 7 says a free parameter has to be priced or dropped.

THE HOUSE PATTERN (see the 2026-09-18 lane-B and lane-C entries in CHANGELOG.md): a
record-bookkeeping question is run with a CAPITAL ARM, so the answer is a number about money and
not only a count of sentences.  Both arms are here and are labelled.

  CAPITAL ARM (the deliverable).  Read the floor clause as what it actually is operationally: a
  bar a candidate must clear before a chooser is allowed to MOVE THE BOOK off its incumbent
  rung.  Declare one q, apply it honestly, and read what it costs or earns.  A chooser sees the
  IN-SAMPLE window only.  For each rung r of a dial ladder it computes the IS Sharpe margin
  m(r) = S_IS(r) - S_IS(incumbent) and the sampling SD of that margin from a PAIRED MOVING-BLOCK
  BOOTSTRAP (block 21 days, B = 400 draws, shared draws across rungs, fixed seed).  It adopts the
  highest-IS-Sharpe rung whose margin clears z_q * SD, and otherwise STAYS AT THE INCUMBENT.
  Then 2017-2026 is read ONCE.  q = 0.50 is z = 0, i.e. "adopt anything that looks better" --
  the record's de facto habit and the control this run is really against.

  CENSUS ARM (reporting only, crude and labelled as such).  A lexical count over the committed
  record of lines that quote a confidence level, and of how many of those also contain any
  justification token at all.  It moves no gate and no verdict.

THE TWO DIALS (PROTOCOL rule 4: max two tuned parameters).
    DIAL 1  q in {0.50, 0.80, 0.90, 0.95, 0.99}  -- the declared confidence level.  0.50 = no bar.
    DIAL 2  CLAIM SET D in {N, GROSS, HOLD, ALL}  -- which ladder the chooser is allowed to move.
            N     : top-N in {10, 15, 20, 30, 40}          (incumbent 20)
            GROSS : gross in {0.50, 0.60, 0.75, 0.85, 1.00} (incumbent 0.60)
            HOLD  : min-hold H in {21, 63, 126, 252}        (incumbent 126)
            ALL   : the union -- the chooser may move any one of the three.

FROZEN, not touched: the composite and its three legs (21/252, 0/126, 0/63 percentile ranks,
equal-weighted), eligibility (above own 200d MA AND vol20 < 0.60), weekly decide-Friday cadence,
equal weight, 260-row warm-up, the 2017-01-01 IS/OOS split, PROTOCOL's 10 bps and t+1 fill.
Costs 25 / 50 bps and a t+2 fill are an ANNEX (reporting, never a verdict).

THE INCUMBENT is the record's single confirmed 4b candidate: U56, N = 20, H = 126, gross 0.60,
weekly.  Gate G2 checks this run reproduces idea 1286's committed row for it to 1e-4.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) q IS A REAL PARAMETER AND A HIGHER BAR PAYS -- mean OOS Sharpe rises monotonically-ish with
      q, and some q beats BOTH q = 0.50 and the frozen incumbent.  The record should declare it.
  (B) q IS A REAL PARAMETER AND THE BAR IS A TAX -- OOS falls as q rises; the record's habit of
      adopting on any positive margin is right and the floor clause should go.
  (C) q IS INERT -- the adopted rung is the same at every q because margins are far from the bar,
      so the number the record never justified never mattered.  Free parameter, zero price.
  (D) NOTHING BEATS STANDING STILL -- every q, including 0.50, loses OOS Sharpe against the
      frozen incumbent.  Then the answer is not a value of q but that the chooser itself is the
      mistake, and the record's real error is adopting at all.

SURVIVORSHIP (rule 9).  U56 (55 investables) and B135 are CURRENT-constituent lists; SMALL663 is
a current sub-$2B screen with the house `max_1d_move >= 1.0` filter applied FIRST.  Every
absolute level is an UPPER bound.  The quoted result is a WITHIN-grid difference -- chooser minus
frozen incumbent, and q minus q = 0.50, on the SAME panel, same names, same dates -- which is
first-order immune to that bias.

Deterministic (fixed seed), offline, no network.  Run: python3 <this file>
"""
import sys, time, json, re
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE = "2026-09-18"
SLUG = "is-the-FLOOR-CLAUSE-s-own-CONFIDENCE-q-a-FREE-PARAMETER-the-RECORD-never-PRICED"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_C = "W"
INC = dict(N=20, H=126, G=0.60)                   # the incumbent rung
LEGS = [(21, 252), (0, 126), (0, 63)]
LADDERS = {"N": [10, 15, 20, 30, 40],
           "GROSS": [0.50, 0.60, 0.75, 0.85, 1.00],
           "HOLD": [21, 63, 126, 252]}
CLAIMSETS = ["N", "GROSS", "HOLD", "ALL"]         # DIAL 2
QS = [0.50, 0.80, 0.90, 0.95, 0.99]               # DIAL 1
COSTS = [10.0, 25.0, 50.0]
DELAYS = [1, 2]
BLOCK, NBOOT, SEED = 21, 400, 20260918
_LOG, GATES = [], []


def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ---------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20: return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20: return np.nan
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r); h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                is_=stats(r[:o]), oos=stats(r[o:]), nis=o,
                is_h1=sharpe(r[:o][:o // 2]), is_h2=sharpe(r[:o][o // 2:]))


# ---------------------------------------------------------------- panel
class Panel:
    def __init__(self, name, px, invest):
        assert "SPY" not in invest, "G5: SPY must never be a constituent"
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.ispy = cols.index("SPY")
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, A_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, N, H):
    """The frozen book machinery at top-N with min-hold H, equal weight (gross applied later)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - 1, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held): held = held[pr[t, held]]
        keep = [int(c) for c in (held[(t - cur[held]) < H] if len(held) else held)]
        k = pan.key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        for c in keep: k[c] = np.inf
        need, take = N - len(keep), []
        for c in np.argsort(k, kind="stable"):
            if need <= 0 or not np.isfinite(k[int(c)]): break
            take.append(int(c)); need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep: new[c] = cur[c]
        for c in take: new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel): continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_raw(pan, Wt, gross, delay):
    if delay > 1:
        Wt = np.vstack([np.repeat(Wt[:1], delay - 1, axis=0), Wt[:-(delay - 1)]])
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M)); turn = np.zeros(T); curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1), turn


# ---------------------------------------------------------------- KEEP paths
def legs_4a(bk, live):
    return dict(H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ---------------------------------------------------------------- bootstrap bar
def block_draws(n, block, nboot, rng):
    """Moving-block bootstrap index matrix (nboot x n).  Shared across rungs so the margin is
    resampled PAIRED -- the same days for the candidate and the incumbent."""
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, max(n - block + 1, 1), size=(nboot, nb))
    off = np.arange(block)[None, None, :]
    return (starts[:, :, None] + off).reshape(nboot, -1)[:, :n]


def margin_sd(R_is, inc_col, draws):
    """SD of (Sharpe_rung - Sharpe_incumbent) across paired block-bootstrap draws.
    R_is: (n_is x n_rungs) IS daily net returns."""
    out = np.empty((draws.shape[0], R_is.shape[1]))
    for b in range(draws.shape[0]):
        X = R_is[draws[b]]
        v = X.std(axis=0, ddof=0)
        s = np.where(v > 0, X.mean(axis=0) * np.sqrt(252) / np.where(v > 0, v, 1.0), np.nan)
        out[b] = s - s[inc_col]
    return np.nanstd(out, axis=0, ddof=1)


# ---------------------------------------------------------------- census arm
CONF = re.compile(r"\b0\.(?:80|90|95|99)\b")
WHY = re.compile(r"\b(because|why|justif|rather than|chosen|declared in advance|pre-declared|"
                 r"pre-registered|reason)\b", re.I)


def census():
    """Crude LEXICAL census over the committed record. Reporting only -- moves no gate."""
    files = sorted(list((ROOT / "research").glob("*.md"))
                   + list((ROOT / "research" / "backtests").glob("*.md")))
    tot = withwhy = 0
    per = {}
    for f in files:
        n = w = 0
        for line in f.read_text(errors="ignore").split("\n"):
            if CONF.search(line):
                n += 1
                if WHY.search(line): w += 1
        if n: per[f.name] = (n, w)
        tot += n; withwhy += w
    return tot, withwhy, len(per), per


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    say(f"# {DATE} idea 1114 lane cloud -- {SLUG}")
    say(f"# DIAL 1 q = {QS} (0.50 = NO BAR, the record's de facto habit)")
    say(f"# DIAL 2 CLAIM SET = {CLAIMSETS}; ladders {LADDERS}")
    say(f"# incumbent rung {INC}; bar = z_q * SD from a PAIRED moving-block bootstrap "
        f"(block {BLOCK}, B {NBOOT}, seed {SEED})")
    say(f"# PROTOCOL cell = 10 bps, t+1.  ANNEX: costs {COSTS}, delays {['t+%d' % d for d in DELAYS]}")
    say("")

    panels = []
    panels.append(Panel("U56", *(lambda p: (p, [c for c in p.columns if c != "SPY"]))(
        load_universe())))
    pxb = load_universe(broad=True)
    panels.append(Panel(f"B{len([c for c in pxb.columns if c != 'SPY'])}", pxb,
                        [c for c in pxb.columns if c != "SPY"]))
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    invs = [c for c in pxs.columns if c != "SPY" and c not in bad]
    say(f"# SMALL: house filter drops {len([c for c in pxs.columns if c in bad])} names on "
        f"max_1d_move >= 1.0; {len(invs)} kept")
    panels.append(Panel(f"SMALL{len(invs)}", pxs, invs))
    for p in panels:
        say(f"# panel {p.name}: {len(p.invest)} investables, {len(p.idx)} rows "
            f"{p.idx[0].date()}..{p.idx[-1].date()} (scored from {p.idx[WARMUP].date()}), "
            f"{len(p.reb)} rebalances")
    say("")

    # ---- the rung universe: (label, N, H, gross), incumbent first
    rungs = [("INC", INC["N"], INC["H"], INC["G"])]
    for n in LADDERS["N"]:
        if n != INC["N"]: rungs.append((f"N={n}", n, INC["H"], INC["G"]))
    for g in LADDERS["GROSS"]:
        if abs(g - INC["G"]) > 1e-12: rungs.append((f"G={g:.2f}", INC["N"], INC["H"], g))
    for h in LADDERS["HOLD"]:
        if h != INC["H"]: rungs.append((f"H={h}", INC["N"], h, INC["G"]))
    LAB = [r[0] for r in rungs]
    MEMBER = {"N": [i for i, l in enumerate(LAB) if l == "INC" or l.startswith("N=")],
              "GROSS": [i for i, l in enumerate(LAB) if l == "INC" or l.startswith("G=")],
              "HOLD": [i for i, l in enumerate(LAB) if l == "INC" or l.startswith("H=")],
              "ALL": list(range(len(rungs)))}
    say(f"# {len(rungs)} rungs: {LAB}")

    recs, cells = [], []
    g1_done = False
    for pan in panels:
        idx = pan.idx[WARMUP:]
        spyw = windows(idx, pan.spy[WARMUP:])
        live = {c: windows(idx, backtest(pan.px, rules_v2_weights(pan.px), cost_bps=c,
                                         freq=A_C)["returns"].fillna(0.0).values[WARMUP:])
                for c in COSTS}
        wcache = {}
        raws = {}
        for lab, N, H, g in rungs:
            if (N, H) not in wcache: wcache[(N, H)] = build(pan, N, H)
            for dly in DELAYS:
                raws[(lab, dly)] = run_raw(pan, wcache[(N, H)], g, dly)

        if not g1_done:
            Wt = wcache[(INC["N"], INC["H"])]
            gr, tn = raws[("INC", 1)]
            wdf = pd.DataFrame(np.roll(INC["G"] * Wt, -1, axis=0), index=pan.idx,
                               columns=pan.px.columns)
            eng = backtest(pan.px, wdf, cost_bps=10.0, freq=A_C)["returns"].fillna(0.0).values
            d = float(np.abs((gr - tn * 10.0 / 1e4)[WARMUP:] - eng[WARMUP:]).max())
            gate("G1 fast runner == engine.backtest (incumbent, 10 bps)", f"{d:.3e}", "< 1e-12",
                 d < 1e-12)
            w = windows(idx, (gr - tn * 10.0 / 1e4)[WARMUP:])
            COMMITTED = dict(CAGR=0.125911, Sharpe=1.151737, MaxDD=-0.155135)
            dd = max(abs(w["full"][k] - v) for k, v in COMMITTED.items())
            gate("G2 incumbent reproduces idea 1286's committed U56 G=0.60 10bps t+1 row",
                 f"max|d| {dd:.2e}", "< 1e-4", dd < 1e-4)
            g1_done = True

        for dly in DELAYS:
            for cost in COSTS:
                R = np.column_stack([raws[(l, dly)][0][WARMUP:] -
                                     raws[(l, dly)][1][WARMUP:] * cost / 1e4 for l in LAB])
                W = [windows(idx, R[:, j]) for j in range(R.shape[1])]
                nis = W[0]["nis"]
                draws = block_draws(nis, BLOCK, NBOOT,
                                    np.random.default_rng(SEED + int(cost) * 10 + dly))
                sd = margin_sd(R[:nis], 0, draws)
                isS = np.array([w["is_"]["Sharpe"] for w in W])
                marg = isS - isS[0]
                for j, l in enumerate(LAB):
                    b = legs_4b(W[j], spyw); a = legs_4a(W[j], live[cost])
                    recs.append(dict(panel=pan.name, rung=l, cost=cost, delay=dly,
                                     IS_S=isS[j], margin=marg[j], sd=sd[j],
                                     t=marg[j] / sd[j] if sd[j] > 0 else np.nan,
                                     CAGR=W[j]["full"]["CAGR"], Sharpe=W[j]["full"]["Sharpe"],
                                     MaxDD=W[j]["full"]["MaxDD"], H1=W[j]["h1"]["Sharpe"],
                                     H2=W[j]["h2"]["Sharpe"], OOS_CAGR=W[j]["oos"]["CAGR"],
                                     OOS_S=W[j]["oos"]["Sharpe"], OOS_DD=W[j]["oos"]["MaxDD"],
                                     pass4a=all(a.values()), pass4b=all(b.values()),
                                     fail4b=failed(b)))
                for D in CLAIMSETS:
                    mem = MEMBER[D]
                    for q in QS:
                        z = 0.0 if q <= 0.5 else float(
                            np.sqrt(2) * _erfinv(2 * q - 1))
                        ok = [j for j in mem if j != 0 and np.isfinite(sd[j]) and sd[j] > 0
                              and marg[j] > z * sd[j]]
                        pick = max(ok, key=lambda j: isS[j]) if ok else 0
                        cells.append(dict(
                            panel=pan.name, claimset=D, q=q, cost=cost, delay=dly, z=z,
                            adopted=LAB[pick], moved=pick != 0, n_clear=len(ok),
                            IS_margin=marg[pick], bar=z * sd[pick] if pick else 0.0,
                            OOS_S=W[pick]["oos"]["Sharpe"], OOS_CAGR=W[pick]["oos"]["CAGR"],
                            OOS_DD=W[pick]["oos"]["MaxDD"],
                            frozen_OOS_S=W[0]["oos"]["Sharpe"],
                            d_oos=W[pick]["oos"]["Sharpe"] - W[0]["oos"]["Sharpe"],
                            Sharpe=W[pick]["full"]["Sharpe"], CAGR=W[pick]["full"]["CAGR"],
                            MaxDD=W[pick]["full"]["MaxDD"], H1=W[pick]["h1"]["Sharpe"],
                            H2=W[pick]["h2"]["Sharpe"],
                            pass4a=all(legs_4a(W[pick], live[cost]).values()),
                            pass4b=all(legs_4b(W[pick], spyw).values()),
                            fail4b=failed(legs_4b(W[pick], spyw))))
        say(f"# {pan.name} done ({time.time() - t0:.0f}s)")

    R = pd.DataFrame(recs); C = pd.DataFrame(cells)
    R.to_csv(f"{STEM}.rungs.csv", index=False); C.to_csv(f"{STEM}.cells.csv", index=False)
    say(f"\n# {len(R)} rung rows and {len(C)} chooser cells written\n")

    # ---------------- the rung ladders at the PROTOCOL rung
    for pan in panels:
        s = R[(R.panel == pan.name) & (R.cost == 10.0) & (R.delay == 1)]
        say(f"## {pan.name} rungs (10 bps, t+1) -- IS margin against the incumbent and its own "
            f"bootstrap SD")
        say(f"{'rung':>9} {'IS_S':>7} {'margin':>8} {'SD':>7} {'t':>6} {'CAGR':>7} {'Shrp':>7} "
            f"{'MaxDD':>7} {'OOS_S':>7} {'4b':>3} {'fail4b'}")
        for _, r in s.iterrows():
            say(f"{r.rung:>9} {r.IS_S:>7.4f} {r.margin:>+8.4f} {r.sd:>7.4f} {r.t:>+6.2f} "
                f"{r.CAGR:>7.2%} {r.Sharpe:>7.4f} {r.MaxDD:>7.2%} {r.OOS_S:>7.4f} "
                f"{'Y' if r.pass4b else 'n':>3} {r.fail4b}")
        say("")

    # ---------------- the chooser grid at the PROTOCOL rung
    say("## CHOOSER GRID (PROTOCOL rung 10 bps / t+1): what one declared q actually adopts")
    say(f"{'panel':>10} {'claims':>7} {'q':>5} {'adopted':>9} {'clear':>5} {'ISmarg':>8} "
        f"{'bar':>7} {'OOS_S':>7} {'frozen':>7} {'d(OOS)':>8} {'4b':>3}")
    for _, r in C[(C.cost == 10.0) & (C.delay == 1)].iterrows():
        say(f"{r.panel:>10} {r.claimset:>7} {r.q:>5.2f} {r.adopted:>9} {r.n_clear:>5.0f} "
            f"{r.IS_margin:>+8.4f} {r.bar:>7.4f} {r.OOS_S:>7.4f} {r.frozen_OOS_S:>7.4f} "
            f"{r.d_oos:>+8.4f} {'Y' if r.pass4b else 'n':>3}")
    say("")

    # ---------------- headline: is q priced?
    say("## HEADLINE 1 -- does the declared q change anything?")
    say(f"{'q':>5} {'cells':>6} {'MOVED':>6} {'mean d(OOS_S) vs FROZEN':>24} {'SE':>8} "
        f"{'t':>7} {'pos/neg':>9} {'mean d vs q=0.50':>18}")
    base = C[C.q == 0.50].set_index(["panel", "claimset", "cost", "delay"]).OOS_S
    for q in QS:
        s = C[C.q == q]
        d = s.d_oos.values
        se = d.std(ddof=1) / np.sqrt(len(d))
        dq = (s.set_index(["panel", "claimset", "cost", "delay"]).OOS_S - base).values
        say(f"{q:>5.2f} {len(s):>6} {int(s.moved.sum()):>6} {d.mean():>24.4f} {se:>8.4f} "
            f"{d.mean() / se if se else np.nan:>+7.2f} "
            f"{str(int((d > 0).sum())) + '/' + str(int((d < 0).sum())):>9} {dq.mean():>+18.4f}")
    inert = C.groupby(["panel", "claimset", "cost", "delay"]).adopted.nunique()
    say(f"\n   cells where the adopted rung is IDENTICAL at all five q: "
        f"{int((inert == 1).sum())} of {len(inert)}")
    say(f"   chooser MOVED off the incumbent at {int(C.moved.sum())} of {len(C)} "
        f"(panel/claimset/cost/delay/q) cells")

    say("\n## HEADLINE 2 -- does ANY q beat standing still?")
    best = C.groupby("q").d_oos.mean()
    say(f"   mean d(OOS Sharpe) by q: " + ", ".join(f"q={q:.2f} {v:+.4f}" for q, v in best.items()))
    allneg = all(v < 0 for v in best.values)
    say(f"   every q loses to the frozen incumbent: {allneg}")
    for p, s in C.groupby("panel"):
        b = s.groupby("q").d_oos.mean()
        say(f"      {p}: " + ", ".join(f"{q:.2f} {v:+.4f}" for q, v in b.items()))
    say(f"   4b PASS: adopted books {int(C.pass4b.sum())} of {len(C)}; "
        f"4a PASS {int(C.pass4a.sum())} of {len(C)}")

    # ---------------- census arm (reporting only)
    tot, withwhy, nf, per = census()
    say(f"\n## CENSUS ARM (crude LEXICAL count over {nf} committed .md files -- reporting only, "
        f"moves no gate)")
    say(f"   lines quoting a confidence level (0.80/0.90/0.95/0.99): {tot}")
    say(f"   of those, lines also carrying ANY justification token: {withwhy} "
        f"({withwhy / tot:.3f})" if tot else "   none found")
    top = sorted(per.items(), key=lambda kv: -kv[1][0])[:6]
    for f, (n, w) in top: say(f"      {f}: {n} lines, {w} with a justification token")
    say("   NOT CLAIMED: that the un-tokened lines are unjustified. A lexical test cannot read "
        "an argument; it can only show that the number and its reason are rarely in the same "
        "sentence. The capital arm above is what prices q.")

    gate("G3 chooser produced a decision at every cell", f"{len(C)}",
         f"{3 * len(CLAIMSETS) * len(QS) * len(COSTS) * len(DELAYS)}",
         len(C) == 3 * len(CLAIMSETS) * len(QS) * len(COSTS) * len(DELAYS))
    gate("G4 bootstrap SD is finite and positive at every rung", f"{int((R.sd > 0).sum())}",
         f"{len(R) - int((R.rung == 'INC').sum())} non-incumbent rows",
         int((R.sd > 0).sum()) >= len(R) - int((R.rung == "INC").sum()))

    say(f"\n# GATES: {sum(g['pass_'] for g in GATES)}/{len(GATES)} pass")
    say(f"# elapsed {time.time() - t0:.0f}s")
    Path(f"{STEM}.log.txt").write_text("\n".join(_LOG) + "\n")
    Path(f"{STEM}.gates.json").write_text(json.dumps(GATES, indent=1) + "\n")


def _erfinv(x):
    """Inverse error function (Giles' rational approximation) -- no scipy in this sandbox."""
    w = -np.log((1.0 - x) * (1.0 + x))
    if w < 5.0:
        w = w - 2.5
        p = 2.81022636e-08
        for c in (3.43273939e-07, -3.5233877e-06, -4.39150654e-06, 0.00021858087,
                  -0.00125372503, -0.00417768164, 0.246640727, 1.50140941):
            p = p * w + c
    else:
        w = np.sqrt(w) - 3.0
        p = -0.000200214257
        for c in (0.000100950558, 0.00134934322, -0.00367342844, 0.00573950773,
                  -0.0076224613, 0.00943887047, 1.00167406, 2.83297682):
            p = p * w + c
    return p * x


if __name__ == "__main__":
    main()
