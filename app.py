"""PandemiScope application entry point and shared site navigation.

Page content lives in pages/. Shared filtering controls live here so their
selected values can later be consumed by callbacks on relevant pages.
"""

from dash import Dash, dcc, html, Input, Output

from pages import (
    overview,
    economic_impact,
    country_explorer,
    employment,
    sector_impact,
    trade_tourism,
    government_response,
    pandemic_analysis,
     pandemic_response,
    recovery,
    data_methodology,
)
from src.callbacks import register_callbacks

app = Dash(
    __name__,
    use_pages=False,
    suppress_callback_exceptions=True,
    title="PandemiScope · The Economics of COVID-19",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

# The route registry is the single source of truth for page paths and labels.
PAGE_REGISTRY = [
    {"key": "overview", "label": "Overview", "path": "/", "layout": overview.layout, "group": "Discover"},
    {"key": "country-explorer", "label": "Country Explorer", "path": "/country-explorer", "layout": country_explorer.layout, "group": "Discover"},
    {"key": "economic-impact", "label": "Economic Impact", "path": "/economic-impact", "layout": economic_impact.layout, "group": "Economic Impact"},
    {"key": "employment", "label": "Employment & Inequality", "path": "/employment", "layout": employment.layout, "group": "Economic Impact"},
    {"key": "sector-impact", "label": "Sector Impact", "path": "/sector-impact", "layout": sector_impact.layout, "group": "Economic Impact"},
    {"key": "trade-tourism", "label": "Trade & Tourism", "path": "/trade-tourism", "layout": trade_tourism.layout, "group": "Economic Impact"},
    {"key": "pandemic-analysis", "label": "Pandemic & Economy", "path": "/pandemic-analysis", "layout": pandemic_analysis.layout, "group": "Analysis & Recovery"},
    {"key": "government-response", "label": "Government Response", "path": "/government-response", "layout": government_response.layout, "group": "Analysis & Recovery"},
    {"key": "pandemic-response","label": "Pandemic & Policy","path": "/pandemic-response","layout": pandemic_response.layout,"group": "Analysis & Recovery",},
    {"key": "recovery", "label": "Recovery", "path": "/recovery", "layout": recovery.layout, "group": "Analysis & Recovery"},
    {"key": "data-methodology", "label": "Data & Methodology", "path": "/data-methodology", "layout": data_methodology.layout, "group": "About the Data"},
]

NAV_GROUPS = ["Discover", "Economic Impact", "Analysis & Recovery", "About the Data"]


def build_navigation():
    """Create grouped dropdown navigation; assets/navigation-dropdowns.js manages closing behavior."""
    groups = []
    for group_name in NAV_GROUPS:
        links = [
            dcc.Link(
                page["label"],
                href=page["path"],
                id=f"nav-{page['key']}",
                className="nav-link",
            )
            for page in PAGE_REGISTRY
            if page["group"] == group_name
        ]
        groups.append(
            html.Details(
                [html.Summary(group_name, className="nav-group-label"), html.Div(links, className="nav-dropdown")],
                className="nav-group",
            )
        )
    return html.Nav(groups, className="nav-links", **{"aria-label": "Main navigation"})


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        # Shared filter state; page callbacks can consume this store as they are developed.
        dcc.Store(
            id="global-filters",
            data={"countries": ["World", "France", "United States"], "start_year": 2019, "end_year": 2023},
        ),
        html.Div(id="scroll-progress", className="scroll-progress"),
        html.Header(
            [
                html.Div(
                    [
                        dcc.Link(["📊 Pandemi", html.B("Scope")], href="/", className="logo"),
                        build_navigation(),
                        html.Button("🌓", id="theme-toggle", title="Toggle theme", className="theme-toggle"),
                    ],
                    className="nav-wrap",
                )
            ],
            className="site-header",
        ),
        # Shared controls are visible across the site. They store selections now;
        # individual page charts will connect to these values in later development.
        html.Main(id="page-content"),
        html.Footer(
            [
                html.Div(
                    [
                        html.Strong("PandemiScope"),
                        html.Span("A student data-storytelling project about the economics of COVID-19."),
                        html.P("Illustrative values must be replaced with verified observations and cited sources before presenting findings."),
                    ],
                    className="footer-inner",
                )
            ],
            className="site-footer",
        ),
        html.Div(id="toast", className="toast"),
    ],
    id="app-root",
    className="theme-dark",  # Launch in dark mode by default.
)


# Route changes swap the page layout and update the active navigation link.
route_outputs = [Output("page-content", "children")] + [
    Output(f"nav-{page['key']}", "className") for page in PAGE_REGISTRY
]


@app.callback(route_outputs, Input("url", "pathname"))
def render_page(pathname):
    pathname = pathname or "/"
    current_page = next((page for page in PAGE_REGISTRY if page["path"] == pathname), PAGE_REGISTRY[0])
    active_classes = [
        "nav-link active" if page["path"] == current_page["path"] else "nav-link"
        for page in PAGE_REGISTRY
    ]
    page_layout = current_page["layout"]
    rendered_page = page_layout() if callable(page_layout) else page_layout
    return [rendered_page, *active_classes]


def save_global_filters(countries, date_range):
    start_year, end_year = (date_range or "2019:2023").split(":", maxsplit=1)
    return {
        "countries": countries or [],
        "start_year": int(start_year),
        "end_year": int(end_year),
    }


register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
