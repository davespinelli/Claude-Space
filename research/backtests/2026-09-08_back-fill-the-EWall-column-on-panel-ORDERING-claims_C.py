#!/usr/bin/env python3
"""Idea 460 — back-fill-the-EWall-column-on-the-319-files-that-lack-it (lane C, 2026-09-08).

PRE-REGISTERED QUESTION (QUEUE 460): idea 239 found 319 of 634 committed multi-panel files
publish no un-ranked control.  Take the subset whose headline is a PANEL ORDERING
(U56 > B136 > SMALL439 and friends) and RE-QUOTE each ordering as an EXCESS over that
panel's own EW_ALL.  HOW MANY ORDERINGS SURVIVE THE RESTATEMENT?

WHY THIS IS NOT A REPHRASING OF IDEA 239.  Idea 239 asked whether a panel's LEVEL clears its
own un-ranked control (answer: 83.7% of rows do not).  A panel ORDERING is a DIFFERENCE of
levels, so it is invariant to anything that shifts all panels equally and can survive even
when every level fails.  The restatement subtracts a DIFFERENT constant per panel, so an
ordering flips exactly when the control's own panel-to-panel gap is comparable to the
published gap.  That is a separate, falsifiable question, and the answer below is not
implied by 239's.

TWO TUNED PARAMETERS ONLY (all 6 grid points reported everywhere):
    p1 = control GROSS    g in {0.50, 0.75, 1.00}
    p2 = control CADENCE  f in {W, M}
Everything else is FIXED and pre-registered before any number was read:
    cost rung 10 bps is the verdict rung (PROTOCOL 2); 25 bps is reported beside it as the
      record's standing robustness rung, not as a third dial.  Next-day execution and the
      10 bps cost are the engine's (PROTOCOL 2).  Control = EW_ALL: every name priced that
      day at g/N_priced, no gate, no ranking, no vol filter.  Warm-up 260 rows dropped.
    Panel alias table is idea 239-cloud's, published verbatim below; anything not in it is
      reported UNMAPPED and NEVER guessed.
    The ordering is read at a MATCHED CELL: all published columns that are not the panel
      column and not an outcome column are held fixed, so two panels are only ever compared
      at the same arm of the same grid.  The outcome-column regex is fixed below.
    Ties (two panels quoting the identical number in a cell) are EXCLUDED from the survival
      denominator and reported separately.

DEFINITIONS
    CELL      : one (file, published-Sharpe-column, dial tuple) with >= 2 distinct mapped
                panels.  Its published values induce a RAW ORDERING of those panels.
    EXCESS    : published Sharpe(panel) - Sharpe(EW_ALL on that panel), window-matched
                (FULL/IS/OOS/H1/H2 read off the published column's own name).
    SURVIVES  : the panel permutation induced by EXCESS is IDENTICAL to the one induced by
                the published RAW values.  Pair-level concordance is reported beside it.
    HEADLINE  : the 3-panel cells whose RAW order is exactly u56 > broad136 > small439 —
                the ordering QUEUE 460 names.

PARTS
 A  ARCHIVE: every committed CSV scanned; matched-cell orderings extracted; per-file flag
    for whether the file's own .py/.md publishes an un-ranked control (idea 239's token set),
    so the "files that lack it" subset is reported separately.
 B  RESTATEMENT: survival share, instance-pooled AND file-clustered, with a FILE-BLOCKED
    bootstrap, over all 6 conventions x 2 rungs x 5 windows.
 C  LIVE ORDERING: the same question asked directly, not archivally — price RANKED(n) for
    n in {5,10,20,40} and EW_GATED on the three panels and print the raw and excess
    orderings side by side in every window.
 D  RULE 8 (PROTOCOL 8), both halves of it:
    D1 live: arm chosen on 2009-2016 IS Sharpe per panel, 2017-2026 read ONCE, against the
       do-nothing EW_ALL control, RULES v2 and SPY, with both KEEP paths on every point.
    D2 convention: (g, f) chosen on committed files dated < 2026-09-06, survival share read
       ONCE on files dated >= 2026-09-06.

SURVIVORSHIP: small439 is current constituents of the sub-$2B screen
(data/SMALL_PANEL_README.md); broad136 is current constituents of universe_broad.json
(PROTOCOL 9).  Every panel-level number here is RELATIVE, never achievable.

Outputs (all committed):
    .cells.csv        Part A/B: one row per ordering cell (raw order, excess order, survives)
    .files.csv        Part A: per-file survival, control flag, cell count
    .survival.csv     Part B: the tally by convention x rung x window x subset
    .live.csv         Part C: the live raw/excess orderings
    .walkforward.csv  Part D: D1 rows (live) and D2 rows (convention)
"""
import re
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics                                          # noqa: E402

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
SELF_STEM = Path(__file__).stem

