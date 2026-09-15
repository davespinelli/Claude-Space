#!/usr/bin/env python3
"""Idea 974 (cloud lane, 2026-09-15):
    should-every-PHASE-CHOOSING-CLAIM-in-the-record-carry-its-FAMILY-S-OWN-BLIND-BASE-RATE

Idea 965 found 37 of 47 (0.787) of the 4b passes an annual phase chooser produced sit on a
family whose own coin flip clears 4b at least 25% of the time.  The queue asks: census EVERY
committed phase-conditional 4b PASS in the record for its family's own blind base rate, and
report how many survive as evidence.

Two legs, both run here:
  (A) RECORD CENSUS  - harvest every committed csv artifact that carries a `phase` column AND
      a 4b-pass column, rebuild each PASS row's own phase family from the same file, and read
      the family's blind base rate (share of that family's phases that also pass).
  (B) FRESH CONTROL GRID - 3 panels x 3 books x 2 gross x (21 monthly + 63 quarterly) phases
      at the protocol's 10 bps, so the base rates are measured on a balanced design the record
      does not control, plus the rule-8 walk-forward (phase chosen on 2009-2016 alone,
      2017-2026 read once) that says whether CHOOSING a phase beats picking one blind.

TUNED PARAMETERS: exactly 2, per the queue line - CLAIM SET (STRICT / WIDE / GRID) and
CADENCE (M / Q / pooled).  Every level of both is reported; neither is chosen.  Panel, book,
gross, chooser and cost rung are reported at all grid points and are not tuned.

PROTOCOL: costs 10 bps/unit turnover, weights decided at close t applied at t+1 (engine
semantics, gate G1 below), both KEEP paths evaluated, rule 8 walk-forward run.
Writes only research/backtests/* artifacts.  RULES.md / scan.py / bot.py / baseline.py
untouched.  No network: every panel comes from the committed caches.
"""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
warnings.filterwarnings("ignore")

from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa: E402

TODAY = "2026-09-15"
SLUG = "phase-claims-vs-family-blind-base-rate"
OUT = Path(__file__).resolve().parent
COST_BPS = 10.0

# ---------------------------------------------------------------- pre-registered bars
# Declared before any number below was computed.  A bar is a bar: no bar is moved later.
BAR_NONCERT = 0.25   # H_NONCERT PASSES if the MEDIAN family blind base rate over committed
                     # phase-conditional 4b PASS rows is >= 0.25 (i.e. the record's phase
                     # passes typically sit where a blind coin flip clears 4b >= 1 time in 4).
BAR_SURV    = 0.50   # H_SURV PASSES if >= 50% of committed phase-conditional 4b PASS rows
                     # sit on a family with blind base rate < 0.25 ("survive as evidence").
BAR_LIFT    = 1.50   # H_LIFT PASSES if the OOS 4b pass rate of IS-CHOSEN phases is >= 1.5x
                     # the blind within-family OOS 4b base rate of the same families.
BAR_RULE8   = 1      # H_RULE8 PASSES if >= 1 rule-8 pick clears 4b out of sample.

IS_END   = "2016-12-31"
OOS_START = "2017-01-01"

