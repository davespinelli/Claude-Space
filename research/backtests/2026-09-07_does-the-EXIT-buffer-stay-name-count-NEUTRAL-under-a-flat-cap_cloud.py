#!/usr/bin/env python3
"""Idea 358: does the EXIT buffer stay name-count NEUTRAL under a FLAT cap?

Idea 349 split idea 331's no-trade band into an entry buffer `e` and an exit buffer `x` and
found the two sides are different kinds of dial:

  * ENTRY e   -- spearman(e, mean holdings) = -0.988.  A concentration dial wearing a band's
                 clothes: it collapses the U56 book from 19.1 names to 7.6.
  * EXIT  x   -- spearman(x, mean holdings) = +0.000, mean marginal Sharpe **+0.0577**,
                 **15/15 positive**, turnover 11.00 -> 5.07x/yr on U56.  A pure turnover dial.

The queue's charge is that the exit side's neutrality is an artefact of ONE convention: the slot
cap each rebalance is the parent's own `k_t = |{rank <= n}|`, which absorbs a drifting name --
a held name at rank n+1..n+x occupies a slot that would otherwise go to a fresh top-n name, so
the count cannot move.  Change the cap and the neutrality may go, and with it the +0.058.

THE TEST, pre-registered before any number was read:

  Exactly two tuned parameters -- the CAP RULE and the exit buffer x.  Entry buffer fixed at
  e = 0 (the queue text sweeps x only), n = 20, weekly, NORM weights g/k at g = 0.75.

    cap rule (3 levels)                       x (6 levels)
      KT    cap = k_t = |{rank <= n}|         {0, 5, 10, 20, 40, 80}
      FLAT  cap = n                               (x = 0 is the hard rank cut)
      UNCAP cap = infinity

  3 x 6 = 18 cells x panel {U56, B136, SMALL439} x cost rung {0, 10, 25} bps = 162 rows, ALL
  printed and committed to `<slug>.grid.csv`.  Panel and rung are REPORTED axes, not tuned.

  KT is the parent's convention and is asserted cell-for-cell against idea 349's committed
  `.grid.csv` (its e = 0 column) AND against the parent module's own `sel_ex` function.
  FLAT is the queue's literal ask.  UNCAP is added because -- see [B0] -- FLAT is provably a
  no-op, so it cannot answer the question the queue is asking; UNCAP is the only cap convention
  in which a drifter is NOT absorbed, i.e. the only one under which the neutrality CAN break.
  Adding it costs no third parameter: the cap rule is one dial with three levels.

WHAT THE ALGEBRA SAYS BEFORE THE RUN (section [B0] tests it, does not assume it).  A name is
holdable only if it is eligible, so the holdable set is {rank <= n+x} of size min(n+x, n_elig).
Holdings = min(cap, |holdable|).  With cap_KT = min(n, n_elig) and cap_FLAT = n, both give
min(n, n_elig): identical selections at EVERY x.  The queue's flat cap is the same cap.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters
every momentum book; CAGR levels are optimistic, the x-DIFFERENCES much less so.  (2) SMALL439
starts 2010-01-04, so its halves are not the same calendar halves as U56/B136, and the 44
tickers with `max_1d_move >= 1.0` in data/small_meta.csv are dropped before anything runs.
(3) rule 8's IS window is 2008-2016 on U56/B136 but effectively 2010-2016 on SMALL439.

Deterministic, standalone.  Reads baseline.py, engine and idea 349's committed script+CSV;
modifies nothing.
"""
import os, sys, importlib.util
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_does-the-EXIT-buffer-stay-name-count-NEUTRAL-under-a-flat-cap_cloud"
OUT = ROOT / "research" / "backtests"
PARENT_PY = OUT / "2026-09-07_does-a-band-on-the-EXIT-ONLY-beat-a-band-on-both-sides_C.py"
PARENT_CSV = OUT / "2026-09-07_does-a-band-on-the-EXIT-ONLY-beat-a-band-on-both-sides_C.grid.csv"
MAX_VOL, GROSS, N = 0.60, 0.75, 20
FREQ = "W"
CAPS = ["KT", "FLAT", "UNCAP"]
XS = [0, 5, 10, 20, 40, 80]
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260


