#!/usr/bin/env python3
"""Idea 1476 (lane C, 2026-09-22): how many committed BEST-RUNG claims sit on a ladder whose
NEIGHBOURS are a FACTOR 2 APART -- and does the argmax relocate once the ladder is refined to
<= 15% spacing?

Two parts, exactly as the queue line specifies.

  (A) CENSUS.  Scan the committed record (LEADERBOARD.md, CHANGELOG.md, every research/backtests
      memo) for claims of the form "rung X is the best / steepest / optimal / argmax".  For each
      site, recover the LADDER its dial was quoted on in the same row, compute the ladder's worst
      adjacent spacing, and record whether ANY standard error was quoted alongside.

  (B) CAPITAL ARM.  Re-price the THREE MOST LOAD-BEARING best-rung claims in the record -- the
      three constants the live books actually ship -- on a refined ladder spaced <= 15%:
        F1  n     = 5   (RULES v1 top-n, gross held at 0.75 so n is not a sizing dial)
        F2  gross = 0.75(RULES v2 clause 3)
        F3  band  = 0.03(RULES v2 clause 2)
      Every refined rung is scored full-sample, on both halves, under BOTH KEEP paths (4a vs the
      live RULES v2 book, 4b vs SPY), and under PROTOCOL rule 8 (dial chosen on 2009-2016 only,
      2017-2026 read once).  A PAIRED stationary-block bootstrap (same resampled dates for every
      rung) prices whether any relocation of the argmax is resolvable at all.

Tuned parameters: 2 (the refined rung, and the bootstrap block length) -- ALL grid points reported.
Panels: U56 (research/universe.json) and B136 (research/universe_broad.json).
SURVIVORSHIP (rule 9): both panels are CURRENT-constituent lists held from 2008, so every absolute
CAGR/Sharpe level is optimistic and the 4b bar is easier than on a point-in-time panel.  The
WITHIN-LADDER contrasts this idea is about are same-tape, same-names and first-order immune; the
absolute pass counts are not.
Deterministic: fixed seed, no network.
"""
import sys, re, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, backtest, metrics  # noqa

SEED, NBOOT = 1476, 400
COST_BPS, FREQ = 10, "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
OUT = Path(__file__).with_suffix("")

# ----------------------------------------------------------------------------- (A) CENSUS
CLAIM_WORDS = r"(?:\bbest\b|\bargmax\b|\boptimal\b|\bsteepest\b|\bpeaks? at\b|\bbest rung\b|\bpicks\b|\bwinning rung\b)"
SE_WORDS    = r"(?:\bSE\b|standard error|\bbootstrap\b|\+/-|±|\bse\s*=|\bCI\b|confidence interval)"
# dial lexicon: name -> regex matching "<dial> = <value>" in the record's own prose
DIALS = ["n", "k", "gross", "g", "band", "c", "phi", "L", "H", "theta", "w", "vol", "max_vol"]

def census():
    files = [ROOT/"research"/"LEADERBOARD.md", ROOT/"research"/"CHANGELOG.md"]
    files += sorted((ROOT/"research"/"backtests").glob("*.md"))
    files += sorted((ROOT/"research"/"ideas").glob("*.md")) if (ROOT/"research"/"ideas").is_dir() else []
    sites = []
    for f in files:
        try: txt = f.read_text(errors="ignore")
        except Exception: continue
        for ln, row in enumerate(txt.split("\n"), 1):
            if len(row) < 40: continue
            if not re.search(CLAIM_WORDS, row, re.I): continue
            for d in DIALS:
                vals = re.findall(rf"\b{re.escape(d)}\s*=\s*(-?\d+(?:\.\d+)?)", row)
                vals = sorted({float(v) for v in vals})
                if len(vals) < 2: continue                     # need a LADDER, not a point
                pos = [v for v in vals if v > 0]
                if len(pos) < 2: continue
                ratios = [pos[i+1]/pos[i] for i in range(len(pos)-1)]
                sites.append(dict(file=f.name, line=ln, dial=d, n_rungs=len(vals),
                                  lo=pos[0], hi=pos[-1], worst_spacing=max(ratios),
                                  has_zero_rung=any(v == 0 for v in vals),
                                  se_quoted=bool(re.search(SE_WORDS, row)),
                                  claim=re.search(CLAIM_WORDS, row, re.I).group(0).lower()))
    return pd.DataFrame(sites)

# ----------------------------------------------------------------------------- books
def bt(px, W):
    return backtest(px, W, cost_bps=COST_BPS, freq=FREQ)["returns"]

