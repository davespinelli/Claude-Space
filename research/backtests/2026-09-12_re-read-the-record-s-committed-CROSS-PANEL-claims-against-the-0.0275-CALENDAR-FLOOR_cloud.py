#!/usr/bin/env python3
"""Idea 696 (cloud, 2026-09-12) - re-read-the-record-s-committed-CROSS-PANEL-claims-against-the-
0.0275-CALENDAR-FLOOR.

QUESTION (QUEUE idea 696, verbatim)
    Idea 517 measured SPY-buy-and-hold, ONE asset held three ways, at a cross-panel Sharpe spread
    of 0.0275 (CAGR 0.0110) under the record's NATIVE convention, i.e. a pure-calendar noise floor
    that no panel content explains.  Harvest the record's committed cross-panel ordering claims and
    report how many quote a margin inside their own floor.

WHY THIS RAN HERE AFTER THREE SKIPS
    This idea was skipped by three earlier lanes as "no price leg (it scores committed rows)".
    That reading is wrong in one respect: the FLOOR is a price quantity and 517 measured only ONE
    comparand (SPY at full weight) under ONE convention.  A census against a floor is only as good
    as the floor, so this file re-measures it first - four panel-invariant comparands x two
    conventions x three cost rungs - and only then reads the record against it.  The census leg
    then runs on committed CSVs, not on prose, so every margin is machine-read rather than parsed
    out of a sentence.  Of 3,917 committed CSVs, 2,263 carry a panel-named column; requiring a
    Sharpe column too, at least two panel levels, and no more than PANELCAP levels (a column with
    more is an arm dial, not a panel axis) leaves 709 contributing files and 116,194 margins.

WHAT A "FLOOR" IS HERE
    A comparand whose HOLDINGS do not depend on panel content, run on each panel's own price file.
    Any spread in its metrics is therefore not panel content.  Two conventions, both reported:
      NATIVE  each panel keeps its own trading-day index and its own warm-up start (px.index[260]),
              which is what `baseline.compare` does and what 517 measured.
      COMMON  every panel is cut to the INTERSECTION of the three trading-day indices and to one
              shared start date.  Holdings and dates are then identical across panels, so a
              residual spread can only be the panel's own price series for the SAME ticker.
    NATIVE - COMMON is the decomposition the record has never published: how much of 517's 0.0275
    is the CALENDAR (which days exist, where the window starts) and how much is the DATA (the same
    ticker priced differently in prices.csv vs prices_broad.csv vs prices_small.csv).

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
    1. FLOOR SOURCE (4) - panel-invariant comparands, all weekly, t+1:
         SPY100   SPY at weight 1.00        (idea 517's comparand, reproduced)
         SPY075   SPY at 0.75 + cash        (the live gross)
         SPY050   SPY at 0.50 + cash
         SPYMA    SPY at 0.75 when SPY is above its OWN 200d MA, else cash - a book that
                  actually TRADES, so its floor carries turnover and is cost-sensitive.
                  (The intended fourth comparand was the tickers priced on all four panels;
                  that set is EMPTY - U56/B136/BSTK100 are large caps and SMALL663 is a sub-$2B
                  screen, so the record's four panels share NO constituent at all.  That fact is
                  reported below and is itself a limit on any cross-panel claim.)
    2. CLAIM SET (2) - TIGHT (committed CSVs carrying BOTH a `panel` column and a Sharpe column,
       arms keyed on every other column) / LOOSE (TIGHT plus CSVs whose panel column is named
       `universe` or `scope`).
    Panels (4: U56, B136, BSTK100, SMALL663) and cost rungs (0/10/25 bps) are REPORTED, NEVER
    SELECTED.  SURVIVORSHIP: B136/BSTK100 are current constituents and SMALL663 is a current
    sub-$2B screen, so every level below is upward-biased by an unmeasured amount.

PRE-REGISTERED HYPOTHESES (written before any number below was read)
    H_517    : SPY100 NATIVE reproduces idea 517's 0.0275 Sharpe spread to within 0.01.
    H_CAL    : the floor is mostly CALENDAR - the COMMON-convention spread is under half the
               NATIVE spread for every comparand.
    H_GROSS  : the floor scales with gross - SPY050's spread is below SPY100's.
    H_INSIDE : a MAJORITY of the record's committed cross-panel Sharpe margins sit inside the
               measured NATIVE floor.
    H_R8     : the floor is stable out of sample - the IS-half floor predicts the OOS-half floor
               to within a factor of 2 for every comparand.

VERDICT RULE (fixed in advance): KEEP only if some comparand clears PROTOCOL 4b at 10 bps on ALL
    FOUR panels AND out of sample.  A panel-invariant comparand is not a trading rule, so the
    expected answer is KILL for capital; the deliverable is the floor and the census.
"""
from __future__ import annotations
import glob, json, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import rebalance_mask, metrics  # noqa: E402

