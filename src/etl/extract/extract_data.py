import json
import requests
import logging
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_weather_data(url:str, output_dir: Path):
    """
    Extract raw data from OpenWeather API and save it as a JSON file.
     
    Steps:
    -Sends a GET request to the API
    -Validates the HTTP response status
    -Parses the response as JSON
    -Saves the raw data into a JSON File

    :param url (str): API endpoint
    :param output_dir(Path): Directory where extracted weather data file will be stored
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

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define the path where the API response will be saved as a JSON file
    file_path = output_dir / "weather_data.json"
    
    # Save raw data into JSON file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(weather_data, file, indent=4, ensure_ascii=False)
    
    logging.info(f"File successfully saved at: {file_path}")
    return str(file_path)