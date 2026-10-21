"""
PandemiScope — Chapter 04: The Road Back
Data-backed recovery analysis built from final_dataset.csv.

The World Bank annual indicators are repeated across daily/monthly rows in the
combined dataset. This page collapses them to one observation per country/year
before calculating charts. GDP recovery is reconstructed from annual real GDP
growth with 2019 = 100; it is a level comparison, not a counterfactual estimate.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from dash import dcc

# Existing analysis module functions are reused where available. The page keeps
# its own validated calculations as a safe fallback if the module is at root
# rather than inside src/.
from src.analysis import (
    annual_data,
    real_gdp_index,
    gdp_recovery_2024,
    unemployment_change,
    inflation_change,
    wealth_vs_shock,
    )


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "final_dataset.csv"

if not DATA_PATH.exists():
    # Support running the app with the project root as the working directory.
    cwd_candidate = Path.cwd() / "final_dataset.csv"
    if cwd_candidate.exists():
        DATA_PATH = cwd_candidate
    else:
        raise FileNotFoundError(
            f"Could not find final_dataset.csv. Expected it at {DATA_PATH}."
        )

raw_df = pd.read_csv(DATA_PATH)
required = {"country", "year", "wb_gdp_growth"}
missing = required - set(raw_df.columns)
if missing:
    raise ValueError(f"final_dataset.csv is missing required columns: {sorted(missing)}")

raw_df["year"] = pd.to_numeric(raw_df["year"], errors="coerce")
raw_df = raw_df.dropna(subset=["country", "year"]).copy()
raw_df["year"] = raw_df["year"].astype(int)


def annual_indicator(data, indicator):
    """One validated median observation per country/year for annual indicators."""
    if indicator not in data.columns:
        return pd.DataFrame(columns=["country", "year", indicator])
    frame = data[["country", "year", indicator]].copy()
    frame[indicator] = pd.to_numeric(frame[indicator], errors="coerce")
    frame = frame.dropna(subset=["country", "year", indicator])
    return (
        frame.groupby(["country", "year"], as_index=False)[indicator]
        .median()
        .sort_values(["country", "year"])
    )


def apply_dark_style(fig, height=440):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#a7b2c8", size=12),
        title_font=dict(family="Plus Jakarta Sans, sans-serif", color="#f4f7ff", size=17),
        margin=dict(l=28, r=28, t=70, b=45),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c5d0e2")),
        hoverlabel=dict(bgcolor="#111b2b", font=dict(color="#f4f7ff")),
    )
    fig.update_xaxes(
        showgrid=False, zeroline=False,
        linecolor="rgba(167,178,200,0.18)",
        tickfont=dict(color="#a7b2c8"),
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="rgba(167,178,200,0.10)",
        zeroline=False, tickfont=dict(color="#a7b2c8"),
    )
    return fig


# --- GDP recovery index: 2019 = 100, compounded from annual growth rates ---
growth = annual_indicator(raw_df, "wb_gdp_growth")
index_records = []
for country, group in growth.groupby("country"):
    rates = group.set_index("year")["wb_gdp_growth"].to_dict()
    if 2019 not in rates:
        continue
    level = 100.0
    index_records.append({"country": country, "year": 2019, "gdp_index": level})
    for year in range(2020, 2025):
        rate = rates.get(year)
        if rate is None or pd.isna(rate):
            break
        level *= 1 + float(rate) / 100
        index_records.append({"country": country, "year": year, "gdp_index": level})
gdp_index = pd.DataFrame(index_records, columns=["country", "year", "gdp_index"])

if not gdp_index.empty:
    recovery_2024 = gdp_index[gdp_index["year"] == 2024].copy()
    recovery_2024["change_vs_2019_pct"] = recovery_2024["gdp_index"] - 100
    recovery_2024 = recovery_2024.sort_values("change_vs_2019_pct")
else:
    recovery_2024 = pd.DataFrame(columns=["country", "gdp_index", "change_vs_2019_pct"])

# Chart 1: GDP level path
if not gdp_index.empty:
    fig_gdp_path = px.line(
        gdp_index, x="year", y="gdp_index", color="country",
        markers=True, title="The road back: reconstructed real GDP level",
        labels={"year": "Year", "gdp_index": "GDP index (2019 = 100)", "country": "Country"},
        custom_data=["country"],
    )
    fig_gdp_path.add_hline(y=100, line_dash="dash", line_color="#e66a4e",
                           annotation_text="2019 baseline", annotation_position="top left")
    fig_gdp_path.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Year: %{x}<br>GDP index: %{y:.1f}<extra></extra>"
    )
else:
    fig_gdp_path = go.Figure().add_annotation(text="Insufficient annual GDP growth data to reconstruct a recovery path.", showarrow=False)
apply_dark_style(fig_gdp_path, 500)
fig_gdp_path.update_xaxes(dtick=1, range=[2019, 2024])

# Chart 2: 2024 leaderboard
if not recovery_2024.empty:
    colors = ["#e66a4e" if value < 0 else "#52c7b8" for value in recovery_2024["change_vs_2019_pct"]]
    fig_recovery_rank = go.Figure(go.Bar(
        x=recovery_2024["change_vs_2019_pct"],
        y=recovery_2024["country"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:+.1f}%" for v in recovery_2024["change_vs_2019_pct"]],
        textposition="outside",
        customdata=recovery_2024[["gdp_index"]].to_numpy(),
        hovertemplate="<b>%{y}</b><br>Change vs 2019: %{x:+.2f}%<br>2024 index: %{customdata[0]:.2f}<extra></extra>",
    ))
    fig_recovery_rank.add_vline(x=0, line_dash="dash", line_color="#a7b2c8")
    fig_recovery_rank.update_layout(
        title="By 2024: who was above the 2019 output level?",
        xaxis_title="Change in reconstructed real GDP level vs 2019 (%)",
        yaxis_title=None,
    )
else:
    fig_recovery_rank = go.Figure().add_annotation(text="No countries have a complete 2019–2024 GDP growth series.", showarrow=False)
apply_dark_style(fig_recovery_rank, max(390, 45 * max(1, len(recovery_2024)) + 110))

# Chart 3: annual GDP growth
fig_growth = px.line(
    growth[growth["year"].between(2015, 2024)],
    x="year", y="wb_gdp_growth", color="country", markers=True,
    title="The rebound is a growth rate — not the GDP level",
    labels={"year": "Year", "wb_gdp_growth": "Annual real GDP growth (%)", "country": "Country"},
)
fig_growth.add_vline(x=2020, line_dash="dash", line_color="#e66a4e",
                     annotation_text="Pandemic shock", annotation_position="top")
fig_growth.add_hline(y=0, line_color="rgba(167,178,200,0.55)")
apply_dark_style(fig_growth, 470)
fig_growth.update_xaxes(dtick=1)

# Chart 4: inflation before/after
inflation = annual_indicator(raw_df, "wb_inflation")
inflation_pivot = inflation[inflation["year"].isin([2019, 2022])].pivot(
    index="country", columns="year", values="wb_inflation"
)
if 2019 in inflation_pivot.columns and 2022 in inflation_pivot.columns:
    inflation_compare = inflation_pivot.dropna(subset=[2019, 2022]).copy()
    inflation_compare["change_pp"] = inflation_compare[2022] - inflation_compare[2019]
    inflation_compare = inflation_compare.sort_values("change_pp")
    fig_inflation = go.Figure()
    for country, row in inflation_compare.iterrows():
        fig_inflation.add_trace(go.Scatter(
            x=[row[2019], row[2022]], y=[country, country], mode="lines",
            line=dict(color="rgba(167,178,200,0.45)", width=3),
            showlegend=False, hoverinfo="skip",
        ))
    fig_inflation.add_trace(go.Scatter(
        x=inflation_compare[2019], y=inflation_compare.index, mode="markers",
        name="2019", marker=dict(color="#a7b2c8", size=10),
        hovertemplate="%{y}<br>2019 inflation: %{x:.2f}%<extra></extra>",
    ))
    fig_inflation.add_trace(go.Scatter(
        x=inflation_compare[2022], y=inflation_compare.index, mode="markers",
        name="2022", marker=dict(color="#e66a4e", size=11),
        hovertemplate="%{y}<br>2022 inflation: %{x:.2f}%<extra></extra>",
    ))
    fig_inflation.update_layout(
        title="The price aftershock: inflation in 2019 vs 2022",
        xaxis_title="Annual inflation rate (%)", yaxis_title=None,
        legend=dict(orientation="h", y=1.12, x=0),
    )
else:
    fig_inflation = go.Figure().add_annotation(text="Inflation comparison requires observations for both 2019 and 2022.", showarrow=False)
apply_dark_style(fig_inflation, 470)

# Chart 5: unemployment before and after
unemployment = annual_indicator(raw_df, "wb_unemployment_rate")
unemp_pivot = unemployment[unemployment["year"].isin([2019, 2020, 2024])].pivot(
    index="country", columns="year", values="wb_unemployment_rate"
)
if 2019 in unemp_pivot.columns and 2020 in unemp_pivot.columns:
    unemp_compare = unemp_pivot.dropna(subset=[2019, 2020]).copy()
    unemp_compare["change_pp"] = unemp_compare[2020] - unemp_compare[2019]
    unemp_compare = unemp_compare.sort_values("change_pp")
    fig_unemployment = go.Figure(go.Bar(
        x=unemp_compare["change_pp"], y=unemp_compare.index, orientation="h",
        marker_color=["#e66a4e" if v > 0 else "#52c7b8" for v in unemp_compare["change_pp"]],
        text=[f"{v:+.1f} pp" for v in unemp_compare["change_pp"]],
        textposition="outside",
        customdata=unemp_compare[[2019, 2020]].to_numpy(),
        hovertemplate="<b>%{y}</b><br>Change: %{x:+.2f} pp<br>2019: %{customdata[0]:.2f}%<br>2020: %{customdata[1]:.2f}%<extra></extra>",
    ))
    fig_unemployment.add_vline(x=0, line_dash="dash", line_color="#a7b2c8")
    fig_unemployment.update_layout(
        title="Employment did not necessarily recover with output",
        xaxis_title="Change in unemployment rate, 2019–2020 (percentage points)",
        yaxis_title=None,
    )
else:
    fig_unemployment = go.Figure().add_annotation(text="Unemployment comparison requires observations for both 2019 and 2020.", showarrow=False)
apply_dark_style(fig_unemployment, 450)

# Chart 6: pre-pandemic income vs 2024 recovery
income = annual_indicator(raw_df, "wb_gdp_per_capita")
income_2019 = income[income["year"] == 2019][["country", "wb_gdp_per_capita"]]
income_recovery = income_2019.merge(
    recovery_2024[["country", "change_vs_2019_pct"]], on="country", how="inner"
)
if not income_recovery.empty:
    fig_income = px.scatter(
        income_recovery, x="wb_gdp_per_capita", y="change_vs_2019_pct",
        text="country", hover_name="country", log_x=True,
        title="Did countries with different starting resources recover differently?",
        labels={
            "wb_gdp_per_capita": "GDP per capita in 2019 (current US$, log scale)",
            "change_vs_2019_pct": "Change in real GDP level by 2024 (%)",
        },
    )
    fig_income.update_traces(marker=dict(size=13, color="#8b80f9"), textposition="top center")
    fig_income.add_hline(y=0, line_dash="dash", line_color="#a7b2c8")
else:
    fig_income = go.Figure().add_annotation(text="Not enough matched 2019 income and 2024 recovery data for this comparison.", showarrow=False)
apply_dark_style(fig_income, 470)

# Optional EU and US high-frequency indicators in the supplied dataset
special_figures = []
if "eu_gdp_index_2019" in raw_df.columns:
    eu = raw_df[["date", "eu_gdp_index_2019"]].copy()
    eu["date"] = pd.to_datetime(eu["date"], dayfirst=True, errors="coerce")
    eu["eu_gdp_index_2019"] = pd.to_numeric(eu["eu_gdp_index_2019"], errors="coerce")
    eu = eu.dropna().drop_duplicates("date").sort_values("date")
    if not eu.empty:
        f = px.line(eu, x="date", y="eu_gdp_index_2019",
                    title="EU GDP volume: quarterly recovery path",
                    labels={"date": "Date", "eu_gdp_index_2019": "GDP volume index (2019 = 100)"})
        f.add_hline(y=100, line_dash="dash", line_color="#e66a4e",
                    annotation_text="2019 baseline")
        apply_dark_style(f, 400)
        special_figures.append(("A closer look: the EU", "Quarterly GDP volume index where available, shown separately from the annual cross-country series.", "recovery-eu-gdp-chart", f))

if "us_gdp_real_bn_idx2019" in raw_df.columns:
    us = raw_df[["date", "us_gdp_real_bn_idx2019"]].copy()
    us["date"] = pd.to_datetime(us["date"], dayfirst=True, errors="coerce")
    us["us_gdp_real_bn_idx2019"] = pd.to_numeric(us["us_gdp_real_bn_idx2019"], errors="coerce")
    us = us.dropna().drop_duplicates("date").sort_values("date")
    if not us.empty:
        f = px.line(us, x="date", y="us_gdp_real_bn_idx2019",
                    title="United States: real GDP index",
                    labels={"date": "Date", "us_gdp_real_bn_idx2019": "Real GDP index (2019 = 100)"})
        f.add_hline(y=100, line_dash="dash", line_color="#e66a4e",
                    annotation_text="2019 baseline")
        apply_dark_style(f, 400)
        special_figures.append(("A closer look: the United States", "Higher-frequency US GDP data offer a more detailed timeline than the annual country comparison.", "recovery-us-gdp-chart", f))


def chart_panel(kicker, title, description, graph_id, figure, height=None):
    graph_style = {"width": "100%", "display": "block"}
    if height:
        graph_style["height"] = f"{height}px"
    return html.Div(
        className="p-panel recovery-chart-panel",
        children=[
            html.Div(kicker, className="p-kicker"),
            html.H3(title, className="p-panel-title"),
            html.P(description, className="p-panel-copy"),
            dcc.Graph(id=graph_id, figure=figure,
                      config={"displayModeBar": False, "responsive": True},
                      style=graph_style),
        ],
        style={
            "display": "block", "visibility": "visible", "opacity": 1,
            "minWidth": 0, "height": "auto", "overflow": "visible",
        },
    )


# Data-driven recovery scorecards
n_countries = int(growth[growth["year"] == 2020]["country"].nunique())
n_above = int((recovery_2024["change_vs_2019_pct"] >= 0).sum()) if not recovery_2024.empty else 0
median_recovery = float(recovery_2024["change_vs_2019_pct"].median()) if not recovery_2024.empty else np.nan
median_unemp_change = float(unemp_compare["change_pp"].median()) if "unemp_compare" in globals() and not unemp_compare.empty else np.nan

def metric(value, label, detail):
    return html.Div(
        className="p-panel recovery-metric",
        children=[
            html.Div(value, className="recovery-metric-value"),
            html.Div(label, className="recovery-metric-label"),
            html.P(detail, className="p-panel-copy"),
        ],
        style={"minWidth": 0, "textAlign": "center"},
    )

median_text = f"{median_recovery:+.1f}%" if pd.notna(median_recovery) else "—"
unemp_text = f"{median_unemp_change:+.1f} pp" if pd.notna(median_unemp_change) else "—"

layout = html.Div(
    id="recovery-story",
    className="pandemic-story recovery-story",
    children=[
        # Chapter hero: preserve existing cinematic structure and class names.
        html.Div(
            className="p-hero",
            children=[
                html.Div(
                    id="recovery-intro",
                    className="pandemic-intro",
                    children=[
                        html.Div("CHAPTER 04", className="pandemic-intro-label"),
                        html.Div(
                            ["The ", html.Br(),
                             html.Span("Road Back.", className="pandemic-intro-highlight")],
                            className="pandemic-intro-title",
                        ),
                        html.Div("The world reopened. But what did recovery really mean?",
                                 className="pandemic-intro-subtitle"),
                        html.Div(className="pandemic-intro-accent-line"),
                    ],
                ),
                html.Div(className="p-grid"),
                html.Div(
                    className="p-hero-inner chapter-hero-content",
                    children=[
                        html.Div("PANDEMISCOPE  /  CHAPTER 04", className="p-kicker"),
                        html.Div("2021 — 2024", className="p-year"),
                        html.H1(["The road ", html.Span("back.", className="p-accent")], className="p-title"),
                        html.P(
                            "A rebound is not the same as a recovery. Follow the output level, "
                            "jobs and prices to see what changed after the 2020 shock—and which "
                            "countries had returned above their 2019 output level by 2024.",
                            className="p-intro",
                        ),
                        html.Div("↓  SCROLL TO EXPLORE THE RECOVERY", className="p-scroll"),
                    ],
                ),
            ],
        ),

        html.Section(
            className="p-section recovery-metrics-section",
            children=[
                html.Div("THE RECOVERY, IN NUMBERS", className="p-kicker"),
                html.H2(["A return to growth is only ", html.Span("the beginning.", className="p-accent")],
                        className="p-section-title"),
                html.P(
                    "Country-level annual indicators from final_dataset.csv. Countries are counted "
                    "only when the required years are available; medians are unweighted.",
                    className="p-section-intro",
                ),
                html.Div(
                    [
                        metric(str(n_countries), "Countries with 2020 GDP growth", "Available annual observations in the combined dataset."),
                        metric(f"{n_above} / {len(recovery_2024)}", "At or above 2019 GDP level by 2024", "Requires a consecutive annual growth series through 2024."),
                        metric(median_text, "Median change in GDP level", "Median reconstructed real GDP level change vs 2019."),
                        metric(unemp_text, "Median unemployment change", "2019 to 2020, percentage points; available countries only."),
                    ],
                    className="recovery-metric-grid",
                    style={"display": "grid", "gridTemplateColumns": "repeat(4, minmax(0, 1fr))", "gap": "18px"},
                ),
                html.P(
                    "Method: GDP index is compounded from annual real GDP growth with 2019 = 100. "
                    "It compares output levels, not a hypothetical no-pandemic trend and not a causal effect.",
                    className="p-chart-caption",
                ),
            ],
        ),

        html.Section(
            className="p-section",
            children=[
                html.Div("01  /  THE LEVEL, NOT JUST THE RATE", className="p-kicker"),
                html.H2(["Did output make it ", html.Span("back?", className="p-accent")],
                        className="p-section-title"),
                html.P(
                    "The GDP growth rate tells us how quickly output changed in a year. The indexed "
                    "GDP level tells us whether the accumulated changes brought output above or below "
                    "its 2019 level.",
                    className="p-section-intro",
                ),
                chart_panel("2019 = 100", "The recovery path", "Track the reconstructed real GDP level. The dashed line marks the pre-pandemic baseline.", "recovery-path-chart", fig_gdp_path),
                chart_panel("COUNTRY COMPARISON / 2024", "Who was above the baseline?", "Countries are ranked by reconstructed 2024 real GDP level relative to 2019. Only complete annual series are included.", "recovery-rank-chart", fig_recovery_rank),
                chart_panel("ANNUAL GROWTH / 2015–2024", "The rebound versus the recovery", "The 2020 shock and later growth rates are shown together. Strong positive growth after a contraction does not automatically erase the cumulative output loss.", "recovery-growth-chart", fig_growth),
            ],
        ),

        html.Section(
            className="p-section",
            children=[
                html.Div("02  /  THE RECOVERY PEOPLE FELT", className="p-kicker"),
                html.H2(["Output, jobs and ", html.Span("prices.", className="p-accent")],
                        className="p-section-title"),
                html.P(
                    "GDP is only one part of recovery. Employment conditions and the cost of living "
                    "can move differently from total economic output.",
                    className="p-section-intro",
                ),
                chart_panel("COST OF LIVING / 2019 VS 2022", "The inflation aftershock", "Compare annual inflation before the pandemic with 2022. These are inflation rates, not the total change in the price level.", "recovery-inflation-chart", fig_inflation),
                chart_panel("LABOUR MARKET / 2019–2020", "The unemployment impact", "The chart shows the percentage-point change in the unemployment rate between 2019 and 2020. A negative value means the measured rate fell; it does not by itself prove labour-market recovery.", "recovery-unemployment-chart", fig_unemployment),
                chart_panel("STARTING POINTS / COUNTRY COMPARISON", "Did starting resources matter?", "Compare 2019 GDP per capita with the change in reconstructed GDP level by 2024. With only a small group of countries, treat this as an exploratory association, not a causal conclusion.", "recovery-income-chart", fig_income),
            ],
        ),

        *[
            html.Section(
                className="p-section",
                children=[
                    html.Div("03  /  A CLOSER LOOK", className="p-kicker"),
                    html.H2(title, className="p-section-title"),
                    html.P(description, className="p-section-intro"),
                    dcc.Graph(id=graph_id, figure=figure,
                              config={"displayModeBar": False, "responsive": True},
                              style={"height": "430px", "width": "100%"}),
                ],
            )
            for title, description, graph_id, figure in special_figures
        ],

        html.Section(
            className="p-section",
            children=[
                html.Div("04  /  WHAT THE EVIDENCE CAN SAY", className="p-kicker"),
                html.Div(
                    className="p-panel p-takeaway-panel",
                    children=[
                        html.H2("Tell the story the data supports.", className="p-section-title"),
                        html.P(
                            "Use the charts to form a conclusion. Separate observed patterns from "
                            "possible explanations, and name one limitation of the data.",
                            className="p-panel-copy",
                        ),
                        dcc.Textarea(
                            id="recovery-takeaway",
                            placeholder="Our evidence suggests...\n\nThe indicators show...\n\nOne important limitation is...",
                            className="p-takeaway-input",
                        ),
                        html.Div(id="takeaway-preview", className="p-takeaway-preview"),
                    ],
                ),
            ],
        ),

        html.Section(
            className="p-ending",
            children=[
                html.Div("CHAPTER 04  /  THE ROAD BACK", className="p-kicker"),
                html.H2(["Recovery is not just ", html.Br(), html.Span("getting back.", className="p-accent")],
                        className="p-section-title"),
                html.P(
                    "It is about understanding whether output returned to its earlier level, "
                    "whether jobs and prices followed the same path, and which challenges remained "
                    "after the world reopened.",
                    className="p-section-intro",
                ),
         dcc.Link(
            "THE STORY CONTINUES →",
            href="/",
            className="p-scroll continue-button",
        ),
    ],
),
    ],
)
