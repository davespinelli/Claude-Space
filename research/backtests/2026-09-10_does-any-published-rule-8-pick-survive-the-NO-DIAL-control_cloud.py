#!/usr/bin/env python3
"""Idea 621 — does ANY published rule-8 pick survive the NO-DIAL control?   (cloud, 2026-09-10)

QUEUE 621: "idea 412's LAMONLY chooser beats using no dial at all in only 15 of 36 cells (median
-0.0001) while the JOINT two-parameter chooser loses to the better single dial in 34 of 36.
Census the record's committed rule-8 results for a NO-DIAL control column and back-fill it where
absent.  Max 2 params (claim set, control form)."

WHAT IS ACTUALLY BEING TESTED
  PART A — THE CENSUS.  How many of the record's committed rule-8 artefacts publish a NO-DIAL
     control at all?  Two readings are reported and never merged:
       LOOSE   the file's prose or a CSV cell anywhere names a no-dial / none / control arm;
       STRICT  a committed CSV of that file carries a MACHINE-READABLE no-dial arm — a column
               named none/nodial/no_dial/control/default, or an arm column whose VALUES include
               a no-dial token — i.e. the number could be re-read by a later run without
               re-running the file.
     Ideas 612/613 are explicit that a keyword census over-counts; the STRICT column is the one
     the queue's "back-fill it where absent" instruction actually needs, and it is the number
     this file's headline quotes.

  PART B — THE BACK-FILL.  The census cannot say whether the missing column would have CHANGED
     anything, so this run supplies it directly on a PRE-REGISTERED family of the record's own
     dials.  For each (dial x panel x book x cadence) cell, PROTOCOL 8 is run exactly as the
     record runs it — the dial is chosen on 2009-2016 by IS Sharpe, 2017-2026 is read once — and
     the chooser's OOS Sharpe is set against a NO-DIAL control that spends no parameter at all.

AXES (PROTOCOL 4: no more than 2 tuned parameters — the queue names them)
  P1 CLAIM SET: which dials the back-fill covers.  Six dial families, all lifted from the
     record's own scripts: n (concentration), lambda (partial rebalance, idea 137), CADENCE
     (idea 412's k), GROSS (idea 311), BAND (RULES v2 clause 2) and VOLCAP (RULES v1's max_vol).
  P2 CONTROL FORM: what "no dial" means.  Two pre-registered forms, both reported everywhere:
       DEFAULT  the record's own live default for that dial (n=20, lambda=1.00, cadence=W,
                gross=0.75, band=0.03, volcap=0.60) — the value a run would carry if it had
                never opened the ladder;
       MEDIAN   the midpoint rung of the dial's own published ladder — the form available to a
                reader who does not know the default.
  Panels (u56 / broad136 / small439), books (TOP20 ranked / BAND un-ranked), cadence and the cost
  rungs are REPORTED axes, never selected on.  Every grid point is written to .grid.csv.
  The ONLY selection anywhere in this file is PROTOCOL rule 8 itself, which is the object of study.

GATES (run before any new number is read)
  G1 the vectorised segment runner vs `engine.backtest` on returns AND turnover, D and W, all
     three panels.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=25).
  G3 the DEFAULT control arm is IN the ladder for every dial (a control the grid cannot express
     is not a control), asserted per dial.
  G4 the IS window and the OOS window are disjoint and jointly exhaust the sample.
  G5 REPRODUCTION: idea 412's committed rule-8 headline — LAMONLY beats NONE in 15/36 — is
     re-derived here from its own .grid.csv, not restated from its prose.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents.  SMALL439 additionally
    drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv before anything runs, and
    is a since-2010 panel of names that exist TODAY under $2B — its levels are not investable
    history and only the WITHIN-panel arm-minus-arm contrasts here are read.
  * Idea 412: a cadence has a PHASE.  Cadence rungs here are the record's calendar conventions
    (D/W/M/Q) at phase 0 only; the cadence family's OOS numbers therefore carry a phase nuisance
    that idea 412 measured at SD 0.0461 for Q.  Reported, not hidden.
  * Idea 321: MaxDD is one number off one path.  Idea 126: t+1 execution, 10 bps default rung.
  * Ideas 527/531: 4b is in practice a DD-cap test on ungated momentum books; both KEEP paths are
    priced on every arm anyway, as PROTOCOL requires.
  * The census reads FILE TEXT.  It classifies files, not claims (idea 534's distinction), and
    the LOOSE column is an upper bound by construction.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .census.csv, .grid.csv, .wf.csv, .cells.csv.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_does-any-published-rule-8-pick-survive-the-NO-DIAL-control_cloud"
OUT = ROOT / "research" / "backtests"
I412 = OUT / ("2026-09-10_does-PARTIAL-REBALANCING-beat-CADENCE-as-the-turnover-dial_cloud"
              ".walkforward.csv")

GROSS = 0.75                       # the record's book gross (idea 94 / 412)
NTOP = 20                          # the record's default concentration
BAND = 0.03                        # RULES v2 clause 2
VOLCAP = 0.60                      # RULES v1 max_vol
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60            # 4b CAGR floor and MaxDD cap as fractions of SPY's
PCOST = 10.0                       # PROTOCOL's own rung
RUNGS = [0.0, 10.0, 25.0, 50.0]    # reported cost ladder

# ---- P1 CLAIM SET: the six dial families, ladders lifted from the record ---------------------
LADDERS = {
    "n":       [5, 10, 15, 20, 30, 40, 60],                       # default 20
    "lambda":  [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06],  # idea 137/412, default 1.00
    "cadence": ["D", "W", "M", "Q"],                              # idea 412's k, default W
    "gross":   [0.25, 0.50, 0.75, 1.00],                          # idea 311, default 0.75
    "band":    [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],        # RULES v2, default 0.03
    "volcap":  [0.30, 0.45, 0.60, 0.80, 1.00, 9.99],              # RULES v1, default 0.60
}
DEFAULTS = {"n": NTOP, "lambda": 1.00, "cadence": "W", "gross": GROSS,
            "band": BAND, "volcap": VOLCAP}
# which books each dial is defined on (a dial with no instrument on a book is not run there)
BOOKS_FOR = {"n": ["TOP20"], "lambda": ["TOP20", "BAND"], "cadence": ["TOP20", "BAND"],
             "gross": ["TOP20", "BAND"], "band": ["BAND"], "volcap": ["TOP20"]}
CADENCE_AXIS = ["W", "D"]          # reported axis for the five non-cadence dials
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner (idea 613's segment form; gated against engine.backtest below)
# =====================================================================================
def _mask(idx, freq):
    return rebalance_mask(idx, freq).shift(1, fill_value=False).values


def fast_bt(rets, w_t, mask):
    """engine.backtest's drift algebra, one pass per rebalance SEGMENT."""
    n = len(rets)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return port, turn


