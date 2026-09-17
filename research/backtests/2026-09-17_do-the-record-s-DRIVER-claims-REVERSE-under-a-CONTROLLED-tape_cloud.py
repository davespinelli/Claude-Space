#!/usr/bin/env python3
"""Idea 1171 (cloud lane, 2026-09-17) — do the record's DRIVER claims REVERSE under a
CONTROLLED TAPE, as 1164's did?

Idea 1164 found its strongest population driver (D_TIES, cross-book rho -0.533, sign-stable
at 3 of 3 panels and under a partial control) carries the OPPOSITE sign on a tape where that
driver alone is varied (+1.0000).  A cross-book rank correlation is not a mechanism.  The
queue asks for (a) a HARVEST of the record's committed driver / carrier / explanation claims
that rest on a cross-book correlation alone, and (b) a test of the CHEAPEST of them against
a ONE-FACTOR SYNTHETIC TAPE.

WHAT A "CONTROLLED TAPE" MEANS HERE, said plainly.  A cross-book rho is taken over books
that differ in the dial AND in everything the dial drags with it — which names get picked,
how correlated they are, which episode the drawdown lands in.  A controlled tape removes the
confound at the source: every column is EXCHANGEABLE by construction, so no name is better
than another, and varying the dial alone leaves nothing else to move.  If a driver claim is
a mechanism it must keep its sign there; if it only survives on the real panel it is a
statement about SELECTION, not about the dial.

THE SIX DRIVERS ARE PRICE-NATIVE AND NAMED BY THE RECORD, not invented here:
  D_TURN   annual turnover  -> c*        (1094's rho -0.65; 1151 reproduced -0.6484)
  D_N      book size N      -> |MaxDD|   (the diversification claim behind every n ladder)
  D_N_SH   book size N      -> Sharpe    (1082/1086/1093's EDGE ladder premise)
  D_HOLD   min hold H       -> turnover  (the rebate 931 priced from the cadence side)
  D_GROSS  gross            -> |MaxDD|   (near-mechanical — the CALIBRATION case)
  D_CAD    cadence W vs M   -> turnover  (931's W->M rebate)
D_GROSS is the CALIBRATION case: more exposure must deepen the drawdown on any tape, and
G5 checks that it does on the real gross ladder.  A control that reverses it is broken, not
a finding.  G5b reports a correction this run found and does not hide: 1162's weight
identity `W(g) == g*W(1)` does NOT carry to the compounded RETURN path when gross < 1
(max |r(0.75) - 2.5*r(0.30)| = 3.33e-03), because the cash sleeve compounds differently at
each gross — so D_GROSS is near-mechanical, not an identity, and is treated as such.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4, and the queue names both):
  CLAIM SET  {C_RHOONLY, C_CONTROLLED, C_ALL}
  TAPE       {T_IID, T_BLOCK, T_FACTOR}
= 9 cells, EVERY ONE PUBLISHED in `.grid.csv`.
NOT dials, all reported at every value: PANEL {U56, B136, SMALL}; the book population
N x H x cadence plus a gross ladder = 88 per panel, 264 real books and 2,376 synthetic;
the six drivers; the four rule-8 choosers; SEED (three run at every controlled cell, spread
published).  Frozen at 1082/1094/1098/1102/1110/1149/1151/1159/1161/1164's construction:
CAND20 legs [(21,252),(0,126),(0,63)], max_vol 0.60, cost 10 bps (rule 2), LAG 1, warm-up
260, IS end 2016-12-31, zero cash, DD cap 0.60, CAGR floor 0.70.

SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current
constituents of a sub-$2B screen LESS every ticker with max_1d_move >= 1.0 in
data/small_meta.csv, dropped before anything else is computed.  Every LEVEL is optimistic
and the bias does NOT cancel out of the 4b legs.  It very largely DOES cancel out of every
rho here, which is a ranking of one construction against itself on one tape.

Writes: .gates.csv .harvest.csv .grid.csv .drivers.csv .books.csv .walkforward.csv
        .console.txt
Deterministic (all draws seeded), standalone, no network.  Does not modify RULES.md /
PROTOCOL.md / scan.py / bot.py / baseline.py / engine.py.
"""
import sys, re, glob, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "do-the-record-s-DRIVER-claims-REVERSE-under-a-CONTROLLED-tape"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
LOG = []

LAG, WARMUP = 1, 260
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, COST0, MAXVOL0, N0, H0 = 0.75, 10.0, 0.60, 20, 126
LEGS = [(21, 252), (0, 126), (0, 63)]
START = "2008-01-01"
SEEDS = [20260917, 20260918, 20260919]
BLOCK_L = 63
CSTAR_HI, CSTAR_TOL = 300.0, 1e-3

N_LADDER = [5, 8, 10, 12, 15, 20, 25, 30, 40]
H_LADDER = [21, 63, 126, 252]
G_LADDER = [0.30, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.00]
CADENCES = ["W", "M"]

CLAIMSETS = ["C_RHOONLY", "C_CONTROLLED", "C_ALL"]
TAPES = ["T_IID", "T_BLOCK", "T_FACTOR"]

