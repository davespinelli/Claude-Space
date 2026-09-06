#!/usr/bin/env python3
"""QUEUE idea 251 — does-reach-belong-beside-every-instrument-price (lane C, 2026-09-06).

Question (pre-registered)
-------------------------
Idea 74 found that above ~6pp of drawdown the insurance menu is decided by REACH — the
deepest MaxDD an instrument's WHOLE ladder can buy — and not by the instrument's price:
the per-name trailing stop cannot buy 4pp at any depth, absolute momentum stops at ~5pp,
the gates at ~7pp, idea 40's book DD control at ~9.4pp, and only de-grossing is unbounded.
Every price the record has ever published was quoted WITHOUT that column.

The queue asks, exactly: back-fill a `max_bought` column over every published
drawdown-instrument price in the record, and report how many published prices were quoted
at a budget the instrument could not actually reach.

Pre-registered definitions, fixed before any number is read:

    bought_pp  = (MaxDD_arm - MaxDD_control) * 100        # positive = shallower than control
    paid_pp    = (CAGR_control - CAGR_arm) * 100
    rate       = paid_pp / bought_pp                      # idea 74's axis, pp/pp
    max_bought = max over the family's WHOLE ladder of bought_pp      # REACH, per cell

A published price is `beyond_reach` when the drawdown budget it was quoted at exceeds the
family's `max_bought` on the MOST GENEROUS matched cell (max over panel x book at 10 bps).
Taking the maximum is deliberately conservative: it under-counts the exposure rather than
inflating it.

Two things are measured, and they are different:
  (1) REACH ITSELF, computed fresh here on idea 245's instrument-free base books, on BOTH
      idea 74's published 6-level ladder (PUB) and on an EXTENDED ladder (EXT) pushed to
      each family's admissible extreme.  If EXT moves reach a lot, idea 74's reach numbers
      are grid artefacts and the column would be quoting a grid edge, not an instrument.
  (2) THE CENSUS: every price claim in the record, with the budget it was quoted at where
      that is recoverable, tested against (1).

Design (PROTOCOL rules 1-8)
---------------------------
Universes : u56 = load_universe() (56 names + SPY); broad = load_universe(broad=True)
            (136 names).  BOTH reported.  SURVIVORSHIP: current constituents, so every
            panel here has shallower crashes than the real world had; reach is an
            absolute (not within-cell) quantity, so this bias is NOT cancelled and every
            `max_bought` printed below is, if anything, an UNDER-statement of what the
            instrument could buy in a panel containing the names that died.  Stated in
            the memo.
Books     : idea 245's two INSTRUMENT-FREE base books, IMPORTED not re-implemented —
            EWALL0 (equal-weight all names) and CAND20 (top-20 composite), gross 0.75.
Params    : exactly TWO tuned dimensions — instrument FAMILY (6) and its STRENGTH level.
            ALL grid points reported.  Panel, book, cost and ladder (PUB/EXT) are
            reporting axes printed at every value and never selected on.
Costs     : 10 bps (PROTOCOL, verdicts read here) and 25 bps, applied analytically.
Execution : PROTOCOL rule 2 throughout (decide at close t, execute at close t+1).
Baseline  : RULES v1 weekly (4a) and SPY buy-and-hold (4b); BOTH KEEP paths evaluated for
            every arm in the grid.
Rule 8    : reach is only a usable column if it is knowable IN ADVANCE.  The level that
            maximises reach is chosen on 2009-2016 ONLY, and 2017-2026 is then read once:
            does the IS-reach-maximising level still maximise OOS reach, how much OOS
            reach does the IS pick forfeit, and what does the IS-picked arm deliver in OOS
            CAGR/Sharpe/MaxDD against RULES v1 and SPY?

Harness gates, asserted before any result is read:
  [A] idea 245's own gates (run(no instrument) == engine.backtest, stop == idea 94's
      run_stop) run on import of its module.
  [B] every bought_pp recomputed here at idea 74's shared (panel, book, cost, family,
      level) points reproduces idea 74's COMMITTED grid CSV to ~0.
  [C] the census parser is auditable: every claim it extracts is written to
      .claims.csv with file:line provenance, and a hand-audited sample is reported.
"""
import importlib.util
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

