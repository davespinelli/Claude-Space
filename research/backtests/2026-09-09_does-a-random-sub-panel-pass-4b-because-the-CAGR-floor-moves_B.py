#!/usr/bin/env python3
"""Idea 253 (lane B, 2026-09-09): does a random sub-panel pass 4b because the CAGR floor moves?

Idea 78 found, and idea 83 reproduced, that random k=80 sub-panels of B136 clear PROTOCOL 4b
at a ~46% base rate.  Idea 83's own 450-book census put the failing bars at
H2 233 / DD 203 / CAGR 194 / OOS 176 / H1 121, 87 passes.  A 46% base rate means the bar
admits noise on that panel at that k.  This run does two things:

  PART A (the null)   Measure, per panel and per sub-panel size k, the random sub-panel 4b
                      base rate AND the sampling distribution of each of the five 4b bars'
                      SLACK.  That gives every bar a panel-specific noise unit sd_null.
  PART B (the census) Back-fill, for EVERY 4b pass in the committed record that can be
                      mechanically recovered, the five raw slacks (idea 306's `bars_4b`
                      convention), which bar was CLOSEST to binding, by how much in raw
                      units, and by how much in PART A's noise units (z = slack / sd_null).
                      Then ask how many published passes sit INSIDE their own panel's
                      random-sub-panel base rate, i.e. have a min-z no better than the
                      typical random draw that happened to clear.

TUNED PARAMETERS (max 2, per PROTOCOL rule 4): k (sub-panel size) and book (EWall | CAND20).
ALL grid points are printed and written to the .null.csv artefact.

RULE 8 (walk-forward): the (k, book) cell is chosen on IS 2009-2016 pass rate ONLY and the
chosen cell's OOS 2017-2026 pass rate and per-draw OOS CAGR/Sharpe/MaxDD are read once,
untouched, against the live RULES v2 baseline and SPY.  Both KEEP paths evaluated.

Costs 10 bps, weekly cadence, next-day execution (PROTOCOL rules 1-2).
SURVIVORSHIP: broad136 and the small panel are CURRENT constituents (PROTOCOL rule 9).
Deterministic: every draw seeded off (panel, k, draw).
Writes:  .null.csv  .census.csv  .binding.csv  .walkforward.csv  .console.txt
"""
import sys, re, glob, json, hashlib, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score          # noqa: E402
from engine import backtest, metrics, rebalance_mask                            # noqa: E402

HERE = Path(__file__).resolve()
STEM = HERE.with_suffix("")
COST_BPS, FREQ = 10.0, "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
N_DRAWS = 150
K_GRID = {"U56": [14, 28, 42], "B136": [20, 40, 80], "SMALL": [60, 120, 240]}
BOOKS = ["EWall", "CAND20"]
BARS = ["H1", "H2", "OOS", "DD", "CAGR"]

