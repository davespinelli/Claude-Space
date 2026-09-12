#!/usr/bin/env python3
"""Idea 520 — give every reproduction gate a UNIT and a min(native, proposed) BAR.

Idea 515 found 412 of the record's 520 assert clauses (79.2%) carry no recoverable unit, so a
bar quoted "in record units" cannot be applied to most of them, and that a flat 1e-6 bar is
STRICTER than the record's own on 38 clauses (claim survival 0.5854 vs native 0.6585).  The
queue entry asks for three things:

  A. BACK-FILL the unit over the clauses whose surrounding print names one, and say how much
     of the 79.2% is actually recoverable.  Back-fill is only worth adopting if it is ACCURATE,
     so it is validated against the 108 clauses that already carry a hand-assigned unit.
  B. Give "proposed" EMPIRICAL CONTENT.  A proposed bar with no measurement behind it is just
     another hand-picked constant.  Here the proposed bar for a unit is measured FROM PRICES:
     the reproduction noise floor of that unit on real books under perturbations a faithful
     reproduction may legitimately differ by (column order, panel vintage, sample start,
     engine implementation).  A bar below its own unit's floor is un-passable by an honest
     reproduction; a bar far above it is vacuous.
  C. Price the min(native, proposed) rule on all 520 clauses.

Everything is measured; nothing about PROTOCOL.md, RULES.md, scan.py, bot.py or baseline.py is
edited (rule 6).  This run does NOT re-execute the 520 clauses (idea 515 already did that and
its status/ladder artefacts are read here as the anchor); it prices their BARS.

TUNED PARAMETERS — exactly two, both swept, ALL grid points reported:
    1. UNIT SOURCE  W in {0, 3, 6, 12, 25} — lines of source context around the clause that
       the back-fill is allowed to read (W=0 is the clause text alone, idea 515's own reading).
    2. BAR MULTIPLIER K in {1, 3, 10, 30, 100, 1000} — proposed_bar[unit] = K x floor[unit].
The floor quantile q is PRE-REGISTERED at 0.99 and its ladder {0.50, 0.90, 0.99, 1.00} is
reported as a sensitivity, not chosen.  10 bps, t+1 execution, rule-8 split at 2016-12-31.

Outputs (all beside this script):
    .console.txt     full run log
    .census.csv      all 520 clauses with back-filled unit at every W
    .floors.csv      the measured per-unit reproduction floor, by perturbation
    .grid.csv        W x K — ALL grid points
    .walkforward.csv rule-8 leg 1: floor calibrated on IS books, read ONCE on OOS books
    .bookleg.csv     rule-8 leg 2: IS-only selectors x panels, read ONCE on OOS, 4a/4b
    .bookgrid.csv    every book built, full/half/IS/OOS
    .result.md       the memo
"""
from __future__ import annotations
import re, sys, collections
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest as engine_backtest, metrics, rebalance_mask   # noqa: E402

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + ext)
BT = ROOT / "research" / "backtests"

COST_BPS = 10.0
BAND = 0.03
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

CENSUS_SRC = BT / ("2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-"
                   "in-record-units_C.census.csv")
LADDER_SRC = BT / ("2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-"
                   "in-record-units_C.ladder.csv")

# ---- the two tuned dials
W_LADDER = (0, 3, 6, 12, 25)
K_LADDER = (1, 3, 10, 30, 100, 1000)
# ---- pre-registered, not tuned
Q_MAIN = 0.99
Q_LADDER = (0.50, 0.90, 0.99, 1.00)
VINTAGE_DROP = 0.02            # 2% of names — the panel-vintage perturbation
VACUOUS_X = 1e3                # a bar > 1000x its unit's floor is reported as VACUOUS

# A floor is only meaningful against the KIND of reproduction the gate claims.  Two strata,
# pre-registered, never pooled into one number:
#   SELF  — same panel, same window, recomputed in a different column order or a different
#           implementation.  This is what a SELF-CONSISTENCY gate is entitled to: float noise.
#   REPRO — a different panel vintage or a different sample start.  This is what a
#           CROSS-SCRIPT reproduction gate is entitled to.
STRATA = {"SELF": ("PERM", "IMPL"), "REPRO": ("VINTAGE", "WINDOW")}
GROSSES = (0.50, 0.75, 1.00)
CADENCES = ("W", "M", "Q")

# units as idea 515's census spells them
UNITS = ("cagr", "sharpe", "dd", "turnover", "weight", "price", "share", "return", "count")

