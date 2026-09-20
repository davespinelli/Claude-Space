#!/usr/bin/env python3
"""Idea 906 (lane B, 2026-09-20) — does-the-k-over-n-OVERLAP-survive-a-POINT-IN-TIME-shaped-ADMISSION-HAIRCUT.

Idea 887 found 60 of 576 cells clearing both 4b LEVEL legs on the k/n (ratio-width) axis and left a
standing KEEP-4b candidate (MEMO_887: U56, monthly, r = 0.35, gross 0.75 / 1.00, PASS full AND OOS).
Every panel underneath it is a CURRENT-CONSTITUENT list, so the overlap may be a survivorship
artefact.  This run haircuts ADMISSIONS and re-scores the whole ladder.

WHAT A HAIRCUT IS HERE.  Admission is masked at the WEIGHTS level, never in the price history:
a name that is not admitted on day t cannot be held on day t, but its trailing windows (200d MA,
vol20, the 3/6/12m composite) are computed on its full price series exactly as the live book does.
That is what point-in-time index membership looks like, and it keeps the ONLY moving part the set
of holdable names -- no rolling-window blindness artefact.

TWO TUNED PARAMETERS, every grid point reported:
    d    — annual admission drop rate, {0.00, 0.05, 0.10, 0.20}
    kind — drop selector, {RANDOM, WINNERCUT, LOSERCUT}

CONTROL AXIS (not a tuned dial; both arms always reported):
    scheme — SHRINK: dropped names are gone, so BREADTH falls with d (the confounded arm).
             ROTATE: a dropped name serves a ONE-YEAR exile and is then re-admitted, so exactly
                     one cohort (d x n0 names) is out at any time and breadth is FLAT in calendar
                     time.  RANDOM at the same d is then an exactly breadth-matched null for
                     WINNERCUT/LOSERCUT, which is what isolates survivorship from 'fewer names'.

WINNERCUT drops the names with the HIGHEST full-sample total return -- the survivorship windfall,
the conservative bracket.  LOSERCUT drops the lowest -- the delisting-mechanics shape, the
flattering bracket.  RANDOM is the neutral null.  Both use full-sample returns DELIBERATELY: they
are a stress applied to the panel, not a tradeable rule.  SPY is the benchmark and is never dropped.

Books: MEMO_887's ratio-width book, r in {0.20,0.35,0.50,0.75} x gross in {0.75,1.00}, monthly,
10 bps, t+1, cash never respread.  Baseline: live RULES v2 on the SAME admitted panel, weekly.
SPY buy-and-hold.  Rule 8: params picked on 2009..2016-12-31 only, 2017-2026 read once.
"""
import sys, itertools, time
from pathlib import Path
import numpy as np, pandas as pd

sys.path.insert(0, "research")
from baseline import load_universe, rules_v2_weights, band_state, score, ROOT  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-20_kn-overlap-vs-admission-haircut_B"
COST_BPS = 10.0
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DROPS = [0.00, 0.05, 0.10, 0.20]
KINDS = ["RANDOM", "WINNERCUT", "LOSERCUT"]
SCHEMES = ["SHRINK", "ROTATE"]
SEEDS = [1, 2, 3, 4, 5]
RATIOS = [0.20, 0.35, 0.50, 0.75]
GROSSES = [0.75, 1.00]
BOOKS = list(itertools.product(RATIOS, GROSSES))
CHOOSERS = ["C_SHARPE", "C_CALMAR", "C_4bIS", "C_FROZEN", "C_LIVE(RULES v2)"]
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)
    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")


