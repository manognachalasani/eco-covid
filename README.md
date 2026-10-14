# COVID-19 Economic Impact — Data Visualization Dashboard

## 1. Project Overview

This project explores the economic impact of the COVID-19 pandemic across countries using data analysis and interactive visualization.

The goal is to build a **multi-page dashboard with Python and Plotly Dash** that helps users explore economic trends, compare countries, and understand how pandemic-related indicators and economic outcomes changed over time.

The project requirements in the brief include:

- Collecting and preprocessing relevant COVID-19 and economic datasets.
- Performing exploratory data analysis (EDA).
- Critically assessing data sufficiency, quality, bias, and context.
- Developing a multi-page Plotly Dash dashboard with clear labels, annotations, and interactive visualizations.
- Communicating findings accurately and transparently.
- Optionally deploying the dashboard.
- **Optional bonus:** Creating a MySQL relational database for the datasets and documenting its schema.

**Final dashboard and oral presentation:** October 21  
**Presentation duration:** 20 minutes per group

## 2. Team Roles and Deliverables

Each team member owns a technical work package. Coordinate interfaces and shared files before implementation so the components integrate cleanly.

### Person 1 — Data Pipeline and Preprocessing

**Responsibility:** Collect, clean, standardize, and prepare the datasets for analysis.

Tasks:
- Obtain and organize the raw datasets.
- Clean missing values and duplicates.
- Standardize country names, dates, column names, and data types.
- Merge datasets using agreed keys, such as country and date/year.
- Export analysis-ready data to `data/processed/`.
- Document sources, transformations, assumptions, and known data limitations.

Deliverables:
- `src/data_processing.py`
- `data/raw/` — original downloaded datasets (do not manually edit originals)
- `data/processed/` — cleaned, analysis-ready datasets
- Reproducible preprocessing script and brief data dictionary

**Definition of done:** A teammate can run the preprocessing script using the documented setup and obtain the expected processed datasets.

### Person 2 — Statistical Analysis and Reusable Visualizations

**Responsibility:** Implement the calculations and reusable chart functions used by the dashboard.

Tasks:
- Calculate descriptive statistics and economic trends.
- Analyze relevant relationships and correlations.
- Create reusable Plotly figures for time series, country comparisons, and relationships between indicators.
- Ensure axes, units, titles, legends, and hover information are clear.
- Work with Person 1 to confirm which indicators are available and comparable.
- Avoid presenting correlation as proof of causation; document relevant limitations.

Deliverables:
- `src/analysis.py`
- `src/visualizations.py`
- `notebooks/exploratory_analysis.ipynb`

**Definition of done:** Analysis and chart functions run on the processed data and return valid, clearly labeled figures.

### Person 3 — Main Dash Application and Interactivity

**Responsibility:** Set up the main application and implement its shared structure and overview page.

Tasks:
- Create and configure the Dash app entry point.
- Implement multi-page routing and navigation.
- Build the global overview page and its KPI cards.
- Connect the processed datasets and reusable visualization functions.
- Implement shared filters, such as country and year, where appropriate.
- Create or coordinate callbacks so filters update the relevant charts.
- Ensure the application starts using the documented command.

Deliverables:
- `app.py`
- `pages/overview.py`
- `src/callbacks.py` (or another agreed callback-module location)

**Definition of done:** The app launches, page navigation works, and the overview page and its agreed filters function correctly.

### Person 4 — Additional Pages, Styling, and Integration

**Responsibility:** Implement the remaining dashboard pages and establish a consistent, polished interface.

Tasks:
- Build the additional pages using the agreed chart functions and data interfaces.
- Apply a consistent layout, typography, spacing, and color palette.
- Add explanatory text, annotations, source notes, and contextual labels.
- Make layouts usable at different screen sizes.
- Test page rendering, navigation, filters, and integration with the main app.
- Coordinate final integration and identify defects before delivery.

