#!/usr/bin/env python3
"""Idea 651 — WHICH *MATCHED-GROSS* CLAIMS IN THE RECORD ARE *SHARPE* CLAIMS?

Idea 462 measured that a SCALAR exposure match (multiply a book's weights by one constant
k <= 1, remainder in cash at 0%) is Sharpe-neutral to max |dSharpe| 0.0036 over 48 arms,
while a RE-SPREAD match (push the same nominal gross across the admitted names only) is a
DIFFERENT BOOK (+3.42% CAGR for -11.96 pp MaxDD on 24/24 paired points).  If that holds
generally, then every published "matched on gross" **Sharpe** claim is one of two things:

  * a NO-OP  — the control was scalar-matched, so the match cannot have moved Sharpe and the
    Sharpe conclusion is the *unmatched* conclusion wearing a control's name; or
  * a RE-SPREAD — the "control" is a different book (different concentration), so the claim
    is a book-vs-book comparison misfiled as an exposure control.

Either way the phrase "matched on gross" is not doing the work its readers think it does on a
Sharpe bar.  This run (a) censuses the record's matched-gross claim sites and classifies each
one, and (b) re-measures the two match types directly on a wider arm set than idea 462's, so
the census's classification rests on a measured bound rather than on idea 462's headline.

Pre-registration (fixed before any number was read):

  * TWO tuned parameters and no more:
      CLAIMSET  (census)      — COMMITTED | ALL
      MATCHTYPE (measurement) — NATIVE | SCALAR | RESPREAD
    Cost rung (10, 25 bps), panel, book, metric and the k-ladder are REPORTED at every point,
    never chosen.  Every grid point is written to disk.

  * PART A — CENSUS.  A claim SITE is one line of the record containing a matched-gross
    phrase (see PHRASES).  Two claim sets:
      COMMITTED — the published record a reader acts on: LEADERBOARD.md, QUEUE.md,
                  CHANGELOG.md, PROTOCOL.md, the *_RECOMMENDATION/memo .md files and every
                  backtests/*.result.md.
      ALL       — COMMITTED plus the .py docstrings/comments and .console.txt logs.
    Each site is classified on two axes, from its own text only:
      BAR       SHARPE if the line names Sharpe; else RETURN if it names CAGR/pp-per-yr/
                return; else DD if it names MaxDD/Calmar/drawdown; else NOBAR.
      TYPE      RESPREAD if the line names a re-spread/concentration construction;
                SCALAR   if it names a scalar/rescale/static-at-own-gross construction;
                BOTH     if both; UNSTATED otherwise.
    Headline census number = SHARPE sites whose TYPE is SCALAR or UNSTATED, i.e. Sharpe
    conclusions resting on a match that (PART B) cannot move Sharpe.

  * PART B — MEASUREMENT.  12 book forms x 3 panels x 2 rungs, idea 462's forms unchanged.
      NATIVE    the book as published (gate books de-grossed, gated weight -> cash).
      SCALAR    w -> k*w, one constant, remainder in cash at 0%, no leverage.  k is fitted on
                the IS window (<= 2016-12-31) ONLY as k = target/own realised gross, target =
                that panel's native GATE-family mean realised gross, capped at 1.0.  Both the
                fitted k and the ACHIEVED full-sample realised gross are published.
      RESPREAD  gate books re-spread their nominal 0.75 across admitted names (g/n_adm).
                Ranked books and EW_ALL have no gated weight, so RESPREAD == NATIVE for them
                by construction; that is asserted, not assumed (gate G4).
    Plus a K-LADDER: k in {0.25 .. 1.00} (7 rungs) on EVERY book/panel/rung, so the scalar
    bound is not a k-specific artefact.  Reported: max and median |dSharpe| per match type,
    the same for CAGR and MaxDD, and how many within-panel book ORDERINGS on Sharpe each
    match type changes.

  * BOTH KEEP PATHS on every point.  4a against the LIVE book (native RULES v2 on the same
    panel, window and rung); 4b against SPY (Sharpe > SPY in both halves AND OOS, MaxDD <=
    60% of SPY's, CAGR >= 70% of SPY's).

  * RULE 8 (PROTOCOL 8): inside each (panel, match type, rung) the book is chosen on IS
    <= 2016-12-31 by IS Sharpe ONLY, and 2017-01-01.. is read ONCE.  OOS CAGR/Sharpe/MaxDD
    reported against native RULES v2 and SPY on the same OOS window.

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are CURRENT-constituent lists, so their
LEVELS are biased upward and unequally so; only within-panel, within-window contrasts
(book minus its own match-type twin) are load-bearing.  U56 is a fixed ETF/mega-cap list and
is least biased.  SMALL439 drops the 44 sub-$2B names with max_1d_move >= 1.0 first.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .census.csv, .sites.csv, .grid.csv, .ladder.csv,
.walkforward.csv, .console.txt.
"""
import re
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-10_which-MATCHED-GROSS-claims-in-the-record-are-SHARPE-claims_cloud"
OUT = ROOT / "research" / "backtests"
FREQ = "W"
GROSS = 0.75
RUNGS = [10, 25]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
KLADDER = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]

