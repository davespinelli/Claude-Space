#!/usr/bin/env python3
"""Idea 823 (cloud, 2026-09-12) - stamp-every-committed-SMALL-PANEL-claim-with-its-PANEL-VINTAGE.

QUESTION (QUEUE idea 823, verbatim)
    Idea 609's reproduction gate found `data/prices_small.csv` grew from 483 to 715 names between
    2026-09-10 and 2026-09-12, so idea 605's SMALL439 rows (440 cols, 44 dropped) cannot be joined
    by any tolerance and no committed SMALL439 number in the record is reproducible today.  Census
    the record's small-panel claims, stamp each with the name count it was computed on, and report
    how many quote a level that a re-run would now move.

WHAT THIS FILE ADDS TO 609's GATE
    609 measured the name count.  A name count is not a reproduction error; the error is whatever
    the re-run MOVES.  This file prices it: it rebuilds BOTH vintages from git blobs, runs the
    record's six canonical small-panel books on each, and reports the level shift a reader would
    now see - then censuses the record against that measured shift instead of against the count.

    Reading the two blobs turned up a THIRD vintage leg the queue text does not name and 609 did
    not measure.  The panel did not only GROW:
      +245 names added, -13 names deleted (ALOT CVGI EVI GETY ICHR III JFB PCYO PROP RDGT SPWR
            TYGO XTNT), and
      206 of the 470 SHARED names carry RE-ADJUSTED price histories - same ticker, same dates,
            different closes (max relative move 2.0626 on WLFC, 0.9714 on HCWC; 208 names differ
            in RETURN space, HCWC by 34.0 on a single day, a reverse-split re-statement).
    So a SMALL439 level is not reproducible today for two independent reasons, and only one of
    them is a name count.  The three-panel design below separates them.

THE THREE PANELS (the vintage axis - REPORTED, NEVER SELECTED)
    V483   `git show e02949d:data/prices_small.csv.gz` (2026-09-08 blob, 483 names) - what a
           reader running the record's SMALL439 rows actually held.
    VMATCH the CURRENT blob cut to the 470 names V483 and V715 share - new prices, old-ish
           membership.  V483 -> VMATCH isolates the RE-ADJUSTMENT leg.
    V715   the current blob, 715 names.  VMATCH -> V715 isolates the MEMBERSHIP leg.
    All three are cut to the SAME trading-day index (V483's, ending 2026-09-04) so no leg is a
    calendar-length artefact, and all three take the PROTOCOL drop (max_1d_move >= 1.0).  The
    drop list comes from data/small_meta.csv where the ticker is present; for the 13 deleted
    names, absent from today's meta, max_1d_move is recomputed from V483 itself by the same rule
    (stated, not assumed).  SPY is joined from data/prices.csv as a benchmark, never a holding.

    SURVIVORSHIP: both vintages are CURRENT constituents of a sub-$2B screen as of their own
    build date, so every small-panel level here - and every level the record quotes - is biased
    upward by an unmeasured amount.  The vintage shift measured below is a shift BETWEEN two
    survivorship-biased panels; it is not a correction of that bias.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
    1. BOOK FORM (6) - the record's canonical small-panel books, all at gross 0.75, weekly, t+1:
         EWALL    every priced name, equal weight
         MA-DG    names above their 200d MA, gated weight to CASH (live RULES v2 weight handling)
         BAND-DG  RULES v2 clause 2: 200d MA +/-3% band with hysteresis, gated weight to CASH
         TOP20    baseline.score composite, top 20, equal weight  (the 2026-09-04 KEEP 4b form)
         TOP10    same, top 10
         LOWVOL20 lowest-vol20 20 names, equal weight
    2. CLAIM SET (2) - TIGHT (leaderboard rows only) / LOOSE (every committed research file).
    Cost is a PINNED three-rung sweep (0 / 10 / 25 bps), all rungs reported.  Nothing below is
    chosen on an outcome.

PRE-REGISTERED HYPOTHESES (written before any number below was read)
    H_MOVE   : every book's full-sample Sharpe moves by more than 0.05 between V483 and V715.
    H_MEMBER : the MEMBERSHIP leg (VMATCH -> V715, +245 names) is the larger of the two legs for
               a majority of books - the queue's implicit reading.
    H_FLIP   : at least one book flips a committed KEEP path (4a or 4b) between the vintages.
    H_STAMP  : a majority of the record's small-panel claim sites carry a name-count stamp
               (SMALL439 / SMALL484 style) rather than a bare SMALL tag.
    H_R8     : the rule-8 IS pick on V483 is the same book as the rule-8 IS pick on V715.

VERDICT RULE (fixed in advance): this is a REPRODUCTION file.  It is a KEEP only if some book
    clears PROTOCOL 4b on ALL THREE panels at 10 bps AND out of sample; anything else is KILL for
    capital, with the census reported either way.
"""
from __future__ import annotations
import re, subprocess, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import rebalance_mask, metrics  # noqa: E402

