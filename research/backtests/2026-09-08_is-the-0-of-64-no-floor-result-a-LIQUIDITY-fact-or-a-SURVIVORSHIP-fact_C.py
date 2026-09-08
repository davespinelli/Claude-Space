#!/usr/bin/env python3
"""QUEUE idea 435 — is-the-0-of-64-no-floor-result-a-LIQUIDITY-fact-or-a-SURVIVORSHIP-fact
(lane C, 2026-09-08).

Question (verbatim from QUEUE)
-----------------------------
"idea 428's rule-8 chooser loses to the no-floor control in 0/64 cells on BOTH panels, i.e. every
liquidity floor is a pure cost OOS.  On SMALL439 that is exactly what a current-constituents panel
would produce (the delisted cohort sits in the thin names a floor removes), but U56 has no such
cohort and shows the same sign.  Test whether the U56 result survives a synthetic delisting
haircut applied to the thinnest decile, and report the haircut size that would flip it.
Max 2 params (haircut, decile)."

What is on trial
----------------
Not a book.  A SIGN and its ROBUSTNESS RADIUS.  Idea 428 reports that an IS-chosen liquidity floor
loses to no floor at all, out of sample, in 64 of 64 cells.  Both panels are CURRENT constituents,
so the thin cohort a floor removes is exactly the cohort whose losers were never recorded.  If a
plausible survivorship correction flips the sign, 428's headline is an artefact of the cache; if it
takes an implausible correction, the headline is a liquidity fact and survives.

The measurand is therefore h*, the smallest haircut on the thin cohort at which the floor chooser
starts beating the no-floor control OOS.  h* ALWAYS EXISTS (as h grows the no-floor arm holds a
progressively poisoned cohort while the floor arm does not), so the finding is never "it flips" or
"it does not" — it is the SIZE of h*, read against what a delisting correction could plausibly be.
That asymmetry is stated here, before any number, so a flip cannot be reported as a discovery.

PRE-REGISTERED (fixed before any Q3-Q7 number was read)
-------------------------------------------------------
P1  MECHANICS.  h* is finite and decreasing in the exposed breadth d, because a wider exposed
    cohort overlaps the gated set more.  (A non-monotone h* in d would mean the floor is not
    removing the cohort the haircut poisons, i.e. the survivorship story has no channel at all.)
P2  PANEL ORDERING.  h* is SMALLER on SMALL439 than on U56 at matched d.  The survivorship story
    is a small-cap story: the sub-$2B panel's missing delisted cohort is large, U56's is ~nil.  If
    h* is not smaller on SMALL439 the queue's own diagnosis of its own result is wrong.
P3  PLAUSIBILITY (the actual verdict).  Declared here, as a judgement and not a measurement: a
    delisting correction on a panel of CURRENT US large caps is worth at most low single digits of
    pp/yr on the thinnest decile.  The band adopted for the verdict is 0-5 pp/yr on U56 and
    0-10 pp/yr on SMALL439 (small caps delist far more often and far worse).  h* inside the band
    => 428's 0/64 is CONFOUNDED on that panel; h* outside it => LIQUIDITY FACT, sign survives.
    This band is not derived from the cache and no number in this run was consulted to set it.
P4  BOOK.  No haircut arm clears 4b on SMALL439 at any (h, d); the haircut can only make books
    worse, so 4b passes should be weakly DECREASING in h, and any increase is a bug, not an edge.

The two tuned parameters
------------------------
EXACTLY TWO: the HAIRCUT h and the exposed DECILE BREADTH d.  Everything else is inherited from
idea 428 verbatim (panels, keys, matched-admission ladder, books, conventions, cost rungs, IS/OOS
split) and is re-checked against 428's committed walkforward.csv at h = 0 as a reproduction gate.
The floor LEVEL is not free: it is chosen inside the rule-8 block on 2010..2016 only, exactly as
428 chose it.  Every grid point is reported.

The haircut, two readings
-------------------------
Exposed cohort: for each day, the live names whose 20d-median price sits in the bottom d deciles
of that day's cross-section (d = 1, 2, 3).  This is the same key a PXL floor cuts on, so the
haircut poisons exactly the cohort the floor removes.  SPY (benchmark, not a constituent) is never
exposed.

READING A — DRAG (primary).  Every exposed name-day's gross return is multiplied by
(1-h)**(1/252), i.e. a constant h pp/yr return correction while a name is thin.  Masks, keys,
trend gates and floor levels are computed on the OBSERVED prices and are IDENTICAL at every h, so
each (h, d) is a paired re-pricing of the same books on the same days: admission stays matched at
1e-16 and the only thing that moves is the P&L.  Pre-registered reading of the haircut: it is a
correction to a RECORDED RETURN, not a rewriting of the panel's observable history.

READING B — EVENT (secondary, Shumway-style).  A terminal shock of -30% fires on exposed name-days
with annual hazard lam = h/0.30, the name is dead from the next day (price NaN, mask False, the
proceeds sit in cash until the next rebalance).  Hazard is SOLVED from h so reading B introduces NO
third parameter: its expected annual drag on the exposed cohort equals reading A's h by
construction.  Seeded (SEED=435), so it is deterministic.  Reading B tests whether the removal and
path-dependence channels add anything the smooth drag misses.

Design (PROTOCOL rules 1-9)
---------------------------
Panels     SMALL439 and U56 via idea 428's `build_panels`, verbatim.  SURVIVORSHIP: both are
           CURRENT constituents — which is the whole subject of this run, so it is measured, not
           just disclosed.  No book is proposed on either.
Books      EWALL (no gate) and MA200 (200d trend gate), gross 0.75, conventions rw and dg.
Instrum.   NONE (no floor), PXL on both panels; DV and VOLSH additionally on SMALL439 (volume
           cache).  Levels are 428's matched-admission ladder, solved from the pooled-quantile
           identity on the OBSERVED panel.
Costs      0/5/10/25 bps, all reported; PROTOCOL rung 10 bps for verdicts.
Rule 8     Floor level chosen on 2010..2016 by IS Sharpe within each cell; 2017..2026 read once
           against SPY, the no-floor control and the incumbent.  Re-run at EVERY (h, d).
Both KEEP  4a vs the live RULES v2 book cost-matched; 4b vs SPY + rule 8, on every grid point.
paths      SPY is never haircut, so the 4b bars are constant across h by construction.

Outputs: .console.txt, .cohort.csv, .grid.csv, .walkforward.csv, .crossing.csv, .verdicts.csv,
         .result.md
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_is-the-0-of-64-no-floor-result-a-LIQUIDITY-fact-or-a-SURVIVORSHIP-fact_C"
REF428 = OUT / "2026-09-08_census-the-record-s-other-DOLLAR-floors-and-caps_C.walkforward.csv"

FREQ, GROSS = "W", 0.75
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DV_LEVELS = [0.0, 0.5e6, 1.0e6, 2.0e6, 5.0e6]
BOOKS = ["EWALL", "MA200"]
CONVS = ["rw", "dg"]

HAIRCUTS = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30]   # pp/yr, param 1
DECILES = [1, 2, 3]                                                # breadth, param 2
HAIRCUTS_B = [0.0, 0.03, 0.08, 0.20]                               # event reading (heavier)
SHOCK = -0.30                                                      # Shumway-style terminal return
SEED = 435
SEEDS = [435, 1, 2, 3, 4, 5, 6, 7]     # replication axis, NOT a parameter: reading B is stochastic
BAND = {"U56": 0.05, "SMALL439": 0.10}                             # P3 plausibility band

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# =====================================================================================
# engine helpers (idea 428 verbatim, with the returns matrix made an explicit argument)
# =====================================================================================
def _bt_core(idx, rets, wt, freq=FREQ):
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


def fast_bt(px, w, freq=FREQ):
    """idea 428's fast_bt, bit-identical: returns taken from px itself."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    return _bt_core(px.index, rets, wt, freq)