def m3(r):
    m = metrics(r); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def rung_row(name, family, rung, r, start, mid, base, spy):
    r, b, s = r.loc[start:], base.loc[start:], spy.loc[start:]
    h = len(r)//2
    c, sh, dd = m3(r)
    h1, h2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    bc, bsh, bdd = m3(b); bh1, bh2 = metrics(b.iloc[:h])["Sharpe"], metrics(b.iloc[h:])["Sharpe"]
    sc, ssh, sdd = m3(s); sh1, sh2 = metrics(s.iloc[:h])["Sharpe"], metrics(s.iloc[h:])["Sharpe"]
    oos, soos, boos = r.loc[OOS_START:], s.loc[OOS_START:], b.loc[OOS_START:]
    oc, osh, odd = m3(oos)
    keep4a = (h1 > bh1) and (h2 > bh2) and (dd >= bdd)
    keep4b = (h1 > sh1) and (h2 > sh2) and (osh > metrics(soos)["Sharpe"]) \
             and (abs(dd) <= 0.60*abs(sdd)) and (c >= 0.70*sc)
    return dict(family=family, rung=rung, CAGR=c, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd, keep4a=keep4a, keep4b=keep4b,
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"])

# ----------------------------------------------------------------------------- bootstrap
def paired_block_boot(R, block, nboot=NBOOT, seed=SEED):
    """R: T x K matrix of daily returns, one column per rung.  Stationary block bootstrap on the
    DATE axis, identical resampled dates for every rung (paired).  Returns (K,) argmax counts and
    the (nboot, K) Sharpe draws."""
    rng = np.random.default_rng(seed)
    T, K = R.shape
    nblk = int(np.ceil(T/block))
    out = np.empty((nboot, K))
    for b in range(nboot):
        starts = rng.integers(0, T, size=nblk)
        idx = (starts[:, None] + np.arange(block)[None, :]).ravel()[:T] % T
        X = R[idx]
        mu, sd = X.mean(0)*252, X.std(0)*np.sqrt(252)
        out[b] = np.where(sd > 0, mu/sd, np.nan)
    return out

# ----------------------------------------------------------------------------- families
def families(px):
    """name -> (coarse ladder as the record quotes it, refined ladder <= 15% spacing, weights fn)"""
    return {
      "F1_n_RULESv1": dict(
          coarse=[3, 5, 10, 15, 20], shipped=5,
          refined=list(range(3, 21)),
          fn=lambda v: rules_v1_weights(px, n=int(v), w=0.75/int(v))),
      "F2_gross_RULESv2": dict(
          coarse=[0.25, 0.50, 0.75, 1.00], shipped=0.75,
          refined=[round(0.25*(4.0**(k/10)), 4) for k in range(11)],
          fn=lambda v: rules_v2_weights(px, band=0.03, gross=float(v))),
      "F3_band_RULESv2": dict(
          coarse=[0.0, 0.02, 0.03, 0.05, 0.08], shipped=0.03,
          refined=[round(0.01*(10.0**(k/17)), 5) for k in range(18)],
          fn=lambda v: rules_v2_weights(px, band=float(v), gross=0.75)),
    }

def run_panel(tag, px):
    t0 = time.time()
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0)
    base = bt(px, rules_v2_weights(px))
    v1   = bt(px, rules_v1_weights(px))
    mid  = None
    rows, rets = [], {}
    for fam, cfg in families(px).items():
        ladder = sorted(set(cfg["refined"]) | set(cfg["coarse"]))
        for v in ladder:
            r = bt(px, cfg["fn"](v))
            rets[(fam, v)] = r.loc[start:]
            row = rung_row(tag, fam, v, r, start, mid, base, spy)
            row["panel"] = tag
            row["on_coarse"] = v in cfg["coarse"]
            row["shipped"]   = (v == cfg["shipped"])
            rows.append(row)
            print(f"  {tag} {fam} rung={v:<8} CAGR={row['CAGR']:.2%} Sh={row['Sharpe']:.4f} "
                  f"DD={row['MaxDD']:.2%} 4a={int(row['keep4a'])} 4b={int(row['keep4b'])}", flush=True)
    df = pd.DataFrame(rows)
    # reference rows
    ref = []
    for nm, r in [("RULESv2_baseline", base), ("RULESv1", v1), ("SPY", spy)]:
        rr = rung_row(tag, "REF", nm, r, start, mid, base, spy); rr["panel"] = tag
        rr["on_coarse"] = rr["shipped"] = False; ref.append(rr)
    print(f"  [{tag}] {len(df)} books in {time.time()-t0:.0f}s", flush=True)
    return df, pd.DataFrame(ref), rets, base.loc[start:], spy.loc[start:]

