"""Print the numbers RESULTS.md quotes, straight from results.json (so the write-up can be checked)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec

R = json.loads((sec.ROOT / "results.json").read_text())


def pct(x):
    return "n/a" if x is None else f"{100 * x:+.2f}%"


def line(label, s):
    if not s or s.get("n", 0) < 3:
        return f"| {label} | {s.get('n', 0) if s else 0} | n/a | n/a | n/a | n/a | n/a |"
    h1, h2 = s.get("half1", {}), s.get("half2", {})
    return (f"| {label} | {s['n']} | {pct(s['mean'])} | {s['t']:.2f} | {pct(s['net_in_trade_direction'])} | "
            f"{s['t_net']:.2f} | {pct(h1.get('mean'))} / {pct(h2.get('mean'))} |")


print("| Cut | Events | Mean AR (+1..+60) | t (clustered) | After 0.2% cost, trade direction | t after cost | First half / second half |")
print("|---|---|---|---|---|---|---|")
print(line("Primary", R["primary"]))
for k, v in R["robustness"].items():
    print(line(k, v))
print(line("Secondary: under $2B", R["secondary_under_2b"]))
print(line("(info) $2B and over", R["secondary_2b_plus"]))
print(line("Secondary: top-20% adoptions", R["secondary_adoptions_top20"]))
print(line("(info) adoptions, per-quarter cutoff", R["secondary_adoptions_top20_perquarter_cutoff"]))
print(line("(info) adoptions, IWM/SPY", R["secondary_adoptions_top20_iwm_spy"]))
print()
print("bounds primary", json.dumps(R["primary_bounds"], default=str)[:800])
print("bounds adoptions", json.dumps(R["secondary_adoptions_top20_bounds"], default=str)[:800])
print("counts", json.dumps(R["counts"], default=str))
print("halves", {k: (R["primary"][k]["from"], R["primary"][k]["to"], R["primary"][k]["n"]) for k in ("half1", "half2")})
print("verdict", R["primary"]["verdict_yes"], "adoption verdict", R["secondary_adoptions_top20"]["verdict_yes"],
      "under2b", R["secondary_under_2b"]["verdict_yes"])
print("adoption cutoff", R["adoption_cutoff_pct_out"], R["adoption_status"], R["benchmark"])