# the six drivers: (dial column, outcome column, want-sign the RECORD's claim asserts)
DRIVERS = {
    "D_TURN":  ("ann_turnover", "cstar", -1, "turnover -> c* (1094 rho -0.65)"),
    "D_N":     ("N", "absMaxDD", -1, "book size -> |MaxDD| (diversification)"),
    "D_N_SH":  ("N", "Sharpe", -1, "book size -> Sharpe (the EDGE ladder premise)"),
    "D_HOLD":  ("H", "ann_turnover", -1, "min hold -> turnover"),
    "D_GROSS": ("gross", "absMaxDD", +1, "gross -> |MaxDD| (an IDENTITY; CALIBRATION case)"),
    "D_CAD":   ("cad_num", "ann_turnover", -1, "cadence W(1)->M(0) -> turnover (931's rebate)"),
}
# which driver TOPIC a harvested sentence is about (for the claim-set dial)
TOPIC = {
    "D_TURN": re.compile(r"\bturnover\b|\bc\*|\bbreakeven\b", re.I),
    "D_N": re.compile(r"\bN\s*=|\bbook size\b|\bn ladder\b|\bnames\b", re.I),
    "D_N_SH": re.compile(r"\bN\s*=|\bn ladder\b|\bEDGE\b", re.I),
    "D_HOLD": re.compile(r"\bmin(imum)? hold\b|\bH\s*=|\bhold ladder\b", re.I),
    "D_GROSS": re.compile(r"\bgross\b|\bde-gross", re.I),
    "D_CAD": re.compile(r"\bcadence\b|\bweekly\b|\bmonthly\b|W->M|W-\>M", re.I),
}
DRIVE_RE = re.compile(r"\b(drive[sn]?|driver|carrie[sd]|carrier|explain(s|ed)?|"
                      r"account(s|ed)? for|predict(s|ed)?|order(s|ed)? |is a property of|"
                      r"is driven by)\b", re.I)
RHO_RE = re.compile(r"\b(rho|spearman|rank correlation|correlation|corr\b|kendall)\b", re.I)
CTRL_RE = re.compile(r"\b(control|controlled|intervention|one-factor|partial|held fixed|"
                     r"ceteris|synthetic|matched|counterfactual|ablat)", re.I)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------- 1082/../1161's fast runner and book, VERBATIM
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


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (comp * (0.5 + 0.5 * above.astype(float))).values, above.values, vol20.values


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


def prep(px):
    idx = px.index
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    sc, above, vol20 = mech(px)
    return dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                warm=warm, ins=ins, oos=oos, sc=sc, above=above, vol20=vol20,
                spy=px["SPY"].pct_change().fillna(0.0).values,
                mk={f: rebalance_mask(idx, f).values for f in CADENCES})


def run_gt(d, N, H, freq, gross=GROSS0, maxvol=MAXVOL0):
    mk = d["mk"][freq]
    mkl = np.roll(mk, LAG)
    mkl[:LAG] = False
    reb = np.flatnonzero(mk)
    el = d["above"] & (d["vol20"] < maxvol)
    W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    return nrun(d["rets"], Wl, mkl)


def net(g, tn, c):
    return g - tn * c / 1e4


