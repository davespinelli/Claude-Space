#!/usr/bin/env python3
"""QUEUE idea 119 — V1u-small-negative-price (cloud, 2026-09-05).

Question (verbatim from QUEUE.md)
---------------------------------
"on V1u/small every gate prices NEGATIVE (-0.34 to -1.41): more CAGR and less drawdown,
+0.02..+0.10 Sharpe, 6/6 arms.  A free lunch that large on a 439-name panel is more likely a
panel artefact (survivorship, 32x/yr turnover, top-5 concentration) than an edge.  Audit before
anyone cites it."

WHAT IS ON TRIAL
----------------
A NUMBER, not a book.  Idea 97's price list reports, in the cell `panel=small, book=V1u`, gate
arms whose price (pp of CAGR surrendered per pp of MaxDD bought, idea 74's axis) is negative —
the gate adds CAGR AND cuts drawdown.  Nothing in this project may cite that cell until the
number has been attacked.  This run attacks it four ways and reports what survives.

HARNESS — idea 94's simulator and idea 97's panel loader, imported, nothing re-implemented
-------------------------------------------------------------------------------------------
  targets() / run() / price() / ladder_slope() / arm_specs()  from idea 94
  panel()                                                     from idea 97
  Panel: data/prices_small.csv.gz, SPY held out as benchmark, the 44 names with
  max_1d_move >= 1.0 in data/small_meta.csv dropped (the convention of every small-panel run in
  this project) -> 439 names, trading-day indexed, eval from ~2011-01, IS = ..2016-12-31.
  Book V1u: RULES v1's composite WITH /sqrt(vol20), top-5 at 15% each, ungated, 75% gross.

TUNED PARAMETERS (PROTOCOL rule 4): TWO — the gate instrument family (5 gates x 2 conventions)
and the book's position count n (5 = V1u's own, 10, 20, 40).  Cost rungs, subsample sizes,
priceability floors and calendar years are REPORTED sensitivity, never selected on.

STATISTICS, DECLARED BEFORE ANY NUMBER WAS COMPUTED
----------------------------------------------------
S0 REPRODUCTION.  Idea 97's committed .pricelist.csv rows for panel=small/book=V1u are read
   back and re-derived here (both cost rungs, all 16 arms).  Tolerance 1e-9 on dCAGR, dMaxDD,
   rate, dSharpe.  If this fails the audit stops: there is nothing to audit.

S1 PREMISE CHECK.  The queue says "every gate prices negative ... 6/6 arms".  Counted literally:
   how many of the 10 gate arms are PRICEABLE (idea 94's floor: dMaxDD > 0.10 pp) at each cost
   rung, and how many of those are negative.  Reported as it falls, including if the queue's
   own wording does not survive.

S2 THE NOISE-BAND TEST.  A price is a ratio of two differences.  On a book whose control
   drawdown is about -34%, an arm that moves MaxDD by 0.57 pp has moved it by under 2% of its
   own depth, and the ratio is then an artefact of the denominator.  Pre-registered: an arm is
   MATERIAL iff dMaxDD >= 10% of the control's |MaxDD| (about 3.4 pp here).  The price list is
   re-tabulated under priceability floors {0.10, 1.0, 2.0, 3.0} pp and the material count is
   reported at each.  Idea 94's own 0.10 pp floor is kept as the reference, not replaced.

S3 THE NAME-SUBSAMPLE BOOTSTRAP — the test with power.  A 5-name book drawn from 439 survivors
   can be a statement about five names.  NDRAW random subsamples dropping DROP_FRAC of the
   names (seeded, deterministic); the control and every audited arm are rebuilt and re-priced
   inside each subsample.  Pre-registered decision, fixed before any draw was run:
       the negative price is a PANEL ARTEFACT iff, for the arm in question, EITHER
       (a) sign(dCAGR) is not the free-lunch sign in at least 90% of draws, OR
       (b) the 25th-75th percentile range of the price spans zero.
       It SURVIVES the audit iff neither holds.
   Reported per arm; no arm is selected on the result.

S4 TIME-LOCALISATION.  Per-calendar-year arm-minus-control return, and the price recomputed
   with each single calendar year deleted (returns spliced; MaxDD is NOT taken on a spliced
   series, so the year-deletion table reports dCAGR and dSharpe only).  A free lunch that lives
   in one year is a year, not an edge.

S5 CONCENTRATION.  The same gates priced on the same panel with the same scorer at n in
   {5,10,20,40}, weight 0.75/n.  If the negative price is a property of holding 5 of 439 names
   it must fade in n.

S6 COSTS.  Every price at 0, 10, 25 and 50 bps.  The book turns over ~33x/yr; if the gate's
   CAGR gain is really a cost saving it must grow with the cost rung and vanish at 0 bps.

S7 WALK-FORWARD (PROTOCOL rule 8, mandatory).  Idea 94's selector S1 — among arms with IS
   dMaxDD >= 1.0 pp and a finite IS rate, argmin IS rate — applied to the IS window only, then
   the untouched OOS window reported: the picked book's OOS CAGR / Sharpe / MaxDD against
   RULES v1 on the same panel and against SPY, with both KEEP paths (4a, 4b) evaluated on the
   full sample and out of sample.

SURVIVORSHIP — stated because it runs AGAINST the artefact hypothesis, not for it.
  The panel is current constituents of a sub-$2B screen, so names that fell and delisted are
  absent.  That bias flatters the UNGATED book (it holds beaten-down names that all, in fact,
  survived) and therefore makes a gate that excludes them look WORSE than it would on a
  delisting-aware panel.  A free lunch measured here is if anything understated by survivorship;
  the artefact hypothesis must be carried by concentration, denominator size, one-year
  dependence or costs, and this run tests those four directly.  Absolute CAGR/Sharpe levels on
  this panel are not quotable (idea 54 remains open).

Deterministic (seeded), standalone, no network:
    python research/backtests/2026-09-05_V1u-small-negative-price_cloud.py
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import rules_v1_weights  # noqa: E402
from engine import metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location("i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)
_s97 = importlib.util.spec_from_file_location("i97", BT / "2026-09-05_price-list-tier-bar_B.py")
H97 = importlib.util.module_from_spec(_s97)
_s97.loader.exec_module(H97)

FREQ, GROSS, MAX_VOL = H.FREQ, H.GROSS, H.MAX_VOL
IS_END, OOS_START = H.IS_END, H.OOS_START
GATES = list(H.GATES)
CONVS = ("dg", "rw")
BOOK = "V1u"
NGRID = [5, 10, 20, 40]
COST_RUNGS = [0.0, 10.0, 25.0, 50.0]
PCOST = 10.0
NDRAW, DROP_FRACS, SEED = 100, (0.10, 0.25), 20260905
MATERIAL_FRAC = 0.10          # dMaxDD must be >= 10% of the control's |MaxDD| to be material
FLOORS = [0.10, 1.0, 2.0, 3.0]

pd.set_option("display.width", 230)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


# ---------------------------------------------------------------- cached signal path
def signals(px):
    return H.composite(px), H.vol20(px)


def targets_cached(px, comp, v20, n, w, gate=None, conv="dg"):
    """H.targets for a top-n/weight-w composite book with /sqrt(vol20), using precomputed
    signals.  Asserted equal to H.targets(px, 'V1u', ...) on the full panel below."""
    s = comp / v20.clip(lower=0.08) ** 0.5
    if gate is None:
        rank = s.rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * w
    g = H.gate_mask(px, gate)
    if conv == "rw":
        rank = s.where(g).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * w
    return ((s.rank(axis=1, ascending=False) <= n).astype(float) * w).where(g, 0.0)


def price_pair(rc, ra):
    """idea 94's price(), reported without the ladder-domination flag."""
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dict(dCAGR=dc, dMaxDD=dd,
                rate=(dc / dd if dd > 0.10 else np.nan),
                dSharpe=ma["Sharpe"] - mc["Sharpe"],
                ctl_MaxDD=mc["MaxDD"] * 100.0)


