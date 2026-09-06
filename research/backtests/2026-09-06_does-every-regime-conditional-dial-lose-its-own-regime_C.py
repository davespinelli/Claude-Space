#!/usr/bin/env python3
"""QUEUE idea 246 — does-every-regime-conditional-dial-lose-its-own-regime (lane C, 2026-09-06)

QUESTION (pre-registered, verbatim from QUEUE.md idea 246)
    "idea 75 is the 15th dial rule in the record to lose to doing nothing, and its mechanism
    is that conditioning ON a regime concentrates the instrument into the regime where it is
    most expensive.  Pool every published regime/state-conditional rule (idea 6's breadth
    sleeve, idea 40, idea 75, the 200d gate) and test the general claim: is the conditional
    version's loss systematically LARGER per armed day than the unconditional version's?
    Max 2 params."

THE CLAIM, MADE FALSIFIABLE
    Every instrument in the record cuts exposure when its own signal turns bad, and every one
    of them costs return.  Idea 75 measured, for ONE instrument (the per-name trailing stop),
    that its cost is concentrated in the SPY<200d regime — the very regime a "arm it only in
    crashes" rule would keep.  If that is a property of *conditioning* rather than a property
    of *stops*, then for a general instrument I and a general regime R:

        L(I, R)  ==  [ ann_return(I armed only on R) - ann_return(control) ] / frac_armed(R)

    the loss PER ARMED DAY, should be systematically MORE NEGATIVE than the unconditional

        L(I, always) == ann_return(I armed every day) - ann_return(control)

    H1 (the queue's claim)   median over cells of  L(I,R) - L(I,always)  < 0, and the sign
                             count is lopsided.  Falsified if the median is >= 0 or the sign
                             count is a coin flip.
    H2 (the mechanism)       inside the ALWAYS-ON arm, the daily delta (arm - control) is more
                             negative on regime-ON days than on regime-OFF days.  This is idea
                             75's decisive table generalised to every instrument; H2 is what
                             would MAKE H1 true, so both are reported and they can disagree.
    H3 (the consequence)     no conditional arm passes a KEEP path that its own always-on arm
                             or its own control does not already pass.

GRID — exactly TWO tuned parameters (INSTRUMENT family, REGIME family).  Every setting inside
    a family is the project's published one and is never selected on; every grid point printed.
      panels  u56 (56 names, universe.json), broad (136, universe_broad.json),
              small (441 sub-$2B names after idea 130's bad-split drop; SPY benchmark only)
      books   V1u (RULES v1's ungated 5-name book), TOP20 (idea 2), EWall (idea 10/72)
      instruments (8, all overlays on the SAME ungated base book, idea 94's definitions)
              g200-dg   per-name 200d MA gate, de-gross          (the 200d gate)
              band3-dg  200d MA with a sticky +/-3% band          (idea 57)
              abs12-dg  absolute momentum px > px[t-252]          (idea 62)
              vol60-dg  vol20 < 0.60                              (v1's other eligibility half)
              stop15    per-name trailing stop 15%                (idea 9 / 75)
              stop25    per-name trailing stop 25%                (idea 9 / 75)
              ddctl8    book DD > 8% -> halve, reset at -D/2       (idea 22 / 40)
              gross50   hold 0.50x the book                       (idea 66's parameter-free lever;
                        gross50 x breadth20 IS idea 6's breadth sleeve, gross50 x spy200 is
                        the classic 200d market-timing overlay)
      regimes (4)
              always     armed every day (f = 1) — the unconditional control arm
              spy200     SPY close < its own 200d MA                       (idea 75's crash regime)
              breadth20  panel breadth <= its EXPANDING 20th pct, min 3y    (idea 6 / 75)
              hivol80    SPY vol20 >= its EXPANDING 80th pct, min 3y        (idea 49's state)
      costs   10 bps (the PROTOCOL point) and 25 bps, both reported for every arm.
      3 x 3 x (8 x 4 + 1) x 2 = 594 runs, all written to the .grid.csv and printed.

ARMING MECHANICS (idea 75's convention, unchanged and applied uniformly)
    Arming gates the instrument's ACTION, never its STATE.  A disarmed trailing stop still
    tracks its per-name high; a disarmed DD control still tracks book equity and its own
    armed flag; a disarmed gate simply lets the ungated target through.  So `always` is a
    strict special case of every conditional arm, not a re-parameterisation — asserted in
    CHECK (b) at machine precision against idea 94's own simulator.
    The regime is read at close t-1 and the weights it selects are applied at t (idea 94's
    `run` already shifts targets by one bar), so there is no look-ahead.  breadth20 and
    hivol80 use EXPANDING quantiles with a 3y minimum: no full-sample threshold anywhere.
    Cost of that honesty: the two expanding regimes arm a smaller share of IS days than OOS
    days.  Stated in the coverage table, never corrected.

KEEP PATHS (PROTOCOL rule 4, evaluated on EVERY one of the 594 rows)
    4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.
RULE 8 (walk-forward, required)
    In each (panel, book, cost) cell the (INSTRUMENT, REGIME) pair is chosen on 2009-2016 IS
    Sharpe alone, over a menu that INCLUDES the do-nothing control, and read once, untouched,
    on 2017-2026 against the control, RULES v1 and SPY.  The regret against do-nothing is the
    reportable number: it is the 16th entry in the record's selection-loses census.

SURVIVORSHIP: all three panels are current-constituent lists (idea 54), so every absolute
    CAGR is optimistic.  The result here is a paired DELTA between arms on the same panel and
    the same days, which is far less exposed than the levels; the rule-8 levels are not.

Deterministic, standalone.  Imports research/baseline.py and idea 94's harness; modifies
nothing outside research/backtests/.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_does-every-regime-conditional-dial-lose-its-own-regime_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PROTO_COST = 10.0
PANELS = ["u56", "broad", "small"]
BOOKS = ["V1u", "TOP20", "EWall"]
REGIMES = ["always", "spy200", "breadth20", "hivol80"]
BREADTH_Q, VOL_Q, MIN_HIST = 0.20, 0.80, 756          # idea 75's settings, unchanged
INSTR = ["g200-dg", "band3-dg", "abs12-dg", "vol60-dg",
         "stop15", "stop25", "ddctl8", "gross50"]
SPEC = {"g200-dg":  dict(kind="gate", gate="g200"),
        "band3-dg": dict(kind="gate", gate="band3"),
        "abs12-dg": dict(kind="gate", gate="abs12"),
        "vol60-dg": dict(kind="gate", gate="vol60"),
        "stop15":   dict(kind="stop", stop=0.15),
        "stop25":   dict(kind="stop", stop=0.25),
        "ddctl8":   dict(kind="dd", D=0.08, k=0.5),
        "gross50":  dict(kind="gross", m=0.50)}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- panels & regimes
def panel(which):
    if which == "u56":
        px = load_universe()
        return px, list(px.columns)
    if which == "broad":
        px = load_universe(broad=True)
        return px, list(px.columns)
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px = px.drop(columns=[c for c in px.columns if c in bad])
    return px, [c for c in px.columns if c != "SPY"]     # SPY is a benchmark here, never held


def regime(px, names, r):
    """Boolean per-day series: is the instrument ARMED at close i?  No look-ahead."""
    if r == "always":
        return pd.Series(True, index=px.index)
    if r == "spy200":
        spy = px["SPY"]
        return (spy < spy.rolling(200).mean()).fillna(False)
    if r == "breadth20":
        p = px[names]
        br = (p > p.rolling(200).mean()).sum(axis=1) / p.notna().sum(axis=1).clip(lower=1)
        q = br.expanding(min_periods=MIN_HIST).quantile(BREADTH_Q)
        return (br <= q).fillna(False)
    if r == "hivol80":
        v = px["SPY"].pct_change().rolling(20).std() * np.sqrt(252)
        q = v.expanding(min_periods=MIN_HIST).quantile(VOL_Q)
        return (v >= q).fillna(False)
    raise ValueError(r)


# ---------------------------------------------------------------- one simulator, every arm
def run_cond(px, W_base, W_gate=None, armed=None, stop=None, D=None, k=1.0, m=1.0,
             bps=PROTO_COST, freq=FREQ):
    """idea 94's `run`, with one added mask: on DISARMED days the instrument does not act.

      gate   : target is W_gate on armed days, W_base on disarmed days
      stop   : the trigger fires only on armed days; the per-name high is tracked always
      dd     : the DD state machine runs always; the k multiplier applies only when armed
      gross  : the m multiplier applies only on armed days

    With armed == all-True and one instrument on, this reproduces H.run bit-for-bit
    (asserted in CHECK (b)).  Costs are charged inside the loop so both state machines see
    NET equity through t-1.
    """
    pxv = px.values
    rets = px.pct_change().fillna(0.0).values
    base = W_base.reindex(px.index).fillna(0.0).values
    gat = base if W_gate is None else W_gate.reindex(px.index).fillna(0.0).values
    arm = (np.ones(len(px), dtype=bool) if armed is None
           else armed.reindex(px.index).fillna(False).values)
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape

    cur = np.zeros(ncol)
    peak_p = np.full(ncol, np.nan)
    pending = np.zeros(ncol, dtype=bool)
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    eq, pk, dd_armed, n_stops, n_cut = 1.0, 1.0, False, 0, 0

    for i in range(nrow):
        if pending.any():                                # 1. stop exits decided at close t-1
            turn[i] += cur[pending].sum()
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        if mask[i] and i > 0:                            # 2. scheduled rebalance
            a = arm[i - 1]                               # regime read at close t-1
            if D is not None:                            # state machine always runs
                dd = eq / pk - 1.0
                if not dd_armed and dd < -D:
                    dd_armed = True
                elif dd_armed and dd > -D / 2.0:
                    dd_armed = False
            new = (gat[i - 1] if a else base[i - 1]).copy()
            if D is not None and dd_armed and a:
                new = new * k
                n_cut += 1
            if m != 1.0 and a:
                new = new * m
            s = new.sum()
            if s > 1.0:
                new = new / s
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp)
        pk = max(pk, eq)
        growth = cur * (1 + rets[i])                     # 3. drift
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
        if stop is not None:                             # 4. trailing highs / fire stops
            alive = cur > 1e-9
            p = pxv[i]
            peak_p = np.where(alive, np.fmax(np.where(np.isnan(peak_p), -np.inf, peak_p), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak_p * (1 - stop))
            if hit.any() and arm[i]:                     # DISARMED: high tracked, no fire
                pending |= hit
                n_stops += int(hit.sum())

    r = (pd.Series((held * rets).sum(axis=1), index=px.index)
         - pd.Series(turn, index=px.index) * bps / 1e4)
    return dict(r=r, to=pd.Series(turn, index=px.index), gross=pd.Series(gross_s, index=px.index),
                n_stops=n_stops, n_cut=n_cut)


# ---------------------------------------------------------------- metric helpers
def ann(r):
    """Annualised (arithmetic) return in pp/yr — additive across day subsets, which is what
    the regime split needs.  CAGR is reported separately for the KEEP paths."""
    return float(r.mean() * 252 * 100.0)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    ms = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=ms["MaxDD"], scagr=ms["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def keep_paths(r, v1, bars):
    h1, h2 = halves(r)
    b1, b2 = halves(v1)
    mm, mo = metrics(r), metrics(r.loc[OOS_START:])
    mv = metrics(v1)
    p4a = bool(h1 > b1 and h2 > b2 and mm["MaxDD"] >= mv["MaxDD"])
    p4b = bool(h1 > bars["s1"] and h2 > bars["s2"] and mo["Sharpe"] > bars["soos"]
               and abs(mm["MaxDD"]) <= 0.60 * abs(bars["sdd"])
               and mm["CAGR"] >= 0.70 * bars["scagr"])
    return p4a, p4b, h1, h2, mm, mo


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(pd.Series(a[ok]).rank(), pd.Series(b[ok]).rank())[0, 1])


def signtest(x):
    """Two-sided exact binomial p for #(<0) vs #(>0), ties dropped."""
    x = np.asarray([v for v in x if np.isfinite(v) and v != 0.0], float)
    n, kneg = len(x), int((x < 0).sum())
    if n == 0:
        return np.nan, 0, 0
    from math import comb
    tail = sum(comb(n, i) for i in range(0, min(kneg, n - kneg) + 1)) / 2.0 ** n
    return float(min(1.0, 2 * tail)), kneg, n


