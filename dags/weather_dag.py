import os
from airflow.sdk import dag, task
from pendulum import datetime
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path
from etl.extract.extract_data import extract_weather_data
from etl.transform.transform_data import transform_weather_data
from etl.load.load_data import load_weather_data


env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
url = f"https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}"

raw_dir = Path(__file__).resolve().parent.parent / 'data' / 'raw_data'

@dag(
    dag_id='weather_etl',
    start_date=datetime(2026, 6, 14, tz="UTC"),
    schedule="0 12 * * *",
    catchup=False,
    description="ETL pipeline that extract weather data from OpenWeather API and stores raw JSON files",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5)
    },
    tags=["etl", "weather", "pipeline"]
)
def weather_pipeline():

    @task
    def extract():
        file_path = extract_weather_data(url, raw_dir)
        return file_path

    @task
    def transform(file_path):
       clean_data_path = transform_weather_data(file_path)
       return clean_data_path

    @task
    def load(clean_data_path):
       load_weather_data(clean_data_path) 

    file_path = extract()
    clean_data_path = transform(file_path)
    load(clean_data_path)

weather_pipeline()
