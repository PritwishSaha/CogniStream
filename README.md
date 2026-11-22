# 🧠 CogniStream
### Developer Productivity & Workflow Analytics Platform

<p align="center">
  <strong>Transforming Developer Activity Data into Actionable Business Intelligence</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-Completed-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Domain-Data%20Analytics-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.13-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Database-DuckDB-orange?style=for-the-badge&logo=duckdb" />
  <img src="https://img.shields.io/badge/Visualization-Power%20BI-F2C811?style=for-the-badge&logo=powerbi" />
</p>

---

## 📌 1. Project Overview

**CogniStream** is an end-to-end Developer Productivity and Workflow Analytics platform designed to analyze developer activities, coding sessions, collaboration patterns, and team performance.

In modern software development environments, developers interact with multiple tools, including Integrated Development Environments (IDEs), GitHub, Slack, task management systems, and meeting platforms.

However, understanding how these activities collectively influence productivity and workflow efficiency can be challenging.

CogniStream addresses this challenge by transforming raw developer activity events into structured analytical datasets and interactive business intelligence dashboards.

The project uses Python for data processing, DuckDB for analytical data storage, SQL for querying and analysis, and Microsoft Power BI for interactive visualization.

It provides insights into:

- Developer activity distribution.
- IDE usage and coding sessions.
- Team-level activity patterns.
- Developer-level performance metrics.
- Session quality and unusual activity.
- Workflow behavior and collaboration patterns.
- Overall developer productivity indicators.

The objective is to provide a centralized analytical solution that helps understand developer workflows through measurable data.

---

## 🎯 2. Project Objectives

The primary objectives of CogniStream are:

1. **Developer Activity Analysis:** Understand how developers interact with different development tools and platforms.

2. **Workflow Analysis:** Examine coding sessions, activity patterns, and workflow behavior.

3. **Team Performance Analysis:** Compare activity across different development teams.

4. **Session Quality Monitoring:** Identify unusual or potentially problematic IDE sessions through validation checks.

5. **Data Engineering:** Develop a structured data processing and storage pipeline using Python and DuckDB.

6. **SQL Analytics:** Extract meaningful information using analytical SQL queries and database views.

7. **Business Intelligence:** Develop an interactive Power BI dashboard to communicate analytical findings.

8. **Decision Support:** Transform developer activity data into understandable metrics that can support workflow evaluation.

---

## 💡 3. Problem Statement

Software development teams generate significant amounts of activity data through different development platforms.

Although individual tools provide activity information, combining these records into a unified analytical system is difficult.

Some common challenges include:

- Developer activity information is distributed across multiple platforms.
- Team-level activity comparisons are difficult without centralized reporting.
- IDE session patterns are not always easy to understand.
- Unusual or low-quality session records can affect analytical results.
- Raw activity data does not directly communicate meaningful business insights.

**CogniStream solves this problem by creating a centralized analytics pipeline that processes developer activity data and presents meaningful information through interactive dashboards.**

---

## 🛠️ 4. Technology Stack

| Technology | Application |
|---|---|
| Python | Data processing and automation |
| Pandas | Data manipulation and transformation |
| NumPy | Numerical computation |
| DuckDB | Analytical database management |
| SQL | Data querying and analytical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Jupyter Notebook | Interactive analysis and experimentation |
| Microsoft Power BI | Interactive dashboard development |
| Git | Version control |
| GitHub | Source code management and project hosting |

### Core Technologies

**Python:** Used to process, transform, and prepare developer activity datasets.

**Pandas:** Used for structured data manipulation, aggregation, and preprocessing.

**DuckDB:** Used as the analytical database for storing and querying structured datasets.

**SQL:** Used to perform analytical queries, data validation, aggregations, and create database views.

**Power BI:** Used to build interactive dashboards for exploring developer activity, team performance, and session quality.

---

## 📊 5. Dataset Overview

The project analyzes developer activity data collected across multiple development-related activities.

### Dataset Summary

| Metric | Value |
|---|---:|
| Total Activity Events | 21,128 |
| Total Developers | 20 |
| Total Development Teams | 4 |
| Total IDE Sessions | 1,226 |
| IDE Activity Events | 16,249 |
| Data Coverage | September 2026 |
| Total Database Tables | 5 |

### Team Distribution

The dataset includes four development teams:

| Team | Developers |
|---|---:|
| Frontend | 5 |
| Backend | 5 |
| DevOps | 5 |
| Data | 5 |
| **Total** | **20** |

### Activity Categories

The activity dataset contains events associated with:

- IDE activity.
- GitHub commits.
- Slack interactions.
- Task switching.
- Meetings.

### Event Distribution

