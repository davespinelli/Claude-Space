#!/usr/bin/env python3
"""QUEUE idea 416 — pre-register-K_CAGR-as-the-rule-8-default  (cloud, 2026-09-08).

QUESTION (verbatim from QUEUE.md idea 416)
    "idea 151 replicated idea 142's K_CAGR-over-K_Sharpe gap (+0.0342 OOS Sharpe, t +3.96,
     36/43 paired cells) on a widened 72-cell corpus with a rung idea 142 never saw, and showed
     it is NOT the 4b CAGR floor in disguise because it survives on the UNSCREENED pool.  Before
     PROTOCOL names a selector, pre-register K_CAGR on a corpus neither run has read (new books
     or a fourth panel) and report the paired gap once.  If it holds, rule 8 gets a named
     default; if not, rule 8 gets the do-nothing control instead."

WHAT THIS RUN IS
    A single, pre-registered, out-of-corpus replication.  Ideas 142 and 151 read the SAME nine
    books on the SAME three panels; 151 only widened the cost rung.  "+0.0342 on 72 cells"
    therefore rests on ~50 distinct book x panel combinations, and the second run could not have
    disconfirmed the first on any cell the first had already read.  This run reads a corpus with
    ZERO (panel, book) overlap with either — asserted, not asserted-by-eye — and reports the
    paired gap ONCE.  There is no second look, no re-cut, no sub-sample rescue.

THE NEW CORPUS — 24 cells, no (panel, book) pair read by idea 142 or idea 151
    A FOURTH PANEL, `bstk100`: the broad panel with all 36 ETFs deleted, SPY held out as the
      benchmark return only (the small-panel convention).  100 US large-cap STOCKS.  The panel
      exists elsewhere in the record (ideas 77/240/243) but neither 142 nor 151 read it.
    SIX NEW BOOKS, none in the nine-book corpus:
      R3    ultra-concentrated composite-ranked top-3 at 0.75/3
      R60   composite-ranked top-60   (panels with >= 100 names only)
      R80   composite-ranked top-80   (panels with >= 100 names only)
      S3-75 TLT/GLD/UUP sleeve at 75% of the book (the corpus topped out at 50%)
      S4-25 TLT/GLD/DBC/UUP sleeve at 25%
      IVOL  inverse-60d-vol weights over every priced name, rescaled to gross 0.75
            (the only genuinely new CONSTRUCTION here: neither equal-weight nor rank-select)
    Cells: u56 {R3,S3-75,S4-25,IVOL} + broad {R3,R60,R80,S3-75,S4-25,IVOL}
         + small {R3,R60,R80,IVOL} + bstk100 {R3,R60,R80,IVOL,EWall,V1u,R5,R10,R20,R40}
         = 24 (panel, book) cells x 3 cost rungs {0, 10, 25} x idea 94's 17 arms
         = 72 paired cells, 1,224 arm-rows, every one written to .grid.csv.
    The six old equity books appear ONLY on the new panel; the four old panel-legs carry ONLY
    new books.  Gate (b) below asserts the (panel, book, cost, arm) key set is disjoint from
    idea 142's committed 816-row grid.

TUNED PARAMETERS — exactly two, identical to idea 151's so the pre-registration is literal
    1. the rule-8 DEFAULT, 6 values:  D_NONE (hold the ungated control; select nothing),
       K_Sharpe (argmax IS Sharpe, the incumbent), K_CAGR (argmax IS CAGR, THE CANDIDATE),
       K_Calmar, K_MaxDD, K_Random (seed 20260908, also reported as a 400-draw distribution).
    2. the POOL: P_ALL (all 17 arms) or P_S1 (IS-4b-admissible arms, phi=0.70, delta=0.60;
       control held on empty).
    Panels, books, cost rungs, arms, scoring metrics and the OOS window are REPORTED axes,
    never selected on.  All 6 x 2 x 72 = 864 picks go to .picks.csv.

PRE-REGISTERED PREDICTIONS (fixed before any number from this corpus was read)
    P1  PRIMARY.  paired mean d(OOS Sharpe) of K_CAGR minus K_Sharpe over the 72 new cells at
        P_ALL is POSITIVE with exact sign-test p < 0.05.   [142: +0.0415 / 151: +0.0342]
    P2  paired mean d(OOS Sharpe) of K_CAGR minus D_NONE is POSITIVE, sign p < 0.05.
                                                            [151: +0.0100, t +3.17]
    P3  paired mean d(OOS Sharpe) of K_Sharpe minus D_NONE is NEGATIVE.  [151: -0.0241]
    P4  K_CAGR buys OOS CAGR and pays OOS drawdown against K_Sharpe: d(OOS CAGR) > 0 and
        d(OOS MaxDD) < 0.                                   [151: +1.36 pp for -1.61 pp]
    P5  K_CAGR minus K_Random is POSITIVE (the gap is CAGR, not merely not-Sharpe).

PRE-REGISTERED DECISION RULE (stated before the run, applied once)
    PROTOCOL rule 8 may name K_CAGR as its default only if P1 AND P2 both hold on this corpus.
    If P1 holds and P2 does not, K_CAGR is a better argmax than the incumbent argmax and rule 8
    still gets the do-nothing control.  If P1 fails, rule 8 gets the do-nothing control.

WALK-FORWARD (PROTOCOL rule 8) — this run IS the walk-forward experiment
    Every default reads IS (<= 2016-12-31) ONLY; each pick is read ONCE on 2017-01-01..2026 and
    reported as OOS CAGR / Sharpe / MaxDD against that cell's do-nothing control, the LIVE
    RULES v2 book, RULES v1 and SPY, cost-matched at each rung.  Both KEEP paths are scored on
    all 1,224 rows: 4a against RULES v2 (live, the comparand PROTOCOL 3/4a names) and RULES v1
    (continuity), 4b on the full sample and again on the OOS window alone.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54).  All four panels are CURRENT constituents.  The small panel is the
      sub-$2B screen's survivors since 2010 with `max_1d_move >= 1.0` names dropped; bstk100 and
      broad are today's large caps; absent delistings inflate every CAGR here.  No level in this
      file is an achievable return and every 4b CAGR-floor margin is optimistic.  It cannot flip
      a PAIRED sign — both sides of every pair are drawn from the same flattered panel — but it
      does inflate the 4b counts, and it bears on K_CAGR specifically: a CAGR-argmax selector is
      the one most exposed to a panel whose CAGR is biased upward.  Stated, not corrected for.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so the P_S1
      screen's IS drawdown bar is measured on a window that cannot express a deep drawdown.
    * Idea 126: every row is t+1 execution only; no intraday, no fills.
    * 72 cells are not 72 independent observations — arms overlap heavily inside a panel and the
      six books on bstk100 share 100 names.  t-statistics are quoted on that understanding and
      the per-panel / per-rung / per-stratum breakdowns are printed so clustering is visible.
    * bstk100 has no ETFs, hence no sleeve books and no diversifier assets; its 4b bars are the
      same SPY bars as broad's because SPY is the benchmark on every panel.

HARNESS
    Idea 94's simulator and arms (H.run, H.arm_specs, H.targets, H.halves, H.window, H.pass4a),
    idea 129's census machinery (C.bars_win, C.margins_at, C.fails) and idea 133's book family
    (D.ranked, D.book_weights, D.panel_px) are IMPORTED, not re-implemented.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .picks.csv, .paired.csv,
.walkforward.csv and .keeppaths.csv next to itself.  Modifies nothing.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_pre-register-K_CAGR-as-the-rule-8-default_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
I142_GRID = OUT / "2026-09-08_selector-comparison-needs-more-cells_B.grid.csv"
I151_GRID = OUT / "2026-09-08_does-any-selector-beat-doing-nothing_B.grid.csv"

SEED = 20260908
PHI0, DELTA0 = 0.70, 0.60
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_CAGR": "IS_CAGR",
             "K_Calmar": "IS_Calmar", "K_MaxDD": "IS_MaxDD"}
DEFAULTS = ["D_NONE", "K_Sharpe", "K_CAGR", "K_Calmar", "K_MaxDD", "K_Random"]
POOLS = ["P_ALL", "P_S1"]
N_RANDOM_DRAWS = 400
BAD_MOVE = 1.0

# ---- THE NEW CORPUS (pre-registered; no (panel, book) pair read by idea 142 or 151) ----
CELLS = [("u56", b) for b in ("R3", "S3-75", "S4-25", "IVOL")] + \
        [("broad", b) for b in ("R3", "R60", "R80", "S3-75", "S4-25", "IVOL")] + \
        [("small", b) for b in ("R3", "R60", "R80", "IVOL")] + \
        [("bstk100", b) for b in ("R3", "R60", "R80", "IVOL",
                                  "EWall", "V1u", "R5", "R10", "R20", "R40")]
STRATUM = {c: ("NEW-PANEL" if c[0] == "bstk100" else "NEW-BOOK") for c in CELLS}


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
D = _load(I133, "i133")

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START

pd.set_option("display.width", 320)
pd.set_option("display.max_columns", 140)
pd.set_option("display.max_rows", 4000)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def calmar(cagr, dd):
    return cagr / abs(dd) if np.isfinite(dd) and abs(dd) > 1e-12 else np.nan


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def sign_p(wins, n):
    """Two-sided exact binomial sign test at p=0.5; ties excluded by the caller."""
    if n == 0:
        return np.nan
    lo = min(wins, n - wins)
    tail = sum(math.comb(n, k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


# ------------------------------------------------------------------ panels and books
def etf_set():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    return {t for g, v in U.items() if g != "megacap" for t in v} - {"BTC-USD", "ETH-USD"}


def panel_px(name):
    """u56 / broad / small are idea 133's construction verbatim.  bstk100 is NEW: the broad
    panel minus every ETF, with SPY held out as the benchmark return only."""
    if name != "bstk100":
        return D.panel_px(name)
    px = load_universe(broad=True)
    inv = [c for c in px.columns if c not in etf_set()]
    return px[inv], px["SPY"].pct_change().fillna(0.0)


def ivol_weights(px, window=60):
    """NEW book form: inverse trailing-60d-vol over every priced name, gross 0.75.  Uses only
    information through t (rolling std of past returns), applied at t+1 by the engine."""
    v = px.pct_change().rolling(window).std()
    inv = (1.0 / v.replace(0.0, np.nan)).where(px.notna())
    return GROSS * inv.div(inv.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def book_weights(px, book, gate=None, conv="dg"):
    """Delegate to idea 133 for every book it already builds; IVOL is the one new form and is
    gated in exactly the two conventions idea 133 uses (dg = to cash, rw = rebuild at gross)."""
    if book != "IVOL":
        return D.book_weights(px, book, gate, conv)
    if gate is None:
        return ivol_weights(px)
    g = H.gate_mask(px, gate)
    if conv == "dg":
        return ivol_weights(px).where(g, 0.0).fillna(0.0)
    v = px.pct_change().rolling(60).std()
    inv = (1.0 / v.replace(0.0, np.nan)).where(px.notna() & g)
    return GROSS * inv.div(inv.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


# ------------------------------------------------------------------ grid
def build_grid():
    rows, ref = [], {}
    panels = sorted({p for p, _ in CELLS}, key=lambda p: ["u56", "broad", "bstk100",
                                                          "small"].index(p))
    for pk in panels:
        px, spy_full = panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = C.bars_win(spy, "full"), C.bars_win(spy, "IS"), C.bars_win(spy, "OOS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        books = [b for p, b in CELLS if p == pk]
        ref[pk] = dict(bfull=bfull, bIS=bIS, bOOS=bOOS, spy=ms, spy_oos=mso, v1=v1, v2=v2)
        say(f"\n[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}, {len(books)} books {books}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS Sharpe {mso['Sharpe']:.3f} "
            f"CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        say(f"    4b bars (full): H1>{bfull['s1']:.3f} H2>{bfull['s2']:.3f} "
            f"OOS>{bfull['soos']:.3f} MaxDD<={DELTA0*abs(bfull['sdd']):.2%} "
            f"CAGR>={PHI0*bfull['scagr']:.2%}")
        for c in COSTS:
            mv2, mv1 = metrics(v2[c]), metrics(v1[c])
            o2, o1 = metrics(H.window(v2[c], "OOS")), metrics(H.window(v1[c], "OOS"))
            say(f"    RULES v2 @{c:>4.0f}bps CAGR {mv2['CAGR']:.2%} Sharpe {mv2['Sharpe']:.3f} "
                f"MaxDD {mv2['MaxDD']:.2%} OOS {o2['Sharpe']:.3f}/{o2['CAGR']:.2%}/"
                f"{o2['MaxDD']:.2%} | v1 Sharpe {mv1['Sharpe']:.3f} OOS {o1['Sharpe']:.3f}")

        # ---- gate (a): the modified runner reproduces engine.backtest on every ungated book ----
        worst = 0.0
        for b in books:
            W = book_weights(px, b)
            worst = max(worst, float((H.run(px, W, bps=10.0)["r"].loc[start:]
                                      - backtest(px, W, cost_bps=10.0,
                                                 freq=FREQ)["returns"].loc[start:]).abs().max()))
        say(f"[a] engine-equivalence, {len(books)} ungated books: max|diff| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — unsafe'})")

        for b in books:
            W_by_arm = {arm: book_weights(px, b, gate, conv)
                        for arm, kind, kw, (gate, conv) in H.arm_specs()}
            for c in COSTS:
                for arm, kind, kw, (gate, conv) in H.arm_specs():
                    res = H.run(px, W_by_arm[arm], bps=c, **kw)
                    r = res["r"].loc[start:]
                    mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
                    h1, h2 = H.halves(r)
                    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                    ismg = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    omg = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                    fail, ofail = C.fails(mg), C.fails(omg)
                    rows.append(dict(
                        panel=pk, book=b, cost=c, arm=arm, kind=kind, conv=conv,
                        stratum=STRATUM[(pk, b)],
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        IS_Calmar=calmar(mi["CAGR"], mi["MaxDD"]),
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        gross=res["gross"].loc[start:].mean(),
                        TO=res["to"].loc[start:].sum() / mm["Years"],
                        IS_m_H1=ismg["H1"], IS_m_H2=ismg["H2"], IS_m_DD=ismg["DD"],
                        IS_m_CAGR=ismg["CAGR"],
                        m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                        m_CAGR=mg["CAGR"],
                        pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-",
                        pass4b_oos=(len(ofail) == 0), fail4b_oos=",".join(ofail) or "-",
                        pass4a_v2=H.pass4a(r, v2[c]), pass4a_v1=H.pass4a(r, v1[c])))
    df = pd.DataFrame(rows)
    isbars = df.panel.map(lambda p: ref[p]["bIS"]["scagr"])
    core = (df.IS_m_H1 > 0) & (df.IS_m_H2 > 0) & (df.IS_m_DD > 0)
    df["adm_P_S1"] = core & (df.IS_CAGR - PHI0 * isbars > 0)
    df["adm_P_ALL"] = True
    return df, ref


# ------------------------------------------------------------------ gate (b): disjointness
def disjointness_gate(df):
    """The pre-registration IS the disjointness.  Assert this corpus shares no (panel, book)
    with either parent run, and no (panel, book, cost, arm) row either."""
    say("\n[b] PRE-REGISTRATION GATE — the corpus must be one neither parent read.")
    mine_pb = set(map(tuple, df[["panel", "book"]].drop_duplicates().values))
    ok = True
    for tag, path in (("idea 142", I142_GRID), ("idea 151", I151_GRID)):
        if not path.exists():
            say(f"    {tag}: committed grid not found at {path.name} — cannot assert; ABORT.")
            ok = False
            continue
        g = pd.read_csv(path)
        theirs_pb = set(map(tuple, g[["panel", "book"]].drop_duplicates().values))
        theirs_row = set(map(tuple, g[["panel", "book", "cost", "arm"]].values))
        mine_row = set(map(tuple, df[["panel", "book", "cost", "arm"]].values))
        say(f"    {tag}: {len(g)} committed rows over {len(theirs_pb)} (panel,book) cells "
            f"{sorted(theirs_pb)[:3]}...")
        say(f"        (panel,book) overlap with this corpus: {sorted(mine_pb & theirs_pb) or 0}")
        say(f"        (panel,book,cost,arm) row overlap: {len(mine_row & theirs_row)}")
        ok = ok and not (mine_pb & theirs_pb) and not (mine_row & theirs_row)
    say(f"    DISJOINT: {ok}  ({len(mine_pb)} new cells, {len(df)} new arm-rows)"
        f"{'' if ok else '  <-- the replication claim below is VOID'}")
    return ok


# ------------------------------------------------------------------ picks
def make_picks(df):
    """One pick per (cell, default, pool).  Every default reads IS columns only."""
    rng = np.random.default_rng(SEED)
    rows = []
    for (pk, b, c), s in df.groupby(["panel", "book", "cost"], sort=True):
        s = s.sort_values("arm").reset_index(drop=True)
        ctl = s.loc[s.arm == "control"].iloc[0]
        for pool in POOLS:
            adm = s.loc[s[f"adm_{pool}"]]
            empty = len(adm) == 0
            base = s if pool == "P_ALL" else (adm if not empty else s.loc[s.arm == "control"])
            for dflt in DEFAULTS:
                if dflt == "D_NONE":
                    pick = ctl.arm
                elif dflt == "K_Random":
                    pick = str(rng.choice(base.arm.values))
                else:
                    pick = base.loc[base[SELECTORS[dflt]].idxmax()].arm
                p = s.loc[s.arm == pick].iloc[0]
                top2 = base[SELECTORS[dflt]].nlargest(2).values if dflt in SELECTORS else []
                rows.append(dict(
                    panel=pk, book=b, cost=c, stratum=STRATUM[(pk, b)], pool=pool,
                    default=dflt, pick=pick, pool_n=len(base), pool_empty=empty,
                    is_control=(pick == "control"),
                    argmax_margin=(float(top2[0] - top2[1]) if len(top2) > 1 else np.nan),
                    OOS_Sharpe=p.OOS_Sharpe, OOS_CAGR=p.OOS_CAGR, OOS_MaxDD=p.OOS_MaxDD,
                    Sharpe=p.Sharpe, CAGR=p.CAGR, MaxDD=p.MaxDD, TO=p.TO, gross=p.gross,
                    pass4a_v2=p.pass4a_v2, pass4b=p.pass4b, pass4b_oos=p.pass4b_oos,
                    pool_mean_dSharpe=float(base.OOS_Sharpe.mean() - ctl.OOS_Sharpe)))
    return pd.DataFrame(rows)


def paired(P, a, b, pool="P_ALL", metric="OOS_Sharpe"):
    """Paired a-minus-b over the 72 cells at one pool, on one OOS metric."""
    key = ["panel", "book", "cost", "stratum"]
    A = P[(P["default"] == a) & (P.pool == pool)].set_index(key)
    B = P[(P["default"] == b) & (P.pool == pool)].set_index(key)
    d = (A[metric] - B.reindex(A.index)[metric]).dropna()
    nz = d[d.abs() > 1e-12]
    wins = int((nz > 0).sum())
    return dict(a=a, b=b, pool=pool, metric=metric, n=len(d), n_nonzero=len(nz),
                mean=float(d.mean()), t=tstat(d.values), wins=wins, losses=len(nz) - wins,
                ties=len(d) - len(nz),
                win_rate=(wins / len(nz) if len(nz) else np.nan),
                sign_p=sign_p(wins, len(nz)), series=d)


def show(res, note=""):
    say(f"    {res['a']:9s} - {res['b']:9s} [{res['pool']}, {res['metric']:11s}]  "
        f"mean {res['mean']:+.4f}  t {res['t']:+.2f}  "
        f"{res['wins']}W/{res['losses']}L/{res['ties']}T  win {res['win_rate']:.3f}  "
        f"sign p {res['sign_p']:.4f}  {note}")


# ------------------------------------------------------------------ main
def main():
    say("=" * 118)
    say("IDEA 416 — pre-register K_CAGR as the rule-8 default.  ONE reading of an unread corpus.")
    say(f"cells {len(CELLS)} | rungs {COSTS} | arms 17 | defaults {DEFAULTS} | pools {POOLS} | "
        f"seed {SEED} | IS<= {IS_END} | OOS>= {OOS_START}")
    say("=" * 118)

    df, ref = build_grid()
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n[grid] {len(df)} arm-rows over {df.groupby(['panel','book','cost']).ngroups} cells "
        f"-> {STEM}.grid.csv (ALL grid points reported)")

    disjoint = disjointness_gate(df)

    P = make_picks(df)
    P.drop(columns=[]).to_csv(OUT / f"{STEM}.picks.csv", index=False)
    say(f"[picks] {len(P)} picks (6 defaults x 2 pools x "
        f"{df.groupby(['panel','book','cost']).ngroups} cells) -> {STEM}.picks.csv")

    # -------------------------------------------------- the pre-registered readings
    say("\n" + "=" * 118)
    say("PRE-REGISTERED READINGS — reported once, on the unread corpus.")
    say("=" * 118)
    pr = {}
    say("\n  P1 (PRIMARY)  K_CAGR vs the incumbent K_Sharpe, OOS Sharpe, P_ALL:")
    pr["P1"] = paired(P, "K_CAGR", "K_Sharpe")
    show(pr["P1"], "[142: +0.0415 | 151: +0.0342]")
    say("\n  P2  K_CAGR vs DOING NOTHING, OOS Sharpe, P_ALL:")
    pr["P2"] = paired(P, "K_CAGR", "D_NONE")
    show(pr["P2"], "[151: +0.0100, t +3.17]")
    say("\n  P3  the incumbent K_Sharpe vs DOING NOTHING, OOS Sharpe, P_ALL:")
    pr["P3"] = paired(P, "K_Sharpe", "D_NONE")
    show(pr["P3"], "[151: -0.0241, t -3.34]")
    say("\n  P4  what K_CAGR trades against K_Sharpe (OOS CAGR up, OOS MaxDD down):")
    pr["P4c"] = paired(P, "K_CAGR", "K_Sharpe", metric="OOS_CAGR")
    pr["P4d"] = paired(P, "K_CAGR", "K_Sharpe", metric="OOS_MaxDD")
    show(pr["P4c"], "[151: +1.36 pp]")
    show(pr["P4d"], "[151: -1.61 pp]")
    say("\n  P5  K_CAGR vs the seeded RANDOM draw, OOS Sharpe, P_ALL:")
    pr["P5"] = paired(P, "K_CAGR", "K_Random")
    show(pr["P5"])

    ver = {"P1": pr["P1"]["mean"] > 0 and pr["P1"]["sign_p"] < 0.05,
           "P2": pr["P2"]["mean"] > 0 and pr["P2"]["sign_p"] < 0.05,
           "P3": pr["P3"]["mean"] < 0,
           "P4": pr["P4c"]["mean"] > 0 and pr["P4d"]["mean"] < 0,
           "P5": pr["P5"]["mean"] > 0}
    say("\n  VERDICT ON THE PRE-REGISTERED PREDICTIONS: "
        + "  ".join(f"{k}={'HOLDS' if v else 'FAILS'}" for k, v in ver.items()))
    say("  PRE-REGISTERED DECISION RULE — rule 8 names K_CAGR only if P1 AND P2 hold:")
    if ver["P1"] and ver["P2"]:
        dec = "NAME K_CAGR as the rule-8 default"
    elif ver["P1"]:
        dec = ("K_CAGR beats the incumbent argmax but NOT doing nothing -> rule 8 gets the "
               "DO-NOTHING control")
    else:
        dec = "P1 fails out of corpus -> rule 8 gets the DO-NOTHING control"
    say(f"      ==> {dec}"
        + ("" if disjoint else "   [VOID: corpus not disjoint]"))

    # -------------------------------------------------- where the gap lives
    say("\n" + "=" * 118)
    say("WHERE THE PRIMARY GAP LIVES (reported axes, never selected on)")
    say("=" * 118)
    d1 = pr["P1"]["series"].reset_index()
    for by in ("stratum", "panel", "cost", "book"):
        g = d1.groupby(by).OOS_Sharpe.agg(["count", "mean", lambda x: (x > 0).sum()])
        g.columns = ["n", "mean_d", "wins"]
        say(f"\n  by {by}:")
        say(g.to_string(float_format=lambda x: f"{x:+.4f}"))

    say("\n  the same three headline pairs, split by stratum and by cost rung:")
    rows = []
    for nm, (a, b) in {"P1 K_CAGR-K_Sharpe": ("K_CAGR", "K_Sharpe"),
                       "P2 K_CAGR-D_NONE": ("K_CAGR", "D_NONE"),
                       "P3 K_Sharpe-D_NONE": ("K_Sharpe", "D_NONE")}.items():
        s = paired(P, a, b)["series"].reset_index()
        for st, sub in s.groupby("stratum"):
            rows.append(dict(pair=nm, cut=f"stratum={st}", n=len(sub),
                             mean=sub.OOS_Sharpe.mean(), wins=int((sub.OOS_Sharpe > 0).sum())))
        for c, sub in s.groupby("cost"):
            rows.append(dict(pair=nm, cut=f"cost={c:.0f}bps", n=len(sub),
                             mean=sub.OOS_Sharpe.mean(), wins=int((sub.OOS_Sharpe > 0).sum())))
    say(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # -------------------------------------------------- full pair matrix + pools + random dist
    say("\n" + "=" * 118)
    say("EVERY DEFAULT AGAINST DOING NOTHING, BOTH POOLS, ALL THREE OOS METRICS")
    say("=" * 118)
    allrows = []
    for pool in POOLS:
        for dflt in DEFAULTS:
            if dflt == "D_NONE":
                continue
            for met in ("OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"):
                r = paired(P, dflt, "D_NONE", pool=pool, metric=met)
                allrows.append({k: v for k, v in r.items() if k != "series"})
    for dflt in DEFAULTS:
        if dflt in ("D_NONE", "K_Sharpe"):
            continue
        for met in ("OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"):
            r = paired(P, dflt, "K_Sharpe", metric=met)
            allrows.append({k: v for k, v in r.items() if k != "series"})
    A = pd.DataFrame(allrows)
    A.to_csv(OUT / f"{STEM}.paired.csv", index=False)
    say(A.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n  RANDOM-SELECTOR DISTRIBUTION (400 draws, the same 72 cells, P_ALL, OOS Sharpe):")
    rng = np.random.default_rng(SEED + 1)
    key = ["panel", "book", "cost"]
    ctl = df[df.arm == "control"].set_index(key).OOS_Sharpe
    cells = list(ctl.index)
    pools = {k: s.OOS_Sharpe.values for k, s in df.groupby(key)}
    draws = np.array([np.mean([rng.choice(pools[k]) - ctl[k] for k in cells])
                      for _ in range(N_RANDOM_DRAWS)])
    say(f"    mean {draws.mean():+.4f}  sd {draws.std(ddof=1):.4f}  "
        f"[2.5%, 97.5%] = [{np.quantile(draws,0.025):+.4f}, {np.quantile(draws,0.975):+.4f}]")
    for nm in ("K_CAGR", "K_Sharpe"):
        m = paired(P, nm, "D_NONE")["mean"]
        say(f"    {nm:9s} paired mean {m:+.4f} -> {(draws < m).mean()*100:5.1f}th percentile "
            f"of the random-selection distribution")

    # -------------------------------------------------- mechanism (idea 417's hypothesis)
    say("\n  MECHANISM: does a DECISIVE in-sample argmax do worse out of sample? "
        "(idea 151 found rho = -0.383)")
    for nm in ("K_Sharpe", "K_CAGR"):
        s = paired(P, nm, "D_NONE")["series"].reset_index()
        mg = P[(P["default"] == nm) & (P.pool == "P_ALL")].set_index(
            ["panel", "book", "cost", "stratum"]).argmax_margin
        j = s.set_index(["panel", "book", "cost", "stratum"]).join(mg.rename("mgn")).dropna()
        say(f"    {nm:9s} rho(d, IS_argmax_margin) = "
            f"{H.spearman(j.OOS_Sharpe.values, j.mgn.values):+.3f}  (n={len(j)})")

    # -------------------------------------------------- walk-forward table
    say("\n" + "=" * 118)
    say("RULE-8 WALK-FORWARD — every pick read ONCE on 2017-2026, vs the cell's own control, "
        "RULES v2 (live), RULES v1 and SPY")
    say("=" * 118)
    wf = []
    for _, p in P[P.pool == "P_ALL"].iterrows():
        R = ref[p.panel]
        cs = df[(df.panel == p.panel) & (df.book == p.book) & (df.cost == p.cost) &
                (df.arm == "control")].iloc[0]
        v2o, v1o = metrics(H.window(R["v2"][p.cost], "OOS")), metrics(H.window(R["v1"][p.cost],
                                                                               "OOS"))
        wf.append(dict(panel=p.panel, book=p.book, cost=p.cost, stratum=p.stratum,
                       default=p["default"], pick=p.pick,
                       OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                       ctl_OOS_Sharpe=cs.OOS_Sharpe, ctl_OOS_CAGR=cs.OOS_CAGR,
                       ctl_OOS_MaxDD=cs.OOS_MaxDD,
                       v2_OOS_Sharpe=v2o["Sharpe"], v2_OOS_CAGR=v2o["CAGR"],
                       v2_OOS_MaxDD=v2o["MaxDD"], v1_OOS_Sharpe=v1o["Sharpe"],
                       spy_OOS_Sharpe=R["spy_oos"]["Sharpe"], spy_OOS_CAGR=R["spy_oos"]["CAGR"],
                       spy_OOS_MaxDD=R["spy_oos"]["MaxDD"],
                       pass4a_v2=p.pass4a_v2, pass4b=p.pass4b, pass4b_oos=p.pass4b_oos))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.groupby("default")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "ctl_OOS_Sharpe",
                               "v2_OOS_Sharpe", "spy_OOS_Sharpe"]].mean()
        .to_string(float_format=lambda x: f"{x:+.4f}"))
    say("\n  per panel, OOS means over the 3 rungs x books (default = K_CAGR vs K_Sharpe vs "
        "D_NONE):")
    sub = WF[WF["default"].isin(["D_NONE", "K_Sharpe", "K_CAGR"])]
    say(sub.groupby(["panel", "default"])[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                                           "v2_OOS_Sharpe", "spy_OOS_Sharpe", "spy_OOS_CAGR",
                                           "spy_OOS_MaxDD"]].mean()
        .to_string(float_format=lambda x: f"{x:+.4f}"))

    # -------------------------------------------------- KEEP paths on every row
    say("\n" + "=" * 118)
    say("BOTH KEEP PATHS, scored on all 1,224 arm-rows (4a vs LIVE RULES v2 and vs v1; "
        "4b full and OOS-window)")
    say("=" * 118)
    K = df.groupby(["panel", "cost"]).agg(
        rows=("arm", "size"), pass4a_v2=("pass4a_v2", "sum"), pass4a_v1=("pass4a_v1", "sum"),
        pass4b=("pass4b", "sum"), pass4b_oos=("pass4b_oos", "sum"))
    K["BOTH_v2"] = df.groupby(["panel", "cost"]).apply(
        lambda s: int((s.pass4a_v2 & s.pass4b).sum()), include_groups=False)
    say(K.to_string())
    say(f"\n  TOTALS over {len(df)} rows: 4a(v2) {int(df.pass4a_v2.sum())}, "
        f"4a(v1) {int(df.pass4a_v1.sum())}, 4b {int(df.pass4b.sum())}, "
        f"4b(OOS window) {int(df.pass4b_oos.sum())}, "
        f"BOTH PATHS {int((df.pass4a_v2 & df.pass4b).sum())}")
    both = df[df.pass4a_v2 & df.pass4b]
    if len(both):
        say("\n  every both-paths row:")
        say(both[["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "gross", "TO"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("\n  no row clears both paths.")
    say("\n  4b failure attribution (which bar binds), all rows:")
    say(df.fail4b.value_counts().head(15).to_string())
    df[["panel", "book", "cost", "arm", "pass4a_v2", "pass4a_v1", "pass4b", "fail4b",
        "pass4b_oos", "fail4b_oos"]].to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)

    say("\n" + "=" * 118)
    say("SURVIVORSHIP CAVEAT (idea 54): all four panels are CURRENT constituents — the small "
        "panel is the sub-$2B screen's survivors since 2010 (max_1d_move >= 1.0 dropped), "
        "bstk100/broad/u56 are today's large caps.  Every CAGR here is inflated and every 4b "
        "CAGR-floor margin is optimistic; a CAGR-argmax selector is the one most exposed to "
        "that bias.  Paired signs are unaffected (both sides share the panel); 4b counts are "
        "not.  No level in this file is an achievable return.")
    say("=" * 118)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