# ==================================================================== fast engine-exact core
def fast_backtest(px: pd.DataFrame, w: pd.DataFrame, raw_mask: np.ndarray, cost_bps=COST_BPS):
    """Bit-for-bit reproduction of products/backtester/engine.backtest in numpy.

    Same arithmetic, same order of operations, same t->t+1 application; only the pandas
    row-assignment is replaced.  Gate G1 checks it against the engine itself.
    `raw_mask` is the UNSHIFTED rebalance mask (engine shifts it by one day internally).
    """
    P = px.to_numpy(dtype=float)
    R = np.zeros_like(P)
    with np.errstate(invalid="ignore", divide="ignore"):
        R[1:] = P[1:] / P[:-1] - 1.0
    R = np.nan_to_num(R, nan=0.0, posinf=0.0, neginf=0.0)

    W = np.nan_to_num(w.reindex(px.index).to_numpy(dtype=float), nan=0.0)
    WT = np.empty_like(W); WT[0] = np.nan; WT[1:] = W[:-1]      # .fillna(0).shift(1) -> row 0 NaN
    #   row 0 is NaN in the engine too (it fills BEFORE shifting), which poisons the series
    #   until the first scheduled rebalance.  Reproduced here on purpose: every window used
    #   below starts at px.index[260], well past it, and gate G1 asserts both are finite there.
    M = np.zeros(len(P), dtype=bool); M[1:] = raw_mask[:-1]     # mask.shift(1, fill=False)

    n = P.shape[1]
    cur = np.zeros(n)
    port = np.zeros(len(P)); turn = np.zeros(len(P))
    for i in range(len(P)):
        if M[i] or i == 0:
            new = WT[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = (cur * R[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + R[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def phase_mask(idx: pd.DatetimeIndex, cadence: str, phase: int) -> np.ndarray:
    """Phase family of a cadence: phase p rebalances p TRADING DAYS BEFORE each period end.
    p = 0 is the CANONICAL book (period-end), which is what the live rules trade.
    M has 21 phases, Q has 63 - one per trading day in an average period."""
    canon = np.flatnonzero(rebalance_mask(idx, cadence).to_numpy())
    pos = np.clip(canon - phase, 0, len(idx) - 1)
    m = np.zeros(len(idx), dtype=bool); m[np.unique(pos)] = True
    return m

N_PHASES = {"M": 21, "Q": 63}

# ==================================================================== panels and books
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])   # ALWAYS dropped, per lane rule
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)

def load_panels():
    u = load_universe()
    b = load_universe(broad=True)
    s, n_dropped = small_panel()
    return {"U56": u, "B136": b, "SMALL": s}, n_dropped

def _elig(px):
    _, above, vol20 = score(px, vol_scale=False)
    return above & (vol20 < 0.60) & px.notna()

def book_top20(px, gross):
    """The standing 2026-09-04 KEEP-4b candidate: top-20 by composite, EQUAL WEIGHT,
    NO vol scaler."""
    s, above, vol20 = score(px, vol_scale=False)
    e = s.where(above & (vol20 < 0.60))
    rank = e.rank(axis=1, ascending=False)
    return (rank <= 20).astype(float) * (gross / 20.0)

def book_ewelig(px, gross):
    """Equal weight EVERY eligible name (finding 2 of the 2026-09-03 memo)."""
    e = _elig(px).astype(float)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def book_band03(px, gross):
    """RULES v2's own book: the 200d +/-3% hysteresis band, de-grossing to cash."""
    return rules_v2_weights(px, band=0.03, gross=gross)

BOOKS = {"TOP20": book_top20, "EWELIG": book_ewelig, "BAND03": book_band03}
GROSSES = [0.75, 1.00]

# ==================================================================== windows and the 4b legs
def windows(idx):
    start = idx[260]                                   # same warm-up skip as baseline.compare
    full = idx[idx >= start]
    h = len(full) // 2
    return dict(FULL=(full[0], full[-1]), H1=(full[0], full[h - 1]), H2=(full[h], full[-1]),
                IS=(full[0], pd.Timestamp(IS_END)), OOS=(pd.Timestamp(OOS_START), full[-1]))

def wmetrics(r, win):
    out = {}
    for k, (a, b) in win.items():
        seg = r.loc[a:b]
        m = metrics(seg)
        out[k] = (m["CAGR"], m["Sharpe"], m["MaxDD"])
    return out

def legs_4b(m, spy):
    """PROTOCOL rule 4b, five legs, each reported separately."""
    return dict(L_H1   = m["H1"][1]  > spy["H1"][1],
                L_H2   = m["H2"][1]  > spy["H2"][1],
                L_OOS  = m["OOS"][1] > spy["OOS"][1],
                L_DD   = abs(m["FULL"][2]) <= 0.60 * abs(spy["FULL"][2]),
                L_CAGR = m["FULL"][0] >= 0.70 * spy["FULL"][0])

def legs_4b_oos(m, spy):
    """The same five legs read ENTIRELY inside 2017-2026 (rule 8's untouched window):
    halves of OOS, OOS itself, OOS drawdown and OOS CAGR."""
    return dict(L_H1=m["OOSH1"][1] > spy["OOSH1"][1], L_H2=m["OOSH2"][1] > spy["OOSH2"][1],
                L_OOS=m["OOS"][1] > spy["OOS"][1],
                L_DD=abs(m["OOS"][2]) <= 0.60 * abs(spy["OOS"][2]),
                L_CAGR=m["OOS"][0] >= 0.70 * spy["OOS"][0])

def legs_4a(m, base):
    return dict(A_H1=m["H1"][1] > base["H1"][1], A_H2=m["H2"][1] > base["H2"][1],
                A_DD=m["FULL"][2] >= base["FULL"][2])

# ==================================================================== gate G1
def gate_g1(panels):
    """The fast core must reproduce the committed engine EXACTLY, not approximately."""
    worst = 0.0; checks = []
    for pname, px in panels.items():
        for bname, gross, cad in [("TOP20", 0.75, "M"), ("EWELIG", 1.00, "Q"), ("BAND03", 0.75, "W")]:
            w = BOOKS[bname](px, gross)
            rm = rebalance_mask(px.index, cad).to_numpy()
            mine, _ = fast_backtest(px, w, rm)
            theirs = engine_backtest(px, w, cost_bps=COST_BPS, freq=cad)["returns"]
            a, b = mine.to_numpy()[260:], theirs.to_numpy()[260:]   # the window anything uses
            if not (np.isfinite(a).all() and np.isfinite(b).all()):
                d = float("inf")
            else:
                d = float(np.abs(a - b).max())
            worst = max(worst, d); checks.append((pname, bname, gross, cad, d))
    return worst, checks

# ==================================================================== (B) the control grid
def build_grid(panels):
    rows = []
    for pname, px in panels.items():
        win = windows(px.index)
        win["OOSH1"], win["OOSH2"] = None, None
        oos = px.index[(px.index >= pd.Timestamp(OOS_START))]
        oh = len(oos) // 2
        win["OOSH1"] = (oos[0], oos[oh - 1]); win["OOSH2"] = (oos[oh], oos[-1])

        spy_r = px["SPY"].pct_change().fillna(0.0)
        spy = wmetrics(spy_r, win)
        base_r, _ = fast_backtest(px, rules_v2_weights(px), rebalance_mask(px.index, "W").to_numpy())
        base = wmetrics(base_r, win)

        for bname, bfn in BOOKS.items():
            for gross in GROSSES:
                w = bfn(px, gross)
                for cad, P in N_PHASES.items():
                    for p in range(P):
                        r, t = fast_backtest(px, w, phase_mask(px.index, cad, p))
                        m = wmetrics(r, win)
                        l4b, l4bo, l4a = legs_4b(m, spy), legs_4b_oos(m, spy), legs_4a(m, base)
                        yrs = len(r.loc[win["FULL"][0]:]) / 252
                        rows.append(dict(
                            panel=pname, book=bname, gross=gross, cadence=cad, phase=p,
                            cost_bps=COST_BPS,
                            CAGR=m["FULL"][0], Sharpe=m["FULL"][1], MaxDD=m["FULL"][2],
                            H1=m["H1"][1], H2=m["H2"][1],
                            IS_CAGR=m["IS"][0], IS_Sharpe=m["IS"][1], IS_MaxDD=m["IS"][2],
                            OOS_CAGR=m["OOS"][0], OOS_Sharpe=m["OOS"][1], OOS_MaxDD=m["OOS"][2],
                            OOS_H1=m["OOSH1"][1], OOS_H2=m["OOSH2"][1],
                            turn_per_yr=float(t.loc[win["FULL"][0]:].sum()) / yrs,
                            spy_CAGR=spy["FULL"][0], spy_Sharpe=spy["FULL"][1], spy_MaxDD=spy["FULL"][2],
                            spy_H1=spy["H1"][1], spy_H2=spy["H2"][1],
                            spy_OOS_CAGR=spy["OOS"][0], spy_OOS_Sharpe=spy["OOS"][1],
                            spy_OOS_MaxDD=spy["OOS"][2],
                            base_Sharpe=base["FULL"][1], base_H1=base["H1"][1], base_H2=base["H2"][1],
                            base_MaxDD=base["FULL"][2],
                            base_OOS_CAGR=base["OOS"][0], base_OOS_Sharpe=base["OOS"][1],
                            base_OOS_MaxDD=base["OOS"][2],
                            IS_legs_passed=int(sum(legs_4b(m, spy).values())),
                            **l4b, pass4b=all(l4b.values()),
                            **{f"O{k}": v for k, v in l4bo.items()}, pass4b_OOSPURE=all(l4bo.values()),
                            **l4a, pass4a=all(l4a.values())))
        print(f"  grid: {pname} done ({len(rows)} rows)", flush=True)
    return pd.DataFrame(rows)

# ==================================================================== rule 8
CHOOSERS = {
    "C_ISSHARPE": lambda d: d.sort_values(["IS_Sharpe", "phase"], ascending=[False, True]).index[0],
    "C_ISCAGR":   lambda d: d.sort_values(["IS_CAGR", "phase"], ascending=[False, True]).index[0],
    "C_ISCALMAR": lambda d: d.assign(_k=d.IS_CAGR / d.IS_MaxDD.abs().clip(lower=1e-9))
                             .sort_values(["_k", "phase"], ascending=[False, True]).index[0],
}

def rule8(grid):
    """Phase chosen on 2009-2016 ALONE, 2017-2026 read ONCE.  The comparand is the family's
    own BLIND base rate: the share of that same family's phases that pass 4b out of sample."""
    out = []
    keys = ["panel", "book", "gross", "cadence"]
    for k, fam in grid.groupby(keys):
        blind_4b = fam.pass4b_OOSPURE.mean()
        blind_4a = fam.pass4a.mean()
        for cname, cfn in CHOOSERS.items():
            i = cfn(fam)
            r = fam.loc[i]
            out.append(dict(zip(keys, k)) | dict(
                chooser=cname, phase=int(r.phase), n_phases=len(fam),
                blind_4b_OOS=blind_4b, blind_4a=blind_4a,
                OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                base_OOS_CAGR=r.base_OOS_CAGR, base_OOS_Sharpe=r.base_OOS_Sharpe,
                pass4b_OOS=bool(r.pass4b_OOSPURE), pass4b_FULL=bool(r.pass4b),
                pass4a=bool(r.pass4a)))
    return pd.DataFrame(out)

# ==================================================================== (A) the record census
PASSCOLS = ["pass4b", "pass4b_REC", "pass4b_OOSPURE", "keep4b"]
PHASECOLS = ["phase"]
KEYCOLS = ["panel", "book", "gross", "cadence", "cost_bps", "cost", "arm", "n", "k", "band",
           "lam", "est", "estimator", "chooser", "corpus", "unit", "cell", "claim_set", "freq",
           "rung", "grid", "split", "scheme", "universe", "cadence_label"]
SELF = f"{TODAY}_{SLUG}_cloud"

def census():
    files = sorted(OUT.glob("*.csv"))
    rows, skipped_self, scanned = [], 0, 0
    for f in files:
        if SELF in f.name:
            skipped_self += 1; continue
        try:
            head = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception:
            continue
        ph = [c for c in PHASECOLS if c in head]
        pc = [c for c in PASSCOLS if c in head]
        if not ph or not pc:
            continue
        scanned += 1
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        keys = [c for c in KEYCOLS if c in df.columns and c not in ph]
        if not keys:
            keys = ["__all__"]; df["__all__"] = 0
        for passcol in pc:
            d = df[keys + ph + [passcol]].copy()
            d[passcol] = d[passcol].map(lambda v: str(v).strip().lower() in
                                        ("true", "1", "1.0", "yes", "y", "t"))
            for fk, fam in d.groupby(keys, dropna=False):
                nph = fam[ph[0]].nunique()
                if nph < 2:
                    continue
                base = fam[passcol].mean()
                npass = int(fam[passcol].sum())
                if npass == 0:
                    continue
                cad = None
                if "cadence" in keys:
                    cad = str(dict(zip(keys, fk if isinstance(fk, tuple) else (fk,))).get("cadence"))
                rows.append(dict(file=f.name, passcol=passcol, n_phases=nph,
                                 n_pass=npass, base_rate=base, cadence=cad,
                                 family=str(fk)[:120]))
    return pd.DataFrame(rows), scanned, len(files)

def census_claimsets(cen, grid):
    """The two tuned dials: CLAIM SET x CADENCE.  Every level printed, none chosen."""
    out = []
    gfam = (grid.groupby(["panel", "book", "gross", "cadence"])
                .agg(n_phases=("phase", "nunique"), n_pass=("pass4b", "sum"),
                     base_rate=("pass4b", "mean")).reset_index())
    gfam["cadence"] = gfam["cadence"].astype(str)
    gfam = gfam[gfam.n_pass > 0]

    sets = {"WIDE": cen[cen.n_phases >= 5],
            "STRICT": cen[cen.n_phases >= 21],
            "GRID": gfam}
    for sname, d in sets.items():
        for cad in ["M", "Q", "pooled"]:
            dd = d if cad == "pooled" else d[d.cadence.astype(str).str.upper().str.startswith(cad)]
            if len(dd) == 0:
                out.append(dict(claim_set=sname, cadence=cad, n_families=0, n_pass_rows=0,
                                median_base=np.nan, share_pass_on_hot_family=np.nan,
                                share_surviving=np.nan)); continue
            # one row per committed PASS, weighted by how many passes each family carries
            w = dd.n_pass.to_numpy(float)
            br = dd.base_rate.to_numpy(float)
            order = np.argsort(br); cw = np.cumsum(w[order]) / w.sum()
            med = float(br[order][np.searchsorted(cw, 0.5)])
            hot = float(w[br >= BAR_NONCERT].sum() / w.sum())
            out.append(dict(claim_set=sname, cadence=cad, n_families=len(dd),
                            n_pass_rows=int(w.sum()), median_base=med,
                            share_pass_on_hot_family=hot, share_surviving=1.0 - hot))
    return pd.DataFrame(out)

# ==================================================================== main
def main():
    print("=" * 100)
    print(f"IDEA 974  {SLUG}   (cloud lane, {TODAY})")
    print("Pre-registered bars: NONCERT median base >= %.2f | SURV share surviving >= %.2f | "
          "LIFT >= %.2fx | RULE8 >= %d" % (BAR_NONCERT, BAR_SURV, BAR_LIFT, BAR_RULE8))
    print("=" * 100)

    panels, n_dropped = load_panels()
    for k, v in panels.items():
        print(f"  panel {k:6s}: {v.shape[1]-1} names + SPY, {v.index[0].date()} -> {v.index[-1].date()}")
    print(f"  SMALL: dropped {n_dropped} tickers with max_1d_move >= 1.0 per data/small_meta.csv")

    print("\n--- GATE G1: fast core vs committed engine ---")
    worst, checks = gate_g1(panels)
    for c in checks:
        print(f"    {c[0]:6s} {c[1]:7s} g{c[2]:.2f} {c[3]}  max|diff| = {c[4]:.3e}")
    g1 = worst < 1e-12
    print(f"  G1 {'PASS' if g1 else 'FAIL'}  (worst {worst:.3e})")

    print("\n--- (B) control grid ---")
    grid = build_grid(panels)
    grid.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.grid.csv", index=False)
    print(f"  {len(grid)} rows -> {TODAY}_{SLUG}_cloud.grid.csv")
    print(f"  full-sample 4b passes at 10 bps: {int(grid.pass4b.sum())} of {len(grid)}"
          f"   |  4a: {int(grid.pass4a.sum())} of {len(grid)}")
    print("  binding legs over the whole grid (share FAILING):")
    for leg in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
        print(f"    {leg:7s} fail {1 - grid[leg].mean():.3f}")

    print("\n  per-family blind 4b base rate (control grid, full-sample 4b):")
    fam = (grid.groupby(["panel", "book", "gross", "cadence"])
               .agg(base=("pass4b", "mean"), base_oos=("pass4b_OOSPURE", "mean")).reset_index())
    print(fam.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    fam.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.families.csv", index=False)

    print("\n--- (A) record census ---")
    cen, scanned, nfiles = census()
    cen.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.census.csv", index=False)
    print(f"  {nfiles} committed csv artifacts scanned; {scanned} carry BOTH a phase column and "
          f"a 4b-pass column; {len(cen)} phase families carrying >= 1 committed PASS; "
          f"{int(cen.n_pass.sum()) if len(cen) else 0} committed phase-conditional 4b PASS rows.")
    tab = census_claimsets(cen, grid)
    tab.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.claimsets.csv", index=False)
    print(tab.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    pooled = tab[(tab.claim_set == "WIDE") & (tab.cadence == "pooled")]
    med = float(pooled.median_base.iloc[0]) if len(pooled) and pooled.n_pass_rows.iloc[0] else np.nan
    surv = float(pooled.share_surviving.iloc[0]) if len(pooled) and pooled.n_pass_rows.iloc[0] else np.nan

    print("\n--- RULE 8: phase chosen on 2009-2016 alone, 2017-2026 read once ---")
    r8 = rule8(grid)
    r8.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.rule8.csv", index=False)
    chosen_rate = r8.pass4b_OOS.mean()
    blind_rate = r8.blind_4b_OOS.mean()
    lift = chosen_rate / blind_rate if blind_rate > 0 else np.inf if chosen_rate > 0 else np.nan
    print(f"  {len(r8)} picks (3 choosers x {len(fam)} families).")
    print(f"  OOS 4b: CHOSEN {int(r8.pass4b_OOS.sum())} of {len(r8)} ({chosen_rate:.3f})"
          f"  vs BLIND within-family base rate {blind_rate:.3f}   lift {lift:.2f}x")
    print(f"  OOS 4a: {int(r8.pass4a.sum())} of {len(r8)}  vs blind {r8.blind_4a.mean():.3f}")
    if r8.pass4b_OOS.any():
        print("  the OOS 4b passes:")
        cols = ["panel", "book", "gross", "cadence", "chooser", "phase", "blind_4b_OOS",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "spy_OOS_Sharpe"]
        print(r8[r8.pass4b_OOS][cols].to_string(index=False,
                                                float_format=lambda x: f"{x:.3f}"))
    best = r8.sort_values("OOS_Sharpe", ascending=False).head(3)
    print("  best 3 picks by OOS Sharpe (whether or not they pass):")
    print(best[["panel", "book", "gross", "cadence", "chooser", "phase", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "pass4b_OOS"]].to_string(
                    index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 100)
    h_noncert = (med >= BAR_NONCERT) if med == med else False
    h_surv = (surv >= BAR_SURV) if surv == surv else False
    h_lift = (lift >= BAR_LIFT) if lift == lift and np.isfinite(lift) else False
    h_r8 = int(r8.pass4b_OOS.sum()) >= BAR_RULE8
    for nm, ok, val, bar in [("H_NONCERT", h_noncert, med, BAR_NONCERT),
                             ("H_SURV", h_surv, surv, BAR_SURV),
                             ("H_LIFT", h_lift, lift, BAR_LIFT),
                             ("H_RULE8", h_r8, r8.pass4b_OOS.sum(), BAR_RULE8)]:
        print(f"  {nm:10s} {'PASS' if ok else 'FAIL'}   value {val:.3f}   bar {bar}")
    print(f"  GATE G1 {'PASS' if g1 else 'FAIL'}")
    print("=" * 100)

    summary = dict(gate_g1=bool(g1), g1_worst=worst, grid_rows=len(grid),
                   grid_pass4b=int(grid.pass4b.sum()), grid_pass4a=int(grid.pass4a.sum()),
                   census_files_scanned=scanned, census_families=len(cen),
                   census_pass_rows=int(cen.n_pass.sum()) if len(cen) else 0,
                   median_base=med, share_surviving=surv,
                   rule8_chosen=float(chosen_rate), rule8_blind=float(blind_rate),
                   rule8_lift=float(lift) if np.isfinite(lift) else None,
                   rule8_pass4b=int(r8.pass4b_OOS.sum()), rule8_pass4a=int(r8.pass4a.sum()),
                   H_NONCERT=bool(h_noncert), H_SURV=bool(h_surv), H_LIFT=bool(h_lift),
                   H_RULE8=bool(h_r8))
    (OUT / f"{TODAY}_{SLUG}_cloud.summary.json").write_text(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    main()
