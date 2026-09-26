#!/usr/bin/env python3
"""Stage 4: map each contract transaction to a listed company.

Key = the transaction's own (point-in-time) parent recipient name as carried
on USAspending (FPDS ultimate parent); when the parent is blank, the recipient
name itself. Matching against the alias list (every current and former SEC
name of every candidate company, all industries, so that a parent name that
belongs to a large or financial company is not handed to a small one):

  1. exact   - parent core == alias core (legal-form words removed);
  2. prefix  - the alias core is a leading part of the parent core and passes
               prefix_ok() (e.g. "VECTRUS SYSTEMS", "KRATOS UNMANNED AERIAL
               SYSTEMS"); longest alias wins;
  3. hand    - data/hand_aliases.csv (parent core -> CIK), built by reading
               the largest unmatched parent names that contain a company's
               search phrase;
  Rows whose parent is the recipient itself (or blank) are matched only by
  rule 1 or 3: USAspending labels every identifier with its current name.
  4. id_link - UEI/DUNS links: a recipient (or parent entity) whose identifier
               appears in name-matched rows of company X is mapped to X for its
               other rows, only within the dates the link was observed.
If one name maps to several CIKs (predecessor/successor registrants), the CIK
whose SEC filing history covers the action date is used, then a listed one,
then the one that filed most recently.

Writes cache/mapped.parquet (mapped transactions, FY2010+) and
data/mapping_pairs.csv (one row per parent name -> CIK pair, with totals).
"""
from __future__ import annotations

import gzip
import json

import numpy as np
import pandas as pd

from common import CACHE, DATA, core, distinctive, log, norm_tokens
from s1_universe import load_subs

BUSINESS_WORDS = {
    "SYSTEMS", "SYSTEM", "SERVICES", "SERVICE", "SOLUTIONS", "TECHNOLOGIES", "TECHNOLOGY",
    "TECH", "INTERNATIONAL", "GOVERNMENT", "FEDERAL", "DEFENSE", "DEFENCE", "AND", "SECURITY",
    "ENGINEERING", "CONSULTING", "MANAGEMENT", "ENTERPRISES", "ENTERPRISE", "INDUSTRIES",
    "INFORMATION", "LABORATORIES", "LABORATORY", "LABS", "AEROSPACE", "ELECTRONICS",
    "MANUFACTURING", "AMERICA", "AMERICAS", "USA", "US", "NORTH", "WORLDWIDE", "GLOBAL",
    "OPERATIONS", "PRODUCTS", "CONSTRUCTORS", "CONSTRUCTION", "CONTRACTING", "HEALTH",
    "HEALTHCARE", "MEDICAL", "RESEARCH", "SCIENCES", "SCIENCE", "PHARMACEUTICALS",
    "PHARMACEUTICAL", "THERAPEUTICS", "INC", "CORP", "CORPORATION", "CO", "COMPANY", "LLC",
    "LTD", "LP", "HOLDINGS", "HOLDING", "GROUP", "OF", "THE", "INCORPORATED", "PUBLIC",
    "SECTOR", "MISSION", "NATIONAL", "SPECIAL", "PROGRAMS", "INTEGRATED", "ADVANCED",
    "DYNAMICS", "COMMUNICATIONS", "NETWORKS", "SOFTWARE", "SUPPORT", "LOGISTICS", "ENERGY",
    "ENVIRONMENTAL", "INFRASTRUCTURE", "MARINE", "SHIPYARD", "SHIPYARDS", "AVIATION",
    "AIRCRAFT", "SPACE", "MISSILE", "DEVICES", "INSTRUMENTS", "CONTROLS", "POWER",
}