# ---------------------------------------------------------------- fast backtest (gated below)
def bt(prices, weights, cost_bps=COST_BPS, freq="M"):
    """numpy replay of engine.backtest — identical arithmetic, no pandas .iloc in the loop."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).to_numpy()
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).to_numpy()
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).to_numpy()
    cur = np.zeros(prices.shape[1])
    port = np.empty(len(idx)); turn = np.zeros(len(idx))
    for i in range(len(idx)):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ---------------------------------------------------------------- books (admission-aware)
def kn_weights(px, adm=None, r=0.35, gross=1.00, kmin=5, max_vol=0.60):
    """MEMO_887's ratio-width book: top k ADMITTED eligible names by the v1 composite,
    k = min(max(5, round(r * n_elig)), n_elig), gross/k each, shortfall to cash."""
    s, above, vol20 = score(px, vol_scale=True)
    elig = above & (vol20 < max_vol) & px.notna()
    if adm is not None:
        elig &= adm
    n_e = elig.sum(axis=1)
    k = np.minimum(np.maximum(kmin, np.round(r * n_e)), n_e)
    rank = s.where(elig).rank(axis=1, ascending=False)
    hold = rank.le(k, axis=0) & elig
    return (hold.astype(float).div(k.replace(0, np.nan), axis=0) * gross).fillna(0.0)


def v2_weights(px, adm=None, band=0.03, gross=0.75):
    """RULES v2 restricted to admitted names (identical to baseline.rules_v2_weights when adm is all-True)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    if adm is not None:
        e = e.where(adm, 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def m_of(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Calmar=m["Calmar"])


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ---------------------------------------------------------------- admission haircut
def admission(px, d, kind, scheme, seed, bench="SPY"):
    """Bool date x name admission mask. SPY always admitted. Drops happen on a random trading day
    inside each calendar year after the first; ROTATE re-admits the same count from the dead pool."""
    adm = pd.DataFrame(True, index=px.index, columns=px.columns)
    if d <= 0:
        return adm, []
    rng = np.random.default_rng(seed * 100003 + int(round(d * 1000)) * 101
                                + KINDS.index(kind) * 7 + SCHEMES.index(scheme) * 3)
    cols = [c for c in px.columns if c != bench]
    tot = px[cols].ffill().iloc[-1] / px[cols].bfill().iloc[0] - 1.0
    order = tot.sort_values(ascending=(kind == "LOSERCUT")).index.tolist()   # front = dropped first
    alive = set(cols)
    n0 = len(cols)
    cohort = {}                       # year dropped -> [names], re-admitted one full year later
    events = []
    for y in sorted({t.year for t in px.index})[1:]:
        days = px.index[px.index.year == y]
        if len(days) == 0:
            continue
        if scheme == "ROTATE":        # first: last year's cohort comes back, exile = 1 year
            for c in cohort.pop(y - 1, []):
                day = days[rng.integers(0, len(days))]
                adm.loc[day:, c] = True
                alive.add(c)
                events.append(dict(ticker=c, year=y, day=str(day.date()), action="READMIT",
                                   kind=kind, scheme=scheme, d=d, seed=seed))
        n_drop = min(int(np.floor(d * (n0 if scheme == "ROTATE" else len(alive)))), len(alive))
        if n_drop <= 0:
            continue
        if kind == "RANDOM":
            pick = list(rng.choice(sorted(alive), size=n_drop, replace=False))
        else:
            pick = [c for c in order if c in alive][:n_drop]
        for c in pick:
            day = days[rng.integers(0, len(days))]
            adm.loc[day:, c] = False
            alive.discard(c)
            events.append(dict(ticker=c, year=y, day=str(day.date()), action="DROP",
                               kind=kind, scheme=scheme, d=d, seed=seed))
        cohort.setdefault(y, []).extend(pick)
    return adm, events


def run_panel(px, adm):
    start = px.index[260]
    res = {k: bt(px, kn_weights(px, adm, r=k[0], gross=k[1]), freq="M")[0].loc[start:] for k in BOOKS}
    base = bt(px, v2_weights(px, adm), freq="W")[0].loc[start:]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    return res, base, spy


def legs(r, base, spy):
    mb, mm, ms = m_of(base), m_of(r), m_of(spy)
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(spy)
    mo, mso = m_of(r.loc[OOS_START:]), m_of(spy.loc[OOS_START:])
    dd_cap, cagr_floor = 0.60 * ms["MaxDD"], 0.70 * ms["CAGR"]
    dd_cap_o, cagr_floor_o = 0.60 * mso["MaxDD"], 0.70 * mso["CAGR"]
    both_level = (mm["MaxDD"] >= dd_cap) and (mm["CAGR"] >= cagr_floor)
    p4b_full = (h1 > s1) and (h2 > s2) and both_level
    p4b_oos = (mo["Sharpe"] > mso["Sharpe"]) and (mo["MaxDD"] >= dd_cap_o) and (mo["CAGR"] >= cagr_floor_o)
    return dict(CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                base_CAGR=mb["CAGR"], base_Sharpe=mb["Sharpe"], base_MaxDD=mb["MaxDD"],
                spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                spy_OOS_Sharpe=mso["Sharpe"], dd_cap=dd_cap, cagr_floor=cagr_floor,
                L_H1=(h1 > s1), L_H2=(h2 > s2), L_DD=(mm["MaxDD"] >= dd_cap), L_CAGR=(mm["CAGR"] >= cagr_floor),
                P4a=((h1 > b1) and (h2 > b2) and (mm["MaxDD"] >= mb["MaxDD"])),
                P4b_FULL=p4b_full, P4b_OOS=p4b_oos, P4b_BOTH=(p4b_full and p4b_oos), BOTH_LEVEL=both_level)


def walkforward(res, base, spy):
    """Rule 8: pick (r, gross) on 2009..2016 only, read 2017-2026 once."""
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms_is, mso = m_of(spy_is), m_of(spy_oos)
    hs = len(spy_is) // 2
    s1, s2 = metrics(spy_is.iloc[:hs])["Sharpe"], metrics(spy_is.iloc[hs:])["Sharpe"]
    cand = {}
    for key, ret in res.items():
        ris = ret.loc[:IS_END]; mis = m_of(ris); h = len(ris) // 2
        i1, i2 = metrics(ris.iloc[:h])["Sharpe"], metrics(ris.iloc[h:])["Sharpe"]
        cand[key] = dict(S=mis["Sharpe"], C=mis["Calmar"],
                         F=(i1 > s1) and (i2 > s2) and (mis["MaxDD"] >= 0.60 * ms_is["MaxDD"])
                           and (mis["CAGR"] >= 0.70 * ms_is["CAGR"]))
    picks = {"C_SHARPE": max(cand, key=lambda k: cand[k]["S"]),
             "C_CALMAR": max(cand, key=lambda k: cand[k]["C"]),
             "C_4bIS": (max([k for k in cand if cand[k]["F"]], key=lambda k: cand[k]["S"])
                        if any(cand[k]["F"] for k in cand) else max(cand, key=lambda k: cand[k]["S"])),
             "C_FROZEN": (0.35, 0.75)}
    mb = m_of(base.loc[OOS_START:])
    out = []
    for cname in CHOOSERS:
        if cname == "C_LIVE(RULES v2)":
            mo, pr, pg = mb, np.nan, np.nan
        else:
            key = picks[cname]; mo, pr, pg = m_of(res[key].loc[OOS_START:]), key[0], key[1]
        out.append(dict(chooser=cname, pick_r=pr, pick_g=pg, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                        OOS_MaxDD=mo["MaxDD"], base_OOS_Sharpe=mb["Sharpe"], base_OOS_MaxDD=mb["MaxDD"],
                        base_OOS_CAGR=mb["CAGR"], spy_OOS_CAGR=mso["CAGR"], spy_OOS_Sharpe=mso["Sharpe"],
                        spy_OOS_MaxDD=mso["MaxDD"],
                        P4b_OOS=(mo["Sharpe"] > mso["Sharpe"]) and (mo["MaxDD"] >= 0.60 * mso["MaxDD"])
                                and (mo["CAGR"] >= 0.70 * mso["CAGR"]),
                        P4a_OOS=(mo["Sharpe"] > mb["Sharpe"]) and (mo["MaxDD"] >= mb["MaxDD"])))
    return out


def main():
    t0 = time.time()
    log(f"# idea 906 — point-in-time-shaped ADMISSION HAIRCUT on the k/n overlap (lane B, {pd.Timestamp.now('UTC'):%Y-%m-%d %H:%M} UTC)")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        log(f"panel {k}: {v.shape[1]} names, {v.index[0].date()} .. {v.index[-1].date()}  (CURRENT constituents — survivorship)")

    px_u = panels["U56"]
    # GATE 1 — the fast backtester replays engine.backtest bit-for-bit
    g1 = 0.0
    for freq, w in (("M", kn_weights(px_u, None, 0.35, 1.00)), ("W", v2_weights(px_u, None))):
        e = engine_backtest(px_u, w, cost_bps=COST_BPS, freq=freq)["returns"]
        f, _ = bt(px_u, w, freq=freq)
        g1 = max(g1, float(np.abs(e - f).max()))
    log(f"GATE 1  local bt() vs engine.backtest, max|d| = {g1:.3e}  ({'PASS' if g1 < 1e-12 else 'FAIL'})")

    # GATE 2 — v2_weights with an all-True mask IS baseline.rules_v2_weights
    g2 = float(np.abs(v2_weights(px_u, None) - rules_v2_weights(px_u)).max().max())
    log(f"GATE 2  v2_weights(adm=None) vs baseline.rules_v2_weights, max|d| = {g2:.3e}  ({'PASS' if g2 == 0 else 'FAIL'})")

    # GATE 3 — reproduce MEMO_887's committed numbers at d = 0
    res0, base0, spy0 = run_panel(px_u, None)
    pub = {(0.35, 1.00): (0.157, 1.152, -0.169, 1.251, 1.071), (0.35, 0.75): (0.117, 1.150, -0.129, 1.249, 1.070)}
    log("GATE 3  MEMO_887 reproduction at d = 0 (published -> this tape):")
    g3 = 0.0
    for key, p in pub.items():
        m = m_of(res0[key]); h1, h2 = halves(res0[key])
        g3 = max(g3, abs(m["Sharpe"] - p[1]), abs(m["MaxDD"] - p[2]), abs(m["CAGR"] - p[0]))
        log(f"        r={key[0]} g={key[1]:.2f}: CAGR {p[0]:.3f}->{m['CAGR']:.4f}  Sharpe {p[1]:.3f}->{m['Sharpe']:.4f}"
            f"  MaxDD {p[2]:.3f}->{m['MaxDD']:.4f}  halves {p[3]:.3f}/{p[4]:.3f}->{h1:.4f}/{h2:.4f}")
    log(f"        max |published - reproduced| = {g3:.4f}  ({'PASS' if g3 < 0.006 else 'FAIL'}; bar 0.006 = tape drift since 2026-09-14)")
    log(f"        SPY {m_of(spy0)['CAGR']:.4f} / {m_of(spy0)['Sharpe']:.4f} / {m_of(spy0)['MaxDD']:.4f}   "
        f"live RULES v2 {m_of(base0)['CAGR']:.4f} / {m_of(base0)['Sharpe']:.4f} / {m_of(base0)['MaxDD']:.4f}")

    # ---------------- the grid
    cells = [("U56", 0.00, "NONE", "NONE", 0), ("B136", 0.00, "NONE", "NONE", 0)]
    for pan, sc, kind, d, sd in itertools.product(["U56", "B136"], SCHEMES, KINDS, [x for x in DROPS if x > 0], SEEDS):
        cells.append((pan, d, kind, sc, sd))
    log(f"\ngrid: {len(cells)} panel-cells x {len(BOOKS)} books + 1 baseline each = {len(cells)*(len(BOOKS)+1)} backtests")

    rows, wfrows, evs = [], [], []
    for ci, (pan, d, kind, sc, sd) in enumerate(cells):
        px = panels[pan]
        adm, ev = admission(px, d, kind, sc, sd)
        evs += ev
        res, base, spy = run_panel(px, None if d == 0 else adm)
        n_adm = float(adm.drop(columns=["SPY"]).loc[px.index[260]:].sum(axis=1).mean())
        for key, ret in res.items():
            v = legs(ret, base, spy)
            v.update(panel=pan, d=d, kind=kind, scheme=sc, seed=sd, r=key[0], gross=key[1], mean_admitted=n_adm)
            rows.append(v)
        for w in walkforward(res, base, spy):
            w.update(panel=pan, d=d, kind=kind, scheme=sc, seed=sd, mean_admitted=n_adm)
            wfrows.append(w)
        if ci % 20 == 0:
            log(f"  .. cell {ci+1}/{len(cells)}  {pan} {sc} {kind} d={d} seed={sd}  mean_admitted={n_adm:.1f}  ({time.time()-t0:.0f}s)")

    df = pd.DataFrame(rows); wfd = pd.DataFrame(wfrows)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    wfd.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(evs).to_csv(OUT / f"{STEM}.admissions.csv", index=False)
    log(f"grid written: {len(df)} book-cells, {len(wfd)} chooser-cells  ({time.time()-t0:.0f}s)")

    def blocks():
        for pan in ["U56", "B136"]:
            yield pan, "NONE", "NONE", 0.00
            for sc in SCHEMES:
                for kind in KINDS:
                    for d in [x for x in DROPS if x > 0]:
                        yield pan, sc, kind, d

    def sub(frame, pan, sc, kind, d, **kw):
        s = frame[(frame.panel == pan) & (frame.scheme == sc) & (frame.kind == kind) & (frame.d == d)]
        for k, v in kw.items():
            s = s[s[k] == v]
        return s

    log("\n## A. PASS RATES BY HAIRCUT — share of the 8-book ladder clearing each path (mean over seeds)")
    log(f"{'panel':<6}{'scheme':<8}{'kind':<11}{'d':>6}{'adm':>6}{'n':>5}{'BOTH_LEVEL':>11}{'4b_FULL':>9}{'4b_OOS':>8}{'4b_BOTH':>9}{'4a':>6}")
    agg = []
    for pan, sc, kind, d in blocks():
        s = sub(df, pan, sc, kind, d)
        if s.empty:
            continue
        row = dict(panel=pan, scheme=sc, kind=kind, d=d, mean_admitted=s.mean_admitted.mean(), cells=len(s),
                   BOTH_LEVEL=s.BOTH_LEVEL.mean(), P4b_FULL=s.P4b_FULL.mean(), P4b_OOS=s.P4b_OOS.mean(),
                   P4b_BOTH=s.P4b_BOTH.mean(), P4a=s.P4a.mean(),
                   L_H1=s.L_H1.mean(), L_H2=s.L_H2.mean(), L_DD=s.L_DD.mean(), L_CAGR=s.L_CAGR.mean())
        agg.append(row)
        log(f"{pan:<6}{sc:<8}{kind:<11}{d:>6.2f}{row['mean_admitted']:>6.1f}{len(s):>5}{row['BOTH_LEVEL']:>11.3f}"
            f"{row['P4b_FULL']:>9.3f}{row['P4b_OOS']:>8.3f}{row['P4b_BOTH']:>9.3f}{row['P4a']:>6.3f}")
    pd.DataFrame(agg).to_csv(OUT / f"{STEM}.passrates.csv", index=False)

    log("\n## A2. WHICH 4b LEG BINDS (share of ladder cells PASSING each leg, full sample)")
    log(f"{'panel':<6}{'scheme':<8}{'kind':<11}{'d':>6}{'H1>SPY':>8}{'H2>SPY':>8}{'DDcap':>8}{'CAGRfl':>8}")
    for row in agg:
        log(f"{row['panel']:<6}{row['scheme']:<8}{row['kind']:<11}{row['d']:>6.2f}{row['L_H1']:>8.3f}"
            f"{row['L_H2']:>8.3f}{row['L_DD']:>8.3f}{row['L_CAGR']:>8.3f}")

    log("\n## B. THE STANDING MEMO_887 CANDIDATE (r = 0.35) UNDER EVERY HAIRCUT (mean over seeds; sd in .grid.csv)")
    log(f"{'panel':<6}{'scheme':<8}{'kind':<11}{'d':>6}{'g':>6}{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}{'OOS_CAGR':>10}{'OOS_Sh':>9}{'OOS_DD':>9}{'4bBOTH':>8}")
    for pan, sc, kind, d in blocks():
        for g_ in GROSSES:
            s = sub(df, pan, sc, kind, d, r=0.35, gross=g_)
            if s.empty:
                continue
            log(f"{pan:<6}{sc:<8}{kind:<11}{d:>6.2f}{g_:>6.2f}{s.CAGR.mean():>9.4f}{s.Sharpe.mean():>9.4f}"
                f"{s.MaxDD.mean():>9.4f}{s.OOS_CAGR.mean():>10.4f}{s.OOS_Sharpe.mean():>9.4f}"
                f"{s.OOS_MaxDD.mean():>9.4f}{s.P4b_BOTH.mean():>8.3f}")

    log("\n## C. RULE 8 — parameters chosen on 2009..2016 ONLY, 2017-2026 read ONCE")
    log(f"{'panel':<6}{'scheme':<8}{'kind':<11}{'d':>6}{'chooser':<18}{'pick r/g':>10}{'OOS_CAGR':>10}{'OOS_Sh':>9}{'OOS_DD':>9}{'4b_OOS':>8}{'4a_OOS':>8}{'SPY_Sh':>8}")
    for pan, sc, kind, d in blocks():
        for cname in CHOOSERS:
            s = sub(wfd, pan, sc, kind, d, chooser=cname)
            if s.empty:
                continue
            pick = "n/a" if s.pick_r.isna().all() else f"{s.pick_r.mean():.2f}/{s.pick_g.mean():.2f}"
            log(f"{pan:<6}{sc:<8}{kind:<11}{d:>6.2f}{cname:<18}{pick:>10}{s.OOS_CAGR.mean():>10.4f}"
                f"{s.OOS_Sharpe.mean():>9.4f}{s.OOS_MaxDD.mean():>9.4f}{s.P4b_OOS.mean():>8.3f}"
                f"{s.P4a_OOS.mean():>8.3f}{s.spy_OOS_Sharpe.mean():>8.4f}")

    log(f"\ndone in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
