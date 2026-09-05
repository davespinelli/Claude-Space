#!/usr/bin/env python3
"""QUEUE idea 158 — does-share-price-any-key-or-only-vol  (lane B, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 158)
    "idea 153 showed book share governs the realised magnitude of the VOL tilt (R2 0.43-0.60
     vs the key's own t at 0.01-0.11).  If the mechanism is arithmetic (a book holding half
     the panel cannot express a ranking) it must hold for EVERY key.  Re-run the identical
     overlap regression with the composite's own three legs (12-1, 6m, 3m) and a random key
     as the tilt, on the same share grid.  A random key is the decisive control: its
     |dSharpe| must fall with overlap too.  Max 2 params."

WHAT IS AT STAKE.  Idea 153 concluded that HOW MUCH OF THE PANEL YOU HOLD prices a
    cross-sectional tilt better than HOW STRONG THE KEY IS, and that conclusion is now load-
    bearing: idea 159 built its value/cost parallelism on it, idea 168 re-read the whole
    delete-the-scaler record through it, and idea 124's book-size floor was sent looking for
    another argument because of it.  But idea 153 measured ONE key (vol20).  With one key,
    "overlap prices the tilt" and "vol20 in particular is weak on high-overlap panels" are
    the same regression.  The only way to separate them is to swap the key and keep
    everything else identical.  A key with NO information at all is the decisive instrument:
    if the mechanism is arithmetic, a random key's |dSharpe| must decay with overlap exactly
    as vol20's does; if instead the decay is something about vol20, the random key will show
    a flat or noisy relationship.

    This run therefore does not test a trading rule.  It tests whether a published mechanism
    claim is a mechanism or a coincidence.  No book here is proposed for anything.

CORPUS
    3 panels (u56 / broad / small) x 7 book shares x 13 books per cell
    (1 no-tilt control + 6 keys x 2 tilt directions) = 273 backtests, each run ONCE at 0 bps
    with the 10 and 25 bps rungs derived exactly from the engine's own cost identity
    r_c = r_0 - turnover * c / 1e4 (verified to 0 below), so gross and net legs of every
    comparison are the SAME book.  Weekly, t+1, 75% gross, no shorting, no leverage.

TUNED PARAMETERS — exactly two, both swept exhaustively, ALL grid points reported:
    1. the target BOOK SHARE m in {0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00}, realised as
       n = max(2, round(m x mean weekly eligible count of that panel)) — idea 153's own map,
       so m = 0.53 is n = 20 on u56 (the incumbent) exactly.
    2. the TILT DIRECTION in {NEG, NONE, POS} (divide by / ignore / multiply by the key's
       damped multiplier), idea 153's INV/NONE/POS generalised off vol20.
    The KEY is a REPORTED axis, never selected on — comparing keys IS the question, the way
    idea 153 compared panels.  Panels, cost rungs, the OOS window and every diagnostic are
    likewise reported, never selected on.  The 200d gate and vol20 < 0.60 stay at v1's values.

THE SIX KEYS (the tilt multiplier g, applied as score = comp / g, comp, comp * g)
    VOL   idea 153 VERBATIM: g = clip(vol20, 0.08) ** 0.5.  NEG == RULES v1's live scaler.
    VOLR  the same key put on the common footing: g = clip(rank_pct(vol20), 0.05, 1) ** 0.5.
    MOM   g = clip(rank_pct(12-1 momentum), 0.05, 1) ** 0.5      } the composite's
    R6    g = clip(rank_pct(6m return),     0.05, 1) ** 0.5      } own three
    R3    g = clip(rank_pct(3m return),     0.05, 1) ** 0.5      } legs
    RAND  g = clip(rank_pct(RW6), 0.05, 1) ** 0.5, where RW6 is the 126-day change of a
          SYNTHETIC geometric random walk per name (seed 158, daily vol = the panel's own
          median daily vol).  Built with R6's exact functional form so it matches the real
          keys' persistence and turnover, and carries zero information by construction.
          This is the decisive control.

DEPENDENT VARIABLE, fixed before any number was read
    Idea 153's, verbatim: dSharpe = Sharpe(tilt) - Sharpe(NONE) at matched (panel, m, cost),
    regressand |dSharpe| (and |dCAGR|).  Overlap is idea 153's own definition: the mean over
    daily rows of |A n B| / |A u B| of the two books' HELD sets.

CONFOUNDS, declared before the result
    (i) m -> 1.00 forces every arm onto the same eligible set, so overlap -> 1 and dSharpe
        -> 0 MECHANICALLY.  Every regression is therefore run twice, on the full grid and on
        m <= 0.53 only, and the endpoint is never quoted as evidence.
    (ii) MOM/R6/R3 are LEGS OF THE COMPOSITE ITSELF, so their books overlap the NONE control
        more at every share than an unrelated key's would.  A POOLED cross-key regression of
        |dSharpe| on overlap therefore partly measures key-vs-composite correlation, not
        share.  The decisive statistic is consequently the WITHIN-KEY one, where m is the
        only thing that moves; the pooled fit is reported for comparability with idea 153
        and is read second, not first.
    (iii) The literal GROSS/n book de-grosses when fewer than n names are eligible (idea 81).
        Realised mean gross is a printed column and the whole grid is re-run gross-normalised
        at 10 bps as a control.

REPRODUCTION, asserted before any new number is read (5 checks)
    [a] idea 153's mean weekly eligible counts: u56 37.50, broad 91.46, small 141.23.
    [b] idea 153's published INV-vs-NONE overlap at n=20: u56 69.4%, broad 42.5%.
    [c] idea 81/153/159/168's control book NONE / n=20 / u56 @ 10 bps:
        12.65974% / 1.09214 / -18.30835%, halves 1.08828 / 1.10155.
    [d] the cost identity r_c = r_0 - turnover * c / 1e4 against a fresh 10 bps engine run.
    [e] RULES v1 on u56 @ 10 bps: 6.45305% / 0.66418 / -13.82780%.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  Reproduction [a]-[e] holds.
    P2  Overlap is monotone increasing in book share within every (panel, key, direction).
    P3  THE DECISIVE ONE.  Within EVERY key including RAND, on the large-cap panels and the
        m <= 0.53 subgrid, Spearman(overlap, |dSharpe|) is negative.
    P4  Pooled on the RAND rows ALONE, the OLS slope of |dSharpe| on overlap is negative with
        |t| > 2, and RAND's R^2 is at least half the mean R^2 of the five real keys.
    P5  The keys' own information does NOT order the tilts they buy: across the six keys,
        Spearman(|rank IC of the key|, mean |dSharpe|) is not positive with |t| > 2.
    P6  Nothing here is a KEEP: no (m, key, direction) passes 4b on more than one panel other
        than by being idea 153's already-published no-tilt candidate under another name.

WALK-FORWARD (PROTOCOL rule 8), selection rules fixed BEFORE any OOS number is read
    (m, key, direction) chosen on 2009-2016 only, the pick read ONCE on 2017-01-01..2026.
    S1 IS-Sharpe argmax over all 91 arms; S2 the do-nothing control (NONE at m = 0.53, i.e.
    the incumbent book, no selection at all); S3 IS-Sharpe argmax restricted to the RAND key
    (a null selector: if S1 ~ S3 the selection is picking noise); S4 IS-Sharpe argmax over
    the NONE arms only (share chosen, no tilt allowed).  Reported as OOS CAGR/Sharpe/MaxDD
    against RULES v1 (same panel, same cost) and SPY.  Both KEEP paths (4a and 4b) are
    evaluated at every one of the 273 books, on the full sample and on the OOS window alone.

CAVEATS carried, not buried
    * Survivorship: all three panels are current-constituent lists (idea 54).
    * Ideas 39/49: the eligibility gate is INVERTED on the small panel, so its numbers are
      about a gate that does not work there; reported, never traded.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 only, no spread or impact model).
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's.
    * m is a sample-average share, not a point-in-time one (idea 157 is the time-varying test).
    * One realised path, measured once; a random key is ONE draw of a random key.

HARNESS
    `baseline` (the live rules), idea 94's window/halves/4a/spearman machinery and idea 129's
    panel and 4b-bar machinery are IMPORTED, so the control arm and the bars are literally the
    committed ones.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .overlap.csv, .delta.csv,
.regression.csv, .ic.csv, .walkforward.csv.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_does-share-price-any-key-or-only-vol_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")

FREQ = "W"
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
OOS_START = H.OOS_START
PHI0, DELTA0 = 0.70, 0.60
GROSS, MAX_VOL = 0.75, 0.60
SEED = 158

SHARES = [0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00]   # tuned parameter 1
DIRS = ["NEG", "NONE", "POS"]                         # tuned parameter 2
KEYS = ["VOL", "VOLR", "MOM", "R6", "R3", "RAND"]     # reported axis
REAL_KEYS = ["VOL", "VOLR", "MOM", "R6", "R3"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the book (idea 153 verbatim)
_P = {}


def parts(px, pk):
    """composite, 200d gate, vol20 — idea 81/153's `parts`, plus the six tilt multipliers."""
    if pk in _P:
        return _P[pk]
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
            + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    v = px.pct_change().rolling(20).std() * np.sqrt(252)

    # --- the synthetic random key: R6's exact functional form on a zero-information path
    rng = np.random.default_rng(SEED)
    sd = float(np.nanmedian(px.pct_change().std().values))
    steps = rng.normal(0.0, sd, size=px.shape)
    rw = pd.DataFrame(np.exp(np.cumsum(steps, axis=0)), index=px.index, columns=px.columns)
    rw6 = rw / rw.shift(126) - 1

    def rk(x):
        return x.rank(axis=1, pct=True).clip(lower=0.05, upper=1.0) ** 0.5

    G = {"VOL": v.clip(lower=0.08) ** 0.5,   # idea 153's LEVEL form, verbatim
         "VOLR": rk(v), "MOM": rk(mom), "R6": rk(r6), "R3": rk(r3), "RAND": rk(rw6)}
    RAW = {"VOL": v, "VOLR": v, "MOM": mom, "R6": r6, "R3": r3, "RAND": rw6}
    _P[pk] = (comp, above, v, G, RAW)
    return _P[pk]


