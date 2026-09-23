#!/usr/bin/env python
"""
Descriptive stats for the operating-leverage commentary dataset.

Inputs : mentions.csv.gz, tone_mentions.csv.gz, clean_events.csv.gz, clean_negative_events.csv.gz,
         mentions_by_cik_quarter.csv.gz, filer_universe_by_year.csv,
         filer_presence_by_cik_quarter.csv.gz (from fetch_universe.py)
Outputs: stats/*.csv and descriptive_stats.md

    .venv/bin/python research/oplev/commentary/describe.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "stats"
PHRASE_ORDER = ["operating leverage", "positive operating leverage", "negative operating leverage",
                "operating deleverage", "incremental margin", "incremental margins",
                "fixed cost absorption", "fixed-cost leverage"]
GROUPS = ["ol_any", "ol_positive", "ol_negative", "incremental", "absorption"]
FORMS = ["8-K", "10-Q", "10-K"]
LAST_FULL_Q = "2026Q2"   # 2026Q3 only runs to 2026-09-23

SIC2 = {1: "Agricultural production - crops", 2: "Agricultural production - livestock", 7: "Agricultural services",
        8: "Forestry", 9: "Fishing", 10: "Metal mining", 12: "Coal mining", 13: "Oil & gas extraction",
        14: "Nonmetallic minerals mining", 15: "Building construction", 16: "Heavy construction",
        17: "Construction special trades", 20: "Food & kindred products", 21: "Tobacco", 22: "Textile mills",
        23: "Apparel", 24: "Lumber & wood", 25: "Furniture & fixtures", 26: "Paper", 27: "Printing & publishing",
        28: "Chemicals & pharma", 29: "Petroleum refining", 30: "Rubber & plastics", 31: "Leather",
        32: "Stone, clay, glass", 33: "Primary metals", 34: "Fabricated metal products",
        35: "Industrial machinery & computer equipment", 36: "Electronic & electrical equipment (incl. semis)",
        37: "Transportation equipment", 38: "Instruments & medical devices", 39: "Misc. manufacturing",
        40: "Railroads", 41: "Local transit", 42: "Trucking & warehousing", 44: "Water transportation",
        45: "Air transportation", 46: "Pipelines", 47: "Transportation services", 48: "Communications",
        49: "Electric, gas & sanitary utilities", 50: "Wholesale - durable goods", 51: "Wholesale - nondurable goods",
        52: "Building materials retail", 53: "General merchandise stores", 54: "Food stores",
        55: "Auto dealers & gas stations", 56: "Apparel stores", 57: "Home furniture stores",
        58: "Restaurants", 59: "Misc. retail", 60: "Banks (depository institutions)",
        61: "Non-bank lenders", 62: "Brokers & dealers", 63: "Insurance carriers", 64: "Insurance agents & brokers",
        65: "Real estate", 67: "Holding & investment offices (REITs, SPACs)", 70: "Hotels", 72: "Personal services",
        73: "Business services (incl. software)", 75: "Auto repair & services", 76: "Misc. repair",
        78: "Motion pictures", 79: "Amusement & recreation", 80: "Health services", 81: "Legal services",
        82: "Educational services", 83: "Social services", 86: "Membership organizations",
        87: "Engineering, accounting, research & mgmt services", 89: "Services NEC", 99: "Nonclassifiable"}


def md_table(df: pd.DataFrame, floatfmt="{:.1%}") -> str:
    df = df.copy()
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join([df.index.name or ""] + cols) + " |",
             "|" + "---|" + "---:|" * len(cols)]
    for idx, row in df.iterrows():
        vals = []
        for v in row:
            if isinstance(v, (float, np.floating)) and not pd.isna(v) and float(v).is_integer() and abs(v) > 1:
                vals.append(f"{int(v):,}")
            elif isinstance(v, (float, np.floating)) and not pd.isna(v) and abs(v) <= 1.0 and floatfmt:
                vals.append(floatfmt.format(v))
            elif isinstance(v, (float, np.floating)) and not pd.isna(v):
                vals.append(f"{v:,.1f}")
            elif isinstance(v, (int, np.integer)):
                vals.append(f"{v:,}")
            else:
                vals.append("" if pd.isna(v) else str(v))
        lines.append("| " + " | ".join([str(idx)] + vals) + " |")
    return "\n".join(lines)


def qnext(q: str) -> str:
    y, n = int(q[:4]), int(q[-1])
    return f"{y + (n == 4)}Q{n % 4 + 1}"


def main():
    OUT.mkdir(exist_ok=True)
    m = pd.read_csv(HERE / "mentions.csv.gz", dtype={"sic": "string", "items": "string", "all_sics": "string"},
                    low_memory=False)
    fq = pd.read_csv(HERE / "mentions_by_cik_quarter.csv.gz", dtype={"sic": "string"})
    uni = pd.read_csv(HERE / "filer_universe_by_year.csv", index_col="year")
    pres = pd.read_csv(HERE / "filer_presence_by_cik_quarter.csv.gz")
    md = ["# Operating-leverage commentary - descriptive statistics", "",
          "Source: SEC EDGAR full-text search, exact phrases, forms 8-K / 10-Q / 10-K (amendments included, "
          "flagged), filed 2010-01-01 to 2026-09-23. **2026 is a partial year (to Sep 23).** "
          "'Files' = matched documents (a filing can have several matched exhibits); 'filings' = distinct "
          "accession numbers; 'companies' = distinct CIKs.", ""]

    # ---- 1. totals per phrase x form
    files = m.drop_duplicates(["adsh", "file_name", "phrase", "query_form"])
    tot = (files.groupby(["phrase", "query_form"]).size().unstack("query_form").reindex(index=PHRASE_ORDER, columns=FORMS)
           .fillna(0).astype(int))
    tot["all forms"] = tot.sum(axis=1)
    tot.index.name = "phrase (FTS hits = files)"
    fil = (m.drop_duplicates(["adsh", "phrase"]).groupby("phrase").size().reindex(PHRASE_ORDER))
    com = m.groupby("phrase").cik.nunique().reindex(PHRASE_ORDER)
    tot["filings"] = fil
    tot["companies"] = com
    tot.to_csv(OUT / "totals_by_phrase_form.csv")
    md += ["## 1. Totals", "", md_table(tot, floatfmt=None), ""]
    grp_c = m.groupby("phrase_group").cik.nunique().reindex(GROUPS)
    md += [f"Distinct companies (CIKs) with at least one hit, by group: " +
           ", ".join(f"{g} {int(v):,}" for g, v in grp_c.items()) +
           f"; any phrase {m.cik.nunique():,}.", ""]
    roles = files[files.phrase == "operating leverage"].copy()
    roles["where"] = np.select(
        [roles.query_form.eq("8-K") & roles.is_ex99 & roles.is_earnings_8k,
         roles.query_form.eq("8-K") & roles.is_ex99, roles.query_form.eq("8-K"),
         roles.is_main_doc, roles.doc_role.eq("ex13_annual_report")],
        ["8-K Item 2.02 EX-99 (earnings release / call transcript / deck)", "8-K other EX-99 (investor deck, transcript)",
         "8-K main doc or other exhibit", "10-Q/10-K main document", "10-K EX-13 annual report"],
        "10-Q/10-K other exhibit")
    wt = roles.groupby("where").size().sort_values(ascending=False).to_frame("files")
    wt["share"] = wt.files / wt.files.sum()
    wt.index.name = "where 'operating leverage' matched"
    wt.to_csv(OUT / "operating_leverage_by_doc_type.csv")
    md += [md_table(wt), ""]

    # ---- 2. per year by phrase and form (filings), plus companies per year
    byy = (m.drop_duplicates(["adsh", "phrase"]).groupby(["year", "phrase", "query_form"]).size()
           .unstack(["phrase", "query_form"]).fillna(0).astype(int))
    byy.to_csv(OUT / "filings_by_year_phrase_form.csv")
    t = pd.DataFrame(index=byy.index)
    for ph in PHRASE_ORDER:
        for f in FORMS:
            t[f"{ph} | {f}"] = byy.get((ph, f), 0)
    t.index.name = "year"
    short = {"operating leverage": "OL", "positive operating leverage": "posOL", "negative operating leverage": "negOL",
             "operating deleverage": "deleverage", "incremental margin": "incr.margin", "incremental margins": "incr.margins",
             "fixed cost absorption": "fixed cost absorp.", "fixed-cost leverage": "fixed-cost lev."}
    t.columns = [f"{short[c.split(' | ')[0]]} {c.split(' | ')[1]}" for c in t.columns]
    md += ["## 2. Filings per year, by phrase and form", "",
           "Distinct filings (accessions) with at least one matched file. 2026 = Jan 1 - Sep 23 only.", "",
           md_table(t[[c for c in t.columns if c.startswith(("OL ", "posOL", "negOL", "deleverage"))]], floatfmt=None), "",
           md_table(t[[c for c in t.columns if not c.startswith(("OL ", "posOL", "negOL", "deleverage"))]], floatfmt=None), ""]

    cy = m.groupby(["year", "phrase_group"]).cik.nunique().unstack("phrase_group").reindex(columns=GROUPS).fillna(0).astype(int)
    cy["any phrase"] = m.groupby("year").cik.nunique()
    nonfin = m[m.is_financial == False]  # noqa: E712
    cy["ol_any non-financial"] = nonfin[nonfin.phrase_group == "ol_any"].groupby("year").cik.nunique()
    cy["ol_any financial"] = m[(m.is_financial == True) & (m.phrase_group == "ol_any")].groupby("year").cik.nunique()  # noqa: E712
    cy = cy.join(uni[["n_ciks_10k_or_10q", "n_ciks_8k"]])
    cy["ol_any share of 10-K/10-Q filers"] = cy["ol_any"] / cy["n_ciks_10k_or_10q"]
    cy["ol_positive share"] = cy["ol_positive"] / cy["n_ciks_10k_or_10q"]
    cy["ol_negative share"] = cy["ol_negative"] / cy["n_ciks_10k_or_10q"]
    cy.index.name = "year"
    cy.to_csv(OUT / "companies_by_year.csv")
    md += ["## 3. Distinct companies per year", "",
           "Denominator = distinct CIKs that filed a 10-K or 10-Q that year (EDGAR master index). "
           "It includes SPACs (a 2021-22 surge), which depresses the share in those years.", "",
           md_table(cy), ""]

    # quarterly view of tone (companies), for 2020 / 2022 spikes
    q = m[m.phrase_group.isin(["ol_any", "ol_positive", "ol_negative"])]
    cq = q.groupby(["cal_quarter", "phrase_group"]).cik.nunique().unstack("phrase_group").fillna(0).astype(int)
    cq.to_csv(OUT / "companies_by_quarter.csv")
    sel = cq.loc[[i for i in cq.index if i[:4] in ("2019", "2020", "2021", "2022", "2023")]]
    sel.index.name = "quarter"
    md += ["Companies per calendar quarter, 2019-2023 (full series in stats/companies_by_quarter.csv):", "",
           md_table(sel[["ol_any", "ol_positive", "ol_negative"]], floatfmt=None), ""]

    # ---- 4. industries
    base = m[m.phrase_group == "ol_any"].copy()
    firm_sic = (m.sort_values("file_date").groupby("cik").sic.agg(lambda s: s.dropna().iloc[-1] if s.notna().any() else None))
    def ind_table(sub, label):
        c = sub.groupby("cik").size().index
        s2 = (pd.to_numeric(firm_sic.reindex(c), errors="coerce") // 100)
        t = s2.value_counts(dropna=False).to_frame("companies")
        t["share of companies"] = t.companies / t.companies.sum()
        f = sub.drop_duplicates(["adsh"]).assign(sic2=lambda d: pd.to_numeric(d.sic, errors="coerce") // 100)
        t["filings"] = f.groupby("sic2", dropna=False).size().reindex(t.index).fillna(0).astype(int)
        t["share of filings"] = t.filings / t.filings.sum()
        t.index = [("missing" if pd.isna(i) else f"{int(i):02d} {SIC2.get(int(i), '?')}") for i in t.index]
        t.index.name = f"SIC2 ({label})"
        return t
    md += ["## 4. Industries (2-digit SIC, latest SIC on the filings)", ""]
    for grp, label in [("ol_any", "operating leverage"), ("ol_positive", "positive operating leverage"),
                       ("ol_negative", "negative OL / deleverage"), ("incremental", "incremental margin(s)"),
                       ("absorption", "fixed cost absorption / leverage")]:
        t = ind_table(m[m.phrase_group == grp], label)
        t.to_csv(OUT / f"industries_{grp}.csv")
        top = t.sort_values("filings", ascending=False)
        fin_share = m[(m.phrase_group == grp)].drop_duplicates("adsh").is_financial.mean()
        md += [f"**{label}** - top 12 by filings; financials (SIC 6000-6999) = {fin_share:.1%} of filings; "
               f"top-5 SIC2 = {top['share of filings'].head(5).sum():.1%} of filings.", "",
               md_table(top.head(12)), ""]

    # ---- 5. persistence
    fq = fq[fq.cal_quarter <= LAST_FULL_Q]
    pres = pres[(pres.cal_quarter >= "2010Q1") & (pres.cal_quarter <= LAST_FULL_Q)]
    pres["active"] = (pres.n_10k + pres.n_10q) > 0
    act = pres[pres.active][["cik", "cal_quarter"]]
    pan = act.merge(fq, on=["cik", "cal_quarter"], how="left")
    cols = ["ol_any", "ol_positive", "ol_negative", "incremental", "absorption", "ol_any_release"]
    pan[cols] = pan[cols].fillna(0)
    pan = pan.merge(firm_sic.rename("sic_f").reset_index(), on="cik", how="left")
    # SIC is only known for firms that appear in the mentions data (it comes from their filings), so the
    # financial / non-financial split is only meaningful among ever-users; base rates use all firms.
    pan["fin"] = pd.to_numeric(pan.sic_f, errors="coerce").between(6000, 6999).fillna(False).astype(bool)
    pan["nxt"] = pan.cal_quarter.map(qnext)
    nxt = pan[["cik", "cal_quarter"] + cols].rename(columns={"cal_quarter": "nxt", **{c: c + "_n" for c in cols}})
    pp = pan.merge(nxt, on=["cik", "nxt"], how="inner")       # firm active in both q and q+1
    ever = set(fq[fq.ol_any > 0].cik)
    rows = []
    for c in cols:
        for lab, sub in [("all", pp), ("non-financial", pp[~pp.fin]), ("financial", pp[pp.fin])]:
            hit, miss = sub[sub[c] > 0], sub[(sub[c] == 0) & sub.cik.isin(set(fq[fq[c] > 0].cik))]
            rows.append(dict(measure=c, filers=lab,
                             n_firm_quarters_with_mention=len(hit),
                             p_next_q_given_mention=(hit[c + "_n"] > 0).mean() if len(hit) else np.nan,
                             p_next_q_given_no_mention_ever_user=(miss[c + "_n"] > 0).mean() if len(miss) else np.nan,
                             share_of_all_active_firm_quarters=(sub[c] > 0).mean() if lab == "all" else np.nan))
    per = pd.DataFrame(rows).set_index(["measure", "filers"])
    per.to_csv(OUT / "persistence_quarterly.csv")
    # yearly persistence and how many quarters firms mention
    yr = m[m.phrase_group == "ol_any"].groupby("cik").year.agg(lambda s: sorted(set(s)))
    pairs = [(y in ys and (y + 1) in ys) for ys in yr for y in ys if y + 1 <= 2025]
    denom = sum(1 for ys in yr for y in ys if y + 1 <= 2025)
    nq = fq[fq.ol_any > 0].groupby("cik").size()
    nq_dist = pd.cut(nq, [0, 1, 2, 4, 8, 16, 32, 100], labels=["1", "2", "3-4", "5-8", "9-16", "17-32", "33+"]).value_counts().sort_index()
    nq_t = nq_dist.to_frame("companies")
    nq_t["share of companies"] = nq_t.companies / nq_t.companies.sum()
    nq_t["share of mention firm-quarters"] = nq.groupby(pd.cut(nq, [0, 1, 2, 4, 8, 16, 32, 100],
                                                               labels=nq_t.index)).sum() / nq.sum()
    nq_t.index.name = "quarters with an 'operating leverage' mention"
    nq_t.to_csv(OUT / "persistence_quarters_per_firm.csv")
    per_md = per.copy()
    per_md.index = [f"{a} / {b}" for a, b in per_md.index]
    per_md.index.name = "measure / filers"
    md += ["## 5. Persistence", "",
           "Panel = every CIK x calendar quarter in which the firm filed a 10-K or 10-Q (EDGAR master index), "
           f"2010Q1-{LAST_FULL_Q}; transition q -> q+1 only where the firm filed in both quarters. "
           "'no-mention, ever-user' = quarters without a mention at firms that use the phrase at some point.", "",
           md_table(per_md), "",
           f"Year to year: a company that says 'operating leverage' in year t says it again in year t+1 "
           f"{sum(pairs) / denom:.1%} of the time (t = 2010-2024, n = {denom:,} company-years).", "",
           md_table(nq_t), ""]
    top_rep = (fq[fq.ol_any > 0].groupby("cik").size().sort_values(ascending=False).head(15).to_frame("quarters")
               .join(fq.groupby("cik")[["display_name", "sic"]].last()))
    top_rep.index.name = "cik"
    md += ["Most persistent users (quarters with an 'operating leverage' mention, of 66 full quarters):", "",
           md_table(top_rep, floatfmt=None), ""]

    # ---- 6. supplementary direction phrases and the clean events
    t = pd.read_csv(HERE / "tone_mentions.csv.gz", dtype={"sic": "string", "items": "string"}, low_memory=False)
    tf = t.drop_duplicates(["adsh", "file_name", "phrase", "query_form"])
    tt = tf.groupby(["phrase", "query_form"]).size().unstack("query_form").reindex(columns=FORMS).fillna(0).astype(int)
    tt["all forms"] = tt.sum(axis=1)
    tt["companies"] = t.groupby("phrase").cik.nunique()
    tt["financial share of filings"] = t.drop_duplicates(["adsh", "phrase"]).groupby("phrase").is_financial.mean()
    tt["group"] = t.drop_duplicates("phrase").set_index("phrase").phrase_group
    tt = tt.sort_values(["group", "all forms"], ascending=[False, False])
    tt.index.name = "supplementary phrase (FTS hits = files)"
    tt.to_csv(OUT / "tone_totals.csv")
    ev = pd.read_csv(HERE / "clean_events.csv.gz")
    neg = pd.read_csv(HERE / "clean_negative_events.csv.gz")
    ey = pd.DataFrame({
        "clean events (filings)": ev.groupby("year").size(),
        "clean: companies": ev.groupby("year").cik.nunique(),
        "clean: 8-K": ev[ev.event_channel.eq("8-K")].groupby("year").size(),
        "clean: 10-Q": ev[ev.event_channel.eq("10-Q")].groupby("year").size(),
        "clean: 10-K": ev[ev.event_channel.eq("10-K")].groupby("year").size(),
        "kicking_in (filings)": ev[ev.kicking_in].groupby("year").size(),
        "kicking_in: companies": ev[ev.kicking_in].groupby("year").cik.nunique(),
        "negative events (filings)": neg.groupby("year").size(),
        "negative: companies": neg.groupby("year").cik.nunique(),
    }).fillna(0).astype(int)
    ey.index.name = "year"
    ey.to_csv(OUT / "clean_events_by_year.csv")
    eq = pd.DataFrame({"kicking_in companies": ev[ev.kicking_in].groupby("cal_quarter").cik.nunique(),
                       "negative-event companies": neg.groupby("cal_quarter").cik.nunique()}).fillna(0).astype(int)
    eq.to_csv(OUT / "clean_events_by_quarter.csv")
    eq_sel = eq.loc[[i for i in eq.index if i[:4] in ("2019", "2020", "2021", "2022", "2023")]]
    eq_sel.index.name = "quarter"
    md += ["## 6. Supplementary direction phrases and the clean events", "",
           "Not in the original phrase list; fetched to give the tone field something other than bank "
           "language (see README).", "", md_table(tt), "",
           "Clean events (definition in README; non-financial, non-SPAC, original filings) per year:", "",
           md_table(ey, floatfmt=None), "",
           "Companies with a kicking_in event vs a negative event, by quarter 2019-2023:", "",
           md_table(eq_sel, floatfmt=None), ""]

    (HERE / "descriptive_stats.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
