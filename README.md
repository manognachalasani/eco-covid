# Pandemiscope — The Cosmic Archive

**Pandemiscope** is an interactive data storytelling project exploring the COVID-19 pandemic, its public-health and economic consequences, government responses, and the recovery across selected countries.

Built with Python, Dash and Plotly, the project presents data through interactive visualizations and a chapter-based narrative.

## Project Structure

```text
cdl-project/
├── assets/                  # CSS, JavaScript and media assets
├── data/
│   ├── raw/                 # Original data and data documentation
│   └── processed/           # Processed dataset used by the dashboard
├── notebooks/               # Data exploration and analysis
├── pages/                   # Interactive dashboard chapters
├── src/                     # Data processing, analysis and visualizations
├── app.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md
```

## Dashboard Chapters

The dashboard explores the pandemic through the following sections:

- **Overview** — Introduction to the project and the pandemic.
- **Pandemic Response** — Public-health developments and pandemic response.
- **Economic Impact** — Changes in economic performance during the pandemic.
- **Employment** — Employment-related impacts and trends.
- **Country Explorer** — Country-level comparisons and indicators.
- **Recovery** — Economic developments following the initial shock.
- **Data Methodology** — Data sources, preparation and methodological considerations.

## Data

The dashboard uses the processed dataset:

`data/processed/final_dataset.csv`

The `data/raw/README.md` file documents the raw data and its sources.

The `data/raw/` and `data/processed/` directories contain `.gitkeep` files to preserve their structure in Git. These files do not contain datasets.

If the processed dataset is not available after cloning the repository, ensure that `final_dataset.csv` is placed in `data/processed/` before starting the application.

## Notebooks

The `notebooks/` directory contains two Jupyter notebooks:

- `covid_economy_final.ipynb` — Notebook for the project's COVID-19 economic analysis.
- `exploratory_analysis.ipynb` — Exploratory data analysis.

## Getting Started

### Prerequisites

- Python 3
- pip

### 1. Clone the repository

```bash
git clone <repository-url>
cd cdl-project
```

Replace `<repository-url>` with the repository's Git URL.

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Check the dataset

Make sure the following file exists:

```text
data/processed/final_dataset.csv
```

If it is missing, consult `data/raw/README.md` for information about the source data and preparation process.

### 5. Run the dashboard

From the project root, execute:

```bash
python app.py
```

Open the local address displayed in the terminal. The default Dash address is usually:

`http://127.0.0.1:8050/`

To stop the server, press `Ctrl+C` in the terminal.

## Technology Stack

- **Python** — Data processing and application logic
- **Dash** — Interactive web dashboard
- **Plotly** — Data visualization
- **Pandas** — Data manipulation and analysis
- **CSS and JavaScript** — Styling, transitions and interactive presentation

## Analytical Scope and Limitations

The project compares public-health and economic indicators across selected countries and over time. Its analysis aims to identify patterns in pandemic-related disruption and subsequent recovery.

Observed changes should be interpreted in their socioeconomic and geopolitical contexts. Associations between pandemic measures and economic outcomes do not, on their own, establish causation. Data availability, missing observations and differences between countries may also affect comparisons.

