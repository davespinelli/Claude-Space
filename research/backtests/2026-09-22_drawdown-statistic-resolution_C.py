#!/usr/bin/env python3
"""Idea 1542 (lane C, 2026-09-22): how many committed DRAWDOWN CLAIMS in the record sit
INSIDE the DD leg's own SE -- and is there ANY statistic of the drawdown path whose
contrast SE is small enough to adjudicate a 1 pp move at this sample length?

Idea 1511 measured the paired circular-block bootstrap SE of a MaxDD contrast against the
frozen incumbent at a mean of 2.93 pp across 240 cells, 0 of 240 reaching |t| > 2, against
an anchor whose ENTIRE 4b drawdown margin is 1.10 pp.  Two halves are run here:

  PART 1 (CENSUS).  Every committed book-level MaxDD figure in LEADERBOARD.md, CHANGELOG.md
  and research/backtests/*.md, contrasted with the frozen incumbent's committed -12.05%, and
  re-scored against BOTH 1511's 2.93 pp SE and the SE this run measures on its own panels.

  PART 2 (CONSTRUCTIVE).  Six statistics of the drawdown path -- MaxDD, Calmar, Ulcer,
  time-under-water, CVaR5 of rolling 1y returns, mean drawdown -- priced with a PAIRED
  circular-block bootstrap of the CONTRAST against the frozen incumbent, on real device
  ladders (gross, band) on two panels at three cost rungs, in three windows.  A statistic
  is scored by its ADJUDICATION RATIO R = |dS/dMaxDD| / (2 x SE_contrast): R > 1 means the
  statistic resolves a move worth 1 pp of MaxDD at |t| > 2.  Rule 8: statistic and block
  length are chosen on 2009-2016 ALONE, 2017-2026 is read once.

TUNED PARAMETERS: exactly two -- the drawdown STATISTIC and the bootstrap BLOCK LENGTH L.
Panel, cost rung, device, window and draw count are REPORTED at every grid point, never
selected.  Price-only, committed caches, no network.  Costs 10 bps (0/25 also reported),
weights decided at close t applied at t+1 (engine).  Deterministic: seed 1542.
"""
import sys, re, json, zlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa
from engine import backtest                                             # noqa

OUT   = ROOT / "research" / "backtests"
STEM  = "2026-09-22_drawdown-statistic-resolution_C"
SEED  = 1542
B     = 1000                      # bootstrap draws (reported, not tuned)
LS    = [21, 63, 126]             # block lengths (TUNED DIAL 2, all rungs reported)
COSTS = [0.0, 10.0, 25.0]         # bps (PROTOCOL rung is 10; others reported)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
ANCHOR_MAXDD_PP = -12.05          # the frozen incumbent's committed MaxDD, RULES v2 @10bps
SE_1511 = 2.93                    # pp, idea 1511's mean paired MaxDD-contrast SE

log_lines = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); log_lines.append(s)

# ---------------------------------------------------------------- statistics
def dd_path(eq):
    return eq / np.maximum.accumulate(eq, axis=0) - 1.0

def stats_from_returns(R):
    """R: (T, k) daily simple returns.  Returns dict of statistic -> (k,) array.
    Units: MaxDD / MeanDD / Ulcer / CVaR5 in PERCENTAGE POINTS, TUW in pp of days,
    Calmar dimensionless."""
    T = R.shape[0]
    L = np.log1p(R)
    cs = np.cumsum(L, axis=0)
    eq = np.exp(cs)
    dd = dd_path(eq)
    yrs = T / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    maxdd = dd.min(axis=0)
    ulcer = np.sqrt((dd ** 2).mean(axis=0))
    tuw = (dd < 0).mean(axis=0)
    meandd = dd.mean(axis=0)
    # rolling 252d simple returns from the log-cumsum, then the mean of the worst 5%
    if T > 252:
        roll = np.exp(cs[252:] - cs[:-252]) - 1.0
        n = roll.shape[0]; q = max(1, int(round(0.05 * n)))
        roll_sorted = np.sort(roll, axis=0)
        cvar5 = roll_sorted[:q].mean(axis=0)
    else:
        cvar5 = np.full(R.shape[1], np.nan)
    with np.errstate(divide="ignore", invalid="ignore"):
        calmar = np.where(maxdd < 0, cagr / np.abs(maxdd), np.nan)
    return {"MaxDD": 100 * maxdd, "Calmar": calmar, "Ulcer": 100 * ulcer,
            "TUW": 100 * tuw, "CVaR5_1y": 100 * cvar5, "MeanDD": 100 * meandd}

