import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


##########################  ROXANE WORK



FOCUS = ['United States', 'United Kingdom', 'China']
FOCUS_ECON = ['United Kingdom', 'United States', 'China', 'Lesotho']
COLORS = {'United States':'#2764AB','United Kingdom':'#E05B49','China':'#329785',
          'Lesotho':'#9164B7','Germany':'#D99C38','Japan':'#557385',
          'Gambia':'#B06C81','Guinea-Bissau':'#798747',
          'Central African Republic':'#8B7865','East Timor':'#777777'}
INK = '#24334B'


def _date(df):
    x=df.copy()
    x['date']=pd.to_datetime(x['date'], dayfirst=True, errors='coerce')
    return x


def _annual(df, measure):
    x=df[['country','year',measure]].dropna().copy()
    x['year']=x['year'].astype(int)
    bad=x.groupby(['country','year'])[measure].nunique()
    if (bad>1).any():
        raise ValueError(f'{measure}: multiple values for a country/year')
    return x.drop_duplicates(['country','year']).sort_values(['country','year'])


def _country(df, measure):
    x=df[['country',measure]].dropna().copy()
    bad=x.groupby('country')[measure].nunique()
    if (bad>1).any():
        raise ValueError(f'{measure}: multiple values for a country')
    return x.drop_duplicates('country')


def _style(fig, height=490, legend=True):
    fig.update_layout(template='plotly_white', font=dict(family='Arial',color=INK),
                      title_font=dict(size=19),height=height,
                      hovermode='x unified', margin=dict(l=55,r=35,t=80,b=85),
                      showlegend=legend, legend=dict(orientation='h',y=-0.22,x=0,xanchor='left'))
    return fig


def _line(df, measure, countries, title, ylabel, start=None, end=None, annual=False):
    data=_annual(df,measure) if annual else _date(df)[['country','date',measure]].dropna()
    xcol='year' if annual else 'date'
    if start is not None:
        data=data[data[xcol]>= (int(start) if annual else pd.Timestamp(start))]
    if end is not None:
        data=data[data[xcol]<= (int(end) if annual else pd.Timestamp(end))]
    if countries is not None:
        data=data[data.country.isin(countries)]
    data=data.sort_values(['country',xcol])
    fig=px.line(data,x=xcol,y=measure,color='country',markers=annual,
                color_discrete_map=COLORS,title=title,
                labels={xcol:'Year' if annual else 'Date',measure:ylabel,'country':'Country'})
    _style(fig)
    if annual: fig.update_xaxes(dtick=1)
    return fig


def _rank(data, measure, title, xlabel, midpoint=None, suffix='', highlight=None):
    data=data.sort_values(measure).copy()
    data['bar_color']=data['country'].apply(lambda c: COLORS.get(c,'#688398') if highlight is None or c in highlight else '#B5C2CC')
    fig=go.Figure(go.Bar(x=data[measure],y=data['country'],orientation='h',
                         marker_color=data['bar_color'],
                         text=[f'{v:,.1f}{suffix}' for v in data[measure]],textposition='auto',cliponaxis=False,
                         customdata=data[['country']],
                         hovertemplate='%{customdata[0]}: %{x:,.2f}'+suffix+'<extra></extra>'))
    _style(fig,height=620,legend=False)
    fig.update_layout(title=title,xaxis_title=xlabel,yaxis_title=None,
                      margin=dict(l=200, r=110, t=85, b=85))
    if midpoint is not None: fig.add_vline(x=midpoint,line_color='#707A88',line_width=1)
    return fig




################################################ Chapter 1 — When the World Stood Still

def plot_covid_mortality(df,countries=None):
    return _line(df,'deaths_per_million', FOCUS if countries is None else countries,
                 'Pandemic waves: reported monthly COVID-19 mortality',
                 'Reported deaths per million (monthly)',start='2020-01-01')


def plot_mortality_comparison(df,start_date='2020-01-01',end_date='2023-07-01'):
    data=_date(df)[['country','date','deaths_per_million']]
    data=data[data.date.between(start_date,end_date)]
    expected=len(pd.date_range(start_date,end_date,freq='MS'))
    valid=data.dropna(subset=['deaths_per_million']).groupby('country')['date'].nunique()
    data=data[data.country.isin(valid[valid.eq(expected)].index)]
    data=data.groupby('country',as_index=False)['deaths_per_million'].sum(min_count=1)
    return _rank(data,'deaths_per_million',
                 'Reported mortality across countries (Jan 2020–Jul 2023)',
                 'Reported COVID-19 deaths per million',highlight=['United Kingdom','United States','China'])


