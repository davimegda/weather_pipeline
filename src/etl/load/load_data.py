from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from pathlib import Path
from dotenv import load_dotenv
from etl.transform.transform_data import transform_weather_data 
import pandas as pd
import logging
import os

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

env_path = Path(__file__).resolve().parents[3] / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DB')
table_name = "sp_weather"

#PostgreSQL está rodando localmente no WSL.
# Se o banco estiver no host Windows/Docker Desktop,
# usar host.docker.internal.
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")


def get_engine():
    logging.info(f"Connecting at {host}:5432/{database}")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}}/{database}"
    )


def load_weather_data(table_name:str, df: pd.DataFrame):
    engine = get_engine()

    try:
        logging.info(f"Loading data into table: {table_name}")
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False
        )

        logging.info(f"Data loaded successfully")

        df_check = pd.read_sql(
            text(f"SELECT * FROM {table_name}"), 
            con=engine
    
        )

        logging.info(f"Records in table: {len(df_check)}")

    except Exception as e:
        logging.error(f"Error loading data to {table_name}: {e}")
        raise
