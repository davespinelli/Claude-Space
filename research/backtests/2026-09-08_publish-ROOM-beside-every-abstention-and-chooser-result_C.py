#!/usr/bin/env python3
"""Idea 457 — publish ROOM beside every ABSTENTION result.   (lane C, 2026-09-08)

QUESTION (QUEUE 457): idea 241 showed the control arm carries +0.0258 of free OOS Sharpe
over a random menu arm (t +22.2) while the argmax buys only -0.0058 against it, so ANY rule
that falls back to the control scores positive for a reason that has nothing to do with the
rule.  Idea 445 drafted the ROOM/REGRET clause for SELECTION results; extend it to
ABSTENTION results, back-fill ROOM over the 1,834 control-carrying census cells, and report
how many published abstention verdicts FLIP once ROOM is netted out.

THE ALGEBRA (this is the whole idea; everything below is bookkeeping)
  A cell i has a menu of arms, an IS argmax `star`, a labelled control `ctl`, and the menu's
  OOS mean.  An abstention rule with gate g falls back to the control when g fires:

      D   = mean_i [ OOS(pick_i) - OOS(star_i) ]  =  mean_i [ 1{g_i} * gain_i ]
      gain_i = OOS_ctl_i - OOS_star_i  =  ROOM_i - LIFT_i
      ROOM_i = OOS_ctl_i  - OOS_mean_i     <- a verdict on the CONTROL vs a random menu arm
      LIFT_i = OOS_star_i - OOS_mean_i     <- what the ARGMAX buys vs a random menu arm

  so   D = f * ( ROOM_fired - LIFT_fired ),   f = fire rate.

  A gate with NO information that fires at the same rate on random cells earns, in
  expectation,   D_null(f) = f * ( ROOM_bar - LIFT_bar ).   Netting:

      FULL-NULL  net D = D - f*(ROOM_bar - LIFT_bar)   <- correct null for a-vs-ARGMAX verdict
      ROOM-ONLY  net D = D - f*ROOM_bar                <- the queue's literal wording; the
                                                          right null when the verdict is quoted
                                                          against the menu mean / a random arm

  Both are published at every grid point.  Neither is selected.

TUNED PARAMETERS (exactly 2, all 30 points reported, IMPORTED not fitted here):
    q    - abstention threshold as a QUANTILE of the corpus's own top-2 gap distribution,
           q in {0.0, 0.1, ..., 0.9}                                          (10 points)
    norm - the scale the gap is measured on, {raw, z, rng}                    (3 points)
  This ladder is idea 241 lane B's, imported verbatim so the two runs are comparable.
  The ROOM-estimator (POOLED | PERFILE) x netting-basis (ROOM-ONLY | FULL-NULL) matrix is a
  4-way REPORTING axis, published in full at every grid point, with no point selected; the
  exact within-file permutation null is carried beside it as the non-parametric reference.

DESIGN
  PART A  back-fill ROOM over the 1,834 control-carrying Sharpe cells of idea 241 lane B's
          committed census (a re-reading of a committed artefact; the four published
          decomposition numbers are reproduced first, as gate G2).  D(tau), f(tau), both
          nettings, and a 2,000-draw within-file permutation null at every grid point.
  PART B  census of PUBLISHED ABSTENTION VERDICTS: every committed research/backtests/*.csv
          row carrying BOTH a fire-rate column and a delta-vs-pick column.  Net ROOM out of
          each and count the sign flips.  Every rejection is counted in a ledger; rows whose
          corpus has no reconstructable ROOM are UNAUDITED, never a pass.
  PART C  RULE 8 on live prices, out of corpus: a fresh 31-arm menu (band x gross x cadence
          + an ungated control) on 3 panels x 2 cost rungs, 300 seeded sub-menus as cells,
          arms read on 2010-2016, tau calibrated on 2014-2016, 2017-2026 read once.  Books:
          ARGMAX, ABSTAIN, INCUMBENT, and a RANDOM-GATE book firing at the SAME rate on
          random cells - the null made into an actual tradable book.  Both KEEP paths on the
          full sample and on the OOS window, against RULES v2 and SPY.

PROTOCOL: 10 bps anchor (25 bps rung reported), next-day execution (engine.backtest), no
shorting, no leverage.  Does not modify RULES.md, scan.py, bot.py, baseline.py or PROTOCOL.md.
Deterministic (seed 457000), no network.
"""
from __future__ import annotations

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

STEM = "2026-09-08_publish-ROOM-beside-every-abstention-and-chooser-result_C"
OUT = ROOT / "research" / "backtests"
CENSUS = OUT / "2026-09-08_the-013-margin-rule_B.census.csv"     # idea 241 lane B, committed

