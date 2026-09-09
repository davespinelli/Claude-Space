#!/usr/bin/env python3
"""IDEA 313 — why do capQ and advQ disagree in SIGN?   (lane B, 2026-09-09)

QUESTION (QUEUE idea 313, verbatim)
    Idea 51's two size columns give decile slopes of -0.336 and +0.335 for the same book on
    the same panel, correlating only +0.545.  Decompose: is the disagreement the
    static-vs-dynamic membership, the look-ahead in the 2026 cap stamp, or survivorship in
    the thin deciles (advQ decile 1 EWall Sharpe 2.03)?  Rebuild capQ as a causal
    price-times-fixed-shares proxy and re-read both slopes.

WHAT IS ALREADY SETTLED, AND WHAT IS NOT
    Idea 424 (2026-09-08, cloud) crossed KEY CONTENT with STATIC/DYNAMIC membership and found
    (a) the gap widens with a price-free key and (b) rho_IS is positive 14/14 while rho_OOS is
    negative 10/14, i.e. the decile-slope statistic does not survive rule 8.  It did NOT build
    a causal cap, and its STATIC stamp is a WHOLE-SAMPLE median — neither early nor late — so
    the look-ahead leg idea 313 names has never been measured.  That leg is this script.

DESIGN — the 2x3 that fills in idea 51's diagonal
    Idea 51 compared capQ (a cap stamped in 2026, membership fixed forever) against advQ (a
    liquidity key re-ranked every day).  Those are OPPOSITE CORNERS of a 2x3: the comparison
    moves KEY CONTENT and STAMP TIMING at once and cannot attribute the sign gap to either.
    Every cell is run here.

        p1  key    CAP   cap_t = px_t * shares_eff_i,  shares_eff_i = mktcap_2026 / px_i(last)
                         so the LATE stamp of CAP is EXACTLY idea 51's capQ ranking.
                   ADV   (px * vol).rolling(60).median()  — idea 51's advQ column, verbatim.
        p2  stamp  LATE  rank once on each name's LAST valid key value   (look-ahead stamp)
                   EARLY rank once on each name's FIRST valid key value  (causal stamp)
                   DYN   rank cross-sectionally every day                (causal, time-varying)

        idea 51's capQ = (CAP, LATE);  idea 51's advQ = (ADV, DYN).   Both are reproduction gates.

    The decomposition then reads two ways, and BOTH are reported:
        path A   gap = [CAP: LATE -> DYN]      + [at DYN: CAP -> ADV]
        path B   gap = [at LATE: CAP -> ADV]   + [ADV: LATE -> DYN]
    A stamp leg that is large and a key leg that is small means idea 51's sign gap is the
    2026 look-ahead; the reverse means the two keys genuinely measure different things.

    HONEST BOUND ON WHAT "CAUSAL" BUYS.  shares_eff is a 2026 share count.  What CAP/EARLY and
    CAP/DYN remove is the PRICE look-ahead inside the cap stamp — the component that actually
    moves over 16 years — not the share-count look-ahead.  A fully causal cap needs a shares
    history, which data/ does not carry (QUEUE idea 195 is PARKed on exactly that).  Stated,
    not hidden: no cell here is a clean market-cap decile, and none is tradable.

Q3 — SURVIVORSHIP, the third named cause
    Two re-reads of the same slopes, no new tuned parameter:
      (i)  drop decile 1 (the thin corner idea 51 flagged at EWall Sharpe 2.03) and recompute rho
      (ii) rebuild every scheme on FULLHIST — names priced on the panel's FIRST bar, i.e. no
           late entrants — and recompute rho.  Current-constituent survivorship is worst for
           names that entered late and thin; if the sign gap is survivorship it should move here.

TUNED PARAMETERS: 2 (key, stamp), fully crossed, ALL 6 grid points reported for every arm.
    Everything else is PINNED at idea 51 lane B's pre-registered decile point and is not tuned:
    g = 0.75, weekly, cost 10 bps, NDEC = 10, key window 60d (min_periods 30), MA 200d,
    arms {EWall, MA-RS, MA-DG}.

GATES
    G1a  (CAP, LATE) decile membership must reproduce idea 51's capQ deciles, and its rows must
         reproduce idea 424's committed .deciles.csv capQ-STATIC rows (same vintage).
    G1b  (ADV, DYN) rows must reproduce idea 424's advQ-DYNAMIC rows, which are bit-exact to
         idea 51 lane B.
    G2   shares_eff reconciliation: mktcap / px(last) vs the file's own `shares` column.

RULE 8 (required)
    IS 2010-2016, OOS 2017-2026 read once.
    W1  the SLOPE claim: rho computed on IS only and on OOS only per (key, stamp, arm).
    W2  a PICK: the decile with the best IS EWall Sharpe per scheme; its OOS CAGR/Sharpe/MaxDD
        read once against SPY, RULES v2 (live baseline) and the whole-panel EWall control.
    KEEP paths 4a and 4b evaluated for every book.

HONESTY
    rho over NDEC = 10 points has SE ~ 1/sqrt(8) = 0.354.  Every rho carries a t and a 1,000-draw
    paired calendar-YEAR block bootstrap (one year-resample per draw applied to every book, so
    gaps are paired).

PANEL / SURVIVORSHIP
    SMALL panel only (data/prices_small.csv.gz, sub-$2B screen), tickers with max_1d_move >= 1.0
    in data/small_meta.csv dropped.  SURVIVORSHIP: current constituents of the screen only — no
    delisted names — so every LEVEL is biased UP, thin deciles most.  Claims here are
    scheme-vs-scheme DIFFERENCES on one panel.

Outputs (committed): .console.txt .deciles.csv .slopes.csv .bootstrap.csv .walkforward.csv
                     .surv.csv .result.md
Deterministic; no network.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

STAMP = "2026-09-09_why-do-capQ-and-advQ-disagree-in-SIGN_B"
OUT = Path(__file__).resolve().parent
COST = 10.0
PIN_G, PIN_FREQ = 0.75, "W"
MA_WIN, NDEC, KEY_WIN = 200, 10, 60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NBOOT, SEED = 1000, 313
KEYS, STAMPS = ("CAP", "ADV"), ("LATE", "EARLY", "DYN")
ARMS = ("EWall", "MA-RS", "MA-DG")

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ------------------------------------------------------------------ book construction
def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)

def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def rowify(r):
    m = metrics(r); h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
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
def first_last_valid(df):
    """(first valid value, last valid value) per column, as Series."""
    f = df.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None else np.nan)
    l = df.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None else np.nan)
    return f, l

def build_raw_keys(px, cols):
    """RAW (unranked) key SERIES on the tradable columns."""
    u = pd.read_csv(ROOT / "research" / "deepvalue" / "universe_under2b.csv",
                    usecols=["ticker", "mktcap", "price", "shares"]).dropna(subset=["mktcap"])
    u = u[u.mktcap > 0].drop_duplicates("ticker").set_index("ticker")
    cap_stamp = u["mktcap"].reindex(cols).dropna()

    pxc = px[cols]
    _, px_last = first_last_valid(pxc)
    shares_eff = (cap_stamp / px_last.reindex(cap_stamp.index)).dropna()      # price-times-FIXED-shares
    CAP = pxc[shares_eff.index].mul(shares_eff, axis=1)                        # cap_t = px_t * shares_eff

    vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
    ADV = (pxc * vol[cols]).rolling(KEY_WIN, min_periods=30).median()
    return {"CAP": CAP, "ADV": ADV}, cap_stamp, shares_eff, u


def rank_scheme(raw, stamp):
    """Return (static_key Series, dynamic pct-rank DataFrame or None) for a stamp."""
    if stamp == "DYN":
        return None, raw.rank(axis=1, pct=True)
    f, l = first_last_valid(raw)
    return (f if stamp == "EARLY" else l).dropna(), None


def rho_t(x, y, method="pearson"):
    """Correlation over the decile ladder plus its t.

    METHOD MATTERS AND THE RECORD DOES NOT SAY WHICH IT USED.  Idea 51's and idea 424's
    published "rho(decile, dSharpe)" is `np.corrcoef(decile, dSharpe)` — a PEARSON
    correlation on 10 points — even though the surrounding prose calls it Spearman.  Both
    are computed here: `pearson` reproduces the record, `spearman` is what the prose says.
    """
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 4 or np.std(y) < 1e-15:
        return np.nan, np.nan
    if method == "spearman":
        x = pd.Series(x).rank().values; y = pd.Series(y).rank().values
    r = float(np.corrcoef(x, y)[0, 1])
    r = min(max(r, -0.999999), 0.999999)
    return r, float(r * np.sqrt(len(x) - 2) / np.sqrt(1 - r * r))


# ==================================================================================== run
def run_panel(px, cols, tag, raws, e_all, ma_all, start, spy, b2, store=None):
    """Build every (key, stamp, decile, arm) book on one panel; return the decile DataFrame."""
    rows = []
    for key in KEYS:
        raw = raws[key]
        have = [c for c in cols if c in raw.columns]
        for stamp in STAMPS:
            static_key, rk = rank_scheme(raw[have], stamp)
            if static_key is not None:
                q_static = pd.qcut(static_key.rank(method="first"), NDEC, labels=False) + 1
            for d in range(1, NDEC + 1):
                memb = pd.DataFrame(False, index=px.index, columns=px.columns)
                if static_key is not None:
                    names = list(q_static[q_static == d].index)
                    memb[names] = True
                    nsz = float(len(names))
                    sub = names + ["SPY"]
                else:
                    lo, hi = (d - 1) / NDEC, d / NDEC
                    sel = (rk > lo) & (rk <= hi) if d > 1 else (rk >= 0) & (rk <= hi)
                    memb.loc[:, sel.columns] = sel.fillna(False).values
                    nsz = float(sel.sum(axis=1).mean())
                    sub = list(px.columns)
                e = (e_all & memb)[sub]
                ma = (ma_all & memb)[sub]
                pxd = px[sub]
                n_all_d = e.sum(axis=1).replace(0, np.nan)
                books = {"EWall": _ew(e, PIN_G), "MA-RS": _ew(ma, PIN_G),
                         "MA-DG": (PIN_G * ma.astype(float)).div(n_all_d, axis=0).fillna(0.0)}
                rets = {k: backtest(pxd, w, cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
                        for k, w in books.items()}
                c = metrics(rets["EWall"])
                ci = metrics(rets["EWall"].loc[:IS_END]); co = metrics(rets["EWall"].loc[OOS_START:])
                for arm in ARMS:
                    r = rets[arm]
                    if store is not None:
                        store[(key, stamp, d, arm)] = r
                    row = dict(panel=tag, key=key, stamp=stamp, decile=d, n_names=nsz, arm=arm)
                    row.update(rowify(r))
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - c["Sharpe"]
                    row["dCAGR_vs_EWall"] = row["CAGR"] - c["CAGR"]
                    row["dSharpeIS_vs_EWall"] = metrics(r.loc[:IS_END])["Sharpe"] - ci["Sharpe"]
                    row["dSharpeOOS_vs_EWall"] = metrics(r.loc[OOS_START:])["Sharpe"] - co["Sharpe"]
                    row["keep4a"] = keep_4a(r, b2)
                    row["keep4b"] = keep_4b(r, spy)
                    rows.append(row)
            P(f"    {tag}  {key}/{stamp:5s} done")
    return pd.DataFrame(rows)


def slope_table(D, panel, col="dSharpe_vs_EWall", deciles=None, method="pearson"):
    out = []
    for key in KEYS:
        for stamp in STAMPS:
            for arm in ARMS:
                s = D[(D.panel == panel) & (D.key == key) & (D.stamp == stamp) & (D.arm == arm)]
                s = s.sort_values("decile")
                if deciles is not None:
                    s = s[s.decile.isin(deciles)]
                r, t = rho_t(s.decile.values, s[col].values, method)
                out.append(dict(panel=panel, key=key, stamp=stamp, arm=arm, stat=col,
                                method=method, n=len(s), rho=r, t=t))
    return pd.DataFrame(out)


def rho_of(S, panel, key, stamp, arm, stat, method="pearson"):
    q = S[(S.panel == panel) & (S.key == key) & (S.stamp == stamp) & (S.arm == arm)
          & (S.stat == stat) & (S.method == method)]
    return np.nan if q.empty else q.rho.iloc[0]


def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 313 — why do capQ and advQ disagree in SIGN?   (lane B, 2026-09-09)")
    P(f"  pinned: g={PIN_G}, cadence {PIN_FREQ}, cost {COST:.0f} bps, NDEC={NDEC}, "
      f"key window {KEY_WIN}d, MA {MA_WIN}d, arms {ARMS}")
    P("  2 parameters: key in {CAP, ADV} x stamp in {LATE, EARLY, DYN}; all 6 cells reported")
    P("=" * 112)

    # ---------------------------------------------------------------- panel
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in pxs.columns if c != "SPY"]
    cols = [c for c in s_all if c not in bad]
    px = pxs[cols + ["SPY"]].dropna(how="all").ffill()
    P(f"\nPANEL SMALL: {len(s_all)} names, dropped {len(s_all)-len(cols)} with max_1d_move >= 1.0 "
      f"-> {len(cols)} tradable;  {px.index[0].date()} .. {px.index[-1].date()} ({len(px)} rows)")
    P("      SURVIVORSHIP: current constituents of the sub-$2B screen only; LEVELS biased UP, "
      "thin deciles most.  Claims below are scheme-vs-scheme DIFFERENCES.")

    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
    e_all = px.notna() & pd.DataFrame(True, index=px.index, columns=px.columns)
    e_all[[c for c in px.columns if c not in cols]] = False
    ma_all = (px > px.rolling(MA_WIN).mean()) & e_all
    ctrl = backtest(px, _ew(e_all, PIN_G), cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]

    P(f"\nREFERENCES over {start.date()}..{px.index[-1].date()}")
    for nm, r in (("SPY", spy), ("RULES v2 (live)", b2), ("EWall whole panel", ctrl)):
        m = metrics(r); mo = metrics(r.loc[OOS_START:])
        P(f"  {nm:20s} CAGR {m['CAGR']:7.2%} Sharpe {m['Sharpe']:6.3f} MaxDD {m['MaxDD']:7.2%}"
          f" | OOS CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:6.3f} MaxDD {mo['MaxDD']:7.2%}")

    # ---------------------------------------------------------------- keys + G2
    raws, cap_stamp, shares_eff, u = build_raw_keys(px, cols)
    P(f"\nKEYS  CAP covers {raws['CAP'].shape[1]}/{len(cols)} tradable names "
      f"(2026 mktcap median ${cap_stamp.median()/1e6:.0f}M, "
      f"${cap_stamp.min()/1e6:.0f}M-${cap_stamp.max()/1e6:.0f}M)")
    sh_file = u["shares"].reindex(shares_eff.index).dropna()
    ratio = (shares_eff.reindex(sh_file.index) / sh_file).dropna()
    P(f"G2    shares_eff = mktcap/px(last) vs the file's own `shares` column, n={len(ratio)}: "
      f"median ratio {ratio.median():.4f}, IQR [{ratio.quantile(.25):.4f}, {ratio.quantile(.75):.4f}]")
    P("      (ratio != 1 is the dividend/split adjustment of the panel's prices; CAP's RANKING "
      "at the LATE stamp is mktcap's by construction, so the gate below is exact.)")
    cap_last = first_last_valid(raws["CAP"])[1]
    g1a = float((cap_last.rank() - cap_stamp.reindex(cap_last.index).rank()).abs().max())
    P(f"G1a   max |rank(CAP at LATE stamp) - rank(mktcap_2026)| = {g1a:.2e}  "
      f"(0 => CAP/LATE IS idea 51's capQ)")

    # ---------------------------------------------------------------- main panel books
    P("\n" + "=" * 112)
    P("Q1  DECILE LADDERS — 2 keys x 3 stamps x 10 deciles x 3 arms = 180 books (MAIN panel)")
    P("=" * 112)
    store: dict = {}
    D = run_panel(px, cols, "MAIN", raws, e_all, ma_all, start, spy, b2, store)
    P(f"  main panel done ({time.time()-t0:.0f}s)")

    # ---- G1b reproduction against idea 424's committed deciles (advQ-DYNAMIC == ADV/DYN)
    ref = OUT / "2026-09-08_re-scope-idea-313-advQ-carries-a-price-LEVEL_cloud.deciles.csv"
    if ref.exists():
        R = pd.read_csv(ref)
        R = R[(R.key == "advQ") & (R.membership == "DYNAMIC")][["decile", "arm", "Sharpe", "CAGR"]]
        M = D[(D.key == "ADV") & (D.stamp == "DYN")][["decile", "arm", "Sharpe", "CAGR"]]
        j = R.merge(M, on=["decile", "arm"], suffixes=("_ref", "_new"))
        P(f"\nG1b   ADV/DYN vs idea 424 advQ-DYNAMIC on {len(j)} rows: "
          f"max|dSharpe| {np.abs(j.Sharpe_ref-j.Sharpe_new).max():.3e}, "
          f"max|dCAGR| {np.abs(j.CAGR_ref-j.CAGR_new).max():.3e}")
        Rc = pd.read_csv(ref)
        Rc = Rc[(Rc.key == "capQ")][["decile", "arm", "Sharpe", "CAGR"]]
        Mc = D[(D.key == "CAP") & (D.stamp == "LATE")][["decile", "arm", "Sharpe", "CAGR"]]
        jc = Rc.merge(Mc, on=["decile", "arm"], suffixes=("_ref", "_new"))
        P(f"G1a2  CAP/LATE vs idea 424 capQ-STATIC on {len(jc)} rows: "
          f"max|dSharpe| {np.abs(jc.Sharpe_ref-jc.Sharpe_new).max():.3e}, "
          f"max|dCAGR| {np.abs(jc.CAGR_ref-jc.CAGR_new).max():.3e}")

    # ---------------------------------------------------------------- Q2 slopes
    P("\n" + "=" * 112)
    P("Q2  THE SIGN GAP, FULL / IS / OOS   rho(decile, dSharpe vs EWall), n=10, SE ~ 0.354")
    P("=" * 112)
    P("    WHICH rho?  Idea 51 and idea 424 both compute np.corrcoef(decile, dSharpe) — a")
    P("    PEARSON correlation on 10 points — while their prose calls it Spearman.  BOTH are")
    P("    reported below; `rho_P` is the record's statistic and is what the gates reproduce.")
    STATS = ("dSharpe_vs_EWall", "dSharpeIS_vs_EWall", "dSharpeOOS_vs_EWall")
    S = pd.concat([slope_table(D, "MAIN", c, method=m) for c in STATS
                   for m in ("pearson", "spearman")], ignore_index=True)

    # ---- G1c: the record's two headline slopes, reproduced under its own statistic
    g1c_cap = rho_of(S, "MAIN", "CAP", "LATE", "MA-DG", "dSharpe_vs_EWall")
    g1c_adv = rho_of(S, "MAIN", "ADV", "DYN", "MA-RS", "dSharpe_vs_EWall")
    P(f"\nG1c   idea 51 published capQ MA-DG -0.336/-0.335 and advQ-D MA-RS +0.335.")
    P(f"      this run, PEARSON:  CAP/LATE MA-DG {g1c_cap:+.4f}   ADV/DYN MA-RS {g1c_adv:+.4f}")
    P(f"      this run, SPEARMAN: CAP/LATE MA-DG "
      f"{rho_of(S,'MAIN','CAP','LATE','MA-DG','dSharpe_vs_EWall','spearman'):+.4f}   "
      f"ADV/DYN MA-RS {rho_of(S,'MAIN','ADV','DYN','MA-RS','dSharpe_vs_EWall','spearman'):+.4f}")

    P(f"\n{'key':4s} {'stamp':6s} {'arm':6s} | {'rho_P':>7s} {'t':>6s} {'rho_S':>7s} |"
      f" {'IS_P':>7s} {'t':>6s} | {'OOS_P':>7s} {'t':>6s}")
    for key in KEYS:
        for stamp in STAMPS:
            for arm in ("MA-RS", "MA-DG"):
                g = lambda c, m="pearson": S[(S.panel == "MAIN") & (S.key == key)
                                             & (S.stamp == stamp) & (S.arm == arm)
                                             & (S.stat == c) & (S.method == m)]
                a, b, c_ = g(STATS[0]), g(STATS[1]), g(STATS[2])
                sp = g(STATS[0], "spearman")
                P(f"{key:4s} {stamp:6s} {arm:6s} | {a.rho.iloc[0]:+7.3f} {a.t.iloc[0]:+6.2f} "
                  f"{sp.rho.iloc[0]:+7.3f} | {b.rho.iloc[0]:+7.3f} {b.t.iloc[0]:+6.2f} |"
                  f" {c_.rho.iloc[0]:+7.3f} {c_.t.iloc[0]:+6.2f}")

    # ---- PEARSON vs SPEARMAN: how much of the published slope is decile 1's magnitude?
    P("\n  PEARSON minus SPEARMAN per scheme (full sample) — a large gap means the published")
    P("  slope is carried by the SIZE of one decile's dSharpe, not by the ladder's ordering:")
    ps_rows = []
    for key in KEYS:
        for stamp in STAMPS:
            for arm in ("MA-RS", "MA-DG"):
                rp = rho_of(S, "MAIN", key, stamp, arm, STATS[0])
                rs = rho_of(S, "MAIN", key, stamp, arm, STATS[0], "spearman")
                P(f"    {key:4s} {stamp:6s} {arm:6s}  P {rp:+.3f}  S {rs:+.3f}  P-S {rp-rs:+.3f}")
                ps_rows.append(dict(key=key, stamp=stamp, arm=arm, rho_P=rp, rho_S=rs,
                                    gap=rp - rs))
    PS = pd.DataFrame(ps_rows)
    P(f"    mean |P - S| over the 12 schemes: {PS.gap.abs().mean():.3f}; "
      f"sign disagreement in {int((np.sign(PS.rho_P) != np.sign(PS.rho_S)).sum())}/12")

    # ---- the two decomposition paths (on the record's own PEARSON statistic)
    P("\n  DECOMPOSITION of idea 51's gap  rho_P(ADV,DYN) - rho_P(CAP,LATE), per arm:")
    dec_rows = []
    for arm in ("MA-RS", "MA-DG"):
        r = {(k, st): rho_of(S, "MAIN", k, st, arm, STATS[0]) for k in KEYS for st in STAMPS}
        gap = r[("ADV", "DYN")] - r[("CAP", "LATE")]
        aA = r[("CAP", "DYN")] - r[("CAP", "LATE")]      # stamp leg, held at CAP
        bA = r[("ADV", "DYN")] - r[("CAP", "DYN")]       # key leg, held at DYN
        aB = r[("ADV", "LATE")] - r[("CAP", "LATE")]     # key leg, held at LATE
        bB = r[("ADV", "DYN")] - r[("ADV", "LATE")]      # stamp leg, held at ADV
        P(f"    {arm:6s} gap {gap:+.3f} = pathA stamp {aA:+.3f} + key {bA:+.3f}"
          f"  = pathB key {aB:+.3f} + stamp {bB:+.3f}")
        dec_rows.append(dict(arm=arm, gap=gap, A_stamp=aA, A_key=bA, B_key=aB, B_stamp=bB,
                             interaction=gap - aA - bA))
    DEC = pd.DataFrame(dec_rows)
    P("    (pathA + pathB differ by the interaction; both are printed so neither is privileged.)")

    # ---------------------------------------------------------------- Q3 survivorship
    P("\n" + "=" * 112)
    P("Q3  SURVIVORSHIP — (i) drop decile 1,  (ii) FULLHIST sub-panel (no late entrants)")
    P("=" * 112)
    S_d210 = pd.concat([slope_table(D, "MAIN", "dSharpe_vs_EWall",
                                    deciles=range(2, NDEC + 1), method=m)
                        for m in ("pearson", "spearman")], ignore_index=True)
    S_d210["stat"] = "dSharpe_vs_EWall_d2to10"

    first_bar = px.index[0]
    fh = [c for c in cols if pd.notna(px[c].iloc[0])]
    P(f"  FULLHIST: {len(fh)}/{len(cols)} names priced on {first_bar.date()} (no late entrants)")
    pxf = px[fh + ["SPY"]]
    e_f = pxf.notna(); e_f["SPY"] = False
    ma_f = (pxf > pxf.rolling(MA_WIN).mean()) & e_f
    rawf = {k: v[[c for c in v.columns if c in fh]] for k, v in raws.items()}
    ctrl_f = backtest(pxf, _ew(e_f, PIN_G), cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
    mf = metrics(ctrl_f)
    P(f"  FULLHIST whole-panel EWall control: CAGR {mf['CAGR']:.2%} Sharpe {mf['Sharpe']:.3f} "
      f"MaxDD {mf['MaxDD']:.2%}  (MAIN control {metrics(ctrl)['CAGR']:.2%} / "
      f"{metrics(ctrl)['Sharpe']:.3f} / {metrics(ctrl)['MaxDD']:.2%})")
    DF = run_panel(pxf, fh, "FULLHIST", rawf, e_f, ma_f, start, spy, b2)
    D = pd.concat([D, DF], ignore_index=True)
    S_fh = pd.concat([slope_table(D, "FULLHIST", c, method=m) for c in STATS
                      for m in ("pearson", "spearman")], ignore_index=True)
    S = pd.concat([S, S_d210, S_fh], ignore_index=True)

    P(f"\n  rho_P(decile, dSharpe) FULL sample, three readings (Spearman in brackets):")
    P(f"{'key':4s} {'stamp':6s} {'arm':6s} | {'MAIN':>16s} {'d2-10':>16s} {'FULLHIST':>16s}")
    for key in KEYS:
        for stamp in STAMPS:
            for arm in ("MA-RS", "MA-DG"):
                cells = []
                for panel, st in (("MAIN", STATS[0]), ("MAIN", "dSharpe_vs_EWall_d2to10"),
                                  ("FULLHIST", STATS[0])):
                    cells.append(f"{rho_of(S,panel,key,stamp,arm,st):+7.3f}"
                                 f"[{rho_of(S,panel,key,stamp,arm,st,'spearman'):+6.3f}]")
                P(f"{key:4s} {stamp:6s} {arm:6s} | " + " ".join(cells))
    for arm in ("MA-RS", "MA-DG"):
        def gp(panel, st):
            return (rho_of(S, panel, "ADV", "DYN", arm, st)
                    - rho_of(S, panel, "CAP", "LATE", arm, st))
        P(f"    gap({arm}) MAIN {gp('MAIN', STATS[0]):+.3f}  "
          f"d2-10 {gp('MAIN','dSharpe_vs_EWall_d2to10'):+.3f}  "
          f"FULLHIST {gp('FULLHIST', STATS[0]):+.3f}")

    # ---------------------------------------------------------------- Q4 bootstrap
    P("\n" + "=" * 112)
    P(f"Q4  PAIRED CALENDAR-YEAR BLOCK BOOTSTRAP ({NBOOT} draws, seed {SEED}) — MAIN panel")
    P("=" * 112)
    idx = next(iter(store.values())).index
    years = np.array(sorted(set(idx.year)))
    ypos = {y: np.where(idx.year == y)[0] for y in years}
    mat = {k: v.values for k, v in store.items()}
    rng = np.random.default_rng(SEED)
    draws = [np.concatenate([ypos[y] for y in rng.choice(years, len(years), replace=True)])
             for _ in range(NBOOT)]

    def sharpe_np(a):
        s = a.std()
        return a.mean() * 252 / (s * np.sqrt(252)) if s > 0 else np.nan

    BARMS = ("MA-RS", "MA-DG")          # EWall's dSharpe vs itself is identically 0 -> rho undefined
    boot = {}
    for key in KEYS:
        for stamp in STAMPS:
            for arm in BARMS:
                out = np.empty(NBOOT)
                for j, sel in enumerate(draws):
                    ds = np.array([sharpe_np(mat[(key, stamp, d, arm)][sel])
                                   - sharpe_np(mat[(key, stamp, d, "EWall")][sel])
                                   for d in range(1, NDEC + 1)])
                    out[j] = rho_t(np.arange(1, NDEC + 1), ds)[0]
                boot[(key, stamp, arm)] = out
        P(f"    bootstrap {key} done ({time.time()-t0:.0f}s)")

    brows = []
    P(f"\n  per-scheme rho: point, bootstrap mean, 5%, 95%, P(rho>0)   (treatment arms only)")
    for key in KEYS:
        for stamp in STAMPS:
            for arm in BARMS:
                v = boot[(key, stamp, arm)]; v = v[np.isfinite(v)]
                pt = rho_of(S, "MAIN", key, stamp, arm, "dSharpe_vs_EWall")
                P(f"    {key:4s} {stamp:6s} {arm:6s} {pt:+.3f} | {v.mean():+.3f} "
                  f"[{np.percentile(v,5):+.3f}, {np.percentile(v,95):+.3f}]  P {(v>0).mean():.3f}")
                brows.append(dict(kind="rho", key=key, stamp=stamp, arm=arm, point=pt,
                                  boot_mean=v.mean(), p5=np.percentile(v, 5),
                                  p95=np.percentile(v, 95), p_pos=(v > 0).mean()))
    P(f"\n  the GAP to (CAP,LATE), paired per draw:")
    for arm in BARMS:
        base = boot[("CAP", "LATE", arm)]
        for key in KEYS:
            for stamp in STAMPS:
                if (key, stamp) == ("CAP", "LATE"): continue
                v = boot[(key, stamp, arm)] - base
                v = v[np.isfinite(v)]
                sgn = np.mean(np.sign(boot[(key, stamp, arm)]) != np.sign(base))
                P(f"    {arm:6s} {key}/{stamp:5s} - CAP/LATE  gap {v.mean():+.3f} "
                  f"[{np.percentile(v,5):+.3f}, {np.percentile(v,95):+.3f}]  "
                  f"P(gap>0) {(v>0).mean():.3f}  P(signs differ) {sgn:.3f}")
                brows.append(dict(kind="gap", key=key, stamp=stamp, arm=arm, point=np.nan,
                                  boot_mean=v.mean(), p5=np.percentile(v, 5),
                                  p95=np.percentile(v, 95), p_pos=(v > 0).mean(),
                                  p_sign_differs=sgn))
    B = pd.DataFrame(brows)

    # ---------------------------------------------------------------- Q5 rule 8 pick
    P("\n" + "=" * 112)
    P("Q5  RULE 8 W2 — decile chosen by best IS (2010-2016) EWall Sharpe; OOS read once")
    P("=" * 112)
    mo_spy, mo_b2, mo_ct = (metrics(x.loc[OOS_START:]) for x in (spy, b2, ctrl))
    P(f"  OOS references: SPY {mo_spy['Sharpe']:.3f}/{mo_spy['CAGR']:.2%}/{mo_spy['MaxDD']:.2%};"
      f"  RULES v2 {mo_b2['Sharpe']:.3f}/{mo_b2['CAGR']:.2%}/{mo_b2['MaxDD']:.2%};"
      f"  EWall ctrl {mo_ct['Sharpe']:.3f}/{mo_ct['CAGR']:.2%}/{mo_ct['MaxDD']:.2%}")
    wrows = []
    for panel in ("MAIN", "FULLHIST"):
        for key in KEYS:
            for stamp in STAMPS:
                s = D[(D.panel == panel) & (D.key == key) & (D.stamp == stamp) & (D.arm == "EWall")]
                pick = int(s.loc[s.IS_Sharpe.idxmax(), "decile"])
                q = s[s.decile == pick].iloc[0]
                P(f"  {panel:8s} {key}/{stamp:5s} pick d{pick:<2d} IS Sh {q.IS_Sharpe:5.3f} | "
                  f"OOS CAGR {q.OOS_CAGR:7.2%} Sh {q.OOS_Sharpe:6.3f} DD {q.OOS_MaxDD:7.2%} | "
                  f"vsSPY {q.OOS_Sharpe-mo_spy['Sharpe']:+.3f} vsV2 {q.OOS_Sharpe-mo_b2['Sharpe']:+.3f} "
                  f"vsCTRL {q.OOS_Sharpe-mo_ct['Sharpe']:+.3f}")
                wrows.append(dict(panel=panel, key=key, stamp=stamp, pick=pick,
                                  IS_Sharpe=q.IS_Sharpe, OOS_CAGR=q.OOS_CAGR,
                                  OOS_Sharpe=q.OOS_Sharpe, OOS_MaxDD=q.OOS_MaxDD,
                                  d_vs_SPY=q.OOS_Sharpe - mo_spy["Sharpe"],
                                  d_vs_v2=q.OOS_Sharpe - mo_b2["Sharpe"],
                                  d_vs_ctrl=q.OOS_Sharpe - mo_ct["Sharpe"]))
    W = pd.DataFrame(wrows)
    P("  NOTE: a pick landing on decile 1 is the thinnest, least-liquid tenth of a "
      "CURRENT-CONSTITUENT small-cap screen — a survivorship measurement, not an edge.")

    # ---- W1 sign-hold count
    hold = 0; tot = 0; posIS = 0; negOOS = 0
    for panel in ("MAIN", "FULLHIST"):
        for key in KEYS:
            for stamp in STAMPS:
                for arm in ("MA-RS", "MA-DG"):
                    a = rho_of(S, panel, key, stamp, arm, "dSharpeIS_vs_EWall")
                    b = rho_of(S, panel, key, stamp, arm, "dSharpeOOS_vs_EWall")
                    tot += 1; hold += int(np.sign(a) == np.sign(b))
                    posIS += int(a > 0); negOOS += int(b < 0)
    P(f"\n  W1 SIGN-HOLD across the rule-8 boundary: {hold}/{tot} (panel,key,stamp,arm) slopes "
      f"keep their sign IS -> OOS;  rho_IS > 0 in {posIS}/{tot}, rho_OOS < 0 in {negOOS}/{tot}")

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 112)
    P("Q6  KEEP PATHS over all books")
    P("=" * 112)
    for panel in ("MAIN", "FULLHIST"):
        s = D[D.panel == panel]
        P(f"  {panel:8s} 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}   "
          f"BOTH {int((s.keep4a & s.keep4b).sum())}/{len(s)}")
    tot4a, tot4b = int(D.keep4a.sum()), int(D.keep4b.sum())
    P(f"  TOTAL    4a {tot4a}/{len(D)}   4b {tot4b}/{len(D)}   "
      f"BOTH {int((D.keep4a & D.keep4b).sum())}/{len(D)}")
    if tot4a:
        P("  4a passers: " + ", ".join(
            f"{r.panel}/{r.key}/{r.stamp}/d{r.decile}/{r.arm}"
            for r in D[D.keep4a].itertuples()))
    if tot4b:
        P("  4b passers: " + ", ".join(
            f"{r.panel}/{r.key}/{r.stamp}/d{r.decile}/{r.arm}"
            for r in D[D.keep4b].itertuples()))

    # ---------------------------------------------------------------- write
    D.to_csv(OUT / f"{STAMP}.deciles.csv", index=False)
    S.to_csv(OUT / f"{STAMP}.slopes.csv", index=False)
    B.to_csv(OUT / f"{STAMP}.bootstrap.csv", index=False)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    DEC.to_csv(OUT / f"{STAMP}.surv.csv", index=False)
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
    P(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
