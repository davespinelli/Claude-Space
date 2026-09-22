#!/usr/bin/env python3
"""Idea 950 -- is-the-BAND-BOOK-s-ONLY-95th-PERCENTILE-CELL-a-DE-GROSSING-artefact  (lane B, 2026-09-22)

THE CLAIM UNDER TEST
  Idea 945 priced five turnover dials against a GROSS-MATCHED coin-flip null.  Exactly one of its
  15 (panel x dial) cells cleared the 95th percentile at 10 bps: SMALL / D5_BAND (band 0.00->0.06),
  book gain +0.1006 of Sharpe against a null median of -0.0115, percentile 100.0 at 250 draws.
  945's null matches the book's TARGET gross at each rebalance -- k(t) names drawn uniformly from
  P(t), each at the book's own per-name weight w(t) = 1/N_priced(t).  But the BAND book is the one
  family in 945 that DE-GROSSES: gated-out weight goes to CASH and is never re-spread, so its
  median REALISED gross is 0.4286 against a target of 0.75, and widening the band MOVES that
  realised exposure.  945's own G6 failed on exactly this.  So the +0.1006 may be an exposure
  difference the null was never given, not a name-selection edge.

WHAT THIS RUN DOES  (max 2 tuned parameters, ALL grid points reported)
  P1  gross-match rule in {TARGET, REALISED}
        TARGET   -- 945's null, verbatim (same seeds, same stream, reproduction gated at G5).
        REALISED -- the SAME draw, then a daily exposure overlay lambda(t) = G_book(t)/G_null(t)
                    so the null carries the book's DRIFTED gross on every row.  lambda(t) is a
                    function of Cp (cumulative returns through t-1) only, so it is predetermined
                    at the open of row t -- no look-ahead.  Turnover is scaled by lambda at the
                    rebalance row so the levered null pays for the exposure it carries.
                    After the overlay the ONLY difference between book and null is WHICH NAMES.
  P2  band ladder b in {0.00, 0.02, 0.03, 0.04, 0.06, 0.08}; every rung is priced against
        b = 0.00 as the high-turnover side A, so D5_BAND (0.00->0.06) is one row of the ladder.

  Reported at every cost rung 0 / 10 / 25 / 50 bps, on SMALL (945's cell) and U56 (robustness).

PROTOCOL DELIVERABLES (rules 2, 3, 4, 8)
  The BAND book IS the live book form: rules_v2_weights(px, band=b, gross=0.75), weekly, 10 bps,
  weights at close t applied t+1.  Every rung is scored with baseline.compare() against RULES v2
  (live), RULES v1 and SPY; 4a and 4b are read on FULL / H1 / H2 / IS / OOS; rule 8 chooses the
  band on 2009-2016 alone and reads 2017-2026 once.

GATES
  G1  the BAND book built here == baseline.rules_v2_weights(px, b, 0.75) exactly
  G2  the TARGET null's target gross / holding count / per-name weight == the book's, every row
  G3  the REALISED null's drifted gross == the book's drifted gross, every row (the overlay works)
  G4  determinism: same seed -> same null series bit-for-bit
  G5  reproduction of 945's committed SMALL/D5_BAND cell at 10 bps

SURVIVORSHIP (rule 9): SMALL is a current-constituent screen (data/SMALL_PANEL_README.md) and U56
is a current-constituent list, so every absolute level is optimistic.  The book-vs-null contrast is
within-tape (same names, same dates, same exposure path) and does not repair the level.
"""
import sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, compare  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST0, LAG, WARMUP = 10.0, 1, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COSTS = [0.0, 10.0, 25.0, 50.0]
NDRAW, HALF, SEED0 = 250, 125, 20260915     # 945's draw count and seed
GROSS0 = 0.75
BANDS = [0.00, 0.02, 0.03, 0.04, 0.06, 0.08]
BASE_BAND = 0.00                            # side A of every dial row (945's D5_BAND side A)
EDGE_PCTL_BAR = 95.0
PANELS = ["SMALL", "U56"]
# 945's SETTINGS index for the two bands it priced, so the TARGET null reproduces bit-for-bit.
SI_945 = {0.00: 4, 0.06: 5}
SI_NEW = {0.02: 6, 0.03: 7, 0.04: 8, 0.08: 9}
PANEL_SI_945 = {"U56": 0, "B136": 1, "SMALL": 2}     # 945's PANELS order
# 945's committed SMALL/D5_BAND cell at 10 bps
PUB945 = dict(book_gain=0.1006, null_gain_median=-0.0115, pctl=100.0, med_realised_gross=0.4286)
TOL945 = 0.004

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"    wrote {p.name}  ({len(df):,} rows)")


