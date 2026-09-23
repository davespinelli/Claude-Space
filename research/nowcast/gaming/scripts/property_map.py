#!/usr/bin/env python3
"""Map state regulators' reporting units (data/state_<st>.csv.gz unit_id) to the properties of the
ownership timeline (data/ownership.csv.gz).

Property-level states: ownership.csv.gz carries `property_id`, which scripts/ownership.py set equal
to the state files' unit_id for every casino a listed company held; the mapping is that id, checked
here against the unit list (every unit with a listed owner must map; units of private/tribal casinos
stay unmapped).  MANUAL holds the few fixes found on review.
Region-level states (MS, CO, NV): the ownership `region` column (Colorado town, Mississippi
"County|Region", Nevada NGCB area) is mapped to the regulator's unit by REGION_UNITS.

Output data/property_map.csv.gz: state, unit_id, property, method.  --review prints the mapping.
"""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# (state, unit_id) -> ownership property name, for units whose property_id did not match
MANUAL: dict[tuple[str, str], str] = {}

REGION_UNITS = {
    "CO": {"Black Hawk": "CO_BLACK_HAWK", "Central City": "CO_CENTRAL_CITY", "Cripple Creek": "CO_CRIPPLE_CREEK"},
    "MS": {"Northern River": "MS_NORTHERN", "Central River": "MS_CENTRAL", "Coastal": "MS_COASTAL"},
    "NV": {"Las Vegas Strip": "NV_CLARK_COUNTY_LAS_VEGAS_STRIP_AREA",
           "Boulder Strip": "NV_CLARK_COUNTY_BOULDER_STRIP_AREA",
           "Downtown": "NV_CLARK_COUNTY_DOWNTOWN_LAS_VEGAS_AREA",
           "North Las Vegas": "NV_CLARK_COUNTY_NORTH_LAS_VEGAS_AREA",
           "Balance of Clark County": "NV_CLARK_COUNTY_BALANCE_OF_COUNTY",
           "Laughlin": "NV_CLARK_COUNTY_LAUGHLIN_AREA",
           "Mesquite": "NV_CLARK_COUNTY_MESQUITE_AREA",
           "Reno": "NV_WASHOE_COUNTY_RENO_AREA",
           "Sparks": "NV_WASHOE_COUNTY_SPARKS_AREA",
           "North Lake Tahoe": "NV_WASHOE_COUNTY_NORTH_SHORE_LAKE_TAHOE_AREA",
           "Balance of Washoe": "NV_WASHOE_COUNTY_BALANCE_OF_COUNTY",
           "South Lake Tahoe": "NV_DOUGLAS_COUNTY_SOUTH_SHORE_LAKE_TAHOE_AREA",
           "Carson Valley Area": "NV_CARSON_VALLEY_AREA",
           "Elko County": "NV_ELKO_COUNTY_BALANCE_OF_COUNTY",      # Jackpot (Cactus Petes, Horseshu)
           "Wendover": "NV_ELKO_COUNTY_WENDOVER_AREA",
           "Churchill County": "NV_CHURCHILL_COUNTY",
           "Nye County": "NV_NYE_COUNTY",
           "Lyon County": "NV_LYON_COUNTY"},
}


def build(review=False) -> pd.DataFrame:
    own = pd.read_csv(DATA / "ownership.csv.gz", dtype=str).fillna("")
    frames = [pd.read_csv(p, dtype=str) for p in sorted(DATA.glob("state_??.csv.gz"))]
    st = pd.concat(frames, ignore_index=True)
    st = st[st["unit_level"] != "state_total"]
    units = st.groupby(["state", "unit_id", "unit_level"])["unit"].agg(lambda s: " | ".join(sorted(set(s)))[:90]).reset_index()
    uid = set(units["unit_id"])
    rows = []
    # property-level
    for _, o in own.drop_duplicates(["state", "property", "property_id"]).iterrows():
        if o["state"] in REGION_UNITS:
            continue
        if o["property_id"] in uid:
            rows.append(dict(state=o["state"], unit_id=o["property_id"], property=o["property"], method="property_id"))
    for (s, u), p in MANUAL.items():
        rows.append(dict(state=s, unit_id=u, property=p, method="manual"))
    # region-level
    for _, o in own.drop_duplicates(["state", "property", "region"]).iterrows():
        if o["state"] not in REGION_UNITS or not o["region"]:
            continue
        lab = o["region"].split("|")[-1] if o["state"] == "MS" else o["region"]
        u = REGION_UNITS[o["state"]].get(lab)
        if u:
            rows.append(dict(state=o["state"], unit_id=u, property=o["property"], method="region"))
        elif review:
            print("UNMAPPED REGION", o["state"], o["property"], o["region"])
    out = pd.DataFrame(rows).drop_duplicates(["state", "unit_id", "property"])
    out.to_csv(DATA / "property_map.csv.gz", index=False)
    if review:
        m = units.merge(out, on=["state", "unit_id"], how="left")
        for _, r in m[m["unit_level"].isin(["property", "operator"])].iterrows():
            print(f"{r['state']} {r['unit_id']:<36} {r['unit'][:55]:<55} -> {r['property'] if isinstance(r['property'], str) else '(no listed owner)'}")
        # ownership property_ids in property-level states that match no unit
        miss = own[~own["state"].isin(REGION_UNITS) & (own["property_id"] != "") & ~own["property_id"].isin(uid)]
        print("ownership ids without a state unit:", sorted(set(miss["state"] + ":" + miss["property_id"])))
        noid = own[~own["state"].isin(REGION_UNITS) & (own["property_id"] == "")]
        print("ownership rows without property_id:", sorted(set(noid["company"] + ":" + noid["state"] + ":" + noid["property"])))
    return out


if __name__ == "__main__":
    build("--review" in sys.argv)
