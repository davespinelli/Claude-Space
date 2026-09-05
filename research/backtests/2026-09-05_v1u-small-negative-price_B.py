#!/usr/bin/env python3
"""QUEUE idea 119 — V1u-small-negative-price (lane B, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"on V1u/small every gate prices NEGATIVE (-0.34 to -1.41): more CAGR and less drawdown,
+0.02..+0.10 Sharpe, 6/6 arms.  A free lunch that large on a 439-name panel is more likely a
panel artefact (survivorship, 32x/yr turnover, top-5 concentration) than an edge.  Audit
before anyone cites it."

This is an AUDIT, not a search for a book.  The thing on trial is a NUMBER already in the
project's record (idea 97's `V1u/small` price column) and the three artefact hypotheses the
queue names for it.  A negative insurance price means the instrument is not insurance at all
but free alpha: hold LESS and earn MORE with a SMALLER drawdown.  Claims of that shape are
where a research programme goes wrong, so the bar here is not "can I reproduce it" (idea 97's
harness is imported unchanged and reproduces it exactly, first thing) but "does the sign
survive every axis on which an artefact would move it".

The audited object.  `V1u` = idea 94's ungated live-rules book: composite (mean pct-rank of
12-1, 6m, 3m) / sqrt(vol20 clipped at 0.08), top NV1=5 names at WV1=15% each (75% gross),
weekly, long-only, next-day execution, 10 bps.  `small` = data/prices_small.csv.gz, 439 names
after dropping the 44 with max_1d_move >= 1.0, SPY held out as benchmark.  A gate arm is that
book with a per-name eligibility mask in one of two conventions: `-dg` zeroes gated-out names
into cash (gross falls), `-rw` rebuilds the top-5 among gated-in names only (gross constant).
Price = (CAGR_control - CAGR_arm) / (|MaxDD_control| - |MaxDD_arm|), both in pp, on matched
days; undefined when the arm buys < 0.10 pp of drawdown (idea 94's convention).

Tuned parameters (PROTOCOL rule 4): TWO, both on the audit axis, both reported at every grid
point and neither chosen — the book's position count n in {5,10,20,40} and the inverse-vol
scaler in {on,off}.  Everything else (gates, band width, vol threshold, gross, cadence, the
IS/OOS split) is inherited from ideas 94/97 and never re-opened.

Tests (each is a way the sign could be an artefact; all are reported whatever they say)
    A  REPRODUCTION.  idea 97's numbers, from idea 94's imported simulator.
    B  COST/TURNOVER (queue hypothesis 2).  The control turns over ~33x/yr; every gate cuts
       turnover, so at 10 bps part of any CAGR gain is simply cost avoided, not names avoided.
       Price the same 10 arms at 0, 5, 10, 25 and 50 bps.  At 0 bps the cost channel is shut:
       if dCAGR loses its sign there, the free lunch is a commission rebate.
    C  CONCENTRATION / SCALER (queue hypothesis 3).  n in {5,10,20,40} x scaler {on,off},
       8 books x {control, g200-dg, g200-rw, v1gate-rw}.  idea 97's TOP20 (n=20, no scaler)
       prices POSITIVE on the same panel, so the sign flip lives on one of these two axes or
       on neither; this separates them.
    D  NAME SAMPLING.  80 random sub-panels of 220 of the 439 names (seeded), composite, gates
       and ranks all recomputed inside each sub-panel.  Fraction with dCAGR < 0, dMaxDD > 0,
       and rate < 0.  A result that holds only on the full name list is a draw, not an edge.
    E  EPISODE / YEAR STRUCTURE.  (E1) annual dCAGR; leave-one-year-out on the full-sample
       price.  (E2) every >10% drawdown episode of the control (idea 62's classification):
       in how many is the arm shallower?  dMaxDD is ~1 pp on a -34% control drawdown, i.e.
       3% of one order statistic on one path — if it comes from a single episode the
       denominator of the price is noise and the ratio is undefined in substance.
    F  CAPACITY.  data/volume_small.csv.gz dollar ADV of the names actually held, and the
       traded fraction of ADV implied by 33x/yr turnover at $1M / $10M / $100M of capital.
       A price that cannot be paid at any size is not a price.
    G  PORTABILITY.  The same V1u book and the same 10 arms on u56 and broad.
    H  PROTOCOL rules 3, 4, 8.  Every arm vs live RULES v1 on the same panel and vs SPY;
       4a and 4b for every arm; walk-forward with the family chosen on 2010-2016 only and
       2017-2026 untouched, under two selectors fixed before any OOS number was read.

Pre-registered predictions (written after test A only — A is a reproduction of a published
number — and before any number of tests B-H was read)
    P1  The sign is cost-dependent: at 0 bps the median gate dCAGR on V1u/small is >= 0
        (i.e. the gate costs CAGR gross of costs) and the negative price is a turnover story.
    P2  The sign is concentration-dependent: negative prices concentrate at n=5 and vanish by
        n=20, reproducing idea 97's positive TOP20 price on the same panel.
    P3  Name sampling: fewer than 70% of the 80 sub-panels reproduce rate < 0.
    P4  dMaxDD is a one-episode artefact: the arm is shallower in <= 60% of the control's
        >10% drawdown episodes despite a positive whole-window dMaxDD.
    P5  No arm passes 4b on the small panel (idea 97 found 0/34; nothing here should change
        it), and the walk-forward pick's OOS Sharpe stays below SPY's.
    P6  Capacity: at $10M the book trades > 10% of the median held name's dollar ADV.

SURVIVORSHIP (queue hypothesis 1, and the one that cannot be tested from inside the panel).
The panel is the CURRENT constituent list of a sub-$2B screen: every name survived to 2026 by
construction, so the 2010-2025 small caps that were delisted, bankrupted or acquired are
absent.  Note the DIRECTION carefully, because it is the opposite of the queue's presumption:
the missing names are the beaten-down ones, i.e. exactly the cohort a 200d/vol gate EXCLUDES.
Their absence flatters the UNGATED control (it never holds the names that went to zero) and
therefore UNDERSTATES the gate's advantage.  Survivorship cannot manufacture a negative gate
price on this panel; it can only shrink one.  What it can do is inflate the LEVEL of every
number here, which is why nothing in this run is quoted as an achievable return.  Test D is
the closest available proxy for composition risk and is reported as such, not as a fix.

Deterministic (seeded), standalone.  Imports research/baseline.py and ideas 94/97's modules;
modifies nothing.  Writes .console.txt and six .csv companions next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_v1u-small-negative-price_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, MAX_VOL = H.FREQ, H.GROSS, H.MAX_VOL
IS_END, OOS_START = H.IS_END, H.OOS_START
GATES = H.GATES
ARMS = [f"{g}-{c}" for g in GATES for c in ("dg", "rw")]
COSTS_B = [0.0, 5.0, 10.0, 25.0, 50.0]
NS = [5, 10, 20, 40]
SCALERS = [True, False]
N_DRAW, DRAW_SIZE, SEED = 80, 220, 119
LADDER = np.round(np.arange(0.10, 1.001, 0.10), 2)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
F3 = lambda x: f"{x:.3f}"  # noqa: E731


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in px.columns if c != "SPY" and c not in bad]
    spy = px["SPY"].pct_change().fillna(0.0)
    return px[inv], spy


def panel(name):
    if name == "small":
        return small_panel()
    px = load_universe(broad=(name == "broad"))
    return px, px["SPY"].pct_change().fillna(0.0)


# ---------------------------------------------------------------- parameterised V1 book
def v1_targets(px, n=5, scaler=True, gate=None, conv="dg"):
    """H.targets's V1u branch with n and the inverse-vol scaler exposed.  Gross is held at
    GROSS for every n (weight GROSS/n), so the n axis is concentration only, not exposure.
    Asserted identical to H.targets(px,'V1u',...) at n=5, scaler=True."""
    s = H.composite(px)
    if scaler:
        s = s / H.vol20(px).clip(lower=0.08) ** 0.5
    w = GROSS / n
    if gate is None:
        return (s.rank(axis=1, ascending=False) <= n).astype(float) * w
    g = H.gate_mask(px, gate)
    if conv == "rw":
        return (s.where(g).rank(axis=1, ascending=False) <= n).astype(float) * w
    return ((s.rank(axis=1, ascending=False) <= n).astype(float) * w).where(g, 0.0)


def px_price(rc, ra):
    """idea 94's price(), without the ladder-dominance flag."""
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dict(dCAGR=dc, dMaxDD=dd, rate=(dc / dd if dd > 0.10 else np.nan),
                dSharpe=ma["Sharpe"] - mc["Sharpe"], CAGR=ma["CAGR"], Sharpe=ma["Sharpe"],
                MaxDD=ma["MaxDD"])


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"],
                soos_cagr=metrics(spy.loc[OOS_START:])["CAGR"],
                soos_dd=metrics(spy.loc[OOS_START:])["MaxDD"])