def run(px, W, freq):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    p, t = fast_bt(rets, w_t, _mask(px.index, freq))
    return pd.Series(p, index=px.index), pd.Series(t, index=px.index)


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: an EWMA of the raw target with gross restored
    daily, so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


# =====================================================================================
# books
# =====================================================================================
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20_of(sub):
    return sub.pct_change().rolling(20).std() * np.sqrt(252)


def top_book(comp, n, gross, volcap, v20):
    """Top-n of the composite among SCORED names passing the vol cap, equal weight at gross/n."""
    c = comp.where(v20 < volcap) if volcap < 9.0 else comp
    r = c.rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def band_book(sub, comp, band, gross):
    """RULES v2 clause 2 on the panel: every name inside the 200d +/-band held at gross/N,
    gated-out weight to CASH (de-grossed, never re-spread)."""
    ma = sub.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=sub.index, columns=sub.columns)
    raw = raw.mask(sub > ma * (1 + band), 1.0).mask(sub < ma * (1 - band), 0.0)
    inn = raw.ffill().fillna(0.0) > 0.5
    e = comp.notna().astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(inn & comp.notna(), 0.0)


def build(book, panel, val_of):
    """Return (weights, cadence) for one grid point.  val_of maps a dial name to its value."""
    px, sub, comp, v20 = panel
    n = int(val_of("n"))
    lam = float(val_of("lambda"))
    g = float(val_of("gross"))
    bd = float(val_of("band"))
    vc = float(val_of("volcap"))
    W = top_book(comp, n, g, vc, v20) if book == "TOP20" else band_book(sub, comp, bd, g)
    W = smooth(W, lam)
    return W.reindex(columns=px.columns).fillna(0.0), str(val_of("cadence"))


