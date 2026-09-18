#!/usr/bin/env python3
"""
Idea 904 (lane B, 2026-09-18) — which committed PLACEBO numbers are BELOW their own SEED FLOOR?

THE QUESTION AS FILED.  Idea 885 published the arithmetic: a per-arm MEDIAN over S seeds has
SE ~ 1.2533*sigma/sqrt(S), so a null-minus-BLOCK median over 1,152 arms resolves to about
+/-0.0008 of Sharpe at 20 seeds.  904 asks the record to be censused against that floor: how
many committed placebo-differenced numbers are INSIDE the resolution their own (arm, seed)
counts buy?

WHY THIS RUN ALSO PRICES A BOOK.  Four lanes skipped 904 as "a census, no price leg".  Lane B's
own idea 1265 overturned that premise: a census CAN carry a capital arm.  The capital question
sitting underneath 904 is sharp and has never been asked —

    a placebo-differenced statistic is a SELECTOR.  Does subtracting a gross-matched null
    before choosing a book buy anything OUT OF SAMPLE, and does the answer depend on whether
    the subtraction clears its own seed floor?

If the record's sub-floor numbers are noise, then a chooser built on them should be no better
than the raw IS-Sharpe chooser, and GATING the chooser on k x floor should be worth nothing.
That is a falsifiable capital claim, and this run measures it on real books.

THE OBJECT (frozen, the record's committed family).  24 real candidate books per panel:

    N  {5, 10, 15, 20, 25, 30}     x     H  {21, 63, 126, 252}

min-hold selection on the RULES-v1 composite rank key, eligibility `above 200d MA & vol20 <
0.60`, GROSS 0.75, WEEKLY, 10 bps, t+1 (PROTOCOL rule 2).  N=20 / H=126 is the record's frozen
anchor (idea 1323).  Nothing in the book family is tuned here — the family is the record's.

THE NULL (gross-matched RAND, the record's standard).  For arm a and seed s, the SAME (N, H)
min-hold machine with the composite rank key replaced by a fresh uniform draw at every
rebalance row: same N, same H, same eligibility gate, same gross, same costs, same days.  Only
the ORDERING is randomised, so the contrast isolates the signal and nothing else.

THE STATISTIC.       X_a(S) = Sharpe_IS(a) - median_{s<=S} Sharpe_IS(null_{a,s})
THE FLOOR (885's).   F_a(S) = 1.2533 * sigma_a / sqrt(S),  sigma_a = sd of that arm's null
                     Sharpes across ALL S_MAX=50 seeds.  sigma is estimated ONCE at S_MAX so the
                     floor is not itself a noisy quantity; this is declared, not discovered.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names "claim set, floor multiple"):

    S  {5, 10, 20, 50}        DIAL 1 — seed budget
    k  {0.0, 0.5, 1.0, 2.0}   DIAL 2 — floor multiple (the LICENSING GATE)

    CHOOSER: among the 24 arms keep those with X_a(S) >= k * F_a(S); pick argmax X_a(S).  If
    the gate licenses nothing, fall back to the raw IS-Sharpe argmax (declared in advance, and
    the fallback count is published per cell).  16 cells x 3 panels = 48 cells, ALL published.

    The chooser reads IS rows ONLY (warm-up .. 2016-12-31).  2017-2026 is therefore untouched
    by construction and every cell's OOS triple is an honest rule-8 read.  Rule 8 is ALSO run
    in its strict form: (S, k) picked on IS by argmax IS Sharpe of the selected book, 2017-2026
    read ONCE for that pick.

COMPARANDS AT EVERY CELL: the RAW IS-Sharpe chooser (no placebo subtraction — the comparand
that decides whether placebo-differencing is worth anything), the FROZEN N=20/H=126 anchor, the
no-choice GRIDAVG (equal blend of all 24 arms, idea 1331's book), the live RULES v2 baseline
and SPY.  Both KEEP paths at every cell.

THE CENSUS LEG (904's literal ask), run alongside and reported separately: a MECHANICAL harvest
of committed placebo-differenced numbers from the record's markdown, each scored against the
floor implied by ITS OWN stated seed and arm counts, at the same k ladder.  The harvest rule is
stated in `census()` and its recall limits are published, not hidden.

PROTOCOL: rule 1 (>=10y, gate G0); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3
(compare vs live RULES v2 AND SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters);
rule 8 (walk-forward, 2017-2026 read once); rule 9 (survivorship stated).  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56, B136 and SMALL are CURRENT-constituent lists, so every absolute
level is an upper bound.  The headline here is a DIFFERENCE between choosers built from the
SAME names on the SAME days, so it is first-order immune; any 4b pass count is not.

Runs standalone and offline (committed caches only; no network):
  python research/backtests/2026-09-18_which-committed-PLACEBO-numbers-are-BELOW-their-own-SEED-FLOOR_B.py
"""
from __future__ import annotations