GATE = ["RULESV2", "MA200dg", "BAND6dg", "ABSdg"]
RANKED = ["TOP5V1", "TOP10", "TOP20", "TOP40", "TOP20V", "TOP20B3", "LOWVOL20"]
BOOKS = ["EWALL"] + GATE + RANKED
PANELS = ["U56", "B136", "SMALL439"]
TYPES = ["NATIVE", "SCALAR", "RESPREAD"]
FAMILY = {**{b: "GATE" for b in GATE}, **{b: "RANKED" for b in RANKED}, "EWALL": "CONTROL"}

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)


# ============================================================ PART A — census machinery
PHRASES = re.compile(
    r"matched[\s\-]*(?:on[\s\-]+)?(?:realised[\s\-]+|realized[\s\-]+)?gross"
    r"|gross[\s\-]*matched"
    r"|matched[\s\-]+exposure"
    r"|gross[\s\-]+match(?:ing|es)?\b"
    r"|match(?:ed|ing)?[\s\-]+on[\s\-]+(?:realised[\s\-]+|realized[\s\-]+)?gross",
    re.I)
SHARPE = re.compile(r"\bsharpe\b", re.I)
RETURN = re.compile(r"\bCAGR\b|pp\s*/\s*yr|\bpp/yr\b|\breturns?\b|\bpp\b", re.I)
DDBAR = re.compile(r"\bMaxDD\b|\bmax\s*dd\b|\bdrawdown\b|\bCalmar\b", re.I)
RESPR = re.compile(r"re[\s\-]?spread|respread|g\s*/\s*n_?adm|across\s+(?:its\s+)?admitted"
                   r"|concentrat", re.I)
SCAL = re.compile(r"\bscalar\b|re[\s\-]?scal|multiplied\s+by\s+(?:a\s+)?(?:single\s+)?"
                  r"(?:constant\s+)?k|constant\s+k|\bk\s*<=\s*1|matched\s+static"
                  r"|static\s+at\s+the\s+arm|own\s+(?:realised\s+|realized\s+)?mean\s+gross"
                  r"|de[\s\-]?gross", re.I)

COMMITTED_ROOTS = ["LEADERBOARD.md", "QUEUE.md", "CHANGELOG.md", "PROTOCOL.md"]


def corpus_files(claimset):
    """Files in the record for one CLAIMSET.  COMMITTED = published prose a reader acts on."""
    R = ROOT / "research"
    files = [R / f for f in COMMITTED_ROOTS if (R / f).exists()]
    files += sorted((R / "backtests").glob("*.result.md"))
    files += sorted(p for p in (R / "backtests").glob("*.md")
                    if not p.name.endswith(".result.md"))
    files += sorted(p for p in R.glob("*.md") if p.name not in COMMITTED_ROOTS)
    if claimset == "ALL":
        files += sorted((R / "backtests").glob("*.py"))
        files += sorted((R / "backtests").glob("*.console.txt"))
        files += sorted((R / "backtests").glob("*.txt"))
        files += sorted(R.glob("*.py"))
    seen, keep = set(), []
    for f in files:
        if f in seen:
            continue
        seen.add(f); keep.append(f)
    return keep


def classify_site(text):
    bar = ("SHARPE" if SHARPE.search(text) else
           "RETURN" if RETURN.search(text) else
           "DD" if DDBAR.search(text) else "NOBAR")
    r, s = bool(RESPR.search(text)), bool(SCAL.search(text))
    typ = "BOTH" if (r and s) else "RESPREAD" if r else "SCALAR" if s else "UNSTATED"
    return bar, typ


