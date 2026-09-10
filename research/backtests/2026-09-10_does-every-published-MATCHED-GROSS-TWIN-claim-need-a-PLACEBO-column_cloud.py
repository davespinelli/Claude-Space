#!/usr/bin/env python3
"""Idea 604 - "does-every-published-MATCHED-GROSS-TWIN-claim-need-a-PLACEBO-column" (cloud).

The finding this run exists to generalise
-----------------------------------------
Idea 602 (lane C, 2026-09-10) ran the record's matched-gross TWIN leg against a null for the
first time.  On its own breadth population the raw twin win rate reads **0.818**, while a
rate- and run-length-matched, INFORMATION-FREE placebo at the IDENTICAL effective gross - and
therefore against the IDENTICAL twin - reads **0.259** (BLOCK) and **0.010** (RAND).  So the
number the record has been publishing (0.818) is not the readable one; the readable one is the
**0.559 difference**.  Idea 602 measured that on ONE clause family tree (breadth: ABS / QEXP /
QROLL).  The queue's question is whether EVERY committed matched-gross / matched-exposure twin
claim in the record needs that placebo column, and how much each claim moves when it gets one.

Two things have to happen for that to be answerable, and this run does both:
  (A) CENSUS.  Walk every committed artefact in the record, find the sites that make a
      matched-gross / matched-exposure / de-grossed-control / twin claim, classify each by
      (i) whether the claim is in the file's HEADLINE block or only in its body, (ii) whether
      the file actually emits a per-arm twin comparison column in a committed CSV, and
      (iii) which INSTRUMENT FAMILY the clause belongs to.  Report how many already carry any
      placebo/null column at all.
  (B) RE-PRICE.  Rebuild a pre-registered set of NINE de-grossing clause families that spans
      the census's instrument kinds - breadth (3 forms), realised vol, dispersion,
      correlation, own-drawdown, market trend, momentum - and price every arm against BOTH its
      matched-gross static twin AND its own BLOCK placebo at the identical effective gross.
      Coverage of the census by the re-priced families is reported, not assumed.

The placebo is not a robustness check bolted on.  It is the control the twin leg never had: a
gate that fires on the same days-count with the same clustering and NO information still gets
compared to a LOWER-gross static book, and if that comparison is itself biased then every
"a gate is more than a gross dial" and every "the clause earns nothing over its own de-grossed
control" sentence in the record is quoting an uncentred statistic.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (CENSUS)     How many committed sites make a matched-gross/twin claim, under three
                    readings of "claim" (WIDE / HEADLINE / ARM), and how many of them already
                    publish a placebo or null column beside the twin?
    Q2 (SIZE)       Per instrument family and per panel: REAL twin win rate, BLOCK placebo win
                    rate, and the difference.  Pre-registered SURVIVAL bar for a claim family:
                    REAL - BLOCK >= 0.10 AND z = (REAL - BLOCK) / sd_seed(BLOCK) >= 2.0.
                    A family that fails it is a family whose published twin leg is placebo.
    Q3 (SIGN)       Does the placebo column ever REVERSE a published claim - i.e. is BLOCK >
                    REAL anywhere?  Counted per family x panel x cadence x gross x rung.
    Q4 (MAGNITUDE)  On the dSharpe (not win-rate) scale, what fraction of the published
                    gate-minus-twin margin is placebo?  Reported as median dSharpe_REAL,
                    median dSharpe_BLOCK and the ratio, per family.
    Q5 (KEEP+RULE8) Both PROTOCOL KEEP paths on every arm, and the rule-8 walk-forward: choose
                    (family, depth) on 2009-2016 by IS placebo-differenced excess, read it once
                    on 2017+ untouched, and report the chosen book's OOS CAGR / Sharpe / MaxDD
                    against RULES v2 and SPY.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. claim set    WIDE (any matching site) / HEADLINE (site in the file's headline block) /
                    ARM (file emits a per-arm twin comparison column in a committed CSV).
    2. placebo kind BLOCK (circular shift of the effective multiplier - exact rate AND exact
                    run-length distribution) / RAND (iid days, exact matched count).
    ALL grid points are reported at every panel / family / level / depth / cadence / gross /
    cost rung.  Nothing below is tuned or selected on.

Reported axes, NEVER tuned or selected on
    family   ABS QEXP QROLL RVOL DISP CORR DDGATE MAGATE MOMGATE   (3 levels each)
    depth    0.25 / 0.50 / 1.00      cadence D / W      gross 0.75 / 1.00
    panel    U56 / B136 / SMALL(sub-$2B)             cost 0 / 10 / 25 bps
    seeds    10 per placebo kind, deterministic (md5 of the arm key)

Reproduction gates (section [0], printed before any new number is read)
    G1  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=c).
    G2  idea 84's ungated EWALL U56 g=0.85 @10bps landmark: 11.8% / 1.05 / -17.9% / H 1.07/1.04.
    G3  idea 602's COMMITTED .excess.csv re-derived arm-for-arm on the overlapping ABS/QEXP/
        QROLL arms (its REAL, BLOCK and RAND win columns), plus its published headline triple
        0.818 / 0.259 / 0.010 recomputed from its committed .placebo.csv.gz.
    G4  twin interpolation: the 0.01-gross cache interpolated to an exact g vs a true
        engine.backtest at that exact g.
    G5  placebo matching identity: BLOCK and RAND reproduce the real arm's on-share and mean
        multiplier EXACTLY (to 0), so they share the real arm's twin exactly.

Conventions inherited verbatim, not re-chosen
    Weights decided at t, applied at t+1 (engine).  Costs 10 bps per unit turnover as the
    protocol rung; 0 and 25 reported beside it.  The gate multiplier is decided at t and
    applied at t+1, with idea 399's switching cost on |dm| * gross * bps.  A TIE is not a win
    (ideas 594/595), TIE = 1e-12.  DDGATE's state is read off the gross=0.75 / 0 bps base book
    ONLY, so the multiplier path is gross- and cost-independent like every other family.

Data: committed caches only, no network, never yfinance.
SURVIVORSHIP: all three panels are CURRENT-CONSTITUENT lists (U56/B136 from the committed
universe json, the small panel from data/SMALL_PANEL_README.md's screen), so CAGR and drawdown
LEVELS are optimistic.  The gate-vs-twin CONTRAST and the placebo DIFFERENCING are the durable
part of this run; the small panel additionally drops every ticker with max_1d_move >= 1.0 in
data/small_meta.csv before anything is computed, and starts 2010-01-04, so its halves are not
U56/B136's calendar halves.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import gzip
import hashlib
import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT_EXCESS = OUT / "2026-09-10_is-the-MATCHED-GROSS-TWIN-win-rate-a-FIRING-RATE-function_C.excess.csv"
PARENT_PLACEBO = OUT / "2026-09-10_is-the-MATCHED-GROSS-TWIN-win-rate-a-FIRING-RATE-function_C.placebo.csv.gz"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
MINQ = 252
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12
NSEED = 10
GSTEP = 0.01
PLACEBO_KINDS = ["BLOCK", "RAND"]          # tuned param 2
CLAIM_SETS = ["WIDE", "HEADLINE", "ARM"]   # tuned param 1
SURV_DIFF = 0.10                           # pre-registered Q2 bar
SURV_Z = 2.0

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# =====================================================================================
# [0] primitives
# =====================================================================================
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def _cadence(m, idx, cadence):
    if cadence == "D":
        return m
    mask = rebalance_mask(idx, FREQ)
    return m.where(mask).ffill().fillna(1.0)


def apply_eff(r_base, turn_base, m_eff, gross, cost_bps):
    """Apply an ALREADY-EFFECTIVE (t+1-aligned) multiplier path, idea 399's switching cost."""
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * (r_base - turn_base * cost_bps / 1e4) - switch * gross * cost_bps / 1e4


