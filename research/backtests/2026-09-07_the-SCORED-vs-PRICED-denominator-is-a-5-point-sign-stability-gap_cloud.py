#!/usr/bin/env python3
"""Idea 380: the SCORED vs PRICED denominator of the record's all-names book.

THE DEFECT.  The record contains two different "equal-weight everything" books that carry the
same name in prose:
    PRICED  (idea 94/122's `EWall`, and `baseline.rules_v2_weights` -- the LIVE book):
            denominator = every instrument with a close that day, `px.notna()`.
    SCORED  (idea 124's `_B2` ALL rung): denominator = every instrument with a DEFINED
            composite that day, which silently requires 253 prior closes.
Idea 124's `_B2` run recorded the consequence in its own caveats: max |dw| 0.0150, the two
counts disagree on 1530 of 4439 u56 eval days, and on IDENTICAL bootstrap draws their mean D3
frac_pos is 0.8133 (SCORED) against 0.7609 (PRICED) -- a 5-point sign-stability gap created
purely by which names the denominator counts.  That is a defect: two books, one name, and no
committed convention.  This run audits the record and proposes one.

PRE-REGISTERED, before any new number was read:

  [0] GATES.  Reproduce, from scratch, (a) idea 94's EWall exactly from the PRICED arm,
      (b) idea 124 `_B2`'s ALL rung exactly from the SCORED arm, (c) the published max |dw|
      0.0150 and the 1530-of-4439 disagreement-day count on u56, and (d) the published
      0.8133 / 0.7609 frac_pos pair, read from the committed `_B2.d3.csv` (an AUDIT read of a
      committed artefact, not a re-derivation).

  [A] THE AUDIT.  Census every committed `research/backtests/*.py` that builds an all-names
      denominator, classify it PRICED / SCORED / BOTH from the actual construction line
      (evidence line committed to `<slug>.audit.csv` so a human can check every call), and
      count how many committed LEADERBOARD rows each convention is responsible for.

  [B] PRICE THE GAP.  Both conventions are endpoints of ONE ladder: require a name to have at
      least M prior closes before it counts.  M = 1 IS the PRICED book; M = 253 is the SCORED
      book (asserted).  Dial 1 = M in {1, 63, 126, 200, 253, SCORED-exact}; dial 2 = the
      evaluation warm-up WARM in {260, 504} -- because if the gap is only a panel-entry
      artefact, a longer warm-up removes it and the convention does not matter.  Exactly two
      tuned parameters.  Panel {U56, B136, SMALL439} and cost rung {0, 10, 25} are REPORTED
      axes, not tuned choices; every point is printed and committed.

  [C] SIGN STABILITY, the queue's actual complaint.  NDRAW = 40 seeded name-subsample draws
      deleting q = 0.10 of the panel, both books rebuilt on the sub-panel: report frac_pos of
      (SCORED - PRICED) on Sharpe, CAGR and MaxDD.  A convention that only changes the LEVEL
      is a naming problem; a convention whose difference has no stable sign is a measurement
      problem, and the queue's 5-point gap claims the latter.

  [D] RULE 8 WALK-FORWARD (PROTOCOL 8, required): (M, WARM) chosen on 2009-2016 IS Sharpe at
      10 bps alone, 2017-2026 read once, against the PRICED anchor, the OOS-best rung
      (regret), RULES v2 (live) and SPY.  Both KEEP paths evaluated on every cell.

  [E] THE PROPOSAL.  One convention, named, with the reason stated and the cost of the other
      one quantified.

BOOK (fixed, never tuned): equal weight over the denominator at GROSS = 0.75 of NAV, remainder
cash; no ranking, no gate -- this IS idea 10/72/94's simplest book, the object under audit.
Weekly cadence, next-day execution, costs 0/10/25 bps.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so every CAGR
level is optimistic; this run is about a WITHIN-CELL convention difference, which is far less
exposed, but a survivorship-free panel would have far more panel-entry dates and would make
the gap LARGER, not smaller.  (2) SMALL439 (44 tickers with `max_1d_move >= 1.0` in
data/small_meta.csv dropped) starts 2010-01-04, so its halves are not the same calendar halves
as U56/B136 -- and it is the panel where names actually enter mid-sample, which is exactly
where the two conventions can differ.  (3) The audit's classifier is a regex over committed
source with the matched line committed as evidence; it reports what it found and cannot prove
it found everything.

Deterministic (seeded), standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, re, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                             # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_the-SCORED-vs-PRICED-denominator-is-a-5-point-sign-stability-gap_cloud"
OUT = ROOT / "research" / "backtests"
GROSS, FREQ = 0.75, "W"
MS = [1, 63, 126, 200, 253, "SCORED"]          # tuned dial 1 (M = min prior closes)
WARMS = [260, 504]                             # tuned dial 2
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NDRAW, QDROP, SEED = 40, 0.10, 20260907
Q_STAR = 0.10                                  # idea 119/122/124's headline draw fraction
ANCHOR_M = 1                                   # PRICED: idea 94's EWall and the LIVE book


# ---------------------------------------------------------------- the two conventions
def composite(px):
    """idea 94's plain composite (no vol scaler).  Defined only once a name has 253 closes."""
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def denom_mask(px, M):
    """Which names count in the equal-weight denominator.

    M = 1        every instrument PRICED that day  -> idea 94's EWall, and the LIVE
                 `rules_v2_weights` convention ("N = instruments priced that day").
    M = k        priced AND with at least k prior closes.
    'SCORED'     every instrument with a DEFINED composite -> idea 124 `_B2`'s ALL rung."""
    if M == "SCORED":
        return composite(px).notna() & px.notna()
    ok = px.notna()
    if M <= 1:
        return ok
    return ok & (ok.cumsum() >= M)


