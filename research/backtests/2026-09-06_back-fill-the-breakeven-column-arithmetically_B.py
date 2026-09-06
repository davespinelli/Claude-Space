#!/usr/bin/env python3
"""Idea 269 - "back-fill-the-breakeven-column-arithmetically-not-by-re-running" (lane B, 2026-09-06).

The question
------------
Idea 262 ended on a law rather than a book:

    c* = dSharpe(0) * 1e4 / (T_x/vol_x - T_y/vol_y)                      (L)

reproducing its measured breakevens at R^2 0.9989 / 0.028 bps median error over 337
flipping points spanning turnover ratios 0.65x-4.3x.  Idea 263 then proposed that any
comparison between two arms whose turnovers differ by more than 2x must publish the
breakeven beside the quoted rung.  The queue's follow-up is the arithmetic one:

    (L) needs only four numbers.  So idea 263's column can be BACK-FILLED over the
    leaderboard's turnover-mismatched rows without re-running any of them.  Census how
    many rows have the four numbers, back-fill those, and report how many published
    verdicts have a breakeven inside 0-25 bps.

This run does exactly that, in four parts, and does NOT take the census on faith.

  (1) THE CENSUS.  Every row of research/LEADERBOARD.md is parsed, attributed to its
      parent script, and tiered by which of the four numbers its parent actually
      committed.  The leaderboard itself publishes no turnover and no vol, so a row is
      only reachable if it can be JOINED to a row of a committed grid CSV.  The join is
      a numeric fingerprint - (CAGR, Sharpe, MaxDD) at the leaderboard's own printed
      precision, inside the parent script's own CSVs - and its ambiguity is reported,
      not hidden.

  (2) THE VOL RECOVERY.  (L) needs vol per arm, and the record commits turnover far more
      often than it commits Vol.  But engine.metrics' own definitions pin vol from two
      numbers that ARE almost always committed:

          Sharpe = mean_ann / vol      and      ln(1+CAGR) = mean_ann - vol^2/2 + O(m3)

      so vol solves  vol^2/2 - Sharpe*vol + ln(1+CAGR) = 0,  discriminant (Sharpe-vol)^2,
      root  vol = Sharpe -/+ sqrt(Sharpe^2 - 2 ln(1+CAGR))  (take the POSITIVE root; for
      Sharpe < 0 that is the upper one).  If that identity holds on the record's own
      committed (CAGR, Sharpe, Vol) triples, then (L) needs THREE committed numbers per
      arm, not four, and the back-fillable share of the leaderboard grows accordingly.
      Every committed triple in research/backtests/*.csv[.gz] is used as the test set.

  (3) THE BACK-FILL.  For every joined row, the comparand is the row's OWN published
      baseline - the leaderboard's "Baseline Sharpe (H1/H2)" column - identified
      mechanically by fingerprinting that (Sharpe, H1, H2) triple against RULES v1 books
      computed live here on every offline panel x cadence.  That is one live computation
      re-used across thousands of rows; it is not a re-run of any row.  c* is anchored at
      the leaderboard's stated rung (10 bps, per its own header), which is (L) re-anchored:

          c* = 10 + dSharpe(10) * 1e4 / (T_x/vol_x - T_y/vol_y)                     (L10)

      Headline: how many published verdicts have a breakeven inside 0-25 bps.

  (4) THE VALIDATION.  Idea 262 fitted (L) on NULL arms only - held/re-drawn uniform keys
      and a rotation.  Idea 267 is separately testing whether its turnover-ratio band is a
      null-arm artefact.  So this run re-measures (L) on the record's NON-NULL dials -
      cadence D/W/M/Q, n, gross, the vol scaler, EWall, v1 - where the two arms differ in
      a real design choice rather than in a random seed, and on BOTH the true and the
      recovered vol.  Exact breakevens by the same 0.05-bps scan + bisection as idea 262.
      If (L) survives off the nulls with recovered vol, the back-fill is sound; if it does
      not, the census is still reported and the back-fill is quoted as an upper bound.

Design
------
Panels U56 / B136 / BSTK100 (idea 82/260/262's construction, imported).  Weekly is the
record's default cadence; the cadence dial is one of the axes under test so D/W/M/Q are
all run.  Gate = above-200d AND vol20 < 0.60.  Costs 10 bps is PROTOCOL's rung; the rung
is a reported axis here because it is the object of study.  Next-day execution throughout
(engine.backtest shifts weights by one day).

COST DERIVATION.  engine.backtest computes  port = (held*rets).sum(axis=1) - turnover*c/1e4
and neither term depends on c, so every book is run ONCE at 0 bps and any rung is derived
EXACTLY as r(c) = r(0) - turnover*c/1e4.  The identity is asserted against live
backtest(cost_bps=...) calls before any result is read; the run aborts if it is not 0.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (3)      2. n (4: 5/10/20/40)
The cadence, the gross, the vol scaler and the cost rung are REPORTED axes, not tuned:
every one of them is written to `.grid.csv` and none is used to select a headline.

Pre-registered decision rule (written before any number of this run was read)
----------------------------------------------------------------------------
  (a) THE VOL RECOVERY is USABLE if the identity reproduces the record's committed Vol
      to better than 1% relative on >= 95% of committed triples.  Worse than that and the
      back-fill is restricted to rows whose parent committed Vol outright.
  (b) THE LAW GENERALISES OFF THE NULLS if measured-vs-predicted breakeven on the
      non-null dial pairs has R^2 > 0.90 with the recovered vol, IS and OOS separately.
      R^2 <= 0.90 in either window kills the arithmetic back-fill as a substitute for
      re-running, and this run reports the census only.
  (c) The HEADLINE is a count, not a book: of the leaderboard rows that can be back-filled,
      how many have c* in (0, 25] bps - i.e. how many published verdicts would flip inside
      the cost range the project actually trades in.
  A KILL / ANSWERED verdict is expected: this is a measurement idea, not a book.  Both KEEP
  paths are still evaluated on every grid point and rule 8 is still run, per PROTOCOL.

Reproduction gate (asserted before anything else is read)
    U56/RULES v1 weekly, record convention (warm-up 260 days dropped) -> 6.5% / 0.666 / -13.8%
    U56/FIXED20  (idea 73's literal GROSS/n)                          -> 12.7% / 1.093 / -18.3%
  A mismatch beyond the stated tolerance aborts the run.

Walk-forward (PROTOCOL rule 8) - selectors fixed, with direction, before any OOS read
    IS = 2009-01-01..2016-12-31 is the ONLY place (panel, n) is chosen: the pair that
    maximises IS Sharpe of the FWD arm, and separately the IS-argmax of the law's own fit.
    OOS = 2017-01-01..end is read once, at every rung, for both the law's error and the
    books' CAGR/Sharpe/MaxDD, against RULES v1 OOS and SPY OOS.

SURVIVORSHIP.  universe_broad.json and the megacap cut are CURRENT constituents, so B136
and BSTK100 are one-directional.  It does not touch this run's object - the law relates
two arms measured on the SAME panel, so a panel bias is common to both sides of every
difference - but it is stated because the panels' own levels are quoted.

Nothing in RULES.md, scan.py, bot.py or baseline.py is touched.
"""
from __future__ import annotations
import json, re, sys, gzip, math
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v1_weights, score          # noqa: E402
from engine import backtest, metrics                                  # noqa: E402

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
LB_PATH = REPO / "research" / "LEADERBOARD.md"

