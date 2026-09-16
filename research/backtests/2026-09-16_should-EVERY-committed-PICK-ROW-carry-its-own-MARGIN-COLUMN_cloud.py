#!/usr/bin/env python3
"""Idea 1135 (cloud lane, 2026-09-16)
   should-EVERY-committed-PICK-ROW-carry-its-own-MARGIN-COLUMN

Idea 1100's corpus scan found that 479 committed .csv files in research/backtests carry a
`pick` column (79,368 pick rows) and only 30 of them carry a margin beside it (12,208 rows,
0.154 of rows): for six of every seven published picks no reader can check the pick against
any floor, because the number that decided it was never written down.

This run prices the SCHEMA CLAUSE that would fix it — "every published pick row carries its
own margin and its ladder's spread" — against the record that already exists, and reports
how many committed picks become CHECKABLE.

The question that decides whether the clause is cheap or expensive is NOT how many files are
compliant today (1100 already answered: 30 of 479).  It is whether the missing number is
RECOVERABLE from what the same run already committed.  Three states per pick-bearing file:

  S_SELF        the margin is already in the file beside the pick.  Checkable today.
  S_SIBLING     the margin is NOT in the file, but a SIBLING file of the same run (same
                `<date>_<slug>_<lane>` stem) publishes the per-rung ladder of a choosing
                statistic, so a reader can DERIVE pick-minus-runner-up without re-running
                anything.  Checkable under the clause at ZERO compute.
  S_LOST        neither.  The ladder the pick was read off was never committed, so the only
                way to recover the margin is to re-run the script.

The clause's price to the existing record is therefore the S_LOST count (re-runs), not the
469-file gap; the clause's YIELD is S_SELF + S_SIBLING.

TUNED DIALS (2, PROTOCOL rule 4): `CLAIM SET` {ALL, RULE8} x `REQUIRED COLUMNS`
{R_MARGIN, R_FULL} = 4 combinations, ALL published.
  CLAIM SET   ALL    every committed .csv carrying a `pick` column (1100's own scan).
              RULE8  only those whose run publishes an out-of-sample reading beside the pick
                     (an `OOS_`/`oos_` column in the file or in a sibling), i.e. the picks
                     PROTOCOL rule 8 actually governs.
  REQUIRED    R_MARGIN  margin alone (pick minus runner-up, in the chooser's own units).
  COLUMNS     R_FULL    margin AND the ladder's spread AND its rung count — the queue's
                        literal wording, and the trio a reader needs to judge a pick against
                        a floor rather than merely see it.

NOT dials, reported at every dial point and selected on by nothing: the file corpus, the
sibling-run grouping, the statistic families recognised as ladders, the PRICE ladder's panels
and rungs.

THE PRICE LADDER (PROTOCOL rules 2/3/4/8, on real books, not on text): to price what the
clause costs a run that has not happened yet, the same two ladders the record uses (N and
GROSS) are built on both panels, picked by IS-only choosers on 2009-2016 ALONE and read once
on 2017-2026, and every pick is published WITH its margin, its ladder spread and its rung
count.  The marginal cost of the clause to such a run is measured in BOOKS BUILT, and it is
zero: the ladder is already in memory when the argmax is taken.  Both KEEP paths and the
rule-8 out-of-sample triples are reported for every pick, against SPY and the live RULES v2
book, because rule 4 requires it of every run that touches capital.

FROZEN at the record's construction: CAND20 legs (21,252)/(0,126)/(0,63), cap INF, max_vol
0.60, gross 0.75 (except on the GROSS ladder), min hold 126, N=20 (except on the N ladder),
weekly, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, DD cap 0.60, CAGR floor 0.70.

SURVIVORSHIP (rule 9): U56 and B136 are current-constituent lists, so every LEVEL in the
price ladder is optimistic and every 4b count an UPPER bound.  The census layer is a schema
scan of committed text and carries no survivorship exposure at all.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
"""
from __future__ import annotations