SEED = 457000
NORMS = ["raw", "z", "rng"]
NORMCOL = {"raw": "margin_raw", "z": "margin_z", "rng": "margin_rng"}
QGRID = [round(0.1 * i, 1) for i in range(10)]
TAU_ANCHOR = 0.013                       # idea 77 / queue 241's absolute anchor, raw Sharpe
NPERM = 2000
MIN_FILE_CELLS = 20                      # PERFILE estimator needs this many, else POOLED

IS_INNER_END = "2013-12-31"
MID_START, MID_END = "2014-01-01", "2016-12-31"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


def tstat(x) -> tuple[float, float, int]:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 2 or x.std(ddof=1) == 0:
        return float(x.mean()) if n else np.nan, np.nan, n
    return float(x.mean()), float(x.mean() / (x.std(ddof=1) / np.sqrt(n))), n


# =============================================================== PART A — the back-fill
def load_cells() -> pd.DataFrame:
    c = pd.read_csv(CENSUS)
    s = c[(c.metric == "Sharpe") & (c.has_ctl == True)].copy()   # noqa: E712
    s["ROOM"] = s.OOS_ctl - s.OOS_mean
    s["LIFT"] = s.OOS_star - s.OOS_mean
    s["gain"] = s.OOS_ctl - s.OOS_star
    s["REGRET"] = s.OOS_best - s.OOS_star
    return s.reset_index(drop=True)


def gate_repro(s: pd.DataFrame) -> pd.DataFrame:
    """G2: reproduce idea 241 lane B's four published decomposition numbers exactly."""
    pub = {"ROOM": (0.0258, 22.2), "LIFT": (0.0201, 11.8),
           "gain_star_minus_ctl": (-0.0058, -3.2), "REGRET": (0.0478, 26.9)}
    rows = []
    for k, (pm, pt) in pub.items():
        col = -s.gain if k == "gain_star_minus_ctl" else s[k]
        m, t, n = tstat(col)
        rows.append(dict(quantity=k, published_mean=pm, recon_mean=m, d_mean=abs(m - pm),
                         published_t=pt, recon_t=t, d_t=abs(t - pt), n=n))
    return pd.DataFrame(rows)


def perm_null(gain: np.ndarray, groups: list[np.ndarray], fired: np.ndarray,
              rng: np.random.Generator, B: int = NPERM) -> tuple[float, float, float, float]:
    """Exact reference: reshuffle WHICH cells fire, keeping the per-file fire count fixed.
    Returns (null mean, null 2.5%, null 97.5%, one-sided p for observed D)."""
    n = len(gain)
    obs = float((gain * fired).sum() / n)
    draws = np.zeros(B)
    for g in groups:
        k = int(fired[g].sum())
        if k == 0 or k == len(g):
            draws += gain[g].sum() / n if k == len(g) else 0.0
            continue
        u = rng.random((len(g), B))
        idx = np.argpartition(u, k - 1, axis=0)[:k]          # k random rows per column
        draws += gain[g][idx].sum(axis=0) / n
    above = obs >= draws.mean()
    p = float((draws >= obs).mean()) if above else float((draws <= obs).mean())
    return float(draws.mean()), float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975)), p


def taugrid(s: pd.DataFrame, label: str, rng: np.random.Generator,
            do_perm: bool = True) -> pd.DataFrame:
    """D(tau), the fire rate, and both nettings under both ROOM estimators."""
    files = s.file.values
    groups = [np.where(files == f)[0] for f in pd.unique(files)]
    gain = s.gain.values.astype(float)
    room_bar, lift_bar = float(s.ROOM.mean()), float(s.LIFT.mean())
    # per-file estimators, falling back to pooled on thin files
    fr = s.groupby("file").agg(n=("gain", "size"), room=("ROOM", "mean"), lift=("LIFT", "mean"))
    fr.loc[fr.n < MIN_FILE_CELLS, ["room", "lift"]] = np.nan
    room_f = s.file.map(fr.room).fillna(room_bar).values
    lift_f = s.file.map(fr.lift).fillna(lift_bar).values

    rows = []
    for norm in NORMS:
        gap = s[NORMCOL[norm]].values.astype(float)
        for q in QGRID:
            tau = float(np.nanquantile(gap, q)) if q > 0 else 0.0
            fired = (np.isfinite(gap) & (gap < tau)).astype(float) if q > 0 else np.zeros(len(gap))
            f = float(fired.mean())
            D = float((gain * fired).mean())
            m, t, n = tstat(np.where(fired > 0, gain, 0.0))
            row = dict(scope=label, norm=norm, q=q, tau=tau, n=len(gain), fire_rate=f, D=D, t=t,
                       ROOM_fired=float((s.ROOM.values * fired).sum() / max(fired.sum(), 1)),
                       LIFT_fired=float((s.LIFT.values * fired).sum() / max(fired.sum(), 1)),
                       ROOM_bar=room_bar, LIFT_bar=lift_bar)
            row["identity_err"] = abs(D - f * (row["ROOM_fired"] - row["LIFT_fired"]))
            # the 4 reporting points
            row["Dnet_POOLED_ROOMONLY"] = D - f * room_bar
            row["Dnet_POOLED_FULLNULL"] = D - f * (room_bar - lift_bar)
            row["Dnet_PERFILE_ROOMONLY"] = D - float((fired * room_f).mean())
            row["Dnet_PERFILE_FULLNULL"] = D - float((fired * (room_f - lift_f)).mean())
            if do_perm and 0 < f < 1:
                nm, lo, hi, p = perm_null(gain, groups, fired, rng)
                row.update(perm_mean=nm, perm_lo=lo, perm_hi=hi, perm_p=p,
                           Dnet_PERM=D - nm)
            else:
                row.update(perm_mean=np.nan, perm_lo=np.nan, perm_hi=np.nan, perm_p=np.nan,
                           Dnet_PERM=np.nan)
            rows.append(row)
    return pd.DataFrame(rows)