def fast_bt_r(idx, rets, w, freq=FREQ):
    """Same engine, driven by an explicit (already haircut) returns matrix."""
    wt = w.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    return _bt_core(idx, rets, wt, freq)


def net(gr, tn, bps):
    return gr - tn * bps / 1e4


def mrow(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def trend(px, book):
    if book == "EWALL":
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    if book == "MA200":
        return (px > px.rolling(200).mean()).fillna(False)
    raise ValueError(book)


def weights_ewall(px_notna, selectable, g, conv, gross=GROSS):
    live = px_notna & selectable
    sel = g & live
    num = sel.astype(float)
    den = (live.sum(axis=1) if conv == "dg" else sel.sum(axis=1)).replace(0, np.nan)
    return num.div(den, axis=0).mul(gross).fillna(0.0)


def build_panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep].dropna(how="all").ffill()
    small_tr = {c for c in pxs.columns if c != "SPY"}
    px56 = load_universe()
    tr56 = set(px56.columns)
    P(f"[panels] SMALL439 {len(small_tr)} tradable (+SPY benchmark), "
      f"{pxs.index[0].date()}..{pxs.index[-1].date()}  |  U56 {len(tr56)} tradable, "
      f"{px56.index[0].date()}..{px56.index[-1].date()}")
    return {"SMALL439": (pxs, small_tr), "U56": (px56, tr56)}


def base_mask(px, tradable):
    m = pd.DataFrame(False, index=px.index, columns=px.columns)
    for c in tradable:
        m[c] = True
    return m


T0 = time.time()
P("=" * 118)
P("IDEA 435  is-the-0-of-64-no-floor-result-a-LIQUIDITY-fact-or-a-SURVIVORSHIP-fact "
  "(lane C, 2026-09-08)")
P("=" * 118)
P("Measurand: h*, the haircut on the thin cohort at which the rule-8 floor chooser starts beating")
P("the no-floor control OOS.  h* always exists; the verdict is its SIZE against a band declared")
P(f"before any number was read: P3 band = U56 {BAND['U56']:.0%}/yr, "
  f"SMALL439 {BAND['SMALL439']:.0%}/yr on the exposed cohort.")

PANELS = build_panels()
START = {k: v[0].index[260] for k, v in PANELS.items()}
pxS, trS = PANELS["SMALL439"]
px56, tr56 = PANELS["U56"]
sS, s56 = START["SMALL439"], START["U56"]


def keys_for(pname):
    px, tr = PANELS[pname]
    out = {"PXL": px.rolling(20).median()}
    if pname == "SMALL439":
        vol = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
        out["DV"] = (px * vol).rolling(20).median()
        out["VOLSH"] = vol.rolling(20).median()
    return out


KEYS, SUPPORT, LIVE = {}, {}, {}
for pname in PANELS:
    px, tr = PANELS[pname]
    K = keys_for(pname)
    KEYS[pname] = K
    live = px.notna() & base_mask(px, tr)
    LIVE[pname] = live
    S = live.copy()
    for k in K.values():
        S &= k.notna()
    SUPPORT[pname] = S.loc[START[pname]:]


def pooled(pname, key):
    k = KEYS[pname][key].loc[START[pname]:]
    S = SUPPORT[pname]
    return np.sort(k.values[S.values])


POOL = {(p, k): pooled(p, k) for p in PANELS for k in KEYS[p]}


def admit_share(pname, key, level):
    v = POOL[(pname, key)]
    return float((v >= level).mean())


def level_for_share(pname, key, share):
    v = POOL[(pname, key)]
    if share >= 1.0:
        return float(v[0]) - 1.0
    i = int(np.floor((1.0 - share) * len(v)))
    return float(v[min(max(i, 0), len(v) - 1)])


