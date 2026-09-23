#!/usr/bin/env python3
"""Build CALM's quarterly history (fiscal 2016 Q1 - fiscal 2026 Q4) from the cached SEC filings.

Inputs: cache/sec/filings_manifest.csv and the documents it lists (run sec_fetch.py first).
Output: data/calm_quarterly.csv (one row per fiscal quarter) and data/calm_sources.csv
        (which document each group of numbers came from).

Sources per quarter
  * Earnings release (8-K Item 2.02, EX-99.1), current 13-week column, AS FIRST REPORTED:
      net sales, cost of sales, gross profit, SG&A, operating income, total other income, pre-tax income,
      income tax, net income attributable to Cal-Maine, diluted EPS, diluted weighted shares.
  * 10-Q (Q1-Q3) or 10-K (fiscal year; Q4 = year minus the three 10-Q quarters) MD&A tables:
      conventional / specialty (incl. co-pack specialty, which was reported separately until fiscal 2020)
      shell egg sales and dozens sold, net average selling price per dozen (reported and implied),
      egg products, prepared foods and other sales, farm production cost per dozen produced (feed, other),
      dozens produced, outside-egg purchase cost per dozen, average CBOT corn and soybean meal prices,
      and the reported YoY change in the Urner Barry southeast large index.
  * Fiscal 2026 Q4: the fiscal 2026 10-K dropped the per-dozen tables (new segment structure). Conventional
    and specialty volume/price for that quarter are rebuilt from the Q4 FY2026 release's segment table
    (volume change % and average price change % vs Q4 FY2025), applied to Q4 FY2025.
"""
import re, sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from htmltext import html_to_text  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
TOK = re.compile(r"\(?\$?-?\d[\d,]*(?:\.\d+)?\)?%?|—")


def flat_text(path):
    t = html_to_text(open(ROOT / path, errors="replace").read()).replace("|", " ")
    t = re.sub("[\ufeff\u200b\u200c\u200d\u2060]", " ", t)
    t = re.sub(r"\s+", " ", t)
    t = t.replace("Non- specialty", "Non-specialty").replace("Non -specialty", "Non-specialty")
    t = re.sub(r"\$\s+", "$", t)
    t = re.sub(r"\(\s+", "(", t)
    t = re.sub(r"\s+\)", ")", t)
    t = re.sub(r"(\d)\s+%", r"\1%", t)
    t = re.sub(r"\)\s+%", ")%", t)
    return t


def tonum(tok):
    if tok is None or tok == "—":
        return 0.0 if tok == "—" else np.nan
    neg = tok.startswith("(") and tok.endswith(")")
    s = tok.strip("()$%").replace(",", "").replace("$", "")
    try:
        v = float(s)
    except ValueError:
        return np.nan
    return -v if neg else v


def nums_after(t, pat, start=0, stop=None, n=1, flags=0):
    """First n numeric tokens after regex `pat` (skipping percentages). Returns list or None."""
    seg = t[start:stop] if stop else t[start:]
    m = re.search(pat, seg, flags)
    if not m:
        return None
    rest = seg[m.end(): m.end() + 400]
    out = []
    for tok in TOK.findall(rest):
        if tok.endswith("%"):
            continue
        out.append(tonum(tok))
        if len(out) == n:
            break
    return out if len(out) == n else None


def first(t, pat, start=0, stop=None, flags=0):
    r = nums_after(t, pat, start, stop, 1, flags)
    return r[0] if r else np.nan


