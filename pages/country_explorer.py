
"""Country Explorer page.

Displays a world map with hover tooltips.
Mock indicators will be replaced with CSV data later.
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html



# --------------------------------------------------
# 1. LOAD REAL DATA FOR THE COUNTRY EXPLORER
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "final_dataset.csv"

COUNTRY_FLAGS = {
    "CAF": "🇨🇫",
    "CHN": "🇨🇳",
    "DEU": "🇩🇪",
    "GBR": "🇬🇧",
    "GMB": "🇬🇲",
    "GNB": "🇬🇼",
    "JPN": "🇯🇵",
    "LSO": "🇱🇸",
    "TLS": "🇹🇱",
    "USA": "🇺🇸",
}


def display_value(value, suffix="", decimals=1):
    """Format real values for hover tooltips; show N/A for missing data."""
    if pd.isna(value):
        return "N/A"

    return f"{value:,.{decimals}f}{suffix}"


def load_country_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = df["date"].dt.year

    country_data = {}

    for code, flag in COUNTRY_FLAGS.items():
        country_rows = df[df["iso_code"] == code].copy()

        if country_rows.empty:
            continue

        # Use 2020 for the pandemic comparison.
        rows_2020 = country_rows[country_rows["year"] == 2020]

        # GDP indicators are already defined for 2020 in the dataset.
        gdp_growth = country_rows["gdp_growth_2020"].dropna()
        gdp_change = country_rows["gdp_shock_2020"].dropna()

        # Prefer the World Bank unemployment indicator for 2020.
        unemployment_rows = rows_2020["wb_unemployment_rate"].dropna()

        # Use the US-specific rate for the United States when available.
        if code == "USA":
            us_rate = rows_2020["us_unemployment_rate"].dropna()
            if not us_rate.empty:
                unemployment_rows = us_rate

        # Cases per million are monthly values: sum the 2020 values.
        cases = rows_2020["cases_per_million"].sum(min_count=1)

        # Average the available monthly restriction scores for 2020.
        stringency = rows_2020["stringency_index"].mean()

        country_name = country_rows["country"].dropna().iloc[0]

        country_data[code] = {
            "name": country_name,
            "flag": flag,
            "gdp_growth": display_value(
                gdp_growth.iloc[0] if not gdp_growth.empty else float("nan"),
                "%",
            ),
            "gdp_change": display_value(
                gdp_change.iloc[0] if not gdp_change.empty else float("nan"),
                "%",
            ),
            "unemployment": display_value(
                unemployment_rows.iloc[0]
                if not unemployment_rows.empty
                else float("nan"),
                "%",
            ),
            "cases_per_million": display_value(cases, decimals=0),
            "stringency": (
                f"{stringency:.1f}/100"
                if pd.notna(stringency)
                else "N/A"
            ),
        }

    return country_data


COUNTRY_DATA = load_country_data()


# --------------------------------------------------
# 2. BUILD THE WORLD MAP
# --------------------------------------------------

def make_country_map():
    country_codes = list(COUNTRY_DATA.keys())

    
    hover_details = [
        [
            COUNTRY_DATA[code]["flag"],
            COUNTRY_DATA[code]["name"],
            COUNTRY_DATA[code]["gdp_growth"],
            COUNTRY_DATA[code]["gdp_change"],
            COUNTRY_DATA[code]["unemployment"],
            COUNTRY_DATA[code]["cases_per_million"],
            COUNTRY_DATA[code]["stringency"],
        ]
        for code in country_codes
    ]


    fig = go.Figure(
        go.Choropleth(
            locations=country_codes,
            z=[1] * len(country_codes),
            locationmode="ISO-3",
            customdata=hover_details,
            colorscale=[
                [0, "#20cdb5"],
                [1, "#20cdb5"],
            ],
            zmin=0,
            zmax=1,
            showscale=False,
            marker={
                "line": {
                    "color": "#a5fff0",
                    "width": 0.8,
                }
            },
            
            
hovertemplate=(
    "<b>%{customdata[0]} &nbsp; %{customdata[1]}</b><br>"
    "<span style='color:#20cdb5'>"
    "ECONOMIC IMPACT · 2020"
    "</span><br><br>"
    "<b>GDP growth (2020):</b> %{customdata[2]}<br>"
    "<b>GDP shock indicator (2020):</b> %{customdata[3]}<br>"
    "<b>Unemployment:</b> %{customdata[4]}<br><br>"
    "<b>COVID-19 cases per million:</b> %{customdata[5]}<br>"
    "<b>Restriction stringency:</b> %{customdata[6]}"
    "<extra></extra>"
),


        )
    )

    fig.update_geos(
    projection_type="orthographic",
    projection_scale=0.95,
    projection_rotation=dict(lon=-15, lat=15),
    showland=True,
    landcolor="#172238",
    showocean=True,
    oceancolor="#0b1220",
    showlakes=True,
    lakecolor="#0b1220",
    showcountries=True,
    countrycolor="#35445b",
    showcoastlines=False,
    bgcolor="rgba(0,0,0,0)",
    showframe=False,
)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 0, "r": 0, "t": 10, "b": 0},
        height=600,
        hoverlabel={
            "bgcolor": "#101b2d",
            "bordercolor": "#20cdb5",
            "font": {
                "family": "Plus Jakarta Sans, sans-serif",
                "color": "#f3f7ff",
                "size": 13,
            },
            "align": "left",
        },
        geo={
            "showframe": False,
        },
font={
    "family": "Plus Jakarta Sans, Inter, sans-serif",
    "color": "#f4f7ff",
    "size": 11,
},
    )

    return fig


# --------------------------------------------------
# 3. PAGE LAYOUT
# --------------------------------------------------



def layout():
    return html.Div(
        id="pandemic-story",
        className="pandemic-story country-explorer-page",
        children=[
            # Cinematic opening
            html.Div(
                className="p-hero",
                children=[
                    html.Div(
                        id="pandemic-intro",
                        className="pandemic-intro",
                        children=[
                            html.Div(
                                "COUNTRY EXPLORER",
                                className="pandemic-intro-label",
                            ),
                            html.Div(
                                [
                                    "A world",
                                    html.Br(),
                                    html.Span(
                                        "transformed.",
                                        className="pandemic-intro-highlight",
                                    ),
                                ],
                                className="pandemic-intro-title",
                            ),
                            html.Div(
                                "Ten countries. One global crisis. "
                                "Different economic consequences.",
                                className="pandemic-intro-subtitle",
                            ),
                            html.Div(
                                className="pandemic-intro-accent-line",
                            ),
                        ],
                    ),
                    html.Div(className="p-grid"),
                    html.Div(
                        className="p-hero-inner chapter-hero-content",
                        children=[
                            html.Div(
                                "COVID STORY / COUNTRY EXPLORER",
                                className="p-kicker",
                            ),
                            html.Div("2020", className="p-year"),
                            html.H1(
                                [
                                    "ONE PANDEMIC. ",
                                    html.Span(
                                        "MANY REALITIES.",
                                        className="p-accent",
                                    ),
                                ],
                                className="p-title",
                            ),
                            html.P(
                                "The pandemic crossed borders, but its "
                                "economic consequences differed from "
                                "country to country. Explore the indicators "
                                "behind a global disruption.",
                                className="p-intro",
                            ),
                            html.Div(
                                "SCROLL TO EXPLORE THE WORLD ↓",
                                className="p-scroll",
                            ),
                        ],
                    ),
                ],
            ),

            # Data disclaimer
            html.Div(
                [
                    html.Strong("DATA NOTE"),
                    html.Span(
                        " Indicators are drawn from the project dataset. "
                        "Missing values are displayed as N/A."
                    ),
                ],
                className="p-chart-note",
            ),

            # World map section
            html.Section(
                className="p-section reveal",
                children=[
                    html.Div(
                        "01 / EXPLORE THE COUNTRIES",
                        className="p-eyebrow",
                    ),
                    html.H2(
                        "One pandemic. Different realities.",
                        className="p-heading",
                    ),
                    html.P(
                        "Hover over a highlighted country to "
                        "explore its economic and COVID-19 indicators.",
                        className="p-copy",
                    ),
                    html.Div(
                        className="p-panel country-globe-panel",
                        children=[
                            html.Div(
                                className="country-map-topbar",
                                children=[
                                    html.Div(
                                        [
                                            html.Div(
                                                "GLOBAL OVERVIEW",
                                                className="country-map-kicker",
                                            ),
                                            html.H3(
                                                "Explore the world",
                                                className="p-panel-title",
                                            ),
                                        ],
                                        className="country-map-heading",
                                    ),
                                    html.Div(
                                        [
                                            html.Span(
                                                className="country-map-legend-dot"
                                            ),
                                            html.Span("Countries in dataset"),
                                            html.Span(
                                                "2020 DATA",
                                                className="country-demo-label",
                                            ),
                                        ],
                                        className="country-map-legend",
                                    ),
                                ],
                            ),
                            dcc.Graph(
                                id="country-explorer-map",
                                figure=make_country_map(),
                                config={
                                    "displayModeBar": False,
                                    "scrollZoom": False,
                                    "responsive": True,
                                },
                                className="country-map-graph",
                                style={
                                    "width": "100%",
                                    "maxWidth": "900px",
                                    "height": "600px",
                                    "margin": "0 auto",
                                },
                            ),
                            html.P(
                                "Indicators are calculated from the project "
                                "dataset. Missing or unavailable values are "
                                "displayed as N/A.",
                                className="p-chart-note",
                            ),
                        ],
                    ),
                ],
            ),

            # Closing story section
            html.Section(
                className="p-ending reveal",
                children=[
                    html.Div(
                        "COUNTRY EXPLORER — FIELD NOTES",
                        className="p-eyebrow",
                    ),
                    html.H2(
                        [
                            "The impact was global. ",
                            html.Span(
                                "The outcomes were not.",
                                className="p-accent",
                            ),
                        ],
                        className="p-ending-title",
                    ),
                    html.P(
                        "Country-level indicators help reveal "
                        "differences in economic performance, "
                        "unemployment, reported cases, and policy "
                        "responses. Their interpretation depends "
                        "on the quality and context of the data.",
                        className="p-copy",
                    ),
                    html.Div(
                        "END OF COUNTRY EXPLORER",
                        className="p-next",
                    ),
                ],
            ),
        ],
    )
