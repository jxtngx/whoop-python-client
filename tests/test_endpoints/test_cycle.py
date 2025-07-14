"""Tests for cycle endpoints."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from whoop_client import WhoopClient
from whoop_client.models import Cycle, PaginatedCycleResponse, ScoreState, Sleep


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


class TestCycleEndpoints:
    """Test cycle-specific endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_cycle_by_id_success(self, client):
        """Test successful retrieval of a cycle by ID."""
        cycle_data = {
            "id": 93845,
            "user_id": 10129,
            "created_at": "2022-04-24T11:25:44.774Z",
            "updated_at": "2022-04-24T14:25:44.774Z",
            "start": "2022-04-24T02:25:44.774Z",
            "end": "2022-04-24T10:25:44.774Z",
            "timezone_offset": "-05:00",
            "score_state": "SCORED",
            "score": {
                "strain": 5.2951527,
                "kilojoule": 8288.297,
                "average_heart_rate": 68,
                "max_heart_rate": 141,
            },
        }
        
        mock_response = Mock()
        mock_response.json.return_value = cycle_data
        
        with patch.object(client, "_request", return_value=mock_response):
            cycle = await client.get_cycle_by_id(93845)
            
            assert isinstance(cycle, Cycle)
            assert cycle.id == 93845
            assert cycle.user_id == 10129
            assert cycle.score_state == ScoreState.SCORED
            assert cycle.score.strain == 5.2951527
    
    @pytest.mark.asyncio
    async def test_get_cycle_collection_with_filters(self, client):
        """Test retrieving cycle collection with date filters."""
        collection_data = {
            "records": [
                {
                    "id": 93845,
                    "user_id": 10129,
                    "created_at": "2022-04-24T11:25:44.774Z",
                    "updated_at": "2022-04-24T14:25:44.774Z",
                    "start": "2022-04-24T02:25:44.774Z",
                    "timezone_offset": "-05:00",
                    "score_state": "PENDING_SCORE",
                },
                {
                    "id": 93846,
                    "user_id": 10129,
                    "created_at": "2022-04-25T11:25:44.774Z",
                    "updated_at": "2022-04-25T14:25:44.774Z",
                    "start": "2022-04-25T02:25:44.774Z",
                    "end": "2022-04-25T10:25:44.774Z",
                    "timezone_offset": "-05:00",
                    "score_state": "SCORED",
                    "score": {
                        "strain": 7.5,
                        "kilojoule": 9500.0,
                        "average_heart_rate": 75,
                        "max_heart_rate": 155,
                    },
                },
            ],
            "next_token": "next_page_token",
        }
        
        mock_response = Mock()
        mock_response.json.return_value = collection_data
        
        start_date = datetime(2022, 4, 24)
        end_date = datetime(2022, 4, 26)
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            response = await client.get_cycle_collection(
                limit=20, start=start_date, end=end_date
            )
            
            mock_request.assert_called_once_with(
                "GET",
                "/v2/cycle",
                params={
                    "limit": 20,
                    "start": "2022-04-24T00:00:00",
                    "end": "2022-04-26T00:00:00",
                },
            )
            
            assert isinstance(response, PaginatedCycleResponse)
            assert len(response.records) == 2
            assert response.next_token == "next_page_token"
            assert response.records[0].score_state == ScoreState.PENDING_SCORE
            assert response.records[0].score is None
            assert response.records[1].score.strain == 7.5
    
    @pytest.mark.asyncio
    async def test_get_sleep_for_cycle(self, client):
        """Test retrieving sleep for a specific cycle."""
        sleep_data = {
            "id": "ecfc6a15-4661-442f-a9a4-f160dd7afae8",
            "user_id": 10129,
            "created_at": "2022-04-24T11:25:44.774Z",
            "updated_at": "2022-04-24T14:25:44.774Z",
            "start": "2022-04-24T02:25:44.774Z",
            "end": "2022-04-24T10:25:44.774Z",
            "timezone_offset": "-05:00",
            "nap": False,
            "score_state": "SCORED",
            "score": {
                "stage_summary": {
                    "total_in_bed_time_milli": 30272735,
                    "total_awake_time_milli": 1403507,
                    "total_no_data_time_milli": 0,
                    "total_light_sleep_time_milli": 14905851,
                    "total_slow_wave_sleep_time_milli": 6630370,
                    "total_rem_sleep_time_milli": 5879573,
                    "sleep_cycle_count": 3,
                    "disturbance_count": 12,
                },
                "sleep_needed": {
                    "baseline_milli": 27395716,
                    "need_from_sleep_debt_milli": 352230,
                    "need_from_recent_strain_milli": 208595,
                    "need_from_recent_nap_milli": -12312,
                },
                "respiratory_rate": 16.11328125,
                "sleep_performance_percentage": 98.0,
                "sleep_consistency_percentage": 90.0,
                "sleep_efficiency_percentage": 91.69533848,
            },
        }
        
        mock_response = Mock()
        mock_response.json.return_value = sleep_data
        
        with patch.object(client, "_request", return_value=mock_response) as mock_request:
            sleep = await client.get_sleep_for_cycle(93845)
            
            mock_request.assert_called_once_with("GET", "/v2/cycle/93845/sleep")
            
            assert isinstance(sleep, Sleep)
            assert str(sleep.id) == "ecfc6a15-4661-442f-a9a4-f160dd7afae8"
            assert sleep.nap is False
            assert sleep.score.sleep_performance_percentage == 98.0
            assert sleep.score.stage_summary.sleep_cycle_count == 3
    
    @pytest.mark.asyncio
    async def test_iterate_cycles_pagination(self, client):
        """Test iterating through all cycles with automatic pagination."""
        # First page
        page1_data = {
            "records": [
                {
                    "id": 1,
                    "user_id": 100,
                    "created_at": "2023-01-01T10:00:00Z",
                    "updated_at": "2023-01-01T11:00:00Z",
                    "start": "2023-01-01T00:00:00Z",
                    "timezone_offset": "-05:00",
                    "score_state": "SCORED",
                },
                {
                    "id": 2,
                    "user_id": 100,
                    "created_at": "2023-01-02T10:00:00Z",
                    "updated_at": "2023-01-02T11:00:00Z",
                    "start": "2023-01-02T00:00:00Z",
                    "timezone_offset": "-05:00",
                    "score_state": "SCORED",
                },
            ],
            "next_token": "page2_token",
        }
        
        # Second page
        page2_data = {
            "records": [
                {
                    "id": 3,
                    "user_id": 100,
                    "created_at": "2023-01-03T10:00:00Z",
                    "updated_at": "2023-01-03T11:00:00Z",
                    "start": "2023-01-03T00:00:00Z",
                    "timezone_offset": "-05:00",
                    "score_state": "SCORED",
                },
            ],
            "next_token": None,
        }
        
        mock_response1 = Mock()
        mock_response1.json.return_value = page1_data
        
        mock_response2 = Mock()
        mock_response2.json.return_value = page2_data
        
        with patch.object(
            client, "_request", side_effect=[mock_response1, mock_response2]
        ) as mock_request:
            cycles = []
            async for cycle in client.iterate_cycles(page_size=2):
                cycles.append(cycle)
            
            # Verify two requests were made
            assert mock_request.call_count == 2
            
            # First request
            mock_request.assert_any_call(
                "GET", "/v2/cycle", params={"limit": 2}
            )
            
            # Second request with next token
            mock_request.assert_any_call(
                "GET", "/v2/cycle", params={"limit": 2, "nextToken": "page2_token"}
            )
            
            # Verify all cycles were collected
            assert len(cycles) == 3
            assert cycles[0].id == 1
            assert cycles[1].id == 2
            assert cycles[2].id == 3