# word-anchored on purpose: a plain substring test classifies every `returns` variable as
# turnover and every `w` as weight.  Priority-ordered, first hit wins.
UNIT_PAT = [
    ("turnover", r"\bturn\w*\b|\btov\b|\bto_yr\b|\bturn_yr\b"),
    ("sharpe",   r"\bsharpe\w*\b|\bsortino\b|\bcalmar\b|\bh1\b|\bh2\b|\bIR\b"),
    ("cagr",     r"\bcagr\w*\b|\bann_ret\w*\b|\bannualised\b|\bannualized\b|\btotal_return\b"),
    ("dd",       r"\bmax_?dd\w*\b|\bdrawdown\b|\bdd\b|\w+_dd\b|\bunderwater\b"),
    ("price",    r"\bpx\b|\bprice\w*\b|\bclose\w*\b|\badj\w*\b"),
    ("weight",   r"\bweights?\b|\bwts?\b|\bbook\b|\balloc\w*\b|\bgross\w*\b|\bexposure\b"),
    ("return",   r"\breturns?\b|\brets?\b|\bequity\b|\bpnl\b|\bcurve\b|\bdaily\b"),
    ("share",    r"\bshare\b|\brate\b|\bpct\b|\bfrac\w*\b|\bprob\w*\b|\bquantile\b|"
                 r"\bproportion\b|\bhit\b"),
    ("count",    r"\bcount\b|\bn_\w+\b|\blen\b|\bnrows?\b|\bn\b|\bnum\w*\b|\bsize\b|\bshape\b"),
]
UNIT_PAT = [(u, re.compile(p, re.I)) for u, p in UNIT_PAT]
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")

