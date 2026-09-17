#!/usr/bin/env python3
"""Idea 1197 (lane C, 2026-09-17): is the BOOK's NULL PERCENTILE SATURATED at every
cell the record quotes it?

QUESTION. Idea 1191 found CH_PCT ties 3.80 of 4 anchors at 1.000 on U56 and 3.90 on
B136 at K=10, so the record's commonest null statistic cannot rank two books at all on
the large-cap panels, while a null-standardised z does and moves 0.1637 of OOS Sharpe
with the seed. Census the record's committed 'percentile of its own null' claims for
saturation at their own cell, and report how many were adjudicated against a statistic
pinned at its ceiling.

TWO DIALS AND NO MORE (rule 4, and the queue names both):
    dial 1 = CLAIM SET  {C_STRICT, C_PROX, C_ALL}
    dial 2 = DRAW COUNT K {10, 20, 50, 100, 200, 400}
=> 18 cells, EVERY ONE PUBLISHED (.grid.csv / .census.csv).
NOT dials, reported at every value: PANEL {U56, B136, SMALL}; ANCHOR (N, cadence) in
{(20,W),(12,W),(20,M),(10,M)}; 20 seeds at every K; the statistics {CH_PCT, CH_Z,
CH_ISSHARPE}; the 4a/4b legs; the three rule-8 choosers.

PRICE ARM. Per (panel, anchor): one REAL book (composite 12-1 + 6m + 3m percentile
ranks, above-own-200d-MA eligibility, top-N equal weight at 0.75/N of NAV, gated-out
weight to CASH, 10 bps, next-day execution) against a pool of NDRAW=400 GROSS-MATCHED
null books (at each rebalance date N names drawn uniformly from those priced that day,
weight 0.75/N). CH_PCT = share of the pool the book's IS Sharpe beats; CH_Z = the same
comparison standardised by the pool's own mean and sd. A K-draw percentile can take at
most K+1 distinct values (G4), which is the whole mechanism under test.

Deterministic: every draw comes from np.random.default_rng(SEED0 + index).
Writes .census.csv .claims.csv .grid.csv .satcells.csv .walkforward.csv .books.csv
.gates.csv and .console.txt next to this file. Modifies nothing in the repo.
"""
import sys, re, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                    # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask                            # noqa: E402

OUT       = Path(__file__).with_suffix("")
COST      = 10.0
GROSS     = 0.75
ANCHORS   = [(20, "W"), (12, "W"), (20, "M"), (10, "M")]
NDRAW     = 400
KLAD      = [10, 20, 50, 100, 200, 400]
NSEED     = 20
SEED0     = 1197
OOS_START = "2017-01-01"
IS_START  = "2009-01-01"
WARMUP    = 260

_LOG = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)

# ====================================================================== runner
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.P = np.cumprod(1.0 + self.rets, axis=0)
        self.Pprev = np.vstack([np.ones((1, self.P.shape[1])), self.P[:-1]])
        self.priced = px.notna().values
        self.seg = {}
        for f in {a[1] for a in ANCHORS}:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            s = np.flatnonzero(m)
            self.seg[f] = (s, np.append(s[1:], len(px)))
        self.i0 = WARMUP                                   # first scored row
        self.ioos = px.index.searchsorted(pd.Timestamp(OOS_START))

def run_from_starts(pan, freq, Wstart):
    """fast_backtest with targets supplied only on rebalance rows. Identical arithmetic
    to engine.backtest (gate G1)."""
    starts, ends = pan.seg[freq]
    T, M = pan.rets.shape
    held = np.zeros((T, M)); turn = np.zeros(T); cur = np.zeros(M)
    for k, (i0, i1) in enumerate(zip(starts, ends)):
        w0 = Wstart[k]
        turn[i0] = np.abs(w0 - cur).sum()
        base = pan.Pprev[i0]
        A = w0[None, :] * (pan.Pprev[i0:i1] / base[None, :])
        cash0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + cash0
        held[i0:i1] = A / V[:, None]
        Aend = w0 * (pan.P[i1 - 1] / base)
        cur = Aend / (Aend.sum() + cash0)
    return (held * pan.rets).sum(axis=1) - turn * COST / 1e4

def starts_from_weights(pan, freq, W):
    starts, _ = pan.seg[freq]
    Wv = W.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
    return Wv[starts]

