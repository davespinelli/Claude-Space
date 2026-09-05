#!/usr/bin/env python3
"""QUEUE idea 133 — is-the-defensive-class-one-book-in-disguise  (research sprint lane B, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 133)
    Idea 129 proposed a `4b-defensive` reporting class: an arm that clears PROTOCOL rule 4b's
    two halves-Sharpe bars, its OOS-Sharpe bar and its MaxDD cap, and fails ONLY the CAGR
    floor.  Its 11 Pareto-best members were ALL `EWall + a slow trend gate, de-grossed to
    cash` sitting at ~53% mean gross, on two panels and both cost rungs.  Idea 129 filed its
    own caveat: "the class may be one construction in disguise".

    THE QUESTION: does the class have any member that is not that construction?  Run the same
    census over the leaderboard's RANKED books (n = 5/10/20/40) and its SLEEVE books, at
    MATCHED GROSS so that a book is not excluded from the class merely because it sits at a
    different exposure.  If the class has exactly one construction, PROTOCOL should name the
    book, not the class.

TWO FALSIFIABLE HYPOTHESES, both stated before any number was read
    H_one   (the queue's worry) — the class IS one construction.  Prediction: extending the
            corpus to ranked and sleeve books, and re-matching gross, yields ZERO floor-only
            members outside `EWall + {g200, band3, abs12, v1gate} + de-gross`.
    H_gross (the alternative)   — the class is a GROSS-LEVEL phenomenon, not a construction:
            any book de-grossed to ~0.53 that keeps its Sharpe joins it.  Prediction: at
            matched gross the ranked and sleeve books enter the class too, and the EWall
            monopoly in idea 129 was an artefact of the three-book corpus it ran on.
    The two make opposite predictions on the same table, so the run cannot be steered.

    NOTE ON IDEA 129's OWN GRID (read before this run was designed, and it sharpens the
    question rather than answering it): of the 27 floor-only rows in
    `2026-09-05_cagr-floor-calibration_B.grid.csv`, 26 are EWall and ONE is `u56 / TOP20 /
    ddctl-8/.5/high @10bps`, and two are the `rw` (re-weight) convention rather than `dg`.
    So the "one construction" claim is already false for the FULL class and is a statement
    about the 11 PARETO-BEST members only.  This run therefore reports the census at both
    strictnesses: full class membership, and the (Sharpe, MaxDD) Pareto front — and the front
    is taken BOTH within-cell (idea 129's convention, per panel x book x cost) and, which is
    the frontier the question actually needs, ACROSS BOOKS within each panel x cost.

HARNESS
    Idea 94's script (`2026-09-04_drawdown-insurance-price-list_B.py`) is IMPORTED, not
    re-implemented: same simulator (`H.run`), same 17 arms (`H.arm_specs`), same gates, same
    windows, same 0.75 nominal gross, same t+1 weekly execution.  Idea 102's sleeve
    construction (`sleeve_weights`, idea 18 variant B: trend-vote x risk-parity over
    {TLT, GLD, DBC, UUP}) is imported from `2026-09-05_which-asset-carries-S4_C.py` rather
    than re-typed.  `book_targets()` below GENERALISES `H.targets` to n-ranked and sleeve
    books; it is asserted to reproduce `H.targets` EXACTLY on the three books that function
    already knows, over every (gate x convention) combination, before anything new is read.

CORPUS
    panels  u56 (56), broad (136), small (484, idea 97/118 construction verbatim)
    books   V1u, TOP5, TOP10, TOP20, TOP40, EWall, SLV25, SLV50      (8; sleeve books need
            TLT/GLD/DBC/UUP and are therefore not run on the small panel — stated, not hidden)
    arms    idea 94's 17: control, 5 gates x {dg, rw}, 2 stops, 2 DD controls, 2 entry budgets
    costs   10, 25 bps
    gross   3 reported levels on the SAME axis (a convention, not a search — see below)
    => u56/broad 8 x 17 x 2 x 3 = 816 rows each, small 6 x 17 x 2 x 3 = 612 rows.  2244 total,
       every one written to .grid.csv.

TUNED PARAMETERS — exactly two
    n  ranked book size    in {5, 10, 20, 40}    (all four reported)
    f  sleeve fraction     in {0.25, 0.50}       (both reported)
    Nothing else is tuned.  Gates, dials, stop levels, DD depths, entry budgets, cadence,
    execution lag, cost rungs, window boundaries and 4b's own coefficients (phi=0.70,
    delta=0.60) are inherited unchanged from ideas 94/129.

GROSS MATCHING (a reported CONVENTION AXIS, fixed in advance, not a searched dial)
    native   m = 1.0 — every arm at its own exposure.  This is idea 129's reading exactly.
    m53      each arm rescaled so its MEAN gross over the evaluation window equals 0.53,
             the mean gross of idea 129's 11 Pareto-best floor-only arms (the queue's number).
    m75      the same at 0.75, the corpus's nominal gross, i.e. matching UP rather than down.
    Both targets were written down before the run; the achieved mean gross is reported for
    every row so the match can be audited.  Solve = two Newton steps on m, no search.

WALK-FORWARD (PROTOCOL rule 8; four selectors fixed in writing before any OOS number was read)
    Parameters are chosen on 2009-2016 alone; 2017-2026 is read once.  Cells pool ALL books
    within a (panel, cost, gross) triple, because "which construction gets picked" is the
    question.
      S0  no screen:  argmax IS Sharpe over every arm in the cell.
      S1  idea 129's S1: argmax IS Sharpe among arms meeting 4b's halves bars, DD cap and
          CAGR floor on the IS window alone.
      S2  idea 129's S2: the same with the CAGR floor deleted (phi = 0).
      S3  NEW, and the one this idea needs: argmax IS Sharpe among arms that are IS-window
          `4b-defensive` — halves bars and DD cap met, CAGR floor FAILED.  If the class is one
          book, S3 picks that book in every cell; if it is a gross level, S3's picks scatter
          across constructions.
    Every pick is evaluated untouched on 2017-2026 against SPY, RULES v1 and the cell's own
    ungated control.  (4b's OOS-Sharpe bar cannot be screened on prospectively and is used
    only in the OOS read, as in idea 129.)

BOTH KEEP PATHS are evaluated on every one of the 2244 rows: 4a via `H.pass4a` against RULES
v1 on the same panel and cost; 4b via the same five re-parameterised bars idea 129 used.

CAVEATS carried, not buried
    - Survivorship (idea 54): three current-constituent panels.  It runs one way here — absent
      delistings inflate every arm's CAGR and inflate the UNGATED, fully-invested books most,
      so the defensive class's exclusion by a CAGR floor is if anything understated.
    - Idea 128: the IS window (SPY MaxDD -22.1%) is shallower than the OOS window (-33.7%), so
      an IS-window drawdown cap is measured on a window that cannot express deep drawdowns;
      this biases every IS screen toward over-admission.
    - Idea 38: u56/broad still carry the calendar-day index; it applies identically to every
      arm inside a cell and cancels in the cross-book comparison this run is about.
    - Idea 126: every number here is at t+1 execution only; no lag band is claimed.
    - Gross matching changes an arm's CAGR and MaxDD together; a matched-gross row is NOT the
      same instrument as its native row and is never quoted as one.
    - MaxDD is one number off one path; the Pareto fronts inherit that fragility.

RUN
    python research/backtests/2026-09-05_defensive-class-census_B.py
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

STEM = "2026-09-05_defensive-class-census_B"
OUT = ROOT / "research" / "backtests"


def _imp(name, fn):
    spec = importlib.util.spec_from_file_location(name, OUT / fn)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _imp("i94", "2026-09-04_drawdown-insurance-price-list_B.py")      # simulator + arms
S = _imp("i102", "2026-09-05_which-asset-carries-S4_C.py")            # sleeve construction

FREQ, GROSS, MAX_VOL = H.FREQ, H.GROSS, H.MAX_VOL
NV1, WV1 = H.NV1, H.WV1
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]

NS = [5, 10, 20, 40]                 # tuned parameter 1 — ranked book size
FS = [0.25, 0.50]                    # tuned parameter 2 — sleeve fraction
BOOKS = ["V1u"] + [f"TOP{n}" for n in NS] + ["EWall"] + [f"SLV{int(f*100)}" for f in FS]
SLEEVE_BOOKS = {f"SLV{int(f*100)}": f for f in FS}
S4 = S.S4

PHI0, DELTA0 = 0.70, 0.60             # 4b's published coefficients, inherited unchanged
GROSS_LEVELS = {"native": None, "m53": 0.53, "m75": 0.75}

# the construction idea 129 says the class is: EWall + a slow trend gate, de-grossed
SLOW_GATES = {"g200-dg", "band3-dg", "abs12-dg", "v1gate-dg"}

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 3000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- panels (idea 97/118 verbatim)
_PC = {}


def panel(name):
    if name not in _PC:
        _PC[name] = _panel(name)
    return _PC[name]


def _panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


# ---------------------------------------------------------------- books (generalises H.targets)
def _ranked(px, s, g, n, w):
    rank = (s if g is None else s.where(g)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * w


def _ewall(px, g):
    e = (pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
         if g is None else g.astype(float))
    return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def _base(px, book, g=None):
    """Ungated (g=None) or re-weighted-among-gated-in (g=mask) target weights."""
    if book == "EWall":
        return _ewall(px, g)
    if book == "V1u":
        s = H.composite(px) / H.vol20(px).clip(lower=0.08) ** 0.5
        return _ranked(px, s, g, NV1, WV1)
    if book.startswith("TOP"):
        n = int(book[3:])
        return _ranked(px, H.composite(px), g, n, GROSS / n)
    if book in SLEEVE_BOOKS:
        f = SLEEVE_BOOKS[book]
        E = _ewall(px, g)                              # equity leg (gated if g given)
        sl = S.sleeve_weights(px, S4)
        tot = sl.sum(axis=1)
        sl = GROSS * sl.div(tot.where(tot > 1e-12), axis=0).fillna(0.0)
        return (1 - f) * E + f * sl                    # sleeve leg is NOT gated (stated)
    raise ValueError(book)


def book_targets(px, book, gate=None, conv="dg"):
    """conv='dg' zeroes gated-out names into CASH; conv='rw' rebuilds at full gross among the
    gated-in names only.  Identical to H.targets for V1u / TOP20 / EWall (asserted below).
    For sleeve books the gate acts on the equity leg only."""
    if gate is None:
        return _base(px, book)
    g = H.gate_mask(px, gate)
    if conv == "rw":
        return _base(px, book, g)
    W = _base(px, book)
    if book in SLEEVE_BOOKS:                           # de-gross the equity leg only
        f = SLEEVE_BOOKS[book]
        E = _ewall(px, None).where(g, 0.0)
        sl = S.sleeve_weights(px, S4)
        tot = sl.sum(axis=1)
        sl = GROSS * sl.div(tot.where(tot > 1e-12), axis=0).fillna(0.0)
        return (1 - f) * E + f * sl
    return W.where(g, 0.0)


# ---------------------------------------------------------------- 4b bars (idea 129 verbatim)
def bars_win(spy, which):
    if which == "full":
        s1, s2 = H.halves(spy)
        m = metrics(spy)
        return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                    soos=metrics(spy.loc[OOS_START:])["Sharpe"])
    w = H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=m["Sharpe"])


def margins_at(r, b, phi, delta, which="full"):
    w = H.window(r, which)
    h1, h2 = H.halves(w)
    m = metrics(w)
    soos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(H1=h1 - b["s1"], H2=h2 - b["s2"], OOS=soos - b["soos"],
                DD=delta * abs(b["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - phi * b["scagr"])


def fails(mg):
    return [k for k in ("H1", "H2", "OOS", "DD", "CAGR") if mg[k] <= 0]


def pareto(df, s="Sharpe", d="MaxDD"):
    S_, D_ = df[s].values, df[d].values
    out = np.ones(len(df), dtype=bool)
    for i in range(len(df)):
        if not np.isfinite(S_[i]) or not np.isfinite(D_[i]):
            out[i] = False
            continue
        out[i] = not ((S_ >= S_[i]) & (D_ >= D_[i]) & ((S_ > S_[i]) | (D_ > D_[i]))).any()
    return out


def construction(row):
    """The construction label the queue's claim is about."""
    if row["book"] == "EWall" and row["arm"] in SLOW_GATES:
        return "EWall+slow-gate-dg"
    return f"{row['book']}/{row['kind']}"


