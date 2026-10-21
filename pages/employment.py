# pages/employment.py — PandemiScope Chapter 3
# Real unemployment data; cinematic page layout preserved.

from pathlib import Path

from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.graph_objects as go

from src.visualizations import (
    plot_unemployment,
    plot_unemployment_change_2020,
    plot_unemployment_vs_2019,
    COLORS as DATA_COLORS,
)

# Locate the same project dataset used by app.py and the other chapters.
# Your current project stores final_dataset.csv beside app.py.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_CANDIDATES = [
    PROJECT_ROOT / "final_dataset.csv",
    PROJECT_ROOT / "data" / "processed" / "final_dataset.csv",
]
DATA_PATH = next((candidate for candidate in DATA_CANDIDATES if candidate.is_file()), None)

if DATA_PATH is None:
    searched = "\\n".join(str(candidate) for candidate in DATA_CANDIDATES)
    raise FileNotFoundError(
        "Could not find final_dataset.csv. Checked these locations:\\n"
        f"{searched}\\n"
        "Place final_dataset.csv beside app.py or in data/processed/."
    )

print(f"Employment page: loading dataset from {DATA_PATH}")
df = pd.read_csv(DATA_PATH).dropna(subset=["country"]).copy()
df["year"] = pd.to_numeric(df["year"], errors="coerce")
YEARS = sorted(df["year"].dropna().astype(int).unique().tolist())
COUNTRIES = sorted(df["country"].dropna().unique().tolist())
DEFAULT_UNEMPLOYMENT = [
    c for c in ["United States", "United Kingdom", "China", "Lesotho"]
    if c in COUNTRIES
]
DEFAULT_RECOVERY = [
    c for c in ["United States", "United Kingdom", "Lesotho", "Gambia"]
    if c in COUNTRIES
]
COLORS = DATA_COLORS
BG = "#0B1020"
TEXT = "#F4F7FF"
MUTED = "#A7B2C8"

# The text below is illustrative context about potentially affected communities,
# not an observed country-level finding of the dataset.
COUNTRY_CONTEXT = {'Central African Republic': {'community': 'Informal work and small-scale livelihoods',
                              'story': 'For households relying on informal trade and daily earnings, '
                                       'movement restrictions and disrupted markets could make '
                                       'earning a living more uncertain.'},
 'China': {'community': 'Manufacturing and urban service workers',
           'story': 'Factory interruptions and changes in consumer demand could affect workers '
                    'differently from those able to work remotely.'},
 'Germany': {'community': 'Industrial workers and small businesses',
             'story': 'Support measures and reduced working hours can shape the difference between '
                      'keeping a job and losing working income.'},
 'United Kingdom': {'community': 'Hospitality, retail and service workers',
                    'story': 'Workers in customer-facing sectors could face sudden closures, reduced '
                             'hours and uncertainty about their next pay cheque.'},
 'Gambia': {'community': 'Tourism, transport and informal traders',
            'story': 'A fall in visitor activity and interruptions to local trade could affect people '
                     'whose income depends on daily transactions.'},
 'Guinea-Bissau': {'community': 'Agriculture, market traders and small producers',
                   'story': 'Disruptions to transport and markets can affect the ability to sell '
                            'goods, even when a person remains economically active.'},
 'Japan': {'community': 'Retail, hospitality and older workers',
           'story': 'A relatively small change in the headline unemployment rate can coexist with '
                    'reduced hours or weaker earnings for some.'},
 'Lesotho': {'community': 'Garment workers and cross-border earners',
             'story': 'Disrupted production and cross-border movement can put pressure on jobs and '
                      'household income in connected communities.'},
 'East Timor': {'community': 'Small businesses, agriculture and tourism',
                'story': 'When travel and local commerce slow down, people may need to combine '
                         'different income sources to support their families.'},
 'United States': {'community': 'Service workers, hourly employees and families',
                   'story': 'Sudden layoffs affected many households, while reopening brought jobs '
                            'back at different speeds across sectors.'}}


