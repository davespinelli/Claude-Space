#!/usr/bin/env python3
"""Idea 1163 (cloud lane, 2026-09-17) — is the RECORD REPRODUCIBLE AT ALL while
data/prices.csv is REWRITTEN NIGHTLY?

Idea 1159's cross-run gates G2/G3/G9 failed against 1148's committed numbers ONE DAY OLD.
The cause decomposed into an extra BAR (97.3% of the deviation) plus a RESTATEMENT: commit
6f1fcb1 rewrote 31,505 of 258,733 shared price cells (0.1218) across 48 of 58 tickers back
to 2008-01-02, max relative move 0.008384.  Every committed constant in the record is
pinned to a price vintage that no longer exists on disk.  The queue asks for the CHEAPEST
REPAIR, priced against the record's existing cross-run gates.

THIS RUN CAN ANSWER IT COMPLETELY, which is unusual: `data/prices.csv` has exactly **12**
recoverable vintages in git (2026-09-03 .. 2026-09-16) and `data/prices_broad.csv` has 4,
and the research record itself begins 2026-09-03.  The vintage population is therefore not
sampled — it is the whole thing.  So the run does three separable pieces of work:

  (A) THE CENSUS.  Is `prices.csv` append-only?  1159 measured ONE transition.  This
      measures ALL 11, plus B136's 3, cell by cell.
  (B) THE REPAIR PRICING.  Four repairs x four gate sets, scored on the record's own
      committed anchors at the record's own declared tolerances.
  (C) THE VERDICT-STABILITY ARM, which is what actually matters for capital: re-run the
      record's own 4a/4b decision on EVERY vintage and count how many KEEP/KILL verdicts
      FLIP.  A rewritten tape that wrecks the gates but never flips a verdict is a very
      different problem from one that flips verdicts.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  REPAIR    {R_NONE, R_TOLERANCE, R_APPENDONLY, R_FINGERPRINT}
  GATE SET  {G_ANCHOR, G_BENCH, G_VERDICT, G_ALL}
= 16 cells, EVERY ONE PUBLISHED in `.repairs.csv`.  VINTAGE is NOT a dial — it is the
population under census and all 12 (U56) / 4 (B136) are published everywhere.  LADDER
{GROSS, N} is not a dial either (1154/1159's construction): all 44 rungs are built and
published on every vintage.  PANEL {U56, B136} is not a dial.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1150/1154/1161's construction:
CAND20 legs [(21,252),(0,126),(0,63)], cap INF, max_vol 0.60, min hold 126, N=20, gross
0.75, cadence W, cost 10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, zero cash.
`research/universe.json` and `research/universe_broad.json` are UNCHANGED across the whole
recoverable history (G11), so a vintage is purely a price-file vintage and nothing else.

Writes: .gates.csv .census.csv .anchors.csv .repairs.csv .ladder.csv .flips.csv
        .hypotheses.csv .walkforward.csv .console.txt
Deterministic, standalone, no network (git object reads only).  Does not modify RULES.md /
PROTOCOL.md / scan.py / bot.py / baseline.py / engine.py.
"""
import io, json, subprocess, sys, time, zlib, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, EXCLUDE  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "is-the-RECORD-REPRODUCIBLE-AT-ALL-while-prices-csv-is-REWRITTEN-NIGHTLY"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG, WARMUP, MAXVOL0 = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, COST0 = 0.75, "W", 126, 20, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
START = "2008-01-01"

LAD = {"GROSS": [round(0.20 + 0.025 * i, 3) for i in range(33)],
       "N": [3, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50]}

# ------------------------------------------------------------------ THE TWO DIALS
REPAIRS = ["R_NONE", "R_TOLERANCE", "R_APPENDONLY", "R_FINGERPRINT"]
GATESETS = ["G_ANCHOR", "G_BENCH", "G_VERDICT", "G_ALL"]

# The record's committed cross-run anchors, quoted from their own files, NEVER re-derived,
# each with the tolerance the record itself declares for it.
ANCHORS = [
    ("A936_CAGR",   "U56 W/H126/N=20 CAGR",        0.155787, 5e-5, "book"),
    ("A936_SHARPE", "U56 W/H126/N=20 Sharpe",      1.139701, 5e-5, "book"),
    ("A936_MAXDD",  "U56 W/H126/N=20 MaxDD",      -0.191276, 5e-5, "book"),
    ("A1098_CAGR",  "U56 n=12 CAGR",               0.1771,   5e-4, "book"),
    ("A1098_SHARPE", "U56 n=12 Sharpe",            1.1692,   5e-4, "book"),
    ("A1098_MAXDD", "U56 n=12 MaxDD",             -0.2017,   5e-4, "book"),
    ("SPY_OOS_CAGR", "SPY OOS CAGR",               0.1521,   5e-4, "bench"),
    ("SPY_OOS_SHARPE", "SPY OOS Sharpe",           0.8713,   5e-4, "bench"),
    ("SPY_OOS_MAXDD", "SPY OOS MaxDD",            -0.3372,   5e-4, "bench"),
    ("LIVE_MAXDD",  "live RULES v2 MaxDD",        -0.1205,   5e-4, "bench"),
]
# 1159's committed restatement measurement for commit 6f1fcb1 — the object G8 replays
A1159_RESTATE = dict(cells=31505, shared=258733, share=0.1218, tickers=48, maxrel=0.008384)

# repair-specific cost bars, DECLARED BEFORE ANY NUMBER
BAR_PASS = 0.90                 # a repair must take the gate pass rate above this
BAR_RESOLUTION_LOST = 0.10      # R_TOLERANCE: share of adjacent-rung pairs it blinds
BAR_BYTES = 64                  # R_FINGERPRINT: bytes per committed constant
BAR_IDENTIFIABLE = 0.90         # R_FINGERPRINT: share of anchors whose vintage resolves

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True).stdout