STATS = ["MaxDD", "Calmar", "Ulcer", "TUW", "CVaR5_1y", "MeanDD"]

def perf(r):
    """Full performance dict on a return Series (for the KEEP-path tables)."""
    a = r.values
    eq = np.cumprod(1 + a); yrs = len(a) / 252.0
    dd = eq / np.maximum.accumulate(eq) - 1
    vol = a.std(ddof=1) * np.sqrt(252)
    return dict(CAGR=eq[-1] ** (1 / yrs) - 1, Sharpe=(a.mean() * 252) / vol if vol else np.nan,
                MaxDD=dd.min(), Vol=vol, Years=yrs)

# ---------------------------------------------------------------- bootstrap
def block_idx(T, L, B, rng):
    """Circular block bootstrap index matrix (B, T)."""
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, T, size=(B, nb))
    off = np.arange(L)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(B, nb * L)[:, :T] % T
    return idx

def paired_se(R, L, B, rng, batch=100):
    """R: (T, k) paired daily returns, column 0 = anchor, LAST column = SPY.  Circular-block
    bootstrap with the SAME index for every column (paired).  Returns
      se[stat] : (k,) SE of the CONTRAST stat(dev) - stat(anchor)
      leg      : (k,) SE of PROTOCOL 4b's own DD LEG MARGIN, MaxDD(dev) - 0.60 x MaxDD(SPY),
                 in pp -- the quantity the 4b drawdown cap actually convicts on."""
    T, k = R.shape
    acc = {s: [] for s in STATS}
    legacc = []
    for b0 in range(0, B, batch):
        nb = min(batch, B - b0)
        idx = block_idx(T, L, nb, rng)                     # (nb, T)
        for j in range(nb):
            Rs = R[idx[j]]                                 # (T, k) resampled, paired
            st = stats_from_returns(Rs)
            for s in STATS:
                acc[s].append(st[s] - st[s][0])
            legacc.append(st["MaxDD"] - 0.60 * st["MaxDD"][-1])
    se = {s: np.nanstd(np.array(acc[s]), axis=0, ddof=1) for s in STATS}
    return se, np.nanstd(np.array(legacc), axis=0, ddof=1)

# ---------------------------------------------------------------- devices
def devices(px):
    d = {"ANCHOR_g0.75_b0.03": rules_v2_weights(px, band=0.03, gross=0.75)}
    for g in (0.25, 0.50, 1.00, 1.25, 1.50):
        d[f"GROSS_g{g:.2f}"] = rules_v2_weights(px, band=0.03, gross=g)
    for b in (0.00, 0.06, 0.09):
        d[f"BAND_b{b:.2f}"] = rules_v2_weights(px, band=b, gross=0.75)
    d["RULESv1_n5"] = rules_v1_weights(px)
    return d

GROSS_LADDER = ["GROSS_g0.25", "GROSS_g0.50", "ANCHOR_g0.75_b0.03",
                "GROSS_g1.00", "GROSS_g1.25", "GROSS_g1.50"]

