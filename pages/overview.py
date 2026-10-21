"""
PandemiScope overview page.

Loads final_dataset.csv from the project root and builds the overview KPIs
and charts from the actual dataset. The dataset should live beside app.py.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

from src.visualizations import (
    metric_card,
    plot_gdp_growth,
    plot_gdp_shock_2020,
    plot_unemployment_change_2020,
    plot_inflation,
    plot_unemployment,
    plot_gdp_index,
    plot_gdp_recovery_2024,
    plot_wealth_vs_gdp_shock,
    plot_gdp_per_capita,
    plot_government_stringency,
    plot_vaccination_rollout,
    plot_mortality_vs_gdp_shock,
)



def _find_dataset():
    """Find final_dataset.csv in the processed/final folder or fallback locations."""
    candidates = []
    cwd = Path.cwd().resolve()

    # Preferred location: data/processed/final/final_dataset.csv
    candidates.append(cwd / "data" / "processed" / "final_dataset.csv")

    # Fallback locations, in case the app is launched from another directory.
    candidates.extend([
        cwd / "final_dataset.csv",
        cwd.parent / "final_dataset.csv",
    ])

    # Search relative to this Python module and its ancestor directories.
    module_path = Path(__file__).resolve()
    for parent in module_path.parents:
        candidates.append(
            parent / "data" / "processed" / "final_dataset.csv"
        )
        candidates.append(parent / "final_dataset.csv")

    seen = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate not in seen:
            seen.add(candidate)
            if candidate.is_file():
                print(f"PandemiScope: loading dataset from {candidate}")
                return candidate

    return None



def _load_dataset():
    """Load and lightly normalize the combined project dataset."""
    path = _find_dataset()
    if path is None:
        print(
            "PandemiScope: final_dataset.csv was not found. "
            "Place it in the project root beside app.py."
        )
        return None

    try:
        data = pd.read_csv(path)
        required = {"country", "year"}
        missing = required - set(data.columns)
        if missing:
            raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

        data = data.copy()
        data["year"] = pd.to_numeric(data["year"], errors="coerce")
        if "date" in data.columns:
            data["date"] = pd.to_datetime(
                data["date"], dayfirst=True, errors="coerce"
            )
        data = data.dropna(subset=["country", "year"])
        data["year"] = data["year"].astype(int)
        print(f"PandemiScope: loaded {len(data):,} rows from {path}")
        return data
    except Exception as exc:
        print(f"PandemiScope: could not load final_dataset.csv: {exc}")
        return None


def _annual_values(data, measure):
    """Return one robust annual value per country/year for a given indicator."""
    if data is None or measure not in data.columns:
        return pd.DataFrame(columns=["country", "year", measure])

    frame = data[["country", "year", measure]].copy()
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    frame[measure] = pd.to_numeric(frame[measure], errors="coerce")
    frame = frame.dropna(subset=["country", "year", measure])
    # Annual indicators are often repeated on each daily COVID row. Collapse
    # those repeats to one value per country/year.
    return (
        frame.groupby(["country", "year"], as_index=False)[measure]
        .median()
        .sort_values(["country", "year"])
    )


def _overview_metrics(data):
    """Compute overview KPIs from country-level indicators in the supplied dataset.

    The dataset contains repeated monthly/quarterly rows for country-level
    summary indicators, so collapse to one row per country before summarizing.
    Median values are used to reduce sensitivity to unusual country-specific
    GDP growth observations in this 10-country sample.
    """
    empty_metrics = [
        ("—", "Countries with usable 2020 GDP data"),
        ("—", "Countries with negative GDP growth in 2020"),
        ("—", "Median GDP growth in 2020 across included countries"),
        ("—", "Median unemployment-rate change, 2019–2020"),
    ]
    if data is None:
        return empty_metrics

    country_rows = data.dropna(subset=["country"]).drop_duplicates("country").copy()

    def numeric_series(column):
        if column not in country_rows.columns:
            return pd.Series(dtype="float64")
        return pd.to_numeric(country_rows[column], errors="coerce").dropna()

    growth_2020 = numeric_series("gdp_growth_2020")
    unemployment_change = numeric_series("unemployment_change_2020")

    country_count = int(growth_2020.size)
    contraction_count = int((growth_2020 < 0).sum())
    median_growth = growth_2020.median() if not growth_2020.empty else float("nan")
    median_unemployment_change = (
        unemployment_change.median()
        if not unemployment_change.empty
        else float("nan")
    )

    def pct(value):
        return "—" if pd.isna(value) else f"{value:+.1f}%"

    def pp(value):
        return "—" if pd.isna(value) else f"{value:+.1f} pp"

    return [
        (f"{country_count:,}", "Countries with usable 2020 GDP data"),
        (f"{contraction_count:,} / {country_count:,}",
         "Countries with negative GDP growth in 2020"),
        (pct(median_growth), "Median GDP growth in 2020 across included countries"),
        (pp(median_unemployment_change),
         "Median unemployment-rate change, 2019–2020"),
    ]


def _empty_figure(message):
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="center",
        font=dict(size=14, color="#64748b"),
    )
    fig.update_layout(
        template="plotly_white",
        height=380,
        margin=dict(l=20, r=20, t=45, b=30),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig




def _safe_chart(chart_function, data, *args, **kwargs):
    """Render visualization-module charts cleanly inside the overview layout."""
    if data is None:
        return _empty_figure(
            "Dataset not loaded. Place final_dataset.csv beside app.py."
        )

    try:
        fig = chart_function(data, *args, **kwargs)

        # Detect horizontal bar charts and give their labels more room.
        is_horizontal_bar = any(
            getattr(trace, "type", None) == "bar"
            and getattr(trace, "orientation", None) == "h"
            for trace in fig.data
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Inter, Arial, sans-serif",
                size=12,
                color="#DCE6F7",
            ),
            title=dict(
                font=dict(size=16, color="#F4F7FF"),
                x=0,
                xanchor="left",
            ),
            autosize=True,
            height=680 if is_horizontal_bar else (fig.layout.height or 620),
            margin=dict(
                l=220 if is_horizontal_bar else 70,
                r=115 if is_horizontal_bar else 40,
                t=90,
                b=95,
            ),
            showlegend=False,
        )

        fig.update_xaxes(
            automargin=True,
            gridcolor="rgba(167,178,200,0.13)",
            zerolinecolor="rgba(167,178,200,0.4)",
            tickfont=dict(color="#A7B2C8", size=11),
            title_font=dict(color="#A7B2C8", size=12),
        )

        fig.update_yaxes(
            automargin=True,
            gridcolor="rgba(167,178,200,0.13)",
            zerolinecolor="rgba(167,178,200,0.4)",
            tickfont=dict(color="#A7B2C8", size=11),
            title_font=dict(color="#A7B2C8", size=12),
        )

        if is_horizontal_bar:
            # Plotly can expose trace.x as a NumPy array. Do not use
            # `trace.x or []`, because its truth value is ambiguous.
            x_values = []
            for trace in fig.data:
                if getattr(trace, "type", None) == "bar":
                    values = trace.x
                    if values is None:
                        continue

                    for value in values:
                        try:
                            if value is not None:
                                numeric_value = float(value)
                                if pd.notna(numeric_value):
                                    x_values.append(numeric_value)
                        except (TypeError, ValueError):
                            continue

            if x_values:
                low = min(0.0, min(x_values))
                high = max(0.0, max(x_values))
                span = max(high - low, 1.0)
                fig.update_xaxes(
                    range=[
                        low - span * 0.16,
                        high + span * 0.20,
                    ],
                    automargin=True,
                )

        return fig

    except Exception as exc:
        print(f"Overview chart {chart_function.__name__} failed: {exc}")
        return _empty_figure(
            f"Chart unavailable: check the dataset columns and values for "
            f"{chart_function.__name__}."
        )



def _all_countries(data):
    """Return every country represented in the loaded dataset."""
    if data is None or "country" not in data.columns:
        return []
    return sorted(data["country"].dropna().astype(str).unique().tolist())


def _chart_panel(title, description, chart_id, chart_function, data, **chart_kwargs):
    """Build a consistently styled overview chart panel."""
    return html.Div(
        [
            html.H3(title),
            html.P(description),
            dcc.Graph(
                id=chart_id,
                figure=_safe_chart(chart_function, data, **chart_kwargs),
                config={"displayModeBar": False, "responsive": True},
                className="overview-chart",
                style={"height": "620px", "width": "100%", "display": "block"},
            ),
        ],
        className="overview-chart-panel p-panel",
        style={
            "display": "block",
            "visibility": "visible",
            "opacity": 1,
            "height": "auto",
            "minHeight": 0,
            "overflow": "visible",
            "position": "relative",
        },
    )


OVERVIEW_DATA = _load_dataset()
OVERVIEW_METRICS = _overview_metrics(OVERVIEW_DATA)
OVERVIEW_COUNTRIES = _all_countries(OVERVIEW_DATA)

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
                            "A data-led snapshot of GDP contraction and labour-market "
                            "change. Values are calculated from countries with "
                            "available observations in final_dataset.csv.",
                            className="overview-section-intro",
                        ),
                        html.Div(
                            [
                                metric_card(value, label)
                                for value, label in OVERVIEW_METRICS
                            ],
                            className="metric-grid overview-metric-grid",
                        ),
                        html.Div(
                            "Method note: country averages are unweighted and use "
                            "available observations only. They should not be read "
                            "as population-weighted global estimates.",
                            className="overview-data-note",
                        ),
                    ],
                    className="overview-content-width",
                ),
            ],
        ),

        # REAL DATA CHARTS
        html.Section(
            className="p-section overview-data-section",
            children=[
                html.Div(
                    className="overview-content-width",
                    children=[
                        html.Div("THE EVIDENCE", className="p-kicker"),
                        html.H2(
                            [
                                "The shock, ",
                                html.Span("measured.", className="p-accent"),
                            ],
                            className="overview-section-title",
                        ),
                        html.P(
                            "Explore ten-country GDP trends alongside the 2020 shock, "
                            "employment, inflation, recovery, income differences, and "
                            "pandemic-policy context. Each chart uses the available "
                            "indicators in final_dataset.csv.",
                            className="overview-section-intro",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3("GDP growth: before, during and after COVID-19"),
                                        html.P(
                                            "Annual real GDP growth for selected countries. "
                                            "The highlighted year marks the initial shock."
                                        ),
                                        dcc.Graph(
                                            id="overview-gdp-growth",
                                            figure=_safe_chart(
                                                plot_gdp_growth,
                                                OVERVIEW_DATA,
                                                countries=OVERVIEW_COUNTRIES,
                                            ),
                                            config={"displayModeBar": False, "responsive": True},
                                            className="overview-chart",
                                            style={"height": "620px", "width": "100%", "display": "block"},
                                        ),
                                    ],
                                    className="overview-chart-panel overview-chart-wide p-panel",
                                    style={
                                        "display": "block",
                                        "visibility": "visible",
                                        "opacity": 1,
                                        "height": "auto",
                                        "minHeight": 0,
                                        "overflow": "visible",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H3("The 2020 economic shock"),
                                        html.P(
                                            "Compare the estimated GDP-growth deviation "
                                            "across countries in the combined dataset."
                                        ),
                                        dcc.Graph(
                                            id="overview-gdp-shock",
                                            figure=_safe_chart(
                                                plot_gdp_shock_2020,
                                                OVERVIEW_DATA,
                                            ),
                                            config={"displayModeBar": False, "responsive": True},
                                            className="overview-chart",
                                            style={"height": "620px", "width": "100%", "display": "block"},
                                        ),
                                    ],
                                    className="overview-chart-panel p-panel",
                                    style={
                                        "display": "block",
                                        "visibility": "visible",
                                        "opacity": 1,
                                        "height": "auto",
                                        "minHeight": 0,
                                        "overflow": "visible",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H3("The unemployment impact"),
                                        html.P(
                                            "Change in the unemployment rate between "
                                            "2019 and 2020, measured in percentage points."
                                        ),
                                        dcc.Graph(
                                            id="overview-unemployment-change",
                                            figure=_safe_chart(
                                                plot_unemployment_change_2020,
                                                OVERVIEW_DATA,
                                            ),
                                            config={"displayModeBar": False, "responsive": True},
                                            className="overview-chart",
                                            style={"height": "620px", "width": "100%", "display": "block"},
                                        ),
                                    ],
                                    className="overview-chart-panel p-panel",
                                    style={
                                        "display": "block",
                                        "visibility": "visible",
                                        "opacity": 1,
                                        "height": "auto",
                                        "minHeight": 0,
                                        "overflow": "visible",
                                    },
                                ),
                                _chart_panel(
                                    "Unemployment over time",
                                    "Annual unemployment rates from 2018 to 2024 for all countries with available observations.",
                                    "overview-unemployment-trend",
                                    plot_unemployment,
                                    OVERVIEW_DATA,
                                    countries=OVERVIEW_COUNTRIES,
                                ),
                                _chart_panel(
                                    "GDP recovery: 2019 baseline",
                                    "Reconstructed real GDP index, with 2019 set to 100. Values above 100 indicate output above the 2019 level.",
                                    "overview-gdp-index",
                                    plot_gdp_index,
                                    OVERVIEW_DATA,
                                    countries=OVERVIEW_COUNTRIES,
                                ),
                                _chart_panel(
                                    "Who recovered by 2024?",
                                    "Change in reconstructed real GDP level versus 2019 for countries with the required annual data.",
                                    "overview-gdp-recovery",
                                    plot_gdp_recovery_2024,
                                    OVERVIEW_DATA,
                                ),
                                _chart_panel(
                                    "Inflation before and after the pandemic",
                                    "Compare annual inflation in 2019 and 2022. The difference is measured in percentage points.",
                                    "overview-inflation",
                                    plot_inflation,
                                    OVERVIEW_DATA,
                                    year_before=2019,
                                    year_after=2022,
                                ),
                                _chart_panel(
                                    "Pre-pandemic income and the 2020 shock",
                                    "Explore the relationship between 2019 GDP per capita and the team's derived 2020 GDP-shock measure. This is descriptive, not causal.",
                                    "overview-wealth-shock",
                                    plot_wealth_vs_gdp_shock,
                                    OVERVIEW_DATA,
                                ),
                                _chart_panel(
                                    "Economic resources before COVID-19",
                                    "GDP per capita in 2019 shows the very different economic starting points across the selected countries.",
                                    "overview-gdp-per-capita",
                                    plot_gdp_per_capita,
                                    OVERVIEW_DATA,
                                ),
                                _chart_panel(
                                    "Government response intensity",
                                    "The Oxford-style stringency indicator tracks recorded policy restrictions over time; it is not a direct measure of policy effectiveness.",
                                    "overview-government-stringency",
                                    plot_government_stringency,
                                    OVERVIEW_DATA,
                                    countries=OVERVIEW_COUNTRIES,
                                ),
                                _chart_panel(
                                    "Vaccination rollout",
                                    "Compare the available vaccination-per-hundred series. Coverage and definitions can differ by country.",
                                    "overview-vaccination-rollout",
                                    plot_vaccination_rollout,
                                    OVERVIEW_DATA,
                                    countries=OVERVIEW_COUNTRIES,
                                ),
                                _chart_panel(
                                    "Reported mortality and the GDP shock",
                                    "Compare reported cumulative COVID-19 deaths per million with the derived 2020 GDP-shock measure. Association does not establish causation.",
                                    "overview-mortality-gdp-shock",
                                    plot_mortality_vs_gdp_shock,
                                    OVERVIEW_DATA,
                                ),
                            ],
                            className="overview-data-grid",
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
                                "gap": "24px",
                                "width": "100%",
                                "height": "auto",
                                "minHeight": 0,
                                "overflow": "visible",
                                "visibility": "visible",
                                "opacity": 1,
                                "alignItems": "start",
                            },
                        ),
                        html.P(
                            "Sources and interpretation: the charts use the columns "
                            "already prepared in final_dataset.csv. GDP and unemployment "
                            "comparisons are descriptive; they do not establish that "
                            "COVID-19 alone caused each country's economic outcome.",
                            className="overview-data-caveat",
                        ),
                    ],
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