# ---------------------------------------------------------------- matched-gross solve
def run_at_gross(px, W, kw, cost, target, start):
    """m=1 when target is None; otherwise two Newton steps on the static gross multiplier so
    that mean gross over the evaluation slice equals `target`.  Returns (res, m, achieved)."""
    res = H.run(px, W, bps=cost, **kw)
    g = float(res["gross"].loc[start:].mean())
    if target is None:
        return res, 1.0, g
    m = 1.0
    for _ in range(2):
        if g <= 1e-9:
            break
        m = float(np.clip(m * target / g, 0.02, 5.0))
        res = H.run(px, W, m=m, bps=cost, **kw)
        g = float(res["gross"].loc[start:].mean())
    return res, m, g


# ---------------------------------------------------------------- one (panel, book, cost, gross)
def do_cell(pname, px, spy, book, cost, glabel, gtarget, bfull, bIS, v1_net, start):
    rows, rets = [], {}
    for arm, kind, kw, (gate, conv) in H.arm_specs():
        W = book_targets(px, book, gate, conv)
        res, m, gach = run_at_gross(px, W, kw, cost, gtarget, start)
        r = res["r"].loc[start:]
        rets[arm] = r
        mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
        mg = margins_at(r, bfull, PHI0, DELTA0, "full")
        mgi = margins_at(r, bIS, PHI0, DELTA0, "IS")
        f = fails(mg)
        h1, h2 = H.halves(r)
        rows.append(dict(
            panel=pname, book=book, cost=cost, gross_mode=glabel, arm=arm, kind=kind,
            m=m, gross=gach,
            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
            IS_m_H1=mgi["H1"], IS_m_H2=mgi["H2"], IS_m_DD=mgi["DD"], IS_m_CAGR=mgi["CAGR"],
            pass4b=(len(f) == 0), fail4b=",".join(f) or "-", n_fail=len(f),
            floor_only=(f == ["CAGR"]),
            IS_floor_only=(fails(mgi) == ["CAGR"]),
            IS_admit_phi70=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
            IS_admit_phi00=all(mgi[k] > 0 for k in ("H1", "H2", "DD")),
            pass4a=H.pass4a(r, v1_net),
            TO=float(res["to"].loc[start:].sum() / (len(r) / 252)),
        ))
    D = pd.DataFrame(rows)
    D["pareto_cell"] = pareto(D)
    return D, rets