| Event Type | Event Count | Percentage |
|---|---:|---:|
| IDE_ACTIVE | 16,249 | 76.91% |
| GITHUB_COMMIT | 1,948 | 9.22% |
| Slack | 1,407 | 6.65% |
| TASK_SWITCH | 775 | 3.67% |
| MEETING | 749 | 3.54% |
| **Total** | **21,128** | **100%** |

*Percentages are rounded.*

### Initial Observation

IDE activity represents approximately 76.91% of all recorded events, making it the dominant activity category in the dataset.

This indicates that IDE-related events form the largest component of the recorded developer activity.

---

## ⚙️ 6. Project Architecture

CogniStream follows a structured data analytics architecture.

```text
             DEVELOPER ACTIVITY DATA
                       |
                       |
                       ▼
              DATA PROCESSING
                  (Python)
                       |
                       |
                       ▼
                DATA CLEANING
               & TRANSFORMATION
                       |
                       |
                       ▼
                DUCKDB DATABASE
                       |
           ┌───────────┼───────────┐
           |           |           |
           ▼           ▼           ▼
        EVENTS      DEVELOPERS   IDE SESSIONS
           |           |           |
           └───────────┼───────────┘
                       |
                       ▼
                  SQL ANALYTICS
                       |
                       ▼
                DATA VALIDATION
                       |
                       ▼
                ANALYTICAL VIEWS
                       |
                       ▼
                  CSV EXPORTS
                       |
                       ▼
                MICROSOFT POWER BI
                       |
          ┌────────────┼─────────────┐
          |            |             |
          ▼            ▼             ▼
       Overview    Team Activity   Developer
                                   Analytics
          |            |             |
          └────────────┼─────────────┘
                       |
                       ▼
                BUSINESS INSIGHTS
```

### Architecture Components

**1. Data Processing Layer**

Python and Pandas are used to process developer activity records and prepare structured datasets.

**2. Database Layer**

DuckDB stores the processed information in structured relational tables.

**3. Analytics Layer**

SQL queries and analytical views are used to generate aggregated metrics and investigate activity patterns.

**4. Validation Layer**

Data quality checks are performed to identify unusual or potentially problematic records.

**5. Visualization Layer**

Prepared CSV datasets are imported into Power BI to develop interactive analytical dashboards.

**6. Business Intelligence Layer**

The completed dashboards provide a consolidated view of developer activity, team performance, and workflow indicators.

---

## 🗄️ 7. Database Design

CogniStream uses **DuckDB** as its analytical database.

Database file:

`cognistream.duckdb`

The database contains five primary tables.

| Table Name | Records | Description |
|---|---:|---|
| `events` | 21,128 | Developer activity event records |
| `developer_metrics` | 20 | Developer-level aggregated metrics |
| `ide_sessions` | 1,226 | IDE session information |
| `ide_events_with_sessions` | 16,249 | IDE events associated with sessions |
| `team_metrics` | 4 | Aggregated team-level metrics |

### Table Descriptions

**1. events**

Contains developer activity records from different platforms and tools.

Used for:
- Event distribution analysis.
- Activity frequency analysis.
- Developer activity exploration.
- Event-level reporting.

**2. developer_metrics**

Contains aggregated metrics for individual developers.

Used for:
- Developer-level comparisons.
- Activity analysis.
- Individual metric reporting.

**3. ide_sessions**

Contains structured IDE session information.

Used for:
- Session duration analysis.
- Session quality evaluation.
- Coding session exploration.

**4. ide_events_with_sessions**

Contains IDE activity events associated with their respective sessions.

Used for:
- IDE activity analysis.
- Session-level event exploration.
- Activity aggregation.

**5. team_metrics**

Contains aggregated information for the four development teams.

Used for:
- Team-level comparisons.
- Team activity analysis.
- Power BI reporting.

---

## 🔍 8. Data Analysis and SQL Implementation

SQL is an important component of the CogniStream analytics pipeline.

The project includes 12 analytical SQL queries and three analytical database views.

### SQL Analysis Areas

| Analysis | Purpose |
|---|---|
| Event Distribution | Understand the frequency of different activity types |
| Developer Activity | Compare activity across developers |
| Team Activity | Analyze activity across development teams |
| IDE Session Analysis | Investigate coding session patterns |
| Session Duration | Examine session duration metrics |
| Session Quality | Identify unusual session records |
| Activity Aggregation | Generate summarized analytical results |
| Data Validation | Check data consistency and quality |

### Analytical Views

Three analytical views were created to organize frequently used analytical results.

These views help simplify reporting queries and provide reusable analytical datasets.

### SQL Benefits

- Efficient analytical querying.
- Structured data aggregation.
- Reusable analytical logic.
- Easier data validation.
- Improved reporting workflow.

---

## 🧹 9. Data Quality and Validation

Data quality is essential for generating reliable analytical results.

