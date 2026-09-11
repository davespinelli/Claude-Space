#!/usr/bin/env python3
"""
IDEA 510 -- is-the-86.7-percent-DD-CUT-RATE-a-PANEL-CONSTANT
============================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 500 found that over 244 arm-rows 4a's two Sharpe legs clear the live book only 15 times
  (6.1%) and the MaxDD leg then cuts 13 of those 15 (86.7%), i.e. PROTOCOL 4a is decided by its
  drawdown leg.  Measure the cut rate per panel and per dial on a wider arm corpus and report
  whether 86.7% is a corpus constant or carried by one panel; if it is a constant, 4a's Sharpe
  legs are close to decorative and PROTOCOL should say so.  Max 2 params (panel, dial).

DEFINITIONS (fixed before any number is read)
---------------------------------------------
  SHARPE-CLEAR   an arm whose Sharpe beats the live book (RULES v2) in BOTH halves.
  DD-CUT         a Sharpe-clear whose MaxDD is worse than the live book's, so 4a fails.
  CUT RATE       DD-cuts / Sharpe-clears -- idea 500's 86.7% (13/15).  Undefined where an
                 (panel, dial, cost) cell has no Sharpe-clear; such cells are reported as
                 n=0 and excluded from every rate, never counted as 0% or 100%.
  The complementary reading the queue asks for is reported beside it: CLEAR RATE
  P(clear Sharpe | pass DD) and the SOLE-CUT shares, so "which leg decides 4a" is answered
  from both directions rather than from the cut rate alone.

THE WIDER CORPUS (the queue's ask; no dial is tuned, every rung is reported)
---------------------------------------------------------------------------
  Nine dials, each a one-dimensional sweep through a book form the record already publishes,
  at three cost rungs on three panels.  Idea 500/508's corpus was 6 dials / 122 arms /
  244 arm-rows at 2 rungs; this one is 9 dials / ~250 arms / ~750 arm-rows at 3 rungs, and
  contains idea 500's own six dials as a labelled subset (the `pub` rungs), so the incumbent
  86.7% is re-derivable inside it rather than merely quoted.

    n         CAND-n ranked composite book (with the vol scaler, as idea 500 wrote it)
    band      RULES v2's 200d band book at band b
    gross     RULES v2's band book at gross g
    volcap    gated equal weight with a vol20 cap
    quantile  gated equal weight over the top x fraction of eligible names
    cadence   RULES v2's band book rebalanced D / W / M / Q
    ma        the band book's moving-average length (50..400)            [new in this run]
    nns       CAND-n with NO vol scaler (the KEEP-4b candidate's form)     [new in this run]
    lookback  CAND-20 on a single momentum lookback (21..504 days)       [new in this run]

  TUNED (2, exactly as the queue allows): PANEL (U56 / B136 / SMALL439) and DIAL.  Cost rungs
  (0 / 10 / 25 bps) are a reporting axis, not a tuned one -- every rung is printed.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  fast_run == engine.backtest @10 bps on a dense book                       bar 1e-12
  G2  the live comparand: RULES v2 on U56 @10 bps == the record's 8.61% / 1.1998 / -12.05%
  G3a idea 500's THREE HEADLINE NUMBERS recomputed from idea 508's COMMITTED arms.csv with
      this file's own leg definitions: 244 arm-rows, 15 Sharpe-clears (6.1%), 13 DD-cuts
      (86.7%).  This is the version that ran; the gate as first drafted -- "idea 500's corpus
      is the `pub` subset of this one" -- was MIS-SPECIFIED and is reported as such below
      rather than dropped: idea 500 skipped every `n` rung wider than its panel (U56 6 arms,
      B136 8, SMALL439 9), so the subset is 174 arm-rows, not 244, and no corpus written here
      can reproduce its row count by construction.  G3b replaces its intent.
  G3b on the (panel, dial, arm, cost) rows the two corpora SHARE, every 4a leg agrees --
      the real content of the mis-specified gate, and the reason this run's `n`, `volcap` and
      `quantile` dials keep idea 500's vol-scaled composite convention exactly.
  G4  the cost rungs are one gross stream minus turnover x c/1e4                bar 1e-15
  G5  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G6  the 4a legs are read as PROTOCOL writes them: MaxDD leg is `arm >= base` (a tie PASSES),
      verified on a book compared against itself (every leg ties, 4a passes)

RULE 8 (PROTOCOL 8, required)
-----------------------------
  Two walk-forward reads, both with 2009-2016 used for choosing and 2017-2026 read once:
  (a) DOES THE CUT RATE WALK FORWARD -- the cut rate is recomputed on the IS window alone and
      on the OOS window alone, per panel and per dial, and the two are compared; a corpus
      constant should survive the split.
  (b) THE ARM PICK -- per panel and cost rung, the arm with the highest IS Sharpe among those
      clearing the IS Sharpe legs is picked on IS only, and its OOS CAGR/Sharpe/MaxDD are read
      once against RULES v2 and SPY, with the IS DD leg's verdict recorded beside it.  This
      prices what the DD leg costs a reader who actually uses 4a to choose a book.

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  B136 is today's constituents and SMALL439 the current sub-$2B screen only (see
  data/SMALL_PANEL_README.md): names delisted, acquired or grown out of the screen are absent,
  so every LEVEL on those two panels is biased upward.  For THIS statistic the bias acts on the
  numerator and denominator in the same direction -- survivor panels make arms look better on
  BOTH legs -- but it is not neutral: it inflates the Sharpe-clear count (the denominator) more
  on the panels whose live comparand is weakest, which is exactly the cross-panel contrast under
  test.  Levels on B136/SMALL439 are therefore upper bounds, and the U56 column is the one with
  the mildest bias.
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score       # noqa: E402
from engine import backtest, rebalance_mask                                   # noqa: E402

COSTS = [0.0, 10.0, 25.0]
PUB_COSTS = [10.0, 25.0]          # idea 500/508's own two rungs (G3)
BAND, GROSS, NCAND = 0.03, 0.75, 20
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
V2_U56_10 = dict(CAGR=0.0861, Sharpe=1.1998, MaxDD=-0.1205)
IDEA500 = dict(rows=244, clears=15, cuts=13)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, index=False):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=index)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ---------------------------------------------------------------- fast engine
def fast_run(px, W, freq):
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]; heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx),
            pd.Series(np.abs(held).sum(axis=1), index=idx))


def costed(gr, turn, bps):
    return gr - turn * bps / 1e4


# ---------------------------------------------------------------- book forms
def _ew(px, mask, gross):
    e = mask.astype(float).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def w_topn(px, n, S, gross=GROSS):
    """CAND-n on the composite WITH the vol scaler -- idea 500/508's own `n` dial, kept
    convention-identical so its corpus is a labelled subset of this one (G3b)."""
    s, above, _ = S["vs"]
    return _ew(px, s.where(above).rank(axis=1, ascending=False) <= n, gross)


def w_nns(px, n, S, gross=GROSS):
    """CAND-n with NO vol scaler -- the 2026-09-04 KEEP-4b candidate's own book form."""
    s, above, _ = S["ns"]
    return _ew(px, s.where(above).rank(axis=1, ascending=False) <= n, gross)


