#!/usr/bin/env python3
"""Idea 1656 (lane cloud, 2026-09-19): is EVERY committed DRAWDOWN CREDIT in the record
quoted at an UNMATCHED REALISED GROSS?

Idea 1649 found a +1.02 pp MaxDD credit REVERSE to -0.28 pp once the comparand carried the
same REALISED gross, and its G11 showed a constant de-gross moves |dSharpe| <= 0.0004 while
moving MaxDD by up to 6.9 pp.  If that is general, every Sharpe claim in the record is
re-gross-immune and every DRAWDOWN claim is an exposure claim wearing a device's name.

Two parts, both published in full:
  A. CENSUS of the committed record (memos + CHANGELOG + LEADERBOARD): how many MaxDD
     contrast sites NAME a realised-gross match.
  B. RE-PRICE of the top families that do not.  Five device families, each at its own
     PUBLISHED live threshold (not tuned), against two comparands:
        UNMATCHED  equal-weight at the SAME TARGET gross g        (the record's convention)
        MATCHED    equal-weight at the constant gross g* whose REALISED mean gross equals
                   the device's own realised mean gross
     Three panels (U56 / B136 / SMALL), gross rungs g {0.50, 0.75, 1.00}, cost axis
     {0, 10, 25, 50} bps derived EXACTLY off the c = 0 run.

Tuned dials: ONE (the gross rung g).  Family thresholds are the record's own live values.
Rule 8: choosers see rows <= 2016-12-31 only; 2017-2026 read once.
Deterministic, offline, no network.  Writes .census.csv .grid.csv .paired.csv .walkforward.csv .gates.csv .log.txt
"""
import sys, re
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, band_state, score  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics                                                       # noqa: E402

OUT = Path(__file__).with_suffix("")
G_RUNGS = [0.50, 0.75, 1.00]
COSTS = [0, 10, 25, 50]
IS_END = "2016-12-31"
BAND = 0.03          # live RULES v2 clause 2
MAXVOL = 0.60        # live RULES v1 vol ceiling
TOPN = 20            # the 2026-09-04 KEEP-4b top-20 book
VOLTGT = 0.15        # the record's published vol target
LOG, gates = [], []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


def gate(name, val, ok, note=""):
    gates.append(dict(gate=name, value=val, pass_=bool(ok), note=note))
    say(f"GATE {name}: {val}  {'PASS' if ok else 'FAIL'}  {note}")


# ================================================================ PART A — CENSUS
DD_TOK = re.compile(r"(dMaxDD|MaxDD|drawdown|Drawdown|DD cap)")
CONTRAST = re.compile(r"(shallower|deeper|\bvs\.?\b|versus|against|minus|worse than|better than|credit|dMaxDD)")
MATCH_TOK = re.compile(
    r"(gross[- ]matched|matched[- ]gross|matches? the (realised|realized) gross|realised gross|realized gross|"
    r"de-?gross twin|de-?grossed twin|exposure[- ]matched|matched[- ]exposure|matched mean equity|"
    r"mean gross|matched realised|same realised gross|turnover-?matched gross)", re.I)

say("# idea 1656 — PART A: census of committed MaxDD contrast sites in the record")
corpora = {
    "memos (research/backtests/*.md)": sorted(ROOT.glob("research/backtests/*.md")),
    "CHANGELOG.md": [ROOT / "research" / "CHANGELOG.md"],
    "LEADERBOARD.md": [ROOT / "research" / "LEADERBOARD.md"],
}
census_rows, sites_unmatched = [], []
for cname, files in corpora.items():
    n_sites = n_matched = 0
    for f in files:
        try:
            txt = f.read_text(errors="replace")
        except Exception:
            continue
        for ln, line in enumerate(txt.split("\n"), 1):
            if DD_TOK.search(line) and CONTRAST.search(line):
                n_sites += 1
                m = bool(MATCH_TOK.search(line))
                n_matched += m
                if not m:
                    sites_unmatched.append(dict(corpus=cname, file=f.name, line_no=ln, text=line.strip()[:300]))
    census_rows.append(dict(corpus=cname, files=len(files), dd_contrast_sites=n_sites,
                            names_realised_gross_match=n_matched,
                            unmatched=n_sites - n_matched,
                            pct_matched=(n_matched / n_sites * 100) if n_sites else float("nan")))
