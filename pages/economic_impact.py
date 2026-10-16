from dash import html, dcc
from src.visualizations import growth_line, year_snapshot, sector_bars, metric_card

layout = html.Div([
    html.Section([
        html.Div([
            html.Span("PAGE 01 · GDP & INDUSTRIES", className="tag"),
            html.H1("Economic impact: the fall and the rebound"),
            html.P("A major contraction in 2020 was followed by a sharp bounce — but the experience varied across regions and industries.")
        ], className="container hero-content")
    ], className="hero hero-subpage"),
    html.Section([
        html.Div([
            html.Div([
                html.H2("Annual GDP growth by region"),
                html.P("Select regions to compare. Hover over chart points for values.", className="section-subtitle"),
                dcc.Checklist(
                    id="growth-region-filter",
                    options=[{"label": x, "value": x} for x in ["World", "US", "Euro area", "France", "China", "India"]],
                    value=["World", "US", "China"],
                    inline=True,
                    className="check-chips",
                ),
                dcc.Graph(id="growth-line-chart", figure=growth_line(["World", "US", "China"]), config={"displayModeBar": False}),
                html.Span("Illustrative, rounded values · % change in real GDP", className="chart-caption")
            ], className="panel"),
            html.Div([
                html.H2("Year snapshot"),
                html.P("Move through time and watch the ranking change.", className="section-subtitle"),
                html.Div(id="snapshot-year-label", children="2020", className="big-year"),
                dcc.Slider(id="snapshot-year", min=0, max=5, step=1, value=2,
                           marks={i: str(y) for i, y in enumerate([2018, 2019, 2020, 2021, 2022, 2023])},
                           tooltip={"placement": "bottom", "always_visible": False}),
                dcc.Graph(id="year-snapshot-chart", figure=year_snapshot(2020), config={"displayModeBar": False}),
                html.Div("A rebound does not necessarily mean the pre-crisis level has been regained.", className="callout")
            ], className="panel")
        ], className="container split split-wide")
    ], className="section"),
    html.Section([
        html.Div([
            html.H2("Not every sector moved in the same direction"),
            html.P("Use the buttons to compare illustrative sector changes. Replace these values with verified sector indicators.", className="section-subtitle"),
            dcc.RadioItems(id="sector-view", options=[
                {"label": "All sectors", "value": "All"},
                {"label": "Winners", "value": "Winners"},
                {"label": "Losers", "value": "Losers"},
            ], value="All", inline=True, className="radio-chips"),
            dcc.Graph(id="sector-bar-chart", figure=sector_bars("All"), config={"displayModeBar": False}),
        ], className="container panel")
    ], className="section section-muted"),
])
