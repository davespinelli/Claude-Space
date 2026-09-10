#!/usr/bin/env python3
"""Idea 632 -- re-cut every published BINDING-BAR claim as a step-normalised argmin.

The record's `m_bind` / `bind_bar` column is `argmin` over the five 4b margins

    m_H1, m_H2, m_OOS   (SHARPE units)
    m_DD                (MaxDD FRACTION units)
    m_CAGR              (CAGR FRACTION units)

i.e. a minimum taken across three different units.  Idea 408 found that the raw argmin and a
step-normalised argmin disagree on 41.3% of 150 points; idea 408R then found that `steps` is
not density-free (median x4/x1 2.089, inf on 22% of cells) and recommended margin/|dm/dc|.

This file asks the queue's question -- how many published "the binding bar is X" claims survive
a unit-free re-read -- and reports one correction to the framing.

    PART A  CENSUS.  Every committed research/backtests/*.csv row carrying the full five-margin
            block, in both the full-sample (`m_*`) and in-sample (`IS_m_*`) families.  G0 checks
            that the published bind column really is the raw argmin.
    PART B  RESTATEMENT.  Re-cut the argmin under four unit-free normalisers on the committed
            rows, at cell level and at claim (file-modal-bar) level, on three claim sets.
    PART C  PROSE.  The record's committed result/memo files that name a binding bar in words,
            checked against their own file's re-cut modal bar.
    PART D  DENSITY.  A fresh grid whose spacing this file controls, to test which normalisers
            are density-free.  RAW is invariant by construction; SD/IQR/RANK depend on WHICH
            points the publisher chose to print; SENS (margin/|dm/dc|) depends only on
            discretisation error.  Also settles whether idea 408R's density complaint reaches
            the ARGMIN at all (it divides all five bars by the same h, so it cannot).
    PART E  RULE 8 (PROTOCOL 8) + BOTH KEEP PATHS on every fresh grid point.

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
    NORM      in {RAW, SD, IQR, RANK, SENS}   (the normaliser; SENS needs a dial, PART D/E only)
    CLAIMSET  in {ALL, PASS4b, FAIL4b}        (which committed rows the claim is read over)
Everything else is read from the committed artefacts or fixed by PROTOCOL.  All grid points are
written to .grid.csv / .census.csv / .files.csv / .density.csv / .walkforward.csv.

PROTOCOL-fixed: weights decided at close t, applied at t+1; 10 bps per unit turnover; long only,
no leverage; warm-up 260 rows dropped; halves at len(r)//2; rule 8 split 2016-12-31.
SURVIVORSHIP: B136 and SMALL439 are CURRENT constituent lists (PROTOCOL 9) -- they exclude names
that were delisted, acquired or fell out of the screen, so their levels are biased UP and no
absolute CAGR/Sharpe from them is a tradable estimate; only the WITHIN-panel contrasts this file
reports (which bar is the argmin) are meant to survive that.  SMALL439 drops the 44 names with
data/small_meta.csv max_1d_move >= 1.0 before anything else.

Run:  python3 research/backtests/2026-09-10_re-cut-every-published-BINDING-BAR-claim-as-a-STEP-NORMALISED-argmin_cloud.py
"""
import re, sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

pd.set_option("display.width", 250)
OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST_BPS, WARMUP, FREQ = 10.0, 260, "W"
BARS = ["H1", "H2", "OOS", "DD", "CAGR"]
NORMS = ["RAW", "SD", "IQR", "RANK"]          # computable from a margin block alone
NORMS_D = NORMS + ["SENS"]                     # SENS needs an ordered dial -> PART D/E only
CLAIMSETS = ["ALL", "PASS4b", "FAIL4b"]
EPS = 1e-12