def plot_government_stringency(df,countries=None):
    fig=_line(df,'stringency_index',FOCUS_ECON if countries is None else countries,
              'How restrictive were government responses?',
              'Stringency index (0–100)',start='2020-01-01',end='2022-12-01')
    fig.update_yaxes(range=[0,100])
    return fig


def plot_vaccination_rollout(df, countries=None):

    if countries is None:
        countries = [
            "United States",
            "Germany",
            "Japan",
            "United Kingdom",
            "China",
            "Central African Republic",
            "Guinea-Bissau",
            "Gambia",
            "Lesotho"
        ]

    data = df[
        ["country", "date", "vaccinated_per_hundred"]
    ].copy()

    data["date"] = pd.to_datetime(
        data["date"],
        dayfirst=True,
        errors="coerce"
    )

    data = data.dropna(subset=["date"])

    fig = go.Figure()

    for country in countries:

        country_data = data[
            data["country"] == country
        ].copy()

        if country_data["vaccinated_per_hundred"].notna().sum() == 0:
            continue

        # Keep the monthly timeline, including missing months
        country_data["date"] = (
            country_data["date"].dt.to_period("M").dt.to_timestamp()
        )

        monthly = (
            country_data
            .sort_values("date")
            .drop_duplicates("date", keep="last")
            .set_index("date")["vaccinated_per_hundred"]
        )

        dates = pd.date_range(
            monthly.index.min(),
            monthly.index.max(),
            freq="MS"
        )

        monthly = monthly.reindex(dates)

        fig.add_trace(
            go.Scatter(
                x=monthly.index,
                y=monthly.values,
                mode="lines+markers",
                name=country,
                connectgaps=False,
                line=dict(
                    color=COLORS.get(country, "#64748B"),
                    width=3
                ),
                marker=dict(size=6),
                hovertemplate=(
                    "%{x|%b %Y}<br>"
                    "%{y:.1f} per 100"
                    "<extra>%{fullData.name}</extra>"
                )
            )
        )

    fig.update_layout(
        title="Vaccination Campaigns Progressed at Different Speeds",
        template="plotly_white",
        height=550,
        xaxis_title="Date",
        yaxis_title="Vaccinated people per 100 (dataset indicator)",
        hovermode="closest",
        legend=dict(
            orientation="h",
            y=-0.25,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(l=80, r=50, t=90, b=110)
    )

    fig.update_yaxes(range=[0, 100])
    fig.update_xaxes(
        range=["2020-12-01", "2023-12-31"],
        dtick="M6",
        tickformat="%b %Y"
    )

    return fig







####################################### Chapter 2 — An Economy Brought to a Halt

def plot_gdp_growth(df, countries=None):

    if countries is None:
        countries = [
            "United Kingdom",
            "United States",
            "China",
            "Germany",
            "Lesotho",
            "Gambia"
        ]

    # Annual data: one observation per country and year
    data = _annual(df, "wb_gdp_growth")

    data = data[
        data["country"].isin(countries)
        & data["year"].between(2015, 2024)
    ]

    countries = [
        c for c in countries
        if c in data["country"].values
    ]

    if not countries:
        return go.Figure()

    ncols = 2
    nrows = (len(countries) + 1) // 2

    fig = make_subplots(
        rows=nrows,
        cols=ncols,
        subplot_titles=countries,
        shared_yaxes=True,
        vertical_spacing=0.12,
        horizontal_spacing=0.12
    )

    for i, country in enumerate(countries):

        row = i // ncols + 1
        col = i % ncols + 1

        country_data = data[
            data["country"] == country
        ].sort_values("year")

        years = country_data["year"].tolist()

        fig.add_trace(
            go.Scatter(
                x=years,
                y=country_data["wb_gdp_growth"],
                mode="lines+markers",
                line=dict(
                    color=COLORS.get(country, "#447AC0"),
                    width=2.5
                ),
                marker=dict(
                    size=[11 if y == 2020 else 5 for y in years],
                    symbol=[
                        "diamond" if y == 2020 else "circle"
                        for y in years
                    ]
                ),
                name=country,
                showlegend=False,
                hovertemplate=(
                    "%{x}: %{y:.2f}%<extra></extra>"
                )
            ),
            row=row,
            col=col
        )

        # Highlight pandemic year
        fig.add_vrect(
            x0=2019.5,
            x1=2020.5,
            fillcolor="#CBD5E1",
            opacity=0.25,
            line_width=0,
            row=row,
            col=col
        )

        # Zero growth reference
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="#A0A0A0",
            row=row,
            col=col
        )

    fig.update_layout(
        title="Before, During and After COVID-19: GDP Growth",
        template="plotly_white",
        height=300 * nrows + 100,
        margin=dict(l=70, r=40, t=110, b=60),
        showlegend=False
    )

    fig.update_xaxes(
        tickvals=[2015, 2018, 2020, 2022, 2024]
    )

        # Same Y-axis scale for every country
    y_min = min(-1, data["wb_gdp_growth"].min() - 1)
    y_max = max(1, data["wb_gdp_growth"].max() + 1)

    fig.update_yaxes(
        range=[y_min, y_max]
    )

    fig.update_yaxes(
        title_text="GDP growth (%)",
        col=1
    )

    return fig