def anchor_row(s: pd.DataFrame, rng: np.random.Generator) -> dict:
    """The queue's pre-registered tau = 0.013 in RAW units (not fitted)."""
    gap = s.margin_raw.values.astype(float)
    fired = (gap < TAU_ANCHOR).astype(float)
    gain = s.gain.values.astype(float)
    f, D = float(fired.mean()), float((gain * fired).mean())
    room_bar, lift_bar = float(s.ROOM.mean()), float(s.LIFT.mean())
    files = s.file.values
    groups = [np.where(files == fl)[0] for fl in pd.unique(files)]
    nm, lo, hi, p = perm_null(gain, groups, fired, rng)
    return dict(scope="RECORD/anchor", norm="raw", q=np.nan, tau=TAU_ANCHOR, n=len(gain),
                fire_rate=f, D=D, ROOM_bar=room_bar, LIFT_bar=lift_bar,
                Dnet_POOLED_ROOMONLY=D - f * room_bar,
                Dnet_POOLED_FULLNULL=D - f * (room_bar - lift_bar),
                perm_mean=nm, perm_p=p, Dnet_PERM=D - nm)


# ============================================= PART B — the published-verdict census
RATE_COLS = ["abstain_rate", "OOS_abstain", "abstained", "abstain", "a", "fire_rate", "OOS_fc"]
DELTA_COLS = ["d_vs_argmax", "OOS_D", "IS_D", "d_clustered", "d_inc", "d_mean", "gain",
              "mean", "D"]
LIVE_HINTS = ("live", "panel")


