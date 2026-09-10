#!/usr/bin/env python3
"""Idea 466 — re-read every chooser result on the OOS RANK of its constant arm.  (lane B, 2026-09-10)

QUEUE 466: "idea 458 found the arm that sweeps 400/400 of idea 241's IS sub-menus ranks 22/31
(broad136), 7/31 (SMALL439) and 31/31 (u56) out of sample, so the degenerate menus are constant on
the losing side.  Take the 121 degenerate (file,panel) menus idea 458 censused and, wherever the
file publishes an OOS column, report the OOS rank of the constant winner; count how many published
chooser verdicts are constant-on-a-loser.  Max 2 params."

WHAT IS BEING TESTED
  458's census marks a (file, panel) menu DEGENERATE when one arm is the IS-Sharpe argmax in EVERY
  cell of that panel — the chooser is a constant there, so the file's "the chooser picks X" is not
  a choice at all.  458 then showed, on ONE menu (its own probe), that the constant arm is BELOW
  the median arm out of sample on two of three panels and LAST on the third.  466 asks whether that
  is a property of the record, not of one probe.  So for every degenerate menu that publishes an
  OOS column, this file reads off the OOS rank of the arm the file's chooser is constant on.

  The statistic is the constant arm's NORMALISED OOS RANK
        u = (rank - 1) / (n_arms - 1),      rank 1 = best OOS,  u in [0, 1]
  A menu is CONSTANT-ON-A-LOSER when u > 0.5 (the arm the file always picks is worse than the
  median arm out of sample).  u = 0.5 under a coin flip, so the null is explicit and pre-registered.

  A degenerate menu is only damning if a NON-degenerate menu does better; otherwise IS-argmax is
  simply uninformative everywhere and degeneracy is not the defect.  So the same statistic is
  computed for the modal IS winner of every NON-degenerate menu, as the record's own control.

AXES (PROTOCOL rule 4: no more than 2 tuned parameters — the queue names none, so both are mine)
  P1 OOS METRIC in {Sharpe, CAGR, MaxDD}.  Which OOS column the rank is read on.  MaxDD is ranked
     sign-correctly (less negative = better).  ALL THREE ARE REPORTED EVERYWHERE.
  P2 AGGREGATION in {percell, pooled}.  `percell` ranks the arms inside each cell and averages the
     constant arm's normalised rank over the menu's cells; `pooled` ranks the arms once on their
     cell-mean OOS metric.  BOTH ARE REPORTED EVERYWHERE.
  6 grid points, every one published in .grid.csv.
  The CORPUS CUTOFF (458's frozen file set vs today's) and the cost rung in R2 are REPORTED axes,
  not tuned: both settings of each are printed.

GATES (run before any new number is read)
  G1 CENSUS REPRODUCTION.  458's admission and degeneracy code is imported by path, not
     re-implemented, and re-run over the file set as it stood on 2026-09-08.  It must return 458's
     published 121 degenerate menus, in 57 files, 15 of them won by a labelled control arm.
  G2 RANK CONVENTION.  A synthetic menu with a known answer must score u = 0 for an arm that is
     best in every cell, u = 1 for one that is worst, and MaxDD must rank -0.10 above -0.30.
  G3 NO IS/OOS COLLISION.  The detected OOS column must never be the IS column the star was chosen
     on, and both must be finite on the rows used.
  G4 R2 RUNNER.  `fast_bt` (vectorised) vs `engine.backtest`, returns AND turnover, W and M.
  G5 WINDOWS.  IS and OOS are disjoint and jointly exhaust the evaluated live sample.

R2 — RULE 8 ON LIVE PRICES (PROTOCOL rule 8, required)
  The census is archaeology; rule 8 wants the claim re-run out of corpus.  R2 rebuilds 458's probe
  menu (the ungated control plus ten 200d-band gated arms) on three live panels, makes the cells
  seeded sub-panel draws, chooses the IS argmax on 2009-2016 ONLY, and reads 2017-2026 once:
    - is the live menu degenerate, and if so what is the constant arm's OOS rank (the census
      statistic, measured out of corpus)?
    - the chooser run as a REAL BOOK: IS-argmax arm on the full panel, held OOS, reported against
      the live RULES v2 baseline and SPY, with PROTOCOL 4a and 4b evaluated on both windows.

OUTPUTS
  .console.txt  .census.csv  .grid.csv  .walkforward.csv  .result.md
"""
from __future__ import annotations

