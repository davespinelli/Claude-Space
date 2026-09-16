#!/usr/bin/env python3
"""Idea 1117 (lane B, 2026-09-16)
   should-the-PROTOCOL-forbid-publishing-an-ARGMAX-on-an-H-or-CADENCE-LADDER-at-all

1116 read an infinite resolution floor on H and CADENCE at every statistic on both large
panels and concluded un-resolvability is a property of the DIAL.  The queue asks for the
obvious consequence: a PROTOCOL clause that BARS an argmax claim on such a ladder, drafted
and PRICED against the record's own committed H and cadence argmaxes.

A clause that forbids a claim is worth enacting only if the claim it forbids carries no
decision value.  So this run has two legs and the second is the one that decides:

  CENSUS  how many of the record's 32 committed argmaxes the clause bars, at every
          (CLAIM SET x BAR) point, under BOTH rung sets.
  PRICE   whether an argmax on a BARRED ladder carries any out-of-sample advantage at all.
          An honest IS-only chooser (rule 8) picks a rung on 2009-2016; OOS 2017-2026 is
          read once; the pick is scored against that ladder's FROZEN DEFAULT rung and
          against SPY and the live RULES v2 book.  If barred ladders' argmaxes buy nothing
          OOS and unbarred ladders' do, the clause is cheap and discriminating.  If barred
          ladders' argmaxes DO buy something, the clause destroys information and dies.

TUNED DIALS (2, PROTOCOL rule 4): `CLAIM SET` {CS_HCAD, CS_ALL32, CS_DECIDED} x `BAR`
{B_ALLSTAT, B_MAJ3, B_ANY} = 9 combinations, ALL published.  PANEL, LADDER and STATISTIC
are not dials.  RUNG SET {CORE, EXT} is NOT a dial either: 1118 found P(INF_FLOOR) FALLS as
rungs are added, so the clause's own trigger is rung-count dependent and BOTH levels are
reported at every point, with no result selected on either.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1118's construction: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75 (except on GROSS), min hold 126 (except on H), N=20 (except on N),
W (except on CADENCE), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, block L=63, 1000
draws, crc32 seeds, q=0.90 headline.

Standalone, deterministic, offline.  Nothing outside research/ is written or modified.
"""
from __future__ import annotations

import sys
import time
import zlib
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "should-the-PROTOCOL-forbid-publishing-an-ARGMAX-on-an-H-or-CADENCE-LADDER-at-all"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = Path(__file__).resolve().parent
PRIOR1110 = BT / "2026-09-16_what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN_C"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]                              # 1116/1110's, 9 rungs
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]    # 1116/1110's, 10 rungs
H_CORE = [21, 63, 126, 252]                                             # 1116/1110's, 4 rungs
H_EXT = [21, 42, 63, 84, 126, 168, 210, 252, 378]                       # 1118's H9, nests H4
C_CORE = ["D", "W", "M", "Q"]                                           # engine's four
C_EXT = ["D", "2D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]              # 1118's C9, nests C4

STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
SCALE = {"S_FULL": 1.0, "S_OOS": 1.0, "CAGR": 100.0, "DD": 100.0}
STATCOL = {"S_FULL": "Sharpe", "S_OOS": "OOS_Sharpe", "CAGR": "CAGR", "DD": "MaxDD"}
LADDERS = ["N", "H", "GROSS", "CADENCE"]
PANELS = ["U56", "B136"]
RUNGSETS = ["CORE", "EXT"]
DEFAULT_RUNG = {"N": "20", "H": "126", "GROSS": "0.75", "CADENCE": "W"}   # the frozen incumbent

CLAIM_SETS = ["CS_HCAD", "CS_ALL32", "CS_DECIDED"]                       # dial 1
BARS = {"B_ALLSTAT": 4, "B_MAJ3": 3, "B_ANY": 1}                         # dial 2 (min INF stats)

# chooser -> (IS column, matched OOS column, sign: +1 higher-is-better)
CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", "OOS_Sharpe", +1.0),
            "C_ISCAGR": ("IS_CAGR", "OOS_CAGR", +1.0),
            "C_ISDD": ("IS_MaxDD", "OOS_MaxDD", +1.0)}   # MaxDD is negative; higher is better

Q_HEAD, L_HEAD, BDRAWS = 0.90, 63, 1000
SEED_BASES = [11171117, 11161116, 11181118]

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

