#!/usr/bin/env python3
"""Idea 1284 (lane cloud, 2026-09-18): does a SECTOR or NAME CONCENTRATION CAP change the
STANDING G = 0.60 BOOK's 4b VERDICT?

THE PREMISE.  The record's single confirmed 4b candidate (memo
2026-09-18_standing-G060-selection-value_cloud.memo.md) is the U56 book: top N = 20 by the frozen
three-leg composite among names above their own 200d MA with vol20 < 0.60, min-hold H = 126,
EQUAL WEIGHT, gross 0.60 of NAV, weekly decide-Friday / trade-Monday.  Idea 1286 found its 4b
pass is carried by the DRAWDOWN leg: DD binds at 0.871 of the failures in that run's grid.  The
book has no cap on how many of its 20 slots come from one risk bucket, and no cap on how large
one name can get when fewer than 20 names are eligible -- which is exactly what happens in a
drawdown, when the 200d gate empties the eligible set.  A concentration cap is the cheapest
drawdown lever on the table and nobody has priced it.

THE TWO DIALS (PROTOCOL rule 4: max two tuned parameters).  Nothing else moves.
    DIAL 1  SECTOR CAP  S in {2, 3, 4, 6, 20}  -- the maximum number of the 20 slots that may be
            filled from ONE risk bucket.  S = 20 is OFF (the standing book).  The cap binds on
            NEW ADDS only; a name already inside its min-hold H is never forced out, because
            forcing it out would change the min-hold rule, which is frozen.
    DIAL 2  NAME CAP    C in {0.05, 0.0625, 0.075, 0.10, 1.00} -- the maximum weight of a single
            name as a fraction of the BOOK (multiply by gross for NAV weight: at G = 0.60,
            C = 0.05 is 3.0% of NAV).  C = 1.00 is OFF.  C = 0.05 is exactly 1/20 and therefore
            binds ONLY when fewer than 20 names are held, i.e. only inside a drawdown.  Weight
            cut by the cap goes to CASH -- de-gross, never re-spread, matching the live RULES v2
            clause.

    The (S = 20, C = 1.00) cell IS the standing book, bit for bit.  It is the control, and gate
    G2 checks it reproduces the memo's committed triple.  All 25 cells are reported.

FROZEN, not touched: the composite and its three legs (21/252, 0/126, 0/63 percentile ranks,
equal-weighted), eligibility (above own 200d MA AND vol20 < 0.60), N = 20, H = 126, weekly
decide-Friday cadence, gross 0.60, 260-row warm-up, PROTOCOL's 10 bps and t+1 fill.  Costs of
25 and 50 bps and a t+2 fill are reported as an ANNEX (the memo narrowed the book to "fills no
slower than t+2 at <= 50 bps") -- they are reporting, not tuning: no verdict is chosen on them.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) A CAP IMPROVES THE BINDING LEG -- some capped cell raises the DD-leg margin (MaxDD /
      SPY MaxDD) over the uncapped book WITHOUT losing any other 4b leg, and holds OOS under
      rule 8.  The book should be written with that cap.
  (B) THE CAP IS FREE BUT POINTLESS -- caps neither help nor hurt materially (the book is
      already diversified; the cap rarely binds).  Report the bind rate and leave the book alone.
  (C) THE CAP COSTS MORE THAN IT BUYS -- capped cells cut MaxDD but lose the CAGR or a Sharpe
      leg, so 4b fails where the uncapped book passed.
  (D) THE CAP IS A TUNING TRAP -- the best IS cell is not the best OOS cell and the rule-8 arm
      loses Sharpe against the frozen uncapped book.  Freeze the book as it stands.

THE RULE-8 ARM (PROTOCOL rule 8, required).  Both dials are chosen on warm-up..2016-12-31 ONLY
-- highest IS Sharpe among cells passing all four IS-computable 4b legs, fallback (declared in
advance) highest IS Sharpe -- and 2017-2026 is read ONCE.  The question asked directly: does a
chooser that is ALLOWED to move the caps beat the frozen uncapped book out of sample?

PANELS.  U56 is the panel the standing book lives on and the only one carrying the sector cap:
the repo holds NO sector labels for the 136-name broad list or the sub-$2B screen, so on B135 and
SMALL only DIAL 2 (the name cap) runs and DIAL 1 is reported as UNAVAILABLE rather than guessed.
The U56 bucket map is STATIC, hand-assigned from public sector membership, written in this file,
and identical in every window -- it is frozen, not tuned, and it is not a third dial.

SURVIVORSHIP (rule 9).  U56 (55 investables) and B135 are CURRENT-constituent lists; SMALL is a
current sub-$2B screen with the house `max_1d_move >= 1.0` filter applied FIRST.  Every absolute
level (CAGR, Sharpe, MaxDD, and every 4a/4b verdict built on them) is an UPPER bound.  The
WITHIN-grid differences this run is actually about -- capped cell minus uncapped cell on the SAME
panel, same names, same dates -- are first-order immune to that bias, and are the quoted result.

Deterministic, offline, no network.  Run: python3 <this file>
"""
import sys, time, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE = "2026-09-18"
SLUG = "does-a-SECTOR-or-NAME-CONCENTRATION-CAP-change-the-STANDING-G-0.60-BOOK-s-4b-VERDICT"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_C, A_G = 20, 126, "W", 0.60           # frozen book: N, min-hold, cadence, gross
LEGS = [(21, 252), (0, 126), (0, 63)]
SCAPS = [2, 3, 4, 6, 20]                          # DIAL 1 (20 = OFF)
NCAPS = [0.05, 0.0625, 0.075, 0.10, 1.00]         # DIAL 2 (1.00 = OFF)
OFF = (20, 1.00)                                  # the standing book
COSTS = [10.0, 25.0, 50.0]                        # 10 = PROTOCOL; rest = annex
DELAYS = [1, 2]                                   # t+1 = PROTOCOL; t+2 = annex
_LOG, GATES = [], []