STRICT_WORDS = {
    "SYSTEMS", "SYSTEM", "SERVICES", "SERVICE", "SOLUTIONS", "TECHNOLOGIES", "TECHNOLOGY", "TECH",
    "INTERNATIONAL", "GOVERNMENT", "FEDERAL", "DEFENSE", "DEFENCE", "AND", "SECURITY", "ENGINEERING",
    "AEROSPACE", "ELECTRONICS", "MANUFACTURING", "AMERICA", "AMERICAS", "USA", "US", "NORTH",
    "WORLDWIDE", "GLOBAL", "OPERATIONS", "PRODUCTS", "CONSTRUCTORS", "CONSTRUCTION", "HEALTH",
    "HEALTHCARE", "MEDICAL", "RESEARCH", "SCIENCES", "LABORATORIES", "LABS", "INC", "CORP",
    "CORPORATION", "CO", "COMPANY", "LLC", "LTD", "LP", "OF", "THE", "INCORPORATED", "BUSINESS",
    "MISSION", "SUPPORT", "LOGISTICS", "INFRASTRUCTURE", "COMMUNICATIONS", "NETWORKS", "SOFTWARE",
    "DYNAMICS", "MARINE", "AVIATION", "SPACE", "POWER", "ENERGY", "ENVIRONMENTAL", "INDUSTRIES",
    "INFORMATION", "PUBLIC", "SECTOR", "SPECIAL", "PROGRAMS",
}


def prefix_ok(head: str, rest: list[str]) -> bool:
    """May a parent name that starts with company core `head` be mapped to it?
    - a distinctive core of 3+ words (e.g. KRATOS DEFENSE AND SECURITY
      SOLUTIONS): yes, whatever follows;
    - otherwise only if every following word is a generic corporate word
      (e.g. VECTRUS SYSTEMS, AECOM GLOBAL, ENGILITY SERVICES), so that
      'APOLLO MANAGEMENT' is not Apollo Education and 'WILLIAMS PROFESSIONAL
      SERVICES' is not Williams Companies."""
    t = head.split()
    if not distinctive(head):
        return False
    if len(t) >= 3:
        return True
    return all(w in STRICT_WORDS for w in rest)


def alias_table() -> pd.DataFrame:
    """Every SEC name of every candidate. A former name is valid only around the
    dates it was in use (name_valid); a current name is valid at any date."""
    U = pd.read_csv(DATA / "universe_all.csv")
    rows = []
    for _, u in U.iterrows():
        cik = int(u.cik)
        js = load_subs(cik) or {}
        fns = js.get("formerNames") or []
        last_to = max((pd.Timestamp(fn["to"]).tz_localize(None) for fn in fns if fn.get("to")), default=None)
        # current names carry no start date: USAspending labels a parent identity
        # with its *current* name on all its rows, so a registrant renamed later
        # (TeamStaff -> DLH, AECOM Technology -> AECOM) shows the new name on old rows
        names = [(u["name"], None, None), (js.get("name") or "", None, None)]
        for fn in fns:
            a = pd.Timestamp(fn["from"]).tz_localize(None) if fn.get("from") else None
            b = pd.Timestamp(fn["to"]).tz_localize(None) if fn.get("to") else None
            names.append((fn.get("name") or "", a, b))
        for n, a, b in names:
            c = core(n)
            if c:
                rows.append(dict(cik=cik, alias=n, core=c, a_from=a, a_to=b))
    A = pd.DataFrame(rows)
    # one row per (cik, core): the widest window
    A = A.groupby(["cik", "core"]).agg(alias=("alias", "first"),
                                        a_from=("a_from", lambda s: s.min() if s.notna().all() else None),
                                        a_to=("a_to", lambda s: s.max() if s.notna().all() else None)).reset_index()
    return A


def name_valid(a_from, a_to, d) -> bool:
    """Name in use on date d, with slack: names show up in FPDS parent data up
    to a year before an SEC name change is recorded and linger for up to two
    years after."""
    if a_from is not None and pd.notna(a_from) and d < a_from - pd.Timedelta(days=365):
        return False
    if a_to is not None and pd.notna(a_to) and d > a_to + pd.Timedelta(days=730):
        return False
    return True


