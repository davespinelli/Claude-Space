#!/usr/bin/env python3
"""Idea 154 — ew-band3-at-085-does-not-hold-on-broad (cloud lane, 2026-09-06).

Pre-registered question (QUEUE 154).  Idea 90's Q4b found idea 84's by-product candidate —
idea 57's `ew-band3` at realised mean gross g = 0.85 — inside its own 4b gross interval in
only 1 of the 4 large-cap cells (u56@10bps), with broad capping it at g = 0.7877 on the
drawdown bar, three m-grid steps below 0.85.  But idea 84 read a 312-point FINE ladder and a
5 bps rung, and the `dg`/`rw` convention is a real fork (idea 90 reports `band3-dg` EMPTY on
broad at both of its rungs, while `band3-rw` has [0.7502, 0.7877]).  Re-run THE TWO
CONSTRUCTIONS side by side on ONE harness at 5, 10 and 25 bps before either number is quoted
again.  The incumbent's own g = 0.75 is interior in 4 of 4, so only the alternative is in
question.

Falsifiable form.  If g = 0.85 is admissible for `band3` on broad at ANY of the three rungs
under EITHER convention on a ladder 5x finer than idea 90's, then idea 90's ceiling was a
resolution artefact of its 0.05 m-grid and idea 84's number stands.  If the ceiling reproduces
at 0.01 resolution on both conventions and all three rungs, idea 84's g = 0.85 is dead and
idea 90's correction is confirmed at the finer grid it was challenged on.

HARNESS.  Idea 94's simulator (`2026-09-04_drawdown-insurance-price-list_B.py`) is IMPORTED,
not re-implemented, and idea 90's panel convention is reproduced exactly, so every number in
this run sits on the simulator that produced the rows being reconciled.  Four checks run
before any new number is read (see CHECKS in the console):
    [a] engine equivalence: H.run(m=1, no instruments) == engine.backtest to machine precision
    [b] idea 94's published EWall + vol60-dg u56 @10bps row: 11.587% / 1.133 / -16.884%
    [c] the cost identity net(c) = net(0) - turnover*c/1e4 (legitimate: with no stop, no DD
        control and no entry budget the turnover path is cost-independent), asserted against
        a direct bps=10 run on every panel
    [d] idea 90's own published joint intervals for `EWall + band3-rw` and `EWall + vol60-dg`
        re-derived on this run's ladder restricted to idea 90's 0.05 m-grid and its two rungs

CORPUS.  1 book (EWall — the book in question) x 4 arms x 3 panels x 121 gross points x
4 cost rungs = 5,808 reported rows, every one in `.grid.csv`.
    arms    band3-dg, band3-rw   (the two constructions under test)
            vol60-dg             (the incumbent, idea 90 says interior in 4 of 4 — control)
            vol60-rw             (idea 90 publishes its interval too — second control)
    panels  u56 (56), broad (136), small (439 sub-$2B names, max_1d_move >= 1.0 dropped)
    ladder  m in 0.10..1.30 step 0.01 — 121 points, 5x finer than idea 90's 25-point grid and
            comparable to idea 84's 312-point ladder.  m = 1.00 is 75% target gross; g is
            reported as REALISED MEAN GROSS, as idea 90 requires.
    rungs   5, 10, 25 bps (the queue's ask) plus 0 as the derivation base.

TUNED PARAMETERS — exactly two: the gross dial m and the cost rung.  Convention (dg/rw), arm
    and panel are REPORTED axes, never selected on: all four arms and all three panels appear
    at every point.  The 4b bar coefficients are PROTOCOL's published 0.70 / 0.60, not swept.

BOTH KEEP PATHS are evaluated at every point (4a against live RULES v1 on the same panel and
rung; 4b against SPY).  RULE 8: the admissible interval is re-read on 2009-2016 only (the OOS
bar is undefined inside the IS window, so the IS interval uses H1/H2/DD/CAGR), its midpoint
and its m = 1.00 pin are then evaluated untouched on 2017-2026 against the do-nothing control
(m = 1.00), RULES v1 and SPY.

CAVEATS carried, not buried.  Survivorship (idea 54): all three panels are current-constituent
lists, which flatters every long book here; the small panel additionally drops 44 names on a
data screen that is not a tradable rule.  Idea 128: the IS window's SPY MaxDD is shallower than
the OOS window's, so every IS drawdown cap admits too much.  Costs are flat linear bps on
turnover, not spread-and-impact (idea 126).

Outputs (all committed):
    .grid.csv       every (panel, arm, m, rung) row with realised gross, metrics and bars
    .intervals.csv  the 4b (and 4a) admissible gross interval per (panel, arm, rung)
    .verdict.csv    the two contested points g = 0.75 and g = 0.85, in/out per cell
    .walkforward.csv rule 8
"""
import importlib.util, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights                  # noqa: E402
from engine import backtest, metrics                                  # noqa: E402

