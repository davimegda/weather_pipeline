import pytest
import json
from unittest.mock import patch, Mock
from pathlib import Path
from requests.exceptions import RequestException

from etl.extract.extract_data import extract_weather_data

fake_url = "https://fakeapi.com/data"

@patch("etl.extract.extract_data.requests.get")
def test_extract_success(mock_get, tmp_path):
    """
    Ensure the function:
    - calls API successfully
    - returns a valid file path
    - creates a JSON file
    """

    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "Davi"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = extract_weather_data(fake_url, tmp_path)
    assert isinstance(result, Path)

    path = Path(result)
    assert path.exists()
    assert path.suffix == ".json"

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == {"id": 1, "name": "Davi"}


@patch("etl.extract.extract_data.requests.get")
def test_extract_api_failure(mock_get):
    """
    Test API failure handling:
    - ensures exception is raised when request fails
    """

    mock_get.side_effect = RequestException()

    with pytest.raises(RequestException):
        extract_weather_data(fake_url, Path("fakepath"))


@patch("etl.extract.extract_data.requests.get")
def test_timeout_is_set(mock_get, tmp_path):
    """
    Ensure request.get is called with timeout = 60.
    """

    mock_response = Mock()
    mock_response.json.return_value = {"x": 1}
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    extract_weather_data(fake_url, tmp_path)

    kwargs = mock_get.call_args.kwargs
    assert kwargs["timeout"] == 60