#!/usr/bin/env python3
"""QUEUE idea 92 — sharpe-bound-books-need-a-book-change (cloud, 2026-09-04).

Question (pre-registered, from QUEUE)
------------------------------------
Idea 84 found that on a SHARPE-bound 4b cell no exposure or turnover lever helps: on
`C2/CAND20` over `universe_broad.json` the H2 margin spans -0.119..-0.020 across 20
gross x entry-budget arms and the best improving move is +0.0027, with 0 conversions.  The
queue therefore asks the complementary question — take that exact cell as the test case and
ask what DOES move H2: sector caps, a per-name weight cap, dropping the ranking entirely, or
a different eligibility gate.  **The deliverable is the list of instruments that are NOT
dials**, i.e. that CANNOT move a Sharpe-bound book, plus whatever does move it.

Test cell (fixed, not chosen here — inherited from ideas 46 and 84)
------------------------------------------------------------------
    C2/CAND20 on universe_broad.json: top-20 eligible by the v1 composite WITHOUT
    /sqrt(vol20), equal weight g/20 with the remainder in cash when E_t < 20, gate =
    price > 200d MA AND vol20 < 0.60, g = 0.75, weekly, next-day execution, 10 bps.
    Published H2 Sharpe 0.814 against SPY's 0.837 — a 4b failure by 0.023 on H2 alone.
`universe.json` (56 names) is run identically as the CONTROL universe, because there the same
book PASSES 4b; an instrument that moves H2 must be shown not to be a broad-only artefact.

The four instrument families (each family sweeps exactly ONE parameter; PROTOCOL rule 4)
-----------------------------------------------------------------------------------------
    SECTOR   sector cap C in {0.15, 0.25, 0.40, 1.00} on CAND20's weights.  Excess weight in
             an over-cap sector is redistributed pro-rata to the under-cap sectors, and only
             the residual that cannot be placed goes to cash (reported).  C=1.00 is the
             control and must reproduce CAND20 exactly.
    WCAP     per-name weight cap w_max in {0.0375, 0.05, 0.075, 0.10}, applied to TWO books:
             CAND20 (equal-weight, where the cap should be definitionally inert — the BIND
             RATE is printed to prove it rather than assert it) and RANKW (the same 20 names
             weighted proportional to 1/rank, a genuinely concentrated book where a cap has
             something to bite).  0.0375 = 0.75/20 is CAND20's own equal weight.
    NORANK   drop the ranking: CAND-n at n in {20, 40, 60} and then EWall (every eligible
             name, no ranking at all, idea 72's book) and ew-band3 (idea 57's book).  This is
             the ranking -> no-ranking continuum on one panel, and idea 82's prediction.
    GATE     the eligibility instrument, holding the CAND20 selection fixed: none / 200d only
             / vol20 only / both (RULES v1's literal gate, the control) / band3 (200d with a
             +/-3% re-entry band) / abs (200d AND 12-1 momentum > 0).

At most two tuned parameters anywhere: the book is fixed and each family sweeps one dial.
ALL arms are reported for both universes at 10 and 25 bps — nothing is selected for display.

Sector labels are PRICE-ONLY and LOOK-AHEAD-FREE (this panel has no sector column)
----------------------------------------------------------------------------------
Each name is assigned, ONCE PER CALENDAR YEAR on the last trading day of the prior year, to
whichever of the 11 SPDR sector ETFs (XLB XLC XLE XLF XLI XLK XLP XLRE XLU XLV XLY, all in
data/prices.csv) its daily returns correlated with most over the PRIOR 756 trading days.
Nothing after the assignment date is used.  Names with <252 days of history at that point are
labelled UNK and are exempt from the cap (reported).  This is a correlation-cluster proxy for
GICS, not GICS: it will put a hardware name in XLK and a "consumer" name that trades like tech
in XLK too.  That is the right object for a RISK cap anyway, and the caveat is stated in the
result.  The assignment's stability is printed (share of names whose label changes year over
year) so the reader can judge how much of the cap is noise.

Pre-registered predictions (written before any number below was read)
---------------------------------------------------------------------
    Q1 The per-name cap is INERT on CAND20 (bind rate 0 except when E_t < 20), so it is not
       an instrument on an equal-weight book at all.  Falsified if bind rate > 1% of days.
    Q2 Following idea 84's own threshold, an instrument "moves H2" if it changes the H2
       Sharpe by more than 0.05 in absolute value.  Levers moved it by <=0.003.
    Q3 (idea 82) Dropping the ranking RAISES H2 on the broad panel — ranking subtracts value
       on large-cap panels and only the eligibility gate earns anything.
    Q4 The gate is the strongest of the four families, because ideas 49/57/61 all found the
       gate instrument, not the selection, carries the book's risk-adjusted return.

Walk-forward (PROTOCOL rule 8): within each family, the dial is chosen by argmax 2009-2016
Sharpe and evaluated untouched on 2017-2026 against RULES v1 and SPY.  Reported per family and
per universe, together with the regret against that family's best OOS arm, so a family that
"moves H2" but is unselectable in-sample is not mistaken for a usable instrument.

KEEP paths 4a and 4b both evaluated for every arm.

SURVIVORSHIP: both panels are current-constituent lists; all CAGR/Sharpe LEVELS are optimistic.
This run compares instruments on the same panel and the same days, so the H2 DELTAS — which
are the result — are far less exposed.  The sector labels inherit the same bias.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-04_sharpe-bound-book-change_cloud"
FREQ, MAX_VOL, GROSS, NCAND, BAND = "W", 0.60, 0.75, 20, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [10, 25]
PCOST = 10
SECTORS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY"]
MOVES_H2 = 0.05          # idea 84's own threshold for "an instrument moved the bar"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)


# ---------------------------------------------------------------- signals
def signals(px, band=0.0, gate="both", absmom=False):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    ma = px.rolling(200).mean()
    if band > 0:
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
        above = raw.ffill().fillna(0.0) > 0.5
    else:
        above = (px > ma).fillna(False)
    if gate == "none":
        elig = pd.DataFrame(True, index=px.index, columns=px.columns) & px.notna()
    elif gate == "200d":
        elig = above
    elif gate == "vol20":
        elig = (vol20 < MAX_VOL).fillna(False)
    else:
        elig = (above & (vol20 < MAX_VOL)).fillna(False)
    if absmom:
        elig = elig & (mom > 0).fillna(False)
    return comp, vol20, elig.fillna(False)


# ---------------------------------------------------------------- sector map
def sector_map(px_all, cols):
    """Look-ahead-free annual assignment: prior-756-day return correlation to 11 SPDRs."""
    rets = px_all.pct_change()
    lab = pd.DataFrame("UNK", index=px_all.index, columns=cols)
    stab = []
    prev = None
    years = sorted({d.year for d in px_all.index})
    for y in years:
        asof = px_all.index[px_all.index < pd.Timestamp(f"{y}-01-01")]
        if len(asof) < 252:
            continue
        win = rets.loc[asof[-756:] if len(asof) >= 756 else asof]
        sec = win[[s for s in SECTORS if s in win.columns]]
        assign = {}
        for c in cols:
            v = win[c] if c in win.columns else None
            if v is None or v.notna().sum() < 252:
                assign[c] = "UNK"; continue
            cc = sec.corrwith(v)
            assign[c] = cc.idxmax() if cc.notna().any() else "UNK"
        s = pd.Series(assign)
        if prev is not None:
            both = (prev != "UNK") & (s != "UNK")
            stab.append(((prev[both] != s[both]).mean(), y))
        prev = s
        idx = px_all.index[px_all.index.year == y]
        lab.loc[idx, :] = np.repeat(s[cols].values[None, :], len(idx), axis=0)
    churn = float(np.mean([a for a, _ in stab])) if stab else np.nan
    return lab, churn


def apply_sector_cap(W, lab, cap):
    """Cap each sector's total weight at `cap`; redistribute pro-rata to under-cap sectors.

    UNK-labelled names are exempt (they carry their weight through untouched).  Any weight
    that cannot be placed without breaching the cap goes to cash; the residual is reported.
    """
    if cap >= 1.0:
        return W, pd.Series(0.0, index=W.index)
    Wv = W.values.copy()
    Lv = lab.reindex(W.index)[W.columns].values
    resid = np.zeros(len(W))
    for s in SECTORS:
        pass
    codes = {s: i for i, s in enumerate(SECTORS)}
    Lc = np.vectorize(lambda x: codes.get(x, -1))(Lv)
    for i in range(Wv.shape[0]):
        w = Wv[i]
        if w.sum() <= 0:
            continue
        c = Lc[i]
        tot = w.sum()
        for _ in range(12):                       # iterate to a fixed point
            over, under_room = 0.0, 0.0
            sums = np.zeros(len(SECTORS))
            for k in range(len(SECTORS)):
                sums[k] = w[c == k].sum()
            lim = cap * tot
            for k in range(len(SECTORS)):
                if sums[k] > lim + 1e-12:
                    over += sums[k] - lim
                else:
                    m = (c == k) & (w > 0)
                    if m.any():
                        under_room += lim - sums[k]
            if over <= 1e-12:
                break
            for k in range(len(SECTORS)):
                m = c == k
                if sums[k] > lim + 1e-12 and sums[k] > 0:
                    w[m] *= lim / sums[k]
            if under_room <= 1e-12:
                resid[i] += over
                break
            place = min(over, under_room)
            for k in range(len(SECTORS)):
                m = (c == k) & (w > 0)
                if m.any() and sums[k] < lim - 1e-12:
                    room = lim - sums[k]
                    add = place * room / under_room
                    w[m] += add * (w[m] / w[m].sum())
            resid[i] += over - place
        Wv[i] = w
    return pd.DataFrame(Wv, index=W.index, columns=W.columns), pd.Series(resid, index=W.index)


# ---------------------------------------------------------------- books
def book_weights(px, kind, n=NCAND, gate="both", band=0.0, absmom=False, g=GROSS):
    comp, vol20, elig = signals(px, band=band, gate=gate, absmom=absmom)
    if kind == "EWALL":
        e = elig.astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g
    rank = comp.where(elig).rank(axis=1, ascending=False)
    if kind == "CAND":                              # idea 2's literal construction
        return (rank <= n).astype(float) * (g / n)
    if kind == "RANKW":                             # 1/rank weights over the same 20 names
        sel = (rank <= n) & rank.notna()
        w = sel.astype(float) / rank.where(sel).fillna(np.inf)
        return w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g
    raise ValueError(kind)


def cap_names(W, wmax):
    """Cap each HELD name at wmax, redistribute the excess pro-rata to the other HELD names.

    Redistribution is confined to names the book already holds — spilling excess onto unheld
    names would silently turn the capped book into a different (wider) book rather than a
    capped version of the same one.  Weight that cannot be placed within the held set goes to
    cash.  Returns (weights, bind rate over rebalance-active days).
    """
    Wv = W.values.copy()
    binds = 0
    for i in range(Wv.shape[0]):
        w = Wv[i]
        if w.sum() <= 0:
            continue
        held = w > 0                                  # the book's own name set, fixed
        if not (w > wmax + 1e-12).any():
            continue
        binds += 1
        # exact water-filling: names above the cap are pinned at it, the rest absorb the
        # excess in proportion to their own weights; terminates in at most n_held rounds.
        base, total = w.copy(), float(w.sum())
        free, fixed_sum = held.copy(), 0.0
        w = np.zeros_like(w)
        while True:
            bs = float(base[free].sum())
            if not free.any() or bs <= 0:
                break                                 # nothing left to take it -> cash
            scale = (total - fixed_sum) / bs
            over = free & (base * scale > wmax + 1e-15)
            if not over.any():
                w[free] = base[free] * scale
                break
            w[over] = wmax
            fixed_sum += wmax * int(over.sum())
            free = free & ~over
        Wv[i] = np.minimum(w, wmax)
    active = int((W.sum(axis=1) > 0).sum())
    return pd.DataFrame(Wv, index=W.index, columns=W.columns), binds / max(active, 1)


# ---------------------------------------------------------------- evaluation
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def eval_arm(r, bars, base):
    h1, h2 = halves(r)
    m = metrics(r)
    oos = metrics(r.loc[OOS_START:])
    f = []
    if not h1 > bars["s1"]: f.append("H1")
    if not h2 > bars["s2"]: f.append("H2")
    if not oos["Sharpe"] > bars["soos"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(bars["sdd"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * bars["scagr"]: f.append("CAGR")
    b1, b2 = halves(base)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                oSharpe=oos["Sharpe"], oCAGR=oos["CAGR"], oMaxDD=oos["MaxDD"],
                p4b=(not f), fails=(",".join(f) if f else "-"),
                p4a=bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= metrics(base)["MaxDD"]))


# ---------------------------------------------------------------- per universe
def run_universe(uname, px, px_all, out):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = bars_of(spy)
    ms = metrics(spy)
    base_r = backtest(px, rules_v1_weights(px), cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
    mb = metrics(base_r); b1, b2 = halves(base_r)
    rows_per_yr = len(px) / ((px.index[-1] - px.index[0]).days / 365.25)

    cols = [c for c in px.columns]
    lab, churn = sector_map(px_all, cols)

    print("\n" + "=" * 215)
    print(f"UNIVERSE {uname}: {px.shape[1]} names | eval {start.date()} -> {px.index[-1].date()}"
          f" | H1/H2 split at {px.loc[start:].index[len(px.loc[start:])//2].date()}"
          f" | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"INDEX SANITY {rows_per_yr:.1f} rows/yr -> "
          f"{'OK trading-day index' if 240 < rows_per_yr < 260 else 'BAD — results unsafe'}")
    print(f"SPY   CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS {bars['soos']:.3f}")
    print(f"RULES v1 @{PCOST}bps  CAGR {mb['CAGR']:.2%}  Sharpe {mb['Sharpe']:.3f}  "
          f"MaxDD {mb['MaxDD']:.2%}  halves {b1:.3f}/{b2:.3f}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f}(H1) / {bars['s2']:.3f}(H2) / {bars['soos']:.3f}(OOS), "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    lastlab = lab.iloc[-1]
    print(f"SECTOR LABELS (price-only, annual, look-ahead-free): "
          f"{dict(lastlab.value_counts())} | mean YoY label churn {churn:.1%}")
    print("=" * 215)

    W0 = book_weights(px, "CAND")                    # the test cell
    Wr = book_weights(px, "RANKW")
    arms = {}

    # ---- family SECTOR
    for cap in [1.00, 0.40, 0.25, 0.15]:
        W, resid = apply_sector_cap(W0, lab, cap)
        arms[("SECTOR", f"cap={cap:.2f}")] = (W, dict(resid=float(resid.loc[start:].mean()),
                                                      gross=float(W.loc[start:].sum(axis=1).mean())))
    # ---- family WCAP on the equal-weight book and on the rank-weighted book
    for wmax in [0.0375, 0.05, 0.075, 0.10]:
        W, br = cap_names(W0, wmax)
        arms[("WCAP-EW", f"wmax={wmax:.4f}")] = (W, dict(bind=br,
                                                 gross=float(W.loc[start:].sum(axis=1).mean())))
        W, br = cap_names(Wr, wmax)
        arms[("WCAP-RANKW", f"wmax={wmax:.4f}")] = (W, dict(bind=br,
                                                    gross=float(W.loc[start:].sum(axis=1).mean())))
    arms[("WCAP-RANKW", "uncapped")] = (Wr, dict(bind=0.0,
                                                 gross=float(Wr.loc[start:].sum(axis=1).mean())))
    # ---- family NORANK
    for n in [20, 40, 60]:
        W = book_weights(px, "CAND", n=n)
        arms[("NORANK", f"CAND n={n}")] = (W, dict(gross=float(W.loc[start:].sum(axis=1).mean())))
    W = book_weights(px, "EWALL")
    arms[("NORANK", "EWall (no ranking)")] = (W, dict(gross=float(W.loc[start:].sum(axis=1).mean())))
    W = book_weights(px, "EWALL", band=BAND)
    arms[("NORANK", "ew-band3 (no ranking)")] = (W, dict(gross=float(W.loc[start:].sum(axis=1).mean())))
    # ---- family GATE (selection held at CAND20)
    for tag, kw in (("both (v1, control)", dict(gate="both")), ("none", dict(gate="none")),
                    ("200d only", dict(gate="200d")), ("vol20 only", dict(gate="vol20")),
                    ("band3", dict(gate="both", band=BAND)),
                    ("abs (200d & mom>0)", dict(gate="both", absmom=True))):
        W = book_weights(px, "CAND", **kw)
        arms[("GATE", tag)] = (W, dict(gross=float(W.loc[start:].sum(axis=1).mean())))

    rows = []
    for (fam, tag), (W, extra) in arms.items():
        for c in COSTS:
            r = backtest(px, W, cost_bps=c, freq=FREQ)["returns"].loc[start:]
            to = backtest(px, W, cost_bps=0.0, freq=FREQ)["turnover"].loc[start:]
            d = eval_arm(r, bars, base_r)
            d.update(uni=uname, family=fam, arm=tag, bps=c,
                     turn=to.sum() / metrics(r)["Years"], **extra)
            rows.append(d)
    df = pd.DataFrame(rows)
    out.append(df)

    ctl = df[(df.family == "SECTOR") & (df.arm == "cap=1.00") & (df.bps == PCOST)].iloc[0]
    ctl2 = df[(df.family == "NORANK") & (df.arm == "CAND n=20") & (df.bps == PCOST)].iloc[0]
    print(f"CONTROL CHECK 1: SECTOR cap=1.00 must equal NORANK CAND n=20 (both are CAND20): "
          f"Sharpe {ctl.Sharpe:.6f} vs {ctl2.Sharpe:.6f} -> "
          f"{'EXACT' if abs(ctl.Sharpe-ctl2.Sharpe) < 1e-9 else 'MISMATCH — unsafe'}")
    # RANKW capped at 0.75/20 must collapse EXACTLY onto CAND20: same 20 names, and every
    # weight pinned at the cap.  This is the check that catches a mis-specified redistribution.
    Wrc = arms[("WCAP-RANKW", "wmax=0.0375")][0]
    nheld0 = (W0 > 0).sum(axis=1)
    tie = nheld0 > NCAND                     # composite ties make `rank <= 20` select >20 names
    dchk = float((Wrc - W0).abs().values.max())
    dchk_nt = float((Wrc - W0)[~tie].abs().values.max())
    print(f"CONTROL CHECK 2: WCAP-RANKW at wmax=0.75/20 must collapse onto CAND20 weight-for-weight. "
          f"max|diff| = {dchk:.3e} overall, {dchk_nt:.3e} off tie days -> "
          f"{'EXACT off ties' if dchk_nt < 1e-12 else 'MISMATCH — unsafe'}")
    print(f"  (NOT a harness error, and worth recording: on {int(tie.sum())} of {len(tie)} days the "
          f"composite ties and `rank <= {NCAND}` selects {int(nheld0[tie].max()) if tie.any() else 0} "
          f"names, so idea 2's LITERAL `g/n` book runs at up to "
          f"{float((W0.sum(axis=1)).max()):.4f} gross rather than {GROSS:.2f}.)")
    print(f"TEST CELL CAND20 @{PCOST}bps: CAGR {ctl.CAGR:.2%} Sharpe {ctl.Sharpe:.3f} "
          f"MaxDD {ctl.MaxDD:.2%} H1/H2 {ctl.H1:.3f}/{ctl.H2:.3f} OOS {ctl.oSharpe:.3f} "
          f"| H2 margin vs SPY {ctl.H2 - bars['s2']:+.3f} | 4b {'PASS' if ctl.p4b else 'FAIL ('+ctl.fails+')'}")

    for c in COSTS:
        sub = df[df.bps == c].copy()
        sub["dH2"] = sub.H2 - ctl.H2
        sub["dSharpe"] = sub.Sharpe - ctl.Sharpe
        sub["H2margin"] = sub.H2 - bars["s2"]
        print(f"\n--- {uname} | ALL ARMS @ {c} bps (dH2 / dSharpe are vs the CAND20 test cell) ---")
        print(sub[["family", "arm", "gross", "turn", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "dH2", "H2margin", "oSharpe", "dSharpe", "p4a", "p4b", "fails"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- the deliverable: which families move H2 by more than idea 84's threshold
    p = df[df.bps == PCOST].copy()
    p["dH2"] = p.H2 - ctl.H2
    print(f"\n--- {uname} | IS IT A DIAL?  (|dH2| > {MOVES_H2} vs the test cell, {PCOST} bps) ---")
    summ = p.groupby("family").agg(arms=("arm", "count"), dH2_min=("dH2", "min"),
                                   dH2_max=("dH2", "max"),
                                   best_up=("dH2", "max"), n_moved=("dH2", lambda s: int((s.abs() > MOVES_H2).sum())),
                                   n_up=("dH2", lambda s: int((s > MOVES_H2).sum())))
    summ["verdict"] = np.where(summ.n_up > 0, "MOVES H2 UP", np.where(summ.n_moved > 0, "moves H2 DOWN only", "NOT A DIAL"))
    print(summ.to_string(float_format=lambda x: f"{x:+.4f}"))
    conv = p[p.p4b & ~bool(ctl.p4b)]
    print(f"Arms that CONVERT the cell to a 4b pass: {len(conv)}"
          + ("" if conv.empty else " -> " + ", ".join(f"{r.family}/{r.arm}" for r in conv.itertuples())))

    # ---- walk-forward per family
    print(f"\n--- {uname} | WALK-FORWARD (rule 8), per family: dial chosen by argmax IS Sharpe "
          f"(<= {IS_END}), evaluated on OOS >= {OOS_START}, {PCOST} bps ---")
    wf = []
    for fam in ["SECTOR", "WCAP-EW", "WCAP-RANKW", "NORANK", "GATE"]:
        cand = [(tag, W) for (f2, tag), (W, _) in arms.items() if f2 == fam]
        isS = {}
        for tag, W in cand:
            r = backtest(px, W, cost_bps=PCOST, freq=FREQ)["returns"].loc[start:IS_END]
            isS[tag] = metrics(r)["Sharpe"]
        pick = max(isS, key=isS.get)
        oosS = {}
        for tag, W in cand:
            r = backtest(px, W, cost_bps=PCOST, freq=FREQ)["returns"].loc[OOS_START:]
            oosS[tag] = metrics(r)["Sharpe"]
        Wp = dict(cand)[pick]
        ro = backtest(px, Wp, cost_bps=PCOST, freq=FREQ)["returns"].loc[OOS_START:]
        mo = metrics(ro)
        wf.append(dict(family=fam, IS_pick=pick, IS_Sharpe=isS[pick],
                       IS_spread=max(isS.values()) - min(isS.values()),
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       best_OOS_arm=max(oosS, key=oosS.get), best_OOS=max(oosS.values()),
                       regret=mo["Sharpe"] - max(oosS.values())))
    wdf = pd.DataFrame(wf)
    print(wdf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    mo_b = metrics(base_r.loc[OOS_START:]); mo_s = metrics(spy.loc[OOS_START:])
    print(f"OOS references: RULES v1 {mo_b['CAGR']:.2%}/{mo_b['Sharpe']:.3f}/{mo_b['MaxDD']:.2%}  "
          f"| SPY {mo_s['CAGR']:.2%}/{mo_s['Sharpe']:.3f}/{mo_s['MaxDD']:.2%}")
    return df, ctl, bars, wdf


def main():
    # The 11 SPDR sector ETFs live in data/prices.csv; the broad panel lives in
    # data/prices_broad.csv, so the correlation frame must be the UNION of the two.
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()
    out, res = [], {}
    for uname, px in (("universe_broad.json (136, the H2-bound cell)", load_universe(broad=True)),
                      ("universe.json (56, control)", load_universe())):
        etfs = ref[[s for s in SECTORS if s in ref.columns]].reindex(px.index).ffill()
        px_all = pd.concat([px.drop(columns=etfs.columns, errors="ignore"), etfs], axis=1)
        res[uname] = run_universe(uname, px, px_all, out)
    allrows = pd.concat(out, ignore_index=True)
    allrows.to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)

    print("\n" + "=" * 215)
    print("SUMMARY — idea 92: which instruments are dials on a Sharpe-bound book?")
    print("=" * 215)
    print(f"Total reported points: {len(allrows)} (2 universes x {len(allrows)//4} arms x 2 costs)")
    for uname, (df, ctl, bars, wdf) in res.items():
        p = df[df.bps == PCOST].copy()
        p["dH2"] = p.H2 - ctl.H2
        print(f"\n{uname}")
        print(f"  test cell CAND20: H2 {ctl.H2:.3f} vs SPY {bars['s2']:.3f} "
              f"(margin {ctl.H2-bars['s2']:+.3f}), 4b {'PASS' if ctl.p4b else 'FAIL ('+ctl.fails+')'}")
        for fam in ["SECTOR", "WCAP-EW", "WCAP-RANKW", "NORANK", "GATE"]:
            s = p[p.family == fam]
            print(f"    {fam:<12} dH2 range {s.dH2.min():+.3f}..{s.dH2.max():+.3f}  "
                  f"best up {s.dH2.max():+.3f}  "
                  f"{'DIAL' if s.dH2.max() > MOVES_H2 else 'NOT A DIAL (upward)'}  "
                  f"| 4b passes {int(s.p4b.sum())}/{len(s)}")
    print("\nWritten:", ROOT / "research" / "backtests" / f"{STEM}.grid.csv")


if __name__ == "__main__":
    main()