def w_band(px, band, S, gross=GROSS):
    return rules_v2_weights(px, band=band, gross=gross)


def w_gross(px, gross, S, band=BAND):
    return rules_v2_weights(px, band=band, gross=gross)


def w_volcap(px, cap, S, gross=GROSS):
    _, above, vol20 = S["vs"]
    return _ew(px, above & (vol20 < cap), gross)


def w_quantile(px, x, S, gross=GROSS):
    s, above, _ = S["vs"]
    return _ew(px, s.where(above).rank(axis=1, ascending=False, pct=True) <= x, gross)


def w_ma(px, L, S, gross=GROSS):
    """The band book with the 200d MA replaced by an L-day MA (band fixed at 0.03)."""
    ma = px.rolling(int(L)).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + BAND), 1.0).mask(px < ma * (1 - BAND), 0.0)
    st = raw.ffill().fillna(0.0) > 0.5
    return _ew(px, px.notna(), gross).where(st, 0.0)


def w_lookback(px, L, S, gross=GROSS):
    """CAND-20 on a SINGLE momentum lookback of L trading days, same 200d trend gate."""
    _, above, _ = S["ns"]
    mom = px / px.shift(int(L)) - 1
    r = mom.where(above).rank(axis=1, ascending=False)
    return _ew(px, r <= NCAND, gross)


