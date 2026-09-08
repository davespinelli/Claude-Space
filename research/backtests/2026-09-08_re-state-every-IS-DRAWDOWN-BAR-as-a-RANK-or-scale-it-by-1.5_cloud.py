#!/usr/bin/env python3
"""Idea 421 — re-state every IS DRAWDOWN BAR as a RANK, or scale it by 1.5.  (cloud, 2026-09-08)

QUESTION (QUEUE 421): idea 420 found the IS window RANKS drawdown well (within-cell slope
+0.918, top-quartile hit 0.580) but is optimistic in LEVEL by 1.49x on 96.2% of arms.
"Re-run the record's committed IS-4b screens with the DD leg (a) as a within-cell RANK bar
and (b) as an ABSOLUTE bar scaled by 1.5, and report how many admissions and picks change."

THE BAR UNDER TEST.  The record's committed IS-4b screen (ideas 132/142/151/416, measured by
163 and swept by 419) admits an arm when

    core:  IS_m_H1 > 0  and  IS_m_H2 > 0
    DD:    delta * |SPY_IS_MaxDD| - |IS_MaxDD| > 0        (delta = 0.60, PROTOCOL 4b)
    CAGR:  IS_CAGR - phi * SPY_IS_CAGR > 0                (phi   = 0.70, PROTOCOL 4b)

Only the DD leg moves here; core and CAGR legs are held at their committed form throughout,
so every difference reported is attributable to the DD leg alone.

THE TWO TUNED PARAMETERS (max 2, per the queue): FORM and SCALE.  Both are SWEPT, and all
18 grid points are reported, none hidden:
    ABS(s)   :  0.60 * s * |SPY_IS_MaxDD| - |IS_MaxDD| > 0 ,  s in 0.50 .. 2.00 (7 points)
                s = 1.00 is the COMMITTED bar; s = 1.50 is the queue's leg (b).
    RANK(q)  :  within-cell ordinal rank of |IS_MaxDD| (shallowest first) <= max(1, floor(q*n)),
                q in 0.10 .. 1.00 (10 points).  This is the queue's leg (a).
    OFF      :  DD leg deleted (idea 163's S2 reference, 1 point).

DESIGN
  PART A — CENSUS of the record.  Every committed grid carrying a 4b-aware admission mask
    (132/142/151/416; 3,570 arm-rows, 210 cells, 4 panels, 3 rungs) behind the two gates
    idea 419 used: G1 the screen must reconstruct from raw columns at the committed
    (phi, delta); G2 every committed deterministic pick must reproduce arm-for-arm from it.
    Then, per grid point x selector: admission counts, empty-pool rate, PICK CHANGES against
    the committed bar, and the paired OOS consequence (MaxDD / CAGR / Sharpe), split
    EMPTY-POOL vs LIVE-POOL because idea 163 showed the pooled number is mostly fallback.
  PART B — the same three forms priced on REAL PRICES: a fresh 31-arm menu (band x gross x
    cadence + an ungated control) on u56 / broad136 / SMALL439 x 10 and 25 bps, IS through
    2016-12-31, OOS 2017-01-01.. read once, with fresh RULES v2 and SPY levels and BOTH
    KEEP paths on the full and the OOS window.

RULE 8.  (i) The rank bar's operating point q* is fixed by EQUAL ADMISSION to the committed
  bar computed on IS columns only — no OOS number is read to set it.  (ii) The corpus is
  additionally split by parent-file date: q* re-derived on the first half, the OOS
  consequence read on the second half untouched.  (iii) Part B's screens see only the IS
  window; the OOS window is read once, after the forms are fixed.

PROTOCOL: 10 bps anchor (25 bps also reported), next-day execution (engine), no shorting.
SURVIVORSHIP: universe_broad.json and the sub-$2B panel are CURRENT constituents only
  (data/SMALL_PANEL_README.md) — read the contrasts across forms, never the levels.
Deterministic, standalone.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
Writes .console.txt, .sweep.csv, .grid.csv, .picks.csv.
"""
from __future__ import annotations

