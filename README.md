# PandemiScope · The Economics of COVID-19

A multi-page Plotly Dash project for exploring the economic impact of COVID-19. The current application combines existing illustrative dashboard pages with minimal scaffolds for the planned ten-page architecture.

## Run locally

Recommended: Python 3.12.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and run:

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:8050`.

## Page architecture

| Page | File | Responsibility |
|---|---|---|
| Overview | `pages/overview.py` | Introduce the project and summarize the story |
| Country Explorer | `pages/country_explorer.py` | Explore and compare countries |
| Economic Impact | `pages/economic_impact.py` | GDP and broader economic indicators |
| Employment & Inequality | `pages/employment.py` | Labor-market effects and group differences |
| Sector Impact | `pages/sector_impact.py` | Compare the shock across industries |
| Trade & Tourism | `pages/trade_tourism.py` | International trade and tourism disruption |
| Pandemic & Economy | `pages/pandemic_analysis.py` | Explore pandemic timing and economic indicators |
| Government Response | `pages/government_response.py` | Economic support measures and policy context |
| Recovery | `pages/recovery.py` | Compare recovery paths and remaining gaps |
| Data & Methodology | `pages/data_methodology.py` | Document sources, definitions and limitations |

Navigation is grouped into Discover, Economic Impact, Analysis & Recovery, and About the Data. The shared country and date controls in `app.py` currently save their selections to `dcc.Store(id="global-filters")`. Relevant charts will be connected to this shared state as each page is developed.

## Code organization

- `app.py`: application setup, routes, grouped navigation and shared filters.
- `pages/`: page layouts; each page exposes a `layout()` function.
- `src/visualizations.py`: existing Plotly chart factories and mock data.
- `src/callbacks.py`: existing chart interactions and callbacks.
- `src/data_processing.py`: future data-loading and cleaning functions.
- `src/analysis.py`: future analysis functions.
- `assets/style.css`: shared visual styling.
- `data/raw/` and `data/processed/`: intended locations for raw and processed data.
- `notebooks/exploratory_analysis.ipynb`: exploratory analysis scaffold.

## Current status and data disclaimer

The new pages are intentionally structural placeholders. Their TODO comments describe future content; they do not yet contain complete charts or analyses. Existing chart and KPI values in the original pages are illustrative placeholders, not verified findings. Replace them with sourced observations and show definitions, units and limitations before presenting conclusions.