# ---------------------------------------------------------------- periodic reports (10-Q / 10-K)
def parse_periodic(t):
    out = {}
    # --- dozens / price block
    m = re.search(r"Dozens sold:?\s*(?=(Non-specialty|Conventional))", t)
    if m:
        b0 = m.start()
        mt = re.compile(r"Total( dozens sold)?\s+\$?[\d,]").search(t, b0)
        b1 = mt.start() if mt else b0 + 300
        blk_end = b1 + 30
        out["conv_doz"] = first(t, r"(Non-specialty|Conventional)( shell eggs?)?", b0, blk_end)
        out["spec_doz"] = first(t, r"(?<![Cc]o-pack )Specialty( shell eggs?)?", b0, blk_end)
        cp = first(t, r"Co-pack specialty( shell eggs?)?", b0, blk_end)
        out["copack_doz"] = 0.0 if np.isnan(cp) else cp
        out["total_doz"] = first(t, r"Total( dozens sold)?", b1 - 1, b1 + 60)
        p0 = t.find("Net average selling price", b1)
        if 0 < p0 - b1 < 200:
            p1 = p0 + 260
            out["conv_price_rep"] = first(t, r"(Non-specialty|Conventional)( shell eggs)?", p0, p1)
            out["spec_price_rep"] = first(t, r"(?<![Cc]o-pack )Specialty( shell eggs)?", p0, p1)
            allp = first(t, r"All shell eggs", p0, p1)
            if np.isnan(allp):
                allp = first(t, r"Net average selling price( per dozen)?:?", p0, p0 + 60)
            out["all_price_rep"] = allp
    # --- sales: revenue disaggregation note (fiscal 2019 on), else MD&A table
    m = re.search(r"(Conventional|Non-specialty) shell egg sales\s*\$?[\d,]+\s", t)
    if m:
        s0 = m.start()
        stop = s0 + 700
        out["conv_sales"] = first(t, r"(Conventional|Non-specialty) shell egg sales", s0, stop)
        out["spec_sales"] = first(t, r"(?<![Cc]o-pack )Specialty shell egg sales", s0, stop)
        cp = first(t, r"Co-pack specialty shell egg sales", s0, stop)
        out["copack_sales"] = 0.0 if np.isnan(cp) else cp
        pf = first(t, r"Prepared foods", s0, stop)
        out["prepared_sales"] = 0.0 if np.isnan(pf) else pf
        out["eggprod_sales"] = first(t, r"Egg products", s0, stop)
        out["other_sales"] = first(t, r"Other", s0, stop)
        out["sales_src"] = "revenue disaggregation note"
        hdr = t[max(0, s0 - 260): s0]
        out["note_q4_first"] = bool(re.search(r"1[34] Weeks Ended\s+(Fifty|5[23]) ?[Ww]eeks Ended|1[34] Weeks Ended 5[23] Weeks Ended", hdr))
    else:
        m = re.search(r"(Total net sales|Net [Ss]ales)\s+\$?[\d,]+\s+\$?[\d,]+(?:\s+\$?[\d,]+\s+\$?[\d,]+)?\s+(Shell egg sales:\s*)?(?=Non-specialty|Conventional)", t)
        if m:
            s0 = m.start()
            stop = t.find("Dozens sold", s0)
            out["md_total_sales"] = first(t, r"(Total net sales|Net [Ss]ales)", s0, stop)
            out["conv_sales"] = first(t, r"(Non-specialty|Conventional)( shell eggs?)?( sales)?", s0, stop)
            out["spec_sales"] = first(t, r"(?<![Cc]o-pack )Specialty( shell eggs?)?( sales)?", s0, stop)
            cp = first(t, r"Co-pack specialty( shell eggs?)?( sales)?", s0, stop)
            out["copack_sales"] = 0.0 if np.isnan(cp) else cp
            out["netshell_sales"] = first(t, r"Net shell egg sales", s0, stop)
            out["other_sales"] = first(t, r"Other", s0, stop)
            out["prepared_sales"] = 0.0
            out["sales_src"] = "MD&A net sales table"
    # --- farm production cost per dozen produced
    m = re.search(r"Farm production costs? \(per dozen p ?roduced\)", t)
    if m:
        f0 = m.start()
        out["feed_per_doz"] = first(t, r"Feed", f0, f0 + 200)
        out["otherfarm_per_doz"] = first(t, r"Other", f0, f0 + 260)
        out["farm_per_doz"] = first(t, r"Total( farm production cost)?", f0, f0 + 330)
        out["outside_cost_per_doz"] = first(t, r"Outside egg purchases \(average cost per dozen\)|Egg purchases \(average cost per dozen\)", f0, f0 + 500)
        out["doz_produced"] = first(t, r"Doz(en|ens) [Pp]roduced", f0 + 40, f0 + 700)
    # --- cost of sales breakdown (farm production dollars etc.)
    m = re.search(r"Cost of sales:?\s*Farm production\s+\$?[\d,]", t)
    if m:
        c0 = m.start()
        out["cogs_farm"] = first(t, r"Farm production", c0, c0 + 100)
        out["cogs_proc"] = first(t, r"Processing,? (and )?packaging", c0, c0 + 400)
        out["cogs_purch"] = first(t, r"(Outside egg|Egg) purchases and other( cost of sales)?", c0, c0 + 600)
        out["cogs_prepared"] = first(t, r"Prepared foods", c0, c0 + 700)
        out["cogs_eggprod"] = first(t, r"Egg products", c0, c0 + 800)
    # --- CBOT corn / soybean meal (first mention = the quarter in a 10-Q, the year in a 10-K)
    m = re.search(r"(Chicago Board of Trade|Chiago Board of Trade|CBOT)[^$]{0,120}\$([\d.]+) per bushel for corn and \$([\d,.]+) per ton", t)
    if m:
        out["cbot_corn"] = float(m.group(2))
        out["cbot_sbm"] = float(m.group(3).replace(",", ""))
    # --- Urner Barry southeast large, YoY change as reported
    m = re.search(r"(Urner[- ]Barry [Ss]outheast(ern)? (Regional )?[Ll]arge|UB southeastern large) (index|Egg Market Price)[^.]{0,160}?(increased|decreased|was (up|down)|were (up|down)|up|down)\s+([\d.]+)%", t)
    if m:
        sign = -1 if ("decrease" in m.group(0) or "down" in m.group(0)) else 1
        out["ub_yoy_rep"] = sign * float(m.group(8)) / 100
    m = re.search(r"USDA daily average price for large shell eggs (increased|decreased) ([\d.]+)%", t)
    if m:
        out["usda_yoy_rep"] = (-1 if m.group(1) == "decreased" else 1) * float(m.group(2)) / 100
    return out