SHARES = [admit_share("SMALL439", "DV", L) for L in DV_LEVELS]     # 428's ladder, verbatim

MASKS, NOTNA = {}, {}
for pname in PANELS:
    px, tr = PANELS[pname]
    S_full = base_mask(px, tr) & px.notna()
    for k in KEYS[pname].values():
        S_full &= k.notna()
    NOTNA[pname] = px.notna()
    d = {"NONE": S_full}
    for i, L in enumerate(DV_LEVELS):
        if L == 0.0:
            continue
        sh, tag = SHARES[i], f"{L / 1e6:g}M"
        if pname == "SMALL439":
            d[f"DV_{tag}"] = S_full & (KEYS[pname]["DV"] >= L).fillna(False)
            d[f"VOLSH_{tag}"] = S_full & (KEYS[pname]["VOLSH"] >=
                                          level_for_share(pname, "VOLSH", sh)).fillna(False)
        d[f"PXL_{tag}"] = S_full & (KEYS[pname]["PXL"] >=
                                    level_for_share(pname, "PXL", sh)).fillna(False)
    MASKS[pname] = d

# =====================================================================================
# Q1 — the exposed cohort, and how much of it each floor actually removes
# =====================================================================================
P("\n" + "-" * 118)
P("Q1  THE EXPOSED COHORT — bottom d deciles of the daily 20d-median-price cross-section")
P("-" * 118)
EXPOSED = {}
for pname in PANELS:
    px, tr = PANELS[pname]
    key = KEYS[pname]["PXL"].where(SUPPORT[pname].reindex(px.index).fillna(False))
    pct = key.rank(axis=1, pct=True)                   # 0..1, 1 = most expensive
    for d in DECILES:
        EXPOSED[(pname, d)] = (pct <= d / 10.0).fillna(False) & SUPPORT[pname].reindex(
            px.index).fillna(False)

COH = []
P(f"  {'panel':<10}{'d':>3}{'exposed share of support':>26}   overlap: share of the GATED set that "
  f"is exposed  |  share of exposed that the floor GATES")
for pname in PANELS:
    S = SUPPORT[pname]
    nS = float(S.values.sum())
    for d in DECILES:
        E = EXPOSED[(pname, d)].loc[START[pname]:] & S
        nE = float(E.values.sum())
        row = dict(panel=pname, d=d, exposed_share=nE / nS)
        txt = []
        for mname in [m for m in MASKS[pname] if m.startswith("PXL_")]:
            adm = MASKS[pname][mname].loc[START[pname]:] & S
            gated = S & ~adm
            ng = float(gated.values.sum())
            f_ge = float((gated & E).values.sum()) / max(ng, 1.0)      # gated that is exposed
            f_eg = float((gated & E).values.sum()) / max(nE, 1.0)      # exposed that is gated
            row[f"{mname}_gated_is_exposed"] = f_ge
            row[f"{mname}_exposed_is_gated"] = f_eg
            txt.append(f"{mname.split('_')[1]}: {f_ge:.2f}/{f_eg:.2f}")
        COH.append(row)
        P(f"  {pname:<10}{d:>3}{nE / nS:>26.4%}   " + "  ".join(txt))
pd.DataFrame(COH).to_csv(OUT / f"{STEM}.cohort.csv", index=False)
P("  (read as GATED-is-exposed / EXPOSED-is-gated at each PXL rung; the second number is the")
P("   fraction of the poisoned cohort the floor actually avoids — the haircut's lever arm.)")

# =====================================================================================
# Q2 — the haircut machinery
# =====================================================================================
RAW = {p: PANELS[p][0].pct_change().fillna(0.0) for p in PANELS}


def rets_drag(pname, h, d):
    """Reading A: multiply exposed name-days' gross return by (1-h)**(1/252)."""
    if h == 0.0:
        return RAW[pname].values.copy()
    f = (1.0 - h) ** (1.0 / 252.0)
    r = RAW[pname].values.copy()
    E = EXPOSED[(pname, d)].values
    r = np.where(E, (1.0 + r) * f - 1.0, r)
    return r


def event_panel(pname, h, d, seed=SEED):
    """Reading B: -30% terminal shock at hazard lam=h/0.30 on exposed name-days; dead thereafter.
    Returns (rets_matrix, alive_mask_DataFrame)."""
    px = PANELS[pname][0]
    r = RAW[pname].values.copy()
    alive = np.ones(r.shape, dtype=bool)
    if h == 0.0:
        return r, pd.DataFrame(alive, index=px.index, columns=px.columns)
    lam = h / abs(SHOCK)
    p_day = 1.0 - (1.0 - min(lam, 1.0)) ** (1.0 / 252.0) if lam < 1.0 else 1.0 - np.exp(-lam / 252)
    rng = np.random.default_rng(seed)
    E = EXPOSED[(pname, d)].values
    spy = [i for i, c in enumerate(px.columns) if c == "SPY"]
    draw = rng.random(r.shape) < p_day
    fire = draw & E
    for j in spy:
        fire[:, j] = False
    first = np.where(fire.any(axis=0), fire.argmax(axis=0), -1)
    for j in range(r.shape[1]):
        t = first[j]
        if t >= 0:
            r[t, j] = SHOCK
            r[t + 1:, j] = 0.0
            alive[t + 1:, j] = False
    return r, pd.DataFrame(alive, index=px.index, columns=px.columns)


# weights are h-independent under reading A -> build once
W_A = {}
for pname in PANELS:
    px = PANELS[pname][0]
    for mname, mask in MASKS[pname].items():
        for book in BOOKS:
            g = trend(px, book)
            for conv in CONVS:
                W_A[(pname, mname, book, conv)] = weights_ewall(NOTNA[pname], mask, g, conv)