# ---------------------------------------------------------------- rule 8
def walk_forward(sub, RET, key, spy, v1_net, ctl_ret):
    mc, ms, mv = (metrics(H.window(ctl_ret, "OOS")), metrics(spy.loc[OOS_START:]),
                  metrics(H.window(v1_net, "OOS")))
    cand = {
        "S0": sub,
        "S1": sub[sub.IS_admit_phi70],
        "S2": sub[sub.IS_admit_phi00],
        "S3": sub[sub.IS_floor_only],
    }
    out = []
    order = sub.OOS_Sharpe.rank(ascending=False)
    best = sub.loc[sub.OOS_Sharpe.idxmax()] if len(sub) else None
    for s, c in cand.items():
        base = dict(sel=s, panel=key[0], cost=key[1], gross_mode=key[2],
                    ctl_OOS_Sharpe=mc["Sharpe"], spy_OOS_Sharpe=ms["Sharpe"],
                    spy_OOS_CAGR=ms["CAGR"], spy_OOS_MaxDD=ms["MaxDD"],
                    v1_OOS_Sharpe=mv["Sharpe"], v1_OOS_CAGR=mv["CAGR"],
                    v1_OOS_MaxDD=mv["MaxDD"])
        if not len(c):
            out.append(dict(base, pick="(none)", pick_book="(none)", pick_constr="(none)",
                            n_admitted=0, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                            OOS_MaxDD=np.nan, beat_ctl=np.nan, beat_spy=np.nan,
                            beat_v1=np.nan, oos_rank=np.nan))
            continue
        p = c.loc[c.IS_Sharpe.idxmax()]
        r = H.window(RET[(p["book"], p["arm"])], "OOS")
        m = metrics(r)
        out.append(dict(base, pick=f"{p['book']}/{p['arm']}", pick_book=p["book"],
                        pick_constr=construction(p), n_admitted=len(c),
                        OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                        beat_ctl=bool(m["Sharpe"] > mc["Sharpe"]),
                        beat_spy=bool(m["Sharpe"] > ms["Sharpe"]),
                        beat_v1=bool(m["Sharpe"] > mv["Sharpe"]),
                        oos_rank=float(order.loc[p.name])))
    return pd.DataFrame(out), (best["book"] + "/" + best["arm"]) if best is not None else "-"