# ---------------------------------------------------------------- main
def main():
    grid, cover, mech, wf = [], [], [], []
    checked_b = False

    for pname in PANELS:
        px, names = panel(pname)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bars = bars_of(spy)
        v1w = rules_v1_weights(px[names]).reindex(columns=px.columns).fillna(0.0)
        v1 = {c: backtest(px, v1w, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        ms = metrics(spy)
        say("\n" + "=" * 190)
        say(f"PANEL {pname}: {len(names)} tradable names, {px.index[0].date()} -> {px.index[-1].date()}"
            f" | eval {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
        say(f"  SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"OOS Sharpe {bars['soos']:.3f} | 4b bars: DD cap {0.60*abs(bars['sdd']):.2%}, "
            f"CAGR floor {0.70*bars['scagr']:.2%}")

        arms = {r: regime(px, names, r) for r in REGIMES}
        for r in REGIMES:
            v = arms[r].loc[start:]
            cover.append(dict(panel=pname, regime=r, armed_frac=float(v.mean()),
                              armed_days=int(v.sum()),
                              frac_IS=float(v.loc[:IS_END].mean()),
                              frac_OOS=float(v.loc[OOS_START:].mean())))

        sub = px[names]
        for book in BOOKS:
            W_base = H.targets(sub, book).reindex(columns=px.columns).fillna(0.0)
            W_gate = {g: H.targets(sub, book, g, "dg").reindex(columns=px.columns).fillna(0.0)
                      for g in ("g200", "band3", "abs12", "vol60")}
            for cost in COSTS:
                ctl = run_cond(px, W_base, bps=cost)
                rc = ctl["r"].loc[start:]
                mc = metrics(rc)
                p4a, p4b, h1, h2, mm, mo = keep_paths(rc, v1[cost], bars)
                grid.append(dict(panel=pname, book=book, cost=cost, instr="control",
                                 regime="-", armed_frac=np.nan, CAGR=mm["CAGR"],
                                 Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                                 OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                                 OOS_MaxDD=mo["MaxDD"], ann_pp=ann(rc), d_ann=0.0,
                                 L_per_armed=0.0, dSharpe=0.0, dMaxDD=0.0,
                                 turn_yr=float(ctl["to"].loc[start:].sum() / (len(rc) / 252)),
                                 gross=float(ctl["gross"].loc[start:].mean()),
                                 pass4a=p4a, pass4b=p4b, IS_Sharpe=metrics(rc.loc[:IS_END])["Sharpe"]))

                for ins in INSTR:
                    sp = SPEC[ins]
                    kw = dict(W_gate=W_gate[sp["gate"]] if sp["kind"] == "gate" else None,
                              stop=sp.get("stop"), D=sp.get("D"), k=sp.get("k", 1.0),
                              m=sp.get("m", 1.0))
                    for reg in REGIMES:
                        a = run_cond(px, W_base, armed=arms[reg], bps=cost, **kw)
                        ra = a["r"].loc[start:]
                        f = float(arms[reg].loc[start:].mean())
                        d_ann = ann(ra) - ann(rc)
                        on = arms[reg].reindex(ra.index).fillna(False)
                        dser = ra - rc
                        d_cond_on = float(dser[on].mean() * 252 * 100) if on.any() else np.nan
                        d_cond_off = float(dser[~on].mean() * 252 * 100) if (~on).any() else np.nan
                        p4a, p4b, hh1, hh2, mm, mo = keep_paths(ra, v1[cost], bars)
                        grid.append(dict(panel=pname, book=book, cost=cost, instr=ins,
                                         regime=reg, armed_frac=f, CAGR=mm["CAGR"],
                                         Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=hh1, H2=hh2,
                                         OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                                         OOS_MaxDD=mo["MaxDD"], ann_pp=ann(ra), d_ann=d_ann,
                                         d_cond_on=d_cond_on, d_cond_off=d_cond_off,
                                         L_per_armed=d_ann / f if f > 0 else np.nan,
                                         dSharpe=mm["Sharpe"] - mc["Sharpe"],
                                         dMaxDD=abs(mc["MaxDD"]) - abs(mm["MaxDD"]),
                                         turn_yr=float(a["to"].loc[start:].sum() / (len(ra) / 252)),
                                         gross=float(a["gross"].loc[start:].mean()),
                                         pass4a=p4a, pass4b=p4b,
                                         IS_Sharpe=metrics(ra.loc[:IS_END])["Sharpe"]))

                        # ---- CHECK (b): always-on == idea 94's own simulator, exactly
                        if (not checked_b) and reg == "always" and ins in ("stop15", "g200-dg",
                                                                          "ddctl8", "gross50"):
                            ref = H.run(px, W_gate[sp["gate"]] if sp["kind"] == "gate" else W_base,
                                        m=sp.get("m", 1.0), stop=sp.get("stop"), D=sp.get("D"),
                                        k=sp.get("k", 1.0), reset="recover", bps=cost)
                            w = float((a["r"] - ref["r"]).abs().max())
                            say(f"  CHECK (b) {pname}/{book}/{ins}@{cost:g} always-on vs idea 94 "
                                f"`run`: max|d| = {w:.3e} -> {'EXACT' if w < 1e-12 else 'MISMATCH'}")
                            assert w < 1e-12, (ins, w)

                    # ---- H2 mechanism: split the ALWAYS-ON delta by each regime
                    a_always = run_cond(px, W_base, armed=arms["always"], bps=cost, **kw)
                    d = (a_always["r"] - ctl["r"]).loc[start:]
                    for reg in [x for x in REGIMES if x != "always"]:
                        on = arms[reg].reindex(d.index).fillna(False)
                        mech.append(dict(panel=pname, book=book, cost=cost, instr=ins, regime=reg,
                                         on_days=int(on.sum()), off_days=int((~on).sum()),
                                         d_on=float(d[on].mean() * 252 * 100) if on.any() else np.nan,
                                         d_off=float(d[~on].mean() * 252 * 100) if (~on).any() else np.nan))
            checked_b = True
            say(f"  built {pname}/{book}")

    G = pd.DataFrame(grid)
    C = pd.DataFrame(cover)
    M = pd.DataFrame(mech)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    C.to_csv(OUT / f"{STEM}.coverage.csv", index=False)
    M.to_csv(OUT / f"{STEM}.mechanism.csv", index=False)

    # ------------------------------------------------------------ 1. coverage
    say("\n" + "=" * 190)
    say("=== 1. REGIME COVERAGE (post-warm-up) ===")
    say(C.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------ 2. every grid point
    say("\n=== 2. ALL ARMS (every grid point; 4a/4b evaluated on each) ===")
    for cost in COSTS:
        say(f"\n--- cost {cost:g} bps ---")
        say(G[G.cost == cost].drop(columns=["cost"]).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ 3. H1
    say("\n" + "=" * 190)
    say("=== 3. H1 — loss per armed day: conditional vs unconditional ===")
    say("L = (ann return of arm - ann return of its control) / armed fraction, pp/yr per unit")
    piv = G[G.instr != "control"].pivot_table(index=["panel", "book", "cost", "instr"],
                                              columns="regime", values="L_per_armed")
    h1rows = []
    for reg in [r for r in REGIMES if r != "always"]:
        dd = (piv[reg] - piv["always"]).dropna()
        p, kneg, n = signtest(dd.values)
        h1rows.append(dict(regime=reg, n=n, median_dL=float(dd.median()),
                           mean_dL=float(dd.mean()), n_more_negative=kneg,
                           frac=kneg / n if n else np.nan, sign_p=p))
    H1 = pd.DataFrame(h1rows)
    say("\npooled over all (panel, book, cost, instrument) cells:")
    say(H1.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\nby INSTRUMENT (median over panel x book x cost of L(cond) - L(always)):")
    per = []
    for ins in INSTR:
        row = dict(instr=ins)
        for reg in [r for r in REGIMES if r != "always"]:
            sl = piv.xs(ins, level="instr")
            dd = (sl[reg] - sl["always"]).dropna()
            row[reg] = float(dd.median())
            row[reg + "_neg"] = f"{int((dd < 0).sum())}/{len(dd)}"
        row["L_always_med"] = float(piv.xs(ins, level="instr")["always"].median())
        per.append(row)
    PER = pd.DataFrame(per)
    say(PER.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    PER.to_csv(OUT / f"{STEM}.h1.csv", index=False)

    # ------------------------------------------------------------ 4. H2
    say("\n" + "=" * 190)
    say("=== 4. H2 — mechanism: the ALWAYS-ON delta split by regime (pp/yr) ===")
    say("d_on  = annualised (arm - control) on regime-ON days;  d_off = on regime-OFF days")
    m2 = M.groupby(["instr", "regime"]).agg(
        med_on=("d_on", "median"), med_off=("d_off", "median"),
        n=("d_on", "size")).reset_index()
    m2["on_minus_off"] = m2.med_on - m2.med_off
    frac = (M.assign(worse=lambda t: t.d_on < t.d_off)
             .groupby(["instr", "regime"]).worse.mean().rename("frac_on_worse"))
    m2 = m2.merge(frac, on=["instr", "regime"])
    say(m2.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    pooled = []
    for reg in [r for r in REGIMES if r != "always"]:
        s = M[M.regime == reg]
        dd = (s.d_on - s.d_off).dropna()
        p, kneg, n = signtest(dd.values)
        pooled.append(dict(regime=reg, n=n, median_on_minus_off=float(dd.median()),
                           n_on_worse=kneg, frac=kneg / n if n else np.nan, sign_p=p))
    P2 = pd.DataFrame(pooled)
    say("\npooled over all (panel, book, cost, instrument):")
    say(P2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ 4b. decomposition
    say("\n" + "=" * 190)
    say("=== 4b. DECOMPOSITION — is H1 the CONCENTRATION the queue named, or something else? ===")
    say("Write f for the armed fraction, d_on / d_off for the ALWAYS-ON arm's annualised delta")
    say("on regime-ON / regime-OFF days, and c_on / c_off for the CONDITIONAL arm's own delta on")
    say("the same two day sets.  Because ann() is additive over day sets,")
    say("    L(always) = f*d_on + (1-f)*d_off      L(cond) = c_on + ((1-f)/f)*c_off")
    say("so the queue's quantity splits EXACTLY three ways:")
    say("    L(cond) - L(always) = CONC + ACT + LEAK, where")
    say("    CONC = (1-f)*(d_on - d_off)   the instrument being dearer in its own regime")
    say("                                   -- this, and only this, is idea 75's mechanism")
    say("    ACT  = c_on - d_on             the conditional arm acting differently ON armed days")
    say("                                   (re-entry turnover, different entry state)")
    say("    LEAK = ((1-f)/f)*c_off         the conditional arm's delta on days it is SUPPOSED")
    say("                                   to be inert, blown up by the 1/f normalisation")
    key = ["panel", "book", "cost", "instr", "regime"]
    dec = M.merge(G[G.instr != "control"][key + ["L_per_armed", "armed_frac",
                                                 "d_cond_on", "d_cond_off"]], on=key, how="left")
    Lalw = (G[(G.regime == "always")][["panel", "book", "cost", "instr", "L_per_armed"]]
            .rename(columns={"L_per_armed": "L_always"}))
    dec = dec.merge(Lalw, on=["panel", "book", "cost", "instr"], how="left")
    f = dec.armed_frac
    dec["total"] = dec.L_per_armed - dec.L_always
    dec["CONC"] = (1.0 - f) * (dec.d_on - dec.d_off)
    dec["ACT"] = dec.d_cond_on - dec.d_on
    dec["LEAK"] = ((1.0 - f) / f) * dec.d_cond_off
    dec["ident"] = (dec.total - dec.CONC - dec.ACT - dec.LEAK).abs()
    say(f"\nidentity check  max|total - CONC - ACT - LEAK| = {dec.ident.max():.3e} "
        f"-> {'EXACT' if dec.ident.max() < 1e-8 else 'BROKEN'}")
    dec.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    agg = dict(n=("total", "size"), med_total=("total", "median"), med_CONC=("CONC", "median"),
               med_ACT=("ACT", "median"), med_LEAK=("LEAK", "median"),
               CONC_neg=("CONC", lambda s: int((s < 0).sum())),
               ACT_neg=("ACT", lambda s: int((s < 0).sum())),
               LEAK_neg=("LEAK", lambda s: int((s < 0).sum())))
    say("\nby REGIME (median pp/yr per armed unit; *_neg = how many of n cells are negative):")
    say(dec.groupby("regime").agg(**agg).reset_index().to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))
    say("\nby INSTRUMENT (n = 3 regimes x 3 panels x 3 books x 2 costs = 54):")
    say(dec.groupby("instr").agg(**agg).reset_index().to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))
    for lab in ("CONC", "ACT", "LEAK"):
        p, k, n = signtest(dec[lab].values)
        say(f"pooled {lab:5s}: negative in {k}/{n} (sign p {p:.4f}), "
            f"median {dec[lab].median():+.3f}, share of median total "
            f"{dec[lab].median() / dec.total.median():.0%}")

    say("\nc_off — the conditional arm's delta on the days it is DISARMED (pp/yr, should be ~0):")
    say(dec.groupby("regime").agg(n=("d_cond_off", "size"),
                                  med_c_off=("d_cond_off", "median"),
                                  med_abs_c_off=("d_cond_off", lambda s: float(s.abs().median())),
                                  med_1mf_over_f=("armed_frac",
                                                  lambda s: float(((1 - s) / s).median()))
                                  ).reset_index().to_string(index=False,
                                                            float_format=lambda x: f"{x:.3f}"))

    say("\nTURNOVER, the ACT term's proximate cause.  `switch_mult` = (conditional turnover /")
    say("always-on turnover) / armed fraction: 1.0 would mean the conditional arm trades in")
    say("proportion to the exposure it actually takes; >1 means it pays to flip in and out.")
    tv = (G[G.instr != "control"]
          .pivot_table(index=["panel", "book", "cost", "instr"], columns="regime", values="turn_yr"))
    fv = (G[G.instr != "control"]
          .pivot_table(index=["panel", "book", "cost", "instr"], columns="regime", values="armed_frac"))
    trow = []
    for reg in [r for r in REGIMES if r != "always"]:
        rat = (tv[reg] / tv["always"] / fv[reg]).replace([np.inf, -np.inf], np.nan).dropna()
        trow.append(dict(regime=reg, med_armed_frac=float(fv[reg].median()),
                         med_switch_mult=float(rat.median()),
                         q25=float(rat.quantile(.25)), q75=float(rat.quantile(.75)),
                         cells_gt_1=int((rat > 1).sum()), n=len(rat)))
    say(pd.DataFrame(trow).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------ 5. H3
    say("\n" + "=" * 190)
    say("=== 5. H3 — KEEP paths ===")
    tot = G[G.instr != "control"]
    say(f"conditional arms passing 4a: {int(tot[tot.regime != 'always'].pass4a.sum())}"
        f"/{len(tot[tot.regime != 'always'])}; passing 4b: "
        f"{int(tot[tot.regime != 'always'].pass4b.sum())}/{len(tot[tot.regime != 'always'])}")
    say(f"always-on arms passing 4a: {int(tot[tot.regime == 'always'].pass4a.sum())}"
        f"/{len(tot[tot.regime == 'always'])}; passing 4b: "
        f"{int(tot[tot.regime == 'always'].pass4b.sum())}/{len(tot[tot.regime == 'always'])}")
    ctlg = G[G.instr == "control"]
    say(f"do-nothing controls passing 4a: {int(ctlg.pass4a.sum())}/{len(ctlg)}; "
        f"4b: {int(ctlg.pass4b.sum())}/{len(ctlg)}")
    ctl_map = {(r.panel, r.book, r.cost): (r.pass4a, r.pass4b) for r in ctlg.itertuples()}
    alw_map = {(r.panel, r.book, r.cost, r.instr): (r.pass4a, r.pass4b)
               for r in G[G.regime == "always"].itertuples()}
    novel = tot[[not ctl_map[(r.panel, r.book, r.cost)][1] and r.pass4b for r in tot.itertuples()]]
    say(f"arms turning a 4b FAIL of their own control into a PASS: {len(novel)} of {len(tot)} "
        f"(this is idea 94's known result — every de-grossing instrument buys drawdown, and the "
        f"4b DD cap is what the ungated books fail)")
    cond = tot[tot.regime != "always"]
    strict = cond[[(not ctl_map[(r.panel, r.book, r.cost)][1])
                   and (not alw_map[(r.panel, r.book, r.cost, r.instr)][1])
                   and r.pass4b for r in cond.itertuples()]]
    say(f"CONDITIONAL arms passing 4b where BOTH their control AND their own always-on sibling "
        f"fail: {len(strict)} of {len(cond)}")
    if len(strict):
        say(strict.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    stricta = cond[[(not ctl_map[(r.panel, r.book, r.cost)][0])
                    and (not alw_map[(r.panel, r.book, r.cost, r.instr)][0])
                    and r.pass4a for r in cond.itertuples()]]
    say(f"same for 4a: {len(stricta)} of {len(cond)}")
    say("\n4b passes by (instr, regime):")
    say(tot.pivot_table(index="instr", columns="regime", values="pass4b",
                        aggfunc="sum").to_string())

    # ------------------------------------------------------------ 6. rule 8
    say("\n" + "=" * 190)
    say("=== 6. RULE 8 walk-forward — (instrument, regime) chosen on 2009-2016 IS Sharpe ===")
    for (pn, bk, ct), sl in G.groupby(["panel", "book", "cost"]):
        cand = sl[sl.instr != "control"]
        pick = cand.loc[cand.IS_Sharpe.idxmax()]
        do_nothing = sl[sl.instr == "control"].iloc[0]
        best_oos = cand.loc[cand.OOS_Sharpe.idxmax()]
        wf.append(dict(panel=pn, book=bk, cost=ct,
                       pick=f"{pick.instr}/{pick.regime}", pick_IS=pick.IS_Sharpe,
                       pick_OOS_S=pick.OOS_Sharpe, pick_OOS_CAGR=pick.OOS_CAGR,
                       pick_OOS_DD=pick.OOS_MaxDD,
                       ctl_IS=do_nothing.IS_Sharpe, ctl_OOS_S=do_nothing.OOS_Sharpe,
                       ctl_OOS_CAGR=do_nothing.OOS_CAGR, ctl_OOS_DD=do_nothing.OOS_MaxDD,
                       regret=pick.OOS_Sharpe - do_nothing.OOS_Sharpe,
                       IS_margin=pick.IS_Sharpe - do_nothing.IS_Sharpe,
                       best_possible=f"{best_oos.instr}/{best_oos.regime}",
                       best_OOS_S=best_oos.OOS_Sharpe,
                       spear_IS_OOS=spearman(cand.IS_Sharpe.values, cand.OOS_Sharpe.values)))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nchooser beats do-nothing OOS in {int((WF.regret > 0).sum())}/{len(WF)} cells; "
        f"mean regret {WF.regret.mean():+.4f}, median {WF.regret.median():+.4f}")
    say(f"chooser picks a CONDITIONAL arm in "
        f"{int((~WF['pick'].str.endswith('always')).sum())}/{len(WF)} cells")
    say(f"median Spearman(IS Sharpe, OOS Sharpe) across the 32-arm menu: "
        f"{WF.spear_IS_OOS.median():.3f}")

    # OOS vs SPY / RULES v1 for the picks, at the PROTOCOL cost
    say("\nOOS levels at 10 bps (pick vs do-nothing vs RULES v1 vs SPY):")
    lv = []
    for pn in PANELS:
        px, names = panel(pn)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        v1w = rules_v1_weights(px[names]).reindex(columns=px.columns).fillna(0.0)
        v1r = backtest(px, v1w, cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]
        mo_s, mo_v = metrics(spy.loc[OOS_START:]), metrics(v1r.loc[OOS_START:])
        for bk in BOOKS:
            w = WF[(WF.panel == pn) & (WF.book == bk) & (WF.cost == PROTO_COST)].iloc[0]
            lv.append(dict(panel=pn, book=bk, pick=w["pick"],
                           pick_CAGR=w.pick_OOS_CAGR, pick_S=w.pick_OOS_S, pick_DD=w.pick_OOS_DD,
                           ctl_CAGR=w.ctl_OOS_CAGR, ctl_S=w.ctl_OOS_S, ctl_DD=w.ctl_OOS_DD,
                           v1_CAGR=mo_v["CAGR"], v1_S=mo_v["Sharpe"], v1_DD=mo_v["MaxDD"],
                           spy_CAGR=mo_s["CAGR"], spy_S=mo_s["Sharpe"], spy_DD=mo_s["MaxDD"]))
    LV = pd.DataFrame(lv)
    LV.to_csv(OUT / f"{STEM}.oos.csv", index=False)
    say(LV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ 7. verdict
    say("\n" + "=" * 190)
    say("=== 7. VERDICT ===")
    for _, r in H1.iterrows():
        say(f"H1 {r.regime:10s}: median dL {r.median_dL:+.3f} pp/yr per armed unit, "
            f"{r.n_more_negative}/{r.n} more negative than always-on, sign p {r.sign_p:.4f}")
    for _, r in P2.iterrows():
        say(f"H2 {r.regime:10s}: median (on - off) {r.median_on_minus_off:+.3f} pp/yr, "
            f"on-regime worse in {r.n_on_worse}/{r.n}, sign p {r.sign_p:.4f}")
    say(f"H3: {len(strict)}/{len(cond)} conditional arms pass 4b where their control AND their "
        f"own always-on sibling both fail; {len(stricta)}/{len(cond)} for 4a")
    say(f"RULE 8: chooser beats do-nothing OOS in {int((WF.regret > 0).sum())}/{len(WF)}, "
        f"mean regret {WF.regret.mean():+.4f}")
    say("\nAlso reported, so the per-armed-day normalisation cannot mislead: the UNNORMALISED")
    say("total loss d_ann (arm - control, pp/yr over ALL days), conditional vs always-on:")
    pv = G[G.instr != "control"].pivot_table(index=["panel", "book", "cost", "instr"],
                                             columns="regime", values="d_ann")
    for reg in [r for r in REGIMES if r != "always"]:
        dd = (pv[reg] - pv["always"]).dropna()
        p, kneg, n = signtest(dd.values)
        say(f"  {reg:10s}: median d_ann(cond) {pv[reg].median():+.3f} vs always "
            f"{pv['always'].median():+.3f}; cond worse in {kneg}/{n} (sign p {p:.4f})")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.{{grid,coverage,mechanism,h1,walkforward,oos}}.csv + console.txt")


if __name__ == "__main__":
    main()