# ---------------------------------------------------------------- earnings releases
REL = {
    "rel_net_sales": r"Net sales",
    "rel_cogs": r"Cost of sales",
    "rel_gross_profit": r"Gross profit( \(loss\))?",
    "rel_sga": r"Selling, general,? and administrative",
    "rel_op_income": r"Operating income( \(loss\))?",
    "rel_other_income": r"(Total other income( \(expense\))?|Other income( \(expense\))?, net)",
    "rel_pretax": r"Income( \(loss\))? before income taxes( and noncontrolling interest)?",
    "rel_tax": r"Income tax(es)? expense( \(benefit\))?",
    "rel_ni_attr": r"Net income( \(loss\))? attributable to Cal-Maine Foods,? Inc\.?",
    "rel_eps_dil": r"Diluted",
}


def parse_release(t):
    i = -1
    for key in ["SUMMARY STATEMENTS OF INCOME", "CONSOLIDATED STATEMENTS OF INCOME", "STATEMENTS OF INCOME",
                "STATEMENTS OF OPERATIONS", "Statements of Income"]:
        i = t.find(key)
        if i >= 0:
            break
    i = max(i, 0)
    j = t.find("Net sales", i)
    out = {}
    stop = t.find("BALANCE SHEET", j)
    stop = stop if stop > 0 else j + 4000
    for k, pat in REL.items():
        out[k] = first(t, pat, j, stop)
    if np.isnan(out["rel_ni_attr"]):
        out["rel_ni_attr"] = first(t, r"Net income( \(loss\))?", j + 200, stop)
    m = re.search(r"Weighted average shares outstanding:?\s*Basic\s+([\d,]+)\s+[\d,]+\s+(?:[\d,]+\s+[\d,]+\s+)?Diluted\s+([\d,]+)", t)
    if m:
        out["rel_shares_basic"] = tonum(m.group(1))
        out["rel_shares_dil"] = tonum(m.group(2))
    return out


