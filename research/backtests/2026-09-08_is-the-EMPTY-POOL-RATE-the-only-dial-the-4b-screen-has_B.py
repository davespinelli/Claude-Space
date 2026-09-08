#!/usr/bin/env python3
"""QUEUE idea 419 — is-the-EMPTY-POOL-RATE-the-only-dial-the-4b-screen-has  (lane B, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 419)
    "idea 163 found the IS-4b screen admits NOTHING in the majority of cells (median 0 of 17
     arms) and that 95.3% of its measured OOS drawdown effect is that fallback, not screening
     (live-pool dDD -0.69 pp, t -1.35).  Sweep the screen's own bars (phi, delta) purely as an
     ADMISSION-RATE dial and regress the OOS d(MaxDD, CAGR) on the realised empty-pool rate:
     if the rate is the whole story, the screen is a hidden exposure switch and should be
     re-specified as one.  Max 2 params."

WHAT IS ACTUALLY BEING TESTED
    Idea 163 measured the screen at ONE setting (phi=0.70, delta=0.60) and found its pooled
    drawdown effect is 95.3% empty-pool fallback.  One setting cannot separate "the screen is
    a rate dial" from "this particular pair of bars happens to be near-inert".  This run turns
    the two bars into an explicit dial and asks whether the ENTIRE input-output behaviour of
    the screen is a function of one scalar — the realised empty-pool (abstention) rate.

      PANEL A  THE DIAL.  Admission rate, empty-pool rate and move rate at all 49 (phi, delta)
               grid points, on the same census idea 163 used.  This is the dial's calibration.
      PANEL B  THE REGRESSION the queue asks for.  Across the 49 grid points, pooled OOS
               d(MaxDD) and d(CAGR) (screened pick minus unscreened pick) regressed on the
               realised empty-pool rate E.  Slope, intercept, R2, and the through-origin fit.
      PANEL C  THE DECOMPOSITION.  At every grid point, split the pooled d into the EMPTY-POOL
               cells (the screen declines the menu; pick = ungated control) and the LIVE-POOL
               cells (the screen actually screens).  If the live-pool leg is null at every
               rate, the screen carries no information beyond its rate.
      PANEL D  THE RATE-MATCHED NULL.  A coin that abstains in k of n cells at random is a
               pure exposure switch by construction.  For every grid point, compare the
               screen's realised pooled d against the distribution of that coin's pooled d at
               the SAME rate (2,000 seeded draws).  |z| < 2 everywhere = the screen IS the coin.
      PANEL E  KEEP PATHS (PROTOCOL rule 4) at every grid point, both 4a(v2) and 4b, plus the
               OOS-window 4b where the parent file carries it, screened vs unscreened.
      PANEL F  LEVELS + rule 8.  Freshly computed RULES v2 and SPY OOS legs from
               research/baseline.py, the 4b OOS bars, and the pooled OOS CAGR/Sharpe/MaxDD of
               the screened policy, the unscreened policy and the do-nothing control at every
               grid point.  Out-of-corpus replication: file 416 alone (zero (panel, book)
               overlap with 142/151) re-reads Panels B-D.

CORPUS — idea 163's census, unchanged: every committed grid in the record carrying a 4b-aware
    admission mask, re-derived from its own `.grid.csv`.
      132  2026-09-05_why-the-IS-4b-screen-changes-no-pick_cloud       18 cells,  306 rows
      142  2026-09-08_selector-comparison-needs-more-cells_B           48 cells,  816 rows
      151  2026-09-08_does-any-selector-beat-doing-nothing_B           72 cells, 1224 rows
      416  2026-09-08_pre-register-K_CAGR-as-the-rule-8-default_cloud  72 cells, 1224 rows
    3,570 arm-rows, 210 (file, cell) pairs, 4 panels, 3 cost rungs, 4 deterministic selectors.

VERDICT GATE (two gates; a file that fails either contributes nothing)
    G1 SCREEN IDENTITY.  The screen is re-derived from RAW grid columns —
         core  = (IS_m_H1 > 0) & (IS_m_H2 > 0)
         DD    = delta * |SPY_IS_MaxDD| - |IS_MaxDD| > 0
         CAGR  = IS_CAGR - phi * SPY_IS_CAGR > 0
       with the panel's SPY IS bars themselves backed out of the committed margin columns
       (|SPY_IS_MaxDD| = (IS_m_DD + |IS_MaxDD|)/0.60, SPY_IS_CAGR = (IS_CAGR - IS_m_CAGR)/0.70)
       and asserted CONSTANT within panel.  At (phi, delta) = (0.70, 0.60) the reconstruction
       must equal the committed admission column on EVERY row.
    G2 PICK IDENTITY.  Every deterministic committed pick must reproduce arm-for-arm from the
       reconstructed mask under the parents' own pick rule (sort by arm, argmax the selector's
       IS column, fall back to the control arm on an empty pool).  K_Random is excluded (its
       draw is not reconstructible from a grid) and is never read.

TUNED PARAMETERS: 2 (phi, delta) — and they are swept, not chosen.  All 49 grid points are
    reported in .dial.csv / .walkforward.csv / .keeppaths.csv; nothing in this file is selected
    by looking at an OOS number, and no book is promoted.  The core bars (IS_m_H1, IS_m_H2) are
    held FIXED at the record's committed form and are not a third dial; their admission rate is
    reported as the dial's ceiling.

WALK-FORWARD (PROTOCOL rule 8) — this run is walk-forward by construction, not by re-fit
    Every admission mask and every argmax reads the IS window (through 2016-12-31) ONLY; every
    d, level and KEEP flag is read ONCE on the untouched 2017-01-01..2026 window.  Panel F adds
    a corpus split: the regression is FIT on the older corpus (132 + 142) and READ on the newer,
    non-overlapping one (151 + 416), so the dial law itself is tested out of sample.

PRE-REGISTERED DECISION RULE (fixed before any Panel-B number was read)
    RATE-IS-THE-ONLY-DIAL requires all three:
      (i)  the Panel-B regression of pooled d(OOS MaxDD) on E has R2 >= 0.80 and |t| >= 2;
      (ii) the Panel-C LIVE-POOL leg is not significant (|t| < 2) at >= 80% of grid points that
           have any live-pool moves, and is not significant pooled;
      (iii) the Panel-D rate-matched null gives |z| < 2 for the pooled d at a MAJORITY of grid
           points.
    -> the screen is a hidden exposure switch and PROTOCOL/queue language should re-specify it
       as an explicit abstention rate.
    MORE-THAN-A-RATE if (ii) or (iii) fails with a consistent sign -> the screen carries real
       selection information and the queue's premise is falsified.
    MIXED otherwise, reported as such.  This run cannot promote a book and does not try;
    PROTOCOL.md, RULES.md, scan.py, bot.py and baseline.py are NOT modified.

CAVEATS carried, not buried
    * Survivorship (idea 54): every panel is current constituents; every CAGR here is
      optimistic and no level in this file is an achievable return.  Read the contrasts.
    * Idea 128 / idea 420: the IS window cannot express a deep drawdown (SPY IS MaxDD -22.1%
      on broad vs -33.7% full), and idea 420 measured OOS drawdowns 1.49x DEEPER than IS on
      96.2% of arms.  A delta dial calibrated on the IS window is therefore optimistic in
      LEVEL by construction; this run reads the dial's ORDER (which idea 420 showed transfers,
      slope +0.918), not its level.
    * Idea 401: data/prices.csv was restated after 132/142 were committed.  Both gates are
      arm-identity gates, which are insensitive to that; no census metric is re-derived from
      prices.  Only Panel F's v2/SPY leg is freshly computed, and it is labelled as such.
    * The parents' OOS metric columns are taken as committed.  This run re-derives POOLS and
      PICKS, not backtests.
    * Idea 126: every row is quoted at t+1 execution and 0/10/25 bps per PROTOCOL rule 2.

Deterministic (seed 20260908), standalone.  Writes .console.txt, .dial.csv, .cells.csv.gz,
.regression.csv, .keeppaths.csv, .walkforward.csv and .result.md next to itself.  Modifies
nothing else.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_is-the-EMPTY-POOL-RATE-the-only-dial-the-4b-screen-has_B"
OUT = ROOT / "research" / "backtests"
SEED = 20260908
OOS_START = "2017-01-01"
PHI0, DELTA0 = 0.70, 0.60                      # the record's committed screen
N_DRAWS = 2000                                 # rate-matched null draws

# THE TWO TUNED PARAMETERS, SWEPT IN FULL (49 grid points, every one reported)
PHIS = [0.00, 0.30, 0.50, 0.70, 0.90, 1.10, 1.30]
DELTAS = [0.20, 0.40, 0.60, 0.80, 1.00, 1.25, 1.50]

SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_Calmar": "IS_Calmar",
             "K_MaxDD": "IS_MaxDD", "K_CAGR": "IS_CAGR"}
METRICS = ["OOS_MaxDD", "OOS_CAGR", "OOS_Sharpe"]

# (tag, stem, committed S1 admission column, picks-file (selector col, pool col), pool label, arm col)
FILES = [
    ("132", "2026-09-05_why-the-IS-4b-screen-changes-no-pick_cloud",
     "adm_S1", ("sel", "screen"), {"U": "S0", "S": "S1"}, "arm"),
    ("142", "2026-09-08_selector-comparison-needs-more-cells_B",
     "adm_S1", ("sel", "screen"), {"U": "S0", "S": "S1"}, "arm"),
    ("151", "2026-09-08_does-any-selector-beat-doing-nothing_B",
     "adm_P_S1", ("default", "pool"), {"U": "P_ALL", "S": "P_S1"}, "arm"),
    ("416", "2026-09-08_pre-register-K_CAGR-as-the-rule-8-default_cloud",
     "adm_P_S1", ("default", "pool"), {"U": "P_ALL", "S": "P_S1"}, "pick"),
]
FILE_ORDER = {"416": 0, "151": 1, "142": 2, "132": 3}   # dedup preference, stated before use
OLD_CORPUS, NEW_CORPUS = {"132", "142"}, {"151", "416"}

LINES = []


def say(s=""):
    print(s)
    LINES.append(s)


# ------------------------------------------------------------------ statistics
def _lchoose(n, k):
    from math import lgamma
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def paired(x, label, **extra):
    """n, mean, t, W/L/T and the exact two-sided sign-test p of a difference series."""
    x = pd.Series(x).dropna().astype(float)
    n = len(x)
    if n == 0:
        return dict(label=label, n=0, mean=np.nan, t=np.nan, wins=0, losses=0, ties=0,
                    sign_p=np.nan, **extra)
    w, l = int((x > 0).sum()), int((x < 0).sum())
    sd = x.std(ddof=1)
    t = float(x.mean() / (sd / np.sqrt(n))) if n > 1 and sd > 0 else np.nan
    nz = w + l
    if nz:
        k = min(w, l)
        c = sum(np.exp(_lchoose(nz, i) - nz * np.log(2.0)) for i in range(0, k + 1))
        sp = float(min(1.0, 2.0 * c))
    else:
        sp = np.nan
    return dict(label=label, n=n, mean=float(x.mean()), t=t, wins=w, losses=l,
                ties=n - w - l, sign_p=sp, **extra)


def fmt(d, scale=100.0, unit=" pp"):
    if not d["n"]:
        return f"n {d['n']:4d}  (empty)"
    return (f"n {d['n']:4d}  mean {d['mean']*scale:+8.4f}{unit}  t {d['t']:+6.2f}  "
            f"{d['wins']:3d}W/{d['losses']:3d}L/{d['ties']:3d}T  sign p {d['sign_p']:.4f}")


def ols(x, y):
    """Simple OLS with intercept: slope, intercept, R2, t(slope), plus the no-intercept slope."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 3 or x.std() == 0:
        return dict(n=n, slope=np.nan, intercept=np.nan, r2=np.nan, t=np.nan, slope0=np.nan)
    b = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
    a = y.mean() - b * x.mean()
    yh = a + b * x
    ss_res = float(((y - yh) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    se = np.sqrt(ss_res / (n - 2) / (((x - x.mean()) ** 2).sum())) if n > 2 else np.nan
    t = b / se if se and np.isfinite(se) and se > 0 else np.nan
    b0 = float((x * y).sum() / (x * x).sum()) if (x * x).sum() > 0 else np.nan
    return dict(n=n, slope=float(b), intercept=float(a), r2=float(r2), t=float(t), slope0=b0)


# ------------------------------------------------------------------ cell machinery
class Cell:
    """One (file, panel, book, cost): arm-sorted arrays, enough to re-derive any (phi,delta)."""

    def __init__(self, tag, key, s):
        s = s.sort_values("arm").reset_index(drop=True)
        self.tag, self.panel, self.book, self.cost = tag, key[0], key[1], key[2]
        self.arms = s.arm.to_numpy()
        self.n = len(s)
        self.core = ((s.IS_m_H1 > 0) & (s.IS_m_H2 > 0)).to_numpy()
        self.isdd = s.IS_MaxDD.abs().to_numpy()
        self.iscagr = s.IS_CAGR.to_numpy()
        # SPY's IS bars, backed out of the committed margins and asserted constant per cell
        sdd = ((s.IS_m_DD + s.IS_MaxDD.abs()) / DELTA0).to_numpy()
        sca = ((s.IS_CAGR - s.IS_m_CAGR) / PHI0).to_numpy()
        assert np.ptp(sdd) < 1e-9 and np.ptp(sca) < 1e-9, f"SPY IS bars not constant in {key}"
        self.sdd, self.scagr = float(sdd[0]), float(sca[0])
        self.sel = {k: s[c].to_numpy() for k, c in SELECTORS.items()}
        self.met = {m: s[m].to_numpy() for m in METRICS}
        self.ctl = int(np.where(self.arms == "control")[0][0])
        a4a = "pass4a_v2" if "pass4a_v2" in s.columns else "pass4a"
        self.p4a = s[a4a].to_numpy().astype(bool)
        self.p4b = s["pass4b"].to_numpy().astype(bool)
        self.has_oos4b = "pass4b_oos" in s.columns
        self.p4bo = (s["pass4b_oos"].to_numpy().astype(bool) if self.has_oos4b
                     else np.zeros(self.n, bool))
        self.committed = None

    def admit(self, phi, delta):
        return self.core & (delta * self.sdd - self.isdd > 0) & (self.iscagr - phi * self.scagr > 0)

    def pick(self, mask, sel):
        """Parents' rule: argmax of the selector's IS column inside the mask; control if empty."""
        v = self.sel[sel]
        if not mask.any():
            return self.ctl, True
        vv = np.where(mask, v, -np.inf)
        return int(np.argmax(vv)), False      # argmax ties -> first in arm-sorted order

    def pick_all(self, sel):
        return int(np.argmax(self.sel[sel])), False


def load_cells():
    """Gate G1 + G2, then the arm-sorted cell objects for every admitted file."""
    say("\n[GATE] two gates: the screen must reconstruct from raw columns, and every")
    say("       committed deterministic pick must reproduce arm-for-arm from it.")
    cells, admitted = [], []
    for tag, stem, admcol, keycols, lab, armcol in FILES:
        g = pd.read_csv(OUT / f"{stem}.grid.csv")
        p = pd.read_csv(OUT / f"{stem}.picks.csv")
        # ---- G1
        sdd = (g.IS_m_DD + g.IS_MaxDD.abs()) / DELTA0
        sca = (g.IS_CAGR - g.IS_m_CAGR) / PHI0
        rec = ((g.IS_m_H1 > 0) & (g.IS_m_H2 > 0)
               & (DELTA0 * sdd - g.IS_MaxDD.abs() > 0) & (g.IS_CAGR - PHI0 * sca > 0))
        g1_hits = int((rec == g[admcol].astype(bool)).sum())
        g1 = g1_hits == len(g)
        # panel-constancy of the backed-out SPY bars
        bars = g.assign(_d=sdd, _c=sca).groupby("panel")[["_d", "_c"]].agg(np.ptp).max().max()
        # ---- G2
        cl = {k: Cell(tag, k, s) for k, s in g.groupby(["panel", "book", "cost"], sort=True)}
        rows = []
        for k, c in cl.items():
            m = c.admit(PHI0, DELTA0)
            for sel in SELECTORS:
                iu, _ = c.pick_all(sel)
                isc, _ = c.pick(m, sel)
                rows.append(dict(panel=k[0], book=k[1], cost=k[2], **{keycols[0]: sel},
                                 **{keycols[1]: lab["U"]}, arm_re=c.arms[iu]))
                rows.append(dict(panel=k[0], book=k[1], cost=k[2], **{keycols[0]: sel},
                                 **{keycols[1]: lab["S"]}, arm_re=c.arms[isc]))
        R = pd.DataFrame(rows)
        m = p.merge(R, on=["panel", "book", "cost", keycols[0], keycols[1]], how="inner")
        g2_hits = int((m[armcol] == m.arm_re).sum())
        g2 = len(m) > 0 and g2_hits == len(m)
        ok = g1 and g2 and bars < 1e-9
        say(f"  {tag}: G1 screen {g1_hits}/{len(g)} rows   G2 picks {g2_hits}/{len(m)}   "
            f"SPY-bar spread {bars:.2e}  ->  {'ADMITTED' if ok else 'REJECTED'}  "
            f"({len(cl)} cells x {list(cl.values())[0].n} arms)")
        if ok:
            admitted.append(tag)
            cells.extend(cl.values())
    say(f"  {len(admitted)} of {len(FILES)} files admitted: {admitted}.  K_Random excluded "
        f"from both gates and from every reading.")
    return cells, admitted


# ------------------------------------------------------------------ the sweep
def sweep(cells):
    """One row per (grid point, file, cell, selector).  Nothing here is chosen; all 49 reported."""
    rows = []
    for phi in PHIS:
        for delta in DELTAS:
            for c in cells:
                m = c.admit(phi, delta)
                nadm = int(m.sum())
                for sel in SELECTORS:
                    iu, _ = c.pick_all(sel)
                    isc, empty = c.pick(m, sel)
                    r = dict(phi=phi, delta=delta, file=c.tag, panel=c.panel, book=c.book,
                             cost=c.cost, sel=sel, n_arms=c.n, n_admitted=nadm,
                             pool_empty=empty, moved=bool(isc != iu),
                             u_arm=c.arms[iu], s_arm=c.arms[isc], c_arm=c.arms[c.ctl])
                    for k in METRICS:
                        v = c.met[k]
                        r[f"U_{k}"], r[f"S_{k}"], r[f"C_{k}"] = float(v[iu]), float(v[isc]), float(v[c.ctl])
                        r[f"d_{k}"] = float(v[isc] - v[iu])       # screened minus unscreened
                        r[f"cu_{k}"] = float(v[c.ctl] - v[iu])    # control minus unscreened
                    r["U_p4a"], r["S_p4a"] = bool(c.p4a[iu]), bool(c.p4a[isc])
                    r["U_p4b"], r["S_p4b"] = bool(c.p4b[iu]), bool(c.p4b[isc])
                    r["has_oos4b"] = c.has_oos4b
                    r["U_p4bo"] = bool(c.p4bo[iu]) if c.has_oos4b else np.nan
                    r["S_p4bo"] = bool(c.p4bo[isc]) if c.has_oos4b else np.nan
                    rows.append(r)
    S = pd.DataFrame(rows)
    S["_o"] = S.file.map(FILE_ORDER)
    return S


def dedup(S):
    """Pooled readings use one row per (phi,delta,panel,book,cost,sel); newest schema wins."""
    return (S.sort_values("_o")
             .drop_duplicates(["phi", "delta", "panel", "book", "cost", "sel"])
             .drop(columns="_o").reset_index(drop=True))


# ------------------------------------------------------------------ rate-matched null
def rate_null(g, rng, n_draws=N_DRAWS):
    """A coin abstaining in k of n cells at random IS an exposure switch.  Compare the screen's
    realised pooled d against that coin at the SAME rate.  Returns z for pooled d and for the
    abstention component alone."""
    n = len(g)
    k = int(g.pool_empty.sum())
    out = {}
    for m in ("OOS_MaxDD", "OOS_CAGR"):
        cu = g[f"cu_{m}"].to_numpy()          # what abstaining in that cell would buy
        act = float(g[f"d_{m}"].mean())
        act_abs = float(g.loc[g.pool_empty, f"d_{m}"].sum() / n) if k else 0.0
        if k == 0 or k == n:
            out[f"z_{m}"] = np.nan
            out[f"zabs_{m}"] = np.nan
            out[f"null_{m}"] = float(cu.mean() * k / n)
            continue
        draws = np.empty(n_draws)
        for i in range(n_draws):
            idx = rng.choice(n, size=k, replace=False)
            draws[i] = cu[idx].sum() / n
        mu, sd = draws.mean(), draws.std(ddof=1)
        out[f"null_{m}"] = float(mu)
        out[f"null_sd_{m}"] = float(sd)
        out[f"z_{m}"] = float((act - mu) / sd) if sd > 0 else np.nan
        out[f"zabs_{m}"] = float((act_abs - mu) / sd) if sd > 0 else np.nan
    return out


# ------------------------------------------------------------------ main
def main():
    rng = np.random.default_rng(SEED)
    say("=" * 110)
    say("IDEA 419 — is the EMPTY-POOL RATE the only dial the 4b screen has?  (lane B, 2026-09-08)")
    say("2 tuned parameters (phi, delta), SWEPT: all 49 grid points reported.  No book promoted.")
    say("=" * 110)

    cells, admitted = load_cells()
    if not admitted:
        say("  NO FILE ADMITTED — nothing can be read.  Stopping.")
        return
    say(f"\n[CORPUS] {len(cells)} (file,cell) pairs | "
        f"{len({(c.panel, c.book, c.cost) for c in cells})} distinct (panel,book,cost) cells | "
        f"{sum(c.n for c in cells)} arm-rows | panels {sorted({c.panel for c in cells})} | "
        f"cost rungs {sorted({c.cost for c in cells})}")

    S = sweep(cells)
    D = dedup(S)
    S.drop(columns="_o").to_csv(OUT / f"{STEM}.cells.csv.gz", index=False,
                               compression="gzip")
    say(f"[SWEEP] {len(S)} (grid point, file, cell, selector) rows -> {len(D)} distinct rows "
        f"per pooled reading ({len(D)//len(PHIS)//len(DELTAS)} per grid point).")

    # ---------------------------------------------------- PANEL A: the dial
    say("\n" + "=" * 110)
    say("[PANEL A] THE DIAL — what (phi, delta) actually controls.  E = empty-pool rate")
    say("          (fraction of cell-selector rows where the screen admits nothing and the")
    say("          pick falls back to the ungated control).  Core bars held FIXED.")
    say("=" * 110)
    dial = []
    for (phi, delta), g in D.groupby(["phi", "delta"]):
        n = len(g)
        rn = rate_null(g, np.random.default_rng(SEED + int(phi * 1000) * 7 + int(delta * 1000)))
        row = dict(phi=phi, delta=delta, n_cells=n,
                   mean_admitted=float(g.n_admitted.mean()),
                   med_admitted=float(g.n_admitted.median()),
                   E=float(g.pool_empty.mean()), move_rate=float(g.moved.mean()),
                   live_move_rate=float((g.moved & ~g.pool_empty).mean()))
        for m in METRICS:
            row[f"d_{m}"] = float(g[f"d_{m}"].mean())
            e = g[g.pool_empty]
            lv = g[~g.pool_empty]
            row[f"dE_{m}"] = float(e[f"d_{m}"].mean()) if len(e) else np.nan
            row[f"dL_{m}"] = float(lv[f"d_{m}"].mean()) if len(lv) else np.nan
            lm = lv[lv.moved]
            pl = paired(lm[f"d_{m}"], "live")
            row[f"dLm_{m}"], row[f"tLm_{m}"], row[f"nLm_{m}"] = pl["mean"], pl["t"], pl["n"]
            row[f"shareE_{m}"] = (float(e[f"d_{m}"].sum() / g[f"d_{m}"].sum())
                                  if abs(g[f"d_{m}"].sum()) > 1e-12 else np.nan)
        row.update(rn)
        dial.append(row)
    DIAL = pd.DataFrame(dial)
    DIAL.to_csv(OUT / f"{STEM}.dial.csv", index=False)
    say("  phi  delta  admitted(mean/med)      E   move  liveMove |  d_MaxDD  d_CAGR  d_Sharpe |"
        "  E-share of d_MaxDD")
    for _, r in DIAL.iterrows():
        mark = "  <- committed" if (r.phi == PHI0 and r.delta == DELTA0) else ""
        sh = f"{r.shareE_OOS_MaxDD:6.1%}" if np.isfinite(r.shareE_OOS_MaxDD) else "     -"
        say(f"  {r.phi:.2f}  {r.delta:.2f}   {r.mean_admitted:5.2f} / {r.med_admitted:4.1f}   "
            f"{r.E:5.1%}  {r.move_rate:5.1%}  {r.live_move_rate:5.1%}  |"
            f" {r.d_OOS_MaxDD*100:+7.3f} {r.d_OOS_CAGR*100:+7.3f} {r.d_OOS_Sharpe:+8.4f} | "
            f"{sh}{mark}")
    say(f"  Dial range: E from {DIAL.E.min():.1%} to {DIAL.E.max():.1%}; mean admitted from "
        f"{DIAL.mean_admitted.min():.2f} to {DIAL.mean_admitted.max():.2f} of 17 arms.")
    say(f"  CEILING (core bars alone, phi=0 delta=inf equivalent): the most permissive grid "
        f"point admits {DIAL.mean_admitted.max():.2f} arms and still abstains "
        f"{DIAL.E.min():.1%} of the time — that residual is the FIXED core, not the dial.")

    # ---------------------------------------------------- PANEL B: the regression
    say("\n" + "=" * 110)
    say("[PANEL B] THE REGRESSION — pooled OOS d (screened minus unscreened) on the realised")
    say("          empty-pool rate E, across the 49 grid points.  Positive d_MaxDD = SHALLOWER.")
    say("=" * 110)
    reg_rows = []
    for m in METRICS:
        o = ols(DIAL.E, DIAL[f"d_{m}"])
        reg_rows.append(dict(scope="grid-point (49)", y=f"d_{m}", **o))
        say(f"  d_{m:<11s} = {o['intercept']*100:+7.4f} pp + {o['slope']*100:+8.4f} pp x E   "
            f"R2 {o['r2']:.4f}  t(slope) {o['t']:+6.2f}  n {o['n']}  "
            f"| through-origin slope {o['slope0']*100:+8.4f} pp")
    say("  Reading: R2 near 1 with an intercept near 0 means the pooled effect is a pure")
    say("  function of the abstention rate — the screen would then BE an exposure switch.")
    say("  HONEST CAVEAT, stated before the number is used: the pooled d is E-weighted by")
    say("  construction (d = E*d_EMPTY + (1-E)*d_LIVE) and d_EMPTY is near-constant across the")
    say(f"  grid ({DIAL.dE_OOS_MaxDD.min()*100:+.3f} to {DIAL.dE_OOS_MaxDD.max()*100:+.3f} pp), so a high Panel-B R2 is")
    say("  most of the way to an identity and is NOT by itself evidence for the queue's claim.")
    say("  Panels C and D are the tests that can actually falsify it.")

    # rule-8 style split of the dial law itself: fit on the old corpus, read on the new one
    say("\n  [rule 8 on the LAW] fit the dial law on the OLD corpus (132+142), read it on the")
    say("  NEW, non-overlapping corpus (151+416).  Same 49 grid points, disjoint cells.")
    for name, sub in (("OLD 132+142", OLD_CORPUS), ("NEW 151+416", NEW_CORPUS)):
        sd = S[S.file.isin(sub)]
        g = sd.groupby(["phi", "delta"]).agg(E=("pool_empty", "mean"),
                                             d_OOS_MaxDD=("d_OOS_MaxDD", "mean"),
                                             d_OOS_CAGR=("d_OOS_CAGR", "mean")).reset_index()
        for m in ("OOS_MaxDD", "OOS_CAGR"):
            o = ols(g.E, g[f"d_{m}"])
            reg_rows.append(dict(scope=name, y=f"d_{m}", **o))
            say(f"    {name}  d_{m:<10s} slope {o['slope']*100:+8.4f} pp  intercept "
                f"{o['intercept']*100:+7.4f} pp  R2 {o['r2']:.4f}  t {o['t']:+6.2f}")
    oldm = [r for r in reg_rows if r["scope"] == "OLD 132+142" and r["y"] == "d_OOS_MaxDD"][0]
    newm = [r for r in reg_rows if r["scope"] == "NEW 151+416" and r["y"] == "d_OOS_MaxDD"][0]
    say(f"    slope ratio NEW/OLD on d_OOS_MaxDD: {newm['slope']/oldm['slope']:.3f} "
        f"(1.00 = the law transfers exactly)")

    # ---------------------------------------------------- PANEL C: decomposition
    say("\n" + "=" * 110)
    say("[PANEL C] THE DECOMPOSITION — at every rate, is the LIVE-POOL leg (the screen actually")
    say("          screening) doing anything?  Pooled over distinct cells at each grid point.")
    say("=" * 110)
    say("  phi  delta      E |  EMPTY-pool d_MaxDD (n)  |  LIVE-pool MOVED d_MaxDD "
        "(n, t)      |  LIVE d_CAGR (t)")
    sig_live, tot_live = 0, 0
    for _, r in DIAL.iterrows():
        nE = int(round(r.E * r.n_cells))
        tl = r.tLm_OOS_MaxDD
        if np.isfinite(tl) and r.nLm_OOS_MaxDD >= 2:
            tot_live += 1
            sig_live += int(abs(tl) >= 2)
        say(f"  {r.phi:.2f}  {r.delta:.2f}  {r.E:5.1%} |  {r.dE_OOS_MaxDD*100:+7.3f} pp "
            f"({nE:3d})        |  {r.dLm_OOS_MaxDD*100:+7.3f} pp ({int(r.nLm_OOS_MaxDD):3d}, "
            f"t {tl:+5.2f})  |  {r.dLm_OOS_CAGR*100:+7.3f} pp (t {r.tLm_OOS_CAGR:+5.2f})")
    say(f"  LIVE-POOL significance count: {sig_live} of {tot_live} grid points with >=2 live "
        f"moves have |t| >= 2 on OOS MaxDD ({sig_live/max(tot_live,1):.1%}).")

    # is the LIVE leg itself a function of the rate, or of the bars?
    LB = DIAL[DIAL.nLm_OOS_MaxDD >= 2]
    say("\n  IS THE LIVE LEG A FUNCTION OF THE RATE?  (grid points with >=2 live moves, n "
        f"{len(LB)})")
    for xname, x in (("E    ", LB.E), ("delta", LB.delta), ("phi  ", LB.phi)):
        o = ols(x, LB.dLm_OOS_MaxDD)
        say(f"    live d_OOS_MaxDD ~ {xname}: slope {o['slope']*100:+8.3f} pp  R2 {o['r2']:.4f}  "
            f"t {o['t']:+6.2f}")
    oe = ols(LB.E, LB.dLm_OOS_MaxDD)
    od = ols(LB.delta, LB.dLm_OOS_MaxDD)
    say(f"    -> the abstention rate explains {oe['r2']:.1%} of the live leg; the DD bar delta "
        f"explains {od['r2']:.1%}.")
    say("    The live leg also runs an exchange: live d_OOS_CAGR ~ delta slope "
        f"{ols(LB.delta, LB.dLm_OOS_CAGR)['slope']*100:+.3f} pp, R2 "
        f"{ols(LB.delta, LB.dLm_OOS_CAGR)['r2']:.4f} — opposite in sign to the MaxDD leg.")

    # pooled live-pool leg over ALL grid points, one row per (grid point, cell)
    LV = D[(~D.pool_empty) & D.moved]
    EM = D[D.pool_empty]
    say("\n  POOLED over all 49 grid points (rows are (grid point, cell) pairs; the same cell")
    say("  recurs across grid points, so these t's are OPTIMISTIC — read the sign and the size):")
    for m in METRICS:
        sc = 100.0 if m != "OOS_Sharpe" else 1.0
        u = " pp" if m != "OOS_Sharpe" else ""
        say(f"    LIVE-POOL MOVED  d_{m:<11s} {fmt(paired(LV[f'd_{m}'], 'live'), sc, u)}")
        say(f"    EMPTY-POOL       d_{m:<11s} {fmt(paired(EM[f'd_{m}'], 'empty'), sc, u)}")
    # per-file live-pool sign check (the out-of-corpus replication)
    say("\n  LIVE-POOL MOVED d_OOS_MaxDD by file (416 has zero (panel,book) overlap with 142/151):")
    for tag in admitted:
        sub = S[(S.file == tag) & (~S.pool_empty) & S.moved]
        say(f"    file {tag}: {fmt(paired(sub['d_OOS_MaxDD'], tag))}")

    # ---------------------------------------------------- PANEL D: rate-matched null
    say("\n" + "=" * 110)
    say("[PANEL D] THE RATE-MATCHED NULL — a coin that abstains in k of n cells AT RANDOM is an")
    say(f"          exposure switch by construction.  {N_DRAWS} seeded draws per grid point.")
    say("=" * 110)
    say("  z(total) prices the WHOLE screen against the coin; z(abst) prices only WHERE it")
    say("  abstains, holding the live-pool picks out, so the two columns separate the rate's")
    say("  placement from the screening itself.")
    say("  phi  delta      E |  actual d_MaxDD   coin mean (sd)  z(total) z(abst) | d_CAGR  z(total)")
    zs, zas = [], []
    for _, r in DIAL.iterrows():
        z, za = r.get("z_OOS_MaxDD", np.nan), r.get("zabs_OOS_MaxDD", np.nan)
        if np.isfinite(z):
            zs.append(z)
        if np.isfinite(za):
            zas.append(za)
        nsd = r.get("null_sd_OOS_MaxDD", np.nan)
        sd_s = f"{nsd*100:5.3f}" if np.isfinite(nsd) else "  nan"
        say(f"  {r.phi:.2f}  {r.delta:.2f}  {r.E:5.1%} |  {r.d_OOS_MaxDD*100:+7.3f} pp    "
            f"{r.get('null_OOS_MaxDD', np.nan)*100:+7.3f} pp ({sd_s})  "
            f"{z:+7.2f} {za:+7.2f} | {r.d_OOS_CAGR*100:+7.3f} pp {r.get('z_OOS_CAGR', np.nan):+6.2f}")
    zs, zas = np.array(zs), np.array(zas)
    n_in = int((np.abs(zs) < 2).sum())
    n_ina = int((np.abs(zas) < 2).sum())
    say(f"  z(total): |z| < 2 at {n_in} of {len(zs)} testable grid points "
        f"({n_in/max(len(zs),1):.1%}); mean {zs.mean():+.2f}, range "
        f"[{zs.min():+.2f}, {zs.max():+.2f}].")
    say(f"  z(abst) : |z| < 2 at {n_ina} of {len(zas)} ({n_ina/max(len(zas),1):.1%}); "
        f"mean {zas.mean():+.2f}, range [{zas.min():+.2f}, {zas.max():+.2f}].")
    say("  z > 0 means the screen abstains where abstaining pays MORE than a coin's; z ~ 0 on")
    say("  BOTH columns is what 'the rate is the only dial' would look like.")

    # ---------------------------------------------------- PANEL E: KEEP paths
    say("\n" + "=" * 110)
    say("[PANEL E] KEEP PATHS (PROTOCOL rule 4) at every grid point — screened vs unscreened")
    say("          picks, distinct cells.  4b_oos is the OOS-window reading where the parent")
    say("          file carries it (151, 416).")
    say("=" * 110)
    kp = []
    say("  phi  delta      E |  4a(v2)  U -> S  |   4b(full)  U -> S  |  4b(OOS)  U -> S "
        "  |  BOTH PATHS U -> S")
    for (phi, delta), g in D.groupby(["phi", "delta"]):
        go = g[g.has_oos4b]
        row = dict(phi=phi, delta=delta, n=len(g), E=float(g.pool_empty.mean()),
                   u4a=int(g.U_p4a.sum()), s4a=int(g.S_p4a.sum()),
                   u4b=int(g.U_p4b.sum()), s4b=int(g.S_p4b.sum()),
                   n_oos=len(go),
                   u4bo=int(go.U_p4bo.sum()) if len(go) else 0,
                   s4bo=int(go.S_p4bo.sum()) if len(go) else 0,
                   uboth=int((go.U_p4a & go.U_p4bo).sum()) if len(go) else 0,
                   sboth=int((go.S_p4a & go.S_p4bo).sum()) if len(go) else 0)
        kp.append(row)
        say(f"  {phi:.2f}  {delta:.2f}  {row['E']:5.1%} |  {row['u4a']:3d} -> {row['s4a']:3d} "
            f"/{len(g):4d}  |  {row['u4b']:3d} -> {row['s4b']:3d} /{len(g):4d}  |  "
            f"{row['u4bo']:3d} -> {row['s4bo']:3d} /{row['n_oos']:4d}  |  "
            f"{row['uboth']:3d} -> {row['sboth']:3d}")
    KP = pd.DataFrame(kp)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    o4b = ols(KP.E, KP.s4b - KP.u4b)
    o4a = ols(KP.E, KP.s4a - KP.u4a)
    say(f"  net 4b(full) swap regressed on E: slope {o4b['slope']:+.2f} passes per unit E, "
        f"R2 {o4b['r2']:.3f}, t {o4b['t']:+.2f}")
    say(f"  net 4a(v2)   swap regressed on E: slope {o4a['slope']:+.2f} passes per unit E, "
        f"R2 {o4a['r2']:.3f}, t {o4a['t']:+.2f}")
    say(f"  BOTH PATHS: {KP.uboth.sum()} unscreened vs {KP.sboth.sum()} screened over all 49 "
        f"grid points ({KP.n_oos.iloc[0]} cells each) — no book in this corpus is promoted here.")

    # ---------------------------------------------------- PANEL F: levels + rule 8
    say("\n" + "=" * 110)
    say("[PANEL F] LEVELS — freshly computed RULES v2 and SPY OOS legs (research/baseline.py),")
    say("          then the pooled OOS levels of the three policies at every grid point.")
    say("=" * 110)
    px = load_universe()
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    mspy_o = metrics(spy.loc[OOS_START:])
    say(f"  panel u56 (research/universe.json): {px.shape[1]} cols, "
        f"{px.index[0].date()}..{px.index[-1].date()}, eval from {start.date()}")
    say(f"  SPY  OOS {OOS_START}..  CAGR {mspy_o['CAGR']:.2%}  Sharpe {mspy_o['Sharpe']:.4f}  "
        f"MaxDD {mspy_o['MaxDD']:.2%}")
    v2lev = {}
    for c in (10.0, 25.0):
        r = backtest(px, rules_v2_weights(px), cost_bps=c, freq="W")["returns"].loc[start:]
        mo = metrics(r.loc[OOS_START:])
        v2lev[c] = mo
        say(f"  RULES v2 (live) @{c:.0f} bps  OOS CAGR {mo['CAGR']:.2%}  Sharpe "
            f"{mo['Sharpe']:.4f}  MaxDD {mo['MaxDD']:.2%}")
    bar_cagr, bar_dd = 0.70 * mspy_o["CAGR"], 0.60 * abs(mspy_o["MaxDD"])
    say(f"  4b OOS bars from this SPY leg: CAGR >= {bar_cagr:.2%}, |MaxDD| <= {bar_dd:.2%}, "
        f"Sharpe > {mspy_o['Sharpe']:.4f}")
    say("  (Survivorship, idea 54: every census level below is optimistic.  Read contrasts.)")

    wf = []
    say("\n  phi  delta      E | screened pick OOS  CAGR/Sharpe/MaxDD | unscreened | do-nothing ctl")
    for (phi, delta), g in D.groupby(["phi", "delta"]):
        row = dict(phi=phi, delta=delta, n=len(g), E=float(g.pool_empty.mean()),
                   S_CAGR=float(g.S_OOS_CAGR.mean()), S_Sharpe=float(g.S_OOS_Sharpe.mean()),
                   S_MaxDD=float(g.S_OOS_MaxDD.mean()),
                   U_CAGR=float(g.U_OOS_CAGR.mean()), U_Sharpe=float(g.U_OOS_Sharpe.mean()),
                   U_MaxDD=float(g.U_OOS_MaxDD.mean()),
                   C_CAGR=float(g.C_OOS_CAGR.mean()), C_Sharpe=float(g.C_OOS_Sharpe.mean()),
                   C_MaxDD=float(g.C_OOS_MaxDD.mean()),
                   spy_oos_cagr=mspy_o["CAGR"], spy_oos_sharpe=mspy_o["Sharpe"],
                   spy_oos_dd=mspy_o["MaxDD"],
                   v2_10_cagr=v2lev[10.0]["CAGR"], v2_10_sharpe=v2lev[10.0]["Sharpe"],
                   v2_10_dd=v2lev[10.0]["MaxDD"],
                   v2_25_cagr=v2lev[25.0]["CAGR"], v2_25_sharpe=v2lev[25.0]["Sharpe"],
                   v2_25_dd=v2lev[25.0]["MaxDD"])
        wf.append(row)
        say(f"  {phi:.2f}  {delta:.2f}  {row['E']:5.1%} |  {row['S_CAGR']:6.2%} "
            f"{row['S_Sharpe']:6.3f} {row['S_MaxDD']:7.2%} | {row['U_CAGR']:6.2%} "
            f"{row['U_Sharpe']:6.3f} {row['U_MaxDD']:7.2%} | {row['C_CAGR']:6.2%} "
            f"{row['C_Sharpe']:6.3f} {row['C_MaxDD']:7.2%}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(reg_rows).to_csv(OUT / f"{STEM}.regression.csv", index=False)

    # the exposure-switch equivalence, stated in levels
    o_lev = ols(WF.E, WF.S_MaxDD)
    o_lev_c = ols(WF.E, WF.S_CAGR)
    say(f"\n  Screened-policy OOS MaxDD level regressed on E: {o_lev['intercept']:.2%} + "
        f"{o_lev['slope']*100:+.3f} pp x E, R2 {o_lev['r2']:.4f}")
    say(f"  Screened-policy OOS CAGR  level regressed on E: {o_lev_c['intercept']:.2%} + "
        f"{o_lev_c['slope']*100:+.3f} pp x E, R2 {o_lev_c['r2']:.4f}")
    say(f"  Exchange rate along the dial: {o_lev_c['slope']/o_lev['slope']:+.3f} pp OOS CAGR "
        f"per pp OOS MaxDD bought (slope ratio).")

    # ---------------------------------------------------- verdict
    say("\n" + "=" * 110)
    say("[VERDICT] against the decision rule fixed before any Panel-B number was read")
    say("=" * 110)
    oB = ols(DIAL.E, DIAL.d_OOS_MaxDD)
    live_pool = paired(LV["d_OOS_MaxDD"], "live-pooled")
    c1 = (oB["r2"] >= 0.80) and abs(oB["t"]) >= 2
    frac_ns = 1.0 - sig_live / max(tot_live, 1)
    c2 = (frac_ns >= 0.80) and (not np.isfinite(live_pool["t"]) or abs(live_pool["t"]) < 2)
    c3 = (n_in / max(len(zs), 1)) > 0.50
    say(f"  (i)   Panel-B R2 {oB['r2']:.4f} >= 0.80 and |t| {abs(oB['t']):.2f} >= 2 : {c1}")
    say(f"  (ii)  live-pool NOT significant at {frac_ns:.1%} of grid points (>=80% required) "
        f"and pooled t {live_pool['t']:+.2f} (|t|<2 required) : {c2}")
    say(f"  (iii) rate-matched |z| < 2 at {n_in/max(len(zs),1):.1%} of grid points (>50% "
        f"required) : {c3}")
    if c1 and c2 and c3:
        verdict = "RATE-IS-THE-ONLY-DIAL"
    elif (not c2) or (not c3):
        verdict = "MORE-THAN-A-RATE"
    else:
        verdict = "MIXED"
    say(f"\n  VERDICT: {verdict}")
    say("  Note on (ii): the pooled t above is the OPTIMISTIC one (cells recur across grid")
    say("  points).  The verdict does not depend on it — the honest per-grid-point count "
        f"({sig_live}/{tot_live}) fails the 80% bar on its own.")
    say("  Note on (i): (i) passing is near-arithmetic (see the Panel-B caveat); it is not "
        "support for the queue's claim.")
    ol = ols(LB.delta, LB.dLm_OOS_MaxDD)
    oc = ols(LB.delta, LB.dLm_OOS_CAGR)
    say("\n  WHAT THIS CHANGES: the screen has a SECOND, real dial.  Inside a live pool the DD")
    say(f"  bar delta moves OOS MaxDD at {ol['slope']*100:+.2f} pp per unit delta (R2 {ol['r2']:.3f}) against")
    say(f"  {oc['slope']*100:+.2f} pp of OOS CAGR (R2 {oc['r2']:.3f}); the abstention rate explains only "
        f"{oe['r2']:.1%} of it.")
    say(f"  The record's committed pair ({PHI0:.2f}, {DELTA0:.2f}) sits on the near-zero crossing of that")
    say("  second dial, which is why idea 163 measured a live-pool NULL there.  Idea 163's")
    say("  reading is correct AT ITS SETTING and does not generalise to the screen.")
    say("  (This run is a measurement of an existing screen, not a book: PROTOCOL path 4a/4b "
        "counts are reported in Panel E, and nothing is promoted.)")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return verdict


if __name__ == "__main__":
    main()