import sys
from math import lgamma
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from baseline import band_state, load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_re-state-every-IS-DRAWDOWN-BAR-as-a-RANK-or-scale-it-by-1.5_cloud"
OUT = ROOT / "research" / "backtests"
PHI0, DELTA0 = 0.70, 0.60                 # the record's committed screen
IS_END, OOS_START = "2016-12-31", "2017-01-01"

SCALES = [0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00]        # ABS(s); 1.00 committed, 1.50 asked
QS = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]   # RANK(q)
SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_Calmar": "IS_Calmar",
             "K_MaxDD": "IS_MaxDD", "K_CAGR": "IS_CAGR"}
OOSM = ["OOS_MaxDD", "OOS_CAGR", "OOS_Sharpe"]

# (tag, stem, committed admission column, (selector col, pool col), pool labels, picks arm col)
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
FILE_DATE = {"132": "2026-09-05", "142": "2026-09-08", "151": "2026-09-08", "416": "2026-09-08"}

LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


# ------------------------------------------------------------------ statistics
def _lchoose(n, k):
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def paired(x, label="", **extra):
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
    return (f"n {d['n']:4d}  mean {d['mean'] * scale:+8.4f}{unit}  t {d['t']:+6.2f}  "
            f"{d['wins']:3d}W/{d['losses']:3d}L/{d['ties']:3d}T  sign p {d['sign_p']:.4f}")


# ------------------------------------------------------------------ cell machinery
class Cell:
    """One (file, panel, book, cost): arm-sorted arrays, enough to re-derive any DD leg."""

    def __init__(self, tag, key, s):
        s = s.sort_values("arm").reset_index(drop=True)
        self.tag, self.panel, self.book, self.cost = tag, key[0], key[1], key[2]
        self.date = FILE_DATE[tag]
        self.arms = s.arm.to_numpy()
        self.n = len(s)
        self.core = ((s.IS_m_H1 > 0) & (s.IS_m_H2 > 0)).to_numpy()
        self.isdd = s.IS_MaxDD.abs().to_numpy()
        self.iscagr = s.IS_CAGR.to_numpy()
        sdd = ((s.IS_m_DD + s.IS_MaxDD.abs()) / DELTA0).to_numpy()
        sca = ((s.IS_CAGR - s.IS_m_CAGR) / PHI0).to_numpy()
        assert np.ptp(sdd) < 1e-9 and np.ptp(sca) < 1e-9, f"SPY IS bars not constant in {key}"
        self.sdd, self.scagr = float(sdd[0]), float(sca[0])
        self.cagr_leg = self.iscagr - PHI0 * self.scagr > 0
        # ordinal rank of |IS_MaxDD|, shallowest = 1, ties broken by arm-sorted order
        self.ddrank = np.argsort(np.argsort(self.isdd, kind="stable"), kind="stable") + 1
        self.sel = {k: s[c].to_numpy() for k, c in SELECTORS.items()}
        self.met = {m: s[m].to_numpy() for m in OOSM}
        self.ctl = int(np.where(self.arms == "control")[0][0])
        a4a = "pass4a_v2" if "pass4a_v2" in s.columns else "pass4a"
        self.p4a = s[a4a].to_numpy().astype(bool)
        self.p4b = s["pass4b"].to_numpy().astype(bool)
        self.has_oos4b = "pass4b_oos" in s.columns
        self.p4bo = (s["pass4b_oos"].to_numpy().astype(bool) if self.has_oos4b
                     else np.zeros(self.n, bool))

    # ---- the DD leg, in its three forms
    def dd_abs(self, s):
        return DELTA0 * s * self.sdd - self.isdd > 0

    def dd_rank(self, q):
        return self.ddrank <= max(1, int(np.floor(q * self.n)))

    def dd_off(self):
        return np.ones(self.n, bool)

    def admit(self, form, p):
        leg = {"ABS": self.dd_abs, "RANK": self.dd_rank}.get(form, lambda _: self.dd_off())
        return self.core & self.cagr_leg & leg(p)

    def pick(self, mask, sel):
        """Parents' rule: argmax of the selector's IS column inside the mask; control if empty."""
        if not mask.any():
            return self.ctl, True
        return int(np.argmax(np.where(mask, self.sel[sel], -np.inf))), False


