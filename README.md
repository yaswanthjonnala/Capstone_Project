# 📊 Education Enrollment & School Performance Intelligence Platform

**End-to-End Education Analytics & ETL Capstone Project**
Built using **Python, Pandas/PySpark, Databricks, Apache Airflow, and Power BI**

---

## 📌 Table of Contents

* [Overview](#-overview)
* [Architecture](#architecture)
* [Tech Stack](#tech-stack)
* [Features](#-features)
* [Setup & Installation](#-setup--installation)
* [Usage](#-usage)
* [Data Pipeline Details](#-data-pipeline-details)
* [Dashboards](#-dashboards)
* [Performance Metrics](#-performance-metrics)
* [Code Examples](#-code-examples)
* [Troubleshooting](#-troubleshooting)
* [Future Enhancements](#-future-enhancements)
* [Conclusion](#conclusion)
* [License](#-license)
* [Author](#-author)
* [Acknowledgments](#-acknowledgments)

---

## 📖 Overview

State education offices and school management bodies generate large volumes of student enrollment and academic performance data every year.
In many cases, this information remains scattered across spreadsheets or CSV exports and is updated inconsistently, making it difficult to use for timely decision-making.

This project delivers a **unified analytics platform** that transforms raw school data into **clean, validated, analytics-ready datasets** and **interactive dashboards** for education administrators.

---

## 🎯 Business Problem

Organizations face the following challenges:

* Data spread across multiple sources with no single trusted dataset
* Heavy dependency on manual compilation and repetitive reporting
* Delayed visibility into year-over-year enrollment trends
* Limited ability to identify early warning signs such as dropout risk or overcrowding

---

## 🎯 Project Goal

Build a complete, automated analytics pipeline that:

* Ingests raw enrollment and performance datasets
* Cleans, validates, deduplicates, and standardizes data
* Produces KPI-ready curated tables
* Automates ETL execution using Apache Airflow
* Enables interactive Power BI dashboards for monitoring and decision-making

---


### Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                        │
│  school_master.csv    enrollment.csv     performance.csv    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      BRONZE LAYER (Raw)                     │
│  • Raw ingestion • Schema enforcement • Basic validation    │
│  Output: bronze_* Delta tables                              │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     SILVER LAYER (Clean)                    │
│  • Cleaning • Standardization • Deduplication • Outliers    │
│  • Referential integrity checks                             │
│  Output: silver_* Delta tables                              │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     GOLD LAYER (Business)                   │
│  • Aggregations • KPIs • Trend analysis                     │
│  Output: enrollment_analytics, performance_analytics        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       POWER BI DASHBOARDS                   │
│  • Enrollment trends • Performance • Risk insights          │
└─────────────────────────────────────────────────────────────┘

                Orchestrated by Apache Airflow
```
### Orchestration Flow

```text
[Validate Sources] → [Run Bronze] → [Run Silver] → [Run Gold] → [Quality Check] → [Email Alert]
```

---

## 🛠️ Tech Stack

| Layer            | Technology                 | Purpose                              |
| ---------------- | -------------------------- | ------------------------------------ |
| Data Processing  | PySpark 3.5                | Distributed transformations          |
| Orchestration    | Apache Airflow 2.8         | Workflow scheduling & retries        |
| Platform         | Databricks                 | Unified analytics environment        |
| Visualization    | Power BI                   | Interactive dashboards               |
| Containerization | Docker                     | Reproducible environments            |
| Language         | Python 3.9+                | Pipeline development                 |
| Version Control  | Git                        | Source control                       |

---

## 📂 Dataset Description (Raw Inputs)

This project uses **three raw CSV datasets** that capture school master data, enrollment counts, and academic performance metrics across academic years and grade levels.

---

### 🏫 `school_master.csv`

**Description**
Master reference table for schools. This dataset is used for joins and provides dimensional attributes.

**Primary Key**

* `school_id`

**Columns**

* `school_id` – Unique school identifier (e.g., `SCH_0104`)
* `school_name` – Name of the school
* `region` – Region label (case and spelling variations exist)
* `district` – District name
* `school_type` – School category (e.g., Government / Govt / Private)
* `capacity` – School capacity (integer)

---

### 👩‍🎓 `student_enrollment.csv`

**Description**
Contains enrollment counts by school, academic year, grade level, and gender.

**Grain**

* `school_id` + `academic_year` + `grade_level` + `gender`

**Columns**

* `school_id` – Foreign key referencing `school_master`
* `academic_year` – Academic year of record
* `grade_level` – Grade/class (missing values exist)
* `gender` – Gender label (variants such as `M`, `Male`, `F`, `Female`)
* `student_count` – Enrollment count (null values exist)

---

### 📘 `student_performance.csv`

**Description**
Stores academic performance, attendance metrics, and dropout risk indicators by school, year, and grade.

**Grain**

* `school_id` + `academic_year` + `grade_level`

**Columns**

* `school_id` – Foreign key referencing `school_master`
* `academic_year` – Academic year of record
* `grade_level` – Grade/class (missing values exist)
* `average_score` – Average academic score (expected range: 0–100; nulls exist)
* `attendance_percentage` – Attendance percentage (expected range: 0–100; nulls exist)
* `dropout_risk_flag` – Binary dropout risk indicator (`0` / `1`; may contain nulls)

---

### ⚠️ Data Quality Notes

* Categorical fields contain **inconsistent spellings and casing**
  *(e.g., region, school_type, gender)* and are standardized in the **Silver layer**
* Several numeric fields contain **missing values** and are handled using validation and cleaning rules
* Expected numeric ranges (0–100) are enforced during data cleaning
* Deduplication and referential integrity checks are applied in later pipeline stages

---

## ✨ Features

### Data Engineering

* Medallion architecture (Bronze / Silver / Gold)
* Schema enforcement and validation
* Deduplication using window functions
* Outlier filtering (scores and attendance constraints)
* Referential integrity checks

### Orchestration

* Daily scheduled runs
* Retry logic with backoff
* Email notifications (success/failure)
* Execution logs and monitoring

### Analytics

* Enrollment trend analysis
* Performance metrics (scores, attendance)
* Dropout risk computation
* District and regional comparisons


## 🚀 Setup & Installation

### Prerequisites

* Python 3.9+
* Docker & Docker Compose
* Databricks account
* Power BI Desktop

### Clone Repository

```bash
git clone https://github.com/yaswanth/education-analytics-pipeline.git
cd education-analytics-pipeline
```

### Environment Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Environment Variables

```bash
cp .env.example .env
```

---

## 💻 Usage

### Run Pipeline via Airflow

```bash
airflow dags trigger Education_ETL_Production
```

### Run Databricks Notebooks

```python
%run /path/to/bronze_layer
%run /path/to/silver_layer
%run /path/to/gold_layer
```

---

## 🔄 Data Pipeline Details

### Bronze Layer

* Raw ingestion with schema enforcement
* Identifier presence checks
* Record count validation

### Silver Layer

* Cleaning and standardization
* Grade-level filtering
* Deduplication
* Outlier validation (0–100 ranges)

### Gold Layer

* Aggregations and KPIs
* Year-over-year enrollment growth
* Dropout rate computation
* Regional and school-level analytics

---

## 📊 Dashboards

### Dashboard 1: Enrollment Trend Analysis

**Purpose**

* Understand enrollment patterns and demographic distribution

**KPIs**

* Total Enrolled Students
* Average Students per School

**Visuals**

* Year-over-Year Enrollment Trend
* Gender Distribution (Donut Chart)
* Grade-wise Enrollment Distribution
* Top 10 Schools by Enrollment

**Slicers**

* Academic Year
* Gender
* School

---

### 📊 Dashboard 2: School Performance Comparison

**Purpose**

* Evaluate academic outcomes and dropout risk

**KPIs**

* Average Attendance (%)
* Average Academic Score
* Average Dropout Risk (%)

**Visuals**

* Attendance vs Academic Performance
* Attendance vs Dropout Trend Over Time
* Top 10 Schools by Dropout Risk
* High-Risk & Low-Performance Schools Table

**Special Features**

* Conditional formatting (green = low risk, red = high risk)
* Totals disabled for meaningful rate analysis

---

## 📈 Performance Metrics

* Average pipeline runtime: **8–12 minutes**
* Records processed: **~14,000**
* Data completeness: **98.5%**
* Success rate: **100%**

---

## 🐛 Troubleshooting

* Verify Airflow scheduler and webserver logs
* Validate Databricks token and workspace
* Use Gmail App Passwords for email alerts

---

## 🔮 Future Enhancements

* Real-time streaming ingestion
* ML-based dropout prediction
* dbt integration
* Unity Catalog governance
* REST API layer
* Advanced cohort analytics

---

## ✅ Conclusion

This project delivers a **production-style education analytics platform** using a Bronze–Silver–Gold architecture, Databricks, Apache Airflow, and Power BI. It demonstrates end-to-end data ingestion, validation, orchestration, and visualization, transforming raw education data into reliable, decision-ready insights. The solution reflects real-world data engineering practices and supports scalable, automated analytics for education planning and performance monitoring.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Yaswanth Reddy Jonnala**<br>
📧 Email: [yaswanthjonnala04@gmail.com](mailto:yaswanthjonnala04@gmail.com)<br>
💻 GitHub: [https://github.com/yaswanthjonnala](https://github.com/yaswanthjonnala)

---

## 🙏 Acknowledgments

* Databricks Community Edition
* Apache Spark & Apache Airflow communities
* Microsoft Power BI