# ============================================================ generic argmin re-cut machinery
def recut(M, norm):
    """M: (n,5) float array of raw margins.  Return the argmin index per row under `norm`.

    RAW  argmin over the margins as published (three different units in one min).
    SD   each bar divided by the SD of that bar over the claim group  -> noise units.
    IQR  each bar divided by the IQR of that bar over the claim group -> robust noise units.
    RANK each bar replaced by its within-group percentile rank        -> distribution free.
    A bar whose scale is degenerate (SD/IQR == 0) is left in raw units and flagged by
    `degen` so the count is never silently inflated.
    """
    M = np.asarray(M, float)
    if norm == "RAW":
        return np.nanargmin(M, axis=1), 0
    if norm == "RANK":
        R = np.empty_like(M)
        for j in range(M.shape[1]):
            R[:, j] = pd.Series(M[:, j]).rank(pct=True, na_option="keep").values
        return np.nanargmin(R, axis=1), 0
    if norm == "SD":
        s = np.nanstd(M, axis=0)
    else:
        s = np.nanpercentile(M, 75, axis=0) - np.nanpercentile(M, 25, axis=0)
    degen = int((s <= EPS).sum())
    s = np.where(s <= EPS, 1.0, s)
    return np.nanargmin(M / s, axis=1), degen


def sens_recut(M, cvals):
    """margin / |dm/dc| along the group's own dial (idea 408R's spacing-free unit).

    |dm/dc| by central difference on the sorted dial; a bar that is flat on the dial gets an
    infinite normalised margin (it can never be reached by moving the dial), which is the
    honest reading and is why this normaliser has to be counted separately.
    """
    o = np.argsort(cvals); c = np.asarray(cvals, float)[o]; A = np.asarray(M, float)[o]
    if len(c) < 3 or np.ptp(c) <= 0:
        return np.full(len(c), -1)[np.argsort(o)]
    D = np.gradient(A, c, axis=0)
    d = np.abs(D)
    N = np.where(d <= EPS, np.inf, A / np.where(d <= EPS, 1.0, d))
    out = np.full(len(c), -1)
    fin = np.isfinite(N).any(axis=1)
    out[fin] = np.nanargmin(np.where(np.isfinite(N), N, np.inf)[fin], axis=1)
    inv = np.empty_like(o); inv[o] = np.arange(len(o))
    return out[inv]


# ================================================================== PART A: the census scan
PREFIXES = [("", "m_bind"), ("IS_", "IS_m_bind")]
BINDCOL = re.compile(r"bind", re.I)


def scan_files():
    """Every committed csv carrying a complete five-margin block, in either family."""
    rows = []
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(OUT.name):
            continue          # never census THIS run's own outputs (determinism on re-run)
        try:
            hdr = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception:
            continue
        binds = [c for c in hdr if BINDCOL.search(c)]
        for pre, bindname in PREFIXES:
            cols = [f"{pre}m_{b}" for b in BARS]
            if all(c in hdr for c in cols):
                # only bind columns belonging to THIS margin family: a `ctl_`/`carrier_`/`mt_`/
                # `IS_` prefixed bind names a different margin block and is not this claim.
                own = [c for c in binds if (c.startswith("IS_") if pre == "IS_"
                                            else not re.match(r"^(IS|ctl|carrier|mt|OOS|a)_", c))]
                rows.append(dict(file=f.name, family=pre or "FULL",
                                 bindcol=bindname if bindname in hdr else (own[0] if own else ""),
                                 allbinds="|".join(own), cols=",".join(cols)))
    return pd.DataFrame(rows)


def load_block(fname, family):
    pre = "" if family == "FULL" else "IS_"
    d = pd.read_csv(BT / fname)
    cols = [f"{pre}m_{b}" for b in BARS]
    M = d[cols].apply(pd.to_numeric, errors="coerce")
    ok = M.notna().all(axis=1).values
    return d.loc[ok].reset_index(drop=True), M.loc[ok].reset_index(drop=True).values