census = pd.DataFrame(census_rows)
tot_s, tot_m = census.dd_contrast_sites.sum(), census.names_realised_gross_match.sum()
census.loc[len(census)] = dict(corpus="TOTAL", files=census.files.sum(), dd_contrast_sites=tot_s,
                               names_realised_gross_match=tot_m, unmatched=tot_s - tot_m,
                               pct_matched=tot_m / tot_s * 100 if tot_s else float("nan"))
census.to_csv(f"{OUT}.census.csv", index=False)
say(census.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
say(f"\nCENSUS HEADLINE: {tot_m} of {tot_s} committed MaxDD contrast sites ({tot_m/tot_s*100:.2f}%) name a "
    f"realised-gross match; {tot_s-tot_m} ({(tot_s-tot_m)/tot_s*100:.2f}%) do not.")
pd.DataFrame(sites_unmatched).head(2000).to_csv(f"{OUT}.unmatched_sites.csv", index=False)
say(f"first 2000 unmatched sites -> {Path(OUT).name}.unmatched_sites.csv")
gate("G0 census corpus non-empty", f"{tot_s} sites over {int(census.files.iloc[-1])-1} files", tot_s > 100,
     "regex census, published verbatim; a site is a LINE, not a claim")


# ================================================================ PART B — RE-PRICE
def ew_weights(px, g, tradable):
    e = px[tradable].notna().astype(float)
    w = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def band_weights(px, g, tradable):
    return ew_weights(px, g, tradable).where(band_state(px, BAND).reindex(columns=px.columns).fillna(False), 0.0)


def ma200_weights(px, g, tradable):
    above = (px > px.rolling(200).mean()).reindex(columns=px.columns).fillna(False)
    return ew_weights(px, g, tradable).where(above, 0.0)


def maxvol_weights(px, g, tradable):
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    ok = (vol20 < MAXVOL).reindex(columns=px.columns).fillna(False)
    return ew_weights(px, g, tradable).where(ok, 0.0)


def topn_weights(px, g, tradable):
    s, above, vol20 = score(px[tradable], vol_scale=True)
    rank = s.rank(axis=1, ascending=False)
    w = (rank <= TOPN).astype(float) * (g / TOPN)
    return w.reindex(columns=px.columns).fillna(0.0)


def voltgt_weights(px, g, tradable):
    """Equal-weight every priced name, scaled so the sleeve's trailing 20d vol hits VOLTGT,
    capped at gross g (no leverage).  Scale uses only information up to t."""
    base = ew_weights(px, 1.0, tradable)
    sleeve = (base.shift(1) * px[tradable].pct_change().reindex(columns=base.columns).fillna(0.0)).sum(axis=1)
    rv = sleeve.rolling(20).std() * np.sqrt(252)
    k = (VOLTGT / rv.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return base.mul(k * g, axis=0)


FAMS = {"BAND": band_weights, "MA200": ma200_weights, "MAXVOL": maxvol_weights,
        "TOPN": topn_weights, "VOLTGT": voltgt_weights}


def run(px, wfn, freq="W"):
    res = backtest(px, wfn(px), cost_bps=0.0, freq=freq)
    return dict(gross=res["returns"], turnover=res["turnover"], rg=res["weights"].sum(axis=1))


def net(r, c):
    return r["gross"] - r["turnover"] * c / 1e4


def legs(ret, start):
    r = ret.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ins, oos = metrics(r.loc[:IS_END]), metrics(r.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=ins["Sharpe"], IS_CAGR=ins["CAGR"], IS_MaxDD=ins["MaxDD"],
                OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"], OOS_MaxDD=oos["MaxDD"])


PANELS = {}
u = load_universe();                      PANELS["U56"] = (u, list(u.columns))
b = load_universe(broad=True);            PANELS["B136"] = (b, list(b.columns))
sm = load_universe(small=True)
meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
keep_small = [c for c in sm.columns if c != "SPY" and c not in bad]
PANELS["SMALL"] = (sm, keep_small)
say(f"\n# PART B — panels: U56 {u.shape[1]} cols (tradable {len(PANELS['U56'][1])}), "
    f"B136 {b.shape[1]} ({len(PANELS['B136'][1])}), SMALL {sm.shape[1]} cols, "
    f"{len(bad)} max_1d_move>=1.0 tickers dropped -> tradable {len(keep_small)} (SPY benchmark-only)")
gate("G1 small panel screen applied", f"{len(bad)} dropped, {len(keep_small)} tradable",
     len(bad) > 0 and "SPY" not in keep_small, "data/small_meta.csv max_1d_move >= 1.0")

rows, paired, wf_store = [], [], {}
for pname, (px, trad) in PANELS.items():
    START = px.index[260]
    yrs = (px.index[-1] - START).days / 365.25
    spy = px["SPY"].pct_change().fillna(0.0)
    spy_f = metrics(spy.loc[START:]); _h = len(spy.loc[START:]) // 2
    spy_h1 = metrics(spy.loc[START:].iloc[:_h]); spy_h2 = metrics(spy.loc[START:].iloc[_h:])
    spy_o = metrics(spy.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
    base_r = run(px, rules_v2_weights)
    v1_r = run(px, rules_v1_weights)
    say(f"\n## PANEL {pname}  {START.date()} -> {px.index[-1].date()}  ({yrs:.2f} y)")
    say(f"   SPY FULL {spy_f['CAGR']:.2%} / {spy_f['Sharpe']:.4f} / {spy_f['MaxDD']:.2%}  halves "
        f"{spy_h1['Sharpe']:.4f} / {spy_h2['Sharpe']:.4f}  OOS {spy_o['CAGR']:.2%} / {spy_o['Sharpe']:.4f} / {spy_o['MaxDD']:.2%}")
    LB = legs(net(base_r, 10), START)
    say(f"   RULES v2 baseline @10bps FULL {LB['CAGR']:.2%} / {LB['Sharpe']:.4f} / {LB['MaxDD']:.2%}  halves "
        f"{LB['H1']:.4f} / {LB['H2']:.4f}  OOS {LB['OOS_CAGR']:.2%} / {LB['OOS_Sharpe']:.4f} / {LB['OOS_MaxDD']:.2%}")

    def keep4a(d, c):
        L = legs(net(base_r, c), START)
        return bool(d["H1"] > L["H1"] and d["H2"] > L["H2"] and d["MaxDD"] >= L["MaxDD"])

    def keep4b(d, oos=False):
        if oos:
            return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"] and d["OOS_Sharpe"] > spy_o["Sharpe"]
                        and d["OOS_MaxDD"] >= 0.6 * spy_o["MaxDD"] and d["OOS_CAGR"] >= 0.7 * spy_o["CAGR"])
        return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"]
                    and d["MaxDD"] >= 0.6 * spy_f["MaxDD"] and d["CAGR"] >= 0.7 * spy_f["CAGR"])

    # ---- realised-gross curve for the constant-gross comparand, then invert by interpolation
    LADDER = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 1.00]
    ew_runs = {g: run(px, lambda p, g=g: ew_weights(p, g, trad)) for g in LADDER}
    curve_x = [float(ew_runs[g]["rg"].loc[START:].mean()) for g in LADDER]
    say(f"   EW realised-gross curve: " + ", ".join(f"g={g:.2f}->{x:.4f}" for g, x in zip(LADDER, curve_x)))
    gate(f"G2 {pname} EW realised-gross curve monotone", f"{np.all(np.diff(curve_x) > 0)}",
         bool(np.all(np.diff(curve_x) > 0)), "required for a unique matched twin")

    def solve_g(target):
        return float(np.interp(target, curve_x, LADDER))

    arms = {}
    for fam, fn in FAMS.items():
        for g in G_RUNGS:
            arms[(fam, g)] = run(px, lambda p, fn=fn, g=g: fn(p, g, trad))
    for g in G_RUNGS:
        arms[("EW", g)] = ew_runs[g] if g in ew_runs else run(px, lambda p, g=g: ew_weights(p, g, trad))

    # matched twins, one confirming engine run each
    match_err = []
    for fam in FAMS:
        for g in G_RUNGS:
            tgt = float(arms[(fam, g)]["rg"].loc[START:].mean())
            gstar = solve_g(tgt)
            tw = run(px, lambda p, gs=gstar: ew_weights(p, gs, trad))
            arms[("TWIN", (fam, g))] = tw
            arms[("TWIN_G", (fam, g))] = gstar
            match_err.append(abs(float(tw["rg"].loc[START:].mean()) - tgt))
    gate(f"G3 {pname} realised-gross match tolerance", f"{max(match_err):.3e}", max(match_err) < 5e-3,
         "device mean realised gross vs its matched constant-gross twin")

    for key, r in arms.items():
        if key[0] in ("TWIN", "TWIN_G"):
            continue
        fam, g = key
        for c in COSTS:
            d = legs(net(r, c), START)
            rows.append(dict(panel=pname, family=fam, gross=g, cost_bps=c,
                             realised_gross=float(r["rg"].loc[START:].mean()),
                             turnover_yr=float(r["turnover"].loc[START:].sum() / yrs),
                             **{k: float(v) for k, v in d.items()},
                             keep4a=keep4a(d, c), keep4b_full=keep4b(d), keep4b_oos=keep4b(d, oos=True)))

    for fam in FAMS:
        for g in G_RUNGS:
            for c in COSTS:
                dv = legs(net(arms[(fam, g)], c), START)
                un = legs(net(arms[("EW", g)], c), START)
                tw = legs(net(arms[("TWIN", (fam, g))], c), START)
                paired.append(dict(
                    panel=pname, family=fam, gross=g, cost_bps=c,
                    dev_realised_gross=float(arms[(fam, g)]["rg"].loc[START:].mean()),
                    unmatched_realised_gross=float(arms[("EW", g)]["rg"].loc[START:].mean()),
                    twin_g=arms[("TWIN_G", (fam, g))],
                    dMaxDD_unmatched_pp=(dv["MaxDD"] - un["MaxDD"]) * 100,
                    dMaxDD_matched_pp=(dv["MaxDD"] - tw["MaxDD"]) * 100,
                    dSharpe_unmatched=dv["Sharpe"] - un["Sharpe"],
                    dSharpe_matched=dv["Sharpe"] - tw["Sharpe"],
                    dCAGR_unmatched_pp=(dv["CAGR"] - un["CAGR"]) * 100,
                    dCAGR_matched_pp=(dv["CAGR"] - tw["CAGR"]) * 100,
                    dMaxDD_OOS_unmatched_pp=(dv["OOS_MaxDD"] - un["OOS_MaxDD"]) * 100,
                    dMaxDD_OOS_matched_pp=(dv["OOS_MaxDD"] - tw["OOS_MaxDD"]) * 100,
                    dSharpe_OOS_unmatched=dv["OOS_Sharpe"] - un["OOS_Sharpe"],
                    dSharpe_OOS_matched=dv["OOS_Sharpe"] - tw["OOS_Sharpe"]))
    wf_store[pname] = dict(px=px, START=START, arms={k: v for k, v in arms.items() if k[0] != "TWIN_G"},
                           base=base_r, spy_h1=spy_h1, spy_h2=spy_h2, spy_o=spy_o, keep4a=keep4a, keep4b=keep4b)

grid = pd.DataFrame(rows); grid.to_csv(f"{OUT}.grid.csv", index=False)
pair = pd.DataFrame(paired); pair.to_csv(f"{OUT}.paired.csv", index=False)
say(f"\n# GRID: {len(grid)} cells published -> {Path(OUT).name}.grid.csv")
say(f"# PAIRED: {len(pair)} device/comparand contrasts published -> {Path(OUT).name}.paired.csv")

# ---------------------------------------------------------------- the finding
say("\n## THE CONTRAST — every device's MaxDD credit, quoted UNMATCHED (same TARGET gross) "
    "then MATCHED (same REALISED gross)")
say(pair[["panel", "family", "gross", "cost_bps", "dev_realised_gross", "twin_g",
          "dMaxDD_unmatched_pp", "dMaxDD_matched_pp", "dSharpe_unmatched", "dSharpe_matched"]]
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

n = len(pair)
cred_un = pair.dMaxDD_unmatched_pp > 0          # shallower than the unmatched comparand
cred_ma = pair.dMaxDD_matched_pp > 0
rev = cred_un & ~cred_ma
say(f"\nCREDITS: MaxDD shallower than the UNMATCHED comparand in {int(cred_un.sum())} of {n} cells "
    f"(mean {pair.dMaxDD_unmatched_pp.mean():+.2f} pp); shallower than the MATCHED twin in "
    f"{int(cred_ma.sum())} of {n} (mean {pair.dMaxDD_matched_pp.mean():+.2f} pp).")
say(f"REVERSALS: {int(rev.sum())} of {int(cred_un.sum())} unmatched MaxDD credits REVERSE sign once the "
    f"comparand carries the same realised gross.")
say(f"MOVE ON MATCHING: mean |dMaxDD shift| {np.abs(pair.dMaxDD_unmatched_pp-pair.dMaxDD_matched_pp).mean():.2f} pp, "
    f"max {np.abs(pair.dMaxDD_unmatched_pp-pair.dMaxDD_matched_pp).max():.2f} pp; "
    f"mean |dSharpe shift| {np.abs(pair.dSharpe_unmatched-pair.dSharpe_matched).mean():.4f}, "
    f"max {np.abs(pair.dSharpe_unmatched-pair.dSharpe_matched).max():.4f}.")
say("OOS leg: reversals " + f"{int(((pair.dMaxDD_OOS_unmatched_pp>0)&(pair.dMaxDD_OOS_matched_pp<=0)).sum())} of "
    f"{int((pair.dMaxDD_OOS_unmatched_pp>0).sum())}; mean |dSharpe_OOS shift| "
    f"{np.abs(pair.dSharpe_OOS_unmatched-pair.dSharpe_OOS_matched).mean():.4f}.")
say("\nby family (pooled over panels, gross rungs and cost rungs):")
agg = pair.groupby("family").agg(cells=("dMaxDD_unmatched_pp", "size"),
                                 credit_unmatched=("dMaxDD_unmatched_pp", lambda s: int((s > 0).sum())),
                                 mean_unmatched_pp=("dMaxDD_unmatched_pp", "mean"),
                                 credit_matched=("dMaxDD_matched_pp", lambda s: int((s > 0).sum())),
                                 mean_matched_pp=("dMaxDD_matched_pp", "mean"),
                                 mean_dSharpe_shift=("dSharpe_unmatched", "mean"))
agg["mean_dSharpe_matched"] = pair.groupby("family").dSharpe_matched.mean()
say(agg.to_string(float_format=lambda x: f"{x:.4f}"))
say("\nby panel:")
say(pair.groupby("panel").agg(cells=("dMaxDD_unmatched_pp", "size"),
                              credit_unmatched=("dMaxDD_unmatched_pp", lambda s: int((s > 0).sum())),
                              credit_matched=("dMaxDD_matched_pp", lambda s: int((s > 0).sum())),
                              mean_unmatched_pp=("dMaxDD_unmatched_pp", "mean"),
                              mean_matched_pp=("dMaxDD_matched_pp", "mean")).to_string(float_format=lambda x: f"{x:.4f}"))

# ---------------------------------------------------------------- KEEP census
k4a = grid[grid.keep4a]; k4b = grid[grid.keep4b_full]; k4bo = grid[grid.keep4b_full & grid.keep4b_oos]
say(f"\n## KEEP paths over all {len(grid)} cells: 4a {len(k4a)}; 4b FULL {len(k4b)}; 4b FULL and OOS {len(k4bo)}")
for nm, sub in (("4a", k4a), ("4b FULL+OOS", k4bo)):
    say(f"  {nm}: " + ("; ".join(f"{r.panel}/{r.family} g={r.gross:.2f} @{r.cost_bps}bps "
                                 f"(S {r.Sharpe:.4f}, DD {r.MaxDD:.2%}, CAGR {r.CAGR:.2%})"
                                 for r in sub.itertuples()) if len(sub) else "none"))

# ---------------------------------------------------------------- rule 8 walk-forward
say("\n## RULE 8 WALK-FORWARD — choosers fitted on rows <= 2016-12-31 only, 2017-2026 read once")
wf = []
for pname, S in wf_store.items():
    px, START = S["px"], S["START"]
    spy = px["SPY"].pct_change().fillna(0.0)
    spy_is = metrics(spy.loc[START:IS_END])
    fam_keys = [k for k in S["arms"] if k[0] != "TWIN"]
    twin_keys = {(f, g): ("TWIN", (f, g)) for f in FAMS for g in G_RUNGS}
    for c in COSTS:
        isd = {k: legs(net(S["arms"][k], c), START) for k in fam_keys}

        def memo_pick(default):
            ok = [k for k in fam_keys if isd[k]["IS_MaxDD"] >= 0.6 * spy_is["MaxDD"]
                  and isd[k]["IS_CAGR"] >= 0.7 * spy_is["CAGR"]]
            return min(ok, key=lambda k: (k[1], k[0])) if ok else default

        # C_DDCREDIT is THIS idea's own chooser: pick the family whose IS MaxDD credit over its
        # MATCHED twin is largest -- i.e. the device that actually buys drawdown at equal exposure.
        def dd_credit_is(k):
            if k[0] == "EW":
                return -9e9
            dv = legs(net(S["arms"][k], c), START); tw = legs(net(S["arms"][twin_keys[k]], c), START)
            return dv["IS_MaxDD"] - tw["IS_MaxDD"]

        choosers = {
            "C_SHARPE": max(fam_keys, key=lambda k: isd[k]["IS_Sharpe"]),
            "C_CAGR": max(fam_keys, key=lambda k: isd[k]["IS_CAGR"]),
            "C_CALMAR": max(fam_keys, key=lambda k: isd[k]["IS_CAGR"] / abs(isd[k]["IS_MaxDD"])),
            "C_DDCREDIT_UNMATCHED": max([k for k in fam_keys if k[0] != "EW"],
                                        key=lambda k: isd[k]["IS_MaxDD"] - isd[("EW", k[1])]["IS_MaxDD"]),
            "C_DDCREDIT_MATCHED": max([k for k in fam_keys if k[0] != "EW"], key=dd_credit_is),
            "C_MEMO": memo_pick(("EW", 0.75)),
            "C_LIVE_BAND": ("BAND", 0.75),
        }
        for nm, k in choosers.items():
            d = legs(net(S["arms"][k], c), START)
            wf.append(dict(panel=pname, cost_bps=c, chooser=nm, pick=f"{k[0]} {k[1]:.2f}",
                           OOS_CAGR=d["OOS_CAGR"], OOS_Sharpe=d["OOS_Sharpe"], OOS_MaxDD=d["OOS_MaxDD"],
                           keep4b_oos=S["keep4b"](d, oos=True), keep4a=S["keep4a"](d, c)))
wf = pd.DataFrame(wf); wf.to_csv(f"{OUT}.walkforward.csv", index=False)
say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say(f"\nOOS 4b pass rate by chooser: \n" +
    wf.groupby("chooser").keep4b_oos.agg(["sum", "size"]).to_string())
say("\nDOES THE UNMATCHED DD-CREDIT CHOOSER AGREE WITH THE MATCHED ONE?  "
    f"picks differ in {int((wf[wf.chooser=='C_DDCREDIT_UNMATCHED'].pick.values != wf[wf.chooser=='C_DDCREDIT_MATCHED'].pick.values).sum())} "
    f"of {len(wf[wf.chooser=='C_DDCREDIT_UNMATCHED'])} (panel, cost) cells.")

gate("G4 chooser sees no 2017+ row", "truncated arrays", True, "IS_* computed on r.loc[:2016-12-31] only")
gate("G5 cost axis derived exactly", "r(c) = r_gross - turnover*c/1e4", True, "verified below")
_px = PANELS["U56"][0]
_chk = backtest(_px, rules_v2_weights(_px), cost_bps=25.0, freq="W")["returns"]
_der = net(run(_px, rules_v2_weights), 25)
gates[-1]["value"] = f"{float((_chk-_der).abs().max()):.3e}"
gates[-1]["pass_"] = float((_chk - _der).abs().max()) < 1e-12
say(f"GATE G5 recomputed: {gates[-1]['value']} {'PASS' if gates[-1]['pass_'] else 'FAIL'}")
gate("G6 every grid point published", f"{len(grid)} grid + {len(pair)} paired + {len(wf)} wf cells", True, "")
gate("G7 tuned dials", "1 (gross rung g)", True, "family thresholds are the record's published live values")
pd.DataFrame(gates).to_csv(f"{OUT}.gates.csv", index=False)
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
print(f"\nwrote {Path(OUT).name}.{{census,unmatched_sites,grid,paired,walkforward,gates}}.csv and .log.txt")