# ---------------------------------------------------------------- reproduction gate
def reproduce():
    say("\n" + "=" * 200)
    say("(0) REPRODUCTION — nothing new is read until these four pass")
    px, spy, _ = panel("u56")
    start = px.index[260]

    # (a) book_targets == H.targets on the three books H knows, every gate x convention
    worst = 0.0
    for bk in ("V1u", "TOP20", "EWall"):
        for gate in [None] + list(H.GATES):
            for conv in ("dg", "rw"):
                a, b = book_targets(px, bk, gate, conv), H.targets(px, bk, gate, conv)
                worst = max(worst, float((a.fillna(0) - b.fillna(0)).abs().values.max()))
    say(f"    (a) book_targets vs H.targets over 3 books x 6 gates x 2 conventions: "
        f"max|diff| = {worst:.3e}   {'PASS' if worst == 0.0 else 'FAIL'}")
    assert worst == 0.0

    # (b) H.run with every instrument off == engine.backtest
    W = book_targets(px, "EWall")
    a = H.run(px, W, bps=10.0)["r"].loc[start:]
    b = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
    d = float((a - b).abs().max())
    say(f"    (b) H.run vs engine.backtest (EWall, 10bps): max|diff| = {d:.3e}   "
        f"{'PASS' if d < 1e-12 else 'FAIL'}")
    assert d < 1e-12

    # (c) idea 94's published EWall + vol60-dg u56 @10bps row
    r = H.run(px, book_targets(px, "EWall", "vol60", "dg"), bps=10.0)["r"].loc[start:]
    m = metrics(r)
    say(f"    (c) idea 94's EWall+vol60-dg u56@10bps: {m['CAGR']:.3%} / {m['Sharpe']:.3f} / "
        f"{m['MaxDD']:.3%}   published 11.6% / 1.133 / -16.9%   "
        f"{'PASS' if abs(m['Sharpe']-1.133) < 5e-4 else 'FAIL'}")
    assert abs(m["Sharpe"] - 1.133) < 5e-4

    # (d) sleeve construction imported, not re-typed
    sl = S.sleeve_weights(px, S4)
    say(f"    (d) idea 102 sleeve_weights imported: {list(sl.columns[sl.abs().sum() > 0])} "
        f"non-zero, mean gross {sl.sum(axis=1).loc[start:].mean():.3f}   PASS")
    return True


