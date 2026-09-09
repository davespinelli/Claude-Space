#!/usr/bin/env python3
"""idea 458 (lane C) — why is the ungated full-gross control the IS argmax on broad136 and
SMALL439 but not on u56?

Idea 241's fresh live corpus (31 arms = 1 ungated full-gross control + 5 bands x 3 gross x 2
cadences of the RULES-v2-shaped gated book, on 3 panels x 2 cost rungs, 200 seeded sub-menus
per cell) is a strict no-op on two of three panels: the control wins IS Sharpe in 400 of 400
sub-menus on broad136 and on SMALL439, and in only ~23% on u56.  Every sub-menu chooser
experiment run on those two panels is therefore a constant, not a choice.

This script (a) reproduces that number from idea 241's own harness, (b) locates the panel
property that produces it, and (c) censuses the committed record for the same degeneracy.

Design.  broad136 is a strict SUPERSET of u56 (all 56 u56 tickers are in it), so "breadth"
and "composition" can be varied independently on ONE price source.  The two tuned dials are:

    k = number of the 12 non-equity names (TLT IEF SHY HYG LQD TIP GLD SLV USO UNG DBC UUP)
        in the panel   ->   phi = k / N, the non-equity share
    N = panel breadth

and nothing else is tuned: the gate band is held at the live 0.03 for every property, arms
span all 5 bands, costs are the protocol's 10 bps (25 bps reported), weights are decided at
t and applied at t+1 by engine.backtest.  ALL grid points are written to .grid.csv.

Windows follow idea 241: warm-up = index[260], IS = start..2016-12-31, OOS = 2017-01-01..end.

Outputs: .arms.csv .grid.csv .props.csv .separation.csv .walkforward.csv .keeppaths.csv
         .census.csv .console.txt
"""
from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_why-is-the-ungated-control-the-IS-argmax-on-broad136-and-SMALL439-but-not-u56_C"
OUT = ROOT / "research" / "backtests"

IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BAND_LIVE = 0.03
COST = 10.0                      # PROTOCOL rule 2
NONEQ = ["TLT", "IEF", "SHY", "HYG", "LQD", "TIP", "GLD", "SLV", "USO", "UNG", "DBC", "UUP"]

KS = [0, 2, 4, 6, 9, 12]         # dial 1: non-equity count
NS = [24, 56, 120]               # dial 2: breadth
SEEDS = [0, 1, 2]

LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


