#!/usr/bin/env python3
"""
H4: does management saying "operating leverage is kicking in" predict returns?

Pre-registered in H4_PREREG.md, written before any H4 return was computed. Its
"Deviations" section was also written before the first H4 return and fixes how
the ambiguous lines are read; this script implements that reading and nothing
else. It reuses the H1-H3 machinery from run_tests.py unchanged (universe,
clean_returns, Book, spread_stats, the delisting scenarios, fund_table) and
never writes results.json or quintile_returns.csv.

Reads   panel.parquet, cache/returns.parquet, commentary/*.csv.gz (read only)
Writes  results_h4.json, and the H4 parts of RESULTS.md (the H4 rows of the
        short-answer table and the "H4. Management commentary" section, spliced
        in between markers so a rerun replaces them). run_tests.py regenerates
        RESULTS.md without H4, so run this script after it.

Groups at each June formation t (formation date = last weekday of June t;
window = formation - 365 days <= file_date < formation, strictly before):
  S (H4a)  priced universe company with >= 1 clean event with kicking_in True
           in the window
  S (H4b)  H4a companies whose first in-window kicking_in event falls in a
           calendar quarter preceded by 8 calendar quarters with no "operating
           leverage" mention of any kind (ol_any, ol_positive, ol_negative all 0)
           and a filing in >= 6 of them; all 8 must be >= 2010Q1 (data start)
  S (H4c)  company with >= 1 clean negative event in the window
  N        no clean event of any kind (clean_events or clean_negative_events) in
           the window, and >= 1 10-K/10-Q/8-K in calendar quarters Q3 t-1 .. Q2 t
Test: S minus N, equal-weighted monthly spread, t = mean / (sd / sqrt n), with
Newey-West(6) beside it. H4a and H4b: Yes iff t >= 2.0. H4c: Yes iff t <= -2.0.
H4d: next fiscal year's fundamentals (CY t vs CY t-1), S versus N, no verdict.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from run_tests import (CACHE, COST, FIRST_HALF, HERE, SECOND_HALF, Book, ann, clean, clean_returns,
                       fund_table, half, sort_groups, spread_stats, survivorship, top_vs, tstat)

COMM = HERE / "commentary"
DATA_START_Q = pd.Period("2010Q1", freq="Q")   # first quarter of mentions and filer presence
SILENT_Q = 8                                    # H4b: quiet calendar quarters before the event
MIN_FILING_Q = 6                                # H4b: of which at least this many with a filing
FLAG_S = 20                                     # years with fewer S companies are flagged
FORMATIONS = range(2011, 2026)
S, N = 2, 1                                     # group labels passed to Book.port
TESTS = {"H4a": +1, "H4b": +1, "H4c": -1}       # expected sign of S minus N


def formation_date(t: int) -> pd.Timestamp:
    """The June close the portfolio is formed at: last weekday of June t."""
    d = pd.Timestamp(t, 6, 30)
    while d.weekday() >= 5:
        d -= pd.Timedelta(days=1)
    return d


# --------------------------------------------------------------------------- #
# groups
# --------------------------------------------------------------------------- #
def load_commentary():
    ev = pd.read_csv(COMM / "clean_events.csv.gz", parse_dates=["file_date"], low_memory=False)
    ng = pd.read_csv(COMM / "clean_negative_events.csv.gz", parse_dates=["file_date"], low_memory=False)
    info = {"clean_events_rows": int(len(ev)), "clean_events_missing_sic_dropped": int(ev.sic.isna().sum()),
            "clean_negative_rows": int(len(ng)), "clean_negative_missing_sic_dropped": int(ng.sic.isna().sum())}
    ev, ng = ev[ev.sic.notna()], ng[ng.sic.notna()]
    fp = pd.read_csv(COMM / "filer_presence_by_cik_quarter.csv.gz")
    fp["q"] = pd.PeriodIndex(fp.cal_quarter, freq="Q")
    mq = pd.read_csv(COMM / "mentions_by_cik_quarter.csv.gz", low_memory=False)
    mq["q"] = pd.PeriodIndex(mq.cal_quarter, freq="Q")
    return ev, ng, fp, mq, info


def build_groups(Pm: pd.DataFrame, ev, ng, fp, mq):
    """Label series (index = panel row) for each test: S = 2, N = 1, else NaN."""
    pres = set(zip(fp.cik, fp.q))
    m = mq[(mq.ol_any + mq.ol_positive + mq.ol_negative) > 0]
    mentioned = set(zip(m.cik, m.q))
    lab = {k: pd.Series(np.nan, index=Pm.index) for k in TESTS}
    first_kick = pd.Series(pd.NaT, index=Pm.index, dtype="datetime64[ns]")
    last_kick = pd.Series(pd.NaT, index=Pm.index, dtype="datetime64[ns]")
    diag = {}
    for t, d in Pm.groupby("year"):
        assert not d.cik.duplicated().any()
        f = formation_date(t)
        lo = f - pd.Timedelta(days=365)
        w = ev[(ev.file_date >= lo) & (ev.file_date < f)]
        wn = ng[(ng.file_date >= lo) & (ng.file_date < f)]
        kick = w[w.kicking_in]
        k_first = kick.groupby("cik").file_date.min()
        k_last = kick.groupby("cik").file_date.max()
        qs = pd.period_range(pd.Period(f"{t - 1}Q3", freq="Q"), pd.Period(f"{t}Q2", freq="Q"), freq="Q")
        filers = set(fp.cik[fp.q.isin(qs)])
        is_s = d.cik.isin(k_first.index)
        any_ev = d.cik.isin(set(w.cik) | set(wn.cik))
        is_n = ~any_ev & d.cik.isin(filers)
        is_c = d.cik.isin(set(wn.cik))
        # H4b: first mention after a silence
        status = {}
        for cik in d.cik[is_s]:
            q0 = pd.Period(k_first[cik], freq="Q")
            look = [q0 - k for k in range(1, SILENT_Q + 1)]
            seen = [q for q in look if q >= DATA_START_Q]
            quiet_seen = not any((cik, q) in mentioned for q in seen)
            if len(seen) < SILENT_Q:
                status[cik] = "unobservable_quiet_so_far" if quiet_seen else "unobservable_already_fails"
            elif not quiet_seen:
                status[cik] = "prior_mention"
            elif sum((cik, q) in pres for q in look) < MIN_FILING_Q:
                status[cik] = "filed_in_fewer_than_6_of_8"
            else:
                status[cik] = "qualifies"
        is_b = d.cik.map(status).eq("qualifies")
        for key, sm in (("H4a", is_s), ("H4b", is_b), ("H4c", is_c)):
            lab[key][d.index[sm]] = S
            lab[key][d.index[is_n]] = N
        first_kick[d.index[is_s]] = d.cik[is_s].map(k_first).to_numpy()
        last_kick[d.index[is_s]] = d.cik[is_s].map(k_last).to_numpy()
        u, ms = d.in_univ, d.missing
        st = pd.Series(status, dtype=object)
        stu = st[st.index.isin(d.cik[u])]
        diag[int(t)] = {
            "formation_date": str(f.date()), "window_start": str(lo.date()),
            "universe": int(u.sum()),
            "S_H4a": int((is_s & u).sum()), "S_H4a_missing": int((is_s & ms).sum()),
            "S_H4b": int((is_b & u).sum()), "S_H4b_missing": int((is_b & ms).sum()),
            "S_H4c": int((is_c & u).sum()), "S_H4c_missing": int((is_c & ms).sum()),
            "S_H4c_also_in_H4a": int((is_c & is_s & u).sum()),
            "N": int((is_n & u).sum()), "N_missing": int((is_n & ms).sum()),
            "universe_other_clean_events_only": int((u & any_ev & ~is_s & ~is_c).sum()),
            "universe_no_event_but_no_filing_found": int((u & ~any_ev & ~d.cik.isin(filers)).sum()),
            "H4b_status_universe": {k: int(v) for k, v in stu.value_counts().items()},
        }
    return lab, first_kick, last_kick, diag


# --------------------------------------------------------------------------- #
# one test
# --------------------------------------------------------------------------- #
def matched(book: Book, labU: pd.Series, cell: pd.Series) -> dict:
    """S minus N within formation-year x size-tercile x SIC2 cells, cells weighted
    by their number of S companies at formation (H4_PREREG Deviations item 6)."""
    labU = labU[cell.reindex(labU.index).notna()]
    H = book.H[book.H.pid.isin(labU.index)][["pid", "month", "ret"]].copy()
    H["g"] = H.pid.map(labU)
    H["c"] = H.pid.map(cell)
    m = H.groupby(["month", "c", "g"]).ret.mean().unstack("g").dropna()
    w = labU[labU == S].groupby(cell.reindex(labU[labU == S].index)).size()
    m["w"] = m.index.get_level_values("c").map(w).astype(float)
    m = m[m.w > 0]
    ws = m.w.groupby(level="month").sum()
    s_ret = (m[S] * m.w).groupby(level="month").sum() / ws
    n_ret = (m[N] * m.w).groupby(level="month").sum() / ws
    n_s_year = labU[labU == S].groupby(cell.reindex(labU[labU == S].index).str.slice(0, 4).astype(int)).size()
    share = ws / n_s_year.reindex([mm.year if mm.month >= 7 else mm.year - 1 for mm in ws.index]).to_numpy()
    out = spread_stats(s_ret, n_ret)
    out["n_cells_used_median_per_month"] = float(m.groupby(level="month").size().median())
    out["share_of_S_in_usable_cells_median"] = float(share.median())
    return out


def run_test(key: str, lab: pd.Series, Pm, book, book_raw, book_raw1, univ_ew, iwm, spy, cell) -> dict:
    expect = TESTS[key]
    labU = lab[Pm.in_univ].dropna()
    labM = lab[Pm.missing].dropna()
    labM50 = lab[Pm.missing & (Pm.pfloat >= 50e6)].dropna()
    yrs = Pm.loc[labU.index, "year"]
    nS = labU[labU == S].groupby(yrs).size().reindex(FORMATIONS, fill_value=0)
    nN = labU[labU == N].groupby(yrs).size().reindex(FORMATIONS, fill_value=0)
    ew = book.port(labU)
    vw = book.port(labU, vw=True)
    out = {"expected_sign": expect,
           "n_S_per_year": {int(k): int(v) for k, v in nS.items()},
           "n_N_per_year": {int(k): int(v) for k, v in nN.items()},
           "years_with_S_below_20_flagged": [int(k) for k, v in nS.items() if v < FLAG_S],
           "n_S_firm_years": int(nS.sum()), "n_S_distinct_companies": int(Pm.loc[labU[labU == S].index, "cik"].nunique()),
           "n_N_firm_years": int(nN.sum())}
    out["ew_ann"] = {"S": ann(ew[S]), "N": ann(ew[N])}
    out["vw_ann"] = {"S": ann(vw[S]), "N": ann(vw[N])}
    out["ew_spread"] = spread_stats(ew[S], ew[N])
    out["first_half_ew_spread"] = spread_stats(half(ew, FIRST_HALF)[S], half(ew, FIRST_HALF)[N])
    out["second_half_ew_spread"] = spread_stats(half(ew, SECOND_HALF)[S], half(ew, SECOND_HALF)[N])
    out["matched_size_sic2_ew_spread"] = matched(book, labU, cell)
    out["vw_spread"] = spread_stats(vw[S], vw[N])
    er = book_raw.port(labU)
    out["raw_returns_ew_spread"] = spread_stats(er[S], er[N])
    er1 = book_raw1.port(labU)
    out["raw_returns_minus_largest_month_ew_spread"] = spread_stats(er1[S], er1[N])
    out["top_vs"] = top_vs(ew[S] - COST / 12, univ_ew, iwm, spy)
    out["survivorship"] = survivorship(book, Pm, lab, labU, labM, labM50, S, ew)
    t = out["ew_spread"]["t"]
    passed = (t >= 2.0) if expect > 0 else (t <= -2.0)
    out["verdict"] = {"verdict": "Yes" if passed else "No",
                      "rule": "t >= 2.0" if expect > 0 else "t <= -2.0",
                      "opposite_side_of_bar": bool((t <= -2.0) if expect > 0 else (t >= 2.0))}
    return out, ew


# --------------------------------------------------------------------------- #
# H4d fundamentals
# --------------------------------------------------------------------------- #
def fundamentals(P, Pm, lab, first_kick, last_kick) -> dict:
    U = Pm[Pm.in_univ]
    out = {"table": {}, "by_year_S_minus_N": {}}
    names = {"H4a": "S_kicking_in", "H4b": "S_first_after_silence", "H4c": "S_negative"}
    for key, nm in names.items():
        ft = fund_table(U, lab[key].reindex(U.index))
        out["table"][nm] = ft[S]
        out["table"]["N"] = ft[N]
        g = lab[key].reindex(U.index)
        res = {}
        for col in ("fwd_margin_chg_pp", "fwd_rev_growth"):
            diffs = {}
            for t in FORMATIONS:
                sel = U.year == t
                a = U.loc[sel & (g == S), col].dropna()
                b = U.loc[sel & (g == N), col].dropna()
                if len(a) and len(b):
                    diffs[t] = float(a.median() - b.median())
            ds = pd.Series(diffs)
            res[col] = {"mean": float(ds.mean()), "t": tstat(ds), "years_S_above_N": int((ds > 0).sum()),
                        "n_years": int(len(ds)), "by_year": {int(k): v for k, v in diffs.items()}}
        out["by_year_S_minus_N"][nm] = res
    # timing check (README point 5): does the forward fiscal year end after the event?
    ends = P.set_index(["cik", "year"]).rev_end

    def fwd_ends(rows):
        e = pd.Series([ends.get((c, y + 1), pd.NaT) for c, y in zip(rows.cik, rows.year)], index=rows.index)
        return pd.to_datetime(e)

    def before_july(e, rows):
        k = e.notna()
        return int((e[k] < pd.to_datetime(rows.year[k].astype(str) + "-07-01")).sum())

    s = U[(lab["H4a"].reindex(U.index) == S) & U.fwd_margin_chg_pp.notna()]
    n = U[(lab["H4a"].reindex(U.index) == N) & U.fwd_margin_chg_pp.notna()]
    fwd_end, fwd_end_n = fwd_ends(s), fwd_ends(n)
    known = fwd_end.notna()
    out["timing_check_H4a"] = {
        "S_firm_years_with_fwd_fundamentals": int(len(s)),
        "fwd_year_end_known": int(known.sum()),
        "share_fwd_year_ends_after_last_event": float((fwd_end[known] > last_kick[s.index][known]).mean()),
        "min_days_fwd_year_end_after_formation": int(min(
            (e - formation_date(int(y))).days for e, y in zip(fwd_end[known], s.year[known]))),
        "S_fwd_year_ends_before_july_of_t": before_july(fwd_end, s),
        "N_fwd_year_end_known": int(fwd_end_n.notna().sum()),
        "N_fwd_year_ends_before_july_of_t": before_july(fwd_end_n, n),
        "share_base_year_ended_before_first_event": float((pd.to_datetime(s.rev_end) < first_kick[s.index]).mean()),
        "share_base_year_ended_before_last_event": float((pd.to_datetime(s.rev_end) < last_kick[s.index]).mean()),
    }
    return out


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    before = (HERE / "results.json").read_bytes()
    P = pd.read_parquet(HERE / "panel.parquet").reset_index(drop=True)
    R_raw = pd.read_parquet(CACHE / "returns.parquet")
    R_raw.index = pd.to_datetime(R_raw.index)
    stocks_raw = R_raw.drop(columns=[c for c in ("IWM", "SPY") if c in R_raw.columns])
    R, rinfo = clean_returns(stocks_raw)
    bench = R_raw[["IWM", "SPY"]]
    book = Book(P, R)
    book_raw = Book(P, stocks_raw)
    top1 = book_raw.H.loc[book_raw.H.ret.abs().idxmax()]      # same diagnostic as run_tests.py
    R_raw1 = stocks_raw.copy()
    R_raw1.loc[top1.month, top1.ticker] = np.nan
    book_raw1 = Book(P, R_raw1)
    U = P[P.in_univ]
    Pm = P[P.in_univ | P.missing].copy()
    univ_ew = book.port(pd.Series(1, index=U.index)).iloc[:, 0]
    iwm = bench["IWM"].reindex(univ_ew.index)
    spy = bench["SPY"].reindex(univ_ew.index)

    ev, ng, fp, mq, cinfo = load_commentary()
    lab, first_kick, last_kick, diag = build_groups(Pm, ev, ng, fp, mq)
    terc = sort_groups(Pm[Pm.in_univ], "mcap", 3)
    cell = (Pm.loc[terc.index, "year"].astype(str) + "_" + terc.astype(int).astype(str) + "_"
            + Pm.loc[terc.index, "sic2"].astype(int).astype(str))

    res = {"meta": {
        "prereg": "H4_PREREG.md (the Deviations section there was written before any H4 return was computed)",
        "formations": "2011-2025 (last weekday of June); H4b 2012-2025 (see Deviations item 1)",
        "window": "formation date - 365 days <= file_date < formation date",
        "control_N": "no clean_events or clean_negative_events row in the window, >= 1 filing in Q3 t-1..Q2 t",
        "test": "S minus N, equal-weighted monthly spread; t = mean/(sd/sqrt n); Newey-West(6) beside it",
        "verdict_rule": "H4a, H4b: Yes iff t >= 2.0; H4c: Yes iff t <= -2.0; robustness does not change it",
        "price_error_rule": rinfo, "commentary": cinfo,
        "benchmarks": {"UNIV_EW_ann": ann(univ_ew), "IWM_ann": ann(iwm), "SPY_ann": ann(spy)},
        "groups_per_year": diag}}
    res["meta"]["largest_held_raw_month"] = {"ticker": top1.ticker, "month": str(top1.month.date()),
                                            "raw_return": float(top1.ret), "formation": int(top1.year)}
    for key in TESTS:
        out, ew = run_test(key, lab[key], Pm, book, book_raw, book_raw1, univ_ew, iwm, spy, cell)
        g = lab[key].get(top1.pid, np.nan)
        out["largest_held_raw_month_group"] = {S: "S", N: "N"}.get(g, "neither")
        res[key] = out
        h = out["ew_spread"]
        print(f"{key}: S {h['ann_top']:.4f} N {h['ann_bottom']:.4f} diff {h['ann_diff']:+.4f} t {h['t']:+.2f} "
              f"NW {h['t_nw6']:+.2f} years {h['years_positive']}/{h['n_years']} -> {out['verdict']['verdict']}")
    res["H4d"] = fundamentals(P, Pm, lab, first_kick, last_kick)
    r = clean(res)
    (HERE / "results_h4.json").write_text(json.dumps(r, indent=1))
    assert (HERE / "results.json").read_bytes() == before, "results.json must not change"
    splice(r)
    print("wrote results_h4.json and the H4 parts of RESULTS.md")


# --------------------------------------------------------------------------- #
# RESULTS.md: H4 rows in the short-answer table + the H4 section at the end
# --------------------------------------------------------------------------- #
MARK = "<!-- H4 section: generated by run_h4.py from results_h4.json; a rerun replaces everything below -->"
NOTE_PREFIX = "For the H4 rows,"
TITLES = {"H4a": "H4a. Management says operating leverage is kicking in",
          "H4b": "H4b. The same, said for the first time after two quiet years",
          "H4c": "H4c. Negative operating-leverage commentary"}
LONG = {"H4a": "Companies whose management said operating leverage was kicking in",
        "H4b": "Companies saying it for the first time after two quiet years",
        "H4c": "Companies with negative operating-leverage commentary"}
SHORT = {"H4a": "the group that said it", "H4b": "the first-mention group", "H4c": "the negative-commentary group"}


def _md():
    from md_writer import SCEN_NAMES, money, p, pts, tt
    return SCEN_NAMES, money, p, pts, tt


def ls(s):
    _, _, _, pts, tt = _md()
    return (f"{pts(s['ann_diff'])} a year (t = {tt(s['t'])}; ahead in {s['years_positive']} of "
            f"{s['n_years']} years)")


def answer(x, key):
    _, _, _, _, tt = _md()
    t, v = x["ew_spread"]["t"], x["verdict"]["verdict"]
    if key == "H4c":
        if v == "Yes":
            return f"{LONG[key]} lagged silent companies (t = {tt(t)}, past the pre-registered bar of -2.0)."
        s = (f"{LONG[key]} did not reliably lag silent companies (t = {tt(t)}; the pre-registered bar was -2.0)")
        return s + (", and in fact came out slightly ahead." if x["ew_spread"]["mean_monthly_x12"] > 0 else ".")
    if v == "Yes":
        return f"{LONG[key]} beat silent companies (t = {tt(t)}, at or above the pre-registered bar of 2.0)."
    if x["verdict"]["opposite_side_of_bar"]:
        return (f"{LONG[key]} did reliably worse than silent companies (t = {tt(t)}), the opposite of the "
                f"hypothesis; by the pre-registered rule the answer is No.")
    return (f"{LONG[key]} did not reliably beat silent companies (t = {tt(t)}, below the pre-registered bar of "
            f"2.0).")


def missing_bullet(x):
    SCEN_NAMES, _, p, pts, tt = _md()
    sv = x["survivorship"]
    sc = sv["scenarios_ew_spread"]

    def sct(k):
        return f"{pts(sc[k]['ann_diff'])}, t = {tt(sc[k]['t'])}"
    exp = x["expected_sign"]
    hit = [k for k, v in sc.items() if (v["t"] >= 2.0 if exp > 0 else v["t"] <= -2.0)]
    opp = [k for k, v in sc.items() if (v["t"] <= -2.0 if exp > 0 else v["t"] >= 2.0)]
    signs = {v["mean_monthly_x12"] > 0 for v in sc.values()}
    L = (f"- Missing companies: {p(sv['missing_share_top'])} of the would-be signal group and "
         f"{p(sv['missing_share_bottom'])} of the would-be silent group have no price. Spread with missing firms "
         f"excluded {sct('a_excluded')}; if every missing firm lost 30%: {sct('b_minus30_all_missing')} (only "
         f"those with public float >= $50M: {sct('b_minus30_float50_missing')}); if every missing firm gained "
         f"15%: {sct('c_plus15_all_missing')} ({sct('c_plus15_float50_missing')}). ")
    L += ("The sign does not change across these assumptions. " if len(signs) == 1
          else "**The sign changes across these assumptions.** ")
    if hit or opp:
        parts = [f"{SCEN_NAMES[k]} (t = {tt(sc[k]['t'])}, "
                 f"{'the hypothesised direction' if k in hit else 'the opposite direction to the hypothesis'})"
                 for k in hit + opp]
        L += "The t-statistic gets past 2 only under " + " and ".join(parts) + "."
        if (sv["missing_share_bottom"] > sv["missing_share_top"] and all(k.startswith("b_") for k in hit + opp)
                and abs(sc["b_minus30_float50_missing"]["t"]) < 2.0):
            bg = sv["by_group"]
            small = {g: 1 - bg[g]["missing_float50"] / bg[g]["missing"] for g in (str(S), str(N))}
            L += (f" That comes from the silent group: it has the larger missing share, and more of its missing "
                  f"companies are small ({p(small[str(N)], 0)} report a public float below $50M or none, against "
                  f"{p(small[str(S)], 0)} in the signal group), so a blanket -30% pulls it down more. Counting only "
                  f"missing companies with float >= $50M, the t-statistic is "
                  f"{tt(sc['b_minus30_float50_missing']['t'])}.")
        L += " By the pre-registered rule these lines do not change the answer."
    else:
        L += "No assumption moves the t-statistic past the bar, so the answer does not flip."
    return L


def test_section(r, key, takeaway):
    _, money, p, pts, tt = _md()
    x = r[key]
    h = x["ew_spread"]
    m = h["n_months"]
    L = [f"### {TITLES[key]}{' (primary)' if key == 'H4a' else ''}", ""]
    L.append(f"**Answer: {x['verdict']['verdict']}.** {answer(x, key)}")
    L.append("")
    L.append(f"**Size of the effect (equal-weighted, the pre-registered headline).** {LONG[key]} returned "
             f"{p(h['ann_top'])} a year against {p(h['ann_bottom'])} for silent companies over the same {m} months, "
             f"a gap of {pts(h['ann_diff'])} a year; {SHORT[key]} was ahead in {h['years_positive']} of "
             f"{h['n_years']} holding years. $10,000 held for the {m} months would have become "
             f"{money(h['ann_top'], m)} in {SHORT[key]} and {money(h['ann_bottom'], m)} in the silent group, before "
             f"costs. Monthly spread t-statistic {tt(h['t'])} (Newey-West {tt(h['t_nw6'])}).")
    L.append("")
    L.append("**How much to trust it.**")
    L.append("")
    first = "2012-2017" if key == "H4b" else "2011-2017"
    L.append(f"- First half (formations {first}): {ls(x['first_half_ew_spread'])}. Second half (2018-2025): "
             f"{ls(x['second_half_ew_spread'])}.")
    mt = x["matched_size_sic2_ew_spread"]
    L.append(f"- Matched within size tercile x 2-digit SIC cells, each cell's gap weighted by its number of signal "
             f"companies ({p(mt['share_of_S_in_usable_cells_median'], 0)} of signal companies share a cell with a "
             f"silent company in the median month): {ls(mt)}.")
    L.append(f"- Value-weighted: {ls(x['vw_spread'])}.")
    L.append(missing_bullet(x))
    lm = r["meta"]["largest_held_raw_month"]
    where = {"N": "which sits in the silent group", "S": "which sits in the signal group",
             "neither": "which is in neither group"}[x["largest_held_raw_month_group"]]
    L.append(f"- Raw Yahoo returns, no bad-print rule: {ls(x['raw_returns_ew_spread'])}; raw returns with only the "
             f"single largest held monthly return removed ({lm['ticker']} in {lm['month'][:7]}, {where}): "
             f"{ls(x['raw_returns_minus_largest_month_ew_spread'])}.")
    ns = {int(k): v for k, v in x["n_S_per_year"].items()}
    nn = {int(k): v for k, v in x["n_N_per_year"].items()}
    act = {k: v for k, v in ns.items() if v > 0}
    fl = x["years_with_S_below_20_flagged"]
    cnt = (f"- Company counts: {min(act.values())} to {max(act.values())} signal companies per formation "
           f"({x['n_S_firm_years']:,} company-years, {x['n_S_distinct_companies']:,} distinct companies) against "
           f"{min(nn.values()):,} to {max(nn.values()):,} silent ones. ")
    if fl:
        cnt += (f"Years with fewer than 20 signal companies, kept in and flagged: "
                f"{', '.join(f'{k} ({ns[k]})' for k in fl)}.")
    else:
        cnt += "No year has fewer than 20."
    if key == "H4b":
        q = sum(d["H4b_status_universe"].get("unobservable_quiet_so_far", 0)
                for d in r["meta"]["groups_per_year"].values())
        cnt += (f" Statements before 2012 cannot be checked for two quiet years, so {q} companies in the 2011-2012 "
                f"formations that might qualify are left out (Deviations item 1).")
    L.append(cnt)
    tv = x["top_vs"]
    L.append(f"- {SHORT[key][0].upper() + SHORT[key][1:]} after 0.5% a year of trading costs: "
             f"{p(tv['univ_ew']['ann_top_net'])} a year vs {p(tv['univ_ew']['ann_bench'])} for the equal-weighted "
             f"universe ({pts(tv['univ_ew']['ann_excess'])}, t = {tt(tv['univ_ew']['t'])}), "
             f"{p(tv['iwm']['ann_bench'])} for IWM ({pts(tv['iwm']['ann_excess'])}, t = {tt(tv['iwm']['t'])}) and "
             f"{p(tv['spy']['ann_bench'])} for SPY ({pts(tv['spy']['ann_excess'])}, t = {tt(tv['spy']['t'])}).")
    L.append("")
    L.append(f"**For picking stocks.** {takeaway}")
    L.append("")
    return "\n".join(L)


# Plain-English consequence for stock picking, written after the results were
# in; each phrases numbers from the results and falls back to a neutral
# sentence if the verdict differs from the one seen when it was written.
def _take_h4a(r):
    _, _, p, pts, _ = _md()
    x, f = r["H4a"], r["H4d"]["table"]
    if x["verdict"]["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    return (f"Do not buy a stock because management says operating leverage is kicking in. The statement does "
            f"line up with wider margins the next year (H4d below), but the stocks did no better than those of companies that "
            f"said nothing: {pts(x['ew_spread']['ann_diff'])} a year, ahead in {x['ew_spread']['years_positive']} "
            f"of {x['ew_spread']['n_years']} years, {pts(x['matched_size_sic2_ew_spread']['ann_diff'])} against "
            f"silent companies of the same size and industry, and {pts(x['vw_spread']['ann_diff'])} value-weighted. "
            f"By the time the statement is in a filing, the improvement appears to be in the price.")


def _take_h4b(r):
    _, _, p, pts, tt = _md()
    x = r["H4b"]
    if x["verdict"]["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    h1, h2 = x["first_half_ew_spread"], x["second_half_ew_spread"]
    ns = {int(k): v for k, v in x["n_S_per_year"].items() if int(k) <= 2017 and v > 0}
    return (f"The \"first time in two years\" version looks better on paper ({pts(x['ew_spread']['ann_diff'])} a "
            f"year) but does not clear the bar, rests on a handful of stocks a year, and all of the gain comes from "
            f"the 2012-2017 formations ({pts(h1['ann_diff'])} a year, t = {tt(h1['t'])}, with only "
            f"{min(ns.values())} to {max(ns.values())} stocks a year); in the 2018-2025 formations the group "
            f"trailed silent companies by {pts(h2['ann_diff'])[1:]} a year. One strong half among many cuts is the "
            f"kind of result chance produces. Not a rule to trade; at most a question to re-test once more filings "
            f"have accumulated.")


def _take_h4c(r):
    _, _, p, pts, _ = _md()
    x, fd = r["H4c"], r["H4d"]
    if x["verdict"]["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    return (f"Negative operating-leverage commentary did not mark a stock to avoid: those companies kept pace with "
            f"silent ones ({pts(x['ew_spread']['ann_diff'])} a year, ahead in {x['ew_spread']['years_positive']} of "
            f"{x['ew_spread']['n_years']} years). Their margins slipped slightly the next year (median "
            f"{fd['table']['S_negative']['fwd_margin_chg_pp']:+.2f} points against "
            f"{fd['table']['N']['fwd_margin_chg_pp']:+.2f}, not reliably year by year; H4d), but that was no "
            f"return signal. Few companies say it (a median of "
            f"{int(np.median([v for v in x['n_S_per_year'].values()]))} a year), so the test is also weak.")


def _take_h4d(r):
    d = r["H4d"]
    a = d["by_year_S_minus_N"]["S_kicking_in"]
    f = d["table"]
    return (f"The statement is informative about the business, not the stock. Companies that said operating "
            f"leverage was kicking in widened margins by a median {f['S_kicking_in']['fwd_margin_chg_pp']:+.2f} "
            f"points the next year against {f['N']['fwd_margin_chg_pp']:+.2f} for silent companies, ahead in "
            f"{a['fwd_margin_chg_pp']['years_S_above_N']} of {a['fwd_margin_chg_pp']['n_years']} years. They also "
            f"grew sales faster ({f['S_kicking_in']['fwd_rev_growth'] * 100:.1f}% against "
            f"{f['N']['fwd_rev_growth'] * 100:.1f}%), so the margin gain goes hand in hand with faster growth, as "
            f"in H2b. Use the "
            f"phrase as a prompt to study a company's cost structure, not as a reason to buy: H4a shows the stocks "
            f"earned nothing extra for it.")


def fund_section(r):
    _, _, p, _, tt = _md()
    d = r["H4d"]
    f = d["table"]
    tc = d["timing_check_H4a"]
    rows = ["| Group | Company-years with next-year data | Next-year change in operating margin (median, pts) | "
            "Next-year revenue growth (median) | Change in revenue growth (median, pts) |",
            "|---|---|---|---|---|"]
    for k, nm in (("S_kicking_in", "Said it is kicking in (H4a)"),
                  ("S_first_after_silence", "First time after two quiet years (H4b)"),
                  ("S_negative", "Negative commentary (H4c)"), ("N", "Silent (control)")):
        v = f[k]
        rows.append(f"| {nm} | {v['n_with_fwd']:,} | {v['fwd_margin_chg_pp']:+.2f} | {p(v['fwd_rev_growth'])} | "
                    f"{v['fwd_growth_chg'] * 100:+.1f} |")
    by = d["by_year_S_minus_N"]

    def yl(k, col, unit):
        z = by[k][col]
        mean = f"{z['mean']:+.2f} points" if unit == "pp" else f"{z['mean'] * 100:+.1f} points"
        return (f"ahead in {z['years_S_above_N']} of {z['n_years']} years (average yearly gap in medians {mean}, "
                f"t = {tt(z['t'])})")
    L = ["### H4d. Do margins follow? (fundamentals, no verdict)", ""]
    L.append("**Next fiscal year, CY t vs CY t-1, the same measure as H1-H3.**")
    L.append("")
    L.extend(rows)
    L.append("")
    L.append(f"Year by year, against silent companies: the H4a group's median margin change was "
             f"{yl('S_kicking_in', 'fwd_margin_chg_pp', 'pp')}, and its median revenue growth "
             f"{yl('S_kicking_in', 'fwd_rev_growth', 'g')}. H4b margin change: "
             f"{yl('S_first_after_silence', 'fwd_margin_chg_pp', 'pp')}. H4c margin change: "
             f"{yl('S_negative', 'fwd_margin_chg_pp', 'pp')}.")
    L.append("")
    L.append(f"Timing (README point 5): the forward fiscal year ends after the company's last statement in the window "
             f"in {p(tc['share_fwd_year_ends_after_last_event'], 0)} of the {tc['fwd_year_end_known']:,} H4a "
             f"company-years where its end date is on file ({tc['S_fwd_year_ends_before_july_of_t']} of them are "
             f"June 30 year-ends that close on or just after the formation date, a correction to Deviations item 8 "
             f"recorded in `H4_PREREG.md`). For {p(1 - tc['share_base_year_ended_before_first_event'], 0)} of H4a "
             f"company-years the first statement came before the base year (CY t-1) had ended, so some of the "
             f"improvement being described is already in the base year; the next-year change measures only what "
             f"came after.")
    L.append("")
    L.append(f"**For picking stocks.** {_take_h4d(r)}")
    L.append("")
    return "\n".join(L)


def render_h4(r):
    _, _, p, _, _ = _md()
    gp = r["meta"]["groups_per_year"]
    nN = [v["N"] for v in gp.values()]
    f = r["H4d"]["table"]
    L = [MARK, "", "## H4. Management commentary", ""]
    L.append("**Question.** When management says in an earnings release or a 10-Q that operating leverage is "
             "kicking in, does the stock go on to beat companies that said nothing about it? Pre-registered in "
             "`H4_PREREG.md` before any H4 return was computed:")
    L.append("")
    L.append("- **H4a (primary, carries the verdict):** companies with at least one \"kicking in\" statement in the "
             "365 days before the June formation (an 8-K or 10-Q that uses \"operating leverage\" with a positive "
             "direction cue, from the precision-checked `commentary/` dataset) against silent companies: universe "
             "companies with no clean operating-leverage filing of any kind, positive or negative, in that window "
             "that were filing with the SEC.")
    L.append("- **H4b:** only companies for which that statement was the first operating-leverage mention after at "
             "least eight quiet calendar quarters (while filing in at least six of them).")
    L.append("- **H4c:** companies with negative operating-leverage commentary; expected to lag.")
    L.append("- **H4d:** do margins and sales actually improve the next fiscal year? No verdict.")
    L.append("")
    L.append(f"Same universe, returns, bad-print rule and delisting scenarios as H1-H3. A statement counts only if "
             f"its EDGAR filing date is strictly before the formation date (the last weekday of June); companies "
             f"are matched on SEC CIK, so no ticker mapping is involved. The bar is t >= 2.0 on the equal-weighted "
             f"monthly spread (t <= -2.0 for H4c), and unlike H1-H3 the robustness lines do not change the answer. "
             f"The silent group holds {min(nN):,} to {max(nN):,} companies a year. Companies that talk about "
             f"operating leverage are somewhat larger (median market cap ${f['S_kicking_in']['median_signal_mcap'] / 1e9:.1f}B "
             f"for the H4a group vs ${f['N']['median_signal_mcap'] / 1e9:.1f}B for silent companies), hence the "
             f"matched size-and-industry version.")
    L.append("")
    L.append("**Deviations from the pre-registration**, all written into `H4_PREREG.md` before any H4 return was "
             "computed: (1) the mention and filing records start in 2010, so two quiet years can only be verified "
             "for statements from 2012 on; H4b has no portfolio in the June 2011 formation and counts only "
             "January-June 2012 statements for June 2012, so it covers 14 formations; (2) filing activity is "
             "recorded by calendar quarter, so \"filing during the window\" means a 10-K, 10-Q or 8-K in the four "
             "calendar quarters from July of t-1 to June of t. Items 3-9 there fix how ambiguous lines were read "
             "(formation date, the control group, the silence test, the matched version, the missing-company "
             "scenarios, H4d timing, the verdict rule). One factual correction was added after the results (see "
             "H4d); it changes no definition or number.")
    L.append("")
    L.append(test_section(r, "H4a", _take_h4a(r)))
    L.append(test_section(r, "H4b", _take_h4b(r)))
    L.append(test_section(r, "H4c", _take_h4c(r)))
    L.append(fund_section(r))
    L.append("**Files.** `research/oplev/run_h4.py` computes H4 and writes this section and the H4 rows of the "
             "short-answer table; every H4 number is in `research/oplev/results_h4.json`. `run_tests.py` rewrites "
             "this file without H4 (its own numbers in `results.json` are untouched by H4), so run `run_h4.py` "
             "after it. H4 adds three return tests to the four above; the multiple-testing caveat applies with "
             "more force.")
    return "\n".join(L) + "\n"


def short_rows(r):
    _, _, _, pts, tt = _md()
    out = []
    for key in TESTS:
        x = r[key]
        h = x["ew_spread"]
        title = TITLES[key] + (" (expected to lag)" if key == "H4c" else "")
        out.append(f"| {title} | {x['verdict']['verdict']} | {pts(h['ann_diff'])} | {tt(h['t'])} | "
                   f"{h['years_positive']} of {h['n_years']} |")
    return out


def splice(r):
    path = HERE / "RESULTS.md"
    lines = path.read_text().split("\n")
    if MARK in lines:
        lines = lines[:lines.index(MARK)]
    kept = []
    for ln in lines:
        if ln.startswith("| H4"):
            continue
        if ln.startswith(NOTE_PREFIX):
            if kept and kept[-1] == "":
                kept.pop()                                   # the blank line inserted with the note
            continue
        kept.append(ln)
    lines = kept
    while lines and lines[-1] == "":
        lines.pop()
    i = max(j for j, ln in enumerate(lines) if ln.startswith("| H3."))       # last row of the short table
    lines[i + 1:i + 1] = short_rows(r)
    k = next(j for j, ln in enumerate(lines) if ln.startswith("\"Top minus bottom\""))
    note = (f"{NOTE_PREFIX} \"top\" is the companies whose management made the statement and \"bottom\" is universe "
            f"companies that said nothing about operating leverage in the year before formation; H4b starts with "
            f"the June 2012 formation. Details in the H4 section at the end.")
    lines[k + 1:k + 1] = ["", note]
    path.write_text("\n".join(lines) + "\n\n" + render_h4(r))


if __name__ == "__main__":
    main()
