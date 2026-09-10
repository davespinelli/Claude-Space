#!/usr/bin/env python3
"""Idea 663 — IS THE RECORD'S *LABEL VOCABULARY* A PER-RUN *COINAGE*?

Idea 661 found that `family`, `dial` and `panel` carry 58.8% of all 146,008 unjoinable
pointer rows at min_col_overlap EXACTLY 0.0, and that 54.6% of the misses join on a SINGLE
key column.  A zero column overlap on a LABEL column has only two possible causes: the two
runs labelled genuinely different things, or they spelled the same thing differently.  The
second is a coinage problem — each run inventing its own token for the same object — and it
is fixable for free by freezing a vocabulary.  This run measures which one it is.

Pre-registration (fixed before any number was read):

  * TWO tuned parameters and no more:
      COLUMN — family | dial | panel   (all three REPORTED at every point)
      BAR B  — the frozen-vocabulary bar: a token is CANONICAL iff it is emitted by at
               least B of the files that emit the column.  B in {0.00, 0.01, 0.02, 0.05,
               0.10, 0.25, 0.50}; B = 0.00 is the identity (no freeze) and is asserted so.
    The NORMAL FORM (RAW | NORM | STEM), the panel, the cost rung, the dial and the rung
    ladder are REPORTED at every point, never chosen.  Every grid point is written to disk.

  * PART A — CENSUS.  Every committed .csv under research/ that emits one of the three
    columns.  For each (file, column) the VOCABULARY is the distinct value set.  Reported:
      - files emitting the column, distinct tokens, distinct vocabularies (distinct sets);
      - COINAGE RATE: files ordered by their date stamp, then name; how many files
        introduce at least one token no earlier file emitted, and how many tokens per run;
      - HAPAX share: tokens emitted by exactly one file;
      - THE JOIN TEST: over every unordered file PAIR emitting the column, the share of
        pairs whose token sets are DISJOINT (min_col_overlap == 0.0 in idea 661's sense),
        under each normal form and each bar.  Reported twice — with and without the files
        the freeze empties — because a bar that erases a file makes it join nothing.
    Normal forms: RAW (as written) / NORM (casefold, non-alphanumerics dropped) /
    STEM (NORM with trailing digits dropped, i.e. SMALL439 and SMALL484 become one token).

  * PART B — THE LIVE LEG.  A vocabulary is not free: a reader can only act on a rung the
    record actually spells.  Four dials, each rung carrying the token the record would
    write for it, on three panels at two cost rungs:
      n     TOP-n ranked book, n in {5, 10, 15, 20, 30, 40}, gross 0.75
      gross RULES v2 band book at gross in {0.50, 0.625, 0.75, 0.875, 1.00}
      band  de-grossed band book, band in {0.00, 0.03, 0.06, 0.09, 0.12}, gross 0.75
      freq  RULES v2 at cadence in {D, W, M, Q}
    FULL menu = every rung.  FROZEN(B) menu = the rungs whose token clears the same bar B
    in the record's own committed CSVs.  If the vocabulary is a per-run coinage, the frozen
    menu is strictly smaller and the rule-8 pick can change; if it is stable, the menus
    agree and the coinage is cosmetic.

  * BOTH KEEP PATHS at every grid point.  4a against the LIVE book (native RULES v2 on the
    same panel, window and rung).  4b against SPY (Sharpe > SPY in BOTH halves AND OOS,
    MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's).

  * RULE 8 (PROTOCOL 8): inside each (panel, dial, menu, rung) the rung is chosen on
    IS <= 2016-12-31 by IS Sharpe ONLY, and 2017-01-01.. is read ONCE.  OOS CAGR / Sharpe /
    MaxDD reported against native RULES v2 and SPY on the same OOS window.

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are CURRENT-constituent lists, so their
LEVELS are biased upward and unequally so; only within-panel, within-window contrasts are
load-bearing.  U56 is a fixed ETF/mega-cap list and is least biased.  SMALL439 drops the
sub-$2B names with max_1d_move >= 1.0 (data/small_meta.csv) BEFORE anything else is done.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .vocab.csv, .coinage.csv, .join.csv, .menu.csv,
.grid.csv, .walkforward.csv, .console.txt.
"""
import csv
import re
import sys
import time
from itertools import combinations
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-10_is-the-record-s-LABEL-VOCABULARY-a-per-run-COINAGE_cloud"
OUT = ROOT / "research" / "backtests"
COLUMNS = ["family", "dial", "panel"]
DIALCOLS = ["n", "gross", "band", "freq"]      # PART B's rung columns, censused the same way
SCANCOLS = COLUMNS + DIALCOLS
FORMS = ["RAW", "NORM", "STEM"]
BARS = [0.00, 0.01, 0.02, 0.05, 0.10, 0.25, 0.50]
RUNGS = [10, 25]
GROSS = 0.75
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PANELS = ["U56", "B136", "SMALL439"]
MAXDISTINCT = 20000          # per (file, column) guard; reported if ever hit

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _console.append(s)


