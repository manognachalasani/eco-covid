
# pages/economic_impact.py

from pathlib import Path

from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd

from src.visualizations import (
    COLORS,
    plot_gdp_growth,
    plot_gdp_shock_2020,
    plot_inflation,
)

# Real project dataset. Change this path if your processed CSV has a different name.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "final_dataset.csv"
if not DATA_PATH.is_file():
    raise FileNotFoundError(
        f"Processed dataset not found: {DATA_PATH}. "
        "Update DATA_PATH in pages/economic_impact.py to your actual CSV."
    )

df = pd.read_csv(DATA_PATH).dropna(subset=["country"])
df["year"] = pd.to_numeric(df["year"], errors="coerce")

YEARS = list(range(2015, 2025))
COUNTRIES = sorted(df["country"].unique().tolist())
DEFAULT_COUNTRIES = [
    country for country in ["United Kingdom", "United States", "China", "Lesotho"]
    if country in COUNTRIES
]


def growth_2020(country):
    values = df.loc[
        (df["country"] == country) & (df["year"] == 2020),
        "wb_gdp_growth",
    ].dropna()
    return f"{values.iloc[0]:+.1f}%" if not values.empty else "N/A"


# ============================================================
# THEME
# ============================================================

BG = "#0B1020"
PANEL = "#121A2D"
TEXT = "#F4F7FF"
MUTED = "#A7B2C8"
CYAN = "#64E5FF"
CORAL = "#FF806E"
PURPLE = "#A99BFF"
GREEN = "#79E2B3"

COUNTRY_COLORS = COLORS

CHART_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "scrollZoom": False,
}


def base_figure(fig, height=360):
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
        margin=dict(l=12, r=18, t=25, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor="#1C2940",
            bordercolor="#354663",
            font_color=TEXT,
        ),
        transition=dict(duration=450, easing="cubic-in-out"),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#26344C",
        tickfont=dict(color=MUTED),
    )
    fig.update_yaxes(
        gridcolor="rgba(167,178,200,0.12)",
        zerolinecolor="rgba(167,178,200,0.3)",
        tickfont=dict(color=MUTED),
    )
    return fig