CLAUSE_TEXT = """\
PROTOCOL rule 10 (DRAFT, priced by idea 1117 — NOT enacted here; rule 6 reserves every
PROTOCOL edit to a Sunday review):

  10. **No argmax on an un-resolvable ladder.**  A backtest may not publish "the best rung
      is X" for a dial whose ladder carries an INFINITE resolution floor at EVERY statistic
      it is scored on — i.e. where, for each statistic, the largest gap between two rungs is
      itself un-resolved at the declared confidence q, so no pair on the ladder is
      separable.  Such a ladder may only be reported as a SET ("every rung on this ladder is
      indistinguishable at q=0.90"), with its floor and rung count quoted.  The rung count
      must be quoted because an INFINITE-floor flag is not comparable across ladders of
      different length (idea 1118)."""

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(base, *parts):
    return base + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------- 1082/1098/1102/1108/1118's fast runner
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
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


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


# --------------------------------------------------- 1098/1102's bootstrap, 1108's seed repair
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_exact(R, idx, nb, L, chunk=100):
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    nd = idx.shape[0]
    st = idx[:, ::L]
    cag = np.empty((R.shape[0], nd))
    shp = np.empty((R.shape[0], nd))
    n = nb * L
    for a in range(0, nd, chunk):
        s = st[a:a + chunk]
        lsum = (CS[:, s + L] - CS[:, s]).sum(axis=2)
        s1 = (CS1[:, s + L] - CS1[:, s]).sum(axis=2)
        s2 = (CS2[:, s + L] - CS2[:, s]).sum(axis=2)
        cag[:, a:a + chunk] = np.expm1(lsum * (252.0 / n))
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        shp[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return cag, shp


def boot_maxdd(R, idx, chunk=40):
    nr, _ = R.shape
    nd = idx.shape[0]
    out = np.empty((nr, nd))
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            path = np.log1p(R[j])[ix]
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
    return out


def agree_matrix(vals, boot):
    k = len(vals)
    A = np.full((k, k), np.nan)
    np.fill_diagonal(A, 1.0)
    for i, j in combinations(range(k), 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g):
            continue
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        A[i, j] = A[j, i] = float((np.sign(d) == np.sign(g)).mean()) if len(d) else np.nan
    return A


def floor_sub(vals, A, sub, q):
    """1098's floor restricted to rung subset `sub`: the smallest gap above which EVERY pair
    is resolved at q; inf when the LARGEST gap in the subset is itself un-resolved."""
    gaps, agr = [], []
    for i, j in combinations(sub, 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g) or not np.isfinite(A[i, j]):
            continue
        gaps.append(abs(g))
        agr.append(A[i, j])
    if not gaps:
        return float("inf"), 0.0
    gaps, agr = np.array(gaps), np.array(agr)
    un = agr < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    return (float(gaps[ok].min()) if ok.any() else float("inf")), largest_un


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    ra, rb = ra - ra.mean(), rb - rb.mean()
    den = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / den) if den else np.nan