def margins(r, bars):
    h1, h2 = halves(r)
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=0.60 * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - 0.70 * bars["scagr"])


def flags(r, bars, v1_net):
    mg = margins(r, bars)
    return dict(m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                p4b=all(v > 0 for v in mg.values()),
                f4b=",".join(k for k, v in mg.items() if not v > 0) or "-",
                p4a=H.pass4a(r, v1_net))


# ================================================================ A. reproduction
def test_A(P, start):
    print("=" * 190)
    print("A. REPRODUCTION — idea 94's simulator, idea 97's V1u/small price column")
    u56 = load_universe()
    s56 = u56.index[260]
    worst = max(float((H.run(u56, H.targets(u56, b), bps=10.0)["r"].loc[s56:]
                       - backtest(u56, H.targets(u56, b), cost_bps=10.0, freq=FREQ)["returns"].loc[s56:]
                       ).abs().max()) for b in H.BOOKS)
    m1 = metrics(H.run(u56, H.targets(u56, "EWall", "vol60", "dg"), bps=10.0)["r"].loc[s56:])
    print(f"  engine-equivalence (u56, 3 books @10bps): max|diff| {worst:.3e} "
          f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — UNSAFE'})")
    print(f"  idea 94 EWall+vol60-dg u56: Sharpe {m1['Sharpe']:.3f} (pub 1.133)  "
          f"CAGR {m1['CAGR']:.1%} (pub 11.6%)  MaxDD {m1['MaxDD']:.1%} (pub -16.9%)")

    # parameterisation check: v1_targets must BE H.targets at n=5, scaler on
    d = 0.0
    for g, c in [(None, "dg")] + [(g, c) for g in GATES for c in ("dg", "rw")]:
        A = v1_targets(P, 5, True, g, c)
        B = H.targets(P, "V1u", g, c)
        d = max(d, float((A - B).abs().max().max()))
    print(f"  v1_targets(n=5,scaler=on) vs H.targets('V1u'): max|diff| over 11 specs {d:.3e} "
          f"({'IDENTICAL' if d < 1e-12 else 'DIVERGENT — UNSAFE'})")

    rc = H.run(P, H.targets(P, "V1u"), bps=10.0)
    r0 = rc["r"].loc[start:]
    m0 = metrics(r0)
    to0 = rc["to"].loc[start:].sum() / m0["Years"]
    print(f"\n  V1u/small control @10bps: CAGR {m0['CAGR']:.2%}  Sharpe {m0['Sharpe']:.3f}  "
          f"MaxDD {m0['MaxDD']:.2%}  turnover {to0:.1f}x/yr  (idea 97: 32x/yr)")
    rows = []
    for a in ARMS:
        g, c = a.rsplit("-", 1)
        ra = H.run(P, H.targets(P, "V1u", g, c), bps=10.0)["r"].loc[start:]
        rows.append(dict(arm=a, **px_price(r0, ra)))
    R = pd.DataFrame(rows)
    print(R.to_string(index=False, float_format=F3))
    fin = R.dropna(subset=["rate"])
    print(f"  priceable arms {len(fin)}/10; negative {int((fin.rate < 0).sum())}; "
          f"range [{fin.rate.min():.3f}, {fin.rate.max():.3f}]  (idea 97 quoted -0.34..-1.41)")
    print(f"  dSharpe on the negative-rate arms: "
          f"{fin.loc[fin.rate < 0, 'dSharpe'].min():+.3f}..{fin.loc[fin.rate < 0, 'dSharpe'].max():+.3f} "
          f"(idea 97 quoted +0.02..+0.10)")
    return r0, R


# ================================================================ B. cost / turnover
def test_B(P, start):
    print("\n" + "=" * 190)
    print("B. COST AXIS — is the free lunch a commission rebate?  price at 0/5/10/25/50 bps, "
          "all 10 arms, ALL points reported")
    rows = []
    for c in COSTS_B:
        rc = H.run(P, H.targets(P, "V1u"), bps=c)
        r0 = rc["r"].loc[start:]
        m0 = metrics(r0)
        to0 = rc["to"].loc[start:].sum() / m0["Years"]
        rows.append(dict(cost=c, arm="control", TO=to0, dCAGR=0.0, dMaxDD=0.0, rate=np.nan,
                         dSharpe=0.0, CAGR=m0["CAGR"], Sharpe=m0["Sharpe"], MaxDD=m0["MaxDD"]))
        for a in ARMS:
            g, cv = a.rsplit("-", 1)
            res = H.run(P, H.targets(P, "V1u", g, cv), bps=c)
            ra = res["r"].loc[start:]
            to = res["to"].loc[start:].sum() / metrics(ra)["Years"]
            rows.append(dict(cost=c, arm=a, TO=to, **px_price(r0, ra)))
    B = pd.DataFrame(rows)
    print(B.to_string(index=False, float_format=F3))
    print("\n  summary by cost (gate arms only):")
    for c in COSTS_B:
        s = B[(B.cost == c) & (B.arm != "control")]
        f = s.dropna(subset=["rate"])
        ctl = B[(B.cost == c) & (B.arm == "control")].iloc[0]
        print(f"   {c:>5.1f} bps | control CAGR {ctl.CAGR:6.2%} TO {ctl.TO:5.1f}x | "
              f"median gate dCAGR {s.dCAGR.median():+6.3f} pp  (dCAGR<0 in {int((s.dCAGR < 0).sum())}/10)  "
              f"median dMaxDD {s.dMaxDD.median():+6.3f} pp  (dMaxDD>0 in {int((s.dMaxDD > 0).sum())}/10) | "
              f"priceable {len(f)}  negative {int((f.rate < 0).sum())}  "
              f"median TO {s.TO.median():5.1f}x")
    return B


# ================================================================ C. concentration / scaler
def test_C(P, start, bars, v1_net):
    print("\n" + "=" * 190)
    print("C. CONCENTRATION x SCALER — n in {5,10,20,40} x inverse-vol scaler {on,off}, "
          "gross fixed at 0.75.  4 arms each, 10 bps.  ALL 32 points reported")
    sub = ["g200-dg", "g200-rw", "v1gate-rw"]
    rows = []
    for sc in SCALERS:
        for n in NS:
            res = H.run(P, v1_targets(P, n, sc), bps=10.0)
            r0 = res["r"].loc[start:]
            m0 = metrics(r0)
            rows.append(dict(scaler=sc, n=n, arm="control", CAGR=m0["CAGR"], Sharpe=m0["Sharpe"],
                             MaxDD=m0["MaxDD"], dCAGR=0.0, dMaxDD=0.0, rate=np.nan, dSharpe=0.0,
                             TO=res["to"].loc[start:].sum() / m0["Years"],
                             **flags(r0, bars, v1_net)))
            for a in sub:
                g, cv = a.rsplit("-", 1)
                rs = H.run(P, v1_targets(P, n, sc, g, cv), bps=10.0)
                ra = rs["r"].loc[start:]
                rows.append(dict(scaler=sc, n=n, arm=a, **px_price(r0, ra),
                                 TO=rs["to"].loc[start:].sum() / metrics(ra)["Years"],
                                 **flags(ra, bars, v1_net)))
    C = pd.DataFrame(rows)
    print(C[["scaler", "n", "arm", "CAGR", "Sharpe", "MaxDD", "dCAGR", "dMaxDD", "rate",
             "dSharpe", "TO", "p4a", "p4b", "f4b"]].to_string(index=False, float_format=F3))
    print("\n  negative-rate count by cell (of 3 gate arms; '.' = unpriceable):")
    for sc in SCALERS:
        line = []
        for n in NS:
            s = C[(C.scaler == sc) & (C.n == n) & (C.arm != "control")]
            f = s.dropna(subset=["rate"])
            line.append(f"n={n}: neg {int((f.rate < 0).sum())}/{len(f)} priceable "
                        f"(medCAGRd {s.dCAGR.median():+.2f})")
        print(f"   scaler={'on ' if sc else 'off'} | " + " | ".join(line))
    return C


# ================================================================ D. name sampling
def test_D(P, start):
    print("\n" + "=" * 190)
    print(f"D. NAME SAMPLING — {N_DRAW} seeded sub-panels of {DRAW_SIZE} of {P.shape[1]} names; "
          "composite, gates and ranks recomputed inside each draw.  Arm = g200-rw (idea 97's "
          "most negative), 10 bps")
    rng = np.random.default_rng(SEED)
    cols = np.array(P.columns)
    rows = []
    for i in range(N_DRAW):
        pick = rng.choice(len(cols), DRAW_SIZE, replace=False)
        Q = P[list(cols[np.sort(pick)])]
        r0 = H.run(Q, H.targets(Q, "V1u"), bps=10.0)["r"].loc[start:]
        ra = H.run(Q, H.targets(Q, "V1u", "g200", "rw"), bps=10.0)["r"].loc[start:]
        rows.append(dict(draw=i, **px_price(r0, ra), ctl_CAGR=metrics(r0)["CAGR"],
                         ctl_MaxDD=metrics(r0)["MaxDD"]))
    D = pd.DataFrame(rows)
    fin = D.dropna(subset=["rate"])
    print(f"  dCAGR   < 0 (gate ADDS return)   : {int((D.dCAGR < 0).sum())}/{N_DRAW}   "
          f"median {D.dCAGR.median():+.3f} pp   [{D.dCAGR.min():+.2f}, {D.dCAGR.max():+.2f}]")
    print(f"  dMaxDD  > 0 (gate CUTS drawdown) : {int((D.dMaxDD > 0).sum())}/{N_DRAW}   "
          f"median {D.dMaxDD.median():+.3f} pp   [{D.dMaxDD.min():+.2f}, {D.dMaxDD.max():+.2f}]")
    print(f"  rate    < 0 (the free lunch)     : {int((fin.rate < 0).sum())}/{len(fin)} priceable "
          f"({N_DRAW - len(fin)} unpriceable: |dMaxDD| <= 0.10 pp)")
    print(f"  dSharpe > 0                      : {int((D.dSharpe > 0).sum())}/{N_DRAW}   "
          f"median {D.dSharpe.median():+.3f}   [{D.dSharpe.min():+.3f}, {D.dSharpe.max():+.3f}]")
    print(f"  BOTH dCAGR<0 AND dMaxDD>0        : "
          f"{int(((D.dCAGR < 0) & (D.dMaxDD > 0)).sum())}/{N_DRAW}")
    print(f"  control CAGR across draws: median {D.ctl_CAGR.median():.2%} "
          f"[{D.ctl_CAGR.min():.2%}, {D.ctl_CAGR.max():.2%}]  "
          f"MaxDD median {D.ctl_MaxDD.median():.2%}")
    return D


# ================================================================ E. episodes / years
def episodes(r, thresh=0.10):
    """idea 62's classification: contiguous stretches where the equity curve is >10% below a
    running high, from the peak date to full recovery (or series end)."""
    eq = (1 + r).cumprod()
    pk = eq.cummax()
    dd = eq / pk - 1.0
    out, i, n = [], 0, len(r)
    idx = r.index
    ddv, pkv = dd.values, pk.values
    while i < n:
        if ddv[i] < -thresh:
            j = i
            while j > 0 and ddv[j - 1] < 0:
                j -= 1                                  # walk back to the peak
            k = i
            while k < n - 1 and ddv[k] < 0:
                k += 1
            out.append((idx[j], idx[min(k, n - 1)]))
            i = k + 1
        else:
            i += 1
    merged = []
    for a, b in out:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged, pd.Series(ddv, index=idx), pd.Series(pkv, index=idx)


def depth(r, a, b):
    s = r.loc[a:b]
    eq = (1 + s).cumprod()
    return float((eq / eq.cummax() - 1.0).min())


def test_E(P, start, r0):
    print("\n" + "=" * 190)
    print("E. EPISODE AND YEAR STRUCTURE — is dMaxDD one path event and dCAGR one year?")
    arms = {a: H.run(P, H.targets(P, "V1u", *a.rsplit("-", 1)), bps=10.0)["r"].loc[start:]
            for a in ["g200-dg", "g200-rw", "abs12-rw", "v1gate-dg", "v1gate-rw"]}

    eps, dd0, _ = episodes(r0)
    m0 = metrics(r0)
    trough = dd0.idxmin()
    print(f"\n  E2. control has {len(eps)} drawdown episodes deeper than 10%; whole-window "
          f"MaxDD {m0['MaxDD']:.2%} troughs {trough.date()}")
    rows = []
    for a, ra in arms.items():
        wins = 0
        rec = dict(arm=a, whole_dMaxDD=(abs(m0["MaxDD"]) - abs(metrics(ra)["MaxDD"])) * 100)
        for k, (s, e) in enumerate(eps):
            d0, da = depth(r0, s, e), depth(ra, s, e)
            rec[f"ep{k}"] = (abs(d0) - abs(da)) * 100
            wins += int(abs(da) < abs(d0))
        rec["shallower_in"] = f"{wins}/{len(eps)}"
        rows.append(rec)
    E2 = pd.DataFrame(rows)
    hdr = "  ".join(f"ep{k}[{s.date()}..{e.date()} {depth(r0, s, e):.1%}]"
                    for k, (s, e) in enumerate(eps))
    print(f"  episodes: {hdr}")
    print("  per-episode dDepth in pp (positive = arm shallower):")
    print(E2.to_string(index=False, float_format=F3))

    print("\n  E1. annual net returns and dCAGR contribution (10 bps)")
    yr = pd.DataFrame({"control": (1 + r0).groupby(r0.index.year).prod() - 1})
    for a, ra in arms.items():
        yr[a] = (1 + ra).groupby(ra.index.year).prod() - 1
    print((yr * 100).to_string(float_format=F3))
    print("\n  E1b. leave-one-year-out on the full-sample price (drop that year's days, "
          "recompute CAGR/MaxDD/price):")
    rows = []
    for y in sorted(set(r0.index.year)):
        keep0 = r0[r0.index.year != y]
        rec = dict(drop=y)
        for a, ra in arms.items():
            p = px_price(keep0, ra[ra.index.year != y])
            rec[f"{a}_rate"] = p["rate"]
            rec[f"{a}_dC"] = p["dCAGR"]
        rows.append(rec)
    E1 = pd.DataFrame(rows)
    print(E1.to_string(index=False, float_format=F3))
    for a in arms:
        s = E1[f"{a}_rate"].dropna()
        print(f"   {a:>10}: LOYO rate sign flips to >=0 in {int((s >= 0).sum())}/{len(s)} "
              f"year-deletions; range [{s.min():.3f}, {s.max():.3f}]")
    return E1, E2, yr


# ================================================================ F. capacity
def test_F(P, start):
    print("\n" + "=" * 190)
    print("F. CAPACITY — dollar ADV of the names V1u/small actually holds, and the traded "
         "fraction of it")
    vol = pd.read_csv(ROOT / "data" / "volume_small.csv.gz", index_col=0, parse_dates=True)
    vol = vol.reindex(P.index)[[c for c in P.columns if c in vol.columns]]
    dv = (vol * P[vol.columns]).rolling(20).median()          # 20d median dollar volume
    W = H.targets(P, "V1u").loc[start:]
    reb = W.index[H.rebalance_mask(W.index, FREQ).values]
    held = W.loc[reb] > 0
    dvr = dv.reindex(index=reb, columns=W.columns)
    vals = dvr.where(held).stack().dropna()
    q = vals.quantile([0.05, 0.25, 0.50, 0.75, 0.95])
    print(f"  held-name 20d median dollar volume over {len(reb)} rebalance dates, "
          f"{len(vals)} name-dates:")
    print("   " + "  ".join(f"p{int(k*100)} ${v/1e6:,.2f}M" for k, v in q.items()))
    res = H.run(P, H.targets(P, "V1u"), bps=10.0)
    to_yr = res["to"].loc[start:].sum() / metrics(res["r"].loc[start:])["Years"]
    print(f"  book turnover {to_yr:.1f}x/yr = {to_yr/52:.3f} of NAV traded per weekly rebalance; "
          f"position size {GROSS/H.NV1:.0%} of NAV")
    med = float(q.loc[0.50])
    for cap in (1e6, 1e7, 1e8):
        pos = cap * GROSS / H.NV1
        print(f"   at ${cap/1e6:,.0f}M capital: position ${pos/1e6:,.2f}M = "
              f"{pos/med:6.1%} of the MEDIAN held name's daily dollar volume "
              f"(p5 name: {pos/float(q.loc[0.05]):8.1%})")
    return q, vals


# ================================================================ G. portability
def test_G():
    print("\n" + "=" * 190)
    print("G. PORTABILITY — the same V1u book and the same 10 arms on u56 and broad, 10 bps")
    rows = []
    for pn in ("u56", "broad"):
        px, _ = panel(pn)
        st = px.index[260]
        r0 = H.run(px, H.targets(px, "V1u"), bps=10.0)["r"].loc[st:]
        for a in ARMS:
            g, cv = a.rsplit("-", 1)
            ra = H.run(px, H.targets(px, "V1u", g, cv), bps=10.0)["r"].loc[st:]
            rows.append(dict(panel=pn, arm=a, **px_price(r0, ra)))
    G = pd.DataFrame(rows)
    print(G.to_string(index=False, float_format=F3))
    for pn in ("u56", "broad"):
        f = G[G.panel == pn].dropna(subset=["rate"])
        print(f"   {pn:>5}: priceable {len(f)}/10, negative {int((f.rate < 0).sum())}, "
              f"median rate {f.rate.median():.3f}, median dCAGR "
              f"{G[G.panel == pn].dCAGR.median():+.3f} pp")
    return G


# ================================================================ H. PROTOCOL 3/4/8
def test_H(P, start, bars, v1_net, spy, C):
    print("\n" + "=" * 190)
    print("H. PROTOCOL rules 3, 4, 8 — every arm vs live RULES v1 and vs SPY; 4a/4b; "
          "walk-forward")
    ms = metrics(spy)
    print(f"  SPY on the small window: CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} "
          f"MaxDD {ms['MaxDD']:.2%} halves {bars['s1']:.3f}/{bars['s2']:.3f} OOS "
          f"{bars['soos']:.3f} ({bars['soos_cagr']:.2%}, {bars['soos_dd']:.2%})")
    mv = metrics(v1_net)
    print(f"  live RULES v1 on small @10bps: CAGR {mv['CAGR']:.2%} Sharpe {mv['Sharpe']:.3f} "
          f"MaxDD {mv['MaxDD']:.2%} halves {halves(v1_net)[0]:.3f}/{halves(v1_net)[1]:.3f} "
          f"OOS {metrics(v1_net.loc[OOS_START:])['Sharpe']:.3f}")
    print(f"  4b bars: Sharpe > {bars['s1']:.3f}/{bars['s2']:.3f}/{bars['soos']:.3f}, "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")

    rows = []
    for a in ["control"] + ARMS:
        spec = (None, "dg") if a == "control" else tuple(a.rsplit("-", 1))
        res = H.run(P, H.targets(P, "V1u", *spec), bps=10.0)
        r = res["r"].loc[start:]
        m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
        h1, h2 = halves(r)
        rows.append(dict(arm=a, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                         IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                         TO=res["to"].loc[start:].sum() / m["Years"], **flags(r, bars, v1_net)))
    W = pd.DataFrame(rows)
    print("\n  every V1u/small arm, 10 bps, full + halves + IS + OOS:")
    print(W[["arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_MaxDD", "OOS_CAGR",
             "OOS_Sharpe", "OOS_MaxDD", "TO", "p4a", "p4b", "f4b"]]
          .to_string(index=False, float_format=F3))
    print(f"  4b passes: {int(W.p4b.sum())}/{len(W)}   4a passes: {int(W.p4a.sum())}/{len(W)}")

    # IS price list for the selectors
    isr = {}
    for a in ["control"] + ARMS:
        spec = (None, "dg") if a == "control" else tuple(a.rsplit("-", 1))
        isr[a] = H.run(P, H.targets(P, "V1u", *spec), bps=10.0)["r"].loc[start:]
    pl = []
    for a in ARMS:
        pi = px_price(isr["control"].loc[:IS_END], isr[a].loc[:IS_END])
        po = px_price(isr["control"].loc[OOS_START:], isr[a].loc[OOS_START:])
        pl.append(dict(arm=a, IS_rate=pi["rate"], IS_dMaxDD=pi["dMaxDD"], IS_dCAGR=pi["dCAGR"],
                       IS_Sharpe=metrics(isr[a].loc[:IS_END])["Sharpe"],
                       OOS_rate=po["rate"], OOS_dMaxDD=po["dMaxDD"], OOS_dCAGR=po["dCAGR"],
                       OOS_Sharpe=metrics(isr[a].loc[OOS_START:])["Sharpe"]))
    PL = pd.DataFrame(pl)
    print("\n  rule 8 — IS (2010-2016) vs OOS (2017-2026) price and Sharpe, every arm:")
    print(PL.to_string(index=False, float_format=F3))
    print(f"   IS-negative rates: {int((PL.IS_rate < 0).sum())}/{PL.IS_rate.notna().sum()} "
          f"priceable | OOS-negative: {int((PL.OOS_rate < 0).sum())}/{PL.OOS_rate.notna().sum()}"
          f" | sign agreement IS->OOS: "
          f"{int(((PL.IS_rate < 0) == (PL.OOS_rate < 0))[PL.IS_rate.notna() & PL.OOS_rate.notna()].sum())}"
          f"/{int((PL.IS_rate.notna() & PL.OOS_rate.notna()).sum())}")

    print("\n  rule 8 walk-forward — both selectors fixed before any OOS number was read:")
    picks = {}
    el = PL[PL.IS_dMaxDD >= 1.0].dropna(subset=["IS_rate"])
    picks["S1 (idea 94: argmin IS price among IS dMaxDD>=1pp)"] = (
        el.loc[el.IS_rate.idxmin(), "arm"] if len(el) else None)
    picks["S2 (argmax IS Sharpe over the 10 gate arms)"] = PL.loc[PL.IS_Sharpe.idxmax(), "arm"]
    for label, arm in picks.items():
        if arm is None:
            print(f"   {label}: no eligible arm")
            continue
        r = isr[arm]
        mo, m = metrics(r.loc[OOS_START:]), metrics(r)
        vo = metrics(v1_net.loc[OOS_START:])
        print(f"   {label}\n      pick = {arm}: OOS CAGR {mo['CAGR']:.2%} Sharpe "
              f"{mo['Sharpe']:.3f} MaxDD {mo['MaxDD']:.2%}   vs live-v1 OOS "
              f"{vo['CAGR']:.2%}/{vo['Sharpe']:.3f}/{vo['MaxDD']:.2%}   vs SPY OOS "
              f"{bars['soos_cagr']:.2%}/{bars['soos']:.3f}/{bars['soos_dd']:.2%}   "
              f"full {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%}")
    return W, PL


# ================================================================ I. does the gate bind?
def test_I(P, start):
    print("\n" + "=" * 190)
    print("I. MECHANISM — how often does the gate actually change the book, and what kind of "
          "name does the inverse-vol scaler pick?  (target weights only, no simulation)")
    reb = P.loc[start:].index[H.rebalance_mask(P.loc[start:].index, FREQ).values]
    W0 = H.targets(P, "V1u").reindex(reb) > 0
    v = H.vol20(P).reindex(reb)
    rows = []
    for a in ARMS:
        g, cv = a.rsplit("-", 1)
        Wa = H.targets(P, "V1u", g, cv).reindex(reb) > 0
        diff = (W0 != Wa).any(axis=1)
        nout = (W0 & ~Wa).sum(axis=1)
        rows.append(dict(arm=a, dates_changed=f"{int(diff.sum())}/{len(reb)}",
                         pct_dates=100 * diff.mean(),
                         mean_names_gated_out=float(nout.mean()),
                         max_names_gated_out=int(nout.max()),
                         med_vol20_of_gated_out=float(v.where(W0 & ~Wa).stack().median()),
                         med_vol20_of_kept=float(v.where(W0 & Wa).stack().median())))
    I = pd.DataFrame(rows)
    print(I.to_string(index=False, float_format=F3))
    for sc, lab in ((True, "scaler on (V1u)"), (False, "scaler off")):
        Wx = v1_targets(P, 5, sc).reindex(reb) > 0
        vv = v.where(Wx).stack()
        print(f"  top-5 picks, {lab:16}: median vol20 of held names {vv.median():.3f}  "
              f"(panel median {v.stack().median():.3f}); "
              f"share of picks with vol20 at the 0.08 clip floor "
              f"{float((v.where(Wx).stack() <= 0.08).mean()):.1%}")
    return I


# ================================================================ main
def main():
    P, spy_full = small_panel()
    start = P.index[260]
    spy = spy_full.reindex(P.index).fillna(0.0).loc[start:]
    bars = bars_of(spy)
    v1_net = backtest(P, rules_v1_weights(P), cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
    print(f"PANEL small — {P.shape[1]} holdable names, {P.index[0].date()} -> "
          f"{P.index[-1].date()}, evaluated from {start.date()} | IS <= {IS_END} | "
          f"OOS >= {OOS_START}")

    r0, A = test_A(P, start)
    B = test_B(P, start)
    C = test_C(P, start, bars, v1_net)
    D = test_D(P, start)
    E1, E2, YR = test_E(P, start, r0)
    q, _ = test_F(P, start)
    G = test_G()
    W, PL = test_H(P, start, bars, v1_net, spy, C)
    I = test_I(P, start)

    print("\n" + "=" * 190)
    print("PREDICTION SCORECARD")
    b0 = B[(B.cost == 0.0) & (B.arm != "control")]
    b10 = B[(B.cost == 10.0) & (B.arm != "control")]
    print(f"  P1 (sign is a cost story; median gate dCAGR >= 0 at 0 bps): "
          f"0 bps median dCAGR {b0.dCAGR.median():+.3f} pp vs 10 bps {b10.dCAGR.median():+.3f} pp "
          f"-> {'CONFIRMED' if b0.dCAGR.median() >= 0 else 'REFUTED'}")
    cn = C[(C.arm != "control")].dropna(subset=["rate"])
    n5 = cn[cn.n == 5]
    n20 = cn[cn.n >= 20]
    print(f"  P2 (negative prices concentrate at n=5, gone by n=20): n=5 neg "
          f"{int((n5.rate < 0).sum())}/{len(n5)}, n>=20 neg {int((n20.rate < 0).sum())}/{len(n20)}"
          f" -> {'CONFIRMED' if (n20.rate < 0).sum() == 0 and (n5.rate < 0).sum() > 0 else 'see table'}")
    fd = D.dropna(subset=["rate"])
    frac = (fd.rate < 0).mean() if len(fd) else np.nan
    print(f"  P3 (<70% of sub-panels reproduce rate<0): {frac:.0%} -> "
          f"{'CONFIRMED' if frac < 0.70 else 'REFUTED'}")
    ws = E2.shallower_in.tolist()
    print(f"  P4 (arm shallower in <=60% of the control's >10% episodes): {ws} -> see table")
    print(f"  P5 (no 4b pass on small; WF pick OOS Sharpe < SPY's {bars['soos']:.3f}): "
          f"4b passes {int(W.p4b.sum()) + int(C.p4b.sum())} across {len(W) + len(C)} arm-points")
    print(f"  P6 (at $10M the book trades >10% of the median held name's ADV): "
          f"{(1e7*GROSS/H.NV1)/float(q.loc[0.50]):.1%} -> "
          f"{'CONFIRMED' if (1e7*GROSS/H.NV1)/float(q.loc[0.50]) > 0.10 else 'REFUTED'}")

    A.to_csv(OUT / f"{STEM}.reproduction.csv", index=False)
    B.to_csv(OUT / f"{STEM}.costaxis.csv", index=False)
    C.to_csv(OUT / f"{STEM}.concentration.csv", index=False)
    D.to_csv(OUT / f"{STEM}.subpanels.csv", index=False)
    E1.to_csv(OUT / f"{STEM}.loyo.csv", index=False)
    E2.to_csv(OUT / f"{STEM}.episodes.csv", index=False)
    YR.to_csv(OUT / f"{STEM}.annual.csv")
    G.to_csv(OUT / f"{STEM}.portability.csv", index=False)
    W.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    PL.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    I.to_csv(OUT / f"{STEM}.binding.csv", index=False)
    print("\nwrote 11 csv companions next to this script.")


if __name__ == "__main__":
    main()
