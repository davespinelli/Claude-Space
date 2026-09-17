#!/usr/bin/env python3
"""Idea 1154 (lane C, 2026-09-17) — why do ALL THREE honest CHOOSERS land on a GROSS ENDPOINT?

Idea 1150 found that on the 33-rung gross ladder C_ISSHARPE and C_ISCAGR both pick gross
1.00 and C_ISDD picks 0.20 on BOTH panels, i.e. every IS-only chooser lands on one of the
two ENDPOINTS (which are also the two binding legs), 0 of 48 picks clears 4b, while 21 of
66 cells at 10 bps do.  The queue asks two things:

  (Q1) is an ENDPOINT PICK a general property of a MONOTONE dial?
  (Q2) what would a chooser have to SCORE to reach the INTERIOR?

Q1 has an algebraic half and an empirical half and this run separates them BEFORE reading
any number.  THE ALGEBRAIC HALF IS AN IDENTITY, NOT A FINDING: the argmax of a weakly
monotone sequence is always attainable at an endpoint, so MONOTONE => ENDPOINT is true by
construction on any dial, any tape, any statistic.  Gate G9 verifies the identity on random
sequences so the run cannot be read as having discovered it.  The empirical content is
therefore entirely in (i) HOW OFTEN a dial IS monotone in the statistic a chooser reads,
(ii) whether the CONVERSE holds — do NON-monotone dials still pick endpoints — and (iii)
Q2's premium.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  CHOOSER {C_ISSHARPE, C_ISCAGR, C_ISDD, C_ISMAR, C_IS4B}   (5, all IS-only)
  DIAL    {D_GROSS, D_N, D_HOLD, D_CADENCE, D_MAXVOL}       (5 ladders, 66 rungs per panel)
= 25 (chooser, dial) cells per panel, 50 in all, EVERY ONE PUBLISHED.  The RUNG inside a
dial is NOT a third tuned parameter: it is the object the chooser selects, which is the
whole subject of the run, and every rung of every dial is published in `.grid.csv`
regardless of what any chooser did with it.  PANEL {U56, B136} is NOT a dial — both are
reported everywhere and nothing is ever selected on the pair.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1150's construction so the numbers
cross-read: CAND20 legs [(21,252),(0,126),(0,63)], cap INF, max_vol 0.60, min hold 126,
N=20, gross 0.75, cadence W, cost 10 bps (PROTOCOL rule 2 — a book cannot choose its cost
rate), LAG 1, warm-up 260, IS end 2016-12-31, zero cash, block L=63, 1000 draws, crc32
seeds, q=0.90.  Each dial moves ONE of those constants and holds the rest.

PRICE VINTAGE, PINNED AND DECLARED (the defect idea 1160 published on 2026-09-17).
`data/prices.csv` gained the 2026-09-16 bar mid-session; the record's committed anchors were
computed on tapes ending 2026-09-15 and no longer reproduce to their own tolerances on the
current file.  Every tape here is truncated at PIN = 2026-09-15 (a no-op for B136, which
ends 2026-09-11) and gates G2/G3 are run BOTH ways so the vintage is published, not absorbed.

Writes: .gates.csv .grid.csv .mono.csv .picks.csv .premium.csv .reach.csv .hypotheses.csv
        .walkforward.csv .console.txt
Deterministic, standalone, no network.  Does not modify RULES.md / scan.py / bot.py /
baseline.py.
"""
import sys, time, zlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "why-do-ALL-THREE-honest-CHOOSERS-land-on-a-GROSS-ENDPOINT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

PIN = "2026-09-15"
LAG, WARMUP, MAXVOL0 = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, COST0 = 0.75, "W", 126, 20, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136"]

# ----------------------------------------------------------------- THE DIALS (param 2 of 2)
# Canonical rung ORDER is declared here and never re-chosen; monotonicity is defined against
# it.  D_CADENCE is ordered by bars-between-rebalances ASCENDING (D fastest .. Q slowest).
LAD = {
    "D_GROSS":   [round(0.20 + 0.025 * i, 3) for i in range(33)],   # 1150's ladder, verbatim
    "D_N":       [3, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50],
    "D_HOLD":    [5, 10, 21, 42, 63, 90, 126, 189, 252],
    "D_CADENCE": ["D", "W", "2W", "M", "2M", "Q"],
    "D_MAXVOL":  [0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 2.00],
}
DIALS = list(LAD)

# ---------------------------------------------------------------- THE CHOOSERS (param 1 of 2)
# All five are IS-ONLY (2009-01..2016-12 after warm-up).  None of them can see one bar after
# IS_END.  Each is a pure argmax of a statistic re-expressed so that HIGHER IS BETTER.
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD", "C_ISMAR", "C_IS4B"]

Q_HEAD, L_HEAD, BDRAWS, SEED_BASE = 0.90, 63, 1000, 11541154

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)      # U56 W/H126/N=20, 10 bps
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
# 1150's committed gross-dial picks — the object this run extends (G8)
A1150_PICKS = {("C_ISSHARPE", "U56"): 1.000, ("C_ISSHARPE", "B136"): 1.000,
               ("C_ISCAGR", "U56"): 1.000, ("C_ISCAGR", "B136"): 1.000,
               ("C_ISDD", "U56"): 0.200, ("C_ISDD", "B136"): 0.200}

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------- 1082/1098/1102/1108/1117/1150's fast runner, verbatim
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
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
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    """Score and the two eligibility ingredients.  maxvol is applied later (it is a dial)."""
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, above.values, vol20.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