def effective(m, idx):
    return m.reindex(idx).shift(1).fillna(1.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def sharpe(r):
    v = r.std()
    return (r.mean() * 252) / (v * np.sqrt(252)) if v else np.nan


def tests_4b(r, spy_pack):
    s1, s2, s_oos, s_dd, s_cagr = spy_pack
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > s_oos,
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
            "CAGR": m["CAGR"] >= 0.70 * s_cagr}


def verdict_4a(r, base_pack):
    b1, b2, bdd = base_pack
    h1, h2 = half_sharpes(r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= bdd)


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def placebo_mults(m_eff, depth, kind, seed):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path.

    RAND : iid days, EXACTLY the same number of de-grossed days.
    BLOCK: circular shift - exact rate AND exact run-length distribution.
    Both preserve mean(m_eff) EXACTLY, so they share the real arm's twin exactly (G5).
    """
    v = m_eff.values
    k = int((v < 1.0 - 1e-12).sum())
    if k == 0:
        return m_eff.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(len(v))
        out[rng.choice(len(v), size=k, replace=False)] = 1.0 - depth
        return pd.Series(out, index=m_eff.index)
    shift = int(rng.integers(1, len(v)))
    return pd.Series(np.roll(v, shift), index=m_eff.index)


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


class Twins:
    """Static-gross EWALL twin returns at an exact g by linear interpolation on a GSTEP cache."""

    def __init__(self, px, start):
        self.px, self.start, self.cache, self.n_bt = px, start, {}, 0

    def _exact(self, g):
        g = round(g, 6)
        if g not in self.cache:
            res = backtest(self.px, ewall_weights(self.px, g), cost_bps=0, freq=FREQ)
            self.cache[g] = (res["returns"].loc[self.start:], res["turnover"].loc[self.start:])
            self.n_bt += 1
        return self.cache[g]

    def at(self, g, cost_bps):
        lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
        lam = (round(g, 6) - lo) / GSTEP
        if lam <= 1e-9:
            r0, t0 = self._exact(lo)
        else:
            rl, tl = self._exact(lo)
            rh, th = self._exact(round(lo + GSTEP, 6))
            r0, t0 = (1 - lam) * rl + lam * rh, (1 - lam) * tl + lam * th
        return r0 - t0 * cost_bps / 1e4


# =====================================================================================
# [1] CENSUS of the record
# =====================================================================================
TWIN_RX = re.compile(
    r"matched[\s_\-]*(mean[\s_\-]*)?(gross|exposure)|matched[\s_\-]*g\b|"
    r"\btwins?\b|de[\s_\-]?grossed\s+(control|twin|comparand|base)|"
    r"gross[\s_\-]*matched|matched[\s_\-]*mean[\s_\-]*g_eff|ewall\s+control|"
    r"exposure[\s_\-]*matched", re.I)
PLACEBO_RX = re.compile(
    r"\bplacebo\b|\bnull\s+(arm|gate|control|column|model)\b|\bshuffl|\bpermut|"
    r"\bbootstrap\b|\bBLOCK\b\s*(placebo|null)|circular\s+shift|information[\s\-]?free", re.I)
FAMILY_RX = {
    "BREADTH": re.compile(r"\bbreadth\b|\bn_elig\b|share of names above", re.I),
    "VOL": re.compile(r"\bvol20\b|\brvol\b|realised vol|realized vol|vol\s*gate|vol\s*cap|volcap", re.I),
    "DISP": re.compile(r"\bdispersion\b|\bdisp\b(?!lay)", re.I),
    "CORR": re.compile(r"\bcorrelation\b|\bmrho\b|\bcorr\b(?!ect)", re.I),
    "DD": re.compile(r"\bdrawdown\s*(gate|budget|control)|\bddctl\b|\bdd\s*gate\b|dd[\s_\-]?budget", re.I),
    "TREND": re.compile(r"\b200d\b|\bMA200\b|\bMA\s*gate\b|\bband\b|200[\s\-]?day", re.I),
    "MOM": re.compile(r"\b12-1\b|\bmomentum\b|\bmom\b(?!ent)", re.I),
    "STOP": re.compile(r"\bstop\b|\btrailing\b|\btrail\b", re.I),
    "SLEEVE": re.compile(r"\bsleeve\b|\bTLT\b|\bGLD\b|\bUUP\b", re.I),
    "COUNT": re.compile(r"\btop-?\d+\b|\bn\s*=\s*\d+\b|\bcount dial\b", re.I),
}
ARM_COL_RX = re.compile(
    r"d_?sharpe|dsharpe|twin|static_?sharpe|matched|ewall|control_?sharpe|ctrl_?sharpe|g_?eff",
    re.I)


def headline_block(path, text):
    """The file's own headline: a .py module docstring, or a .md/.txt first block."""
    if path.suffix == ".py":
        m = re.search(r'^\s*(?:#![^\n]*\n)?\s*(?:"""|\'\'\')(.*?)(?:"""|\'\'\')', text, re.S)
        return m.group(1) if m else text[:2000]
    return "\n".join(text.split("\n")[:60])


