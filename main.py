# from etl.extract.extract_data import extract_weather_data
# from etl.transform.transform_data import transform_weather_data
# from etl.load.load_data import load_weather_data
# from pathlib import Path
# from dotenv import load_dotenv
# import os

# import logging
# logging.basicConfig(level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# env_path = Path(__file__).resolve().parent / 'config' / '.env'
# raw_dir = Path(__file__).resolve().parent / 'data' / 'raw_data'

# load_dotenv(env_path)

# API_KEY = os.getenv('API_KEY')

# BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# city = "Sao Paulo"
# country = "BR"
# units = "metric"

# url = (
#     f"{BASE_URL}"
#     f"?q={city},{country}"
#     f"&units={units}"
#     f"&appid={API_KEY}"
# )

# table_name = 'sp_weather'

# def pipeline():
#      try:
#          logging.info("ETAPA 1: EXTRACT")
#          raw_path = extract_weather_data(url, raw_dir)
        
#          logging.info("ETAPA 2: TRANSFORM")
#          parquet_path = transform_weather_data(raw_path)
        
#          logging.info("ETAPA 3: LOAD")
#          load_weather_data(parquet_path)
        
#          print("\n" + "="*60)
#          print("✅ Pipeline concluído com sucesso!")
#          print("="*60)
        
#      except Exception as e:
#          logging.error(f"❌ ERRO no Pipeline: {e}")
#          import traceback
#          traceback.print_exc()
    
# pipeline()