#  CogniStream

## ---------------------------

### Developer Productivity & Workflow Analytics Platform

**CogniStream** is a data analytics project designed to analyze developer activity, coding sessions, workflow patterns, and team-level productivity using structured event data.

The project transforms developer activity events into analytical datasets using Python, SQL, and DuckDB. The resulting data can be used to understand coding activity, session duration, task switching, interruptions, and differences in activity across development teams.

The current implementation focuses on data processing, database development, SQL analytics, data validation, and preparing datasets for Power BI visualization.

---

## 🎯 Project Objectives

* Analyze developer activity and workflow patterns.
* Understand coding session duration and IDE activity.
* Examine task switching and potential workflow interruptions.
* Compare activity across developers and teams.
* Build a structured analytical database using DuckDB.
* Use SQL queries and analytical views to extract insights.
* Prepare clean, structured datasets for Power BI dashboards.

---

## 🛠️ Technology Stack

| Technology       | Purpose                                       |
| ---------------- | --------------------------------------------- |
| Python           | Data processing and database automation       |
| Pandas           | Data manipulation and analysis                |
| NumPy            | Numerical operations                          |
| DuckDB           | Analytical database                           |
| SQL              | Data exploration, aggregation, and validation |
| Matplotlib       | Data visualization                            |
| Seaborn          | Statistical visualization                     |
| Jupyter Notebook | Interactive analysis                          |
| Power BI         | Planned interactive dashboard development     |
| Git & GitHub     | Version control and project hosting           |

---

## 📊 Current Project Status

The project has progressed through data preparation, database development, SQL analysis, validation, and analytical data export.

| Component                                     | Current Status               |
| --------------------------------------------- | ---------------------------- |
| Project repository                            | Completed                    |
| Python environment setup                      | Completed                    |
| Data processing scripts                       | Implemented                  |
| DuckDB database                               | Created                      |
| Database tables                               | Created and populated        |
| SQL analytical queries                        | Implemented                  |
| Data validation                               | Completed for current checks |
| Analytical views                              | Created                      |
| CSV exports for Power BI                      | Generated                    |
| Power BI dashboard                            | Next development stage       |
| Final dashboard documentation and screenshots | Pending                      |

*Status reflects the work completed so far, not the entire planned project.*

---

## 🗄️ Database Overview

The project uses **DuckDB** as its analytical database.

Database file:

`cognistream.duckdb`

The current database contains five tables.

| Table                      | Row Count | Description                         |
| -------------------------- | --------: | ----------------------------------- |
| `events`                   |    21,128 | Developer activity events           |
| `developer_metrics`        |        20 | Developer-level metrics             |
| `ide_sessions`             |     1,226 | IDE session records                 |
| `ide_events_with_sessions` |    16,249 | IDE events associated with sessions |
| `team_metrics`             |         4 | Team-level metrics                  |

These tables support event-level analysis, developer comparisons, coding-session analysis, and team-level reporting.

### Dataset Coverage

* **Developers:** 20
* **Teams:** 4
* **IDE sessions:** 1,226
* **Total activity events:** 21,128
* **Event date range:** September 1–30, 2026

The dataset includes activity from IDE usage, GitHub commits, Slack, task switching, and meetings.

### Event Distribution

| Event Type    |      Count | Percentage |
| ------------- | ---------: | ---------: |
| IDE_ACTIVE    |     16,249 |     76.91% |
| GITHUB_COMMIT |      1,948 |      9.22% |
| Slack         |      1,407 |      6.65% |
| TASK_SWITCH   |        775 |      3.67% |
| MEETING       |        749 |      3.54% |
| **Total**     | **21,128** |   **100%** |

*Percentages are rounded. Event names and counts should be interpreted according to the project's source data.*

---

## 🔍 Data Analysis Implemented

### 1. Event Analysis

The event data provides a foundation for understanding developer activity across different tools and work-related events.

The current analysis includes:

* Event distribution and frequency.
* Activity patterns across the dataset.
* Developer activity aggregation.
* Team-level activity aggregation.
* Structured event-level data for further analysis.

### 2. Developer Metrics

The `developer_metrics` table contains aggregated metrics for 20 developers.

It provides a foundation for comparing developer activity and investigating differences in workflow patterns.

### 3. IDE Session Analysis

The `ide_sessions` table contains 1,226 session records.

Session-quality validation produced the following results:

| Validation Result                 |  Sessions |
| --------------------------------- | --------: |
| OK                                |     1,216 |
| Zero-duration, single-event flags |        10 |
| **Total**                         | **1,226** |

