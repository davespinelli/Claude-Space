#!/usr/bin/env python3
"""Second view of the live quarter using Cal-Maine's new segment disclosure (Q4 FY2026 release, EX-99.1).

Parses the recast quarterly segment tables (fiscal 2024-2026: Conventional Shell Eggs, Specialty Shell Eggs,
Prepared Foods; sales, intersegment sales, COGS, SG&A, operating income) into data/calm_segments.csv, then
builds fiscal 2027 Q1 operating income segment by segment from the fourth quarter's cost per dozen:
  conventional / specialty: Q4 FY26 segment sales scaled by the model's volume and price change vs Q4;
                            Q4 FY26 segment cost per dozen, moved by k x (market price change)
  prepared foods, 'other' segment: Q4 FY26 operating income held flat
  unallocated corporate SG&A: fiscal 2026 Q1-Q3 average ($108.4M for the year less the $37.9M year-end Q4)
"""
import json, re, sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_sec import flat_text  # noqa: E402
from common import DATA, load_quarters  # noqa: E402

REL = "cache/sec/000156276226000078/exhibit991.htm"   # Q4 FY2026 earnings release


def parse_segments():
    t = flat_text(REL)
    rows = []
    for seg in ["Conventional Shell Eggs", "Specialty Shell Eggs", "Prepared Foods"]:
        i = t.find("SUMMARY SEGMENT INCOME " + seg)
        nxt = t.find("SUMMARY SEGMENT INCOME", i + 30)
        blk = t[i: nxt if nxt > 0 else i + 4000]
        for fy in [2026, 2025, 2024]:
            j = blk.find(f"Fiscal Year {fy} 1st Qtr")
            if j < 0:
                continue
            b = blk[j: j + 700] + " "
            def grab(label):
                m = re.search(re.escape(label) + r"\s+((?:\$?\(?[\d,—]+\)?\s+){4})", b)
                vals = []
                for tok in m.group(1).split():
                    tok = tok.replace("$", "")
                    neg = tok.startswith("(")
                    tok = tok.strip("()").replace(",", "")
                    v = 0.0 if tok in ("—", "") else float(tok)
                    vals.append(-v if neg else v)
                return vals
            ext, inter, tot = grab("Net sales - external customers"), grab("Intersegment sales"), grab("Total segment sales")
            cogs, sga, oi = grab("Segment COGS"), grab("Segment SG&A"), grab("Segment operating income")
            for q in range(4):
                rows.append(dict(segment=seg, fy=fy, q=q + 1, ext_sales=ext[q], interseg_sales=inter[q],
                                 seg_sales=tot[q], seg_cogs=cogs[q], seg_sga=sga[q], seg_oi=oi[q]))
    S = pd.DataFrame(rows).sort_values(["segment", "fy", "q"])
    S.to_csv(DATA / "calm_segments.csv", index=False)
    return S


def main():
    S = parse_segments()
    Q = load_quarters()
    live = json.load(open(DATA / "live_estimate.json"))["estimate"]
    q4 = Q[(Q.fy == 2026) & (Q.q == 4)].iloc[0]
    q1 = Q[(Q.fy == 2026) & (Q.q == 1)].iloc[0]
    g = lambda seg, fy, q: S[(S.segment == seg) & (S.fy == fy) & (S.q == q)].iloc[0]
    cv, sp, pf = g("Conventional Shell Eggs", 2026, 4), g("Specialty Shell Eggs", 2026, 4), g("Prepared Foods", 2026, 4)
    k = live["k"]
    B = pd.read_csv(DATA / "backtest.csv")
    dM = live["M"] - float(B.loc[B.label == "FY26 Q4", "M"].iloc[0])  # market price change vs Q4 FY26
    out = {}
    # conventional
    cv_sales = cv.seg_sales * (live["conv_doz"] / q4.conv_doz) * (live["conv_price"] / q4.conv_price)
    cv_cost_doz = (cv.seg_cogs + cv.seg_sga) / q4.conv_doz + k * dM
    out["conventional_oi"] = cv_sales - cv_cost_doz * live["conv_doz"]
    sp_sales = sp.seg_sales * (live["spec_doz"] / q4.spec_doz_all) * (live["spec_price"] / q4.spec_price)
    sp_cost_doz = (sp.seg_cogs + sp.seg_sga) / q4.spec_doz_all + k * dM
    out["specialty_oi"] = sp_sales - sp_cost_doz * live["spec_doz"]
    out["prepared_oi"] = pf.seg_oi
    out["other_segment_oi"] = -7394.0          # Q4 FY26 'Other - segment income (loss)', held flat
    seg_q1_fy26 = sum(g(s, 2026, 1).seg_oi for s in ["Conventional Shell Eggs", "Specialty Shell Eggs", "Prepared Foods"])
    out["corporate_and_other_q1fy26"] = q1.rel_op_income - seg_q1_fy26 - 7488.0  # ex involuntary-conversion gain
    # Q1 FY26 remainder includes a positive 'other' segment (egg products at high prices); use corporate only:
    # FY26 unallocated corporate SG&A was $108.4M with $37.9M in Q4 -> Q1-Q3 average $23.5M
    out["corporate_sga"] = -(108353.0 - 37897.0) / 3
    oi = out["conventional_oi"] + out["specialty_oi"] + out["prepared_oi"] + out["other_segment_oi"] + out["corporate_sga"]
    pretax = oi + live["other_income"]
    ni = pretax * (1 - live["tax_rate"]) - live["nci"]
    out.update(op_income=oi, pretax=pretax, ni=ni, eps=ni / live["shares"],
               conv_sales=cv_sales, spec_sales=sp_sales, conv_cost_per_doz=cv_cost_doz, spec_cost_per_doz=sp_cost_doz)
    json.dump(out, open(DATA / "segment_check.json", "w"), indent=1)
    for kk, v in out.items():
        print(f"{kk:28s} {v:12.3f}")


if __name__ == "__main__":
    main()
