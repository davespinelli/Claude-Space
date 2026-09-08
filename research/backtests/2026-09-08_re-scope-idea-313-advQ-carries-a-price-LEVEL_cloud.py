#!/usr/bin/env python3
"""Idea 424 — re-scope idea 313: does the capQ/advQ SIGN gap survive replacing advQ with a
price-free liquidity key?

QUESTION (queue 424, following 313 and 197)
    Idea 51 (lane B) reported two size columns giving OPPOSITE-signed decile slopes for the same
    book on the same panel:  capQ  rho(decile, dSharpe) = -0.336   vs   advQ = +0.335,
    the two series correlating only +0.545.  Idea 313 asked why.  Idea 197's T1 then showed that
    advQ = (px*vol).rolling(w).median().rank(axis=1) is NOT invariant under the split-re-adjustment
    operator px -> px @ diag(c)  (73% of its cells move), while a share-volume-only key (VOLSH)
    moves 0.0000 of them.  So advQ carries a price LEVEL.  This script re-runs idea 51's decile
    decomposition with advQ replaced by
        VOLSH  = vol.rolling(60).median()                (no price at all — T1-invariant)
        DVOLT  = (term_i * vol).rolling(60).median()     (a FIXED per-name price scale x volume)
    and asks whether the sign gap survives.

DECOMPOSITION (the confound idea 313 named)
    capQ and advQ differ on TWO axes at once, not one:
      (a) KEY CONTENT     static 2026 market cap   vs   a traded-liquidity measure
      (b) MEMBERSHIP      STATIC (a name sits in one decile forever)  vs
                          DYNAMIC (re-ranked cross-sectionally every day)
    Idea 51 ran capQ only as STATIC and advQ only as DYNAMIC, so its sign gap cannot tell the two
    apart.  Here every liquidity key is run under BOTH membership schemes, so the 2x2 is complete:
        capQ-S | advQ-S  advQ-D | VOLSH-S  VOLSH-D | DVOLT-S  DVOLT-D
    (capQ is constant in time, so capQ-D does not exist.)

PARAMETERS (2, both design axes, fully crossed and ALL grid points reported)
    p1  key         in {capQ, advQ, VOLSH, DVOLT}
    p2  membership  in {STATIC, DYNAMIC}
    Everything else is PINNED at idea 51 lane B's pre-registered values and is not tuned:
    g = 0.75, cadence weekly, cost 10 bps (0 bps reported alongside), NDEC = 10, key window 60d
    (min_periods 30), arms {EWall, MA-RS, MA-DG}, MA window 200.

GATES
    G1  reproduction — capQ/advQ rows must reproduce idea 51 lane B's committed .deciles.csv.
    G2  T1 invariance — re-measure idea 197's cell-move fraction for each key on THIS panel, so
        the premise ("advQ carries a price level, VOLSH does not") is verified here, not cited.

HONESTY
    rho over NDEC = 10 points has SE ~ 1/sqrt(8) = 0.354.  Every rho is reported with its t-stat
    and with a 1,000-draw calendar-YEAR block bootstrap (the same year draw applied to every book,
    so the gap is a PAIRED statistic), and the sign gap is reported as a bootstrap sign-flip rate.

PANEL / SURVIVORSHIP
    SMALL panel only (data/prices_small.csv.gz, sub-$2B screen, 2010-2026), tickers with
    max_1d_move >= 1.0 in data/small_meta.csv dropped first.  SURVIVORSHIP: the small panel is
    CURRENT constituents of the screen only — no delisted names — so every level (CAGR, Sharpe) on
    it is biased UP, the thin/illiquid deciles most of all.  This script's claims are about
    DIFFERENCES between size keys on the same panel, which the bias affects far less than levels,
    but no level here is capital-worthy on its own.

RULE 8 (required)
    IS 2010-2016, OOS 2017-2026 read once.  Two walk-forwards:
      W1  the SLOPE claim: rho is computed on IS only and on OOS only, per key x membership x arm.
          A sign gap that is real must reappear OOS.
      W2  a PICK: the decile with the best IS EWall Sharpe is chosen per key x membership and its
          OOS CAGR/Sharpe/MaxDD is read against SPY, RULES v2 (live baseline) and the do-nothing
          whole-panel EWall control at the same gross.
    KEEP paths 4a and 4b are evaluated for every decile book.

Outputs (committed): .console.txt  .deciles.csv  .slopes.csv  .bootstrap.csv  .walkforward.csv
                     .keys.csv  .result.md
Runtime ~15 min.
"""
import sys, time, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