def cadence_mask(idx, spec):
    """engine.rebalance_mask verbatim for D/W/M/Q (gate G7); '<k><BASE>' keeps every k-th bar
    of that base schedule.  engine.py is NOT modified."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]) if spec[:-1].isdigit() else int(spec[:-2]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


def main():
    t0 = time.time()
    P(f"# Idea 1117 (lane B, {DATE}) — should the PROTOCOL forbid publishing an ARGMAX on an")
    P("#   H or CADENCE ladder at all?  Draft the clause, then PRICE it.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIM_SETS} x BAR {list(BARS)}")
    P(f"#   = {len(CLAIM_SETS) * len(BARS)} combinations, ALL published.  PANEL, LADDER and "
      "STATISTIC are not dials.")
    P("# RUNG SET {CORE, EXT} is NOT a dial: 1118 found P(INF_FLOOR) FALLS as rungs are added,")
    P("#   so the clause's own trigger is rung-count dependent.  BOTH levels are reported at")
    P("#   every dial point and NOTHING is selected on either.")
    P(f"#   CORE  H {H_CORE}  CADENCE {C_CORE}   (1116/1110's own rungs)")
    P(f"#   EXT   H {H_EXT}  CADENCE {C_EXT}   (1118's)")
    P(f"#   N {LAD_N} and GROSS {LAD_G} are the same at both levels.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, min hold "
      f"{HOLD0}, N {N0}, cadence {FREQ0}, {COST:.0f} bps,")
    P(f"#   LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, block L={L_HEAD}, {BDRAWS} draws, "
      f"crc32 seeds, q={Q_HEAD}, {len(SEED_BASES)} seed bases.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_PREMISE      1117's premise — the record's committed census carries an")
    P("#                      INFINITE floor at 4 of 4 statistics in 4 of 4 H/CADENCE blocks")
    P("#                      ('8 of 8 cells' as the queue words it).")
    P("#   (b) H_BARS_HCAD    at B_ALLSTAT on CORE rungs the clause bars EXACTLY the four")
    P("#                      H/CADENCE blocks and no N or GROSS block.")
    P("#   (c) H_STABLE       the set of blocks the clause bars is UNCHANGED from CORE to EXT")
    P("#                      rungs — i.e. the clause cannot be escaped by adding rungs.")
    P("#   (d) H_WORTHLESS    on BARRED blocks an honest IS-only argmax buys NOTHING out of")
    P("#                      sample: median matched-statistic advantage over that ladder's")
    P("#                      FROZEN DEFAULT rung is <= 0.")
    P("#   (e) H_DISCRIMINATES on UNBARRED blocks the same chooser DOES buy something")
    P("#                      (median advantage > 0), so the clause separates the two.")
    P("#   (f) H_ISOOS_RANK   barred blocks carry a LOWER mean |Spearman(IS rung order, OOS")
    P("#                      rung order)| than unbarred blocks.")
    P("#   (g) NOT A KEEP PATH  no book is proposed; 4a/4b and rule 8 are scored at every rung")
    P("#                      because rule 4 requires it.")
    P("# DECISION RULE, declared before any number: the clause is ENACT-WORTHY only if")
    P("#   H_STABLE and H_WORTHLESS and H_DISCRIMINATES all hold.  Any one failing and the")
    P("#   clause is KILLED or PARKED, with the failing leg named.")
    P("")

    gaterows, gates = [], {}

    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> "
          f"{idx[-1].date()}, warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

    def run_cell(panel, N, H, gross, freq):
        d = panels[panel]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4, tn

    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest", value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                        {g1:.2e}   {'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]), abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="committed U56 W/H126/N=20 triple", value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy_u = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy_u, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   {'PASS' if gates['G3'] else 'FAIL'}")

    r12, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="committed U56 n=12 triple", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple       {g4:.2e}   {'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="committed B136 n=15 triple", value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN 1098/1102's committed B136 n=15 triple      {g4b:.2e}   {'PASS' if gates['G4b'] else 'FAIL'}")

    lb = {}
    for panel in PANELS:
        dp = panels[panel]
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST, freq="W")["returns"].values
        lb[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g5 = abs(lb["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD", value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   {'PASS' if gates['G5'] else 'FAIL'}")

    r12b, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism", value=g6, pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   {'PASS' if gates['G6'] else 'FAIL'}")

    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int) - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gates["G7"] = g7 == 0
    gaterows.append(dict(gate="G7", what="cadence_mask == engine.rebalance_mask on D/W/M/Q",
                         value=float(g7), pass_=gates["G7"]))
    P(f"  G7  cadence_mask == engine.rebalance_mask (D/W/M/Q)       {g7:.2e}   {'PASS' if gates['G7'] else 'FAIL'}")

    # ------------------------------------------------------------------------ BUILD EVERY BOOK
    H_ALL = sorted(set(H_CORE + H_EXT))
    RUNGS = {"N": [str(x) for x in LAD_N], "GROSS": [str(x) for x in LAD_G],
             "H": [str(x) for x in H_ALL], "CADENCE": list(C_EXT)}
    SUBSET = {("N", "CORE"): RUNGS["N"], ("N", "EXT"): RUNGS["N"],
              ("GROSS", "CORE"): RUNGS["GROSS"], ("GROSS", "EXT"): RUNGS["GROSS"],
              ("H", "CORE"): [str(x) for x in H_CORE], ("H", "EXT"): [str(x) for x in H_EXT],
              ("CADENCE", "CORE"): list(C_CORE), ("CADENCE", "EXT"): list(C_EXT)}

    def cell_params(lad, rung):
        N, H, gr, fq = N0, HOLD0, GROSS0, FREQ0
        if lad == "N":
            N = int(rung)
        elif lad == "H":
            H = int(rung)
        elif lad == "GROSS":
            gr = float(rung)
        else:
            fq = str(rung)
        return N, H, gr, fq

    grid_rows, RET = [], {}
    for panel in PANELS:
        dp = panels[panel]
        sb = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values, dp["warm"], dp["ins"], dp["oos"])
        panels[panel]["spy_m"] = sb
        for lad in LADDERS:
            for rung in RUNGS[lad]:
                N, H, gr, fq = cell_params(lad, rung)
                r, tn = run_cell(panel, N, H, gr, fq)
                RET[(panel, lad, rung)] = r
                b = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
                row = dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=gr, freq=fq,
                           in_core=bool(rung in SUBSET[(lad, "CORE")]),
                           turnover=float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0), **b)
                row.update(legs_4b(b, sb))
                row.update(legs_4b_oos(b, sb))
                row.update(legs_4a(b, lb[panel]))
                row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                grid_rows.append(row)
    G = pd.DataFrame(grid_rows)
    P(f"  built {len(G):,} books ({int(G.in_core.sum())} of them on 1110/1116's CORE rungs) "
      f"in {time.time() - t0:.0f}s")

    prior = pd.read_csv(f"{PRIOR1110}.grid.csv", dtype=str, keep_default_na=False)
    mine = G.set_index(["panel", "ladder", "rung"])
    dev = []
    for _, r in prior.iterrows():
        key = (r["panel"], r["ladder"], r["rung"])
        if key not in mine.index:
            dev.append(np.inf)
            continue
        mr = mine.loc[key]
        dev.append(max(abs(mr["CAGR"] - float(r["CAGR"])), abs(mr["Sharpe"] - float(r["Sharpe"])),
                       abs(mr["MaxDD"] - float(r["MaxDD"])), abs(mr["OOS_Sharpe"] - float(r["OOS_Sharpe"])),
                       abs(mr["turnover"] - float(r["turnover"]))))
    g8 = float(np.max(dev))
    gates["G8"] = g8 < 1e-9 and len(prior) == 54
    gaterows.append(dict(gate="G8", what=f"reproduce 1110's committed {len(prior)}-row CORE grid",
                         value=g8, pass_=gates["G8"]))
    P(f"  G8  reproduce 1110's committed {len(prior)}-row CORE grid         {g8:.2e}   {'PASS' if gates['G8'] else 'FAIL'}")

    # -------------------------------------------------------- BOOTSTRAP, per panel per ladder
    _VCACHE: dict = {}

    def vals_of(panel, lad, rungs, stat):
        key = (panel, lad, tuple(rungs), stat)
        if key not in _VCACHE:
            gi = G.set_index(["panel", "ladder", "rung"])[STATCOL[stat]]
            _VCACHE[key] = np.array([gi.loc[(panel, lad, r)] for r in rungs], float) * SCALE[stat]
        return _VCACHE[key]

    AGR = {}
    for base in SEED_BASES:
        for panel in PANELS:
            dp = panels[panel]
            for lad in LADDERS:
                rl = RUNGS[lad]
                Rw = np.array([RET[(panel, lad, r)][dp["warm"]] for r in rl])
                Ro = np.array([RET[(panel, lad, r)][dp["oos"]] for r in rl])
                rng = np.random.default_rng(seed_of(base, panel, lad, "warm"))
                iw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
                cagb, shpb = boot_exact(Rw, iw, nbw, L_HEAD)
                ddb = boot_maxdd(Rw, iw)
                rng2 = np.random.default_rng(seed_of(base, panel, lad, "oos"))
                io, nbo = block_index(rng2, Ro.shape[1], L_HEAD, BDRAWS)
                _, shpo = boot_exact(Ro, io, nbo, L_HEAD)
                bo = {"S_FULL": shpb, "S_OOS": shpo, "CAGR": cagb * 100.0, "DD": ddb * 100.0}
                for stat in STATS:
                    AGR[(base, panel, lad, stat)] = agree_matrix(vals_of(panel, lad, rl, stat), bo[stat])
        P(f"  bootstrap base {base} done at {time.time() - t0:.0f}s")

    def inf_flag(base, panel, lad, rungs, stat):
        rl = RUNGS[lad]
        sub = [rl.index(r) for r in rungs]
        v = vals_of(panel, lad, rl, stat)
        flo, _ = floor_sub(v, AGR[(base, panel, lad, stat)], sub, Q_HEAD)
        return (not np.isfinite(flo)), flo

    # ---- G9: reproduce 1110's committed argmax peaks and INF/finite floor flags on CORE rungs
    cl = pd.read_csv(f"{PRIOR1110}.clause.csv", dtype=str, keep_default_na=False)
    com = cl[(cl.clause == "AS_WRITTEN") & (cl.q == "0.9") & (cl.coarse == "")].copy()
    peak_bad = flag_bad = 0
    com_rows = []
    for _, r in com.iterrows():
        panel, lad, stat = r["panel"], r["ladder"], r["stat"]
        rungs = SUBSET[(lad, "CORE")]
        v = vals_of(panel, lad, rungs, stat)
        mine_peak = rungs[int(np.nanargmax(v))]
        ok_peak = str(mine_peak) == str(r["peak"])
        peak_bad += (not ok_peak)
        com_inf = (r["floor"] == "inf")
        my_inf, my_floor = inf_flag(SEED_BASES[0], panel, lad, rungs, stat)
        flag_bad += (com_inf != my_inf)
        com_rows.append(dict(panel=panel, ladder=lad, stat=stat, committed_peak=r["peak"],
                             my_peak=mine_peak, peak_match=ok_peak, committed_inf=com_inf,
                             my_inf=my_inf, my_floor=my_floor,
                             committed_decided=int(r["decided"]), committed_set_size=int(r["set_size"])))
    CM = pd.DataFrame(com_rows)
    gates["G9"] = (peak_bad == 0) and len(com) == 32
    gaterows.append(dict(gate="G9", what="reproduce 1110's 32 committed argmax peaks",
                         value=float(peak_bad), pass_=gates["G9"]))
    P(f"  G9  reproduce 1110's 32 committed argmax PEAKS            {peak_bad:.2e}   "
      f"{'PASS' if gates['G9'] else 'FAIL'}  (INF/finite flag mismatches: {flag_bad} of 32 — "
      "reported, NOT gated: the flag is a redraw quantity)")
    dump(CM, "committed")

    g10 = float(min(np.nanmax(vals_of(p, l, RUNGS[l], s)) - np.nanmin(vals_of(p, l, RUNGS[l], s))
                    for p in PANELS for l in LADDERS for s in STATS))
    gates["G10"] = g10 > 0
    gaterows.append(dict(gate="G10", what="every ladder x statistic live", value=g10, pass_=gates["G10"]))
    P(f"  G10 every ladder x statistic is LIVE (min spread)         {g10:.2e}   {'PASS' if gates['G10'] else 'FAIL'}")
    P(f"  GATES: {sum(gates.values())} of {len(gates)} PASS")
    dump(pd.DataFrame(gaterows), "gates")
    P("")

    # ---------------------------------------------------------------------- THE CLAUSE, DRAFTED
    P("## THE CLAUSE, DRAFTED (not enacted — rule 6 reserves PROTOCOL edits to a Sunday review)")
    for line in CLAUSE_TEXT.split("\n"):
        P("  " + line)
    P("")

    # ------------------------------------------------------------------ THE TRIGGER, PER BLOCK
    P("## THE TRIGGER — INFINITE-FLOOR count (of 4 statistics) per (panel, ladder) BLOCK")
    trig_rows = []
    for base in SEED_BASES:
        for rs in RUNGSETS:
            for panel in PANELS:
                for lad in LADDERS:
                    rungs = SUBSET[(lad, rs)]
                    flags = {s: inf_flag(base, panel, lad, rungs, s)[0] for s in STATS}
                    trig_rows.append(dict(base=base, rung_set=rs, panel=panel, ladder=lad,
                                          k=len(rungs), inf_count=int(sum(flags.values())),
                                          **{f"inf_{s}": bool(flags[s]) for s in STATS}))
    TR = pd.DataFrame(trig_rows)
    dump(TR, "trigger")
    head_tr = TR[TR.base == SEED_BASES[0]]
    P(head_tr.pivot_table(index=["panel", "ladder"], columns="rung_set", values=["k", "inf_count"]).to_string())
    P("")
    P(f"  over all {len(SEED_BASES)} seed bases — inf_count min/median/max per block:")
    agg = TR.groupby(["rung_set", "panel", "ladder"])["inf_count"].agg(["min", "median", "max"]).reset_index()
    P(agg.to_string(index=False))
    P("")

    def barred(base, rs, panel, lad, bar):
        row = TR[(TR.base == base) & (TR.rung_set == rs) & (TR.panel == panel) & (TR.ladder == lad)]
        return int(row["inf_count"].iloc[0]) >= BARS[bar]

    # ------------------------------------------------------------- CENSUS: 9 DIAL POINTS x 2 RS
    P("## THE CENSUS — how many of the record's committed argmaxes the clause BARS")
    CMi = CM.set_index(["panel", "ladder", "stat"])

    def claim_cells(cs):
        cells = [(p, l, s) for p in PANELS for l in LADDERS for s in STATS]
        if cs == "CS_HCAD":
            return [c for c in cells if c[1] in ("H", "CADENCE")]
        if cs == "CS_DECIDED":
            return [c for c in cells if int(CMi.loc[c, "committed_set_size"]) == 1]
        return cells

    cen_rows = []
    for cs in CLAIM_SETS:
        cells = claim_cells(cs)
        for bar in BARS:
            for rs in RUNGSETS:
                for base in SEED_BASES:
                    nb = sum(barred(base, rs, p, l, bar) for (p, l, s) in cells)
                    cen_rows.append(dict(claim_set=cs, bar=bar, rung_set=rs, base=base,
                                         n_claims=len(cells), n_barred=nb,
                                         share=nb / len(cells) if cells else np.nan))
    CE = pd.DataFrame(cen_rows)
    dump(CE, "census")
    piv = CE[CE.base == SEED_BASES[0]].pivot_table(index=["claim_set", "bar"], columns="rung_set",
                                                   values=["n_claims", "n_barred"])
    P(f"  headline base {SEED_BASES[0]}:")
    P(piv.to_string())
    P("")
    P(f"  median over {len(SEED_BASES)} seed bases:")
    P(CE.pivot_table(index=["claim_set", "bar"], columns="rung_set", values="n_barred",
                     aggfunc="median").to_string())
    P("")

    # ------------------------------------------------- THE PRICE LEG: RULE 8 WALK-FORWARD
    P("## THE PRICE LEG — RULE 8 WALK-FORWARD.  Rung chosen on IS 2009-2016 ALONE; OOS")
    P("##   2017-2026 read ONCE.  Scored against that ladder's FROZEN DEFAULT rung, against")
    P("##   SPY and against the live RULES v2 book.")
    gi = G.set_index(["panel", "ladder", "rung"])
    wf = []
    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        for lad in LADDERS:
            for rs in RUNGSETS:
                rungs = SUBSET[(lad, rs)]
                sub = G[(G.panel == panel) & (G.ladder == lad) & (G.rung.isin(rungs))]
                dref = gi.loc[(panel, lad, DEFAULT_RUNG[lad])]
                for ch, (iscol, ooscol, sign) in CHOOSERS.items():
                    pick = sub.loc[sub[iscol].idxmax()]
                    best = sub.loc[sub[ooscol].idxmax()]
                    fullbest = sub.loc[sub[STATCOL["S_FULL"]].idxmax()]
                    wf.append(dict(
                        panel=panel, ladder=lad, rung_set=rs, chooser=ch, k=len(rungs),
                        pick=pick["rung"], default=DEFAULT_RUNG[lad],
                        full_argmax=fullbest["rung"],
                        pick_is_default=bool(pick["rung"] == DEFAULT_RUNG[lad]),
                        pick_is_full_argmax=bool(pick["rung"] == fullbest["rung"]),
                        CAGR=pick["CAGR"], Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"],
                        H1=pick["H1"], H2=pick["H2"],
                        OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                        OOS_MaxDD=pick["OOS_MaxDD"],
                        adv_matched=sign * float(pick[ooscol] - dref[ooscol]),
                        adv_oos_sharpe=float(pick["OOS_Sharpe"] - dref["OOS_Sharpe"]),
                        regret=float(sign * (best[ooscol] - pick[ooscol])),
                        def_OOS_Sharpe=float(dref["OOS_Sharpe"]),
                        pass_4b_full=bool(pick["pass_4b_full"]), pass_4b_oos=bool(pick["pass_4b_oos"]),
                        pass_4a=bool(pick["pass_4a"]),
                        spy_OOS_Sharpe=sb["OOS_Sharpe"], live_OOS_Sharpe=lbm["OOS_Sharpe"]))
    WF = pd.DataFrame(wf)
    # attach barred status at the headline base under each bar
    for bar in BARS:
        WF[f"barred_{bar}"] = [barred(SEED_BASES[0], r.rung_set, r.panel, r.ladder, bar)
                               for r in WF.itertuples()]
    dump(WF, "walkforward")
    dump(G, "grid")

    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        P(f"  {panel} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}   "
          f"OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2  full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:.2%}   "
          f"OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:.2%}")
    P(f"  IS picks: {len(WF)} — 4b full {int(WF.pass_4b_full.sum())}, 4b OOS "
      f"{int(WF.pass_4b_oos.sum())}, 4a {int(WF.pass_4a.sum())}, median OOS Sharpe "
      f"{WF.OOS_Sharpe.median():.4f}, median regret {WF.regret.median():+.4f}")
    P(f"  whole grid {len(G)} rungs: 4b full {int(G.pass_4b_full.sum())}, 4b OOS "
      f"{int(G.pass_4b_oos.sum())}, 4a {int(G.pass_4a.sum())}; on rungs outside 1110's CORE "
      f"{int(G[~G.in_core].pass_4b_full.sum())} of {int((~G.in_core).sum())}")
    P("")
    P("  DOES AN ARGMAX BUY ANYTHING OUT OF SAMPLE?  matched-statistic advantage of the")
    P("  IS-chosen rung over that ladder's FROZEN DEFAULT rung, split by the clause's verdict:")
    for bar in BARS:
        for rs in RUNGSETS:
            w = WF[WF.rung_set == rs]
            bb, ub = w[w[f"barred_{bar}"]], w[~w[f"barred_{bar}"]]
            def fmt(x):
                return (f"n={len(x):2d} median adv {x.adv_matched.median():+.4f} "
                        f"mean {x.adv_matched.mean():+.4f} wins {int((x.adv_matched > 0).sum())}/{len(x)} "
                        f"median OOS-Sharpe adv {x.adv_oos_sharpe.median():+.4f}") if len(x) else "n= 0"
            P(f"    {bar:10s} {rs:4s}  BARRED   {fmt(bb)}")
            P(f"    {bar:10s} {rs:4s}  UNBARRED {fmt(ub)}")
    P("")
    P("  by ladder (both rung sets pooled):")
    bl = WF.groupby(["ladder", "rung_set"]).agg(
        n=("adv_matched", "size"), med_adv=("adv_matched", "median"),
        wins=("adv_matched", lambda x: int((x > 0).sum())),
        med_oos_sharpe=("OOS_Sharpe", "median"), med_regret=("regret", "median"),
        picks_default=("pick_is_default", "sum")).reset_index()
    P(bl.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  THE ZEROES ARE NOT ALL THE SAME ZERO — the honest chooser sometimes RE-PICKS the")
    P("  frozen default rung, which is an advantage of exactly 0 by construction.  Split:")
    ndp = WF[~WF.pick_is_default]
    dp_ = WF[WF.pick_is_default]
    P(f"    pick == the frozen DEFAULT rung: {len(dp_)} of {len(WF)} (advantage 0 by construction)")
    P(f"    pick MOVED off the default:      n={len(ndp)}  median matched advantage "
      f"{ndp.adv_matched.median():+.4f}  mean {ndp.adv_matched.mean():+.4f}  "
      f"wins {int((ndp.adv_matched > 0).sum())}/{len(ndp)}  median OOS-Sharpe advantage "
      f"{ndp.adv_oos_sharpe.median():+.4f}")
    for bar in BARS:
        for rs in RUNGSETS:
            x = ndp[(ndp.rung_set == rs)]
            b2, u2 = x[x[f"barred_{bar}"]], x[~x[f"barred_{bar}"]]
            def f2(y):
                return (f"n={len(y):2d} median adv {y.adv_matched.median():+.4f} "
                        f"wins {int((y.adv_matched > 0).sum())}/{len(y)}") if len(y) else "n= 0"
            P(f"      {bar:10s} {rs:4s}  BARRED   {f2(b2)}    UNBARRED {f2(u2)}")
    P(f"    pick == the FULL-SAMPLE argmax (what the record publishes): "
      f"{int(WF.pick_is_full_argmax.sum())} of {len(WF)}")
    P("")
    P("  EVERY IS PICK THAT CLEARS 4b (full), with its OOS triple:")
    pw = WF[WF.pass_4b_full]
    if len(pw):
        P(pw[["panel", "ladder", "rung_set", "chooser", "pick", "pick_is_default", "CAGR",
              "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("    none")
    P("")

    # ---------------------------------------------- IS vs OOS RANK INFORMATION, PER BLOCK
    P("## DOES A BARRED LADDER CARRY ANY OOS SELECTION INFORMATION?  Spearman(IS rung order,")
    P("##   OOS rung order) per (panel, ladder, statistic) block")
    rk_rows = []
    for panel in PANELS:
        for lad in LADDERS:
            for rs in RUNGSETS:
                rungs = SUBSET[(lad, rs)]
                sub = gi.loc[[(panel, lad, r) for r in rungs]]
                for ch, (iscol, ooscol, sign) in CHOOSERS.items():
                    rk_rows.append(dict(panel=panel, ladder=lad, rung_set=rs, chooser=ch,
                                        rho=spearman(sub[iscol].values, sub[ooscol].values)))
    RK = pd.DataFrame(rk_rows)
    for bar in BARS:
        RK[f"barred_{bar}"] = [barred(SEED_BASES[0], r.rung_set, r.panel, r.ladder, bar)
                               for r in RK.itertuples()]
    dump(RK, "rankinfo")
    P(RK.pivot_table(index=["panel", "ladder"], columns=["rung_set"], values="rho").to_string(
        float_format=lambda x: f"{x:+.4f}"))
    bar0 = "B_ALLSTAT"
    rb, ru = RK[RK[f"barred_{bar0}"]], RK[~RK[f"barred_{bar0}"]]
    P(f"  mean |rho| BARRED ({bar0}) {rb.rho.abs().mean():.4f} (n={len(rb)})   "
      f"UNBARRED {ru.rho.abs().mean():.4f} (n={len(ru)})")
    P("")

    # ----------------------------------------------------------------------------- HYPOTHESES
    core0 = TR[(TR.base == SEED_BASES[0]) & (TR.rung_set == "CORE")].set_index(["panel", "ladder"])
    ext0 = TR[(TR.base == SEED_BASES[0]) & (TR.rung_set == "EXT")].set_index(["panel", "ladder"])
    hcad_blocks = [(p, l) for p in PANELS for l in ("H", "CADENCE")]
    ng_blocks = [(p, l) for p in PANELS for l in ("N", "GROSS")]

    com_hcad_inf = int(CM[(CM.ladder.isin(["H", "CADENCE"])) & (CM.committed_inf)].shape[0])
    premise_ok = com_hcad_inf == 16

    bars_hcad = (all(int(core0.loc[b, "inf_count"]) >= 4 for b in hcad_blocks)
                 and all(int(core0.loc[b, "inf_count"]) < 4 for b in ng_blocks))
    barred_core = {b for b in core0.index if int(core0.loc[b, "inf_count"]) >= 4}
    barred_ext = {b for b in ext0.index if int(ext0.loc[b, "inf_count"]) >= 4}
    stable = barred_core == barred_ext

    w = WF
    bb_all, ub_all = w[w["barred_B_ALLSTAT"]], w[~w["barred_B_ALLSTAT"]]
    worthless = bool(len(bb_all) and bb_all.adv_matched.median() <= 0)
    discrim = bool(len(ub_all) and ub_all.adv_matched.median() > 0)
    rank_ok = bool(len(rb) and len(ru) and rb.rho.abs().mean() < ru.rho.abs().mean())

    H = {
        "H_PREMISE": (premise_ok,
                      f"1110's committed census carries an INFINITE floor at {com_hcad_inf} of 16 "
                      f"H/CADENCE cells (the queue's premise says 16 of 16 / '8 of 8 cells')"),
        "H_BARS_HCAD": (bars_hcad,
                        "CORE blocks at inf_count>=4: " + ", ".join(
                            f"{p}/{l} {int(core0.loc[(p, l), 'inf_count'])}"
                            for p in PANELS for l in LADDERS)),
        "H_STABLE": (stable, f"barred CORE {sorted(barred_core)} vs barred EXT {sorted(barred_ext)}"),
        "H_WORTHLESS": (worthless,
                        f"BARRED median matched advantage over the default rung "
                        f"{bb_all.adv_matched.median():+.4f} (n={len(bb_all)}, "
                        f"{int((bb_all.adv_matched > 0).sum())} wins)"),
        "H_DISCRIMINATES": (discrim,
                            f"UNBARRED median matched advantage {ub_all.adv_matched.median():+.4f} "
                            f"(n={len(ub_all)}, {int((ub_all.adv_matched > 0).sum())} wins)"),
        "H_ISOOS_RANK": (rank_ok, f"mean |rho| barred {rb.rho.abs().mean():.4f} vs unbarred "
                                  f"{ru.rho.abs().mean():.4f}"),
    }
    P("## HYPOTHESES, declared before any number")
    for k, (ok, why) in H.items():
        P(f"  {'SUPPORTED' if ok else 'REFUTED  '}  {k:16s} {why}")
    P(f"  {sum(1 for v in H.values() if v[0])} of {len(H)} SUPPORTED")
    dump(pd.DataFrame([dict(hypothesis=k, supported=v[0], evidence=v[1]) for k, v in H.items()]),
         "hypotheses")
    P("")

    enact = stable and worthless and discrim
    P("## THE VERDICT ON THE CLAUSE (decision rule declared before any number)")
    P(f"  H_STABLE {stable}   H_WORTHLESS {worthless}   H_DISCRIMINATES {discrim}")
    P(f"  => the clause as written is {'ENACT-WORTHY' if enact else 'NOT ENACT-WORTHY'}")
    if not enact:
        fail = [k for k, v in (("H_STABLE", stable), ("H_WORTHLESS", worthless),
                               ("H_DISCRIMINATES", discrim)) if not v]
        P(f"  failing leg(s): {', '.join(fail)}")
    P("")

    P(f"\n# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