# ================================================================================================
class Panel:
    def __init__(self, name, px, freq="W"):
        self.name, self.px, self.freq = name, px, freq
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = rebalance_mask(self.idx, freq).shift(LAG, fill_value=False).values.copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.dec = np.maximum(self.reb - LAG, 0)
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        m_full = np.asarray(self.idx >= self.idx[WARMUP])
        fp = np.flatnonzero(m_full); h = len(fp) // 2
        m1 = np.zeros(T, bool); m1[fp[:h]] = True
        m2 = np.zeros(T, bool); m2[fp[h:]] = True
        self.masks = {"FULL": m_full, "H1": m1, "H2": m2,
                      "IS": m_full & np.asarray(self.idx <= pd.Timestamp(IS_END)),
                      "OOS": np.asarray(self.idx >= pd.Timestamp(OOS_START))}
        self.spy = px["SPY"].pct_change().fillna(0.0).values


class Book:
    """A gross-1.0 weights matrix priced on a Panel (945's Book, verbatim + a gross accessor)."""

    def __init__(self, panel: Panel, W1: np.ndarray):
        self.pan = panel
        wt = np.roll(W1, LAG, axis=0).copy(); wt[:LAG] = 0.0
        self.wt_reb = wt[panel.reb]
        A = wt[panel.s0]; AR = A * panel.R
        self.S = AR.sum(axis=1); self.As = A.sum(axis=1)
        self.ARr = (AR * panel.rets).sum(axis=1)
        Ap = wt[panel.s0p[panel.reb]]
        self.ARp = Ap * panel.Rp
        self.Sp = self.ARp.sum(axis=1); self.Asp = Ap.sum(axis=1)

    def parts(self, g=GROSS0):
        """(daily gross return, turnover-at-reb, realised drifted gross) -- all predetermined."""
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gret = g * self.ARr / V
        gross = g * self.S / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]; heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gret, turn, gross

    def at(self, g=GROSS0, cost=COST0):
        gret, turn, _ = self.parts(g)
        return gret - turn * cost / 1e4, turn

    def target_gross_at_reb(self, g=GROSS0):
        return g * self.wt_reb.sum(axis=1)


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 3 or not np.isfinite(r).all():
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return np.nan
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def pack(r, pan):
    c, s, d = fmet(np.asarray(r)[pan.masks["FULL"]])
    co, so, do = fmet(np.asarray(r)[pan.masks["OOS"]])
    ci, si_, di = fmet(np.asarray(r)[pan.masks["IS"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=d,
                H1=fsharpe(np.asarray(r)[pan.masks["H1"]]),
                H2=fsharpe(np.asarray(r)[pan.masks["H2"]]),
                IS_Sharpe=si_, IS_CAGR=ci, IS_MaxDD=di,
                oCAGR=co, oSharpe=so, oMaxDD=do)


def legs4b(s, spy):
    L = dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]),
             L3_OOS=bool(s["oSharpe"] > spy["oSharpe"]),
             L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
             L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    L["pass4b"] = bool(all(L.values()))
    return L


def legs4b_oos(s, spy):
    """4b read on the OOS window alone (rule 8): Sharpe > SPY, DD cap, CAGR floor, all OOS."""
    return dict(O_Sharpe=bool(s["oSharpe"] > spy["oSharpe"]),
                O_DDcap=bool(s["oMaxDD"] >= DD_CAP * spy["oMaxDD"]),
                O_CAGRfloor=bool(s["oCAGR"] >= CAGR_FLOOR * spy["oCAGR"]))


