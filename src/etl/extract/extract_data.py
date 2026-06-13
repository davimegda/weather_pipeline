import json
import requests
from pathlib import Path
import logging
import os

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def extract_weather_data(url:str):
    """
    Extract raw data from OpenWeather API and save it as a JSON file.
     
    This function performs the following steps:
    -Sends a GET request to the API
    -Validates the HTTP response satus
    -Parses the response as JSON
    -Saves the raw data into a JSON File

    :param url (str): API endpoint
    :return: Parsed JSON response (dict or list)
    """

    logging.info(f"Starting extraction process from URL: {url}")

    # Send the HTTP Get request and validate the response
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error while requesting data: {e}")
        raise

    # Parse response into JSON format
    weather_data = response.json()

    # Define output directory
    output_dir = Path("data/raw_data")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define file path
    file_path = output_dir / "weather_data"
    
    # Save JSON data into file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(weather_data, file, indent=4, ensure_ascii=False)
    
    logging.info(f"File successfully saved at: {file_path}")
    return str(file_path)