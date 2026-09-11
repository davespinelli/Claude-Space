#!/usr/bin/env python3
"""
IDEA 673 -- how-much-of-the-record-s-CAND-vs-EWALL-premia-is-EXPOSURE
=====================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 504 showed the record's standard EW-all comparand is not gross-matched to a
  fixed-weight CAND-n book, which de-grosses to cash below n eligible names, and that the gap
  this opens (+0.0594 U56, +0.0423 B136 median Sharpe at 10 bps) is larger than every
  selection effect measured beside it.  Re-price every committed CAND-vs-EWall premium in the
  record at a matched gross and report how many survive.  Max 2 params (claim set, matching
  rule).

WHAT IS AT STAKE
----------------
  "X beats EW-all" is one of the record's most-used sentences.  If the EW-all comparand runs a
  full gross while the book beside it de-grosses to cash, the published premium contains an
  exposure term the reader never sees -- and 504 measured that term as LARGER than every
  selection effect it sat next to.  This run asks how much of the committed record that
  contaminates, and whether any of it survives when the exposure leg is taken back out.

DESIGN -- two parts, because the record cannot answer alone
-----------------------------------------------------------
  PART A  CENSUS of the committed record.  Every CSV in research/backtests is scanned for a
          published CAND-vs-EWall premium in one of two forms:
            FORM A  an explicit premium column  (dSharpe_vs_EWall / dSharpe_vs_EWALL / ...)
            FORM B  a paired column  (Sharpe  and  EWall_Sharpe / EW_Sharpe / ...)
          Each premium row is then classified on the one thing the queue cares about: does the
          file carry, for that row's own cell, an EW control whose GROSS equals the row's?
            MATCHED       an EW control exists at the same cell and |dgross| <= 1e-6
            UNMATCHED     an EW control exists at the same cell at a DIFFERENT gross
            UNKNOWN_*     no EW control row at that cell, or the file publishes no gross
          UNKNOWN is COUNTED, NEVER GUESSED (idea 459's convention).

  PART B  A FRESH grid where the matched control exists BY CONSTRUCTION, which is the only way
          to measure the exposure leg the record omits.  On each panel, through the incumbent's
          own gate (above the 200d MA, vol20 < 0.60, composite with NO vol scaler), weekly,
          four books:
            CANDn    top n by composite, FIXED 0.75/n per name  (de-grosses to cash below n)
            EWall    EVERY eligible name sharing a full gross of 0.75      <- the record's comparand
            EWmg     every eligible name, equal weight, at CANDn's OWN gross that day
            CANDrg   CANDn's own names, renormalised to a full gross of 0.75
          giving the same premium under two MATCHING RULES (tuned axis 2):
            MR-EWMG   PREMIUM = CANDn - EWall = SELECTION (CANDn - EWmg) + EXPOSURE (EWmg - EWall)
            MR-CANDRG PREMIUM = CANDn - EWall = SELECTION (CANDrg - EWall) + EXPOSURE (CANDn - CANDrg)
          One de-levers the diversified control down to the book; the other levers the book up
          to the control.  Both are defensible and they are NOT the same number; publishing one
          alone would be the same error the census is about.

  PART D  RE-PRICE the census.  For every census premium row that has a same-file EW control
          and a published gross, the exposure leg is predicted from Part B's measured slope
          (Sharpe per unit of gross deficit, fitted per panel and cost rung, with its R^2 and a
          min/max slope BRACKET published beside the point estimate), subtracted, and the row's
          SIGN re-read.  Rows without a control or without a gross are un-repriceable and are
          reported as such -- coverage is this run's binding limit, and it is stated, not hidden.

  TUNED (2)   CLAIM SET (which committed rows count as a published CAND-vs-EWall premium:
              FORM A explicit-column rows, and the wider FORM A+B reading) x MATCHING RULE
              (MR-EWMG / MR-CANDRG).  Both readings of both axes are reported in full.
  NOT TUNED   n in {3,5,10,15,20,30,40} and panel {U56,B136,SMALL439} are STRUCTURAL axes,
              every point reported; gross 0.75, band/vol gate, cadence W, warm-up 260 rows,
              IS/OOS split 2016-12-31 / 2017-01-01 (PROTOCOL rule 8).  None chosen by outcome.
  COST        10 bps (PROTOCOL rule 2) is the only rung a verdict is taken at.  0 and 25 bps are
              a LABELLED appendix; they are free here (gross-return and turnover streams are
              shared) and are not a third tuned axis.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  Panel.run == engine.backtest @10 bps                                      bar 1e-12
  G2  band_book(0.03,0.75) == baseline.rules_v2_weights                         bar 0.0
  G3  CAND20 on FULL U56 == the standing 2026-09-04 KEEP-4b incumbent
      (published 12.66% / 1.0921 / -18.31%)                                     bar 5e-3
  G4  EWall holds gross 0.75 exactly whenever any name is eligible              bar 1e-12
  G4b EWmg's daily gross == CANDn's, every day, every n                         bar 1e-12
  G4c CANDrg holds gross 0.75 exactly whenever any name is eligible             bar 1e-12
  G5  the cost-rung identity net(c) = gross_ret - turnover*c/1e4 vs a live
      engine.backtest(cost_bps=25)                                              bar 1e-12
  G6  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  B136 is today's constituents and SMALL439 the current sub-$2B screen only (see
  data/SMALL_PANEL_README.md): names acquired, delisted or grown out of the screen are absent,
  so every LEVEL on those panels is biased upward and none is a tradeable estimate.  Every leg
  reported here is a WITHIN-PANEL difference over the same names and days, so the bias applies
  to both sides and largely differences out; the 4b PASS COUNTS, which are levels against SPY,
  do not enjoy that protection.
"""
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

