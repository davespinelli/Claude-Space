#!/usr/bin/env python3
"""Idea 1281 (lane cloud, 2026-09-18): is the record's MAXDD UN-RESOLVABILITY really a
p = 0.999 FACT?

THE PREMISE (idea 1146, quoted by the queue).  1146 found that the tape-length signature that
makes MaxDD "un-resolvable" -- its bootstrap SD GROWING with tape length instead of shrinking --
switches OFF at every drawdown quantile below p = 0.999: b_sd -0.0926 at p = 0.90 against
+0.1654 at the maximum.  On this tape that means the whole effect lives in the top ~0.1% of the
drawdown distribution -- one or two crash troughs.

WHAT THE QUEUE ASKS, LITERALLY.  Re-run the record's DD floor / robustness claims with MaxDD
REPLACED by Q_0.99 throughout, and report how many committed DD-keyed verdicts change.

WHY IT IS A CAPITAL QUESTION AND NOT BOOKKEEPING.  PROTOCOL rule 4b's DD cap is the record's
ONLY binding risk leg (CHANGELOG, repeatedly).  If that cap is keyed on a statistic decided by
one or two troughs, then every 4b pass in the record is a claim about 2020 and 2022 wearing the
clothes of a distributional statement -- and a quantile key that reads the SAME drawdown path
with converging noise would be a drop-in replacement worth having.  This run asks whether the
substitution (i) moves anything, (ii) resolves better, (iii) forecasts better, (iv) PAYS.

DIALS (PROTOCOL rule 4: at most two, and both from the queue's own wording):
    DIAL 1  QUANTILE p in {0.90, 0.95, 0.975, 0.99, 0.995, 0.999, 1.00} of the |drawdown| path.
            p = 1.00 IS |MaxDD| exactly (gate G2), so the ladder provably contains the incumbent
            it is scored against.  p = 0.99 is the queue's nominated replacement.
    DIAL 2  PANEL in {U56, B136, SMALL663}.
Everything else is REPORTED at every value and is not tuned: the cap multiple (PROTOCOL's own
0.60, with 0.50 / 0.75 / 1.00 as a reported sensitivity), the four ladders of books, every
window (full / h1 / h2 / IS / OOS), and both KEEP paths.

THE BOOKS ARE THE RECORD'S OWN FOUR LADDERS AROUND ITS ANCHOR, not a fresh grid:
    N     {5, 10, 15, 20, 30, 40}                       slots
    H     {5, 10, 21, 42, 63, 90, 126, 189, 252}        minimum-hold rungs (1095's ladder)
    G     {0.50, 0.60, 0.75, 0.85, 1.00}                gross of NAV
    C     {D, W, M}                                     rebalance cadence
    anchor = N=20, H=126, G=0.75, C=W -- the committed 2026-09-04 KEEP 4b book.
Duplicates of the anchor across ladders are de-duplicated, giving 20 distinct books per panel.

FOUR ARMS, ALL PRE-DECLARED BEFORE ANY NUMBER WAS READ:
  ARM 1  DOES IT MOVE ANYTHING.  For every (panel, book, window) cell, the re-keyed DD leg is
         PASS iff Q_p(book) <= m * Q_p(SPY).  Report the share of cells bit-identical to the
         incumbent key and the share whose DD leg FLIPS, at every p and every m.
  ARM 2  IS IT BETTER RESOLVED.  Paired circular block bootstrap (block 63, B = 300, book and
         SPY resampled on the SAME draws, fixed seed) of the margin M = m*Q_p(SPY) - Q_p(book).
         Report the share of DD verdicts decided inside 1 SD of their own margin and the median
         |M|/SD, at every p.  1146 predicts Q_0.99 resolves BETTER than MaxDD.
  ARM 3  THE VERDICT CENSUS THE QUEUE ASKED FOR.  Whole 4b verdicts (all five legs; the other
         four held at their own values so any flip is attributable to the key) on the full
         window at m = 0.60, under every p against the incumbent.  Named, not just counted.
  ARM 4  CAPITAL, RULE 8, OOS READ ONCE.  Each (panel, p, m) cell supplies an IS-ONLY chooser:
         buy the highest-IS-Sharpe book passing all four IS-computable 4b legs under THAT cell's
         key; fallback (declared in advance) highest IS Sharpe.  Parameters chosen on
         warm-up..2016-12-31, 2017-2026 read ONCE.  Reported against SPY, live RULES v2 and the
         anchor, with both KEEP paths leg by leg.

PRE-DECLARED OUTCOMES:
  (A) Q_0.99 IS A DROP-IN REPLACEMENT -- it moves few verdicts, resolves better, and its
      chooser is no worse OOS.  Then the record should re-key and re-derive the multiple.
  (B) DIFFERENT, NOT BETTER -- it moves verdicts and costs OOS Sharpe where it does.
  (C) A RELABELLING -- Q_0.99 is bit-identical to MaxDD often enough that the substitution is
      not a substitution on this tape, and 1146's p = 0.999 boundary is not reachable here.
  (D) STRICTLY BETTER -- resolves better AND pays OOS.  Only (D) is a KEEP-candidate.

FROZEN at the record's construction, not touched here: RAW three-leg composite (21/252, 0/126,
0/63 percentile ranks), eligibility = above own 200d MA AND vol20 < 0.60, equal 1/len(held)
slots, 10 bps per unit turnover, t+1 execution, 260-row warm-up.  SPY is the BENCHMARK and is
NEVER a constituent (gate G7).

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL663 is a current
sub-$2B screen with the house `max_1d_move >= 1.0` filter applied FIRST.  The headline is a
CONTRAST between two keys read on identical windows of one tape -- which books a cap admits and
how well each cap resolves its own verdict -- and is first-order immune to a bias that moves
every book's drawdown together.  A current-constituent panel UNDERSTATES deep drawdowns
specifically, which is exactly the tail this run truncates, so the contrast is CONSERVATIVE for
the quantile key and optimistic for MaxDD.  The absolute OOS triples in ARM 4 are NOT immune and
are upper bounds; they are quoted against SPY and RULES v2 on the same panel.

Deterministic (fixed seed), offline, no network.  Run: python3 <this file>
"""
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE = "2026-09-18"
SLUG = "is-the-RECORD-s-MAXDD-UN-RESOLVABILITY-really-a-p-EQUALS-0.999-FACT"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
PS = [0.90, 0.95, 0.975, 0.99, 0.995, 0.999, 1.00]            # DIAL 1
PNAME = {0.90: "Q900", 0.95: "Q950", 0.975: "Q975", 0.99: "Q990",
         0.995: "Q995", 0.999: "Q999", 1.00: "Q1000(=MaxDD)"}
