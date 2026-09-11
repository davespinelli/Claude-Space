#!/usr/bin/env python3
"""Idea 738 — census the record's "PREDICTOR IS REAL" claims that were never scored
against the CONSTANT out of sample.

Idea 735 found, on ONE outcome (the de-grossing TIMING RESIDUAL) and ONE corpus (idea 538's
162 cells), that 13 of 15 IS-significant single-term predictors are OOS-DEAD against their own
family constant, and that IS R2 is UNINFORMATIVE about survival (the ladder's highest-R2 form,
DSH at R2 0.4212 / t 10.79, is 29% WORSE than the constant out of sample).  The queue asks the
obvious follow-up: the record quotes an in-sample t or R2 as evidence that a predictor is real
all over the place.  HOW MANY such claims are there, how many were EVER scored against a
constant out of sample, and what is the base rate at which such a claim survives that scoring?

Two legs, because neither alone answers it:

  LEG A  CENSUS (counting).  Harvest every IS-EVIDENCE SITE in the committed record — a
         quoted t-statistic, R2, OLS slope/beta, Spearman/rho or p-value — and classify each
         by what its own surrounding text does with it:
             SCORED_vs_CONSTANT  the claim carries BOTH an out-of-sample marker AND a
                                 constant/null comparand (the idea-735 standard)
             OOS_ONLY            an out-of-sample marker but no constant comparand
             IS_ONLY             neither: the t/R2 IS the evidence.  <- what 738 asks to count
         Corpora (P1 CLAIM SET): CHANGELOG (the committed headline record), LEADERBOARD,
         RESULTS (636 .result.md), MEMOS (22 *MEMO.md), ALL.  Window width is swept
         (SENTENCE / +-300 / +-600 chars) and every width published, because the classifier's
         only real dial is how much context counts as "the claim".

  LEG B  RE-SCORE (measurement).  The census cannot say whether an unscored claim WOULD have
         survived, so rebuild a corpus and actually score.  Idea 735 did this for one outcome;
         here the SAME 20 single-term predictors are scored against SEVEN cell-level OUTCOME
         FAMILIES the record makes claims about — RESID, GAP, PRED, CSD, TURN, SHARPE, CAGR,
         MAXDD — each against FOUR constants (P2 CONSTANT: ZERO / GLOBAL / FAMILY / PANEL),
         at two splits.  Every fit is on IS-window cell values ONLY and scored ONCE on the
         OOS-window truth.  That yields the base rate the census needs: of the forms an
         IS t would have certified, what share beat their own family constant out of sample?

  The two legs multiply: (record's IS_ONLY claim count) x (1 - survival rate) is the record's
  exposure, and it is reported as such.

METHOD (leg B population, identical to idea 735 / idea 538 so the gate is exact)
  162 cells / 324 books.  A cell is (panel, family, level, cadence) at gross 0.75; its two
  books are the RESPREAD and DEGROSS constructions of one gate mask.
      gap0 = 100*(CAGR(DEGROSS,0bps) - CAGR(RESPREAD,0bps))   pp/yr
      pred0 = 100*(CAGR(c_bar*RESPREAD) - CAGR(RESPREAD))     constant-leverage drag
      resid0 = gap0 - pred0                                   the TIMING of c_t
      c_t = held gross(DEGROSS) / held gross(RESPREAD)
  Panels U56 / B136 / SMALL439; families QUANTILE (9 levels) and MA-THRESH (9 thetas);
  cadences W/M/Q; 10 bps; next-day execution; 0-bps rung DERIVED as r0 = r10 + turn*bps/1e4.

  TUNED PARAMETERS (exactly 2, per the queue, every grid point reported, nothing selected
  outside rule 8):
      P1 CLAIM SET   5 values  CHANGELOG / LEADERBOARD / RESULTS / MEMOS / ALL
      P2 CONSTANT    4 values  ZERO / GLOBAL / FAMILY / PANEL
  FORM (23), OUTCOME FAMILY (8), SPLIT (2) and WINDOW WIDTH (3) are ENUMERATED EXHAUSTIVELY
  and published in full in the .ladder.csv / .census.csv — no cell is chosen, so none of them
  is a tuned dial; the headline is a rate over all of them, not a best cell.

  RULE 8 (required): WF-A picks each arm's (level, cadence) on IS Sharpe ALONE and reads 2017+
  ONCE against RULES v2 and SPY.  Both KEEP paths are evaluated on all 324 books.

SURVIVORSHIP: all three panels are CURRENT constituent lists (idea 54) — no delistings — so
every CAGR LEVEL is inflated and the 4a/4b columns inherit that in full.  Leg B's headline
object is a cross-cell fit on an arm-minus-arm contrast (both constructions share one gate
mask, names, days and gross), so the bias very largely cancels out of RESID/GAP/PRED; it does
NOT cancel out of CAGR, SHARPE, MAXDD or the KEEP columns, which are read as levels.
SMALL439 drops every ticker with max_1d_move >= 1.0 first.

Deterministic, standalone, no network.  Modifies nothing outside its own outputs.
"""
import sys, time, re, json, glob
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights        # noqa
from engine import backtest as engine_backtest, metrics, rebalance_mask  # noqa

