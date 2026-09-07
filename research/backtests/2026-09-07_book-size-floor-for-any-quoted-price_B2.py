#!/usr/bin/env python3
"""QUEUE idea 124 — book-size-floor-for-any-quoted-price (lane B, 2026-09-07).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 122 found that ALL 24 panel-axis and ALL 5 cost-axis sign failures in idea 94's price
list are the 5-name V1u book (16/41 admissible) while the 56-name EWall book is 47/48.
Derive the floor directly: price the same instruments on top-n books with n in
{3,5,10,20,40,all} and find the n at which the denominator's sign becomes stable.  The
answer is a number PROTOCOL can state instead of '~20 names'.  Max 2 params."

What is being measured
----------------------
Every drawdown "price" the record publishes is

    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)   pp CAGR per pp MaxDD

whose denominator dMaxDD is a difference of two single-day maxima.  Idea 122 subjected that
denominator to a three-axis SIGN TEST and found the failures were not spread over the record
— they were concentrated in ONE book.  But that book (V1u) differs from the surviving book
(EWall) in TWO ways at once: it holds 5 names instead of 56, AND it scores them with the
1/sqrt(vol20) scaler.  Idea 122 could not separate the two.  This run holds everything else
fixed and moves ONLY the book size.

THE LADDER (one family, one dial — this is the whole design)
    TOPn = idea 2's composite ranking, NO vol scaler, NO gate, top-n names at GROSS/n each,
           n in {3, 5, 10, 20, 40, ALL}.  GROSS = 0.75 at every rung, so the rungs differ in
           CONCENTRATION only: same score, same days, same gross, same arms, same costs.
           ALL = every name with a defined composite that day at GROSS/k (the n -> inf limit).
    Two rungs of this ladder are books idea 94 already published:
        TOPn(n=20) IS idea 94's TOP20, bit for bit  -> asserted against idea 122's committed
                   signtest.csv and d3.csv (same seed, same draws) as a reproduction gate.
    V1u is carried as an OFF-LADDER REFERENCE (5 names AND the vol scaler) so that the
    ladder's own n=5 rung answers idea 124's confound: is V1u's fragility SIZE or the SCALER?
    idea 94's EWall is not re-run; its published D3 fractions are read from idea 122's
    committed d3.csv (identical seed/draws/panel) and quoted beside the ALL rung.

THE SIGN TEST (inherited verbatim from idea 122; nothing here re-tunes it)
    A published rate is ADMISSIBLE only if its denominator's sign survives all three
    perturbations, none of which the price claim depends on:
      D1 cost    dMaxDD > 0 at every rung in {0, 5, 10, 25} bps
      D2 window  dMaxDD > 0 in BOTH 2009-2016 and 2017-2026
      D3 panel   dMaxDD > 0 in at least a fraction tau of NDRAW=40 draws that delete a
                 fraction q of the panel at random (signals recomputed on the sub-panel)

Tuned parameters (PROTOCOL rule 4).  TWO, both of the TEST and neither of any trading rule:
    q    drop fraction in {0.05, 0.10, 0.20}
    tau  sign-agreement threshold in {0.80, 0.90, 0.95, 1.00}
ALL 12 grid points are reported at every rung.  (q, tau) = (0.10, 0.90) is the headline,
adopted unchanged from idea 119/122 so this run cannot pick its own bar.  n is the axis under
measurement, not a tuned parameter: every rung is reported and none is selected.

THE FLOOR (pre-registered definition, written before any number was read)
    n* = the smallest ladder rung whose ADMISSIBLE fraction of published rows is >= 0.90 on
    BOTH panels at the headline (q, tau).  The 0.90 is a reporting bar, not a trading dial;
    the full admissible-fraction-vs-n curve is printed at all 12 (q, tau) points so any other
    bar can be read straight off it.  If the curve is NOT monotone in n, "a floor" is the
    wrong shape and the honest answer is that no floor exists — that is a KILL of the
    queue's premise, not a failure of the run.

Pre-registered predictions (written before any number below was read)
    P1  The admissible fraction is MONOTONE NON-DECREASING in n on both panels.
    P2  n* <= 20 on both panels: the record's informal "~20 names" is conservative.
    P3  The binding axis at small n is the PANEL axis D3, not the cost axis D1 (idea 122
        found 24 panel failures against 5 cost failures on the same list).
    P4  The clean TOP5 rung is MORE admissible than V1u: part of V1u's fragility is the
        vol scaler, not its size.
    P5  No new KEEP.  This is a measurement run; 4a and 4b are reported for every row.

Walk-forward (PROTOCOL rule 8), fixed before any OOS number was read
    S1  idea 94's own selector, unchanged: in each (universe, rung, cost) cell, among arms
        that bought >= 1.0 pp of IS MaxDD, pick the LOWEST IS rate; evaluate untouched on
        2017-2026.
    S2  the same selector restricted to arms whose denominator passes the sign test computed
        on 2009-2016 DATA ONLY (IS cost axis, IS-window draws).  The OOS window is never
        consulted by the screen.
    S3  the floor itself as a walk-forward object: n*_IS is computed on IS data only and
        compared with n*_OOS computed on the untouched window.  A floor that PROTOCOL can
        state must be the same number in both windows.
    Reported for S1/S2: OOS CAGR / Sharpe / MaxDD against the cell's own control, against
    the LIVE baseline RULES v2, against RULES v1, and against SPY.

Execution realism (PROTOCOL rule 2): inherited from idea 94 — weekly decision at close t
applied at t+1, long-only, no leverage, costs charged inside the loop so the stop and the
drawdown state machine see NET equity.  10 bps is the PROTOCOL point; 25 bps also published.

SURVIVORSHIP: universe.json (56) and universe_broad.json (136) are current-constituent
lists, so every absolute CAGR below is optimistic.  This run reports within-cell differences
and the STABILITY of a sign, both far less exposed than levels — but a survivorship-free
panel could still move which rows pass.

Deterministic (seed 20260905, idea 122's, so the D3 draws are byte-identical to the
committed run), standalone.  Imports research/baseline.py and idea 94's script; modifies
nothing.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location(
    "i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)

STEM = Path(__file__).stem
OUT = BT / STEM
I122 = BT / "2026-09-05_price-denominator-sign-test_C"

PCOST = 10.0
COST_RUNGS = [0.0, 5.0, 10.0, 25.0]           # D1
PUB_COSTS = [10.0, 25.0]                      # the rungs idea 94 published
IS_END, OOS_START = H.IS_END, H.OOS_START
NDRAW, DROP_FRACS, TAUS, SEED = 40, (0.05, 0.10, 0.20), (0.80, 0.90, 0.95, 1.00), 20260905
Q_STAR, TAU_STAR = 0.10, 0.90                 # idea 119/122's headline, adopted unchanged
FLOOR = 0.10                                  # idea 94's absolute floor on |dMaxDD|
FLOOR_BAR = 0.90                              # the reporting bar in the n* definition
RUNGS = [3, 5, 10, 20, 40, "ALL"]
BOOKS = [f"TOP{n}" for n in RUNGS] + ["V1u"]  # V1u is OFF-LADDER, always labelled as such
ARMS = [(n, k, kw, sp) for (n, k, kw, sp) in H.arm_specs() if n != "control"]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 4000)


def fmt(df):
    return df.to_string(index=False, float_format=lambda x: f"{x:.4f}")


def rung_of(book):
    return None if book == "V1u" else book[3:]


def nnames(book, px):
    r = rung_of(book)
    if r is None:
        return H.NV1
    return px.shape[1] if r == "ALL" else int(r)


# ---------------------------------------------------------------- cached panel signals
def panel(px):
    """Everything every book/arm on this panel needs, computed ONCE.

    The ladder's whole point is that all six rungs share one score, so the expensive rank
    matrices are computed per (score, gate) and reused across rungs — 12 ranks per panel
    instead of one per (rung, gate)."""
    comp = H.composite(px)
    v20 = H.vol20(px)
    ma = px.rolling(200).mean()
    S = dict(comp=comp, v20=v20, ma=ma, v1s=comp / v20.clip(lower=0.08) ** 0.5)
    S["gates"] = {g: gmask(px, g, S) for g in H.GATES}
    S["rank"] = {}
    for skey in ("comp", "v1s"):
        s = S[skey]
        S["rank"][(skey, None)] = s.rank(axis=1, ascending=False)
        S["rank"][(skey, "cnt")] = s.notna().sum(axis=1)
        for g in H.GATES:
            sg = s.where(S["gates"][g])
            S["rank"][(skey, g)] = sg.rank(axis=1, ascending=False)
            S["rank"][(skey, g, "cnt")] = sg.notna().sum(axis=1)
    return S


def gmask(px, gate, S):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma, v = S["ma"], S["v20"]
    if gate == "g200":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * 1.03, 1.0)
        raw = raw.mask(px < ma * 0.97, 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "abs12":
        return (px > px.shift(252)).fillna(False)
    if gate == "vol60":
        return (v < H.MAX_VOL).fillna(False)
    if gate == "v1gate":
        return ((px > ma) & (v < H.MAX_VOL)).fillna(False)
    raise ValueError(gate)


def _topw(rank, n, cnt):
    """Top-n of `rank` at GROSS/n each.  n='ALL' -> every scored name at GROSS/k."""
    if n == "ALL":
        k = cnt.replace(0, np.nan)
        return rank.le(k, axis=0).astype(float).mul(H.GROSS / k, axis=0).fillna(0.0)
    return (rank <= n).astype(float) * (H.GROSS / n)


def targets(px, book, S, gate=None, conv="dg"):
    """Target weights for one ladder rung (or the off-ladder V1u) under one instrument."""
    skey = "v1s" if book == "V1u" else "comp"
    r = rung_of(book)
    if conv == "rw" and gate is not None:
        rank = S["rank"][(skey, gate)]
        if book == "V1u":
            return (rank <= H.NV1).astype(float) * H.WV1
        return _topw(rank, r if r == "ALL" else int(r), S["rank"][(skey, gate, "cnt")])
    rank = S["rank"][(skey, None)]
    base = ((rank <= H.NV1).astype(float) * H.WV1 if book == "V1u"
            else _topw(rank, r if r == "ALL" else int(r), S["rank"][(skey, "cnt")]))
    if gate is None:
        return base
    return base.where(S["gates"][gate], 0.0)


# ---------------------------------------------------------------- price primitives
def dpair(rc, ra):
    """(dCAGR, dMaxDD) in pp and idea 94's rate with its absolute floor."""
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd > FLOOR else np.nan)


