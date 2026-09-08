#!/usr/bin/env python3
"""Idea 443 — a-within-cell-DIFFERENCE-curve-may-not-carry-a-published-sign-threshold (lane C).

Idea 440 showed idea 168c's "k crossing" is a reader floor: y = f(x) - f(x0) is identically 0
at x0 with zero variance, `crossing_of` needs a STRICTLY positive value, so the smallest number
the reader can emit is the next grid point above x0.  That is a property of the CONSTRUCTION,
not of 168c.  This run asks how much of the record is built the same way.

Scope (the record's own, not re-invented):
  (i)  the 10 items of idea 439's committed ITEMS registry, each with its declared x / y / cells,
       imported from that script rather than retyped;
  (ii) a mechanical sweep of EVERY committed research/backtests/*curve*.csv over all (x, y)
       column pairs, so difference columns that were never registered are caught too.

The pinning test needs no knowledge of the cell structure: if y = f(x) - f(x0) within cell then
y == 0 at x = x0 in EVERY row whatever the cells are.  So the test is "is there an x level at
which y is identically zero, while y has real spread elsewhere".

TUNED PARAMETERS — exactly two, all grid points reported:
  P1  control-detection rule  in {STRICT, MAJORITY, SDZERO}
  P2  tolerance               in {0, 1e-12, 1e-9, 1e-6, 1e-3}
Headline cell: STRICT x 1e-12 (a machine-zero pin, the definitional case).

Rule 8 (part E): the band-width dial is one of the pinned curves (x0 = 0 = the bare 200d gate),
and it is also a LIVE dial — RULES v2's adopted 3% band.  126 fresh books (3 panels x 3 gross
x 2 cadence x 7 bands, 10 bps, weekly/monthly, t+1); the reading is taken on IS <= 2016-12-31
only and 2017-2026 is read once.  Arms: the reader floor, the plateau/argmax, the control point,
the live constant, and the per-cell IS argmax.  Both KEEP paths evaluated for every arm.

Outputs: .console.txt, .census.csv, .sensitivity.csv, .pinned.csv, .bookgrid.csv,
         .walkforward.csv, .keeppaths.csv, .result.md
Nothing outside research/ is touched; RULES.md, scan.py, bot.py, baseline.py untouched.
"""
from __future__ import annotations
import sys, importlib.util
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest  # noqa

BT = ROOT / "research" / "backtests"
STEM = "2026-09-08_a-within-cell-DIFFERENCE-curve-may-not-carry-a-published-sign-threshold_C"
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------- import idea 439's committed frame
_SRC = BT / "2026-09-08_census-every-CROSSING-in-the-record-for-dial-heterogeneity_C.py"
_spec = importlib.util.spec_from_file_location("idea439", _SRC)
C439 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C439)              # module level only; its main() is behind __main__

ITEMS = C439.ITEMS
load_item, local_curve, crossing_of = C439.load_item, C439.local_curve, C439.crossing_of
argmax_of, make_grid = C439.argmax_of, C439.make_grid
fast_backtest, band_book, csd = C439.fast_backtest, C439.band_book, C439.csd
COST_BPS, IS_END, OOS_START = C439.COST_BPS, C439.IS_END, C439.OOS_START
BANDS, GROSSES, CADENCES = C439.BANDS, C439.GROSSES, C439.CADENCES
HM_HEADLINE = C439.HM_HEADLINE

RULES = ["STRICT", "MAJORITY", "SDZERO"]                     # TUNED PARAMETER 1
TOLS = [0.0, 1e-12, 1e-9, 1e-6, 1e-3]                        # TUNED PARAMETER 2
RULE_H, TOL_H = "STRICT", 1e-12                              # headline cell
MAJ_FRAC = 0.95
B_BOOT = 2000
RNG = np.random.default_rng(443)

# The location each source run PUBLISHES for its curve (idea 439's ITEMS `published` field is the
# record's own wording; the number, where there is one, is idea 441's committed PROV).
PUB = {"219": 0.425, "167": np.nan, "159B": np.nan, "159c": 0.85, "168B": np.nan,
       "168c": np.nan, "103": np.nan, "61": np.nan, "277": np.nan, "bandgate": np.nan}


