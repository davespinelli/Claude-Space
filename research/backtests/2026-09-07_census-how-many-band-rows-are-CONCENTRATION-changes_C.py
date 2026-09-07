#!/usr/bin/env python3
"""Idea 359: census -- how many of the record's 'band' rows changed the book's WIDTH
rather than its trading rule?

Idea 349 established that a cell reported as a *band* can hold 7.6 names where its
parent holds 19.1 and still be labelled a band: the ENTRY buffer `e` moves holdings
(spearman(e, names) -0.988) far more than it moves turnover (-0.298), so it is a
CONCENTRATION dial wearing a band's name.  The EXIT buffer `x` under the parent's
k_t = |{rank <= n}| cap is name-count-NEUTRAL (spearman +0.000) and is a real
turnover dial.  The queue's question: across the whole committed record, how many
rows that claim a band/hysteresis result are of the first kind?

THE TEST, pre-registered before any number was read:

  [A] CENSUS OF THE COMMITTED RECORD.  Parse every data row of LEADERBOARD.md, flag
      the ones whose Idea text matches a BAND lexicon, then split those into
      - INSTRUMENT rows: the band is a trading rule (hysteresis gate, no-trade zone,
        entry/exit buffer, re-entry threshold);
      - INTERVAL rows: 'band' names an interval of a PARAMETER (admissible gross band,
        turnover-ratio band, confidence band) and no trading rule is banded at all.
      For every INSTRUMENT row, resolve its Script column to the committed artefacts
      and ask the queue's literal question: is mean holdings RECOVERABLE from a
      committed CSV?  A row is recoverable only if some CSV of that script carries
      both a holdings-like column and a band-dial column.  Counts are reported for
      the whole set; the classification is TEXTUAL and the lexicon is printed in full
      so a reader can re-run it.

  [B] DIRECT MEASUREMENT (the part that actually answers the question).  Because [A]
      is expected to leave most rows UNDEFINED, re-measure the record's band
      CONSTRUCTIONS from scratch and price each one's width effect:
        MAB-EWALL   200d MA band with hysteresis (baseline.band_state), hold every
                    in-band name at g/N.  Parent b = 0 (the hard 200d gate).
        MAB-TOPN    same band on ELIGIBILITY, then the hard top-n composite cut.
        RANKX       exit buffer: hold until rank > n + x, cap k_t = |{rank <= n}|.
                    Parent x = 0 (the hard cut).   [idea 331/349's band]
        RANKE       entry buffer: enter only at rank <= n - e, same cap.
                    Parent e = 0.                  [idea 349's entry side]
      For every cell: mean holdings/day, dNames vs the family's own dial-0 parent,
      spearman(dial, names), turnover, Sharpe, CAGR, MaxDD, halves, OOS, 4a/4b.
      A construction is WIDTH-CHANGING if |dNames| / names(parent) exceeds 5% at the
      family's largest dial on a majority of panel x n cells; NEUTRAL otherwise.
      The 5% threshold is pre-registered, and the full dNames ladder is printed so
      the reader can move it.

  [C] ATTRIBUTION.  Map each INSTRUMENT row of [A] to a [B] construction family by
      its own text, and report how many committed band rows sit on a construction
      measured WIDTH-CHANGING.  Rows whose construction cannot be identified are
      reported as UNATTRIBUTED, never as either verdict.

  [D] KEEP paths 4a and 4b at EVERY grid point, at cost rungs {0, 10, 25} bps.

  [E] RULE 8 walk-forward: dial chosen on 2008-2016 by IS Sharpe at 10 bps, 2017-2026
      read once, per family x panel x n, against the family's dial-0 parent, the
      OOS-best cell (regret), RULES v2 (live) and SPY.

Exactly TWO tuned parameters: the band dial value and n.  Construction family, panel,
book-form and cost rung are REPORTED axes -- every point of every axis is printed and
written to `<slug>.grid.csv`.

Book (fixed, idea 331/349's convention, never tuned): composite = the RULES v1 score
with the vol scaler OFF; eligibility = above the 200d MA and vol20 < 0.60; NORM
weights w_i = g/k at g = 0.75 so no dial can smuggle in a gross change; WEEKLY
rebalance; next-day execution; 10 bps per unit turnover at the anchor rung.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which
flatters every momentum book; the levels are optimistic, the dial-DIFFERENCES much
less so.  (2) SMALL439 starts 2010-01-04, so its halves are not the same calendar
halves as U56/B136 and its rule-8 IS window is effectively 2010-2016.  (3) [A] and [C]
are TEXT classifications of a hand-written leaderboard: they are reproducible but not
authoritative, and both the lexicon and every classified row are committed so the
call can be audited.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, re, sys, glob, csv
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights, band_state          # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_census-how-many-band-rows-are-CONCENTRATION-changes_C"
OUT = ROOT / "research" / "backtests"
LB = ROOT / "research" / "LEADERBOARD.md"
PARENT349 = OUT / "2026-09-07_does-a-band-on-the-EXIT-ONLY-beat-a-band-on-both-sides_C.grid.csv"

MAX_VOL, GROSS = 0.60, 0.75
FREQ = "W"
NS = [10, 20]
BS = [0.00, 0.01, 0.03, 0.05, 0.08, 0.12]     # MA band half-width
XS = [0, 5, 10, 20, 40, 80]                   # exit buffer
ES = [0, 2, 4, 6, 8, 12]                      # entry buffer
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
WIDTH_TOL = 0.05                              # pre-registered: >5% of parent names = WIDTH-CHANGING

# ---------------------------------------------------------------- [A] lexicons (printed in full)
BAND_LEX = [r"\bbands?\b", r"\bbanded\b", r"\bband\d+\b", r"hyster", r"\bbuffer",
            r"no-?trade", r"dead-?band", r"dead-?zone", r"re-?entry threshold"]
INTERVAL_LEX = [r"gross band", r"admissible .{0,24}band", r"band per n", r"ratio.{0,12}band",
                r"confidence band", r"\bg-band\b", r"band of gross", r"turnover.{0,12}band",
                r"\bbandwidth\b"]
FAMILY_LEX = [                                # -> [B] construction family
    ("RANKE",     [r"entry buffer", r"\be\s*=\s*\d", r"ENTRY side", r"enter at rank"]),
    ("RANKX",     [r"exit buffer", r"\bx\s*=\s*\d", r"EXIT side", r"exit at rank"]),
    # MA-band cues next: a percentage band width, or an explicit trend/200d/gate reference
    ("MAB",       [r"gate\s*=\s*band", r"band\s*>?=?\s*0\.\d", r"\bb\s*=\s*0\.\d", r"200d",
                   r"\bMA\b", r"trend.{0,16}band", r"band.{0,16}trend", r"\bband\s*[0-9]\b",
                   r"hyster"]),
    # then rank-band cues: a no-trade zone or an integer band width around n
    ("RANKM",     [r"no-?trade", r"\bm\s*=\s*\d+", r"BAND\d\d", r"band.{0,20}rank",
                   r"rank.{0,20}band", r"\bm\b.{0,8}band", r"band.{0,8}\bm\b"]),
]
HOLD_COL = re.compile(r"^(names|mean_names|names_mean|holdings|mean_holdings|n_names|nhold|"
                      r"avg_names|n_held|held|k|k_t|kbar)$", re.I)
DIAL_COL = re.compile(r"^(band|b|m|x|e|width|halfwidth|dial|buffer|gate)$", re.I)
RECOVER_FILES = {}                            # stem -> committed CSVs carrying holdings AND a dial


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- book machinery
def rank_frame(px, drop_spy=False, band=0.0):
    """Composite rank among eligible names.  band > 0 replaces the hard 200d gate in the
    ELIGIBILITY test with baseline.band_state's hysteresis band; band = 0 is the hard gate."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    trend = above if band <= 0 else band_state(px, band)
    elig = trend & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    return rk <= n