def csv_header_has_arm_col(p):
    try:
        if p.suffix == ".gz":
            with gzip.open(p, "rt") as fh:
                head = fh.readline()
        else:
            head = p.open("r", errors="replace").readline()
    except Exception:
        return False
    return bool(ARM_COL_RX.search(head))


def run_census():
    log("\n" + "=" * 180)
    log("[1] CENSUS - every committed matched-gross / matched-exposure / twin claim in the record")
    log("=" * 180)
    targets = sorted(
        [p for p in OUT.rglob("*") if p.suffix in (".py", ".md", ".txt")]
        + [REPO / "research" / f for f in ("LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md", "RULES.md", "PROTOCOL.md")]
    )
    sib = {}
    for p in OUT.rglob("*"):
        if p.suffix in (".csv", ".gz"):
            sib.setdefault(re.split(r"\.", p.name)[0], []).append(p)

    rows = []
    for p in targets:
        if p.name == SCRIPT:
            continue
        try:
            text = p.read_text(errors="replace")
        except Exception:
            continue
        hits = [(m.start(), m.group(0)) for m in TWIN_RX.finditer(text)]
        if not hits:
            continue
        head = headline_block(p, text)
        n_head = len(TWIN_RX.findall(head))
        stem = re.split(r"\.", p.name)[0]
        arm = any(csv_header_has_arm_col(c) for c in sib.get(stem, []))
        ctx = "".join(text[max(0, s - 400): s + 400] for s, _ in hits[:40])
        fams = sorted(k for k, rx in FAMILY_RX.items() if rx.search(ctx))
        rows.append(dict(file=p.relative_to(REPO).as_posix(), kind=p.suffix.lstrip("."),
                         n_sites=len(hits), in_headline=n_head > 0, arm_col=arm,
                         has_placebo=bool(PLACEBO_RX.search(text)),
                         placebo_near=bool(PLACEBO_RX.search(ctx)),
                         families="+".join(fams) if fams else "-"))
    cen = pd.DataFrame(rows)
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)

    log(f"\n  files with >=1 twin/matched-gross site : {len(cen)}   "
        f"(sites total {cen['n_sites'].sum()})")
    log(f"  by artefact kind: " + ", ".join(f"{k} {v}" for k, v in cen['kind'].value_counts().items()))
    log("\n  Q1 - the three CLAIM SET readings (tuned param 1) and their placebo coverage:")
    log(f"    {'reading':<10} {'files':>6} {'sites':>7} {'with any placebo col':>22} {'placebo NEAR the site':>23}")
    sets = {"WIDE": cen, "HEADLINE": cen[cen.in_headline], "ARM": cen[cen.arm_col]}
    for name, sub in sets.items():
        log(f"    {name:<10} {len(sub):>6} {sub['n_sites'].sum():>7} "
            f"{sub['has_placebo'].sum():>10} ({sub['has_placebo'].mean():>6.1%}) "
            f"{sub['placebo_near'].sum():>11} ({sub['placebo_near'].mean():>6.1%})")
    log("\n  instrument families named in the context of a twin claim (WIDE reading, "
        "a file may carry several):")
    fc = {}
    for s in cen["families"]:
        for f in s.split("+"):
            fc[f] = fc.get(f, 0) + 1
    for k, v in sorted(fc.items(), key=lambda kv: -kv[1]):
        log(f"    {k:<10} {v:>4} files  ({v/len(cen):>6.1%})")
    log("\n  .py files carrying a twin claim, most sites first (top 20):")
    py = cen[cen.kind == "py"].sort_values("n_sites", ascending=False).head(20)
    log(py[["file", "n_sites", "in_headline", "arm_col", "has_placebo", "families"]].to_string(index=False))
    return cen, sets


