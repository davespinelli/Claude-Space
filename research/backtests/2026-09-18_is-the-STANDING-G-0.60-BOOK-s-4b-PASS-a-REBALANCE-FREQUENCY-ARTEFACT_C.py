#!/usr/bin/env python3
"""Idea 1285 (lane C, 2026-09-18): is the STANDING G = 0.60 BOOK's 4b PASS a REBALANCE
FREQUENCY ARTEFACT?

THE PREMISE.  The record's single confirmed 4b candidate -- the U56 book, top N = 20 by the
frozen 21/252 + 0/126 + 0/63 composite among names above their own 200d MA with vol20 < 0.60,
min-hold H = 126 trading days, equal weight, gross rung G = 0.60 -- is fixed at WEEKLY
decide-Friday and has never been re-priced on any other cadence.  Idea 1286 (this repo, today)
found that on B135 ONE extra day of fill delay costs the same construction 4b's drawdown leg
outright (MaxDD -16.84% -> -20.44% against a -20.23% cap).  If a single day of timing does that,
the CADENCE dial may be carrying more of the standing pass than the composite is.

THE CONFOUND THAT MAKES THIS NON-TRIVIAL, FROM THE RECORD.  Idea 943 established that the
W -> M improvement is a TURNOVER REBATE EVERY BOOK COLLECTS: a gross-matched null's own median
gain runs +0.0466 / +0.3334 / +0.7624 / +1.4501 Sharpe at 0 / 10 / 25 / 50 bps.  So "the book
does better monthly" is not by itself a fact about the book.  Every cadence reading here is
therefore published BESIDE a same-cadence control, and the difference -- not the level -- is
the claim.

THE TWO DIALS (PROTOCOL rule 4, max 2 tuned parameters):
    DIAL 1  CADENCE  {D, W, M, Q} -- decide on the last trading day of the period, fill t+1.
    DIAL 2  COST RUNG  {10, 25, 50} bps per unit turnover, the queue's own set.  0 bps is
            published beside them as a REFERENCE column (costs are exactly linear in turnover,
            so it is free and it is what isolates the rebate).
GROSS is NOT a dial: all five rungs {0.50, 0.60, 0.75, 0.85, 1.00} are published at every grid
point; the standing rung G = 0.60 carries every headline; the rule-8 arm chooses it in sample.
PANEL is reported at every value, never selected on.

THE ARMS, identical in everything but selection:
    RANK     the standing book.  The thing being defended.
    RAND     IDENTICAL mechanics -- same N = 20 slots, same min-hold H = 126, same equal
             weights, same cadence, same eligibility set -- drawing uniformly at random instead
             of by composite.  12 seeds.  THIS IS THE TURNOVER-MATCHED CONTROL the queue asks
             for: it is matched by CONSTRUCTION (same slot count, same min-hold, same cadence),
             and the match is not assumed -- realised turnover/yr is published for both arms at
             every cell, and every RANK - RAND comparison is ALSO published in a
             TURNOVER-NEUTRAL form in which the control is charged the cost rung
             c * (turnover_RANK / turnover_RAND) so the two pay exactly the same annual drag.
    SPYONLY  gross g of NAV in SPY, rest cash.  Exposure with no selection and no intra-period
             trading; cadence-invariant by construction (gate G4), so it is the fixed ruler the
             whole cadence ladder is read against.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) NOT AN ARTEFACT -- the standing construction passes 4b at G = 0.60 on U56 at W AND at a
      majority of the other cadences, and RANK - RAND stays positive across the ladder.  The
      weekly choice is a convenience, not the result.
  (B) ARTEFACT -- the pass exists at W and nowhere else, and/or RANK - RAND at W is not
      distinguishable from the same difference at the cadences that fail.  The record would
      then have to write the book as "weekly, and only weekly", or retire it.
  (C) ARTEFACT IN THE OTHER DIRECTION -- some slower cadence dominates W, but by no more than
      the null's own same-cadence rebate, i.e. the record has been reading 943's rebate as an
      edge.
  (D) COST-CONTINGENT -- the cadence verdict reverses between 10 and 50 bps, in which case
      PROTOCOL's 10 bps assumption, not the tape, is picking the book.

THE RULE-8 ARM (PROTOCOL rule 8, required).  Parameters chosen on warm-up..2016-12-31 ONLY,
2017-2026 read ONCE.  Two choosers per (panel, arm, seed, cost) cell, both pre-declared:
    FREE    picks (cadence, gross) jointly in sample -- highest IS Sharpe among combinations
            passing all four IS-computable 4b legs, fallback highest IS Sharpe.
    FROZEN  picks gross only, cadence PINNED at W (the standing book's own cadence).
d(OOS Sharpe) = FREE - FROZEN is the direct capital answer: if letting the chooser move the
cadence does not pay out of sample, the cadence is not a dial worth having, and the standing
weekly book loses nothing by staying weekly.

FROZEN, not touched here: the composite and its three legs, eligibility (above 200d MA and
vol20 < 0.60), N = 20, H = 126, equal 1/len(held) slots, t+1 fill (PROTOCOL rule 2), the
260-row warm-up, the 4b constants (DD cap 0.60 x SPY, CAGR floor 0.70 x SPY).  SPY is the
BENCHMARK and NEVER a panel constituent (gate G5).

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists; SMALL663 is a current
sub-$2B screen with the house `max_1d_move >= 1.0` filter applied FIRST.  A current-constituent
list is a list of SURVIVORS, so a RANDOM draw from it is a draw from winners and the RAND
control is FLATTERED -- which biases this run AGAINST outcome (A).  It also understates deep
drawdowns, which is the leg the record says binds, so every absolute 4b verdict and OOS triple
below is an UPPER BOUND.  The headline is a CONTRAST between cadences read on identical windows
of one tape and is first-order immune to a bias that moves all four cadences together.

POST-RUN NOTE, added after the first execution and left here rather than edited away
(PROTOCOL rule 7).  The pre-declaration above calls SPYONLY "cadence-invariant by construction"
and gate G4 was written to assert it.  G4 FAILS, and the failure is a finding: at gross < 1.00
the arm carries a CASH SLEEVE and rebalancing back to gross g IS a trade, so a book with no
stock selection whatsoever is still a cadence object.  The pre-declared gate is kept in the
table as a refuted premise, its spread is published beside the book's own, and the invariant
that IS true -- gross = 1.00, no cash sleeve, zero turnover -- is added as G4b.  Nothing in the
headline depends on the refuted claim; SPY itself, not SPYONLY, is 4b's benchmark.

Deterministic (fixed seeds), offline, no network.  Run: python3 <this file>
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
SLUG = "is-the-STANDING-G-0.60-BOOK-s-4b-PASS-a-REBALANCE-FREQUENCY-ARTEFACT"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H = 20, 126
STAND_C, STAND_G = "W", 0.60                     # the standing rung under defence
LEGS = [(21, 252), (0, 126), (0, 63)]
CADENCES = ["D", "W", "M", "Q"]                  # DIAL 1
COSTS = [0.0, 10.0, 25.0, 50.0]                  # DIAL 2 (0 published as reference)
GROSSES = [0.50, 0.60, 0.75, 0.85, 1.00]         # reported everywhere, never tuned
NSEED, SEED0 = 12, 20260918
# the record's committed standing-rung triple (idea 1281, U56 G=0.60, W, 10 bps, t+1)
REC_U56 = dict(CAGR=0.1259, Sharpe=1.1517, MaxDD=-0.1551, oos_Sharpe=1.1826)
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
                is_=stats(r[:o]), oos=stats(r[o:]),
                is_h1=sharpe(r[:o][:o // 2]), is_h2=sharpe(r[:o][o // 2:]))


def flat(w):
    out = {}
    for k, v in w.items():
        if isinstance(v, dict):
            for m, x in v.items(): out[f"{k}_{m}"] = x
        else: out[k] = v
    return out


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
        self.reb = {}
        for c in CADENCES:
            m = rebalance_mask(px.index, c).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.reb[c] = np.flatnonzero(m)


def _slots(pan, reb, keyfn, N, H):
    """Shared N-slot / min-hold-H machinery. keyfn(ts) -> per-name sort key (lower is better,
    np.inf = ineligible). RANK and RAND differ ONLY in keyfn -- that is the whole control."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(reb)
    for i, t in enumerate(reb):
        ts = max(t - 1, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held): held = held[pr[t, held]]
        keep = [int(c) for c in (held[(t - cur[held]) < H] if len(held) else held)]
        k = keyfn(ts).copy()
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