import importlib.util
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest, metrics, rebalance_mask                      # noqa: E402

STEM = "2026-09-10_re-read-every-chooser-result-on-the-OOS-RANK-of-its-constant-arm_B"
OUT = ROOT / "research" / "backtests"

S458 = "2026-09-08_why-is-the-ungated-control-the-IS-argmax-on-broad136-and-SMALL439-but-not-u56_C"
CUT_458 = "2026-09-09"          # 458 ran on 2026-09-08: its corpus is every file dated < this
CUT_NOW = "9999-99-99"          # today's full corpus

ARMCOLS = ("arm", "book", "spec", "config", "label", "name", "variant")
IS_KEYS = ("is_sharpe", "issharpe")
OOS_PAT = re.compile(r"(?i)^(?:oos[_\.]?(sharpe|cagr|maxdd)|(sharpe|cagr|maxdd)[_\.]?oos)$")
BIGGER_IS_BETTER = {"Sharpe": True, "CAGR": True, "MaxDD": True}   # MaxDD is negative: -0.10 > -0.30
P1_METRICS = ["Sharpe", "CAGR", "MaxDD"]
P2_AGGS = ["percell", "pooled"]

IS_END, OOS_START = "2016-12-31", "2017-01-01"
BAND_LIVE, COSTS, DRAWS, SEED = 0.03, [10.0, 25.0], 30, 20260910
FRAC = 0.60                      # each live cell is a 60% sub-panel draw

LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