DIALS = {
    "n":        dict(fn=w_topn,     pub=[5, 10, 20, 30, 50],
                     ext=[3, 7, 15, 25, 40, 75, 100], freq="W"),
    "band":     dict(fn=w_band,     pub=[0.00, 0.01, 0.03, 0.05, 0.08, 0.12],
                     ext=[0.02, 0.04, 0.06, 0.10, 0.16, 0.20, 0.25, 0.35], freq="W"),
    "gross":    dict(fn=w_gross,    pub=[0.25, 0.50, 0.75, 1.00],
                     ext=[0.10, 0.35, 0.60, 0.85, 0.90, 1.10], freq="W"),
    "volcap":   dict(fn=w_volcap,   pub=[0.30, 0.45, 0.60, 0.90, 9.99],
                     ext=[0.20, 0.25, 0.35, 0.75, 1.50], freq="W"),
    "quantile": dict(fn=w_quantile, pub=[0.10, 0.25, 0.50, 0.75, 1.00],
                     ext=[0.02, 0.05, 0.15, 0.35, 0.60, 0.90], freq="W"),
    "cadence":  dict(fn=None,       pub=["D", "W", "M", "Q"], ext=[], freq=None),
    "ma":       dict(fn=w_ma,       pub=[], ext=[50, 75, 100, 150, 200, 250, 300, 400], freq="W"),
    "nns":      dict(fn=w_nns,      pub=[], ext=[3, 5, 10, 20, 30, 50, 75], freq="W"),
    "lookback": dict(fn=w_lookback, pub=[], ext=[21, 63, 126, 189, 252, 378, 504], freq="W"),
}


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(px.columns) - len(keep)


# ---------------------------------------------------------------- metrics
def M0(r):
    v = r.std() * np.sqrt(252)
    return float((r.mean() * 252) / v) if v else np.nan


def M(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    h = len(r) // 2
    return dict(CAGR=float(eq.iloc[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=float((r.mean() * 252) / vol) if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()), Vol=float(vol),
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def wilson(k, n):
    if n == 0: return (np.nan, np.nan)
    p, z = k / n, 1.96
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    hw = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - hw), min(1.0, c + hw))


def legs4a(m, mb):
    """PROTOCOL 4a read exactly as written: Sharpe > base in BOTH halves, MaxDD >= base."""
    s1, s2 = m["H1"] > mb["H1"], m["H2"] > mb["H2"]
    dd = m["MaxDD"] >= mb["MaxDD"]
    return bool(s1), bool(s2), bool(dd)


def pass4b(m, oos_s, ms, spy_oos):
    return bool((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > spy_oos)
                and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
                and (m["CAGR"] >= 0.70 * ms["CAGR"]))


# ---------------------------------------------------------------- corpus
def panel_state(px):
    return {"ns": score(px, vol_scale=False), "vs": score(px, vol_scale=True)}


def build_corpus(panels, n_dropped):
    rows = []
    for pname, px in panels.items():
        S = panel_state(px)
        i0 = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0.0)
        base_gr, base_tn, base_gx = fast_run(px, rules_v2_weights(px, BAND, GROSS), "W")
        for dname, D in DIALS.items():
            for v, pub in [(x, 1) for x in D["pub"]] + [(x, 0) for x in D["ext"]]:
                if dname == "cadence":
                    W, freq = rules_v2_weights(px, BAND, GROSS), v
                else:
                    W, freq = D["fn"](px, v, S), D["freq"]
                gr, tn, gx = fast_run(px, W, freq)
                for c in COSTS:
                    r = costed(gr, tn, c).loc[i0:]
                    b = costed(base_gr, base_tn, c).loc[i0:]
                    m, mb, ms = M(r), M(b), M(spy.loc[i0:])
                    mi, mo = M(r.loc[:IS_END]), M(r.loc[OOS_START:])
                    mbi, mbo = M(b.loc[:IS_END]), M(b.loc[OOS_START:])
                    s1, s2, dd = legs4a(m, mb)
                    i1, i2, idd = legs4a(mi, mbi)
                    o1, o2, odd = legs4a(mo, mbo)
                    rows.append(dict(
                        panel=pname, dial=dname, arm=str(v), pub=pub, cost=c, freq=freq,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                        H1=m["H1"], H2=m["H2"], gross=float(gx.loc[i0:].mean()),
                        turn_yr=float(tn.loc[i0:].sum() / (len(r) / 252)),
                        base_H1=mb["H1"], base_H2=mb["H2"], base_MaxDD=mb["MaxDD"],
                        base_Vol=mb["Vol"], base_Sharpe=mb["Sharpe"],
                        spy_MaxDD=ms["MaxDD"], spy_CAGR=ms["CAGR"],
                        leg_H1=s1, leg_H2=s2, leg_DD=dd,
                        sharpe_clear=s1 and s2, dd_cut=(s1 and s2) and not dd,
                        pass4a=s1 and s2 and dd,
                        pass4b=pass4b(m, mo["Sharpe"], ms, M0(spy.loc[OOS_START:])),
                        dd_margin=m["MaxDD"] - mb["MaxDD"],
                        IS_Sharpe=mi["Sharpe"], IS_H1=mi["H1"], IS_H2=mi["H2"],
                        IS_MaxDD=mi["MaxDD"], IS_clear=i1 and i2, IS_dd=idd,
                        IS_cut=(i1 and i2) and not idd,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        OOS_clear=o1 and o2, OOS_dd=odd, OOS_cut=(o1 and o2) and not odd,
                        v2_OOS_CAGR=mbo["CAGR"], v2_OOS_Sharpe=mbo["Sharpe"],
                        v2_OOS_MaxDD=mbo["MaxDD"]))
        P(f"  {pname}: {sum(1 for r in rows if r['panel'] == pname)} arm-rows "
          f"({px.shape[1]} columns, base Sharpe {M(costed(base_gr, base_tn, 10.0).loc[i0:])['Sharpe']:.4f}, "
          f"base MaxDD {M(costed(base_gr, base_tn, 10.0).loc[i0:])['MaxDD']:.2%})")
    return pd.DataFrame(rows)


