#!/usr/bin/env python3
"""Idea 381 - "is-the-vol-scaler-the-record's-general-instability-source" (cloud, 2026-09-07).

QUESTION (from QUEUE.md, verbatim).  "idea 124 showed V1u's sign failures are the
1/sqrt(vol20) scaler, not its 5 names (0.402 vs the clean TOP5's 0.857 at matched size,
panel axis 24/41 vs 0/26), and the Sep-3 memo showed the same scaler cancels the
composite's IC.  Re-run the sign test on the ladder WITH and WITHOUT the scaler at every
rung (the scaler as the only dial) and test whether the scaler, not concentration,
explains the record's panel-axis failures corpus-wide.  Max 2 params."

Idea 124 could answer this at ONE rung only: its ladder was scaler-OFF at every n and
carried a single scaler-ON book (V1u) at n=5.  A one-rung contrast cannot separate "the
scaler is bad" from "the scaler is bad AT FIVE NAMES".  This run puts the scaler on the
whole ladder.

DESIGN.  Idea 94's harness and idea 124's sign test, VERBATIM, with the book axis widened
from 7 books to 11 so that the scaler becomes a matched-pairs dial:

    scaler OFF : TOP3  TOP5  TOP10  TOP20  TOP40      (idea 124's ladder, replicated)
    scaler ON  : VS3   VS5   VS10   VS20   VS40       (NEW: comp / clip(vol20,.08)**.5)
    both       : TOPall                               (every priced name at GROSS/N)

Every rung is the same book in every other respect: same composite, same top-n rule, same
equal weight GROSS/n, same weekly cadence, same next-day execution, same 17 arms, same
cost rungs.  The ONLY thing that moves inside a matched pair is whether the ranking score
is divided by sqrt(vol20).

TWO STRUCTURAL FACTS, stated before the numbers because they decide how to read them:
  (i)  GROSS/n at n=5 is 0.75/5 = 0.15 = idea 94's WV1, so **VS5 IS V1u exactly** -- the
       record's own unstable book is a rung of this ladder, not a separate object (gated).
  (ii) The scaler is a RANKING instrument.  At n=all nothing is ranked, so a scaler-ON
       TOPall is byte-identical to TOPall (gated).  The ladder therefore must converge as
       n -> all whatever the scaler does, and the interesting region is small n.

TUNED PARAMETERS (max 2, per PROTOCOL rule 4): (1) the scaler, on/off; (2) the panel
(u56 / broad).  n is the SUBJECT axis and every rung is reported, exactly as in idea 124.
q = 0.10 and tau = 0.90 are INHERITED unchanged from ideas 119/122/124 -- this run does not
get to pick its own bar -- and all 4 tau points are reported anyway.

THE SIGN TEST (idea 122/124's, unchanged).  A quoted price
    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)
is admissible only if its DENOMINATOR keeps its sign under three nuisance perturbations:
    D1 cost axis   dMaxDD > 0 at 0, 5, 10 and 25 bps
    D2 window axis dMaxDD > 0 in BOTH 2009-2016 and 2017-2026
    D3 panel axis  dMaxDD > 0 in >= tau of 40 name-subsample draws (drop q of the panel)
"published" = |dMaxDD| clears idea 94's 0.10 pp floor, i.e. the record would have quoted it.
D3 is the PANEL AXIS the queue's question is about.

RNG REPLICATION.  idea 124's bootstrap consumed `np.random.default_rng(20260907)` over
q in (0.05, 0.10, 0.20) x 40 draws in that order.  This run consumes the identical stream
in the identical order but only BACKTESTS the q=0.10 block, so its q=0.10 sub-panels are
the SAME 40 draws idea 124 used -- which is what makes G5 (below) a real replication gate
rather than a coincidence of distribution.

PRE-REGISTERED READING.  Fixed before any number was read, on adm_pub (share of a cell's
PUBLISHED rows that survive D1+D2+D3 at q=0.10, tau=0.90):
    SCALER          mean(adm_pub OFF - adm_pub ON) over the 20 matched (panel x n x cost)
                    pairs is >= +0.10 AND the difference is >= 0 on >= 7 of the 10
                    (panel x n) pairs.  The scaler is the instability source.
    CONCENTRATION   spearman(n, adm_pub) >= +0.50 in BOTH scaler states on BOTH panels AND
                    the scaler gap above is < +0.10.  Name count is the source.
    BOTH            both hold.        NEITHER  neither holds.
The same contrast is reported on D3 ALONE, because idea 122's actual claim (24/41 vs 0/26)
is a panel-axis claim, not a joint-screen claim.

RULE 8 (PROTOCOL rule 8), both legs fixed before any OOS number was read:
    W1  The CONTRAST itself.  Recompute the whole screen on 2009-2016 only (D1 on IS
        returns, D3 on IS-window draws; D2 has no IS-only form, per idea 122), read the
        scaler gap IS.  Then read the 2017-2026 screen untouched and report the gap OOS.
        A scaler effect that exists only in-sample is not a corpus fact.
    W2  The PRICE LIST at each rung.  In each (panel, book, cost) cell, S1 = idea 94's
        selector (among arms buying >= 1.0 pp of IS MaxDD, the LOWEST IS rate).  Evaluate
        that arm untouched on 2017-2026: OOS CAGR / Sharpe / MaxDD against the cell
        control, the LIVE RULES v2 baseline and SPY, plus spearman(IS rate, OOS rate)
        within the cell -- split by scaler state.

KEEP PATHS.  Both evaluated for every arm-point at both published rungs: 4a against the
live RULES v2 on that panel, 4b against SPY (Sharpe > SPY in both halves AND OOS, MaxDD
<= 60% of SPY's, CAGR >= 70% of SPY's).

GATES (all asserted, all printed).  G1 every shared book's targets == idea 124's
`targets_n` to 0.  G2 **VS5 targets == idea 94's V1u** to 0.  G3 control `run()` ==
`engine.backtest`.  G4 the shared books' grid rows reproduce idea 124's committed
`grid.csv` to 1e-9.  G5 the shared books' q=0.10 D3 rows reproduce idea 124's committed
`d3.csv` to 1e-9 (the rng replication).  G6 a scaler-ON TOPall is byte-identical to TOPall.

CAVEATS.  (1) SURVIVORSHIP -- universe.json and universe_broad.json are current-constituent
lists, so every absolute CAGR here is optimistic; the SUBJECT of this run is the SIGN of a
difference between two arms sharing a panel and the same days, which is far less exposed
than a level.  (2) 40 draws at one q is a 40-point binomial per cell; a share of 0.90 has a
+/- ~0.09 sampling band, reported, and idea 216's warning about few-block estimators
applies.  (3) u56 and broad share names, so two panels is not two independent samples.
(4) This run tests the scaler as a RANKING dial only; it says nothing about a vol scaler
used for SIZING.

Deterministic, standalone, modifies nothing.
"""
import importlib.util, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights                              # noqa
from engine import backtest, metrics                                                 # noqa