def plot_gdp_shock_2020(df):
    data=_country(df,'gdp_shock_2020')
    return _rank(data,'gdp_shock_2020',
                 'The 2020 economic shock differed sharply between countries',
                 'GDP growth deviation from reference (percentage points)',midpoint=0,
                 suffix=' pp',highlight=['United Kingdom','Lesotho','China','East Timor'])


def plot_inflation(df, year_before=2019, year_after=2022):
    """
    Compare inflation rates between two years
    across all available countries.
    """

    data = df[
        ["country", "year", "wb_inflation"]
    ].copy()

    data["year"] = pd.to_numeric(
        data["year"]
    ).astype("Int64")

    # Keep one annual value per country
    data = data.drop_duplicates(
        subset=["country", "year"]
    )

    # Create comparison table
    comparison = data.pivot(
        index="country",
        columns="year",
        values="wb_inflation"
    )

    comparison = comparison.dropna(
        subset=[year_before, year_after]
    ).copy()

    # Calculate change in percentage points
    comparison["change"] = (
        comparison[year_after] - comparison[year_before]
    )

    comparison = comparison.sort_values(
        "change", ascending=False
    )

    fig = go.Figure()

    # Connecting lines
    for country, row in comparison.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row[year_before], row[year_after]],
                y=[country, country],
                mode="lines",
                line=dict(color="#CBD5E1", width=3),
                showlegend=False,
                hoverinfo="skip"
            )
        )

    # Before-pandemic markers
    fig.add_trace(
        go.Scatter(
            x=comparison[year_before],
            y=comparison.index,
            mode="markers",
            name=str(year_before),
            marker=dict(color="#94A3B8", size=11),
            hovertemplate="%{y}: %{x:.2f}%<extra>2019</extra>"
        )
    )

    # Post-pandemic markers
    fig.add_trace(
        go.Scatter(
            x=comparison[year_after],
            y=comparison.index,
            mode="markers",
            name=str(year_after),
            marker=dict(color="#E66A4E", size=12),
            hovertemplate="%{y}: %{x:.2f}%<extra>2022</extra>"
        )
    )

    fig.update_layout(
        title="Inflation Surged After the Pandemic, But Not Everywhere",
        template="plotly_white",
        height=650,
        xaxis_title="Annual inflation rate (%)",
        yaxis_title=None,
        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        ),
        margin=dict(l=190, r=50, t=100, b=60)
    )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=comparison.index[::-1].tolist()
    )

    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="#94A3B8"
    )

    return fig







##################################################### Chapter 3 — Livelihoods on the Line

def plot_unemployment(df,countries=None):
    return _line(df,'wb_unemployment_rate',FOCUS_ECON if countries is None else countries,
                 'Unemployment before, during and after COVID-19',
                 'Unemployment (% of labor force)',start=2018,end=2024,annual=True)


