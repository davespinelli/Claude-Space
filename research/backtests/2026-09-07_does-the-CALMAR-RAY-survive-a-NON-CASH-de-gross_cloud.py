#!/usr/bin/env python3
"""Idea 383 - "does-the-CALMAR-RAY-survive-a-NON-CASH-de-gross" (cloud, 2026-09-07).

QUESTION (from QUEUE.md).  Idea 333 found that gross slides a book along a nearly FIXED
Calmar ray (max spread 0.0198 over gross, sign-correct 15/15), so de-grossing into CASH
trades CAGR for drawdown at a constant exchange rate and can never clear 4b's JOINT
DD+CAGR bar where it is not already cleared.  The mechanism is that cash earns 0, so at
gross g the book is g * (book) + (1-g) * (nothing) -- a ray through the ORIGIN, and
Calmar = CAGR/|MaxDD| is invariant along a ray through the origin.  Re-run idea 333's
n x gross grid with the UN-INVESTED weight held in a real asset instead of cash and ask
whether the ray TILTS enough to open a band where cash leaves none.

DESIGN.  Idea 333's grid verbatim -- family = idea 329's anchor arm (top-n of the v1
composite, vol scaler OFF, RULES v1 eligibility [200d MA up, vol20 < 0.60], NORM weights
w_i = g/k_t, band m=0, weekly, next-day execution) -- with ONE thing changed: what the
residual (1-g) of NAV is held in.

    CASH   residual earns 0                        (idea 333's convention, the control)
    SPY    residual held in SPY                    (the queue's first suggestion)
    SHY    residual held in SHY, 1-3y Treasuries   (the queue's T-bill proxy, cached)

TUNED PARAMETERS (max 2, as the queue specifies): n in {10, 20, 40, 80, ALL} x gross in
{0.375, 0.50, 0.625, 0.75} = 20 cells.  ALL 20 reported per panel per arm per cost rung
{0, 10, 25}.  The RESIDUAL ASSET is the treatment being priced, not a tuned dial -- all
three arms are always reported side by side and none is selected on.

BOOK CONSTRUCTION, and the one deviation from idea 333.  SPY and SHY are dropped from the
RANKED universe on EVERY panel (idea 333 dropped SPY only on SMALL439), so the residual
asset can never also be a holding and CASH-vs-SPY-vs-SHY is the only thing that moves
between arms.  The deviation is gated: G3 shows the cash arm at idea 333's own
drop_spy setting reproduces its committed (B136, n=20, g=0.75) row exactly, and G3b
prints what dropping SPY/SHY from the ranked universe costs, so the shift is priced
rather than assumed.

COSTS.  The residual sleeve is TRADED in the SPY and SHY arms and its turnover is charged
at the same rung as the book's.  Cash is not charged (holding cash has no spread).  This
deliberately handicaps the non-cash arms relative to a naive reading, and is the honest
treatment: rebalancing an ETF sleeve costs money.

PRE-REGISTERED READING.  Idea 333 established that on SMALL439 the admissible gross band
(DD cap AND CAGR floor jointly satisfiable) is EMPTY at 5/5 n, while on B136 and U56 it
is non-empty at 5/5.  SMALL439 is therefore the panel where "cash leaves none".  Fixed
before any number was read:

    TILTS   on a panel where the CASH band is empty at all 5 n, a non-cash residual makes
            it NON-EMPTY at >= 1 n AND that cell clears the FULL 4b conjunction AND the
            rule-8 pick on that panel/arm also clears 4b.
    PARTIAL bands open but no cell clears full 4b, or a cell clears 4b but rule 8 does not.
    NO TILT the bands stay empty wherever cash's were.

Reported regardless: the Calmar spread over gross per (panel, arm, n) -- the ray statistic
itself -- against idea 333's 0.0198 for cash; the linearity R2 of CAGR and MaxDD in gross
per arm (cash is near-exactly linear BY CONSTRUCTION, the non-cash arms need not be); and
the 4a/4b counts and rule-8 walk-forward on every arm.

RULE 8.  (n, gross) chosen on IS 2008-2016 Sharpe @10 bps per (panel, arm), 2017-2026 read
once; OOS CAGR/Sharpe/MaxDD reported against RULES v2 and SPY.

GATES (asserted and printed).  G1 fast_backtest == engine.backtest on returns and turnover
at 0 and 25 bps.  G2 the CASH arm run through the augmented code path (a constant-price
residual column) equals the implicit-cash path to 1e-12 -- the three arms share one engine.
G3 idea 333's committed (B136, n=20, g=0.75) row reproduced to 1e-9.  G4 g=1.0 makes the
residual weight zero, so all three arms coincide exactly.  G5 the SHY/SPY residual series
carry no NaN over any panel's evaluation window.

CAVEATS.  (1) All three panels are CURRENT-CONSTITUENT lists -- SURVIVORSHIP.  SMALL439 is
the sub-$2B screen with the max_1d_move >= 1.0 names dropped, as required; its 4b CAGR
floor is tested in the book's favour, which makes a NO TILT verdict there conservative and
a TILT verdict there generous.  (2) SHY is a 1-3y Treasury ETF, not a T-bill: it carries
real (small) duration risk and its 2022 drawdown is not zero.  (3) gross <= 0.75
throughout, so nothing here is leverage; the residual is a funding choice, not a size one.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights                             # noqa
from engine import backtest, metrics, rebalance_mask                                    # noqa

SLUG = "2026-09-07_does-the-CALMAR-RAY-survive-a-NON-CASH-de-gross_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, FREQ, WARMUP = 0.60, "W", 260
NS = [10, 20, 40, 80, "ALL"]
GROSSES = [0.375, 0.50, 0.625, 0.75]
COSTS = [0, 10, 25]
ARMS = ["CASH", "SPY", "SHY"]
RESID_COL = "_RESID"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CALMAR_MULT = 0.70 / 0.60          # idea 333's closed form for the joint DD+CAGR bar
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


# ------------------------------------------------------------------ panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    P(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} "
      f"names + SPY  (SURVIVORSHIP: current constituents of the screen only)")
    return px[keep]


def resid_series(arm, index):
    """Price path of the residual asset, reindexed onto a panel's trading days.
    CASH is a constant price (zero return), so the augmented path nests idea 333."""
    if arm == "CASH":
        return pd.Series(1.0, index=index, name=RESID_COL)
    p = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[arm]
    return p.reindex(index, method="ffill").rename(RESID_COL)


# ------------------------------------------- the book (idea 329/333's anchor arm)
def rank_frame(px, drop=()):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    for c in drop:
        if c in elig.columns:
            elig = elig.copy(); elig[c] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    return rk.notna() if n == "ALL" else rk <= n


def weights_from(sel, gross):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, cost_bps=0.0, freq=FREQ):
    """idea 325/329/333's backtester, verbatim.  Un-invested weight is IMPLICIT cash."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT); cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = px.index
    return (pd.Series(np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4, index=idx),
            pd.Series(turn, index=idx), pd.Series(np.nansum(held, axis=1), index=idx),
            pd.Series((held > 0).sum(axis=1), index=idx))


