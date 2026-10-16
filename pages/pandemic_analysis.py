from dash import html, dcc
from src.visualizations import unemployment_line, trade_line, fiscal_bars

layout = html.Div([
    html.Section([
        html.Div([
            html.Span("PAGE 02 · SHOCK & RESPONSE", className="tag"),
            html.H1("Pandemic analysis"),
            html.P("The pandemic was a health crisis and an economic shock. Explore labor-market disruption, trade interruption and policy responses.")
        ], className="container hero-content")
    ], className="hero hero-subpage"),
    html.Section([
        html.Div([
            html.Div([
                html.H2("Unemployment during 2020"),
                html.P("Compare illustrative monthly trends across labor markets.", className="section-subtitle"),
                dcc.Checklist(id="jobs-region-filter", options=[
                    {"label": "United States", "value": "US"},
                    {"label": "Euro area", "value": "Euro area"},
                ], value=["US", "Euro area"], inline=True, className="check-chips"),
                dcc.Graph(id="unemployment-chart", figure=unemployment_line(["US", "Euro area"]), config={"displayModeBar": False}),
                html.Span("Illustrative monthly values (%)", className="chart-caption")
            ], className="panel"),
            html.Div([
                html.H2("World goods trade"),
                html.P("A placeholder index illustrating a dip and subsequent rebound.", className="section-subtitle"),
                dcc.Graph(figure=trade_line(), config={"displayModeBar": False}),
                html.Span("Illustrative index · 2019 Q4 = 100", className="chart-caption")
            ], className="panel")
        ], className="container split")
    ], className="section"),
    html.Section([
        html.Div([
            html.H2("Fiscal support"),
            html.P("Emergency measures cushioned some effects of the shock. Cross-country comparisons need careful definitions.", className="section-subtitle"),
            dcc.Graph(figure=fiscal_bars(), config={"displayModeBar": False}),
            html.Div([
                html.Strong("⚠️ Interpretation guardrail"),
                html.P("A relationship between policy support and economic outcomes does not establish policy effectiveness. Timing, eligibility, implementation and other shocks matter.")
            ], className="callout")
        ], className="container panel")
    ], className="section section-muted"),
    html.Section([
        html.Div([
            html.H2("Questions to investigate"),
            html.Div([
                html.Div([html.Span("01", className="number"), html.H3("Who was most exposed?"), html.P("Compare sector mix, age, contract type and the ability to work remotely.")], className="question-card"),
                html.Div([html.Span("02", className="number"), html.H3("Which indicators moved together?"), html.P("Test relationships, but account for timing, confounding and country differences.")], className="question-card"),
                html.Div([html.Span("03", className="number"), html.H3("What does the dataset miss?"), html.P("Consider informal work, unpaid care, revisions and differences in national definitions.")], className="question-card"),
            ], className="feature-grid")
        ], className="container")
    ], className="section"),
])
