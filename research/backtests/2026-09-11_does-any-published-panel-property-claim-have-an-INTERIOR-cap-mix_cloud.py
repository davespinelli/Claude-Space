#!/usr/bin/env python3
"""IDEA 524 - does any published panel-property claim have an INTERIOR cap mix?

Idea 286 established that q (the share of a panel's names drawn from SMALL439, the rest from
BSTK100) is the axis every cross-panel property claim is really moving, and that every NAMED
panel in the record sits at a corner: U56 / B136 / BSTK100 / ETF36 at q=0, SMALL439 at q=1.
A claim that compares two corners cannot separate "a property of the panel" from "a different
cap mix", so the record's cross-panel prose has no within-stratum content.

PART A - THE CENSUS.  Every committed claim-bearing document is scanned for the panel
vocabulary, each named panel is mapped to its q, and every claim naming >= 2 panels is scored
by the q-span it actually crosses.  Counted, never guessed: a panel token the map does not
know is UNKNOWN and is reported as UNKNOWN.

PART B - PRICING THE INTERIOR COMPARAND.  If the census finds no standing interior panel,
the queue asks what one would cost to ADD.  A cost has two halves and both are measured:
  (i)  COMPUTE  - the wall-clock seconds a standing interior comparand adds to a run, and
  (ii) INFORMATION - what it BUYS.  A comparand that lands on the straight line between the
       two corners it sits between buys nothing: the corners already imply it.  So for every
       arm x metric the interior cells are scored against the CORNER-IMPLIED value
       q*v(1) + (1-q)*v(0), and the deviation is put next to the seed dispersion at that q.
       Deviation inside the noise = the interior panel is redundant; outside = the record's
       corner-only comparisons are reading a curve as a line.

P1 = q in {0.00, 0.25, 0.50, 0.75, 1.00}  (the cap-mix ladder)
P2 = k in {40, 80}                        (panel width, so width is never confounded with mix)
Seeds are REPLICATION, never selection: every seed is reported, none is chosen.
All 5 x 2 x 5 arms = 50 cells are reported, plus the named-panel reproduction rows.

Panel construction, the book arms, the statistics block and PROTOCOL's keep flags are
IMPORTED from idea 284's module (`2026-09-06_does-any-panel-property-separate-at-FIXED-cap-
mix_C.py`), not re-typed, so this run cannot drift from the construction the census is about.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens, so every
small-cap and interior cell here is survivorship-biased upward; the corner-vs-interior
CONTRAST is the reported quantity, not the level.  10 bps, weekly, next-day, no shorting.

Rule 8: parameters are chosen on 2009-2016 and evaluated on 2017-2026 untouched; OOS
CAGR/Sharpe/MaxDD are reported for every cell against the live baseline and SPY.

Deterministic, standalone.  Writes only its own artefacts.  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are untouched.
"""
import importlib.util
import os
import re
import sys
import time
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
from baseline import rules_v2_weights          # noqa: E402
from engine import backtest, metrics           # noqa: E402

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
I284 = OUT / "2026-09-06_does-any-panel-property-separate-at-FIXED-cap-mix_C.py"

QS = [float(x) for x in os.environ.get("I524_QS", "0.00,0.25,0.50,0.75,1.00").split(",")]
KS = [int(x) for x in os.environ.get("I524_KS", "40,80").split(",")]        # P2
N_SEEDS = int(os.environ.get("I524_SEEDS", "8"))   # replication, not selection
ARMS = ["EWall", "CAND10", "CAND20", "v1", "v2"]
COST_BPS, FREQ = 10, "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- the panel vocabulary, and the q the record's own construction gives each token -------
# q = share of the panel drawn from SMALL439 (idea 284's axis, idea 286's reading).
Q_MAP = {
    "U56": 0.0, "B136": 0.0, "BSTK100": 0.0, "BSTK": 0.0, "ETF36": 0.0,
    "SMALL439": 1.0, "SMALL483": 1.0, "SMALL": 1.0,
}
# tokens that name a panel but carry no defensible q on their own
AMBIGUOUS = {"broad", "panel", "universe"}
PANEL_TOK = re.compile(r"\b(U56|B136|BSTK100|BSTK\d*|ETF36|SMALL\d{3})\b")
# `q` is OVERLOADED in this record: idea 284's cap mix, but also quantile trims (`q0.17`,
# `q=0.90` selectivity).  A loose `q<number>` detector therefore over-counts, and is reported
# as a measured UPPER BOUND with its contamination named, never as the interior count.
INTERIOR_LOOSE = re.compile(r"\bq\s*=?\s*0?\.\d+|\bq0\.\d+", re.I)
# the TIGHT detector: vocabulary that can only mean a capitalisation mix
INTERIOR_TOK = re.compile(r"q\d?\.\d{3}~s\d"                       # idea 284's panel id
                          r"|cap[- ]mix|capitalisation mix|capitalization mix"
                          r"|mixed panel|interior (?:panel|cap|mix|q)"
                          r"|q *= *(?:the )?share", re.I)
