#!/usr/bin/env python3
"""Idea 357: is the ENTRY buffer just `n` in disguise?

Idea 349 split idea 331's single band dial `m` into two sides -- an ENTRY buffer (enter an
unheld name only at rank <= n-e) and an EXIT buffer (sell a held name only once rank > n+x) --
and found the entry side moves HOLDINGS (spearman(e, names) -0.988) far more than it moves
TURNOVER (-0.298), while the exit side is name-count-neutral by construction.  A dial that
mostly shrinks the book is not a band: it is a smaller top-n cut wearing a band's name.

THE TEST, pre-registered before any number was read:

  [A] TWO LADDERS on the same frame, same weights, same cadence, same costs.
        BUFFER ladder: n = 20 fixed, e in {0,2,4,6,8,12,16}, x = 0   (idea 349's entry side)
        HARD   ladder: plain top-n' cut, n' in 2..20                 (the comparand)
      (e=0) and (n'=20) are the SAME book and are asserted identical in section [0].
      Exactly two tuned parameters (n, e); the hard ladder is the same `n` axis read at its
      own values, and every point of both ladders is printed and written to `<slug>.grid.csv`.
      Panel {U56, B136, SMALL439} and cost rung {0, 10, 25} bps are REPORTED axes, not choices.

  [B] THE MATCH.  Three readings of the same 7-cell entry ladder, per panel per rung:
      B1  NAIVE PAIR: buffer(e) vs the hard cut at n' = 20 - e (same nominal entry threshold).
      B2  HOLDINGS-MATCHED (the decisive one, and the queue's own request): the hard ladder's
          Sharpe is linearly interpolated in mean holdings k, and each buffer cell is read
          against the hard cut of ITS OWN k.  If dSharpe_match <= 0 the buffer bought nothing
          that shrinking n would not have bought.  Nearest-neighbour match reported beside it.
      B3  TURNOVER-MATCHED control: the same interpolation done in annual turnover instead.
          The buffer trades LESS than the equal-holdings hard cut, so this is the reading that
          flatters it; quoting both is what separates "band" from "narrower book".
      B4  ADMISSION: does any buffer cell clear a KEEP path (4a or 4b) that no hard cell on the
          same panel and rung clears?  A dial that opens no cell is a re-parameterisation.

  [C] BREAKEVEN c*: largest whole bps at which all five 4b bars hold, both ladders.

  [D] RULE 8 walk-forward: the cell is chosen on 2008-2016 by IS Sharpe at 10 bps and
      2017-2026 is read once, on three MENUS -- BUFFER-ONLY (7 cells), HARD-ONLY (19 cells),
      UNION (26) -- against the n=20 anchor, the OOS-best cell (regret), RULES v2 (live) and
      SPY.  If an ex-ante chooser given the entry dial does no better than one given only `n`,
      the record should retire `e` and quote `n`.

Book (fixed, idea 349's convention, never tuned): eligible = above the 200d MA and vol20 < 0.60;
ranked by the RULES v1 composite with the vol scaler OFF; NORM weights w_i = g/k_t at g = 0.75
so neither ladder can smuggle in a gross change; weekly; next-day execution; 10 bps per unit
turnover at the anchor rung.  The buffer arm keeps idea 349's slot cap k_t = |{rank <= n}|.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters
every momentum book, and flatters a CONCENTRATED one most; the levels are optimistic, the
buffer-vs-hard DIFFERENCES much less so.  (2) SMALL439 starts 2010-01-04, so its halves are not
the same calendar halves as U56/B136 and its rule-8 IS window is effectively 2010-2016; the 44
tickers with `max_1d_move >= 1.0` in data/small_meta.csv are dropped before anything runs.
(3) The hard ladder's mean holdings is bounded below by 2 and above by ~20, so a buffer cell
whose k falls outside that range is reported as EXTRAPOLATED and excluded from the B2 mean.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_is-the-ENTRY-buffer-just-n-in-disguise_cloud"
OUT = ROOT / "research" / "backtests"
PARENT = OUT / "2026-09-07_does-a-band-on-the-EXIT-ONLY-beat-a-band-on-both-sides_C.grid.csv"
MAX_VOL, GROSS, N = 0.60, 0.75, 20
FREQ = "W"
ES = [0, 2, 4, 6, 8, 12, 16]                 # entry buffer (enter at rank <= n - e), x = 0
NS = list(range(2, 21))                      # plain hard top-n' cut
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the book
def rank_frame(px, drop_spy=False):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    """Plain top-n' rank cut, recomputed from scratch every rebalance."""
    return rk <= n