OUT = Path(__file__).with_suffix("")
COST_BPS, GROSS = 10, 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
SPLITS = {"S2016": ("2016-12-31", "2017-01-01"), "S2018": ("2018-12-31", "2019-01-01")}
REF735 = REPO / "research" / "backtests" / ("2026-09-11_do-the-ARM-LEVEL-turnover-slopes-"
                                            "that-die-OOS-die-on-every-residual-family_cloud")
REF538 = REPO / "research" / "backtests" / "2026-09-11_is-c_sd-the-right-SCALE-or-is-it-a-TURNOVER-proxy_B"
# idea 735's committed RESID ladder at S2016 (its .ladder.csv), used as the G1 bar:
REF735_RESID_S2016 = {"CSD": 0.177296, "CT_RANGE": 0.176908, "FAMILY": 0.193700,
                      "ZERO": 0.264220, "GLOBAL": 0.246024, "DSH": 0.249912,
                      "RESID_IS": 0.208734, "TORS": 0.242709, "DTO": 0.240438}

GROUPS = {
    "CONSTANT": ["ZERO", "GLOBAL", "FAMILY", "PANEL"],
    "INCUMBENT": ["CSD"],
    "TURNOVER": ["TO", "TORS", "DTO", "LOGTO", "TORATIO"],
    "EXPOSURE": ["CBAR", "ABSCBAR", "CT_AC1", "CT_RANGE", "GSHARE"],
    "BOOK": ["ISSH_DG", "ISSH_RS", "DSH"],
    "DECOMP": ["GAP_IS", "PRED_IS", "RESID_IS"],
    "DESIGN": ["LEVEL", "CADRANK", "NNAMES"],
}
FORMS = [f for g in GROUPS.values() for f in g]
GROUP_OF = {f: g for g, fs in GROUPS.items() for f in fs}
CONSTANTS = GROUPS["CONSTANT"]

# outcome family -> (is column, oos column, the form that IS this outcome's own IS value)
OUTCOMES = {
    "RESID":  ("resid_is",       "resid_oos",       "RESID_IS"),
    "GAP":    ("gap_is",         "gap_oos",         "GAP_IS"),
    "PRED":   ("pred_is",        "pred_oos",        "PRED_IS"),
    "CSD":    ("c_sd_is",        "c_sd_oos",        "CSD"),
    "TURN":   ("tors_is",        "tors_oos",        "TORS"),
    "SHARPE": ("isSharpe_rs_is", "isSharpe_rs_oos", "ISSH_RS"),
    "CAGR":   ("cagr_rs_is",     "cagr_rs_oos",     None),
    "MAXDD":  ("mdd_rs_is",      "mdd_rs_oos",      None),
}

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

# ============================================================ LEG A: the census machinery
# An IS-EVIDENCE SITE is a place where the record quotes an in-sample fit statistic as
# evidence.  Patterns are deliberately literal — they match how this record actually writes.
IS_EVIDENCE = {
    "T_STAT":   r"(?:\|t\|\s*[<>=]{1,2}\s*[-+]?\d+(?:\.\d+)?|\bt[- ]?stat\w*|\bt\s*[=:]\s*[-+]?\d+\.\d+|\bt\s+[-+]?\d+\.\d{2,})",
    "R2":       r"(?:\bR2\b|\bR\^2\b|R²)",
    "SLOPE":    r"(?:\bslopes?\b|\bbeta(?:_\w+)?\b)",
    "CORR":     r"(?:\bSpearman\b|\brho\b|\bcorrelat\w+)",
    "PVALUE":   r"\bp\s*[<=]\s*0?\.\d+",
}
# markers that the claim was taken OUT OF SAMPLE at all
OOS_MARK = r"(?:\bOOS\b|out[- ]of[- ]sample|walk[- ]forward|\bWF-[A-Z]\b|rule 8|2017\+|held out|hold[- ]out)"
# markers that it was scored against a CONSTANT / null comparand
CONST_MARK = (r"(?:\bconstant\b|\bFAMILY\b|\bGLOBAL\b|\bnull\b|\bplacebo\b|\bbase rate\b|"
              r"\bcoin[- ]flip\b|\bpermut\w+|\bzero[- ]signal\b|\bMAE\b|\bshuffl\w+|\brandom\b|"
              r"\bintercept[- ]only\b|\bmean[- ]only\b|\bunconditional\b)")

def sentences(text):
    """Crude but deterministic sentence spans: split on '. ' / newline / ';' boundaries."""
    spans, start = [], 0
    for m in re.finditer(r"(?:\.\s|\n|;\s|\*\*\s)", text):
        spans.append((start, m.end())); start = m.end()
    spans.append((start, len(text)))
    return spans

def window_for(text, pos, mode, spans, starts):
    if mode == "SENTENCE":
        i = np.searchsorted(starts, pos, side="right") - 1
        i = max(i, 0)
        return text[spans[i][0]:spans[i][1]]
    w = int(mode)
    return text[max(0, pos - w): pos + w]

# A site is QUANTIFIED only if a DECIMAL number sits immediately beside the evidence token
# (35 chars after, or ending within 25 chars before) and the token is not part of a FILENAME.
# Without this, `.correlation.csv` (an artefact path) and "the unfolded-fit slope habit"
# (prose) count as published claims; with it, only places where the record actually PRINTS a
# fit statistic do.  Both the raw and the quantified counts are reported at every grid point.
DEC = r"[-+]?\d*\.\d+"
FILEISH = r"\.(?:csv|py|md|json|txt)\b"

