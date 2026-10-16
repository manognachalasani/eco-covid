from dash import Dash, dcc, html, Input, Output
from pages import overview, economic_impact, pandemic_analysis, recovery
from src.callbacks import register_callbacks

app = Dash(
    __name__,
    use_pages=False,
    suppress_callback_exceptions=True,
    title="PandemiScope · The Economics of COVID-19",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

NAV = [
    ("overview", "Home", "/"),
    ("economic-impact", "Economic impact", "/economic-impact"),
    ("pandemic-analysis", "Pandemic analysis", "/pandemic-analysis"),
    ("recovery", "Recovery", "/recovery"),
]

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="global-filters", data={"regions": ["World", "US", "Euro area"], "year": 2020}),
    html.Div(id="scroll-progress", className="scroll-progress"),
    html.Header([
        html.Div([
            dcc.Link(["📊 Pandemi", html.B("Scope")], href="/", className="logo"),
            html.Nav([
                dcc.Link(label, href=href, id=f"nav-{key}", className="nav-link")
                for key, label, href in NAV
            ], className="nav-links"),
            html.Button("🌓", id="theme-toggle", title="Toggle theme", className="theme-toggle"),
        ], className="nav-wrap")
    ], className="site-header"),
    html.Main(id="page-content"),
    html.Footer([
        html.Div([
            html.Strong("PandemiScope"),
            html.Span("A student mock-up for CentraleDigitalLab Data Storytelling."),
            html.P("All figures are illustrative placeholders. Replace with verified datasets and cite sources before presenting.")
        ], className="footer-inner")
    ], className="site-footer"),
    html.Div(id="toast", className="toast"),
], id="app-root")

@app.callback(
    Output("page-content", "children"),
    Output("nav-overview", "className"),
    Output("nav-economic-impact", "className"),
    Output("nav-pandemic-analysis", "className"),
    Output("nav-recovery", "className"),
    Input("url", "pathname"),
)
def render_page(pathname):
    pathname = pathname or "/"
    page_map = {
        "/": overview.layout,
        "/economic-impact": economic_impact.layout,
        "/pandemic-analysis": pandemic_analysis.layout,
        "/recovery": recovery.layout,
    }
    keys = ["/", "/economic-impact", "/pandemic-analysis", "/recovery"]
    active = pathname if pathname in keys else "/"
    classes = ["nav-link active" if p == active else "nav-link" for p in keys]
    return page_map.get(pathname, overview.layout), *classes

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