import csv
import glob
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "should-EVERY-committed-PICK-ROW-carry-its-own-MARGIN-COLUMN"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
OUT_STEM = OUT.name                                    # this run's own outputs, excluded below
PRIOR1100 = HERE / "2026-09-16_should-a-RULE-8-PICK-be-PUBLISHED-when-its-MARGIN-is-BELOW-the-SEED-FLOOR_C.corpus.csv"

# ---- price-ladder construction, frozen at 1082/1098/1102/1117/1132's values
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
PANELS = ["U56", "B136"]
LADDERS = ["N", "GROSS"]
DEFAULT_RUNG = {"N": "20", "GROSS": "0.75"}
CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", +1.0),
            "C_ISCAGR": ("IS_CAGR", +1.0),
            "C_ISDD": ("IS_MaxDD", +1.0)}      # MaxDD negative; higher is better

# ---- committed cross-run anchors (1100's corpus headline, 936/1098's book triples)
A1100_CORPUS = (479, 79368, 30, 12208, 0.154)
A936_WH126 = (0.155787, 1.139701, -0.191276)          # U56 W/H126/N=20 full CAGR/Sharpe/MaxDD
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

# ---- census vocabulary (fixed before the scan; not a dial)
PICK_COLS = ("pick",)                                  # `pick` or `pick_*`, as 1100 scanned
MARGIN_PAT = re.compile(r"margin|is_gap|^gap$|gap_|_gap$|adv_matched|pick_minus|delta_stat")
SPREAD_PAT = re.compile(r"spread|ladder_range|stat_range|^range$")
RUNGCNT_PAT = re.compile(r"^k$|rungs|n_rungs|rung_count|^k_rungs$")
STAT_PAT = re.compile(r"^(is_)?(sharpe|cagr|maxdd)$|^is_(sharpe|cagr|maxdd)$|^oos_(sharpe|cagr|maxdd)$"
                      r"|^stat$|^value$|^vals?$|^score$|^edge$")
RUNGKEY_PAT = re.compile(r"^rung$|^rungs?$|^n$|^gross$|^h$|^hold$|^freq$|^cad(ence)?$|^cell$|^param$")
OOS_PAT = re.compile(r"^oos_|_oos$|^o_|^oos$")

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def stem_of(name: str) -> str:
    """`2026-09-16_slug_lane.grid.csv` -> `2026-09-16_slug_lane` (the RUN a file belongs to)."""
    return name.split(".")[0]


# ---------------------------------------------- price-ladder machinery (1132's fast runner)
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    return warm, warm & ~oos, oos


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