Deliverables:
- `pages/economic_impact.py`
- `pages/pandemic_analysis.py`
- `pages/recovery.py`
- `assets/style.css`

**Definition of done:** All assigned pages render in the integrated app, follow the shared design, and pass basic functional checks.

### Shared Responsibilities

All four team members must:
- Review the accuracy and clarity of charts.
- Test the integrated application, not only their own files.
- Document sources and important assumptions.
- Review and merge code changes through Git.
- Contribute to the final presentation and explain their technical contribution.

The MySQL database and deployment are optional extensions. Complete the core dashboard first. If the team chooses the MySQL bonus, Person 1 can extend the data pipeline with schema and loading scripts, with the database design reviewed by the team.

## 3. Proposed Project Structure

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

This is the proposed structure. The team can adjust filenames as needed, but changes to shared interfaces should be communicated before merging.

### Folder and File Responsibilities

| Path | Purpose | Owner |
|---|---|---|
| `app.py` | Dash application entry point and page registration | Person 3 |
| `pages/overview.py` | Global overview and KPI cards | Person 3 |
| `pages/economic_impact.py` | Economic indicators and trends | Person 4 |
| `pages/pandemic_analysis.py` | Pandemic/economic comparisons | Person 4 |
| `pages/recovery.py` | Recovery trends and conclusions | Person 4 |
| `src/data_processing.py` | Data loading, cleaning, and merging | Person 1 |
| `src/analysis.py` | Statistical calculations and analysis functions | Person 2 |
| `src/visualizations.py` | Reusable Plotly figure functions | Person 2 |
| `src/callbacks.py` | Shared Dash callbacks, if used | Person 3, coordinated with Person 4 |
| `data/raw/` | Original source datasets | Person 1 |
| `data/processed/` | Cleaned datasets used by analysis and dashboard | Person 1 |
| `notebooks/` | Exploratory analysis and development experiments | Person 2 |
| `assets/style.css` | Shared styles | Person 4 |
| `requirements.txt` | Python dependencies | All; one person coordinates updates |

## 4. Proposed Dashboard Pages

The final page scope should be confirmed after the team checks data availability.

1. **Global Overview:** Key indicators, country comparisons, and a timeline of pandemic and economic trends.
2. **Economic Impact:** GDP growth, unemployment, inflation, or other economic indicators available in the selected datasets.
3. **Pandemic and Economy:** Explore relationships between pandemic indicators and economic outcomes. Use careful language: observed associations do not establish causation.
4. **Recovery and Conclusions:** Compare recovery patterns, summarize supported findings, and explain data limitations.

Every page should include:
- A clear title and the question the page helps answer.
- Appropriate charts with labeled axes and units.
- Useful legends, hover details, and annotations where appropriate.
- Data source and time-period information.
- Clear explanations of limitations where they affect interpretation.

## 5. Data and Technical Conventions

### Data sources

The project brief suggests the following sources; these are starting points, not a mandatory exhaustive list:

- Mendeley — COVID-19 datasets
- Our World in Data — Coronavirus
- Eurostat — COVID-19
- INSEE — COVID-19 data

The team may use other relevant sources. Record the dataset name, source URL, retrieval date, coverage, units, and any known limitations in the README or a dedicated data-source document.

### Shared data contract

Before implementation, agree on:
- Country identifier and country-name conventions.
- Date or year format and analysis time range.
- Names and units of the selected indicators.
- Missing-value conventions.
- Processed dataset filenames and column names.

Do not assume every source has the same geographic coverage, time frequency, definitions, or units. Validate these before merging.

### Python environment

The brief recommends an Anaconda project and Python 3.12.

