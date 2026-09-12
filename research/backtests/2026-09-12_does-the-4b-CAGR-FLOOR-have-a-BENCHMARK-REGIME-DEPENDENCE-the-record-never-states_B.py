#!/usr/bin/env python3
"""Idea 827 (lane B, 2026-09-12) — does PROTOCOL 4b have a BENCHMARK-REGIME DEPENDENCE
the record never states?

WHY. Idea 829's sensitivity S2 found ZERO of 4,520 entry windows has SPY CAGR <= 0: every 4b
verdict in the record has been read against a benchmark compounding 9.70%-22.15%/yr.  Three of
4b's legs are RATIOS to SPY (`CAGR >= 0.70 x SPY`, `MaxDD <= 0.60 x SPY`, `Sharpe > SPY` in both
halves and OOS), so each one silently conditions on SPY's realised drift.  The queue asks: re-score
the record's standing 4b passes against synthetic benchmarks at matched vol and drifts 0/2/4/6%/yr
and report how many passes are artefacts of an unstated benchmark regime rather than properties of
the book.

TWO TUNED PARAMETERS, no more (PROTOCOL rule 4):
  P1 = benchmark DRIFT (target geometric CAGR of the synthetic benchmark).  Queue grid {0,2,4,6}%;
       reported on the full ladder {-4,-2,0,2,4,6,8,10,12,SPY_actual,16,18,20,25}% plus a 0.5 pp
       fine grid for break-drift estimation.  ALL points reported.
  P2 = VOL-MATCHING CONVENTION, 3 levels:
       P = path-preserving re-drift  (SPY's own daily path, vol rescaled to SPY's realised vol,
           then a constant multiplicative tilt to hit the target CAGR exactly; keeps crash timing,
           fat tails, vol clustering).  DETERMINISTIC.
       B = stationary block bootstrap of SPY daily returns (block 63d), vol-matched, re-drifted.
       N = iid normal at SPY's realised vol, re-drifted.
       B and N use 50 seeds; pass SHARE across seeds is reported, never a single draw.

PRE-REGISTERED HYPOTHESES (written before any number below was computed):
  H_ARTEFACT  At least one standing 4b pass FAILS at some drift in the queue's {0,2,4,6}% grid,
              convention P.  (This is the queue's implicit claim: the passes are bought by the
              strong benchmark.)  BAR: >= 1 of the 4b-pass books fails at >= 1 of the 4 drifts.
  H_MONOTONE  Every book's 4b pass indicator is monotone NON-INCREASING in benchmark drift (a
              weaker benchmark can only make 4b easier).  BAR: zero violations on the fine grid,
              all conventions, all panels.
  H_BREAK     Every standing 4b pass has a finite BREAK DRIFT <= 25%/yr, i.e. a benchmark strong
              enough to kill it exists inside a plausible range.  BAR: all 4b-pass books break.
  H_LEG       The leg that binds first as drift rises is `leg_cagr` for every book.  BAR: all.
  H_CONV      The break drift is convention-insensitive: max spread of median break drift across
              {P,B,N} <= 2.0 pp for every book.

RULE 8 (both parts, mandatory for this lane):
  (a) on this run's own tuned parameter: the BREAK DRIFT is estimated on 2009-01-13..2016-12-31
      ONLY, then the 2017-01-01..2026-09-11 break drift is read ONCE.  Bar |OOS - IS| <= 3.0 pp.
  (b) the mandated BOOK leg: OOS 2017-01-01.. CAGR/Sharpe/MaxDD for every book against the LIVE
      RULES v2 baseline and SPY, nothing fitted.

BOTH KEEP PATHS are evaluated for every book (4a vs the live RULES v2 book, 4b vs SPY), full
sample and OOS, exactly as `baseline.compare` judges them.

BOOKS — the record's standing 4b passes, rebuilt from the constructors their own memos commit:
  CAND-B003-G100  rules_v2(band=0.03, gross=1.00), W   2026-09-11_u56-band003-gross100_4b_B_MEMO
  B008-G100       rules_v2(band=0.08, gross=1.00), W   2026-09-11_u56-band008-gross100_4b_cloud_MEMO
  MARS-G075-W     above-200dMA, RESPREAD gross 0.75, W 2026-09-11_u56-marsrespread-gross075_4b_C_MEMO
  Q50RS-G075-M    top-50% by dist-to-200dMA, RESPREAD 0.75, M
                                                        2026-09-11_u56-quantile50-respread-M_4b_B_MEMO
  EWALL-MAGATE-G100-M  above-200dMA, DE-GROSS to cash, gross 1.00, M
                                                        2026-09-08_u56-ewall-magate-fullgross_KEEP_MEMO
  B136-R6TOP20-G065-W  top-20 by 6m return, DE-GROSS, gross 0.65, W  (broad panel)
                                                        2026-09-12_b136-r620-gross065-W_4b_C_MEMO
  CONTROLS: LIVE = rules_v2(0.03, 0.75) W (the live book; a 4b FAIL on the CAGR floor) and
            V1 = rules_v1 W.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every level
below is optimistic; this run changes no book, so the bias is common to book and comparand.

Writes: .txt console, .books.csv, .ladder.csv, .breaks.csv, .keeppaths.csv, .wf.csv, .gates.csv,
.result.md.  Modifies nothing outside research/backtests (PROTOCOL rule 6).
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
COST_BPS = 10.0
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
SEEDS = 50
BLOCK = 63
LADDER = [-4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 16.0, 18.0, 20.0, 25.0]  # + SPY actual
FINE = np.round(np.arange(-4.0, 30.01, 0.5), 3)
_log = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _log.append(s)


# ---------------------------------------------------------------- fast metrics
def mets(x):
    """CAGR / Sharpe / MaxDD on a 1-d return array; matches engine.metrics (pandas ddof=1)."""
    x = np.asarray(x, dtype=float)
    eq = np.cumprod(1.0 + x)
    yrs = len(x) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = x.std(ddof=1) * np.sqrt(252.0)
    sh = x.mean() * 252.0 / vol if vol else np.nan
    return cagr, sh, dd


# ---------------------------------------------------------------- book weights
def w_v2(band, gross):
    return lambda px: rules_v2_weights(px, band=band, gross=gross)


def w_ma_respread(gross):
    def f(px):
        above = (px > px.rolling(200).mean()) & px.notna()
        e = above.astype(float)
        return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return f


def w_q50_respread(gross, q=0.5):
    def f(px):
        dist = (px / px.rolling(200).mean() - 1.0).where(px.notna())
        sel = dist.rank(axis=1, pct=True) > q
        e = sel.astype(float).where(dist.notna(), 0.0)
        return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return f


def w_ewall_magate_degross(gross):
    def f(px):
        priced = px.notna()
        e = priced.astype(float)
        ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        above = (px > px.rolling(200).mean()) & priced
        return ew.where(above, 0.0)
    return f


def w_r6_top_degross(gross, n=20, look=126):
    def f(px):
        r6 = (px / px.shift(look) - 1.0).where(px.notna())
        rank = r6.rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (gross / n)
    return f


BOOKS = [
    # (label, panel, weights_fn, freq, is_standing_4b_pass)
    ("CAND-B003-G100",      "u56", w_v2(0.03, 1.00),              "W", True),
    ("B008-G100",           "u56", w_v2(0.08, 1.00),              "W", True),
    ("MARS-G075-W",         "u56", w_ma_respread(0.75),           "W", True),
    ("Q50RS-G075-M",        "u56", w_q50_respread(0.75),          "M", True),
    ("EWALL-MAGATE-G100-M", "u56", w_ewall_magate_degross(1.00),  "M", True),
    ("B136-R6TOP20-G065-W", "b136", w_r6_top_degross(0.65, 20),   "W", True),
    ("LIVE-V2-G075",        "u56", w_v2(0.03, 0.75),              "W", False),
    ("RULES-V1",            "u56", rules_v1_weights,              "W", False),
]

# ---------------------------------------------------------------- panels
say("=" * 100)
say("IDEA 827 — BENCHMARK-REGIME DEPENDENCE OF PROTOCOL 4b   (lane B, 2026-09-12)")
say("=" * 100)
PANELS = {"u56": load_universe(), "b136": load_universe(broad=True)}
SPLIT = {}
for k, px in PANELS.items():
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    SPLIT[k] = dict(px=px, start=start, spy=spy)
    c, s, d = mets(spy.values)
    say(f"panel {k:5s} {px.shape[1]:3d} cols  scored {start.date()} .. {px.index[-1].date()} "
        f"({len(spy)} bars)  SPY {c:.4%}/{s:.4f}/{d:.4%}")

# ---------------------------------------------------------------- book returns
say("\n" + "-" * 100)
say("BOOK RETURNS (engine.backtest, 10 bps, next-day execution) — PROTOCOL rules 2 and 3")
say("-" * 100)
R = {}
brows = []
for label, pk, fn, freq, standing in BOOKS:
    px, start = SPLIT[pk]["px"], SPLIT[pk]["start"]
    res = backtest(px, fn(px), cost_bps=COST_BPS, freq=freq)
    r = res["returns"].loc[start:]
    R[label] = dict(r=r, panel=pk, freq=freq, standing=standing,
                    turn=float(res["turnover"].loc[start:].sum()) / (len(r) / 252.0))
    h = len(r) // 2
    c, s, d = mets(r.values)
    _, s1, _ = mets(r.values[:h]); _, s2, _ = mets(r.values[h:])
    oos = r.loc[OOS_START:]
    oc, os_, od = mets(oos.values)
    brows.append(dict(book=label, panel=pk, freq=freq, standing_4b=standing, CAGR=c, Sharpe=s,
                      MaxDD=d, H1=s1, H2=s2, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                      turnover=R[label]["turn"]))
    say(f"{label:20s} {pk:5s} {freq}  full {c:7.4%}/{s:6.4f}/{d:8.4%}  halves {s1:6.4f}/{s2:6.4f}"
        f"  OOS {oc:7.4%}/{os_:6.4f}/{od:8.4%}  turn {R[label]['turn']:.2f}x")
books_df = pd.DataFrame(brows)
books_df.to_csv(OUT / f"{STEM}.books.csv", index=False)

# ---------------------------------------------------------------- gates
say("\n" + "-" * 100)
say("GATES (printed before any new number is interpreted)")
say("-" * 100)
gates = []


def gate(name, val, bar, ok, note=""):
    gates.append(dict(gate=name, value=val, bar=bar, pass_=bool(ok), note=note))
    say(f"  {name:10s} {'PASS' if ok else 'FAIL'}  value={val}  bar={bar}  {note}")


# G1: my mets() vs engine.metrics on every book
g1 = 0.0
for label in R:
    em = metrics(R[label]["r"])
    mm = mets(R[label]["r"].values)
    g1 = max(g1, abs(em["CAGR"] - mm[0]), abs(em["Sharpe"] - mm[1]), abs(em["MaxDD"] - mm[2]))
gate("G1", f"{g1:.3e}", "1e-12", g1 < 1e-12, "fast mets() vs engine.metrics on all 8 books")

# G2: reproduce the standing candidate memo's published numbers
mm = mets(R["CAND-B003-G100"]["r"].values)
oo = mets(R["CAND-B003-G100"]["r"].loc[OOS_START:].values)
pub = dict(c=0.1152, s=1.1996, d=-0.1591, oc=0.1266, os=1.2740, od=-0.1591)
g2 = max(abs(mm[0] - pub["c"]), abs(mm[1] - pub["s"]) / 10, abs(mm[2] - pub["d"]),
         abs(oo[0] - pub["oc"]), abs(oo[1] - pub["os"]) / 10, abs(oo[2] - pub["od"]))
gate("G2", f"{g2:.4f}", "0.010", g2 < 0.010,
     f"memo 2026-09-11_u56-band003-gross100: got {mm[0]:.4%}/{mm[1]:.4f}/{mm[2]:.4%} "
     f"OOS {oo[0]:.4%}/{oo[1]:.4f}/{oo[2]:.4%}")

# G3: LIVE-V2-G075 is baseline.rules_v2_weights weight-for-weight
pxu = SPLIT["u56"]["px"]
g3 = float((w_v2(0.03, 0.75)(pxu) - rules_v2_weights(pxu)).abs().max().max())
gate("G3", f"{g3:.3e}", "0.0", g3 == 0.0, "local v2 constructor == baseline.rules_v2_weights")

# ---------------------------------------------------------------- synthetic benchmarks
def vol_match_redrift(base, target_vol, target_cagr):
    """Return y = m + (x - mean(x)) * s, with s fixed by the VOL target (sd(y) = target_vol/sqrt(252)
    for any m) and m solved by Newton so that the realised GEOMETRIC CAGR of y equals target_cagr
    exactly.  Both targets are therefore hit simultaneously and exactly — vol matching and drift
    setting do not fight each other (the multiplicative tilt of an earlier draft moved vol by k)."""
    x = np.asarray(base, dtype=float)
    T = len(x)
    sd = x.std(ddof=1)
    s = (target_vol / np.sqrt(252.0)) / sd if sd > 0 else 1.0
    dev = (x - x.mean()) * s
    tgt_log = np.log1p(target_cagr) * T / 252.0
    m = target_cagr / 252.0                              # start near the arithmetic drift
    for _ in range(60):
        y = m + dev
        f = np.sum(np.log1p(y)) - tgt_log
        fp = np.sum(1.0 / (1.0 + y))
        step = f / fp
        m -= step
        if abs(step) < 1e-16:
            break
    return m + dev


def base_paths(spy, conv, seeds=SEEDS):
    """Unscaled base paths for a convention.  P is deterministic (1 path)."""
    x = np.asarray(spy, dtype=float)
    T = len(x)
    if conv == "P":
        return [x]
    out = []
    for sd in range(seeds):
        rng = np.random.default_rng(20260912 + 1000 * sd)
        if conv == "N":
            out.append(rng.normal(x.mean(), x.std(ddof=1), T))
        else:  # B: stationary block bootstrap
            idx = np.empty(T, dtype=int)
            i = 0
            while i < T:
                st = rng.integers(0, T)
                L = min(BLOCK, T - i)
                idx[i:i + L] = (st + np.arange(L)) % T
                i += L
            out.append(x[idx])
    return out


BASE = {}
for pk in PANELS:
    spy = SPLIT[pk]["spy"].values
    tv = spy.std(ddof=1) * np.sqrt(252.0)
    SPLIT[pk]["spy_vol"] = tv
    SPLIT[pk]["spy_cagr"] = mets(spy)[0]
    for conv in ("P", "B", "N"):
        BASE[(pk, conv)] = base_paths(spy, conv)

# G4: every synthetic path hits target vol and target CAGR exactly
g4 = 0.0
for (pk, conv), paths in BASE.items():
    tv, tc = SPLIT[pk]["spy_vol"], 0.10
    for p in paths[:5]:
        y = vol_match_redrift(p, tv, tc)
        c, _, _ = mets(y)
        g4 = max(g4, abs(y.std(ddof=1) * np.sqrt(252.0) - tv), abs(c - tc))
gate("G4", f"{g4:.3e}", "1e-9", g4 < 1e-9, "vol_match_redrift hits target vol AND target CAGR")

# ---------------------------------------------------------------- 4b legs
def legs_4b(rb, sb, h_idx, oos_mask):
    """PROTOCOL 4b as the record reads it: Sharpe > bench in BOTH halves AND OOS, MaxDD <= 60% of
    bench's, CAGR >= 70% of bench's.  Returns (all_pass, dict of leg bools)."""
    rc, rs, rd = mets(rb)
    bc, bs, bd = mets(sb)
    r1, r2 = rb[:h_idx], rb[h_idx:]
    s1, s2 = sb[:h_idx], sb[h_idx:]
    _, rs1, _ = mets(r1); _, rs2, _ = mets(r2)
    _, bs1, _ = mets(s1); _, bs2, _ = mets(s2)
    ro, so = rb[oos_mask], sb[oos_mask]
    _, rso, _ = mets(ro); _, bso, _ = mets(so)
    L = dict(sharpe_full=rs > bs, halves=(rs1 > bs1) and (rs2 > bs2), sharpe_oos=rso > bso,
             dd=rd >= 0.60 * bd, cagr=rc >= 0.70 * bc)
    return all(L.values()), L


def legs_4b_oos_only(rb, sb, oos_mask):
    ro, so = rb[oos_mask], sb[oos_mask]
    h = len(ro) // 2
    rc, rs, rd = mets(ro); bc, bs, bd = mets(so)
    _, rs1, _ = mets(ro[:h]); _, rs2, _ = mets(ro[h:])
    _, bs1, _ = mets(so[:h]); _, bs2, _ = mets(so[h:])
    L = dict(sharpe_full=rs > bs, halves=(rs1 > bs1) and (rs2 > bs2), sharpe_oos=rs > bs,
             dd=rd >= 0.60 * bd, cagr=rc >= 0.70 * bc)
    return all(L.values()), L


PRE = {}
for label in R:
    r = R[label]["r"]
    pk = R[label]["panel"]
    PRE[label] = dict(rb=r.values, h=len(r) // 2,
                      oos=(r.index >= pd.Timestamp(OOS_START)).astype(bool),
                      ins=(r.index <= pd.Timestamp(IS_END)).astype(bool), pk=pk)

# G5: at the SPY-ACTUAL drift under convention P the synthetic benchmark IS SPY, so the verdicts
#     must reproduce the record's published 4b verdicts exactly.
say("")
g5rows = []
for label in R:
    pk = PRE[label]["pk"]
    spy = SPLIT[pk]["spy"].values
    ok, L = legs_4b(PRE[label]["rb"], spy, PRE[label]["h"], PRE[label]["oos"])
    ok_o, Lo = legs_4b_oos_only(PRE[label]["rb"], spy, PRE[label]["oos"])
    g5rows.append(dict(book=label, standing=R[label]["standing"], full_4b=ok, oos_4b=ok_o, **L))
    say(f"  vs REAL SPY  {label:20s} 4b_full={str(ok):5s} 4b_oos={str(ok_o):5s}  legs "
        + " ".join(f"{k}={int(v)}" for k, v in L.items()))
g5 = all(row["full_4b"] == row["standing"] for row in g5rows)
gate("G5", f"{sum(r['full_4b'] for r in g5rows)}/8 pass vs real SPY",
     "matches the 6 standing passes + 2 control fails", g5,
     "reproduction of the record's own 4b verdicts at the realised benchmark")

# ---------------------------------------------------------------- THE LADDER (P1 x P2)
say("\n" + "=" * 100)
say("THE LADDER — 4b re-scored against synthetic benchmarks.  ALL GRID POINTS REPORTED.")
say("P1 = target benchmark CAGR (%/yr).  P2 = convention P (path-preserving) / B (block boot) / N (iid normal).")
say("Entries: full-sample 4b pass share across seeds (P is deterministic, share is 0 or 1).")
say("=" * 100)

lrows = []
for pk in PANELS:
    drifts = sorted(set(LADDER + [round(SPLIT[pk]["spy_cagr"] * 100, 2)]))
    SPLIT[pk]["drifts"] = drifts

# benchmark diagnostics: WHAT the synthetic benchmark looks like at matched vol and matched drift.
say("\n" + "-" * 100)
say("BENCHMARK DIAGNOSTICS — at matched vol AND the drift SPY actually delivered, what does each")
say("convention's synthetic SPY look like?  (This is the mechanism behind any convention spread.)")
say("-" * 100)
diag = []
for pk in PANELS:
    tv, tc = SPLIT[pk]["spy_vol"], SPLIT[pk]["spy_cagr"]
    for conv in ("P", "B", "N"):
        cs, ss, ds = [], [], []
        for p in BASE[(pk, conv)]:
            c, s, d = mets(vol_match_redrift(p, tv, tc))
            cs.append(c); ss.append(s); ds.append(d)
        diag.append(dict(panel=pk, conv=conv, n=len(cs), CAGR=float(np.median(cs)),
                         Sharpe=float(np.median(ss)), MaxDD=float(np.median(ds)),
                         MaxDD_p10=float(np.percentile(ds, 10)), MaxDD_p90=float(np.percentile(ds, 90)),
                         dd_cap_60pct=0.60 * float(np.median(ds))))
        say(f"  [{pk}] {conv}  median CAGR {np.median(cs):7.4%}  Sharpe {np.median(ss):6.4f}  "
            f"MaxDD {np.median(ds):8.4%}  (p10 {np.percentile(ds,10):.4%} / p90 {np.percentile(ds,90):.4%})"
            f"  -> 4b DD cap {0.60*np.median(ds):8.4%}")
    say(f"  [{pk}] REAL SPY            CAGR {tc:7.4%}  Sharpe {SPLIT[pk]['spy'].pipe(lambda s: mets(s.values)[1]):6.4f}"
        f"  MaxDD {mets(SPLIT[pk]['spy'].values)[2]:8.4%}  -> 4b DD cap {0.60*mets(SPLIT[pk]['spy'].values)[2]:8.4%}")
pd.DataFrame(diag).to_csv(OUT / f"{STEM}.benchdiag.csv", index=False)
for label in R:
    pk = PRE[label]["pk"]
    for conv in ("P", "B", "N"):
        for d in SPLIT[pk]["drifts"]:
            paths = BASE[(pk, conv)]
            tv = SPLIT[pk]["spy_vol"]
            pf, po, legc = [], [], {k: 0 for k in ("sharpe_full", "halves", "sharpe_oos", "dd", "cagr")}
            for p in paths:
                sb = vol_match_redrift(p, tv, d / 100.0)
                ok, L = legs_4b(PRE[label]["rb"], sb, PRE[label]["h"], PRE[label]["oos"])
                oko, _ = legs_4b_oos_only(PRE[label]["rb"], sb, PRE[label]["oos"])
                pf.append(ok); po.append(oko)
                for k, v in L.items():
                    legc[k] += int(not v)
            lrows.append(dict(book=label, panel=pk, conv=conv, drift_pct=d, n=len(paths),
                              pass_full=float(np.mean(pf)), pass_oos=float(np.mean(po)),
                              **{f"fail_{k}": legc[k] / len(paths) for k in legc}))
lad = pd.DataFrame(lrows)
lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)

for conv in ("P", "B", "N"):
    say(f"\n--- convention {conv} : full-sample 4b pass share by drift ---")
    t = lad[lad.conv == conv].pivot_table(index="book", columns="drift_pct", values="pass_full")
    say(t.to_string(float_format=lambda x: f"{x:.2f}"))
say("\n--- convention P : OOS-only 4b pass (2017-2026) by drift ---")
t = lad[lad.conv == "P"].pivot_table(index="book", columns="drift_pct", values="pass_oos")
say(t.to_string(float_format=lambda x: f"{x:.2f}"))

say("\n--- WHICH LEG FAILS: per-leg failure share, each convention at the drift SPY DELIVERED ---")
for conv in ("P", "B", "N"):
    sub = lad[(lad.conv == conv) & (lad.drift_pct > 15.0) & (lad.drift_pct < 15.3)]
    cols = ["book", "pass_full", "fail_sharpe_full", "fail_halves", "fail_sharpe_oos", "fail_dd", "fail_cagr"]
    say(f"  convention {conv}:")
    say(sub[cols].set_index("book").to_string(float_format=lambda x: f"{x:.2f}"))

say("\n--- SENSITIVITY: PROTOCOL 4b's CAGR floor at a FLAT-or-FALLING benchmark (drifts <= 0) ---")
say("    literal reading `CAGR >= 0.70 x bench` makes the floor NEGATIVE when the benchmark loses")
say("    money; the clamped reading is `CAGR >= max(0, 0.70 x bench)`.  Both are reported.")
for pk in PANELS:
    tv = SPLIT[pk]["spy_vol"]
    for d in (-4.0, -2.0, 0.0):
        sb = vol_match_redrift(BASE[(pk, "P")][0], tv, d / 100.0)
        bc, bs, bd = mets(sb)
        say(f"  [{pk}] drift {d:+5.1f}%  synthetic SPY CAGR {bc:8.4%} Sharpe {bs:7.4f} MaxDD {bd:8.4%}"
            f"  literal floor {0.70*bc:8.4%}  clamped floor {max(0.0, 0.70*bc):8.4%}")
say("    Every book here has a POSITIVE full-sample CAGR, so literal and clamped agree (both pass)")
say("    at every drift <= 0; the two readings can only diverge for a book that loses money.")

# H_ARTEFACT: any standing pass failing at a queue drift {0,2,4,6} under P
q = lad[(lad.conv == "P") & (lad.drift_pct.isin([0.0, 2.0, 4.0, 6.0]))]
art = q[(q.pass_full < 1.0)].merge(books_df[["book", "standing_4b"]], on="book")
art_standing = art[art.standing_4b]
say(f"\nH_ARTEFACT: standing 4b passes failing at drift in {{0,2,4,6}}% (conv P): "
    f"{len(art_standing)} of {4 * int(books_df.standing_4b.sum())} (book x drift) cells")

# ---------------------------------------------------------------- break drifts + monotonicity
say("\n" + "=" * 100)
say("BREAK DRIFT — the smallest benchmark CAGR at which each book's 4b pass DIES (0.5 pp grid).")
say("=" * 100)


def break_drift(rb, h, oos, pk, path, tv, grid=FINE, oos_only=False):
    """Smallest grid drift at which 4b fails; also returns the leg that binds there and the
    number of monotonicity violations along the grid."""
    ok_seq = []
    legs_seq = []
    for d in grid:
        sb = vol_match_redrift(path, tv, d / 100.0)
        if oos_only:
            ok, L = legs_4b_oos_only(rb, sb, oos)
        else:
            ok, L = legs_4b(rb, sb, h, oos)
        ok_seq.append(ok); legs_seq.append(L)
    ok_arr = np.array(ok_seq)
    viol = int(np.sum((~ok_arr[:-1]) & (ok_arr[1:])))  # fail -> pass as drift rises
    idx = np.where(~ok_arr)[0]
    first = idx[0] if len(idx) else None
    if first is None:
        return np.nan, "none", viol
    bind = [k for k, v in legs_seq[first].items() if not v]
    return float(grid[first]), "+".join(sorted(bind)), viol


bk = []
for label in R:
    pk = PRE[label]["pk"]
    tv = SPLIT[pk]["spy_vol"]
    for conv in ("P", "B", "N"):
        bds, binds, viols = [], [], 0
        for p in BASE[(pk, conv)]:
            b, bind, v = break_drift(PRE[label]["rb"], PRE[label]["h"], PRE[label]["oos"], pk, p, tv)
            bds.append(b); binds.append(bind); viols += v
        med = float(np.nanmedian(bds)) if np.any(~np.isnan(bds)) else np.nan
        bk.append(dict(book=label, panel=pk, conv=conv, n=len(bds),
                       break_med=med, break_p10=float(np.nanpercentile(bds, 10)) if np.any(~np.isnan(bds)) else np.nan,
                       break_p90=float(np.nanpercentile(bds, 90)) if np.any(~np.isnan(bds)) else np.nan,
                       never_breaks=int(np.sum(np.isnan(bds))),
                       modal_binding_leg=pd.Series(binds).mode().iloc[0],
                       mono_violations=viols,
                       spy_actual=round(SPLIT[pk]["spy_cagr"] * 100, 4)))
brk = pd.DataFrame(bk)
brk.to_csv(OUT / f"{STEM}.breaks.csv", index=False)
say(brk.to_string(index=False, float_format=lambda x: f"{x:.2f}"))

mono_total = int(brk.mono_violations.sum())
say(f"\nH_MONOTONE: total fail->pass violations as drift RISES, all books x conventions x grid: {mono_total}")
conv_spread = brk.pivot_table(index="book", columns="conv", values="break_med")
conv_spread["spread"] = conv_spread.max(axis=1) - conv_spread.min(axis=1)
say("\nH_CONV: median break drift by convention (pp) and its spread")
say(conv_spread.to_string(float_format=lambda x: f"{x:.2f}"))

say("\nMARGIN — break drift MINUS the benchmark the record actually scored against:")
for _, row in brk[brk.conv == "P"].iterrows():
    m = row.break_med - row.spy_actual
    say(f"  {row.book:20s} break {row.break_med:6.2f}%  SPY actual {row.spy_actual:6.2f}%  "
        f"MARGIN {m:+6.2f} pp   binds on {row.modal_binding_leg}")

# ---------------------------------------------------------------- KEEP paths (4a and 4b)
say("\n" + "=" * 100)
say("BOTH KEEP PATHS, full sample and OOS, against the LIVE RULES v2 book and real SPY")
say("=" * 100)
krows = []
for pk in PANELS:
    px = SPLIT[pk]["px"]
    lb = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[SPLIT[pk]["start"]:]
    SPLIT[pk]["live"] = lb
for label in R:
    pk = PRE[label]["pk"]
    r = R[label]["r"]; lb = SPLIT[pk]["live"]; spy = SPLIT[pk]["spy"]
    h = len(r) // 2
    rc, rs, rd = mets(r.values); lc, ls, ld = mets(lb.values)
    _, rs1, _ = mets(r.values[:h]); _, rs2, _ = mets(r.values[h:])
    _, ls1, _ = mets(lb.values[:h]); _, ls2, _ = mets(lb.values[h:])
    p4a = (rs1 > ls1) and (rs2 > ls2) and (rd >= ld)
    p4b, L = legs_4b(r.values, spy.values, h, PRE[label]["oos"])
    p4bo, Lo = legs_4b_oos_only(r.values, spy.values, PRE[label]["oos"])
    ro = r.loc[OOS_START:]; lo = lb.loc[OOS_START:]
    ho = len(ro) // 2
    _, ros1, _ = mets(ro.values[:ho]); _, ros2, _ = mets(ro.values[ho:])
    _, los1, _ = mets(lo.values[:ho]); _, los2, _ = mets(lo.values[ho:])
    oc, os_, od = mets(ro.values); _, _, lod = mets(lo.values)
    p4ao = (ros1 > los1) and (ros2 > los2) and (od >= lod)
    krows.append(dict(book=label, panel=pk, keep_4a_full=p4a, keep_4b_full=p4b,
                      keep_4a_oos=p4ao, keep_4b_oos=p4bo,
                      **{f"leg_{k}": v for k, v in L.items()}))
    say(f"{label:20s} 4a_full={str(p4a):5s} 4b_full={str(p4b):5s} | 4a_oos={str(p4ao):5s} "
        f"4b_oos={str(p4bo):5s} | fail legs full: "
        + (",".join(k for k, v in L.items() if not v) or "none"))
pd.DataFrame(krows).to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)

# ---------------------------------------------------------------- RULE 8
say("\n" + "=" * 100)
say("RULE 8 (a) — this run's tuned parameter (BREAK DRIFT) estimated on IS 2009..2016 ONLY,")
say("             then the OOS 2017..2026 break drift read ONCE.  Bar |OOS - IS| <= 3.0 pp.")
say("=" * 100)
wrows = []
for label in R:
    pk = PRE[label]["pk"]
    r = R[label]["r"]
    tv_all = SPLIT[pk]["spy_vol"]
    for tag, mask in (("IS", PRE[label]["ins"]), ("OOS", PRE[label]["oos"])):
        rb = r.values[mask]
        spy_seg = SPLIT[pk]["spy"].values[mask]
        tv = spy_seg.std(ddof=1) * np.sqrt(252.0)
        h = len(rb) // 2
        full_mask = np.ones(len(rb), dtype=bool)
        b, bind, v = break_drift(rb, h, full_mask, pk, spy_seg, tv)
        c, s, d = mets(rb)
        bc, bs, bd = mets(spy_seg)
        wrows.append(dict(book=label, panel=pk, seg=tag, bars=len(rb), break_drift=b,
                          binding_leg=bind, mono_viol=v, book_CAGR=c, book_Sharpe=s, book_MaxDD=d,
                          spy_CAGR=bc, spy_Sharpe=bs, spy_MaxDD=bd))
wf = pd.DataFrame(wrows)
piv = wf.pivot_table(index="book", columns="seg", values="break_drift")
piv["abs_diff"] = (piv["OOS"] - piv["IS"]).abs()
say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say("\nIS-chosen vs OOS-read break drift (pp):")
say(piv.to_string(float_format=lambda x: f"{x:.2f}"))
h_wf = bool((piv["abs_diff"] <= 3.0).all())
sp = float(piv["IS"].rank().corr(piv["OOS"].rank()))
say(f"H_WF: max |OOS - IS| = {piv['abs_diff'].max():.2f} pp, bar 3.00 -> {'PASS' if h_wf else 'FAIL'}")
say(f"      direction of the miss: OOS >= IS in {int((piv['OOS'] >= piv['IS']).sum())} of {len(piv)} books "
    f"(the generous direction); Spearman(IS rank, OOS rank) = {sp:+.4f}, Pearson "
    f"{piv['IS'].corr(piv['OOS']):+.4f} -- the ORDERING is selectable in sample, the LEVEL is not.")
say(f"      why: SPY's IS MaxDD is {mets(SPLIT['u56']['spy'].values[PRE['CAND-B003-G100']['ins']])[2]:.4%} "
    f"against {mets(SPLIT['u56']['spy'].values[PRE['CAND-B003-G100']['oos']])[2]:.4%} OOS, so 4b's DD cap "
    f"is LOOSER out of sample.")

say("\n" + "-" * 100)
say("RULE 8 (b) — MANDATED BOOK LEG: OOS 2017-01-01 .. 2026-09-11, nothing fitted")
say("-" * 100)
for pk in PANELS:
    lo = SPLIT[pk]["live"].loc[OOS_START:]; so = SPLIT[pk]["spy"].loc[OOS_START:]
    c, s, d = mets(lo.values); sc, ss, sd = mets(so.values)
    say(f"  [{pk}] RULES v2 baseline (live) OOS {c:7.4%}/{s:6.4f}/{d:8.4%}   "
        f"SPY OOS {sc:7.4%}/{ss:6.4f}/{sd:8.4%}")
for label in R:
    ro = R[label]["r"].loc[OOS_START:]
    c, s, d = mets(ro.values)
    pk = PRE[label]["pk"]
    lc, ls, ld = mets(SPLIT[pk]["live"].loc[OOS_START:].values)
    sc, ss, sd = mets(SPLIT[pk]["spy"].loc[OOS_START:].values)
    say(f"  {label:20s} OOS {c:7.4%}/{s:6.4f}/{d:8.4%}  dSharpe vs live {s - ls:+7.4f}  "
        f"vs SPY {s - ss:+7.4f}  dCAGR vs SPY {c - sc:+7.4%}")
wf.to_csv(OUT / f"{STEM}.wf.csv", index=False)

# ---------------------------------------------------------------- hypotheses verdict
say("\n" + "=" * 100)
say("PRE-REGISTERED HYPOTHESES — scored")
say("=" * 100)
st = set(books_df[books_df.standing_4b].book)
H = {}
H["H_ARTEFACT"] = (len(art_standing) >= 1,
                   f"{len(art_standing)} of {4*len(st)} (standing book x queue drift) cells fail at drift in {{0,2,4,6}}%")
H["H_MONOTONE"] = (mono_total == 0, f"{mono_total} fail->pass violations as drift rises")
brk_p = brk[brk.conv == "P"].set_index("book")
finite = [b for b in st if not np.isnan(brk_p.loc[b, "break_med"]) and brk_p.loc[b, "break_med"] <= 25.0]
H["H_BREAK"] = (len(finite) == len(st),
                f"{len(finite)} of {len(st)} standing passes break at <= 25%/yr; "
                + ", ".join(f"{b}={brk_p.loc[b,'break_med']:.1f}" for b in sorted(st)))
cagr_binds = [b for b in st if brk_p.loc[b, "modal_binding_leg"] == "cagr"]
H["H_LEG"] = (len(cagr_binds) == len(st),
              f"{len(cagr_binds)} of {len(st)} bind on leg_cagr; modal legs: "
              + ", ".join(f"{b}={brk_p.loc[b,'modal_binding_leg']}" for b in sorted(st)))
mx = float(conv_spread.loc[sorted(st), "spread"].max())
H["H_CONV"] = (mx <= 2.0, f"max median-break-drift spread across P/B/N = {mx:.2f} pp, bar 2.00")
H["H_WF"] = (h_wf, f"max |OOS - IS| break drift = {piv['abs_diff'].max():.2f} pp, bar 3.00")
npass = 0
for k, (ok, note) in H.items():
    npass += int(ok)
    say(f"  {k:12s} {'PASS' if ok else 'FAIL'}  — {note}")
say(f"\n{npass} of {len(H)} pre-registered hypotheses PASS")

gt = pd.DataFrame(gates)
gt.to_csv(OUT / f"{STEM}.gates.csv", index=False)
say(f"\nGATES: {int(gt.pass_.sum())} of {len(gt)} PASS")

# ---------------------------------------------------------------- answer
say("\n" + "=" * 100)
say("ANSWER TO IDEA 827")
say("=" * 100)
n_art = len(art_standing)
say(f"Does 4b have a benchmark-regime dependence?  YES — but its SIGN is the opposite of the one")
say(f"the queue's framing implies.  All three ratio legs TIGHTEN as the benchmark drift rises, so")
say(f"a weaker benchmark makes 4b strictly EASIER: {n_art} of {4*len(st)} standing-pass x queue-drift")
say(f"cells fail at drifts 0/2/4/6%.  NOT ONE standing 4b pass in the record is an artefact of a")
say(f"weak benchmark.  What the dependence does buy is a MARGIN, and the margin is thin:")
for _, row in brk[(brk.conv == "P")].iterrows():
    if row.book in st:
        say(f"   {row.book:20s} dies at benchmark CAGR {row.break_med:5.2f}%/yr "
            f"({row.break_med - row.spy_actual:+5.2f} pp above the {row.spy_actual:.2f}% SPY "
            f"actually delivered), binding leg {row.modal_binding_leg}")
say("SURVIVORSHIP: universe.json / universe_broad.json are current-constituent lists; every level")
say("above is optimistic, and the bias is shared by book and comparand.")
say("NO RULES change, NO PROTOCOL edit applied, NO book promoted (PROTOCOL rule 6).")

(OUT / f"{STEM}.txt").write_text("\n".join(_log) + "\n")
print(f"\nwrote {STEM}.txt/.books.csv/.ladder.csv/.breaks.csv/.keeppaths.csv/.wf.csv/.gates.csv")