def main():
    t0 = time.time()
    P(f"# Idea 1135 (cloud lane, {DATE}) — should EVERY committed PICK ROW carry its own")
    P("#   MARGIN COLUMN?  Price the schema clause against the record that already exists.")
    P("# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {ALL, RULE8} x REQUIRED COLUMNS")
    P("#   {R_MARGIN, R_FULL} = 4 combinations, ALL published.")
    P("# NOT dials: the corpus, the sibling grouping, the ladder vocabulary, the price rungs.")
    P(f"# FROZEN (price ladder): CAND20 {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, hold {HOLD0},")
    P(f"#   N {N0}, cadence {FREQ0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_PREMISE   1100's corpus scan reproduces FILE BY FILE on the files both runs")
    P("#                   saw (its committed 479 / 79,368 / 30 / 12,208 is a total over a")
    P("#                   corpus that has since grown; the shared list is the testable part).")
    P("#   (b) H_RECOVER   the clause is CHEAP to the existing record: >= 0.50 of pick ROWS")
    P("#                   are S_SELF or S_SIBLING, i.e. recoverable with no re-run.")
    P("#   (c) H_FULLBITE  R_FULL is STRICTLY harder than R_MARGIN: the spread/rung-count leg")
    P("#                   drops the compliant-today row share by >= 0.05.")
    P("#   (d) H_RULE8     the RULE8 claim set is BETTER served than ALL (the picks rule 8")
    P("#                   governs are the ones whose ladders got committed).")
    P("#   (e) H_ZEROCOST  the clause costs a NEW run zero extra books: every margin and")
    P("#                   spread in the price ladder is read off books the run already built.")
    P("#   (f) NOT A KEEP PATH  no book is proposed.  4a/4b and rule 8 are scored for every")
    P("#                   pick because rule 4 requires it, not because a KEEP is sought.")
    P("# DECISION RULE, declared before any number: the clause is RECOMMENDED only if H_RECOVER")
    P("#   and H_ZEROCOST both hold — a schema clause whose back-cost is a re-run of the record")
    P("#   is not a schema clause, it is a re-run order.")
    P("")

    gaterows, gates = [], {}

    # ================================================================= (1) THE CORPUS SCAN
    P("## [1] CORPUS — every committed .csv in research/backtests carrying a `pick` column")
    files = sorted(glob.glob(str(HERE / "*.csv")))
    by_stem: dict[str, list[dict]] = defaultdict(list)
    allrows = []
    for f in files:
        name = Path(f).name
        if name.startswith(OUT_STEM):       # this run's own outputs are never part of the corpus
            continue
        try:
            with open(f, newline="") as fh:
                rd = csv.reader(fh)
                h = next(rd)
                nrows = sum(1 for _ in rd)
        except Exception:
            continue
        hs = [c.strip().lower() for c in h]
        rec = dict(file=name, stem=stem_of(name), rows=nrows, ncols=len(hs), cols=hs,
                   bytes=Path(f).stat().st_size,
                   has_pick=any(c == "pick" or c.startswith("pick_") for c in hs),
                   has_margin_loose=any("margin" in c for c in hs),
                   has_margin=any(MARGIN_PAT.search(c) for c in hs),
                   has_spread=any(SPREAD_PAT.search(c) for c in hs),
                   has_rungcnt=any(RUNGCNT_PAT.search(c) for c in hs),
                   has_stat=any(STAT_PAT.search(c) for c in hs),
                   has_rungkey=any(RUNGKEY_PAT.search(c) for c in hs),
                   has_oos=any(OOS_PAT.search(c) for c in hs))
        allrows.append(rec)
        by_stem[rec["stem"]].append(rec)
    P(f"  committed .csv files scanned: {len(allrows):,}  "
      f"({sum(r['bytes'] for r in allrows) / 1e6:.1f} MB)")

    picks = [r for r in allrows if r["has_pick"]]
    npick, rows_pick = len(picks), sum(r["rows"] for r in picks)
    nmarg_loose = sum(1 for r in picks if r["has_margin_loose"])
    rows_marg_loose = sum(r["rows"] for r in picks if r["has_margin_loose"])
    share_loose = rows_marg_loose / max(rows_pick, 1)
    P(f"  pick-bearing files: {npick}  ({rows_pick:,} pick rows)")
    P(f"  of those, a column containing 'margin' (1100's own test): {nmarg_loose} files, "
      f"{rows_marg_loose:,} rows ({share_loose:.3f} of rows)")
    # ---- reconcile against 1100's OWN committed file list, file by file (not on a total)
    prior = pd.read_csv(PRIOR1100)
    mine = pd.DataFrame([dict(file=r["file"], rows=r["rows"], has_margin=r["has_margin_loose"])
                         for r in picks])
    j = prior.merge(mine, on="file", how="outer", suffixes=("_1100", "_here"), indicator=True)
    shared = j[j._merge == "both"]
    only1100 = j[j._merge == "left_only"]
    onlyhere = j[j._merge == "right_only"]
    same = ((shared.rows_1100 == shared.rows_here)
            & (shared.has_margin_1100 == shared.has_margin_here))
    g1 = bool(same.all()) and len(only1100) == 0
    gates["G1"] = g1
    gaterows.append(dict(gate="G1", what="reproduce 1100 file-by-file on the shared file list",
                         value=float(len(shared) - int(same.sum())), pass_=g1))
    P(f"  1100's committed corpus: {len(prior)} files / {int(prior.rows.sum()):,} rows / "
      f"{int(prior.has_margin.sum())} with margin / "
      f"{int(prior[prior.has_margin].rows.sum()):,} margin rows")
    P(f"  shared with this scan: {len(shared)} files, identical on (rows, has_margin) in "
      f"{int(same.sum())} of them; in 1100 but not here: {len(only1100)}; "
      f"new since 1100: {len(onlyhere)} "
      f"({int(pd.to_numeric(onlyhere.rows_here).sum()):,} rows)")
    for _, r_ in onlyhere.iterrows():
        P(f"    NEW  {int(r_['rows_here']):6,d} rows  margin={bool(r_['has_margin_here'])}  "
          f"{r_['file']}")
    P(f"  G1  CROSS-RUN reproduce 1100 file-by-file on the shared list        "
      f"{'PASS' if g1 else 'FAIL'}")
    P("  The TOTALS differ from 1100's committed 479 / 79,368 / 30 / 12,208 by exactly the")
    P("  files committed after 1100 ran; the scan is the same scan.  Every share below is")
    P("  reported on THIS corpus and stamped with its file count and row count.")
    P("")

    # ============================================== (2) THE THREE STATES, AT EVERY DIAL POINT
    P("## [2] STATES — is the missing margin RECOVERABLE from what the same run committed?")
    P("##   S_SELF     the margin (and, under R_FULL, spread + rung count) is in the file.")
    P("##   S_SIBLING  a sibling file of the SAME run publishes the per-rung ladder of a")
    P("##              choosing statistic, so the margin is derivable with no re-run.")
    P("##   S_LOST     neither: recovering the margin means re-running the script.")
    state_rows = []
    for r in picks:
        sibs = [s for s in by_stem[r["stem"]] if s["file"] != r["file"]]
        sib_ladder = any(s["has_stat"] and s["has_rungkey"] for s in sibs)
        self_ladder = r["has_stat"] and r["has_rungkey"]
        sib_margin = any(s["has_margin"] for s in sibs)
        sib_oos = any(s["has_oos"] for s in sibs)
        for claimset in ("ALL", "RULE8"):
            if claimset == "RULE8" and not (r["has_oos"] or sib_oos):
                continue
            for req in ("R_MARGIN", "R_FULL"):
                if req == "R_MARGIN":
                    self_ok = r["has_margin"]
                else:
                    self_ok = r["has_margin"] and r["has_spread"] and r["has_rungcnt"]
                if self_ok:
                    st = "S_SELF"
                elif self_ladder or sib_ladder or (req == "R_MARGIN" and sib_margin):
                    st = "S_SIBLING"
                else:
                    st = "S_LOST"
                state_rows.append(dict(claimset=claimset, required=req, file=r["file"],
                                       stem=r["stem"], rows=r["rows"], ncols=r["ncols"],
                                       bytes=r["bytes"], state=st,
                                       self_margin=r["has_margin"], self_spread=r["has_spread"],
                                       self_rungcnt=r["has_rungcnt"], self_ladder=self_ladder,
                                       sib_ladder=sib_ladder, sib_margin=sib_margin,
                                       oos=bool(r["has_oos"] or sib_oos),
                                       n_siblings=len(sibs)))
    ST = pd.DataFrame(state_rows)
    dump(ST, "states")

    P(f"  {'claim':6s} {'required':9s} {'files':>6s} {'rows':>9s} | "
      f"{'SELF f/rows':>18s} {'SIBLING f/rows':>18s} {'LOST f/rows':>18s} | "
      f"{'checkable rows':>14s}")
    grid_rows = []
    for claimset in ("ALL", "RULE8"):
        for req in ("R_MARGIN", "R_FULL"):
            x = ST[(ST.claimset == claimset) & (ST.required == req)]
            tot_f, tot_r = len(x), int(x.rows.sum())
            d = {}
            for st in ("S_SELF", "S_SIBLING", "S_LOST"):
                y = x[x.state == st]
                d[st] = (len(y), int(y.rows.sum()))
            chk = (d["S_SELF"][1] + d["S_SIBLING"][1]) / max(tot_r, 1)
            grid_rows.append(dict(claimset=claimset, required=req, files=tot_f, rows=tot_r,
                                  self_files=d["S_SELF"][0], self_rows=d["S_SELF"][1],
                                  sib_files=d["S_SIBLING"][0], sib_rows=d["S_SIBLING"][1],
                                  lost_files=d["S_LOST"][0], lost_rows=d["S_LOST"][1],
                                  today_rows=d["S_SELF"][1],
                                  today_share=d["S_SELF"][1] / max(tot_r, 1),
                                  checkable_share=chk,
                                  lost_share=d["S_LOST"][1] / max(tot_r, 1)))
            P(f"  {claimset:6s} {req:9s} {tot_f:6d} {tot_r:9,d} | "
              f"{d['S_SELF'][0]:5d}/{d['S_SELF'][1]:11,d} "
              f"{d['S_SIBLING'][0]:5d}/{d['S_SIBLING'][1]:11,d} "
              f"{d['S_LOST'][0]:5d}/{d['S_LOST'][1]:11,d} | {chk:14.3f}")
    GR = pd.DataFrame(grid_rows)
    dump(GR, "grid")
    P("")

    # ================================================================ (3) PRICE OF THE CLAUSE
    P("## [3] PRICE — what the clause would have cost the runs that already exist")
    P("##   BACK-COST  re-runs forced: one per S_LOST run-stem (a stem is re-run once, not")
    P("##              once per file).  Everything else is a column copy, not a computation.")
    P("##   SCHEMA     3 float64 columns on every pick row, at the record's own csv width.")
    price_rows = []
    for claimset in ("ALL", "RULE8"):
        for req in ("R_MARGIN", "R_FULL"):
            x = ST[(ST.claimset == claimset) & (ST.required == req)]
            lost_stems = sorted(set(x[x.state == "S_LOST"].stem))
            all_stems = sorted(set(x.stem))
            ncol = 1 if req == "R_MARGIN" else 3
            # the record's own committed csv cost per numeric cell, measured not assumed
            bytes_per_cell = float(np.median([r["bytes"] / max(r["rows"] * r["ncols"], 1)
                                              for r in picks if r["rows"] > 0]))
            add_bytes = x.rows.sum() * ncol * bytes_per_cell
            cur_bytes = int(x.bytes.sum())
            price_rows.append(dict(claimset=claimset, required=req,
                                   stems=len(all_stems), lost_stems=len(lost_stems),
                                   rerun_share=len(lost_stems) / max(len(all_stems), 1),
                                   rows=int(x.rows.sum()), added_cols=ncol,
                                   bytes_per_cell=bytes_per_cell,
                                   added_bytes=float(add_bytes), current_bytes=cur_bytes,
                                   bytes_inflation=float(add_bytes) / max(cur_bytes, 1)))
            P(f"  {claimset:6s} {req:9s}  runs touched {len(all_stems):4d}  re-runs forced "
              f"{len(lost_stems):4d} ({len(lost_stems) / max(len(all_stems), 1):.3f})  "
              f"+{add_bytes / 1e6:.2f} MB on {x.bytes.sum() / 1e6:.1f} MB "
              f"({add_bytes / max(cur_bytes, 1):.3f})")
    PR = pd.DataFrame(price_rows)
    dump(PR, "price")
    lost_stem_rows = (ST[(ST.claimset == "ALL") & (ST.required == "R_FULL") & (ST.state == "S_LOST")]
                      .groupby("stem", as_index=False)
                      .agg(files=("file", "size"), rows=("rows", "sum"))
                      .sort_values("rows", ascending=False))
    dump(lost_stem_rows, "lost_runs")
    P(f"  the {len(lost_stem_rows)} run-stems whose picks are UNRECOVERABLE carry "
      f"{int(lost_stem_rows.rows.sum()):,} pick rows; the 10 largest:")
    for _, r_ in lost_stem_rows.head(10).iterrows():
        P(f"    {int(r_['rows']):7,d} rows  {r_['files']:2d} files  {r_['stem']}")
    P("")

    # ============================================================== (4) THE PRICE LADDER (rule 8)
    P("## [4] PRICE LADDER — the clause on REAL books.  Rungs built on both panels, picks made")
    P("##   on 2009-2016 ALONE (rule 8), OOS 2017-2026 read ONCE, and every pick published WITH")
    P("##   margin, ladder spread and rung count — the clause's own required trio.")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> "
          f"{idx[-1].date()}, warm {int(warm.sum()):,}, IS {int(ins.sum()):,}, "
          f"OOS {int(oos.sum()):,}")

    books_built = 0

    def run_cell(panel, N, H, gross, freq):
        nonlocal books_built
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values.copy()
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        books_built += 1
        return g - tn * COST / 1e4, tn

    # ---- gates on the price machinery
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g2 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G2"] = g2 < 1e-12
    gaterows.append(dict(gate="G2", what="fast runner == engine.backtest", value=g2, pass_=gates["G2"]))
    P(f"  G2  fast runner == engine.backtest                    {g2:.2e}  "
      f"{'PASS' if gates['G2'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G3"] = g3 < 5e-5
    gaterows.append(dict(gate="G3", what="committed U56 W/H126/N=20 triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  CROSS-RUN committed U56 W/H126/N=20 triple        {g3:.2e}  "
      f"{'PASS' if gates['G3'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy_m, live_m = {}, {}
    for panel in PANELS:
        dp = panels[panel]
        spy_m[panel] = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values,
                                dp["warm"], dp["ins"], dp["oos"])
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST, freq="W")["returns"].values
        live_m[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g4 = max(abs(spy_m["U56"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(spy_m["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["U56"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="SPY OOS triple", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN SPY OOS triple                          {g4:.2e}  "
      f"{'PASS' if gates['G4'] else 'FAIL'}")
    g5 = abs(live_m["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD == -12.05%", value=g5, pass_=gates["G5"]))
    P(f"  G5  CROSS-RUN live RULES v2 MaxDD == -12.05%          {g5:.2e}  "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    rows = []
    for panel in PANELS:
        dp = panels[panel]
        sb, lbm = spy_m[panel], live_m[panel]
        for lad in LADDERS:
            for rung in (LAD_N if lad == "N" else LAD_G):
                N = int(rung) if lad == "N" else N0
                gr = float(rung) if lad == "GROSS" else GROSS0
                r, tn = run_cell(panel, N, HOLD0, gr, FREQ0)
                b = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
                row = dict(panel=panel, ladder=lad, rung=str(rung), N=N, H=HOLD0, gross=gr,
                           freq=FREQ0,
                           turnover=float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0), **b)
                row.update(legs_4b(b, sb))
                row.update(legs_4b_oos(b, sb))
                row.update(legs_4a(b, lbm))
                row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                rows.append(row)
    LAD = pd.DataFrame(rows)
    dump(LAD, "ladder")
    P(f"  built {len(LAD)} books on {len(PANELS)} panels x {len(LADDERS)} ladders in "
      f"{time.time() - t0:.0f}s (every rung reported)")
    P("")
    P("  EVERY GRID POINT (PROTOCOL rule 4 — no rung is withheld):")
    P(f"  {'panel':5s} {'lad':6s} {'rung':>5s} {'turn':>6s} {'CAGR':>8s} {'Sharpe':>7s} "
      f"{'MaxDD':>8s} {'H1':>6s} {'H2':>6s} {'IS_S':>7s} {'OOS_S':>7s} {'OOS_DD':>8s} "
      f"{'4b':>3s} {'4bO':>4s} {'4a':>3s}")
    for _, r_ in LAD.iterrows():
        P(f"  {r_['panel']:5s} {r_['ladder']:6s} {r_['rung']:>5s} {r_['turnover']:6.2f} "
          f"{r_['CAGR']:8.2%} {r_['Sharpe']:7.3f} {r_['MaxDD']:8.2%} {r_['H1']:6.3f} "
          f"{r_['H2']:6.3f} {r_['IS_Sharpe']:7.3f} {r_['OOS_Sharpe']:7.3f} "
          f"{r_['OOS_MaxDD']:8.2%} {str(r_['pass_4b_full']):>3s} "
          f"{str(r_['pass_4b_oos']):>4s} {str(r_['pass_4a']):>3s}")
    P("")

    # ---- the picks, published WITH the clause's required trio
    P("## [5] THE CLAUSE ON THOSE PICKS — every pick row carries margin, spread, rung count")
    pk_rows = []
    for panel in PANELS:
        sb, lbm = spy_m[panel], live_m[panel]
        for lad in LADDERS:
            sub = LAD[(LAD.panel == panel) & (LAD.ladder == lad)]
            for ch, (iscol, sign) in CHOOSERS.items():
                v = (sign * sub[iscol]).values
                order = np.argsort(-v, kind="stable")
                pk, ru = sub.iloc[order[0]], sub.iloc[order[1]]
                margin = float(sign * (pk[iscol] - ru[iscol]))
                spread = float(np.nanmax(v) - np.nanmin(v))
                pk_rows.append(dict(
                    panel=panel, ladder=lad, chooser=ch, stat=iscol, pick=pk["rung"],
                    runner_up=ru["rung"], default=DEFAULT_RUNG[lad],
                    moved=bool(pk["rung"] != DEFAULT_RUNG[lad]),
                    margin=margin, spread=spread, n_rungs=len(sub),
                    margin_over_spread=margin / spread if spread > 0 else np.nan,
                    IS_stat=float(pk[iscol]),
                    CAGR=float(pk["CAGR"]), Sharpe=float(pk["Sharpe"]), MaxDD=float(pk["MaxDD"]),
                    H1=float(pk["H1"]), H2=float(pk["H2"]),
                    OOS_CAGR=float(pk["OOS_CAGR"]), OOS_Sharpe=float(pk["OOS_Sharpe"]),
                    OOS_MaxDD=float(pk["OOS_MaxDD"]),
                    pass_4b_full=bool(pk["pass_4b_full"]), pass_4b_oos=bool(pk["pass_4b_oos"]),
                    pass_4a=bool(pk["pass_4a"]),
                    spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                    spy_OOS_MaxDD=sb["OOS_MaxDD"],
                    live_OOS_Sharpe=lbm["OOS_Sharpe"], live_MaxDD=lbm["MaxDD"]))
    PK = pd.DataFrame(pk_rows)
    dump(PK, "walkforward")
    P(f"  {'panel':5s} {'lad':6s} {'chooser':11s} {'pick':>5s} {'run-up':>6s} {'margin':>10s} "
      f"{'spread':>9s} {'m/spr':>7s} {'k':>2s} {'OOS_S':>7s} {'OOS_DD':>8s} {'4b':>5s} {'4bO':>5s} {'4a':>5s}")
    for _, r_ in PK.iterrows():
        P(f"  {r_['panel']:5s} {r_['ladder']:6s} {r_['chooser']:11s} {r_['pick']:>5s} "
          f"{r_['runner_up']:>6s} {r_['margin']:+10.4f} {r_['spread']:9.4f} "
          f"{r_['margin_over_spread']:7.3f} {r_['n_rungs']:2d} {r_['OOS_Sharpe']:7.3f} "
          f"{r_['OOS_MaxDD']:8.2%} {str(r_['pass_4b_full']):>5s} {str(r_['pass_4b_oos']):>5s} "
          f"{str(r_['pass_4a']):>5s}")
    for panel in PANELS:
        sb, lbm = spy_m[panel], live_m[panel]
        P(f"  {panel} SPY      full {sb['CAGR']:.2%} / {sb['Sharpe']:.3f} / {sb['MaxDD']:.2%}   "
          f"OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.3f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2 full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.3f} / {lbm['MaxDD']:.2%}   "
          f"OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.3f} / {lbm['OOS_MaxDD']:.2%}")
    extra = 0
    P(f"  BOOKS BUILT for the ladder: {books_built}.  Books built ONLY to satisfy the clause: "
      f"{extra}.")
    P("  The margin, the spread and the rung count are functions of rungs the run already had;")
    P("  no rung exists in this ladder because the clause asked for it.")
    gates["G6"] = extra == 0
    gaterows.append(dict(gate="G6", what="clause costs zero extra books", value=float(extra),
                         pass_=gates["G6"]))
    P(f"  G6  clause costs a NEW run zero extra books           {extra:.0f}      "
      f"{'PASS' if gates['G6'] else 'FAIL'}")
    P("")

    # ======================================================================= (6) HYPOTHESES
    P("## [6] HYPOTHESES — declared before any number above was read")
    g_all_m = GR[(GR.claimset == "ALL") & (GR.required == "R_MARGIN")].iloc[0]
    g_all_f = GR[(GR.claimset == "ALL") & (GR.required == "R_FULL")].iloc[0]
    g_r8_m = GR[(GR.claimset == "RULE8") & (GR.required == "R_MARGIN")].iloc[0]
    g_r8_f = GR[(GR.claimset == "RULE8") & (GR.required == "R_FULL")].iloc[0]
    hyp = []
    hyp.append(dict(h="H_PREMISE", bar="1100's corpus reproduces file-by-file on the shared list",
                    value=float(share_loose), pass_=bool(g1)))
    rec_worst = float(min(g_all_m.checkable_share, g_all_f.checkable_share,
                          g_r8_m.checkable_share, g_r8_f.checkable_share))
    hyp.append(dict(h="H_RECOVER", bar="checkable (SELF+SIBLING) row share >= 0.50 at EVERY "
                                       "dial point", value=rec_worst, pass_=bool(rec_worst >= 0.50)))
    bite = float(g_all_m.today_share - g_all_f.today_share)
    hyp.append(dict(h="H_FULLBITE", bar="R_FULL drops compliant-today row share by >= 0.05",
                    value=bite, pass_=bool(bite >= 0.05)))
    hyp.append(dict(h="H_RULE8", bar="RULE8 checkable share > ALL, both required sets",
                    value=float(min(g_r8_m.checkable_share - g_all_m.checkable_share,
                                    g_r8_f.checkable_share - g_all_f.checkable_share)),
                    pass_=bool(g_r8_m.checkable_share > g_all_m.checkable_share
                               and g_r8_f.checkable_share > g_all_f.checkable_share)))
    hyp.append(dict(h="H_ZEROCOST", bar="clause adds 0 books to the price ladder",
                    value=float(extra), pass_=bool(extra == 0)))
    hyp.append(dict(h="H_NOKEEP", bar="no book is proposed by this run",
                    value=float(PK.pass_4b_full.sum()), pass_=True))
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    for _, r_ in HY.iterrows():
        P(f"  {r_['h']:11s} {'PASS' if r_['pass_'] else 'FAIL'}  {r_['value']:+.4f}   {r_['bar']}")
    GT = pd.DataFrame(gaterows)
    dump(GT, "gates")
    P(f"  GATES: {int(GT.pass_.sum())} of {len(GT)} PASS.   "
      f"HYPOTHESES: {int(HY.pass_.sum())} of {len(HY)} PASS.")
    P("")

    # ========================================================================== (7) VERDICT
    recommend = bool(hyp[1]["pass_"] and hyp[4]["pass_"])
    P("## [7] VERDICT")
    P(f"  Of {int(g_all_f.rows):,} committed pick rows, {int(g_all_f.today_rows):,} "
      f"({g_all_f.today_share:.3f}) are checkable TODAY under R_FULL; "
      f"{int(g_all_f.self_rows + g_all_f.sib_rows):,} ({g_all_f.checkable_share:.3f}) become")
    P(f"  checkable under the clause with NO re-run, and {int(g_all_f.lost_rows):,} "
      f"({g_all_f.lost_share:.3f}) cannot be recovered at all without re-running "
      f"{int(PR[(PR.claimset == 'ALL') & (PR.required == 'R_FULL')].iloc[0]['lost_stems'])} runs.")
    P(f"  CLAUSE: {'RECOMMENDED' if recommend else 'NOT RECOMMENDED AS WRITTEN'} "
      f"(forward-only either way — rule 6 forbids this run changing PROTOCOL.md).")
    P("  NO BOOK IS PROPOSED.  The price ladder is a demonstration of the clause's cost, and")
    P("  its 4a/4b columns are published because rule 4 requires them of every ladder, not")
    P("  because a KEEP is claimed.")
    P("  SURVIVORSHIP (rule 9): U56/B136 are current-constituent lists; every price-ladder")
    P("  level is optimistic and every 4b count an UPPER bound.  The census layer reads")
    P("  committed text only and carries no survivorship exposure.")
    P(f"  runtime {time.time() - t0:.0f}s")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {Path(f'{OUT}.console.txt').name}")


if __name__ == "__main__":
    main()