def scan_published(live_room: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Every committed CSV row that publishes both a fire rate and a delta-vs-pick."""
    ledger, rows = [], []
    for path in sorted(OUT.glob("*.csv")):
        if path.name.startswith(STEM):
            continue                                   # idempotent on a re-run
        try:
            df = pd.read_csv(path, nrows=5)
        except Exception as e:
            ledger.append(dict(file=path.name, admitted=False, reason=f"unreadable:{type(e).__name__}"))
            continue
        cols = list(df.columns)
        rate = next((c for c in RATE_COLS if c in cols), None)
        delta = next((c for c in DELTA_COLS if c in cols), None)
        if rate is None:
            ledger.append(dict(file=path.name, admitted=False, reason="no fire-rate column"))
            continue
        if delta is None:
            ledger.append(dict(file=path.name, admitted=False, reason="no delta-vs-pick column"))
            continue
        try:
            df = pd.read_csv(path)
        except Exception as e:
            ledger.append(dict(file=path.name, admitted=False, reason=f"unreadable:{type(e).__name__}"))
            continue
        r = pd.to_numeric(df[rate], errors="coerce")
        if r.notna().sum() == 0:
            ledger.append(dict(file=path.name, admitted=False, reason="fire-rate not numeric"))
            continue
        counted = False
        if r.max(skipna=True) > 1.0:                    # a COUNT, not a rate
            if "n" in cols:
                r = r / pd.to_numeric(df["n"], errors="coerce")
                counted = True
            else:
                ledger.append(dict(file=path.name, admitted=False, reason="fire-rate >1 and no n"))
                continue
        d = pd.to_numeric(df[delta], errors="coerce")
        ok = r.notna() & d.notna() & (r >= 0) & (r <= 1)
        if ok.sum() == 0:
            ledger.append(dict(file=path.name, admitted=False, reason="no usable (rate, delta) row"))
            continue
        # anchor certificate: does the file's own f=0 row publish delta == 0?
        z = ok & (r <= 1e-12)
        cert = float((d[z].abs() < 1e-9).mean()) if z.sum() else np.nan
        sub = df[ok].copy()
        sub["_rate"], sub["_delta"] = r[ok], d[ok]
        # scope: RECORD corpus vs a LIVE panel vs unknown
        txt = (path.name + " " + " ".join(cols)).lower()
        scope_col = next((c for c in ("scope", "corpus") if c in cols), None)
        for _, rr in sub.iterrows():
            sc = str(rr[scope_col]).lower() if scope_col else ""
            panel = str(rr["panel"]).lower() if "panel" in cols else ""
            if panel in live_room:
                kind, key = "LIVE", panel
            elif "record" in sc or "frozen" in sc or "parent" in sc:
                kind, key = "RECORD", "RECORD"
            elif any(h in txt for h in LIVE_HINTS) and "record" not in txt:
                kind, key = "LIVE", "LIVEPOOL"
            elif "record" in txt or "census" in txt or "corpus" in txt:
                kind, key = "RECORD", "RECORD"
            else:
                kind, key = "UNKNOWN", None
            rows.append(dict(file=path.name, rate_col=rate, delta_col=delta, counted=counted,
                             anchor_cert=cert, scope=kind, room_key=key,
                             f=float(rr["_rate"]), D=float(rr["_delta"])))
        ledger.append(dict(file=path.name, admitted=True, reason="", rate_col=rate,
                           delta_col=delta, rows=int(ok.sum()), anchor_cert=cert))
    return pd.DataFrame(rows), pd.DataFrame(ledger)


def net_published(v: pd.DataFrame, room_bar: float, lift_bar: float,
                  live_room: dict, live_lift: dict) -> pd.DataFrame:
    v = v.copy()
    rb, lb = [], []
    for _, r in v.iterrows():
        if r.scope == "RECORD":
            rb.append(room_bar); lb.append(lift_bar)
        elif r.scope == "LIVE":
            k = r.room_key if r.room_key in live_room else "LIVEPOOL"
            rb.append(live_room.get(k, np.nan)); lb.append(live_lift.get(k, np.nan))
        else:
            rb.append(np.nan); lb.append(np.nan)
    v["ROOM_bar"], v["LIFT_bar"] = rb, lb
    v["Dnet_ROOMONLY"] = v.D - v.f * v.ROOM_bar
    v["Dnet_FULLNULL"] = v.D - v.f * (v.ROOM_bar - v.LIFT_bar)
    # bounds for the UNAUDITED rows: net them under EVERY ROOM estimate this run has, and
    # report the flip count as a range rather than as a pass.
    cands = [(room_bar, lift_bar)] + [(live_room[k], live_lift[k]) for k in live_room]
    lo = np.full(len(v), np.inf)
    hi = np.full(len(v), -np.inf)
    for rbc, lbc in cands:
        for x in (v.D - v.f * rbc, v.D - v.f * (rbc - lbc)):
            lo, hi = np.minimum(lo, x.values), np.maximum(hi, x.values)
    v["Dnet_lo"], v["Dnet_hi"] = lo, hi
    v["verdict"] = np.where(v.D > 0, "POSITIVE", np.where(v.D < 0, "NEGATIVE", "NEUTRAL"))
    for c in ("ROOMONLY", "FULLNULL"):
        v[f"flip_{c}"] = (v.D > 0) & (v[f"Dnet_{c}"] <= 0)
        v[f"unaudited_{c}"] = v[f"Dnet_{c}"].isna()
    return v


# ================================================================= PART C — live corpus
def ew_band_weights(px, band, gross, gated=True):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0) if gated else ew


def arm_menu():
    arms = [("control", dict(band=None, gross=1.0, freq="W", gated=False))]
    for band in (0.0, 0.015, 0.03, 0.045, 0.06):
        for gross in (0.50, 0.75, 1.00):
            for freq in ("W", "M"):
                arms.append((f"b{band:g}-g{gross:.2f}-{freq}",
                             dict(band=band, gross=gross, freq=freq, gated=True)))
    return arms


def load_panels():
    P = {"u56": load_universe(), "broad136": load_universe(broad=True)}
    small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["small439"] = small[[c for c in small.columns if c not in bad]]
    return P


def win_metrics(r, lo=None, hi=None, prefix=""):
    x = r.loc[lo:hi] if (lo or hi) else r
    if len(x) < 30:
        return {f"{prefix}{k}": np.nan for k in ("CAGR", "Sharpe", "MaxDD")}
    m = metrics(x)
    return {f"{prefix}CAGR": m["CAGR"], f"{prefix}Sharpe": m["Sharpe"], f"{prefix}MaxDD": m["MaxDD"]}


def keep_paths(r, base, spy):
    """4a vs the live RULES v2 book, 4b vs SPY, on the full sample and on the OOS window."""
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
                r = (r0 - to * c / 1e4).loc[start:]
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


def submenus(all_arms, n_cells=300, lo=5, hi=15, seed=SEED):
    rng = np.random.default_rng(seed)
    pool = [a for a in all_arms if a != "control"]
    out = []
    for _ in range(n_cells):
        k = int(rng.integers(lo, hi + 1)) - 1
        out.append(["control"] + sorted(rng.choice(pool, size=k, replace=False)))
    return out


def live_cells(fg: pd.DataFrame, menus, is_pre: str, oos_pre: str) -> pd.DataFrame:
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
            I, O, A = I[ok], O[ok], A[ok]
            order = np.argsort(-I)
            star, second = A[order[0]], A[order[1]]
            ctl_i = list(A).index("control") if "control" in A else None
            if ctl_i is None:
                continue
            gap = float(I[order[0]] - I[order[1]])
            sd = float(np.std(I, ddof=1)) if len(I) > 1 else np.nan
            rng_ = float(I.max() - I.min())
            rows.append(dict(panel=pname, cost=c, menu=j, n_arms=len(A), arm_star=star,
                             arm_second=second, margin_raw=gap,
                             margin_z=gap / sd if sd and sd > 0 else np.nan,
                             margin_rng=gap / rng_ if rng_ > 0 else np.nan,
                             OOS_star=float(O[order[0]]), OOS_ctl=float(O[ctl_i]),
                             OOS_mean=float(O.mean()), OOS_best=float(O.max()),
                             star_is_ctl=bool(star == "control"),
                             file=f"LIVE/{pname}"))
    d = pd.DataFrame(rows)
    d["ROOM"] = d.OOS_ctl - d.OOS_mean
    d["LIFT"] = d.OOS_star - d.OOS_mean
    d["gain"] = d.OOS_ctl - d.OOS_star
    d["REGRET"] = d.OOS_best - d.OOS_star
    return d


def books(cells: pd.DataFrame, curves, norm: str, tau: float, rng: np.random.Generator,
          n_rand: int = 20):
    """ARGMAX / ABSTAIN(tau) / INCUMBENT / RANDGATE(matched fire rate) return streams."""
    out = {}
    col = NORMCOL[norm]
    for (pname, c), sub in cells.groupby(["panel", "cost"]):
        fired = (sub[col] < tau).values
        picks_arg = sub.arm_star.values
        picks_abs = np.where(fired, "control", picks_arg)
        out[(pname, c, "ARGMAX")] = pd.concat([curves[(pname, c, a)] for a in picks_arg], axis=1).mean(axis=1)
        out[(pname, c, "ABSTAIN")] = pd.concat([curves[(pname, c, a)] for a in picks_abs], axis=1).mean(axis=1)
        out[(pname, c, "INCUMBENT")] = curves[(pname, c, "control")]
        k = int(fired.sum())
        streams = []
        for _ in range(n_rand):
            m = np.zeros(len(sub), dtype=bool)
            if k:
                m[rng.choice(len(sub), size=k, replace=False)] = True
            p = np.where(m, "control", picks_arg)
            streams.append(pd.concat([curves[(pname, c, a)] for a in p], axis=1).mean(axis=1))
        out[(pname, c, "RANDGATE")] = pd.concat(streams, axis=1).mean(axis=1)
    return out


def gate_cost_identity(px) -> float:
    w = ew_band_weights(px, 0.03, 0.75, gated=True)
    a = backtest(px, w, cost_bps=0.0, freq="W")
    direct = backtest(px, w, cost_bps=25.0, freq="W")["returns"]
    return float((a["returns"] - a["turnover"] * 25.0 / 1e4 - direct).abs().max())


# ============================================================================== main
def main():
    rng = np.random.default_rng(SEED)
    say(f"# Idea 457 — publish ROOM beside every abstention result   ({STEM})")
    say("")

    # ---------------- PART A
    s = load_cells()
    say(f"PART A — census re-read: {CENSUS.name}")
    say(f"  control-carrying Sharpe cells {len(s)} over {s.file.nunique()} files; "
        f"argmax IS the control in {int(s.star_is_ctl.sum())} ({s.star_is_ctl.mean():.1%})")
    g2 = gate_repro(s)
    say("\nGATE G2 — idea 241 lane B's published decomposition, reproduced:")
    say(g2.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    say(f"  max |d_mean| {g2.d_mean.max():.2e}   max |d_t| {g2.d_t.max():.2e}")

    room_bar, lift_bar = float(s.ROOM.mean()), float(s.LIFT.mean())
    rm, rt, _ = tstat(s.ROOM)
    say(f"\n  ROOM_bar {room_bar:+.5f} (t {rt:+.1f})   LIFT_bar {lift_bar:+.5f}   "
        f"ROOM-LIFT {room_bar - lift_bar:+.5f}")
    say(f"  ROOM > 0 in {(s.ROOM > 0).mean():.1%} of cells; ROOM > LIFT in {(s.ROOM > s.LIFT).mean():.1%}")

    perfile = s.groupby("file").agg(n=("gain", "size"), ROOM=("ROOM", "mean"),
                                    LIFT=("LIFT", "mean"), gain=("gain", "mean"))
    perfile["estimator"] = np.where(perfile.n >= MIN_FILE_CELLS, "PERFILE", "POOLED-fallback")
    perfile.sort_values("n", ascending=False).to_csv(OUT / f"{STEM}.room.csv")
    say(f"  per-file ROOM: {int((perfile.n >= MIN_FILE_CELLS).sum())} of {len(perfile)} files carry "
        f">= {MIN_FILE_CELLS} cells (the rest fall back to pooled); "
        f"file-level ROOM range {perfile.ROOM.min():+.4f} .. {perfile.ROOM.max():+.4f}")

    tg = taugrid(s, "RECORD/all", rng)
    tg = pd.concat([tg, pd.DataFrame([anchor_row(s, rng)])], ignore_index=True)
    tg.to_csv(OUT / f"{STEM}.taugrid.csv", index=False)
    say(f"\n  identity  D = f*(ROOM_fired - LIFT_fired):  max err {tg.identity_err.max():.3e}")
    say("\nPART A — all 30 grid points + the pre-registered anchor (D vs the RAW ARGMAX):")
    show = tg[["norm", "q", "tau", "fire_rate", "D", "t", "Dnet_POOLED_ROOMONLY",
               "Dnet_POOLED_FULLNULL", "Dnet_PERFILE_ROOMONLY", "Dnet_PERFILE_FULLNULL",
               "perm_mean", "Dnet_PERM", "perm_p"]]
    say(show.to_string(index=False, float_format=lambda x: f"{x:+.5f}"))

    pos = tg[(tg.D > 0) & tg.fire_rate.between(1e-12, 1 - 1e-12)]
    say(f"\n  grid points with D > 0: {len(pos)} of {len(tg[tg.fire_rate > 0])} non-degenerate")
    for c in ("Dnet_POOLED_ROOMONLY", "Dnet_POOLED_FULLNULL", "Dnet_PERFILE_ROOMONLY",
              "Dnet_PERFILE_FULLNULL", "Dnet_PERM"):
        say(f"    still > 0 after {c[5:]:22s}: {int((pos[c] > 0).sum())} of {len(pos)}   "
            f"(median netted {pos[c].median():+.5f} vs median raw D {pos.D.median():+.5f})")
    sig_up = pos[(pos.Dnet_PERM > 0) & (pos.perm_p <= 0.05)]
    sig_dn = pos[(pos.Dnet_PERM < 0) & (pos.perm_p <= 0.05)]
    say(f"    vs the matched-rate RANDOM GATE: significantly ABOVE it at {len(sig_up)} of "
        f"{len(pos)} points, significantly BELOW it at {len(sig_dn)}, indistinguishable at "
        f"{len(pos) - len(sig_up) - len(sig_dn)}")
    if len(sig_up):
        say("      the points that do beat a random gate (and by how little): "
            + ", ".join(f"{r.norm}/q{r.q:g} D {r.D:+.5f} net {r.Dnet_PERM:+.5f} "
                        f"({r.Dnet_PERM / r.D:.0%} of it)" for _, r in sig_up.iterrows()))

    # ---------------- PART C (before B: B needs the live ROOM estimates)
    say("\nPART C — fresh live corpus (out of the committed record entirely)")
    panels = load_panels()
    g1 = gate_cost_identity(panels["u56"])
    say(f"GATE G1 — cost-rung identity net(c) = gross - TO*c/1e4 : max err {g1:.3e}")
    fg, curves = fresh_grid(panels)
    fg.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    menus = submenus([a for a, _ in arm_menu()])
    lc = live_cells(fg, menus, "IS_", "OOS_")
    lc.to_csv(OUT / f"{STEM}.livecells.csv", index=False)
    say(f"  {len(lc)} live cells over {lc.panel.nunique()} panels x 2 cost rungs "
        f"({len(menus)} seeded sub-menus each); argmax IS the control in "
        f"{lc.star_is_ctl.mean():.1%} of them")
    for p, sub in lc.groupby("panel"):
        say(f"    {p:9s} n {len(sub):4d}  star_is_ctl {sub.star_is_ctl.mean():6.1%}  "
            f"ROOM {sub.ROOM.mean():+.4f}  LIFT {sub.LIFT.mean():+.4f}  "
            f"gain {sub.gain.mean():+.4f}")
    live_room = {p: float(g.ROOM.mean()) for p, g in lc.groupby("panel")}
    live_lift = {p: float(g.LIFT.mean()) for p, g in lc.groupby("panel")}
    live_room["LIVEPOOL"], live_lift["LIVEPOOL"] = float(lc.ROOM.mean()), float(lc.LIFT.mean())

    # calibration cells (arms read on 2010-2013, tau chosen on 2014-2016)
    cal = live_cells(fg, menus, "ISin_", "MID_")
    cg = taugrid(cal.assign(file=cal.panel), "LIVE/cal", rng, do_perm=False)
    cg.to_csv(OUT / f"{STEM}.calgrid.csv", index=False)
    best = cg[cg.fire_rate > 0].sort_values("D", ascending=False).iloc[0]
    say(f"\n  RULE 8 — (norm, q) chosen on 2014-2016 ONLY: {best.norm}/q{best.q:g}, "
        f"tau {best.tau:.4f}, calibration D {best.D:+.5f} (fire rate {best.fire_rate:.1%})")
    tau_live = float(np.nanquantile(lc[NORMCOL[best.norm]].values.astype(float), best.q)) \
        if best.q > 0 else 0.0
    lg = taugrid(lc.assign(file=lc.panel), "LIVE/oos", rng)
    lg.to_csv(OUT / f"{STEM}.livegrid.csv", index=False)
    say("\n  live OOS grid (2017-2026, read once) — all 30 points:")
    say(lg[["norm", "q", "tau", "fire_rate", "D", "t", "Dnet_POOLED_ROOMONLY",
            "Dnet_POOLED_FULLNULL", "perm_mean", "Dnet_PERM", "perm_p"]]
        .to_string(index=False, float_format=lambda x: f"{x:+.5f}"))
    sel = lg[(lg.norm == best.norm) & (lg.q == best.q)].iloc[0]
    say(f"\n  the CHOSEN point read once OOS: D {sel.D:+.5f} (t {sel.t:+.2f}), fire rate "
        f"{sel.fire_rate:.1%}, ROOM-netted {sel.Dnet_POOLED_ROOMONLY:+.5f}, "
        f"FULL-NULL {sel.Dnet_POOLED_FULLNULL:+.5f}, permutation-netted {sel.Dnet_PERM:+.5f} "
        f"(p {sel.perm_p:.3f})")

    bk = books(lc, curves, best.norm, tau_live, rng)
    krows = []
    for (pname, c, label), r in sorted(bk.items()):
        spy, base = curves[(pname, c, "__SPY__")], curves[(pname, c, "__V2__")]
        row = dict(panel=pname, cost=c, book=label)
        row.update(win_metrics(r))
        row.update(win_metrics(r, lo=OOS_START, prefix="OOS_"))
        row.update(win_metrics(spy, lo=OOS_START, prefix="SPY_OOS_"))
        row.update(win_metrics(base, lo=OOS_START, prefix="V2_OOS_"))
        h = len(r) // 2
        row["H1"] = metrics(r.iloc[:h])["Sharpe"]
        row["H2"] = metrics(r.iloc[h:])["Sharpe"]
        row.update(keep_paths(r, base, spy))
        krows.append(row)
    for (pname, c) in sorted({(p, c) for p, c, _ in bk}):
        spy, base = curves[(pname, c, "__SPY__")], curves[(pname, c, "__V2__")]
        for label, r in (("SPY", spy), ("RULES_v2", base)):
            row = dict(panel=pname, cost=c, book=label)
            row.update(win_metrics(r))
            row.update(win_metrics(r, lo=OOS_START, prefix="OOS_"))
            h = len(r) // 2
            row["H1"] = metrics(r.iloc[:h])["Sharpe"]
            row["H2"] = metrics(r.iloc[h:])["Sharpe"]
            krows.append(row)
    kp = pd.DataFrame(krows)
    kp.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say("\n  BOOKS (10/25 bps, next-day execution, OOS = 2017-01-01..):")
    say(kp[["panel", "cost", "book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b", "pass4a_oos", "pass4b_oos"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ab = kp[kp.book.isin(["ABSTAIN", "ARGMAX", "RANDGATE"])].pivot_table(
        index=["panel", "cost"], columns="book", values="OOS_Sharpe")
    say("\n  OOS Sharpe: ABSTAIN vs ARGMAX vs the matched-rate RANDOM GATE")
    say(ab.to_string(float_format=lambda x: f"{x:.4f}"))
    if {"ABSTAIN", "ARGMAX", "RANDGATE"} <= set(ab.columns):
        say(f"    ABSTAIN - ARGMAX  mean {float((ab.ABSTAIN - ab.ARGMAX).mean()):+.4f}  "
            f"wins {int((ab.ABSTAIN > ab.ARGMAX).sum())}/{len(ab)}")
        say(f"    ABSTAIN - RANDGATE mean {float((ab.ABSTAIN - ab.RANDGATE).mean()):+.4f}  "
            f"wins {int((ab.ABSTAIN > ab.RANDGATE).sum())}/{len(ab)}")
        say(f"    RANDGATE - ARGMAX mean {float((ab.RANDGATE - ab.ARGMAX).mean()):+.4f}  "
            f"wins {int((ab.RANDGATE > ab.ARGMAX).sum())}/{len(ab)}")
        nd = ab[(ab.ABSTAIN - ab.ARGMAX).abs() > 1e-12]        # books where the gate moves at all
        if len(nd):
            say(f"    NON-DEGENERATE books only ({len(nd)} of {len(ab)}; the gate is a strict "
                f"no-op elsewhere): ABSTAIN-ARGMAX {float((nd.ABSTAIN - nd.ARGMAX).mean()):+.4f}, "
                f"ABSTAIN-RANDGATE {float((nd.ABSTAIN - nd.RANDGATE).mean()):+.4f}")
    for p in ("4a", "4b"):
        for w in ("", "_oos"):
            c = f"pass{p}{w}"
            n = kp[kp.book.isin(["ARGMAX", "ABSTAIN", "INCUMBENT", "RANDGATE"])]
            say(f"    KEEP {p}{w or '(full)'}: {int(n[c].sum())} of {len(n)} books  "
                + ", ".join(f"{b} {int(g[c].sum())}/{len(g)}" for b, g in n.groupby('book')))

    # ---------------- PART B
    say("\nPART B — the published-verdict census (every committed CSV re-read)")
    v, ledger = scan_published(live_room)
    ledger.to_csv(OUT / f"{STEM}.ledger.csv", index=False)
    v = net_published(v, room_bar, lift_bar, live_room, live_lift)
    v.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
    adm = ledger[ledger.admitted == True]                      # noqa: E712
    say(f"  {len(ledger)} committed CSVs scanned -> {len(adm)} admitted, {len(v)} verdict rows")
    say("  rejections: " + ", ".join(f"{r} {n}" for r, n in
                                     ledger[ledger.admitted == False].reason.value_counts().items()))  # noqa: E712
    say(f"  anchor certificate (the file's own f=0 row publishes delta == 0): "
        f"{int((adm.anchor_cert == 1.0).sum())} of {int(adm.anchor_cert.notna().sum())} files "
        f"that carry an f=0 row; {int(adm.anchor_cert.isna().sum())} files carry none")
    say("  admitted files:")
    for _, r in adm.sort_values("rows", ascending=False).iterrows():
        say(f"    {r.file:78s} rate={r.rate_col:12s} delta={r.delta_col:12s} rows={int(r.rows):5d}")
    say("")
    say(f"  scope: " + ", ".join(f"{k} {int(n)}" for k, n in v.scope.value_counts().items()))
    say(f"  published verdicts by sign: " + ", ".join(f"{k} {int(n)}" for k, n in
                                                      v.verdict.value_counts().items()))
    posv = v[v.verdict == "POSITIVE"]
    say(f"\n  THE ANSWER — of {len(posv)} POSITIVE published abstention verdicts:")
    for c in ("ROOMONLY", "FULLNULL"):
        fl = int(posv[f"flip_{c}"].sum())
        un = int(posv[f"unaudited_{c}"].sum())
        aud = len(posv) - un
        say(f"    net {c:9s}: {fl} FLIP to <= 0 ({fl / max(aud, 1):.1%} of the {aud} auditable), "
            f"{aud - fl} survive, {un} UNAUDITED (no reconstructable ROOM)")
    say(f"    ALL {len(posv)} positive rows, netted under EVERY ROOM estimate this run measured "
        f"(record {room_bar:+.4f}; live " + ", ".join(f"{k} {vv:+.4f}" for k, vv in live_room.items())
        + "): ")
    say(f"      "
        f"{int((posv.Dnet_hi <= 0).sum())} flip under ALL of them, "
        f"{int((posv.Dnet_lo > 0).sum())} survive ALL of them, "
        f"{int(((posv.Dnet_lo <= 0) & (posv.Dnet_hi > 0)).sum())} are estimator-dependent "
        f"(of all {len(posv)} positive verdicts)")
    say("\n  by file (POSITIVE rows only):")
    t = posv.groupby("file").agg(rows=("D", "size"), mean_f=("f", "mean"), mean_D=("D", "mean"),
                                 mean_net_RO=("Dnet_ROOMONLY", "mean"),
                                 mean_net_FN=("Dnet_FULLNULL", "mean"),
                                 flip_RO=("flip_ROOMONLY", "sum"), flip_FN=("flip_FULLNULL", "sum"))
    say(t.to_string(float_format=lambda x: f"{x:+.5f}"))

    # walk-forward summary table required by PROTOCOL 8
    wf = pd.DataFrame([
        dict(where="WF-A record corpus, tau ladder", chosen_on="n/a (all 30 points published)",
             D=float(tg[tg.fire_rate > 0].D.max()), netted=float(tg[tg.fire_rate > 0].Dnet_PERM.max())),
        dict(where="WF-C live, tau chosen 2014-2016", chosen_on=f"{best.norm}/q{best.q:g}",
             D=float(sel.D), netted=float(sel.Dnet_PERM)),
    ])
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\nWALK-FORWARD (PROTOCOL 8) summary:")
    say(wf.to_string(index=False, float_format=lambda x: f"{x:+.5f}"))
    flush()


if __name__ == "__main__":
    main()
