"""Employment & Inequality page scaffold.

Purpose: examine labor-market effects and differences between worker groups.
"""
from dash import html


def layout():
    return html.Div([
        html.Section([
            html.Div([
                html.Span("ECONOMIC IMPACT · PEOPLE", className="tag"),
                html.H1("Employment & Inequality"),
                html.P("Investigate how jobs and labor-market outcomes changed during the pandemic."),
            ], className="container hero-content")
        ], className="hero hero-subpage"),
        html.Section([
            html.Div([
                html.H2("Labor-market indicators"),
                html.P("TODO: Add unemployment, employment and labor-force participation indicators."),
                html.Div("Employment KPI cards and trend charts will appear here.", className="page-placeholder"),
                html.H2("Who was most affected?"),
                html.P("TODO: Compare age, gender, contract type or other groups where comparable data exists."),
                html.Div("Group comparison charts will appear here.", className="page-placeholder"),
                html.H2("Employment recovery"),
                html.P("TODO: Compare the return of employment indicators to the pre-pandemic baseline."),
            ], className="container section page-container")
        ])
    ])
