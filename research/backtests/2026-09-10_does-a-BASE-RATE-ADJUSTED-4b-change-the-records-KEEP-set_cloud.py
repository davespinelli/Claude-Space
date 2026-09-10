#!/usr/bin/env python3
"""Idea 481 — DOES A BASE-RATE-ADJUSTED 4b CHANGE THE RECORD'S KEEP SET?

Idea 253 found (a) that random sub-panels clear PROTOCOL 4b at a non-trivial base rate (U56
28.1%, B136 23.0%, SMALL 0.0% of 900), (b) that 46.8% of the record's 25,028 reproduced 4b
passes sit inside their own panel's random-sub-panel null, and (c) that the base rate does not
walk forward (B136 49.3% IS -> 26.0% OOS).  A bar that admits noise at 23-28% is not a bar.

This run PRE-REGISTERS the obvious repair — a min-z FLOOR — and re-scores the record with it:

    BASE-RATE-ADJUSTED 4b (BRA-4b).  Let sd_null(bar | panel) be the sd of that 4b bar's slack
    across the panel's random sub-panel draws.  For a candidate, z_bar = slack_bar /
    sd_null(bar|panel) and min_z = min over the five bars.  The candidate passes BRA-4b iff it
    passes 4b AND min_z > z*(panel, q), where z*(panel, q) is the q-th quantile of min_z over
    the random draws THAT THEMSELVES CLEARED 4b on that panel.
    Read plainly: "beat the q-th percentile of the coin flips that also cleared the bar."

Pre-registration (fixed before any number of this run was read):

  * TWO tuned parameters and no more: FLOORQ (the floor quantile, ladder 0.50 / 0.75 / 0.90 /
    0.95 / 0.99, headline q=0.90 as the idea specifies) and PANEL (U56 / B136 / SMALL).  The
    sub-panel size k, the null book (EWall / CAND20), the cost rung and every bar are REPORTED
    at every point, never chosen.  Every grid point is written to disk.

  * PART A — THE NULL.  Idea 253's null reproduced verbatim: 3 panels x 3 k x 2 books x 150
    deterministic draws (seeded off (panel, k, draw)), gross 0.75, weekly, 10 bps, next-day
    execution, 200d-MA + vol<60% eligibility.  GATE A asserts the U56 and B136 base rates
    reproduce idea 253's published 28.1% / 23.0%.  ONE deliberate deviation, stated up front:
    the small panel drops the 44 names with `max_1d_move >= 1.0` (data/small_meta.csv) before
    any draw, per the current standing instruction; idea 253 did not.  U56 and B136 are
    untouched, which is why the gate is read on those two.

  * PART B — RE-SCORE THE RECORD.  Every mechanically recoverable published 4b PASS in the
    committed CSVs (idea 253's harvest, unchanged: a file must carry a 4b flag column, a panel
    column and CAGR/Sharpe/MaxDD/H1/H2/OOS_Sharpe).  Rows whose published pass does not
    reproduce against this run's panel SPY reference are EXCLUDED from every margin statistic.
    Report the surviving KEEP set at every q, per panel.

  * PART C — IDEA 247'S LIVE CANDIDATE, re-run rather than read off the record: ISFIX(q=0.80)
    — BAND3-de-grossed when SPY vol20 >= the IS-only 80th percentile, EW_ALL otherwise, gross
    0.75 — on all three panels at 10 and 25 bps.  Its five slacks, min_z and BRA-4b verdict at
    every q are reported beside the record's.

  * PART D — RULE 8 (PROTOCOL 8).  The floor is re-fitted on the IS window (<= 2016-12-31)
    ALONE — an IS-only null, IS-only sds, IS-only random passes — and the OOS window
    (2017-01-01..) is then read ONCE: the OOS base rate, the OOS admission of the IS-fitted
    floor, and the candidate's OOS CAGR/Sharpe/MaxDD against native RULES v2 and SPY.

  * BOTH KEEP PATHS on every arm: 4a against the live book (native RULES v2, same panel,
    window, rung); 4b against SPY.

SURVIVORSHIP (PROTOCOL 9, idea 54): B136 and SMALL are CURRENT-constituent lists, so their
levels are biased upward and unequally so; only within-panel contrasts (an arm against its own
panel's null) are load-bearing here — which is exactly what a base-rate adjustment is.  U56 is
a fixed ETF/mega-cap list and is least biased.

Costs 10/25 bps per unit turnover, weekly, next-day execution (PROTOCOL 1-2).  Deterministic,
no network.  Writes .null.csv, .census.csv, .floor.csv, .candidate.csv, .walkforward.csv,
.console.txt.
"""
import glob
import hashlib
import re
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, score   # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, metrics, rebalance_mask   # noqa