The flagged records are retained as validation findings rather than automatically being treated as invalid data.

This helps distinguish potentially unusual sessions from sessions that pass the current validation checks.

### 4. Team Activity Analysis

The `team_metrics` table contains aggregated metrics for four teams.

It supports team-level comparisons and provides a structured source for future Power BI visualizations.

### 5. SQL Analytics

The current SQL analysis includes:

* 12 analytical SQL queries.
* Data validation checks.
* Three analytical views.
* Aggregated event and team activity.
* IDE session quality analysis.

These queries provide a repeatable foundation for exploring the dataset and generating reporting outputs.

---

## 📁 Power BI Data Exports

Three CSV files have been generated for the next stage of dashboard development.

| File                  |   Rows | Purpose                      |
| --------------------- | -----: | ---------------------------- |
| `event_overview.csv`  | 21,128 | Event-level reporting        |
| `team_activity.csv`   |      4 | Team-level comparison        |
| `session_quality.csv` |  1,226 | IDE session quality analysis |

These exports separate the data into reporting-friendly datasets.

They can be imported into Power BI to build visualizations and interactive reports.

**Note:** CSV export is complete. The final Power BI dashboard and its visualizations are not yet documented as completed.

---

## 📂 Project Structure

The project uses separate locations for data, analysis, database code, SQL queries, and Power BI development.

```text
CogniStream/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│   └── database/
│
├── sql/
│
├── powerbi/
│
├── reports/
│
├── cognistream.duckdb
├── requirements.txt
└── README.md
```

*This is a logical overview of the project organization. Refer to the actual repository for the exact filenames and current contents of each directory.*

---

## ⚙️ Tools and Environment

The project uses Python with a virtual environment and DuckDB for analytical processing.

The development environment includes:

* Python
* Pandas
* NumPy
* DuckDB
* Matplotlib
* Seaborn
* Jupyter

A virtual environment helps isolate the project's Python dependencies from other projects.

---

## 🚀 Current Workflow

The implemented workflow can be summarized as follows:

```text
Developer Activity Data
          |
          v
   Data Processing
          |
          v
    DuckDB Database
          |
          v
     SQL Analysis
          |
          v
 Data Validation Checks
          |
          v
   Analytical Views
          |
          v
      CSV Exports
          |
          v
 Power BI Dashboard
   (Next Development Stage)
```

This workflow separates data preparation, storage, analytical processing, validation, and visualization.

---

## 📈 Planned Next Steps

The next development stage is to turn the prepared analytical datasets into an interactive Power BI dashboard.

### 1. Build the Power BI Dashboard

Import the three exported CSV files into Power BI and establish the appropriate relationships, if required by the chosen report design.

### 2. Create KPI Cards

Potential dashboard metrics include:

* Total activity events.
* Number of developers.
* Number of teams.
* Total IDE sessions.
* Session-quality results.

### 3. Develop Visualizations

Potential visuals include:

* Event distribution by event type.
* Activity comparison across teams.
* Developer activity comparisons.
* IDE session duration analysis.
* Session-quality breakdown.
* Workflow activity patterns.

### 4. Add Interactive Filters

Where the underlying data supports them, add filters for:

* Date.
* Developer.
* Team.
* Event type.

### 5. Validate Dashboard Results

Compare Power BI totals with the corresponding DuckDB tables and exported CSV files.

### 6. Document the Final Implementation

After the dashboard is completed, update the README with screenshots, final dashboard features, validated findings, and the completed project workflow.

---

## 🎓 Learning Outcomes

The current implementation demonstrates practical work in:

* Data processing with Python.
* Analytical database development with DuckDB.
* SQL-based data exploration.
* Aggregation and analytical view creation.
* Data validation and quality checks.
* Preparing datasets for business intelligence tools.
* Organizing an end-to-end data analytics workflow.

---

## 👨‍💻 Project Information

**Project:** CogniStream
**Category:** Data Analytics
**Primary Technologies:** Python, SQL, DuckDB, Pandas
**Visualization Tool:** Power BI — next development stage
**Repository:** [PritwishSaha/CogniStream](https://github.com/PritwishSaha/CogniStream)

---

## 📝 Conclusion

CogniStream is being developed as a structured developer productivity and workflow analytics platform.

The current implementation establishes the data-processing and analytical foundation through Python, DuckDB, SQL queries, validation checks, analytical views, and CSV exports.

The next major milestone is developing the Power BI dashboard to transform these datasets into interactive visual reports that make developer activity and team workflow patterns easier to explore.
