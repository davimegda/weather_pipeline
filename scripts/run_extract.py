from dotenv import load_dotenv
from etl.extract.extract_data import extract_weather_data
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

output_dir = Path(__file__).resolve().parent.parent / "data" / "raw_data"

city = "Sao Paulo"
country = "BR"
units = "metric"

url = (
    f"{BASE_URL}"
    f"?q={city},{country}"
    f"&units={units}"
    f"&appid={API_KEY}"
)

extract_weather_data(url, output_dir)
