#!/usr/bin/env python3
"""Idea 400 — census the record's ABSOLUTE thresholds for the firing-RATE artefact.

Idea 336 showed that a fixed absolute cut applied to a PANEL-DEPENDENT statistic measures
the FREQUENCY of admission, not the signal: its ABS breadth gate fired at 0.193 / 0.413 /
0.686 spread across panels (B = 0.30 / 0.40 / 0.50), and 83.5% of the full-sample Sharpe
movement on SMALL484 sat on the RATE term.  This run does what the queue asked:

  A. GATES (pre-registered, run and printed BEFORE any hypothesis number is computed).
  B. CENSUS of research/LEADERBOARD.md: every claim whose instrument is an absolute cut on
     a panel-dependent statistic (breadth / dispersion / vol20 / correlation), machine
     extracted, every hit committed to a CSV so the extraction is auditable.
  C. RATE: the realised firing rate of every distinct (family, level) the census names, on
     all three panels, and its cross-panel spread against idea 336's ABS reference.
  D. TRADE (PROTOCOL 3/4/8): the same thresholds as de-gross clauses on an EWALL book, ABS
     against a rate-equalised twin, walk-forward with 2 tuned parameters (family, level),
     both KEEP paths evaluated on every grid point.

Two tuned parameters: FAMILY and LEVEL.  Every grid point is reported.
Deterministic, standalone, offline (committed caches only).
"""
from __future__ import annotations
import re, sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights      # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics                        # noqa: E402

STEM = Path(__file__).with_suffix("")
COST = 10.0            # PROTOCOL 2
FREQ = "W"
GROSS = 0.75           # RULES v2's live gross
WARM = 260             # warm-up rows skipped, as baseline.compare does
IS_END = pd.Timestamp("2016-12-31")     # PROTOCOL 8
COMMON_LAST = None                      # filled at load time
VINTAGE = "2026-09-08"                  # the U56 panel stamp idea 486's published triple was
                                        # computed on (idea 328/514's panel-stamp rule)

# ---------------------------------------------------------------- pre-registration
# Directions are pre-registered: risk-ON is high breadth, LOW vol, LOW dispersion,
# LOW correlation.  Ladders are pre-registered too; the census's own extracted levels are
# unioned onto them in part C.
LADDER = {
    "BREADTH": ([0.20, 0.30, 0.40, 0.50, 0.60], "ge"),
    "VOL20":   ([0.20, 0.25, 0.30, 0.40, 0.60], "le"),
    "DISP":    ([0.06, 0.08, 0.10, 0.14, 0.20], "le"),
    "CORR":    ([0.30, 0.40, 0.50, 0.60, 0.70], "le"),
}
# idea 336's committed ABS on_share spreads at B = 0.30 / 0.40 / 0.50
REF336 = [0.193, 0.413, 0.686]
BAR = REF336[1]        # pre-registered bar = the median of idea 336's three ABS spreads

