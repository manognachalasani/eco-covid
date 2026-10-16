"""Sector Impact page scaffold.

Purpose: compare the depth of the shock and recovery across industries.
"""
from dash import html


def layout():
    return html.Div([
        html.Section([
            html.Div([
                html.Span("ECONOMIC IMPACT · INDUSTRIES", className="tag"),
                html.H1("Sector Impact"),
                html.P("Explore how the pandemic affected industries in different ways."),
            ], className="container hero-content")
        ], className="hero hero-subpage"),
        html.Section([
            html.Div([
                html.H2("Industry comparison"),
                html.P("TODO: Compare sector output, value added or employment using consistent measures."),
                html.Div("Sector comparison chart will appear here.", className="page-placeholder"),
                html.H2("Winners, losses and exposure"),
                html.P("TODO: Add filterable rankings and explain the indicator used for each ranking."),
                html.Div("Sector ranking and detail table will appear here.", className="page-placeholder"),
                html.H2("Recovery by sector"),
                html.P("TODO: Compare sector-level recovery paths and time to baseline."),
            ], className="container section page-container")
        ])
    ])
