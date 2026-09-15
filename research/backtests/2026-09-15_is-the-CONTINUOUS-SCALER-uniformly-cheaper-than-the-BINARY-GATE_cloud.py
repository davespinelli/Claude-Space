#!/usr/bin/env python3
"""QUEUE idea 902 — is-the-CONTINUOUS-SCALER-uniformly-CHEAPER-than-the-BINARY-GATE-at-matched-effect
(cloud, 2026-09-15).

QUESTION (pre-registered, verbatim from QUEUE.md idea 902)
    "idea 870 priced the textbook continuous vol target for the first time in this record and it
     clears 4b on U56 at gate turnover 0.71/yr against CORR-HI's 2.16 for a comparable Sharpe,
     with the smallest cost decay of 3,456 arms.  Test whether continuous-vs-binary is a general
     cost saving across every gate family and state, at matched realised gross.
     Max 2 params (scaler form, cost rung)."

WHAT "CHEAPER" HAS TO MEAN, declared before any number was read
    A de-grossing overlay costs money in exactly one place: the switch cost it pays when the
    multiplier moves (idea 399's convention, |dm| * gross * bps).  So an overlay is CHEAPER than
    a twin if, AT THE SAME REALISED GROSS, it moves the multiplier less.  Two consequences that
    this run reports separately, because conflating them is how a cost claim becomes a
    performance claim:
      COST CHANNEL       gate turnover, and Sharpe(0 bps) - Sharpe(25 bps) = the cost decay.
      GROSS-PATH CHANNEL Sharpe at 0 bps, where no cost is paid at all.  Any difference here is
                         NOT a cost saving: it is a different bet with the same average exposure.
    H_COST is about the first.  H_FREE below is the falsifier for the second.

THE HYPOTHESES, written out in full BEFORE any number below was read
    H_CHEAP   the continuous form moves the multiplier less: at matched mean multiplier, gate
              turnover(CONT) < gate turnover(BINARY) in >= 90% of cells, in EVERY one of the six
              state x side families.  "Uniformly" is the word the queue used and it is tested as
              written: a single family below 90% falsifies it.
    H_COST    the saving reaches the P&L: median dSharpe(CONT - BINARY) at 25 bps > 0 in all six
              families, and larger at 25 bps than at 0 bps in all six.
    H_FREE    the advantage is a COST advantage and nothing else: |median dSharpe at 0 bps|
              <= 0.02 in all six families.  If the continuous form also wins at ZERO cost, the
              queue's framing is wrong — it is a better bet, not a cheaper one, and the record
              must stop calling it a cost saving.
    Declared before running: H_CHEAP is the mechanical claim, H_FREE is the one that decides
    whether "cheaper" is the right word.

THE BOOKS AND OVERLAY MECHANICS, IMPORTED not re-invented (idea 870 lane B, verbatim)
    base EWALL   equal-weight every eligible name (above 200d MA, vol20 < 0.60) at gross g,
                 weekly, 10 bps — idea 870's own base, so its committed arm reproduces (G1).
    base TOP20   the 2026-09-04 shelf KEEP-4b book: composite with NO vol scaler, top 20 by rank,
                 equal weight g/20, shortfall to cash never respread, MONTHLY.  Carried as a
                 second reported base because that is the book the record is deciding capital on.
    overlay      r_overlaid[t] = m_eff[t] * r_base[t] - |dm_eff[t]| * gross * bps / 1e4, with
                 m_eff the t+1-aligned multiplier path (idea 399's switch cost).
    states       CORR (20d average pairwise correlation via the index/name variance identity),
                 PORTVOL (20d realised vol of the EW book), NAMEVOL (20d average name vol).
                 All three verbatim from idea 870 / 815 / 606.

THE TWO TUNED PARAMETERS (the only two; every value of both is reported)
    P1 SCALER FORM  BINARY  m = 1 on the non-tail days, 1 - depth on the tail days (the record's
                            gate, idea 606/815 verbatim).
                    RAMP    the SAME firing set, graded: m = 1 - depth * clip(encroachment, 0, 1)
                            where encroachment is the distance past the q-quantile threshold as a
                            fraction of the distance from that threshold to the rolling extreme
                            of the same window.  Isolates STEP vs GRADED with the support held
                            fixed.
                    RATIO   the textbook continuous target, idea 870's VTCONT generalised from
                            PORTVOL to every state: HI m = clip(thr/st, 1-depth, 1),
                            LO m = clip(st/thr, 1-depth, 1).  Its support is NOT the gate's.
    P2 COST RUNG    {0, 10, 25} bps.  All three read on every arm; none selected.
    AUDIT axes, printed in full and never selected on: q {0.07, 0.12, 0.17}, w {252, 504, 1008,
    2016}, depth {0.25, 0.50, 1.00}, cadence {D, W}, gross {0.75, 1.00}, base {EWALL, TOP20},
    state {CORR, PORTVOL, NAMEVOL}, side {LO, HI}.

MATCHED REALISED GROSS — the whole comparison rests on this, so it is exact, not approximate
    For each cell, the continuous path is rescaled by a single scalar a:
        m' = 1 - a * (1 - m_cont),   a = (1 - mean(m_bin)) / (1 - mean(m_cont))
    which makes mean(m') == mean(m_bin) EXACTLY (linearity), i.e. the two overlays hold the same
    average gross over the sample.  a is reported.  A cell is INFEASIBLE and is dropped, counted,
    and named if the rescale would drive the multiplier below 0 (a * (1 - min m_cont) > 1) or if
    the binary twin never fires.  Rescaling changes the continuous form's depth, not its shape;
    depth is an audit axis on both arms, so nothing is being tuned by the match.

PROTOCOL rule 8 walk-forward (required, read once)
    IS = start .. 2016-12-31, OOS = 2017-01-01 .. end.  Selector declared here before the run:
    within EACH form separately, take the arm with the highest IS Sharpe at the PROTOCOL cell
    (10 bps, base EWALL, matched gross).  OOS CAGR / Sharpe / MaxDD for those three picks is then
    read ONCE against RULES v2 (live) and SPY, with BOTH KEEP paths evaluated.

GATES, printed before any hypothesis is read
    G1  idea 870's committed VTCONT-HI arm (U56, q 0.17, w 252, depth 0.50, cadence W, g 1.00)
        rebuilds here: 13.66% / 1.098 / -18.79% full, gate turnover 0.71/yr, and CORR-HI's 2.16.
    G2  a never-firing multiplier reproduces the ungated base exactly (max|dr| < 1e-12).
    G3  the match is exact: max |mean(m') - mean(m_bin)| < 1e-12 over every feasible cell.
    G4  support identity: BINARY and RAMP fire on exactly the same days, every cell (0 mismatches).
    G5  the fast Sharpe used across the grid equals engine.metrics()['Sharpe'].

CAVEATS carried, not buried
    * SURVIVORSHIP.  research/universe.json is the CURRENT constituent list (idea 54), so CAGR and
      drawdown LEVELS are optimistic throughout.  The CONT-minus-BINARY differencing at matched
      gross is the durable part; the levels are not.
    * The grid is dense and heavily overlapping (neighbouring q / w cells share most of their
      firing days), so counts like "x of 432" are sensitivities, not independent trials.
    * RAMP's encroachment anchor is the rolling extreme of the same window, so it is sensitive to
      a single outlier day in w; that is a property of the form as declared, not a bug.
    * For CORR the state can be negative, so the RATIO form's ratio can be negative; the clip at
      1 - depth handles it and those days are simply at full depth. Flagged, not hidden.
    * 2020 and 2022 are the only real stress episodes in the panel.
    * Rule 6: nothing here is a rules change; a rules change is a Sunday-review decision.

Deterministic, standalone, committed caches only, never yfinance.  Modifies nothing.
"""
import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, metrics, rebalance_mask                  # noqa: E402