def win(r, w):
    return r if w == "full" else (r.loc[:IS_END] if w == "IS" else r.loc[OOS_START:])


# ---------------------------------------------------------------- main grid (D1, D2)
def build_grid(uname, kw):
    px = H.load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    S = panel(px)
    ms = metrics(spy)

    print("\n" + "=" * 210)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f} OOS {bars['soos']:.3f}")
    print("=" * 210)

    # ---- gate A: the n=20 rung must BE idea 94's TOP20 and V1u must BE idea 94's V1u
    worst = 0.0
    for bk, i94 in (("TOP20", "TOP20"), ("V1u", "V1u")):
        for g in [None] + H.GATES:
            for conv in (("dg",) if g is None else ("dg", "rw")):
                a = targets(px, bk, S, g, conv).fillna(0.0)
                e = H.targets(px, i94, g, conv).fillna(0.0)
                worst = max(worst, float((a - e).abs().to_numpy().max()))
    print(f"[gate A] ladder rung TOP20 / V1u vs idea 94 targets(): max|diff| = {worst:.3e} "
          f"({'EXACT' if worst < 1e-15 else 'NOT EXACT — unsafe'})")

    # ---- gate B: the run harness with every instrument off == engine.backtest
    wb = 0.0
    for b in BOOKS:
        W = targets(px, b, S)
        wb = max(wb, float((H.run(px, W, bps=PCOST)["r"].loc[start:]
                            - backtest(px, W, cost_bps=PCOST, freq=H.FREQ)["returns"].loc[start:])
                           .abs().max()))
    print(f"[gate B] control vs engine.backtest @{PCOST:.0f}bps: max|diff| = {wb:.3e} "
          f"({'EXACT' if wb < 1e-12 else 'NOT EXACT — unsafe'})")

    # ---- how far the ALL rung sits from idea 94's EWall (scored-limit vs priced-limit)
    dw = float((targets(px, "TOPALL", S) - H.targets(px, "EWall")).abs().loc[start:].to_numpy().max())
    n_all = S["rank"][("comp", "cnt")].loc[start:]
    print(f"[note]  ALL rung (scored limit) vs idea 94 EWall (priced limit): max|dw| = {dw:.4f}; "
          f"ALL holds {n_all.mean():.1f} names on average (panel {px.shape[1]}), "
          f"differs from priced count on {int((n_all != px.notna().sum(axis=1).loc[start:]).sum())} "
          f"of {len(n_all)} eval days")

    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
              for c in PUB_COSTS}
    v2_net = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
              for c in PUB_COSTS}

    rets = {}
    for b in BOOKS:
        for name, kind, kwargs, (g, conv) in H.arm_specs():
            W = targets(px, b, S, g, conv)
            for c in COST_RUNGS:
                rets[(b, name, c)] = H.run(px, W, bps=c, **kwargs)["r"].loc[start:]

    rows = []
    for b in BOOKS:
        for c in PUB_COSTS:
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in ARMS:
                ra = rets[(b, name, c)]
                dc, dd, rate = dpair(rc, ra)
                rec = dict(uni=uname, book=b, rung=rung_of(b) or "V1u(off-ladder)",
                           n=nnames(b, px), cost=c, arm=name, kind=kind,
                           dCAGR=dc, dMaxDD=dd, rate=rate, published=bool(np.isfinite(rate)))
                for cc in COST_RUNGS:
                    _, dd_c, _ = dpair(rets[(b, "control", cc)], rets[(b, name, cc)])
                    rec[f"dMaxDD@{cc:.0f}"] = dd_c
                    _, dd_ci, _ = dpair(win(rets[(b, "control", cc)], "IS"),
                                        win(rets[(b, name, cc)], "IS"))
                    rec[f"dMaxDD_IS@{cc:.0f}"] = dd_ci
                for w in ("IS", "OOS"):
                    dcw, ddw, rw_ = dpair(win(rc, w), win(ra, w))
                    rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dcw, ddw, rw_
                ma_, mc_ = metrics(ra), metrics(rc)
                mg = H.margins(ra, bars)
                rec.update(CAGR=ma_["CAGR"], Sharpe=ma_["Sharpe"], MaxDD=ma_["MaxDD"],
                           ctl_CAGR=mc_["CAGR"], ctl_MaxDD=mc_["MaxDD"],
                           p4a_v2=H.pass4a(ra, v2_net[c]), p4a_v1=H.pass4a(ra, v1_net[c]),
                           p4b=all(v > 0 for v in mg.values()),
                           f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-")
                rows.append(rec)
    G = pd.DataFrame(rows)
    G["D1_pass"] = np.all([G[f"dMaxDD@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    G["D2_pass"] = (G.dMaxDD_IS > 0) & (G.dMaxDD_OOS > 0)
    G["D1_pass_IS_only"] = np.all([G[f"dMaxDD_IS@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    return px, start, S, spy, bars, v1_net, v2_net, rets, G


# ---------------------------------------------------------------- D3 bootstrap
def bootstrap(uname, px, start):
    """Name-subsample draws.  Seed, q order and NDRAW are idea 122's, so for any given
    (q, draw) the kept column SET is byte-identical to the committed run — which is what
    makes the TOP20 reproduction gate and the EWall comparison legitimate."""
    rng = np.random.default_rng(SEED)
    ncol = px.shape[1]
    out, t0 = [], time.time()
    for q in DROP_FRACS:
        k = int(round(ncol * (1 - q)))
        for d in range(NDRAW):
            keep = sorted(rng.choice(ncol, size=k, replace=False))
            sub = px.iloc[:, keep]
            Ss = panel(sub)
            for b in BOOKS:
                rc = H.run(sub, targets(sub, b, Ss), bps=PCOST)["r"].loc[start:]
                for name, kind, kwargs, (g, conv) in ARMS:
                    ra = H.run(sub, targets(sub, b, Ss, g, conv), bps=PCOST,
                               **kwargs)["r"].loc[start:]
                    rec = dict(uni=uname, q=q, draw=d, book=b, arm=name)
                    for w in ("full", "IS", "OOS"):
                        dc, dd, rt = dpair(win(rc, w), win(ra, w))
                        rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dc, dd, rt
                    out.append(rec)
        print(f"    [{uname}] q={q:.2f}: {NDRAW} draws done ({time.time()-t0:.0f}s elapsed)",
              flush=True)
    B = pd.DataFrame(out)
    D3 = B.groupby(["uni", "q", "book", "arm"]).agg(
        frac_pos_full=("dMaxDD_full", lambda s: float((s > 0).mean())),
        frac_pos_IS=("dMaxDD_IS", lambda s: float((s > 0).mean())),
        frac_pos_OOS=("dMaxDD_OOS", lambda s: float((s > 0).mean())),
        frac_priceable=("rate_full", lambda s: float(np.isfinite(s).mean())),
        dMaxDD_med=("dMaxDD_full", "median"), dCAGR_med=("dCAGR_full", "median"),
        rate_med=("rate_full", "median")).reset_index()
    return B, D3


# ---------------------------------------------------------------- assemble the sign test
def signtest(G, D3, q, tau):
    d = D3[D3.q == q].set_index(["uni", "book", "arm"])
    T = G.copy()
    idx = pd.MultiIndex.from_frame(T[["uni", "book", "arm"]])
    T["D3_frac_full"] = d.frac_pos_full.reindex(idx).values
    T["D3_frac_IS"] = d.frac_pos_IS.reindex(idx).values
    T["D3_pass"] = T.D3_frac_full >= tau
    T["D3_pass_IS_only"] = T.D3_frac_IS >= tau
    T["ADMISSIBLE"] = T.published & T.D1_pass & T.D2_pass & T.D3_pass
    T["ADMISSIBLE_IS"] = T.D1_pass_IS_only & T.D3_pass_IS_only & (T.dMaxDD_IS > FLOOR)
    return T


def floor_curve(T, label):
    """Admissible fraction of PUBLISHED rows by rung, plus the per-axis pass rates."""
    rows = []
    for (uni, b), g in T.groupby(["uni", "book"], sort=False):
        p = g[g.published]
        rows.append(dict(uni=uni, book=b, n=int(g.n.iloc[0]), rows=len(g),
                         published=len(p),
                         adm=int(p.ADMISSIBLE.sum()),
                         adm_frac=float(p.ADMISSIBLE.mean()) if len(p) else np.nan,
                         D1=float(p.D1_pass.mean()) if len(p) else np.nan,
                         D2=float(p.D2_pass.mean()) if len(p) else np.nan,
                         D3=float(p.D3_pass.mean()) if len(p) else np.nan,
                         mean_D3_frac=float(p.D3_frac_full.mean()) if len(p) else np.nan,
                         min_D3_frac=float(p.D3_frac_full.min()) if len(p) else np.nan,
                         pub_frac=float(g.published.mean())))
    F = pd.DataFrame(rows)
    F["grid"] = label
    return F


def n_star(F, bar=FLOOR_BAR):
    """Smallest LADDER rung (V1u excluded — it is off-ladder) meeting `bar` on BOTH panels."""
    lad = F[F.book != "V1u"]
    ok = []
    for b in [f"TOP{n}" for n in RUNGS]:
        s = lad[lad.book == b]
        if len(s) and (s.adm_frac >= bar).all() and s.uni.nunique() == lad.uni.nunique():
            ok.append(b)
    return ok[0] if ok else None


def monotone(F):
    order = [f"TOP{n}" for n in RUNGS]
    out = {}
    for uni, g in F[F.book != "V1u"].groupby("uni"):
        v = g.set_index("book").reindex(order).adm_frac.values
        out[uni] = bool(np.all(np.diff(v) >= -1e-12))
    return out


# ---------------------------------------------------------------- reproduction gates
def reproduce(T, D3):
    """Gate C: the shared rungs must reproduce idea 122's committed file exactly."""
    f = I122.with_suffix(".signtest.csv")
    if not f.exists():
        print("[gate C] idea 122 signtest.csv missing — reproduction gate SKIPPED")
        return None
    R = pd.read_csv(f)
    cols = ["dCAGR", "dMaxDD", "rate", "dMaxDD_IS", "dMaxDD_OOS", "D1_pass", "D2_pass"]
    SENT = -9.0e99
    recs = []
    for mine, theirs in (("TOP20", "TOP20"), ("V1u", "V1u")):
        a = T[T.book == mine].set_index(["uni", "cost", "arm"]).sort_index()
        b = R[R.book == theirs].set_index(["uni", "cost", "arm"]).sort_index()
        j = a.index.intersection(b.index)
        for c in cols:
            x, y = a.loc[j, c], b.loc[j, c]
            if x.dtype == bool or y.dtype == bool:
                dv = float((x.astype(bool) != y.astype(bool)).mean())
            else:   # sentinel-fill so a NaN facing a number counts as a disagreement
                dv = float((pd.to_numeric(x).fillna(SENT)
                            - pd.to_numeric(y).fillna(SENT)).abs().max())
            recs.append(dict(book=mine, col=c, n=len(j), diff=dv))
    d3f = I122.with_suffix(".d3.csv")
    if d3f.exists():
        R3 = pd.read_csv(d3f)
        for mine, theirs in (("TOP20", "TOP20"), ("V1u", "V1u")):
            a = D3[D3.book == mine].set_index(["uni", "q", "arm"]).sort_index()
            b = R3[R3.book == theirs].set_index(["uni", "q", "arm"]).sort_index()
            j = a.index.intersection(b.index)
            for c in ("frac_pos_full", "frac_pos_IS", "frac_pos_OOS"):
                recs.append(dict(book=mine, col=f"D3.{c}", n=len(j),
                                 diff=float((a.loc[j, c] - b.loc[j, c]).abs().max())))
    C = pd.DataFrame(recs)
    worst = float(C.loc[C.col.str.startswith(("dCAGR", "dMaxDD", "rate", "D3")), "diff"].max())
    print("\n[gate C] REPRODUCTION of idea 122's committed rows by the nested ladder rungs")
    print(fmt(C))
    print(f"[gate C] worst numeric disagreement = {worst:.3e} "
          f"({'EXACT' if worst < 1e-9 else 'NOT EXACT — the ladder does not nest the record'})")
    return C


def ewall_reference(D3):
    """idea 94's EWall D3 fractions, read from idea 122's committed d3.csv (same draws)."""
    f = I122.with_suffix(".d3.csv")
    if not f.exists():
        return None
    R = pd.read_csv(f)
    E = R[R.book == "EWall"].copy()
    E["book"] = "EWall(idea94, committed)"
    return E


# ---------------------------------------------------------------- walk-forward (rule 8)
def walk_forward(T, rets, spy, v1_net, v2_net, uname, px):
    spy_o = metrics(spy.loc[OOS_START:])
    out = []
    for b in BOOKS:
        for c in PUB_COSTS:
            cell = T[(T.uni == uname) & (T.book == b) & (T.cost == c)]
            ctl_o = metrics(rets[(b, "control", c)].loc[OOS_START:])
            base = dict(uni=uname, book=b, rung=rung_of(b) or "V1u(off-ladder)",
                        n=nnames(b, px), cost=c,
                        ctl_CAGR=ctl_o["CAGR"], ctl_Sharpe=ctl_o["Sharpe"], ctl_MaxDD=ctl_o["MaxDD"],
                        v2_Sharpe=metrics(v2_net[c].loc[OOS_START:])["Sharpe"],
                        v2_CAGR=metrics(v2_net[c].loc[OOS_START:])["CAGR"],
                        v2_MaxDD=metrics(v2_net[c].loc[OOS_START:])["MaxDD"],
                        v1_Sharpe=metrics(v1_net[c].loc[OOS_START:])["Sharpe"],
                        spy_CAGR=spy_o["CAGR"], spy_Sharpe=spy_o["Sharpe"], spy_MaxDD=spy_o["MaxDD"])
            for sel, pool in (("S1", cell[(cell.dMaxDD_IS >= 1.0) & np.isfinite(cell.rate_IS)]),
                              ("S2", cell[(cell.dMaxDD_IS >= 1.0) & np.isfinite(cell.rate_IS)
                                          & cell.ADMISSIBLE_IS])):
                r = dict(base, sel=sel)
                if pool.empty:
                    r.update(pick="NOTHING", IS_rate=np.nan, OOS_rate=np.nan,
                             OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                             OOS_dMaxDD=np.nan, pool=0)
                else:
                    p = pool.sort_values("rate_IS").iloc[0]
                    ro = rets[(b, p.arm, c)].loc[OOS_START:]
                    mo = metrics(ro)
                    r.update(pick=p.arm, IS_rate=p.rate_IS, OOS_rate=p.rate_OOS,
                             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                             OOS_dMaxDD=p.dMaxDD_OOS, pool=len(pool))
                out.append(r)
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    grids, d3s, boots, wfs, pxs = [], [], [], [], {}
    store = {}
    for uname, kw in (("universe.json(56)", dict()), ("universe_broad.json", dict(broad=True))):
        px, start, S, spy, bars, v1_net, v2_net, rets, G = build_grid(uname, kw)
        print(f"\nMAIN GRID {uname} — {len(G)} published rows "
              f"({len(BOOKS)} books x {len(ARMS)} arms x {len(PUB_COSTS)} costs)")
        print(fmt(G[["book", "n", "cost", "arm", "dCAGR", "dMaxDD", "rate", "dMaxDD_IS",
                     "dMaxDD_OOS", "CAGR", "Sharpe", "MaxDD", "D1_pass", "D2_pass",
                     "p4a_v2", "p4a_v1", "p4b", "f4b"]]))
        print(f"\n  D3 bootstrap: {len(DROP_FRACS)} x {NDRAW} draws x {len(BOOKS)} books x "
              f"{len(ARMS)} arms on {uname} (seed {SEED})", flush=True)
        B, D3 = bootstrap(uname, px, start)
        grids.append(G)
        d3s.append(D3)
        boots.append(B)
        pxs[uname] = px
        store[uname] = (rets, spy, v1_net, v2_net, px)
    G = pd.concat(grids, ignore_index=True)
    D3 = pd.concat(d3s, ignore_index=True)
    B = pd.concat(boots, ignore_index=True)

    # ---------------- the full (q, tau) grid of floor curves — ALL 12 points reported
    curves = []
    for q in DROP_FRACS:
        for tau in TAUS:
            T = signtest(G, D3, q, tau)
            F = floor_curve(T, f"q={q:.2f},tau={tau:.2f}")
            F["q"], F["tau"] = q, tau
            curves.append(F)
    FC = pd.concat(curves, ignore_index=True)
    Th = signtest(G, D3, Q_STAR, TAU_STAR)

    print("\n" + "=" * 210)
    print("A. THE FLOOR CURVE — admissible fraction of published rows by ladder rung, "
          f"ALL {len(DROP_FRACS)*len(TAUS)} (q, tau) points reported")
    print("=" * 210)
    for q in DROP_FRACS:
        for tau in TAUS:
            s = FC[(FC.q == q) & (FC.tau == tau)]
            print(f"\n--- q={q:.2f} tau={tau:.2f} "
                  f"{'  <== PRE-REGISTERED HEADLINE' if (q, tau) == (Q_STAR, TAU_STAR) else ''}")
            print(fmt(s[["uni", "book", "n", "published", "adm", "adm_frac",
                         "D1", "D2", "D3", "mean_D3_frac", "min_D3_frac"]]))
            print(f"    n* (smallest rung >= {FLOOR_BAR:.2f} on BOTH panels) = "
                  f"{n_star(s) or 'NONE — no rung clears the bar'}")

    print("\n" + "=" * 210)
    print("B. THE ANSWER — headline (q, tau) = "
          f"({Q_STAR}, {TAU_STAR}); the ladder is composite-ranked, gross 0.75, one dial (n)")
    print("=" * 210)
    Fh = FC[(FC.q == Q_STAR) & (FC.tau == TAU_STAR)]
    print(fmt(Fh[["uni", "book", "n", "published", "adm", "adm_frac", "D1", "D2", "D3",
                  "mean_D3_frac", "min_D3_frac"]]))
    ns = n_star(Fh)
    print(f"\n  n* = {ns or 'NONE'}   (smallest ladder rung with admissible fraction >= "
          f"{FLOOR_BAR:.2f} on BOTH panels)")
    print(f"  monotone in n?  {monotone(Fh)}")
    nstar_by_bar = {bar: n_star(Fh, bar) for bar in (0.80, 0.85, 0.90, 0.95, 1.00)}
    print(f"  n* under other reporting bars: {nstar_by_bar}")
    E = ewall_reference(D3)
    if E is not None:
        eh = E[E.q == Q_STAR]
        print(f"\n  reference (committed idea 94 EWall, idea 122's own D3 draws): "
              f"mean frac_pos_full = {eh.frac_pos_full.mean():.4f}, "
              f"min = {eh.frac_pos_full.min():.4f} over {len(eh)} arm-cells")
        al = D3[(D3.q == Q_STAR) & (D3.book == "TOPALL")]
        print(f"  this run's ALL rung (scored limit):                        "
              f"mean frac_pos_full = {al.frac_pos_full.mean():.4f}, "
              f"min = {al.frac_pos_full.min():.4f} over {len(al)} arm-cells")

    C = reproduce(Th, D3)

    print("\n" + "=" * 210)
    print("C. SIZE vs SCALER — the confound idea 122 could not separate "
          "(TOP5 = 5 names, no scaler; V1u = 5 names AND the 1/sqrt(vol20) scaler)")
    print("=" * 210)
    cmp_ = Fh[Fh.book.isin(["TOP5", "V1u"])][["uni", "book", "n", "published", "adm",
                                              "adm_frac", "D1", "D2", "D3", "mean_D3_frac"]]
    print(fmt(cmp_))

    print("\n" + "=" * 210)
    print("D. PER-AXIS FAILURE CENSUS at the headline — which perturbation binds, by rung")
    print("=" * 210)
    pub = Th[Th.published]
    crows = []
    for (b, n), g in pub.groupby(["book", "n"], sort=False):
        allrows = Th[(Th.book == b)]
        crows.append(dict(
            book=b, n=int(n), rows=len(allrows), published=len(g),
            unpriceable=len(allrows) - len(g),
            fail_D1=int((~g.D1_pass).sum()), fail_D2=int((~g.D2_pass).sum()),
            fail_D3=int((~g.D3_pass).sum()),
            fail_D3_only=int((~g.D3_pass & g.D1_pass & g.D2_pass).sum()),
            fail_D1_only=int((~g.D1_pass & g.D2_pass & g.D3_pass).sum()),
            admissible=int(g.ADMISSIBLE.sum())))
    cen = pd.DataFrame(crows).sort_values("n")
    print(fmt(cen))

    # ---------------- rule 8
    print("\n" + "=" * 210)
    print("E. RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 only, evaluated untouched "
          "on 2017-2026")
    print("=" * 210)
    for uname in store:
        rets, spy, v1_net, v2_net, px = store[uname]
        wfs.append(walk_forward(Th, rets, spy, v1_net, v2_net, uname, px))
    W = pd.concat(wfs, ignore_index=True)
    print(fmt(W[["uni", "book", "n", "cost", "sel", "pick", "pool", "IS_rate", "OOS_rate",
                 "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_dMaxDD", "ctl_Sharpe",
                 "v2_Sharpe", "v1_Sharpe", "spy_Sharpe"]]))
    for sel in ("S1", "S2"):
        s = W[(W.sel == sel) & W.OOS_Sharpe.notna()]
        print(f"  {sel}: {len(s)} of {len(W[W.sel==sel])} cells picked something; "
              f"mean OOS Sharpe {s.OOS_Sharpe.mean():.4f} "
              f"(control {s.ctl_Sharpe.mean():.4f}, RULES v2 {s.v2_Sharpe.mean():.4f}, "
              f"RULES v1 {s.v1_Sharpe.mean():.4f}, SPY {s.spy_Sharpe.mean():.4f}); "
              f"beats SPY in {int((s.OOS_Sharpe > s.spy_Sharpe).sum())}/{len(s)}, "
              f"beats RULES v2 in {int((s.OOS_Sharpe > s.v2_Sharpe).sum())}/{len(s)}")
    chg = W.pivot_table(index=["uni", "book", "cost"], columns="sel", values="pick",
                        aggfunc="first")
    if {"S1", "S2"} <= set(chg.columns):
        print(f"  S2 (IS sign screen) changes the pick in "
              f"{int((chg.S1 != chg.S2).sum())} of {len(chg)} cells")

    # ---------------- S3: is the FLOOR itself out-of-sample stable?
    print("\n  S3 — the floor as a walk-forward object (n* from IS data only vs n* from OOS)")
    s3 = []
    for q in DROP_FRACS:
        for tau in TAUS:
            T = signtest(G, D3, q, tau)
            pub_ = T[T.published]
            rowsq = []
            for (uni, b), g in pub_.groupby(["uni", "book"]):
                rowsq.append(dict(uni=uni, book=b, n=int(g.n.iloc[0]),
                                  adm_frac=float((g.D1_pass_IS_only & g.D3_pass_IS_only
                                                  & (g.dMaxDD_IS > FLOOR)).mean())))
            Fis = pd.DataFrame(rowsq)
            rowsq = []
            for (uni, b), g in pub_.groupby(["uni", "book"]):
                d3o = D3[(D3.q == q)].set_index(["uni", "book", "arm"]).frac_pos_OOS
                key = pd.MultiIndex.from_frame(g[["uni", "book", "arm"]])
                rowsq.append(dict(uni=uni, book=b, n=int(g.n.iloc[0]),
                                  adm_frac=float(((d3o.reindex(key).values >= tau)
                                                  & (g.dMaxDD_OOS > FLOOR).values).mean())))
            Foos = pd.DataFrame(rowsq)
            s3.append(dict(q=q, tau=tau, n_star_IS=n_star(Fis), n_star_OOS=n_star(Foos),
                           agree=n_star(Fis) == n_star(Foos)))
    S3 = pd.DataFrame(s3)
    print(fmt(S3))
    hd = S3[(S3.q == Q_STAR) & (S3.tau == TAU_STAR)].iloc[0]
    print(f"  IS and OOS floors agree at {int(S3.agree.sum())} of {len(S3)} (q, tau) points; "
          f"headline: n*_IS = {hd.n_star_IS} vs n*_OOS = {hd.n_star_OOS}")

    # ---------------- KEEP paths
    print("\n" + "=" * 210)
    print("F. KEEP PATHS — 4a (beat the live book, RULES v2) and 4b (capital-worthy) for "
          "every published row")
    print("=" * 210)
    print(f"  4a vs live RULES v2: {int(G.p4a_v2.sum())} of {len(G)} rows"
          f"  |  4a vs RULES v1 (continuity): {int(G.p4a_v1.sum())} of {len(G)}")
    print(f"  4b:                  {int(G.p4b.sum())} of {len(G)} rows")
    if G.p4b.any():
        print(fmt(G[G.p4b][["uni", "book", "n", "cost", "arm", "CAGR", "Sharpe", "MaxDD",
                            "rate", "dMaxDD"]].head(60)))
        adm4b = Th[Th.p4b & Th.ADMISSIBLE]
        print(f"  of the 4b rows, {len(adm4b)} also have an ADMISSIBLE denominator at the "
              f"headline; by rung: {adm4b.groupby('book').size().to_dict()}")
    print(f"  4b pass rate by rung: "
          f"{G.groupby('book').p4b.mean().round(3).to_dict()}")

    # ---------------- scorecard
    print("\n" + "=" * 210)
    print("G. PREDICTION SCORECARD")
    print("=" * 210)
    mono = monotone(Fh)
    print(f"  P1 admissible fraction monotone non-decreasing in n: {mono} "
          f"({'CONFIRMED' if all(mono.values()) else 'REFUTED'})")
    ns_num = {"TOP3": 3, "TOP5": 5, "TOP10": 10, "TOP20": 20, "TOP40": 40, "TOPALL": 10 ** 6}
    print(f"  P2 n* <= 20 on both panels: n* = {ns} "
          f"({'CONFIRMED' if ns and ns_num[ns] <= 20 else 'REFUTED'})")
    f1 = int((~pub.D1_pass).sum())
    f3 = int((~pub.D3_pass).sum())
    small = pub[pub.n <= 5]
    print(f"  P3 the binding axis is D3 (panel), not D1 (cost): all rungs D1 fails {f1}, "
          f"D3 fails {f3}; at n<=5 D1 {int((~small.D1_pass).sum())} vs D3 "
          f"{int((~small.D3_pass).sum())} ({'CONFIRMED' if f3 > f1 else 'REFUTED'})")
    a5 = Fh[Fh.book == "TOP5"].adm_frac.mean()
    av = Fh[Fh.book == "V1u"].adm_frac.mean()
    print(f"  P4 TOP5 (size only) more admissible than V1u (size + vol scaler): "
          f"{a5:.4f} vs {av:.4f} ({'CONFIRMED' if a5 > av else 'REFUTED'})")
    print(f"  P5 no new KEEP: 4a(v2) {int(G.p4a_v2.sum())}, 4b {int(G.p4b.sum())} of {len(G)} "
          f"({'CONFIRMED' if G.p4a_v2.sum() == 0 and G.p4b.sum() == 0 else 'see F above'})")

    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    Th.to_csv(OUT.with_suffix(".signtest.csv"), index=False)
    FC.to_csv(OUT.with_suffix(".floorcurve.csv"), index=False)
    D3.to_csv(OUT.with_suffix(".d3.csv"), index=False)
    B.to_csv(OUT.with_suffix(".bootstrap.csv"), index=False)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    S3.to_csv(OUT.with_suffix(".floorwf.csv"), index=False)
    cen.to_csv(OUT.with_suffix(".census.csv"), index=False)
    if C is not None:
        C.to_csv(OUT.with_suffix(".reproduction.csv"), index=False)
    print(f"\nWrote {STEM}.{{grid,signtest,floorcurve,d3,bootstrap,walkforward,floorwf,"
          f"census,reproduction}}.csv   ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
