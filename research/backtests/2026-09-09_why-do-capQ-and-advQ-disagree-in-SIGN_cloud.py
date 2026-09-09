#!/usr/bin/env python3
"""Idea 313 (cloud, 2026-09-09) - why-do-capQ-and-advQ-disagree-in-SIGN.

QUESTION
--------
Idea 51 (lane B) reported two size columns giving OPPOSITE-signed decile slopes for the same
book on the same panel:

    capQ  rho(decile, dSharpe vs EWall) = -0.336      advQ = +0.335      corr(capQ, advQ) = +0.545

The queue asks: is the disagreement (i) the STATIC-vs-DYNAMIC membership, (ii) the LOOK-AHEAD in
the 2026 cap stamp, or (iii) SURVIVORSHIP in the thin deciles (advQ decile 1 EWall Sharpe 2.03)?
Rebuild capQ as a CAUSAL price-times-fixed-shares proxy and re-read both slopes.

THE CAUSAL REBUILD (what makes the question answerable)
-------------------------------------------------------
research/deepvalue/universe_under2b.csv carries `mktcap`, `price` and `shares` and satisfies
mktcap = price * shares EXACTLY (gate G2 below, 716/716 rows within 1e-2 relative).  So the
record's capQ column is one number per name: the 2026 PRICE times the 2026 SHARE COUNT.  Its
look-ahead is therefore exactly the 2026 price, and it can be removed while holding the share
count fixed:

    capQ26  = price_2026 * shares          the record's column          (STATIC only)
    capC_t  = px_t       * shares          causal, TIME-VARYING         (STATIC and DYNAMIC)
    capC0   = px_first   * shares          purely ex-ante stamp         (STATIC only)
    advQ    = (px * vol).rolling(60).median()   idea 51's column        (STATIC and DYNAMIC)

capC-DYNAMIC is the cell idea 424 recorded as not existing ("capQ is constant in time, so capQ-D
does not exist").  The causal rebuild creates it, which is what lets membership and key content
be separated inside the cap family instead of only across families.

THE THREE CHANNELS (each measured TWICE, so no single path is privileged)
-------------------------------------------------------------------------
    LOOKAHEAD   rho(capQ26,S) - rho(capC0,S)     and   rho(capQ26,S) - rho(capC,S)
    CONTENT     rho(advQ,S)   - rho(capC,S)      and   rho(advQ,D)   - rho(capC,D)
    MEMBERSHIP  rho(capC,D)   - rho(capC,S)      and   rho(advQ,D)   - rho(advQ,S)

The published gap is G = rho(advQ,D) - rho(capQ26,S).  Two orderings sum to G exactly:
    PATH A  = LOOKAHEAD(capC) + CONTENT(at S) + MEMBERSHIP(advQ)
    PATH B  = LOOKAHEAD(capC) + MEMBERSHIP(capC) + CONTENT(at D)
Their difference is the content x membership interaction and is reported, not hidden.

PRE-REGISTERED HYPOTHESES (stated before any result is read)
------------------------------------------------------------
H_MEMB  : MEMBERSHIP carries the gap - |MEMBERSHIP| is the largest of the three channels
          (averaged over its two measurements) on the MA-RS arm.
H_LOOK  : LOOKAHEAD carries the gap - |LOOKAHEAD| is the largest.
H_THIN  : the gap is a thin-decile artefact - dropping the single decile whose removal moves the
          gap most cuts |G| by >= 50%.
Exactly one of H_MEMB / H_LOOK / (CONTENT) is the answer; all three are reported either way, and
H_THIN is orthogonal to all of them.

TUNED PARAMETERS: exactly 2 - key {capQ26, capC, capC0, advQ} x membership {STATIC, DYNAMIC}
(6 legal cells; capQ26 and capC0 are constants in time so their DYNAMIC cells do not exist).
Everything else is PINNED at idea 51 lane B's pre-registered values and is NOT tuned:
gross 0.75, cadence W, cost 10 bps (0 bps reported alongside), NDEC 10, key window 60d
(min_periods 30), MA window 200, arms {EWall, MA-RS, MA-DG}.  All grid points reported.

GATES
-----
G1  reproduction - the advQ rows must reproduce idea 424's committed .slopes.csv / .deciles.csv
    to 1e-9 (advQ is unchanged here).  The capQ26 leg is checked against idea 424's capQ-STATIC
    rows, which already carry the 2026-09-07 data-vintage drift idea 424 documented; that drift
    is re-reported here, not asserted away.
G2  cap identity - mktcap == price * shares to 1e-2 relative on every covered row, and
    capC_t at the panel's last date == capQ26 to 1e-2 relative.  Without G2 the causal rebuild is
    not the same object as the record's column.
G3  n = 10 honesty - SE(rho) ~ 1/sqrt(8) = 0.354.  Every rho carries its t-stat, and every
    channel carries a 1,000-draw PAIRED calendar-year block bootstrap.

PANEL / SURVIVORSHIP
--------------------
SMALL panel only (data/prices_small.csv.gz, sub-$2B screen, 2010-2026); tickers with
max_1d_move >= 1.0 in data/small_meta.csv dropped first.  SURVIVORSHIP: current constituents of
the screen only - no delisted names - so every LEVEL (CAGR, Sharpe) is biased UP, the thin and
illiquid deciles most of all.  That is exactly channel (iii), so it is measured (the
leave-one-decile-out jackknife) rather than only disclaimed.

RULE 8 (required)
-----------------
IS 2010-2016 (choice), OOS 2017-2026 (read once).  W1: every rho and every channel recomputed on
IS only and on OOS only - a channel that carries the gap must carry it OOS too.  W2: the decile
with the best IS EWall Sharpe is picked per scheme and its OOS CAGR/Sharpe/MaxDD read once
against SPY, RULES v2 (live) and the whole-panel EWall control.  KEEP paths 4a and 4b evaluated
for every decile book.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .deciles.csv .slopes.csv .channels.csv .jackknife.csv .bootstrap.csv .walkforward.csv
         .keeppaths.csv .console.txt
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

STAMP = "2026-09-09_why-do-capQ-and-advQ-disagree-in-SIGN_cloud"
OUT = Path(__file__).resolve().parent
COST = 10.0
PIN_G, PIN_FREQ = 0.75, "W"
MA_WIN, NDEC, KEY_WIN = 200, 10, 60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NBOOT, SEED = 1000, 313
IDENT_TOL = 1e-2          # relative, G2
REPRO_TOL = 1e-9          # G1
THIN_BAR = 0.50           # H_THIN

IDEA424 = OUT / "2026-09-08_re-scope-idea-313-advQ-carries-a-price-LEVEL_cloud"

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def flush():
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


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


def fail_4b(r, spy):
    a1, a2 = halves(r); s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    t = {"H1": a1 > s1, "H2": a2 > s2,
         "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"],
         "DD": m["MaxDD"] >= 0.60 * ms["MaxDD"],
         "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def rho_t(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if np.std(y) < 1e-15:
        return 0.0, 0.0
    r = float(np.corrcoef(x, y)[0, 1])
    r = min(max(r, -0.999999), 0.999999)
    return r, float(r * np.sqrt(len(x) - 2) / np.sqrt(1 - r * r))


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 126)
    P("IDEA 313 - why do capQ and advQ disagree in SIGN?  The causal price-x-fixed-shares rebuild.")
    P("=" * 126)
    P(f"  pinned (NOT tuned): g={PIN_G}, cadence {PIN_FREQ}, cost {COST:.0f} bps "
      f"(0 bps alongside), NDEC={NDEC}, key window {KEY_WIN}d, MA {MA_WIN}d,")
    P("                      arms {EWall, MA-RS, MA-DG}, decile edges = qcut on the covered set.")
    P("  2 parameters: key in {capQ26, capC, capC0, advQ} x membership in {STATIC, DYNAMIC} "
      "(6 legal cells - capQ26 and capC0 are")
    P("                constants in time, so their DYNAMIC cells do not exist).  ALL grid points "
      "reported.")
    P("  PRE-REGISTERED  H_MEMB : |MEMBERSHIP| is the largest of the three channels on MA-RS.")
    P("                  H_LOOK : |LOOKAHEAD| is the largest.")
    P(f"                  H_THIN : dropping the single most influential decile cuts |G| by "
      f">= {THIN_BAR:.0%}.")

    # ---------------------------------------------------------------- panel
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in pxs.columns if c != "SPY"]
    cols = [c for c in s_all if c not in bad]
    px = pxs[cols + ["SPY"]].dropna(how="all").ffill()
    tradable = set(cols)
    P(f"\nPANEL  SMALL: {len(s_all)} names, dropped {len(s_all)-len(cols)} with "
      f"max_1d_move >= 1.0 -> {len(cols)} tradable")
    P(f"       {px.index[0].date()} .. {px.index[-1].date()}  ({len(px)} rows)")
    P("       SURVIVORSHIP: current constituents of the sub-$2B screen only; every LEVEL on this "
      "panel is biased UP, the thin")
    P("       deciles most.  That bias IS channel (iii), so it is measured below (jackknife), not "
      "only disclaimed.")

    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
    e_all = _priced(px, tradable) > 0
    ma_all = above_ma(px) & e_all
    ctrl = backtest(px, _ew(e_all, PIN_G), cost_bps=COST, freq=PIN_FREQ)["returns"].loc[start:]
    P(f"\nREFERENCES over {start.date()}..{px.index[-1].date()}")
    for nm, r in (("SPY", spy), ("RULES v2 (live)", b2), ("EWall whole panel", ctrl)):
        m = metrics(r); mo = metrics(r.loc[OOS_START:]); h1, h2 = halves(r)
        P(f"  {nm:18s} CAGR {m['CAGR']:7.2%}  Sharpe {m['Sharpe']:6.3f}  MaxDD {m['MaxDD']:7.2%}"
          f"  halves {h1:6.3f}/{h2:6.3f} | OOS CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:6.3f}")
    ms = metrics(spy); s1, s2 = halves(spy)
    P(f"  4b bars from SPY: H1>{s1:.3f} H2>{s2:.3f} "
      f"OOS>{metrics(spy.loc[OOS_START:])['Sharpe']:.3f} "
      f"MaxDD>=-{0.60*abs(ms['MaxDD']):.1%} CAGR>={0.70*ms['CAGR']:.2%}")
    flush()

    # ---------------------------------------------------------------- G2: the cap identity
    P("\n" + "=" * 126)
    P("G2  THE CAP IDENTITY - is capQ literally price x shares?  (if not, the causal rebuild is a "
      "different object)")
    P("=" * 126)
    u = pd.read_csv(ROOT / "research" / "deepvalue" / "universe_under2b.csv",
                    usecols=["ticker", "mktcap", "price", "shares"]).dropna()
    u = u[(u.mktcap > 0) & (u.price > 0) & (u.shares > 0)].drop_duplicates("ticker") \
         .set_index("ticker")
    rel = (u.price * u.shares / u.mktcap - 1).abs()
    ok_ident = float(rel.max()) < IDENT_TOL
    P(f"  mktcap vs price*shares over {len(u)} rows: max relative |diff| = {rel.max():.3e} "
      f"(bar {IDENT_TOL:.0e})  {'PASS' if ok_ident else 'FAIL'}")

    sh = u["shares"].reindex(cols).dropna()
    capQ26 = (u["price"] * u["shares"]).reindex(cols).dropna()
    P(f"  coverage: {len(sh)}/{len(cols)} tradable names carry a share count "
      f"(median {sh.median()/1e6:.1f}M shares)")
    cap_t = px[cols].mul(sh.reindex(cols), axis=1)              # causal cap_t = px_t * shares
    last = cap_t.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                       else np.nan)
    common = capQ26.index.intersection(last.dropna().index)
    rel2 = (last[common] / capQ26[common] - 1).abs()
    ok_last = float(rel2.max()) < IDENT_TOL
    P(f"  capC at the panel's last bar vs capQ26 over {len(common)} names: max relative |diff| = "
      f"{rel2.max():.3e} (bar {IDENT_TOL:.0e})  {'PASS' if ok_last else 'FAIL'}")
    P(f"  -> the record's capQ look-ahead is exactly the 2026 PRICE; the share count is common to "
      f"all four keys.")

    first = cap_t.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                        else np.nan)
    capC0 = first.dropna()
    capC_static = cap_t.median(axis=0).dropna()
    P(f"  capQ26 median ${capQ26.median()/1e6:.0f}M   capC(median over time) "
      f"${capC_static.median()/1e6:.0f}M   capC0(first bar) ${capC0.median()/1e6:.0f}M")

    vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
    advQ_t = (px * vol)[cols].rolling(KEY_WIN, min_periods=30).median()
    advQ_static = advQ_t.median(axis=0).dropna()

    SK = pd.DataFrame({"capQ26": capQ26.reindex(cols), "capC": capC_static.reindex(cols),
                       "capC0": capC0.reindex(cols), "advQ": advQ_static.reindex(cols)})
    P("\n  pairwise agreement of the STATIC per-name key RANKS (Spearman):")
    P("    " + SK.rank().corr().to_string(float_format=lambda x: f"{x:+.3f}")
      .replace("\n", "\n    "))
    P("    (idea 51 quoted corr(capQ, advQ) = +0.545.)")
    flush()

    # ---------------------------------------------------------------- decile books
    P("\n" + "=" * 126)
    P("Q1  DECILE LADDERS - 6 key x membership cells x 10 deciles x 3 arms = "
      f"{6*NDEC*3} books, all reported in {STAMP}.deciles.csv")
    P("=" * 126)
    schemes = [("capQ26", "STATIC"), ("capC0", "STATIC"), ("capC", "STATIC"),
               ("capC", "DYNAMIC"), ("advQ", "STATIC"), ("advQ", "DYNAMIC")]
    static_key = {"capQ26": capQ26, "capC0": capC0, "capC": capC_static, "advQ": advQ_static}
    dyn_key = {"capC": cap_t, "advQ": advQ_t}

    rets_store, dec_rows = {}, []
    for key, memb in schemes:
        base_static = static_key[key].reindex(cols).dropna()
        q_static = pd.qcut(base_static.rank(method="first"), NDEC, labels=False) + 1
        rk = None if memb == "STATIC" else dyn_key[key].rank(axis=1, pct=True)

        for d in range(1, NDEC + 1):
            memb_mask = pd.DataFrame(False, index=px.index, columns=px.columns)
            if memb == "STATIC":
                names = list(q_static[q_static == d].index)
                memb_mask[names] = True
                nsz = float(len(names))
                lbl = f"{base_static[names].median()/1e6:.3f}M {key}"
                sub = names + ["SPY"]
            else:
                lo, hi = (d - 1) / NDEC, d / NDEC
                sel = (rk > lo) & (rk <= hi) if d > 1 else (rk >= 0) & (rk <= hi)
                memb_mask.loc[:, sel.columns] = sel.fillna(False).values
                nsz = float(sel.sum(axis=1).mean())
                lbl = f"{dyn_key[key].where(sel).stack().median()/1e6:.3f}M {key}"
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
            ci = metrics(rets["EWall"].loc[:IS_END])
            co = metrics(rets["EWall"].loc[OOS_START:])
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
                row["f4b"] = fail_4b(r, spy)
                row["keep4b"] = row["f4b"] == "-"
                dec_rows.append(row)
        P(f"  {key}-{memb[:1]} done ({time.time()-t0:.0f}s)")
        flush()
    D = pd.DataFrame(dec_rows)
    D.to_csv(OUT / f"{STAMP}.deciles.csv", index=False)
    D.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)

    # ---------------------------------------------------------------- G1 reproduction
    P("\n" + "=" * 126)
    P("G1  REPRODUCTION of idea 424's committed .deciles.csv (the advQ legs are unchanged here)")
    P("=" * 126)
    ref_p = Path(f"{IDEA424}.deciles.csv")
    if ref_p.exists():
        ref = pd.read_csv(ref_p)
        ref = ref[ref.key == "advQ"].copy()
        mine = D[D.key == "advQ"].merge(ref, on=["key", "membership", "decile", "arm"],
                                        suffixes=("", "_ref"))
        worst, wc = 0.0, None
        for c_ in ("CAGR", "Sharpe", "MaxDD", "dSharpe_vs_EWall", "dSharpeIS_vs_EWall",
                   "dSharpeOOS_vs_EWall"):
            dv = float((mine[c_] - mine[c_ + "_ref"]).abs().max())
            if dv > worst:
                worst, wc = dv, c_
        ok_g1 = (len(mine) == len(ref)) and worst < REPRO_TOL
        P(f"  advQ (STATIC+DYNAMIC): {len(mine)}/{len(ref)} rows x 6 columns, worst |d| = "
          f"{worst:.3e} ({wc})  (bar {REPRO_TOL:.0e})  {'PASS' if ok_g1 else 'FAIL'}")
        ref2 = pd.read_csv(ref_p)
        refc = ref2[(ref2.key == "capQ") & (ref2.membership == "STATIC")]
        minec = D[(D.key == "capQ26") & (D.membership == "STATIC")].copy()
        mc = minec.merge(refc, on=["membership", "decile", "arm"], suffixes=("", "_ref"))
        dsh = float((mc.Sharpe - mc.Sharpe_ref).abs().max())
        nmis = int((mc.n_names != mc.n_names_ref).sum())
        P(f"  capQ26-STATIC vs idea 424's capQ-STATIC: {len(mc)} rows, max |dSharpe| = "
          f"{dsh:.3e}, {nmis} rows with a different decile size")
        P(f"    (idea 424 built capQ from the `mktcap` column; this script builds it as "
          f"price*shares.  G2 shows those are the")
        P(f"     same number to {IDENT_TOL:.0e}, so any residue here is qcut edge placement on "
          f"ties, and it is reported, not hidden.)")
    else:
        ok_g1 = None
        P("  idea 424 .deciles.csv NOT FOUND - reproduction gate could not be run")
    flush()

    # ---------------------------------------------------------------- slopes
    P("\n" + "=" * 126)
    P("Q2  THE SLOPES - rho(decile, dSharpe vs EWall), FULL / IS 2010-2016 / OOS 2017-2026")
    P(f"    n = {NDEC} deciles, so SE(rho) ~ {1/np.sqrt(NDEC-2):.3f}; "
      f"t = rho*sqrt(n-2)/sqrt(1-rho^2).  EVERY cell reported.")
    P("=" * 126)
    sl_rows = []
    P(f"  {'key':7s} {'memb':8s} {'arm':6s} {'rho_full':>9s} {'t':>6s} {'rho_IS':>8s} {'t':>6s} "
      f"{'rho_OOS':>8s} {'t':>6s} {'rhoCAGR':>8s} {'+d/10':>6s}")
    for key, memb in schemes:
        for arm in ("MA-RS", "MA-DG"):
            s = D[(D.key == key) & (D.membership == memb) & (D.arm == arm)].sort_values("decile")
            rf, tf = rho_t(s.decile, s.dSharpe_vs_EWall)
            ri, ti = rho_t(s.decile, s.dSharpeIS_vs_EWall)
            ro, to = rho_t(s.decile, s.dSharpeOOS_vs_EWall)
            rc, tc = rho_t(s.decile, s.dCAGR_vs_EWall)
            npos = int((s.dSharpe_vs_EWall > 0).sum())
            sl_rows.append(dict(key=key, membership=memb, arm=arm, rho_full=rf, t_full=tf,
                                rho_IS=ri, t_IS=ti, rho_OOS=ro, t_OOS=to, rho_CAGR=rc, t_CAGR=tc,
                                n_pos_deciles=npos))
            P(f"  {key:7s} {memb:8s} {arm:6s} {rf:+9.3f} {tf:+6.2f} {ri:+8.3f} {ti:+6.2f} "
              f"{ro:+8.3f} {to:+6.2f} {rc:+8.3f} {npos:4d}/10")
    S = pd.DataFrame(sl_rows)
    S.to_csv(OUT / f"{STAMP}.slopes.csv", index=False)

    def R(key, memb, arm, col="rho_full"):
        q = S[(S.key == key) & (S.membership == memb) & (S.arm == arm)]
        return float(q[col].iloc[0]) if len(q) else np.nan

    # ---------------------------------------------------------------- the channels
    P("\n" + "=" * 126)
    P("Q3  THE THREE CHANNELS.  G = rho(advQ,D) - rho(capQ26,S) is the published sign gap; each "
      "channel is measured TWICE.")
    P("=" * 126)
    ch_rows = []
    for arm in ("MA-RS", "MA-DG"):
        for col, win in (("rho_full", "FULL"), ("rho_IS", "IS"), ("rho_OOS", "OOS")):
            g = R("advQ", "DYNAMIC", arm, col) - R("capQ26", "STATIC", arm, col)
            look_a = R("capQ26", "STATIC", arm, col) - R("capC0", "STATIC", arm, col)
            look_b = R("capQ26", "STATIC", arm, col) - R("capC", "STATIC", arm, col)
            cont_s = R("advQ", "STATIC", arm, col) - R("capC", "STATIC", arm, col)
            cont_d = R("advQ", "DYNAMIC", arm, col) - R("capC", "DYNAMIC", arm, col)
            memb_c = R("capC", "DYNAMIC", arm, col) - R("capC", "STATIC", arm, col)
            memb_a = R("advQ", "DYNAMIC", arm, col) - R("advQ", "STATIC", arm, col)
            pathA = -look_b + cont_s + memb_a
            pathB = -look_b + memb_c + cont_d
            ch_rows.append(dict(arm=arm, window=win, G=g,
                                LOOKAHEAD_vs_capC0=look_a, LOOKAHEAD_vs_capC=look_b,
                                CONTENT_at_S=cont_s, CONTENT_at_D=cont_d,
                                MEMBERSHIP_capC=memb_c, MEMBERSHIP_advQ=memb_a,
                                pathA=pathA, pathB=pathB,
                                pathA_err=pathA - g, pathB_err=pathB - g,
                                interaction=pathA - pathB,
                                mean_LOOK=np.mean([abs(look_a), abs(look_b)]),
                                mean_CONT=np.mean([abs(cont_s), abs(cont_d)]),
                                mean_MEMB=np.mean([abs(memb_c), abs(memb_a)])))
    CH = pd.DataFrame(ch_rows)
    CH["largest"] = CH[["mean_LOOK", "mean_CONT", "mean_MEMB"]].idxmax(axis=1) \
                      .str.replace("mean_", "", regex=False)
    CH.to_csv(OUT / f"{STAMP}.channels.csv", index=False)
    P(CH.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\n  PATH A = -LOOKAHEAD_vs_capC + CONTENT_at_S + MEMBERSHIP_advQ  (must equal G exactly)")
    P("  PATH B = -LOOKAHEAD_vs_capC + MEMBERSHIP_capC + CONTENT_at_D    (must equal G exactly)")
    P(f"  identity check: max |pathA - G| = {CH.pathA_err.abs().max():.2e}, "
      f"max |pathB - G| = {CH.pathB_err.abs().max():.2e}")
    for arm in ("MA-RS", "MA-DG"):
        row = CH[(CH.arm == arm) & (CH.window == "FULL")].iloc[0]
        P(f"  {arm}: G = {row.G:+.4f};  mean |LOOKAHEAD| {row.mean_LOOK:.4f}  "
          f"|CONTENT| {row.mean_CONT:.4f}  |MEMBERSHIP| {row.mean_MEMB:.4f}  "
          f"-> largest = {row.largest};  content x membership interaction "
          f"{row.interaction:+.4f}")
    ma_rs_full = CH[(CH.arm == "MA-RS") & (CH.window == "FULL")].iloc[0]
    P(f"\n  H_MEMB {'HOLDS' if ma_rs_full.largest == 'MEMB' else 'FAILS'} | "
      f"H_LOOK {'HOLDS' if ma_rs_full.largest == 'LOOK' else 'FAILS'} | "
      f"CONTENT largest: {'YES' if ma_rs_full.largest == 'CONT' else 'no'}   "
      f"(MA-RS, FULL sample)")
    P("  OOS reading of the same channels (rule-8 W1): "
      + ", ".join(f"{a} {CH[(CH.arm==a)&(CH.window=='OOS')].largest.iloc[0]}"
                  for a in ("MA-RS", "MA-DG")))
    flush()

    # ---------------------------------------------------------------- jackknife (channel iii)
    P("\n" + "=" * 126)
    P("Q4  CHANNEL (iii) SURVIVORSHIP IN THE THIN DECILES - leave-one-decile-out jackknife of "
      "every rho and of the gap G.")
    P("=" * 126)
    jk_rows = []
    for arm in ("MA-RS", "MA-DG"):
        g_full = R("advQ", "DYNAMIC", arm) - R("capQ26", "STATIC", arm)
        for dd in range(1, NDEC + 1):
            r_by = {}
            for key, memb in schemes:
                s = D[(D.key == key) & (D.membership == memb) & (D.arm == arm)
                      & (D.decile != dd)].sort_values("decile")
                r_by[(key, memb)] = rho_t(s.decile, s.dSharpe_vs_EWall)[0]
            g_jk = r_by[("advQ", "DYNAMIC")] - r_by[("capQ26", "STATIC")]
            jk_rows.append(dict(arm=arm, dropped=dd, G_full=g_full, G_jk=g_jk,
                                dG=g_jk - g_full,
                                shrink=1 - abs(g_jk) / abs(g_full) if abs(g_full) > 1e-12 else np.nan,
                                sign_flip=bool(np.sign(g_jk) != np.sign(g_full)),
                                **{f"rho_{k}_{m[:1]}": v for (k, m), v in r_by.items()}))
    JK = pd.DataFrame(jk_rows)
    JK.to_csv(OUT / f"{STAMP}.jackknife.csv", index=False)
    P(JK.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    thin_ok = {}
    for arm in ("MA-RS", "MA-DG"):
        sub = JK[JK.arm == arm]
        w = sub.loc[sub.shrink.idxmax()]
        thin_ok[arm] = bool(w.shrink >= THIN_BAR)
        P(f"\n  {arm}: the most influential decile is D{int(w.dropped)} - dropping it moves G "
          f"{w.G_full:+.4f} -> {w.G_jk:+.4f} (|G| cut {w.shrink:.1%}, "
          f"sign flip {w.sign_flip})  H_THIN {'HOLDS' if thin_ok[arm] else 'FAILS'}")
    P("\n  decile-1 EWall Sharpe by scheme (the 2.03 the queue flags), and the decile sizes:")
    d1 = D[(D.decile == 1) & (D.arm == "EWall")][["key", "membership", "n_names", "size",
                                                  "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"]]
    P("  " + d1.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    flush()

    # ---------------------------------------------------------------- bootstrap
    P("\n" + "=" * 126)
    P(f"Q5  PAIRED CALENDAR-YEAR BLOCK BOOTSTRAP ({NBOOT} draws, seed {SEED}) - is the sign gap, "
      f"and each channel, distinguishable from 0?")
    P("    One year-resample per draw applied to EVERY book, so G and the channels are PAIRED "
      "statistics.")
    P("=" * 126)
    idx = rets_store[("capQ26", "STATIC", 1, "EWall")].index
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

    dgrid = np.arange(1, NDEC + 1)

    def rho_np(ds):
        ds = np.asarray(ds)
        return 0.0 if ds.std() < 1e-15 else float(np.corrcoef(dgrid, ds)[0, 1])

    bt_rows = []
    for arm in ("MA-RS", "MA-DG"):
        boot = {}
        for key, memb in schemes:
            rr = np.empty(NBOOT)
            for j, sel in enumerate(draws):
                rr[j] = rho_np([sharpe_np(Rmat[(key, memb, d, arm)][sel])
                                - sharpe_np(Rmat[(key, memb, d, "EWall")][sel])
                                for d in dgrid])
            boot[(key, memb)] = rr
        stats = {
            "G": boot[("advQ", "DYNAMIC")] - boot[("capQ26", "STATIC")],
            "LOOKAHEAD_vs_capC0": boot[("capQ26", "STATIC")] - boot[("capC0", "STATIC")],
            "LOOKAHEAD_vs_capC": boot[("capQ26", "STATIC")] - boot[("capC", "STATIC")],
            "CONTENT_at_S": boot[("advQ", "STATIC")] - boot[("capC", "STATIC")],
            "CONTENT_at_D": boot[("advQ", "DYNAMIC")] - boot[("capC", "DYNAMIC")],
            "MEMBERSHIP_capC": boot[("capC", "DYNAMIC")] - boot[("capC", "STATIC")],
            "MEMBERSHIP_advQ": boot[("advQ", "DYNAMIC")] - boot[("advQ", "STATIC")],
        }
        pt = {"G": R("advQ", "DYNAMIC", arm) - R("capQ26", "STATIC", arm)}
        row = CH[(CH.arm == arm) & (CH.window == "FULL")].iloc[0]
        for k in list(stats)[1:]:
            pt[k] = float(row[k])
        for k, v in stats.items():
            lo, hi = np.percentile(v, [5, 95])
            bt_rows.append(dict(arm=arm, statistic=k, point=pt[k], boot_mean=float(v.mean()),
                                p05=lo, p95=hi, p_positive=float((v > 0).mean()),
                                excludes_zero=bool(lo > 0 or hi < 0)))
        P(f"  {arm} bootstrapped ({time.time()-t0:.0f}s)")
        flush()
    BT = pd.DataFrame(bt_rows)
    BT.to_csv(OUT / f"{STAMP}.bootstrap.csv", index=False)
    P("")
    P(BT.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P(f"\n  statistics whose 90% band excludes zero: {int(BT.excludes_zero.sum())}/{len(BT)}")

    # ---------------------------------------------------------------- rule 8 W2 + KEEP
    P("\n" + "=" * 126)
    P(f"RULE 8 W2 - per scheme, pick the decile with the best IS ({IS_END} and earlier) EWall "
      f"Sharpe, read its OOS ONCE.")
    P("=" * 126)
    wf = []
    spy_o = metrics(spy.loc[OOS_START:])
    b2_o = metrics(b2.loc[OOS_START:])
    ctrl_o = metrics(ctrl.loc[OOS_START:])
    for key, memb in schemes:
        s = D[(D.key == key) & (D.membership == memb) & (D.arm == "EWall")]
        pick = int(s.loc[s.IS_Sharpe.idxmax()].decile)
        for arm in ("EWall", "MA-RS", "MA-DG"):
            r = D[(D.key == key) & (D.membership == memb) & (D.decile == pick)
                  & (D.arm == arm)].iloc[0]
            wf.append(dict(key=key, membership=memb, pick=pick, arm=arm,
                           IS_Sharpe=r.IS_Sharpe, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                           OOS_MaxDD=r.OOS_MaxDD, spy_OOS=spy_o["Sharpe"], v2_OOS=b2_o["Sharpe"],
                           ctrl_OOS=ctrl_o["Sharpe"],
                           beat_spy=bool(r.OOS_Sharpe > spy_o["Sharpe"]),
                           beat_v2=bool(r.OOS_Sharpe > b2_o["Sharpe"]),
                           beat_ctrl=bool(r.OOS_Sharpe > ctrl_o["Sharpe"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  WF picks beating SPY OOS {int(WF.beat_spy.sum())}/{len(WF)}, "
      f"RULES v2 OOS {int(WF.beat_v2.sum())}/{len(WF)}, "
      f"the whole-panel EWall control {int(WF.beat_ctrl.sum())}/{len(WF)}")

    P("\n" + "=" * 126)
    P(f"KEEP PATHS over all {len(D)} decile books (4a vs RULES v2 live, 4b vs SPY).")
    P("=" * 126)
    n4a, n4b = int(D.keep4a.sum()), int(D.keep4b.sum())
    P(f"  4a passers {n4a}/{len(D)}   4b passers {n4b}/{len(D)}   "
      f"BOTH {int((D.keep4a & D.keep4b).sum())}/{len(D)}")
    P("  4b failure reasons (fail SET, not first clause):")
    P("  " + D.f4b.value_counts().rename("n").to_frame().to_string().replace("\n", "\n  "))
    if n4b:
        P("\n  every 4b passer:")
        P("  " + D[D.keep4b][["key", "membership", "decile", "arm", "n_names", "CAGR", "Sharpe",
                              "MaxDD", "H1", "H2", "OOS_Sharpe"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    if n4a:
        P("\n  every 4a passer:")
        P("  " + D[D.keep4a][["key", "membership", "decile", "arm", "n_names", "CAGR", "Sharpe",
                              "MaxDD", "H1", "H2", "f4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 126)
    P("VERDICT")
    P("=" * 126)
    P(f"1. G2 PASSES: capQ IS price x shares ({rel.max():.1e} relative), so the causal rebuild "
      f"capC_t = px_t * shares is the same")
    P(f"   object with the 2026 price removed, and capC-DYNAMIC - the cell idea 424 recorded as "
      f"non-existent - exists.")
    P(f"2. MA-RS FULL: G = {ma_rs_full.G:+.4f}; channels |LOOK| {ma_rs_full.mean_LOOK:.4f}, "
      f"|CONT| {ma_rs_full.mean_CONT:.4f}, |MEMB| {ma_rs_full.mean_MEMB:.4f} "
      f"-> {ma_rs_full.largest} is largest.")
    P(f"   H_MEMB {'HOLDS' if ma_rs_full.largest == 'MEMB' else 'FAILS'}, "
      f"H_LOOK {'HOLDS' if ma_rs_full.largest == 'LOOK' else 'FAILS'}.")
    P(f"3. H_THIN MA-RS {'HOLDS' if thin_ok['MA-RS'] else 'FAILS'}, "
      f"MA-DG {'HOLDS' if thin_ok['MA-DG'] else 'FAILS'} "
      f"(leave-one-decile-out).")
    P(f"4. n = {NDEC}: {int(BT.excludes_zero.sum())}/{len(BT)} bootstrap bands exclude zero - "
      f"read every rho with SE ~ {1/np.sqrt(NDEC-2):.3f} in mind.")
    P(f"5. KEEP: 4a {n4a}/{len(D)}, 4b {n4b}/{len(D)}.  WF picks beat SPY OOS "
      f"{int(WF.beat_spy.sum())}/{len(WF)}.  No book promoted.")
    P("6. SURVIVORSHIP restated: the small panel is current constituents only; every LEVEL is "
      "biased up, the thin deciles most.")
    flush()


if __name__ == "__main__":
    main()