# the loose detector's dominant false-positive channel, measured not assumed
QUANTILE_CTX = re.compile(r"(?i)trim|quantile|decile|percentile|breadth|selectivit|"
                          r"threshold|floor|trailing")
CLAIMY = re.compile(r"(?i)\b(vs\.?|versus|than|compared|beats?|worse|better|higher|lower|"
                    r"gap|difference|separat\w+|reverses?|survives?|fails?|holds?)\b")

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


# =========================================================================================
# PART A - the census
# =========================================================================================
def claim_docs():
    """Every committed document that carries published PROSE claims."""
    docs = [REPO / "research" / n for n in
            ("LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md", "RULES.md", "PROTOCOL.md")]
    docs += sorted(OUT.glob("*.result.md"))
    docs += sorted(OUT.glob("*_memo.md")) + sorted(OUT.glob("*.memo.md"))
    docs += sorted((REPO / "research" / "ideas").glob("*.md")) if (
        REPO / "research" / "ideas").exists() else []
    return [d for d in docs if d.exists() and d.name != f"{STEM}.result.md"]


def census():
    rows = []
    for d in claim_docs():
        try:
            txt = d.read_text(errors="replace")
        except Exception:
            continue
        for ln, line in enumerate(txt.splitlines(), 1):
            toks = PANEL_TOK.findall(line)
            if not toks:
                continue
            names = sorted(set(toks))
            qs, unknown = [], []
            for t in names:
                if t in Q_MAP:
                    qs.append(Q_MAP[t])
                elif t.startswith("BSTK"):
                    qs.append(0.0)
                elif t.startswith("SMALL"):
                    qs.append(1.0)
                else:
                    unknown.append(t)
            loose = bool(INTERIOR_LOOSE.search(line))
            rows.append(dict(
                doc=d.name, line=ln, n_panels=len(names), panels="|".join(names),
                n_unknown=len(unknown), unknown="|".join(unknown),
                q_min=min(qs) if qs else np.nan, q_max=max(qs) if qs else np.nan,
                q_span=(max(qs) - min(qs)) if len(qs) >= 2 else np.nan,
                has_interior_token=int(bool(INTERIOR_TOK.search(line))),
                loose_q_token=int(loose),
                loose_is_quantile=int(loose and bool(QUANTILE_CTX.search(line))),
                claimy=int(bool(CLAIMY.search(line))),
                text=line.strip()[:300]))
    return pd.DataFrame(rows)


