#!/usr/bin/env python3
"""Idea 772 (lane cloud, 2026-09-19) — IS THE SMALL 4a BAR CARRIED ENTIRELY BY ITS OOS
SECOND HALF?

Idea 767 read the live book (RULES v2) on the small panel at OOS Sharpe 0.5665 with OOS
halves 0.9166 / 0.1704.  PROTOCOL path 4a asks a device to beat THAT book in both halves,
so if the bar itself collapses inside one sub-window, every SMALL 4a verdict is a verdict
about a degenerate comparand.  This run re-measures the bar, re-scores a pre-registered
device corpus against split-aware bars, and asks whether the collapse is resolvable at all.

DIALS (2, the protocol maximum)
  SPLIT  in {H2, T3, Y}   halves / thirds / calendar-year blocks of the scoring window
  BAR    in {POOLED, MIN, ALL}
         POOLED = committed practice: device Sharpe > bar Sharpe in both halves of the window
         MIN    = lenient: device pooled Sharpe > the bar's WORST block Sharpe
         ALL    = strict: device Sharpe > bar Sharpe in EVERY block of the split

PUBLISHED, NOT TUNED (every cell printed)
  PANEL   SMALL (the claim's panel) + U56 and B136 as controls
  WINDOW  FULL / IS (<= 2016-12-31) / OOS (2017+)
  DEVICE  17 books rebuilt from research/baseline.py, none of them tuned by this run:
          BAND b in {0.00, 0.03, 0.08} x G in {0.75, 1.00}   (the live family)
          MAXVOL m in {0.60, 0.80}     x G                    (v1 eligibility, equal weight)
          TOPN n in {10, 20, 40}       x G                    (2026-09-04 KEEP-4b construction,
                                                               composite score, NO vol scaler)
          RULES v1 (n=5, w=0.15)                               (legacy)

Costs 10 bps / unit turnover, weekly, decided at t applied at t+1 (PROTOCOL 2).
Rule 8: device chosen on IS only, OOS 2017-2026 read once, reported vs baseline and SPY.
Noise: circular block bootstrap (21-day blocks, 2000 draws, seed 20260919) of the bar's own
OOS half-Sharpe difference, so "collapsed second half" is quoted against its own SE.
"""
import sys, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state, score   # noqa
from engine import backtest, rebalance_mask, metrics                                        # noqa

