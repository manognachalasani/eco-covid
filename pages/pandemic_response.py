"""Chapter 1 frontend. Demo data is synthetic; replace load_data() with the team's data/API adapter."""
import math
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, dcc, html, callback

COLORS = {"cases": "#64e5ff", "deaths": "#ff806e", "policy": "#a99bff", "vax": "#79e2b3"}
TEXT, MUTED, GRID = "#f4f7ff", "#a7b2c8", "rgba(180,199,228,.12)"

def load_data():
    """Synthetic preview data. Replace with processed CSV/API when ready."""
    dates = pd.date_range("2020-01-01", "2022-12-01", freq="MS")
    countries = ["France", "India", "United States", "Italy", "Germany"]
    rows = []
    for ci, country in enumerate(countries):
        for i, date in enumerate(dates):
            cases = (max(0, 140 * (1 + math.sin((i-3)/2.2))) +
                     max(0, 95 * (1 + math.sin((i-13)/2))) ) * (0.7 + ci*0.12)
            rows.append({
                "date": date, "country": country,
                "new_cases_per_million": round(cases, 2),
                "new_deaths_per_million": round(cases * max(0.004, 0.018-i*0.00035), 2),
                "stringency_index": round(max(15, min(95, 48+27*math.sin((i+ci)/3.5))), 2),
                "vaccinated_per_hundred": round(min(92, max(0, (i-10)*(3.2-ci*0.18))), 2),
            })
    return pd.DataFrame(rows)

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
        ("new_cases_per_million", "New cases / million", COLORS["cases"]),
        ("new_deaths_per_million", "New deaths / million", COLORS["deaths"]),
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