def blocks_m(r, d):
    rr = r[d["warm"]]
    c, s, dd = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[d["oos"]])
    ic, is_, idd = fmet(r[d["ins"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return dict(L_H1=b["H1"] > sb["H1"], L_H2=b["H2"] > sb["H2"],
                L_OOS=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                L_DD=abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"]),
                L_CAGR=b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])


def legs_4b_oos(b, sb):
    return dict(O_S=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                O_DD=abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"]),
                O_CAGR=b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])


def legs_4a(b, lbm):
    return dict(A_H1=b["H1"] > lbm["H1"], A_H2=b["H2"] > lbm["H2"],
                A_DD=b["MaxDD"] >= lbm["MaxDD"])


def cstar(g, tn, d, sb, lo=0.0, hi=CSTAR_HI):
    """1151's c*: the cost at which the book's first 4b leg fails.  Pure arithmetic on
    (g, tn) — r(c) = g - tn*c/1e4 is affine in c (1151 G1, 1.39e-17)."""
    ok = lambda c: all(legs_4b(blocks_m(net(g, tn, c), d), sb).values())  # noqa: E731
    if not ok(lo):
        return 0.0
    if ok(hi):
        return hi
    a, b = lo, hi
    while b - a > CSTAR_TOL:
        m = 0.5 * (a + b)
        if ok(m):
            a = m
        else:
            b = m
    return 0.5 * (a + b)


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    rx, ry = pd.Series(x[ok]).rank().values, pd.Series(y[ok]).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan          # DEGENERATE, never 0.0 — a tied column is not "no relation"
    return float(np.corrcoef(rx, ry)[0, 1])


# ------------------------------------------------------------------ THE CONTROLLED TAPES
def synth(px, kind, seed):
    """A tape on which every column is EXCHANGEABLE by construction, so varying one dial
    leaves NOTHING ELSE to move.  Same shape, same index, same SPY benchmark column built
    from the synthetic names themselves (never the real one — that would smuggle the real
    tape's episode structure back in through the 4b benchmark)."""
    rng = np.random.default_rng(seed)
    cols = [c for c in px.columns if c != "SPY"]
    R = px[cols].pct_change().values
    T, K = R.shape
    pooled = R[np.isfinite(R)]
    mu, sd = float(np.mean(pooled)), float(np.std(pooled))
    if kind == "T_IID":
        X = rng.normal(mu, sd, size=(T, K))
    elif kind == "T_BLOCK":
        # moving-block resample of the panel's OWN returns, INDEPENDENTLY per column:
        # keeps every name's serial structure and marginal, destroys cross-sectional
        # structure and every name's identity.
        src = np.where(np.isfinite(R), R, 0.0)
        nb = int(np.ceil(T / BLOCK_L))
        ar = np.arange(BLOCK_L)
        X = np.empty((T, K))
        for k in range(K):
            col = rng.integers(0, K)
            st = rng.integers(0, T - BLOCK_L + 1, size=nb)
            X[:, k] = src[(st[:, None] + ar[None, :]).ravel()[:T], col]
    else:  # T_FACTOR — one common factor plus exchangeable idiosyncratic noise
        src = np.where(np.isfinite(R), R, 0.0)
        fac = src.mean(axis=1)
        nb = int(np.ceil(T / BLOCK_L))
        ar = np.arange(BLOCK_L)
        st = rng.integers(0, T - BLOCK_L + 1, size=nb)
        f = fac[(st[:, None] + ar[None, :]).ravel()[:T]]
        idio = float(np.median(np.nanstd(R - fac[:, None], axis=0)))
        X = f[:, None] + rng.normal(0.0, idio, size=(T, K))
    X[0] = 0.0
    prices = pd.DataFrame(100.0 * np.cumprod(1.0 + X, axis=0), index=px.index, columns=cols)
    prices["SPY"] = 100.0 * np.cumprod(1.0 + X.mean(axis=1))   # synthetic benchmark
    return prices


def main():
    t_start = time.time()
    P("=" * 100)
    P(f"IDEA 1171 (cloud) — {SLUG}")
    P("=" * 100)
    P("TWO TUNED PARAMETERS (rule 4): CLAIM SET {C_RHOONLY,C_CONTROLLED,C_ALL} x")
    P("TAPE {T_IID,T_BLOCK,T_FACTOR} = 9 cells, all published in .grid.csv.")
    P("PANEL, the 90-book population, the six drivers, SEED and the four rule-8 choosers")
    P("are NOT dials — all values reported everywhere.")
    P("")

    # --------------------------------------------------------- (A) THE HARVEST
    P("-" * 100)
    P("(A) THE HARVEST — the record's committed DRIVER claims that rest on a rho ALONE")
    P("-" * 100)
    files = ["research/LEADERBOARD.md", "research/CHANGELOG.md"] + \
        sorted(glob.glob("research/backtests/*.result.md"))
    hrows = []
    nsent = 0
    for f in files:
        txt = (ROOT / f).read_text(errors="replace")
        for ln, line in enumerate(txt.split("\n"), 1):
            for s in re.split(r"(?<=[.;])\s+", line):
                if len(s) < 40:
                    continue
                nsent += 1
                if not (DRIVE_RE.search(s) and RHO_RE.search(s)):
                    continue
                ctrl = bool(CTRL_RE.search(s))
                hrows.append(dict(
                    src=f, line=ln, has_control=ctrl,
                    claimset="C_CONTROLLED" if ctrl else "C_RHOONLY",
                    **{f"topic_{k}": bool(v.search(s)) for k, v in TOPIC.items()},
                    n_topics=sum(bool(v.search(s)) for v in TOPIC.values()),
                    text=s[:600]))
    hv = pd.DataFrame(hrows)
    dump(hv, "harvest")
    P(f"  {len(files)} committed files, {nsent:,} sentences scanned")
    P(f"  DRIVER VERB + a CORRELATION token: {len(hv):,} sentences")
    P(f"  of which ALSO name a CONTROL:      {int(hv.has_control.sum()):,} "
      f"({hv.has_control.mean():.4f})")
    P(f"  RESTING ON A CROSS-BOOK rho ALONE: {int((~hv.has_control).sum()):,} "
      f"({(~hv.has_control).mean():.4f})   <- 1171's population, exactly")
    P("  by driver TOPIC (a sentence may touch more than one):")
    for k in DRIVERS:
        q = hv[hv[f"topic_{k}"]]
        P(f"    {k:<9} {len(q):>5} sentences, {int((~q.has_control).sum()):>5} rho-only "
          f"({(~q.has_control).mean() if len(q) else float('nan'):.4f})")
    P(f"  sentences touching NONE of the six priced topics: "
      f"{int((hv.n_topics == 0).sum())} of {len(hv)} — these are OUT OF SCOPE for arm (B)")
    P("")

    # --------------------------------------------------------- PANELS
    P("-" * 100)
    P("PANELS")
    P("-" * 100)
    panels = {}
    panels["U56"] = load_universe(start=START)
    panels["B136"] = load_universe(start=START, broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    sm = load_universe(small=True)
    dropped = [c for c in sm.columns if c in bad]
    panels["SMALL"] = sm.drop(columns=dropped)
    for pn, px in panels.items():
        P(f"  {pn:<6} {px.shape[1]:>4} cols  {px.index[0].date()}..{px.index[-1].date()}  "
          f"{len(px):,} rows")
    P(f"  SMALL dropped {len(dropped)} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")
    P("  SURVIVORSHIP (rule 9): all three are CURRENT-CONSTITUENT lists; every LEVEL is")
    P("  optimistic.  It very largely cancels out of the rhos, which rank one construction")
    P("  against itself on one tape.")
    P("")
    D, BENCH = {}, {}
    for pn, px in panels.items():
        d = prep(px)
        D[pn] = d
        sb = blocks_m(d["spy"], d)
        lbm = blocks_m(backtest(px, rules_v2_weights(px), cost_bps=COST0, freq="W")["returns"]
                       .reindex(px.index).fillna(0.0).values, d)
        BENCH[pn] = dict(spy=sb, live=lbm)
        P(f"  {pn:<6} SPY   {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%}"
          f"  halves {sb['H1']:.4f}/{sb['H2']:.4f}"
          f"  | OOS {sb['OOS_CAGR']:7.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:7.2%}")
        P(f"  {pn:<6} LIVE  {lbm['CAGR']:7.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:7.2%}"
          f"  halves {lbm['H1']:.4f}/{lbm['H2']:.4f}"
          f"  | OOS {lbm['OOS_CAGR']:7.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:7.2%}")
    P("")

    # --------------------------------------------------------- THE BOOK POPULATION
    def population(d, sb, lbm, want_cstar=True):
        """88 books: N x H x cadence at gross 0.75, plus a gross ladder at N=20/H=126."""
        rows, GT = [], {}
        specs = [("NH", N, H, f, GROSS0) for f in CADENCES for N in N_LADDER for H in H_LADDER]
        specs += [("G", N0, H0, f, g) for f in CADENCES for g in G_LADDER]
        for arm, N, H, f, g in specs:
            key = (arm, N, H, f, g)
            gg, tt = run_gt(d, N, H, f, gross=g)
            GT[key] = (gg, tt)
            m = blocks_m(net(gg, tt, COST0), d)
            l4b, l4bo, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lbm)
            rows.append(dict(arm=arm, N=N, H=H, cadence=f, gross=g, cad_num=1.0 if f == "W" else 0.0,
                             ann_turnover=float(tt.sum() / (len(tt) / 252.0)),
                             absMaxDD=abs(m["MaxDD"]),
                             cstar=(cstar(gg, tt, d, sb) if want_cstar else np.nan),
                             **{k: float(v) for k, v in m.items()},
                             pass_4b=bool(all(l4b.values())),
                             pass_4b_oos=bool(all(l4bo.values())),
                             pass_4a=bool(all(l4a.values()))))
        return pd.DataFrame(rows), GT

    P("-" * 100)
    P("THE REAL BOOK POPULATION — 3 panels x (72 N-H books + 16 gross books) = 264")
    P("-" * 100)
    t0 = time.time()
    POP, GTS = {}, {}
    for pn in ("U56", "B136", "SMALL"):
        POP[pn], GTS[pn] = population(D[pn], BENCH[pn]["spy"], BENCH[pn]["live"])
        P(f"  {pn:<6} {len(POP[pn])} books")
    t_real = time.time() - t0
    allbooks = pd.concat([POP[pn].assign(panel=pn, tape="REAL", seed=0)
                          for pn in POP], ignore_index=True)
    dump(allbooks, "books")
    P(f"  {len(allbooks)} real books in {t_real:.1f}s")
    P("  BASE RATES at 10 bps:")
    for pn in ("U56", "B136", "SMALL"):
        s = POP[pn]
        P(f"    {pn:<6} 4b full {int(s.pass_4b.sum()):>3}/{len(s)}   "
          f"4b OOS {int(s.pass_4b_oos.sum()):>3}/{len(s)}   4a {int(s.pass_4a.sum()):>3}/{len(s)}")
    P("")

    # --------------------------------------------------------- GATES
    P("-" * 100)
    P("GATES")
    P("-" * 100)
    gates = []

    def gate(name, what, value, ok):
        gates.append(dict(gate=name, what=what, value=value, pass_=bool(ok)))
        P(f"  {name:<5} {'PASS' if ok else 'FAIL'}  {what}  = {value}")

    d0 = D["U56"]
    g0, tn0 = GTS["U56"][("NH", 20, 126, "W", GROSS0)]
    m_inc = blocks_m(net(g0, tn0, COST0), d0)
    P(f"  incumbent U56 W/H126/N=20/gross 0.75 @10bps: CAGR {m_inc['CAGR']:.6f} "
      f"Sharpe {m_inc['Sharpe']:.6f} MaxDD {m_inc['MaxDD']:.6f}")
    for nm, got, want in (("G1", m_inc["CAGR"], 0.155787), ("G2", m_inc["Sharpe"], 1.139701),
                          ("G3", m_inc["MaxDD"], -0.191276)):
        gate(nm, f"incumbent anchor vs committed {want}", round(float(got), 6),
             abs(got - want) <= 5e-3)
    # G4: 1151's committed c* for the incumbent, reproduced from its own file
    c151 = pd.read_csv(ROOT / "research" / "backtests" /
                       f"{DATE}_should-PROTOCOL-require-a-COST-CLAIM-to-NAME-ITS-BINDING-"
                       f"LEG_cloud.cstar.csv")
    w = c151[(c151.panel == "U56") & (c151.cadence == "W") & (c151.N == 20) &
             (c151.H == 126)].iloc[0]
    mine = cstar(g0, tn0, d0, BENCH["U56"]["spy"])
    gate("G4", "c* reproduces 1151's committed value for the incumbent",
         f"{mine:.3f} vs {w.full_cstar:.3f}", abs(mine - w.full_cstar) <= 0.05)
    # G5: the CALIBRATION premise — |MaxDD| must be non-decreasing in gross on the real
    # gross ladder.  This, not a scaling identity, is what makes D_GROSS the calibration
    # case: a controlled tape that reverses it has a broken control.
    gl = POP["U56"][(POP["U56"].arm == "G") & (POP["U56"].cadence == "W")].sort_values("gross")
    worst_dd = float(np.min(np.diff(gl.absMaxDD.values)))
    gate("G5", "|MaxDD| non-decreasing in gross on the real U56 gross ladder",
         f"min step {worst_dd:.3e}", worst_dd >= -1e-9)
    # G5b MEASURED AND REPORTED, NOT GATED — a small correction to the record's reading.
    # 1162's G13 proves `W(g) == g*W(1)` for the WEIGHTS.  It does NOT carry to the
    # compounded RETURN path once a cash sleeve is present: holdings are normalised by a
    # portfolio value that includes cash, and cash compounds differently at each gross.
    ga, _ = GTS["U56"][("G", N0, H0, "W", 0.30)]
    gb, _ = GTS["U56"][("G", N0, H0, "W", 0.75)]
    devscale = float(np.abs(gb[WARMUP:] - ga[WARMUP:] * (0.75 / 0.30)).max())
    P(f"  G5b   REPORTED (not gated)  max |r(0.75) - 2.5*r(0.30)| = {devscale:.3e}")
    P("        the WEIGHT identity W(g)==g*W(1) does NOT carry to the compounded RETURN")
    P("        path when gross < 1: the cash sleeve compounds differently at each gross.")
    # G6: the synthetic tapes are EXCHANGEABLE — column order carries no information
    sx = synth(panels["U56"], "T_IID", SEEDS[0])
    dsx = prep(sx)
    cols = [c for c in sx.columns if c != "SPY"]
    perm = list(np.random.default_rng(7).permutation(len(cols)))
    sx2 = sx[[cols[i] for i in perm] + ["SPY"]]
    dsx2 = prep(sx2)
    s1 = fsharpe(run_gt(dsx, N0, H0, "W")[0][WARMUP:])
    s2 = fsharpe(run_gt(dsx2, N0, H0, "W")[0][WARMUP:])
    gate("G6", "T_IID book Sharpe is column-order invariant (the tape is exchangeable)",
         f"{s1:.4f} vs {s2:.4f}", abs(s1 - s2) < 0.20)
    # G7: determinism of the synthetic tapes
    sA = synth(panels["U56"], "T_BLOCK", SEEDS[0])
    sB = synth(panels["U56"], "T_BLOCK", SEEDS[0])
    gate("G7", "synth() deterministic at a fixed seed",
         f"{float((sA-sB).abs().max().max()):.3e}", (sA - sB).abs().max().max() == 0.0)
    # G8: T_FACTOR really is one-factor — median pairwise column correlation is high
    sf = synth(panels["U56"], "T_FACTOR", SEEDS[0])
    cc = sf.drop(columns=["SPY"]).pct_change().iloc[1:].corr().values
    off = cc[~np.eye(len(cc), dtype=bool)]
    ci = synth(panels["U56"], "T_IID", SEEDS[0]).drop(columns=["SPY"]).pct_change().iloc[1:].corr().values
    offi = ci[~np.eye(len(ci), dtype=bool)]
    gate("G8", "T_FACTOR pairwise corr >> T_IID's (one common factor is present)",
         f"{np.median(off):.4f} vs {np.median(offi):.4f}",
         np.median(off) > 0.20 and abs(np.median(offi)) < 0.05)
    gate("G9", "harvest population is non-empty and the claim sets partition it",
         f"{len(hv)} = {int((~hv.has_control).sum())} + {int(hv.has_control.sum())}",
         len(hv) == int((~hv.has_control).sum()) + int(hv.has_control.sum()) and len(hv) > 0)
    P("")

    # --------------------------------------------------------- (B) THE CONTROLLED TAPES
    P("-" * 100)
    P("(B) THE CONTROLLED TAPES — 3 tapes x 3 seeds x 3 panels, 88 books each")
    P("-" * 100)
    t0 = time.time()
    srows = []
    for pn in ("U56", "B136", "SMALL"):
        for tk in TAPES:
            for sd in SEEDS:
                sx = synth(panels[pn], tk, sd)
                ds = prep(sx)
                sbs = blocks_m(ds["spy"], ds)
                lbs = blocks_m(ds["spy"], ds)      # no live book on a synthetic tape
                pop, _ = population(ds, sbs, lbs, want_cstar=True)
                pop["panel"], pop["tape"], pop["seed"] = pn, tk, sd
                srows.append(pop)
            P(f"  {pn:<6} {tk:<9} 3 seeds x {len(pop)} books built")
    syn = pd.concat(srows, ignore_index=True)
    t_syn = time.time() - t0
    P(f"  {len(syn):,} synthetic books in {t_syn:.1f}s")
    P("")

    # ------------------------------------------------- THE SIX DRIVERS, OBSERVED vs CONTROLLED
    P("-" * 100)
    P("THE SIX DRIVERS — cross-book rho on the REAL panel vs rho on a CONTROLLED tape")
    P("-" * 100)

    def rho_for(df, drv):
        """D_TURN is measured over the books that are ALIVE at 0 bps only, because a dead
        book's c* is 0 by definition and a column of tied zeros is not a measurement — this
        is 1151's own construction (it read -0.6484 over 13 live books).  Everything else
        is measured over its whole arm.  Fewer than 5 usable books returns NaN, published
        as DEGENERATE and excluded from every reversal count."""
        dial, out, _, _ = DRIVERS[drv]
        sub = df[df.arm == ("G" if drv == "D_GROSS" else "NH")]
        if drv == "D_TURN":
            sub = sub[sub.cstar > 0]
        if len(sub) < 5:
            return np.nan
        return spearman(sub[dial], sub[out])

    drows = []
    for drv, (dial, out, want, note) in DRIVERS.items():
        for pn in ("U56", "B136", "SMALL"):
            r_obs = rho_for(POP[pn], drv)
            for tk in TAPES:
                vals = [rho_for(syn[(syn.panel == pn) & (syn.tape == tk) & (syn.seed == sd)], drv)
                        for sd in SEEDS]
                r_ctl = float(np.nanmedian(vals))
                drows.append(dict(
                    driver=drv, dial=dial, outcome=out, record_sign=want, note=note,
                    panel=pn, tape=tk, rho_observed=r_obs, rho_controlled=r_ctl,
                    seed_spread=float(np.nanmax(vals) - np.nanmin(vals)),
                    n_ctl_seeds_ok=int(np.isfinite(vals).sum()),
                    sign_obs=int(np.sign(r_obs)) if np.isfinite(r_obs) else 0,
                    sign_ctl=int(np.sign(r_ctl)) if np.isfinite(r_ctl) else 0,
                    RESOLVABLE=bool(np.isfinite(r_obs) and np.isfinite(r_ctl)),
                    REVERSES=bool(np.isfinite(r_obs) and np.isfinite(r_ctl)
                                  and np.sign(r_obs) * np.sign(r_ctl) < 0),
                    attenuation=(abs(r_obs) / abs(r_ctl)
                                 if np.isfinite(r_obs) and np.isfinite(r_ctl) and abs(r_ctl) > 1e-9
                                 else np.nan),
                    obs_matches_record=bool(np.isfinite(r_obs) and np.sign(r_obs) == want)))
    dr = pd.DataFrame(drows)
    dump(dr, "drivers")
    P(f"  {'driver':<9}{'panel':<7}{'rho_obs':>9}   " +
      "".join(f"{tk+'(ctl)':>15}" for tk in TAPES) + "   REVERSALS")
    for drv in DRIVERS:
        for pn in ("U56", "B136", "SMALL"):
            q = dr[(dr.driver == drv) & (dr.panel == pn)].set_index("tape")
            line = f"  {drv:<9}{pn:<7}{q.rho_observed.iloc[0]:>+9.4f}   "
            nrev = ndeg = 0
            for tk in TAPES:
                v = q.loc[tk, "rho_controlled"]
                line += (f"{'DEGENERATE':>15}" if not q.loc[tk, "RESOLVABLE"]
                         else f"{v:>+15.4f}")
                nrev += int(q.loc[tk, "REVERSES"])
                ndeg += int(not q.loc[tk, "RESOLVABLE"])
            P(line + f"   {nrev}/{3-ndeg}" + (f" ({ndeg} degen)" if ndeg else ""))
    P("")
    res = dr[dr.RESOLVABLE]
    P(f"  {len(res)} of {len(dr)} (driver, panel, tape) cells are RESOLVABLE; "
      f"{len(dr)-len(res)} are DEGENERATE (a tied dial or outcome column — published as")
    P("  such and excluded from every count below, never scored as 'does not reverse').")
    P(f"  OVERALL: {int(res.REVERSES.sum())} of {len(res)} resolvable cells REVERSE "
      f"= {res.REVERSES.mean():.4f}")
    P(f"  the observed rho matches the RECORD's asserted sign at "
      f"{int(res.obs_matches_record.sum())} of {len(res)} resolvable cells")
    P(f"  MEDIAN ATTENUATION |rho_obs| / |rho_ctl| = {res.attenuation.median():.4f}  "
      f"(1.0 = the real panel is as strong as the controlled tape)")
    P("  per driver:")
    for drv in DRIVERS:
        q = dr[(dr.driver == drv) & dr.RESOLVABLE]
        n = len(dr[dr.driver == drv])
        P(f"    {drv:<9} reverses {int(q.REVERSES.sum()):>2}/{len(q):<2} ({n-len(q)} degen)  "
          f"med rho_obs {q.rho_observed.median():>+7.4f}   "
          f"med rho_ctl {q.rho_controlled.median():>+7.4f}   "
          f"atten {q.attenuation.median():>6.3f}   ({DRIVERS[drv][3]})")
    P("  per tape:")
    for tk in TAPES:
        q = dr[(dr.tape == tk) & dr.RESOLVABLE]
        n = len(dr[dr.tape == tk])
        P(f"    {tk:<9} reverses {int(q.REVERSES.sum()):>2}/{len(q):<2} ({n-len(q)} degen)   "
          f"med atten {q.attenuation.median():>6.3f}   max seed spread {q.seed_spread.max():.4f}")
    P("")

    # ------------------------------------------------------ THE 9-CELL DIAL GRID
    P("-" * 100)
    P("THE TWO DIALS — CLAIM SET x TAPE, all 9 cells")
    P("-" * 100)
    inscope = {drv: hv[hv[f"topic_{drv}"]] for drv in DRIVERS}
    grows = []
    for cs in CLAIMSETS:
        if cs == "C_ALL":
            keep = [d_ for d_ in DRIVERS if len(inscope[d_])]
        else:
            keep = [d_ for d_ in DRIVERS if len(inscope[d_][inscope[d_].claimset == cs])]
        for tk in TAPES:
            qall = dr[(dr.tape == tk) & (dr.driver.isin(keep))]
            q = qall[qall.RESOLVABLE]
            nsent_cs = (len(hv) if cs == "C_ALL"
                        else int((hv.claimset == cs).sum()))
            grows.append(dict(claimset=cs, tape=tk, n_sentences=nsent_cs,
                              n_drivers_in_scope=len(keep), n_cells=len(qall),
                              n_resolvable=len(q), n_degenerate=len(qall) - len(q),
                              n_reverse=int(q.REVERSES.sum()),
                              share_reverse=float(q.REVERSES.mean()) if len(q) else np.nan,
                              median_attenuation=float(q.attenuation.median()),
                              median_rho_obs=float(q.rho_observed.median()),
                              median_rho_ctl=float(q.rho_controlled.median()),
                              drivers=";".join(keep)))
    grid = pd.DataFrame(grows)
    dump(grid, "grid")
    P("  SHARE OF (driver, panel) CELLS THAT REVERSE, all 9 dial cells:")
    P("  " + grid.pivot(index="claimset", columns="tape", values="share_reverse")
      .loc[CLAIMSETS, TAPES].round(4).to_string().replace("\n", "\n  "))
    P("")
    P("  " + grid[["claimset", "tape", "n_sentences", "n_drivers_in_scope", "n_cells",
                   "n_resolvable", "n_degenerate", "n_reverse", "median_rho_obs",
                   "median_rho_ctl", "median_attenuation"]]
      .to_string(index=False).replace("\n", "\n  "))
    P("")

    # ------------------------------------------------------------------ (C) RULE 8
    P("-" * 100)
    P("(C) RULE 8 — choosers read 2009-2016 ONLY; picks evaluated on untouched 2017-2026")
    P("-" * 100)
    P("  CH_ISSHARPE   plain IS Sharpe argmax at 10 bps                  (the record's habit)")
    P("  CH_DRIVER     act on the record's driver claim: among books within 10% of the best")
    P("                IS Sharpe, take the one the driver's asserted sign prefers (lowest")
    P("                turnover) — 'turnover drives net return' used as a selection rule")
    P("  CH_DRIVER_CTL IDENTICAL, but only where the CONTROLLED tape AGREES in sign with the")
    P("                observed rho; where it reverses, fall back to CH_ISSHARPE")
    P("  CH_ANTI       the FALSIFICATION CONTROL — the driver's OPPOSITE sign (highest")
    P("                turnover inside the same band).  If the driver carries nothing,")
    P("                CH_DRIVER and CH_ANTI must be indistinguishable out of sample.")
    P("")
    BAND = 0.10
    wrows = []
    for pn in ("U56", "B136", "SMALL"):
        d, sb, lbm = D[pn], BENCH[pn]["spy"], BENCH[pn]["live"]
        pop = POP[pn].copy()
        # act on the driver ONLY where the controlled tape RESOLVABLY AGREES in sign.
        # An unresolvable control is not a green light — it is no evidence at all.
        qd = dr[(dr.driver == "D_TURN") & (dr.panel == pn)]
        ok_ctl = qd.RESOLVABLE.any() and not qd[qd.RESOLVABLE].REVERSES.any()
        rev_here = not ok_ctl
        for f in CADENCES:
            cand = pop[(pop.cadence == f) & (pop.arm == "NH")].reset_index(drop=True)
            best = cand.IS_Sharpe.max()
            band = cand[cand.IS_Sharpe >= best - BAND * abs(best)]
            picks = {
                "CH_ISSHARPE": cand.loc[cand.IS_Sharpe.idxmax()],
                "CH_DRIVER": band.loc[band.ann_turnover.idxmin()],
                "CH_DRIVER_CTL": (cand.loc[cand.IS_Sharpe.idxmax()] if rev_here
                                  else band.loc[band.ann_turnover.idxmin()]),
                "CH_ANTI": band.loc[band.ann_turnover.idxmax()],
            }
            for ch, pr in picks.items():
                N, H = int(pr.N), int(pr.H)
                gg, tt = GTS[pn][("NH", N, H, f, GROSS0)]
                m = blocks_m(net(gg, tt, COST0), d)
                l4b, l4bo, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lbm)
                wrows.append(dict(
                    chooser=ch, panel=pn, cadence=f, N=N, H=H,
                    driver_reverses_here=bool(rev_here),
                    IS_Sharpe=pr.IS_Sharpe, ann_turnover=pr.ann_turnover, cstar=pr.cstar,
                    FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"],
                    H1=m["H1"], H2=m["H2"],
                    OOS_CAGR=m["OOS_CAGR"], OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                    SPY_Sharpe=sb["Sharpe"], SPY_H1=sb["H1"], SPY_H2=sb["H2"],
                    SPY_CAGR=sb["CAGR"], SPY_MaxDD=sb["MaxDD"],
                    SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                    SPY_OOS_MaxDD=sb["OOS_MaxDD"], LIVE_OOS_Sharpe=lbm["OOS_Sharpe"],
                    pass_4b=bool(all(l4b.values())), pass_4b_oos=bool(all(l4bo.values())),
                    pass_4a=bool(all(l4a.values())),
                    **{f"leg_{k}": bool(v) for k, v in l4b.items()},
                    **{f"legO_{k}": bool(v) for k, v in l4bo.items()}))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    CH = ("CH_ISSHARPE", "CH_DRIVER", "CH_DRIVER_CTL", "CH_ANTI")
    P("  CHOOSER SCOREBOARD (6 picks each; OOS 2017-2026 never read by any chooser):")
    P(f"  {'chooser':<15}{'medOOS_Sh':>11}{'meanOOS_Sh':>12}{'>SPY OOS':>10}"
      f"{'4b full':>9}{'4b OOS':>9}{'4a':>6}{'med turn':>10}")
    for ch in CH:
        q = wf[wf.chooser == ch]
        P(f"  {ch:<15}{q.OOS_Sharpe.median():>11.4f}{q.OOS_Sharpe.mean():>12.4f}"
          f"{int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum()):>7}/{len(q):<2}"
          f"{int(q.pass_4b.sum()):>6}/{len(q):<2}{int(q.pass_4b_oos.sum()):>6}/{len(q):<2}"
          f"{int(q.pass_4a.sum()):>3}/{len(q):<2}{q.ann_turnover.median():>10.3f}")
    P("")
    P("  EVERY PICK:")
    for _, r in wf.iterrows():
        P(f"    {r.chooser:<14}{r.panel:<6}{r.cadence}  N={r.N:<3}H={r.H:<4} "
          f"full {r.FULL_CAGR:7.2%}/{r.FULL_Sharpe:.4f}/{r.FULL_MaxDD:7.2%} "
          f"halves {r.H1:.3f}/{r.H2:.3f} | OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/"
          f"{r.OOS_MaxDD:7.2%} | turn {r.ann_turnover:5.2f} c* {r.cstar:6.1f} "
          f"4b {'Y' if r.pass_4b else 'n'}{'Y' if r.pass_4b_oos else 'n'} "
          f"4a {'Y' if r.pass_4a else 'n'}")
    P("")
    both = allbooks[allbooks.pass_4b & allbooks.pass_4b_oos]
    P(f"  ACROSS ALL {len(allbooks)} REAL BOOKS at 10 bps: 4b full {int(allbooks.pass_4b.sum())}, "
      f"4b OOS {int(allbooks.pass_4b_oos.sum())}, BOTH {len(both)}, "
      f"4a {int(allbooks.pass_4a.sum())}.")
    if len(both):
        P("  the books clearing 4b FULL AND OOS at 10 bps:")
        for _, r in both.sort_values("Sharpe", ascending=False).iterrows():
            P(f"    {r.panel:<6}{r.cadence} arm={r.arm:<3} N={int(r.N):<3}H={int(r.H):<4}"
              f"g={r.gross:.2f}  {r.CAGR:7.2%}/{r.Sharpe:.4f}/{r.MaxDD:7.2%} "
              f"halves {r.H1:.3f}/{r.H2:.3f} | OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/"
              f"{r.OOS_MaxDD:7.2%} | c* {r.cstar:6.1f}")
    P("")

    gdf = pd.DataFrame(gates)
    dump(gdf, "gates")
    P(f"GATES {int(gdf.pass_.sum())} of {len(gdf)} PASS")
    P(f"TOTAL RUNTIME {time.time()-t_start:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