def load_cells():
    say("\n[GATE] two gates, both from idea 419: G1 the committed screen must reconstruct from")
    say("       raw columns; G2 every committed deterministic pick must reproduce from it.")
    cells, admitted = [], []
    for tag, stem, admcol, keycols, lab, armcol in FILES:
        g = pd.read_csv(OUT / f"{stem}.grid.csv")
        p = pd.read_csv(OUT / f"{stem}.picks.csv")
        sdd = (g.IS_m_DD + g.IS_MaxDD.abs()) / DELTA0
        sca = (g.IS_CAGR - g.IS_m_CAGR) / PHI0
        rec = ((g.IS_m_H1 > 0) & (g.IS_m_H2 > 0)
               & (DELTA0 * sdd - g.IS_MaxDD.abs() > 0) & (g.IS_CAGR - PHI0 * sca > 0))
        g1_hits = int((rec == g[admcol].astype(bool)).sum())
        g1 = g1_hits == len(g)
        bars = g.assign(_d=sdd, _c=sca).groupby("panel")[["_d", "_c"]].agg(np.ptp).max().max()
        cl = {k: Cell(tag, k, s) for k, s in g.groupby(["panel", "book", "cost"], sort=True)}
        rows = []
        for k, c in cl.items():
            m = c.admit("ABS", 1.00)
            for sel in SELECTORS:
                iu = int(np.argmax(c.sel[sel]))
                isc, _ = c.pick(m, sel)
                rows.append(dict(panel=k[0], book=k[1], cost=k[2], **{keycols[0]: sel},
                                 **{keycols[1]: lab["U"]}, arm_re=c.arms[iu]))
                rows.append(dict(panel=k[0], book=k[1], cost=k[2], **{keycols[0]: sel},
                                 **{keycols[1]: lab["S"]}, arm_re=c.arms[isc]))
        R = pd.DataFrame(rows)
        m = p.merge(R, on=["panel", "book", "cost", keycols[0], keycols[1]], how="inner")
        g2_hits = int((m[armcol] == m.arm_re).sum())
        ok = g1 and len(m) > 0 and g2_hits == len(m) and bars < 1e-9
        say(f"  {tag}: G1 screen {g1_hits}/{len(g)} rows   G2 picks {g2_hits}/{len(m)}   "
            f"SPY-bar spread {bars:.2e}  ->  {'ADMITTED' if ok else 'REJECTED'}  "
            f"({len(cl)} cells x {list(cl.values())[0].n} arms)")
        if ok:
            admitted.append(tag)
            cells.extend(cl.values())
    say(f"  {len(admitted)} of {len(FILES)} files admitted: {admitted}.  "
        f"{len(cells)} cells, {sum(c.n for c in cells)} arm-rows.")
    return cells, admitted


# ------------------------------------------------------------------ the sweep
GRID = ([("ABS", s) for s in SCALES] + [("RANK", q) for q in QS] + [("OFF", np.nan)])


def sweep(cells):
    """One row per (grid point, cell, selector).  Committed = ABS(1.00); everything is
    reported against it.  No point is hidden and none is chosen here."""
    base = {}
    for c in cells:
        m0 = c.admit("ABS", 1.00)
        for sel in SELECTORS:
            i0, e0 = c.pick(m0, sel)
            base[(id(c), sel)] = (i0, e0, int(m0.sum()))
    rows = []
    for form, p in GRID:
        for c in cells:
            m = c.admit(form, p)
            nadm = int(m.sum())
            for sel in SELECTORS:
                i, empty = c.pick(m, sel)
                i0, e0, n0 = base[(id(c), sel)]
                r = dict(form=form, param=p, point=f"{form}({p:.2f})" if form != "OFF" else "OFF",
                         file=c.tag, date=c.date, panel=c.panel, book=c.book, cost=c.cost,
                         sel=sel, n_arms=c.n, n_admitted=nadm, n_admitted_committed=n0,
                         pool_empty=empty, pool_empty_committed=e0,
                         arm=c.arms[i], arm_committed=c.arms[i0], changed=int(i != i0),
                         pick4a=bool(c.p4a[i]), pick4b=bool(c.p4b[i]),
                         pick4b_oos=(bool(c.p4bo[i]) if c.has_oos4b else np.nan),
                         c4a=bool(c.p4a[i0]), c4b=bool(c.p4b[i0]),
                         c4b_oos=(bool(c.p4bo[i0]) if c.has_oos4b else np.nan))
                for m_ in OOSM:
                    r[m_] = float(c.met[m_][i])
                    r["d_" + m_] = float(c.met[m_][i] - c.met[m_][i0])
                rows.append(r)
    return pd.DataFrame(rows)