def gate_g0(F):
    """G0  where a file publishes a bind-shaped column, is it really the RAW argmin?

    Checked per COLUMN, not pooled: a file may publish more than one bind column (one raw and
    one already normalised).  The gate asserts that every file has at least one column that
    reproduces the raw argmin exactly -- i.e. the published claim really is the raw argmin --
    and REPORTS the columns that do not, because those are the record's own precedent for
    the re-cut this idea proposes.
    """
    recs, chk, tot = [], 0, 0
    for _, r in F.iterrows():
        if not r.bindcol:
            continue
        d, M = load_block(r.file, r.family)
        if len(d) == 0:
            continue
        hit_any = False
        for col in [c for c in str(r.allbinds).split("|") if c and c in d.columns]:
            pub = d[col].astype(str).str.upper().str.replace("MAXDD", "DD", regex=False)
            m = pub.isin([b.upper() for b in BARS]).values
            if m.sum() < 8:
                continue          # a bind column of a different kind (counts, rates, booleans)
            got = np.char.upper(np.array(BARS)[recut(M, "RAW")[0]])
            rate = float((pub.values[m] == got[m]).mean())
            recs.append(dict(file=r.file, family=r.family, col=col, n=int(m.sum()),
                             repro_raw=rate))
            tot += int(m.sum()); chk += int((pub.values[m] == got[m]).sum())
            hit_any = hit_any or rate > 0.999
        if recs and not hit_any:
            print(f"      NOTE {r.file} [{r.family}] publishes no column reproducing the raw argmin")
    R = pd.DataFrame(recs)
    R.to_csv(OUT.with_suffix(".g0.csv"), index=False)
    exact = R[R.repro_raw > 0.999]
    print(f"G0  bind-shaped columns checked: {len(R)} over {R.file.nunique()} files, {tot} rows")
    print(f"    columns reproducing the RAW argmin exactly: {len(exact)}/{len(R)} "
          f"({int(exact.n.sum())}/{tot} rows)")
    for _, b in R[R.repro_raw <= 0.999].iterrows():
        print(f"      NOT raw: {b.file} :: {b.col}  ({b.n} rows, agrees {b.repro_raw:.4f})")
    assert len(exact) and float(exact.n.sum()) / tot > 0.5, \
        "G0 FAILED: the record's bind columns are not predominantly the raw argmin"
    return tot, float(exact.n.sum()) / tot, R


# ================================================== PART D/E: fresh grid, engine and dials
def fast_backtest(prices, weights, freq=FREQ):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


DIALS = {
    "band":  dict(c0=0.03, step=0.01, lo=0.00, hi=0.12, host="V2"),
    "gross": dict(c0=0.75, step=0.05, lo=0.30, hi=1.20, host="V2"),
    "n":     dict(c0=5,    step=4,    lo=1,    hi=29,   host="V1"),
}
SCALES = {"x1": 1, "x2": 2}


class Panel:
    def __init__(self, px):
        self.px = px
        q = px.drop(columns=["SPY"]); self.q = q
        mom = q.shift(21) / q.shift(252) - 1
        r6 = q / q.shift(126) - 1
        r3 = q / q.shift(63) - 1
        self.comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                     + r3.rank(axis=1, pct=True)) / 3
        self.vol20 = q.pct_change().rolling(20).std() * np.sqrt(252)
        self.notna = q.notna()
        self._ma, self._above, self._band = {}, {}, {}

    def ma(self, K):
        if K not in self._ma: self._ma[K] = self.q.rolling(int(K)).mean()
        return self._ma[K]

    def above(self, K):
        if K not in self._above: self._above[K] = self.q > self.ma(K)
        return self._above[K]

    def band_state(self, K, band):
        key = (K, round(float(band), 8))
        if key not in self._band:
            ma = self.ma(K)
            raw = pd.DataFrame(np.nan, index=self.q.index, columns=self.q.columns)
            raw = raw.mask(self.q > ma * (1 + band), 1.0).mask(self.q < ma * (1 - band), 0.0)
            self._band[key] = raw.ffill().fillna(0.0) > 0.5
        return self._band[key]

    def w_v2(self, band, gross, K=200):
        e = self.notna.astype(float)
        ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(self.band_state(K, band), 0.0)

    def w_v1(self, n, K=200, w=0.15, vol=0.60):
        s = self.comp * (0.5 + 0.5 * self.above(K).astype(float))
        s = s / self.vol20.clip(lower=0.08) ** 0.5
        elig = s.where(self.above(K) & (self.vol20 < vol))
        return (elig.rank(axis=1, ascending=False) <= n).astype(float) * w

    def book(self, dial, c):
        if DIALS[dial]["host"] == "V2":
            return self.w_v2(c if dial == "band" else DIALS["band"]["c0"],
                             c if dial == "gross" else DIALS["gross"]["c0"])
        return self.w_v1(int(c))