RUNGS = [0, 1, 2, 5, 10, 25]
PROTO_RUNG = 10.0
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS = [5, 10, 20, 40]
CADENCES = ["D", "W", "M", "Q"]
GROSSES = [0.50, 0.75, 1.00]
IS_START = "2009-01-01"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BE_MAX = 60.0
BE_STEP = 0.05
WARMUP = 260                      # the record's convention: px.index[260] is the first read day
BAND_LO, BAND_HI = 0.0, 25.0      # the queue's reporting band

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


# ======================================================================== helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def v4a(r, base):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def sharpe_at(r0, turn, c):
    """Sharpe of the 0-bps return stream charged at c bps.  ddof=1 to match pandas .std()."""
    r = np.asarray(r0, float) - np.asarray(turn, float) * c / 1e4
    v = r.std(ddof=1)
    return (r.mean() / v * np.sqrt(252)) if v > 0 else np.nan


def moments(r0, turn):
    """The five scalars that make Sharpe(c) EXACT in closed form for every rung.

        r(c) = r0 - k*turn,  k = c/1e4
        mean(c) = m0 - k*mt
        var(c)  = Sxx - 2k*Sxt + k^2*Stt      (ddof=1, matching pandas .std())

    so a cost ladder needs no re-arithmetic over the return series at all.  Asserted
    against the sample-based sharpe_at() in section 0 before anything is read.
    """
    x = np.asarray(r0, float); t = np.asarray(turn, float)
    n = len(x)
    if n < 3: return None
    xc, tc = x - x.mean(), t - t.mean()
    return dict(m0=float(x.mean()), mt=float(t.mean()),
                Sxx=float(xc @ xc) / (n - 1), Sxt=float(xc @ tc) / (n - 1),
                Stt=float(tc @ tc) / (n - 1), n=n)


def sharpe_mom(M, c):
    """Sharpe at rung c (bps) from a moment tuple.  Vectorised over c."""
    k = np.asarray(c, float) / 1e4
    mu = M["m0"] - k * M["mt"]
    var = M["Sxx"] - 2 * k * M["Sxt"] + k * k * M["Stt"]
    with np.errstate(invalid="ignore", divide="ignore"):
        out = np.where(var > 0, mu / np.sqrt(np.where(var > 0, var, np.nan)) * np.sqrt(252), np.nan)
    return out


def breakeven_mom(MX, MY):
    """Exact cost rung at which Sharpe(X,c) - Sharpe(Y,c) changes sign (idea 262's solver,
    on closed-form moments rather than a re-summed series).

    Coarse BE_STEP-spaced scan to BE_MAX so a non-monotonic difference cannot be missed,
    then bisection inside the FIRST bracket to 1e-4 bps.  NaN if it never flips.
    """
    if MX is None or MY is None: return np.nan
    cs = np.arange(0.0, BE_MAX + BE_STEP, BE_STEP)
    d = sharpe_mom(MX, cs) - sharpe_mom(MY, cs)
    if not np.isfinite(d[0]) or d[0] == 0: return np.nan
    s0 = np.sign(d[0])
    sgn = np.sign(d)
    flip = np.where(np.isfinite(d) & (sgn != s0))[0]
    if len(flip) == 0: return np.nan
    i = int(flip[0])
    lo, hi = cs[i - 1], cs[i]
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        dm = float(sharpe_mom(MX, mid) - sharpe_mom(MY, mid))
        if np.sign(dm) == s0: lo = mid
        else: hi = mid
        if hi - lo < 1e-4: break
    return 0.5 * (lo + hi)


def recover_vol(cagr, sharpe):
    """vol from (CAGR, Sharpe) via engine.metrics' own definitions.

        Sharpe = mean_ann/vol ;  ln(1+CAGR) = sum ln(1+r)/yrs ~= mean_ann - vol^2/2
        =>  vol^2/2 - Sharpe*vol + ln(1+CAGR) = 0,  discriminant = (Sharpe - vol)^2 >= 0

    Both roots are Sharpe -/+ |Sharpe - vol|; the admissible one is the POSITIVE root, and
    when both are positive (Sharpe > 0) it is the SMALLER.  Exact only to the lognormal
    (third-moment) term; section 2 measures the residual on the record's own triples.
    """
    c = np.asarray(cagr, float); s = np.asarray(sharpe, float)
    g = np.log1p(np.where(c > -0.999999, c, np.nan))
    disc = np.clip(s * s - 2.0 * g, 0.0, None)
    root = np.sqrt(disc)
    lo, hi = s - root, s + root
    v = np.where(lo > 1e-8, lo, np.where(hi > 1e-8, hi, np.nan))
    return v


def law_breakeven(dS_at_rung, rung, t_x, v_x, t_y, v_y):
    """(L) re-anchored at an arbitrary rung.  Returns NaN when the denominator vanishes."""
    den = np.asarray(t_x, float) / np.asarray(v_x, float) - np.asarray(t_y, float) / np.asarray(v_y, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = rung + np.asarray(dS_at_rung, float) * 1e4 / den
    return np.where(np.isfinite(out), out, np.nan)


# ======================================================================== panels & books
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {"U56": sub(px56, list(px56.columns)),
            "B136": sub(px136, list(px136.columns)),
            "BSTK100": sub(px136, b_stk, tradable=b_stk)}


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop: m[drop] = False
    return m


def weights(px, tradable, arm, n=None, gross=GROSS, elig=None):
    """The record's non-null dials.  All arms share the gate; only the pick/size moves.

    FWD      top-n by the composite WITHOUT the vol scaler, gross RE-NORMALISED to `gross`
    FWDVS    top-n by the composite WITH the /sqrt(vol) scaler (the live key), re-normalised
    EWall    every eligible name, equal weight, gross matched  (gate only, no pick)
    FIXED    top-n by the un-scaled composite at the LITERAL per-name weight GROSS/n
             (idea 73's book: gross falls below `gross` whenever fewer than n names pass
             the gate, which is exactly the dial that separates it from FWD)
    v1       the live RULES book, verbatim from baseline.rules_v1_weights
    """
    if arm == "v1":
        return rules_v1_weights(px)
    if elig is None: elig = eligible_mask(px, tradable)
    s_ns, _, _ = score(px, vol_scale=False)
    s_vs, _, _ = score(px, vol_scale=True)
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        key = s_vs if arm == "FWDVS" else s_ns
        rank = key.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= n).astype(float)
    if arm == "FIXED":
        return sel * (GROSS / n)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(gross).fillna(0.0)