# ==================================================================== PART A — census
_NONALNUM = re.compile(r"[^0-9a-z]+")
_TRAILDIG = re.compile(r"\d+$")
_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def form(tok, f):
    if f == "RAW":
        return tok
    n = _NONALNUM.sub("", tok.casefold())
    if f == "NORM":
        return n
    return _TRAILDIG.sub("", n)


def corpus_csvs():
    """Every committed .csv the record carries under research/, date-ordered then by name."""
    files = sorted((ROOT / "research" / "backtests").glob("*.csv"))
    files += sorted(p for p in (ROOT / "research").glob("*.csv"))
    files += sorted((ROOT / "research" / "deepvalue").glob("*.csv"))
    files += sorted((ROOT / "research" / "tenders").glob("*.csv"))
    seen, keep = set(), []
    for f in files:
        if f in seen or not f.exists():
            continue
        seen.add(f); keep.append(f)
    def key(p):
        m = _DATE.search(p.name)
        return (m.group(1) if m else "0000-00-00", p.name)
    return sorted(keep, key=key)


def scan_corpus():
    """{column: {file: set(raw tokens)}} — one streaming pass, only the needed columns."""
    voc = {c: {} for c in SCANCOLS}
    capped = []
    files = corpus_csvs()
    t0 = time.time()
    for k, f in enumerate(files):
        try:
            fh = f.open(newline="", errors="replace")
        except Exception:
            continue
        with fh:
            try:
                rd = csv.reader(fh)
                head = next(rd)
            except Exception:
                continue
            low = [h.strip().casefold() for h in head]
            idx = {c: low.index(c) for c in SCANCOLS if c in low}
            if not idx:
                continue
            sets = {c: set() for c in idx}
            try:
                for row in rd:
                    for c, i in idx.items():
                        if i < len(row):
                            v = row[i].strip()
                            if v and len(sets[c]) < MAXDISTINCT:
                                sets[c].add(v)
            except Exception:
                pass
        for c, s in sets.items():
            if len(s) >= MAXDISTINCT:
                capped.append((f.name, c))
            if s:
                voc[c][str(f.relative_to(ROOT))] = s
        if (k + 1) % 500 == 0:
            say(f"    scanned {k+1}/{len(files)} csvs  ({time.time()-t0:.0f}s)")
    say(f"    scanned {len(files)} csvs in {time.time()-t0:.0f}s;"
        f" distinct-value cap hit on {len(capped)} (file, column) pairs")
    return voc, files


def bitsets(mapped):
    """{file: set} -> ({file: int bitmask}, token list)."""
    toks = sorted({t for s in mapped.values() for t in s})
    ix = {t: i for i, t in enumerate(toks)}
    return {f: sum(1 << ix[t] for t in s) for f, s in mapped.items()}, toks


def popcount(x):
    return x.bit_count() if hasattr(x, "bit_count") else bin(x).count("1")


def join_stats(mapped):
    """Over every unordered file pair: disjoint share and mean Jaccard, empties reported."""
    B, _ = bitsets(mapped)
    keys = sorted(B)
    ne = [k for k in keys if B[k]]
    n_all = len(keys) * (len(keys) - 1) // 2
    dis_all = dis_ne = 0
    jsum = 0.0
    n_ne = len(ne) * (len(ne) - 1) // 2
    for a, b in combinations(ne, 2):
        x, y = B[a], B[b]
        inter = x & y
        if not inter:
            dis_ne += 1
        else:
            jsum += popcount(inter) / popcount(x | y)
    dis_all = dis_ne + (n_all - n_ne)          # every pair touching an emptied file is disjoint
    return dict(files=len(keys), files_nonempty=len(ne), pairs=n_all,
                disjoint_share_all=dis_all / n_all if n_all else np.nan,
                pairs_nonempty=n_ne,
                disjoint_share_nonempty=dis_ne / n_ne if n_ne else np.nan,
                mean_jaccard_nonempty=jsum / n_ne if n_ne else np.nan)


