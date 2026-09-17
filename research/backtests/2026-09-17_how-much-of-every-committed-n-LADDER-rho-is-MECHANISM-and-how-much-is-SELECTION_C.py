#!/usr/bin/env python3
"""Idea 1176 (lane C, 2026-09-17) — how much of every committed n-LADDER rho is MECHANISM
and how much is SELECTION?

Idea 1171 found that five of six price-native driver claims keep their SIGN on a controlled
tape, but that the MAGNITUDES do not carry: the real panel shows only 0.202 of the
controlled tape's N -> Sharpe relation (+0.1659 against +0.9134) and 0.582 of its
N -> |MaxDD| relation (-0.4980 against -0.9377).  On an exchangeable tape book size orders
Sharpe and drawdown almost perfectly, because a smaller book is simply a noisier average of
i.i.d. columns.  On the real panel most of that is cancelled.  The record quotes those
attenuated magnitudes as STRENGTH.  This run decomposes them.

THE DECOMPOSITION, and why it needs a control 1171 did not run.
1171's `attenuation` compares a REAL-tape/SCORE-selected rho against a SYNTHETIC-tape/
score-selected one, so it confounds TWO differences at once: the tape (real cross-sectional
structure and fat tails vs exchangeable columns) and the SELECTION (a composite score picks
the names vs nothing distinguishes them).  Adding one control separates them at fixed tape:

  T_REALRAND   the REAL panel, the REAL eligibility gate, the REAL cadence / min-hold /
               gross machinery, but the RANK KEY replaced by exchangeable noise, so the
               book is a RANDOM N of the eligible names.  Same tape, no selection.

  rho_obs      real tape, score selection        (what the record publishes)
  rho_rand     real tape, random selection       (the MECHANISM, on the record's own tape)
  rho_synth    exchangeable tape, score selection (the MECHANISM with no names at all)

  SELECTION      = rho_obs  - rho_rand    <- identified at FIXED TAPE.  This is the term
                                             the queue asks for.
  TAPE STRUCTURE = rho_rand - rho_synth   <- what 1171's attenuation folded into "selection"
  retention      = rho_obs / rho_rand     <- share of the mechanism the real book keeps

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4; the queue names both):
  CLAIM SET  {C_VALUED, C_SIGNED, C_ALL}     which committed n-ladder sentences are scored
  TAPE       {T_REALRAND, T_IID, T_BLOCK, T_FACTOR}   what the mechanism is measured on
= 12 cells, EVERY ONE PUBLISHED in `.grid.csv`.
NOT dials, all reported at every value: PANEL {U56, B136, SMALL}; the six n-ladder OUTCOMES;
the 88-book population per panel (N x H x cadence at gross 0.75 plus a gross ladder);
SEED (five at every controlled cell, spread published); the reading-change BAR (reported on
a 0.00/0.25/0.50/0.75/1.00 ladder, headline at 0.50, so any bar can be read off the file);
the four rule-8 choosers.  Frozen at 1082/1086/1093/1094/1151/1164/1171's construction:
CAND20 legs [(21,252),(0,126),(0,63)], max_vol 0.60, cost 10 bps (rule 2), LAG 1, warm-up
260, IS end 2016-12-31, zero cash, DD cap 0.60, CAGR floor 0.70.

WHAT "CHANGES READING" MEANS, stated before the numbers are seen.
  SIGN change       sign(rho_obs) != sign(rho_mech): the direction the record asserts is not
                    the mechanism's.  This is the only thing that can move a SIGNED claim.
  MAGNITUDE change  retention < BAR (0.50): the quoted rho is majority-SELECTION, not the
                    dial's mechanism.  A VALUED claim quoting such a rho as the strength of
                    a diversification / edge argument is over-read.
A C_SIGNED claim changes reading on SIGN only; a C_VALUED claim on either.

SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current
constituents of a sub-$2B screen LESS every ticker with max_1d_move >= 1.0 in
data/small_meta.csv, dropped before anything else is computed.  Every LEVEL is optimistic
and the bias does NOT cancel out of the 4b legs.  It cancels much better out of a rho, which
ranks one construction against itself on one tape — but T_REALRAND is built from the SAME
surviving names, so the mechanism term inherits the same optimistic marginals as rho_obs,
which is exactly what makes the SELECTION difference the cleaner of the two contrasts.

Writes: .gates.csv .harvest.csv .cells.csv .grid.csv .claims.csv .books.csv .walkforward.csv
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
SLUG = "how-much-of-every-committed-n-LADDER-rho-is-MECHANISM-and-how-much-is-SELECTION"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
LOG = []

LAG, WARMUP = 1, 260
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, COST0, MAXVOL0, N0, H0 = 0.75, 10.0, 0.60, 20, 126
LEGS = [(21, 252), (0, 126), (0, 63)]
START = "2008-01-01"
SEEDS = [20260917, 20260918, 20260919, 20260920, 20260921]
BLOCK_L = 63

N_LADDER = [5, 8, 10, 12, 15, 20, 25, 30, 40]
H_LADDER = [21, 63, 126, 252]
G_LADDER = [0.30, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.00]
CADENCES = ["W", "M"]
PANELS = ["U56", "B136", "SMALL"]

CLAIMSETS = ["C_VALUED", "C_SIGNED", "C_ALL"]
TAPES = ["T_REALRAND", "T_IID", "T_BLOCK", "T_FACTOR"]
SYNTH_TAPES = ["T_IID", "T_BLOCK", "T_FACTOR"]
BARS = [0.00, 0.25, 0.50, 0.75, 1.00]
BAR0 = 0.50

# the six n-LADDER outcomes the record's n-ladder claims are about.  dial is ALWAYS N.
# record_sign is the direction the record asserts, taken from 1171's DRIVERS table and
# 1082/1086/1093's EDGE-ladder premise -- not chosen here.
OUTCOMES = {
    "O_SHARPE":  ("Sharpe", -1, "N -> Sharpe (1082/1086/1093 EDGE-ladder premise: smaller is better)"),
    "O_DD":      ("absMaxDD", -1, "N -> |MaxDD| (the diversification claim behind every n ladder)"),
    "O_CAGR":    ("CAGR", -1, "N -> CAGR (concentration premium)"),
    "O_TURN":    ("ann_turnover", -1, "N -> annual turnover"),
    "O_OOSSH":   ("OOS_Sharpe", -1, "N -> OOS Sharpe (the ladder as a selection device)"),
    "O_CSTAR":   ("cstar", -1, "N -> c* (4b-CONDITIONAL; 1175's population, published as such)"),
}

# ---- the harvest's regexes.  An n-ladder sentence names BOOK SIZE and an ORDERING token.
NTOK_RE = re.compile(r"\bn[- ]?ladder\b|\bN\s*=\s*\d|\bn\s*=\s*\d|\bbook size\b|"
                     r"\bnumber of (names|holdings|positions)\b|\btop-?\d+\b|"
                     r"\bEDGE\s*\(\s*\d", re.I)
RHO_RE = re.compile(r"\b(rho|spearman|rank correlation|correlation|corr\b|kendall)\b", re.I)
ORDER_RE = re.compile(r"\b(monoton\w*|order(s|ed|ing)?|ladder|slope|increas\w*|decreas\w*|"
                      r"rises?|falls?|declin\w*|hump\w*|argmax|peak\w*)\b", re.I)
VAL_RE = re.compile(r"[-+−]?\s?\d?\.\d{2,}")          # a quoted magnitude, e.g. -0.4980
CTRL_RE = re.compile(r"\b(control|controlled|intervention|one-factor|exchangeable|"
                     r"held fixed|synthetic|matched|counterfactual|ablat|null)", re.I)
# which OUTCOME a harvested sentence is about (a sentence may touch more than one)
OTOPIC = {
    "O_SHARPE": re.compile(r"\bsharpe\b", re.I),
    "O_DD":     re.compile(r"\bmaxdd\b|\bdrawdown\b|\bDD\b", re.I),
    "O_CAGR":   re.compile(r"\bcagr\b|\breturn\b", re.I),
    "O_TURN":   re.compile(r"\bturnover\b", re.I),
    "O_OOSSH":  re.compile(r"\bOOS\b|\bout[- ]of[- ]sample\b", re.I),
    "O_CSTAR":  re.compile(r"\bc\*|\bbreakeven\b|\bbinding leg\b", re.I),
}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------- 1082/../1171's fast runner and book, VERBATIM
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


def run_gt(d, N, H, freq, gross=GROSS0, maxvol=MAXVOL0, key=None):
    """key=None uses the composite score (SELECTION on).  key=<array> substitutes an
    exchangeable rank key (SELECTION off) with EVERYTHING ELSE — tape, eligibility gate,
    cadence, min hold, gross, lag, costs — held exactly fixed."""
    mk = d["mk"][freq]
    mkl = np.roll(mk, LAG)
    mkl[:LAG] = False
    reb = np.flatnonzero(mk)
    el = d["above"] & (d["vol20"] < maxvol)
    rk = (-d["sc"]) if key is None else key
    W = build(rk, el, d["priced"], reb, N, H, d["T"], d["K"], gross)
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


CSTAR_HI, CSTAR_TOL = 300.0, 1e-3


def cstar(g, tn, d, sb, lo=0.0, hi=CSTAR_HI):
    """1151's c*: the cost at which the book's first 4b leg fails."""
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
    """1171's `synth()`, VERBATIM: a tape on which every column is EXCHANGEABLE, with its
    own synthetic SPY built from the synthetic names (never the real one)."""
    rng = np.random.default_rng(seed)
    cols = [c for c in px.columns if c != "SPY"]
    R = px[cols].pct_change().values
    T, K = R.shape
    pooled = R[np.isfinite(R)]
    mu, sd = float(np.mean(pooled)), float(np.std(pooled))
    if kind == "T_IID":
        X = rng.normal(mu, sd, size=(T, K))
    elif kind == "T_BLOCK":
        src = np.where(np.isfinite(R), R, 0.0)
        nb = int(np.ceil(T / BLOCK_L))
        ar = np.arange(BLOCK_L)
        X = np.empty((T, K))
        for k in range(K):
            col = rng.integers(0, K)
            st = rng.integers(0, T - BLOCK_L + 1, size=nb)
            X[:, k] = src[(st[:, None] + ar[None, :]).ravel()[:T], col]
    else:  # T_FACTOR
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
    prices["SPY"] = 100.0 * np.cumprod(1.0 + X.mean(axis=1))
    return prices


def rand_key(d, seed):
    """THE NEW CONTROL.  An exchangeable rank key on the REAL tape: a fresh uniform draw
    per (day, name), so the book is a random N of the names the REAL eligibility gate
    admits.  Nothing else about the machinery changes."""
    return np.random.default_rng(seed).random((d["T"], d["K"]))


def main():
    t_start = time.time()
    P("=" * 100)
    P(f"IDEA 1176 (lane C) — {SLUG}")
    P("=" * 100)
    P("TWO TUNED PARAMETERS (rule 4): CLAIM SET {C_VALUED,C_SIGNED,C_ALL} x")
    P("TAPE {T_REALRAND,T_IID,T_BLOCK,T_FACTOR} = 12 cells, all published in .grid.csv.")
    P("PANEL, the six n-ladder OUTCOMES, the 88-book population, SEED, the reading-change")
    P("BAR ladder and the four rule-8 choosers are NOT dials — all values reported.")
    P("")
    P("DECOMPOSITION (stated before any number is seen):")
    P("  rho_obs  = real tape, SCORE selection      (what the record publishes)")
    P("  rho_rand = real tape, RANDOM selection     (T_REALRAND: the mechanism on the")
    P("             record's OWN tape — identified at FIXED TAPE)")
    P("  rho_syn  = exchangeable tape, score sel.   (the mechanism with no names at all)")
    P("  SELECTION = rho_obs - rho_rand;  TAPE STRUCTURE = rho_rand - rho_syn")
    P("  retention = rho_obs / rho_mech;  a claim's MAGNITUDE changes reading at retention")
    P(f"  < BAR = {BAR0} (whole ladder {BARS} published), its SIGN at a sign flip.")
    P("")

    # --------------------------------------------------------- (A) THE HARVEST
    P("-" * 100)
    P("(A) THE HARVEST — the record's committed n-LADDER claims")
    P("-" * 100)
    files = ["research/LEADERBOARD.md", "research/CHANGELOG.md"] + \
        sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.result.md"))) + \
        sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.memo.md")))
    files = [str(Path(f).relative_to(ROOT)) if Path(f).is_absolute() else f for f in files]
    hrows, nsent = [], 0
    for f in files:
        txt = (ROOT / f).read_text(errors="replace")
        for ln, line in enumerate(txt.split("\n"), 1):
            for s in re.split(r"(?<=[.;])\s+", line):
                if len(s) < 40:
                    continue
                nsent += 1
                if not NTOK_RE.search(s):
                    continue
                if not (RHO_RE.search(s) or ORDER_RE.search(s)):
                    continue
                valued = bool(VAL_RE.search(s))
                topics = {k: bool(v.search(s)) for k, v in OTOPIC.items()}
                hrows.append(dict(
                    claim_id=len(hrows), src=f, line=ln,
                    has_rho_token=bool(RHO_RE.search(s)),
                    has_control=bool(CTRL_RE.search(s)),
                    valued=valued, claimset="C_VALUED" if valued else "C_SIGNED",
                    **{f"topic_{k}": v for k, v in topics.items()},
                    n_topics=sum(topics.values()), text=s[:600]))
    hv = pd.DataFrame(hrows)
    dump(hv, "harvest")
    P(f"  {len(files)} committed files, {nsent:,} sentences scanned")
    P(f"  sentences naming BOOK SIZE and an ORDERING/CORRELATION token: {len(hv):,}")
    P(f"    of which QUOTE A MAGNITUDE (C_VALUED): {int(hv.valued.sum()):,} "
      f"({hv.valued.mean():.4f})")
    P(f"    directional only            (C_SIGNED): {int((~hv.valued).sum()):,} "
      f"({(~hv.valued).mean():.4f})")
    P(f"    carrying an explicit rho token:         {int(hv.has_rho_token.sum()):,}")
    P(f"    naming a CONTROL of any kind:           {int(hv.has_control.sum()):,} "
      f"({hv.has_control.mean():.4f})")
    P("  by n-ladder OUTCOME topic (a sentence may touch more than one):")
    for k in OUTCOMES:
        q = hv[hv[f"topic_{k}"]]
        P(f"    {k:<9} {len(q):>6} sentences   valued {int(q.valued.sum()):>6}   "
          f"({OUTCOMES[k][2]})")
    P(f"  touching NONE of the six outcomes: {int((hv.n_topics == 0).sum()):,} of {len(hv)} — "
      f"OUT OF SCOPE, declared, never quietly counted")
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
    P("  optimistic.  T_REALRAND inherits the SAME surviving marginals as rho_obs, which is")
    P("  what makes the SELECTION contrast the cleaner of the two.")
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
    def population(d, sb, lbm, key=None):
        """88 books: N x H x cadence at gross 0.75, plus a gross ladder at N=20/H=126."""
        rows, GT = [], {}
        specs = [("NH", N, H, f, GROSS0) for f in CADENCES for N in N_LADDER for H in H_LADDER]
        specs += [("G", N0, H0, f, g) for f in CADENCES for g in G_LADDER]
        for arm, N, H, f, g in specs:
            gg, tt = run_gt(d, N, H, f, gross=g, key=key)
            GT[(arm, N, H, f, g)] = (gg, tt)
            m = blocks_m(net(gg, tt, COST0), d)
            l4b, l4bo, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lbm)
            rows.append(dict(arm=arm, N=N, H=H, cadence=f, gross=g,
                             ann_turnover=float(tt.sum() / (len(tt) / 252.0)),
                             absMaxDD=abs(m["MaxDD"]), cstar=cstar(gg, tt, d, sb),
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
    for pn in PANELS:
        POP[pn], GTS[pn] = population(D[pn], BENCH[pn]["spy"], BENCH[pn]["live"])
        P(f"  {pn:<6} {len(POP[pn])} books")
    P(f"  264 real books in {time.time()-t0:.1f}s")
    allbooks = pd.concat([POP[pn].assign(panel=pn, tape="REAL", seed=0) for pn in POP],
                         ignore_index=True)
    dump(allbooks, "books")
    P("  BASE RATES at 10 bps:")
    for pn in PANELS:
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

    # G4 the run REPRODUCES 1171's two committed attenuations it is built to decompose.
    f171 = sorted(glob.glob(str(ROOT / "research" / "backtests" /
                                "*DRIVER-claims-REVERSE-under-a-CONTROLLED-tape*.drivers.csv")))
    d171 = pd.read_csv(f171[-1])
    for nm, drv, col, want in (("G4", "D_N_SH", "rho_observed", 0.1659),
                               ("G5", "D_N", "rho_observed", -0.4980)):
        got = float(d171[d171.driver == drv][col].median())
        gate(nm, f"1171's committed median {col} for {drv} ({want})", round(got, 4),
             abs(got - want) <= 2e-3)

    # G6 THE NEW CONTROL IS REALLY EXCHANGEABLE: two independent random keys must give
    # books whose N->Sharpe rho agrees far better with each other than with the real one.
    rk_a, rk_b = rand_key(d0, SEEDS[0]), rand_key(d0, SEEDS[1])
    ra, _ = run_gt(d0, N0, H0, "W", key=rk_a)
    rb, _ = run_gt(d0, N0, H0, "W", key=rk_b)
    sa, sbb = fsharpe(ra[WARMUP:]), fsharpe(rb[WARMUP:])
    gate("G6", "T_REALRAND is seed-exchangeable (two random keys, same incumbent cell)",
         f"{sa:.4f} vs {sbb:.4f}", abs(sa - sbb) < 0.40)

    # G7 THE CONTROL REALLY REMOVES SELECTION: the random book must under-perform the
    # score book at the incumbent cell.  If it does not, the composite carries nothing and
    # every 'selection' term below would be mislabelled.
    s_score = fsharpe(net(g0, tn0, COST0)[WARMUP:])
    s_rand = fsharpe(net(ra, run_gt(d0, N0, H0, "W", key=rk_a)[1], COST0)[WARMUP:])
    gate("G7", "the composite score beats a random book at the incumbent cell "
         "(so 'selection' is a real term)", f"{s_score:.4f} vs {s_rand:.4f}",
         s_score > s_rand)

    # G8 determinism of the new control
    gate("G8", "rand_key() deterministic at a fixed seed",
         f"{float(np.abs(rand_key(d0, SEEDS[0]) - rk_a).max()):.3e}",
         np.abs(rand_key(d0, SEEDS[0]) - rk_a).max() == 0.0)

    # G9 synth() determinism (1171's G7, re-run here because this file re-uses it)
    sA, sB = synth(panels["U56"], "T_BLOCK", SEEDS[0]), synth(panels["U56"], "T_BLOCK", SEEDS[0])
    gate("G9", "synth() deterministic at a fixed seed",
         f"{float((sA-sB).abs().max().max()):.3e}", (sA - sB).abs().max().max() == 0.0)

    # G10 the harvest's claim sets partition it
    gate("G10", "harvest claim sets partition the population",
         f"{len(hv)} = {int(hv.valued.sum())} + {int((~hv.valued).sum())}",
         len(hv) > 0 and len(hv) == int(hv.valued.sum()) + int((~hv.valued).sum()))
    P("")

    # --------------------------------------------------------- (B) THE MECHANISM TAPES
    P("-" * 100)
    P(f"(B) THE MECHANISM TAPES — {len(TAPES)} tapes x {len(SEEDS)} seeds x 3 panels, 88 books each")
    P("-" * 100)
    t0 = time.time()
    srows = []
    for pn in PANELS:
        for tk in TAPES:
            for sd in SEEDS:
                if tk == "T_REALRAND":
                    ds, sbs, lbs = D[pn], BENCH[pn]["spy"], BENCH[pn]["spy"]
                    pop, _ = population(ds, sbs, lbs, key=rand_key(ds, sd))
                else:
                    sx = synth(panels[pn], tk, sd)
                    ds = prep(sx)
                    sbs = blocks_m(ds["spy"], ds)
                    pop, _ = population(ds, sbs, sbs, key=None)
                pop["panel"], pop["tape"], pop["seed"] = pn, tk, sd
                srows.append(pop)
            P(f"  {pn:<6} {tk:<11} {len(SEEDS)} seeds x {len(pop)} books built "
              f"({time.time()-t0:.0f}s elapsed)")
    syn = pd.concat(srows, ignore_index=True)
    P(f"  {len(syn):,} mechanism books in {time.time()-t0:.1f}s")
    P("")

    # ------------------------------------------- THE DECOMPOSITION, cell by cell
    P("-" * 100)
    P("THE DECOMPOSITION — rho_obs = MECHANISM + SELECTION, per (outcome, panel, tape)")
    P("-" * 100)

    def rho_for(df, out):
        """n-ladder rho over the NH arm (72 books: 9 N x 4 H x 2 cadences), 1171's own
        pooling.  O_CSTAR is measured over the books ALIVE at 0 bps only (1151/1171's
        convention); a column of tied zeros is DEGENERATE, never 0.0."""
        col = OUTCOMES[out][0]
        sub = df[df.arm == "NH"]
        if out == "O_CSTAR":
            sub = sub[sub.cstar > 0]
        if len(sub) < 5:
            return np.nan
        return spearman(sub["N"], sub[col])

    crows = []
    for out in OUTCOMES:
        col, want, note = OUTCOMES[out]
        for pn in PANELS:
            r_obs = rho_for(POP[pn], out)
            for tk in TAPES:
                vals = [rho_for(syn[(syn.panel == pn) & (syn.tape == tk) & (syn.seed == sd)], out)
                        for sd in SEEDS]
                fin = [v for v in vals if np.isfinite(v)]
                r_mech = float(np.median(fin)) if fin else np.nan
                resolvable = bool(np.isfinite(r_obs) and np.isfinite(r_mech)
                                  and abs(r_mech) > 1e-9)
                sel = (r_obs - r_mech) if (np.isfinite(r_obs) and np.isfinite(r_mech)) else np.nan
                ret = (r_obs / r_mech) if resolvable else np.nan
                crows.append(dict(
                    outcome=out, dial="N", outcome_col=col, record_sign=want, note=note,
                    panel=pn, tape=tk, rho_obs=r_obs, rho_mech=r_mech,
                    selection=sel, retention=ret,
                    abs_share_selection=(abs(sel) / (abs(r_mech) + abs(sel))
                                         if np.isfinite(sel) and (abs(r_mech) + abs(sel)) > 1e-12
                                         else np.nan),
                    seed_spread=(float(np.max(fin) - np.min(fin)) if len(fin) > 1 else np.nan),
                    n_seeds_ok=len(fin),
                    RESOLVABLE=resolvable,
                    SIGN_CHANGE=bool(resolvable and np.sign(r_obs) != np.sign(r_mech)),
                    obs_matches_record=bool(np.isfinite(r_obs) and np.sign(r_obs) == want),
                    **{f"MAG_CHANGE_bar{int(b*100):03d}": bool(resolvable and ret < b)
                       for b in BARS}))
    cells = pd.DataFrame(crows)
    dump(cells, "cells")

    P(f"  {'outcome':<10}{'panel':<7}{'rho_obs':>9}   " +
      "".join(f"{tk:>13}" for tk in TAPES))
    for out in OUTCOMES:
        for pn in PANELS:
            q = cells[(cells.outcome == out) & (cells.panel == pn)].set_index("tape")
            line = (f"  {out:<10}{pn:<7}"
                    + (f"{q.rho_obs.iloc[0]:>+9.4f}" if np.isfinite(q.rho_obs.iloc[0]) else f"{'DEGEN':>9}")
                    + "   ")
            for tk in TAPES:
                v = q.loc[tk, "rho_mech"]
                line += (f"{v:>+13.4f}" if np.isfinite(v) else f"{'DEGENERATE':>13}")
            P(line)
    P("")
    P(f"  {'outcome':<10}{'panel':<7}{'tape':<12}{'rho_obs':>9}{'rho_mech':>10}"
      f"{'SELECTION':>11}{'retention':>11}{'|sel| share':>12}{'seedspread':>11}  flags")
    for _, r in cells.iterrows():
        if not r.RESOLVABLE:
            P(f"  {r.outcome:<10}{r.panel:<7}{r.tape:<12}"
              f"{r.rho_obs if np.isfinite(r.rho_obs) else float('nan'):>+9.4f}"
              f"{'DEGENERATE':>10}{'':>11}{'':>11}{'':>12}"
              f"{'':>11}  NOT RESOLVABLE")
            continue
        fl = []
        if r.SIGN_CHANGE:
            fl.append("SIGN-FLIP")
        if r[f"MAG_CHANGE_bar{int(BAR0*100):03d}"]:
            fl.append(f"MAG<{BAR0}")
        P(f"  {r.outcome:<10}{r.panel:<7}{r.tape:<12}{r.rho_obs:>+9.4f}{r.rho_mech:>+10.4f}"
          f"{r.selection:>+11.4f}{r.retention:>+11.4f}{r.abs_share_selection:>12.4f}"
          f"{r.seed_spread:>11.4f}  {' '.join(fl)}")
    P("")
    res = cells[cells.RESOLVABLE]
    P(f"  {len(res)} of {len(cells)} (outcome, panel, tape) cells RESOLVABLE; "
      f"{len(cells)-len(res)} DEGENERATE (a tied dial/outcome column or a zero mechanism),")
    P("  published as such and excluded from every share below — never scored as 'no change'.")
    P(f"  MEDIAN retention (rho_obs / rho_mech) = {res.retention.median():.4f}")
    P(f"  MEDIAN |selection| share of |mech|+|sel| = {res.abs_share_selection.median():.4f}")
    P(f"  SIGN CHANGES: {int(res.SIGN_CHANGE.sum())} of {len(res)}")
    for b in BARS:
        c = f"MAG_CHANGE_bar{int(b*100):03d}"
        P(f"  retention < {b:.2f}: {int(res[c].sum()):>3} of {len(res)} "
          f"({res[c].mean():.4f})")
    P("  per OUTCOME (median over panels x tapes):")
    for out in OUTCOMES:
        q = res[res.outcome == out]
        n_all = len(cells[cells.outcome == out])
        if not len(q):
            P(f"    {out:<10} ALL {n_all} CELLS DEGENERATE   ({OUTCOMES[out][2]})")
            continue
        P(f"    {out:<10} rho_obs {q.rho_obs.median():>+7.4f}  mech {q.rho_mech.median():>+7.4f}  "
          f"sel {q.selection.median():>+7.4f}  retention {q.retention.median():>+7.4f}  "
          f"sign-flips {int(q.SIGN_CHANGE.sum())}/{len(q)} ({n_all-len(q)} degen)")
    P("  per TAPE (median over outcomes x panels):")
    for tk in TAPES:
        q = res[res.tape == tk]
        P(f"    {tk:<12} mech {q.rho_mech.median():>+7.4f}  retention {q.retention.median():>+7.4f}  "
          f"sign-flips {int(q.SIGN_CHANGE.sum())}/{len(q)}  "
          f"max seed spread {q.seed_spread.max():.4f}")
    P("  per PANEL (median over outcomes x tapes):")
    for pn in PANELS:
        q = res[res.panel == pn]
        P(f"    {pn:<12} rho_obs {q.rho_obs.median():>+7.4f}  mech {q.rho_mech.median():>+7.4f}  "
          f"retention {q.retention.median():>+7.4f}")
    P("")
    P("  THE TWO CONTRASTS SEPARATED (the reason T_REALRAND was added):")
    P(f"  {'outcome':<10}{'panel':<7}{'rho_obs':>9}{'rand(real)':>12}{'syn(median)':>13}"
      f"{'SELECTION':>11}{'TAPE-STRUCT':>13}")
    for out in OUTCOMES:
        for pn in PANELS:
            q = cells[(cells.outcome == out) & (cells.panel == pn)]
            rr = q[q.tape == "T_REALRAND"].rho_mech.iloc[0]
            sy = q[q.tape.isin(SYNTH_TAPES)].rho_mech.median()
            ob = q.rho_obs.iloc[0]
            if not (np.isfinite(rr) and np.isfinite(sy) and np.isfinite(ob)):
                P(f"  {out:<10}{pn:<7}{'':>9}{'':>12}{'':>13}  NOT RESOLVABLE")
                continue
            P(f"  {out:<10}{pn:<7}{ob:>+9.4f}{rr:>+12.4f}{sy:>+13.4f}"
              f"{ob-rr:>+11.4f}{rr-sy:>+13.4f}")
    P("")

    # ------------------------------------------------------ (C) THE 12-CELL DIAL GRID
    P("-" * 100)
    P("(C) THE TWO DIALS — CLAIM SET x TAPE, all 12 cells: how many CLAIMS change reading")
    P("-" * 100)
    P("  A claim is scored on the (outcome, panel) cells its own text is about; a claim")
    P("  touching no priced outcome is UNSCORABLE and counted separately, never as 'no")
    P("  change'.  C_SIGNED changes on a SIGN flip only; C_VALUED on a sign flip OR")
    P(f"  retention < {BAR0}.")
    MAGCOL = f"MAG_CHANGE_bar{int(BAR0*100):03d}"
    LOOK = {(tk, o): cells[(cells.tape == tk) & cells.RESOLVABLE & (cells.outcome == o)]
            for tk in TAPES for o in OUTCOMES}
    clrows = []
    for cs in CLAIMSETS:
        pop_cl = hv if cs == "C_ALL" else hv[hv.claimset == cs]
        for tk in TAPES:
            n_scor = n_sign = n_mag = n_any = n_unscor = 0
            for _, c in pop_cl.iterrows():
                outs = [o for o in OUTCOMES if c[f"topic_{o}"]]
                q = (pd.concat([LOOK[(tk, o)] for o in outs]) if outs
                     else cells.iloc[:0])
                if not outs or not len(q):
                    n_unscor += 1
                    continue
                n_scor += 1
                sign = bool(q.SIGN_CHANGE.any())
                # a claim's MAGNITUDE changes reading when the MAJORITY of the (outcome,
                # panel) cells it is about retain less than BAR0 of the mechanism.
                mag = bool(q[MAGCOL].mean() > 0.5)
                changes = sign if not c.valued else (sign or mag)
                n_sign += int(sign)
                n_mag += int(mag and c.valued)
                n_any += int(changes)
                clrows.append(dict(claimset=cs, tape=tk, claim_id=int(c.claim_id),
                                   valued=bool(c.valued), outcomes=";".join(outs),
                                   n_cells=len(q), sign_change=sign, mag_change=bool(mag),
                                   CHANGES_READING=bool(changes), src=c.src, line=int(c.line),
                                   text=c.text[:300]))
            clrows.append(dict(claimset=cs, tape=tk, claim_id=-1, valued=None,
                               outcomes="__SUMMARY__", n_cells=n_scor, sign_change=n_sign,
                               mag_change=n_mag, CHANGES_READING=n_any,
                               src=f"unscorable={n_unscor}", line=len(pop_cl), text=""))
    claims = pd.DataFrame(clrows)
    dump(claims, "claims")
    summ = claims[claims.outcomes == "__SUMMARY__"].copy()
    summ = summ.rename(columns={"n_cells": "n_scorable", "sign_change": "n_sign",
                                "mag_change": "n_mag", "CHANGES_READING": "n_change",
                                "line": "n_claims", "src": "unscorable"})
    summ["share_change"] = summ.n_change / summ.n_scorable.replace(0, np.nan)
    grid = summ[["claimset", "tape", "n_claims", "n_scorable", "unscorable",
                 "n_sign", "n_mag", "n_change", "share_change"]]
    dump(grid, "grid")
    P("  SHARE OF SCORABLE CLAIMS THAT CHANGE READING, all 12 dial cells:")
    P("  " + grid.pivot(index="claimset", columns="tape", values="share_change")
      .loc[CLAIMSETS, TAPES].round(4).to_string().replace("\n", "\n  "))
    P("")
    P("  " + grid.to_string(index=False).replace("\n", "\n  "))
    P("")

    # ------------------------------------------------------------------ (D) RULE 8
    P("-" * 100)
    P("(D) RULE 8 — choosers read 2009-2016 ONLY; picks evaluated on untouched 2017-2026")
    P("-" * 100)
    P("  CH_ISSHARPE  plain IS Sharpe argmax at 10 bps                   (the record's habit)")
    P("  CH_NSMALL    ACT ON the n-ladder claim as the record states it: among books within")
    P("               10% of the best IS Sharpe, take the SMALLEST N")
    P("  CH_NMECH     IDENTICAL, but only where the MECHANISM survives on the record's own")
    P("               tape (T_REALRAND, retention >= BAR and no sign flip for O_SHARPE on")
    P("               that panel); otherwise fall back to CH_ISSHARPE")
    P("  CH_NBIG      the FALSIFICATION CONTROL — the LARGEST N in the same band.  If the")
    P("               n-ladder rho carries nothing for selection, these must be alike.")
    P("")
    BAND = 0.10
    wrows = []
    for pn in PANELS:
        d, sb, lbm = D[pn], BENCH[pn]["spy"], BENCH[pn]["live"]
        pop = POP[pn].copy()
        q = cells[(cells.outcome == "O_SHARPE") & (cells.panel == pn) &
                  (cells.tape == "T_REALRAND")].iloc[0]
        mech_ok = bool(q.RESOLVABLE and (not q.SIGN_CHANGE) and q.retention >= BAR0)
        for f in CADENCES:
            cand = pop[(pop.cadence == f) & (pop.arm == "NH")].reset_index(drop=True)
            best = cand.IS_Sharpe.max()
            band = cand[cand.IS_Sharpe >= best - BAND * abs(best)]
            picks = {
                "CH_ISSHARPE": cand.loc[cand.IS_Sharpe.idxmax()],
                "CH_NSMALL": band.loc[band.N.idxmin()],
                "CH_NMECH": (band.loc[band.N.idxmin()] if mech_ok
                             else cand.loc[cand.IS_Sharpe.idxmax()]),
                "CH_NBIG": band.loc[band.N.idxmax()],
            }
            for ch, pr in picks.items():
                N, H = int(pr.N), int(pr.H)
                gg, tt = GTS[pn][("NH", N, H, f, GROSS0)]
                m = blocks_m(net(gg, tt, COST0), d)
                l4b, l4bo, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lbm)
                wrows.append(dict(
                    chooser=ch, panel=pn, cadence=f, N=N, H=H,
                    mechanism_survives_here=mech_ok,
                    retention_O_SHARPE_realrand=float(q.retention) if np.isfinite(q.retention) else np.nan,
                    IS_Sharpe=float(pr.IS_Sharpe), ann_turnover=float(pr.ann_turnover),
                    cstar=float(pr.cstar),
                    FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"],
                    H1=m["H1"], H2=m["H2"],
                    OOS_CAGR=m["OOS_CAGR"], OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                    SPY_Sharpe=sb["Sharpe"], SPY_H1=sb["H1"], SPY_H2=sb["H2"],
                    SPY_CAGR=sb["CAGR"], SPY_MaxDD=sb["MaxDD"],
                    SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                    SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                    LIVE_Sharpe=lbm["Sharpe"], LIVE_OOS_Sharpe=lbm["OOS_Sharpe"],
                    pass_4b=bool(all(l4b.values())), pass_4b_oos=bool(all(l4bo.values())),
                    pass_4a=bool(all(l4a.values())),
                    **{f"leg_{k}": bool(v) for k, v in l4b.items()},
                    **{f"legO_{k}": bool(v) for k, v in l4bo.items()}))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    CH = ("CH_ISSHARPE", "CH_NSMALL", "CH_NMECH", "CH_NBIG")
    P("  CHOOSER SCOREBOARD (6 picks each; OOS 2017-2026 never read by any chooser):")
    P(f"  {'chooser':<14}{'medOOS_Sh':>11}{'meanOOS_Sh':>12}{'>SPY OOS':>10}"
      f"{'4b full':>9}{'4b OOS':>9}{'4a':>7}{'med N':>7}{'medOOS CAGR':>13}")
    for ch in CH:
        q = wf[wf.chooser == ch]
        P(f"  {ch:<14}{q.OOS_Sharpe.median():>11.4f}{q.OOS_Sharpe.mean():>12.4f}"
          f"{int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum()):>7}/{len(q):<2}"
          f"{int(q.pass_4b.sum()):>6}/{len(q):<2}{int(q.pass_4b_oos.sum()):>6}/{len(q):<2}"
          f"{int(q.pass_4a.sum()):>4}/{len(q):<2}{q.N.median():>7.1f}"
          f"{q.OOS_CAGR.median():>13.2%}")
    P("")
    P("  EVERY PICK:")
    for _, r in wf.iterrows():
        P(f"    {r.chooser:<13}{r.panel:<6}{r.cadence}  N={r.N:<3}H={r.H:<4} "
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
    P("  MECHANISM BOOKS ARE NOT CANDIDATES.  For reference only, the 4b base rate of the")
    P("  RANDOM-SELECTION books on the REAL tape (T_REALRAND), which is the coin flip every")
    P("  n-ladder claim is really being read against:")
    rr = syn[syn.tape == "T_REALRAND"]
    for pn in PANELS:
        q = rr[rr.panel == pn]
        P(f"    {pn:<6} 4b full {int(q.pass_4b.sum()):>4}/{len(q)} "
          f"({q.pass_4b.mean():.4f})   4b OOS {int(q.pass_4b_oos.sum()):>4}/{len(q)} "
          f"({q.pass_4b_oos.mean():.4f})")
    P("  (their benchmark is the REAL SPY, so this is directly comparable to the book's.)")
    P("")

    gdf = pd.DataFrame(gates)
    dump(gdf, "gates")
    P(f"GATES {int(gdf.pass_.sum())} of {len(gdf)} PASS")
    P(f"TOTAL RUNTIME {time.time()-t_start:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
