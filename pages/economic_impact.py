
# pages/economic_impact.py

from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# ============================================================
# MOCK DATA — REPLACE WITH VERIFIED ANALYSIS RESULTS LATER
# Values are illustrative, rounded, and NOT research findings.
# GDP growth = annual real GDP growth (%).
# Sector values = illustrative change (%).
# ============================================================

YEARS = [2018, 2019, 2020, 2021, 2022, 2023]

GDP_DATA = {
    "World":     [3.3, 2.6, -3.1, 6.0, 3.5, 3.2],
    "US":        [3.0, 2.6, -2.2, 6.1, 2.5, 2.9],
    "Euro area": [1.8, 1.6, -6.1, 6.2, 3.5, 0.4],
    "France":    [1.9, 1.8, -7.5, 6.4, 2.6, 1.1],
    "China":     [6.7, 6.0, 2.2, 8.4, 3.0, 5.2],
    "India":     [6.5, 3.9, -5.8, 9.7, 7.0, 8.2],
}

# These are illustrative index values, not actual GDP observations.
# 2019 is the pre-pandemic reference year = 100.
GDP_INDEX = {
    "World":     [96.5, 100, 96.9, 102.7, 106.3, 109.7],
    "US":        [96.1, 100, 97.8, 103.8, 106.4, 109.5],
    "Euro area": [98.2, 100, 93.9, 99.7, 103.2, 103.6],
    "France":    [98.1, 100, 92.5, 98.4, 100.9, 102.0],
    "China":     [100.7, 100, 102.2, 110.8, 114.1, 120.0],
    "India":     [96.8, 100, 94.2, 103.3, 110.5, 119.6],
}

SECTOR_DATA = pd.DataFrame({
    "Sector": [
        "Travel & tourism",
        "Hospitality",
        "Manufacturing",
        "Retail",
        "Construction",
        "Digital services",
        "Healthcare",
    ],
    "Illustrative change (%)": [-55, -38, -12, -15, -10, 18, 12],
})


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

COUNTRY_COLORS = {
    "World": CYAN,
    "US": CORAL,
    "Euro area": PURPLE,
    "France": "#FFBD69",
    "China": GREEN,
    "India": "#F08BC5",
}

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


def growth_line(selected_regions):
    fig = go.Figure()

    for region in selected_regions:
        fig.add_trace(go.Scatter(
            x=YEARS,
            y=GDP_DATA[region],
            name=region,
            mode="lines+markers",
            line=dict(
                color=COUNTRY_COLORS[region],
                width=3,
                shape="spline",
            ),
            marker=dict(size=7),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "%{x}: %{y:.1f}%<extra></extra>"
            ),
        ))

    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="rgba(255,255,255,0.35)",
    )
    fig.update_layout(
        title=None,
        xaxis=dict(
            tickmode="array",
            tickvals=YEARS,
            title=None,
        ),
        yaxis_title="Annual real GDP growth (%)",
    )
    return base_figure(fig, 380)


def year_snapshot(year):
    index = YEARS.index(year)
    regions = list(GDP_DATA.keys())
    values = [GDP_DATA[r][index] for r in regions]

    ordered = sorted(
        zip(regions, values),
        key=lambda item: item[1],
    )
    labels = [x[0] for x in ordered]
    data = [x[1] for x in ordered]

    colors = [
        COUNTRY_COLORS[r] if value >= 0 else CORAL
        for r, value in ordered
    ]

    fig = go.Figure(go.Bar(
        x=data,
        y=labels,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(width=0),
        ),
        text=[f"{v:+.1f}%" for v in data],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))

    fig.add_vline(
        x=0,
        line_color="rgba(255,255,255,0.4)",
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Annual real GDP growth (%)",
        yaxis_title=None,
        xaxis=dict(zeroline=False),
    )
    return base_figure(fig, 360)


def recovery_chart(selected_regions):
    fig = go.Figure()

    for region in selected_regions:
        fig.add_trace(go.Scatter(
            x=YEARS,
            y=GDP_INDEX[region],
            name=region,
            mode="lines+markers",
            line=dict(
                color=COUNTRY_COLORS[region],
                width=2.7,
                shape="spline",
            ),
            marker=dict(size=6),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "%{x}: index %{y:.1f}<extra></extra>"
            ),
        ))

    fig.add_hline(
        y=100,
        line_dash="dash",
        line_color="#FFFFFF",
        annotation_text="2019 baseline",
        annotation_font_color=MUTED,
    )
    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=YEARS),
        yaxis_title="Illustrative GDP index (2019 = 100)",
    )
    return base_figure(fig, 380)