def alive_windows(ciks) -> dict:
    """cik -> (first filing date, last 10-K/10-Q/20-F date) from the cached submissions."""
    out = {}
    for cik in ciks:
        js = load_subs(int(cik)) or {}
        rec = (js.get("filings") or {}).get("recent") or {}
        d = pd.to_datetime(pd.Series(rec.get("filingDate", [])), errors="coerce")
        f = pd.Series(rec.get("form", []))
        first = d.min() if len(d) else pd.NaT
        for fi in (js.get("filings") or {}).get("files") or []:
            fr = pd.to_datetime(fi.get("filingFrom"), errors="coerce")
            if pd.notna(fr) and (pd.isna(first) or fr < first):
                first = fr
        per = d[f.isin(["10-K", "10-Q", "10-K405", "10-KT", "20-F", "40-F", "10-K/A", "10-Q/A"])]
        last = per.max() if len(per) else (d.max() if len(d) else pd.NaT)
        out[int(cik)] = (first, last)
    return out


def load_transactions() -> pd.DataFrame:
    fs = sorted((CACHE / "dl").glob("b*.parquet"))
    T = pd.concat([pd.read_parquet(f) for f in fs], ignore_index=True)
    n0 = len(T)
    T = T.drop_duplicates("contract_transaction_unique_key")
    T["action_date"] = pd.to_datetime(T.action_date, errors="coerce")
    T["amount"] = pd.to_numeric(T.federal_action_obligation, errors="coerce")
    log(f"transactions: {n0} rows downloaded, {len(T)} unique")
    return T