FREQ = "W"
COSTS = (0, 10, 25)
OOS_START = "2017-01-01"
PANELCAP = 12           # a "panel" column with more levels than this is not a panel axis
KEYCAP = 6              # at most this many object columns form an arm key (reported)
ROWCAP = 40000          # per-CSV row cap for the census (reported; files above it are counted)
_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# =============================================================== vectorised engine clone (gate G1)
def fast_bt(px, W, cost_bps=10):
    idx = px.index
    rets = px.pct_change().fillna(0.0).to_numpy(float)
    wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).to_numpy(float)
    mk = rebalance_mask(idx, FREQ).to_numpy(bool)
    mk = np.concatenate([[False], mk[:-1]]).copy()
    mk[0] = True
    T, N = rets.shape
    Cs = np.empty((T, N))
    Cs[0] = 1.0
    np.cumprod(1.0 + rets[:-1], axis=0, out=Cs[1:])
    starts = np.flatnonzero(mk)
    seg = np.searchsorted(starts, np.arange(T), side="right") - 1
    s_of_t = starts[seg]
    new = wt[s_of_t]
    num = new * (Cs / Cs[s_of_t])
    D = num.sum(axis=1) + (1.0 - new.sum(axis=1))
    held = num / D[:, None]
    turn = np.zeros(T)
    turn[0] = np.abs(wt[0]).sum()
    later = starts[1:]
    if len(later):
        sp = starts[seg[later] - 1]
        prev_new = wt[sp]
        np_ = prev_new * (Cs[later] / Cs[sp])
        Dp = np_.sum(axis=1) + (1.0 - prev_new.sum(axis=1))
        turn[later] = np.abs(wt[later] - np_ / Dp[:, None]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r):
    m = metrics(r)
    h1, h2 = halves(r)
    mo = metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    if not (len(ro) > 60 and metrics(ro)["Sharpe"] > metrics(so)["Sharpe"]):
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# =============================================================== panels
def build_panels():
    g = json.loads((ROOT / "research" / "universe.json").read_text())
    etf36 = set(g["broad"] + g["sectors"] + g["bonds_fx_commod"])
    px56 = load_universe()
    px136 = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    pxs = load_universe(small=True)
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep]
    bstk = [t for t in px136.columns if t not in etf36 and t != "SPY"]
    px_bstk = px136[bstk + ["SPY"]]
    panels = {"U56": px56, "B136": px136, "BSTK100": px_bstk, "SMALL663": pxs}
    for k, v in panels.items():
        P(f"  {k:9s} {v.shape[1] - 1:4d} names + SPY, {len(v.index):5d} rows, "
          f"{v.index[0].date()} .. {v.index[-1].date()}")
    P(f"  SMALL663 drops {len(bad)} tickers with max_1d_move >= 1.0 per PROTOCOL; survivorship "
      f"caveat in the docstring applies to B136 / BSTK100 / SMALL663 alike.")
    return panels


def core_tickers(panels):
    s = None
    for v in panels.values():
        c = set(v.columns) - {"SPY"}
        s = c if s is None else (s & c)
    return sorted(s)


# =============================================================== comparands
def comparand(px, kind, core):
    """Panel-INVARIANT holdings, expressed in each panel's own column space."""
    W = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    if kind == "SPYMA":
        spy = px["SPY"]
        W["SPY"] = 0.75 * (spy > spy.rolling(200).mean()).astype(float)
        return W
    if kind.startswith("SPY"):
        W["SPY"] = float(kind[3:]) / 100.0
        return W
    raise ValueError(kind)


