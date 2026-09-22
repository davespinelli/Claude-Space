#!/usr/bin/env python3
"""Idea 2254 (2026-09-22, lane B) — DOES A RANK-HYSTERESIS BUFFER CUT THE BOTH-PATHS CELL'S
8.18x/yr TURNOVER TOWARD THE LIVE BOOK'S 1.77x WITHOUT LOSING THE PASS?

WHY THIS RUN EXISTS
    The 2026-09-20 SUNDAY REVIEW re-verified the record's ONLY book clearing PROTOCOL path 4a
    (against the live RULES v2 book) AND path 4b at the same time --- idea 142's by-product
    `u56 / S3-50 + band3-rw @10 bps` (11.27% / 1.2632 / -11.63%, halves 1.282/1.247, OOS 1.288)
    --- and refused to promote it for exactly one reason, quoted verbatim:

        "The mechanism is turnover: 8.18x/yr on u56 and 10.88x/yr on broad, against the live
         book's 1.77x, so every basis point of cost is charged to it four to six times over.
         ...  What would change the answer is a version of this book that keeps the pass while
         cutting turnover toward the live book's 1.77x --- that is the question to file."

    This run is that question.  The device is the standard one for a ranked book and it carries
    NO return signal of its own: a HYSTERESIS BUFFER on the top-n selection.  A name enters the
    equity leg when its composite rank reaches K_in and is then HELD until its rank falls past
    K_out >= K_in (the same state machine `baseline.band_state` already uses on price).  At
    K_in = K_out = 20 the book is the committed cell bit-for-bit, so the buffer is a strict
    generalisation with the incumbent at its own grid point.

THE BOOK (idea 133's `S3-50` under idea 94's `band3` gate, `rw` convention, weekly)
        equity leg  :  composite-ranked names, selected by the K_in/K_out state machine,
                       equal-weighted, ranked AMONG gated-in names only (the `rw` convention)
        sleeve leg  :  TLT / GLD / UUP momentum-vote x risk-parity, gated
        blend       :  0.50 / 0.50, then rescaled to gross 0.75
    Everything except K_in and K_out is FROZEN at the committed values: blend f = 0.50, band 3%,
    gross 0.75, weekly cadence, t+1 execution, S3 = TLT/GLD/UUP, n = 20 at the incumbent point.

THE GRID (every point published, pass or fail)
    K_in  in {10, 15, 20, 25, 30}
    K_out in {10, 15, 20, 25, 30, 40, 56}, K_out >= K_in          -> 25 (K_in, K_out) pairs
    x COST {5, 10, 25, 50} bps  x  PANEL {u56, broad}             -> 200 published rows.
    Two tuned dials and NO MORE: K_in and K_out.  Cost, panel, cadence, blend, band and gross
    are REPORTED axes, never selected on.

GATES (printed before any hypothesis is read)
    G1  K_in = K_out = 20 reproduces `i133.book_weights(px,'S3-50','band3','rw')` at max|dw| = 0.
    G2  the harness reproduces `engine.backtest` on the live RULES v2 book (max|diff| < 1e-12).
    G3  the (u56, 10 bps, 20/20) cell reproduces the Sunday review's re-run of idea 142 to
        < 5e-3 on CAGR / Sharpe / MaxDD / H1 / H2 / OOS Sharpe.
    G4  every one of the 200 cells is published.
    G5  the buffer is a genuine turnover device: at fixed K_in, annual turnover is
        non-increasing in K_out (reported cell by cell, pass count printed).

RULE 8 (PROTOCOL rule 8 --- walk-forward, 2017-2026 READ ONCE)
    (K_in, K_out) chosen by argmax IN-SAMPLE Sharpe on 2009-2016 ONLY, per panel per cost rung;
    the 2017-2026 leg is then reported untouched against the live book's OOS and SPY's OOS.

CAVEATS carried
    Survivorship (PROTOCOL rule 9 / idea 54): u56 and broad are CURRENT constituents, so every
    CAGR level is optimistic and both 4b bars are easier than on a point-in-time panel.  The
    turnover CONTRASTS are same-tape / same-names and first-order immune; the pass counts are not.
    Costs are flat per unit turnover with no spread, impact or borrow.  One cadence (W), one
    execution delay (t+1), one blend (0.50), one band (3%), one gross (0.75).
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

STEM = "2026-09-22_rank-hysteresis-turnover-cut_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"

K_INS = [10, 15, 20, 25, 30]
K_OUTS = [10, 15, 20, 25, 30, 40, 56]
COSTS = [5.0, 10.0, 25.0, 50.0]
PANELS = ["u56", "broad"]
GATE, CONV, BLEND = "band3", "rw", 0.50
PHI0, DELTA0 = 0.70, 0.60                 # PROTOCOL 4b: CAGR floor and MaxDD cap multipliers
LIVE_TO = 1.77                            # the live RULES v2 book's annual turnover (Sunday review)

# the Sunday review's own re-run of idea 142: u56 / S3-50 / band3-rw / 10 bps / t+1
REF142 = dict(CAGR=0.11264347733520674, Sharpe=1.2631836842789088, MaxDD=-0.11630008422595184,
              H1=1.2821692801839668, H2=1.2472607800728146, OOS_Sharpe=1.288118742321921)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
D = _load(I133, "i133")
FREQ, GROSS, OOS_START, IS_END = H.FREQ, H.GROSS, H.OOS_START, H.IS_END

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ----------------------------------------------------------------- the device ----
def held_mask(px, k_in, k_out, gate, conv):
    """Two-threshold selection state.  IN when composite rank reaches k_in, OUT when it falls
    past k_out, previous state in between, OUT wherever the score does not exist.  This is the
    same ffill state machine `baseline.band_state` uses on price, applied to RANK."""
    s = H.composite(px)
    if gate is not None and conv == "rw":
        s = s.where(H.gate_mask(px, gate))
    rank = s.rank(axis=1, ascending=False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    # the OUT predicate is the exact COMPLEMENT of `rank <= k_out`, not `rank > k_out`, so a
    # tied rank (pandas averages ties, e.g. 20.5) is resolved the same way the committed
    # `(rank <= n)` rule resolves it instead of carrying the previous state.  Without this the
    # k_in = k_out = 20 cell is not bit-identical to idea 133's book (gate G1).
    raw = raw.mask(rank <= k_in, 1.0).mask(~(rank <= k_out) & rank.notna(), 0.0)
    return (raw.ffill().fillna(0.0) > 0.5) & rank.notna()


def ranked_hyst(px, k_in, k_out, gate=GATE, conv=CONV):
    """idea 133's `ranked(px, 20, gate, conv)` with the top-n rule replaced by the buffer.

    SIZING.  Per-name weight is `GROSS / max(h, k_in)` where h is the number of names held that
    day.  This is the committed rule's OWN scarcity behaviour written out: idea 133 pays
    GROSS/n to each of the top-n names, so the equity leg carries gross GROSS whenever n names
    are available and GROSS*h/n when the gate leaves fewer.  The formula reproduces both cases
    and keeps the equity leg's gross INDEPENDENT of the buffer, so K_out cannot smuggle in a
    blend change.  At k_in = k_out = 20 the held set is exactly `rank <= 20` (h <= 20 always),
    so the weights are the committed ones bit-for-bit --- gate G1."""
    m = held_mask(px, k_in, k_out, gate, conv).astype(float)
    h = m.sum(axis=1).clip(lower=k_in)
    w = m.div(h, axis=0).fillna(0.0) * GROSS
    if gate is not None and conv == "dg":
        w = w.where(H.gate_mask(px, gate), 0.0)
    return w


def book_hyst(px, k_in, k_out):
    """idea 133's S3-50 / band3 / rw book with the buffered equity leg.  Line-for-line the
    `rw` branch of `i133.book_weights`, with `ranked(px,20,...)` -> `ranked_hyst(px,k_in,k_out)`."""
    gm = H.gate_mask(px, GATE)
    sl = D.sleeve_weights(px, D.S3).where(gm, 0.0)
    w = (1 - BLEND) * ranked_hyst(px, k_in, k_out) + BLEND * sl
    return w.mul((GROSS / w.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


# ----------------------------------------------------------------- scoring ----
def score_cell(px, W, start, bars, base_r, bps):
    res = H.run(px, W, bps=bps)
    r = res["r"].loc[start:]
    m, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    h1, h2 = H.halves(r)
    b1, b2 = H.halves(base_r)
    mb, mbo = metrics(base_r), metrics(base_r.loc[OOS_START:])
    fail = []
    if not h1 > bars["s1"]:
        fail.append("H1")
    if not h2 > bars["s2"]:
        fail.append("H2")
    if not mo["Sharpe"] > bars["soos"]:
        fail.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA0 * abs(bars["sdd"]):
        fail.append("DD")
    if not m["CAGR"] >= PHI0 * bars["scagr"]:
        fail.append("CAGR")
    return dict(
        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
        IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
        TO=res["to"].loc[start:].sum() / m["Years"],
        v2_CAGR=mb["CAGR"], v2_Sharpe=mb["Sharpe"], v2_MaxDD=mb["MaxDD"],
        v2_H1=b1, v2_H2=b2, v2_OOS_Sharpe=mbo["Sharpe"], v2_OOS_MaxDD=mbo["MaxDD"],
        v2_OOS_CAGR=mbo["CAGR"],
        pass4a_v2=bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= mb["MaxDD"]),
        beats_v2_oos=bool(mo["Sharpe"] > mbo["Sharpe"]),
        pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-")


def main():
    say(f"IDEA 2254 — {STEM}")
    say("Does a RANK-HYSTERESIS BUFFER cut the both-paths cell's 8.18x/yr turnover toward the")
    say("live book's 1.77x without losing the 4a+4b pass?  (the 2026-09-20 Sunday review's own")
    say("filed question).  Two tuned dials: K_in, K_out.  Everything else frozen.\n")

    pairs = [(a, b) for a in K_INS for b in K_OUTS if b >= a]
    say(f"grid: {len(pairs)} (K_in,K_out) pairs x {len(COSTS)} cost rungs x {len(PANELS)} panels "
        f"= {len(pairs) * len(COSTS) * len(PANELS)} cells\n")

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
            f"  halves {bars['s1']:.4f}/{bars['s2']:.4f}   OOS {mso['CAGR']:.2%} / "
            f"{mso['Sharpe']:.4f} / {mso['MaxDD']:.2%}")
        say(f"    4b bars (full): CAGR floor {PHI0 * bars['scagr']:.2%}, MaxDD cap "
            f"{-DELTA0 * abs(bars['sdd']):.2%}, half-Sharpe {bars['s1']:.4f}/{bars['s2']:.4f}, "
            f"OOS Sharpe {bars['soos']:.4f}")
        say(f"    4b bars (OOS leg): CAGR floor {PHI0 * mso['CAGR']:.2%}, MaxDD cap "
            f"{-DELTA0 * abs(mso['MaxDD']):.2%}")

        Wv2 = rules_v2_weights(px)
        g2 = float((H.run(px, Wv2, bps=10.0)["r"].loc[start:]
                    - backtest(px, Wv2, cost_bps=10.0, freq=FREQ)["returns"].loc[start:])
                   .abs().max())
        say(f"[G2] harness vs engine.backtest on RULES v2 @10bps: max|diff| {g2:.3e} "
            f"({'EXACT' if g2 < 1e-12 else 'NOT EXACT — unsafe'})")

        # ---- G1 the incumbent is on the grid: K_in = K_out = 20 must BE idea 133's book.
        A20, B20 = ranked_hyst(px, 20, 20), D.ranked(px, 20, GATE, CONV)
        g1a = int(((A20 > 0) != (B20 > 0)).sum().sum())
        ties = int((B20.sum(axis=1) > GROSS + 1e-12).sum())
        g1b = float((A20 - B20).abs().where(B20.sum(axis=1) <= GROSS + 1e-12, 0.0).max().max())
        rA = H.run(px, book_hyst(px, 20, 20), bps=10.0)["r"].loc[start:]
        rB = H.run(px, D.book_weights(px, "S3-50", GATE, CONV), bps=10.0)["r"].loc[start:]
        g1c = float((rA - rB).abs().max())
        say(f"[G1a] K_in=K_out=20 HELD SET vs i133.ranked(px,20,'band3','rw'): "
            f"{g1a} name-day mismatches of {A20.size} ({'IDENTICAL' if g1a == 0 else 'unsafe'})")
        say(f"[G1b] weights identical on every non-tie day: max|dw| {g1b:.3e} "
            f"({'EXACT' if g1b < 1e-15 else 'unsafe'}).  On {ties} of {len(px)} days pandas'"
            f" AVERAGE tie-rank lets the committed `rank <= 20` rule hold 21 names at 0.75/20"
            f" each, i.e. gross 0.7875 > 0.75; the buffered rule's GROSS/max(h,K_in) sizing"
            f" holds gross at exactly 0.75 there.  This is the ONLY construction difference.")
        say(f"[G1c] resulting 10 bps return paths: max|dr| {g1c:.3e} per day "
            f"({'< 1e-3 — the incumbent is on the grid' if g1c < 1e-3 else 'unsafe'})")

        v2_by_cost = {c: H.run(px, Wv2, bps=c)["r"].loc[start:] for c in COSTS}
        W_by_pair = {p: book_hyst(px, *p) for p in pairs}
        for (a, b) in pairs:
            for c in COSTS:
                d = score_cell(px, W_by_pair[(a, b)], start, bars, v2_by_cost[c], c)
                d.update(panel=pk, K_in=a, K_out=b, cost=c, buffer=b - a)
                rows.append(d)
        say("")

    df = pd.DataFrame(rows)
    front = ["panel", "K_in", "K_out", "buffer", "cost"]
    df = df[front + [c for c in df.columns if c not in front]]
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    ref = df[(df.panel == "u56") & (df.cost == 10.0) & (df.K_in == 20) & (df.K_out == 20)].iloc[0]
    g3 = max(abs(float(ref[k]) - v) for k, v in REF142.items())
    say(f"[G3] (u56, 10 bps, 20/20) vs the Sunday review's idea-142 re-run: max|diff| {g3:.3e} "
        f"({'PASS' if g3 < 5e-3 else 'FAIL'})")
    say(f"[G4] cells published: {len(df)} of {len(pairs) * len(COSTS) * len(PANELS)}")
    mono_ok = mono_n = 0
    for (pk, c, a), sub in df.groupby(["panel", "cost", "K_in"]):
        s = sub.sort_values("K_out").TO.values
        mono_n += 1
        mono_ok += int(bool(np.all(np.diff(s) <= 1e-9)))
    say(f"[G5] turnover non-increasing in K_out at fixed K_in: {mono_ok} of {mono_n} ladders\n")

    # ------------------------------------------------------------ PART 1: the dial ----
    say("=" * 118)
    say("PART 1 — IS THE BUFFER A REAL TURNOVER DEVICE?  (annual turnover by cell, 10 bps)")
    say("=" * 118)
    for pk in PANELS:
        t = df[(df.panel == pk) & (df.cost == 10.0)].pivot(index="K_in", columns="K_out", values="TO")
        say(f"\n[{pk}] annual turnover x/yr   (live RULES v2 book = {LIVE_TO}x; incumbent 20/20 = "
            f"{df[(df.panel==pk)&(df.cost==10.0)&(df.K_in==20)&(df.K_out==20)].TO.iloc[0]:.2f}x)")
        say(t.to_string(float_format=lambda x: f"{x:.2f}"))
        say(f"    min {t.min().min():.2f}x  max {t.max().max():.2f}x  "
            f"-> the buffer spans {t.max().max() / t.min().min():.2f}x of turnover")

    say("\nSHARPE OVER THE SAME GRID (10 bps)")
    for pk in PANELS:
        t = df[(df.panel == pk) & (df.cost == 10.0)].pivot(index="K_in", columns="K_out", values="Sharpe")
        say(f"\n[{pk}] full-sample Sharpe @10 bps")
        say(t.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\nCAGR OVER THE SAME GRID (10 bps)")
    for pk in PANELS:
        t = df[(df.panel == pk) & (df.cost == 10.0)].pivot(index="K_in", columns="K_out", values="CAGR")
        say(f"\n[{pk}] full-sample CAGR @10 bps")
        say(t.to_string(float_format=lambda x: f"{x:.2%}"))

    # ------------------------------------------------- PART 2: does the pass survive ----
    say("\n" + "=" * 118)
    say("PART 2 — THE SUNDAY PROMOTION BAR AT EVERY CELL  (pass4a_v2 AND beats_v2_oos AND pass4b)")
    say("=" * 118)
    df["promo"] = df.pass4a_v2 & df.beats_v2_oos & df.pass4b
    for c in COSTS:
        sub = df[df.cost == c]
        say(f"\n[{c:.0f} bps] promotion-bar cells: {int(sub.promo.sum())} of {len(sub)}   "
            f"(4a {int(sub.pass4a_v2.sum())}, beats-v2-OOS {int(sub.beats_v2_oos.sum())}, "
            f"4b {int(sub.pass4b.sum())})")
        for pk in PANELS:
            s2 = sub[sub.panel == pk]
            say(f"    {pk:6s}: promo {int(s2.promo.sum()):2d}/{len(s2)}   "
                f"4a {int(s2.pass4a_v2.sum()):2d}   4b {int(s2.pass4b.sum()):2d}   "
                f"min TO among promo cells "
                f"{(f'{s2[s2.promo].TO.min():.2f}x' if s2.promo.any() else 'n/a')}")
    say("\nBINDING LEG OF 4b ON FAIL ROWS (all 200 cells)")
    legs = {}
    for f in df[~df.pass4b].fail4b:
        for leg in f.split(","):
            legs[leg] = legs.get(leg, 0) + 1
    nf = int((~df.pass4b).sum())
    for leg, n in sorted(legs.items(), key=lambda kv: -kv[1]):
        say(f"    {leg:5s} binds in {n:3d} of {nf} 4b-fail rows ({n / max(nf,1):.1%})")

    say("\nTHE TURNOVER-vs-PASS FRONTIER (10 bps, both panels, sorted by turnover)")
    cols = ["panel", "K_in", "K_out", "TO", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
            "pass4a_v2", "beats_v2_oos", "pass4b", "fail4b", "promo"]
    say(df[df.cost == 10.0].sort_values("TO")[cols].to_string(index=False,
        float_format=lambda x: f"{x:.4f}"))

    say("\nTHE SAME CELLS AT 25 bps — the rung the incumbent dies on")
    say(df[df.cost == 25.0].sort_values("TO")[cols].to_string(index=False,
        float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------- PART 3: rule 8 ----
    say("\n" + "=" * 118)
    say("PART 3 — RULE 8 WALK-FORWARD.  (K_in,K_out) chosen by argmax IS Sharpe on 2009-2016 ONLY;")
    say("          2017-2026 read ONCE and reported untouched.")
    say("=" * 118)
    wf = []
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        mso = metrics(spy.loc[OOS_START:])
        for c in COSTS:
            sub = df[(df.panel == pk) & (df.cost == c)]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            inc = sub[(sub.K_in == 20) & (sub.K_out == 20)].iloc[0]
            ok_cagr = pick.OOS_CAGR >= PHI0 * mso["CAGR"]
            ok_dd = abs(pick.OOS_MaxDD) <= DELTA0 * abs(mso["MaxDD"])
            ok_sh = pick.OOS_Sharpe > mso["Sharpe"]
            wf.append(dict(panel=pk, cost=c, K_in=int(pick.K_in), K_out=int(pick.K_out),
                           IS_Sharpe=pick.IS_Sharpe, inc_IS_Sharpe=inc.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD, TO=pick.TO, inc_TO=inc.TO,
                           inc_OOS_Sharpe=inc.OOS_Sharpe, inc_OOS_CAGR=inc.OOS_CAGR,
                           inc_OOS_MaxDD=inc.OOS_MaxDD,
                           v2_OOS_CAGR=pick.v2_OOS_CAGR, v2_OOS_Sharpe=pick.v2_OOS_Sharpe,
                           v2_OOS_MaxDD=pick.v2_OOS_MaxDD,
                           spy_OOS_CAGR=mso["CAGR"], spy_OOS_Sharpe=mso["Sharpe"],
                           spy_OOS_MaxDD=mso["MaxDD"],
                           oos4b=bool(ok_cagr and ok_dd and ok_sh),
                           oos4b_fail=",".join([x for x, o in
                                                (("CAGR", ok_cagr), ("DD", ok_dd), ("OOS", ok_sh))
                                                if not o]) or "-",
                           oos4a=bool(pick.OOS_Sharpe > pick.v2_OOS_Sharpe
                                      and pick.OOS_MaxDD >= pick.v2_OOS_MaxDD)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  rule-8 cells where the IS chooser's pick clears 4b OOS: {int(W.oos4b.sum())} of {len(W)}")
    say(f"  rule-8 cells where the pick beats the LIVE book OOS on Sharpe AND MaxDD (4a-OOS): "
        f"{int(W.oos4a.sum())} of {len(W)}")
    say(f"  rule-8 cells where the pick beats the INCUMBENT 20/20 OOS Sharpe: "
        f"{int((W.OOS_Sharpe > W.inc_OOS_Sharpe).sum())} of {len(W)}")
    say(f"  mean turnover of the picks {W.TO.mean():.2f}x vs incumbent {W.inc_TO.mean():.2f}x "
        f"vs live book {LIVE_TO}x")

    # ------------------------------------------------------------- PART 4: verdict ----
    say("\n" + "=" * 118)
    say("PART 4 — VERDICT")
    say("=" * 118)
    u10 = df[(df.panel == "u56") & (df.cost == 10.0)]
    inc10 = u10[(u10.K_in == 20) & (u10.K_out == 20)].iloc[0]
    cheap = u10[u10.TO <= inc10.TO]
    say(f"  incumbent u56 @10 bps: TO {inc10.TO:.2f}x, Sharpe {inc10.Sharpe:.4f}, "
        f"CAGR {inc10.CAGR:.2%}, MaxDD {inc10.MaxDD:.2%}, promo {bool(inc10.promo)}")
    say(f"  u56 cells at or below the incumbent's turnover: {len(cheap)} of {len(u10)}; "
        f"of those, {int(cheap.promo.sum())} clear the promotion bar at 10 bps")
    for tgt in (6.0, 4.0, 3.0, 2.0, LIVE_TO):
        sub = df[(df.TO <= tgt) & (df.promo)]
        at25 = df[(df.TO <= tgt) & (df.promo) & (df.cost >= 25.0)]
        say(f"  cells with TO <= {tgt:.2f}x clearing the promotion bar: {len(sub):3d} "
            f"(of which at 25 bps or worse: {len(at25)})")
    say("\nCAVEAT: u56/broad are CURRENT constituents (PROTOCOL rule 9 / idea 54); every CAGR level")
    say("above is optimistic and both 4b bars are easier than on a point-in-time panel. The")
    say("turnover contrasts are same-tape/same-names and first-order immune; the pass counts are not.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
