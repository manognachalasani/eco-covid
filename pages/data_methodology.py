"""Data & Methodology page.

A story-style page (same look as the Economic Impact and Employment chapters)
that explains, in plain words:
  * which data sources were used and what was taken from each one,
  * how the final dataset (one row per country and month) was built,
  * what the numbers can and cannot tell us.

Content mirrors covid_economy_final.ipynb.

Files used by this page (put all three in the Dash ``assets/`` folder):
  * data_methodology.css : styles, all scoped to ``.methodology-story``
  * data_methodology.js  : intro animation, scroll reveals, reading progress
  * style.css            : global theme (not modified)

To change the text, edit the data blocks (SOURCES, STEPS, ...). The layout
functions below them should not need to change.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from dash import html

__all__ = ["layout"]

# ------------------------------------------------------------------ constants
ROOT_ID = "methodology-story"            # must match data_methodology.js
INTRO_ID = "methodology-chapter-intro"   # must match data_methodology.js
PROGRESS_ID = "methodology-progress-fill"  # must match data_methodology.js

ACCESS_DATE = "October 2026"
START_YEAR, END_YEAR = 2015, 2024
N_COUNTRIES_ALL = 237
N_COUNTRIES_DASHBOARD = 10
N_COLUMNS = 70
N_MONTHS = (END_YEAR - START_YEAR + 1) * 12  # 120


# ---------------------------------------------------------------- data models
@dataclass(frozen=True)
class Step:
    title: str
    text: str


@dataclass(frozen=True)
class Source:
    tag: str
    name: str
    took: str
    covers: str
    frequency: str
    note: str
    url: str
    url_label: str
    used: bool = True


@dataclass(frozen=True)
class Measure:
    name: str
    column: str
    meaning: str


@dataclass(frozen=True)
class Caveat:
    title: str
    text: str


# -------------------------------------------------------------------- content
STEPS: tuple[Step, ...] = (
    Step("Download", "Each source is fetched from its public website or API. A source that fails is skipped, never guessed."),
    Step("Clean", "Totals such as \"World\" are removed, errors are fixed and everything gets the same format."),
    Step("Join", "All sources are placed in one table with one row for each country and each month."),
    Step("Add summaries", "A few simple measures are calculated per country, such as total COVID deaths and the 2020 GDP shock."),
    Step("Select", "The 5 biggest and 5 smallest economies are kept for the main dashboard."),
)

SOURCES: tuple[Source, ...] = (
    Source(
        "COVID & RULES", "Our World in Data",
        "COVID cases and deaths, government strictness (Oxford index), vaccination, excess deaths, population, and country traits such as median age, hospital beds and life expectancy.",
        "All countries", "Daily, turned into monthly", "Data stops in August 2024.",
        "https://github.com/owid/covid-19-data", "github.com/owid/covid-19-data",
    ),
    Source(
        "EUROPE", "Eurostat",
        "Unemployment (total and youth), inflation, industrial production, retail sales and real GDP.",
        "About 30 European countries", "Monthly and quarterly", "Production, retail and GDP are rescaled so that 2019 = 100.",
        "https://ec.europa.eu/eurostat", "ec.europa.eu/eurostat",
    ),
    Source(
        "UNITED STATES", "FRED",
        "Ten US series: prices, consumer spending, unemployment, money supply, interest rate, GDP and investment.",
        "United States only", "Monthly and quarterly", "Columns start with us_.",
        "https://fred.stlouisfed.org", "fred.stlouisfed.org",
    ),
    Source(
        "FRANCE", "INSEE",
        "Three French series: unemployment rate, consumer prices and GDP.",
        "France only", "Monthly and quarterly", "INSEE no longer updates these series. Columns start with fr_.",
        "https://www.insee.fr/fr/statistiques/series", "insee.fr",
    ),
    Source(
        "WHOLE WORLD", "World Bank",
        "GDP, GDP growth, GDP per person, unemployment, inflation, and the income group of each country.",
        "217 countries", "Yearly", "Columns start with wb_.",
        "https://data.worldbank.org", "data.worldbank.org",
    ),
    Source(
        "TESTED, NOT USED", "Mendeley Data",
        "Two research datasets were tested, but nothing from them is in the final table.",
        "OECD / 58 countries", "As published", "They have no usable country column, so they could not be joined.",
        "https://data.mendeley.com/datasets/gtzzs3659m/1", "data.mendeley.com",
        used=False,
    ),
)

# (time scale, what we do with it, examples)
TIME_SCALES: tuple[tuple[str, str, str], ...] = (
    ("Daily", "Added up or averaged into months.", "COVID cases, deaths, strictness"),
    ("Monthly", "Used as it is.", "Unemployment, prices, retail sales"),
    ("Quarterly", "Repeated on each month of the quarter.", "GDP"),
    ("Yearly", "Repeated on each of the 12 months.", "World Bank indicators"),
)

MEASURES: tuple[Measure, ...] = (
    Measure("Total COVID deaths", "cum_deaths_per_million",
            "COVID deaths per million people, added up over 2020-2022."),
    Measure("2020 GDP shock", "gdp_shock_2020",
            "GDP growth in 2020 minus the country's usual growth in 2015-2019. Negative means worse than normal."),
    Measure("Severity", "severity",
            "Countries sorted by total deaths and split into 4 equal groups: Low, Medium, High, Very high."),
    Measure("Impact profile", "impact_profile",
            "Deaths and GDP shock compared with the middle country. Gives 4 groups, from \"high deaths, big GDP hit\" to \"low deaths, resilient economy\"."),
    Measure("Period", "period",
            "Before March 2020, March 2020 to February 2022, and after. The dates are approximate."),
)

SELECTION_RULES: tuple[str, ...] = (
    "Rank countries by total GDP in 2019.",
    "Keep only countries with COVID deaths data, a 2020 GDP figure and at least 1 million people.",
    "Take the 5 biggest and the 5 smallest economies.",
)
TOP_COUNTRIES: tuple[str, ...] = ("United States", "China", "Japan", "Germany", "United Kingdom")
BOTTOM_COUNTRIES: tuple[str, ...] = ("Lesotho", "Central African Republic", "East Timor", "Gambia", "Guinea-Bissau")

# (prefix, what it contains, where it comes from)
PREFIXES: tuple[tuple[str, str, str], ...] = (
    ("no prefix", "COVID data, country traits and our own summaries", "OWID and our calculations"),
    ("eu_", "Economy of European countries", "Eurostat"),
    ("wb_", "Yearly economy of each country", "World Bank"),
    ("us_", "US economy (filled on USA rows only)", "FRED"),
    ("fr_", "French economy (filled on FRA rows only)", "INSEE"),
)

CAVEATS: tuple[Caveat, ...] = (
    Caveat("Not every country has the same data.",
           "Europe, the US and France have extra series. Other countries do not."),
    Caveat("Empty means no data.",
           "Missing values are never filled with guesses and never turned into zero. The only zeros are COVID counts before 2020."),
    Caveat("The 10 countries are not the whole world.",
           "They show a contrast between big and small economies, not middle-income countries. France is not among them, so its fr_ columns are empty in the main file."),
    Caveat("COVID numbers are not equally reliable.",
           "Case counts depend on testing. Poor countries may report fewer deaths, which can mean less reporting, not less impact."),
    Caveat("Time scales are mixed.",
           "Yearly and quarterly values are repeated on each month, so they do not show monthly changes."),
    Caveat("Labels are relative.",
           "Severity and impact profile compare countries with each other and would change with another set of countries."),
    Caveat("Correlation is not causation.",
           "A link between deaths, strictness and GDP does not prove that one caused the other. Income, tourism and age also matter."),
    Caveat("Data can change.",
           "Statistical offices revise their numbers, so a new download may give slightly different values."),
)

TAKEAWAYS: tuple[str, ...] = (
    "Empty means no data, never zero.",
    "Compare trends inside one source, not levels across sources.",
    "Deaths, strictness and GDP moving together does not prove cause.",
    "The 10 countries show a contrast, not the whole world.",
)

JUMP_LINKS: tuple[tuple[str, str], ...] = (
    ("#method-how", "How it was built"),
    ("#method-sources", "Sources"),
    ("#method-fit", "How they fit"),
    ("#method-measures", "Our measures"),
    ("#method-countries", "The 10 countries"),
    ("#method-caution", "Keep in mind"),
)


# ------------------------------------------------------------ small builders
def _external_link(url: str, label: str) -> html.A:
    return html.A(label, href=url, target="_blank", rel="noopener noreferrer", className="method-link")


def _eyebrow(text: str) -> html.Div:
    return html.Div(text, className="method-eyebrow")


def _section(number: int, eyebrow: str, title: str, description: str,
             body: Sequence, *, anchor: str, muted: bool = False) -> html.Section:
    """One numbered story section: a header followed by its content."""
    classes = "method-section" + (" method-section-muted" if muted else "")
    return html.Section(
        html.Div([
            html.Div([
                html.Div(f"{number:02d}", className="method-number"),
                html.Div([
                    _eyebrow(eyebrow),
                    html.H2(title, className="method-heading"),
                    html.P(description, className="method-description"),
                ]),
            ], className="method-section-header reveal"),
            *body,
        ], className="method-container"),
        id=anchor, className=classes,
    )


def _intro_overlay() -> html.Div:
    """Short cinematic opening. Removed by data_methodology.js after it plays."""
    return html.Div([
        html.Div(className="method-intro-backdrop"),
        html.Div(className="method-intro-scanline"),
        html.Div(className="method-intro-streak"),
        html.Div([html.Span(className=f"method-spark method-spark-{n}") for n in (1, 2, 3)],
                 className="method-intro-particles"),
        html.Div([
            html.Div("DATA", className="method-intro-word"),
            html.Div("PANDEMISCOPE · BEHIND THE DATA", className="method-intro-eyebrow"),
            html.H2([
                html.Span("Where the data", className="method-intro-line"),
                html.Span(html.Span("comes from", className="method-accent"), className="method-intro-line"),
            ], className="method-intro-title"),
            html.P("Sources, steps and limits, explained simply.", className="method-intro-subtitle"),
        ], className="method-intro-content"),
    ], id=INTRO_ID, className="method-intro-overlay")


def _hero() -> html.Section:
    stats = (
        ("6", "public sources", "cyan"),
        (f"{N_COUNTRIES_ALL} → {N_COUNTRIES_DASHBOARD}", "countries downloaded, then kept in the dashboard", "purple"),
        (f"{START_YEAR}-{END_YEAR}", "period covered, month by month", "green"),
        (f"{N_COLUMNS}", "columns in the final table", "coral"),
    )
    return html.Section([
        html.Div(className="method-grid"),
        html.Div(className="method-orb method-orb-one"),
        html.Div(className="method-orb method-orb-two"),
        html.Div([
            html.Div("DATA", className="method-hero-word"),
            html.Div("ABOUT THE DATA · TRANSPARENCY", className="method-kicker"),
            html.H1([
                html.Span("Where the data", className="method-title-line"),
                html.Span(html.Span("comes from", className="method-accent"), className="method-title-line"),
            ], className="method-title"),
            html.P("What we used, what we took from each source, and how it became one clean table with a row for every country and every month.",
                   className="method-lead"),
            html.Nav([html.A(label, href=href, className="method-jump-link") for href, label in JUMP_LINKS],
                     className="method-jump", **{"aria-label": "Jump to a section"}),
            html.Div([
                html.Div([
                    html.Div(value, className=f"method-stat-value accent-{accent}"),
                    html.P(label, className="method-stat-label"),
                ], className="method-stat") for value, label, accent in stats
            ], className="method-stats"),
            html.Div([
                html.Span("DATA NOTE", className="method-note-label"),
                html.P(f"All data was downloaded in {ACCESS_DATE}. Check each publisher's terms of use before reusing it.",
                       className="method-note-text"),
            ], className="method-note"),
            html.Div([
                html.Span(className="method-live-dot"),
                html.Span("SCROLL TO READ"),
                html.Span("↓", className="method-scroll-arrow"),
            ], className="method-scroll-cue"),
        ], className="method-hero-inner"),
    ], className="method-hero")


# ------------------------------------------------------------------- sections
def _how_section() -> html.Section:
    steps = html.Ol([
        html.Li([
            html.Span(f"{i}", className="method-step-number"),
            html.H3(step.title, className="method-step-title"),
            html.P(step.text, className="method-step-text"),
        ], className="method-step reveal") for i, step in enumerate(STEPS, start=1)
    ], className="method-steps")
    return _section(
        1, "THE PIPELINE", "How the dataset was built",
        "Five simple steps, from the raw files to the table the dashboard reads. The whole process is written in one notebook, so it can be run again.",
        [steps], anchor="method-how",
    )


def _source_card(source: Source) -> html.Article:
    return html.Article([
        html.Div(source.tag, className="method-card-tag"),
        html.H3(source.name, className="method-card-title"),
        html.P(source.took, className="method-card-text"),
        html.Dl([
            html.Div([html.Dt("Covers"), html.Dd(source.covers)]),
            html.Div([html.Dt("Time scale"), html.Dd(source.frequency)]),
        ], className="method-facts"),
        html.P(source.note, className="method-card-note"),
        _external_link(source.url, source.url_label),
    ], className="method-card reveal" + ("" if source.used else " method-card-muted"))


def _sources_section() -> html.Section:
    return _section(
        2, "WHAT WE TOOK", "Six sources, one purpose each",
        "Each source covers a different part of the story: health, rules, jobs, prices and growth. Here is what we kept from each.",
        [html.Div([_source_card(s) for s in SOURCES], className="method-source-grid")],
        anchor="method-sources", muted=True,
    )


def _fit_section() -> html.Section:
    ladder = html.Div([
        _eyebrow("TIME SCALES"),
        html.H3("Everything is lined up on months", className="method-panel-title"),
        html.P("Sources do not all use the same time scale, so each one is adjusted before the join.",
               className="method-panel-text"),
        html.Div([
            html.Div([
                html.Span(scale, className="method-scale-chip"),
                html.Div([
                    html.Strong(rule),
                    html.Span(examples),
                ], className="method-scale-text"),
            ], className="method-scale-row") for scale, rule, examples in TIME_SCALES
        ], className="method-scale-list"),
    ], className="method-panel reveal")

    grid = html.Div([
        _eyebrow("THE FINAL GRID"),
        html.H3("One row per country and month", className="method-panel-title"),
        html.Div([
            html.Div([html.Span(f"{N_COUNTRIES_DASHBOARD}", className="accent-cyan"), " countries × ",
                      html.Span(f"{N_MONTHS}", className="accent-purple"), " months = ",
                      html.Span(f"{N_COUNTRIES_DASHBOARD * N_MONTHS:,}", className="accent-green"), " rows"],
                     className="method-equation"),
            html.Div([html.Span(f"{N_COUNTRIES_ALL}", className="accent-cyan"), " countries × ",
                      html.Span(f"{N_MONTHS}", className="accent-purple"), " months = ",
                      html.Span(f"{N_COUNTRIES_ALL * N_MONTHS:,}", className="accent-green"), " rows (all-countries file)"],
                     className="method-equation method-equation-small"),
        ], className="method-equations"),
        html.Div([
            html.Span("OUR RULE", className="method-callout-label"),
            html.P("We never fill gaps with guesses. If a value is missing, the cell stays empty.",
                   className="method-callout-text"),
        ], className="method-callout"),
        html.P("US and France series only fill the rows of those two countries.", className="method-panel-text"),
    ], className="method-panel reveal")

    return _section(
        3, "PUTTING IT TOGETHER", "How the sources fit together",
        "The table starts as every country crossed with every month, from January 2015 to December 2024. Each source is then joined onto it.",
        [html.Div([ladder, grid], className="method-two-column")], anchor="method-fit",
    )


def _measures_section() -> html.Section:
    rows = html.Div([
        html.Div([
            html.Span(f"{i}", className="method-row-index"),
            html.Div([
                html.H3(m.name, className="method-row-title"),
                html.P(m.meaning, className="method-row-text"),
            ]),
            html.Code(m.column, className="method-code"),
        ], className="method-row") for i, m in enumerate(MEASURES, start=1)
    ], className="method-rows")
    return _section(
        4, "CALCULATED BY US", "Measures that are not in any source",
        "These columns were calculated in the notebook from the sources above. The column name is shown on the right.",
        [html.Div(rows, className="method-panel reveal")], anchor="method-measures", muted=True,
    )


def _country_list(title: str, countries: Sequence[str], accent: str) -> html.Div:
    return html.Div([
        _eyebrow(title),
        html.Ul([
            html.Li([html.Span(f"{i}", className=f"method-rank accent-{accent}"), name])
            for i, name in enumerate(countries, start=1)
        ], className="method-country-list"),
    ], className="method-panel reveal")


def _countries_section() -> html.Section:
    rules = html.Div([
        _eyebrow("SELECTION RULES"),
        html.Ol([html.Li(rule) for rule in SELECTION_RULES], className="method-rule-list"),
        html.P("The population rule matters: without it, the smallest economies would only be tiny islands.",
               className="method-panel-text"),
    ], className="method-panel reveal")
    return _section(
        5, "THE SELECTION", f"Why only {N_COUNTRIES_DASHBOARD} countries",
        f"The full table has {N_COUNTRIES_ALL} countries. The main dashboard keeps the richest and the poorest economies to make the contrast clear. The full table is saved separately.",
        [html.Div([
            rules,
            _country_list("5 BIGGEST ECONOMIES", TOP_COUNTRIES, "cyan"),
            _country_list("5 SMALLEST ECONOMIES", BOTTOM_COUNTRIES, "coral"),
        ], className="method-three-column")],
        anchor="method-countries",
    )


def _columns_section() -> html.Section:
    table = html.Div(
        html.Table([
            html.Thead(html.Tr([html.Th("Prefix"), html.Th("What it contains"), html.Th("Source")])),
            html.Tbody([
                html.Tr([html.Td(html.Code(prefix, className="method-code")), html.Td(contains), html.Td(source)])
                for prefix, contains, source in PREFIXES
            ]),
        ], className="method-table"),
        className="method-table-wrap",
    )
    return _section(
        6, "READING THE TABLE", "What the column names tell you",
        "A prefix shows where a column comes from. The data dictionary file lists all columns with their meaning and unit.",
        [html.Div(table, className="method-panel reveal")], anchor="method-columns", muted=True,
    )


def _caution_section() -> html.Section:
    cards = html.Div([
        html.Div([
            html.Span(f"{i:02d}", className="method-caveat-index"),
            html.H3(c.title, className="method-caveat-title"),
            html.P(c.text, className="method-caveat-text"),
        ], className="method-caveat reveal") for i, c in enumerate(CAVEATS, start=1)
    ], className="method-caveat-grid")
    return _section(
        7, "READ WITH CARE", "What the data cannot tell you",
        "Good analysis also says where it stops. Keep these points in mind when you read the charts.",
        [cards], anchor="method-caution",
    )


def _closing() -> html.Section:
    return html.Section(
        html.Div([
            _eyebrow("IN SHORT"),
            html.H2([
                html.Span("Read the charts", className="method-closing-line"),
                html.Span(html.Span("with these in mind", className="method-accent"), className="method-closing-line"),
            ], className="method-closing-title"),
            html.P("The dataset is built from public sources, step by step, with no guessed values. It is a good tool for comparing patterns, and a poor tool for proving causes.",
                   className="method-closing-description"),
            html.Div([
                html.Div([html.Span(f"{i}", className="method-closing-number"), html.P(text)])
                for i, text in enumerate(TAKEAWAYS, start=1)
            ], className="method-closing-steps"),
            html.Div(f"Data downloaded in {ACCESS_DATE} · Built with covid_economy_final.ipynb",
                     className="method-closing-label"),
        ], className="method-closing-inner reveal"),
        className="method-closing",
    )


# --------------------------------------------------------------------- layout
def layout() -> html.Div:
    """Return the full page. Register it as the page layout in your Dash app."""
    return html.Div([
        html.Div(html.Div(id=PROGRESS_ID), className="method-progress-track"),
        _intro_overlay(),
        _hero(),
        _how_section(),
        _sources_section(),
        _fit_section(),
        _measures_section(),
        _countries_section(),
        _columns_section(),
        _caution_section(),
        _closing(),
    ], id=ROOT_ID, className="methodology-story")