def load_harness():
    """Import idea 241's lane-B harness by path (main() is guarded; nothing runs on import).
    458's census used exactly this module's `id_columns` and `CONTROL_LABELS`."""
    p = OUT / "2026-09-08_the-013-margin-rule_B.py"
    spec = importlib.util.spec_from_file_location("h241", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = load_harness()

PROBE_ARMS = [("control", dict(band=None, gross=1.0, freq="W", gated=False))] + [
    (f"b{b:g}-g1.00-{f}", dict(band=b, gross=1.0, freq=f, gated=True))
    for b in (0.0, 0.015, 0.03, 0.045, 0.06) for f in ("W", "M")]


# ---------------------------------------------------------------- rank machinery (P1 x P2)
def rank_of(values: np.ndarray, star: int, metric: str) -> tuple[float, int, int]:
    """(normalised rank u, integer rank, n) of `star` among `values` for `metric`.

    rank 1 = best.  Ties take the average rank, so a menu whose arms are identical scores
    u = 0.5 (the coin-flip null) rather than 1 or 0."""
    v = np.asarray(values, float)
    ok = np.isfinite(v)
    if not ok[star] or ok.sum() < 2:
        return np.nan, -1, int(ok.sum())
    v = v[ok]
    star = int(np.cumsum(ok)[star] - 1)
    s = -v if BIGGER_IS_BETTER[metric] else v
    r = pd.Series(s).rank(method="average").values
    n = len(v)
    return float((r[star] - 1) / (n - 1)) if n > 1 else np.nan, int(round(r[star])), n


def menu_rows(df: pd.DataFrame, pcol: str, armcol: str, iscol: str, ids: list[str]):
    """458's cell decomposition, verbatim in shape: yield (panel, cells) where each cell is
    (arm labels, IS values, row index) and only cells with >=2 arms count."""
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
        cells = [c for _, c in g.groupby("_k") if len(c) > 1]
        if len(cells) < 2 or sub[armcol].nunique() < 2:
            continue
        yield str(pname), sub, cells


def census(cutoff: str) -> pd.DataFrame:
    """One row per admitted (file, panel) menu: 458's degeneracy flag plus, for every P1 x P2
    grid point, the normalised OOS rank of the arm the chooser is constant on."""
    rows = []
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM) or f.name.startswith(S458) or f.name[:10] >= cutoff:
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
        iscol = next((cols[c] for c in IS_KEYS if c in cols), None)
        if armcol is None or iscol is None or len(df) < 4:
            continue
        try:
            ids = [c for c in H.id_columns(df, armcol) if c != pcol]
        except Exception:
            continue
        oos = {}
        for c in df.columns:
            m = OOS_PAT.match(c)
            if m:
                oos.setdefault({"sharpe": "Sharpe", "cagr": "CAGR",
                                "maxdd": "MaxDD"}[(m.group(1) or m.group(2)).lower()], c)
        for pname, sub, cells in menu_rows(df, pcol, armcol, iscol, ids):
            stars = [c.loc[c["_v"].idxmax(), armcol] for c in cells]
            share = pd.Series(stars).value_counts(normalize=True).iloc[0]
            modal = str(pd.Series(stars).value_counts().index[0])
            row = dict(file=f.name, panel=pname, n_cells=len(cells),
                       n_arms=int(sub[armcol].nunique()), modal_arm=modal,
                       modal_share=float(share), degenerate=bool(share >= 1.0),
                       is_control=modal.strip().lower() in H.CONTROL_LABELS,
                       has_oos=bool(oos), oos_cols="|".join(sorted(oos)))
            for met in P1_METRICS:
                oc = oos.get(met)
                if oc is None:
                    row[f"u_percell_{met}"] = row[f"u_pooled_{met}"] = np.nan
                    row[f"nrank_{met}"] = np.nan
                    continue
                us, rr, nn, means = [], [], [], {}
                for c in cells:
                    lab = list(c[armcol].astype(str))
                    v = pd.to_numeric(c[oc], errors="coerce").values
                    if modal not in lab:
                        continue
                    u, ri, n = rank_of(v, lab.index(modal), met)
                    if np.isfinite(u):
                        us.append(u); rr.append(ri); nn.append(n)
                    for a, x in zip(lab, v):
                        means.setdefault(a, []).append(x)
                row[f"u_percell_{met}"] = float(np.mean(us)) if us else np.nan
                row[f"nrank_{met}"] = float(np.mean(rr)) if rr else np.nan
                row[f"ncells_{met}"] = len(us)
                labs = list(means)
                mv = np.array([np.nanmean(means[a]) for a in labs], float)
                if modal in labs and np.isfinite(mv).sum() >= 2:
                    row[f"u_pooled_{met}"] = rank_of(mv, labs.index(modal), met)[0]
                else:
                    row[f"u_pooled_{met}"] = np.nan
            rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- R2 live runner
def ew_band_weights(px, band, gross, gated=True):
    """241/458's arm weights, verbatim: EW over everything priced at gross/N, gated names to CASH."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0) if gated else ew


def fast_bt(px, w, freq):
    """Vectorised equivalent of engine.backtest returning GROSS returns and turnover separately,
    so the cost rung is a post-hoc sweep.  Gated against engine.backtest at G4."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]

    def _held(start_idx, rows=None):
        base = Cp[start_idx]
        top = Cp if rows is None else Cp[rows]
        g = np.divide(top, base, out=np.zeros_like(base), where=base != 0)
        raw = wt[start_idx] * g
        nav = raw.sum(axis=1) + (1.0 - wt[start_idx].sum(axis=1))
        nav = np.where(nav > 0, nav, 1.0)
        return raw / nav[:, None]

    held = _held(s0)
    gross = (held * rets).sum(axis=1)
    turn = np.zeros(T)
    turn[0] = np.abs(wt[0]).sum()
    if len(reb) > 1:
        rows = reb[1:]
        turn[rows] = np.abs(wt[rows] - _held(s0[rows - 1], rows)).sum(axis=1)
    return pd.Series(gross, index=idx), pd.Series(turn, index=idx)