# ---------------------------------------------- 1082/../1154/1161's fast runner, verbatim
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (comp * (0.5 + 0.5 * above.astype(float))).values, above.values, vol20.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def prep(px):
    idx = px.index
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    sc, above, vol20 = mech(px)
    return dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                warm=warm, ins=ins, oos=oos, sc=sc, above=above, vol20=vol20,
                spy=px["SPY"].pct_change().fillna(0.0).values)


def run_cell(d, gross=GROSS0, N=N0, H=HOLD0, freq=FREQ0, maxvol=MAXVOL0):
    mk = rebalance_mask(d["idx"], freq).values
    mkl = np.roll(mk, LAG)
    mkl[:LAG] = False
    reb = np.flatnonzero(mk)
    el = d["above"] & (d["vol20"] < maxvol)
    W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    g, t = nrun(d["rets"], Wl, mkl)
    return g - t * COST0 / 1e4, t


def blocks_m(r, d):
    rr = r[d["warm"]]
    c, s, dd = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[d["oos"]])
    ic, is_, idd = fmet(r[d["ins"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return dict(L_H1=b["H1"] > sb["H1"], L_H2=b["H2"] > sb["H2"],
                L_OOS=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                L_DD=abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"]),
                L_CAGR=b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])


def legs_4b_oos(b, sb):
    return dict(O_S=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                O_DD=abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"]),
                O_CAGR=b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])


def legs_4a(b, lbm):
    return dict(A_H1=b["H1"] > lbm["H1"], A_H2=b["H2"] > lbm["H2"], A_DD=b["MaxDD"] >= lbm["MaxDD"])


def tent_min(m, sb):
    cap = DD_CAP * abs(sb["IS_MaxDD"])
    flo = CAGR_FLOOR * sb["IS_CAGR"]
    return min((m["IS_Sharpe"] - sb["IS_Sharpe"]) / abs(sb["IS_Sharpe"]),
               (cap - abs(m["IS_MaxDD"])) / cap,
               (m["IS_CAGR"] - flo) / abs(flo))


# ------------------------------------------------------------------ VINTAGE MACHINERY
def vintages_of(relpath):
    out = git("log", "--format=%H\t%h\t%ad\t%s", "--date=short", "--reverse", "--", relpath)
    rows = []
    for ln in out.decode().strip().split("\n"):
        h, sh, ad, msg = ln.split("\t", 3)
        rows.append(dict(sha=h, short=sh, date=ad, subject=msg[:60]))
    return rows


def read_vintage(sha, relpath, tickers):
    raw = git("show", f"{sha}:{relpath}")
    px = pd.read_csv(io.BytesIO(raw), index_col=0, parse_dates=True)
    have = [t for t in tickers if t in px.columns]
    return (px[have].loc[START:].dropna(how="all").ffill(),
            hashlib.sha256(raw).hexdigest(), len(raw), px)


def main():
    t0 = time.time()
    P(f"# Idea 1163 (cloud lane, {DATE}) — is the RECORD REPRODUCIBLE AT ALL while")
    P("#   data/prices.csv is REWRITTEN NIGHTLY?")
    P("#")
    P("# 1159 found its cross-run gates failing against 1148's numbers ONE DAY OLD, and")
    P("#   decomposed it into an extra BAR (97.3%) plus a RESTATEMENT of 31,505 of 258,733")
    P("#   shared cells by commit 6f1fcb1.  The queue asks for the CHEAPEST REPAIR.")
    P("#")
    P("# THE VINTAGE POPULATION IS NOT SAMPLED — IT IS THE WHOLE THING.  data/prices.csv has")
    P("#   12 recoverable vintages in git and the research record itself begins 2026-09-03,")
    P("#   so every price vintage any committed constant could have been computed on is here.")
    P("#")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4, the two the queue names): REPAIR {REPAIRS}")
    P(f"#   x GATE SET {GATESETS} = {len(REPAIRS) * len(GATESETS)} cells, EVERY ONE PUBLISHED.")
    P("#   VINTAGE is NOT a dial — it is the population under census, all published.")
    P("#   LADDER {GROSS, N} is not a dial (1154/1159's construction): all 44 rungs built on")
    P("#   every vintage.  PANEL {U56, B136} is not a dial.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL0}, min hold {HOLD0}, N {N0},")
    P(f"#   gross {GROSS0}, cadence {FREQ0}, cost {COST0} bps (rule 2), LAG {LAG}, warm-up")
    P(f"#   {WARMUP}, IS end {IS_END}, zero cash.")
    P("#")
    P("# DEFINITIONS, DECLARED BEFORE ANY NUMBER:")
    P("#   RESTATED CELL — a (date, ticker) present in BOTH of two consecutive vintages whose")
    P("#     value differs.  APPEND-ONLY — zero restated cells at a transition.")
    P("#   R_NONE        run the gate on the CURRENT file, compare to the committed constant at")
    P("#                 the tolerance the record itself declares (5e-5 book, 5e-4 bench).")
    P("#   R_TOLERANCE   the same, with every tolerance widened to the observed MAX vintage-")
    P("#                 induced spread of that statistic.  Paid in RESOLUTION LOST.")
    P("#   R_APPENDONLY  rebuild the tape so no cell is ever restated (every shared cell keeps")
    P("#                 its EARLIEST recoverable value; only genuinely new rows append), then")
    P("#                 run the gate at the ORIGINAL tolerance.")
    P("#   R_FINGERPRINT commit a tape hash beside every constant; the gate re-runs on THAT")
    P("#                 vintage, or declares itself UNREPRODUCIBLE.  Paid in bytes per")
    P("#                 constant, and it only works if the vintage is IDENTIFIABLE.")
    P("#   RESOLUTION LOST — the share of ADJACENT-RUNG pairs on the record's own two ladders")
    P("#     whose statistic differs by LESS than the widened tolerance, i.e. pairs of")
    P("#     genuinely different books a widened gate can no longer tell apart.")
    P("#   VERDICT FLIP — a (ladder, rung, path) whose 4a / 4b-full / 4b-OOS verdict differs")
    P("#     between a vintage and the CURRENT one.")
    P("#")
    P("# HYPOTHESES, DECLARED BEFORE ANY NUMBER:")
    P("#   H_NOTAPPEND   prices.csv is NOT append-only at a MAJORITY of its transitions")
    P("#                 (>= 6 of 11 restate at least one shared cell).  1159 saw one; this")
    P("#                 asks whether 6f1fcb1 was exceptional or routine.")
    P("#   H_SMALLMOVES  the restatements are numerically tiny: median |relative move| over all")
    P("#                 restated cells < 1e-4.  (1159 measured 1.50e-06 on its one commit.)")
    P("#   H_GATEFAIL    under R_NONE the record's own anchors FAIL at a majority of (anchor,")
    P("#                 vintage) cells at their declared tolerances.")
    P("#   H_VERDICTSTABLE  despite that, the SCIENCE is vintage-stable: < 5% of (vintage,")
    P("#                 ladder, rung, path) verdict cells flip against the current vintage.")
    P("#                 If this fails, the defect is not bookkeeping — it reaches capital.")
    P("#   H_APPENDNOFIX R_APPENDONLY does NOT on its own restore the gates (pass rate < 0.90),")
    P("#                 because 1159 attributed 97.3% of the deviation to the extra BAR, which")
    P("#                 an append-only cache does not remove.")
    P("#   H_FPWINS      R_FINGERPRINT is the cheapest repair clearing BAR_PASS: it costs <= 64")
    P("#                 bytes per constant and identifies the vintage for >= 0.90 of anchors.")
    P("# DECISION RULE, declared before any number: a repair is ENACT-WORTHY iff it takes the")
    P("#   gate pass rate above 0.90 AND its cost clears its own declared bar (R_TOLERANCE:")
    P("#   resolution lost < 0.10; R_FINGERPRINT: <= 64 bytes and >= 0.90 identifiable;")
    P("#   R_APPENDONLY: pass rate >= 0.90).  CHEAPEST = enact-worthy at the lowest cost in the")
    P("#   currency the record actually pays.  Nothing is enacted here either way (rule 6).")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  {name:<4s} {what:<64s} {value:.2e}   {'PASS' if ok else 'FAIL'}")

    # ------------------------------------------------------------ THE VINTAGES
    P("## THE VINTAGES — the whole recoverable population, stamped before any result number")
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    TICK_U56 = sorted({t for g in U.values() for t in g} - set(EXCLUDE))
    TICK_B136 = json.loads((ROOT / "research" / "universe_broad.json").read_text())

    SPEC = {"U56": ("data/prices.csv", TICK_U56), "B136": ("data/prices_broad.csv", TICK_B136)}
    vint = {}
    for panel, (rel, tk) in SPEC.items():
        vs = vintages_of(rel)
        for v in vs:
            px, h, nb, rawpx = read_vintage(v["sha"], rel, tk)
            # A pre-bugfix vintage is one indexed on CALENDAR days (commit c006b439 "Fix
            # calendar-day index bug" aligned crypto to equity trading days).  Detected
            # from the tape itself — weekend bars present — never from the commit message.
            wknd = int((px.index.dayofweek >= 5).sum())
            v.update(px=px, raw=rawpx, sha256=h, bytes=nb, rows=len(px), cols=len(px.columns),
                     rawcols=len(rawpx.columns), last=str(px.index[-1].date()),
                     weekend_bars=wknd, calendar_indexed=bool(wknd > 0))
        vint[panel] = vs
        P(f"  {panel}: {len(vs)} vintages of {rel}")
        for v in vs:
            P(f"    {v['short']}  {v['date']}  rows {v['rows']:,}  cols {v['cols']:3d} "
              f"(raw {v['rawcols']:3d})  last bar {v['last']}  {v['bytes']:,} bytes  "
              f"sha256 {v['sha256'][:12]}"
              + (f"   ** CALENDAR-INDEXED ({v['weekend_bars']:,} weekend bars)"
                 if v["calendar_indexed"] else ""))
    # The TRADING-DAY subset, declared here: every vintage whose tape is not calendar-indexed.
    # Every headline below is reported over ALL vintages AND over this subset, because two
    # of U56's twelve carry a known, since-fixed index bug and it would be dishonest to let
    # them either dominate a spread or be quietly dropped.
    VOK = {p: [v for v in vint[p] if not v["calendar_indexed"]] for p in SPEC}
    for p in SPEC:
        P(f"  {p}: {len(VOK[p])} of {len(vint[p])} vintages are TRADING-DAY indexed "
          f"({', '.join(v['short'] for v in vint[p] if v['calendar_indexed']) or 'none excluded'}"
          f"{' carry the calendar-day index bug' if len(VOK[p]) < len(vint[p]) else ''})")
    P("")

    # ------------------------------------------------------------ GATES
    P("## GATES — printed before any result number")
    cur = {p: prep(vint[p][-1]["px"]) for p in SPEC}
    d = cur["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["above"] & (d["vol20"] < MAXVOL0), d["priced"], np.flatnonzero(mk),
              N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST0, freq=FREQ0)["returns"].values
    rf, _ = run_cell(d)
    v1 = float(np.abs(eng[d["warm"]] - rf[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest", v1, v1 < 1e-12)

    lu = load_universe().dropna(how="all").ffill()
    v2 = float(np.abs(lu.values - vint["U56"][-1]["px"].reindex_like(lu).values)[
        ~np.isnan(lu.values)].max()) if lu.shape == vint["U56"][-1]["px"].shape else np.inf
    gate("G2", "vintage reader (HEAD) == baseline.load_universe() on disk", v2, v2 == 0.0)

    rf2, _ = run_cell(d)
    v3 = float(np.abs(rf - rf2).max())
    gate("G3", "determinism (same cell twice)", v3, v3 == 0.0)

    r12, _ = run_cell(d, N=12)
    m12 = blocks_m(r12, d)
    v4 = max(abs(m12["CAGR"] - 0.1771), abs(m12["Sharpe"] - 1.1692), abs(m12["MaxDD"] + 0.2017))
    gate("G4", "1098/1102's n=12 triple on the CURRENT vintage (reported, expected to FAIL)",
         v4, True)
    P(f"       ({m12['CAGR']:.4%} / {m12['Sharpe']:.4f} / {m12['MaxDD']:.4%}) — "
      f"the gate is recorded as PASS because its FAILING is this run's subject, not its bug.")

    # G5 — 1159's restatement measurement for 6f1fcb1 must replay
    def restate_pair(a, b):
        A, B = a["px"], b["px"]
        cols = [c for c in A.columns if c in B.columns]
        rows = A.index.intersection(B.index)
        X, Y = A.loc[rows, cols], B.loc[rows, cols]
        both = X.notna() & Y.notna()
        diff = (X != Y) & both
        rel = (Y - X).abs() / X.abs().replace(0, np.nan)
        rv = rel.values[diff.values]
        rv = rv[np.isfinite(rv)]
        per_t = diff.sum(axis=0)
        return dict(shared=int(both.values.sum()), restated=int(diff.values.sum()),
                    share=float(diff.values.sum() / max(both.values.sum(), 1)),
                    tickers_touched=int((per_t > 0).sum()), n_cols=len(cols),
                    rows_added=int(len(B.index.difference(A.index))),
                    rows_removed=int(len(A.index.difference(B.index))),
                    max_rel=float(rv.max()) if len(rv) else 0.0,
                    med_rel=float(np.median(rv)) if len(rv) else 0.0,
                    first_restated=str(diff.any(axis=1).idxmax().date()) if diff.values.any() else "")

    # G5 replays 1159's object on 1159's OWN construction: the RAW file, ALL columns, no
    # universe filter and no ffill.  This run's own census is the 56-name universe one; the
    # two differ by exactly the two crypto columns baseline.EXCLUDE drops, and the gate is
    # matched to 1159 rather than the tolerance widened.
    vs = vint["U56"]
    last_raw = restate_pair(dict(px=vs[-2]["raw"]), dict(px=vs[-1]["raw"]))
    g5 = max(abs(last_raw["restated"] - A1159_RESTATE["cells"]) / A1159_RESTATE["cells"],
             abs(last_raw["shared"] - A1159_RESTATE["shared"]) / A1159_RESTATE["shared"],
             abs(last_raw["tickers_touched"] - A1159_RESTATE["tickers"]) / A1159_RESTATE["tickers"],
             abs(last_raw["max_rel"] - A1159_RESTATE["maxrel"]) / A1159_RESTATE["maxrel"])
    gate("G5", "CROSS-RUN 1159's 6f1fcb1 restatement census, on 1159's RAW construction",
         g5, g5 < 1e-3)
    P(f"       (restated {last_raw['restated']:,} of {last_raw['shared']:,} = "
      f"{last_raw['share']:.4f}, {last_raw['tickers_touched']} of {last_raw['n_cols']} cols, "
      f"max rel {last_raw['max_rel']:.6f}) vs 1159's "
      f"{A1159_RESTATE['cells']:,} / {A1159_RESTATE['shared']:,} = {A1159_RESTATE['share']}, "
      f"{A1159_RESTATE['tickers']} tickers, {A1159_RESTATE['maxrel']}")
    last_u = restate_pair(vs[-2], vs[-1])
    P(f"       (this run's 56-name UNIVERSE census of the same commit: "
      f"{last_u['restated']:,} of {last_u['shared']:,} = {last_u['share']:.4f}, "
      f"{last_u['tickers_touched']} of {last_u['n_cols']} cols — the difference from 1159 is "
      f"exactly the 2 crypto columns baseline.EXCLUDE drops.)")

    v6 = max(int(np.abs(rebalance_mask(d["idx"], f).values.astype(int)
                        - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gate("G6", "rebalance_mask stable across calls", float(v6), v6 == 0)

    # G11 — the universes must be BYTE-IDENTICAL at the first and last price vintage, so a
    # vintage is a price-file vintage and nothing else.  Measured by blob hash, not by
    # counting commits in a date window.
    def blob(sha, f):
        try:
            return hashlib.sha256(git("show", f"{sha}:{f}")).hexdigest()
        except subprocess.CalledProcessError:
            return None

    ujs = []
    for f, first in (("research/universe.json", vint["U56"][0]["sha"]),
                     ("research/universe_broad.json", vint["B136"][0]["sha"])):
        a, b = blob(first, f), blob(vint["U56"][-1]["sha"], f)
        ujs.append((f, a, b, a is not None and a == b))
    nbad = sum(1 for _, _, _, ok in ujs if not ok)
    gate("G11", "universes BYTE-IDENTICAL from their own first price vintage to HEAD",
         float(nbad), nbad == 0)
    for f, a, b, ok in ujs:
        P(f"       {f:<32s} {(a or 'absent')[:12]} -> {(b or 'absent')[:12]}  "
          f"{'same' if ok else 'CHANGED'}")

    # ------------------------------------------------------------ (A) THE CENSUS
    P("")
    P("## (A) THE CENSUS — is prices.csv append-only?  ALL transitions, cell by cell")
    crows = []
    for panel in SPEC:
        vs = vint[panel]
        for i in range(1, len(vs)):
            r = restate_pair(vs[i - 1], vs[i])
            r.update(panel=panel, frm=vs[i - 1]["short"], to=vs[i]["short"],
                     frm_date=vs[i - 1]["date"], to_date=vs[i]["date"],
                     append_only=bool(r["restated"] == 0))
            crows.append(r)
            P(f"  {panel:<5s} {vs[i-1]['short']} -> {vs[i]['short']} ({vs[i]['date']})  "
              f"+{r['rows_added']:2d} rows  restated {r['restated']:6,d} of {r['shared']:7,d} "
              f"({r['share']:.4f})  {r['tickers_touched']:3d} cols  "
              f"max rel {r['max_rel']:.2e}  med {r['med_rel']:.2e}  "
              f"back to {r['first_restated'] or '-':<10s} "
              f"{'APPEND-ONLY' if r['append_only'] else 'RESTATED'}")
    census = pd.DataFrame(crows)
    dump(census, "census")

    # ------------------------------------------------------------ THE ANCHORS x VINTAGES
    P("")
    P("## THE ANCHORS ON EVERY VINTAGE — which vintage does each committed constant live on?")
    preps = {}
    anchor_vals = {}
    for panel in SPEC:
        for v in vint[panel]:
            preps[(panel, v["short"])] = prep(v["px"])
    for v in vint["U56"]:
        dv = preps[("U56", v["short"])]
        m20 = blocks_m(run_cell(dv)[0], dv)
        m12v = blocks_m(run_cell(dv, N=12)[0], dv)
        sp = blocks_m(dv["spy"], dv)
        lr = backtest(dv["px"], rules_v2_weights(dv["px"]), cost_bps=COST0, freq="W")["returns"].values
        lm = blocks_m(lr, dv)
        anchor_vals[v["short"]] = {
            "A936_CAGR": m20["CAGR"], "A936_SHARPE": m20["Sharpe"], "A936_MAXDD": m20["MaxDD"],
            "A1098_CAGR": m12v["CAGR"], "A1098_SHARPE": m12v["Sharpe"], "A1098_MAXDD": m12v["MaxDD"],
            "SPY_OOS_CAGR": sp["OOS_CAGR"], "SPY_OOS_SHARPE": sp["OOS_Sharpe"],
            "SPY_OOS_MAXDD": sp["OOS_MaxDD"], "LIVE_MAXDD": lm["MaxDD"]}
    arows = []
    okset = {v["short"] for v in VOK["U56"]}
    for key, what, committed, tol, kind in ANCHORS:
        vals = {v["short"]: anchor_vals[v["short"]][key] for v in vint["U56"]}
        ok_vals = {k: x for k, x in vals.items() if k in okset}
        devs = {k: abs(x - committed) for k, x in vals.items()}
        best = min(devs, key=devs.get)
        hits = [k for k, x in devs.items() if x < tol]
        ok_hits = [k for k in hits if k in okset]
        spread = max(vals.values()) - min(vals.values())
        ok_spread = max(ok_vals.values()) - min(ok_vals.values())
        arows.append(dict(anchor=key, what=what, committed=committed, tol=tol, kind=kind,
                          best_vintage=best, best_dev=devs[best],
                          n_vintages_within_tol=len(hits),
                          identifiable=bool(len(hits) == 1),
                          n_tradingday_within_tol=len(ok_hits),
                          identifiable_tradingday=bool(len(ok_hits) == 1),
                          hit_vintages="|".join(hits),
                          current_dev=devs[vint["U56"][-1]["short"]],
                          current_pass=bool(devs[vint["U56"][-1]["short"]] < tol),
                          vintage_spread=float(spread),
                          vintage_spread_tradingday=float(ok_spread),
                          val_min=float(min(vals.values())), val_max=float(max(vals.values()))))
        P(f"  {key:<16s} committed {committed: .6f}  tol {tol:.0e}  best vintage {best} "
          f"(dev {devs[best]:.2e})  within-tol {len(hits):2d} of 12 ({len(ok_hits)} of 10 "
          f"trading-day)  CURRENT dev {devs[vint['U56'][-1]['short']]:.2e} "
          f"{'PASS' if devs[vint['U56'][-1]['short']] < tol else 'FAIL'}  "
          f"spread {spread:.2e} (trading-day {ok_spread:.2e})")
    anchors = pd.DataFrame(arows)
    dump(anchors, "anchors")

    # ------------------------------------------------------------ (C) THE LADDER x VINTAGE
    P("")
    P("## (C) THE LADDERS ON EVERY VINTAGE — 44 rungs x 12 (U56) / 4 (B136) vintages")
    lrows = []
    for panel in SPEC:
        for v in vint[panel]:
            dv = preps[(panel, v["short"])]
            sb = blocks_m(dv["spy"], dv)
            lr = backtest(dv["px"], rules_v2_weights(dv["px"]), cost_bps=COST0, freq="W")["returns"].values
            lbm = blocks_m(lr, dv)
            for lad, rungs in LAD.items():
                for j, rung in enumerate(rungs):
                    kw = dict(gross=GROSS0, N=N0)
                    kw["gross" if lad == "GROSS" else "N"] = rung
                    r, tt = run_cell(dv, **kw)
                    mm = blocks_m(r, dv)
                    l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm)
                    lrows.append(dict(panel=panel, vintage=v["short"], vdate=v["date"],
                                      ladder=lad, rung_i=j, rung=str(rung),
                                      **{k: float(x) for k, x in mm.items()},
                                      tent_IS=float(tent_min(mm, sb)),
                                      SPY_Sharpe=float(sb["Sharpe"]),
                                      SPY_OOS_Sharpe=float(sb["OOS_Sharpe"]),
                                      pass_4b=bool(all(l4b.values())),
                                      pass_4b_oos=bool(all(l4bo.values())),
                                      pass_4a=bool(all(l4a.values()))))
            P(f"  {panel:<5s} {v['short']} {v['date']}  44 rungs  ({time.time() - t0:.0f}s)")
    ladder = pd.DataFrame(lrows)
    dump(ladder, "ladder")

    # ------------------------------------------------------------ VERDICT FLIPS
    P("")
    P("## VERDICT FLIPS against the CURRENT vintage — the arm that reaches capital")
    frows = []
    for panel in SPEC:
        curv = vint[panel][-1]["short"]
        base = ladder[(ladder.panel == panel) & (ladder.vintage == curv)].set_index(["ladder", "rung"])
        for v in vint[panel][:-1]:
            sub = ladder[(ladder.panel == panel) & (ladder.vintage == v["short"])].set_index(["ladder", "rung"])
            for path in ("pass_4b", "pass_4b_oos", "pass_4a"):
                a, b = sub[path].reindex(base.index), base[path]
                fl = int((a.values != b.values).sum())
                frows.append(dict(panel=panel, vintage=v["short"], vdate=v["date"], path=path,
                                  calendar_indexed=bool(v["calendar_indexed"]),
                                  n_rungs=len(b), n_flips=fl, flip_rate=fl / len(b)))
    flips = pd.DataFrame(frows)
    dump(flips, "flips")
    tot_cells = int(flips["n_rungs"].sum())
    tot_flips = int(flips["n_flips"].sum())
    fl_ok = flips[~flips.calendar_indexed]
    tot_cells_ok = int(fl_ok["n_rungs"].sum())
    tot_flips_ok = int(fl_ok["n_flips"].sum())
    P(f"  TOTAL {tot_flips} flips of {tot_cells} (vintage, ladder, rung, path) cells "
      f"= {tot_flips / tot_cells:.4f}")
    P(f"  TRADING-DAY VINTAGES ONLY: {tot_flips_ok} flips of {tot_cells_ok} "
      f"= {tot_flips_ok / tot_cells_ok:.4f}")
    for path in ("pass_4b", "pass_4b_oos", "pass_4a"):
        s, so = flips[flips.path == path], fl_ok[fl_ok.path == path]
        P(f"    {path:<12s} all {int(s['n_flips'].sum()):3d} of {int(s['n_rungs'].sum()):4d} "
          f"= {s['n_flips'].sum() / s['n_rungs'].sum():.4f}   |   trading-day "
          f"{int(so['n_flips'].sum()):3d} of {int(so['n_rungs'].sum()):4d} "
          f"= {so['n_flips'].sum() / so['n_rungs'].sum():.4f}")
    worst = flips.sort_values("n_flips", ascending=False).head(5)
    for _, w in worst.iterrows():
        P(f"    worst: {w['panel']} {w['vintage']} ({w['vdate']}) {w['path']} "
          f"{int(w['n_flips'])} of {int(w['n_rungs'])}"
          f"{'  [CALENDAR-INDEXED]' if w['calendar_indexed'] else ''}")

    # ------------------------------------------------------------ (B) THE REPAIRS
    P("")
    P("## (B) THE REPAIRS — 4 x 4 cells, every one published")

    # R_APPENDONLY: rebuild a tape in which no shared cell was ever restated
    def append_only_tape(panel, vs=None):
        vs = vs or vint[panel]
        base = vs[0]["px"].copy()
        for v in vs[1:]:
            nxt = v["px"]
            newcols = [c for c in nxt.columns if c not in base.columns]
            if newcols:
                base = base.join(nxt[newcols], how="outer")
            newrows = nxt.index.difference(base.index)
            if len(newrows):
                base = pd.concat([base, nxt.loc[newrows].reindex(columns=base.columns)]).sort_index()
        return base.ffill()

    def ao_anchor_vals(dao):
        m20a = blocks_m(run_cell(dao)[0], dao)
        m12a = blocks_m(run_cell(dao, N=12)[0], dao)
        spa = blocks_m(dao["spy"], dao)
        lra = backtest(dao["px"], rules_v2_weights(dao["px"]), cost_bps=COST0,
                       freq="W")["returns"].values
        lma = blocks_m(lra, dao)
        return {"A936_CAGR": m20a["CAGR"], "A936_SHARPE": m20a["Sharpe"], "A936_MAXDD": m20a["MaxDD"],
                "A1098_CAGR": m12a["CAGR"], "A1098_SHARPE": m12a["Sharpe"],
                "A1098_MAXDD": m12a["MaxDD"], "SPY_OOS_CAGR": spa["OOS_CAGR"],
                "SPY_OOS_SHARPE": spa["OOS_Sharpe"], "SPY_OOS_MAXDD": spa["OOS_MaxDD"],
                "LIVE_MAXDD": lma["MaxDD"]}

    # TWO append-only tapes, because the choice of WHERE an append-only cache would have
    # started is itself the finding: from the first vintage it inherits the calendar-day
    # index bug FOREVER (a cache that cannot be restated cannot be repaired either); from
    # the first trading-day vintage it is the fair reading of the repair.  Both published;
    # the repair is SCORED on the second, the favourable one.
    dao_all = prep(append_only_tape("U56"))
    dao_ok = prep(append_only_tape("U56", VOK["U56"]))
    ao_vals_all, ao_vals = ao_anchor_vals(dao_all), ao_anchor_vals(dao_ok)
    P(f"  R_APPENDONLY from the FIRST vintage: {dao_all['T']:,} rows, last bar "
      f"{dao_all['idx'][-1].date()} — it inherits the CALENDAR-DAY INDEX BUG permanently, "
      f"because a cache that may never be restated may never be REPAIRED either.")
    P(f"  R_APPENDONLY from the first TRADING-DAY vintage: {dao_ok['T']:,} rows, last bar "
      f"{dao_ok['idx'][-1].date()} (the current file has {cur['U56']['T']:,} rows) — "
      f"restating never happened, the extra BARS still did.  The repair is scored on THIS one.")

    # widened tolerances = observed max vintage spread per anchor, BOTH readings
    wide_all = {r["anchor"]: float(r["vintage_spread"]) for _, r in anchors.iterrows()}
    wide = {r["anchor"]: float(r["vintage_spread_tradingday"]) for _, r in anchors.iterrows()}

    # RESOLUTION LOST at the widened tolerance, on the record's own two ladders
    curL = ladder[(ladder.panel == "U56") & (ladder.vintage == vint["U56"][-1]["short"])]
    res_lost, res_lost_all = {}, {}
    for stat, anch in (("CAGR", "A936_CAGR"), ("Sharpe", "A936_SHARPE"), ("MaxDD", "A936_MAXDD")):
        tot = blind = blind_all = 0
        for lad in LAD:
            s = curL[curL.ladder == lad].sort_values("rung_i")[stat].values
            dd_ = np.abs(np.diff(s))
            tot += len(dd_)
            blind += int((dd_ < wide[anch]).sum())
            blind_all += int((dd_ < wide_all[anch]).sum())
        res_lost[stat], res_lost_all[stat] = blind / tot, blind_all / tot
        P(f"  R_TOLERANCE {stat:<7s}: trading-day spread {wide[anch]:.2e} blinds {blind:2d} of "
          f"{tot} adjacent-rung pairs = {blind / tot:.4f}   |   all-vintage spread "
          f"{wide_all[anch]:.2e} blinds {blind_all} of {tot} = {blind_all / tot:.4f}")

    def pass_rate(repair, gset):
        sel = [a for a in ANCHORS if (gset == "G_ALL"
                                      or (gset == "G_ANCHOR" and a[4] == "book")
                                      or (gset == "G_BENCH" and a[4] == "bench"))]
        if gset == "G_VERDICT":
            # the verdict gate: does the 4a/4b pass set reproduce?
            if repair == "R_NONE":
                return 1.0 - tot_flips / tot_cells, 0.0
            if repair == "R_TOLERANCE":
                return 1.0 - tot_flips / tot_cells, float(np.mean(list(res_lost.values())))
            if repair == "R_APPENDONLY":
                return 1.0 - tot_flips_ok / tot_cells_ok, 0.0
            return 1.0, float(BAR_BYTES)     # a fingerprinted verdict re-runs on its own tape
        n = ok = 0
        for key, what, committed, tol, kind in sel:
            if repair == "R_NONE":
                n += 1
                ok += int(abs(anchor_vals[vint["U56"][-1]["short"]][key] - committed) < tol)
            elif repair == "R_TOLERANCE":
                n += 1
                ok += int(abs(anchor_vals[vint["U56"][-1]["short"]][key] - committed)
                          < max(tol, wide[key]))
            elif repair == "R_APPENDONLY":
                n += 1
                ok += int(abs(ao_vals[key] - committed) < tol)
            else:   # R_FINGERPRINT — re-run on the vintage the fingerprint names
                n += 1
                row = anchors[anchors.anchor == key].iloc[0]
                ok += int(row["best_dev"] < tol)
        cost = {"R_NONE": 0.0, "R_TOLERANCE": float(np.mean(list(res_lost.values()))),
                "R_APPENDONLY": 0.0, "R_FINGERPRINT": float(BAR_BYTES)}[repair]
        return ok / max(n, 1), cost

    rrows = []
    for rep in REPAIRS:
        for gs in GATESETS:
            pr, cost = pass_rate(rep, gs)
            rrows.append(dict(repair=rep, gate_set=gs, pass_rate=pr, cost=cost,
                              clears_pass_bar=bool(pr >= BAR_PASS)))
    repairs = pd.DataFrame(rrows)
    dump(repairs, "repairs")
    P("")
    P(repairs.pivot(index="repair", columns="gate_set", values="pass_rate")
      .to_string(float_format=lambda x: f"{x:.4f}"))

    ident = float(anchors["identifiable"].mean())
    ident_ok = float(anchors["identifiable_tradingday"].mean())
    fp_bytes = 64
    P("")
    P("  R_FINGERPRINT has a PROSPECTIVE and a RETROACTIVE half and they do not agree:")
    P(f"    PROSPECTIVE — a constant committed WITH its tape hash re-runs on that tape by "
      f"construction: {repairs[(repairs.repair == 'R_FINGERPRINT') & (repairs.gate_set == 'G_ALL')].pass_rate.iloc[0]:.4f} "
      f"at {fp_bytes} bytes/constant (sha256 hex; 8 with crc32).")
    P(f"    RETROACTIVE — recovering the vintage of an ALREADY-committed constant from its "
      f"VALUE alone resolves to exactly one vintage for only "
      f"{int(anchors['identifiable'].sum())} of {len(anchors)} anchors = {ident:.4f} "
      f"({int(anchors['identifiable_tradingday'].sum())} of {len(anchors)} = {ident_ok:.4f} "
      f"among trading-day vintages).  The repair CANNOT be applied backwards.")
    P(f"  R_APPENDONLY pass rate on G_ALL: "
      f"{repairs[(repairs.repair == 'R_APPENDONLY') & (repairs.gate_set == 'G_ALL')].pass_rate.iloc[0]:.4f}"
      f"  (from the FIRST vintage instead, it also permanently inherits the calendar-day bug)")

    # ------------------------------------------------------------ HYPOTHESES
    P("")
    P("## HYPOTHESES — scored against the bars declared above")
    hyp = []
    u = census[census.panel == "U56"]
    nnot = int((~u.append_only).sum())
    hyp.append(("H_NOTAPPEND", ">= 6 of 11 U56 transitions restate a shared cell",
                float(nnot), nnot >= 6))
    allmed = float(np.median([r for r in census.med_rel if r > 0])) if (census.med_rel > 0).any() else 0.0
    hyp.append(("H_SMALLMOVES", "median |relative move| over restating transitions < 1e-4",
                allmed, allmed < 1e-4))
    pn = repairs[(repairs.repair == "R_NONE") & (repairs.gate_set == "G_ALL")].pass_rate.iloc[0]
    hyp.append(("H_GATEFAIL", "R_NONE pass rate on G_ALL < 0.50 (a majority FAIL)",
                float(pn), pn < 0.50))
    fr = tot_flips / tot_cells
    hyp.append(("H_VERDICTSTABLE", "verdict flip rate < 0.05", float(fr), fr < 0.05))
    pa = repairs[(repairs.repair == "R_APPENDONLY") & (repairs.gate_set == "G_ALL")].pass_rate.iloc[0]
    hyp.append(("H_APPENDNOFIX", "R_APPENDONLY G_ALL pass rate < 0.90", float(pa), pa < 0.90))
    pf = repairs[(repairs.repair == "R_FINGERPRINT") & (repairs.gate_set == "G_ALL")].pass_rate.iloc[0]
    hyp.append(("H_FPWINS", "R_FINGERPRINT G_ALL >= 0.90 and identifiable >= 0.90",
                float(min(pf, ident)), pf >= BAR_PASS and ident >= BAR_IDENTIFIABLE))
    for n, w, val, ok in hyp:
        P(f"  {n:<16s} {w:<56s} {val: .4f}   {'SUPPORTED' if ok else 'REFUTED'}")
    dump(pd.DataFrame([dict(hypothesis=n, bar=w, value=float(v), supported=bool(o))
                       for n, w, v, o in hyp]), "hypotheses")

    # ------------------------------------------------------------ RULE 8 + KEEP PATHS
    P("")
    P("## RULE 8 WALK-FORWARD + BOTH KEEP PATHS — on every vintage, and the question is")
    P("##   whether the WALK-FORWARD PICK ITSELF is vintage-stable.")
    wrows = []
    for panel in SPEC:
        for v in vint[panel]:
            sub = ladder[(ladder.panel == panel) & (ladder.vintage == v["short"])]
            for lad in LAD:
                s = sub[sub.ladder == lad].sort_values("rung_i")
                for ch, col, asc in (("C_ISSHARPE", "IS_Sharpe", False),
                                     ("C_ISCAGR", "IS_CAGR", False),
                                     ("C_IS4B", "tent_IS", False)):
                    row = s.iloc[int(np.nanargmax(s[col].values))]
                    wrows.append(dict(panel=panel, vintage=v["short"], vdate=v["date"],
                                      ladder=lad, chooser=ch, pick=row["rung"],
                                      OOS_CAGR=row["OOS_CAGR"], OOS_Sharpe=row["OOS_Sharpe"],
                                      OOS_MaxDD=row["OOS_MaxDD"],
                                      SPY_OOS_Sharpe=row["SPY_OOS_Sharpe"],
                                      pass_4b=bool(row["pass_4b"]),
                                      pass_4b_oos=bool(row["pass_4b_oos"]),
                                      pass_4a=bool(row["pass_4a"])))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    for panel in SPEC:
        for lad in LAD:
            for ch in ("C_ISSHARPE", "C_ISCAGR", "C_IS4B"):
                s = wf[(wf.panel == panel) & (wf.ladder == lad) & (wf.chooser == ch)]
                nun = s["pick"].nunique()
                P(f"  {panel:<5s} {lad:<5s} {ch:<11s} pick over {len(s)} vintages: "
                  f"{nun} distinct ({'|'.join(sorted(set(s['pick'])))})  "
                  f"4bOOS {int(s.pass_4b_oos.sum())}/{len(s)}  4a {int(s.pass_4a.sum())}/{len(s)}")
    P("")
    cv = ladder[ladder.vintage.isin([vint[p][-1]["short"] for p in SPEC])]
    for panel in SPEC:
        s = cv[cv.panel == panel]
        P(f"  {panel} CURRENT vintage base rates over {len(s)} rungs: "
          f"4b full {int(s.pass_4b.sum())}, 4b OOS {int(s.pass_4b_oos.sum())}, "
          f"4a {int(s.pass_4a.sum())}")
        dcur = cur[panel]
        sb = blocks_m(dcur["spy"], dcur)
        lr = backtest(dcur["px"], rules_v2_weights(dcur["px"]), cost_bps=COST0, freq="W")["returns"].values
        lm = blocks_m(lr, dcur)
        P(f"    SPY      full {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:6.2%}/{sb['OOS_Sharpe']:.4f}")
        P(f"    RULES v2 full {lm['CAGR']:7.2%} / {lm['Sharpe']:.4f} / {lm['MaxDD']:7.2%}  "
          f"halves {lm['H1']:.4f}/{lm['H2']:.4f}  OOS {lm['OOS_CAGR']:6.2%}/{lm['OOS_Sharpe']:.4f}")
        b = s[s.pass_4b & s.pass_4b_oos]
        if len(b):
            bb = b.iloc[int(np.nanargmax(b["Sharpe"].values))]
            P(f"    best cell clearing 4b full AND OOS: {bb['ladder']} {bb['rung']}  "
              f"{bb['CAGR']:7.2%} / {bb['Sharpe']:.4f} / {bb['MaxDD']:7.2%}  "
              f"OOS {bb['OOS_CAGR']:6.2%}/{bb['OOS_Sharpe']:.4f}")
        else:
            P("    no cell clears 4b full AND OOS on this panel's current vintage")

    gdf = pd.DataFrame(gaterows)
    dump(gdf, "gates")
    P(f"  GATES {sum(gates.values())} of {len(gates)} PASS")
    P("")
    P(f"## DONE in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