# --- import idea 245's module (base books, simulator, instruments) -------------
_p245 = ROOT / "research" / "backtests" / "2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud.py"
_spec = importlib.util.spec_from_file_location("i245", _p245)
i245 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(i245)
run = i245.run
arm_returns = i245.arm_returns
BASE_BOOKS = i245.BASE_BOOKS
harness = i245.harness
m = i245.m
halves = i245.halves
at_cost = i245.at_cost
turn_per_yr = i245.turn_per_yr
fail4a = i245.fail4a
fail4b = i245.fail4b

COSTS = [10, 25]
PROTO_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BUDGETS = [2.0, 4.0, 6.0, 8.0, 10.0]        # idea 74's pre-registered budget grid, pp
SCRIPT = "research/backtests/2026-09-06_does-reach-belong-beside-every-instrument-price_C.py"
OUT = ROOT / "research" / "backtests" / "2026-09-06_does-reach-belong-beside-every-instrument-price_C"
I74_GRID = ROOT / "research" / "backtests" / "2026-09-06_drawdown-instrument-exchange-rate_cloud.grid.csv"
I74_MENU = ROOT / "research" / "backtests" / "2026-09-06_drawdown-instrument-exchange-rate_cloud.menu.csv"

FAMILIES = ["200d", "band", "abs", "dg", "ddctl", "stop"]
LABEL = {"200d": "200d-type MA gate", "band": "MA re-entry band", "abs": "absolute momentum",
         "dg": "de-gross (reference)", "ddctl": "book DD control (idea 40)",
         "stop": "per-name trailing stop"}

# idea 74's PUBLISHED ladder (the one every reach number in the record rests on)
PUB = {
    "200d":  [75, 100, 150, 200, 250, 300],
    "band":  [0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
    "abs":   [42, 63, 126, 189, 252, 378],
    "dg":    [0.90, 0.80, 0.70, 0.60, 0.50, 0.40],
    "ddctl": [0.05, 0.08, 0.12, 0.16, 0.20, 0.25],
    "stop":  [0.08, 0.10, 0.15, 0.20, 0.25, 0.30],
}
# EXTENDED ladder — each family pushed to its admissible extreme, so that a reach number
# is a property of the INSTRUMENT and not of idea 74's grid.  Superset of PUB.
EXT = {
    "200d":  [20, 50, 75, 100, 150, 200, 250, 300, 400, 500],
    "band":  [0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30],
    "abs":   [10, 21, 42, 63, 126, 189, 252, 378, 504, 756],
    "dg":    [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0.05, 0.00],
    "ddctl": [0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30, 0.40],
    "stop":  [0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50],
}


# ------------------------------------------------------------------ the grid
def build_grid(panels):
    """Every (panel, book, cost, family, level) arm on the EXT ladder (PUB is a subset).

    Returns the arm table with bought_pp / paid_pp / rate, the IS and OOS splits, and
    both KEEP-path verdicts.
    """
    rows = []
    for pname, px in panels.items():
        # idea 74's convention, kept EXACTLY so harness [B] is a bit-for-bit check and so
        # every reach number here is on the same window as the published ones: the first
        # 260 bars are the instruments' warm-up (200d MA, 252d momentum) and are dropped
        # from BOTH the arm and its control, so the comparison is matched.
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq="W")["returns"].loc[start:]
        base25 = backtest(px, rules_v1_weights(px), cost_bps=25, freq="W")["returns"].loc[start:]
        base_by_cost = {10: base, 25: base25}
        spy_oos_sh = metrics(spy[OOS_START:])["Sharpe"]
        for bname, bfn in BASE_BOOKS.items():
            w = bfn(px)
            ctrl_full = run(px, w)                # (gross, turn, invested, fires)
            ctrl = tuple(s.loc[start:] for s in ctrl_full[:3]) + (ctrl_full[3],)
            for cost in COSTS:
                cr = at_cost(ctrl[0], ctrl[1], cost)
                c_c, c_s, c_dd = m(cr)
                c_is = m(cr[:IS_END]); c_oos = m(cr[OOS_START:])
                rows.append(dict(panel=pname, book=bname, cost=cost, family="none", level=np.nan,
                                 CAGR=c_c, Sharpe=c_s, MaxDD=c_dd,
                                 H1=halves(cr)[0], H2=halves(cr)[1],
                                 IS_CAGR=c_is[0], IS_MaxDD=c_is[2], IS_Sharpe=c_is[1],
                                 OOS_CAGR=c_oos[0], OOS_Sharpe=c_oos[1], OOS_MaxDD=c_oos[2],
                                 paid_pp=0.0, bought_pp=0.0, rate=np.nan,
                                 IS_bought=0.0, OOS_bought=0.0,
                                 turn_yr=turn_per_yr(ctrl[1]), gross=float(ctrl[2].mean()),
                                 fail4a="|".join(fail4a(cr, base_by_cost[cost])),
                                 fail4b="|".join(fail4b(cr, spy, c_oos[1], spy_oos_sh)),
                                 in_pub=True))
                for fam in FAMILIES:
                    for lev in EXT[fam]:
                        g, t, inv, _ = arm_returns(px, w, fam, lev, ctrl_full)
                        g, t, inv = g.loc[start:], t.loc[start:], inv.loc[start:]
                        r = at_cost(g, t, cost)
                        a_c, a_s, a_dd = m(r)
                        a_is = m(r[:IS_END]); a_oos = m(r[OOS_START:])
                        rows.append(dict(
                            panel=pname, book=bname, cost=cost, family=fam, level=lev,
                            CAGR=a_c, Sharpe=a_s, MaxDD=a_dd,
                            H1=halves(r)[0], H2=halves(r)[1],
                            IS_CAGR=a_is[0], IS_MaxDD=a_is[2], IS_Sharpe=a_is[1],
                            OOS_CAGR=a_oos[0], OOS_Sharpe=a_oos[1], OOS_MaxDD=a_oos[2],
                            paid_pp=(c_c - a_c) * 100, bought_pp=(a_dd - c_dd) * 100,
                            rate=((c_c - a_c) * 100) / ((a_dd - c_dd) * 100)
                                 if (a_dd - c_dd) * 100 > 1e-9 else np.nan,
                            IS_bought=(a_is[2] - c_is[2]) * 100,
                            OOS_bought=(a_oos[2] - c_oos[2]) * 100,
                            turn_yr=turn_per_yr(t), gross=float(inv.mean()),
                            fail4a="|".join(fail4a(r, base_by_cost[cost])),
                            fail4b="|".join(fail4b(r, spy, a_oos[1], spy_oos_sh)),
                            in_pub=lev in PUB[fam]))
    return pd.DataFrame(rows)


