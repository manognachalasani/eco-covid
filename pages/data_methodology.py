"""Data & Methodology page scaffold.

Purpose: make sources, definitions, transformations and limitations transparent.
"""
from dash import html


def layout():
    return html.Div([
        html.Section([
            html.Div([
                html.Span("ABOUT THE DATA · TRANSPARENCY", className="tag"),
                html.H1("Data & Methodology"),
                html.P("Understand where the data comes from, how indicators are defined, and what the analysis can and cannot claim."),
            ], className="container hero-content")
        ], className="hero hero-subpage"),
        html.Section([
            html.Div([
                html.H2("Data sources"),
                html.P("TODO: List datasets, publishers, source links, access dates and licenses."),
                html.Div("Dataset source catalogue will appear here.", className="page-placeholder"),
                html.H2("Definitions and processing"),
                html.P("TODO: Document units, time frequency, country coverage, cleaning and aggregation."),
                html.Div("Indicator dictionary and processing notes will appear here.", className="page-placeholder"),
                html.H2("Limitations and responsible interpretation"),
                html.P("TODO: Explain missing data, revisions, comparability limits, uncertainty and correlation-versus-causation."),
                html.Div("Limitations and interpretation notes will appear here.", className="page-placeholder"),
            ], className="container section page-container")
        ])
    ])