pd.set_option("display.width", 230)

FREQ, MAX_VOL, SMOOTH = "W", 0.60, 20
QS = [0.07, 0.12, 0.17]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
GROSSES = [0.75, 1.00]
RUNGS = [0, 10, 25]
STATES = ["CORR", "PORTVOL", "NAMEVOL"]
SIDES = ["LO", "HI"]
FORMS = ["BINARY", "RAMP", "RATIO"]
SPLIT = "2017-01-01"
N_BOOK = 20


# ---------------------------------------------------------- primitives (idea 870 lane B, verbatim)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def top20_weights(px, gross):
    """The 2026-09-04 shelf KEEP-4b book (idea 879 / 897 verbatim): monthly, cash never respread."""
    comp, above, vol20 = score(px, vol_scale=False)
    elig = comp.where(above & (vol20 < MAX_VOL))
    m = pd.Series(px.index.to_period("M"), index=px.index)
    dates = px.index[(m != m.shift(-1)).values]
    W = ((elig.rank(axis=1, ascending=False) <= N_BOOK).astype(float) * (gross / N_BOOK)).loc[dates]
    return W.reindex(px.index).ffill().fillna(0.0)


def fast_sharpe(v):
    v = np.asarray(v, float)
    sd = v.std(ddof=1)
    return v.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def state_namevol(px):
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_portvol(px):
    return px.pct_change().mean(axis=1).rolling(SMOOTH).std() * np.sqrt(252)