def reach_table(grid, ladder):
    """max_bought per (panel, book, cost, family) on the requested ladder."""
    g = grid[grid.family != "none"]
    if ladder == "PUB":
        g = g[g.in_pub]
    out = []
    for (p, b, c, f), sub in g.groupby(["panel", "book", "cost", "family"]):
        i = sub.bought_pp.idxmax()
        j = sub[sub.bought_pp > 1e-9].rate.idxmin() if (sub.bought_pp > 1e-9).any() else None
        out.append(dict(ladder=ladder, panel=p, book=b, cost=c, family=f,
                        max_bought=sub.loc[i, "bought_pp"], at_level=sub.loc[i, "level"],
                        paid_at_max=sub.loc[i, "paid_pp"], rate_at_max=sub.loc[i, "rate"],
                        cheapest_rate=sub.loc[j, "rate"] if j is not None else np.nan,
                        IS_max_bought=sub.IS_bought.max(), OOS_max_bought=sub.OOS_bought.max(),
                        IS_argmax_level=sub.loc[sub.IS_bought.idxmax(), "level"],
                        OOS_argmax_level=sub.loc[sub.OOS_bought.idxmax(), "level"],
                        OOS_at_IS_pick=sub.loc[sub.IS_bought.idxmax(), "OOS_bought"]))
    return pd.DataFrame(out)


# ------------------------------------------------------------------ the census
CLAIM_RE = re.compile(
    r"(pp\s+(of\s+)?CAGR\s+(surrendered\s+)?(per|/)\s*pp|per\s+pp\s+of\s+(\|?MaxDD\|?|drawdown|DD)"
    r"|pp\s*/\s*pp|pp/pp|exchange[-\s]rate)", re.I)