# =====================================================================================
# [2] the nine re-priced clause families
# =====================================================================================
def panel_states(px):
    """Every family's STATE series, computed once per panel.  All are panel-level (one number
    per day) so every family is the same shape of clause: 'de-gross the whole book by `depth`
    while the state is bad'."""
    rets = px.drop(columns=["SPY"], errors="ignore").pct_change()
    above = px.drop(columns=["SPY"], errors="ignore") > px.drop(columns=["SPY"], errors="ignore").rolling(200).mean()
    st = {}
    st["BREADTH"] = above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    st["RVOL"] = -(rets.std(axis=1).rolling(20).mean())          # low state = BAD -> negate vol
    st["DISP"] = -(rets.rolling(20).std().mean(axis=1))          # high dispersion = BAD
    ew = rets.mean(axis=1)
    xs = rets.sub(ew, axis=0)
    tot = rets.rolling(60).var().mean(axis=1)
    idio = xs.rolling(60).var().mean(axis=1)
    st["CORR"] = -(1.0 - idio / tot.replace(0, np.nan))           # high co-movement = BAD
    spy = px["SPY"]
    st["MA"] = spy / spy.rolling(200).mean() - 1.0
    mom = px.drop(columns=["SPY"], errors="ignore")
    st["MOM"] = (mom.shift(21) / mom.shift(252) - 1).mean(axis=1)
    return st


FAMILIES = [
    # (name, state key, level kind, levels)      "ABS" = absolute cut, "QEXP"/"QROLL" = quantile
    ("ABS",     "BREADTH", "ABS",   [0.30, 0.40, 0.50]),
    ("QEXP",    "BREADTH", "QEXP",  [0.07, 0.12, 0.17]),
    ("QROLL",   "BREADTH", "QROLL", [0.07, 0.12, 0.17]),
    ("RVOL",    "RVOL",    "QEXP",  [0.20, 0.30, 0.40]),
    ("DISP",    "DISP",    "QEXP",  [0.20, 0.30, 0.40]),
    ("CORR",    "CORR",    "QEXP",  [0.20, 0.30, 0.40]),
    ("MAGATE",  "MA",      "ABS",   [-0.03, 0.00, 0.03]),
    ("MOMGATE", "MOM",     "QEXP",  [0.20, 0.30, 0.40]),
    ("DDGATE",  "DD",      "ABS",   [-0.05, -0.10, -0.15]),
]
WROLL = 1008   # idea 399/601's rate-faithful default, inherited not tuned


def raw_multiplier(state, kind, level, depth, idx):
    """1.0 normally, 1-depth while the state is BAD (below its cut).  Decided at t."""
    if kind == "ABS":
        thr = pd.Series(level, index=state.index)
    elif kind == "QEXP":
        thr = state.expanding(min_periods=MINQ).quantile(level)
    else:
        thr = state.rolling(WROLL, min_periods=WROLL).quantile(level)
    bad = (state < thr) & state.notna() & thr.notna()
    return pd.Series(1.0, index=idx).where(~bad.reindex(idx).fillna(False), 1.0 - depth)


