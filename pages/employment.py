
# pages/employment.py

from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# MOCK DATA — REPLACE WITH VERIFIED DATA BEFORE PRESENTATION
#
# All figures below are invented for prototyping.
# They must not be presented as actual historical observations.
#
# unemployment_rate: illustrative annual unemployment rate (%)
# employment_index: illustrative employment index, 2019 = 100
# ============================================================

YEARS = [2018, 2019, 2020, 2021, 2022, 2023]

COUNTRY_DATA = {
    "Central African Republic": {
        "unemployment_rate": [6.2, 6.3, 7.0, 6.8, 6.5, 6.3],
        "employment_index": [98, 100, 94, 96, 99, 101],
        "community": "Informal work and small-scale livelihoods",
        "story": (
            "For households relying on informal trade and daily earnings, "
            "movement restrictions and disrupted markets could make "
            "earning a living more uncertain."
        ),
    },
    "China": {
        "unemployment_rate": [4.9, 5.2, 5.6, 5.1, 5.6, 5.2],
        "employment_index": [98, 100, 96, 99, 97, 101],
        "community": "Manufacturing and urban service workers",
        "story": (
            "Factory interruptions and changes in consumer demand could "
            "affect workers differently from those able to work remotely."
        ),
    },
    "Germany": {
        "unemployment_rate": [3.4, 3.1, 3.8, 3.6, 3.1, 3.0],
        "employment_index": [99, 100, 98, 100, 103, 105],
        "community": "Industrial workers and small businesses",
        "story": (
            "Support measures and reduced working hours can shape the "
            "difference between keeping a job and losing working income."
        ),
    },
    "United Kingdom": {
        "unemployment_rate": [4.0, 3.8, 4.5, 4.8, 3.8, 4.0],
        "employment_index": [99, 100, 96, 97, 100, 102],
        "community": "Hospitality, retail and service workers",
        "story": (
            "Workers in customer-facing sectors could face sudden closures, "
            "reduced hours and uncertainty about their next pay cheque."
        ),
    },
    "The Gambia": {
        "unemployment_rate": [8.5, 8.6, 9.5, 9.1, 8.7, 8.4],
        "employment_index": [98, 100, 93, 95, 98, 101],
        "community": "Tourism, transport and informal traders",
        "story": (
            "A fall in visitor activity and interruptions to local trade "
            "could affect people whose income depends on daily transactions."
        ),
    },
    "Guinea-Bissau": {
        "unemployment_rate": [6.7, 6.8, 7.5, 7.2, 6.9, 6.7],
        "employment_index": [98, 100, 94, 96, 99, 101],
        "community": "Agriculture, market traders and small producers",
        "story": (
            "Disruptions to transport and markets can affect the ability "
            "to sell goods, even when a person remains economically active."
        ),
    },
    "Japan": {
        "unemployment_rate": [2.4, 2.4, 2.8, 2.8, 2.6, 2.6],
        "employment_index": [99, 100, 98, 99, 101, 102],
        "community": "Retail, hospitality and older workers",
        "story": (
            "A relatively small change in the headline unemployment rate "
            "can coexist with reduced hours or weaker earnings for some."
        ),
    },
    "Lesotho": {
        "unemployment_rate": [23.5, 23.6, 25.0, 24.5, 23.9, 23.4],
        "employment_index": [98, 100, 91, 94, 98, 100],
        "community": "Garment workers and cross-border earners",
        "story": (
            "Disrupted production and cross-border movement can put "
            "pressure on jobs and household income in connected communities."
        ),
    },
    "East Timor": {
        "unemployment_rate": [4.8, 4.9, 5.8, 5.5, 5.1, 4.9],
        "employment_index": [98, 100, 94, 96, 99, 101],
        "community": "Small businesses, agriculture and tourism",
        "story": (
            "When travel and local commerce slow down, people may need "
            "to combine different income sources to support their families."
        ),
    },
    "United States": {
        "unemployment_rate": [3.9, 3.7, 8.1, 5.3, 3.6, 3.6],
        "employment_index": [99, 100, 91, 95, 99, 102],
        "community": "Service workers, hourly employees and families",
        "story": (
            "Sudden layoffs affected many households, while reopening "
            "brought jobs back at different speeds across sectors."
        ),
    },
}

COUNTRIES = list(COUNTRY_DATA.keys())

