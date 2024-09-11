from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from news.crawler import Crawler

# define default arguments for the DAG
default_args={
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,9,10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries':1,
    'retry_delay': timedelta(minutes=5)
}

# define the DAG
dag = DAG(
    'news_crawler',
    default_args='A simple news crawling DAG',
    schedule_interval='@hourly', # run every hour
)

# define the task that will run the crawling function
def run_news_crawler():
    crawler = Crawler()
    crawler.crawling_for_just_in()
    
# define a pythonoperator to run the crawler function
crawl_task = PythonOperator(
    task_id='run_new_crawler',
    python_callable=run_news_crawler,
    dag=dag,
)
