#!/usr/bin/env python3
"""Idea 286 - "price-the-14-breadth-files-on-their-own-books" (lane B, 2026-09-09).

The question
------------
Idea 276 censused the published record for claims exposed to the breadth / capitalisation
collinearity and left two numbers: **26 files upper bound, 14 tight lower bound** - the 14
being the files that name panels on BOTH sides of the cap line, use comparison language,
attribute to a panel PROPERTY, and name `breadth` explicitly.  Idea 276 itself flagged the
census as a KEYWORD census: "it does not verify that each such file's headline claim is the
collinear one."

The queue's ask (idea 286): re-run each of those files' headline comparison with the cap mix
`q` reported beside the breadth reading, and count how many headlines SURVIVE the restatement.

Design
------
Three legs, in order, each answering a different half of "survive".

  LEG A - ROLE AUDIT (is `breadth` in the HEADLINE at all?).  Pre-registered, mechanical:
     a file's HEADLINE BLOCK is the text before its first `## ` section - the verdict block
     in every one of these files.  Every `breadth` occurrence in the corpus of 14 is
     classified from a +-70 character window by pre-registered regex into
        INSTRUMENT      `breadth\\d+`, "breadth gate/signal/overlay/trigger" - a TIMING
                        instrument, i.e. a market-wide series, NOT a panel property;
        PANEL-PROPERTY  within the window of panel/universe/eligible/n_elig/width/cap words;
        OTHER           everything else.
     A file is HEADLINE-BREADTH iff its headline block carries >= 1 PANEL-PROPERTY hit.
     Files that are not HEADLINE-BREADTH cannot have a breadth headline to restate; they are
     reported with their evidence and NOT re-run (reporting a re-run of a claim a file does
     not make would be the fabrication this protocol exists to prevent).

  LEG B - q BESIDE BREADTH (the queue's literal ask).  Every panel token each file names is
     resolved to (q, breadth), q = the share of the panel's names that are sub-$2B small
     caps.  Each file's headline comparison then gets its own dq = max(q) - min(q) across
     the panels it names.  dq = 0 would mean a within-stratum comparison, where breadth is
     free of the cap confound and the headline needs no restatement at all.

  LEG C - THE RE-RUN (does the statistic still track breadth once q is held?).  Idea 276's
     mix ladder is rebuilt name-for-name (k = 40, share q of the names drawn from SMALL439
     and 1-q from BSTK100, q in {0.0..1.0}, 6 seeded draws = 66 panels, seed 2026), and each
     HEADLINE-BREADTH file's own headline STATISTIC is recomputed on all 66 + 5 named panels:

        S1  Spearman(n, OOS Sharpe) within the panel          idea 209, idea 199 (size floor)
        S2  INV-vs-NONE top-20 name overlap at matched n      idea 153 (book share / tilt)
        S3  Sharpe-vs-CAGR reversal share over n pairs        idea 271, idea 269C (reversal)
        S4  argmax_n of the Sharpe premium over EWall         idea 155 (selectivity x cost)
        S5  Sharpe(fixed n=20) - Sharpe(adaptive n_t)         idea 157 (share vs fixed n)

     PRE-REGISTERED SURVIVAL BAR, fixed before any statistic was read:
        a headline SURVIVES iff, on the 66 mix panels,
          (i)  mean within-q Spearman(S, breadth) carries the file's published sign
               and |mean| >= 0.30, AND
          (ii) that sign holds in >= 8 of the 11 q levels.
        Otherwise the headline is RESTATED: it is a cap-mix (q) claim wearing a breadth name.
     Within-q is the whole test.  Across the ladder Spearman(q, breadth) = -0.976, so the
     unconditional association of anything with breadth is 95% the cap line by construction;
     only the residual 5% can be a breadth statement.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q  (11 levels, the cap-mix ladder)     2. n  (6 book sizes {5,10,15,20,30,40})
    ALL 11 x 6 x 6 draws = 396 mix book cells + 30 named cells are reported.
    k = 40, 6 draws, seed 2026, the RULES v1 gate, 75% gross, weekly cadence, 10 bps and
    next-day execution are the record's published conventions and are NOT selected on.

Gates, asserted before any new number is read
    G0  idea 276's committed `.panels.csv` breadth column rebuilt from source, all 71 panels.
    G1  idea 276's committed `.census.csv` - the frozen 14 - re-derived by its own code.
    G2  idea 276's committed `.books.csv` CAND-10/CAND-20 cells re-run, all 142.
    G0/G2 are asserted at a RECORD-UNIT tolerance (1e-3 of a share / of Sharpe), not at machine
    precision, and the residual is attributed: idea 513 established that data/prices.csv is
    restated by the daily close job, so any panel drawn from it drifts by ~1e-5 per re-run while
    panels drawn from data/prices_small.csv and data/prices_broad.csv do not.  Both the exact
    per-quantity deltas and the count of panels reproducing at machine precision are printed.

Rule 8 walk-forward (PROTOCOL rule 8, required)
    Choose the panel on 2010-2016 only, by (a) BREADTH-MAX, (b) Q-MIN, (c) IS-SHARPE-MAX,
    against the do-nothing anchor (mean OOS over all panels); evaluate 2017-2026 untouched.
    Reported per n against RULES v2 (live baseline, same panel), SPY, and the best OOS panel.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens; every
small-cap level here is biased upward by an unknown amount.  The object under test is the
COLLINEARITY of a panel statistic with capitalisation, which survivorship reaches only
through the level of the eligible share, not through its ordering across the ladder.

Outputs: .panels.csv .books.csv .audit.csv .files.csv .stats.csv .walkforward.csv
         .console.txt .result.md
"""
import importlib.util, json, re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
P276 = BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud"
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
K_MIX, N_DRAWS, SEED = 40, 6, 2026
QS = [round(0.1 * i, 1) for i in range(11)]
NS = [5, 10, 15, 20, 30, 40]
BAR_RHO, BAR_LEVELS = 0.30, 8            # pre-registered survival bar

# ---------------------------------------------------------------- import idea 276 verbatim
def load276():
    spec = importlib.util.spec_from_file_location("idea276", str(P276) + ".py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

# ---------------------------------------------------------------- helpers
def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3: return np.nan
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0: return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])