CogniStream includes validation checks to examine the consistency of processed datasets and IDE session records.

### IDE Session Quality Analysis

The current session validation results are:

| Validation Category | Count |
|---|---:|
| Validated Sessions (OK) | 1,216 |
| Flagged Sessions | 10 |
| Total Sessions | 1,226 |

### Session Quality Rate

\[
\text{Pass Rate} =
\frac{1216}{1226}\times100
\]

\[
\boxed{99.18\%}
\]

The current validation indicates that approximately 99.18% of the IDE sessions passed the implemented quality checks.

The remaining 10 sessions were flagged for further examination.

**Important:** A flagged session is not automatically a fraudulent or invalid session. It represents a record requiring additional attention based on the implemented validation rules.

---

## 📈 10. Power BI Dashboard

Microsoft Power BI is used to convert the processed analytical datasets into interactive reports.

The completed CogniStream dashboard contains five analytical pages.

### Dashboard 1: Overview Dashboard

**Purpose:** Provide a consolidated overview of developer activity and project-level KPIs.

Key indicators include:

- Total activity events.
- Total developers.
- Total development teams.
- Total IDE sessions.
- Overall activity distribution.

Potential analytical questions addressed:

- How much activity was recorded?
- How many developers contributed to the dataset?
- Which activity categories dominate?
- What is the overall distribution of developer activity?

### Dashboard 2: Team Activity

**Purpose:** Analyze activity patterns across different development teams.

Teams included:

- Frontend.
- Backend.
- DevOps.
- Data.

Analytical focus:

- Team-level activity distribution.
- Comparison of team metrics.
- Activity patterns across teams.
- Team-level reporting.

This page helps explore differences in recorded activity between development teams.

### Dashboard 3: Session Quality

**Purpose:** Examine IDE session records and their validation results.

Key metrics:

- Total IDE sessions: 1,226.
- Validated sessions: 1,216.
- Flagged sessions: 10.
- Session quality pass rate: 99.18%.

Analytical focus:

- Session quality distribution.
- Validated versus flagged sessions.
- Session-level metrics.
- Unusual session records.

This page helps identify records that may require further examination.

### Dashboard 4: Developer Analytics

**Purpose:** Explore individual developer activity and productivity-related indicators.

Analytical focus:

- Developer-level metrics.
- Individual activity comparisons.
- Developer activity patterns.
- IDE session-related information.

This page provides a more detailed perspective on individual developer activity.

**Note:** Recorded activity is not equivalent to actual productivity or work quality. The dashboard provides behavioral indicators, not a definitive ranking of developer performance.

### Dashboard 5: Executive Insights

**Purpose:** Present high-level analytical findings in a business-oriented format.

The page brings together important metrics and analytical observations from the project.

Its purpose is to make the results understandable for decision-makers without requiring them to examine individual database tables or SQL queries.

Analytical focus:

- Overall activity patterns.
- Team-level observations.
- Developer activity indicators.
- Session quality findings.
- High-level reporting.

---

## 📊 11. Key Analytical Findings

The current dataset provides several useful observations.

### Finding 1: IDE Activity Dominates

IDE_ACTIVE accounts for 16,249 events, approximately 76.91% of the total activity.

This establishes IDE usage as the largest recorded activity category.

### Finding 2: Multiple Development Activities

The dataset captures activity beyond IDE usage, including GitHub commits, Slack interactions, meetings, and task switching.

This provides a broader view of the development workflow.

### Finding 3: Balanced Team Representation

The dataset includes 20 developers distributed equally across four teams, with five developers per team.

This makes team-level comparisons possible.

### Finding 4: Session Quality

Out of 1,226 IDE sessions, 1,216 passed the implemented validation checks.

The resulting session quality pass rate is approximately 99.18%.

### Finding 5: Session Duration

The current IDE session analysis indicates:

| Metric | Result |
|---|---:|
| Average IDE session duration | 98.67 minutes |
| Average elapsed session duration | 127.78 minutes |
| Average events per session | 13.25 |

These measurements provide an understanding of the recorded coding session patterns.

*Session duration and elapsed duration represent different measurements and should not be treated as interchangeable.*

---

## 📁 12. Project Directory Structure

The project is organized into separate components for data processing, database operations, SQL analytics, and reporting.

```text
CogniStream/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   └── database/
│       ├── load_data.py
│       └── run_analysis.py
│
├── sql/
│   └── cognistream_analysis.sql
│
├── notebooks/
│
├── powerbi/
│   ├── event_overview.csv
│   ├── team_activity.csv
│   └── session_quality.csv
│
├── reports/
│
├── cognistream.duckdb
│
├── requirements.txt
│
└── README.md
```

*The structure above is a logical representation. Keep the actual repository filenames and directory names if they differ.*

---

## 🚀 13. Installation and Setup