MULTS = [0.50, 0.60, 0.75, 1.00]                              # reported, not tuned
NL = [5, 10, 15, 20, 30, 40]
HL = [5, 10, 21, 42, 63, 90, 126, 189, 252]
GL = [0.50, 0.60, 0.75, 0.85, 1.00]
CL = ["D", "W", "M"]
BLOCK, NBOOT, SEED = 63, 300, 20260918
FRACS = [0.125, 0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]   # ARM 0, tape fractions
COMMITTED_1146 = {0.90: -0.0926, 1.00: +0.1654}                # b_sd, cross-run reference
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


def ddpath(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return np.abs(e / np.maximum.accumulate(e) - 1.0)


def mdd(r):
    return -float(ddpath(r).max())


def qdd(r, ps=PS):
    """DIAL 1: the p-th quantile of the |drawdown| path, as a POSITIVE magnitude.
    p = 1.00 is the maximum, i.e. |MaxDD| exactly (gate G2)."""
    return np.quantile(ddpath(r), ps)


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r); h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    w = dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
             is_=stats(r[:o]), oos=stats(r[o:]))
    w["dd"] = {k: qdd(v) for k, v in
               dict(full=r, h1=r[:h], h2=r[h:], is_=r[:o], oos=r[o:]).items()}
    return w


