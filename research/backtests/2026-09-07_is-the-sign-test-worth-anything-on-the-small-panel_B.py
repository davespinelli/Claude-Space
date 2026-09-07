#!/usr/bin/env python3
"""QUEUE idea 129 — is-the-sign-test-worth-anything-on-the-small-panel (lane B, 2026-09-07).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 122 showed the screen has ZERO out-of-sample discriminating power on u56/broad (OOS
denominator positive in 138/138 rows, admissible and rejected alike).  Idea 119's small panel
is where the sign actually moves, so run the identical IS-only screen there and ask the one
question that matters: does an IS-admissible small-panel denominator stay positive OOS more
often than a rejected one?  If not, the clause is cosmetic everywhere and PROTOCOL should say
so."

What is being tested.  Idea 122 proposed a PROTOCOL clause: no drawdown price
    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)
may be quoted unless its denominator dMaxDD survives three nuisance perturbations (D1 cost,
D2 window, D3 panel draws).  On the two large-cap lists the clause was harmless-but-inert:
two thirds of rows passed and the OOS denominator was positive in 138/138 rows, so the screen
separated nothing.  Idea 122 itself flagged the small panel (idea 119: sign held 49/80) as the
place where the denominator actually moves.  This run takes the SAME screen, the SAME books,
the SAME arms and the SAME grid to the sub-$2B panel and asks the discrimination question
directly, as a 2x2.

THE SCREEN (identical to idea 122; nothing re-tuned)
    D1 cost      dMaxDD > 0 at every cost rung in {0, 5, 10, 25} bps
    D2 window    dMaxDD > 0 in BOTH the IS and the OOS window          (full-sample form only)
    D3 panel     dMaxDD > 0 in >= tau of NDRAW=40 draws deleting a fraction q of the panel's
                 names at random, signals recomputed on the sub-panel so the book is re-formed
    IS-ONLY form (the one the queue asks for, and the only one a walk-forward may use):
                 ADM_IS = D1 on IS-window returns AND D3 on IS-window draws.  D2 has no
                 IS-only form and is excluded, exactly as in idea 122's S2.

THE ONE QUESTION, pre-registered as a 2x2 before any number below was read
        H_DISCRIM:  P(dMaxDD_OOS > 0 | ADM_IS)  >  P(dMaxDD_OOS > 0 | not ADM_IS)
    Reported as counts, as a difference of proportions, and with a deterministic two-sided
    permutation test (10,000 relabellings, seeded).  Also reported as a continuous version on
    the bootstrap: mean OOS draw-level sign-agreement by IS admissibility, and the rank
    correlation between IS and OOS sign-agreement.  PASS requires a positive gap that the
    permutation test does not attribute to chance at p <= 0.05.

CONFOUND CONTROLS for H_DISCRIM (a PASS is only interesting if the perturbation machinery
earns its keep over something trivial; each control is scored on the same 2x2)
    N1 naive sign      admit iff dMaxDD_IS > 0 at the published rung — one number, no
                       perturbation, no bootstrap
    N2 magnitude       admit the top-k rows by dMaxDD_IS with k = the screen's own admitted
                       count, so the two screens are matched on selectivity
    N3 ROC             rank-AUC of dMaxDD_IS (continuous) for predicting the OOS sign, with
                       the screen plotted as a point (TPR, FPR).  A screen that lies on the
                       magnitude ROC adds nothing to a number already in every row
    N4 kind strata     the same 2x2 computed WITHIN each instrument kind (gate / dd / stop /
                       bud), since kind alone may drive both admission and OOS sign
    N5 incremental     the 2x2 restricted to rows with dMaxDD_IS > 0, i.e. what the two
                       perturbation axes add once the naive sign is already known

Tuned parameters (PROTOCOL rule 4).  TWO, both of the TEST and neither of any trading rule:
    q    drop fraction in {0.05, 0.10, 0.20}
    tau  sign-agreement threshold in {0.80, 0.90, 0.95, 1.00}
ALL 12 grid points reported.  (q, tau) = (0.10, 0.90) is the pre-registered headline, adopted
unchanged from ideas 119/122 so this run cannot pick its own bar.

Panel / books / arms: idea 94's module is imported, not re-implemented.
    panel   data/prices_small.csv, the 484-column sub-$2B screen panel (483 small caps + SPY
            as the benchmark column, which idea 119's convention leaves in the draw pool)
    books   V1u (v1's composite, ungated, top-5 @15%), TOP20 (idea 2's ranking, ungated),
            EWall (equal-weight every name @75% gross)
    arms    5 gates x {de-gross, reweight}, 2 trailing stops, 2 book DD controls, 2 entry-only
            turnover budgets  (16 treated arms + control)
    costs   published at 10 and 25 bps -> 3 books x 16 arms x 2 rungs = 96 audited rows

Walk-forward (PROTOCOL rule 8), fixed before any OOS number was read
    S1  idea 94's selector, unchanged: in each (book, cost) cell, among arms that bought
        >= 1.0 pp of IS MaxDD, pick the LOWEST IS rate; evaluate untouched on 2017-2026.
    S2  the same selector restricted to arms passing ADM_IS.  The OOS window is never
        consulted by the screen.
    Reported for both at all 12 grid points: OOS CAGR / Sharpe / MaxDD vs the cell's own
    control, vs the live book (RULES v2), vs RULES v1 and vs SPY.

Pre-registered predictions (written before any number was read)
    P1  The small-panel OOS denominator is NOT degenerate: strictly between 60% and 95% of the
        96 rows have dMaxDD_OOS > 0 (idea 122 got 100% on the large-cap lists).
    P2  H_DISCRIM FAILS: the IS screen buys < 10 pp of OOS sign rate and p > 0.05.  The
        screen's axes are nuisance dimensions of the SAME window, so they measure IS noise,
        not OOS persistence.
    P2b If P2 is refuted, the controls carry the finding: the screen does NOT beat the naive
        dMaxDD_IS > 0 rule (N1) by more than 5 pp of OOS sign rate, and its point lies on the
        magnitude ROC (N3).  Registered before the controls were computed.
    P3  The screen is again near-inert in selection: it changes at most 2 of 6 walk-forward
        picks at the headline setting.
    P4  No new KEEP.  Neither selector passes 4b; the small panel has passed 4b 0 times in
        the record (ideas 117/121/136 and six reproductions).

Execution realism (PROTOCOL rule 2): inherited from idea 94 — weekly decision at close t
applied at t+1, long-only, no leverage, costs charged inside the loop so both state machines
see NET equity.  10 bps is the PROTOCOL point.

SURVIVORSHIP: data/prices_small.csv is a CURRENT-CONSTITUENT screen (see
data/SMALL_PANEL_README.md).  Every absolute level below is optimistic.  This run reports
within-cell differences and the stability of a SIGN, both far less exposed than levels, but a
delisting-aware panel could still move which rows pass.

Deterministic (seeded), standalone.  Imports research/baseline.py and idea 94's script;
modifies nothing.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location(
    "i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)

STEM = Path(__file__).stem
OUT = BT / STEM
PCOST = 10.0
COST_RUNGS = [0.0, 5.0, 10.0, 25.0]           # D1
PUB_COSTS = [10.0, 25.0]                      # the rungs idea 94 published
IS_END, OOS_START = H.IS_END, H.OOS_START
BOOKS = list(H.BOOKS)
ARMS = [(n, k, kw, sp) for (n, k, kw, sp) in H.arm_specs() if n != "control"]
NDRAW, DROP_FRACS, TAUS, SEED = 40, (0.05, 0.10, 0.20), (0.80, 0.90, 0.95, 1.00), 20260905
Q_STAR, TAU_STAR = 0.10, 0.90                 # pre-registered headline (ideas 119/122)
FLOOR = 0.10                                  # idea 94's absolute floor, kept for continuity
NPERM = 10000
PANEL = "small(sub-$2B)"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)


def fmt(df):
    return df.to_string(index=False, float_format=lambda x: f"{x:.4f}")


# ---------------------------------------------------------------- cached signal path
def signals(px):
    return dict(comp=H.composite(px), v20=H.vol20(px), ma=px.rolling(200).mean())


def gmask_c(px, gate, S):
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


def targets_c(px, book, S, gate=None, conv="dg"):
    """H.targets with cached signals.  Asserted identical to H.targets on the full panel."""
    def base():
        if book == "EWall":
            e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
            return H.GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        s = S["comp"] / S["v20"].clip(lower=0.08) ** 0.5 if book == "V1u" else S["comp"]
        n, w = (H.NV1, H.WV1) if book == "V1u" else (H.NTOP, H.GROSS / H.NTOP)
        return (s.rank(axis=1, ascending=False) <= n).astype(float) * w

    if gate is None:
        return base()
    g = gmask_c(px, gate, S)
    if conv == "rw":
        if book == "EWall":
            e = g.astype(float)
            return H.GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        s = S["comp"] / S["v20"].clip(lower=0.08) ** 0.5 if book == "V1u" else S["comp"]
        n, w = (H.NV1, H.WV1) if book == "V1u" else (H.NTOP, H.GROSS / H.NTOP)
        return (s.where(g).rank(axis=1, ascending=False) <= n).astype(float) * w
    return base().where(g, 0.0)


# ---------------------------------------------------------------- price primitives
def dpair(rc, ra):
    """(dCAGR, dMaxDD) in pp, and idea 94's rate with its absolute floor."""
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd > FLOOR else np.nan)