# =============================================================== census
def census(floor_native):
    """Machine-read every committed CSV with a panel column: group rows into ARMS (all columns
    except the panel column and the metric columns) and emit every cross-panel Sharpe margin."""
    PANEL_COLS = {"panel": "TIGHT", "universe": "LOOSE", "scope": "LOOSE"}
    files = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv")))
    out = {"TIGHT": [], "LOOSE": []}
    nf = {"TIGHT": 0, "LOOSE": 0}
    capped = 0
    wide = 0
    nseen = [0]
    for f in files:
        try:
            head = pd.read_csv(f, nrows=1)
        except Exception:
            continue
        low = {c.lower(): c for c in head.columns}
        pcol = next((low[k] for k in PANEL_COLS if k in low), None)
        scol = next((low[k] for k in ("sharpe", "sh", "shrp") if k in low), None)
        if pcol is None or scol is None:
            continue
        tier = PANEL_COLS[pcol.lower()]
        try:
            d = pd.read_csv(f, nrows=ROWCAP)
        except Exception:
            continue
        if len(d) == ROWCAP:
            capped += 1
        d = d[pd.to_numeric(d[scol], errors="coerce").notna()]
        if d.empty or d[pcol].nunique() < 2:
            continue
        if d[pcol].nunique() > PANELCAP:      # a column with > PANELCAP levels is not a panel axis
            wide += 1
            continue
        d[scol] = pd.to_numeric(d[scol], errors="coerce")
        keycols = [c for c in d.columns if c != pcol and d[c].dtype == object][:KEYCAP]
        if not keycols:
            keycols = [c for c in d.columns if c not in (pcol, scol)][:3]
        if not keycols:
            continue
        nseen[0] += 1
        if nseen[0] % 250 == 0:
            P(f"    ... {nseen[0]} panel-bearing files read")
        # arm key = a 64-bit hash of the non-panel object columns, so the groupby is integer-keyed
        akey = pd.util.hash_pandas_object(d[keycols].astype(str), index=False).to_numpy()
        tmp = pd.DataFrame({"a": akey, "p": d[pcol].astype(str).to_numpy(),
                            "s": d[scol].to_numpy(float)})
        piv = tmp.groupby(["a", "p"], sort=False)["s"].mean().unstack("p")
        pans = list(piv.columns)
        for i in range(len(pans)):
            for j in range(i + 1, len(pans)):
                m = (piv[pans[i]] - piv[pans[j]]).dropna()
                if len(m):
                    out[tier].append(m.abs().to_numpy())
        nf[tier] += 1
    tight = np.concatenate(out["TIGHT"]) if out["TIGHT"] else np.array([])
    loose = np.concatenate(out["TIGHT"] + out["LOOSE"]) if (out["TIGHT"] or out["LOOSE"]) else np.array([])
    return dict(TIGHT=tight, LOOSE=loose, nfiles=nf, capped=capped, wide=wide, nseen=nseen[0])