Suggested setup (adapt to the team's environment):

```bash
conda create -n covid-dashboard python=3.12
conda activate covid-dashboard
pip install -r requirements.txt
```

Keep dependencies in `requirements.txt`. Update it when adding or changing packages.

### Running the application

Once the application entry point is implemented and dependencies are installed:

```bash
python app.py
```

Use the local URL printed by Dash in the terminal to open the dashboard.

## 6. Git Collaboration Workflow

1. Clone the shared repository.
2. Create a branch for each feature or work package, for example:
   - `feature/data-pipeline`
   - `feature/analysis-charts`
   - `feature/dash-overview`
   - `feature/dashboard-pages`
3. Commit focused changes with descriptive messages.
4. Push the branch and open a pull request.
5. Review changes and resolve conflicts before merging.
6. Pull the latest shared branch before starting new work.

Example commands:

```bash
git clone <repository-url>
cd covid-economic-impact
git checkout -b feature/data-pipeline

git add src/data_processing.py
git commit -m "Add data preprocessing pipeline"
git push -u origin feature/data-pipeline
```

Replace `<repository-url>` with the actual Git repository URL. Avoid having multiple people edit shared files such as `app.py` or `requirements.txt` simultaneously without coordinating.

### Data and secrets in Git

- Do not commit passwords, API keys, credentials, or private data.
- Do not commit large raw datasets unless the team has agreed that their size and licensing permit it.
- If datasets are too large for Git, document how teammates can download them.
- Add virtual environments, cache files, and local secrets to `.gitignore`.
- Preserve dataset attribution and comply with source licensing and terms.

## 7. Integration Contracts

To reduce merge conflicts and integration delays, agree on the following before coding:

- Person 1 publishes a small sample and the final processed column names early.
- Person 2 documents each chart function's expected input columns and return value.
- Person 3 defines the page-routing and app structure before Person 4 builds the additional pages.
- Person 3 and Person 4 agree on how shared filters and callbacks will communicate with pages.
- Everyone uses the same environment and dependency list.
- Shared function names, filenames, and data schemas should not be changed silently.

## 8. Suggested Milestones

The project brief sets the final dashboard and oral presentation for **October 21**. The following are suggested internal targets:

| Target | Milestone |
|---|---|
| October 12 | Agree on research questions, datasets, indicators, folder structure, and interfaces |
| October 13–14 | Data pipeline produces an initial cleaned dataset |
| October 14–16 | Analysis and reusable charts are ready |
| October 16–18 | Dashboard pages and interactions are implemented |
| October 19–20 | Integration testing, fixes, source notes, and presentation preparation |
| October 21 | Final dashboard and oral presentation |

Adjust these milestones together if data access or implementation takes longer than expected. Prioritize a working, validated dashboard over optional features.

## 9. Testing Checklist

Before delivery, confirm:

- [ ] The documented environment can be installed.
- [ ] The data-processing script runs and produces the expected files.
- [ ] The analysis functions run against the processed datasets.
- [ ] Every dashboard page loads without errors.
- [ ] Navigation and shared filters work as intended.
- [ ] Charts show correct units, labels, date ranges, and country selections.
- [ ] Missing data and incomparable indicators are handled transparently.
- [ ] Data sources and important limitations are documented.
- [ ] The dashboard layout is readable and consistent.
- [ ] A teammate can clone the repository and follow the README to run the app.
- [ ] The final presentation is prepared by the team.

## 10. Optional Extensions

### MySQL relational database — bonus challenge

If time permits, create a MySQL database for the datasets. Document:
- The purpose of each table.
- Attributes and data types.
- Primary and foreign keys.
- Relationships between tables.
- The reasons for the chosen schema.

Keep this separate from the minimum viable dashboard until the core application is stable.

### Deployment

Deployment is optional but recommended by the brief if a web server is available. First confirm the dashboard works locally, then document deployment configuration and any environment variables without committing secrets.

---

## Definition of project completion

The project is ready for delivery when the team can run the multi-page Plotly Dash application from the repository, explore the selected COVID-19 and economic indicators interactively, and interpret the visualizations with sufficient context about data sources, limitations, and uncertainty.