def census_corpus(name, text, modes=("SENTENCE", "300", "600")):
    spans = sentences(text); starts = np.array([s for s, _ in spans])
    out = []
    for kind, pat in IS_EVIDENCE.items():
        for m in re.finditer(pat, text, flags=re.I):
            tail, head = text[m.end(): m.end() + 35], text[max(0, m.start() - 25): m.start()]
            isfile = bool(re.search(FILEISH, text[max(0, m.start() - 30): m.end() + 15]))
            quant = (bool(re.search(DEC, tail)) or bool(re.search(DEC + r"\s*$", head))) and not isfile
            # For a t-statistic site, recover the VALUE, so an affirmative claim (|t| >= 2)
            # can be separated from a NULL reading (|t| < 2).  A site is only a "predictor is
            # real" claim in the first case; the record quotes plenty of the second.
            tv = np.nan
            if kind == "T_STAT":
                mt = re.search(r"[-+]?\d+\.\d+", m.group(0)) or re.search(r"^\s*[-+]?\d+\.\d+", tail)
                if mt: tv = float(mt.group(0))
            rec = dict(corpus=name, kind=kind, pos=m.start(), hit=m.group(0)[:40],
                       quantified=bool(quant), tval=tv)
            for mode in modes:
                w = window_for(text, m.start(), mode, spans, starts)
                oos = bool(re.search(OOS_MARK, w, flags=re.I))
                con = bool(re.search(CONST_MARK, w, flags=re.I))
                rec[f"cls_{mode}"] = ("SCORED_vs_CONSTANT" if (oos and con)
                                      else "OOS_ONLY" if oos else
                                      "CONST_ONLY" if con else "IS_ONLY")
            rec["ctx"] = re.sub(r"\s+", " ", window_for(text, m.start(), "160", spans, starts))
            out.append(rec)
    return out