GROSSES = [0.50, 0.75, 1.00]      # p1
FREQS = ["W", "M"]                # p2
RUNGS = [10.0, 25.0]              # fixed: 10 is the verdict rung (PROTOCOL 2)
VERDICT_RUNG = 10.0
VERDICT_G, VERDICT_F = 0.75, "W"  # the record's default control convention (idea 239)
NS = [5, 10, 20, 40]
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
FILE_SPLIT = "2026-09-06"         # D2: files before this are in sample
BOOT = 2000
PANEL_ORDER = ["u56", "broad136", "small439"]

# --- idea 239-cloud's alias table, verbatim.  Not extended: unmapped labels are counted.
ALIAS = {
    "u56": "u56", "U56": "u56", "universe.json": "u56", "universe.json(56)": "u56",
    "U56(56)": "u56", "u56(56)": "u56",
    "broad": "broad136", "B136": "broad136", "BROAD136": "broad136", "broad136": "broad136",
    "universe_broad.json": "broad136", "B136(136)": "broad136",
    "SMALL439": "small439", "small439": "small439", "small": "small439", "SMALL": "small439",
    "SMALL484": "small439", "small484": "small439", "SMALL483": "small439",
}
PANCOL = re.compile(r"(?i)^(panel|universe|univ|panel_name|uni)$")
SHARPE = re.compile(r"(?i)^(sharpe|oos_sharpe|is_sharpe|h1_sharpe|h2_sharpe|"
                    r"sharpe_net|net_sharpe|sharpe10|sharpe25)$")
# outcome columns are never part of the cell key (they are results, not dials)
OUTCOL = re.compile(r"(?i)(sharpe|cagr|maxdd|drawdown|^dd$|^dd_|vol|turn|gross|^h1|^h2|fail|"
                    r"verdict|pass|keep|excess|calmar|sortino|equity|alpha|beta|t_?stat|"
                    r"p_?val|pval|mean|median|std|q10|q90|^start|^end|names|count|^ret|corr|"
                    r"rho|win|share|margin|delta|^d[A-Z]|nobs|n_obs)")
# idea 239's un-ranked-control token set, applied to each file's own source text
CTRL_TOKENS = (r"\bEW[_ -]?ALL\b", r"\bEWall\b", r"\bEWALL\b", r"ew-all", r"ew_all",
               r"un-?ranked", r"unranked", r"equal[- ]weight all", r"\bEWA\b")
ROWCAP = 200_000


def window_of(col: str) -> str:
    c = str(col).upper()
    if c.startswith("OOS"):
        return "OOS"
    if c.startswith("IS"):
        return "IS"
    if c.startswith("H1"):
        return "H1"
    if c.startswith("H2"):
        return "H2"
    return "FULL"


# ---------------------------------------------------------------- machinery (idea 239's)
def freq_mask(idx, freq):
    per = idx.to_period("W" if freq == "W" else "M")
    s = pd.Series(per, index=idx)
    return (s != s.shift(-1)).values