# Consistent colours for all countries.
PALETTE = [
    "#64E5FF", "#79E2B3", "#A99BFF", "#FF806E", "#FFBD69",
    "#F08BC5", "#8CB8FF", "#B5D878", "#65D7C5", "#E8A5FF",
]

COLORS = dict(zip(COUNTRIES, PALETTE))

BG = "#0B1020"
TEXT = "#F4F7FF"
MUTED = "#A7B2C8"


def base_figure(fig, height=380):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Plus Jakarta Sans, sans-serif",
            color=TEXT,
            size=12,
        ),
        height=height,
        margin=dict(l=14, r=22, t=25, b=22),
        hoverlabel=dict(
            bgcolor="#1C2940",
            bordercolor="#354663",
            font_color=TEXT,
        ),
        transition=dict(duration=350, easing="cubic-in-out"),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#26344C",
        tickfont=dict(color=MUTED),
    )
    fig.update_yaxes(
        gridcolor="rgba(167,178,200,0.12)",
        zeroline=False,
        tickfont=dict(color=MUTED),
    )
    return fig


def unemployment_chart(selected):
    fig = go.Figure()

    for country in selected:
        values = COUNTRY_DATA[country]["unemployment_rate"]
        fig.add_trace(go.Scatter(
            x=YEARS,
            y=values,
            name=country,
            mode="lines+markers",
            line=dict(color=COLORS[country], width=2.6, shape="spline"),
            marker=dict(size=5),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "%{x}: %{y:.1f}%<extra></extra>"
            ),
        ))

    fig.add_vline(
        x=2020,
        line_dash="dot",
        line_color="rgba(255,128,110,0.75)",
        annotation_text="Pandemic shock",
        annotation_font_color="#FFB1A5",
    )
    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=YEARS),
        yaxis_title="Illustrative unemployment rate (%)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
        ),
    )
    return base_figure(fig)


def employment_index_chart(selected):
    fig = go.Figure()

    for country in selected:
        values = COUNTRY_DATA[country]["employment_index"]
        fig.add_trace(go.Scatter(
            x=YEARS,
            y=values,
            name=country,
            mode="lines+markers",
            line=dict(color=COLORS[country], width=2.6, shape="spline"),
            marker=dict(size=5),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "%{x}: index %{y:.1f}<extra></extra>"
            ),
        ))

    fig.add_hline(
        y=100,
        line_dash="dash",
        line_color="rgba(255,255,255,0.55)",
        annotation_text="2019 baseline",
        annotation_font_color=MUTED,
    )
    fig.add_vline(
        x=2020,
        line_dash="dot",
        line_color="rgba(255,128,110,0.75)",
    )
    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=YEARS),
        yaxis_title="Illustrative employment index (2019 = 100)",
    )
    return base_figure(fig)