def grid_for(dial, scale):
    d = DIALS[dial]; h = d["step"] / scale
    if dial == "n":
        h = max(1, int(round(h)))
        g = list(range(int(d["c0"]), int(d["lo"]) - 1, -h))[::-1] + \
            list(range(int(d["c0"]) + h, int(d["hi"]) + 1, h))
        return sorted(set(g)), h
    nlo = int(round((d["c0"] - d["lo"]) / h)); nhi = int(round((d["hi"] - d["c0"]) / h))
    return [round(d["c0"] + i * h, 8) for i in range(-nlo, nhi + 1)], h


def legs(r):
    r = r.iloc[WARMUP:]
    h = len(r) // 2
    f, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
    hi = len(ri) // 2
    i, i1, i2, o = metrics(ri), metrics(ri.iloc[:hi]), metrics(ri.iloc[hi:]), metrics(ro)
    return dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_CAGR=i["CAGR"], IS_Sharpe=i["Sharpe"], IS_MaxDD=i["MaxDD"],
                IS_H1=i1["Sharpe"], IS_H2=i2["Sharpe"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def margins_full(L, S):
    """The five 4b bars over the FULL sample, signed, >=0 passes (PROTOCOL 4b)."""
    return [L["H1"] - S["H1"], L["H2"] - S["H2"], L["OOS_Sharpe"] - S["OOS_Sharpe"],
            L["MaxDD"] - 0.60 * S["MaxDD"], L["CAGR"] - 0.70 * S["CAGR"]]


def margins_is(L, S):
    """The same five bars computed inside the IS window ONLY (rule 8's choosing side).
    The 'OOS' slot becomes the IS-window full Sharpe, since no OOS data may be read."""
    return [L["IS_H1"] - S["IS_H1"], L["IS_H2"] - S["IS_H2"], L["IS_Sharpe"] - S["IS_Sharpe"],
            L["IS_MaxDD"] - 0.60 * S["IS_MaxDD"], L["IS_CAGR"] - 0.70 * S["IS_CAGR"]]


def v4a(L, B):
    return int(L["H1"] > B["H1"] and L["H2"] > B["H2"] and L["MaxDD"] >= B["MaxDD"])


def load_panels():
    P = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    dropped = [c for c in sm.columns if c in bad]
    P["SMALL439"] = sm.drop(columns=dropped)
    print(f"  SMALL: dropped {len(dropped)} names with max_1d_move >= 1.0")
    return P


def gate_g1(P):
    w = P.w_v2(0.03, 0.75)
    fr, ft = fast_backtest(P.q, w)
    eng = backtest(P.q, w, cost_bps=0.0, freq=FREQ)
    st = P.q.index[WARMUP]
    dr = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    dt = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    print(f"G1  fast_backtest vs engine.backtest: max|dret| {dr:.3e}  max|dturn| {dt:.3e}")
    assert dr < 1e-10 and dt < 1e-10, "G1 FAILED"


def gate_g2(P):
    d2 = float((P.w_v2(0.03, 0.75) - rules_v2_weights(P.q, 0.03, 0.75)).abs().max().max())
    d1 = float((P.w_v1(5) - rules_v1_weights(P.q, n=5, w=0.15, max_vol=0.60)).abs().max().max())
    print(f"G2  host V2 vs baseline.rules_v2_weights {d2:.3e};  host V1 vs rules_v1_weights {d1:.3e}")
    assert d2 < 1e-12 and d1 < 1e-12, "G2 FAILED"


def gate_g3():
    """G3  a common-factor normaliser cannot move an argmin.  This is the whole reason idea
    408R's density complaint about `steps` does not reach the binding-bar CLAIM."""
    rng = np.random.default_rng(0)
    M = rng.normal(size=(500, 5))
    a = np.nanargmin(M, axis=1)
    b = np.nanargmin(M / 7.3, axis=1)
    assert (a == b).all(), "G3 FAILED"
    print("G3  argmin invariant to a common positive factor on 500 random rows: 500/500")


# ==================================================================================== main
def main():
    print("=" * 100)
    print("IDEA 632  re-cut every published BINDING-BAR claim as a step-normalised argmin")
    print("=" * 100)

    # ------------------------------------------------------------------ PART A  CENSUS
    print("\n=== PART A  CENSUS of the record's committed five-margin blocks ===")
    F = scan_files()
    F.to_csv(OUT.with_suffix(".files.csv"), index=False)
    print(f"  csvs under research/backtests: {len(list(BT.glob('*.csv')))}")
    print(f"  files x family carrying a COMPLETE five-margin block: {len(F)}")
    print(f"    of which publish an explicit bind-shaped column: {(F.bindcol != '').sum()}")
    print(f"    families: " + "  ".join(f"{k}={v}" for k, v in F.family.value_counts().items()))
    n_bind_rows, g0rate, G0 = gate_g0(F)
    gate_g3()

    # ------------------------------------------------------------- PART B  RESTATEMENT
    print("\n=== PART B  RESTATEMENT: the argmin re-cut under four unit-free normalisers ===")
    cells, files = [], []
    for _, r in F.iterrows():
        d, M = load_block(r.file, r.family)
        if len(M) < 8:                       # a claim needs a population to be a claim
            continue
        pass4b = (M.min(axis=1) >= 0)
        base = np.array(BARS)[recut(M, "RAW")[0]]
        for cs in CLAIMSETS:
            sel = np.ones(len(M), bool) if cs == "ALL" else (pass4b if cs == "PASS4b" else ~pass4b)
            if sel.sum() < 8:
                continue
            Ms = M[sel]; b0 = base[sel]
            row = dict(file=r.file, family=r.family, claimset=cs, n=int(sel.sum()),
                       raw_modal=pd.Series(b0).mode().iat[0],
                       raw_modal_share=float(pd.Series(b0).value_counts(normalize=True).iat[0]))
            for nm in NORMS:
                idx, degen = recut(Ms, nm)
                bn = np.array(BARS)[idx]
                row[f"agree_{nm}"] = float((bn == b0).mean())
                row[f"modal_{nm}"] = pd.Series(bn).mode().iat[0]
                row[f"modalshare_{nm}"] = float(pd.Series(bn).value_counts(normalize=True).iat[0])
                row[f"degen_{nm}"] = degen
                row[f"survive_{nm}"] = int(row[f"modal_{nm}"] == row["raw_modal"])
            files.append(row)
            if cs == "ALL":
                for i in range(len(Ms)):
                    cells.append(dict(file=r.file, family=r.family, raw=b0[i],
                                      **{f"m_{b}": Ms[i, j] for j, b in enumerate(BARS)}))
    FB = pd.DataFrame(files)
    FB.to_csv(OUT.with_suffix(".census.csv"), index=False)
    pd.DataFrame(cells).to_csv(OUT.with_suffix(".cells.csv"), index=False)
    print(f"  claim rows (file x family x claimset, n>=8): {len(FB)}   "
          f"cells restated: {len(cells)}")

    print("\n  CELL-LEVEL agreement with the published RAW argmin, and CLAIM-LEVEL survival")
    print("  (a claim survives if the file's MODAL binding bar is unchanged)")
    hdr = f"    {'claimset':9s} {'claims':>6s} {'cells':>7s} " + \
          "".join(f"{n:>19s}" for n in NORMS)
    print(hdr)
    summ = []
    for cs in CLAIMSETS:
        s = FB[FB.claimset == cs]
        if not len(s):
            continue
        line = f"    {cs:9s} {len(s):6d} {int(s.n.sum()):7d} "
        for nm in NORMS:
            cell = float((s[f"agree_{nm}"] * s.n).sum() / s.n.sum())
            surv = float(s[f"survive_{nm}"].mean())
            line += f"  cell {cell:.3f} clm {surv:.3f}"
            summ.append(dict(claimset=cs, norm=nm, claims=len(s), cells=int(s.n.sum()),
                             cell_agree=cell, claim_survive=surv))
        print(line)
    pd.DataFrame(summ).to_csv(OUT.with_suffix(".summary.csv"), index=False)

    print("\n  WHICH bar the record says binds, and which it says under each normaliser (ALL):")
    sA = FB[FB.claimset == "ALL"]
    tab = pd.DataFrame({"RAW(published)": sA.raw_modal.value_counts()})
    for nm in NORMS:
        tab[nm] = sA[f"modal_{nm}"].value_counts()
    print(tab.fillna(0).astype(int).to_string())

    # ------------------------------------------------------------------- PART C  PROSE
    print("\n=== PART C  PROSE: committed files that name a binding bar in words ===")
    BARWORD = {"CAGR": r"CAGR", "DD": r"(?:MaxDD|DD cap|drawdown cap|DD leg)",
               "H1": r"\bH1\b", "H2": r"\bH2\b", "OOS": r"\bOOS\b"}
    BINDSENT = re.compile(r"[^.\n]*\b(?:binding bar|bar that (?:binds|cuts)|what (?:binds|cuts)|"
                          r"sole (?:bar|cut)|binds\b|is the binding)\b[^.\n]*", re.I)
    prose = []
    for f in sorted(list(BT.glob("*.result.md")) + list(BT.glob("*.memo.md"))):
        txt = f.read_text(errors="ignore")
        for s in BINDSENT.findall(txt):
            named = [b for b, p in BARWORD.items() if re.search(p, s)]
            if len(named) == 1:
                prose.append(dict(file=f.name, bar=named[0], sentence=" ".join(s.split())[:220]))
    PR = pd.DataFrame(prose)
    PR.to_csv(OUT.with_suffix(".prose.csv"), index=False)
    print(f"  result/memo files scanned: {len(list(BT.glob('*.result.md'))) + len(list(BT.glob('*.memo.md')))}")
    print(f"  sentences naming EXACTLY ONE bar as binding: {len(PR)}"
          f"   across {PR.file.nunique() if len(PR) else 0} files")
    if len(PR):
        print("  bar named: " + "  ".join(f"{k}={v}" for k, v in PR.bar.value_counts().items()))
        stem = {f.replace(".result.md", "").replace(".memo.md", "") for f in PR.file}
        link = sA[sA.file.str.replace(r"\.[^.]+\.csv$", "", regex=True).isin(stem)]
        print(f"  prose files that ALSO commit a five-margin block in the same run: "
              f"{link.file.nunique()}")
        if len(link):
            joined = []
            for _, rr in link.iterrows():
                st = re.sub(r"\.[^.]+\.csv$", "", rr.file)
                bars = PR[PR.file.str.startswith(st)].bar.unique().tolist()
                for b in bars:
                    joined.append(dict(file=rr.file, prose_bar=b, raw_modal=rr.raw_modal,
                                       **{f"modal_{n}": rr[f"modal_{n}"] for n in NORMS}))
            J = pd.DataFrame(joined)
            J.to_csv(OUT.with_suffix(".prose_linked.csv"), index=False)
            for nm in NORMS:
                print(f"    prose-bar == file {nm:4s} modal bar : "
                      f"{int((J.prose_bar == J[f'modal_{nm}']).sum())}/{len(J)}")

    # -------------------------------------------------------- PART D/E  fresh grid
    print("\n=== PART D  FRESH GRID (spacing controlled here) ===")
    panels = {k: Panel(v) for k, v in load_panels().items()}
    for pn, P in panels.items():
        print(f"  {pn:9s} {P.q.shape[1]:4d} names  {P.q.index[0].date()} .. {P.q.index[-1].date()}")
    gate_g1(panels["U56"]); gate_g2(panels["U56"])

    rows = []
    for pn, P in panels.items():
        S = legs(P.px["SPY"].pct_change().fillna(0.0))
        br, bt = fast_backtest(P.q, P.w_v2(0.03, 0.75))
        B = legs(br - bt * COST_BPS / 1e4)
        for dl in DIALS:
            for sn, sc in SCALES.items():
                g, h = grid_for(dl, sc)
                for c in g:
                    r, t = fast_backtest(P.q, P.book(dl, c))
                    L = legs(r - t * COST_BPS / 1e4)
                    mf, mi = margins_full(L, S), margins_is(L, S)
                    rows.append(dict(
                        panel=pn, dial=dl, scale=sn, h=h, c=c,
                        adopted=int(abs(c - DIALS[dl]["c0"]) < 1e-9),
                        **{f"m_{b}": mf[j] for j, b in enumerate(BARS)},
                        **{f"IS_m_{b}": mi[j] for j, b in enumerate(BARS)},
                        m_min=min(mf), IS_m_min=min(mi),
                        pass4b=int(min(mf) >= 0), pass4a=v4a(L, B),
                        spy_OOS_Sharpe=S["OOS_Sharpe"], spy_OOS_CAGR=S["OOS_CAGR"],
                        spy_OOS_MaxDD=S["OOS_MaxDD"], base_OOS_Sharpe=B["OOS_Sharpe"],
                        base_OOS_CAGR=B["OOS_CAGR"], base_OOS_MaxDD=B["OOS_MaxDD"],
                        base_H1=B["H1"], base_H2=B["H2"], base_MaxDD=B["MaxDD"],
                        **L))
        print(f"  {pn}: {len(rows)} grid points so far")
    G = pd.DataFrame(rows)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"  fresh grid points: {len(G)} -> {OUT.with_suffix('.grid.csv').name}   "
          f"4b passes {int(G.pass4b.sum())}   4a passes {int(G.pass4a.sum())}")

    # ---- argmin under every normaliser, per (panel, dial, scale)
    dens = []
    Mcols = [f"m_{b}" for b in BARS]
    for (pn, dl, sn), sub in G.groupby(["panel", "dial", "scale"]):
        sub = sub.sort_values("c").reset_index(drop=True)
        M = sub[Mcols].values
        picks = {}
        for nm in NORMS:
            picks[nm] = np.array(BARS)[recut(M, nm)[0]]
        si = sens_recut(M, sub.c.values)
        picks["SENS"] = np.where(si >= 0, np.array(BARS)[np.clip(si, 0, 4)], "NONE")
        for i in range(len(sub)):
            dens.append(dict(panel=pn, dial=dl, scale=sn, c=sub.c.iat[i],
                             adopted=sub.adopted.iat[i], pass4b=sub.pass4b.iat[i],
                             **{f"bind_{nm}": picks[nm][i] for nm in NORMS_D}))
    D = pd.DataFrame(dens)
    D.to_csv(OUT.with_suffix(".density.csv"), index=False)

    print("\n  Fresh-grid agreement with RAW argmin (all points, both densities):")
    for nm in NORMS_D:
        if nm == "RAW":
            continue
        ok = D[D[f"bind_{nm}"] != "NONE"]
        print(f"    {nm:5s}: {float((ok.bind_RAW == ok[f'bind_{nm}']).mean()):.3f}"
              f"   ({len(ok)} points)   modal {ok[f'bind_{nm}'].mode().iat[0]}")

    print("\n  DENSITY TEST -- same dial VALUE, published at x1 vs x2 spacing:")
    x1 = D[D.scale == "x1"].set_index(["panel", "dial", "c"])
    x2 = D[D.scale == "x2"].set_index(["panel", "dial", "c"])
    common = x1.index.intersection(x2.index)
    print(f"    shared dial values: {len(common)}")
    dsum = []
    for nm in NORMS_D:
        a, b = x1.loc[common, f"bind_{nm}"], x2.loc[common, f"bind_{nm}"]
        inv = float((a.values == b.values).mean())
        dsum.append(dict(norm=nm, density_invariance=inv, n=len(common)))
        print(f"    {nm:5s} density-invariant on {inv:.4f} of shared points")
    pd.DataFrame(dsum).to_csv(OUT.with_suffix(".densitysummary.csv"), index=False)

    # ---------------------------------------------------- PART E  RULE 8 + KEEP PATHS
    print("\n=== PART E  RULE 8 (choose on 2008-2016, evaluate 2017-2026 untouched) ===")
    ISc = [f"IS_m_{b}" for b in BARS]
    wf = []
    for (pn, dl, sn), sub in G.groupby(["panel", "dial", "scale"]):
        sub = sub.sort_values("c").reset_index(drop=True)
        Mi = sub[ISc].values
        for nm in NORMS_D:
            if nm == "SENS":
                si = sens_recut(Mi, sub.c.values)
                if (si < 0).all():
                    continue
                sc_ = np.abs(np.gradient(Mi, sub.c.values, axis=0)) if len(sub) >= 3 else np.ones_like(Mi)
                norm_m = np.where(sc_ <= EPS, np.inf, Mi / np.where(sc_ <= EPS, 1.0, sc_))
                obj = np.nanmin(np.where(np.isfinite(norm_m), norm_m, np.inf), axis=1)
            elif nm == "RAW":
                obj = Mi.min(axis=1)
            elif nm == "RANK":
                R = np.column_stack([pd.Series(Mi[:, j]).rank(pct=True).values for j in range(5)])
                obj = R.min(axis=1)
            else:
                s = np.nanstd(Mi, axis=0) if nm == "SD" else \
                    np.nanpercentile(Mi, 75, axis=0) - np.nanpercentile(Mi, 25, axis=0)
                s = np.where(s <= EPS, 1.0, s)
                obj = (Mi / s).min(axis=1)
            k = int(np.nanargmax(obj))
            r = sub.iloc[k]
            wf.append(dict(panel=pn, dial=dl, scale=sn, norm=nm, pick_c=r.c,
                           picked_adopted=int(r.adopted), IS_m_min=r.IS_m_min,
                           OOS_Sharpe=r.OOS_Sharpe, OOS_CAGR=r.OOS_CAGR, OOS_MaxDD=r.OOS_MaxDD,
                           base_OOS_Sharpe=r.base_OOS_Sharpe, base_OOS_CAGR=r.base_OOS_CAGR,
                           base_OOS_MaxDD=r.base_OOS_MaxDD, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                           spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                           d_vs_base=r.OOS_Sharpe - r.base_OOS_Sharpe,
                           d_vs_spy=r.OOS_Sharpe - r.spy_OOS_Sharpe,
                           pass4b=r.pass4b, pass4a=r.pass4a))
    W = pd.DataFrame(wf)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print(f"  rule-8 picks: {len(W)}  (panel x dial x density x normaliser)")
    print("\n  Does the NORMALISER change the rule-8 pick, and does it change the OOS answer?")
    piv = W.pivot_table(index=["panel", "dial", "scale"], columns="norm", values="pick_c")
    disagree = (piv.nunique(axis=1) > 1).mean()
    print(f"    cells where the normalisers do not all pick the same dial value: {disagree:.3f} "
          f"({int((piv.nunique(axis=1) > 1).sum())}/{len(piv)})")
    print(W.groupby("norm")[["d_vs_base", "d_vs_spy", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD",
                             "pass4b", "pass4a"]].mean().to_string(float_format=lambda x: f"{x:.4f}"))
    print("\n  Per panel (mean over dials x densities x normalisers), OOS 2017-2026:")
    pp = W.groupby("panel")[["OOS_Sharpe", "base_OOS_Sharpe", "spy_OOS_Sharpe",
                             "OOS_CAGR", "base_OOS_CAGR", "spy_OOS_CAGR",
                             "OOS_MaxDD", "base_OOS_MaxDD", "spy_OOS_MaxDD"]].mean()
    print(pp.to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n  BOTH KEEP PATHS over the whole fresh grid:")
    kp = G.groupby(["panel", "dial"])[["pass4b", "pass4a"]].sum()
    kp["points"] = G.groupby(["panel", "dial"]).size()
    print(kp.to_string())
    kp.to_csv(OUT.with_suffix(".keeppaths.csv"))
    print(f"  rule-8 picks passing 4b: {int(W.pass4b.sum())}/{len(W)}   "
          f"passing 4a: {int(W.pass4a.sum())}/{len(W)}")

    # --------------------------------------------------------------------- headline
    print("\n" + "=" * 100)
    a_all = pd.DataFrame(summ)
    worst = a_all[a_all.claimset == "ALL"].sort_values("claim_survive")
    print("HEADLINE")
    print(f"  {len(FB[FB.claimset=='ALL'])} committed claims ({int(FB[FB.claimset=='ALL'].n.sum())} cells) "
          f"re-cut.  Claim-level survival of the published modal binding bar:")
    for _, r in worst.iterrows():
        print(f"    {r.norm:5s}  cell-level agreement {r.cell_agree:.3f}   claim survives {r.claim_survive:.3f}")
    print(f"  G0: the record's own bind columns are the RAW argmin on {g0rate:.4f} of {n_bind_rows} rows.")
    print("=" * 100)


if __name__ == "__main__":
    main()