def book_weights(pan, n):
    q = pan.px[pan.invest]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    elig = comp.where(q > q.rolling(200).mean())
    rk = elig.rank(axis=1, ascending=False)
    W = pd.DataFrame(0.0, index=pan.px.index, columns=pan.px.columns)
    W[pan.invest] = (rk <= n).astype(float) * (GROSS / n)
    return W

def null_starts(pan, freq, n, rng):
    """gross-matched null: same target gross, same holding count, no score."""
    starts, _ = pan.seg[freq]
    out = np.zeros((len(starts), pan.rets.shape[1]))
    for k, i in enumerate(starts):
        avail = pan.iinv[pan.priced[max(i - 1, 0)][pan.iinv]]
        if len(avail) < n:
            continue
        out[k, rng.choice(avail, size=n, replace=False)] = GROSS / n
    return out

def sharpe(r):
    v = r.std(ddof=0) * np.sqrt(252)
    return r.mean() * 252 / v if v > 0 else np.nan

def mdd(r):
    e = np.cumprod(1 + r); return float((e / np.maximum.accumulate(e) - 1).min())

def cagr(r):
    e = np.cumprod(1 + r); return float(e[-1] ** (252 / len(r)) - 1)

def trip(r):
    return dict(CAGR=cagr(r), Sharpe=float(sharpe(r)), MaxDD=mdd(r))

# ====================================================================== census
# A "percentile of its own null" claim: a NULL token and a PERCENTILE token in the same
# committed text unit; C_STRICT additionally requires a numeric percentile VALUE.
NULLTOK = re.compile(r"\b(null|coin[- ]?flip|matched[- ]null|control (?:book|basket|arm)|"
                     r"permutation|bootstrap\w*|resampl\w*|monte[- ]?carlo)\b", re.I)
PCTTOK  = re.compile(r"\b(percentile|pctile|pct|quantile|CH_PCT|p-?value|rank inside)\b", re.I)
ADJUD   = re.compile(r"\b(clears?|cleared|passe?s?|passed|fails?|failed|beats?|picks?|picked|"
                     r"chooser|verdict|KEEP|KILL|PARK|significan\w*|decisive\w*|confirms?|"
                     r"refutes?|ranks?|ranked|selects?|adjudicat\w*)\b")
# numeric percentile values: "percentile 100.0", "100th percentile", "CH_PCT 1.000",
# "percentile of 0.95", "at the 95th pct"
PCTVAL  = re.compile(
    r"(?:(?:null\s+)?(?:percentile|pctile|CH_PCT|p-?value|quantile)\s*(?:of|=|:|is|at)?\s*"
    r"(\d{1,3}(?:\.\d+)?)\s*%?)"
    r"|(?:(\d{1,3}(?:\.\d+)?)\s*(?:st|nd|rd|th)?\s*[- ]?(?:percentile|pctile))", re.I)
KTOK    = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(draws?|seeds?|resamples?|replicat\w*|"
                     r"bootstrap\w*|permutations?|paths?|simulations?|null books?|nulls?)\b", re.I)

def pct_values(txt):
    """Every quoted percentile in the unit as (value on the 0-100 scale, the resolution
    it is written to IN PERCENTAGE POINTS, the literal). A 0-1 form like '1.000' is
    read on its own scale and its resolution scaled with it."""
    out = []
    for m in PCTVAL.finditer(txt):
        raw = m.group(1) or m.group(2)
        try:
            v = float(raw)
        except ValueError:
            continue
        if v > 100:                        # not a percentile
            continue
        dec = len(raw.split(".")[1]) if "." in raw else 0
        unit01 = v <= 1.0 and dec >= 2                        # "1.000" is the ceiling
        val = v * 100.0 if unit01 else v
        res_pp = 10.0 ** (-dec) * (100.0 if unit01 else 1.0)
        out.append((val, res_pp, raw))
    return out