GROSS = 0.75
FREQ = "W"
COSTS = (0, 10, 25)
OOS_START = "2017-01-01"
OLD_REV = "e02949d"          # 2026-09-08 blob, 483 names
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
    ro = r.loc[OOS_START:]
    mo = metrics(ro)
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
def _read_blob(rev):
    raw = subprocess.run(["git", "show", f"{rev}:data/prices_small.csv.gz"],
                         cwd=ROOT, capture_output=True, check=True).stdout
    import gzip, io
    return pd.read_csv(io.BytesIO(gzip.decompress(raw)), index_col=0, parse_dates=True).sort_index()


def _protocol_drop(px, meta_bad):
    """PROTOCOL drop: max_1d_move >= 1.0.  Meta where present, recomputed where not."""
    keep, recomputed = [], 0
    for c in px.columns:
        if c in meta_bad:
            if meta_bad[c]:
                continue
            keep.append(c)
        else:
            recomputed += 1
            mv = px[c].pct_change().abs().max()
            if not (mv >= 1.0):
                keep.append(c)
    return px[keep], recomputed


def build_panels():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    meta_bad = dict(zip(meta.ticker, meta.max_1d_move >= 1.0))
    old_raw = _read_blob(OLD_REV)
    new_raw = pd.read_csv(ROOT / "data" / "prices_small.csv.gz", index_col=0, parse_dates=True).sort_index()
    shared = [c for c in old_raw.columns if c in new_raw.columns]
    P(f"  raw blobs: V483 {old_raw.shape[1]} names, V715 {new_raw.shape[1]} names, shared {len(shared)}")
    P(f"  deleted since the old blob ({len(set(old_raw.columns) - set(new_raw.columns))}): "
      f"{sorted(set(old_raw.columns) - set(new_raw.columns))}")
    P(f"  added since the old blob: {len(set(new_raw.columns) - set(old_raw.columns))}")
    idx = old_raw.index.intersection(new_raw.index)
    A = old_raw.loc[idx]
    B = new_raw.loc[idx]
    rel = ((A[shared] - B[shared]).abs() / B[shared].abs().clip(lower=1e-9)).max()
    rdiff = (A[shared].pct_change() - B[shared].pct_change()).abs().max()
    P(f"  RE-ADJUSTMENT leg: {(rel > 1e-6).sum()} of {len(shared)} shared names differ in PRICE, "
      f"{(rdiff > 1e-8).sum()} differ in RETURN; worst price {rel.max():.4f} ({rel.idxmax()}), "
      f"worst return {rdiff.max():.4f} ({rdiff.idxmax()})")
    spy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
    spy = spy.reindex(idx, method="ffill").rename("SPY")
    out = {}
    for tag, raw in (("V483", A), ("VMATCH", B[shared]), ("V715", B)):
        px, rec = _protocol_drop(raw.dropna(how="all").ffill(), meta_bad)
        P(f"  {tag}: {raw.shape[1]} -> {px.shape[1]} tradable after PROTOCOL drop "
          f"(max_1d_move >= 1.0; {rec} names not in small_meta.csv, recomputed from the blob)")
        out[tag] = pd.concat([px, spy], axis=1)
    P(f"  common index {idx[0].date()} .. {idx[-1].date()} ({len(idx)} rows) on all three panels")
    return out


# =============================================================== books
def _ew(mask, g=GROSS):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.astype(float).div(n, axis=0).fillna(0.0)


def _topn(sc, elig, n, g=GROSS):
    s = sc.where(elig)
    rank = s.rank(axis=1, ascending=False)
    m = rank <= n
    cnt = m.sum(axis=1).replace(0, np.nan)
    return g * m.astype(float).div(cnt, axis=0).fillna(0.0)