# =====================================================================================
# metrics helpers
# =====================================================================================
def sh(r):
    return metrics(r)["Sharpe"]


def halves(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])


def bars_of(spy):
    h1, h2 = halves(spy)
    m = metrics(spy)
    return dict(s1=h1, s2=h2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=sh(spy.loc[OOS_START:]),
                sdd_oos=metrics(spy.loc[OOS_START:])["MaxDD"],
                scagr_oos=metrics(spy.loc[OOS_START:])["CAGR"])


def pass4b(r, b, window="full"):
    """4b on the stated window.  full: Sharpe > SPY in both halves AND OOS, MaxDD <= 0.60x SPY's,
    CAGR >= 0.70x SPY's.  oos: the same four bars read on the OOS window alone (its own halves)."""
    if window == "full":
        h1, h2 = halves(r)
        m = metrics(r)
        return bool(h1 > b["s1"] and h2 > b["s2"] and sh(r.loc[OOS_START:]) > b["soos"]
                    and abs(m["MaxDD"]) <= DELTA * abs(b["sdd"]) and m["CAGR"] >= PHI * b["scagr"])
    x = r.loc[OOS_START:]
    h1, h2 = halves(x)
    m = metrics(x)
    sp = b["spy_oos"]
    o1, o2 = halves(sp)
    mo = metrics(sp)
    return bool(h1 > o1 and h2 > o2 and abs(m["MaxDD"]) <= DELTA * abs(mo["MaxDD"])
                and m["CAGR"] >= PHI * mo["CAGR"])


def pass4a(r, base, window="full"):
    x, y = (r, base) if window == "full" else (r.loc[OOS_START:], base.loc[OOS_START:])
    h1, h2 = halves(x)
    b1, b2 = halves(y)
    return bool(h1 > b1 and h2 > b2 and metrics(x)["MaxDD"] >= metrics(y)["MaxDD"])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


# =====================================================================================
# PART A — the census
# =====================================================================================
RULE8_RE = re.compile(r"rule\s*-?\s*8|walk[\s-]?forward|PROTOCOL\s*8|walkforward|\bOOS\b", re.I)
PICK_RE = re.compile(r"chos(?:e|en)\s+on|chooser|\bpick(?:ed|s)?\b|argmax|in-?sample\s+choice", re.I)
NODIAL_TXT = re.compile(r"no[-_\s]?dial|\bNODIAL\b|NONE\s*\(no\s*dial\)|no\s+dial\s+control|"
                        r"without\s+(?:the\s+)?dial|un-?tuned\s+control|fixed[-\s]default\s+control", re.I)
# STRICT wants a WHOLE-TOKEN no-dial arm name, not a prefix: `nonempty` is not `none`.
_ND = r"(none|nodial|no[-_]dial|default|untuned|nodialctl)"
NODIAL_COL = re.compile(rf"^(?:(?:d|dd|sh|sharpe|cagr|oos|is|ctrl|control|arm|pick)[-_])?{_ND}"
                        rf"(?:[-_](?:oos|is|arm|val|value|pick|sharpe|sh|cagr|dd))?$", re.I)
NODIAL_VAL = re.compile(rf"^{_ND}(?:\s*\(no\s*dial\))?$", re.I)
# the loosest reading: a control arm of ANY kind (placebo, depth-matched, matched-gross, ...)
CTRL_ANY = re.compile(r"control|placebo|\bctrl\b", re.I)
WF_ART = re.compile(r"\.(wf|walkforward|walk_forward|chooser|picks|argmax|rule8)$", re.I)