# =================================================================================== the pin test
def pin_levels(x, y, rule, tol):
    """Levels x0 of the x-axis at which y is a control zero under `rule` at `tol`.

    STRICT   : every row at x0 has |y| <= tol           (the definitional f(x) - f(x0) case)
    MAJORITY : >= MAJ_FRAC of rows at x0 have |y| <= tol (survives a handful of dirty cells)
    SDZERO   : sd(y at x0) <= tol                       (also catches a constant non-zero offset)
    In every rule the curve must have real spread overall, else the whole column is degenerate.
    """
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 6:
        return []
    if not (np.nanstd(y) > max(10 * tol, 1e-15)):
        return []
    out = []
    for lv in np.unique(x):
        yy = y[x == lv]
        if len(yy) < 2:
            continue
        if rule == "STRICT":
            hit = np.max(np.abs(yy)) <= tol
        elif rule == "MAJORITY":
            hit = (np.abs(yy) <= tol).mean() >= MAJ_FRAC
        else:
            hit = np.std(yy) <= tol
        if hit:
            out.append(float(lv))
    return out


def exact_curve(x, y):
    """Per-x means with no window at all (idea 440's exact reading)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    return [(float(lv), int((x == lv).sum()), float(y[x == lv].mean())) for lv in np.unique(x)]


def neighbours(grid, x0):
    g = np.asarray(sorted(grid), float)
    up = g[g > x0]; dn = g[g < x0]
    return (float(up[0]) if len(up) else np.nan), (float(dn[-1]) if len(dn) else np.nan)


def numeric_cols(d):
    out = []
    for c in d.columns:
        v = pd.to_numeric(d[c], errors="coerce")
        if v.notna().sum() >= 6:
            out.append((c, v.values))
    return out


# ============================================================================ PART A — repro gate
def part_a():
    P("=" * 116)
    P("PART A - REPRODUCTION GATE (nothing new is read before these match)")
    P("=" * 116)
    rows = []

    # A1: idea 439's ITEMS load and its headline crossing readings
    for it in ITEMS:
        d, keys = load_item(it)
        grid = it.get("grid", make_grid(d["__x__"].values))
        step = float(np.median(np.diff(np.unique(np.asarray(grid, float))))) if len(grid) > 1 else np.nan
        loc = local_curve(d["__x__"].values, d["__y__"].values, grid, HM_HEADLINE * step)
        ch, below = crossing_of(loc)
        rows.append(dict(item=it["id"], rows=len(d), cells_keys="|".join(keys),
                         crossing_hm3=ch, last_nonpos=below))
        P(f"  {it['id']:9s} rows {len(d):5d}  x={it['x']:12s}  crossing@hm3 "
          f"{ch if np.isfinite(ch) else float('nan'):>8.4f}  last non-pos "
          f"{below if np.isfinite(below) else float('nan'):>8.4f}")
    g1 = [r for r in rows if r["item"] == "219"][0]
    P(f"\n  GATE idea 219 crossing published 0.425 / last non-positive 0.400 -> "
      f"{g1['crossing_hm3']:.4f} / {g1['last_nonpos']:.4f}  "
      f"{'MATCH' if abs(g1['crossing_hm3'] - 0.425) < 1e-9 and abs(g1['last_nonpos'] - 0.400) < 1e-9 else 'MISMATCH'}")

    # A2: idea 440's exact per-k table for 168c, reproduced off the committed curve
    it = [i for i in ITEMS if i["id"] == "168c"][0]
    d, _ = load_item(it)
    ex = exact_curve(d["__x__"].values, d["__y__"].values)
    P("\n  GATE idea 440's EXACT per-k means on 168c's committed curve (published in its result.md):")
    pub440 = {-1.0: -0.35419, -0.5: -0.20276, 0.0: 0.0, 0.10: 0.04596, 1.0: 0.06066}
    worst = 0.0
    for k, n, m in ex:
        tag = ""
        if round(k, 4) in pub440:
            dd = abs(m - pub440[round(k, 4)]); worst = max(worst, dd)
            tag = f"   published {pub440[round(k,4)]:+.5f}  diff {dd:.2e}"
        P(f"     k {k:+.2f}  n {n:3d}  mean dSharpe {m:+.5f}{tag}")
    P(f"  GATE max |diff| vs idea 440's published exact means: {worst:.2e}  "
      f"{'MATCH' if worst < 1e-4 else 'MISMATCH'}")
    ch_ex, below_ex = crossing_of(ex)
    P(f"  GATE 168c EXACT crossing {ch_ex:+.2f} (idea 440 published +0.10), last non-positive "
      f"{below_ex:+.2f} (published 0.00)  "
      f"{'MATCH' if abs(ch_ex - 0.10) < 1e-9 and abs(below_ex) < 1e-9 else 'MISMATCH'}")

    # A3: fast_backtest vs engine.backtest
    px = load_universe()
    W = rules_v2_weights(px)
    a = engine_backtest(px, W, cost_bps=COST_BPS, freq="W")["returns"]
    b = fast_backtest(px, W, COST_BPS, "W")
    dmax = float(np.abs(a - b).max())
    P(f"\n  GATE fast_backtest vs engine.backtest, RULES v2 / U56 @10 bps: max |diff| {dmax:.3e}  "
      f"{'MATCH' if dmax < 1e-12 else 'MISMATCH'}")
    assert dmax < 1e-12
    return pd.DataFrame(rows), px


# ============================================================ PART B — the census over the corpus
def part_b():
    P("\n" + "=" * 116)
    P("PART B - THE CENSUS.  Which committed curves are WITHIN-CELL DIFFERENCES against a")
    P("control level of their OWN x-axis?  Test: is there an x level at which y is identically")
    P("zero (y = f(x) - f(x0) forces exactly that), while y has real spread elsewhere?")
    P("=" * 116)

    files = sorted(p.name for p in BT.glob("*curve*.csv"))
    P(f"  committed *curve*.csv in research/backtests: {len(files)}")
    for f in files:
        P(f"     {f}")

    # ---- B1: the 10 REGISTERED items (x and y declared by idea 439, not chosen here)
    P("\n  B1 - the 10 registered items of idea 439's ITEMS (x / y as that run declared them)")
    reg = []
    for it in ITEMS:
        d, keys = load_item(it)
        x, y = d["__x__"].values, d["__y__"].values
        grid = sorted(np.unique(x[np.isfinite(x)]))
        pins = pin_levels(x, y, RULE_H, TOL_H)
        ex = exact_curve(x, y)
        ch, below = crossing_of(ex)
        up, dn = (neighbours(grid, pins[0]) if pins else (np.nan, np.nan))
        floor = bool(pins) and np.isfinite(ch) and np.isfinite(up) and abs(ch - up) < 1e-12
        reg.append(dict(scope="REGISTERED", item=it["id"], file=it["file"], x=it["x"],
                        y=str(it["y"]), rows=len(d), levels=len(grid),
                        pinned=bool(pins), x0=(pins[0] if pins else np.nan),
                        n_pins=len(pins), next_up=up, next_dn=dn,
                        exact_crossing=ch, last_nonpos=below, reader_floor=floor,
                        published=PUB.get(it["id"], np.nan), kind=it["kind"]))
        P(f"     {it['id']:9s} {'PINNED at x0=' + format(pins[0], '.4g') if pins else 'not pinned':<22s}"
          f"  exact crossing {ch:>8.4f}" if np.isfinite(ch) else
          f"     {it['id']:9s} {'PINNED at x0=' + format(pins[0], '.4g') if pins else 'not pinned':<22s}"
          f"  exact crossing     none")
        if pins:
            P(f"                 next grid point above x0 = {up:.4g}; reader floor? "
              f"{'YES' if floor else 'no'}")

    # ---- B2: mechanical sweep of every (x, y) pair in every committed curve file
    P("\n  B2 - mechanical sweep: EVERY (x, y) numeric column pair in EVERY committed curve file")
    mech = []
    for f in files:
        try:
            d = pd.read_csv(BT / f)
        except Exception as e:
            P(f"     {f}: unreadable ({e})"); continue
        cols = numeric_cols(d)
        for xc, xv in cols:
            lv = np.unique(xv[np.isfinite(xv)])
            if not (3 <= len(lv) <= 60):
                continue
            if min((xv == l).sum() for l in lv) < 2:
                continue
            for yc, yv in cols:
                if yc == xc:
                    continue
                pins = pin_levels(xv, yv, RULE_H, TOL_H)
                if not pins:
                    continue
                ex = exact_curve(xv, yv)
                ch, below = crossing_of(ex)
                up, dn = neighbours(lv, pins[0])
                mech.append(dict(scope="SWEEP", item="", file=f, x=xc, y=yc, rows=len(d),
                                 levels=len(lv), pinned=True, x0=pins[0], n_pins=len(pins),
                                 next_up=up, next_dn=dn, exact_crossing=ch, last_nonpos=below,
                                 reader_floor=bool(np.isfinite(ch) and np.isfinite(up)
                                                   and abs(ch - up) < 1e-12),
                                 published=np.nan, kind=""))
    P(f"     pairs pinned under the headline cell ({RULE_H}, tol {TOL_H:g}): {len(mech)}"
      f"  in {len(set(m['file'] for m in mech))} files")
    for m in sorted(mech, key=lambda r: (r["file"], r["x"], r["y"])):
        P(f"     {m['file'][:62]:62s} x={m['x'][:14]:14s} y={m['y'][:16]:16s} x0={m['x0']:.4g}"
          f"  crossing {m['exact_crossing'] if np.isfinite(m['exact_crossing']) else float('nan'):>8.4f}"
          f"  floor={'YES' if m['reader_floor'] else 'no'}")

    census = pd.DataFrame(reg + mech)

    # ---- B3: the P1 x P2 sensitivity, ALL grid points
    P("\n  B3 - SENSITIVITY, all 3 x 5 grid points (count of pinned (file, x, y) pairs)")
    sens = []
    for rule in RULES:
        for tol in TOLS:
            n_reg = 0
            for it in ITEMS:
                d, _ = load_item(it)
                if pin_levels(d["__x__"].values, d["__y__"].values, rule, tol):
                    n_reg += 1
            n_sw, fset = 0, set()
            for f in files:
                try:
                    d = pd.read_csv(BT / f)
                except Exception:
                    continue
                cols = numeric_cols(d)
                for xc, xv in cols:
                    lv = np.unique(xv[np.isfinite(xv)])
                    if not (3 <= len(lv) <= 60):
                        continue
                    if min((xv == l).sum() for l in lv) < 2:
                        continue
                    for yc, yv in cols:
                        if yc != xc and pin_levels(xv, yv, rule, tol):
                            n_sw += 1; fset.add(f)
            sens.append(dict(rule=rule, tol=tol, registered_pinned=n_reg,
                             sweep_pairs=n_sw, sweep_files=len(fset)))
            P(f"     P1={rule:8s} P2={tol:<8g}  registered {n_reg:2d}/10   sweep pairs {n_sw:4d}"
              f"   sweep files {len(fset):2d}")
    return census, pd.DataFrame(sens), files


# =========================================== PART C — what each pinned curve may publish instead
def part_c(census):
    P("\n" + "=" * 116)
    P("PART C - FOR EVERY PINNED CURVE: is the published location a READER FLOOR, and what")
    P("MAGNITUDE could be published in its place?  Bootstrap B=%d over rows." % B_BOOT)
    P("=" * 116)
    rows = []
    pin = census[census.pinned].copy()
    seen = set()
    for _, r in pin.iterrows():
        key = (r["file"], r["x"], r["y"])
        if key in seen:
            continue
        seen.add(key)
        hit = [i for i in ITEMS if i["id"] == str(r["item"])]
        if hit:
            d = load_item(hit[0])[0]
            x, y = d["__x__"].values, d["__y__"].values
        else:
            d = pd.read_csv(BT / r["file"])
            x = pd.to_numeric(d[r["x"]], errors="coerce").values
            y = pd.to_numeric(d[r["y"]], errors="coerce").values
        ok = np.isfinite(x) & np.isfinite(y)
        x, y = x[ok], y[ok]
        lv = np.unique(x)
        up = r["next_up"]
        xmax = float(lv.max())
        m_up = float(y[x == up].mean()) if np.isfinite(up) else np.nan
        m_max = float(y[x == xmax].mean())
        # positive arm: everything strictly above x0
        arm = lv[lv > r["x0"]]
        # slope over the positive arm (OLS on per-x means)
        if len(arm) >= 3:
            mu = np.array([y[x == a].mean() for a in arm])
            slope = float(np.polyfit(arm, mu, 1)[0])
        else:
            slope = np.nan
        # bootstrap: resample rows, recompute the exact reading
        chs, plateau = [], []
        n = len(x)
        for _ in range(B_BOOT):
            idx = RNG.integers(0, n, n)
            xb, yb = x[idx], y[idx]
            ex = exact_curve(xb, yb)
            c, _b = crossing_of(ex)
            chs.append(c)
            mu_up = yb[xb == up].mean() if np.isfinite(up) and (xb == up).any() else np.nan
            mu_mx = yb[xb == xmax].mean() if (xb == xmax).any() else np.nan
            plateau.append(mu_mx - mu_up)
        chs = np.array(chs, float); plateau = np.array(plateau, float)
        p_floor = float(np.mean(np.isfinite(chs) & np.isfinite(up) & (np.abs(chs - up) < 1e-12)))
        lo, hi = (np.nanpercentile(plateau, 2.5), np.nanpercentile(plateau, 97.5))
        sep = bool(np.isfinite(lo) and np.isfinite(hi) and (lo > 0 or hi < 0))
        rows.append(dict(item=r["item"], file=r["file"], x=r["x"], y=r["y"], x0=r["x0"], next_up=up,
                         exact_crossing=r["exact_crossing"], reader_floor=r["reader_floor"],
                         P_crossing_eq_floor=p_floor,
                         level_at_floor=m_up, plateau_level=m_max, arm_slope=slope,
                         plateau_minus_floor=m_max - m_up, ci_lo=lo, ci_hi=hi,
                         plateau_separable=sep, published=r["published"]))
        P(f"  {(str(r['item']) or '-'):9s} {r['file'][:52]:52s} x={r['x'][:12]:12s} y={r['y'][:14]:14s}")
        P(f"            x0={r['x0']:.4g}  next grid point up={up if np.isfinite(up) else float('nan'):.4g}"
          f"  exact crossing={r['exact_crossing'] if np.isfinite(r['exact_crossing']) else float('nan'):.4g}"
          f"  READER FLOOR={'YES' if r['reader_floor'] else 'no'}  P(=floor)={p_floor:.3f}")
        P(f"            magnitudes instead: level at floor {m_up:+.5f}, plateau (x max) "
          f"{m_max:+.5f}, arm slope {slope:+.5f}, plateau-floor {m_max - m_up:+.5f} "
          f"95% CI [{lo:+.5f}, {hi:+.5f}] separable={'YES' if sep else 'NO'}")
    # ---- C2: the ENDPOINT pin is a different failure mode from the CONTROL pin
    P("\n  C2 - an ENDPOINT pin (x0 at the top of the axis, nothing above it) cannot floor a")
    P("  crossing, but it does deflate everything a window reaching it would report.")
    it = [i for i in ITEMS if i["id"] == "219"][0]
    d, _ = load_item(it)
    grid = it["grid"]; step = float(np.median(np.diff(np.unique(np.asarray(grid, float)))))
    x, y = d["__x__"].values, d["__y__"].values
    loc = local_curve(x, y, grid, HM_HEADLINE * step)
    keep = x < 1.0
    loc2 = local_curve(x[keep], y[keep], grid, HM_HEADLINE * step)
    P(f"     idea 219: {int((x == 1.0).sum())} rows at share_mean = 1.0, every one exactly 0 "
      f"(a unanimous mode has nothing to differ from)")
    P(f"     crossing with the pinned endpoint {crossing_of(loc)}   without it {crossing_of(loc2)}"
      f"   -> the LOCATION is unmoved")
    P(f"     top centre (1.000) local mean with the pin {loc[-1][2]:+.6f}, without it "
      f"{loc2[-1][2]:+.6f}  -> the LEVEL is deflated {loc2[-1][2] / loc[-1][2]:.2f}x")
    return pd.DataFrame(rows)


# ================================================== PART E — rule 8 on live prices + KEEP paths
def part_e():
    P("\n" + "=" * 116)
    P("PART E - RULE 8, LIVE PRICES.  The band-width dial IS one of the pinned curves (x0 = 0")
    P("is the bare 200d gate) and it is also the record's only adopted constant (RULES v2's 3%).")
    P("126 books: 3 panels x 3 gross x 2 cadence x 7 band widths, 10 bps, t+1.  y = Sharpe(band)")
    P("- Sharpe(band=0) WITHIN cell.  Reading taken on IS <= %s only; %s-2026 read once." % (IS_END, OOS_START[:4]))
    P("=" * 116)
    panels = {}
    for lab, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL439", dict(small=True))]:
        px = load_universe(**kw)
        panels[lab] = px
        P(f"  {lab:10s} {px.shape[1]:4d} cols  {px.index[0].date()} -> {px.index[-1].date()}")

    rows = []
    rets = {}
    for lab, px in panels.items():
        st = px.index[260]
        for g in GROSSES:
            for cd in CADENCES:
                for bnd in BANDS:
                    r = fast_backtest(px, band_book(px, bnd, g), COST_BPS, cd).loc[st:]
                    rets[(lab, g, cd, bnd)] = r
                    ris = r.loc[:IS_END]; ros = r.loc[OOS_START:]
                    c, s, dd = csd(r); ci, si, di = csd(ris); co, so, do = csd(ros)
                    h = len(r) // 2
                    rows.append(dict(panel=lab, gross=g, cadence=cd, band=bnd,
                                     CAGR=c, Sharpe=s, MaxDD=dd,
                                     H1=csd(r.iloc[:h])[1], H2=csd(r.iloc[h:])[1],
                                     IS_Sharpe=si, OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=do))
    grid = pd.DataFrame(rows)
    P(f"\n  {len(grid)} books.")

    # the pinned IS curve: y = IS Sharpe(band) - IS Sharpe(band=0) within (panel, gross, cadence)
    base = grid[grid.band == 0].set_index(["panel", "gross", "cadence"])["IS_Sharpe"]
    grid["dIS"] = grid["IS_Sharpe"].values - base.loc[
        list(zip(grid.panel, grid.gross, grid.cadence))].values
    ex = exact_curve(grid["band"].values, grid["dIS"].values)
    P("\n  IS curve, exact per-band means over the 18 cells (no window):")
    for b, n, m in ex:
        P(f"     band {b:5.2f}  n {n:3d}  mean dIS_Sharpe {m:+.5f}  sd "
          f"{grid.loc[grid.band == b, 'dIS'].std():.5f}  >0 in "
          f"{int((grid.loc[grid.band == b,'dIS'] > 0).sum())}/{int((grid.band == b).sum())}")
    ch, below = crossing_of(ex)
    up, _dn = neighbours([b for b, _, _ in ex], 0.0)
    amax = argmax_of(ex)
    P(f"\n  EXACT crossing {ch if np.isfinite(ch) else float('nan')}  (next grid point above the "
      f"control x0=0 is {up})  -> READER FLOOR = {'YES' if np.isfinite(ch) and abs(ch - up) < 1e-12 else 'no'}")
    P(f"  EXACT argmax (the MAGNITUDE reading) {amax}; live adopted constant 0.03")

    arms = {"A_FLOOR (crossing)": (up if not np.isfinite(ch) else ch),
            "A_PLATEAU (argmax)": amax,
            "A_CTRL (band=0, the control point)": 0.0,
            "A_LIVE (RULES v2's 0.03)": 0.03}
    wf = []
    for name, bnd in arms.items():
        rr = [rets[(lab, g, cd, bnd)] for lab in panels for g in GROSSES for cd in CADENCES]
        pooled = pd.concat(rr, axis=1).mean(axis=1)
        wf.append(_wfrow(name, f"{bnd:.2f}", pooled))
    # per-cell IS argmax (the selection arm)
    picks, rr = [], []
    for (lab, g, cd), sub in grid.groupby(["panel", "gross", "cadence"]):
        b = float(sub.loc[sub.IS_Sharpe.idxmax(), "band"])
        picks.append(b); rr.append(rets[(lab, g, cd, b)])
    wf.append(_wfrow("A_IS (per-cell IS argmax)",
                     "/".join(sorted({f'{p:.2f}' for p in picks})), pd.concat(rr, axis=1).mean(axis=1)))
    # SPY and RULES v2, pooled the same way
    spy = pd.concat([panels[l]["SPY"].pct_change().fillna(0).loc[panels[l].index[260]:]
                     for l in panels], axis=1).mean(axis=1)
    wf.append(_wfrow("SPY (equal-weight of the 3 panels)", "-", spy))
    v2 = pd.concat([fast_backtest(panels[l], rules_v2_weights(panels[l]), COST_BPS, "W")
                    .loc[panels[l].index[260]:] for l in panels], axis=1).mean(axis=1)
    wf.append(_wfrow("RULES v2 (live) @10 bps", "-", v2))
    wfd = pd.DataFrame(wf)
    P("\n  " + wfd.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    # ---- KEEP paths
    s = wfd.set_index("arm")
    spy_r = s.loc["SPY (equal-weight of the 3 panels)"]
    v2_r = s.loc["RULES v2 (live) @10 bps"]
    kp = []
    for name in list(arms) + ["A_IS (per-cell IS argmax)"]:
        a = s.loc[name]
        f4a = bool(a.H1 > v2_r.H1 and a.H2 > v2_r.H2 and a.MaxDD >= v2_r.MaxDD)
        fails = []
        if not a.H1 > spy_r.H1: fails.append("H1")
        if not a.H2 > spy_r.H2: fails.append("H2")
        if not a.OOS_Sharpe > spy_r.OOS_Sharpe: fails.append("OOS")
        if not abs(a.MaxDD) <= 0.60 * abs(spy_r.MaxDD): fails.append("DD")
        if not a.CAGR >= 0.70 * spy_r.CAGR: fails.append("CAGR")
        kp.append(dict(arm=name, band=a.pick, pass4a=f4a, pass4b=not fails,
                       failing="|".join(fails) or "-",
                       CAGR=a.CAGR, Sharpe=a.Sharpe, MaxDD=a.MaxDD, H1=a.H1, H2=a.H2,
                       OOS_Sharpe=a.OOS_Sharpe, OOS_CAGR=a.OOS_CAGR, OOS_MaxDD=a.OOS_MaxDD))
    kpd = pd.DataFrame(kp)
    P("\n  KEEP paths (4b bars off the pooled SPY: H1>%.4f, H2>%.4f, OOS>%.4f, |MaxDD|<=%.4f, CAGR>=%.4f)"
      % (spy_r.H1, spy_r.H2, spy_r.OOS_Sharpe, 0.60 * abs(spy_r.MaxDD), 0.70 * spy_r.CAGR))
    P("  " + kpd.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    P(f"\n  4a passes: {int(kpd.pass4a.sum())}/{len(kpd)}   4b passes: {int(kpd.pass4b.sum())}/{len(kpd)}")
    return grid, wfd, kpd


def _wfrow(name, pick, r):
    c, s, dd = csd(r)
    h = len(r) // 2
    co, so, do = csd(r.loc[OOS_START:])
    return dict(arm=name, pick=pick, CAGR=c, Sharpe=s, MaxDD=dd,
                H1=csd(r.iloc[:h])[1], H2=csd(r.iloc[h:])[1],
                OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=do)


# ============================================================================================ main
def main():
    repro, _px = part_a()
    census, sens, files = part_b()
    pinned = part_c(census)
    grid, wfd, kpd = part_e()

    P("\n" + "=" * 116)
    P("PART D - PROPOSED PROTOCOL WORDING (drafted here, NOT written into PROTOCOL.md:")
    P("a protocol clause is a Sunday-review decision, rule 6)")
    P("=" * 116)
    for ln in PROTOCOL_DRAFT.strip().split("\n"):
        P("  " + ln)

    census.to_csv(BT / f"{STEM}.census.csv", index=False)
    sens.to_csv(BT / f"{STEM}.sensitivity.csv", index=False)
    pinned.to_csv(BT / f"{STEM}.pinned.csv", index=False)
    repro.to_csv(BT / f"{STEM}.repro.csv", index=False)
    grid.to_csv(BT / f"{STEM}.bookgrid.csv", index=False)
    wfd.to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    kpd.to_csv(BT / f"{STEM}.keeppaths.csv", index=False)
    (BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nWrote {STEM}.{{census,sensitivity,pinned,repro,bookgrid,walkforward,keeppaths}}.csv "
      f"and .console.txt")
    (BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


PROTOCOL_DRAFT = """
10. **A within-cell difference curve may not carry a published sign threshold.**  When a curve's
    y is defined as `f(x) - f(x0)` within cell and `x0` is a level of the SAME x-axis, then
    `y(x0) = 0` identically, with zero variance, in every cell.  A sign reader (`crossing_of`
    and anything else that requires a strictly positive value) therefore cannot return `x0` or
    anything below it, and the smallest value it is capable of emitting is the next grid point
    above `x0`.  Such a curve MAY publish a magnitude - the level at a named x, the plateau
    level, the slope of an arm, a hinge location fitted with its knot charged as a parameter -
    but it MAY NOT publish the crossing as a location.  A run that reports a crossing on such a
    curve must publish, in the same table: (a) the control level `x0`; (b) the next grid point
    above it; and (c) `P(crossing = that grid point)` under the run's own bootstrap.  Where (c)
    is at or near 1.0, the reading is a reader floor and is not a measurement.
    Detection is mechanical and needs no knowledge of the cell structure: y is a within-cell
    difference against a level of its own x-axis iff there is an x level at which every row's
    |y| is at or below tolerance while y has spread elsewhere.
"""

if __name__ == "__main__":
    main()