# ---------------------------------------------------------------- XBRL companyfacts (fills gaps in release parsing)
XBRL_MAP = {
    "rel_net_sales": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "rel_cogs": ["CostOfGoodsAndServicesSold", "CostOfRevenue"],
    "rel_gross_profit": ["GrossProfit"],
    "rel_sga": ["SellingGeneralAndAdministrativeExpense"],
    "rel_op_income": ["OperatingIncomeLoss"],
    "rel_other_income": ["NonoperatingIncomeExpense"],
    "rel_pretax": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                   "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
    "rel_tax": ["IncomeTaxExpenseBenefit"],
    "rel_ni_attr": ["NetIncomeLoss"],
}


def xbrl_quarters(Q):
    import json
    cf = json.load(open(ROOT / "cache/sec/companyfacts.json"))["facts"]["us-gaap"]
    out = {}
    for col, tags in XBRL_MAP.items():
        facts = []
        for tag in tags:
            if tag not in cf:
                continue
            for u, arr in cf[tag]["units"].items():
                for f in arr:
                    if "start" in f:
                        facts.append(dict(tag=tag, start=f["start"], end=f["end"], val=f["val"], filed=f["filed"]))
        if not facts:
            continue
        F = pd.DataFrame(facts)
        F["dur"] = (pd.to_datetime(F.end) - pd.to_datetime(F.start)).dt.days
        F = F.sort_values("filed").drop_duplicates(["start", "end"], keep="first")  # as first reported
        for _, r in Q.iterrows():
            if pd.isna(r.period_end):
                continue
            end = str(r.period_end)[:10]
            if r.q in (1, 2, 3):
                m = F[(F.end == end) & (F.dur.between(80, 100))]
                if len(m):
                    out[(r.fy, r.q, col)] = m.iloc[0].val / 1000.0
            else:
                fyv = F[(F.end == end) & (F.dur.between(350, 380))]
                qs = [out.get((r.fy, k, col)) for k in (1, 2, 3)]
                if len(fyv) and all(v is not None for v in qs):
                    out[(r.fy, 4, col)] = fyv.iloc[0].val / 1000.0 - sum(qs)
    return out


def fiscal_label(period_end):
    """CALM fiscal year ends on the Saturday nearest May 31. Quarter from the period end month."""
    d = pd.Timestamp(period_end)
    fy = d.year + (1 if d.month >= 6 else 0)
    if d.month == 6 and d.day <= 7:  # FY ending in early June (e.g. 2017-06-03, 2019-06-01)
        fy = d.year
    m = d.month
    q = {8: 1, 9: 1, 11: 2, 12: 2, 2: 3, 3: 3, 5: 4, 6: 4}[m]
    return fy, q