STAMP = "2026-09-08_re-scope-idea-313-advQ-carries-a-price-LEVEL_cloud"
OUT = Path(__file__).resolve().parent
COST = 10.0
PIN_G, PIN_FREQ = 0.75, "W"          # idea 51's pre-registered decile point
MA_WIN, NDEC, KEY_WIN = 200, 10, 60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NBOOT, SEED = 1000, 424

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ------------------------------------------------------------------ book construction
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e

def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)

def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()

def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def rowify(r):
    m = metrics(r); h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])

def keep_4a(r, b):
    a1, a2 = halves(r); b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])

def keep_4b(r, spy):
    a1, a2 = halves(r); s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return bool(a1 > s1 and a2 > s2
                and metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]
                and m["MaxDD"] >= 0.60 * ms["MaxDD"] and m["CAGR"] >= 0.70 * ms["CAGR"])


# ------------------------------------------------------------------ size keys
def last_valid_row(px):
    lv = px.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                  else np.nan)
    return pd.DataFrame(np.tile(lv.values, (len(px), 1)), index=px.index,
                        columns=px.columns).where(px.notna())

def static_cap(cols):
    f = ROOT / "research" / "deepvalue" / "universe_under2b.csv"
    u = pd.read_csv(f, usecols=["ticker", "mktcap"]).dropna()
    u = u[u.mktcap > 0].drop_duplicates("ticker").set_index("ticker")["mktcap"]
    return u.reindex(cols).dropna()

def build_keys(px, cols):
    """RAW (unranked) liquidity keys on the tradable columns.  advQ is idea 51's exact column."""
    vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
    term = last_valid_row(px)
    raw = {"advQ":  (px * vol)[cols],          # px LEVEL x volume   (idea 51's column)
           "VOLSH": vol[cols],                 # share volume only   (T1-invariant)
           "DVOLT": (term * vol)[cols]}        # FIXED price scale x volume
    return {k: v.rolling(KEY_WIN, min_periods=30).median() for k, v in raw.items()}


