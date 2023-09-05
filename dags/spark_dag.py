from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.operators.python_operator import PythonOperator
from airflow import DAG

from datetime import datetime, timedelta

with DAG(
    "spark_dag",
    default_args = {
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="Spark on kubernetes DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["demo"],
) as dag:
  moves = "{{ dag_run.conf.get('moves') or 'b4' }}"

  def push_args_callable(*, ti, moves):
    ti.xcom_push(key='args', value=[moves])
  
  push_args = PythonOperator(
    python_callable=push_args_callable,
    task_id='push_args',
    op_kwargs={"moves": moves},
    provide_context=True,
    dag=dag
  )

  t1 = SparkKubernetesOperator(
    task_id="spark_demo_op",
    application_file='spark.yaml',
    do_xcom_push=True,
    namespace='spark-demo',
    dag=dag,
  )

  push_args >> t1
  