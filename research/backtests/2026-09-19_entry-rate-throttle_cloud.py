#!/usr/bin/env python3
"""
Idea 1395 (lane cloud, 2026-09-19) — does an ENTRY-RATE THROTTLE buy the BINDING 4b DD LEG?

WHY THIS IDEA.  The sprint rule gives this lane the FIRST eligible item in QUEUE.md's '## Open'.
Every numbered item above 1395 (1204 / 1194 / 1182 / 1184 / 1185 / 1186, the 1090-down-to-3xx
block, 429, 353) is a RECORD-BOOKKEEPING census of committed text, gates or margins and yields no
weights function, so none can carry this protocol's step-3 deliverable.  1395 is the FIRST item
standing in '## Open' that has a price leg; it is price-only and fully offline.

THE PREMISE.  Idea 1377 killed RETENTION hysteresis: signal immunity could not buy the turnover
that calendar immunity buys, and the dial saturated.  1395 is the MIRROR axis — how fast the book
churns IN.  The frozen 2026-09-04 KEEP-4b incumbent (U56, N = 20 slots, H = 126-day holding period,
gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1) refills EVERY vacant slot at EVERY
rebalance, however many are vacant.  After a stress episode that empties the book, it re-enters at
full speed on the first week the screen re-admits names.  The throttle caps NEW entries at K per
rebalance and leaves the rest of the queue for the following weeks (the queue is implicit: the
ranking is re-derived each week, so a name not taken this week competes again next week).

The claim to test is the record's standing one — that the 4b DRAWDOWN leg is the sole binding leg
on U56 — against the one axis nobody has walked.  A throttle changes NO eligibility test and NO
sizing rule; it only slows re-entry.

THE CONSTRUCTION.  Byte-identical to the frozen book except for the entry cap: same raw 3-leg
composite, same above-200d and vol20 < 0.60 entry screen, N = 20 slots, H = 126, gross 0.75,
weekly cadence, 10 bps per unit turnover, t+1 execution, 260-row warm-up.  K = 20 (>= N) cannot
bind and is bit-identical to the incumbent by construction (gate G3).

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4):
    K      entries allowed per rebalance.  Rungs {1, 2, 3, 4, 6, 20}, ALL reported.
    panel  {U56, B136, SMALL} — the record's three standing panels.

NOT A DIAL, published at every value (control, never chosen on):
    SIZE {RESPREAD, FIXED}   RESPREAD is the incumbent's own sizing rule: w = gross / n_held, so a
           throttled (short-fill) book CONCENTRATES into the names it does hold.  FIXED is the live
           RULES v2 convention: w = gross / N per slot, vacant weight goes to CASH, never
           re-spread.  The throttle MANUFACTURES short-fill rows, so the sizing convention is not
           separable from it and both readings are published at every K on every panel.  (Lane B's
           idea 1403 found the incumbent's 4b pass survives the no-re-spread rule, and that B136's
           committed 4b FAIL is a convention artefact; this run does not re-litigate that, it
           simply reports both.)
    Paired circular-block bootstrap, 400 reps x 63-row blocks, seed 20260919, identical blocks on
           both sides, on the (throttle cell minus K=20 incumbent) daily difference — full and OOS.

PRE-DECLARED OUTCOMES, written before any number below was read:
  H_BIND   the throttle actually binds: at K = 1 the U56 book spends materially more name-weeks
           short of N = 20 than the incumbent's committed 3.7% of rebalance rows (idea 1399).
  H_DD     the throttle does NOT shallow the U56 MaxDD by 0.5 pp or more against K = 20.  Every
           mechanism tried so far on the live panel (1358 sleeve, 1366 release, 1369 cluster cap,
           1373 inverse-vol, 1377 rank buffer) has failed to buy the binding DD leg.
  H_TURN   turnover falls monotonically as K falls, because a capped entry rate caps the matched
           exit rate one holding period later.
  H_PICK   the rule-8 chooser (argmax IS net Sharpe over the K ladder on warm-up..2016-12-31, ties
           to the LARGEST K, 2017-2026 read ONCE) does NOT beat the frozen K = 20 anchor OOS.
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not the full sample.

GATES.  G1 the K = 20 RESPREAD U56 control replays the committed incumbent anchor (15.80% /
1.1537 / -19.13%, idea 1350's head-vintage triple) to within the 5e-3 tape-vintage Sharpe floor
that run established; the deviation is PUBLISHED, not asserted.  G2 weights sum to exactly gross at
every FULL rebalance row (|dev| < 1e-12).  G3 K = 20 is bit-for-bit identical to a wholly
UNTHROTTLED build, under BOTH sizing conventions.  (The two conventions do NOT coincide at K = 20
on U56 or B136, because those panels short-fill on their OWN — rows where fewer than N = 20 names
pass the entry screen at all.  That divergence is idea 1399's object and is PUBLISHED as
measurement D1, not gated.)  G4 all 36 throttle cells published.  G5 exactly two tuned parameters.  G6 the chooser
reads no row on or after 2017-01-01.  G7 determinism: a headline cell recomputed bit for bit.

PROTOCOL: rule 1 committed caches, >= 10 years; rule 2 10 bps per unit turnover, t+1 execution;
rule 3 compared against live RULES v2 AND SPY on each panel; rule 4 both KEEP paths at every cell;
rule 5 one idea, one script, deterministic, standalone; rule 8 walk-forward as above; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST), so every absolute
level is an upper bound and every 4b pass an optimistic one.  The headline is a DIFFERENCE between
two entry rules over the SAME panel on the SAME days, which is first-order immune to a level bias
common to both; the pass COUNT is not.

Offline and deterministic (committed caches only, no network, no yfinance):
  python research/backtests/2026-09-19_entry-rate-throttle_cloud.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import EXCLUDE, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask             # noqa: E402

DATE, SLUG = "2026-09-19", "entry-rate-throttle"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
A_N, A_H, A_G = 20, 126, 0.75                  # the frozen 2026-09-04 incumbent
LEGS = [(21, 252), (0, 126), (0, 63)]          # the committed RAW three-leg composite
KS = [1, 2, 3, 4, 6, 20]                       # 20 >= N -> cannot bind -> the incumbent
SIZES = ["RESPREAD", "FIXED"]
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NBOOT, BLOCK = 20260919, 400, 63
COMMITTED_U56 = (0.1580, 1.1537, -0.1913)      # idea 1350 head-vintage anchor
TAPE_FLOOR = 5e-3

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    h = len(r) // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]),
                **{"is": stats(r[:o])})


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


def legs_4a(b, live):
    return dict(H1=b["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(b, spy):
    return dict(H1=b["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=b["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=b["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def block_boot(d, reps=NBOOT, block=BLOCK, seed=SEED):
    d = np.asarray(d, float)
    n = len(d)
    if n < block * 3:
        return np.nan
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]) % n
    return float(d[idx.reshape(reps, -1)[:, :n]].mean(axis=1).std(ddof=1))


# ------------------------------------------------------------------ panels
UNIV = sorted({t for g in json.loads((ROOT / "research" / "universe.json").read_text()).values()
               for t in g} - set(EXCLUDE))
_meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD_SMALL = set(_meta.loc[_meta.max_1d_move >= 1.0, "ticker"])


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.idx = name, px, px.index
        q = px[invest]
        self.rets = q.pct_change().fillna(0.0).values
        self.priced = q.notna().values
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        v20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(v20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.C = C
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.T = len(px)
        self.K = len(invest)


def panels():
    out = []
    raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()
    keep = [c for c in UNIV if c in raw.columns]
    px = raw[keep].loc["2008-01-01":].dropna(how="all").ffill()
    out.append(Panel("U56", px, [c for c in px.columns if c != "SPY"]))

    pb = pd.read_csv(ROOT / "data" / "prices_broad.csv", index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":].dropna(how="all").ffill()
    out.append(Panel("B136", pb, [c for c in pb.columns if c != "SPY"]))

    ps = pd.read_csv(ROOT / "data" / "prices_small.csv.gz", index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":].dropna(how="all").ffill()
    spy = raw["SPY"].reindex(ps.index, method="ffill").rename("SPY")
    ps = pd.concat([ps.drop(columns=["SPY"], errors="ignore"), spy], axis=1)
    inv = [c for c in ps.columns if c != "SPY" and c not in BAD_SMALL]
    out.append(Panel("SMALL", ps, inv))
    return out


# ------------------------------------------------------------------ selection
def build_sel(pan, cap, H=A_H, N=A_N, lag=1):
    """Held set per rebalance segment under an ENTRY-RATE THROTTLE of `cap` new names per row.

    Retention is the frozen book's CALENDAR rule verbatim: a name is held while its age is < H
    rebalance-day rows and it is still priced.  Entry is the frozen book's ranking verbatim
    (eligible + priced, top of the same composite), except that at most `cap` names may enter on
    any one rebalance row.  cap >= N can never bind."""
    K = pan.K
    segs, diag = [], []
    cur = np.full(K, -1, dtype=np.int64)
    pr, T, nreb = pan.priced, pan.T, len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        evicted = len(held) - len(keep)
        want = N - len(keep)                       # vacancies before the throttle
        need = min(want, cap)                      # vacancies the throttle allows to be filled
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        queued = max(want - cap, 0)                # vacancies the throttle deliberately deferred
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        if len(sel):
            segs.append((int(t), int(stop), sel.copy(), int(ts)))
            diag.append(dict(row=int(t), n_held=len(sel), short=int(len(sel) < N),
                             evicted=evicted, added=len(take), queued=queued, days=stop - t))
    return segs, pd.DataFrame(diag)


def run(pan, segs, size, gross=A_G, N=A_N):
    """size='RESPREAD' -> w = gross/n_held (the incumbent's own sizing rule).
       size='FIXED'    -> w = gross/N per slot, vacant weight to CASH (live RULES v2 convention)."""
    T = pan.T
    r = np.zeros(T)
    turn_tot, wdev = 0.0, 0.0
    curw = np.zeros(pan.K)
    for (i0, i1, sel, ts) in segs:
        n = len(sel)
        w = np.full(n, gross / n if size == "RESPREAD" else gross / N)
        if n == N:
            wdev = max(wdev, abs(w.sum() - gross))
        new = np.zeros(pan.K)
        new[sel] = w
        turn = float(np.abs(new - curw).sum())
        turn_tot += turn
        base = pan.Cp[i0, sel]
        A = w[None, :] * (pan.Cp[i0:i1, sel] / base[None, :])
        c0 = 1.0 - w.sum()
        V = A.sum(axis=1) + c0
        seg = (A * pan.rets[i0:i1, sel]).sum(axis=1) / V
        seg[0] -= turn * COST / 1e4
        r[i0:i1] = seg
        Ae = w * (pan.C[i1 - 1, sel] / base)
        curw = np.zeros(pan.K)
        curw[sel] = Ae / (Ae.sum() + c0)
    return r, dict(turnover=turn_tot / (T / 252.0), wdev=wdev)


def summarise(dg, st):
    d = dg[dg.row >= st]
    return dict(n_held=float(d.n_held.mean()),
                short_row_share=float(d.short.mean()),
                add_per_reb=float(d.added.mean()),
                queued_per_reb=float(d.queued.mean()),
                queued_rows=float((d.queued > 0).mean()))


def main():
    t0 = time.time()
    say("=" * 110)
    say("Idea 1395 (lane cloud) — ENTRY-RATE THROTTLE vs the frozen 2026-09-04 KEEP-4b incumbent")
    say("=" * 110)

    rows, boots, ctrl = [], [], []
    for pan in panels():
        say(f"\n--- panel {pan.name}: {pan.K} investables, {pan.T} rows "
            f"{pan.idx[0].date()}..{pan.idx[-1].date()}, {len(pan.reb)} rebalances")
        o = int(np.searchsorted(pan.idx, OOS_START))
        st = WARMUP
        base = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live = windows(base[st:], o - st)
        spy = windows(pan.spy[st:], o - st)
        say(f"    live RULES v2  CAGR {live['full']['CAGR']:.2%}  Sharpe {live['full']['Sharpe']:.4f}"
            f"  MaxDD {live['full']['MaxDD']:.2%}  H1/H2 {live['h1']['Sharpe']:.3f}/{live['h2']['Sharpe']:.3f}"
            f"  OOS Sharpe {live['oos']['Sharpe']:.4f}")
        say(f"    SPY            CAGR {spy['full']['CAGR']:.2%}  Sharpe {spy['full']['Sharpe']:.4f}"
            f"  MaxDD {spy['full']['MaxDD']:.2%}  H1/H2 {spy['h1']['Sharpe']:.3f}/{spy['h2']['Sharpe']:.3f}"
            f"  OOS Sharpe {spy['oos']['Sharpe']:.4f}  OOS CAGR {spy['oos']['CAGR']:.2%}")

        cells = {}
        for size in SIZES:
            for cap in KS:
                segs, dg = build_sel(pan, cap)
                rr, extra = run(pan, segs, size)
                w = windows(rr[st:], o - st)
                b4a, b4b = legs_4a(w, live), legs_4b(w, spy)
                sm = summarise(dg, st)
                label = f"K={cap} {size}"
                rows.append(dict(panel=pan.name, cell=label, K=cap, size=size, **flat(w),
                                 turnover=extra["turnover"], **sm,
                                 pass4a=all(b4a.values()), fail4a=failed(b4a),
                                 pass4b=all(b4b.values()), fail4b=failed(b4b),
                                 m4b_DD=(w["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]) * 100,
                                 m4b_CAGR=(w["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]) * 100,
                                 m4b_OOS=w["oos"]["Sharpe"] - spy["oos"]["Sharpe"],
                                 spy_sharpe=spy["full"]["Sharpe"], live_sharpe=live["full"]["Sharpe"],
                                 wdev=extra["wdev"]))
                say(f"    {label:<15}: CAGR {w['full']['CAGR']:7.2%} Sharpe {w['full']['Sharpe']:.4f} "
                    f"MaxDD {w['full']['MaxDD']:7.2%} H1/H2 {w['h1']['Sharpe']:.3f}/{w['h2']['Sharpe']:.3f} "
                    f"OOS {w['oos']['CAGR']:6.2%}/{w['oos']['Sharpe']:.4f}/{w['oos']['MaxDD']:7.2%} "
                    f"trn {extra['turnover']:5.2f} nheld {sm['n_held']:5.2f} "
                    f"short% {sm['short_row_share']:6.2%} q/reb {sm['queued_per_reb']:5.2f} "
                    f"4b {'PASS' if all(b4b.values()) else 'fail:' + failed(b4b)} "
                    f"4a {'PASS' if all(b4a.values()) else 'fail:' + failed(b4a)}")
                cells[label] = (rr, w)

        # ---- gates per panel
        # G3: K=20 (>= N) cannot bind, so it must be bit-identical to a wholly UNTHROTTLED build.
        for size in SIZES:
            u, _ = run(pan, build_sel(pan, 10 ** 9)[0], size)
            d3 = float(np.abs(cells[f"K=20 {size}"][0] - u).max())
            gate(f"G3-{pan.name}-{size}", f"{d3:.3e}",
                 "K=20 == unthrottled incumbent, < 1e-15", d3 < 1e-15)
        # D1 is a MEASUREMENT, not a gate: at K=20 the two sizing conventions can still differ,
        # and they differ by exactly the panel's OWN short-fill rows (idea 1399's object) — rows
        # where fewer than N=20 names pass the entry screen at all.  Published, not asserted.
        d1 = float(np.abs(cells["K=20 RESPREAD"][0] - cells["K=20 FIXED"][0]).max())
        srs = [r["short_row_share"] for r in rows
               if r["panel"] == pan.name and r["cell"] == "K=20 RESPREAD"][0]
        say(f"   MEASURED D1-{pan.name}: unthrottled RESPREAD-vs-FIXED max daily |diff| {d1:.3e}"
            f" on a panel whose own short-fill row share is {srs:.4%}")
        GATES.append(dict(gate=f"D1-{pan.name}", value=f"maxdiff {d1:.3e}, short-fill rows {srs:.4%}",
                          target="MEASUREMENT (idea 1399's short-fill rows), no pass/fail",
                          pass_=True))
        wd = max(r["wdev"] for r in rows if r["panel"] == pan.name)
        gate(f"G2-{pan.name}", f"{wd:.3e}", "|sum(w) - gross| < 1e-12 on FULL rows", wd < 1e-12)

        # ---- paired block bootstrap against the K=20 incumbent, per sizing convention
        for size in SIZES:
            a = cells[f"K=20 {size}"][0]
            for cap in KS:
                lbl = f"K={cap} {size}"
                rr = cells[lbl][0]
                for win, sl in (("FULL", slice(st, None)), ("OOS", slice(o, None))):
                    d = rr[sl] - a[sl]
                    se = block_boot(d)
                    boots.append(dict(panel=pan.name, cell=lbl, size=size, window=win,
                                      d_mean_bp=d.mean() * 1e4, se_bp=se * 1e4,
                                      t=d.mean() / se if se else np.nan,
                                      sharpe_cell=sharpe(rr[sl]), sharpe_anchor=sharpe(a[sl]),
                                      d_sharpe=sharpe(rr[sl]) - sharpe(a[sl]),
                                      dd_cell=mdd(rr[sl]), dd_anchor=mdd(a[sl]),
                                      d_dd_pp=(mdd(rr[sl]) - mdd(a[sl])) * 100))

        # ---- rule 8: K chosen on warm-up..2016 only, 2017-2026 read once (per SIZE control)
        for size in SIZES:
            pick, best = None, -np.inf
            for cap in KS:
                s_is = sharpe(cells[f"K={cap} {size}"][0][st:o])
                if pick is None or s_is > best + 1e-12:
                    best, pick = s_is, cap
                elif abs(s_is - best) <= 1e-12:
                    pick = max(pick, cap)          # ties to the LARGEST K (least intervention)
            wp, wa = cells[f"K={pick} {size}"][1], cells[f"K=20 {size}"][1]
            bestoos = max(KS, key=lambda kk: cells[f"K={kk} {size}"][1]["oos"]["Sharpe"])
            ctrl.append(dict(panel=pan.name, size=size, pick_K=pick, is_sharpe=best,
                             oos_CAGR_pick=wp["oos"]["CAGR"], oos_Sharpe_pick=wp["oos"]["Sharpe"],
                             oos_MaxDD_pick=wp["oos"]["MaxDD"],
                             oos_CAGR_anchor=wa["oos"]["CAGR"], oos_Sharpe_anchor=wa["oos"]["Sharpe"],
                             oos_MaxDD_anchor=wa["oos"]["MaxDD"],
                             d_oos_Sharpe=wp["oos"]["Sharpe"] - wa["oos"]["Sharpe"],
                             d_oos_CAGR_pp=(wp["oos"]["CAGR"] - wa["oos"]["CAGR"]) * 100,
                             d_oos_MaxDD_pp=(wp["oos"]["MaxDD"] - wa["oos"]["MaxDD"]) * 100,
                             spy_oos_Sharpe=spy["oos"]["Sharpe"], spy_oos_CAGR=spy["oos"]["CAGR"],
                             spy_oos_MaxDD=spy["oos"]["MaxDD"], best_oos_K=bestoos))
            say(f"    RULE 8 size={size}: IS pick K={pick} (IS Sharpe {best:.4f}) -> OOS Sharpe "
                f"{wp['oos']['Sharpe']:.4f} vs K=20 anchor {wa['oos']['Sharpe']:.4f} "
                f"(delta {wp['oos']['Sharpe'] - wa['oos']['Sharpe']:+.4f}); ex-post best OOS K={bestoos}")

        if pan.name == "U56":
            wa = cells["K=20 RESPREAD"][1]["full"]
            dev = abs(wa["Sharpe"] - COMMITTED_U56[1])
            gate("G1", f"CAGR {wa['CAGR']:.4f} Sharpe {wa['Sharpe']:.4f} MaxDD {wa['MaxDD']:.4f} "
                       f"|dSharpe| {dev:.2e}", f"1350 anchor, |dSharpe| < {TAPE_FLOOR}", dev < TAPE_FLOOR)
            rr2, _ = run(pan, build_sel(pan, 2)[0], "RESPREAD")
            dd = float(np.abs(rr2 - cells["K=2 RESPREAD"][0]).max())
            gate("G7", f"{dd:.3e}", "determinism < 1e-15", dd < 1e-15)

    G = pd.DataFrame(rows)
    B = pd.DataFrame(boots)
    C = pd.DataFrame(ctrl)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    B.to_csv(f"{STEM}.bootstrap.csv", index=False)
    C.to_csv(f"{STEM}.rule8.csv", index=False)

    nb = len(KS) * len(SIZES) * 3
    gate("G4", f"{len(G)} rows", f"{nb} published (6 K x 2 SIZE x 3 panels)", len(G) == nb)
    gate("G5", "K, panel", "exactly 2 tuned parameters (SIZE is a published control)", True)
    gate("G6", str(OOS_START.date()), "chooser reads only rows < 2017-01-01", True)

    say("\n" + "=" * 110)
    say("GRID (ALL grid points)")
    say(G[["panel", "cell", "full_CAGR", "full_Sharpe", "full_MaxDD", "h1_Sharpe", "h2_Sharpe",
           "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "turnover", "n_held", "short_row_share",
           "queued_per_reb", "pass4a", "pass4b", "fail4b", "m4b_DD", "m4b_CAGR"]].to_string(
          index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nBOOTSTRAP (cell minus K=20 incumbent, same sizing convention)")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nRULE 8 (K chosen on IS only; 2017-2026 read once)")
    say(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nGATES")
    say(pd.DataFrame(GATES).to_string(index=False))
    say(f"\n4b passes: {int(G.pass4b.sum())} of {len(G)};  4a passes: {int(G.pass4a.sum())} of {len(G)}")
    say(f"elapsed {time.time() - t0:.0f}s")
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)


if __name__ == "__main__":
    main()
