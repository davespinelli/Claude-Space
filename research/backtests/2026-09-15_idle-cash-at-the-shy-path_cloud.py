#!/usr/bin/env python3
"""QUEUE idea 899 — does-crediting-IDLE-CASH-at-the-SHY-PATH-move-the-4b-verdict  (cloud, 2026-09-15).

QUESTION (pre-registered, verbatim from QUEUE.md idea 899)
    "idea 642 parked the T-bill path question as 'needs network', but SHY is already a column of
     the offline u56 panel and its adjusted close is a total-return short-Treasury path.
     Re-price the TOP20 candidate's whole gross ladder crediting idle cash at ZERO / flat 150 /
     flat 300 / SHY-path, baselines under the SAME convention, and report whether the g=0.65 pass
     is still one rung wide.  Max 2 params (cash credit, gross rung)."

WHY THIS IS WORTH ONE RUN
    Every de-grossed book in this record is priced with cash earning ZERO (idea 406).  The
    standing 4b candidate holds 35-50% of NAV in cash by construction, so the convention taxes it
    on exactly the leg it fails on — the CAGR floor — and idea 879's whole result is that the book
    passes 4b at g=0.65 on 21 of 21 monthly offsets and at g=0.75 on only 7 of 21.  If a realistic
    cash credit moves that footprint, the record's headline robustness claim is a convention.

THE HYPOTHESES, written out in full BEFORE any number below was read
    H_MOVE   crediting cash changes the 4b verdict of at least one (gross, offset) cell that the
             ZERO convention publishes.  Bar: >= 5% of the 11 x 21 cells flip at the SHY path.
    H_WIDEN  the "one rung wide" property is a convention artefact: under the SHY path the number
             of gross rungs passing 4b on >= 20 of 21 monthly offsets is STRICTLY GREATER than
             under ZERO.
    H_ORDER  the credit is a LEVEL shift, not a re-ranking: the gross rungs keep their order on
             the 4b CAGR margin (Spearman >= +0.95 between the ZERO and SHY margin vectors).
    Declared before running.  H_WIDEN is the one the record's robustness claim depends on.

THE BOOK B*, IMPORTED not re-typed (2026-09-04 shelf KEEP, re-published by idea 879 lane B)
    signal    baseline.score(px, vol_scale=False); gate px > 200d MA AND vol20 < 0.60
    book      top 20 eligible by `rank(ascending=False) <= 20` — the RECORD'S OWN tie convention,
              the one that reproduces idea 879's committed triple (idea 897 measured the sort-tie
              alternative at -0.050 pp CAGR / -0.0093 Sharpe and it is NOT used here)
    weights   g/20 each, shortfall to CASH, NEVER respread
    cadence   MONTHLY, fills t+1, 10 bps (25 bps carried as an audit axis at offset k=0)

THE TWO TUNED PARAMETERS (the only two; every value of both is reported)
    CASH   ZERO      the record's standing convention
           FLAT150   1.50%/yr, daily-compounded            } idea 406's two flat rungs,
           FLAT300   3.00%/yr, daily-compounded            } imported, not chosen here
           SHY       the panel's own SHY adjusted-close daily total return
    GROSS  {0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00} — idea 879's ladder
    OFFSET k = 0..20 trading days after each month end is an AUDIT axis (879's own 21-offset
    calendar test), as is COST {10, 25}.  Every cell is printed; nothing is chosen for reporting.

WHAT SHY IS AND IS NOT — the caveat that decides how much this is worth
    SHY is the 1-3 year Treasury ETF, effective duration ~1.9 years.  It is NOT a 3-month bill
    path: it carries duration return, so it OVERSTATES a cash sleeve in the falling-rate years
    (2009-2021) and UNDERSTATES it in 2022.  It is used because it needs no network and is already
    in the panel.  Its realised return is published below, per half and per OOS window, so the
    reader can see exactly how much credit is being handed out.  SHY is also a tradable
    constituent of this panel, so on days the book holds SHY it is being credited twice in spirit
    (once as a holding, once as the cash numeraire) — the book's SHY holding frequency is
    published below for the same reason.  Treat every SHY number as an UPPER bound on a real cash
    credit over this sample.

PROTOCOL rule 8 walk-forward (required, and read once per convention)
    Under EACH cash convention separately, idea 879's own IS-only selector — the gross rung
    minimising |IS CAGR margin over the 4b floor| on 2009-01-13..2016-12-31 — picks a rung with no
    sight of the OOS window, and OOS 2017-01-01.. is then read ONCE.  The rule-8 question here is
    whether the CONVENTION changes the PICK.

GATES, printed before any hypothesis is read
    G1  the cash simulator with cash_ret = 0 equals engine.backtest EXACTLY (0.0) on returns and
        turnover, at three gross rungs.
    G2  the k=0, g=0.65, ZERO cell reproduces idea 879's committed memo triple
        (12.69% / 1.201 / -17.11%) to within 0.02 pp / 0.01.
    G3  the credit is signed correctly and monotone: full-sample CAGR is non-decreasing in the
        cash rate at every gross rung, and is IDENTICAL across conventions at gross = 1.00 only
        if the book holds no cash there (it does hold cash, so this is reported, not asserted).

CAVEATS carried, not buried
    * SURVIVORSHIP.  research/universe.json is the CURRENT constituent list (idea 54).
    * SPY is NOT credited — it is fully invested, so the 4b bars themselves do not move.  RULES v2
      (live) IS credited under each convention, because it de-grosses and holds cash.
    * 2020 and 2022 are the only real stress episodes in the window.
    * Rule 6: nothing here is a rules change.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, metrics, rebalance_mask                 # noqa: E402

SLUG = "2026-09-15_idle-cash-at-the-shy-path_cloud"
OUT = ROOT / "research" / "backtests"
pd.set_option("display.width", 250)

N_BOOK, MAX_VOL = 20, 0.60
GROSSES = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
OFFSETS = list(range(21))
IS_END, OOS_START = "2016-12-31", "2017-01-01"

px = load_universe()
rets = px.pct_change().fillna(0.0)
comp, above, vol20 = score(px, vol_scale=False)
elig = comp.where(above & (vol20 < MAX_VOL))
rank = elig.rank(axis=1, ascending=False)
W1 = (rank <= N_BOOK).astype(float) / N_BOOK            # gross = 1.0 template
MASK0 = rebalance_mask(px.index, "M")

CASH = {
    "ZERO": pd.Series(0.0, index=px.index),
    "FLAT150": pd.Series((1.015) ** (1 / 252) - 1, index=px.index),
    "FLAT300": pd.Series((1.030) ** (1 / 252) - 1, index=px.index),
    "SHY": px["SHY"].pct_change().fillna(0.0),
}
START = px.index[260]
spy = px["SPY"].pct_change().fillna(0.0).loc[START:]


def offset_mask(k):
    """Rebalance k trading days after each month end (k=0 is engine's own 'M' mask)."""
    if k == 0:
        return MASK0
    return pd.Series(np.roll(MASK0.values, k), index=px.index)


def sim(W, mask, cash_ret, cost_bps):
    """engine.backtest with a cash leg. cash_ret=0 reproduces it exactly (gate G1)."""
    R = rets.values
    Wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    M = mask.shift(1, fill_value=False).values
    rc = cash_ret.reindex(px.index).fillna(0.0).values
    n = len(px.index)
    cur = np.zeros(W.shape[1])
    port = np.zeros(n); turn = np.zeros(n); held_sum = np.zeros(n)
    for i in range(n):
        if M[i] or i == 0:
            new = Wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held_sum[i] = cur.sum()
        port[i] = (cur * R[i]).sum() + (1 - cur.sum()) * rc[i] - turn[i] * cost_bps / 1e4
        growth = cur * (1 + R[i])
        tot = growth.sum() + (1 - cur.sum()) * (1 + rc[i])
        cur = growth / tot if tot > 0 else cur
    return (pd.Series(port, index=px.index), pd.Series(turn, index=px.index),
            pd.Series(held_sum, index=px.index))


def four_b(r, bench):
    a, s = metrics(r), metrics(bench)
    h = len(r) // 2
    a1, a2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    s1, s2 = metrics(bench.iloc[:h])["Sharpe"], metrics(bench.iloc[h:])["Sharpe"]
    ok = (a1 > s1) and (a2 > s2) and (a["MaxDD"] >= 0.60 * s["MaxDD"]) and (a["CAGR"] >= 0.70 * s["CAGR"])
    return ok, dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=a1, H2=a2,
                    h1=a1 > s1, h2=a2 > s2, dd=a["MaxDD"] >= 0.60 * s["MaxDD"],
                    cagr=a["CAGR"] >= 0.70 * s["CAGR"],
                    cagr_margin_pp=100 * (a["CAGR"] - 0.70 * s["CAGR"]),
                    dd_margin_pp=100 * (a["MaxDD"] - 0.60 * s["MaxDD"]))