BT = ROOT / "research" / "backtests"


def _load(mod, fname):
    s = importlib.util.spec_from_file_location(mod, BT / fname)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


H = _load("i94", "2026-09-04_drawdown-insurance-price-list_B.py")
I124 = _load("i124", "2026-09-07_book-size-floor-for-any-quoted-price_B.py")

SLUG = Path(__file__).stem
OUT = BT / SLUG
PCOST = 10.0
COST_RUNGS = [0.0, 5.0, 10.0, 25.0]
PUB_COSTS = [10.0, 25.0]
IS_END, OOS_START = H.IS_END, H.OOS_START
FLOOR = 0.10
LADDER_N = [3, 5, 10, 20, 40]
BOOKS = ([f"TOP{n}" for n in LADDER_N] + ["TOPall"] + [f"VS{n}" for n in LADDER_N])
SHARED = {f"TOP{n}": f"TOP{n}" for n in LADDER_N}          # idea 124 book name
SHARED["TOPall"] = "TOPall"; SHARED["VS5"] = "V1u"
ARMS = [a for a in H.arm_specs() if a[0] != "control"]
UNIS = [("universe.json(56)", dict()), ("universe_broad.json", dict(broad=True))]
NDRAW, DROP_FRACS, TAUS, SEED = 40, (0.05, 0.10, 0.20), (0.80, 0.90, 0.95, 1.00), 20260907
Q_RUN = 0.10                                  # the only q BACKTESTED (rng stream unchanged)
Q_STAR, TAU_STAR = 0.10, 0.90                 # inherited headline
GAP_BAR, SIGN_BAR, RHO_BAR = 0.10, 7, 0.50    # pre-registered decision thresholds
LOG = []

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.append(s)


def fmt(df):
    return df.to_string(index=False, float_format=lambda x: f"{x:.4f}")


def scaler_of(b):
    return "ON" if b.startswith("VS") else ("OFF" if b != "TOPall" else "n/a")


def n_of(b, npanel):
    return npanel if b == "TOPall" else int(b.replace("TOP", "").replace("VS", ""))


# ------------------------------------------------------------------ the book
def signals(px):
    return dict(comp=H.composite(px), v20=H.vol20(px))


