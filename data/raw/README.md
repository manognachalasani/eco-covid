# COVID-19 and the Economy: Data Sources

Data for the multi-page Dash dashboard on the economic impact of COVID-19. Everything is downloaded when `covid_economy_final.ipynb` runs; no raw data is stored in this repository.

| Source | Used for | Coverage | How we get it | What worked |
|---|---|---|---|---|
| Our World in Data | COVID cases, deaths, vaccination, stringency | All countries, daily | CSV file | Backup (GitHub) |
| Eurostat | Unemployment, inflation, production, retail, GDP | Europe | API | API |
| FRED | CPI, GDP, jobs, M2, investment | United States | API with personal key | API |
| INSEE | Unemployment, prices, GDP | France | API | API |
| Mendeley Data | Two research datasets | OECD / 58 countries | API | API |
| World Bank | GDP, growth, unemployment, inflation, income groups | All countries, yearly | API | API |

## Our World in Data
- Page: https://ourworldindata.org/coronavirus
- Main file: `https://covid.ourworldindata.org/data/owid-covid-data.csv` (**did not work**, connection failed)
- Backup file: `https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv` (**worked**, 429,435 rows, data ends 14 Aug 2024)
- The stringency index comes from the Oxford COVID-19 Government Response Tracker: https://www.bsg.ox.ac.uk/research/covid-19-government-response-tracker

## Eurostat
- API: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{dataset}/{filter}?format=SDMX-CSV`
- No backup. All datasets loaded.

| Data | Dataset code |
|---|---|
| Unemployment (total and under 25) | `une_rt_m` |
| Inflation (HICP) | `prc_hicp_manr` |
| Industrial production | `sts_inpr_m` |
| Retail trade volume | `sts_trtu_m` |
| Quarterly real GDP | `namq_10_gdp` (unit `CLV20_MEUR` worked) |

Dataset pages: `https://ec.europa.eu/eurostat/databrowser/view/{dataset}/default/table`

## FRED
- API: `https://api.stlouisfed.org/fred/series/observations`
- Uses a personal API key (free, after creating an account at https://fred.stlouisfed.org). Create yours at https://fred.stlouisfed.org/docs/api/api_key.html and set `FRED_API_KEY`. Never share the key.
- All 10 series loaded.

| Series ID | Data |
|---|---|
| `CPIAUCSL` | Consumer price index |
| `PCEC96` | Real consumer spending |
| `UNRATE` | Unemployment rate |
| `UNEMPLOY` | Number of unemployed |
| `UEMPMEAN` | Average weeks unemployed |
| `M2SL` | M2 money supply |
| `FEDFUNDS` | Federal funds rate |
| `GDPC1` | Real GDP |
| `GPDIC1` | Real investment |
| `A006RL1Q225SBEA` | Investment growth |

## INSEE
- API: `https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/{idbank}` (no key needed)
- No backup. All 3 series loaded.

| idbank | Data |
|---|---|
| `001688526` | Unemployment rate (ILO), quarterly |
| `001759970` | Consumer price index, monthly |
| `010565692` | GDP volume, quarterly |

INSEE labels all three as "stopped series" (an older base year). The data is fine for 2015 to 2025, but they will not update. The GDP series ends earlier than the other two.

## Mendeley Data
- API: `https://data.mendeley.com/public-api/datasets/{id}/files?folder_id=root&version=1`
- Both datasets downloaded through the API.

| Dataset | Link |
|---|---|
| Unemployment and COVID-19 (OECD), DOI 10.17632/gtzzs3659m.1 | https://data.mendeley.com/datasets/gtzzs3659m/1 |
| 2020 crisis, 38 developed and 20 developing countries | https://data.mendeley.com/datasets/kjk9thmh2r/1 |

The second dataset's Excel sheets loaded with no usable country column, so it needs its headers fixed by hand before it can be merged.

## World Bank
- API: `https://api.worldbank.org/v2/country/all/indicator/{code}?format=json`
- Country list and income groups: `https://api.worldbank.org/v2/country`
- No backup. All 5 indicators loaded.

| Code | Data |
|---|---|
| `NY.GDP.MKTP.CD` | GDP (current US$) |
| `NY.GDP.MKTP.KD.ZG` | GDP growth (%) |
| `NY.GDP.PCAP.CD` | GDP per capita |
| `SL.UEM.TOTL.ZS` | Unemployment (%) |
| `FP.CPI.TOTL.ZG` | Inflation (%) |

## Attribution

> Data: Our World in Data (incl. Oxford COVID-19 Government Response Tracker), Eurostat, INSEE, FRED (Federal Reserve Bank of St. Louis), World Bank, Mendeley Data. Accessed October 2026.

Check each provider's terms before publishing the dashboard.

## Run it
1. Install `pandas numpy requests pyarrow sqlalchemy openpyxl plotly` (Python 3.12).
2. Set your own `FRED_API_KEY`.
3. Run `covid_economy_final.ipynb` from top to bottom. A failed source prints `✗` and is skipped.
4. Output goes to `data/clean/` and `data/covid_economy.db`.