# ---- STATIC risk-bucket map for U56 (frozen; hand-assigned from public sector membership) ----
BUCKETS = {
    "TECH":      ["XLK", "SMH", "AAPL", "MSFT", "NVDA", "AVGO", "AMD", "CRM", "ORCL", "PLTR"],
    "COMM_DISC": ["XLY", "XLC", "ITB", "AMZN", "TSLA", "GOOGL", "META", "NFLX"],
    "FIN":       ["XLF", "KRE", "JPM", "V", "BRK-B"],
    "HEALTH":    ["XLV", "XBI", "LLY", "UNH"],
    "ENERGY":    ["XLE", "XOM", "USO", "UNG"],
    "MATERIALS": ["XLB", "GDX", "GLD", "SLV"],
    "STAPLES":   ["XLP", "COST"],
    "INDUSTRY":  ["XLI"],
    "UTIL":      ["XLU"],
    "REALEST":   ["XLRE"],
    "EQ_BROAD":  ["QQQ", "IWM", "DIA", "EFA", "EEM", "VTI", "RSP"],
    "BONDS":     ["TLT", "IEF", "SHY", "HYG", "LQD", "TIP"],
    "FX_CMDTY":  ["UUP", "DBC"],
}
TICK2BUCKET = {t: b for b, ts in BUCKETS.items() for t in ts}


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


# ---------------------------------------------------------------- panel
class Panel:
    def __init__(self, name, px, invest, bucket_of=None):
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
        if bucket_of is None:
            self.bucket = None
        else:
            names = sorted({bucket_of[t] for t in invest})
            self.bucket = np.array([names.index(bucket_of[t]) for t in invest])
            self.nbucket = len(names)
            self.bucket_names = names