# =====================================================================================
# Q3 — reproduction gates (bind before any new number is read)
# =====================================================================================
P("\n" + "-" * 118)
P("Q3  REPRODUCTION GATES")
P("-" * 118)
w_probe = W_A[("SMALL439", "NONE", "MA200", "dg")]
r_eng = backtest(pxS, w_probe, cost_bps=10.0, freq=FREQ)["returns"]
g_, t_, _ = fast_bt_r(pxS.index, rets_drag("SMALL439", 0.0, 1), w_probe)
P(f"  [a] fast_bt_r(h=0) vs engine.backtest      max|diff| = "
  f"{np.abs(r_eng - net(g_, t_, 10)).max():.3e}")
ga, ta, _ = fast_bt(pxS, w_probe)
P(f"  [b] fast_bt_r(h=0) vs idea 428's fast_bt   max|diff| = "
  f"{np.abs(net(ga, ta, 10) - net(g_, t_, 10)).max():.3e}")
for pname in PANELS:
    sp = mrow(PANELS[pname][0]["SPY"].pct_change().fillna(0).loc[START[pname]:])
    P(f"  [c] SPY on the {pname} window: {sp['CAGR']:.2%}/{sp['Sharpe']:.3f}/{sp['MaxDD']:.1%} "
      f"halves {sp['H1']:.3f}/{sp['H2']:.3f}")
gv2, tv2, _ = fast_bt(px56, rules_v2_weights(px56))
v2_full = net(gv2, tv2, PROTO_COST)
mv2_10 = mrow(v2_full.loc[s56:])
P(f"  [d] LIVE RULES v2 on U56 @10bps: {mv2_10['CAGR']:.2%}/{mv2_10['Sharpe']:.4f}/"
  f"{mv2_10['MaxDD']:.2%}   [published 8.66%/1.2056/-12.05%]")

# =====================================================================================
# Q4 — the grid: reading A at every (h, d), every panel x mask x book x conv x cost
# =====================================================================================
P("\n" + "-" * 118)
P("Q4  MAIN GRID (reading A, DRAG) — every haircut x decile x panel x mask x book x conv x cost")
P("-" * 118)
spy_full = {p: PANELS[p][0]["SPY"].pct_change().fillna(0).loc[START[p]:] for p in PANELS}
spy_oos = {p: metrics(spy_full[p].loc[OOS_START:]) for p in PANELS}
spy_m = {p: mrow(spy_full[p]) for p in PANELS}

CONFIGS_A = [(0.0, DECILES[0])] + [(h, d) for h in HAIRCUTS if h > 0 for d in DECILES]
rowsA, RET = [], {}
for (h, d) in CONFIGS_A:
    for pname in PANELS:
        px = PANELS[pname][0]
        st = START[pname]
        rmat = rets_drag(pname, h, d)
        for mname in MASKS[pname]:
            for book in BOOKS:
                for conv in CONVS:
                    gr, tn, ex = fast_bt_r(px.index, rmat, W_A[(pname, mname, book, conv)])
                    for bps in COSTS:
                        r = net(gr.loc[st:], tn.loc[st:], bps)
                        m = mrow(r)
                        RET[("A", h, d, pname, mname, book, conv, bps)] = r
                        rowsA.append(dict(reading="A", h=h, d=d, panel=pname,
                                          inst=mname.split("_")[0], mask=mname, book=book,
                                          conv=conv, bps=bps, **m,
                                          mean_expo=float(ex.loc[st:].mean())))
GA = pd.DataFrame(rowsA)
P(f"  reading A grid points: {len(GA)}  "
  f"({len(CONFIGS_A)} (h,d) configs x panels x masks x {len(BOOKS)} books x {len(CONVS)} convs x "
  f"{len(COSTS)} cost rungs)   [{time.time() - T0:.0f}s]")
P(f"\n  Book-level cost of the haircut at 10 bps (no-floor arm, mean over books x convs), CAGR:")
P(f"  {'h':>6}" + "".join(f"{f'U56 d={d}':>12}" for d in DECILES)
  + "".join(f"{f'SM d={d}':>12}" for d in DECILES))
for h in HAIRCUTS:
    cells = []
    for pname in ["U56", "SMALL439"]:
        for d in DECILES:
            dd = DECILES[0] if h == 0.0 else d
            sub = GA[(GA.reading == "A") & (GA.h == h) & (GA.d == dd) & (GA.panel == pname)
                     & (GA["mask"] == "NONE") & (GA.bps == PROTO_COST)]
            cells.append(sub.CAGR.mean())
    P(f"  {h:>6.0%}" + "".join(f"{c:>12.2%}" for c in cells))

# =====================================================================================
# Q5 — reading B (event/delisting), fewer haircuts, masks rebuilt because names die
# =====================================================================================
P("\n" + "-" * 118)
P(f"Q5  READING B (EVENT) — {SHOCK:.0%} terminal shock, hazard SOLVED as h/{abs(SHOCK):.2f} "
  f"so no third parameter, seed {SEED}")
P("-" * 118)
CONFIGS_B = [(0.0, DECILES[0])] + [(h, d) for h in HAIRCUTS_B if h > 0 for d in DECILES]
rowsB, DEATHS = [], []
for (h, d) in CONFIGS_B:
    for pname in PANELS:
        px = PANELS[pname][0]
        st = START[pname]
        rmat, alive = event_panel(pname, h, d)
        nd = int((~alive.iloc[-1]).sum())
        DEATHS.append(dict(reading="B", h=h, d=d, panel=pname, delisted_names=nd,
                           tradable=len(PANELS[pname][1])))
        notna_b = NOTNA[pname] & alive
        for mname in MASKS[pname]:
            mask_b = MASKS[pname][mname] & alive
            for book in BOOKS:
                g = trend(px, book)
                for conv in CONVS:
                    w = weights_ewall(notna_b, mask_b, g, conv)
                    gr, tn, ex = fast_bt_r(px.index, rmat, w)
                    for bps in COSTS:
                        r = net(gr.loc[st:], tn.loc[st:], bps)
                        m = mrow(r)
                        RET[("B", h, d, pname, mname, book, conv, bps)] = r
                        rowsB.append(dict(reading="B", h=h, d=d, panel=pname,
                                          inst=mname.split("_")[0], mask=mname, book=book,
                                          conv=conv, bps=bps, **m,
                                          mean_expo=float(ex.loc[st:].mean())))