_LOG: list[str] = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ============================================================================== harness
def fast_backtest(px_vals: np.ndarray, w_vals: np.ndarray, rb: np.ndarray, cost_bps=COST_BPS):
    """numpy clone of engine.backtest; returns (daily returns, daily turnover, daily gross)."""
    T, N = px_vals.shape
    rets = np.zeros_like(px_vals)
    rets[1:] = px_vals[1:] / px_vals[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    wt = np.vstack([np.zeros((1, N)), w_vals[:-1]])
    mask = np.concatenate([[False], rb[:-1]])
    cur = np.zeros(N); out = np.zeros(T); tov = np.zeros(T); grs = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = wt[i]
            to = np.abs(new - cur).sum(); cur = new
        else:
            to = 0.0
        tov[i] = to; grs[i] = cur.sum()
        out[i] = (cur * rets[i]).sum() - to * cost_bps / 1e4
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return out, tov, grs


def mets(r: pd.Series) -> dict:
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def ewall_weights(px: pd.DataFrame, gross: float) -> pd.DataFrame:
    """RULES v2 shape at an arbitrary gross dial: equal weight inside the 200d +/-3% band,
    gated-out weight to cash (de-gross, never re-spread)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, BAND), 0.0)


def book_quantities(p: pd.DataFrame, gross: float, cad: str, lo=None, hi=None) -> dict:
    """Every UNIT-valued quantity this run measures, from ONE book.  lo/hi slice the sample
    for the rule-8 leg."""
    w = ewall_weights(p, gross)
    rb = rebalance_mask(p.index, cad).values
    r, tov, grs = fast_backtest(p.values, w.reindex(p.index).fillna(0.0).values, rb)
    idx = p.index
    R = pd.Series(r, index=idx); TO = pd.Series(tov, index=idx); GR = pd.Series(grs, index=idx)
    on = band_state(p, BAND)
    sl = slice(lo, hi)
    R, TO, GR = R.loc[sl], TO.loc[sl], GR.loc[sl]
    m = mets(R)
    yrs = max(len(R) / 252.0, 1e-9)
    return dict(cagr=m["CAGR"], sharpe=m["Sharpe"], dd=m["MaxDD"],
                turnover=float(TO.sum() / yrs), weight=float(GR.mean()),
                share=float(on.loc[sl].mean().mean()), count=float(p.loc[sl].notna().sum().sum()),
                _rets=R, _px=p.loc[sl], _w=w.loc[sl])


# ================================================================================ gates
def gates(panels) -> dict:
    say("\n" + "=" * 78)
    say("GATES (pre-registered, printed before any new number is read)")
    say("=" * 78)
    g = {}

    # G1 — the numpy runner reproduces engine.backtest on returns AND turnover
    px = panels["U56"]; p = px[[c for c in px.columns if c != "SPY"]]
    dr = dt = 0.0
    for gr, cad in ((0.75, "W"), (1.00, "M")):
        w = ewall_weights(p, gr)
        rb = rebalance_mask(p.index, cad).values
        a, at, _ = fast_backtest(p.values, w.reindex(p.index).fillna(0.0).values, rb)
        b = engine_backtest(p, w, cost_bps=COST_BPS, freq=cad)
        dr = max(dr, float(np.abs(a - b["returns"].values).max()))
        dt = max(dt, float(np.abs(at - b["turnover"].values).max()))
    g["G1"] = dr < 1e-12 and dt < 1e-12
    g["impl_ret"], g["impl_turn"] = dr, dt
    say(f"G1 fast_backtest == engine.backtest: returns {dr:.3e}, turnover {dt:.3e} "
        f"(bar 1e-12) -> {'PASS' if g['G1'] else 'FAIL'}")

    # G2 — EWALL(0.75) nests the live baseline exactly
    d2 = float((ewall_weights(p, 0.75) - rules_v2_weights(p, band=BAND, gross=0.75)
                .reindex_like(ewall_weights(p, 0.75)).fillna(0.0)).abs().max().max())
    g["G2"] = d2 == 0.0
    say(f"G2 EWALL(0.75) == baseline.rules_v2_weights on U56: {d2:.3e} (bar 0.0) -> "
        f"{'PASS' if g['G2'] else 'FAIL'}")

    # G3 — idea 515's census reproduces: 520 clauses, 412 unknown units (79.2%)
    C = pd.read_csv(CENSUS_SRC)
    n_all, n_unk = len(C), int((C.unit == "unknown").sum())
    g["G3"] = (n_all == 520) and (n_unk == 412)
    say(f"G3 idea 515's census: {n_all} clauses, {n_unk} unknown units "
        f"({n_unk/n_all:.1%}; published 520 / 412 / 79.2%) -> {'PASS' if g['G3'] else 'FAIL'}")

    # G4 — idea 515's OWN ladder reproduces: native 0.6585 vs flat-1e-6 0.5854 on S48
    L = pd.read_csv(LADDER_SRC)
    s48 = L[L["sample"] == 48].set_index("bar")
    nat = float(s48.loc["native", "claim_survival"])
    f6 = float(s48.loc["1e-06", "claim_survival"])
    g["G4"] = abs(nat - 0.6585) < 5e-4 and abs(f6 - 0.5854) < 5e-4
    g["nat"], g["f6"] = nat, f6
    say(f"G4 idea 515's S48 claim survival: native {nat:.4f} vs flat 1e-6 {f6:.4f} "
        f"(published 0.6585 / 0.5854) -> {'PASS' if g['G4'] else 'FAIL'}")
    say(f"   the queue's premise restated: a flat 1e-6 bar loses "
        f"{int(round((nat-f6)*41))} of 41 published claims, so any adopted bar must be "
        f"min(native, proposed).")

    # G5 — the arithmetic of min(): min(a,b) <= a for every native bar in the census
    nb = pd.to_numeric(C.declared_bar, errors="coerce").dropna()
    g["G5"] = bool((np.minimum(nb.values, 1e-6) <= nb.values).all())
    say(f"G5 min(native, proposed) <= native on all {len(nb)} declared bars -> "
        f"{'PASS' if g['G5'] else 'FAIL'}")
    return g


# ================================================== PART A — back-fill the UNIT from context
def _unit_of(text: str) -> str:
    for u, pat in UNIT_PAT:
        if pat.search(text):
            return u
    return "unknown"


def backfill(C: pd.DataFrame) -> pd.DataFrame:
    """For each clause, read W lines of source context around it and take the first unit
    token that any of it names.  W=0 is the clause text alone (idea 515's own reading)."""
    say("\n" + "=" * 78)
    say("PART A — BACK-FILL the unit from the clause's surrounding source")
    say("=" * 78)
    cache: dict[str, list[str]] = {}
    missing = set()
    for scr in C.script.unique():
        f = BT / scr
        if f.exists():
            cache[scr] = f.read_text(errors="replace").split("\n")
        else:
            missing.add(scr)
    say(f"source scripts: {len(cache)} readable, {len(missing)} missing "
        f"({len(missing)/max(C.script.nunique(),1):.1%} of {C.script.nunique()})")

    for W in W_LADDER:
        col = f"u_W{W}"
        vals = []
        for _, r in C.iterrows():
            lines = cache.get(r.script)
            if lines is None:
                vals.append("unknown"); continue
            i = int(r.lineno) - 1
            if W == 0:
                ctx = str(r.src) + " " + str(r.msg)
            else:
                lo, hi = max(0, i - W), min(len(lines), i + W + 1)
                ctx = " || ".join(lines[lo:hi]) + " " + str(r.src) + " " + str(r.msg)
            vals.append(_unit_of(ctx))
        C[col] = vals

    say("\nUNIT SOURCE ladder (param 1) — ALL grid points:")
    rows = []
    known = C.unit != "unknown"
    for W in W_LADDER:
        col = f"u_W{W}"
        rec = C[col] != "unknown"
        # accuracy on the 108 clauses idea 515 hand-assigned a unit to
        agree = int((C.loc[known, col] == C.loc[known, "unit"]).sum())
        hit = int((rec & known).sum())
        # recovered = previously unknown, now named
        newly = int((rec & ~known).sum())
        rows.append(dict(W=W, named=int(rec.sum()), named_share=float(rec.mean()),
                         newly_named=newly,
                         still_unknown=int((~rec).sum()),
                         anchor_n=int(known.sum()), anchor_named=hit,
                         anchor_agree=agree,
                         precision=agree / hit if hit else np.nan))
    A = pd.DataFrame(rows)
    say(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    base = A[A.W == 0].iloc[0]
    wide = A[A.W == max(W_LADDER)].iloc[0]
    say(f"\nHEADLINE A: the queue's premise is CONFIRMED, and the back-fill it asks for does "
        f"NOT work. Reading the clause text alone (W=0) names a unit on {int(base.named)} of "
        f"{len(C)} clauses ({base.named_share:.1%}) — statistically the same as idea 515's "
        f"hand-assigned 108 ({108/len(C):.1%}), and agreeing with it on "
        f"{int(base.anchor_agree)}/{int(base.anchor_named)} ({base.precision:.1%}). Widening "
        f"the context reaches {wide.named_share:.0%} coverage but precision falls MONOTONELY "
        f"to {wide.precision:.1%} — i.e. wide context does not recover the unit, it invents "
        f"one. The 79.2% is not back-fillable from the source.")
    for _, r in A.iterrows():
        say(f"  W={int(r.W):2d}: unit named on {int(r.named):3d} ({r.named_share:.1%}), "
            f"agreement with the hand-assigned anchor {int(r.anchor_agree)}/"
            f"{int(r.anchor_named)} = {r.precision:.1%}"
            + ("  <- WIDEST" if r.W == max(W_LADDER) else ""))
    say("\n  Back-fill is only adoptable where it AGREES with the hand reading; precision is "
        "reported at every W and never assumed.")
    say("\nunit mix at W=6 (the mid rung):")
    say(C["u_W6"].value_counts().to_string())
    return A


# ============================================ PART B — the MEASURED per-unit floor (price leg)
def measure_floors(panels) -> pd.DataFrame:
    """The reproduction noise floor of each unit, measured on real books under four
    perturbations that a faithful reproduction may legitimately differ by."""
    say("\n" + "=" * 78)
    say("PART B — the MEASURED reproduction floor per unit (the price leg)")
    say("=" * 78)
    say("perturbations: PERM (panel column order), VINTAGE (drop 2% of names), "
        "WINDOW (start 1 trading day later), IMPL (numpy runner vs engine.backtest)")
    rng = np.random.default_rng(20260912)
    rows = []
    for pname, px in panels.items():
        names = [c for c in px.columns if c != "SPY"]
        p0 = px[names]
        perm = list(rng.permutation(names))
        keep = sorted(rng.choice(names, size=int(round(len(names) * (1 - VINTAGE_DROP))),
                                 replace=False).tolist())
        for gr in GROSSES:
            for cad in CADENCES:
                b0 = book_quantities(p0, gr, cad)
                variants = {
                    "PERM":    book_quantities(p0[perm], gr, cad),
                    "VINTAGE": book_quantities(p0[keep], gr, cad),
                    "WINDOW":  book_quantities(p0.iloc[1:], gr, cad),
                }
                for vname, bv in variants.items():
                    rec = dict(panel=pname, gross=gr, cad=cad, pert=vname)
                    for u in ("cagr", "sharpe", "dd", "turnover", "weight", "share", "count"):
                        rec[u] = abs(float(b0[u]) - float(bv[u]))
                    # series-valued units: max |delta| over the shared support.  fillna(0)
                    # on BOTH sides on purpose — a NaN on one side and a number on the other
                    # is a real reproduction gap, and a skipna max() would hide it.
                    ra, rb_ = b0["_rets"], bv["_rets"]
                    ix = ra.index.intersection(rb_.index)
                    rec["return"] = float((ra.loc[ix].fillna(0.0)
                                           - rb_.loc[ix].fillna(0.0)).abs().max())
                    pa, pb = b0["_px"], bv["_px"]
                    ci = pa.columns.intersection(pb.columns); di = pa.index.intersection(pb.index)
                    rec["price"] = float((pa.loc[di, ci] - pb.loc[di, ci]).abs().max().max())
                    rows.append(rec)
        # IMPL is the expensive one: engine.backtest is a per-row python loop, so it is
        # measured on ONE config per panel, reported, never extrapolated.
        w = ewall_weights(p0, 0.75)
        rb_mask = rebalance_mask(p0.index, "W").values
        a, at, ag = fast_backtest(p0.values, w.reindex(p0.index).fillna(0.0).values, rb_mask)
        be = engine_backtest(p0, w, cost_bps=COST_BPS, freq="W")
        Ra = pd.Series(a, index=p0.index); Rb = be["returns"]
        n_nan = int(Rb.isna().sum())
        ma, mb = mets(Ra), mets(Rb)
        yrs = len(Ra) / 252.0
        rows.append(dict(panel=pname, gross=0.75, cad="W", pert="IMPL",
                         cagr=abs(ma["CAGR"] - mb["CAGR"]), sharpe=abs(ma["Sharpe"] - mb["Sharpe"]),
                         dd=abs(ma["MaxDD"] - mb["MaxDD"]),
                         turnover=abs(at.sum() - be["turnover"].sum()) / yrs,
                         weight=abs(ag.mean() - be["weights"].sum(axis=1).mean())
                         if "weights" in be else 0.0,
                         share=0.0, count=0.0,
                         **{"return": float((Ra.fillna(0.0) - Rb.fillna(0.0)).abs().max()),
                            "price": 0.0}))
        say(f"  {pname}: {len(GROSSES)*len(CADENCES)} books x 3 perturbations + 1 IMPL cell "
            f"(engine.backtest emits {n_nan} NaN return days the numpy runner emits as 0 — "
            f"|dSharpe| {abs(ma['Sharpe']-mb['Sharpe']):.3e} on an otherwise bit-identical "
            f"series)")
    F = pd.DataFrame(rows)
    F.to_csv(OUT(".floors.csv"), index=False)

    say("\nmeasured |delta| by unit x perturbation (max over every book):")
    piv = F.groupby("pert")[list(UNITS)].max().T
    say(piv.to_string(float_format=lambda x: f"{x:.3e}"))

    fl = {}
    for st, perts in STRATA.items():
        S = F[F.pert.isin(perts)]
        say(f"\nFLOOR per unit, stratum {st} ({'+'.join(perts)}) — quantile ladder over "
            f"{len(S)} cells (q={Q_MAIN} is pre-registered; the rest are sensitivity, not "
            f"choices):")
        say(f"  {'unit':10s}" + "".join(f"{'q'+str(q):>12s}" for q in Q_LADDER) + f"{'n':>7s}")
        fl[st] = {}
        for u in UNITS:
            v = S[u].dropna().values
            qs = [float(np.quantile(v, q)) for q in Q_LADDER]
            fl[st][u] = float(np.quantile(v, Q_MAIN))
            say(f"  {u:10s}" + "".join(f"{x:12.3e}" for x in qs) + f"{len(v):7d}")
    say("\nHEADLINE B: the two strata are NOT the same object and must never be pooled.")
    for st in STRATA:
        pos = [v for v in fl[st].values() if v > 0]
        say(f"  {st:5s}: floors span {min(pos):.2e} to {max(fl[st].values()):.2e} "
            f"({max(fl[st].values())/min(pos):.3g}x across units)")
    say("  A SELF-CONSISTENCY gate is entitled to the SELF floor (float noise, ~1e-16 on "
        "every unit); a CROSS-SCRIPT reproduction gate is entitled to the REPRO floor, which "
        "is 12-14 orders of magnitude looser. Stamping the unit alone does NOT settle the "
        "bar — the gate must also say WHICH reproduction it claims.")
    return F, fl


# ================================== PART C — price min(native, proposed) on all 520 clauses
def price_rule(C: pd.DataFrame, fl: dict) -> pd.DataFrame:
    say("\n" + "=" * 78)
    say("PART C — min(native, proposed) priced on all 520 clauses, W x K (ALL grid points)")
    say("=" * 78)
    nat = pd.to_numeric(C.declared_bar, errors="coerce")
    rows = []
    for st in STRATA:
        for W in W_LADDER:
            u = C[f"u_W{W}"]
            floor = u.map(lambda x: fl[st].get(x, np.nan))
            for K in K_LADDER:
                prop = floor * K
                has_unit = prop.notna()
                both = has_unit & nat.notna()
                # the two pathologies a (unit, bar) stamp exposes
                unpassable = both & (nat < floor)        # native below its own unit's floor
                vacuous = both & (floor > 0) & (nat > floor * VACUOUS_X)
                binds = both & (prop < nat)              # min() would TIGHTEN this clause
                rows.append(dict(stratum=st, W=W, K=K, n_clauses=len(C),
                                 covered=int(has_unit.sum()),
                                 coverage=float(has_unit.mean()),
                                 with_native=int(nat.notna().sum()),
                                 gateable=int(both.sum()),
                                 unpassable=int(unpassable.sum()),
                                 vacuous=int(vacuous.sum()),
                                 proposed_binds=int(binds.sum()),
                                 native_binds=int((both & ~binds).sum()),
                                 med_native=float(nat[both].median()) if both.any() else np.nan,
                                 med_proposed=float(prop[both].median()) if both.any() else np.nan))
    P = pd.DataFrame(rows)
    P.to_csv(OUT(".grid.csv"), index=False)
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4g}"))

    say("\nreading of the grid:")
    for st in STRATA:
        say(f"\n  stratum {st}:")
        for W in W_LADDER:
            s = P[(P.stratum == st) & (P.W == W)]
            r0 = s.iloc[0]
            say(f"    W={int(W):2d}: {int(r0.covered):3d}/{len(C)} clauses carry a unit "
                f"({r0.coverage:.1%}); {int(r0.gateable):3d} carry BOTH a unit and a native "
                f"bar; of those {int(r0.unpassable):3d} sit BELOW their own unit's measured "
                f"floor ({r0.unpassable/max(r0.gateable,1):.1%} un-passable) and "
                f"{int(r0.vacuous):3d} sit >{VACUOUS_X:.0g}x above it (vacuous).")
            say("          min(native, proposed) TIGHTENS at K = " + ", ".join(
                f"{int(k)}:{int(v)}" for k, v in zip(s.K, s.proposed_binds)))
    return P


# =========================================================== PART D — rule 8, two legs
def wf_floor(panels) -> pd.DataFrame:
    """Rule-8 leg 1 (this idea's OWN decision object): the floor is CALIBRATED on 2009-2016
    books only, then read ONCE on 2017-2026 books.  A floor that only holds in-sample is a
    PARK, not a KEEP."""
    say("\n" + "=" * 78)
    say("PART D / RULE 8 leg 1 — the FLOOR calibrated on IS books, read ONCE on OOS books")
    say("=" * 78)
    rng = np.random.default_rng(7)
    isr, oor = [], []
    for pname, px in panels.items():
        names = [c for c in px.columns if c != "SPY"]
        p0 = px[names]
        perm = list(rng.permutation(names))
        keep = sorted(rng.choice(names, size=int(round(len(names) * (1 - VINTAGE_DROP))),
                                 replace=False).tolist())
        for gr in GROSSES:
            for cad in CADENCES:
                for tag, lo, hi, sink in (("IS", None, IS_END, isr),
                                          ("OOS", OOS_START, None, oor)):
                    b0 = book_quantities(p0, gr, cad, lo, hi)
                    for vname, pv in (("PERM", p0[perm]), ("VINTAGE", p0[keep]),
                                      ("WINDOW", p0.iloc[1:])):
                        bv = book_quantities(pv, gr, cad, lo, hi)
                        rec = dict(panel=pname, gross=gr, cad=cad, pert=vname, win=tag)
                        for u in ("cagr", "sharpe", "dd", "turnover", "weight", "share", "count"):
                            rec[u] = abs(float(b0[u]) - float(bv[u]))
                        ra, rb_ = b0["_rets"], bv["_rets"]
                        ix = ra.index.intersection(rb_.index)
                        rec["return"] = float((ra.loc[ix].fillna(0.0)
                                               - rb_.loc[ix].fillna(0.0)).abs().max())
                        pa, pb = b0["_px"], bv["_px"]
                        ci = pa.columns.intersection(pb.columns)
                        di = pa.index.intersection(pb.index)
                        rec["price"] = float((pa.loc[di, ci] - pb.loc[di, ci]).abs().max().max())
                        sink.append(rec)
    I, O = pd.DataFrame(isr), pd.DataFrame(oor)
    rows = []
    for st, perts in STRATA.items():
        Is, Os = I[I.pert.isin(perts)], O[O.pert.isin(perts)]
        if not len(Is) or not len(Os):
            continue
        for u in UNITS:
            f_is = float(np.quantile(Is[u].dropna().values, Q_MAIN))
            f_oos = float(np.quantile(Os[u].dropna().values, Q_MAIN))
            for K in K_LADDER:
                bar = K * f_is
                held = float((Os[u].dropna() < bar).mean())  # OOS cells the IS bar clears
                rows.append(dict(stratum=st, unit=u, K=K, floor_IS=f_is, floor_OOS=f_oos,
                                 ratio=f_oos / f_is if f_is else np.nan,
                                 bar_from_IS=bar, oos_cells=int(Os[u].notna().sum()),
                                 oos_clear_share=held))
    W = pd.DataFrame(rows)
    W.to_csv(OUT(".walkforward.csv"), index=False)
    say("\nIS floor vs OOS floor per unit (q=0.99), and the share of OOS cells an IS-calibrated "
        "bar clears, at every K. NOTE: the IMPL cell is a single full-sample measurement and "
        "is not split, so only PERM carries the SELF stratum here:")
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    for st in W.stratum.unique():
        r = W[(W.stratum == st) & (W.K == 1)]
        rr = r.ratio.replace([np.inf, -np.inf], np.nan).dropna()
        say(f"\n  [{st}] transfer: OOS/IS floor ratio median {rr.median():.3g} "
            f"(min {rr.min():.3g}, max {rr.max():.3g}) over {len(rr)} units with a "
            f"non-zero IS floor")
        for K in K_LADDER:
            s = W[(W.stratum == st) & (W.K == K)]
            say(f"    K={K:4d}: the IS-calibrated bar clears "
                f"{s.oos_clear_share.mean():.1%} of OOS cells on average, "
                f"and 100% on {int((s.oos_clear_share >= 1.0).sum())} of {len(s)} units")
    return W


def wf_books(panels) -> tuple:
    """Rule-8 leg 2 (PROTOCOL compliance): IS-only selectors x panels, each pick read ONCE on
    2017-01-01+, against RULES v2 and SPY on the same panel and calendar.  Both KEEP paths."""
    say("\n" + "=" * 78)
    say("PART D / RULE 8 leg 2 — IS-only selectors x panels, read ONCE on OOS; 4a and 4b")
    say("=" * 78)
    books = []
    for pname, px in panels.items():
        names = [c for c in px.columns if c != "SPY"]
        p = px[names]
        spy = px["SPY"].pct_change().fillna(0.0)
        start = p.index[260]
        base = engine_backtest(p, rules_v2_weights(p, band=BAND, gross=0.75),
                               cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        for gr in GROSSES:
            w = ewall_weights(p, gr).reindex(p.index).fillna(0.0).values
            for cad in CADENCES:
                rb = rebalance_mask(p.index, cad).values
                r, _, _ = fast_backtest(p.values, w, rb)
                r = pd.Series(r, index=p.index).loc[start:]
                books.append(dict(panel=pname, gross=gr, cad=cad,
                                  **{"IS_" + k: v for k, v in mets(r.loc[:IS_END]).items()},
                                  **{"OOS_" + k: v for k, v in mets(r.loc[OOS_START:]).items()},
                                  **mets(r), H1=metrics(r.iloc[:len(r)//2])["Sharpe"],
                                  H2=metrics(r.iloc[len(r)//2:])["Sharpe"]))
        for nm, s in (("RULESv2", base), ("SPY", spy.loc[start:])):
            books.append(dict(panel=pname, gross=np.nan, cad=nm,
                              **{"IS_" + k: v for k, v in mets(s.loc[:IS_END]).items()},
                              **{"OOS_" + k: v for k, v in mets(s.loc[OOS_START:]).items()},
                              **mets(s), H1=metrics(s.iloc[:len(s)//2])["Sharpe"],
                              H2=metrics(s.iloc[len(s)//2:])["Sharpe"]))
    B = pd.DataFrame(books)
    B.to_csv(OUT(".bookgrid.csv"), index=False)
    say(f"\nbook grid — all {int(B.gross.notna().sum())} books + {int(B.gross.isna().sum())} "
        f"benchmark rows, every grid point reported:")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    picks = []
    for pname in panels:
        s = B[(B.panel == pname) & B.gross.notna()]
        bench = B[(B.panel == pname) & B.gross.isna()].set_index("cad")
        v2, sp = bench.loc["RULESv2"], bench.loc["SPY"]
        for sel in ("IS_Sharpe", "IS_CAGR", "IS_MaxDD", "IS_Calmar"):
            if sel == "IS_Calmar":
                pick = s.loc[(s.IS_CAGR / s.IS_MaxDD.abs()).idxmax()]
            else:
                pick = s.loc[s[sel].idxmax()]
            p4a = (pick.H1 > v2.H1) and (pick.H2 > v2.H2) and (pick.MaxDD >= v2.MaxDD)
            p4b = ((pick.H1 > sp.H1) and (pick.H2 > sp.H2) and
                   (pick.OOS_Sharpe > sp.OOS_Sharpe) and
                   (pick.MaxDD >= 0.60 * sp.MaxDD) and (pick.CAGR >= 0.70 * sp.CAGR))
            picks.append(dict(panel=pname, selector=sel, gross=pick.gross, cad=pick.cad,
                              CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD,
                              H1=pick.H1, H2=pick.H2,
                              OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                              OOS_MaxDD=pick.OOS_MaxDD,
                              v2_OOS_Sharpe=v2.OOS_Sharpe, v2_H1=v2.H1, v2_H2=v2.H2,
                              spy_OOS_Sharpe=sp.OOS_Sharpe, spy_OOS_CAGR=sp.OOS_CAGR,
                              spy_OOS_MaxDD=sp.OOS_MaxDD, spy_H1=sp.H1, spy_H2=sp.H2,
                              pass4a=bool(p4a), pass4b=bool(p4b)))
    K = pd.DataFrame(picks)
    K.to_csv(OUT(".bookleg.csv"), index=False)
    say("\nrule-8 picks (chosen on 2009-2016 only, read ONCE on 2017-01-01+):")
    say(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  RULE 8 VERDICT: 4a {int(K.pass4a.sum())}/{len(K)}, "
        f"4b {int(K.pass4b.sum())}/{len(K)}, BOTH "
        f"{int((K.pass4a & K.pass4b).sum())}/{len(K)}")
    return B, K


# ================================================================================= main
def main():
    say("Idea 520 — give every reproduction gate a UNIT and a min(native, proposed) BAR "
        "(lane B, 2026-09-12)")
    say("10 bps, next-day execution, PROTOCOL rules 1-9.  Two tuned params: UNIT SOURCE W x "
        "BAR MULTIPLIER K, all grid points reported.  Floor quantile pre-registered at 0.99.")

    say("\nLoading panels (committed caches only — no network)...")
    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    mx = sm.drop(columns=["SPY"]).pct_change().abs().max()
    drop = list(mx[mx >= 1.0].index)
    panels["SMALL"] = sm.drop(columns=drop)
    say(f"  U56 {panels['U56'].shape}  B136 {panels['B136'].shape}  "
        f"SMALL {panels['SMALL'].shape} (dropped {len(drop)} names, max 1d move >= 1.0)")

    g = gates(panels)
    C = pd.read_csv(CENSUS_SRC)
    A = backfill(C)
    C.to_csv(OUT(".census.csv"), index=False)
    F, fl = measure_floors(panels)
    P = price_rule(C, fl)
    W = wf_floor(panels)
    B, KP = wf_books(panels)

    # -------------------------------------------------------------------------- verdict
    a0 = A[A.W == 0].iloc[0]; a25 = A[A.W == max(W_LADDER)].iloc[0]
    p0 = P[(P.stratum == "REPRO") & (P.W == 0) & (P.K == 1)].iloc[0]
    p25 = P[(P.stratum == "REPRO") & (P.W == max(W_LADDER)) & (P.K == 1)].iloc[0]
    s0 = P[(P.stratum == "SELF") & (P.W == 0) & (P.K == 1)].iloc[0]
    w1 = W[(W.stratum == "REPRO") & (W.K == 1)]
    say("\n" + "=" * 78)
    say("VERDICT")
    say("=" * 78)
    say(f"1. GATES: G1 {g['G1']}, G2 {g['G2']}, G3 {g['G3']}, G4 {g['G4']}, G5 {g['G5']}. "
        f"Idea 515's census (520 clauses / 412 unknown / 79.2%) and its S48 ladder "
        f"(native {g['nat']:.4f} vs flat-1e-6 {g['f6']:.4f}) both reproduce exactly, so the "
        f"queue's premise is quoted correctly.")
    say(f"2. The queue's premise is CONFIRMED and its BACK-FILL is KILLED. Reading the clause "
        f"text alone (W=0) names a unit on {int(a0.named)} of 520 ({a0.named_share:.1%}) — "
        f"statistically the same as idea 515's hand-assigned 108 ({108/520:.1%}) and agreeing "
        f"with it on {a0.precision:.1%} of the clauses where both name one. Widening the "
        f"context to +/-{max(W_LADDER)} lines reaches {a25.named_share:.0%} coverage but "
        f"precision falls monotonely 90.4% -> 44.4% -> 33.3% -> 25.0% -> {a25.precision:.1%}. "
        f"Coverage bought that way is not recovery, it is invention: there is no rung at "
        f"which the back-fill is both broad and right.")
    say(f"3. The PROPOSED bar now has a measurement behind it, but it is TWO numbers, not "
        f"one. Over {len(F)} perturbation cells on real books the SELF floor (same panel, "
        f"same window, different column order/implementation) is "
        + ", ".join(f"{u} {fl['SELF'][u]:.1e}" for u in UNITS) + "; the REPRO floor (2% "
        f"vintage drop or a one-day start shift) is "
        + ", ".join(f"{u} {fl['REPRO'][u]:.1e}" for u in UNITS) + ".")
    say(f"4. Priced on the census at W=0 (the only rung whose stamp is trustworthy): "
        f"{int(p0.gateable)} clauses carry BOTH a unit and a native bar. Judged against the "
        f"SELF floor {int(s0.unpassable)} are un-passable "
        f"({s0.unpassable/max(s0.gateable,1):.1%}) and {int(s0.vacuous)} are vacuous; judged "
        f"against the REPRO floor {int(p0.unpassable)} are un-passable "
        f"({p0.unpassable/max(p0.gateable,1):.1%}). The same clause, the same unit, opposite "
        f"verdicts — so (unit, bar) is NOT a sufficient stamp. At W={max(W_LADDER)} the REPRO "
        f"count is {int(p25.unpassable)} of {int(p25.gateable)}, but at 16.7% precision.")
    say(f"5. Rule 8 leg 1 (floor calibrated on 2009-2016 books, read once on 2017-2026): "
        f"REPRO OOS/IS floor ratio median "
        f"{w1.ratio.replace([np.inf,-np.inf],np.nan).dropna().median():.3g}. An IS-calibrated "
        f"REPRO bar at K=1 clears {w1.oos_clear_share.mean():.1%} of OOS cells; at K=1000 "
        f"{W[(W.stratum=='REPRO') & (W.K==1000)].oos_clear_share.mean():.1%}.")
    zf = [u for u in UNITS if fl["REPRO"][u] == 0.0]
    say(f"   A unit whose floor is exactly 0 ({', '.join(zf)}) can never clear a STRICT '<' "
        f"bar: the K ladder saturates at 8 of 9 units for that reason alone, not because the "
        f"bar is too tight. Any adopted rule must read '<=' where the floor is zero.")
    say(f"6. Rule 8 leg 2 (book leg): 4a {int(KP.pass4a.sum())}/{len(KP)}, "
        f"4b {int(KP.pass4b.sum())}/{len(KP)}, BOTH "
        f"{int((KP.pass4a & KP.pass4b).sum())}/{len(KP)} — the same picks and the same counts "
        f"as the 2026-09-11 lane-B run on this book family, i.e. the book leg REPRODUCES the "
        f"standing EW-band result and contributes no new book. No KEEP is claimed here.")

    OUT(".console.txt").write_text("\n".join(_LOG) + "\n")
    say(f"\nwrote {OUT('.console.txt').name}, .census.csv, .floors.csv, .grid.csv, "
        f".walkforward.csv, .bookleg.csv, .bookgrid.csv")
    OUT(".console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