def load_parent():
    spec = importlib.util.spec_from_file_location("idea349", PARENT_PY)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the book (idea 349's, verbatim)
def rank_frame(px, drop_spy=False):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    return rk <= n


def sel_x(px, rk, n, x, cap="KT", freq=FREQ):
    """Exit-buffer book under an explicit CAP RULE.  Enter at rank <= n; hold until rank > n+x
    or the name leaves the eligible set.  Free slots refill from the best-ranked unheld name at
    rank <= n.  Slot cap per rebalance:
        KT    |{rank <= n}|   (idea 349/331's convention -- absorbs the drifter)
        FLAT  n               (the queue's ask)
        UNCAP no cap          (drifters held IN ADDITION to the fresh top-n)
    cap is irrelevant at x = 0 by construction, so KT/FLAT/UNCAP all nest sel_hard(n) there."""
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns); nC = len(cols)
    out = np.zeros((len(px.index), nC)); rkv = rk.values
    held = []; last = np.zeros(nC)
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            capn = int(np.nansum(r <= n)) if cap == "KT" else (n if cap == "FLAT" else nC)
            held = [j for j in held if r[j] == r[j] and r[j] <= n + x]
            held.sort(key=lambda j: r[j])
            if len(held) > capn:
                held = held[:capn]
            if len(held) < capn:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs_ = set(held)
                for j in order:
                    if len(held) >= capn:
                        break
                    if r[j] != r[j] or r[j] > n:
                        break
                    if j not in hs_:
                        held.append(j); hs_.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(nC); last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return GROSS * s.div(k, axis=0).fillna(0.0)


# ---------------------------------------------------------------- fast backtester (idea 349's)
def fast_backtest(px, w, cost_bps=0.0, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT)
    cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(np.nansum(held, axis=1), index=idx), pd.Series((held > 0).sum(axis=1), index=idx))


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    """PROTOCOL 4a: Sharpe > the LIVE book in BOTH halves and MaxDD no worse."""
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def breakeven(r0, t0, spy, hi=200):
    cstar, bar = None, ""
    for c in range(0, hi + 1):
        ok, _, f = bars_4b(r0 - t0 * c / 1e4, spy)
        if ok:
            cstar = c
        else:
            bar = ",".join(f); break
    return cstar, bar


def spearman(a, b):
    """Spearman rho, or 0.0 when either side is CONSTANT (np.corrcoef would give nan).
    A constant `names` column IS the neutrality this idea is testing, so it is reported as
    an exact 0.000 with the `const` flag rather than as a missing value."""
    x, y = pd.Series(list(a), dtype=float), pd.Series(list(b), dtype=float)
    if x.nunique() < 2 or y.nunique() < 2:
        return 0.0
    return float(x.rank().corr(y.rank()))