def census_report(C):
    P("=" * 104)
    P("PART A - CENSUS OF THE RECORD'S PANEL-NAMING CLAIMS")
    P("=" * 104)
    P(f"  documents scanned: {C.doc.nunique()}   lines naming at least one panel: {len(C)}")
    multi = C[C.n_panels >= 2]
    P(f"  lines naming >= 2 distinct panels: {len(multi)}   of those, claim-shaped "
      f"(carry a comparison verb): {int(multi.claimy.sum())}")
    cl = multi[multi.claimy == 1]
    if len(cl):
        vc = cl.q_span.round(3).value_counts().sort_index()
        P("")
        P("  q-span actually crossed by each claim-shaped multi-panel line:")
        for span, n in vc.items():
            lab = ("0.0 = SAME CORNER (within-stratum, but AT a corner)" if span == 0
                   else "1.0 = the two corners, fully confounded" if span == 1
                   else f"{span} = INTERIOR CONTRAST")
            P(f"    q_span {span:<5} : {n:6d}  ({n/len(cl):6.1%})   {lab}")
        P(f"    UNKNOWN q (panel token off the map): "
          f"{int((cl.n_unknown > 0).sum())} lines - counted, not guessed")
        interior = cl[(cl.q_span > 0) & (cl.q_span < 1)]
        P("")
        P(f"  >>> claim-shaped lines whose compared panels differ in q by LESS than 1.0 and "
          f"more than 0: {len(interior)}")
        loose = C[C.loose_q_token == 1]
        tight = C[C.has_interior_token == 1]
        P("")
        P(f"  UPPER BOUND, loose `q<number>` detector: {len(loose)} lines in "
          f"{loose.doc.nunique()} documents - but `q` is OVERLOADED in this record and "
          f"{int(loose.loose_is_quantile.sum())} of them ({loose.loose_is_quantile.mean():.1%}) "
          f"sit beside trim/quantile/breadth vocabulary, i.e. are a QUANTILE q, not a cap mix.")
        P(f"  TIGHT cap-mix vocabulary (q#.###~s seed ids, 'cap mix', 'mixed panel', "
          f"'interior panel', 'q = share'): {len(tight)} lines in "
          f"{tight.doc.nunique()} documents")
        if len(tight):
            P("      where they live - these are the SEEDED STRATA of ideas 284/286, which are "
              "a study's own outputs, not standing comparands any later idea can cite:")
            for d, n in tight.doc.value_counts().head(12).items():
                P(f"        {n:5d}  {d}")
        both = tight[(tight.claimy == 1) & (tight.n_panels >= 2)]
        P(f"      of those, claim-shaped AND naming >= 2 panels: {len(both)}")
    return cl