def rule8_and_boot(tag, df, rets, blocks=(21, 63)):
    """PROTOCOL rule 8 + the paired bootstrap, per family."""
    out = []
    for fam, cfg in [(f, c) for f, c in families_meta.items()]:
        sub = df[(df.panel == tag) & (df.family == fam)].sort_values("rung")
        if sub.empty: continue
        coarse = sub[sub.on_coarse]
        ship   = sub[sub.shipped].iloc[0]
        # rule 8: argmax IS Sharpe on 2009-2016 only, then read OOS once
        pick_r = sub.loc[sub.IS_Sharpe.idxmax()]
        pick_c = coarse.loc[coarse.IS_Sharpe.idxmax()]
        # full-sample argmax (the "best rung" claim the record publishes)
        arg_r  = sub.loc[sub.Sharpe.idxmax()]
        arg_c  = coarse.loc[coarse.Sharpe.idxmax()]
        ladder = list(sub.rung)
        R = np.column_stack([rets[(fam, v)].values for v in ladder])
        rec = dict(panel=tag, family=fam,
                   coarse_worst_spacing=max(b/a for a, b in zip(sorted(x for x in cfg["coarse"] if x>0)[:-1],
                                                                sorted(x for x in cfg["coarse"] if x>0)[1:])),
                   refined_worst_spacing=max(b/a for a, b in zip(sorted(x for x in cfg["refined"] if x>0)[:-1],
                                                                 sorted(x for x in cfg["refined"] if x>0)[1:])),
                   shipped=ship.rung, shipped_Sharpe=ship.Sharpe,
                   coarse_argmax=arg_c.rung, coarse_argmax_Sharpe=arg_c.Sharpe,
                   refined_argmax=arg_r.rung, refined_argmax_Sharpe=arg_r.Sharpe,
                   relocates=(arg_r.rung != arg_c.rung),
                   gap_refined_minus_coarse=arg_r.Sharpe - arg_c.Sharpe,
                   gap_refined_minus_shipped=arg_r.Sharpe - ship.Sharpe,
                   r8_refined_pick=pick_r.rung, r8_refined_OOS_Sharpe=pick_r.OOS_Sharpe,
                   r8_refined_OOS_CAGR=pick_r.OOS_CAGR, r8_refined_OOS_MaxDD=pick_r.OOS_MaxDD,
                   r8_coarse_pick=pick_c.rung, r8_coarse_OOS_Sharpe=pick_c.OOS_Sharpe,
                   r8_coarse_OOS_CAGR=pick_c.OOS_CAGR, r8_coarse_OOS_MaxDD=pick_c.OOS_MaxDD,
                   shipped_OOS_Sharpe=ship.OOS_Sharpe, shipped_OOS_CAGR=ship.OOS_CAGR,
                   shipped_OOS_MaxDD=ship.OOS_MaxDD,
                   n4a_refined=int(sub.keep4a.sum()), n4b_refined=int(sub.keep4b.sum()),
                   n_rungs=len(sub))
        for blk in blocks:
            S = paired_block_boot(R, blk)
            am = np.asarray([ladder[i] for i in np.nanargmax(S, axis=1)], dtype=float)
            i_ship = ladder.index(ship.rung); i_arg = ladder.index(arg_r.rung)
            d = S[:, i_arg] - S[:, i_ship]
            rec[f"boot{blk}_P_shipped_is_argmax"] = float((am == ship.rung).mean())
            rec[f"boot{blk}_P_refined_argmax"]    = float((am == arg_r.rung).mean())
            rec[f"boot{blk}_argmax_spread"]       = float(np.nanpercentile(am, 95) - np.nanpercentile(am, 5))
            rec[f"boot{blk}_paired_SE_gap"]       = float(np.nanstd(d, ddof=1))
            rec[f"boot{blk}_gap_over_SE"]         = float(rec["gap_refined_minus_shipped"] / np.nanstd(d, ddof=1)) \
                                                     if np.nanstd(d, ddof=1) > 0 else np.nan
            rec[f"boot{blk}_P_gap_le_0"]          = float((d <= 0).mean())
        out.append(rec)
    return pd.DataFrame(out)