def plot_unemployment_change_2020(df):
    annual=_annual(df,'wb_unemployment_rate')
    two=annual[annual.year.isin([2019,2020])].pivot(index='country',columns='year',values='wb_unemployment_rate')
    two=two.dropna(subset=[2019,2020])
    data=(two[2020]-two[2019]).rename('delta').reset_index()
    return _rank(data,'delta',
                 "The Pandemic's Unequal Impact on Unemployment",
                 'Change in unemployment rate, 2019–2020 (percentage points)',
                 midpoint=0,suffix=' pp',highlight=['United States','Lesotho','United Kingdom'])

def plot_unemployment_vs_2019(df, countries=None):

    if countries is None:
        countries = [
            "United States",
            "United Kingdom",
            "Lesotho",
            "Gambia"
        ]

    # Select annual unemployment data
    data = df[
        ["country", "year", "wb_unemployment_rate"]
    ].copy()

    data["year"] = pd.to_numeric(
        data["year"], errors="coerce"
    )

    data = data.dropna().drop_duplicates(
        subset=["country", "year"]
    )

    data = data[data["country"].isin(countries)]

    # Reference unemployment rate in 2019
    baseline = (
        data[data["year"] == 2019]
        .set_index("country")["wb_unemployment_rate"]
    )

    data["baseline_2019"] = data["country"].map(baseline)

    # Difference relative to 2019 in percentage points
    data["change_vs_2019"] = (
        data["wb_unemployment_rate"] - data["baseline_2019"]
    )

    data = data.dropna(subset=["change_vs_2019"])

    fig = px.line(
        data.sort_values("year"),
        x="year",
        y="change_vs_2019",
        color="country",
        markers=True,
        title="Did Unemployment Return to Pre-Pandemic Levels?",
        labels={
            "year": "Year",
            "change_vs_2019": "Change vs 2019 (percentage points)",
            "country": "Country"
        },
        color_discrete_map={
            "United States": "#2A66A5",
            "United Kingdom": "#DF594B",
            "Lesotho": "#8E63B4",
            "Gambia": "#B37188"
        }
    )

    # Highlight 2020
    fig.add_vrect(
        x0=2019.5,
        x1=2020.5,
        fillcolor="#CBD5E1",
        opacity=0.25,
        line_width=0
    )

    # Pre-pandemic baseline
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray"
    )

    fig.update_layout(
        template="plotly_white",
        height=550,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            y=-0.25,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(l=90, r=50, t=80, b=100)
    )

    fig.update_xaxes(
        dtick=1,
        range=[2019, 2024]
    )

    return fig








########################################## Chapter 4 — One Pandemic, Many Realities