GB = pd.DataFrame(rowsB)
G = pd.concat([GA, GB], ignore_index=True)
G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
DE = pd.DataFrame(DEATHS)
P(f"  reading B grid points: {len(GB)}   TOTAL grid {len(G)}   [{time.time() - T0:.0f}s]")
P(f"  names delisted by the end of sample (of tradable):")
P(f"  {'h':>6}" + "".join(f"{f'U56 d={d}':>12}" for d in DECILES)
  + "".join(f"{f'SM d={d}':>12}" for d in DECILES))
for h in HAIRCUTS_B:
    cells = []
    for pname in ["U56", "SMALL439"]:
        for d in DECILES:
            dd = DECILES[0] if h == 0.0 else d
            sub = DE[(DE.h == h) & (DE.d == dd) & (DE.panel == pname)]
            cells.append(f"{int(sub.delisted_names.iloc[0])}/{int(sub.tradable.iloc[0])}")
    P(f"  {h:>6.0%}" + "".join(f"{c:>12}" for c in cells))

# =====================================================================================
# Q6 — RULE 8 walk-forward at every (reading, h, d); the 0/64 count re-read
# =====================================================================================
P("\n" + "-" * 118)
P("Q6  RULE 8 WALK-FORWARD — floor LEVEL chosen on 2010..2016 only, 2017..2026 read once,")
P("    re-run at every (reading, haircut, decile).  The 64-cell count is idea 428's, reproduced.")
P("-" * 118)
wf = []
for (reading, configs) in (("A", CONFIGS_A), ("B", CONFIGS_B)):
    for (h, d) in configs:
        for pname in PANELS:
            insts = sorted({m.split("_")[0] for m in MASKS[pname] if m != "NONE"})
            for inst in insts:
                cands = [m for m in MASKS[pname] if m.split("_")[0] == inst]
                for book in BOOKS:
                    for conv in CONVS:
                        for bps in COSTS:
                            key = (reading, h, d, pname)
                            isS = {m: metrics(RET[key + (m, book, conv, bps)].loc[:IS_END])
                                   ["Sharpe"] for m in cands}
                            pick = max(isS, key=lambda m: isS[m])
                            mo = metrics(RET[key + (pick, book, conv, bps)].loc[OOS_START:])
                            mnf = metrics(RET[key + ("NONE", book, conv, bps)].loc[OOS_START:])
                            best = max(cands, key=lambda m: metrics(
                                RET[key + (m, book, conv, bps)].loc[OOS_START:])["Sharpe"])
                            wf.append(dict(
                                reading=reading, h=h, d=d, panel=pname, inst=inst, book=book,
                                conv=conv, bps=bps, pick=pick, IS_Sharpe=isS[pick],
                                OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                                OOS_MaxDD=mo["MaxDD"], nofloor_OOS_Sharpe=mnf["Sharpe"],
                                nofloor_OOS_CAGR=mnf["CAGR"], nofloor_OOS_MaxDD=mnf["MaxDD"],
                                oracle_OOS_Sharpe=metrics(RET[key + (best, book, conv, bps)]
                                                          .loc[OOS_START:])["Sharpe"],
                                spy_OOS_Sharpe=spy_oos[pname]["Sharpe"],
                                spy_OOS_CAGR=spy_oos[pname]["CAGR"]))
WF = pd.DataFrame(wf)
WF["edge"] = WF.OOS_Sharpe - WF.nofloor_OOS_Sharpe
WF["edge_cagr"] = WF.OOS_CAGR - WF.nofloor_OOS_CAGR
WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

# --- gate: h=0 must reproduce idea 428's committed walkforward exactly -----------------
base = WF[(WF.reading == "A") & (WF.h == 0.0)].set_index(
    ["panel", "inst", "book", "conv", "bps"]).sort_index()
P(f"  [gate] h=0 cells: {len(base)}   (idea 428 published 64)")
if REF428.exists():
    ref = pd.read_csv(REF428).set_index(["panel", "inst", "book", "conv", "bps"]).sort_index()
    common = base.index.intersection(ref.index)
    dmax = max(float(np.abs(base.loc[common, c] - ref.loc[common, c]).max())
               for c in ["OOS_Sharpe", "OOS_CAGR", "nofloor_OOS_Sharpe", "nofloor_OOS_CAGR"])
    same_pick = int((base.loc[common, "pick"] == ref.loc[common, "pick"]).sum())
    P(f"  [gate] vs idea 428 committed walkforward.csv on {len(common)} shared cells: "
      f"max|diff| {dmax:.3e}; identical picks {same_pick}/{len(common)}")
    P(f"  [gate] 428's headline re-read here: chooser beats no-floor in "
      f"{int((base.edge > 0).sum())}/{len(base)} cells "
      f"(published 0/64); mean edge {base.edge.mean():+.4f} Sharpe, "
      f"{100 * base.edge_cagr.mean():+.3f} pp CAGR")
else:
    P("  [gate] idea 428's walkforward.csv not found — reproduction gate SKIPPED")

P(f"\n  Cells where the IS floor chooser BEATS the no-floor control OOS, by haircut "
  f"(reading A, all {len(base)} cells per (h,d)):")
P(f"  {'h':>6}" + "".join(f"{f'd={d}':>10}" for d in DECILES)
  + f"{'|':>4}{'U56 only (16 cells)':>34}")