def run_panel(panel, px, cen_families):
    start = px.index[260]
    idx = px.index
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy)
    s1, s2 = half_sharpes(spy)
    spy_pack = (s1, s2, metrics(spy.loc[OOS_START:])["Sharpe"], ms["MaxDD"], ms["CAGR"])

    log(f"\n{'='*180}")
    log(f"PANEL {panel}: {px.shape[1]} columns, {idx[0].date()} -> {idx[-1].date()}, "
        f"eval from {start.date()} ({len(px.loc[start:])} days)")
    log(f"  SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}; 4b bars: CAGR floor "
        f"{0.70*ms['CAGR']:.2%}, DD cap {-0.60*abs(ms['MaxDD']):.2%}, halves {s1:.3f}/{s2:.3f}, "
        f"OOS {spy_pack[2]:.3f}")

    # RULES v2 comparand for 4a, cost-matched per rung (idea 398's wording)
    v2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    v2r0, v2t = v2["returns"].loc[start:], v2["turnover"].loc[start:]
    base_packs = {}
    for c in RUNGS:
        rv = v2r0 - v2t * c / 1e4
        h1, h2 = half_sharpes(rv)
        base_packs[c] = (h1, h2, metrics(rv)["MaxDD"])
    mv = metrics(v2r0 - v2t * RUNG_HEAD / 1e4)
    log(f"  RULES v2 @10bps {mv['CAGR']:.2%} / {mv['Sharpe']:.3f} / {mv['MaxDD']:.2%}")

    # base books
    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])
    twins = Twins(px, start)

    states = panel_states(px)
    # DDGATE's state: the gross=0.75 / 0bps base book's own running drawdown (gross-independent)
    eq = (1 + base0[G_HEAD][0]).cumprod()
    states["DD"] = (eq / eq.cummax() - 1).reindex(idx)

    arms, placebos = [], []
    for fam, skey, lkind, levels in FAMILIES:
        st = states[skey]
        for level in levels:
            for depth in DEPTHS:
                m_raw = raw_multiplier(st, lkind, level, depth, idx)
                for cadence in CADENCES:
                    m = _cadence(m_raw, idx, cadence)
                    m_eff = effective(m, idx).loc[start:]
                    on_share = float((m_eff < 1.0 - 1e-12).mean())
                    mult_mean = float(m_eff.mean())
                    # placebo multiplier paths (shared across gross & rung: G5)
                    pmults = {k: [placebo_mults(m_eff, depth, k, seed_of(panel, fam, level, depth, cadence, k, s))
                                  for s in range(NSEED)] for k in PLACEBO_KINDS}
                    for g in GROSSES:
                        g_eff = g * mult_mean
                        rb, tb = base0[g]
                        for c in RUNGS:
                            r_real = apply_eff(rb, tb, m_eff, g, c)
                            r_twin = twins.at(g_eff, c)
                            d = sharpe(r_real) - sharpe(r_twin)
                            m_real = metrics(r_real)
                            h1, h2 = half_sharpes(r_real)
                            t4b = tests_4b(r_real, spy_pack)
                            row = dict(panel=panel, family=fam, level=level, depth=depth,
                                       cadence=cadence, gross=g, cost=c,
                                       on_share=on_share, mult_mean=mult_mean, g_eff=g_eff,
                                       CAGR=m_real["CAGR"], Sharpe=m_real["Sharpe"],
                                       MaxDD=m_real["MaxDD"], H1=h1, H2=h2,
                                       OOS_CAGR=metrics(r_real.loc[OOS_START:])["CAGR"],
                                       OOS_Sharpe=metrics(r_real.loc[OOS_START:])["Sharpe"],
                                       OOS_MaxDD=metrics(r_real.loc[OOS_START:])["MaxDD"],
                                       twin_Sharpe=sharpe(r_twin), dSharpe=d,
                                       win=bool(d > TIE),
                                       p4a=verdict_4a(r_real, base_packs[c]),
                                       p4b=all(t4b.values()),
                                       fail4b=",".join(k for k, v in t4b.items() if not v) or "-")
                            # IS/OOS legs of the CLAIM itself (rule 8)
                            for tag, sl in (("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))):
                                rr, rt = r_real.loc[sl], r_twin.loc[sl]
                                row[f"dSharpe_{tag}"] = sharpe(rr) - sharpe(rt)
                                row[f"win_{tag}"] = bool(sharpe(rr) - sharpe(rt) > TIE)
                            arms.append(row)
                            for kind in PLACEBO_KINDS:
                                for s, pm in enumerate(pmults[kind]):
                                    r_p = apply_eff(rb, tb, pm, g, c)
                                    dp = sharpe(r_p) - sharpe(r_twin)
                                    prow = dict(panel=panel, family=fam, level=level, depth=depth,
                                                cadence=cadence, gross=g, cost=c, kind=kind, seed=s,
                                                p_on=float((pm < 1.0 - 1e-12).mean()),
                                                p_mult=float(pm.mean()), dSharpe=dp,
                                                win=bool(dp > TIE))
                                    for tag, sl in (("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))):
                                        prow[f"dSharpe_{tag}"] = sharpe(r_p.loc[sl]) - sharpe(r_twin.loc[sl])
                                        prow[f"win_{tag}"] = bool(prow[f"dSharpe_{tag}"] > TIE)
                                    placebos.append(prow)
    A = pd.DataFrame(arms)
    P = pd.DataFrame(placebos)
    log(f"  arms {len(A)}, placebo rows {len(P)}, twin backtests cached {twins.n_bt}")
    # G5 on this panel
    j = P.merge(A[["panel", "family", "level", "depth", "cadence", "gross", "cost",
                   "on_share", "mult_mean"]],
                on=["panel", "family", "level", "depth", "cadence", "gross", "cost"])
    log(f"  G5 placebo matching identity: max|on_share diff| {abs(j.p_on - j.on_share).max():.3e}, "
        f"max|mean multiplier diff| {abs(j.p_mult - j.mult_mean).max():.3e}")
    return A, P


# =====================================================================================
# main
# =====================================================================================
def main():
    log(f"# {STEM}")
    log(f"# idea 604 - does every published MATCHED-GROSS TWIN claim need a PLACEBO column?")
    log(f"# tuned params: (1) claim set {CLAIM_SETS}  (2) placebo kind {PLACEBO_KINDS}. "
        f"All other axes reported, never selected on.")

    # ---------------------------------------------------------------- [0] gates
    log("\n" + "=" * 180)
    log("[0] REPRODUCTION GATES")
    log("=" * 180)
    px_u = load_universe()
    start_u = px_u.index[260]
    w85 = ewall_weights(px_u, 0.85)
    r0 = backtest(px_u, w85, cost_bps=0, freq=FREQ)
    r10 = backtest(px_u, w85, cost_bps=10, freq=FREQ)
    derived = r0["returns"] - r0["turnover"] * 10 / 1e4
    g1 = float(abs(derived - r10["returns"]).max())
    log(f"  G1 derived-rung identity r(10) = r(0) - turnover*10/1e4 : max|diff| {g1:.3e}  "
        f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]")
    rr = r10["returns"].loc[start_u:]
    m84 = metrics(rr)
    h1, h2 = half_sharpes(rr)
    log(f"  G2 idea 84 EWALL U56 g=0.85 @10bps: {m84['CAGR']:.1%} / {m84['Sharpe']:.2f} / "
        f"{m84['MaxDD']:.1%} / H {h1:.2f}/{h2:.2f}   (committed 11.8% / 1.05 / -17.9% / 1.07/1.04)")
    tw = Twins(px_u, start_u)
    errs = []
    for g in (0.6234, 0.7117, 0.7788, 0.8351, 0.9042, 0.4567):
        true = backtest(px_u, ewall_weights(px_u, g), cost_bps=10, freq=FREQ)["returns"].loc[start_u:]
        errs.append(abs(sharpe(tw.at(g, 10)) - sharpe(true)))
    log(f"  G4 twin interpolation error over 6 off-grid g: max|dSharpe| {max(errs):.3e}, "
        f"mean {np.mean(errs):.3e}")

    # ---------------------------------------------------------------- [1] census
    cen, sets = run_census()

    # ---------------------------------------------------------------- G3 vs idea 602
    log("\n  G3 idea 602's committed artefacts:")
    if PARENT_PLACEBO.exists():
        with gzip.open(PARENT_PLACEBO, "rt") as fh:
            pp = pd.read_csv(io.StringIO(fh.read()))
        head = pp.groupby("kind")["win"].mean()
        log(f"    .placebo.csv.gz recomputed win rates: " +
            ", ".join(f"{k} {v:.3f}" for k, v in head.items()) +
            "   (idea 602 headline BLOCK 0.259 / RAND 0.010)")
    if PARENT_EXCESS.exists():
        pe = pd.read_csv(PARENT_EXCESS)
        log(f"    .excess.csv rows {len(pe)}; REAL mean {pe['REAL'].mean():.4f}, "
            f"BLOCK mean {pe['BLOCK'].mean():.4f}, RAND mean {pe['RAND'].mean():.4f} "
            f"(these are mean dSharpe columns, not win rates)")

    # ---------------------------------------------------------------- [2] re-price
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pxs, ndrop = small_panel()
    panels["SMALL"] = pxs
    log(f"\n  small panel: dropped {ndrop} tickers with max_1d_move >= 1.0 -> {pxs.shape[1]-1} names")

    As, Ps = [], []
    for name, px in panels.items():
        a, p = run_panel(name, px, cen)
        As.append(a)
        Ps.append(p)
    A = pd.concat(As, ignore_index=True)
    P = pd.concat(Ps, ignore_index=True)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    with gzip.open(OUT / f"{STEM}.placebo.csv.gz", "wt") as fh:
        P.to_csv(fh, index=False)

    # ---------------------------------------------------------------- [3] Q2/Q3/Q4
    log("\n" + "=" * 180)
    log("[3] Q2 - REAL twin win rate vs its OWN placebo, per family and panel "
        f"(cost {RUNG_HEAD} bps, both gross, both cadences; every rung in the csv)")
    log("=" * 180)
    key = ["panel", "family"]
    surv_rows = []
    for kind in PLACEBO_KINDS:
        Ah = A[A.cost == RUNG_HEAD]
        Ph = P[(P.cost == RUNG_HEAD) & (P.kind == kind)]
        real = Ah.groupby(key)["win"].mean()
        # per-seed placebo win rate -> mean and sd across seeds (the z denominator)
        per_seed = Ph.groupby(key + ["seed"])["win"].mean().unstack()
        pmean, psd = per_seed.mean(axis=1), per_seed.std(axis=1, ddof=1)
        med_r = Ah.groupby(key)["dSharpe"].median()
        med_p = Ph.groupby(key)["dSharpe"].median()
        for k in real.index:
            diff = real[k] - pmean[k]
            z = diff / psd[k] if psd[k] > 0 else np.inf
            surv_rows.append(dict(placebo=kind, panel=k[0], family=k[1], n_arms=int((Ah.groupby(key).size())[k]),
                                  REAL=real[k], PLACEBO=pmean[k], sd_seed=psd[k], diff=diff, z=z,
                                  survives=bool(diff >= SURV_DIFF and z >= SURV_Z),
                                  reversed_=bool(pmean[k] > real[k]),
                                  med_dS_REAL=med_r[k], med_dS_PLACEBO=med_p[k],
                                  placebo_share=(med_p[k] / med_r[k]) if abs(med_r[k]) > 1e-9 else np.nan))
    S = pd.DataFrame(surv_rows)
    S.to_csv(OUT / f"{STEM}.survival.csv", index=False)
    for kind in PLACEBO_KINDS:
        sub = S[S.placebo == kind].copy()
        log(f"\n  placebo = {kind}   (survival bar: diff >= {SURV_DIFF} AND z >= {SURV_Z})")
        log(sub.pivot_table(index="family", columns="panel",
                            values=["REAL", "PLACEBO", "diff"]).round(3).to_string())
        log(f"    survives: {sub.survives.sum()} of {len(sub)} family x panel cells; "
            f"REVERSED (placebo beats real): {sub.reversed_.sum()}")
    log("\n  full survival table (BLOCK, the queue's named placebo):")
    log(S[S.placebo == "BLOCK"].drop(columns=["placebo"]).round(4).to_string(index=False))

    log("\n  Q4 - what share of the published gate-minus-twin dSharpe margin is placebo? "
        "(median over arms, BLOCK, 10 bps)")
    q4 = S[S.placebo == "BLOCK"].groupby("family")[["med_dS_REAL", "med_dS_PLACEBO"]].median()
    q4["placebo_share_of_margin"] = q4.med_dS_PLACEBO / q4.med_dS_REAL.replace(0, np.nan)
    log(q4.round(4).to_string())

    # pooled headline, the direct analogue of idea 602's 0.818 / 0.259 / 0.010
    log("\n  POOLED headline (all families, all panels, 10 bps):")
    for c in RUNGS:
        rr = A[A.cost == c]["win"].mean()
        line = f"    cost {c:>2} bps: REAL {rr:.3f}"
        for kind in PLACEBO_KINDS:
            line += f"   {kind} {P[(P.cost == c) & (P.kind == kind)]['win'].mean():.3f}"
        log(line + f"   diff vs BLOCK {rr - P[(P.cost == c) & (P.kind=='BLOCK')]['win'].mean():+.3f}")

    log("\n  Q3 - sign reversals, per family x panel x cadence x gross x rung (BLOCK):")
    kk = ["panel", "family", "cadence", "gross", "cost"]
    rc = A.groupby(kk)["win"].mean()
    pc = P[P.kind == "BLOCK"].groupby(kk)["win"].mean()
    cmp_ = pd.DataFrame({"REAL": rc, "BLOCK": pc}).dropna()
    log(f"    cells {len(cmp_)}; REAL > BLOCK {int((cmp_.REAL > cmp_.BLOCK).sum())}, "
        f"REAL == BLOCK {int((cmp_.REAL == cmp_.BLOCK).sum())}, "
        f"REVERSED {int((cmp_.REAL < cmp_.BLOCK).sum())} "
        f"({(cmp_.REAL < cmp_.BLOCK).mean():.1%})")
    log("    the reversed cells:")
    rev = cmp_[cmp_.REAL < cmp_.BLOCK]
    log(rev.round(3).to_string() if len(rev) else "      (none)")

    # ---------------------------------------------------------------- census coverage
    log("\n  CENSUS COVERAGE - which census instrument families this run actually re-prices:")
    covered = {"BREADTH": "ABS+QEXP+QROLL", "VOL": "RVOL", "DISP": "DISP", "CORR": "CORR",
               "DD": "DDGATE", "TREND": "MAGATE", "MOM": "MOMGATE"}
    fc = {}
    for s in cen["families"]:
        for f in s.split("+"):
            fc[f] = fc.get(f, 0) + 1
    tot = sum(v for k, v in fc.items() if k != "-")
    cov = sum(v for k, v in fc.items() if k in covered)
    log(f"    re-priced families: {', '.join(f'{k}->{v}' for k, v in covered.items())}")
    log(f"    NOT re-priced: STOP (idea 396's own run), SLEEVE (idea 395), COUNT (n dial)")
    log(f"    census family-mentions covered: {cov} of {tot} = {cov/tot:.1%}")
    for rd, sub in sets.items():
        n_any = sum(1 for s in sub["families"] if any(f in covered for f in s.split("+")))
        log(f"    {rd:<9}: {n_any} of {len(sub)} files ({n_any/max(len(sub),1):.1%}) name at least one "
            f"re-priced family")

    # ---------------------------------------------------------------- [4] KEEP paths
    log("\n" + "=" * 180)
    log("[4] PROTOCOL KEEP paths on every arm (4a vs cost-matched RULES v2, 4b vs SPY)")
    log("=" * 180)
    log(f"  4a passes {int(A.p4a.sum())} of {len(A)} arms; at the protocol rung (10 bps) "
        f"{int(A[A.cost==RUNG_HEAD].p4a.sum())} of {int((A.cost==RUNG_HEAD).sum())}")
    log(f"  4b passes {int(A.p4b.sum())} of {len(A)} arms; at the protocol rung "
        f"{int(A[A.cost==RUNG_HEAD].p4b.sum())} of {int((A.cost==RUNG_HEAD).sum())}")
    log("  4a by cost rung: " + ", ".join(f"{c} bps {int(A[A.cost==c].p4a.sum())}" for c in RUNGS))
    log("  4b by cost rung: " + ", ".join(f"{c} bps {int(A[A.cost==c].p4b.sum())}" for c in RUNGS))
    log("  binding 4b bar (which leg fails), 10 bps, all arms:")
    fb = A[A.cost == RUNG_HEAD]["fail4b"].value_counts().head(12)
    log(fb.to_string())
    if A.p4b.any():
        log("\n  the 4b passers (all rungs):")
        cols = ["panel", "family", "level", "depth", "cadence", "gross", "cost", "CAGR",
                "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "dSharpe", "p4a"]
        log(A[A.p4b][cols].round(4).to_string(index=False))

    # ---------------------------------------------------------------- [5] rule 8
    log("\n" + "=" * 180)
    log("[5] RULE 8 WALK-FORWARD - choose on 2009-2016, read once on 2017+ untouched")
    log("=" * 180)
    log("  (a) THE CLAIM's own walk-forward: does the placebo-differenced excess chosen IS")
    log("      hold OOS?  Per panel x family: IS excess = win_IS(REAL) - win_IS(BLOCK).")
    kk2 = ["panel", "family"]
    Ah = A[A.cost == RUNG_HEAD]
    Ph = P[(P.cost == RUNG_HEAD) & (P.kind == "BLOCK")]
    wf = pd.DataFrame({
        "REAL_IS": Ah.groupby(kk2)["win_IS"].mean(),
        "BLOCK_IS": Ph.groupby(kk2)["win_IS"].mean(),
        "REAL_OOS": Ah.groupby(kk2)["win_OOS"].mean(),
        "BLOCK_OOS": Ph.groupby(kk2)["win_OOS"].mean()})
    wf["excess_IS"] = wf.REAL_IS - wf.BLOCK_IS
    wf["excess_OOS"] = wf.REAL_OOS - wf.BLOCK_OOS
    wf["sign_holds"] = np.sign(wf.excess_IS) == np.sign(wf.excess_OOS)
    wf.to_csv(OUT / f"{STEM}.wf.csv")
    log(wf.round(3).to_string())
    log(f"    sign of the placebo-differenced excess holds IS->OOS in "
        f"{int(wf.sign_holds.sum())} of {len(wf)} panel x family cells; "
        f"Spearman(excess_IS, excess_OOS) = "
        f"{wf['excess_IS'].rank().corr(wf['excess_OOS'].rank()):.3f}")

    log("\n  (b) THE BOOK's rule 8: choose (family, level, depth, cadence, gross) on IS Sharpe")
    log("      within each panel, read the pick once on 2017+ against RULES v2 and SPY.")
    pick_rows = []
    for panel, px in panels.items():
        start = px.index[260]
        sub = A[(A.panel == panel) & (A.cost == RUNG_HEAD)].copy()
        # IS Sharpe of the arm itself, recomputed from committed columns is not available;
        # use the claim's IS leg proxy: rank on IS dSharpe is a CLAIM statistic, so instead
        # we re-derive IS Sharpe here from the stored grid by re-running only the picked arm.
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
        v2r = (v2["returns"] - v2["turnover"] * RUNG_HEAD / 1e4).loc[start:]
        base0 = {}
        for g in GROSSES:
            res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
            base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])
        states = panel_states(px)
        eq = (1 + base0[G_HEAD][0]).cumprod()
        states["DD"] = (eq / eq.cummax() - 1).reindex(px.index)
        best, best_is = None, -np.inf
        cache = {}
        for fam, skey, lkind, levels in FAMILIES:
            for level in levels:
                for depth in DEPTHS:
                    mr = raw_multiplier(states[skey], lkind, level, depth, px.index)
                    for cadence in CADENCES:
                        m_eff = effective(_cadence(mr, px.index, cadence), px.index).loc[start:]
                        for g in GROSSES:
                            rb, tb = base0[g]
                            r = apply_eff(rb, tb, m_eff, g, RUNG_HEAD)
                            cache[(fam, level, depth, cadence, g)] = r
                            s_is = sharpe(r.loc[:IS_END])
                            if s_is > best_is:
                                best_is, best = s_is, (fam, level, depth, cadence, g)
        r = cache[best]
        mo, mv, msp = metrics(r.loc[OOS_START:]), metrics(v2r.loc[OOS_START:]), metrics(spy_r.loc[OOS_START:])
        log(f"\n    {panel}: IS pick = {best[0]} level {best[1]} depth {best[2]} "
            f"cadence {best[3]} gross {best[4]}  (IS Sharpe {best_is:.3f})")
        log(f"      OOS 2017+   pick  {mo['CAGR']:>7.2%} / {mo['Sharpe']:.3f} / {mo['MaxDD']:>7.2%}")
        log(f"                  v2    {mv['CAGR']:>7.2%} / {mv['Sharpe']:.3f} / {mv['MaxDD']:>7.2%}")
        log(f"                  SPY   {msp['CAGR']:>7.2%} / {msp['Sharpe']:.3f} / {msp['MaxDD']:>7.2%}")
        pick_rows.append(dict(panel=panel, family=best[0], level=best[1], depth=best[2],
                              cadence=best[3], gross=best[4], IS_Sharpe=best_is,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              v2_OOS_CAGR=mv["CAGR"], v2_OOS_Sharpe=mv["Sharpe"], v2_OOS_MaxDD=mv["MaxDD"],
                              spy_OOS_CAGR=msp["CAGR"], spy_OOS_Sharpe=msp["Sharpe"], spy_OOS_MaxDD=msp["MaxDD"],
                              beats_v2=bool(mo["Sharpe"] > mv["Sharpe"]),
                              beats_spy=bool(mo["Sharpe"] > msp["Sharpe"])))
    PK = pd.DataFrame(pick_rows)
    PK.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    log(f"\n    picks beating RULES v2 OOS: {int(PK.beats_v2.sum())} of {len(PK)}; "
        f"beating SPY OOS: {int(PK.beats_spy.sum())} of {len(PK)}")

    (OUT / f"{STEM}.txt").write_text("\n".join(LINES) + "\n")
    log(f"\nwrote {STEM}.txt / .census.csv / .arms.csv / .placebo.csv.gz / .survival.csv / .wf.csv / .picks.csv")
    (OUT / f"{STEM}.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