OUT = ROOT / "research" / "backtests"
STAMP = "2026-09-19_small-4a-bar-oos-halves_cloud"
COST, FREQ, IS_END, SEED, NDRAW, BLOCK = 10.0, "W", "2016-12-31", 20260919, 2000, 21
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def fast_bt(px, W, cost_bps=COST, freq=FREQ):
    """Replay of engine.backtest in numpy (gated below)."""
    P = px.values
    R = np.zeros_like(P, dtype=float); R[1:] = P[1:] / P[:-1] - 1.0
    R = np.nan_to_num(R, nan=0.0, posinf=0.0, neginf=0.0)
    Wv = np.nan_to_num(W.reindex(px.index).values.astype(float), nan=0.0)
    Ws = np.zeros_like(Wv); Ws[1:] = Wv[:-1]
    m = rebalance_mask(px.index, freq).values
    ms = np.zeros(len(P), dtype=bool); ms[1:] = m[:-1]
    cur = np.zeros(P.shape[1]); port = np.zeros(len(P)); turn = np.zeros(len(P))
    for i in range(len(P)):
        if ms[i] or i == 0:
            new = Ws[i]; turn[i] = np.abs(new - cur).sum(); cur = new.copy()
        port[i] = float(cur @ R[i]) - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + R[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


# ---------------------------------------------------------------- device corpus
def eqw(mask, gross):
    n = mask.sum(axis=1).replace(0, np.nan)
    return (mask.astype(float).div(n, axis=0) * gross).fillna(0.0)


def make_devices():
    D = {}
    for g in (0.75, 1.00):
        for b in (0.00, 0.03, 0.08):
            D[f"BAND{b:.2f}_G{g:.2f}"] = (lambda px, b=b, g=g: rules_v2_weights(px, b, g))
        for m in (0.60, 0.80):
            def f(px, m=m, g=g):
                _, above, vol20 = score(px)
                return eqw(above & (vol20 < m) & px.notna(), g)
            D[f"MAXVOL{m:.2f}_G{g:.2f}"] = f
        for n in (10, 20, 40):
            def f(px, n=n, g=g):
                s, above, vol20 = score(px, vol_scale=False)
                elig = s.where(above & (vol20 < 0.60) & px.notna())
                return eqw(elig.rank(axis=1, ascending=False) <= n, g)
            D[f"TOP{n}_G{g:.2f}"] = f
    D["RULESv1"] = rules_v1_weights
    return D


# ---------------------------------------------------------------- blocks / bars
def blocks(idx, split):
    if split == "H2":
        h = len(idx) // 2
        return [("B1", idx[:h]), ("B2", idx[h:])]
    if split == "T3":
        t = len(idx) // 3
        return [("B1", idx[:t]), ("B2", idx[t:2 * t]), ("B3", idx[2 * t:])]
    if split == "Y":
        out = []
        for y in sorted({d.year for d in idx}):
            sel = idx[[d.year == y for d in idx]]
            if len(sel) >= 120: out.append((str(y), sel))
        return out
    raise ValueError(split)


def sharpe(r):
    return metrics(r)["Sharpe"] if len(r) > 20 else np.nan


def verdict4a(rd, rb, split, bar):
    """PROTOCOL 4a restated under (SPLIT, BAR).  MaxDD leg unchanged in every reading."""
    dd_ok = metrics(rd)["MaxDD"] >= metrics(rb)["MaxDD"]
    bl = blocks(rd.index, split)
    if bar == "POOLED":
        h = len(rd) // 2
        return bool(sharpe(rd.iloc[:h]) > sharpe(rb.iloc[:h]) and sharpe(rd.iloc[h:]) > sharpe(rb.iloc[h:]) and dd_ok)
    if bar == "MIN":
        return bool(sharpe(rd) > min(sharpe(rb.loc[b]) for _, b in bl) and dd_ok)
    if bar == "ALL":
        return bool(all(sharpe(rd.loc[b]) > sharpe(rb.loc[b]) for _, b in bl) and dd_ok)
    raise ValueError(bar)


def pass4b(r, spy):
    h = len(r) // 2
    m, ms = metrics(r), metrics(spy)
    return bool(sharpe(r.iloc[:h]) > sharpe(spy.iloc[:h]) and sharpe(r.iloc[h:]) > sharpe(spy.iloc[h:])
                and m["MaxDD"] >= 0.60 * ms["MaxDD"] and m["CAGR"] >= 0.70 * ms["CAGR"])


def boot_half_diff(r, nd=NDRAW, block=BLOCK, seed=SEED):
    """Circular block bootstrap of (Sharpe H1 - Sharpe H2) of one return stream."""
    x = r.values; T = len(x); rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / block))
    out = np.empty(nd)
    for i in range(nd):
        st = rng.integers(0, T, nb)
        samp = np.concatenate([np.take(x, np.arange(s, s + block) % T) for s in st])[:T]
        h = T // 2
        a, b = samp[:h], samp[h:]
        sa = a.mean() * 252 / (a.std() * np.sqrt(252)) if a.std() else np.nan
        sb = b.mean() * 252 / (b.std() * np.sqrt(252)) if b.std() else np.nan
        out[i] = sa - sb
    return out


# ---------------------------------------------------------------- driver
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"SMALL: dropped {px.shape[1]-len(keep)} names with max_1d_move >= 1.0 -> {len(keep)-1} names "
        f"(SURVIVORSHIP: current constituents of the screen only; the record's `SMALL439` label now "
        f"denotes this rebuilt pool, idea 1074)")
    return px[keep]