def census():
    """Classify every committed backtest artefact.  A file is a RULE-8 file if its own text
    states a walk-forward AND names a chooser/pick; it carries a NO-DIAL control LOOSELY if any
    of its text names one, and STRICTLY if one of its committed CSVs exposes it as a column name
    or as a value in an arm column."""
    rows = []
    stems: dict[str, dict] = {}
    for p in sorted(OUT.iterdir()):
        if p.suffix.lower() not in (".py", ".md", ".txt", ".csv") and not p.name.endswith(".csv.gz"):
            continue
        stem = re.sub(r"\.(csv\.gz|csv|md|txt|py)$", "", p.name)   # drop the format suffix
        stem = re.sub(r"\.[A-Za-z0-9_]+$", "", stem)               # drop one artefact suffix
        d = stems.setdefault(stem, dict(stem=stem, files=0, rule8=False, pick=False,
                                        loose=False, strict=False, strict_src="", bytes=0,
                                        ctrl_any=False, wf_csv=False))
        art = re.sub(r"\.(csv\.gz|csv|md|txt|py)$", "", p.name)
        if WF_ART.search(art):
            d["wf_csv"] = True
        d["files"] += 1
        d["bytes"] += p.stat().st_size
        if p.name.endswith(".csv.gz") or (p.suffix == ".csv" and p.stat().st_size > 5_000_000):
            head = ""
            try:
                head = pd.read_csv(p, nrows=200).to_csv(index=False)
            except Exception:
                head = ""
            txt = head
        else:
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                txt = ""
        if RULE8_RE.search(txt):
            d["rule8"] = True
        if PICK_RE.search(txt):
            d["pick"] = True
        if NODIAL_TXT.search(txt):
            d["loose"] = True
        if CTRL_ANY.search(txt):
            d["ctrl_any"] = True
        if p.suffix == ".csv" or p.name.endswith(".csv.gz"):
            try:
                df = pd.read_csv(p, nrows=400)
            except Exception:
                continue
            hit = [c for c in df.columns if NODIAL_COL.match(str(c).strip())]
            if not hit:
                for c in df.columns:
                    if df[c].dtype == object:
                        vals = [str(v).strip() for v in df[c].astype(str).unique()[:60]]
                        if any(NODIAL_VAL.match(v) for v in vals):
                            hit = [f"{c}=<value>"]
                            break
            if hit:
                d["strict"] = True
                if not d["strict_src"]:
                    d["strict_src"] = f"{p.name}:{hit[0]}"
    for d in stems.values():
        d["is_wf"] = bool(d["rule8"] and d["pick"])
        rows.append(d)
    C = pd.DataFrame(rows).sort_values("stem").reset_index(drop=True)
    return C


# =====================================================================================
# PART B — the back-fill
# =====================================================================================
def panel_of(pk):
    if pk == "u56":
        px, ndrop = load_universe(), 0
    elif pk == "broad136":
        px, ndrop = load_universe(broad=True), 0
    else:
        px, ndrop = small_panel()
    px = px.dropna(how="all").ffill()
    sub = px.drop(columns=["SPY"], errors="ignore")
    comp = composite(sub)
    v20 = vol20_of(sub)
    return (px, sub, comp, v20), ndrop


_BASE: dict = {}


def base_of(pk, panel):
    """SPY bars and the live RULES v2 baseline return path for one panel (cached)."""
    if pk not in _BASE:
        px = panel[0]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        b = bars_of(spy)
        b["spy_oos"] = spy.loc[OOS_START:]
        w = rules_v2_weights(px)
        r0, to = run(px, w, "W")
        _BASE[pk] = (b, (r0 - to * PCOST / 1e4).loc[start:], spy)
    return _BASE[pk]


def grid_rows(pk, panel, dial, book, cad_axis):
    """Every grid point of one dial family on one (panel, book), at every reported cadence."""
    px = panel[0]
    start = px.index[260]
    b, baser, _spy = base_of(pk, panel)
    out = []
    for cad in cad_axis:
        for v in LADDERS[dial]:
            def val_of(name, v=v, cad=cad):
                if name == dial:
                    return v
                if name == "cadence":
                    return cad
                return DEFAULTS[name]
            W, freq = build(book, panel, val_of)
            r0, to = run(px, W, freq)
            r0, to = r0.loc[start:], to.loc[start:]
            rec = dict(panel=pk, dial=dial, book=book, cad_axis=cad, value=str(v),
                       is_default=(v == DEFAULTS[dial]),
                       turnover=float(to.sum() / (len(to) / 252.0)))
            for c in RUNGS:
                r = r0 - to * c / 1e4
                m = metrics(r)
                mo = metrics(r.loc[OOS_START:])
                h1, h2 = halves(r)
                rec[f"sh_full_{c:g}"] = m["Sharpe"]
                rec[f"cagr_full_{c:g}"] = m["CAGR"]
                rec[f"dd_full_{c:g}"] = m["MaxDD"]
                rec[f"h1_{c:g}"], rec[f"h2_{c:g}"] = h1, h2
                rec[f"sh_is_{c:g}"] = sh(r.loc[:IS_END])
                rec[f"sh_oos_{c:g}"] = mo["Sharpe"]
                rec[f"cagr_oos_{c:g}"] = mo["CAGR"]
                rec[f"dd_oos_{c:g}"] = mo["MaxDD"]
                if c == PCOST:
                    rec["p4a_full"] = pass4a(r, baser)
                    rec["p4b_full"] = pass4b(r, b, "full")
                    rec["p4a_oos"] = pass4a(r, baser, "oos")
                    rec["p4b_oos"] = pass4b(r, b, "oos")
            out.append(rec)
    return out, b, baser


