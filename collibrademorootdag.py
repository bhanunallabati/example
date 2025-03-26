from airflow import DAG
from datetime import datetime
from utils.collibra_utils import Collibra

# Define default_args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

# Instantiate the DAG
with DAG(
    dag_id='collibra_dq_demo',
    default_args=default_args,
    description='A demo DAG for Collibra Data Quality',
    schedule_interval='@daily',
    start_date=datetime(2025, 3, 1),
    catchup=False
) as dag:

    # Create tasks using the Collibra class
    aggregate_score_task = Collibra.create_aggregate_score_task(
        task_id='collibra_aggregate_score',
        config={'score_type': 'aggregate', 'threshold': 90},
        dag=dag
    )

    rule_task = Collibra.create_rule_task(
        task_id='collibra_rule_check',
        rule_config={'rule_name': 'data_quality_rule'},
        dag=dag
    )

    score_task = Collibra.create_score_task(
        task_id='collibra_score_check',
        score_config={'metric': 'accuracy'},
        dag=dag
    )

    job_task = Collibra.create_job_task(
        task_id='collibra_job_execution',
        job_config={'job_id': '12345'},
        dag=dag
    )

    # Define task dependencies
    aggregate_score_task >> rule_task >> score_task >> job_task