def simulate(px, W, mask):
    """Weights decided at t, applied at t+1; drift between rebalances (== engine.backtest)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], mask[:-1]])
    cur = np.zeros(px.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(len(px))
    for i in range(len(px)):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series((held * rets).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index))


def net(gross, turn, bps):
    return gross - turn * bps / 1e4


def windows(r):
    """The five windows a published Sharpe column can name, all off one return series."""
    h = len(r) // 2
    return dict(FULL=metrics(r)["Sharpe"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                IS=metrics(r.loc[:IS_END])["Sharpe"], OOS=metrics(r.loc[OOS_START:])["Sharpe"])


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_4a(s, b):
    f = []
    if not s["H1"] > b["H1"]: f.append("H1")
    if not s["H2"] > b["H2"]: f.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]: f.append("DD")
    return ",".join(f)


def bars_4b(s, spy, oos_s, oos_spy):
    f = []
    if not s["H1"] > spy["H1"]: f.append("H1")
    if not s["H2"] > spy["H2"]: f.append("H2")
    if not oos_s > oos_spy: f.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: f.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: f.append("CAGR")
    return ",".join(f)


def ew_weights(px, above, g, gated):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(above, 0.0) if gated else ew


def ranked_weights(comp, above, vol20, n, g):
    elig = comp.where(above & (vol20 < MAX_VOL))
    return (elig.rank(axis=1, ascending=False) <= n).astype(float) * (g / n)


# ---------------------------------------------------------------- panels
def build_panels():
    u56 = load_universe()
    b136 = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv", index_col=0)
    sm = load_universe(small=True)
    keep = [c for c in sm.columns if c == "SPY" or meta.max_1d_move.get(c, 0) < 1.0]
    return {"u56": u56, "broad136": b136, "small439": sm[keep]}


def price_controls(panels):
    """The back-fill column itself: EW_ALL Sharpe per (panel, g, f, rung, window)."""
    rows = []
    for pname, px in panels.items():
        univ = px.drop(columns=["SPY"]) if pname == "small439" else px
        above = px > px.rolling(200).mean()          # only used by the gated arm in Part C
        start = px.index[260]
        for g in GROSSES:
            W = ew_weights(univ, above.reindex(columns=univ.columns), g, gated=False)
            W = W.reindex(columns=px.columns).fillna(0.0)
            for f in FREQS:
                gr, tu, hd = simulate(px, W, freq_mask(px.index, f))
                for c in RUNGS:
                    r = net(gr, tu, c).loc[start:]
                    m = metrics(r)
                    rows.append(dict(panel=pname, gross=g, freq=f, bps=c, names=univ.shape[1],
                                     CAGR=m["CAGR"], MaxDD=m["MaxDD"], turn_yr=float(
                                         tu.loc[start:].sum() / (len(r) / 252)),
                                     mean_gross=float(hd.loc[start:].mean()), **windows(r)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- Part A: archive scan
def file_has_control(stem: str) -> bool:
    """Does the file's own source (.py) or memo (.md) name an un-ranked control?"""
    for suf in (".py", ".md", ".result.md"):
        p = BT / (stem + suf)
        if p.exists():
            txt = p.read_text(errors="ignore")
            if any(re.search(t, txt) for t in CTRL_TOKENS):
                return True
    return False


def scan_cells():
    """Every committed CSV -> matched-cell panel orderings.  Nothing is guessed."""
    cells, ledger, unmapped = [], [], {}
    files = sorted(list(BT.glob("*.csv")) + list(BT.glob("*.csv.gz")))
    for f in files:
        if f.name.startswith(SELF_STEM):
            continue
        rec = dict(file=f.name, status="", n_rows=0, n_cells=0)
        try:
            df = pd.read_csv(f, nrows=ROWCAP, low_memory=False)
        except Exception as e:
            rec["status"] = f"unreadable:{type(e).__name__}"
            ledger.append(rec)
            continue
        rec["n_rows"] = len(df)
        pcs = [c for c in df.columns if PANCOL.match(str(c))]
        scs = [c for c in df.columns if SHARPE.match(str(c))]
        if not pcs:
            rec["status"] = "no panel column"
            ledger.append(rec)
            continue
        if not scs:
            rec["status"] = "panel but no Sharpe column"
            ledger.append(rec)
            continue
        pc = pcs[0]
        lab = df[pc].astype(str)
        pan = lab.map(ALIAS)
        for u in lab[pan.isna()].unique():
            unmapped[u] = unmapped.get(u, 0) + int((lab == u).sum())
        if pan.dropna().nunique() < 2:
            rec["status"] = "single mapped panel"
            ledger.append(rec)
            continue
        keys = [str(c) for c in df.columns if str(c) != pc and not OUTCOL.search(str(c))]
        d = df.assign(_p=pan).dropna(subset=["_p"])
        n_here = 0
        for sc in scs:
            v = pd.to_numeric(d[sc], errors="coerce")
            ok = v.notna() & np.isfinite(v) & v.abs().lt(20)
            dd = d[ok.values].assign(_s=v[ok.values])
            if not len(dd):
                continue
            grp = dd.groupby(keys, dropna=False) if keys else [((), dd)]
            for kk, sub in grp:
                per = sub.groupby("_p")._s.agg(["mean", "size"])
                if len(per) < 2:
                    continue
                vals = per["mean"]
                cells.append(dict(file=f.name, stem=f.name.split(".")[0], date=f.name[:10],
                                  col=str(sc), window=window_of(sc), k=len(per),
                                  dup=int((per["size"] > 1).any()),
                                  cell_key=str(kk)[:120],
                                  **{f"s_{p}": float(vals[p]) if p in vals.index else np.nan
                                     for p in PANEL_ORDER}))
                n_here += 1
        rec["n_cells"] = n_here
        rec["status"] = "ADMITTED" if n_here else "no multi-panel cell"
        ledger.append(rec)
    C = pd.DataFrame(cells)
    U = pd.DataFrame(sorted(unmapped.items(), key=lambda x: -x[1]),
                     columns=["label", "n_rows"])
    return C, pd.DataFrame(ledger), U


