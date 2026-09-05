#!/usr/bin/env python3
"""QUEUE idea 134 — sleeve-f-that-clears-the-floor  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 134)
    "idea 133 found the `4b-defensive` class's best members are macro-sleeve books
     (broad/SLV50/ebud-0.10 8.7%/1.292/-13.6%, OOS 1.311; SLV50/vol60-dg OOS MaxDD -10.6%)
     that miss 4b's CAGR floor by only 2.0-3.0 pp/yr at f=0.50.  Sweep f in
     {0.05,0.10,0.15,0.20,0.25} on both universes at 10/25 bps: is there an f at which a
     sleeve book clears the floor while keeping a drawdown inside 4b's cap, i.e. does the
     class have a 4b-passing member one dial away?"

    `4b-defensive` (idea 129's class) = an arm that clears 4b's two halves bars, its OOS-Sharpe
    bar and its drawdown cap (MaxDD <= 60% of SPY's) and fails ONLY the CAGR floor
    (CAGR >= 70% of SPY's).  This run asks whether lowering the sleeve fraction f — which
    mechanically returns weight to the equity book and therefore buys CAGR with drawdown —
    walks such a member across the floor without walking it out through the cap.

AUDIT OF THE PREMISE, BEFORE ANY NEW NUMBER
    The queue's two quoted rows are re-derived from idea 133's own published `.grid.csv`
    rather than trusted.  Note in advance that the queue's label "SLV50" is not a book name
    in that file; the file's sleeve books are `S3-50` (TLT/GLD/UUP) and `S4-50`
    (TLT/GLD/DBC/UUP), both at f=0.50, and check (b) below prints the actual rows whose
    numbers the queue is quoting, on both panels, so the reader can see which book and which
    panel each headline belongs to.  Nothing downstream depends on resolving the label.

CORPUS
    BOOKS (all at MATCHED gross 0.75 before any overlay, so f moves the MIX and never the
    exposure — the exposure axis is the separate static-gross ladder below):
        R20            composite-ranked top-20 at 0.75/20 — the f=0.00 no-sleeve control
        S3-f           (1-f) x R20 + f x sleeve(TLT,GLD,UUP),      rescaled to 0.75
        S4-f           (1-f) x R20 + f x sleeve(TLT,GLD,DBC,UUP),  rescaled to 0.75
        f in {0.05, 0.10, 0.15, 0.20, 0.25} (the swept values) PLUS f=0.50 (idea 133's
        published anchor, carried so this run reproduces it rather than re-describing it).
    INSTRUMENTS: idea 94's 17 arms unchanged (control, 5 gates x {dg,rw}, 2 stops, 2 book
        drawdown controls, 2 entry budgets).  The queue names `ebud-0.10` and `vol60-dg`; they
        are run as two of the seventeen and are never selected on.
    PANELS: u56 (research/universe.json) and broad (universe_broad.json) — "both universes"
        in the queue's sense.  The small panel has no TLT/GLD/DBC/UUP so a sleeve book cannot
        exist there; idea 136 is the open item for the small panel and this run does not
        pretend to answer it.
    COSTS: 10 and 25 bps, both reported on every row.
    = 2 panels x 13 books x 17 arms x 2 costs = 884 arm-rows, every one printed and written
    to .grid.csv, plus a 13 x 5 x 2 x 2 = 260-row static-gross ladder control.

TUNED PARAMETERS — exactly two: the sleeve fraction f (6 values, all reported) and the sleeve
    asset set (S3 vs S4, both reported).  Panels, cost rungs, all 17 overlay instruments, the
    gross ladder and both KEEP paths are reported axes and are never selected on.

WHY THE LADDER CONTROL IS HERE
    Lowering f is one way to buy CAGR; simply raising gross is another, and idea 129 found the
    CAGR floor's real content is a gross-level filter.  If a static-gross ladder point on the
    SAME book clears 4b wherever a low-f sleeve book does, then f is not the dial that did the
    work and the queue's "one dial away" is the wrong dial.  The ladder is run at
    m in {0.60,0.80,1.00,1.20,1.40} on every book so the two dials are directly comparable.

WALK-FORWARD (PROTOCOL rule 8; selectors fixed in writing before any OOS number was read)
    S0  argmax IS Sharpe over the whole corpus in the (panel, cost) cell — no screen.
    S1  argmax IS Sharpe among arms whose IS window ALONE clears 4b's halves bars, its DD cap
        and its CAGR floor (the full IS 4b screen).
    S2  the same with the floor deleted — the screen that admits the defensive class.
    Each pick is read ONCE on 2017-2026 against its cell's R20 control, RULES v1 and SPY.
    Reported: OOS CAGR / Sharpe / MaxDD for each pick and for SPY and the baseline.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  At least one (panel, cost, book, arm) with f <= 0.25 passes 4b outright.
    P2  If P1 holds, the passing f's are the LOW end of the sweep (f <= 0.15), because the
        floor is what binds at f=0.50 and the floor is bought by holding less sleeve.
    P3  The pass is NOT uniform across the two panels: idea 133's u56 rows are stronger than
        its broad rows, so any pass should appear on u56 first.
    P4  The static-gross ladder reaches 4b on the same books at some m, i.e. f is not the only
        dial — the queue's "one dial away" is true of the exposure dial too.
    P5  25 bps kills more of the passes than 10 bps does (cost is the binding axis once the
        floor is cleared).

CAVEATS carried, not buried
    * Survivorship: both panels are current constituents (idea 54).  Absent delistings inflate
      every arm's CAGR, and they inflate the EQUITY leg more than the ETF sleeve, so this run's
      CAGR floor margins are biased in FAVOUR of low f.  No level here is an achievable return.
    * Idea 128: the IS window's SPY MaxDD (-22.1%) is shallower than the OOS window's (-33.7%),
      so an IS drawdown cap is measured on a window that cannot express a deep drawdown; the
      S1/S2 screens are biased toward admitting too much.
    * Idea 126: every row is quoted at t+1 execution only.
    * Idea 127: a gated row is a joint statement about the gate and about cash, so mean realised
      gross is reported on every row and the dg/rw split is never collapsed.
    * The queue records idea 134 as blocked on ideas 105/106 for any RULES wording ("macro
      sleeve" may be a gold claim, and DBC may be a contango artefact).  This run therefore
      cannot propose RULES wording for a sleeve book even if one passes; a pass here is a
      KEEP-candidate conditional on 105/106, and the memo says so.

HARNESS
    Idea 94's script is IMPORTED (H.run, H.targets, H.gate_mask, H.arm_specs, H.halves,
    H.margins, H.pass4a) and idea 129's census machinery too (C.bars_win, C.margins_at,
    C.fails, C.pareto_front), so every number sits on the simulator that produced the rows
    being extended.  Checks run before any new number is read:
      (a) every ungated book vs engine.backtest — must be exact;
      (b) idea 133's published sleeve rows re-derived from its .grid.csv;
      (c) this run's f=0.50 rows must equal idea 133's S3-50 / S4-50 rows arm-for-arm.

Deterministic, standalone.  Imports research/baseline.py and two prior scripts; modifies
nothing.  Writes .console.txt, .grid.csv, .ladder.csv and .walkforward.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_sleeve-f-that-clears-the-floor_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I133_GRID = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")

FREQ, GROSS, COSTS = H.FREQ, H.GROSS, H.COSTS
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60
FS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.50]      # tuned parameter 1 — ALL reported
S3, S4 = ["TLT", "GLD", "UUP"], ["TLT", "GLD", "DBC", "UUP"]   # tuned parameter 2
LADDER_M = [0.60, 0.80, 1.00, 1.20, 1.40]
NTOP = 20

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ books ----
def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """Ideas 100/104's sleeve, verbatim from idea 133: momentum vote x risk parity."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def ranked(px, n, gate=None, conv="dg"):
    s = H.composite(px)
    g = H.gate_mask(px, gate)
    if gate is not None and conv == "rw":
        s = s.where(g)
    w = (s.rank(axis=1, ascending=False) <= n).astype(float) * (GROSS / n)
    if gate is not None and conv == "dg":
        w = w.where(g, 0.0)
    return w


