import pytest
import requests.exceptions

from api_client_clean.client.api_client import APIClient
from unittest.mock import Mock, patch

def test_send_data_success():
    client = APIClient("https://httpbin.org")
    payload = {"msg": "Hallo Leo"}
    response = client.send_data(payload, path="post")

    assert response["json"] == payload

def test_send_data_error():
    client = APIClient("https://httpbin.org")
    payload = {"msg": "Hallo Leo"}

    with pytest.raises(Exception) as excinfo:
        client.send_data(payload, path="falsch")

    assert "Fehler" in str(excinfo)

def test_send_data_timeout():
    client = APIClient("https://10.255.255.1")
    payload = {"msg": "Hallo Leo"}

    with pytest.raises(Exception) as excinfo:
        client.send_data(payload)
    assert "Alle Versuche fehlgeschlagen" in str(excinfo.value)

@patch("client.api_client.requests.get")
def test_get_status_success(mock_get):
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"status": "ok"}

    mock_get.return_value = fake_response

    client = APIClient("https://example.com")
    result = client.get_status()

    assert result["status"] == "ok"
    mock_get.assert_called_once_with("https://example.com/status", timeout=5)

@patch("client.api_client.requests.get")
def test_get_status_error(mock_get):
    fake_response = Mock()
    fake_response.status_code = 503

    mock_get.return_value = fake_response

    client = APIClient("https://example.com")

    with pytest.raises(Exception) as excinfo:
        client.get_status()

    assert "Statusfehler" in str(excinfo.value)

@patch("client.api_client.requests.get")
def test_get_status_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout

    client = APIClient("https://example.com")

    with pytest.raises(Exception) as excinfo:
        client.get_status()

    assert "Timeout beim Abrufen des Status" in str(excinfo.value)


