import datetime as dt

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from modules.run_ML_models import checker


args = {
    'owner': 'airflow',
    'start_date': dt.datetime.now(),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
    'depends_on_past': False,
}

with DAG(
        dag_id='loan_prediction',
        schedule="*/10 * * * *",
        default_args=args,
) as dag:
    run_ML_models = PythonOperator(
        task_id='run_ML_models',
        python_callable=checker,
        dag=dag
    )

    bash_task = BashOperator(
        task_id='bash_task',
        bash_command='echo Запуск ML моделей для предсказания по новым данным',
        dag=dag
    )

    bash_task >> run_ML_models
