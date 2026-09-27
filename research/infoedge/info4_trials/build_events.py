"""Step 4: turn trial-level registry changes into company events.

For each change in data/trial_changes.csv:
  - sponsor at the time = the lead sponsor named in that version, mapped to a CIK
    (data/sponsor_map_kept.csv; names not in the map are normalised and matched again);
  - public date = posting date of the version (PREREG deviation 1);
  - 8-K / 6-K screen: none filed from 5 trading days before the history (version) date
    through the posting date (primary, deviation 2); the literal window (5 trading days
    before the version date through the version date) is kept as a flag.
Changes are then collapsed to one event per company per posting date.
Output: data/events.csv (company events), data/changes_mapped.csv (trial level).
"""
from pathlib import Path
import numpy as np
import pandas as pd
from map_sponsors import norm

HERE = Path(__file__).resolve().parent


def trading_days():
    px = pd.read_pickle(HERE / "cache/prices_daily.pkl")[["date", "ticker"]]
    return pd.DatetimeIndex(sorted(px.loc[px.ticker == "SPY", "date"].unique()))


def main():
    C = pd.read_csv(HERE / "data/trial_changes.csv")
    mp = pd.read_csv(HERE / "data/sponsor_map_kept.csv")
    name2cik = dict(zip(mp.lead_sponsor, mp.cik))
    name_first = dict(zip(mp.lead_sponsor, mp.name_first_seen))
    norm2cik = {}
    for n, c in zip(mp.lead_sponsor.map(norm), mp.cik):
        norm2cik.setdefault(n, set()).add(c)
    cur = pd.read_csv(HERE / "data/trials_universe.csv", dtype=str)
    cur_cik = dict(zip(cur.nct, cur.lead_sponsor.map(name2cik)))

    def to_cik(row):
        s = row.lead_sponsor
        if isinstance(s, str):
            if s in name2cik: return name2cik[s], "version_name"
            n = norm(s)
            if n in norm2cik and len(norm2cik[n]) == 1: return next(iter(norm2cik[n])), "version_norm"
            return np.nan, "version_name_unmapped"
        return cur_cik.get(row.nct, np.nan), "current_name"

    res = C.apply(to_cik, axis=1, result_type="expand"); C["cik"], C["map_via"] = res[0], res[1]
    print("changes:", len(C), "| sponsor mapping:", C.map_via.value_counts().to_dict())
    C = C.dropna(subset=["cik"]).copy(); C["cik"] = C.cik.astype(int)
    # Point in time: a private sponsor that later reverse-merged into a listed shell must not be
    # attributed to the shell's stock before the merger. The sponsor's name must have been used by
    # that SEC registrant (a periodic report under a matching name) no more than 120 days after
    # the posting date.
    first = C.lead_sponsor.map(name_first)
    late = pd.to_datetime(first, errors="coerce") > pd.to_datetime(C.post_date) + pd.Timedelta(days=120)
    print("changes dropped because the sponsor name was not yet used by the registrant:", int(late.sum()))
    C = C[~late].copy()

    T = trading_days()
    def tpos_on_or_before(d):
        return T.searchsorted(pd.Timestamp(d), side="right") - 1
    C["qc_pos"] = C.qc_date.map(tpos_on_or_before)
    C["post_pos"] = C.post_date.map(tpos_on_or_before)

    ek = pd.read_csv(HERE / "cache/edgar_8k_dates.csv")
    ek = ek[ek.cik.isin(set(C.cik))]
    ek["pos"] = ek.date.map(tpos_on_or_before)
    by_cik = {c: np.sort(g.pos.values) for c, g in ek.groupby("cik")}

    def any_in(c, lo, hi):
        a = by_cik.get(c)
        if a is None: return False
        i = np.searchsorted(a, lo, side="left")
        return i < len(a) and a[i] <= hi

    C["k8_primary"] = [any_in(c, q - 5, p) for c, q, p in zip(C.cik, C.qc_pos, C.post_pos)]
    C["k8_literal"] = [any_in(c, q - 5, q) for c, q in zip(C.cik, C.qc_pos)]
    C["phase23"] = C.phases.fillna("").str.contains("PHASE2|PHASE3")
    C.to_csv(HERE / "data/changes_mapped.csv", index=False)

    ev = (C.groupby(["cik", "post_date"])
            .agg(n_changes=("nct", "size"), n_trials=("nct", "nunique"),
                 types=("type", lambda x: "|".join(sorted(set(x)))),
                 any_phase23=("phase23", "any"), all_phase23=("phase23", "all"),
                 k8_primary=("k8_primary", "any"), k8_literal=("k8_literal", "any"),
                 qc_date=("qc_date", "min"), ncts=("nct", lambda x: "|".join(sorted(set(x)))))
            .reset_index())
    ev.to_csv(HERE / "data/events_all.csv", index=False)
    print("company-date events (before 8-K screen):", len(ev), "| with an 8-K/6-K in window:", int(ev.k8_primary.sum()))


if __name__ == "__main__":
    main()