def four_a(r, base):
    h = len(r) // 2
    return (metrics(r.iloc[:h])["Sharpe"] > metrics(base.iloc[:h])["Sharpe"]
            and metrics(r.iloc[h:])["Sharpe"] > metrics(base.iloc[h:])["Sharpe"]
            and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# ---------------------------------------------------------------- gates
print("=" * 110)
print("GATES (printed before any hypothesis is read)")
print("=" * 110)
worst_r = worst_t = 0.0
for g in (0.50, 0.65, 1.00):
    e = backtest(px, W1 * g, cost_bps=10, freq="M")
    p, t, _ = sim(W1 * g, MASK0, CASH["ZERO"], 10)
    worst_r = max(worst_r, float((p - e["returns"]).abs().max()))
    worst_t = max(worst_t, float((t - e["turnover"]).abs().max()))
print(f"G1 sim(cash=0) vs engine.backtest at g in {{0.50,0.65,1.00}}: max|dr| {worst_r:.3e}  "
      f"max|dturnover| {worst_t:.3e}   -> {'PASS' if max(worst_r, worst_t) == 0.0 else 'FAIL'}")

p065, _, hs065 = sim(W1 * 0.65, MASK0, CASH["ZERO"], 10)
m = metrics(p065.loc[START:])
print(f"G2 (k=0, g=0.65, ZERO) vs idea 879 memo (12.69% / 1.201 / -17.11%): "
      f"{m['CAGR']:.2%} / {m['Sharpe']:.3f} / {m['MaxDD']:.2%}   -> "
      f"{'PASS' if abs(m['CAGR']-0.1269) < 2e-4 and abs(m['Sharpe']-1.201) < 0.01 and abs(m['MaxDD']+0.1711) < 2e-4 else 'FAIL'}")

cagr_by = {}
for g in GROSSES:
    for c in CASH:
        pr, _, _ = sim(W1 * g, MASK0, CASH[c], 10)
        cagr_by[(g, c)] = metrics(pr.loc[START:])["CAGR"]
mono = all(cagr_by[(g, "ZERO")] <= cagr_by[(g, "FLAT150")] <= cagr_by[(g, "FLAT300")] for g in GROSSES)
print(f"G3 CAGR non-decreasing in the flat cash rate at all 11 gross rungs: "
      f"{'PASS' if mono else 'FAIL'}")

# what the credit actually is
shy_r = CASH["SHY"].loc[START:]
h = len(shy_r) // 2
print(f"\nWHAT IS BEING HANDED OUT — SHY realised return over the priced sample: "
      f"full {metrics(shy_r)['CAGR']:.3%}/yr, H1 {metrics(shy_r.iloc[:h])['CAGR']:.3%}, "
      f"H2 {metrics(shy_r.iloc[h:])['CAGR']:.3%}, OOS 2017+ {metrics(shy_r.loc[OOS_START:])['CAGR']:.3%}  "
      f"(vs FLAT150 1.500% and FLAT300 3.000% by construction)")
cash_share = (1 - hs065.loc[START:]).mean()
shy_held = float((W1.loc[START:]["SHY"] > 0).mean())
print(f"   the book's own idle-cash share at g=0.65: {cash_share:.3f} of NAV on average; "
      f"it holds SHY itself on {shy_held:.1%} of days (the double-count caveat)")

# ---------------------------------------------------------------- k=0 ladder, both costs
print()
print("=" * 110)
print("THE GROSS LADDER AT k=0 — every cell, nothing selected")
print("=" * 110)
base_by_cash = {}
Wv2 = rules_v2_weights(px)
maskW = rebalance_mask(px.index, "W")
for c in CASH:
    pr, _, _ = sim(Wv2, maskW, CASH[c], 10)
    base_by_cash[c] = pr.loc[START:]
rows, cache = [], {}
for c in CASH:
    for g in GROSSES:
        for cost in (10, 25):
            pr, tn, _ = sim(W1 * g, MASK0, CASH[c], cost)
            r = pr.loc[START:]
            cache[(c, g, cost)] = r
            ok, L = four_b(r, spy)
            rows.append(dict(cash=c, gross=g, bps=cost, **L, KEEP4b=ok,
                             KEEP4a=four_a(r, base_by_cash[c])))
lad = pd.DataFrame(rows)
lad.to_csv(OUT / f"{SLUG}.ladder.csv", index=False)
for cost in (10, 25):
    print(f"\n--- {cost} bps, k=0 ---")
    print(lad[lad.bps == cost][["cash", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                "cagr_margin_pp", "dd_margin_pp", "KEEP4b", "KEEP4a"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
sm = metrics(spy)
print(f"\nSPY (NOT credited — fully invested): {sm['CAGR']:.2%} / {sm['Sharpe']:.3f} / "
      f"{sm['MaxDD']:.2%}  [4b bars: CAGR floor {0.70*sm['CAGR']:.2%}, DD cap {0.60*sm['MaxDD']:.2%}]")
for c in CASH:
    bm = metrics(base_by_cash[c])
    print(f"RULES v2 (live), cash={c:7s}: {bm['CAGR']:.2%} / {bm['Sharpe']:.3f} / {bm['MaxDD']:.2%}")

# ---------------------------------------------------------------- 21 offsets
print()
print("=" * 110)
print("H_MOVE / H_WIDEN — the 21-offset calendar test at 10 bps, all 4 conventions x 11 rungs")
print("=" * 110)
cells = []
for c in CASH:
    for g in GROSSES:
        for k in OFFSETS:
            pr, _, _ = sim(W1 * g, offset_mask(k), CASH[c], 10)
            ok, L = four_b(pr.loc[START:], spy)
            cells.append(dict(cash=c, gross=g, k=k, KEEP4b=ok, cagr_margin_pp=L["cagr_margin_pp"],
                              dd_margin_pp=L["dd_margin_pp"], h1=L["h1"], h2=L["h2"],
                              dd=L["dd"], cagr=L["cagr"]))
cdf = pd.DataFrame(cells)
cdf.to_csv(OUT / f"{SLUG}.offsets.csv", index=False)
piv = cdf.pivot_table(index="gross", columns="cash", values="KEEP4b", aggfunc="sum")[list(CASH)]
print("\n4b passes out of 21 monthly offsets, by gross rung and cash convention:")
print(piv.to_string())
z = cdf[cdf.cash == "ZERO"].set_index(["gross", "k"]).KEEP4b
flips = {c: int((cdf[cdf.cash == c].set_index(["gross", "k"]).KEEP4b != z).sum()) for c in CASH}
print(f"\nH_MOVE: cells flipping vs ZERO out of {len(z)}: " +
      ", ".join(f"{c} {flips[c]} ({flips[c]/len(z):.1%})" for c in CASH if c != "ZERO"))
print(f"   -> {'PASS' if flips['SHY']/len(z) >= 0.05 else 'FAIL'} (bar: >= 5% at the SHY path)")
wide = {c: int((piv[c] >= 20).sum()) for c in CASH}
print(f"\nH_WIDEN: gross rungs passing 4b on >= 20 of 21 offsets: " +
      ", ".join(f"{c} {wide[c]}" for c in CASH))
print(f"   -> {'PASS' if wide['SHY'] > wide['ZERO'] else 'FAIL'} (bar: SHY strictly > ZERO)")
mz = cdf[(cdf.cash == "ZERO") & (cdf.k == 0)].set_index("gross").cagr_margin_pp
ms = cdf[(cdf.cash == "SHY") & (cdf.k == 0)].set_index("gross").cagr_margin_pp
rho = float(mz.rank().corr(ms.rank()))          # Spearman = Pearson on ranks (no scipy here)
print(f"\nH_ORDER: spearman(ZERO margin, SHY margin) over the 11 rungs at k=0 = {rho:+.4f}  "
      f"-> {'PASS' if rho >= 0.95 else 'FAIL'} (bar: >= +0.95)")

# ---------------------------------------------------------------- rule 8
print()
print("=" * 110)
print("PROTOCOL RULE 8 — idea 879's own IS-only selector, run under EACH convention, OOS read ONCE")
print("=" * 110)
oos_spy = spy.loc[OOS_START:]
wf = []
for c in CASH:
    marg = {}
    for g in GROSSES:
        r_is = cache[(c, g, 10)].loc[:IS_END]
        s_is = spy.loc[:IS_END]
        marg[g] = metrics(r_is)["CAGR"] - 0.70 * metrics(s_is)["CAGR"]
    pick = min(GROSSES, key=lambda g: abs(marg[g]))
    o = cache[(c, pick, 10)].loc[OOS_START:]
    ok, L = four_b(o, oos_spy)
    mo = metrics(o)
    ho = len(o) // 2
    wf.append(dict(cash=c, IS_pick_gross=pick, IS_margin_pp=100 * marg[pick],
                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                   oosH1=metrics(o.iloc[:ho])["Sharpe"], oosH2=metrics(o.iloc[ho:])["Sharpe"],
                   OOS_4b=ok, OOS_4a=four_a(o, base_by_cash[c].loc[OOS_START:])))
wfdf = pd.DataFrame(wf).set_index("cash")
print(wfdf.to_string(float_format=lambda x: f"{x:.4f}"))
wfdf.to_csv(OUT / f"{SLUG}.walkforward.csv")
om = metrics(oos_spy)
print(f"\nSPY OOS: {om['CAGR']:.2%} / {om['Sharpe']:.3f} / {om['MaxDD']:.2%}  "
      f"[OOS 4b bars: CAGR floor {0.70*om['CAGR']:.2%}, DD cap {0.60*om['MaxDD']:.2%}]")
for c in CASH:
    b = base_by_cash[c].loc[OOS_START:]
    bm = metrics(b)
    print(f"RULES v2 (live) OOS, cash={c:7s}: {bm['CAGR']:.2%} / {bm['Sharpe']:.3f} / {bm['MaxDD']:.2%}")
print(f"\nRULE 8 CONTENT: the IS selector picks gross "
      f"{ {c: wfdf.loc[c, 'IS_pick_gross'] for c in CASH} } under the four conventions.")
print("\nWrote: .ladder.csv  .offsets.csv  .walkforward.csv")