_LOG = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ---------------------------------------------------------------- engine twins
def fast_backtest(px, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost (idea 325's helper, gated below)."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        T = u.sum(axis=1) + (1.0 - w.sum())
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def net(r0, turn, cost_bps=COST_BPS):
    return r0 - turn * cost_bps / 1e4


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy, oos_start=OOS_START):
    """PROTOCOL 4b slacks, idea 306's `bars_4b` sign convention: positive = passing.
    Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[oos_start:])["Sharpe"] - metrics(spy.loc[oos_start:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4b_from_cells(CAGR, Sharpe_h1, Sharpe_h2, MaxDD, OOS_Sharpe, ref):
    """Same five slacks from PUBLISHED cell metrics + a panel SPY reference dict."""
    return {"H1": Sharpe_h1 - ref["H1"], "H2": Sharpe_h2 - ref["H2"],
            "OOS": OOS_Sharpe - ref["OOS_Sharpe"],
            "DD": 0.60 * abs(ref["MaxDD"]) - abs(MaxDD),
            "CAGR": CAGR - 0.70 * ref["CAGR"]}


def bars_4a(r, base):
    d = {"H1": hs(r)[0] - hs(base)[0], "H2": hs(r)[1] - hs(base)[1],
         "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    return (not [k for k, v in d.items() if v < 0]), d


# ---------------------------------------------------------------- books
# Idea 78/83's two sub-panel books, reproduced VERBATIM so this null is the published null:
# gated (200d MA + vol<60%) at gross 0.75, gate-out weight to cash (never re-spread).
GROSS, MAX_VOL, CAND_N = 0.75, 0.60, 20


def _elig(sub):
    _, above, vol20 = score(sub)
    return above & (vol20 < MAX_VOL)


def ew_weights(sub, gross=GROSS):
    """EWall: equal weight over the ELIGIBLE names of the sub-panel (idea 83 weights_ewall)."""
    e = _elig(sub)
    cnt = e.sum(axis=1).replace(0, np.nan)
    return e.astype(float).div(cnt, axis=0).mul(gross).fillna(0.0)


def cand_weights(sub, n=CAND_N, gross=GROSS):
    """CAND-n: top-n of the sub-panel by the unscaled composite (idea 83 weights_cand)."""
    e = _elig(sub)
    s = score(sub, vol_scale=False)[0]
    rank = s.where(e).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def draw_book(px, key, k, d, book):
    """Deterministic random sub-panel of size k, its book, and its NET 10 bps return series."""
    names = [c for c in px.columns if c != "SPY"]
    cols = list(rng_for(key, k, d).choice(names, size=k, replace=False))
    sub = px[cols].dropna(how="all").ffill()
    w = ew_weights(sub) if book == "EWall" else cand_weights(sub)
    r0, tu = fast_backtest(sub, w)
    return ev(net(r0, tu), key), ev(tu, key), cols


# ---------------------------------------------------------------- panels
START = {}          # panel -> first evaluated day (px.index[260], baseline.compare's warm-up)


def panels():
    """FULL panels (the backtest runs on all of them; the first 260 days are warm-up and are
    dropped from every metric, exactly as baseline.compare does)."""
    out = {}
    for key, kw in [("U56", {}), ("B136", {"broad": True}), ("SMALL", {"small": True})]:
        px = load_universe(**kw).dropna(how="all").ffill()
        START[key] = px.index[260]
        out[key] = px
    return out


def ev(r, key):
    """Drop the warm-up. engine.backtest emits NaN on day 0 and the first rebalance day
    (its shift(1) target row); both sit inside the warm-up and are dropped here."""
    return r.loc[START[key]:]


def spy_ref(px, key):
    spy = ev(px["SPY"].pct_change().fillna(0.0), key)
    m = metrics(spy); h1, h2 = hs(spy)
    return {"CAGR": m["CAGR"], "Sharpe": m["Sharpe"], "MaxDD": m["MaxDD"], "H1": h1, "H2": h2,
            "OOS_Sharpe": metrics(spy.loc[OOS_START:])["Sharpe"],
            "OOS_CAGR": metrics(spy.loc[OOS_START:])["CAGR"],
            "OOS_MaxDD": metrics(spy.loc[OOS_START:])["MaxDD"],
            "IS_Sharpe": metrics(spy.loc[:IS_END])["Sharpe"]}, spy


def rng_for(panel, k, d):
    h = hashlib.sha256(f"{panel}|{k}|{d}".encode()).hexdigest()[:8]
    return np.random.default_rng(int(h, 16))


# ================================================================= GATES
def gates(PX):
    P("=" * 100)
    P("GATE 0 - engine twin, published anchors, and the 4b bar definition")
    P("=" * 100)
    px = PX["U56"]
    sub = px[[c for c in px.columns if c != "SPY"][:20]].dropna(how="all").ffill()
    w = ew_weights(sub)
    r0, t0 = fast_backtest(sub, w)
    live = backtest(sub, w, cost_bps=COST_BPS, freq=FREQ)
    a, b = ev(net(r0, t0), "U56"), ev(live["returns"], "U56")
    dr = float(np.abs(a.values - b.values).max())
    dt = float(np.abs(ev(t0, "U56").values - ev(live["turnover"], "U56").values).max())
    P(f"  fast_backtest vs engine.backtest: max |dret| {dr:.3e}   max |dturnover| {dt:.3e}")
    assert dr < 1e-12 and dt < 1e-12, "engine twin disagrees"

    for key in ("U56", "B136", "SMALL"):
        ref, _ = spy_ref(PX[key], key)
        P(f"  {key:6s} n={PX[key].shape[1]-1:4d} {START[key].date()}..{PX[key].index[-1].date()}  "
          f"SPY {ref['CAGR']:.2%} / {ref['Sharpe']:.3f} / {ref['MaxDD']:.2%}  "
          f"halves {ref['H1']:.3f}/{ref['H2']:.3f}  OOS {ref['OOS_Sharpe']:.3f}  "
          f"4b bars: CAGR floor {0.70*ref['CAGR']:.2%}, DD cap {0.60*abs(ref['MaxDD']):.2%}")

    # digit-exact anchor: idea 83's published B136 SPY line (its console.txt line 11)
    rb, _ = spy_ref(PX["B136"], "B136")
    got = (f"{rb['CAGR']:.2%}", f"{rb['Sharpe']:.3f}", f"{rb['MaxDD']:.2%}",
           f"{rb['H1']:.3f}", f"{rb['H2']:.3f}", f"{rb['OOS_Sharpe']:.3f}")
    want = ("15.23%", "0.889", "-33.72%", "0.957", "0.834", "0.882")
    P(f"  ANCHOR idea 83 console line 11 (B136 SPY): want {want} got {got} -> "
      f"{'MATCH' if got == want else 'MISMATCH'}")
    assert got == want, "idea 83's published SPY reference does not reproduce"
    P("  books are idea 83's own weights_ewall / weights_cand (gross 0.75, 200d+vol gate),")
    P("  so PART A's base rates are directly comparable to idea 78/83's published ~46%.")
    return True


# ================================================================= PART A
def part_a(PX):
    P("")
    P("=" * 100)
    P("PART A - the null: random sub-panel 4b base rate and per-bar slack noise, ALL grid points")
    P("=" * 100)
    parts = []
    for key, px in PX.items():
        parts.append(part_a_panel(PX, key))
    NULL = pd.concat(parts, ignore_index=True)
    NULL.to_csv(str(STEM) + ".null.csv", index=False)
    P(f"  -> wrote {Path(str(STEM)+'.null.csv').name}  ({len(NULL)} draws)")
    return NULL


def part_a_panel(PX, key):
    """One panel's null. Cached per panel (the draws are seeded, so the cache is exact);
    the sandbox freezes between calls, so each panel is runnable on its own:
        python <this script> --panel SMALL"""
    cache = Path(f"{STEM}.nullA_{key}.csv")
    want = len(K_GRID[key]) * len(BOOKS) * N_DRAWS
    if cache.exists():
        D0 = pd.read_csv(cache)
        if len(D0) == want:
            P(f"  (re-using deterministic cache {cache.name}: {len(D0)} draws)")
            _part_a_summary(D0)
            return D0
    rows = []
    if True:
        px = PX[key]
        ref, spy = spy_ref(px, key)
        names = [c for c in px.columns if c != "SPY"]
        for k in K_GRID[key]:
            for book in BOOKS:
                t0 = time.time()
                recs = []
                for d in range(N_DRAWS):
                    r, tu, cols = draw_book(px, key, k, d, book)
                    ok, sl, _ = bars_4b(r, spy)
                    m = metrics(r); mo = metrics(r.loc[OOS_START:])
                    # IS/OOS window 4b, evaluated inside each window on its own halves
                    rI, sI = r.loc[:IS_END], spy.loc[:IS_END]
                    rO, sO = r.loc[OOS_START:], spy.loc[OOS_START:]
                    okIS = _win4b(rI, sI); okOOS = _win4b(rO, sO)
                    rec = dict(panel=key, k=k, book=book, draw=d, pass4b=bool(ok),
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                               H1=hs(r)[0], H2=hs(r)[1], OOS_Sharpe=mo["Sharpe"],
                               OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                               IS_Sharpe=metrics(rI)["Sharpe"], IS_pass4b=okIS, OOS_pass4b=okOOS,
                               turnover=float(tu.sum() / (len(r) / 252)))
                    rec.update({f"slack_{b}": sl[b] for b in BARS})
                    recs.append(rec)
                D = pd.DataFrame(recs)
                rows.append(D)
                rate = D.pass4b.mean()
                P(f"  {key:6s} k={k:4d} {book:7s} 4b base rate {rate:6.1%}  "
                  f"(IS-window {D.IS_pass4b.mean():5.1%}, OOS-window {D.OOS_pass4b.mean():5.1%})  "
                  f"[{time.time()-t0:.0f}s]")
                P("           bar slack mean/sd: " + "  ".join(
                    f"{b} {D['slack_'+b].mean():+.4f}/{D['slack_'+b].std():.4f}" for b in BARS))
                fails = D.loc[~D.pass4b, [f"slack_{b}" for b in BARS]]
                cnt = {b: int((D[f"slack_{b}"] < 0).sum()) for b in BARS}
                P(f"           failing-bar census (of {len(D)}): " +
                  ", ".join(f"{b} {cnt[b]}" for b in BARS) + f", pass {int(D.pass4b.sum())}")
    D0 = pd.concat(rows, ignore_index=True)
    D0.to_csv(cache, index=False)
    P(f"  -> wrote {cache.name}  ({len(D0)} draws)")
    return D0


def _part_a_summary(NULL):
    for (key, k, book), D in NULL.groupby(["panel", "k", "book"], sort=False):
        P(f"  {key:6s} k={k:4d} {book:7s} 4b base rate {D.pass4b.mean():6.1%}  "
          f"(IS-window {D.IS_pass4b.mean():5.1%}, OOS-window {D.OOS_pass4b.mean():5.1%})")
        P("           bar slack mean/sd: " + "  ".join(
            f"{b} {D['slack_'+b].mean():+.4f}/{D['slack_'+b].std():.4f}" for b in BARS))
        P(f"           failing-bar census (of {len(D)}): " +
          ", ".join(f"{b} {int((D['slack_'+b] < 0).sum())}" for b in BARS) +
          f", pass {int(D.pass4b.sum())}")


def _win4b(r, spy):
    """4b inside one window: Sharpe > SPY in both halves of the window, DD <= 60%, CAGR >= 70%.
    (No separate OOS leg — the window IS the evaluation.)"""
    if len(r) < 60: return False
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    return bool(h1 > s1 and h2 > s2 and abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])
                and m["CAGR"] >= 0.70 * ms["CAGR"])


# ================================================================= PART B
PANEL_MAP = [
    (re.compile(r"^(u56|universe\.json\(56\)|U56)$", re.I), "U56"),
    (re.compile(r"^(b136|broad136|broad|BROAD136|universe_broad\(136\))$", re.I), "B136"),
    (re.compile(r"^(small\d*|SMALL|small|SMALL439\+SPY)$", re.I), "SMALL"),
]
NEED = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]
FLAGCOLS = ["pass4b", "keep4b", "f4b", "fail4b", "p4b"]


def map_panel(v):
    v = str(v).strip()
    for rx, key in PANEL_MAP:
        if rx.match(v): return key
    return None


def published_pass(d, col):
    if col in ("pass4b", "keep4b"):
        return d[col].astype(str).str.strip().str.lower().isin(["true", "1", "1.0", "yes"])
    if col == "p4b":
        return pd.to_numeric(d[col], errors="coerce") > 0
    return d[col].isna() | d[col].astype(str).str.strip().isin(["-", "", "nan", "none"])


def part_b(PX, NULL):
    P("")
    P("=" * 100)
    P("PART B - the census: every mechanically recoverable 4b PASS in the committed record")
    P("=" * 100)
    REF = {k: spy_ref(px, k)[0] for k, px in PX.items()}
    SD = (NULL.groupby("panel")[[f"slack_{b}" for b in BARS]].std()
          .rename(columns={f"slack_{b}": b for b in BARS}))
    P("  noise units sd_null(bar | panel), pooled over ALL k and both books (PART A):")
    P(SD.to_string(float_format=lambda x: f"{x:.4f}"))

    files = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv")))
    seen = {"files": 0, "cand": 0, "used": 0, "rows": 0, "pass": 0, "nopanel": 0,
            "unmapped": 0, "repro": 0, "norepro": 0}
    out = []
    for f in files:
        if Path(f).name.startswith(HERE.stem): continue
        seen["files"] += 1
        try:
            hdr = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception:
            continue
        if not any("4b" in c.lower() for c in hdr): continue
        seen["cand"] += 1
        if not all(c in hdr for c in NEED): continue
        fc = next((c for c in FLAGCOLS if c in hdr), None)
        if fc is None: continue
        pcol = "panel" if "panel" in hdr else ("universe" if "universe" in hdr else None)
        if pcol is None:
            seen["nopanel"] += 1; continue
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        seen["used"] += 1; seen["rows"] += len(d)
        d["_pass"] = published_pass(d, fc)
        d = d.loc[d["_pass"]].copy()
        if d.empty: continue
        seen["pass"] += len(d)
        d["_panel"] = d[pcol].map(map_panel)
        seen["unmapped"] += int(d["_panel"].isna().sum())
        d = d.loc[d["_panel"].notna()].copy()
        if d.empty: continue
        for c in NEED:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d = d.dropna(subset=NEED)
        if d.empty: continue
        for key, g in d.groupby("_panel"):
            ref = REF[key]
            sl = bars_4b_from_cells(g["CAGR"], g["H1"], g["H2"], g["MaxDD"], g["OOS_Sharpe"], ref)
            M = pd.DataFrame({f"m_{b}": sl[b] for b in BARS}, index=g.index)
            M["repro"] = (M[[f"m_{b}" for b in BARS]] >= 0).all(axis=1)
            for b in BARS:
                M[f"z_{b}"] = M[f"m_{b}"] / SD.loc[key, b]
            zc = [f"z_{b}" for b in BARS]
            M["binding"] = M[zc].idxmin(axis=1).str[2:]
            M["min_z"] = M[zc].min(axis=1)
            M["binding_raw"] = M[[f"m_{b}" for b in BARS]].idxmin(axis=1).str[2:]
            M["file"] = Path(f).name; M["panel"] = key
            for extra in ("book", "arm", "n", "gross", "cost", "family", "dial", "kind"):
                M[extra] = g[extra].astype(str) if extra in g.columns else ""
            out.append(M)
    C = pd.concat(out, ignore_index=True) if out else pd.DataFrame()
    seen["repro"] = int(C["repro"].sum()); seen["norepro"] = int((~C["repro"]).sum())
    P("")
    P(f"  corpus: {seen['files']} committed CSVs, {seen['cand']} carry a 4b column, "
      f"{seen['used']} carry a 4b column + panel + all of {NEED}")
    P(f"  rows in those files {seen['rows']:,}; published 4b PASS rows {seen['pass']:,}; "
      f"panel unmappable {seen['unmapped']:,}; recovered with metrics {len(C):,}")
    P(f"  REPRODUCTION GATE (my panel SPY reference must re-derive the published pass): "
      f"{seen['repro']:,} reproduce ({seen['repro']/max(len(C),1):.1%}), {seen['norepro']:,} do not.")
    P("     rows that do NOT reproduce are EXCLUDED from every margin statistic below —")
    P("     they used a different window, cost rung or SPY comparand than this panel default.")
    if seen["norepro"]:
        nb = C.loc[~C.repro, [f"m_{b}" for b in BARS]].lt(0).sum()
        P("     which bar my reference says they fail: " +
          ", ".join(f"{b} {int(nb['m_'+b])}" for b in BARS))
        P("     top non-reproducing files: " +
          ", ".join(f"{k}({v})" for k, v in C.loc[~C.repro, "file"].value_counts().head(5).items()))
    C.to_csv(str(STEM) + ".census.csv", index=False)
    G = C.loc[C.repro].copy()
    P("")
    P(f"  ---- THE BACK-FILL: which bar was CLOSEST to binding, over {len(G):,} reproduced passes")
    for key, g in G.groupby("panel"):
        vc = g.binding.value_counts()
        P(f"  {key:6s} N={len(g):6,d}  closest bar (noise units): " +
          ", ".join(f"{b} {int(vc.get(b,0)):,} ({vc.get(b,0)/len(g):.0%})" for b in BARS))
        P(f"           median slack at that bar: raw " +
          ", ".join(f"{b} {g.loc[g.binding==b, 'm_'+b].median():+.4f}" for b in BARS if (g.binding==b).any()))
        P(f"           median min-z {g.min_z.median():+.3f}   "
          f"q10 {g.min_z.quantile(.10):+.3f}  q90 {g.min_z.quantile(.90):+.3f}")
        vr = g.binding_raw.value_counts()
        P(f"           (raw-unit argmin for comparison: " +
          ", ".join(f"{b} {int(vr.get(b,0)):,}" for b in BARS) + ")")
    vc = G.binding.value_counts()
    P(f"  ALL    N={len(G):6,d}  closest bar: " +
      ", ".join(f"{b} {int(vc.get(b,0)):,} ({vc.get(b,0)/len(G):.1%})" for b in BARS))
    G.groupby(["panel", "binding"]).agg(N=("min_z", "size"), med_min_z=("min_z", "median")) \
     .to_csv(str(STEM) + ".binding.csv")
    # ROW counts are dominated by a few very large grids: repeat the census ONE VOTE PER FILE
    fw = G.groupby(["file", "panel"]).binding.agg(lambda x: x.value_counts().idxmax())
    P(f"  FILE-WEIGHTED (one vote per (file,panel), N={len(fw)}): " +
      ", ".join(f"{b} {int((fw==b).sum())} ({(fw==b).mean():.1%})" for b in BARS))
    fwp = G.groupby(["file", "panel"]).binding.agg(lambda x: x.value_counts().idxmax()).reset_index()
    for key, g in fwp.groupby("panel"):
        P(f"     {key:6s} N={len(g):4d}: " +
          ", ".join(f"{b} {int((g.binding==b).sum())}" for b in BARS))
    # how MARGINAL are they: min-z is the distance to the nearest bar in panel-noise units
    P("  marginality of the reproduced passes (min-z = distance to the nearest bar, "
      "in that panel's random-sub-panel noise units):")
    for key, g in G.groupby("panel"):
        P(f"     {key:6s} min-z  q10 {g.min_z.quantile(.10):+.3f}  q25 {g.min_z.quantile(.25):+.3f}  "
          f"median {g.min_z.median():+.3f}  q75 {g.min_z.quantile(.75):+.3f}  "
          f"q90 {g.min_z.quantile(.90):+.3f};  share with min-z < 0.25 sd: "
          f"{(g.min_z < 0.25).mean():.1%}, < 0.50 sd: {(g.min_z < 0.50).mean():.1%}")

    # ---- how many published passes sit inside their own panel's random base rate
    P("")
    P("  ---- INSIDE THE BASE RATE?  a published pass is INSIDE its panel's random-sub-panel")
    P("       null when its min-z is no better than the MEDIAN min-z of the random draws that")
    P("       cleared 4b on that panel (i.e. it is a typical coin-flip pass, not a distinguished one).")
    inside_rows = []
    for key, g in G.groupby("panel"):
        nz = NULL.loc[(NULL.panel == key) & NULL.pass4b].copy()
        for b in BARS:
            nz[f"z_{b}"] = nz[f"slack_{b}"] / SD.loc[key, b]
        nz["min_z"] = nz[[f"z_{b}" for b in BARS]].min(axis=1)
        if len(nz) < 10:
            P(f"  {key:6s} FEWER THAN 10 random 4b passes ({len(nz)}) - the null cannot be read at")
            P("           this k grid; reported below against ALL random draws' min-z instead.")
            nz = NULL.loc[NULL.panel == key].copy()
            for b in BARS:
                nz[f"z_{b}"] = nz[f"slack_{b}"] / SD.loc[key, b]
            nz["min_z"] = nz[[f"z_{b}" for b in BARS]].min(axis=1)
        med = nz.min_z.median(); q90 = nz.min_z.quantile(.90)
        rate = float(NULL.loc[NULL.panel == key, "pass4b"].mean())
        ins = float((g.min_z <= med).mean()); ins90 = float((g.min_z <= q90).mean())
        pct = g.min_z.map(lambda v: float((nz.min_z <= v).mean()))
        P(f"  {key:6s} random 4b base rate (pooled over k, books) {rate:5.1%}; random passes N={len(nz)}, "
          f"median min-z {med:+.3f}, q90 {q90:+.3f}")
        P(f"           published passes N={len(g):,}: {ins:.1%} sit at or below the random median "
          f"min-z, {ins90:.1%} at or below its q90; median published percentile "
          f"within the random-pass null {pct.median():.1%}")
        inside_rows.append(dict(panel=key, random_base_rate=rate, n_random_pass=len(nz),
                                med_min_z_random=med, q90_min_z_random=q90,
                                n_published_pass=len(g), frac_inside_median=ins,
                                frac_inside_q90=ins90, median_percentile=float(pct.median())))
    IN = pd.DataFrame(inside_rows)
    tot = IN.n_published_pass.sum()
    wins = float((IN.frac_inside_median * IN.n_published_pass).sum() / tot)
    P(f"  ALL    {wins:.1%} of {tot:,} reproduced published 4b passes are inside the random median.")
    return C, G, SD, IN


# ================================================================= RULE 8
def rule8(PX, NULL):
    P("")
    P("=" * 100)
    P("RULE 8 - walk-forward: (k, book) chosen on IS 2009-2016 pass rate ONLY, read once on OOS")
    P("=" * 100)
    rows = []
    for (panel, k, book), g in NULL.groupby(["panel", "k", "book"]):
        rows.append(dict(panel=panel, k=k, book=book, N=len(g),
                         IS_rate=g.IS_pass4b.mean(), OOS_rate=g.OOS_pass4b.mean(),
                         full_rate=g.pass4b.mean(),
                         OOS_CAGR=g.OOS_CAGR.median(), OOS_Sharpe=g.OOS_Sharpe.median(),
                         OOS_MaxDD=g.OOS_MaxDD.median()))
    W = pd.DataFrame(rows)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    out = []
    for panel, g in W.groupby("panel"):
        pick = g.sort_values("IS_rate", ascending=False).iloc[0]
        px = PX[panel]; ref, spy = spy_ref(px, panel)
        base = ev(backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"], panel)
        bo = metrics(base.loc[OOS_START:]); so = metrics(spy.loc[OOS_START:])
        # the IS-argmax DRAW inside the picked cell, read once OOS
        cell = NULL[(NULL.panel == panel) & (NULL.k == pick.k) & (NULL.book == pick.book)]
        arg = cell.sort_values("IS_Sharpe", ascending=False).iloc[0]
        P("")
        P(f"  {panel}: IS-argmax cell k={int(pick.k)} {pick.book} (IS 4b rate {pick.IS_rate:.1%}) "
          f"-> OOS 4b rate {pick.OOS_rate:.1%} [full-sample {pick.full_rate:.1%}]")
        P(f"      cell median OOS  {pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:.3f} / {pick.OOS_MaxDD:7.2%}")
        P(f"      IS-argmax draw   {arg.OOS_CAGR:7.2%} / {arg.OOS_Sharpe:.3f} / {arg.OOS_MaxDD:7.2%}   "
          f"(IS Sharpe {arg.IS_Sharpe:.3f}, draw #{int(arg.draw)})")
        P(f"      RULES v2 baseline{bo['CAGR']:7.2%} / {bo['Sharpe']:.3f} / {bo['MaxDD']:7.2%}")
        P(f"      SPY              {so['CAGR']:7.2%} / {so['Sharpe']:.3f} / {so['MaxDD']:7.2%}")
        rank = int((cell.OOS_Sharpe > arg.OOS_Sharpe).sum()) + 1
        P(f"      the IS-argmax draw's OOS Sharpe rank inside its own cell: {rank}/{len(cell)}")
        out.append(dict(panel=panel, k=int(pick.k), book=pick.book, IS_rate=pick.IS_rate,
                        OOS_rate=pick.OOS_rate, full_rate=pick.full_rate,
                        cell_OOS_CAGR=pick.OOS_CAGR, cell_OOS_Sharpe=pick.OOS_Sharpe,
                        cell_OOS_MaxDD=pick.OOS_MaxDD, arg_draw=int(arg.draw),
                        arg_OOS_CAGR=arg.OOS_CAGR, arg_OOS_Sharpe=arg.OOS_Sharpe,
                        arg_OOS_MaxDD=arg.OOS_MaxDD, arg_OOS_rank=rank, n_cell=len(cell),
                        base_OOS_CAGR=bo["CAGR"], base_OOS_Sharpe=bo["Sharpe"], base_OOS_MaxDD=bo["MaxDD"],
                        spy_OOS_CAGR=so["CAGR"], spy_OOS_Sharpe=so["Sharpe"], spy_OOS_MaxDD=so["MaxDD"]))
    WF = pd.DataFrame(out)
    W.to_csv(str(STEM) + ".walkforward.csv", index=False)
    WF.to_csv(str(STEM) + ".rule8pick.csv", index=False)
    return W, WF


# ================================================================= KEEP paths
def keep_paths(PX, NULL, WF):
    P("")
    P("=" * 100)
    P("BOTH KEEP PATHS - the rule-8 picked cells' books, full sample, 10 bps")
    P("=" * 100)
    P("  (a census run proposes no book; these rows say what the picked draws would score.)")
    n4a = n4b = 0
    for _, w in WF.iterrows():
        px = PX[w.panel]; ref, spy = spy_ref(px, w.panel)
        base = ev(backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"], w.panel)
        r, tu, cols = draw_book(px, w.panel, int(w.k), int(w.arg_draw), w.book)
        ok4b, sl, f4b = bars_4b(r, spy); ok4a, sl4a = bars_4a(r, base)
        m = metrics(r)
        n4a += int(ok4a); n4b += int(ok4b)
        P(f"  {w.panel:6s} k={int(w.k):3d} {w.book:7s} draw#{int(w.arg_draw):3d}  "
          f"{m['CAGR']:7.2%} / {m['Sharpe']:.3f} / {m['MaxDD']:7.2%}  "
          f"H1/H2 {hs(r)[0]:.3f}/{hs(r)[1]:.3f}  4a {'KEEP' if ok4a else 'no'}  "
          f"4b {'KEEP' if ok4b else 'no (' + ','.join(f4b) + ')'}")
        P("           4b slacks: " + "  ".join(f"{b} {sl[b]:+.4f}" for b in BARS))
    P(f"  4a {n4a}/{len(WF)}   4b {n4b}/{len(WF)}")
    return n4a, n4b


def main():
    t0 = time.time()
    P(f"idea 253 lane B - {pd.Timestamp.utcnow():%Y-%m-%d %H:%M}Z   "
      f"cost {COST_BPS:.0f} bps, freq {FREQ}, draws {N_DRAWS}, OOS from {OOS_START}")
    PX = panels()
    gates(PX)
    NULL = part_a(PX)
    C, G, SD, IN = part_b(PX, NULL)
    W, WF = rule8(PX, NULL)
    keep_paths(PX, NULL, WF)
    P("")
    P(f"total runtime {time.time()-t0:.0f}s")
    Path(str(STEM) + ".console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--panel":
        PX = panels(); gates(PX); part_a_panel(PX, sys.argv[2])
    else:
        main()