# ---------------------------------------------------------------- Part B: restatement
def order_of(vals: dict):
    """Descending panel permutation; None if any two values tie exactly."""
    items = [(p, v) for p, v in vals.items() if np.isfinite(v)]
    vs = [v for _, v in items]
    if len(set(vs)) < len(vs):
        return None
    return tuple(p for p, _ in sorted(items, key=lambda x: -x[1]))


def restate(C, ctl, g, f, bps):
    """Attach the excess ordering for one convention.  Returns a copy of C with columns."""
    ref = {(r.panel, w): getattr(r, w)
           for r in ctl[(ctl.gross == g) & (ctl.freq == f) & (ctl.bps == bps)].itertuples()
           for w in ("FULL", "IS", "OOS", "H1", "H2")}
    raws, excs, surv, pair_n, pair_ok = [], [], [], [], []
    for r in C.itertuples():
        vals = {p: getattr(r, f"s_{p}") for p in PANEL_ORDER}
        vals = {p: v for p, v in vals.items() if np.isfinite(v)}
        ex = {p: v - ref[(p, r.window)] for p, v in vals.items()}
        o1, o2 = order_of(vals), order_of(ex)
        raws.append(">".join(o1) if o1 else "")
        excs.append(">".join(o2) if o2 else "")
        surv.append(np.nan if (o1 is None or o2 is None) else float(o1 == o2))
        # pair-level concordance: how many of the k(k-1)/2 pairwise comparisons keep sign
        ps = list(vals)
        n_ok = n_tot = 0
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                a, b = ps[i], ps[j]
                d1, d2 = vals[a] - vals[b], ex[a] - ex[b]
                if d1 == 0 or d2 == 0:
                    continue
                n_tot += 1
                n_ok += int(np.sign(d1) == np.sign(d2))
        pair_n.append(n_tot)
        pair_ok.append(n_ok)
    out = C.copy()
    out["raw_order"] = raws
    out["exc_order"] = excs
    out["survives"] = surv
    out["pairs"] = pair_n
    out["pairs_kept"] = pair_ok
    return out


def boot_file_blocked(df, col="survives", n=BOOT, seed=0):
    """Bootstrap the pooled share, resampling FILES (idea 241's convention).  The pooled
    mean of a resample is sum(sums)/sum(counts), so no array is ever concatenated."""
    rng = np.random.default_rng(seed)
    agg = df.groupby("file")[col].agg(["sum", "count"])
    agg = agg[agg["count"] > 0]
    if len(agg) < 2:
        return (np.nan, np.nan)
    s, k = agg["sum"].values, agg["count"].values.astype(float)
    idx = rng.integers(0, len(s), (n, len(s)))
    out = s[idx].sum(axis=1) / k[idx].sum(axis=1)
    return float(np.quantile(out, 0.025)), float(np.quantile(out, 0.975))