def score_of(px, pk, key, d):
    comp, above, v, G, _ = parts(px, pk)
    if d == "NONE":
        return comp
    g = G[key]
    return comp / g if d == "NEG" else comp * g


def held_mask(px, pk, key, d, n):
    _, above, v, _, _ = parts(px, pk)
    s = score_of(px, pk, key, d)
    return s.where(above & (v < MAX_VOL)).rank(axis=1, ascending=False) <= n


def weights(px, pk, key, d, n, constr="lit"):
    m = held_mask(px, pk, key, d, n).astype(float)
    if constr == "lit":
        return m * (GROSS / n)
    k = m.sum(axis=1).replace(0, np.nan)
    return m.div(k, axis=0).fillna(0.0) * GROSS


def eligible_mask(px, pk):
    _, above, v, _, _ = parts(px, pk)
    return above & (v < MAX_VOL)


def overlap(A, B):
    """Idea 153/81's definition: mean over daily rows of |A n B| / |A u B| of the held sets."""
    inter = (A & B).sum(axis=1)
    un = (A | B).sum(axis=1).replace(0, np.nan)
    return float((inter / un).mean())


def ols(y, X, names):
    X = np.column_stack([np.ones(len(y))] + [np.asarray(x, float) for x in X])
    y = np.asarray(y, float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(len(y) - X.shape[1], 1)
    s2 = resid @ resid / dof
    se = np.sqrt(np.maximum(np.diag(np.linalg.pinv(X.T @ X)) * s2, 1e-30))
    ss = ((y - y.mean()) ** 2).sum()
    return (dict(zip(["const"] + names, beta)), dict(zip(["const"] + names, beta / se)),
            (1 - (resid @ resid) / ss) if ss > 0 else np.nan)


def rank_ic(key_df, px, elig, start, h=21):
    """Mean cross-sectional Spearman(key, forward h-day return) over weekly dates, and its t."""
    fwd = px.shift(-h) / px - 1
    idx = key_df.loc[start:].index
    idx = idx[::5]
    ics = []
    K = key_df.reindex(idx)
    F = fwd.reindex(idx)
    E = elig.reindex(idx)
    for d in idx:
        k, f, e = K.loc[d], F.loc[d], E.loc[d]
        ok = e.fillna(False) & k.notna() & f.notna()
        if int(ok.sum()) < 8:
            continue
        ics.append(H.spearman(k[ok].values, f[ok].values))
    ics = np.array([x for x in ics if np.isfinite(x)])
    if len(ics) < 20:
        return np.nan, np.nan, len(ics)
    return float(ics.mean()), float(ics.mean() / (ics.std(ddof=1) / np.sqrt(len(ics)))), len(ics)


def main():
    say("=" * 200)
    say(f"IDEA 158 — does-share-price-any-key-or-only-vol   ({STEM})")
    say("Idea 153 said book share, not key strength, prices a cross-sectional tilt.  It "
        "measured one key.  Swap the key — including for one with no information at all.")
    say("=" * 200)

    ok, rows, ov_rows, ic_rows, ref = {}, [], [], [], {}

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        el = eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        ref[pk] = dict(px=px, start=start, spy=ms, spy_oos=mso, bfull=bfull, bIS=bIS, bOOS=bOOS,
                       v1=v1, n_elig=n_elig, desc=desc, el=el)
        nmap = {m: max(2, int(round(m * n_elig))) for m in SHARES}
        ref[pk]["nmap"] = nmap

        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval from {start.date()}, mean "
            f"weekly eligible names {n_elig:.2f}")
        say("    book share -> n:  " + ", ".join(f"m={m:.2f}->n={nmap[m]}" for m in SHARES))
        say(f"    SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso['CAGR']:.2%}/{mso['Sharpe']:.3f}/"
            f"{mso['MaxDD']:.2%}")
        for c in COSTS:
            mm = metrics(v1[c])
            say(f"    RULES v1 @{int(c)}bps: {mm['CAGR']:.5%}/{mm['Sharpe']:.5f}/{mm['MaxDD']:.5%}")

        # ---------- the keys' own information content (the competing explanation)
        _, _, _, _, RAW = parts(px, pk)
        for key in KEYS:
            ic, t, nd = rank_ic(RAW[key], px, el, start)
            ic_rows.append(dict(panel=pk, key=key, rank_IC=ic, t_IC=t, n_dates=nd))

        # ---------- the books.  Run ONCE at 0 bps; derive the cost rungs exactly.
        for m in SHARES:
            n = nmap[m]
            arms = [("NONE", "NONE")] + [(k, d) for k in KEYS for d in ("NEG", "POS")]
            masks, r0s, tos = {}, {}, {}
            for constr in ("lit", "norm"):
                if constr == "norm" and m > 0.53:
                    continue          # the norm control is only read on the m<=0.53 subgrid
                for (key, d) in arms:
                    W = weights(px, pk, key, d, n, constr=constr)
                    res = backtest(px, W, cost_bps=0.0, freq=FREQ)
                    r0 = res["returns"].loc[start:]
                    to = res["turnover"].loc[start:]
                    r0s[(key, d, constr)] = r0
                    tos[(key, d, constr)] = to
                    if constr == "lit":
                        masks[(key, d)] = held_mask(px, pk, key, d, n).loc[start:]
                    gross = float(W.loc[start:].sum(axis=1).mean())
                    yrs = metrics(r0)["Years"]
                    for c in COSTS:
                        if constr == "norm" and c != 10.0:
                            continue
                        r = r0 - to * c / 1e4
                        mm = metrics(r)
                        mo, mi = metrics(H.window(r, "OOS")), metrics(H.window(r, "IS"))
                        h1, h2 = H.halves(r)
                        ih1, ih2 = H.halves(H.window(r, "IS"))
                        mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                        mgo = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                        mgi = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                        rows.append(dict(
                            panel=pk, m=m, n=n, key=key, dir=d, cost=c, constr=constr,
                            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=ih1, IS_H2=ih2, TO=to.sum() / yrs, gross=gross,
                            pass4a=H.pass4a(r, v1[c]),
                            pass4b=(len(C.fails(mg)) == 0), fail4b=",".join(C.fails(mg)) or "-",
                            pass4b_oos=all(mgo[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                            IS_adm=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR"))))

            # ---------- [d] the cost identity, checked once per panel on the incumbent share
            if m == 0.53 and "d" not in ok:
                W = weights(px, pk, "NONE", "NONE", n)
                fresh = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
                der = r0s[("NONE", "NONE", "lit")] - tos[("NONE", "NONE", "lit")] * 10.0 / 1e4
                mx = float((fresh - der).abs().max())
                ok["d"] = mx < 1e-12
                say(f"[d] cost identity r_c = r_0 - TO*c/1e4 vs a fresh 10 bps engine run: "
                    f"max|diff| {mx:.2e} -> {'EXACT' if ok['d'] else 'MISMATCH — unsafe'}")

            # ---------- overlap of every tilted book with its own no-tilt control
            base = masks[("NONE", "NONE")]
            nh = float(base.sum(axis=1).mean())
            for key in KEYS:
                for d in ("NEG", "POS"):
                    ov_rows.append(dict(panel=pk, m=m, n=n, key=key, dir=d, n_elig=n_elig,
                                        n_held=nh, realised_share=nh / n_elig,
                                        overlap=overlap(masks[(key, d)], base)))

        # ---------- [a]/[b] idea 153's published anchors
        pub_e = {"u56": 37.50, "broad": 91.46, "small": 141.23}[pk]
        ok[f"a:{pk}"] = abs(n_elig - pub_e) < 0.02
        say(f"[a] {pk} mean weekly eligible: idea 153 published {pub_e:.2f}, this run "
            f"{n_elig:.2f} -> {'MATCH' if ok[f'a:{pk}'] else 'MISMATCH'}")
        if pk in ("u56", "broad"):
            A = held_mask(px, pk, "VOL", "NEG", 20).loc[start:]
            B = held_mask(px, pk, "NONE", "NONE", 20).loc[start:]
            o = overlap(A, B)
            pub = 0.694 if pk == "u56" else 0.425
            ok[f"b:{pk}"] = abs(o - pub) < 0.006
            say(f"[b] {pk} n=20 INV(VOL/NEG)-vs-NONE overlap: idea 153 published {pub:.1%}, "
                f"this run {o:.1%} -> {'MATCH' if ok[f'b:{pk}'] else 'MISMATCH'}")

    df = pd.DataFrame(rows)
    OVL = pd.DataFrame(ov_rows)
    IC = pd.DataFrame(ic_rows)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    OVL.to_csv(OUT / f"{STEM}.overlap.csv", index=False)
    IC.to_csv(OUT / f"{STEM}.ic.csv", index=False)

    # ---------- [c]/[e] the committed control book and the live rules
    b = df[(df.panel == "u56") & (df.key == "NONE") & (df.n == 20) & (df.cost == 10.0)
           & (df.constr == "lit")]
    if len(b):
        b = b.iloc[0]
        pubc = dict(CAGR=0.1265974, Sharpe=1.09214, MaxDD=-0.1830835, H1=1.08828, H2=1.10155)
        ok["c"] = all(abs(b[k] - v) < 5e-5 for k, v in pubc.items())
        say(f"\n[c] NONE/n=20/u56@10bps: {b.CAGR:.5%}/{b.Sharpe:.5f}/{b.MaxDD:.5%} halves "
            f"{b.H1:.5f}/{b.H2:.5f}  vs published 12.65974%/1.09214/-18.30835% halves "
            f"1.08828/1.10155 -> {'MATCH' if ok['c'] else 'MISMATCH'}")
    else:
        ok["c"] = False
        say("\n[c] u56 n=20 not on the share grid — check skipped, NOT quietly passed")
    mv = metrics(ref["u56"]["v1"][10.0])
    ok["e"] = (abs(mv["CAGR"] - 0.0645305) < 5e-6 and abs(mv["Sharpe"] - 0.66418) < 5e-5
               and abs(mv["MaxDD"] + 0.1382780) < 5e-6)
    say(f"[e] RULES v1 u56@10bps: {mv['CAGR']:.5%}/{mv['Sharpe']:.5f}/{mv['MaxDD']:.5%} vs "
        f"published 6.45305%/0.66418/-13.82780% -> {'MATCH' if ok['e'] else 'MISMATCH'}")
    if not all(ok.values()):
        say("\n[WARNING] a pre-check did not hold; read everything below with that in mind.")

    # =============================================================== the grid
    say("\n" + "=" * 200)
    say("THE GRID — 2 tuned parameters (book share m x tilt direction) = 21 points per key, "
        "EVERY one reported, on 6 keys x 3 panels x 2 cost rungs (literal GROSS/n book)")
    say("=" * 200)
    cols = ["m", "n", "key", "dir", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "pass4a", "pass4b", "fail4b", "pass4b_oos"]
    for pk in PANELS:
        for c in COSTS:
            s = df[(df.panel == pk) & (df.cost == c) & (df.constr == "lit")]
            s = s.sort_values(["m", "key", "dir"])
            r_ = ref[pk]
            say(f"\n  {pk} @ {int(c)} bps  (SPY {r_['spy']['CAGR']:.2%}/{r_['spy']['Sharpe']:.3f}/"
                f"{r_['spy']['MaxDD']:.2%}; RULES v1 {metrics(r_['v1'][c])['CAGR']:.2%}/"
                f"{metrics(r_['v1'][c])['Sharpe']:.3f}/{metrics(r_['v1'][c])['MaxDD']:.2%})")
            say(s[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # =============================================================== the keys' information
    say("\n" + "=" * 200)
    say("THE COMPETING EXPLANATION — each key's own information (weekly cross-sectional rank "
        "IC vs the forward 21d return, inside the eligibility gate)")
    say("=" * 200)
    say(IC.pivot_table(index="key", columns="panel", values=["rank_IC", "t_IC"])
        .to_string(float_format=lambda x: f"{x:+.4f}"))

    # =============================================================== P2 — overlap vs share
    say("\n" + "=" * 200)
    say("P2 — overlap with the no-tilt control, by book share, for every key")
    say("=" * 200)
    piv = OVL.pivot_table(index=["panel", "m"], columns=["key", "dir"], values="overlap")
    say(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    bad = []
    for (pk, key, d), g in OVL.groupby(["panel", "key", "dir"]):
        if not g.sort_values("m").overlap.is_monotonic_increasing:
            bad.append(f"{pk}/{key}/{d}")
    ok["P2"] = not bad
    say(f"\n    overlap monotone increasing in m in {36 - len(bad)} of 36 (panel, key, dir) "
        f"cells -> P2 {'HELD' if ok['P2'] else 'FAILED: ' + ', '.join(bad)}")

    # =============================================================== deltas
    D = []
    for (pk, m, c, cn), _ in df.groupby(["panel", "m", "cost", "constr"]):
        s = df[(df.panel == pk) & (df.m == m) & (df.cost == c) & (df.constr == cn)]
        s = s.set_index(["key", "dir"])
        base = s.loc[("NONE", "NONE")]
        for key in KEYS:
            for d in ("NEG", "POS"):
                o = OVL[(OVL.panel == pk) & (OVL.m == m) & (OVL.key == key) & (OVL.dir == d)]
                D.append(dict(panel=pk, m=m, n=int(base["n"]), cost=c, constr=cn, key=key, dir=d,
                              overlap=float(o.iloc[0].overlap),
                              share=float(o.iloc[0].realised_share),
                              dSharpe=s.loc[(key, d), "Sharpe"] - base["Sharpe"],
                              dCAGR=s.loc[(key, d), "CAGR"] - base["CAGR"],
                              dMaxDD=s.loc[(key, d), "MaxDD"] - base["MaxDD"],
                              dTO=s.loc[(key, d), "TO"] - base["TO"]))
    D = pd.DataFrame(D)
    D["absdS"], D["absdC"] = D.dSharpe.abs(), D.dCAGR.abs()
    D = D.merge(IC.rename(columns={"rank_IC": "key_IC", "t_IC": "key_tIC"}),
                on=["panel", "key"], how="left")
    D["absIC"] = D.key_IC.abs()
    D.to_csv(OUT / f"{STEM}.delta.csv", index=False)

    say("\n" + "=" * 200)
    say("THE TILT DELTAS — dSharpe / dCAGR vs the no-tilt control at matched (panel, share, "
        "cost), literal book @10 bps")
    say("=" * 200)
    say(D[(D.constr == "lit") & (D.cost == 10.0)]
        .sort_values(["panel", "key", "dir", "m"])
        [["panel", "m", "n", "key", "dir", "overlap", "dSharpe", "dCAGR", "dMaxDD", "dTO"]]
        .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # =============================================================== P3 — the decisive test
    say("\n" + "=" * 200)
    say("P3 (DECISIVE) — WITHIN EACH KEY, does |dSharpe| fall as overlap rises?  m is the only "
        "thing that moves, so this is the arithmetic claim with no cross-key confound.")
    say("=" * 200)
    wr = []
    for (pk, key, cn, c), g in D.groupby(["panel", "key", "constr", "cost"]):
        if cn != "lit":
            continue
        gs = g[g.m <= 0.53]
        bo, to_, r2 = ols(g.absdS, [g.overlap], ["ov"])
        wr.append(dict(panel=pk, key=key, cost=c, n_rows=len(g),
                       rho_all=H.spearman(g.overlap.values, g.absdS.values),
                       rho_le053=H.spearman(gs.overlap.values, gs.absdS.values),
                       b_ov=bo["ov"], t_ov=to_["ov"], R2=r2,
                       mean_absdS=float(g.absdS.mean())))
    WK = pd.DataFrame(wr)
    say(WK.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    lc = WK[WK.panel.isin(["u56", "broad"])]
    neg = lc.groupby("key").rho_le053.apply(lambda s: bool((s < 0).all()))
    ok["P3"] = bool(neg.all())
    say("\n    large-cap panels, m<=0.53, Spearman(overlap, |dSharpe|) negative in every cell?")
    for k_, v_ in neg.items():
        s = lc[lc.key == k_].rho_le053
        say(f"      {k_:5s}: {', '.join(f'{x:+.3f}' for x in s)}  -> "
            f"{'negative in all' if v_ else 'NOT all negative'}")
    say(f"    P3 -> {'HELD' if ok['P3'] else 'FAILED'}")

    # =============================================================== P4 — the random control
    say("\n" + "=" * 200)
    say("P4 — the pooled regression idea 153 ran, re-run KEY BY KEY.  RAND is the control: if "
        "the mechanism is arithmetic its slope is negative and its R2 comparable.")
    say("=" * 200)
    rr = []
    for label, sub in [("literal, all m", D[D.constr == "lit"]),
                       ("literal, m<=0.53", D[(D.constr == "lit") & (D.m <= 0.53)]),
                       ("gross-normalised, m<=0.53", D[(D.constr == "norm") & (D.m <= 0.53)])]:
        for key in ["POOLED"] + KEYS:
            s = sub if key == "POOLED" else sub[sub.key == key]
            for yn in ("absdS", "absdC"):
                bo, to_, r2 = ols(s[yn], [s.overlap], ["ov"])
                rr.append(dict(sample=label, key=key, y=yn, n_rows=len(s),
                               b_overlap=bo["ov"], t_overlap=to_["ov"], R2=r2,
                               mean_y=float(s[yn].mean())))
    R = pd.DataFrame(rr)
    R.to_csv(OUT / f"{STEM}.regression.csv", index=False)
    say(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    kk = R[(R["sample"] == "literal, m<=0.53") & (R.y == "absdS")].set_index("key")
    r2_real = float(kk.loc[REAL_KEYS, "R2"].mean())
    rnd = kk.loc["RAND"]
    ok["P4"] = bool(rnd.b_overlap < 0 and abs(rnd.t_overlap) > 2 and rnd.R2 >= 0.5 * r2_real)
    say(f"\n    RAND alone (m<=0.53, literal): slope {rnd.b_overlap:+.4f} (t {rnd.t_overlap:+.2f}), "
        f"R2 {rnd.R2:.3f}; mean R2 of the five real keys {r2_real:.3f} "
        f"(needed >= {0.5 * r2_real:.3f})")
    say(f"    idea 153's own pooled reading for comparison: R2 {kk.loc['POOLED', 'R2']:.3f}, "
        f"slope {kk.loc['POOLED', 'b_overlap']:+.4f} (t {kk.loc['POOLED', 't_overlap']:+.2f})")
    say(f"    P4 -> {'HELD' if ok['P4'] else 'FAILED'}")

    # =============================================================== P5 — does key strength order it?
    say("\n" + "=" * 200)
    say("P5 — does the key's own information order the tilt it buys, once share is matched?")
    say("=" * 200)
    p5 = []
    for (pk, c), g in D[D.constr == "lit"].groupby(["panel", "cost"]):
        t = g.groupby("key").agg(mean_absdS=("absdS", "mean"), mean_ov=("overlap", "mean"),
                                 absIC=("absIC", "first"), IC=("key_IC", "first"))
        rho = H.spearman(t.absIC.values, t.mean_absdS.values)
        p5.append(dict(panel=pk, cost=c, rho_absIC_absdS=rho,
                       rho_ov_absdS=H.spearman(t.mean_ov.values, t.mean_absdS.values)))
        say(f"\n  {pk} @ {int(c)} bps — per-key means (share grid pooled):")
        say(t.to_string(float_format=lambda x: f"{x:+.4f}"))
        say(f"    Spearman across the 6 keys: |IC| vs mean|dSharpe| {rho:+.3f} | "
            f"mean overlap vs mean|dSharpe| "
            f"{H.spearman(t.mean_ov.values, t.mean_absdS.values):+.3f}")
    P5 = pd.DataFrame(p5)
    mrho = float(P5.rho_absIC_absdS.mean())
    ok["P5"] = bool(not (P5.rho_absIC_absdS > 0.6).all())
    say(f"\n    mean Spearman(|IC|, mean|dSharpe|) across the 6 cells: {mrho:+.3f}; "
        f"mean Spearman(overlap, mean|dSharpe|) {float(P5.rho_ov_absdS.mean()):+.3f}")
    say(f"    P5 (key strength does NOT order the tilt) -> {'HELD' if ok['P5'] else 'FAILED'}")

    # =============================================================== KEEP paths
    say("\n" + "=" * 200)
    say("BOTH KEEP PATHS on all 273 literal books (4a vs the live rules, 4b vs SPY)")
    say("=" * 200)
    lit = df[df.constr == "lit"]
    kp = lit.groupby(["key", "dir"]).agg(pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"),
                                         pass4b_oos=("pass4b_oos", "sum"), cells=("panel", "size"))
    say(kp.to_string())
    say(f"\n    total: 4a {int(lit.pass4a.sum())} of {len(lit)}, 4b full-sample "
        f"{int(lit.pass4b.sum())} of {len(lit)}, 4b on the OOS window alone "
        f"{int(lit.pass4b_oos.sum())} of {len(lit)}")
    xu = lit[lit.pass4b].groupby(["m", "key", "dir"]).panel.nunique()
    xu = xu[xu > 1]
    say("    cross-universe 4b ((m, key, dir) passing on >1 panel): "
        + (", ".join(f"m={k[0]}/{k[1]}/{k[2]} on {v} panels" for k, v in xu.items())
           if len(xu) else "NONE"))
    tilted = lit[(lit.pass4b) & (lit.key != "NONE")]
    ok["P6"] = len(xu) == 0
    say(f"    P6 -> {'HELD' if ok['P6'] else 'FAILED — a cross-universe pass exists, see above'}")
    if lit.pass4b.any():
        say("\n    every 4b pass (single-panel), tilted and untilted:")
        say(lit[lit.pass4b][["panel", "cost", "m", "n", "key", "dir", "CAGR", "Sharpe", "MaxDD",
                            "H1", "H2", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO"]]
            .sort_values(["panel", "cost", "m"])
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        say(f"    of which tilted (key != NONE): {len(tilted)}")

    # =============================================================== rule 8
    say("\n" + "=" * 200)
    say("RULE 8 WALK-FORWARD — (m, key, dir) chosen on the IS window (<= 2016-12-31) only, "
        "read ONCE on 2017-01-01..2026")
    say("=" * 200)
    wrows = []
    for pk in PANELS:
        for c in COSTS:
            s = lit[(lit.panel == pk) & (lit.cost == c)].reset_index(drop=True)
            v1o = metrics(ref[pk]["v1"][c].loc[OOS_START:])
            sp = ref[pk]["spy_oos"]
            ctl = s[(s.key == "NONE") & (s.m == 0.53)].iloc[0]
            nones = s[s.key == "NONE"]
            rands = s[s.key == "RAND"]
            picks = {"S1_ISSharpe_all": s.loc[s.IS_Sharpe.idxmax()],
                     "S2_donothing_m053": ctl,
                     "S3_RANDonly": rands.loc[rands.IS_Sharpe.idxmax()],
                     "S4_NONEonly": nones.loc[nones.IS_Sharpe.idxmax()]}
            for nm, r_ in picks.items():
                wrows.append(dict(panel=pk, cost=c, sel=nm, key=r_.key, dir=r_["dir"], m=r_.m,
                                  n=int(r_.n), IS_Sharpe=r_.IS_Sharpe, IS_MaxDD=r_.IS_MaxDD,
                                  OOS_CAGR=r_.OOS_CAGR, OOS_Sharpe=r_.OOS_Sharpe,
                                  OOS_MaxDD=r_.OOS_MaxDD, pass4b_oos=r_.pass4b_oos,
                                  v1_OOS_CAGR=v1o["CAGR"], v1_OOS_Sharpe=v1o["Sharpe"],
                                  v1_OOS_MaxDD=v1o["MaxDD"], spy_OOS_CAGR=sp["CAGR"],
                                  spy_OOS_Sharpe=sp["Sharpe"], spy_OOS_MaxDD=sp["MaxDD"]))
    Wf = pd.DataFrame(wrows)
    Wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(Wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n    mean OOS Sharpe by selector (6 cells each):")
    for nm, g in Wf.groupby("sel"):
        say(f"      {nm:20s} {g.OOS_Sharpe.mean():.4f}   (CAGR {g.OOS_CAGR.mean():.2%}, "
            f"MaxDD {g.OOS_MaxDD.mean():.2%}, OOS-4b passes {int(g.pass4b_oos.sum())}/{len(g)})")
    say(f"      {'RULES v1':20s} {Wf.v1_OOS_Sharpe.mean():.4f}   "
        f"(CAGR {Wf.v1_OOS_CAGR.mean():.2%}, MaxDD {Wf.v1_OOS_MaxDD.mean():.2%})")
    say(f"      {'SPY':20s} {Wf.spy_OOS_Sharpe.mean():.4f}   "
        f"(CAGR {Wf.spy_OOS_CAGR.mean():.2%}, MaxDD {Wf.spy_OOS_MaxDD.mean():.2%})")
    lcw = Wf[Wf.panel.isin(["u56", "broad"])]
    say("\n    large-cap only (4 cells each):")
    for nm, g in lcw.groupby("sel"):
        say(f"      {nm:20s} OOS Sharpe {g.OOS_Sharpe.mean():.4f}, CAGR {g.OOS_CAGR.mean():.2%}, "
            f"MaxDD {g.OOS_MaxDD.mean():.2%}")
    s1 = Wf[Wf.sel == "S1_ISSharpe_all"].set_index(["panel", "cost"])
    s2 = Wf[Wf.sel == "S2_donothing_m053"].set_index(["panel", "cost"])
    s3 = Wf[Wf.sel == "S3_RANDonly"].set_index(["panel", "cost"])
    say(f"\n    paired: S1 (selection over all 91 arms) beats S2 (do nothing) in "
        f"{int((s1.OOS_Sharpe > s2.OOS_Sharpe).sum())} of {len(s1)} cells; "
        f"S3 (a RANDOM key, IS-selected) beats S2 in "
        f"{int((s3.OOS_Sharpe > s2.OOS_Sharpe).sum())} of {len(s3)}; "
        f"S1 beats S3 in {int((s1.OOS_Sharpe > s3.OOS_Sharpe).sum())} of {len(s1)}")
    say(f"    keys picked by S1: " + ", ".join(f"{k} {v}" for k, v in
                                               Wf[Wf.sel == 'S1_ISSharpe_all'].key.value_counts().items()))

    say("\n" + "=" * 200)
    say("PRE-REGISTERED PREDICTIONS — outcome")
    say("=" * 200)
    for k_, v_ in ok.items():
        say(f"    {k_}: {'HELD/OK' if v_ else 'FAILED'}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