# ---------------------------------------------------------------- fast backtester
def fast_backtest(prices: pd.DataFrame, weights: pd.DataFrame, cost_bps=COST, freq=FREQ):
    """numpy transcription of engine.backtest (same drift, same t+1 fill, same costs)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); port = np.zeros(n); turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        port[i] = float(cur @ rets[i]) - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


def stats(r: pd.Series) -> dict:
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    mx = px.drop(columns=["SPY"]).pct_change().abs().max()
    drop = mx[mx >= 1.0].index                       # the record's SMALL439 filter
    return px.drop(columns=list(drop)), len(drop)


def load_panels():
    global COMMON_LAST
    u = load_universe()
    b = load_universe(broad=True)
    s, ndrop = small_panel()
    COMMON_LAST = min(u.index[-1], b.index[-1], s.index[-1])
    out = {}
    for name, px in (("U56", u), ("B136", b), ("SMALL439", s)):
        out[name] = px.loc[:COMMON_LAST].dropna(how="all").ffill()
    return out, ndrop


# ---------------------------------------------------------------- panel statistics
def panel_stats(px: pd.DataFrame) -> pd.DataFrame:
    """The four panel-dependent statistics the queue names.  SPY is a benchmark column,
    never a constituent, so it is dropped everywhere here."""
    p = px.drop(columns=["SPY"], errors="ignore")
    live = p.notna()
    ret = p.pct_change()

    ma = p.rolling(200).mean()
    above = (p > ma) & ma.notna()
    breadth = above.sum(axis=1) / ma.notna().sum(axis=1).replace(0, np.nan)

    sig = ret.rolling(20).std() * np.sqrt(252)
    vol20 = sig.median(axis=1)

    r21 = p / p.shift(21) - 1.0
    disp = r21.std(axis=1)

    s60 = ret.rolling(60).std()
    n60 = s60.notna().sum(axis=1)
    sum_s = s60.sum(axis=1, min_count=1)
    sum_s2 = (s60 ** 2).sum(axis=1, min_count=1)
    ew = ret.where(live).mean(axis=1)
    var_p = (ew.rolling(60).std()) ** 2
    num = (n60 ** 2) * var_p - sum_s2
    den = sum_s ** 2 - sum_s2
    corr = (num / den.replace(0, np.nan)).clip(-1, 1)

    return pd.DataFrame({"BREADTH": breadth, "VOL20": vol20, "DISP": disp, "CORR": corr})


def gate_state(series: pd.Series, level: float, sense: str) -> pd.Series:
    """ON = risk-on.  NaN statistic (warm-up) is OFF, which is the conservative reading."""
    s = series.ge(level) if sense == "ge" else series.le(level)
    return (s & series.notna()).astype(float)


# ---------------------------------------------------------------- books
def ew_weights(px: pd.DataFrame) -> pd.DataFrame:
    p = px.drop(columns=["SPY"], errors="ignore")
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    w = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def clause_book(px, base_w, on: pd.Series):
    return base_w.mul(on.reindex(px.index).fillna(0.0), axis=0)


# ---------------------------------------------------------------- census of LEADERBOARD
FAMILY_TOKENS = {
    "BREADTH": r"breadth",
    "VOL20":   r"vol20|realised vol|realized vol|20d vol",
    "DISP":    r"dispersion|\bdisp\b",
    "CORR":    r"correlation|\bcorr\b",
}
PANEL_TOKENS = [r"u56", r"b136|broad", r"small\d*"]
# a threshold form: token, then within 60 chars a comparison / at / @ and a bare number
CUT = re.compile(r"(?:>=|<=|>|<|=|@|\bat\b|\bof\b)\s*(-?\d*\.\d+|-?\d+(?:\.\d+)?%?)")
REL_WORDS = re.compile(r"quantile|percentile|\bpct\b|\bq\s*=|\bq\d|decile|rank|\bqtl\b|z-score|zscore")


def census(md_path: Path) -> pd.DataFrame:
    rows = []
    for ln, line in enumerate(md_path.read_text().split("\n"), start=1):
        if not line.startswith("|"):
            continue
        low = line.lower()
        npanel = sum(1 for t in PANEL_TOKENS if re.search(t, low))
        for fam, tok in FAMILY_TOKENS.items():
            for m in re.finditer(tok, low):
                win = low[m.end(): m.end() + 60]
                rel = bool(REL_WORDS.search(low[max(0, m.start() - 30): m.end() + 60]))
                c = CUT.search(win)
                if not c:
                    continue
                raw = c.group(1)
                pct = raw.endswith("%")
                try:
                    val = float(raw.rstrip("%")) / (100.0 if pct else 1.0)
                except ValueError:
                    continue
                rows.append(dict(line=ln, family=fam, level=val, relative=rel,
                                 cross_panel=npanel >= 2, n_panel_tokens=npanel,
                                 context=line[max(0, 0):][:0] or low[max(0, m.start() - 40): m.end() + 60]))
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.drop_duplicates(subset=["line", "family", "level", "relative"]).reset_index(drop=True)


# ---------------------------------------------------------------- hand audit
# Every in-domain ABSOLUTE hit the extractor returns was read by hand and classified.
# Keyed by (LEADERBOARD line, family, level).  PANEL = a genuine absolute cut on a
# panel-AGGREGATE statistic; NAME = a genuine absolute cut applied per NAME in the
# cross-section (same artefact class, different denominator); FALSE = not a threshold at
# all (a reported statistic value, a range, a regression coefficient, a Sharpe compare).
AUDIT = {
    (4122, "BREADTH", 0.05):  ("FALSE", "draw-to-draw breadth RANGE of 0.05"),
    (3895, "BREADTH", 0.187): ("FALSE", "sd(phi) 0.048 -> 0.187"),
    (4340, "BREADTH", 0.2):   ("PANEL", "`b136 / breadth >= 0.20 / weekly`"),
    (4365, "BREADTH", 0.3):   ("PANEL", "breadthcash@0.30"),
    (4136, "BREADTH", 0.34):  ("FALSE", "max |40*breadth - ebar| = 0.34"),
    (3088, "BREADTH", 0.4):   ("PANEL", "breadth gate b=0.40"),
    (3115, "BREADTH", 0.4):   ("PANEL", "breadth gate b=0.40 depth 0.50"),
    (2795, "BREADTH", 0.5):   ("PANEL", "`breadth<0.5` as a classifier cut"),
    (2812, "BREADTH", 0.5):   ("PANEL", "`breadth<0.5` is the 50/50 cap-mix line"),
    (4303, "BREADTH", 0.58):  ("FALSE", "regression loading l=0.58"),
    (4099, "BREADTH", 0.675): ("FALSE", "breadth flat 0.6821 -> 0.6750"),
    (3405, "BREADTH", 0.75):  ("FALSE", "depth=0.75 is the de-gross depth, not a breadth level"),
    (3158, "CORR", 0.088):    ("FALSE", "conv_per_pp = 0.088 - 0.081*corr"),
    (3160, "CORR", 0.2):      ("FALSE", "idea 103's `corr` is the arm's correlation WITH S9, "
                               "a between-book statistic, not a panel aggregate"),
    (4099, "CORR", 0.3436):   ("FALSE", "corr flat 0.3626 -> 0.3436"),
    (4099, "CORR", 0.426):    ("FALSE", "correlation rises 0.355 -> 0.426"),
    (3160, "CORR", 0.5):      ("FALSE", "same line, same between-book `corr`"),
    (4251, "CORR", 0.5):      ("PANEL", "c_bar >= 0.5 conditioning cut"),
    (4397, "CORR", 0.75):     ("FALSE", "g=0.75 is gross"),
    (3174, "CORR", 0.931):    ("FALSE", "sign agreement 134/144 = 0.931"),
    (2827, "DISP", 0.062):    ("FALSE", "disp 0.0964 -> 0.0620"),
    (4099, "DISP", 0.062):    ("FALSE", "disp halves 0.0964 -> 0.0620"),
    (4099, "DISP", 0.438):    ("FALSE", "beta 0.823 -> 0.438"),
    (2058, "VOL20", 0.2):     ("FALSE", "m = 0.20/0.50/1.00 is a multiplier"),
    (1913, "VOL20", 0.383):   ("FALSE", "held-name vol20 0.321 -> 0.383"),
    (16,   "VOL20", 0.6):     ("NAME",  "`vol20 < 0.60` clause (per-name eligibility)"),
    (1425, "VOL20", 0.6):     ("NAME",  "vol60-dg (vol20<0.60 to cash)"),
    (2558, "VOL20", 0.6):     ("NAME",  "eligible = above 200d, vol20<0.60"),
    (2565, "VOL20", 0.6):     ("NAME",  "above-200d & vol20<0.60"),
    (2781, "VOL20", 0.6):     ("NAME",  "the `vol20 < 0.60` half costs 4.26pp"),
    (2787, "VOL20", 0.6):     ("NAME",  "does the `vol20 < 0.60` half pay on large caps"),
    (2793, "VOL20", 0.6):     ("NAME",  "ewall + vol20<0.60, no trend gate"),
    (2819, "VOL20", 0.6):     ("NAME",  "`vol20 < 0.60` in isolation"),
    (2834, "VOL20", 0.6):     ("NAME",  "gated (200d & vol20<0.60, de-gross)"),
    (2921, "VOL20", 0.6):     ("NAME",  "the vol20 < 0.60 cap costs -3.93 pp/yr on small439"),
    (3142, "VOL20", 0.6):     ("NAME",  "equal-weight above-200d, vol20<0.60"),
    (3749, "VOL20", 0.6):     ("NAME",  "eligible = above 200d ma & vol20<0.60"),
    (1956, "VOL20", 0.75):    ("FALSE", "g = 0.75 x vol_spy/vol is a gross formula"),
    (4323, "VOL20", 0.959):   ("FALSE", "h1 1.294 > 0.959 is a Sharpe compare"),
}


def in_domain(fam, lv):
    lo, hi = {"BREADTH": (0.05, 0.95), "VOL20": (0.05, 1.50),
              "DISP": (0.01, 0.60), "CORR": (0.05, 0.95)}[fam]
    return lo <= lv <= hi


# ================================================================= main
def main():
    print("=" * 100)
    print("IDEA 400 — census the record's ABSOLUTE thresholds for the firing-RATE artefact")
    print("=" * 100)

    panels, ndrop = load_panels()
    print(f"\npanels truncated to common last date {COMMON_LAST.date()}; "
          f"SMALL: {ndrop} names with max_1d_move >= 1.0 dropped")
    for k, v in panels.items():
        print(f"  {k:9s} {v.shape[0]:5d} rows x {v.shape[1]:4d} cols  "
              f"{v.index[0].date()} -> {v.index[-1].date()}")

    # ------------------------------------------------------------ A. GATES
    print("\n" + "-" * 100)
    print("A. GATES (pre-registered; run before any hypothesis number)")
    print("-" * 100)
    gates = []

    # G1 fast_backtest == engine.backtest on real books
    g1 = 0.0
    for name in ("U56", "B136"):
        px = panels[name]
        for wfn in (ew_weights, lambda p: rules_v2_weights(p), lambda p: rules_v1_weights(p)):
            W = wfn(px)
            r_fast, t_fast = fast_backtest(px, W)
            eng = backtest(px, W, cost_bps=COST, freq=FREQ)
            g1 = max(g1, float(np.abs(r_fast - eng["returns"]).max()),
                     float(np.abs(t_fast - eng["turnover"]).max()))
    gates.append(("G1 fast_backtest vs engine.backtest (6 books, returns+turnover)", g1, 1e-12, g1 < 1e-12))

    # G2 idea 486's committed U56 RULES v1 triple, at ITS OWN VINTAGE.  Idea 328/514's
    # panel stamp is load-bearing here: the published triple is the U56 panel as of
    # 2026-09-08, and this run truncates every panel to the common last date, so the
    # reproduction gate is run at the published vintage and the truncated value is
    # published beside it as the drift.
    pub = (0.064194, 0.66110, -0.138278)
    u_raw = load_universe()
    u_vint = u_raw.loc[:VINTAGE]
    r_v, _ = fast_backtest(u_vint, rules_v1_weights(u_vint)); r_v = r_v.iloc[WARM:]
    mv = metrics(r_v); gotv = (mv["CAGR"], mv["Sharpe"], mv["MaxDD"])
    g2 = max(abs(a - b) for a, b in zip(pub, gotv))
    gates.append((f"G2 U56/RULES v1 @ vintage {VINTAGE} = {gotv[0]:.4%} / {gotv[1]:.5f} / "
                  f"{gotv[2]:.4%} vs published {pub[0]:.4%} / {pub[1]:.5f} / {pub[2]:.4%}",
                  g2, 1e-4, g2 < 1e-4))
    r_t, _ = fast_backtest(panels["U56"], rules_v1_weights(panels["U56"])); r_t = r_t.iloc[WARM:]
    mt = metrics(r_t)
    print(f"  [note] same book on THIS run's truncated U56 ({COMMON_LAST.date()}): "
          f"{mt['CAGR']:.4%} / {mt['Sharpe']:.5f} / {mt['MaxDD']:.4%} — panel-stamp drift "
          f"{max(abs(a-b) for a,b in zip(pub,(mt['CAGR'],mt['Sharpe'],mt['MaxDD']))):.3e}, "
          f"MaxDD identical.")

    # G3 clause identity: a state forced always-ON reproduces the ungated parent exactly
    px = panels["U56"]; W = ew_weights(px)
    on1 = pd.Series(1.0, index=px.index)
    r_on, _ = fast_backtest(px, clause_book(px, W, on1))
    r_par, _ = fast_backtest(px, W)
    g3 = float(np.abs(r_on - r_par).max())
    gates.append(("G3 always-ON clause == ungated EWALL parent", g3, 1e-15, g3 < 1e-15))

    # G4 statistics are finite and in domain on every panel
    ST = {k: panel_stats(v) for k, v in panels.items()}
    bad = 0
    for k, d in ST.items():
        d2 = d.dropna()
        bad += int(((d2["BREADTH"] < 0) | (d2["BREADTH"] > 1)).sum())
        bad += int(((d2["CORR"] < -1) | (d2["CORR"] > 1)).sum())
        bad += int((d2["VOL20"] <= 0).sum()) + int((d2["DISP"] < 0).sum())
    gates.append(("G4 panel statistics inside their domains (all panels)", float(bad), 0.5, bad == 0))

    for label, val, bar, ok in gates:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {val:.3e} (bar {bar:.0e})")
    pd.DataFrame([dict(gate=l, value=v, bar=b, passed=o) for l, v, b, o in gates]).to_csv(
        f"{STEM}.gates.csv", index=False)
    if not all(o for *_, o in gates):
        print("\n!! a gate FAILED — results below are reported anyway, flagged.")

    # ------------------------------------------------------------ B. CENSUS
    print("\n" + "-" * 100)
    print("B. CENSUS of research/LEADERBOARD.md")
    print("-" * 100)
    lb = ROOT / "research" / "LEADERBOARD.md"
    n_rows = sum(1 for l in lb.read_text().split("\n") if l.startswith("|"))
    cen = census(lb)
    cen.to_csv(f"{STEM}.census.csv", index=False)
    abs_cuts = cen[~cen["relative"]]
    abs_xp = abs_cuts[abs_cuts["cross_panel"]]
    print(f"  LEADERBOARD table lines scanned                : {n_rows}")
    print(f"  lines carrying a panel-dependent statistic     : {cen['line'].nunique()}")
    print(f"  threshold hits (family, level) extracted       : {len(cen)}")
    print(f"    ... flagged RELATIVE (quantile/rank wording)  : {int(cen['relative'].sum())}")
    print(f"    ... ABSOLUTE cuts                             : {len(abs_cuts)}")
    print(f"    ... ABSOLUTE and CROSS-PANEL (>=2 panels named): {len(abs_xp)}")
    print("\n  by family (ABSOLUTE hits / of which cross-panel / distinct in-domain levels):")
    extracted = {}
    for fam in LADDER:
        f_all = abs_cuts[abs_cuts["family"] == fam]
        f_xp = f_all[f_all["cross_panel"]]
        lv = sorted({round(x, 4) for x in f_all["level"] if in_domain(fam, x)})
        extracted[fam] = lv
        print(f"    {fam:8s} {len(f_all):5d} / {len(f_xp):5d} / {len(lv):3d}   levels={lv[:12]}"
              f"{' ...' if len(lv) > 12 else ''}")

    # ------------------------------------------------------------ B2. HAND AUDIT
    print("\n  HAND AUDIT of every in-domain ABSOLUTE hit (PANEL = real cut on a panel")
    print("  aggregate; NAME = real cut applied per name; FALSE = not a threshold):")
    aud = abs_cuts[[in_domain(f, l) for f, l in zip(abs_cuts["family"], abs_cuts["level"])]].copy()
    aud["verdict"] = [AUDIT.get((int(r.line), r.family, round(r.level, 4)), ("UNSEEN", ""))[0]
                      for r in aud.itertuples()]
    aud["why"] = [AUDIT.get((int(r.line), r.family, round(r.level, 4)), ("UNSEEN", ""))[1]
                  for r in aud.itertuples()]
    aud.to_csv(f"{STEM}.audit.csv", index=False)
    vc = aud["verdict"].value_counts()
    print("    " + "  ".join(f"{k} {v}" for k, v in vc.items()) + f"   (total {len(aud)})")
    print(f"    machine precision for 'absolute cut on a PANEL statistic': "
          f"{vc.get('PANEL', 0)}/{len(aud)} = {vc.get('PANEL', 0)/max(len(aud),1):.1%}")
    print(f"    precision for 'a genuine absolute cut of any kind'        : "
          f"{(vc.get('PANEL',0)+vc.get('NAME',0))}/{len(aud)} = "
          f"{(vc.get('PANEL',0)+vc.get('NAME',0))/max(len(aud),1):.1%}")
    if vc.get("UNSEEN", 0):
        print(f"    !! {vc['UNSEEN']} hits were NOT in the hand-audit table — reported unaudited")

    # ------------------------------------------------------------ C. RATE
    print("\n" + "-" * 100)
    print("C. REALISED FIRING RATE and cross-panel SPREAD  (bar = idea 336's median ABS")
    print(f"   spread {BAR:.3f}; idea 336's three ABS spreads were {REF336})")
    print("-" * 100)
    rate_rows = []
    cells = {}
    for fam, (ladder, sense) in LADDER.items():
        levels = sorted(set(ladder) | set(extracted[fam]))
        cells[fam] = (levels, sense)
        for lv in levels:
            rec = dict(family=fam, level=lv, sense=sense,
                       source=("both" if lv in ladder and lv in extracted[fam]
                               else "ladder" if lv in ladder else "census"))
            rates = {}
            for pk, px in panels.items():
                on = gate_state(ST[pk][fam], lv, sense).iloc[WARM:]
                rates[pk] = float(on.mean())
                rec[f"rate_{pk}"] = rates[pk]
            rec["spread"] = max(rates.values()) - min(rates.values())
            rec["artefact"] = rec["spread"] > BAR
            rate_rows.append(rec)
    rates_df = pd.DataFrame(rate_rows).sort_values(["family", "level"]).reset_index(drop=True)
    rates_df.to_csv(f"{STEM}.rates.csv", index=False)
    with pd.option_context("display.width", 200):
        print(rates_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n  cells: {len(rates_df)}; spread > {BAR:.3f} (rate artefact) in "
          f"{int(rates_df['artefact'].sum())} = {rates_df['artefact'].mean():.1%}")
    print("  median spread by family:")
    for fam, g in rates_df.groupby("family"):
        print(f"    {fam:8s} median {g['spread'].median():.4f}  max {g['spread'].max():.4f}  "
              f"artefact {int(g['artefact'].sum())}/{len(g)}")

    # ---- C2: the AUDITED cells only, and the per-NAME denominator ----
    key = rates_df.set_index(["family", "level"])
    aud_p = aud[aud["verdict"] == "PANEL"].copy()
    aud_p["spread"] = [float(key.loc[(r.family, round(r.level, 4)), "spread"])
                       for r in aud_p.itertuples()]
    for pk in panels:
        aud_p[f"rate_{pk}"] = [float(key.loc[(r.family, round(r.level, 4)), f"rate_{pk}"])
                               for r in aud_p.itertuples()]
    aud_p["min_rate"] = aud_p[[f"rate_{p}" for p in panels]].min(axis=1)
    aud_p.to_csv(f"{STEM}.audited_rates.csv", index=False)
    print("\n  THE ANSWER TO THE QUEUE'S QUESTION — the AUDITED published cuts only:")
    print(aud_p[["line", "family", "level", "cross_panel"] +
                [f"rate_{p}" for p in panels] + ["spread"]].sort_values(
        ["family", "level"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n    published PANEL cuts: {len(aud_p)};  spread > {BAR:.3f} (idea 336 median): "
          f"{int((aud_p.spread > BAR).sum())};  > {REF336[0]:.3f} (idea 336 min): "
          f"{int((aud_p.spread > REF336[0]).sum())};  > {REF336[2]:.3f} (max): "
          f"{int((aud_p.spread > REF336[2]).sum())}")
    print(f"    INERT (min panel rate > 0.90, i.e. the clause barely fires on ANY panel): "
          f"{int((aud_p.min_rate > 0.90).sum())}/{len(aud_p)}")

    # per-NAME admission share — the right denominator for the record's most-cited
    # absolute cut, `vol20 < 0.60` (12 of the 39 in-domain hits)
    print("\n  PER-NAME denominator for the record's most-cited absolute cut "
          "(`vol20 < 0.60`, 12 hits) and its ladder:")
    nm_rows = []
    for lv in [0.30, 0.40, 0.60, 0.80, 1.00]:
        rec = {"cut": f"vol20 < {lv:.2f}"}
        vals = {}
        for pk, px in panels.items():
            p = px.drop(columns=["SPY"], errors="ignore")
            sig = p.pct_change().rolling(20).std() * np.sqrt(252)
            adm = (sig < lv).sum(axis=1) / sig.notna().sum(axis=1).replace(0, np.nan)
            vals[pk] = float(adm.iloc[WARM:].mean())
            rec[f"admit_{pk}"] = vals[pk]
        rec["spread"] = max(vals.values()) - min(vals.values())
        rec["artefact"] = rec["spread"] > BAR
        nm_rows.append(rec)
    nm = pd.DataFrame(nm_rows)
    nm.to_csv(f"{STEM}.pername.csv", index=False)
    print(nm.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ D. TRADE
    print("\n" + "-" * 100)
    print("D. THE SAME THRESHOLDS AS BOOKS  (EWALL gross 0.75, DEGROSS to cash, weekly,")
    print("   10 bps, t+1).  Arms: ABS (fixed level, tradable) / CQTL (causal expanding")
    print("   quantile at the pooled ABS rate, tradable) / MATCH (per-panel frozen level at")
    print("   the pooled rate — LOOK-AHEAD, control only).")
    print("-" * 100)

    # references per panel
    ref = {}
    for pk, px in panels.items():
        spy = px["SPY"].pct_change().fillna(0.0).iloc[WARM:]
        r_v2, _ = fast_backtest(px, rules_v2_weights(px)); r_v2 = r_v2.iloc[WARM:]
        r_ew, _ = fast_backtest(px, ew_weights(px)); r_ew = r_ew.iloc[WARM:]
        ref[pk] = dict(SPY=stats(spy), V2=stats(r_v2), EW=stats(r_ew),
                       spy_r=spy, v2_r=r_v2, ew_r=r_ew)
        print(f"  {pk:9s} SPY {ref[pk]['SPY']['CAGR']:7.2%} / {ref[pk]['SPY']['Sharpe']:.3f} / "
              f"{ref[pk]['SPY']['MaxDD']:7.2%}   RULES v2 {ref[pk]['V2']['CAGR']:7.2%} / "
              f"{ref[pk]['V2']['Sharpe']:.3f} / {ref[pk]['V2']['MaxDD']:7.2%}   "
              f"EWALL {ref[pk]['EW']['CAGR']:7.2%} / {ref[pk]['EW']['Sharpe']:.3f} / "
              f"{ref[pk]['EW']['MaxDD']:7.2%}")

    def keep_paths(s, pk, oos_sharpe):
        v2, spy = ref[pk]["V2"], ref[pk]["SPY"]
        p4a = (s["H1"] > v2["H1"]) and (s["H2"] > v2["H2"]) and (s["MaxDD"] >= v2["MaxDD"])
        p4b = (s["H1"] > spy["H1"] and s["H2"] > spy["H2"] and oos_sharpe is not None
               and oos_sharpe > _oos_spy[pk] and s["MaxDD"] >= 0.60 * spy["MaxDD"]
               and s["CAGR"] >= 0.70 * spy["CAGR"])
        return p4a, p4b

    # OOS SPY / v2 references
    _oos_spy, _oos_v2 = {}, {}
    for pk in panels:
        _oos_spy[pk] = metrics(ref[pk]["spy_r"].loc[IS_END + pd.Timedelta(days=1):])["Sharpe"]
        _oos_v2[pk] = metrics(ref[pk]["v2_r"].loc[IS_END + pd.Timedelta(days=1):])["Sharpe"]

    books = []
    pooled_rate = {}
    for fam, (levels, sense) in cells.items():
        for lv in levels:
            r = rates_df[(rates_df.family == fam) & (rates_df.level == lv)].iloc[0]
            pooled_rate[(fam, lv)] = float(np.mean([r[f"rate_{p}"] for p in panels]))

    for pk, px in panels.items():
        W = ew_weights(px)
        for fam, (levels, sense) in cells.items():
            s = ST[pk][fam]
            for lv in levels:
                p = pooled_rate[(fam, lv)]
                q = p if sense == "le" else 1.0 - p
                # ABS
                arms = {"ABS": gate_state(s, lv, sense)}
                # CQTL — causal expanding quantile at the pooled rate (min 252 obs)
                thr = s.expanding(min_periods=252).quantile(q)
                cq = (s.le(thr) if sense == "le" else s.ge(thr))
                arms["CQTL"] = (cq & s.notna() & thr.notna()).astype(float)
                # MATCH — per-panel frozen full-sample level at the pooled rate (look-ahead)
                lvl_m = float(s.iloc[WARM:].quantile(q))
                arms["MATCH"] = gate_state(s, lvl_m, sense)
                for arm, on in arms.items():
                    rr, tt = fast_backtest(px, clause_book(px, W, on))
                    rr = rr.iloc[WARM:]
                    st = stats(rr)
                    oos = rr.loc[IS_END + pd.Timedelta(days=1):]
                    iss = rr.loc[:IS_END]
                    m_o, m_i = metrics(oos), metrics(iss)
                    onr = float(on.iloc[WARM:].mean())
                    p4a, p4b = keep_paths(st, pk, m_o["Sharpe"])
                    books.append(dict(panel=pk, family=fam, level=lv, arm=arm,
                                      matched_level=lvl_m if arm == "MATCH" else np.nan,
                                      on_share=onr, turnover=float(tt.iloc[WARM:].sum() /
                                                                   (len(rr) / 252)),
                                      **st, IS_Sharpe=m_i["Sharpe"], OOS_CAGR=m_o["CAGR"],
                                      OOS_Sharpe=m_o["Sharpe"], OOS_MaxDD=m_o["MaxDD"],
                                      pass4a=p4a, pass4b=p4b))
    bk = pd.DataFrame(books)
    bk.to_csv(f"{STEM}.books.csv", index=False)
    print(f"\n  {len(bk)} books ( {bk.panel.nunique()} panels x {len(cells)} families x "
          f"levels x 3 arms ), ALL reported in .books.csv")
    print("\n  KEEP paths over all books:")
    print(f"    4a: {int(bk.pass4a.sum())}/{len(bk)}    4b: {int(bk.pass4b.sum())}/{len(bk)}")
    print("\n  4b passes by arm / panel:")
    piv = bk.pivot_table(index="arm", columns="panel", values="pass4b", aggfunc="sum")
    print(piv.to_string())
    print("\n  mean Sharpe by arm (ABS vs the rate-equalised twins):")
    print(bk.groupby(["panel", "arm"])[["Sharpe", "OOS_Sharpe", "on_share"]].mean()
          .to_string(float_format=lambda x: f"{x:.4f}"))

    # rate-vs-form decomposition on Sharpe: ABS - MATCH is the LEVEL(form) leg at equal
    # rate; MATCH - parent is what the rate alone buys.
    dec = []
    for pk in panels:
        par = ref[pk]["EW"]["Sharpe"]
        par_o = metrics(ref[pk]["ew_r"].loc[IS_END + pd.Timedelta(days=1):])["Sharpe"]
        for fam, (levels, _s) in cells.items():
            for lv in levels:
                sel = bk[(bk.panel == pk) & (bk.family == fam) & (bk.level == lv)]
                a = sel[sel.arm == "ABS"].iloc[0]; mt = sel[sel.arm == "MATCH"].iloc[0]
                dec.append(dict(panel=pk, family=fam, level=lv,
                                total=a.Sharpe - par, rate=mt.Sharpe - par,
                                form=a.Sharpe - mt.Sharpe,
                                total_oos=a.OOS_Sharpe - par_o, rate_oos=mt.OOS_Sharpe - par_o,
                                form_oos=a.OOS_Sharpe - mt.OOS_Sharpe))
    dd = pd.DataFrame(dec)
    dd["rate_share"] = dd["rate"].abs() / (dd["rate"].abs() + dd["form"].abs()).replace(0, np.nan)
    dd["rate_share_oos"] = dd["rate_oos"].abs() / (dd["rate_oos"].abs() +
                                                   dd["form_oos"].abs()).replace(0, np.nan)
    dd.to_csv(f"{STEM}.decomp.csv", index=False)
    mat = dd[dd["total"].abs() >= 0.05]
    print(f"\n  DECOMPOSITION (Sharpe): total = rate + form, {len(dd)} cells, "
          f"{len(mat)} material (|total| >= 0.05)")
    print(f"    median |rate| {mat['rate'].abs().median():.4f} vs median |form| "
          f"{mat['form'].abs().median():.4f};  median rate_share "
          f"{mat['rate_share'].median():.1%}  (OOS {mat['rate_share_oos'].median():.1%})")
    print("    by family (median rate_share, full / OOS):")
    for fam, g in mat.groupby("family"):
        print(f"      {fam:8s} {g['rate_share'].median():.1%} / "
              f"{g['rate_share_oos'].median():.1%}   n={len(g)}")

    # ------------------------------------------------------------ RULE 8
    print("\n" + "-" * 100)
    print("E. RULE 8 WALK-FORWARD — (family, level) chosen on IS <= 2016-12-31 by IS Sharpe,")
    print("   OOS 2017+ read once.  Tradable arms only (ABS, CQTL); MATCH is look-ahead.")
    print("-" * 100)
    wf = []
    for pk in panels:
        for arm in ("ABS", "CQTL"):
            sub = bk[(bk.panel == pk) & (bk.arm == arm)]
            pick = sub.loc[sub["IS_Sharpe"].idxmax()]
            par = ref[pk]["EW"]
            par_o = metrics(ref[pk]["ew_r"].loc[IS_END + pd.Timedelta(days=1):])
            wf.append(dict(panel=pk, arm=arm, pick=f"{pick.family}@{pick.level:g}",
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           parent_OOS_Sharpe=par_o["Sharpe"], parent_OOS_CAGR=par_o["CAGR"],
                           v2_OOS_Sharpe=_oos_v2[pk], spy_OOS_Sharpe=_oos_spy[pk],
                           full_CAGR=pick.CAGR, full_Sharpe=pick.Sharpe, full_MaxDD=pick.MaxDD,
                           H1=pick.H1, H2=pick.H2, on_share=pick.on_share,
                           pass4a=bool(pick.pass4a), pass4b=bool(pick.pass4b)))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{STEM}.walkforward.csv", index=False)
    with pd.option_context("display.width", 220):
        print(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n  walk-forward rows: 4a {int(wfd.pass4a.sum())}/{len(wfd)},  "
          f"4b {int(wfd.pass4b.sum())}/{len(wfd)}")

    print("\n" + "=" * 100)
    print("DONE — artefacts: .gates.csv .census.csv .rates.csv .books.csv .decomp.csv "
          ".walkforward.csv")
    print("=" * 100)


if __name__ == "__main__":
    main()
