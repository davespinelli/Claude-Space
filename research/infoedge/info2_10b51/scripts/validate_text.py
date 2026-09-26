"""Validate the text parser on tagged filings (PREREG D3): per filing, does the parser find an early
termination by a CEO / CFO / director, compared with the XBRL-based answer?"""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec
import parse_text as p

ev, st = p.run(groups=("valid_pos", "valid_neg"))
a = pd.read_csv(sec.ROOT / "data" / "arrangements.csv.gz", low_memory=False)
a["prim"] = (a.is_trm == True) & (a.trm_class == "early") & a.insider_target & a.person_ok & ~a.trm_stale & ~a.purchase_only
truth = a.groupby("adsh").prim.any()
if len(ev):
    ev["prim"] = (ev.trm_class == "early") & (ev.is_ceo | ev.is_cfo | ev.is_dir) & ~ev.purchase_only
    pred = ev.groupby("adsh").prim.any()
    anyt = ev.groupby("adsh").size() > 0
else:
    pred = pd.Series(dtype=bool); anyt = pd.Series(dtype=bool)
st = st[st.fetched]
st["truth"] = st.adsh.map(truth).fillna(False).astype(bool)
st["pred"] = st.adsh.map(pred).fillna(False).astype(bool)
st["pred_any_trm"] = st.adsh.map(anyt).fillna(False).astype(bool)
st["truth_any_trm"] = st.adsh.isin(set(a.adsh[(a.is_trm == True) & a.person_ok]))
tp = int((st.pred & st.truth).sum()); fp = int((st.pred & ~st.truth).sum()); fn = int((~st.pred & st.truth).sum())
res = {"filings": len(st), "truth_pos": int(st.truth.sum()), "pred_pos": int(st.pred.sum()), "tp": tp, "fp": fp, "fn": fn,
       "precision": tp / max(1, tp + fp), "recall": tp / max(1, tp + fn),
       "any_trm_precision": float((st.pred_any_trm & st.truth_any_trm).sum() / max(1, st.pred_any_trm.sum())),
       "any_trm_recall": float((st.pred_any_trm & st.truth_any_trm).sum() / max(1, st.truth_any_trm.sum()))}
st.to_csv(sec.ROOT / "data" / "text_validation.csv", index=False)
ev.to_csv(sec.CACHE / "text_validation_events.csv", index=False)
print(res)