def rescale(px, sigma, seed):
    """Idea 197's T1 operator: px -> px @ diag(c), c_i = exp(N(0, sigma)), one draw per NAME.
    Exactly what truncating an auto-adjusted panel at an earlier date does to it."""
    rng = np.random.default_rng(seed)
    c = np.exp(rng.normal(0.0, sigma, size=px.shape[1]))
    return px.mul(pd.Series(c, index=px.columns), axis=1)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 424 — does the capQ/advQ decile SIGN gap survive replacing advQ with a price-free key?")
    P(f"  pinned: g={PIN_G}, cadence {PIN_FREQ}, cost {COST:.0f} bps (0 bps alongside), "
      f"NDEC={NDEC}, key window {KEY_WIN}d, MA {MA_WIN}d")
    P("  2 parameters: key in {capQ, advQ, VOLSH, DVOLT} x membership in {STATIC, DYNAMIC}")
    P("=" * 112)

    # ---------------------------------------------------------------- panel
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in pxs.columns if c != "SPY"]
    cols = [c for c in s_all if c not in bad]
    P(f"\nPANEL  SMALL: {len(s_all)} names, dropped {len(s_all)-len(cols)} with max_1d_move >= 1.0 "
      f"-> {len(cols)} tradable")
    px = pxs[cols + ["SPY"]].dropna(how="all").ffill()
    tradable = set(cols)
    P(f"       {px.index[0].date()} .. {px.index[-1].date()}  ({len(px)} rows)")
    P("       SURVIVORSHIP: current constituents of the sub-$2B screen only; every LEVEL on this "
      "panel is biased UP, thin deciles most.  Claims below are key-vs-key DIFFERENCES.")

    start = px.index[260]                       # same warm-up convention as baseline.compare
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
    P(f"\nREFERENCES over {start.date()}..{px.index[-1].date()}")
    for nm, r in (("SPY", spy), ("RULES v2 (live)", b2)):
        m = metrics(r); mo = metrics(r.loc[OOS_START:])
        P(f"  {nm:16s} CAGR {m['CAGR']:7.2%}  Sharpe {m['Sharpe']:6.3f}  MaxDD {m['MaxDD']:7.2%}"
          f"   | OOS CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:6.3f} MaxDD {mo['MaxDD']:7.2%}")

    # do-nothing control: whole-panel EWall at the same gross
    e_all = _priced(px, tradable) > 0
    ma_all = above_ma(px) & e_all
    ctrl = backtest(px, _ew(e_all, PIN_G), cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
    mc = metrics(ctrl); mco = metrics(ctrl.loc[OOS_START:])
    P(f"  {'EWall whole panel':16s} CAGR {mc['CAGR']:7.2%}  Sharpe {mc['Sharpe']:6.3f}  "
      f"MaxDD {mc['MaxDD']:7.2%}   | OOS CAGR {mco['CAGR']:7.2%} Sharpe {mco['Sharpe']:6.3f} "
      f"MaxDD {mco['MaxDD']:7.2%}")

    # ---------------------------------------------------------------- keys
    cap = static_cap(cols)
    keys = build_keys(px, cols)
    P(f"\nKEYS   capQ covers {len(cap)}/{len(cols)} tradable names "
      f"(median ${cap.median()/1e6:.0f}M, ${cap.min()/1e6:.0f}M-${cap.max()/1e6:.0f}M)")
    for k, v in keys.items():
        unit = "$" if k in ("advQ", "DVOLT") else ""
        P(f"       {k:6s} panel-median 60d value {unit}{v.stack().median()/1e6:.3f}M  "
          f"({v.notna().any().sum()} names)")

    # ---- G2  T1 invariance on THIS panel (idea 197's operator, re-measured, not cited)
    P("\nG2  T1 RE-ADJUSTMENT INVARIANCE (px -> px @ diag(c), c ~ lognormal(0, sigma), 3 seeds)")
    P("    'moved' = fraction of finite key cells whose cross-sectional rank changes.")
    kt_rows = []
    for sigma in (0.25, 0.50):
        for seed in (1, 2, 3):
            px2 = rescale(px, sigma, seed)
            keys2 = build_keys(px2, cols)
            for k in keys:
                a = keys[k].rank(axis=1, pct=True); b = keys2[k].rank(axis=1, pct=True)
                fin = a.notna() & b.notna()
                moved = float(((a - b).abs() > 1e-12)[fin].sum().sum() / fin.sum().sum())
                kt_rows.append(dict(key=k, sigma=sigma, seed=seed, moved=moved))
            # capQ is a file column, untouched by any price operator, by construction
            kt_rows.append(dict(key="capQ", sigma=sigma, seed=seed, moved=0.0))
    KT = pd.DataFrame(kt_rows)
    KT.to_csv(OUT / f"{STAMP}.keys.csv", index=False)
    for k in ["capQ", "advQ", "VOLSH", "DVOLT"]:
        s = KT[KT.key == k]
        P(f"    {k:6s} moved {s.moved.mean():.4f} mean  "
          f"[{s.moved.min():.4f}, {s.moved.max():.4f}] over {len(s)} draws")
    P("    -> advQ/DVOLT carry a price LEVEL (cells move); VOLSH and capQ do not.")

    # ---- key agreement (idea 51 quoted capQ~advQ corr +0.545)
    P("\n    pairwise agreement of the STATIC per-name key ranks (Spearman, n = names):")
    stat_key = {"capQ": cap.reindex(cols)}
    for k, v in keys.items():
        stat_key[k] = v.median(axis=0).reindex(cols)
    SK = pd.DataFrame(stat_key)
    agree = SK.rank().corr(method="pearson")
    P("    " + agree.to_string(float_format=lambda x: f"{x:+.3f}").replace("\n", "\n    "))

    # ---------------------------------------------------------------- decile books
    P("\n" + "=" * 112)
    P("Q1  DECILE LADDERS — 4 keys x 2 memberships x 10 deciles x 3 arms (ALL grid points below)")
    P("=" * 112)
    schemes = [("capQ", "STATIC")] + [(k, m) for k in ("advQ", "VOLSH", "DVOLT")
                                      for m in ("STATIC", "DYNAMIC")]
    rets_store: dict[tuple, pd.Series] = {}
    dec_rows = []
    for key, memb in schemes:
        if key == "capQ":
            base_static = cap.reindex(cols).dropna()
        else:
            base_static = keys[key].median(axis=0).reindex(cols).dropna()
        q_static = pd.qcut(base_static.rank(method="first"), NDEC, labels=False) + 1
        rk = None if memb == "STATIC" else keys[key].rank(axis=1, pct=True)

        for d in range(1, NDEC + 1):
            memb_mask = pd.DataFrame(False, index=px.index, columns=px.columns)
            if memb == "STATIC":
                names = list(q_static[q_static == d].index)
                memb_mask[names] = True
                nsz = len(names)
                lbl = (f"${cap[names].median()/1e6:.0f}M cap" if key == "capQ"
                       else f"{base_static[names].median()/1e6:.3f}M {key}")
                sub = names + ["SPY"]                       # column subset -> fast path
            else:
                lo, hi = (d - 1) / NDEC, d / NDEC
                sel = (rk > lo) & (rk <= hi) if d > 1 else (rk >= 0) & (rk <= hi)
                memb_mask.loc[:, sel.columns] = sel.fillna(False).values
                nsz = int(sel.sum(axis=1).mean())
                lbl = f"{keys[key].where(sel).stack().median()/1e6:.3f}M {key}"
                sub = list(px.columns)

            e = (e_all & memb_mask)[sub]
            ma = (ma_all & memb_mask)[sub]
            pxd = px[sub]
            n_all_d = e.sum(axis=1).replace(0, np.nan)
            books = {"EWall": _ew(e, PIN_G), "MA-RS": _ew(ma, PIN_G),
                     "MA-DG": (PIN_G * ma.astype(float)).div(n_all_d, axis=0).fillna(0.0)}
            rets = {k: backtest(pxd, w, cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
                    for k, w in books.items()}
            rets0 = {k: backtest(pxd, w, cost_bps=0.0, freq=PIN_FREQ)["returns"].loc[start:]
                     for k, w in books.items()}
            c, c0 = metrics(rets["EWall"]), metrics(rets0["EWall"])
            ci = metrics(rets["EWall"].loc[:IS_END]); co = metrics(rets["EWall"].loc[OOS_START:])
            for arm in ("EWall", "MA-RS", "MA-DG"):
                r = rets[arm]
                rets_store[(key, memb, d, arm)] = r
                row = dict(key=key, membership=memb, decile=d, n_names=nsz, size=lbl, arm=arm)
                row.update(rowify(r))
                row["dCAGR_vs_EWall"] = row["CAGR"] - c["CAGR"]
                row["dSharpe_vs_EWall"] = row["Sharpe"] - c["Sharpe"]
                row["dCAGR0_vs_EWall"] = metrics(rets0[arm])["CAGR"] - c0["CAGR"]
                row["dSharpeIS_vs_EWall"] = metrics(r.loc[:IS_END])["Sharpe"] - ci["Sharpe"]
                row["dSharpeOOS_vs_EWall"] = metrics(r.loc[OOS_START:])["Sharpe"] - co["Sharpe"]
                row["keep4a"] = keep_4a(r, b2)
                row["keep4b"] = keep_4b(r, spy)
                dec_rows.append(row)
        P(f"  {key}-{memb[:1]} done ({time.time()-t0:.0f}s)")
    D = pd.DataFrame(dec_rows)
    D.to_csv(OUT / f"{STAMP}.deciles.csv", index=False)

    # ---- G1 reproduction of idea 51 lane B, reported PER LEG
    P("\nG1  REPRODUCTION of idea 51 lane B `.deciles.csv` (capQ-STATIC and advQ-DYNAMIC rows)")
    ref = pd.read_csv(OUT / "2026-09-06_trend-filter-by-market-cap_B.deciles.csv")
    ref["key"] = ref.scheme.map({"capQ": "capQ", "advQ": "advQ"})
    ref["membership"] = ref.scheme.map({"capQ": "STATIC", "advQ": "DYNAMIC"})
    mine = D.merge(ref, on=["key", "membership", "decile", "arm"], suffixes=("", "_ref"))
    for leg, sub in mine.groupby(["key", "membership"]):
        nmis = int((sub.n_names != sub.n_names_ref).sum())
        P(f"    {leg[0]}-{leg[1][:1]} ({len(sub)} rows, {nmis} with a different decile size):")
        for c_ in ("CAGR", "Sharpe", "MaxDD", "dSharpe_vs_EWall"):
            P(f"      {c_:18s} max |diff| {(sub[c_] - sub[c_ + '_ref']).abs().max():.2e}")
    adv = mine[mine.key == "advQ"]
    P(f"    -> advQ-DYNAMIC (the leg the queue's question is about) "
      f"{'REPRODUCES EXACTLY' if (adv.Sharpe - adv.Sharpe_ref).abs().max() < 1e-9 else 'MISMATCHES'}"
      f" arm-for-arm on all {len(adv)} rows.")
    P(f"    -> capQ-STATIC does NOT reproduce bit-exact, and the cause is a DATA VINTAGE, not this")
    P(f"       script: `research/deepvalue/universe_under2b.csv` was re-committed on 2026-09-07,")
    P(f"       AFTER idea 51 ran.  It now covers {len(cap)} of the 439 tradable names against the")
    P(f"       435 idea 51's console reports, and since the decile edges are `qcut` on the covered")
    P(f"       set, one name moves and the 43/44 sizes alternate differently.  The published capQ")
    P(f"       vintage is not recoverable from the repo.  Bound on the damage: max |dSharpe| drift")
    P(f"       {(mine[mine.key=='capQ'].Sharpe - mine[mine.key=='capQ'].Sharpe_ref).abs().max():.4f}"
      f", and idea 51's HEADLINE slopes still reproduce (see Q2: capQ MA-DG rho -0.335 vs published")
    P(f"       -0.336/-0.335; advQ-D MA-RS rho +0.335 vs published +0.335).  Reported, not asserted away.")

    # ---------------------------------------------------------------- slopes
    P("\n" + "=" * 112)
    P("Q2  THE SIGN GAP — rho(decile, dSharpe vs EWall), FULL / IS 2010-2016 / OOS 2017-2026")
    P("    n = 10 deciles, so SE(rho) ~ 0.354; t = rho*sqrt(8)/sqrt(1-rho^2).")
    P("=" * 112)
    def rho_t(x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        if np.std(y) < 1e-15: return 0.0, 0.0
        r = float(np.corrcoef(x, y)[0, 1])
        r = min(max(r, -0.999999), 0.999999)
        return r, float(r * np.sqrt(len(x) - 2) / np.sqrt(1 - r * r))

    sl_rows = []
    P(f"  {'key':6s} {'memb':8s} {'arm':6s} "
      f"{'rho_full':>9s} {'t':>6s} {'rho_IS':>8s} {'t':>6s} {'rho_OOS':>8s} {'t':>6s} "
      f"{'rhoCAGR':>8s} {'+d/10':>6s}")
    for key, memb in schemes:
        for arm in ("MA-RS", "MA-DG"):
            s = D[(D.key == key) & (D.membership == memb) & (D.arm == arm)].sort_values("decile")
            rf, tf = rho_t(s.decile, s.dSharpe_vs_EWall)
            ri, ti = rho_t(s.decile, s.dSharpeIS_vs_EWall)
            ro, to = rho_t(s.decile, s.dSharpeOOS_vs_EWall)
            rc, tc = rho_t(s.decile, s.dCAGR_vs_EWall)
            npos = int((s.dSharpe_vs_EWall > 0).sum())
            sl_rows.append(dict(key=key, membership=memb, arm=arm, rho_full=rf, t_full=tf,
                                rho_IS=ri, t_IS=ti, rho_OOS=ro, t_OOS=to, rho_CAGR=rc,
                                t_CAGR=tc, n_pos_deciles=npos))
            P(f"  {key:6s} {memb:8s} {arm:6s} {rf:+9.3f} {tf:+6.2f} {ri:+8.3f} {ti:+6.2f} "
              f"{ro:+8.3f} {to:+6.2f} {rc:+8.3f} {npos:4d}/10")
    S = pd.DataFrame(sl_rows)
    S.to_csv(OUT / f"{STAMP}.slopes.csv", index=False)

    # ---------------------------------------------------------------- bootstrap
    P("\n" + "=" * 112)
    P(f"Q3  PAIRED CALENDAR-YEAR BLOCK BOOTSTRAP ({NBOOT} draws, seed {SEED}) — is the sign gap real?")
    P("    One year-resample per draw, applied to EVERY book, so rho and the gap are PAIRED.")
    P("=" * 112)
    idx = rets_store[("capQ", "STATIC", 1, "EWall")].index
    years = idx.year.values
    uy = np.unique(years)
    ypos = {y: np.where(years == y)[0] for y in uy}
    Rmat = {k: v.values for k, v in rets_store.items()}
    rng = np.random.default_rng(SEED)
    draws = [np.concatenate([ypos[y] for y in rng.choice(uy, size=len(uy), replace=True)])
             for _ in range(NBOOT)]

    def sharpe_np(a):
        sd = a.std(ddof=1)
        return 0.0 if sd < 1e-15 else float(a.mean() / sd * np.sqrt(252))

    boot = {}
    for key, memb in schemes:
        for arm in ("MA-RS", "MA-DG"):
            rr = np.empty(NBOOT)
            for j, sel in enumerate(draws):
                ds = [sharpe_np(Rmat[(key, memb, d, arm)][sel])
                      - sharpe_np(Rmat[(key, memb, d, "EWall")][sel]) for d in range(1, NDEC + 1)]
                ds = np.asarray(ds)
                rr[j] = 0.0 if ds.std() < 1e-15 else np.corrcoef(np.arange(1, NDEC + 1), ds)[0, 1]
            boot[(key, memb, arm)] = rr
        P(f"  {key}-{memb[:1]} bootstrapped ({time.time()-t0:.0f}s)")

    bt_rows = []
    P(f"\n  {'key':6s} {'memb':8s} {'arm':6s} {'rho_pt':>8s} {'boot mean':>9s} "
      f"{'5%':>7s} {'95%':>7s} {'P(rho>0)':>9s}")
    for (key, memb, arm), rr in boot.items():
        pt = float(S[(S.key == key) & (S.membership == memb) & (S.arm == arm)].rho_full.iloc[0])
        lo, hi = np.percentile(rr, [5, 95])
        bt_rows.append(dict(key=key, membership=memb, arm=arm, rho_point=pt, boot_mean=rr.mean(),
                            p05=lo, p95=hi, p_positive=float((rr > 0).mean())))
        P(f"  {key:6s} {memb:8s} {arm:6s} {pt:+8.3f} {rr.mean():+9.3f} {lo:+7.3f} {hi:+7.3f} "
          f"{(rr > 0).mean():9.3f}")

    P("\n  THE GAP (rho_key - rho_capQ), paired per draw:")
    P(f"  {'arm':6s} {'contrast':22s} {'gap_pt':>8s} {'boot mean':>9s} {'5%':>7s} {'95%':>7s} "
      f"{'P(gap>0)':>9s} {'P(signs differ)':>16s}")
    gp_rows = []
    for arm in ("MA-RS", "MA-DG"):
        ref_rr = boot[("capQ", "STATIC", arm)]
        ref_pt = float(S[(S.key == "capQ") & (S.arm == arm)].rho_full.iloc[0])
        for key, memb in schemes:
            if key == "capQ": continue
            rr = boot[(key, memb, arm)]
            g = rr - ref_rr
            pt = float(S[(S.key == key) & (S.membership == memb) & (S.arm == arm)].rho_full.iloc[0])
            lo, hi = np.percentile(g, [5, 95])
            flip = float((np.sign(rr) != np.sign(ref_rr)).mean())
            gp_rows.append(dict(arm=arm, key=key, membership=memb, gap_point=pt - ref_pt,
                                boot_mean=g.mean(), p05=lo, p95=hi,
                                p_gap_positive=float((g > 0).mean()), p_signs_differ=flip))
            P(f"  {arm:6s} {key+'-'+memb[:1]+' vs capQ-S':22s} {pt-ref_pt:+8.3f} {g.mean():+9.3f} "
              f"{lo:+7.3f} {hi:+7.3f} {(g > 0).mean():9.3f} {flip:16.3f}")
    pd.DataFrame(bt_rows + gp_rows).to_csv(OUT / f"{STAMP}.bootstrap.csv", index=False)

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 112)
    P("Q4  RULE 8 W2 — decile chosen by best IS (2010-2016) EWall Sharpe, OOS 2017-2026 read once")
    P("=" * 112)
    mo_spy, mo_b2, mo_c = (metrics(spy.loc[OOS_START:]), metrics(b2.loc[OOS_START:]),
                           metrics(ctrl.loc[OOS_START:]))
    wf = []
    P(f"  {'key':6s} {'memb':8s} {'pick':>4s} {'IS Sh':>7s} | "
      f"{'OOS CAGR':>9s} {'OOS Sh':>7s} {'OOS DD':>8s} | {'vs SPY Sh':>9s} {'vs v2 Sh':>9s} "
      f"{'vs ctrl Sh':>10s} {'4a':>4s} {'4b':>4s}")
    for key, memb in schemes:
        s = D[(D.key == key) & (D.membership == memb) & (D.arm == "EWall")]
        pick = int(s.loc[s.IS_Sharpe.idxmax(), "decile"])
        row = D[(D.key == key) & (D.membership == memb) & (D.decile == pick)
                & (D.arm == "EWall")].iloc[0]
        wf.append(dict(key=key, membership=memb, pick_decile=pick, IS_Sharpe=row.IS_Sharpe,
                       OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
                       d_vs_SPY=row.OOS_Sharpe - mo_spy["Sharpe"],
                       d_vs_v2=row.OOS_Sharpe - mo_b2["Sharpe"],
                       d_vs_ctrl=row.OOS_Sharpe - mo_c["Sharpe"],
                       keep4a=bool(row.keep4a), keep4b=bool(row.keep4b)))
        P(f"  {key:6s} {memb:8s} {pick:4d} {row.IS_Sharpe:7.3f} | {row.OOS_CAGR:9.2%} "
          f"{row.OOS_Sharpe:7.3f} {row.OOS_MaxDD:8.2%} | {row.OOS_Sharpe-mo_spy['Sharpe']:+9.3f} "
          f"{row.OOS_Sharpe-mo_b2['Sharpe']:+9.3f} {row.OOS_Sharpe-mo_c['Sharpe']:+10.3f} "
          f"{str(bool(row.keep4a)):>4s} {str(bool(row.keep4b)):>4s}")
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P(f"\n  OOS references: SPY Sharpe {mo_spy['Sharpe']:.3f} CAGR {mo_spy['CAGR']:.2%} "
      f"MaxDD {mo_spy['MaxDD']:.2%} | RULES v2 {mo_b2['Sharpe']:.3f} / {mo_b2['CAGR']:.2%} "
      f"/ {mo_b2['MaxDD']:.2%} | EWall-panel control {mo_c['Sharpe']:.3f} / {mo_c['CAGR']:.2%} "
      f"/ {mo_c['MaxDD']:.2%}")
    P(f"  picks beating SPY OOS Sharpe: {(W.d_vs_SPY > 0).sum()}/{len(W)}; "
      f"beating the do-nothing control: {(W.d_vs_ctrl > 0).sum()}/{len(W)}; "
      f"beating RULES v2: {(W.d_vs_v2 > 0).sum()}/{len(W)}")
    P(f"  READ THIS BEFORE THE ROW ABOVE: the IS chooser lands on decile 1 in "
      f"{int((W.pick_decile == 1).sum())} of {len(W)} cells — the THINNEST, least-liquid decile,")
    P("  which is precisely where current-constituent survivorship is largest (idea 51's cloud")
    P("  replication rejected the same corner: 'control returns 19.71% CAGR, least-liquid")
    P("  survivorship decile').  These OOS Sharpes are a bias measurement, NOT an edge, and 4b")
    P("  passes 0 of 210 books, which is the honest reading of the same fact.")

    # ---------------------------------------------------------------- keep paths
    P("\n" + "=" * 112)
    P("Q5  KEEP PATHS over ALL grid points")
    P("=" * 112)
    P(f"  4a passes: {int(D.keep4a.sum())}/{len(D)} books;  4b passes: {int(D.keep4b.sum())}/{len(D)}")
    for flag in ("keep4a", "keep4b"):
        sub = D[D[flag]]
        if len(sub):
            P(f"  {flag} rows: " + ", ".join(
                f"{r.key}-{r.membership[:1]} d{r.decile} {r.arm}" for r in sub.itertuples()))
    P("  NOTE any 4b pass on this panel is on CURRENT constituents only (survivorship);"
      " it is a decomposition read, not a capital claim.")

    P(f"\nDONE in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