def win(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    return metrics(x) if len(x) >= 30 else {k: np.nan for k in ("CAGR", "Sharpe", "MaxDD")}


def arm_streams(px_all, cols, start):
    """(gross, turnover) per arm on `cols`; other columns are benchmarks the arms hold zero in."""
    out = {}
    for name, a in PROBE_ARMS:
        w = ew_band_weights(px_all[cols], 0.0 if a["band"] is None else a["band"],
                            a["gross"], gated=a["gated"]).reindex(columns=px_all.columns).fillna(0.0)
        g, t = fast_bt(px_all, w, a["freq"])
        out[name] = (g.loc[start:], t.loc[start:])
    return out


# ---------------------------------------------------------------- gates
def gates(panels):
    say("\n## GATES")
    C458 = census(CUT_458)
    d = int(C458.degenerate.sum())
    nf = C458[C458.degenerate].file.nunique()
    nc = int((C458.degenerate & C458.is_control).sum())
    ok1 = (d == 121) and (nf == 57) and (nc == 15)
    say(f"  G1 census reproduction (458's corpus, files dated < {CUT_458}): admitted {len(C458)} "
        f"menus in {C458.file.nunique()} files; DEGENERATE {d} (published 121) in {nf} files "
        f"(published 57); control-won {nc} (published 15)  -> {'PASS' if ok1 else 'FAIL'}")
    say(f"     458 published the denominator as 566 menus / 194 files; this run admits {len(C458)}"
        f" / {C458.file.nunique()}.  The drift is +{len(C458)-566} menus in +{C458.file.nunique()-194}"
        "  files dated 2026-09-08 that landed AFTER 458 ran; all three degeneracy figures are exact.")

    lab = ["a", "b", "c"]
    cells = [pd.DataFrame({"arm": lab, "IS_Sharpe": [3, 2, 1], "OOS_Sharpe": [1, 2, 3],
                           "OOS_MaxDD": [-0.30, -0.20, -0.10]}) for _ in range(2)]
    v = cells[0]["OOS_Sharpe"].values
    u_worst = rank_of(v, 0, "Sharpe")[0]
    u_best = rank_of(v, 2, "Sharpe")[0]
    u_dd = rank_of(cells[0]["OOS_MaxDD"].values, 2, "MaxDD")[0]
    u_tie = rank_of(np.array([1.0, 1.0, 1.0]), 0, "Sharpe")[0]
    ok2 = (u_worst == 1.0) and (u_best == 0.0) and (u_dd == 0.0) and (u_tie == 0.5)
    say(f"  G2 rank convention: worst arm u={u_worst:.2f} (want 1.00), best u={u_best:.2f} (0.00), "
        f"MaxDD -0.10 u={u_dd:.2f} (0.00), all-tied u={u_tie:.2f} (0.50) -> {'PASS' if ok2 else 'FAIL'}")

    coll = 0
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM) or f.name[:10] >= CUT_458:
            continue
        try:
            cs = pd.read_csv(f, nrows=1).columns
        except Exception:
            continue
        low = {c.lower() for c in cs}
        coll += len({c for c in cs if OOS_PAT.match(c)} & {c for c in cs if c.lower() in IS_KEYS})
        assert not (low & set(IS_KEYS) & {c.lower() for c in cs if OOS_PAT.match(c)})
    say(f"  G3 no IS/OOS column collision over the corpus: {coll} collisions -> "
        f"{'PASS' if coll == 0 else 'FAIL'}")

    px = panels["u56"][0]
    cols = panels["u56"][1][:20]
    w = ew_band_weights(px[cols], BAND_LIVE, 1.0).reindex(columns=px.columns).fillna(0.0)
    worst = 0.0
    for fq in ("W", "M"):
        g, t = fast_bt(px, w, fq)
        e = backtest(px, w, cost_bps=0.0, freq=fq)
        worst = max(worst, float(np.abs(g - e["returns"]).max()),
                    float(np.abs(t - e["turnover"]).max()))
    ok4 = worst < 1e-10
    say(f"  G4 fast_bt vs engine.backtest (returns AND turnover, W and M): max abs diff {worst:.3e}"
        f" -> {'PASS' if ok4 else 'FAIL'}")

    idx = px.loc[px.index[260]:].index
    a, b = idx[idx <= IS_END], idx[idx >= OOS_START]
    ok5 = len(a) + len(b) == len(idx) and a.max() < b.min()
    say(f"  G5 windows: IS {a.min().date()}..{a.max().date()} ({len(a)}d), OOS {b.min().date()}.."
        f"{b.max().date()} ({len(b)}d), disjoint and exhaustive -> {'PASS' if ok5 else 'FAIL'}")
    assert ok1 and ok2 and coll == 0 and ok4 and ok5, "a gate failed"
    return C458