for h in HAIRCUTS:
    cells, u56 = [], []
    for d in DECILES:
        dd = DECILES[0] if h == 0.0 else d
        sub = WF[(WF.reading == "A") & (WF.h == h) & (WF.d == dd)]
        cells.append(f"{int((sub.edge > 0).sum())}/{len(sub)}")
        s2 = sub[sub.panel == "U56"]
        u56.append(f"{int((s2.edge > 0).sum())}/{len(s2)}")
    P(f"  {h:>6.0%}" + "".join(f"{c:>10}" for c in cells) + f"{'|':>4}"
      + "".join(f"{c:>11}" for c in u56))

P(f"\n  Mean OOS Sharpe edge (chooser - no-floor), reading A, by panel x haircut:")
P(f"  {'panel':<10}{'h':>7}" + "".join(f"{f'd={d}':>12}" for d in DECILES)
  + f"{'mean edge CAGR pp (d=1)':>26}")
for pname in ["U56", "SMALL439"]:
    for h in HAIRCUTS:
        cells = []
        for d in DECILES:
            dd = DECILES[0] if h == 0.0 else d
            sub = WF[(WF.reading == "A") & (WF.h == h) & (WF.d == dd) & (WF.panel == pname)]
            cells.append(sub.edge.mean())
        d1 = WF[(WF.reading == "A") & (WF.h == h) & (WF.d == DECILES[0])
                & (WF.panel == pname)].edge_cagr.mean()
        P(f"  {pname:<10}{h:>7.0%}" + "".join(f"{c:>12.4f}" for c in cells) + f"{100 * d1:>26.3f}")

# =====================================================================================
# Q7 — h*, the crossing haircut, per cell and per panel
# =====================================================================================
P("\n" + "-" * 118)
P("Q7  h* — THE CROSSING HAIRCUT (linear interpolation in h of the OOS Sharpe edge)")
P("-" * 118)


def crossing(hs, es):
    """Smallest h at which edge first becomes > 0, linearly interpolated; nan if never."""
    for i in range(1, len(hs)):
        if es[i] > 0 and es[i - 1] <= 0:
            if es[i] == es[i - 1]:
                return hs[i]
            return hs[i - 1] + (0 - es[i - 1]) * (hs[i] - hs[i - 1]) / (es[i] - es[i - 1])
    return np.nan if not (len(es) and es[0] > 0) else 0.0


CROSS = []
for reading, HH in (("A", HAIRCUTS), ("B", HAIRCUTS_B)):
    for pname in PANELS:
        insts = sorted({m.split("_")[0] for m in MASKS[pname] if m != "NONE"})
        for inst in insts:
            for d in DECILES:
                for book in BOOKS:
                    for conv in CONVS:
                        for bps in COSTS:
                            es, hs = [], []
                            for h in HH:
                                dd = DECILES[0] if h == 0.0 else d
                                q = WF[(WF.reading == reading) & (WF.h == h) & (WF.d == dd)
                                       & (WF.panel == pname) & (WF.inst == inst)
                                       & (WF.book == book) & (WF.conv == conv) & (WF.bps == bps)]
                                hs.append(h)
                                es.append(float(q.edge.iloc[0]))
                            CROSS.append(dict(reading=reading, panel=pname, inst=inst, d=d,
                                              book=book, conv=conv, bps=bps,
                                              hstar=crossing(hs, es),
                                              edge0=es[0], edge_max=max(es)))
CRALL = pd.DataFrame(CROSS)
CRALL.to_csv(OUT / f"{STEM}.crossing.csv", index=False)
CR = CRALL[CRALL.reading == "A"]
P(f"  {'panel':<10}{'inst':<7}{'d':>3}{'cells':>7}{'crossed <=30%':>15}{'median h*':>12}"
  f"{'min h*':>10}{'max h*':>10}{'P3 band':>10}{'inside band':>13}")
for (pname, inst, d), sub in CR.groupby(["panel", "inst", "d"]):
    ok = sub.hstar.notna()
    inb = (sub.hstar <= BAND[pname]) & ok
    P(f"  {pname:<10}{inst:<7}{d:>3}{len(sub):>7}{int(ok.sum()):>10}/{len(sub):<4}"
      f"{(sub.hstar.median() if ok.any() else np.nan):>12.2%}"
      f"{(sub.hstar.min() if ok.any() else np.nan):>10.2%}"
      f"{(sub.hstar.max() if ok.any() else np.nan):>10.2%}"
      f"{BAND[pname]:>10.0%}{int(inb.sum()):>9}/{len(sub):<4}")
P(f"\n  P1 (h* decreasing in d):")
for (pname, inst), sub in CR.groupby(["panel", "inst"]):
    med = [sub[sub.d == d].hstar.median() for d in DECILES]
    mono = all(not (np.isfinite(med[i]) and np.isfinite(med[i + 1])) or med[i] >= med[i + 1]
               for i in range(len(med) - 1))
    P(f"    {pname:<10}{inst:<7} median h* by d = "
      + "  ".join(f"{m:.2%}" if np.isfinite(m) else "  n/a " for m in med)
      + f"   monotone-decreasing: {mono}")
u56m = CR[CR.panel == "U56"].hstar.median()
smlm = CR[CR.panel == "SMALL439"].hstar.median()
P(f"\n  P2 (h* smaller on SMALL439): U56 median h* "
  f"{u56m:.2%} vs SMALL439 {smlm:.2%}  ->  P2 "
  f"{'HOLDS' if np.isfinite(smlm) and np.isfinite(u56m) and smlm < u56m else 'FAILS'}")
P(f"  P3 (plausibility): U56 cells with h* inside the {BAND['U56']:.0%} band "
  f"{int(((CR.panel == 'U56') & (CR.hstar <= BAND['U56'])).sum())}/"
  f"{int((CR.panel == 'U56').sum())}; SMALL439 inside {BAND['SMALL439']:.0%} "
  f"{int(((CR.panel == 'SMALL439') & (CR.hstar <= BAND['SMALL439'])).sum())}/"
  f"{int((CR.panel == 'SMALL439').sum())}")