def state_corr(px):
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"CORR": state_corr, "PORTVOL": state_portvol, "NAMEVOL": state_namevol}


def _cadence(m, cadence, idx):
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def mult_binary(st, thr, side, depth, cadence, idx, ext=None):
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    return _cadence(pd.Series(1.0, index=idx).where(~fire, 1.0 - depth), cadence, idx)


def mult_ramp(st, thr, side, depth, cadence, idx, ext=None):
    """Same firing set as BINARY, graded by how far past the threshold the state has gone,
    as a fraction of the threshold-to-rolling-extreme distance of the same window."""
    span = (thr - ext) if side == "LO" else (ext - thr)
    enc = ((thr - st) if side == "LO" else (st - thr)) / span.replace(0, np.nan)
    enc = enc.clip(lower=0.0, upper=1.0)
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = (1.0 - depth * enc).where(fire, 1.0)
    return _cadence(m.where(st.notna() & thr.notna(), 1.0).reindex(idx).fillna(1.0), cadence, idx)


def mult_ratio(st, thr, side, depth, cadence, idx, ext=None):
    """idea 870's VTCONT, generalised from PORTVOL to every state."""
    ratio = (thr / st) if side == "HI" else (st / thr)
    m = ratio.clip(upper=1.0).clip(lower=1.0 - depth)
    return _cadence(m.where(st.notna() & thr.notna(), 1.0).reindex(idx).fillna(1.0), cadence, idx)


MULT_FN = {"BINARY": mult_binary, "RAMP": mult_ramp, "RATIO": mult_ratio}


def apply_eff(r_base, m_eff, gross, cost_bps):
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def gate_turnover(m_eff):
    return float(np.abs(np.diff(m_eff, prepend=m_eff[0])).sum() * 252 / len(m_eff))


def pack(r, idx):
    m = metrics(pd.Series(r, index=idx))
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def keep_paths(c, s, dd, h1, h2, bl, spy):
    a = (h1 > bl["h1"]) and (h2 > bl["h2"]) and (dd >= bl["dd"])
    b = (h1 > spy["h1"]) and (h2 > spy["h2"]) and (dd >= 0.60 * spy["dd"]) and (c >= 0.70 * spy["c"])
    return a, b


# ------------------------------------------------------------------------------ panel and bases
px = load_universe()
core = px.drop(columns=["SPY"], errors="ignore")
idx = px.index
ii = idx[idx >= idx[260]]
oos = np.asarray(ii >= pd.Timestamp(SPLIT))
isw = ~oos

states = {s: STATE_FN[s](core) for s in STATES}
BASE = {("EWALL", g): backtest(core, ewall_weights(core, g), cost_bps=10, freq=FREQ)["returns"].loc[ii]
        for g in GROSSES}
BASE.update({("TOP20", g): backtest(core, top20_weights(core, g), cost_bps=10, freq="M")["returns"].loc[ii]
             for g in GROSSES})

spy_v = px["SPY"].pct_change().fillna(0.0).loc[ii].values
sc, ss, sd = pack(spy_v, ii)
sh1, sh2 = halves(spy_v)
soc, sos_, sod = pack(spy_v[oos], ii[oos])
soh1, soh2 = halves(spy_v[oos])
bl_r = backtest(core, rules_v2_weights(core), cost_bps=10, freq=FREQ)["returns"].loc[ii]
bc, bs, bd = pack(bl_r.values, ii)
bh1, bh2 = halves(bl_r.values)
boc, bos_, bod = pack(bl_r.values[oos], ii[oos])
boh1, boh2 = halves(bl_r.values[oos])
SPYD = dict(c=sc, s=ss, dd=sd, h1=sh1, h2=sh2)
SPYO = dict(c=soc, s=sos_, dd=sod, h1=soh1, h2=soh2)
BLD = dict(c=bc, s=bs, dd=bd, h1=bh1, h2=bh2)
BLO = dict(c=boc, s=bos_, dd=bod, h1=boh1, h2=boh2)

