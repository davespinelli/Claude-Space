#!/usr/bin/env python3
"""Idea 130 — de-gross-vs-reweight-is-not-one-convention   (research sprint, cloud lane, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 130)
    Idea 95 found that `dg` and `rw` are not two readings of one instrument: on ONE book
    (EWall) with ONE gate (vol60) they differ by 1.4 pp of CAGR and 3.6 pp of MaxDD at
    theta=0.40, `rw` wins 4b at TIGHT thresholds where `dg` fails the CAGR floor, and `dg`
    wins at LOOSE ones where `rw` breaches the drawdown cap — i.e. the convention SWAPS WHICH
    4b BAR BINDS.  Re-run the convention axis on every gated book the project has and report
    whether the crossover threshold is STABLE.

    Falsifiable form.  If the crossover is a property of the gate's STRICTNESS (how much of the
    panel it excludes) it should sit at a similar admitted-fraction across gates and books, and
    PROTOCOL can state one number.  If it sits at a different place for every gate, or does not
    exist for most of them, then "the convention" is not one axis at all and no general
    statement is available — only a per-book measurement.

GRID — exactly TWO tuned parameters (gate strictness dial, convention); everything else is a
    reported axis, never selected on.
      5 gates x 5 strictness points x 2 conventions x 3 books x 3 panels x 2 cost rungs.
      gate   native dial (default = the project's published setting, marked *)
        g200    MA window W  in {50, 100, 200*, 300, 400}
        band3   band b (%)   in {0, 2, 3*, 5, 8}   around the 200d MA, sticky
        abs12   lookback L   in {63, 126, 252*, 378, 504}
        vol60   theta        in {0.40, 0.50, 0.60*, 0.80, 1.00}       (idea 95's own dial)
        v1gate  theta        in {0.40, 0.50, 0.60*, 0.80, 1.00}, AND px > 200d MA
      books: V1u (the live rules' 5-name book), TOP20, EWall (the standing 4b candidate).
      panels: universe.json (56), universe_broad.json (136), small (439 sub-$2B names).
      All 900 arm-rows are written to the .grid.csv; the console prints every one.

CONVENTIONS (idea 94's definitions, unchanged)
    dg  gated-out names go to CASH   -> the book de-grosses when the gate excludes a lot.
    rw  the book is rebuilt at full gross among the gated-in names only.
    For EWall these two differ ONLY by the time-varying scaler f_t (the admitted fraction):
    rw_t = dg_t / f_t exactly.  For the RANKED books (V1u, TOP20) they differ in COMPOSITION as
    well, because rw promotes the next-ranked admitted name into the vacated slot.  That
    asymmetry is itself part of the answer and is reported (see the DECOMPOSITION section).

COMMON AXIS
    Each gate's native dial is in different units, so the crossover is located on the one axis
    they share: `adm`, the mean fraction of the panel the gate admits (equivalently the mean
    gross of the dg book / GROSS).  A stable crossover means the same `adm` across gates.

HARNESS
    Idea 94's script is IMPORTED, not re-implemented, so every number sits on the simulator
    that produced the rows being generalised.  `H.gate_mask` is monkeypatched with the
    dial-parameterised version below; CHECK (b) asserts the patched mask reproduces H's own
    mask EXACTLY at each gate's default dial, and CHECK (c) asserts idea 95's published
    EWall+vol60-dg u56 @10bps row.  Costs are derived from one bps=0 run per arm (legitimate
    here because with no stop/DD-control/entry-budget the turnover path is cost-independent);
    CHECK (d) asserts that derivation against a direct bps=10 run.

KEEP PATHS (PROTOCOL rule 4, both evaluated on every row)
    4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.
RULE 8  (dial, convention) chosen on IS Sharpe (<= 2016-12-31) alone, evaluated untouched on
    2017-2026 against the ungated book, RULES v1 and SPY, in every (panel, book, gate, cost).

CAVEATS carried, not buried
    * Survivorship: all three panels are current-constituent lists (idea 54).  The small panel
      additionally drops the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv (bad
      splits), leaving 439 names, and SPY is a joined benchmark there, never a constituent —
      so on the small panel SPY is excluded from every book.  On u56/broad SPY is a genuine
      universe.json constituent and is left in, exactly as ideas 94/95 had it.
    * Idea 38's calendar-day-index warning is checked rather than assumed: CHECK (a).
    * This run measures a CONVENTION, not a new book.  Nothing here can promote a candidate;
      it can only change what the project is allowed to SAY about a published dg/rw row.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import metrics  # noqa: E402

STEM = "2026-09-05_de-gross-vs-reweight-across-gates_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)
_ORIG_MASK = H.gate_mask

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS = ["V1u", "TOP20", "EWall"]
CONVS = ["dg", "rw"]
DIALS = {"g200": [50, 100, 200, 300, 400],
         "band3": [0.0, 2.0, 3.0, 5.0, 8.0],
         "abs12": [63, 126, 252, 378, 504],
         "vol60": [0.40, 0.50, 0.60, 0.80, 1.00],
         "v1gate": [0.40, 0.50, 0.60, 0.80, 1.00]}
DEFAULT = {"g200": 200, "band3": 3.0, "abs12": 252, "vol60": 0.60, "v1gate": 0.60}
GATES = list(DIALS)

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 2000)


# ---------------------------------------------------------------- dial-parameterised gates
def mask_of(px, gate, s):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    if gate == "g200":
        return (px > px.rolling(int(s)).mean()).fillna(False)
    if gate == "band3":
        ma = px.rolling(200).mean()
        if s <= 0:
            return (px > ma).fillna(False)
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + s / 100.0), 1.0)
        raw = raw.mask(px < ma * (1 - s / 100.0), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "abs12":
        return (px > px.shift(int(s))).fillna(False)
    if gate == "vol60":
        return (H.vol20(px) < s).fillna(False)
    if gate == "v1gate":
        return ((px > px.rolling(200).mean()) & (H.vol20(px) < s)).fillna(False)
    raise ValueError(gate)


class Dial:
    """Context manager: make H.targets() see the dial-parameterised gate instead of H's."""
    def __init__(self, px, gate, s):
        self.m = mask_of(px, gate, s)

    def __enter__(self):
        H.gate_mask = lambda px, gate: (pd.DataFrame(True, index=px.index, columns=px.columns)
                                        if gate is None else self.m)
        return self

    def __exit__(self, *a):
        H.gate_mask = _ORIG_MASK


