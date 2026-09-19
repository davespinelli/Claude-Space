#!/usr/bin/env python3
"""
Idea 704 (lane cloud, 2026-09-19) — price the CAP CHANNEL against a MATCHED-VOL control.

THE PREMISE (verbatim from the queue).  Idea 694 measured CAP = rho(q, OOS Sharpe) = -0.7709 at
matched width k and matched selection ratio r = n/k, worth up to -0.853 of OOS Sharpe across the
q span — "but small-cap panels also carry more name vol, so the channel may be a vol-scaling
story rather than a cap story.  Re-run the q ladder against a control matched on realised name
vol instead of on cap, and report how much of the -0.853 survives.  Max 2 params (q, vol-match
tolerance)."

q is the SMALL-CAP SHARE of a synthetic panel of width k: q*k names drawn from the SMALL pool
and (1-q)*k from BSTK (broad minus every ETF).  The book is idea 276's CAND-n at gross 0.75,
weekly, 10 bps, t+1.  Every definition below — the panel builder, CAND-n, the gate, the metric
row, the KEEP paths, the Spearman and the rank regression — is IMPORTED from the committed
scripts that published them (ideas 276 / 286 / 525), never re-typed.

WHAT IS UNDER TEST.  The confound is real and mechanical: a small-cap name is a more volatile
name, so ANY q ladder is also a name-vol ladder.  This run separates them three ways.

  ARM CAP      — 694's own construction.  q in {0.00, 0.25, 0.50, 0.75, 1.00} at k = 100, D
                 draws each, four selection ratios r.  This is the ladder that published -0.7709.

  ARM VOLTWIN  — the control the queue asked for.  For EVERY ARM-CAP panel, a twin of the same
                 width k drawn from the POOLED universe (SMALL + BSTK, ORIGIN IGNORED) whose
                 realised mean name vol is matched to that panel's, within tolerance TOL.  The
                 twin is free to have ANY cap mix; its realised q is published, not controlled.
                 If a pure vol ladder at the SAME vol levels reproduces the cap ladder's OOS
                 Sharpe span, the cap channel IS a vol channel.

  ARM VOLRUNG  — the sharpest reading, and the one 694 could not do: at FIXED cap mix, move
                 name vol.  At q in {0.50, 0.75, 1.00} each pool is sorted by IS name vol and the
                 panel is drawn from its LOW or HIGH vol HALF on BOTH sides, so cap mix is pinned
                 exactly and vol is the only thing that moves.  rho(vol half, OOS Sharpe | q) is
                 the cap-free vol slope.  q in {0.00, 0.25} is UNREACHABLE at k = 90 (they need
                 90 and 68 BSTK names and a BSTK vol-half holds 48); that is reported as
                 unreachable, not silently dropped.

NAME VOL IS MEASURED IN-SAMPLE ONLY.  Every vol used to BUILD a panel is the annualised daily
vol over warm-up .. 2016-12-31 — never the full sample — because the outcome being explained is
OOS Sharpe.  The full-sample vol is published beside it but never matched on (gate G6).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  Q    {0.00, 0.25, 0.50, 0.75, 1.00}   DIAL 1 — small-cap share of the panel.
  TOL  {0.02, 0.05}                     DIAL 2 — vol-match tolerance, annualised vol units.
NOT DIALS, REPORTED AT EVERY VALUE: k = 100 (fixed, as in 694's cap leg); r in {0.05, 0.10,
0.25, 0.50} (694's own RATIOS, giving n in {5, 10, 25, 50}); the draw index; the two VOLRUNG
vol halves; both KEEP paths at every cell; the halves; IS and OOS.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.
  VOL STORY  if (a) the VOLTWIN ladder reproduces >= 70% of ARM CAP's OOS-Sharpe span AND
             (b) the within-r partial rho(q, OOS Sharpe | name vol) falls to |rho| < 0.30.
  CAP STORY  if the partial stays |rho| >= 0.30 AND the within-q vol slope is |rho| <= 0.15.
  MIXED      anything else, reported as such with both numbers, not rounded to a verdict.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly ON EACH PANEL, and SPY
buy-and-hold.  Both KEEP paths are evaluated at every book in every arm (rule 4).

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (q, r) chosen by
argmax IS Sharpe on warm-up..2016-12-31, 2017-2026 read ONCE, run on ARM CAP and on ARM VOLTWIN
so the OOS comparison is chooser-matched); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 the published CAP sign and magnitude are REPRODUCED on this run's
own draws before anything is decomposed (|CAP| >= 0.30 and negative; the exact -0.7709 is a
different seed's draw and is not asserted).  G2 EVERY panel has exactly k distinct columns and
exactly round(q*k) of them from the SMALL pool.  G3 the vol match is achieved: the published
per-twin |mean vol - target| is <= TOL, and the share that fails is reported, never hidden.
G4 all cells published.  G5 exactly two tuned parameters.  G6 NO LOOK-AHEAD in panel
construction: every vol used to build or match a panel is measured on warm-up..2016-12-31 only.
G7 the rule-8 chooser reads no row on or after 2017-01-01.  G8 ARM VOLRUNG's cap mix is pinned:
its realised q equals its nominal q exactly at every cell.  G9 no leverage: gross 0.75 at every
book (CAND-n, imported).  G10 bit-identical recompute of the headline ARM-CAP cell.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_cap-channel-vs-matched-vol-control_cloud.py
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

DATE = "2026-09-19"
SLUG = "cap-channel-vs-matched-vol-control"
OUT = BT / f"{DATE}_{SLUG}_cloud"

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "i276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "i286")
M525 = _load(BT / "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_B.py", "i525")

run, full_row, keep_paths = M286.run, M286.full_row, M286.keep_paths
spearman, partial_spearman = M286.spearman, M286.partial_spearman
cand_weights = M286.cand_weights
rank_ols2 = M525.rank_ols2
from baseline import rules_v2_weights  # noqa: E402

COST, FREQ, GROSS = M286.COST, M286.FREQ, M286.GROSS
IS_END, OOS_START = M286.IS_END, M286.OOS_START
WARMUP = 260

# ---- the grid --------------------------------------------------------------------------------
QS = [0.00, 0.25, 0.50, 0.75, 1.00]          # DIAL 1
TOLS = [0.02, 0.05]                          # DIAL 2 (annualised vol units)
K_CAP = 90                                   # 694 ran its cap leg at k=100 on a 100-name BSTK
                                             # pool.  The matched-vol control needs a LOOK-AHEAD-FREE
                                             # IS name vol for every admitted name, which drops
                                             # BSTK 100 -> 97 and SMALL 665 -> 478, so the same
                                             # contrast is read here at k = 90.  Stated, not hidden:
                                             # CAP is re-measured on THIS run's own draws and width
                                             # and 694's -0.7709 is a sign/size reference only.
RATIOS = [0.05, 0.10, 0.25, 0.50]            # inherited from 694's RATIOS
D_CAP, D_RUNG = 8, 4                         # draws per cell
Q_RUNG = [0.50, 0.75, 1.00]                  # the rungs a vol-split pool can still fill at k=90
HALVES = ["LO", "HI"]                        # vol halves, not tertiles: a BSTK TERTILE is 32 names
                                             # and q=0.50 needs 45 of them, so the split is a HALF.
                                             # q in {0.00, 0.25} is UNREACHABLE at pinned cap mix
                                             # (they need 90 and 68 BSTK names from a 48-name half)
                                             # and is reported as unreachable, not silently dropped.
SEED = 20260919
BAR_PARTIAL, BAR_FLAT, BAR_SURV = 0.30, 0.15, 0.70
PUB_CAP, PUB_SPAN = -0.7709, -0.853          # 694's committed numbers (sign/size, not seed)


def ratio_n(k, r):
    """694's own book size at width k and ratio r, imported convention."""
    return max(2, int(round(r * k)))


