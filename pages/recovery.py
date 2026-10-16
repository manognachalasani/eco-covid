from dash import html, dcc
from src.visualizations import recovery_line, recovery_index_bars

layout = html.Div([
    html.Section([
        html.Div([
            html.Span("PAGE 03 · AFTER THE SHOCK", className="tag"),
            html.H1("Recovery: more than a bounce"),
            html.P("A headline rebound can hide persistent gaps. Compare growth, employment and sector activity to understand whether recovery was broad-based.")
        ], className="container hero-content")
    ], className="hero hero-subpage"),
    html.Section([
        html.Div([
            html.Div([
                html.H2("The recovery path"),
                html.P("Explore the illustrative return toward pre-pandemic activity.", className="section-subtitle"),
                dcc.Graph(figure=recovery_line(), config={"displayModeBar": False}),
                html.Span("Illustrative index · baseline = 100", className="chart-caption")
            ], className="panel"),
            html.Div([
                html.H2("Recovery is uneven"),
                html.P("Illustrative activity index by sector. Replace with comparable real measures.", className="section-subtitle"),
                dcc.Graph(figure=recovery_index_bars(), config={"displayModeBar": False}),
                html.Div("Compare both the depth of the shock and the time required to recover.", className="callout callout-green")
            ], className="panel")
        ], className="container split")
    ], className="section"),
    html.Section([
        html.Div([
            html.H2("A useful recovery checklist"),
            html.P("Before claiming that an economy has recovered, check multiple dimensions.", className="section-subtitle"),
            html.Div([
                html.Div([html.H3("Output"), html.P("Has real GDP returned to its pre-shock level and trend?")], className="check-card"),
                html.Div([html.H3("Employment"), html.P("Have employment, hours worked and labor-force participation recovered?")], className="check-card"),
                html.Div([html.H3("Distribution"), html.P("Did recovery reach sectors and groups that were hit hardest?")], className="check-card"),
                html.Div([html.H3("Prices & public debt"), html.P("What changed in inflation, debt and household purchasing power?")], className="check-card"),
            ], className="feature-grid")
        ], className="container")
    ], className="section section-muted"),
    html.Section([
        html.Div([
            html.H2("Draft your evidence-based takeaway"),
            html.P("Use this space to structure a finding. This is a prototype input and does not save to a database.", className="section-subtitle"),
            dcc.Textarea(id="recovery-takeaway", placeholder="Our evidence suggests… The indicator shows… This interpretation is limited by…", className="takeaway-input"),
            html.Button("Preview takeaway", id="preview-takeaway", className="btn btn-primary"),
            html.Div(id="takeaway-preview", className="takeaway-preview")
        ], className="container panel")
    ], className="section"),
])