FAMILY_KEYS = [
    ("stop",  [r"trailing stop", r"\bstop\b", r"idea 9\b", r"idea 94\b"]),
    ("ddctl", [r"ddctl", r"drawdown control", r"\bDD control\b", r"idea 40\b"]),
    ("band",  [r"re-entry band", r"\bband\d?\b", r"\bband\b"]),
    ("abs",   [r"absolute momentum", r"\babs[- ]?mom", r"\babs\b"]),
    ("200d",  [r"200d", r"trend gate", r"\bMA gate\b", r"\bgate\b"]),
    ("dg",    [r"de-?gross", r"static[- ]gross", r"gross lever", r"holding less",
               r"gross ladder", r"\blever\b", r"\bgross multiplier\b"]),
]
# depth phrasings: a number of pp of drawdown that a price was quoted against
DEPTH_RE = re.compile(
    r"([-+]?\d+(?:\.\d+)?)\s*(?:pp|percentage points?)\s*(?:of\s+)?"
    r"(?:\|?MaxDD\|?|drawdown|DD)\b", re.I)
BUDGET_RE = re.compile(r"\bT\s*=\s*(\d+(?:\.\d+)?)\s*pp", re.I)
RATE_RE = re.compile(r"([-+]?\d+(?:\.\d+)?)")


def classify_family(text):
    """Every instrument family the claim names. A comparative claim (a menu, a
    'dearer than de-gross' sentence) names several and is EXPOSED on each of them,
    so it is expanded into one (claim, family) pair per named family rather than
    being discarded as ambiguous."""
    return [f for f, keys in FAMILY_KEYS if any(re.search(k, text, re.I) for k in keys)]


def census(root):
    """Every published price claim in the record, with file:line provenance.

    Scope: research/**/*.md excluding research/deepvalue (stock triage packs, not
    drawdown-instrument prices).  A claim = one line matching CLAIM_RE.  The family is
    classified from a +/-3 line context window; the budget the price was quoted at is
    taken from an explicit `T = X pp` or an `X pp of MaxDD` phrase in the same window.
    """
    rows = []
    files = sorted([p for p in root.rglob("*.md") if "deepvalue" not in p.parts])
    for f in files:
        lines = f.read_text(errors="ignore").split("\n")
        for i, line in enumerate(lines):
            if not CLAIM_RE.search(line):
                continue
            lo, hi = max(0, i - 3), min(len(lines), i + 4)
            ctx = " ".join(lines[lo:hi])
            fams = classify_family(ctx)
            # STRICT: the depth a price was quoted at is read from the CLAIM'S OWN LINE.
            # A +/-3 line window leaks numbers out of neighbouring claims (verified: it
            # attributed a 28.1pp figure from an adjacent CHANGELOG entry), so the window
            # is used for naming the family only, and the LOOSE count is reported as an
            # upper bound rather than used for the verdict.
            strict = ([float(x) for x in BUDGET_RE.findall(line)]
                      + [abs(float(x)) for x in DEPTH_RE.findall(line)])
            loose = ([float(x) for x in BUDGET_RE.findall(ctx)]
                     + [abs(float(x)) for x in DEPTH_RE.findall(ctx)])
            base = dict(file=str(f.relative_to(root)), line=i + 1,
                        n_families=len(fams), families="+".join(fams) or "unclassified",
                        quoted_depth=max(strict) if strict else np.nan,
                        quoted_depth_loose=max(loose) if loose else np.nan,
                        n_depth_tokens=len(strict), text=line.strip()[:300])
            for fam in (fams or ["unclassified"]):
                rows.append(dict(base, family=fam))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ main