# ------------------------------------------------------------------------------ build every arm
print("=" * 112)
print("GATES (printed before any hypothesis is read)")
print("=" * 112)

rb_e75 = BASE[("EWALL", 0.75)].values
ones = np.ones(len(rb_e75))
g2 = float(np.max(np.abs(apply_eff(rb_e75, ones, 0.75, 10) - rb_e75)))
print(f"G2 never-firing multiplier == ungated base   max|dr| = {g2:.3e}   "
      f"[{'PASS' if g2 < 1e-12 else 'FAIL'}]")
g5 = abs(fast_sharpe(rb_e75) - metrics(BASE[("EWALL", 0.75)])["Sharpe"])
print(f"G5 fast Sharpe == engine.metrics Sharpe      |d|     = {g5:.3e}   "
      f"[{'PASS' if g5 < 1e-10 else 'FAIL'}]")

# ---- G1: idea 870's committed VTCONT-HI arm, UNMATCHED, read before the grid is built --------
_q, _w, _d, _cad, _g = 0.17, 252, 0.50, "W", 1.00
_mp = max(60, _w // 4)
_g1 = {}
for _s, _form in (("PORTVOL", "RATIO"), ("CORR", "BINARY")):
    _st = states[_s]
    _th = _st.rolling(_w, min_periods=_mp).quantile(1 - _q)
    _ex = _st.rolling(_w, min_periods=_mp).max()
    _m = MULT_FN[_form](_st, _th, "HI", _d, _cad, idx, _ex).shift(1).fillna(1.0).loc[ii].values
    _r = apply_eff(BASE[("EWALL", _g)].values, _m, _g, 10)
    _g1[(_s, _form)] = (*pack(_r, ii), gate_turnover(_m))
_vt, _ch = _g1[("PORTVOL", "RATIO")], _g1[("CORR", "BINARY")]
_ok = abs(_vt[0] - 0.1366) <= 0.0010 and abs(_vt[1] - 1.098) <= 0.02 and abs(_vt[3] - 0.71) <= 0.05
print(f"G1 idea 870 VTCONT-HI arm (U56 q.17 w252 d.50 W g1.00, UNMATCHED): "
      f"{_vt[0]:.2%} / {_vt[1]:.3f} / {_vt[2]:.2%}  gate turnover {_vt[3]:.2f}/yr  "
      f"vs memo 13.66% / 1.098 / -18.79% @ 0.71   [{'PASS' if _ok else 'FAIL'}]")
print(f"   CORR-HI binary, same cell: gate turnover {_ch[3]:.2f}/yr vs memo 2.16   "
      f"[{'PASS' if abs(_ch[3] - 2.16) <= 0.05 else 'FAIL'}]   "
      f"({_ch[0]:.2%} / {_ch[1]:.3f} / {_ch[2]:.2%})")

rows, raw, match_err, support_bad, infeasible, n_cells = [], [], 0.0, 0, 0, 0
INFEAS = []
for q, w in product(QS, WS):
    mp = max(60, w // 4)
    thr, ext = {}, {}
    for s in STATES:
        st = states[s]
        thr[(s, "LO")] = st.rolling(w, min_periods=mp).quantile(q)
        thr[(s, "HI")] = st.rolling(w, min_periods=mp).quantile(1 - q)
        ext[(s, "LO")] = st.rolling(w, min_periods=mp).min()
        ext[(s, "HI")] = st.rolling(w, min_periods=mp).max()
    for s, side, depth, cad in product(STATES, SIDES, DEPTHS, CADENCES):
        st, th, ex = states[s], thr[(s, side)], ext[(s, side)]
        eff = {}
        for form in FORMS:
            m = MULT_FN[form](st, th, side, depth, cad, idx, ex)
            eff[form] = m.shift(1).fillna(1.0).loc[ii].values
        n_cells += 1
        fb, fr = eff["BINARY"] < 1.0, eff["RAMP"] < 1.0
        support_bad += int((fb != fr).sum() > 0)
        gbar_b = float(eff["BINARY"].mean())

        # --- UNMATCHED record, kept for EVERY cell: this is the reading idea 870 published ---
        for form in FORMS:
            raw.append(dict(state=s, side=side, family=f"{s}-{side}", form=form, q=q, w=w,
                            depth=depth, cadence=cad, gbar=float(eff[form].mean()),
                            gt=gate_turnover(eff[form]), rate=float((eff[form] < 1.0).mean())))

        # --- matched-gross arms, where the rescale is feasible ---
        if gbar_b >= 1.0:                       # binary never fires -> nothing to match
            infeasible += 1
            INFEAS.append(dict(state=s, side=side, q=q, w=w, depth=depth, cadence=cad,
                               reason="binary never fires", form="-", alpha=np.nan))
            continue
        keep = {"BINARY": eff["BINARY"]}
        ok = True
        for form in ("RAMP", "RATIO"):
            mc = eff[form]
            den = 1.0 - float(mc.mean())
            if den <= 1e-12:
                ok = False
                INFEAS.append(dict(state=s, side=side, q=q, w=w, depth=depth, cadence=cad,
                                   reason="continuous never de-grosses", form=form, alpha=np.nan))
                break
            a = (1.0 - gbar_b) / den
            mm = 1.0 - a * (1.0 - mc)
            if mm.min() < 0.0:
                ok = False
                INFEAS.append(dict(state=s, side=side, q=q, w=w, depth=depth, cadence=cad,
                                   reason="rescale drives multiplier below 0", form=form, alpha=a))
                break
            match_err = max(match_err, abs(float(mm.mean()) - gbar_b))
            keep[form] = mm
            keep[form + "_alpha"] = a
        if not ok:
            infeasible += 1
            continue
        for form in FORMS:
            me = keep[form]
            for base_name, g in product(("EWALL", "TOP20"), GROSSES):
                rb = BASE[(base_name, g)].values
                rr = {c: apply_eff(rb, me, g, c) for c in RUNGS}
                c_, s_, d_ = pack(rr[10], ii)
                h1, h2 = halves(rr[10])
                oc, os_, od = pack(rr[10][oos], ii[oos])
                oh1, oh2 = halves(rr[10][oos])
                a4, b4 = keep_paths(c_, s_, d_, h1, h2, BLD, SPYD)
                oa4, ob4 = keep_paths(oc, os_, od, oh1, oh2, BLO, SPYO)
                rows.append(dict(
                    base=base_name, state=s, side=side, family=f"{s}-{side}", form=form,
                    q=q, w=w, depth=depth, cadence=cad, gross=g,
                    gbar=float(me.mean()), gt=gate_turnover(me),
                    alpha=keep.get(form + "_alpha", 1.0),
                    S0=fast_sharpe(rr[0]), S10=fast_sharpe(rr[10]), S25=fast_sharpe(rr[25]),
                    decay=fast_sharpe(rr[0]) - fast_sharpe(rr[25]),
                    CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                    IS_S=fast_sharpe(rr[10][isw]), OOS_CAGR=oc, OOS_S=os_, OOS_MaxDD=od,
                    OOS_H1=oh1, OOS_H2=oh2, keep4a=a4, keep4b=b4, oos4a=oa4, oos4b=ob4))

A = pd.DataFrame(rows)
RAW = pd.DataFrame(raw)

print(f"G3 matched mean multiplier exact           max|d| = {match_err:.3e}   "
      f"[{'PASS' if match_err < 1e-12 else 'FAIL'}]")
print(f"G4 BINARY and RAMP share their firing set  cells with a mismatch: {support_bad} of "
      f"{n_cells}   [{'PASS' if support_bad == 0 else 'FAIL'}]")
print(f"   cells built {n_cells}; matched {n_cells - infeasible}; unmatchable {infeasible}; "
      f"matched arms {len(A)}; unmatched (as-published) rows {len(RAW)}")

print()
print("=" * 112)
print("WHY 300-ODD CELLS CANNOT BE MATCHED — the sample the matched contrast is read on")
print("=" * 112)
IF = pd.DataFrame(INFEAS)
if len(IF):
    print(IF.groupby(["reason", "form"]).size().to_string())
    print("\nunmatchable cells by depth and side (a binary gate at depth d removes d of the gross "
          "on its firing days; a continuous scaler that de-grosses much less needs alpha >> 1 to "
          "match it, which drives its deepest day below zero):")
    print(pd.crosstab([IF["depth"], IF["side"]], IF["state"]).to_string())
    print(f"alpha required on the 'below 0' cells: median {IF['alpha'].median():.2f}, "
          f"max {IF['alpha'].max():.2f}")
print("\nThe matched contrast below is therefore read on the SHALLOW end of the depth axis only. "
      "That is a real restriction on the answer and is stated, not hidden: at depths where a "
      "continuous scaler CAN be made to hold the same average gross as the binary gate, it does "
      "not do so more cheaply.  At the deeper end it cannot be matched at all.")

print()
print("=" * 112)
print("AS-PUBLISHED (UNMATCHED) READING — what idea 870's 0.71-vs-2.16 comparison actually is")
print("(same cell, no rescale; this is the reading the queue's premise rests on)")
print("=" * 112)
U = RAW.pivot_table(index=["state", "side", "q", "w", "depth", "cadence"], columns="form",
                    values=["gt", "gbar"])
urows = []
for form in ("RAMP", "RATIO"):
    d = pd.DataFrame({"d_gt": U[("gt", form)] - U[("gt", "BINARY")],
                      "d_gbar": U[("gbar", form)] - U[("gbar", "BINARY")]}).reset_index()
    d["form"] = form
    urows.append(d)
UU = pd.concat(urows, ignore_index=True)
print(UU.groupby(["form", "state", "side"]).agg(
    n=("d_gt", "size"), gt_cheaper=("d_gt", lambda x: (x < 0).mean()),
    med_d_gt=("d_gt", "median"), med_d_gbar=("d_gbar", "median")).to_string(
    float_format=lambda x: f"{x:.4f}"))
print("\nd_gbar > 0 means the continuous form HOLDS MORE GROSS than the binary gate it is being "
      "compared with — i.e. it de-grosses less.  An overlay that barely moves is trivially "
      "low-turnover; that is the whole of the unmatched turnover gap.")

# --------------------------------------------------------------------------- the matched contrast
print()
print("=" * 112)
print("MATCHED-GROSS CONTRAST — CONT minus BINARY, paired within every cell")
print("(pairing keys: base, state, side, q, w, depth, cadence, gross; nothing selected)")
print("=" * 112)
keys = ["base", "state", "side", "q", "w", "depth", "cadence", "gross"]
piv = A.pivot_table(index=keys, columns="form",
                    values=["gt", "S0", "S10", "S25", "decay", "gbar"])
pairs = []
for form in ("RAMP", "RATIO"):
    d = pd.DataFrame({
        "d_gt": piv[("gt", form)] - piv[("gt", "BINARY")],
        "d_S0": piv[("S0", form)] - piv[("S0", "BINARY")],
        "d_S10": piv[("S10", form)] - piv[("S10", "BINARY")],
        "d_S25": piv[("S25", form)] - piv[("S25", "BINARY")],
        "d_decay": piv[("decay", form)] - piv[("decay", "BINARY")],
        "d_gbar": piv[("gbar", form)] - piv[("gbar", "BINARY")],
    }).reset_index()
    d["form"] = form
    pairs.append(d)
P = pd.concat(pairs, ignore_index=True)
print(f"max |mean-multiplier gap| across every pair: {P['d_gbar'].abs().max():.3e} (must be ~0)")

for base_name in ("EWALL", "TOP20"):
    sub = P[P["base"] == base_name]
    tab = sub.groupby(["form", "state", "side"]).agg(
        n=("d_gt", "size"),
        gt_cheaper=("d_gt", lambda x: (x < 0).mean()),
        med_d_gt=("d_gt", "median"),
        med_d_decay=("d_decay", "median"),
        med_dS0=("d_S0", "median"),
        med_dS10=("d_S10", "median"),
        med_dS25=("d_S25", "median"),
        win25=("d_S25", lambda x: (x > 0).mean()))
    print(f"\n--- base {base_name} ---")
    print(tab.to_string(float_format=lambda x: f"{x:.4f}"))

print()
print("=" * 112)
print("HYPOTHESES (EWALL base = idea 870's own; TOP20 reported beside it)")
print("=" * 112)
for base_name in ("EWALL", "TOP20"):
    sub = P[P["base"] == base_name]
    print(f"\n[{base_name}]")
    for form in ("RAMP", "RATIO"):
        f = sub[sub["form"] == form]
        gcheap = f.groupby(["state", "side"])["d_gt"].apply(lambda x: (x < 0).mean())
        h_cheap = bool((gcheap >= 0.90).all())
        m25 = f.groupby(["state", "side"])["d_S25"].median()
        m0 = f.groupby(["state", "side"])["d_S0"].median()
        h_cost = bool((m25 > 0).all() and (m25 > m0).all())
        h_free = bool((m0.abs() <= 0.02).all())
        print(f"  {form:6s} H_CHEAP {'SUPPORTED' if h_cheap else 'FALSIFIED'} "
              f"(min family share below BINARY turnover {gcheap.min():.3f}; worst family "
              f"{gcheap.idxmin()})")
        print(f"         H_COST  {'SUPPORTED' if h_cost else 'FALSIFIED'} "
              f"(median dSharpe@25 range {m25.min():+.4f}..{m25.max():+.4f}; "
              f"families with dS25>dS0 {int((m25 > m0).sum())} of 6)")
        print(f"         H_FREE  {'SUPPORTED' if h_free else 'FALSIFIED'} "
              f"(|median dSharpe@0| max {m0.abs().max():.4f}, range {m0.min():+.4f}..{m0.max():+.4f})")

print()
print("=" * 112)
print("COST DECAY by form (the queue's own statistic), all arms, both bases")
print("=" * 112)
print(A.groupby(["base", "form"]).agg(n=("decay", "size"), med_decay=("decay", "median"),
                                      med_gt=("gt", "median"), med_S10=("S10", "median"),
                                      keep4b=("keep4b", "sum"), keep4a=("keep4a", "sum"),
                                      oos4b=("oos4b", "sum"))
      .to_string(float_format=lambda x: f"{x:.4f}"))

print()
print("=" * 112)
print("PROTOCOL rule 8 walk-forward — IS-only pick per FORM, OOS read once")
print("=" * 112)
sel = A[(A["base"] == "EWALL")]
out = []
for form in FORMS:
    f = sel[sel["form"] == form].sort_values("IS_S", ascending=False)
    r = f.iloc[0]
    out.append(dict(form=form, family=r["family"], q=r["q"], w=r["w"], depth=r["depth"],
                    cad=r["cadence"], gross=r["gross"], IS_S=r["IS_S"],
                    OOS_CAGR=r["OOS_CAGR"], OOS_S=r["OOS_S"], OOS_MaxDD=r["OOS_MaxDD"],
                    OOS_H1=r["OOS_H1"], OOS_H2=r["OOS_H2"], oos4a=r["oos4a"], oos4b=r["oos4b"],
                    full_CAGR=r["CAGR"], full_S=r["Sharpe"], full_MaxDD=r["MaxDD"],
                    gt=r["gt"], decay=r["decay"]))
W = pd.DataFrame(out)
print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
print(f"\nbenchmarks — SPY full {sc:.2%} / {ss:.3f} / {sd:.2%}  (H1 {sh1:.3f} H2 {sh2:.3f});  "
      f"OOS {soc:.2%} / {sos_:.3f} / {sod:.2%}")
print(f"             RULES v2 (live) full {bc:.2%} / {bs:.3f} / {bd:.2%};  "
      f"OOS {boc:.2%} / {bos_:.3f} / {bod:.2%}")
print(f"             TOP20 shelf book g0.65 full "
      f"{metrics(BASE[('TOP20', 0.75)])['CAGR']:.2%} / {metrics(BASE[('TOP20', 0.75)])['Sharpe']:.3f} "
      f"(printed at g=0.75, the grid's rung, not the shelf's 0.65)")

print()
print("=" * 112)
print("4b / 4a FOOTPRINT by form (matched-gross arms only)")
print("=" * 112)
print(A.groupby(["base", "form"])[["keep4a", "keep4b", "oos4a", "oos4b"]].mean()
      .to_string(float_format=lambda x: f"{x:.4f}"))

A.to_csv(REPO / "research" / "backtests" /
         "2026-09-15_is-the-CONTINUOUS-SCALER-uniformly-cheaper-than-the-BINARY-GATE_cloud.arms.csv",
         index=False)
print("\nSURVIVORSHIP: universe.json is the current constituent list; levels optimistic, the "
      "CONT-minus-BINARY differencing at matched gross is the durable part.")
