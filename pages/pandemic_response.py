"""Chapter 1 frontend. Demo data is synthetic; replace load_data() with the team's data/API adapter."""

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, dcc, html, callback
from pathlib import Path
import pandas as pd


from src.visualizations import (
    plot_covid_mortality,
    plot_government_stringency,
    plot_vaccination_rollout,
)

COLORS = {"cases": "#64e5ff", "deaths": "#ff806e", "policy": "#a99bff", "vax": "#79e2b3"}
TEXT, MUTED, GRID = "#f4f7ff", "#a7b2c8", "rgba(180,199,228,.12)"

def load_data():
    """Load the real processed dataset from the project root."""
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    data_path = PROJECT_ROOT / "data" / "processed" / "final_dataset.csv"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {data_path}"
        )

    df = pd.read_csv(data_path)

    required_columns = {
    "date",
    "country",
    "cases_per_million",
    "deaths_per_million",
    "stringency_index",
    "vaccinated_per_hundred",
}

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns in final_dataset.csv: {sorted(missing)}"
        )

    df["date"] = pd.to_datetime(
    df["date"],
    format="%d.%m.%Y",
    errors="coerce"
)

    df = df.dropna(subset=["date", "country"]).copy()
    df = df.sort_values(["country", "date"])

    return df

DATA = load_data()


for col in [
    "cases_per_million",
    "deaths_per_million",
    "deaths_per_million",
    "stringency_index",
    "vaccinated_per_hundred",
]:
    if col in DATA.columns:
        print(f"{col}: {DATA[col].notna().sum()} non-null values")
    else:
        print(f"{col}: COLUMN MISSING")

COUNTRIES = sorted(DATA["country"].dropna().unique())

DEFAULT_COUNTRY = (
    "United States"
    if "United States" in COUNTRIES
    else COUNTRIES[0]
)

MONTHS = sorted(
    DATA.loc[DATA["date"] >= "2018-01-01", "date"]
    .dt.to_period("M")
    .dropna()
    .unique()
)


def styled(fig, height=330, y_title=""):
    fig.update_layout(
        height=height, margin=dict(l=8, r=12, t=15, b=8),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color=TEXT, size=11),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.12, x=0, font=dict(color=MUTED)),
        yaxis_title=y_title,
        hoverlabel=dict(bgcolor="#121a2d", bordercolor="#33415a", font_color=TEXT))
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color=MUTED), linecolor=GRID)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED))
    return fig

def line_fig(df, chosen):
    fig = go.Figure()
    for key, label, color in [
        ("cases_per_million", "New cases / million", COLORS["cases"]),
        ("deaths_per_million", "New deaths / million", COLORS["deaths"]),
    ]:
        if key in chosen:
            fig.add_trace(go.Scatter(
                x=df.date, y=df[key], name=label, mode="lines",
                line=dict(color=color, width=2.6), connectgaps=False,
                hovertemplate="%{x|%b %Y}<br>%{y:,.1f}<extra>%{fullData.name}</extra>"))
    return styled(fig, 380, "Monthly rate per million")

def simple_fig(df, key, label, color, y_title, range_y=None):
    fig = go.Figure()
    valid = df.dropna(subset=[key])
    if not valid.empty:
        fig.add_trace(go.Scatter(
            x=valid.date, y=valid[key], name=label, mode="lines",
            line=dict(color=color, width=2.8),
            fill="tozeroy" if key == "stringency_index" else None,
            fillcolor="rgba(169,155,255,.10)", connectgaps=False,
            hovertemplate="%{x|%b %Y}<br>%{y:.1f}<extra></extra>"))
    if range_y:
        fig.update_yaxes(range=range_y)
    return styled(fig, 300, y_title)

def metric(label, ident, detail, accent, delay=0):
    delay_class = f"reveal-delay-{delay}" if delay else ""
    return html.Div(className=f"p-metric reveal {delay_class}".strip(), children=[
        html.Div(label, className="p-metric-label"),
        html.Div("—", id=ident, className=f"p-metric-value {accent}"),
        html.Div(detail, className="p-metric-detail")])