COST0 = 10.0                       # PROTOCOL rule 2 -- the only rung a verdict is taken at
COSTS = [0.0, 10.0, 25.0]
FREQ = "W"
BAND0, GROSS0 = 0.03, 0.75
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [3, 5, 10, 15, 20, 30, 40]    # structural axis, every point reported
KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)
MAXBYTES = 300 * 1024 * 1024       # census file-size guard; skips are reported

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ---------------------------------------------------------------------------------- engine --
class Panel:
    """Everything about one panel that does not depend on the book (engine copied verbatim
    from 2026-09-11_price-PERSISTENCE-...-composite_C.py, where G1/G1b pinned it)."""

    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx = px.index
        self.T, self.N = px.shape
        self.rets = px.pct_change().fillna(0.0).values
        pe = np.flatnonzero(rebalance_mask(self.idx, FREQ).values)
        reb = np.concatenate([[0], (pe + 1)[pe + 1 < self.T]])
        self.reb = reb
        self.dec = np.concatenate([[-1], pe[pe + 1 < self.T]])
        C = np.cumprod(1.0 + self.rets, axis=0)
        Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.C, self.Cp = C, Cp
        seg = np.searchsorted(reb, np.arange(self.T), side="right") - 1
        self.seg = seg
        s0, s0p = reb[seg], reb[np.maximum(seg - 1, 0)]
        self.CpS, self.CpP = Cp / Cp[s0], Cp / Cp[s0p]
        self.segp = np.maximum(seg - 1, 0)
        sc, above, vol20 = score(px, vol_scale=False)
        tr = list(px.columns)                  # baseline ranks SPY with the rest (G3 pins it)
        self.elig = (above[tr] & (vol20[tr] < VOLCAP)).values
        self.sc = sc[tr].values
        self.start = WARM
        self.cols = tr

    def run(self, Wreb):
        W0 = Wreb[self.seg]
        h = W0 * self.CpS
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = Wreb[self.segp]
        hp = W0p * self.CpP
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(Wreb - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn


def M0(r):
    v = r.std(ddof=1) * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = np.cumprod(1 + r)
    yrs = len(r) / 252
    vol = r.std(ddof=1) * np.sqrt(252)
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    h = len(r) // 2
    return dict(CAGR=eq[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r[:h]), H2=M0(r[h:]))


def keeppaths(m, oos_s, mb, ms, spy_oos):
    """PROTOCOL rule 4.  4a: Sharpe > the live book in BOTH halves and MaxDD no worse.
       4b: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > spy_oos)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b)


def fail4b(m, oos_s, ms, spy_oos):
    f = []
    if not m["H1"] > ms["H1"]: f.append("H1")
    if not m["H2"] > ms["H2"]: f.append("H2")
    if not oos_s > spy_oos: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return "+".join(f) if f else "-"


# ----------------------------------------------------------------------------------- books --
def cand_lists(pan, n):
    """top-n by composite on every rebalance row, average-rank ties exactly as
    baseline's `rank(axis=1, ascending=False) <= n` (a tie straddling rank n keeps BOTH)."""
    R = len(pan.reb)
    lists = [np.empty(0, int)]
    for k in range(1, R):
        d = pan.dec[k]
        el = np.flatnonzero(pan.elig[d] & ~np.isnan(pan.sc[d]))
        if el.size:
            s = pan.sc[d][el]
            sel = el[pd.Series(s).rank(ascending=False).values <= n]
        else:
            sel = np.empty(0, int)
        lists.append(np.sort(sel))
    return lists


def elig_lists(pan):
    R = len(pan.reb)
    lists = [np.empty(0, int)]
    for k in range(1, R):
        d = pan.dec[k]
        lists.append(np.flatnonzero(pan.elig[d] & ~np.isnan(pan.sc[d])))
    return lists


def W_from(pan, lists, wfun):
    """wfun(k, L) -> per-name weight for that rebalance row."""
    W = np.zeros((len(pan.reb), pan.N))
    for k, L in enumerate(lists):
        if L.size:
            W[k, L] = wfun(k, L)
    return W


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


# ------------------------------------------------------------------------------------ gates --
def gates(panels, n_dropped):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    pan = panels["U56"]
    px = pan.px

    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2  band_book(0.03,0.75) == rules_v2_weights            : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= g2 == 0.0

    Wreb = np.zeros((len(pan.reb), pan.N))
    wv = w.values
    for k in range(1, len(pan.reb)):
        Wreb[k] = wv[pan.dec[k]]
    gr, tu = pan.run(Wreb)
    slow = backtest(px, w, cost_bps=COST0, freq=FREQ)["returns"].values
    g1 = float(np.abs(slow[WARM:] - (gr - tu * COST0 / 1e4)[WARM:]).max())
    P(f"  G1  Panel.run == engine.backtest @10 bps                : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    slow25 = backtest(px, w, cost_bps=25.0, freq=FREQ)["returns"].values
    g5 = float(np.abs(slow25[WARM:] - (gr - tu * 25.0 / 1e4)[WARM:]).max())
    P(f"  G5  cost-rung identity net(25) vs live backtest(25)     : {g5:.3e}  "
      f"{'PASS' if g5 < 1e-12 else 'FAIL'}")
    ok &= g5 < 1e-12

    # G3 -- the standing incumbent, and G4/G4b/G4c -- the gross matching this run depends on
    EL = elig_lists(pan)
    W_ewall = W_from(pan, EL, lambda k, L: GROSS0 / L.size)
    gmax = 0.0
    gmaxrg = 0.0
    gmatch = 0.0
    for n in NS:
        CL = cand_lists(pan, n)
        W_c = W_from(pan, CL, lambda k, L, n=n: GROSS0 / n)
        W_rg = W_from(pan, CL, lambda k, L: GROSS0 / L.size)
        sizes = np.array([L.size for L in CL], float)
        W_mg = W_from(pan, EL, lambda k, L, s=sizes, n=n: (GROSS0 / n) * s[k] / L.size)
        gmatch = max(gmatch, float(np.abs(W_mg.sum(axis=1) - W_c.sum(axis=1)).max()))
        nz = np.array([L.size > 0 for L in CL])
        gmaxrg = max(gmaxrg, float(np.abs(W_rg.sum(axis=1)[nz] - GROSS0).max()))
        if n == 20:
            grc, tuc = pan.run(W_c)
            m = M((grc - tuc * COST0 / 1e4)[WARM:])
    nz = np.array([L.size > 0 for L in EL])
    gmax = float(np.abs(W_ewall.sum(axis=1)[nz] - GROSS0).max())

    d = {k: abs(m[k] - v) for k, v in KEEP4B_INCUMBENT.items()}
    P("  G3  CAND20 on FULL U56 == the 2026-09-04 KEEP-4b incumbent (top-20 EW, no vol scaler):")
    P(f"      got {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   published "
      f"{KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {max(d.values()):.3e}  "
      f"{'PASS' if max(d.values()) < 5e-3 else 'FAIL'}")
    P("      (the published triple is the 2026-09-04 vintage; ideas 672/679 re-derived the "
      "same book on today's cache at 12.63% / 1.090 / -18.31%)")
    ok &= max(d.values()) < 5e-3
    P(f"  G4  EWall gross == 0.75 whenever any name eligible      : {gmax:.3e}  "
      f"{'PASS' if gmax < 1e-12 else 'FAIL'}")
    P(f"  G4b EWmg daily gross == CANDn's, every n, every day     : {gmatch:.3e}  "
      f"{'PASS' if gmatch < 1e-12 else 'FAIL'}")
    P(f"  G4c CANDrg gross == 0.75 whenever any name eligible     : {gmaxrg:.3e}  "
      f"{'PASS' if gmaxrg < 1e-12 else 'FAIL'}")
    ok &= (gmax < 1e-12) and (gmatch < 1e-12) and (gmaxrg < 1e-12)

    P(f"  G6  SMALL439 dropped {n_dropped} tickers with max_1d_move >= 1.0 : "
      f"{'PASS' if n_dropped > 0 else 'FAIL'}")
    ok &= n_dropped > 0
    P()
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- results below are not trustworthy'}")
    return ok


# ------------------------------------------------------------------------------ PART A: census
PREM_RE = re.compile(r"^d.*sharpe.*ew", re.I)
EWSHARPE_RE = re.compile(r"^(ew|ewall|ew_all|ewfull)[_a-z0-9]*_?sharpe$", re.I)
BOOKCOL = ("book", "arm", "kind", "variant", "scheme", "family", "label", "name", "rule")
EWLAB_RE = re.compile(r"^(ew|ewall|ew[-_ ]?all|equal)", re.I)
CANDLAB_RE = re.compile(r"cand|top\d|^top$|rank|mom|ma-|sel|comp", re.I)
METRIC_RE = re.compile(r"sharpe|cagr|maxdd|dd|calmar|turn|vol|gross|keep|pass|fail|beat|"
                       r"oos|_is|is_|h1|h2|median|mean|sd|pct|share|rho|slope|t_|_t$|"
                       r"count|^n_|margin|excess|ratio|width|seed", re.I)
PANEL_MAP = {"u56": "U56", "universe": "U56", "live": "U56", "u": "U56",
             "b136": "B136", "broad": "B136", "b": "B136", "broad136": "B136",
             "small439": "SMALL439", "small": "SMALL439", "small485": "SMALL439",
             "s439": "SMALL439", "sm": "SMALL439"}


def _is_text(s):
    """pandas 3 reads CSV label columns as the `str` dtype, not object."""
    return s.dtype == object or pd.api.types.is_string_dtype(s)


def _panel_of(v):
    s = str(v).strip().lower()
    return PANEL_MAP.get(s, None)


def census():
    P()
    P("=" * 100)
    P("(B) PART A -- CENSUS of the committed record: who publishes a CAND-vs-EWall premium?")
    P("=" * 100)
    files = sorted(p for p in OUT.glob("*.csv") if not p.name.startswith(STEM))
    P(f"  CSV artefacts scanned (this run's own outputs excluded): {len(files)}")
    cand_files, skipped = [], []
    for p in files:
        try:
            head = p.open("r", errors="ignore").readline().strip()
        except Exception:
            skipped.append((p.name, "unreadable header"))
            continue
        cols = head.split(",")
        pcols = [c for c in cols if PREM_RE.match(c.strip('"'))]
        ecols = [c for c in cols if EWSHARPE_RE.match(c.strip('"'))]
        has_sharpe = any(c.strip('"').lower() == "sharpe" for c in cols)
        if pcols or (ecols and has_sharpe):
            if p.stat().st_size > MAXBYTES:
                skipped.append((p.name, f"{p.stat().st_size/1e6:.0f} MB > guard"))
                continue
            cand_files.append((p, pcols, ecols if has_sharpe else []))
    P(f"  files carrying a premium column (FORM A) or an EW-Sharpe pair (FORM B): "
      f"{len(cand_files)}   skipped: {len(skipped)}")
    for nm, why in skipped:
        P(f"     SKIPPED {nm}  ({why})")

    rows, per_file = [], []
    for p, pcols, ecols in cand_files:
        try:
            df = pd.read_csv(p, low_memory=False)
        except Exception as e:
            skipped.append((p.name, f"parse: {type(e).__name__}"))
            continue
        cols = list(df.columns)
        # the BOOK column is the label column that actually names an EW control (the one whose
        # values the premium is measured against); ties break on the count of EW-labelled rows
        bcands = [c for c in cols if c.lower() in BOOKCOL and _is_text(df[c])]
        scored = sorted(((int(df[c].astype(str).str.match(EWLAB_RE).sum()), -cols.index(c), c)
                         for c in bcands), reverse=True)
        bookcol = scored[0][2] if scored and scored[0][0] > 0 else (bcands[0] if bcands else None)
        grosscol = next((c for c in cols if c.lower() in ("gross", "g", "gross_mean",
                                                          "mean_gross", "gross_realised",
                                                          "gross_realized")), None)
        panelcol = next((c for c in cols if c.lower() in ("panel", "universe", "pan")), None)
        costcol = next((c for c in cols if c.lower() in ("bps", "cost", "cost_bps", "rung")),
                       None)
        keys = [c for c in cols
                if c != bookcol and not METRIC_RE.search(c)
                and (_is_text(df[c]) or str(df[c].dtype).startswith(("int", "bool")))]
        if costcol and costcol not in keys:
            keys.append(costcol)
        # EW control rows, indexed by their cell key
        ctrl = {}
        if bookcol is not None:
            ew = df[df[bookcol].astype(str).str.match(EWLAB_RE)]
            if grosscol is not None and len(ew):
                for _, r in ew.iterrows():
                    k = tuple(r[c] for c in keys) if keys else ()
                    ctrl.setdefault(k, []).append(r[grosscol])
        n_a = n_b = 0
        for form, cset in (("A", pcols), ("B", ecols)):
            for c in cset:
                c = c.strip('"')
                if c not in df.columns:
                    continue
                if form == "A":
                    prem = pd.to_numeric(df[c], errors="coerce")
                else:
                    prem = (pd.to_numeric(df["Sharpe"], errors="coerce")
                            - pd.to_numeric(df[c], errors="coerce"))
                for i, v in prem.items():
                    if not np.isfinite(v):
                        continue
                    lab = str(df.at[i, bookcol]) if bookcol is not None else ""
                    is_ctrl = bool(EWLAB_RE.match(lab)) or (form == "A" and v == 0.0
                                                            and bookcol is None)
                    if is_ctrl:
                        continue                      # the control's own zero row is not a claim
                    k = tuple(df.at[i, cc] for cc in keys) if keys else ()
                    g = df.at[i, grosscol] if grosscol is not None else np.nan
                    gc = np.nan
                    if k in ctrl and len(ctrl[k]):
                        gc = float(np.nanmedian([float(x) for x in ctrl[k]]))
                    if not np.isfinite(pd.to_numeric(pd.Series([g]), errors="coerce")[0]):
                        status = "UNKNOWN_NOGROSS"
                    elif not np.isfinite(gc):
                        status = "UNKNOWN_NOCTRL"
                    else:
                        g = float(g)
                        status = "MATCHED" if abs(g - gc) <= 1e-6 else "UNMATCHED"
                    pn = _panel_of(df.at[i, panelcol]) if panelcol is not None else None
                    cst = pd.to_numeric(pd.Series([df.at[i, costcol]]),
                                        errors="coerce")[0] if costcol is not None else np.nan
                    kind = ("EWCTRL" if EWLAB_RE.match(lab) else
                            "RANKED" if CANDLAB_RE.search(lab) else
                            "OTHER" if lab else "UNLABELLED")
                    rows.append(dict(file=p.name, form=form, col=c, row=i, book=lab, kind=kind,
                                     premium=float(v), gross=float(g) if np.isfinite(
                                         pd.to_numeric(pd.Series([g]), errors="coerce")[0])
                                     else np.nan,
                                     gross_ctrl=gc, status=status,
                                     panel=pn if pn else (str(df.at[i, panelcol])
                                                          if panelcol is not None else ""),
                                     panel_mapped=bool(pn), bps=cst))
                    n_a += form == "A"
                    n_b += form == "B"
        per_file.append(dict(file=p.name, formA_cols=len(pcols), formB_cols=len(ecols),
                             rows=len(df), claims_A=n_a, claims_B=n_b,
                             has_book=bookcol is not None, has_gross=grosscol is not None,
                             has_panel=panelcol is not None, keys="|".join(keys[:8])))
    cl = pd.DataFrame(rows)
    pf = pd.DataFrame(per_file)
    P()
    P(f"  PREMIUM ROWS FOUND: {len(cl)}  over {cl.file.nunique()} files "
      f"({(cl.form=='A').sum()} FORM A explicit-column, {(cl.form=='B').sum()} FORM B paired)")
    P()
    P("  claim set x gross-match status (the queue's question, counted not guessed):")
    tab = cl.pivot_table(index="status", columns="form", values="premium", aggfunc="count",
                         fill_value=0)
    tab["ALL"] = tab.sum(axis=1)
    tab.loc["TOTAL"] = tab.sum()
    P(tab.to_string())
    P()
    P("  by book kind (label vocabulary, UNLABELLED = the file names no book column):")
    P(cl.groupby("kind").agg(rows=("premium", "size"),
                             median_premium=("premium", "median"),
                             share_positive=("premium", lambda s: float((s > 0).mean()))
                             ).to_string(float_format=lambda x: f"{x:.4f}"))
    P()
    pos = cl[cl.premium > 0]
    P(f"  POSITIVE premia ('the book beats EW-all'): {len(pos)} of {len(cl)} "
      f"({len(pos)/max(len(cl),1):.1%});  median premium over all rows "
      f"{cl.premium.median():+.4f}, over positives {pos.premium.median():+.4f}")
    um = cl[cl.status == "UNMATCHED"]
    P(f"  UNMATCHED rows (an EW control exists at the cell, at a DIFFERENT gross): {len(um)}"
      f"   median |dgross| {np.nanmedian(np.abs(um.gross - um.gross_ctrl)) if len(um) else float('nan'):.4f}")
    P(f"  re-priceable population (a same-file control AND a published gross): "
      f"{int((cl.status.isin(['MATCHED','UNMATCHED'])).sum())} of {len(cl)} "
      f"({(cl.status.isin(['MATCHED','UNMATCHED'])).mean():.1%}) -- COVERAGE IS THE BINDING LIMIT")
    dump(cl, "claims")
    dump(pf, "census")
    return cl


# ------------------------------------------------------------------------------- PART B: grid
def run_grid(panels):
    P()
    P("=" * 100)
    P("(C) PART B -- the fresh grid: 3 panels x 7 n x 4 books, matched control BY CONSTRUCTION")
    P("=" * 100)
    rows, legs = [], []
    store = {}
    for pn, pan in panels.items():
        px = pan.px
        dates = pan.idx[pan.start:]
        oos = np.asarray(dates >= pd.Timestamp(OOS_START))
        pan.oos = oos
        spy = px["SPY"].pct_change().fillna(0).values[pan.start:]
        ms, spy_o, spy_oos = M(spy), M(spy[oos]), M0(spy[oos])
        w = band_book(px, BAND0, GROSS0).values
        Wv2 = np.zeros((len(pan.reb), pan.N))
        for k in range(1, len(pan.reb)):
            Wv2[k] = w[pan.dec[k]]
        gv, tv = pan.run(Wv2)
        refs = {}
        for c in COSTS:
            rb = (gv - tv * c / 1e4)[pan.start:]
            refs[c] = dict(v2=M(rb), v2_oos=M(rb[oos]), spy=ms, spy_oos=spy_oos, spy_o=spy_o)
        mb, base_o = refs[COST0]["v2"], refs[COST0]["v2_oos"]
        P()
        P(f"  --- {pn}  ({pan.N - 1} tradable + SPY, {dates[0].date()} -> {dates[-1].date()}, "
          f"mean eligible {pan.elig[pan.start:].sum(axis=1).mean():.1f}) ---")
        P(f"      SPY           {ms['CAGR']:7.2%} / {ms['Sharpe']:6.3f} / {ms['MaxDD']:7.2%}"
          f"   H1 {ms['H1']:6.3f} H2 {ms['H2']:6.3f}   OOS {spy_o['CAGR']:7.2%} / "
          f"{spy_oos:6.3f} / {spy_o['MaxDD']:7.2%}")
        P(f"      live RULES v2 {mb['CAGR']:7.2%} / {mb['Sharpe']:6.3f} / {mb['MaxDD']:7.2%}"
          f"   H1 {mb['H1']:6.3f} H2 {mb['H2']:6.3f}   OOS {base_o['CAGR']:7.2%} / "
          f"{base_o['Sharpe']:6.3f} / {base_o['MaxDD']:7.2%}")

        EL = elig_lists(pan)
        W_ew = W_from(pan, EL, lambda k, L: GROSS0 / L.size)
        g_ew, t_ew = pan.run(W_ew)
        store[(pn, "EWall", 0)] = (g_ew, t_ew)
        gross_ew = W_ew.sum(axis=1)[pan.seg][pan.start:]

        def emit(book, n, gr, tu, gmean):
            out = {}
            for c in COSTS:
                r = (gr - tu * c / 1e4)[pan.start:]
                m, mo = M(r), M(r[oos])
                is_s = M0(r[~oos])
                p4a, p4b = keeppaths(m, mo["Sharpe"], refs[c]["v2"], refs[c]["spy"],
                                     refs[c]["spy_oos"])
                rows.append(dict(panel=pn, book=book, n=n, bps=c, gross_mean=gmean,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=m["H1"], H2=m["H2"], IS_Sharpe=is_s,
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                 OOS_MaxDD=mo["MaxDD"],
                                 turnover_yr=tu[pan.start:].sum() / (len(r) / 252),
                                 SPY_Sharpe=refs[c]["spy"]["Sharpe"],
                                 SPY_CAGR=refs[c]["spy"]["CAGR"],
                                 SPY_MaxDD=refs[c]["spy"]["MaxDD"],
                                 SPY_OOS_Sharpe=refs[c]["spy_oos"],
                                 v2_Sharpe=refs[c]["v2"]["Sharpe"],
                                 v2_OOS_Sharpe=refs[c]["v2_oos"]["Sharpe"],
                                 pass4a=p4a, pass4b=p4b,
                                 fail4b=fail4b(m, mo["Sharpe"], refs[c]["spy"],
                                               refs[c]["spy_oos"])))
                out[c] = dict(m=m, oos=mo, is_s=is_s)
            return out

        mew = emit("EWall", 0, g_ew, t_ew, float(np.mean(gross_ew)))
        ew10 = [x for x in rows if x["panel"] == pn and x["book"] == "EWall"
                and x["bps"] == COST0][0]
        P()
        P("      n  book     gross    CAGR   Sharpe    MaxDD     H1     H2 |  OOS Sh  OOS DD | "
          "4a 4b   PREMIUM  SELECT  EXPOSE   (MR-EWMG / MR-CANDRG)")
        P(f"      -  EWall   {np.mean(gross_ew):.4f} {mew[COST0]['m']['CAGR']:7.2%} "
          f"{mew[COST0]['m']['Sharpe']:7.3f} {mew[COST0]['m']['MaxDD']:8.2%} "
          f"{mew[COST0]['m']['H1']:6.3f} {mew[COST0]['m']['H2']:6.3f} | "
          f"{mew[COST0]['oos']['Sharpe']:7.3f} {mew[COST0]['oos']['MaxDD']:7.2%} |  "
          f"{'Y' if ew10['pass4a'] else '.'}  {'Y' if ew10['pass4b'] else '.'}"
          "        -       -       -")
        for n in NS:
            CL = cand_lists(pan, n)
            sizes = np.array([L.size for L in CL], float)
            W_c = W_from(pan, CL, lambda k, L, n=n: GROSS0 / n)
            W_rg = W_from(pan, CL, lambda k, L: GROSS0 / L.size)
            W_mg = W_from(pan, EL, lambda k, L, s=sizes, n=n: (GROSS0 / n) * s[k] / L.size)
            gc = W_c.sum(axis=1)[pan.seg][pan.start:]
            res = {}
            for lab, W in (("CAND", W_c), ("CANDrg", W_rg), ("EWmg", W_mg)):
                gr, tu = pan.run(W)
                store[(pn, lab, n)] = (gr, tu)
                res[lab] = emit(lab, n, gr, tu, float(np.mean(
                    (W.sum(axis=1)[pan.seg][pan.start:]))))
            for c in COSTS:
                prem = res["CAND"][c]["m"]["Sharpe"] - mew[c]["m"]["Sharpe"]
                sel_mg = res["CAND"][c]["m"]["Sharpe"] - res["EWmg"][c]["m"]["Sharpe"]
                exp_mg = res["EWmg"][c]["m"]["Sharpe"] - mew[c]["m"]["Sharpe"]
                sel_rg = res["CANDrg"][c]["m"]["Sharpe"] - mew[c]["m"]["Sharpe"]
                exp_rg = res["CAND"][c]["m"]["Sharpe"] - res["CANDrg"][c]["m"]["Sharpe"]
                oprem = res["CAND"][c]["oos"]["Sharpe"] - mew[c]["oos"]["Sharpe"]
                osel_mg = res["CAND"][c]["oos"]["Sharpe"] - res["EWmg"][c]["oos"]["Sharpe"]
                osel_rg = res["CANDrg"][c]["oos"]["Sharpe"] - mew[c]["oos"]["Sharpe"]
                legs.append(dict(panel=pn, n=n, bps=c, gross_cand=float(np.mean(gc)),
                                 gross_ew=float(np.mean(gross_ew)),
                                 gdef=float(np.mean(gross_ew) - np.mean(gc)),
                                 PREMIUM=prem, SEL_EWMG=sel_mg, EXP_EWMG=exp_mg,
                                 SEL_CANDRG=sel_rg, EXP_CANDRG=exp_rg,
                                 OOS_PREMIUM=oprem, OOS_SEL_EWMG=osel_mg,
                                 OOS_SEL_CANDRG=osel_rg,
                                 dCAGR=res["CAND"][c]["m"]["CAGR"] - mew[c]["m"]["CAGR"],
                                 dMaxDD=res["CAND"][c]["m"]["MaxDD"] - mew[c]["m"]["MaxDD"],
                                 survives_EWMG=bool(np.sign(sel_mg) == np.sign(prem)
                                                    and sel_mg != 0),
                                 survives_CANDRG=bool(np.sign(sel_rg) == np.sign(prem)
                                                      and sel_rg != 0)))
            r10 = res["CAND"][COST0]
            gi = [x for x in rows if x["panel"] == pn and x["book"] == "CAND"
                  and x["n"] == n and x["bps"] == COST0][0]
            P(f"     {n:2d}  CAND    {np.mean(gc):.4f} {r10['m']['CAGR']:7.2%} "
              f"{r10['m']['Sharpe']:7.3f} {r10['m']['MaxDD']:8.2%} {r10['m']['H1']:6.3f} "
              f"{r10['m']['H2']:6.3f} | {r10['oos']['Sharpe']:7.3f} "
              f"{r10['oos']['MaxDD']:7.2%} |  {'Y' if gi['pass4a'] else '.'}  "
              f"{'Y' if gi['pass4b'] else '.'}  {legs[-2]['PREMIUM']:+7.4f} "
              f"{legs[-2]['SEL_EWMG']:+7.4f} {legs[-2]['EXP_EWMG']:+7.4f}   "
              f"({legs[-2]['SEL_CANDRG']:+.4f} / {legs[-2]['EXP_CANDRG']:+.4f})")
    gr_df, lg_df = pd.DataFrame(rows), pd.DataFrame(legs)
    dump(gr_df, "grid")
    dump(lg_df, "legs")
    return gr_df, lg_df, store


def leg_summary(lg):
    P()
    P("  --- THE ANSWER on the fresh grid (10 bps, the only verdict rung) ---")
    x = lg[lg.bps == COST0]
    P()
    P("   panel      n  gross(CAND)  PREMIUM   = SEL(EWmg) + EXP(EWmg)  |  SEL(CANDrg) + "
      "EXP(CANDrg)  | survives?")
    for _, r in x.iterrows():
        P(f"   {r.panel:9s} {int(r.n):2d}   {r.gross_cand:.4f}    {r.PREMIUM:+7.4f}   "
          f"{r.SEL_EWMG:+7.4f}   {r.EXP_EWMG:+7.4f}   |  {r.SEL_CANDRG:+7.4f}   "
          f"{r.EXP_CANDRG:+7.4f}   |  "
          f"{'EWMG' if r.survives_EWMG else '----'} {'CANDRG' if r.survives_CANDRG else '------'}")
    P()
    for pn, g in x.groupby("panel"):
        P(f"   {pn}: median PREMIUM {g.PREMIUM.median():+.4f}  = SEL {g.SEL_EWMG.median():+.4f}"
          f" + EXP {g.EXP_EWMG.median():+.4f} (MR-EWMG)   |   SEL {g.SEL_CANDRG.median():+.4f}"
          f" + EXP {g.EXP_CANDRG.median():+.4f} (MR-CANDRG)")
    pos = x[x.PREMIUM > 0]
    P()
    P(f"   POSITIVE premia on the fresh grid: {len(pos)} of {len(x)}; of those, SIGN SURVIVES "
      f"the matched control in {int(pos.survives_EWMG.sum())} (MR-EWMG) and "
      f"{int(pos.survives_CANDRG.sum())} (MR-CANDRG) cases")
    P(f"   |EXPOSURE| > |SELECTION| in {int((x.EXP_EWMG.abs() > x.SEL_EWMG.abs()).sum())} of "
      f"{len(x)} cells (MR-EWMG), "
      f"{int((x.EXP_CANDRG.abs() > x.SEL_CANDRG.abs()).sum())} of {len(x)} (MR-CANDRG)")
    P()
    P("   APPENDIX (labelled, not a tuned axis) -- the same counts at 0 and 25 bps:")
    for c in (0.0, 25.0):
        y = lg[lg.bps == c]
        yp = y[y.PREMIUM > 0]
        P(f"     {int(c):2d} bps: {len(yp)}/{len(y)} positive; sign survives "
          f"{int(yp.survives_EWMG.sum())} (EWMG) / {int(yp.survives_CANDRG.sum())} (CANDRG); "
          f"median EXP {y.EXP_EWMG.median():+.4f} vs SEL {y.SEL_EWMG.median():+.4f}")


# ------------------------------------------------------------ PART D: re-price the census --
def reprice(cl, lg):
    P()
    P("=" * 100)
    P("(D) PART D -- RE-PRICE the committed premia at a matched gross")
    P("=" * 100)
    slopes = {}
    P()
    P("  Exposure slope fitted on the fresh grid: EXPOSURE Sharpe per unit of GROSS DEFICIT")
    P("  (through the origin -- a zero deficit is a matched book, whose exposure leg is 0)")
    P()
    P("   panel      bps   slope   R^2    n cells   bracket [min,max] per-cell slope")
    for (pn, c), g in lg.groupby(["panel", "bps"]):
        gd, ex = g.gdef.values, g.EXP_EWMG.values
        ok = gd > 1e-9
        if ok.sum() < 2:
            continue
        b = float((gd[ok] * ex[ok]).sum() / (gd[ok] ** 2).sum())
        ss = float(1 - ((ex[ok] - b * gd[ok]) ** 2).sum() / (ex[ok] ** 2).sum())
        per = ex[ok] / gd[ok]
        slopes[(pn, c)] = (b, float(per.min()), float(per.max()))
        P(f"   {pn:9s} {int(c):3d}  {b:+7.4f}  {ss:5.3f}   {int(ok.sum()):4d}      "
          f"[{per.min():+.4f}, {per.max():+.4f}]")
    pooled = {}
    for c in COSTS:
        vals = [v for (pn, cc), v in slopes.items() if cc == c]
        if vals:
            pooled[c] = (float(np.median([v[0] for v in vals])),
                         float(min(v[1] for v in vals)), float(max(v[2] for v in vals)))
    P(f"   POOLED (used when a row's panel label does not map): "
      + ", ".join(f"{int(c)} bps {pooled[c][0]:+.4f}" for c in sorted(pooled)))

    rp = cl[cl.status.isin(["MATCHED", "UNMATCHED"])].copy()
    P()
    P(f"  RE-PRICEABLE population: {len(rp)} rows of {len(cl)} "
      f"({len(rp)/max(len(cl),1):.1%}).  The other {len(cl)-len(rp)} publish no gross or carry "
      f"no same-file EW control at their own cell and CANNOT be re-priced from the record.")
    if not len(rp):
        return rp
    def _slope(r, which):
        c = r.bps if r.bps in COSTS else COST0
        key = (r.panel, c)
        s = slopes.get(key) or pooled.get(c) or pooled.get(COST0)
        return s[which]

    # The record's `gross` column is the NOMINAL dial, not the book's realised exposure.  A
    # ranked book at nominal 0.75 does NOT run 0.75: it de-grosses to cash whenever fewer than
    # n names are eligible, which is exactly the channel 504 named and the nominal column
    # cannot see.  So every row is re-priced twice, and both readings are reported:
    #   NOMINAL   deficit = published control gross - published row gross   (MATCHED -> 0)
    #   REALISED  deficit = that, PLUS the fresh grid's measured realised deficit for a
    #             de-grossing ranked book on that panel (median over n at the row's cost rung)
    real = {}
    for (pn, c), g in lg.groupby(["panel", "bps"]):
        real[(pn, c)] = float(g.gdef.median())
    real_pool = {c: float(np.median([v for (p_, cc), v in real.items() if cc == c]))
                 for c in COSTS}
    P()
    P("  measured REALISED gross deficit by n (10 bps) -- what the record's NOMINAL gross "
      "column cannot see; a book at nominal 0.75 does not run 0.75:")
    w = lg[lg.bps == COST0].pivot_table(index="panel", columns="n", values="gdef")
    P("   " + w.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P()
    P("  measured REALISED gross deficit of a de-grossing ranked book (fresh grid, median "
      "over n):")
    for c in COSTS:
        P(f"    {int(c):2d} bps  " + "   ".join(
            f"{pn} {real.get((pn, c), float('nan')):.4f}" for pn in ("U56", "B136", "SMALL439"))
          + f"   pooled {real_pool[c]:.4f}")

    def _real(r):
        c = r.bps if r.bps in COSTS else COST0
        return real.get((r.panel, c), real_pool.get(c, real_pool[COST0]))

    rp["gdef_nom"] = rp.gross_ctrl - rp.gross
    rp["gdef_real"] = [r.gdef_nom + _real(r) for _, r in rp.iterrows()]
    rp["exp_nom"] = [_slope(r, 0) * r.gdef_nom for _, r in rp.iterrows()]
    rp["exp_real"] = [_slope(r, 0) * r.gdef_real for _, r in rp.iterrows()]
    rp["exp_real_lo"] = [min(_slope(r, 1) * r.gdef_real, _slope(r, 2) * r.gdef_real)
                         for _, r in rp.iterrows()]
    rp["exp_real_hi"] = [max(_slope(r, 1) * r.gdef_real, _slope(r, 2) * r.gdef_real)
                         for _, r in rp.iterrows()]
    rp["sel_nom"] = rp.premium - rp.exp_nom
    rp["sel_real"] = rp.premium - rp.exp_real
    rp["survives_nom"] = (np.sign(rp.sel_nom) == np.sign(rp.premium)) & (rp.premium != 0)
    rp["survives_real"] = (np.sign(rp.sel_real) == np.sign(rp.premium)) & (rp.premium != 0)
    rp["survives_bracket"] = ((np.sign(rp.premium - rp.exp_real_lo) == np.sign(rp.premium))
                              & (np.sign(rp.premium - rp.exp_real_hi) == np.sign(rp.premium))
                              & (rp.premium != 0))
    P()
    P("  by gross-match status  (survival = the premium keeps its published SIGN):")
    for st, g in rp.groupby("status"):
        pos = g[g.premium > 0]
        P(f"    {st:10s} rows {len(g):6d}  median premium {g.premium.median():+.4f}")
        P(f"               NOMINAL  deficit {g.gdef_nom.median():+.4f} -> exposure "
          f"{g.exp_nom.median():+.4f}  survives {int(g.survives_nom.sum())}/{len(g)} "
          f"({g.survives_nom.mean():.1%})")
        P(f"               REALISED deficit {g.gdef_real.median():+.4f} -> exposure "
          f"{g.exp_real.median():+.4f}  survives {int(g.survives_real.sum())}/{len(g)} "
          f"({g.survives_real.mean():.1%});  slope BRACKET "
          f"{int(g.survives_bracket.sum())}/{len(g)} ({g.survives_bracket.mean():.1%})")
        if len(pos):
            P(f"               of the {len(pos)} POSITIVE ones, "
              f"{int(pos.survives_nom.sum())} ({pos.survives_nom.mean():.1%}) stay positive "
              f"under NOMINAL and {int(pos.survives_real.sum())} "
              f"({pos.survives_real.mean():.1%}) under REALISED")
    P()
    P("  by panel -- UNMAPPED is a label this run could not resolve to a known panel and is "
      "counted, never guessed (idea 656's warning: the record's panel vocabulary is wider "
      "than any three-key alias map):")
    rp["panel_grp"] = np.where(rp.panel_mapped.values, rp.panel.values, "UNMAPPED")
    for pn, g in rp.groupby("panel_grp"):
        P(f"    {str(pn)[:12]:12s} rows {len(g):6d}  survives NOM "
          f"{int(g.survives_nom.sum()):6d} ({g.survives_nom.mean():.1%})  REAL "
          f"{int(g.survives_real.sum()):6d} ({g.survives_real.mean():.1%})  median |gdef_nom| "
          f"{np.abs(g.gdef_nom).median():.4f}")
    P()
    P("  HOW INFORMATIVE IS THE SLOPE?  The per-cell slopes above STRADDLE ZERO on every panel, "
      "so a re-price at the bracket's ends can flip a sign in either direction.  The point "
      "estimate below is therefore the reading that stands; the bracket column says how much "
      "of the record is re-priceable ROBUSTLY, which is a different and much smaller number.")
    P()
    P("  by claim set (the tuned axis): FORM A only vs the wider FORM A+B reading")
    for form, g in rp.groupby("form"):
        P(f"    FORM {form}: rows {len(g):6d}  positive {int((g.premium>0).sum()):6d}  "
          f"survives NOM {g.survives_nom.mean():.1%}  REAL {g.survives_real.mean():.1%}")
    P(f"    FORM A+B: rows {len(rp)}  positive {int((rp.premium>0).sum())}  "
      f"survives NOM {rp.survives_nom.mean():.1%}  REAL {rp.survives_real.mean():.1%}")
    dump(rp, "repriced")
    return rp


# -------------------------------------------------------------------- PART E: rule 8 (WF) --
def walkforward(panels, gr, store):
    P()
    P("=" * 100)
    P("(E) RULE 8 WALK-FORWARD -- n chosen on 2009-2016 only, scored on 2017-2026 untouched")
    P("=" * 100)
    rows = []
    for pn, pan in panels.items():
        dates = pan.idx[pan.start:]
        oos = pan.oos
        px = pan.px
        spy = px["SPY"].pct_change().fillna(0).values[pan.start:]
        spy_oos_m = M(spy[oos])
        w = band_book(px, BAND0, GROSS0).values
        Wv2 = np.zeros((len(pan.reb), pan.N))
        for k in range(1, len(pan.reb)):
            Wv2[k] = w[pan.dec[k]]
        gv, tv = pan.run(Wv2)
        v2 = (gv - tv * COST0 / 1e4)[pan.start:]
        v2_oos = M(v2[oos])
        P()
        P(f"  --- {pn} ---   SPY OOS {spy_oos_m['CAGR']:7.2%} / {spy_oos_m['Sharpe']:6.3f} / "
          f"{spy_oos_m['MaxDD']:7.2%}    RULES v2 OOS {v2_oos['CAGR']:7.2%} / "
          f"{v2_oos['Sharpe']:6.3f} / {v2_oos['MaxDD']:7.2%}")
        picks = {}
        for lab in ("CAND", "CANDrg", "EWmg"):
            best, bn = -np.inf, None
            for n in NS:
                grr, tuu = store[(pn, lab, n)]
                r = (grr - tuu * COST0 / 1e4)[pan.start:]
                s = M0(r[~oos])
                if s > best:
                    best, bn = s, n
            grr, tuu = store[(pn, lab, bn)]
            r = (grr - tuu * COST0 / 1e4)[pan.start:]
            mo, m = M(r[oos]), M(r)
            p4a, p4b = keeppaths(m, mo["Sharpe"], M(v2), M(spy), M0(spy[oos]))
            picks[lab] = (bn, r, mo)
            rows.append(dict(panel=pn, family=lab, pick_n=bn, IS_Sharpe=best,
                             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                             SPY_OOS_CAGR=spy_oos_m["CAGR"], SPY_OOS_Sharpe=spy_oos_m["Sharpe"],
                             SPY_OOS_MaxDD=spy_oos_m["MaxDD"], v2_OOS_CAGR=v2_oos["CAGR"],
                             v2_OOS_Sharpe=v2_oos["Sharpe"], v2_OOS_MaxDD=v2_oos["MaxDD"],
                             pass4a=p4a, pass4b=p4b,
                             fail4b=fail4b(m, mo["Sharpe"], M(spy), M0(spy[oos]))))
            P(f"      {lab:7s} picks n={bn:2d} (IS Sharpe {best:.3f}) -> OOS "
              f"{mo['CAGR']:7.2%} / {mo['Sharpe']:6.3f} / {mo['MaxDD']:7.2%}   "
              f"4a {'Y' if p4a else '.'}  4b {'Y' if p4b else '.'}")
        grr, tuu = store[(pn, "EWall", 0)]
        rew = (grr - tuu * COST0 / 1e4)[pan.start:]
        mo_ew = M(rew[oos])
        P(f"      EWall   (no n)                          -> OOS "
          f"{mo_ew['CAGR']:7.2%} / {mo_ew['Sharpe']:6.3f} / {mo_ew['MaxDD']:7.2%}")
        rows.append(dict(panel=pn, family="EWall", pick_n=0, IS_Sharpe=M0(rew[~oos]),
                         OOS_CAGR=mo_ew["CAGR"], OOS_Sharpe=mo_ew["Sharpe"],
                         OOS_MaxDD=mo_ew["MaxDD"], SPY_OOS_CAGR=spy_oos_m["CAGR"],
                         SPY_OOS_Sharpe=spy_oos_m["Sharpe"], SPY_OOS_MaxDD=spy_oos_m["MaxDD"],
                         v2_OOS_CAGR=v2_oos["CAGR"], v2_OOS_Sharpe=v2_oos["Sharpe"],
                         v2_OOS_MaxDD=v2_oos["MaxDD"], pass4a=False, pass4b=False, fail4b=""))
        n_c = picks["CAND"][0]
        grc, tuc = store[(pn, "CAND", n_c)]
        rc = (grc - tuc * COST0 / 1e4)[pan.start:]
        grm, tum = store[(pn, "EWmg", n_c)]
        rm = (grm - tum * COST0 / 1e4)[pan.start:]
        grg, tug = store[(pn, "CANDrg", n_c)]
        rg = (grg - tug * COST0 / 1e4)[pan.start:]
        P(f"      OOS legs at the IS-picked n={n_c}:  PREMIUM "
          f"{M(rc[oos])['Sharpe'] - mo_ew['Sharpe']:+.4f}  = SEL(EWmg) "
          f"{M(rc[oos])['Sharpe'] - M(rm[oos])['Sharpe']:+.4f} + EXP "
          f"{M(rm[oos])['Sharpe'] - mo_ew['Sharpe']:+.4f}   |   SEL(CANDrg) "
          f"{M(rg[oos])['Sharpe'] - mo_ew['Sharpe']:+.4f} + EXP "
          f"{M(rc[oos])['Sharpe'] - M(rg[oos])['Sharpe']:+.4f}")
        rows[-1]["note"] = f"OOS legs at n={n_c}"
    wf = pd.DataFrame(rows)
    dump(wf, "walkforward")
    P()
    g10 = gr[gr.bps == COST0]
    P(f"  KEEP paths over the {len(g10)} book-cells at 10 bps (all four books, all n): "
      f"4a {int(g10.pass4a.sum())}, 4b {int(g10.pass4b.sum())}, BOTH "
      f"{int((g10.pass4a & g10.pass4b).sum())}.  4b passers: "
      + ", ".join(f"{r.panel}/{r.book}{int(r.n) if r.n else ''}"
                  for _, r in g10[g10.pass4b].iterrows()))
    return wf


def main():
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    raw["SMALL439"] = sm[keep]
    n_dropped = len(sm.columns) - len(keep)
    panels = {k: Panel(k, v) for k, v in raw.items()}
    ok = gates(panels, n_dropped)
    cl = census()
    gr, lg, store = run_grid(panels)
    leg_summary(lg)
    rp = reprice(cl, lg)
    wf = walkforward(panels, gr, store)
    P()
    P("=" * 100)
    P("(F) VERDICT")
    P("=" * 100)
    x = lg[lg.bps == COST0]
    pos = x[x.PREMIUM > 0]
    P(f"  gates {'ALL PASS' if ok else 'FAILED'};  census {len(cl)} premium rows over "
      f"{cl.file.nunique()} files;  re-priceable {len(rp)};  fresh grid {len(x)} cells.")
    P(f"  fresh grid: {len(pos)}/{len(x)} positive premia, sign survives a matched control in "
      f"{int(pos.survives_EWMG.sum())} (MR-EWMG) / {int(pos.survives_CANDRG.sum())} (MR-CANDRG).")
    if len(rp):
        P(f"  record: {int(rp.survives_nom.sum())}/{len(rp)} re-priceable premia keep their "
          f"sign at the PUBLISHED (nominal) gross ({rp.survives_nom.mean():.1%}) and "
          f"{int(rp.survives_real.sum())}/{len(rp)} ({rp.survives_real.mean():.1%}) once the "
          f"REALISED de-grossing the nominal column cannot see is priced in; slope bracket "
          f"{int(rp.survives_bracket.sum())}/{len(rp)} ({rp.survives_bracket.mean():.1%}).")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