def units():
    U = []
    for ln in (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore").split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    n_md = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        n_md += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, n_md

def census():
    U, n_md = units()
    fileset = {}
    for src, txt in U:
        fileset.setdefault(src, False)
        if NULLTOK.search(txt) and PCTTOK.search(txt):
            fileset[src] = True
    rows = []
    for src, txt in U:
        nt, pt = bool(NULLTOK.search(txt)), bool(PCTTOK.search(txt))
        vals = pct_values(txt)
        ks = [int(m.group(1).replace(",", "")) for m in KTOK.finditer(txt)]
        sat_hi = any(abs(v - 100.0) < 1e-9 for v, _, _ in vals)
        sat_lo = any(abs(v - 0.0) < 1e-9 for v, _, _ in vals)
        # quoted resolution vs the finest a K-draw null can carry, 100/(K+1) pp
        overq = False
        if vals and ks:
            res = 100.0 / (max(ks) + 1)
            overq = any(rp < res * 0.999 for _, rp, _ in vals)
        rows.append(dict(
            src=src, n_chars=len(txt),
            C_STRICT=nt and pt and bool(vals),
            C_PROX=nt and pt,
            C_ALL=fileset[src] and (nt or pt),
            N_VALS=len(vals), STATES_K=bool(ks), K_MAX=max(ks) if ks else 0,
            SAT_CEIL=sat_hi, SAT_FLOOR=sat_lo, SAT_EITHER=sat_hi or sat_lo,
            OVERQUOTED=overq, ADJUDICATED=bool(ADJUD.search(txt)),
            VALS=";".join(f"{v:g}" for v, _, _ in vals)[:200]))
    return pd.DataFrame(rows), len(U), n_md

# ====================================================================== panels
def build_panels():
    out = []
    u = load_universe()
    out.append(("U56", u, [c for c in u.columns if c != "SPY"]))
    b = load_universe(broad=True)
    out.append(("B136", b, [c for c in b.columns if c != "SPY"]))
    s = load_universe(small=True)
    mx = s.pct_change().abs().max()
    inv = [c for c in s.columns if c != "SPY" and not (mx.get(c, 0) >= 1.0)]
    out.append(("SMALL", s, inv))
    return out

# ====================================================================== main
def main():
    t0 = time.time()
    gates = []

    say("=" * 78)
    say("(A) CENSUS — committed 'percentile of its own null' claims")
    say("=" * 78)
    cdf, nU, n_md = census()
    cdf.to_csv(f"{OUT}.census.csv", index=False)
    say(f"  corpus: {nU} committed text units "
        f"(LEADERBOARD rows {int((cdf.src == 'LEADERBOARD').sum())}, "
        f"CHANGELOG paragraphs {int((cdf.src == 'CHANGELOG').sum())}, {n_md} markdown artefacts)")
    crows = []
    for cs in ["C_STRICT", "C_PROX", "C_ALL"]:
        sub = cdf[cdf[cs]]
        n = len(sub)
        d = dict(CLAIM_SET=cs, N=n,
                 SAT_CEIL=int(sub.SAT_CEIL.sum()), SAT_ANY=int(sub.SAT_EITHER.sum()),
                 STATES_K=int(sub.STATES_K.sum()), ADJUD=int(sub.ADJUDICATED.sum()),
                 ADJUD_AND_SAT=int((sub.ADJUDICATED & sub.SAT_CEIL).sum()),
                 ADJUD_NO_K=int((sub.ADJUDICATED & ~sub.STATES_K).sum()),
                 OVERQUOTED=int(sub.OVERQUOTED.sum()))
        for k in ["SAT_CEIL", "SAT_ANY", "STATES_K", "ADJUD", "ADJUD_AND_SAT", "ADJUD_NO_K"]:
            d[k + "_share"] = d[k] / n if n else np.nan
        crows.append(d)
        say(f"  {cs:9s} n={n:6d}  ceiling-quoted {d['SAT_CEIL']:5d} ({d['SAT_CEIL_share']:.4f})  "
            f"states draw count {d['STATES_K']:5d} ({d['STATES_K_share']:.4f})  "
            f"adjudicated {d['ADJUD']:5d}  ADJUDICATED AT THE CEILING {d['ADJUD_AND_SAT']:5d} "
            f"({d['ADJUD_AND_SAT_share']:.4f})  adjudicated with NO draw count {d['ADJUD_NO_K']:5d}")
    pd.DataFrame(crows).to_csv(f"{OUT}.claims.csv", index=False)
    gates.append(dict(gate="G6 census sets nest C_STRICT<=C_PROX<=C_ALL",
                      value=float((cdf.C_STRICT & ~cdf.C_PROX).sum() + (cdf.C_PROX & ~cdf.C_ALL).sum()),
                      target=0.0, pass_=bool(((cdf.C_STRICT & ~cdf.C_PROX).sum() +
                                              (cdf.C_PROX & ~cdf.C_ALL).sum()) == 0)))

    # ------------------------------------------------------------- price arm
    say("")
    say("=" * 78)
    say("(B) RE-PRICING — 12 books, 4,800 gross-matched null backtests")
    say("=" * 78)
    panels = build_panels()
    grid, books, satcells, wf = [], [], [], []

    for pname, px, invest in panels:
        pan = Panel(pname, px, invest)
        spy = px["SPY"].pct_change().fillna(0.0).values
        i0, ioos = pan.i0, pan.ioos
        s_full, s_is, s_oos = spy[i0:], spy[i0:ioos], spy[ioos:]
        base_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        b_full, b_oos = base_r[i0:], base_r[ioos:]
        h = len(s_full) // 2
        spyT, baseT = trip(s_full), trip(b_full)
        spyH = (float(sharpe(s_full[:h])), float(sharpe(s_full[h:])))
        say(f"  {pname}: SPY {spyT['CAGR']:.2%} / {spyT['Sharpe']:.4f} / {spyT['MaxDD']:.2%} "
            f"(halves {spyH[0]:.4f}/{spyH[1]:.4f}), OOS {cagr(s_oos):.2%} / {sharpe(s_oos):.4f}; "
            f"LIVE v2 {baseT['CAGR']:.2%} / {baseT['Sharpe']:.4f} / {baseT['MaxDD']:.2%}, "
            f"OOS {cagr(b_oos):.2%} / {sharpe(b_oos):.4f}")
        if pname == "U56":
            gates.append(dict(gate="G3 live RULES v2 U56 MaxDD == record -12.05%",
                              value=baseT["MaxDD"], target=-0.1205,
                              pass_=abs(baseT["MaxDD"] + 0.1205) < 5e-4))

        for ai, (n, freq) in enumerate(ANCHORS):
            cell = 1000 * ([p[0] for p in panels].index(pname) + 1) + ai   # deterministic
            W = book_weights(pan, n)
            r = run_from_starts(pan, freq, starts_from_weights(pan, freq, W))
            if pname == "U56" and (n, freq) == ANCHORS[0]:
                eng = backtest(px, W, cost_bps=COST, freq=freq)["returns"].values
                d = float(np.nanmax(np.abs(np.asarray(eng[i0:], float) - r[i0:])))
                gates.append(dict(gate="G1 fast runner == engine.backtest (post-warm-up)",
                                  value=d, target=0.0, pass_=d < 1e-12))
            rf, ris, ros = r[i0:], r[i0:ioos], r[ioos:]
            bt, half1, half2 = trip(rf), float(sharpe(rf[:h])), float(sharpe(rf[h:]))
            # 4a vs live RULES v2, 4b vs SPY
            k4a = (half1 > float(sharpe(b_full[:h])) and half2 > float(sharpe(b_full[h:]))
                   and bt["MaxDD"] >= baseT["MaxDD"])
            k4b = (half1 > spyH[0] and half2 > spyH[1] and float(sharpe(ros)) > float(sharpe(s_oos))
                   and bt["MaxDD"] >= 0.60 * spyT["MaxDD"] and bt["CAGR"] >= 0.70 * spyT["CAGR"])

            # null pool
            nsh_is = np.empty(NDRAW); nsh_full = np.empty(NDRAW)
            for d_ in range(NDRAW):
                rng = np.random.default_rng(SEED0 + 100003 * cell + d_)
                nr = run_from_starts(pan, freq, null_starts(pan, freq, n, rng))
                nsh_is[d_] = sharpe(nr[i0:ioos]); nsh_full[d_] = sharpe(nr[i0:])
            books.append(dict(panel=pname, N=n, cadence=freq, **bt, H1=half1, H2=half2,
                              IS_Sharpe=float(sharpe(ris)), OOS_CAGR=cagr(ros),
                              OOS_Sharpe=float(sharpe(ros)), OOS_MaxDD=mdd(ros),
                              KEEP_4a=k4a, KEEP_4b=k4b,
                              null_is_mean=float(nsh_is.mean()), null_is_sd=float(nsh_is.std(ddof=1)),
                              null_is_max=float(nsh_is.max())))

            for K in KLAD:
                for sd in range(NSEED):
                    rs = np.random.default_rng(SEED0 + 7919 * K + sd)
                    idx = rs.choice(NDRAW, size=K, replace=False)
                    pool = nsh_is[idx]
                    pct = float((pool < float(sharpe(ris))).mean())
                    z = float((float(sharpe(ris)) - pool.mean()) / pool.std(ddof=1))
                    grid.append(dict(panel=pname, N=n, cadence=freq, K=K, seed=sd,
                                     CH_PCT=pct, CH_Z=z, SATURATED=bool(pct >= 1.0 - 1e-12),
                                     pool_mean=float(pool.mean()), pool_sd=float(pool.std(ddof=1))))
        say(f"    {pname} done  t={time.time()-t0:.0f}s")

    gdf = pd.DataFrame(grid); bdf = pd.DataFrame(books)
    gdf.to_csv(f"{OUT}.grid.csv", index=False); bdf.to_csv(f"{OUT}.books.csv", index=False)

    # ------------------------------------- saturation: the headline of arm (B)
    say("")
    say("  SATURATION of CH_PCT (share of (anchor,seed) cells pinned at 1.000):")
    for pname in [p[0] for p in panels]:
        row = []
        for K in KLAD:
            s = gdf[(gdf.panel == pname) & (gdf.K == K)].SATURATED.mean()
            row.append(f"K={K}:{s:.3f}")
        say(f"    {pname:6s} " + "  ".join(row))
    say("  ANCHORS TIED AT THE MAXIMUM of CH_PCT, of 4 (mean over 20 seeds) — 1191's statistic:")
    for pname in [p[0] for p in panels]:
        row = []
        for K in KLAD:
            sub = gdf[(gdf.panel == pname) & (gdf.K == K)]
            ties = [(g.CH_PCT == g.CH_PCT.max()).sum() for _, g in sub.groupby("seed")]
            zt = [(g.CH_Z == g.CH_Z.max()).sum() for _, g in sub.groupby("seed")]
            row.append(f"K={K}:{np.mean(ties):.2f}/{np.mean(zt):.2f}")
            satcells.append(dict(panel=pname, K=K, tied_PCT=float(np.mean(ties)),
                                 tied_Z=float(np.mean(zt)),
                                 sat_share=float(sub.SATURATED.mean()),
                                 distinct_PCT=int(sub.CH_PCT.nunique()),
                                 distinct_Z=int(sub.CH_Z.nunique())))
        say(f"    {pname:6s} PCT/Z  " + "  ".join(row))
    pd.DataFrame(satcells).to_csv(f"{OUT}.satcells.csv", index=False)
    # G4: a K-draw percentile can take at most K+1 distinct values
    bad = sum(1 for K in KLAD if gdf[gdf.K == K].CH_PCT.nunique() > K + 1)
    gates.append(dict(gate="G4 CH_PCT distinct values <= K+1 at every rung", value=float(bad),
                      target=0.0, pass_=bad == 0))
    # G5: CH_Z never saturates (no two cells tie at its maximum by construction)
    tz = float(np.mean([(g.CH_Z == g.CH_Z.max()).sum() for _, g in gdf.groupby(["panel", "K", "seed"])]))
    gates.append(dict(gate="G5 CH_Z mean anchors tied at max == 1.0 (no ceiling)",
                      value=tz, target=1.0, pass_=abs(tz - 1.0) < 1e-9))
    # G7: the null is gross-matched
    pan0 = Panel(*panels[0]); st = null_starts(pan0, "W", 20, np.random.default_rng(0))
    gmax = float(np.abs(st.sum(axis=1) - GROSS).max())
    gates.append(dict(gate="G7 null target gross == 0.75 at every rebalance row",
                      value=gmax, target=0.0, pass_=gmax < 1e-12))
    # G2 determinism
    r1 = run_from_starts(pan0, "W", null_starts(pan0, "W", 20, np.random.default_rng(5)))
    r2 = run_from_starts(pan0, "W", null_starts(pan0, "W", 20, np.random.default_rng(5)))
    gates.append(dict(gate="G2 determinism", value=float(np.abs(r1 - r2).max()), target=0.0,
                      pass_=float(np.abs(r1 - r2).max()) == 0.0))

    # ------------------------------------------------- (C) rule 8 walk-forward
    say("")
    say("=" * 78)
    say("(C) RULE 8 WALK-FORWARD — anchor chosen on 2009-2016 ONLY, 2017-2026 read ONCE")
    say("=" * 78)
    for pname, px, invest in panels:
        pan = Panel(pname, px, invest)
        i0, ioos = pan.i0, pan.ioos
        spy = px["SPY"].pct_change().fillna(0.0).values
        base_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        sb = bdf[bdf.panel == pname].reset_index(drop=True)
        for K in KLAD:
            for chooser in ["CH_PCT", "CH_Z", "CH_ISSHARPE"]:
                pl = []
                for sd in range(NSEED):
                    if chooser == "CH_ISSHARPE":
                        j = int(sb.IS_Sharpe.idxmax())
                    else:
                        sub = gdf[(gdf.panel == pname) & (gdf.K == K) & (gdf.seed == sd)]
                        key = sub.sort_values(["N", "cadence"]).reset_index(drop=True)
                        m = key[chooser].max()
                        w = key[key[chooser] == m].iloc[0]        # FIRST-WINS, deterministic
                        j = int(sb[(sb.N == w.N) & (sb.cadence == w.cadence)].index[0])
                    pl.append(j)
                    if chooser == "CH_ISSHARPE":
                        break
                picks = sorted(set(pl))
                modal = max(picks, key=lambda x: (pl.count(x), -x))   # ties -> lowest index
                row = sb.loc[modal]
                spread = np.nan
                if len(picks) > 1:
                    spread = float(sb.loc[picks].OOS_Sharpe.max() - sb.loc[picks].OOS_Sharpe.min())
                wf.append(dict(panel=pname, K=K, chooser=chooser, n_distinct=len(picks),
                               modal_share=pl.count(modal) / len(pl),
                               pick=f"N={int(row.N)}/{row.cadence}", OOS_CAGR=row.OOS_CAGR,
                               OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
                               OOS_spread_over_seeds=spread,
                               SPY_OOS_Sharpe=float(sharpe(spy[ioos:])),
                               LIVE_OOS_Sharpe=float(sharpe(base_r[ioos:])),
                               KEEP_4a=bool(row.KEEP_4a), KEEP_4b=bool(row.KEEP_4b)))
    wdf = pd.DataFrame(wf); wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    for pname in [p[0] for p in panels]:
        for chooser in ["CH_PCT", "CH_Z", "CH_ISSHARPE"]:
            sub = wdf[(wdf.panel == pname) & (wdf.chooser == chooser)]
            say(f"  {pname:6s} {chooser:11s} distinct picks over 20 seeds by K: "
                + " ".join(f"{int(r.K)}:{int(r.n_distinct)}" for _, r in sub.iterrows())
                + f" | modal pick @K=10 {sub.iloc[0]['pick']} OOS {sub.iloc[0].OOS_CAGR:.2%}/"
                  f"{sub.iloc[0].OOS_Sharpe:.4f}/{sub.iloc[0].OOS_MaxDD:.2%}"
                + (f" | max OOS-Sharpe spread over seeds {np.nanmax(sub.OOS_spread_over_seeds):.4f}"
                   if sub.n_distinct.max() > 1 else " | seed CANNOT move it"))

    say("")
    say(f"  4b full AND OOS: {int(bdf.KEEP_4b.sum())} of {len(bdf)} books;  "
        f"4a: {int(bdf.KEEP_4a.sum())} of {len(bdf)}")
    for _, r in bdf[bdf.KEEP_4b].iterrows():
        say(f"    4b PASS  {r.panel} N={int(r.N)}/{r.cadence}: {r.CAGR:.2%} / {r.Sharpe:.4f} / "
            f"{r.MaxDD:.2%}, halves {r.H1:.3f}/{r.H2:.3f}, OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f}")
    say(f"  rule-8 picks clearing 4b: {int(wdf.KEEP_4b.sum())} of {len(wdf)};  "
        f"4a: {int(wdf.KEEP_4a.sum())} of {len(wdf)}")

    say("")
    say("=" * 78); say("GATES"); say("=" * 78)
    gdf2 = pd.DataFrame(gates); gdf2.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gdf2.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate}: {g.value:.6g} (target {g.target:g})")
    say(f"  {int(gdf2.pass_.sum())} of {len(gdf2)} gates pass.  total {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")

if __name__ == "__main__":
    main()
