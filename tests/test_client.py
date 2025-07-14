"""Tests for WHOOP API client."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

import httpx
import pytest

from whoop_client import WhoopClient
from whoop_client.auth import OAuth2Handler, TokenResponse
from whoop_client.models import (
    Cycle,
    CycleScore,
    PaginatedCycleResponse,
    Recovery,
    RecoveryCollection,
    RecoveryScore,
    ScoreState,
    Sleep,
    UserBasicProfile,
    UserBodyMeasurement,
    WorkoutV2,
)


@pytest.fixture
def mock_auth():
    """Create a mock OAuth2Handler."""
    auth = Mock(spec=OAuth2Handler)
    auth.access_token = "test_access_token"
    auth.refresh_token = "test_refresh_token"
    auth.is_token_expired.return_value = False
    return auth


@pytest.fixture
def client(mock_auth):
    """Create a WHOOP client with mocked auth."""
    client = WhoopClient(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="http://localhost:8000/callback",
    )
    client.auth = mock_auth
    return client


class TestWhoopClient:
    """Test WHOOP client methods."""
    
    @pytest.mark.asyncio
    async def test_get_cycle_by_id(self, client):
        """Test getting a cycle by ID."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 12345,
            "user_id": 67890,
            "created_at": "2023-01-01T10:00:00Z",
            "updated_at": "2023-01-01T11:00:00Z",
            "start": "2023-01-01T00:00:00Z",
            "end": "2023-01-01T23:59:59Z",
            "timezone_offset": "-05:00",
            "score_state": "SCORED",
            "score": {
                "strain": 5.5,
                "kilojoule": 8000.0,
                "average_heart_rate": 70,
                "max_heart_rate": 140,
            },
        }
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            cycle = await client.get_cycle_by_id(12345)
            
            mock_request.assert_called_once_with("GET", "/v2/cycle/12345")
            assert isinstance(cycle, Cycle)
            assert cycle.id == 12345
            assert cycle.score.strain == 5.5
    
    @pytest.mark.asyncio
    async def test_get_cycle_collection(self, client):
        """Test getting a collection of cycles."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "records": [
                {
                    "id": 12345,
                    "user_id": 67890,
                    "created_at": "2023-01-01T10:00:00Z",
                    "updated_at": "2023-01-01T11:00:00Z",
                    "start": "2023-01-01T00:00:00Z",
                    "timezone_offset": "-05:00",
                    "score_state": "PENDING_SCORE",
                }
            ],
            "next_token": "token123",
        }
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            response = await client.get_cycle_collection(limit=10)
            
            mock_request.assert_called_once_with(
                "GET", "/v2/cycle", params={"limit": 10}
            )
            assert isinstance(response, PaginatedCycleResponse)
            assert len(response.records) == 1
            assert response.next_token == "token123"
    
    @pytest.mark.asyncio
    async def test_get_sleep_by_id(self, client):
        """Test getting a sleep by ID."""
        sleep_id = "550e8400-e29b-41d4-a716-446655440000"
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": sleep_id,
            "user_id": 12345,
            "created_at": "2023-01-01T10:00:00Z",
            "updated_at": "2023-01-01T11:00:00Z",
            "start": "2023-01-01T00:00:00Z",
            "end": "2023-01-01T08:00:00Z",
            "timezone_offset": "-05:00",
            "nap": False,
            "score_state": "SCORED",
        }
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            sleep = await client.get_sleep_by_id(sleep_id)
            
            mock_request.assert_called_once_with(
                "GET", f"/v2/activity/sleep/{sleep_id}"
            )
            assert isinstance(sleep, Sleep)
            assert str(sleep.id) == sleep_id
            assert sleep.nap is False
    
    @pytest.mark.asyncio
    async def test_get_recovery_for_cycle(self, client):
        """Test getting recovery for a cycle."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "cycle_id": 12345,
            "sleep_id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": 67890,
            "created_at": "2023-01-01T10:00:00Z",
            "updated_at": "2023-01-01T11:00:00Z",
            "score_state": "SCORED",
            "score": {
                "user_calibrating": False,
                "recovery_score": 65.0,
                "resting_heart_rate": 55.0,
                "hrv_rmssd_milli": 45.5,
            },
        }
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            recovery = await client.get_recovery_for_cycle(12345)
            
            mock_request.assert_called_once_with(
                "GET", "/v2/activity/recovery/cycle/12345/recovery"
            )
            assert isinstance(recovery, Recovery)
            assert recovery.cycle_id == 12345
            assert recovery.score.recovery_score == 65.0
    
    @pytest.mark.asyncio
    async def test_get_profile_basic(self, client):
        """Test getting basic user profile."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "user_id": 12345,
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            profile = await client.get_profile_basic()
            
            mock_request.assert_called_once_with("GET", "/v2/user/profile/basic")
            assert isinstance(profile, UserBasicProfile)
            assert profile.email == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_get_body_measurement(self, client):
        """Test getting body measurements."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "height_meter": 1.80,
            "weight_kilogram": 75.5,
            "max_heart_rate": 190,
        }
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            measurement = await client.get_body_measurement()
            
            mock_request.assert_called_once_with("GET", "/v2/user/measurement/body")
            assert isinstance(measurement, UserBodyMeasurement)
            assert measurement.height_meter == 1.80
    
    @pytest.mark.asyncio
    async def test_iterate_cycles(self, client):
        """Test iterating through cycles with pagination."""
        # First page
        mock_response1 = Mock()
        mock_response1.json.return_value = {
            "records": [
                {
                    "id": 1,
                    "user_id": 100,
                    "created_at": "2023-01-01T10:00:00Z",
                    "updated_at": "2023-01-01T11:00:00Z",
                    "start": "2023-01-01T00:00:00Z",
                    "timezone_offset": "-05:00",
                    "score_state": "SCORED",
                }
            ],
            "next_token": "page2",
        }
        
        # Second page
        mock_response2 = Mock()
        mock_response2.json.return_value = {
            "records": [
                {
                    "id": 2,
                    "user_id": 100,
                    "created_at": "2023-01-02T10:00:00Z",
                    "updated_at": "2023-01-02T11:00:00Z",
                    "start": "2023-01-02T00:00:00Z",
                    "timezone_offset": "-05:00",
                    "score_state": "SCORED",
                }
            ],
            "next_token": None,
        }
        
        with patch.object(
            client, "_request", side_effect=[mock_response1, mock_response2]
        ):
            cycles = []
            async for cycle in client.iterate_cycles():
                cycles.append(cycle)
            
            assert len(cycles) == 2
            assert cycles[0].id == 1
            assert cycles[1].id == 2
    
    @pytest.mark.asyncio
    async def test_token_refresh(self, client):
        """Test automatic token refresh."""
        client.auth.is_token_expired.return_value = True
        client.auth.refresh_access_token = AsyncMock()
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "user_id": 12345,
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
        
        with patch.object(client, "_request", return_value=mock_response):
            await client.get_profile_basic()
            
            client.auth.refresh_access_token.assert_called_once_with(
                client.auth.refresh_token
            )
    
    @pytest.mark.asyncio
    async def test_no_access_token_error(self, client):
        """Test error when no access token is available."""
        client.auth.access_token = None
        
        with pytest.raises(ValueError, match="No access token available"):
            await client.get_profile_basic()
    
    @pytest.mark.asyncio
    async def test_date_filtering(self, client):
        """Test date filtering in collection endpoints."""
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 31)
        
        mock_response = Mock()
        mock_response.json.return_value = {"records": [], "next_token": None}
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            await client.get_cycle_collection(start=start_date, end=end_date)
            
            mock_request.assert_called_once_with(
                "GET",
                "/v2/cycle",
                params={
                    "limit": 10,
                    "start": "2023-01-01T00:00:00",
                    "end": "2023-01-31T00:00:00",
                },
            )


