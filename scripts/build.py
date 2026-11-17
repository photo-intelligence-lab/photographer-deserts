# /// script
# dependencies = ["pandas", "openpyxl", "scipy"]
# ///
"""Photographer deserts: build county / CBSA / state tables from official Census files.

Inputs (all in raw/, downloaded unmodified from www2.census.gov / bls.gov, see findings.md):
  cbp23co.txt          County Business Patterns 2023, county  (employer establishments)
  cbp23msa.txt         CBP 2023, metro/micro (cross-check only)
  nonemp24co.txt       Nonemployer Statistics 2024, county
  nonemp24msa.txt      NES 2024, metro/micro (cross-check only)
  nonemp23co.txt       NES 2023, county (robustness: matched-year run)
  co-est2025-alldata.csv   Population Estimates Vintage 2025, counties
  cbsa-est2025-alldata.csv PEP Vintage 2025, CBSAs + county components
  oews25/oesm25ma/MSA_M2025_dl.xlsx  BLS OEWS May 2025, metro areas (cross-check)

Supply measure (primary): NAICS 54192 Photographic Services
  = CBP 2023 employer establishments (54192/ = 541921 portrait + 541922 commercial)
  + NES 2024 nonemployer establishments (NES publishes 54192 only, no 6-digit split).
Portrait-only (541921) is available for employers only and is reported as a separate column.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

D = Path(__file__).parent
R = D / "raw"
OUT = D
log = {}

# ---------- population (PEP V2025) ----------
pep = pd.read_csv(R / "co-est2025-alldata.csv", encoding="latin-1", dtype={"STATE": str, "COUNTY": str})
pep = pep[pep.SUMLEV == 50].copy()
pep["fips"] = pep.STATE + pep.COUNTY
pep = pep.rename(columns={"STNAME": "state", "CTYNAME": "county", "POPESTIMATE2023": "pop2023",
                          "POPESTIMATE2024": "pop2024", "POPESTIMATE2025": "pop2025"})
pep = pep[["fips", "county", "state", "pop2023", "pop2024", "pop2025"]]
log["pep_counties"] = len(pep)

# ---------- CBP 2023 county ----------
cbp = pd.read_csv(R / "cbp23co.txt", dtype=str)
cbp["fips"] = cbp.fipstate + cbp.fipscty
cbp["est"] = cbp.est.astype(int)
cbp_w = cbp[cbp.naics.isin(["54192/", "541921", "541922"])].pivot_table(
    index=["fips", "fipstate", "fipscty"], columns="naics", values="est", aggfunc="sum").reset_index()
cbp_w = cbp_w.rename(columns={"54192/": "cbp23_54192", "541921": "cbp23_541921", "541922": "cbp23_541922"})
for c in ["cbp23_54192", "cbp23_541921", "cbp23_541922"]:
    cbp_w[c] = cbp_w[c].fillna(0).astype(int)
# consistency: 54192 should equal 541921+541922
bad = cbp_w[cbp_w.cbp23_54192 != cbp_w.cbp23_541921 + cbp_w.cbp23_541922]
log["cbp_54192_ne_sum_rows"] = len(bad)
cbp_state999 = cbp_w[cbp_w.fipscty == "999"]
log["cbp_statewide_999_rows_54192"] = int(cbp_state999.cbp23_54192.sum())

# ---------- NES county ----------
def load_nes(path, tag):
    n = pd.read_csv(path, dtype=str)
    n = n[n.NAICS == "54192"].copy()
    n["fips"] = n.ST + n.CTY
    n[f"{tag}_54192"] = n.ESTAB.astype(int)
    n[f"{tag}_flag"] = n.ESTAB_F.fillna("")
    n.loc[n[f"{tag}_flag"] == "S", f"{tag}_54192"] = np.nan  # S = withheld, does not meet publication standards
    n[f"{tag}_rcptot_k"] = pd.to_numeric(n.RCPTOT, errors="coerce")
    return n[["fips", f"{tag}_54192", f"{tag}_flag", f"{tag}_rcptot_k"]]

nes24 = load_nes(R / "nonemp24co.txt", "nes24")
nes23 = load_nes(R / "nonemp23co.txt", "nes23")
log["nes24_rows_54192"] = len(nes24)
log["nes24_S_flags"] = int((nes24.nes24_flag == "S").sum())
log["nes23_S_flags"] = int((nes23.nes23_flag == "S").sum())

# ---------- join ----------
df = pep.merge(cbp_w[["fips", "cbp23_54192", "cbp23_541921", "cbp23_541922"]], on="fips", how="left") \
        .merge(nes24, on="fips", how="left").merge(nes23[["fips", "nes23_54192", "nes23_flag"]], on="fips", how="left")
# unmatched source geographies (not in PEP county list)
cbp_counties = set(cbp_w.loc[cbp_w.fipscty != "999", "fips"])
nes_counties = set(nes24.fips[~nes24.fips.str.endswith("999")])
log["cbp_fips_not_in_pep"] = sorted(cbp_counties - set(pep.fips))
log["nes24_fips_not_in_pep"] = sorted(nes_counties - set(pep.fips))
log["nes24_statewide_999_rows"] = int(nes24.fips.str.endswith("999").sum())

for c in ["cbp23_54192", "cbp23_541921", "cbp23_541922"]:
    df[c] = df[c].fillna(0).astype(int)  # CBP publishes only nonzero cells -> absent = 0
for t in ["nes24", "nes23"]:
    absent = df[f"{t}_flag"].isna()
    df.loc[absent, f"{t}_54192"] = 0       # absent from NES file = no published nonemployers in 54192
    df.loc[absent, f"{t}_flag"] = "absent(0)"
    df.loc[df[f"{t}_flag"] == "", f"{t}_flag"] = "published"

df["nes24_suppressed"] = df.nes24_flag == "S"
df["total_54192"] = df.cbp23_54192 + df.nes24_54192.fillna(0)  # lower bound if suppressed
df["per100k"] = df.total_54192 / df.pop2024 * 1e5
df["per100k"] = df["per100k"].where(~df.nes24_suppressed)  # don't rank suppressed counties
df["total_lower_bound_if_suppressed"] = np.where(df.nes24_suppressed, df.cbp23_54192, np.nan)
# Since RY2017 CBP drops any cell with <3 establishments; NES county cells are likewise never published
# below 3 (min published ESTAB = 3). So an absent cell means 0, 1 or 2. Upper bound adds 2 per absent source.
df["cbp_absent"] = df.cbp23_54192 == 0
df["nes_absent"] = df.nes24_flag == "absent(0)"
df["total_upper"] = df.total_54192 + 2 * df.cbp_absent + 2 * df.nes_absent
df["per100k_upper"] = (df.total_upper / df.pop2024 * 1e5).where(~df.nes24_suppressed)
df["portrait_employer_per100k"] = df.cbp23_541921 / df.pop2024 * 1e5
df["nonemp_per100k"] = df.nes24_54192 / df.pop2024 * 1e5
df["residents_per_business"] = (df.pop2024 / df.total_54192).where(df.total_54192 > 0)
# matched-year robustness (CBP 2023 + NES 2023 + PEP July 2023)
df["total_2023matched"] = df.cbp23_54192 + df.nes23_54192.fillna(0)
df["per100k_2023matched"] = (df.total_2023matched / df.pop2023 * 1e5).where(df.nes23_flag != "S")

# ---------- CBSA membership ----------
cb = pd.read_csv(R / "cbsa-est2025-alldata.csv", encoding="latin-1", dtype={"CBSA": str, "MDIV": str, "STCOU": str})
cbsa_tot = cb[cb.LSAD.isin(["Metropolitan Statistical Area", "Micropolitan Statistical Area"])][
    ["CBSA", "NAME", "LSAD", "POPESTIMATE2024", "POPESTIMATE2025"]]
members = cb[(cb.LSAD == "County or equivalent")][["CBSA", "STCOU"]].drop_duplicates()
df = df.merge(members.rename(columns={"STCOU": "fips", "CBSA": "cbsa"}), on="fips", how="left")
df = df.merge(cbsa_tot[["CBSA", "NAME", "LSAD"]].rename(columns={"CBSA": "cbsa", "NAME": "cbsa_name", "LSAD": "cbsa_type"}),
              on="cbsa", how="left")
df["cbsa_type"] = df.cbsa_type.fillna("Outside CBSA (rural)")
log["counties_total"] = len(df)
log["counties_in_cbsa"] = int(df.cbsa.notna().sum())

# ---------- county CSV ----------
cols = ["fips", "county", "state", "pop2024", "pop2025", "cbsa", "cbsa_name", "cbsa_type",
        "cbp23_541921", "cbp23_541922", "cbp23_54192", "nes24_54192", "nes24_flag", "total_54192",
        "per100k", "total_upper", "per100k_upper", "residents_per_business", "portrait_employer_per100k", "nonemp_per100k",
        "nes24_rcptot_k", "nes23_54192", "nes23_flag", "total_2023matched", "per100k_2023matched"]
county = df[cols].sort_values("fips")
county.to_csv(OUT / "county_photographers_per100k.csv", index=False, float_format="%.2f")

# ---------- CBSA rollup (sum of member counties; consistent with PEP V2025 delineation) ----------
g = df[df.cbsa.notna()].groupby(["cbsa", "cbsa_name", "cbsa_type"]).agg(
    counties=("fips", "count"), pop2024=("pop2024", "sum"), cbp23_541921=("cbp23_541921", "sum"),
    cbp23_54192=("cbp23_54192", "sum"), nes24_54192=("nes24_54192", "sum"),
    suppressed_counties=("nes24_suppressed", "sum")).reset_index()
g["total_54192"] = g.cbp23_54192 + g.nes24_54192
g["per100k"] = g.total_54192 / g.pop2024 * 1e5
g["portrait_employer_per100k"] = g.cbp23_541921 / g.pop2024 * 1e5
# cross-check against Census's own metro files
cm = pd.read_csv(R / "cbp23msa.txt", dtype=str)
cm = cm[cm.naics == "54192/"][["msa", "est"]].rename(columns={"msa": "cbsa", "est": "cbp23msa_file"})
nm = pd.read_csv(R / "nonemp24msa.txt", dtype=str)
nm = nm[nm.NAICS == "54192"][["MSA", "ESTAB", "ESTAB_F"]].rename(columns={"MSA": "cbsa", "ESTAB": "nes24msa_file", "ESTAB_F": "nes24msa_flag"})
g = g.merge(cm, on="cbsa", how="left").merge(nm, on="cbsa", how="left")
for c in ["cbp23msa_file", "nes24msa_file"]:
    g[c] = pd.to_numeric(g[c])
# BLS OEWS May 2025, SOC 27-4021 Photographers (wage-and-salary employees only)
try:
    oe = pd.read_excel(R / "oews25/oesm25ma/MSA_M2025_dl.xlsx", dtype=str)
    oe.columns = [c.upper() for c in oe.columns]
    oe = oe[oe.OCC_CODE == "27-4021"][["AREA", "AREA_TITLE", "TOT_EMP", "JOBS_1000", "LOC_QUOTIENT", "A_MEDIAN", "H_MEDIAN"]]
    oe = oe.rename(columns={"AREA": "cbsa", "TOT_EMP": "oews25_photographers_emp", "JOBS_1000": "oews25_per1000jobs",
                            "LOC_QUOTIENT": "oews25_lq", "A_MEDIAN": "oews25_annual_median_wage", "H_MEDIAN": "oews25_hourly_median_wage"})
    g = g.merge(oe.drop(columns=["AREA_TITLE"]), on="cbsa", how="left")
    log["oews_photographer_rows"] = len(oe)
except Exception as e:  # noqa
    log["oews_error"] = repr(e)
g.sort_values("pop2024", ascending=False).to_csv(OUT / "cbsa_photographers_per100k.csv", index=False, float_format="%.2f")

# ---------- state (county sums incl. statewide-unallocated 999 rows) ----------
st_cbp = cbp_w.groupby("fipstate").cbp23_54192.sum()
st_cbpp = cbp_w.groupby("fipstate").cbp23_541921.sum()
ns = pd.read_csv(R / "nonemp24st.txt", dtype=str)
ns = ns[(ns.NAICS == "54192") & (ns.LFO == "-")].set_index("ST")
stp = pep.assign(st=pep.fips.str[:2]).groupby(["st", "state"]).pop2024.sum().reset_index()
stp["cbp23_54192"] = stp.st.map(st_cbp).fillna(0).astype(int)
stp["cbp23_541921"] = stp.st.map(st_cbpp).fillna(0).astype(int)
stp["nes24_54192"] = stp.st.map(ns.ESTAB.astype(int))
stp["nes24_flag"] = stp.st.map(ns.ESTAB_F)
stp["nes24_rcptot_k"] = stp.st.map(pd.to_numeric(ns.RCPTOT))
stp["total_54192"] = stp.cbp23_54192 + stp.nes24_54192
stp["per100k"] = stp.total_54192 / stp.pop2024 * 1e5
stp["portrait_employer_per100k"] = stp.cbp23_541921 / stp.pop2024 * 1e5
stp["nonemp_avg_receipts_usd"] = stp.nes24_rcptot_k * 1000 / stp.nes24_54192
stp = stp.sort_values("per100k")
stp["rank_low_to_high"] = range(1, len(stp) + 1)
stp.to_csv(OUT / "state_photographers_per100k.csv", index=False, float_format="%.2f")

# ---------- summary stats ----------
ok = df[~df.nes24_suppressed]
us_pop = df.pop2024.sum()
nat_cbp = int(cbp_w.cbp23_54192.sum()); nat_nes = int(stp.nes24_54192.sum())
nus = pd.read_csv(R / "nonemp24st.txt", dtype=str)
s = {}
s["us_pop2024"] = int(us_pop)
s["us_cbp23_54192"] = nat_cbp
s["us_cbp23_541921"] = int(cbp_w.cbp23_541921.sum())
s["us_cbp23_541922"] = int(cbp_w.cbp23_541922.sum())
s["us_nes24_54192_sum_states"] = nat_nes
s["us_nes24_rcptot_k_sum_states"] = float(stp.nes24_rcptot_k.sum())
s["us_rate_per100k"] = (nat_cbp + nat_nes) / us_pop * 1e5
s["county_median_per100k"] = float(ok.per100k.median())
s["county_p10_per100k"] = float(ok.per100k.quantile(.10))
s["county_p90_per100k"] = float(ok.per100k.quantile(.90))
w = ok.sort_values("per100k"); cw = w.pop2024.cumsum() / w.pop2024.sum()
s["pop_weighted_median_per100k"] = float(w.per100k[cw >= .5].iloc[0])
s["counties_ranked"] = int(ok.per100k.notna().sum())
s["counties_suppressed"] = int(df.nes24_suppressed.sum())
z = df[(df.cbp23_54192 == 0) & (df.nes24_54192 == 0) & (~df.nes24_suppressed)]
s["zero_both_counties"] = len(z); s["zero_both_pop2024"] = int(z.pop2024.sum())
z23 = df[(df.cbp23_54192 == 0) & (df.nes23_54192 == 0) & (df.nes23_flag != "S")]
s["zero_both_counties_2023matched"] = len(z23)
s["counties_no_employer_studio"] = int((df.cbp23_54192 == 0).sum())
s["pop_no_employer_studio"] = int(df.loc[df.cbp23_54192 == 0, "pop2024"].sum())
s["counties_no_portrait_employer_541921"] = int((df.cbp23_541921 == 0).sum())
s["pop_no_portrait_employer_541921"] = int(df.loc[df.cbp23_541921 == 0, "pop2024"].sum())
s["nonemployer_share_of_total"] = nat_nes / (nat_cbp + nat_nes)
s["by_cbsa_type"] = df.groupby("cbsa_type").apply(
    lambda x: {"counties": len(x), "pop2024": int(x.pop2024.sum()),
               "per100k": float((x.cbp23_54192.sum() + x.nes24_54192.sum()) / x.pop2024.sum() * 1e5),
               "median_county_per100k": float(x.per100k.median())}).to_dict()
# robustness: rank correlation 2024-mix vs 2023-matched
r = ok.dropna(subset=["per100k", "per100k_2023matched"])
s["spearman_primary_vs_2023matched"] = float(spearmanr(r.per100k, r.per100k_2023matched).statistic)
gg = g[g.oews25_per1000jobs.notna()].copy()
gg["oews25_per1000jobs"] = pd.to_numeric(gg.oews25_per1000jobs, errors="coerce")
gg = gg.dropna(subset=["oews25_per1000jobs"])
s["oews_join_metros"] = len(gg)
s["spearman_cbsa_per100k_vs_oews_per1000jobs"] = float(spearmanr(gg.per100k, gg.oews25_per1000jobs).statistic) if len(gg) else None
gm = g[g.cbp23msa_file.notna()]
s["cbsa_rollup_vs_cbp_msa_file_exact_match_share"] = float((gm.cbp23_54192 == gm.cbp23msa_file).mean())
gn = g[g.nes24msa_file.notna() & (g.nes24msa_flag != "S")]
s["cbsa_rollup_vs_nes_msa_file_exact_match_share"] = float((gn.nes24_54192 == gn.nes24msa_file).mean())
s["log"] = log
(OUT / "summary.json").write_text(json.dumps(s, indent=2, default=str))
print(json.dumps(s, indent=2, default=str))
