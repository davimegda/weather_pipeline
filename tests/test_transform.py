import pytest
import pandas as pd
from pathlib import Path

from etl.transform.transform_data import (
    data_transformations,
    create_weather_dataframe
)


@pytest.fixture
def sample_weather_file(tmp_path):
    import json

    data = {
        "weather": [{
            "id": 1,
            "main": "Clouds",
            "description": "overcast",
            "icon": "04d"
        }],
        "coord": {
            "lon": -46.6,
            "lat": -23.5
        },
        "main": {
            "temp": 25,
            "feels_like": 26,
            "pressure": 1012,
            "humidity": 80
        },
        "dt": 1700000000,
        "sunrise": 1700000001,
        "sunset": 1700009999,
        "name": "Test City"
    }

    file = tmp_path / "weather.json"
    file.write_text(json.dumps(data))
    return Path(file)


def test_etl_pipeline_and_file_handling(sample_weather_file):
    """
    Ensure ETL pipeline executes correctly with controlled input data
    """

    # Act
    df = data_transformations(sample_weather_file)

    # Assert - structure
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape[0] > 0

    # Assert - expected columns
    expected_columns = [
        "weather_id",
        "latitude",
        "city_name",
        "sunrise"
    ]

    for col in expected_columns:
        assert col in df.columns

    # Assert - removed columns
    assert "weather" not in df.columns

    # Assert - datetime conversion
    assert pd.api.types.is_datetime64_any_dtype(df["sunrise"])
    assert pd.api.types.is_datetime64_any_dtype(df["sunset"])


def test_create_weather_dataframe_file_not_found():
    """
    Ensure function raises FileNotFoundError when path is invalid
    """

    with pytest.raises(FileNotFoundError):
        create_weather_dataframe(Path("invalid/path.json"))