def sel_entry(px, rk, n, e, freq=FREQ):
    """Idea 349's ENTRY-buffer book with x = 0: slot cap k_t = |{rank <= n}|, a held name is
    sold as soon as its rank passes n, but a free slot may only be filled from rank <= n-e.
    e = 0 nests sel_hard(n) exactly (asserted in [0])."""
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    enter_at = n - e
    held = []
    last = np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n]
            held.sort(key=lambda j: r[j])
            if len(held) > cap:
                held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs_ = set(held)
                for j in order:
                    if len(held) >= cap:
                        break
                    if r[j] != r[j] or r[j] > enter_at:
                        break
                    if j not in hs_:
                        held.append(j); hs_.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols))
            last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return GROSS * s.div(k, axis=0).fillna(0.0)


# ---------------------------------------------------------------- fast backtester
def fast_backtest(px, w, cost_bps=0.0, freq=FREQ):
    """Vectorised-loop clone of engine.backtest (same semantics). Asserted in [0]."""
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
            bar = ",".join(f)
            break
    return cstar, bar


def spearman(a, b):
    x, y = pd.Series(list(a)).rank(), pd.Series(list(b)).rank()
    return float(x.corr(y))


def interp_at(xs, ys, x0):
    """Linear interpolation of y(x) on a ladder that need not be sorted; returns
    (value, extrapolated?).  Used to read the hard ladder at the buffer cell's own k / T."""
    o = np.argsort(np.asarray(xs, dtype=float))
    X = np.asarray(xs, dtype=float)[o]; Y = np.asarray(ys, dtype=float)[o]
    ex = bool(x0 < X[0] or x0 > X[-1])
    return float(np.interp(x0, X, Y)), ex


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print(f"Book: eligible = above 200d MA and vol20 < {MAX_VOL}, ranked by the v1 composite "
          f"(vol scaler OFF), NORM weights g/k_t at g={GROSS}, WEEKLY, next-day execution.")
    print(f"Tuned (2): n and e.  BUFFER ladder n={N}, e in {ES} (x=0).  HARD ladder n' in "
          f"{NS[0]}..{NS[-1]}.  {len(ES)}+{len(NS)} cells per panel.")
    print(f"Reported axes: panel, cost {COSTS} bps.  e=0 and n'={N} are the same book.")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    gcsv, ccsv = OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.ctx.csv"
    if RESUME and gcsv.exists() and ccsv.exists():
        analyse(pd.read_csv(gcsv), pd.read_csv(ccsv).set_index("panel"))
        return

    parent = pd.read_csv(PARENT)
    parent = parent[parent.x == 0].set_index(["panel", "e"])

    rows, ctx_rows = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        nel = elig.sum(axis=1).loc[start:]
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(f"    eligible/day mean {nel.mean():.1f} min {nel.min()} max {nel.max()}")
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
                             end=str(px.index[-1].date()), elig_mean=nel.mean(),
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
        dd = int((sel_entry(px, rk, N, 0)[reb] != sel_hard(rk, N)[reb]).values.sum())
        print(f"    G3 [{pname}] sel_entry(e=0) nests sel_hard(n={N}) on {int(reb.sum())} weekly "
              f"rebalance days: {dd} disagreements of {int(reb.sum()) * px.shape[1]}")
        assert dd == 0

        # ------------------------------------------------ the two ladders
        print(f"\n[A] GRID {pname} (every point; turn/yr = mean yearly sum|dw|)")
        print(f"    {'arm':>6} {'p':>3} {'turn/yr':>8} {'names':>6} {'gross':>6} | "
              + " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} {'OOS':>6} 4b 4a"
                           for c in COSTS))
        for arm, vals in (("BUFFER", ES), ("HARD", NS)):
            for v in vals:
                sel = sel_entry(px, rk, N, v) if arm == "BUFFER" else sel_hard(rk, v)
                r0, t0, gr, kk = fast_backtest(px, weights_from(sel), 0.0, FREQ)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                rec = dict(panel=pname, arm=arm, p=v, e=(v if arm == "BUFFER" else -1),
                           n=(N if arm == "BUFFER" else v), turn_per_yr=tpy,
                           names=kk.loc[start:].mean(), gross=gr.loc[start:].mean())
                line = (f"    {arm:>6} {v:>3} {tpy:>8.2f} {rec['names']:>6.2f} "
                        f"{rec['gross']:>6.3f} |")
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
                    rec.update({f"m4b_{k}_{c}": v2 for k, v2 in d4b.items()})
                    rec.update({f"m4a_{k}_{c}": v2 for k, v2 in d4a.items()})
                cst, cbar = (breakeven(r0, t0, spy) if rec["keep4b_0"] else (None, rec["fail4b_0"]))
                rec["breakeven_bps"] = cst if cst is not None else -1
                rec["breakeven_first_fail"] = cbar
                line += f" c*={rec['breakeven_bps']:>4}"
                print(line)
                rows.append(rec)

                # -------- reproduction against idea 349's committed entry-ladder rows
                if arm == "BUFFER":
                    p = parent.loc[(pname, v)]
                    ds = abs(p["Sharpe_10"] - rec["Sharpe_10"]); dc = abs(p["CAGR_10"] - rec["CAGR_10"])
                    dt_ = abs(p["turn_per_yr"] - rec["turn_per_yr"]); dm = abs(p["MaxDD_10"] - rec["MaxDD_10"])
                    do = abs(p["OOS_Sharpe_10"] - rec["OOS_Sharpe_10"]); dk = abs(p["names"] - rec["names"])
                    print(f"        G4 vs idea 349 grid.csv [{pname} e={v} x=0]: |dSharpe| {ds:.3e} "
                          f"|dCAGR| {dc:.3e} |dMaxDD| {dm:.3e} |dturn| {dt_:.3e} |dOOS| {do:.3e} "
                          f"|dnames| {dk:.3e}")
                    assert max(ds, dc, dt_, dm, do, dk) < 1e-12

    g = pd.DataFrame(rows); g.to_csv(gcsv, index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel"); ctx.reset_index().to_csv(ccsv, index=False)
    print(f"\n    wrote {gcsv.name} ({len(g)} rows) and {ccsv.name}")
    analyse(g, ctx)


# ---------------------------------------------------------------- analysis
def analyse(g, ctx):
    panels = list(dict.fromkeys(g.panel))
    buf = lambda d, e: d[(d.arm == "BUFFER") & (d.p == e)].iloc[0]
    hrd = lambda d, n: d[(d.arm == "HARD") & (d.p == n)].iloc[0]

    # ------------------------------------------------------------ [B0] what the dial does
    print("\n\n[B0] WHAT EACH DIAL MOVES (10 bps; spearman of the ladder parameter against k and T)")
    for pname in panels:
        d = g[g.panel == pname]
        b, h = d[d.arm == "BUFFER"].sort_values("p"), d[d.arm == "HARD"].sort_values("p")
        print(f"  {pname}: BUFFER e {list(b.p)} -> k {[round(v,2) for v in b.names]} "
              f"T {[round(v,2) for v in b.turn_per_yr]}")
        print(f"  {' '*len(pname)}  spearman(e,k) {spearman(b.p, b.names):+.3f}  "
              f"spearman(e,T) {spearman(b.p, b.turn_per_yr):+.3f} | "
              f"HARD spearman(n,k) {spearman(h.p, h.names):+.3f}  "
              f"spearman(n,T) {spearman(h.p, h.turn_per_yr):+.3f}")
        print(f"  {' '*len(pname)}  hard-ladder k range {h.names.min():.2f}..{h.names.max():.2f}, "
              f"T range {h.turn_per_yr.min():.2f}..{h.turn_per_yr.max():.2f}")

    # ------------------------------------------------------------ [B1]-[B3] the match
    print("\n[B1/B2/B3] THE MATCH — buffer(e) against the hard ladder, three ways, every rung")
    print("     naive  = hard cut at n'=20-e | k-match = hard ladder interpolated at the buffer's")
    print("     own mean holdings (DECISIVE) | T-match = interpolated at its own annual turnover")
    m = []
    for pname in panels:
        d = g[g.panel == pname]
        h = d[d.arm == "HARD"]
        for c in COSTS:
            print(f"  {pname} @ {c} bps:")
            for e in ES:
                if e == 0:
                    continue
                cb = buf(d, e)
                anchor = buf(d, 0)[f"Sharpe_{c}"]
                nn = N - e
                naive = hrd(d, nn)[f"Sharpe_{c}"] if nn in list(h.p) else np.nan
                sk, exk = interp_at(h.names, h[f"Sharpe_{c}"], cb.names)
                st, ext = interp_at(h.turn_per_yr, h[f"Sharpe_{c}"], cb.turn_per_yr)
                nnk = h.iloc[(h.names - cb.names).abs().values.argmin()]
                rec = dict(panel=pname, cost=c, e=e, k=cb.names, T=cb.turn_per_yr,
                           Sharpe=cb[f"Sharpe_{c}"], dS_vs_anchor=cb[f"Sharpe_{c}"] - anchor,
                           naive_n=nn, naive_Sharpe=naive, dS_naive=cb[f"Sharpe_{c}"] - naive,
                           kmatch_Sharpe=sk, dS_kmatch=cb[f"Sharpe_{c}"] - sk, kmatch_extrap=exk,
                           nn_n=int(nnk.p), nn_k=nnk.names, nn_Sharpe=nnk[f"Sharpe_{c}"],
                           dS_nn=cb[f"Sharpe_{c}"] - nnk[f"Sharpe_{c}"],
                           Tmatch_Sharpe=st, dS_Tmatch=cb[f"Sharpe_{c}"] - st, Tmatch_extrap=ext,
                           OOS=cb[f"OOS_Sharpe_{c}"],
                           dOOS_kmatch=cb[f"OOS_Sharpe_{c}"] - interp_at(h.names, h[f"OOS_Sharpe_{c}"], cb.names)[0])
                m.append(rec)
                print(f"     e={e:>2} k {cb.names:5.2f} T {cb.turn_per_yr:5.2f} S {cb[f'Sharpe_{c}']:.3f} "
                      f"| vs anchor {rec['dS_vs_anchor']:+.3f} "
                      f"| naive n'={nn:<2} {naive:.3f} -> {rec['dS_naive']:+.3f} "
                      f"| k-match {sk:.3f} -> {rec['dS_kmatch']:+.3f}{'*' if exk else ' '} "
                      f"(nn n'={int(nnk.p)} k {nnk.names:5.2f} -> {rec['dS_nn']:+.3f}) "
                      f"| T-match {st:.3f} -> {rec['dS_Tmatch']:+.3f}{'*' if ext else ''} "
                      f"| dOOS_k {rec['dOOS_kmatch']:+.3f}")
    m = pd.DataFrame(m)
    m.to_csv(OUT / f"{SLUG}.match.csv", index=False)

    print("\n     SUMMARY of the match (all panels x rungs; * = extrapolated cells excluded from k-match)")
    ok = m[~m.kmatch_extrap]
    print(f"       vs the (e=0) anchor      : mean dS {m.dS_vs_anchor.mean():+.4f}  "
          f"positive {int((m.dS_vs_anchor>0).sum())}/{len(m)}")
    print(f"       NAIVE  (hard n'=20-e)    : mean dS {m.dS_naive.mean():+.4f}  "
          f"positive {int((m.dS_naive>0).sum())}/{len(m)}")
    print(f"       K-MATCHED (decisive)     : mean dS {ok.dS_kmatch.mean():+.4f}  "
          f"positive {int((ok.dS_kmatch>0).sum())}/{len(ok)}  "
          f"(nearest-neighbour {int((ok.dS_nn>0).sum())}/{len(ok)}, mean {ok.dS_nn.mean():+.4f})")
    print(f"       K-MATCHED out of sample  : mean dOOS {ok.dOOS_kmatch.mean():+.4f}  "
          f"positive {int((ok.dOOS_kmatch>0).sum())}/{len(ok)}")
    okt = m[~m.Tmatch_extrap]
    print(f"       T-MATCHED (control)      : mean dS {okt.dS_Tmatch.mean():+.4f}  "
          f"positive {int((okt.dS_Tmatch>0).sum())}/{len(okt)}")
    for c in COSTS:
        z = ok[ok.cost == c]; zt = okt[okt.cost == c]
        print(f"       by rung c={c:>2}: k-match {int((z.dS_kmatch>0).sum())}/{len(z)} "
              f"mean {z.dS_kmatch.mean():+.4f} | T-match {int((zt.dS_Tmatch>0).sum())}/{len(zt)} "
              f"mean {zt.dS_Tmatch.mean():+.4f} | naive "
              f"{int((m[m.cost==c].dS_naive>0).sum())}/{len(m[m.cost==c])}")
    for pname in panels:
        z = ok[ok.panel == pname]
        print(f"       by panel {pname:>9}: k-match {int((z.dS_kmatch>0).sum())}/{len(z)} "
              f"mean {z.dS_kmatch.mean():+.4f}  max {z.dS_kmatch.max():+.4f} "
              f"(e={int(z.iloc[z.dS_kmatch.values.argmax()].e)} @ "
              f"{int(z.iloc[z.dS_kmatch.values.argmax()].cost)} bps)")
    print(f"       explanatory power of k alone: spearman(k, Sharpe) across BOTH ladders @10 bps:")
    for pname in panels:
        d = g[(g.panel == pname)]
        print(f"         {pname:>9}: hard {spearman(d[d.arm=='HARD'].names, d[d.arm=='HARD'].Sharpe_10):+.3f}  "
              f"buffer {spearman(d[d.arm=='BUFFER'].names, d[d.arm=='BUFFER'].Sharpe_10):+.3f}  "
              f"pooled {spearman(d.names, d.Sharpe_10):+.3f}")

    # ------------------------------------------------------------ [B5] cost decomposition
    print("\n[B5] WHAT THE SURVIVING MARGIN IS MADE OF (holdings-matched, decomposed by cost)")
    print("     For a book of effective vol s, Sharpe(c) = (mu - T*c/1e4)/s exactly, so")
    print("     dS_kmatch(c) = dS_kmatch(0) + (c/1e4)*(T_hard/s_hard - T_buf/s_buf).")
    print("     s is recovered from each book's OWN rungs: s = T*25/(1e4*(S_0 - S_25)).")
    dec = []
    for pname in panels:
        d = g[g.panel == pname]
        h = d[d.arm == "HARD"]
        print(f"  {pname}:")
        for e in ES:
            if e == 0:
                continue
            cb = buf(d, e)
            sb = cb.turn_per_yr * 25 / 1e4 / (cb.Sharpe_0 - cb.Sharpe_25)
            Th = interp_at(h.names, h.turn_per_yr, cb.names)[0]
            S0h = interp_at(h.names, h.Sharpe_0, cb.names)[0]
            S25h = interp_at(h.names, h.Sharpe_25, cb.names)[0]
            sh = Th * 25 / 1e4 / (S0h - S25h)
            a0 = cb.Sharpe_0 - S0h
            for c in (10, 25):
                Sch = interp_at(h.names, h[f"Sharpe_{c}"], cb.names)[0]
                act = cb[f"Sharpe_{c}"] - Sch
                cost_comp = (c / 1e4) * (Th / sh - cb.turn_per_yr / sb)
                dec.append(dict(panel=pname, e=e, cost=c, k=cb.names, T_buf=cb.turn_per_yr,
                                T_kmatch=Th, dT=cb.turn_per_yr - Th, s_buf=sb, s_hard=sh,
                                alpha_at_0=a0, cost_component=cost_comp,
                                predicted=a0 + cost_comp, actual=act,
                                resid=act - a0 - cost_comp,
                                cost_share=(cost_comp / act) if act else np.nan))
            r10 = dec[-2]
            print(f"     e={e:>2} k {cb.names:5.2f} | T buf {cb.turn_per_yr:5.2f} vs k-matched hard "
                  f"{Th:5.2f} (dT {cb.turn_per_yr-Th:+5.2f}, {100*(cb.turn_per_yr/Th-1):+5.1f}%) | "
                  f"dS(0) {a0:+.3f} + cost {r10['cost_component']:+.3f} = {r10['predicted']:+.3f} "
                  f"vs actual {r10['actual']:+.3f} @10bps (resid {r10['resid']:+.4f})")
    dec = pd.DataFrame(dec)
    dec.to_csv(OUT / f"{SLUG}.decomp.csv", index=False)
    for c in (10, 25):
        z = dec[dec.cost == c]
        print(f"     @{c:>2} bps: mean actual {z.actual.mean():+.4f} = alpha_at_0 "
              f"{z.alpha_at_0.mean():+.4f} + cost {z.cost_component.mean():+.4f} "
              f"(resid mean {z.resid.mean():+.5f}, max |resid| {z.resid.abs().max():.5f}); "
              f"cost share of the margin {100*z.cost_component.sum()/z.actual.sum():.0f}%")
    print(f"     turnover gap at matched holdings: mean {dec[dec.cost==10].dT.mean():+.2f}x/yr "
          f"({100*(dec[dec.cost==10].T_buf/dec[dec.cost==10].T_kmatch-1).mean():+.1f}%), "
          f"buffer trades less in {int((dec[dec.cost==10].dT<0).sum())}/{len(dec[dec.cost==10])} cells")
    print(f"     alpha_at_0 (the margin with costs switched OFF): mean "
          f"{dec[dec.cost==10].alpha_at_0.mean():+.4f}, positive "
          f"{int((dec[dec.cost==10].alpha_at_0>0).sum())}/{len(dec[dec.cost==10])}")

    # ------------------------------------------------------------ [B4] admission
    print("\n[B4] ADMISSION (both KEEP paths, every cell, every rung)")
    for c in COSTS:
        print(f"  c={c:>2} bps: 4b {int(g[f'keep4b_{c}'].sum())}/{len(g)}   "
              f"4a {int(g[f'keep4a_{c}'].sum())}/{len(g)}")
        for pname in panels:
            d = g[g.panel == pname]
            for arm in ("BUFFER", "HARD"):
                a = d[d.arm == arm]
                print(f"      {pname:>9} {arm:>6}: 4b {int(a[f'keep4b_{c}'].sum()):>2}/{len(a)}  "
                      f"4a {int(a[f'keep4a_{c}'].sum()):>2}/{len(a)}  "
                      f"passing p = {sorted(int(v) for v in a[a[f'keep4b_{c}']].p)}")
        fails = g[~g[f"keep4b_{c}"]][f"fail4b_{c}"].str.split(",").explode()
        print(f"      binding 4b bars: " + "  ".join(f"{k} {v}" for k, v in fails.value_counts().items()))
    print("  Does any BUFFER cell clear 4b where no HARD cell on the same panel+rung does?")
    newpanel = 0
    for pname in panels:
        for c in COSTS:
            d = g[g.panel == pname]
            nb = int(d[(d.arm == "BUFFER")][f"keep4b_{c}"].sum())
            nh = int(d[(d.arm == "HARD")][f"keep4b_{c}"].sum())
            tag = "NEW" if (nb > 0 and nh == 0) else "no"
            newpanel += tag == "NEW"
            print(f"      {pname:>9} @{c:>2} bps: buffer {nb}/{len(ES)}  hard {nh}/{len(NS)}  -> {tag}")
    print(f"      NEW cells opened by the entry dial: {newpanel}/{len(panels)*len(COSTS)} panel-rungs")

    # ------------------------------------------------------------ [C] breakeven
    print("\n[C] BREAKEVEN c* (largest whole bps at which all five 4b bars hold; -1 = fails at 0)")
    for arm in ("BUFFER", "HARD"):
        a = g[g.arm == arm]
        top = a.sort_values("breakeven_bps", ascending=False).head(6)
        print(f"  {arm}: best c* {int(a.breakeven_bps.max())} bps; cells with c* >= 10: "
              f"{int((a.breakeven_bps >= 10).sum())}/{len(a)}")
        for _, r in top.iterrows():
            print(f"      {r.panel:>9} p={int(r.p):>2}  c* {int(r.breakeven_bps):>4} bps  "
                  f"k {r.names:5.2f}  first fail {r.breakeven_first_fail:<12} "
                  f"S10 {r.Sharpe_10:.3f} T {r.turn_per_yr:5.2f}")

    # ------------------------------------------------------------ [D] rule 8
    print("\n[D] RULE 8 WALK-FORWARD: cell chosen on 2008-2016 IS Sharpe @10 bps, 2017-2026 read once")
    menus = {"BUFFER-ONLY (7)": lambda d: d[d.arm == "BUFFER"],
             "HARD-ONLY (19)": lambda d: d[d.arm == "HARD"],
             "UNION (26)": lambda d: d}
    wf = []
    for pname in panels:
        d = g[g.panel == pname]
        cx = ctx.loc[pname]
        best = d.iloc[d.OOS_Sharpe_10.values.argmax()]
        anch = hrd(d, N)
        print(f"  {pname}:  SPY OOS {cx.spy_OOS:.3f} | RULES v2 (live) OOS {cx.base_OOS:.3f} | "
              f"anchor n=20 OOS {anch.OOS_Sharpe_10:.3f} | OOS-best ({best.arm} p={int(best.p)}) "
              f"{best.OOS_Sharpe_10:.3f}")
        for mname, f in menus.items():
            sub = f(d)
            pick = sub.iloc[sub.IS_Sharpe_10.values.argmax()]
            print(f"      {mname:>16}: pick {pick.arm} p={int(pick.p):>2} (k {pick.names:5.2f}) IS "
                  f"{pick.IS_Sharpe_10:.3f} -> OOS Sharpe {pick.OOS_Sharpe_10:.3f} "
                  f"CAGR {pick.OOS_CAGR_10:.2%} MaxDD {pick.OOS_MaxDD_10:.2%} | "
                  f"regret {pick.OOS_Sharpe_10 - best.OOS_Sharpe_10:+.3f} | "
                  f"vs anchor {pick.OOS_Sharpe_10 - anch.OOS_Sharpe_10:+.3f} "
                  f"vs SPY {pick.OOS_Sharpe_10 - cx.spy_OOS:+.3f} "
                  f"vs LIVE {pick.OOS_Sharpe_10 - cx.base_OOS:+.3f}")
            wf.append(dict(panel=pname, menu=mname, arm=pick.arm, p=int(pick.p), k=pick.names,
                           IS=pick.IS_Sharpe_10, OOS=pick.OOS_Sharpe_10,
                           OOS_CAGR=pick.OOS_CAGR_10, OOS_MaxDD=pick.OOS_MaxDD_10,
                           regret=pick.OOS_Sharpe_10 - best.OOS_Sharpe_10,
                           vs_anchor=pick.OOS_Sharpe_10 - anch.OOS_Sharpe_10,
                           vs_spy=pick.OOS_Sharpe_10 - cx.spy_OOS,
                           vs_live=pick.OOS_Sharpe_10 - cx.base_OOS,
                           spy_OOS=cx.spy_OOS, live_OOS=cx.base_OOS,
                           anchor_OOS=anch.OOS_Sharpe_10, keep4b_10=bool(pick.keep4b_10)))
    wf = pd.DataFrame(wf)
    print("\n     MENU SUMMARY (mean over the 3 panels):")
    for mname in menus:
        z = wf[wf.menu == mname]
        print(f"      {mname:>16}: OOS {z.OOS.mean():.4f}  regret {z.regret.mean():+.4f}  "
              f"beats anchor {int((z.vs_anchor>0).sum())}/3  beats SPY {int((z.vs_spy>0).sum())}/3  "
              f"beats LIVE {int((z.vs_live>0).sum())}/3  4b {int(z.keep4b_10.sum())}/3")
    bo = wf[wf.menu == "BUFFER-ONLY (7)"].set_index("panel")
    ho = wf[wf.menu == "HARD-ONLY (19)"].set_index("panel")
    dd = (bo.OOS - ho.OOS)
    print(f"      BUFFER-ONLY minus HARD-ONLY OOS Sharpe: " +
          "  ".join(f"{p} {v:+.4f}" for p, v in dd.items()) + f"  | mean {dd.mean():+.4f}, "
          f"buffer menu wins {int((dd>0).sum())}/{len(dd)}")
    wf.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(f"\n    wrote {SLUG}.match.csv / .walkforward.csv")

    # ------------------------------------------------------------ verdict inputs
    print("\n[VERDICT INPUTS]")
    print(f"  k-matched dSharpe positive in {int((ok.dS_kmatch>0).sum())}/{len(ok)} cells, "
          f"mean {ok.dS_kmatch.mean():+.4f}, median {ok.dS_kmatch.median():+.4f}, "
          f"max {ok.dS_kmatch.max():+.4f}, min {ok.dS_kmatch.min():+.4f}")
    print(f"  T-matched dSharpe positive in {int((okt.dS_Tmatch>0).sum())}/{len(okt)} cells, "
          f"mean {okt.dS_Tmatch.mean():+.4f}")
    print(f"  rule-8 BUFFER-ONLY vs HARD-ONLY mean OOS {dd.mean():+.4f}")
    print(f"  panel-rungs where the entry dial opens a 4b cell the n dial does not: {newpanel}")


if __name__ == "__main__":
    main()