def part_a(voc):
    vrows, crows, jrows = [], [], []
    for col in COLUMNS:
        per = voc[col]
        if not per:
            say(f"\n--- column `{col}`: emitted by NO committed csv"); continue
        order = list(per)                                     # already date-then-name ordered
        say("\n" + "-" * 100)
        say(f"--- column `{col}`: emitted by {len(per)} committed csvs")
        for f in FORMS:
            mapped = {k: {form(t, f) for t in s} for k, s in per.items()}
            toks = {}
            for k, s in mapped.items():
                for t in s:
                    toks[t] = toks.get(t, 0) + 1
            vocabs = {frozenset(s) for s in mapped.values()}
            hapax = sum(1 for t, n in toks.items() if n == 1)
            # coinage: walk the record in run order
            seen, new_files, new_tokens, curve = set(), 0, 0, []
            for k in order:
                nn = mapped[k] - seen
                if nn:
                    new_files += 1; new_tokens += len(nn)
                seen |= mapped[k]
                curve.append(len(seen))
            vrows.append(dict(column=col, form=f, files=len(per), tokens=len(toks),
                              vocabularies=len(vocabs),
                              vocab_per_file=len(vocabs) / len(per),
                              hapax=hapax, hapax_share=hapax / max(len(toks), 1),
                              coining_files=new_files,
                              coining_share=new_files / len(per),
                              new_tokens_per_file=new_tokens / len(per),
                              median_set_size=float(np.median([len(s) for s in mapped.values()])),
                              max_set_size=max(len(s) for s in mapped.values())))
            say(f"  {f:5s} tokens {len(toks):6d}  distinct vocabularies {len(vocabs):5d}"
                f"  ({len(vocabs)/len(per):.3f} per file)  hapax {hapax}"
                f" ({hapax/max(len(toks),1):.1%})  files coining a new token"
                f" {new_files}/{len(per)} ({new_files/len(per):.1%})")
            for q in (0.10, 0.25, 0.50, 0.75, 1.00):
                i = max(0, int(round(q * len(order))) - 1)
                crows.append(dict(column=col, form=f, quantile=q, files_seen=i + 1,
                                  cumulative_tokens=curve[i]))
            # the join test at every bar
            for B in BARS:
                canon = {t for t, n in toks.items() if n / len(per) >= B} if B > 0 else set(toks)
                mm = {k: (s & canon) for k, s in mapped.items()}
                st = join_stats(mm)
                jrows.append(dict(column=col, form=f, bar=B, vocab_size=len(canon), **st))
        jj = pd.DataFrame([r for r in jrows if r["column"] == col])
        say("\n  JOIN TEST (share of file pairs with ZERO token overlap):")
        say("  " + jj[["form", "bar", "vocab_size", "files_nonempty", "disjoint_share_all",
                       "disjoint_share_nonempty", "mean_jaccard_nonempty"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    V = pd.DataFrame(vrows); V.to_csv(OUT / f"{STAMP}.vocab.csv", index=False)
    C = pd.DataFrame(crows); C.to_csv(OUT / f"{STAMP}.coinage.csv", index=False)
    J = pd.DataFrame(jrows); J.to_csv(OUT / f"{STAMP}.join.csv", index=False)
    return V, C, J


# =========================================================== PART B — the live leg
def fast_backtest(px, weights, freq="W"):
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


def dg_weights(px, gate, g=GROSS, cols=None):
    """De-grossed: g/N on every priced name, gated weight -> CASH, never re-spread."""
    p = px if cols is None else px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(gate.reindex_like(ew).fillna(False), 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def topn_weights(px, n, cols, g=GROSS):
    p = px[cols]
    s, above, _ = score(p, vol_scale=False)
    rank = s.where(above).rank(axis=1, ascending=False)
    w = (rank <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def panels():
    out = {}
    u = load_universe(); out["U56"] = (u, list(u.columns))
    b = load_universe(broad=True); out["B136"] = (b, list(b.columns))
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    dropped = len(bad & set(sm.columns))
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    say(f"    SMALL panel: dropped {dropped} names with max_1d_move >= 1.0;"
        f" {len([c for c in sm.columns if c != 'SPY'])} remain")
    out["SMALL439"] = (sm, [c for c in sm.columns if c != "SPY"])
    return out


DIALS = {
    "n":     ("n",     [5, 10, 15, 20, 30, 40]),
    "gross": ("gross", [0.50, 0.625, 0.75, 0.875, 1.00]),
    "band":  ("band",  [0.00, 0.03, 0.06, 0.09, 0.12]),
    "freq":  ("freq",  ["D", "W", "M", "Q"]),
}


def book(px, cols, dial, rung):
    """(weights, freq) for one dial rung.  Every other dial sits at the live book's value."""
    p = px[cols]
    if dial == "n":
        return topn_weights(px, rung, cols), "W"
    if dial == "gross":
        return dg_weights(px, band_state(p, 0.03), g=rung, cols=cols), "W"
    if dial == "band":
        gate = (p > p.rolling(200).mean()).fillna(False) if rung == 0.0 else band_state(p, rung)
        return dg_weights(px, gate, cols=cols), "W"
    return dg_weights(px, band_state(p, 0.03), cols=cols), rung


def rung_token_freq(voc_all):
    """How often the record's own CSVs spell each rung, under the dial's own column."""
    freq = {}
    for dial, (col, rungs) in DIALS.items():
        per = voc_all.get(col, {})
        nfiles = len(per)
        for r in rungs:
            hits = 0
            for s in per.values():
                for v in s:
                    if _match_rung(v, r):
                        hits += 1; break
            freq[(dial, r)] = (hits, nfiles, hits / nfiles if nfiles else 0.0)
    return freq


def _match_rung(v, r):
    if isinstance(r, str):
        return v.strip().casefold() == r.casefold()
    try:
        return abs(float(v) - float(r)) < 1e-9
    except Exception:
        return False


def keep_flags(s, base, spy, oos_sharpe, spy_oos_sharpe):
    a = (s["H1"] > base["H1"]) and (s["H2"] > base["H2"]) and (s["MaxDD"] >= base["MaxDD"])
    b = (s["H1"] > spy["H1"] and s["H2"] > spy["H2"] and oos_sharpe > spy_oos_sharpe
         and s["MaxDD"] >= 0.60 * spy["MaxDD"]        # MaxDD negative: >= is "no worse"
         and s["CAGR"] >= 0.70 * spy["CAGR"])
    return a, b


def part_b(voc_all):
    say("\n" + "=" * 100)
    say("PART B — the live leg: does the FROZEN vocabulary change the menu, and the pick?")
    say("=" * 100)
    RF = rung_token_freq(voc_all)
    mrows = []
    say("\n  RUNG TOKENS as the record spells them (files emitting the value / files"
        " emitting the column):")
    for dial, (col, rungs) in DIALS.items():
        bits = []
        for r in rungs:
            h, n, sh = RF[(dial, r)]
            bits.append(f"{r}:{h}/{n}({sh:.3f})")
            for B in BARS:
                mrows.append(dict(dial=dial, column=col, rung=str(r), files=h, col_files=n,
                                  share=sh, bar=B, in_frozen_menu=sh >= B))
        say(f"    {dial:6s} [{col}] " + "  ".join(bits))
    M = pd.DataFrame(mrows); M.to_csv(OUT / f"{STAMP}.menu.csv", index=False)
    say("\n  FROZEN MENU SIZE by bar:")
    piv = M.groupby(["dial", "bar"]).in_frozen_menu.sum().unstack()
    say("  " + piv.to_string().replace("\n", "\n  "))

    PX = panels()
    say("\n=== GATES ===")
    upx, ucols = PX["U56"]
    st = upx.index[260]
    w2 = rules_v2_weights(upx)
    e_res = engine_backtest(upx, w2, cost_bps=10, freq="W")
    f_res = fast_backtest(upx, w2)
    g1r = float(np.abs((net(f_res, 10) - e_res["returns"]).loc[st:].values).max())
    g1t = float(np.abs((f_res["turnover"] - e_res["turnover"]).loc[st:].values).max())
    say(f"G1 fast_backtest vs engine.backtest  max|dret| {g1r:.3e}  max|dturn| {g1t:.3e}")
    assert g1r < 1e-12 and g1t < 1e-12, "G1 FAILED"
    g2 = float(np.abs(dg_weights(upx, band_state(upx[ucols], 0.03), cols=ucols).values
                      - w2.values).max())
    say(f"G2 dg_weights(BAND 0.03, 0.75) == baseline.rules_v2_weights  max|diff| {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED"
    g3 = all(M[M.bar == 0.00].in_frozen_menu)
    say(f"G3 bar 0.00 is the identity menu (every rung admitted): {g3}")
    assert g3, "G3 FAILED"
    mono = M.groupby(["dial", "bar"]).in_frozen_menu.sum().unstack()
    g4 = bool((mono.diff(axis=1).fillna(0) <= 0).all().all())
    say(f"G4 frozen menu size is non-increasing in the bar: {g4}")
    assert g4, "G4 FAILED"

    rows, wf_rows = [], []
    for pname in PANELS:
        px, cols = PX[pname]
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = mstats(spy_r)
        spy_oos = metrics(spy_r.loc[OOS_START:])
        base = fast_backtest(px, rules_v2_weights(px), freq="W")
        say(f"\n--- {pname}: {start.date()}..{px.index[-1].date()}, {len(cols)} names")
        RES = {}
        for dial, (col, rungs) in DIALS.items():
            for r in rungs:
                w, fq = book(px, cols, dial, r)
                RES[(dial, r)] = fast_backtest(px, w, freq=fq)
        for bps in RUNGS:
            base_s = mstats(net(base, bps).loc[start:])
            base_oos = metrics(net(base, bps).loc[OOS_START:])
            for dial, (col, rungs) in DIALS.items():
                for r in rungs:
                    R = RES[(dial, r)]
                    rr = net(R, bps).loc[start:]
                    s = mstats(rr)
                    mos = metrics(net(R, bps).loc[OOS_START:])
                    mis = metrics(net(R, bps).loc[start:IS_END])
                    a, b = keep_flags(s, base_s, spy_s, mos["Sharpe"], spy_oos["Sharpe"])
                    rows.append(dict(panel=pname, dial=dial, rung=str(r), bps=bps,
                                     gross=float(R["gross"].loc[start:].mean()),
                                     turnover_yr=float(R["turnover"].loc[start:].sum()
                                                       / (len(rr) / 252)),
                                     **s, IS_Sharpe=mis["Sharpe"],
                                     OOS_CAGR=mos["CAGR"], OOS_Sharpe=mos["Sharpe"],
                                     OOS_MaxDD=mos["MaxDD"],
                                     base_Sharpe=base_s["Sharpe"], base_MaxDD=base_s["MaxDD"],
                                     spy_Sharpe=spy_s["Sharpe"], spy_MaxDD=spy_s["MaxDD"],
                                     keep4a=a, keep4b=b))
                # rule 8 on each menu
                for B in BARS:
                    menu = [r for r in rungs if RF[(dial, r)][2] >= B]
                    if not menu:
                        wf_rows.append(dict(panel=pname, dial=dial, bar=B, bps=bps,
                                            menu_size=0, pick="NONE"))
                        continue
                    iss = {r: metrics(net(RES[(dial, r)], bps).loc[start:IS_END])["Sharpe"]
                           for r in menu}
                    pick = max(iss, key=iss.get)
                    mos = metrics(net(RES[(dial, pick)], bps).loc[OOS_START:])
                    wf_rows.append(dict(
                        panel=pname, dial=dial, bar=B, bps=bps, menu_size=len(menu),
                        pick=str(pick), IS_Sharpe=iss[pick],
                        OOS_CAGR=mos["CAGR"], OOS_Sharpe=mos["Sharpe"], OOS_MaxDD=mos["MaxDD"],
                        base_OOS_CAGR=base_oos["CAGR"], base_OOS_Sharpe=base_oos["Sharpe"],
                        base_OOS_MaxDD=base_oos["MaxDD"],
                        spy_OOS_CAGR=spy_oos["CAGR"], spy_OOS_Sharpe=spy_oos["Sharpe"],
                        spy_OOS_MaxDD=spy_oos["MaxDD"],
                        beats_base=mos["Sharpe"] > base_oos["Sharpe"],
                        beats_spy=mos["Sharpe"] > spy_oos["Sharpe"]))
    G = pd.DataFrame(rows); G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    WF = pd.DataFrame(wf_rows); WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    say("\n=== EVERY GRID POINT (full sample, both cost rungs) ===")
    say(G[["panel", "dial", "rung", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "keep4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n=== KEEP PATHS over all %d grid points ===" % len(G))
    say(f"  4a {int(G.keep4a.sum())}/{len(G)}   4b {int(G.keep4b.sum())}/{len(G)}"
        f"   BOTH {int((G.keep4a & G.keep4b).sum())}/{len(G)}")
    for pn in PANELS:
        s = G[G.panel == pn]
        say(f"    {pn:9s} 4a {int(s.keep4a.sum())}/{len(s)}  4b {int(s.keep4b.sum())}/{len(s)}")
    if int(G.keep4b.sum()):
        say("  4b passers:")
        say(G[G.keep4b][["panel", "dial", "rung", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe", "spy_Sharpe"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n=== RULE 8 WALK-FORWARD (choose on IS <= %s by IS Sharpe, read %s.. once) ==="
        % (IS_END, OOS_START))
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    ok = WF[WF.menu_size > 0]
    say(f"  picks beating the live book OOS Sharpe: {int(ok.beats_base.sum())}/{len(ok)};"
        f" beating SPY OOS Sharpe: {int(ok.beats_spy.sum())}/{len(ok)}")
    piv = ok.pivot_table(index=["panel", "dial", "bps"], columns="bar", values="pick",
                         aggfunc="first")
    base_col = piv[0.00]
    say("\n  Does the FREEZE change the rule-8 pick? (vs bar 0.00, the full menu)")
    for B in BARS[1:]:
        if B not in piv.columns:
            continue
        chg = int((piv[B] != base_col).sum())
        say(f"    bar {B:<5} pick changed in {chg}/{len(piv)} (panel, dial, rung) cells")
    dso = ok.pivot_table(index=["panel", "dial", "bps"], columns="bar", values="OOS_Sharpe")
    for B in BARS[1:]:
        if B not in dso.columns:
            continue
        d = (dso[B] - dso[0.00]).dropna()
        say(f"    bar {B:<5} dOOS_Sharpe vs full menu: mean {d.mean():+.4f}"
            f"  median {d.median():+.4f}  min {d.min():+.4f}  max {d.max():+.4f}")
    return G, WF, M


def main():
    say("=" * 100)
    say("PART A — CENSUS of the record's `family` / `dial` / `panel` label vocabularies")
    say("=" * 100)
    voc, files = scan_corpus()
    for c in COLUMNS:
        say(f"  `{c}` emitted by {len(voc[c])} of {len(files)} committed csvs")
    V, C, J = part_a(voc)

    say("\n  CUMULATIVE distinct tokens as the record is read in run order:")
    say("  " + C.pivot_table(index=["column", "form"], columns="quantile",
                             values="cumulative_tokens").to_string().replace("\n", "\n  "))

    G, WF, M = part_b(voc)

    say("\n" + "=" * 100)
    say("PART C — is the coinage the reason the misses miss?")
    say("=" * 100)
    for col in COLUMNS:
        j = J[J.column == col]
        if j.empty:
            continue
        raw0 = j[(j.form == "RAW") & (j.bar == 0.00)]["disjoint_share_nonempty"].iloc[0]
        stem0 = j[(j.form == "STEM") & (j.bar == 0.00)]["disjoint_share_nonempty"].iloc[0]
        best = j.loc[j["disjoint_share_nonempty"].idxmin()]
        say(f"  `{col}`: disjoint-pair share RAW {raw0:.4f} -> STEM {stem0:.4f}"
            f" (spelling alone recovers {raw0 - stem0:+.4f});"
            f" best cell form {best['form']} bar {best['bar']}"
            f" -> {best['disjoint_share_nonempty']:.4f} on"
            f" {int(best['files_nonempty'])} non-empty files"
            f" (all-pairs {best['disjoint_share_all']:.4f})")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    say("\nwrote .vocab.csv .coinage.csv .join.csv .menu.csv .grid.csv .walkforward.csv"
        " .console.txt")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