# ------------------------------------------------------------------------------ the BAND setting
def build_band(px, bd):
    """945's BAND setting: (W1, pool, k(t), per-name weight w(t))."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    npr = e.sum(axis=1).replace(0, np.nan)
    ew = e.div(npr, axis=0).fillna(0.0)
    inb = band_state(px, bd) & px.notna()
    W1 = ew.where(inb, 0.0).values
    return W1, (px.notna()).values, inb.sum(axis=1).values.astype(int), (1.0 / npr).fillna(0.0).values


def null_w1(pool, kc, wpn, dec, rng):
    """945's gross-matched coin flip, verbatim."""
    T, N = pool.shape
    W = np.zeros((T, N))
    for t in dec:
        k = int(kc[t])
        if k <= 0 or wpn[t] <= 0:
            continue
        idx = np.flatnonzero(pool[t])
        if len(idx) == 0:
            continue
        W[t, rng.choice(idx, size=min(k, len(idx)), replace=False)] = wpn[t]
    return W


def overlay(gret_n, turn_n, gross_n, gross_b, reb):
    """REALISED-gross match: carry the BOOK's drifted gross on every row."""
    lam = np.zeros_like(gross_n)
    ok = np.abs(gross_n) > 1e-9
    lam[ok] = gross_b[ok] / gross_n[ok]
    return gret_n * lam, turn_n * lam, gross_n * lam, lam


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 950 -- is the BAND book's only 95th-percentile cell a DE-GROSSING artefact?")
    P("lane B, 2026-09-22.  P1 = gross-match rule {TARGET, REALISED}; P2 = band ladder.")
    P("=" * 100)

    panels, ctx = {}, {}
    for pn in PANELS:
        px = load_universe(small=True) if pn == "SMALL" else load_universe()
        pan = Panel(pn, px, "W")
        panels[pn] = pan
        P(f"  {pn}: {pan.px.shape[1]} cols x {pan.T} rows, {pan.idx[0].date()}..{pan.idx[-1].date()}, "
          f"{len(pan.reb)} weekly rebalances")
        for b in BANDS:
            W1, pool, kc, wpn = build_band(pan.px, b)
            ctx[(pn, b)] = dict(pan=pan, bk=Book(pan, W1), pool=pool, kc=kc, wpn=wpn, W1=W1)

    # ------------------------------------------------------------------------------------ GATES
    P("\n" + "-" * 100); P("GATES"); P("-" * 100)
    gates = []

    d1 = 0.0
    for pn in PANELS:
        for b in BANDS:
            mine = pd.DataFrame(ctx[(pn, b)]["W1"] * GROSS0, index=panels[pn].idx,
                                columns=panels[pn].px.columns)
            theirs = rules_v2_weights(panels[pn].px, band=b, gross=GROSS0)
            d1 = max(d1, float(np.nanmax(np.abs(mine.values - theirs.values))))
    gates.append(dict(gate="G1 BAND book == baseline.rules_v2_weights(px,b,0.75)",
                      stat=f"max|dw| {d1:.3e}", bar="< 1e-12", passed=bool(d1 < 1e-12)))

    d2g, d2k, d2w = [], [], []
    for pn in PANELS:
        for b in BANDS:
            c = ctx[(pn, b)]; pan = c["pan"]
            NW = null_w1(c["pool"], c["kc"], c["wpn"], pan.dec, np.random.default_rng(7))
            nbk = Book(pan, NW)
            d2g.append(float(np.max(np.abs(nbk.target_gross_at_reb() - c["bk"].target_gross_at_reb()))))
            d2k.append(int(np.max(np.abs((NW[pan.dec] > 0).sum(1) - (c["W1"][pan.dec] > 0).sum(1)))))
            nz = NW[pan.dec][NW[pan.dec] > 0]
            d2w.append(float(np.max(np.abs(nz - np.repeat(c["wpn"][pan.dec],
                                                          (NW[pan.dec] > 0).sum(1))))) if nz.size else 0.0)
    gates.append(dict(gate="G2 TARGET null's gross / count / per-name weight == book's",
                      stat=f"max|dgross| {max(d2g):.3e}, max|dcount| {max(d2k)}, max|dw| {max(d2w):.3e}",
                      bar="all ~ 0", passed=bool(max(d2g) < 1e-12 and max(d2k) == 0 and max(d2w) < 1e-12)))

    d3 = 0.0
    for pn in PANELS:
        for b in BANDS:
            c = ctx[(pn, b)]; pan = c["pan"]
            _, _, gb = c["bk"].parts()
            nbk = Book(pan, null_w1(c["pool"], c["kc"], c["wpn"], pan.dec, np.random.default_rng(11)))
            gn_, tn_, gg_ = nbk.parts()
            _, _, gm, _ = overlay(gn_, tn_, gg_, gb, pan.reb)
            m = np.abs(gg_) > 1e-9
            d3 = max(d3, float(np.max(np.abs(gm[m] - gb[m]))))
    gates.append(dict(gate="G3 REALISED null's drifted gross == book's drifted gross",
                      stat=f"max|dG| {d3:.3e}", bar="< 1e-10", passed=bool(d3 < 1e-10)))

    c = ctx[("SMALL", 0.06)]
    ra, _ = Book(c["pan"], null_w1(c["pool"], c["kc"], c["wpn"], c["pan"].dec,
                                   np.random.default_rng((SEED0, 2, 5, 3)))).at()
    rb, _ = Book(c["pan"], null_w1(c["pool"], c["kc"], c["wpn"], c["pan"].dec,
                                   np.random.default_rng((SEED0, 2, 5, 3)))).at()
    d4 = float(np.max(np.abs(ra - rb)))
    gates.append(dict(gate="G4 determinism (same seed -> same null)", stat=f"max|d| {d4:.3e}",
                      bar="== 0", passed=bool(d4 == 0.0)))

    for g in gates:
        P(f"  [{'PASS' if g['passed'] else 'FAIL'}] {g['gate']}\n         {g['stat']}   (bar {g['bar']})")

    # ------------------------------------------------------- the realised-gross fact that motivates
    P("\n" + "-" * 100)
    P("THE MOTIVATING FACT -- the BAND book DE-GROSSES, and the band dial MOVES the exposure")
    P("-" * 100)
    P(f"  {'panel':<6} {'band':>5} {'med realised gross':>19} {'mean realised gross':>20} "
      f"{'med target gross':>17} {'ann turnover':>13}")
    rg = []
    for pn in PANELS:
        for b in BANDS:
            c = ctx[(pn, b)]; pan = c["pan"]
            _, turn, gb = c["bk"].parts()
            m = pan.masks["FULL"]
            row = dict(panel=pn, band=b, med_realised_gross=float(np.median(gb[m])),
                       mean_realised_gross=float(np.mean(gb[m])),
                       med_target_gross=float(np.median(c["bk"].target_gross_at_reb())),
                       ann_turn=float(turn[m].sum() / (m.sum() / 252.0)))
            rg.append(row)
            P(f"  {pn:<6} {b:>5.2f} {row['med_realised_gross']:>19.4f} "
              f"{row['mean_realised_gross']:>20.4f} {row['med_target_gross']:>17.4f} "
              f"{row['ann_turn']:>13.2f}")
    rgd = pd.DataFrame(rg); dump(rgd, "grossprofile.csv")
    s945 = rgd[(rgd.panel == "SMALL") & (rgd.band == 0.00)].iloc[0].med_realised_gross
    P(f"\n  945 published SMALL BAND median realised gross {PUB945['med_realised_gross']:.4f}; "
      f"here (band 0.00) {s945:.4f}  -> d {s945 - PUB945['med_realised_gross']:+.4f}")

    # ------------------------------------------------------------------------------- THE BOOKS
    P("\n" + "-" * 100)
    P("THE BOOKS -- every band rung, every cost rung (weights at close t applied t+1, no shorting)")
    P("-" * 100)
    brows = []
    for pn in PANELS:
        pan = panels[pn]
        spy = pack(pan.spy, pan)
        for b in BANDS:
            for cost in COSTS:
                r, turn = ctx[(pn, b)]["bk"].at(GROSS0, cost)
                m = pack(r, pan)
                brows.append(dict(panel=pn, band=b, cost_bps=cost, **m,
                                  ann_turn=float(turn[pan.masks["FULL"]].sum() /
                                                 (pan.masks["FULL"].sum() / 252.0)),
                                  **legs4b(m, spy), **legs4b_oos(m, spy)))
    bk = pd.DataFrame(brows); dump(bk, "books.csv")
    P(f"  {'panel':<6} {'band':>5} {'cost':>5} {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} "
      f"{'H1':>6} {'H2':>6} {'IS_Sh':>6} {'oSh':>6} {'turn':>7} {'4b':>5}")
    for _, r in bk.iterrows():
        P(f"  {r.panel:<6} {r.band:>5.2f} {r.cost_bps:>5.0f} {r.CAGR:>7.4f} {r.Sharpe:>7.4f} "
          f"{r.MaxDD:>8.4f} {r.H1:>6.3f} {r.H2:>6.3f} {r.IS_Sharpe:>6.3f} {r.oSharpe:>6.3f} "
          f"{r.ann_turn:>7.2f} {str(bool(r.pass4b)):>5}")

    # -------------------------------------------------------------------------------- THE NULLS
    P("\n" + "-" * 100)
    P(f"THE NULLS -- {NDRAW} draws per (panel, band), each scored TWICE: 945's TARGET-gross match")
    P("and this run's REALISED-gross match (same draw, exposure overlay).  P1 is the only thing")
    P("that changes between the two readings of one draw.")
    P("-" * 100)
    nrows = []
    for pn in PANELS:
        pan = panels[pn]
        for b in BANDS:
            c = ctx[(pn, b)]
            _, _, gb = c["bk"].parts()
            si = SI_945.get(b, SI_NEW.get(b))
            for s in range(NDRAW):
                rng = np.random.default_rng((SEED0, PANEL_SI_945[pn], si, s))
                nbk = Book(pan, null_w1(c["pool"], c["kc"], c["wpn"], pan.dec, rng))
                gn_, tn_, gg_ = nbk.parts()
                gm_, tm_, gmm, lam = overlay(gn_, tn_, gg_, gb, pan.reb)
                for kind, (gr, tu, gx) in (("TARGET", (gn_, tn_, gg_)),
                                           ("REALISED", (gm_, tm_, gmm))):
                    for cost in COSTS:
                        r = gr - tu * cost / 1e4
                        mm = pack(r, pan)
                        nrows.append(dict(panel=pn, band=b, match=kind, seed=s, cost_bps=cost,
                                          Sharpe=mm["Sharpe"], CAGR=mm["CAGR"], MaxDD=mm["MaxDD"],
                                          oSharpe=mm["oSharpe"],
                                          med_gross=float(np.median(gx[pan.masks["FULL"]])),
                                          ann_turn=float(tu[pan.masks["FULL"]].sum() /
                                                         (pan.masks["FULL"].sum() / 252.0))))
            P(f"    {pn}/band {b:.2f}: {NDRAW} draws x 2 match rules done  ({time.time()-t0:.0f}s)")
    nl = pd.DataFrame(nrows)
    nl.to_csv(OUT / f"{STEM}.nulls.csv.gz", index=False)
    P(f"    wrote {STEM}.nulls.csv.gz  ({len(nl):,} rows)")

    # ------------------------------------------------------------------------- THE ANSWER TABLE
    P("\n" + "=" * 100)
    P("THE ANSWER -- the band dial's BOOK gain against its own null's gain, both match rules")
    P("(side A = band 0.00 everywhere; D5_BAND is the b = 0.06 row)")
    P("=" * 100)
    grows = []
    for pn in PANELS:
        for b in BANDS:
            if b == BASE_BAND:
                continue
            for kind in ("TARGET", "REALISED"):
                for cost in COSTS:
                    ba = bk[(bk.panel == pn) & (bk.band == BASE_BAND) & (bk.cost_bps == cost)].iloc[0]
                    bb = bk[(bk.panel == pn) & (bk.band == b) & (bk.cost_bps == cost)].iloc[0]
                    d_book = bb.Sharpe - ba.Sharpe
                    na = nl[(nl.panel == pn) & (nl.band == BASE_BAND) & (nl.match == kind) &
                            (nl.cost_bps == cost)].set_index("seed").Sharpe
                    nb_ = nl[(nl.panel == pn) & (nl.band == b) & (nl.match == kind) &
                             (nl.cost_bps == cost)].set_index("seed").Sharpe
                    d_null = (nb_ - na).dropna().values
                    pct = float((d_null < d_book).mean() * 100.0)
                    ga = float(rgd[(rgd.panel == pn) & (rgd.band == BASE_BAND)].iloc[0]
                               .med_realised_gross)
                    gbn = float(rgd[(rgd.panel == pn) & (rgd.band == b)].iloc[0].med_realised_gross)
                    nga = float(nl[(nl.panel == pn) & (nl.band == BASE_BAND) & (nl.match == kind) &
                                   (nl.cost_bps == cost)].med_gross.median())
                    ngb = float(nl[(nl.panel == pn) & (nl.band == b) & (nl.match == kind) &
                                   (nl.cost_bps == cost)].med_gross.median())
                    grows.append(dict(panel=pn, band_A=BASE_BAND, band_B=b, match=kind,
                                      cost_bps=cost, book_A=ba.Sharpe, book_B=bb.Sharpe,
                                      book_gain=d_book,
                                      null_gain_median=float(np.median(d_null)),
                                      null_gain_p95=float(np.percentile(d_null, 95)),
                                      null_gain_sd=float(np.std(d_null, ddof=1)),
                                      book_pctl_in_null=pct,
                                      pctl_half=float((d_null[:HALF] < d_book).mean() * 100.0),
                                      excess=d_book - float(np.median(d_null)),
                                      clears95=bool(pct >= EDGE_PCTL_BAR), n_draws=len(d_null),
                                      book_gross_A=ga, book_gross_B=gbn,
                                      book_dGross=gbn - ga,
                                      null_gross_A=nga, null_gross_B=ngb,
                                      null_dGross=ngb - nga,
                                      gross_mismatch_A=nga - ga, gross_mismatch_B=ngb - gbn))
    gn = pd.DataFrame(grows); dump(gn, "gain.csv")
    P(f"  {'panel':<6} {'dial':>14} {'match':>9} {'cost':>5} {'book gain':>10} {'null med':>9} "
      f"{'null p95':>9} {'pctl':>7} {'pctl/2':>7} {'excess':>9} {'>=95':>5} "
      f"{'bk dGross':>10} {'nl dGross':>10} {'mismatchB':>10}")
    for _, r in gn.iterrows():
        P(f"  {r.panel:<6} {f'{r.band_A:.2f}->{r.band_B:.2f}':>14} {r.match:>9} {r.cost_bps:>5.0f} "
          f"{r.book_gain:>10.4f} {r.null_gain_median:>9.4f} {r.null_gain_p95:>9.4f} "
          f"{r.book_pctl_in_null:>7.1f} {r.pctl_half:>7.1f} {r.excess:>9.4f} "
          f"{str(bool(r.clears95)):>5} {r.book_dGross:>10.4f} {r.null_dGross:>10.4f} "
          f"{r.gross_mismatch_B:>10.4f}")
    P("\n  TARGET vs REALISED, side by side -- what the exposure overlay is worth, per rung")
    P(f"  {'panel':<6} {'dial':>14} {'cost':>5} {'pctl TARGET':>12} {'pctl REALISED':>14} "
      f"{'d null med':>11} {'d excess':>10}")
    for pn in PANELS:
        for b in BANDS:
            if b == BASE_BAND:
                continue
            for cost in COSTS:
                t_ = gn[(gn.panel == pn) & (gn.band_B == b) & (gn.match == "TARGET") &
                        (gn.cost_bps == cost)].iloc[0]
                r_ = gn[(gn.panel == pn) & (gn.band_B == b) & (gn.match == "REALISED") &
                        (gn.cost_bps == cost)].iloc[0]
                P(f"  {pn:<6} {f'{BASE_BAND:.2f}->{b:.2f}':>14} {cost:>5.0f} "
                  f"{t_.book_pctl_in_null:>12.1f} {r_.book_pctl_in_null:>14.1f} "
                  f"{r_.null_gain_median - t_.null_gain_median:>11.4f} "
                  f"{r_.excess - t_.excess:>10.4f}")

    # G5 reproduction of 945
    rep = gn[(gn.panel == "SMALL") & (gn.band_B == 0.06) & (gn.match == "TARGET") &
             (gn.cost_bps == 10.0)].iloc[0]
    dg = abs(rep.book_gain - PUB945["book_gain"]); dn = abs(rep.null_gain_median - PUB945["null_gain_median"])
    g5a = bool(rep.book_gain > 0 and rep.null_gain_median < rep.book_gain and
               rep.book_pctl_in_null >= 99.0)
    g5b = bool(dg < TOL945 and dn < TOL945)
    gates.append(dict(gate="G5a reproduces 945's SMALL/D5_BAND DIRECTION and PERCENTILE at 10 bps",
                      stat=f"book gain {rep.book_gain:+.4f} > null med {rep.null_gain_median:+.4f}; "
                           f"pctl {rep.book_pctl_in_null:.1f} vs 945's {PUB945['pctl']:.1f}",
                      bar="gain > null median and pctl >= 99", passed=g5a))
    gates.append(dict(gate="G5b reproduces 945's SMALL/D5_BAND LEVELS at 10 bps",
                      stat=f"book gain {rep.book_gain:+.4f} vs {PUB945['book_gain']:+.4f} (d {dg:.4f}); "
                           f"null med {rep.null_gain_median:+.4f} vs {PUB945['null_gain_median']:+.4f} "
                           f"(d {dn:.4f}).  TAPE VINTAGE: 945 ran 2026-09-15, this tape ends "
                           f"{panels['SMALL'].idx[-1].date()} and the SMALL cache was rebuilt "
                           f"2026-09-22, so the book leg (which carries NO draw noise) cannot be "
                           f"expected to match to the last basis point.",
                      bar=f"|d| < {TOL945}", passed=g5b))
    for g in gates[-2:]:
        P(f"\n  [{'PASS' if g['passed'] else 'FAIL'}] {g['gate']}\n         {g['stat']}")
    dump(pd.DataFrame(gates), "gates.csv")

    # ----------------------------------------------------------------- 4a / 4b AND compare(), rule 8
    P("\n" + "=" * 100)
    P("PROTOCOL 3 / 4 -- every band rung against RULES v2 (live), RULES v1 and SPY, 10 bps weekly")
    P("=" * 100)
    lb = []
    for pn in PANELS:
        px = panels[pn].px
        for b in BANDS:
            P(f"\n  --- {pn}  band {b:.2f}  (gross {GROSS0}) ---")
            res = compare(f"950 BAND b={b:.2f} g={GROSS0:.2f} [{pn}]",
                          lambda p, _b=b: rules_v2_weights(p, band=_b, gross=GROSS0),
                          px, freq="W", cost_bps=10, baseline_freq="W")
            lb.append(dict(panel=pn, band=b, verdict4a=res["verdict"], row=res["row"]))
    P("\n  4a (beat the book) verdicts: " +
      ", ".join(f"{d['panel']}/b{d['band']:.2f}={d['verdict4a']}" for d in lb))

    P("\n" + "-" * 100)
    P("4b legs at 10 bps (FULL-window legs vs SPY, then the OOS-only read)")
    P("-" * 100)
    for pn in PANELS:
        spy = pack(panels[pn].spy, panels[pn])
        P(f"  {pn}: SPY FULL CAGR {spy['CAGR']:.4f} Sharpe {spy['Sharpe']:.4f} MaxDD {spy['MaxDD']:.4f} "
          f"| H1 {spy['H1']:.3f} H2 {spy['H2']:.3f} | OOS {spy['oCAGR']:.4f}/{spy['oSharpe']:.4f}/"
          f"{spy['oMaxDD']:.4f}")
        for _, r in bk[(bk.panel == pn) & (bk.cost_bps == 10.0)].iterrows():
            P(f"    b {r.band:>4.2f}  L1 {str(bool(r.L1_H1)):>5} L2 {str(bool(r.L2_H2)):>5} "
              f"L3 {str(bool(r.L3_OOS)):>5} L4 {str(bool(r.L4_DDcap)):>5} "
              f"L5 {str(bool(r.L5_CAGRfloor)):>5} -> 4b {str(bool(r.pass4b)):>5}   "
              f"| OOS-only: Sh {str(bool(r.O_Sharpe)):>5} DD {str(bool(r.O_DDcap)):>5} "
              f"CAGR {str(bool(r.O_CAGRfloor)):>5}")

    # ---------------------------------------------------------------------- RULE 8 WALK-FORWARD
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD -- band chosen on 2009-2016 IS Sharpe alone, 2017-2026 read ONCE")
    P("=" * 100)
    wf = []
    for pn in PANELS:
        pan = panels[pn]
        spy = pack(pan.spy, pan)
        cand = bk[(bk.panel == pn) & (bk.cost_bps == 10.0)]
        pick = cand.loc[cand.IS_Sharpe.idxmax()]
        base_r = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=10, freq="W")["returns"]
        base = pack(base_r.reindex(pan.idx).fillna(0.0).values, pan)
        P(f"\n  {pn}: IS argmax band = {pick.band:.2f} (IS Sharpe {pick.IS_Sharpe:.4f}); "
          f"IS ranking " + " ".join(f"b{r.band:.2f}:{r.IS_Sharpe:.3f}" for _, r in cand.iterrows()))
        P(f"    {'series':<26} {'OOS CAGR':>9} {'OOS Sharpe':>11} {'OOS MaxDD':>10}")
        for nm, m in (("950 pick b=%.2f" % pick.band, pick), ("RULES v2 baseline (live)", base),
                      ("SPY", spy)):
            P(f"    {nm:<26} {m['oCAGR']:>9.4f} {m['oSharpe']:>11.4f} {m['oMaxDD']:>10.4f}")
        o4b = legs4b_oos(pick, spy)
        o4b_base = legs4b_oos(base, spy)
        P(f"    OOS 4b legs (pick): " + " ".join(f"{k}={v}" for k, v in o4b.items()) +
          f"  -> {'PASS' if all(o4b.values()) else 'FAIL'}")
        P(f"    OOS 4b legs (RULES v2): " + " ".join(f"{k}={v}" for k, v in o4b_base.items()) +
          f"  -> {'PASS' if all(o4b_base.values()) else 'FAIL'}")
        P(f"    4a OOS (pick vs live book): Sharpe {pick.oSharpe:.4f} vs {base['oSharpe']:.4f}, "
          f"MaxDD {pick.oMaxDD:.4f} vs {base['oMaxDD']:.4f}")
        wf.append(dict(panel=pn, pick_band=float(pick.band), IS_Sharpe=float(pick.IS_Sharpe),
                       oCAGR=float(pick.oCAGR), oSharpe=float(pick.oSharpe), oMaxDD=float(pick.oMaxDD),
                       base_oCAGR=base["oCAGR"], base_oSharpe=base["oSharpe"], base_oMaxDD=base["oMaxDD"],
                       spy_oCAGR=spy["oCAGR"], spy_oSharpe=spy["oSharpe"], spy_oMaxDD=spy["oMaxDD"],
                       pass4b_oos=bool(all(o4b.values())),
                       pass4b_full=bool(bk[(bk.panel == pn) & (bk.band == pick.band) &
                                           (bk.cost_bps == 10.0)].iloc[0].pass4b)))
    dump(pd.DataFrame(wf), "walkforward.csv")

    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG), encoding="utf-8")
    P(f"\n  done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
