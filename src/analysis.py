"""Statistical analysis for the COVID-19 economic dashboard.

All functions accept the team's processed dataframe and return pandas DataFrames,
except wealth_shock_correlations, which returns a small correlation summary.
IMPORTANT: World Bank annual indicators are repeated on monthly rows. Never
sum or count the repeated values as independent annual observations.
"""

import numpy as np
import pandas as pd


def annual_data(df, indicators):
    """Return one validated row per country/year for annual indicators.

    Raises an error if the same country/year contains contradictory values.
    Missing values are preserved; callers decide what can be compared.
    """
    if isinstance(indicators, str):
        indicators = [indicators]
    cols = ["country", "year", *indicators]
    data = df[cols].copy().dropna(subset=["country", "year"])
    data["year"] = pd.to_numeric(data["year"], errors="coerce")
    data = data.dropna(subset=["year"])
    data["year"] = data["year"].astype(int)

    for indicator in indicators:
        contradictory = data.groupby(["country", "year"])[indicator].nunique(dropna=True)
        if contradictory.gt(1).any():
            examples = contradictory[contradictory.gt(1)].index.tolist()[:3]
            raise ValueError(f"{indicator}: contradictory values within country/year: {examples}")

    return (
        data.groupby(["country", "year"], as_index=False)[indicators]
        .first()
        .sort_values(["country", "year"])
        .reset_index(drop=True)
    )


def gdp_growth_summary(df, pre_years=(2015, 2019), shock_year=2020):
    """Compare mean pre-pandemic growth with growth in the shock year.

    'prepandemic_avg_growth' is an arithmetic mean of annual growth rates,
    not an estimate of the causal effect of COVID-19.
    """
    annual = annual_data(df, "wb_gdp_growth")
    pre = (
        annual[annual["year"].between(*pre_years)]
        .groupby("country")["wb_gdp_growth"]
        .mean()
        .rename("prepandemic_avg_growth")
    )
    shock = (
        annual[annual["year"].eq(shock_year)]
        .set_index("country")["wb_gdp_growth"]
        .rename("growth_2020")
    )
    result = pd.concat([pre, shock], axis=1).dropna().reset_index()
    result["growth_deviation_vs_preaverage_pp"] = (
        result["growth_2020"] - result["prepandemic_avg_growth"]
    )
    return result.sort_values("growth_2020").reset_index(drop=True)


def unemployment_change(df, start_year=2019, end_year=2020):
    """Unemployment percentage-point difference between two years."""
    annual = annual_data(df, "wb_unemployment_rate")
    table = annual.pivot(index="country", columns="year", values="wb_unemployment_rate")
    table = table.dropna(subset=[start_year, end_year])
    return (
        pd.DataFrame({
            "country": table.index,
            "unemployment_before": table[start_year].to_numpy(),
            "unemployment_after": table[end_year].to_numpy(),
            "change_pp": (table[end_year] - table[start_year]).to_numpy(),
        })
        .sort_values("change_pp", ascending=False)
        .reset_index(drop=True)
    )


def inflation_change(df, start_year=2019, end_year=2022):
    """Inflation percentage-point difference between two years."""
    annual = annual_data(df, "wb_inflation")
    table = annual.pivot(index="country", columns="year", values="wb_inflation")
    table = table.dropna(subset=[start_year, end_year])
    return (
        pd.DataFrame({
            "country": table.index,
            "inflation_before": table[start_year].to_numpy(),
            "inflation_after": table[end_year].to_numpy(),
            "change_pp": (table[end_year] - table[start_year]).to_numpy(),
        })
        .sort_values("change_pp", ascending=False)
        .reset_index(drop=True)
    )


def real_gdp_index(df, base_year=2019, end_year=2024):
    """Reconstruct a real GDP volume index from annual real growth (base=100).

    Requires a consecutive series: 2020 index = 100 * (1 + 2020 growth/100).
    The index is GDP LEVEL relative to base year, not a counterfactual trend.
    """
    annual = annual_data(df, "wb_gdp_growth")
    annual = annual[annual["year"].between(base_year, end_year)]
    records = []
    for country, group in annual.groupby("country"):
        growth_by_year = group.set_index("year")["wb_gdp_growth"]
        if base_year not in growth_by_year.index:
            continue
        level = 100.0
        records.append({"country": country, "year": base_year, "gdp_index": level})
        for year in range(base_year + 1, end_year + 1):
            if year not in growth_by_year.index or pd.isna(growth_by_year.loc[year]):
                break
            level *= (1 + growth_by_year.loc[year] / 100)
            records.append({"country": country, "year": year, "gdp_index": level})
    return pd.DataFrame(records, columns=["country", "year", "gdp_index"])


def gdp_recovery_2024(df, base_year=2019, target_year=2024):
    """Return change in REAL GDP level (not growth rate) versus base year."""
    levels = real_gdp_index(df, base_year=base_year, end_year=target_year)
    current = levels[levels["year"].eq(target_year)].copy()
    current["change_vs_2019_pct"] = current["gdp_index"] - 100.0
    return current.sort_values("change_vs_2019_pct", ascending=False).reset_index(drop=True)


def wealth_vs_shock(df, baseline_year=2019):
    """Country-level data for an exploratory wealth/economic shock scatter.

    gdp_shock_2020 is a team-defined derived measure; verify its construction
    with the preprocessing owner before drawing substantive conclusions.
    """
    annual = annual_data(df, ["wb_gdp_per_capita", "gdp_shock_2020"])
    comparison = annual[annual["year"].eq(baseline_year)].copy()
    comparison = comparison.dropna(subset=["wb_gdp_per_capita", "gdp_shock_2020"])
    comparison = comparison[comparison["wb_gdp_per_capita"] > 0]
    return comparison[["country", "wb_gdp_per_capita", "gdp_shock_2020"]].reset_index(drop=True)


def wealth_shock_correlations(df):
    """Exploratory correlations with and without the Timor-Leste outlier.

    Only 10 selected countries: descriptive, not population inference or causality.
    """
    data = wealth_vs_shock(df)
    records = []
    for label, subset in [
        ("All available countries", data),
        ("Excluding East Timor (sensitivity)", data[data["country"].ne("East Timor")]),
    ]:
        records.append({
            "sample": label,
            "countries": len(subset),
            "pearson_r": subset["wb_gdp_per_capita"].corr(
                subset["gdp_shock_2020"], method="pearson"
            ),
            "spearman_rho": subset["wb_gdp_per_capita"].rank().corr(
                subset["gdp_shock_2020"].rank()
            ),
        })

    return pd.DataFrame(records)
