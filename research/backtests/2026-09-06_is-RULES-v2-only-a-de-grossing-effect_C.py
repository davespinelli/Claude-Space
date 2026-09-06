#!/usr/bin/env python3
"""Idea 274 — is RULES v2 only a de-grossing effect?

RULES v2 (live 2026-09-06) = hold every priced name inside the 200d +/-3% band at
0.75/N of NAV, gated-out weight to CASH, weekly, no ranking, no vol filter.
Published: u56, 10 bps, 8.66% CAGR / 1.2056 Sharpe / -12.05% MaxDD, halves 1.2259/1.1908.

The question: does the gate carry information, or is it just an exposure choice?
Because the gate de-grosses (nominal 0.75, realised mean gross ~0.53), any comparison
against the un-gated 0.75 book is confounded by exposure. So build MATCHED controls:

  V2      the live book (band gate, de-gross to cash).
  CG(g)   NO gate, constant nominal gross g, equal weight over priced names, weekly.
          Swept as a ladder; g* = the rung whose REALISED mean gross matches V2's.
  RGT(k)  random gate at the same average exposure: each name's gate series circularly
          rotated by an independent random shift. Preserves every name's on-share,
          persistence and turnover; destroys the gate's TIMING alignment with returns.
          This is the queue's "random-gate book at the same average exposure".
  RGP(k)  the same gate matrix with its COLUMN LABELS permuted. Preserves the daily
          in-band COUNT exactly (identical gross path and timing) and destroys only
          WHICH names are held. Decomposition bonus: separates timing from selection.

Both nulls are turnover-matched by construction, which is what idea 262 says a
non-zero cost rung otherwise turns into a turnover test rather than an information test.
Every arm is also priced at 0 bps for the same reason.

Tuned parameters: ONE — the constant gross g of the CG control (full ladder reported).
Band width held at the live 3%; null draw count is not a tuned parameter.

Rule 8 walk-forward: IS = 2009-01-01..2016-12-31 chooses, OOS = 2017-01-01..end read once.
Both KEEP paths evaluated: 4a vs the live RULES v2 book, 4b vs SPY.

Deterministic (seeded). Standalone: python research/backtests/2026-09-06_...C.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state, backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
BAND, NOMINAL_GROSS, FREQ = 0.03, 0.75, "W"
RUNGS = (0, 10)                     # cost rungs, bps
GROSS_LADDER = [round(x, 3) for x in np.arange(0.20, 1.001, 0.05)]
N_DRAWS = 60
SEED = 20260906
WARMUP = 260                        # bars skipped, same as baseline.compare


# ---------------------------------------------------------------- books
def ew_priced(px):
    """Equal weight over names priced that day, gross 1.0."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def cg_weights(px, g):
    """CG(g): no gate, constant nominal gross g."""
    return ew_priced(px) * g


def gated_weights(px, gate, g=NOMINAL_GROSS):
    """EWall at g/N, gated to cash by `gate` (a boolean frame)."""
    return (ew_priced(px) * g).where(gate, 0.0)


def rotate_gate(gate, rng):
    """Per-name independent circular rotation of the boolean gate series."""
    a = gate.values
    out = np.empty_like(a)
    shifts = rng.integers(1, a.shape[0], size=a.shape[1])
    for j in range(a.shape[1]):
        out[:, j] = np.roll(a[:, j], shifts[j])
    return pd.DataFrame(out, index=gate.index, columns=gate.columns)


def permute_gate(gate, rng):
    """Permute the gate's column labels (derangement-ish: resample until <20% fixed)."""
    cols = list(gate.columns)
    for _ in range(50):
        perm = rng.permutation(len(cols))
        if (perm == np.arange(len(cols))).mean() < 0.20:
            break
    out = gate.values[:, perm]
    return pd.DataFrame(out, index=gate.index, columns=cols)


# ---------------------------------------------------------------- evaluation
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fail4a(r, base_r):
    """4a: Sharpe > live book in BOTH halves and MaxDD no worse."""
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base_r)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base_r)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def run(px, w, bps, start):
    res = backtest(px, w, cost_bps=bps, freq=FREQ)
    r = res["returns"].loc[start:]
    gross = res["weights"].sum(axis=1).loc[start:]
    turn = res["turnover"].loc[start:]
    return r, gross, turn