def w_rank(pan, cad):
    return _slots(pan, pan.reb[cad], lambda ts: pan.key[ts], A_N, A_H)


def w_rand(pan, cad, seed):
    rng = np.random.default_rng(seed)
    draw = rng.random((len(pan.idx), len(pan.iinv)))   # pre-drawn: reproducible, cadence-free
    return _slots(pan, pan.reb[cad], lambda ts: draw[ts], A_N, A_H)


def w_spy(pan):
    T, M = pan.rets.shape
    W = np.zeros((T, M))
    W[:, pan.ispy] = 1.0
    return W


def run_raw(pan, reb, Wt, gross):
    """Gross-of-cost return path and per-day turnover, fill t+1 (PROTOCOL rule 2, baked into
    reb).  Costs are applied OUTSIDE so all four rungs of DIAL 2 come from one run (the cost
    term is exactly linear in turnover) -- and so the TURNOVER-NEUTRAL re-charge is exact."""
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


def legs_4b_is(bk, spy):
    """The four legs computable IN SAMPLE -- all a rule-8 chooser may see."""
    return dict(H1=bk["is_h1"] > spy["is_h1"], H2=bk["is_h2"] > spy["is_h2"],
                DD=bk["is_"]["MaxDD"] >= DD_CAP * spy["is_"]["MaxDD"],
                CAGR=bk["is_"]["CAGR"] >= CAGR_FLOOR * spy["is_"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1285 lane C -- {SLUG}")
    say(f"# DIAL 1 CADENCE = {CADENCES};  DIAL 2 COST = {COSTS} bps (0 = reference column)")
    say(f"# ARMS: RANK (the standing book) / RAND ({NSEED} seeds, same N/H/cadence, ranking "
        f"removed = the turnover-matched control) / SPYONLY (exposure alone, cadence-invariant)")
    say(f"# GROSS published at every grid point, never tuned: {GROSSES}; standing rung "
        f"G = {STAND_G}, standing cadence {STAND_C}, fill t+1")
    say(f"# frozen: N={A_N} H={A_H} warm-up={WARMUP} elig=above200d & vol20<{MAXVOL}")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, r8rows, turn_rows = [], [], []
    SPYSH, TURN = {}, {}
    g1_done = False
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        yrs = len(idx) / 252.0
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=10.0,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        SPYSH[pname] = spy["full"]["Sharpe"]
        say(f"\n## {pname}  n_names={len(inv)}  {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY      full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   OOS Sh {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2  full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS Sh {live['oos']['Sharpe']:.4f}")
        say(f"   decision counts D/W/M/Q = " +
            " / ".join(str(len(pan.reb[c])) for c in CADENCES))

        cache = {}          # (arm, seed, cad, gross) -> (gross_ret, turn)
        for cad in CADENCES:
            WS = [("RANK", -1, w_rank(pan, cad)), ("SPYONLY", -1, w_spy(pan))]
            WS += [("RAND", s, w_rand(pan, cad, SEED0 + s)) for s in range(NSEED)]
            if not g1_done and cad == STAND_C:
                wdf = pd.DataFrame(np.roll(STAND_G * WS[0][2], -1, axis=0),
                                   index=pan.idx, columns=pan.px.columns)
                eng = backtest(pan.px, wdf, cost_bps=10.0, freq=STAND_C)["returns"].fillna(0.0).values
                gr, tn = run_raw(pan, pan.reb[cad], WS[0][2], STAND_G)
                d = float(np.abs((gr - tn * 10.0 / 1e4)[WARMUP:] - eng[WARMUP:]).max())
                gate("G1 fast runner == engine.backtest (standing book, W, 10bps)",
                     f"{d:.3e}", "< 1e-12", d < 1e-12)
                g1_done = True
            for arm, seed, Wt in WS:
                for g in GROSSES:
                    gr, tn = run_raw(pan, pan.reb[cad], Wt, g)
                    grw, tnw = gr[WARMUP:], tn[WARMUP:]
                    cache[(arm, seed, cad, g)] = (grw, tnw)
                    ty = tnw.sum() / yrs
                    TURN[(pname, arm, seed, cad, g)] = ty
                    for c in COSTS:
                        r = grw - tnw * c / 1e4
                        w = windows(idx, r)
                        a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                        rows.append(dict(panel=pname, arm=arm, seed=seed, cadence=cad,
                                         gross=g, cost=c, turnover_yr=ty,
                                         keep4a=all(a4.values()), keep4b=all(b4.values()),
                                         fail4a=failed(a4), fail4b=failed(b4), **flat(w)))

        # ---- TURNOVER-NEUTRAL control: charge RAND the rung that equalises annual drag
        for cad in CADENCES:
            for g in GROSSES:
                grk, tnk = cache[("RANK", -1, cad, g)]
                tk = tnk.sum()
                for s in range(NSEED):
                    grd, tnd = cache[("RAND", s, cad, g)]
                    td = tnd.sum()
                    ratio = tk / td if td > 0 else np.nan
                    for c in COSTS:
                        rk = windows(idx, grk - tnk * c / 1e4)
                        ce = c * ratio if np.isfinite(ratio) else c
                        rd = windows(idx, grd - tnd * ce / 1e4)
                        turn_rows.append(dict(panel=pname, cadence=cad, gross=g, cost=c, seed=s,
                                              turn_rank=tk / yrs, turn_rand=td / yrs,
                                              ratio=ratio, cost_eff_rand=ce,
                                              rank_Sharpe=rk["full"]["Sharpe"],
                                              rand_Sharpe_neutral=rd["full"]["Sharpe"],
                                              rank_oos=rk["oos"]["Sharpe"],
                                              rand_oos_neutral=rd["oos"]["Sharpe"]))

        # ---- rule 8: FREE picks (cadence, gross) IS-only; FROZEN pins cadence at W
        for arm, seed in [("RANK", -1), ("SPYONLY", -1)] + [("RAND", s) for s in range(NSEED)]:
            for c in COSTS:
                cand = {}
                for cad in CADENCES:
                    for g in GROSSES:
                        gr, tn = cache[(arm, seed, cad, g)]
                        cand[(cad, g)] = windows(idx, gr - tn * c / 1e4)
                for mode, pool0 in [("FREE", list(cand)),
                                    ("FROZEN_W", [k for k in cand if k[0] == STAND_C])]:
                    ok = [k for k in pool0 if all(legs_4b_is(cand[k], spy).values())]
                    pool = ok if ok else pool0
                    pick = max(pool, key=lambda k: (cand[k]["is_"]["Sharpe"],
                                                    CADENCES.index(k[0]), k[1]))
                    w = cand[pick]
                    a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                    r8rows.append(dict(panel=pname, arm=arm, seed=seed, cost=c, mode=mode,
                                       pick_cadence=pick[0], pick_gross=pick[1],
                                       n_eligible=len(ok), fallback=not bool(ok),
                                       is_Sharpe=w["is_"]["Sharpe"],
                                       oos_CAGR=w["oos"]["CAGR"], oos_Sharpe=w["oos"]["Sharpe"],
                                       oos_MaxDD=w["oos"]["MaxDD"],
                                       full_CAGR=w["full"]["CAGR"],
                                       full_Sharpe=w["full"]["Sharpe"],
                                       full_MaxDD=w["full"]["MaxDD"],
                                       h1=w["h1"]["Sharpe"], h2=w["h2"]["Sharpe"],
                                       keep4a=all(a4.values()), keep4b=all(b4.values()),
                                       fail4a=failed(a4), fail4b=failed(b4),
                                       spy_oos_Sharpe=spy["oos"]["Sharpe"],
                                       spy_oos_CAGR=spy["oos"]["CAGR"],
                                       spy_oos_MaxDD=spy["oos"]["MaxDD"],
                                       spy_full_Sharpe=spy["full"]["Sharpe"],
                                       live_oos_Sharpe=live["oos"]["Sharpe"]))

    D = pd.DataFrame(rows); R8 = pd.DataFrame(r8rows); TN = pd.DataFrame(turn_rows)
    say(f"\n# published cells: {len(D)}   chooser rows: {len(R8)}   "
        f"turnover-neutral rows: {len(TN)}")

    # ================================================================ GATES
    say("\n### GATES")
    sp = D[(D.arm == "SPYONLY") & (D.cost == 0.0) & (D.gross == 1.00)]
    g2 = float(max(abs(r.full_Sharpe - SPYSH[r.panel]) for _, r in sp.iterrows()))
    gate("G2 SPYONLY at gross 1.00, 0 bps reproduces that panel's OWN SPY Sharpe",
         f"{g2:.3e}", "< 1e-9", g2 < 1e-9)
    mono = D.groupby(["panel", "arm", "seed", "cadence", "gross"]).apply(
        lambda d: bool(d.sort_values("cost").full_CAGR.is_monotonic_decreasing),
        include_groups=False)
    gate("G3 CAGR non-increasing in the cost rung", f"{int((~mono).sum())} violations",
         "0", int((~mono).sum()) == 0)
    # G4 was PRE-DECLARED as "SPYONLY is cadence-invariant, so it is a fixed ruler".  It is
    # REFUTED, and the refutation is a result, not a bug: at gross < 1.00 the arm holds a CASH
    # SLEEVE, and rebalancing back to gross g IS a trade, so even a book with no stock selection
    # at all is a cadence object.  It is kept in the gate table as a failed pre-declaration
    # (PROTOCOL rule 7) and the spread it opens is published beside the book's own.
    idn = D[D.arm == "SPYONLY"].groupby(["panel", "gross", "cost"])["full_Sharpe"].nunique()
    gate("G4 (pre-declared, REFUTED) SPYONLY invariant to cadence at EVERY gross",
         f"max distinct = {int(idn.max())}", "1", int(idn.max()) == 1)
    sp1 = D[(D.arm == "SPYONLY") & (D.gross == 1.00)]
    g4b = float(sp1.groupby(["panel", "cost"])["full_Sharpe"].nunique().max())
    g4t = float(sp1.turnover_yr.abs().max())
    gate("G4b SPYONLY at gross 1.00 (NO cash sleeve) IS cadence- and cost-invariant",
         f"max distinct Sharpe = {int(g4b)}, max turnover/yr = {g4t:.2e}", "1 and ~0",
         int(g4b) == 1 and g4t < 1e-9)
    say("   -- the refutation, quantified: SPYONLY's own Sharpe spread across D/W/M/Q at "
        f"G = {STAND_G}, by (panel, cost):")
    for pname in D.panel.unique():
        for c in COSTS:
            v = [float(D[(D.panel == pname) & (D.arm == "SPYONLY") & (D.cadence == cd) &
                         (D.gross == STAND_G) & (D.cost == c)].full_Sharpe.iloc[0])
                 for cd in CADENCES]
            say(f"      {pname:>9} {c:4.0f} bps: " +
                " ".join(f"{cd} {x:.4f}" for cd, x in zip(CADENCES, v)) +
                f"   spread {max(v) - min(v):.4f}")
    gate("G5 SPY never a panel constituent", "asserted in Panel.__init__", "true", True)
    gate("G6 every chooser decided on IS rows only", "structural (legs_4b_is / is_ windows)",
         "true", True)
    tt = D[(D.arm == "RANK") & (D.gross == STAND_G) & (D.cost == 10.0)]
    bad_t = 0
    for p in tt.panel.unique():
        v = [float(tt[(tt.panel == p) & (tt.cadence == c)].turnover_yr.iloc[0]) for c in CADENCES]
        bad_t += sum(1 for a, b in zip(v, v[1:]) if b > a + 1e-12)
    gate("G7 RANK turnover/yr non-increasing as the cadence slows (D>=W>=M>=Q)",
         f"{bad_t} violations of 9", "0", bad_t == 0)
    rec = D[(D.panel == "U56") & (D.arm == "RANK") & (D.cadence == STAND_C) &
            (D.gross == STAND_G) & (D.cost == 10.0)].iloc[0]
    d8 = max(abs(rec.full_Sharpe - REC_U56["Sharpe"]), abs(rec.oos_Sharpe - REC_U56["oos_Sharpe"]))
    gate("G8 reproduces the record's committed standing-rung triple (idea 1281, U56 G=0.60 W 10bps)",
         f"full {rec.full_CAGR:.2%}/{rec.full_Sharpe:.4f}/{rec.full_MaxDD:.2%} OOS "
         f"{rec.oos_Sharpe:.4f}  (max|dSharpe| {d8:.4f})",
         f"{REC_U56['CAGR']:.2%}/{REC_U56['Sharpe']}/{REC_U56['MaxDD']:.2%} OOS "
         f"{REC_U56['oos_Sharpe']}, tol 0.01", d8 < 0.01)

    # ================================================================ ARM A: the headline
    say("\n### ARM A -- THE STANDING RUNG (G = 0.60) RE-PRICED AT D / W / M / Q, "
        "both KEEP paths, every cost rung")
    for pname in D.panel.unique():
        say(f"\n   -- {pname} --   (4a is vs LIVE RULES v2; 4b is vs SPY)")
        say("   cad  cost |  RANK  CAGR   Sharpe    MaxDD    H1/H2      OOS Sh | turn/yr | "
            "4a   4b    failing 4b legs")
        for cad in CADENCES:
            for c in COSTS:
                d = D[(D.panel == pname) & (D.arm == "RANK") & (D.cadence == cad) &
                      (D.gross == STAND_G) & (D.cost == c)].iloc[0]
                say(f"   {cad:>3}  {c:4.0f} | {d.full_CAGR:7.2%} {d.full_Sharpe:8.4f} "
                    f"{d.full_MaxDD:8.2%} {d.h1_Sharpe:5.2f}/{d.h2_Sharpe:5.2f} "
                    f"{d.oos_Sharpe:8.4f} | {d.turnover_yr:6.2f} | "
                    f"{'Y' if d.keep4a else 'n'}    {'Y' if d.keep4b else 'n'}    {d.fail4b}")

    say("\n   4b PASS COUNT for the standing construction at G = 0.60, by (panel, cadence), "
        "over the 3 costed rungs {10,25,50} and over all 4 incl. 0:")
    st = D[(D.arm == "RANK") & (D.gross == STAND_G)]
    for pname in D.panel.unique():
        line = []
        for cad in CADENCES:
            d = st[(st.panel == pname) & (st.cadence == cad)]
            line.append(f"{cad} {int(d[d.cost > 0].keep4b.sum())}/3 ({int(d.keep4b.sum())}/4)")
        say(f"     {pname:>9}: " + "  ".join(line))

    # ================================================================ ARM B: the control
    say("\n### ARM B -- RANK minus the TURNOVER-MATCHED CONTROL, at every (cadence, cost). "
        "z = (RANK - median RAND) / sd(RAND); pct = RANK's percentile among the 12 seeds.")
    sep = []
    for pname in D.panel.unique():
        say(f"\n   -- {pname} --  G = {STAND_G}")
        say("   cad  cost |  RANK Sh   medRAND    diff       z    pct | "
            "turn RANK/RAND | NEUTRAL diff | RANK 4b / RAND 4b passes")
        for cad in CADENCES:
            for c in COSTS:
                d = D[(D.panel == pname) & (D.cadence == cad) & (D.gross == STAND_G) &
                      (D.cost == c)]
                rk = d[d.arm == "RANK"].iloc[0]
                rd = d[d.arm == "RAND"]
                m, sd = float(rd.full_Sharpe.median()), float(rd.full_Sharpe.std(ddof=1))
                z = (rk.full_Sharpe - m) / sd if sd > 0 else np.nan
                pct = float((rd.full_Sharpe < rk.full_Sharpe).mean())
                t = TN[(TN.panel == pname) & (TN.cadence == cad) & (TN.gross == STAND_G) &
                       (TN.cost == c)]
                nd = float(rk.full_Sharpe - t.rand_Sharpe_neutral.median())
                sep.append(dict(panel=pname, cadence=cad, cost=c, rank=rk.full_Sharpe,
                                med_rand=m, diff=rk.full_Sharpe - m, z=z, pct=pct,
                                neutral_diff=nd, turn_rank=rk.turnover_yr,
                                turn_rand=float(rd.turnover_yr.median()),
                                rank_4b=bool(rk.keep4b), rand_4b=int(rd.keep4b.sum()),
                                rank_oos=rk.oos_Sharpe, med_rand_oos=float(rd.oos_Sharpe.median())))
                say(f"   {cad:>3}  {c:4.0f} | {rk.full_Sharpe:8.4f} {m:9.4f} "
                    f"{rk.full_Sharpe - m:+9.4f} {z:+7.2f} {pct:5.2f} | "
                    f"{rk.turnover_yr:5.2f}/{float(rd.turnover_yr.median()):5.2f} | "
                    f"{nd:+12.4f} | {'Y' if rk.keep4b else 'n'} / {int(rd.keep4b.sum())}/12")
    SEP = pd.DataFrame(sep)

    # ================================================================ ARM C: 943's rebate
    say("\n### ARM C -- THE CADENCE GAIN, DECOMPOSED AGAINST ITS OWN SAME-CADENCE NULL "
        "(idea 943's turnover rebate). gain = Sharpe(cad) - Sharpe(W), same arm, same cost.")
    say("   If book_gain ~= null_gain the cadence dial is a rebate every book collects and the "
        "record must not read it as an edge.")
    reb_rows = []
    for pname in D.panel.unique():
        say(f"\n   -- {pname} --  G = {STAND_G}")
        say("   cad  cost |  RANK gain   NULL(med) gain    excess |  RANK OOS gain   NULL OOS gain")
        for cad in CADENCES:
            if cad == STAND_C: continue
            for c in COSTS:
                def pick(arm, seed, cd):
                    return D[(D.panel == pname) & (D.arm == arm) & (D.seed == seed) &
                             (D.cadence == cd) & (D.gross == STAND_G) & (D.cost == c)].iloc[0]
                rk_g = pick("RANK", -1, cad).full_Sharpe - pick("RANK", -1, STAND_C).full_Sharpe
                rk_o = pick("RANK", -1, cad).oos_Sharpe - pick("RANK", -1, STAND_C).oos_Sharpe
                ng = [pick("RAND", s, cad).full_Sharpe - pick("RAND", s, STAND_C).full_Sharpe
                      for s in range(NSEED)]
                no = [pick("RAND", s, cad).oos_Sharpe - pick("RAND", s, STAND_C).oos_Sharpe
                      for s in range(NSEED)]
                nm, nmo = float(np.median(ng)), float(np.median(no))
                reb_rows.append(dict(panel=pname, cadence=cad, cost=c, rank_gain=rk_g,
                                     null_gain=nm, excess=rk_g - nm, rank_oos_gain=rk_o,
                                     null_oos_gain=nmo, excess_oos=rk_o - nmo,
                                     null_gain_sd=float(np.std(ng, ddof=1))))
                say(f"   {cad:>3}  {c:4.0f} | {rk_g:+10.4f} {nm:+16.4f} {rk_g - nm:+9.4f} | "
                    f"{rk_o:+13.4f} {nmo:+15.4f}")
    REB = pd.DataFrame(reb_rows)

    # ================================================================ ARM D: rule 8
    say("\n### ARM D -- RULE 8. Parameters chosen on warm-up..2016-12-31 only; 2017-2026 read "
        "ONCE.  FREE picks (cadence, gross); FROZEN_W pins the standing weekly cadence.")
    piv = R8.pivot_table(index=["panel", "arm", "seed", "cost"], columns="mode",
                         values=["oos_Sharpe", "pick_cadence", "pick_gross", "keep4b", "keep4a"],
                         aggfunc="first")
    dfree = (piv[("oos_Sharpe", "FREE")] - piv[("oos_Sharpe", "FROZEN_W")]).astype(float)
    say(f"\n   d(OOS Sharpe) = FREE - FROZEN_W over all {len(dfree)} chooser cells: "
        f"mean {dfree.mean():+.4f}  SE {dfree.std(ddof=1)/np.sqrt(len(dfree)):.4f}  "
        f"t {dfree.mean()/(dfree.std(ddof=1)/np.sqrt(len(dfree))):+.2f}  "
        f"positive {int((dfree > 0).sum())}/{len(dfree)}  zero {int((dfree == 0).sum())}")
    for arm in ["RANK", "RAND", "SPYONLY"]:
        sub = dfree[dfree.index.get_level_values("arm") == arm]
        say(f"     {arm:>8}: n={len(sub)}  mean {sub.mean():+.4f}  "
            f"SE {sub.std(ddof=1)/np.sqrt(len(sub)) if len(sub) > 1 else float('nan'):.4f}  "
            f"positive {int((sub > 0).sum())}  negative {int((sub < 0).sum())}  "
            f"identical picks {int((sub == 0).sum())}")
    fr = R8[R8['mode'] == "FREE"]
    say("\n   FREE chooser's IS pick of CADENCE (how often the standing W is chosen in sample):")
    for arm in ["RANK", "RAND", "SPYONLY"]:
        vc = fr[fr.arm == arm].pick_cadence.value_counts()
        say(f"     {arm:>8}: " + "  ".join(f"{c} {int(vc.get(c, 0))}" for c in CADENCES))
    say("\n   RANK chooser rows in full (the capital-relevant ones):")
    say("   panel      cost mode      pick        IS Sh    OOS CAGR   OOS Sh   OOS MaxDD  "
        "4a 4b  failing 4b")
    for _, r in R8[R8.arm == "RANK"].sort_values(["panel", "cost", "mode"]).iterrows():
        say(f"   {r.panel:>9} {r.cost:5.0f} {r['mode']:<9} {r.pick_cadence}/{r.pick_gross:.2f}  "
            f"{r.is_Sharpe:8.4f} {r.oos_CAGR:9.2%} {r.oos_Sharpe:8.4f} {r.oos_MaxDD:9.2%}  "
            f"{'Y' if r.keep4a else 'n'}  {'Y' if r.keep4b else 'n'}   {r.fail4b}")
    say(f"\n   rule-8 4b passes by arm (of own n): " + "  ".join(
        f"{a} {int(R8[R8.arm == a].keep4b.sum())}/{len(R8[R8.arm == a])}"
        for a in ["RANK", "RAND", "SPYONLY"]))
    say(f"   rule-8 4a passes, ALL arms and modes: {int(R8.keep4a.sum())}/{len(R8)}")
    say(f"   published cells passing 4a: {int(D.keep4a.sum())}/{len(D)};  "
        f"passing 4b: {int(D.keep4b.sum())}/{len(D)}")

    # ---- binding-leg census, for continuity with the record's standing diagnosis
    say("\n   FAILING-4b-LEG SHARE by arm (share of that arm's failing published cells naming "
        "each leg):")
    for arm in ["RANK", "RAND", "SPYONLY"]:
        f = D[(D.arm == arm) & (~D.keep4b)]
        n = len(f)
        parts = {k: float(f.fail4b.str.contains(k).mean()) for k in
                 ["H1", "H2", "OOS", "DD", "CAGR"]}
        say(f"     {arm:>8} (n={n}): " + "  ".join(f"{k} {v:.4f}" for k, v in parts.items()))

    # ================================================================ write-out
    D.to_csv(f"{STEM}.grid.csv", index=False)
    R8.to_csv(f"{STEM}.walkforward.csv", index=False)
    TN.to_csv(f"{STEM}.turnover_neutral.csv.gz", index=False, compression="gzip")
    SEP.to_csv(f"{STEM}.separation.csv", index=False)
    REB.to_csv(f"{STEM}.cadence_rebate.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\n# gates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} passing")
    say(f"# elapsed {time.time() - t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
