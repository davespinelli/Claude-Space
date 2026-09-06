#!/usr/bin/env python3
"""QUEUE idea 281 — re-price-every-ranked-candidate-at-its-Sharpe-maximising-turnover
(lane C, 2026-09-06).

Question
--------
Idea 273 found corr(turnover, Sharpe) = -0.946 @10bps / -0.986 @25bps on the broad ranked
book across a realised-gross span of 0.0028, i.e. on THAT book the whole Sharpe curve is a
turnover curve.  If that is a property of ranked books generally and not of one book, then
every ranked candidate the record has published AT ITS NATURAL CADENCE was priced at the
wrong end of its own curve, and some published verdicts are cadence/churn artefacts.

The queued test, verbatim: re-run the record's ranked KEEP-candidates and near-misses with
the buffer attached, report how many VERDICTS MOVE, separating cells whose Sharpe gain
survives the rule-8 selector from those that do not.

Census (pre-registered, every row traceable to a published LEADERBOARD row)
--------------------------------------------------------------------------
The record's ranked books are all the same object: composite (mean pct-rank of 12-1 / 6m /
3m, NO /sqrt(vol20)) among eligible names, top NPOS=20, equal weight GROSS/NPOS = 0.75/20,
cash otherwise; eligible = vol20 < 0.60 AND the trend gate.  The census is the 12 distinct
(panel, gate, cadence) books the record published leaderboard rows for:

  * gate dial   (idea 57 / idea 4, weekly): gate in {none, 200d, band3} x {u56, broad}
  * cadence dial(idea 3, gate=200d)       : freq in {D, W, M, Q}       x {u56, broad}

(gate=200d/W is the same book in both dials -> 12 distinct.)  Published @10bps, CAGR /
Sharpe / MaxDD, asserted below as a REPRODUCTION GATE before any new number is read:

  u56   none/W 13.7 1.12 -18.5 | 200d/W 12.7 1.09 -18.3 | band3/W 13.1 1.12 -18.0
        200d/D 10.9 0.98 -16.3 | 200d/M 14.7 1.20 -19.5 | 200d/Q 13.5 1.02 -27.1
  broad none/W 12.8 0.93 -20.7 | 200d/W 13.1 0.96 -20.1 | band3/W 13.0 0.95 -20.1
        200d/D  9.9 0.76 -19.7 | 200d/M 16.4 1.10 -26.1 | 200d/Q 13.8 0.92 -27.1

Their published verdicts span the range the queue asks for: 4b KEEPs (all six u56 weekly /
monthly rows), one-axis near-misses (broad 200d/W and band3/W miss 4b on H2 alone; u56
200d/Q on DD alone; u56 200d/D on H1 alone) and clear KILLs (broad D/M/Q).

Instrument
----------
Idea 273's no-trade band on the composite rank, taken VERBATIM (its `band_weights`, with
its tie quirk, its forced-exit asymmetry and its parent-set-size target) so that m=0 nests
each parent EXACTLY: a name enters only inside the top NPOS, and a held name is replaced
only once its rank falls past NPOS + m.  Ineligible holdings (below the gate, or vol20 >=
0.60) are always sold; those forced sells are never banded.  Idea 273's j (replacements per
rebalance) is held FIXED at 999 = uncapped, the parent's own behaviour.

Params   : exactly ONE tuned dial, m in {0,2,5,10,15,20,30,50,999} (999 = hold until
           ineligible).  ALL 9 x 12 = 108 grid points are reported at BOTH cost rungs.
           Nothing about the 12 parent books is tuned here — they are the record's.
Costs    : 10 bps is the protocol rung and the verdict rung; 25 bps is a reporting axis.
           Both rungs come from ONE backtest per cell run at 0 bps, re-costed as
           r(bps) = r(0) - turnover * bps/1e4, which is the engine's own identity.
Rule 8   : m chosen on 2009-2016 ONLY (highest IS Sharpe), 2017-2026 untouched, per book.
           The book is causal so the IS window is a slice of the same run.  STATED AS A
           WEAKNESS, not hidden: 2017-2026 is essentially H2 on this sample, so the OOS bar
           and the 4b H2 bar overlap almost completely (idea 111's window problem).
Verdict  : both KEEP paths on every grid point.  4a against the LIVE book (RULES v2 at its
           own weekly cadence); 4b against SPY.
Reported : realised mean gross per cell beside the nominal (idea 274), so no arm can hide
           an exposure difference; and realised turnover per cell, since that is the axis
           the queued claim is about.

SURVIVORSHIP: universe.json (56) and universe_broad.json (136) are current constituents, so
absolute CAGR/Sharpe are optimistic on both panels.  Every comparison here is between arms
on the SAME panel over the SAME days, and the census parents carry the same bias as the
published rows they reproduce.

Outputs: .console.txt, .grid.csv (all 108 cells x 2 rungs), .census.csv (reproduction gate),
.verdicts.csv (m=0 vs oracle-best m vs rule-8 m), .walkforward.csv.  Deterministic, offline.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, metrics, rebalance_mask          # noqa: E402

NPOS, GROSS, MAX_VOL = 20, 0.75, 0.60
J = 999                                   # idea 273's second dial, held FIXED (uncapped)
END = "2026-09-03"                        # the record's eval end, so halves split as published
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MGRID = [0, 2, 5, 10, 15, 20, 30, 50, 999]
RUNGS = [10, 25]
OUT = Path(__file__).with_suffix("")

# census: (panel, gate, freq) -> published CAGR%, Sharpe, MaxDD% @10bps and published verdict
CENSUS = {
    ("u56",   "none",  "W"): (13.7, 1.12, -18.5, "KEEP 4b / KILL 4a"),
    ("u56",   "200d",  "W"): (12.7, 1.09, -18.3, "KEEP 4b / KILL 4a"),
    ("u56",   "band3", "W"): (13.1, 1.12, -18.0, "KEEP 4b / KILL 4a"),
    ("u56",   "200d",  "D"): (10.9, 0.98, -16.3, "KILL 4b (H1) / KILL 4a"),
    ("u56",   "200d",  "M"): (14.7, 1.20, -19.5, "KEEP 4b / KILL 4a"),
    ("u56",   "200d",  "Q"): (13.5, 1.02, -27.1, "KILL 4b (DD) / KILL 4a"),
    ("broad", "none",  "W"): (12.8, 0.93, -20.7, "KILL 4b (H2,OOS,DD) / KEEP 4a"),
    ("broad", "200d",  "W"): (13.1, 0.96, -20.1, "KILL 4b (H2) / KEEP 4a"),
    ("broad", "band3", "W"): (13.0, 0.95, -20.1, "KILL 4b (H2) / KEEP 4a"),
    ("broad", "200d",  "D"): (9.9,  0.76, -19.7, "KILL 4b (H1,H2,OOS,CAGR) / KEEP 4a"),
    ("broad", "200d",  "M"): (16.4, 1.10, -26.1, "KILL 4b (DD) / KILL 4a"),
    ("broad", "200d",  "Q"): (13.8, 0.92, -27.1, "KILL 4b (H2,OOS,DD) / KILL 4a"),
}
TOL = dict(CAGR=0.45, Sharpe=0.025, MaxDD=0.9)   # pp / abs / pp — published rows are 1-2 dp

_LINES = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LINES.append(s)


# --------------------------------------------------------------- construction
def composite(px):
    """v1's rank blend WITHOUT the /sqrt(vol20) term (idea 2/55/57/66's scorer)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, gate):
    if gate == "none":
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    if gate == "200d":
        return px > px.rolling(200).mean()
    if gate.startswith("band"):                      # hysteresis band, idea 57's definition
        b = int(gate[4:]) / 100.0
        ma = px.rolling(200).mean()
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + b), 1.0).mask(px < ma * (1 - b), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    raise ValueError(gate)


def eligible(px, gate):
    return (vol20(px) < MAX_VOL) & trend(px, gate)


def parent_weights(px, gate):
    """The record's stateless ranked book."""
    rank = composite(px).where(eligible(px, gate)).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def band_weights(px, gate, freq, m, j=J):
    """Idea 273's no-trade band on the composite rank (verbatim, generalised to gate/freq).

    At each rebalance date: (1) drop holdings that are INELIGIBLE today (risk rule, never
    banded, never capped); (2) among still-eligible holdings, sell those ranked worse than
    NPOS + m, at most j of them (worst-ranked first); (3) refill from the best-ranked
    non-held names inside the top NPOS, up to the PARENT'S own set size on that date
    (|{rank <= NPOS}|, which is 20 except on tie dates) — carrying that quirk is what makes
    m=0 nest the parent exactly rather than approximately.
    """
    comp = composite(px)
    rank_all = comp.where(eligible(px, gate)).rank(axis=1, ascending=False)
    dates = px.index[rebalance_mask(px.index, freq).values]
    cols = list(px.columns)
    pos = {c: i for i, c in enumerate(cols)}
    W = np.zeros((len(px.index), len(cols)))
    rk = rank_all.values
    didx = {d: i for i, d in enumerate(px.index)}
    held, row, prev_i = [], np.zeros(len(cols)), 0
    for d in dates:
        i = didx[d]
        W[prev_i:i] = row
        r = rk[i]
        held = [t for t in held if not np.isnan(r[pos[t]])]
        breach = sorted([t for t in held if r[pos[t]] > NPOS + m], key=lambda t: -r[pos[t]])
        for t in breach[:j]:
            held.remove(t)
        npos_t = int(np.nansum(r <= NPOS))
        need = npos_t - len(held)
        if need > 0:
            hs = set(held)
            cand = [(r[pos[c]], c) for c in cols
                    if c not in hs and not np.isnan(r[pos[c]]) and r[pos[c]] <= NPOS]
            cand.sort()
            held += [c for _, c in cand[:need]]
        row = np.zeros(len(cols))
        for t in held:
            row[pos[t]] = GROSS / NPOS
        W[i] = row
        prev_i = i + 1
    W[prev_i:] = row
    return pd.DataFrame(W, index=px.index, columns=px.columns)


# ------------------------------------------------------------------ machinery
def run0(px, w, freq):
    """One backtest at ZERO cost; both rungs are derived from it by the engine's identity."""
    return backtest(px, w, cost_bps=0.0, freq=freq)


def rets(res, bps, start):
    return (res["returns"] - res["turnover"] * bps / 1e4).loc[start:]


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none): Pearson of the ranks."""
    return pd.Series(a).rank().corr(pd.Series(b).rank())


def path4a(r, base):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(base.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(base.iloc[h:])["Sharpe"]: bad.append("H2")
    if metrics(r)["MaxDD"] < metrics(base)["MaxDD"]: bad.append("DD")
    return bad


def path4b(r, spy, oos_s, spy_oos_s):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(spy.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(spy.iloc[h:])["Sharpe"]: bad.append("H2")
    if oos_s <= spy_oos_s: bad.append("OOS")
    if abs(metrics(r)["MaxDD"]) > 0.60 * abs(metrics(spy)["MaxDD"]): bad.append("DD")
    if metrics(r)["CAGR"] < 0.70 * metrics(spy)["CAGR"]: bad.append("CAGR")
    return bad


def vstr(bad, tag):
    return f"KEEP {tag}" if not bad else f"KILL {tag}(" + ",".join(bad) + ")"


def cell_stats(r, res, start, spy, spy_oos_s, base):
    m = metrics(r)
    h = len(r) // 2
    oos = r.loc[OOS_START:]
    mo = metrics(oos)
    turn = res["turnover"].loc[start:]
    gross = res["weights"].loc[start:].sum(axis=1)
    b4a, b4b = path4a(r, base), path4b(r, spy, mo["Sharpe"], spy_oos_s)
    return dict(
        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
        H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
        IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
        turn_yr=turn.sum() / (len(r) / 252.0), gross=gross.mean(),
        v4a=vstr(b4a, "4a"), v4b=vstr(b4b, "4b"),
        keep4a=int(not b4a), keep4b=int(not b4b),
    )


# ==================================================================== main
def main():
    pd.set_option("display.width", 240)
    px = {"u56": load_universe().loc[:END], "broad": load_universe(broad=True).loc[:END]}
    for k, v in px.items():
        P(f"{k}: {v.shape[1]} tickers, {v.index[0].date()} -> {v.index[-1].date()}")

    ctx = {}
    for k, p in px.items():
        start = p.index[260]
        spy = p["SPY"].pct_change().fillna(0.0).loc[start:]
        base_res = run0(p, rules_v2_weights(p), "W")           # live RULES v2, its own cadence
        ctx[k] = dict(start=start, spy=spy,
                      spy_oos_s=metrics(spy.loc[OOS_START:])["Sharpe"],
                      base={b: rets(base_res, b, start) for b in RUNGS})
        m = metrics(spy); mo = metrics(spy.loc[OOS_START:])
        h = len(spy) // 2
        P(f"  SPY {k}: {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%} "
          f"halves {metrics(spy.iloc[:h])['Sharpe']:.4f}/{metrics(spy.iloc[h:])['Sharpe']:.4f} "
          f"OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.4f} | 4b bars: DD <= {0.60*abs(m['MaxDD']):.2%}, "
          f"CAGR >= {0.70*m['CAGR']:.2%}")
        b = ctx[k]["base"][10]
        mb = metrics(b)
        P(f"  RULES v2 {k} @10bps: {mb['CAGR']:.2%} / {mb['Sharpe']:.4f} / {mb['MaxDD']:.2%} "
          f"halves {metrics(b.iloc[:len(b)//2])['Sharpe']:.4f}/{metrics(b.iloc[len(b)//2:])['Sharpe']:.4f}")

    # ---------------------------------------------------- gate 1: reproduce the census
    P("\n=== REPRODUCTION GATE: 12 census parents vs their published LEADERBOARD rows (@10bps)")
    rep, parents = [], {}
    for (pan, gate, freq), (cP, sP, dP, vP) in CENSUS.items():
        p = px[pan]; c = ctx[pan]
        res = run0(p, parent_weights(p, gate), freq)
        r = rets(res, 10, c["start"])
        m = metrics(r)
        ok = (abs(m["CAGR"] * 100 - cP) <= TOL["CAGR"] and abs(m["Sharpe"] - sP) <= TOL["Sharpe"]
              and abs(m["MaxDD"] * 100 - dP) <= TOL["MaxDD"])
        parents[(pan, gate, freq)] = res
        rep.append(dict(panel=pan, gate=gate, freq=freq, pub_CAGR=cP, got_CAGR=100 * m["CAGR"],
                        pub_Sharpe=sP, got_Sharpe=m["Sharpe"], pub_MaxDD=dP,
                        got_MaxDD=100 * m["MaxDD"], reproduces=ok, published_verdict=vP))
    rep = pd.DataFrame(rep)
    P(rep.drop(columns=["published_verdict"]).to_string(index=False,
      float_format=lambda x: f"{x:.3f}"))
    rep.to_csv(f"{OUT}.census.csv", index=False)
    nrep = int(rep["reproduces"].sum())
    P(f"reproduces: {nrep}/12 within +/-{TOL['CAGR']}pp CAGR, +/-{TOL['Sharpe']} Sharpe, "
      f"+/-{TOL['MaxDD']}pp MaxDD")
    if nrep < 12:
        P("NOTE: non-reproducing books are kept in the grid but EXCLUDED from every "
          "verdict-move count below; the count is over reproduced books only.")

    # ---------------------------------------------------------------- the grid
    P("\n=== GRID: 12 books x 9 m x 2 rungs (all points)")
    rows, nest, cells = [], [], {}
    for (pan, gate, freq) in CENSUS:
        p, c = px[pan], ctx[pan]
        for m in MGRID:
            res = parents[(pan, gate, freq)] if m == 0 else run0(p, band_weights(p, gate, freq, m), freq)
            if m == 0:                                   # gate 2: the band nests the parent
                w0 = band_weights(p, gate, freq, 0)
                r0 = run0(p, w0, freq)
                rb = rebalance_mask(p.index, freq).values  # the only rows the engine reads
                dw = float(np.abs(w0.values[rb] - parent_weights(p, gate).fillna(0.0).values[rb]).max())
                dr = float((r0["returns"] - res["returns"]).abs().max())
                nest.append((pan, gate, freq, dw, dr))
                assert dw == 0.0 and dr == 0.0, (pan, gate, freq, dw, dr)
            cells[(pan, gate, freq, m)] = res            # kept for the cost-rung robustness pass
            for bps in RUNGS:
                r = rets(res, bps, c["start"])
                d = cell_stats(r, res, c["start"], c["spy"], c["spy_oos_s"], c["base"][bps])
                rows.append(dict(panel=pan, gate=gate, freq=freq, m=m, bps=bps, **d))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"nest gate: band_weights(m=0) == parent for all {len(nest)} books on every rebalance row "
      f"(max|dw| = {max(x[3] for x in nest):.1e}) and in returns (max|dr| = {max(x[4] for x in nest):.1e})")

    show = ["panel", "gate", "freq", "m", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "turn_yr", "gross", "v4a", "v4b"]
    for bps in RUNGS:
        P(f"\n--- all {len(MGRID)*len(CENSUS)} cells @ {bps} bps")
        P(G[G.bps == bps][show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------- the queued question
    P("\n=== Q1: is corr(turnover, Sharpe) < 0 on every ranked book, or only on idea 273's?")
    cr = []
    for (pan, gate, freq), g in G.groupby(["panel", "gate", "freq"], sort=False):
        for bps in RUNGS:
            s = g[g.bps == bps]
            cr.append(dict(panel=pan, gate=gate, freq=freq, bps=bps,
                           corr=s["turn_yr"].corr(s["Sharpe"]),
                           spearman=spearman(s["turn_yr"].values, s["Sharpe"].values),
                           turn_lo=s["turn_yr"].min(), turn_hi=s["turn_yr"].max(),
                           gross_span=s["gross"].max() - s["gross"].min(),
                           dSharpe=s["Sharpe"].max() - s["Sharpe"].min()))
    CR = pd.DataFrame(cr)
    P(CR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for bps in RUNGS:
        s = CR[CR.bps == bps]
        P(f"@{bps}bps: corr(turnover,Sharpe) negative in {int((s['corr'] < 0).sum())}/{len(s)} books, "
          f"median {s['corr'].median():.3f}; max realised-gross span across a book's 9 cells "
          f"{s['gross_span'].max():.4f}")

    P("\n=== Q2: how many VERDICTS MOVE when the buffer is attached?")
    P("m*  = ORACLE best-m by FULL-sample Sharpe (not implementable, the upper bound)")
    P("m8  = rule-8 best-m by 2009-2016 IS Sharpe only (implementable)")
    vd = []
    for (pan, gate, freq), (_, _, _, vpub) in CENSUS.items():
        for bps in RUNGS:
            s = G[(G.panel == pan) & (G.gate == gate) & (G.freq == freq) & (G.bps == bps)].set_index("m")
            base_row = s.loc[0]
            mo = s["Sharpe"].idxmax()
            m8 = s["IS_Sharpe"].idxmax()
            vd.append(dict(
                panel=pan, gate=gate, freq=freq, bps=bps, published=vpub,
                reproduces=bool(rep[(rep.panel == pan) & (rep.gate == gate) & (rep.freq == freq)]["reproduces"].iloc[0]),
                m_star=mo, m_8=m8,
                S0=base_row["Sharpe"], S_star=s.loc[mo, "Sharpe"], S_8=s.loc[m8, "Sharpe"],
                dS_star=s.loc[mo, "Sharpe"] - base_row["Sharpe"],
                dS_8=s.loc[m8, "Sharpe"] - base_row["Sharpe"],
                turn0=base_row["turn_yr"], turn8=s.loc[m8, "turn_yr"],
                OOS0=base_row["OOS_Sharpe"], OOS_8=s.loc[m8, "OOS_Sharpe"],
                dOOS_8=s.loc[m8, "OOS_Sharpe"] - base_row["OOS_Sharpe"],
                v4b_0=base_row["v4b"], v4b_star=s.loc[mo, "v4b"], v4b_8=s.loc[m8, "v4b"],
                v4a_0=base_row["v4a"], v4a_star=s.loc[mo, "v4a"], v4a_8=s.loc[m8, "v4a"],
                any4b=int(s["keep4b"].max()), n4b=int(s["keep4b"].sum()),
                any4a=int(s["keep4a"].max()), n4a=int(s["keep4a"].sum()),
                spearman_IS_OOS=spearman(s["IS_Sharpe"].values, s["OOS_Sharpe"].values),
            ))
    V = pd.DataFrame(vd)
    V.to_csv(f"{OUT}.verdicts.csv", index=False)
    cols = ["panel", "gate", "freq", "bps", "m_star", "m_8", "S0", "S_star", "S_8", "dS_star",
            "dS_8", "turn0", "turn8", "OOS0", "OOS_8", "v4b_0", "v4b_8", "n4b", "n4a",
            "spearman_IS_OOS"]
    P(V[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n--- verdict-move tally (reproduced books only)")
    R = V[V.reproduces]
    for bps in RUNGS:
        s = R[R.bps == bps]
        k0 = s["v4b_0"].str.startswith("KEEP")
        ks = s["v4b_star"].str.startswith("KEEP")
        k8 = s["v4b_8"].str.startswith("KEEP")
        a0 = s["v4a_0"].str.startswith("KEEP")
        a8 = s["v4a_8"].str.startswith("KEEP")
        P(f"@{bps}bps  n={len(s)} books")
        P(f"  4b: KEEP at m=0 {int(k0.sum())} | at oracle m* {int(ks.sum())} | at rule-8 m8 {int(k8.sum())}")
        P(f"      moved KILL->KEEP: oracle {int((~k0 & ks).sum())}, rule-8 {int((~k0 & k8).sum())}"
          f" | moved KEEP->KILL: oracle {int((k0 & ~ks).sum())}, rule-8 {int((k0 & ~k8).sum())}")
        P(f"  4a: KEEP at m=0 {int(a0.sum())} | at rule-8 m8 {int(a8.sum())}"
          f" | moved KILL->KEEP {int((~a0 & a8).sum())}, KEEP->KILL {int((a0 & ~a8).sum())}")
        P(f"  rule-8 m8 != 0 in {int((s['m_8'] != 0).sum())}/{len(s)} books; "
          f"dS_8 > 0 in {int((s['dS_8'] > 0).sum())}/{len(s)}, mean {s['dS_8'].mean():+.4f}; "
          f"dOOS_8 > 0 in {int((s['dOOS_8'] > 0).sum())}/{len(s)}, mean {s['dOOS_8'].mean():+.4f}")
        P(f"  Spearman(IS,OOS) over the 9 m-cells: median {s['spearman_IS_OOS'].median():+.3f}, "
          f"positive in {int((s['spearman_IS_OOS'] > 0).sum())}/{len(s)}")

    # ------------------------------------------------------------- rule 8 detail
    P("\n=== RULE 8 walk-forward: m picked on 2009-2016 IS Sharpe, 2017-2026 untouched")
    wf = []
    for (pan, gate, freq) in CENSUS:
        c = ctx[pan]
        spy_oos = c["spy"].loc[OOS_START:]
        mspy = metrics(spy_oos)
        for bps in RUNGS:
            s = G[(G.panel == pan) & (G.gate == gate) & (G.freq == freq) & (G.bps == bps)].set_index("m")
            m8 = s["IS_Sharpe"].idxmax()
            bo = c["base"][bps].loc[OOS_START:]
            mb = metrics(bo)
            wf.append(dict(panel=pan, gate=gate, freq=freq, bps=bps, m_8=m8,
                           OOS_CAGR=s.loc[m8, "OOS_CAGR"], OOS_Sharpe=s.loc[m8, "OOS_Sharpe"],
                           OOS_MaxDD=s.loc[m8, "OOS_MaxDD"],
                           parent_OOS_CAGR=s.loc[0, "OOS_CAGR"], parent_OOS_Sharpe=s.loc[0, "OOS_Sharpe"],
                           parent_OOS_MaxDD=s.loc[0, "OOS_MaxDD"],
                           gridmean_OOS_Sharpe=s["OOS_Sharpe"].mean(),
                           best_OOS_Sharpe=s["OOS_Sharpe"].max(), best_OOS_m=s["OOS_Sharpe"].idxmax(),
                           base_OOS_CAGR=mb["CAGR"], base_OOS_Sharpe=mb["Sharpe"], base_OOS_MaxDD=mb["MaxDD"],
                           spy_OOS_CAGR=mspy["CAGR"], spy_OOS_Sharpe=mspy["Sharpe"], spy_OOS_MaxDD=mspy["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for bps in RUNGS:
        s = WF[WF.bps == bps]
        P(f"@{bps}bps: rule-8 pick beats its own parent OOS in "
          f"{int((s['OOS_Sharpe'] > s['parent_OOS_Sharpe']).sum())}/{len(s)} books, "
          f"beats the grid mean in {int((s['OOS_Sharpe'] > s['gridmean_OOS_Sharpe']).sum())}/{len(s)}, "
          f"is the OOS-best m in {int((s['m_8'] == s['best_OOS_m']).sum())}/{len(s)}; "
          f"mean OOS dSharpe vs parent {(s['OOS_Sharpe'] - s['parent_OOS_Sharpe']).mean():+.4f}")

    # -------------------------------------------------- cost-rung robustness (reporting axis)
    P("\n=== ROBUSTNESS: every rule-8 cell that KEEPs 4b @10bps, re-costed at 5/10/25/50 bps")
    P("(the cost rung is a REPORTING axis, never a tuned one; 10 bps remains the verdict rung)")
    rb = []
    keep8 = V[(V.bps == 10) & V.v4b_8.str.startswith("KEEP")]
    for _, k in keep8.iterrows():
        pan, gate, freq, m8 = k["panel"], k["gate"], k["freq"], int(k["m_8"])
        c = ctx[pan]
        res = cells[(pan, gate, freq, m8)]
        for bps in [5, 10, 25, 50]:
            r = rets(res, bps, c["start"])
            base = rets(run0(px[pan], rules_v2_weights(px[pan]), "W"), bps, c["start"])
            d = cell_stats(r, res, c["start"], c["spy"], c["spy_oos_s"], base)
            rb.append(dict(panel=pan, gate=gate, freq=freq, m=m8, bps=bps,
                           CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"], H1=d["H1"],
                           H2=d["H2"], OOS_Sharpe=d["OOS_Sharpe"], turn_yr=d["turn_yr"],
                           v4b=d["v4b"], v4a=d["v4a"]))
    RB = pd.DataFrame(rb)
    RB.to_csv(f"{OUT}.rungs.csv", index=False)
    P(RB.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    surv = RB.groupby(["panel", "gate", "freq", "m"])["v4b"].apply(lambda s: int(s.str.startswith("KEEP").sum()))
    P("4b KEEPs across the 4 rungs (5/10/25/50 bps), per rule-8 cell:")
    P(surv.to_string())


    Path(f"{OUT}.console.txt").write_text("\n".join(_LINES) + "\n")
    P(f"\nwrote {OUT.name}.console.txt/.census.csv/.grid.csv/.verdicts.csv/.rungs.csv/.walkforward.csv")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LINES) + "\n")


if __name__ == "__main__":
    main()