def rate_table(df, by):
    out = []
    for k, sub in df.groupby(by, dropna=False):
        cl = int(sub.sharpe_clear.sum()); cut = int(sub.dd_cut.sum())
        ddp = int(sub.leg_DD.sum())
        clr = int((sub.sharpe_clear & sub.leg_DD).sum())
        lo, hi = wilson(cut, cl)
        row = {(by if isinstance(by, str) else "cell"): k} if isinstance(k, str) else \
              dict(zip(by if isinstance(by, list) else [by], k if isinstance(k, tuple) else (k,)))
        row.update(n=len(sub), clears=cl, clear_rate=cl / len(sub), cuts=cut,
                   cut_rate=cut / cl if cl else np.nan, cut_lo=lo, cut_hi=hi,
                   dd_pass=ddp, dd_pass_rate=ddp / len(sub),
                   clear_given_dd=clr / ddp if ddp else np.nan,
                   pass4a=int(sub.pass4a.sum()), pass4b=int(sub.pass4b.sum()),
                   med_dd_margin=float(sub.loc[sub.sharpe_clear, "dd_margin"].median())
                   if cl else np.nan)
        out.append(row)
    return pd.DataFrame(out)


# ---------------------------------------------------------------- gates
def gates(panels, n_dropped):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]
    W = rules_v2_weights(px, BAND, GROSS)
    gr, tn, gx = fast_run(px, W, "W")
    j = px.index[WARM]
    slow = backtest(px, W, cost_bps=10.0, freq="W")["returns"]
    g1 = float(np.abs(slow.loc[j:].values - costed(gr, tn, 10.0).loc[j:].values).max())
    P(f"  G1 fast_run == engine.backtest @10 bps                 : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    m = M(costed(gr, tn, 10.0).loc[j:])
    d = max(abs(m["CAGR"] - V2_U56_10["CAGR"]), abs(m["Sharpe"] - V2_U56_10["Sharpe"]),
            abs(m["MaxDD"] - V2_U56_10["MaxDD"]))
    P(f"  G2 live comparand RULES v2 U56 @10 bps: {m['CAGR']:.2%} / {m['Sharpe']:.4f} / "
      f"{m['MaxDD']:.2%} vs record {V2_U56_10['CAGR']:.2%} / {V2_U56_10['Sharpe']:.4f} / "
      f"{V2_U56_10['MaxDD']:.2%}  max|d| {d:.3e}  {'PASS' if d < 6e-3 else 'FAIL'}")
    ok &= d < 6e-3

    r0 = costed(gr, tn, 0.0); r10 = costed(gr, tn, 10.0)
    g4 = float(np.abs((r0 - r10) - tn * 10.0 / 1e4).max())
    P(f"  G4 cost rungs are ONE gross stream minus turnover x c  : {g4:.3e}  "
      f"{'PASS' if g4 < 1e-15 else 'FAIL'}")
    ok &= g4 < 1e-15

    mb = M(costed(gr, tn, 10.0).loc[j:])
    s1, s2, dd = legs4a(mb, mb)
    P(f"  G6 4a read as written (ties PASS the DD leg): a book vs itself -> H1 {s1}, H2 {s2}, "
      f"DD {dd}  {'PASS' if (dd and not s1 and not s2) else 'FAIL'}")
    ok &= dd and not s1 and not s2

    P(f"  G5 SMALL439 dropped {n_dropped} tickers with max_1d_move >= 1.0 : "
      f"{'PASS' if n_dropped > 0 else 'FAIL'}")
    ok &= n_dropped > 0
    return ok


def gate3(corpus):
    """G3a: idea 500's three headline numbers, recomputed from idea 508's COMMITTED arms.csv
    with this file's leg definitions.  G3b: on the (panel, dial, arm, cost) rows the two
    corpora share, every 4a leg must agree.  The gate as first drafted (idea 500's corpus ==
    the `pub` subset of this one) was mis-specified; both readings are printed."""
    f = ROOT / "research" / "backtests" / \
        "2026-09-11_price-the-4a-MaxDD-leg-against-a-VOL-MATCHED-cap_B.arms.csv"
    a = pd.read_csv(f)
    a = a[a.dial != "_comparand"].copy()
    a["clear"] = (a.H1_Sharpe > a.base_H1) & (a.H2_Sharpe > a.base_H2)
    a["cut"] = a["clear"] & ~(a.FULL_MaxDD >= a.base_MaxDD)
    rows, cl, cut = len(a), int(a["clear"].sum()), int(a["cut"].sum())
    ok_a = (rows == IDEA500["rows"] and cl == IDEA500["clears"] and cut == IDEA500["cuts"])
    P(f"  G3a idea 500's corpus from idea 508's committed arms.csv: {rows} arm-rows, {cl} "
      f"Sharpe-clears ({cl/rows:.1%}), {cut} DD-cuts ({cut/cl:.1%})  vs published "
      f"{IDEA500['rows']} / {IDEA500['clears']} ({IDEA500['clears']/IDEA500['rows']:.1%}) / "
      f"{IDEA500['cuts']} ({IDEA500['cuts']/IDEA500['clears']:.1%})  "
      f"{'PASS' if ok_a else 'FAIL'}")

    sub = corpus[(corpus.pub == 1) & (corpus.cost.isin(PUB_COSTS))]
    P(f"      (the mis-specified reading, reported not dropped: the `pub` subset of THIS corpus "
      f"is {len(sub)} arm-rows, {int(sub.sharpe_clear.sum())} clears, "
      f"{int(sub.dd_cut.sum())} cuts -- idea 500 skipped every `n` rung wider than its panel, "
      f"so it can never be {IDEA500['rows']} rows)")

    k = ["panel", "dial", "arm", "cost"]
    a["arm"] = a["arm"].astype(str); a["cost"] = a["cost"].astype(float)
    j = a.merge(corpus, on=k, suffixes=("_500", "_now"))
    dis_cl = int((j["clear"] != j.sharpe_clear).sum())
    dis_cut = int((j["cut"] != j.dd_cut).sum())
    dmax = float(np.abs(j.H1_Sharpe - j.H1).max()) if len(j) else np.nan
    ok_b = len(j) > 0 and dis_cl == 0 and dis_cut == 0
    P(f"  G3b shared rows {len(j)} of {rows}: leg disagreements clear {dis_cl}, cut {dis_cut}; "
      f"max|dH1_Sharpe| {dmax:.3e}  {'PASS' if ok_b else 'FAIL'}")
    return ok_a and ok_b


# ---------------------------------------------------------------- main
def main():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    panels["SMALL439"], n_dropped = small_panel()
    ok = gates(panels, n_dropped)
    P()
    P("=" * 100)
    P("(B) THE WIDER CORPUS")
    P("=" * 100)
    corpus = build_corpus(panels, n_dropped)
    P(f"  total {len(corpus)} arm-rows = {len(corpus)//len(COSTS)} arms x {len(COSTS)} cost rungs"
      f"   (idea 500: {IDEA500['rows']} arm-rows)")
    g3 = gate3(corpus)
    P(f"  GATES: {'ALL PASS' if (ok and g3) else 'SEE ABOVE -- a gate did not pass'}")

    P()
    P("=" * 100)
    P("(C) THE CUT RATE -- corpus, per panel, per dial, per cost rung")
    P("=" * 100)
    cl = int(corpus.sharpe_clear.sum()); cut = int(corpus.dd_cut.sum())
    lo, hi = wilson(cut, cl)
    P(f"  CORPUS  {len(corpus)} arm-rows, {cl} Sharpe-clears ({cl/len(corpus):.1%}), "
      f"{cut} DD-cuts -> CUT RATE {cut/cl:.1%} [95% CI {lo:.1%}, {hi:.1%}]  "
      f"(idea 500: 86.7%, 13/15)")
    P(f"  4a passes {int(corpus.pass4a.sum())}, 4b passes {int(corpus.pass4b.sum())}")
    by_panel = rate_table(corpus, "panel")
    by_dial = rate_table(corpus, "dial")
    by_cost = rate_table(corpus, "cost")
    by_cell = rate_table(corpus, ["panel", "dial"])
    by_pc = rate_table(corpus, ["panel", "cost"])
    for nm, t in [("PANEL", by_panel), ("DIAL", by_dial), ("COST", by_cost)]:
        P()
        P(f"  by {nm}:")
        cols = ["n", "clears", "clear_rate", "cuts", "cut_rate", "cut_lo", "cut_hi",
                "clear_given_dd", "pass4a", "pass4b", "med_dd_margin"]
        show = t.set_index(t.columns[0])[cols]
        for line in show.to_string(float_format=lambda x: f"{x:.3f}").split("\n"):
            P("    " + line)
    P()
    P("  by PANEL x COST (cut rate; '.' = no Sharpe-clear in the cell):")
    pv = by_pc.pivot_table(index="panel", columns="cost", values="cut_rate")
    for line in pv.to_string(float_format=lambda x: f"{x:.3f}", na_rep=".").split("\n"):
        P("    " + line)
    P()
    P("  by PANEL x DIAL (clears / cuts):")
    tab = corpus.groupby(["panel", "dial"]).agg(cl=("sharpe_clear", "sum"),
                                                ct=("dd_cut", "sum")).reset_index()
    pv = tab.pivot(index="dial", columns="panel", values=["cl", "ct"])
    for line in pv.to_string().split("\n"):
        P("    " + line)

    # homogeneity of the cut rate across panels (2x3 chi-square on clears x {cut, pass})
    P()
    obs = by_panel[by_panel.clears > 0]
    if len(obs) >= 2:
        n = obs.clears.values.astype(float); k = obs.cuts.values.astype(float)
        pbar = k.sum() / n.sum()
        chi = float(np.nansum((k - n * pbar) ** 2 / (n * pbar * (1 - pbar)))) if 0 < pbar < 1 else 0.0
        P(f"  HOMOGENEITY of the cut rate across panels: pooled {pbar:.1%}, "
          f"chi2 = {chi:.2f} on {len(obs)-1} df "
          f"(5% critical {3.84 if len(obs)==2 else 5.99:.2f}) -> "
          f"{'NOT rejected (constant is tenable)' if chi < (3.84 if len(obs)==2 else 5.99) else 'REJECTED (panel-dependent)'}")
        P("  per-panel cut rates: " + ", ".join(
            f"{r.panel} {r.cut_rate:.1%} ({int(r.cuts)}/{int(r.clears)}) "
            f"[{r.cut_lo:.0%},{r.cut_hi:.0%}]" for _, r in obs.iterrows()))

    P()
    P("=" * 100)
    P("(D) RULE 8 (a) -- does the cut rate walk forward?  IS <= 2016-12-31, OOS read once")
    P("=" * 100)
    wf = []
    for (pn,), sub in corpus.groupby(["panel"]):
        for tag, cflag, dflag in [("IS", "IS_clear", "IS_cut"), ("OOS", "OOS_clear", "OOS_cut"),
                                  ("FULL", "sharpe_clear", "dd_cut")]:
            c = int(sub[cflag].sum()); u = int(sub[dflag].sum())
            lo_, hi_ = wilson(u, c)
            wf.append(dict(panel=pn, window=tag, n=len(sub), clears=c, cuts=u,
                           cut_rate=u / c if c else np.nan, lo=lo_, hi=hi_))
    wf = pd.DataFrame(wf)
    for line in wf.set_index(["panel", "window"]).to_string(
            float_format=lambda x: f"{x:.3f}").split("\n"):
        P("    " + line)

    P()
    P("=" * 100)
    P("(E) RULE 8 (b) -- the arm pick: chosen on IS Sharpe among IS Sharpe-clears, OOS read once")
    P("=" * 100)
    picks = []
    for (pn, c), sub in corpus.groupby(["panel", "cost"]):
        elig = sub[sub.IS_clear]
        row = dict(panel=pn, cost=c, n_IS_clear=len(elig))
        if len(elig):
            p = elig.sort_values("IS_Sharpe", ascending=False).iloc[0]
            free = sub.sort_values("IS_Sharpe", ascending=False).iloc[0]
            row.update(pick=f"{p.dial}={p.arm}", IS_Sharpe=p.IS_Sharpe, IS_dd_pass=bool(p.IS_dd),
                       OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                       v2_OOS_CAGR=p.v2_OOS_CAGR, v2_OOS_Sharpe=p.v2_OOS_Sharpe,
                       v2_OOS_MaxDD=p.v2_OOS_MaxDD, spy_MaxDD=p.spy_MaxDD,
                       pass4a=bool(p.pass4a), pass4b=bool(p.pass4b),
                       ddleg_pick=f"{free.dial}={free.arm}", ddleg_OOS_Sharpe=free.OOS_Sharpe,
                       ddleg_OOS_MaxDD=free.OOS_MaxDD)
            # what the DD leg costs: best IS arm that ALSO passes the IS DD leg
            both = elig[elig.IS_dd]
            if len(both):
                q = both.sort_values("IS_Sharpe", ascending=False).iloc[0]
                row.update(pick_ddok=f"{q.dial}={q.arm}", ddok_OOS_Sharpe=q.OOS_Sharpe,
                           ddok_OOS_MaxDD=q.OOS_MaxDD, ddok_OOS_CAGR=q.OOS_CAGR)
        picks.append(row)
    picks = pd.DataFrame(picks)
    spy = panels["U56"]["SPY"].pct_change().fillna(0.0)
    mso = M(spy.loc[OOS_START:])
    P(f"  SPY OOS (U56 calendar): {mso['CAGR']:.2%} / {mso['Sharpe']:.4f} / {mso['MaxDD']:.2%}")
    cols = [c for c in ["panel", "cost", "n_IS_clear", "pick", "IS_Sharpe", "IS_dd_pass",
                        "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pick_ddok", "ddok_OOS_CAGR",
                        "ddok_OOS_Sharpe", "ddok_OOS_MaxDD", "v2_OOS_Sharpe", "v2_OOS_MaxDD",
                        "pass4a", "pass4b"] if c in picks.columns]
    for line in picks[cols].to_string(index=False,
                                      float_format=lambda x: f"{x:.4f}").split("\n"):
        P("    " + line)

    dump(corpus, "arms")
    dump(by_panel, "bypanel")
    dump(by_dial, "bydial")
    dump(by_cell, "bycell")
    dump(wf, "walkforward")
    dump(picks, "picks")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"  wrote {STEM}.console.txt")
    return ok and g3


if __name__ == "__main__":
    main()