def summarise(name, r, gross, turn, spy, arm=""):
    h1, h2 = half_sharpes(r)
    m = metrics(r); mo = metrics(r.loc[OOS_START:]); mi = metrics(r.loc[IS_START:IS_END])
    return dict(arm=arm or name, name=name,
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                H1=h1, H2=h2,
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                gross_mean=float(gross.mean()),
                gross_mean_IS=float(gross.loc[IS_START:IS_END].mean()),
                gross_mean_OOS=float(gross.loc[OOS_START:].mean()),
                gross_sd=float(gross.std()),
                turnover=float(turn.sum() / (len(turn) / 252)),
                f4a=fail4a(r, spy["base_r"]), f4b=fail4b(r, spy["spy"], r.loc[OOS_START:], spy["spy"].loc[OOS_START:]))


def fmt(df, cols=None):
    d = df[cols] if cols else df
    return d.to_string(float_format=lambda x: f"{x:.4f}")


# ---------------------------------------------------------------- main
def analyse(px, panel, draws=N_DRAWS, ladder=GROSS_LADDER, verbose=True):
    start = px.index[WARMUP]
    gate = band_state(px, BAND)
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    rows, series = [], {}

    for bps in RUNGS:
        base_r, base_g, base_t = run(px, rules_v2_weights(px, BAND, NOMINAL_GROSS), bps, start)
        ctx = dict(spy=spy_r, base_r=base_r)
        v1_r, v1_g, v1_t = run(px, rules_v1_weights(px), bps, start)

        rows.append(dict(panel=panel, bps=bps, family="LIVE",
                         **summarise("RULES v2 (live)", base_r, base_g, base_t, ctx)))
        rows.append(dict(panel=panel, bps=bps, family="LIVE",
                         **summarise("RULES v1 (previous)", v1_r, v1_g, v1_t, ctx)))
        sm = metrics(spy_r); smo = metrics(spy_r.loc[OOS_START:]); smi = metrics(spy_r.loc[IS_START:IS_END])
        s1, s2 = half_sharpes(spy_r)
        rows.append(dict(panel=panel, bps=bps, family="BENCH", arm="SPY", name="SPY",
                         CAGR=sm["CAGR"], Sharpe=sm["Sharpe"], MaxDD=sm["MaxDD"], Vol=sm["Vol"],
                         H1=s1, H2=s2, IS_CAGR=smi["CAGR"], IS_Sharpe=smi["Sharpe"], IS_MaxDD=smi["MaxDD"],
                         OOS_CAGR=smo["CAGR"], OOS_Sharpe=smo["Sharpe"], OOS_MaxDD=smo["MaxDD"],
                         gross_mean=1.0, gross_mean_IS=1.0, gross_mean_OOS=1.0, gross_sd=0.0,
                         turnover=0.0, f4a=fail4a(spy_r, base_r), f4b="-"))
        series[(panel, bps, "V2")] = base_r

        # ---- CG ladder (the one tuned parameter; every rung reported)
        for g in ladder:
            r, gr, tu = run(px, cg_weights(px, g), bps, start)
            rows.append(dict(panel=panel, bps=bps, family="CG", g=g,
                             **summarise(f"CG g={g:.2f}", r, gr, tu, ctx, arm="CG")))
            series[(panel, bps, f"CG{g:.2f}")] = r

        # ---- nulls: rotated gate (RGT) and label-permuted gate (RGP)
        for kind, maker in (("RGT", rotate_gate), ("RGP", permute_gate)):
            rng = np.random.default_rng(SEED + (0 if kind == "RGT" else 999))
            for k in range(draws):
                gk = maker(gate, rng)
                r, gr, tu = run(px, gated_weights(px, gk), bps, start)
                rows.append(dict(panel=panel, bps=bps, family=kind, draw=k,
                                 **summarise(f"{kind} draw {k}", r, gr, tu, ctx, arm=kind)))
        if verbose:
            print(f"  [{panel} @{bps}bps] done", flush=True)
    return pd.DataFrame(rows)


def null_band(df, family, panel, bps, col):
    x = df[(df.family == family) & (df.panel == panel) & (df.bps == bps)][col].values
    return dict(n=len(x), mean=float(x.mean()), sd=float(x.std(ddof=1)),
                q05=float(np.quantile(x, 0.05)), q50=float(np.quantile(x, 0.50)),
                q95=float(np.quantile(x, 0.95)), lo=float(x.min()), hi=float(x.max()))


