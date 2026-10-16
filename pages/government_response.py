"""Government Response page scaffold.

Purpose: document economic support measures and compare them carefully with outcomes.
"""
from dash import html


def layout():
    return html.Div([
        html.Section([
            html.Div([
                html.Span("ANALYSIS & RECOVERY · POLICY", className="tag"),
                html.H1("Government Response"),
                html.P("Explore the policy measures governments used to cushion the economic shock."),
            ], className="container hero-content")
        ], className="hero hero-subpage"),
        html.Section([
            html.Div([
                html.H2("Fiscal and economic support"),
                html.P("TODO: Summarize support measures using a clearly defined and comparable metric."),
                html.Div("Policy indicator cards and charts will appear here.", className="page-placeholder"),
                html.H2("Compare policy responses"),
                html.P("TODO: Compare country responses while documenting differences in definitions and coverage."),
                html.Div("Policy comparison table will appear here.", className="page-placeholder"),
                html.H2("Policy and outcomes"),
                html.P("TODO: Explore associations without treating correlations as proof of policy effectiveness."),
            ], className="container section page-container")
        ])
    ])