def main():
    man = pd.read_csv(ROOT / "cache/sec/filings_manifest.csv")
    per = man[man.form.isin(["10-Q", "10-K"])].copy()
    rows, srcs = {}, []
    for _, r in per.iterrows():
        fy, q = fiscal_label(r.report_date)
        if r.form == "10-K":
            q = 0  # full year
        t = flat_text(r.local)
        d = parse_periodic(t)
        d.update(fy=fy, q=q, period_end=r.report_date, filed=r.filing_date, form=r.form)
        rows[(fy, q)] = d
        srcs.append(dict(fy=fy, q=q, kind=r.form, filed=r.filing_date, url=r.url))
    P = pd.DataFrame(rows.values())

    # ---- releases: map each 2.02 8-K to the quarter it reports (the next periodic report filed same day or after)
    rel = man[man.form == "8-K"].copy()
    R = []
    for _, r in rel.iterrows():
        t = flat_text(r.local)
        d = parse_release(t)
        # quarter = periodic report with the closest filing date on/after the release
        cand = per[per.filing_date >= r.filing_date].sort_values("filing_date")
        pr = cand.iloc[0]
        fy, q = fiscal_label(pr.report_date)
        if pr.form == "10-K":
            q = 4
        d.update(fy=fy, q=q, rel_date=r.filing_date, rel_accepted_utc=r.accepted_utc, rel_url=r.url)
        R.append(d)
        srcs.append(dict(fy=fy, q=q, kind="8-K EX-99.1", filed=r.filing_date, url=r.url))
    R = pd.DataFrame(R)

    # ---- quarterly frame; derive Q4 = FY - (Q1+Q2+Q3) from 10-K
    Q = P[P.q > 0].copy()
    flows = ["conv_doz", "spec_doz", "copack_doz", "total_doz", "conv_sales", "spec_sales", "copack_sales",
             "prepared_sales", "eggprod_sales", "other_sales", "netshell_sales", "md_total_sales", "doz_produced",
             "cogs_farm", "cogs_proc", "cogs_purch", "cogs_prepared", "cogs_eggprod"]
    q4rows = []
    for _, y in P[P.q == 0].iterrows():
        fy = y.fy
        qs = Q[Q.fy == fy]
        if len(qs) != 3:
            continue
        d = dict(fy=fy, q=4, period_end=y.period_end, filed=y.filed, form="10-K (FY minus Q1-Q3)")
        sales_cols = ["conv_sales", "spec_sales", "copack_sales", "prepared_sales", "eggprod_sales", "other_sales"]
        for c in flows:
            if c in sales_cols and y.get("note_q4_first") is True and pd.notna(y.get(c)):
                d[c] = y[c]  # 10-K revenue note shows the 13/14-week fourth quarter first
            elif c in y and pd.notna(y[c]) and qs[c].notna().all():
                d[c] = y[c] - qs[c].sum()
        # per-dozen farm costs: production-weighted
        for c in ["feed_per_doz", "otherfarm_per_doz", "farm_per_doz"]:
            if pd.notna(y.get(c)) and pd.notna(y.get("doz_produced")) and qs[c].notna().all() and "doz_produced" in d:
                d[c] = (y[c] * y["doz_produced"] - (qs[c] * qs["doz_produced"]).sum()) / d["doz_produced"]
        # CBOT for Q4: year average x 4 - sum of quarters (approximation: equal-weight quarters)
        # (CBOT Q4 not derived: the 10-K quotes the fiscal-year average only)
        q4rows.append(d)
    Q = pd.concat([Q, pd.DataFrame(q4rows)], ignore_index=True)
    Q = Q.merge(R, on=["fy", "q"], how="outer").sort_values(["fy", "q"]).reset_index(drop=True)

    # ---- drop the fiscal 2015 Q4 release (no periodic tables for fiscal 2015 Q1-Q3 in the pull)
    Q = Q[~((Q.fy == 2015))].reset_index(drop=True)
    # ---- fill / repair release numbers from XBRL (first reported); flag what was filled
    X = xbrl_quarters(Q)
    Q["filled_from_xbrl"] = ""
    for i, r in Q.iterrows():
        for col in XBRL_MAP:
            xv = X.get((r.fy, r.q, col))
            if xv is None:
                continue
            cur = r[col]
            garbled = (r.fy == 2016 and r.q == 4)  # spaces inside numbers in that release's text
            bad = pd.isna(cur) or garbled or (col == "rel_net_sales" and abs(cur - xv) > 0.5 * abs(xv))
            if bad:
                Q.loc[i, col] = xv
                Q.loc[i, "filled_from_xbrl"] += col.replace("rel_", "") + ";"
    # fiscal 2016 Q4 release text is garbled (spaces inside numbers); diluted shares from the fiscal 2017 Q4
    # release's prior-year column (48,247) and EPS as released (-0.01)
    i = Q.index[(Q.fy == 2016) & (Q.q == 4)][0]
    Q.loc[i, "rel_shares_dil"] = 48247.0
    Q.loc[i, "filled_from_xbrl"] += "shares from FY17 Q4 release prior-year column;"
    # net income attributable: releases for fiscal 2018 Q1-Q2 parsed badly -> recompute check vs EPS x shares
    for i, r in Q.iterrows():
        if pd.notna(r.rel_eps_dil) and pd.notna(r.rel_shares_dil) and pd.notna(r.rel_ni_attr):
            if abs(r.rel_ni_attr / r.rel_shares_dil - r.rel_eps_dil) > 0.05:
                xv = X.get((r.fy, r.q, "rel_ni_attr"))
                if xv is not None:
                    Q.loc[i, "rel_ni_attr"] = xv
                    Q.loc[i, "filled_from_xbrl"] += "ni_attr(release parse failed check);"

    # ---- consistent definitions
    Q["spec_doz_all"] = Q.spec_doz + Q.copack_doz.fillna(0)
    Q["spec_sales_all"] = Q.spec_sales + Q.copack_sales.fillna(0)
    Q["conv_price"] = Q.conv_sales / Q.conv_doz
    Q["spec_price"] = Q.spec_sales_all / Q.spec_doz_all
    Q["shell_sales"] = Q.conv_sales + Q.spec_sales_all
    Q["nonshell_sales"] = Q.rel_net_sales * 1.0 - Q.shell_sales
    Q["prepared_sales"] = Q.prepared_sales.fillna(0)

    # ---- fiscal 2026 Q4 from the Q4 release segment table (per-dozen tables no longer published)
    q4_25 = Q[(Q.fy == 2025) & (Q.q == 4)].iloc[0]
    i = Q.index[(Q.fy == 2026) & (Q.q == 4)][0]
    # Q4 FY2026 release: Conventional volume +3.1%, avg price -70.9%; Specialty volume -5.9%, avg price -16.5%
    Q.loc[i, "conv_doz"] = q4_25.conv_doz * 1.031
    Q.loc[i, "conv_price"] = q4_25.conv_price * (1 - 0.709)
    Q.loc[i, "spec_doz_all"] = q4_25.spec_doz_all * (1 - 0.059)
    Q.loc[i, "spec_price"] = q4_25.spec_price * (1 - 0.165)
    Q.loc[i, "conv_sales"] = Q.loc[i, "conv_doz"] * Q.loc[i, "conv_price"]
    Q.loc[i, "spec_sales_all"] = Q.loc[i, "spec_doz_all"] * Q.loc[i, "spec_price"]
    Q.loc[i, "shell_sales"] = Q.loc[i, "conv_sales"] + Q.loc[i, "spec_sales_all"]
    Q.loc[i, "nonshell_sales"] = Q.loc[i, "rel_net_sales"] - Q.loc[i, "shell_sales"]
    Q.loc[i, "prepared_sales"] = 60403.0  # Prepared Foods segment sales, Q4 FY2026 release
    Q.loc[i, "total_doz"] = Q.loc[i, "conv_doz"] + Q.loc[i, "spec_doz_all"]
    Q.loc[i, "derived_note"] = "Q4 FY26 volumes/prices rebuilt from segment % changes vs Q4 FY25"

    Q["period_start"] = pd.to_datetime(Q.period_end).shift(1) + pd.Timedelta(days=1)
    Q.loc[Q.index[0], "period_start"] = pd.Timestamp(Q.period_end.iloc[0]) - pd.Timedelta(days=90)
    keep = ["fy", "q", "period_start", "period_end", "rel_date", "rel_accepted_utc", "filed",
            "rel_net_sales", "rel_cogs", "rel_gross_profit", "rel_sga", "rel_op_income", "rel_other_income",
            "rel_pretax", "rel_tax", "rel_ni_attr", "rel_eps_dil", "rel_shares_dil",
            "conv_sales", "spec_sales_all", "shell_sales", "prepared_sales", "eggprod_sales", "other_sales",
            "nonshell_sales", "conv_doz", "spec_doz_all", "total_doz", "conv_price", "spec_price",
            "conv_price_rep", "spec_price_rep", "all_price_rep", "feed_per_doz", "otherfarm_per_doz",
            "farm_per_doz", "doz_produced", "outside_cost_per_doz", "cogs_farm", "cogs_proc", "cogs_purch",
            "cogs_prepared", "cogs_eggprod", "cbot_corn", "cbot_sbm", "ub_yoy_rep", "usda_yoy_rep",
            "sales_src", "derived_note", "filled_from_xbrl", "rel_url"]
    Q = Q[[c for c in keep if c in Q.columns]]
    Q.to_csv(DATA / "calm_quarterly.csv", index=False, float_format="%.4f")
    pd.DataFrame(srcs).sort_values(["fy", "q", "kind"]).to_csv(DATA / "calm_sources.csv", index=False)
    print(Q[["fy", "q", "period_end", "rel_net_sales", "rel_eps_dil", "conv_doz", "conv_price", "conv_price_rep",
             "spec_doz_all", "spec_price", "feed_per_doz", "cbot_corn", "ub_yoy_rep"]].to_string())


if __name__ == "__main__":
    main()