def pct_of(df, family, panel, bps, col, value):
    x = df[(df.family == family) & (df.panel == panel) & (df.bps == bps)][col].values
    return float((x < value).mean())


def main():
    pd.set_option("display.width", 250)
    print("=" * 100)
    print("Idea 274 — is RULES v2 only a de-grossing effect?  (lane C, 2026-09-06)")
    print("=" * 100)

    px = load_universe()
    start = px.index[WARMUP]
    print(f"u56 panel: {px.shape[1]} columns, {px.index[0].date()}..{px.index[-1].date()}, "
          f"evaluated from {start.date()}")

    # ---------- reproduction check against the CHANGELOG's published digits
    r0, g0, t0 = run(px, rules_v2_weights(px, BAND, NOMINAL_GROSS), 10, start)
    m0 = metrics(r0); h1, h2 = half_sharpes(r0)
    pub = dict(CAGR=0.0866, Sharpe=1.2056, MaxDD=-0.1205, H1=1.2259, H2=1.1908, turnover=1.77)
    got = dict(CAGR=m0["CAGR"], Sharpe=m0["Sharpe"], MaxDD=m0["MaxDD"], H1=h1, H2=h2,
               turnover=float(t0.sum() / (len(t0) / 252)))
    print("\nREPRODUCTION of the live book (published vs re-run):")
    for k in pub:
        print(f"  {k:9s} published {pub[k]:+.4f}   re-run {got[k]:+.4f}   diff {got[k]-pub[k]:+.5f}")
    assert abs(got["Sharpe"] - pub["Sharpe"]) < 5e-4 and abs(got["CAGR"] - pub["CAGR"]) < 5e-4, "reproduction failed"
    print("  -> reproduction EXACT to published precision.")

    # ---------- the exposure fact the question rests on
    gross = g0
    print(f"\nEXPOSURE: v2 nominal gross {NOMINAL_GROSS:.2f}; REALISED mean gross "
          f"{gross.mean():.4f} (IS {gross.loc[IS_START:IS_END].mean():.4f}, "
          f"OOS {gross.loc[OOS_START:].mean():.4f}), sd {gross.std():.4f}, "
          f"min {gross.min():.4f}, max {gross.max():.4f}")
    onshare = band_state(px, BAND).loc[start:].mean().mean()
    fwd60 = px["SPY"].pct_change(60).shift(-60).loc[start:]
    both = pd.concat([gross.rename("g"), fwd60.rename("f")], axis=1).dropna()
    print(f"         gate on-share (mean over names/days) {onshare:.4f}; "
          f"corr(gross_t, SPY next-60d return) {both.g.corr(both.f):+.4f} over {len(both)} days")

    # ---------- main grid
    print("\nRunning grid (u56): 2 rungs x [ladder %d + 2 nulls x %d draws]..." % (len(GROSS_LADDER), N_DRAWS))
    grid = analyse(px, "u56")

    # ---------- broad-panel replicate (survivorship: current constituents only)
    print("\nRunning broad replicate (fewer draws)...")
    pxb = load_universe(broad=True)
    gridb = analyse(pxb, "broad", draws=20)
    grid = pd.concat([grid, gridb], ignore_index=True)
    grid.to_csv(OUT.with_name(OUT.name + "_grid.csv"), index=False)
    print(f"grid rows: {len(grid)} -> {OUT.name}_grid.csv")

    # ---------- Q1: does a constant-gross book at MATCHED exposure reproduce v2?
    print("\n" + "=" * 100)
    print("Q1  CG LADDER — every rung reported.  g* = rung whose REALISED mean gross matches v2's.")
    print("=" * 100)
    matched = {}
    for panel in ("u56", "broad"):
        v2 = grid[(grid.panel == panel) & (grid.bps == 10) & (grid.name == "RULES v2 (live)")].iloc[0]
        lad = grid[(grid.panel == panel) & (grid.bps == 10) & (grid.family == "CG")].copy()
        lad["gross_gap"] = (lad.gross_mean - v2.gross_mean).abs()
        gstar = float(lad.sort_values("gross_gap").iloc[0].g)
        matched[panel] = gstar
        print(f"\n--- {panel}: v2 realised gross {v2.gross_mean:.4f} -> matched rung g*={gstar:.2f} "
              f"(realised {lad.set_index('g').loc[gstar,'gross_mean']:.4f}) @10bps")
        print(fmt(lad.set_index("g")[["gross_mean", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                      "OOS_Sharpe", "OOS_CAGR", "turnover", "f4a", "f4b"]]))
        print(f"    v2 row: gross {v2.gross_mean:.4f} CAGR {v2.CAGR:.4f} Sharpe {v2.Sharpe:.4f} "
              f"MaxDD {v2.MaxDD:.4f} H1/H2 {v2.H1:.4f}/{v2.H2:.4f} OOS {v2.OOS_Sharpe:.4f} "
              f"turnover {v2.turnover:.2f} 4a[{v2.f4a}] 4b[{v2.f4b}]")

    # headline table: v2 vs matched CG vs nulls, both rungs, both panels
    print("\n" + "=" * 100)
    print("Q2  MATCHED CONTROLS — v2 against CG(g*), the rotated-gate null (RGT) and the")
    print("    label-permuted-gate null (RGP).  Both nulls are turnover-matched by construction.")
    print("=" * 100)
    head = []
    for panel in ("u56", "broad"):
        for bps in RUNGS:
            sl = grid[(grid.panel == panel) & (grid.bps == bps)]
            v2 = sl[sl.name == "RULES v2 (live)"].iloc[0]
            cg = sl[(sl.family == "CG") & (sl.g == matched[panel])].iloc[0]
            spy = sl[sl.family == "BENCH"].iloc[0]
            head.append(dict(panel=panel, bps=bps, arm="V2", **{k: v2[k] for k in
                        ("gross_mean", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "turnover", "f4a", "f4b")}))
            head.append(dict(panel=panel, bps=bps, arm=f"CG g*={matched[panel]:.2f}", **{k: cg[k] for k in
                        ("gross_mean", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "turnover", "f4a", "f4b")}))
            for fam in ("RGT", "RGP"):
                b = sl[sl.family == fam]
                if not len(b): continue
                head.append(dict(panel=panel, bps=bps, arm=f"{fam} mean({len(b)})",
                                 gross_mean=b.gross_mean.mean(), CAGR=b.CAGR.mean(), Sharpe=b.Sharpe.mean(),
                                 MaxDD=b.MaxDD.mean(), H1=b.H1.mean(), H2=b.H2.mean(),
                                 OOS_Sharpe=b.OOS_Sharpe.mean(), OOS_CAGR=b.OOS_CAGR.mean(),
                                 turnover=b.turnover.mean(), f4a=f"{(b.f4a=='-').sum()}/{len(b)} pass",
                                 f4b=f"{(b.f4b=='-').sum()}/{len(b)} pass"))
            head.append(dict(panel=panel, bps=bps, arm="SPY", **{k: spy[k] for k in
                        ("gross_mean", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "turnover", "f4a", "f4b")}))
    H = pd.DataFrame(head)
    print(fmt(H.set_index(["panel", "bps", "arm"])))
    H.to_csv(OUT.with_name(OUT.name + "_headline.csv"), index=False)

    # null bands and v2's percentile within them
    print("\nNULL BANDS (Sharpe) and v2's position inside them:")
    band_rows = []
    for panel in ("u56", "broad"):
        for bps in RUNGS:
            v2 = grid[(grid.panel == panel) & (grid.bps == bps) & (grid.name == "RULES v2 (live)")].iloc[0]
            for fam in ("RGT", "RGP"):
                for col in ("Sharpe", "CAGR", "MaxDD", "OOS_Sharpe"):
                    nb = null_band(grid, fam, panel, bps, col)
                    band_rows.append(dict(panel=panel, bps=bps, null=fam, metric=col, v2=v2[col],
                                          **nb, pctile=pct_of(grid, fam, panel, bps, col, v2[col]),
                                          z=(v2[col] - nb["mean"]) / nb["sd"] if nb["sd"] else np.nan))
    B = pd.DataFrame(band_rows)
    print(fmt(B.set_index(["panel", "bps", "null", "metric"])))
    B.to_csv(OUT.with_name(OUT.name + "_nullbands.csv"), index=False)

    # ---------- Q3: rule 8 walk-forward
    print("\n" + "=" * 100)
    print("Q3  RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 only, 2017-2026 read once.")
    print("=" * 100)
    wf = []
    for panel in ("u56", "broad"):
        for bps in RUNGS:
            sl = grid[(grid.panel == panel) & (grid.bps == bps)]
            spy = sl[sl.family == "BENCH"].iloc[0]
            v2 = sl[sl.name == "RULES v2 (live)"].iloc[0]
            lad = sl[sl.family == "CG"]
            # (a) IS-Sharpe argmax over the gross ladder
            pick_s = lad.loc[lad.IS_Sharpe.idxmax()]
            # (b) IS realised-gross match to v2's IS gross (no OOS information at all)
            pick_m = lad.loc[(lad.gross_mean_IS - v2.gross_mean_IS).abs().idxmin()]
            # (c) chooser over {V2, CG@IS-argmax} by IS Sharpe
            cand = pd.concat([sl[sl.name == "RULES v2 (live)"], pick_s.to_frame().T])
            pick_c = cand.loc[cand.IS_Sharpe.astype(float).idxmax()]
            for label, p in (("CG IS-argmax g", pick_s), ("CG IS-gross-matched g", pick_m),
                             ("chooser{V2,CG}", pick_c), ("V2 (do-nothing)", v2), ("SPY", spy)):
                wf.append(dict(panel=panel, bps=bps, selector=label,
                               pick=p.get("name", p["arm"]), IS_Sharpe=p.IS_Sharpe, IS_CAGR=p.IS_CAGR,
                               OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                               f4a=p.f4a, f4b=p.f4b))
    W = pd.DataFrame(wf)
    print(fmt(W.set_index(["panel", "bps", "selector"])))
    W.to_csv(OUT.with_name(OUT.name + "_walkforward.csv"), index=False)

    # ---------- Q4: KEEP-path census over the whole grid
    print("\n" + "=" * 100)
    print("Q4  KEEP PATHS over every grid row")
    print("=" * 100)
    cen = grid[grid.family != "BENCH"].groupby(["panel", "bps", "family"]).agg(
        n=("Sharpe", "size"), pass4a=("f4a", lambda s: (s == "-").sum()),
        pass4b=("f4b", lambda s: (s == "-").sum()), mean_Sharpe=("Sharpe", "mean"),
        mean_OOS=("OOS_Sharpe", "mean"))
    print(fmt(cen))
    print(f"\nTOTAL: 4a {int((grid[grid.family!='BENCH'].f4a=='-').sum())} / "
          f"{len(grid[grid.family!='BENCH'])}, "
          f"4b {int((grid[grid.family!='BENCH'].f4b=='-').sum())} / {len(grid[grid.family!='BENCH'])}")

    # ---------- Q5: the cost-rung / breakeven column (idea 263)
    print("\n" + "=" * 100)
    print("Q5  COST SENSITIVITY of the v2-vs-CG(g*) comparison (turnovers differ)")
    print("=" * 100)
    for panel in ("u56", "broad"):
        for bps in RUNGS:
            sl = grid[(grid.panel == panel) & (grid.bps == bps)]
            v2 = sl[sl.name == "RULES v2 (live)"].iloc[0]
            cg = sl[(sl.family == "CG") & (sl.g == matched[panel])].iloc[0]
            print(f"  {panel} @{bps:2d}bps: dSharpe(V2-CG*) {v2.Sharpe-cg.Sharpe:+.4f}  "
                  f"dCAGR {100*(v2.CAGR-cg.CAGR):+.2f}pp  dMaxDD {100*(v2.MaxDD-cg.MaxDD):+.2f}pp  "
                  f"turnover {v2.turnover:.2f} vs {cg.turnover:.2f} ({v2.turnover/max(cg.turnover,1e-9):.2f}x)")
        sl0 = grid[(grid.panel == panel) & (grid.bps == 0)]
        v20 = sl0[sl0.name == "RULES v2 (live)"].iloc[0]
        cg0 = sl0[(sl0.family == "CG") & (sl0.g == matched[panel])].iloc[0]
        num = (v20.Sharpe - cg0.Sharpe) * 1e4
        den = v20.turnover / v20.Vol - cg0.turnover / cg0.Vol
        print(f"  {panel} breakeven c* = {num/den if den else float('nan'):.2f} bps "
              f"(idea 262's law; positive = V2 loses the comparison above that rung)")

    print("\nWrote: %s_{grid,headline,nullbands,walkforward}.csv" % OUT.name)


if __name__ == "__main__":
    main()
