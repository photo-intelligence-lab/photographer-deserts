# /// script
# dependencies = ["pandas", "tabulate"]
# ///
"""Print the ranked tables used in findings.md (reads the CSVs written by build.py)."""
from pathlib import Path
import pandas as pd

D = Path(__file__).parent
c = pd.read_csv(D / "county_photographers_per100k.csv", dtype={"fips": str, "cbsa": str})
m = pd.read_csv(D / "cbsa_photographers_per100k.csv", dtype={"cbsa": str})
s = pd.read_csv(D / "state_photographers_per100k.csv", dtype={"st": str})
pd.set_option("display.width", 250)
fmt = lambda d: d.to_markdown(index=False, floatfmt=".1f")
out = []
def sec(t, d): out.append(f"\n### {t}\n\n{fmt(d)}\n")

cols = ["county", "state", "pop2024", "cbp23_54192", "nes24_54192", "total_54192", "per100k", "per100k_upper", "per100k_2023matched", "cbsa_type"]
for floor in (50_000, 100_000, 250_000, 1_000_000):
    x = c[(c.pop2024 >= floor) & c.per100k.notna()].sort_values("per100k")
    sec(f"Lowest 15 counties, pop >= {floor:,} (n={len(x)})", x[cols].head(15))
    if floor in (250_000, 1_000_000):
        sec(f"Highest 10 counties, pop >= {floor:,}", x[cols].tail(10).iloc[::-1])
z = c[(c.cbp23_54192 == 0) & (c.nes24_54192 == 0) & (c.nes24_flag != "S")].sort_values("pop2024", ascending=False)
sec(f"Counties with no published employer AND no published nonemployer photography cell (n={len(z)}, pop {z.pop2024.sum():,}) - top 30 by pop",
    z[["fips", "county", "state", "pop2024", "cbsa_name", "cbsa_type", "nes23_54192"]].head(30))
zs = z.groupby("state").agg(counties=("fips", "count"), pop=("pop2024", "sum")).sort_values("counties", ascending=False)
sec("Zero-published counties by state", zs.reset_index().head(15))
z.to_csv(D / "zero_published_counties.csv", index=False)
sec("Counties suppressed (NES 'S')", c[c.nes24_flag == "S"][["fips", "county", "state", "pop2024", "cbp23_54192"]])
st = s[["rank_low_to_high", "state", "pop2024", "cbp23_54192", "nes24_54192", "total_54192", "per100k", "portrait_employer_per100k", "nonemp_avg_receipts_usd"]]
sec("States, lowest to highest", st)
big = m[(m.cbsa_type == "Metropolitan Statistical Area") & (m.pop2024 >= 1_000_000)].sort_values("per100k")
mc = ["cbsa_name", "pop2024", "cbp23_54192", "nes24_54192", "total_54192", "per100k", "portrait_employer_per100k", "oews25_photographers_emp", "oews25_per1000jobs", "oews25_annual_median_wage"]
sec(f"Metros >= 1M, lowest to highest (n={len(big)})", big[mc])
mid = m[(m.cbsa_type == "Metropolitan Statistical Area") & (m.pop2024 >= 250_000)].sort_values("per100k")
sec("Metros >= 250k: lowest 15", mid[mc].head(15))
sec("Metros >= 250k: highest 10", mid[mc].tail(10).iloc[::-1])
# share of population by per100k band
c2 = c[c.per100k.notna()]
bands = pd.cut(c2.per100k, [-0.1, 0, 25, 50, 75, 100, 1e9], labels=["0 published", "<25", "25-50", "50-75", "75-100", "100+"])
sec("Population by county supply band (per 100k)", c2.groupby(bands, observed=False).agg(counties=("fips", "count"), pop=("pop2024", "sum")).reset_index())
(D / "tables.md").write_text("".join(out))
print("".join(out))