def main():
    rng_master = np.random.default_rng(SEED)
    panels = {"u56": load_universe(), "b136": load_universe(broad=True)}

    # ---------- price every device once at ZERO cost, keep turnover, derive cost rungs
    book = {}      # (panel, dev) -> DataFrame[r0, turn]
    for pname, px in panels.items():
        start = px.index[260]
        for dname, w in devices(px).items():
            res = backtest(px, w, cost_bps=0.0, freq="W")
            book[(pname, dname)] = pd.DataFrame(
                {"r0": res["returns"].loc[start:], "turn": res["turnover"].loc[start:]})
        book[(pname, "SPY")] = pd.DataFrame(
            {"r0": px["SPY"].pct_change().fillna(0).loc[start:], "turn": 0.0})
        log(f"[data] {pname}: {px.shape[1]} cols, {start.date()} -> {px.index[-1].date()}, "
            f"{len(book[(pname,'ANCHOR_g0.75_b0.03')])} bars")

    def ret(pname, dname, bps):
        d = book[(pname, dname)]
        return d["r0"] - d["turn"] * bps / 1e4

    # ---------- GATE G1: derived cost ladder == full re-simulation
    px = panels["u56"]; start = px.index[260]
    sim10 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
    g1 = float((sim10 - ret("u56", "ANCHOR_g0.75_b0.03", 10.0)).abs().max())
    log(f"[GATE G1] derived 10bps rung vs full re-simulation, max|dr| = {g1:.3e}  -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    # ---------- GATE G2: the anchor IS the live book (compare()'s own baseline)
    from baseline import rules_v2_weights as _rv2
    g2 = float((rules_v2_weights(px) - _rv2(px)).abs().max().max())
    log(f"[GATE G2] anchor == RULES v2 live weights, max|dw| = {g2:.3e}  -> {'PASS' if g2 == 0 else 'FAIL'}")

    # ---------- GATE G3: the anchor reproduces its committed MaxDD (-12.05%)
    m = perf(ret("u56", "ANCHOR_g0.75_b0.03", 10.0))
    g3 = abs(100 * m["MaxDD"] - ANCHOR_MAXDD_PP)
    log(f"[GATE G3] anchor u56 @10bps FULL: CAGR {m['CAGR']:.2%} Sharpe {m['Sharpe']:.4f} "
        f"MaxDD {m['MaxDD']:.2%}; |dMaxDD| vs committed -12.05% = {g3:.3f} pp "
        f"-> {'PASS' if g3 < 0.10 else 'FAIL'}")

    windows = {}   # name -> slicer
    idx = book[("u56", "ANCHOR_g0.75_b0.03")].index
    h = len(idx) // 2
    windows["FULL"] = (idx[0], idx[-1])
    windows["H1"]   = (idx[0], idx[h - 1])
    windows["H2"]   = (idx[h], idx[-1])
    windows["IS"]   = (idx[0], pd.Timestamp(IS_END))
    windows["OOS"]  = (pd.Timestamp(OOS_START), idx[-1])

    DEVS = list(devices(panels["u56"]).keys())

    # ================================================== PART 2a: book metrics + KEEP paths
    rows = []
    for pname in panels:
        for bps in COSTS:
            spy = {wn: perf(ret(pname, "SPY", bps).loc[a:b]) for wn, (a, b) in windows.items()}
            anc = {wn: perf(ret(pname, "ANCHOR_g0.75_b0.03", bps).loc[a:b]) for wn, (a, b) in windows.items()}
            for dname in DEVS:
                pm = {wn: perf(ret(pname, dname, bps).loc[a:b]) for wn, (a, b) in windows.items()}
                turn = book[(pname, dname)]["turn"].sum() / pm["FULL"]["Years"]
                # PROTOCOL 4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse
                keep4a = (pm["H1"]["Sharpe"] > anc["H1"]["Sharpe"] and
                          pm["H2"]["Sharpe"] > anc["H2"]["Sharpe"] and
                          pm["FULL"]["MaxDD"] >= anc["FULL"]["MaxDD"])
                # PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% SPY, CAGR >= 70% SPY
                def leg4b(w):
                    return (pm["H1"]["Sharpe"] > spy["H1"]["Sharpe"] and
                            pm["H2"]["Sharpe"] > spy["H2"]["Sharpe"] and
                            pm["OOS"]["Sharpe"] > spy["OOS"]["Sharpe"] and
                            pm[w]["MaxDD"] >= 0.60 * spy[w]["MaxDD"] and
                            pm[w]["CAGR"] >= 0.70 * spy[w]["CAGR"])
                rows.append(dict(panel=pname, cost_bps=bps, device=dname, turnover_yr=turn,
                                 **{f"{k}_{wn}": pm[wn][k] for wn in windows for k in ("CAGR", "Sharpe", "MaxDD")},
                                 SPY_Sharpe_FULL=spy["FULL"]["Sharpe"], SPY_Sharpe_OOS=spy["OOS"]["Sharpe"],
                                 SPY_CAGR_FULL=spy["FULL"]["CAGR"], SPY_CAGR_OOS=spy["OOS"]["CAGR"],
                                 SPY_MaxDD_FULL=spy["FULL"]["MaxDD"], SPY_MaxDD_OOS=spy["OOS"]["MaxDD"],
                                 base_Sharpe_FULL=anc["FULL"]["Sharpe"], base_MaxDD_FULL=anc["FULL"]["MaxDD"],
                                 KEEP_4a=keep4a, KEEP_4b_FULL=leg4b("FULL"), KEEP_4b_OOS=leg4b("OOS")))
    books = pd.DataFrame(rows)
    books.to_csv(OUT / f"{STEM}.books.csv", index=False)
    log(f"\n[PART 2a] {len(books)} book cells published -> {STEM}.books.csv")
    log(f"[PART 2a] KEEP counts over all cells: 4a {int(books.KEEP_4a.sum())}, "
        f"4b FULL {int(books.KEEP_4b_FULL.sum())}, 4b OOS {int(books.KEEP_4b_OOS.sum())}, "
        f"BOTH(4a & 4b OOS) {int((books.KEEP_4a & books.KEEP_4b_OOS).sum())}")
    sel = books[(books.cost_bps == 10.0)]
    log("\n[PART 2a] every device @10 bps (FULL CAGR/Sharpe/MaxDD | OOS CAGR/Sharpe/MaxDD | 4a 4bF 4bO):")
    for _, r in sel.iterrows():
        log(f"  {r.panel:5s} {r.device:20s} FULL {r.CAGR_FULL:7.2%} {r.Sharpe_FULL:6.4f} {r.MaxDD_FULL:8.2%} | "
            f"OOS {r.CAGR_OOS:7.2%} {r.Sharpe_OOS:6.4f} {r.MaxDD_OOS:8.2%} | "
            f"{int(r.KEEP_4a)} {int(r.KEEP_4b_FULL)} {int(r.KEEP_4b_OOS)} | turn {r.turnover_yr:.2f}x")
    for pname in panels:
        s = books[(books.panel == pname) & (books.cost_bps == 10.0)].iloc[0]
        log(f"  [{pname}] SPY FULL {s.SPY_CAGR_FULL:.2%} / {s.SPY_Sharpe_FULL:.4f} / {s.SPY_MaxDD_FULL:.2%} | "
            f"OOS {s.SPY_CAGR_OOS:.2%} / {s.SPY_Sharpe_OOS:.4f} / {s.SPY_MaxDD_OOS:.2%}")

    # ================================================== PART 2b: contrast SEs, all grid points
    se_rows, con_rows, leg_rows = [], [], []
    for pname in panels:
        for bps in COSTS:
            for wn in ("FULL", "IS", "OOS"):
                a, b = windows[wn]
                cols = DEVS + ["SPY"]
                R = np.column_stack([ret(pname, d, bps).loc[a:b].values for d in cols])
                pt = stats_from_returns(R)                          # point estimates
                for L in LS:
                    rng = np.random.default_rng(SEED + L + int(bps)
                                                 + zlib.crc32((pname + wn).encode()) % 10000)   # crc32, not hash(): PYTHONHASHSEED-independent
                    se, leg_se = paired_se(R, L, B, rng)
                    leg_pt = pt["MaxDD"] - 0.60 * pt["MaxDD"][-1]
                    for i, d in enumerate(cols):
                        leg_rows.append(dict(panel=pname, cost_bps=bps, window=wn, block_L=L, device=d,
                                             MaxDD_pp=pt["MaxDD"][i], SPY_MaxDD_pp=pt["MaxDD"][-1],
                                             leg_margin_pp=leg_pt[i], leg_SE_pp=leg_se[i],
                                             leg_t=leg_pt[i] / leg_se[i] if leg_se[i] > 0 else np.nan,
                                             leg_passes=bool(leg_pt[i] >= 0),
                                             leg_decidable=bool(leg_se[i] > 0 and abs(leg_pt[i] / leg_se[i]) > 2)))
                    for s in STATS:
                        for i, d in enumerate(DEVS):
                            if i == 0:
                                continue
                            contrast = pt[s][i] - pt[s][0]
                            sd = se[s][i]
                            se_rows.append(dict(panel=pname, cost_bps=bps, window=wn, block_L=L,
                                                stat=s, device=d, point_dev=pt[s][i], point_anchor=pt[s][0],
                                                contrast=contrast, SE=sd,
                                                t=contrast / sd if sd > 0 else np.nan,
                                                decisive=bool(sd > 0 and abs(contrast / sd) > 2)))
                for s in STATS:
                    for i, d in enumerate(cols):
                        con_rows.append(dict(panel=pname, cost_bps=bps, window=wn, stat=s,
                                             device=d, point=pt[s][i]))
                log(f"[PART 2b] {pname} {bps:>4.0f}bps {wn:4s}: bootstrapped {len(LS)} block lengths "
                    f"x {B} draws x {len(STATS)} statistics x {len(DEVS)-1} contrasts")
    se = pd.DataFrame(se_rows); se.to_csv(OUT / f"{STEM}.contrast_se.csv", index=False)
    legs = pd.DataFrame(leg_rows); legs.to_csv(OUT / f"{STEM}.dd_leg.csv", index=False)
    pd.DataFrame(con_rows).to_csv(OUT / f"{STEM}.points.csv", index=False)
    log(f"[PART 2b] {len(se)} contrast cells published -> {STEM}.contrast_se.csv")

    # ---------- adjudication ratio R = |dS/dMaxDD| / (2 x median SE) on the GROSS ladder
    adj_rows = []
    for (pname, bps, wn, L, s), g in se.groupby(["panel", "cost_bps", "window", "block_L", "stat"]):
        pts = pd.DataFrame(con_rows)
        pts = pts[(pts.panel == pname) & (pts.cost_bps == bps) & (pts.window == wn)]
        y = pts[(pts.stat == s) & (pts.device.isin(GROSS_LADDER))].set_index("device").point
        x = pts[(pts.stat == "MaxDD") & (pts.device.isin(GROSS_LADDER))].set_index("device").point
        y, x = y.reindex(GROSS_LADDER).values, x.reindex(GROSS_LADDER).values
        beta = np.polyfit(x, y, 1)[0]                      # dS per 1 pp of MaxDD
        med_se = float(np.nanmedian(g.SE.values))
        adj_rows.append(dict(panel=pname, cost_bps=bps, window=wn, block_L=L, stat=s,
                             beta_per_pp_MaxDD=beta, median_SE=med_se,
                             resolution=2 * med_se,
                             R=abs(beta) / (2 * med_se) if med_se > 0 else np.nan,
                             decisive_share=float(g.decisive.mean()),
                             n_contrasts=int(len(g))))
    adj = pd.DataFrame(adj_rows); adj.to_csv(OUT / f"{STEM}.adjudication.csv", index=False)
    log(f"\n[PART 2c] adjudication ratio R = |dS/dMaxDD| / (2 x median contrast SE); R > 1 resolves a "
        f"1 pp-of-MaxDD-equivalent move at |t| > 2.  {len(adj)} rows -> {STEM}.adjudication.csv")
    log("\n[PART 2c] ALL grid points, window=FULL, 10 bps:")
    for _, r in adj[(adj.window == "FULL") & (adj.cost_bps == 10.0)].sort_values(["panel", "stat", "block_L"]).iterrows():
        log(f"  {r.panel:5s} L={r.block_L:3d} {r.stat:9s} beta {r.beta_per_pp_MaxDD:+8.4f}/pp  "
            f"SE {r.median_SE:7.4f}  resolution {r.resolution:7.4f}  R {r.R:6.3f}  "
            f"decisive {r.decisive_share:5.1%}")

    # ---------- PART 2d: PROTOCOL 4b's OWN DD LEG, margin vs its measured SE
    log("\n[PART 2d] PROTOCOL 4b's DD leg itself: margin = MaxDD(book) - 0.60 x MaxDD(SPY), in pp, "
        "with the SE of that same quantity from the SAME paired bootstrap.  A leg is DECIDABLE only "
        "at |t| > 2.  All grid points -> " + f"{STEM}.dd_leg.csv")
    q = legs[(legs.cost_bps == 10.0) & (legs.window.isin(["FULL", "OOS"])) & (legs.device != "SPY")]
    log(f"  decidable share of the DD leg over {len(q)} (panel x window x L x device) cells @10 bps: "
        f"{q.leg_decidable.mean():.1%}; among the cells whose leg PASSES: "
        f"{q[q.leg_passes].leg_decidable.mean():.1%}")
    for _, r in legs[(legs.cost_bps == 10.0) & (legs.block_L == 126) & (legs.window == "OOS")].iterrows():
        log(f"  OOS L=126 {r.panel:5s} {r.device:20s} MaxDD {r.MaxDD_pp:7.2f} pp  "
            f"leg margin {r.leg_margin_pp:+7.2f} pp  SE {r.leg_SE_pp:5.2f}  t {r.leg_t:+6.2f}  "
            f"{'PASS' if r.leg_passes else 'FAIL'} {'DECIDABLE' if r.leg_decidable else 'undecidable'}")

    # ================================================== RULE 8 walk-forward
    log("\n[RULE 8] statistic and block length are chosen on 2009-2016 (IS) ALONE, on the "
        "u56+b136 pooled mean R at the PROTOCOL 10 bps rung; 2017-2026 (OOS) is then read ONCE.")
    is_tab = (adj[(adj.window == "IS") & (adj.cost_bps == 10.0)]
              .groupby(["stat", "block_L"])[["R", "decisive_share"]].mean().reset_index())
    oos_tab = (adj[(adj.window == "OOS") & (adj.cost_bps == 10.0)]
               .groupby(["stat", "block_L"])[["R", "decisive_share"]].mean().reset_index())
    wf = is_tab.merge(oos_tab, on=["stat", "block_L"], suffixes=("_IS", "_OOS"))
    wf = wf.sort_values("R_IS", ascending=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log("  IS-ranked, ALL 18 (statistic x block length) grid points:")
    for _, r in wf.iterrows():
        log(f"    {r.stat:9s} L={int(r.block_L):3d}  R_IS {r.R_IS:6.3f} (decisive {r.decisive_share_IS:5.1%})"
            f"  ->  R_OOS {r.R_OOS:6.3f} (decisive {r.decisive_share_OOS:5.1%})")
    pick = wf.iloc[0]
    log(f"  IS-ONLY PICK: stat = {pick.stat}, block L = {int(pick.block_L)}  "
        f"(R_IS {pick.R_IS:.3f}).  READ ONCE OOS: R_OOS {pick.R_OOS:.3f}, "
        f"decisive share OOS {pick.decisive_share_OOS:.1%}.")
    mx = wf[wf.stat == "MaxDD"].sort_values("R_IS", ascending=False).iloc[0]
    log(f"  INCUMBENT STATISTIC (MaxDD, best L by the same IS rule, L={int(mx.block_L)}): "
        f"R_IS {mx.R_IS:.3f} -> R_OOS {mx.R_OOS:.3f}, decisive OOS {mx.decisive_share_OOS:.1%}.")
    log(f"  LIFT of the IS-chosen statistic over MaxDD, OOS, read once: "
        f"R {pick.R_OOS:.3f} vs {mx.R_OOS:.3f} = {pick.R_OOS / mx.R_OOS:.2f}x; "
        f"decisive share {pick.decisive_share_OOS:.1%} vs {mx.decisive_share_OOS:.1%}.")

    # ================================================== PART 1: the census
    log("\n[PART 1] CENSUS of committed book-level MaxDD figures against the frozen incumbent.")
    files = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    files += sorted((ROOT / "research" / "backtests").glob("*.md"))
    trip = re.compile(r"(-?\d{1,3}\.\d{1,2})\s*%\s*/\s*(-?\d\.\d{2,4})\s*/\s*(-?\d{1,3}\.\d{1,2})\s*%")
    named = re.compile(r"[Mm]axDD[^%\n]{0,24}?(-\d{1,3}\.\d{1,2})\s*%")
    crows = []
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for m in trip.finditer(txt):
            dd = float(m.group(3))
            if -100 < dd < 0:
                crows.append(dict(file=f.name, kind="CAGR/Sharpe/MaxDD triple", maxdd_pp=dd))
        for m in named.finditer(txt):
            dd = float(m.group(1))
            if -100 < dd < 0:
                crows.append(dict(file=f.name, kind="named MaxDD", maxdd_pp=dd))
    cen = pd.DataFrame(crows)
    cen["contrast_pp"] = cen.maxdd_pp - ANCHOR_MAXDD_PP
    # this run's own measured SE for the MaxDD contrast, 10 bps, FULL window, per block length
    own_se = (se[(se.stat == "MaxDD") & (se.cost_bps == 10.0) & (se.window == "FULL")]
              .groupby("block_L").SE.median())
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    log(f"  {len(cen)} committed MaxDD figures found over {cen.file.nunique()} files "
        f"({(cen.kind == 'CAGR/Sharpe/MaxDD triple').sum()} triples, "
        f"{(cen.kind == 'named MaxDD').sum()} named).  -> {STEM}.census.csv")
    log(f"  median committed MaxDD {cen.maxdd_pp.median():.2f} pp, "
        f"median |contrast vs the anchor's {ANCHOR_MAXDD_PP:.2f} pp| = {cen.contrast_pp.abs().median():.2f} pp")
    for label, sd in [("1511's 2.93 pp", SE_1511)] + [(f"this run L={L}", float(own_se.loc[L])) for L in LS]:
        inside2 = float((cen.contrast_pp.abs() < 2 * sd).mean())
        inside1 = float((cen.contrast_pp.abs() < sd).mean())
        log(f"  against SE = {sd:.2f} pp ({label}): {inside1:6.1%} of committed MaxDD figures sit inside 1 SE "
            f"of the anchor, {inside2:6.1%} inside 2 SE (i.e. NOT distinguishable at |t| > 2)")

    (OUT / f"{STEM}.log.txt").write_text("\n".join(log_lines) + "\n")

if __name__ == "__main__":
    main()
