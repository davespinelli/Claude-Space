#!/usr/bin/env python3
"""SUNDAY REVIEW 2026-09-20 — the promotion stress on the record's only BOTH-PATHS cell.

WHY THIS RUN EXISTS
    The Sunday review must pick the strongest standing KEEP-candidate, re-run its script, and
    promote it only if it beats the LIVE book (RULES v2) in both halves and out of sample.
    Parsing LEADERBOARD.md's KEEP-candidate rows by min(H1, H2) Sharpe puts one row first:

        idea 142 by-product, `u56 / S3-50 / band3-rw @10 bps`
        committed 2026-09-08: 11.27% / 1.2624 / -11.63%, halves 1.279 / 1.249, OOS 1.2886

    It is one of only two rows in the record to clear PROTOCOL path 4a (against the LIVE v2 book)
    AND path 4b at the same time.  Its own script was re-run today and it reproduces (see
    2026-09-20_SUNDAY-reverify-idea142.console.txt).

    But idea 142 priced it at ONE cost rung pair (10 / 25 bps) and, like every row in that run,
    at t+1 execution ONLY.  Today's own CHANGELOG (idea 2046) closes with a standing note: any
    4a claim must publish its EXECUTION DELAY, because latency — not cost — is what kills 4a
    passes in this record.  This run supplies exactly the two ladders the promotion decision
    needs, on the candidate itself, before any rule is touched.

THE QUESTION
    Does the both-paths pass of `S3-50 + band3-rw` survive the COST ladder {5, 10, 25, 50} bps
    and the EXECUTION-DELAY ladder {t+1, t+2, t+3}, jointly, against the LIVE book scored at the
    SAME cost and the SAME delay?

CONSTRUCTION
    PANEL {u56, broad} x COST {5, 10, 25, 50} x DELAY {t+1, t+2, t+3} = 24 candidate cells, all
    published.  The book is idea 133's `S3-50` (ranked top-20 blended 50/50 with the TLT/GLD/UUP
    sleeve, rescaled to gross 0.75) under idea 94's `band3` gate in the RE-WEIGHT convention,
    weekly, IMPORTED from those scripts, never re-implemented.  Delay d is applied by shifting
    the target-weight frame by (d - 1) extra rows before the harness's own t+1 application, so
    d = 1 is the committed convention exactly.
    COMPARANDS, both scored at the same cost and the same delay as the cell:
        RULES v2 (the live book) via baseline.rules_v2_weights   -> path 4a
        SPY buy & hold (delay-free by construction)              -> path 4b
    NOTHING IS TUNED.  Cost, delay and panel are reported axes, never selected on; the book's
    own dials (n = 20, blend 0.50, band 3%, gross 0.75) are frozen at idea 142's committed values.

GATES (printed before any hypothesis is read)
    G1  the harness with every instrument off reproduces engine.backtest (the live convention).
    G2  the (u56, 10 bps, t+1) cell reproduces today's re-run of idea 142 to < 5e-3 on
        CAGR / Sharpe / MaxDD / H1 / H2 / OOS Sharpe.
    G3  d = 1 is a no-op shift: the d = 1 book is identical to the unshifted book (0.0).
    G4  every one of the 24 cells is published, pass or fail.

CAVEATS carried
    Survivorship (idea 54): u56 and broad are CURRENT constituents, so every CAGR level is
    optimistic and both 4b bars are easier than on a point-in-time panel.  The cost x delay
    CONTRASTS are same-tape / same-names and first-order immune; the PASS COUNTS are not.
    Deterministic, standalone.  Writes .console.txt and .grid.csv next to itself.  Modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-20_sunday-cost-latency-stress-of-the-both-paths-cell_REVIEW"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"

COSTS = [5.0, 10.0, 25.0, 50.0]
DELAYS = [1, 2, 3]
PANELS = ["u56", "broad"]
BOOK, GATE, CONV = "S3-50", "band3", "rw"
PHI0, DELTA0 = 0.70, 0.60          # 4b's CAGR floor and MaxDD cap multipliers (PROTOCOL 4b)

# committed reference for G2: today's re-run of idea 142, u56 / S3-50 / band3-rw / 10 bps / t+1
REF142 = dict(CAGR=0.11264347733520674, Sharpe=1.2631836842789088, MaxDD=-0.11630008422595184,
              H1=1.2821692801839668, H2=1.2472607800728146, OOS_Sharpe=1.288118742321921)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
D = _load(I133, "i133")
FREQ, OOS_START = H.FREQ, H.OOS_START

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def delayed(W, d):
    """t+d execution.  The harness already applies the frame at t+1, so shift by d-1."""
    return W if d == 1 else W.shift(d - 1)


def main():
    say(f"SUNDAY REVIEW {STEM}")
    say("cost x delay stress of the record's only both-paths cell, before any promotion\n")
    rows = []
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bars = H.bars_of(spy)
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        say(f"[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")
        say(f"    SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.4f}  MaxDD {ms['MaxDD']:.2%}"
            f"  halves {bars['s1']:.4f}/{bars['s2']:.4f}  OOS Sharpe {mso['Sharpe']:.4f}")
        say(f"    4b bars: CAGR floor {PHI0 * bars['scagr']:.2%}, MaxDD cap "
            f"{-DELTA0 * abs(bars['sdd']):.2%}, half-Sharpe {bars['s1']:.4f}/{bars['s2']:.4f}, "
            f"OOS Sharpe {bars['soos']:.4f}")

        Wc = D.book_weights(px, BOOK, GATE, CONV)
        Wv2 = rules_v2_weights(px)

        # ---- G1 harness == engine on the live book, committed convention
        g1 = float((H.run(px, Wv2, bps=10.0)["r"].loc[start:]
                    - backtest(px, Wv2, cost_bps=10.0, freq=FREQ)["returns"].loc[start:])
                   .abs().max())
        say(f"[G1] harness vs engine.backtest on RULES v2 @10bps: max|diff| {g1:.3e} "
            f"({'EXACT' if g1 < 1e-12 else 'NOT EXACT — unsafe'})")
        # ---- G3 d=1 is a no-op
        g3 = float((delayed(Wc, 1) - Wc).abs().max().max())
        say(f"[G3] d=1 shift is a no-op on the candidate frame: {g3:.3e}")

        for d in DELAYS:
            Wcd, Wvd = delayed(Wc, d), delayed(Wv2, d)
            for c in COSTS:
                res = H.run(px, Wcd, bps=c)
                r = res["r"].loc[start:]
                base = H.run(px, Wvd, bps=c)["r"].loc[start:]
                m, mo = metrics(r), metrics(r.loc[OOS_START:])
                h1, h2 = H.halves(r)
                b1, b2 = H.halves(base)
                mb, mbo = metrics(base), metrics(base.loc[OOS_START:])
                fail4b = []
                if not h1 > bars["s1"]:
                    fail4b.append("H1")
                if not h2 > bars["s2"]:
                    fail4b.append("H2")
                if not mo["Sharpe"] > bars["soos"]:
                    fail4b.append("OOS")
                if not abs(m["MaxDD"]) <= DELTA0 * abs(bars["sdd"]):
                    fail4b.append("DD")
                if not m["CAGR"] >= PHI0 * bars["scagr"]:
                    fail4b.append("CAGR")
                rows.append(dict(
                    panel=pk, delay=f"t+{d}", cost=c,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    TO=res["to"].loc[start:].sum() / m["Years"],
                    v2_CAGR=mb["CAGR"], v2_Sharpe=mb["Sharpe"], v2_MaxDD=mb["MaxDD"],
                    v2_H1=b1, v2_H2=b2, v2_OOS_Sharpe=mbo["Sharpe"],
                    pass4a_v2=bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= mb["MaxDD"]),
                    beats_v2_oos=bool(mo["Sharpe"] > mbo["Sharpe"]),
                    pass4b=(len(fail4b) == 0), fail4b=",".join(fail4b) or "-"))
        say("")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    ref = df[(df.panel == "u56") & (df.cost == 10.0) & (df.delay == "t+1")].iloc[0]
    g2 = max(abs(ref[k] - v) for k, v in REF142.items())
    say(f"[G2] (u56, 10 bps, t+1) vs today's idea-142 re-run: max|diff| {g2:.3e} "
        f"({'PASS' if g2 < 5e-3 else 'FAIL'})")
    say(f"[G4] cells published: {len(df)} of {len(PANELS) * len(COSTS) * len(DELAYS)}\n")

    cols = ["panel", "delay", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "TO",
            "v2_Sharpe", "v2_H1", "v2_H2", "v2_OOS_Sharpe", "pass4a_v2", "beats_v2_oos",
            "pass4b", "fail4b"]
    say("ALL 24 CELLS (the promotion test is: pass4a_v2 AND beats_v2_oos AND pass4b)")
    say(df[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    promo = df[df.pass4a_v2 & df.beats_v2_oos & df.pass4b]
    say(f"\n[VERDICT] cells clearing the Sunday promotion bar: {len(promo)} of {len(df)}")
    if len(promo):
        say(promo[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"  4a vs the live book:  {int(df.pass4a_v2.sum())} of {len(df)}")
    say(f"  beats the live book OOS: {int(df.beats_v2_oos.sum())} of {len(df)}")
    say(f"  4b (vs SPY):          {int(df.pass4b.sum())} of {len(df)}")
    u = df[df.panel == "u56"]
    say(f"  u56 only — 4a {int(u.pass4a_v2.sum())}/12, OOS {int(u.beats_v2_oos.sum())}/12, "
        f"4b {int(u.pass4b.sum())}/12, all three {int((u.pass4a_v2 & u.beats_v2_oos & u.pass4b).sum())}/12")
    say(f"  mean annual turnover, candidate {df.TO.mean():.2f}x")
    say("\nCAVEAT: u56/broad are CURRENT constituents (idea 54); every CAGR level is optimistic "
        "and both 4b bars are easier than on a point-in-time panel.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