# ---------------------------------------------------------- THE IS-ONLY 4b MARGIN (chooser 5)
# Same signed-fraction currency 1150 declared, but computed on the IS WINDOW ONLY so the
# chooser stays honest: three legs (IS Sharpe vs SPY IS Sharpe, IS drawdown cap, IS CAGR
# floor), and C_IS4B maximises the MINIMUM of the three.
def is_margins(b, sb):
    cap = DD_CAP * abs(sb["IS_MaxDD"])
    flo = CAGR_FLOOR * sb["IS_CAGR"]
    return {"M_S": (b["IS_Sharpe"] - sb["IS_Sharpe"]) / abs(sb["IS_Sharpe"]),
            "M_DD": (cap - abs(b["IS_MaxDD"])) / cap,
            "M_CAGR": (b["IS_CAGR"] - flo) / abs(flo)}


# ---------------------------------------------------------------- MONOTONICITY, DECLARED FIRST
# v is the chooser's statistic over the ladder's canonical rung order, re-expressed so that
# HIGHER IS BETTER.  MONO is exact (every consecutive difference has one sign, ties allowed).
# mono_score is the largest share of steps with a single strict sign and is reported for the
# cells that are not exactly monotone, so a near-ladder is distinguishable from a jumble.
def mono_of(v):
    d = np.diff(np.asarray(v, float))
    d = d[np.isfinite(d)]
    if len(d) == 0:
        return dict(mono=False, direction="none", mono_score=np.nan, rho=np.nan)
    up, dn = bool((d >= 0).all()), bool((d <= 0).all())
    m = bool(up or dn)
    sc = max(float((d > 0).mean()), float((d < 0).mean()))
    x = np.arange(len(v), dtype=float)
    ok = np.isfinite(np.asarray(v, float))
    rho = np.nan
    if ok.sum() > 2:
        a = pd.Series(np.asarray(v, float)[ok]).rank().values
        b = pd.Series(x[ok]).rank().values
        rho = float(np.corrcoef(a, b)[0, 1])
    return dict(mono=m, direction=("up" if up and not dn else "down" if dn and not up else
                                   "flat" if up and dn else "none"),
                mono_score=sc, rho=rho)


def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_stats(R, idx, chunk=50):
    """CAGR, Sharpe, |MaxDD| of R under each block-bootstrap draw (PAIRED index)."""
    nd, TL = idx.shape
    out = np.empty((nd, 3))
    for a in range(0, nd, chunk):
        b = min(a + chunk, nd)
        X = R[idx[a:b]]
        eq = np.cumprod(1.0 + X, axis=1)
        out[a:b, 0] = eq[:, -1] ** (252.0 / TL) - 1.0
        vol = X.std(axis=1, ddof=1) * np.sqrt(252.0)
        out[a:b, 1] = (X.mean(axis=1) * 252.0) / vol
        out[a:b, 2] = np.abs((eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1))
    return out


def cadence_mask(idx, spec):
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


def stat_of(chooser, m, sb):
    """The chooser's statistic, HIGHER IS BETTER, IS-window only."""
    if chooser == "C_ISSHARPE":
        return m["IS_Sharpe"]
    if chooser == "C_ISCAGR":
        return m["IS_CAGR"]
    if chooser == "C_ISDD":
        return -abs(m["IS_MaxDD"])
    if chooser == "C_ISMAR":
        return m["IS_CAGR"] / abs(m["IS_MaxDD"]) if m["IS_MaxDD"] else np.nan
    if chooser == "C_IS4B":
        return min(is_margins(m, sb).values())
    raise KeyError(chooser)


def boot_stat_vec(chooser, bs, sb):
    """The same statistic evaluated on a bootstrap draw matrix (CAGR, Sharpe, |dd|)."""
    if chooser == "C_ISSHARPE":
        return bs[:, 1]
    if chooser == "C_ISCAGR":
        return bs[:, 0]
    if chooser == "C_ISDD":
        return -bs[:, 2]
    if chooser == "C_ISMAR":
        return bs[:, 0] / np.maximum(bs[:, 2], 1e-12)
    if chooser == "C_IS4B":
        cap = DD_CAP * abs(sb["IS_MaxDD"])
        flo = CAGR_FLOOR * sb["IS_CAGR"]
        return np.minimum.reduce([(bs[:, 1] - sb["IS_Sharpe"]) / abs(sb["IS_Sharpe"]),
                                  (cap - bs[:, 2]) / cap,
                                  (bs[:, 0] - flo) / abs(flo)])
    raise KeyError(chooser)