def win(r, w):
    return r if w == "full" else (r.loc[:IS_END] if w == "IS" else r.loc[OOS_START:])


def perm_test(flag, adm, nperm=NPERM, seed=SEED):
    """Two-sided permutation test on the difference of proportions P(flag|adm)-P(flag|~adm).
    Returns (p_adm, p_rej, gap, pvalue, n_adm, n_rej).  Exact-by-construction under the null
    that admissibility labels are exchangeable."""
    flag = np.asarray(flag, bool)
    adm = np.asarray(adm, bool)
    n_adm, n_rej = int(adm.sum()), int((~adm).sum())
    if n_adm == 0 or n_rej == 0:
        return (float(flag[adm].mean()) if n_adm else np.nan,
                float(flag[~adm].mean()) if n_rej else np.nan,
                np.nan, np.nan, n_adm, n_rej)
    p1, p0 = float(flag[adm].mean()), float(flag[~adm].mean())
    obs = p1 - p0
    rng = np.random.default_rng(seed)
    idx = np.arange(len(flag))
    hits = 0
    for _ in range(nperm):
        perm = rng.permutation(idx)[:n_adm]
        m = np.zeros(len(flag), bool)
        m[perm] = True
        if abs(float(flag[m].mean()) - float(flag[~m].mean())) >= abs(obs) - 1e-12:
            hits += 1
    return p1, p0, obs, (hits + 1) / (nperm + 1), n_adm, n_rej