P(f"\n  READING B cross-check (event/delisting) — cells where the chooser beats no-floor:")
P(f"  {'h':>6}" + "".join(f"{f'd={d}':>10}" for d in DECILES) + f"{'|':>4}{'U56 only':>22}")
for h in HAIRCUTS_B:
    cells, u56c = [], []
    for d in DECILES:
        dd = DECILES[0] if h == 0.0 else d
        sub = WF[(WF.reading == "B") & (WF.h == h) & (WF.d == dd)]
        cells.append(f"{int((sub.edge > 0).sum())}/{len(sub)}")
        s2 = sub[sub.panel == "U56"]
        u56c.append(f"{int((s2.edge > 0).sum())}/{len(s2)}")
    P(f"  {h:>6.0%}" + "".join(f"{c:>10}" for c in cells) + f"{'|':>4}"
      + "".join(f"{c:>7}" for c in u56c))
P("  (reading B at matched expected drag; a large gap between A and B means the removal channel,")
P("   not the return correction, is what moves the sign.)")
CRB = CRALL[CRALL.reading == "B"]
P(f"\n  reading B h* (only {len(HAIRCUTS_B)} rungs, so this is a COARSE bracket, not a level):")
P(f"  {'panel':<10}{'inst':<7}{'d':>3}{'cells':>7}{'crossed <=20%':>15}{'median h*':>12}"
  f"{'min h*':>10}{'inside band':>13}")
for (pname, inst, d), sub in CRB.groupby(["panel", "inst", "d"]):
    ok = sub.hstar.notna()
    P(f"  {pname:<10}{inst:<7}{d:>3}{len(sub):>7}{int(ok.sum()):>10}/{len(sub):<4}"
      f"{(sub.hstar.median() if ok.any() else np.nan):>12.2%}"
      f"{(sub.hstar.min() if ok.any() else np.nan):>10.2%}"
      f"{int(((sub.hstar <= BAND[pname]) & ok).sum()):>9}/{len(sub):<4}")

# ---- Q7b: reading B is STOCHASTIC.  Is the flip a seed or a mechanism? ----------------
P("\n" + "-" * 118)
P(f"Q7b  SEED STABILITY of reading B — {len(SEEDS)} seeds, {PROTO_COST} bps.  Seed is a")
P("     REPLICATION axis, not a third parameter: nothing is selected on it and all seeds report.")
P("-" * 118)
SEEDROWS = []
SEED_GRID = ([("U56", h, d) for h in HAIRCUTS_B if h > 0 for d in DECILES]
             + [("SMALL439", 0.03, d) for d in DECILES])
for seed in SEEDS:
    for (pname, h, d) in SEED_GRID:
        px = PANELS[pname][0]
        st = START[pname]
        rmat, alive = event_panel(pname, h, d, seed=seed)
        notna_b = NOTNA[pname] & alive
        R = {}
        for mname in MASKS[pname]:
            mask_b = MASKS[pname][mname] & alive
            for book in BOOKS:
                g = trend(px, book)
                for conv in CONVS:
                    gr, tn, _ = fast_bt_r(px.index, rmat,
                                          weights_ewall(notna_b, mask_b, g, conv))
                    R[(mname, book, conv)] = net(gr.loc[st:], tn.loc[st:], PROTO_COST)
        insts = sorted({m.split("_")[0] for m in MASKS[pname] if m != "NONE"})
        nwin = ntot = 0
        for inst in insts:
            cands = [m for m in MASKS[pname] if m.split("_")[0] == inst]
            for book in BOOKS:
                for conv in CONVS:
                    isS = {m: metrics(R[(m, book, conv)].loc[:IS_END])["Sharpe"] for m in cands}
                    pick = max(isS, key=lambda m: isS[m])
                    e = (metrics(R[(pick, book, conv)].loc[OOS_START:])["Sharpe"]
                         - metrics(R[("NONE", book, conv)].loc[OOS_START:])["Sharpe"])
                    nwin += int(e > 0)
                    ntot += 1
        SEEDROWS.append(dict(seed=seed, panel=pname, h=h, d=d, wins=nwin, cells=ntot,
                             delisted=int((~alive.iloc[-1]).sum())))
SD = pd.DataFrame(SEEDROWS)
SD.to_csv(OUT / f"{STEM}.seeds.csv", index=False)
P(f"  cells per (seed, panel, h, d): U56 4, SMALL439 12  (inst x book x conv at {PROTO_COST} bps)")
P(f"  {'panel':<10}{'h':>6}{'d':>3}   " + "".join(f"{f'seed {s}':>9}" for s in SEEDS)
  + f"{'mean win rate':>15}{'seeds with >=1 win':>21}")
for (pname, h, d), sub in SD.groupby(["panel", "h", "d"]):
    sub = sub.set_index("seed").reindex(SEEDS)
    P(f"  {pname:<10}{h:>6.0%}{d:>3}   "
      + "".join(f"{f'{int(r.wins)}/{int(r.cells)}':>9}" for _, r in sub.iterrows())
      + f"{(sub.wins / sub.cells).mean():>15.3f}{int((sub.wins > 0).sum()):>18}/{len(SEEDS)}")
P(f"\n  Reading B seed dispersion is the honest width of its flip claim: the seed-435 row is one")
P(f"  draw of {len(SEEDS)}, and a claim that survives only some seeds is a draw, not a mechanism.")

# =====================================================================================
# Q8 — both KEEP paths at every grid point
# =====================================================================================
P("\n" + "-" * 118)
P("Q8  BOTH KEEP PATHS at 10 bps (4a vs live RULES v2 cost-matched; 4b vs SPY + rule 8)")
P("-" * 118)