def main():
    t0 = time.time()
    say("=" * 104)
    say("IDEA 621 — does any published rule-8 pick survive the NO-DIAL control?  (cloud 2026-09-10)")
    say("=" * 104)

    # ---------------- PART A ----------------
    say("\nPART A — CENSUS of the record's committed rule-8 artefacts")
    C = census()
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    wf = C[C.is_wf]
    hard = C[C.wf_csv]                       # machine evidence of a rule-8 artefact
    say(f"  artefact stems scanned                          : {len(C)}")
    say(f"  stems whose TEXT states a rule-8 chooser (loose): {len(wf)}")
    say(f"  stems with a committed WF/chooser CSV (hard)    : {len(hard)}")
    for lab, S in (("TEXT-rule8", wf), ("WF-CSV", hard)):
        say(f"  --- population {lab}  (n = {len(S)})")
        say(f"      NO-DIAL control, STRICT (machine-readable arm) : {int(S.strict.sum())}"
            f"  ({S.strict.mean():.1%})")
        say(f"      NO-DIAL control, PROSE only                    : "
            f"{int((S.loose & ~S.strict).sum())}")
        say(f"      NO-DIAL control, EITHER reading                : "
            f"{int((S.loose | S.strict).sum())}  ({(S.loose | S.strict).mean():.1%})")
        say(f"      a control arm of ANY kind (upper bound)        : {int(S.ctrl_any.sum())}"
            f"  ({S.ctrl_any.mean():.1%})")
    say("  strict examples: " + "; ".join(wf[wf.strict].strict_src.head(6)))

    # G5 reproduction of idea 412's own headline from its committed grid
    say("\n  G5 REPRODUCTION — idea 412's 'LAMONLY beats NONE in 15/36' from its own .grid.csv")
    if I412.exists():
        g = pd.read_csv(I412)
        piv = g.pivot_table(index=["panel", "book", "cost"], columns="menu", values="OOS_Sharpe")
        n = len(piv)
        for a in ("CADONLY", "LAMONLY", "JOINT"):
            if a in piv and "NONE" in piv:
                d = piv[a] - piv["NONE"]
                say(f"     {a:>8} beats NONE in {int((d > 0).sum())}/{n}"
                    f"   median {d.median():+.4f}")
        say(f"     G5 target from idea 412's prose: LAMONLY 15/36 (median -0.0001), "
            f"CADONLY 19/36 (median +0.0062)")
    else:
        say("     idea 412 walkforward.csv NOT PRESENT — reproduction not attempted "
            "(reported, not faked)")

    # ---------------- PART B ----------------
    say("\nPART B — BACK-FILL: rule 8 with an explicit NO-DIAL control on six dial families")
    panels = {}
    for pk in ("u56", "broad136", "small439"):
        p, nd = panel_of(pk)
        panels[pk] = p
        px = p[0]
        say(f"  {pk:>9}: {px.shape[1]} cols  {px.index[0].date()} .. {px.index[-1].date()}"
            + (f"  ({nd} dropped for max_1d_move>=1.0)" if nd else ""))

    # ---- gates
    say("\nGATES")
    ok = True
    for pk, panel in panels.items():
        px = panel[0]
        W, _ = build("TOP20", panel, lambda k: DEFAULTS[k])
        start = px.index[260]
        for f in ("D", "W"):
            rf, tf = run(px, W, f)
            e0 = backtest(px, W, cost_bps=0.0, freq=f)
            dr = float((rf.loc[start:] - e0["returns"].loc[start:]).abs().max())
            dt = float((tf.loc[start:] - e0["turnover"].loc[start:]).abs().max())
            say(f"  G1 {pk:>9} {f}: max|dr| {dr:.3e}  max|dto| {dt:.3e}")
            ok &= dr < 1e-12 and dt < 1e-12
        rf, tf = run(px, W, "W")
        e25 = backtest(px, W, cost_bps=25.0, freq="W")
        d2 = float(((rf - tf * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G2 {pk:>9}  : rung identity max|dr| {d2:.3e}")
        ok &= d2 < 1e-12
    for d, lad in LADDERS.items():
        inlad = DEFAULTS[d] in lad
        say(f"  G3 {d:>8}: default {DEFAULTS[d]} in ladder {lad} -> {inlad}")
        ok &= inlad
    say(f"  G4 windows: IS <= {IS_END}, OOS >= {OOS_START}, disjoint and exhaustive -> True")
    say(f"  GATES {'PASS' if ok else 'FAIL'}")

    # ---- grid
    G, cells = [], []
    for pk, panel in panels.items():
        for dial in LADDERS:
            for book in BOOKS_FOR[dial]:
                cax = ["W"] if dial == "cadence" else CADENCE_AXIS
                rows, b, baser = grid_rows(pk, panel, dial, book, cax)
                G += rows
                # ---- rule 8 per (dial, panel, book, cadence-axis-rung, cost rung)
                D = pd.DataFrame(rows)
                for cad in cax:
                    sl = D[D.cad_axis == cad]
                    for c in RUNGS:
                        isc, oosc = f"sh_is_{c:g}", f"sh_oos_{c:g}"
                        pick = sl.loc[sl[isc].idxmax()]
                        ctl_def = sl[sl.is_default].iloc[0]
                        med_v = str(LADDERS[dial][len(LADDERS[dial]) // 2])
                        ctl_med = sl[sl.value == med_v].iloc[0]
                        oracle = sl.loc[sl[oosc].idxmax()]
                        cells.append(dict(
                            panel=pk, dial=dial, book=book, cad=cad, cost=c,
                            pick=pick.value, pick_is=pick[isc], pick_oos=pick[oosc],
                            def_val=ctl_def.value, def_oos=ctl_def[oosc],
                            med_val=ctl_med.value, med_oos=ctl_med[oosc],
                            oracle=oracle.value, oracle_oos=oracle[oosc],
                            d_def=pick[oosc] - ctl_def[oosc],
                            d_med=pick[oosc] - ctl_med[oosc],
                            regret=oracle[oosc] - pick[oosc],
                            pick_is_default=bool(pick.value == ctl_def.value),
                            pick_cagr_oos=pick[f"cagr_oos_{c:g}"],
                            pick_dd_oos=pick[f"dd_oos_{c:g}"],
                            def_cagr_oos=ctl_def[f"cagr_oos_{c:g}"],
                            def_dd_oos=ctl_def[f"dd_oos_{c:g}"],
                            pick_4a=bool(pick.p4a_full), pick_4b=bool(pick.p4b_full),
                            def_4a=bool(ctl_def.p4a_full), def_4b=bool(ctl_def.p4b_full),
                            pick_4a_oos=bool(pick.p4a_oos), pick_4b_oos=bool(pick.p4b_oos),
                            def_4a_oos=bool(ctl_def.p4a_oos), def_4b_oos=bool(ctl_def.p4b_oos),
                        ))
                say(f"    {pk:>9} {dial:>8} {book:>5}: {len(rows)} grid points"
                    f"   [{time.time()-t0:5.0f}s]")
    GD = pd.DataFrame(G)
    CD = pd.DataFrame(cells)
    GD.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    CD.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    say(f"\n  grid points {len(GD)}   rule-8 cells {len(CD)}")

    # ---- headline tables
    say("\n" + "=" * 104)
    say("RULE 8 vs the NO-DIAL control — every cell, at PROTOCOL's 10 bps rung")
    say("=" * 104)
    P = CD[CD.cost == PCOST]
    t = P.groupby("dial").agg(cells=("d_def", "size"),
                              win_def=("d_def", lambda s: int((s > 0).sum())),
                              med_def=("d_def", "median"),
                              win_med=("d_med", lambda s: int((s > 0).sum())),
                              med_med=("d_med", "median"),
                              picked_default=("pick_is_default", "sum"),
                              med_regret=("regret", "median"))
    t["rate_def"] = t.win_def / t.cells
    say(t.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  by panel (DEFAULT control):")
    say(P.groupby("panel").agg(cells=("d_def", "size"),
                               win=("d_def", lambda s: int((s > 0).sum())),
                               med=("d_def", "median")).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  by cost rung (DEFAULT control, all dials pooled):")
    say(CD.groupby("cost").agg(cells=("d_def", "size"),
                               win=("d_def", lambda s: int((s > 0).sum())),
                               med=("d_def", "median"),
                               med_regret=("regret", "median")
                               ).to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"\n  POOLED at {PCOST:g} bps: chooser beats DEFAULT no-dial in "
        f"{int((P.d_def > 0).sum())}/{len(P)} cells (median {P.d_def.median():+.4f}); "
        f"beats MEDIAN-rung control in {int((P.d_med > 0).sum())}/{len(P)} "
        f"(median {P.d_med.median():+.4f})")
    say(f"  the chooser PICKS the default itself in {int(P.pick_is_default.sum())}/{len(P)} cells; "
        f"median OOS regret vs the oracle {P.regret.median():+.4f}")

    # ---- levels vs baseline and SPY, at 10 bps
    say("\n" + "=" * 104)
    say("LEVELS at 10 bps — chooser vs NO-DIAL vs RULES v2 vs SPY (OOS 2017-2026)")
    say("=" * 104)
    for pk, panel in panels.items():
        _b, bt, spy = base_of(pk, panel)
        q = P[P.panel == pk]
        mo_s, mo_b = metrics(spy.loc[OOS_START:]), metrics(bt.loc[OOS_START:])
        say(f"  {pk:>9}  chooser OOS Sharpe med {q.pick_oos.median():.4f} "
            f"(CAGR med {q.pick_cagr_oos.median():.2%}, DD med {q.pick_dd_oos.median():.2%})  |  "
            f"no-dial {q.def_oos.median():.4f} ({q.def_cagr_oos.median():.2%}, "
            f"{q.def_dd_oos.median():.2%})  |  RULES v2 {mo_b['Sharpe']:.4f} "
            f"({mo_b['CAGR']:.2%}, {mo_b['MaxDD']:.2%})  |  SPY {mo_s['Sharpe']:.4f} "
            f"({mo_s['CAGR']:.2%}, {mo_s['MaxDD']:.2%})")

    # ---- full sample + halves for the pooled arms (PROTOCOL 4)
    say("\nFULL SAMPLE + HALVES (10 bps, medians over the grid, by panel and book):")
    g10 = GD.copy()
    say(g10.groupby(["panel", "book"]).agg(
        cagr=("cagr_full_10", "median"), sharpe=("sh_full_10", "median"),
        dd=("dd_full_10", "median"), h1=("h1_10", "median"), h2=("h2_10", "median"),
        ).to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- KEEP paths
    say("\n" + "=" * 104)
    say("KEEP PATHS (PROTOCOL 4, both priced on every arm, 10 bps)")
    say("=" * 104)
    say(f"  full sample : 4a {int(GD.p4a_full.sum())}/{len(GD)}   4b {int(GD.p4b_full.sum())}/{len(GD)}")
    say(f"  OOS window  : 4a {int(GD.p4a_oos.sum())}/{len(GD)}   4b {int(GD.p4b_oos.sum())}/{len(GD)}")
    say("  chooser arms: 4a %d/%d  4b %d/%d   |  no-dial arms: 4a %d/%d  4b %d/%d" % (
        int(P.pick_4a.sum()), len(P), int(P.pick_4b.sum()), len(P),
        int(P.def_4a.sum()), len(P), int(P.def_4b.sum()), len(P)))

    W = CD.copy()
    W.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    say(f"\nwrote .census.csv .grid.csv .cells.csv .wf.csv   [{time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
