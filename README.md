# CogniStream — Developer Activity Analytics

<p align="center">
  <strong>Understanding Developer Activity, Team Workflows, and IDE Session Quality Through Data Analytics</strong>
</p>

<p align="center">
  Python • SQL • DuckDB • Pandas • Data Visualization • Power BI
</p>

---

## 📌 Project Overview

**CogniStream** is a developer activity analytics project designed to transform raw developer event data into structured datasets, analytical insights, and interactive Power BI dashboards.

The project uses Python for data processing, DuckDB for analytical data storage, SQL for querying and aggregation, and Power BI for reporting and visualization.

It explores developer activity patterns, team-level activity distribution, IDE session characteristics, and developer-level metrics.

The objective is to demonstrate an end-to-end data analytics workflow, from data ingestion and transformation to analytical reporting.

## 🎯 Project Objectives

* Process raw developer activity datasets using Python.
* Store and analyze structured data using DuckDB.
* Perform analytical queries using SQL.
* Measure developer and team activity patterns.
* Analyze IDE sessions and identify session-quality issues.
* Export analytical datasets for Power BI.
* Build dashboards that communicate key metrics and findings.
* Demonstrate practical data analytics and business intelligence skills.

## 🏗️ Project Architecture

```text
Raw Developer Activity Data
            |
            v
   Python Data Processing
      Pandas / NumPy
            |
            v
      DuckDB Database
            |
            v
       SQL Analytics
            |
            v
    Analytical Datasets
            |
            v
      Power BI Exports
            |
            v
     Power BI Dashboard
            |
            v
   Insights and Reporting
```

The project separates data processing, analytical storage, SQL analysis, and visualization into distinct stages.

## 🛠️ Technology Stack

| Technology       | Purpose                                          |
| ---------------- | ------------------------------------------------ |
| Python           | Data processing and workflow automation          |
| Pandas           | Data manipulation and transformation             |
| NumPy            | Numerical operations                             |
| DuckDB           | Analytical database and SQL execution            |
| SQL              | Aggregation, analysis, and analytical views      |
| Matplotlib       | Data visualization                               |
| Seaborn          | Exploratory data visualization                   |
| Jupyter Notebook | Exploratory analysis and experimentation         |
| Power BI         | Interactive dashboards and business intelligence |
| Git              | Version control                                  |
| GitHub           | Source code hosting and project collaboration    |

## 📊 Dataset Overview

CogniStream uses synthetic developer activity data to simulate activity across a software development organization.

The available data represents activity during September 2026.

### Dataset Summary

| Metric                              |                Value |
| ----------------------------------- | -------------------: |
| Total developer events              |               21,128 |
| Developers                          |                   20 |
| Teams                               |                    4 |
| IDE sessions                        |                1,226 |
| IDE events associated with sessions |               16,249 |
| Analysis period                     | September 1–30, 2026 |

### Teams

The dataset represents four teams:

* Backend
* Frontend
* Data
* DevOps

Each team contains five developers in the current dataset.

### Event Types

The recorded event types include:

| Event Type         | Event Count |
| ------------------ | ----------: |
| IDE_ACTIVE         |      16,249 |
| GITHUB_COMMIT      |       1,948 |
| SLACK_NOTIFICATION |       1,407 |
| TASK_SWITCH        |         775 |
| MEETING            |         749 |
| **Total**          |  **21,128** |

These figures describe the available synthetic dataset and should be treated as analytical inputs, not real-world measurements of employee performance.

## 🗄️ Database and Data Processing

DuckDB serves as the project's analytical database.

The local database is named:

```text
cognistream.duckdb
```

It is used to store structured event data and support SQL-based analysis.

### Main Database Tables

The project contains the following tables:

| Table                      | Purpose                                       |
| -------------------------- | --------------------------------------------- |
| `events`                   | Developer activity event records              |
| `ide_events_with_sessions` | IDE activity records associated with sessions |
| `ide_sessions`             | Aggregated IDE session records                |
| `developer_metrics`        | Developer-level analytical metrics            |
| `team_metrics`             | Team-level analytical metrics                 |