def build_books(px):
    """Six canonical small-panel books.  SPY is a benchmark column, never a holding."""
    pxn = px.drop(columns=["SPY"])
    priced = pxn.notna()
    ma = pxn > pxn.rolling(200).mean()
    npriced = priced.sum(axis=1).replace(0, np.nan)
    vol20 = pxn.pct_change().rolling(20).std() * np.sqrt(252)
    sc, _, _ = score(pxn, vol_scale=True)
    # band with hysteresis (RULES v2 clause 2)
    m200 = pxn.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=pxn.index, columns=pxn.columns)
    raw = raw.mask(pxn > m200 * 1.03, 1.0).mask(pxn < m200 * 0.97, 0.0)
    band = raw.ffill().fillna(0.0) > 0.5
    books = {
        "EWALL": _ew(priced),
        "MA-DG": (GROSS * ma.astype(float).div(npriced, axis=0)).fillna(0.0),
        "BAND-DG": (GROSS * band.astype(float).div(npriced, axis=0)).fillna(0.0),
        "TOP20": _topn(sc, priced, 20),
        "TOP10": _topn(sc, priced, 10),
        "LOWVOL20": _topn(-vol20, priced & vol20.notna(), 20),
    }
    return {k: v.reindex(columns=px.columns).fillna(0.0) for k, v in books.items()}


# =============================================================== census
TAG = re.compile(r"SMALL(\d{2,4})\b")
BARE = re.compile(r"\bSMALL\b(?!\d)|\bsmall panel\b|small=True", re.I)


def census():
    """Two claim sets.  A SITE is a committed line that makes a small-panel claim; it is STAMPED
    if it names a panel size (SMALL439-style tag), BARE if it only says SMALL/small panel."""
    sets = {
        "TIGHT": [ROOT / "research" / "LEADERBOARD.md"],
        "LOOSE": sorted(list((ROOT / "research").rglob("*.md")) + list((ROOT / "research").rglob("*.py"))),
    }
    res = {}
    for name, files in sets.items():
        stamped = bare = 0
        counts: dict[str, int] = {}
        for f in files:
            try:
                txt = f.read_text(errors="ignore")
            except Exception:
                continue
            for line in txt.split("\n"):
                tags = TAG.findall(line)
                if tags:
                    stamped += 1
                    for t in tags:
                        counts[t] = counts.get(t, 0) + 1
                elif BARE.search(line):
                    bare += 1
        res[name] = dict(stamped=stamped, bare=bare, counts=counts,
                         share=stamped / max(1, stamped + bare), files=len(files))
    return res