def flat(w):
    out = {}
    for k, v in w.items():
        if k == "dd":
            for wn, arr in v.items():
                for p, x in zip(PS, arr): out[f"dd_{wn}_{PNAME[p]}"] = x
        else:
            for m, x in v.items(): out[f"{k}_{m}"] = x
    return out


# ---------------------------------------------------------------- panel / books
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        assert "SPY" not in invest, "G7: SPY must never be a constituent"
        self.iinv = np.array([cols.index(c) for c in invest])
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
        self._reb = {}
        for f in CL:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self._reb[f] = np.flatnonzero(m)

    def reb(self, f): return self._reb[f]


def build(pan, H, N=A_N, freq=A_C, lag=1):
    """Min-hold-H, N-slot selection on the frozen composite. Identical mechanics to the
    record's committed runner; `lag` is the decide-t / trade-t+1 convention."""
    reb = pan.reb(freq)
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    key = pan.key
    nreb = len(reb)
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held): held = held[pr[t, held]]
        keep = [int(c) for c in (held[(t - cur[held]) < H] if len(held) else held)]
        k = key[ts].copy()
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
        stop = reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross=A_G, freq=A_C):
    reb = pan.reb(freq)
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M)); turn = np.zeros(T); curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def ladder_books():
    """The record's four ladders around its anchor, de-duplicated."""
    seen, out = set(), []
    for lab, N, H, G, Cd in (
            [(f"N={n}", n, A_H, A_G, A_C) for n in NL] +
            [(f"H={h}", A_N, h, A_G, A_C) for h in HL] +
            [(f"G={g:.2f}", A_N, A_H, g, A_C) for g in GL] +
            [(f"C={c}", A_N, A_H, A_G, c) for c in CL]):
        k = (N, H, G, Cd)
        if k in seen: continue
        seen.add(k); out.append((lab, N, H, G, Cd))
    return out


# ---------------------------------------------------------------- KEEP paths
def legs_4a(bk, live, pi, m=1.00):
    """4a with the DD leg re-keyed on quantile index pi against the LIVE book."""
    return dict(H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=bk["dd"]["full"][pi] <= m * live["dd"]["full"][pi])