import hashlib
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE = "2026-09-18"
SLUG = "which-committed-PLACEBO-numbers-are-BELOW-their-own-SEED-FLOOR"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL, COST = 260, 0.60, 10.0
GROSS, CADENCE = 0.75, "W"
NS = [5, 10, 15, 20, 25, 30]
HS = [21, 63, 126, 252]
ANCHOR = (20, 126)
S_LADDER = [5, 10, 20, 50]          # DIAL 1
K_LADDER = [0.0, 0.5, 1.0, 2.0]     # DIAL 2
S_MAX = max(S_LADDER)
MED_SE = 1.2533                     # asymptotic SE multiplier of a median (885's constant)
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}  (target {target})")


# ---------------------------------------------------------------- mechanics (baseline's, copied)
def mech(q):
    """RULES-v1 composite rank key + eligibility, exactly as research/baseline.py:score()."""
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)   # ascending = best first
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def build(pan, N, H, key=None, rand=None, stop=None):
    """Min-hold selection frame at GROSS=1.0 (rule 2: the selection row is t-1, applied at t).

    key=None  -> the record's composite rank key (a REAL arm).
    rand      -> (n_reb x K) uniform draws; the arm's ordering is replaced by the draw (the
                 gross-matched RAND null).  Everything else — N, H, eligibility, gross, days,
                 costs — is identical to the real arm, so the contrast isolates the ORDERING.
    stop      -> last row built (None = full sample).  Used to build IS-only null frames.
    """
    reb = pan.reb if stop is None else pan.reb[pan.reb < stop]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - 1, 0)                                    # rule 2: nothing at or after t
        ok = pan.elig[ts] & pr[ts]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = (pan.rank_key[ts] if rand is None else rand[i]).astype(float).copy()
            k[~ok] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop_i = reb[i + 1] if i + 1 < len(reb) else (stop if stop is not None else T)
            W[t:stop_i, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, frame, g=GROSS, stop=None):
    """Constant-gross runner (the record's).  Returns (gross returns, turnover)."""
    rets = pan.rets
    T, M = rets.shape
    end = T if stop is None else stop
    reb = np.asarray([r for r in pan.reb if r < end], dtype=np.int64)
    ends = np.append(reb[1:], end)
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = pan.Cp[i0]
        A = w0[None, :] * (pan.Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (pan.C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn


def at_cost(gr, tu, c=COST):
    return gr - tu * c / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a vs the LIVE rules; 4b vs SPY (PROTOCOL rule 4, both paths, every leg published)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(L_H1=bool(h1 > bm["H1"]), L_H2=bool(h2 > bm["H2"]),
                L_DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                L_CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- the census leg (904's literal ask)
CUES = {
    "NARROW": re.compile(r"placebo|null[- ]minus|minus[- ]BLOCK|gross-matched null|"
                         r"excess over (the )?null|null excess", re.I),
    "WIDE": re.compile(r"placebo|null[- ]minus|minus[- ]?(BLOCK|RAND|SWITCH|UG)|gross-matched null|"
                       r"null excess|excess over (the )?null|null-differenc|matched null", re.I),
}
NUM = re.compile(r"[+-]?\d+\.\d{4,}")
SEEDS = re.compile(r"(\d{1,4})\s*(?:md5\s*)?seeds?\b", re.I)
ARMS = re.compile(r"(\d[\d,]{0,8})\s*arms?\b", re.I)


def census(sigma_hat):
    """MECHANICAL harvest, stated in full so its RECALL is auditable rather than assumed.

    POPULATION: the record's RESULT files only — research/backtests/*.md and
    research/CHANGELOG.md.  LEADERBOARD.md and QUEUE.md are EXCLUDED by declaration: they are
    index and agenda files whose 4-dp numbers are Sharpe LEVELS, and including them turns the
    harvest into a level census.  The exclusion is stated, not silent.

    FUNNEL (published in full, because the funnel IS most of the answer):
        cued sentences -> those carrying a >= 4-dp decimal -> those whose |x| < 0.1 (a Sharpe
        DIFFERENCE, an order of magnitude below a Sharpe LEVEL, which the same sentences also
        carry) -> those STAMPED with both a seed count and an arm count.

    CLAIM SETS, both reported, never one (the queue names "claim set" as a dial):
        NARROW  the placebo / null-minus vocabulary idea 885 itself used;
        WIDE    NARROW plus matched-null, RAND/SWITCH/UG-minus and null-difference wordings.
    Within each, the EXPLICIT-SIGN subset (the record's own typography for a difference) is
    reported too.

    (S, A) are read from the sentence first, then from the SAME file (first match).  Missing
    either is UNSTAMPED and is reported, never imputed.

    FLOOR (idea 885's arithmetic, a per-arm median aggregated over A arms):
        floor(S, A) = MED_SE * sigma / sqrt(S * A)
    sigma is NOT 885's quoted 0.067; it is THIS RUN's MEASURED per-arm null dispersion
    (`sigma_hat`) — the one input to the floor the record never measured.
    """
    files = sorted(list((ROOT / "research" / "backtests").glob("*.md"))
                   + [ROOT / "research" / "CHANGELOG.md"])
    rows, funnel = [], []
    for cue_name, cue in CUES.items():
        n_sent = n_num = 0
        for f in files:
            try:
                txt = f.read_text(errors="ignore")
            except Exception:
                continue
            fS, fA = SEEDS.search(txt), ARMS.search(txt)
            for sent in re.split(r"(?<=[.;:])\s+|\n", txt):
                if not cue.search(sent):
                    continue
                n_sent += 1
                nums = NUM.findall(sent)
                if not nums:
                    continue
                n_num += 1
                sS, sA = SEEDS.search(sent), ARMS.search(sent)
                S = int((sS or fS).group(1)) if (sS or fS) else None
                A = int((sA or fA).group(1).replace(",", "")) if (sA or fA) else None
                for x in nums:
                    v = float(x)
                    if abs(v) >= 0.1:            # a Sharpe LEVEL, not a difference
                        continue
                    rows.append(dict(cueset=cue_name, file=f.name, S=S, A=A, value=v,
                                     signed=x[0] in "+-",
                                     S_from="sentence" if sS else ("file" if fS else "none"),
                                     A_from="sentence" if sA else ("file" if fA else "none"),
                                     stamped=bool(S is not None and A is not None),
                                     sentence=sent.strip()[:240]))
        funnel.append(dict(cueset=cue_name, cued_sentences=n_sent, with_4dp_number=n_num))
    df = pd.DataFrame(rows)
    fn = pd.DataFrame(funnel)
    if len(df):
        df["floor"] = np.where(df["stamped"],
                               MED_SE * sigma_hat / np.sqrt(df["S"].fillna(1) * df["A"].fillna(1)),
                               np.nan)
        for k in K_LADDER:
            if k == 0.0:
                continue
            df[f"below_k{k}"] = df["stamped"] & (df["value"].abs() < k * df["floor"])
        fn = fn.merge(df.groupby("cueset").agg(differences=("value", "size"),
                                               stamped=("stamped", "sum"),
                                               files=("file", "nunique")).reset_index(),
                      on="cueset", how="left")
    return df, fn


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 112)
    say("IDEA 904 (lane B, 2026-09-18) — which committed PLACEBO numbers are BELOW their own SEED FLOOR?")
    say("CAPITAL ARM: is a PLACEBO-DIFFERENCED chooser, gated on its own seed floor, worth")
    say("             anything OUT OF SAMPLE against the RAW IS-Sharpe chooser?")
    say(f"DIALS: S {S_LADDER} x k {K_LADDER}.  Book family frozen: N {NS} x H {HS}, "
        f"gross {GROSS}, {CADENCE}, {COST:.0f} bps, t+1.")
    say("=" * 112)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    mv = pxS.pct_change().abs().max()
    invS = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0 -> {len(invS)} investables.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, invS)]
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y), {len(p.reb)} weekly rebalances, {len(p.iinv)} investables")
    gate("G0 min sample >= 10 years (rule 1)", f"{min(len(p.idx) for p in panels)/252:.1f}y",
         ">= 10.0y", min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    arms = [(n, h) for n in NS for h in HS]
    grid_rows, cell_rows, null_rows, wf_rows = [], [], [], []
    sigma_all = []

    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy_f, spy_o = pan.spy[WARMUP:], pan.spy[i_oos:]
        liveres = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq=CADENCE)
        live_f = liveres["returns"].values[WARMUP:]
        live_o = liveres["returns"].values[i_oos:]
        bm, lv = bmpack(spy_f), bmpack(live_f)
        bmO, lvO = bmpack(spy_o), bmpack(live_o)
        say(f"\n  [{pan.name}] SPY full {bm['CAGR']:.2%}/{bm['Sharpe']:.4f}/{bm['MaxDD']:.2%}  "
            f"-> 4b caps DD {DD_CAP*bm['MaxDD']:.2%}, CAGR {CAGR_FLOOR*bm['CAGR']:.2%};  "
            f"RULES v2 live {lv['CAGR']:.2%}/{lv['Sharpe']:.4f}/{lv['MaxDD']:.2%}")
        say(f"  [{pan.name}] OOS SPY {bmO['CAGR']:.2%}/{bmO['Sharpe']:.4f}/{bmO['MaxDD']:.2%};  "
            f"OOS RULES v2 {lvO['CAGR']:.2%}/{lvO['Sharpe']:.4f}/{lvO['MaxDD']:.2%}")

        # ---- real arms: full sample once, IS Sharpe for the chooser
        real = {}
        for (n, h) in arms:
            W = build(pan, n, h)
            gr, tu = run(pan, W)
            r = at_cost(gr, tu)
            real[(n, h)] = dict(r_full=r[WARMUP:], r_oos=r[i_oos:],
                                is_sharpe=sharpe(r[WARMUP:i_oos]), turn=tu)
            grid_rows.append(dict(panel=pan.name, N=n, H=h, IS_Sharpe=real[(n, h)]["is_sharpe"],
                                  **{f"full_{k}": v for k, v in triple(r[WARMUP:]).items()},
                                  **{f"oos_{k}": v for k, v in triple(r[i_oos:]).items()}))
        say(f"  [{pan.name}] 24 real arms built in {time.time()-t0:.0f}s")

        # ---- nulls: S_MAX seeds per arm, IS window only (the chooser never sees OOS rows)
        K = len(pan.iinv)
        n_reb_is = int(np.sum(pan.reb < i_oos))
        null_S = {}
        for (n, h) in arms:
            vals = np.empty(S_MAX)
            for s in range(S_MAX):
                sd = int(hashlib.md5(f"{pan.name}|{n}|{h}|{s}".encode()).hexdigest()[:8], 16)  # md5: reproducible across runs
                rng = np.random.default_rng(sd)
                rand = rng.random((n_reb_is, K))
                Wn = build(pan, n, h, rand=rand, stop=i_oos)
                grn, tun = run(pan, Wn, stop=i_oos)
                vals[s] = sharpe(at_cost(grn, tun)[WARMUP:i_oos])
            null_S[(n, h)] = vals
            null_rows.append(dict(panel=pan.name, N=n, H=h, null_mean=float(np.mean(vals)),
                                  null_median50=float(np.median(vals)), null_sd=float(np.std(vals, ddof=1)),
                                  real_IS=real[(n, h)]["is_sharpe"],
                                  excess50=float(real[(n, h)]["is_sharpe"] - np.median(vals))))
            sigma_all.append(float(np.std(vals, ddof=1)))
        say(f"  [{pan.name}] {len(arms)*S_MAX} null books done at {time.time()-t0:.0f}s")

        sigma = {a: float(np.std(null_S[a], ddof=1)) for a in arms}

        # ---- comparands
        raw_pick = max(arms, key=lambda a: real[a]["is_sharpe"])
        gridavg_f = np.mean([real[a]["r_full"] for a in arms], axis=0)
        gridavg_o = np.mean([real[a]["r_oos"] for a in arms], axis=0)
        for nm, rf, ro in [("RAW-IS-Sharpe-chooser", real[raw_pick]["r_full"], real[raw_pick]["r_oos"]),
                           ("FROZEN-anchor-N20H126", real[ANCHOR]["r_full"], real[ANCHOR]["r_oos"]),
                           ("GRIDAVG-no-choice", gridavg_f, gridavg_o)]:
            a4, b4, m, h1, h2, legs = keep_paths(rf, bm, lv)
            a4o, b4o, mo, h1o, h2o, legso = keep_paths(ro, bmO, lvO)
            cell_rows.append(dict(panel=pan.name, S=np.nan, k=np.nan, kind=nm,
                                  pick=str(raw_pick if nm.startswith("RAW") else
                                           (ANCHOR if nm.startswith("FROZEN") else "all24")),
                                  n_licensed=np.nan, fell_back=np.nan,
                                  full_CAGR=m["CAGR"], full_Sharpe=m["Sharpe"], full_MaxDD=m["MaxDD"],
                                  H1=h1, H2=h2, keep4a=a4, keep4b=b4, **legs,
                                  oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                                  oos_keep4a=a4o, oos_keep4b=b4o,
                                  **{f"oos_{k}": v for k, v in legso.items()}))

        # ---- the 16 dial cells
        for S in S_LADDER:
            med = {a: float(np.median(null_S[a][:S])) for a in arms}
            X = {a: real[a]["is_sharpe"] - med[a] for a in arms}
            F = {a: MED_SE * sigma[a] / np.sqrt(S) for a in arms}
            for k in K_LADDER:
                lic = [a for a in arms if X[a] >= k * F[a]]
                fell = len(lic) == 0
                pick = raw_pick if fell else max(lic, key=lambda a: X[a])
                rf, ro = real[pick]["r_full"], real[pick]["r_oos"]
                a4, b4, m, h1, h2, legs = keep_paths(rf, bm, lv)
                a4o, b4o, mo, h1o, h2o, legso = keep_paths(ro, bmO, lvO)
                cell_rows.append(dict(panel=pan.name, S=S, k=k, kind="PLACEBO-chooser",
                                      pick=str(pick), n_licensed=len(lic), fell_back=fell,
                                      full_CAGR=m["CAGR"], full_Sharpe=m["Sharpe"], full_MaxDD=m["MaxDD"],
                                      H1=h1, H2=h2, keep4a=a4, keep4b=b4, **legs,
                                      oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                                      oos_keep4a=a4o, oos_keep4b=b4o,
                                      **{f"oos_{kk}": v for kk, v in legso.items()},
                                      is_Sharpe_sel=real[pick]["is_sharpe"],
                                      X_sel=X[pick], F_sel=F[pick],
                                      n_below_floor=int(sum(1 for a in arms if abs(X[a]) < F[a]))))

        # ---- rule 8 strict: (S, k) picked on IS by argmax IS Sharpe of the selected book
        cand = [c for c in cell_rows if c["panel"] == pan.name and c["kind"] == "PLACEBO-chooser"]
        best = max(cand, key=lambda c: c["is_Sharpe_sel"])
        wf_rows.append(dict(panel=pan.name, chosen_S=best["S"], chosen_k=best["k"],
                            pick=best["pick"], IS_Sharpe=best["is_Sharpe_sel"],
                            oos_CAGR=best["oos_CAGR"], oos_Sharpe=best["oos_Sharpe"],
                            oos_MaxDD=best["oos_MaxDD"], oos_keep4a=best["oos_keep4a"],
                            oos_keep4b=best["oos_keep4b"],
                            spy_oos_CAGR=bmO["CAGR"], spy_oos_Sharpe=bmO["Sharpe"], spy_oos_MaxDD=bmO["MaxDD"],
                            live_oos_CAGR=lvO["CAGR"], live_oos_Sharpe=lvO["Sharpe"], live_oos_MaxDD=lvO["MaxDD"],
                            raw_oos_Sharpe=triple(real[raw_pick]["r_oos"])["Sharpe"],
                            anchor_oos_Sharpe=triple(real[ANCHOR]["r_oos"])["Sharpe"],
                            gridavg_oos_Sharpe=triple(gridavg_o)["Sharpe"]))

    grid = pd.DataFrame(grid_rows)
    cells = pd.DataFrame(cell_rows)
    nulls = pd.DataFrame(null_rows)
    wf = pd.DataFrame(wf_rows)

    sigma_hat = float(np.mean(sigma_all))
    gate("G1 the null is GROSS-MATCHED (same N, H, gate, gross, days — only the ORDERING differs)",
         "build(rand=...) shares every argument with the real arm", "by construction", True)
    gate("G2 the chooser reads NO row at or after 2017-01-01 (rule 8)",
         "null frames built with stop=i_oos; X uses r[WARMUP:i_oos] only", "0 OOS rows read", True)
    gate("G3 measured per-arm null dispersion sigma_hat vs 885's quoted 0.067",
         f"{sigma_hat:.4f}", "reported, not assumed", True)
    gate("G4 every dial cell published", f"{int((cells['kind']=='PLACEBO-chooser').sum())} cells",
         f"{len(S_LADDER)*len(K_LADDER)*3} = 48", int((cells['kind'] == 'PLACEBO-chooser').sum()) == 48)
    gate("G5 exactly 2 tuned parameters (rule 4)", "S, k", "<= 2", True)

    # ---------------- the placebo excess, and how much of it is resolvable
    say("\n" + "=" * 112)
    say("THE MEASUREMENT — is the placebo excess resolvable at all at the record's seed budgets?")
    say("=" * 112)
    say(f"  measured per-arm null-Sharpe dispersion sigma_hat = {sigma_hat:.4f} "
        f"(885 assumed 0.067); per-arm floor = {MED_SE:.4f}*sigma/sqrt(S)")
    for S in S_LADDER:
        f_typ = MED_SE * sigma_hat / np.sqrt(S)
        sub = nulls.assign(exc=lambda d: d["real_IS"] - d["null_median50"])
        say(f"    S={S:3d}: typical per-arm floor {f_typ:.4f} of Sharpe; "
            f"arms whose |excess| < floor: "
            + ", ".join(f"{p} {int((cells[(cells.panel==p)&(cells.S==S)].n_below_floor.iloc[0]))}/{len(arms)}"
                        for p in ["U56", "B136", "SMALL"]))
    say("\n  per-panel mean placebo excess (real IS Sharpe - null median, 50 seeds):")
    for p in ["U56", "B136", "SMALL"]:
        d = nulls[nulls.panel == p]
        say(f"    {p:6s} mean {d.excess50.mean():+.4f}  min {d.excess50.min():+.4f}  "
            f"max {d.excess50.max():+.4f}  mean null sd {d.null_sd.mean():.4f}")

    # ---------------- the capital answer
    say("\n" + "=" * 112)
    say("THE CAPITAL ANSWER — 48 dial cells + 3 comparands per panel, ALL published")
    say("=" * 112)
    for p in ["U56", "B136", "SMALL"]:
        d = cells[cells.panel == p]
        cm = d[d.kind != "PLACEBO-chooser"]
        say(f"\n  [{p}] comparands")
        for _, r in cm.iterrows():
            say(f"    {r['kind']:24s} pick {r['pick']:12s} full {r.full_CAGR:7.2%}/{r.full_Sharpe:.4f}/"
                f"{r.full_MaxDD:7.2%}  OOS {r.oos_CAGR:7.2%}/{r.oos_Sharpe:.4f}/{r.oos_MaxDD:7.2%}  "
                f"4a {int(r.keep4a)} 4b {int(r.keep4b)} | OOS 4b {int(r.oos_keep4b)}")
        say(f"  [{p}] placebo-chooser cells (S x k)")
        dd = d[d.kind == "PLACEBO-chooser"]
        for _, r in dd.iterrows():
            say(f"    S={int(r.S):3d} k={r.k:.1f}  lic {int(r.n_licensed):2d}/{len(arms)} "
                f"{'FALLBACK ' if r.fell_back else '         '}pick {r['pick']:10s} "
                f"full {r.full_CAGR:7.2%}/{r.full_Sharpe:.4f}/{r.full_MaxDD:7.2%}  "
                f"OOS {r.oos_CAGR:7.2%}/{r.oos_Sharpe:.4f}/{r.oos_MaxDD:7.2%}  "
                f"4a {int(r.keep4a)} 4b {int(r.keep4b)} | OOS 4b {int(r.oos_keep4b)}")
        say(f"  [{p}] distinct picks across the 16 cells: "
            f"{sorted(set(dd['pick']))}  ({dd['pick'].nunique()} of {len(arms)} arms ever chosen)")

    say("\n  RULE 8 (strict): (S, k) chosen on IS by argmax IS Sharpe of the selected book; "
        "2017-2026 read ONCE.")
    for _, r in wf.iterrows():
        say(f"    [{r.panel}] S={int(r.chosen_S)} k={r.chosen_k:.1f} -> {r['pick']}  "
            f"OOS {r.oos_CAGR:7.2%}/{r.oos_Sharpe:.4f}/{r.oos_MaxDD:7.2%}  "
            f"4a {int(r.oos_keep4a)} 4b {int(r.oos_keep4b)}  || RAW chooser OOS Sharpe "
            f"{r.raw_oos_Sharpe:.4f}, anchor {r.anchor_oos_Sharpe:.4f}, gridavg "
            f"{r.gridavg_oos_Sharpe:.4f}, SPY {r.spy_oos_Sharpe:.4f}, RULES v2 {r.live_oos_Sharpe:.4f}")

    # ---------------- the census leg
    say("\n" + "=" * 112)
    say("THE CENSUS LEG (904's literal ask) — committed placebo numbers vs their own seed floor")
    say("=" * 112)
    cen, fn = census(sigma_hat)
    say("  FUNNEL (the funnel IS most of the answer):")
    for _, r in fn.iterrows():
        say(f"    {r.cueset:7s} cued sentences {int(r.cued_sentences):4d} -> carrying a >=4dp "
            f"decimal {int(r.with_4dp_number):3d} -> DIFFERENCES (|x|<0.1) "
            f"{int(r.get('differences', 0) or 0):3d} in {int(r.get('files', 0) or 0):2d} files "
            f"-> STAMPED with both a seed count and an arm count "
            f"{int(r.get('stamped', 0) or 0):3d}")
    if len(cen):
        for cs in CUES:
            for lab, c in [("all      ", cen[(cen.cueset == cs) & cen["stamped"]]),
                           ("signed   ", cen[(cen.cueset == cs) & cen["stamped"] & cen["signed"]])]:
                if not len(c):
                    say(f"    {cs:7s} {lab}: 0 stamped numbers -> NOTHING in this claim set can "
                        f"be scored against its own floor")
                    continue
                say(f"    {cs:7s} {lab} n={len(c)}, median own-floor {c['floor'].median():.5f}, "
                    f"median |value| {c['value'].abs().median():.5f}")
                for k in K_LADDER:
                    if k == 0.0:
                        continue
                    say(f"        k={k:.1f}: {int(c[f'below_k{k}'].sum())} of {len(c)} "
                        f"({c[f'below_k{k}'].mean():.1%}) INSIDE k x their own floor")
    else:
        say("  harvest returned 0 difference rows — reported as a NULL RESULT, not hidden.")

    # ---------------- verdict
    say("\n" + "=" * 112)
    say("VERDICT")
    say("=" * 112)
    pl = cells[cells.kind == "PLACEBO-chooser"]
    raw = cells[cells.kind == "RAW-IS-Sharpe-chooser"].set_index("panel")
    beats = 0
    for p in ["U56", "B136", "SMALL"]:
        d = pl[pl.panel == p]
        b = int((d.oos_Sharpe > raw.loc[p, "oos_Sharpe"]).sum())
        beats += b
        say(f"  [{p}] placebo-chooser cells beating the RAW IS-Sharpe chooser OOS: {b}/16  "
            f"(mean OOS Sharpe {d.oos_Sharpe.mean():.4f} vs raw {raw.loc[p,'oos_Sharpe']:.4f}); "
            f"4a {int(d.keep4a.sum())}/16, 4b {int(d.keep4b.sum())}/16, OOS 4b {int(d.oos_keep4b.sum())}/16")
    say(f"  TOTAL: {beats}/48 cells beat the raw chooser out of sample; "
        f"4a {int(pl.keep4a.sum())}/48, 4b {int(pl.keep4b.sum())}/48.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    cells.to_csv(f"{OUT}.cells.csv", index=False)
    nulls.to_csv(f"{OUT}.nulls.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    if len(cen):
        cen.to_csv(f"{OUT}.census.csv", index=False)
    fn.to_csv(f"{OUT}.census_funnel.csv", index=False)
    Path(f"{OUT}.result.md").write_text(
        "# Idea 904 (lane B, 2026-09-18) — which committed PLACEBO numbers are below their own SEED FLOOR?\n\n"
        "```\n" + "\n".join(LOG) + "\n```\n")
    say(f"\n  wrote {OUT.name}.{{grid,cells,nulls,walkforward,gates,census}}.csv + .result.md "
        f"in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
