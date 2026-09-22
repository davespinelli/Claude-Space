#!/usr/bin/env python3
"""Idea 2077 (lane C, 2026-09-22): THE BAND BOOK'S FINANCING FRONTIER.

THE QUESTION.  Idea 2085 (lane B, this same day) found leverage on the live band book is
Sharpe-NEUTRAL (constant to 3dp across gross 0.75 -> 2.00) and that the 4b DD cap binds
around gross 1.25-1.5, but it modelled financing as a flat rate on borrowed gross and only
sampled {0, 3, 6}%/yr on one cell.  The whole levered case rests on an unpriced assumption:
gross > 1 is only free at 0%/yr.  This run prices the frontier.

  Q1  What is the BREAK-EVEN financing rate r* at which a levered cell's CAGR gain over the
      unlevered (gross 1.00) book is exactly eaten?  Per panel, per rung.  r* is MODEL-FREE:
      whatever anyone believes the funding path was, if r* sits below it the cell is dead.
  Q2  At each financing rung, what is the BREAK-EVEN GROSS g* -- the point on the ladder past
      which levering no longer pays?
  Q3  DOES ANY LEVERED CELL SURVIVE A REALISTIC BORROW COST ON THE 4b MARGIN?  (the idea's
      own headline question), under both KEEP paths, with rule 8, and against idea 914's
      offset-spread clause.

TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4): FIN MODEL and GROSS.
  FIN   {0%, 2%, 4%, 6%, 8%}/yr flat on borrowed gross, plus ONE time-varying proxy TV_SHY.
  GROSS {0.75, 1.00, 1.25, 1.50, 1.75, 2.00}.
  Band FIXED at the live 0.03, cadence FIXED weekly, cost FIXED at PROTOCOL's 10 bps.
  6 x 6 x 2 panels = 72 cells, ALL published (.grid.csv).

THE TIME-VARYING PROXY, AND ITS STATED BIAS.  The sandbox has no internet and the committed
caches carry NO clean bill instrument (no BIL, no SHV).  TV_SHY is therefore built from SHY
-- a committed constituent of BOTH panels -- as
        rate_t = clip(trailing 252d total return of SHY, 0, inf) + SPREAD(150 bps), lagged 1d.
Nothing is imported and no rate level is recalled from memory.  SHY carries ~1.9y of
duration, so this proxy UNDERSTATES funding exactly when rates rise: its 2022 reading is
NEGATIVE (-3.5%/yr trailing TR, floored to 0) against a funding rate that was climbing
through 4%.  It is published as a PATH-SHAPE experiment only; the FLAT ladder and the
model-free break-even r* carry the verdict.  Both are stated in the memo.

CONVENTION, STATED (B7).  The record's convention is that un-invested NAV earns 0%, which
flatters de-grossed books not at all and levered books not at all -- but it is asymmetric
once a borrow rate exists.  B7 re-verdicts the whole grid under a SYMMETRIC convention:
idle NAV earns (fin - SPREAD) floored at 0, borrowed NAV pays fin.  It is a reported
convention, never a tuned dial, and no pick is made on it.

Price-only on the committed caches (U56 = research/universe.json, B136 =
research/universe_broad.json).  No EDGAR / Form 4 / 8-K / options / live data.
SURVIVORSHIP: current constituents on both panels.

    python research/backtests/2026-09-22_lever-the-band-book-financing-frontier_C.py
"""
import sys, itertools, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, metrics, rebalance_mask          # noqa: E402

SLUG = Path(__file__).stem
OUT = Path(__file__).parent
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- fixed dials
BAND = 0.03            # live RULES v2
CADENCE = "W"          # live RULES v2
COST = 10              # PROTOCOL rule 2
SPREAD = 0.015         # broker spread over the short rate, STATED not fitted
WARM = 260
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
GROSS = [0.75, 1.00, 1.25, 1.50, 1.75, 2.00]
FLAT = [0.00, 0.02, 0.04, 0.06, 0.08]
FINMODELS = [f"FLAT{int(100*f)}" for f in FLAT] + ["TV_SHY"]
OFFSETS = [0, 1, 2, 3, 4]     # idea 914's clause: the book is ALWAYS read at d=0