def sector_bars(view):
    data = SECTOR_DATA.copy()

    if view == "Winners":
        data = data[data["Illustrative change (%)"] > 0]
    elif view == "Losers":
        data = data[data["Illustrative change (%)"] < 0]

    data = data.sort_values("Illustrative change (%)")

    colors = [
        GREEN if value >= 0 else CORAL
        for value in data["Illustrative change (%)"]
    ]

    fig = go.Figure(go.Bar(
        x=data["Illustrative change (%)"],
        y=data["Sector"],
        orientation="h",
        marker_color=colors,
        text=[
            f"{value:+.0f}%"
            for value in data["Illustrative change (%)"]
        ],
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "%{y}<br>Illustrative change: %{x:+.0f}%<extra></extra>"
        ),
    ))
    fig.add_vline(
        x=0,
        line_color="rgba(255,255,255,0.45)",
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Illustrative change (%)",
        yaxis_title=None,
    )
    return base_figure(fig, max(250, 48 * len(data) + 70))


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
                "This is a storytelling prototype. All displayed chart "
                "values are illustrative mock data, not verified findings. "
                "Replace them with results from your finalized dataset "
                "before drawing conclusions.",
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
                        "The lines show illustrative annual real GDP growth.",
                        className="panel-description",
                    ),
                    dcc.Checklist(
                        id="growth-region-filter",
                        options=[
                            {"label": r, "value": r}
                            for r in GDP_DATA
                        ],
                        value=["World", "US", "France", "China"],
                        inline=True,
                        className="story-checklist",
                        inputClassName="story-check-input",
                        labelClassName="story-check-label",
                    ),
                    dcc.Graph(
                        id="growth-line-chart",
                        figure=growth_line(
                            ["World", "US", "France", "China"]
                        ),
                        config=CHART_CONFIG,
                        className="story-graph",
                    ),
                    html.P(
                        "Illustrative values · annual real GDP growth (%)",
                        className="chart-footnote",
                    ),
                ], className="story-panel chart-panel"),

                html.Div([
                    html.P("THE CRISIS IN NUMBERS", className="mini-eyebrow"),
                    html.H3("The shock was not uniform.", className="panel-title"),
                    html.P(
                        "These example indicators establish the questions "
                        "the final analysis should answer.",
                        className="panel-description",
                    ),
                    html.Div([
                        metric(
                            "Global growth · 2020",
                            "−3.1%",
                            "Illustrative annual contraction",
                            "coral",
                        ),
                        metric(
                            "France · 2020",
                            "−7.5%",
                            "Illustrative contraction",
                            "purple",
                        ),
                        metric(
                            "China · 2020",
                            "+2.2%",
                            "Illustrative positive growth",
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
            ], className="story-two-column"),
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
                        min=2018,
                        max=2023,
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
                    className="story-graph",
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
                            "Test whether the same pattern appears "
                            "in your finalized data."
                        ),
                    ], className="insight-step"),
                ], className="insight-steps"),
            ], className="story-panel chart-panel"),
            section_id="country-comparison",
            extra_class="story-section-muted",
        ),

        # ACT 3 — REBOUND VS RECOVERY
        story_section(
            "03",
            "AFTER THE FALL",
            "A rebound is not the same as recovery",
            "Growth measures how quickly output changes. An index compares "
            "the level of output against a reference year. A strong growth "
            "rate can follow a deep decline without immediately restoring "
            "the lost ground.",
            html.Div([
                html.Div([
                    html.P("FOLLOW THE RECOVERY", className="mini-eyebrow"),
                    html.H3(
                        "Who returned to the 2019 baseline?",
                        className="panel-title",
                    ),
                    html.P(
                        "The horizontal reference line marks the illustrative "
                        "pre-pandemic level. Select economies to follow the "
                        "path of the index.",
                        className="panel-description",
                    ),
                    dcc.Checklist(
                        id="recovery-region-filter",
                        options=[
                            {"label": r, "value": r}
                            for r in GDP_INDEX
                        ],
                        value=["World", "France", "US", "China"],
                        inline=True,
                        className="story-checklist",
                        labelClassName="story-check-label",
                    ),
                    dcc.Graph(
                        id="recovery-line-chart",
                        figure=recovery_chart(
                            ["World", "France", "US", "China"]
                        ),
                        config=CHART_CONFIG,
                        className="story-graph",
                    ),
                    html.P(
                        "Illustrative index only · 2019 = 100",
                        className="chart-footnote",
                    ),
                ], className="story-panel chart-panel"),
                html.Div([
                    html.P("READ THE CHART", className="mini-eyebrow"),
                    html.H3("Two different questions.", className="panel-title"),
                    html.Div([
                        html.Span("01", className="explain-number"),
                        html.Div([
                            html.H4("Growth"),
                            html.P(
                                "How much did output change compared "
                                "with the previous year?"
                            ),
                        ]),
                    ], className="explain-row"),
                    html.Div([
                        html.Span("02", className="explain-number"),
                        html.Div([
                            html.H4("Recovery"),
                            html.P(
                                "How far has output returned relative "
                                "to its pre-crisis level?"
                            ),
                        ]),
                    ], className="explain-row"),
                    html.Div([
                        html.Span("03", className="explain-number"),
                        html.Div([
                            html.H4("Resilience"),
                            html.P(
                                "Did output recover quickly, slowly, "
                                "or follow a different path altogether?"
                            ),
                        ]),
                    ], className="explain-row"),
                ], className="story-panel explanation-panel"),
            ], className="story-two-column"),
            section_id="the-rebound",
        ),

        # ACT 4 — INDUSTRIES
        story_section(
            "04",
            "BEYOND GDP",
            "Some industries stopped. Others adapted.",
            "National GDP can conceal very different experiences. Restrictions "
            "hit travel and hospitality directly, while some digital services "
            "benefited from a rapid shift to remote work and online activity. "
            "The final dataset should test these patterns rather than assume them.",
            html.Div([
                html.Div([
                    html.P("COMPARE INDUSTRIES", className="mini-eyebrow"),
                    html.H3(
                        "The shock beneath the headline",
                        className="panel-title",
                    ),
                    html.P(
                        "Switch between the illustrative sector groups. "
                        "Positive values represent an increase; negative "
                        "values represent a decline.",
                        className="panel-description",
                    ),
                    dcc.RadioItems(
                        id="sector-view",
                        options=[
                            {"label": "All sectors", "value": "All"},
                            {"label": "Positive", "value": "Winners"},
                            {"label": "Negative", "value": "Losers"},
                        ],
                        value="All",
                        inline=True,
                        className="story-checklist",
                        labelClassName="story-check-label",
                    ),
                    dcc.Graph(
                        id="sector-bar-chart",
                        figure=sector_bars("All"),
                        config=CHART_CONFIG,
                        className="story-graph",
                    ),
                    html.P(
                        "Illustrative values only · replace with sourced "
                        "sector indicators and a defined comparison period.",
                        className="chart-footnote",
                    ),
                ], className="story-panel chart-panel"),
                html.Div([
                    html.P("WHAT TO INVESTIGATE", className="mini-eyebrow"),
                    html.H3("Look beyond the average.", className="panel-title"),
                    html.Div([
                        html.Span("A", className="sector-letter"),
                        html.Div([
                            html.H4("Exposure"),
                            html.P(
                                "Which sectors depended on physical "
                                "movement or in-person contact?"
                            ),
                        ]),
                    ], className="sector-question"),
                    html.Div([
                        html.Span("B", className="sector-letter"),
                        html.Div([
                            html.H4("Adaptation"),
                            html.P(
                                "Which sectors could shift to digital "
                                "delivery or remote work?"
                            ),
                        ]),
                    ], className="sector-question"),
                    html.Div([
                        html.Span("C", className="sector-letter"),
                        html.Div([
                            html.H4("Unequal impact"),
                            html.P(
                                "Did countries with different sector "
                                "mixes experience different shocks?"
                            ),
                        ]),
                    ], className="sector-question"),
                ], className="story-panel explanation-panel"),
            ], className="story-two-column"),
            section_id="industry-impact",
        ),

        # CLOSING — STORY SUMMARY / TRANSITION
        html.Section([
            html.Div([
                html.P("CHAPTER 02 · THE TAKEAWAY", className="chapter-kicker"),
                html.H2([
                    html.Span("One crisis.", className="closing-line"),
                    html.Span("Many economic realities.", className="closing-line title-accent"),
                ], className="closing-title"),
                html.P(
                    "The global shock provides the starting point, not "
                    "the whole story. To understand its lasting economic "
                    "impact, we must compare the depth of contraction, "
                    "the pace of recovery and the industries behind the totals.",
                    className="closing-description",
                ),
                html.Div([
                    html.Div([
                        html.Span("01", className="closing-number"),
                        html.P("Measure the shock"),
                    ]),
                    html.Div([
                        html.Span("02", className="closing-number"),
                        html.P("Compare countries"),
                    ]),
                    html.Div([
                        html.Span("03", className="closing-number"),
                        html.P("Trace recovery"),
                    ]),
                    html.Div([
                        html.Span("04", className="closing-number"),
                        html.P("Uncover sector differences"),
                    ]),
                ], className="closing-steps"),
                html.Div(
                    "NEXT CHAPTER  /  FROM SHOCK TO RECOVERY  →",
                    className="next-chapter-label",
                ),
            ], className="closing-inner"),
        ], className="chapter-closing reveal"),
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


@callback(
    Output("recovery-line-chart", "figure"),
    Input("recovery-region-filter", "value"),
)
def update_recovery_chart(regions):
    return recovery_chart(regions or [])


@callback(
    Output("sector-bar-chart", "figure"),
    Input("sector-view", "value"),
)
def update_sector_chart(view):
    return sector_bars(view or "All")