def census(claimset):
    rows = []
    for f in corpus_files(claimset):
        try:
            txt = f.read_text(errors="replace")
        except Exception:
            continue
        for i, line in enumerate(txt.split("\n"), 1):
            if not PHRASES.search(line):
                continue
            n = len(PHRASES.findall(line))
            bar, typ = classify_site(line)
            rows.append(dict(claimset=claimset, file=str(f.relative_to(ROOT)), line=i,
                             mentions=n, bar=bar, type=typ,
                             committed=f.name.endswith(".result.md") or f.name in COMMITTED_ROOTS
                                       or f.suffix == ".md",
                             text=line.strip()[:400]))
    return pd.DataFrame(rows)


# ============================================================ PART B — engine twin (idea 460)
def fast_backtest(px, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost, also returning drifted gross."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n); gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index),
            "gross": pd.Series(gross, index=px.index)}


def net(res, bps):
    return res["returns0"] - res["turnover"] * bps / 1e4


def mstats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# ---------------------------------------------------------------- books (idea 460 forms)
def dg_weights(px, gate, g=GROSS, cols=None):
    """De-grossed: g/N on every admitted priced name, gated weight -> CASH, never re-spread."""
    p = px if cols is None else px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(gate.reindex_like(ew).fillna(False), 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def rs_weights(px, gate, g=GROSS, cols=None):
    """RE-SPREAD twin: g/n_admitted on the admitted names, leverage-free."""
    p = px if cols is None else px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    adm = e.where(gate.reindex_like(e).fillna(False), 0.0)
    w = g * adm.div(adm.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def topn_weights(px, n, cols, vol_scale=False, gate=None, g=GROSS):
    p = px[cols]
    s, above, vol20 = score(p, vol_scale=vol_scale)
    elig = s.where(above)
    if gate is not None:
        elig = elig.where(gate.reindex_like(elig).fillna(False))
    rank = elig.rank(axis=1, ascending=False)
    w = (rank <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def lowvol_weights(px, n, cols, g=GROSS):
    p = px[cols]
    vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
    rank = vol20.rank(axis=1, ascending=True)
    w = (rank <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def build_books(px, cols, respread_gates=False):
    """The 12 pre-registered book forms on one panel.  SPY is a benchmark, never held."""
    p = px[cols]
    ma = p.rolling(200).mean()
    vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
    NONE = pd.DataFrame(True, index=p.index, columns=p.columns)
    gw = rs_weights if respread_gates else dg_weights
    B = {}
    B["EWALL"] = dg_weights(px, NONE, cols=cols)
    B["RULESV2"] = gw(px, band_state(p, 0.03), cols=cols)
    B["MA200dg"] = gw(px, (p > ma).fillna(False), cols=cols)
    B["BAND6dg"] = gw(px, band_state(p, 0.06), cols=cols)
    B["ABSdg"] = gw(px, (p > p.shift(252)).fillna(False), cols=cols)
    v1 = topn_weights(px, 5, cols, vol_scale=True)
    ok = (vol20 < 0.60).fillna(False).reindex(columns=px.columns).fillna(False)
    B["TOP5V1"] = (v1.where(ok, 0.0)) * (0.15 * 5 / GROSS)
    B["TOP10"] = topn_weights(px, 10, cols)
    B["TOP20"] = topn_weights(px, 20, cols)
    B["TOP40"] = topn_weights(px, 40, cols)
    B["TOP20V"] = topn_weights(px, 20, cols, vol_scale=True)
    B["TOP20B3"] = topn_weights(px, 20, cols, gate=band_state(p, 0.03))
    B["LOWVOL20"] = lowvol_weights(px, 20, cols)
    return B


def panels():
    out = {}
    u = load_universe(); out["U56"] = (u, [c for c in u.columns])
    b = load_universe(broad=True); out["B136"] = (b, [c for c in b.columns])
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    say(f"    SMALL panel: dropped {len(bad & set(load_universe(small=True).columns))}"
        f" names with max_1d_move >= 1.0; {len([c for c in sm.columns if c != 'SPY'])} remain")
    out["SMALL439"] = (sm, [c for c in sm.columns if c != "SPY"])
    return out


def keep_flags(s, base, spy):
    """4a against the live book (native RULES v2, same panel/window/rung); 4b against SPY."""
    a = (s["H1"] > base["H1"]) and (s["H2"] > base["H2"]) and (s["MaxDD"] >= base["MaxDD"])
    b = (s["H1"] > spy["H1"] and s["H2"] > spy["H2"]
         and s["MaxDD"] >= 0.60 * spy["MaxDD"]          # MaxDD is negative: >= is "no worse"
         and s["CAGR"] >= 0.70 * spy["CAGR"])
    return a, b


def main():
    # ------------------------------------------------------------------ PART A
    say("=" * 100)
    say("PART A — CENSUS of matched-gross claim sites")
    say("=" * 100)
    sites = pd.concat([census(cs) for cs in ("COMMITTED", "ALL")], ignore_index=True)
    sites.to_csv(OUT / f"{STAMP}.sites.csv", index=False)
    cen_rows = []
    for cs in ("COMMITTED", "ALL"):
        s = sites[sites.claimset == cs]
        say(f"\nCLAIMSET={cs}: {len(s)} sites in {s.file.nunique()} files,"
            f" {int(s.mentions.sum())} phrase mentions")
        ct = pd.crosstab(s.bar, s.type)
        for t in ("SCALAR", "RESPREAD", "BOTH", "UNSTATED"):
            if t not in ct.columns:
                ct[t] = 0
        ct = ct[["SCALAR", "RESPREAD", "BOTH", "UNSTATED"]]
        say(ct.to_string())
        sh = s[s.bar == "SHARPE"]
        noop = int((sh.type.isin(["SCALAR", "UNSTATED"])).sum())
        say(f"  SHARPE sites: {len(sh)}   of which SCALAR/UNSTATED (a match that cannot move"
            f" Sharpe): {noop} ({noop / max(len(sh), 1):.1%})")
        for t in ("SCALAR", "RESPREAD", "BOTH", "UNSTATED"):
            n = int((sh.type == t).sum())
            cen_rows.append(dict(claimset=cs, bar="SHARPE", type=t, sites=n,
                                 share=n / max(len(sh), 1)))
        for bar in ("RETURN", "DD", "NOBAR"):
            sb = s[s.bar == bar]
            for t in ("SCALAR", "RESPREAD", "BOTH", "UNSTATED"):
                n = int((sb.type == t).sum())
                cen_rows.append(dict(claimset=cs, bar=bar, type=t, sites=n,
                                     share=n / max(len(sb), 1)))
    pd.DataFrame(cen_rows).to_csv(OUT / f"{STAMP}.census.csv", index=False)

    # ------------------------------------------------------------------ PART B
    say("\n" + "=" * 100)
    say("PART B — MEASUREMENT: what can each match type do to Sharpe?")
    say("=" * 100)
    PX = panels()

    # ---- gates
    say("\n=== GATES ===")
    upx, ucols = PX["U56"]
    st = upx.index[260]
    w2 = rules_v2_weights(upx)
    e_res = engine_backtest(upx, w2, cost_bps=10, freq=FREQ)
    f_res = fast_backtest(upx, w2)
    g1r = float(np.abs((net(f_res, 10) - e_res["returns"]).loc[st:].values).max())
    g1t = float(np.abs((f_res["turnover"] - e_res["turnover"]).loc[st:].values).max())
    say(f"G1 fast_backtest vs engine.backtest  max|dret| {g1r:.3e}  max|dturn| {g1t:.3e}")
    assert g1r < 1e-12 and g1t < 1e-12, "G1 FAILED"
    B3 = band_state(upx[ucols], 0.03)
    g2 = float(np.abs(dg_weights(upx, B3, cols=ucols).values - w2.values).max())
    say(f"G2 dg_weights(BAND3,0.75) == baseline.rules_v2_weights  max|diff| {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED"
    bn = build_books(upx, ucols, respread_gates=False)
    br = build_books(upx, ucols, respread_gates=True)
    g4 = max(float(np.abs(bn[b].values - br[b].values).max()) for b in ["EWALL"] + RANKED)
    g4g = float(np.abs(bn["RULESV2"].values - br["RULESV2"].values).max())
    say(f"G4 RESPREAD == NATIVE for EWALL+RANKED (no gated weight)  max|diff| {g4:.3e};"
        f"  and DIFFERS for a gate book (RULESV2 max|diff| {g4g:.3e})")
    assert g4 < 1e-12 and g4g > 1e-6, "G4 FAILED"

    # ---- run every (panel, type, book) once at zero cost, then apply both rungs
    rows, lad_rows = [], []
    wf_rows = []
    for pname in PANELS:
        px, cols = PX[pname]
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        BN = build_books(px, cols, respread_gates=False)
        BR = build_books(px, cols, respread_gates=True)
        # native results & realised gross
        RES = {b: fast_backtest(px, BN[b]) for b in BOOKS}
        RESR = {b: fast_backtest(px, BR[b]) for b in BOOKS}
        gr_is = {b: float(RES[b]["gross"].loc[start:IS_END].mean()) for b in BOOKS}
        gr_fs = {b: float(RES[b]["gross"].loc[start:].mean()) for b in BOOKS}
        target = float(np.mean([gr_is[b] for b in GATE]))     # IS-fitted, gate-family gross
        kfit = {b: min(1.0, target / gr_is[b]) for b in BOOKS}
        RESS = {b: fast_backtest(px, BN[b] * kfit[b]) for b in BOOKS}
        say(f"\n--- {pname}: window {start.date()}..{px.index[-1].date()},"
            f" {len(cols)} names; IS gate-family mean realised gross target {target:.4f}")
        say("    " + "  ".join(f"{b}:k={kfit[b]:.3f}(g {gr_is[b]:.3f}->"
                               f"{float(RESS[b]['gross'].loc[start:].mean()):.3f})"
                               for b in BOOKS))
        # k-ladder (every book, every k)
        LAD = {}
        for b in BOOKS:
            for k in KLADDER:
                LAD[(b, k)] = RES[b] if k == 1.00 else fast_backtest(px, BN[b] * k)
        for bps in RUNGS:
            spy_s = mstats(spy_r)
            base_s = mstats(net(RES["RULESV2"], bps).loc[start:])
            for b in BOOKS:
                for typ, R in (("NATIVE", RES), ("SCALAR", RESS), ("RESPREAD", RESR)):
                    r = net(R[b], bps).loc[start:]
                    s = mstats(r)
                    ris = net(R[b], bps).loc[start:IS_END]
                    ros = net(R[b], bps).loc[OOS_START:]
                    a, bb = keep_flags(s, base_s, spy_s)
                    rows.append(dict(panel=pname, book=b, family=FAMILY[b], type=typ, bps=bps,
                                     k=kfit[b] if typ == "SCALAR" else 1.0,
                                     gross=float(R[b]["gross"].loc[start:].mean()),
                                     turnover_yr=float(R[b]["turnover"].loc[start:].sum()
                                                       / (len(r) / 252)),
                                     **s,
                                     IS_Sharpe=metrics(ris)["Sharpe"],
                                     OOS_Sharpe=metrics(ros)["Sharpe"],
                                     OOS_CAGR=metrics(ros)["CAGR"],
                                     OOS_MaxDD=metrics(ros)["MaxDD"],
                                     keep4a=a, keep4b=bb))
                for k in KLADDER:
                    r = net(LAD[(b, k)], bps).loc[start:]
                    s = mstats(r)
                    lad_rows.append(dict(panel=pname, book=b, bps=bps, k=k,
                                         gross=float(LAD[(b, k)]["gross"].loc[start:].mean()),
                                         **s))
            # rule 8 per (panel, type, rung)
            for typ, R in (("NATIVE", RES), ("SCALAR", RESS), ("RESPREAD", RESR)):
                iss = {b: metrics(net(R[b], bps).loc[start:IS_END])["Sharpe"] for b in BOOKS}
                pick = max(iss, key=iss.get)
                ros = net(R[pick], bps).loc[OOS_START:]
                bos = net(RES["RULESV2"], bps).loc[OOS_START:]
                sos = spy_r.loc[OOS_START:]
                m, mb, ms = metrics(ros), metrics(bos), metrics(sos)
                wf_rows.append(dict(panel=pname, type=typ, bps=bps, pick=pick,
                                    IS_Sharpe=iss[pick],
                                    OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                                    OOS_MaxDD=m["MaxDD"],
                                    base_OOS_CAGR=mb["CAGR"], base_OOS_Sharpe=mb["Sharpe"],
                                    base_OOS_MaxDD=mb["MaxDD"],
                                    spy_OOS_CAGR=ms["CAGR"], spy_OOS_Sharpe=ms["Sharpe"],
                                    spy_OOS_MaxDD=ms["MaxDD"],
                                    beats_base=m["Sharpe"] > mb["Sharpe"],
                                    beats_spy=m["Sharpe"] > ms["Sharpe"]))
    G = pd.DataFrame(rows); G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    LADdf = pd.DataFrame(lad_rows); LADdf.to_csv(OUT / f"{STAMP}.ladder.csv", index=False)
    WF = pd.DataFrame(wf_rows); WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ---- B1: how far can each match type move Sharpe?
    say("\n=== B1  |dSharpe| of each match type vs its own NATIVE arm (36 book-panel-rung) ===")
    piv = G.pivot_table(index=["panel", "book", "bps"], columns="type",
                        values=["Sharpe", "CAGR", "MaxDD", "gross"])
    b1 = []
    for typ in ("SCALAR", "RESPREAD"):
        for met in ("Sharpe", "CAGR", "MaxDD", "gross"):
            d = (piv[(met, typ)] - piv[(met, "NATIVE")]).dropna()
            b1.append(dict(type=typ, metric=met, n=len(d), max_abs=float(d.abs().max()),
                           median_abs=float(d.abs().median()), mean=float(d.mean())))
    B1 = pd.DataFrame(b1)
    say(B1.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    # restrict RESPREAD to the books it can actually move (gate books)
    gate_idx = piv.index.get_level_values("book").isin(GATE)
    dr = (piv[("Sharpe", "RESPREAD")] - piv[("Sharpe", "NATIVE")])[gate_idx]
    ds = (piv[("Sharpe", "SCALAR")] - piv[("Sharpe", "NATIVE")])[gate_idx]
    say(f"  GATE books only (n={len(dr)}): RESPREAD max|dSharpe| {dr.abs().max():.4f}"
        f" median {dr.abs().median():.4f}  |  SCALAR max|dSharpe| {ds.abs().max():.4f}"
        f" median {ds.abs().median():.4f}")

    # ---- B2: the k-ladder — is scalar Sharpe-neutrality a k-specific artefact?
    say("\n=== B2  K-LADDER: |Sharpe(k*w) - Sharpe(w)| over 7 k-rungs x 12 books x 3 panels"
        " x 2 rungs ===")
    base_k = LADdf[LADdf.k == 1.00].set_index(["panel", "book", "bps"])["Sharpe"]
    LADdf["dSharpe"] = LADdf.apply(
        lambda r: r["Sharpe"] - base_k.loc[(r["panel"], r["book"], r["bps"])], axis=1)
    LADdf["dCAGR"] = LADdf.apply(
        lambda r: r["CAGR"] - LADdf[(LADdf.panel == r["panel"]) & (LADdf.book == r["book"])
                                    & (LADdf.bps == r["bps"]) & (LADdf.k == 1.00)]["CAGR"].iloc[0],
        axis=1)
    LADdf.to_csv(OUT / f"{STAMP}.ladder.csv", index=False)
    tab = LADdf.groupby("k").agg(n=("dSharpe", "size"),
                                 max_abs_dSharpe=("dSharpe", lambda s: s.abs().max()),
                                 med_abs_dSharpe=("dSharpe", lambda s: s.abs().median()),
                                 mean_dCAGR=("dCAGR", "mean"),
                                 max_abs_dCAGR=("dCAGR", lambda s: s.abs().max()))
    say(tab.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"  ALL k<1 rungs pooled (n={int((LADdf.k < 1).sum())}):"
        f" max|dSharpe| {LADdf[LADdf.k < 1]['dSharpe'].abs().max():.4f},"
        f" median {LADdf[LADdf.k < 1]['dSharpe'].abs().median():.4f};"
        f" max|dCAGR| {LADdf[LADdf.k < 1]['dCAGR'].abs().max():.4f}")

    # ---- B3: does the match type change the within-panel Sharpe ORDERING of the books?
    say("\n=== B3  within-panel book ORDERING on Sharpe: does the match type move it? ===")
    ord_rows = []
    for pname in PANELS:
        for bps in RUNGS:
            sub = G[(G.panel == pname) & (G.bps == bps)]
            o = {t: list(sub[sub.type == t].sort_values("Sharpe", ascending=False)["book"])
                 for t in TYPES}
            for t in ("SCALAR", "RESPREAD"):
                same = o[t] == o["NATIVE"]
                # pairwise concordance
                nat = {b: float(sub[(sub.type == "NATIVE") & (sub.book == b)]["Sharpe"].iloc[0])
                       for b in BOOKS}
                alt = {b: float(sub[(sub.type == t) & (sub.book == b)]["Sharpe"].iloc[0])
                       for b in BOOKS}
                flips = sum(1 for i in range(len(BOOKS)) for j in range(i + 1, len(BOOKS))
                            if np.sign(nat[BOOKS[i]] - nat[BOOKS[j]])
                            != np.sign(alt[BOOKS[i]] - alt[BOOKS[j]]))
                ord_rows.append(dict(panel=pname, bps=bps, type=t, order_identical=same,
                                     pair_flips=flips, pairs=len(BOOKS) * (len(BOOKS) - 1) // 2,
                                     native_top=o["NATIVE"][0], alt_top=o[t][0]))
    OD = pd.DataFrame(ord_rows)
    say(OD.to_string(index=False))
    for t in ("SCALAR", "RESPREAD"):
        s = OD[OD.type == t]
        say(f"  {t}: identical full ordering in {int(s.order_identical.sum())}/{len(s)} cells;"
            f" pairwise flips {int(s.pair_flips.sum())}/{int(s.pairs.sum())}"
            f" ({s.pair_flips.sum() / s.pairs.sum():.1%})")

    # ---- KEEP paths
    say("\n=== KEEP PATHS (every one of the %d grid points) ===" % len(G))
    for t in TYPES:
        s = G[G.type == t]
        say(f"  {t:9s} 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}")
    if int(G.keep4b.sum()):
        say("  4b passers:")
        say(G[G.keep4b][["panel", "book", "type", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe"]].to_string(index=False,
                                                  float_format=lambda x: f"{x:.3f}"))

    # ---- RULE 8
    say("\n=== RULE 8 WALK-FORWARD (choose on IS <= %s, read %s.. once) ===" % (IS_END, OOS_START))
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"  picks beating native RULES v2 OOS Sharpe: {int(WF.beats_base.sum())}/{len(WF)};"
        f" beating SPY OOS Sharpe: {int(WF.beats_spy.sum())}/{len(WF)}")
    same_pick = WF.pivot_table(index=["panel", "bps"], columns="type", values="pick",
                               aggfunc="first")
    agree_s = int((same_pick["SCALAR"] == same_pick["NATIVE"]).sum())
    agree_r = int((same_pick["RESPREAD"] == same_pick["NATIVE"]).sum())
    say(f"  rule-8 PICK unchanged by the match: SCALAR {agree_s}/{len(same_pick)},"
        f" RESPREAD {agree_r}/{len(same_pick)}")

    # ---- PART C: join the census to the measured bound
    say("\n" + "=" * 100)
    say("PART C — how many published Sharpe conclusions rest on a match that cannot move Sharpe")
    say("=" * 100)
    bound = float(LADdf[LADdf.k < 1]["dSharpe"].abs().max())
    for cs in ("COMMITTED", "ALL"):
        sh = sites[(sites.claimset == cs) & (sites.bar == "SHARPE")]
        noop = int(sh.type.isin(["SCALAR", "UNSTATED"]).sum())
        say(f"  {cs:9s}: {len(sh)} Sharpe-bar matched-gross sites; {noop} "
            f"({noop / max(len(sh), 1):.1%}) name a SCALAR match or name none at all, and the "
            f"measured ceiling on what a scalar match can do to Sharpe is {bound:.4f}.")
    say(f"  Measured ceiling |dSharpe| for a scalar (exposure-level) match: {bound:.4f}"
        f"  — versus a RESPREAD match on gate books: {dr.abs().max():.4f}"
        f" (median {dr.abs().median():.4f}).")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    say("\nwrote .census.csv .sites.csv .grid.csv .ladder.csv .walkforward.csv .console.txt")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