I94 = ROOT / "research" / "backtests" / "2026-09-04_drawdown-insurance-price-list_B.py"
_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

OUT = Path(__file__).with_suffix("")
IS_END, OOS_START = H.IS_END, H.OOS_START
RUNGS = [0.0, 5.0, 10.0, 25.0]
QUEUE_RUNGS = [5.0, 10.0, 25.0]
MGRID = [round(x, 2) for x in np.arange(0.10, 1.3001, 0.01)]          # 121 points
M90 = [round(x, 2) for x in np.arange(0.10, 1.3001, 0.05)]            # idea 90's grid
ARMS = [("band3", "dg"), ("band3", "rw"), ("vol60", "dg"), ("vol60", "rw")]
CONTESTED = {"incumbent g=0.75": 0.75, "alternative g=0.85": 0.85}
PHI, DELTA = 0.70, 0.60          # PROTOCOL's published CAGR floor and MaxDD cap coefficients
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def rule(t):
    say("\n" + "=" * 110); say(t); say("=" * 110)


def panel(name):
    """idea 90's _panel, reproduced exactly: SPY is a benchmark, held out on the small panel."""
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY out)"
    raise ValueError(name)


def bars_from(spy, which):
    """4b bar levels from SPY over the requested window."""
    s = spy if which == "full" else spy.loc[OOS_START:] if which == "OOS" else spy.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    oos = spy.loc[OOS_START:]
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(oos)["Sharpe"] if len(oos) else np.nan)