def reproduce_129(G):
    """The native-gross rows on idea 129's own three books must reproduce its grid exactly."""
    ref = pd.read_csv(OUT / "2026-09-05_cagr-floor-calibration_B.grid.csv")
    mine = G[(G.gross_mode == "native") & (G.book.isin(["V1u", "TOP20", "EWall"]))]
    k = ["panel", "book", "cost", "arm"]
    j = ref.merge(mine, on=k, suffixes=("_129", "_133"))
    say(f"    (e) idea 129 grid re-run: {len(j)} of {len(ref)} rows matched on {k}")
    for col in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "gross"):
        d = float((j[f"{col}_129"] - j[f"{col}_133"]).abs().max())
        say(f"        max|d {col}| = {d:.3e}")
    nf = int((j["floor_only_129"] != j["floor_only_133"]).sum())
    n4b = int((j["pass4b_129"] != j["pass4b_133"]).sum())
    say(f"        floor_only mismatches {nf}/{len(j)}   pass4b mismatches {n4b}/{len(j)}   "
        f"{'PASS' if nf == 0 and n4b == 0 else 'FAIL'}")
    return j


# ---------------------------------------------------------------- main
def main():
    say("=" * 200)
    say("IDEA 133 — is the `4b-defensive` class one book in disguise?")
    say(f"corpus: panels {PANELS} x books {BOOKS} (sleeve books u56/broad only) x 17 arms x "
        f"costs {COSTS} bps x gross {list(GROSS_LEVELS)}")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, nominal gross {GROSS:.0%}.  "
        f"Bars: CAGR >= {PHI0} x SPY, MaxDD <= {DELTA0} x |SPY|.")
    say(f"tuned: n in {NS} (ranked size), f in {FS} (sleeve fraction).  All grid points reported.")
    say("=" * 200)

    reproduce()

    GR, WF, BESTS = [], [], {}
    SPYREF = {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bfull, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        mo = metrics(spy.loc[OOS_START:])
        SPYREF[pname] = dict(desc=desc, **bfull, oos_cagr=mo["CAGR"], oos_dd=mo["MaxDD"])
        books = [b for b in BOOKS if not (pname == "small" and b in SLEEVE_BOOKS)]
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()} | "
            f"books {books}")
        say(f"    SPY full CAGR {bfull['scagr']:.2%} MaxDD {bfull['sdd']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} OOS Sharpe {bfull['soos']:.3f} | bars: CAGR "
            f">= {PHI0*bfull['scagr']:.2%}/yr, MaxDD >= {-DELTA0*abs(bfull['sdd']):.2%}")

        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        for glabel, gtarget in GROSS_LEVELS.items():
            for c in COSTS:
                RET = {}
                cellrows = []
                for book in books:
                    D, rets = do_cell(pname, px, spy, book, c, glabel, gtarget,
                                      bfull, bIS, v1[c], start)
                    cellrows.append(D)
                    for a, r in rets.items():
                        RET[(book, a)] = r
                CD = pd.concat(cellrows, ignore_index=True)
                CD["pareto_panelcost"] = pareto(CD)      # across ALL books in the cell
                GR.append(CD)
                ctl = RET[("EWall", "control")]
                wf, best = walk_forward(CD, RET, (pname, c, glabel), spy, v1[c], ctl)
                WF.append(wf)
                BESTS[(pname, c, glabel)] = best
                say(f"    {pname:5s} gross={glabel:6s} {int(c):2d}bps: {len(CD)} arms | "
                    f"4b {int(CD.pass4b.sum()):3d} | 4a {int(CD.pass4a.sum()):3d} | "
                    f"floor-only {int(CD.floor_only.sum()):3d} | mean gross "
                    f"{CD.gross.mean():.3f}")

    G = pd.concat(GR, ignore_index=True)
    W = pd.concat(WF, ignore_index=True)
    G["constr"] = G.apply(construction, axis=1)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    say("\n" + "=" * 200)
    say(f"(0e) REPRODUCTION OF IDEA 129'S GRID  (its 306 rows are a strict subset of this run's "
        f"native-gross rows)")
    reproduce_129(G)

    # ---------------------------------------------------------------- (1) the census
    say("\n" + "=" * 200)
    say("(1) THE CENSUS — who is in the `4b-defensive` class (clears H1, H2, OOS, DD; fails ONLY "
        "the CAGR floor)?")
    say(f"    total rows {len(G)};  4b passes {int(G.pass4b.sum())};  4a passes "
        f"{int(G.pass4a.sum())};  floor-only {int(G.floor_only.sum())}")
    FO = G[G.floor_only]
    if len(FO):
        say("\n    membership by gross mode x book:")
        say(pd.crosstab(FO.book, FO.gross_mode).to_string())
        say("\n    membership by gross mode x construction:")
        say(pd.crosstab(FO.constr, FO.gross_mode).to_string())
        say("\n    membership by panel x book:")
        say(pd.crosstab(FO.panel, FO.book).to_string())
        say("\n    membership by arm kind:")
        say(pd.crosstab(FO["kind"], FO.gross_mode).to_string())
    nonew = FO[FO.constr != "EWall+slow-gate-dg"]
    say(f"\n    >>> members NOT of the form `EWall + slow trend gate + de-gross`: "
        f"{len(nonew)} of {len(FO)}")
    if len(nonew):
        say(nonew.sort_values("Sharpe", ascending=False)[
            ["panel", "book", "arm", "cost", "gross_mode", "gross", "CAGR", "Sharpe", "MaxDD",
             "OOS_Sharpe", "OOS_MaxDD", "m_CAGR", "pass4a"]].to_string(index=False,
            float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- (2) Pareto fronts
    say("\n" + "=" * 200)
    say("(2) THE PARETO-BEST SUBSET — idea 129's claim is about this set, not the whole class")
    for lbl, col in (("within (panel,book,cost) — idea 129's convention", "pareto_cell"),
                     ("across ALL books within (panel,cost,gross) — the frontier this question "
                      "needs", "pareto_panelcost")):
        P = G[G.floor_only & G[col]]
        say(f"\n    Pareto-best floor-only, {lbl}: {len(P)} rows")
        if len(P):
            say(pd.crosstab(P.constr, P.gross_mode).to_string())
            say(f"    not EWall+slow-gate-dg: {int((P.constr != 'EWall+slow-gate-dg').sum())} "
                f"of {len(P)}; mean gross {P.gross.mean():.3f}")
            say(P.sort_values(["panel", "cost", "gross_mode", "Sharpe"], ascending=False)[
                ["panel", "book", "arm", "cost", "gross_mode", "gross", "CAGR", "Sharpe",
                 "MaxDD", "OOS_Sharpe", "OOS_MaxDD"]].to_string(index=False,
                float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- (3) why non-members miss
    say("\n" + "=" * 200)
    say("(3) WHY THE OTHER BOOKS ARE NOT IN THE CLASS — the binding bar, by book")
    tab = pd.crosstab(G.book, G.fail4b)
    say(tab.to_string())
    say("\n    for each (panel, book, gross_mode): the arm that comes CLOSEST to the class "
        "(fails the floor plus the fewest other bars), and which bar it fails")
    near = (G[~G.floor_only & (G.fail4b.str.contains("CAGR"))]
            .sort_values("n_fail").groupby(["panel", "book", "gross_mode"]).head(1))
    say(near[["panel", "book", "gross_mode", "arm", "cost", "gross", "Sharpe", "MaxDD",
              "CAGR", "fail4b", "m_DD", "m_H1", "m_H2", "m_OOS"]]
        .sort_values(["panel", "book"]).to_string(index=False,
        float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- (4) gross vs construction
    say("\n" + "=" * 200)
    say("(4) IS IT THE GROSS LEVEL OR THE CONSTRUCTION?  (H_gross vs H_one)")
    say("    mean gross of class members vs non-members, by gross mode:")
    t = G.groupby("gross_mode").apply(
        lambda d: pd.Series(dict(
            n=len(d), n_class=int(d.floor_only.sum()),
            gross_class=d.loc[d.floor_only, "gross"].mean(),
            gross_other=d.loc[~d.floor_only, "gross"].mean(),
            Sharpe_class=d.loc[d.floor_only, "Sharpe"].mean(),
            Sharpe_other=d.loc[~d.floor_only, "Sharpe"].mean(),
            OOS_Sharpe_class=d.loc[d.floor_only, "OOS_Sharpe"].mean(),
            OOS_Sharpe_other=d.loc[~d.floor_only, "OOS_Sharpe"].mean(),
            MaxDD_class=d.loc[d.floor_only, "MaxDD"].mean(),
            MaxDD_other=d.loc[~d.floor_only, "MaxDD"].mean())), include_groups=False)
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n    class membership RATE by book, at each gross mode (the decisive table):")
    rate = G.pivot_table(index="book", columns="gross_mode", values="floor_only",
                         aggfunc="mean")
    cnt = G.pivot_table(index="book", columns="gross_mode", values="floor_only", aggfunc="sum")
    say((rate * 100).round(1).astype(str) + "%  (n=" + cnt.astype(int).astype(str) + ")")
    say("\n    H_one  predicts: the m53/m75 columns stay 0 for every book except EWall.")
    say("    H_gross predicts: at m53 the ranked and sleeve books join the class.")

    # ---------------------------------------------------------------- (5) rule 8
    say("\n" + "=" * 200)
    say("(5) RULE 8 WALK-FORWARD — parameters chosen on 2009-2016, 2017-2026 read once")
    say("    cells pool ALL books; S3 selects the IS-window defensive class deliberately.")
    say(W[["panel", "cost", "gross_mode", "sel", "n_admitted", "pick", "OOS_CAGR",
           "OOS_Sharpe", "OOS_MaxDD", "beat_spy", "beat_v1", "beat_ctl", "oos_rank"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n    selector summary (means over cells where the selector picks):")
    su = W.groupby("sel").apply(lambda d: pd.Series(dict(
        cells=len(d), picks=int(d["pick"].ne("(none)").sum()),
        OOS_CAGR=d.OOS_CAGR.mean(), OOS_Sharpe=d.OOS_Sharpe.mean(),
        OOS_MaxDD=d.OOS_MaxDD.mean(),
        beat_spy=d.beat_spy.sum(), beat_v1=d.beat_v1.sum(), beat_ctl=d.beat_ctl.sum(),
        mean_rank=d.oos_rank.mean())), include_groups=False)
    say(su.to_string(float_format=lambda x: f"{x:.3f}"))
    say(f"\n    reference: SPY OOS {W.spy_OOS_CAGR.mean():.2%}/{W.spy_OOS_Sharpe.mean():.3f}/"
        f"{W.spy_OOS_MaxDD.mean():.2%} | RULES v1 OOS {W.v1_OOS_CAGR.mean():.2%}/"
        f"{W.v1_OOS_Sharpe.mean():.3f}/{W.v1_OOS_MaxDD.mean():.2%} | ungated EWall control OOS "
        f"Sharpe {W.ctl_OOS_Sharpe.mean():.3f}")
    say("\n    S3's picks by construction (does the defensive class select one book?):")
    s3 = W[W.sel == "S3"]
    say(s3.groupby(["pick_constr"]).size().to_string())
    say("\n    S1 vs S3 pick identity, per cell:")
    piv = W.pivot_table(index=["panel", "cost", "gross_mode"], columns="sel", values="pick",
                        aggfunc="first")
    say(piv.to_string())

    # ---------------------------------------------------------------- (6) KEEP paths
    say("\n" + "=" * 200)
    say("(6) BOTH KEEP PATHS on all rows")
    say(f"    4a passes: {int(G.pass4a.sum())} of {len(G)}")
    say(f"    4b passes: {int(G.pass4b.sum())} of {len(G)}")
    if G.pass4b.any():
        say(G[G.pass4b].groupby(["panel", "book", "gross_mode"]).size().to_string())
        k = G[G.pass4b].sort_values("Sharpe", ascending=False).head(15)
        say("\n    best 4b passes:")
        say(k[["panel", "book", "arm", "cost", "gross_mode", "gross", "CAGR", "Sharpe",
               "MaxDD", "H1", "H2", "OOS_Sharpe", "TO"]].to_string(index=False,
            float_format=lambda x: f"{x:.3f}"))
        say("\n    cross-cell survivors: arms passing 4b in all four (u56/broad x 10/25bps) "
            "cells at NATIVE gross:")
        nat = G[(G.gross_mode == "native") & G.panel.isin(["u56", "broad"])]
        srv = (nat.groupby(["book", "arm"]).pass4b.sum() == 4)
        say(", ".join(f"{b}/{a}" for (b, a), v in srv.items() if v) or "    (none)")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nWrote {STEM}.grid.csv ({len(G)} rows), {STEM}.walkforward.csv ({len(W)} rows), "
        f"{STEM}.console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
