
from dash import html, dcc
from src.visualizations import growth_line, sector_bars, metric_card


layout = html.Div(
    id="overview-story",
    className="pandemic-story overview-story",
    children=[

        # PROLOGUE HERO
        html.Div(
            className="p-hero overview-hero",
            children=[
                
# Cinematic opening overlay — Overview prologue
html.Div(
    id="pandemic-intro",
    className="pandemic-intro",
    children=[
        html.Div(
            "PANDEMISCOPE  /  THE PROLOGUE",
            className="pandemic-intro-label",
        ),
        html.Div(
            [
                "The world",
                html.Br(),
                html.Span(
                    "changed.",
                    className="pandemic-intro-highlight",
                ),
            ],
            className="pandemic-intro-title",
        ),
        html.Div(
            "One pandemic. A global economic shock. A story still unfolding.",
            className="pandemic-intro-subtitle",
        ),
        html.Div(className="pandemic-intro-accent-line"),
    ],
),

html.Div(className="p-grid"),

                html.Div(className="p-grid"),

                html.Div(
                    className="p-hero-inner chapter-hero-content",
                    children=[
                        html.Div(
                            "PANDEMISCOPE  /  THE PROLOGUE",
                            className="p-kicker",
                        ),
                        html.Div(
                            "A WORLD TRANSFORMED",
                            className="p-year",
                        ),
                        html.H1(
                            [
                                "How did a virus reshape ",
                                html.Span(
                                    "the global economy?",
                                    className="p-accent",
                                ),
                            ],
                            className="p-title",
                        ),
                        html.P(
                            "In 2020, the world slowed down almost overnight. "
                            "Businesses closed, workers faced uncertainty, "
                            "and global trade was disrupted. Explore the "
                            "economic shock, the policy response, and the "
                            "uneven road to recovery.",
                            className="p-intro",
                        ),

                       
                        html.Div(
                           [
                       # KEEP THE EXISTING VIDEO BUTTON
                         html.Button(
                         [
                            html.Span(
                                  "▶",
                                 className="intro-play-icon",
                                ),
                            html.Span(
                          "Watch introduction",
                              className="intro-play-label",
                             ),
                             ],
                         id="open-intro-video",
                         className="intro-play-button",
                         type="button",
                         title="Play the website introduction",
                        **{
                         "aria-label": "Play the website introduction video"
                          },
                         ),

        dcc.Link(
            "Explore the data  ↗",
            href="/pandemic-analysis",
            className="overview-secondary-link",
        ),

        dcc.Link(
    "Begin with Chapter One  →",
    href="/pandemic-response",
    className="p-chapter-button",
),
    ],
    className="hero-actions overview-hero-actions",
),


                        html.Div(
                            "↓  SCROLL TO DISCOVER THE STORY",
                            className="p-scroll",
                        ),
                    ],
                ),
            ],
        ),

        # KEY FIGURES
        html.Section(
            className="p-section overview-metrics-section",
            children=[
                html.Div(
                    [
                        html.Div(
                            "THE SHOCK IN NUMBERS",
                            className="p-kicker",
                        ),
                        html.H2(
                            [
                                "A crisis felt ",
                                html.Span(
                                    "around the world.",
                                    className="p-accent",
                                ),
                            ],
                            className="overview-section-title",
                        ),
                        html.P(
                            "Four illustrative figures introduce the scale "
                            "of the disruption. They are placeholders, not "
                            "verified findings.",
                            className="overview-section-intro",
                        ),
                        html.Div(
                            [
                                metric_card(
                                    "3.1%",
                                    "Illustrative world output dip, 2020",
                                ),
                                metric_card(
                                    "14.7%",
                                    "Illustrative US unemployment peak",
                                ),
                                metric_card(
                                    "−60%",
                                    "Illustrative air travel activity shock",
                                ),
                                metric_card(
                                    "6.0%",
                                    "Illustrative global rebound, 2021",
                                ),
                            ],
                            className="metric-grid overview-metric-grid",
                        ),
                        html.Div(
                            "DEMO VALUES ONLY  ·  Replace with verified "
                            "data and sources before presenting.",
                            className="p-demo-note",
                        ),
                    ],
                    className="overview-content-width",
                ),
            ],
        ),

        # EXPLORE THE STORY
        html.Section(
            className="p-section overview-discover-section",
            children=[
                html.Div(
                    "THE JOURNEY AHEAD",
                    className="p-kicker",
                ),
                html.H2(
                    [
                        "Four perspectives.",
                        html.Br(),
                        html.Span(
                            "One global story.",
                            className="p-accent",
                        ),
                    ],
                    className="overview-section-title",
                ),
                html.P(
                    "Move beyond the headline numbers. Each chapter "
                    "explores a different part of the pandemic's economic "
                    "story, with interactive charts to investigate along "
                    "the way.",
                    className="overview-section-intro",
                ),

                html.Div(
                    [
                        html.A(
                            [
                                html.Div(
                                    "01  /  THE SHOCK",
                                    className="overview-card-kicker",
                                ),
                                html.Span(
                                    "↗",
                                    className="overview-card-arrow",
                                ),
                                html.Span(
                                    "📉",
                                    className="card-icon",
                                ),
                                html.H3("Economic impact"),
                                html.P(
                                    "Follow the sudden fall in economic "
                                    "activity and compare the effects "
                                    "across regions."
                                ),
                            ],
                            href="/economic-impact",
                            className="feature-card p-panel overview-story-card",
                        ),

                        html.A(
                            [
                                html.Div(
                                    "02  /  THE RESPONSE",
                                    className="overview-card-kicker",
                                ),
                                html.Span(
                                    "↗",
                                    className="overview-card-arrow",
                                ),
                                html.Span(
                                    "🦠",
                                    className="card-icon",
                                ),
                                html.H3("Pandemic analysis"),
                                html.P(
                                    "Explore the timing of the crisis "
                                    "and its relationship with policy, "
                                    "employment, and economic activity."
                                ),
                            ],
                            href="/pandemic-analysis",
                            className="feature-card p-panel overview-story-card",
                        ),

                        html.A(
                            [
                                html.Div(
                                    "03  /  THE AFTERMATH",
                                    className="overview-card-kicker",
                                ),
                                html.Span(
                                    "↗",
                                    className="overview-card-arrow",
                                ),
                                html.Span(
                                    "🌱",
                                    className="card-icon",
                                ),
                                html.H3("The road back"),
                                html.P(
                                    "Investigate recovery and why "
                                    "a rebound in output does not "
                                    "necessarily mean everyone recovered."
                                ),
                            ],
                            href="/recovery",
                            className="feature-card p-panel overview-story-card",
                        ),

                        html.A(
                            [
                                html.Div(
                                    "04  /  THE EVIDENCE",
                                    className="overview-card-kicker",
                                ),
                                html.Span(
                                    "↗",
                                    className="overview-card-arrow",
                                ),
                                html.Span(
                                    "🧭",
                                    className="card-icon",
                                ),
                                html.H3("Read data wisely"),
                                html.P(
                                    "Question the context, comparability, "
                                    "uncertainty, and limitations behind "
                                    "every chart."
                                ),
                            ],
                            href="/data-methodology",
                            className="feature-card p-panel overview-story-card",
                        ),
                    ],
                    className="feature-grid overview-story-grid",
                ),
            ],
        ),

        # THE BIG PICTURE
        html.Section(
            className="p-section overview-context-section",
            children=[
                html.Div(
                    className="overview-context-panel p-panel",
                    children=[
                        html.Div(
                            "THE BIG PICTURE",
                            className="p-kicker",
                        ),
                        html.H2(
                            [
                                "An economy is more than ",
                                html.Span(
                                    "numbers.",
                                    className="p-accent",
                                ),
                            ],
                            className="overview-section-title",
                        ),
                        html.P(
                            "People buy, businesses produce, workers earn, "
                            "and goods move across borders. The pandemic "
                            "interrupted many of these connections at once, "
                            "creating effects that reached far beyond public "
                            "health.",
                            className="overview-context-copy",
                        ),
                        html.P(
                            "The aim of PandemiScope is not just to display "
                            "charts. It is to help you understand what the "
                            "evidence says, what it leaves out, and how to "
                            "ask better questions.",
                            className="overview-context-copy",
                        ),
                        html.Div(
                            [
                                html.Strong("A curious mindset"),
                                html.P(
                                    "When a chart surprises you, ask: "
                                    "who is included, over what period, "
                                    "and compared with what? Good analysis "
                                    "begins with those questions."
                                ),
                            ],
                            className="overview-learning-note",
                        ),
                    ],
                ),
            ],
        ),

        # CLOSING CTA
        html.Section(
            className="p-ending overview-ending",
            children=[
               # CLOSING CONCLUSION
html.Div(
    className="p-ending overview-ending",
    children=[
        html.Div(
            "THE BIGGER PICTURE",
            className="p-kicker",
        ),

        html.H2(
            "One crisis. A world transformed.",
        ),

        html.P(
            "The pandemic was more than a public health emergency. "
            "It disrupted economies, reshaped industries, changed how "
            "people lived and worked, and challenged countries in "
            "different ways. Its effects did not end when lockdowns did."
        ),

        html.P(
            "Understanding what happened means looking beyond the "
            "headlines — at the data, the inequalities it revealed, "
            "and the different paths countries took toward recovery."
        ),

        html.Div(
            "PANDEMISCOPE  /  UNDERSTANDING THE IMPACT",
            className="overview-ending-note",
        ),
    ],
),
                
            ],
        ),

        # ==========================================================
        # EXISTING INTRODUCTION VIDEO OVERLAY
        # PRESERVED: video source, IDs, controls and classes
        # ==========================================================
        html.Div(
            [
                html.Video(
                    id="intro-video-player",
                    src="/assets/intro.mp4",
                    controls=True,
                    autoPlay=False,
                    muted=False,
                    preload="auto",
                    playsInline=True,
                    className="intro-video-player",
                    **{
                        "aria-label":
                            "Introduction to the COVID-19 economic impact website",
                    },
                ),

                html.Div(
                    [
                        html.Button(
                            "Skip intro →",
                            id="skip-intro-video",
                            className="intro-skip-button",
                            type="button",
                        ),
                    ],
                    className="intro-video-bottom-controls",
                ),

                html.Button(
                    "✕",
                    id="close-intro-video",
                    className="intro-video-close",
                    type="button",
                    title="Close introduction",
                    **{"aria-label": "Close introduction video"},
                ),

                html.Div(
                    "If playback does not start, press play on the video.",
                    id="intro-video-status",
                    className="intro-video-status",
                    role="status",
                    **{"aria-live": "polite"},
                ),
            ],
            id="intro-video-overlay",
            className="intro-video-overlay",
            **{
                "aria-label": "Website introduction video",
                "aria-hidden": "true",
            },
        ),
    ],
)
