
from dash import html, dcc

from src.visualizations import recovery_line, recovery_index_bars


# Reuse the existing charts, but match the cinematic story theme.
recovery_path_fig = recovery_line()
sector_recovery_fig = recovery_index_bars()

for fig in (recovery_path_fig, sector_recovery_fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Plus Jakarta Sans, sans-serif",
            color="#a7b2c8",
            size=12,
        ),
        title_font=dict(
            family="Plus Jakarta Sans, sans-serif",
            color="#f4f7ff",
        ),
        margin=dict(l=18, r=18, t=30, b=18),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c5d0e2"),
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="rgba(167,178,200,0.18)",
            tickfont=dict(color="#a7b2c8"),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(167,178,200,0.10)",
            zeroline=False,
            tickfont=dict(color="#a7b2c8"),
        ),
    )


layout = html.Div(
    id="recovery-story",
    className="pandemic-story recovery-story",
    children=[

        # CHAPTER HERO
        html.Div(
            className="p-hero",
            children=[

                # Cinematic intro overlay
                html.Div(
                    id="recovery-intro",
                    className="pandemic-intro",
                    children=[
                        html.Div(
                            "CHAPTER 04",
                            className="pandemic-intro-label",
                        ),
                        html.Div(
                            [
                                "The ",
                                html.Br(),
                                html.Span(
                                    "Road Back.",
                                    className="pandemic-intro-highlight",
                                ),
                            ],
                            className="pandemic-intro-title",
                        ),
                        html.Div(
                            "The world reopened. But what did recovery really mean?",
                            className="pandemic-intro-subtitle",
                        ),
                        html.Div(
                            className="pandemic-intro-accent-line",
                        ),
                    ],
                ),

                # Decorative background grid
                html.Div(className="p-grid"),

                # Hero content
                html.Div(
                    className="p-hero-inner chapter-hero-content",
                    children=[
                        html.Div(
                            "PANDEMISCOPE  /  CHAPTER 04",
                            className="p-kicker",
                        ),
                        html.Div("2021 — 2023", className="p-year"),
                        html.H1(
                            [
                                "The road ",
                                html.Span(
                                    "back.",
                                    className="p-accent",
                                ),
                            ],
                            className="p-title",
                        ),
                        html.P(
                            "As restrictions eased and businesses reopened, "
                            "economies began to recover. But a rebound in "
                            "economic activity does not tell the whole story. "
                            "Who recovered, what changed, and what was left behind?",
                            className="p-intro",
                        ),
                        html.Div(
                            "↓  SCROLL TO EXPLORE THE RECOVERY",
                            className="p-scroll",
                        ),
                    ],
                ),
            ],
        ),

        # DATA DISCLAIMER
        html.Div(
            [
                html.Span("●  DATA NOTE  ", className="p-kicker"),
                html.Span(
                    "The current charts use illustrative data. "
                    "Treat them as visual demonstrations, not verified "
                    "economic findings.",
                ),
            ],
            className="p-demo-note",
        ),

        # SECTION 1: THE REBOUND
        html.Section(
            className="p-section",
            children=[
                html.Div(
                    "01  /  THE REBOUND",
                    className="p-kicker",
                ),
                html.H2(
                    [
                        "An economy can bounce back.",
                        html.Br(),
                        html.Span(
                            "But how far?",
                            className="p-accent",
                        ),
                    ],
                    className="p-section-title",
                ),
                html.P(
                    "The first question is whether economic activity "
                    "returned to its pre-pandemic level. A sharp rebound "
                    "after a collapse can look impressive, but the starting "
                    "point matters just as much as the growth rate.",
                    className="p-section-intro",
                ),

                html.Div(
                    className="p-panel",
                    children=[
                        html.Div(
                            "ECONOMIC ACTIVITY  /  RECOVERY PATH",
                            className="p-kicker",
                        ),
                        html.H3(
                            "The recovery path",
                            className="p-panel-title",
                        ),
                        html.P(
                            "Explore the existing activity index and its "
                            "illustrative return toward the baseline.",
                            className="p-panel-copy",
                        ),
                        dcc.Graph(
                            id="recovery-path-chart",
                            figure=recovery_path_fig,
                            config={"displayModeBar": False},
                            style={"height": "370px"},
                        ),
                        html.Div(
                            "Illustrative index · baseline = 100",
                            className="p-chart-caption",
                        ),
                    ],
                ),
            ],
        ),

        # SECTION 2: UNEVEN RECOVERY
        html.Section(
            className="p-section",
            children=[
                html.Div(
                    "02  /  NOT EVERYONE RECOVERS EQUALLY",
                    className="p-kicker",
                ),
                html.H2(
                    [
                        "One crisis.",
                        html.Br(),
                        html.Span(
                            "Different recoveries.",
                            className="p-accent",
                        ),
                    ],
                    className="p-section-title",
                ),
                html.P(
                    "An overall recovery can hide important differences. "
                    "Industries, workers and households do not necessarily "
                    "return to normal at the same pace.",
                    className="p-section-intro",
                ),

                html.Div(
                    className="p-panel",
                    children=[
                        html.Div(
                            "SECTOR COMPARISON  /  RECOVERY INDEX",
                            className="p-kicker",
                        ),
                        html.H3(
                            "Recovery across sectors",
                            className="p-panel-title",
                        ),
                        html.P(
                            "Compare the illustrative sector activity "
                            "indices. A consistent baseline and time period "
                            "are needed for a meaningful comparison.",
                            className="p-panel-copy",
                        ),
                        dcc.Graph(
                            id="recovery-sector-chart",
                            figure=sector_recovery_fig,
                            config={"displayModeBar": False},
                            style={"height": "370px"},
                        ),
                        html.Div(
                            "Illustrative values · replace with verified data",
                            className="p-chart-caption",
                        ),
                    ],
                ),
            ],
        ),

        # SECTION 3: WHAT RECOVERY REALLY MEANS
        html.Section(
            className="p-section",
            children=[
                html.Div(
                    "03  /  BEYOND THE HEADLINES",
                    className="p-kicker",
                ),
                html.H2(
                    [
                        "So, what does",
                        html.Br(),
                        html.Span(
                            "recovery mean?",
                            className="p-accent",
                        ),
                    ],
                    className="p-section-title",
                ),
                html.P(
                    "There is no single indicator that can capture the "
                    "full experience of recovery. Look across several "
                    "dimensions before drawing a conclusion.",
                    className="p-section-intro",
                ),

                html.Div(
                    className="p-recovery-checklist",
                    children=[
                        html.Div(
                            [
                                html.Div("01", className="p-card-number"),
                                html.H3("Economic output"),
                                html.P(
                                    "Did real GDP return to its pre-pandemic "
                                    "level? Did it return to the growth path "
                                    "that might have occurred without the shock?"
                                ),
                            ],
                            className="p-panel p-check-card",
                        ),
                        html.Div(
                            [
                                html.Div("02", className="p-card-number"),
                                html.H3("Employment"),
                                html.P(
                                    "Did employment recover alongside "
                                    "output? Consider unemployment, hours "
                                    "worked and labour-force participation."
                                ),
                            ],
                            className="p-panel p-check-card",
                        ),
                        html.Div(
                            [
                                html.Div("03", className="p-card-number"),
                                html.H3("Unequal outcomes"),
                                html.P(
                                    "Did recovery reach the sectors, "
                                    "regions and groups that experienced "
                                    "the greatest disruption?"
                                ),
                            ],
                            className="p-panel p-check-card",
                        ),
                        html.Div(
                            [
                                html.Div("04", className="p-card-number"),
                                html.H3("Cost of living"),
                                html.P(
                                    "How did inflation, purchasing power "
                                    "and public debt shape the experience "
                                    "of recovery?"
                                ),
                            ],
                            className="p-panel p-check-card",
                        ),
                    ],
                ),
            ],
        ),

        # SECTION 4: EVIDENCE-BASED TAKEAWAY
        html.Section(
            className="p-section",
            children=[
                html.Div(
                    "04  /  YOUR CONCLUSION",
                    className="p-kicker",
                ),
                html.Div(
                    className="p-panel p-takeaway-panel",
                    children=[
                        html.H2(
                            "Tell the story the data supports.",
                            className="p-section-title",
                        ),
                        html.P(
                            "Bring the indicators together. Write a "
                            "conclusion, identify the evidence behind it, "
                            "and acknowledge what the data cannot establish.",
                            className="p-panel-copy",
                        ),
                        dcc.Textarea(
                            id="recovery-takeaway",
                            placeholder=(
                                "Our evidence suggests...\n\n"
                                "The indicators show...\n\n"
                                "One important limitation is..."
                            ),
                            className="p-takeaway-input",
                        ),
                        html.Button(
                            "Preview my conclusion  →",
                            id="preview-takeaway",
                            className="p-chapter-button",
                            n_clicks=0,
                        ),
                        html.Div(
                            id="takeaway-preview",
                            className="p-takeaway-preview",
                        ),
                    ],
                ),
            ],
        ),

        # CHAPTER ENDING
        html.Section(
            className="p-ending",
            children=[
                html.Div(
                    "CHAPTER 04  /  THE ROAD BACK",
                    className="p-kicker",
                ),
                html.H2(
                    [
                        "Recovery is not just",
                        html.Br(),
                        html.Span(
                            "getting back.",
                            className="p-accent",
                        ),
                    ],
                    className="p-section-title",
                ),
                html.P(
                    "It is about understanding what changed, who benefited "
                    "from the rebound, and which challenges remained long "
                    "after the world reopened.",
                    className="p-section-intro",
                ),
                html.Div(
                    "THE STORY CONTINUES",
                    className="p-scroll",
                ),
            ],
        ),
    ],
)
