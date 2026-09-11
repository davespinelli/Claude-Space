#!/usr/bin/env python3
"""Idea 524 (lane B, 2026-09-11): does any published panel-property claim have an
INTERIOR cap mix — and if not, what would a standing interior comparand COST?

The question
------------
Idea 286 established that every NAMED panel in the record sits at cap-mix q in {0, 1}:
U56, B136, BSTK100 and ETF36 are pure large-cap/ETF (q = 0), SMALL439 is pure sub-$2B
(q = 1).  So when the record says "the result is a panel property", the two panels being
compared are always the two ENDPOINTS of the cap axis, and the claim has no within-stratum
content.  The queue asks two things:

  PART A (the census)  Over every committed *.result.md, resolve the panels each
                       cross-panel property claim compares into q and report the
                       distribution of dq = max q - min q.  The queue's literal bar is
                       "dq < 1.0".  That bar is reported, AND split, because dq = 0
                       (both compared panels inside the SAME stratum) passes it while
                       carrying zero cap variation; the claim with content is the one
                       whose compared set contains an INTERIOR panel, 0 < q < 1.

  PART B (the price)   "Price what a single interior panel (q=0.5, k matched) would cost
                       to add as a standing comparand."  Three prices, all published:
                         B1 COMPUTE   seconds and book-cells per added comparand.
                         B2 INFORMATION  does MIX50 ever land OUTSIDE the endpoint
                            interval on the statistics the record publishes?  If it
                            always interpolates, a standing interior panel tells you
                            nothing an endpoint pair does not already imply.
                         B3 RESOLUTION  the draw-to-draw sd of an interior panel against
                            the endpoint gap it is meant to bisect — i.e. how many draws
                            a standing MIX50 needs before its position is even readable.
                            A SINGLE interior panel is priced here, as the queue words it.

  PART C (rule 8)      PROTOCOL 8 walk-forward on the same grid: (q, k) chosen on IS
                       2010-2016 by argmax mean IS Sharpe, OOS 2017-2026 read once
                       against RULES v2 on the SAME panel and against SPY.  Both KEEP
                       paths (4a, 4b) evaluated on every book cell.

TUNED PARAMETERS (max 2, PROTOCOL rule 4): q (5 rungs: 0, .25, .50, .75, 1) and k
(3 widths: 40, 56, 100).  Every grid point is reported (.grid.csv carries all of them).
Draws (6, seeded), gross (0.75), cadence (weekly), cost (10 bps), t+1 execution and the
RULES v1 eligibility gate are the record's published conventions and are NOT tuned.
k = 40 is the record's own ladder width (ideas 276/285/525), k = 56 matches U56 (the
"k matched" comparand the queue names), k = 100 is the widest width at which q = 0 is
constructible at all (BSTK100 has exactly 100 non-ETF large caps).

GATES
  G0  fast_backtest (vectorised twin) vs engine.backtest on a real interior mix panel:
      max |dSharpe| and max |dCAGR| printed, must be < 1e-9.
  G1  idea 286's premise re-derived structurally, not quoted: the q of every named panel
      computed from the source lists.  All five must land in {0, 1} or the census's
      mapping is wrong.

SURVIVORSHIP (PROTOCOL rule 9): the small panel and broad136 are CURRENT constituents of
their screens, so every small-cap level is biased upward by an unknown amount.  The
objects under test here are a CENSUS (a property of the record's text, survivorship-free)
and the SHAPE/SPREAD of statistics along the cap axis; levels are not the finding.

Deterministic (seeded).  Writes .grid.csv .census.csv .interp.csv .walkforward.csv
.console.txt .result.md
"""
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score            # noqa: E402
from engine import backtest, metrics, rebalance_mask                   # noqa: E402

STEM = Path(__file__).resolve().with_suffix("").name
OUT = Path(__file__).resolve().parent

