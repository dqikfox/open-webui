import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json

@pytest.fixture
def client():
    from open_webui.main import app
    return TestClient(app)

@pytest.fixture
def mock_user():
    return Mock(id="test_user", email="test@example.com")

def test_oasis_status_endpoint(client, mock_user):
    with patch('open_webui.utils.auth.get_verified_user', return_value=mock_user):
        response = client.get("/api/oasis/status")
        assert response.status_code == 200
        data = response.json()
        assert "agent" in data
        assert "memory" in data

def test_oasis_execute_endpoint(client, mock_user):
    with patch('open_webui.utils.auth.get_verified_user', return_value=mock_user):
        response = client.post(
            "/api/oasis/execute",
            json={"command": "test hello"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["action"] == "test"

def test_oasis_tools_endpoint(client, mock_user):
    with patch('open_webui.utils.auth.get_verified_user', return_value=mock_user):
        response = client.get("/api/oasis/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data

@patch('psutil.cpu_percent')
@patch('psutil.virtual_memory')
@patch('psutil.disk_usage')
def test_system_stats_endpoint(mock_disk, mock_memory, mock_cpu, client, mock_user):
    mock_cpu.return_value = 50.0
    mock_memory.return_value = Mock(used=1000, total=2000, available=1000)
    mock_disk.return_value = Mock(used=500, total=1000, free=500)
    
    with patch('open_webui.utils.auth.get_verified_user', return_value=mock_user):
        response = client.get("/api/oasis/system/stats")
        assert response.status_code == 200
        data = response.json()
        assert "cpu" in data
        assert "memory" in data
        assert "disk" in data