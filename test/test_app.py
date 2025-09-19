from flask import session
import pytest
from flask.testing import FlaskClient
from unittest.mock import Mock, patch

@pytest.fixtu
def client():
    from app import app
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_requests():
    with patch('requests.request') as mock_req:
        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        mock_req.return_value = mock_resp
        return mock_req

def test_session_history(client: FlaskClient, mock_requests):
    mock_requests.return_value.text = '<div class="quote"><span class="text">Quote</span></div>'
    rv = client.post('/process', data={'url': 'https://example.com', 'mode': 'scrape', 'selectors': '.text', 'format': 'csv'})
    assert rv.status_code == 200
    assert b'table' in rv.data.lower()
    assert len(session.get('history', [])) > 0