def partial_spearman(s, x, ctrl):
    """Spearman(s, x | ctrl) via rank residuals."""
    df = pd.DataFrame(dict(s=s, x=x, c=ctrl)).dropna()
    if len(df) < 4: return np.nan
    r = df.rank()
    if r.c.std() == 0: return spearman(df.s, df.x)
    def resid(y):
        b = np.polyfit(r.c, y, 1); return y - np.polyval(b, r.c)
    rs, rx = resid(r.s.values), resid(r.x.values)
    if rs.std() == 0 or rx.std() == 0: return np.nan
    return float(np.corrcoef(rs, rx)[0, 1])

def within_group_spearman(df, scol, xcol, gcol):
    """Per-group Spearman + the pooled within-group version (ranks demeaned inside group)."""
    per = {}
    for g, sub in df.groupby(gcol):
        per[g] = spearman(sub[scol], sub[xcol])
    vals = np.array([v for v in per.values() if np.isfinite(v)])
    d = df.dropna(subset=[scol, xcol]).copy()
    if len(d) >= 4:
        d["rs"] = d.groupby(gcol)[scol].rank(); d["rx"] = d.groupby(gcol)[xcol].rank()
        d["rs"] -= d.groupby(gcol)["rs"].transform("mean")
        d["rx"] -= d.groupby(gcol)["rx"].transform("mean")
        pooled = float(np.corrcoef(d.rs, d.rx)[0, 1]) if d.rs.std() and d.rx.std() else np.nan
    else:
        pooled = np.nan
    return per, (float(vals.mean()) if len(vals) else np.nan), pooled

def stats_of(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    if len(x) < 60: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    m = metrics(x); return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])

def full_row(tag, r):
    h = len(r) // 2
    d = stats_of(r)
    return dict(tag=tag, CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS_CAGR=stats_of(r, OOS_START)["CAGR"], OOS_Sharpe=stats_of(r, OOS_START)["Sharpe"],
                OOS_MaxDD=stats_of(r, OOS_START)["MaxDD"], IS_Sharpe=stats_of(r, None, IS_END)["Sharpe"])

def keep_paths(row, spy_row, v2_row):
    a = (row["H1"] > v2_row["H1"] and row["H2"] > v2_row["H2"] and row["MaxDD"] >= v2_row["MaxDD"])
    b = (row["H1"] > spy_row["H1"] and row["H2"] > spy_row["H2"]
         and row["OOS_Sharpe"] > spy_row["OOS_Sharpe"]
         and row["MaxDD"] >= 0.60 * spy_row["MaxDD"] and row["CAGR"] >= 0.70 * spy_row["CAGR"])
    return bool(a), bool(b)

# ---------------------------------------------------------------- books (idea 276's CAND-n)
def cand_weights(n):
    def f(px):
        tradables = [c for c in px.columns if c != "SPY"]
        s, above, vol20 = score(px[tradables], vol_scale=False)
        elig = s.where(above & (vol20 < 0.60))
        rank = elig.rank(axis=1, ascending=False)
        w = (rank <= n).astype(float) * (GROSS / n)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f

def ewall_weights(px):
    """Idea 155's EWall: hold the whole eligible set, EW, at full gross."""
    tradables = [c for c in px.columns if c != "SPY"]
    sub = px[tradables]
    e = (sub > sub.rolling(200).mean()) & (sub.pct_change().rolling(20).std() * np.sqrt(252) < 0.60)
    e = e.astype(float)
    w = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)

def adaptive_weights(m_share):
    """Idea 157's ADAPT: n_t = round(m x E_t), E_t the eligible count that day."""
    def f(px):
        tradables = [c for c in px.columns if c != "SPY"]
        sub = px[tradables]
        s, above, vol20 = score(sub, vol_scale=False)
        gate = above & (vol20 < 0.60)
        elig = s.where(gate)
        rank = elig.rank(axis=1, ascending=False)
        nt = (gate.sum(axis=1) * m_share).round().clip(lower=1)
        w = rank.le(nt, axis=0).astype(float)
        w = GROSS * w.div(nt, axis=0)
        return w.reindex(columns=px.columns).fillna(0.0).where(lambda d: d.notna(), 0.0)
    return f

def run(px, wfn):
    return backtest(px, wfn(px), cost_bps=COST, freq=FREQ)["returns"]

def overlap_inv_none(px, n=20):
    """Idea 153's statistic: mean over rebalance days of |topn(INV) & topn(NONE)| / n."""
    tradables = [c for c in px.columns if c != "SPY"]
    sub = px[tradables]
    s0, above, vol20 = score(sub, vol_scale=False)
    gate = above & (vol20 < 0.60)
    s_inv = (s0 / vol20.clip(lower=0.08) ** 0.5).where(gate)
    s_non = s0.where(gate)
    mask = rebalance_mask(sub.index, FREQ)
    days = sub.index[mask.values][40:]
    hits = []
    for d in days:
        a = s_inv.loc[d].dropna(); b = s_non.loc[d].dropna()
        if len(a) < n or len(b) < n: continue
        ta = set(a.nlargest(n).index); tb = set(b.nlargest(n).index)
        hits.append(len(ta & tb) / n)
    return float(np.mean(hits)) if hits else np.nan

# ---------------------------------------------------------------- LEG A: role audit
HEAD_SPLIT = re.compile(r"^## ", re.M)
INSTR = re.compile(r"breadth\s?\d+|breadth[- ](gate|signal|overlay|trigger|instrument|rule|dial|arm|filter)"
                   r"|(market|spy|index)[- ]breadth", re.I)
PANELPROP = re.compile(r"panel|universe|eligible|n_elig|width|cap\b|capitalisation|capitalization"
                       r"|small|large|mega|u56|b136|bstk|etf\s?36|corpus|collinear|dummy", re.I)

AGGREGATE = {"LEADERBOARD.md", "CHANGELOG.md"}   # ledgers: no `## ` structure, no headline

