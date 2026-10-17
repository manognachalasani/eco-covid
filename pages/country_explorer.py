
"""Country Explorer page.

Displays a world map with hover tooltips.
Mock indicators will be replaced with CSV data later.
"""

from dash import dcc, html
import plotly.graph_objects as go


# --------------------------------------------------
# 1. MOCK DATA
# Replace these values with CSV-derived indicators later.
# All numeric values below are illustrative.
# --------------------------------------------------


COUNTRY_DATA = {
    "CAF": {
        "name": "Central African Republic",
        "flag": "🇨🇫",
        "gdp_growth": "-1.0%",
        "gdp_change": "-2.0%",
        "unemployment": "6.2%",
        "cases_per_million": "2,800",
        "stringency": "55/100",
    },
    "CHN": {
        "name": "China",
        "flag": "🇨🇳",
        "gdp_growth": "2.2%",
        "gdp_change": "10.0%",
        "unemployment": "5.1%",
        "cases_per_million": "7,000",
        "stringency": "75/100",
    },
    "DEU": {
        "name": "Germany",
        "flag": "🇩🇪",
        "gdp_growth": "-4.1%",
        "gdp_change": "-4.1%",
        "unemployment": "3.8%",
        "cases_per_million": "460,000",
        "stringency": "65/100",
    },
    "GBR": {
        "name": "United Kingdom",
        "flag": "🇬🇧",
        "gdp_growth": "-10.3%",
        "gdp_change": "-10.3%",
        "unemployment": "4.5%",
        "cases_per_million": "365,000",
        "stringency": "70/100",
    },
    "GMB": {
        "name": "The Gambia",
        "flag": "🇬🇲",
        "gdp_growth": "-0.2%",
        "gdp_change": "-0.2%",
        "unemployment": "9.5%",
        "cases_per_million": "4,500",
        "stringency": "50/100",
    },
    "GNB": {
        "name": "Guinea-Bissau",
        "flag": "🇬🇼",
        "gdp_growth": "1.5%",
        "gdp_change": "3.0%",
        "unemployment": "3.0%",
        "cases_per_million": "4,000",
        "stringency": "45/100",
    },
    "JPN": {
        "name": "Japan",
        "flag": "🇯🇵",
        "gdp_growth": "-4.2%",
        "gdp_change": "-4.2%",
        "unemployment": "2.8%",
        "cases_per_million": "270,000",
        "stringency": "50/100",
    },
    "LSO": {
        "name": "Lesotho",
        "flag": "🇱🇸",
        "gdp_growth": "-5.6%",
        "gdp_change": "-5.6%",
        "unemployment": "16.0%",
        "cases_per_million": "16,000",
        "stringency": "60/100",
    },
    "TLS": {
        "name": "Timor-Leste",
        "flag": "🇹🇱",
        "gdp_growth": "-8.6%",
        "gdp_change": "-8.6%",
        "unemployment": "4.0%",
        "cases_per_million": "17,000",
        "stringency": "55/100",
    },
    "USA": {
        "name": "United States",
        "flag": "🇺🇸",
        "gdp_growth": "-2.2%",
        "gdp_change": "-2.2%",
        "unemployment": "8.1%",
        "cases_per_million": "310,000",
        "stringency": "65/100",
    },
}



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
    "ECONOMIC IMPACT · DEMO DATA"
    "</span><br><br>"
    "<b>GDP growth (2020):</b> %{customdata[2]}<br>"
    "<b>GDP change vs 2019:</b> %{customdata[3]}<br>"
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
                                className="pandemic-intro-accent-line"
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
                className="p-container",
                children=[
                    html.Div(
                        className="p-demo-note reveal",
                        children=[
                            html.Strong("FRONTEND PREVIEW"),
                            html.Span(
                                "Illustrative demo values are shown until "
                                "the final dataset is connected. These "
                                "values should not be presented as "
                                "historical statistics."
                            ),
                        ],
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
                                "explore its economic and COVID-19 "
                                "indicators.",
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
                                                    html.Span(
                                                        "Countries in dataset"
                                                    ),
                                                    html.Span(
                                                        "DEMO DATA",
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
                                        "The map currently uses illustrative "
                                        "values. Indicators will be connected "
                                        "to the project CSV in a later step.",
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
            ),
        ],
    )