# ---------------------------------------------------------------- panels
def panel(which):
    if which == "u56":
        px = load_universe()
        return px, list(px.columns)                       # SPY is a genuine constituent here
    if which == "broad":
        px = load_universe(broad=True)
        return px, list(px.columns)
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px = px.drop(columns=[c for c in px.columns if c in bad])
    return px, [c for c in px.columns if c != "SPY"]      # benchmark only, never held


def check_index(px, label):
    wk = int((px.index.dayofweek >= 5).sum())
    ch = px.pct_change()
    flat = int(((ch.abs() < 1e-12).sum(axis=1) / px.notna().sum(axis=1) > 0.7).sum())
    print(f"CHECK (a) index {label}: {len(px)} rows, weekend {wk}, >70%-flat {flat} -> "
          f"{'TRADING-DAY CLEAN' if wk == 0 and flat == 0 else 'CALENDAR ARTEFACT'}")


def targets(px, names, book, gate, s, conv):
    """H's book construction on the tradable columns only, reindexed back onto px."""
    sub = px[names]
    with Dial(sub, gate, s):
        W = H.targets(sub, book, gate, conv)
    return W.reindex(columns=px.columns).fillna(0.0)


def stats(r, bars, v1r):
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    h1, h2 = H.halves(r)
    marg = dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=0.60 * bars["absdd"] - abs(m["MaxDD"]), CAGR=m["CAGR"] - 0.70 * bars["cagr"])
    fail = [k for k in ("H1", "H2", "OOS", "DD", "CAGR") if marg[k] <= 0]
    vh1, vh2 = H.halves(v1r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                pass4a=bool(h1 > vh1 and h2 > vh2 and m["MaxDD"] >= metrics(v1r)["MaxDD"]),
                pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-",
                binds=",".join(fail) or "-")