# =========================================================================================
# PART B - the interior comparand, priced
# =========================================================================================
def build_grid(m284):
    px56, px136, pxs, etf36, b_stk, s_stk = m284.build_sources()
    idx = pxs.index.intersection(px136.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), px136.reindex(idx).ffill()
    P(f"  common calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"pools: SMALL{len(s_stk)} / BSTK{len(b_stk)}")
    small_pool, large_pool = np.array(sorted(s_stk)), np.array(sorted(b_stk))
    panels = {}
    for k in KS:
        for q in QS:
            n_s = int(round(q * k)); n_l = k - n_s
            for sd in range(N_SEEDS):
                seed = zlib.crc32(f"I524|{k}|{q:.3f}|{sd}".encode()) % (2 ** 32)
                rng = np.random.default_rng(seed)
                sc = sorted(rng.choice(small_pool, n_s, replace=False).tolist()) if n_s else []
                lc = sorted(rng.choice(large_pool, n_l, replace=False).tolist()) if n_l else []
                px, tr = m284.make_panel(pxs_c, pxb_c, sc, lc)
                panels[(k, q, sd)] = dict(px=px, tradable=tr, k=k, q=q, seed=sd)
    # named reproduction rows, at their own widths
    named = {
        "U56": (px56, [c for c in px56.columns if c != "SPY"]),
        "B136": (px136, [c for c in px136.columns if c != "SPY"]),
        "BSTK100": (px136, b_stk),
        "ETF36": (px136, etf36),
        "SMALL439": (pxs, s_stk),
    }
    return panels, named, pxb_c


def run_panel(m284, px, tradable, tag, k, q, sd):
    spy = px["SPY"].pct_change().fillna(0.0)
    start = px.index[260]
    rows = []
    for arm in ARMS:
        n = int(arm[4:]) if arm.startswith("CAND") else None
        w = m284.book_weights(px, tradable, arm, n=n)
        r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        rows.append(dict(tag=tag, k=k, q=q, seed=sd, arm=arm,
                         **m284.stat_block(r, spy.loc[start:])))
    rows.append(dict(tag=tag, k=k, q=q, seed=sd, arm="SPY",
                     **m284.stat_block(spy.loc[start:], spy.loc[start:])))
    return rows


def adjudicate(D, m284):
    """PROTOCOL 4a and 4b, per panel, against that panel's OWN SPY and its OWN v2 row."""
    out = []
    for key, g in D.groupby(["tag", "k", "q", "seed"]):
        g = g.set_index("arm")
        if "SPY" not in g.index or "v2" not in g.index:
            continue
        spy, v2 = g.loc["SPY"], g.loc["v2"]
        for arm, r in g.iterrows():
            if arm == "SPY":
                continue
            a, b, why = m284.keep_flags(r, spy, v2)
            out.append(dict(tag=key[0], k=key[1], q=key[2], seed=key[3], arm=arm,
                            pass4a=int(a), pass4b=int(b), fail4b=why,
                            CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                            OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                            OOS_MaxDD=r.OOS_MaxDD,
                            spy_CAGR=spy.CAGR, spy_Sharpe=spy.Sharpe, spy_MaxDD=spy.MaxDD,
                            spy_OOS_Sharpe=spy.OOS_Sharpe))
    return pd.DataFrame(out)


def curvature(D):
    """What the interior cell BUYS: its distance from the corner-implied line, in units of
    the seed dispersion at that same cell.  |z| <= 1 means the corners already imply it."""
    rows = []
    mets = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
    for (k, arm), g in D[D.tag == "MIX"].groupby(["k", "arm"]):
        piv = g.groupby("q")[mets].mean()
        sdv = g.groupby("q")[mets].std(ddof=1)
        cnt = g.groupby("q").size()
        if not {0.0, 1.0}.issubset(set(piv.index)):
            continue
        for q in [x for x in piv.index if 0 < x < 1]:
            for mt in mets:
                lin = q * piv.loc[1.0, mt] + (1 - q) * piv.loc[0.0, mt]
                obs = piv.loc[q, mt]
                se = sdv.loc[q, mt] / np.sqrt(max(1, cnt.loc[q]))
                rows.append(dict(k=k, arm=arm, q=q, metric=mt, observed=obs,
                                 corner_implied=lin, deviation=obs - lin,
                                 seed_sd=sdv.loc[q, mt], seed_se=se,
                                 z=(obs - lin) / se if se and np.isfinite(se) and se > 0
                                 else np.nan))
    return pd.DataFrame(rows)


# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 104)
    P("IDEA 524 (cloud, 2026-09-11) - DOES ANY PUBLISHED PANEL-PROPERTY CLAIM HAVE AN")
    P("INTERIOR CAP MIX?  and what would a standing interior comparand cost to add?")
    P("=" * 104)

    m284 = load_mod(I284, "i284")
    P(f"[G1] idea 284's construction imported verbatim from {I284.name}: "
      f"build_sources / make_panel / book_weights / stat_block / keep_flags - PASS")
    assert m284.K_MIX == 40 and m284.COST_BPS == 10 and m284.FREQ == "W" and m284.GROSS == 0.75
    P(f"[G2] its constants are the record's: k_mix {m284.K_MIX}, {m284.COST_BPS} bps, "
      f"freq {m284.FREQ}, gross {m284.GROSS}, max_vol {m284.MAX_VOL} - PASS")

    C = census()
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    cl = census_report(C)
    cl.to_csv(OUT / f"{STEM}.claims.csv", index=False)

    P("")
    P("=" * 104)
    P("PART B - PRICING A STANDING INTERIOR COMPARAND")
    P("=" * 104)
    t_build = time.time()
    panels, named, pxb = build_grid(m284)
    P(f"  {len(panels)} mixed panels built ({len(QS)} q x {len(KS)} k x {N_SEEDS} seeds) "
      f"in {time.time() - t_build:.1f}s")

    rows, timing = [], []
    for (k, q, sd), d in panels.items():
        ts = time.time()
        rows += run_panel(m284, d["px"], d["tradable"], "MIX", k, q, sd)
        timing.append(dict(kind="MIX", k=k, q=q, seed=sd, secs=time.time() - ts))
    for nm, (px, cols) in named.items():
        keep = list(dict.fromkeys([c for c in cols if c in px.columns] + ["SPY"]))
        p = px[keep].dropna(how="all").ffill()
        ts = time.time()
        rows += run_panel(m284, p, set(c for c in cols if c in px.columns), nm,
                          len([c for c in cols if c in px.columns]), np.nan, -1)
        timing.append(dict(kind="NAMED", k=len(keep) - 1, q=np.nan, seed=-1,
                           secs=time.time() - ts, name=nm))
    D = pd.DataFrame(rows)
    D.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    T = pd.DataFrame(timing)
    T.to_csv(OUT / f"{STEM}.timing.csv", index=False)

    A = adjudicate(D, m284)
    A.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)

    # ---- the full grid, every point ------------------------------------------------------
    P("")
    P("  THE FULL GRID - mean over seeds, every (k, q, arm) cell reported")
    for k in KS:
        g = D[(D.tag == "MIX") & (D.k == k)]
        piv = g.pivot_table(index="arm", columns="q",
                            values=["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"])
        P("")
        P(f"  --- k = {k} ---")
        P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  named reproduction rows:")
    P(D[D.tag != "MIX"].pivot_table(index="tag", columns="arm",
                                    values=["CAGR", "Sharpe", "OOS_Sharpe"]
                                    ).to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- KEEP paths ----------------------------------------------------------------------
    P("")
    P("  PROTOCOL KEEP paths, all cells:")
    kp = A[A.tag == "MIX"].groupby(["k", "q", "arm"])[["pass4a", "pass4b"]].mean()
    P(kp.unstack("arm").to_string(float_format=lambda x: f"{x:.3f}"))
    P(f"  4a passes: {int(A.pass4a.sum())} of {len(A)} cells;  "
      f"4b passes: {int(A.pass4b.sum())} of {len(A)}")
    if int(A.pass4b.sum()):
        by = A[A.pass4b == 1].groupby("q").size()
        P(f"  4b passes by q: {by.to_dict()}  (idea 286 found them all at q <= 0.25)")
    P("  4b binding bar over the failures:")
    P(A[A.pass4b == 0].fail4b.value_counts().head(10).to_string())

    # ---- what the interior BUYS -----------------------------------------------------------
    CV = curvature(D)
    CV.to_csv(OUT / f"{STEM}.curvature.csv", index=False)
    P("")
    P("-" * 104)
    P("WHAT AN INTERIOR COMPARAND BUYS - deviation from the corner-implied line, in seed SEs")
    P("-" * 104)
    hd = CV[CV.metric.isin(["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"])]
    P(hd.pivot_table(index=["k", "arm", "q"], columns="metric", values="z"
                     ).to_string(float_format=lambda x: f"{x:+.2f}"))
    out1 = CV[np.abs(CV.z) > 1]
    out2 = CV[np.abs(CV.z) > 2]
    P("")
    P(f"  interior cells measurably OFF the corner line (|z| > 1): {len(out1)} of {len(CV)} "
      f"({len(out1)/max(1,len(CV)):.1%});  |z| > 2: {len(out2)} ({len(out2)/max(1,len(CV)):.1%})")
    worst = CV.reindex(CV.z.abs().sort_values(ascending=False).index).head(8)
    P("  the 8 largest departures:")
    P(worst[["k", "arm", "q", "metric", "observed", "corner_implied", "deviation", "seed_se",
             "z"]].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    bymet = CV.groupby("metric").z.apply(lambda s: float(np.abs(s).median()))
    P("")
    P("  median |z| by metric (which statistics the corners can and cannot interpolate):")
    P(bymet.sort_values(ascending=False).to_string(float_format=lambda x: f"{x:.2f}"))

    # ---- the compute half of the cost ------------------------------------------------------
    mix_t = T[T.kind == "MIX"]
    P("")
    P(f"  COMPUTE COST: one interior panel's standard 5-arm block costs "
      f"{mix_t.secs.mean():.2f}s (median {mix_t.secs.median():.2f}s, k=40 "
      f"{mix_t[mix_t.k==40].secs.mean():.2f}s, k=80 {mix_t[mix_t.k==80].secs.mean():.2f}s).")
    P(f"                A standing comparand at {N_SEEDS} seeds costs "
      f"{mix_t[mix_t.q==0.5].secs.sum():.0f}s per run across both widths.")

    # ---- rule 8, book axis ------------------------------------------------------------------
    P("")
    P("=" * 104)
    P("RULE 8 - IS 2009-2016 chooses, OOS 2017-2026 evaluates, untouched")
    P("=" * 104)
    W = []
    for (k, q, arm), g in D[D.tag == "MIX"].groupby(["k", "q", "arm"]):
        W.append(dict(k=k, q=q, arm=arm, n_seeds=len(g),
                      IS_Sharpe=g.IS_Sharpe.mean(), CAGR=g.CAGR.mean(),
                      Sharpe=g.Sharpe.mean(), MaxDD=g.MaxDD.mean(),
                      H1=g.H1.mean(), H2=g.H2.mean(),
                      OOS_CAGR=g.OOS_CAGR.mean(), OOS_Sharpe=g.OOS_Sharpe.mean(),
                      OOS_MaxDD=g.OOS_MaxDD.mean()))
    WF = pd.DataFrame(W)
    # the rule-8 pick: best IS Sharpe over the (q, arm) grid at each k, evaluated OOS
    picks = []
    for k in KS:
        g = WF[(WF.k == k) & (WF.arm != "SPY")]
        best = g.loc[g.IS_Sharpe.idxmax()]
        spy = WF[(WF.k == k) & (WF.arm == "SPY")]
        spy = spy.iloc[0] if len(spy) else None
        picks.append(dict(k=k, pick_q=best.q, pick_arm=best.arm, IS_Sharpe=best.IS_Sharpe,
                          OOS_CAGR=best.OOS_CAGR, OOS_Sharpe=best.OOS_Sharpe,
                          OOS_MaxDD=best.OOS_MaxDD,
                          interior=int(0 < best.q < 1)))
    PK = pd.DataFrame(picks)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    PK.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  rule-8 picks (chosen on IS Sharpe alone, read OOS):")
    P(PK.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # the live baseline and SPY on the record's own U56 panel, for the comparand row
    px56 = m284.load_universe()
    st = px56.index[260]
    rb = backtest(px56, rules_v2_weights(px56), cost_bps=COST_BPS,
                  freq=FREQ)["returns"].loc[st:]
    rs = px56["SPY"].pct_change().fillna(0.0).loc[st:]
    base = []
    for nm, r in (("RULES v2 (live)", rb), ("SPY (U56)", rs)):
        h = len(r) // 2
        m, o = metrics(r), metrics(r.loc[OOS_START:])
        base.append(dict(book=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                         H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                         OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"]))
    B = pd.DataFrame(base)
    B.to_csv(OUT / f"{STEM}.baseline.csv", index=False)
    P("")
    P("  the standing comparands every cell above is judged against:")
    P(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- headline ---------------------------------------------------------------------------
    interior_claims = len(cl[(cl.q_span > 0) & (cl.q_span < 1)]) if len(cl) else 0
    P("")
    P("=" * 104)
    P(f"HEADLINE A (CENSUS): of {len(cl)} claim-shaped lines naming >= 2 panels, "
      f"{interior_claims} compare panels whose q differs by less than 1.0 and more than 0. "
      f"Corner-to-corner: {int((cl.q_span == 1).sum()) if len(cl) else 0}; "
      f"same-corner: {int((cl.q_span == 0).sum()) if len(cl) else 0}.")
    P(f"HEADLINE B (PRICE): an interior comparand costs {mix_t.secs.mean():.2f}s per panel-arm "
      f"block and lands {len(out1)}/{len(CV)} statistics more than one seed SE off the "
      f"corner-implied line.")
    P(f"HEADLINE C (KEEP): 4a {int(A.pass4a.sum())}/{len(A)}, 4b {int(A.pass4b.sum())}/"
      f"{len(A)} over the whole grid; rule-8 picks at k=40/80 land at q="
      f"{list(PK.pick_q)} arm={list(PK.pick_arm)}.")
    P("=" * 104)
    P(f"elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