def main():
    print(f"=== idea 251 does-reach-belong-beside-every-instrument-price (lane C) ===\n{SCRIPT}\n")
    panels = {"u56": load_universe(), "broad": load_universe(broad=True)}
    for k, v in panels.items():
        print(f"panel {k}: {v.shape[1]} cols, {v.index[0].date()} .. {v.index[-1].date()}")

    print("\n--- harness [A] (idea 245's gates, u56) ---")
    harness(panels["u56"])

    print("\n--- building the arm grid (EXT ladder; PUB is a flagged subset) ---")
    grid = build_grid(panels)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    print(f"{len(grid)} rows ({(grid.family != 'none').sum()} arms + {(grid.family == 'none').sum()} controls)")

    # [B] reproduce idea 74's committed bought_pp at the shared points
    print("\n--- harness [B] vs idea 74's committed grid ---")
    i74 = pd.read_csv(I74_GRID)
    i74 = i74[i74.family != "none"].copy()
    key = ["panel", "book", "cost", "family", "level"]
    mine = grid[grid.family != "none"][key + ["bought_pp", "paid_pp", "MaxDD", "CAGR"]]
    j = i74.merge(mine, on=key, suffixes=("_74", "_C"))
    for col in ("bought_pp", "paid_pp", "MaxDD", "CAGR"):
        d = float(np.abs(j[f"{col}_74"] - j[f"{col}_C"]).max())
        print(f"[B] {col:10s} matched on {len(j)} shared points: max|diff| = {d:.3e}")
        assert d < 1e-9, col

    # ---- reach, both ladders
    reach = pd.concat([reach_table(grid, "PUB"), reach_table(grid, "EXT")], ignore_index=True)
    reach.to_csv(f"{OUT}.reach.csv", index=False)
    print("\n--- REACH: max_bought (pp of MaxDD the whole ladder can buy), 10 bps ---")
    print(f"{'family':<8}{'ladder':<7}{'u56/EWALL0':>12}{'u56/CAND20':>12}"
          f"{'broad/EWALL0':>14}{'broad/CAND20':>14}{'  best cell':>12}")
    for fam in FAMILIES:
        for lad in ("PUB", "EXT"):
            s = reach[(reach.family == fam) & (reach.ladder == lad) & (reach.cost == PROTO_COST)]
            g = {(r.panel, r.book): r.max_bought for r in s.itertuples()}
            print(f"{fam:<8}{lad:<7}{g[('u56','EWALL0')]:12.2f}{g[('u56','CAND20')]:12.2f}"
                  f"{g[('broad','EWALL0')]:14.2f}{g[('broad','CAND20')]:14.2f}"
                  f"{s.max_bought.max():12.2f}")

    # the single reportable column: the family's reach on the most generous cell @10bps
    REACH10 = {lad: {fam: float(reach[(reach.ladder == lad) & (reach.family == fam)
                                      & (reach.cost == PROTO_COST)].max_bought.max())
                     for fam in FAMILIES} for lad in ("PUB", "EXT")}
    print("\nmax_bought column as it would be published (max over the 4 matched cells, 10 bps):")
    for fam in FAMILIES:
        print(f"  {LABEL[fam]:<28} PUB {REACH10['PUB'][fam]:6.2f} pp   EXT {REACH10['EXT'][fam]:6.2f} pp")

    # ---- stratum 1: idea 74's own committed menu (fully machine-readable)
    print("\n--- STRATUM 1: idea 74's committed menu.csv (prices quoted AT a budget) ---")
    menu = pd.read_csv(I74_MENU)
    # per-CELL reach, so PUB and EXT are compared on the same footing (idea 74's
    # `reachable` flag is per panel x book x cost, not a best-cell number)
    ext_cell = reach[reach.ladder == "EXT"][["panel", "book", "cost", "family", "max_bought"]]
    pub_cell = reach[reach.ladder == "PUB"][["panel", "book", "cost", "family", "max_bought"]]
    menu = menu.merge(ext_cell.rename(columns={"max_bought": "reach_EXT"}),
                      on=["panel", "book", "cost", "family"], how="left")
    menu = menu.merge(pub_cell.rename(columns={"max_bought": "reach_PUB_mine"}),
                      on=["panel", "book", "cost", "family"], how="left")
    d = float(np.abs(menu.max_bought - menu.reach_PUB_mine).max())
    print(f"[B2] idea 74's committed per-cell max_bought reproduced here: max|diff| = {d:.3e}")
    assert d < 1e-9
    menu["unreach_PUB"] = ~menu.reachable
    menu["unreach_EXT"] = menu.budget > menu.reach_EXT
    menu.to_csv(f"{OUT}.menu_backfilled.csv", index=False)
    n = len(menu)
    print(f"{n} published menu entries (2 panels x 2 books x 2 costs x 6 families x 5 budgets)")
    print(f"  quoted beyond the PUBLISHED ladder's reach : {int(menu.unreach_PUB.sum()):3d}"
          f"  ({menu.unreach_PUB.mean():.1%})")
    print(f"  still beyond reach on the EXTENDED ladder  : {int(menu.unreach_EXT.sum()):3d}"
          f"  ({menu.unreach_EXT.mean():.1%})")
    closed = int((menu.unreach_PUB & ~menu.unreach_EXT).sum())
    print(f"  closed by extending the ladder             : {closed:3d}"
          f"  -> {'grid artefact' if closed > menu.unreach_PUB.sum()/2 else 'a real instrument limit'}")
    print("\n  by family (of 40 entries each): unreachable PUB / EXT")
    for fam in FAMILIES:
        s = menu[menu.family == fam]
        print(f"    {LABEL[fam]:<28} {int(s.unreach_PUB.sum()):2d} / {int(s.unreach_EXT.sum()):2d}")

    # ---- the corrected menu: what the 19 rescued quotes actually cost, and whether the
    # published ORDERING survives the instruments being priced at their true reach
    print("\n--- the menu re-read on the EXTENDED ladder (median rate over the 4 cells, "
          "10 bps; 'unreach' = no level of the family buys T in that cell) ---")
    arms10 = grid[(grid.family != "none") & (grid.cost == PROTO_COST)]
    print(f"{'family':<10}" + "".join(f"{'T=' + str(int(T)) + 'pp':>22}" for T in BUDGETS))
    for fam in FAMILIES:
        line = f"{fam:<10}"
        for T in BUDGETS:
            pub_r, ext_r, n_ok = [], [], 0
            for (p, b), sub in arms10[arms10.family == fam].groupby(["panel", "book"]):
                ok_e = sub[sub.bought_pp >= T]
                ok_p = sub[(sub.bought_pp >= T) & sub.in_pub]
                if len(ok_e):
                    n_ok += 1
                    ext_r.append(ok_e.loc[ok_e.paid_pp.idxmin()].rate)
                if len(ok_p):
                    pub_r.append(ok_p.loc[ok_p.paid_pp.idxmin()].rate)
            pv = f"{np.median(pub_r):.2f}" if pub_r else "unreach"
            ev = f"{np.median(ext_r):.2f}" if ext_r else "unreach"
            line += f"{pv + ' -> ' + ev + f' [{n_ok}/4]':>22}"
        print(line)
    print("  (PUB rate -> EXT rate [cells where the EXTENDED ladder reaches T]; "
          "de-gross is the reference row every other instrument has to beat)")

    # does back-filling reach CHANGE a published menu pick?
    flips, cells = [], 0
    for (p, b, c), sub in grid[grid.family != "none"].groupby(["panel", "book", "cost"]):
        for T in BUDGETS:
            cells += 1
            def cheapest(d):
                ok = d[d.bought_pp >= T]
                if not len(ok):
                    return None
                best = ok.loc[ok.rate.idxmin()]
                return (best.family, float(best.rate))
            cp, ce = cheapest(sub[sub.in_pub]), cheapest(sub)
            if (cp is None) != (ce is None) or (cp and ce and cp[0] != ce[0]):
                flips.append((p, b, c, T, cp, ce))
    print(f"\n  the pick a reader takes off the menu changes in {len(flips)}/{cells} "
          f"(panel, book, cost, budget) cells once reach is back-filled:")
    for p, b, c, T, cp, ce in flips:
        sp = "none reachable" if cp is None else f"{cp[0]} @ {cp[1]:.2f}"
        se = "none reachable" if ce is None else f"{ce[0]} @ {ce[1]:.2f}"
        print(f"    {p}/{b} @{c}bps T={T:.0f}pp : {sp:<22} -> {se}")

    # ---- stratum 2: the record's prose price claims
    print("\n--- STRATUM 2: census of published price claims in the record ---")
    cl = census(ROOT / "research")
    cl["reach_PUB"] = cl.family.map(REACH10["PUB"])
    cl["reach_EXT"] = cl.family.map(REACH10["EXT"])
    cl["beyond_reach_PUB"] = cl.quoted_depth > cl.reach_PUB
    cl["beyond_reach_EXT"] = cl.quoted_depth > cl.reach_EXT
    cl["beyond_reach_EXT_loose"] = cl.quoted_depth_loose > cl.reach_EXT
    # applicability: share of PROTOCOL's budget grid the family cannot reach at all
    cl["budget_share_unreachable"] = cl.family.map(
        lambda f: np.mean([b > REACH10["EXT"].get(f, np.inf) for b in BUDGETS])
        if f in REACH10["EXT"] else np.nan)
    cl.to_csv(f"{OUT}.claims.csv", index=False)
    n_lines = cl.groupby(["file", "line"]).ngroups
    print(f"{n_lines} price-claim lines in {cl.file.nunique()} files "
          f"-> {len(cl)} (claim, named-instrument) pairs")
    print(f"  lines naming no instrument family (unclassified): "
          f"{int((cl.family == 'unclassified').sum())}")
    print("\n  pairs per family (each carries a price the record published without a reach):")
    for fam in FAMILIES:
        k = int((cl.family == fam).sum())
        print(f"    {LABEL[fam]:<28} {k:3d}   reach(EXT) {REACH10['EXT'][fam]:6.2f} pp")
    cls = cl[cl.family.isin(FAMILIES)]
    withd = cls[cls.quoted_depth.notna()]
    print(f"\n  classified (claim, family) pairs          : {len(cls)}")
    print(f"  of those, a depth/budget is recoverable   : {len(withd)}  "
          f"({len(withd)/max(len(cls),1):.1%})  <- the record's prices almost never state "
          f"the depth they were quoted at")
    print(f"  quoted BEYOND reach (published ladder)    : {int(withd.beyond_reach_PUB.sum())}"
          f"  ({withd.beyond_reach_PUB.mean():.1%} of recoverable)")
    print(f"  quoted BEYOND reach (extended ladder)     : {int(withd.beyond_reach_EXT.sum())}"
          f"  ({withd.beyond_reach_EXT.mean():.1%} of recoverable)")
    wl = cls[cls.quoted_depth_loose.notna()]
    print(f"  [upper bound, LOOSE +/-3 line depth]      : {int(wl.beyond_reach_EXT_loose.sum())}"
          f" of {len(wl)} — reported as an upper bound only; the window leaks numbers "
          f"between adjacent claims")
    if withd.beyond_reach_EXT.any():
        print("\n  pairs quoted beyond reach (file:line, family, quoted depth vs reach):")
        for r in withd[withd.beyond_reach_EXT].itertuples():
            print(f"    {r.file}:{r.line}  {r.family:<6} quoted {r.quoted_depth:5.1f}pp "
                  f"> reach {r.reach_EXT:5.2f}pp")
            print(f"      | {r.text[:150]}")
    print("\n  EXPOSURE — share of PROTOCOL's own budget grid {2,4,6,8,10}pp on which each "
          "family's published prices are undefined:")
    tot_exposed = 0
    for fam in FAMILIES:
        sh = np.mean([b > REACH10["EXT"][fam] for b in BUDGETS])
        shp = np.mean([b > REACH10["PUB"][fam] for b in BUDGETS])
        n_fam = int((cls.family == fam).sum())
        tot_exposed += n_fam * sh
        print(f"    {LABEL[fam]:<28} PUB {shp:4.0%}  EXT {sh:4.0%}   "
              f"{n_fam:3d} published prices carry no reach column")
    print(f"    -> across the {len(cls)} classified pairs, a budget drawn uniformly from the "
          f"grid lands outside the instrument's reach {tot_exposed/max(len(cls),1):.1%} of the time")

    # ---- rule 8: is reach knowable in advance?
    print("\n--- RULE 8 walk-forward: is max_bought an EX-ANTE column? ---")
    wf = []
    for lad in ("PUB", "EXT"):
        s = reach[reach.ladder == lad]
        for r in s.itertuples():
            wf.append(dict(ladder=lad, panel=r.panel, book=r.book, cost=r.cost, family=r.family,
                           IS_argmax=r.IS_argmax_level, OOS_argmax=r.OOS_argmax_level,
                           IS_max=r.IS_max_bought, OOS_max=r.OOS_max_bought,
                           OOS_at_IS_pick=r.OOS_at_IS_pick,
                           regret=r.OOS_max_bought - r.OOS_at_IS_pick,
                           hit=bool(r.IS_argmax_level == r.OOS_argmax_level)))
    wf = pd.DataFrame(wf)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    for lad in ("PUB", "EXT"):
        s = wf[wf.ladder == lad]
        print(f"  {lad}: IS reach-argmax == OOS reach-argmax in {int(s.hit.sum())}/{len(s)} cells; "
              f"median OOS reach regret {s.regret.median():.2f} pp "
              f"(mean {s.regret.mean():.2f}, max {s.regret.max():.2f})")
    # does the IS reach ORDER the families the same way OOS?
    for lad in ("PUB", "EXT"):
        s = wf[(wf.ladder == lad) & (wf.cost == PROTO_COST)]
        rho = []
        for (p, b), sub in s.groupby(["panel", "book"]):
            rho.append(sub[["IS_max", "OOS_max"]].corr(method="spearman").iloc[0, 1])
        print(f"  {lad}: Spearman(IS reach, OOS reach) across the 6 families = "
              f"{np.mean(rho):.3f} (per-cell {', '.join(f'{x:.2f}' for x in rho)})")
    print("  LEVEL shift — a max_bought measured on one window is not the other window's:")
    for fam in FAMILIES:
        s = wf[(wf.ladder == "EXT") & (wf.family == fam)]
        print(f"    {LABEL[fam]:<28} IS {s.IS_max.mean():6.2f} pp -> OOS {s.OOS_max.mean():6.2f} pp"
              f"   (mean shift {s.OOS_max.mean() - s.IS_max.mean():+6.2f} pp)")
    s = wf[wf.ladder == "EXT"]
    print(f"    all families: OOS reach exceeds IS reach in {int((s.OOS_max > s.IS_max).sum())}"
          f"/{len(s)} cells — reach measured on 2009-2016 UNDER-states what the instrument "
          f"bought in 2017-2026")

    # ---- both KEEP paths, every arm
    print("\n--- KEEP paths (every arm in the grid, PROTOCOL rule 4) ---")
    arms = grid[grid.family != "none"]
    print(f"  arms passing 4a (no failing bar): {int((arms.fail4a == '').sum())}/{len(arms)}")
    print(f"  arms passing 4b (no failing bar): {int((arms.fail4b == '').sum())}/{len(arms)}")
    if (arms.fail4b == "").any():
        print(arms[arms.fail4b == ""][["panel", "book", "cost", "family", "level",
                                       "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"]].to_string(index=False))
    else:
        print("  none — this idea is a MEASUREMENT of the record, not a candidate book.")
    # OOS of the reach-maximising arms vs baselines, PROTOCOL rule 8 reporting
    px = panels["u56"]
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq="W")["returns"].loc[start:]
    bc, bs, bdd = m(base[OOS_START:]); sc, ss, sdd = m(spy[OOS_START:])
    print(f"\n  OOS (2017-2026) reference: RULES v1 {bc:.2%}/{bs:.3f}/{bdd:.1%}   "
          f"SPY {sc:.2%}/{ss:.3f}/{sdd:.1%}")
    print("  OOS of each family's IS-reach-maximising arm on u56/EWALL0 @10bps:")
    for fam in FAMILIES:
        sub = grid[(grid.panel == "u56") & (grid.book == "EWALL0") & (grid.cost == PROTO_COST)
                   & (grid.family == fam)]
        pick = sub.loc[sub.IS_bought.idxmax()]
        print(f"    {LABEL[fam]:<28} level {str(pick.level):>7}  OOS {pick.OOS_CAGR:6.2%}/"
              f"{pick.OOS_Sharpe:.3f}/{pick.OOS_MaxDD:6.1%}  (IS reach {pick.IS_bought:5.2f}pp, "
              f"OOS reach {pick.OOS_bought:5.2f}pp)")

    # ---- [C] auditable sample of the census parser (deterministic: every 11th pair)
    print("\n--- harness [C] census audit sample (every 11th classified pair; "
          "full table in .claims.csv) ---")
    for r in cls.iloc[::11].itertuples():
        print(f"  {r.file}:{r.line} -> {r.family:<6} depth="
              f"{'n/a' if not np.isfinite(r.quoted_depth) else f'{r.quoted_depth:.1f}pp'}")
        print(f"    | {r.text[:140]}")

    print(f"\nwrote {OUT}.grid.csv / .reach.csv / .menu_backfilled.csv / .claims.csv / .walkforward.csv")


if __name__ == "__main__":
    main()