def legs_4b(bk, spy, pi, m=DD_CAP):
    return dict(H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=bk["dd"]["full"][pi] <= m * spy["dd"]["full"][pi],
                CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def legs_4b_is(bk, spy, pi, m=DD_CAP):
    """The four legs computable IN SAMPLE (no OOS leg) -- what a rule-8 chooser may see."""
    return dict(H1=bk["is_h1"] > spy["is_h1"], H2=bk["is_h2"] > spy["is_h2"],
                DD=bk["is_dd"][pi] <= m * spy["is_dd"][pi],
                CAGR=bk["is_cagr"] >= CAGR_FLOOR * spy["is_cagr"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ---------------------------------------------------------------- bootstrap
def paired_boot_sd(rb, rs, ms, rng, nboot=NBOOT, block=BLOCK):
    """SD of the margin M = m*Q_p(SPY) - Q_p(book) under a PAIRED circular block bootstrap:
    book and SPY are resampled on the SAME index draws, so the margin's own noise is measured
    and not the difference of two independent noises. Returns array (len(MULTS), len(PS))."""
    n = len(rb)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(nboot, nb))
    off = np.arange(block)
    idxm = (starts[:, :, None] + off[None, None, :]).reshape(nboot, nb * block)[:, :n] % n
    qb = np.empty((nboot, len(PS))); qs = np.empty((nboot, len(PS)))
    for j in range(nboot):
        ix = idxm[j]
        qb[j] = qdd(rb[ix]); qs[j] = qdd(rs[ix])
    out = np.empty((len(ms), len(PS)))
    for a, m in enumerate(ms):
        out[a] = np.nanstd(m * qs - qb, axis=0, ddof=1)
    return out


def disjoint(n, L):
    w = int(np.floor(n * L))
    if w < 2 * BLOCK: return []
    return [(i * w, (i + 1) * w) for i in range(n // w)]


def ols_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3: return np.nan
    x, y = x[ok], y[ok]
    return float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())


def sd_of_q(r, rng, nboot=150, block=BLOCK):
    """Unpaired circular-block-bootstrap SD of Q_p itself, for ARM 0's tape-length scaling."""
    n = len(r)
    if n < 2 * block: return np.full(len(PS), np.nan)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(nboot, nb))
    off = np.arange(block)
    ix = (starts[:, :, None] + off[None, None, :]).reshape(nboot, nb * block)[:, :n] % n
    return np.nanstd(np.array([qdd(r[j]) for j in ix], float), axis=0, ddof=1)


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1281 lane cloud -- {SLUG}")
    say(f"# DIAL 1 QUANTILE p = {PS}  (p=1.00 IS |MaxDD| exactly, gate G2)")
    say(f"# DIAL 2 PANEL = U56 / B136 / SMALL")
    say(f"# cap multiples REPORTED (not tuned): {MULTS}; PROTOCOL's own is {DD_CAP}")
    say(f"# books: the record's four ladders around N={A_N} H={A_H} G={A_G} C={A_C}; "
        f"{COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# bootstrap: PAIRED circular block, L={BLOCK}, B={NBOOT}, seed {SEED}")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, "
        f"{len(bad & set(psm.columns))} dropped for max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    PI = {p: i for i, p in enumerate(PS)}
    iMAX = PI[1.00]; i99 = PI[0.99]
    BOOKS = ladder_books()
    ALAB = next(l for l, N, H, G, Cd in BOOKS if (N, H, G, Cd) == (A_N, A_H, A_G, A_C))
    say(f"# anchor book label = {ALAB}")
    say(f"# {len(BOOKS)} distinct books per panel x 3 panels = {3*len(BOOKS)} books")

    bookrows, cellrows, bootrows, r8rows, fliprows, arm0rows = [], [], [], [], [], []
    g1_val = None
    SPYMDD = {}

    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        SPYMDD[pname] = abs(spy["full"]["MaxDD"])
        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"{idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY      full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   OOS Sh {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2  full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS Sh {live['oos']['Sharpe']:.4f}")
        say("   SPY |dd| quantiles  " + "  ".join(
            f"{PNAME[p]}={spy['dd']['full'][PI[p]]:.4f}" for p in PS))

        # ---- books
        R, W = {}, {}
        for lab, N, H, G, Cd in BOOKS:
            R[lab] = run(pan, build(pan, H, N, Cd), G, Cd)[WARMUP:]
            W[lab] = windows(idx, R[lab])

        # ---- ARM 0: does 1146's PREMISE reproduce? b_sd of Q_p vs log tape length,
        #      anchor book, DISJOINT windows (idea 1146 lane cloud's own geometry finding).
        rng0 = np.random.default_rng(SEED + 101)
        ra = R[ALAB]
        for L in FRACS:
            wins = disjoint(len(ra), L)
            if not wins: continue
            sds = np.array([sd_of_q(ra[a:b], rng0) for a, b in wins], float)
            lv = np.array([qdd(ra[a:b]) for a, b in wins], float)
            m = np.nanmean(sds, axis=0); lvl = np.nanmean(lv, axis=0)
            for p in PS:
                arm0rows.append(dict(panel=pname, L=L, n_windows=len(wins), p=p,
                                     sd=m[PI[p]], level=lvl[PI[p]]))

        # ---- G1 fast runner == engine.backtest at the anchor (U56 only, once)
        if g1_val is None:
            # build() bakes the decide-t / trade-t+1 lag into its own rows, so the
            # engine-facing frame is rolled back one row before engine.backtest re-applies it.
            wdf = pd.DataFrame(np.roll(A_G * build(pan, A_H, A_N, A_C), -1, axis=0),
                               index=pan.idx, columns=pan.px.columns)
            eng = backtest(pan.px, wdf, cost_bps=COST, freq=A_C)["returns"].fillna(0.0).values
            g1_val = float(np.abs(R[ALAB] - eng[WARMUP:]).max())
            gate("G1 fast runner == engine.backtest (anchor)", f"{g1_val:.3e}", "< 1e-12",
                 g1_val < 1e-12)

        # ---- G2 / G3 on real books
        g2 = max(abs(W[l]["dd"]["full"][iMAX] - abs(W[l]["full"]["MaxDD"])) for l in W)
        g3 = sum(int(np.any(np.diff(W[l]["dd"]["full"]) < -1e-15)) for l in W)
        if pname == panels[0][0]:
            gate("G2 Q_1.00 == |MaxDD| exactly", f"{g2:.3e}", "0.0", g2 == 0.0)
            gate("G3 Q_p non-decreasing in p", g3, "0 violations", g3 == 0)

        # ---- ARM 1 + ARM 3: every (book, window, p, m) cell
        for lab, N, H, G, Cd in BOOKS:
            w = W[lab]
            base4b = legs_4b(w, spy, iMAX, DD_CAP)
            base4a = legs_4a(w, live, iMAX, 1.00)
            bookrows.append(dict(panel=pname, book=lab, N=N, H=H, gross=G, cadence=Cd,
                                 anchor=(N, H, G, Cd) == (A_N, A_H, A_G, A_C),
                                 keep4a_maxdd=all(base4a.values()),
                                 keep4b_maxdd=all(base4b.values()),
                                 fail4a=failed(base4a), fail4b=failed(base4b), **flat(w)))
            for p in PS:
                pi = PI[p]
                for m in MULTS:
                    for wn in ("full", "h1", "h2", "is_", "oos"):
                        qb, qs = w["dd"][wn][pi], spy["dd"][wn][pi]
                        qb0, qs0 = w["dd"][wn][iMAX], spy["dd"][wn][iMAX]
                        cellrows.append(dict(
                            panel=pname, book=lab, p=p, mult=m, window=wn,
                            q_book=qb, q_spy=qs, margin=m * qs - qb,
                            dd_pass=bool(qb <= m * qs),
                            dd_pass_incumbent=bool(qb0 <= m * qs0),
                            identical=bool(abs((m * qs - qb) - (m * qs0 - qb0)) < 1e-15)))
                    # whole-4b verdict flip census, full window, this p and m
                    v = legs_4b(w, spy, pi, m)
                    v0 = legs_4b(w, spy, iMAX, m)
                    fliprows.append(dict(panel=pname, book=lab, p=p, mult=m,
                                         keep4b=all(v.values()), keep4b_incumbent=all(v0.values()),
                                         fail=failed(v), fail_incumbent=failed(v0),
                                         margin=m * spy["dd"]["full"][pi] - w["dd"]["full"][pi],
                                         margin_incumbent=m * spy["dd"]["full"][iMAX]
                                                          - w["dd"]["full"][iMAX]))

        # ---- ARM 2: paired block bootstrap of the margin, full window
        rng = np.random.default_rng(SEED + abs(hash(pname)) % 10000)
        rspy = pan.spy[WARMUP:]
        for lab, *_ in BOOKS:
            sd = paired_boot_sd(R[lab], rspy, MULTS, rng)
            for a, m in enumerate(MULTS):
                for p in PS:
                    pi = PI[p]
                    M = m * spy["dd"]["full"][pi] - W[lab]["dd"]["full"][pi]
                    bootrows.append(dict(panel=pname, book=lab, p=p, mult=m, margin=M,
                                         sd=sd[a, pi],
                                         ratio=abs(M) / sd[a, pi] if sd[a, pi] > 0 else np.nan))

        # ---- ARM 4: rule-8 chooser, one per (p, m), IS-only, OOS read ONCE
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        ISB = {}
        for lab, *_ in BOOKS:
            r = R[lab]; ri = r[:o]; h = len(ri) // 2
            ISB[lab] = dict(is_sharpe=sharpe(ri), is_cagr=cagr(ri),
                            is_h1=sharpe(ri[:h]), is_h2=sharpe(ri[h:]), is_dd=qdd(ri))
        ri = rspy[:o]; h = len(ri) // 2
        ISS = dict(is_sharpe=sharpe(ri), is_cagr=cagr(ri), is_h1=sharpe(ri[:h]),
                   is_h2=sharpe(ri[h:]), is_dd=qdd(ri))
        for p in PS:
            pi = PI[p]
            for m in MULTS:
                elig = [l for l, *_ in BOOKS if all(legs_4b_is(ISB[l], ISS, pi, m).values())]
                pool = elig if elig else [l for l, *_ in BOOKS]
                pick = max(pool, key=lambda l: (ISB[l]["is_sharpe"], l))
                w = W[pick]
                a4, b4 = legs_4a(w, live, pi, 1.00), legs_4b(w, spy, pi, m)
                r8rows.append(dict(panel=pname, p=p, mult=m, pick=pick,
                                   n_eligible=len(elig), fallback=not bool(elig),
                                   is_sharpe=ISB[pick]["is_sharpe"],
                                   oos_CAGR=w["oos"]["CAGR"], oos_Sharpe=w["oos"]["Sharpe"],
                                   oos_MaxDD=w["oos"]["MaxDD"],
                                   full_CAGR=w["full"]["CAGR"], full_Sharpe=w["full"]["Sharpe"],
                                   full_MaxDD=w["full"]["MaxDD"],
                                   h1=w["h1"]["Sharpe"], h2=w["h2"]["Sharpe"],
                                   keep4a=all(a4.values()), keep4b=all(b4.values()),
                                   fail4a=failed(a4), fail4b=failed(b4),
                                   spy_oos_Sharpe=spy["oos"]["Sharpe"],
                                   spy_oos_CAGR=spy["oos"]["CAGR"],
                                   spy_oos_MaxDD=spy["oos"]["MaxDD"],
                                   live_oos_Sharpe=live["oos"]["Sharpe"],
                                   anchor_oos_Sharpe=W[ALAB]["oos"]["Sharpe"]))

    BK = pd.DataFrame(bookrows); CE = pd.DataFrame(cellrows)
    BO = pd.DataFrame(bootrows); R8 = pd.DataFrame(r8rows); FL = pd.DataFrame(fliprows)
    A0 = pd.DataFrame(arm0rows)

    # ---- G4: the incumbent cell reproduces PROTOCOL 4b's DD leg on every book
    inc = CE[(CE.p == 1.00) & (CE.mult == DD_CAP) & (CE.window == "full")]
    chk = BK.set_index(["panel", "book"])
    bad4 = 0
    for _, r in inc.iterrows():
        # PROTOCOL 4b as written: MaxDD(book) >= 0.60 * MaxDD(SPY), both NEGATIVE.
        want = chk.loc[(r.panel, r.book), "full_MaxDD"] >= DD_CAP * (-SPYMDD[r.panel])
        if bool(r.dd_pass) != bool(want): bad4 += 1
    gate("G4 incumbent cell == PROTOCOL 4b DD leg", bad4, "0 disagreements", bad4 == 0)

    # ---- G5: bootstrap SD stable across rng streams
    pan0 = Panel("U56chk", panels[0][1], panels[0][2])
    r0 = run(pan0, build(pan0, A_H))[WARMUP:]
    s0 = paired_boot_sd(r0, pan0.spy[WARMUP:], [DD_CAP], np.random.default_rng(SEED))[0]
    s1 = paired_boot_sd(r0, pan0.spy[WARMUP:], [DD_CAP], np.random.default_rng(SEED + 7))[0]
    rel = float(np.median(np.abs(s1 - s0) / np.maximum(s0, 1e-12)))
    gate("G5 bootstrap SD stable across streams", f"{rel:.4f}", "< 0.25", rel < 0.25)
    gate("G6 chooser decided on IS rows only", "structural (legs_4b_is, no OOS field)",
         "true", True)
    gate("G7 SPY never a constituent", "asserted in Panel.__init__", "true", True)

    # ================================================================ ARM 0
    say("\n### ARM 0 -- DOES 1146's PREMISE REPRODUCE? b_sd = OLS slope of log SD(Q_p) on "
        "log(tape fraction), anchor book, DISJOINT windows")
    say(f"   1146 committed, for reference: p=0.90 {COMMITTED_1146[0.90]:+.4f}, "
        f"p=1.00 (MaxDD) {COMMITTED_1146[1.00]:+.4f}")
    b0 = {}
    for pn in A0.panel.unique():
        d = A0[A0.panel == pn]
        b0[pn] = {PNAME[p]: ols_slope(np.log(d[d.p == p].L), np.log(d[d.p == p].sd))
                  for p in PS}
    T0 = pd.DataFrame(b0).T
    say(T0.to_string(float_format=lambda x: f"{x:+.4f}"))
    say("   (b_sd > 0 = sampling noise GROWS with tape length = 'un-resolvable'; "
        "b_sd < 0 = converges normally)")

    # ================================================================ ARM 1
    say("\n### ARM 1 -- DOES THE RE-KEY MOVE ANYTHING "
        "(all panels, all books, all windows, at PROTOCOL's own multiple 0.60)")
    a1 = CE[CE.mult == DD_CAP]
    t1 = a1.groupby("p").agg(identical_share=("identical", "mean"),
                             flip_share=("dd_pass", lambda s: np.nan))
    ident = a1.groupby("p")["identical"].mean()
    flip = a1.groupby("p").apply(lambda d: (d.dd_pass != d.dd_pass_incumbent).mean(),
                                 include_groups=False)
    tab = pd.DataFrame({"identical_share": ident, "DD_flip_share": flip})
    tab.index = [PNAME[p] for p in tab.index]
    say(tab.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n   DD-leg flip share by panel x p (m = 0.60):")
    fp = a1.groupby(["panel", "p"]).apply(
        lambda d: (d.dd_pass != d.dd_pass_incumbent).mean(), include_groups=False).unstack()
    fp.columns = [PNAME[c] for c in fp.columns]
    say(fp.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n   DD-leg PASS RATE by p and multiple (all cells):")
    pr = CE.groupby(["mult", "p"])["dd_pass"].mean().unstack()
    pr.columns = [PNAME[c] for c in pr.columns]
    say(pr.to_string(float_format=lambda x: f"{x:.4f}"))

    # ================================================================ ARM 2
    say("\n### ARM 2 -- IS THE QUANTILE KEY BETTER RESOLVED "
        f"(paired circular block bootstrap, L={BLOCK}, B={NBOOT})")
    b2 = BO[BO.mult == DD_CAP]
    t2 = pd.DataFrame({
        "share_inside_1SD": b2.groupby("p")["ratio"].apply(lambda s: (s < 1.0).mean()),
        "median_|M|/SD": b2.groupby("p")["ratio"].median(),
        "median_SD": b2.groupby("p")["sd"].median()})
    t2.index = [PNAME[p] for p in t2.index]
    say(t2.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n   share decided inside 1 SD, by multiple:")
    t2b = BO.groupby(["mult", "p"])["ratio"].apply(lambda s: (s < 1.0).mean()).unstack()
    t2b.columns = [PNAME[c] for c in t2b.columns]
    say(t2b.to_string(float_format=lambda x: f"{x:.4f}"))

    # ================================================================ ARM 3
    say("\n### ARM 3 -- THE VERDICT CENSUS THE QUEUE ASKED FOR "
        "(whole 4b, full window, m = 0.60)")
    f3 = FL[FL.mult == DD_CAP]
    n_inc = int(f3[f3.p == 1.00]["keep4b_incumbent"].sum())
    say(f"   incumbent (MaxDD) whole-4b passes: {n_inc} of {len(f3[f3.p==1.00])}")
    for p in PS:
        d = f3[f3.p == p]
        chg = d[d.keep4b != d.keep4b_incumbent]
        p2f = int(((~d.keep4b) & d.keep4b_incumbent).sum())
        f2p = int((d.keep4b & (~d.keep4b_incumbent)).sum())
        say(f"   {PNAME[p]:>14}: passes {int(d.keep4b.sum()):3d}  "
            f"changed {len(chg):3d} of {len(d)}  (pass->fail {p2f}, fail->pass {f2p})")
    d99 = f3[f3.p == 0.99]
    chg99 = d99[d99.keep4b != d99.keep4b_incumbent]
    say(f"\n   NAMED FLIPS at the queue's nominated p = 0.99 "
        f"({len(chg99)} of {len(d99)}):")
    if len(chg99):
        say(chg99[["panel", "book", "keep4b_incumbent", "keep4b", "fail_incumbent",
                   "fail", "margin_incumbent", "margin"]]
            .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    else:
        say("   (none)")

    # ================================================================ ARM 4
    say("\n### ARM 4 -- CAPITAL, RULE 8, OOS 2017-2026 READ ONCE")
    piv = R8.pivot_table(index=["panel", "mult"], columns="p", values="oos_Sharpe")
    piv.columns = [PNAME[c] for c in piv.columns]
    say("   chooser OOS Sharpe by (panel, multiple) x p:")
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    base = R8[R8.p == 1.00].set_index(["panel", "mult"])["oos_Sharpe"]
    diffs = {}
    for p in PS:
        if p == 1.00: continue
        d = R8[R8.p == p].set_index(["panel", "mult"])["oos_Sharpe"] - base
        diffs[PNAME[p]] = dict(mean=d.mean(), se=d.std(ddof=1) / np.sqrt(len(d)),
                               n_diff_pick=int((R8[R8.p == p].set_index(["panel", "mult"])["pick"]
                                                != R8[R8.p == 1.00].set_index(["panel", "mult"])["pick"]).sum()),
                               n=len(d))
    say("\n   d(OOS Sharpe) vs the MaxDD-keyed chooser, over all 12 (panel, multiple) cells:")
    say(pd.DataFrame(diffs).T.to_string(float_format=lambda x: f"{x:+.4f}"))
    say(f"\n   4a passes: {int(R8.keep4a.sum())} of {len(R8)} chooser rows; "
        f"4b (own key): {int(R8.keep4b.sum())} of {len(R8)}")
    say(f"   published books: 4a {int(BK.keep4a_maxdd.sum())} of {len(BK)}, "
        f"4b {int(BK.keep4b_maxdd.sum())} of {len(BK)} (incumbent key)")
    best = R8.loc[R8.oos_Sharpe.idxmax()]
    say(f"\n   BEST quantile-keyed chooser: {best.panel} p={PNAME[best.p]} m={best.mult} "
        f"-> {best['pick']}")
    say(f"     full {best.full_CAGR:7.2%} / {best.full_Sharpe:.4f} / {best.full_MaxDD:7.2%}   "
        f"halves {best.h1:.4f} / {best.h2:.4f}")
    say(f"     OOS  {best.oos_CAGR:7.2%} / {best.oos_Sharpe:.4f} / {best.oos_MaxDD:7.2%}")
    say(f"     vs SPY OOS {best.spy_oos_CAGR:7.2%} / {best.spy_oos_Sharpe:.4f} / "
        f"{best.spy_oos_MaxDD:7.2%};  live RULES v2 OOS {best.live_oos_Sharpe:.4f};  "
        f"anchor OOS {best.anchor_oos_Sharpe:.4f}")
    say(f"     4a {'PASS' if best.keep4a else 'FAIL'} ({best.fail4a})   "
        f"4b {'PASS' if best.keep4b else 'FAIL'} ({best.fail4b})")

    # ---- write
    BK.to_csv(f"{STEM}.books.csv", index=False)
    CE.to_csv(f"{STEM}.cells.csv.gz", index=False)
    BO.to_csv(f"{STEM}.bootstrap.csv", index=False)
    FL.to_csv(f"{STEM}.flips.csv", index=False)
    A0.to_csv(f"{STEM}.scaling.csv", index=False)
    R8.to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\n# gates {sum(g['pass_'] for g in GATES)}/{len(GATES)}  "
        f"elapsed {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