def path_verdicts(pname, r_full):
    m = mrow(r_full)
    ms = spy_m[pname]
    bad_a = []
    if m["H1"] <= mv2_10["H1"]:
        bad_a.append("H1")
    if m["H2"] <= mv2_10["H2"]:
        bad_a.append("H2")
    if m["MaxDD"] < mv2_10["MaxDD"]:
        bad_a.append("DD")
    bad_b = []
    if m["H1"] <= ms["H1"]:
        bad_b.append("H1")
    if m["H2"] <= ms["H2"]:
        bad_b.append("H2")
    if metrics(r_full.loc[OOS_START:])["Sharpe"] <= spy_oos[pname]["Sharpe"]:
        bad_b.append("OOS")
    if m["MaxDD"] < 0.60 * ms["MaxDD"]:
        bad_b.append("DD")
    if m["CAGR"] < 0.70 * ms["CAGR"]:
        bad_b.append("CAGR")
    return bad_a, bad_b


vrows = []
for key, r in RET.items():
    reading, h, d, pname, mname, book, conv, bps = key
    if bps != PROTO_COST:
        continue
    ba, bb = path_verdicts(pname, r)
    m = mrow(r)
    vrows.append(dict(reading=reading, h=h, d=d, panel=pname, mask=mname,
                      inst=mname.split("_")[0], book=book, conv=conv, **m,
                      path4a="KEEP" if not ba else "KILL(" + ",".join(ba) + ")",
                      path4b="KEEP" if not bb else "KILL(" + ",".join(bb) + ")"))
V = pd.DataFrame(vrows)
V.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
for pname in PANELS:
    sp = spy_m[pname]
    P(f"  4b bars ({pname} window, SPY, NOT haircut): H1 > {sp['H1']:.3f}, H2 > {sp['H2']:.3f}, "
      f"OOS Sharpe > {spy_oos[pname]['Sharpe']:.3f}, MaxDD >= {0.60 * sp['MaxDD']:.1%}, "
      f"CAGR >= {0.70 * sp['CAGR']:.2%}")
P(f"  4a bars (RULES v2 @10bps): H1 > {mv2_10['H1']:.3f}, H2 > {mv2_10['H2']:.3f}, "
  f"MaxDD >= {mv2_10['MaxDD']:.2%}")
P(f"\n  {'reading':<9}{'h':>7}{'panel':<11}{'points':>8}{'4a KEEP':>10}{'4b KEEP':>10}"
  f"   binding bars (4b)")
for (reading, h, pname), sub in V.groupby(["reading", "h", "panel"]):
    fails = pd.Series([x for s in sub.path4b for x in
                       (s[5:-1].split(",") if s.startswith("KILL") else [])]).value_counts()
    P(f"  {reading:<9}{h:>7.0%}{pname:<11}{len(sub):>8}{int((sub.path4a == 'KEEP').sum()):>10}"
      f"{int((sub.path4b == 'KEEP').sum()):>10}   "
      f"{', '.join(f'{k} {v}' for k, v in fails.items())}")
P(f"\n  TOTAL: 4a KEEP {int((V.path4a == 'KEEP').sum())}/{len(V)};  "
  f"4b KEEP {int((V.path4b == 'KEEP').sum())}/{len(V)}")
mono4b = []
for (reading, d, pname, mname, book, conv), sub in V.groupby(
        ["reading", "d", "panel", "mask", "book", "conv"]):
    s = sub.sort_values("h")
    k = (s.path4b == "KEEP").astype(int).values
    mono4b.append(all(k[i] >= k[i + 1] for i in range(len(k) - 1)))
P(f"  P4 (4b passes weakly DECREASING in h): {int(sum(mono4b))}/{len(mono4b)} book-tracks monotone")
if (V.path4b == "KEEP").any():
    P("  4b passes at 10 bps:")
    for _, r in V[V.path4b == "KEEP"].iterrows():
        P(f"    {r.reading}/h={r.h:.0%}/d={r.d}/{r.panel}/{r['mask']}/{r.book}/{r.conv}: "
          f"{r.CAGR:.2%}/{r.Sharpe:.3f}/{r.MaxDD:.1%}  H {r.H1:.3f}/{r.H2:.3f}")

# =====================================================================================
# verdict
# =====================================================================================
P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
u56cr = CR[CR.panel == "U56"]
smlcr = CR[CR.panel == "SMALL439"]
u56_in = int((u56cr.hstar <= BAND["U56"]).sum())
sml_in = int((smlcr.hstar <= BAND["SMALL439"]).sum())
P(f"  U56      median h* {u56cr.hstar.median():.2%}  (band {BAND['U56']:.0%}) -> "
  f"{u56_in}/{len(u56cr)} cells inside the plausibility band")
P(f"  SMALL439 median h* {smlcr.hstar.median():.2%}  (band {BAND['SMALL439']:.0%}) -> "
  f"{sml_in}/{len(smlcr)} cells inside")
P(f"  428's 0/64 reproduced at h=0: {int((base.edge > 0).sum())}/{len(base)}")
sdU = SD[(SD.panel == "U56") & (SD.h == 0.03)]
sdS = SD[(SD.panel == "SMALL439") & (SD.h == 0.03)]
P(f"  reading B (EVENT) at h=3%, the only haircut inside BOTH bands: U56 win rate "
  f"{(sdU.wins / sdU.cells).mean():.3f} over {len(SEEDS)} seeds x {sdU.d.nunique()} deciles, "
  f"SMALL439 {(sdS.wins / sdS.cells).mean():.3f}")
P(f"  4a {int((V.path4a == 'KEEP').sum())}/{len(V)};  4b {int((V.path4b == 'KEEP').sum())}/{len(V)}"
  f"   -> no book promoted; PROTOCOL/RULES/scan/bot/baseline untouched.")
P(f"\n  runtime {time.time() - T0:.0f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