COST, FREQ, GROSS = 10.0, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
QS = [0.0, 0.25, 0.50, 0.75, 1.0]
KS = [40, 56, 100]
N_DRAWS = 6
NS = [5, 10, 20]
SEED = 524

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- engine twin
def fast_backtest(px, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost; gated against it in G0."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        T = u.sum(axis=1) + (1.0 - w.sum())
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def run_net(px, wfn, cost=COST):
    r0, turn = fast_backtest(px, wfn(px))
    return r0 - turn * cost / 1e4


# ---------------------------------------------------------------- books
def cand_weights(n):
    """Idea 2's KEEP-candidate book, verbatim from ideas 276/285: RULES v1 gate, composite
    score (no vol scaler), top n equal-weighted at 75% gross."""
    def f(px):
        tradables = [c for c in px.columns if c != "SPY"]
        s, above, vol20 = score(px[tradables], vol_scale=False)
        elig = s.where(above & (vol20 < 0.60))
        rank = elig.rank(axis=1, ascending=False)
        w = (rank <= n).astype(float) * (GROSS / n)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f


def ewall_weights(px):
    tradables = [c for c in px.columns if c != "SPY"]
    e = pd.DataFrame(1.0, index=px.index, columns=tradables).where(px[tradables].notna(), 0.0)
    w = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def v2_weights(px):
    return (rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
            .reindex(columns=px.columns).fillna(0.0))


def n_elig_mean(px):
    """Mean daily eligible count under the RULES v1 gate (idea 286's Ebar)."""
    tradables = [c for c in px.columns if c != "SPY"]
    s, above, vol20 = score(px[tradables], vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    return float(elig.notna().sum(axis=1).loc[px.index[260]:].mean())


# ---------------------------------------------------------------- metrics
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r)
    h1, h2 = hs(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"])


def pass4b(row, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves and OOS, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's."""
    s1, s2 = hs(spy)
    ms = metrics(spy)
    return bool(row["H1"] > s1 and row["H2"] > s2
                and row["OOS_Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]
                and abs(row["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])
                and row["CAGR"] >= 0.70 * ms["CAGR"])


def pass4a(row, v2):
    """PROTOCOL 4a: Sharpe > the live rules in BOTH halves, MaxDD no worse."""
    return bool(row["H1"] > v2["H1"] and row["H2"] > v2["H2"] and row["MaxDD"] >= v2["MaxDD"])


def spearman(a, b):
    x, y = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = x.notna() & y.notna()
    if ok.sum() < 3:
        return float("nan")
    return float(x[ok].rank().corr(y[ok].rank()))


# ---------------------------------------------------------------- panels
def sources():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    px56, pxb = load_universe(), load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    pxs = load_universe(small=True)
    s_stk = sorted(c for c in pxs.columns if c != "SPY" and c not in bad)
    b_all = [c for c in pxb.columns if c != "SPY"]
    b_stk = sorted(c for c in b_all if c not in etfs)
    b_etf = sorted(c for c in b_all if c in etfs)
    u_all = sorted(c for c in px56.columns if c != "SPY")
    P(f"[src] SMALL {len(pxs.columns)-1} screened, dropped {len(bad)} with max_1d_move>=1.0 "
      f"-> SMALL{len(s_stk)};  B136 {len(b_all)} = BSTK{len(b_stk)} + ETF{len(b_etf)};  "
      f"U56 {len(u_all)}")
    spy = pxs["SPY"]
    return dict(px56=px56, pxb=pxb, pxs=pxs, s_stk=s_stk, b_stk=b_stk, b_etf=b_etf,
                u_all=u_all, small_names=set(s_stk), spy=spy)


def mix_panel(S, sc, lc):
    """Panel with small-cap names sc and large-cap names lc, plus SPY as benchmark."""
    parts = []
    if sc:
        parts.append(S["pxs"][list(sc)])
    if lc:
        parts.append(S["pxb"][list(lc)])
    px = pd.concat(parts + [S["spy"].rename("SPY")], axis=1, sort=True)
    px = px.loc[S["pxs"].index.min():].dropna(how="all").ffill()
    return px[list(sc) + list(lc) + ["SPY"]]


def draw_cells(S):
    """(q, k, draw) -> panel.  Deterministic; exact-duplicate draws are deduped and the
    dedupe is reported, never silently dropped."""
    rng = np.random.default_rng(SEED)
    cells = []
    seen = {}
    for k in KS:
        for q in QS:
            ns = int(round(q * k))
            nl = k - ns
            if nl > len(S["b_stk"]) or ns > len(S["s_stk"]):
                P(f"[src] (q={q}, k={k}) NOT CONSTRUCTIBLE (needs {nl} large of "
                  f"{len(S['b_stk'])}, {ns} small of {len(S['s_stk'])}) — skipped")
                continue
            for d in range(N_DRAWS):
                sc = tuple(sorted(rng.choice(S["s_stk"], ns, replace=False))) if ns else ()
                lc = tuple(sorted(rng.choice(S["b_stk"], nl, replace=False))) if nl else ()
                key = (sc, lc)
                if key in seen:
                    cells.append(dict(q=q, k=k, draw=d, sc=sc, lc=lc, dup_of=seen[key]))
                    continue
                seen[key] = d
                cells.append(dict(q=q, k=k, draw=d, sc=sc, lc=lc, dup_of=-1))
    ndup = sum(1 for c in cells if c["dup_of"] >= 0)
    P(f"[src] {len(cells)} (q,k,draw) cells over {len(QS)} q rungs x {len(KS)} widths x "
      f"{N_DRAWS} draws; {ndup} are EXACT repeats (the pool is exhausted at that cell) and "
      f"are kept in the grid but flagged dup=1")
    return cells


# ======================================================================= GATES ==
def gate0(S, cells):
    c = next(c for c in cells if c["q"] == 0.5 and c["k"] == 40 and c["draw"] == 0)
    px = mix_panel(S, c["sc"], c["lc"])
    wfn = cand_weights(10)
    t0 = time.time()
    eng = backtest(px, wfn(px), cost_bps=COST, freq=FREQ)["returns"]
    t_eng = time.time() - t0
    t0 = time.time()
    fast = run_net(px, wfn)
    t_fast = time.time() - t0
    st = px.index[260]
    a, b = metrics(eng.loc[st:]), metrics(fast.loc[st:])
    dS, dC = abs(a["Sharpe"] - b["Sharpe"]), abs(a["CAGR"] - b["CAGR"])
    P(f"[G0] engine vs fast twin on an INTERIOR panel (q=0.5, k=40, draw 0, CAND-10): "
      f"|dSharpe| {dS:.3e}  |dCAGR| {dC:.3e}  -> {'PASS' if max(dS, dC) < 1e-9 else 'FAIL'}"
      f"   (engine {t_eng:.2f}s vs twin {t_fast:.3f}s, {t_eng/max(t_fast,1e-9):.0f}x)")
    assert max(dS, dC) < 1e-9, "G0 FAILED"
    return t_eng, t_fast


def gate1(S):
    """Idea 286's premise, re-derived from the source lists rather than quoted."""
    small = S["small_names"]
    named = {
        "U56": S["u_all"],
        "B136": [c for c in S["pxb"].columns if c != "SPY"],
        "BSTK100": S["b_stk"],
        "ETF36": S["b_etf"],
        "SMALL439": S["s_stk"],
    }
    qs = {}
    for tag, names in named.items():
        qs[tag] = sum(1 for c in names if c in small) / len(names)
    P("[G1] q of every NAMED panel, computed from the source lists (idea 286's premise):")
    for tag, q in qs.items():
        P(f"        {tag:<9} k={len(named[tag]):>3}  q={q:.4f}")
    interior = [t for t, q in qs.items() if 0 < q < 1]
    P(f"[G1] named panels with INTERIOR q (0<q<1): {len(interior)} of {len(qs)} "
      f"-> {'PASS (premise holds)' if not interior else 'FAIL: ' + str(interior)}")
    assert not interior, "G1 FAILED"
    return qs, {t: len(v) for t, v in named.items()}


# ====================================================================== LEG A ==
# Claim-detection regexes imported VERBATIM from idea 525 (cloud) leg C so the two
# censuses are comparable; only the resolution target changes (q, not Ebar).
PANEL_TOK = [("U56", re.compile(r"\bU56\b|universe\.json", re.I)),
             ("B136", re.compile(r"\bB136\b|universe_broad|\bbroad\b", re.I)),
             ("BSTK100", re.compile(r"BSTK\s?\d{2,3}", re.I)),
             ("ETF36", re.compile(r"\bETF\s?36\b", re.I)),
             ("SMALL439", re.compile(r"SMALL\s?43\d|prices_small|small=True|sub-\$2B|"
                                     r"small[- ]cap panel|small panel", re.I))]
PROP = re.compile(r"panel|universe|breadth|cap[- ]mix|capitalisation|capitalization|width|"
                  r"corpus|small[- ]cap|mega[- ]cap", re.I)
EXPLAINS = re.compile(r"explain|order|ordering|drives?|carries|accounts for|is a .{0,20}fact|"
                      r"because the panel|panel property|panel-of-origin", re.I)
# NEW here: does the file construct/report an INTERIOR-q panel at all?
MIXTOK = re.compile(r"\bq\s*=\s*0?\.(?!0\b)\d|\bq\s*in\s*[\{\(]|mix[- ]panel|mixed panel|"
                    r"MIX\d{2}|cap[- ]mix (?:ladder|axis|rung)|small[- ]cap share", re.I)


def leg_a(qs):
    files = sorted(OUT.glob("*.result.md"))
    P(f"\n[A] CENSUS of {len(files)} committed *.result.md files "
      f"(claim regexes imported verbatim from idea 525 cloud leg C)")
    rows = []
    for f in files:
        t = f.read_text(errors="ignore")
        named = [tag for tag, rx in PANEL_TOK if rx.search(t)]
        if len(named) < 2 or not PROP.search(t):
            continue
        tight = False
        for mo in EXPLAINS.finditer(t):
            win = t[max(0, mo.start() - 200): mo.start() + 200]
            if PROP.search(win) and any(rx.search(win) for _, rx in PANEL_TOK):
                tight = True
                break
        qv = [qs[p] for p in named]
        rows.append(dict(file=f.name, panels=";".join(named), n_panels=len(named),
                         explains=bool(EXPLAINS.search(t)), explains_tight=tight,
                         q_min=min(qv), q_max=max(qv), dq=max(qv) - min(qv),
                         builds_interior=bool(MIXTOK.search(t))))
    c = pd.DataFrame(rows)
    P(f"[A] {len(c)} files name >= 2 panels AND a panel-property word; "
      f"{int(c.explains.sum())} carry an EXPLAINS verb anywhere (LOOSE), "
      f"{int(c.explains_tight.sum())} within 200 chars of both a panel token and a "
      f"property word (TIGHT)")
    for lab, sel in (("LOOSE", c[c.explains]), ("TIGHT", c[c.explains_tight])):
        lt = int((sel.dq < 1.0).sum())
        zero = int((sel.dq == 0).sum())
        one = int((sel.dq == 1.0).sum())
        P(f"[A] {lab} ({len(sel)} claims): dq < 1.0 (the queue's literal bar) "
          f"{lt} ({lt/max(len(sel),1):.3f}) — of which dq == 0 EXACTLY {zero}, i.e. "
          f"DEGENERATE (both compared panels in the SAME stratum, zero cap variation); "
          f"dq == 1.0 {one}; claims with an INTERIOR compared panel (0<q<1): 0 BY "
          f"CONSTRUCTION (G1: no named panel is interior)")
        P(f"[A] {lab}: files that CONSTRUCT an interior-q panel anywhere in their text: "
          f"{int(sel.builds_interior.sum())} ({sel.builds_interior.mean():.3f}) — these are "
          f"the ladders (ideas 276/285/525), whose interior rungs are RUNGS OF A SWEEP, not "
          f"standing comparands: no named panel they compare against is interior")
    P(f"[A] dq distribution over TIGHT claims: {dict(c[c.explains_tight].dq.value_counts())}")
    P(f"[A] panel-pair frequency (TIGHT): "
      f"{dict(c[c.explains_tight].panels.value_counts().head(6))}")
    return c


# ====================================================================== LEG B ==
def leg_b(S, cells):
    """Run every (q,k,draw) panel x every book; the grid that prices the comparand."""
    P(f"\n[B] GRID: {len(cells)} panels x {len(NS)+2} books "
      f"(CAND-{'/'.join(map(str,NS))}, EWall, RULES v2), {COST:.0f} bps, weekly, t+1")
    rows = []
    t0 = time.time()
    for i, c in enumerate(cells):
        px = mix_panel(S, c["sc"], c["lc"])
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        eb = n_elig_mean(px)
        v2r = run_net(px, v2_weights).loc[st:]
        v2m = mrow(v2r)
        books = [(f"CAND-{n}", cand_weights(n)) for n in NS] + \
                [("EWall", ewall_weights), ("RULESv2", v2_weights)]
        for name, wfn in books:
            r = v2r if name == "RULESv2" else run_net(px, wfn).loc[st:]
            m = mrow(r)
            rows.append(dict(q=c["q"], k=c["k"], draw=c["draw"], dup=int(c["dup_of"] >= 0),
                             book=name, Ebar=eb, breadth=eb / c["k"], **m,
                             pass4a=pass4a(m, v2m), pass4b=pass4b(m, spy),
                             spy_S=metrics(spy)["Sharpe"],
                             spy_oosS=metrics(spy.loc[OOS_START:])["Sharpe"],
                             spy_CAGR=metrics(spy)["CAGR"], spy_MaxDD=metrics(spy)["MaxDD"],
                             spy_H1=hs(spy)[0], spy_H2=hs(spy)[1]))
        if (i + 1) % 15 == 0:
            P(f"      .. {i+1}/{len(cells)} panels ({time.time()-t0:.0f}s)")
    g = pd.DataFrame(rows)
    wall = time.time() - t0
    P(f"[B] grid done: {len(g)} book cells over {len(cells)} panels in {wall:.0f}s "
      f"({wall/len(cells):.2f}s per panel, {wall/len(g):.2f}s per book cell)")
    P(f"[B] KEEP paths over the whole grid: 4a passes {int(g.pass4a.sum())} of {len(g)}, "
      f"4b passes {int(g.pass4b.sum())} of {len(g)}")
    sub = g[g.book != "RULESv2"]
    P(f"[B] 4b passes by q rung (non-v2 books): "
      f"{dict(sub.groupby('q').pass4b.mean().round(4))}")
    P(f"[B] 4b passes by k (non-v2 books): {dict(sub.groupby('k').pass4b.mean().round(4))}")
    return g, wall


def leg_b_prices(g, wall, t_eng, t_fast, census):
    """B1 compute, B2 information, B3 resolution."""
    P("\n[B1] COMPUTE PRICE of one standing interior comparand")
    per_panel = wall / g.groupby(["q", "k", "draw"]).ngroups
    n_books = g.book.nunique()
    P(f"[B1] one panel = {n_books} book cells = {per_panel:.2f}s on the vectorised twin, "
      f"{per_panel*t_eng/max(t_fast,1e-9):.0f}s on engine.backtest. A standing MIX50 at one "
      f"k adds {per_panel:.2f}s and {n_books} cells per run; at all {len(KS)} widths, "
      f"{per_panel*len(KS):.2f}s. Against the {len(census)} committed cross-panel claim "
      f"files, retrofitting one interior comparand to the whole record = "
      f"{per_panel*len(census)/60:.1f} min of twin compute "
      f"({per_panel*len(census)*t_eng/max(t_fast,1e-9)/3600:.1f} h on engine.backtest).")

    P("\n[B2] INFORMATION PRICE: does the interior panel ever land OUTSIDE the endpoint "
      "interval?  Per (k, book, draw), compare S(q=0.5) against [min,max] of S(q=0), S(q=1) "
      "and against the midpoint. 'outside' = beyond the endpoint interval by more than the "
      "within-cell draw sd of that statistic.")
    stats = ["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "Ebar"]
    rows = []
    for (k, book), sel in g.groupby(["k", "book"]):
        piv = sel.pivot_table(index="draw", columns="q", values=stats)
        for s in stats:
            if not {0.0, 0.5, 1.0}.issubset(set(piv[s].columns)):
                continue
            sd = float(sel.groupby("q")[s].std().max())
            for d in piv.index:
                a, m_, b = piv[s].loc[d, 0.0], piv[s].loc[d, 0.5], piv[s].loc[d, 1.0]
                lo, hi = min(a, b), max(a, b)
                out = (m_ < lo - sd) or (m_ > hi + sd)
                mid = 0.5 * (a + b)
                gap = b - a
                rows.append(dict(k=k, book=book, stat=s, draw=d, q0=a, q50=m_, q100=b,
                                 sd=sd, outside=bool(out), resid=m_ - mid,
                                 resid_in_sd=(m_ - mid) / sd if sd else np.nan,
                                 # signed position on the q=0 -> q=1 chord: 0.5 == midpoint,
                                 # < 0.5 == the interior panel sits NEARER the q=0 endpoint
                                 pos_on_chord=((m_ - a) / gap) if gap else np.nan))
    it = pd.DataFrame(rows)
    P(it.groupby("stat").agg(cells=("outside", "size"), outside=("outside", "sum"),
                             outside_rate=("outside", "mean"),
                             mean_abs_resid_in_sd=("resid_in_sd", lambda x: x.abs().mean()),
                             mean_pos_on_chord=("pos_on_chord", "mean"),
                             frac_below_midpoint=("pos_on_chord", lambda x: (x < 0.5).mean()))
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"[B2] over ALL {len(it)} (k, book, stat, draw) cells: the interior panel lands "
      f"outside the endpoint interval (by more than one draw sd) in {int(it.outside.sum())} "
      f"({it.outside.mean():.4f}); mean |midpoint residual| = "
      f"{it.resid_in_sd.abs().mean():.3f} draw-sd = "
      f"{(it.pos_on_chord - 0.5).abs().mean():.3f} of the endpoint gap.")
    # The DD leg is the one BOTH KEEP paths use, so it is tested directly and not left to
    # the chord statistic: is the interior panel's drawdown shallower than BOTH endpoints?
    dd = it[it.stat == "MaxDD"]
    better = (dd.q50.abs() < dd.q0.abs()) & (dd.q50.abs() < dd.q100.abs())
    P(f"[B2] DD LEG (used by BOTH KEEP paths), tested directly: the q=0.5 panel's MaxDD is "
      f"SHALLOWER THAN BOTH ENDPOINTS in {int(better.sum())} of {len(dd)} (k, book, draw) "
      f"cells ({better.mean():.4f}) — a strictly non-monotone cap axis, which an "
      f"endpoint-only comparison cannot represent at all.")
    ddc = dd.assign(better=better).groupby(["k", "book"]).better.mean().unstack()
    P(ddc.to_string(float_format=lambda x: f"{x:.3f}"))

    # Per-draw chord positions carry noise from all three panels, so the curvature test is
    # run on the (k, book, stat) MEAN over draws with its own standard error.  Two-sided
    # |t| > 2 against the straight-axis null of 0.5.
    agg = (it.dropna(subset=["pos_on_chord"]).groupby(["k", "book", "stat"])
             .pos_on_chord.agg(["mean", "std", "count"]).reset_index())
    agg["se"] = agg["std"] / np.sqrt(agg["count"])
    agg["t_vs_half"] = (agg["mean"] - 0.5) / agg["se"].replace(0, np.nan)
    P("[B2] CURVATURE TEST on the (k, book, stat) means (6 draws each), null = 0.5:")
    P(agg.groupby("stat").agg(triples=("mean", "size"), mean_pos=("mean", "mean"),
                              median_t=("t_vs_half", "median"),
                              below_half_t_lt_m2=("t_vs_half", lambda x: int((x < -2).sum())),
                              above_half_t_gt_2=("t_vs_half", lambda x: int((x > 2).sum())))
      .to_string(float_format=lambda x: f"{x:.4f}"))
    sig = int((agg.t_vs_half.abs() > 2).sum())
    P(f"[B2] {sig} of {len(agg)} (k, book, statistic) triples reject the straight-axis null "
      f"at |t| > 2, {int((agg.t_vs_half < -2).sum())} of them BELOW the midpoint (the q=0.5 "
      f"panel behaves MORE like the large-cap endpoint than a linear cap axis predicts).")
    P(f"[B2] CHORD POSITION (the part linear interpolation would get wrong): mean "
      f"{it.pos_on_chord.mean():.4f} against 0.5 for a straight cap axis; the interior "
      f"panel sits below the midpoint in {int((it.pos_on_chord < 0.5).sum())} of "
      f"{int(it.pos_on_chord.notna().sum())} cells "
      f"({(it.pos_on_chord < 0.5).mean():.3f}). A mean far from 0.5 with a lopsided sign "
      f"count is CURVATURE the endpoints cannot show; a mean near 0.5 with a ~50/50 split "
      f"is draw noise around a straight axis.")

    P("\n[B3] RESOLUTION PRICE: the draw-to-draw sd of an interior panel against the "
      "endpoint gap it is meant to bisect. A SINGLE interior panel resolves its own "
      "position only if sd << gap/2.")
    rows = []
    for (k, book, s) in [(k, b, s) for k in sorted(g.k.unique())
                         for b in sorted(g.book.unique()) for s in stats]:
        sel = g[(g.k == k) & (g.book == book)]
        if not {0.0, 0.5, 1.0}.issubset(set(sel.q.unique())):
            continue
        e0, e1 = sel[sel.q == 0.0][s].mean(), sel[sel.q == 1.0][s].mean()
        gap = abs(e1 - e0)
        sd = float(sel[sel.q == 0.5][s].std())
        need = int(np.ceil((2 * sd / (gap / 2)) ** 2)) if gap > 0 else -1
        rows.append(dict(k=k, book=book, stat=s, endpoint_gap=gap, interior_sd=sd,
                         sd_over_halfgap=sd / (gap / 2) if gap > 0 else np.nan,
                         draws_needed=need))
    rr = pd.DataFrame(rows)
    P(rr.groupby("stat").agg(median_gap=("endpoint_gap", "median"),
                             median_sd=("interior_sd", "median"),
                             median_sd_over_halfgap=("sd_over_halfgap", "median"),
                             median_draws_needed=("draws_needed", "median"),
                             worst_draws_needed=("draws_needed", "max"))
      .to_string(float_format=lambda x: f"{x:.3f}"))
    n1 = int((rr.sd_over_halfgap > 1).sum())
    P(f"[B3] on {n1} of {len(rr)} (k, book, statistic) triples the interior panel's "
      f"SINGLE-DRAW sd EXCEEDS half the endpoint gap (on those, one interior panel cannot "
      f"say which side of the midpoint it is on); on the other {len(rr)-n1} it resolves the "
      f"half-gap from a single draw. Median draws needed for a half-gap-resolution standing "
      f"comparand: {rr.draws_needed.median():.0f}; worst over all triples: "
      f"{int(rr.draws_needed.max())}.")
    return it, rr


# ====================================================================== LEG C ==
def leg_c(g):
    """PROTOCOL rule 8: (q, k) picked on IS 2010-2016 only, OOS 2017-2026 read once."""
    P("\n[C] RULE 8 WALK-FORWARD: for each book, (q, k) chosen by argmax mean IS Sharpe "
      "on 2010-2016 ONLY; OOS 2017-2026 read once against RULES v2 on the SAME panel "
      "and against SPY.")
    rows = []
    for book in [b for b in sorted(g.book.unique()) if b != "RULESv2"]:
        sel = g[g.book == book]
        cell = sel.groupby(["q", "k"]).IS_Sharpe.mean()
        q, k = cell.idxmax()
        pick = sel[(sel.q == q) & (sel.k == k)]
        v2 = g[(g.book == "RULESv2") & (g.q == q) & (g.k == k)]
        rows.append(dict(book=book, pick_q=q, pick_k=k, IS_Sharpe=cell.max(),
                         CAGR=pick.CAGR.mean(), Sharpe=pick.Sharpe.mean(),
                         MaxDD=pick.MaxDD.mean(), H1=pick.H1.mean(), H2=pick.H2.mean(),
                         v2_CAGR=v2.CAGR.mean(), v2_Sharpe=v2.Sharpe.mean(),
                         v2_MaxDD=v2.MaxDD.mean(), v2_H1=v2.H1.mean(), v2_H2=v2.H2.mean(),
                         spy_CAGR=pick.spy_CAGR.mean(), spy_S=pick.spy_S.mean(),
                         spy_MaxDD=pick.spy_MaxDD.mean(),
                         OOS_CAGR=pick.OOS_CAGR.mean(), OOS_Sharpe=pick.OOS_Sharpe.mean(),
                         OOS_MaxDD=pick.OOS_MaxDD.mean(),
                         v2_OOS_CAGR=v2.OOS_CAGR.mean(), v2_OOS_Sharpe=v2.OOS_Sharpe.mean(),
                         v2_OOS_MaxDD=v2.OOS_MaxDD.mean(),
                         spy_OOS_Sharpe=pick.spy_oosS.mean(),
                         beats_v2=int(pick.OOS_Sharpe.mean() > v2.OOS_Sharpe.mean()),
                         beats_spy=int(pick.OOS_Sharpe.mean() > pick.spy_oosS.mean()),
                         p4a=int(pick.pass4a.sum()), p4b=int(pick.pass4b.sum()),
                         n=len(pick)))
    wf = pd.DataFrame(rows)
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"[C] picked (q,k) cells: {sorted(set(zip(wf.pick_q, wf.pick_k)))}; interior q picked "
      f"in {int(((wf.pick_q > 0) & (wf.pick_q < 1)).sum())} of {len(wf)} books")
    P(f"[C] OOS Sharpe beats SPY in {int(wf.beats_spy.sum())} of {len(wf)} picks; beats "
      f"RULES v2 on the same panel in {int(wf.beats_v2.sum())}; 4a passes "
      f"{int(wf.p4a.sum())}, 4b passes {int(wf.p4b.sum())} over {int(wf.n.sum())} "
      f"picked book-panels")

    P(f"\n[C2] THE k=56 CAP LADDER (U56-matched width — the 'k matched' comparand the "
      f"queue names), mean over {N_DRAWS} draws. SPY on the same sample: "
      f"CAGR {g.spy_CAGR.mean():.4f}, Sharpe {g.spy_S.mean():.4f} "
      f"(H1 {g.spy_H1.mean():.4f} / H2 {g.spy_H2.mean():.4f}), MaxDD {g.spy_MaxDD.mean():.4f}, "
      f"OOS Sharpe {g.spy_oosS.mean():.4f}")
    lad = (g[g.k == 56].groupby(["book", "q"])
           [["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
             "Ebar"]].mean())
    P(lad.to_string(float_format=lambda x: f"{x:.4f}"))
    return wf


# ======================================================================= MAIN ==
def main():
    P(f"IDEA 524 (lane B) — {STEM}")
    P(f"q rungs {QS}; k widths {KS}; {N_DRAWS} seeded draws; books CAND-{NS}+EWall+RULESv2; "
      f"{COST:.0f} bps, freq={FREQ}, t+1 (engine convention), gross {GROSS}, seed {SEED}")
    S = sources()
    qs, widths = gate1(S)
    cells = draw_cells(S)
    t_eng, t_fast = gate0(S, cells)
    census = leg_a(qs)
    g, wall = leg_b(S, cells)
    it, rr = leg_b_prices(g, wall, t_eng, t_fast, census[census.explains_tight])
    wf = leg_c(g)

    g.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    census.to_csv(OUT / f"{STEM}.census.csv", index=False)
    it.to_csv(OUT / f"{STEM}.interp.csv", index=False)
    rr.to_csv(OUT / f"{STEM}.resolution.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    P("\nSURVIVORSHIP (PROTOCOL rule 9): SMALL439 and B136 are CURRENT constituents of "
      "their screens; small-cap levels are optimistic by an unknown amount. The census is "
      "a property of the record's text and is survivorship-free; the interpolation and "
      "resolution prices are contrasts, not levels.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