def point_table(S):
    """Per grid point: admission, empty-pool rate, pick changes and the paired OOS deltas."""
    out = []
    for pt, g in S.groupby("point", sort=False):
        live = g[~g.pool_empty & ~g.pool_empty_committed]
        mv = g[g.changed == 1]
        row = dict(point=pt, form=g.form.iloc[0], param=g.param.iloc[0], n=len(g),
                   mean_adm=float(g.n_admitted.mean()), med_adm=float(g.n_admitted.median()),
                   E=float(g.pool_empty.mean()), changed=float(g.changed.mean()),
                   changed_live=float(live.changed.mean()) if len(live) else np.nan,
                   n_changed=int(g.changed.sum()))
        for m_ in OOSM:
            row["d" + m_[4:]] = float(g["d_" + m_].mean())
            row["dMV_" + m_[4:]] = float(mv["d_" + m_].mean()) if len(mv) else np.nan
        row["t_dMaxDD"] = paired(g.d_OOS_MaxDD)["t"]
        row["pick4b"] = float(g.pick4b.mean())
        row["pick4b_oos"] = float(g.pick4b_oos.dropna().mean()) if g.pick4b_oos.notna().any() else np.nan
        row["pick4a"] = float(g.pick4a.mean())
        out.append(row)
    return pd.DataFrame(out)


def equal_admission_q(cells, subset=None):
    """RULE 8 (i): fix the rank bar's q by matching the committed bar's ADMISSION RATE.
    Uses IS columns only — no OOS metric is read.  Returns (q*, committed rate, rate at q*)."""
    cs = cells if subset is None else [c for c in cells if subset(c)]
    tgt = float(np.mean([c.admit("ABS", 1.00).sum() / c.n for c in cs]))
    best, bq = np.inf, QS[0]
    tab = []
    for q in QS:
        r = float(np.mean([c.admit("RANK", q).sum() / c.n for c in cs]))
        tab.append((q, r))
        if abs(r - tgt) < best - 1e-12:
            best, bq = abs(r - tgt), q
    return bq, tgt, dict(tab)


# ------------------------------------------------------------------ Part B: fresh prices
def ew_band_weights(px, band, gross, gated=True):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0) if gated else ew


def arm_menu():
    arms = [("control", dict(band=0.0, gross=1.0, freq="W", gated=False))]
    for band in (0.0, 0.015, 0.03, 0.045, 0.06):
        for gross in (0.50, 0.75, 1.00):
            for freq in ("W", "M"):
                arms.append((f"b{band:g}-g{gross:.2f}-{freq}",
                             dict(band=band, gross=gross, freq=freq, gated=True)))
    return arms


def win(r, lo=None, hi=None, prefix=""):
    x = r.loc[lo:hi] if (lo or hi) else r
    m = metrics(x)
    h = len(x) // 2
    return {f"{prefix}CAGR": m["CAGR"], f"{prefix}Sharpe": m["Sharpe"], f"{prefix}MaxDD": m["MaxDD"],
            f"{prefix}H1": metrics(x.iloc[:h])["Sharpe"], f"{prefix}H2": metrics(x.iloc[h:])["Sharpe"]}


def load_panels():
    P = {"u56": load_universe(), "broad136": load_universe(broad=True)}
    small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["small439"] = small[[c for c in small.columns if c not in bad]]
    return P, len(bad)


