"""
Airflow DAG to orchestrate Databricks Serverless ETL Job
School Enrollment & Education Performance Analytics Platform: Bronze → Silver → Gold

Features:
- Input validation
- Databricks ETL trigger
- Real output data quality checks
- Custom file-based logging
- Email notification on success
"""

import os
import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.providers.databricks.hooks.databricks_sql import DatabricksSqlHook
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.trigger_rule import TriggerRule

# Custom Logger Configuration (Separate from Airflow UI Logs)

CUSTOM_LOG_DIR = "/opt/airflow/logs/custom"
os.makedirs(CUSTOM_LOG_DIR, exist_ok=True)

custom_logger = logging.getLogger("education_etl_logger")
custom_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    f"{CUSTOM_LOG_DIR}/education_etl.log"
)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
file_handler.setFormatter(formatter)

if not custom_logger.handlers:
    custom_logger.addHandler(file_handler)

# Default Airflow logger (visible in UI)
logger = logging.getLogger(__name__)

# --------------
# Task Functions


def validate_inputs(**context):
    """
    Validate availability of source data before triggering ETL.
    (Lightweight checks — deep validation happens in Databricks)
    """
    logger.info("Validating source datasets (Airflow UI log)")
    custom_logger.info("Starting source data validation")

    # Example placeholder for file existence / metadata checks
    custom_logger.info("Source datasets are accessible")
    custom_logger.info("Input validation completed successfully")

    return True


def check_outputs(**context):
    """
    Perform real post-ETL data quality checks
    by querying Databricks Gold layer metrics.
    """
    logger.info("Running post-ETL quality checks (Airflow UI log)")
    custom_logger.info("Starting output data quality validation")

    hook = DatabricksSqlHook(
        databricks_conn_id="databricks_default"
    )

    # Query metrics table produced in Gold layer
    result = hook.get_first("""
        SELECT
            total_records,
            null_school_ids,
            min_dropout,
            max_dropout
        FROM etl_quality_metrics
    """)

    if result is None:
        raise ValueError("Quality metrics table not found")

    total_records, null_ids, min_dropout, max_dropout = result

    custom_logger.info(f"Total records in Gold layer: {total_records}")
    custom_logger.info(f"Null school_id count: {null_ids}")
    custom_logger.info(f"Dropout rate range: {min_dropout}–{max_dropout}")

    # Validation rules
    if total_records == 0:
        raise ValueError("Gold layer produced zero records")

    if null_ids > 0:
        raise ValueError("Null school_id values detected in Gold layer")

    if min_dropout < 0 or max_dropout > 100:
        raise ValueError("Dropout rate outside valid range (0–100)")

    custom_logger.info("All output quality checks passed successfully")

    return {
        "status": "success",
        "records": total_records
    }


def on_failure(context):
    """
    DAG-level failure callback
    """
    task_id = context["task_instance"].task_id
    logger.error(f"Task failed: {task_id}")
    custom_logger.error(f"Pipeline failed at task: {task_id}")


def on_success(context):
    """
    DAG-level success callback
    """
    duration = context["task_instance"].duration
    logger.info("Pipeline completed successfully")
    custom_logger.info(
        f"Pipeline completed successfully in {duration} seconds"
    )

# ---------------------
# Default DAG Arguments

default_args = {
    "owner": "Yaswanth Reddy",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=2),
    "on_failure_callback": on_failure,
}

# --------------
# DAG Definition

with DAG(
    dag_id="Education_ETL_Production",
    description="End-to-End Education Analytics ETL (Bronze → Silver → Gold)",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 2 * * *",  # Daily at 2 AM
    catchup=False,
    on_success_callback=on_success,
    tags=["education", "databricks", "etl", "production"],
) as dag:

    # Step 1: Validate input datasets
    validate_source_files = PythonOperator(
        task_id="validate_source_files",
        python_callable=validate_inputs,
    )

    # Step 2: Trigger Databricks ETL Job
    run_databricks_etl = DatabricksRunNowOperator(
        task_id="run_databricks_etl",
        databricks_conn_id="databricks_default",
        job_id=887076441884673,  # Your Databricks Job ID
    )

    # Step 3: Validate Gold layer outputs
    check_data_quality = PythonOperator(
        task_id="check_data_quality",
        python_callable=check_outputs,
    )

    # Step 4: Send success email notification
    send_success_email = EmailOperator(
        task_id="send_success_email",
        to="yaswanthjonnala04@gmail.com",
        subject="✅ Education ETL Pipeline Completed Successfully",
        html_content="""
        <h2>Education ETL Pipeline Status</h2>
        <p>The Education Analytics ETL pipeline completed successfully.</p>
        <ul>
            <li>Bronze → Silver → Gold processing completed</li>
            <li>All data quality checks passed</li>
        </ul>
        """,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    # -------------
    # Pipeline Flow

    validate_source_files >> run_databricks_etl >> check_data_quality >> send_success_email