def book_weights(px, book, gate=None, conv="dg"):
    """R20 (f=0) and the S3-f / S4-f blends, all rescaled to GROSS before any overlay."""
    if book == "R20":
        return ranked(px, NTOP, gate, conv)
    assets = S3 if book.startswith("S3") else S4
    f = int(book.split("-")[1]) / 100.0
    base = (1 - f) * ranked(px, NTOP) + f * sleeve_weights(px, assets)
    B = base.mul((GROSS / base.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0)
    if gate is None:
        return B.fillna(0.0)
    gm = H.gate_mask(px, gate)
    if conv == "dg":
        return B.where(gm, 0.0).fillna(0.0)
    w = (1 - f) * ranked(px, NTOP, gate, "rw") + f * sleeve_weights(px, assets).where(gm, 0.0)
    return w.mul((GROSS / w.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


def books():
    return ["R20"] + [f"S3-{int(f*100)}" for f in FS] + [f"S4-{int(f*100)}" for f in FS]


def fval(book):
    return 0.0 if book == "R20" else int(book.split("-")[1]) / 100.0


# ------------------------------------------------------------------ main ----
def main():
    # ---- (b) premise audit against idea 133's own published file ----
    say("[b] PREMISE AUDIT — idea 133's published grid, re-derived here (the queue's two rows)")
    g133 = pd.read_csv(I133_GRID)
    q = g133[g133.book.isin(["S3-50", "S4-50"]) & g133.arm.isin(["ebud-0.10", "vol60-dg"])]
    cols = ["panel", "book", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "OOS_MaxDD",
            "gross", "m_CAGR", "floor_only", "pass4b"]
    say(q[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("    NOTE: the queue's label 'SLV50' is not a book name in that file; the f=0.50 sleeve")
    say("    books there are S3-50 and S4-50.  The queue's 8.7%/1.292/-13.6% headline is closest")
    say("    to u56/S3-50/ebud-0.10 @10bps (9.94%/1.291/-11.1%, OOS 1.277); nothing below")
    say("    depends on resolving the label — this run re-derives every f=0.50 row itself.")
    fo = g133[g133.floor_only & g133.book.str.startswith("S")]
    say(f"    idea 133 sleeve rows in the 4b-defensive class: {len(fo)}; CAGR-floor shortfall "
        f"(m_CAGR) min {fo.m_CAGR.min()*100:.2f} median {fo.m_CAGR.median()*100:.2f} "
        f"max {fo.m_CAGR.max()*100:.2f} pp/yr — the queue's '2.0-3.0 pp/yr' is the tail, not "
        f"the median.")

    rows, lrows, rets, ref = [], [], {}, {}
    for pk in ("u56", "broad"):
        px = load_universe(broad=(pk == "broad"))
        missing = [t for t in S4 if t not in px.columns]
        if missing:
            raise RuntimeError(f"{pk} lacks {missing}")
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        bars, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        ms = metrics(spy)
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk] = dict(bars=bars, spy=ms, v1=v1, start=start)
        say(f"\n[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")
        say(f"    SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {bars['s1']:.3f}/{bars['s2']:.3f} OOS {bars['soos']:.3f} | 4b bars: "
            f"MaxDD <= {DELTA*abs(ms['MaxDD']):.2%}, CAGR >= {PHI*ms['CAGR']:.2%}")

        worst = 0.0
        for b in books():
            W = book_weights(px, b)
            a = H.run(px, W, bps=10.0)["r"].loc[start:]
            e = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
            worst = max(worst, float((a - e).abs().max()))
        say(f"[a] engine-equivalence over {len(books())} ungated books: max|diff| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — unsafe'})")

        for b in books():
            for name, kind, kwargs, (gt, conv) in H.arm_specs():
                W = book_weights(px, b, gt, conv)
                for c in COSTS:
                    res = H.run(px, W, bps=c, **kwargs)
                    r = res["r"].loc[start:]
                    rets[(pk, b, name, c)] = r
                    mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
                    h1, h2 = H.halves(r)
                    mg = C.margins_at(r, bars, PHI, DELTA, "full")
                    ismg = C.margins_at(r, bIS, PHI, DELTA, "IS")
                    fail = C.fails(mg)
                    rows.append(dict(
                        panel=pk, book=b, f=fval(b), sleeve=("-" if b == "R20" else b[:2]),
                        arm=name, kind=kind,
                        conv=("rw" if name.endswith("-rw") else "dg" if name.endswith("-dg") else "-"),
                        cost=c, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        gross=res["gross"].loc[start:].mean(),
                        TO=res["to"].loc[start:].sum() / mm["Years"],
                        m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                        IS_m_H1=ismg["H1"], IS_m_H2=ismg["H2"], IS_m_DD=ismg["DD"], IS_m_CAGR=ismg["CAGR"],
                        pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-", n_fail=len(fail),
                        floor_only=(fail == ["CAGR"]), pass4a=H.pass4a(r, v1[c])))
            for m_ in LADDER_M:
                for c in COSTS:
                    res = H.run(px, book_weights(px, b), m=m_, bps=c)
                    r = res["r"].loc[start:]
                    mm = metrics(r)
                    mg = C.margins_at(r, bars, PHI, DELTA, "full")
                    fail = C.fails(mg)
                    lrows.append(dict(panel=pk, book=b, f=fval(b), m=m_, cost=c, CAGR=mm["CAGR"],
                                      Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                      gross=res["gross"].loc[start:].mean(),
                                      OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                      m_CAGR=mg["CAGR"], m_DD=mg["DD"],
                                      pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-",
                                      floor_only=(fail == ["CAGR"])))

    df = pd.DataFrame(rows)
    lad = pd.DataFrame(lrows)
    df["pareto"] = False
    for (pk, c), s in df.groupby(["panel", "cost"]):
        df.loc[s.index, "pareto"] = C.pareto_front(s)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)

    # ---- (c) reproduction of idea 133's f=0.50 rows ----
    j = df[df.f == 0.50].merge(g133, on=["panel", "book", "arm", "cost"], suffixes=("", "_133"))
    d = {k: float((j[k] - j[f"{k}_133"]).abs().max()) for k in
         ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "gross")}
    say(f"\n[c] reproduction of idea 133's f=0.50 sleeve rows: {len(j)} matched, max|diff| "
        + " ".join(f"{k} {v:.2e}" for k, v in d.items())
        + ("  EXACT" if max(d.values()) < 1e-9 else "  NOT EXACT — unsafe"))

    say(f"\n[GRID] {len(df)} arm-rows, ALL reported")
    gc = ["panel", "book", "f", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
          "OOS_Sharpe", "OOS_MaxDD", "gross", "TO", "m_CAGR", "m_DD", "pass4a", "pass4b", "fail4b",
          "floor_only", "pareto"]
    with pd.option_context("display.max_rows", None):
        say(df[gc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- THE QUESTION ----
    P = df[df.pass4b]
    say(f"\n[ANSWER] 4b passes in the whole {len(df)}-row grid: {len(P)}")
    if len(P):
        with pd.option_context("display.max_rows", None):
            say(P[gc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        say(f"[ANSWER] passes by f: {dict(sorted(P.f.value_counts().items()))}")
        say(f"[ANSWER] passes by panel: {dict(P.panel.value_counts())} | by cost: "
            f"{dict(P.cost.value_counts())} | by sleeve: {dict(P.sleeve.value_counts())}")
        say(f"[ANSWER] passes among SLEEVE books only (f>0): {int((P.f > 0).sum())}; "
            f"among the swept f<=0.25 sleeve books: {int(((P.f > 0) & (P.f <= 0.25)).sum())}")
        say(f"[ANSWER] cross-cell: sleeve (book, arm) pairs passing in ALL 4 (panel, cost) cells: "
            f"{sorted({k for k, v in P[P.f > 0].groupby(['book', 'arm']).size().items() if v == 4})}")
    else:
        say("[ANSWER] none — no f in the sweep produces a 4b-passing sleeve arm on either panel.")

    D = df[df.floor_only]
    say(f"\n[CLASS] 4b-defensive rows (floor-only failures): {len(D)} of {len(df)}")
    say(f"[CLASS] by f: {dict(sorted(D.f.value_counts().items()))} | by panel: "
        f"{dict(D.panel.value_counts())} | by cost: {dict(D.cost.value_counts())}")

    say("\n[F-CURVE] mean over the 17 arms, per (panel, cost, book): what f actually buys")
    fc = (df.groupby(["panel", "cost", "book", "f"])
            .agg(CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "mean"),
                 OOS_Sharpe=("OOS_Sharpe", "mean"), m_CAGR=("m_CAGR", "mean"),
                 m_DD=("m_DD", "mean"), n_pass4b=("pass4b", "sum"),
                 n_floor_only=("floor_only", "sum")).reset_index().sort_values(
                     ["panel", "cost", "book"]))
    with pd.option_context("display.max_rows", None):
        say(fc.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n[BINDING] which 4b bar fails, by f (counts over all arms, panels and cost rungs)")
    bind = []
    for f_, s in df.groupby("f"):
        bind.append(dict(f=f_, n=len(s), pass4b=int(s.pass4b.sum()),
                         fail_H1=int((s.m_H1 <= 0).sum()), fail_H2=int((s.m_H2 <= 0).sum()),
                         fail_OOS=int((s.m_OOS <= 0).sum()), fail_DD=int((s.m_DD <= 0).sum()),
                         fail_CAGR=int((s.m_CAGR <= 0).sum()),
                         mean_m_CAGR_pp=float(s.m_CAGR.mean() * 100),
                         mean_m_DD_pp=float(s.m_DD.mean() * 100)))
    say(pd.DataFrame(bind).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say(f"\n[LADDER] {len(lad)} static-gross control rows, ALL reported")
    with pd.option_context("display.max_rows", None):
        say(lad.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    LP = lad[lad.pass4b]
    say(f"[LADDER] 4b passes on the pure exposure dial: {len(LP)} of {len(lad)}; by book "
        f"{dict(LP.book.value_counts()) if len(LP) else '{}'}; m "
        f"{LP.m.min() if len(LP) else float('nan')}..{LP.m.max() if len(LP) else float('nan')}")

    # ---- rule 8 walk-forward ----
    say("\n[RULE 8] S0 (no screen) / S1 (IS 4b screen with floor) / S2 (floor deleted); argmax IS "
        "Sharpe per (panel, cost) cell; OOS 2017-2026 read once.")
    wrows = []
    for (pk, c), s in df.groupby(["panel", "cost"]):
        bars = ref[pk]["bars"]
        v1oos = metrics(ref[pk]["v1"][c].loc[OOS_START:])
        ctl = s[(s.book == "R20") & (s.arm == "control")].iloc[0]
        scr = (s.IS_m_H1 > 0) & (s.IS_m_H2 > 0) & (s.IS_m_DD > 0)
        for k, cand in {"S0": s, "S1": s[scr & (s.IS_m_CAGR > 0)], "S2": s[scr]}.items():
            if not len(cand):
                wrows.append(dict(sel=k, panel=pk, cost=c, pick="(none admitted)", n_admitted=0))
                continue
            p = cand.loc[cand.IS_Sharpe.idxmax()]
            wrows.append(dict(sel=k, panel=pk, cost=c, pick=f"{p.book}/{p.arm}", f=p.f,
                              n_admitted=len(cand), OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe,
                              OOS_MaxDD=p.OOS_MaxDD, pass4b=bool(p.pass4b),
                              defensive=bool(p.floor_only),
                              ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                              ctl_OOS_MaxDD=ctl.OOS_MaxDD, spy_OOS_Sharpe=bars["soos"],
                              v1_OOS_Sharpe=v1oos["Sharpe"], v1_OOS_CAGR=v1oos["CAGR"],
                              beat_ctl=p.OOS_Sharpe > ctl.OOS_Sharpe,
                              beat_spy=p.OOS_Sharpe > bars["soos"],
                              beat_v1=p.OOS_Sharpe > v1oos["Sharpe"]))
    wf = pd.DataFrame(wrows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    with pd.option_context("display.max_rows", None):
        say(wf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("[RULE 8] mean OOS Sharpe by selector: "
        + ", ".join(f"{k} {v:.3f}" for k, v in wf.groupby("sel").OOS_Sharpe.mean().items()))
    piv = wf.pivot_table(index=["panel", "cost"], columns="sel", values="pick", aggfunc="first")
    say(f"[RULE 8] S1 != S2 in {int((piv.get('S1') != piv.get('S2')).sum())} of {len(piv)} cells; "
        f"S0 != S1 in {int((piv.get('S0') != piv.get('S1')).sum())}")

    # OOS-window 4b re-test of every arm that passes 4b on the full sample
    if len(P):
        say("\n[OOS 4b] every full-sample 4b pass re-tested on the OOS window alone "
            "(halves of 2017-2026, OOS bars):")
        orows = []
        for r_ in P.itertuples():
            rr = rets[(r_.panel, r_.book, r_.arm, r_.cost)].loc[OOS_START:]
            spyo = (load_universe(broad=(r_.panel == "broad"))["SPY"].pct_change().fillna(0.0)
                    .loc[OOS_START:])
            bo = C.bars_win(spyo, "full")
            mg = C.margins_at(rr, bo, PHI, DELTA, "full")
            f_ = C.fails(mg)
            mm = metrics(rr)
            orows.append(dict(panel=r_.panel, book=r_.book, arm=r_.arm, cost=r_.cost,
                              OOS_CAGR=mm["CAGR"], OOS_Sharpe=mm["Sharpe"], OOS_MaxDD=mm["MaxDD"],
                              spy_CAGR=metrics(spyo)["CAGR"], spy_Sharpe=metrics(spyo)["Sharpe"],
                              spy_MaxDD=metrics(spyo)["MaxDD"],
                              oos4b=(len(f_) == 0), oos_fail=",".join(f_) or "-"))
        say(pd.DataFrame(orows).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- predictions ----
    say("\n[P] PRE-REGISTERED PREDICTIONS, scored")
    p1 = bool(len(P[(P.f > 0) & (P.f <= 0.25)]))
    say(f"   P1 >=1 sleeve arm with f<=0.25 passes 4b: {int(((P.f > 0) & (P.f <= 0.25)).sum())} "
        f"-> {'HELD' if p1 else 'FAILED'}")
    lowf = sorted(set(P[(P.f > 0)].f))
    p2 = bool(lowf) and max(lowf) <= 0.15
    say(f"   P2 the passing sleeve f's are the low end (<=0.15): {lowf} -> "
        f"{'HELD' if p2 else 'FAILED'}")
    pu = int((P.panel == "u56").sum()) if len(P) else 0
    pb_ = int((P.panel == "broad").sum()) if len(P) else 0
    say(f"   P3 passes are not uniform across panels, u56 first: u56 {pu} / broad {pb_} -> "
        f"{'HELD' if pu > pb_ else 'FAILED'}")
    say(f"   P4 the static-gross ladder also reaches 4b: {len(LP)} rows -> "
        f"{'HELD' if len(LP) else 'FAILED'}")
    n10 = int((P.cost == 10.0).sum()) if len(P) else 0
    n25 = int((P.cost == 25.0).sum()) if len(P) else 0
    say(f"   P5 25 bps kills more passes than 10 bps: 10bps {n10} / 25bps {n25} -> "
        f"{'HELD' if n10 > n25 else 'FAILED'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