def sel_buf(px, rk, n, e, x, freq=FREQ):
    """idea 349's sel_ex: enter at rank <= n-e, hold until rank > n+x; cap = |{rank <= n}|."""
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    enter_at = n - e
    held = []
    last = np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n + x]
            held.sort(key=lambda j: r[j])
            if len(held) > cap:
                held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs_ = set(held)
                for j in order:
                    if len(held) >= cap:
                        break
                    if r[j] != r[j] or r[j] > enter_at:
                        break
                    if j not in hs_:
                        held.append(j); hs_.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols))
            last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return GROSS * s.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, cost_bps=0.0, freq=FREQ):
    """Vectorised-loop clone of engine.backtest.  Asserted at 0.000e+00 in section [0]."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT)
    cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series((held > 1e-12).sum(axis=1), index=idx))


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def spearman(a, b):
    x, y = pd.Series(list(a), dtype=float).rank(), pd.Series(list(b), dtype=float).rank()
    c = x.corr(y)
    return float(c) if c == c else float("nan")


# ================================================================ [A] census
def census():
    rows = []
    for line in LB.read_text().split("\n"):
        if not line.startswith("|") or line.startswith("| Date") or set(line.strip("|").strip()) <= set("-| "):
            continue
        p = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(p) < 4:
            continue
        rows.append({"date": p[0], "idea": p[1], "verdict": p[-2] if len(p) >= 3 else "",
                     "script": p[-1]})
    df = pd.DataFrame(rows)
    band_re = re.compile("|".join(BAND_LEX), re.I)
    intv_re = re.compile("|".join(INTERVAL_LEX), re.I)
    df["is_band"] = df["idea"].str.contains(band_re)
    df["is_interval"] = df["idea"].str.contains(intv_re)
    df["kind"] = np.where(~df["is_band"], "not-a-band-row",
                 np.where(df["is_interval"], "INTERVAL", "INSTRUMENT"))

    fams = []
    for t in df["idea"]:
        hit = ""
        for fam, pats in FAMILY_LEX:
            if re.search("|".join(pats), t, re.I):
                hit = fam; break
        fams.append(hit)
    df["family"] = fams
    df.loc[df["kind"] != "INSTRUMENT", "family"] = ""

    # ---- recoverability: does any committed CSV of this script carry holdings AND a dial?
    cache = {}
    def probe(script):
        # the Script column is written both bare and with a `research/backtests/` prefix
        stem = os.path.basename(script.strip())
        stem = stem[:-3] if stem.endswith(".py") else stem
        if stem in cache:
            return cache[stem]
        files = sorted(glob.glob(str(OUT / (glob.escape(stem) + "*.csv"))))
        hold = dial = both = False
        for f in files:
            try:
                hdr = [c.strip() for c in open(f).readline().strip().split(",")]
            except Exception:
                continue
            h = any(HOLD_COL.match(c) for c in hdr)
            d = any(DIAL_COL.match(c) for c in hdr)
            hold |= h; dial |= d
            if h and d:
                both = True
                RECOVER_FILES.setdefault(stem, []).append(f)
        r = (len(files), hold, dial, both)
        cache[stem] = r
        return r

    rec = [probe(s) for s in df["script"]]
    df["n_csv"] = [r[0] for r in rec]
    df["has_hold"] = [r[1] for r in rec]
    df["has_dial"] = [r[2] for r in rec]
    df["recoverable"] = [r[3] for r in rec]
    df.loc[df["kind"] != "INSTRUMENT", ["has_hold", "has_dial", "recoverable"]] = False
    return df


# ================================================================ [B] measurement
def build_cells():
    """Every (family, n, dial) cell.  n is degenerate (ALL) for MAB-EWALL."""
    cells = []
    for b in BS:
        cells.append(("MAB-EWALL", 0, b))
    for n in NS:
        for b in BS:
            cells.append(("MAB-TOPN", n, b))
        for x in XS:
            cells.append(("RANKX", n, x))
        for e in ES:
            cells.append(("RANKE", n, e))
    return cells


def selection(px, fam, n, dial, drop_spy):
    if fam == "MAB-EWALL":
        keep = band_state(px, dial) if dial > 0 else (px > px.rolling(200).mean())
        keep = keep & px.notna()
        if drop_spy and "SPY" in px.columns:
            keep = keep.copy(); keep["SPY"] = False
        return keep
    if fam == "MAB-TOPN":
        rk, _ = rank_frame(px, drop_spy, band=dial)
        return sel_hard(rk, n)
    rk, _ = rank_frame(px, drop_spy, band=0.0)
    if fam == "RANKX":
        return sel_buf(px, rk, n, 0, int(dial))
    if fam == "RANKE":
        return sel_buf(px, rk, n, int(dial), 0)
    raise ValueError(fam)


def run_panel(name, px, drop_spy):
    reb = rebalance_mask(px.index, FREQ)
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    b0 = base["returns"].loc[start:]
    bt = base["turnover"].loc[start:]
    out = []
    for fam, n, dial in build_cells():
        sel = selection(px, fam, n, dial, drop_spy)
        w = weights_from(sel)
        r0, t0, nh = fast_backtest(px, w, 0.0)
        r0, t0, nh = r0.loc[start:], t0.loc[start:], nh.loc[start:]
        names = float(nh.mean())
        rec = dict(panel=name, family=fam, n=(n if n else "ALL"), dial=dial,
                   names=names, turnover=float(t0.sum()) / (len(r0) / 252.0))
        for c in COSTS:
            r = r0 - t0 * c / 1e4
            m = metrics(r); h1, h2 = hs(r)
            mo = metrics(r.loc[OOS_START:])
            ok4b, d4b, f4b = bars_4b(r, spy)
            bl = b0 - bt * c / 1e4
            ok4a, d4a, f4a = bars_4a(r, bl)
            # a DEGENERATE cell holds nothing (entry buffer e >= n admits nobody): its Sharpe is
            # NaN and every bar comparison is vacuously true.  It is not a book; it fails both.
            if names <= 0 or not np.isfinite(m["Sharpe"]):
                ok4a, ok4b = False, False
                f4a = f4b = ["DEGENERATE"]
            rec.update({f"CAGR_{c}": m["CAGR"], f"Sharpe_{c}": m["Sharpe"], f"MaxDD_{c}": m["MaxDD"],
                        f"H1_{c}": h1, f"H2_{c}": h2,
                        f"OOS_Sharpe_{c}": mo["Sharpe"], f"OOS_CAGR_{c}": mo["CAGR"],
                        f"OOS_MaxDD_{c}": mo["MaxDD"],
                        f"p4a_{c}": ok4a, f"f4a_{c}": ",".join(f4a),
                        f"p4b_{c}": ok4b, f"f4b_{c}": ",".join(f4b)})
        out.append(rec)
        print(f"    {name:9s} {fam:10s} n={str(n or 'ALL'):>3s} dial={dial:<5g} "
              f"names={names:6.2f} T={rec['turnover']:5.2f}x "
              f"S10={rec['Sharpe_10']:+.3f} 4b@10={rec['p4b_10']}")
    ms = metrics(spy); s1, s2 = hs(spy); mso = metrics(spy.loc[OOS_START:])
    b10 = b0 - bt * 10 / 1e4                 # the live book at PROTOCOL's 10 bps rung
    mb = metrics(b10); b1_, b2_ = hs(b10); mbo = metrics(b10.loc[OOS_START:])
    ctx = dict(panel=name, start=str(start.date()), end=str(px.index[-1].date()),
               spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
               spy_H1=s1, spy_H2=s2, spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
               spy_OOS_MaxDD=mso["MaxDD"],
               v2_10_Sharpe=mb["Sharpe"], v2_10_CAGR=mb["CAGR"], v2_10_MaxDD=mb["MaxDD"],
               v2_10_H1=b1_, v2_10_H2=b2_, v2_10_OOS_Sharpe=mbo["Sharpe"],
               v2_10_OOS_CAGR=mbo["CAGR"], v2_10_OOS_MaxDD=mbo["MaxDD"])
    return out, ctx


# ================================================================ [E] walk-forward
def walkforward(px, name, drop_spy, grid):
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base = backtest(px, rules_v2_weights(px), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    rows = []
    cache = {}
    for fam, n, dial in build_cells():
        key = (fam, n, dial)
        sel = selection(px, fam, n, dial, drop_spy)
        r0, t0, _ = fast_backtest(px, weights_from(sel), 0.0)
        r = (r0 - t0 * 10 / 1e4).loc[start:]
        cache[key] = r
    for fam in ["MAB-EWALL", "MAB-TOPN", "RANKX", "RANKE"]:
        ns = [0] if fam == "MAB-EWALL" else NS
        for n in ns:
            # DEGENERATE cells (all cash, zero variance) are removed from the menu: an ex-ante
            # chooser cannot select a book that holds nothing.
            menu = [k for k in cache if k[0] == fam and k[1] == n
                    and cache[k].std() > 0 and np.isfinite(metrics(cache[k].loc[:IS_END])["Sharpe"])]
            if not menu:
                continue
            pick = max(menu, key=lambda k: metrics(cache[k].loc[:IS_END])["Sharpe"])
            anchor = (fam, n, min(k[2] for k in menu))
            best = max(menu, key=lambda k: metrics(cache[k].loc[OOS_START:])["Sharpe"])
            mo = metrics(cache[pick].loc[OOS_START:])
            ma = metrics(cache[anchor].loc[OOS_START:])
            mb = metrics(cache[best].loc[OOS_START:])
            msp = metrics(spy.loc[OOS_START:]); mv2 = metrics(base.loc[OOS_START:])
            rows.append(dict(panel=name, family=fam, n=(n or "ALL"),
                             pick_dial=pick[2], anchor_dial=anchor[2], best_dial=best[2],
                             IS_Sharpe=metrics(cache[pick].loc[:IS_END])["Sharpe"],
                             OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                             anchor_OOS_Sharpe=ma["Sharpe"], anchor_OOS_CAGR=ma["CAGR"],
                             anchor_OOS_MaxDD=ma["MaxDD"],
                             best_OOS_Sharpe=mb["Sharpe"], regret=mb["Sharpe"] - mo["Sharpe"],
                             spy_OOS_Sharpe=msp["Sharpe"], spy_OOS_CAGR=msp["CAGR"],
                             spy_OOS_MaxDD=msp["MaxDD"],
                             v2_OOS_Sharpe=mv2["Sharpe"], v2_OOS_CAGR=mv2["CAGR"],
                             v2_OOS_MaxDD=mv2["MaxDD"],
                             chooser_beats_anchor=mo["Sharpe"] > ma["Sharpe"]))
    return rows


# ================================================================ gates
def gates(px):
    print("\n[0] reproduction gates")
    rk, _ = rank_frame(px, drop_spy=False, band=0.0)
    w = weights_from(sel_hard(rk, 20))
    eng = backtest(px, w, cost_bps=0, freq=FREQ)
    r0, t0, _ = fast_backtest(px, w, 0.0)
    d1 = float((eng["returns"] - r0).abs().max())
    d2 = float((eng["turnover"] - t0).abs().max())
    print(f"    G1 fast_backtest vs engine.backtest: returns {d1:.3e}, turnover {d2:.3e}")
    assert d1 < 1e-12 and d2 < 1e-12
    eng25 = backtest(px, w, cost_bps=25, freq=FREQ)["returns"]
    d3 = float((eng25 - (r0 - t0 * 25 / 1e4)).abs().max())
    print(f"    G2 derived cost rung r(25) vs backtest(cost_bps=25): {d3:.3e}")
    assert d3 < 1e-12
    a = sel_buf(px, rk, 20, 0, 0); b = sel_hard(rk, 20)
    reb = rebalance_mask(px.index, FREQ)
    dis = int((a.loc[reb] != b.loc[reb]).values.sum())
    print(f"    G3 sel_buf(e=0,x=0) nests the hard top-20 cut: {dis} disagreements "
          f"of {int(reb.sum())*a.shape[1]}")
    assert dis == 0
    d4 = float((band_state(px, 0.0).astype(int) - (px > px.rolling(200).mean()).astype(int))
               .abs().values[200:].max())
    print(f"    G4 band_state(b=0) vs the hard 200d gate: {d4:.3e} (b=0 is the hard gate)")
    if PARENT349.exists():
        p = pd.read_csv(PARENT349)
        sub = p[(p.get("panel") == "U56") & (p.get("e") == 0)]
        if len(sub):
            got = {}
            for x in sorted(set(sub["x"])):
                s = sel_buf(px, rk, 20, 0, int(x))
                rr, tt, _ = fast_backtest(px, weights_from(s), 0.0)
                st = px.index[WARMUP]
                got[x] = metrics((rr - tt * 10 / 1e4).loc[st:])["Sharpe"]
            col = "Sharpe_10" if "Sharpe_10" in sub.columns else None
            if col:
                err = max(abs(got[r["x"]] - r[col]) for _, r in sub.iterrows() if r["x"] in got)
                print(f"    G5 reproduces idea 349's committed U56 e=0 rows on {col}: {err:.3e}")
                assert err < 1e-9
            else:
                print(f"    G5 idea 349 grid has no Sharpe_10 column; cols={list(sub.columns)[:12]}")
    else:
        print("    G5 idea 349 grid CSV not found -- gate skipped")
    p331 = OUT / "2026-09-07_is-CADENCE-the-real-dial-behind-the-band_cloud.grid.csv"
    if p331.exists():
        p = pd.read_csv(p331)
        sub = p[(p["panel"] == "U56") & (p["cadence"] == "W")] if "cadence" in p.columns else \
              p[p["panel"] == "U56"]
        st = px.index[WARMUP]
        errS, errN, k = 0.0, 0.0, 0
        for _, r in sub.iterrows():
            m_ = int(r["m"])
            s = sel_buf(px, rk, 20, 0, m_)
            rr, tt, nn = fast_backtest(px, weights_from(s), 0.0)
            errS = max(errS, abs(metrics((rr - tt * 10 / 1e4).loc[st:])["Sharpe"] - r["Sharpe_10"]))
            errN = max(errN, abs(float(nn.loc[st:].mean()) - r["names"]))
            k += 1
        print(f"    G6 reproduces idea 331's committed weekly U56 rows ({k} m-cells): "
              f"Sharpe_10 {errS:.3e}, names {errN:.3e}")
        assert errS < 1e-9 and errN < 1e-9


# ================================================================ analysis
def analyse(cen, grid, ctx, wf):
    print("\n" + "=" * 100)
    print("[A] CENSUS OF LEADERBOARD.md")
    print("=" * 100)
    tot = len(cen)
    band = cen[cen["is_band"]]
    inst = cen[cen["kind"] == "INSTRUMENT"]
    intv = cen[cen["kind"] == "INTERVAL"]
    print(f"    leaderboard data rows                  {tot}")
    print(f"    match the BAND lexicon                 {len(band)}  ({len(band)/tot:.1%})")
    print(f"      of which INTERVAL (a parameter band) {len(intv)}")
    print(f"      of which INSTRUMENT (a banded rule)  {len(inst)}")
    print(f"    distinct scripts behind INSTRUMENT rows {inst['script'].nunique()}")
    print("\n    -- the queue's literal question: is mean holdings recoverable from a committed CSV?")
    print(f"    INSTRUMENT rows with ANY committed CSV        {(inst['n_csv']>0).sum()} / {len(inst)}")
    print(f"    ... with a holdings-like column somewhere     {inst['has_hold'].sum()}")
    print(f"    ... with a band-dial column somewhere         {inst['has_dial'].sum()}")
    print(f"    ... RECOVERABLE (both, in one CSV)            {inst['recoverable'].sum()}"
          f"  ({inst['recoverable'].mean():.1%})")
    print("\n    INSTRUMENT rows by construction family (textual):")
    fc = inst["family"].replace("", "UNATTRIBUTED").value_counts()
    for k, v in fc.items():
        print(f"      {k:14s} {v:4d}")

    print("\n[A2] the queue's LITERAL recovery, on the rows where the record allows it")
    print("     (mean holdings at the dial-0 parent vs the largest dial, read out of the")
    print("      committed CSV itself -- no re-running)")
    a2 = []
    for stem, files in sorted(RECOVER_FILES.items()):
        for f in files:
            try:
                d = pd.read_csv(f)
            except Exception:
                continue
            hcol = next((c for c in d.columns if HOLD_COL.match(c.strip())), None)
            dcol = next((c for c in d.columns if DIAL_COL.match(c.strip())), None)
            if hcol is None or dcol is None:
                continue
            keys = [c for c in ("panel", "universe", "book", "n", "cadence", "arm") if c in d.columns]
            try:
                d[dcol] = pd.to_numeric(d[dcol]); d[hcol] = pd.to_numeric(d[hcol])
            except Exception:
                continue
            d = d.dropna(subset=[dcol, hcol])
            if not len(d):
                continue
            for key, s in (d.groupby(keys) if keys else [((), d)]):
                s = s[s[hcol] > 0].sort_values(dcol)
                if len(s) < 2 or s[dcol].nunique() < 2:
                    continue
                p0, pt = s.iloc[0], s.iloc[-1]
                a2.append(dict(script=stem[:52], csv=Path(f).name.split(".")[-2], dial=dcol,
                               key="/".join(str(k) for k in (key if isinstance(key, tuple) else (key,))),
                               d0=p0[dcol], names0=p0[hcol], dT=pt[dcol], namesT=pt[hcol],
                               rel=(pt[hcol] - p0[hcol]) / p0[hcol] if p0[hcol] else np.nan))
    A2 = pd.DataFrame(a2)
    if len(A2):
        A2["width_changing"] = A2["rel"].abs() > WIDTH_TOL
        # a `m`/`b` column in a band script's CSV is not necessarily a BAND dial (idea 318's
        # `m` is an explicit WIDTH multiplier, idea 103's a share multiplier).  Split the
        # recovery by whether the SCRIPT NAME itself carries a band cue, and report both.
        A2["script_band_cue"] = A2["script"].str.contains(re.compile("|".join(BAND_LEX), re.I))
        print(A2.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        print(f"\n     recovered ladders: {len(A2)}; width-changing by the same >{WIDTH_TOL:.0%} "
              f"rule: {int(A2['width_changing'].sum())} ({A2['width_changing'].mean():.1%})")
        sub = A2[A2["script_band_cue"]]
        if len(sub):
            print(f"     restricted to ladders in a script whose NAME carries a band cue "
                  f"(so the dial is a band, not a width/share multiplier): {len(sub)} ladders, "
                  f"width-changing {int(sub['width_changing'].sum())} "
                  f"({sub['width_changing'].mean():.1%})")
            byd = sub.groupby("dial")["width_changing"].agg(["size", "sum"])
            for d, r in byd.iterrows():
                print(f"        dial column `{d}`: {int(r['sum'])}/{int(r['size'])} width-changing")
        A2.to_csv(OUT / f"{SLUG}.recovered.csv", index=False)
    else:
        print("     no ladder could be recovered from a committed CSV.")

    print("\n" + "=" * 100)
    print("[B] DIRECT MEASUREMENT -- width effect of each band construction")
    print("=" * 100)
    g = grid.copy()
    g["nkey"] = g["n"].astype(str)
    width_rows = []
    for (fam, nk), sub in g.groupby(["family", "nkey"]):
        for panel, s2 in sub.groupby("panel"):
            s2 = s2.sort_values("dial")
            # a cell with 0 names is DEGENERATE (entry buffer e >= n admits nobody): it is not a
            # book at all, so it is dropped from the width reading rather than scored as -100%.
            live = s2[s2["names"] > 0]
            ndeg = len(s2) - len(live)
            p = live.iloc[0]
            top = live.iloc[-1]
            dn = top["names"] - p["names"]
            const = bool(live["names"].max() - live["names"].min() < 1e-9)
            sp = spearman(live["dial"], live["names"])
            width_rows.append(dict(family=fam, n=nk, panel=panel, degen=ndeg,
                                   parent_names=p["names"], top_dial=top["dial"],
                                   top_names=top["names"],
                                   dNames=dn, rel=dn / p["names"] if p["names"] else np.nan,
                                   spearman=(0.0 if const else sp), names_const=const,
                                   spearman_turnover=spearman(live["dial"], live["turnover"]),
                                   dTurnover=top["turnover"] - p["turnover"]))
    W = pd.DataFrame(width_rows)
    W["width_changing"] = W["rel"].abs() > WIDTH_TOL
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\n    pre-registered rule: WIDTH-CHANGING if |dNames|/parent > {WIDTH_TOL:.0%} "
          f"at the family's largest NON-DEGENERATE dial, on a majority of (panel x n) cells.")
    if W["degen"].sum():
        print(f"    degenerate cells dropped (0 names held -- entry buffer admits nobody): "
              f"{int(W['degen'].sum())}")
    verd = {}
    print("\n    family verdicts:")
    for fam, s in W.groupby("family"):
        frac = s["width_changing"].mean()
        verd[fam] = "WIDTH-CHANGING" if frac > 0.5 else "NEUTRAL"
        print(f"      {fam:11s} width-changing in {int(s['width_changing'].sum())}/{len(s)} cells "
              f"| median |rel| {s['rel'].abs().median():.3f} "
              f"| median spearman(dial,names) {s['spearman'].median():+.3f} "
              f"| median spearman(dial,turnover) {s['spearman_turnover'].median():+.3f} "
              f"-> {verd[fam]}")

    print("\n    the full dNames ladder (mean holdings/day at every dial), panel-pooled mean:")
    lad = g.pivot_table(index=["family", "nkey"], columns="dial", values="names", aggfunc="mean")
    print(lad.to_string(float_format=lambda x: f"{x:.2f}"))

    print("\n" + "=" * 100)
    print("[C] ATTRIBUTION -- how many committed band rows sit on a WIDTH-CHANGING construction?")
    print("=" * 100)
    fam_map = {"RANKE": "RANKE", "RANKX": "RANKX", "RANKM": "RANKX", "MAB": "MAB-TOPN"}
    counts = {"WIDTH-CHANGING": 0, "NEUTRAL": 0, "UNATTRIBUTED": 0}
    detail = []
    for fam, s in inst.groupby(inst["family"].replace("", "UNATTRIBUTED")):
        if fam == "UNATTRIBUTED":
            counts["UNATTRIBUTED"] += len(s); detail.append((fam, "UNATTRIBUTED", len(s))); continue
        meas = fam_map.get(fam)
        # RANKM is idea 331's single dial = the exit buffer under the same cap
        v = verd.get(meas, "UNATTRIBUTED")
        if fam == "MAB":
            # MAB rows split between the EWALL and TOP-N book forms; report the worse case
            v = "WIDTH-CHANGING" if "WIDTH-CHANGING" in (verd.get("MAB-EWALL"), verd.get("MAB-TOPN")) else "NEUTRAL"
        counts[v] = counts.get(v, 0) + len(s)
        detail.append((fam, v, len(s)))
    for fam, v, k in sorted(detail, key=lambda t: -t[2]):
        print(f"      {fam:14s} -> {v:15s} {k:4d} rows")
    ni = len(inst)
    print(f"\n    ROBUSTNESS of the textual call: MAB and RANKM are the two buckets a reader could "
          f"argue about\n    (a leaderboard string like 'BAND12' does not say whether 12 is a "
          f"percentage or a rank).\n    Both measure {verd.get('MAB-TOPN')} / {verd.get('RANKX')} "
          f"in [B], so moving rows between them cannot change the answer;\n    only the RANKE "
          f"bucket can, and its cue ('entry buffer' / 'ENTRY side') is unambiguous.")
    print(f"\n    ANSWER: of {ni} INSTRUMENT band rows in the committed record, "
          f"{counts['WIDTH-CHANGING']} ({counts['WIDTH-CHANGING']/ni:.1%}) sit on a construction "
          f"measured WIDTH-CHANGING,")
    print(f"            {counts['NEUTRAL']} ({counts['NEUTRAL']/ni:.1%}) on a NEUTRAL one, and "
          f"{counts['UNATTRIBUTED']} ({counts['UNATTRIBUTED']/ni:.1%}) cannot be attributed from text.")

    print("\n" + "=" * 100)
    print("[D] KEEP PATHS at every grid point")
    print("=" * 100)
    for c in COSTS:
        print(f"    {c:2d} bps: 4a {int(g[f'p4a_{c}'].sum()):3d}/{len(g)}   "
              f"4b {int(g[f'p4b_{c}'].sum()):3d}/{len(g)}")
    if g["p4b_10"].any():
        print("\n    cells clearing 4b at 10 bps:")
        k = g[g["p4b_10"]][["panel", "family", "n", "dial", "names", "turnover",
                            "CAGR_10", "Sharpe_10", "MaxDD_10", "H1_10", "H2_10", "OOS_Sharpe_10"]]
        print(k.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    else:
        print("    no cell clears 4b at 10 bps.")
    fails = {}
    for _, r in g.iterrows():
        for f in str(r["f4b_10"]).split(","):
            if f:
                fails[f] = fails.get(f, 0) + 1
    print("    4b failing bars at 10 bps (count over all cells): "
          + ", ".join(f"{k} {v}" for k, v in sorted(fails.items(), key=lambda t: -t[1])))

    print("\n" + "=" * 100)
    print("[E] RULE 8 WALK-FORWARD (dial chosen on <=2016 IS Sharpe @10bps; 2017-2026 read once)")
    print("=" * 100)
    cols = ["panel", "family", "n", "pick_dial", "anchor_dial", "best_dial", "IS_Sharpe",
            "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "anchor_OOS_Sharpe", "regret",
            "spy_OOS_Sharpe", "v2_OOS_Sharpe"]
    print(wf[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\n    IS chooser beats its own dial-0 anchor OOS in "
          f"{int(wf['chooser_beats_anchor'].sum())}/{len(wf)} cells; mean regret vs the "
          f"OOS-best dial {wf['regret'].mean():+.4f}")
    print(f"    picks above SPY OOS: {int((wf['OOS_Sharpe'] > wf['spy_OOS_Sharpe']).sum())}/{len(wf)}"
          f"   above RULES v2 OOS: {int((wf['OOS_Sharpe'] > wf['v2_OOS_Sharpe']).sum())}/{len(wf)}")
    print("\n    context (per panel):")
    print(ctx.to_string(float_format=lambda x: f"{x:.3f}"))


def main():
    print(f"=== {SLUG}")
    print(f"Tuned parameters (2): the band dial value, and n in {NS}.")
    print(f"Reported axes: construction family, panel, cost rung {COSTS} bps.")
    print(f"Book: composite (vol scaler OFF), RULES v1 eligibility, NORM weights g/k at "
          f"g={GROSS}, WEEKLY, next-day execution.")

    gcsv = OUT / f"{SLUG}.grid.csv"
    ccsv = OUT / f"{SLUG}.census.csv"
    xcsv = OUT / f"{SLUG}.ctx.csv"
    wcsv = OUT / f"{SLUG}.walkforward.csv"

    print("\n[A] censusing LEADERBOARD.md ...")
    cen = census()
    cen.to_csv(ccsv, index=False)
    print(f"    wrote {ccsv.name} ({len(cen)} rows)")
    print("    BAND lexicon:     " + " | ".join(BAND_LEX))
    print("    INTERVAL lexicon: " + " | ".join(INTERVAL_LEX))

    if RESUME and gcsv.exists() and xcsv.exists() and wcsv.exists():
        analyse(cen, pd.read_csv(gcsv), pd.read_csv(xcsv).set_index("panel"), pd.read_csv(wcsv))
        return

    print("\n[panels]")
    panels = [("U56", load_universe(), False), ("B136", load_universe(broad=True), False),
              ("SMALL439", small_panel(), True)]
    gates(panels[0][1])

    print("\n[B] measuring every cell ...")
    grid, ctxs, wfs = [], [], []
    for nm, px, ds in panels:
        rows, ctx = run_panel(nm, px, ds)
        grid += rows; ctxs.append(ctx)
        wfs += walkforward(px, nm, ds, rows)
    G = pd.DataFrame(grid); G.to_csv(gcsv, index=False)
    X = pd.DataFrame(ctxs).set_index("panel"); X.to_csv(xcsv)
    W = pd.DataFrame(wfs); W.to_csv(wcsv, index=False)
    print(f"    wrote {gcsv.name} ({len(G)} cells), {xcsv.name}, {wcsv.name}")
    analyse(cen, G, X, W)


if __name__ == "__main__":
    main()
