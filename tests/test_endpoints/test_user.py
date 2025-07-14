"""Tests for user endpoints."""

from unittest.mock import Mock, patch

import pytest

from whoop_client import WhoopClient
from whoop_client.models import UserBasicProfile, UserBodyMeasurement


@pytest.fixture
def client():
    """Create a WHOOP client."""
    return WhoopClient(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="http://localhost:8000/callback",
        access_token="test_token",
        refresh_token="refresh_token",
    )


class TestUserEndpoints:
    """Test user-specific endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_profile_basic(self, client):
        """Test retrieving basic user profile."""
        profile_data = {
            "user_id": 10129,
            "email": "jsmith123@whoop.com",
            "first_name": "John",
            "last_name": "Smith",
        }
        
        mock_response = Mock()
        mock_response.json.return_value = profile_data
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            profile = await client.get_profile_basic()
            
            mock_request.assert_called_once_with("GET", "/v2/user/profile/basic")
            
            assert isinstance(profile, UserBasicProfile)
            assert profile.user_id == 10129
            assert profile.email == "jsmith123@whoop.com"
            assert profile.first_name == "John"
            assert profile.last_name == "Smith"
    
    @pytest.mark.asyncio
    async def test_get_body_measurement(self, client):
        """Test retrieving user body measurements."""
        measurement_data = {
            "height_meter": 1.8288,
            "weight_kilogram": 90.7185,
            "max_heart_rate": 200,
        }
        
        mock_response = Mock()
        mock_response.json.return_value = measurement_data
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            measurement = await client.get_body_measurement()
            
            mock_request.assert_called_once_with("GET", "/v2/user/measurement/body")
            
            assert isinstance(measurement, UserBodyMeasurement)
            assert measurement.height_meter == 1.8288
            assert measurement.weight_kilogram == 90.7185
            assert measurement.max_heart_rate == 200