def plot_gdp_per_capita(df):

    # GDP per capita in 2019
    data = df[
        ["country", "year", "wb_gdp_per_capita"]
    ].copy()

    data = data[data["year"] == 2019]

    # One observation per country
    data = data.dropna().drop_duplicates("country")

    data = data[data["wb_gdp_per_capita"] > 0]

    data = data.sort_values("wb_gdp_per_capita")

    # Highlight the two extremes
    colors = [
        "#2A66A5" if c == "United States"
        else "#E66A4E" if c == "Central African Republic"
        else "#94A3B8"
        for c in data["country"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["wb_gdp_per_capita"],
            y=data["country"],
            mode="markers+text",
            marker=dict(
                color=colors,
                size=14
            ),
            text=[
                f"${v:,.0f}"
                for v in data["wb_gdp_per_capita"]
            ],
            textposition="middle right",
            hovertemplate=(
                "%{y}<br>"
                "GDP per capita: $%{x:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Countries Entered the Pandemic with Unequal Economic Resources",
        template="plotly_white",
        height=600,
        xaxis_title="GDP per capita in 2019 (current US$, logarithmic scale)",
        yaxis_title=None,
        showlegend=False,
        margin=dict(l=190, r=100, t=90, b=70)
    )

    fig.update_xaxes(
        type="log",
        range=[2.4, 5.2],
        tickvals=[500, 1000, 5000, 10000, 50000, 100000],
        ticktext=["$500", "$1k", "$5k", "$10k", "$50k", "$100k"]
    )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=data["country"].tolist()
    )

    return fig


def plot_mortality_vs_gdp_shock(df):
    data=_country(df,'cum_deaths_per_million').merge(_country(df,'gdp_shock_2020'),on='country')
    fig=go.Figure()
    for _,r in data.iterrows():
        fig.add_trace(go.Scatter(x=[r.cum_deaths_per_million],y=[r.gdp_shock_2020],
                    mode='markers+text',text=[r.country],textposition='top center',
                    marker=dict(size=13,color=COLORS.get(r.country,'#67788B')),
                    name=r.country,showlegend=False,
                    hovertemplate=f'{r.country}<br>Reported cumulative deaths / million: %{{x:,.1f}}<br>GDP shock: %{{y:,.1f}} pp<extra></extra>'))
    _style(fig,height=600,legend=False)
    fig.update_layout(title='Does reported mortality predict economic damage?',
        xaxis_title='Cumulative reported COVID deaths per million (period to verify)',
        yaxis_title='GDP growth shock in 2020 (percentage points)',
        margin=dict(l=70,r=90,t=80,b=90))
    fig.add_hline(y=0,line_color='#9EA8B5',line_dash='dash')

    return fig

def plot_wealth_vs_gdp_shock(df):

    # Select pre-pandemic economic data
    data = df[
        ["country", "year", "wb_gdp_per_capita", "gdp_shock_2020"]
    ].copy()

    data["year"] = pd.to_numeric(
        data["year"], errors="coerce"
    )

    # Keep one observation per country in 2019
    data = (
        data[data["year"] == 2019]
        .dropna()
        .drop_duplicates("country")
        .copy()
    )

    data = data[data["wb_gdp_per_capita"] > 0]

    # Highlight countries illustrating different outcomes
    highlight_colors = {
        "United States": "#2A66A5",
        "United Kingdom": "#E66A4E",
        "Lesotho": "#8E63B4",
        "East Timor": "#C28B37"
    }

    colors = [
        highlight_colors.get(country, "#A7B4C2")
        for country in data["country"]
    ]

    labels = [
        country if country in highlight_colors else ""
        for country in data["country"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["wb_gdp_per_capita"],
            y=data["gdp_shock_2020"],
            mode="markers+text",
            text=labels,
            textposition="top center",
            customdata=data["country"],
            marker=dict(
                size=15,
                color=colors,
                line=dict(color="white", width=1.5)
            ),
            hovertemplate=(
                "<b>%{customdata}</b><br>"
                "GDP per capita (2019): $%{x:,.0f}<br>"
                "GDP shock (2020): %{y:+.1f} pp"
                "<extra></extra>"
            ),
            showlegend=False
        )
    )

    # Zero shock reference
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="#64748B"
    )

    fig.update_layout(
        title="Did Pre-Pandemic Wealth Protect Countries from the Economic Shock?",
        template="plotly_white",
        height=650,
        xaxis_title="GDP per capita in 2019 (current US$, log scale)",
        yaxis_title="2020 GDP growth deviation from reference (pp)",
        margin=dict(l=90, r=70, t=120, b=80),

        # Allow users to examine the 9 negative shocks
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1,
                y=1.13,
                xanchor="right",
                buttons=[
                    dict(
                        label="All 10 countries",
                        method="relayout",
                        args=[{"yaxis.range": [-15, 32]}]
                    ),
                    dict(
                        label="Zoom: negative shocks",
                        method="relayout",
                        args=[{"yaxis.range": [-14, 1]}]
                    )
                ]
            )
        ]
    )

    fig.update_xaxes(
        type="log",
        tickvals=[500, 1000, 5000, 10000, 50000],
        ticktext=["$500", "$1k", "$5k", "$10k", "$50k"]
    )

    fig.update_yaxes(range=[-15, 32])

    return fig








#################################################### Chapter 5 — The Road Back