def run_arm(px_aug, sel, gross, arm):
    """The book at `gross` with the residual (1-gross) parked in `arm`.

    CASH  -> the residual is left implicit, exactly as idea 333 priced it (uncharged).
    SPY/SHY -> the residual is an EXPLICIT column, so it accrues that asset's return AND
    its rebalancing turnover is charged at the same rung as the book's.
    Returns (gross_returns, turnover, realised_gross_in_the_BOOK, mean_names)."""
    w = weights_from(sel, gross)
    if arm != "CASH":
        w = w.copy(); w[RESID_COL] = 1.0 - gross
    w = w.reindex(columns=px_aug.columns, fill_value=0.0)   # CASH -> residual weight 0
    r, t, gr, nn = fast_backtest(px_aug, w, 0.0, FREQ)
    return r, t, gr, nn


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2,
         "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def linfit(x, y):
    """least squares y = a + b x, returns (a, b, R2)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 2 or np.std(x) == 0: return (np.nan, np.nan, np.nan)
    b, a = np.polyfit(x, y, 1)
    yh = a + b * x
    ss = float(((y - y.mean()) ** 2).sum())
    return (float(a), float(b), 1.0 - float(((y - yh) ** 2).sum()) / ss if ss > 0 else np.nan)


def gross_interval(sub, dd_cap, cagr_floor):
    """Invert the two bars into a gross interval, per idea 333's method.
    MaxDD and CAGR are fitted linear in gross; returns (g_lo, g_hi, r2_dd, r2_cg)."""
    a_d, b_d, r2d = linfit(sub.gross, sub.MaxDD.abs())      # |MaxDD| = a_d + b_d * g
    a_c, b_c, r2c = linfit(sub.gross, sub.CAGR)             # CAGR    = a_c + b_c * g
    g_hi = (dd_cap - a_d) / b_d if b_d not in (0, np.nan) and b_d != 0 else np.nan
    g_lo = (cagr_floor - a_c) / b_c if b_c != 0 else np.nan
    if b_d < 0: g_hi = np.inf if dd_cap >= a_d else g_hi    # shallower as g rises: unusual
    return g_lo, g_hi, r2d, r2c


# ============================================================================ main
def main():
    P(f"=== idea 383 — does the CALMAR RAY survive a NON-CASH de-gross?  ({SLUG}) ===")
    P("Family: idea 329/333's anchor arm (composite, vol scaler OFF, v1 eligibility, NORM "
      "weights, m=0, weekly).")
    P(f"Tuned params (2): n in {NS} x gross in {GROSSES} = {len(NS)*len(GROSSES)} cells, "
      f"ALL reported, at {COSTS} bps.")
    P(f"Treatment (not a tuned dial, always reported side by side): residual asset in {ARMS}.")
    P("Pre-registered: TILTS iff on a panel where the CASH gross band is EMPTY at 5/5 n, a "
      "non-cash residual opens it at >=1 n AND that cell clears full 4b AND rule 8 agrees.")

    P("\n[panels]")
    panels = {"B136": load_universe(broad=True), "U56": load_universe(),
              "SMALL439": small_panel()}

    # ------------------------------------------------------------------ gates
    P("\n[0] GATES")
    bpx = panels["B136"]
    start_b = bpx.index[WARMUP]
    rk333, _ = rank_frame(bpx, drop=())                    # idea 333's B136 setting
    w333 = weights_from(sel_hard(rk333, 20), 0.75)
    fr, ft, _, _ = fast_backtest(bpx, w333, 0.0, FREQ)
    for c in (0, 25):
        eng = backtest(bpx, w333, cost_bps=c, freq=FREQ)
        d1 = float(np.abs(eng["returns"].loc[start_b:] - (fr - ft * c / 1e4).loc[start_b:]).max())
        d2 = float(np.abs(eng["turnover"].loc[start_b:] - ft.loc[start_b:]).max())
        P(f"    G1 cost_bps={c:>2}: max|dr| {d1:.3e}  max|dturn| {d2:.3e}")
        assert d1 < 1e-12 and d2 < 1e-12
    aug = pd.concat([bpx, resid_series("CASH", bpx.index)], axis=1)
    w_aug = w333.copy(); w_aug[RESID_COL] = 1.0 - 0.75
    ra, ta, _, _ = fast_backtest(aug, w_aug, 0.0, FREQ)
    d_g2 = float(np.abs((ra - fr).loc[start_b:]).max())
    P(f"    G2 explicit constant-price residual == implicit cash: max|dr| {d_g2:.3e} "
      f"(turnover differs by construction: the cash sleeve's own trades, "
      f"max {float((ta-ft).loc[start_b:].max()):.4f}/reb, and are NOT charged in the CASH arm)")
    assert d_g2 < 1e-12
    r10 = (fr - ft * 10 / 1e4).loc[start_b:]
    m10 = metrics(r10); h1_, h2_ = hs(r10)
    tgt = dict(CAGR=0.12992958836952506, Sharpe=0.9431848997615343,
               MaxDD=-0.2005204833110832, H1=1.1047866702854354, H2=0.8025166021122436,
               OOS_Sharpe=metrics(r10.loc[OOS_START:])["Sharpe"])
    got = dict(CAGR=m10["CAGR"], Sharpe=m10["Sharpe"], MaxDD=m10["MaxDD"], H1=h1_, H2=h2_,
               OOS_Sharpe=metrics(r10.loc[OOS_START:])["Sharpe"])
    d_g3 = max(abs(got[k] - v) for k, v in tgt.items() if k != "OOS_Sharpe")
    P(f"    G3 (B136, n=20, g=0.75, idea 333's drop setting) vs its committed row: "
      f"max|d| {d_g3:.3e}   [CAGR {got['CAGR']:.4%} Sharpe {got['Sharpe']:.4f} "
      f"MaxDD {got['MaxDD']:.4%} OOS {got['OOS_Sharpe']:.4f}]")
    assert d_g3 < 1e-9
    rk_d, _ = rank_frame(bpx, drop=("SPY", "SHY"))
    frd, ftd, _, _ = fast_backtest(bpx, weights_from(sel_hard(rk_d, 20), 0.75), 0.0, FREQ)
    rd10 = (frd - ftd * 10 / 1e4).loc[start_b:]
    md = metrics(rd10)
    P(f"    G3b what dropping SPY+SHY from the RANKED universe costs on B136 (n=20, "
      f"g=0.75, 10 bps): dCAGR {md['CAGR']-m10['CAGR']:+.4%}  dSharpe "
      f"{md['Sharpe']-m10['Sharpe']:+.4f}  dMaxDD {md['MaxDD']-m10['MaxDD']:+.4%} "
      f"— priced, not assumed; every arm below uses the dropped universe")
    for arm in ARMS:
        rr = resid_series(arm, bpx.index)
        assert rr.notna().all(), arm
    P(f"    G5 residual series {ARMS} carry no NaN on B136's index: OK")

    # ------------------------------------------------------------------ the grid
    rows = []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        calmar_spy = ms_["CAGR"] / abs(ms_["MaxDD"])
        dd_cap, cg_floor = 0.60 * abs(ms_["MaxDD"]), 0.70 * ms_["CAGR"]
        rk, elig = rank_frame(px, drop=("SPY", "SHY"))
        P(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
          f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        P(f"    eligible/day mean {elig.sum(axis=1).loc[start:].mean():.1f}")
        P(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
          f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%}")
        P(f"    4b bars: H1>{s1:.3f} H2>{s2:.3f} OOS>{so['Sharpe']:.3f} "
          f"|MaxDD|<={dd_cap:.2%} CAGR>={cg_floor:.2%} | Calmar_SPY {calmar_spy:.4f} -> "
          f"joint bar Calmar >= {CALMAR_MULT*calmar_spy:.4f}")
        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0, FREQ)
        base = {c: (br - bt * c / 1e4).loc[start:] for c in COSTS}
        bm = metrics(base[10]); b1, b2 = hs(base[10])
        P(f"    RULES v2 (live, weekly, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
          f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS "
          f"{metrics(base[10].loc[OOS_START:])['Sharpe']:.3f}")
        for arm in ARMS:
            rs = resid_series(arm, px.index)
            aug = pd.concat([px, rs], axis=1)
            rm = metrics(rs.pct_change().fillna(0).loc[start:])
            P(f"    residual arm {arm:4s}: CAGR {rm['CAGR']:7.2%} Sharpe {rm['Sharpe']:7.3f} "
              f"MaxDD {rm['MaxDD']:7.2%}")
            for n in NS:
                sel = sel_hard(rk, n)
                for g in GROSSES:
                    r0, t0, gr, nn = run_arm(aug, sel, g, arm)
                    row = dict(panel=pname, arm=arm, n=str(n), gross=g,
                               turn_per_yr=float(t0.loc[start:].sum()
                                                 / (len(t0.loc[start:]) / 252.0)),
                               names=float(nn.loc[start:].mean()),
                               realised_gross=float(gr.loc[start:].mean()),
                               calmar_spy=calmar_spy, calmar_bar=CALMAR_MULT * calmar_spy,
                               dd_cap=dd_cap, cg_floor=cg_floor,
                               spy_H1=s1, spy_H2=s2, spy_OOS=so["Sharpe"],
                               spy_CAGR=ms_["CAGR"], spy_MaxDD=ms_["MaxDD"])
                    for c in COSTS:
                        r = (r0 - t0 * c / 1e4).loc[start:]
                        m = metrics(r); hh1, hh2 = hs(r)
                        ok4b, d4b, f4b = bars_4b(r, spy)
                        ok4a, _, f4a = bars_4a(r, base[c])
                        row.update({f"CAGR_{c}": m["CAGR"], f"Sharpe_{c}": m["Sharpe"],
                                    f"MaxDD_{c}": m["MaxDD"],
                                    f"Calmar_{c}": m["CAGR"] / abs(m["MaxDD"]),
                                    f"H1_{c}": hh1, f"H2_{c}": hh2,
                                    f"OOS_Sharpe_{c}": metrics(r.loc[OOS_START:])["Sharpe"],
                                    f"OOS_CAGR_{c}": metrics(r.loc[OOS_START:])["CAGR"],
                                    f"OOS_MaxDD_{c}": metrics(r.loc[OOS_START:])["MaxDD"],
                                    f"IS_Sharpe_{c}": metrics(r.loc[:IS_END])["Sharpe"],
                                    f"ddok_{c}": d4b["DD"] >= 0, f"cgok_{c}": d4b["CAGR"] >= 0,
                                    f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                    f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a)})
                    rows.append(row)
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    P(f"\n[1] grid: {len(G)} rows -> {SLUG}.grid.csv "
      f"({len(panels)} panels x {len(ARMS)} arms x {len(NS)*len(GROSSES)} cells)")

    # G4: at g -> 1 the residual weight vanishes and the arms must coincide.  0.75 is the
    # top of the pre-registered ladder, so this is run as a separate identity check.
    P("\n    G4 identity check at gross = 1.0 (residual weight zero -> arms must coincide):")
    aug_s = pd.concat([panels["U56"], resid_series("SPY", panels["U56"].index)], axis=1)
    aug_c = pd.concat([panels["U56"], resid_series("CASH", panels["U56"].index)], axis=1)
    rk_u, _ = rank_frame(panels["U56"], drop=("SPY", "SHY"))
    s_u = sel_hard(rk_u, 20)
    r_s, _, _, _ = run_arm(aug_s, s_u, 1.0, "SPY")
    r_c, _, _, _ = run_arm(aug_c, s_u, 1.0, "CASH")
    d_g4 = float(np.abs(r_s - r_c).max())
    P(f"      max|d returns| {d_g4:.3e}")
    assert d_g4 < 1e-12

    # --------------------------------------------- [2] the ray statistic itself
    P("\n[2] THE CALMAR RAY — spread of Calmar over the gross ladder, per (panel, arm, n) "
      "@10 bps")
    P("    idea 333 measured max spread 0.0198 for CASH.  A ray through the origin is "
      "Calmar-invariant;")
    P("    a residual with its own return/drawdown TILTS it.  Bigger spread = more tilt.")
    ray = []
    for (pn, arm, n), sub in G.groupby(["panel", "arm", "n"]):
        sub = sub.sort_values("gross")
        c = sub["Calmar_10"]
        a_d, b_d, r2d = linfit(sub.gross, sub.MaxDD_10.abs())
        a_c, b_c, r2c = linfit(sub.gross, sub.CAGR_10)
        ray.append(dict(panel=pn, arm=arm, n=n, calmar_lo=float(c.min()),
                        calmar_hi=float(c.max()), calmar_spread=float(c.max() - c.min()),
                        calmar_at_min_g=float(sub.Calmar_10.iloc[0]),
                        calmar_at_max_g=float(sub.Calmar_10.iloc[-1]),
                        calmar_bar=float(sub.calmar_bar.iloc[0]),
                        clears_bar_any=bool((c >= sub.calmar_bar).any()),
                        dd_intercept=a_d, dd_slope=b_d, dd_R2=r2d,
                        cagr_intercept=a_c, cagr_slope=b_c, cagr_R2=r2c))
    R = pd.DataFrame(ray)
    R.to_csv(OUT / f"{SLUG}.ray.csv", index=False)
    P(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n    max Calmar spread over gross, by (panel, arm):")
    piv = R.pivot_table(index="panel", columns="arm", values="calmar_spread", aggfunc="max")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n    linearity of |MaxDD| and CAGR in gross (min R2 over the 5 n), by (panel, arm):")
    lin = R.groupby(["panel", "arm"])[["dd_R2", "cagr_R2"]].min()
    P(lin.to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------- [3] the admissible gross band (the queue's question)
    P("\n[3] THE ADMISSIBLE GROSS BAND (DD cap AND CAGR floor jointly satisfiable) @10 bps")
    P("    Bars inverted into a gross interval per idea 333's method (linear fits above).")
    P("    A band is EMPTY when g_lo(CAGR floor) > g_hi(DD cap).  Extrapolation beyond the")
    P("    tested ladder [0.375, 0.750] is FLAGGED, never claimed.")
    band = []
    for (pn, arm, n), sub in G.groupby(["panel", "arm", "n"]):
        sub = sub.sort_values("gross").rename(columns={"MaxDD_10": "MaxDD", "CAGR_10": "CAGR"})
        g_lo, g_hi, r2d, r2c = gross_interval(sub, float(sub.dd_cap.iloc[0]),
                                              float(sub.cg_floor.iloc[0]))
        obs_ok = sub[(sub.MaxDD.abs() <= sub.dd_cap) & (sub.CAGR >= sub.cg_floor)]
        band.append(dict(panel=pn, arm=arm, n=n, g_lo=g_lo, g_hi=g_hi,
                         nonempty=bool(np.isfinite(g_lo) and np.isfinite(g_hi) and g_lo <= g_hi),
                         width=(g_hi - g_lo) if np.isfinite(g_lo) and np.isfinite(g_hi) else np.nan,
                         inside_tested=bool(np.isfinite(g_lo) and np.isfinite(g_hi)
                                            and g_lo >= min(GROSSES) and g_hi <= max(GROSSES)),
                         observed_cells_both_bars=len(obs_ok),
                         dd_R2=r2d, cagr_R2=r2c))
    B = pd.DataFrame(band)
    B.to_csv(OUT / f"{SLUG}.band.csv", index=False)
    P(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n    non-empty bands (of 5 n) and observed cells clearing BOTH bars, by "
      "(panel, arm):")
    summ = B.groupby(["panel", "arm"]).agg(nonempty_of_5=("nonempty", "sum"),
                                           observed_both=("observed_cells_both_bars", "sum"))
    P(summ.to_string())

    # ------------------------------------------------ [4] KEEP paths on every arm
    P("\n[4] KEEP PATHS — 4a (vs RULES v2) and 4b (vs SPY), every cell, every rung")
    for c in COSTS:
        P(f"    @{c:>2} bps:")
        for (pn, arm), sub in G.groupby(["panel", "arm"]):
            P(f"      {pn:9s} {arm:4s}  4a {int(sub[f'keep4a_{c}'].sum()):>2}/{len(sub)}   "
              f"4b {int(sub[f'keep4b_{c}'].sum()):>2}/{len(sub)}")
    k10 = G[G.keep4b_10]
    if len(k10):
        P("\n    4b passers @10 bps:")
        P(k10[["panel", "arm", "n", "gross", "CAGR_10", "Sharpe_10", "MaxDD_10",
               "Calmar_10", "H1_10", "H2_10", "OOS_Sharpe_10", "turn_per_yr"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("\n    no 4b passers @10 bps")
    ff = G[~G.keep4b_10].fail4b_10.str.split(",").explode()
    P("\n    first-failing 4b bars @10 bps (all arms pooled): "
      + ", ".join(f"{k} {v}" for k, v in ff.value_counts().items()))
    P(f"    4a passers @10 bps: {int(G.keep4a_10.sum())}/{len(G)}")

    # -------------------------------------------------------------- [5] rule 8
    P("\n[5] RULE 8 WALK-FORWARD — (n, gross) chosen on IS 2008-2016 Sharpe @10 bps, "
      "2017-2026 read once")
    wf = []
    for (pn, arm), sub in G.groupby(["panel", "arm"]):
        pick = sub.loc[sub.IS_Sharpe_10.idxmax()]
        px = panels[pn]; start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0, FREQ)
        b10 = (br - bt * 10 / 1e4).loc[start:]
        wf.append(dict(panel=pn, arm=arm, pick_n=pick.n, pick_gross=pick.gross,
                       IS_Sharpe=pick.IS_Sharpe_10, OOS_CAGR=pick.OOS_CAGR_10,
                       OOS_Sharpe=pick.OOS_Sharpe_10, OOS_MaxDD=pick.OOS_MaxDD_10,
                       full_CAGR=pick.CAGR_10, full_Sharpe=pick.Sharpe_10,
                       full_MaxDD=pick.MaxDD_10, H1=pick.H1_10, H2=pick.H2_10,
                       spy_OOS=metrics(spy.loc[OOS_START:])["Sharpe"],
                       spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                       v2_OOS=metrics(b10.loc[OOS_START:])["Sharpe"],
                       v2_OOS_CAGR=metrics(b10.loc[OOS_START:])["CAGR"],
                       best_OOS=float(sub.OOS_Sharpe_10.max()),
                       regret=float(sub.OOS_Sharpe_10.max()) - pick.OOS_Sharpe_10,
                       keep4b=bool(pick.keep4b_10), keep4a=bool(pick.keep4a_10)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n    picks above SPY OOS: {int((W.OOS_Sharpe > W.spy_OOS).sum())}/{len(W)} | "
      f"above RULES v2 OOS: {int((W.OOS_Sharpe > W.v2_OOS).sum())}/{len(W)} | "
      f"clearing 4b: {int(W.keep4b.sum())}/{len(W)} | 4a: {int(W.keep4a.sum())}/{len(W)} | "
      f"mean regret {W.regret.mean():+.4f}")

    # ------------------------------------------------------------- [6] verdict
    P("\n[6] PRE-REGISTERED READING")
    cash_empty = {pn for pn in panels
                  if int(B[(B.panel == pn) & (B.arm == "CASH")].nonempty.sum()) == 0}
    P(f"    panels where the CASH band is EMPTY at 5/5 n (idea 333's 'cash leaves none'): "
      f"{sorted(cash_empty) if cash_empty else 'none'}")
    opened, opened_4b, opened_wf = [], [], []
    for pn in sorted(cash_empty):
        for arm in ARMS:
            if arm == "CASH": continue
            k = int(B[(B.panel == pn) & (B.arm == arm)].nonempty.sum())
            n4b = int(G[(G.panel == pn) & (G.arm == arm)].keep4b_10.sum())
            wfk = bool(W[(W.panel == pn) & (W.arm == arm)].keep4b.iloc[0])
            P(f"      {pn} + {arm:4s} residual: non-empty bands {k}/5, "
              f"cells clearing full 4b @10bps {n4b}/20, rule-8 pick clears 4b {wfk}")
            if k > 0: opened.append((pn, arm))
            if n4b > 0: opened_4b.append((pn, arm))
            if wfk: opened_wf.append((pn, arm))
    if opened_4b and opened_wf:
        v = ("TILTS — a non-cash residual opens a band, clears full 4b and survives rule 8 "
             f"on {opened_wf}")
    elif opened or opened_4b:
        v = ("PARTIAL — a non-cash residual moves the band but does not deliver a "
             "4b-clearing, rule-8-surviving cell where cash leaves none")
    else:
        v = ("NO TILT — the Calmar ray survives a non-cash de-gross; the band stays empty "
             "everywhere cash's was")
    P(f"    VERDICT: {v}")
    P("\n    CAVEATS: every panel is a current-constituent list (SURVIVORSHIP), so 4b's CAGR "
      "floor is tested in each book's favour — which makes a NO-TILT reading on SMALL439 "
      "conservative; SHY is a 1-3y Treasury ETF, not a T-bill, and carries real duration "
      "(its 2022 drawdown is not zero); gross <= 0.75 throughout, so nothing here is "
      "leverage; and the SPY/SHY sleeves are CHARGED their own turnover while cash is not.")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")
    return v


if __name__ == "__main__":
    main()
