# Photographer deserts: where the US has the fewest photographers per capita

Open dataset from the **Photo Intelligence Lab by Narkis**. Photography businesses (NAICS 54192, employer
establishments from Census County Business Patterns 2023 plus self-employed nonemployer businesses from Census
Nonemployer Statistics 2024) per 100,000 residents, for every US county, metro and state.

Read the full study with maps and rankings: **[Photographer deserts](https://narkis.ai/research/photographer-deserts?utm_source=github&utm_medium=lab-dataset)**.

## Fewest photographers per 100k residents, by state

| State | Per 100k |
|---|---|
| Mississippi | 49.4 |
| West Virginia | 53.5 |
| New Mexico | 55.1 |
| Kentucky | 56.9 |
| Arkansas | 59.9 |
| Delaware | 61.2 |
| Alabama | 61.5 |
| Indiana | 64.0 |
| Pennsylvania | 65.8 |
| Arizona | 65.8 |

## Files (`data/`)

- `county_photographers_per100k.csv`: 3,144 counties, with published and upper-bound rates (Census suppresses cells with fewer than 3 businesses, so `per100k_upper` adds the maximum hidden count; rank on it before claiming a county is lowest)
- `cbsa_photographers_per100k.csv`: metro and micro areas
- `state_photographers_per100k.csv`: states
- `zero_published_counties.csv`: counties where Census publishes no photography business at all (means 0-2, not zero)

## Study notes

Photo Intelligence Lab by Narkis. Built 2026-10-25. Only official public data was used (Census CBP, Census Nonemployer Statistics, Census Population Estimates, BLS OEWS). No Narkis listing data is in any number below. All files are read-only downloads, and every figure can be rebuilt with `scripts/build.py` and `scripts/tables.py`.

## What we measure, in one paragraph

**Photography businesses per 100,000 residents, by county.** Businesses = NAICS **54192 Photographic Services**, counted two ways and added together: **employer establishments** (businesses with payroll, from County Business Patterns **2023**) plus **nonemployer businesses** (self-employed people filing as a business with receipts of at least $1,000, from Nonemployer Statistics **2024**). Residents = Census Population Estimates, Vintage 2025, **July 1, 2024**, chosen to line up with the NES year. Nonemployers make up **94%** of the total (243,502 of 258,975 nationally), which is why using CBP alone would be wrong for this question.

> **Why 54192 and not 541921 (portrait only)?** Nonemployer Statistics only publishes 5-digit 54192 (portrait plus commercial photography) for counties, metros and states. It has no 6-digit split anywhere. CBP does split it, so we also report **portrait-studio employers (541921)** as a separate column. The headline measure, though, is "photography businesses", not "portrait photographers". Nationally, employer establishments break down as 541921 = 10,515 and 541922 = 4,424 in published county cells.

## National baseline

| Metric | Value |
|---|---|
| US photography businesses (CBP 2023 employer, county cells 15,473 + NES 2024 nonemployer, state file 243,502) | **258,975** |
| US rate | **76.2 per 100k** (≈1 per 1,313 residents) |
| **Median county** (3,127 counties ranked) | **56.8 per 100k** |
| Population-weighted median county | 73.9 per 100k |
| County p10 / p90 | 0 / 100.9 per 100k |
| Metro counties (1,186) / micro (658) / rural non-CBSA (1,300) | **78.8 / 62.1 / 52.7 per 100k** |
| Average receipts per nonemployer photography business, US (NES 2024) | **$29,379/yr** (average, not median) |

## Lowest-supply counties

**Population ≥ 50,000** (1,010 counties ranked):

| # | County | Pop 2024 | Employer est. (CBP23) | Nonemployers (NES24) | Per 100k | 2023-matched |
|---|---|---|---|---|---|---|
| 1 | McKinley County, NM (Gallup) | 68,631 | <3 (not published) | 11 | **16.0** | 16.0 (#1) |
| 2 | Apache County, AZ | 64,695 | <3 | 12 | 18.6 | 20.0 (#2) |
| 3 | Maverick County, TX (Eagle Pass) | 58,580 | <3 | 12 | 20.5 | 24.1 (#6) |
| 4 | Anderson County, TX | 59,573 | <3 | 15 | 25.2 | 35.6 (#38, unstable) |
| 5 | Orangeburg County, SC | 83,171 | <3 | 23 | 27.6 | 24.0 (#5) |
| 6 | Imperial County, CA | 182,771 | 3 | 48 | 27.9 | 20.5 (#3) |
| 7 | Cumberland County, NJ | 156,407 | 3 | 42 | 28.8 | 27.8 |
| 8 | Ashtabula County, OH | 96,748 | <3 | 28 | 28.9 | 21.7 |
| 9 | Robeson County, NC | 119,400 | <3 | 35 | 29.3 | 24.6 |
| 10 | San Patricio County, TX | 71,534 | <3 | 21 | 29.4 | 28.3 |

**Population ≥ 250,000** (292 counties):

| # | County | Pop 2024 | Employer | Nonemployer | Per 100k | 2023-matched rank |
|---|---|---|---|---|---|---|
| 1 | **Merced County, CA** | 296,807 | **<3** | 96 | **32.3** | #1 |
| 2 | **Bronx County, NY** | 1,406,052 | 12 | 446 | **32.6** | #2 |
| 3 | El Paso County, TX | 879,894 | 19 | 316 | 38.1 | #4 |
| 4 | Tulare County, CA | 483,851 | 6 | 189 | 40.3 | #3 |
| 5 | Kern County, CA | 924,648 | 16 | 360 | 40.7 | #5 |
| 6 | Yakima County, WA | 258,971 | 5 | 104 | 42.1 | #9 |
| 7 | Webb County, TX (Laredo) | 280,570 | 6 | 117 | 43.8 | |
| 8 | San Joaquin County, CA | 817,149 | 15 | 358 | 45.6 | |
| 9 | Cameron County, TX | 432,952 | 3 | 196 | 46.0 | |
| 10 | Luzerne County, PA | 330,898 | 10 | 144 | 46.5 | |

At the top among ≥250k: New York County (Manhattan) 167.1, Kings (Brooklyn) 160.7, Williamson TN 154.9, Utah County UT 154.6, Marin CA 147.1, Davidson TN (Nashville) 146.9.

**Population ≥ 1M** (50 counties): lowest are Bronx 32.6, Fresno 47.8, San Bernardino 55.2, **Santa Clara 57.4**, Wayne MI 59.2, Riverside 59.9. Highest are Manhattan 167.1, Brooklyn 160.7, Travis TX 121.0 and Fulton GA 117.1. The same six are the bottom six in the matched-2023 run (Wayne and Riverside swap 5/6).

Full list: `tables.md`. Every county: `county_photographers_per100k.csv`.

## States (lowest → highest, per 100k)

Lowest: **Mississippi 49.4** (38 employer studios statewide), West Virginia 53.5 (11 employer studios for 1.77M people), New Mexico 55.1, Kentucky 56.9, Arkansas 59.9, Delaware 61.2, Alabama 61.5, Indiana 64.0.
Highest: **Montana 124.0**, Hawaii 117.6, Utah 112.4, Colorado 111.1, Wyoming 108.4, Vermont 97.0.
Average receipts per self-employed photography business run from about $21.7k (MS) and $22.0k (WV) up to $41.8k (NY) and $40.0k (DC). Full table: `state_photographers_per100k.csv`.

## Biggest metros (CBSAs ≥ 1M, 55 metros; county roll-up)

Lowest: **Fresno 46.8**, Riverside–San Bernardino 57.7, **San Jose–Sunnyvale–Santa Clara 57.9**, Buffalo 59.5, Tucson 60.3, Memphis 62.4, Louisville 63.8, San Antonio 66.0, Houston 68.5, Phoenix 70.0.
Highest: **Nashville 115.7**, Denver 109.3, Austin 107.3, Portland OR 102.2, Grand Rapids 100.5, Los Angeles 99.4, Salt Lake City 98.7.
Metros ≥250k, lowest: Merced 32.3, El Paso 37.9, Visalia 40.3, Bakersfield 40.7, Yakima 42.1, Laredo 43.8, Stockton 45.6, Brownsville 46.0, Corpus Christi 46.4, Fresno 46.8. Highest: Provo–Orem 153.4, Bend 142.3, Boulder 140.2, Fort Collins 129.6.
File: `cbsa_photographers_per100k.csv`, with BLS OEWS May 2025 photographer employment, jobs per 1,000 and median wage joined in where BLS publishes them.

## Counties with no published photography businesses of either kind

**399 counties, home to 2,154,988 people (2024)**, have no published CBP 54192 cell and no published NES 54192 cell. **This does not mean zero.** Both programs leave out any cell with fewer than 3 establishments, so the precise statement is "**fewer than 3 photography studios with employees and fewer than 3 self-employed photography businesses**", which allows at most 4 in total. These are all small counties: the largest is Clarke County, AL (22,127), and the median is 4,181. Texas (67), Nebraska (35), Kansas (30), South Dakota (26) and Georgia (24) have the most. **93 of the 399 had a published NES count (≥3) in 2023**, so membership changes a lot from year to year. Publish this as a count of counties and people, not as a "these towns have no photographer" list. File: `zero_published_counties.csv` (400 lines incl. header), with nes23 values for context.

Related and more robust facts:
- **2,412 of 3,144 counties (64.9M residents)** have fewer than 3 photography **employer** establishments. 343 of those counties have ≥50k residents (28.1M people in total).
- The largest counties with **fewer than 3 photography employer establishments** (they rely entirely on self-employed photographers) are **Clayton County, GA (297k)**, **Merced County, CA (297k)**, Yuma AZ (221k), Onslow NC (215k), Butte CA (209k), Richmond GA (Augusta, 207k), Kaufman TX (198k) and DeSoto MS (197k).
- 2,487 counties (72.7M people) have fewer than 3 **portrait-studio (541921)** employer establishments.
- 498 counties (4.56M people) are below 25 per 100k on the published counts. If every unpublished cell is filled at its maximum of 2, only **28 counties (0.83M people)** stay below 25. So "under 25" is only defensible as a lower-bound claim.

## Headline candidates (defensible, local-press angles)

1. **The Bronx has a fifth of Manhattan's photographers.** 32.6 photography businesses per 100k residents vs 167.1 in Manhattan and 160.7 in Brooklyn. That makes the Bronx the lowest of all 50 US counties with 1M+ people, and it held in both data years (2023: 30.5 vs 170.6). Self-employed photographers in the Bronx also average $27.6k in receipts vs $55.3k in Manhattan. *(Caveat: NES uses the owner's mailing address, so this measures where photographers are based, not where they shoot.)*
2. **Merced County, CA is the most under-served large county in America.** Its 297k residents are served by 96 self-employed photography businesses and fewer than 3 studios with staff: 32.3 per 100k, the lowest of 292 counties with 250k+ people, in both years. The San Joaquin Valley and Texas border metros fill the bottom of the 250k+ metro list (Merced, El Paso, Visalia, Bakersfield, Laredo, Stockton, Brownsville, Fresno, McAllen).
3. **Fresno is the biggest-metro photography desert; Nashville is the oasis.** Among 55 US metros with 1M+ people, Fresno has 46.8 per 100k and Nashville 115.7, a 2.5× gap. **Silicon Valley (San Jose metro, 57.9) ranks 3rd-lowest**, a headshot-heavy labor market with among the fewest photographers per resident of any big metro.
4. **Mississippi is the least-served state, Montana the best-served (49.4 vs 124.0 per 100k, 2.5×).** West Virginia has 11 photography studios with employees for 1.77M people. Self-employed photographers in MS/WV average about $22k a year in receipts, roughly half of New York's $41.8k.
5. **Rural America has a third fewer photographers per person.** Rural (non-metro, non-micro) counties have 52.7 per 100k vs 78.8 in metro counties. 2.15M people live in 399 counties where Census publishes no photography business count at all (fewer than 3 of each type).
6. **94% of America's photography businesses are one-person operations.** 243,502 nonemployer businesses vs 15,473 employer establishments, with average receipts of $29.4k a year. In 2,412 counties (65M residents) there are fewer than three photography businesses with any paid staff.
7. **The lowest-supply county with 50k+ people is McKinley County, NM (Gallup)** at 16.0 per 100k, followed by Apache County, AZ at 18.6, the same top two in both years. *Handle with care:* both counties cover large parts of the Navajo Nation, and IRS-based counts can miss informal or tribal-jurisdiction businesses. Pitch it only with local verification.

Strongest for press: **1 (Bronx vs Manhattan), 2 (Merced / Central Valley), 3 (Fresno vs Nashville + Silicon Valley), 4 (MS vs MT), 6 (94% solo)**.

## Caveats (publish these with the study)

1. **Industry ≠ headshot photographers.** NAICS 54192 covers portrait studios (school, wedding, family, headshot) plus commercial photography. Businesses are classified by their primary activity, as self-reported to the IRS/Census, so wedding/event shooters, part-time photographers filing under other codes, and photographers working inside other businesses (media, schools, retail chains) are miscounted either way. Say "photography businesses", not "headshot photographers".
2. **Nonemployers include part-timers and side gigs.** Anyone filing a Schedule C (or as a partnership/corporation with no payroll) with ≥$1,000 in receipts counts, including a hobbyist with a few paid shoots. The count is of businesses, not full-time equivalents. Average receipts ($29k) are skewed by the tail, and NES publishes no medians.
3. **Data years differ.** CBP **2023** is the latest published: no 2024 CBP was on www2.census.gov on 2026-10-25. NES **2024** (released 2026). Population is PEP V2025 July 2024. As a robustness run, the fully matched **2023** version (CBP 2023 + NES 2023 + PEP July 2023) gives a Spearman rank correlation of **0.85** with the primary across counties, and the headline rankings above hold. BLS OEWS is May 2025.
4. **Disclosure suppression.** Since reference year 2017, CBP **drops any cell with fewer than 3 establishments** (there is no "D" flag any more, and the employment noise flags G/H/J don't affect establishment counts). NES county cells are likewise never published below 3. NES 2024 has **17 counties flagged "S"** (estimate did not meet publication standards). They are left out of rankings, kept in the CSV, and all are small (≤14k people). As a result, an absent cell is treated as 0 in the main measure (a lower bound), and `per100k_upper` adds 2 for each absent source. No headline above changes under the upper bound except the "under 25" claim, as noted.
5. **Geography.** NES assigns businesses by the owner's mailing address, and CBP by establishment location. Photographers serve neighbouring counties, so a low county rate next to a high one (Bronx/Manhattan) partly reflects commuting and where people live, not access alone. Metro numbers are sums of their counties, using the 2023 OMB delineation as used in PEP V2025. They match Census's own NES metro file in 94% of metros and run slightly below the CBP metro file in some metros, because county cells under 3 are dropped (e.g., Chicago 609 vs 611).
6. **Cross-check with BLS OEWS** (SOC 27-4021, photographers employed by others, so self-employed are excluded): Spearman 0.45 between metro per-100k and OEWS photographers per 1,000 jobs across 179 joinable metros. They agree in direction but measure different things.
7. Connecticut uses the 9 planning regions (09110–09190) in every source, and all join cleanly. No source FIPS failed to match the PEP county list.
8. Nothing here comes from Narkis listings. Our own data can't say anything about supply.

## Exact sources and queries

The Census Data API (`api.census.gov/data/<year>/cbp|nonemp`) now answers keyless requests with a 302 redirect to `missing_key.html`, so the official bulk files were used instead. They hold identical published values.

```
B=https://www2.census.gov/programs-surveys
curl -O $B/cbp/datasets/2023/cbp23co.zip            # CBP 2023 county  (naics "54192/", "541921", "541922"; field est)
curl -O $B/cbp/datasets/2023/cbp23msa.zip           # CBP 2023 metro (cross-check)
curl -O $B/nonemployer-statistics/datasets/2024/historical-datasets/nonemp24co.zip   # NES 2024 county (NAICS "54192"; ESTAB, ESTAB_F, RCPTOT)
curl -O $B/nonemployer-statistics/datasets/2024/historical-datasets/nonemp24msa.zip  # NES 2024 metro (cross-check)
curl -O $B/nonemployer-statistics/datasets/2024/historical-datasets/nonemp24st.zip   # NES 2024 state (LFO "-")
curl -O $B/nonemployer-statistics/datasets/2023/historical-datasets/nonemp23co.zip   # NES 2023 county (robustness)
curl -O $B/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv          # PEP V2025 county (SUMLEV 50; POPESTIMATE2024)
curl -O $B/popest/datasets/2020-2025/metro/totals/cbsa-est2025-alldata.csv           # PEP V2025 CBSA + component counties
curl -A "Mozilla/5.0" -O https://www.bls.gov/oes/special-requests/oesm25ma.zip         # BLS OEWS May 2025 metro (OCC_CODE 27-4021)
```
Equivalent API calls (with a key; not executed here, variable names per Census API docs): `https://api.census.gov/data/2023/cbp?get=ESTAB,NAME&for=county:*&NAICS2017=54192&key=…` and `https://api.census.gov/data/2024/nonemp?get=NESTAB,NAME&for=county:*&NAICS2017=54192&key=…`.

Rules used in `build.py`: county = PEP SUMLEV 50 (3,144). CBP row absent → 0 (true value 0–2). NES row absent → 0 (0–2). NES `S` → NaN, excluded from rankings. total = CBP 54192 + NES 54192. per100k = total / POPESTIMATE2024 × 100,000. State totals = CBP county cells summed + NES state file.

## Files

- `raw/`: unmodified downloads (zips + extracted txt/csv, OEWS xlsx)
- `build.py`: builds every table and `summary.json` (all summary numbers, join logs, robustness stats)
- `tables.py` → `tables.md`: ranked tables quoted above
- `county_photographers_per100k.csv`: one row per county (fips, county, state, pop2024/2025, CBSA, cbp23_541921 portrait employers, cbp23_541922, cbp23_54192, nes24_54192 + flag, total, per100k, per100k_upper, receipts, 2023-matched columns)
- `cbsa_photographers_per100k.csv`: 925 CBSAs (387 metro + 538 micro), with Census metro-file cross-check and BLS OEWS columns
- `state_photographers_per100k.csv`
- `zero_published_counties.csv`

## Before publishing

- Ground-truth the 3–4 headline places by hand (Merced, Bronx, Fresno, McKinley): a Google Maps / Yelp count of photographers based locally, as a sanity layer only.
- Optional access layer: distance from each zero-published county's population centroid to the nearest county with ≥10 businesses (Census centers of population), which would make "desert" a distance claim instead of a count.


## No photographer nearby?

In a photographer desert the nearest studio can be an hour away. [Narkis](https://narkis.ai?utm_source=github&utm_medium=lab-dataset) makes professional
headshots from your own selfies: up to 200 photos from $27, no studio, no drive. Disclosure: the Lab is run by Narkis.

## License

CC BY 4.0. Source data: US Census Bureau (CBP 2023, NES 2024, Population Estimates V2025). Cite as: *Photo Intelligence
Lab by Narkis, "Photographer deserts", 2026, https://narkis.ai/research/photographer-deserts*.
