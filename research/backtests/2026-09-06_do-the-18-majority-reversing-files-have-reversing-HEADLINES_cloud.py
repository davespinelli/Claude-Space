#!/usr/bin/env python3
"""Idea 268 - "do-the-18-majority-reversing-files-have-reversing-HEADLINES" (cloud, 2026-09-06).

The question
------------
Idea 259 censused 37,044 EWall-vs-ranked comparison pairs across 91 committed CSVs and found
33.7% reverse between Sharpe and CAGR, with **18 of 91 files** where a MAJORITY of pairs
reverse.  The queue's follow-up is a scope question, not a new statistic:

    "a grid row is not a published sentence.  Read the headline claim of each of those 18
     parents and report how many of the SENTENCES (not rows) change once the CAGR column
     is beside them."

A grid CSV can be 62% reversing without a single published sentence depending on it, if the
EWall arm is a CARRIER (a second base book dragged through an overlay study) rather than the
subject of the claim.  This run measures that gap.

Design (two legs)
-----------------
A. SENTENCE AUDIT (the queue's literal ask).  Re-derive the 18 files from idea 259's committed
   `.census.csv.gz` (majority = reversal share > 0.50 among RANKED pairs), map them to their
   PARENT scripts, and read every parent's committed prose: `.result.md`, `.memo.md` if any,
   and every `research/LEADERBOARD.md` row whose last column names that script.

   Pre-registered definitions, fixed before any prose was read:
     * HEADLINE = the parent's title line plus the contiguous block of text before the first
       `##` sub-heading (this is where every parent in the record puts its bolded verdict).
       BODY = the remainder of the file.
     * A sentence is EWALL-MENTIONING if it contains an EWall-type token
       (`EWall`, `ewall`, `ew-all`, `EW-all`, `equal-weight-all`, `equal-weight all`, `EWALL`).
     * A sentence is a COMPARATIVE EWall-vs-ranked CLAIM if it is EWall-mentioning AND names a
       ranked-book token (`top20`, `top-20`, `top-n`, `ranked`, `FWD`, `CAND`, `V1`, `R5..R40`,
       `STK`, `frac`, `band`-book) AND carries a comparative verb/operator
       (`beat`, `win`, `lose`, `better`, `worse`, `higher`, `lower`, `dominat`, `outperform`,
       `underperform`, `>`, `<`, `vs`).
     * A claim's METRIC is SHARPE if the sentence names Sharpe and not CAGR, CAGR if the
       reverse, BOTH if both, UNQUALIFIED if neither.
     * A claim CHANGES iff it is a SHARPE or UNQUALIFIED comparative EWall-vs-ranked claim AND
       the census pairs from that parent that back it reverse in a majority of cells.
   The headline count is the answer; the body count is reported beside it so the reader can see
   how much of the exposure sits below the headline.

B. CONTROLLED RE-RUN (the empirical leg; PROTOCOL rules 2-4 and 8).
   Ten of the eleven parents share one construction: a carrier pair {`ewall`, `top20`} dragged
   through an overlay dial, with the HEADLINE always about the DIAL, never about the pair.  So
   the sentence-shaped question is not "does EWall beat top20 on both metrics" (idea 259 already
   answered that) but "does the OVERLAY DELTA - the difference the parents actually publish -
   reverse between Sharpe and CAGR too?"  Both are measured here on one construction:

     arms    EWall  = every eligible name, equal weight        (the carrier)
             TOP20  = top 20 by the composite key, equal weight (the ranked carrier)
     dials   TWO separate 2-parameter grids, each swept exhaustively, no pick across them:
               grid G  gross g in {0.55, 0.65, 0.75, 0.85, 1.00}  at band 0   (ref g = 0.75)
               grid B  200d re-entry band in {0, 2, 3, 5, 8}%     at g = 0.75 (ref band = 0)
             gross is the dial every one of the 11 parents carries; the band is added because
             gross turned out to be a PURE LEVER (Sharpe invariant to it, so a within-book
             delta cannot reverse by construction) and the sentence-shaped test needs a dial
             with real Sharpe content
     gate    above 200d MA AND vol20 < 0.60;  key = composite WITHOUT the vol scaler
     weekly, next-day execution, 10 bps (0 bps carried as a diagnostic column only)

   CARRIER reversal   = sign(dSharpe) != sign(dCAGR) for EWall - TOP20 at fixed (panel, g, bps)
   SENTENCE reversal  = the same test on the within-book overlay delta d(g) = metric(g) -
                        metric(g = 0.75), which is the statistic the parents' sentences assert.

Tuned parameters (PROTOCOL rule 4: at most two) - leg B only
    grid G: 1. panel (4)  2. gross g (5)      grid B: 1. panel (4)  2. band (5)
Each grid is selected on SEPARATELY (rule 8 argmax within a grid); nothing is picked across
the two, so neither grid exceeds two tuned parameters.
The arm axis (EWall vs TOP20) is the hypothesis, not a dial.  The cost rung is fixed at
PROTOCOL's 10 bps; 0 bps is a diagnostic, never selected on.  Leg A tunes nothing - it reads
committed files.  ALL grid points are written to `.grid.csv` and printed.

Walk-forward (PROTOCOL rule 8), direction pre-registered before any OOS number was read
    IS = 2009-01-01..2016-12-31 chooses; OOS = 2017-01-01..end read ONCE.
      S_SHARPE  argmax IS Sharpe over (arm x g) within the panel   - the metric the record quotes
      S_CAGR    argmax IS CAGR   over (arm x g) within the panel   - the metric it does not
      EWALL_ref EWall at the grid's reference dial value, no selection - do-nothing carrier
      TOP20_ref TOP20 at the grid's reference dial value, no selection - do-nothing ranked
    If the reversal is a REPORTING artefact the two selectors pick the same point and rule 8 is
    silent; if it is a DECISION they diverge and the OOS gap is the price of quoting one metric.
    OOS CAGR/Sharpe/MaxDD are reported against the RULES v1 baseline and against SPY.

Verdicts (both KEEP paths, evaluated on EVERY leg-B point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1 (same panel, same rung).
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

SURVIVORSHIP: universe_broad.json, the BSTK100 megacap cut and the 483-name sub-$2B panel are
CURRENT constituents - dead names are absent.  On a list of known survivors the un-ranked book
that holds EVERYTHING inherits the full survivorship premium while any ranking rule can only
redistribute it, so the bias runs TOWARD the pro-EWall side of every comparison counted here.
Names with `max_1d_move >= 1.0` in data/small_meta.csv are dropped from the small panel first.

Deterministic, standalone.  Reads baseline.py and committed artefacts; writes only its own files.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import re
import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

COST_BPS, DIAG_BPS = 10, 0
FREQ = "W"
MAX_VOL = 0.60
N_RANKED = 20
GROSSES = [0.55, 0.65, 0.75, 0.85, 1.00]
G_REF = 0.75
BANDS = [0.0, 0.02, 0.03, 0.05, 0.08]   # 200d re-entry band (idea 57/84/91)
B_REF = 0.0
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
EPS_S, EPS_C = 0.005, 0.0005          # idea 259's pre-registered epsilons, reused verbatim
CENSUS = "2026-09-06_does-the-sharpe-cagr-reversal-sit-under-every-EWall-claim_C.census.csv.gz"

OUT = REPO / "research" / "backtests"
STEM = Path(__file__).name[:-3]
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ============================================================ LEG A: the sentence audit
EW_TOK = re.compile(r"\b(EWall|ewall|EWALL|EW-all|ew-all|ew_all|equal[- ]weight[- ]all|"
                    r"equal-weight all|un-?ranked book)\b")
RANKED_TOK = re.compile(r"\b(top ?-?20|top-?n|top ?\d+|ranked|FWD\d*|CAND\w*|V1u?C?|v1|"
                        r"R\d+|STK\d*|BSTK\d*|frac|band\d)\b")
CMP_TOK = re.compile(r"(beat\w*|win\w*|won|lose\w*|lost|better|worse|higher|lower|dominat\w*|"
                     r"outperform\w*|underperform\w*|ahead of|behind|>|<|\bvs\b|\bversus\b)")
SHARPE_TOK = re.compile(r"Sharpe", re.I)
CAGR_TOK = re.compile(r"\bCAGR\b|pp/yr|return\b", re.I)

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(*`\"'‘“])")


def sentences(text):
    """Prose sentences only: markdown tables, code fences and bullet-only lines are dropped."""
    out, in_code = [], False
    for para in text.split("\n\n"):
        lines = []
        for ln in para.split("\n"):
            if ln.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if ln.strip().startswith("|") or set(ln.strip()) <= set("|-: "):
                continue
            lines.append(ln)
        blob = " ".join(lines).strip()
        if not blob:
            continue
        for s in SENT_SPLIT.split(blob):
            s = s.strip()
            if len(s) >= 12:
                out.append(s)
    return out


def split_headline(md):
    """HEADLINE = title line + everything before the first '##'; BODY = the rest."""
    lines = md.split("\n")
    cut = len(lines)
    for i, ln in enumerate(lines):
        if ln.startswith("## "):
            cut = i
            break
    return "\n".join(lines[:cut]), "\n".join(lines[cut:])


def classify(s):
    ew = bool(EW_TOK.search(s))
    rk = bool(RANKED_TOK.search(s))
    cm = bool(CMP_TOK.search(s))
    if not ew:
        return dict(ew=False, claim=False, metric="")
    sh, cg = bool(SHARPE_TOK.search(s)), bool(CAGR_TOK.search(s))
    metric = "BOTH" if (sh and cg) else "SHARPE" if sh else "CAGR" if cg else "UNQUALIFIED"
    return dict(ew=True, claim=bool(rk and cm), metric=metric)


def leg_a():
    cen = pd.read_csv(OUT / CENSUS)
    ranked = cen[cen.cmp_class == "RANKED"]
    g = ranked.groupby("file").agg(pairs=("rev", "size"), rev=("rev", "sum"))
    g["share"] = g.rev / g.pairs
    maj = g[g.share > 0.50].sort_values("share", ascending=False)

    P("\n" + "=" * 100)
    P("LEG A - the 18 majority-reversing files, re-derived from idea 259's committed census")
    P("=" * 100)
    P(f"RANKED-pair files in census: {len(g)}   majority-reversing (share > 0.50): {len(maj)}")
    P(fmt(maj.assign(share=maj.share), 3))

    # file -> parent script stem (strip the artefact suffix, e.g. '.grid.csv', '.census.csv.gz')
    def parent(fn):
        return re.sub(r"\.[a-z0-9_]+\.csv(\.gz)?$", "", fn)

    maj = maj.reset_index()
    maj["parent"] = maj.file.map(parent)
    parents = sorted(maj.parent.unique())
    P(f"\n{len(maj)} files -> {len(parents)} distinct PARENT scripts:")
    for p in parents:
        fs = maj[maj.parent == p]
        P(f"  {p}   ({len(fs)} file(s), reversal share "
          f"{'/'.join(f'{x:.2f}' for x in fs.share)})")

    lb = (REPO / "research" / "LEADERBOARD.md").read_text().split("\n")

    rows, sent_rows = [], []
    for p in parents:
        md_paths = [OUT / f"{p}.result.md"] + sorted(OUT.glob(f"{p}.memo.md"))
        md = "\n\n".join(q.read_text() for q in md_paths if q.exists())
        if not md:
            P(f"  !! no prose committed for {p}")
            continue
        head, body = split_headline(md)
        lb_rows = [ln for ln in lb if p in ln and ln.startswith("|")]
        blocks = [("HEADLINE", sentences(head)), ("BODY", sentences(body)),
                  ("LEADERBOARD", [ln.strip() for ln in lb_rows])]
        counts = {}
        for where, sents in blocks:
            n_ew = n_claim = 0
            for s in sents:
                c = classify(s)
                if not c["ew"]:
                    continue
                n_ew += 1
                n_claim += int(c["claim"])
                sent_rows.append(dict(parent=p, block=where, metric=c["metric"],
                                      claim=c["claim"], sentence=s[:400]))
            counts[where] = (len(sents), n_ew, n_claim)
        rows.append(dict(
            parent=p,
            files=int((maj.parent == p).sum()),
            max_share=float(maj.loc[maj.parent == p, "share"].max()),
            pairs=int(maj.loc[maj.parent == p, "pairs"].sum()),
            head_sent=counts["HEADLINE"][0], head_ew=counts["HEADLINE"][1],
            head_claim=counts["HEADLINE"][2],
            body_sent=counts["BODY"][0], body_ew=counts["BODY"][1], body_claim=counts["BODY"][2],
            lb_rows=counts["LEADERBOARD"][0], lb_ew=counts["LEADERBOARD"][1],
            lb_claim=counts["LEADERBOARD"][2],
        ))
    aud = pd.DataFrame(rows)
    sen = pd.DataFrame(sent_rows)

    P("\n" + "-" * 100)
    P("Per-parent sentence census (head_* = title + pre-'##' verdict block)")
    P("-" * 100)
    P(fmt(aud.set_index("parent"), 2))

    P(f"\nTOTALS over the {len(aud)} parents:")
    P(f"  HEADLINE sentences                     : {aud.head_sent.sum()}")
    P(f"  ... mentioning an EWall-type arm       : {aud.head_ew.sum()}")
    P(f"  ... comparative EWall-vs-ranked CLAIMS : {aud.head_claim.sum()}   <-- the queue's unit")
    P(f"  BODY sentences                         : {aud.body_sent.sum()}")
    P(f"  ... mentioning an EWall-type arm       : {aud.body_ew.sum()}")
    P(f"  ... comparative EWall-vs-ranked CLAIMS : {aud.body_claim.sum()}")
    P(f"  LEADERBOARD rows naming these parents  : {aud.lb_rows.sum()}  "
      f"(EWall-mentioning {aud.lb_ew.sum()}, claims {aud.lb_claim.sum()})")

    if not sen.empty:
        P("\nEvery EWall-mentioning sentence found, by block and metric:")
        P(fmt(sen.pivot_table(index="block", columns="metric", values="claim",
                              aggfunc="size", fill_value=0), 0))
        P("\nAll comparative EWall-vs-ranked claims (verbatim, truncated to 400 chars):")
        cl = sen[sen.claim]
        if cl.empty:
            P("  (none)")
        for _, r in cl.iterrows():
            P(f"  [{r.block}/{r.metric}] {r.parent}\n      {r.sentence}")

    # backing pairs for any headline claim
    P("\nBacking-pair reversal for HEADLINE claims (the 'does the sentence change' test):")
    hc = sen[(sen.block == "HEADLINE") & (sen.claim)] if not sen.empty else pd.DataFrame()
    changed = 0
    if hc.empty:
        P("  0 headline claims -> 0 sentences can change.  The reversal exposure in these files "
          "is entirely BELOW the headline (carrier rows), not in it.")
    else:
        for _, r in hc.iterrows():
            f = maj[maj.parent == r.parent]
            sh = float(f.share.max())
            ch = r.metric in ("SHARPE", "UNQUALIFIED") and sh > 0.50
            changed += int(ch)
            P(f"  {r.parent}: metric={r.metric}, backing reversal share {sh:.2f} -> "
              f"{'CHANGES' if ch else 'stands'}")
    P(f"\nLEG A ANSWER: {changed} of {aud.head_claim.sum()} headline claims change; "
      f"{len(aud)} parents / {len(maj)} files carry the 62%-reversing rows.")

    aud.to_csv(OUT / f"{STEM}.audit.csv", index=False)
    if not sen.empty:
        sen.to_csv(OUT / f"{STEM}.sentences.csv", index=False)
    maj.to_csv(OUT / f"{STEM}.files.csv", index=False)
    return aud, sen, maj


# ============================================================ LEG B: the controlled re-run
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    P(f"panels: U56 {px56.shape}, B136 {px136.shape}, small raw {pxs.shape}, "
      f"small dropped for max_1d_move>=1.0: {len(set(pxs.columns) & bad)}")
    return {
        "U56": sub(px56, list(px56.columns)),
        "B136": sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL": sub(pxs, s_stk, tradable=s_stk),
    }


def eligible_mask(px, tradable, band=0.0):
    """band = re-entry band on the 200d gate (idea 57/84/91's construction).

    band 0 is the plain `px > 200dMA` gate.  band b > 0 is hysteresis: a name enters when
    px > MA*(1+b), leaves when px < MA*(1-b), and holds its previous state in between.
    """
    _, above, vol20 = score(px)
    if band > 0:
        ma = px.rolling(200).mean()
        state = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        state = state.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
        above = state.ffill().fillna(0.0).astype(bool) & ma.notna()
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights(px, tradable, arm, g, band=0.0):
    elig = eligible_mask(px, tradable, band)
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        key = score(px, vol_scale=False)[0]
        sel = (key.where(elig).rank(axis=1, ascending=False) <= N_RANKED).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(g).fillna(0.0)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, r_oos, spy_oos):
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def v4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def paired_t(d):
    d = np.asarray([x for x in d if np.isfinite(x)], float)
    if len(d) < 2:
        return np.nan, np.nan, 0
    se = d.std(ddof=1) / np.sqrt(len(d))
    return d.mean(), (d.mean() / se if se > 0 else np.nan), int((d > 0).sum())


def leg_b(panels, dial, values, cache):
    """One 2-parameter grid: panel x `dial`.  dial='g' sweeps gross at band 0;
    dial='band' sweeps the 200d re-entry band at gross G_REF.  All points reported."""
    rows = []
    for pname, (px, tr) in panels.items():
        spy = px["SPY"].pct_change().fillna(0)
        start = px.index[260]
        for bps in (COST_BPS, DIAG_BPS):
            if ("v1", pname, "v1", np.nan, bps) not in cache:
                bres = backtest(px, rules_v1_weights(px), cost_bps=bps, freq=FREQ)
                cache[("v1", pname, "v1", np.nan, bps)] = bres["returns"].loc[start:]
        for arm in ("EWall", "TOP20"):
            for v in values:
                g = v if dial == "g" else G_REF
                band = v if dial == "band" else 0.0
                w = weights(px, tr, arm, g, band)
                for bps in (COST_BPS, DIAG_BPS):
                    res = backtest(px, w, cost_bps=bps, freq=FREQ)
                    r = res["returns"].loc[start:]
                    sp = spy.loc[start:]
                    r_is, r_oos = r.loc[IS_START:IS_END], r.loc[OOS_START:]
                    sp_oos = sp.loc[OOS_START:]
                    mm, mo, mi = metrics(r), metrics(r_oos), metrics(r_is)
                    h1, h2 = halves(r)
                    cache[(arm, pname, dial, v, bps)] = r
                    rows.append(dict(
                        dial=dial, panel=pname, arm=arm, val=v, g=g, band=band, bps=bps,
                        CAGR=mm["CAGR"], Vol=mm["Vol"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                        H1=h1, H2=h2, IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        Turn_yr=float(res["turnover"].loc[start:].sum() / (len(r) / 252)),
                        gross_real=float(w.loc[start:].sum(axis=1).mean()),
                        SPY_CAGR=metrics(sp)["CAGR"], SPY_Sharpe=metrics(sp)["Sharpe"],
                        SPY_MaxDD=metrics(sp)["MaxDD"],
                        SPY_OOS_Sharpe=metrics(sp_oos)["Sharpe"],
                    ))
                    P(f"  ran {pname:8s} {arm:6s} {dial}={v:.2f} {bps:2d}bps  "
                      f"CAGR {mm['CAGR']:6.2%}  Sharpe {mm['Sharpe']:.3f}  "
                      f"DD {mm['MaxDD']:6.2%}  OOS_Sharpe {mo['Sharpe']:.3f}")
    grid = pd.DataFrame(rows)
    p4a, f4b = [], []
    for _, r in grid.iterrows():
        rr = cache[(r.arm, r.panel, r.dial, r.val, r.bps)]
        base = cache[("v1", r.panel, "v1", np.nan, r.bps)]
        px = panels[r.panel][0]
        sp = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        p4a.append(v4a(rr, base))
        f4b.append(fail4b(rr, sp, rr.loc[OOS_START:], sp.loc[OOS_START:]))
    grid["pass4a"] = p4a
    grid["fail4b"] = f4b
    grid["pass4b"] = grid.fail4b == "-"
    return grid, cache


def reversals(grid, ref_val):
    """(i) carrier reversal EWall-TOP20 at fixed (panel,val,bps); (ii) overlay-delta reversal."""
    car = []
    for (pn, v, bps), s in grid.groupby(["panel", "val", "bps"]):
        e = s[s.arm == "EWall"].iloc[0]
        t = s[s.arm == "TOP20"].iloc[0]
        dS, dC = e.Sharpe - t.Sharpe, e.CAGR - t.CAGR
        dOS, dOC = e.OOS_Sharpe - t.OOS_Sharpe, e.OOS_CAGR - t.OOS_CAGR
        car.append(dict(panel=pn, val=v, bps=bps, S_ew=e.Sharpe, S_top=t.Sharpe,
                        C_ew=e.CAGR, C_top=t.CAGR, dS=dS, dC=dC, dOS=dOS, dOC=dOC,
                        rev=bool(np.sign(dS) != np.sign(dC) and abs(dS) > EPS_S and abs(dC) > EPS_C),
                        rev_oos=bool(np.sign(dOS) != np.sign(dOC) and abs(dOS) > EPS_S
                                     and abs(dOC) > EPS_C)))
    car = pd.DataFrame(car)

    ov = []
    for (pn, arm, bps), s in grid.groupby(["panel", "arm", "bps"]):
        ref = s[s.val == ref_val].iloc[0]
        for _, r in s.iterrows():
            if r.val == ref_val:
                continue
            dS, dC = r.Sharpe - ref.Sharpe, r.CAGR - ref.CAGR
            ov.append(dict(panel=pn, arm=arm, bps=bps, val=r.val, dS=dS, dC=dC,
                           rev=bool(np.sign(dS) != np.sign(dC) and abs(dS) > EPS_S
                                    and abs(dC) > EPS_C),
                           dS_small=bool(abs(dS) <= EPS_S)))
    ov = pd.DataFrame(ov)
    return car, ov


def rule8(grid, cache, panels, ref_val):
    out = []
    for (pn, bps), s in grid.groupby(["panel", "bps"]):
        dial = s.dial.iloc[0]
        px = panels[pn][0]
        sp = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        base = cache[("v1", pn, "v1", np.nan, bps)]
        picks = {
            "S_SHARPE": s.loc[s.IS_Sharpe.idxmax()],
            "S_CAGR": s.loc[s.IS_CAGR.idxmax()],
            "EWALL_ref": s[(s.arm == "EWall") & (s.val == ref_val)].iloc[0],
            "TOP20_ref": s[(s.arm == "TOP20") & (s.val == ref_val)].iloc[0],
        }
        for nm, r in picks.items():
            rr = cache[(r.arm, pn, dial, r.val, bps)].loc[OOS_START:]
            m = metrics(rr)
            out.append(dict(panel=pn, bps=bps, selector=nm, pick=f"{r.arm}@{dial}{r.val:.2f}",
                            IS_Sharpe=r.IS_Sharpe, IS_CAGR=r.IS_CAGR,
                            OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
        bo, so = metrics(base.loc[OOS_START:]), metrics(sp.loc[OOS_START:])
        out.append(dict(panel=pn, bps=bps, selector="RULESv1", pick="baseline",
                        IS_Sharpe=metrics(base.loc[IS_START:IS_END])["Sharpe"],
                        IS_CAGR=metrics(base.loc[IS_START:IS_END])["CAGR"],
                        OOS_CAGR=bo["CAGR"], OOS_Sharpe=bo["Sharpe"], OOS_MaxDD=bo["MaxDD"]))
        out.append(dict(panel=pn, bps=bps, selector="SPY", pick="buy-and-hold",
                        IS_Sharpe=metrics(sp.loc[IS_START:IS_END])["Sharpe"],
                        IS_CAGR=metrics(sp.loc[IS_START:IS_END])["CAGR"],
                        OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"]))
    return pd.DataFrame(out)


def main():
    aud, sen, maj = leg_a()

    P("\n" + "=" * 100)
    P("LEG B - controlled re-run: carrier pair vs within-book dial delta, TWO 2-parameter grids")
    P("=" * 100)
    panels = build_panels()
    cache = {}
    grids, cars, ovs, wfs = [], [], [], []
    cols = ["panel", "arm", "val", "bps", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2",
            "IS_Sharpe", "IS_CAGR", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "Turn_yr",
            "gross_real", "pass4a", "pass4b", "fail4b"]

    for dial, values, ref in (("g", GROSSES, G_REF), ("band", BANDS, B_REF)):
        P("\n" + "#" * 100)
        P(f"# GRID {dial.upper()}  (tuned params: panel x {dial}; the other dial fixed at its "
          f"reference).  {len(panels)*len(values)*2*2} points.")
        P("#" * 100)
        grid, cache = leg_b(panels, dial, values, cache)
        grids.append(grid)

        P(f"\nALL {len(grid)} grid points for dial={dial} (every one reported):")
        P(fmt(grid[cols].set_index(["panel", "arm", "val", "bps"]), 3))

        car, ov = reversals(grid, ref)
        car["dial"], ov["dial"] = dial, dial
        cars.append(car)
        ovs.append(ov)

        P("\n" + "-" * 100)
        P(f"CARRIER reversal (EWall - TOP20 at fixed panel/{dial}/rung) - idea 259's unit, clean")
        P("-" * 100)
        P(fmt(car.set_index(["panel", "val", "bps"]).drop(columns=["dial"]), 3))
        c10 = car[car.bps == COST_BPS]
        P(f"\n@10 bps: {int(c10.rev.sum())}/{len(c10)} carrier pairs reverse full-sample, "
          f"{int(c10.rev_oos.sum())}/{len(c10)} OOS.  "
          f"EWall wins Sharpe in {int((c10.dS > 0).sum())}/{len(c10)}, "
          f"CAGR in {int((c10.dC > 0).sum())}/{len(c10)}.  "
          f"Conditional on EWall winning Sharpe it loses CAGR in "
          f"{int((c10.rev & (c10.dS > 0)).sum())}/{max(int((c10.dS > EPS_S).sum()), 1)}.")
        m, t, w = paired_t(c10.dS)
        P(f"  paired dSharpe mean {m:+.4f} t {t:+.2f} ({w}/{len(c10)} positive)")
        m, t, w = paired_t(c10.dC)
        P(f"  paired dCAGR   mean {m:+.4f} t {t:+.2f} ({w}/{len(c10)} positive)")

        P("\n" + "-" * 100)
        P(f"SENTENCE-SHAPED reversal: within-book dial delta d({dial}) = metric({dial}) "
          f"- metric({dial}={ref})")
        P("(this is the statistic the 11 parents' headlines actually assert)")
        P("-" * 100)
        P(fmt(ov.set_index(["panel", "arm", "bps", "val"]).drop(columns=["dial"]), 4))
        o10 = ov[ov.bps == COST_BPS]
        P(f"\n@10 bps: {int(o10.rev.sum())}/{len(o10)} dial deltas reverse between Sharpe and CAGR "
          f"({o10.rev.mean():.1%}) vs the carrier pair's {c10.rev.mean():.1%}.")
        P(f"  |dSharpe| <= eps ({EPS_S}) in {int(o10.dS_small.sum())}/{len(o10)} of them "
          f"(a dial with no Sharpe content cannot reverse by construction).")
        P(fmt(o10.groupby("arm")[["rev", "dS_small"]].agg(["size", "sum", "mean"]), 3))

        P("\n" + "-" * 100)
        P(f"RULE 8 walk-forward on the {dial} grid: IS 2009-2016 chooses, OOS 2017+ read once")
        P("-" * 100)
        wf = rule8(grid, cache, panels, ref)
        wf["dial"] = dial
        wfs.append(wf)
        P(fmt(wf.set_index(["panel", "bps", "selector"]).drop(columns=["dial"]), 3))
        w1 = wf[wf.bps == COST_BPS]
        P("\n@10 bps, OOS by selector:")
        P(fmt(w1.pivot_table(index="panel", columns="selector",
                             values=["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]), 3))
        a = w1[w1.selector == "S_CAGR"].set_index("panel")
        b = w1[w1.selector == "S_SHARPE"].set_index("panel")
        P(f"\nS_CAGR - S_SHARPE, OOS: dSharpe {(a.OOS_Sharpe - b.OOS_Sharpe).mean():+.4f} mean, "
          f"dCAGR {(a.OOS_CAGR - b.OOS_CAGR).mean():+.4f} mean; "
          f"same pick in {int((a.pick == b.pick).sum())}/{len(a)} panels.")

        P("\n" + "-" * 100)
        P(f"KEEP paths on every point of the {dial} grid (10 bps)")
        P("-" * 100)
        g10 = grid[grid.bps == COST_BPS]
        P(f"4a passes: {int(g10.pass4a.sum())}/{len(g10)}   "
          f"4b passes: {int(g10.pass4b.sum())}/{len(g10)}")
        P(fmt(g10.groupby(["panel", "arm"])[["pass4a", "pass4b"]].sum(), 0))
        P("\n4b failing bars, by point:")
        P(g10.groupby("fail4b").size().to_string())
        if g10.pass4b.any():
            P("\n4b PASSES:")
            P(fmt(g10[g10.pass4b][cols].set_index(["panel", "arm", "val"]), 3))

    G = pd.concat(grids, ignore_index=True)
    C = pd.concat(cars, ignore_index=True)
    V = pd.concat(ovs, ignore_index=True)
    W = pd.concat(wfs, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    C.to_csv(OUT / f"{STEM}.carrier.csv", index=False)
    V.to_csv(OUT / f"{STEM}.overlay.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    P("\n" + "=" * 100)
    P("POOLED over both grids, 10 bps")
    P("=" * 100)
    c10, o10 = C[C.bps == COST_BPS], V[V.bps == COST_BPS]
    P(f"  CARRIER (between-book EWall vs TOP20): {int(c10.rev.sum())}/{len(c10)} reverse "
      f"= {c10.rev.mean():.1%}")
    P(f"  DIAL    (within-book,  the sentence unit): {int(o10.rev.sum())}/{len(o10)} reverse "
      f"= {o10.rev.mean():.1%}   (|dSharpe|<=eps in {int(o10.dS_small.sum())}/{len(o10)})")
    P(fmt(V[V.bps == COST_BPS].groupby("dial")[["rev", "dS_small"]].agg(["size", "sum", "mean"]), 3))
    g10 = G[G.bps == COST_BPS]
    P(f"\n  4a passes {int(g10.pass4a.sum())}/{len(g10)}, "
      f"4b passes {int(g10.pass4b.sum())}/{len(g10)} over both grids.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