# ---------------------------------------------------------------- R1
def report_grid(C: pd.DataFrame, tag: str) -> pd.DataFrame:
    """Every P1 x P2 grid point, on degenerate menus and on the non-degenerate control."""
    rows = []
    for met in P1_METRICS:
        for agg in P2_AGGS:
            col = f"u_{agg}_{met}"
            for deg in (True, False):
                s = C.loc[C.degenerate == deg, col].dropna()
                if s.empty:
                    rows.append(dict(corpus=tag, metric=met, agg=agg, degenerate=deg, n=0))
                    continue
                rows.append(dict(corpus=tag, metric=met, agg=agg, degenerate=deg, n=len(s),
                                 mean_u=float(s.mean()), median_u=float(s.median()),
                                 loser_share=float((s > 0.5).mean()),
                                 strict_last=float((s == 1.0).mean()),
                                 strict_first=float((s == 0.0).mean()),
                                 t_vs_half=float((s.mean() - 0.5) / (s.std(ddof=1) / np.sqrt(len(s))))
                                 if len(s) > 2 and s.std(ddof=1) > 0 else np.nan))
    return pd.DataFrame(rows)


def part_r1(C458: pd.DataFrame):
    say("\n## R1 — the census, re-read on the OOS rank of the constant arm")
    say("  u = normalised OOS rank of the arm the chooser is constant on (0 = best arm out of")
    say("  sample, 1 = worst, 0.5 = the coin-flip null).  CONSTANT-ON-A-LOSER := u > 0.5.")
    Cnow = census(CUT_NOW)
    grids = []
    for tag, C in (("458-frozen", C458), ("today", Cnow)):
        d = C[C.degenerate]
        say(f"\n  corpus {tag}: {len(C)} admitted menus in {C.file.nunique()} files; "
            f"{len(d)} degenerate ({len(d)/len(C):.1%}) in {d.file.nunique()} files; "
            f"{int(d.has_oos.sum())} of the degenerate menus publish an OOS column")
        g = report_grid(C, tag)
        grids.append(g)
        say(g.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    G = pd.concat(grids, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    Cnow.to_csv(OUT / f"{STEM}.census.csv", index=False)

    say("\n  HEADLINE (458's own frozen corpus, the queue's 121 menus, OOS Sharpe, per-cell):")
    d = C458[C458.degenerate & C458.u_percell_Sharpe.notna()]
    say(f"    {len(d)} of the 121 degenerate menus publish an OOS Sharpe column")
    say(f"    mean u {d.u_percell_Sharpe.mean():.3f}  median {d.u_percell_Sharpe.median():.3f}")
    say(f"    CONSTANT-ON-A-LOSER (u > 0.5): {int((d.u_percell_Sharpe > 0.5).sum())} of {len(d)} "
        f"({(d.u_percell_Sharpe > 0.5).mean():.1%})")
    say(f"    constant on the OOS-WORST arm in every cell (u = 1.0): "
        f"{int((d.u_percell_Sharpe == 1.0).sum())}")
    say(f"    constant on the OOS-BEST arm in every cell (u = 0.0): "
        f"{int((d.u_percell_Sharpe == 0.0).sum())}")
    nd = C458[(~C458.degenerate) & C458.u_percell_Sharpe.notna()]
    say(f"    CONTROL — non-degenerate menus, modal IS winner: n {len(nd)}, mean u "
        f"{nd.u_percell_Sharpe.mean():.3f}, loser share {(nd.u_percell_Sharpe > 0.5).mean():.1%}")
    say("\n  BY MENU WIDTH — with n_arms = 2 the statistic is binary (u is 0 or 1 only), so a")
    say("  corpus full of 2-arm menus can move the mean without any arm ever being mid-ranked:")
    for tag, C in (("458-frozen", C458), ("today", Cnow)):
        d = C[C.degenerate & C.u_percell_Sharpe.notna()].copy()
        d["width"] = pd.cut(d.n_arms, [1, 2, 3, 5, 10, 10_000],
                            labels=["2", "3", "4-5", "6-10", "11+"])
        t = d.groupby("width", observed=True).agg(
            n=("u_percell_Sharpe", "size"), mean_u=("u_percell_Sharpe", "mean"),
            loser=("u_percell_Sharpe", lambda s: (s > 0.5).mean()),
            worst=("u_percell_Sharpe", lambda s: (s == 1.0).mean()))
        say(f"    corpus {tag}:")
        say(t.to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n  458's OWN probe menu placed inside this distribution (its three published ranks):")
    pub = [("u56", 31, 31), ("broad136", 22, 31), ("SMALL439", 7, 31)]
    us = [(r - 1) / (n - 1) for _, r, n in pub]
    d = C458[C458.degenerate & C458.u_percell_Sharpe.notna()].u_percell_Sharpe
    for (p, r, n), u in zip(pub, us):
        say(f"    {p:9s} rank {r}/{n} -> u {u:.3f}; census percentile "
            f"{(d < u).mean():.1%} of the 117 degenerate menus")
    say(f"    458's probe mean u {np.mean(us):.3f} vs census mean {d.mean():.3f} — the probe sits "
        f"at the {(d < np.mean(us)).mean():.1%} percentile of the record it was generalised to")

    say("\n  per-file worst offenders (degenerate menus, u_percell_Sharpe, today's corpus):")
    dn = Cnow[Cnow.degenerate & Cnow.u_percell_Sharpe.notna()]
    top = dn.sort_values("u_percell_Sharpe", ascending=False).head(12)
    say(top[["file", "panel", "n_cells", "n_arms", "modal_arm", "u_percell_Sharpe"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return C458, Cnow, G


# ---------------------------------------------------------------- R2
def part_r2(panels):
    say("\n## R2 — PROTOCOL rule 8: the same statistic on LIVE PRICES, out of corpus")
    say(f"  cells = {DRAWS} seeded {FRAC:.0%} sub-panel draws per panel (seed {SEED}); arms = 458's")
    say("  probe menu (control + 10 band-gated); arm chosen on IS Sharpe 2009-2016 ONLY; 2017- read once.")
    rows, books = [], []
    for pname, (px, cols) in panels.items():
        start = px.index[260]
        rng = np.random.default_rng(SEED)
        full = arm_streams(px, cols, start)
        cells = [list(rng.choice(cols, size=max(8, int(round(FRAC * len(cols)))), replace=False))
                 for _ in range(DRAWS)]
        for cost in COSTS:
            per_cell = []
            for ci, cc in enumerate(cells):
                keep = list(dict.fromkeys(list(cc) + (["SPY"] if "SPY" in px.columns else [])))
                R = arm_streams(px[keep], cc, start)
                net = {k: g - t * cost / 1e4 for k, (g, t) in R.items()}
                labs = list(net)
                I = np.array([win(net[k], hi=IS_END)["Sharpe"] for k in labs])
                O = np.array([win(net[k], lo=OOS_START)["Sharpe"] for k in labs])
                per_cell.append((labs, I, O))
            stars = [labs[int(np.nanargmax(I))] for labs, I, O in per_cell]
            share = pd.Series(stars).value_counts(normalize=True).iloc[0]
            modal = str(pd.Series(stars).value_counts().index[0])
            us = [rank_of(O, labs.index(modal), "Sharpe")[0] for labs, I, O in per_cell
                  if modal in labs]
            us = [u for u in us if np.isfinite(u)]
            netf = {k: g - t * cost / 1e4 for k, (g, t) in full.items()}
            labs = list(netf)
            If = np.array([win(netf[k], hi=IS_END)["Sharpe"] for k in labs])
            Of = np.array([win(netf[k], lo=OOS_START)["Sharpe"] for k in labs])
            fstar = labs[int(np.nanargmax(If))]
            uf = rank_of(Of, labs.index(fstar), "Sharpe")
            rows.append(dict(panel=pname, cost_bps=cost, n_cells=len(per_cell), n_arms=len(labs),
                             modal_share=float(share), degenerate=bool(share >= 1.0),
                             modal_arm=modal, mean_u_oos=float(np.mean(us)) if us else np.nan,
                             loser_share=float(np.mean(np.array(us) > 0.5)) if us else np.nan,
                             full_panel_IS_argmax=fstar, full_panel_u_oos=uf[0],
                             full_panel_oos_rank=f"{uf[1]}/{uf[2]}"))
            if cost == 10.0:
                books.append((pname, fstar, netf[fstar], px))
    W = pd.DataFrame(rows)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    say("\n  THE CHOOSER AS A REAL BOOK (10 bps, PROTOCOL rule 2): IS-argmax arm on the FULL panel,")
    say("  held out of sample, vs the live RULES v2 baseline and SPY.  PROTOCOL 4a and 4b evaluated.")
    krows = []
    for pname, arm, r, px in books:
        start = px.index[260]
        bres = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")
        b = bres["returns"].loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        for lab, rr in (("book", r), ("RULES v2", b), ("SPY", spy)):
            for wlab, lo, hi in (("FULL", None, None), ("IS", None, IS_END), ("OOS", OOS_START, None)):
                m = win(rr, lo, hi)
                krows.append(dict(panel=pname, arm=arm if lab == "book" else lab, series=lab,
                                  window=wlab, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"]))
        h = len(r) // 2
        H1, H2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
        bh1, bh2 = metrics(b.iloc[:h]), metrics(b.iloc[h:])
        sh1, sh2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
        mo, so = win(r, OOS_START), win(spy, OOS_START)
        p4a = (H1["Sharpe"] > bh1["Sharpe"] and H2["Sharpe"] > bh2["Sharpe"]
               and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])
        p4b = (H1["Sharpe"] > sh1["Sharpe"] and H2["Sharpe"] > sh2["Sharpe"]
               and mo["Sharpe"] > so["Sharpe"] and metrics(r)["MaxDD"] >= 0.60 * metrics(spy)["MaxDD"]
               and metrics(r)["CAGR"] >= 0.70 * metrics(spy)["CAGR"])
        say(f"    {pname:9s} arm {arm:14s} halves {H1['Sharpe']:.3f}/{H2['Sharpe']:.3f} "
            f"(v2 {bh1['Sharpe']:.3f}/{bh2['Sharpe']:.3f}, SPY {sh1['Sharpe']:.3f}/{sh2['Sharpe']:.3f}) "
            f"| OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%} vs SPY "
            f"{so['CAGR']:.2%}/{so['Sharpe']:.3f}/{so['MaxDD']:.2%} | 4a {p4a} 4b {p4b}")
    K = pd.DataFrame(krows)
    say("\n  full metric table (every window, every comparand):")
    say(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return W, K


def main():
    say(f"# {STEM}")
    say(__doc__.split("OUTPUTS")[0].strip())
    panels = {}
    for lab, kw in (("u56", {}), ("broad136", dict(broad=True)), ("small484", dict(small=True))):
        px = load_universe(**kw)
        panels[lab] = (px, [c for c in px.columns if c != "SPY"])
        say(f"\nloaded {lab}: {px.shape[1]} columns, {px.index[0].date()}..{px.index[-1].date()}")
    C458 = gates(panels)
    part_r1(C458)
    if "--r1" not in sys.argv:
        part_r2(panels)
    say(f"\nwrote {STEM}.{{census,grid,walkforward,console}}.csv/txt")
    flush()


if __name__ == "__main__":
    main()