HERE = Path(__file__).resolve()
STEM = HERE.with_suffix("")
FREQ, GROSS, MAX_VOL, CAND_N = "W", 0.75, 0.60, 20
COST_BPS = 10.0
RUNGS = [10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
N_DRAWS = 150
K_GRID = {"U56": [14, 28, 42], "B136": [20, 40, 80], "SMALL": [60, 120, 240]}
NULL_BOOKS = ["EWall", "CAND20"]
BARS = ["H1", "H2", "OOS", "DD", "CAGR"]
WBARS = ["H1", "H2", "DD", "CAGR"]            # in-window 4b (no separate OOS leg)
QLADDER = [0.50, 0.75, 0.90, 0.95, 0.99]
HEADLINE_Q = 0.90

_LOG = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ---------------------------------------------------------------- engine twin
def fast_backtest(px, weights, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n); gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return (pd.Series(port, index=px.index), pd.Series(turn, index=px.index),
            pd.Series(gross, index=px.index))


def net(r0, turn, bps=COST_BPS):
    return r0 - turn * bps / 1e4


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy, oos_start=OOS_START):
    """PROTOCOL 4b slacks; positive = passing."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[oos_start:])["Sharpe"] - metrics(spy.loc[oos_start:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    return (min(d.values()) >= 0), d


def bars_4b_window(r, spy):
    """4b inside ONE window (the window IS the evaluation; no separate OOS leg)."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    d = {"H1": h1 - s1, "H2": h2 - s2,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    return (min(d.values()) >= 0), d


def bars_4b_from_cells(CAGR, H1, H2, MaxDD, OOS_Sharpe, ref):
    return {"H1": H1 - ref["H1"], "H2": H2 - ref["H2"],
            "OOS": OOS_Sharpe - ref["OOS_Sharpe"],
            "DD": 0.60 * abs(ref["MaxDD"]) - abs(MaxDD),
            "CAGR": CAGR - 0.70 * ref["CAGR"]}


