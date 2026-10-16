"""Country Explorer page scaffold.

Purpose: compare economic indicators across countries and regions.
This file intentionally contains structure only; charts and data logic come later.
"""
from dash import html


def layout():
    return html.Div([
        html.Section([
            html.Div([
                html.Span("DISCOVER · COUNTRIES", className="tag"),
                html.H1("Country Explorer"),
                html.P("Explore how the economic impact of COVID-19 differed across countries and regions."),
            ], className="container hero-content")
        ], className="hero hero-subpage"),
        html.Section([
            html.Div([
                html.H2("Country profile"),
                html.P("TODO: Summarize the selected country's indicators and data coverage."),
                html.Div("Country KPI cards will appear here.", className="page-placeholder"),
                html.H2("Compare countries"),
                html.P("TODO: Add multi-country trend charts and a sortable comparison table."),
                html.Div("Country comparison charts and table will appear here.", className="page-placeholder"),
                html.H2("Country timeline"),
                html.P("TODO: Show economic changes over the selected time period."),
            ], className="container section page-container")
        ])
    ])