class TestOAuth2Handler:
    """Test OAuth2 handler."""
    
    def test_get_authorization_url(self):
        """Test generating authorization URL."""
        handler = OAuth2Handler(
            client_id="test_client",
            client_secret="test_secret",
            redirect_uri="http://localhost:8000/callback",
            scopes=["read:profile", "read:sleep"],
        )
        
        url = handler.get_authorization_url(state="test_state")
        
        assert "https://api.prod.whoop.com/oauth/oauth2/auth" in url
        assert "client_id=test_client" in url
        assert "redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback" in url
        assert "scope=read%3Aprofile+read%3Asleep" in url
        assert "state=test_state" in url
    
    @pytest.mark.asyncio
    async def test_exchange_code(self):
        """Test exchanging authorization code for tokens."""
        handler = OAuth2Handler(
            client_id="test_client",
            client_secret="test_secret",
            redirect_uri="http://localhost:8000/callback",
        )
        
        mock_response = {
            "access_token": "new_access_token",
            "token_type": "bearer",
            "expires_in": 3600,
            "refresh_token": "new_refresh_token",
            "scope": "read:profile",
        }
        
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = Mock()
            
            token_response = await handler.exchange_code("auth_code_123")
            
            assert isinstance(token_response, TokenResponse)
            assert token_response.access_token == "new_access_token"
            assert handler.access_token == "new_access_token"
            assert not handler.is_token_expired()
    
    def test_token_expiry(self):
        """Test token expiry calculation."""
        handler = OAuth2Handler(
            client_id="test_client",
            client_secret="test_secret",
            redirect_uri="http://localhost:8000/callback",
        )
        
        # No token set
        assert handler.is_token_expired()
        
        # Set token with 1 hour expiry
        handler.set_tokens("access_token", "refresh_token", expires_in=3600)
        assert not handler.is_token_expired()
        
        # Set token with 0 expiry (should be expired due to 5-minute buffer)
        handler.set_tokens("access_token", "refresh_token", expires_in=0)
        assert handler.is_token_expired()