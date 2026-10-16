"""Trade & Tourism page scaffold.

Purpose: examine changes in international trade and travel-related activity.
"""
from dash import html


def layout():
    return html.Div([
        html.Section([
            html.Div([
                html.Span("ECONOMIC IMPACT · CROSS-BORDER ACTIVITY", className="tag"),
                html.H1("Trade & Tourism"),
                html.P("Explore how cross-border goods, services and travel activity changed during COVID-19."),
            ], className="container hero-content")
        ], className="hero hero-subpage"),
        html.Section([
            html.Div([
                html.H2("Imports and exports"),
                html.P("TODO: Add trade-volume and trade-value trends with units and source notes."),
                html.Div("Trade time-series charts will appear here.", className="page-placeholder"),
                html.H2("Tourism and travel"),
                html.P("TODO: Explore international arrivals, receipts or other available tourism indicators."),
                html.Div("Tourism indicators will appear here.", className="page-placeholder"),
                html.H2("Cross-country comparison"),
                html.P("TODO: Compare the scale and timing of disruption across selected countries."),
            ], className="container section page-container")
        ])
    ])