# ------------------------------------------------------- engine-equivalent run
def offset_mask(idx, d, freq):
    """True d trading days BEFORE the last trading day of each period (d=0 == rebalance_mask)."""
    key = pd.Series(idx.to_period(freq), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out


def run(prices, weights, mask):
    """engine.backtest's loop, additionally returning the HELD GROSS path (needed to charge
    financing on the borrowed slice).  Costs are applied afterwards and never touch the path."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gr = np.empty(n); turn = np.zeros(n); held = np.empty(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur.sum()
        gr[i] = np.nansum(cur * rets[i])
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    ix = prices.index
    return pd.Series(gr, index=ix), pd.Series(turn, index=ix), pd.Series(held, index=ix)


def shy_rate(px):
    """TV_SHY: trailing 252d SHY total return, floored at 0, + SPREAD, lagged one day."""
    shy = px["SHY"]
    r = (shy / shy.shift(252) - 1).clip(lower=0.0) + SPREAD
    return r.shift(1).bfill()


def net(gr, turn, held, rate, cost_bps=COST, cash_yield=False):
    """Net daily return: gross - costs - financing on borrowed NAV (+ optional cash credit)."""
    r = gr - turn * cost_bps / 1e4
    borrowed = (held - 1.0).clip(lower=0.0)
    if isinstance(rate, pd.Series):
        rt = rate.reindex(r.index).fillna(0.0)
    else:
        rt = pd.Series(float(rate), index=r.index)
    r = r - borrowed * rt / 252.0
    if cash_yield:
        idle = (1.0 - held).clip(lower=0.0)
        r = r + idle * (rt - SPREAD).clip(lower=0.0) / 252.0
    return r


# ------------------------------------------------------------------- metrics
def met(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def v4a(m, base):
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves, MaxDD no worse."""
    return bool(m["H1"] > base["H1"] and m["H2"] > base["H2"] and m["MaxDD"] >= base["MaxDD"])


def v4b(m, ms):
    """PROTOCOL 4b: Sharpe > SPY both halves, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    legs = dict(sharpe=bool(m["H1"] > ms["H1"] and m["H2"] > ms["H2"]),
                dd=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                cagr=bool(m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(all(legs.values())), legs


def cagr_of(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    return eq.iloc[-1] ** (1 / yrs) - 1


def breakeven_rate(gr, turn, held, target_cagr, lo=0.0, hi=1.00, tol=1e-6):
    """Smallest flat financing rate at which the cell's CAGR falls to target_cagr.
    None if it is already below at 0%/yr, or still above at hi."""
    f = lambda x: cagr_of(net(gr, turn, held, x)) - target_cagr
    if f(lo) <= 0:
        return None            # never paid, even free
    if f(hi) > 0:
        return float("inf")    # unkillable on this ladder (no borrow at all, or a huge edge)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0: lo = mid
        else: hi = mid
        if hi - lo < tol: break
    return 0.5 * (lo + hi)


# ------------------------------------------------------------------ the panels
def build(px, name):
    """One run() per (gross, offset); financing is applied afterwards, so the 72-cell grid
    costs only 6 held-paths per panel."""
    P(f"\n{'='*86}\nPANEL {name}   {px.index[0].date()} -> {px.index[-1].date()}  ({px.shape[1]} cols)\n{'='*86}")
    paths = {}
    for g in GROSS:
        w = rules_v2_weights(px, band=BAND, gross=g)
        for d in OFFSETS:
            gr, tn, hd = run(px, w, offset_mask(px.index, d, CADENCE))
            paths[(g, d)] = (gr.iloc[WARM:], tn.iloc[WARM:], hd.iloc[WARM:])
    spy = px["SPY"].pct_change().fillna(0.0).iloc[WARM:]
    return paths, spy, shy_rate(px).iloc[WARM:]


def rate_for(model, tv):
    return tv if model == "TV_SHY" else float(model.replace("FLAT", "")) / 100.0


def window(s, w):
    return {"FULL": s, "IS": s.loc[:IS_END], "OOS": s.loc[OOS_START:]}[w]


def main():
    P(f"# {SLUG}")
    P(f"# dials: FIN {FINMODELS} x GROSS {GROSS}  (2 tuned, PROTOCOL rule 4)")
    P(f"# fixed: band={BAND} cadence={CADENCE} cost={COST}bps spread={SPREAD:.3%} warm={WARM}")
    grid, bes, clause, wf, conv = [], [], [], [], []

    for name, kw in [("U56", {}), ("B136", {"broad": True})]:
        px = load_universe(**kw)
        paths, spy, tv = build(px, name)

        # ---- GATES -------------------------------------------------------
        g0, t0, h0 = paths[(0.75, 0)]
        eng = backtest(px, rules_v2_weights(px, BAND, 0.75), cost_bps=COST, freq=CADENCE)["returns"].iloc[WARM:]
        d1 = float((net(g0, t0, h0, 0.0) - eng).abs().max())
        P(f"G1 run()+net() == engine.backtest(band .03, gross .75, 10bps): max|diff| {d1:.3e}  [{'PASS' if d1 < 1e-12 else 'FAIL'}]")
        maxheld_1 = float(max(paths[(g, 0)][2].max() for g in [0.75, 1.00]))
        P(f"G2 borrowed==0 at gross<=1.00: max held gross {maxheld_1:.4f}  [{'PASS' if maxheld_1 <= 1.0 + 1e-9 else 'FAIL'}]")
        P(f"G3 TV_SHY proxy: mean {tv.mean():.3%}/yr  min {tv.min():.3%}  max {tv.max():.3%}  "
          f"NaN {int(tv.isna().sum())}  [{'PASS' if tv.notna().all() and tv.min() >= 0 else 'FAIL'}]")
        yr = tv.groupby(tv.index.year).mean()
        P("   TV_SHY by year: " + "  ".join(f"{y}:{v:.2%}" for y, v in yr.items()))
        P(f"G4 SPY comparand is unlevered buy-and-hold, financing-invariant by construction  [PASS]")

        base_m = {w: met(window(net(*paths[(0.75, 0)], 0.0), w)) for w in ("FULL", "IS", "OOS")}
        spy_m = {w: met(window(spy, w)) for w in ("FULL", "IS", "OOS")}
        for w in ("FULL", "IS", "OOS"):
            b, s = base_m[w], spy_m[w]
            P(f"comparands {w:<4}: RULES v2 {b['CAGR']:7.2%}/{b['Sharpe']:.3f}/{b['MaxDD']:7.2%}   "
              f"SPY {s['CAGR']:7.2%}/{s['Sharpe']:.3f}/{s['MaxDD']:7.2%}   "
              f"4b bars CAGR>={0.70*s['CAGR']:.2%} DD>={0.60*s['MaxDD']:.2%} Sh>({s['H1']:.3f}/{s['H2']:.3f})")

        # ---- B1  the 72-cell grid ---------------------------------------
        P(f"\n--- B1  GRID (all {len(FINMODELS)*len(GROSS)} cells, panel {name}) ---")
        for model, g in itertools.product(FINMODELS, GROSS):
            gr, tn, hd = paths[(g, 0)]
            rate = rate_for(model, tv)
            r = net(gr, tn, hd, rate)
            row = dict(panel=name, fin=model, gross=g)
            for w in ("FULL", "OOS"):
                m = met(window(r, w))
                ok4b, legs = v4b(m, spy_m[w])
                row.update({f"{w}_CAGR": m["CAGR"], f"{w}_Sharpe": m["Sharpe"], f"{w}_MaxDD": m["MaxDD"],
                            f"{w}_H1": m["H1"], f"{w}_H2": m["H2"], f"{w}_4b": ok4b,
                            f"{w}_cagr_ok": legs["cagr"], f"{w}_dd_ok": legs["dd"], f"{w}_sh_ok": legs["sharpe"],
                            f"{w}_4a": v4a(m, base_m[w])})
            borrowed = (hd - 1.0).clip(lower=0.0)
            rt = rate if isinstance(rate, pd.Series) else pd.Series(rate, index=hd.index)
            row["mean_held_gross"] = float(hd.mean())
            row["mean_borrowed"] = float(borrowed.mean())
            row["fin_drag_ann"] = float((borrowed * rt).mean())
            row["turnover_ann"] = float(tn.mean() * 252)
            grid.append(row)
        df = pd.DataFrame([r for r in grid if r["panel"] == name])
        show = df[["fin", "gross", "FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD", "FULL_H1", "FULL_H2",
                   "FULL_4a", "FULL_4b", "FULL_cagr_ok", "FULL_dd_ok", "FULL_sh_ok",
                   "mean_borrowed", "fin_drag_ann"]].copy()
        for c in ["FULL_CAGR", "FULL_MaxDD", "fin_drag_ann"]:
            show[c] = show[c].map(lambda x: f"{x:.2%}")
        for c in ["FULL_Sharpe", "FULL_H1", "FULL_H2", "mean_borrowed"]:
            show[c] = show[c].map(lambda x: f"{x:.3f}")
        P(show.to_string(index=False))

        # ---- B2  break-even financing rate ------------------------------
        P(f"\n--- B2  BREAK-EVEN FINANCING RATE r* (panel {name}), model-free ---")
        P("    r*_unlev : flat rate at which the levered cell's CAGR falls to the gross-1.00 book's")
        P("    r*_v2    : ... to the LIVE RULES v2 book's (band .03, gross .75)")
        P("    r*_4b    : ... to the 4b CAGR floor (0.70 x SPY)")
        for w in ("FULL", "OOS"):
            unlev = cagr_of(window(net(*paths[(1.00, 0)], 0.0), w))
            for g in GROSS:
                gr, tn, hd = paths[(g, 0)]
                sub = (window(gr, w), window(tn, w), window(hd, w))
                row = dict(panel=name, window=w, gross=g,
                           cagr_free=cagr_of(net(*sub, 0.0)),
                           r_unlev=breakeven_rate(*sub, unlev),
                           r_v2=breakeven_rate(*sub, base_m[w]["CAGR"]),
                           r_4b=breakeven_rate(*sub, 0.70 * spy_m[w]["CAGR"]))
                bes.append(row)
                f = lambda x: "n/a (below already)" if x is None else ("inf" if x == float("inf") else f"{x:.2%}")
                P(f"  {w:<4} gross {g:.2f}: CAGR@0% {row['cagr_free']:7.2%}   "
                  f"r*_unlev {f(row['r_unlev']):>20}   r*_v2 {f(row['r_v2']):>20}   r*_4b {f(row['r_4b']):>20}")

        # ---- B3  break-even gross per financing rung --------------------
        P(f"\n--- B3  BREAK-EVEN GROSS g* per financing rung (panel {name}) ---")
        for model in FINMODELS:
            rate = rate_for(model, tv)
            cg = {g: cagr_of(net(*paths[(g, 0)], rate)) for g in GROSS}
            ref = cg[1.00]
            better = [g for g in GROSS if g > 1.00 and cg[g] > ref]
            P(f"  {model:<7}: " + "  ".join(f"{g:.2f}:{cg[g]:.2%}" for g in GROSS) +
              f"   | levered rungs beating gross 1.00: {better if better else 'NONE'}")

        # ---- B5  rule 8 --------------------------------------------------
        P(f"\n--- B5  RULE 8 walk-forward (panel {name}): choose on <= {IS_END}, read {OOS_START}+ ONCE ---")
        for chooser, models in [("GROSS only, financing FIXED at TV_SHY (headline)", ["TV_SHY"]),
                                ("GROSS only, financing FIXED at FLAT4", ["FLAT4"]),
                                ("BOTH dials free (sensitivity)", FINMODELS)]:
            cells = []
            for model, g in itertools.product(models, GROSS):
                rate = rate_for(model, tv)
                r = net(*paths[(g, 0)], rate)
                m_is = met(r.loc[:IS_END])
                ok, _ = v4b(m_is, spy_m["IS"])
                cells.append((model, g, m_is["Sharpe"], ok, r))
            legal = [c for c in cells if c[3]]
            pool = legal if legal else cells
            model, g, is_sh, ok, r = max(pool, key=lambda c: c[2])
            tag = "4b-legal IS" if legal else "NONE 4b-legal IS -> max IS Sharpe fallback"
            m_o = met(r.loc[OOS_START:])
            ok_o, legs_o = v4b(m_o, spy_m["OOS"])
            P(f"  [{chooser}]  IS pick fin={model} gross={g:.2f} (IS Sharpe {is_sh:.3f}; chooser={tag}; "
              f"{len(legal)}/{len(cells)} IS-legal)")
            P(f"      OOS pick     {m_o['CAGR']:7.2%}/{m_o['Sharpe']:.3f}/{m_o['MaxDD']:7.2%}  halves {m_o['H1']:.3f}/{m_o['H2']:.3f}")
            P(f"      OOS RULES v2 {base_m['OOS']['CAGR']:7.2%}/{base_m['OOS']['Sharpe']:.3f}/{base_m['OOS']['MaxDD']:7.2%}"
              f"   OOS SPY {spy_m['OOS']['CAGR']:7.2%}/{spy_m['OOS']['Sharpe']:.3f}/{spy_m['OOS']['MaxDD']:7.2%}")
            P(f"      OOS 4b={ok_o} legs {legs_o}   OOS 4a={v4a(m_o, base_m['OOS'])}")
            wf.append(dict(panel=name, chooser=chooser, fin=model, gross=g, is_sharpe=is_sh,
                           is_legal_n=len(legal), n_cells=len(cells),
                           oos_CAGR=m_o["CAGR"], oos_Sharpe=m_o["Sharpe"], oos_MaxDD=m_o["MaxDD"],
                           oos_H1=m_o["H1"], oos_H2=m_o["H2"], oos_4b=ok_o, oos_4a=v4a(m_o, base_m["OOS"]),
                           **{f"oos_{k}_ok": v for k, v in legs_o.items()}))

        # ---- B6  idea 914's offset-spread clause -------------------------
        P(f"\n--- B6  IDEA 914 CLAUSE: every 4b pass's leg margins vs its OWN 5-offset spread (panel {name}) ---")
        passes = [r for r in grid if r["panel"] == name and (r["FULL_4b"] or r["OOS_4b"])]
        if not passes:
            P("  no 4b pass on this panel at any of the 36 cells -> clause vacuous here")
        for r0 in passes:
            g, model = r0["gross"], r0["fin"]
            rate = rate_for(model, tv)
            for w in ("FULL", "OOS"):
                if not r0[f"{w}_4b"]:
                    continue
                legsv = {k: [] for k in ("CAGR", "Sharpe", "MaxDD")}
                pass_at = 0
                for d in OFFSETS:
                    m = met(window(net(*paths[(g, d)], rate), w))
                    for k in legsv: legsv[k].append(m[k])
                    pass_at += int(v4b(m, spy_m[w])[0])
                m0 = met(window(net(*paths[(g, 0)], rate), w))
                marg = dict(CAGR=m0["CAGR"] - 0.70 * spy_m[w]["CAGR"],
                            MaxDD=m0["MaxDD"] - 0.60 * spy_m[w]["MaxDD"],
                            Sharpe=min(m0["H1"] - spy_m[w]["H1"], m0["H2"] - spy_m[w]["H2"]))
                sprd = {k: max(v) - min(v) for k, v in legsv.items()}
                resolved = all(abs(marg[k]) > sprd[k] for k in ("CAGR", "MaxDD"))
                P(f"  {w:<4} fin={model:<7} gross={g:.2f}: margins CAGR {marg['CAGR']:+.2%} / DD {marg['MaxDD']:+.2%}"
                  f" vs offset spreads {sprd['CAGR']:.2%} / {sprd['MaxDD']:.2%}"
                  f"  -> resolved={resolved}, holds at {pass_at}/5 offsets")
                clause.append(dict(panel=name, window=w, fin=model, gross=g,
                                   marg_CAGR=marg["CAGR"], marg_MaxDD=marg["MaxDD"], marg_Sharpe=marg["Sharpe"],
                                   spread_CAGR=sprd["CAGR"], spread_MaxDD=sprd["MaxDD"], spread_Sharpe=sprd["Sharpe"],
                                   resolved=resolved, offsets_passing=pass_at))

        # ---- B7  symmetric-cash convention ------------------------------
        P(f"\n--- B7  CONVENTION SENSITIVITY: idle NAV earns (fin - {SPREAD:.1%}) instead of 0% (panel {name}) ---")
        for model in FINMODELS:
            rate = rate_for(model, tv)
            line = []
            for g in GROSS:
                r = net(*paths[(g, 0)], rate, cash_yield=True)
                m = met(window(r, "FULL"))
                ok, _ = v4b(m, spy_m["FULL"])
                line.append(f"{g:.2f}:{m['CAGR']:.2%}{'*' if ok else ''}")
                conv.append(dict(panel=name, fin=model, gross=g, conv="cash_yield",
                                 FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"], FULL_4b=ok))
            P(f"  {model:<7}: " + "  ".join(line) + "   (* = 4b FULL pass)")

    # ------------------------------------------------------------- summary
    G = pd.DataFrame(grid); B = pd.DataFrame(bes); C = pd.DataFrame(clause); W = pd.DataFrame(wf); V = pd.DataFrame(conv)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    B.to_csv(OUT / f"{SLUG}.breakeven.csv", index=False)
    C.to_csv(OUT / f"{SLUG}.clause.csv", index=False)
    W.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    V.to_csv(OUT / f"{SLUG}.convention.csv", index=False)

    P(f"\n{'='*86}\nSUMMARY\n{'='*86}")
    for name in ("U56", "B136"):
        g = G[G.panel == name]
        lev = g[g.gross > 1.0]
        P(f"{name}: 4b FULL passes {int(g.FULL_4b.sum())}/{len(g)} (levered {int(lev.FULL_4b.sum())}/{len(lev)}); "
          f"4b OOS passes {int(g.OOS_4b.sum())}/{len(g)} (levered {int(lev.OOS_4b.sum())}/{len(lev)}); "
          f"4a FULL {int(g.FULL_4a.sum())}/{len(g)}")
        b = B[(B.panel == name) & (B.window == "FULL") & (B.gross > 1.0)]
        f = lambda x: "never-paid" if pd.isna(x) else (">100%" if np.isinf(x) else f"{x:.2%}")
        P(f"  r*_unlev FULL by gross: " + "  ".join(f"{r.gross:.2f}:{f(r.r_unlev)}" for r in b.itertuples()))
    P("\nQ3 (does any levered cell survive a realistic borrow cost on the 4b margin?): "
      f"{int(G[(G.gross > 1.0) & (G.fin != 'FLAT0')].FULL_4b.sum())} levered non-zero-financing cells pass 4b FULL, "
      f"{int(G[(G.gross > 1.0) & (G.fin != 'FLAT0')].OOS_4b.sum())} pass 4b OOS, of "
      f"{len(G[(G.gross > 1.0) & (G.fin != 'FLAT0')])}.")
    if len(C):
        P(f"idea-914 clause on those passes: resolved {int(C.resolved.sum())}/{len(C)}, "
          f"5-of-5-offset stable {int((C.offsets_passing == 5).sum())}/{len(C)}")
    (OUT / f"{SLUG}.log.txt").write_text("\n".join(LOG) + "\n")
    print("wrote", f"{SLUG}.[grid|breakeven|clause|walkforward|convention].csv + .log.txt")


if __name__ == "__main__":
    main()