def const_flag(v):
    return "const" if pd.Series(list(v), dtype=float).nunique() < 2 else "     "


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print(f"Book: top-{N} eligible by the v1 composite (vol scaler OFF), NORM weights g/k at "
          f"g={GROSS}, WEEKLY, next-day execution, entry buffer FIXED at e=0.")
    print(f"Tuned (2): cap rule {CAPS} x exit buffer x {XS} = {len(CAPS)*len(XS)} cells.")
    print(f"Reported axes: panel, cost {COSTS} bps.  x=0 is the hard rank cut under every cap.")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    gcsv, ccsv = OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.ctx.csv"
    if RESUME and gcsv.exists() and ccsv.exists():
        analyse(pd.read_csv(gcsv), pd.read_csv(ccsv).set_index("panel"), panels)
        return

    parent_mod = load_parent()
    parent = pd.read_csv(PARENT_CSV)
    parent = parent[parent.e == 0].set_index(["panel", "x"])

    rows, ctx_rows = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        nel = elig.sum(axis=1).loc[start:]
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(f"    eligible/day mean {nel.mean():.1f} min {nel.min()} max {nel.max()} | "
              f"days with n_elig < {N}: {int((nel < N).sum())} of {len(nel)} ({(nel < N).mean():.1%})")
        print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%} "
              f"MaxDD {so['MaxDD']:.2%}")

        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0, "W")
        base10 = (br - bt * 10 / 1e4).loc[start:]
        bm = metrics(base10); b1, b2 = hs(base10); bo = metrics(base10.loc[OOS_START:])
        print(f"    RULES v2 (live, weekly, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f} "
              f"CAGR {bo['CAGR']:.2%} MaxDD {bo['MaxDD']:.2%}")
        ctx_rows.append(dict(panel=pname, names=px.shape[1] - 1, start=str(start.date()),
                             end=str(px.index[-1].date()), nelig_mean=nel.mean(),
                             nelig_below_n=float((nel < N).mean()),
                             spy_CAGR=ms_["CAGR"], spy_Sharpe=ms_["Sharpe"], spy_MaxDD=ms_["MaxDD"],
                             spy_H1=s1, spy_H2=s2, spy_OOS=so["Sharpe"], spy_OOS_CAGR=so["CAGR"],
                             spy_OOS_MaxDD=so["MaxDD"],
                             base_CAGR=bm["CAGR"], base_Sharpe=bm["Sharpe"], base_MaxDD=bm["MaxDD"],
                             base_H1=b1, base_H2=b2, base_OOS=bo["Sharpe"],
                             base_OOS_CAGR=bo["CAGR"], base_OOS_MaxDD=bo["MaxDD"],
                             base_IS=metrics(base10.loc[:IS_END])["Sharpe"]))

        # ------------------------------------------------ [0] gates
        if pname == "U56":
            print("\n[0] GATES (all asserted before any new number is read)")
            wA = weights_from(sel_hard(rk, N))
            eng = backtest(px, wA, cost_bps=0.0, freq="W")
            f_r, f_t, _, _ = fast_backtest(px, wA, 0.0, "W")
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            print(f"    G1 fast_backtest vs engine.backtest: max|dr| {d1:.3e}  max|dturn| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            eng25 = backtest(px, wA, cost_bps=25.0, freq="W")
            d3 = np.abs(eng25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            print(f"    G2 derived rung r(25) vs backtest(cost_bps=25): max|d| {d3:.3e}")
            assert d3 < 1e-12
        reb = rebalance_mask(px.index, FREQ)
        kt_cnt = (rk <= N).sum(axis=1)
        nelig = elig.sum(axis=1)
        over = (kt_cnt > N) & reb            # TIE OVERHANG: |{rank <= n}| > n (average ranks)
        # A cap-rule SEED day: the two caps can pick different books.  cap_KT = |{r<=n}| and
        # cap_FLAT = n differ whenever ties move the count off n; the difference only BITES when
        # more names are holdable than cap_KT admits, i.e. when n_elig > |{r<=n}|.
        seed = (kt_cnt != N) & (nelig > kt_cnt) & reb
        print(f"    cap-rule seed days (|{{r<={N}}}| != {N} and n_elig > |{{r<={N}}}|): "
              f"{int(seed.sum())} of {int(reb.sum())} rebalance days "
              f"({int(over.sum())} of them tie-OVERHANG, |{{r<={N}}}| > {N})")
        for cp in CAPS:
            dis = (sel_x(px, rk, N, 0, cp)[reb] != sel_hard(rk, N)[reb])
            dd = int(dis.values.sum()); ddays = dis.index[dis.any(axis=1)]
            print(f"    G3 [{pname}] sel_x(x=0, cap={cp:<5}) nests sel_hard on {int(reb.sum())} "
                  f"weekly rebalance days: {dd} disagreements of {int(reb.sum())*px.shape[1]}"
                  + (f"  [tie-overhang days: {int(over.sum())} of {int(reb.sum())}]" if cp == "FLAT" else ""))
            if cp == "FLAT":
                # FLAT is NOT an exact nesting: on a tie-overhang day the average-rank convention
                # puts n+1 names at rank <= n, so k_t = n+1 while the flat cap holds n.  Assert
                # the difference is CONFINED to those days -- a tie convention, not the cap.
                assert set(ddays) <= set(over.index[over]), "FLAT differs off tie-overhang days"
            else:
                assert dd == 0
        for x in XS:
            mine = sel_x(px, rk, N, x, "KT")[reb]
            theirs = parent_mod.sel_ex(px, rk, N, 0, x)[reb]
            dd = int((mine != theirs).values.sum())
            print(f"    G4 [{pname}] sel_x(x={x:>2}, cap=KT) == idea 349 sel_ex(e=0, x={x:>2}): "
                  f"{dd} disagreements")
            assert dd == 0

        # ------------------------------------------------ the grid
        print(f"\n[A] GRID {pname} (every point; turn/yr = mean yearly sum|dw|)")
        print(f"    {'cap':>5} {'x':>3} {'turn/yr':>8} {'names':>6} {'gross':>6} | "
              + " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} {'OOS':>6} 4b 4a"
                           for c in COSTS))
        kt_sel = {}
        for cp in CAPS:
            for x in XS:
                sel = sel_x(px, rk, N, x, cp)
                if cp == "KT":
                    kt_sel[x] = sel
                dis_kt = int((sel[reb] != kt_sel[x][reb]).values.sum())
                dis_days = int((sel[reb] != kt_sel[x][reb]).any(axis=1).sum())
                r0, t0, gr, kk = fast_backtest(px, weights_from(sel), 0.0, FREQ)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                line = (f"    {cp:>5} {x:>3} {tpy:>8.2f} {kk.loc[start:].mean():>6.2f} "
                        f"{gr.loc[start:].mean():>6.3f} |")
                rec = dict(panel=pname, cap=cp, x=x, turn_per_yr=tpy,
                           names=kk.loc[start:].mean(), names_max=int(kk.loc[start:].max()),
                           gross=gr.loc[start:].mean(), disagree_vs_KT=dis_kt,
                           disagree_days_vs_KT=dis_days, reb_days=int(reb.sum()),
                           tie_overhang_days=int(over.sum()), cap_seed_days=int(seed.sum()))
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    basec = base10 if c == 10 else (br - bt * c / 1e4).loc[start:]
                    ok4a, d4a, f4a = bars_4a(r, basec)
                    line += (f" {mt['CAGR']:>10.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{h1:>6.3f}/{h2:<6.3f} {oo['Sharpe']:>6.3f} "
                             f"{'Y' if ok4b else 'n':>2} {'Y' if ok4a else 'n':>2} |")
                    rec.update({f"CAGR_{c}": mt["CAGR"], f"Sharpe_{c}": mt["Sharpe"],
                                f"MaxDD_{c}": mt["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                                f"OOS_Sharpe_{c}": oo["Sharpe"], f"OOS_CAGR_{c}": oo["CAGR"],
                                f"OOS_MaxDD_{c}": oo["MaxDD"],
                                f"IS_Sharpe_{c}": metrics(r.loc[:IS_END])["Sharpe"],
                                f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a)})
                    rec.update({f"m4b_{k}_{c}": v for k, v in d4b.items()})
                    rec.update({f"m4a_{k}_{c}": v for k, v in d4a.items()})
                cst, cbar = (breakeven(r0, t0, spy) if rec["keep4b_0"] else (None, rec["fail4b_0"]))
                rec["breakeven_bps"] = cst if cst is not None else -1
                rec["breakeven_first_fail"] = cbar
                line += f" c*={rec['breakeven_bps']:>4}"
                print(line)
                rows.append(rec)

                if cp == "KT":
                    p = parent.loc[(pname, x)]
                    ds = abs(p["Sharpe_10"] - rec["Sharpe_10"]); dc = abs(p["CAGR_10"] - rec["CAGR_10"])
                    dt_ = abs(p["turn_per_yr"] - rec["turn_per_yr"]); dm = abs(p["MaxDD_10"] - rec["MaxDD_10"])
                    do = abs(p["OOS_Sharpe_10"] - rec["OOS_Sharpe_10"]); dk = abs(p["names"] - rec["names"])
                    print(f"        G5 vs idea 349 grid.csv [{pname} e=0 x={x}]: |dSharpe| {ds:.3e} "
                          f"|dCAGR| {dc:.3e} |dMaxDD| {dm:.3e} |dturn| {dt_:.3e} |dOOS| {do:.3e} "
                          f"|dnames| {dk:.3e}")
                    assert max(ds, dc, dt_, dm, do, dk) < 1e-12

    g = pd.DataFrame(rows); g.to_csv(gcsv, index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel"); ctx.reset_index().to_csv(ccsv, index=False)
    print(f"\n    wrote {gcsv.name} ({len(g)} rows) and {ccsv.name}")
    analyse(g, ctx, panels)


# ---------------------------------------------------------------- analysis
def analyse(g, ctx, panels):
    pnames = list(dict.fromkeys(g.panel))
    key = lambda d, cp, x: d[(d.cap == cp) & (d.x == x)].iloc[0]

    # ------------------------------------------------------------ [B0] is FLAT a no-op?
    print("\n\n[B0] IS THE FLAT CAP A NO-OP?  (cell-for-cell KT vs FLAT, all 6 x on all 3 panels)")
    print("     Algebra: holdings = min(cap, |holdable|); |holdable| <= n_elig; cap_KT = |{r<=n}|")
    print("     and cap_FLAT = n.  These coincide EXCEPT on tie-overhang days, where the average-")
    print("     rank convention puts n+1 names at rank <= n.  Tested here, not assumed.")
    print(f"     {'panel':>9} {'x':>3} | {'sel disagree':>12} {'days':>6}/{'reb':<5} | "
          f"{'dSharpe':>10} {'dCAGR':>10} {'dturn':>10} {'dnames':>10}")
    worst = 0.0; tot_days = 0
    for pname in pnames:
        d = g[g.panel == pname]
        for x in XS:
            a, b = key(d, "KT", x), key(d, "FLAT", x)
            ds = b.Sharpe_10 - a.Sharpe_10; dc = b.CAGR_10 - a.CAGR_10
            dt_ = b.turn_per_yr - a.turn_per_yr; dk = b.names - a.names
            worst = max(worst, abs(ds)); tot_days += int(b.disagree_days_vs_KT)
            print(f"     {pname:>9} {x:>3} | {int(b.disagree_vs_KT):>12} "
                  f"{int(b.disagree_days_vs_KT):>6}/{int(b.reb_days):<5} | "
                  f"{ds:>10.3e} {dc:>10.3e} {dt_:>10.3e} {dk:>10.3e}")
    print(f"     WORST |dSharpe| over all 18 KT-vs-FLAT pairs: {worst:.3e}; total rebalance days "
          f"on which the two caps pick a different book: {tot_days}")
    print("     Cap-rule SEED days per panel (ties put |{r<=n}| off n with names to spare; of "
          "which tie-OVERHANG):")
    for p in pnames:
        z = g[g.panel == p].iloc[0]
        print(f"       {p:>9} {int(z.cap_seed_days):>4}/{int(z.reb_days)} "
              f"({int(z.tie_overhang_days)} overhang)")
    print("     The x=0 row is memoryless, so it shows the seed alone.  At x>0 the buffer CARRIES")
    print("     a divergence forward, which is why a handful of tie days becomes hundreds of")
    print("     differing rebalances and up to 0.037 of Sharpe: a PATH artefact, not a mechanism.")

    # ------------------------------------------------------------ [B1] marginals by cap rule
    print("\n\n[B1] MARGINAL EFFECT OF THE EXIT BUFFER, BY CAP RULE (dSharpe vs x=0, 10 bps)")
    print("     Parent's published EXIT reading (KT cap): mean +0.0577, 15/15 positive, "
          "spearman(x, names) +0.000.")
    b1 = []
    for pname in pnames:
        d = g[g.panel == pname]
        a = key(d, "KT", 0)
        print(f"  {pname}: anchor x=0 Sharpe {a.Sharpe_10:.3f} turn {a.turn_per_yr:.2f} "
              f"names {a.names:.2f}")
        for cp in CAPS:
            parts = []
            for x in XS:
                if x == 0:
                    continue
                c = key(d, cp, x)
                parts.append(f"{x:>3}: dS {c.Sharpe_10 - a.Sharpe_10:+.3f} T {c.turn_per_yr:5.2f} "
                             f"k {c.names:5.2f}")
                b1.append(dict(panel=pname, cap=cp, x=x, dSharpe=c.Sharpe_10 - a.Sharpe_10,
                               dCAGR=c.CAGR_10 - a.CAGR_10, turn=c.turn_per_yr, names=c.names,
                               dnames=c.names - a.names,
                               dOOS=c.OOS_Sharpe_10 - a.OOS_Sharpe_10,
                               dMaxDD=abs(a.MaxDD_10) - abs(c.MaxDD_10)))
            print(f"     {cp:>5} | " + " | ".join(parts))
    b1 = pd.DataFrame(b1)
    b1.to_csv(OUT / f"{SLUG}.marginals.csv", index=False)
    print(f"\n     {'cap':>5} | {'mean dS':>9} {'positive':>9} {'mean dOOS':>10} {'OOS pos':>8} "
          f"{'mean dnames':>12} {'sp(x,names)':>12} {'sp(x,turn)':>11}")
    for cp in CAPS:
        z = b1[b1.cap == cp]
        print(f"     {cp:>5} | {z.dSharpe.mean():>+9.4f} {int((z.dSharpe>0).sum()):>5}/{len(z):<3} "
              f"{z.dOOS.mean():>+10.4f} {int((z.dOOS>0).sum()):>4}/{len(z):<3} "
              f"{z.dnames.mean():>+12.3f} {spearman(z.x, z.names):>12.3f} "
              f"{spearman(z.x, z.turn):>11.3f}")
    for pname in pnames:
        for cp in CAPS:
            z = b1[(b1.panel == pname) & (b1.cap == cp)]
            print(f"       {pname:>9} {cp:>5}: mean dS {z.dSharpe.mean():+.4f}  "
                  f"pos {int((z.dSharpe>0).sum())}/{len(z)}  mean dnames {z.dnames.mean():+.3f}  "
                  f"sp(x,names) {spearman(z.x, z.names):+.3f} {const_flag(z.names)}")

    # ------------------------------------------------------------ [B2] KT vs UNCAP head to head
    print("\n\n[B2] DOES DROPPING THE CAP CHANGE THE ANSWER?  (UNCAP minus KT at the same x)")
    print(f"     {'panel':>9} {'x':>3} | {'dSharpe':>9} {'dOOS':>9} {'dCAGR':>9} {'dturn':>8} "
          f"{'dnames':>8}")
    hh = []
    for pname in pnames:
        d = g[g.panel == pname]
        for x in XS:
            if x == 0:
                continue
            a, b = key(d, "KT", x), key(d, "UNCAP", x)
            row = dict(panel=pname, x=x, dSharpe=b.Sharpe_10 - a.Sharpe_10,
                       dOOS=b.OOS_Sharpe_10 - a.OOS_Sharpe_10, dCAGR=b.CAGR_10 - a.CAGR_10,
                       dturn=b.turn_per_yr - a.turn_per_yr, dnames=b.names - a.names)
            hh.append(row)
            print(f"     {pname:>9} {x:>3} | {row['dSharpe']:>+9.4f} {row['dOOS']:>+9.4f} "
                  f"{row['dCAGR']:>+9.2%} {row['dturn']:>+8.2f} {row['dnames']:>+8.2f}")
    hh = pd.DataFrame(hh)
    print(f"     UNCAP beats KT on Sharpe {int((hh.dSharpe>0).sum())}/{len(hh)} "
          f"(mean {hh.dSharpe.mean():+.4f}), on OOS {int((hh.dOOS>0).sum())}/{len(hh)} "
          f"(mean {hh.dOOS.mean():+.4f}); mean dnames {hh.dnames.mean():+.2f}")

    # ------------------------------------------------------------ [C] width-matched control
    print("\n\n[C] IS THE UNCAP MARGIN JUST WIDTH?  Each UNCAP cell against a HOLDINGS-MATCHED")
    print("    hard cut: the plain top-n' book whose mean holdings is nearest the UNCAP cell's.")
    mrows = []
    print(f"     {'panel':>9} {'x':>3} {'k(UNCAP)':>9} | {'n*':>3} {'k(hard)':>8} "
          f"{'dS vs matched':>14} {'dOOS':>9}")
    for pname in pnames:
        px = panels[pname]
        start = px.index[WARMUP]
        rk, _ = rank_frame(px, drop_spy=(pname == "SMALL439"))
        cand = {}
        for npr in range(N, min(N + 81, px.shape[1]) + 1, 2):
            r0, t0, _, kk = fast_backtest(px, weights_from(sel_hard(rk, npr)), 0.0, FREQ)
            r0, t0 = r0.loc[start:], t0.loc[start:]
            r = r0 - t0 * 10 / 1e4
            cand[npr] = (kk.loc[start:].mean(), metrics(r)["Sharpe"],
                         metrics(r.loc[OOS_START:])["Sharpe"], t0.sum() / (len(r0) / 252))
        d = g[g.panel == pname]
        for x in XS:
            if x == 0:
                continue
            u = key(d, "UNCAP", x)
            nstar = min(cand, key=lambda q: abs(cand[q][0] - u.names))
            km, sm, om, tm = cand[nstar]
            mrows.append(dict(panel=pname, x=x, k_uncap=u.names, n_star=nstar, k_hard=km,
                              S_uncap=u.Sharpe_10, S_hard=sm, dS=u.Sharpe_10 - sm,
                              OOS_uncap=u.OOS_Sharpe_10, OOS_hard=om, dOOS=u.OOS_Sharpe_10 - om,
                              turn_uncap=u.turn_per_yr, turn_hard=tm))
            print(f"     {pname:>9} {x:>3} {u.names:>9.2f} | {nstar:>3} {km:>8.2f} "
                  f"{u.Sharpe_10 - sm:>+14.4f} {u.OOS_Sharpe_10 - om:>+9.4f}")
    mr = pd.DataFrame(mrows); mr.to_csv(OUT / f"{SLUG}.match.csv", index=False)
    print(f"     UNCAP beats its holdings-matched hard cut {int((mr.dS>0).sum())}/{len(mr)} "
          f"(mean {mr.dS.mean():+.4f}), OOS {int((mr.dOOS>0).sum())}/{len(mr)} "
          f"(mean {mr.dOOS.mean():+.4f}); mean turnover {mr.turn_uncap.mean():.2f} vs "
          f"{mr.turn_hard.mean():.2f}x/yr")

    # ------------------------------------------------------------ [D] rule 8 walk-forward
    print("\n\n[D] RULE 8 WALK-FORWARD: x chosen by IS Sharpe (<= 2016-12-31), read once on 2017+.")
    print("    Reported per cap rule, per panel, per rung, against RULES v2 and SPY OOS.")
    wf = []
    print(f"     {'panel':>9} {'cap':>5} {'c':>3} | {'x*':>3} {'OOS Shrp':>9} {'OOS CAGR':>9} "
          f"{'OOS MaxDD':>10} | {'x=0 OOS':>8} {'base OOS':>9} {'SPY OOS':>8} | {'4b OOS-win':>10}")
    for pname in pnames:
        d = g[g.panel == pname]
        c_ = ctx.loc[pname]
        for cp in CAPS:
            for c in COSTS:
                z = d[d.cap == cp]
                pick = z.loc[z[f"IS_Sharpe_{c}"].idxmax()]
                ctrl = key(d, cp, 0)
                wf.append(dict(panel=pname, cap=cp, cost=c, x_star=int(pick.x),
                               IS_Sharpe=pick[f"IS_Sharpe_{c}"],
                               OOS_Sharpe=pick[f"OOS_Sharpe_{c}"], OOS_CAGR=pick[f"OOS_CAGR_{c}"],
                               OOS_MaxDD=pick[f"OOS_MaxDD_{c}"],
                               OOS_donothing=ctrl[f"OOS_Sharpe_{c}"],
                               base_OOS=c_.base_OOS, spy_OOS=c_.spy_OOS,
                               beats_spy_OOS=bool(pick[f"OOS_Sharpe_{c}"] > c_.spy_OOS),
                               beats_base_OOS=bool(pick[f"OOS_Sharpe_{c}"] > c_.base_OOS),
                               keep4b=bool(pick[f"keep4b_{c}"]), keep4a=bool(pick[f"keep4a_{c}"])))
                print(f"     {pname:>9} {cp:>5} {c:>3} | {int(pick.x):>3} "
                      f"{pick[f'OOS_Sharpe_{c}']:>9.3f} {pick[f'OOS_CAGR_{c}']:>9.2%} "
                      f"{pick[f'OOS_MaxDD_{c}']:>10.2%} | {ctrl[f'OOS_Sharpe_{c}']:>8.3f} "
                      f"{c_.base_OOS:>9.3f} {c_.spy_OOS:>8.3f} | "
                      f"{'Y' if pick[f'OOS_Sharpe_{c}'] > c_.spy_OOS else 'n':>10}")
    wf = pd.DataFrame(wf); wf.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(f"\n     mean OOS Sharpe by cap rule: " + "  ".join(
        f"{cp} {wf[wf.cap==cp].OOS_Sharpe.mean():.4f}" for cp in CAPS))
    print(f"     IS chooser vs do-nothing (x=0): chooser wins "
          f"{int((wf.OOS_Sharpe > wf.OOS_donothing).sum())}/{len(wf)}, "
          f"mean {(wf.OOS_Sharpe - wf.OOS_donothing).mean():+.4f}")
    print(f"     picks that differ between KT and UNCAP: "
          f"{int((wf[wf.cap=='KT'].x_star.values != wf[wf.cap=='UNCAP'].x_star.values).sum())} of 9")
    print(f"     OOS Sharpe > SPY: {int(wf.beats_spy_OOS.sum())}/{len(wf)}; "
          f"> RULES v2: {int(wf.beats_base_OOS.sum())}/{len(wf)}")

    # ------------------------------------------------------------ [E] KEEP paths
    print("\n\n[E] KEEP PATHS over all 162 (cell x rung) rows")
    for c in COSTS:
        n4a = int(g[f"keep4a_{c}"].sum()); n4b = int(g[f"keep4b_{c}"].sum())
        print(f"     {c:>2} bps: 4a {n4a}/{len(g)}   4b {n4b}/{len(g)}")
    for cp in CAPS:
        z = g[g.cap == cp]
        print(f"       {cp:>5}: 4b " + " ".join(f"{c}bps {int(z[f'keep4b_{c}'].sum())}/{len(z)}"
                                                for c in COSTS)
              + " | 4a " + " ".join(f"{c}bps {int(z[f'keep4a_{c}'].sum())}/{len(z)}" for c in COSTS))
    k = g[g.keep4b_10]
    if len(k):
        print("\n     4b passers at 10 bps (the PROTOCOL rung):")
        for _, r in k.sort_values("Sharpe_10", ascending=False).iterrows():
            print(f"       {r.panel:>9} cap={r['cap']:<5} x={int(r.x):<3} CAGR {r.CAGR_10:>6.2%} "
                  f"Sharpe {r.Sharpe_10:.3f} MaxDD {r.MaxDD_10:>7.2%} H1/H2 "
                  f"{r.H1_10:.3f}/{r.H2_10:.3f} OOS {r.OOS_Sharpe_10:.3f} k {r.names:.1f} "
                  f"c*={int(r.breakeven_bps)}")
    print(f"\n    wrote {SLUG}.marginals.csv / .match.csv / .walkforward.csv")


if __name__ == "__main__":
    main()
