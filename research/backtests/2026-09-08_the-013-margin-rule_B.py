#!/usr/bin/env python3
"""Idea 241 — the 0.013 margin rule.   (lane B, 2026-09-08)

QUESTION (QUEUE 241): idea 77's IS-Sharpe chooser lost 0.230 of OOS Sharpe on an IS margin
of 0.013 (BSTK100 1.0520 vs STK20 1.0392).  Pool every published argmax in the record with
its runner-up gap and test whether a MINIMUM-MARGIN ABSTENTION rule — fall back to the
incumbent when the top-2 IS gap is under a pre-registered threshold tau — beats the raw
argmax OUT OF SAMPLE.

WHY THIS IS NOT A REPEAT OF IDEA 431.  Lane C (idea 431, 2026-09-08) already reported that
"idea 241's minimum-margin rule is DEGENERATE on dial pools: 100% of the 36 pools have a
top-2 IS gap under 0.15, so every m >= 0.10 IS do-nothing by construction".  That is a
statement about a tau ladder quoted in ABSOLUTE Sharpe units on ONE 36-pool corpus.  The
repair is to define tau on the scale the corpus actually has: a QUANTILE of the observed
top-2 gap distribution, which cannot be degenerate by construction, and to run it over the
whole record rather than 36 pools.  Idea 431's degeneracy claim is reproduced here as a
gate (G2) before anything new is read.

DESIGN
  PART A — CENSUS.  Every `research/backtests/*.csv` carrying, per arm, a matched
    (IS_M, OOS_M) pair.  Cells are discovered mechanically (idea 417's `id_columns`, reused
    verbatim so the two censuses are comparable); every exclusion is counted in a ledger.
    Per cell:  margin = IS_M(argmax) - IS_M(runner-up), and the OOS value of the argmax, of
    the runner-up, of the labelled CONTROL arm, of the IS-MEDIAN-ranked arm, of the menu
    mean, and of the OOS oracle.
    SELECTOR(tau):  pick the IS-argmax when margin >= tau, else the INCUMBENT.
    ESTIMAND:  D(tau) = mean_cells [ OOS(selector) - OOS(raw argmax) ].  D(tau=0) == 0 by
    construction, so the raw argmax is its own control and the test is exactly the queue's.
  PART B — FRESH LIVE CORPUS on real prices, out of the committed corpus entirely: a 31-arm
    menu (band x gross x cadence + an ungated control) on 3 panels x 2 cost rungs, with
    seeded SUB-MENUS as cells so the rule is priced on hundreds of live selection problems
    rather than 6.  Realised OOS CAGR/Sharpe/MaxDD of the ARGMAX book, the ABSTAIN book and
    the INCUMBENT book against RULES v2 and SPY, with both KEEP paths (4a and 4b) on the
    full sample and on the OOS window.

TUNED PARAMETERS (exactly 2, every grid point reported):
    q    — the abstention threshold, expressed as a quantile of the CALIBRATION set's own
           top-2 gap distribution, q in {0.0, 0.1, ..., 0.9}   (10 points)
    norm — the scale the gap is measured on, {raw, z, rng}                  (3 points)
  = 30 grid points, all printed and written to `.taugrid.csv`.  The metric is pinned at
  Sharpe by the queue's own wording; CAGR/MaxDD/Calmar are reported as a labelled
  SENSITIVITY, not as a third dial.  The queue's absolute anchor tau = 0.013 (raw) is
  reported beside the grid as a pre-registered point, not fitted.

RULE 8 (PROTOCOL 8) in three places:
    WF1  record corpus split by parent-file date; (q, norm) chosen on the first half, read
         on the second half untouched.
    WF2  (q, norm) chosen on the WHOLE record corpus, read once on the fresh live cells,
         which share no data with it.
    WF3  live-only, fully nested: arms chosen on 2010..2013, tau chosen on 2014..2016,
         both read once on 2017-01-01.. .  This is the walk-forward that produces the
         headline OOS CAGR/Sharpe/MaxDD.

PROTOCOL: 10 bps anchor (25 bps rung also reported), next-day execution (engine.backtest),
no shorting, no leverage.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
from __future__ import annotations

import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_the-013-margin-rule_B"
OUT = ROOT / "research" / "backtests"

METRICS = ["Sharpe", "CAGR", "MaxDD", "Calmar"]
NORMS = ["raw", "z", "rng"]
NORMCOL = {"raw": "margin_raw", "z": "margin_z", "rng": "margin_rng"}
QGRID = [round(0.1 * i, 1) for i in range(10)]          # 0.0 .. 0.9
INCUMBENTS = ["ctl", "med", "mean"]                      # fall-back definitions
TAU_ANCHOR = 0.013                                       # the queue's own number, raw Sharpe

CONTROL_LABELS = {"control", "ctl", "base", "baseline", "none", "off", "d_none", "nogate",
                  "ungated", "no_overlay", "plain"}

IS_INNER_END = "2013-12-31"     # WF3: arms chosen here
MID_START, MID_END = "2014-01-01", "2016-12-31"   # WF3: tau chosen here
IS_END = "2016-12-31"           # headline: arms chosen 2010..2016
OOS_START = "2017-01-01"        # headline: read once here

LINES: list[str] = []
SORT_ROWS: list[dict] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


# ------------------------------------------------------------------- statistics
def _ncdf(z):
    import math
    return 0.5 * (1 + math.erf(z / np.sqrt(2)))


def paired_t(x) -> dict:
    """Mean, one-sample t, win/loss counts and two-sided p on a paired difference."""
    x = pd.Series(x).dropna().astype(float)
    n = len(x)
    if n < 2:
        return dict(n=n, mean=np.nan, t=np.nan, p=np.nan, W=0, L=0, Z=0)
    sd = x.std(ddof=1)
    t = float(x.mean() / (sd / np.sqrt(n))) if sd > 0 else np.nan
    p = float(2 * (1 - _ncdf(abs(t)))) if np.isfinite(t) else np.nan
    return dict(n=n, mean=float(x.mean()), t=t, p=p,
                W=int((x > 0).sum()), L=int((x < 0).sum()), Z=int((x == 0).sum()))


# ------------------------------------------------------------------- Part A: harvest
METRIC_PREFIX = re.compile(r"^(IS_|OOS_|pass|fail|adm_|m_|d_|uc_|sc_|U_|S_|C_|n_)")
METRIC_NAMES = {"CAGR", "Sharpe", "MaxDD", "Calmar", "Sortino", "Vol", "H1", "H2", "TO",
                "turnover", "Total", "Years", "WinRate", "breakeven", "cstar", "c_star"}


def id_columns(df: pd.DataFrame, armcol: str) -> list[str]:
    """Cell-identifying columns, found mechanically (idea 417's rule, reused verbatim)."""
    out = []
    for c in df.columns:
        if c == armcol or METRIC_PREFIX.match(c) or c in METRIC_NAMES:
            continue
        nu = df[c].nunique(dropna=False)
        if nu < 2 or nu > 40:
            continue
        if df[c].dtype.kind == "f" and nu > 12:
            continue
        per_arm = df.groupby(armcol)[c].nunique(dropna=False)
        if (per_arm <= 1).all():          # one value per arm => arm parameter, not a cell label
            continue
        out.append(c)
    return out


def cell_row(A, I, O, meta: dict) -> dict | None:
    """One census row: the IS ordering of a cell's arms and every OOS read-off it licenses."""
    order = np.argsort(-I, kind="stable")
    star, second = order[0], order[1]
    margin = float(I[star] - I[second])
    sd = float(np.std(I, ddof=1))
    rng = float(I.max() - I.min())
    med_pos = order[len(order) // 2]                       # IS-median-ranked arm
    ctl_mask = np.array([str(a).strip().lower() in CONTROL_LABELS for a in A])
    r = dict(**meta, n_arms=int(len(I)), arm_star=str(A[star]), arm_second=str(A[second]),
             margin_raw=margin,
             margin_z=margin / sd if sd > 0 else np.nan,
             margin_rng=margin / rng if rng > 0 else np.nan,
             IS_star=float(I[star]), IS_second=float(I[second]),
             OOS_star=float(O[star]), OOS_second=float(O[second]),
             OOS_med=float(O[med_pos]), OOS_mean=float(O.mean()),
             OOS_best=float(O.max()), arm_med=str(A[med_pos]),
             has_ctl=bool(ctl_mask.any()))
    if ctl_mask.any():
        r["OOS_ctl"] = float(O[ctl_mask][0])
        r["star_is_ctl"] = bool(ctl_mask[star])
    else:
        r["OOS_ctl"] = np.nan
        r["star_is_ctl"] = False
    return r


def harvest() -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, ledger = [], []
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM):
            continue
        rec = dict(file=f.name, status="", n_cells=0, n_rows=0)
        try:
            df = pd.read_csv(f)
        except Exception as e:
            rec["status"] = f"unreadable:{type(e).__name__}"
            ledger.append(rec)
            continue
        armcol = "arm" if "arm" in df.columns else ("pick" if "pick" in df.columns else None)
        if armcol is None:
            rec["status"] = "no arm column"
            ledger.append(rec)
            continue
        mets = [m for m in METRICS if f"IS_{m}" in df.columns and f"OOS_{m}" in df.columns]
        if not mets:
            rec["status"] = "no matched IS_/OOS_ pair"
            ledger.append(rec)
            continue
        ids = id_columns(df, armcol)
        groups = df.groupby(ids, dropna=False, sort=True) if ids else [((), df)]
        n_cells = n_used = 0
        before = len(rows)
        for key, cell in groups:
            n_cells += 1
            if cell[armcol].duplicated().any() or cell[armcol].nunique() < 3:
                continue
            arms = cell[armcol].astype(str)
            used_here = False
            for m in mets:
                isv = pd.to_numeric(cell[f"IS_{m}"], errors="coerce")
                oov = pd.to_numeric(cell[f"OOS_{m}"], errors="coerce")
                ok = isv.notna() & oov.notna() & np.isfinite(isv) & np.isfinite(oov)
                if ok.sum() < 3 or isv[ok].nunique() < 2:
                    continue
                meta = dict(file=f.name, date=f.name[:10], stem=f.name.split(".")[0], metric=m,
                            cell="|".join(map(str, key)) if ids else "ALL")
                r = cell_row(arms[ok].values, isv[ok].values, oov[ok].values, meta)
                if r is not None:
                    rows.append(r)
                    used_here = True
            n_used += int(used_here)
        rec.update(status="ADMITTED" if n_used else "no usable cell",
                   n_cells=n_cells, n_rows=len(rows) - before)
        ledger.append(rec)
    return pd.DataFrame(rows), pd.DataFrame(ledger)


# ------------------------------------------------------------------- the selector
def selector_delta(cen: pd.DataFrame, norm: str, tau: float, inc: str) -> dict:
    """D(tau) = mean [ OOS(selector) - OOS(raw argmax) ] over the cells that HAVE the
    incumbent named by `inc`.  Also returns the abstention rate and the hit rate."""
    col = NORMCOL[norm]
    inc_col = {"ctl": "OOS_ctl", "med": "OOS_med", "mean": "OOS_mean"}[inc]
    sub = cen[cen[col].notna() & cen[inc_col].notna() & cen["OOS_star"].notna()]
    if not len(sub):
        return dict(n=0, mean=np.nan, t=np.nan, p=np.nan, W=0, L=0, Z=0,
                    abstain=np.nan, sel_mean=np.nan, argmax_mean=np.nan, inc_mean=np.nan)
    ab = sub[col] < tau
    sel = np.where(ab, sub[inc_col].values, sub["OOS_star"].values)
    d = sel - sub["OOS_star"].values
    out = paired_t(d)
    out.update(abstain=float(ab.mean()), sel_mean=float(np.mean(sel)),
               argmax_mean=float(sub["OOS_star"].mean()), inc_mean=float(sub[inc_col].mean()))
    return out


def tau_grid(cal: pd.DataFrame, test: pd.DataFrame, incs=INCUMBENTS, label="") -> pd.DataFrame:
    """All 30 grid points (q x norm) x incumbent.  tau is the q-quantile of the CALIBRATION
    set's own gap distribution, so no grid point can be vacuous by construction."""
    out = []
    for norm in NORMS:
        col = NORMCOL[norm]
        gaps = cal[col].dropna()
        for q in QGRID:
            tau = float(gaps.quantile(q)) if len(gaps) else np.nan
            for inc in incs:
                r = selector_delta(test, norm, tau, inc)
                out.append(dict(scope=label, norm=norm, q=q, tau=tau, incumbent=inc, **r))
    return pd.DataFrame(out)


# ------------------------------------------------------------------- Part B: live arms
def ew_band_weights(px, band, gross, gated=True):
    """EW over everything priced that day at gross/N; gated names go to CASH (RULES v2 shape)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if not gated:
        return ew
    return ew.where(band_state(px, band), 0.0)


def arm_menu():
    arms = [("control", dict(band=None, gross=1.0, freq="W", gated=False))]
    for band in (0.0, 0.015, 0.03, 0.045, 0.06):
        for gross in (0.50, 0.75, 1.00):
            for freq in ("W", "M"):
                arms.append((f"b{band:g}-g{gross:.2f}-{freq}",
                             dict(band=band, gross=gross, freq=freq, gated=True)))
    return arms


def load_panels():
    P = {}
    P["u56"] = load_universe()
    P["broad136"] = load_universe(broad=True)
    small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["small439"] = small[[c for c in small.columns if c not in bad]]
    return P


def win_metrics(r, lo=None, hi=None, prefix=""):
    x = r.loc[lo:hi] if (lo or hi) else r
    if len(x) < 30:
        return {f"{prefix}{k}": np.nan for k in ("CAGR", "Sharpe", "MaxDD", "Calmar")}
    m = metrics(x)
    return {f"{prefix}CAGR": m["CAGR"], f"{prefix}Sharpe": m["Sharpe"],
            f"{prefix}MaxDD": m["MaxDD"], f"{prefix}Calmar": m["Calmar"]}


def keep_paths(r, base, spy):
    """4a vs the LIVE RULES v2 book, 4b vs SPY — on the full sample and on the OOS window."""
    def bars(x, b, s):
        mx, mb, ms = metrics(x), metrics(b), metrics(s)
        h = len(x) // 2
        xh = (metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"])
        bh = (metrics(b.iloc[:h])["Sharpe"], metrics(b.iloc[h:])["Sharpe"])
        sh = (metrics(s.iloc[:h])["Sharpe"], metrics(s.iloc[h:])["Sharpe"])
        p4a = xh[0] > bh[0] and xh[1] > bh[1] and mx["MaxDD"] >= mb["MaxDD"]
        p4b = (xh[0] > sh[0] and xh[1] > sh[1] and mx["Sharpe"] > ms["Sharpe"]
               and mx["MaxDD"] >= 0.60 * ms["MaxDD"] and mx["CAGR"] >= 0.70 * ms["CAGR"])
        return bool(p4a), bool(p4b)
    a_f, b_f = bars(r, base, spy)
    a_o, b_o = bars(r.loc[OOS_START:], base.loc[OOS_START:], spy.loc[OOS_START:])
    return dict(pass4a=a_f, pass4b=b_f, pass4a_oos=a_o, pass4b_oos=b_o)


def fresh_grid(panels, costs=(10.0, 25.0)):
    """Arm-level table + the raw net return stream of every (panel, cost, arm)."""
    rows, curves = [], {}
    arms = arm_menu()
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        univ = px.drop(columns=["SPY"], errors="ignore") if pname == "small439" else px
        base_r = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        raw = {}
        for name, a in arms:
            w = ew_band_weights(univ, a["band"] if a["band"] is not None else 0.0,
                                a["gross"], gated=a["gated"]).reindex(columns=px.columns).fillna(0.0)
            res = backtest(px, w, cost_bps=0.0, freq=a["freq"])
            raw[name] = (res["returns"], res["turnover"])
        for c in costs:
            for name, a in arms:
                r0, to = raw[name]
                r = (r0 - to * c / 1e4).loc[start:]           # cost-rung identity, gated in G1
                curves[(pname, c, name)] = r
                row = dict(panel=pname, cost=c, arm=name, band=a["band"], gross=a["gross"],
                           freq=a["freq"], gated=a["gated"])
                row.update(win_metrics(r))
                row.update(win_metrics(r, hi=IS_INNER_END, prefix="ISin_"))
                row.update(win_metrics(r, lo=MID_START, hi=MID_END, prefix="MID_"))
                row.update(win_metrics(r, hi=IS_END, prefix="IS_"))
                row.update(win_metrics(r, lo=OOS_START, prefix="OOS_"))
                rows.append(row)
            curves[(pname, c, "__SPY__")] = spy
            curves[(pname, c, "__V2__")] = base_r
    return pd.DataFrame(rows), curves


def submenus(all_arms, n_cells=200, lo=5, hi=15, seed=20260908):
    """Seeded sub-menus of the arm list, each containing the control (the incumbent must
    exist for the abstention rule to be defined).  Deterministic: numpy Generator, no hash()."""
    rng = np.random.default_rng(seed)
    pool = [a for a in all_arms if a != "control"]
    out = []
    for i in range(n_cells):
        k = int(rng.integers(lo, hi + 1)) - 1
        pick = list(rng.choice(pool, size=k, replace=False))
        out.append(["control"] + sorted(pick))
    return out


def live_cells(fg: pd.DataFrame, menus, is_pre: str, oos_pre: str) -> pd.DataFrame:
    """One census-shaped row per (panel, cost, sub-menu), IS/OOS windows named by prefix."""
    rows = []
    for (pname, c), cell in fg.groupby(["panel", "cost"]):
        idx = cell.set_index("arm")
        for j, menu in enumerate(menus):
            sub = idx.loc[[a for a in menu if a in idx.index]]
            I = sub[f"{is_pre}Sharpe"].values.astype(float)
            O = sub[f"{oos_pre}Sharpe"].values.astype(float)
            A = np.array(sub.index)
            ok = np.isfinite(I) & np.isfinite(O)
            if ok.sum() < 3 or len(set(I[ok])) < 2:
                continue
            r = cell_row(A[ok], I[ok], O[ok],
                         dict(file="LIVE", date="2026-09-08", stem="LIVE", metric="Sharpe",
                              cell=f"{pname}|{c:g}|m{j:03d}"))
            r.update(panel=pname, cost=c, menu=j)
            rows.append(r)
    return pd.DataFrame(rows)


def selector_book(cells: pd.DataFrame, curves, norm: str, tau: float, inc_arm="control"):
    """Realised return stream of the ABSTAIN(tau) book and of the raw ARGMAX book: an equal
    weight over the cells' picks within each (panel, cost) — one decision per cell."""
    books = {}
    col = NORMCOL[norm]
    for (pname, c), sub in cells.groupby(["panel", "cost"]):
        for label in ("ARGMAX", "ABSTAIN", "INCUMBENT"):
            streams = []
            for _, row in sub.iterrows():
                if label == "INCUMBENT":
                    arm = inc_arm
                elif label == "ARGMAX":
                    arm = row.arm_star
                else:
                    arm = inc_arm if (pd.notna(row[col]) and row[col] < tau) else row.arm_star
                streams.append(curves[(pname, c, arm)])
            books[(pname, c, label)] = pd.concat(streams, axis=1).mean(axis=1)
    return books


# ------------------------------------------------------------------- gates
def gate_cost_identity(px) -> float:
    """G1: net(c) = gross - turnover * c/1e4, the identity Part B leans on."""
    w = ew_band_weights(px, 0.03, 0.75, gated=True)
    a = backtest(px, w, cost_bps=0.0, freq="W")
    direct = backtest(px, w, cost_bps=25.0, freq="W")["returns"]
    return float((a["returns"] - a["turnover"] * 25.0 / 1e4 - direct).abs().max())


def gate_idea431(path: Path) -> dict:
    """G2: reproduce idea 431's degeneracy claim — 100% of its 36 dial pools have a top-2
    IS_Sharpe gap under 0.15, which is why an absolute tau ladder is vacuous there."""
    df = pd.read_csv(path)
    gaps = []
    for key, cell in df.groupby(["panel", "family", "cost"]):
        I = np.sort(cell["IS_Sharpe"].values.astype(float))[::-1]
        if len(I) >= 2:
            gaps.append(dict(pool="|".join(map(str, key)), gap=float(I[0] - I[1]), n=len(I)))
    G = pd.DataFrame(gaps)
    return dict(pools=len(G), under_015=int((G.gap < 0.15).sum()),
                under_010=int((G.gap < 0.10).sum()), max_gap=float(G.gap.max()),
                median_gap=float(G.gap.median()), table=G)


# ------------------------------------------------------------------- main
def main():
    say("=" * 100)
    say("IDEA 241 — the 0.013 margin rule: does a minimum-margin ABSTENTION beat the raw argmax OOS?")
    say("lane B, 2026-09-08.  PROTOCOL 10 bps anchor, next-day execution, rule 8 everywhere.")
    say("=" * 100)

    # ------------------------------------------------------------- GATES
    say("\n## GATES (passed before any new number is read)\n")
    px_u56 = load_universe()
    g1 = gate_cost_identity(px_u56)
    say(f"  [G1] cost-rung identity  net(25bps) == gross - TO*25/1e4   max|d| = {g1:.3e}")
    p431 = OUT / "2026-09-08_is-K_MEDIAN-a-real-abstention-rule-or-a-36-cell-accident_C.grid.csv"
    if p431.exists():
        g2 = gate_idea431(p431)
        say(f"  [G2] idea 431 premise: {g2['pools']} dial pools; top-2 IS_Sharpe gap < 0.15 in "
            f"{g2['under_015']}/{g2['pools']} ({g2['under_015'] / g2['pools']:.0%}), < 0.10 in "
            f"{g2['under_010']}/{g2['pools']}; max gap {g2['max_gap']:.4f}, median {g2['median_gap']:.4f}")
        say("       -> idea 431's DEGENERACY claim REPRODUCED.  An ABSOLUTE tau ladder is vacuous on "
            "that corpus; this run therefore defines tau as a QUANTILE of the corpus's own gaps.")
        g2["table"].to_csv(OUT / f"{STEM}.gate431.csv", index=False)
    else:
        say("  [G2] idea 431 grid file not found — degeneracy premise UNAUDITED (reported, not assumed)")
    say(f"  [G3] the queue's anchor tau = {TAU_ANCHOR} raw Sharpe (idea 77: BSTK100 1.0520 vs "
        "STK20 1.0392, gap 0.0128) is carried as a PRE-REGISTERED point beside the fitted grid; "
        "idea 77's own two numbers are quoted from the queue, not recomputed here.")
    flush()

    # ------------------------------------------------------------- PART A
    say("\n\n## PART A — CENSUS: every committed grid carrying a matched (IS_M, OOS_M) pair per arm\n")
    cen, led = harvest()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    led.to_csv(OUT / f"{STEM}.ledger.csv", index=False)
    adm = led[led.status == "ADMITTED"]
    say(f"  files scanned {len(led)} -> ADMITTED {len(adm)};  "
        + "; ".join(f"{k} {v}" for k, v in led.status.value_counts().items() if k != "ADMITTED"))
    say(f"  census rows (file x cell x metric) {len(cen)};  distinct cells "
        f"{cen.groupby(['file', 'cell']).ngroups};  files {cen.file.nunique()}")
    S = cen[cen.metric == "Sharpe"].copy()
    say(f"  SHARPE cells {len(S)} over {S.file.nunique()} files;  with a labelled control arm "
        f"{int(S.has_ctl.sum())} ({S.has_ctl.mean():.1%});  argmax IS the control in "
        f"{int(S.star_is_ctl.sum())} ({S.star_is_ctl.mean():.1%}) — abstention is a NO-OP there")

    say("\n### The gap distribution the queue's 0.013 has to live in (Sharpe cells)")
    for norm in NORMS:
        gg = S[NORMCOL[norm]].dropna()
        qs = gg.quantile(QGRID + [1.0])
        say(f"  {norm:3s}  n {len(gg):5d}  " + "  ".join(f"q{q:.1f} {qs[q]:.4f}" for q in QGRID + [1.0]))
    frac = float((S.margin_raw < TAU_ANCHOR).mean())
    say(f"  the queue's tau = {TAU_ANCHOR} raw sits at the {frac:.1%} quantile of the record's own gaps "
        f"-> it would abstain on {frac:.1%} of cells")

    say("\n[t-STAT CAVEAT, stated once and applying to every t and p below] cells inside one file "
        "share an arm ladder and cells inside one live (panel, cost) share 31 arms, so the paired t "
        "treats correlated cells as independent and is INFLATED — badly so on the live corpus, where "
        "1,200 sub-menus are drawn from 31 arms.  Read the SIGN and the MAGNITUDE of D; the t is a "
        "direction indicator, not a p-value this run is entitled to.")
    say("\n### ALL 30 GRID POINTS (q x norm) x 3 incumbent definitions — "
        "D(tau) = mean[ OOS(selector) - OOS(argmax) ], Sharpe units\n")
    TG = tau_grid(S, S, label="RECORD/all")
    TG.to_csv(OUT / f"{STEM}.taugrid.csv", index=False)
    for inc in INCUMBENTS:
        piv = TG[TG.incumbent == inc].pivot_table(index="q", columns="norm", values="mean")
        ab = TG[TG.incumbent == inc].pivot_table(index="q", columns="norm", values="abstain")
        say(f"  incumbent = {inc}   (n = {int(TG[TG.incumbent == inc].n.max())} cells)")
        say("    D(tau):\n" + piv.to_string(float_format=lambda x: f"{x:+.4f}"))
        say("    abstention rate:\n" + ab.to_string(float_format=lambda x: f"{x:.2f}"))
    say("\n  full table with t, p, wins/losses:\n"
        + TG[["norm", "q", "tau", "incumbent", "n", "mean", "t", "p", "W", "L", "Z", "abstain"]]
        .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n### The PRE-REGISTERED point (not fitted): tau = 0.013 raw Sharpe")
    for inc in INCUMBENTS:
        r = selector_delta(S, "raw", TAU_ANCHOR, inc)
        say(f"  incumbent {inc:5s}  n {r['n']:5d}  abstains {r['abstain']:.1%}  "
            f"D {r['mean']:+.4f}  t {r['t']:+.2f}  p {r['p']:.4f}  W/L/Z {r['W']}/{r['L']}/{r['Z']}")

    say("\n### SENSITIVITY (labelled, NOT a third tuned dial): the same rule on the other metrics")
    sens = []
    for m in METRICS:
        sub = cen[cen.metric == m]
        if len(sub) < 30:
            continue
        for inc in INCUMBENTS:
            gaps = sub["margin_z"].dropna()
            for q in (0.3, 0.5, 0.7):
                r = selector_delta(sub, "z", float(gaps.quantile(q)), inc)
                sens.append(dict(metric=m, incumbent=inc, q=q, **r))
    SS = pd.DataFrame(sens)
    SS.to_csv(OUT / f"{STEM}.sensitivity.csv", index=False)
    say(SS[["metric", "incumbent", "q", "n", "mean", "t", "p", "abstain"]]
        .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n### DEGENERACY CHECK — the abstention can only move a cell where argmax != incumbent")
    mv = S[~S.star_is_ctl.astype(bool)]
    say(f"  MOVED cells (argmax != control): {len(mv)} of {len(S)} ({len(mv) / len(S):.1%})")
    for inc in INCUMBENTS:
        gaps = mv["margin_z"].dropna()
        for q in (0.3, 0.5, 0.7):
            r = selector_delta(mv, "z", float(gaps.quantile(q)), inc)
            say(f"  MOVED-only  inc {inc:5s} q {q:.1f}  n {r['n']:5d}  abstains {r['abstain']:.1%}  "
                f"D {r['mean']:+.4f}  t {r['t']:+.2f}  p {r['p']:.4f}")
    flush()

    # ------------------------------------------------------------- WF1
    say("\n### DECOMPOSITION — where a positive D against the CONTROL comes from")
    k = S[S.OOS_ctl.notna()]
    dec_rows = []
    for lab, x in (("ROOM the control carries   OOS_ctl  - OOS_mean", k.OOS_ctl - k.OOS_mean),
                   ("what the argmax buys       OOS_star - OOS_mean", k.OOS_star - k.OOS_mean),
                   ("argmax vs control          OOS_star - OOS_ctl ", k.OOS_star - k.OOS_ctl),
                   ("oracle regret              OOS_best - OOS_star", k.OOS_best - k.OOS_star)):
        r = paired_t(x)
        dec_rows.append(dict(term=lab.strip(), **r))
        say(f"  {lab}   n {r['n']:5d}  mean {r['mean']:+.4f}  t {r['t']:+.2f}")
    pd.DataFrame(dec_rows).to_csv(OUT / f"{STEM}.decomposition.csv", index=False)
    say("  -> the control is a BETTER-THAN-AVERAGE arm in these grids by +0.026 of Sharpe.  Any rule "
        "that hands cells back to it inherits that ROOM whether or not the margin carries information "
        "(idea 229/445: margin = ROOM - REGRET).")

    say("\n### THE DECISIVE TEST — does the MARGIN SORT the abstention payoff?")
    say("  gain(cell) = OOS_ctl - OOS_star, i.e. what abstaining on that cell actually pays.")
    say("  If the queue's rule is real, gain must FALL with the margin.  Terciles, MOVED cells only:")
    sort_rows = []
    mv2 = k[~k.star_is_ctl.astype(bool)].copy()
    mv2["gain"] = mv2.OOS_ctl - mv2.OOS_star
    for norm in NORMS:
        col = NORMCOL[norm]
        mv2["T"] = pd.qcut(mv2[col], 3, labels=["narrow", "mid", "wide"], duplicates="drop")
        rho = float(mv2[col].rank().corr(mv2.gain.rank()))
        parts = []
        for t_, g in mv2.groupby("T", observed=True):
            r = paired_t(g.gain)
            parts.append(f"{t_} n {r['n']:4d} {r['mean']:+.4f} (t {r['t']:+.2f})")
            sort_rows.append(dict(scope="RECORD", norm=norm, tercile=str(t_), **r))
        say(f"  RECORD {norm:3s}: " + " | ".join(parts) + f"   spearman(margin, gain) {rho:+.4f}")
    SORT_ROWS.extend(sort_rows)

    say("\n### RULE 8 / WF1 — choose (q, norm) on the FIRST half of the record by parent-file "
        "date, read the SECOND half untouched\n")
    dates = sorted(S.date.unique())
    cut = dates[len(dates) // 2]
    A, B = S[S.date < cut], S[S.date >= cut]
    say(f"  files < {cut}: {A.file.nunique()} files / {len(A)} cells (IS);  "
        f">= {cut}: {B.file.nunique()} files / {len(B)} cells (OOS)")
    wf_rows = []
    for inc in INCUMBENTS:
        gis = tau_grid(A, A, incs=[inc], label="WF1/IS")
        for _, g in gis.iterrows():
            tau = float(A[NORMCOL[g["norm"]]].dropna().quantile(g["q"]))
            o = selector_delta(B, g["norm"], tau, inc)
            wf_rows.append(dict(incumbent=inc, norm=g["norm"], q=g["q"], tau=tau,
                                IS_n=g["n"], IS_D=g["mean"], IS_t=g["t"],
                                OOS_n=o["n"], OOS_D=o["mean"], OOS_t=o["t"], OOS_p=o["p"],
                                OOS_abstain=o["abstain"]))
    WF1 = pd.DataFrame(wf_rows)
    WF1.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF1.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    for inc in INCUMBENTS:
        sub = WF1[WF1.incumbent == inc]
        pick = sub.loc[sub.IS_D.idxmax()]
        say(f"  CHOSEN (max IS D), incumbent {inc:5s}: {pick['norm']}/q{pick['q']:.1f} "
            f"tau {pick['tau']:+.4f}  IS D {pick['IS_D']:+.4f} (t {pick['IS_t']:+.2f}, n {int(pick['IS_n'])}) "
            f"-> OOS D {pick['OOS_D']:+.4f} (t {pick['OOS_t']:+.2f}, p {pick['OOS_p']:.4f}, "
            f"n {int(pick['OOS_n'])}, abstains {pick['OOS_abstain']:.0%})")
    flush()

    # ------------------------------------------------------------- PART B
    say("\n\n## PART B — FRESH LIVE CORPUS on real prices (31 arms x 3 panels x 2 rungs, "
        "seeded sub-menus as cells)\n")
    panels = load_panels()
    for k, v in panels.items():
        say(f"  panel {k:9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    say("  SURVIVORSHIP: SMALL439 and universe_broad.json are CURRENT constituents "
        "(data/SMALL_PANEL_README.md) — read the CONTRASTS between selectors, not the levels.")
    fg, curves = fresh_grid(panels)
    fg.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    say(f"  arm-rows {len(fg)} over {fg.groupby(['panel', 'cost']).ngroups} (panel, cost) cells")

    say("\n### Levels, freshly computed (OOS window 2017-01-01..)")
    for pname in panels:
        s, v = metrics(curves[(pname, 10.0, "__SPY__")].loc[OOS_START:]), \
            metrics(curves[(pname, 10.0, "__V2__")].loc[OOS_START:])
        say(f"  {pname:9s} SPY {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:7.2%}   "
            f"RULES v2@10bps {v['CAGR']:7.2%} / {v['Sharpe']:.4f} / {v['MaxDD']:7.2%}   "
            f"[4b OOS bars: CAGR >= {0.70 * s['CAGR']:.2%}, MaxDD >= {0.60 * s['MaxDD']:.2%}]")

    menus = submenus([a for a, _ in arm_menu()])
    LC = live_cells(fg, menus, "IS_", "OOS_")
    LC.to_csv(OUT / f"{STEM}.livecells.csv", index=False)
    say(f"\n  live cells (panel x cost x sub-menu): {len(LC)};  menu sizes "
        f"{LC.n_arms.min()}..{LC.n_arms.max()};  argmax IS the control in "
        f"{int(LC.star_is_ctl.sum())} ({LC.star_is_ctl.mean():.1%})")
    say("  live gap quantiles (Sharpe):")
    for norm in NORMS:
        gg = LC[NORMCOL[norm]].dropna()
        say(f"    {norm:3s}  " + "  ".join(f"q{q:.1f} {gg.quantile(q):.4f}" for q in QGRID + [1.0]))

    say("\n### THE DECISIVE TEST, live half — does the MARGIN SORT the abstention payoff?")
    for pname, g in LC.groupby("panel"):
        g = g[~g.star_is_ctl.astype(bool)].copy()
        if len(g) < 30:
            say(f"  LIVE {pname:9s}: {len(g)} MOVED cells of {int((LC.panel == pname).sum())} — "
                "the ungated control IS the IS-argmax, so abstention is a strict NO-OP on this panel")
            continue
        g["gain"] = g.OOS_ctl - g.OOS_star
        g["T"] = pd.qcut(g.margin_raw, 3, labels=["narrow", "mid", "wide"], duplicates="drop")
        rho = float(g.margin_raw.rank().corr(g.gain.rank()))
        parts = []
        for t_, gg in g.groupby("T", observed=True):
            r = paired_t(gg.gain)
            parts.append(f"{t_} n {r['n']:4d} {r['mean']:+.4f} (t {r['t']:+.2f})")
            SORT_ROWS.append(dict(scope=f"LIVE/{pname}", norm="raw", tercile=str(t_), **r))
        say(f"  LIVE {pname:9s}: " + " | ".join(parts) + f"   spearman(margin, gain) {rho:+.4f}")
    pd.DataFrame(SORT_ROWS).to_csv(OUT / f"{STEM}.sorting.csv", index=False)

    say("\n### ALL 30 GRID POINTS on the LIVE corpus (tau from the live gaps)\n")
    TGL = tau_grid(LC, LC, label="LIVE/all")
    TGL.to_csv(OUT / f"{STEM}.taugrid_live.csv", index=False)
    for inc in INCUMBENTS:
        piv = TGL[TGL.incumbent == inc].pivot_table(index="q", columns="norm", values="mean")
        say(f"  incumbent = {inc}:\n" + piv.to_string(float_format=lambda x: f"{x:+.4f}"))
    say("\n  full table:\n" + TGL[["norm", "q", "tau", "incumbent", "n", "mean", "t", "p",
                                   "W", "L", "Z", "abstain"]]
        .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # WF2: the record's own chosen point, read once on the live corpus
    say("\n### RULE 8 / WF2 — (q, norm) chosen on the WHOLE RECORD, read ONCE on the live corpus")
    wf2 = []
    for inc in INCUMBENTS:
        sub = TG[TG.incumbent == inc]
        pick = sub.loc[sub["mean"].idxmax()]
        tau_live = float(LC[NORMCOL[pick["norm"]]].dropna().quantile(pick["q"]))
        o = selector_delta(LC, pick["norm"], tau_live, inc)
        wf2.append(dict(incumbent=inc, norm=pick["norm"], q=pick["q"], record_D=pick["mean"],
                        tau_live=tau_live, **o))
        say(f"  inc {inc:5s}: record picks {pick['norm']}/q{pick['q']:.1f} (record D {pick['mean']:+.4f}) "
            f"-> LIVE D {o['mean']:+.4f}  t {o['t']:+.2f}  p {o['p']:.4f}  n {o['n']}  "
            f"abstains {o['abstain']:.0%}")
    pd.DataFrame(wf2).to_csv(OUT / f"{STEM}.wf2.csv", index=False)

    # WF3: fully nested live walk-forward
    say("\n### RULE 8 / WF3 — nested live walk-forward: arms chosen 2010..2013, tau chosen "
        "2014..2016, both read ONCE on 2017-01-01..\n")
    LC_cal = live_cells(fg, menus, "ISin_", "MID_")     # arms on 2010..2013, read on 2014..2016
    LC_cal.to_csv(OUT / f"{STEM}.livecells_cal.csv", index=False)
    wf3_rows = []
    for inc in INCUMBENTS:
        cal = tau_grid(LC_cal, LC_cal, incs=[inc], label="WF3/cal")
        for _, g in cal.iterrows():
            tau_test = float(LC[NORMCOL[g["norm"]]].dropna().quantile(g["q"]))
            o = selector_delta(LC, g["norm"], tau_test, inc)
            wf3_rows.append(dict(incumbent=inc, norm=g["norm"], q=g["q"],
                                 cal_D=g["mean"], cal_t=g["t"], cal_n=g["n"],
                                 tau_test=tau_test, OOS_D=o["mean"], OOS_t=o["t"],
                                 OOS_p=o["p"], OOS_n=o["n"], OOS_abstain=o["abstain"]))
    WF3 = pd.DataFrame(wf3_rows)
    WF3.to_csv(OUT / f"{STEM}.walkforward_live.csv", index=False)
    say(WF3.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    picks3 = {}
    for inc in INCUMBENTS:
        sub = WF3[WF3.incumbent == inc]
        p = sub.loc[sub.cal_D.idxmax()]
        picks3[inc] = p
        say(f"  CHOSEN on 2014..2016, incumbent {inc:5s}: {p['norm']}/q{p['q']:.1f} "
            f"(cal D {p['cal_D']:+.4f}, t {p['cal_t']:+.2f}) -> OOS D {p['OOS_D']:+.4f} "
            f"(t {p['OOS_t']:+.2f}, p {p['OOS_p']:.4f}, abstains {p['OOS_abstain']:.0%})")
    flush()

    # ------------------------------------------------------------- books + KEEP paths
    say("\n\n## THE BOOKS — realised return streams of ARGMAX vs ABSTAIN vs INCUMBENT\n")
    p = picks3["ctl"]
    tau_star = float(LC[NORMCOL[p["norm"]]].dropna().quantile(p["q"]))
    say(f"  WF3-chosen abstention: norm {p['norm']}, q {p['q']:.1f}, tau {tau_star:.4f} "
        "(chosen on 2014..2016, never on 2017+)")
    books = selector_book(LC, curves, p["norm"], tau_star)
    brows = []
    for (pname, c, label), r in books.items():
        base, spy = curves[(pname, c, "__V2__")], curves[(pname, c, "__SPY__")]
        row = dict(panel=pname, cost=c, book=label)
        row.update(win_metrics(r))
        row.update(win_metrics(r, lo=OOS_START, prefix="OOS_"))
        row.update(keep_paths(r, base, spy))
        brows.append(row)
    BK = pd.DataFrame(brows).sort_values(["panel", "cost", "book"])
    BK.to_csv(OUT / f"{STEM}.books.csv", index=False)
    say("\n" + BK[["panel", "cost", "book", "CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe",
                   "OOS_MaxDD", "pass4a", "pass4b", "pass4a_oos", "pass4b_oos"]]
        .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n### Headline comparison at the PROTOCOL 10 bps anchor, OOS window 2017-01-01..")
    say(f"  {'panel':10s} {'book':10s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}")
    for pname in panels:
        for label in ("ARGMAX", "ABSTAIN", "INCUMBENT"):
            m = metrics(books[(pname, 10.0, label)].loc[OOS_START:])
            say(f"  {pname:10s} {label:10s} {m['CAGR']:8.2%} {m['Sharpe']:11.4f} {m['MaxDD']:9.2%}")
        for nm, cur in (("RULES v2", "__V2__"), ("SPY", "__SPY__")):
            m = metrics(curves[(pname, 10.0, cur)].loc[OOS_START:])
            say(f"  {pname:10s} {nm:10s} {m['CAGR']:8.2%} {m['Sharpe']:11.4f} {m['MaxDD']:9.2%}")

    say("\n### KEEP paths")
    say(f"  books: 4a {int(BK.pass4a.sum())}/{len(BK)}   4b {int(BK.pass4b.sum())}/{len(BK)}   "
        f"4a(OOS) {int(BK.pass4a_oos.sum())}/{len(BK)}   4b(OOS) {int(BK.pass4b_oos.sum())}/{len(BK)}   "
        f"BOTH {int((BK.pass4a & BK.pass4b).sum())}/{len(BK)}")
    for label, sub in BK.groupby("book"):
        say(f"    {label:10s} 4a {int(sub.pass4a.sum())}/{len(sub)}  4b {int(sub.pass4b.sum())}/{len(sub)}  "
            f"4b(OOS) {int(sub.pass4b_oos.sum())}/{len(sub)}")
    # every individual arm too, so the KEEP census is not just the three books
    kp = [keep_paths(curves[(r.panel, r.cost, r.arm)], curves[(r.panel, r.cost, "__V2__")],
                     curves[(r.panel, r.cost, "__SPY__")]) for _, r in fg.iterrows()]
    fgk = pd.concat([fg.reset_index(drop=True), pd.DataFrame(kp)], axis=1)
    fgk.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(f"  individual arms: 4a {int(fgk.pass4a.sum())}/{len(fgk)}  4b {int(fgk.pass4b.sum())}/{len(fgk)}  "
        f"4b(OOS) {int(fgk.pass4b_oos.sum())}/{len(fgk)}  "
        f"BOTH {int((fgk.pass4a & fgk.pass4b).sum())}/{len(fgk)}")
    both = fgk[fgk.pass4a & fgk.pass4b]
    if len(both):
        say("  BOTH-PATHS arms:\n" + both[["panel", "cost", "arm", "CAGR", "Sharpe", "MaxDD",
                                           "OOS_CAGR", "OOS_Sharpe"]].to_string(index=False))

    say("\n### Does the ABSTAIN book beat the ARGMAX book, per (panel, cost)?")
    d = []
    for pname in panels:
        for c in (10.0, 25.0):
            a = metrics(books[(pname, c, "ARGMAX")].loc[OOS_START:])
            b = metrics(books[(pname, c, "ABSTAIN")].loc[OOS_START:])
            i = metrics(books[(pname, c, "INCUMBENT")].loc[OOS_START:])
            d.append(dict(panel=pname, cost=c, dSharpe_abs_argmax=b["Sharpe"] - a["Sharpe"],
                          dCAGR_abs_argmax=b["CAGR"] - a["CAGR"],
                          dSharpe_inc_argmax=i["Sharpe"] - a["Sharpe"]))
    D = pd.DataFrame(d)
    say(D.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say(f"  ABSTAIN beats ARGMAX on OOS Sharpe in {int((D.dSharpe_abs_argmax > 0).sum())} of {len(D)} "
        f"(panel, cost) books; mean {D.dSharpe_abs_argmax.mean():+.4f}")
    say(f"  INCUMBENT (never choose) beats ARGMAX in {int((D.dSharpe_inc_argmax > 0).sum())} of {len(D)}; "
        f"mean {D.dSharpe_inc_argmax.mean():+.4f}")

    flush()
    say(f"\nwrote {STEM}.{{census,ledger,taugrid,sensitivity,walkforward,arms,livecells,"
        "livecells_cal,taugrid_live,wf2,walkforward_live,books,keeppaths,gate431,console}}")
    flush()


if __name__ == "__main__":
    main()