def targets_b(px, book, S, gate=None, conv="dg", force_scaler=None):
    """The 11-book grid.  `force_scaler` exists only for gate G6."""
    vs = (book.startswith("VS")) if force_scaler is None else force_scaler

    def score():
        return S["comp"] / S["v20"].clip(lower=0.08) ** 0.5 if vs else S["comp"]

    def base():
        if book == "TOPall":
            e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
            return H.GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        n = n_of(book, px.shape[1])
        return (score().rank(axis=1, ascending=False) <= n).astype(float) * (H.GROSS / n)

    if gate is None:
        return base()
    g = H.gate_mask(px, gate)
    if conv == "rw":
        if book == "TOPall":
            e = g.astype(float)
            return H.GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        n = n_of(book, px.shape[1])
        return (score().where(g).rank(axis=1, ascending=False) <= n).astype(float) * (H.GROSS / n)
    return base().where(g, 0.0)


def dpair(rc, ra):
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd > FLOOR else np.nan)


def win(r, w):
    return r if w == "full" else (r.loc[:IS_END] if w == "IS" else r.loc[OOS_START:])


# ------------------------------------------------------------------ gates
def gates(uname, px, S, start):
    g = []
    worst_shared = worst_v1 = 0.0
    for gate in [None] + H.GATES:
        for conv in (("dg",) if gate is None else ("dg", "rw")):
            for b, ref in SHARED.items():
                if ref == "V1u":
                    continue
                a = targets_b(px, b, S, gate, conv).fillna(0.0).loc[start:]
                e = I124.targets_n(px, ref, S, gate, conv).fillna(0.0).loc[start:]
                worst_shared = max(worst_shared, float((a - e).abs().to_numpy().max()))
            a = targets_b(px, "VS5", S, gate, conv).fillna(0.0)
            e = I124.targets_n(px, "V1u", S, gate, conv).fillna(0.0)
            worst_v1 = max(worst_v1, float((a - e).abs().to_numpy().max()))
    g.append(("G1 shared books == idea 124 targets_n (all gate/conv)", worst_shared, 1e-15))
    g.append(("G2 VS5 == idea 94 V1u exactly (GROSS/5 == WV1)", worst_v1, 1e-15))
    worst = 0.0
    for b in BOOKS:
        W = targets_b(px, b, S)
        a = H.run(px, W, bps=PCOST)["r"].loc[start:]
        e = backtest(px, W, cost_bps=PCOST, freq=H.FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    g.append(("G3 control run() == engine.backtest", worst, 1e-12))
    d6 = float((targets_b(px, "TOPall", S, force_scaler=True).fillna(0.0)
                - targets_b(px, "TOPall", S, force_scaler=False).fillna(0.0))
               .abs().to_numpy().max())
    g.append(("G6 scaler is a NO-OP at n=all (unranked book)", d6, 1e-15))
    return g


# ------------------------------------------------------------------ D1/D2 grid
def build_grid(uname, kw):
    px = H.load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    S = signals(px)
    P("\n" + "=" * 120)
    P(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
      f" | eval {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    ms = metrics(spy)
    P(f"SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
      f"halves {bars['s1']:.3f}/{bars['s2']:.3f} OOS {bars['soos']:.3f}")
    P("=" * 120)
    for label, val, tol in gates(uname, px, S, start):
        ok = val < tol
        P(f"[gate] {label:52s} max|diff| = {val:.3e}  ({'PASS' if ok else 'FAIL'})")
        assert ok, label

    v2n = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
           for c in PUB_COSTS}
    v1n = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
           for c in PUB_COSTS}
    m2 = metrics(v2n[PCOST])
    P(f"[gate] LIVE RULES v2 @10bps: CAGR {m2['CAGR']:.2%} Sharpe {m2['Sharpe']:.4f} "
      f"MaxDD {m2['MaxDD']:.2%} halves {H.halves(v2n[PCOST])[0]:.4f}/{H.halves(v2n[PCOST])[1]:.4f}")

    rets, tinfo = {}, {}
    for b in BOOKS:
        for name, kind, kwargs, (gt, conv) in H.arm_specs():
            W = targets_b(px, b, S, gt, conv)
            tinfo[(b, name)] = dict(names=float((W.loc[start:] > 0).sum(axis=1).mean()))
            for c in COST_RUNGS:
                res = H.run(px, W, bps=c, **kwargs)
                rets[(b, name, c)] = res["r"].loc[start:]
                if c == PCOST:
                    tinfo[(b, name)]["gross"] = float(res["gross"].loc[start:].mean())
                    tinfo[(b, name)]["TO"] = float(res["to"].loc[start:].sum()
                                                   / metrics(res["r"].loc[start:])["Years"])
    rows = []
    for b in BOOKS:
        for c in PUB_COSTS:
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in ARMS:
                ra = rets[(b, name, c)]
                dc, dd, rate = dpair(rc, ra)
                rec = dict(uni=uname, npanel=px.shape[1], book=b, scaler=scaler_of(b),
                           n=n_of(b, px.shape[1]), cost=c, arm=name, kind=kind,
                           dCAGR=dc, dMaxDD=dd, rate=rate, published=bool(np.isfinite(rate)))
                for cc in COST_RUNGS:
                    rec[f"dMaxDD@{cc:.0f}"] = dpair(rets[(b, "control", cc)],
                                                    rets[(b, name, cc)])[1]
                    rec[f"dMaxDD_IS@{cc:.0f}"] = dpair(win(rets[(b, "control", cc)], "IS"),
                                                       win(rets[(b, name, cc)], "IS"))[1]
                for w in ("IS", "OOS"):
                    a, bb, cq = dpair(win(rc, w), win(ra, w))
                    rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = a, bb, cq
                ma_, mc_ = metrics(ra), metrics(rc)
                mg = H.margins(ra, bars)
                rec.update(CAGR=ma_["CAGR"], Sharpe=ma_["Sharpe"], MaxDD=ma_["MaxDD"],
                           H1=H.halves(ra)[0], H2=H.halves(ra)[1],
                           OOS_CAGR=metrics(win(ra, "OOS"))["CAGR"],
                           OOS_Sharpe=metrics(win(ra, "OOS"))["Sharpe"],
                           OOS_MaxDD=metrics(win(ra, "OOS"))["MaxDD"],
                           ctl_CAGR=mc_["CAGR"], ctl_MaxDD=mc_["MaxDD"], ctl_Sharpe=mc_["Sharpe"],
                           names=tinfo[(b, name)]["names"], gross=tinfo[(b, name)]["gross"],
                           TO=tinfo[(b, name)]["TO"],
                           p4a_v2=H.pass4a(ra, v2n[c]), p4a_v1=H.pass4a(ra, v1n[c]),
                           p4b=all(v > 0 for v in mg.values()),
                           f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-")
                rows.append(rec)
    G = pd.DataFrame(rows)
    G["D1_pass"] = np.all([G[f"dMaxDD@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    G["D2_pass"] = (G.dMaxDD_IS > 0) & (G.dMaxDD_OOS > 0)
    G["D1_pass_IS"] = np.all([G[f"dMaxDD_IS@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    extra = dict(spy=metrics(win(spy, "OOS"))["Sharpe"], spy_c=metrics(win(spy, "OOS"))["CAGR"],
                 spy_dd=metrics(win(spy, "OOS"))["MaxDD"],
                 v2=metrics(win(v2n[PCOST], "OOS"))["Sharpe"],
                 v2_c=metrics(win(v2n[PCOST], "OOS"))["CAGR"],
                 v1=metrics(win(v1n[PCOST], "OOS"))["Sharpe"])
    return px, start, S, G, rets, extra


# ------------------------------------------------------------------ D3 bootstrap
def bootstrap(uname, px, start):
    """idea 124's draw generator, rng stream IDENTICAL; only the q=0.10 block is run."""
    rng = np.random.default_rng(SEED)
    ncol = px.shape[1]
    out, t0 = [], time.time()
    for q in DROP_FRACS:
        k = int(round(ncol * (1 - q)))
        for d in range(NDRAW):
            keep = sorted(rng.choice(ncol, size=k, replace=False))
            if q != Q_RUN:
                continue                              # stream consumed, work skipped
            sub = px.iloc[:, keep]
            Ss = signals(sub)
            for b in BOOKS:
                rc = H.run(sub, targets_b(sub, b, Ss), bps=PCOST)["r"].loc[start:]
                for name, kind, kwargs, (gt, conv) in ARMS:
                    ra = H.run(sub, targets_b(sub, b, Ss, gt, conv), bps=PCOST,
                               **kwargs)["r"].loc[start:]
                    rec = dict(uni=uname, q=q, draw=d, nkeep=k, book=b,
                               scaler=scaler_of(b), arm=name)
                    for w in ("full", "IS", "OOS"):
                        a, bb, cq = dpair(win(rc, w), win(ra, w))
                        rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = a, bb, cq
                    out.append(rec)
            if (d + 1) % 10 == 0:
                P(f"    [{uname}] q={q:.2f} draw {d+1}/{NDRAW} x {len(BOOKS)} books "
                  f"({time.time()-t0:.0f}s)")
    return pd.DataFrame(out)


def d3_table(B):
    g = B.groupby(["uni", "q", "book", "arm"])
    return pd.DataFrame(dict(
        frac_pos_full=g.dMaxDD_full.apply(lambda s: float((s > 0).mean())),
        frac_pos_IS=g.dMaxDD_IS.apply(lambda s: float((s > 0).mean())),
        frac_pos_OOS=g.dMaxDD_OOS.apply(lambda s: float((s > 0).mean())),
        frac_priceable=g.rate_full.apply(lambda s: float(s.notna().mean())),
        dMaxDD_med=g.dMaxDD_full.median(), dCAGR_med=g.dCAGR_full.median(),
        rate_med=g.rate_full.median())).reset_index()


# ------------------------------------------------------------------ the screen
def screen(G, D3, q, tau, window="full"):
    d3 = D3[D3.q == q].set_index(["uni", "book", "arm"])
    col = {"full": "frac_pos_full", "IS": "frac_pos_IS", "OOS": "frac_pos_OOS"}[window]
    rows = []
    for _, r in G.iterrows():
        key = (r.uni, r.book, r.arm)
        f = float(d3.loc[key, col]) if key in d3.index else np.nan
        d3ok = bool(f >= tau)
        if window == "full":
            ok, pub = bool(r.D1_pass and r.D2_pass and d3ok), bool(r.published)
        elif window == "IS":
            ok, pub = bool(r.D1_pass_IS and d3ok), bool(np.isfinite(r.rate_IS))
        else:
            ok, pub = bool(r.dMaxDD_OOS > 0 and d3ok), bool(np.isfinite(r.rate_OOS))
        rows.append(dict(uni=r.uni, book=r.book, scaler=r.scaler, n=r.n, cost=r.cost,
                         arm=r.arm, published=pub, admissible=ok, d3=f, d3_pass=d3ok,
                         D1=bool(r.D1_pass), D2=bool(r.D2_pass)))
    return pd.DataFrame(rows)


def cellstats(A, key=("uni", "scaler", "n", "book")):
    g = A.groupby(list(key))
    return pd.DataFrame(dict(
        rows=g.size(), pub=g.published.sum(),
        adm_all=g.admissible.mean(),
        adm_pub=g.apply(lambda d: float(d.admissible[d.published].mean())
                        if d.published.any() else np.nan, include_groups=False),
        d3_pub=g.apply(lambda d: float(d.d3_pass[d.published].mean())
                       if d.published.any() else np.nan, include_groups=False),
    )).reset_index()


def matched(C):
    """OFF minus ON at matched (uni, n)."""
    off = C[C.scaler == "OFF"].set_index(["uni", "n"])
    on = C[C.scaler == "ON"].set_index(["uni", "n"])
    j = off.join(on, lsuffix="_off", rsuffix="_on", how="inner").reset_index()
    j["d_adm_pub"] = j.adm_pub_off - j.adm_pub_on
    j["d_adm_all"] = j.adm_all_off - j.adm_all_on
    j["d_d3_pub"] = j.d3_pub_off - j.d3_pub_on
    return j


# ------------------------------------------------------------------ W2
def walk_forward(G, rets_by_uni, extra_by_uni):
    out = []
    for (uname, b, c), cell in G.groupby(["uni", "book", "cost"]):
        rets = rets_by_uni[uname]
        elig = cell[(cell.dMaxDD_IS >= 1.0) & np.isfinite(cell.rate_IS)]
        pick = elig.sort_values("rate_IS").iloc[0].arm if len(elig) else None
        ro = win(rets[(b, "control", c)], "OOS"); mc = metrics(ro)
        ex = extra_by_uni[uname]
        rec = dict(uni=uname, book=b, scaler=cell.scaler.iloc[0], n=int(cell.n.iloc[0]),
                   cost=c, pick=pick, n_elig=len(elig), ctl_OOS_CAGR=mc["CAGR"],
                   ctl_OOS_Sharpe=mc["Sharpe"], ctl_OOS_MaxDD=mc["MaxDD"])
        if pick is not None:
            ra = win(rets[(b, pick, c)], "OOS"); ma = metrics(ra)
            dc, dd, rt = dpair(ro, ra)
            r_is = cell.set_index("arm").rate_IS; r_oos = cell.set_index("arm").rate_OOS
            rec.update(OOS_CAGR=ma["CAGR"], OOS_Sharpe=ma["Sharpe"], OOS_MaxDD=ma["MaxDD"],
                       IS_rate=float(cell[cell.arm == pick].rate_IS.iloc[0]),
                       OOS_rate=rt, OOS_dMaxDD=dd,
                       spearman_IS_OOS=H.spearman(r_is.values, r_oos.values),
                       n_both=int((np.isfinite(r_is.values) & np.isfinite(r_oos.values)).sum()))
        rec.update(spy_OOS_Sharpe=ex["spy"], spy_OOS_CAGR=ex["spy_c"],
                   spy_OOS_MaxDD=ex["spy_dd"], v2_OOS_Sharpe=ex["v2"],
                   v2_OOS_CAGR=ex["v2_c"], v1_OOS_Sharpe=ex["v1"])
        out.append(rec)
    return pd.DataFrame(out)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P("=" * 120)
    P("IDEA 381 — is the vol scaler the record's general instability source?  (cloud)")
    P(f"Books ({len(BOOKS)}): {BOOKS}.  Scaler = comp / clip(vol20,0.08)**0.5, the ONLY dial")
    P(f"inside a matched (n) pair.  {len(ARMS)} treated arms x {len(PUB_COSTS)} published "
      f"rungs x {len(UNIS)} panels.")
    P(f"Sign axes: D1 cost {COST_RUNGS}, D2 window IS/OOS, D3 panel {NDRAW} draws at "
      f"q={Q_RUN} (seed {SEED}, idea 124's stream).  tau reported at {TAUS}.")
    P(f"Pre-registered: SCALER if mean(adm_pub OFF-ON) >= {GAP_BAR:+.2f} and sign holds on "
      f">= {SIGN_BAR}/10 (panel x n) pairs; CONCENTRATION if spearman(n, adm_pub) >= "
      f"{RHO_BAR:+.2f} in both states on both panels and the gap < {GAP_BAR:+.2f}.")
    P("STRUCTURAL: VS5 IS V1u (GROSS/5 = 0.15 = WV1); the scaler is a no-op at n=all.")
    P("=" * 120)

    G_all, D3_all, rets_by_uni, extra_by_uni = [], [], {}, {}
    for uname, kw in UNIS:
        px, start, S, G, rets, extra = build_grid(uname, kw)
        G_all.append(G); rets_by_uni[uname] = rets; extra_by_uni[uname] = extra
        P(f"\n  [D3] {uname}: bootstrapping q={Q_RUN} ({NDRAW} draws x {len(BOOKS)} books "
          f"x {len(ARMS)} arms)")
        D3_all.append(bootstrap(uname, px, start))
    G = pd.concat(G_all, ignore_index=True)
    B = pd.concat(D3_all, ignore_index=True)
    D3 = d3_table(B)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    B.to_csv(f"{OUT}.draws.csv", index=False)
    D3.to_csv(f"{OUT}.d3.csv", index=False)

    # ---------------------------------------------------------- replication gates
    P("\n" + "=" * 120)
    P("[G4/G5] REPLICATION OF IDEA 124'S COMMITTED ARTEFACTS (shared books only)")
    ref = pd.read_csv(BT / "2026-09-07_book-size-floor-for-any-quoted-price_B.grid.csv")
    mine = G[G.book.isin(SHARED)].copy(); mine["refbook"] = mine.book.map(SHARED)
    M = ref.merge(mine, left_on=["uni", "book", "cost", "arm"],
                  right_on=["uni", "refbook", "cost", "arm"], suffixes=("_124", "_381"))
    cols = ["dCAGR", "dMaxDD", "dCAGR_IS", "dMaxDD_IS", "dCAGR_OOS", "dMaxDD_OOS",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
    d4 = max(float((M[c + "_124"] - M[c + "_381"]).abs().max()) for c in cols)
    P(f"    G4 grid rows: {len(M)} joined (expect {len(SHARED)*len(ARMS)*len(PUB_COSTS)*len(UNIS)})"
      f"  max|d| {d4:.3e}  ({'PASS' if d4 < 1e-9 else 'FAIL'})")
    assert len(M) == len(SHARED) * len(ARMS) * len(PUB_COSTS) * len(UNIS) and d4 < 1e-9
    refd3 = pd.read_csv(BT / "2026-09-07_book-size-floor-for-any-quoted-price_B.d3.csv")
    refd3 = refd3[refd3.q == Q_RUN]
    myd3 = D3.copy(); myd3["refbook"] = myd3.book.map(SHARED)
    M3 = refd3.merge(myd3[myd3.refbook.notna()], left_on=["uni", "q", "book", "arm"],
                     right_on=["uni", "q", "refbook", "arm"], suffixes=("_124", "_381"))
    c3 = ["frac_pos_full", "frac_pos_IS", "frac_pos_OOS", "frac_priceable", "dMaxDD_med",
          "dCAGR_med"]
    d5 = max(float((M3[c + "_124"] - M3[c + "_381"]).abs().max()) for c in c3)
    P(f"    G5 D3 rows at q={Q_RUN}: {len(M3)} joined  max|d| {d5:.3e}  "
      f"({'PASS' if d5 < 1e-9 else 'FAIL'})  — the rng stream replicates exactly")
    assert d5 < 1e-9

    # ---------------------------------------------------------- the headline
    A = screen(G, D3, Q_STAR, TAU_STAR, "full")
    A.to_csv(f"{OUT}.signtest.csv", index=False)
    C = cellstats(A)
    C.to_csv(f"{OUT}.cellstats.csv", index=False)
    P("\n" + "=" * 120)
    P(f"[1] THE LADDER, BOTH SCALER STATES (q={Q_STAR}, tau={TAU_STAR}) — "
      "adm_pub = share of PUBLISHED rows surviving D1+D2+D3")
    for uname, _ in UNIS:
        P(f"\n    {uname}")
        P(fmt(C[C.uni == uname].sort_values(["scaler", "n"])
              [["scaler", "book", "n", "rows", "pub", "adm_all", "adm_pub", "d3_pub"]]))
    Mt = matched(C)
    Mt.to_csv(f"{OUT}.matched.csv", index=False)
    P("\n[2] THE MATCHED CONTRAST — same n, same weights, scaler the ONLY difference")
    P(fmt(Mt[["uni", "n", "adm_pub_off", "adm_pub_on", "d_adm_pub", "d3_pub_off",
              "d3_pub_on", "d_d3_pub", "pub_off", "pub_on"]]))
    gap = float(Mt.d_adm_pub.mean()); gap3 = float(Mt.d_d3_pub.mean())
    nsign = int((Mt.d_adm_pub >= 0).sum())
    P(f"\n    mean(adm_pub OFF - ON) = {gap:+.4f} over {len(Mt)} (panel x n) pairs; "
      f"OFF >= ON on {nsign}/{len(Mt)}")
    P(f"    mean(d3_pub  OFF - ON) = {gap3:+.4f}  (the PANEL AXIS alone — idea 122's claim)")

    P("\n[2b] BY COST RUNG (the contrast must not be a single-rung artefact)")
    Cc = cellstats(A, key=("uni", "scaler", "n", "cost"))
    off = Cc[Cc.scaler == "OFF"].set_index(["uni", "n", "cost"])
    on = Cc[Cc.scaler == "ON"].set_index(["uni", "n", "cost"])
    J = off.join(on, lsuffix="_off", rsuffix="_on", how="inner").reset_index()
    J["d_adm_pub"] = J.adm_pub_off - J.adm_pub_on
    P(fmt(J[["uni", "n", "cost", "adm_pub_off", "adm_pub_on", "d_adm_pub"]]))
    P(f"    mean over {len(J)} (panel x n x cost) pairs: {float(J.d_adm_pub.mean()):+.4f}; "
      f"OFF >= ON on {int((J.d_adm_pub >= 0).sum())}/{len(J)}")

    P("\n[3] CONCENTRATION — spearman(n, adm_pub) inside each scaler state")
    rhos = []
    for uname, _ in UNIS:
        for sc in ("OFF", "ON"):
            d = C[(C.uni == uname) & (C.scaler == sc)].sort_values("n")
            rhos.append(dict(uni=uname, scaler=sc, n_rungs=len(d),
                             rho_n_adm_pub=H.spearman(d.n.values, d.adm_pub.values),
                             rho_n_d3_pub=H.spearman(d.n.values, d3 := d.d3_pub.values),
                             adm_pub_min=float(np.nanmin(d.adm_pub.values)),
                             adm_pub_max=float(np.nanmax(d.adm_pub.values))))
    R = pd.DataFrame(rhos)
    P(fmt(R))
    P(f"    TOPall (scaler is a proven no-op there): "
      + ", ".join(f"{u} adm_pub "
                  f"{float(C[(C.uni==u)&(C.book=='TOPall')].adm_pub.iloc[0]):.4f}"
                  for u, _ in UNIS))

    P(f"\n[4] TAU SENSITIVITY — the same contrast at tau in {TAUS} (q={Q_STAR})")
    tt = []
    for tau in TAUS:
        Mt_ = matched(cellstats(screen(G, D3, Q_STAR, tau, "full")))
        tt.append(dict(tau=tau, mean_gap=float(Mt_.d_adm_pub.mean()),
                       sign_pairs=int((Mt_.d_adm_pub >= 0).sum()), pairs=len(Mt_),
                       mean_gap_d3=float(Mt_.d_d3_pub.mean())))
    T = pd.DataFrame(tt); T.to_csv(f"{OUT}.tau.csv", index=False)
    P(fmt(T))

    # ---------------------------------------------------------- rule 8 / W1
    P("\n[5] RULE 8 / W1 — the CONTRAST recomputed IS-only, then read OOS untouched")
    w1 = []
    for wdw in ("IS", "OOS"):
        Mw = matched(cellstats(screen(G, D3, Q_STAR, TAU_STAR, wdw)))
        w1.append(dict(window=wdw, mean_gap=float(Mw.d_adm_pub.mean()),
                       sign_pairs=int((Mw.d_adm_pub >= 0).sum()), pairs=len(Mw),
                       mean_gap_d3=float(Mw.d_d3_pub.mean())))
    W1 = pd.DataFrame(w1 + [dict(window="full", mean_gap=gap, sign_pairs=nsign,
                                 pairs=len(Mt), mean_gap_d3=gap3)])
    W1.to_csv(f"{OUT}.w1.csv", index=False)
    P(fmt(W1))

    # ---------------------------------------------------------- rule 8 / W2
    P("\n[6] RULE 8 / W2 — idea 94's price-list selector per cell, evaluated OOS")
    W = walk_forward(G, rets_by_uni, extra_by_uni)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(W[["uni", "book", "scaler", "n", "cost", "pick", "n_elig", "IS_rate", "OOS_rate",
             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "ctl_OOS_Sharpe", "v2_OOS_Sharpe",
             "spy_OOS_Sharpe", "spearman_IS_OOS"]]))
    for sc, w in W.groupby("scaler"):
        w = w.dropna(subset=["OOS_Sharpe"])
        P(f"    scaler {sc:3s}: {len(w):>2d} cells with a pick | above SPY OOS "
          f"{int((w.OOS_Sharpe > w.spy_OOS_Sharpe).sum())}/{len(w)} | above RULES v2 OOS "
          f"{int((w.OOS_Sharpe > w.v2_OOS_Sharpe).sum())}/{len(w)} | above own control "
          f"{int((w.OOS_Sharpe > w.ctl_OOS_Sharpe).sum())}/{len(w)} | mean spearman(IS,OOS) "
          f"{float(w.spearman_IS_OOS.mean()):+.4f} | mean OOS Sharpe {float(w.OOS_Sharpe.mean()):.4f}")

    # ---------------------------------------------------------- KEEP paths
    P("\n[7] KEEP PATHS — 4a (vs live RULES v2) and 4b (vs SPY), every arm-point")
    for sc, g in G.groupby("scaler"):
        P(f"    scaler {sc:3s}: {len(g):>4d} arm-points | 4a {int(g.p4a_v2.sum())} | "
          f"4b {int(g.p4b.sum())}")
    p4b = G[G.p4b]
    if len(p4b):
        P("\n    4b passers:")
        P(fmt(p4b[["uni", "book", "scaler", "n", "cost", "arm", "CAGR", "Sharpe", "MaxDD",
                   "H1", "H2", "OOS_Sharpe"]]))
    else:
        P("\n    no 4b passers")
    p4a = G[G.p4a_v2]
    P(f"\n    4a passers: {len(p4a)}"
      + ("" if not len(p4a) else "\n" + fmt(p4a[["uni", "book", "scaler", "n", "cost", "arm",
                                                 "CAGR", "Sharpe", "MaxDD", "H1", "H2"]])))
    ffl = G[~G.p4b].f4b.str.split(",").explode()
    P("    failing 4b bars: " + ", ".join(f"{k} {v}" for k, v in ffl.value_counts().items()))

    # ---------------------------------------------------------- verdict
    P("\n[8] VERDICT")
    scaler_holds = (gap >= GAP_BAR) and (nsign >= SIGN_BAR)
    rho_ok = bool((R.rho_n_adm_pub >= RHO_BAR).all())
    conc_holds = rho_ok and (gap < GAP_BAR)
    read = ("BOTH" if (scaler_holds and rho_ok and gap >= GAP_BAR) else
            "SCALER" if scaler_holds else "CONCENTRATION" if conc_holds else "NEITHER")
    P(f"    mean adm_pub gap (OFF-ON) {gap:+.4f} vs bar {GAP_BAR:+.2f}; sign {nsign}/{len(Mt)} "
      f"vs bar {SIGN_BAR}/10  -> SCALER {'HOLDS' if scaler_holds else 'FAILS'}")
    P(f"    spearman(n, adm_pub) >= {RHO_BAR:+.2f} in all 4 (panel x state) cells: {rho_ok} "
      f"-> CONCENTRATION {'HOLDS' if conc_holds else 'FAILS'}")
    P(f"    panel-axis-only gap (D3 alone) {gap3:+.4f}")
    P(f"    pre-registered reading: {read}")
    P(f"\n    total {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