def main():
    t0 = time.time()
    P(f"# Idea 1154 (lane C, {DATE}) — why do ALL THREE honest CHOOSERS land on a GROSS ENDPOINT?")
    P("#")
    P("# THE QUESTION SPLIT BEFORE ANY NUMBER IS READ.")
    P("#   (Q1) is an ENDPOINT pick a general property of a MONOTONE dial?")
    P("#   (Q2) what would a chooser have to SCORE to reach the INTERIOR?")
    P("# Q1's forward direction is an ALGEBRAIC IDENTITY, NOT A FINDING: the argmax of a weakly")
    P("#   monotone sequence is always attainable at an endpoint.  G9 verifies the identity on")
    P("#   random sequences so this run cannot be read as having discovered it.  The empirical")
    P("#   content is (i) how often a dial IS monotone in the statistic a chooser reads, (ii) the")
    P("#   CONVERSE — do NON-monotone dials still pick endpoints — and (iii) Q2's premium.")
    P("#")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4, the two the queue names): CHOOSER {CHOOSERS}")
    P(f"#   x DIAL {DIALS} = {len(CHOOSERS) * len(DIALS)} cells per panel, "
      f"{len(CHOOSERS) * len(DIALS) * len(PANELS)} in all, EVERY ONE PUBLISHED.")
    P(f"#   The RUNG inside a dial is NOT a third tuned parameter — it is the object the chooser")
    P(f"#   SELECTS, which is the subject of the run; all {sum(len(v) for v in LAD.values())} rungs "
      f"per panel are published in .grid.csv whatever any chooser did.")
    P("# PANEL {U56, B136} is NOT a dial (both reported everywhere, nothing selected on the pair).")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL0}, min hold {HOLD0}, N {N0},")
    P(f"#   gross {GROSS0}, cadence {FREQ0}, cost {COST0} bps (rule 2), LAG {LAG}, warm-up {WARMUP},")
    P(f"#   IS end {IS_END}, zero cash, block L={L_HEAD}, {BDRAWS} draws, crc32 seeds, q={Q_HEAD}.")
    P(f"# PRICE VINTAGE PINNED at {PIN} (idea 1160's defect); G2/G3 run BOTH ways.")
    P("#")
    P("# LADDERS, canonical order declared here and never re-chosen:")
    for k in DIALS:
        P(f"#   {k:<10s} {len(LAD[k]):2d} rungs  {LAD[k]}")
    P("#")
    P("# DEFINITIONS, DECLARED BEFORE ANY NUMBER:")
    P("#   MONO(dial, chooser) — every consecutive difference of the chooser's statistic over the")
    P("#     ladder's canonical order has ONE sign (ties allowed).  mono_score = largest share of")
    P("#     steps with a single strict sign, so a near-ladder is distinguishable from a jumble.")
    P("#   ENDPOINT pick — argmax rung index in {0, R-1}.  INTERIOR pick — anything else.")
    P("#   PREMIUM (Q2's answer) — need = best ENDPOINT value - best INTERIOR value, in the")
    P("#     chooser's own units.  need > 0 means the interior FALLS SHORT by that much and the")
    P("#     chooser would have to see the interior gain `need` to select it.  need/SD is the same")
    P("#     figure in units of the PAIRED block-bootstrap SD of that very difference (same draws")
    P("#     on both arms, so the tape cancels), i.e. how many noise units the preference is worth.")
    P("#")
    P("# HYPOTHESES, DECLARED BEFORE ANY NUMBER:")
    P("#   H_IDENTITY   MONO => ENDPOINT holds at 100% of monotone cells.  This is an IDENTITY;")
    P("#                a failure would mean a code bug, not a discovery.  Bar: 1.000.")
    P("#   H_CONVERSE   the converse FAILS: >= 1 NON-monotone (chooser, dial, panel) cell still")
    P("#                picks an endpoint.  Endpoint picking is therefore NOT diagnostic of")
    P("#                monotonicity, which is what 1150's three-for-three would otherwise suggest.")
    P("#   H_GROSSFLAT  on D_GROSS, IS Sharpe is NOT monotone (1150 measured a full-sample Sharpe")
    P("#                spread of 0.0016 across the whole ladder) while IS CAGR and IS MaxDD ARE.")
    P("#                So C_ISSHARPE's gross-1.00 pick is a FLAT-DIAL NOISE ARGMAX and C_ISCAGR's")
    P("#                and C_ISDD's are MECHANICAL — the same pick for two different reasons.")
    P("#   H_INTERIOR   at least one (chooser, dial) cell picks the INTERIOR, i.e. endpoint picking")
    P("#                is a property of the GROSS dial's shape and not of IS-only choosing.")
    P("#   H_UNRESOLVED at the majority of ENDPOINT picks on NON-monotone dials, |need|/SD < 1:")
    P("#                the endpoint is preferred by less than one unit of its own noise.")
    P("#   H_NOPAY      chooser picks clear 4b at a LOWER rate than the ladders' own base rate")
    P("#                (1150: 0 of 48 picks vs 21 of 66 cells).  Rule 8, on five dials this time.")
    P("# DECISION RULE, declared before any number: the queue's question is ANSWERED 'YES BUT")
    P("#   TRIVIALLY, AND MONOTONICITY IS NOT THE REASON ON THE GROSS DIAL' iff H_IDENTITY holds")
    P("#   (as it must), H_CONVERSE holds and H_GROSSFLAT holds.  If IS Sharpe turns out MONOTONE")
    P("#   in gross, the three picks have one common mechanical cause and the answer is a flat YES.")
    P("#   If H_INTERIOR fails, endpoint picking is a property of IS-only choosing itself and that")
    P("#   is a stronger and more troubling answer than the one the queue expects.")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  {name:<4s} {what:<62s} {value:.2e}   {'PASS' if ok else 'FAIL'}")

    P("## PANELS — loaded, PINNED and stamped before any result number")
    panels, raw_unpinned = {}, {}
    for panel in PANELS:
        pxu = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        raw_unpinned[panel] = pxu
        px = pxu.loc[:PIN]
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, above, vol20 = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, above=above, vol20=vol20)
        P(f"  {panel:<5s} {len(px.columns):4d} names, PINNED {len(idx):,} rows "
          f"{idx[0].date()} -> {idx[-1].date()} (unpinned ends {pxu.index[-1].date()}), "
          f"warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")
    P("")

    def elig_of(panel, maxvol):
        d = panels[panel]
        return d["above"] & (d["vol20"] < maxvol)

    def run_cell(panel, gross=GROSS0, N=N0, H=HOLD0, freq=FREQ0, maxvol=MAXVOL0, px=None, d=None):
        d = d or panels[panel]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        el = d["above"] & (d["vol20"] < maxvol)
        W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        return nrun(d["rets"], Wl, mkl)

    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], elig_of("U56", MAXVOL0), d["priced"], np.flatnonzero(mk),
              N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST0, freq=FREQ0)["returns"].values
    gr, tn = run_cell("U56")
    rfast = gr - tn * COST0 / 1e4
    gate("G1", "fast runner == engine.backtest", float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max()),
         float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max()) < 1e-12)

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]), abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", f"committed U56 W/H126/N=20 triple, PINNED at {PIN}", g2, g2 < 5e-5)
    P(f"       ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    # the vintage, published not absorbed
    pxu = raw_unpinned["U56"]
    du = dict(idx=pxu.index, K=len(pxu.columns), T=len(pxu.index),
              rets=pxu.pct_change().fillna(0.0).values, priced=pxu.notna().values)
    scu, abu, vlu = mech(pxu)
    du.update(sc=scu, above=abu, vol20=vlu)
    wu, iu, ou = windows(pxu.index)
    du.update(warm=wu, ins=iu, oos=ou)
    gru, tnu = run_cell("U56", d=du)
    mu = blocks_m(gru - tnu * COST0 / 1e4, wu, iu, ou)
    g2u = max(abs(mu["CAGR"] - A936_WH126[0]), abs(mu["Sharpe"] - A936_WH126[1]), abs(mu["MaxDD"] - A936_WH126[2]))
    P(f"       THE VINTAGE, PUBLISHED NOT ABSORBED: the same gate UNPINNED reads {g2u:.2e} "
      f"({g2u / max(g2, 1e-18):.1f}x the pinned reading) from ONE extra bar of {len(pxu):,}.")
    gaterows.append(dict(gate="G2u", what="same gate on the UNPINNED file (reported, not gated)",
                         value=float(g2u), pass_=bool(g2u < 5e-5)))

    spy_m, live_m = {}, {}
    for panel in PANELS:
        dp = panels[panel]
        spy_m[panel] = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values, dp["warm"], dp["ins"], dp["oos"])
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST0, freq="W")["returns"].values
        live_m[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g3 = max(abs(spy_m["U56"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(spy_m["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["U56"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", f"SPY OOS triple, PINNED at {PIN}", g3, g3 < 5e-4)

    g12, t12 = run_cell("U56", N=12)
    m12 = blocks_m(g12 - t12 * COST0 / 1e4, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gate("G4", "CROSS-RUN 1098/1102's committed U56 n=12 triple", g4, g4 < 5e-4)

    g5 = abs(live_m["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G5", "live RULES v2 MaxDD == committed -12.05%", g5, g5 < 5e-4)

    g12b, _ = run_cell("U56", N=12)
    gate("G6", "determinism (same cell twice)", float(np.abs(g12 - g12b).max()),
         float(np.abs(g12 - g12b).max()) == 0.0)

    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int) - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gate("G7", "cadence_mask == engine.rebalance_mask (D/W/M/Q)", float(g7), g7 == 0)

    # ---------------------------------------------------------------- THE GRID (all rungs)
    P("")
    P("## THE GRID — every rung of every dial on both panels, published whatever a chooser did")
    rows, streams = [], {}
    for panel in PANELS:
        dp = panels[panel]
        sb = spy_m[panel]
        lbm = live_m[panel]
        for dial in DIALS:
            for j, rung in enumerate(LAD[dial]):
                kw = dict(gross=GROSS0, N=N0, H=HOLD0, freq=FREQ0, maxvol=MAXVOL0)
                kw[{"D_GROSS": "gross", "D_N": "N", "D_HOLD": "H",
                    "D_CADENCE": "freq", "D_MAXVOL": "maxvol"}[dial]] = rung
                g, t = run_cell(panel, **kw)
                r = g - t * COST0 / 1e4
                mm = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
                streams[(panel, dial, j)] = r
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm)
                imr = is_margins(mm, sb)
                row = dict(panel=panel, dial=dial, rung_i=j, rung=str(rung),
                           n_rungs=len(LAD[dial]),
                           turn_per_yr=float(t[dp["warm"]].sum() / (dp["warm"].sum() / 252.0)),
                           **{k: float(v) for k, v in mm.items()},
                           **{k: float(v) for k, v in imr.items()},
                           **{k: bool(v) for k, v in l4b.items()},
                           **{k: bool(v) for k, v in l4bo.items()},
                           **{k: bool(v) for k, v in l4a.items()},
                           pass_4b=bool(all(l4b.values())), pass_4b_oos=bool(all(l4bo.values())),
                           pass_4a=bool(all(l4a.values())))
                for ch in CHOOSERS:
                    row[f"S_{ch}"] = float(stat_of(ch, mm, sb))
                rows.append(row)
        P(f"  {panel}: {sum(len(LAD[x]) for x in DIALS)} rungs run  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(rows)
    dump(grid, "grid")

    # G8 — 1150's committed gross-dial picks must reproduce
    g8bad = 0
    for (ch, panel), want in A1150_PICKS.items():
        sub = grid[(grid.panel == panel) & (grid.dial == "D_GROSS")].sort_values("rung_i")
        got = float(sub.iloc[int(np.nanargmax(sub[f"S_{ch}"].values))]["rung"])
        if abs(got - want) > 1e-9:
            g8bad += 1
            P(f"       G8 mismatch: {ch} on {panel} picks {got} not 1150's {want}")
    gate("G8", "CROSS-RUN 1150's three gross-dial picks on both panels", float(g8bad), g8bad == 0)

    # G9 — the IDENTITY, on synthetic monotone sequences (so the run cannot claim to find it)
    rng = np.random.default_rng(seed_of("identity"))
    bad = 0
    for _ in range(20000):
        v = np.sort(rng.normal(size=rng.integers(3, 34)))
        if rng.random() < 0.5:
            v = v[::-1]
        if int(np.argmax(v)) not in (0, len(v) - 1):
            bad += 1
    gate("G9", "IDENTITY argmax(monotone) is an endpoint, 20,000 synthetic", float(bad), bad == 0)

    # G10 — the ladders nest the record's committed rungs
    nest = (all(abs(x - y) < 1e-9 for x, y in
                zip([r for r in LAD["D_GROSS"] if abs(r * 20 - round(r * 20)) < 1e-9],
                    [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75,
                     0.80, 0.85, 0.90, 0.95, 1.00]))
            and N0 in LAD["D_N"] and 12 in LAD["D_N"] and HOLD0 in LAD["D_HOLD"]
            and FREQ0 in LAD["D_CADENCE"] and "M" in LAD["D_CADENCE"] and MAXVOL0 in LAD["D_MAXVOL"])
    gate("G10", "ladders NEST the record's committed rungs (0.05 gross, n=12/20, H=126, W/M)",
         float(nest), nest)
    P(f"  GATES {sum(gates.values())} of {len(gates)} PASS")

    # ------------------------------------------------------- MONOTONICITY + PICKS + PREMIUM
    P("")
    P("## MONOTONICITY, PICKS AND THE INTERIOR PREMIUM — 5 choosers x 5 dials x 2 panels = 50 cells")
    monorows, pickrows, premrows, reachrows, wfrows = [], [], [], [], []
    for panel in PANELS:
        dp = panels[panel]
        sb, lbm = spy_m[panel], live_m[panel]
        Tis = int(dp["ins"].sum())
        rngb = np.random.default_rng(seed_of("boot", panel))
        bidx, _ = block_index(rngb, Tis, L_HEAD, BDRAWS)
        for dial in DIALS:
            sub = grid[(grid.panel == panel) & (grid.dial == dial)].sort_values("rung_i").reset_index(drop=True)
            R = len(sub)
            for ch in CHOOSERS:
                v = sub[f"S_{ch}"].values.astype(float)
                mo = mono_of(v)
                k = int(np.nanargmax(v))
                ties = int(np.sum(np.isclose(v, v[k], rtol=0, atol=1e-12)))
                endpoint = k in (0, R - 1)
                monorows.append(dict(panel=panel, dial=dial, chooser=ch, n_rungs=R,
                                     mono=mo["mono"], direction=mo["direction"],
                                     mono_score=mo["mono_score"], rho=mo["rho"],
                                     pick_i=k, pick=str(sub.rung[k]), endpoint=endpoint,
                                     ties=ties,
                                     spread=float(np.nanmax(v) - np.nanmin(v))))
                pr = sub.iloc[k]
                pickrows.append(dict(panel=panel, dial=dial, chooser=ch, pick=str(pr.rung),
                                     pick_i=k, endpoint=endpoint, mono=mo["mono"],
                                     IS_Sharpe=pr.IS_Sharpe, IS_CAGR=pr.IS_CAGR, IS_MaxDD=pr.IS_MaxDD,
                                     CAGR=pr.CAGR, Sharpe=pr.Sharpe, MaxDD=pr.MaxDD,
                                     H1=pr.H1, H2=pr.H2,
                                     OOS_CAGR=pr.OOS_CAGR, OOS_Sharpe=pr.OOS_Sharpe,
                                     OOS_MaxDD=pr.OOS_MaxDD,
                                     pass_4b=bool(pr.pass_4b), pass_4b_oos=bool(pr.pass_4b_oos),
                                     pass_4a=bool(pr.pass_4a),
                                     ladder_4b=int(sub.pass_4b.sum()),
                                     ladder_4b_oos=int(sub.pass_4b_oos.sum()),
                                     ladder_4a=int(sub.pass_4a.sum()), n_rungs=R))
                wfrows.append(dict(panel=panel, dial=dial, chooser=ch, arm=f"PICK {pr.rung}",
                                   chosen_on="IS 2009-2016 only",
                                   OOS_CAGR=pr.OOS_CAGR, OOS_Sharpe=pr.OOS_Sharpe,
                                   OOS_MaxDD=pr.OOS_MaxDD, full_CAGR=pr.CAGR, full_Sharpe=pr.Sharpe,
                                   full_MaxDD=pr.MaxDD, H1=pr.H1, H2=pr.H2,
                                   pass_4b=bool(pr.pass_4b), pass_4b_oos=bool(pr.pass_4b_oos),
                                   pass_4a=bool(pr.pass_4a)))

                # ---- Q2: THE PREMIUM.  What would it have to score to reach the interior?
                ei = 0 if v[0] >= v[R - 1] else R - 1
                inner = v[1:R - 1]
                ii = int(np.nanargmax(inner)) + 1 if len(inner) and np.isfinite(inner).any() else -1
                need = float(v[ei] - v[ii]) if ii > 0 else np.nan
                sd = ci_lo = ci_hi = np.nan
                if ii > 0:
                    Re = streams[(panel, dial, ei)][dp["ins"]]
                    Ri = streams[(panel, dial, ii)][dp["ins"]]
                    de = boot_stat_vec(ch, boot_stats(Re, bidx), sb)
                    di = boot_stat_vec(ch, boot_stats(Ri, bidx), sb)
                    diff = de - di                    # PAIRED: same draws, tape cancels
                    sd = float(np.nanstd(diff, ddof=1))
                    ci_lo, ci_hi = (float(np.nanquantile(diff, 0.05)), float(np.nanquantile(diff, 0.95)))
                premrows.append(dict(panel=panel, dial=dial, chooser=ch, n_rungs=R,
                                     pick_i=k, endpoint=endpoint, mono=mo["mono"],
                                     best_endpoint_i=ei, best_endpoint=str(sub.rung[ei]),
                                     best_interior_i=ii, best_interior=(str(sub.rung[ii]) if ii > 0 else ""),
                                     need=need, paired_SD=sd, need_over_SD=(need / sd if sd else np.nan),
                                     paired_90lo=ci_lo, paired_90hi=ci_hi,
                                     resolvable=bool(np.isfinite(need) and np.isfinite(sd)
                                                     and abs(need) > sd)))

                # ---- the capital-relevant version of Q2: reach a rung that PASSES 4b
                okrows = sub[sub.pass_4b & sub.pass_4b_oos]
                if len(okrows):
                    best = okrows.iloc[int(np.nanargmax(okrows[f"S_{ch}"].values))]
                    reachrows.append(dict(panel=panel, dial=dial, chooser=ch,
                                          pick=str(pr.rung), pick_passes=bool(pr.pass_4b and pr.pass_4b_oos),
                                          nearest_passing=str(best.rung),
                                          stat_gap=float(v[k] - float(best[f"S_{ch}"])),
                                          pick_OOS_Sharpe=float(pr.OOS_Sharpe),
                                          passing_OOS_Sharpe=float(best.OOS_Sharpe),
                                          n_passing=int(len(okrows)), n_rungs=R))
        P(f"  {panel}: 25 cells scored  ({time.time() - t0:.0f}s)")

    mono = pd.DataFrame(monorows)
    picks = pd.DataFrame(pickrows)
    prem = pd.DataFrame(premrows)
    reach = pd.DataFrame(reachrows)
    dump(mono, "mono")
    dump(picks, "picks")
    dump(prem, "premium")
    dump(reach, "reach")

    # ------------------------------------------------------------------------ THE ANSWER
    P("")
    P("## THE ANSWER")
    n_mono = int(mono.mono.sum())
    mono_end = int((mono.mono & mono.endpoint).sum())
    h_identity = (mono_end == n_mono) and gates["G9"]
    nonmono = mono[~mono.mono]
    nonmono_end = int(nonmono.endpoint.sum())
    h_converse = nonmono_end >= 1
    P(f"  MONOTONE at {n_mono} of {len(mono)} (chooser, dial, panel) cells; of those "
      f"{mono_end} pick an ENDPOINT  -> H_IDENTITY {'HOLDS (as it must)' if h_identity else 'FAILS = BUG'}")
    P(f"  NON-MONOTONE at {len(nonmono)} cells; of those {nonmono_end} "
      f"({nonmono_end / max(len(nonmono), 1):.1%}) STILL pick an endpoint "
      f"-> H_CONVERSE {'SUPPORTED' if h_converse else 'REFUTED'}")
    P(f"  ENDPOINT picks overall: {int(mono.endpoint.sum())} of {len(mono)} "
      f"({mono.endpoint.mean():.1%});  INTERIOR picks {int((~mono.endpoint).sum())}")

    P("")
    P("  BY DIAL (endpoint share / monotone share, both panels, all five choosers):")
    for dial in DIALS:
        s = mono[mono.dial == dial]
        P(f"    {dial:<10s} endpoint {int(s.endpoint.sum())}/{len(s)}   monotone {int(s.mono.sum())}/{len(s)}"
          f"   median spread {np.nanmedian(np.abs(s.spread)):.4g}")
    P("  BY CHOOSER:")
    for ch in CHOOSERS:
        s = mono[mono.chooser == ch]
        P(f"    {ch:<11s} endpoint {int(s.endpoint.sum())}/{len(s)}   monotone {int(s.mono.sum())}/{len(s)}")

    P("")
    P("  H_GROSSFLAT — the gross dial, statistic by statistic (this is the queue's own cell):")
    gf = {}
    for panel in PANELS:
        sub = grid[(grid.panel == panel) & (grid.dial == "D_GROSS")].sort_values("rung_i")
        for ch in CHOOSERS:
            v = sub[f"S_{ch}"].values.astype(float)
            mo = mono_of(v)
            gf[(panel, ch)] = mo
            P(f"    {panel:<5s} {ch:<11s} mono {str(mo['mono']):<5s} dir {mo['direction']:<5s} "
              f"score {mo['mono_score']:.3f}  rho {mo['rho']:+.3f}  spread {np.nanmax(v) - np.nanmin(v):.4g}  "
              f"pick {sub.rung.values[int(np.nanargmax(v))]}")
    h_grossflat = (not any(gf[(p, 'C_ISSHARPE')]["mono"] for p in PANELS)) and \
                  all(gf[(p, 'C_ISCAGR')]["mono"] and gf[(p, 'C_ISDD')]["mono"] for p in PANELS)
    P(f"    -> H_GROSSFLAT {'SUPPORTED' if h_grossflat else 'REFUTED'}: IS Sharpe "
      f"{'is NOT' if not any(gf[(p, 'C_ISSHARPE')]['mono'] for p in PANELS) else 'IS'} monotone in gross, "
      f"IS CAGR and IS MaxDD {'ARE' if all(gf[(p, c)]['mono'] for p in PANELS for c in ('C_ISCAGR', 'C_ISDD')) else 'are NOT'}.")

    h_interior = bool((~mono.endpoint).any())
    P("")
    P(f"  H_INTERIOR {'SUPPORTED' if h_interior else 'REFUTED'} — "
      f"{int((~mono.endpoint).sum())} of {len(mono)} cells pick the interior:")
    for _, r in mono[~mono.endpoint].iterrows():
        P(f"    {r.panel:<5s} {r.dial:<10s} {r.chooser:<11s} picks rung {r['pick']} "
          f"(index {r.pick_i} of {r.n_rungs - 1}), mono {r.mono}")

    P("")
    P("  Q2 — THE INTERIOR PREMIUM.  need = best endpoint - best interior, in the chooser's own")
    P("     units; need/SD is the same figure in paired block-bootstrap SDs (IS window, same")
    P("     draws on both arms).  need <= 0 means the interior already wins (an interior pick).")
    ep = prem[prem.endpoint & prem.need.notna()]
    epn = ep[~ep.mono]
    frac_unres = float((epn.need_over_SD.abs() < 1).mean()) if len(epn) else np.nan
    h_unres = bool(len(epn) and frac_unres > 0.5)
    P(f"     over all {len(ep)} endpoint picks with a finite premium: median need/SD "
      f"{np.nanmedian(ep.need_over_SD):.3f}, share |need/SD| < 1 = {float((ep.need_over_SD.abs() < 1).mean()):.1%}")
    P(f"     over the {len(epn)} endpoint picks on NON-MONOTONE dials: median need/SD "
      f"{np.nanmedian(epn.need_over_SD) if len(epn) else float('nan'):.3f}, "
      f"share |need/SD| < 1 = {frac_unres:.1%}  -> H_UNRESOLVED "
      f"{'SUPPORTED' if h_unres else 'REFUTED'}")
    P("     the queue's own three, on D_GROSS:")
    for _, r in prem[(prem.dial == "D_GROSS") & prem.chooser.isin(["C_ISSHARPE", "C_ISCAGR", "C_ISDD"])].iterrows():
        P(f"       {r.panel:<5s} {r.chooser:<11s} endpoint {r.best_endpoint} beats best interior "
          f"{r.best_interior} by need {r.need:+.6g} = {r.need_over_SD:+.3f} SD "
          f"[90% {r.paired_90lo:+.4g}, {r.paired_90hi:+.4g}]  resolvable {r.resolvable}")

    # --------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("")
    P("## RULE 8 (walk-forward) AND BOTH KEEP PATHS")
    P("   Every chooser is IS-ONLY by construction, so each of the 50 picks IS a rule-8 decision:")
    P(f"   parameters read on 2009-01..{IS_END} and scored on {IS_END}..{PIN} untouched.")
    for panel in PANELS:
        sb, lb = spy_m[panel], live_m[panel]
        P(f"   {panel} SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f}/{sb['H2']:.4f}), OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   {panel} RULES v2   full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%} "
          f"(halves {lb['H1']:.4f}/{lb['H2']:.4f}), OOS {lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        for nm, mm in (("SPY", sb), ("RULESv2", lb)):
            wfrows.append(dict(panel=panel, dial="(benchmark)", chooser=nm, arm=nm, chosen_on="n/a",
                               OOS_CAGR=mm["OOS_CAGR"], OOS_Sharpe=mm["OOS_Sharpe"],
                               OOS_MaxDD=mm["OOS_MaxDD"], full_CAGR=mm["CAGR"], full_Sharpe=mm["Sharpe"],
                               full_MaxDD=mm["MaxDD"], H1=mm["H1"], H2=mm["H2"],
                               pass_4b=False, pass_4b_oos=False, pass_4a=False))
    n_cells = len(grid)
    P(f"   LADDER BASE RATES over all {n_cells} published cells: 4b full {int(grid.pass_4b.sum())}, "
      f"4b OOS {int(grid.pass_4b_oos.sum())}, both {int((grid.pass_4b & grid.pass_4b_oos).sum())}, "
      f"4a {int(grid.pass_4a.sum())}")
    P(f"   CHOOSER PICKS over all {len(picks)} picks:       4b full {int(picks.pass_4b.sum())}, "
      f"4b OOS {int(picks.pass_4b_oos.sum())}, both {int((picks.pass_4b & picks.pass_4b_oos).sum())}, "
      f"4a {int(picks.pass_4a.sum())}")
    base_rate = float((grid.pass_4b & grid.pass_4b_oos).mean())
    pick_rate = float((picks.pass_4b & picks.pass_4b_oos).mean())
    h_nopay = pick_rate < base_rate
    P(f"   pick pass-rate {pick_rate:.1%} vs ladder base rate {base_rate:.1%}  -> H_NOPAY "
      f"{'SUPPORTED' if h_nopay else 'REFUTED'}")
    P("   PER DIAL (passing rungs / rungs, both panels; picks that pass / picks):")
    for dial in DIALS:
        gsub = grid[grid.dial == dial]
        psub = picks[picks.dial == dial]
        P(f"     {dial:<10s} ladder {int((gsub.pass_4b & gsub.pass_4b_oos).sum())}/{len(gsub)}"
          f"   picks {int((psub.pass_4b & psub.pass_4b_oos).sum())}/{len(psub)}")
    best = grid[grid.pass_4b & grid.pass_4b_oos]
    if len(best):
        bb = best.iloc[int(np.nanargmax(best.OOS_Sharpe.values))]
        P(f"   BEST cell passing 4b FULL and OOS: {bb.panel} {bb.dial} rung {bb.rung} — full "
          f"{bb.CAGR:.2%} / {bb.Sharpe:.4f} / {bb.MaxDD:.2%} (halves {bb.H1:.4f}/{bb.H2:.4f}), "
          f"OOS {bb.OOS_CAGR:.2%} / {bb.OOS_Sharpe:.4f} / {bb.OOS_MaxDD:.2%}, {bb.turn_per_yr:.2f}x/yr")
    P(f"   4a is {int(grid.pass_4a.sum())} of {n_cells} cells and {int(picks.pass_4a.sum())} of {len(picks)} picks.")
    if len(reach):
        P("   WHAT A CHOOSER WOULD HAVE TO SCORE TO REACH A 4b-PASSING RUNG (capital-relevant Q2):")
        for _, r in reach.sort_values("stat_gap", ascending=False).head(12).iterrows():
            P(f"     {r.panel:<5s} {r.dial:<10s} {r.chooser:<11s} picked {r['pick']:<6s} "
              f"(passes {r.pick_passes}); nearest passing rung {r.nearest_passing:<6s} sits "
              f"{r.stat_gap:+.6g} BELOW the pick in the chooser's own statistic, "
              f"OOS Sharpe {r.passing_OOS_Sharpe:.4f} vs picked {r.pick_OOS_Sharpe:.4f}")

    wf = pd.DataFrame(wfrows)
    dump(wf, "walkforward")

    hyp = pd.DataFrame([
        dict(hypothesis="H_IDENTITY", bar="MONO => ENDPOINT at 100% of monotone cells (an IDENTITY)",
             value=f"{mono_end}/{n_mono}", verdict="HOLDS" if h_identity else "FAILS=BUG"),
        dict(hypothesis="H_CONVERSE", bar=">=1 NON-monotone cell still picks an endpoint",
             value=f"{nonmono_end}/{len(nonmono)}", verdict="SUPPORTED" if h_converse else "REFUTED"),
        dict(hypothesis="H_GROSSFLAT", bar="IS Sharpe NOT monotone in gross; IS CAGR and IS MaxDD ARE",
             value=f"Sharpe mono={[bool(gf[(p, 'C_ISSHARPE')]['mono']) for p in PANELS]}, "
                   f"CAGR={[bool(gf[(p, 'C_ISCAGR')]['mono']) for p in PANELS]}, "
                   f"DD={[bool(gf[(p, 'C_ISDD')]['mono']) for p in PANELS]}",
             verdict="SUPPORTED" if h_grossflat else "REFUTED"),
        dict(hypothesis="H_INTERIOR", bar=">=1 (chooser, dial) cell picks the interior",
             value=f"{int((~mono.endpoint).sum())}/{len(mono)}",
             verdict="SUPPORTED" if h_interior else "REFUTED"),
        dict(hypothesis="H_UNRESOLVED", bar="|need|/SD < 1 at a majority of endpoint picks on NON-monotone dials",
             value=f"{frac_unres:.3f} over {len(epn)}", verdict="SUPPORTED" if h_unres else "REFUTED"),
        dict(hypothesis="H_NOPAY", bar="pick 4b pass-rate < ladder base rate",
             value=f"{pick_rate:.3f} vs {base_rate:.3f}", verdict="SUPPORTED" if h_nopay else "REFUTED"),
    ])
    dump(hyp, "hypotheses")
    dump(pd.DataFrame(gaterows), "gates")
    P("")
    P("## HYPOTHESES")
    P(hyp.to_string(index=False))
    P("")
    P(f"# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