def main():
    px, spy_full, label = H97.panel("small")
    start = px.index[260]
    spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
    comp, v20 = signals(px)
    print(f"[data] {label} | {px.index[0].date()} -> {px.index[-1].date()} | eval from "
          f"{start.date()} | IS ..{IS_END} | OOS {OOS_START}..")
    print(f"[pre-registered] S0 reproduction · S1 premise · S2 noise band (material = dMaxDD >= "
          f"{MATERIAL_FRAC:.0%} of |control MaxDD|)")
    print(f"[pre-registered] S3 bootstrap {NDRAW} draws x drop {DROP_FRACS} (seed {SEED}); "
          f"ARTEFACT iff sign(dCAGR) held <90% of draws OR the IQR of the price spans 0")
    print("[pre-registered] S4 year deletion · S5 n in %s · S6 costs %s bps · S7 rule-8 WF\n"
          % (NGRID, [int(c) for c in COST_RUNGS]))

    # harness identity: the cached path must equal idea 94's own targets()
    for gate in [None] + GATES:
        for conv in CONVS:
            if gate is None and conv == "rw":
                continue
            a = targets_cached(px, comp, v20, H.NV1, H.WV1, gate, conv)
            b = H.targets(px, BOOK, gate, conv)
            d = float((a - b).abs().max().max())
            assert d < 1e-12, (gate, conv, d)
    print("[check] cached-signal target path reproduces idea 94's targets() exactly "
          f"(max |diff| < 1e-12 over {1 + len(GATES) * 2} arms)")

    # ============================================================ S0 reproduction
    print("\n" + "=" * 122)
    print("S0  REPRODUCTION of idea 97's committed pricelist rows for panel=small / book=V1u")
    ref = pd.read_csv(BT / "2026-09-05_price-list-tier-bar_B.pricelist.csv")
    ref = ref[(ref.panel == "small") & (ref.book == BOOK)].copy()
    specs = H.arm_specs()
    rows, rets = [], {}
    for bps in (10.0, 25.0):
        ctl = H.run(px, H.targets(px, BOOK), bps=bps)["r"].loc[start:]
        rets[("control", bps)] = ctl
        for name, kind, kw, (gate, conv) in specs:
            if name == "control":
                continue
            W = H.targets(px, BOOK, gate, conv)
            r = H.run(px, W, bps=bps, **kw)["r"].loc[start:]
            rets[(name, bps)] = r
            p = price_pair(ctl, r)
            p.update(arm=name, cost=bps, kind=kind)
            rows.append(p)
    MINE = pd.DataFrame(rows)
    m = ref.merge(MINE, on=["arm", "cost"], suffixes=("_ref", "_new"))
    errs = {c: float((m[f"{c}_ref"] - m[f"{c}_new"]).abs().max())
            for c in ("dCAGR", "dMaxDD", "dSharpe")}
    rr = m[["rate_ref", "rate_new"]].dropna()
    errs["rate"] = float((rr.rate_ref - rr.rate_new).abs().max()) if len(rr) else 0.0
    worst = max(errs.values())
    print(f"    matched {len(m)} of {len(ref)} committed rows; max |diff| = {worst:.2e} "
          + "  ".join(f"{k}:{v:.1e}" for k, v in errs.items()))
    assert worst < 1e-9 and len(m) == len(ref), "reproduction failed — nothing to audit"
    print("    REPRODUCTION: EXACT")

    # ============================================================ S1 premise
    print("\n" + "=" * 122)
    print("S1  PREMISE CHECK — the queue's wording, counted literally")
    gate_arms = [f"{g}-{c}" for g in GATES for c in CONVS]
    GA = MINE[MINE.arm.isin(gate_arms)].copy()
    print(fmt(GA.set_index(["cost", "arm"])[["dCAGR", "dMaxDD", "rate", "dSharpe", "ctl_MaxDD"]]))
    for bps in (10.0, 25.0):
        s = GA[GA.cost == bps]
        pr = s[s.rate.notna()]
        neg = pr[pr.rate < 0]
        print(f"  @{bps:.0f} bps: {len(pr)} of {len(s)} gate arms priceable (dMaxDD > 0.10 pp); "
              f"{len(neg)} of those price NEGATIVE "
              f"(range {neg.rate.min():+.3f}..{neg.rate.max():+.3f}); "
              f"dSharpe over the negative arms {neg.dSharpe.min():+.3f}..{neg.dSharpe.max():+.3f}")
    allneg = GA[GA.rate.notna() & (GA.rate < 0)]
    allpr = GA[GA.rate.notna()]
    lit = ("SUPPORTED" if len(allneg) == len(allpr) else
           f"NOT LITERAL — {len(allpr) - len(allneg)} priceable gate arm(s) price POSITIVE")
    print(f"  Pooled over both rungs: {len(allneg)} negative of {len(allpr)} priceable of "
          f"{len(GA)} gate arms. Queue wording '6/6 arms': {lit}")
    AUDITED = sorted(allneg.arm.unique())
    print(f"  Arms carried into the audit (negative at either rung): {AUDITED}")

    # ============================================================ S2 noise band
    print("\n" + "=" * 122)
    print("S2  NOISE BAND — a price is a ratio; how big is the denominator it is divided by?")
    ctl_dd = abs(MINE.ctl_MaxDD.iloc[0])
    bar = MATERIAL_FRAC * ctl_dd
    GA["dMaxDD_pct_of_ctl"] = GA.dMaxDD / ctl_dd
    GA["material"] = GA.dMaxDD >= bar
    print(f"    control |MaxDD| = {ctl_dd:.2f} pp; material bar = {bar:.2f} pp of drawdown bought")
    print(fmt(GA.set_index(["cost", "arm"])[["dCAGR", "dMaxDD", "dMaxDD_pct_of_ctl", "rate",
                                             "material"]]))
    print("\n    price list under rising priceability floors (arms surviving / negative):")
    for fl in FLOORS:
        s = GA[GA.dMaxDD >= fl]
        print(f"      floor {fl:>4.2f} pp: {len(s):2d} gate rows survive, "
              f"{int((s.dCAGR < 0).sum())} of them free-lunch-signed")
    print(f"\n    MATERIAL negative-priced gate rows: {int((GA.material & (GA.rate < 0)).sum())} "
          f"of {int((GA.rate < 0).sum())}")

    # ============================================================ S3 bootstrap
    print("\n" + "=" * 122)
    print(f"S3  NAME-SUBSAMPLE BOOTSTRAP — {NDRAW} seeded draws per drop fraction")
    names = [c for c in px.columns]
    rng = np.random.default_rng(SEED)
    boot = []
    for frac in DROP_FRACS:
        k = int(round(len(names) * (1 - frac)))
        for d in range(NDRAW):
            keep = sorted(rng.choice(len(names), size=k, replace=False))
            sub = px.iloc[:, keep]
            c2, v2 = signals(sub)
            ctl = H.run(sub, targets_cached(sub, c2, v2, H.NV1, H.WV1), bps=PCOST)["r"].loc[start:]
            for arm in AUDITED:
                g, conv = arm.rsplit("-", 1)
                r = H.run(sub, targets_cached(sub, c2, v2, H.NV1, H.WV1, g, conv),
                          bps=PCOST)["r"].loc[start:]
                p = price_pair(ctl, r)
                p.update(arm=arm, draw=d, drop_frac=frac)
                boot.append(p)
    B = pd.DataFrame(boot)
    B.to_csv(Path(__file__).with_suffix(".bootstrap.csv"), index=False)
    print(f"    {len(B)} subsample prices -> {Path(__file__).stem}.bootstrap.csv\n")
    dec = []
    for frac in DROP_FRACS:
        for arm in AUDITED:
            s = B[(B["drop_frac"] == frac) & (B.arm == arm)]
            full = GA[(GA.arm == arm) & (GA.cost == PCOST)]
            fr = float(full.rate.iloc[0]) if len(full) and np.isfinite(full.rate.iloc[0]) else np.nan
            free = float((s.dCAGR < 0).mean())          # dCAGR < 0 == the arm ADDS CAGR
            q1, q3 = s.rate.quantile(0.25), s.rate.quantile(0.75)
            iqr_spans_0 = bool(q1 < 0 < q3) or not (np.isfinite(q1) and np.isfinite(q3))
            artefact = (free < 0.90) or iqr_spans_0
            dec.append(dict(drop_frac=frac, arm=arm, full_rate=fr,
                            frac_freelunch_sign=free,
                            frac_priceable=float(s.rate.notna().mean()),
                            dCAGR_med=float(s.dCAGR.median()),
                            dMaxDD_med=float(s.dMaxDD.median()),
                            rate_q25=float(q1), rate_med=float(s.rate.median()),
                            rate_q75=float(q3),
                            frac_rate_neg=float((s.rate < 0).mean()),
                            IQR_spans_0=iqr_spans_0, ARTEFACT=artefact))
    DEC = pd.DataFrame(dec)
    print(fmt(DEC.set_index(["drop_frac", "arm"])))
    print(f"\n    Pre-registered verdict: ARTEFACT in {int(DEC.ARTEFACT.sum())} of {len(DEC)} "
          f"(arm x drop-fraction) audits; SURVIVES in {int((~DEC.ARTEFACT).sum())}")

    # ============================================================ S4 time localisation
    print("\n" + "=" * 122)
    print("S4  TIME-LOCALISATION — arm minus control by calendar year, and year-deleted prices")
    ctl10 = rets[("control", PCOST)]
    yrs = sorted({d.year for d in ctl10.index})
    peryear, yrdel = [], []
    for arm in AUDITED:
        r = rets[(arm, PCOST)]
        row = {"arm": arm}
        for y in yrs:
            a = r.loc[f"{y}-01-01":f"{y}-12-31"]
            c = ctl10.loc[f"{y}-01-01":f"{y}-12-31"]
            row[str(y)] = float((1 + a).prod() - (1 + c).prod()) * 100.0
        peryear.append(row)
        for y in yrs:
            aa, cc = r[r.index.year != y], ctl10[ctl10.index.year != y]
            n = len(aa) / 252.0
            dc = ((1 + cc).prod() ** (1 / n) - 1) - ((1 + aa).prod() ** (1 / n) - 1)
            yrdel.append(dict(arm=arm, year_deleted=y, dCAGR_pp=dc * 100.0,
                              dSharpe=float(aa.mean() / aa.std() * np.sqrt(252)
                                            - cc.mean() / cc.std() * np.sqrt(252))))
    PY = pd.DataFrame(peryear).set_index("arm")
    print("    arm-minus-control TOTAL RETURN by year, pp (10 bps):")
    print(fmt(PY))
    YD = pd.DataFrame(yrdel).pivot(index="arm", columns="year_deleted", values="dCAGR_pp")
    print("\n    dCAGR (pp, control minus arm; negative = arm still adds CAGR) with each year deleted:")
    print(fmt(YD))
    print(f"\n    sign flips under single-year deletion: "
          + ", ".join(f"{a} {int((YD.loc[a] > 0).sum())}/{YD.shape[1]}" for a in YD.index))

    # ============================================================ S5 concentration
    print("\n" + "=" * 122)
    print("S5  CONCENTRATION — the same gates on the same panel at n in %s" % NGRID)
    conc = []
    for n in NGRID:
        w = H.WV1 if n == H.NV1 else GROSS / n
        ctl = H.run(px, targets_cached(px, comp, v20, n, w), bps=PCOST)["r"].loc[start:]
        mc = metrics(ctl)
        for arm in [f"{g}-{c}" for g in GATES for c in CONVS]:
            g, conv = arm.rsplit("-", 1)
            r = H.run(px, targets_cached(px, comp, v20, n, w, g, conv), bps=PCOST)["r"].loc[start:]
            p = price_pair(ctl, r)
            p.update(n=n, arm=arm, ctl_CAGR=mc["CAGR"] * 100.0, ctl_Sharpe=mc["Sharpe"])
            conc.append(p)
    C = pd.DataFrame(conc)
    print(fmt(C.pivot(index="arm", columns="n", values="rate")))
    print("\n    dCAGR (pp, control minus arm) by n:")
    print(fmt(C.pivot(index="arm", columns="n", values="dCAGR")))
    print("\n    dMaxDD (pp bought) by n:")
    print(fmt(C.pivot(index="arm", columns="n", values="dMaxDD")))
    print("\n    control book by n: " + ", ".join(
        f"n={n} CAGR {C[C.n == n].ctl_CAGR.iloc[0]:.2f}% Sharpe {C[C.n == n].ctl_Sharpe.iloc[0]:.3f}"
        for n in NGRID))
    fl_by_n = {n: int((C[(C.n == n) & C.rate.notna()].rate < 0).sum()) for n in NGRID}
    pr_by_n = {n: int(C[(C.n == n)].rate.notna().sum()) for n in NGRID}
    print(f"    negative-priced gate arms: " +
          ", ".join(f"n={n} {fl_by_n[n]}/{pr_by_n[n]} priceable" for n in NGRID))

    # ============================================================ S6 costs
    print("\n" + "=" * 122)
    print("S6  COSTS — every audited arm at 0 / 10 / 25 / 50 bps")
    cost_rows = []
    for bps in COST_RUNGS:
        ctl = H.run(px, H.targets(px, BOOK), bps=bps)["r"].loc[start:]
        for arm in AUDITED:
            g, conv = arm.rsplit("-", 1)
            r = H.run(px, H.targets(px, BOOK, g, conv), bps=bps)["r"].loc[start:]
            p = price_pair(ctl, r)
            p.update(cost=bps, arm=arm)
            cost_rows.append(p)
    CO = pd.DataFrame(cost_rows)
    print(fmt(CO.pivot(index="arm", columns="cost", values="dCAGR")))
    print("\n    price by cost rung:")
    print(fmt(CO.pivot(index="arm", columns="cost", values="rate")))
    to_ctl = H.run(px, H.targets(px, BOOK), bps=PCOST)
    print(f"\n    control turnover {float(to_ctl['to'].loc[start:].sum() / (len(ctl10) / 252)):.1f}x/yr; "
          + ", ".join(
              f"{a} {float(H.run(px, H.targets(px, BOOK, *a.rsplit('-', 1)), bps=PCOST)['to'].loc[start:].sum() / (len(ctl10) / 252)):.1f}x"
              for a in AUDITED))

    # ============================================================ S7 walk-forward
    print("\n" + "=" * 122)
    print("S7  RULE-8 WALK-FORWARD — idea 94's selector S1 on the IS window only")
    v1 = {}
    for bps in (10.0, 25.0):
        v1[bps] = H.run(px, rules_v1_weights(px), bps=bps)["r"].loc[start:]
    wf = []
    for bps in (10.0, 25.0):
        ctl = rets[("control", bps)]
        cand = []
        for name, kind, kw, (gate, conv) in specs:
            if name == "control":
                continue
            r = rets[(name, bps)]
            pis = price_pair(ctl.loc[:IS_END], r.loc[:IS_END])
            if pis["dMaxDD"] >= 1.0 and np.isfinite(pis["rate"]):
                cand.append((pis["rate"], name, r))
        if not cand:
            print(f"  @{bps:.0f} bps: selector picks NOTHING — no arm bought >= 1.0 pp of IS drawdown")
            continue
        cand.sort(key=lambda z: (z[0], z[1]))
        rate_is, pick, r = cand[0]
        po = price_pair(ctl.loc[OOS_START:], r.loc[OOS_START:])
        best_oos = min((price_pair(ctl.loc[OOS_START:], rets[(nm, bps)].loc[OOS_START:])["rate"]
                        for nm, *_ in [(s[0],) for s in specs] if nm != "control"
                        and np.isfinite(price_pair(ctl.loc[OOS_START:],
                                                   rets[(nm, bps)].loc[OOS_START:])["rate"])),
                       default=np.nan)
        mo, mf = metrics(r.loc[OOS_START:]), metrics(r)
        so, sf = metrics(spy.loc[OOS_START:]), metrics(spy)
        vo, vf = metrics(v1[bps].loc[OOS_START:]), metrics(v1[bps])
        h1, h2 = H.halves(r)
        s1, s2 = H.halves(spy)
        b1, b2 = H.halves(v1[bps])
        wf.append(dict(cost=bps, pick=pick, IS_rate=rate_is, OOS_rate=po["rate"],
                       regret=po["rate"] - best_oos if np.isfinite(best_oos) else np.nan,
                       CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       v1_OOS_Sharpe=vo["Sharpe"], v1_OOS_CAGR=vo["CAGR"], v1_OOS_MaxDD=vo["MaxDD"],
                       spy_OOS_Sharpe=so["Sharpe"], spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"],
                       p4a=bool(h1 > b1 and h2 > b2 and mf["MaxDD"] >= vf["MaxDD"]),
                       p4b=bool(h1 > s1 and h2 > s2 and mo["Sharpe"] > so["Sharpe"]
                                and mf["MaxDD"] >= 0.60 * sf["MaxDD"]
                                and mf["CAGR"] >= 0.70 * sf["CAGR"]),
                       p4b_oos=bool(mo["Sharpe"] > so["Sharpe"]
                                    and mo["MaxDD"] >= 0.60 * so["MaxDD"]
                                    and mo["CAGR"] >= 0.70 * so["CAGR"])))
    W = pd.DataFrame(wf)
    W.to_csv(Path(__file__).with_suffix(".walkforward.csv"), index=False)
    print(fmt(W))
    if len(W):
        print(f"\n    OOS references (small panel, same days): RULES v1 "
              f"{W.v1_OOS_CAGR.iloc[0]:.1%}/{W.v1_OOS_Sharpe.iloc[0]:.3f}/{W.v1_OOS_MaxDD.iloc[0]:.1%}"
              f"  |  SPY {W.spy_OOS_CAGR.iloc[0]:.1%}/{W.spy_OOS_Sharpe.iloc[0]:.3f}/"
              f"{W.spy_OOS_MaxDD.iloc[0]:.1%}")
        print(f"    KEEP paths over the walk-forward picks: 4a {int(W.p4a.sum())}/{len(W)}, "
              f"4b {int(W.p4b.sum())}/{len(W)}, 4b-OOS {int(W.p4b_oos.sum())}/{len(W)}")

    # full-sample KEEP footprint over every audited book (both paths, both rungs)
    kp = []
    for bps in (10.0, 25.0):
        for nm in ["control"] + AUDITED:
            r = rets[(nm, bps)]
            mf, sf, vf = metrics(r), metrics(spy), metrics(v1[bps])
            mo, so = metrics(r.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
            h1, h2 = H.halves(r)
            s1, s2 = H.halves(spy)
            b1, b2 = H.halves(v1[bps])
            kp.append(dict(cost=bps, arm=nm, CAGR=mf["CAGR"], Sharpe=mf["Sharpe"],
                           MaxDD=mf["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=mo["Sharpe"],
                           p4a=bool(h1 > b1 and h2 > b2 and mf["MaxDD"] >= vf["MaxDD"]),
                           p4b=bool(h1 > s1 and h2 > s2 and mo["Sharpe"] > so["Sharpe"]
                                    and mf["MaxDD"] >= 0.60 * sf["MaxDD"]
                                    and mf["CAGR"] >= 0.70 * sf["CAGR"])))
    KP = pd.DataFrame(kp)
    print("\n    Both KEEP paths on every audited book (the books themselves, not the prices):")
    print(fmt(KP.set_index(["cost", "arm"])))
    print(f"    4a passes {int(KP.p4a.sum())}/{len(KP)}; 4b passes {int(KP.p4b.sum())}/{len(KP)}; "
          f"SPY {metrics(spy)['CAGR']:.1%}/{metrics(spy)['Sharpe']:.3f}/{metrics(spy)['MaxDD']:.1%}")

    MINE.to_csv(Path(__file__).with_suffix(".pricelist.csv"), index=False)
    C.to_csv(Path(__file__).with_suffix(".concentration.csv"), index=False)
    CO.to_csv(Path(__file__).with_suffix(".costs.csv"), index=False)
    DEC.to_csv(Path(__file__).with_suffix(".bootdecision.csv"), index=False)

    print("\n" + "=" * 122)
    print("HEADLINE")
    print(f"  premise: {len(allneg)}/{len(allpr)} priceable gate arms price negative "
          f"({len(GA)} gate rows in total)")
    print(f"  material (dMaxDD >= {bar:.2f} pp): "
          f"{int((GA.material & (GA.rate < 0)).sum())} of {int((GA.rate < 0).sum())} negative rows")
    print(f"  bootstrap: ARTEFACT in {int(DEC.ARTEFACT.sum())} of {len(DEC)} audits")
    print(f"  concentration: negative-priced arms " +
          ", ".join(f"n={n}: {fl_by_n[n]}" for n in NGRID))
    print(f"\n[outputs] {Path(__file__).stem}"
          ".pricelist.csv .bootstrap.csv .bootdecision.csv .concentration.csv .costs.csv "
          ".walkforward.csv")


if __name__ == "__main__":
    main()