def margin_resolvability(tag, df, rets, base, spy, blocks=(21, 63)):
    """For every rung that PASSES a KEEP path (plus the shipped rung of each family), price the
    Sharpe margin over the comparand the path is judged against with the SAME paired stationary
    block bootstrap.  A pass held by less than 1 SE is a placement, not a book."""
    out = []
    sub = df[(df.panel == tag) & (df.keep4a | df.keep4b | df.shipped)]
    for _, row in sub.iterrows():
        r = rets[(row.family, row.rung)]
        for path, comp, cname in [("4a", base, "RULESv2"), ("4b", spy, "SPY")]:
            if path == "4a" and not (row.keep4a or row.shipped): continue
            if path == "4b" and not (row.keep4b or row.shipped): continue
            X = np.column_stack([r.values, comp.values])
            rec = dict(panel=tag, family=row.family, rung=row.rung, path=path, comparand=cname,
                       passes=bool(row.keep4a if path == "4a" else row.keep4b),
                       shipped=bool(row.shipped),
                       margin_Sharpe=metrics(r)["Sharpe"] - metrics(comp)["Sharpe"])
            for blk in blocks:
                S = paired_block_boot(X, blk)
                d = S[:, 0] - S[:, 1]
                se = float(np.nanstd(d, ddof=1))
                rec[f"boot{blk}_SE"] = se
                rec[f"boot{blk}_margin_over_SE"] = rec["margin_Sharpe"]/se if se > 0 else np.nan
                rec[f"boot{blk}_P_margin_le_0"] = float((d <= 0).mean())
            out.append(rec)
    return pd.DataFrame(out)

# ----------------------------------------------------------------------------- main
if __name__ == "__main__":
    print("=" * 100)
    print("IDEA 1476 (lane C) -- BEST-RUNG claims, ladder spacing, and the refined re-pricing")
    print("=" * 100)

    print("\n### (A) CENSUS of committed BEST-RUNG claim sites\n")
    C = census()
    C.to_csv(f"{OUT}.census.csv", index=False)
    if len(C):
        C["factor2_plus"] = C.worst_spacing >= 2.0
        print(f"claim sites with a recoverable ladder : {len(C)}  (files: {C.file.nunique()})")
        print(f"  worst adjacent spacing >= 2.0x      : {int(C.factor2_plus.sum())} "
              f"({C.factor2_plus.mean():.1%})")
        print(f"  ladder contains a ZERO rung         : {int(C.has_zero_rung.sum())} "
              f"({C.has_zero_rung.mean():.1%})  [spacing undefined]")
        print(f"  any SE / bootstrap / CI quoted      : {int(C.se_quoted.sum())} "
              f"({C.se_quoted.mean():.1%})")
        print(f"  worst-spacing quartiles             : "
              + " / ".join(f"{q:.2f}x" for q in C.worst_spacing.quantile([.25,.5,.75,.95])))
        print("\n  by dial:")
        g = C.groupby("dial").agg(sites=("dial","size"), med_spacing=("worst_spacing","median"),
                                  pct_ge_2x=("factor2_plus","mean"), pct_SE=("se_quoted","mean"))
        print(g.sort_values("sites", ascending=False).to_string(float_format=lambda x: f"{x:.3f}"))
        print(f"\n  SITES MEETING THE <=15% SPACING BAR  : {int((C.worst_spacing <= 1.15).sum())} "
              f"({(C.worst_spacing <= 1.15).mean():.1%})")

    print("\n### (B) CAPITAL ARM -- refined re-pricing of the three shipped best-rung claims\n")
    all_df, all_ref, all_r8, all_mg = [], [], [], []
    for tag, kw in [("U56", dict()), ("B136", dict(broad=True))]:
        px = load_universe(**kw)
        families_meta = families(px)
        df, ref, rets, base_r, spy_r = run_panel(tag, px)
        all_df.append(df); all_ref.append(ref)
        all_r8.append(rule8_and_boot(tag, df, rets))
        all_mg.append(margin_resolvability(tag, df, rets, base_r, spy_r))
    D = pd.concat(all_df, ignore_index=True); R8 = pd.concat(all_r8, ignore_index=True)
    MG = pd.concat(all_mg, ignore_index=True); MG.to_csv(f"{OUT}.keep_margins.csv", index=False)
    REF = pd.concat(all_ref, ignore_index=True)
    D.to_csv(f"{OUT}.rungs.csv", index=False)
    R8.to_csv(f"{OUT}.rule8_bootstrap.csv", index=False)
    REF.to_csv(f"{OUT}.reference.csv", index=False)

    print("\n--- ALL GRID POINTS (every refined rung, both panels) ---")
    cols = ["panel","family","rung","on_coarse","shipped","CAGR","Sharpe","MaxDD","H1","H2",
            "IS_Sharpe","OOS_CAGR","OOS_Sharpe","OOS_MaxDD","keep4a","keep4b"]
    print(D[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n--- REFERENCE BOOKS ---")
    print(REF[["panel","rung","CAGR","Sharpe","MaxDD","H1","H2","OOS_CAGR","OOS_Sharpe","OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n--- RULE 8 + PAIRED BOOTSTRAP (all block lengths reported) ---")
    with pd.option_context("display.width", 250, "display.max_columns", 99):
        print(R8.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n--- KEEP-PATH MARGIN RESOLVABILITY (paired bootstrap vs the path's own comparand) ---")
    with pd.option_context("display.width", 250, "display.max_columns", 99):
        print(MG.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nDONE")