def bars_4a(r, base):
    d = {"H1": hs(r)[0] - hs(base)[0], "H2": hs(r)[1] - hs(base)[1],
         "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    return (min(d.values()) >= 0), d


# ---------------------------------------------------------------- null books (idea 78/83)
def _elig(sub):
    _, above, vol20 = score(sub)
    return above & (vol20 < MAX_VOL)


def ew_weights_sub(sub, g=GROSS):
    e = _elig(sub)
    return e.astype(float).div(e.sum(axis=1).replace(0, np.nan), axis=0).mul(g).fillna(0.0)


def cand_weights_sub(sub, n=CAND_N, g=GROSS):
    e = _elig(sub)
    s = score(sub, vol_scale=False)[0]
    rank = s.where(e).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


def rng_for(panel, k, d):
    h = hashlib.sha256(f"{panel}|{k}|{d}".encode()).hexdigest()[:8]
    return np.random.default_rng(int(h, 16))


# ---------------------------------------------------------------- idea 247's candidate
def ew_weights_full(px, cols, g=GROSS):
    p = px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    w = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def band3dg_weights(px, cols, g=GROSS):
    return ew_weights_full(px, cols, g).where(
        band_state(px[cols], 0.03).reindex(columns=px.columns).fillna(False), 0.0)


def isfix_weights(px, cols, q=0.80, g=GROSS):
    """Idea 247's repaired arm: BAND3-dg when SPY vol20 >= the IS-ONLY q-th percentile
    (threshold frozen for the whole sample -> causal), EW_ALL otherwise."""
    v = px["SPY"].pct_change().rolling(20).std() * np.sqrt(252)
    thr = float(v.loc[:IS_END].dropna().quantile(q))
    armed = (v >= thr).fillna(False)
    W, B = ew_weights_full(px, cols, g), band3dg_weights(px, cols, g)
    return B.where(armed, axis=0).fillna(0.0) + W.where(~armed, axis=0).fillna(0.0), thr, armed


# ---------------------------------------------------------------- panels
START, PKEY = {}, {"U56": {}, "B136": {"broad": True}, "SMALL": {"small": True}}


def panels():
    out, cols = {}, {}
    for key, kw in PKEY.items():
        px = load_universe(**kw).dropna(how="all").ffill()
        if key == "SMALL":
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
            n0 = len([c for c in px.columns if c != "SPY"])
            px = px[[c for c in px.columns if c == "SPY" or c not in bad]]
            P(f"  SMALL: dropped {n0 - len([c for c in px.columns if c != 'SPY'])} names with"
              f" max_1d_move >= 1.0; {len([c for c in px.columns if c != 'SPY'])} remain"
              f"  [deliberate deviation from idea 253's null]")
        START[key] = px.index[260]
        out[key] = px
        cols[key] = [c for c in px.columns if c != "SPY"]
    return out, cols


def ev(r, key):
    return r.loc[START[key]:]


def spy_ref(px, key):
    spy = ev(px["SPY"].pct_change().fillna(0.0), key)
    m = metrics(spy); h1, h2 = hs(spy)
    return {"CAGR": m["CAGR"], "Sharpe": m["Sharpe"], "MaxDD": m["MaxDD"], "H1": h1, "H2": h2,
            "OOS_Sharpe": metrics(spy.loc[OOS_START:])["Sharpe"]}, spy


# ================================================================= PART A
def part_a(PX):
    P("=" * 100)
    P("PART A — THE NULL (idea 253's, reproduced): 3 panels x 3 k x 2 books x %d draws" % N_DRAWS)
    P("=" * 100)
    rows = []
    for key, px in PX.items():
        names = [c for c in px.columns if c != "SPY"]
        _, spy = spy_ref(px, key)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        for k in K_GRID[key]:
            for book in NULL_BOOKS:
                for d in range(N_DRAWS):
                    cs = list(rng_for(key, k, d).choice(names, size=k, replace=False))
                    sub = px[cs].dropna(how="all").ffill()
                    w = ew_weights_sub(sub) if book == "EWall" else cand_weights_sub(sub)
                    r0, tu, _ = fast_backtest(sub, w)
                    r = ev(net(r0, tu), key)
                    ok, sl = bars_4b(r, spy)
                    okI, slI = bars_4b_window(r.loc[:IS_END], spy_is)
                    okO, slO = bars_4b_window(r.loc[OOS_START:], spy_oos)
                    rows.append(dict(panel=key, k=k, book=book, draw=d, pass4b=ok,
                                     **{f"slack_{b}": sl[b] for b in BARS},
                                     passIS=okI, **{f"IS_{b}": slI[b] for b in WBARS},
                                     passOOS=okO, **{f"OOS_{b}": slO[b] for b in WBARS}))
            P(f"    {key} k={k}: done")
    NULL = pd.DataFrame(rows)
    NULL.to_csv(str(STEM) + ".null.csv", index=False)
    P("")
    P("  4b base rate by (panel, k, book) — every grid point:")
    br = NULL.pivot_table(index=["panel", "k"], columns="book", values="pass4b")
    P(br.to_string(float_format=lambda x: f"{x:.1%}"))
    P("  pooled base rate: " + "  ".join(
        f"{k} {NULL.loc[NULL.panel == k, 'pass4b'].mean():.1%} ({int(NULL.loc[NULL.panel==k,'pass4b'].sum())}"
        f"/{int((NULL.panel==k).sum())})" for k in PX))
    return NULL


def noise_sd(NULL, cols, prefix="slack_"):
    return (NULL.groupby("panel")[[f"{prefix}{b}" for b in cols]].std()
            .rename(columns={f"{prefix}{b}": b for b in cols}))


def add_minz(df, SD, panel, cols, prefix="slack_"):
    z = pd.DataFrame({b: df[f"{prefix}{b}"] / SD.loc[panel, b] for b in cols}, index=df.index)
    return z.min(axis=1), z.idxmin(axis=1)


def floors(NULL, SD, cols, passcol="pass4b", prefix="slack_"):
    """z*(panel, q): the q-th quantile of min_z over the random draws that CLEARED 4b."""
    out, note = {}, {}
    for key, g in NULL.groupby("panel"):
        nz = g.loc[g[passcol]].copy()
        src = "random 4b passes"
        if len(nz) < 10:
            nz, src = g.copy(), "ALL random draws (fewer than 10 random passes)"
        mz, _ = add_minz(nz, SD, key, cols, prefix)
        out[key] = {q: float(mz.quantile(q)) for q in QLADDER}
        note[key] = (src, len(nz), float(mz.median()))
    return out, note


# ================================================================= PART B
PANEL_MAP = [(re.compile(r"^(u56|universe\.json\(56\)|U56)$", re.I), "U56"),
             (re.compile(r"^(b136|broad136|broad|BROAD136|universe_broad\(136\))$", re.I), "B136"),
             (re.compile(r"^(small\d*|SMALL|small|SMALL439\+SPY)$", re.I), "SMALL")]
NEED = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]
FLAGCOLS = ["pass4b", "keep4b", "f4b", "fail4b", "p4b"]


