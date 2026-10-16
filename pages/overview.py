from dash import html, dcc
from src.visualizations import growth_line, sector_bars, metric_card

layout = html.Div([
    html.Section([
        html.Div([
            html.Span("✨ AN INTERACTIVE LEARNING JOURNEY", className="tag"),
            html.H1("How did a virus reshape the global economy?"),
            html.P("In 2020, the world slowed down almost overnight. Explore what happened to growth, jobs, industries and trade — one interactive chart at a time."),
            html.Div([
                dcc.Link("Start the journey →", href="/economic-impact", className="btn"),
                dcc.Link("How to read data wisely", href="/pandemic-analysis", className="btn btn-ghost"),
            ], className="hero-actions")
        ], className="container hero-content")
    ], className="hero hero-home"),
    html.Div([
        html.Div([
            metric_card("3.1%", "Illustrative world output dip, 2020"),
            metric_card("14.7%", "Illustrative US unemployment peak"),
            metric_card("−60%", "Illustrative air travel activity shock"),
            metric_card("6.0%", "Illustrative global rebound, 2021"),
        ], className="metric-grid"),
        html.Div("DEMO VALUES ONLY · Replace these figures before presenting.", className="data-disclaimer")
    ], className="container metric-overlap"),
    html.Section([
        html.Div([
            html.H2("What you'll discover"),
            html.P("Four stops. Every chart is interactive, so explore the details and ask what each pattern can — and cannot — tell you.", className="section-subtitle"),
            html.Div([
                html.A([html.Span("📉", className="card-icon"), html.H3("Economic impact"), html.P("The sudden fall and rebound of GDP, compared across regions.")], href="/economic-impact", className="feature-card"),
                html.A([html.Span("🦠", className="card-icon"), html.H3("Pandemic analysis"), html.P("Explore the timing of the shock and its links to jobs, sectors and policy.")], href="/pandemic-analysis", className="feature-card"),
                html.A([html.Span("🌱", className="card-icon"), html.H3("Recovery"), html.P("See how recovery paths differed, and why a rebound isn't the whole story.")], href="/recovery", className="feature-card"),
                html.A([html.Span("🧭", className="card-icon"), html.H3("Read data wisely"), html.P("Keep context, uncertainty, comparability and ethics visible.")], href="/pandemic-analysis", className="feature-card"),
            ], className="feature-grid")
        ], className="container")
    ], className="section"),
    html.Section([
        html.Div([
            html.Div([
                html.H2("The big picture, in plain words"),
                html.P("Think of an economy as a giant conversation: people buy, firms produce, workers earn, and money keeps flowing. Lockdowns and uncertainty interrupted many of those conversations at once."),
                html.P("The goal is not just to show numbers, but to help you understand the story behind them.")
            ], className="story-copy"),
            html.Div([
                html.Strong("🌱 A learning mindset"),
                html.P("If a chart surprises you, ask: who is included, over what period, and compared with what? Surprise is where good analysis begins.")
            ], className="callout callout-green")
        ], className="container split")
    ], className="section section-muted"),
])