def plot_gdp_index(df, countries=None):

    if countries is None:
        countries = [
            "United Kingdom",
            "United States",
            "China",
            "Germany",
            "Lesotho",
            "Gambia"
        ]

    data = df[
        ["country", "year", "wb_gdp_growth"]
    ].copy()

    data["year"] = pd.to_numeric(
        data["year"], errors="coerce"
    )

    data = (
        data.dropna()
        .drop_duplicates(["country", "year"])
    )

    countries = [
        c for c in countries
        if c in data["country"].values
    ]

    if not countries:
        return go.Figure()

    ncols = 2
    nrows = (len(countries) + 1) // 2

    fig = make_subplots(
        rows=nrows,
        cols=ncols,
        subplot_titles=countries,
        vertical_spacing=0.12
    )

    colors = {
        "United Kingdom": "#E66A4E",
        "United States": "#2A66A5",
        "China": "#329989",
        "Germany": "#DC9734",
        "Lesotho": "#8E63B4",
        "Gambia": "#B37188"
    }

    all_values = []

    for i, country in enumerate(countries):

        row = i // ncols + 1
        col = i % ncols + 1

        country_data = data[
            data["country"] == country
        ].set_index("year")["wb_gdp_growth"]

        # 2019 is the reference year
        years = [2019]
        index_values = [100.0]

        index = 100.0

        # Reconstruct real GDP index
        for year in range(2020, 2025):

            if year not in country_data.index:
                break

            growth = country_data.loc[year]

            index = index * (1 + growth / 100)

            years.append(year)
            index_values.append(index)

        all_values.extend(index_values)

        fig.add_trace(
            go.Scatter(
                x=years,
                y=index_values,
                mode="lines+markers",
                line=dict(
                    color=colors.get(country, "#64748B"),
                    width=3
                ),
                marker=dict(size=7),
                showlegend=False,
                hovertemplate=(
                    "Year: %{x}<br>"
                    "Real GDP index: %{y:.1f}"
                    "<extra></extra>"
                )
            ),
            row=row,
            col=col
        )

        # Pre-pandemic GDP level
        fig.add_hline(
            y=100,
            line_dash="dash",
            line_color="#94A3B8",
            row=row,
            col=col
        )

    fig.update_layout(
        title="The Road Back: Did Economies Recover Their 2019 GDP?",
        template="plotly_white",
        height=300 * nrows + 100,
        margin=dict(l=70, r=40, t=110, b=60)
    )

    fig.update_xaxes(
        tickvals=[2019, 2020, 2022, 2024]
    )

    # Same scale across countries
    fig.update_yaxes(
        range=[
            min(95, min(all_values) - 5),
            max(105, max(all_values) + 5)
        ]
    )

    return fig


def plot_postpandemic_growth(df,countries=None):
    fig=_line(df,'wb_gdp_growth',FOCUS_ECON if countries is None else countries,
              'Growth rates returned — but was the output loss recovered?',
              'Annual real GDP growth (%)',start=2020,end=2024,annual=True)
    fig.add_hline(y=0,line_color='#8995A4')
    return fig


def plot_gdp_recovery_2024(df):

    data = df[
        ["country", "year", "wb_gdp_growth"]
    ].copy()

    data["year"] = pd.to_numeric(
        data["year"], errors="coerce"
    )

    # One observation per country and year
    annual = (
        data.dropna()
        .drop_duplicates(["country", "year"])
        .pivot(
            index="country",
            columns="year",
            values="wb_gdp_growth"
        )
    )

    # Require complete annual data from 2019 to 2024
    years = list(range(2020, 2025))

    annual = annual.dropna(
        subset=[2019] + years
    )

    # Reconstruct the 2024 real GDP index
    index_2024 = (
        100 * (1 + annual[years] / 100).prod(axis=1)
    )

    comparison = pd.DataFrame({
        "country": index_2024.index,
        "gdp_index_2024": index_2024.values
    })

    # Percentage change from 2019
    comparison["change"] = (
        comparison["gdp_index_2024"] - 100
    )

    comparison = comparison.sort_values("change")

    # Distinguish gains and losses
    colors = [
        "#E66A4E" if v < 0 else "#2A66A5"
        for v in comparison["change"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=comparison["change"],
            y=comparison["country"],
            orientation="h",
            marker_color=colors,
            text=[
                f"{v:+.1f}%"
                for v in comparison["change"]
            ],
            textposition="outside",
            customdata=comparison["gdp_index_2024"],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Change since 2019: %{x:+.1f}%<br>"
                "2024 GDP index: %{customdata:.1f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="#64748B"
    )

    fig.update_layout(
        title="By 2024 : Who Recovered, Who Fell Behind?",
        template="plotly_white",
        height=650,
        xaxis_title="Change in real GDP level vs 2019 (%)",
        yaxis_title=None,
        margin=dict(l=200, r=90, t=90, b=70),
        showlegend=False
    )

    fig.update_yaxes(categoryorder="total ascending")

    fig.update_xaxes(range=[-25, 35])

    return fig


def metric_card(value, label):
    from dash import html

    return html.Div(
        [
            html.Div(str(value), className="metric-value"),
            html.Div(label, className="metric-label"),
        ],
        className="metric-card",
    )