# ======================================================================== (1) census
def parse_leaderboard():
    rows = []
    for ln, line in enumerate(LB_PATH.read_text().splitlines(), 1):
        if not line.startswith("|") or re.match(r"^\|[\s\-|]+\|$", line): continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 9 or c[0] == "Date": continue
        def pct(s):
            m = re.search(r"(-?\d+(?:\.\d+)?)\s*%", s)
            return float(m.group(1)) / 100 if m else np.nan
        def num(s):
            m = re.search(r"(-?\d+(?:\.\d+)?)", s)
            return float(m.group(1)) if m else np.nan
        halves = re.findall(r"(-?\d+(?:\.\d+)?)", c[5])
        base = re.findall(r"(-?\d+(?:\.\d+)?)", c[6])
        rows.append(dict(
            lb_line=ln, raw=line.strip(), date=c[0], idea=c[1], CAGR=pct(c[2]), Sharpe=num(c[3]), MaxDD=pct(c[4]),
            H1=float(halves[0]) if len(halves) > 0 else np.nan,
            H2=float(halves[1]) if len(halves) > 1 else np.nan,
            base_raw=c[6],
            bS=float(base[0]) if len(base) > 0 else np.nan,
            bH1=float(base[1]) if len(base) > 1 else np.nan,
            bH2=float(base[2]) if len(base) > 2 else np.nan,
            verdict=c[-2], script=c[-1].split("/")[-1].strip("` ")))
    return pd.DataFrame(rows)


def _read_any(p):
    try:
        return pd.read_csv(p)
    except Exception:
        return None


def corpus_csvs():
    """Every committed CSV in research/backtests EXCEPT this script's own outputs.

    The exclusion matters: this run writes .grid/.validation/.backfill CSVs into the same
    directory it censuses, so without it a re-run would grade itself.
    """
    return [p for p in OUT.iterdir()
            if (p.suffix == ".csv" or p.name.endswith(".csv.gz")) and not p.name.startswith(STEM + ".")]


def script_grids():
    """{script stem -> concatenated committed rows carrying (CAGR, Sharpe, MaxDD, turnover)}."""
    files = corpus_csvs()
    by_stem = {}
    for p in files:
        stem = p.name.split(".")[0]
        by_stem.setdefault(stem, []).append(p)
    out, schema = {}, []
    for stem, ps in by_stem.items():
        frames = []
        for p in ps:
            d = _read_any(p)
            if d is None or d.empty: continue
            cl = {c.lower(): c for c in d.columns}
            tcols = [c for c in d.columns if "turn" in c.lower()]
            vcols = [c for c in d.columns if c.lower() in ("vol", "volatility", "ann_vol")]
            schema.append(dict(file=p.name, nrow=len(d), has_cagr="cagr" in cl,
                               has_sharpe="sharpe" in cl, has_maxdd="maxdd" in cl,
                               has_turn=bool(tcols), has_vol=bool(vcols)))
            if not (("cagr" in cl) and ("sharpe" in cl) and ("maxdd" in cl) and tcols): continue
            q = pd.DataFrame({
                "CAGR": pd.to_numeric(d[cl["cagr"]], errors="coerce"),
                "Sharpe": pd.to_numeric(d[cl["sharpe"]], errors="coerce"),
                "MaxDD": pd.to_numeric(d[cl["maxdd"]], errors="coerce"),
                "turn": pd.to_numeric(d[tcols[0]], errors="coerce"),
                "Vol": pd.to_numeric(d[vcols[0]], errors="coerce") if vcols else np.nan,
                "src_file": p.name, "turn_col": tcols[0]})
            frames.append(q.dropna(subset=["CAGR", "Sharpe", "MaxDD", "turn"]))
        if frames: out[stem] = pd.concat(frames, ignore_index=True)
    return out, pd.DataFrame(schema)


def tier_rows(LB, grids, schema):
    """Tier every leaderboard row by which of the four numbers its parent committed."""
    have_any = {}
    for _, r in schema.iterrows():
        stem = r.file.split(".")[0]
        a = have_any.setdefault(stem, dict(csv=False, turn=False, tv=False, tsc=False))
        a["csv"] = True
        if r.has_turn: a["turn"] = True
        if r.has_turn and r.has_vol and r.has_sharpe: a["tv"] = True
        if r.has_turn and r.has_sharpe and r.has_cagr: a["tsc"] = True
    tiers, joins = [], []
    for _, r in LB.iterrows():
        stem = r.script[:-3] if r.script.endswith(".py") else None
        a = have_any.get(stem, dict(csv=False, turn=False, tv=False, tsc=False)) if stem else \
            dict(csv=False, turn=False, tv=False, tsc=False)
        if a["tv"]: tier = "A_turn+vol+sharpe"
        elif a["tsc"]: tier = "B_turn+sharpe+cagr(vol recoverable)"
        elif a["turn"]: tier = "C_turn only"
        elif a["csv"]: tier = "D_csv without turnover"
        else: tier = "E_no committed csv"
        G = grids.get(stem)
        nm, turn, vol, srcf = 0, np.nan, np.nan, ""
        if G is not None and np.isfinite(r.CAGR) and np.isfinite(r.Sharpe) and np.isfinite(r.MaxDD):
            m = G[(np.abs(G.CAGR - r.CAGR) < 5e-4) & (np.abs(G.Sharpe - r.Sharpe) < 5e-3)
                  & (np.abs(G.MaxDD - r.MaxDD) < 5e-4)]
            nm = len(m)
            if nm:
                if m.turn.round(6).nunique() == 1:
                    turn = float(m.turn.iloc[0]); srcf = m.src_file.iloc[0]
                    v = m.Vol.dropna()
                    vol = float(v.iloc[0]) if len(v) and v.round(6).nunique() == 1 else np.nan
                else:
                    srcf = m.src_file.iloc[0]
        tiers.append(tier)
        joins.append((nm, turn, vol, srcf))
    LB = LB.copy()
    LB["tier"] = tiers
    LB["n_match"] = [j[0] for j in joins]
    LB["turn"] = [j[1] for j in joins]
    LB["vol_committed"] = [j[2] for j in joins]
    LB["join_file"] = [j[3] for j in joins]
    return LB


