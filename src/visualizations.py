"""Plotly chart factory functions for the PandemiScope mock dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

YEARS = [2018, 2019, 2020, 2021, 2022, 2023]
COLORS = {
    "World": "#4a6cf7", "US": "#ff7a59", "Euro area": "#12b886",
    "France": "#7c3aed", "China": "#f0476b", "India": "#f59f00"
}
GDP = {
    "World": [3.6, 2.9, -3.1, 6.1, 3.4, 3.3],
    "US": [2.9, 2.3, -2.8, 5.9, 1.9, 2.5],
    "Euro area": [1.8, 1.6, -6.1, 5.9, 3.4, 0.4],
    "France": [1.8, 1.8, -7.4, 6.4, 2.5, 0.9],
    "China": [6.8, 6.0, 2.2, 8.4, 3.0, 5.2],
    "India": [6.5, 3.9, -5.8, 9.7, 7.0, 8.2],
}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
UNEMPLOYMENT = {
    "US": [3.5, 3.5, 4.4, 14.7, 13.3, 11.1, 10.2, 8.4, 7.8, 6.9, 6.7, 6.7],
    "Euro area": [7.3, 7.3, 7.3, 7.3, 7.5, 7.8, 8.1, 8.4, 8.5, 8.4, 8.4, 8.3],
}
SECTORS = [
    ("Air travel", -60), ("Hospitality", -35), ("Arts & events", -30),
    ("Physical retail", -12), ("Manufacturing", -8), ("Finance", 1),
    ("Healthcare", 3), ("Software & IT", 10), ("E-commerce", 25), ("Delivery", 30)
]

def _style(fig, height=360):
    fig.update_layout(
        template="plotly_white", height=height, margin=dict(l=16, r=16, t=20, b=28),
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#5d6785", size=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.12, x=0),
        hoverlabel=dict(bgcolor="#171d36", font_color="#ffffff"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#e3e8f6")
    fig.update_yaxes(gridcolor="#edf0f8", zeroline=False)
    return fig

def metric_card(value, label):
    from dash import html
    return html.Div([html.Div(value, className="metric-value"), html.Div(label, className="metric-label")], className="metric-card")

def growth_line(regions=None):
    regions = regions or ["World", "US", "China"]
    rows = [{"year": y, "region": region, "growth": GDP[region][i]}
            for region in regions if region in GDP for i, y in enumerate(YEARS)]
    fig = px.line(pd.DataFrame(rows), x="year", y="growth", color="region", markers=True,
                  color_discrete_map=COLORS, labels={"year": "Year", "growth": "Real GDP growth (%)", "region": "Region"})
    fig.add_hline(y=0, line_dash="dash", line_color="#ff7a59", opacity=.8)
    fig.update_traces(line_width=3, marker_size=7)
    fig.update_xaxes(dtick=1)
    return _style(fig)

def year_snapshot(year=2020):
    idx = YEARS.index(year) if year in YEARS else 2
    d = pd.DataFrame({"region": list(GDP.keys()), "growth": [vals[idx] for vals in GDP.values()]})
    d = d.sort_values("growth")
    fig = px.bar(d, x="growth", y="region", orientation="h", color="growth",
                 color_continuous_scale=["#f0476b", "#ffb86b", "#12b886"],
                 labels={"growth": "GDP growth (%)", "region": ""})
    fig.update_layout(coloraxis_showscale=False)
    return _style(fig, 300)

def sector_bars(view="All"):
    d = pd.DataFrame(SECTORS, columns=["sector", "change"])
    if view == "Winners": d = d[d.change > 0]
    elif view == "Losers": d = d[d.change < 0]
    d = d.sort_values("change")
    fig = px.bar(d, x="change", y="sector", orientation="h", color="change",
                 color_continuous_scale=["#f0476b", "#e3e8f6", "#12b886"],
                 labels={"change": "Illustrative activity change (%)", "sector": ""})
    fig.update_layout(coloraxis_showscale=False)
    return _style(fig, max(300, 32 * len(d) + 70))

def unemployment_line(regions=None):
    regions = regions or ["US", "Euro area"]
    rows = [{"month": month, "region": region, "rate": UNEMPLOYMENT[region][i]}
            for region in regions if region in UNEMPLOYMENT for i, month in enumerate(MONTHS)]
    fig = px.line(pd.DataFrame(rows), x="month", y="rate", color="region", markers=True,
                  color_discrete_map={"US": COLORS["US"], "Euro area": COLORS["Euro area"]},
                  labels={"month": "", "rate": "Unemployment rate (%)", "region": ""})
    fig.update_traces(line_width=3, marker_size=5)
    return _style(fig)

def trade_line():
    quarters = ["19Q4", "20Q1", "20Q2", "20Q3", "20Q4", "21Q1", "21Q2", "21Q3"]
    values = [100, 98, 82, 94, 100, 104, 107, 108]
    fig = px.line(pd.DataFrame({"quarter": quarters, "index": values}), x="quarter", y="index",
                  markers=True, labels={"quarter": "", "index": "Trade volume index"})
    fig.update_traces(line_color=COLORS["World"], line_width=3, marker_size=7)
    fig.add_hline(y=100, line_dash="dash", line_color="#ff7a59")
    return _style(fig)

def fiscal_bars():
    d = pd.DataFrame({"country": ["Japan", "United States", "United Kingdom", "Germany", "France", "Italy"],
                      "support": [17, 16, 16, 13, 9, 7]})
    fig = px.bar(d.sort_values("support"), x="support", y="country", orientation="h",
                 labels={"support": "Illustrative support (% GDP)", "country": ""})
    fig.update_traces(marker_color=COLORS["World"])
    return _style(fig, 320)

def recovery_line():
    quarters = ["2019 Q4", "2020 Q1", "2020 Q2", "2020 Q3", "2020 Q4", "2021 Q1", "2021 Q2", "2021 Q3"]
    values = [100, 98, 82, 94, 100, 104, 107, 108]
    d = pd.DataFrame({"quarter": quarters, "activity": values})
    fig = px.area(d, x="quarter", y="activity", labels={"quarter": "", "activity": "Illustrative activity index"})
    fig.update_traces(line_color=COLORS["World"], fillcolor="rgba(74,108,247,.16)")
    fig.add_hline(y=100, line_dash="dash", line_color="#ff7a59")
    return _style(fig)

def recovery_index_bars():
    d = pd.DataFrame({"sector": ["Air travel", "Hospitality", "Retail", "Manufacturing", "Digital services"],
                      "index": [58, 72, 91, 96, 125]})
    fig = px.bar(d.sort_values("index"), x="index", y="sector", orientation="h",
                 color="index", color_continuous_scale=["#f0476b", "#ffb86b", "#12b886"],
                 labels={"index": "Illustrative recovery index (baseline = 100)", "sector": ""})
    fig.update_layout(coloraxis_showscale=False)
    return _style(fig, 300)