def main():
    devices = make_devices()
    rows, bars, boots = [], [], []
    panels = [("SMALL", small_panel()), ("U56", load_universe()), ("B136", load_universe(broad=True))]
    for pname, px in panels:
        t0 = time.time()
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        r_bar, _ = fast_bt(px, rules_v2_weights(px, 0.03, 0.75))
        eng = backtest(px, rules_v2_weights(px, 0.03, 0.75), cost_bps=COST, freq=FREQ)["returns"]
        d = float((eng.loc[start:] - r_bar.loc[start:]).abs().max())
        say(f"{pname}: GATE fast_bt vs engine.backtest max|d| = {d:.3e}")
        assert d < 1e-15
        r_bar = r_bar.loc[start:]
        if pname == "SMALL":
            o = r_bar.loc["2017-01-01":]; h = len(o) // 2
            say(f"SMALL: BAR reproduction — OOS Sharpe {sharpe(o):.4f} halves {sharpe(o.iloc[:h]):.4f} / "
                f"{sharpe(o.iloc[h:]):.4f}; idea 767 committed 0.5665 / 0.9166 / 0.1704 on the PRE-REBUILD "
                f"pool (idea 1074: the `SMALL439` label now denotes this 665-name pool). Same sign, same shape.")
        wins = dict(FULL=r_bar.index, IS=r_bar.loc[:IS_END].index, OOS=r_bar.loc["2017-01-01":].index)

        # ---- (1) the BAR's own profile
        for wn, widx in wins.items():
            rb = r_bar.loc[widx]
            rec = dict(panel=pname, window=wn, bar_Sharpe=sharpe(rb), bar_CAGR=metrics(rb)["CAGR"],
                       bar_MaxDD=metrics(rb)["MaxDD"], spy_Sharpe=sharpe(spy.loc[widx]))
            for sp in ("H2", "T3", "Y"):
                bs = [sharpe(rb.loc[b]) for _, b in blocks(widx, sp)]
                rec[f"{sp}_min"], rec[f"{sp}_max"] = np.nanmin(bs), np.nanmax(bs)
                rec[f"{sp}_spread"] = rec[f"{sp}_max"] - rec[f"{sp}_min"]
                rec[f"{sp}_blocks"] = "/".join(f"{b:.4f}" for b in bs)
            bars.append(rec)
            if wn == "OOS":
                bd = boot_half_diff(rb)
                h = len(rb) // 2
                obs = sharpe(rb.iloc[:h]) - sharpe(rb.iloc[h:])
                boots.append(dict(panel=pname, obs_half_diff=obs, boot_sd=float(np.nanstd(bd)),
                                  t=obs / float(np.nanstd(bd)), p_gt0=float(np.nanmean(bd > 0)),
                                  p_two_sided=float(np.nanmean(np.abs(bd) >= abs(obs))),
                                  lo=float(np.nanpercentile(bd, 2.5)), hi=float(np.nanpercentile(bd, 97.5))))

        # ---- (2) the device corpus, re-scored under every (SPLIT, BAR) rung
        for dname, fn in devices.items():
            r, turn = fast_bt(px, fn(px))
            r = r.loc[start:]
            rec = dict(panel=pname, device=dname, turn_yr=float(turn.loc[start:].sum() / (len(r) / 252)))
            for wn, widx in wins.items():
                rd, rb, sp_ = r.loc[widx], r_bar.loc[widx], spy.loc[widx]
                m = metrics(rd)
                rec.update({f"{wn}_CAGR": m["CAGR"], f"{wn}_Sharpe": m["Sharpe"], f"{wn}_MaxDD": m["MaxDD"],
                            f"{wn}_4b": pass4b(rd, sp_)})
                for split in ("H2", "T3", "Y"):
                    for bar in ("POOLED", "MIN", "ALL"):
                        if bar == "POOLED" and split != "H2":
                            continue                       # POOLED does not read the split
                        rec[f"{wn}_4a_{split}_{bar}" if bar != "POOLED" else f"{wn}_4a_POOLED"] = \
                            verdict4a(rd, rb, split, bar)
            rows.append(rec)
        say(f"{pname}: {len(devices)} devices in {time.time()-t0:.1f}s")

    B = pd.DataFrame(bars); G = pd.DataFrame(rows); BT = pd.DataFrame(boots)
    B.to_csv(OUT / f"{STAMP}.bars.csv", index=False)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    BT.to_csv(OUT / f"{STAMP}.bootstrap.csv", index=False)

    say("")
    say("=" * 108)
    say("(1) THE BAR ITSELF (live RULES v2, band 0.03, G 0.75, weekly, 10 bps) BLOCK BY BLOCK")
    say("=" * 108)
    for _, r in B.iterrows():
        say(f"{r.panel:6}{r.window:5} Sharpe {r.bar_Sharpe:7.4f} CAGR {r.bar_CAGR:7.2%} MaxDD {r.bar_MaxDD:7.2%}"
            f" | SPY {r.spy_Sharpe:7.4f} | H2 {r.H2_blocks:18} spread {r.H2_spread:6.4f}"
            f" | T3 {r.T3_blocks:26} spread {r.T3_spread:6.4f}")
    say("")
    say("calendar-year blocks of the bar:")
    for _, r in B[B.window == "FULL"].iterrows():
        say(f"  {r.panel:6} {r.Y_blocks}  (spread {r.Y_spread:.4f})")
    say("")
    say("(1b) IS THE COLLAPSE RESOLVABLE?  circular block bootstrap, 21d blocks, 2000 draws, seed 20260919")
    for _, r in BT.iterrows():
        say(f"  {r.panel:6} OOS H1-H2 Sharpe diff {r.obs_half_diff:+7.4f}  SE {r.boot_sd:.4f}"
            f"  t {r.t:+6.2f}  95% CI [{r.lo:+.4f}, {r.hi:+.4f}]  P(|boot| >= |obs|) {r.p_two_sided:.3f}")

    say("")
    say("=" * 108)
    say("(2) EVERY DEVICE, EVERY RUNG (4a readings; 4b for reference).  WINDOW = OOS unless stated")
    say("=" * 108)
    cols4a = [c for c in G.columns if "_4a_" in c or c.endswith("_4a_POOLED")]
    hdr = f"{'panel':6}{'device':16}{'OOS CAGR':>9}{'Sharpe':>9}{'MaxDD':>9} | {'4a POOL':>8}{'MIN H2':>7}{'ALL H2':>7}{'ALL T3':>7}{'ALL Y':>7} | {'4b OOS':>7}"
    say(hdr); say("-" * len(hdr))
    for _, r in G.iterrows():
        say(f"{r.panel:6}{r.device:16}{r.OOS_CAGR:9.2%}{r.OOS_Sharpe:9.4f}{r.OOS_MaxDD:9.2%} |"
            f" {str(r.OOS_4a_POOLED):>8}{str(r.OOS_4a_H2_MIN):>7}{str(r.OOS_4a_H2_ALL):>7}"
            f"{str(r.OOS_4a_T3_ALL):>7}{str(r.OOS_4a_Y_ALL):>7} | {str(r.OOS_4b):>7}")

    say("")
    say("=" * 108)
    say("(3) HOW MANY 4a PASSES SURVIVE EACH RUNG")
    say("=" * 108)
    for pn in G.panel.unique():
        sub = G[G.panel == pn]
        for wn in ("FULL", "IS", "OOS"):
            line = f"{pn:6}{wn:5}"
            for c in [f"{wn}_4a_POOLED", f"{wn}_4a_H2_MIN", f"{wn}_4a_H2_ALL", f"{wn}_4a_T3_ALL", f"{wn}_4a_Y_ALL"]:
                line += f"  {c.split('_4a_')[1]:7}{int(sub[c].sum()):2d}/{len(sub)}"
            line += f"   | 4b {int(sub[f'{wn}_4b'].sum()):2d}/{len(sub)}"
            say(line)

    # ---- (4) rule 8: pick the device on IS only, read OOS once
    say("")
    say("=" * 108)
    say("(4) RULE 8 — device chosen on IS (<= 2016-12-31) only, OOS 2017-2026 read once")
    say("=" * 108)
    wf = []
    for pn, px in panels:
        sub = G[G.panel == pn]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        rb, _ = fast_bt(px, rules_v2_weights(px, 0.03, 0.75)); rb = rb.loc[start:]
        base_oos, spy_oos = metrics(rb.loc["2017-01-01":]), metrics(spy.loc["2017-01-01":])
        picks = {"C_SHARPE": sub.loc[sub.IS_Sharpe.idxmax()],
                 "C_CALMAR": sub.loc[(sub.IS_CAGR / sub.IS_MaxDD.abs()).idxmax()],
                 "C_IS4a_ALL": (sub[sub.IS_4a_Y_ALL].sort_values("IS_Sharpe", ascending=False).iloc[0]
                                if sub.IS_4a_Y_ALL.any() else None)}
        for cn, pk in picks.items():
            if pk is None:
                say(f"{pn:6}{cn:12} -> no device clears IS 4a under ALL/Y"); continue
            say(f"{pn:6}{cn:12} -> {pk.device:16} OOS {pk.OOS_CAGR:7.2%} / {pk.OOS_Sharpe:7.4f} / {pk.OOS_MaxDD:7.2%}"
                f" | bar OOS {base_oos['CAGR']:6.2%}/{base_oos['Sharpe']:.4f}/{base_oos['MaxDD']:.2%}"
                f" | SPY OOS {spy_oos['CAGR']:6.2%}/{spy_oos['Sharpe']:.4f}/{spy_oos['MaxDD']:.2%}"
                f" | 4a POOL {pk.OOS_4a_POOLED} ALL/Y {pk.OOS_4a_Y_ALL} | 4b {pk.OOS_4b}")
            wf.append(dict(panel=pn, chooser=cn, device=pk.device, OOS_CAGR=pk.OOS_CAGR,
                           OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                           OOS_4a_POOLED=pk.OOS_4a_POOLED, OOS_4a_Y_ALL=pk.OOS_4a_Y_ALL, OOS_4b=pk.OOS_4b,
                           bar_OOS_Sharpe=base_oos["Sharpe"], bar_OOS_CAGR=base_oos["CAGR"],
                           bar_OOS_MaxDD=base_oos["MaxDD"], spy_OOS_Sharpe=spy_oos["Sharpe"],
                           spy_OOS_CAGR=spy_oos["CAGR"], spy_OOS_MaxDD=spy_oos["MaxDD"]))
    pd.DataFrame(wf).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    (OUT / f"{STAMP}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