Follow these steps to set up the project locally.

### Step 1: Clone the Repository

```bash
git clone https://github.com/PritwishSaha/CogniStream.git
```

### Step 2: Navigate to the Project

```bash
cd CogniStream
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Load Data into DuckDB

```bash
python src/database/load_data.py
```

### Step 7: Execute the Analysis

```bash
python src/database/run_analysis.py
```

*These commands represent the documented project workflow. The data files and dependencies must be available in the repository, and the scripts should be run in the appropriate order.*

---

## 📊 14. Power BI Integration

The project generates three CSV exports for Power BI reporting.

| CSV File | Records | Application |
|---|---:|---|
| `event_overview.csv` | 21,128 | Event overview |
| `team_activity.csv` | 4 | Team activity |
| `session_quality.csv` | 1,226 | Session quality |

### Importing the Data

1. Open Microsoft Power BI Desktop.
2. Select **Get Data**.
3. Choose **Text/CSV**.
4. Import the three exported datasets.
5. Verify column data types.
6. Configure relationships where necessary.
7. Create measures and visualizations.
8. Build the five dashboard pages.

---

## 💼 15. Business Applications

CogniStream demonstrates how developer activity data can be used for workflow analytics and organizational reporting.

Potential applications include:

- Understanding development activity patterns.
- Comparing recorded activity across teams.
- Identifying unusual session records.
- Monitoring IDE usage patterns.
- Exploring collaboration-related activity.
- Supporting workflow improvement discussions.
- Providing centralized analytical reporting.

The platform is intended to support data-informed workflow evaluation rather than make definitive judgments about individual developer productivity.

---

## 🧠 16. Skills Demonstrated

This project demonstrates practical knowledge and implementation experience in:

### Data Analytics
- Data exploration.
- Data preprocessing.
- Data aggregation.
- Statistical analysis.
- Analytical reporting.

### Python Development
- Pandas.
- NumPy.
- Data manipulation.
- Database integration.
- Script-based processing.

### Database Management
- DuckDB.
- Relational data organization.
- SQL queries.
- Analytical views.
- Data validation.

### Business Intelligence
- Power BI.
- KPI reporting.
- Interactive dashboards.
- Data visualization.
- Team-level analysis.

### Professional Development
- Project organization.
- Analytical problem-solving.
- Data-driven decision-making.
- Version control using Git and GitHub.
- End-to-end project implementation.

---

## 🎓 17. Learning Outcomes

Through the development of CogniStream, the project demonstrates the practical application of a complete data analytics workflow.

Major learning outcomes include:

1. Working with structured developer activity datasets.
2. Processing and transforming data using Python and Pandas.
3. Creating an analytical database using DuckDB.
4. Performing data exploration and analysis using SQL.
5. Implementing data validation checks.
6. Creating reusable analytical database views.
7. Preparing datasets for business intelligence reporting.
8. Developing interactive dashboards using Power BI.
9. Converting raw data into meaningful analytical observations.
10. Organizing an end-to-end analytics project.

---

## 📸 18. Project Screenshots

Screenshots of the completed Power BI dashboard can be added here.

### Dashboard Overview

<!-- Add your Overview dashboard screenshot here -->

### Team Activity

<!-- Add your Team Activity dashboard screenshot here -->

### Session Quality

<!-- Add your Session Quality dashboard screenshot here -->

### Developer Analytics

<!-- Add your Developer Analytics dashboard screenshot here -->

### Executive Insights

<!-- Add your Executive Insights dashboard screenshot here -->

---

## 🏁 19. Project Status

<p align="center">
  <img src="https://img.shields.io/badge/Development-Completed-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Database-Completed-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/SQL%20Analytics-Completed-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Power%20BI-Completed-yellow?style=for-the-badge" />
</p>

**CogniStream is a completed Data Analytics and Business Intelligence project.**

The project covers the complete analytical workflow, including data processing, database development, SQL analysis, data quality validation, analytical exports, and interactive Power BI dashboards.

It demonstrates how raw developer activity records can be transformed into structured analytical information and presented through business intelligence visualizations.

---

## 👨‍💻 20. Author

**Pritwish Saha**

B.Tech – Computer Science and Engineering (Artificial Intelligence & Machine Learning)

Brainware University

### Connect With Me

- GitHub: [PritwishSaha](https://github.com/PritwishSaha)
- LinkedIn: [Pritwish Saha](https://www.linkedin.com/in/pritwish-saha-b49604362/)
- Portfolio: [Personal Portfolio](https://infotact.in/pritwish-hk5nxp)

---

<p align="center">
  <strong>CogniStream — Turning Developer Activity into Data-Driven Insights.</strong>
</p>

<p align="center">
  ⭐ If you find this project interesting, consider starring the repository!
</p>