layout = html.Div(
    id="pandemic-story",
    className="pandemic-story",
    children=[
        # Hero section
        html.Div(className="p-hero", children=[
            html.Div(
                id="pandemic-intro",
                className="pandemic-intro",
                children=[
                    html.Div("CHAPTER 01", className="pandemic-intro-label"),
                    html.Div(
                        [
                            "Where the world",
                            html.Br(),
                            html.Span(
                                "stood still.",
                                className="pandemic-intro-highlight",
                            ),
                        ],
                        className="pandemic-intro-title",
                    ),
                    html.Div(
                        "A world connected. A virus that changed everything.",
                        className="pandemic-intro-subtitle",
                    ),
                    html.Div(className="pandemic-intro-accent-line"),
                ],
            ),
            html.Div(className="p-grid"),
            html.Div(className="p-hero-inner chapter-hero-content", children=[
                html.Div("COVID STORY  /  CHAPTER 01", className="p-kicker"),
                html.Div("2020", className="p-year"),
                html.H1(
                    ["When the world ", html.Span("stood still.", className="p-accent")],
                    className="p-title",
                ),
                html.P(
                    "A new virus crossed borders. Governments responded with "
                    "restrictions, public-health measures and, later, vaccination "
                    "campaigns. Follow the pandemic timeline and the policy choices "
                    "recorded in the data.",
                    className="p-intro",
                ),
                html.Div("●  SCROLL TO OPEN THE ARCHIVE  ↓", className="p-scroll"),
            ]),
        ]),

        html.Div(className="p-demo-note reveal", children=[
            html.Strong("DATA NOTE"),
            html.Span(
                "Charts use the connected dataset. Interpret rates per million "
                "as rates, not total counts."
            ),
        ]),

        # Main content
        html.Div(className="p-container", children=[
            # Section 1: Outbreak
            html.Section(className="p-section reveal", children=[
                html.Div("01  /  THE SCALE OF THE OUTBREAK", className="p-eyebrow"),
                html.H2("A crisis measured over time", className="p-heading"),
                html.P(
                    "Choose a country, change the time window and toggle metrics. "
                    "The other charts follow the same filters.",
                    className="p-copy",
                ),

                html.Div(className="p-controls", children=[
                    html.Div(className="p-control", children=[
                        html.Label("Country"),
                        dcc.Dropdown(
                            id="p-country",
                            options=[{"label": c, "value": c} for c in COUNTRIES],
                            value=DEFAULT_COUNTRY,
                            clearable=False,
                        ),
                    ]),
                    html.Div(className="p-control p-time", children=[
                        html.Label("TIME WINDOW"),
                        dcc.RangeSlider(
                            id="p-range",
                            min=0,
                            max=max(0, len(MONTHS) - 1),
                            step=1,
                            value=[0, max(0, len(MONTHS) - 1)],
                            marks={
                                i: MONTHS[i].strftime("%b '%y")
                                for i in sorted(set([
                                    0,
                                    len(MONTHS) // 3,
                                    2 * len(MONTHS) // 3,
                                    len(MONTHS) - 1,
                                ]))
                                if 0 <= i < len(MONTHS)
                            },
                            tooltip={
                                "placement": "bottom",
                                "always_visible": False,
                            },
                            className="p-slider",
                        ),
                    ]),
                    html.Div(className="p-control p-metric-filter", children=[
                        html.Label("SHOW METRICS"),
                        dcc.Checklist(
                            id="p-metrics",
                            options=[
                                {"label": " New cases", "value": "cases_per_million"},
                                {"label": " New deaths", "value": "deaths_per_million"},
                            ],
                            value=["cases_per_million", "deaths_per_million"],
                            inline=True,
                            className="p-checklist",
                        ),
                    ]),
                ]),

                html.Div(className="p-metrics", children=[
                    metric("AVG CASE RATE / MILLION", "p-cases", "Across countries and selected dates", "cyan", 0),
                    metric("AVG DEATH RATE / MILLION", "p-deaths", "Across countries and selected dates", "coral", 1),
                    metric("PEAK CASE RATE", "p-peak", "Highest recorded rate in selection", "purple", 2),
                    metric("LATEST STRINGENCY", "p-stringency", "Average latest value across countries", "green", 3),
                ]),

                html.Div(className="p-panel reveal", children=[
                    html.H3("The outbreak, month by month", className="p-panel-title"),
                    html.P(
                        "Rates per million are not the same as total cases or deaths.",
                        className="p-copy",
                    ),
                    dcc.Graph(
                        id="p-outbreak",
                        config={"displaylogo": False, "responsive": True},
                    ),
                ]),
            ]),

            # Section 2: Government response
           html.Section(className="p-section p-muted-section", children=[
                html.Div("02  /  THE RESPONSE", className="p-eyebrow"),
                html.H2("How strict were the measures?", className="p-heading"),
                html.P(
                    "The stringency index summarizes selected government measures. "
                    "It does not directly measure compliance or policy effectiveness.",
                    className="p-copy",
                ),
                html.Div(className="p-columns", children=[
                    html.Div(className="p-panel", children=[
                        html.H3("Restrictions over time", className="p-panel-title"),
                       dcc.Graph(
    id="p-policy",
    config={"displaylogo": False, "responsive": True},
    style={"height": "560px", "width": "100%"},
),
                    ]),
                    html.Div(className="p-panel p-explainer", children=[
                        html.Div("READING THE INDEX", className="p-eyebrow"),
                        html.H3("A policy signal, not a verdict.", className="p-panel-title"),
                        html.P(
                            "Higher values indicate stricter recorded measures. "
                            "The index cannot tell us whether a restriction was fair, "
                            "followed, or effective on its own.",
                            className="p-copy",
                        ),
                        html.Div(className="p-callout", children=[
                            html.Strong("KEEP IN MIND"),
                            html.P(
                                "A timeline can show that policy and case rates moved "
                                "together. It cannot, by itself, prove that one caused the other."
                            ),
                        ]),
                    ]),
                ]),
            ]),

            # Section 3: Vaccination
            html.Section(className="p-section reveal", children=[
                html.Div("03  /  A TURNING POINT", className="p-eyebrow"),
                html.H2("The vaccination rollout", className="p-heading"),
                html.P(
                    "Vaccination coverage can mark a new phase of the pandemic. "
                    "Missing observations should remain missing—not be converted to zero.",
                    className="p-copy",
                ),
                html.Div(className="p-panel reveal", children=[
                    html.H3("Vaccination coverage", className="p-panel-title"),
                    dcc.Graph(
                        id="p-vaccination",
                        config={"displaylogo": False, "responsive": True},
                    ),
                    html.P(
                        "Confirm the exact vaccination definition against the final dataset.",
                        className="p-chart-note",
                    ),
                ]),
            ]),

            # Closing section
            html.Section(className="p-ending reveal", children=[
                html.Div("CHAPTER 01 — ARCHIVE NOTE", className="p-eyebrow"),
                html.H2(
                    [
                        "The numbers describe the response. ",
                        html.Span("Context gives them meaning.", className="p-accent"),
                    ],
                    className="p-ending-title",
                ),
                html.P(
                    "Reported cases and deaths depend on testing and reporting. "
                    "Stringency is a summary of measures, not a causal explanation. "
                    "Next, follow the economic consequences that unfolded alongside the pandemic.",
                    className="p-copy",
                ),
                html.Div(
                    "NEXT CHAPTER  /  AN ECONOMY BROUGHT TO A HALT  →",
                    className="p-next",
                ),
                dcc.Link(
                    "Continue to Chapter 2 →",
                    href="/economic-impact",
                    className="p-chapter-button",
                ),
            ]),
        ]),
    ],
)