def map_panel(v):
    v = str(v).strip()
    for rx, key in PANEL_MAP:
        if rx.match(v):
            return key
    return None


def published_pass(d, col):
    if col in ("pass4b", "keep4b"):
        return d[col].astype(str).str.strip().str.lower().isin(["true", "1", "1.0", "yes"])
    if col == "p4b":
        return pd.to_numeric(d[col], errors="coerce") > 0
    return d[col].isna() | d[col].astype(str).str.strip().isin(["-", "", "nan", "none"])


def part_b(PX, SD):
    P("")
    P("=" * 100)
    P("PART B — RE-SCORE: every mechanically recoverable published 4b PASS in the record")
    P("=" * 100)
    REF = {k: spy_ref(px, k)[0] for k, px in PX.items()}
    P("  noise units sd_null(bar | panel), pooled over all k and both books:")
    P(SD.to_string(float_format=lambda x: f"{x:.4f}"))
    files = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv")))
    seen = dict(files=0, cand=0, used=0, rows=0, pas=0, unmapped=0)
    out = []
    for f in files:
        if Path(f).name.startswith(HERE.stem):
            continue
        seen["files"] += 1
        try:
            hdr = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception:
            continue
        if not any("4b" in c.lower() for c in hdr):
            continue
        seen["cand"] += 1
        if not all(c in hdr for c in NEED):
            continue
        fc = next((c for c in FLAGCOLS if c in hdr), None)
        pcol = "panel" if "panel" in hdr else ("universe" if "universe" in hdr else None)
        if fc is None or pcol is None:
            continue
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        seen["used"] += 1; seen["rows"] += len(d)
        d = d.loc[published_pass(d, fc)].copy()
        if d.empty:
            continue
        seen["pas"] += len(d)
        d["_panel"] = d[pcol].map(map_panel)
        seen["unmapped"] += int(d["_panel"].isna().sum())
        d = d.loc[d["_panel"].notna()].copy()
        if d.empty:
            continue
        for c in NEED:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d = d.dropna(subset=NEED)
        if d.empty:
            continue
        for key, g in d.groupby("_panel"):
            sl = bars_4b_from_cells(g["CAGR"], g["H1"], g["H2"], g["MaxDD"], g["OOS_Sharpe"],
                                    REF[key])
            M = pd.DataFrame({f"m_{b}": sl[b] for b in BARS}, index=g.index)
            M["repro"] = (M[[f"m_{b}" for b in BARS]] >= 0).all(axis=1)
            M["panel"] = key; M["file"] = Path(f).name
            mz, bind = add_minz(M, SD, key, BARS, prefix="m_")
            M["min_z"] = mz; M["binding"] = bind
            M["binding_raw"] = M[[f"m_{b}" for b in BARS]].idxmin(axis=1).str[2:]
            out.append(M)
    C = pd.concat(out, ignore_index=True)
    C.to_csv(str(STEM) + ".census.csv", index=False)
    P(f"  corpus: {seen['files']} committed CSVs, {seen['cand']} carry a 4b column,"
      f" {seen['used']} carry 4b + panel + all of {NEED}")
    P(f"  rows {seen['rows']:,}; published 4b PASS rows {seen['pas']:,};"
      f" panel unmappable {seen['unmapped']:,}; recovered with metrics {len(C):,}")
    P(f"  REPRODUCTION GATE: {int(C.repro.sum()):,} of {len(C):,}"
      f" ({C.repro.mean():.1%}) re-derive as a pass against this run's panel SPY reference;"
      f" the other {int((~C.repro).sum()):,} are EXCLUDED from every statistic below.")
    return C.loc[C.repro].copy()