def auc(score, flag):
    """Rank AUC of a continuous score for a binary flag (ties handled by mid-rank)."""
    score, flag = np.asarray(score, float), np.asarray(flag, bool)
    ok = np.isfinite(score)
    score, flag = score[ok], flag[ok]
    n1, n0 = int(flag.sum()), int((~flag).sum())
    if n1 == 0 or n0 == 0:
        return np.nan
    r = pd.Series(score).rank().values
    return float((r[flag].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or np.std(a[ok]) == 0 or np.std(b[ok]) == 0:
        return np.nan
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


# ---------------------------------------------------------------- main grid (D1, D2)
def build_grid(px, start, spy, bars):
    S = signals(px)

    worst_t = 0.0
    for b in BOOKS:
        for g in [None] + H.GATES:
            for conv in (("dg",) if g is None else ("dg", "rw")):
                a = targets_c(px, b, S, g, conv).fillna(0.0)
                e = H.targets(px, b, g, conv).fillna(0.0)
                worst_t = max(worst_t, float((a - e).abs().to_numpy().max()))
    print(f"[check] cached targets vs idea 94 targets(): max|diff| = {worst_t:.3e} "
          f"({'EXACT' if worst_t < 1e-15 else 'NOT EXACT — unsafe'})")

    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c,
                          freq=H.FREQ)["returns"].loc[start:] for c in PUB_COSTS}
    v2_net = {c: backtest(px, rules_v2_weights(px), cost_bps=c,
                          freq=H.FREQ)["returns"].loc[start:] for c in PUB_COSTS}

    rets = {}
    t0 = time.time()
    for b in BOOKS:
        for name, kind, kwargs, (g, conv) in H.arm_specs():
            W = targets_c(px, b, S, g, conv)
            for c in COST_RUNGS:
                rets[(b, name, c)] = H.run(px, W, bps=c, **kwargs)["r"].loc[start:]
        print(f"    book {b}: arm x cost grid done ({time.time()-t0:.0f}s)", flush=True)

    rows = []
    for b in BOOKS:
        for c in PUB_COSTS:
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in ARMS:
                ra = rets[(b, name, c)]
                dc, dd, rate = dpair(rc, ra)
                rec = dict(panel=PANEL, book=b, cost=c, arm=name, kind=kind,
                           dCAGR=dc, dMaxDD=dd, rate=rate,
                           published=bool(np.isfinite(rate)))
                for cc in COST_RUNGS:                              # D1 (full and IS-only)
                    _, dd_c, _ = dpair(rets[(b, "control", cc)], rets[(b, name, cc)])
                    rec[f"dMaxDD@{cc:.0f}"] = dd_c
                    _, dd_ci, _ = dpair(win(rets[(b, "control", cc)], "IS"),
                                        win(rets[(b, name, cc)], "IS"))
                    rec[f"dMaxDD_IS@{cc:.0f}"] = dd_ci
                for w in ("IS", "OOS"):                            # D2
                    dcw, ddw, rw_ = dpair(win(rc, w), win(ra, w))
                    rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dcw, ddw, rw_
                ma_, mc_ = metrics(ra), metrics(rc)
                mo_ = metrics(ra.loc[OOS_START:])
                mg = H.margins(ra, bars)
                rec.update(CAGR=ma_["CAGR"], Sharpe=ma_["Sharpe"], MaxDD=ma_["MaxDD"],
                           OOS_CAGR=mo_["CAGR"], OOS_Sharpe=mo_["Sharpe"],
                           OOS_MaxDD=mo_["MaxDD"],
                           ctl_MaxDD=mc_["MaxDD"], ctl_CAGR=mc_["CAGR"],
                           p4a_v2=H.pass4a(ra, v2_net[c]), p4a_v1=H.pass4a(ra, v1_net[c]),
                           p4b=all(v > 0 for v in mg.values()),
                           f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-")
                rows.append(rec)
    G = pd.DataFrame(rows)
    G["D1_pass"] = np.all([G[f"dMaxDD@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    G["D2_pass"] = (G.dMaxDD_IS > 0) & (G.dMaxDD_OOS > 0)
    G["D1_pass_IS_only"] = np.all([G[f"dMaxDD_IS@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    return S, v1_net, v2_net, rets, G


# ---------------------------------------------------------------- D3 bootstrap
def bootstrap(px, start):
    """Name-subsample draws.  Signals recomputed on each sub-panel so the book is genuinely
    re-formed; the draw is uniform over ALL panel columns (idea 119's convention)."""
    rng = np.random.default_rng(SEED)
    ncol = px.shape[1]
    out = []
    t0 = time.time()
    for q in DROP_FRACS:
        k = int(round(ncol * (1 - q)))
        for d in range(NDRAW):
            keep = sorted(rng.choice(ncol, size=k, replace=False))
            sub = px.iloc[:, keep]
            Ss = signals(sub)
            for b in BOOKS:
                rc = H.run(sub, targets_c(sub, b, Ss), bps=PCOST)["r"].loc[start:]
                for name, kind, kwargs, (g, conv) in ARMS:
                    ra = H.run(sub, targets_c(sub, b, Ss, g, conv), bps=PCOST,
                               **kwargs)["r"].loc[start:]
                    rec = dict(panel=PANEL, q=q, draw=d, book=b, arm=name)
                    for w in ("full", "IS", "OOS"):
                        dc, dd, rt = dpair(win(rc, w), win(ra, w))
                        rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dc, dd, rt
                    out.append(rec)
            if (d + 1) % 10 == 0:
                print(f"    q={q:.2f}: {d+1}/{NDRAW} draws ({time.time()-t0:.0f}s)", flush=True)
    return pd.DataFrame(out)


def d3_table(B):
    g = B.groupby(["q", "book", "arm"])
    return pd.DataFrame(dict(
        frac_pos_full=g.dMaxDD_full.apply(lambda s: float((s > 0).mean())),
        frac_pos_IS=g.dMaxDD_IS.apply(lambda s: float((s > 0).mean())),
        frac_pos_OOS=g.dMaxDD_OOS.apply(lambda s: float((s > 0).mean())),
        frac_priceable=g.rate_full.apply(lambda s: float(s.notna().mean())),
        rate_med=g.rate_full.median(),
        dMaxDD_med=g.dMaxDD_full.median(), dCAGR_med=g.dCAGR_full.median(),
    )).reset_index()


# ---------------------------------------------------------------- walk-forward
def walk_forward(G, D3, rets, v1_net, v2_net, spy):
    """S1 = idea 94's selector.  S2 = the same selector after the IS-ONLY sign screen."""
    out = []
    for (b, c), cell in G.groupby(["book", "cost"]):
        ctl_o = metrics(rets[(b, "control", c)].loc[OOS_START:])
        v1_o = metrics(v1_net[c].loc[OOS_START:])
        v2_o = metrics(v2_net[c].loc[OOS_START:])
        spy_o = metrics(spy.loc[OOS_START:])
        base = cell[(cell.dMaxDD_IS >= 1.0) & np.isfinite(cell.rate_IS)]
        for q in DROP_FRACS:
            for tau in TAUS:
                d3 = D3[(D3.q == q) & (D3.book == b)].set_index("arm").frac_pos_IS
                s2 = base[base.arm.map(lambda a: d3.get(a, 0.0) >= tau) & base.D1_pass_IS_only]
                for sel, sub in (("S1", base), ("S2", s2)):
                    if sel == "S1" and (q, tau) != (DROP_FRACS[0], TAUS[0]):
                        continue
                    rec = dict(panel=PANEL, book=b, cost=c, q=q, tau=tau, selector=sel,
                               ctl_OOS_CAGR=ctl_o["CAGR"], ctl_OOS_Sharpe=ctl_o["Sharpe"],
                               ctl_OOS_MaxDD=ctl_o["MaxDD"],
                               v1_OOS_Sharpe=v1_o["Sharpe"], v2_OOS_Sharpe=v2_o["Sharpe"],
                               v2_OOS_CAGR=v2_o["CAGR"], v2_OOS_MaxDD=v2_o["MaxDD"],
                               spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_Sharpe=spy_o["Sharpe"],
                               spy_OOS_MaxDD=spy_o["MaxDD"], n_eligible=len(sub))
                    if sub.empty:
                        rec.update(pick="NOTHING ADMISSIBLE", IS_rate=np.nan, OOS_rate=np.nan,
                                   OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                   p4a=False, p4b=False)
                    else:
                        pk = sub.sort_values("rate_IS").iloc[0]
                        ro = rets[(b, pk.arm, c)].loc[OOS_START:]
                        mo = metrics(ro)
                        rec.update(pick=pk.arm, IS_rate=pk.rate_IS, OOS_rate=pk.rate_OOS,
                                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                   OOS_MaxDD=mo["MaxDD"], p4a=bool(pk.p4a_v2),
                                   p4b=bool(pk.p4b))
                    out.append(rec)
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    print(__doc__.split("Deterministic")[0])
    print("=" * 200)
    print(f"PRE-REGISTERED: screen D1 costs {COST_RUNGS} bps | D2 windows IS/OOS | "
          f"D3 {NDRAW} draws x q in {DROP_FRACS} (seed {SEED}), tau in {TAUS}; "
          f"headline (q,tau) = ({Q_STAR}, {TAU_STAR}); permutation test {NPERM} draws")
    print("=" * 200)

    px = load_universe(small=True)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
    print(f"\nPANEL {PANEL}: {px.shape[1]} columns {px.index[0].date()} -> "
          f"{px.index[-1].date()} | eval from {start.date()} | IS <= {IS_END} | "
          f"OOS >= {OOS_START}")
    print(f"SPY  full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%}  halves "
          f"{bars['s1']:.3f}/{bars['s2']:.3f}  OOS {mso['CAGR']:.2%}/{mso['Sharpe']:.3f}/"
          f"{mso['MaxDD']:.2%}")

    S, v1_net, v2_net, rets, G = build_grid(px, start, spy, bars)
    print(f"\nD3 bootstrap: {len(DROP_FRACS)} x {NDRAW} draws x {len(BOOKS)} books x "
          f"{len(ARMS)} arms + control ...", flush=True)
    bcache = next((p for p in (Path(f"{OUT}.bootstrap.csv.gz"), Path(f"{OUT}.bootstrap.csv"))
                   if p.exists()), Path(f"{OUT}.bootstrap.csv"))
    if bcache.exists():
        # The draws are seeded, so the cache is bit-identical to a recomputation; delete the
        # file to force the ~35 min re-run.  Standalone from scratch either way.
        print(f"    [cache] reading {bcache.name} (seeded draws, identical to recomputation)")
        B = pd.read_csv(bcache)
    else:
        B = bootstrap(px, start)
        B.to_csv(bcache, index=False)
    D3 = d3_table(B)
    D3.to_csv(f"{OUT}.d3.csv", index=False)

    d3s = D3[D3.q == Q_STAR].set_index(["book", "arm"])
    G["D3_frac_full"] = [d3s.frac_pos_full.get((b, a), np.nan) for b, a in zip(G.book, G.arm)]
    G["D3_frac_IS"] = [d3s.frac_pos_IS.get((b, a), np.nan) for b, a in zip(G.book, G.arm)]
    G["D3_frac_OOS"] = [d3s.frac_pos_OOS.get((b, a), np.nan) for b, a in zip(G.book, G.arm)]
    G["D3_pass"] = G.D3_frac_full >= TAU_STAR
    G["D3_pass_IS_only"] = G.D3_frac_IS >= TAU_STAR
    G["ADMISSIBLE"] = G.D1_pass & G.D2_pass & G.D3_pass
    G["ADM_IS"] = G.D1_pass_IS_only & G.D3_pass_IS_only
    G["OOS_sign_pos"] = G.dMaxDD_OOS > 0
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ------------------------------------------------ A. is the premise true here?
    print("\n" + "=" * 200)
    print("A. THE PREMISE — does the small-panel denominator actually move?  "
          "(idea 122 got OOS-positive 138/138 on u56/broad)")
    pub = G[G.published].copy()
    prem = pd.DataFrame([dict(
        window=w, n=len(G), n_pos=int((G[f"dMaxDD_{w}"] > 0).sum()) if w != "full"
        else int((G.dMaxDD > 0).sum()),
        frac_pos=float((G[f"dMaxDD_{w}"] > 0).mean()) if w != "full"
        else float((G.dMaxDD > 0).mean()),
        median_dMaxDD=float(G[f"dMaxDD_{w}"].median()) if w != "full"
        else float(G.dMaxDD.median()))
        for w in ("full", "IS", "OOS")])
    print(fmt(prem))
    print(f"    published rows (idea 94 floor dMaxDD > {FLOOR} pp): {len(pub)} of {len(G)}")
    p1_lo, p1_hi = 0.60, 0.95
    oos_frac = float((G.dMaxDD_OOS > 0).mean())
    print(f"    P1 (0.60 < frac_pos_OOS < 0.95): frac = {oos_frac:.4f} -> "
          f"{'CONFIRMED' if p1_lo < oos_frac < p1_hi else 'REFUTED'}")
    prem.to_csv(f"{OUT}.premise.csv", index=False)

    print("\n--- draw-level sign agreement (D3, q = headline), by book ---")
    dd = D3[D3.q == Q_STAR].groupby("book")[["frac_pos_full", "frac_pos_IS", "frac_pos_OOS"]] \
        .median().reset_index()
    print(fmt(dd))

    # ------------------------------------------------ B. THE 2x2, all 12 grid points
    print("\n" + "=" * 200)
    print("B. H_DISCRIM — does an IS-ADMISSIBLE denominator stay positive OOS more often "
          "than a rejected one?  IS-only screen (D1_IS & D3_IS), all 12 grid points.")
    rowsB = []
    for q in DROP_FRACS:
        d3q = D3[D3.q == q].set_index(["book", "arm"]).frac_pos_IS
        fIS = np.array([d3q.get((b, a), np.nan) for b, a in zip(G.book, G.arm)])
        fOOSc = np.array([D3[D3.q == q].set_index(["book", "arm"]).frac_pos_OOS.get((b, a), np.nan)
                          for b, a in zip(G.book, G.arm)])
        for tau in TAUS:
            adm = G.D1_pass_IS_only.values & (fIS >= tau)
            p1, p0, gap, pv, na, nr = perm_test(G.OOS_sign_pos.values, adm)
            # continuous version: mean OOS draw-level agreement by IS admissibility
            c1 = float(np.nanmean(fOOSc[adm])) if na else np.nan
            c0 = float(np.nanmean(fOOSc[~adm])) if nr else np.nan
            rowsB.append(dict(q=q, tau=tau, n_adm=na, n_rej=nr,
                              OOSpos_if_adm=p1, OOSpos_if_rej=p0, gap=gap, perm_p=pv,
                              OOSagree_if_adm=c1, OOSagree_if_rej=c0,
                              cont_gap=(c1 - c0) if (na and nr) else np.nan,
                              headline=(q == Q_STAR and tau == TAU_STAR)))
    DISC = pd.DataFrame(rowsB)
    print(fmt(DISC))
    DISC.to_csv(f"{OUT}.discrimination.csv", index=False)

    hd = DISC[DISC.headline].iloc[0]
    passed = bool(np.isfinite(hd.gap) and hd.gap > 0 and np.isfinite(hd.perm_p)
                  and hd.perm_p <= 0.05)
    print(f"\n    HEADLINE (q={Q_STAR}, tau={TAU_STAR}): "
          f"P(OOS sign +ve | admissible) = {hd.OOSpos_if_adm:.4f} ({hd.n_adm} rows) vs "
          f"{hd.OOSpos_if_rej:.4f} ({hd.n_rej} rows), gap {hd.gap:+.4f}, perm p = {hd.perm_p:.4f}")
    print(f"    H_DISCRIM: {'PASS' if passed else 'FAIL'}")
    npos = int(((DISC.gap > 0) & (DISC.perm_p <= 0.05)).sum())
    print(f"    grid points with a positive, significant gap: {npos} of {len(DISC)}")
    print(f"    P2 (gap < 0.10 pp-fraction AND p > 0.05 at headline): "
          f"{'CONFIRMED' if (not passed) and (not np.isfinite(hd.gap) or hd.gap < 0.10) else 'REFUTED'}")

    # rank correlation IS vs OOS sign agreement (continuous, per book-arm, all q)
    print("\n--- continuous form: spearman(frac_pos_IS, frac_pos_OOS) over 51 book-arms ---")
    sp = pd.DataFrame([dict(q=q, spearman_IS_OOS=spearman(
        D3[D3.q == q].frac_pos_IS, D3[D3.q == q].frac_pos_OOS),
        n=len(D3[D3.q == q])) for q in DROP_FRACS])
    print(fmt(sp))
    sp.to_csv(f"{OUT}.rankcorr.csv", index=False)

    # the same 2x2 with the FULL (D1+D2+D3) screen, for continuity with idea 122's headline
    p1f, p0f, gapf, pvf, naf, nrf = perm_test(G.OOS_sign_pos.values, G.ADMISSIBLE.values)
    print(f"\n--- continuity check: idea 122's FULL three-axis screen on this panel — "
          f"admissible {naf}/{len(G)} ({naf/len(G):.1%}); "
          f"idea 122 got 90/138 (65.2%) on the large-cap lists ---")
    print(f"    (the full screen contains D2, which reads the OOS window, so its 2x2 is "
          f"circular and is reported for continuity only: {p1f:.4f} vs {p0f:.4f})")

    # ------------------------------------------------ B2. confound controls
    print("\n" + "=" * 200)
    print("B2. CONFOUND CONTROLS — does the perturbation machinery beat something trivial?")
    y = G.OOS_sign_pos.values
    adm_h = G.ADM_IS.values                       # the headline screen
    k = int(adm_h.sum())
    mag = G.dMaxDD_IS.values
    order = np.argsort(-np.nan_to_num(mag, nan=-1e18))
    topk = np.zeros(len(G), bool)
    topk[order[:k]] = True
    naive = mag > 0

    ctrl = []
    for nm, a in (("SCREEN ADM_IS (D1_IS & D3_IS)", adm_h),
                  ("N1 naive dMaxDD_IS > 0", naive),
                  (f"N2 top-{k} by dMaxDD_IS", topk)):
        p1, p0, gap, pv, na, nr = perm_test(y, a)
        ctrl.append(dict(control=nm, n_adm=na, n_rej=nr, OOSpos_if_adm=p1,
                         OOSpos_if_rej=p0, gap=gap, perm_p=pv,
                         agree_with_screen=float((a == adm_h).mean())))
    CTRL = pd.DataFrame(ctrl)
    print(fmt(CTRL))
    a_mag = auc(mag, y)
    tpr = float(adm_h[y].mean()) if y.sum() else np.nan
    fpr = float(adm_h[~y].mean()) if (~y).sum() else np.nan
    print(f"\n    N3 ROC: AUC(dMaxDD_IS -> OOS sign) = {a_mag:.4f}; the screen sits at "
          f"(FPR {fpr:.4f}, TPR {tpr:.4f}).  A screen ON the magnitude curve adds nothing.")
    print(f"       AUC of the screen itself (binary) = {auc(adm_h.astype(float), y):.4f}; "
          f"AUC(D3_frac_IS) = {auc(G.D3_frac_IS.values, y):.4f}")
    scr_gap = float(CTRL.gap.iloc[0])
    n1_gap = float(CTRL.gap.iloc[1])
    print(f"    P2b (screen beats N1 by <= 5 pp): screen {scr_gap:+.4f} vs N1 {n1_gap:+.4f}, "
          f"delta {scr_gap - n1_gap:+.4f} -> "
          f"{'CONFIRMED' if (scr_gap - n1_gap) <= 0.05 else 'REFUTED'}")

    print("\n    N4 within instrument-kind strata (kind may drive both admission and sign):")
    st = []
    for kd, d in G.groupby("kind"):
        p1, p0, gap, pv, na, nr = perm_test(d.OOS_sign_pos.values, d.ADM_IS.values)
        st.append(dict(kind=kd, n=len(d), n_adm=na, n_rej=nr, OOSpos_if_adm=p1,
                       OOSpos_if_rej=p0, gap=gap, perm_p=pv))
    ST = pd.DataFrame(st)
    print(fmt(ST))
    kind_auc = auc(G.groupby("kind").OOS_sign_pos.transform("mean").values, y)
    print(f"       AUC of instrument KIND alone (its mean OOS sign rate) = {kind_auc:.4f}")

    print("\n    N5 incremental: the 2x2 restricted to rows whose naive IS sign is already "
          "positive")
    sub = G[naive]
    p1, p0, gap, pv, na, nr = perm_test(sub.OOS_sign_pos.values, sub.ADM_IS.values)
    print(f"       n = {len(sub)} ({na} admitted / {nr} rejected): {p1:.4f} vs {p0:.4f}, "
          f"gap {gap:+.4f}, perm p = {pv if np.isfinite(pv) else float('nan'):.4f}")
    ST.to_csv(f"{OUT}.strata.csv", index=False)
    CTRL.loc[len(CTRL)] = dict(control="N5 incremental (within naive-positive)", n_adm=na,
                               n_rej=nr, OOSpos_if_adm=p1, OOSpos_if_rej=p0, gap=gap,
                               perm_p=pv, agree_with_screen=np.nan)
    CTRL.to_csv(f"{OUT}.controls.csv", index=False)

    print("\n--- where the IS screen's rejections live (headline) ---")
    by = G.groupby("book").agg(n=("arm", "size"), adm_IS=("ADM_IS", "sum"),
                               D1_IS=("D1_pass_IS_only", "sum"),
                               D3_IS=("D3_pass_IS_only", "sum"),
                               OOS_pos=("OOS_sign_pos", "sum"),
                               med_dMaxDD_IS=("dMaxDD_IS", "median"),
                               med_dMaxDD_OOS=("dMaxDD_OOS", "median")).reset_index()
    print(fmt(by))
    by2 = G.groupby("kind").agg(n=("arm", "size"), adm_IS=("ADM_IS", "sum"),
                                OOS_pos=("OOS_sign_pos", "sum"),
                                med_dMaxDD_IS=("dMaxDD_IS", "median"),
                                med_dMaxDD_OOS=("dMaxDD_OOS", "median")).reset_index()
    print(fmt(by2))

    # ------------------------------------------------ C. the row-by-row list
    print("\n" + "=" * 200)
    print(f"C. THE SMALL-PANEL PRICE LIST UNDER THE SCREEN — {len(G)} rows, "
          f"{len(pub)} carry a publishable rate")
    print(fmt(G[["book", "cost", "arm", "dCAGR", "dMaxDD", "rate", "published",
                 "dMaxDD_IS", "dMaxDD_OOS", "D1_pass_IS_only", "D3_frac_IS", "D3_frac_OOS",
                 "ADM_IS", "OOS_sign_pos", "ADMISSIBLE", "p4a_v2", "p4b", "f4b"]]))

    # ------------------------------------------------ D. rule 8 walk-forward
    print("\n" + "=" * 200)
    print("D. RULE 8 WALK-FORWARD — parameters chosen on IS only, OOS read once")
    WF = walk_forward(G, D3, rets, v1_net, v2_net, spy)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(fmt(WF[["book", "cost", "q", "tau", "selector", "n_eligible", "pick", "IS_rate",
                  "OOS_rate", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "ctl_OOS_Sharpe",
                  "v2_OOS_Sharpe", "spy_OOS_Sharpe", "p4a", "p4b"]]))

    s1 = WF[WF.selector == "S1"].set_index(["book", "cost"])
    changed = []
    for (q, tau), sub in WF[WF.selector == "S2"].groupby(["q", "tau"]):
        n_ch = 0
        for _, r in sub.iterrows():
            if r.pick != s1.loc[(r.book, r.cost), "pick"]:
                n_ch += 1
        changed.append(dict(q=q, tau=tau, picks_changed=n_ch, n_cells=len(sub),
                            S2_mean_OOS_Sharpe=float(sub.OOS_Sharpe.mean()),
                            S2_empty_cells=int((sub.pick == "NOTHING ADMISSIBLE").sum())))
    CH = pd.DataFrame(changed)
    CH["S1_mean_OOS_Sharpe"] = float(WF[WF.selector == "S1"].OOS_Sharpe.mean())
    print("\n--- selection effect of the screen (S2 vs S1), all 12 grid points ---")
    print(fmt(CH))
    CH.to_csv(f"{OUT}.selection.csv", index=False)
    hcell = CH[(CH.q == Q_STAR) & (CH.tau == TAU_STAR)].iloc[0]
    print(f"    P3 (<= 2 of {int(hcell.n_cells)} picks changed at headline): "
          f"{int(hcell.picks_changed)} -> "
          f"{'CONFIRMED' if hcell.picks_changed <= 2 else 'REFUTED'}")

    # ------------------------------------------------ E. both KEEP paths
    print("\n" + "=" * 200)
    print("E. BOTH KEEP PATHS (PROTOCOL rule 4) over all audited arm-points")
    kp = pd.DataFrame([dict(
        scope=s, n=len(d), p4a_vs_RULESv2=int(d.p4a_v2.sum()), p4a_vs_RULESv1=int(d.p4a_v1.sum()),
        p4b=int(d.p4b.sum()))
        for s, d in (("all rows", G), ("publishable rows", pub),
                     ("IS-admissible rows", G[G.ADM_IS]),
                     ("full-screen admissible", G[G.ADMISSIBLE]))])
    print(fmt(kp))
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)
    print("\n    first-failing 4b bar, count over all rows:")
    print(G.f4b.value_counts().to_string())
    wf4 = WF.dropna(subset=["OOS_Sharpe"])
    print(f"\n    walk-forward picks: 4a {int(wf4.p4a.sum())}/{len(wf4)}, "
          f"4b {int(wf4.p4b.sum())}/{len(wf4)}")
    print(f"    P4 (no new KEEP): "
          f"{'CONFIRMED' if int(G.p4b.sum()) == 0 and int(wf4.p4b.sum()) == 0 else 'REFUTED'}")

    print("\n" + "=" * 200)
    print("VERDICT INPUTS")
    print(f"  premise: OOS denominator positive in {int(G.OOS_sign_pos.sum())}/{len(G)} rows "
          f"(idea 122: 138/138 on u56/broad)")
    print(f"  H_DISCRIM at headline: gap {hd.gap:+.4f}, perm p {hd.perm_p:.4f} -> "
          f"{'PASS' if passed else 'FAIL'}; positive+significant at {npos}/12 grid points")
    print(f"  controls: screen gap {scr_gap:+.4f} vs naive-sign N1 {n1_gap:+.4f} vs "
          f"top-{k} magnitude {float(CTRL.gap.iloc[2]):+.4f}; AUC(dMaxDD_IS) {a_mag:.4f}, "
          f"AUC(kind) {kind_auc:.4f}; incremental gap {float(CTRL.gap.iloc[3]):+.4f} "
          f"(p {float(CTRL.perm_p.iloc[3]):.4f})")
    print(f"  selection: {int(hcell.picks_changed)}/{int(hcell.n_cells)} picks changed, "
          f"S2 mean OOS Sharpe {hcell.S2_mean_OOS_Sharpe:.4f} vs S1 "
          f"{float(CH.S1_mean_OOS_Sharpe.iloc[0]):.4f}")
    print(f"  KEEP: 4a {int(G.p4a_v2.sum())}/{len(G)} vs RULES v2, 4b {int(G.p4b.sum())}/{len(G)}")
    print("=" * 200)


if __name__ == "__main__":
    main()
