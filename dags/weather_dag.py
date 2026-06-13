from airflow.sdk import dag, task
from pendulum import datetime
from datetime import timedelta
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

from etl.extract.extract_data import extract_weather_data


API_KEY = os.getenv('API_KEY')

url = f"https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}"



@dag(
    dag_id='weather_etl',
    start_date=datetime(2026, 6, 14, tz="UTC"),
    schedule="0 12 * * *",
    catchup=False,
    description="ETL pipeline that extract weather data from OpenWeather API and stores raw JSON files",
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5)
    },
    tags=["etl", "weather", "openweather"]
)
def weather_pipeline():

    @task
    def extract():
        return extract_weather_data(url)

    @task transform(path_file):
        transform_weather_data(path_file)

transform(extract())    