# =============================================================== main
def main():
    P("=" * 110)
    P("IDEA 696 - re-read-the-record-s-committed-CROSS-PANEL-claims-against-the-0.0275-CALENDAR-FLOOR")
    P("  (cloud 2026-09-12)")
    P("=" * 110)

    P("\n[PANELS]")
    panels = build_panels()
    core = core_tickers(panels)
    P(f"  tickers priced on ALL FOUR panels: {len(core)} {core} — the four panels are "
      f"CONSTITUENT-DISJOINT across the large/small split, so no multi-name comparand can be held "
      f"identically on all four; SPYMA (a trading book in SPY alone) is used as the fourth floor "
      f"source instead.")

    P("\n[G1] engine gate - fast_bt vs engine.backtest on the live baseline, U56")
    from engine import backtest as eng_bt
    pxq = panels["U56"]
    Wq = rules_v2_weights(pxq.drop(columns=["SPY"])).reindex(columns=pxq.columns).fillna(0.0)
    a = fast_bt(pxq, Wq, 10)
    b = eng_bt(pxq, Wq, cost_bps=10, freq=FREQ)["returns"]
    P(f"  max |fast_bt - engine| = {float((a - b).abs().max()):.3e}  (pass < 1e-10)")
    assert float((a - b).abs().max()) < 1e-10

    # ------------- the two conventions
    common_idx = None
    for v in panels.values():
        common_idx = v.index if common_idx is None else common_idx.intersection(v.index)
    P(f"\n[CONVENTIONS] NATIVE = each panel's own index and own px.index[260] warm-up start")
    P(f"              COMMON = the {len(common_idx)}-day intersection index, one shared start "
      f"{common_idx[260].date()}")

    kinds = ["SPY100", "SPY075", "SPY050", "SPYMA"]
    rows = []
    for conv in ("NATIVE", "COMMON"):
        for pname, px in panels.items():
            pxc = px if conv == "NATIVE" else px.loc[common_idx]
            start = pxc.index[260]
            spy = pxc["SPY"].pct_change().fillna(0.0).loc[start:]
            base = rules_v2_weights(pxc.drop(columns=["SPY"])).reindex(columns=pxc.columns).fillna(0.0)
            for c in COSTS:
                rb = fast_bt(pxc, base, c).loc[start:]
                for k in kinds:
                    W = comparand(pxc, k, core)
                    r = fast_bt(pxc, W, c).loc[start:]
                    d = rowify(r)
                    d.update(conv=conv, panel=pname, kind=k, cost=c,
                             k4a=keep_4a(r, rb), f4b=fail_4b(r, spy))
                    rows.append(d)
    F = pd.DataFrame(rows)

    P("\n[GRID] 4 comparands x 4 panels x 2 conventions x 3 cost rungs = 96 cells, all reported")
    for conv in ("NATIVE", "COMMON"):
        for c in COSTS:
            P(f"\n  --- {conv}, {c} bps " + "-" * 76)
            P(f"  {'comparand':9s} {'panel':9s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} "
              f"{'H2':>6s} {'oSharpe':>8s}  4a  4b-fail")
            for k in kinds:
                for pname in panels:
                    d = F[(F.conv == conv) & (F.cost == c) & (F.kind == k) & (F.panel == pname)].iloc[0]
                    P(f"  {k:9s} {pname:9s} {d.CAGR:7.2%} {d.Sharpe:7.4f} {d.MaxDD:8.2%} {d.H1:6.3f} "
                      f"{d.H2:6.3f} {d.oSharpe:8.4f}  {'Y' if d.k4a else 'n'}  {d.f4b}")

    # ------------- the floor
    P("\n[FLOOR] cross-panel SPREAD (max - min over the 4 panels) of a PANEL-INVARIANT comparand")
    P(f"  {'comparand':9s} {'cost':>4s} {'NAT dSharpe':>12s} {'COM dSharpe':>12s} {'NAT dCAGR_pp':>13s} "
      f"{'COM dCAGR_pp':>13s} {'NAT dMaxDD_pp':>14s}  COM/NAT")
    fl = []
    for k in kinds:
        for c in COSTS:
            n = F[(F.conv == "NATIVE") & (F.cost == c) & (F.kind == k)]
            m = F[(F.conv == "COMMON") & (F.cost == c) & (F.kind == k)]
            sn, sm = n.Sharpe.max() - n.Sharpe.min(), m.Sharpe.max() - m.Sharpe.min()
            cn, cm = (n.CAGR.max() - n.CAGR.min()) * 100, (m.CAGR.max() - m.CAGR.min()) * 100
            dn = (n.MaxDD.max() - n.MaxDD.min()) * 100
            fl.append(dict(kind=k, cost=c, nat=sn, com=sm, cn=cn, cm=cm, dn=dn))
            P(f"  {k:9s} {c:4d} {sn:12.4f} {sm:12.4f} {cn:13.4f} {cm:13.4f} {dn:14.4f}  "
              f"{(sm / sn if sn else float('nan')):.3f}")
    FL = pd.DataFrame(fl)
    nat10 = FL[(FL.cost == 10)].nat
    P(f"\n  517's comparand and convention: SPY100 NATIVE 0 bps dSharpe = "
      f"{float(FL[(FL.kind == 'SPY100') & (FL.cost == 0)].nat.iloc[0]):.4f}, "
      f"dCAGR = {float(FL[(FL.kind == 'SPY100') & (FL.cost == 0)].cn.iloc[0]):.4f} pp "
      f"(published: 0.0275 Sharpe, 0.0110 = 1.10 pp CAGR)")
    FLOOR = float(nat10.max())
    P(f"  FLOOR used for the census = max NATIVE dSharpe over the 4 comparands at 10 bps = {FLOOR:.4f}")
    P(f"  (a conservative floor: the census counts a margin as INSIDE only if it is below the "
      f"LARGEST panel-invariant spread)")

    # ------------- rule 8 on the floor
    P("\n[RULE 8] is the floor itself stable? measured on the IS half, read once on the OOS half")
    P(f"  {'comparand':9s} {'IS dSharpe':>11s} {'OOS dSharpe':>12s} {'ratio':>7s}")
    r8 = []
    for k in kinds:
        isv, oov = [], []
        for pname, px in panels.items():
            start = px.index[260]
            r = fast_bt(px, comparand(px, k, core), 10).loc[start:]
            h = len(r) // 2
            isv.append(metrics(r.iloc[:h])["Sharpe"])
            oov.append(metrics(r.iloc[h:])["Sharpe"])
        a, b = max(isv) - min(isv), max(oov) - min(oov)
        r8.append(dict(kind=k, is_=a, oos=b, ratio=(b / a if a else np.nan)))
        P(f"  {k:9s} {a:11.4f} {b:12.4f} {(b / a if a else float('nan')):7.3f}")
    R8 = pd.DataFrame(r8)

    # ------------- census
    P("\n[CENSUS] every committed cross-panel Sharpe margin in the record's machine-readable CSVs")
    cs = census(FLOOR)
    for tier in ("TIGHT", "LOOSE"):
        m = cs[tier]
        if not len(m):
            P(f"  {tier}: no margins found")
            continue
        inside = float((m < FLOOR).mean())
        P(f"  {tier}: {len(m):,} cross-panel margins from {cs['nfiles']['TIGHT'] if tier == 'TIGHT' else sum(cs['nfiles'].values())} "
          f"file(s); median |dSharpe| {np.median(m):.4f}, mean {m.mean():.4f}, "
          f"p25 {np.percentile(m, 25):.4f}, p75 {np.percentile(m, 75):.4f}, max {m.max():.4f}")
        P(f"          INSIDE the {FLOOR:.4f} floor: {int((m < FLOOR).sum()):,} ({inside:.4f}); "
          f"inside 0.0275 (517's published number): {float((m < 0.0275).mean()):.4f}")
    P(f"  ({cs['capped']} file(s) hit the {ROWCAP:,}-row cap and were read to it; {cs['wide']} file(s) "
      f"were skipped because their panel-named column carries more than {PANELCAP} levels, i.e. it "
      f"is not a panel axis; {cs['nseen']} file(s) contributed margins.)")

    # ------------- hypotheses
    P("\n[HYPOTHESES]")
    spy100_0 = float(FL[(FL.kind == "SPY100") & (FL.cost == 0)].nat.iloc[0])
    h517 = abs(spy100_0 - 0.0275) < 0.01
    hcal = bool((FL[FL.cost == 10].com < 0.5 * FL[FL.cost == 10].nat).all())
    hgross = bool(FL[(FL.kind == "SPY050") & (FL.cost == 10)].nat.iloc[0]
                  < FL[(FL.kind == "SPY100") & (FL.cost == 10)].nat.iloc[0])
    hin = bool(len(cs["TIGHT"]) and (cs["TIGHT"] < FLOOR).mean() > 0.5)
    hr8 = bool((R8.ratio.between(0.5, 2.0)).all())
    for k, v, note in (("H_517", h517, f"SPY100 NATIVE 0 bps = {spy100_0:.4f} vs published 0.0275"),
                       ("H_CAL", hcal, f"COMMON/NATIVE ratios at 10 bps: "
                                       f"{[round(x, 3) for x in (FL[FL.cost == 10].com / FL[FL.cost == 10].nat)]}"),
                       ("H_GROSS", hgross, f"SPY050 {FL[(FL.kind == 'SPY050') & (FL.cost == 10)].nat.iloc[0]:.4f} "
                                           f"vs SPY100 {FL[(FL.kind == 'SPY100') & (FL.cost == 10)].nat.iloc[0]:.4f}"),
                       ("H_INSIDE", hin, f"TIGHT inside share "
                                         f"{(cs['TIGHT'] < FLOOR).mean() if len(cs['TIGHT']) else float('nan'):.4f}"),
                       ("H_R8", hr8, f"ratios {[round(x, 3) for x in R8.ratio]}")):
        P(f"  {k:9s} {'PASS' if v else 'FAIL'}   {note}")

    # ------------- verdict
    P("\n[VERDICT]")
    ok = [k for k in kinds
          if all(F[(F.conv == "NATIVE") & (F.cost == 10) & (F.kind == k) & (F.panel == p)].iloc[0].f4b == "-"
                 for p in panels)]
    n4a = int(F[(F.conv == "NATIVE") & (F.cost == 10)].k4a.sum())
    n4b = int((F[(F.conv == "NATIVE") & (F.cost == 10)].f4b == "-").sum())
    P(f"  comparands clearing 4b at 10 bps on ALL FOUR panels: {ok if ok else 'NONE'}")
    P(f"  NATIVE 10 bps: 4a {n4a} of {F[(F.conv == 'NATIVE') & (F.cost == 10)].shape[0]}, 4b {n4b}")
    P("  VERDICT: " + ("KEEP-candidate" if ok else
                       "KILL for capital — a panel-invariant comparand is a measuring stick, not a rule"))

    out = ROOT / "research" / "backtests" / (Path(__file__).stem + ".txt")
    out.write_text("\n".join(_LOG) + "\n")
    F.to_csv(ROOT / "research" / "backtests" / (Path(__file__).stem + "_grid.csv"), index=False)
    print(f"\nwrote {out.name} and the 96-row grid CSV")


if __name__ == "__main__":
    main()