def build(pan, scap, ncap):
    """The standing book with DIAL 1 (sector cap on new adds) and DIAL 2 (per-name weight cap,
    excess to cash).  Returns (weights T x M, n_bind_sector, n_bind_name, n_reb)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    bind_s = bind_n = 0
    use_s = (pan.bucket is not None) and (scap < A_N)
    for i, t in enumerate(pan.reb):
        ts = max(t - 1, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held): held = held[pr[t, held]]
        keep = [int(c) for c in (held[(t - cur[held]) < A_H] if len(held) else held)]
        k = pan.key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        for c in keep: k[c] = np.inf
        bcount = None
        if use_s:
            bcount = np.zeros(pan.nbucket, dtype=np.int64)
            for c in keep: bcount[pan.bucket[c]] += 1
        need, take, blocked = A_N - len(keep), [], False
        for c in np.argsort(k, kind="stable"):
            if need <= 0: break
            c = int(c)
            if not np.isfinite(k[c]): break
            if use_s:
                b = pan.bucket[c]
                if bcount[b] >= scap:
                    blocked = True
                    continue
                bcount[b] += 1
            take.append(c); need -= 1
        if blocked: bind_s += 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep: new[c] = cur[c]
        for c in take: new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel): continue
        w = min(1.0 / len(sel), ncap)
        if w < 1.0 / len(sel) - 1e-15: bind_n += 1
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = w
    return W, bind_s, bind_n, nreb


def run_raw(pan, Wt, gross, delay):
    """Gross-of-cost return path and turnover.  Costs are applied OUTSIDE so every cost rung
    comes from ONE run (the cost term is exactly linear in turnover)."""
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


def spy_path(pan, delay):
    W = np.zeros((len(pan.idx), pan.rets.shape[1])); W[:, pan.ispy] = 1.0
    r, _ = run_raw(pan, W, 1.0, delay)
    return r


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
    say(f"# {DATE} idea 1284 lane cloud -- {SLUG}")
    say(f"# DIAL 1 SECTOR CAP = {SCAPS} (20 = OFF);  DIAL 2 NAME CAP = {NCAPS} (1.00 = OFF)")
    say(f"# frozen: N={A_N} H={A_H} cadence={A_C} gross={A_G} elig=above200d & vol20<{MAXVOL} "
        f"warm-up={WARMUP}")
    say(f"# PROTOCOL cell = 10 bps, t+1.  ANNEX (reporting only): costs {COSTS}, delays "
        f"{['t+%d' % d for d in DELAYS]}")
    say("")

    # ---------------- panels
    panels = []
    px = load_universe()
    inv = [c for c in px.columns if c != "SPY"]
    miss = [t for t in inv if t not in TICK2BUCKET]
    gate("G0 bucket map covers every U56 investable", f"{len(inv) - len(miss)}/{len(inv)}"
         + (f" missing={miss}" if miss else ""), f"{len(inv)}/{len(inv)}", not miss)
    panels.append(Panel("U56", px, inv, TICK2BUCKET))

    pxb = load_universe(broad=True)
    invb = [c for c in pxb.columns if c != "SPY"]
    panels.append(Panel(f"B{len(invb)}", pxb, invb, None))

    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    invs = [c for c in pxs.columns if c != "SPY" and c not in bad]
    say(f"# SMALL: house filter drops {len([c for c in pxs.columns if c in bad])} names on "
        f"max_1d_move >= 1.0; {len(invs)} kept")
    panels.append(Panel(f"SMALL{len(invs)}", pxs, invs, None))

    for p in panels:
        say(f"# panel {p.name}: {len(p.invest)} investables, {len(p.idx)} rows "
            f"{p.idx[0].date()}..{p.idx[-1].date()} (scored from {p.idx[WARMUP].date()} after "
            f"the {WARMUP}-row warm-up), {len(p.reb)} rebalances")
    say("")

    # ---------------- gate G1: fast runner == engine.backtest
    pan = panels[0]
    Wt, _, _, _ = build(pan, *OFF)
    r_fast, turn = run_raw(pan, Wt, A_G, 1)
    wdf = pd.DataFrame(np.roll(A_G * Wt, -1, axis=0), index=pan.idx, columns=pan.px.columns)
    eng = backtest(pan.px, wdf, cost_bps=10.0, freq=A_C)["returns"].fillna(0.0).values
    d = float(np.abs((r_fast - turn * 10.0 / 1e4)[WARMUP:] - eng[WARMUP:]).max())
    gate("G1 fast runner == engine.backtest (uncapped book, 10 bps)", f"{d:.3e}", "< 1e-12",
         d < 1e-12)

    # ---------------- gate G2: the OFF cell reproduces the STANDING BOOK's committed numbers
    idx = pan.idx[WARMUP:]
    rows_spy = {dly: windows(idx, pan.spy[WARMUP:]) for dly in DELAYS}
    w_off = windows(idx, r_fast[WARMUP:] - turn[WARMUP:] * 10.0 / 1e4)
    # idea 1286's committed U56 RANK G=0.60 row at 10 bps / t+1 (its grid.csv, same repo)
    COMMITTED = dict(CAGR=0.125911, Sharpe=1.151737, MaxDD=-0.155135)
    dd = max(abs(w_off["full"][k] - v) for k, v in COMMITTED.items())
    gate("G2 OFF cell reproduces idea 1286's committed U56 G=0.60 10bps t+1 row",
         f"max|d| {dd:.2e} (CAGR {w_off['full']['CAGR']:.6f} Sharpe "
         f"{w_off['full']['Sharpe']:.6f} MaxDD {w_off['full']['MaxDD']:.6f})", "< 1e-4",
         dd < 1e-4)
    say(f"   OFF cell U56 10bps t+1: full CAGR {w_off['full']['CAGR']:.4f} Sharpe "
        f"{w_off['full']['Sharpe']:.4f} MaxDD {w_off['full']['MaxDD']:.4f} | halves "
        f"{w_off['h1']['Sharpe']:.4f}/{w_off['h2']['Sharpe']:.4f} | OOS "
        f"{w_off['oos']['CAGR']:.4f}/{w_off['oos']['Sharpe']:.4f}/{w_off['oos']['MaxDD']:.4f}")
    l4b_off = legs_4b(w_off, rows_spy[1])
    gate("G2b OFF cell is a 4b PASS (the standing book, U56 10bps t+1)",
         f"legs {l4b_off}", "all True", all(l4b_off.values()))

    # ---------------- the grid
    recs = []
    for pan in panels:
        scaps = SCAPS if pan.bucket is not None else [20]
        if pan.bucket is None:
            say(f"# {pan.name}: DIAL 1 UNAVAILABLE (no sector labels in repo for this panel); "
                f"DIAL 2 only")
        idx = pan.idx[WARMUP:]
        spyw = {d: windows(idx, pan.spy[WARMUP:]) for d in DELAYS}
        live = {}
        for c in COSTS:
            lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=c,
                          freq=A_C)["returns"].fillna(0.0).values[WARMUP:]
            lw_ = windows(idx, lr)
            for d in DELAYS: live.setdefault(d, {})[c] = lw_
        for s in scaps:
            for c in NCAPS:
                Wt, bs, bn, nr = build(pan, s, c)
                for dly in DELAYS:
                    raw, tn = run_raw(pan, Wt, A_G, dly)
                    raw, tn = raw[WARMUP:], tn[WARMUP:]
                    tpy = tn.sum() / (len(raw) / 252.0)
                    for cost in COSTS:
                        w = windows(idx, raw - tn * cost / 1e4)
                        a = legs_4a(w, live[dly][cost]); b = legs_4b(w, spyw[dly])
                        recs.append(dict(
                            panel=pan.name, scap=s, ncap=c, delay=dly, cost=cost,
                            bind_s=bs / nr, bind_n=bn / nr, turns=tpy,
                            CAGR=w["full"]["CAGR"], Sharpe=w["full"]["Sharpe"],
                            MaxDD=w["full"]["MaxDD"], H1=w["h1"]["Sharpe"], H2=w["h2"]["Sharpe"],
                            IS_S=w["is_"]["Sharpe"], OOS_CAGR=w["oos"]["CAGR"],
                            OOS_S=w["oos"]["Sharpe"], OOS_DD=w["oos"]["MaxDD"],
                            is_h1=w["is_h1"], is_h2=w["is_h2"], IS_DD=w["is_"]["MaxDD"],
                            IS_CAGR=w["is_"]["CAGR"],
                            DDratio=w["full"]["MaxDD"] / spyw[dly]["full"]["MaxDD"],
                            CAGRratio=w["full"]["CAGR"] / spyw[dly]["full"]["CAGR"],
                            pass4a=all(a.values()), fail4a=failed(a),
                            pass4b=all(b.values()), fail4b=failed(b),
                            is4b=all(legs_4b_is(w, spyw[dly]).values())))
        say(f"# {pan.name} done  ({time.time() - t0:.0f}s)")
    G = pd.DataFrame(recs)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    say(f"\n# GRID: {len(G)} cells written to {Path(STEM).name}.grid.csv\n")

    # ---------------- report: every cell at the PROTOCOL rung
    for pan in panels:
        sub = G[(G.panel == pan.name) & (G.cost == 10.0) & (G.delay == 1)]
        sw = windows(pan.idx[WARMUP:], pan.spy[WARMUP:])
        say(f"## {pan.name} -- PROTOCOL rung (10 bps, t+1).  SPY full "
            f"{sw['full']['CAGR']:.2%}/{sw['full']['Sharpe']:.4f}/{sw['full']['MaxDD']:.2%}, "
            f"OOS S {sw['oos']['Sharpe']:.4f}")
        say(f"{'S':>3} {'C':>7} {'bindS':>6} {'bindN':>6} {'turn':>5} {'CAGR':>7} {'Shrp':>7} "
            f"{'MaxDD':>7} {'H1':>7} {'H2':>7} {'OOS_S':>7} {'DD/SPY':>7} {'4a':>3} {'4b':>3} "
            f"{'fail4b'}")
        for _, r in sub.iterrows():
            say(f"{r.scap:>3.0f} {r.ncap:>7.4f} {r.bind_s:>6.3f} {r.bind_n:>6.3f} "
                f"{r.turns:>5.2f} {r.CAGR:>7.2%} {r.Sharpe:>7.4f} {r.MaxDD:>7.2%} "
                f"{r.H1:>7.4f} {r.H2:>7.4f} {r.OOS_S:>7.4f} {r.DDratio:>7.4f} "
                f"{'Y' if r.pass4a else 'n':>3} {'Y' if r.pass4b else 'n':>3} {r.fail4b}")
        say("")

    # ---------------- the OFF-cell delta table (the within-grid result)
    say("## DELTA vs the UNCAPPED standing book (same panel, same dates, same cost/delay)")
    say(f"{'panel':>10} {'cost':>5} {'dly':>4} {'S':>3} {'C':>7} {'dSharpe':>8} {'dMaxDD':>8} "
        f"{'dCAGR':>8} {'dOOS_S':>8} {'4b':>3}")
    for (p, cost, dly), sub in G.groupby(["panel", "cost", "delay"]):
        off = sub[(sub.scap == OFF[0]) & (sub.ncap == OFF[1])].iloc[0]
        for _, r in sub.iterrows():
            if r.scap == OFF[0] and r.ncap == OFF[1]: continue
            say(f"{p:>10} {cost:>5.0f} {dly:>4.0f} {r.scap:>3.0f} {r.ncap:>7.4f} "
                f"{r.Sharpe - off.Sharpe:>+8.4f} {r.MaxDD - off.MaxDD:>+8.4f} "
                f"{r.CAGR - off.CAGR:>+8.4f} {r.OOS_S - off.OOS_S:>+8.4f} "
                f"{'Y' if r.pass4b else 'n':>3}")
    say("")

    # ---------------- rule 8: choose both dials IS, read OOS once
    say("## RULE 8 -- both dials chosen on warm-up..2016 ONLY, 2017-2026 read ONCE")
    say(f"{'panel':>10} {'cost':>5} {'dly':>4} {'chosen S/C':>12} {'via':>9} {'IS_S':>7} "
        f"{'OOS_S':>7} {'frozen OOS_S':>13} {'d(OOS_S)':>9} {'OOS CAGR':>9} {'OOS DD':>8}")
    r8 = []
    for (p, cost, dly), sub in G.groupby(["panel", "cost", "delay"]):
        off = sub[(sub.scap == OFF[0]) & (sub.ncap == OFF[1])].iloc[0]
        ok = sub[sub.is4b]
        via = "4b-IS" if len(ok) else "maxIS-S"
        pick = (ok if len(ok) else sub).sort_values(
            ["IS_S", "scap", "ncap"], ascending=[False, True, True]).iloc[0]
        d = pick.OOS_S - off.OOS_S
        r8.append(dict(panel=p, cost=cost, delay=dly, scap=pick.scap, ncap=pick.ncap, via=via,
                       d_oos=d, oos=pick.OOS_S, frozen=off.OOS_S, moved=not (
                           pick.scap == OFF[0] and pick.ncap == OFF[1])))
        say(f"{p:>10} {cost:>5.0f} {dly:>4.0f} {pick.scap:>5.0f}/{pick.ncap:<6.4f} {via:>9} "
            f"{pick.IS_S:>7.4f} {pick.OOS_S:>7.4f} {off.OOS_S:>13.4f} {d:>+9.4f} "
            f"{pick.OOS_CAGR:>9.2%} {pick.OOS_DD:>8.2%}")
    R8 = pd.DataFrame(r8)
    R8.to_csv(f"{STEM}.rule8.csv", index=False)
    dv = R8.d_oos.values
    se = dv.std(ddof=1) / np.sqrt(len(dv)) if len(dv) > 1 else np.nan
    say(f"\n   d(OOS Sharpe) CHOOSER - FROZEN over {len(dv)} cells: mean {dv.mean():+.4f}, "
        f"SE {se:.4f}, t {dv.mean() / se if se else float('nan'):+.2f}; "
        f"positive {int((dv > 0).sum())} / negative {int((dv < 0).sum())} / "
        f"identical {int((dv == 0).sum())}; chooser MOVED off the uncapped book at "
        f"{int(R8.moved.sum())} of {len(R8)} cells")
    gate("G3 rule-8 arm produced a chooser at every cell", f"{len(R8)}",
         f"{G.groupby(['panel', 'cost', 'delay']).ngroups}",
         len(R8) == G.groupby(['panel', 'cost', 'delay']).ngroups)

    # ---------------- headline counts
    say("")
    u = G[(G.panel == "U56") & (G.cost == 10.0) & (G.delay == 1)]
    off = u[(u.scap == OFF[0]) & (u.ncap == OFF[1])].iloc[0]
    better_dd = u[(u.MaxDD > off.MaxDD + 1e-12)]
    clean = better_dd[better_dd.pass4b]
    say(f"## HEADLINE (U56, PROTOCOL rung).  Uncapped book: MaxDD {off.MaxDD:.2%}, Sharpe "
        f"{off.Sharpe:.4f}, CAGR {off.CAGR:.2%}, OOS S {off.OOS_S:.4f}")
    say(f"   cells with a SHALLOWER MaxDD than uncapped: {len(better_dd)} of {len(u) - 1}; "
        f"of those still passing 4b: {len(clean)}")
    if len(clean):
        bb = clean.sort_values("MaxDD", ascending=False).iloc[0]
        say(f"   best DD among 4b-passing capped cells: S={bb.scap:.0f} C={bb.ncap:.4f} -> "
            f"MaxDD {bb.MaxDD:.2%} (d {bb.MaxDD - off.MaxDD:+.2%}), Sharpe {bb.Sharpe:.4f} "
            f"(d {bb.Sharpe - off.Sharpe:+.4f}), CAGR {bb.CAGR:.2%} "
            f"(d {bb.CAGR - off.CAGR:+.2%}), OOS S {bb.OOS_S:.4f} "
            f"(d {bb.OOS_S - off.OOS_S:+.4f})")
    say(f"   4b PASS rate over the whole grid: {int(G.pass4b.sum())} of {len(G)}; "
        f"4a PASS rate: {int(G.pass4a.sum())} of {len(G)}")
    for p, sub in G.groupby("panel"):
        say(f"      {p}: 4b {int(sub.pass4b.sum())}/{len(sub)}, 4a {int(sub.pass4a.sum())}/"
            f"{len(sub)}; most common 4b failure: "
            f"{sub[~sub.pass4b].fail4b.value_counts().idxmax() if (~sub.pass4b).any() else '-'}")

    say(f"\n# GATES: {sum(g['pass_'] for g in GATES)}/{len(GATES)} pass")
    say(f"# elapsed {time.time() - t0:.0f}s")
    Path(f"{STEM}.log.txt").write_text("\n".join(_LOG) + "\n")
    Path(f"{STEM}.gates.json").write_text(json.dumps(GATES, indent=1) + "\n")


if __name__ == "__main__":
    main()