def crossover(sub, col="dSharpe"):
    """First dial value (interpolated on adm) at which rw-minus-dg changes sign."""
    sub = sub.sort_values("adm")
    v, a, d = sub[col].values, sub["adm"].values, sub["dial"].values
    for i in range(len(v) - 1):
        if np.isfinite(v[i]) and np.isfinite(v[i + 1]) and v[i] * v[i + 1] < 0:
            w = abs(v[i]) / (abs(v[i]) + abs(v[i + 1]))
            return a[i] + w * (a[i + 1] - a[i]), d[i], d[i + 1]
    return np.nan, np.nan, np.nan


# ---------------------------------------------------------------- one panel
def do_panel(which):
    px, names = panel(which)
    print("\n" + "=" * 210)
    print(f"PANEL {which}: {len(names)} tradable of {px.shape[1]} columns | "
          f"{px.index[0].date()} -> {px.index[-1].date()}")
    check_index(px, which)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy)
    s1, s2 = H.halves(spy)
    bars = dict(s1=s1, s2=s2, soos=metrics(spy.loc[OOS_START:])["Sharpe"],
                absdd=abs(ms["MaxDD"]), cagr=ms["CAGR"])
    v1 = {c: H.run(px, rules_v1_weights(px), bps=c)["r"].loc[start:] for c in COSTS}
    print(f"eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {s1:.3f}/{s2:.3f}  OOS {bars['soos']:.3f}")
    print(f"4b bars: Sharpe > {s1:.3f}/{s2:.3f}/{bars['soos']:.3f}, MaxDD <= "
          f"{0.60*bars['absdd']:.2%}, CAGR >= {0.70*bars['cagr']:.2%}")

    # ---- CHECK (b): patched mask reproduces H's at each default dial
    for g in GATES:
        a = mask_of(px[names], g, DEFAULT[g])
        b = _ORIG_MASK(px[names], g)
        eq = bool((a == b).all().all())
        print(f"CHECK (b) mask {g} @default {DEFAULT[g]}: {'EXACT' if eq else 'MISMATCH — UNSAFE'}")

    rows, rets = [], {}
    # ---- ungated controls
    for book in BOOKS:
        Wc = targets(px, names, book, None, None, "dg")
        out = H.run(px, Wc, bps=0.0)
        rg, to = out["r"].loc[start:], out["to"].loc[start:]
        if book == "EWall" and which == "u56":
            d10 = H.run(px, Wc, bps=10.0)["r"].loc[start:]
            print(f"CHECK (d) cost derivation, ungated EWall: max|diff| = "
                  f"{float(((rg - to*10.0/1e4) - d10).abs().max()):.3e}")
        for c in COSTS:
            r = rg - to * c / 1e4
            rets[(book, "control", np.nan, "control", c)] = r
            rows.append(dict(panel=which, book=book, gate="none", dial=np.nan, conv="control",
                             cost=c, adm=1.0, turn=float(to.sum() / (len(r) / 252.0)),
                             gross=float(out["gross"].loc[start:].mean()),
                             nheld=float((Wc.loc[start:] > 0).sum(axis=1).mean()),
                             **stats(r, bars, v1[c])))
    for c in COSTS:
        rows.append(dict(panel=which, book="RULESv1", gate="none", dial=np.nan, conv="control",
                         cost=c, adm=np.nan, turn=np.nan, gross=np.nan, nheld=np.nan,
                         **stats(v1[c], bars, v1[c])))

    # ---- CHECK (c): idea 95's published row
    if which == "u56":
        W = targets(px, names, "EWall", "vol60", 0.60, "dg")
        m = metrics(H.run(px, W, bps=10.0)["r"].loc[start:])
        print(f"CHECK (c) EWall+vol60-dg u56 @10bps: CAGR {m['CAGR']:.1%} (pub 11.6%)  "
              f"Sharpe {m['Sharpe']:.3f} (pub 1.133)  MaxDD {m['MaxDD']:.1%} (pub -16.9%)")

    # ---- the grid
    for gate in GATES:
        for s in DIALS[gate]:
            adm = float(mask_of(px[names], gate, s).loc[start:].mean(axis=1).mean())
            for book in BOOKS:
                for conv in CONVS:
                    W = targets(px, names, book, gate, s, conv)
                    out = H.run(px, W, bps=0.0)
                    rg, to = out["r"].loc[start:], out["to"].loc[start:]
                    for c in COSTS:
                        r = rg - to * c / 1e4
                        rets[(book, gate, s, conv, c)] = r
                        rows.append(dict(panel=which, book=book, gate=gate, dial=float(s),
                                         conv=conv, cost=c, adm=adm,
                                         turn=float(to.sum() / (len(r) / 252.0)),
                                         gross=float(out["gross"].loc[start:].mean()),
                                         nheld=float((W.loc[start:] > 0).sum(axis=1).mean()),
                                         **stats(r, bars, v1[c])))
    df = pd.DataFrame(rows)
    cols = ["book", "gate", "dial", "conv", "cost", "adm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "turn", "gross", "nheld", "pass4a", "pass4b", "binds"]
    print(f"\nGRID {which} — ALL {len(df)} rows")
    print(df[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- the convention axis: rw minus dg, along each gate's dial
    print(f"\nCONVENTION AXIS {which} — (rw - dg) along each gate's strictness dial")
    pairs = []
    for (book, gate, c), sub in df[df.conv.isin(CONVS)].groupby(["book", "gate", "cost"]):
        p = sub.pivot_table(index=["dial", "adm"], columns="conv",
                            values=["CAGR", "Sharpe", "MaxDD"]).reset_index()
        p.columns = ["dial", "adm"] + [f"{a}_{b}" for a, b in p.columns[2:]]
        p["panel"], p["book"], p["gate"], p["cost"] = which, book, gate, c
        p["dSharpe"] = p["Sharpe_rw"] - p["Sharpe_dg"]
        p["dCAGR_pp"] = (p["CAGR_rw"] - p["CAGR_dg"]) * 100
        p["dMaxDD_pp"] = (abs(p["MaxDD_dg"]) - abs(p["MaxDD_rw"])) * 100   # + = rw draws down LESS
        b_dg = sub[sub.conv == "dg"].set_index("dial")["binds"]
        b_rw = sub[sub.conv == "rw"].set_index("dial")["binds"]
        p["binds_dg"] = p.dial.map(b_dg)
        p["binds_rw"] = p.dial.map(b_rw)
        p["swap"] = (p.binds_dg != p.binds_rw)
        p["p4b_dg"] = p.dial.map(sub[sub.conv == "dg"].set_index("dial")["pass4b"])
        p["p4b_rw"] = p.dial.map(sub[sub.conv == "rw"].set_index("dial")["pass4b"])
        pairs.append(p)
    P = pd.concat(pairs, ignore_index=True)
    pc = ["book", "gate", "cost", "dial", "adm", "Sharpe_dg", "Sharpe_rw", "dSharpe",
          "dCAGR_pp", "dMaxDD_pp", "p4b_dg", "p4b_rw", "binds_dg", "binds_rw", "swap"]
    print(P[pc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- crossover location
    print(f"\nCROSSOVER {which} — admitted fraction at which sign(rw - dg) flips on Sharpe")
    xr = []
    for (book, gate, c), sub in P.groupby(["book", "gate", "cost"]):
        a, d0, d1 = crossover(sub)
        xr.append(dict(panel=which, book=book, gate=gate, cost=c, adm_star=a,
                       between_dials=f"{d0}->{d1}" if np.isfinite(d0) else "-",
                       sign_at_tightest=np.sign(sub.sort_values("adm").dSharpe.iloc[0]),
                       sign_at_loosest=np.sign(sub.sort_values("adm").dSharpe.iloc[-1]),
                       rng_dSharpe=float(sub.dSharpe.max() - sub.dSharpe.min())))
    X = pd.DataFrame(xr)
    print(X.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- rule 8
    print(f"\nRULE 8 WALK-FORWARD {which} — (dial, conv) on IS Sharpe only, OOS untouched")
    wf = []
    for (book, gate, c), sub in df[df.conv.isin(CONVS)].groupby(["book", "gate", "cost"]):
        p = sub.sort_values("IS_Sharpe", ascending=False).iloc[0]
        ro = rets[(book, gate, p.dial, p.conv, c)].loc[OOS_START:]
        mo = metrics(ro)
        co = metrics(rets[(book, "control", np.nan, "control", c)].loc[OOS_START:])
        vo, so = metrics(v1[c].loc[OOS_START:]), metrics(spy.loc[OOS_START:])
        wf.append(dict(panel=which, book=book, gate=gate, cost=c,
                       pick=f"{p.dial:g}/{p.conv}", conv=p.conv, IS_Sharpe=p.IS_Sharpe,
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       OOS_rank=int((sub.OOS_Sharpe > mo["Sharpe"]).sum()) + 1, n_arms=len(sub),
                       conv_right=bool(mo["Sharpe"] >= sub.OOS_Sharpe.max() - 1e-12),
                       beat_ctl=bool(mo["Sharpe"] > co["Sharpe"]), ctl_Sharpe=co["Sharpe"],
                       beat_SPY=bool(mo["Sharpe"] > so["Sharpe"]), spy_Sharpe=so["Sharpe"],
                       v1_Sharpe=vo["Sharpe"],
                       rho=H.spearman(sub.IS_Sharpe.values, sub.OOS_Sharpe.values)))
    W = pd.DataFrame(wf)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return df, P, X, W


def main():
    print(__doc__)
    D, PP, XX, WW = [], [], [], []
    for which in ("u56", "broad", "small"):
        d, p, x, w = do_panel(which)
        D.append(d); PP.append(p); XX.append(x); WW.append(w)
    D = pd.concat(D, ignore_index=True); P = pd.concat(PP, ignore_index=True)
    X = pd.concat(XX, ignore_index=True); W = pd.concat(WW, ignore_index=True)
    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P.to_csv(OUT / f"{STEM}.convention.csv", index=False)
    X.to_csv(OUT / f"{STEM}.crossover.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    print("\n" + "=" * 210)
    print("ANSWER 1 — is the crossover STABLE?")
    have = X.dropna(subset=["adm_star"])
    print(f"  cells with a sign change on the dial: {len(have)} of {len(X)}"
          f"  ({len(have)/len(X):.0%})")
    if len(have):
        print(f"  adm* over those cells: mean {have.adm_star.mean():.3f}  sd {have.adm_star.std():.3f}"
              f"  min {have.adm_star.min():.3f}  max {have.adm_star.max():.3f}")
        print("\n  adm* by gate (is it a gate property?):")
        print(have.groupby("gate").adm_star.agg(["count", "mean", "std", "min", "max"])
              .to_string(float_format=lambda x: f"{x:.3f}"))
        print("\n  adm* by book (or a book property?):")
        print(have.groupby("book").adm_star.agg(["count", "mean", "std", "min", "max"])
              .to_string(float_format=lambda x: f"{x:.3f}"))
        print("\n  adm* by panel:")
        print(have.groupby("panel").adm_star.agg(["count", "mean", "std", "min", "max"])
              .to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  cells monotone in the convention (no crossover), by direction:")
    mono = X[X.adm_star.isna()]
    print(f"    rw wins throughout: {int((mono.sign_at_tightest > 0).sum())}   "
          f"dg wins throughout: {int((mono.sign_at_tightest < 0).sum())}")

    print("\nANSWER 2 — does the convention SWAP which 4b bar binds (idea 95's claim)?")
    print(f"  rows where binds_dg != binds_rw: {int(P.swap.sum())} of {len(P)} "
          f"({P.swap.mean():.0%})")
    print("  by book:")
    print(P.groupby("book").swap.agg(["count", "sum", "mean"]).to_string(float_format=lambda x: f"{x:.3f}"))
    print("  by gate:")
    print(P.groupby("gate").swap.agg(["count", "sum", "mean"]).to_string(float_format=lambda x: f"{x:.3f}"))
    d_only = P[(P.p4b_dg) & (~P.p4b_rw)]
    r_only = P[(~P.p4b_dg) & (P.p4b_rw)]
    print(f"  rows where the CONVENTION ALONE decides 4b: dg-only {len(d_only)}, rw-only {len(r_only)}, "
          f"both {int((P.p4b_dg & P.p4b_rw).sum())}, neither {int((~P.p4b_dg & ~P.p4b_rw).sum())} "
          f"of {len(P)}")
    if len(d_only):
        print("    dg-only rows:")
        print(d_only[["panel", "book", "gate", "cost", "dial", "adm", "binds_rw"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    if len(r_only):
        print("    rw-only rows:")
        print(r_only[["panel", "book", "gate", "cost", "dial", "adm", "binds_dg"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\nANSWER 3 — size of the convention effect vs the size of the gate choice")
    print("  |rw - dg| Sharpe, by book (EWall: pure gross scaler; ranked: gross AND composition):")
    print(P.assign(ad=P.dSharpe.abs()).groupby("book").ad
          .agg(["count", "mean", "median", "max"]).to_string(float_format=lambda x: f"{x:.3f}"))
    print("  |rw - dg| Sharpe, by gate:")
    print(P.assign(ad=P.dSharpe.abs()).groupby("gate").ad
          .agg(["count", "mean", "median", "max"]).to_string(float_format=lambda x: f"{x:.3f}"))
    print("  spread ACROSS gates at the default dial, same book/conv (the comparison size):")
    g = D[(D.conv.isin(CONVS))]
    dflt = g[[abs(r.dial - DEFAULT[r.gate]) < 1e-9 for r in g.itertuples()]]
    sp = (dflt.groupby(["panel", "book", "conv", "cost"]).Sharpe.agg(lambda s: s.max() - s.min()))
    print(f"    across-gate Sharpe spread: mean {sp.mean():.3f}, median {sp.median():.3f}, "
          f"max {sp.max():.3f}  |  convention effect mean {P.dSharpe.abs().mean():.3f}")

    print("\nANSWER 4 — rule 8: does the walk-forward pick the right convention?")
    print(f"  picks rw in {int((W.conv=='rw').sum())} of {len(W)} cells; "
          f"the pick is the OOS-best arm in {int(W.conv_right.sum())} of {len(W)}; "
          f"beats the ungated control in {int(W.beat_ctl.sum())}; beats SPY in {int(W.beat_SPY.sum())}")
    print(W.groupby(["panel", "book"]).agg(rw_picks=("conv", lambda s: int((s == 'rw').sum())),
                                           n=("conv", "size"),
                                           beat_ctl=("beat_ctl", "sum"),
                                           mean_rho=("rho", "mean")).to_string())
    print("=" * 210)


if __name__ == "__main__":
    main()