def main():
    T = load_transactions()
    A = alias_table()
    by_core = {}
    for r in A.itertuples():
        by_core.setdefault(r.core, []).append((int(r.cik), r.a_from, r.a_to))
    hand = {}
    hp = DATA / "hand_aliases.csv"
    if hp.exists():
        H = pd.read_csv(hp, comment="#")
        hand = {core(r.parent_name): int(r.cik) for r in H.itertuples() if int(r.cik) > 0}
        # blocks act on the full parent name (not the core), so blocking
        # 'GRAHAM GROUP LTD' does not also block 'GRAHAM CORP'
        block_full = {" ".join(norm_tokens(r.parent_name)) for r in H.itertuples() if int(r.cik) <= 0}
    else:
        block_full = set()
    hand_block = set()

    T["pname"] = T.recipient_parent_name.where(T.recipient_parent_name.fillna("").str.strip() != "",
                                               T.recipient_name)
    T["pcore"] = T.pname.fillna("").map(core)
    pairs = {}
    for pc in T.pcore.unique():
        if not pc or pc in hand_block:
            continue
        if pc in hand:
            pairs[pc] = ([(hand[pc], None, None)], "hand")
            continue
        if pc in by_core:
            pairs[pc] = (by_core[pc], "exact")
            continue
        toks = pc.split()
        for k in range(len(toks) - 1, 0, -1):
            head = " ".join(toks[:k])
            if head in by_core and prefix_ok(head, toks[k:]):
                pairs[pc] = (by_core[head], "prefix")
                break
    T["cands"] = T.pcore.map(lambda c: pairs.get(c, (None, None))[0])
    T["match"] = T.pcore.map(lambda c: pairs.get(c, (None, None))[1])
    T["blocked"] = T.pname.fillna("").map(lambda n: " ".join(norm_tokens(n))).isin(block_full)
    T.loc[T.blocked, "cands"] = None
    T.loc[T.blocked, "match"] = None
    log(f"  rows with a blocked parent name: {int(T.blocked.sum())}")
    # USAspending shows each identifier (UEI/DUNS) under its *current* name. When
    # the parent is the recipient itself (or blank), the name therefore says
    # nothing about who owned the recipient at the time (a subsidiary renamed
    # after its acquirer shows the acquirer's brand on pre-acquisition awards).
    # Such rows are mapped only by an exact name match with a registrant (the
    # recipient is the listed company itself) or a hand alias.
    def same(a, b):
        a, b = str(a).strip(), str(b).strip()
        return a not in ("", "nan", "None") and a == b
    T["self_parent"] = ((T.recipient_parent_name.fillna("").str.strip() == "").to_numpy()
                        | np.array([same(a, b) for a, b in zip(T.recipient_parent_uei, T.recipient_uei)], bool)
                        | np.array([same(a, b) for a, b in zip(T.recipient_parent_duns, T.recipient_duns)], bool)
                        | (T.pcore == T.recipient_name.fillna("").map(core)).to_numpy())
    weak = T.self_parent & T.match.isin(["prefix"])
    T.loc[weak, "cands"] = None
    T.loc[weak, "match"] = None
    M = T[T.cands.notna()].copy()
    allc = sorted({c for cs in M.cands for c, _, _ in cs})
    win = alive_windows(allc)
    U = pd.read_csv(DATA / "universe_all.csv").set_index("cik")

    def pick(row):
        cs = sorted({c for c, a, b in row.cands if name_valid(a, b, row.action_date)})
        if not cs:
            return -2                      # the matching name was not in use on the action date
        if len(cs) == 1:
            return cs[0]
        ok = [c for c in cs if pd.notna(win[c][0]) and win[c][0] <= row.action_date
              and (pd.isna(win[c][1]) or row.action_date <= win[c][1] + pd.Timedelta(days=120))]
        if len(ok) == 1:
            return ok[0]
        pool = ok or cs
        lst = [c for c in pool if c in U.index]
        cur = [c for c in lst if U.at[c, "listing"] == "current"]
        if len(cur) == 1:
            return cur[0]
        pool = cur or lst or pool
        if len(pool) == 1:
            return pool[0]
        # same name, several registrants alive: the one that filed most recently
        lasts = [(win[c][1] if pd.notna(win[c][1]) else pd.Timestamp(0), c) for c in pool]
        return max(lasts)[1]

    M["cik"] = M.apply(pick, axis=1)
    amb = int((M.cik == -1).sum())
    n_stale = int((M.cik == -2).sum())
    log(f"  name matches outside the name's dates of use: {n_stale}")
    M = M[M.cik > 0].copy()
    # a prefix match counts only if the company also appears under its own exact
    # name within three years (it contracts in its own name; e.g. 'VERTEX
    # AEROSPACE' is not Vertex, Inc., the tax-software company)
    ex_dates = {c: np.sort(g.action_date.to_numpy()) for c, g in M[M.match == "exact"].groupby("cik")}

    def near_exact(c, d):
        a = ex_dates.get(c)
        if a is None or not len(a):
            return False
        i = np.searchsorted(a, np.datetime64(d))
        best = min(abs((a[j] - np.datetime64(d)).astype("timedelta64[D]").astype(int))
                   for j in (i - 1, i) if 0 <= j < len(a))
        return best <= 3 * 365
    pm = M.match == "prefix"
    okp = np.array([near_exact(c, d) for c, d in zip(M.cik[pm], M.action_date[pm])], bool)
    drop = M.index[pm][~okp]
    log(f"  prefix matches without an exact-name match within 3 years, dropped: {len(drop)}")
    M = M.drop(index=drop)

    # 4. identifier links (UEI/DUNS): a recipient, or a parent entity, whose
    #    identifier was seen in name-matched rows of company X is mapped to X
    #    for its other rows too, but only inside the dates the link was seen
    #    (first seen .. last seen + 365 days), so that a
    #    subsidiary's awards from before an acquisition are not handed to the
    #    later owner.
    def links(col):
        L = {}
        g = M.dropna(subset=[col]).groupby([col, "cik"]).action_date.agg(["min", "max", "size"])
        for (ident, cik), r in g.iterrows():
            ident = str(ident).strip()
            if not ident or ident.lower() == "nan":
                continue
            L.setdefault(ident, []).append((int(cik), r["min"], r["max"], int(r["size"])))
        return L
    Lr = {**links("recipient_uei"), **{("D" + k): v for k, v in links("recipient_duns").items()}}
    Lp = {**links("recipient_parent_uei"), **{("D" + k): v for k, v in links("recipient_parent_duns").items()}}
    R = T[T.cands.isna() & ~T.blocked].copy()

    def via(row):
        for L, keys in ((Lp, (row.recipient_parent_uei, "D" + str(row.recipient_parent_duns))),
                        (Lr, (row.recipient_uei, "D" + str(row.recipient_duns)))):
            for k in keys:
                k = str(k).strip()
                if not k or k in ("nan", "Dnan", "DNone", "None", "D"):
                    continue
                hits = [c for c, a, b, n in L.get(k, [])
                        if a <= row.action_date <= b + pd.Timedelta(days=365)]
                if len(set(hits)) == 1:
                    return hits[0]
        return -1
    R["cik"] = R.apply(via, axis=1) if len(R) else []
    R = R[R.cik > 0].copy()
    R["match"] = "id_link"
    M = pd.concat([M, R], ignore_index=True)
    win.update(alive_windows(sorted(set(R.cik) - set(win))))
    M["financial"] = M.cik.map(U.financial).fillna(False).astype(bool)
    # foreign private issuers (20-F/40-F, no 10-K): SEC counts ordinary shares while
    # Yahoo often prices an ADS, so market cap cannot be computed (as research/oplev)
    def foreign(cik):
        js = load_subs(int(cik)) or {}
        forms = set((js.get("filings") or {}).get("recent", {}).get("form", []))
        return bool(forms & {"20-F", "40-F", "20-F/A"}) and not (forms & {"10-K", "10-K/A"})
    fr = {c: foreign(c) for c in M.cik.unique()}
    M["foreign_filer"] = M.cik.map(fr)
    M["in_universe"] = M.cik.isin(pd.read_csv(DATA / "universe.csv").cik) & ~M.foreign_filer
    fw, lw = zip(*[win.get(int(c), (pd.NaT, pd.NaT)) for c in M.cik])
    M["sec_first"] = pd.to_datetime(list(fw))
    M["sec_last"] = pd.to_datetime(list(lw))
    M["alive"] = (M.sec_first <= M.action_date) & (M.action_date <= M.sec_last + pd.Timedelta(days=120))
    M["ticker"] = M.cik.map(U.ticker)
    M["listing"] = M.cik.map(U.listing)
    M["sic"] = M.cik.map(U.sic)
    M["company"] = M.cik.map(U.sub_name).fillna(M.cik.map(U["name"]))
    M["dod"] = M.awarding_agency_name.fillna("").str.strip().eq("Department of Defense")
    keep = ["contract_transaction_unique_key", "contract_award_unique_key", "award_id_piid",
            "modification_number", "transaction_number", "parent_award_id_piid", "action_date", "amount",
            "awarding_agency_code", "awarding_agency_name", "awarding_sub_agency_name", "awarding_office_name",
            "recipient_name", "recipient_uei", "recipient_duns", "recipient_parent_name", "recipient_parent_uei",
            "recipient_parent_duns", "pname", "pcore", "match", "cik", "company", "ticker", "listing", "sic",
            "financial", "in_universe", "alive", "sec_first", "sec_last", "dod", "self_parent", "last_modified_date",
            "action_type_code", "award_type_code", "transaction_description"]
    M = M[keep]
    M.to_parquet(CACHE / "mapped.parquet", index=False)
    P = (M.groupby(["pname", "pcore", "match", "cik", "company", "ticker"], dropna=False)
         .agg(n=("amount", "size"), total=("amount", "sum"), max_amt=("amount", "max"),
              first=("action_date", "min"), last=("action_date", "max")).reset_index()
         .sort_values("total", ascending=False))
    P.to_csv(DATA / "mapping_pairs.csv", index=False)
    log(f"mapped {len(M)} transactions ({int(M.in_universe.sum())} to non-financial candidates) "
        f"to {M.cik.nunique()} CIKs; ambiguous dropped {amb}; match types "
        f"{M.match.value_counts().to_dict()}")
    # review list: unmatched parent names with big totals (for the hand alias list)
    UM = T[T.cands.isna() & ~T.contract_transaction_unique_key.isin(R.contract_transaction_unique_key)].groupby("pname").agg(n=("amount", "size"), total=("amount", "sum"),
                                                max_amt=("amount", "max")).reset_index()
    UM = UM[UM.max_amt >= 1e6].sort_values("total", ascending=False)
    UM.to_csv(DATA / "unmatched_parents_review.csv", index=False)
    log(f"unmatched parent names with a transaction >= $1M: {len(UM)}")


if __name__ == "__main__":
    main()