# ================================================================= main
def main():
    P("=" * 100); P("PANELS"); P("=" * 100)
    PX, COLS = panels()
    for k, px in PX.items():
        P(f"  {k:6s} {len(COLS[k]):4d} names, window {START[k].date()}..{px.index[-1].date()}")

    # ---------------- GATES
    P("")
    P("=== GATES ===")
    px = PX["U56"]
    sub = px[COLS["U56"][:20]].dropna(how="all").ffill()
    w = ew_weights_sub(sub)
    r0, t0, _ = fast_backtest(sub, w)
    live = engine_backtest(sub, w, cost_bps=COST_BPS, freq=FREQ)
    dr = float(np.abs(ev(net(r0, t0), "U56").values - ev(live["returns"], "U56").values).max())
    dt = float(np.abs(ev(t0, "U56").values - ev(live["turnover"], "U56").values).max())
    P(f"G1 fast_backtest vs engine.backtest  max|dret| {dr:.3e}  max|dturn| {dt:.3e}")
    assert dr < 1e-12 and dt < 1e-12, "G1 FAILED"
    w247, thr, armed = isfix_weights(px, COLS["U56"], 0.80)
    P(f"G2 idea 247's ISFIX(0.80) threshold on U56: theta={thr:.4f}"
      f" (published 0.2125), armed IS {armed.loc[:IS_END].mean():.1%} /"
      f" OOS {armed.loc[OOS_START:].mean():.1%} (published 15.5% / 16.4%)")
    assert abs(thr - 0.2125) < 5e-3, "G2 FAILED"

    NULL = part_a(PX)
    P("")
    P("GATE A — idea 253's published base rates (U56 28.1%, B136 23.0%) must reproduce:")
    for key, pub in (("U56", 0.281), ("B136", 0.230)):
        got = float(NULL.loc[NULL.panel == key, "pass4b"].mean())
        P(f"   {key}: {got:.1%} vs published {pub:.1%}  (|d| {abs(got-pub):.1%})")
        assert abs(got - pub) < 0.02, f"GATE A FAILED on {key}"
    P("   PASS — the null is idea 253's null.  SMALL is not gated (its panel differs by the"
      " 44-name max_1d_move drop stated above).")

    SD = noise_sd(NULL, BARS)
    FL, NOTE = floors(NULL, SD, BARS)
    P("")
    P("=== THE PRE-REGISTERED FLOOR  z*(panel, q) ===")
    for key in PX:
        src, n, med = NOTE[key]
        P(f"  {key:6s} floor read on {n} {src}; median min-z {med:+.3f};  " +
          "  ".join(f"q{int(q*100)}={FL[key][q]:+.3f}" for q in QLADDER))

    G = part_b(PX, SD)

    # ---- the KEEP-set restatement
    P("")
    P("=== THE RESTATEMENT: how much of the record's published 4b KEEP set survives BRA-4b ===")
    rows = []
    for key, g in G.groupby("panel"):
        line = f"  {key:6s} N={len(g):6,d} reproduced passes; median min-z {g.min_z.median():+.3f};"
        for q in QLADDER:
            sv = float((g.min_z > FL[key][q]).mean())
            rows.append(dict(panel=key, q=q, floor=FL[key][q], n=len(g), survive=sv,
                             n_survive=int((g.min_z > FL[key][q]).sum())))
            line += f"  q{int(q*100)}: {sv:.1%}"
        P(line)
    FLR = pd.DataFrame(rows)
    tot = {q: (int(FLR.loc[FLR.q == q, "n_survive"].sum()), int(FLR.loc[FLR.q == q, "n"].sum()))
           for q in QLADDER}
    P("  ALL PANELS POOLED: " + "  ".join(
        f"q{int(q*100)} {tot[q][0]:,}/{tot[q][1]:,} = {tot[q][0]/tot[q][1]:.1%}" for q in QLADDER))
    P(f"  HEADLINE (q={HEADLINE_Q}): the base-rate adjustment removes"
      f" {1 - tot[HEADLINE_Q][0]/tot[HEADLINE_Q][1]:.1%} of the record's reproduced 4b passes.")
    P("  binding bar among SURVIVORS at q=0.90 (noise units): " +
      ", ".join(f"{b} {int((G.loc[G.apply(lambda r: r.min_z > FL[r.panel][HEADLINE_Q], axis=1), 'binding'] == b).sum()):,}"
                for b in BARS))
    FLR.to_csv(str(STEM) + ".floor.csv", index=False)

    # ---------------- PART C — idea 247's live candidate, re-run
    P("")
    P("=" * 100)
    P("PART C — IDEA 247'S LIVE CANDIDATE (ISFIX 0.80), re-run and put through BRA-4b")
    P("=" * 100)
    crows = []
    for key, px in PX.items():
        ref, spy = spy_ref(px, key)
        w247, thr, armed = isfix_weights(px, COLS[key], 0.80)
        r0, tu, gr = fast_backtest(px, w247)
        b0, bt, _ = fast_backtest(px, rules_v2_weights(px))
        for bps in RUNGS:
            r = ev(net(r0, tu, bps), key)
            base = ev(net(b0, bt, bps), key)
            ok4b, sl = bars_4b(r, spy)
            ok4a, sl4a = bars_4a(r, base)
            M = pd.DataFrame([{f"m_{b}": sl[b] for b in BARS}])
            mz, bind = add_minz(M, SD, key, BARS, prefix="m_")
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            crows.append(dict(panel=key, bps=bps, theta=thr, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                              MaxDD=m["MaxDD"], H1=hs(r)[0], H2=hs(r)[1],
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              gross=float(ev(gr, key).mean()),
                              **{f"slack_{b}": sl[b] for b in BARS},
                              min_z=float(mz.iloc[0]), binding=str(bind.iloc[0]),
                              keep4a=ok4a, keep4b=ok4b,
                              **{f"BRA_q{int(q*100)}": bool(ok4b and float(mz.iloc[0]) > FL[key][q])
                                 for q in QLADDER}))
    CAND = pd.DataFrame(crows)
    CAND.to_csv(str(STEM) + ".candidate.csv", index=False)
    P(CAND[["panel", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "min_z",
            "binding", "keep4a", "keep4b"] + [f"BRA_q{int(q*100)}" for q in QLADDER]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  slacks (raw units, positive = passing):")
    P(CAND[["panel", "bps"] + [f"slack_{b}" for b in BARS]].to_string(
        index=False, float_format=lambda x: f"{x:+.4f}"))
    for _, r in CAND.iterrows():
        pct = float((G.loc[G.panel == r.panel, "min_z"] <= r.min_z).mean()) if (G.panel == r.panel).any() else np.nan
        P(f"  {r.panel:6s} @{int(r.bps)}bps: min_z {r.min_z:+.3f} (binding {r.binding});"
          f" floor q90 {FL[r.panel][HEADLINE_Q]:+.3f} -> BRA-4b"
          f" {'PASS' if r[f'BRA_q{int(HEADLINE_Q*100)}'] else 'FAIL'};"
          f" it sits at the {pct:.1%} percentile of the record's own reproduced passes")

    # ---------------- PART D — RULE 8
    P("")
    P("=" * 100)
    P("RULE 8 — floor RE-FITTED on IS <= %s alone; OOS %s.. read ONCE" % (IS_END, OOS_START))
    P("=" * 100)
    SD_IS = noise_sd(NULL, WBARS, prefix="IS_")
    SD_OOS = noise_sd(NULL, WBARS, prefix="OOS_")
    FL_IS, NOTE_IS = floors(NULL, SD_IS, WBARS, passcol="passIS", prefix="IS_")
    wf = []
    for key in PX:
        gI = NULL.loc[NULL.panel == key]
        mzO, _ = add_minz(gI, SD_IS, key, WBARS, prefix="OOS_")     # IS units, OOS slacks
        for q in QLADDER:
            adm_is = float(((gI["passIS"]) & (add_minz(gI, SD_IS, key, WBARS, "IS_")[0]
                                              > FL_IS[key][q])).mean())
            adm_oos = float(((gI["passOOS"]) & (mzO > FL_IS[key][q])).mean())
            wf.append(dict(panel=key, q=q, floor_IS=FL_IS[key][q],
                           base_IS=float(gI.passIS.mean()), base_OOS=float(gI.passOOS.mean()),
                           admit_IS=adm_is, admit_OOS=adm_oos))
        P(f"  {key:6s} raw base rate IS {gI.passIS.mean():.1%} -> OOS {gI.passOOS.mean():.1%}"
          f"  (idea 253: does not transfer)")
        for q in QLADDER:
            w = [x for x in wf if x["panel"] == key and x["q"] == q][0]
            P(f"          q{int(q*100)} floor {w['floor_IS']:+.3f}: admits"
              f" {w['admit_IS']:.1%} of IS draws and {w['admit_OOS']:.1%} of the SAME draws OOS")
    WF = pd.DataFrame(wf)

    # candidate through rule 8
    P("")
    P("  IDEA 247's CANDIDATE under the IS-fitted floor, OOS window read once:")
    crows2 = []
    for key, px in PX.items():
        ref, spy = spy_ref(px, key)
        w247, thr, _ = isfix_weights(px, COLS[key], 0.80)
        r0, tu, _ = fast_backtest(px, w247)
        b0, bt, _ = fast_backtest(px, rules_v2_weights(px))
        for bps in RUNGS:
            r = ev(net(r0, tu, bps), key)
            base = ev(net(b0, bt, bps), key)
            rI, rO = r.loc[:IS_END], r.loc[OOS_START:]
            sI, sO = spy.loc[:IS_END], spy.loc[OOS_START:]
            okI, slI = bars_4b_window(rI, sI)
            okO, slO = bars_4b_window(rO, sO)
            mzI = add_minz(pd.DataFrame([{f"IS_{b}": slI[b] for b in WBARS}]), SD_IS, key,
                           WBARS, "IS_")[0].iloc[0]
            mzO = add_minz(pd.DataFrame([{f"IS_{b}": slO[b] for b in WBARS}]), SD_IS, key,
                           WBARS, "IS_")[0].iloc[0]
            mo, mb, ms = metrics(rO), metrics(base.loc[OOS_START:]), metrics(sO)
            crows2.append(dict(panel=key, bps=bps,
                               IS_pass=okI, IS_min_z=float(mzI), floor_IS=FL_IS[key][HEADLINE_Q],
                               IS_admit=bool(okI and mzI > FL_IS[key][HEADLINE_Q]),
                               OOS_pass=okO, OOS_min_z=float(mzO),
                               OOS_admit=bool(okO and mzO > FL_IS[key][HEADLINE_Q]),
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               base_OOS_CAGR=mb["CAGR"], base_OOS_Sharpe=mb["Sharpe"],
                               base_OOS_MaxDD=mb["MaxDD"],
                               spy_OOS_CAGR=ms["CAGR"], spy_OOS_Sharpe=ms["Sharpe"],
                               spy_OOS_MaxDD=ms["MaxDD"]))
    C2 = pd.DataFrame(crows2)
    P(C2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pd.concat([WF, C2], axis=0, ignore_index=True).to_csv(str(STEM) + ".walkforward.csv",
                                                          index=False)

    # ---------------- KEEP paths
    P("")
    P("=== BOTH KEEP PATHS (idea 247's candidate, all panels, both rungs) ===")
    P(f"  4a {int(CAND.keep4a.sum())}/{len(CAND)}   4b {int(CAND.keep4b.sum())}/{len(CAND)}"
      f"   BRA-4b @q=0.90 {int(CAND[f'BRA_q{int(HEADLINE_Q*100)}'].sum())}/{len(CAND)}")

    P("")
    P("=" * 100)
    P("VERDICT INPUTS")
    P("=" * 100)
    P(f"  record's reproduced 4b passes surviving BRA-4b @q=0.90:"
      f" {tot[HEADLINE_Q][0]:,}/{tot[HEADLINE_Q][1]:,} = {tot[HEADLINE_Q][0]/tot[HEADLINE_Q][1]:.1%}")
    P(f"  idea 247's live candidate: 4b {int(CAND.keep4b.sum())}/{len(CAND)} cells,"
      f" BRA-4b {int(CAND[f'BRA_q{int(HEADLINE_Q*100)}'].sum())}/{len(CAND)} cells,"
      f" 4a {int(CAND.keep4a.sum())}/{len(CAND)}")
    (Path(str(STEM) + ".console.txt")).write_text("\n".join(_LOG) + "\n")
    P("wrote .null.csv .census.csv .floor.csv .candidate.csv .walkforward.csv .console.txt")
    (Path(str(STEM) + ".console.txt")).write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
