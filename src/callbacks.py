
"""Callbacks are kept separate from page layouts to keep app.py readable."""

from dash import Input, Output, State, html
from src.visualizations import unemployment_line


def register_callbacks(app):

    @app.callback(
        Output("unemployment-chart", "figure"),
        Input("jobs-region-filter", "value"),
    )
    def update_jobs(regions):
        return unemployment_line(regions or ["US"])

    @app.callback(
        Output("takeaway-preview", "children"),
        Input("preview-takeaway", "n_clicks"),
        State("recovery-takeaway", "value"),
        prevent_initial_call=True,
    )
    def preview_takeaway(n, value):
        if not value or not value.strip():
            return html.Div(
                "Write a takeaway first.",
                className="preview-empty",
            )

        return html.Div(
            [
                html.Strong("Preview · team finding"),
                html.P(value.strip()),
            ],
            className="preview-card",
        )

    @app.callback(
        Output("app-root", "className"),
        Input("theme-toggle", "n_clicks"),
        State("app-root", "className"),
    )
    def toggle_theme(n, current):
        if not n:
            return current or "theme-light"

        return (
            "theme-dark"
            if current != "theme-dark"
            else "theme-light"
        )