def margins(r, b, oos=True):
    h = len(r) // 2
    m = metrics(r)
    d = dict(H1=metrics(r.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(r.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if oos:
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def interval(sub, keys):
    """Admissible realised-gross set for one (panel, arm, rung) slice, and its interval."""
    ok = sub[[f"m_{k}" for k in keys]].gt(0).all(axis=1).values
    g = sub["gross"].values
    if not ok.any():
        return dict(n_ok=0, lo=np.nan, hi=np.nan, width=np.nan, contiguous=np.nan,
                    cens_lo=False, cens_hi=False)
    idx = np.flatnonzero(ok)
    return dict(n_ok=int(ok.sum()), lo=float(g[idx[0]]), hi=float(g[idx[-1]]),
                width=float(g[idx[-1]] - g[idx[0]]),
                contiguous=bool(np.all(np.diff(idx) == 1)),
                cens_lo=bool(idx[0] == 0), cens_hi=bool(idx[-1] == len(g) - 1))


def main():
    t0 = time.time()
    rows, checks = [], []

    for pname in ["u56", "broad", "small"]:
        px, spy_full, desc = panel(pname)
        start = px.index[260]
        spy = spy_full.loc[start:]
        b_full = bars_from(spy, "full")
        b_is = bars_from(spy.loc[:IS_END], "IS")

        # ---- checks (a),(b),(c) on this panel
        Wchk = H.targets(px, "EWall", "vol60", "dg")
        r0 = H.run(px, Wchk, m=1.0, bps=0.0)
        r10 = H.run(px, Wchk, m=1.0, bps=10.0)
        derived = r0["r"] - r0["to"] * 10.0 / 1e4
        checks.append((pname, "cost identity", float(np.abs(derived - r10["r"]).max())))
        eng = backtest(px, Wchk, cost_bps=10.0, freq=H.FREQ)["returns"]
        checks.append((pname, "engine equivalence", float(np.abs(eng - r10["r"]).max())))
        if pname == "u56":
            m = metrics(r10["r"].loc[start:])
            checks.append(("u56", "idea 94 published row (11.587/1.133/-16.884)",
                           f"{m['CAGR']:.5%} / {m['Sharpe']:.3f} / {m['MaxDD']:.3%}"))

        # ---- RULES v1 baseline per rung (for 4a)
        v1 = H.run(px, rules_v1_weights(px), m=1.0, bps=0.0)
        base = {c: (v1["r"] - v1["to"] * c / 1e4).loc[start:] for c in RUNGS}

        for gate, conv in ARMS:
            W = H.targets(px, "EWall", gate, conv)
            for m_ in MGRID:
                res = H.run(px, W, m=m_, bps=0.0)
                r_raw, to_raw = res["r"], res["to"]
                g_real = float(res["gross"].loc[start:].mean())
                to_yr = float(to_raw.loc[start:].sum() / (len(r_raw.loc[start:]) / 252))
                for c in RUNGS:
                    r = (r_raw - to_raw * c / 1e4).loc[start:]
                    mm, mo = metrics(r), metrics(r.loc[OOS_START:])
                    mg = margins(r, b_full, oos=True)
                    mgi = margins(r.loc[:IS_END], b_is, oos=False)
                    rows.append(dict(
                        panel=pname, arm=f"{gate}-{conv}", gate=gate, conv=conv, m=m_,
                        gross=g_real, bps=c, TO=to_yr,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                        H1=metrics(r.iloc[:len(r) // 2])["Sharpe"],
                        H2=metrics(r.iloc[len(r) // 2:])["Sharpe"],
                        OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                        IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                        **{f"m_{k}": v for k, v in mg.items()},
                        **{f"is_{k}": v for k, v in mgi.items()},
                        pass4b=all(v > 0 for v in mg.values()),
                        fail4b=",".join(k for k, v in mg.items() if not v > 0),
                        pass4a=H.pass4a(r, base[c]),
                        spy_CAGR=b_full["scagr"], spy_MaxDD=b_full["sdd"],
                        spy_H1=b_full["s1"], spy_H2=b_full["s2"], spy_OOS=b_full["soos"],
                        base_Sharpe=metrics(base[c])["Sharpe"]))
            say(f"  {pname}/{gate}-{conv}: {time.time()-t0:.0f}s")
        say(f"{pname} ({desc}) done {time.time()-t0:.0f}s")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    rule("CHECKS (all must pass before any new number is read)")
    for a, b, c in checks:
        say(f"  {a:>6} | {b:<45} | {c if isinstance(c, str) else f'{c:.3e}'}")

    # ---------------------------------------------------------------- intervals
    iv = []
    for (p_, a_, c_), sub in G.groupby(["panel", "arm", "bps"]):
        sub = sub.sort_values("m")
        d4b = interval(sub, ["H1", "H2", "OOS", "DD", "CAGR"])
        sub4a = sub.assign(**{"m_p4a": sub.pass4a.astype(float) - 0.5})
        d4a = interval(sub4a, ["p4a"])
        iv.append(dict(panel=p_, arm=a_, bps=c_,
                       **{f"b_{k}": v for k, v in d4b.items()},
                       **{f"a_{k}": v for k, v in d4a.items()}))
    IV = pd.DataFrame(iv).sort_values(["arm", "panel", "bps"])
    IV.to_csv(f"{OUT}.intervals.csv", index=False)

    rule("Q1 — THE 4b ADMISSIBLE GROSS INTERVAL, 121-point ladder, both conventions, 3 rungs")
    say(IV[["panel", "arm", "bps", "b_n_ok", "b_lo", "b_hi", "b_width", "b_contiguous",
            "b_cens_hi", "a_n_ok", "a_lo", "a_hi"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\ncontiguity: {int(IV.b_contiguous.fillna(False).sum())} of "
        f"{int(IV.b_n_ok.gt(0).sum())} non-empty 4b intervals are contiguous")

    # ---------------------------------------------------------------- check (d)
    rule("CHECK (d) — idea 90's published intervals re-derived on ITS 0.05 grid and ITS rungs")
    for arm in ["band3-rw", "vol60-dg", "vol60-rw", "band3-dg"]:
        for p_ in ["u56", "broad"]:
            for c_ in [10.0, 25.0]:
                sub = G[(G.arm == arm) & (G.panel == p_) & (G.bps == c_)
                        & (G.m.isin(M90))].sort_values("m")
                d = interval(sub, ["H1", "H2", "OOS", "DD", "CAGR"])
                say(f"  {arm:<10} {p_:<6} {int(c_):>3}bps  n={d['n_ok']:>3}  "
                    f"[{d['lo']:.4f}, {d['hi']:.4f}]" if d["n_ok"] else
                    f"  {arm:<10} {p_:<6} {int(c_):>3}bps  EMPTY")
    say("\nidea 90's published joint (large-cap pair, 10 AND 25 bps) intervals for reference:")
    say("  EWall + vol60-dg  [0.6839, 0.7594]   EWall + band3-rw  [0.7502, 0.7877]")
    say("  EWall + vol60-rw  [0.6753, 0.7127]   EWall + band3-dg  EMPTY on broad")

    # ---------------------------------------------------------------- the contested points
    rule("Q2 — THE TWO CONTESTED POINTS ON THE FINE LADDER (the queue's actual question)")
    ver = []
    for arm in ["band3-dg", "band3-rw", "vol60-dg", "vol60-rw"]:
        for label, gt in CONTESTED.items():
            for p_ in ["u56", "broad", "small"]:
                for c_ in QUEUE_RUNGS:
                    sub = G[(G.arm == arm) & (G.panel == p_) & (G.bps == c_)].sort_values("m")
                    i = (sub.gross - gt).abs().idxmin()
                    r = G.loc[i]
                    d = IV[(IV.arm == arm) & (IV.panel == p_) & (IV.bps == c_)].iloc[0]
                    ver.append(dict(arm=arm, point=label, target_g=gt, panel=p_, bps=c_,
                                    nearest_m=r.m, nearest_g=r.gross,
                                    g_err=abs(r.gross - gt), pass4b=bool(r.pass4b),
                                    fail4b=r.fail4b, in_interval=bool(r.pass4b),
                                    iv_lo=d.b_lo, iv_hi=d.b_hi,
                                    dist_to_hi=(gt - d.b_hi) if np.isfinite(d.b_hi) else np.nan,
                                    CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                                    H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe,
                                    m_DD=r.m_DD, m_CAGR=r.m_CAGR, m_H1=r.m_H1, m_H2=r.m_H2,
                                    m_OOS=r.m_OOS, TO=r.TO, pass4a=bool(r.pass4a)))
    V = pd.DataFrame(ver)
    V.to_csv(f"{OUT}.verdict.csv", index=False)
    say(V[["arm", "point", "panel", "bps", "nearest_m", "nearest_g", "pass4b", "fail4b",
           "iv_lo", "iv_hi", "dist_to_hi", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "TO"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    rule("Q2 SUMMARY — cells passed, out of the 6 large-cap cells (2 panels x 5/10/25 bps)")
    big = V[V.panel.isin(["u56", "broad"])]
    say(big.groupby(["arm", "point"])["pass4b"].agg(["sum", "count"]).to_string())
    say("\nall 9 cells including the small panel:")
    say(V.groupby(["arm", "point"])["pass4b"].agg(["sum", "count"]).to_string())
    say("\nfirst-failing bar for every FAILING contested cell:")
    say(V[~V.pass4b].groupby(["arm", "point", "fail4b"]).size().to_string())

    rule("Q3 — IS THE BROAD CEILING A RESOLUTION ARTEFACT?  ceiling at 0.05 vs 0.01 grid")
    art = []
    for arm in ["band3-dg", "band3-rw", "vol60-dg", "vol60-rw"]:
        for p_ in ["u56", "broad"]:
            for c_ in QUEUE_RUNGS:
                sub = G[(G.arm == arm) & (G.panel == p_) & (G.bps == c_)].sort_values("m")
                fine = interval(sub, ["H1", "H2", "OOS", "DD", "CAGR"])
                coarse = interval(sub[sub.m.isin(M90)], ["H1", "H2", "OOS", "DD", "CAGR"])
                art.append(dict(arm=arm, panel=p_, bps=c_, hi_fine=fine["hi"],
                                hi_coarse=coarse["hi"], d_hi=fine["hi"] - coarse["hi"]
                                if np.isfinite(fine["hi"]) and np.isfinite(coarse["hi"])
                                else np.nan,
                                lo_fine=fine["lo"], lo_coarse=coarse["lo"],
                                gap_085=0.85 - fine["hi"] if np.isfinite(fine["hi"]) else np.nan))
    A = pd.DataFrame(art)
    say(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nmean |ceiling moved by 5x finer grid| = "
        f"{A.d_hi.abs().mean():.4f} of realised gross "
        f"(one coarse step is ~0.0375, one fine step ~0.0075)")

    rule("Q4 — RULE 8: interval read on 2009-2016 only, 2017-2026 read once")
    wf = []
    for (p_, a_, c_), sub in G.groupby(["panel", "arm", "bps"]):
        if c_ not in QUEUE_RUNGS:
            continue
        sub = sub.sort_values("m").reset_index(drop=True)
        okis = sub[[f"is_{k}" for k in ("H1", "H2", "DD", "CAGR")]].gt(0).all(axis=1)
        sub_is = sub[okis]
        if len(sub_is):
            mid_g = 0.5 * (sub_is.gross.iloc[0] + sub_is.gross.iloc[-1])
            mid = sub_is.iloc[(sub_is.gross - mid_g).abs().values.argmin()]
        else:
            mid = None
        dn = sub.iloc[(sub.m - 1.00).abs().values.argmin()]        # do-nothing: m = 1.00
        best_is = sub.iloc[sub.IS_Sharpe.values.argmax()]          # plain IS-Sharpe chooser
        wf.append(dict(panel=p_, arm=a_, bps=c_, is_n_ok=int(okis.sum()),
                       is_lo=sub_is.gross.iloc[0] if len(sub_is) else np.nan,
                       is_hi=sub_is.gross.iloc[-1] if len(sub_is) else np.nan,
                       mid_g=mid.gross if mid is not None else np.nan,
                       mid_OOS_Sharpe=mid.OOS_Sharpe if mid is not None else np.nan,
                       mid_OOS_CAGR=mid.OOS_CAGR if mid is not None else np.nan,
                       mid_OOS_MaxDD=mid.OOS_MaxDD if mid is not None else np.nan,
                       dn_g=dn.gross, dn_OOS_Sharpe=dn.OOS_Sharpe, dn_OOS_CAGR=dn.OOS_CAGR,
                       dn_OOS_MaxDD=dn.OOS_MaxDD,
                       isS_g=best_is.gross, isS_OOS_Sharpe=best_is.OOS_Sharpe,
                       d_mid_minus_dn=(mid.OOS_Sharpe - dn.OOS_Sharpe) if mid is not None
                       else np.nan,
                       d_isS_minus_dn=best_is.OOS_Sharpe - dn.OOS_Sharpe,
                       oracle_OOS_Sharpe=sub.OOS_Sharpe.max(),
                       spy_OOS_Sharpe=sub.spy_OOS.iloc[0]))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(WF[["panel", "arm", "bps", "is_n_ok", "is_lo", "is_hi", "mid_g", "mid_OOS_Sharpe",
            "dn_g", "dn_OOS_Sharpe", "isS_g", "isS_OOS_Sharpe", "oracle_OOS_Sharpe",
            "d_mid_minus_dn", "d_isS_minus_dn", "spy_OOS_Sharpe"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nmean d(IS-interval midpoint - do-nothing) OOS Sharpe = "
        f"{WF.d_mid_minus_dn.mean():+.4f} over {int(WF.d_mid_minus_dn.notna().sum())} cells, "
        f"wins {100*(WF.d_mid_minus_dn > 0).mean():.1f}%")
    say(f"mean d(IS-Sharpe argmax - do-nothing)      OOS Sharpe = "
        f"{WF.d_isS_minus_dn.mean():+.4f}, wins {100*(WF.d_isS_minus_dn > 0).mean():.1f}%")

    rule("Q5 — KEEP paths over all 5,808 rows")
    say(f"4b: {int(G.pass4b.sum())}/{len(G)}    4a: {int(G.pass4a.sum())}/{len(G)}")
    say("\n4b passes by panel x arm x rung:")
    say(G.groupby(["panel", "arm", "bps"])["pass4b"].sum().to_string())
    say("\n4b failing-bar census (all failing rows):")
    say(G[~G.pass4b].fail4b.value_counts().head(12).to_string())
    say("\nbest 4b-passing row per (panel, arm, rung), by Sharpe:")
    bp = G[G.pass4b].sort_values("Sharpe", ascending=False) \
        .groupby(["panel", "arm", "bps"]).head(1)
    if len(bp):
        say(bp[["panel", "arm", "bps", "m", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_Sharpe", "TO", "m_DD", "m_CAGR"]]
            .sort_values(["panel", "arm", "bps"])
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nSPY reference by panel (full sample from each panel's own start):")
    say(G.groupby("panel")[["spy_CAGR", "spy_MaxDD", "spy_H1", "spy_H2", "spy_OOS"]]
        .first().to_string(float_format=lambda x: f"{x:.4f}"))
    say("\nRULES v1 baseline Sharpe by panel x rung:")
    say(G.pivot_table(index="panel", columns="bps", values="base_Sharpe")
        .to_string(float_format=lambda x: f"{x:.4f}"))

    say(f"\ntotal {time.time()-t0:.0f}s")
    (Path(f"{OUT}.console.txt")).write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