# ============================================================ LEG B: backtest machinery
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq="W"):
    """numpy re-implementation of engine.backtest; returns (returns, turnover, held gross)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); grs = np.empty(n); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        grs[i] = cur.sum(); pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = prices.index
    return (pd.Series(pr - turn * cost_bps / 1e4, index=idx),
            pd.Series(turn, index=idx), pd.Series(grs, index=idx))

def cagr(r):
    eq = (1 + r).cumprod(); return eq.iloc[-1] ** (252 / len(r)) - 1

def stat(r, is_end, oos_start):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:is_end]), metrics(r.loc[oos_start:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])

def live_mask(px): return px.notna() & px.shift(1).notna()

def gate_mask(px, family, level):
    live = live_mask(px); ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    kt = np.ceil(level * live.sum(axis=1)).astype(int).clip(lower=1)
    return dist.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live

def unit_book(px, g, construction):
    if construction == "RESPREAD":
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0)
    return g.astype(float).div(live_mask(px).sum(axis=1).clip(lower=1), axis=0)

def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b; n, k = X.shape
    s2 = r @ r / max(n - k, 1)
    se = np.sqrt(np.diag(s2 * np.linalg.pinv(X.T @ X)))
    tss = ((y - y.mean()) ** 2).sum()
    return b, se, np.where(se > 0, b / se, np.nan), 1 - (r @ r) / tss if tss > 0 else np.nan

def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56, px136 = load_universe(), load_universe(broad=True)
    P(f"panels: SMALL439 {len(inv)} names ({len(bad)} dropped for max_1d_move >= 1.0), "
      f"U56 {px56.shape[1]-1}, B136 {px136.shape[1]-1}")
    return {"SMALL439": (pxs[inv], pxs["SPY"]),
            "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
            "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"])}

t0 = time.time()
P("=" * 100)
P("IDEA 738 — census the record's 'PREDICTOR IS REAL' claims never scored against the CONSTANT")
P(f"10 bps, next-day execution, gross {GROSS}; 0-bps rung DERIVED (r0 = r10 + turn*bps/1e4).")
P("P1 CLAIM SET (5) x P2 CONSTANT (4) tuned; FORM (23) x OUTCOME (8) x SPLIT (2) x WINDOW (3)")
P("enumerated exhaustively and published whole.")
P("=" * 100)

# ================================================================== LEG A — CENSUS
P("\n" + "=" * 100); P("LEG A — CENSUS of IS-EVIDENCE SITES in the committed record")
P("=" * 100)
CORPORA = {}
CORPORA["CHANGELOG"] = (REPO / "research" / "CHANGELOG.md").read_text(errors="replace")
CORPORA["LEADERBOARD"] = (REPO / "research" / "LEADERBOARD.md").read_text(errors="replace")
res_files = sorted(glob.glob(str(REPO / "research" / "backtests" / "*.result.md")))
memo_files = sorted(glob.glob(str(REPO / "research" / "backtests" / "*MEMO.md")))
CORPORA["RESULTS"] = "\n".join(Path(f).read_text(errors="replace") for f in res_files)
CORPORA["MEMOS"] = "\n".join(Path(f).read_text(errors="replace") for f in memo_files)
P(f"corpora: CHANGELOG {len(CORPORA['CHANGELOG']):,} chars | LEADERBOARD "
  f"{len(CORPORA['LEADERBOARD']):,} | RESULTS {len(res_files)} files "
  f"{len(CORPORA['RESULTS']):,} | MEMOS {len(memo_files)} files {len(CORPORA['MEMOS']):,}")

sites = []
for nm, txt in CORPORA.items():
    s = census_corpus(nm, txt); sites += s
    nq = sum(1 for r in s if r["quantified"])
    P(f"  {nm:12s} {len(s):6d} IS-evidence sites ({nq} QUANTIFIED)")
CEN = pd.DataFrame(sites)
CEN.to_csv(f"{OUT}.census.csv", index=False)
P(f"  ALL          {len(CEN):6d} IS-evidence sites ({int(CEN.quantified.sum())} QUANTIFIED, "
  f"{CEN.quantified.mean():.1%}) — the QUANTIFIED set is the census population; the raw set is "
  f"reported beside it so the filter itself can be checked.")

CLS = ["SCORED_vs_CONSTANT", "OOS_ONLY", "CONST_ONLY", "IS_ONLY"]
def crosstab(df, rowcol, col):
    ct = pd.crosstab(df[rowcol], df[col])
    for c in CLS:
        if c not in ct.columns: ct[c] = 0
    ct = ct[CLS]; ct.loc["ALL"] = ct.sum(); ct["n"] = ct.sum(axis=1)
    ct["IS_ONLY_share"] = ct.IS_ONLY / ct.n
    ct["SCORED_share"] = ct.SCORED_vs_CONSTANT / ct.n
    return ct

Q = CEN[CEN.quantified]
P("\nP1 CLAIM SET x classification, at each window width (ALL grid points), QUANTIFIED sites:")
for mode in ("SENTENCE", "300", "600"):
    P(f"\n--- window = {mode} (quantified only, n = {len(Q)}) ---")
    P(crosstab(Q, "corpus", f"cls_{mode}").to_string(float_format=lambda x: f"{x:.4f}"))
P("\n--- window = SENTENCE, ALL sites including unquantified (n = %d), for comparison ---" % len(CEN))
P(crosstab(CEN, "corpus", "cls_SENTENCE").to_string(float_format=lambda x: f"{x:.4f}"))

P("\nBY EVIDENCE KIND (window = SENTENCE, corpus = ALL, QUANTIFIED):")
P(crosstab(Q, "kind", "cls_SENTENCE").to_string(float_format=lambda x: f"{x:.4f}"))

P("\nAFFIRMATIVE vs NULL among the t-statistic sites — an IS_ONLY site is only a 'predictor "
  "is real' claim when the t it quotes CLEARS the bar; the record quotes plenty that do not:")
TS = Q[(Q.kind == "T_STAT") & Q.tval.notna()].copy()
TS["affirmative"] = TS.tval.abs() >= 2.0
for mode in ("SENTENCE", "300", "600"):
    tt = pd.crosstab(TS.affirmative, TS[f"cls_{mode}"])
    for c in CLS:
        if c not in tt.columns: tt[c] = 0
    tt = tt[CLS]; tt["n"] = tt.sum(axis=1)
    P(f"\n--- window {mode}: {len(TS)} quantified T_STAT sites with a recoverable value "
      f"({int(TS.affirmative.sum())} affirmative |t|>=2, {int((~TS.affirmative).sum())} null |t|<2) ---")
    P(tt.to_string())
AFF_IS_ONLY = {m: int(((TS.affirmative) & (TS[f"cls_{m}"] == "IS_ONLY")).sum())
               for m in ("SENTENCE", "300", "600")}
P(f"\n  AFFIRMATIVE-AND-IS_ONLY t-sites (the narrowest honest reading of what 738 asks to "
  f"count): {AFF_IS_ONLY}")

P("\nAUDIT SAMPLE — 12 QUANTIFIED sites the classifier calls IS_ONLY at EVERY window width "
  "(deterministic: every 1/12th of the sorted strict index). Read these to check the label.")
strict = Q[(Q.cls_SENTENCE == "IS_ONLY") & (Q.cls_300 == "IS_ONLY") & (Q.cls_600 == "IS_ONLY")]
P(f"  strictly-IS_ONLY at all three widths: {len(strict)}/{len(Q)} quantified sites "
  f"({len(strict)/max(len(Q),1):.2%})")
if len(strict):
    step = max(len(strict) // 12, 1)
    for _, r in strict.iloc[::step].head(12).iterrows():
        P(f"   [{r.corpus}/{r.kind}] ...{r.ctx[:210]}...")

# ================================================================== LEG B — BUILD
P("\n" + "=" * 100); P("LEG B — rebuild idea 538's 162 cells / 324 books and re-score every form")
P("=" * 100)
rows, cells, wfa = [], [], []
PX = panels()
ie0, os0 = SPLITS["S2016"]
for pname, (px, spy_px) in PX.items():
    start = px.index[260]
    live_full, _, _ = fast_backtest(px.join(spy_px.rename("SPY")),
                                    rules_v2_weights(px.join(spy_px.rename("SPY"))), COST_BPS, "W")
    spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
    spy_s = stat(spy_r, ie0, os0); live_s = stat(live_full.loc[start:], ie0, os0)
    P(f"\nPANEL {pname}  eval from {start.date()}  SPY CAGR {spy_s['CAGR']:.4f} Sharpe "
      f"{spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} | OOS {spy_s['oCAGR']:.4f}/"
      f"{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.4f}")
    P(f"  RULES v2 (live, SAME-PANEL per PROTOCOL rule 3) CAGR {live_s['CAGR']:.4f} Sharpe "
      f"{live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} | OOS {live_s['oCAGR']:.4f}/"
      f"{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.4f}")
    for family in FAMILIES:
        for li, level in enumerate(QUANT_X if family == "QUANTILE" else MA_THETA):
            gm = gate_mask(px, family, level)
            gshare_full = (gm.sum(axis=1) / live_mask(px).sum(axis=1).clip(lower=1)).loc[start:]
            ub = {c: unit_book(px, gm, c) for c in CONSTRUCTIONS}
            for cad in CADENCES:
                got = {}
                for con in CONSTRUCTIONS:
                    r10, turn, grs = fast_backtest(px, ub[con] * GROSS, COST_BPS, cad)
                    r10, turn, grs = r10.loc[start:], turn.loc[start:], grs.loc[start:]
                    got[con] = dict(r0=r10 + turn * COST_BPS / 1e4, turn=turn, gross=grs, r10=r10)
                    s = stat(r10, ie0, os0)
                    rows.append(dict(panel=pname, family=family, level=level, cad=cad, con=con,
                                     **s, turn_yr=turn.sum() / (len(turn) / 252),
                                     p4a=bool(s["H1"] > live_s["H1"] and s["H2"] > live_s["H2"]
                                              and s["MaxDD"] >= live_s["MaxDD"]),
                                     p4b=bool(s["H1"] > spy_s["H1"] and s["H2"] > spy_s["H2"]
                                              and s["oSharpe"] > spy_s["oSharpe"]
                                              and abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"])
                                              and s["CAGR"] >= 0.70 * spy_s["CAGR"])))
                dg, rs = got["DEGROSS"], got["RESPREAD"]
                c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                for sp, (ie, os_) in SPLITS.items():
                    rec = dict(panel=pname, family=family, level=level, cad=cad, split=sp,
                               li=li, cadrank=CADENCES.index(cad) + 1, nnames=px.shape[1])
                    for tag, sl in (("is", slice(None, ie)), ("oos", slice(os_, None))):
                        rr, rd, ct = rs["r0"].loc[sl], dg["r0"].loc[sl], c_t.loc[sl]
                        cb = float(ct.mean())
                        g0 = 100 * (cagr(rd) - cagr(rr)); p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        yrs = len(rr) / 252
                        mrs = metrics(rs["r10"].loc[sl])
                        rec[f"resid_{tag}"] = g0 - p0; rec[f"gap_{tag}"] = g0
                        rec[f"pred_{tag}"] = p0; rec[f"c_bar_{tag}"] = cb
                        rec[f"c_sd_{tag}"] = float(ct.std())
                        rec[f"ct_ac1_{tag}"] = float(ct.autocorr(1)) if ct.std() > 0 else 0.0
                        rec[f"ct_range_{tag}"] = float(ct.max() - ct.min())
                        rec[f"to_{tag}"] = dg["turn"].loc[sl].sum() / yrs
                        rec[f"tors_{tag}"] = rs["turn"].loc[sl].sum() / yrs
                        rec[f"gshare_{tag}"] = float(gshare_full.loc[sl].mean())
                        rec[f"isSharpe_dg_{tag}"] = metrics(dg["r10"].loc[sl])["Sharpe"]
                        rec[f"isSharpe_rs_{tag}"] = mrs["Sharpe"]
                        rec[f"cagr_rs_{tag}"] = 100 * mrs["CAGR"]
                        rec[f"mdd_rs_{tag}"] = 100 * mrs["MaxDD"]
                    rec["oSharpe_dg"] = metrics(dg["r10"].loc[SPLITS[sp][1]:])["Sharpe"]
                    rec["oSharpe_rs"] = metrics(rs["r10"].loc[SPLITS[sp][1]:])["Sharpe"]
                    cells.append(rec)
    P(f"  ... {pname} done ({time.time()-t0:.0f}s)")

G = pd.DataFrame(rows); C0 = pd.DataFrame(cells)
C0["dto_is"] = C0.to_is - C0.tors_is; C0["dto_oos"] = C0.to_oos - C0.tors_oos
G.to_csv(f"{OUT}.grid.csv", index=False); C0.to_csv(f"{OUT}.cells.csv", index=False)

# ================================================================== G1 REPRODUCTION GATE
P("\n" + "=" * 100); P("G1 REPRODUCTION GATE vs ideas 538 and 735 (printed before any new fit is read)")
P("=" * 100)
key = ["panel", "family", "level", "cad"]
mine = C0[C0.split == "S2016"].set_index(key).sort_index()
gate_ok = True
for tag, refp, cols in (("538", REF538, [("c_sd_is", "c_sd_is"), ("c_bar_is", "c_bar_is"),
                                         ("resid_is", "resid_is"), ("resid_oos", "resid_oos"),
                                         ("to_is", "to_is"), ("tors_is", "tors_is"),
                                         ("oSharpe_dg", "oSharpe_dg")]),):
    ref = pd.read_csv(f"{refp}.cells.csv").set_index(key).sort_index()
    assert list(mine.index) == list(ref.index), f"cell alignment vs idea {tag}"
    for col, mycol in cols:
        d = float(np.abs(mine[mycol].values - ref[col].values).max())
        P(f"  idea {tag}: max |d {col:12s}| = {d:.3e}")
        if col in ("c_sd_is",) and d > 1e-6: gate_ok = False
        if col.startswith("resid") and d > 1e-2: gate_ok = False
P(f"  n cells {len(mine)} (538: 162);  n books {len(G)}")
assert gate_ok, "G1 FAIL on idea 538 cell reproduction"

# ================================================================== LEG B ladder
def xcol(form, d):
    m = {"CSD": d.c_sd_is, "TO": d.to_is, "TORS": d.tors_is, "DTO": d.dto_is,
         "LOGTO": np.log(d.to_is.clip(lower=1e-6)), "TORATIO": d.to_is / d.tors_is.clip(lower=1e-9),
         "CBAR": d.c_bar_is, "ABSCBAR": (1 - d.c_bar_is).abs(), "CT_AC1": d.ct_ac1_is,
         "CT_RANGE": d.ct_range_is, "GSHARE": d.gshare_is,
         "ISSH_DG": d.isSharpe_dg_is, "ISSH_RS": d.isSharpe_rs_is,
         "DSH": d.isSharpe_dg_is - d.isSharpe_rs_is,
         "GAP_IS": d.gap_is, "PRED_IS": d.pred_is, "RESID_IS": d.resid_is,
         "LEVEL": d.li.astype(float), "CADRANK": d.cadrank.astype(float),
         "NNAMES": np.log(d.nnames.astype(float))}
    return m[form].values.astype(float)

lad = []
for sp in SPLITS:
    d = C0[C0.split == sp].reset_index(drop=True)
    famdum = (d.family == "MA-THRESH").values
    for oname, (yc_is, yc_oos, ownform) in OUTCOMES.items():
        y_is, y_oos = d[yc_is].values.astype(float), d[yc_oos].values.astype(float)
        base = {"ZERO": np.zeros(len(d)),
                "GLOBAL": np.full(len(d), y_is.mean())}
        base["FAMILY"] = np.where(famdum, y_is[famdum].mean(), y_is[~famdum].mean())
        pm = {p: y_is[(d.panel == p).values].mean() for p in d.panel.unique()}
        base["PANEL"] = d.panel.map(pm).values.astype(float)
        for form in FORMS:
            if form in base:
                pred, t, r2, coef = base[form], np.nan, np.nan, np.nan
            else:
                x = xcol(form, d); X = np.column_stack([np.ones(len(d)), x])
                b, se, ts, r2 = ols(X, y_is)
                pred = X @ b; t, coef = ts[1], b[1]
            lad.append(dict(split=sp, outcome=oname, group=GROUP_OF[form], form=form,
                            n=len(d), coef=coef, tstat=t, IS_R2=r2,
                            IS_MAE=float(np.abs(pred - y_is).mean()),
                            OOS_MAE=float(np.abs(pred - y_oos).mean()),
                            degenerate=(form == ownform)))
L = pd.DataFrame(lad)
for (sp, on), g in L.groupby(["split", "outcome"]):
    for c in CONSTANTS:
        v = float(g[g.form == c].OOS_MAE.iloc[0])
        L.loc[(L.split == sp) & (L.outcome == on), f"MAE_{c}"] = v
for c in CONSTANTS:
    L[f"ratio_vs_{c}"] = L.OOS_MAE / L[f"MAE_{c}"]
L["IS_LIVE"] = L.tstat.abs() >= 2.0
L["OOS_LIVE_FAMILY"] = L.OOS_MAE <= L.MAE_FAMILY
L["OOS_LIVE_BEST"] = L.OOS_MAE <= L[[f"MAE_{c}" for c in CONSTANTS]].min(axis=1)
L["cellclass"] = np.where(L.form.isin(CONSTANTS), "constant",
                 np.where(L.IS_LIVE & L.OOS_LIVE_FAMILY, "IS-live / OOS-live",
                 np.where(L.IS_LIVE & ~L.OOS_LIVE_FAMILY, "IS-SIGNIFICANT / OOS-DEAD",
                 np.where(~L.IS_LIVE & L.OOS_LIVE_FAMILY, "IS-dead / OOS-live", "dead / dead"))))
L.to_csv(f"{OUT}.ladder.csv", index=False)

P("\nG1b — idea 735's committed RESID ladder at S2016 (its .ladder.csv numbers):")
r0 = L[(L.split == "S2016") & (L.outcome == "RESID")].set_index("form")
for f, ref in REF735_RESID_S2016.items():
    P(f"  {f:9s} OOS MAE mine {r0.loc[f,'OOS_MAE']:.6f} vs 735 {ref:.6f} "
      f"(d {abs(r0.loc[f,'OOS_MAE']-ref):.3e})")
assert all(abs(r0.loc[f, "OOS_MAE"] - v) < 1e-2 for f, v in REF735_RESID_S2016.items()), "G1b FAIL"
P("  G1b PASS (1e-2 pp allowance, idea 301's stated prices.csv daily-vintage tolerance)")

P("\n" + "=" * 100); P("ALL GRID POINTS — P2 CONSTANT x OUTCOME (survival of every form)")
P("=" * 100)
for c in CONSTANTS:
    nc = L[~L.form.isin(CONSTANTS)]
    tab = nc.groupby("outcome").apply(
        lambda g: pd.Series({"forms": len(g), "IS_live": int(g.IS_LIVE.sum()),
                             "OOS_beats_const": int((g.OOS_MAE <= g[f"MAE_{c}"]).sum()),
                             "IS_live_and_beats": int((g.IS_LIVE & (g.OOS_MAE <= g[f"MAE_{c}"])).sum()),
                             "median_ratio": g[f"ratio_vs_{c}"].median()}), include_groups=False)
    tab.loc["ALL"] = tab.sum(); tab.loc["ALL", "median_ratio"] = nc[f"ratio_vs_{c}"].median()
    tab["survival_of_IS_live"] = tab.IS_live_and_beats / tab.IS_live.replace(0, np.nan)
    P(f"\n--- P2 CONSTANT = {c} (both splits pooled, {len(nc)} non-constant form-cells) ---")
    P(tab.to_string(float_format=lambda x: f"{x:.4f}"))

P("\n" + "=" * 100); P("THE 2x2 per OUTCOME FAMILY (constant = FAMILY, both splits pooled)")
P("=" * 100)
nc = L[~L.form.isin(CONSTANTS)]
for on in OUTCOMES:
    s = nc[nc.outcome == on]
    isl = int(s.IS_LIVE.sum()); dead = int((s.IS_LIVE & ~s.OOS_LIVE_FAMILY).sum())
    alive = sorted(set(s[s.IS_LIVE & s.OOS_LIVE_FAMILY].form))
    P(f"  {on:7s} IS-significant {isl:3d}/{len(s):3d}  of those OOS-DEAD {dead:3d} "
      f"({dead/max(isl,1):.0%})  OOS-live at any t: {int(s.OOS_LIVE_FAMILY.sum()):3d} "
      f"-> IS-live survivors {alive}")
tot_is = int(nc.IS_LIVE.sum()); tot_dead = int((nc.IS_LIVE & ~nc.OOS_LIVE_FAMILY).sum())
SURV = 1 - tot_dead / max(tot_is, 1)
P(f"\n  POOLED over all 8 outcome families, 2 splits, 20 forms ({len(nc)} form-cells):")
P(f"  IS-significant {tot_is}/{len(nc)} ({tot_is/len(nc):.1%});  of those OOS-DEAD {tot_dead} "
  f"({tot_dead/max(tot_is,1):.1%});  SURVIVAL RATE {SURV:.1%}")

# A form that IS the outcome's own IS value (RESID_IS for RESID, TORS for TURN, ...) is a
# PERSISTENCE test, not a predictor discovery.  Both readings are published.
nd = nc[~nc.degenerate]
nd_is = int(nd.IS_LIVE.sum()); nd_dead = int((nd.IS_LIVE & ~nd.OOS_LIVE_FAMILY).sum())
SURV_ND = 1 - nd_dead / max(nd_is, 1)
P(f"  EXCLUDING the 6 degenerate own-value forms ({len(nd)} form-cells): IS-significant "
  f"{nd_is}/{len(nd)}; OOS-DEAD {nd_dead} ({nd_dead/max(nd_is,1):.1%}); SURVIVAL {SURV_ND:.1%}")

P("\n  DOES IS EVIDENCE PREDICT OOS SURVIVAL?  Spearman(statistic, ratio_vs_FAMILY) — negative")
P("  means MORE in-sample evidence goes with a BETTER out-of-sample score.  The POOLED number")
P("  mixes families whose ratio scales differ, so the WITHIN-OUTCOME rows are the honest read:")
def sp(d, a, b):
    return float(d[[a, b]].corr(method="spearman").iloc[0, 1]) if len(d) > 3 else np.nan
nd2 = nd.assign(abst=nd.tstat.abs())
P(f"    POOLED (all {len(nd2)} cells):  R2 {sp(nd2,'IS_R2','ratio_vs_FAMILY'):+.4f}   "
  f"|t| {sp(nd2,'abst','ratio_vs_FAMILY'):+.4f}")
wr = []
for on in OUTCOMES:
    s = nd2[nd2.outcome == on]
    wr.append(dict(outcome=on, n=len(s), rho_R2=sp(s, "IS_R2", "ratio_vs_FAMILY"),
                   rho_absT=sp(s, "abst", "ratio_vs_FAMILY")))
WR = pd.DataFrame(wr)
P(WR.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
P(f"    median WITHIN-outcome rho: R2 {WR.rho_R2.median():+.4f}, |t| {WR.rho_absT.median():+.4f}; "
  f"negative in {int((WR.rho_R2 < 0).sum())}/8 and {int((WR.rho_absT < 0).sum())}/8 families")

P("\n" + "=" * 100); P("THE TWO LEGS MULTIPLIED — the record's exposure")
P("=" * 100)
for mode in ("SENTENCE", "300", "600"):
    n_is_only = int((Q[f"cls_{mode}"] == "IS_ONLY").sum())
    P(f"  window {mode:8s}: {n_is_only:6d} QUANTIFIED IS_ONLY sites x measured OOS-death rate "
      f"{1-SURV:.1%} = {n_is_only*(1-SURV):8.0f} sites whose evidence would not survive "
      f"a constant-scoring, at this study's base rate")
P("  (an EXPECTED COUNT under the leg-B base rate, NOT a claim that these specific sites are")
P("   wrong: leg B measures ONE corpus of 162 cells and 20 forms, and a site is a text match,")
P("   not an adjudicated claim. The audit sample above is the honest check on the label.)")

# ================================================================== RULE 8
P("\n" + "=" * 100); P("RULE 8 — WF-A: each arm's (level, cadence) chosen on IS Sharpe ALONE, 2017+ read ONCE")
P("=" * 100)
for pname, (px, spy_px) in PX.items():
    start = px.index[260]
    lf, _, _ = fast_backtest(px.join(spy_px.rename("SPY")),
                             rules_v2_weights(px.join(spy_px.rename("SPY"))), COST_BPS, "W")
    live_s = stat(lf.loc[start:], ie0, os0)
    spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:], ie0, os0)
    for family in FAMILIES:
        for con in CONSTRUCTIONS:
            arm = G[(G.panel == pname) & (G.family == family) & (G.con == con)]
            pick = arm.loc[arm.isSharpe.idxmax()]
            wfa.append(dict(panel=pname, family=family, con=con,
                            pick=f"level={pick.level} cad={pick.cad}", IS_Sharpe=pick.isSharpe,
                            OOS_CAGR=pick.oCAGR, OOS_Sharpe=pick.oSharpe, OOS_MaxDD=pick.oMaxDD,
                            v2_OOS_Sharpe=live_s["oSharpe"], SPY_OOS_CAGR=spy_s["oCAGR"],
                            SPY_OOS_Sharpe=spy_s["oSharpe"], SPY_OOS_MaxDD=spy_s["oMaxDD"],
                            beats_v2=pick.oSharpe > live_s["oSharpe"],
                            beats_SPY=pick.oSharpe > spy_s["oSharpe"],
                            p4a=bool(pick.p4a), p4b=bool(pick.p4b)))
W = pd.DataFrame(wfa); W.to_csv(f"{OUT}.walkforward.csv", index=False)
P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
P(f"\nWF-A: beats RULES v2 OOS Sharpe {int(W.beats_v2.sum())}/{len(W)}; beats SPY OOS Sharpe "
  f"{int(W.beats_SPY.sum())}/{len(W)}; 4a {int(W.p4a.sum())}/{len(W)}; 4b {int(W.p4b.sum())}/{len(W)}")

P("\n" + "=" * 100); P("BOTH KEEP PATHS on all 324 books")
P("=" * 100)
P(f"  4a (SAME-PANEL RULES v2 comparand, PROTOCOL rule 3): {int(G.p4a.sum())}/{len(G)}")
P(f"  4b (vs SPY, both halves + OOS + DD cap + CAGR floor): {int(G.p4b.sum())}/{len(G)}")
P(G.groupby(["panel", "con"]).agg(n=("p4a", "size"), p4a=("p4a", "sum"),
                                  p4b=("p4b", "sum")).to_string())

summary = dict(idea=738, lane="C", date="2026-09-11",
               census_sites=int(len(CEN)), census_quantified=int(len(Q)),
               census_IS_ONLY={m: int((Q[f"cls_{m}"] == "IS_ONLY").sum())
                               for m in ("SENTENCE", "300", "600")},
               census_SCORED={m: int((Q[f"cls_{m}"] == "SCORED_vs_CONSTANT").sum())
                              for m in ("SENTENCE", "300", "600")},
               strict_IS_ONLY=int(len(strict)), affirmative_IS_ONLY=AFF_IS_ONLY,
               ladder_cells=int(len(L)), nonconstant=int(len(nc)),
               IS_significant=tot_is, IS_sig_OOS_dead=tot_dead, survival_rate=float(SURV),
               survival_rate_nondegenerate=float(SURV_ND),
               rho_R2_pooled=sp(nd2, "IS_R2", "ratio_vs_FAMILY"),
               rho_R2_within_median=float(WR.rho_R2.median()),
               survival_by_outcome={on: float(1 - (nd2[(nd2.outcome == on) & nd2.IS_LIVE
                                                       & ~nd2.OOS_LIVE_FAMILY].shape[0]
                                                  / max(int(nd2[(nd2.outcome == on)].IS_LIVE.sum()), 1)))
                                    for on in OUTCOMES},
               p4a=int(G.p4a.sum()), p4b=int(G.p4b.sum()), n_books=int(len(G)),
               wfa_beats_v2=int(W.beats_v2.sum()), wfa_beats_SPY=int(W.beats_SPY.sum()),
               wfa_4a=int(W.p4a.sum()), wfa_4b=int(W.p4b.sum()), wfa_n=int(len(W)))
Path(f"{OUT}.summary.json").write_text(json.dumps(summary, indent=2))
P(f"\nwrote {OUT.name}.census.csv .grid.csv .cells.csv .ladder.csv .walkforward.csv "
  f".summary.json  ({time.time()-t0:.0f}s)")
Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