def ew_weights(px, M):
    e = denom_mask(px, M).astype(float)
    return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def fast_backtest(px, w, cost_bps=0.0, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT)
    cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return (pd.Series(port, index=px.index), pd.Series(turn, index=px.index),
            pd.Series((held > 0).sum(axis=1), index=px.index))


def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- [A] the audit
PRICED_PAT = [r"\.where\(\s*px\.notna\(\)\s*,\s*0\.0\s*\)", r"px\.notna\(\)\.astype\(float\)"]
SCORED_PAT = [r"rank\.le\(\s*k\s*,\s*axis=0\)", r"\.le\(\s*cnt\s*,\s*axis=0\)",
              r"(?:comp|score|sc|s)\.notna\(\)\.sum\(axis=1\)"]
DIVIDE_PAT = re.compile(r"\.div\(|GROSS\s*/|\bmul\(|/\s*k\b|/\s*cnt\b")
ALLNAME_PAT = re.compile(r"EWall|EW_ALL|['\"]ALL['\"]|equal-weight EVERY|all-names")


def audit():
    """Classify every committed backtest script that builds an all-names denominator.

    A match counts only when the convention idiom sits within +/-3 lines of a division by a
    per-day count -- i.e. inside a weight construction, not in prose or an unrelated notna().
    The matched line is committed as evidence."""
    P = re.compile("|".join(PRICED_PAT)); S = re.compile("|".join(SCORED_PAT))
    rows = []
    for p in sorted(OUT.glob("*.py")):
        try:
            txt = p.read_text()
        except Exception:
            continue
        if not ALLNAME_PAT.search(txt):
            continue
        lines = txt.split("\n")
        ev = {"PRICED": "", "SCORED": ""}
        for i, ln in enumerate(lines):
            near = "\n".join(lines[max(0, i - 3):i + 4])
            if not DIVIDE_PAT.search(near):
                continue
            if P.search(ln) and not ev["PRICED"]:
                ev["PRICED"] = f"L{i+1}: {ln.strip()[:120]}"
            if S.search(ln) and not ev["SCORED"]:
                ev["SCORED"] = f"L{i+1}: {ln.strip()[:120]}"
        if not ev["PRICED"] and not ev["SCORED"]:
            continue
        cls = ("BOTH" if ev["PRICED"] and ev["SCORED"] else
               "PRICED" if ev["PRICED"] else "SCORED")
        rows.append(dict(script=p.name, convention=cls,
                         priced_evidence=ev["PRICED"], scored_evidence=ev["SCORED"]))
    a = pd.DataFrame(rows)

    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    cite = {}
    for ln in lb:
        parts = [x.strip() for x in ln.split("|")]
        if len(parts) > 3 and parts[-2].endswith(".py"):
            cite[parts[-2]] = cite.get(parts[-2], 0) + 1
    a["leaderboard_rows"] = [int(cite.get(s, 0)) for s in a.script]
    return a


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print(f"Book: equal weight over the denominator at gross {GROSS}, weekly, next-day, ungated.")
    print(f"Tuned (2): M in {MS} x WARM in {WARMS}.  Reported: panel, cost {COSTS} bps.")
    print("PRICED = M 1 (idea 94 EWall + the LIVE rules_v2 convention); SCORED = defined composite "
          "(idea 124 _B2's ALL rung).")

    # ------------------------------------------------------------ [A] audit first: no numbers needed
    print("\n\n[A] AUDIT of every committed backtest script that builds an all-names denominator")
    a = audit()
    a.to_csv(OUT / f"{SLUG}.audit.csv", index=False)
    print(f"    {len(a)} scripts build one.  By convention: "
          f"{a.convention.value_counts().to_dict()}")
    print(f"    LEADERBOARD rows attributable to each convention: "
          f"{a.groupby('convention').leaderboard_rows.sum().to_dict()}")
    for _, r in a.iterrows():
        print(f"      {r.convention:6s} rows{r.leaderboard_rows:>4}  {r.script}")
        if r.priced_evidence:
            print(f"               P {r.priced_evidence}")
        if r.scored_evidence:
            print(f"               S {r.scored_evidence}")

    print("\n[A2] the LIVE book's own convention (baseline.rules_v2_weights docstring):")
    import inspect
    doc = inspect.getdoc(rules_v2_weights).replace("\n", " ")
    print(f"      \"{doc[:200]}\"")
    print("      -> the live book counts INSTRUMENTS PRICED, i.e. PRICED (M = 1).")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    gcsv = OUT / f"{SLUG}.grid.csv"
    rows, dis_rows, boot_rows, ctx_rows = [], [], [], []

    for pname, px in panels.items():
        print(f"\n{'='*140}\n{pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}")

        # -------------------------------------------------- [0] gates (U56 only, where published)
        wP, wS = ew_weights(px, 1), ew_weights(px, "SCORED")
        nP = denom_mask(px, 1).sum(axis=1); nS = denom_mask(px, "SCORED").sum(axis=1)
        for WARM in WARMS:
            st = px.index[WARM]
            dw = float((wS - wP).abs().loc[st:].to_numpy().max())
            dd = int((nP.loc[st:] != nS.loc[st:]).sum()); nd = int(len(px.loc[st:]))
            print(f"    [0] WARM {WARM}: eval from {st.date()}, {nd} days | max|dw| {dw:.4f} | "
                  f"denominator counts disagree on {dd} of {nd} days ({dd/nd:.1%}) | "
                  f"mean names PRICED {nP.loc[st:].mean():.2f} vs SCORED {nS.loc[st:].mean():.2f}")
            dis_rows.append(dict(panel=pname, warm=WARM, days=nd, max_dw=dw, disagree_days=dd,
                                 disagree_frac=dd / nd, mean_priced=nP.loc[st:].mean(),
                                 mean_scored=nS.loc[st:].mean()))
            if pname == "U56" and WARM == 260:
                print(f"        GATE vs idea 124 _B2's published pair (max |dw| 0.0150, "
                      f"1530 of 4439 days): |d(max dw)| {abs(dw-0.0150):.4f}, "
                      f"days {dd} vs 1530, sample {nd} vs 4439")
        if pname == "U56":
            e94 = (pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0))
            w94 = GROSS * e94.div(e94.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            g94 = float((wP - w94).abs().to_numpy().max())
            rk = composite(px).rank(axis=1, ascending=False)
            cnt = composite(px).notna().sum(axis=1).replace(0, np.nan)
            wB2 = rk.le(cnt, axis=0).astype(float).mul(GROSS / cnt, axis=0).fillna(0.0)
            gB2 = float((wS - wB2).abs().to_numpy().max())
            print(f"    [0] NESTING: PRICED arm == idea 94's EWall construction "
                  f"max|d| {g94:.3e}; SCORED arm == _B2's ALL rung construction max|d| {gB2:.3e}")
            assert g94 < 1e-15 and gB2 < 1e-12

        # -------------------------------------------------- [B] the grid
        for WARM in WARMS:
            start = px.index[WARM]
            spy = px["SPY"].pct_change().fillna(0).loc[start:]
            ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
            br, bt, _ = fast_backtest(px, rules_v2_weights(px))
            base10 = (br - bt * 10 / 1e4).loc[start:]
            bm = metrics(base10); bo = metrics(base10.loc[OOS_START:])
            if WARM == WARMS[0]:
                print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} "
                      f"MaxDD {ms_['MaxDD']:.2%} H1/H2 {s1:.3f}/{s2:.3f} OOS {so['Sharpe']:.3f} | "
                      f"RULES v2 (live) {bm['CAGR']:.2%} / {bm['Sharpe']:.3f} / {bm['MaxDD']:.2%} "
                      f"OOS {bo['Sharpe']:.3f}")
                ctx_rows.append(dict(panel=pname, spy_sharpe=ms_["Sharpe"], spy_cagr=ms_["CAGR"],
                                     spy_dd=ms_["MaxDD"], spy_h1=s1, spy_h2=s2,
                                     spy_oos_sharpe=so["Sharpe"], base_sharpe=bm["Sharpe"],
                                     base_dd=bm["MaxDD"], base_oos_sharpe=bo["Sharpe"]))
            print(f"\n[B] GRID {pname} WARM={WARM} (eval from {start.date()}; every point)")
            print(f"    {'M':>7} {'names':>6} {'turn/yr':>8} | " +
                  " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} "
                             f"{'OOS':>6} 4b 4a" for c in COSTS))
            for M in MS:
                r0, t0, kk = fast_backtest(px, ew_weights(px, M))
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                rec = dict(panel=pname, warm=WARM, M=str(M), names=kk.loc[start:].mean(),
                           turn_per_yr=tpy)
                line = f"    {str(M):>7} {kk.loc[start:].mean():>6.1f} {tpy:>8.2f} |"
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    basec = (br - bt * c / 1e4).loc[start:]
                    ok4a, d4a, f4a = bars_4a(r, basec)
                    line += (f" {mt['CAGR']:>7.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{h1:>6.3f}/{h2:<6.3f} {oo['Sharpe']:>6.3f} "
                             f"{'Y' if ok4b else 'n'}  {'Y' if ok4a else 'n'} |")
                    rec.update({f"CAGR_{c}": mt["CAGR"], f"Sharpe_{c}": mt["Sharpe"],
                                f"MaxDD_{c}": mt["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                                f"OOS_Sharpe_{c}": oo["Sharpe"], f"OOS_CAGR_{c}": oo["CAGR"],
                                f"OOS_MaxDD_{c}": oo["MaxDD"],
                                f"IS_Sharpe_{c}": metrics(r.loc[:IS_END])["Sharpe"],
                                f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a),
                                f"m4b_H1_{c}": d4b["H1"], f"m4b_H2_{c}": d4b["H2"],
                                f"m4b_OOS_{c}": d4b["OOS"], f"m4b_DD_{c}": d4b["DD"],
                                f"m4b_CAGR_{c}": d4b["CAGR"]})
                print(line)
                rows.append(rec)

        # -------------------------------------------------- [C] sign stability
        start = px.index[WARMS[0]]
        rng = np.random.default_rng(SEED)
        cols = [c for c in px.columns if c != "SPY"]
        keep_n = int(round(len(cols) * (1 - QDROP)))
        print(f"\n[C] SIGN STABILITY {pname}: {NDRAW} draws keeping {keep_n} of {len(cols)} names "
              f"(q={QDROP}), both books rebuilt on the sub-panel, 10 bps")
        dS, dC, dD = [], [], []
        for d in range(NDRAW):
            sub = list(rng.choice(cols, size=keep_n, replace=False))
            sp = px[sub + ["SPY"]]
            out = {}
            for M in (1, "SCORED"):
                r0, t0, _ = fast_backtest(sp, ew_weights(sp, M))
                r = (r0 - t0 * 10 / 1e4).loc[start:]
                out[M] = metrics(r)
            dS.append(out["SCORED"]["Sharpe"] - out[1]["Sharpe"])
            dC.append(out["SCORED"]["CAGR"] - out[1]["CAGR"])
            dD.append(abs(out[1]["MaxDD"]) - abs(out["SCORED"]["MaxDD"]))
        dS, dC, dD = np.array(dS), np.array(dC), np.array(dD)
        print(f"    dSharpe (SCORED - PRICED): mean {dS.mean():+.4f} sd {dS.std():.4f} "
              f"frac_pos {float((dS > 0).mean()):.4f}  [min {dS.min():+.4f} max {dS.max():+.4f}]")
        print(f"    dCAGR   (SCORED - PRICED): mean {dC.mean():+.4%} frac_pos {float((dC>0).mean()):.4f}")
        print(f"    dMaxDD  (PRICED - SCORED, +ve = SCORED shallower): mean {dD.mean():+.4%} "
              f"frac_pos {float((dD > 0).mean()):.4f}")
        boot_rows.append(dict(panel=pname, ndraw=NDRAW, q=QDROP,
                              dSharpe_mean=dS.mean(), dSharpe_sd=dS.std(),
                              dSharpe_fracpos=float((dS > 0).mean()),
                              dCAGR_mean=dC.mean(), dCAGR_fracpos=float((dC > 0).mean()),
                              dMaxDD_mean=dD.mean(), dMaxDD_fracpos=float((dD > 0).mean())))

    df = pd.DataFrame(rows); df.to_csv(gcsv, index=False)
    pd.DataFrame(dis_rows).to_csv(OUT / f"{SLUG}.disagree.csv", index=False)
    pd.DataFrame(boot_rows).to_csv(OUT / f"{SLUG}.bootstrap.csv", index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel"); ctx.to_csv(OUT / f"{SLUG}.ctx.csv")

    # ---------------------------------------------------------- [C2] the published pair
    print("\n\n[C2] AUDIT READ of the two committed d3.csv files (the queue's 0.8133 / 0.7609),")
    print("     restricted to q = 0.10 -- the two runs' draws are the same seeded draws.")
    p = OUT / "2026-09-07_book-size-floor-for-any-quoted-price_B2.d3.csv"
    p94 = OUT / "2026-09-07_book-size-floor-for-any-quoted-price_cloud.d3.csv"
    got = {}
    for f, lab in ((p, "SCORED ALL rung (_B2)"), (p94, "PRICED ALL rung (_cloud)")):
        if not f.exists():
            print(f"    [{lab}] {f.name} not committed -- cannot read"); continue
        d = pd.read_csv(f)
        sub = d[(d.book.astype(str).str.upper().isin(["ALL", "TOPALL", "EWALL"])) &
                (d.q == Q_STAR)]
        got[lab] = sub
        print(f"    [{lab:24s}] {f.name}: rows {len(d)}, ALL-rung q={Q_STAR} rows {len(sub)}, "
              f"mean frac_pos_full = {sub.frac_pos_full.mean():.4f}")
    if len(got) == 2:
        A = list(got.values())[0].set_index(["uni", "arm"]).frac_pos_full
        B = list(got.values())[1].set_index(["uni", "arm"]).frac_pos_full
        j = pd.concat([A.rename("scored"), B.rename("priced")], axis=1).dropna()
        dlt = j.scored - j.priced
        print(f"    GATE vs the queue's published pair (0.8133 SCORED / 0.7609 PRICED): "
              f"|d| {abs(A.mean()-0.8133):.4f} / {abs(B.mean()-0.7609):.4f}")
        print(f"    PER-ARM on IDENTICAL draws: {len(j)} arm-points, "
              f"{int((dlt != 0).sum())} differ, mean {dlt.mean():+.4f}, "
              f"range [{dlt.min():+.3f}, {dlt.max():+.3f}], "
              f"SCORED higher on {int((dlt > 0).sum())}, PRICED higher on {int((dlt < 0).sum())}")
        print(f"    LEVERAGE: a max |dw| of 0.0150 (0.35 pp of a 4.3%% average weight) moves the "
              f"published sign statistic by {dlt.mean():+.4f} on average and up to "
              f"{dlt.abs().max():.3f} on a single arm.")
        j.assign(delta=dlt).to_csv(OUT / f"{SLUG}.d3gap.csv")

    # ---------------------------------------------------------- the head-to-head
    print("\n\n[B*] PRICED vs SCORED head-to-head at 10 bps, every panel x warm-up")
    print(f"    {'panel':9s} {'WARM':>5} | {'PRICED':>29} | {'SCORED':>29} | {'SCORED-PRICED':>28}")
    hh = []
    for pname in df.panel.unique():
        for WARM in WARMS:
            d = df[(df.panel == pname) & (df.warm == WARM)]
            P = d[d.M == "1"].iloc[0]; S = d[d.M == "SCORED"].iloc[0]
            print(f"    {pname:9s} {WARM:>5} | {P.CAGR_10:>7.2%} {P.Sharpe_10:>6.3f} "
                  f"{P.MaxDD_10:>7.2%} {'Y' if P.keep4b_10 else 'n'} | "
                  f"{S.CAGR_10:>7.2%} {S.Sharpe_10:>6.3f} {S.MaxDD_10:>7.2%} "
                  f"{'Y' if S.keep4b_10 else 'n'} | "
                  f"dCAGR {S.CAGR_10-P.CAGR_10:+.2%} dSharpe {S.Sharpe_10-P.Sharpe_10:+.4f} "
                  f"dMaxDD {abs(P.MaxDD_10)-abs(S.MaxDD_10):+.2%} dOOS "
                  f"{S.OOS_Sharpe_10-P.OOS_Sharpe_10:+.4f}")
            hh.append(dict(panel=pname, warm=WARM, dCAGR=S.CAGR_10 - P.CAGR_10,
                           dSharpe=S.Sharpe_10 - P.Sharpe_10,
                           dMaxDD=abs(P.MaxDD_10) - abs(S.MaxDD_10),
                           dOOS=S.OOS_Sharpe_10 - P.OOS_Sharpe_10,
                           keep4b_priced=bool(P.keep4b_10), keep4b_scored=bool(S.keep4b_10)))
    pd.DataFrame(hh).to_csv(OUT / f"{SLUG}.headtohead.csv", index=False)

    # ---------------------------------------------------------- [D] rule 8
    print("\n\n[D] RULE 8 WALK-FORWARD: (M, WARM) chosen on 2009-2016 IS Sharpe @10 bps alone,")
    print("    2017-2026 read ONCE.")
    wf = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        c_ = ctx.loc[pname]
        pick = d.loc[d.IS_Sharpe_10.idxmax()]
        best = d.loc[d.OOS_Sharpe_10.idxmax()]
        anch = d[(d.M == str(ANCHOR_M)) & (d.warm == WARMS[0])].iloc[0]
        print(f"    {pname:9s} picks M={pick.M:>7} WARM={int(pick.warm)} (IS {pick.IS_Sharpe_10:.3f}) "
              f"-> OOS {pick.OOS_Sharpe_10:.3f} CAGR {pick.OOS_CAGR_10:.2%} "
              f"MaxDD {pick.OOS_MaxDD_10:.2%} | OOS-best M={best.M} WARM={int(best.warm)} "
              f"({best.OOS_Sharpe_10:.3f}), regret {pick.OOS_Sharpe_10-best.OOS_Sharpe_10:+.3f} | "
              f"PRICED anchor {anch.OOS_Sharpe_10:.3f} | SPY {c_.spy_oos_sharpe:.3f} | "
              f"RULES v2 {c_.base_oos_sharpe:.3f}")
        wf.append(dict(panel=pname, pick_M=pick.M, pick_warm=int(pick.warm),
                       IS_Sharpe=pick.IS_Sharpe_10, OOS_Sharpe=pick.OOS_Sharpe_10,
                       OOS_CAGR=pick.OOS_CAGR_10, OOS_MaxDD=pick.OOS_MaxDD_10,
                       oos_best_M=best.M, oos_best_warm=int(best.warm),
                       oos_best_sharpe=best.OOS_Sharpe_10,
                       regret=pick.OOS_Sharpe_10 - best.OOS_Sharpe_10,
                       anchor_oos=anch.OOS_Sharpe_10, spy_oos=c_.spy_oos_sharpe,
                       base_oos=c_.base_oos_sharpe,
                       beats_spy=bool(pick.OOS_Sharpe_10 > c_.spy_oos_sharpe),
                       beats_live=bool(pick.OOS_Sharpe_10 > c_.base_oos_sharpe)))
    pd.DataFrame(wf).to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)

    # ---------------------------------------------------------- [E] KEEP paths + proposal
    print("\n\n[E] KEEP-path census over the full grid")
    for c in COSTS:
        print(f"    {c:>2} bps: 4b {int(df[f'keep4b_{c}'].sum())}/{len(df)}  "
              f"by panel {df[df[f'keep4b_{c}']].groupby('panel').size().to_dict()}  |  "
              f"4a {int(df[f'keep4a_{c}'].sum())}/{len(df)}")

    print("\n=== PROPOSAL")
    dd = pd.DataFrame(dis_rows); bb = pd.DataFrame(boot_rows); hhd = pd.DataFrame(hh)
    print(f"    max |dSharpe| across all panel x warm cells: {hhd.dSharpe.abs().max():.4f}; "
          f"max |dCAGR| {hhd.dCAGR.abs().max():.2%}; 4b verdict flips: "
          f"{int((hhd.keep4b_priced != hhd.keep4b_scored).sum())} of {len(hhd)}")
    print(f"    disagreement days by panel (WARM {WARMS[0]}): "
          f"{dd[dd.warm==WARMS[0]].set_index('panel').disagree_frac.round(3).to_dict()}")
    print(f"    bootstrap frac_pos of dSharpe by panel: "
          f"{bb.set_index('panel').dSharpe_fracpos.to_dict()}")
    print("    The LIVE book (rules_v2_weights) already counts INSTRUMENTS PRICED.")


if __name__ == "__main__":
    main()