The database is populated through the project's Python loading workflow.

### Data Processing Workflow

The implemented workflow includes:

1. Reading the available source datasets.
2. Loading and processing data using Python.
3. Storing data in DuckDB.
4. Running SQL queries and analytical views.
5. Performing session-quality checks.
6. Exporting datasets for Power BI.

Relevant scripts include:

```text
src/
└── database/
    ├── load_data.py
    ├── run_analysis.py
    ├── export_powerbi.py
    └── export_developer_analytics.py

sql/
├── cognistream_analysis.sql
├── cognistream_views.sql
└── session_quality_checks.sql
```

These scripts and SQL files form the main data processing and analytical workflow.

## 🔍 Analytical Areas

### 1. Developer Activity Analysis

Examines the distribution of recorded activity events and provides a basis for understanding activity patterns.

Potential analytical dimensions include:

* Event frequency
* Activity type distribution
* Activity over time
* Developer-level metrics

### 2. Team Activity Analysis

Compares recorded activity across Backend, Frontend, Data, and DevOps.

The analysis can help answer questions such as:

* How many events were recorded for each team?
* Which event types occur most frequently?
* How does task-switch activity differ between teams?
* How does recorded activity vary over time?

Activity volume alone does not establish which team is more productive.

### 3. IDE Session Quality Analysis

Examines IDE sessions and identifies records that require additional attention.

The current session-quality results are:

| Quality Category           |  Sessions |
| -------------------------- | --------: |
| OK                         |     1,216 |
| ZERO_DURATION_SINGLE_EVENT |        10 |
| **Total**                  | **1,226** |

The resulting session quality rate is approximately **99.18%**.

The `ZERO_DURATION_SINGLE_EVENT` category identifies sessions that need to be distinguished from ordinary sessions during analysis.

### 4. Developer Analytics

Provides developer-level analytical metrics derived from the available activity and session data.

This supports exploration of differences in recorded activity across developers.

Individual metrics should be interpreted in context. Event counts and recorded IDE activity are not direct measures of code quality, contribution value, or employee performance.

### 5. Executive Insights

Combines selected metrics and visualizations into a high-level reporting page.

Its purpose is to communicate the main patterns found in the dataset without requiring the viewer to inspect every underlying table.

## 📈 Power BI Dashboard

The Power BI report is located at:

```text
powerbi/CogniStream_Analytics.pbix
```

### Dashboard Pages

#### 01 — Overview

Provides a high-level summary of the dataset.

Key metrics include:

* Total events
* Total developers
* Total teams
* Total IDE sessions

It also presents activity distribution and team-level comparisons.

#### 02 — Team Activity

Focuses on team-level activity patterns.

It supports comparisons between teams and helps identify differences in event distribution and recorded task-switch activity.

#### 03 — Session Quality

Presents session counts and session-quality checks.

The page helps distinguish sessions classified as `OK` from sessions flagged by the implemented validation rules.

#### 04 — Developer Analytics

Provides a developer-level view of the available analytical metrics.

It supports exploration of activity differences across the 20 developers in the dataset.

#### 05 — Executive Insights

Summarizes selected metrics and analytical findings for a high-level audience.

The objective is to make the results easier to interpret and communicate.

## 📂 Project Structure

```text
CogniStream/
│
├── data/
│   ├── raw/
│   └── powerbi/
│
├── notebooks/
│
├── powerbi/
│   └── CogniStream_Analytics.pbix
│
├── src/
│   └── database/
│       ├── load_data.py
│       ├── run_analysis.py
│       ├── export_powerbi.py
│       └── export_developer_analytics.py
│
├── sql/
│   ├── cognistream_analysis.sql
│   ├── cognistream_views.sql
│   └── session_quality_checks.sql
│
├── README.md
└── .gitignore
```

*This is a representative structure of the main project components. Additional files may exist in the repository.*

## ⚙️ Setup and Execution

### Prerequisites

Install the following:

* Python 3.11 or a compatible Python version supported by the project's dependencies
* Git
* Power BI Desktop for opening and refreshing the report

