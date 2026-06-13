import json
import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

file_path = Path(__file__).resolve().parents[3] / 'data' / 'raw_data' / 'weather_data.json'

columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_names_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds", 
        "sys.type": "sys_type",                 
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
    }
columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_weather_dataframe(file_path: Path):
    """
    Load a weather JSON file and transform to a Pandas DataFrame.

    Steps:
    - Load raw JSON data
    - Normalize main DataFrame structure
    - Extract and normalize nested 'weather' column (list of dictionaries)
    - Rename weather-related columns
    - Merge normalized data with main DataFrame
    - Remove original nested column

    :param file_path (Path): Path object where raw data was stored in the project
    :return (pd.DataFrame): Returns a Pandas DataFrame
    """

    logging.info("Creating DataFrame with JSON file...")

    path = file_path

    if not path.exists():
        logging.error(f"File not found: {path}")
        raise FileNotFoundError(f"File not found at: {path}")

    # Load JSON file
    logging.info("Loading JSON file...")
    with open(path, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    # Create base DataFrame
    df = pd.json_normalize(raw_data)
    logging.info(f"Base DataFrame created")
    return df

def normalize_weather_column(df: pd.DataFrame):
    """
    Normalize nasted 'weather' column from the Weather DataFrame

    :param df(pd.DataFrame): Recive Pandas DataFrame
    :return df(pd.DataFrame): Returns Pandas DataFrame
    """
    # Normalize nested weather column
    logging.info("Normalizing nested 'weather' column...")

    weather_df = pd.json_normalize(
        df['weather'].apply(
            lambda x: x[0] if isinstance(x, list) and len(x) > 0 else {}
        )
    )

    # Rename weather columns
    weather_df = weather_df.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    logging.info("Weather column normalized and successfully renamed!")

    # Merge DataFrames
    df = df.join(weather_df)
    print(f"Current DataFrame shape: {df.shape}")
    return df

def drop_columns(df: pd.DataFrame, columns_names: list[str]):
    """
    Drop columns from the Weather DataFrame.

    :param df(pd.DataFrame): Recive a Pandas DataFrame
    :return df(pd.DataFrame): Return a Pandas DataFrame
    """

    logging.info(f"Droping columns: {columns_names}")

    df = df.drop(columns=columns_names, errors='ignore')
    logging.info(f"Columns successfully droped!")
    print(f"Current DataFrame shape: {df.shape}")
    return df

def rename_columns(df: pd.DataFrame, columns_names: dict[str, str]):
    """
    Rename columns from the Weather DataFrame.

    :param df(pd.DataFrame): Recive a Pandas DataFrame
    :param columns_names(dict): Recive a dictionary with old column and the new name
    :return df(pd.DataFrame): Return a Pandas DataFrame
    """
    
    logging.info(f"Renaming DataFrame columns...")

    df = df.rename(columns=columns_names)
    logging.info(f"Columns successfully renamed!")
    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_names: list[str]):
    """
    Convert selected list of columns from the Weather DataFrame to datetime type

    :param df(pd.DataFrame): Recive a Pandas DataFrame
    :param columns_names(list): List of the columns names to be converted
    :return df(pd.DataFrame): Return a Pandas DataFrame
    """
    logging.info(f"Converting columns to datetime...")

    for name in columns_names:
        df[name] = (pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo'))
    logging.info(f"Columns successfully converted to datetime!")
    return df

def data_transformations():
    print(f"Initiating transformations... ")
    df = create_weather_dataframe(file_path)
    df = normalize_weather_column(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info(
        f"Transformation completed successfully. Final DataFrame: "
        f"{len(df)} rows and {len(df)} columns"
    )

    print(f"DataFrame HEAD: \n{df.head()}")
    print(f"DataFrame final shape: {df.shape}")
    return df

data_transformations()