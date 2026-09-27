"""Draw 50 random quiet changes of priced sponsors (registry sponsor name on that version vs the
SEC registrant and ticker used) for a hand check of mapping precision where it matters.
Uses no returns. Output: data/event_spotcheck.csv (the hand verdict is added in column 'correct')."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent


def main():
    C = pd.read_csv(HERE / "data/changes_mapped.csv")
    comp = pd.read_csv(HERE / "data/sponsor_companies_priced.csv").set_index("cik")
    C = C[(~C.k8_primary) & C.cik.isin(comp.index[comp.ticker.notna()])]
    ev = C.drop_duplicates(["cik", "post_date"]).sample(50, random_state=4)
    out = pd.DataFrame({"post_date": ev.post_date, "nct": ev.nct, "type": ev.type,
                        "sponsor_in_version": ev.lead_sponsor,
                        "registrant_now": ev.cik.map(comp.name_now), "ticker": ev.cik.map(comp.ticker)})
    out.to_csv(HERE / "data/event_spotcheck.csv", index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 48)
    print(out.reset_index(drop=True).to_string())


if __name__ == "__main__":
    main()