The project has also been developed in a Python 3.13 environment.

### 1. Clone the Repository

```bash
git clone https://github.com/PritwishSaha/CogniStream.git
cd CogniStream
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If a `requirements.txt` file is present in the repository:

```powershell
pip install -r requirements.txt
```

If it is not present, install the project's required dependencies according to the imports used in its Python scripts.

### 4. Load the Data

Run the data loader from the project root:

```powershell
python src/database/load_data.py
```

This step requires the expected source datasets to be available at the paths configured in the script.

### 5. Run the Analysis

```powershell
python src/database/run_analysis.py
```

Review the script output to verify that the analytical workflow completes successfully.

### 6. Export Power BI Datasets

Run the general export script:

```powershell
python src/database/export_powerbi.py
```

Run the developer analytics export:

```powershell
python src/database/export_developer_analytics.py
```

These commands assume that the DuckDB database has been created and contains the required tables.

### 7. Open the Power BI Report

Open:

```text
powerbi/CogniStream_Analytics.pbix
```

in Power BI Desktop.

If Power BI prompts for data source locations, configure them to match the CSV exports and paths used by the report.

Refresh the report after confirming the source paths.

*The setup commands document the intended execution order. A clean-environment installation and complete end-to-end run should be verified before treating the setup as fully reproducible.*

## 📁 Power BI Export Files

The project has generated the following analytical exports:

| File                      | Purpose                           |
| ------------------------- | --------------------------------- |
| `event_overview.csv`      | Event-level reporting data        |
| `team_activity.csv`       | Team activity summary             |
| `session_quality.csv`     | Session-quality reporting data    |
| `developer_analytics.csv` | Developer-level reporting metrics |

The exports are stored in:

```text
data/powerbi/
```

The exact export columns depend on the corresponding Python and SQL implementations.

## 💡 Key Findings

Based on the current dataset and analytical results:

* The dataset contains 21,128 recorded developer events across four teams.
* IDE activity is the largest event category, with 16,249 records.
* The dataset contains 20 developers and 1,226 IDE sessions.
* The current session-quality classification identifies 1,216 sessions as `OK` and 10 as `ZERO_DURATION_SINGLE_EVENT`.
* The five-page Power BI report provides overview, team, session, developer, and executive-level views.

These findings describe the current dataset. They should not be interpreted as evidence of actual organizational productivity or employee performance.

## 🚧 Remaining Work

The following tasks are part of the final project review:

* [ ] Confirm that local Git commits are synchronized with GitHub.
* [ ] Run the complete pipeline from data loading to Power BI export.
* [ ] Verify that expected record counts remain consistent after reloading.
* [ ] Confirm that all Power BI data sources refresh successfully.
* [ ] Add screenshots of all five dashboard pages.
* [ ] Verify setup instructions in a clean environment.
* [ ] Record a short project demonstration.
* [ ] Complete the final documentation review.

## 🔮 Future Improvements

Possible extensions include:

* Automated data quality reports.
* Additional time-based activity analysis.
* More detailed developer and team comparisons.
* Scheduled data refresh workflows.
* Automated report generation.
* Expanded analytical views and documented business questions.

These are potential improvements, not features claimed to be implemented in the current version.

## ⚠️ Limitations

* The project uses synthetic developer activity data.
* Activity frequency does not directly measure productivity.
* Session-quality classifications depend on the implemented validation rules.
* The analysis does not establish causation between activity patterns and software development outcomes.
* Findings are limited to the available data and selected analytical metrics.

## 👨‍💻 Author

**Pritwish Saha**

B.Tech — Computer Science and Engineering (Artificial Intelligence and Machine Learning)

* GitHub: [PritwishSaha](https://github.com/PritwishSaha)
* LinkedIn: [Pritwish Saha](https://www.linkedin.com/in/pritwish-saha-b49604362/)

## 📄 License

Add a license to the repository if you intend to distribute the project under specific reuse permissions.

---

<p align="center">
  <strong>CogniStream — From Developer Activity Data to Analytical Insights</strong>
</p>