def load_harness():
    """Import idea 241's lane-B harness by path (main() is guarded; nothing runs on import)."""
    p = OUT / "2026-09-08_the-013-margin-rule_B.py"
    spec = importlib.util.spec_from_file_location("h241", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = load_harness()

# probe menu: the control plus the 10 (band x cadence) gated arms at gross 1.00.
PROBE_ARMS = [("control", dict(band=None, gross=1.0, freq="W", gated=False))] + [
    (f"b{b:g}-g1.00-{f}", dict(band=b, gross=1.0, freq=f, gated=True))
    for b in (0.0, 0.015, 0.03, 0.045, 0.06) for f in ("W", "M")]


# ------------------------------------------------------------------ small helpers
def win(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    return metrics(x) if len(x) >= 30 else {k: np.nan for k in ("CAGR", "Sharpe", "MaxDD")}


def auc(x, y) -> float:
    """Rank AUC of continuous x predicting boolean y (0.5 = no information)."""
    x = np.asarray(x, float)
    y = np.asarray(y, bool)
    ok = np.isfinite(x)
    x, y = x[ok], y[ok]
    if y.all() or (~y).all() or len(x) < 3:
        return np.nan
    r = pd.Series(x).rank().values
    n1, n0 = y.sum(), (~y).sum()
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def best_threshold(x, y):
    """Best single split accuracy for predicting boolean y from x; returns (acc, thr, sign)."""
    x = np.asarray(x, float)
    y = np.asarray(y, bool)
    ok = np.isfinite(x)
    x, y = x[ok], y[ok]
    best = (-1.0, np.nan, 0)
    for t in np.unique(x):
        for s in (+1, -1):
            pred = (x >= t) if s > 0 else (x < t)
            acc = float((pred == y).mean())
            if acc > best[0]:
                best = (acc, float(t), s)
    return best


def arm_returns(px_all, cols, arms=PROBE_ARMS, cost=COST):
    """Net return stream of every arm; weights on `cols` only, other columns are benchmarks."""
    start = px_all.index[260]
    out = {}
    for name, a in arms:
        w = H.ew_band_weights(px_all[cols], 0.0 if a["band"] is None else a["band"],
                              a["gross"], gated=a["gated"])
        w = w.reindex(columns=px_all.columns).fillna(0.0)
        res = backtest(px_all, w, cost_bps=0.0, freq=a["freq"])
        out[name] = (res["returns"] - res["turnover"] * cost / 1e4).loc[start:]
    return out


def panel_props(px_all, cols):
    """Panel properties, all computed on the IS window only (no OOS leakage)."""
    start = px_all.index[260]
    sub = px_all[cols]
    bs = band_state(sub, BAND_LIVE).loc[start:IS_END]
    px_is = sub.loc[start:IS_END]
    ret = px_is.pct_change()
    priced = px_is.notna()
    inband = float((bs & priced).values.sum() / priced.values.sum())
    r_out = ret.where(~bs & priced).stack().mean() * 252
    r_in = ret.where(bs & priced).stack().mean() * 252
    C = ret.corr().values
    iu = np.triu_indices(len(cols), 1)
    tot = px_is.ffill().iloc[-1] / px_is.bfill().iloc[0] - 1
    return dict(N=len(cols), phi=len(set(cols) & set(NONEQ)) / len(cols),
                inband=inband, r_in=float(r_in), r_out=float(r_out),
                avoided=float(r_in - r_out),
                disp=float(ret.std(axis=1).mean() * np.sqrt(252)),
                rho=float(np.nanmean(C[iu])),
                negdrift=float((tot < 0).mean()),
                ewvol=float(ret.mean(axis=1).std() * np.sqrt(252)))


def cell_read(px_all, cols, label, source):
    """One probe cell: IS/OOS Sharpe of control vs the best gated arm, plus panel properties.

    The price frame is narrowed to the cell's own columns (+ SPY, benchmark only): the engine
    prices every column it is handed, and the arms hold zero in the ones outside `cols`."""
    keep = list(dict.fromkeys(list(cols) + (["SPY"] if "SPY" in px_all.columns else [])))
    px_all = px_all[keep]
    R = arm_returns(px_all, cols)
    d = dict(cell=label, source=source, **panel_props(px_all, cols))
    S_is = {k: win(v, hi=IS_END)["Sharpe"] for k, v in R.items()}
    S_oos = {k: win(v, lo=OOS_START)["Sharpe"] for k, v in R.items()}
    gated = [k for k in R if k != "control"]
    d["IS_ctl"] = S_is["control"]
    d["IS_bestgated"] = max(S_is[k] for k in gated)
    d["IS_argmax"] = max(S_is, key=lambda k: S_is[k])
    d["D_is"] = d["IS_ctl"] - d["IS_bestgated"]
    d["ctl_wins_is"] = bool(d["D_is"] > 0)
    d["OOS_ctl"] = S_oos["control"]
    d["OOS_bestgated"] = max(S_oos[k] for k in gated)
    d["D_oos"] = d["OOS_ctl"] - d["OOS_bestgated"]
    d["ctl_wins_oos"] = bool(d["D_oos"] > 0)
    d["OOS_CAGR_ctl"] = win(R["control"], lo=OOS_START)["CAGR"]
    d["OOS_MaxDD_ctl"] = win(R["control"], lo=OOS_START)["MaxDD"]
    return d


# ------------------------------------------------------------------ G0: reproduce idea 241
def part_g0():
    say("## G0 — reproduce idea 241's live corpus (its own harness, imported not re-implemented)")
    panels = H.load_panels()
    for k, v in panels.items():
        say(f"  {k}: {v.shape[1]} columns, {v.index[0].date()}..{v.index[-1].date()}")
    fg, curves = H.fresh_grid(panels)
    menus = H.submenus([a for a, _ in H.arm_menu()])
    LC = H.live_cells(fg, menus, "IS_", "OOS_")
    say(f"  live cells (panel x cost x sub-menu): {len(LC)}  over {len(menus)} menus x 2 cost rungs")
    tab = LC.groupby("panel").agg(n=("star_is_ctl", "size"), ctl_wins=("star_is_ctl", "sum"))
    tab["rate"] = tab.ctl_wins / tab.n
    say(tab.to_string(float_format=lambda x: f"{x:.4f}"))
    pub = {"broad136": 1.00, "small439": 1.00, "u56": 0.23}
    ok = all(abs(tab.loc[p, "rate"] - v) <= 0.02 for p, v in pub.items() if p in tab.index)
    say(f"  GATE G0 (published 400/400, 400/400, 23%): {'PASS' if ok else 'FAIL'}")
    return fg, curves, LC


def part_r1(fg):
    """The panel-level fact under the sub-menus: the full 31-arm IS Sharpe ordering."""
    say("\n## R1 — the whole 31-arm menu, IS Sharpe (2009..2016), ALL grid points -> .arms.csv")
    rows = []
    for (p, c), sub in fg.groupby(["panel", "cost"]):
        s = sub.set_index("arm")["IS_Sharpe"]
        ctl = s["control"]
        g = s.drop("control")
        rows.append(dict(panel=p, cost=c, IS_ctl=ctl, IS_bestgated=g.max(),
                         best_gated_arm=g.idxmax(), D=ctl - g.max(),
                         ctl_rank=int((s > ctl).sum() + 1), n_arms=len(s),
                         n_gated_beaten=int((g < ctl).sum())))
    T = pd.DataFrame(rows)
    say(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  The sub-menu result is a panel-level fact: on broad136/small439 the control beats")
    say("  ALL 30 gated arms outright, so every sub-menu containing it is won by it.")
    # gross invariance of the gated arms' Sharpe (justifies the 11-arm probe menu at gross 1.00)
    sub = fg[(fg.cost == COST) & fg.gated]
    sp = sub.groupby(["panel", "band", "freq"])["IS_Sharpe"].agg(lambda x: x.max() - x.min())
    say(f"  gross-invariance of gated IS Sharpe (max-min over gross 0.50/0.75/1.00): "
        f"max {sp.max():.4f}, median {sp.median():.4f} — the probe menu fixes gross at 1.00")
    fg.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    return T


# ------------------------------------------------------------------ R2/R3: the (phi, N) grid
def part_grid():
    say("\n## R2 — the (phi, N) grid on one price source (broad136 is a superset of u56)")
    broad = load_universe(broad=True)
    small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    EQ = sorted(set(broad.columns) - set(NONEQ) - {"SPY"})
    say(f"  equity pool (broad136 minus the 12 non-equity names minus SPY): {len(EQ)}")
    say("  SPY is joined as a benchmark column only and is never investable in a probe cell.")
    rows = []
    for k in KS:
        for N in NS:
            if N - k > len(EQ) or k > N:
                continue
            for seed in SEEDS:
                rng = np.random.default_rng(20260908 + 1000 * seed + 10 * k + N)
                cols = sorted(list(rng.choice(NONEQ, size=k, replace=False)) +
                              list(rng.choice(EQ, size=N - k, replace=False)))
                rows.append(cell_read(broad, cols, f"broad|k{k}|N{N}|s{seed}", "broad136"))
                say(f"    {rows[-1]['cell']:<22} phi {rows[-1]['phi']:.3f}  D_is {rows[-1]['D_is']:+.4f}"
                    f"  ctl_wins_is {rows[-1]['ctl_wins_is']}")
                flush()
    # named reference cells: the two real panels, SPY excluded from the investable set
    for label, cols in [("REF|u56", sorted(set(load_universe().columns) - {"SPY"})),
                        ("REF|broad136", sorted(set(broad.columns) - {"SPY"}))]:
        rows.append(cell_read(broad, cols, label, "broad136"))
        say(f"    {label:<22} phi {rows[-1]['phi']:.3f}  D_is {rows[-1]['D_is']:+.4f}"
            f"  ctl_wins_is {rows[-1]['ctl_wins_is']}")
        flush()
    # out-of-family check: the small panel, with the same non-equity sleeve spliced in
    say("  out-of-family: SMALL439 (survivorship: current constituents only, see")
    say("  data/SMALL_PANEL_README.md) with the same 12 non-equity names spliced in")
    sm_cols = [c for c in small.columns if c not in bad and c != "SPY" and c not in NONEQ]
    smx = pd.concat([small[[c for c in small.columns if c not in bad and c not in NONEQ]],
                     broad[NONEQ].reindex(small.index).ffill()], axis=1)
    for k in (0, 4, 12):
        for N in (56, 120):
            for seed in (0, 1):
                rng = np.random.default_rng(20260908 + 7 * seed + k + N)
                cols = sorted(list(rng.choice(NONEQ, size=k, replace=False)) +
                              list(rng.choice(sm_cols, size=N - k, replace=False)))
                rows.append(cell_read(smx, cols, f"small|k{k}|N{N}|s{seed}", "small439"))
                say(f"    {rows[-1]['cell']:<22} phi {rows[-1]['phi']:.3f}  D_is {rows[-1]['D_is']:+.4f}"
                    f"  ctl_wins_is {rows[-1]['ctl_wins_is']}")
                flush()
    rows.append(cell_read(smx, sm_cols, "REF|small439", "small439"))
    say(f"    {'REF|small439':<22} phi {rows[-1]['phi']:.3f}  D_is {rows[-1]['D_is']:+.4f}"
        f"  ctl_wins_is {rows[-1]['ctl_wins_is']}")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n  {len(G)} probe cells written to .grid.csv (every point reported)")
    piv = G[G.source == "broad136"].pivot_table(index="phi", columns="N", values="D_is",
                                                aggfunc="mean")
    say("\n  mean D_is = IS Sharpe(control) - IS Sharpe(best gated arm), by (phi, N):")
    say(piv.to_string(float_format=lambda x: f"{x:+.4f}"))
    piv2 = G[G.source == "broad136"].pivot_table(index="phi", columns="N", values="ctl_wins_is",
                                                 aggfunc="mean")
    say("\n  control-wins rate by (phi, N):")
    say(piv2.to_string(float_format=lambda x: f"{x:.2f}"))
    return G


def part_separation(G):
    say("\n## R3 — which panel property carries the sign?  (label = control wins IS)")
    props = ["phi", "N", "inband", "disp", "rho", "negdrift", "avoided", "r_out", "ewvol"]
    rows = []
    for p in props:
        a = auc(G[p].values, G.ctl_wins_is.values)
        acc, thr, sgn = best_threshold(G[p].values, G.ctl_wins_is.values)
        rows.append(dict(property=p, AUC=a, best_acc=acc, threshold=thr, side=("high" if sgn > 0 else "low"),
                         corr_with_D=float(np.corrcoef(G[p].values, G.D_is.values)[0, 1])))
    S = pd.DataFrame(rows).sort_values("best_acc", ascending=False)
    say(S.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    S.to_csv(OUT / f"{STEM}.separation.csv", index=False)
    G[props + ["cell", "source", "D_is", "D_oos", "ctl_wins_is", "ctl_wins_oos"]].to_csv(
        OUT / f"{STEM}.props.csv", index=False)
    # breadth held fixed: does phi still move the sign?
    say("\n  breadth held fixed (broad-source cells only):")
    for N in NS:
        sub = G[(G.source == "broad136") & (G.N == N)]
        if len(sub) < 2:
            continue
        say(f"    N={N:<4} phi {sub.phi.min():.3f}..{sub.phi.max():.3f}  "
            f"D_is {sub.D_is.min():+.4f}..{sub.D_is.max():+.4f}  "
            f"control wins {int(sub.ctl_wins_is.sum())}/{len(sub)}  "
            f"corr(phi, D_is) {np.corrcoef(sub.phi, sub.D_is)[0, 1]:+.3f}")
    say("  composition held fixed (k = 12 non-equity names, breadth varying):")
    sub = G[(G.source == "broad136") & (G.N.isin(NS))]
    for k in KS:
        s2 = G[(G.source == "broad136") & (G.cell.str.contains(f"k{k}\\|"))]
        if len(s2) < 2:
            continue
        say(f"    k={k:<3} N {s2.N.min()}..{s2.N.max()}  D_is {s2.D_is.min():+.4f}..{s2.D_is.max():+.4f}  "
            f"control wins {int(s2.ctl_wins_is.sum())}/{len(s2)}")
    return S


def part_walkforward(G, S):
    """PROTOCOL rule 8: the property AND its threshold are fitted on the IS window's labels
    only, then read once on the untouched 2017-2026 labels."""
    say("\n## R4 — rule 8 walk-forward (property + threshold fitted on IS labels, read on OOS)")
    rows = []
    for p in S.property:
        acc_is, thr, sgn = best_threshold(G[p].values, G.ctl_wins_is.values)
        pred = (G[p].values >= thr) if sgn > 0 else (G[p].values < thr)
        acc_oos = float((pred == G.ctl_wins_oos.values).mean())
        rows.append(dict(property=p, thr=thr, side=("high" if sgn > 0 else "low"),
                         IS_acc=acc_is, OOS_acc=acc_oos,
                         OOS_auc=auc(G[p].values, G.ctl_wins_oos.values)))
    W = pd.DataFrame(rows).sort_values("OOS_acc", ascending=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    base = float(max(G.ctl_wins_oos.mean(), 1 - G.ctl_wins_oos.mean()))
    say(f"  majority-class OOS accuracy (predict the same label everywhere): {base:.4f}")
    say(f"  control wins OOS in {int(G.ctl_wins_oos.sum())} of {len(G)} probe cells")
    return W


def part_keeppaths(fg, curves):
    """Both KEEP paths for the books the corpus actually holds, full sample and OOS window."""
    say("\n## R5 — KEEP paths (4a vs live RULES v2, 4b vs SPY), full sample and OOS window")
    rows = []
    for p in ["u56", "broad136", "small439"]:
        cell = fg[(fg.panel == p) & (fg.cost == COST)].set_index("arm")
        picks = {"control": "control", "IS-argmax": cell["IS_Sharpe"].idxmax(),
                 "IS-argmax-gated": cell.drop("control")["IS_Sharpe"].idxmax()}
        for label, arm in picks.items():
            r = curves[(p, COST, arm)]
            b = curves[(p, COST, "__V2__")]
            s = curves[(p, COST, "__SPY__")]
            kp = H.keep_paths(r, b, s)
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            ms, mso = metrics(s), metrics(s.loc[OOS_START:])
            mb, mbo = metrics(b), metrics(b.loc[OOS_START:])
            rows.append(dict(panel=p, pick=label, arm=arm, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                             MaxDD=m["MaxDD"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                             OOS_MaxDD=mo["MaxDD"], SPY_OOS_CAGR=mso["CAGR"],
                             SPY_OOS_Sharpe=mso["Sharpe"], SPY_OOS_MaxDD=mso["MaxDD"],
                             V2_OOS_Sharpe=mbo["Sharpe"], V2_OOS_MaxDD=mbo["MaxDD"], **kp))
    K = pd.DataFrame(rows)
    say(K.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(f"  4b passes (full): {int(K.pass4b.sum())}/{len(K)};  4b on the OOS window: "
        f"{int(K.pass4b_oos.sum())}/{len(K)};  4a: {int(K.pass4a.sum())}/{len(K)}")
    return K


# ------------------------------------------------------------------ R6: census of the record
ARMCOLS = ("arm", "book", "spec", "config", "label", "name", "variant")


def part_census():
    say("\n## R6 — census: how many published multi-panel menus are degenerate the same way?")
    say("  degenerate(file, panel) := >=2 arms and >=2 cells, and ONE arm is the IS-Sharpe")
    say("  argmax in EVERY cell of that panel — i.e. the chooser is a constant there.")
    rows = []
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM):
            continue
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        cols = {c.lower(): c for c in df.columns}
        if "panel" not in cols and "universe" not in cols:
            continue
        pcol = cols.get("panel", cols.get("universe"))
        armcol = next((cols[a] for a in ARMCOLS if a in cols), None)
        iscol = next((cols[c] for c in ("is_sharpe", "issharpe") if c in cols), None)
        if armcol is None or iscol is None or len(df) < 4:
            continue
        try:
            ids = [c for c in H.id_columns(df, armcol) if c != pcol]
        except Exception:
            continue
        for pname, sub in df.groupby(pcol):
            sub = sub[np.isfinite(pd.to_numeric(sub[iscol], errors="coerce"))]
            if sub.empty:
                continue
            sub = sub.assign(_v=pd.to_numeric(sub[iscol], errors="coerce"))
            if ids:
                key = sub[ids].apply(lambda r: "|".join(map(str, np.ravel(r.values))), axis=1)
            else:
                key = pd.Series("all", index=sub.index)
            g = sub.assign(_k=key.values)
            sizes = g.groupby("_k")["_v"].size()
            idx = g.groupby("_k")["_v"].idxmax()
            stars = g.loc[idx[sizes > 1].values, armcol]
            n_arms = sub[armcol].nunique()
            if len(stars) < 2 or n_arms < 2:
                continue
            share = stars.value_counts(normalize=True).iloc[0]
            rows.append(dict(file=f.name, panel=str(pname), n_cells=len(stars), n_arms=int(n_arms),
                             modal_arm=str(stars.value_counts().index[0]), modal_share=float(share),
                             degenerate=bool(share >= 1.0)))
    C = pd.DataFrame(rows)
    if C.empty:
        say("  no admissible files")
        return C
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    nfiles = C.file.nunique()
    say(f"  admitted {len(C)} (file, panel) menus over {nfiles} committed files")
    say(f"  degenerate: {int(C.degenerate.sum())} of {len(C)} ({C.degenerate.mean():.1%}) — "
        f"{C[C.degenerate].file.nunique()} of {nfiles} files have at least one")
    say("  modal-argmax share, distribution:")
    say(C.modal_share.describe().to_string(float_format=lambda x: f"{x:.3f}"))
    ctl = C.modal_arm.str.strip().str.lower().isin(H.CONTROL_LABELS)
    say(f"  of the degenerate menus, {int((C.degenerate & ctl).sum())} are won by an explicitly "
        f"labelled CONTROL arm; the rest by a named parameter arm")
    top = (C.groupby("panel").agg(n=("degenerate", "size"), deg=("degenerate", "sum"))
           .assign(rate=lambda d: d.deg / d.n).sort_values("n", ascending=False).head(12))
    say("  by panel label (top 12 by menu count):")
    say(top.to_string(float_format=lambda x: f"{x:.3f}"))
    return C


def part_fit():
    """`--fit`: read this script's own committed .grid.csv and separate breadth from
    composition jointly (the two dials are correlated by construction: phi = k / N)."""
    say(f"# {STEM} --fit")
    G = pd.read_csv(OUT / f"{STEM}.grid.csv")

    def ols(y, X, names):
        X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ b
        s2 = resid @ resid / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.pinv(X.T @ X)))
        r2 = 1 - resid.var() / y.var()
        say("    " + "  ".join(f"{n} {bi:+.4f} (t {bi / s:+.2f})"
                               for n, bi, s in zip(["const"] + names, b, se)) + f"   R2 {r2:.3f}")
        return b

    y = G.D_is.values.astype(float)
    say("  D_is on breadth and composition, all 69 probe cells:")
    ols(y, [np.log(G.N.values)], ["logN"])
    ols(y, [G.phi.values], ["phi"])
    ols(y, [np.log(G.N.values), G.phi.values], ["logN", "phi"])
    ols(y, [G.inband.values], ["inband"])
    ols(y, [G.r_out.values], ["r_out"])
    ols(y, [np.log(G.N.values), G.phi.values, G.r_out.values], ["logN", "phi", "r_out"])
    say("  same, broad136-source cells only (one price source, dials orthogonalised by design):")
    B = G[G.source == "broad136"]
    ols(B.D_is.values.astype(float), [np.log(B.N.values), B.phi.values], ["logN", "phi"])
    say("  leave-source-out: fit the sign rule on broad-source cells, read it on small-source:")
    acc, thr, sgn = best_threshold(B.r_out.values, B.ctl_wins_is.values)
    S = G[G.source == "small439"]
    pred = (S.r_out.values >= thr) if sgn > 0 else (S.r_out.values < thr)
    say(f"    r_out threshold {thr:+.4f} ({'high' if sgn > 0 else 'low'}) — in-source acc {acc:.3f}, "
        f"held-out acc {float((pred == S.ctl_wins_is.values).mean()):.3f} on {len(S)} cells")
    for p in ("N", "phi", "inband"):
        a2, t2, s2s = best_threshold(B[p].values, B.ctl_wins_is.values)
        pr = (S[p].values >= t2) if s2s > 0 else (S[p].values < t2)
        say(f"    {p:<7} threshold {t2:+.4f} — in-source acc {a2:.3f}, "
            f"held-out acc {float((pr == S.ctl_wins_is.values).mean()):.3f}")
    (OUT / f"{STEM}.fit.txt").write_text("\n".join(LINES) + "\n")


def part_halves():
    """`--halves`: full-sample halves for the LEADERBOARD rows (books priced in R5 only)."""
    say(f"# {STEM} --halves")
    panels = H.load_panels()
    fg, curves = H.fresh_grid(panels)
    rows = []
    for p in ["u56", "broad136", "small439"]:
        cell = fg[(fg.panel == p) & (fg.cost == COST)].set_index("arm")
        for label, arm in [("control", "control"), ("IS-argmax", cell["IS_Sharpe"].idxmax()),
                           ("SPY", "__SPY__"), ("RULES v2", "__V2__")]:
            r = curves[(p, COST, arm)]
            h = len(r) // 2
            m = metrics(r)
            rows.append(dict(panel=p, pick=label, arm=arm, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                             MaxDD=m["MaxDD"], H1=metrics(r.iloc[:h])["Sharpe"],
                             H2=metrics(r.iloc[h:])["Sharpe"],
                             OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                             OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                             OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"]))
    T = pd.DataFrame(rows)
    say(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    T.to_csv(OUT / f"{STEM}.halves.csv", index=False)
    (OUT / f"{STEM}.halves.txt").write_text("\n".join(LINES) + "\n")


def main():
    if "--halves" in sys.argv:
        return part_halves()
    if "--fit" in sys.argv:
        return part_fit()
    if "--census" in sys.argv:                 # R6 alone (it reads only committed CSVs)
        say(f"# {STEM} --census")
        part_census()
        (OUT / f"{STEM}.census.txt").write_text("\n".join(LINES) + "\n")
        return
    say(f"# {STEM}")
    say(__doc__.strip().split("\n\n")[0])
    fg, curves, LC = part_g0()
    flush()
    part_r1(fg)
    flush()
    G = part_grid()
    flush()
    S = part_separation(G)
    W = part_walkforward(G, S)
    flush()
    K = part_keeppaths(fg, curves)
    flush()
    C = part_census()
    flush()

    say("\n## VERDICT")
    top = S.iloc[0]
    say(f"  best IS separator: {top['property']} (acc {top['best_acc']:.3f}, AUC {top['AUC']:+.3f}); "
        f"best OOS-validated separator: {W.iloc[0]['property']} (OOS acc {W.iloc[0]['OOS_acc']:.3f})")
    say(f"  4b passes anywhere: {int(K.pass4b.sum())} full / {int(K.pass4b_oos.sum())} OOS of {len(K)}")
    flush()
    say(f"\nwrote {STEM}.{{arms,grid,props,separation,walkforward,keeppaths,census,console}}.csv")
    flush()


if __name__ == "__main__":
    main()