@callback(
    Output("p-outbreak", "figure"),
    Output("p-policy", "figure"),
    Output("p-vaccination", "figure"),
    Output("p-cases", "children"),
    Output("p-deaths", "children"),
    Output("p-peak", "children"),
    Output("p-stringency", "children"),
    Input("p-country", "value"),
    Input("p-range", "value"),
    Input("p-metrics", "value"),
)
def update_charts(country, period, chosen):
    if DATA.empty or not MONTHS:
        blank = go.Figure()
        return blank, blank, blank, "—", "—", "—", "—"
    print("DATA columns:", DATA.columns.tolist())
    print("DATA shape:", DATA.shape)
    print(DATA[["country", "date", "cases_per_million",
            "deaths_per_million"]].head())
    # Convert slider positions into calendar months.
    start, end = period or [0, len(MONTHS) - 1]
    start = max(0, min(int(start), len(MONTHS) - 1))
    end = max(start, min(int(end), len(MONTHS) - 1))

    start_month = MONTHS[start]
    end_month = MONTHS[end]

    # Keep the selected date range, but retain all countries.
    df = DATA[
        DATA["date"].dt.to_period("M").between(start_month, end_month)
    ].copy()

    if df.empty:
        blank = go.Figure()
        return blank, blank, blank, "—", "—", "—", "—"

    chosen = chosen or []

    numeric_columns = [
    "cases_per_million",
    "deaths_per_million",
    "stringency_index",
    "vaccinated_per_hundred",
]

    for col in numeric_columns:
      if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["cases_per_million", "deaths_per_million"]:
      print(f"\n{col}:")

    peak = df.loc[df[col].idxmax(), ["date", "country", col]]
    print("Overall peak:")
    print(peak)

    print("Yearly maximum:")
    print(df.groupby(df["date"].dt.year)[col].max())

    countries = [c for c in COUNTRIES if c in df["country"].unique()]

    
    # Consistent country colours across all charts.
    palette = [
        "#2764AB", "#E05B49", "#329785", "#9164B7", "#D99C38",
        "#557385", "#B06C81", "#798747", "#8B7865", "#777777",
    ]
    country_colors = {
        name: palette[i % len(palette)]
        for i, name in enumerate(COUNTRIES)
    }

    # 1. OUTBREAK: new cases and new deaths for all countries.
    outbreak = go.Figure()

    metrics = [
        ("cases_per_million", "New cases / million", "solid"),
        ("deaths_per_million", "New deaths / million", "dash"),
    ]

    for col, label, dash in metrics:
        if col not in chosen or col not in df.columns:
            continue

        for name in countries:
            part = df[df["country"] == name].sort_values("date")
            valid = part.dropna(subset=[col])

            if valid.empty:
                continue

          
            
            outbreak.add_trace(go.Scatter(
                x=valid["date"],
                y=valid[col],
                name=f"{name} — {label}",
                mode="lines",
                connectgaps=False,
                line=dict(
                    color=country_colors[name],
                    width=3 if name == country else 2,
                    dash="solid" if col == "cases_per_million" else "dash",
                ),
                opacity=1.0 if name == country else 0.85,
                hovertemplate=(
                    f"{name}<br>%{{x|%b %Y}}"
                    f"<br>%{{y:,.2f}}<extra>{label}</extra>"
                ),
            ))


    
    outbreak.update_layout(
     title="New cases and deaths across countries",
     yaxis_title="New reported rate per million",
     hovermode="x unified",
     height=650,
     margin=dict(l=60, r=30, t=80, b=160),
     legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.32,
        xanchor="left",
        x=0,
        font=dict(size=9),
    ),
)


    # 2. GOVERNMENT STRINGENCY: use the existing visualization function.
    policy = plot_government_stringency(
        df,
        countries=countries,
    )

    # 3. VACCINATION: use the existing visualization function.
    vaccination = plot_vaccination_rollout(
        df,
        countries=countries,
    )

    # Apply the Pandemiscope dark theme without replacing chart data.
    for fig in [outbreak, policy, vaccination]:
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Plus Jakarta Sans, Inter, sans-serif",
                color=TEXT,
                size=11,
            ),
           height=650,
           margin=dict(l=60, r=30, t=80, b=160),
           legend=dict(
           orientation="h",
           yanchor="bottom",
           y=-0.32,
           xanchor="left",
           x=0,
           font=dict(color=MUTED, size=9),
),
        )
        fig.update_xaxes(
            showgrid=False,
            tickfont=dict(color=MUTED),
            linecolor=GRID,
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor=GRID,
            tickfont=dict(color=MUTED),
            zeroline=False,
        )

    policy.update_yaxes(range=[0, 100])
    vaccination.update_yaxes(range=[0, 100])

    # 4. Summary cards: focus on the selected country.
    selected = df[df["country"] == country].copy()

    def fmt(value):
        return "—" if pd.isna(value) else f"{value:,.1f}"

    cases_col = "cases_per_million"
    deaths_col = "deaths_per_million"

    cases = (
        selected[cases_col].mean()
        if cases_col in selected.columns
        else float("nan")
    )

    deaths = (
        selected[deaths_col].mean()
        if deaths_col in selected.columns
        else float("nan")
    )

    peak_cases = (
        selected[cases_col].max()
        if cases_col in selected.columns
        else float("nan")
    )

    # Most recent available stringency value for the selected country.
    latest_stringency = float("nan")

    if "stringency_index" in selected.columns:
        latest_rows = (
            selected.dropna(subset=["stringency_index"])
            .sort_values("date")
        )

        if not latest_rows.empty:
            latest_stringency = latest_rows.iloc[-1]["stringency_index"]

    return (
        outbreak,
        policy,
        vaccination,
        fmt(cases),
        fmt(deaths),
        fmt(peak_cases),
        fmt(latest_stringency),
    )