# ---------------------------------------------------------------- Part C/D: live
def live_and_walkforward(panels, ctl):
    live, wf = [], []
    for pname, px in panels.items():
        univ = px.drop(columns=["SPY"]) if pname == "small439" else px
        s_ns, above, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above.astype(float))
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s, spy_w = stats(spy_r), windows(spy_r)
        spy_oos = metrics(spy_r.loc[OOS_START:])
        mask = freq_mask(px.index, VERDICT_F)

        v2g, v2t, _ = simulate(px, rules_v2_weights(px), mask)
        v1g, v1t, _ = simulate(px, rules_v1_weights(px), mask)
        base = {c: stats(net(v2g, v2t, c).loc[start:]) for c in RUNGS}
        base_oos = {c: metrics(net(v2g, v2t, c).loc[OOS_START:]) for c in RUNGS}

        # GATE: the fast path must reproduce engine.backtest exactly on this panel
        eng = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        gate = float(np.abs(eng - net(v1g, v1t, 10.0).loc[start:]).max())

        arms = {}
        Wg = ew_weights(univ, above.reindex(columns=univ.columns), VERDICT_G, gated=True)
        arms["EW_GATED"] = simulate(px, Wg.reindex(columns=px.columns).fillna(0.0), mask)
        Wa = ew_weights(univ, above.reindex(columns=univ.columns), VERDICT_G, gated=False)
        arms["EW_ALL"] = simulate(px, Wa.reindex(columns=px.columns).fillna(0.0), mask)
        for n in NS:
            if n <= univ.shape[1]:
                arms[f"RANKED{n}"] = simulate(px, ranked_weights(
                    comp.reindex(columns=px.columns), above, vol20, n, VERDICT_G), mask)

        for c in RUNGS:
            reads = {}
            for a, (gr, tu, hd) in arms.items():
                r = net(gr, tu, c).loc[start:]
                reads[a] = dict(r=r, st=stats(r), w=windows(r),
                                oos=metrics(r.loc[OOS_START:]),
                                is_=metrics(r.loc[:IS_END]),
                                mean_gross=float(hd.loc[start:].mean()),
                                turn_yr=float(tu.loc[start:].sum() / (len(r) / 252)))
            ctl_w = {w: float(ctl[(ctl.panel == pname) & (ctl.gross == VERDICT_G) &
                                 (ctl.freq == VERDICT_F) & (ctl.bps == c)][w].iloc[0])
                     for w in ("FULL", "IS", "OOS", "H1", "H2")}
            for a, d in reads.items():
                live.append(dict(panel=pname, arm=a, bps=c, gate_max_abs_diff=gate,
                                 CAGR=d["st"]["CAGR"], Sharpe=d["st"]["Sharpe"],
                                 MaxDD=d["st"]["MaxDD"], H1=d["st"]["H1"], H2=d["st"]["H2"],
                                 IS_Sharpe=d["is_"]["Sharpe"], OOS_Sharpe=d["oos"]["Sharpe"],
                                 OOS_CAGR=d["oos"]["CAGR"], OOS_MaxDD=d["oos"]["MaxDD"],
                                 mean_gross=d["mean_gross"], turn_yr=d["turn_yr"],
                                 **{f"exc_{w}": d["w"][w] - ctl_w[w]
                                    for w in ("FULL", "IS", "OOS", "H1", "H2")},
                                 spy_Sharpe=spy_s["Sharpe"], spy_OOS_Sharpe=spy_oos["Sharpe"],
                                 fail4a=bars_4a(d["st"], base[c]),
                                 fail4b=bars_4b(d["st"], spy_s, d["oos"]["Sharpe"],
                                                spy_oos["Sharpe"])))
            # D1: rule 8 — arm picked on IS Sharpe only, OOS read once
            pick = max(reads, key=lambda a: reads[a]["is_"]["Sharpe"])
            p, dn = reads[pick], reads["EW_ALL"]
            wf.append(dict(part="D1_live", panel=pname, bps=c, pick=pick,
                           full_argmax=max(reads, key=lambda a: reads[a]["st"]["Sharpe"]),
                           IS_Sharpe=p["is_"]["Sharpe"], OOS_Sharpe=p["oos"]["Sharpe"],
                           OOS_CAGR=p["oos"]["CAGR"], OOS_MaxDD=p["oos"]["MaxDD"],
                           dn_OOS_Sharpe=dn["oos"]["Sharpe"], dn_OOS_CAGR=dn["oos"]["CAGR"],
                           dn_OOS_MaxDD=dn["oos"]["MaxDD"],
                           v2_OOS_Sharpe=base_oos[c]["Sharpe"], v2_OOS_CAGR=base_oos[c]["CAGR"],
                           v2_OOS_MaxDD=base_oos[c]["MaxDD"],
                           spy_OOS_Sharpe=spy_oos["Sharpe"], spy_OOS_CAGR=spy_oos["CAGR"],
                           spy_OOS_MaxDD=spy_oos["MaxDD"],
                           fail4a=bars_4a(p["st"], base[c]),
                           fail4b=bars_4b(p["st"], spy_s, p["oos"]["Sharpe"],
                                          spy_oos["Sharpe"])))
        print(f"  live {pname:9s} {univ.shape[1]:4d} names  gate {gate:.2e}", flush=True)
    return pd.DataFrame(live), pd.DataFrame(wf)


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    print("=" * 100)
    print("Idea 460 — back-fill the EW_ALL column on the record's PANEL ORDERING claims (lane C)")
    print("=" * 100)

    panels = build_panels()
    print("\nPanels:", {k: v.shape[1] - 1 for k, v in panels.items()})
    ctl = price_controls(panels)
    ctl.to_csv(f"{OUT}.controls.csv", index=False)
    print("\nTHE BACK-FILLED COLUMN — EW_ALL Sharpe by panel and convention (all 6 points, "
          "both rungs):")
    print(ctl[["panel", "gross", "freq", "bps", "names", "CAGR", "MaxDD", "turn_yr",
               "FULL", "H1", "H2", "IS", "OOS"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    piv = ctl[ctl.bps == VERDICT_RUNG].pivot_table(index=["gross", "freq"], columns="panel",
                                                   values="FULL")
    print("\n  panel-to-panel GAPS in the control (this is what the restatement subtracts):")
    gaps = pd.DataFrame({"u56-broad136": piv["u56"] - piv["broad136"],
                         "broad136-small439": piv["broad136"] - piv["small439"],
                         "u56-small439": piv["u56"] - piv["small439"]})
    print(gaps.to_string(float_format=lambda x: f"{x:+.4f}"))

    print(f"\nPART A — scanning committed CSVs ...  ({time.time()-t0:.0f}s)")
    C, led, unm = scan_cells()
    led.to_csv(f"{OUT}.ledger.csv", index=False)
    unm.to_csv(f"{OUT}.unmapped.csv", index=False)
    print(led.status.value_counts().to_string())
    print(f"  ordering cells: {len(C)} over {C.file.nunique()} files "
          f"({C.stem.nunique()} stems); k=3 cells {int((C.k == 3).sum())}, "
          f"k=2 {int((C.k == 2).sum())}; cells with a duplicated panel row "
          f"{int(C.dup.sum())} ({C.dup.mean():.1%}, panel value = mean of its rows).")
    print(f"  UNMAPPED panel labels: {len(unm)} distinct, {int(unm.n_rows.sum())} rows — "
          f"listed in .unmapped.csv, never guessed. Top: "
          f"{', '.join(f'{r.label}({r.n_rows})' for r in unm.head(6).itertuples())}")

    ctrl_flag = {s: file_has_control(s) for s in C.stem.unique()}
    C["own_control"] = C.stem.map(ctrl_flag)
    print(f"  files whose own source names an un-ranked control: "
          f"{sum(ctrl_flag.values())}/{len(ctrl_flag)} stems; "
          f"cells from stems WITHOUT one: {int((~C.own_control).sum())} "
          f"({(~C.own_control).mean():.1%}) — QUEUE 460's subset.")

    print(f"\nPART B — restating every ordering as an excess over EW_ALL ...  "
          f"({time.time()-t0:.0f}s)")
    tally, best = [], None
    for g in GROSSES:
        for f in FREQS:
            for c in RUNGS:
                R = restate(C, ctl, g, f, c)
                if (g, f, c) == (VERDICT_G, VERDICT_F, VERDICT_RUNG):
                    best = R
                for sub_name, sub in (("ALL", R),
                                      ("no_own_control", R[~R.own_control]),
                                      ("has_own_control", R[R.own_control]),
                                      ("k3", R[R.k == 3]),
                                      ("headline_u56>broad136>small439",
                                       R[R.raw_order == "u56>broad136>small439"])):
                    v = sub.survives.dropna()
                    per_file = sub.groupby("file").survives.mean().dropna()
                    tally.append(dict(gross=g, freq=f, bps=c, subset=sub_name,
                                      n_cells=len(v), n_files=len(per_file),
                                      pooled=float(v.mean()) if len(v) else np.nan,
                                      file_clustered=float(per_file.mean())
                                      if len(per_file) else np.nan,
                                      n_tied=int(sub.survives.isna().sum()),
                                      pair_kept=float(sub.pairs_kept.sum() /
                                                      max(sub.pairs.sum(), 1))))
    T = pd.DataFrame(tally)
    T.to_csv(f"{OUT}.survival.csv", index=False)
    best.to_csv(f"{OUT}.cells.csv", index=False)
    best.groupby(["file", "own_control"]).agg(
        n_cells=("survives", "size"), survives=("survives", "mean"),
        pairs=("pairs", "sum"), pairs_kept=("pairs_kept", "sum")
    ).reset_index().to_csv(f"{OUT}.files.csv", index=False)

    print("\nSURVIVAL OF THE PUBLISHED ORDERING UNDER THE RESTATEMENT "
          "(pooled = per cell, file_clustered = mean of per-file shares):")
    print(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print(f"\nVERDICT CONVENTION g={VERDICT_G} {VERDICT_F} @ {VERDICT_RUNG:.0f} bps:")
    for sub_name, sub in (("ALL", best), ("no_own_control", best[~best.own_control]),
                          ("has_own_control", best[best.own_control])):
        v = sub.survives.dropna()
        lo, hi = boot_file_blocked(sub)
        print(f"  {sub_name:18s} n={len(v):6d} cells / {sub.file.nunique():3d} files  "
              f"pooled {v.mean():.4f}  file-clustered "
              f"{sub.groupby('file').survives.mean().mean():.4f}  "
              f"file-blocked 95% CI [{lo:.4f}, {hi:.4f}]")
    print("\n  by window:")
    print(best.groupby("window").survives.agg(["size", "mean"]).to_string(
        float_format=lambda x: f"{x:.4f}"))
    print("\n  by k (number of panels compared in the cell):")
    print(best.groupby("k").survives.agg(["size", "mean"]).to_string(
        float_format=lambda x: f"{x:.4f}"))
    print("\n  RAW orderings the record publishes (top 12) and how often each survives:")
    tb = best.groupby("raw_order").survives.agg(["size", "mean"]).sort_values(
        "size", ascending=False).head(12)
    print(tb.to_string(float_format=lambda x: f"{x:.4f}"))
    print("\n  what the headline ordering u56>broad136>small439 BECOMES under the restatement:")
    hd = best[best.raw_order == "u56>broad136>small439"]
    if len(hd):
        print(hd.exc_order.value_counts().to_string())
    else:
        print("   (no cell publishes that exact 3-panel ordering)")
    print("\n  PAIRWISE sign concordance (a weaker bar than the full permutation):")
    cv = ctl[(ctl.gross == VERDICT_G) & (ctl.freq == VERDICT_F) & (ctl.bps == VERDICT_RUNG)]
    ref = {(r.panel, w): getattr(r, w) for r in cv.itertuples()
           for w in ("FULL", "IS", "OOS", "H1", "H2")}
    for a, b in (("u56", "broad136"), ("broad136", "small439"), ("u56", "small439")):
        m = best[best[f"s_{a}"].notna() & best[f"s_{b}"].notna()]
        if not len(m):
            continue
        ca = m.window.map(lambda w: ref[(a, w)]).values
        cb = m.window.map(lambda w: ref[(b, w)]).values
        d1 = (m[f"s_{a}"] - m[f"s_{b}"]).values
        d2 = d1 - (ca - cb)
        ok = (d1 != 0) & (d2 != 0)
        print(f"    {a:9s} vs {b:9s}  n={len(m):6d}  raw favours {a} in "
              f"{(d1 > 0).mean():.3f}  excess favours {a} in {(d2 > 0).mean():.3f}  "
              f"sign kept under excess "
              f"{float((np.sign(d1[ok]) == np.sign(d2[ok])).mean()):.4f}  "
              f"(control gap {ref[(a, 'FULL')] - ref[(b, 'FULL')]:+.4f})")

    print(f"\nPART C — the same question asked LIVE (not archivally)  ({time.time()-t0:.0f}s)")
    live, wf = live_and_walkforward(panels, ctl)
    live.to_csv(f"{OUT}.live.csv", index=False)
    lv = live[live.bps == VERDICT_RUNG]
    print(lv[["panel", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
              "exc_FULL", "exc_OOS", "mean_gross", "turn_yr", "fail4a", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  LIVE panel ordering per arm, raw vs excess over that panel's EW_ALL:")
    rows = []
    for arm in lv.arm.unique():
        s = lv[lv.arm == arm].set_index("panel")
        for w, col, ecol in (("FULL", "Sharpe", "exc_FULL"), ("OOS", "OOS_Sharpe", "exc_OOS")):
            raw = ">".join(s[col].sort_values(ascending=False).index)
            exc = ">".join(s[ecol].sort_values(ascending=False).index)
            rows.append(dict(arm=arm, window=w, raw_order=raw, exc_order=exc,
                             same=raw == exc))
    LO = pd.DataFrame(rows)
    print(LO.to_string(index=False))
    print(f"  live orderings unchanged by the restatement: "
          f"{int(LO.same.sum())}/{len(LO)}")

    print("\nPART D1 — rule 8 walk-forward, live (IS 2009-2016 -> OOS 2017-2026, read once):")
    d1 = wf[wf.part == "D1_live"]
    print(d1.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"  chooser beats the do-nothing EW_ALL OOS in "
          f"{int((d1.OOS_Sharpe > d1.dn_OOS_Sharpe).sum())}/{len(d1)}; "
          f"beats RULES v2 OOS in {int((d1.OOS_Sharpe > d1.v2_OOS_Sharpe).sum())}/{len(d1)}; "
          f"beats SPY OOS in {int((d1.OOS_Sharpe > d1.spy_OOS_Sharpe).sum())}/{len(d1)}.")
    print(f"  KEEP paths over all {len(live)} live grid points: "
          f"4a {int((live.fail4a == '').sum())}, 4b {int((live.fail4b == '').sum())}.")
    if (live.fail4b == "").any():
        print(live[live.fail4b == ""].to_string(index=False,
                                                float_format=lambda x: f"{x:.3f}"))

    print("\nPART D2 — rule 8 on the CONVENTION (files <", FILE_SPLIT, "in sample):")
    d2 = []
    ins, oos = C.date < FILE_SPLIT, C.date >= FILE_SPLIT
    print(f"  in-sample files {C[ins].file.nunique()} ({int(ins.sum())} cells), "
          f"held-out files {C[oos].file.nunique()} ({int(oos.sum())} cells)")
    for g in GROSSES:
        for f in FREQS:
            R = restate(C, ctl, g, f, VERDICT_RUNG)
            d2.append(dict(part="D2_conv", gross=g, freq=f,
                           IS_share=float(R[ins.values].survives.dropna().mean()),
                           OOS_share=float(R[oos.values].survives.dropna().mean())))
    D2 = pd.DataFrame(d2)
    print(D2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pick = D2.loc[D2.IS_share.idxmax()]
    print(f"  IS-chosen convention: g={pick.gross} {pick.freq} (IS {pick.IS_share:.4f}) "
          f"-> held-out {pick.OOS_share:.4f}; the six conventions span "
          f"{D2.OOS_share.min():.4f}-{D2.OOS_share.max():.4f} out of sample.")
    pd.concat([wf, D2], ignore_index=True).to_csv(f"{OUT}.walkforward.csv", index=False)

    print(f"\nDone in {time.time()-t0:.0f}s. Wrote: " + ", ".join(
        Path(p).name for p in [f"{OUT}.controls.csv", f"{OUT}.ledger.csv",
                               f"{OUT}.unmapped.csv", f"{OUT}.cells.csv", f"{OUT}.files.csv",
                               f"{OUT}.survival.csv", f"{OUT}.live.csv",
                               f"{OUT}.walkforward.csv"]))


if __name__ == "__main__":
    main()