def keep_paths(r, spy, base):
    def bars(x, b, s):
        mx, mb, ms = metrics(x), metrics(b), metrics(s)
        h = len(x) // 2
        xh = (metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"])
        bh = (metrics(b.iloc[:h])["Sharpe"], metrics(b.iloc[h:])["Sharpe"])
        sh = (metrics(s.iloc[:h])["Sharpe"], metrics(s.iloc[h:])["Sharpe"])
        return (xh[0] > bh[0] and xh[1] > bh[1] and mx["MaxDD"] >= mb["MaxDD"],
                xh[0] > sh[0] and xh[1] > sh[1] and mx["Sharpe"] > ms["Sharpe"]
                and mx["MaxDD"] >= 0.60 * ms["MaxDD"] and mx["CAGR"] >= 0.70 * ms["CAGR"])
    a, b = bars(r, base, spy)
    ao, bo = bars(r.loc[OOS_START:], base.loc[OOS_START:], spy.loc[OOS_START:])
    return dict(pass4a=a, pass4b=b, pass4a_oos=ao, pass4b_oos=bo)


def fresh_grid(panels, costs=(10.0, 25.0)):
    rows, curves, bench = [], {}, {}
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        bench[pname] = dict(SPY=spy, V2=v2)
        univ = px.drop(columns=["SPY"], errors="ignore") if pname == "small439" else px
        raw = {}
        for name, a in arm_menu():
            w = ew_band_weights(univ, a["band"], a["gross"], gated=a["gated"])
            res = backtest(px, w.reindex(columns=px.columns).fillna(0.0), cost_bps=0.0,
                           freq=a["freq"])
            raw[name] = (res["returns"], res["turnover"])
        for c in costs:
            for name, a in arm_menu():
                r0, to = raw[name]
                r = (r0 - to * c / 1e4).loc[start:]          # rung identity (idea 352)
                curves[(pname, c, name)] = r
                row = dict(panel=pname, cost=c, arm=name, band=a["band"], gross=a["gross"],
                           freq=a["freq"], gated=a["gated"], n_arms=31)
                row.update(win(r))
                row.update(win(r, hi=IS_END, prefix="IS_"))
                row.update(win(r, lo=OOS_START, prefix="OOS_"))
                row.update(keep_paths(r, spy, v2))
                rows.append(row)
    return pd.DataFrame(rows), curves, bench


def fresh_screen_row(cell, form, p, sel, spy_is):
    """Apply one DD-leg form to a fresh cell (a DataFrame of arms with IS_/OOS_ columns).
    Core and CAGR legs are the record's committed form: half-Sharpe margins over SPY's IS
    halves, and IS_CAGR above phi x SPY's IS CAGR."""
    c = cell.sort_values("arm").reset_index(drop=True)
    spy_is_dd, spy_is_cagr = spy_is["MaxDD"], spy_is["CAGR"]
    core = (c.IS_H1 - spy_is["H1"] > 0) & (c.IS_H2 - spy_is["H2"] > 0)
    cagr_leg = c.IS_CAGR - PHI0 * spy_is_cagr > 0
    isdd = c.IS_MaxDD.abs().to_numpy()
    if form == "ABS":
        leg = DELTA0 * p * abs(spy_is_dd) - isdd > 0
    elif form == "RANK":
        rk = np.argsort(np.argsort(isdd, kind="stable"), kind="stable") + 1
        leg = rk <= max(1, int(np.floor(p * len(c))))
    else:
        leg = np.ones(len(c), bool)
    m = core.to_numpy() & cagr_leg.to_numpy() & np.asarray(leg)
    ctl = int(np.where(c.arm.to_numpy() == "control")[0][0])
    i = ctl if not m.any() else int(np.argmax(np.where(m, c[SELECTORS[sel]].to_numpy(), -np.inf)))
    return i, c, int(m.sum()), (not m.any())


# ------------------------------------------------------------------ main
def main():
    say("=" * 100)
    say("IDEA 421 — re-state every IS DRAWDOWN BAR as a RANK, or scale it by 1.5   "
        "(cloud, 2026-09-08)")
    say("=" * 100)
    say("Two tuned parameters (FORM, SCALE), both SWEPT: 18 grid points, all reported.")
    say("Committed bar = ABS(1.00).  Queue leg (a) = RANK(q).  Queue leg (b) = ABS(1.50).")

    # ---------------- Part A
    say("\n\n## PART A — the record's committed IS-4b screens, DD leg re-stated\n")
    cells, admitted = load_cells()
    if not admitted:
        say("no admitted file — abort")
        return
    S = sweep(cells)
    S.to_csv(OUT / f"{STEM}.sweep.csv.gz", index=False, compression="gzip")
    say(f"  sweep rows {len(S)} = {len(GRID)} grid points x {len(cells)} cells x "
        f"{len(SELECTORS)} selectors")

    say("\n### ALL 18 GRID POINTS (pooled over 210 cells x 4 selectors = 840 cell-selector rows)")
    P = point_table(S)
    P.to_csv(OUT / f"{STEM}.points.csv", index=False)
    say("  point        adm(mean/med)      E   changed  chg|live |   dMaxDD   dCAGR  dSharpe |"
        "  4b(pick)  4bOOS")
    for _, r in P.iterrows():
        mark = "  <- COMMITTED" if r.point == "ABS(1.00)" else ("  <- queue (b)" if r.point == "ABS(1.50)" else "")
        say(f"  {r.point:11s} {r.mean_adm:5.2f} / {r.med_adm:4.1f}  {r.E:5.1%}  "
            f"{r.changed:6.1%}  {r.changed_live:7.1%} | {r.dMaxDD * 100:+7.3f} "
            f"{r.dCAGR * 100:+7.3f} {r.dSharpe:+8.4f} |  {r.pick4b:6.1%}  {r.pick4b_oos:5.1%}"
            + mark)
    say("  reading: `adm` arms admitted of 17; `E` empty-pool rate (screen admits nothing, the")
    say("  selector falls back to the ungated control); `changed` share of cell-selector rows")
    say("  whose PICK differs from the committed bar's; `chg|live` the same restricted to rows")
    say("  where BOTH bars admitted something; d* are paired OOS deltas vs the committed pick.")

    say("\n### THE QUEUE'S TWO QUESTIONS, answered directly")
    com = P.set_index("point").loc["ABS(1.00)"]
    b15 = P.set_index("point").loc["ABS(1.50)"]
    say(f"  committed ABS(1.00): admits {com.mean_adm:.2f} of 17 arms, empty pool {com.E:.1%}")
    say(f"  (b) ABS(1.50):       admits {b15.mean_adm:.2f} of 17 arms, empty pool {b15.E:.1%}; "
        f"picks change in {b15.changed:.1%} of rows ({int(b15.n_changed)} of {int(com.n)})")
    q_star, tgt, rate_tab = equal_admission_q(cells)
    say(f"  (a) RANK(q): equal-admission q* = {q_star:.2f} (committed admission rate {tgt:.3f}; "
        f"rank-bar rate at q* {rate_tab[q_star]:.3f}) — fixed on IS columns only")
    ra = P.set_index("point").loc[f"RANK({q_star:.2f})"]
    say(f"      RANK({q_star:.2f}): admits {ra.mean_adm:.2f} of 17, empty pool {ra.E:.1%}; "
        f"picks change in {ra.changed:.1%} of rows ({int(ra.n_changed)} of {int(com.n)})")
    say("      rank-bar admission rate by q: "
        + "  ".join(f"{q:.1f}:{rate_tab[q]:.3f}" for q in QS))

    say("\n### THE CONFOUND (idea 163): pooled deltas vs the fallback split")
    say("  point        |  EMPTY-pool moves            |  LIVE-pool moves (both bars admit)")
    for pt in ["ABS(0.50)", "ABS(1.00)", "ABS(1.50)", "ABS(2.00)", f"RANK({q_star:.2f})",
               "RANK(0.30)", "RANK(1.00)", "OFF"]:
        g = S[S.point == pt]
        em = g[(g.pool_empty != g.pool_empty_committed) & (g.changed == 1)]
        lv = g[(~g.pool_empty) & (~g.pool_empty_committed) & (g.changed == 1)]
        say(f"  {pt:11s}  |  {fmt(paired(em.d_OOS_MaxDD)):48s} |  {fmt(paired(lv.d_OOS_MaxDD))}")
    say("  (d OOS MaxDD in pp; positive = shallower drawdown than the committed bar's pick)")

    say("\n### PER SELECTOR — pick changes at the two re-statements")
    say("  selector    ABS(1.50) changed   d MaxDD   d CAGR  |  "
        f"RANK({q_star:.2f}) changed   d MaxDD   d CAGR")
    for sel in SELECTORS:
        a = S[(S.point == "ABS(1.50)") & (S.sel == sel)]
        b = S[(S.point == f"RANK({q_star:.2f})") & (S.sel == sel)]
        say(f"  {sel:10s}  {a.changed.mean():13.1%} {a.d_OOS_MaxDD.mean() * 100:+9.3f} "
            f"{a.d_OOS_CAGR.mean() * 100:+8.3f}  |  {b.changed.mean():14.1%} "
            f"{b.d_OOS_MaxDD.mean() * 100:+9.3f} {b.d_OOS_CAGR.mean() * 100:+8.3f}")

    say("\n### PER PANEL / PER RUNG — ABS(1.50) and RANK(q*) pick-change rates")
    for key in ("panel", "cost"):
        for k, g in S.groupby(key):
            a = g[g.point == "ABS(1.50)"]
            b = g[g.point == f"RANK({q_star:.2f})"]
            say(f"  {key}={str(k):10s} n {len(a):4d}  ABS(1.50) changed {a.changed.mean():6.1%} "
                f"(E {a.pool_empty.mean():5.1%})   RANK changed {b.changed.mean():6.1%} "
                f"(E {b.pool_empty.mean():5.1%})")

    say("\n### RULE 8 (ii) — q* re-derived on the FIRST half of the corpus by parent-file date,")
    say("    the OOS consequence read on the SECOND half untouched")
    dates = sorted({c.date for c in cells})
    cut = dates[-1]
    q_is, tgt_is, _ = equal_admission_q(cells, subset=lambda c: c.date < cut)
    nA = sum(1 for c in cells if c.date < cut)
    say(f"  IS corpus: files dated < {cut} ({nA} cells) -> q* = {q_is:.2f} "
        f"(committed rate {tgt_is:.3f})")
    B = S[S.date >= cut]
    say(f"  OOS corpus: {B.file.nunique()} files, {B[B.point == 'ABS(1.00)'].shape[0]} "
        "cell-selector rows, read once")
    for pt in [f"RANK({q_is:.2f})", "ABS(1.50)"]:
        g = B[B.point == pt]
        say(f"  {pt:11s} on the OOS corpus: changed {g.changed.mean():.1%}   "
            f"d MaxDD {fmt(paired(g.d_OOS_MaxDD))}")
        say(f"              {'':11s} d CAGR {fmt(paired(g.d_OOS_CAGR))}")
        say(f"              {'':11s} d Sharpe {fmt(paired(g.d_OOS_Sharpe), scale=1.0, unit='  ')}")

    # ---------------- Part B
    say("\n\n## PART B — the three forms priced on REAL PRICES (fresh 31-arm menu)\n")
    panels, nbad = load_panels()
    for k, v in panels.items():
        say(f"  panel {k:9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    say(f"  SMALL439 = the sub-$2B panel less the {nbad} names with max 1d move >= 1.0.")
    say("  SURVIVORSHIP: the small panel and universe_broad.json are CURRENT constituents only")
    say("  (data/SMALL_PANEL_README.md) — read the contrasts between forms, not the levels.")
    FG, curves, bench = fresh_grid(panels)
    FG.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"  fresh grid: {len(FG)} arm-rows over {FG.groupby(['panel', 'cost']).ngroups} cells "
        f"(IS through {IS_END}, OOS from {OOS_START}, read once)")

    say("\n### Benchmarks, freshly computed (OOS window)")
    for pn in panels:
        ms, mv = metrics(bench[pn]["SPY"].loc[OOS_START:]), metrics(bench[pn]["V2"].loc[OOS_START:])
        say(f"  {pn:9s} SPY {ms['CAGR']:7.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:7.2%}   "
            f"RULES v2@10bps {mv['CAGR']:7.2%} / {mv['Sharpe']:.4f} / {mv['MaxDD']:7.2%}   "
            f"[4b OOS bars: CAGR >= {0.70 * ms['CAGR']:.2%}, MaxDD >= {0.60 * ms['MaxDD']:.2%}]")

    say("\n### What each DD-leg form picks on fresh prices (selector K_Sharpe, PROTOCOL default)")
    say("  panel/rung   form         adm  pick                    OOS CAGR  Sharpe   MaxDD  "
        "4a 4b 4bOOS")
    prows = []
    for (pn, cst), cell in FG.groupby(["panel", "cost"]):
        spy, v2 = bench[pn]["SPY"], bench[pn]["V2"]
        s_is = win(spy, hi=IS_END)
        s_is = {k[3:] if k.startswith("IS_") else k: v for k, v in s_is.items()}
        for form, p in [("ABS", 1.00), ("ABS", 1.50), ("RANK", q_star), ("OFF", np.nan)]:
            for sel in ["K_Sharpe", "K_CAGR"]:
                i, c, nadm, empty = fresh_screen_row(cell, form, p, sel, s_is)
                a = c.iloc[i]
                r = curves[(pn, cst, a.arm)]
                prows.append(dict(panel=pn, cost=cst, form=form, param=p, sel=sel,
                                  n_admitted=nadm, empty=empty, arm=a.arm,
                                  OOS_CAGR=a.OOS_CAGR, OOS_Sharpe=a.OOS_Sharpe,
                                  OOS_MaxDD=a.OOS_MaxDD, **keep_paths(r, spy, v2)))
                if sel == "K_Sharpe":
                    pt = f"{form}({p:.2f})" if form != "OFF" else "OFF"
                    say(f"  {pn:9s}@{cst:<3.0f} {pt:11s} {nadm:4d}  {a.arm:20s} "
                        f"{a.OOS_CAGR:8.2%} {a.OOS_Sharpe:7.4f} {a.OOS_MaxDD:7.2%}  "
                        f"{'Y' if prows[-1]['pass4a'] else '.'}  "
                        f"{'Y' if prows[-1]['pass4b'] else '.'}  "
                        f"{'Y' if prows[-1]['pass4b_oos'] else '.'}")
    PK = pd.DataFrame(prows)
    PK.to_csv(OUT / f"{STEM}.picks.csv", index=False)

    say("\n### Fresh-price summary: does the DD leg's FORM change the answer?")
    for sel in ["K_Sharpe", "K_CAGR"]:
        g = PK[PK.sel == sel]
        ref = g[(g.form == "ABS") & (g.param == 1.00)].set_index(["panel", "cost"])
        say(f"  selector {sel}")
        for form, p in [("ABS", 1.50), ("RANK", q_star), ("OFF", np.nan)]:
            h = g[(g.form == form) & ((g.param == p) if form != "OFF" else True)] \
                .set_index(["panel", "cost"])
            chg = int((h.arm != ref.arm).sum())
            say(f"    {form}({p:.2f})" .ljust(16) + f"picks differ in {chg} of {len(ref)} cells; "
                f"mean OOS CAGR {h.OOS_CAGR.mean():7.2%} (ref {ref.OOS_CAGR.mean():7.2%}), "
                f"Sharpe {h.OOS_Sharpe.mean():.4f} (ref {ref.OOS_Sharpe.mean():.4f}), "
                f"MaxDD {h.OOS_MaxDD.mean():7.2%} (ref {ref.OOS_MaxDD.mean():7.2%}); "
                f"4b {int(h.pass4b.sum())}/{len(h)} 4bOOS {int(h.pass4b_oos.sum())}/{len(h)} "
                f"(ref {int(ref.pass4b.sum())}/{int(ref.pass4b_oos.sum())})")

    say("\n### KEEP paths over the whole fresh menu (all 186 arm-rows, both windows)")
    say(f"  4a(v2) full {int(FG.pass4a.sum())}/{len(FG)}   4b full {int(FG.pass4b.sum())}/{len(FG)}"
        f"   4a OOS {int(FG.pass4a_oos.sum())}/{len(FG)}   4b OOS {int(FG.pass4b_oos.sum())}/{len(FG)}"
        f"   BOTH(4a&4b full) {int((FG.pass4a & FG.pass4b).sum())}/{len(FG)}")
    both = FG[FG.pass4b & FG.pass4b_oos]
    say(f"  arms clearing 4b on BOTH windows: {len(both)}")
    if len(both):
        say(both.sort_values("OOS_Sharpe", ascending=False)
            [["panel", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe",
              "OOS_MaxDD"]].head(8).to_string(index=False,
                                              float_format=lambda x: f"{x:.4f}"))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    say(f"\nwrote {STEM}.console.txt / .points.csv / .sweep.csv.gz / .grid.csv / .picks.csv")


if __name__ == "__main__":
    main()
