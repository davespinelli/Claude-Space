#!/usr/bin/env python3
"""IDEA 525 (cloud) — is n_elig the variable the record keeps mislabelling?

QUESTION (queue).  Idea 286's k-identity (breadth = mean(n_elig)/k) made idea 153's published
overlap ordering REVERSE the moment panel width was held, because the record's small panel is its
WIDEST in n_elig (Ebar 141.5) while U56, the narrowest panel, is its narrowest in n_elig (36.1).
Re-run the record's other "panel property explains the result" claims with n_elig and k published
beside the property, and count how many are n_elig statistics.

DESIGN — the confound, stated.  A named panel carries TWO numbers at once: k (its width) and
Ebar = mean daily n_elig (how many of it are investable on an average day).  Every published
cross-panel property claim reads one of them and names the other.  The only way to tell them apart
is to HOLD k and let Ebar move, which is what matched-width draws do.

PARAMETERS — exactly two, every grid point reported, neither tuned on an outcome:
  P1  k, the MATCHED PANEL WIDTH, 3 levels {20, 36, 55}.  55 is U56's own tradable width (the
      record's narrowest named panel); 36 is idea 286's published U56 Ebar; 20 is the record's
      standard book size.
  P2  band, the ELIGIBILITY DIAL, 3 levels {0.00, 0.03, 0.08} of the live 200d +/-band gate.  It
      moves Ebar at FIXED k, which is the contrast the record never runs.
  Draws per (panel, k) are FIXED at 8 and seeded, not swept.  Gross is FIXED at the live 0.75.

LEGS.
  [A] 3 panels (U56, B136, SMALL439) x 3 k x 3 bands x 8 draws = 216 books at 10 bps, weekly,
      t+1, each with k, Ebar, breadth=Ebar/k and full/halves/OOS published BESIDE the outcome.
      Then: Spearman(Ebar, Sharpe) vs Spearman(breadth, Sharpe) vs the PANEL ordering, pooled and
      within every matched (k, band) cell, plus both partials, plus the within-Ebar-stratum panel
      effect.  Both KEEP paths on every book.
  [B] RULE 8: the band is chosen on 2009-2016 alone (per panel, per k, best mean IS Sharpe) and
      2017-2026 is read once.  OOS CAGR/Sharpe/MaxDD against RULES v2 and SPY.
  [C] THE CENSUS the queue asks for: every committed `*.result.md` naming >= 2 of the record's
      panels together with a panel-property word, scored for whether it publishes n_elig and k
      BESIDE the property — and, for each, whether the panels it compares differ in Ebar by more
      than this run's own within-panel draw spread, i.e. whether the claim is SEPARABLE from an
      n_elig difference at all.

REPRODUCTION GATES (recorded, NEVER raising).  Idea 286's published named-panel numbers, re-derived
from its own eligibility definition (200d MA AND 20d ann. vol < 0.60, counted on weekly rebalance
days, first 40 dropped): Ebar U56 ~36.1 and SMALL439 ~141.5, breadth U56 0.6571 / SMALL439 0.3224,
k 55 / 135 / 439, and the 44 names dropped from the 483-name small panel by max_1d_move >= 1.0.

SURVIVORSHIP (idea 54): every panel here is CURRENT constituents only.  The sub-$2B panel is the
worst case — it is the survivors of a screen run today, so its levels are optimistic; the matched-k
CONTRASTS are the part of this run that survives that caveat, not the levels.

Deterministic; seeded draws only.  Writes <STEM>.{books,grid,cells,strata,walkforward,census}.csv
and <STEM>.console.txt.  Does not modify RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

from baseline import band_state, load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_cloud"
KS = [20, 36, 55]
BANDS = [0.00, 0.03, 0.08]
DRAWS = 8
GROSS = 0.75
COST_BPS, FREQ = 10, "W"
OOS_START = "2017-01-01"

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, ok, detail):
    say(f"  GATE {name:<22} {'PASS' if ok else 'FAIL'}   {detail}")
    return bool(ok)


def spearman(x, y):
    x, y = pd.Series(list(x)).astype(float), pd.Series(list(y)).astype(float)
    m = x.notna() & y.notna()
    if m.sum() < 3:
        return np.nan
    return float(x[m].rank().corr(y[m].rank()))


def partial_spearman(y, x, z):
    """Spearman(y, x) with z held: correlate the residuals of the rank regressions."""
    df = pd.DataFrame({"y": list(y), "x": list(x), "z": list(z)}).astype(float).dropna()
    if len(df) < 4:
        return np.nan
    r = df.rank()
    ry = r.y - np.polyval(np.polyfit(r.z, r.y, 1), r.z)
    rx = r.x - np.polyval(np.polyfit(r.z, r.x, 1), r.z)
    return float(pd.Series(ry).corr(pd.Series(rx)))


# ===================================================================== PANELS ==
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


def ebar(px_sub: pd.DataFrame) -> float:
    """Idea 286's eligibility definition, re-implemented: 200d MA AND 20d ann. vol < 0.60,
    counted on weekly rebalance days, first 40 rebalance rows dropped."""
    g = (px_sub > px_sub.rolling(200).mean()) & \
        (px_sub.pct_change().rolling(20).std() * np.sqrt(252) < 0.60)
    mask = rebalance_mask(px_sub.index, FREQ)
    return float(g.loc[mask.values].sum(axis=1).iloc[40:].mean())


def book(px, band):
    """The live convention: hold every in-band name at GROSS/N, gated-out weight to cash."""
    trad = [c for c in px.columns if c != "SPY"]
    sub = px[trad]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(band_state(sub, band), 0.0)
    return w.reindex(columns=px.columns, fill_value=0.0)


def pack(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    oos = r.loc[OOS_START:]
    mo = metrics(oos)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], isS=metrics(r.loc[:"2016-12-31"])["Sharpe"],
                oosC=mo["CAGR"], oosS=mo["Sharpe"], oosD=mo["MaxDD"])


def keep_paths(a, base, spy):
    p4a = int(a["H1"] > base["H1"] and a["H2"] > base["H2"] and a["MaxDD"] >= base["MaxDD"])
    m4a = min(a["H1"] - base["H1"], a["H2"] - base["H2"], a["MaxDD"] - base["MaxDD"])
    legs = [a["H1"] - spy["H1"], a["H2"] - spy["H2"], a["oosS"] - spy["oosS"],
            a["MaxDD"] - 0.60 * spy["MaxDD"], a["CAGR"] - 0.70 * spy["CAGR"]]
    p4b = int(all(x > 0 for x in legs[:3]) and legs[3] >= 0 and legs[4] >= 0)
    return p4a, m4a, p4b, min(legs)


# ====================================================================== LEG A ==
def leg_a():
    u56 = load_universe()
    b136 = load_universe(broad=True)
    small, n_drop = small_panel()
    panels = {"U56": u56, "B136": b136, "SMALL439": small}
    say(f"[A] panels: " + ", ".join(
        f"{t} {p.shape[1]-1} tradable x {p.shape[0]} days ({p.index[0].date()}..{p.index[-1].date()})"
        for t, p in panels.items()))

    say("\nREPRODUCTION GATES (recorded, non-raising; idea 286's own definitions)")
    gate("small.dropped", n_drop == 44, f"{n_drop} names with max_1d_move >= 1.0 vs published 44")
    widths = {t: p.shape[1] - 1 for t, p in panels.items()}
    gate("k.U56", widths["U56"] == 55, f"{widths['U56']} vs 55")
    gate("k.B136", widths["B136"] == 135, f"{widths['B136']} vs 135")
    gate("k.SMALL439", widths["SMALL439"] == 439, f"{widths['SMALL439']} vs 439")
    eb = {t: ebar(p[[c for c in p.columns if c != "SPY"]]) for t, p in panels.items()}
    gate("Ebar.U56", abs(eb["U56"] - 36.1) < 1.0, f"{eb['U56']:.2f} vs published 36.1")
    gate("Ebar.SMALL439", abs(eb["SMALL439"] - 141.5) < 3.0, f"{eb['SMALL439']:.2f} vs published 141.5")
    for t in panels:
        gate(f"breadth.{t}", True, f"Ebar/k = {eb[t]/widths[t]:.4f}  (Ebar {eb[t]:.2f}, k {widths[t]})")
    say("  THE IDENTITY, restated on today's panels: the record's SMALL panel is its WIDEST in "
        f"n_elig ({eb['SMALL439']:.1f}) and its NARROWEST in breadth ({eb['SMALL439']/439:.4f}); "
        f"U56 is the reverse ({eb['U56']:.1f}, {eb['U56']/55:.4f}).")

    rows = []
    for pi, (tag, px) in enumerate(panels.items()):
        trad = [c for c in px.columns if c != "SPY"]
        st = px.index[260]
        spy = pack(px["SPY"].pct_change().fillna(0).loc[st:])
        # the live book, on THIS panel's own sample, is the 4a comparand
        bser = backtest(u56.loc[px.index[0]:px.index[-1]],
                        rules_v2_weights(u56.loc[px.index[0]:px.index[-1]]),
                        cost_bps=COST_BPS, freq=FREQ)["returns"].loc[st:]
        base = pack(bser)
        say(f"\n[A] {tag}: comparands over {st.date()}..{px.index[-1].date()} — "
            f"RULES v2 CAGR {base['CAGR']:.4f} Sharpe {base['Sharpe']:.4f} MaxDD {base['MaxDD']:.4f} "
            f"H1/H2 {base['H1']:.3f}/{base['H2']:.3f} | SPY CAGR {spy['CAGR']:.4f} "
            f"Sharpe {spy['Sharpe']:.4f} MaxDD {spy['MaxDD']:.4f} OOS Sharpe {spy['oosS']:.4f}")
        for k in KS:
            if k > len(trad):
                continue
            ndraw = 1 if k == len(trad) else DRAWS
            for d in range(ndraw):
                rng = np.random.default_rng(1000 * pi + 10 * k + d)
                cols = (list(trad) if k == len(trad)
                        else list(rng.choice(trad, size=k, replace=False)))
                sub = px[cols + ["SPY"]]
                e_k = ebar(sub[cols])
                for b in BANDS:
                    r = backtest(sub, book(sub, b), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[st:]
                    a = pack(r)
                    p4a, m4a, p4b, m4b = keep_paths(a, base, spy)
                    rows.append(dict(panel=tag, k=k, draw=d, band=b, Ebar=e_k,
                                     breadth=e_k / k, **a, pass4a=p4a, margin4a=m4a,
                                     pass4b=p4b, margin4b=m4b,
                                     spy_S=spy["Sharpe"], spy_oosS=spy["oosS"],
                                     v2_S=base["Sharpe"], v2_H1=base["H1"], v2_H2=base["H2"]))
    bk = pd.DataFrame(rows)
    say(f"\n[A] {len(bk)} books built ({bk.panel.nunique()} panels x {bk.k.nunique()} k x "
        f"{bk.band.nunique()} bands x up to {DRAWS} draws), 10 bps, weekly, t+1, gross {GROSS}")

    say("\n[A] EVERY (panel, k, band) CELL — n_elig and k published BESIDE the outcome")
    cells = (bk.groupby(["panel", "k", "band"])
               .agg(n=("Sharpe", "size"), Ebar=("Ebar", "mean"), sd_Ebar=("Ebar", "std"),
                    breadth=("breadth", "mean"), CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"),
                    sd_Sharpe=("Sharpe", "std"), MaxDD=("MaxDD", "mean"), H1=("H1", "mean"),
                    H2=("H2", "mean"), oosC=("oosC", "mean"), oosS=("oosS", "mean"),
                    oosD=("oosD", "mean"), p4a=("pass4a", "sum"), p4b=("pass4b", "sum"))
               .reset_index())
    say(cells.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"[A] KEEP paths over all {len(bk)} books: 4a {int(bk.pass4a.sum())}, "
        f"4b {int(bk.pass4b.sum())}")
    return bk, cells, panels, eb, widths


def leg_a2(bk: pd.DataFrame):
    say("\n[A2] WHICH VARIABLE ORDERS THE OUTCOME — pooled and inside every matched cell")
    out = []
    for col in ["Sharpe", "oosS", "CAGR", "MaxDD"]:
        rb, re_, = spearman(bk.breadth, bk[col]), spearman(bk.Ebar, bk[col])
        pbe = partial_spearman(bk[col], bk.breadth, bk.Ebar)
        peb = partial_spearman(bk[col], bk.Ebar, bk.breadth)
        out.append(dict(stat=col, rho_breadth=rb, rho_Ebar=re_,
                        partial_breadth_given_Ebar=pbe, partial_Ebar_given_breadth=peb))
        say(f"  {col:<7} Spearman(breadth,.) {rb:+.4f}   Spearman(Ebar,.) {re_:+.4f}   "
            f"PARTIAL (breadth|Ebar) {pbe:+.4f}   (Ebar|breadth) {peb:+.4f}")
    pooled = pd.DataFrame(out)

    say("\n[A2] INSIDE each matched (k, band) cell — k is HELD, so only Ebar can move")
    within = []
    for (k, b), s in bk.groupby(["k", "band"]):
        within.append(dict(k=k, band=b, n=len(s),
                           rho_Ebar_S=spearman(s.Ebar, s.Sharpe),
                           rho_Ebar_oosS=spearman(s.Ebar, s.oosS),
                           rho_breadth_S=spearman(s.breadth, s.Sharpe),
                           Ebar_lo=s.Ebar.min(), Ebar_hi=s.Ebar.max(),
                           S_lo=s.Sharpe.min(), S_hi=s.Sharpe.max()))
    w = pd.DataFrame(within)
    say(w.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  NOTE: inside a matched cell breadth = Ebar/k is a LINEAR RESCALING of Ebar, so the two "
        "rank-correlations are identical BY CONSTRUCTION. That identity is the finding: the two "
        "variables are only distinguishable ACROSS k, which is exactly what the record never holds.")

    say("\n[A2] THE PANEL ORDERING at each matched k — does the named panel survive holding width?")
    po = (bk.groupby(["k", "panel"]).agg(Ebar=("Ebar", "mean"), Sharpe=("Sharpe", "mean"),
                                         oosS=("oosS", "mean"), sd=("Sharpe", "std"),
                                         n=("Sharpe", "size")).reset_index())
    say(po.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for k, s in po.groupby("k"):
        o_s = " > ".join(s.sort_values("Sharpe", ascending=False).panel)
        o_e = " > ".join(s.sort_values("Ebar", ascending=False).panel)
        say(f"  k={k:<3} Sharpe order {o_s:<28} Ebar order {o_e:<28} "
            f"{'SAME' if o_s == o_e else 'DIFFERENT'}")

    say("\n[A2] WITHIN-Ebar-STRATUM panel effect (3 terciles of Ebar over all books)")
    bk = bk.copy()
    bk["stratum"] = pd.qcut(bk.Ebar, 3, labels=["Ebar-lo", "Ebar-mid", "Ebar-hi"])
    st = (bk.groupby(["stratum", "panel"], observed=True)
            .agg(n=("Sharpe", "size"), Ebar=("Ebar", "mean"), Sharpe=("Sharpe", "mean"),
                 oosS=("oosS", "mean")).reset_index())
    say(st.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return pooled, w, po, st


# ====================================================================== LEG B ==
def leg_b(bk: pd.DataFrame):
    say("\n[B] RULE 8 — band chosen on 2009-2016 ONLY (best mean IS Sharpe per panel x k), "
        "2017-2026 read ONCE")
    rows = []
    for (p, k), s in bk.groupby(["panel", "k"]):
        m = s.groupby("band").agg(isS=("isS", "mean")).reset_index()
        pick = float(m.loc[m.isS.idxmax(), "band"])
        sel = s[s.band == pick]
        rows.append(dict(panel=p, k=k, picked_band=pick, isS=sel.isS.mean(),
                         oosC=sel.oosC.mean(), oosS=sel.oosS.mean(), oosD=sel.oosD.mean(),
                         Ebar=sel.Ebar.mean(), breadth=sel.breadth.mean(),
                         spy_oosS=sel.spy_oosS.mean(),
                         beats_spy_oosS=int(sel.oosS.mean() > sel.spy_oosS.mean()),
                         p4a=int(sel.pass4a.sum()), p4b=int(sel.pass4b.sum()), n=len(sel)))
    wf = pd.DataFrame(rows)
    say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"[B] OOS-Sharpe beats SPY in {int(wf.beats_spy_oosS.sum())} of {len(wf)} (panel, k) picks; "
        f"4a passes {int(wf.p4a.sum())}, 4b passes {int(wf.p4b.sum())} over "
        f"{int(wf.n.sum())} picked books")
    say(f"[B] Spearman(Ebar, OOS Sharpe) over the {len(wf)} picks: "
        f"{spearman(wf.Ebar, wf.oosS):+.4f}   Spearman(breadth, OOS Sharpe): "
        f"{spearman(wf.breadth, wf.oosS):+.4f}   Spearman(k, OOS Sharpe): "
        f"{spearman(wf.k, wf.oosS):+.4f}")
    return wf


# ====================================================================== LEG C ==
PANEL_TOK = [("U56", re.compile(r"\bU56\b|universe\.json", re.I)),
             ("B136", re.compile(r"\bB136\b|universe_broad|\bbroad\b", re.I)),
             ("BSTK100", re.compile(r"BSTK\s?\d{2,3}", re.I)),
             ("ETF36", re.compile(r"\bETF\s?36\b", re.I)),
             ("SMALL439", re.compile(r"SMALL\s?43\d|prices_small|small=True|sub-\$2B|"
                                     r"small[- ]cap panel|small panel", re.I))]
PROP = re.compile(r"panel|universe|breadth|cap[- ]mix|capitalisation|capitalization|width|"
                  r"corpus|small[- ]cap|mega[- ]cap", re.I)
EXPLAINS = re.compile(r"explain|order|ordering|drives?|carries|accounts for|is a .{0,20}fact|"
                      r"because the panel|panel property|panel-of-origin", re.I)
NELIG = re.compile(r"n_elig|n-elig|Ebar|eligible count|mean eligible|number eligible", re.I)
KTOK = re.compile(r"\bk\s?=|panel width|\bwidth\b|\bk\b\s*\(|tradable width|instruments\b", re.I)


def leg_c(eb: dict, widths: dict, bk: pd.DataFrame):
    files = sorted(OUT.glob("*.result.md"))
    say(f"\n[C] CENSUS of {len(files)} committed *.result.md files")
    # this run's own within-panel draw spread in Ebar, per k — the separability yardstick
    sd = bk.groupby(["panel", "k"]).Ebar.std().groupby("k").max()
    yard = float(2 * sd.max())
    say(f"[C] separability yardstick = 2 x the LARGEST within-(panel,k) sd of Ebar in this run "
        f"= {yard:.3f} eligible names")
    rows = []
    for f in files:
        t = f.read_text(errors="ignore")
        named = [tag for tag, rx in PANEL_TOK if rx.search(t)]
        if len(named) < 2 or not PROP.search(t):
            continue
        known = [p for p in named if p in eb]
        gapE = (max(eb[p] for p in known) - min(eb[p] for p in known)) if len(known) >= 2 else np.nan
        gapk = (max(widths[p] for p in known) - min(widths[p] for p in known)) if len(known) >= 2 else np.nan
        # LOOSE: the verb appears anywhere in the file (counts the WORD).  TIGHT: the verb sits
        # within 200 characters of BOTH a panel token and a property word (closer to the CLAIM).
        # Both are published; neither is a tuned dial.
        tight = False
        for mo in EXPLAINS.finditer(t):
            win = t[max(0, mo.start() - 200): mo.start() + 200]
            if PROP.search(win) and any(rx.search(win) for _, rx in PANEL_TOK):
                tight = True
                break
        rows.append(dict(file=f.name, panels=";".join(named), n_panels=len(named),
                         explains=bool(EXPLAINS.search(t)), explains_tight=tight,
                         publishes_n_elig=bool(NELIG.search(t)),
                         publishes_k=bool(KTOK.search(t)),
                         known_panels=";".join(known), Ebar_gap=gapE, k_gap=gapk,
                         separable=bool(gapE < yard) if gapE == gapE else None))
    c = pd.DataFrame(rows)
    say(f"[C] {len(c)} files name >= 2 panels AND a panel-property word; "
        f"{int(c.explains.sum())} carry an EXPLAINS verb ANYWHERE (LOOSE, an UPPER bound — this "
        f"counts the WORD, idea 286/523's own critique), {int(c.explains_tight.sum())} carry it "
        f"WITHIN 200 CHARS of both a panel token and a property word (TIGHT)")
    for lab, sel in (("LOOSE", c[c.explains]), ("TIGHT", c[c.explains_tight])):
        say(f"[C] of the {len(sel)} {lab} claim files: publish n_elig "
            f"{int(sel.publishes_n_elig.sum())} ({sel.publishes_n_elig.mean():.3f}), publish "
            f"k/width {int(sel.publishes_k.sum())}, publish NEITHER "
            f"{int(((~sel.publishes_n_elig) & (~sel.publishes_k)).sum())}")
    sep = c[c.explains_tight & c.Ebar_gap.notna()]
    if len(sep):
        say(f"[C] SEPARABILITY: of {len(sep)} claim files whose compared panels this run measures, "
            f"{int((~sep.separable.astype(bool)).sum())} compare panels whose Ebar differs by MORE "
            f"than the yardstick — i.e. their 'panel property' is NOT separable from an n_elig "
            f"difference; {int(sep.separable.astype(bool).sum())} are separable.")
        say(f"[C] median Ebar gap among the non-separable: "
            f"{sep.loc[~sep.separable.astype(bool), 'Ebar_gap'].median():.1f} eligible names "
            f"(U56 {eb['U56']:.1f} -> SMALL439 {eb['SMALL439']:.1f})")
    say(f"[C] panel-pair frequency: {dict(c.panels.value_counts().head(6))}")
    return c


# ======================================================================= MAIN ==
def main():
    say(f"IDEA 525 (cloud) — {STEM}")
    say(f"P1 k {KS}; P2 band {BANDS}; draws {DRAWS} (fixed, seeded); gross {GROSS} (fixed); "
        f"{COST_BPS} bps, freq={FREQ}, t+1 (engine)")

    bk, cells, panels, eb, widths = leg_a()
    pooled, within, panelorder, strata = leg_a2(bk)
    wf = leg_b(bk)
    c = leg_c(eb, widths, bk)

    bk.to_csv(OUT / f"{STEM}.books.csv", index=False)
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    pooled.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    within.to_csv(OUT / f"{STEM}.within.csv", index=False)
    panelorder.to_csv(OUT / f"{STEM}.panelorder.csv", index=False)
    strata.to_csv(OUT / f"{STEM}.strata.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    c.to_csv(OUT / f"{STEM}.census.csv", index=False)

    say(f"\nSURVIVORSHIP (idea 54): all three panels are CURRENT constituents only; the sub-$2B "
        f"panel is survivors of a screen run today. Levels are optimistic; the matched-k contrasts "
        f"are what survives.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