def real_figure_style(fig, height=550, horizontal=False):
    """Adapt the existing Plotly charts to the full-width dark story panels."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Plus Jakarta Sans, sans-serif", color=TEXT, size=12),
        title=None,
        height=height,
        autosize=True,
        margin=dict(l=188 if horizontal else 70, r=85 if horizontal else 40, t=30, b=85),
        hoverlabel=dict(bgcolor="#1C2940", bordercolor="#354663", font_color=TEXT),
        legend=dict(orientation="h", y=-0.18, x=0, xanchor="left"),
    )
    fig.update_xaxes(tickfont=dict(color=MUTED), gridcolor="rgba(167,178,200,0.12)")
    fig.update_yaxes(tickfont=dict(color=MUTED), gridcolor="rgba(167,178,200,0.12)")
    return fig


def unemployment_chart(selected):
    chosen = [c for c in (selected or []) if c in COUNTRIES]
    fig = plot_unemployment(df, countries=chosen)
    return real_figure_style(fig, height=540)


def unemployment_vs_2019_chart(selected):
    chosen = [c for c in (selected or []) if c in COUNTRIES]
    fig = plot_unemployment_vs_2019(df, countries=chosen)
    return real_figure_style(fig, height=540)


def unemployment_shock_chart():
    fig = plot_unemployment_change_2020(df)
    return real_figure_style(fig, height=650, horizontal=True)


def country_snapshot(year):
    """Actual unemployment rates in the selected year, not mock figures."""
    year_data = (df.loc[df["year"] == year, ["country", "wb_unemployment_rate"]]
                 .dropna().drop_duplicates("country")
                 .sort_values("wb_unemployment_rate"))
    fig = go.Figure(go.Bar(
        x=year_data["wb_unemployment_rate"],
        y=year_data["country"],
        orientation="h",
        marker_color=[COLORS.get(country, "#64E5FF") for country in year_data["country"]],
        text=[f"{v:.1f}%" for v in year_data["wb_unemployment_rate"]],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
    ))
    fig.update_layout(showlegend=False, xaxis_title="Unemployment rate (% of labor force)",
                      yaxis_title=None)
    return real_figure_style(fig, height=615, horizontal=True)


def country_card(country):
    context = COUNTRY_CONTEXT.get(country, {
        "community": "National labor market",
        "story": "Consider which communities may experience changes not visible in a national rate."
    })
    rate = (df.loc[(df["country"] == country) & (df["year"] == 2020),
                   "wb_unemployment_rate"].dropna())
    rate_caption = f"2020 unemployment rate: {rate.iloc[0]:.1f}%" if not rate.empty else "2020 rate unavailable"
    return html.Div([
        html.Div([
            html.Span(country, className="employment-country-name"),
            html.Span(context["community"], className="employment-community-label"),
        ], className="employment-country-header"),
        html.P(rate_caption, className="employment-observed-rate"),
        html.P(context["story"], className="employment-country-story"),
    ], className="employment-country-card")


# ============================================================
# PAGE LAYOUT — original page structure and CSS classes retained
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
            html.Strong("DATA SOURCE & LIMITATIONS"),
            html.P(
                "Charts and 2020 unemployment rates use the cleaned project dataset "
                "(World Bank unemployment indicator). The community descriptions "
                "are illustrative scenarios, not verified findings. National "
                "unemployment rates do not capture changes in hours or income; "
                "these comparisons do not establish causation."
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
                            "Select countries to compare measured annual unemployment "
                            "rates before, during and after the initial pandemic shock.",
                            className="employment-panel-description",
                        ),
                        dcc.Checklist(
                            id="employment-country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in COUNTRIES
                            ],
                            value=DEFAULT_UNEMPLOYMENT,
                            inline=True,
                            className="employment-country-filter",
                            labelClassName="employment-filter-chip",
                        ),
                        dcc.Graph(
                            id="employment-unemployment-chart",
                            className="employment-real-graph",
                            style={"height": "540px", "width": "100%"},
                            figure=unemployment_chart(DEFAULT_UNEMPLOYMENT),
                            config={"displayModeBar": False, "responsive": True},
                        ),
                        html.P(
                            "World Bank annual unemployment rate (% of labor force) · 2018–2024",
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
                            "These cards combine observed national unemployment rates in "
                            "2020 with examples of communities that might be affected. "
                            "The community descriptions are illustrative, not "
                            "country-specific research findings.",
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
                            "An unemployment rate can return to its 2019 level while "
                            "working hours, income or job quality remain changed. "
                            "The chart compares each country with its own 2019 rate.",
                            className="employment-section-description",
                        ),
                    ]),
                ], className="employment-section-header"),

                html.Div([
                    html.P("COMPARE WITH 2019", className="employment-mini-label"),
                    html.H3(
                        "Did unemployment return to its 2019 rate?",
                        className="employment-panel-title",
                    ),
                    dcc.Checklist(
                        id="employment-index-filter",
                        options=[
                            {"label": country, "value": country}
                            for country in COUNTRIES
                        ],
                        value=DEFAULT_RECOVERY,
                        inline=True,
                        className="employment-country-filter",
                        labelClassName="employment-filter-chip",
                    ),
                    dcc.Graph(
                        id="employment-index-chart",
                            className="employment-real-graph",
                            style={"height": "540px", "width": "100%"},
                        figure=unemployment_vs_2019_chart(DEFAULT_RECOVERY),
                        config={"displayModeBar": False, "responsive": True},
                    ),
                    html.P(
                        "Change in unemployment rate relative to 2019 · percentage points (pp)",
                        className="employment-chart-footnote",
                    ),
                ], className="employment-panel"),

                html.Div([
                    html.Div([
                        html.Span("01", className="employment-insight-number"),
                        html.Div([
                            html.H3("The shock"),
                            html.P(
                                "Identify when unemployment rose above the 2019 baseline "
                                "and by how many percentage points."
                            ),
                        ]),
                    ], className="employment-insight-card"),
                    html.Div([
                        html.Span("02", className="employment-insight-number"),
                        html.Div([
                            html.H3("The rebound"),
                            html.P(
                                "See whether unemployment returns to its country's "
                                "pre-pandemic rate (zero line)."
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
                            "First compare the unemployment-rate change in 2020. "
                            "Then move through the years to compare measured "
                            "unemployment rates across all ten countries. "
                            "Neither chart is a causal estimate.",
                            className="employment-section-description",
                        ),
                    ]),
                ], className="employment-section-header"),

                html.Div([
                    html.P("THE INITIAL SHOCK · 2019 TO 2020", className="employment-mini-label"),
                    html.H3("Which unemployment rates changed most in 2020?",
                            className="employment-panel-title"),
                    html.P("Difference between 2020 and 2019 unemployment rates, "
                           "measured in percentage points.",
                           className="employment-panel-description"),
                    dcc.Graph(
                        id="employment-2020-change-chart",
                        figure=unemployment_shock_chart(),
                        config={"displayModeBar": False, "responsive": True},
                        className="employment-real-graph",
                        style={"height": "650px", "width": "100%"},
                    ),
                    html.Div(className="employment-chart-divider"),
                    html.Div([
                        html.P("SELECT YEAR", className="employment-mini-label"),
                        html.Div("2020", id="employment-year-label",
                                 className="employment-year-label"),
                    ]),
                    dcc.Slider(
                        id="employment-year-slider",
                        min=min(YEARS),
                        max=max(YEARS),
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
                            className="employment-real-graph",
                            style={"height": "615px", "width": "100%"},
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
                            "The unemployment rate measures one part of the labor market. "
                            "Even when it returns toward its 2019 value, it "
                            "does not tell us whether wages, hours or job security "
                            "have recovered. Our country comparisons help frame "
                            "questions the available data cannot resolve.",
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
    return unemployment_vs_2019_chart(selected or [])


@callback(
    Output("employment-year-label", "children"),
    Output("employment-year-chart", "figure"),
    Input("employment-year-slider", "value"),
)
def update_employment_snapshot(year):
    year = int(year or 2020)
    return str(year), country_snapshot(year)