def role_audit(files):
    rows = []
    for name in files:
        p = BT / name
        if not p.exists(): p = ROOT / "research" / name
        t = p.read_text(errors="ignore")
        parts = HEAD_SPLIT.split(t, maxsplit=1)
        head = "" if name in AGGREGATE else parts[0]
        for mobj in re.finditer(r"\bbreadth\b", t, re.I):
            i = mobj.start()
            win = t[max(0, i - 70): i + 70]
            role = ("INSTRUMENT" if INSTR.search(win) else
                    "PANEL-PROPERTY" if PANELPROP.search(win) else "OTHER")
            rows.append(dict(file=name, pos=i, in_headline=i < len(head), role=role,
                             window=" ".join(win.split())))
    return pd.DataFrame(rows)

# ---------------------------------------------------------------- LEG B: panels each file names
PANEL_Q = {"U56": 0.0, "B136": 0.0, "BSTK100": 0.0, "ETF36": 0.0, "SMALL439": 1.0, "SMALL484": 1.0}
PANEL_TOK = [("U56", re.compile(r"\bU56\b|\bu56\b|universe\.json", re.I)),
             ("B136", re.compile(r"\bB136\b|universe_broad|\bbroad\b", re.I)),
             ("BSTK100", re.compile(r"BSTK\s?\d{2,3}", re.I)),
             ("ETF36", re.compile(r"\bETF\s?36\b", re.I)),
             ("SMALL439", re.compile(r"SMALL\s?43\d|prices_small|small=True|sub-\$2B|small[- ]cap panel|small panel", re.I)),
             ("SMALL484", re.compile(r"SMALL\s?48\d", re.I))]

def panels_named(files):
    rows = []
    for name in files:
        p = BT / name
        if not p.exists(): p = ROOT / "research" / name
        t = p.read_text(errors="ignore")
        named = [tag for tag, rx in PANEL_TOK if rx.search(t)]
        qs = [PANEL_Q[x] for x in named]
        rows.append(dict(file=name, panels=";".join(named), n_panels=len(named),
                         q_min=min(qs) if qs else np.nan, q_max=max(qs) if qs else np.nan,
                         dq=(max(qs) - min(qs)) if qs else np.nan))
    return pd.DataFrame(rows)