# =============================================================== main
def main():
    P("=" * 108)
    P("IDEA 823 - stamp-every-committed-SMALL-PANEL-claim-with-its-PANEL-VINTAGE  (cloud 2026-09-12)")
    P("=" * 108)
    P("\n[PANELS]")
    panels = build_panels()

    P("\n[G1] engine gate - fast_bt vs engine.backtest on the live baseline, V483")
    from engine import backtest as eng_bt
    pxq = panels["V483"]
    Wq = rules_v2_weights(pxq.drop(columns=["SPY"])).reindex(columns=pxq.columns).fillna(0.0)
    a = fast_bt(pxq, Wq, 10)
    b = eng_bt(pxq, Wq, cost_bps=10, freq=FREQ)["returns"]
    P(f"  max |fast_bt - engine| = {float((a - b).abs().max()):.3e}  (pass < 1e-10)")
    assert float((a - b).abs().max()) < 1e-10

    # ---------------- book x panel x cost grid, ALL points reported
    P("\n[GRID] 6 books x 3 vintages x 3 cost rungs = 54 cells, all reported")
    rows = []
    bench = {}
    for tag, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        pxn = px.drop(columns=["SPY"])
        base = rules_v2_weights(pxn).reindex(columns=px.columns).fillna(0.0)
        books = build_books(px)
        for c in COSTS:
            bench[(tag, c)] = dict(spy=spy, base=fast_bt(px, base, c).loc[start:])
        for bk, W in books.items():
            for c in COSTS:
                r = fast_bt(px, W, c).loc[start:]
                d = rowify(r)
                d.update(book=bk, panel=tag, cost=c,
                         k4a=keep_4a(r, bench[(tag, c)]["base"]),
                         f4b=fail_4b(r, bench[(tag, c)]["spy"]))
                rows.append(d)
    G = pd.DataFrame(rows)

    for c in COSTS:
        P(f"\n  --- cost {c} bps " + "-" * 88)
        P(f"  {'book':9s} {'panel':7s} {'CAGR':>7s} {'Shrp':>6s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
          f"{'oCAGR':>7s} {'oShrp':>6s} {'oMaxDD':>8s}  4a  4b-fail")
        for bk in ("EWALL", "MA-DG", "BAND-DG", "TOP20", "TOP10", "LOWVOL20"):
            for tag in ("V483", "VMATCH", "V715"):
                d = G[(G.book == bk) & (G.panel == tag) & (G.cost == c)].iloc[0]
                P(f"  {bk:9s} {tag:7s} {d.CAGR:7.2%} {d.Sharpe:6.3f} {d.MaxDD:8.2%} {d.H1:6.3f} {d.H2:6.3f} "
                  f"{d.oCAGR:7.2%} {d.oSharpe:6.3f} {d.oMaxDD:8.2%}  {'Y' if d.k4a else 'n'}  {d.f4b}")
        for who in ("base", "spy"):
            for tag in ("V483", "VMATCH", "V715"):
                r = bench[(tag, c)][who]
                d = rowify(r)
                nm = "RULESv2" if who == "base" else "SPY"
                P(f"  {nm:9s} {tag:7s} {d['CAGR']:7.2%} {d['Sharpe']:6.3f} {d['MaxDD']:8.2%} {d['H1']:6.3f} "
                  f"{d['H2']:6.3f} {d['oCAGR']:7.2%} {d['oSharpe']:6.3f} {d['oMaxDD']:8.2%}   -  -")

    # ---------------- the vintage shift, decomposed
    P("\n[SHIFT] what a re-run MOVES, by leg (10 bps).  READJ = V483->VMATCH, MEMB = VMATCH->V715")
    P(f"  {'book':9s} {'dSharpe_READJ':>14s} {'dSharpe_MEMB':>13s} {'dSharpe_TOT':>12s} "
      f"{'dCAGR_TOT_pp':>13s} {'dMaxDD_TOT_pp':>14s}  larger leg")
    shifts = []
    for bk in ("EWALL", "MA-DG", "BAND-DG", "TOP20", "TOP10", "LOWVOL20"):
        g = {t: G[(G.book == bk) & (G.panel == t) & (G.cost == 10)].iloc[0] for t in ("V483", "VMATCH", "V715")}
        dre = g["VMATCH"].Sharpe - g["V483"].Sharpe
        dme = g["V715"].Sharpe - g["VMATCH"].Sharpe
        dto = g["V715"].Sharpe - g["V483"].Sharpe
        dc = (g["V715"].CAGR - g["V483"].CAGR) * 100
        dd = (g["V715"].MaxDD - g["V483"].MaxDD) * 100
        big = "MEMB" if abs(dme) > abs(dre) else "READJ"
        shifts.append(dict(book=bk, readj=dre, memb=dme, tot=dto, dcagr=dc, dmaxdd=dd, big=big))
        P(f"  {bk:9s} {dre:14.4f} {dme:13.4f} {dto:12.4f} {dc:13.2f} {dd:14.2f}  {big}")
    S = pd.DataFrame(shifts)
    P(f"  median |dSharpe| total = {S.tot.abs().median():.4f}   max = {S.tot.abs().max():.4f}   "
      f"median |dCAGR| = {S.dcagr.abs().median():.2f} pp   median |dMaxDD| = {S.dmaxdd.abs().median():.2f} pp")
    P(f"  larger leg is MEMBERSHIP in {int((S.big == 'MEMB').sum())} of {len(S)} books")

    # ---------------- verdict flips
    P("\n[FLIPS] committed KEEP paths that change between V483 and V715")
    nflip = 0
    for c in COSTS:
        for bk in ("EWALL", "MA-DG", "BAND-DG", "TOP20", "TOP10", "LOWVOL20"):
            o = G[(G.book == bk) & (G.panel == "V483") & (G.cost == c)].iloc[0]
            n = G[(G.book == bk) & (G.panel == "V715") & (G.cost == c)].iloc[0]
            if bool(o.k4a) != bool(n.k4a) or (o.f4b == "-") != (n.f4b == "-") or o.f4b != n.f4b:
                nflip += 1
                P(f"  {c:2d} bps {bk:9s} 4a {('Y' if o.k4a else 'n')}->{('Y' if n.k4a else 'n')}   "
                  f"4b-fail {o.f4b} -> {n.f4b}")
    P(f"  {nflip} of {6 * len(COSTS)} (book, cost) cells change a reported verdict string")

    # ---------------- rule 8
    P("\n[RULE 8] walk-forward: pick the book on the FIRST HALF of each vintage, evaluate the SECOND")
    picks = {}
    for tag, px in panels.items():
        start = px.index[260]
        pxn = px.drop(columns=["SPY"])
        books = build_books(px)
        h = len(px.loc[start:]) // 2
        best, bs = None, -9e9
        for bk, W in books.items():
            r = fast_bt(px, W, 10).loc[start:]
            s = metrics(r.iloc[:h])["Sharpe"]
            if s > bs:
                best, bs = bk, s
        picks[tag] = (best, bs)
        P(f"  {tag}: IS pick = {best} (IS Sharpe {bs:.3f})")
    P(f"  same IS pick on V483 and V715: {picks['V483'][0] == picks['V715'][0]}")
    P(f"\n  OOS ({OOS_START}+) of the V483 IS pick '{picks['V483'][0]}' on every vintage, 10 bps, "
      f"vs RULES v2 and SPY:")
    P(f"  {'panel':7s} {'oCAGR':>8s} {'oShrp':>7s} {'oMaxDD':>8s} | {'base oCAGR':>10s} {'oShrp':>7s} "
      f"{'oMaxDD':>8s} | {'SPY oCAGR':>10s} {'oShrp':>7s} {'oMaxDD':>8s}")
    for tag in ("V483", "VMATCH", "V715"):
        d = G[(G.book == picks["V483"][0]) & (G.panel == tag) & (G.cost == 10)].iloc[0]
        bb = rowify(bench[(tag, 10)]["base"])
        ss = rowify(bench[(tag, 10)]["spy"])
        P(f"  {tag:7s} {d.oCAGR:8.2%} {d.oSharpe:7.3f} {d.oMaxDD:8.2%} | {bb['oCAGR']:10.2%} "
          f"{bb['oSharpe']:7.3f} {bb['oMaxDD']:8.2%} | {ss['oCAGR']:10.2%} {ss['oSharpe']:7.3f} {ss['oMaxDD']:8.2%}")

    # ---------------- census
    P("\n[CENSUS] how the record stamps its small-panel claims")
    cs = census()
    for nm, d in cs.items():
        P(f"  {nm:6s} ({d['files']} file(s)): {d['stamped']} STAMPED sites, {d['bare']} BARE sites, "
          f"stamped share {d['share']:.4f}")
        top = sorted(d["counts"].items(), key=lambda kv: -kv[1])[:8]
        P(f"         tags: " + ", ".join(f"SMALL{k} x{v}" for k, v in top))
    live = panels["V715"].shape[1] - 1
    for nm, d in cs.items():
        tot = sum(d["counts"].values())
        cur = d["counts"].get(str(live), 0)
        P(f"  {nm:6s}: {cur} of {tot} stamped sites ({cur / max(1, tot):.4f}) name TODAY's tradable "
          f"count ({live}); the other {tot - cur} name a panel that no longer exists.")
    P(f"  A stamp is not a reproduction: it makes the staleness VISIBLE but does not make the level "
      f"re-runnable.  The measured cost of that staleness is the [SHIFT] block above.")

    # ---------------- hypotheses
    P("\n[HYPOTHESES]")
    hm = bool((S.tot.abs() > 0.05).all())
    hmem = bool((S.big == "MEMB").sum() > len(S) / 2)
    hflip = nflip > 0
    hstamp = cs["LOOSE"]["share"] > 0.5
    hr8 = picks["V483"][0] == picks["V715"][0]
    for k, v, note in (("H_MOVE", hm, f"min |dSharpe| = {S.tot.abs().min():.4f}"),
                       ("H_MEMBER", hmem, f"{int((S.big == 'MEMB').sum())}/{len(S)} books"),
                       ("H_FLIP", hflip, f"{nflip} verdict-string flips"),
                       ("H_STAMP", hstamp, f"LOOSE stamped share {cs['LOOSE']['share']:.4f}"),
                       ("H_R8", hr8, f"{picks['V483'][0]} vs {picks['V715'][0]}")):
        P(f"  {k:9s} {'PASS' if v else 'FAIL'}   {note}")

    # ---------------- verdict
    P("\n[VERDICT]")
    allthree = []
    for bk in ("EWALL", "MA-DG", "BAND-DG", "TOP20", "TOP10", "LOWVOL20"):
        ok = all(G[(G.book == bk) & (G.panel == t) & (G.cost == 10)].iloc[0].f4b == "-"
                 for t in ("V483", "VMATCH", "V715"))
        if ok:
            allthree.append(bk)
    P(f"  books clearing 4b at 10 bps on ALL THREE vintages: {allthree if allthree else 'NONE'}")
    n4a = int(G[(G.cost == 10)].k4a.sum())
    P(f"  4a passes at 10 bps: {n4a} of {G[(G.cost == 10)].shape[0]} cells; "
      f"4b passes: {int((G[(G.cost == 10)].f4b == '-').sum())}")
    P("  VERDICT: " + ("KEEP-candidate" if allthree else "KILL for capital — reproduction result only"))

    out = ROOT / "research" / "backtests" / (Path(__file__).stem + ".txt")
    out.write_text("\n".join(_LOG) + "\n")
    G.to_csv(ROOT / "research" / "backtests" / (Path(__file__).stem + "_grid.csv"), index=False)
    print(f"\nwrote {out.name} and the 54-row grid CSV")


if __name__ == "__main__":
    main()