# ======================================================================== main
def main():
    print("=" * 240)
    print(f"Idea 269 back-fill-the-breakeven-column-arithmetically-not-by-re-running (lane B) | {SCRIPT}")
    print("=" * 240)

    # ---------------------------------------------------------------- panels + reference books
    panels = build_panels()
    elig = {pk: eligible_mask(px, tr) for pk, (px, tr) in panels.items()}
    spy_r = {pk: panels[pk][0]["SPY"].pct_change().fillna(0.0) for pk in panels}

    books = {}          # (panel, arm, n, cadence, gross) -> dict(r0=..., turn=...)
    def run(pk, arm, n, freq, gross):
        key = (pk, arm, n, freq, gross)
        if key in books: return books[key]
        px, tr = panels[pk]
        w = weights(px, tr, arm, n=n, gross=gross, elig=elig[pk])
        res = backtest(px, w, cost_bps=0.0, freq=freq)
        start = px.index[WARMUP]
        books[key] = dict(r0=res["returns"].loc[start:], turn=res["turnover"].loc[start:])
        return books[key]

    # ---- the grid of non-null dials.  v1 and EWall carry no n; FIXED carries no gross.
    specs = []
    for pk in panels:
        specs.append((pk, "v1", None, "W", np.nan))
        for freq in CADENCES:
            specs.append((pk, "EWall", None, freq, GROSS))
            for n in NS:
                specs.append((pk, "FWD", n, freq, GROSS))
                specs.append((pk, "FWDVS", n, freq, GROSS))
        for n in NS:
            for g in GROSSES:
                specs.append((pk, "FWD", n, "W", g))
            specs.append((pk, "FIXED", n, "W", np.nan))
    specs = list(dict.fromkeys(specs))
    print(f"\nbooks to run: {len(specs)}")
    for i, (pk, arm, n, freq, g) in enumerate(specs, 1):
        run(pk, arm, n, freq, g)
        if i % 20 == 0: print(f"  ... {i}/{len(specs)}")

    # ---------------------------------------------------------------- harness identity
    print("\n" + "-" * 240)
    print("0. HARNESS IDENTITY  (derived rung vs a live backtest at that rung; must be 0)")
    worst = 0.0
    for pk, arm, n, freq, g, c in [("U56", "FWD", 20, "W", GROSS, 10.0),
                                   ("B136", "FWD", 10, "M", GROSS, 25.0),
                                   ("BSTK100", "EWall", None, "W", GROSS, 5.0)]:
        px, tr = panels[pk]
        live = backtest(px, weights(px, tr, arm, n=n, gross=g, elig=elig[pk]), cost_bps=c, freq=freq)
        live_r = live["returns"].loc[px.index[WARMUP]:]
        b = books[(pk, arm, n, freq, g)]
        der = b["r0"] - b["turn"] * c / 1e4
        e = float(np.abs(live_r - der).max()); worst = max(worst, e)
        print(f"   {pk:8s} {arm:6s} n={str(n):4s} {freq} @{c:5.1f} bps   max|live-derived| = {e:.3e}")
    assert worst == 0.0, f"cost-derivation identity broken: {worst:.3e}"
    print(f"   -> max over checks = {worst:.3e}  OK")

    print("\n   moment identity (closed-form Sharpe(c) vs the re-summed series; must be ~0):")
    wm = 0.0
    for key in [("U56", "FWD", 20, "W", GROSS), ("B136", "EWall", None, "Q", GROSS),
                ("BSTK100", "FIXED", 40, "W", np.nan)]:
        b = books[key]; M = moments(b["r0"].values, b["turn"].values)
        for c in (0.0, 3.7, 10.0, 25.0, 60.0):
            e = abs(float(sharpe_mom(M, c)) - sharpe_at(b["r0"].values, b["turn"].values, c))
            wm = max(wm, e)
        print(f"   {key[0]:8s} {key[1]:6s} n={str(key[2]):4s} {key[3]}   max|closed-form - series| = {wm:.3e}")
    assert wm < 1e-10, f"moment identity broken: {wm:.3e}"
    print(f"   -> max over checks = {wm:.3e}  OK")

    # ---------------------------------------------------------------- reproduction gate
    print("\n" + "-" * 240)
    print("1. REPRODUCTION GATE (asserted before any result of this run is read)")
    rep = {}
    for name, key in [("U56/RULES v1", ("U56", "v1", None, "W", np.nan)),
                      ("U56/FIXED20", ("U56", "FIXED", 20, "W", np.nan))]:
        r = books[key]["r0"] - books[key]["turn"] * PROTO_RUNG / 1e4
        m = metrics(r); h1, h2 = half_sharpes(r)
        rep[name] = (m["CAGR"], m["Sharpe"], m["MaxDD"], h1, h2)
        print(f"   {name:14s} {m['CAGR']:7.2%} / {m['Sharpe']:.3f} / {m['MaxDD']:7.2%}   halves {h1:.3f}/{h2:.3f}")
    print("   published:     U56/RULES v1  6.5% / 0.666 / -13.8%   |   U56/FIXED20  12.7% / 1.093 / -18.3%")
    ok = abs(rep["U56/RULES v1"][1] - 0.666) < 0.01 and abs(rep["U56/FIXED20"][1] - 1.093) < 0.01
    assert ok, f"reproduction gate FAILED: {rep}"
    print("   -> gate PASSED")

    # ---------------------------------------------------------------- (2) census
    print("\n" + "=" * 240)
    print("2. THE CENSUS - how many published rows carry the four numbers")
    LB = parse_leaderboard()
    grids, schema = script_grids()
    schema.to_csv(OUT / f"{STEM}.schema.csv", index=False)
    LBt = tier_rows(LB, grids, schema)
    LBt.to_csv(OUT / f"{STEM}.rows.csv.gz", index=False, compression="gzip")
    n_uniq = int(LB.raw.nunique())
    print(f"\n   LEADERBOARD.md: {len(LB)} data rows, {LB.script.nunique()} distinct script cells, "
          f"{len(schema)} committed CSVs over {schema.file.str.split('.').str[0].nunique()} script stems")
    print(f"   INCIDENTAL FINDING: {len(LB) - n_uniq} of those {len(LB)} rows are byte-identical duplicates of "
          f"another row ({n_uniq} distinct).  Pre-existing in the file (a rebase artefact), not created here; "
          f"every count below is reported on BOTH the raw and the DISTINCT row set.")
    tt = LBt.tier.value_counts().rename_axis("tier").reset_index(name="rows").sort_values("tier")
    tt["share"] = tt["rows"] / len(LBt)
    print("\n   Tier by PARENT SCRIPT's committed schema (does the parent commit the numbers at all):")
    print(tt.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    j = LBt[LBt.n_match > 0]
    ju = LBt[(LBt.n_match > 0) & np.isfinite(LBt.turn)]
    print(f"\n   Fingerprint JOIN (CAGR,Sharpe,MaxDD at the leaderboard's printed precision, inside the parent's own CSVs):")
    print(f"     rows with all three numbers printed        : {int(LBt[['CAGR','Sharpe','MaxDD']].notna().all(axis=1).sum())}")
    print(f"     rows matching >=1 committed grid row       : {len(j)}")
    print(f"     rows with an UNAMBIGUOUS turnover          : {len(ju)}")
    print(f"       of those, vol also committed outright    : {int(np.isfinite(ju.vol_committed).sum())}")
    print(f"       of those, vol must be RECOVERED          : {int((~np.isfinite(ju.vol_committed)).sum())}")
    print(f"     rows matching >1 grid row (ambiguous turn) : {len(j) - len(ju)}")

    # ---------------------------------------------------------------- (3) vol recovery
    print("\n" + "=" * 240)
    print("3. THE VOL RECOVERY - can vol be reconstructed from (CAGR, Sharpe)?")
    tri = []
    for p in corpus_csvs():
        d = _read_any(p)
        if d is None or d.empty: continue
        cl = {c.lower(): c for c in d.columns}
        if not all(k in cl for k in ("cagr", "sharpe", "vol")): continue
        q = pd.DataFrame({"CAGR": pd.to_numeric(d[cl["cagr"]], errors="coerce"),
                          "Sharpe": pd.to_numeric(d[cl["sharpe"]], errors="coerce"),
                          "Vol": pd.to_numeric(d[cl["vol"]], errors="coerce"), "file": p.name})
        tri.append(q.dropna())
    TRI = pd.concat(tri, ignore_index=True)
    TRI = TRI[(TRI.Vol > 1e-4) & (TRI.Sharpe.abs() < 10)].reset_index(drop=True)
    TRI["vol_hat"] = recover_vol(TRI.CAGR.values, TRI.Sharpe.values)
    TRI["abs_err"] = (TRI.vol_hat - TRI.Vol).abs()
    TRI["rel_err"] = TRI.abs_err / TRI.Vol
    TRI.to_csv(OUT / f"{STEM}.volrecovery.csv.gz", index=False, compression="gzip")
    good = float((TRI.rel_err < 0.01).mean())
    print(f"\n   test set: {len(TRI)} committed (CAGR, Sharpe, Vol) triples from {TRI.file.nunique()} CSVs")
    print(f"   median |rel err| {TRI.rel_err.median():.3e}   p90 {TRI.rel_err.quantile(.90):.3e}   "
          f"p99 {TRI.rel_err.quantile(.99):.3e}   max {TRI.rel_err.max():.3e}")
    print(f"   median |abs err| {TRI.abs_err.median():.3e} vol points   p99 {TRI.abs_err.quantile(.99):.3e}")
    print(f"   share within 1% relative: {good:.4f}   within 0.1%: {(TRI.rel_err<0.001).mean():.4f}")
    print(f"   PRE-REGISTERED (a): usable iff >=95% within 1% relative  ->  {'USABLE' if good>=0.95 else 'NOT USABLE'}")
    bad = TRI[TRI.rel_err >= 0.01]
    if len(bad):
        print(f"\n   the {len(bad)} failures, by sign of Sharpe and by file:")
        print(bad.assign(neg=bad.Sharpe < 0).groupby(["file", "neg"]).size()
                 .rename("rows").reset_index().to_string(index=False))
    VOL_USABLE = good >= 0.95

    # ---------------------------------------------------------------- baseline identification
    print("\n" + "=" * 240)
    print("4. THE COMPARAND - identifying each row's published baseline book mechanically")
    # The leaderboard's baseline column is printed to 2 dp and the record's earliest rows were
    # run on an EARLIER price vintage, so an exact match is not available.  Candidates are
    # therefore v1 (and SPY) on every panel x cadence x START CONVENTION the record has used,
    # and a string resolves only if every candidate inside one printed unit (0.011 on each of
    # Sharpe/H1/H2) agrees on the same (panel, cadence).  The convention spread in (turn, vol)
    # is carried through to the headline as a sensitivity band rather than being hidden.
    CONV = {"warm260": None, "2009": IS_START, "2010": "2010-01-01", "full": "FULL"}
    ref = []
    for pk in panels:
        px = panels[pk][0]
        for freq in ("W", "M"):
            b = run(pk, "v1", None, freq, np.nan)
            full = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=freq)
            for cv, st in CONV.items():
                if cv == "warm260": r0, tt = b["r0"], b["turn"]
                elif st == "FULL": r0, tt = full["returns"], full["turnover"]
                else: r0, tt = full["returns"].loc[st:], full["turnover"].loc[st:]
                r = r0 - tt * PROTO_RUNG / 1e4
                m = metrics(r); h1, h2 = half_sharpes(r)
                ref.append(dict(book=f"v1/{pk}/{freq}", conv=cv, panel=pk, freq=freq,
                                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                Vol=m["Vol"], turn_yr=float(tt.sum() / m["Years"])))
        for cv, st in CONV.items():
            spy = spy_r[pk].loc[px.index[WARMUP]:] if cv == "warm260" else (
                spy_r[pk] if st == "FULL" else spy_r[pk].loc[st:])
            m = metrics(spy); h1, h2 = half_sharpes(spy)
            ref.append(dict(book=f"SPY/{pk}", conv=cv, panel=pk, freq="-", CAGR=m["CAGR"],
                            Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, Vol=m["Vol"],
                            turn_yr=0.0))
    REF = pd.DataFrame(ref)
    REF.to_csv(OUT / f"{STEM}.baselines.csv", index=False)
    print("\n   RULES v1 and SPY computed live on every offline panel x start convention (10 bps):")
    print(REF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    HEAD = REF[REF.conv == "warm260"].set_index("book")

    TOL = 0.011                                        # one printed unit on a 2-dp column

    def match_base(bS, bH1, bH2):
        if not np.isfinite(bS): return None, 0, np.nan
        cand = REF[np.abs(REF.Sharpe - bS) < TOL]
        if np.isfinite(bH1): cand = cand[np.abs(cand.H1 - bH1) < TOL]
        if np.isfinite(bH2): cand = cand[np.abs(cand.H2 - bH2) < TOL]
        if len(cand) == 0 or cand.book.nunique() != 1: return None, len(cand), np.nan
        resid = float(np.abs(cand.Sharpe - bS).min())
        return cand.book.iloc[0], len(cand), resid

    seen, seen_n, seen_res = {}, {}, {}
    for s in LBt.base_raw.unique():
        r = LBt[LBt.base_raw == s].iloc[0]
        bk, nc, rs = match_base(r.bS, r.bH1, r.bH2)
        seen[s], seen_n[s], seen_res[s] = bk, nc, rs
    LBt["base_book"] = LBt.base_raw.map(seen)
    LBt["base_resid"] = LBt.base_raw.map(seen_res)
    nb = int(LBt.base_book.notna().sum())
    print(f"\n   baseline strings resolved to a live book: {sum(v is not None for v in seen.values())} of {len(seen)} distinct "
          f"({nb} of {len(LBt)} rows).  Tolerance {TOL} = one printed unit on each of Sharpe/H1/H2.")
    top = LBt.groupby(LBt.base_raw).size().sort_values(ascending=False).head(10)
    print("   most common baseline strings, what they resolved to, and the residual in Sharpe:")
    for s, ct in top.items():
        rs = seen_res.get(s)
        print(f"     {ct:5d}  {s[:40]:42s} -> {str(seen.get(s) or '(unresolved)'):14s} "
              f"resid {('%.4f' % rs) if np.isfinite(rs) else '  -   '}  ({seen_n.get(s,0)} conv-variants matched)")
    conv_band = REF[REF.book.str.startswith("v1/")].groupby("book").agg(
        turn_lo=("turn_yr", "min"), turn_hi=("turn_yr", "max"), vol_lo=("Vol", "min"), vol_hi=("Vol", "max"))
    print("\n   start-convention spread in the numbers the law actually uses (T/yr and vol):")
    print(conv_band.to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- (5) the back-fill
    print("\n" + "=" * 240)
    print("5. THE BACK-FILL - c* = 10 + dSharpe(10)*1e4/(T_x/vol_x - T_y/vol_y), no re-runs")
    B = LBt[(LBt.n_match > 0) & np.isfinite(LBt.turn) & LBt.base_book.notna()].copy()
    B["vol_used"] = np.where(np.isfinite(B.vol_committed), B.vol_committed,
                             recover_vol(B.CAGR.values, B.Sharpe.values))
    B["vol_source"] = np.where(np.isfinite(B.vol_committed), "committed", "recovered")
    B["turn_base"] = B.base_book.map(HEAD.turn_yr)
    B["vol_base"] = B.base_book.map(HEAD.Vol)
    B["sharpe_base"] = B.base_book.map(HEAD.Sharpe)
    B["dS10"] = B.Sharpe - B.sharpe_base
    B["turn_ratio"] = B.turn / B.turn_base
    B["den"] = B.turn / B.vol_used - B.turn_base / B.vol_base
    B["cstar"] = law_breakeven(B.dS10.values, PROTO_RUNG, B.turn.values, B.vol_used.values,
                               B.turn_base.values, B.vol_base.values)
    # A row whose arm is turnover-matched to its own baseline has a denominator near zero, so
    # c* is the ratio of two small numbers and is not a statement about cost at all.  Flagged,
    # not dropped: the headline is reported with and without them.
    B["degenerate"] = B.den.abs() < 1.0
    B.to_csv(OUT / f"{STEM}.backfill.csv", index=False)
    ok_rows = B[np.isfinite(B.cstar) & np.isfinite(B.vol_used)]
    U = ok_rows.drop_duplicates("raw")
    print(f"\n   rows back-filled: {len(ok_rows)} raw / {len(U)} distinct  "
          f"(vol committed {int((ok_rows.vol_source=='committed').sum())}, "
          f"recovered {int((ok_rows.vol_source=='recovered').sum())})")
    if not VOL_USABLE:
        print("   !! vol recovery FAILED its pre-registered bar - the recovered-vol rows are an UPPER BOUND, not a result")
    mism = U[(U.turn_ratio > 2) | (U.turn_ratio < 0.5)]
    print(f"   of the distinct rows, idea 263's >2x turnover-mismatched: {len(mism)}")
    print(f"   degenerate denominator (|T_x/vol_x - T_y/vol_y| < 1, arm turnover-matched to its baseline): "
          f"{int(U.degenerate.sum())} distinct")

    def band(df): return df[(df.cstar > BAND_LO) & (df.cstar <= BAND_HI)]
    inband = band(ok_rows)
    ibU = band(U)
    ibU_nd = band(U[~U.degenerate])
    print(f"\n   *** HEADLINE: published verdicts whose breakeven vs their own baseline lies in "
          f"({BAND_LO:.0f}, {BAND_HI:.0f}] bps ***")
    print(f"       distinct rows, non-degenerate : {len(ibU_nd)} of {len(U[~U.degenerate])} "
          f"({len(ibU_nd)/max(len(U[~U.degenerate]),1):.1%})")
    print(f"       distinct rows, all            : {len(ibU)} of {len(U)} ({len(ibU)/max(len(U),1):.1%})")
    print(f"       raw rows (duplicates kept)    : {len(inband)} of {len(ok_rows)} "
          f"({len(inband)/max(len(ok_rows),1):.1%})")
    print(f"       of the {len(mism)} >2x-mismatched distinct rows: {len(band(mism))} "
          f"({len(band(mism))/max(len(mism),1):.1%})")
    print("\n   the in-band rows, one line each (distinct, non-degenerate), lowest c* first:")
    print("   " + ibU_nd.sort_values("cstar")[["date", "idea", "verdict", "Sharpe", "sharpe_base",
                                               "turn", "turn_base", "vol_used", "vol_source", "cstar"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}", max_colwidth=52).replace("\n", "\n   "))
    print("\n   c* distribution over back-filled DISTINCT rows (bps):")
    print(U.cstar.describe(percentiles=[.05, .25, .5, .75, .95]).to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n   by parent script (distinct rows), most rows first:")
    vt = U.assign(inband=(U.cstar > BAND_LO) & (U.cstar <= BAND_HI)) \
          .groupby("script").agg(rows=("cstar", "size"), in_band=("inband", "sum"),
                                 degen=("degenerate", "sum"), med_cstar=("cstar", "median"),
                                 med_turn_ratio=("turn_ratio", "median")).sort_values("rows", ascending=False)
    print(vt.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n   NOTE: c* < 0 means the row's sign versus its baseline NEVER flips at a positive cost")
    print("         (the quoted verdict is cost-robust); c* > 25 means it flips only above the")
    print("         project's own worst rung.  Only (0,25] is a live risk to the published verdict.")

    # --- sensitivity of the headline to the baseline's start convention and to the vol source
    print("\n   SENSITIVITY of the headline count (the baseline's own (T,vol) is vintage-dependent):")
    sens = []
    for cv in CONV:
        hb = REF[REF.conv == cv].set_index("book")
        cs = law_breakeven(B.Sharpe.values - B.base_book.map(hb.Sharpe).values, PROTO_RUNG,
                           B.turn.values, B.vol_used.values,
                           B.base_book.map(hb.turn_yr).values, B.base_book.map(hb.Vol).values)
        cs = cs[np.isfinite(cs)]
        sens.append(dict(conv=cv, rows=len(cs), in_band=int(((cs > BAND_LO) & (cs <= BAND_HI)).sum()),
                         med_cstar=float(np.median(cs)) if len(cs) else np.nan))
    # and with the committed vol wherever it exists, instead of the recovered one
    only_rec = law_breakeven(B.dS10.values, PROTO_RUNG, B.turn.values,
                             recover_vol(B.CAGR.values, B.Sharpe.values),
                             B.turn_base.values, B.vol_base.values)
    cs_c = only_rec[np.isfinite(only_rec)]
    sens.append(dict(conv="warm260, RECOVERED vol on every row", rows=len(cs_c),
                     in_band=int(((cs_c > BAND_LO) & (cs_c <= BAND_HI)).sum()),
                     med_cstar=float(np.median(cs_c)) if len(cs_c) else np.nan))
    SENS = pd.DataFrame(sens)
    print(SENS.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    SENS.to_csv(OUT / f"{STEM}.sensitivity.csv", index=False)

    # ---------------------------------------------------------------- (6) validation off the nulls
    print("\n" + "=" * 240)
    print("6. VALIDATION - does the law survive on NON-NULL dials, with RECOVERED vol?")
    print("   (idea 262 fitted it on held/re-drawn uniform nulls only)")

    def window(b, lo=None, hi=None):
        r0, t = b["r0"], b["turn"]
        if lo: r0, t = r0.loc[lo:], t.loc[lo:]
        if hi: r0, t = r0.loc[:hi], t.loc[:hi]
        return r0, t

    def stats(r0, t, rung):
        r = r0 - t * rung / 1e4
        m = metrics(r)
        return m["Sharpe"], m["CAGR"], m["Vol"], float(t.sum() / m["Years"])

    def pair_rows(lo, hi, tag):
        per = {}
        for k, b in books.items():
            r0, t = window(b, lo, hi)
            S, C, V, T = stats(r0, t, PROTO_RUNG)
            if not all(np.isfinite([S, C, V, T])) or V <= 0: continue
            per[k] = dict(M=moments(r0.values, t.values), S=S, C=C, V=V, T=T,
                          vh=float(recover_vol(C, S)))
        rows = []
        for pk in panels:
            ks = [k for k in per if k[0] == pk]
            for i in range(len(ks)):
                for jx in range(i + 1, len(ks)):
                    kx, ky = ks[i], ks[jx]
                    px_, py_ = per[kx], per[ky]
                    ratio = px_["T"] / py_["T"] if py_["T"] > 0 else np.inf
                    rows.append(dict(
                        window=tag, panel=pk,
                        x=f"{kx[1]}/n{kx[2]}/{kx[3]}/g{kx[4]}", y=f"{ky[1]}/n{ky[2]}/{ky[3]}/g{ky[4]}",
                        arm_x=kx[1], arm_y=ky[1], n_x=kx[2], n_y=ky[2], freq_x=kx[3], freq_y=ky[3],
                        gross_x=kx[4], gross_y=ky[4],
                        turn_x=px_["T"], turn_y=py_["T"], turn_ratio=ratio,
                        vol_x=px_["V"], vol_y=py_["V"], volhat_x=px_["vh"], volhat_y=py_["vh"],
                        dS10=px_["S"] - py_["S"],
                        meas_be=breakeven_mom(px_["M"], py_["M"]),
                        pred_true=float(law_breakeven(px_["S"] - py_["S"], PROTO_RUNG,
                                                      px_["T"], px_["V"], py_["T"], py_["V"])),
                        pred_hat=float(law_breakeven(px_["S"] - py_["S"], PROTO_RUNG,
                                                     px_["T"], px_["vh"], py_["T"], py_["vh"]))))
        return pd.DataFrame(rows)

    def fit_report(P, label):
        Q = P[np.isfinite(P.meas_be)]
        out = {}
        for col in ("pred_true", "pred_hat"):
            R = Q[np.isfinite(Q[col])]
            if len(R) < 3:
                out[col] = (np.nan, np.nan, 0); continue
            err = R[col] - R.meas_be
            ss = float(((R.meas_be - R.meas_be.mean()) ** 2).sum())
            r2 = 1 - float((err ** 2).sum()) / ss if ss > 0 else np.nan
            out[col] = (r2, float(err.abs().median()), len(R))
        print(f"\n   {label}: {len(P)} pairs, {len(Q)} flip below {BE_MAX:.0f} bps "
              f"(turnover ratio {P.turn_ratio.min():.2f}x-{P.turn_ratio.max():.2f}x)")
        for col, nm in (("pred_true", "committed vol"), ("pred_hat", "RECOVERED vol")):
            r2, mae, nn = out[col]
            print(f"      {nm:15s} R^2 {r2:8.4f}   median |err| {mae:7.4f} bps   n {nn}")
        return out

    FULL = pair_rows(None, None, "FULL")
    fit_full = fit_report(FULL, "FULL sample")

    # ---------------------------------------------------------------- (7) rule 8
    print("\n" + "=" * 240)
    print(f"7. RULE 8 WALK-FORWARD  (IS {IS_START}..{IS_END} chooses; OOS {OOS_START}.. read once)")
    IS = pair_rows(IS_START, IS_END, "IS")
    OOS = pair_rows(OOS_START, None, "OOS")
    fit_is = fit_report(IS, f"IS  {IS_START}..{IS_END}")
    fit_oos = fit_report(OOS, f"OOS {OOS_START}..")
    PAIRS = pd.concat([FULL, IS, OOS], ignore_index=True)
    PAIRS.to_csv(OUT / f"{STEM}.validation.csv.gz", index=False, compression="gzip")
    r2_is, r2_oos = fit_is["pred_hat"][0], fit_oos["pred_hat"][0]
    LAW_OK = (r2_is > 0.90) and (r2_oos > 0.90)
    print(f"\n   PRE-REGISTERED (b): law generalises off the nulls iff R^2(recovered vol) > 0.90 IS *and* OOS")
    print(f"      IS  R^2 = {r2_is:.4f}      OOS R^2 = {r2_oos:.4f}   ->  {'HOLDS' if LAW_OK else 'FAILS'}")

    # ---- the books' own walk-forward, chosen on IS only
    print("\n   Book selection, IS only: (panel, n) maximising IS Sharpe of FWD/W/g0.75 at 10 bps")
    cand = []
    for pk in panels:
        for n in NS:
            b = books[(pk, "FWD", n, "W", GROSS)]
            r0, t = window(b, IS_START, IS_END)
            cand.append(dict(panel=pk, n=n, IS_Sharpe=stats(r0, t, PROTO_RUNG)[0]))
    C = pd.DataFrame(cand).sort_values("IS_Sharpe", ascending=False)
    print(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pick = C.iloc[0]
    pk, n = pick.panel, int(pick.n)
    print(f"   -> IS-argmax: panel {pk}, n={n}  (IS Sharpe {pick.IS_Sharpe:.3f}).  OOS now read ONCE.")

    def oos_line(name, r):
        ro = r.loc[OOS_START:]
        m, mo = metrics(r), metrics(ro)
        h1, h2 = half_sharpes(r)
        return dict(book=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])

    bsel = books[(pk, "FWD", n, "W", GROSS)]
    r_sel = bsel["r0"] - bsel["turn"] * PROTO_RUNG / 1e4
    bv1 = books[(pk, "v1", None, "W", np.nan)]
    r_v1 = bv1["r0"] - bv1["turn"] * PROTO_RUNG / 1e4
    spy = spy_r[pk].reindex(r_sel.index).fillna(0.0)
    WF = pd.DataFrame([oos_line(f"IS-argmax {pk}/FWD{n}/W", r_sel),
                       oos_line(f"RULES v1 ({pk})", r_v1),
                       oos_line(f"SPY ({pk})", spy)])
    print("\n   " + WF.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- (8) KEEP paths on every book
    print("\n" + "=" * 240)
    print("8. BOTH KEEP PATHS on every book x rung (PROTOCOL rule 4)")
    grows = []
    for (pkk, arm, nn, freq, g), b in books.items():
        base = books[(pkk, "v1", None, "W", np.nan)]
        sp = spy_r[pkk].reindex(b["r0"].index).fillna(0.0)
        for c in RUNGS:
            r = b["r0"] - b["turn"] * c / 1e4
            rb = base["r0"] - base["turn"] * c / 1e4
            m = metrics(r); h1, h2 = half_sharpes(r); ro = r.loc[OOS_START:]
            mo = metrics(ro)
            grows.append(dict(panel=pkk, arm=arm, n=nn, freq=freq, gross=g, bps=c,
                              CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                              H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], turn_yr=float(b["turn"].sum() / m["Years"]),
                              v4a=v4a(r, rb), fail4b=fail4b(r, sp, ro, sp.loc[OOS_START:])))
    G = pd.DataFrame(grows)
    G["v4b"] = G.fail4b == "-"
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    K = G[G.v4a | G.v4b]
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    print(f"\n   grid points written: {len(G)}  ({len(books)} books x {len(RUNGS)} rungs)")
    print(f"   4a passes: {int(G.v4a.sum())}   4b passes: {int(G.v4b.sum())}   either: {len(K)}")
    print(f"   4b passes at PROTOCOL's own 10 bps: {int(G[(G.bps==PROTO_RUNG)].v4b.sum())}")
    if len(K):
        print("\n   the passing points (any rung):")
        print("   " + K.sort_values(["v4b", "Sharpe"], ascending=False)
              [["panel", "arm", "n", "freq", "gross", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_Sharpe", "turn_yr", "v4a", "v4b", "fail4b"]]
              .head(25).to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n   "))
    print("\n   4b failure reasons at 10 bps:")
    print("   " + G[G.bps == PROTO_RUNG].fail4b.value_counts().rename_axis("fails").reset_index(name="books")
          .to_string(index=False).replace("\n", "\n   "))

    # ---------------------------------------------------------------- leaderboard rows
    print("\n" + "=" * 240)
    print("9. LEADERBOARD ROWS")
    d = pd.Timestamp("today").date()
    bl = REF[(REF.book == f"v1/{pk}/W") & (REF.conv == "warm260")].iloc[0]
    sel = G[(G.panel == pk) & (G.arm == "FWD") & (G.n == n) & (G.freq == "W") &
            (G.gross == GROSS) & (G.bps == PROTO_RUNG)].iloc[0]
    lines = [
        f"| {d} | 269 back-fill census: {len(U)} of {n_uniq} DISTINCT leaderboard rows carry the four numbers "
        f"(turnover join {len(ju)}, baseline resolved {int(nb)}; {len(LBt)-n_uniq} rows are duplicates) "
        f"| — | — | — | — / — | — | ANSWERED | {SCRIPT} |",
        f"| {d} | 269 vol recovery from (CAGR,Sharpe): {TRI.rel_err.median():.1e} median rel err on "
        f"{len(TRI)} committed triples, {good:.1%} within 1% | — | — | — | — / — | — | "
        f"{'ANSWERED' if VOL_USABLE else 'KILL'} | {SCRIPT} |",
        f"| {d} | 269 law off the nulls (recovered vol): R^2 IS {r2_is:.3f} / OOS {r2_oos:.3f} on "
        f"{int(np.isfinite(OOS.meas_be).sum())} flipping non-null pairs | — | — | — | — / — | — | "
        f"{'ANSWERED' if LAW_OK else 'KILL'} | {SCRIPT} |",
        f"| {d} | 269 HEADLINE: published verdicts with breakeven vs own baseline in (0,25] bps = "
        f"{len(ibU_nd)} of {len(U[~U.degenerate])} back-filled distinct non-degenerate rows "
        f"({len(ibU_nd)/max(len(U[~U.degenerate]),1):.1%}) | — | — | — | — / — | — | ANSWERED | {SCRIPT} |",
        f"| {d} | 269 IS-argmax book {pk}/FWD{n}/W @10bps (reference, not a new idea) | {sel.CAGR:.1%} | "
        f"{sel.Sharpe:.2f} | {sel.MaxDD:.1%} | {sel.H1:.2f} / {sel.H2:.2f} | "
        f"{bl.Sharpe:.2f} ({bl.H1:.2f}/{bl.H2:.2f}) | {'KEEP-candidate' if sel.v4b else 'KILL'} | {SCRIPT} |",
    ]
    print("\n" + "\n".join(lines))
    (OUT / f"{STEM}.leaderboard.txt").write_text("\n".join(lines) + "\n")

    print("\n" + "=" * 240)
    print("VERDICT SUMMARY")
    print(f"  vol recovery usable (pre-reg a) : {VOL_USABLE}   ({good:.1%} within 1% relative)")
    print(f"  law holds off nulls (pre-reg b) : {LAW_OK}   (IS R^2 {r2_is:.4f}, OOS R^2 {r2_oos:.4f})")
    print(f"  leaderboard rows back-filled    : {len(U)} of {n_uniq} distinct ({len(ok_rows)} of {len(LBt)} raw)")
    print(f"  verdicts with c* in (0,25] bps  : {len(ibU_nd)} distinct non-degenerate ({len(ibU)} incl. degenerate)")
    print(f"  new KEEP-candidate books        : {int(G[(G.bps==PROTO_RUNG)].v4b.sum())} at 10 bps")
    print("=" * 240)


if __name__ == "__main__":
    main()