layout = html.Div(id="pandemic-story", className="pandemic-story", children=[
    html.Div(className="p-hero", children=[
                # Cinematic opening overlay
       
# Cinematic opening overlay
html.Div(
    id="pandemic-intro",
    className="pandemic-intro",
    children=[
        html.Div(
            "CHAPTER 01",
            className="pandemic-intro-label",
        ),
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
            html.H1(["When the world ", html.Span("stood still.", className="p-accent")], className="p-title"),
            html.P("A new virus crossed borders. Governments responded with restrictions, public-health measures and, later, vaccination campaigns. Follow the pandemic timeline and the policy choices recorded in the data.", className="p-intro"),
            html.Div("●  SCROLL TO OPEN THE ARCHIVE  ↓", className="p-scroll"),
        ])]),
    html.Div(className="p-demo-note reveal", children=[
        html.Strong("FRONTEND PREVIEW"),
        html.Span("Synthetic demo data is shown until the real dataset/backend is connected. Do not present these values as historical statistics.")]),
    html.Div(className="p-container", children=[
        html.Section(className="p-section reveal", children=[
            html.Div("01  /  THE SCALE OF THE OUTBREAK", className="p-eyebrow"),
            html.H2("A crisis measured over time", className="p-heading"),
            html.P("Choose a country, change the time window and toggle metrics. The other charts follow the same filters.", className="p-copy"),
            html.Div(className="p-controls", children=[
                html.Div([html.Label("COUNTRY"), dcc.Dropdown(
                    id="p-country", options=[{"label": c, "value": c} for c in ["France","India","United States","Italy","Germany"]],
                    value="France", clearable=False)], className="p-control"),
                html.Div([html.Label("TIME WINDOW"), dcc.RangeSlider(
                    id="p-range", min=0, max=35, step=1, value=[0,35],
                    marks={0:"Jan ’20",12:"Jan ’21",24:"Jan ’22",35:"Dec ’22"},
                    tooltip={"placement":"bottom","always_visible":False}, className="p-slider")],
                    className="p-control p-time"),
                html.Div([html.Label("SHOW METRICS"), dcc.Checklist(
                    id="p-metrics", options=[
                        {"label":" New cases","value":"new_cases_per_million"},
                        {"label":" New deaths","value":"new_deaths_per_million"}],
                    value=["new_cases_per_million","new_deaths_per_million"], inline=True,
                    className="p-checklist")], className="p-control p-metric-filter")]),
            html.Div(className="p-metrics", children=[
                metric("CASES / MILLION","p-cases","Sum across selected months","cyan",0),
                metric("DEATHS / MILLION","p-deaths","Sum across selected months","coral",1),
                metric("PEAK CASE RATE","p-peak","Highest monthly value","purple",2),
                metric("LATEST STRINGENCY","p-stringency","Index from 0 to 100","green",3)]),
            html.Div(className="p-panel reveal", children=[
                html.H3("The outbreak, month by month", className="p-panel-title"),
                html.P("Rates per million are not the same as total cases or deaths.", className="p-copy"),
                dcc.Graph(id="p-outbreak", config={"displaylogo":False,"responsive":True})]),
        ]),
        html.Section(className="p-section p-muted-section reveal", children=[
            html.Div("02  /  THE RESPONSE", className="p-eyebrow"),
            html.H2("How strict were the measures?", className="p-heading"),
            html.P("The stringency index summarizes selected government measures. It does not directly measure compliance or policy effectiveness.", className="p-copy"),
            html.Div(className="p-columns", children=[
                html.Div(className="p-panel reveal", children=[
                    html.H3("Restrictions over time", className="p-panel-title"),
                    dcc.Graph(id="p-policy", config={"displaylogo":False,"responsive":True})]),
                html.Div(className="p-panel p-explainer reveal", children=[
                    html.Div("READING THE INDEX", className="p-eyebrow"),
                    html.H3("A policy signal, not a verdict.", className="p-panel-title"),
                    html.P("Higher values indicate stricter recorded measures. The index cannot tell us whether a restriction was fair, followed, or effective on its own.", className="p-copy"),
                    html.Div(className="p-callout", children=[
                        html.Strong("KEEP IN MIND"),
                        html.P("A timeline can show that policy and case rates moved together. It cannot, by itself, prove that one caused the other.")])])]),
        ]),
        html.Section(className="p-section reveal", children=[
            html.Div("03  /  A TURNING POINT", className="p-eyebrow"),
            html.H2("The vaccination rollout", className="p-heading"),
            html.P("Vaccination coverage can mark a new phase of the pandemic. Missing observations should remain missing—not be converted to zero.", className="p-copy"),
            html.Div(className="p-panel reveal", children=[
                html.H3("Vaccination coverage", className="p-panel-title"),
                dcc.Graph(id="p-vaccination", config={"displaylogo":False,"responsive":True}),
                html.P("Confirm the exact vaccination definition against the final dataset.", className="p-chart-note")]),
        ]),
        html.Section(className="p-ending reveal", children=[
            html.Div("CHAPTER 01 — ARCHIVE NOTE", className="p-eyebrow"),
            html.H2(["The numbers describe the response. ",html.Span("Context gives them meaning.",className="p-accent")], className="p-ending-title"),
            html.P("Reported cases and deaths depend on testing and reporting. Stringency is a summary of measures, not a causal explanation. Next, follow the economic consequences that unfolded alongside the pandemic.", className="p-copy"),
            html.Div("NEXT CHAPTER  /  AN ECONOMY BROUGHT TO A HALT  →", className="p-next"),
           dcc.Link("Continue to Chapter 2 →",href="/economic-impact",className="p-chapter-button",)


        ])
    ])
])

@callback(
    Output("p-outbreak","figure"), Output("p-policy","figure"), Output("p-vaccination","figure"),
    Output("p-cases","children"), Output("p-deaths","children"),
    Output("p-peak","children"), Output("p-stringency","children"),
    Input("p-country","value"), Input("p-range","value"), Input("p-metrics","value"))
def update_charts(country, period, chosen):
    df = load_data()
    df["date"] = pd.to_datetime(df["date"])
    df = df[df.country == country].sort_values("date").reset_index(drop=True)
    start, end = period or [0, len(df)-1]
    df = df.iloc[int(start):int(end)+1]
    if df.empty:
        blank = styled(go.Figure())
        return blank, blank, blank, "—", "—", "—", "—"
    outbreak = line_fig(df, chosen or [])
    policy = simple_fig(df, "stringency_index", "Stringency index", COLORS["policy"], "Index (0–100)", [0,100])
    vax = simple_fig(df, "vaccinated_per_hundred", "Vaccinated per 100", COLORS["vax"], "People per 100", [0,100])
    def fmt(value):
        return "—" if pd.isna(value) else f"{value:,.1f}"
    return (
        outbreak, policy, vax,
        fmt(df["new_cases_per_million"].sum(min_count=1)),
        fmt(df["new_deaths_per_million"].sum(min_count=1)),
        fmt(df["new_cases_per_million"].max()),
        fmt(df["stringency_index"].dropna().iloc[-1] if df["stringency_index"].notna().any() else float("nan"))
    )