def country_snapshot(year):
    index = YEARS.index(year)
    rows = sorted(
        [
            (
                country,
                COUNTRY_DATA[country]["unemployment_rate"][index],
            )
            for country in COUNTRIES
        ],
        key=lambda item: item[1],
    )

    fig = go.Figure(go.Bar(
        x=[row[1] for row in rows],
        y=[row[0] for row in rows],
        orientation="h",
        marker_color=[
            COLORS[row[0]] for row in rows
        ],
        text=[f"{row[1]:.1f}%" for row in rows],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        showlegend=False,
        xaxis_title="Illustrative unemployment rate (%)",
        yaxis_title=None,
    )
    return base_figure(fig, height=510)


def country_card(country):
    data = COUNTRY_DATA[country]

    return html.Div([
        html.Div([
            html.Span(
                country,
                className="employment-country-name",
            ),
            html.Span(
                data["community"],
                className="employment-community-label",
            ),
        ], className="employment-country-header"),
        html.P(data["story"], className="employment-country-story"),
    ], className="employment-country-card")


# ============================================================
# PAGE LAYOUT
# ============================================================

layout = html.Div(
    id="employment-story",
    className="economic-story employment-story",
    children=[

        # CHAPTER 3 CINEMATIC INTRO
        html.Div(
            [
                html.Div(className="cinematic-backdrop"),
                html.Div(className="cinematic-scanline"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span(className="cinematic-spark"),
                                html.Span(
                                    className="cinematic-spark spark-two"
                                ),
                                html.Span(
                                    className="cinematic-spark spark-three"
                                ),
                            ],
                            className="cinematic-particles",
                        ),
                        html.P(
                            "PEOPLE · WORK · LIVELIHOODS",
                            className="cinematic-eyebrow",
                        ),
                        html.Div(
                            "03",
                            className="cinematic-giant-number",
                            **{"aria-hidden": "true"},
                        ),
                        html.H2(
                            "CHAPTER 03",
                            className="cinematic-chapter-label",
                        ),
                        html.H1(
                            [
                                html.Span(
                                    "Livelihoods",
                                    className="cinematic-title-line",
                                ),
                                html.Span(
                                    "on the line.",
                                    className=(
                                        "cinematic-title-line "
                                        "cinematic-title-accent"
                                    ),
                                ),
                            ],
                            className="cinematic-title",
                        ),
                        html.P(
                            "Behind every statistic, a life was changing.",
                            className="cinematic-subtitle",
                        ),
                        html.Div(
                            className="cinematic-light-streak",
                            **{"aria-hidden": "true"},
                        ),
                    ],
                    className="cinematic-content",
                ),
            ],
            id="employment-chapter-intro",
            className="chapter-intro-overlay",
            **{
                "aria-label": "Chapter 3: Livelihoods on the line",
            },
        ),

        html.Div(
            html.Div(id="employment-progress-fill"),
            className="employment-progress-track",
            **{"aria-hidden": "true"},
        ),

        # OPENING
        html.Section([
            html.Div([
                html.P(
                    "CHAPTER 03 · PEOPLE BEHIND THE NUMBERS",
                    className="employment-kicker",
                ),
                html.H1([
                    html.Span("Livelihoods", className="employment-title-line"),
                    html.Span(
                        "on the line.",
                        className="employment-title-line employment-title-accent",
                    ),
                ], className="employment-hero-title"),
                html.P(
                    "A job is more than a number. It can mean rent paid, "
                    "food on the table, a child's school fees, or the "
                    "ability to help an entire family. When COVID-19 "
                    "disrupted work, its impact reached far beyond the workplace.",
                    className="employment-hero-description",
                ),
                html.Div([
                    html.Span(className="employment-live-dot"),
                    html.Span(
                        "10 COUNTRIES · ONE GLOBAL SHOCK",
                        className="employment-scroll-label",
                    ),
                    html.Span("↓", className="employment-scroll-arrow"),
                ], className="employment-scroll-cue"),
            ], className="employment-container employment-hero-content"),
            html.Div(className="employment-hero-glow"),
        ], className="employment-hero"),

        html.Div([
            html.Strong("IMPORTANT · MOCK DATA"),
            html.P(
                "Every numerical value on this page is illustrative and "
                "has been created for layout and interaction testing. "
                "Country stories are hypotheses to investigate, not "
                "verified findings. Replace all values with sourced "
                "observations and validate the comparisons before presenting."
            ),
        ], className="employment-container employment-data-note reveal"),

        # ACT 1 — THE HUMAN SHOCK
        html.Section([
            html.Div([
                html.Div([
                    html.Span("01", className="employment-act-number"),
                    html.Div([
                        html.P("THE HUMAN SHOCK", className="employment-kicker"),
                        html.H2(
                            "When work disappeared, uncertainty moved home.",
                            className="employment-section-title",
                        ),
                        html.P(
                            "The pandemic changed not just whether people "
                            "worked, but how much they earned, how securely "
                            "they were employed, and how they supported others.",
                            className="employment-section-description",
                        ),
                    ]),
                ], className="employment-section-header"),

                html.Div([
                    html.Div([
                        html.P("FOLLOW THE SHOCK", className="employment-mini-label"),
                        html.H3(
                            "Unemployment did not move the same way everywhere.",
                            className="employment-panel-title",
                        ),
                        html.P(
                            "Select countries to compare the illustrative "
                            "unemployment trajectory before, during and after "
                            "the initial pandemic shock.",
                            className="employment-panel-description",
                        ),
                        dcc.Checklist(
                            id="employment-country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in COUNTRIES
                            ],
                            value=[
                                "United States",
                                "Germany",
                                "China",
                                "The Gambia",
                            ],
                            inline=True,
                            className="employment-country-filter",
                            labelClassName="employment-filter-chip",
                        ),
                        dcc.Graph(
                            id="employment-unemployment-chart",
                            figure=unemployment_chart([
                                "United States",
                                "Germany",
                                "China",
                                "The Gambia",
                            ]),
                            config={"displayModeBar": False, "responsive": True},
                        ),
                        html.P(
                            "Illustrative annual unemployment rates (%)",
                            className="employment-chart-footnote",
                        ),
                    ], className="employment-panel"),
                ]),
            ], className="employment-container"),
        ], className="employment-section reveal"),

        # ACT 2 — THE MAP OF DIFFERENT EXPERIENCES
        html.Section([
            html.Div([
                html.Div([
                    html.Span("02", className="employment-act-number"),
                    html.Div([
                        html.P("TEN COUNTRIES · DIFFERENT REALITIES", className="employment-kicker"),
                        html.H2(
                            "There was no single story of work.",
                            className="employment-section-title",
                        ),
                        html.P(
                            "A national rate can hide the experience of a "
                            "market trader, a factory worker, a hospitality "
                            "employee or a family relying on seasonal income. "
                            "Explore the communities this analysis will investigate.",
                            className="employment-section-description",
                        ),
                    ]),
                ], className="employment-section-header"),

                html.Div(
                    [country_card(country) for country in COUNTRIES],
                    className="employment-country-grid",
                ),
            ], className="employment-container"),
        ], className="employment-section employment-section-alt reveal"),

        # ACT 3 — EMPLOYMENT LEVELS
        html.Section([
            html.Div([
                html.Div([
                    html.Span("03", className="employment-act-number"),
                    html.Div([
                        html.P("THE ROAD BACK", className="employment-kicker"),
                        html.H2(
                            "A recovering economy does not guarantee a recovered livelihood.",
                            className="employment-section-title",
                        ),
                        html.P(
                            "A job count can recover while hours, pay, security "
                            "or the quality of work remain different. The index "
                            "below is designed to distinguish the employment "
                            "level from the unemployment rate.",
                            className="employment-section-description",
                        ),
                    ]),
                ], className="employment-section-header"),

                html.Div([
                    html.P("COMPARE EMPLOYMENT LEVELS", className="employment-mini-label"),
                    html.H3(
                        "How far did employment fall — and how far did it return?",
                        className="employment-panel-title",
                    ),
                    dcc.Checklist(
                        id="employment-index-filter",
                        options=[
                            {"label": country, "value": country}
                            for country in COUNTRIES
                        ],
                        value=[
                            "United States",
                            "United Kingdom",
                            "Japan",
                            "Lesotho",
                        ],
                        inline=True,
                        className="employment-country-filter",
                        labelClassName="employment-filter-chip",
                    ),
                    dcc.Graph(
                        id="employment-index-chart",
                        figure=employment_index_chart([
                            "United States",
                            "United Kingdom",
                            "Japan",
                            "Lesotho",
                        ]),
                        config={"displayModeBar": False, "responsive": True},
                    ),
                    html.P(
                        "Illustrative employment index · 2019 = 100",
                        className="employment-chart-footnote",
                    ),
                ], className="employment-panel"),

                html.Div([
                    html.Div([
                        html.Span("01", className="employment-insight-number"),
                        html.Div([
                            html.H3("The shock"),
                            html.P(
                                "Identify the lowest point and compare how "
                                "deeply the employment index falls."
                            ),
                        ]),
                    ], className="employment-insight-card"),
                    html.Div([
                        html.Span("02", className="employment-insight-number"),
                        html.Div([
                            html.H3("The rebound"),
                            html.P(
                                "See whether employment levels return to "
                                "their pre-pandemic reference."
                            ),
                        ]),
                    ], className="employment-insight-card"),
                    html.Div([
                        html.Span("03", className="employment-insight-number"),
                        html.Div([
                            html.H3("The missing story"),
                            html.P(
                                "Investigate job quality, working hours, "
                                "informality and household income where data "
                                "allow."
                            ),
                        ]),
                    ], className="employment-insight-card"),
                ], className="employment-insight-grid"),
            ], className="employment-container"),
        ], className="employment-section reveal"),

        # ACT 4 — SELECT A YEAR
        html.Section([
            html.Div([
                html.Div([
                    html.Span("04", className="employment-act-number"),
                    html.Div([
                        html.P("A YEAR AT A TIME", className="employment-kicker"),
                        html.H2(
                            "Which countries were under the greatest pressure?",
                            className="employment-section-title",
                        ),
                        html.P(
                            "Move through the timeline to compare the "
                            "illustrative unemployment rate across all ten "
                            "countries. This is a descriptive comparison, "
                            "not a ranking of national resilience.",
                            className="employment-section-description",
                        ),
                    ]),
                ], className="employment-section-header"),

                html.Div([
                    html.Div([
                        html.P("SELECT YEAR", className="employment-mini-label"),
                        html.Div("2020", id="employment-year-label",
                                 className="employment-year-label"),
                    ]),
                    dcc.Slider(
                        id="employment-year-slider",
                        min=2018,
                        max=2023,
                        step=1,
                        value=2020,
                        marks={
                            year: {
                                "label": str(year),
                                "style": {"color": "#A7B2C8"},
                            }
                            for year in YEARS
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": False,
                        },
                        className="employment-year-slider",
                    ),
                    dcc.Graph(
                        id="employment-year-chart",
                        figure=country_snapshot(2020),
                        config={"displayModeBar": False, "responsive": True},
                    ),
                ], className="employment-panel"),
            ], className="employment-container"),
        ], className="employment-section employment-section-alt reveal"),

        
        # CLOSING — CHAPTER 03 SUMMARY / TRANSITION TO RECOVERY
        html.Section(
            [
                html.Div(
                    [
                        html.P(
                            "CHAPTER 03 · THE HUMAN TAKEAWAY",
                            className="employment-kicker",
                        ),

                        html.H2(
                            [
                                html.Span(
                                    "A job returning",
                                    className="employment-title-line",
                                ),
                                html.Span(
                                    "is not the whole recovery.",
                                    className=(
                                        "employment-title-line "
                                        "employment-title-accent"
                                    ),
                                ),
                            ],
                            className="employment-closing-title",
                        ),

                        html.P(
                            "Employment figures can climb back toward normal "
                            "while families are still rebuilding their savings, "
                            "workers are accepting fewer hours, and entire "
                            "communities are finding their footing again. "
                            "The numbers may signal a rebound. The human story "
                            "asks whether people have truly recovered.",
                            className="employment-closing-description",
                        ),

                        # Three questions that lead into the recovery chapter.
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "01",
                                            className="closing-number",
                                        ),
                                        html.P("Did jobs return?"),
                                    ],
                                    className="closing-step",
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "02",
                                            className="closing-number",
                                        ),
                                        html.P("Did livelihoods recover?"),
                                    ],
                                    className="closing-step",
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "03",
                                            className="closing-number",
                                        ),
                                        html.P("Who was left behind?"),
                                    ],
                                    className="closing-step",
                                ),
                            ],
                            className="closing-steps",
                        ),

                        # Transition card to Chapter 04: Recovery.
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "NEXT CHAPTER",
                                            className="transition-eyebrow",
                                        ),
                                        html.Span(
                                            "04",
                                            className="transition-number",
                                        ),
                                    ],
                                    className="transition-topline",
                                ),

                                html.H3(
                                    "The numbers began to heal. Did the world?",
                                    className="transition-title",
                                ),

                                html.P(
                                    "The shock reshaped economies. The "
                                    "employment crisis reshaped lives. Now, "
                                    "we follow the road beyond the crisis: "
                                    "which economies bounced back, how quickly "
                                    "they recovered, and what the headline "
                                    "figures may still leave unseen.",
                                    className="transition-description",
                                ),

                                dcc.Link(
                                    [
                                        html.Span(
                                            "Continue to Recovery",
                                            className="transition-button-text",
                                        ),
                                        html.Span(
                                            "→",
                                            className="transition-button-arrow",
                                        ),
                                    ],
                                    href="/recovery",
                                    className="transition-button",
                                ),
                            ],
                            className="chapter-transition",
                        ),
                    ],
                    className="employment-container employment-closing-inner",
                ),
            ],
            className="employment-closing reveal",
        ),
    ],
)


# ============================================================
# CALLBACKS
# Unique component IDs avoid conflicts with Chapters 1 and 2.
# ============================================================

@callback(
    Output("employment-unemployment-chart", "figure"),
    Input("employment-country-filter", "value"),
)
def update_employment_unemployment(selected):
    return unemployment_chart(selected or [])


@callback(
    Output("employment-index-chart", "figure"),
    Input("employment-index-filter", "value"),
)
def update_employment_index(selected):
    return employment_index_chart(selected or [])


@callback(
    Output("employment-year-label", "children"),
    Output("employment-year-chart", "figure"),
    Input("employment-year-slider", "value"),
)
def update_employment_snapshot(year):
    year = int(year or 2020)
    return str(year), country_snapshot(year)