def real_chart_style(fig, height=None):
    """Adapt the real Plotly figures to the page's dark cinematic theme."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Plus Jakarta Sans, sans-serif", color=TEXT, size=12),
        title=None,
        hoverlabel=dict(bgcolor="#1C2940", font_color=TEXT),
    )
    if height is not None:
        fig.update_layout(height=height)
    fig.update_xaxes(tickfont=dict(color=MUTED), gridcolor="rgba(167,178,200,0.12)")
    fig.update_yaxes(tickfont=dict(color=MUTED), gridcolor="rgba(167,178,200,0.12)")
    return fig


def growth_line(selected_regions):
    countries = [country for country in (selected_regions or []) if country in COUNTRIES]
    fig = plot_gdp_growth(df, countries=countries)
    # The original design uses a half-width card; 2x2 small multiples fit four countries.
    nrows = max(1, (len(countries) + 1) // 2)
    fig = real_chart_style(fig, height=max(540, 290 * nrows + 125))
    fig.update_layout(margin=dict(l=65, r=35, t=90, b=65))
    return fig


def year_snapshot(year):
    """Real annual GDP growth comparison for the selected year."""
    data = df.loc[df["year"] == year, ["country", "wb_gdp_growth"]].dropna()
    data = data.drop_duplicates("country").sort_values("wb_gdp_growth")
    fig = go.Figure(go.Bar(
        x=data["wb_gdp_growth"],
        y=data["country"],
        orientation="h",
        marker_color=[COUNTRY_COLORS.get(c, CYAN) for c in data["country"]],
        text=[f"{v:+.1f}%" for v in data["wb_gdp_growth"]],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
    ))
    fig.add_vline(x=0, line_color="rgba(255,255,255,0.4)")
    fig = real_chart_style(fig, height=540)
    fig.update_layout(
        showlegend=False,
        xaxis_title="Annual real GDP growth (%)",
        yaxis_title=None,
        margin=dict(l=190, r=65, t=35, b=55),
    )
    return fig


def gdp_shock_chart():
    fig = plot_gdp_shock_2020(df)
    fig = real_chart_style(fig, height=660)
    fig.update_layout(margin=dict(l=190, r=35, t=50, b=65))
    return fig


def inflation_chart():
    fig = plot_inflation(df)
    fig = real_chart_style(fig, height=700)
    fig.update_layout(margin=dict(l=190, r=35, t=55, b=70))
    return fig


# ============================================================
# REUSABLE PAGE COMPONENTS
# ============================================================

def story_section(number, eyebrow, title, description, content,
                  section_id=None, extra_class=""):
    return html.Section(
        html.Div([
            html.Div([
                html.Span(number, className="story-number"),
                html.Div([
                    html.P(eyebrow, className="story-eyebrow"),
                    html.H2(title, className="story-heading"),
                    html.P(description, className="story-description"),
                ], className="story-heading-copy"),
            ], className="story-section-header"),
            content,
        ], className="story-container"),
        id=section_id,
        className=f"story-section reveal {extra_class}",
    )


def metric(label, value, detail, accent="cyan"):
    return html.Div([
        html.P(label, className="metric-label"),
        html.Div(value, className=f"metric-value accent-{accent}"),
        html.P(detail, className="metric-detail"),
    ], className="story-metric")


def panel(children, extra_class=""):
    return html.Div(children, className=f"story-panel {extra_class}")


# ============================================================
# PAGE LAYOUT
# Layout fixes for large Plotly plots live in assets/economic_impact_fix.css.
# ============================================================

layout = html.Div(
    id="economic-story",
    className="economic-story",

    children=[

        
# CINEMATIC CHAPTER TRANSITION
html.Div(
    [
        html.Div(className="cinematic-backdrop"),
        html.Div(className="cinematic-scanline"),

        html.Div(
            [
                html.Div(
                    [
                        html.Span(className="cinematic-spark"),
                        html.Span(className="cinematic-spark spark-two"),
                        html.Span(className="cinematic-spark spark-three"),
                    ],
                    className="cinematic-particles",
                ),

                html.P(
                    "THE GLOBAL ECONOMY · 2020",
                    className="cinematic-eyebrow",
                ),

                html.Div(
                    "02",
                    className="cinematic-giant-number",
                    **{"aria-hidden": "true"},
                ),

                html.H2(
                    "CHAPTER 02",
                    className="cinematic-chapter-label",
                ),

                html.H1(
                    [
                        html.Span("Economy brought", className="cinematic-title-line"),
                        html.Span("to a halt.", className="cinematic-title-line cinematic-title-accent"),
                    ],
                    className="cinematic-title",
                ),

                html.P(
                    "The world stopped. The economic shock began.",
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
    id="chapter-intro-overlay",
    className="chapter-intro-overlay",
    **{"aria-label": "Chapter 2: Economy brought to a halt"},
),


        # A persistent, scoped progress line is animated by page JS.
        html.Div(
            html.Div(id="story-progress-fill"),
            className="story-progress-track",
            **{"aria-hidden": "true"},
        ),

        # CHAPTER INTRO
        html.Section([
            html.Div([
                html.Div(
                    "ECONOMIC IMPACT  /  CHAPTER 02",
                    className="chapter-kicker",
                ),
                html.Div(
                    "2020",
                    className="chapter-year",
                    **{"aria-hidden": "true"},
                ),
                html.H1([
                    html.Span("Economy brought", className="title-line"),
                    html.Span("to a halt.", className="title-line title-accent"),
                ], className="chapter-title"),
                html.P(
                    "When the world stopped moving, its economies "
                    "felt the shock. But not every country fell in "
                    "the same way — and recovery would not be equal.",
                    className="chapter-intro",
                ),
                html.Div([
                    html.Span(className="intro-dot"),
                    html.Span("THE GLOBAL SHOCK", className="intro-label"),
                    html.Span("↓", className="intro-arrow"),
                    html.Span("SCROLL TO EXPLORE", className="intro-label"),
                ], className="chapter-scroll-cue"),
            ], className="chapter-inner"),
            html.Div(className="chapter-orb orb-one"),
            html.Div(className="chapter-orb orb-two"),
            html.Div(className="chapter-grid"),
        ], className="chapter-hero"),

        # EVIDENCE LABEL
        html.Div([
            html.Span("DATA NOTE", className="data-note-label"),
            html.P(
                "Figures use the project's cleaned dataset and World Bank "
                "GDP growth and inflation indicators. Comparisons are "
                "descriptive; they do not establish COVID-19 causation.",
                className="data-note-text",
            ),
        ], className="story-container data-note reveal"),

        # ACT 1 — THE SHOCK
        story_section(
            "01",
            "THE SHOCK",
            "A sudden break in the global economy",
            "Lockdowns, disrupted supply chains, restricted travel and "
            "uncertainty collided. The annual numbers reveal the scale "
            "of the contraction — and the differences between economies.",
            html.Div([
                html.Div([
                    html.P("EXPLORE THE CONTRACTION", className="mini-eyebrow"),
                    html.H3("One crisis. Different trajectories.", className="panel-title"),
                    html.P(
                        "Choose the economies you want to compare. "
                        "Each panel shows annual real GDP growth from the dataset.",
                        className="panel-description",
                    ),
                    dcc.Checklist(
                        id="growth-region-filter",
                        options=[
                            {"label": r, "value": r}
                            for r in COUNTRIES
                        ],
                        value=DEFAULT_COUNTRIES,
                        inline=True,
                        className="story-checklist",
                        inputClassName="story-check-input",
                        labelClassName="story-check-label",
                    ),
                    dcc.Graph(
                        id="growth-line-chart",
                        figure=growth_line(DEFAULT_COUNTRIES),
                        config=CHART_CONFIG,
                        className="story-graph story-graph-auto",
                    ),
                    html.P(
                        "Source: cleaned project dataset · annual real GDP growth (%)",
                        className="chart-footnote",
                    ),
                ], className="story-panel chart-panel story-chart-panel-full"),

                html.Div([
                    html.P("THE CRISIS IN NUMBERS", className="mini-eyebrow"),
                    html.H3("The shock was not uniform.", className="panel-title"),
                    html.P(
                        "Observed annual real GDP growth rates in 2020, "
                        "taken from the project dataset.",
                        className="panel-description",
                    ),
                    html.Div([
                        metric(
                            "United Kingdom · 2020",
                            growth_2020("United Kingdom"),
                            "Real GDP growth",
                            "coral",
                        ),
                        metric(
                            "United States · 2020",
                            growth_2020("United States"),
                            "Real GDP growth",
                            "purple",
                        ),
                        metric(
                            "China · 2020",
                            growth_2020("China"),
                            "Real GDP growth",
                            "green",
                        ),
                    ], className="story-metrics"),
                    html.Div([
                        html.Span("KEY QUESTION", className="callout-label"),
                        html.P(
                            "Why did the same global emergency produce "
                            "different economic outcomes?",
                            className="callout-text",
                        ),
                    ], className="story-callout"),
                ], className="story-panel insight-panel"),
            ], className="story-two-column story-two-column-single"),
            section_id="the-shock",
        ),

        # ACT 2 — COUNTRY COMPARISON
        story_section(
            "02",
            "COUNTRY BY COUNTRY",
            "The world did not fall together",
            "National economies entered the crisis with different "
            "structures, restrictions and exposure to global demand. "
            "Move through the years to compare their annual growth rates.",
            html.Div([
                html.Div([
                    html.Div([
                        html.P("CHANGE THE YEAR", className="mini-eyebrow"),
                        html.Div("2020", id="snapshot-year-label",
                                 className="snapshot-year-label"),
                    ]),
                    dcc.Slider(
                        id="snapshot-year",
                        min=2015,
                        max=2024,
                        step=1,
                        value=2020,
                        marks={
                            y: {
                                "label": str(y),
                                "style": {"color": "#A7B2C8"},
                            }
                            for y in YEARS
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": False,
                        },
                        className="story-slider",
                    ),
                ], className="year-control"),
                dcc.Graph(
                    id="year-snapshot-chart",
                    figure=year_snapshot(2020),
                    config=CHART_CONFIG,
                    className="story-graph story-graph-auto",
                ),
                html.Div([
                    html.Div([
                        html.Span("01", className="insight-index"),
                        html.P("Compare the depth of the contraction."),
                    ], className="insight-step"),
                    html.Div([
                        html.Span("02", className="insight-index"),
                        html.P("Look for economies that continued to grow."),
                    ], className="insight-step"),
                    html.Div([
                        html.Span("03", className="insight-index"),
                        html.P(
                            "Compare 2020 with the pre-pandemic years."
                        ),
                    ], className="insight-step"),
                ], className="insight-steps"),
            ], className="story-panel chart-panel story-chart-panel-full"),
            section_id="country-comparison",
            extra_class="story-section-muted",
        ),

        # ACT 3 — GDP SHOCK VS. PRE-PANDEMIC BASELINE
        story_section(
            "03",
            "THE 2020 SHOCK",
            "How far did growth fall below normal?",
            "Annual growth in 2020 is compared with each country's average "
            "growth rate in 2015–2019. The difference is measured in "
            "percentage points, not as a percentage change.",
            html.Div([
                html.Div([
                    html.P("COMPARE THE SHOCK", className="mini-eyebrow"),
                    html.H3("One pandemic. Unequal economic shocks.", className="panel-title"),
                    html.P(
                        "A negative value means 2020 growth was below the "
                        "country's pre-pandemic average.",
                        className="panel-description",
                    ),
                    dcc.Graph(
                        id="gdp-shock-chart",
                        figure=gdp_shock_chart(),
                        config=CHART_CONFIG,
                        className="story-graph story-graph-auto",
                    ),
                    html.P(
                        "2020 GDP growth minus mean growth (2015–2019), in percentage points",
                        className="chart-footnote",
                    ),
                ], className="story-panel chart-panel story-chart-panel-full"),
                html.Div([
                    html.P("READ THE CHART", className="mini-eyebrow"),
                    html.H3("What does the shock measure?", className="panel-title"),
                    html.Div([
                        html.Span("01", className="explain-number"),
                        html.Div([
                            html.H4("Pre-pandemic baseline"),
                            html.P("Average annual real GDP growth from 2015 to 2019."),
                        ]),
                    ], className="explain-row"),
                    html.Div([
                        html.Span("02", className="explain-number"),
                        html.Div([
                            html.H4("Deviation in 2020"),
                            html.P("2020 growth minus the reference average, in percentage points."),
                        ]),
                    ], className="explain-row"),
                    html.Div([
                        html.Span("03", className="explain-number"),
                        html.Div([
                            html.H4("Interpretation"),
                            html.P(
                                "The deviation describes the shock; it does not "
                                "isolate the pandemic from other influences."
                            ),
                        ]),
                    ], className="explain-row"),
                ], className="story-panel explanation-panel"),
            ], className="story-two-column story-two-column-single"),
            section_id="the-rebound",
        ),

        # ACT 4 — INFLATION
        story_section(
            "04",
            "BEYOND GDP",
            "Inflation: the next economic challenge",
            "The 2020 GDP shock was followed by substantial changes in prices. "
            "Compare annual inflation in 2019 and 2022 across countries. "
            "Inflation in 2022 also reflects energy and other global shocks.",
            html.Div([
                html.Div([
                    html.P("COMPARE INFLATION", className="mini-eyebrow"),
                    html.H3("Price pressures diverged.", className="panel-title"),
                    html.P(
                        "The connected markers show inflation rates in 2019 "
                        "and 2022 for each country.",
                        className="panel-description",
                    ),
                    dcc.Graph(
                        id="inflation-comparison-chart",
                        figure=inflation_chart(),
                        config=CHART_CONFIG,
                        className="story-graph story-graph-auto",
                    ),
                    html.P(
                        "World Bank annual inflation (%) · 2019 versus 2022",
                        className="chart-footnote",
                    ),
                ], className="story-panel chart-panel story-chart-panel-full"),
                html.Div([
                    html.P("WHAT TO CONSIDER", className="mini-eyebrow"),
                    html.H3("Read inflation carefully.", className="panel-title"),
                    html.Div([
                        html.Span("A", className="sector-letter"),
                        html.Div([
                            html.H4("Price changes"),
                            html.P("Inflation measures the rate of price increases, not the price level."),
                        ]),
                    ], className="sector-question"),
                    html.Div([
                        html.Span("B", className="sector-letter"),
                        html.Div([
                            html.H4("Different national patterns"),
                            html.P("Compare how the rates changed, rather than assuming one global trend."),
                        ]),
                    ], className="sector-question"),
                    html.Div([
                        html.Span("C", className="sector-letter"),
                        html.Div([
                            html.H4("No single cause"),
                            html.P("Pandemic disruption was not the only driver of inflation in 2022."),
                        ]),
                    ], className="sector-question"),
                ], className="story-panel explanation-panel"),
            ], className="story-two-column story-two-column-single"),
            section_id="industry-impact",
        ),

        # CLOSING — STORY SUMMARY / TRANSITION TO CHAPTER 3
        html.Section(
            [
                html.Div(
                    [
                        html.P(
                            "CHAPTER 02 · THE TAKEAWAY",
                            className="chapter-kicker",
                        ),
                        html.H2(
                            [
                                html.Span("One crisis.", className="closing-line"),
                                html.Span(
                                    "Many economic realities.",
                                    className="closing-line title-accent",
                                ),
                            ],
                            className="closing-title",
                        ),
                        html.P(
                            "The global shock provides the starting point, not "
                            "the whole story. We compare annual growth, the "
                            "deviation from pre-pandemic trends, and subsequent "
                            "inflation. The next chapter explores unemployment.",
                            className="closing-description",
                        ),

                        # Four key takeaways
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span("01", className="closing-number"),
                                        html.P("Measure the shock"),
                                    ],
                                    className="closing-step",
                                ),
                                html.Div(
                                    [
                                        html.Span("02", className="closing-number"),
                                        html.P("Compare countries"),
                                    ],
                                    className="closing-step",
                                ),
                                html.Div(
                                    [
                                        html.Span("03", className="closing-number"),
                                        html.P("Compare with 2015–2019"),
                                    ],
                                    className="closing-step",
                                ),
                                html.Div(
                                    [
                                        html.Span("04", className="closing-number"),
                                        html.P("Track inflation"),
                                    ],
                                    className="closing-step",
                                ),
                            ],
                            className="closing-steps",
                        ),

                        # Transition card: link is a child, not an argument
                        # of the next-chapter-label Div.
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "NEXT CHAPTER",
                                            className="transition-eyebrow",
                                        ),
                                        html.Span(
                                            "03",
                                            className="transition-number",
                                        ),
                                    ],
                                    className="transition-topline",
                                ),
                                html.H3(
                                    "From economic shock to human impact.",
                                    className="transition-title",
                                ),
                                html.P(
                                    "GDP tells us what happened to the economy. "
                                    "Employment brings us closer to the people "
                                    "who lived through it.",
                                    className="transition-description",
                                ),
                                dcc.Link(
                                    [
                                        html.Span(
                                            "Continue to Chapter 3",
                                            className="transition-button-text",
                                        ),
                                        html.Span(
                                            "→",
                                            className="transition-button-arrow",
                                        ),
                                    ],
                                    href="/employment",
                                    className="transition-button",
                                ),
                            ],
                            className="chapter-transition",
                        ),
                    ],
                    className="closing-inner",
                ),
            ],
            className="chapter-closing reveal",
        ),
    ],
)


# ============================================================
# INTERACTIVITY
# ============================================================

@callback(
    Output("growth-line-chart", "figure"),
    Input("growth-region-filter", "value"),
)
def update_growth_chart(regions):
    return growth_line(regions or [])


@callback(
    Output("snapshot-year-label", "children"),
    Output("year-snapshot-chart", "figure"),
    Input("snapshot-year", "value"),
)
def update_snapshot(year):
    year = int(year)
    return str(year), year_snapshot(year)


