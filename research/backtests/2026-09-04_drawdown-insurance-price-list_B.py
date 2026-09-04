#!/usr/bin/env python3
"""QUEUE idea 94 — drawdown-insurance-price-list (lane B, 2026-09-04).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 22 measured the book-level DD control at 1.02 pp CAGR per pp MaxDD against the static
gross lever's 0.57 on matched books and matched days, which is the first two entries of the
menu idea 74 asked for.  Complete it on the SAME harness (same books, same days, same
matched-gross control): 200d gate, 3% band, abs momentum, per-name trailing stop, entry-only
turnover budget.  Output is one ranked table RULES can quote when a drawdown budget is set."

The axis (idea 74).  Every instrument below reduces exposure when its own signal turns bad.
Each therefore buys drawdown and surrenders return.  The price of an instrument is

    rate = (CAGR_control - CAGR_arm) / (|MaxDD_control| - |MaxDD_arm|)   pp CAGR per pp MaxDD

measured on the SAME base book, the SAME days and the SAME cost.  The reference price is the
static gross lever (hold m x the book, no rule at all), which idea 66 showed is an exact,
parameter-free, path-independent dial with zero Sharpe content.  An instrument is worth its
place in RULES only if it buys drawdown MORE CHEAPLY than simply holding less.

Books (pre-chosen, never selected; all reported).  Idea 22 used the GATED books, which makes
its own subject (the 200d gate) invisible.  This run therefore takes the UNGATED book as the
common base so that every instrument — gates included — is priced as an overlay on it.  All
three sit at 75% gross so the cells are comparable.
    V1u     RULES v1's composite WITH /sqrt(vol20), top-5 at 15% each, NO 200d gate, NO vol20
            gate.  Live RULES v1 is exactly this book plus the `v1gate-rw` arm below.
    TOP20   idea 2's candidate ranking (composite, no vol scaler), top-20 at 0.75/20, ungated.
    EWall   idea 10 / 72's simplest book: equal-weight EVERY name at 75%, no ranking, ungated.
Universes: universe.json (56 names) and universe_broad.json (136).  Both always reported.

Instruments (18 treated arms per cell, ALL reported, none selected)
    gross-m       static multiplier m in 0.10..1.00 step 0.05 — the REFERENCE lever (19 pts)
    g200          per-name 200d MA gate                     (idea 57's instrument)
    band3         200d MA with a +/-3% re-entry band         (idea 57's KEEP-candidate gate)
    abs12         absolute momentum: px > px 252d ago        (idea 62's instrument)
    vol60         vol20 < 0.60                               (v1's other eligibility half)
    v1gate        200d AND vol20 < 0.60                      (the LIVE gate, as one instrument)
    stop15/25     per-name trailing stop, 15% / 25%          (idea 9)
    ddctl         book DD > 8% -> halve, reset `recover` and `high` (idea 22, for continuity)
    ebud-0.10/20  ENTRY-ONLY turnover budget: exits always execute in full, the sum of weight
                  INCREASES per rebalance is capped at B (idea 83's budget, exit-side freed)
Each gate is run in BOTH conventions, because they are different instruments:
    -dg  de-gross: a gated-out name's weight goes to CASH (the book shrinks) — the honest
         insurance form, directly comparable to a stop or to the gross lever.
    -rw  reweight: the book is rebuilt at full gross among the gated-in names only (this is
         how RULES v1 and idea 57 are actually written) — a SELECTION change, not exposure.

Tuned parameters (PROTOCOL rule 4).  ONE: the instrument family.  Every setting inside a
family (band width 3%, stop depth 15/25, budget 0.10/0.20, DD reset) is reported, and the
walk-forward selects over families only.  No number below was chosen to make a result.

Pre-registered predictions (written before any number was read)
    P1  Every instrument prices ABOVE the static gross lever (rate > slope) in the majority of
        cells: idea 22's 1.02-vs-0.57 generalises and the menu's honest top entry is "hold less".
    P2  Among the real instruments the ordering is by SPEED (idea 61's flip-rate finding):
        band3 cheapest, then abs12, then g200, with the per-name stop dearest.
    P3  The `-rw` gate arms buy little or no drawdown at all (gross is unchanged), so their
        rate is undefined or enormous — the drawdown reduction attributed to v1's gate is
        mostly a de-grossing effect that shows up only in the -dg form.
    P4  No arm converts a 4b failure into a 4b pass on both universes (this is a measurement
        run; a KEEP would be a surprise).

Walk-forward (PROTOCOL rule 8), selection fixed before any OOS number was read
    S1  In each cell, among arms that bought at least 1.0 pp of MaxDD in-sample (2009-2016),
        pick the LOWEST IS rate.  Evaluate that arm untouched on 2017-2026: OOS CAGR / Sharpe
        / MaxDD vs the base control, vs live RULES v1 and vs SPY, plus its OOS rate and its
        OOS rank among all arms of that cell.
    S2  Spearman(IS rate, OOS rate) across arms within each cell.  The menu is only usable if
        the ORDERING is stable out of sample; a price list that re-shuffles is not a price list.

Execution realism (PROTOCOL rule 2): weights decided at close t are applied at t+1, weekly
rebalance, long-only, no leverage, costs charged on realised turnover inside the loop so the
drawdown state machine and the stop see NET equity.  10 bps is the PROTOCOL point; 25 bps is
reported for every arm because the instruments differ enormously in turnover.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every
absolute CAGR is optimistic.  This run compares arms sharing a panel and the same days, so
the treatment deltas — which are the result — are far less exposed than the levels.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-04_drawdown-insurance-price-list_B"
FREQ, MAX_VOL, GROSS, NTOP, NV1, WV1 = "W", 0.60, 0.75, 20, 5, 0.15
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PCOST, COSTS = 10.0, [10.0, 25.0]
BOOKS = ["V1u", "TOP20", "EWall"]
LADDER = np.round(np.arange(0.10, 1.001, 0.05), 2)
GATES = ["g200", "band3", "abs12", "vol60", "v1gate"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 2000)


# ---------------------------------------------------------------- signals
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def gate_mask(px, gate):
    """Per-name boolean: True = the instrument allows the name to be held."""
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if gate == "g200":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * 1.03, 1.0)          # cross up through the upper band -> in
        raw = raw.mask(px < ma * 0.97, 0.0)          # cross down through the lower band -> out
        return raw.ffill().fillna(0.0) > 0.5         # sticky in between; out before warm-up
    if gate == "abs12":
        return (px > px.shift(252)).fillna(False)
    if gate == "vol60":
        return (vol20(px) < MAX_VOL).fillna(False)
    if gate == "v1gate":
        return ((px > ma) & (vol20(px) < MAX_VOL)).fillna(False)
    raise ValueError(gate)


def targets(px, book, gate=None, conv="dg"):
    """Target weights.  conv='dg' zeroes gated-out names into CASH; conv='rw' rebuilds the
    book at full gross among the gated-in names only."""
    g = gate_mask(px, gate)
    if conv == "rw" and gate is not None:
        if book == "EWall":
            e = g.astype(float)
            return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        s = composite(px)
        if book == "V1u":
            s = s / vol20(px).clip(lower=0.08) ** 0.5
            n, w = NV1, WV1
        else:
            n, w = NTOP, GROSS / NTOP
        rank = s.where(g).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * w
    W = targets(px, book) if gate is not None else None
    if W is None:                                    # the ungated base book
        if book == "EWall":
            e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
            return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        s = composite(px)
        if book == "V1u":
            s = s / vol20(px).clip(lower=0.08) ** 0.5
            n, w = NV1, WV1
        else:
            n, w = NTOP, GROSS / NTOP
        rank = s.rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * w
    return W.where(g, 0.0)                           # de-gross form


# ---------------------------------------------------------------- one simulator, every arm
def run(px, W, m=1.0, stop=None, cooldown=0, D=None, k=1.0, reset="recover",
        ebud=None, bps=PCOST, freq=FREQ):
    """engine.backtest + (static gross m) + (per-name trailing stop) + (book DD control) +
    (entry-only turnover budget).  With every instrument off it reproduces engine.backtest
    to machine precision on the evaluated slice (asserted below).

    Costs are charged inside the loop so both state machines read NET equity through t-1.
    """
    pxv = px.values
    rets = px.pct_change().fillna(0.0).values
    tgt = (W.reindex(px.index).fillna(0.0) * m).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape

    cur = np.zeros(ncol)
    peak_p = np.full(ncol, np.nan)                   # per-name running high since entry
    pending = np.zeros(ncol, dtype=bool)             # stop fired at t-1, executes now
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    cut = np.zeros(nrow, dtype=bool)
    eq, pk, armed, episodes, n_stops = 1.0, 1.0, False, 0, 0

    for i in range(nrow):
        if pending.any():                            # 1. stop exits decided at close t-1
            turn[i] += cur[pending].sum()
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        if mask[i] and i > 0:                        # 2. scheduled rebalance
            if D is not None:
                dd = eq / pk - 1.0                   # equity through close i-1: no look-ahead
                if not armed and dd < -D:
                    armed, episodes = True, episodes + 1
                elif armed and (dd >= 0.0 if reset == "high" else dd > -D / 2.0):
                    armed = False
            new = tgt[i - 1] * (k if armed else 1.0)
            s = new.sum()
            if s > 1.0:
                new = new / s
            if ebud is not None:                     # 3. entry-only budget: exits are free
                d = new - cur
                up = np.clip(d, 0.0, None).sum()
                if up > ebud:
                    new = cur + np.clip(d, None, 0.0) + np.clip(d, 0.0, None) * (ebud / up)
            turn[i] += np.abs(new - cur).sum()
            cur = new
        cut[i] = armed
        held[i] = cur
        gross_s[i] = cur.sum()
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp)
        pk = max(pk, eq)
        growth = cur * (1 + rets[i])                 # 4. drift
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
        if stop is not None:                         # 5. trailing highs / fire stops
            alive = cur > 1e-9
            p = pxv[i]
            peak_p = np.where(alive, np.fmax(np.where(np.isnan(peak_p), -np.inf, peak_p), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak_p * (1 - stop))
            if hit.any():
                pending |= hit
                n_stops += int(hit.sum())

    r = pd.Series((held * rets).sum(axis=1), index=px.index) - pd.Series(turn, index=px.index) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=px.index), gross=pd.Series(gross_s, index=px.index),
                cut=pd.Series(cut, index=px.index), episodes=episodes, n_stops=n_stops)


# ---------------------------------------------------------------- metric helpers
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def margins(r, bars):
    h1, h2 = halves(r)
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=0.60 * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - 0.70 * bars["scagr"])


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def window(r, which):
    return r.loc[:IS_END] if which == "IS" else (r.loc[OOS_START:] if which == "OOS" else r)


def price(rc, ra, lad_slope):
    """The menu entry: pp of CAGR surrendered per pp of MaxDD bought, vs the control."""
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    rate = dc / dd if dd > 0.10 else np.nan          # < 0.1 pp bought -> no meaningful price
    return dict(dCAGR=dc, dMaxDD=dd, rate=rate, dSharpe=ma["Sharpe"] - mc["Sharpe"],
                dominated=(rate >= lad_slope) if np.isfinite(rate) else np.nan)


def ladder_slope(L, col_dd="MaxDD", col_c="CAGR"):
    x = L[col_dd].abs().values * 100.0
    y = L[col_c].values * 100.0
    return float(np.polyfit(x, y, 1)[0])


def matched_dd(L, target_dd, col_dd="MaxDD", col_c="CAGR"):
    """CAGR of the static-gross ladder at the m whose MaxDD equals the arm's, by linear
    interpolation on the ladder (MaxDD is monotone in m).  The decisive control: if simply
    holding less reaches the same drawdown at a HIGHER CAGR, the instrument is dominated."""
    d = L.sort_values(col_dd, key=lambda s: s.abs())
    x = d[col_dd].abs().values * 100.0
    y = d[col_c].values * 100.0
    t = abs(target_dd) * 100.0
    if t < x[0] or t > x[-1]:
        return np.nan
    return float(np.interp(t, x, y))


# ---------------------------------------------------------------- arms
def arm_specs():
    """(name, kind, kwargs-for-run, target-spec).  Order is the print order."""
    A = [("control", "ctl", dict(), (None, "dg"))]
    for g in GATES:
        for conv in ("dg", "rw"):
            A.append((f"{g}-{conv}", "gate", dict(), (g, conv)))
    A += [("stop15", "stop", dict(stop=0.15), (None, "dg")),
          ("stop25", "stop", dict(stop=0.25), (None, "dg")),
          ("ddctl-8/.5/recover", "dd", dict(D=0.08, k=0.5, reset="recover"), (None, "dg")),
          ("ddctl-8/.5/high", "dd", dict(D=0.08, k=0.5, reset="high"), (None, "dg")),
          ("ebud-0.10", "bud", dict(ebud=0.10), (None, "dg")),
          ("ebud-0.20", "bud", dict(ebud=0.20), (None, "dg"))]
    return A


# ---------------------------------------------------------------- one universe
def do_universe(uname, kw):
    px = load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = bars_of(spy)
    ms = metrics(spy)
    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}

    print("\n" + "=" * 200)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS Sharpe {bars['soos']:.3f}")
    print(f"live RULES v1 @10bps: CAGR {metrics(v1_net[10.0])['CAGR']:.2%}  "
          f"Sharpe {metrics(v1_net[10.0])['Sharpe']:.3f}  MaxDD {metrics(v1_net[10.0])['MaxDD']:.2%}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f}(H1)/{bars['s2']:.3f}(H2)/{bars['soos']:.3f}(OOS), "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    print("=" * 200)

    # ---- harness sanity: every instrument off must reproduce engine.backtest exactly
    worst = 0.0
    for b in BOOKS:
        W = targets(px, b)
        a = run(px, W, bps=PCOST)["r"].loc[start:]
        e = backtest(px, W, cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    print(f"ENGINE-EQUIVALENCE (control vs engine.backtest @{PCOST:.0f}bps): max|diff| = {worst:.3e} "
          f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — results below are unsafe'})")

    rows, rets, ladders = [], {}, {}
    for b in BOOKS:
        # ---- the reference lever: static-gross ladder (no rule at all), per cost
        for c in COSTS:
            lad = []
            for m_ in LADDER:
                res = run(px, targets(px, b), m=m_, bps=c)
                r = res["r"].loc[start:]
                mm = metrics(r)
                lad.append(dict(m=m_, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                gross=res["gross"].loc[start:].mean(),
                                TO=res["to"].loc[start:].sum() / mm["Years"],
                                IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"]))
            ladders[(b, c)] = pd.DataFrame(lad)

        # ---- every treated arm
        for name, kind, kwargs, (g, conv) in arm_specs():
            W = targets(px, b, g, conv)
            for c in COSTS:
                res = run(px, W, bps=c, **kwargs)
                r = res["r"].loc[start:]
                rets[(b, name, c)] = r
                mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
                h1, h2 = halves(r)
                mg = margins(r, bars)
                yr = (1 + r).groupby(r.index.year).prod() - 1
                rows.append(dict(
                    uni=uname, book=b, arm=name, kind=kind, cost=c,
                    CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    TO=res["to"].loc[start:].sum() / mm["Years"],
                    gross=res["gross"].loc[start:].mean(),
                    cut_days=res["cut"].loc[start:].mean(), stops=res["n_stops"],
                    y2020=yr.get(2020, np.nan), y2022=yr.get(2022, np.nan),
                    m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                    p4b=all(v > 0 for v in mg.values()),
                    f4b=",".join([kk for kk, v in mg.items() if not v > 0]) or "-",
                    p4a=pass4a(r, v1_net[c])))
    df = pd.DataFrame(rows)

    print(f"\nFULL GRID {uname} — {len(df)} arm-points, ALL reported "
          f"(3 books x {len(arm_specs())} arms x {len(COSTS)} costs)")
    print(df[["book", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
              "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "y2020", "y2022", "p4a", "p4b", "f4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    for c in COSTS:
        print(f"\nSTATIC-GROSS LADDER {uname} @{c:.0f}bps — {len(LADDER)} points per book, ALL reported")
        print(pd.concat([ladders[(b, c)].assign(book=b) for b in BOOKS])
              [["book", "m", "gross", "CAGR", "Sharpe", "MaxDD", "TO", "IS_CAGR", "IS_MaxDD",
                "OOS_CAGR", "OOS_MaxDD"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return px, start, df, rets, ladders, bars, spy, v1_net


# ---------------------------------------------------------------- the price list
def price_list(uname, df, rets, ladders):
    out = []
    for b in BOOKS:
        for c in COSTS:
            L = ladders[(b, c)]
            slope = {w: ladder_slope(L, f"{p}MaxDD", f"{p}CAGR")
                     for w, p in (("full", ""), ("IS", "IS_"), ("OOS", "OOS_"))}
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in arm_specs():
                if name == "control":
                    continue
                ra = rets[(b, name, c)]
                p_full = price(rc, ra, slope["full"])
                p_is = price(window(rc, "IS"), window(ra, "IS"), slope["IS"])
                p_oos = price(window(rc, "OOS"), window(ra, "OOS"), slope["OOS"])
                am = metrics(ra)
                gm = matched_dd(L, am["MaxDD"])
                row = df[(df.book == b) & (df.arm == name) & (df.cost == c)].iloc[0]
                out.append(dict(
                    uni=uname, book=b, cost=c, arm=name, kind=kind,
                    dCAGR=p_full["dCAGR"], dMaxDD=p_full["dMaxDD"], rate=p_full["rate"],
                    lever=slope["full"], dominated=p_full["dominated"],
                    dSharpe=p_full["dSharpe"], gross=row.gross, TO=row.TO,
                    md_ctl_CAGR=gm, vs_matchedDD=(am["CAGR"] * 100.0 - gm) if np.isfinite(gm) else np.nan,
                    IS_rate=p_is["rate"], IS_dMaxDD=p_is["dMaxDD"], IS_lever=slope["IS"],
                    OOS_rate=p_oos["rate"], OOS_dMaxDD=p_oos["dMaxDD"], OOS_lever=slope["OOS"],
                    p4b=row.p4b, p4a=row.p4a))
    return pd.DataFrame(out)


def walk_forward(P, df, rets, bars, spy, v1_net, uname):
    """S1: cheapest IS rate among arms that bought >= 1pp of IS drawdown; evaluated on OOS."""
    print(f"\nRULE 8 WALK-FORWARD {uname} — parameters (instrument family) chosen on "
          f"2009-{IS_END[:4]} only, evaluated untouched on {OOS_START[:4]}-2026")
    spy_o, out = metrics(spy.loc[OOS_START:]), []
    for b in BOOKS:
        for c in COSTS:
            cell = P[(P.book == b) & (P.cost == c)]
            elig = cell[(cell.IS_dMaxDD >= 1.0) & np.isfinite(cell.IS_rate)]
            v1_o = metrics(v1_net[c].loc[OOS_START:])
            ctl_o = metrics(rets[(b, "control", c)].loc[OOS_START:])
            if elig.empty:
                out.append(dict(uni=uname, book=b, cost=c, pick="NOTHING (no arm bought >=1pp IS)",
                                IS_rate=np.nan, OOS_rate=np.nan, OOS_rank=np.nan,
                                OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                ctl_CAGR=ctl_o["CAGR"], ctl_Sharpe=ctl_o["Sharpe"], ctl_MaxDD=ctl_o["MaxDD"],
                                v1_Sharpe=v1_o["Sharpe"], spy_Sharpe=spy_o["Sharpe"]))
                continue
            pick = elig.sort_values("IS_rate").iloc[0]
            ro = rets[(b, pick.arm, c)].loc[OOS_START:]
            mo = metrics(ro)
            oos_ranked = cell[np.isfinite(cell.OOS_rate) & (cell.OOS_dMaxDD >= 1.0)] \
                .sort_values("OOS_rate").arm.tolist()
            out.append(dict(
                uni=uname, book=b, cost=c, pick=pick.arm, IS_rate=pick.IS_rate,
                OOS_rate=pick.OOS_rate,
                OOS_rank=(oos_ranked.index(pick.arm) + 1) if pick.arm in oos_ranked else np.nan,
                n_oos_arms=len(oos_ranked),
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                ctl_CAGR=ctl_o["CAGR"], ctl_Sharpe=ctl_o["Sharpe"], ctl_MaxDD=ctl_o["MaxDD"],
                v1_CAGR=v1_o["CAGR"], v1_Sharpe=v1_o["Sharpe"], v1_MaxDD=v1_o["MaxDD"],
                spy_CAGR=spy_o["CAGR"], spy_Sharpe=spy_o["Sharpe"], spy_MaxDD=spy_o["MaxDD"],
                rho=spearman(cell.IS_rate.values, cell.OOS_rate.values)))
    W = pd.DataFrame(out)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return W


# ---------------------------------------------------------------- main
def main():
    parts = []
    for uname, kw in (("universe.json(56)", dict()), ("universe_broad.json", dict(broad=True))):
        px, start, df, rets, ladders, bars, spy, v1_net = do_universe(uname, kw)
        P = price_list(uname, df, rets, ladders)
        print(f"\nPRICE LIST {uname} — pp of CAGR surrendered per pp of MaxDD bought, vs the SAME "
              f"base book on the SAME days.  `lever` = static-gross reference price in that cell.")
        print(P[["book", "cost", "arm", "dCAGR", "dMaxDD", "rate", "lever", "dominated",
                 "dSharpe", "gross", "TO", "vs_matchedDD", "IS_rate", "OOS_rate", "p4a", "p4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        W = walk_forward(P, df, rets, bars, spy, v1_net, uname)
        parts.append((uname, df, P, W))

    G = pd.concat([p[2] for p in parts], ignore_index=True)
    A = pd.concat([p[1] for p in parts], ignore_index=True)
    Wf = pd.concat([p[3] for p in parts], ignore_index=True)
    G.to_csv(ROOT / "research" / "backtests" / f"{STEM}.pricelist.csv", index=False)
    A.to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)

    print("\n" + "=" * 200)
    print("THE MENU — every instrument, both universes, all three books, ranked by median price")
    print("(pp of CAGR surrendered per pp of MaxDD bought at 10 bps; lower = cheaper insurance)")
    print("=" * 200)
    for c in COSTS:
        sub = G[G.cost == c]
        agg = sub.groupby("arm").agg(
            cells_priced=("rate", lambda s: int(np.isfinite(s).sum())),
            median_rate=("rate", "median"), mean_rate=("rate", "mean"),
            min_rate=("rate", "min"), max_rate=("rate", "max"),
            median_dMaxDD=("dMaxDD", "median"), median_dCAGR=("dCAGR", "median"),
            median_dSharpe=("dSharpe", "median"),
            beats_lever=("dominated", lambda s: int((s == False).sum())),
            n_dom=("dominated", lambda s: int(np.isfinite(pd.to_numeric(s, errors="coerce")).sum())),
            median_TO=("TO", "median"), median_gross=("gross", "median"),
            median_vs_matchedDD=("vs_matchedDD", "median"),
        ).sort_values("median_rate")
        lev = sub.groupby("book").lever.median()
        print(f"\n--- {c:.0f} bps ---   static-gross lever price by book: "
              + "  ".join(f"{b} {lev[b]:.3f}" for b in BOOKS)
              + f"   (median {sub.lever.median():.3f})")
        print(agg.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\nPREDICTION SCORECARD")
    s10 = G[G.cost == PCOST]
    beat = s10[s10.dominated == False]
    print(f"  P1 every instrument prices ABOVE the static lever in the majority of cells: "
          f"{len(beat)} of {int(np.isfinite(s10.rate).sum())} priced arm-cells beat the lever "
          f"({'REFUTED' if len(beat) > np.isfinite(s10.rate).sum()/2 else 'CONFIRMED'})")
    med = s10.groupby("arm").rate.median().sort_values()
    print(f"  P2 speed ordering (band3 < abs12 < g200 < stop): observed order of the -dg gates "
          f"and stops = {[a for a in med.index if a.endswith('-dg') or a.startswith('stop')]}")
    rw = s10[s10.arm.str.endswith("-rw")]
    print(f"  P3 -rw gates buy little drawdown: median dMaxDD(rw) = {rw.dMaxDD.median():.2f} pp "
          f"vs dg = {s10[s10.arm.str.endswith('-dg')].dMaxDD.median():.2f} pp")
    both = A[(A.cost == PCOST) & A.p4b].groupby("arm").uni.nunique()
    print(f"  P4 arms passing 4b on BOTH universes @10bps: "
          f"{sorted(both[both == 2].index.tolist()) or 'none'}")
    print(f"\n  4a passes @10bps (vs live RULES v1): "
          f"{sorted(set(A[(A.cost==PCOST) & A.p4a].arm)) or 'none'}")
    print(f"  Walk-forward rank stability: median Spearman(IS rate, OOS rate) across the 12 cells "
          f"= {Wf.rho.median():.3f}  (per-cell: {[round(x,2) for x in Wf.rho.dropna().tolist()]})")
    print(f"\nWrote {STEM}.pricelist.csv and {STEM}.grid.csv")


if __name__ == "__main__":
    main()
