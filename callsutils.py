from airflow_collibra_dq_provider.operators.dq import (
    CollibraDQCHeckAggregateScoreOperator,
    CollibraDQCHeckRuleOperator,
    CollibraDQCHeckScoreOperator,
    CollibraDQJobOperator
)

def create_aggregate_score_task(task_id, config, dag):
    """
    Create a Collibra Aggregate Score Task.
    """
    return CollibraDQCHeckAggregateScoreOperator(
        task_id=task_id,
        config=config,
        dag=dag
    )

def create_rule_task(task_id, rule_config, dag):
    """
    Create a Collibra Rule Check Task.
    """
    return CollibraDQCHeckRuleOperator(
        task_id=task_id,
        rule_config=rule_config,
        dag=dag
    )

def create_score_task(task_id, score_config, dag):
    """
    Create a Collibra Score Check Task.
    """
    return CollibraDQCHeckScoreOperator(
        task_id=task_id,
        score_config=score_config,
        dag=dag
    )

def create_job_task(task_id, job_config, dag):
    """
    Create a Collibra Job Task.
    """
    return CollibraDQJobOperator(
        task_id=task_id,
        job_config=job_config,
        dag=dag
    )