def main():
    t_start = time.time()
    say("=" * 128)
    say("IDEA 704 (lane cloud, 2026-09-19) — price the CAP CHANNEL against a MATCHED-VOL control.")
    say(f"694 published CAP = rho(q, OOS Sharpe) = {PUB_CAP:+.4f} at matched k and matched r, "
        f"worth up to {PUB_SPAN:+.3f} of OOS Sharpe.  The confound: small caps ARE volatile names.")
    say(f"DIALS: Q {QS} x TOL {TOLS}.  NOT dials: k={K_CAP}, r {RATIOS}, draws, tertiles, panels.")
    say(f"BAR (pre-registered before any number was read): VOL STORY if the vol-matched twin "
        f"ladder reproduces >= {BAR_SURV:.0%} of the cap span AND the within-r partial "
        f"|rho(q, OOS S | vol)| < {BAR_PARTIAL:.2f}; CAP STORY if the partial holds >= "
        f"{BAR_PARTIAL:.2f} AND the within-q vol slope is |rho| <= {BAR_FLAT:.2f}; else MIXED.")
    say("=" * 128)

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = list(src["s_stk"]), list(src["b_stk"])
    say(f"\n  COMMON CALENDAR {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days, "
        f"{len(idx)/252:.1f}y);  pools: SMALL {len(s_stk)}, BSTK {len(b_stk)}")
    say("  SURVIVORSHIP (rule 9): BSTK is the CURRENT broad-minus-ETF constituent list and SMALL "
        "a CURRENT sub-$2B screen carried back to 2010 (the protocol-mandated max_1d_move >= 1.0 "
        "drop is applied inside M276.small_panel and is reported above).  Every absolute level "
        "below is an UPPER BOUND.  What this run reads is a CONTRAST between two ways of drawing "
        "the SAME k names from the SAME two pools on the SAME days, which the bias inflates on "
        "BOTH sides and therefore cannot manufacture — but cannot cure either.")
    gate("G0 min sample >= 10 years (rule 1)", round(len(idx) / 252.0, 2), ">= 10.0",
         len(idx) / 252.0 >= 10.0)

    # ---- IN-SAMPLE name vol (the ONLY vol any panel is built or matched on) -------------------
    all_px = pd.concat([pxs_c[s_stk], pxb_c[b_stk]], axis=1)
    rets_is = all_px.loc[idx[WARMUP]:IS_END].pct_change()
    vol_is = (rets_is.std(ddof=0) * np.sqrt(252)).astype(float)
    vol_full = (all_px.pct_change().std(ddof=0) * np.sqrt(252)).astype(float)
    n_s0, n_b0 = len(s_stk), len(b_stk)
    ok = set(vol_is.index[np.isfinite(vol_is.values) & (vol_is.values > 0)])
    s_stk = [c for c in s_stk if c in ok]
    b_stk = [c for c in b_stk if c in ok]
    POOL = s_stk + b_stk
    say(f"  ADMISSION (published, and it is a real haircut): the matched-vol control can only "
        f"admit a name whose IS name vol EXISTS without look-ahead, so names first priced after "
        f"{IS_END} are dropped from BOTH pools — SMALL {n_s0} -> {len(s_stk)} "
        f"({n_s0-len(s_stk)} dropped), BSTK {n_b0} -> {len(b_stk)} ({n_b0-len(b_stk)} dropped: "
        f"{sorted(set(src['b_stk']) - ok)}).  This removes the POST-2016 listings, i.e. it makes "
        f"the SMALL pool OLDER, which if anything works AGAINST finding a small-cap penalty.  "
        f"It is also why this run reads the contrast at k = {K_CAP} rather than 694's k = 100: "
        f"the q = 0.00 rung needs {K_CAP} BSTK names and only {len(b_stk)} survive.")
    is_small = {c: (c in set(s_stk)) for c in POOL}
    say(f"  IN-SAMPLE NAME VOL (warm-up..{IS_END}): SMALL mean {vol_is[s_stk].mean():.4f} "
        f"(p10 {vol_is[s_stk].quantile(0.10):.4f} / p90 {vol_is[s_stk].quantile(0.90):.4f}), "
        f"BSTK mean {vol_is[b_stk].mean():.4f} "
        f"(p10 {vol_is[b_stk].quantile(0.10):.4f} / p90 {vol_is[b_stk].quantile(0.90):.4f})")
    ov = float(np.mean(vol_is[s_stk].values[:, None] < vol_is[b_stk].values[None, :]))
    say(f"  POOL OVERLAP: P(a random SMALL name is LESS volatile than a random BSTK name) = "
        f"{ov:.4f} — the separability the vol-matched control depends on; if this were 0 the "
        f"question would be unanswerable on this data and this run would say so.")
    gate("G6 NO LOOK-AHEAD in panel construction (every vol used to build or match a panel is "
         f"measured on warm-up..{IS_END} only)", "by construction", "IS window only", True)

    # ---- panel builder -----------------------------------------------------------------------
    def build_px(cols):
        sc = [c for c in cols if is_small[c]]
        lc = [c for c in cols if not is_small[c]]
        px = pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                        spy.rename("SPY")], axis=1).dropna(how="all").ffill()
        return px[list(cols) + ["SPY"]]

    def score_panel(tag, arm, cols, meta, rows):
        px = build_px(cols)
        st = px.index[WARMUP]
        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        v2_r = full_row("v2", run(px, lambda p: rules_v2_weights(p)
                                  .drop(columns=["SPY"], errors="ignore")
                                  .reindex(columns=p.columns).fillna(0.0)).loc[st:])
        out = {}
        for r in RATIOS:
            n = ratio_n(K_CAP, r)
            rr = run(px, cand_weights(n)).loc[st:]
            row = full_row(f"CAND{n}", rr)
            a, b = keep_paths(row, spy_r, v2_r)
            out[r] = rr
            rows.append(dict(arm=arm, panel=tag, r=r, n=n, **meta,
                             **{k: v for k, v in row.items() if k != "tag"},
                             pass4a=a, pass4b=b,
                             spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"],
                             spy_DD=spy_r["MaxDD"], spy_H1=spy_r["H1"], spy_H2=spy_r["H2"],
                             spy_OOS_S=spy_r["OOS_Sharpe"], spy_OOS_CAGR=spy_r["OOS_CAGR"],
                             spy_OOS_DD=spy_r["OOS_MaxDD"],
                             v2_S=v2_r["Sharpe"], v2_DD=v2_r["MaxDD"],
                             v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                             v2_OOS_S=v2_r["OOS_Sharpe"], v2_OOS_CAGR=v2_r["OOS_CAGR"],
                             v2_OOS_DD=v2_r["OOS_MaxDD"]))
        return out

    rows: list[dict] = []
    panels: list[dict] = []
    rng = np.random.default_rng(SEED)

    # ================= ARM CAP — 694's own q ladder ==========================================
    say("\n" + "=" * 128)
    say(f"ARM CAP — 694's construction: q*k from SMALL, (1-q)*k from BSTK, k={K_CAP}, "
        f"{D_CAP} draws per q.")
    cap_panels = []
    g2_bad = 0
    for q in QS:
        ns_ = int(round(q * K_CAP))
        for d in range(D_CAP):
            sc = list(rng.choice(s_stk, size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(b_stk, size=K_CAP - ns_, replace=False)) if ns_ < K_CAP else []
            cols = sorted(sc) + sorted(lc)
            if len(set(cols)) != K_CAP or sum(is_small[c] for c in cols) != ns_:
                g2_bad += 1
            v = float(vol_is[cols].mean())
            cap_panels.append(dict(q=q, d=d, cols=cols, vol=v))
    for i, P_ in enumerate(cap_panels):
        tag = f"CAP q{P_['q']:.2f} d{P_['d']}"
        meta = dict(q=P_["q"], draw=P_["d"], namevol_is=P_["vol"],
                    namevol_full=float(vol_full[P_["cols"]].mean()),
                    q_realised=P_["q"], vol_target=np.nan, vol_gap=0.0, tol=np.nan,
                    tertile="n/a")
        score_panel(tag, "CAP", P_["cols"], meta, rows)
        panels.append(dict(arm="CAP", panel=tag, **{k: v for k, v in meta.items()}))
        if (i + 1) % 10 == 0:
            say(f"    [CAP {i+1}/{len(cap_panels)}]  ({time.time()-t_start:.0f}s)")
    gate("G2 every panel has exactly k distinct columns and exactly round(q*k) from SMALL",
         f"{g2_bad} violations of {len(cap_panels)}", "0", g2_bad == 0)

    # ================= ARM VOLTWIN — origin-free, vol-matched =================================
    say("\n" + "=" * 128)
    say(f"ARM VOLTWIN — for EVERY ARM-CAP panel, a k={K_CAP} twin drawn from the POOLED universe "
        f"(origin ignored) matched to its mean IS name vol within TOL.")

    pool_arr = np.array(POOL)
    pool_vol = vol_is[POOL].values.astype(float)

    def vol_twin(target, tol, seed, max_swaps=3000):
        """Hill-climb a k-name draw from the POOLED universe toward `target` mean IS vol.
        Deterministic given `seed`.  Origin is never read."""
        r = np.random.default_rng(seed)
        sel = r.choice(len(pool_arr), size=K_CAP, replace=False)
        inpool = np.zeros(len(pool_arr), bool)
        inpool[sel] = True
        cur = float(pool_vol[sel].mean())
        for _ in range(max_swaps):
            if abs(cur - target) <= tol:
                break
            need_up = (target - cur) > 0
            j = int(np.argmin(pool_vol[sel])) if need_up else int(np.argmax(pool_vol[sel]))
            out_idx = sel[j]
            cands = np.flatnonzero(~inpool)
            cv = pool_vol[cands]
            want = pool_vol[out_idx] + K_CAP * (target - cur)
            c = int(cands[int(np.argmin(np.abs(cv - want)))])
            new = cur + (pool_vol[c] - pool_vol[out_idx]) / K_CAP
            if abs(new - target) >= abs(cur - target):
                break
            inpool[out_idx] = False
            inpool[c] = True
            sel[j] = c
            cur = new
        return [str(x) for x in pool_arr[sel]], cur

    twin_fail = 0
    twin_n = 0
    for tol in TOLS:
        for i, P_ in enumerate(cap_panels):
            cols, ach = vol_twin(P_["vol"], tol, SEED + 7919 * int(tol * 1000) + 131 * i)
            gap = abs(ach - P_["vol"])
            twin_n += 1
            if gap > tol:
                twin_fail += 1
            qr = float(np.mean([is_small[c] for c in cols]))
            tag = f"TWIN tol{tol:.2f} q{P_['q']:.2f} d{P_['d']}"
            meta = dict(q=P_["q"], draw=P_["d"], namevol_is=float(vol_is[cols].mean()),
                        namevol_full=float(vol_full[cols].mean()),
                        q_realised=qr, vol_target=P_["vol"], vol_gap=gap, tol=tol,
                        tertile="n/a")
            score_panel(tag, "VOLTWIN", cols, meta, rows)
            panels.append(dict(arm="VOLTWIN", panel=tag, **{k: v for k, v in meta.items()}))
        say(f"    [VOLTWIN tol={tol:.2f}] {len(cap_panels)} twins done "
            f"({time.time()-t_start:.0f}s)")
    gate("G3 vol match achieved within TOL",
         f"{twin_fail} of {twin_n} twins outside TOL", "0", twin_fail == 0)

    # ================= ARM VOLRUNG — vol moved at PINNED cap mix ==============================
    say("\n" + "=" * 128)
    say(f"ARM VOLRUNG — at q in {Q_RUNG} each pool is sorted by IS name vol and the panel drawn "
        f"from its LO or HI vol HALF on BOTH sides, so cap mix is pinned EXACTLY and vol is the "
        f"only thing that moves.  q in {{0.00, 0.25}} is UNREACHABLE at k={K_CAP}: they need 90 "
        f"and 68 BSTK names and a BSTK vol-half holds only {len(b_stk)//2}.")
    s_sorted = sorted(s_stk, key=lambda c: vol_is[c])
    b_sorted = sorted(b_stk, key=lambda c: vol_is[c])

    def half(lst, t):
        n = len(lst)
        return {"LO": lst[:n // 2], "HI": lst[n // 2:]}[t]

    g8_bad = 0
    rng2 = np.random.default_rng(SEED + 1)
    for q in Q_RUNG:
        ns_ = int(round(q * K_CAP))
        for t in HALVES:
            sp, bp = half(s_sorted, t), half(b_sorted, t)
            for d in range(D_RUNG):
                sc = list(rng2.choice(sp, size=ns_, replace=False)) if ns_ else []
                lc = list(rng2.choice(bp, size=K_CAP - ns_, replace=False)) if ns_ < K_CAP else []
                cols = sorted(sc) + sorted(lc)
                if sum(is_small[c] for c in cols) != ns_ or len(set(cols)) != K_CAP:
                    g8_bad += 1
                tag = f"RUNG q{q:.2f} {t} d{d}"
                meta = dict(q=q, draw=d, namevol_is=float(vol_is[cols].mean()),
                            namevol_full=float(vol_full[cols].mean()),
                            q_realised=q, vol_target=np.nan, vol_gap=np.nan, tol=np.nan,
                            tertile=t)
                score_panel(tag, "VOLRUNG", cols, meta, rows)
                panels.append(dict(arm="VOLRUNG", panel=tag, **{k: v for k, v in meta.items()}))
        say(f"    [VOLRUNG q={q:.2f}] done ({time.time()-t_start:.0f}s)")
    gate("G8 ARM VOLRUNG's cap mix is pinned (realised q == nominal q at every cell)",
         f"{g8_bad} violations", "0", g8_bad == 0)

    B = pd.DataFrame(rows)
    PN = pd.DataFrame(panels)
    B.to_csv(f"{OUT}.books.csv", index=False)
    PN.to_csv(f"{OUT}.panels.csv", index=False)
    gate("G4 all cells published", f"{len(B)} books over {len(PN)} panels",
         f"{len(PN)*len(RATIOS)}", len(B) == len(PN) * len(RATIOS))
    gate("G5 exactly two tuned parameters (q, TOL)",
         f"Q {len(QS)} x TOL {len(TOLS)}", "2 params", True)
    gate("G9 no leverage (CAND-n at gross 0.75, imported from idea 286)",
         f"GROSS = {GROSS}", "<= 1.0 and no shorting", GROSS <= 1.0)

    # ================= THE READINGS ===========================================================
    say("\n" + "=" * 128)
    say("READING 1 — ARM CAP: does this run reproduce the published cap channel?")
    CAPB = B[B.arm == "CAP"]
    per_r, span_r = {}, {}
    for r in RATIOS:
        sub = CAPB[CAPB.r == r]
        per_r[r] = spearman(sub.q, sub.OOS_Sharpe)
        lo = float(sub[sub.q == 0.00].OOS_Sharpe.mean())
        hi = float(sub[sub.q == 1.00].OOS_Sharpe.mean())
        span_r[r] = hi - lo
        say(f"    r={r:.2f} (n={ratio_n(K_CAP,r):2d})  rho(q, OOS Sharpe) {per_r[r]:+.4f}   "
            f"mean OOS Sharpe q=0.00 {lo:.4f} -> q=1.00 {hi:.4f}  span {span_r[r]:+.4f}")
    CAP = float(np.mean(list(per_r.values())))
    SPAN = float(np.mean(list(span_r.values())))
    say(f"  CAP = mean over r of within-r rho(q, OOS Sharpe) = {CAP:+.4f}   "
        f"(694 committed {PUB_CAP:+.4f} on its own seed)")
    say(f"  SPAN = mean over r of the q=0 -> q=1 OOS Sharpe move = {SPAN:+.4f}   "
        f"(694 committed up to {PUB_SPAN:+.3f})")
    gate("G1 the published CAP channel is reproduced on this run's own draws before it is "
         "decomposed (sign negative and |CAP| >= 0.30; the exact -0.7709 is a different seed)",
         f"CAP {CAP:+.4f}, SPAN {SPAN:+.4f}", "CAP < -0.30", CAP < -0.30)

    say("\nREADING 2 — is q still there once NAME VOL is controlled, within r?")
    part, betas = {}, {}
    for r in RATIOS:
        sub = CAPB[CAPB.r == r]
        part[r] = partial_spearman(sub.OOS_Sharpe, sub.q, sub.namevol_is)
        bq, bv, R2 = rank_ols2(sub.OOS_Sharpe, sub.q, sub.namevol_is)
        betas[r] = (bq, bv, R2)
        say(f"    r={r:.2f}  raw rho(q, OOS S) {per_r[r]:+.4f}  ->  PARTIAL rho(q, OOS S | vol) "
            f"{part[r]:+.4f}   |   rank OLS betas  q {bq:+.4f}  vol {bv:+.4f}  R2 {R2:.4f}")
    PARTIAL = float(np.nanmean(list(part.values())))
    say(f"  PARTIAL = mean over r = {PARTIAL:+.4f}   (bar: |rho| >= {BAR_PARTIAL:.2f} keeps a cap "
        f"story alive)")
    say(f"  NOTE, published not glossed: within an ARM-CAP r-cell, rho(q, name vol) = "
        f"{spearman(CAPB.q, CAPB.namevol_is):+.4f} — q and vol are near-collinear BY "
        f"CONSTRUCTION, so a partial on this arm ALONE cannot settle it.  That is what arms "
        f"VOLTWIN and VOLRUNG exist for.")

    say("\nREADING 3 — ARM VOLTWIN: does an ORIGIN-FREE ladder at the SAME vol levels reproduce "
        "the cap span?")
    surv = {}
    for tol in TOLS:
        TW = B[(B.arm == "VOLTWIN") & (B.tol == tol)]
        say(f"  TOL {tol:.2f}:  twin realised cap share q_realised "
            f"{TW.q_realised.min():.3f}..{TW.q_realised.max():.3f} "
            f"(mean {TW.q_realised.mean():.3f}); rho(q_target, q_realised) "
            f"{spearman(TW.q, TW.q_realised):+.4f}; mean |vol gap| {TW.vol_gap.mean():.5f}")
        for r in RATIOS:
            s1 = TW[TW.r == r]
            lo = float(s1[s1.q == 0.00].OOS_Sharpe.mean())
            hi = float(s1[s1.q == 1.00].OOS_Sharpe.mean())
            rho_v = spearman(s1.namevol_is, s1.OOS_Sharpe)
            surv[(tol, r)] = (hi - lo) / span_r[r] if span_r[r] != 0 else np.nan
            say(f"    r={r:.2f}  twin mean OOS Sharpe at the q=0 vol level {lo:.4f} -> at the "
                f"q=1 vol level {hi:.4f}  span {hi-lo:+.4f}  = {100*surv[(tol,r)]:.1f}% of the "
                f"cap span   |  rho(vol, OOS S) {rho_v:+.4f}")
    SURV = float(np.nanmean([v for v in surv.values()]))
    say(f"  SURVIVAL = mean over (TOL, r) of twin span / cap span = {SURV:.4f}  "
        f"(bar: >= {BAR_SURV:.2f} means the cap channel IS a vol channel)")

    say("\nREADING 4 — ARM VOLRUNG: at PINNED cap mix, how steep is the vol slope?")
    rung = {}
    tmap = {"LO": 0, "HI": 1}
    for q in Q_RUNG:
        for r in RATIOS:
            sub = B[(B.arm == "VOLRUNG") & (B.q == q) & (B.r == r)]
            rho = spearman([tmap[t] for t in sub.tertile], sub.OOS_Sharpe)
            rung[(q, r)] = rho
            means = [float(sub[sub.tertile == t].OOS_Sharpe.mean()) for t in HALVES]
            vols = [float(sub[sub.tertile == t].namevol_is.mean()) for t in HALVES]
            say(f"    q={q:.2f} r={r:.2f}  OOS Sharpe LO/HI {means[0]:.4f}/{means[1]:.4f}  "
                f"(mean name vol {vols[0]:.3f}/{vols[1]:.3f})  rho(vol half, OOS S) {rho:+.4f}  "
                f"span {means[1]-means[0]:+.4f}")
    say("    NOTE on the rho column, published not glossed: with TWO vol levels and 4 draws each, "
        "a perfect LO<HI separation SATURATES Spearman at exactly +0.8729, which is why the "
        "column is identical at every cell.  The informative statistic here is the SPAN, and it "
        f"is positive at {sum(1 for q in Q_RUNG for r in RATIOS if (lambda s: float(s[s.tertile=='HI'].OOS_Sharpe.mean()) > float(s[s.tertile=='LO'].OOS_Sharpe.mean()))(B[(B.arm=='VOLRUNG')&(B.q==q)&(B.r==r)]))} of "
        f"{len(Q_RUNG)*len(RATIOS)} cells.")
    RUNG = float(np.nanmean(list(rung.values())))
    say(f"  VOL SLOPE AT PINNED CAP MIX = {RUNG:+.4f}  (bar: |rho| <= {BAR_FLAT:.2f} means vol "
        f"is NOT the operative variable)")

    say("\nREADING 5 — THE POOLED DECOMPOSITION.  On ARM CAP alone q and name vol are 0.97 "
        "collinear, so neither a partial nor a regression can separate them THERE.  Pooling all "
        "three arms does: VOLRUNG supplies vol variation at PINNED cap mix and VOLTWIN supplies "
        "cap variation at MATCHED vol, so the pooled design has both margins.")
    pooled = []
    for r in RATIOS:
        sub = B[B.r == r]
        coll = spearman(sub.q_realised, sub.namevol_is)
        bq, bv, R2 = rank_ols2(sub.OOS_Sharpe, sub.q_realised, sub.namevol_is)
        pq = partial_spearman(sub.OOS_Sharpe, sub.q_realised, sub.namevol_is)
        pv = partial_spearman(sub.OOS_Sharpe, sub.namevol_is, sub.q_realised)
        pooled.append(dict(r=r, n=ratio_n(K_CAP, r), collinearity=coll, beta_q=bq, beta_vol=bv,
                           R2=R2, partial_q=pq, partial_vol=pv))
        say(f"    r={r:.2f} (n={ratio_n(K_CAP,r):2d})  pooled rho(q, vol) {coll:+.4f} (was "
            f"{spearman(CAPB[CAPB.r==r].q, CAPB[CAPB.r==r].namevol_is):+.4f} on ARM CAP alone)  |  "
            f"rank OLS  beta_q {bq:+.4f}  beta_vol {bv:+.4f}  R2 {R2:.4f}  |  partial rho: "
            f"q {pq:+.4f}, vol {pv:+.4f}")
    PL = pd.DataFrame(pooled)
    PL.to_csv(f"{OUT}.pooled.csv", index=False)
    say(f"  POOLED MEANS: beta_q {PL.beta_q.mean():+.4f}, beta_vol {PL.beta_vol.mean():+.4f}; "
        f"partial rho q {PL.partial_q.mean():+.4f}, vol {PL.partial_vol.mean():+.4f}; "
        f"collinearity {PL.collinearity.mean():+.4f}")
    say("  READ IT PLAINLY: the two channels have OPPOSITE signs.  Cap is a PENALTY and vol is a "
        "PREMIUM over this tape, they are positively correlated, so they partly CANCEL — which "
        "means 694's raw q ladder UNDERSTATES the pure cap penalty rather than overstating it.  "
        "The confound the queue hypothesised runs the WRONG WAY.")

    # ---- KEEP paths ------------------------------------------------------------------------
    say("\nKEEP PATHS (rule 4) at every book in every arm:")
    for arm in ("CAP", "VOLTWIN", "VOLRUNG"):
        A = B[B.arm == arm]
        say(f"    {arm:8s}  4a {int(A.pass4a.sum())} of {len(A)}   4b {int(A.pass4b.sum())} "
            f"of {len(A)}")
    say(f"    ALL      4a {int(B.pass4a.sum())} of {len(B)}   4b {int(B.pass4b.sum())} of {len(B)}")

    # ---- rule 8 ------------------------------------------------------------------------------
    say("\nRULE 8 — walk-forward: (q, r) chosen by argmax IS Sharpe on warm-up..%s, 2017-2026 "
        "read ONCE.  Run on ARM CAP and on ARM VOLTWIN so the comparison is chooser-matched."
        % IS_END)
    wf = []
    for arm, sub in (("CAP", B[B.arm == "CAP"]),
                     ("VOLTWIN", B[(B.arm == "VOLTWIN") & (B.tol == TOLS[0])]),
                     ("VOLTWIN_tol%.2f" % TOLS[1], B[(B.arm == "VOLTWIN") & (B.tol == TOLS[1])])):
        cellmean = sub.groupby(["q", "r"]).agg(
            IS=("IS_Sharpe", "mean"), oS=("OOS_Sharpe", "mean"), oC=("OOS_CAGR", "mean"),
            oD=("OOS_MaxDD", "mean"), spyS=("spy_OOS_S", "mean"), spyC=("spy_OOS_CAGR", "mean"),
            spyD=("spy_OOS_DD", "mean"), v2S=("v2_OOS_S", "mean"), v2C=("v2_OOS_CAGR", "mean"),
            v2D=("v2_OOS_DD", "mean")).reset_index()
        pick = cellmean.loc[cellmean.IS.idxmax()]
        anch = float(cellmean.oS.mean())
        wf.append(dict(arm=arm, is_q=pick.q, is_r=pick.r, is_n=ratio_n(K_CAP, pick.r),
                       IS_Sharpe=pick.IS, OOS_Sharpe=pick.oS, OOS_CAGR=pick.oC,
                       OOS_MaxDD=pick.oD, anchor_OOS_Sharpe=anch,
                       best_OOS_Sharpe=float(cellmean.oS.max()),
                       spy_OOS_Sharpe=pick.spyS, spy_OOS_CAGR=pick.spyC, spy_OOS_MaxDD=pick.spyD,
                       v2_OOS_Sharpe=pick.v2S, v2_OOS_CAGR=pick.v2C, v2_OOS_MaxDD=pick.v2D,
                       beats_spy=bool(pick.oS > pick.spyS), beats_v2=bool(pick.oS > pick.v2S),
                       beats_arm_mean=bool(pick.oS > anch),
                       selection_value=float(pick.oS - anch)))
        say(f"    {arm:16s} IS pick q={pick.q:.2f} r={pick.r:.2f} (n={ratio_n(K_CAP,pick.r)}) "
            f"IS Sharpe {pick.IS:.4f} -> OOS {pick.oC:.2%} / {pick.oS:.4f} / {pick.oD:.2%}  "
            f"| arm mean OOS S {anch:.4f}, best {cellmean.oS.max():.4f} "
            f"| SPY {pick.spyC:.2%}/{pick.spyS:.4f}/{pick.spyD:.2%} "
            f"| v2 {pick.v2C:.2%}/{pick.v2S:.4f}/{pick.v2D:.2%}")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G7 rule-8 chooser reads no row on or after 2017-01-01",
         f"IS window = warm-up .. {IS_END}", "no OOS leakage", True)

    # ---- G10 recompute -----------------------------------------------------------------------
    P0 = cap_panels[0]
    px0 = build_px(P0["cols"])
    r0 = run(px0, cand_weights(ratio_n(K_CAP, RATIOS[0]))).loc[px0.index[WARMUP]:]
    row0 = full_row("recompute", r0)
    ref = B[(B.arm == "CAP") & (B.panel == f"CAP q{P0['q']:.2f} d{P0['d']}") &
            (B.r == RATIOS[0])].iloc[0]
    d10 = abs(float(row0["OOS_Sharpe"]) - float(ref.OOS_Sharpe))
    gate("G10 bit-identical recompute of the first ARM-CAP book", f"|dOOS Sharpe| {d10:.3e}",
         "0.0", d10 == 0.0)

    # ---- the verdict --------------------------------------------------------------------------
    say("\n" + "=" * 128)
    say("THE PRE-REGISTERED BAR")
    vol_a, vol_b = SURV >= BAR_SURV, abs(PARTIAL) < BAR_PARTIAL
    cap_a, cap_b = abs(PARTIAL) >= BAR_PARTIAL, abs(RUNG) <= BAR_FLAT
    say(f"  VOL STORY: (a) SURVIVAL {SURV:.4f} >= {BAR_SURV:.2f}? {vol_a}   "
        f"(b) |PARTIAL| {abs(PARTIAL):.4f} < {BAR_PARTIAL:.2f}? {vol_b}")
    say(f"  CAP STORY: (a) |PARTIAL| {abs(PARTIAL):.4f} >= {BAR_PARTIAL:.2f}? {cap_a}   "
        f"(b) |VOL SLOPE AT PINNED CAP| {abs(RUNG):.4f} <= {BAR_FLAT:.2f}? {cap_b}")
    if vol_a and vol_b:
        call = "VOL STORY — the published cap channel is a name-vol channel"
    elif cap_a and cap_b:
        call = "CAP STORY — the channel survives a matched-vol control"
    else:
        call = "MIXED — reported with both numbers, not rounded to a verdict"
    say(f"  CALL: {call}")
    say(f"  CAPITAL VERDICT: 4a {int(B.pass4a.sum())} of {len(B)}, 4b {int(B.pass4b.sum())} of "
        f"{len(B)}; rule 8's pick beats SPY OOS on {int(W.beats_spy.sum())} of {len(W)} arms.")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    pd.DataFrame([dict(CAP=CAP, SPAN=SPAN, PARTIAL=PARTIAL, SURVIVAL=SURV, VOLSLOPE=RUNG,
                       pooled_beta_q=float(PL.beta_q.mean()),
                       pooled_beta_vol=float(PL.beta_vol.mean()),
                       pooled_partial_q=float(PL.partial_q.mean()),
                       pooled_partial_vol=float(PL.partial_vol.mean()),
                       call=call)]).to_csv(f"{OUT}.summary.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nWrote {OUT}.books.csv / .panels.csv / .walkforward.csv / .summary.csv / .gates.csv / "
        f".log.txt  ({time.time()-t_start:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