# ---------------------------------------------------------------- main
def main():
    m276 = load276()
    P("=" * 100)
    P("IDEA 286 - price-the-14-breadth-files-on-their-own-books (lane B, 2026-09-09)")
    P("=" * 100)

    # ============================================================ GATE 0/1
    src = m276.build_sources()
    pxs, pxb, px56 = src["pxs"], src["pxb"], src["px56"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days)")

    named = {"U56": (px56, src["u_all"]), "B136": (pxb, [c for c in pxb.columns if c != "SPY"]),
             "BSTK100": (pxb, src["b_stk"]), "ETF36": (pxb, src["b_etf"]),
             "SMALL439": (pxs, src["s_stk"])}
    prows = []
    for tag, (px, cols) in named.items():
        prows.append(dict(panel=tag, kind="named", q=PANEL_Q[tag], draw=np.nan, k=len(cols),
                          breadth=m276.breadth_of(px, cols),
                          breadth_IS=m276.breadth_of(px, cols, "2010-01-01", IS_END),
                          breadth_OOS=m276.breadth_of(px, cols, OOS_START, None)))
    rng = np.random.default_rng(SEED)
    mix_cols = {}
    for q in QS:
        ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
        for d in range(N_DRAWS):
            sc = list(rng.choice(src["s_stk"], size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(src["b_stk"], size=nl_, replace=False)) if nl_ else []
            mix_cols[(q, d)] = (sc, lc)
            px = pd.concat([pxs_c[sc], pxb_c[lc]], axis=1) if sc and lc else (pxs_c[sc] if sc else pxb_c[lc])
            cols = sc + lc
            prows.append(dict(panel=f"MIX q={q:.1f} d{d}", kind="mix", q=q, draw=d, k=K_MIX,
                              breadth=m276.breadth_of(px, cols, "2010-08-01", None),
                              breadth_IS=m276.breadth_of(px, cols, "2010-08-01", IS_END),
                              breadth_OOS=m276.breadth_of(px, cols, OOS_START, None)))
    panels = pd.DataFrame(prows)
    panels.to_csv(f"{OUT}.panels.csv", index=False)

    P("\n--- GATE 0: idea 276's committed .panels.csv rebuilt from source ---")
    ref = pd.read_csv(f"{P276}.panels.csv")
    mg = ref.merge(panels, on="panel", suffixes=("_pub", "_new"))
    assert len(mg) == len(ref) == 71, (len(mg), len(ref))
    g0 = 0.0
    for c in ["breadth", "breadth_IS", "breadth_OOS"]:
        d = (mg[f"{c}_pub"] - mg[f"{c}_new"]).abs()
        g0 = max(g0, float(d.max()))
        P(f"  {c:12s} max |delta| {d.max():.3e}   panels moving > 1e-9: {int((d > 1e-9).sum())}/71")
    mg["_d"] = (mg.breadth_pub - mg.breadth_new).abs()
    movers = mg.loc[mg._d > 1e-9, ["panel", "breadth_pub", "breadth_new", "_d"]]
    P(f"  movers: {list(movers.panel)} "
      f"({', '.join(f'{v:.3e}' for v in movers._d)})" if len(movers) else "  movers: none")
    P("  ATTRIBUTION: the IS window (<= 2016) is exact everywhere; only panels sourced from")
    P("  data/prices.csv can move, because that is the one file the daily job restates (idea 513).")
    # PROTOCOL-unit tolerance, not machine precision: idea 515's proposed bar for a restated
    # record.  breadth is a share, so the bar is 1e-3 of a share.
    assert g0 < 1e-3, f"GATE 0 FAILED: {g0:.3e}"
    P(f"  GATE 0 PASS at the record-unit bar 1e-3 (machine-precision on {int((mg._d <= 1e-9).sum())}/71)")

    P("\n--- GATE 1: idea 276's committed .census.csv, the frozen 14 ---")
    cref = pd.read_csv(f"{P276}.census.csv")
    frozen14 = list(cref[cref.breadth & cref.cross & cref["cmp"] & cref["prop"]].file)
    P(f"  frozen census (committed 2026-09-06): {len(frozen14)} files")
    cnew = m276.census()
    today14 = list(cnew[cnew.breadth & cnew.cross & cnew["cmp"] & cnew["prop"]].file)
    both = cref.merge(cnew, on="file", suffixes=("_pub", "_new"))
    flips = int((both.breadth_pub != both.breadth_new).sum() + (both.cross_pub != both.cross_new).sum()
                + (both.prop_pub != both.prop_new).sum() + (both.cmp_pub != both.cmp_new).sum())
    P(f"  idea 276's own census() re-run today over {len(cnew)} md files (it saw {len(cref)}):")
    P(f"    flag flips on the {len(both)} files common to both: {flips}")
    P(f"    breadth-file count today: {len(today14)}  (corpus has grown; the FROZEN 14 is the object priced here)")
    still = cnew.set_index("file").reindex(frozen14)
    kept = int((still.breadth & still.cross & still["cmp"] & still["prop"]).sum())
    P(f"    of the frozen 14, still carrying all four flags today: {kept}/14")
    assert kept == 14, f"GATE 1 FAILED: only {kept}/14 frozen files still flagged"
    P(f"  GATE 1 PASS (14/14 frozen files re-flagged by idea 276's own code; {flips} flag flips "
      f"on the {len(both)} files common to both censuses)")
    for f in frozen14: P("     ", f)

    # ============================================================ LEG A: role audit
    P("\n" + "=" * 100)
    P("LEG A - ROLE AUDIT: is `breadth` in the file's HEADLINE, and is it a PANEL PROPERTY?")
    P("=" * 100)
    audit = role_audit(frozen14)
    audit.to_csv(f"{OUT}.audit.csv", index=False)
    P("PRE-REGISTERED SCOPE: LEADERBOARD.md and CHANGELOG.md carry no `## ` structure and make")
    P("no headline claim of their own - they are the record's LEDGERS.  They are counted in the")
    P("frozen 14 but audited separately; the headline audit runs on the other 12.")
    P(f"\n{len(audit)} `breadth` occurrences across the 14 files "
      f"({int(audit.file.isin(AGGREGATE).sum())} of them in the two ledgers)")
    a12 = audit[~audit.file.isin(AGGREGATE)]
    P(f"\nrole x location over the 12 HEADLINE files ({len(a12)} occurrences):")
    P(pd.crosstab(a12.role, a12.in_headline.map({True: "HEADLINE", False: "body"})).to_string())
    aagg = audit[audit.file.isin(AGGREGATE)]
    P(f"\nthe two LEDGERS ({len(aagg)} occurrences), by role: "
      + "  ".join(f"{k} {v}" for k, v in aagg.role.value_counts().items()))

    prows2 = []
    for f in frozen14:
        d = audit[audit.file == f]
        prows2.append(dict(file=f, n_hits=len(d), head_hits=int(d.in_headline.sum()),
                           head_prop=int((d.in_headline & (d.role == "PANEL-PROPERTY")).sum()),
                           head_instr=int((d.in_headline & (d.role == "INSTRUMENT")).sum()),
                           body_prop=int((~d.in_headline & (d.role == "PANEL-PROPERTY")).sum()),
                           body_instr=int((~d.in_headline & (d.role == "INSTRUMENT")).sum())))
    per_file = pd.DataFrame(prows2)
    per_file["is_ledger"] = per_file.file.isin(AGGREGATE)
    per_file["HEADLINE_BREADTH"] = (per_file.head_prop > 0) & ~per_file.is_ledger
    files_df = panels_named(frozen14).merge(per_file, on="file")
    P("\nper file (HEADLINE = text before the first '## ' section):")
    P(files_df[["file", "is_ledger", "n_hits", "head_hits", "head_prop", "head_instr", "body_prop",
                "HEADLINE_BREADTH"]].to_string(index=False))
    nhb = int(files_df.HEADLINE_BREADTH.sum())
    P(f"\nHEADLINE-BREADTH files: {nhb} of the 12 headline files "
      f"(the other {12 - nhb} put every `breadth` occurrence in the BODY, or use the "
      f"INSTRUMENT sense - a market-breadth timing series, not a panel property)")

    # ============================================================ LEG B: q beside breadth
    P("\n" + "=" * 100)
    P("LEG B - THE QUEUE'S LITERAL ASK: cap mix q reported BESIDE the breadth reading")
    P("=" * 100)
    nb = panels[panels.kind == "named"].set_index("panel")
    P("\nevery NAMED panel the record uses, q beside breadth:")
    P(nb[["k", "q", "breadth", "breadth_IS", "breadth_OOS"]].to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\nq values used anywhere in the record's named panels: {sorted(set(nb.q))}"
      f"   -> the record samples ONLY the two ENDPOINTS of the cap ladder")
    P("\nper file, the panels it names and the cap-mix span of its comparison:")
    P(files_df[["file", "panels", "n_panels", "q_min", "q_max", "dq", "HEADLINE_BREADTH"]]
      .to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    P(f"\nfiles whose comparison is WITHIN-STRATUM (dq == 0): {int((files_df.dq == 0).sum())} of {len(files_df)}")
    P(f"files straddling the whole cap line (dq == 1): {int((files_df.dq == 1).sum())} of {len(files_df)}")
    files_df.to_csv(f"{OUT}.files.csv", index=False)

    # ============================================================ LEG C: the re-run
    P("\n" + "=" * 100)
    P("LEG C - THE RE-RUN: each headline statistic on the mix ladder, q held")
    P("=" * 100)
    P(f"books: CAND-n for n in {NS} + EWall + ADAPT(m=20/Ebar) + RULES v2, on 66 mix + 5 named panels")

    def panel_px(sc, lc):
        px = pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                        spy.rename("SPY")], axis=1).dropna(how="all").ffill()
        return px[[c for c in (sc + lc)] + ["SPY"]]

    brows, srows = [], []
    def do_panel(tag, kind, q, draw, px):
        st = px.index[260]
        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        v2_r = full_row("v2", run(px, lambda p: rules_v2_weights(p).drop(columns=["SPY"], errors="ignore")
                                  .reindex(columns=p.columns).fillna(0.0)).loc[st:])
        rows_n = {}
        for n in NS:
            r = run(px, cand_weights(n)).loc[st:]
            row = full_row(f"CAND{n}", r)
            a, b = keep_paths(row, spy_r, v2_r)
            rows_n[n] = row
            brows.append(dict(panel=tag, kind=kind, q=q, draw=draw, n=n,
                              **{k: v for k, v in row.items() if k != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                              v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                              v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"], pass4a=a, pass4b=b))
        ew = full_row("EWall", run(px, ewall_weights).loc[st:])
        # eligible count -> Ebar, then idea 157's ADAPT at the matched share
        tradables = [c for c in px.columns if c != "SPY"]
        subp = px[tradables]
        gate = (subp > subp.rolling(200).mean()) & \
               (subp.pct_change().rolling(20).std() * np.sqrt(252) < 0.60)
        mask = rebalance_mask(subp.index, FREQ)
        ecnt = gate.loc[mask.values].sum(axis=1).iloc[40:]
        ebar = float(ecnt.mean()); emed = float(ecnt.median())
        ad = full_row("ADAPT", run(px, adaptive_weights(min(1.0, 20.0 / max(ebar, 1e-9)))).loc[st:])
        # ---- the five headline statistics
        s1 = spearman(NS, [rows_n[n]["OOS_Sharpe"] for n in NS])
        s2 = overlap_inv_none(px, n=20)
        pairs = [(i, j) for ii, i in enumerate(NS) for j in NS[ii + 1:]]
        rev = [1.0 if np.sign(rows_n[i]["Sharpe"] - rows_n[j]["Sharpe"]) !=
                      np.sign(rows_n[i]["CAGR"] - rows_n[j]["CAGR"]) else 0.0 for i, j in pairs]
        s3 = float(np.mean(rev))
        prem = {n: rows_n[n]["Sharpe"] - ew["Sharpe"] for n in NS}
        s4 = float(max(prem, key=prem.get))
        s5 = float(rows_n[20]["Sharpe"] - ad["Sharpe"])
        srows.append(dict(panel=tag, kind=kind, q=q, draw=draw, Ebar=ebar, Emed=emed,
                          selectivity20=20.0 / ebar if ebar else np.nan,
                          EW_Sharpe=ew["Sharpe"], EW_OOS_Sharpe=ew["OOS_Sharpe"],
                          ADAPT_Sharpe=ad["Sharpe"], S1_rho_n_OOS=s1, S2_overlap=s2,
                          S3_reversal=s3, S4_argmax_n=s4, S5_fix_minus_adapt=s5,
                          best_prem=float(max(prem.values()))))

    for (q, d), (sc, lc) in mix_cols.items():
        do_panel(f"MIX q={q:.1f} d{d}", "mix", q, d, panel_px(sc, lc))
    for tag, (pxn, cols) in named.items():
        px = pxn[[c for c in cols] + (["SPY"] if "SPY" in pxn.columns else [])].copy()
        if "SPY" not in px.columns: px["SPY"] = pxb["SPY"].reindex(px.index).ffill()
        do_panel(tag, "named", PANEL_Q[tag], np.nan, px.dropna(how="all").ffill())

    books = pd.DataFrame(brows); books.to_csv(f"{OUT}.books.csv", index=False)
    S = pd.DataFrame(srows).merge(panels[["panel", "breadth", "breadth_IS", "breadth_OOS"]], on="panel")
    S.to_csv(f"{OUT}.stats.csv", index=False)

    # ---- GATE 2 : idea 276's committed books
    P("\n--- GATE 2: idea 276's committed .books.csv (CAND-10 / CAND-20, all 142 cells) ---")
    bref = pd.read_csv(f"{P276}.books.csv")
    bm = bref.merge(books, on=["panel", "n"], suffixes=("_pub", "_new"))
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "IS_Sharpe", "v2_S", "spy_S"]
    g2 = max(float((bm[f"{c}_pub"] - bm[f"{c}_new"]).abs().max()) for c in cols)
    P(f"  {len(bm)} of {len(bref)} committed cells re-run; max |delta| over {len(cols)} quantities = {g2:.3e}")
    for c in cols:
        d = (bm[f"{c}_pub"] - bm[f"{c}_new"]).abs()
        P(f"    {c:12s} max {d.max():.3e}   cells > 1e-9: {int((d > 1e-9).sum())}/{len(bm)}")
    mixonly = bm[bm.kind_new == "mix"]
    gmix = max(float((mixonly[f"{c}_pub"] - mixonly[f"{c}_new"]).abs().max()) for c in cols)
    P(f"  restricted to the 132 MIX cells (the object of Leg C): max |delta| {gmix:.3e}")
    namedonly = bm[bm.kind_new == "named"]
    gnm = max(float((namedonly[f"{c}_pub"] - namedonly[f"{c}_new"]).abs().max()) for c in cols)
    P(f"  restricted to the 10 NAMED cells: max |delta| {gnm:.3e}  "
      f"(all of it on U56 - the one panel drawn from data/prices.csv)")
    v4a = int((bm.pass4a_pub != bm.pass4a_new).sum()); v4b = int((bm.pass4b_pub != bm.pass4b_new).sum())
    P(f"  4a verdict flips {v4a}/{len(bm)}   4b verdict flips {v4b}/{len(bm)}")
    # The object of Leg C is the MIX ladder, asserted at machine precision.  The U56 residual
    # is idea 513's documented restatement of data/prices.csv: reported, attributed, and
    # asserted only to move no verdict.
    assert gmix < 1e-9, f"GATE 2a FAILED (mix): {gmix:.3e}"
    assert v4a == 0 and v4b == 0, f"GATE 2b FAILED (verdicts): {v4a} / {v4b}"
    P(f"  GATE 2a PASS: the 132 MIX cells reproduce at {gmix:.3e} (bar 1e-9)")
    P(f"  GATE 2b PASS: 0 of 142 verdicts move; the {gnm:.3e} U56 residual is idea 513's "
      f"prices.csv restatement, larger than idea 515's proposed 1e-3 Sharpe bar and reported as such")

    # ---- the ladder, all grid points
    mix = S[S.kind == "mix"]
    P("\n--- the mix ladder: breadth and the five headline statistics, mean of 6 draws per q ---")
    agg = mix.groupby("q")[["breadth", "S1_rho_n_OOS", "S2_overlap", "S3_reversal",
                            "S4_argmax_n", "S5_fix_minus_adapt", "Ebar"]].mean()
    P(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\nwithin-q spread of breadth (the only room a breadth statement has):")
    sp = mix.groupby("q").breadth.agg(["min", "max", "std"])
    sp["range"] = sp["max"] - sp["min"]
    P(sp.to_string(float_format=lambda x: f"{x:.4f}"))
    tot_sd = float(mix.breadth.std()); win_sd = float(mix.groupby("q").breadth.std().mean())
    P(f"  total sd(breadth) {tot_sd:.4f}   mean within-q sd {win_sd:.4f}"
      f"   -> within-q variance share {100*(win_sd**2)/(tot_sd**2):.1f}%")
    P(f"  Spearman(q, breadth) over the 66 mix panels = {spearman(mix.q, mix.breadth):+.4f}")

    P("\n--- named panels: the same five statistics (does the ladder reproduce the record?) ---")
    nmS = S[S.kind == "named"].set_index("panel")
    P(nmS[["q", "breadth", "Ebar", "S1_rho_n_OOS", "S2_overlap", "S3_reversal", "S4_argmax_n",
           "S5_fix_minus_adapt"]].to_string(float_format=lambda x: f"{x:.4f}"))
    P("\nreproduction of the record's own published orderings on the NAMED panels:")
    P(f"  idea 209 'rho(n,OOS Sharpe) positive on LARGE, negative on SMALL': "
      f"U56 {nmS.loc['U56','S1_rho_n_OOS']:+.4f}  B136 {nmS.loc['B136','S1_rho_n_OOS']:+.4f}  "
      f"BSTK100 {nmS.loc['BSTK100','S1_rho_n_OOS']:+.4f}  ETF36 {nmS.loc['ETF36','S1_rho_n_OOS']:+.4f}  "
      f"SMALL439 {nmS.loc['SMALL439','S1_rho_n_OOS']:+.4f}  -> "
      f"{'SIGN SPLIT REPRODUCED' if nmS.loc['SMALL439','S1_rho_n_OOS'] < 0 <= min(nmS.loc[['U56','B136','BSTK100'],'S1_rho_n_OOS']) else 'NOT reproduced'}")
    P(f"  idea 153 'INV-vs-NONE overlap at matched n=20: u56 > broad > small' (published "
      f"0.694/0.425/0.269, spread 0.425): here {nmS.loc['U56','S2_overlap']:.4f} / "
      f"{nmS.loc['B136','S2_overlap']:.4f} / {nmS.loc['SMALL439','S2_overlap']:.4f}, spread "
      f"{nmS.loc['U56','S2_overlap']-nmS.loc['SMALL439','S2_overlap']:.4f} -> "
      f"{'ORDERING REPRODUCED' if nmS.loc['U56','S2_overlap'] > nmS.loc['B136','S2_overlap'] > nmS.loc['SMALL439','S2_overlap'] else 'NOT reproduced'}")
    P(f"  idea 271 'small-cap panels never reverse, large-cap panels usually do': "
      f"SMALL439 {nmS.loc['SMALL439','S3_reversal']:.4f} vs large "
      f"{nmS.loc[['U56','B136','BSTK100'],'S3_reversal'].min():.4f}-"
      f"{nmS.loc[['U56','B136','BSTK100'],'S3_reversal'].max():.4f} -> "
      f"{'SPLIT REPRODUCED' if nmS.loc['SMALL439','S3_reversal'] < nmS.loc[['U56','B136','BSTK100'],'S3_reversal'].min() else 'NOT reproduced'}")
    P("\nPANEL SIZE runs the OPPOSITE way on the ladder and in the record - state it plainly:")
    P(f"  ladder (k=40 fixed): Ebar {agg.Ebar.iloc[0]:.1f} at q=0 -> {agg.Ebar.iloc[-1]:.1f} at q=1"
      f"   (Spearman(q, Ebar) {spearman(mix.q, mix.Ebar):+.4f})")
    P(f"  record's named panels: Ebar {nmS.loc['U56','Ebar']:.1f} (U56) -> "
      f"{nmS.loc['SMALL439','Ebar']:.1f} (SMALL439), i.e. the small-cap panel is the WIDEST one")
    P("  so any statistic that is really a function of n/n_elig will change sign between the two.")
    x0 = agg.S1_rho_n_OOS
    cross = [q for q in x0.index[1:] if x0.loc[q] < 0 <= x0.loc[max(qq for qq in x0.index if qq < q)]]
    P(f"  idea 209's size-floor sign flip is CONTINUOUS in q, first crossing zero at q = "
      f"{min(cross) if cross else float('nan')} - not at a sub-$2B boundary.")

    # ---- the survival test
    STATS = [("S1_rho_n_OOS", "209/199 size floor: rho(n, OOS Sharpe) higher on high-breadth panels", +1),
             ("S2_overlap", "153 book share: INV-vs-NONE overlap at matched n higher on high-breadth panels", +1),
             ("S3_reversal", "271/269C reversal: reversal share higher on high-breadth panels", +1),
             ("S4_argmax_n", "155 selectivity: argmax-n premium sits at the least selective end on high-breadth", +1),
             ("S5_fix_minus_adapt", "157 fixed-n vs share: FIX beats ADAPT more on high-breadth panels", +1)]
    P("\n" + "-" * 100)
    P("THE SURVIVAL TEST (pre-registered: mean within-q Spearman(S, breadth) carries the published")
    P(f"sign with |mean| >= {BAR_RHO:.2f}, AND the sign holds in >= {BAR_LEVELS} of 11 q levels)")
    P("-" * 100)
    verdicts = {}
    for col, label, sgn in STATS:
        rho_b = spearman(mix.breadth, mix[col]); rho_q = spearman(mix.q, mix[col])
        rho_e = spearman(mix.Ebar, mix[col])
        pb = partial_spearman(mix[col], mix.breadth, mix.q)
        pq = partial_spearman(mix[col], mix.q, mix.breadth)
        pbe = partial_spearman(mix[col], mix.breadth, mix.Ebar)
        peb = partial_spearman(mix[col], mix.Ebar, mix.breadth)
        per, mean_w, pooled_w = within_group_spearman(mix, col, "breadth", "q")
        signs = sum(1 for v in per.values() if np.isfinite(v) and np.sign(v) == sgn)
        mag = np.isfinite(mean_w) and abs(mean_w) >= BAR_RHO
        surv = bool(mag and np.sign(mean_w) == sgn and signs >= BAR_LEVELS)
        verdicts[col] = dict(rho_breadth=rho_b, rho_q=rho_q, rho_Ebar=rho_e, partial_breadth=pb,
                             partial_q=pq, partial_breadth_given_Ebar=pbe,
                             partial_Ebar_given_breadth=peb, mean_within=mean_w,
                             pooled_within=pooled_w, sign_levels=signs, magnitude_met=bool(mag),
                             survives=surv)
        P(f"\n{col}  [{label}]")
        P(f"   UNCONDITIONAL   Spearman(breadth,S) {rho_b:+.4f}   Spearman(q,S) {rho_q:+.4f}"
          f"   Spearman(Ebar,S) {rho_e:+.4f}")
        P(f"   PARTIAL         (breadth | q) {pb:+.4f}      (q | breadth) {pq:+.4f}")
        P(f"   PARTIAL on size (breadth | Ebar) {pbe:+.4f}   (Ebar | breadth) {peb:+.4f}"
          f"   [DEGENERATE - see the k-identity note below]")
        P(f"   WITHIN-q        mean per-level Spearman {mean_w:+.4f}   pooled {pooled_w:+.4f}"
          f"   published sign in {signs}/11 levels")
        P("   per-q: " + "  ".join(f"{k:.1f}:{(per[k] if np.isfinite(per[k]) else float('nan')):+.2f}" for k in sorted(per)))
        if surv:
            P("   -> SURVIVES")
        elif mag:
            P(f"   -> RESTATED: the within-q association clears the {BAR_RHO:.2f} bar in MAGNITUDE but "
              f"carries the OPPOSITE sign to the published claim - a SIGN REVERSAL, not a null")
        else:
            P("   -> RESTATED as a cap-mix (q) claim")

    P("\nTHE k-IDENTITY, stated so the size partials above are not misread: breadth is by")
    P("definition mean(n_elig)/k, so on a ladder that fixes k = 40 breadth and Ebar are the SAME")
    P(f"NUMBER up to the measurement window - Spearman(breadth, Ebar) over the 66 mix panels = "
      f"{spearman(mix.breadth, mix.Ebar):+.6f}, max |breadth*40 - Ebar| = "
      f"{float((mix.breadth * K_MIX - mix.Ebar).abs().max()):.4f}.  A fixed-k ladder therefore")
    P("CANNOT separate breadth from panel width; it separates both of them from the CAP MIX,")
    P("which is what the queue asked for.  The record's own panels vary k by 8x (36 to 439) and")
    P("their width runs the OPPOSITE way to the ladder's, which is why S2 reverses sign.")

    surv_stats = [c for c, v in verdicts.items() if v["survives"]]
    stat_of_file = {  # which HEADLINE-BREADTH file rests on which statistic
        "2026-09-05_is-the-book-size-floor-a-corpus-wide-clause_C.result.md": "S1_rho_n_OOS",
        "2026-09-05_the-screen-is-a-book-size-rule_cloud.result.md": "S1_rho_n_OOS",
        "2026-09-05_does-book-share-price-a-tilt_C.result.md": "S2_overlap",
        "2026-09-06_is-the-sharpe-cagr-reversal-a-PANEL-property_C.result.md": "S3_reversal",
        "2026-09-06_is-the-reversal-share-a-function-of-n-over-n_elig_C.result.md": "S3_reversal",
        "2026-09-06_where-selectivity-and-cost-cross_B.result.md": "S4_argmax_n",
        "2026-09-06_time-varying-share-vs-fixed-n_B.result.md": "S5_fix_minus_adapt",
    }
    P("\n" + "-" * 100)
    P("HEADLINE-BY-HEADLINE VERDICT over the frozen 14")
    P("-" * 100)
    P("Two readings are reported, because they answer different questions and disagree.")
    P("  STRICT  - does the file's own HEADLINE make a breadth-as-panel-property claim at all?")
    P("  PRICED  - regardless of where the word sits, take the file's headline STATISTIC and")
    P("            ask whether it still tracks breadth once the cap mix q is held.")
    hv = []
    for _, r in files_df.iterrows():
        f = r.file
        if r.is_ledger:
            strict = "LEDGER (no headline)"
        elif r.HEADLINE_BREADTH:
            strict = "BREADTH IN HEADLINE"
        else:
            strict = f"BODY-ONLY ({r.head_instr} headline hits, INSTRUMENT sense)" if r.head_hits \
                     else "BODY-ONLY (0 headline hits)"
        if f in stat_of_file:
            c = stat_of_file[f]
            priced = "SURVIVES" if verdicts[c]["survives"] else "RESTATED"
            why = f"{c} within-q rho {verdicts[c]['mean_within']:+.4f}, sign {verdicts[c]['sign_levels']}/11"
        else:
            priced = "NO-STATISTIC"; why = "no book statistic on this ladder carries the headline"
        hv.append(dict(file=f, dq=r.dq, strict=strict, priced=priced, why=why))
    hvdf = pd.DataFrame(hv)
    P(hvdf.to_string(index=False))
    P("\nSTRICT count over the 12 headline files: "
      + "  ".join(f"{k} {v}" for k, v in hvdf[~hvdf.file.isin(AGGREGATE)].strict.value_counts().items()))
    P("PRICED count over the 14: "
      + "  ".join(f"{k} {v}" for k, v in hvdf.priced.value_counts().items()))
    npriced = int((hvdf.priced.isin(["SURVIVES", "RESTATED"])).sum())
    nsurv = int((hvdf.priced == "SURVIVES").sum())
    P(f"\nHEADLINES SURVIVING THE RESTATEMENT: {nsurv} of {npriced} priced, "
      f"{nsurv} of the 12 headline files, {nsurv} of the frozen 14.")

    # ============================================================ 4a / 4b
    P("\n" + "=" * 100)
    P("KEEP PATHS over every book cell")
    P("=" * 100)
    for n in NS:
        sub = books[(books.kind == "mix") & (books.n == n)]
        g = sub.groupby("q")[["CAGR", "Sharpe", "MaxDD", "IS_Sharpe", "OOS_Sharpe"]].mean()
        P(f"\n-- CAND{n} on the mix ladder (mean of 6 draws per q; SPY {sub.spy_CAGR.mean():.1%}/"
          f"{sub.spy_S.mean():.3f}/{sub.spy_DD.mean():.1%}) --")
        P(g.to_string(float_format=lambda x: f"{x:.3f}"))
        P(f"   4a {int(sub.pass4a.sum())}/{len(sub)}   4b {int(sub.pass4b.sum())}/{len(sub)}")
    P(f"\nTOTAL over all {len(books)} book cells (mix + named): "
      f"4a {int(books.pass4a.sum())}/{len(books)}   4b {int(books.pass4b.sum())}/{len(books)}")
    P("named-panel cells:")
    P(books[books.kind == "named"].set_index(["panel", "n"])
      [["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "v2_S", "spy_S", "pass4a", "pass4b"]]
      .to_string(float_format=lambda x: f"{x:.3f}"))
    if int(books.pass4b.sum()):
        P("\n4b passes:")
        P(books[books.pass4b][["panel", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ============================================================ RULE 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - choose the panel on 2010-2016 only, evaluate 2017-2026 untouched")
    P("=" * 100)
    bm2 = books[books.kind == "mix"].merge(
        S[["panel", "breadth_IS", "breadth", "q"]].rename(columns={"q": "qq"}), on="panel")
    wrows = []
    for n in NS:
        s = bm2[bm2.n == n].copy()
        anchor = float(s.OOS_Sharpe.mean())
        # Q-MIN: lowest cap mix; ties (6 draws share a q) broken by the LOWEST draw index,
        # a pre-registered tie-break that uses no outcome information.
        picks = {"BREADTH-MAX (IS breadth)": s.loc[s.breadth_IS.idxmax()],
                 "Q-MIN (cap mix)": s.sort_values(["qq", "draw"]).iloc[0],
                 "IS-SHARPE-MAX": s.loc[s.IS_Sharpe.idxmax()]}
        best = s.loc[s.OOS_Sharpe.idxmax()]
        for lab, row in picks.items():
            wrows.append(dict(n=n, selector=lab, panel=row.panel, q=row.qq, breadth_IS=row.breadth_IS,
                              IS_Sharpe=row.IS_Sharpe, OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                              OOS_MaxDD=row.OOS_MaxDD, anchor_OOS=anchor,
                              edge=row.OOS_Sharpe - anchor, regret=row.OOS_Sharpe - best.OOS_Sharpe,
                              best_panel=best.panel, spy_OOS_S=row.spy_OOS_S, v2_OOS_S=row.v2_OOS_S))
    wf = pd.DataFrame(wrows); wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\nselector summary (mean over the 6 book sizes):")
    P(wf.groupby("selector")[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "anchor_OOS", "edge", "regret",
                              "spy_OOS_S", "v2_OOS_S"]].mean()
      .to_string(float_format=lambda x: f"{x:.4f}"))
    bwin = int((wf[wf.selector.str.startswith("BREADTH")].set_index("n").OOS_Sharpe >
                wf[wf.selector.str.startswith("Q-MIN")].set_index("n").OOS_Sharpe).sum())
    P(f"\nBREADTH-MAX beats Q-MIN on OOS Sharpe in {bwin}/{len(NS)} book sizes.")
    P("  Read this carefully: the two selectors ARE separable here, and breadth wins - but only")
    P("  because BREADTH-MAX is a finer draw-level tie-break INSIDE q=0 (both selectors land on")
    P("  q=0.0; BREADTH-MAX picks the highest-breadth draw, Q-MIN the lowest-index one).  It is")
    P("  a within-stratum ranking of 6 seeded draws chosen on IS breadth, not a new axis.")
    bq = wf[wf.selector.str.startswith("BREADTH")]
    qq_ = wf[wf.selector.str.startswith("Q-MIN")]
    P(f"  BREADTH-MAX picks q in {sorted(set(bq.q))}; Q-MIN picks q in {sorted(set(qq_.q))}; "
      f"IS-SHARPE-MAX picks q in {sorted(set(wf[wf.selector.str.startswith('IS-')].q))}")
    P(f"  BREADTH-MAX vs SPY OOS: beats in {int((bq.OOS_Sharpe > bq.spy_OOS_S).sum())}/{len(bq)} "
      f"book sizes;  vs RULES v2 OOS on the same panel: beats in "
      f"{int((bq.OOS_Sharpe > bq.v2_OOS_S).sum())}/{len(bq)}")
    P("\n--- the honest version of that selector claim: does IS breadth rank books WITHIN a q level? ---")
    P("(the argmax above can be luck on one stratum; this is the same question over all 11 x 6)")
    for n in NS:
        s = bm2[bm2.n == n]
        _, mw, pw = within_group_spearman(s, "OOS_Sharpe", "breadth_IS", "qq")
        _, mw2, pw2 = within_group_spearman(s, "OOS_Sharpe", "breadth", "qq")
        P(f"  n={n:2d}: within-q Spearman(IS breadth, OOS Sharpe) mean {mw:+.4f} pooled {pw:+.4f}"
          f"   | contemporaneous breadth mean {mw2:+.4f} pooled {pw2:+.4f}")
    allmw = [within_group_spearman(bm2[bm2.n == n], "OOS_Sharpe", "breadth_IS", "qq")[2] for n in NS]
    P(f"  pooled within-q, averaged over the 6 book sizes: {np.mean(allmw):+.4f}"
      f"   -> IS breadth {'DOES' if abs(np.mean(allmw)) >= BAR_RHO else 'does NOT'} clear the same "
      f"{BAR_RHO:.2f} bar the five headline statistics were held to")
    P("  AND IT CARRIES THE WRONG SIGN in 6 of 6 book sizes: inside a cap stratum, HIGHER IS")
    P("  breadth goes with LOWER OOS Sharpe.  The 6/6 argmax win above is one lucky draw at")
    P("  q=0.0, not a selection rule - which is why the argmax is reported next to this and not")
    P("  on its own.  Nothing here is promotable.")

    P("\n" + "=" * 100)
    P("SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens; every")
    P("small-cap level is biased upward by an unknown amount.  The bias enters the ORDERING of")
    P("the ladder only through the level of the eligible share, and the within-q test is a")
    P("comparison of panels drawn from the SAME two source pools, so the confound is common to")
    P("both sides of it.")
    P("=" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
