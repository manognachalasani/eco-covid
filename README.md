# PandemiScope · The Economics of COVID-19

A multi-page Plotly Dash mock dashboard for the CentraleDigitalLab Data Storytelling project.

## Project structure

```text
covid-economic-impact/
├── app.py
├── pages/
│   ├── overview.py
│   ├── economic_impact.py
│   ├── pandemic_analysis.py
│   └── recovery.py
├── src/
│   ├── data_processing.py
│   ├── analysis.py
│   ├── visualizations.py
│   └── callbacks.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── exploratory_analysis.ipynb
├── assets/
│   └── style.css
├── requirements.txt
├── .gitignore
└── README.md
```

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

Open the local URL shown in the terminal, usually `http://127.0.0.1:8050`.

## Pages and responsibilities

- **Overview:** project landing page, headline placeholder metrics and navigation.
- **Economic impact:** GDP line chart, year snapshot slider and sector filter.
- **Pandemic analysis:** unemployment comparison, trade index and fiscal support.
- **Recovery:** recovery index, sector recovery comparison and takeaway preview.
- **`src/visualizations.py`:** chart factories and clearly marked mock arrays.
- **`src/callbacks.py`:** callbacks that update charts and preview text.
- **`src/data_processing.py`:** future data-loading and cleaning entry points.
- **`src/analysis.py`:** intentional scaffold for future analysis.
- **`assets/style.css`:** shared styling for all pages.
- **`notebooks/exploratory_analysis.ipynb`:** exploratory analysis scaffold.

## Important data disclaimer

**All numeric values currently used by charts and metric cards are illustrative placeholders. They are not validated observations and must not be presented as findings.** Once you select the datasets, replace the mock arrays in `src/visualizations.py` with data-driven chart functions, and update labels, units, sources and limitations.

## Suggested data workflow (future work)

1. Keep downloaded originals in `data/raw/`.
2. Document source URLs, retrieval dates, definitions, units and coverage.
3. Clean and harmonize into `data/processed/`.
4. Implement checks in `src/data_processing.py`.
5. Implement descriptive statistics and analysis in `src/analysis.py`.
6. Update chart factories in `src/visualizations.py` to consume processed data.
7. Keep UI callbacks in `src/callbacks.py` rather than embedding them in page modules.
8. Cite data sources on the relevant page and explain limitations.

## Architecture note

This structure separates **page layouts**, **visualization factories**, **callbacks**, and the future **data/analysis pipeline**. It is a practical fit for a student Dash project. If the app grows substantially, consider adding `src/config.py`, `src/data_repository.py`, tests and a database layer.
