"""Tests for WHOOP API models."""

from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from whoop_client.models import (
    Cycle,
    CycleScore,
    PaginatedCycleResponse,
    Recovery,
    RecoveryScore,
    ScoreState,
    Sleep,
    SleepScore,
    SleepStageSummary,
    UserBasicProfile,
    UserBodyMeasurement,
    WorkoutScore,
    WorkoutV2,
    ZoneDurations,
)


class TestCycleModels:
    """Test cycle-related models."""
    
    def test_cycle_score_creation(self):
        """Test CycleScore model creation."""
        score = CycleScore(
            strain=5.5,
            kilojoule=8000.0,
            average_heart_rate=70,
            max_heart_rate=140,
        )
        assert score.strain == 5.5
        assert score.kilojoule == 8000.0
        assert score.average_heart_rate == 70
        assert score.max_heart_rate == 140
    
    def test_cycle_creation(self):
        """Test Cycle model creation."""
        cycle = Cycle(
            id=12345,
            user_id=67890,
            created_at="2023-01-01T10:00:00Z",
            updated_at="2023-01-01T11:00:00Z",
            start="2023-01-01T00:00:00Z",
            end="2023-01-01T23:59:59Z",
            timezone_offset="-05:00",
            score_state=ScoreState.SCORED,
            score=CycleScore(
                strain=5.5,
                kilojoule=8000.0,
                average_heart_rate=70,
                max_heart_rate=140,
            ),
        )
        assert cycle.id == 12345
        assert cycle.user_id == 67890
        assert cycle.score_state == ScoreState.SCORED
        assert cycle.score.strain == 5.5
    
    def test_cycle_without_end(self):
        """Test Cycle model without end time (current cycle)."""
        cycle = Cycle(
            id=12345,
            user_id=67890,
            created_at="2023-01-01T10:00:00Z",
            updated_at="2023-01-01T11:00:00Z",
            start="2023-01-01T00:00:00Z",
            timezone_offset="-05:00",
            score_state=ScoreState.PENDING_SCORE,
        )
        assert cycle.end is None
        assert cycle.score is None
    
    def test_paginated_cycle_response(self):
        """Test PaginatedCycleResponse model."""
        response = PaginatedCycleResponse(
            records=[],
            next_token="token123",
        )
        assert response.records == []
        assert response.next_token == "token123"


class TestSleepModels:
    """Test sleep-related models."""
    
    def test_sleep_stage_summary(self):
        """Test SleepStageSummary model creation."""
        summary = SleepStageSummary(
            total_in_bed_time_milli=30000000,
            total_awake_time_milli=1500000,
            total_no_data_time_milli=0,
            total_light_sleep_time_milli=15000000,
            total_slow_wave_sleep_time_milli=6000000,
            total_rem_sleep_time_milli=7500000,
            sleep_cycle_count=4,
            disturbance_count=10,
        )
        assert summary.total_in_bed_time_milli == 30000000
        assert summary.sleep_cycle_count == 4
    
    def test_sleep_creation(self):
        """Test Sleep model creation."""
        sleep = Sleep(
            id="550e8400-e29b-41d4-a716-446655440000",
            user_id=12345,
            created_at="2023-01-01T10:00:00Z",
            updated_at="2023-01-01T11:00:00Z",
            start="2023-01-01T00:00:00Z",
            end="2023-01-01T08:00:00Z",
            timezone_offset="-05:00",
            nap=False,
            score_state=ScoreState.SCORED,
        )
        assert isinstance(sleep.id, UUID)
        assert sleep.nap is False
        assert sleep.score_state == ScoreState.SCORED


class TestRecoveryModels:
    """Test recovery-related models."""
    
    def test_recovery_score_creation(self):
        """Test RecoveryScore model creation."""
        score = RecoveryScore(
            user_calibrating=False,
            recovery_score=65.0,
            resting_heart_rate=55.0,
            hrv_rmssd_milli=45.5,
            spo2_percentage=96.5,
            skin_temp_celsius=34.2,
        )
        assert score.recovery_score == 65.0
        assert score.spo2_percentage == 96.5
    
    def test_recovery_creation(self):
        """Test Recovery model creation."""
        recovery = Recovery(
            cycle_id=12345,
            sleep_id="550e8400-e29b-41d4-a716-446655440000",
            user_id=67890,
            created_at="2023-01-01T10:00:00Z",
            updated_at="2023-01-01T11:00:00Z",
            score_state=ScoreState.SCORED,
        )
        assert recovery.cycle_id == 12345
        assert isinstance(recovery.sleep_id, UUID)


class TestUserModels:
    """Test user-related models."""
    
    def test_user_basic_profile(self):
        """Test UserBasicProfile model creation."""
        profile = UserBasicProfile(
            user_id=12345,
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        assert profile.user_id == 12345
        assert profile.email == "test@example.com"
    
    def test_user_body_measurement(self):
        """Test UserBodyMeasurement model creation."""
        measurement = UserBodyMeasurement(
            height_meter=1.80,
            weight_kilogram=75.5,
            max_heart_rate=190,
        )
        assert measurement.height_meter == 1.80
        assert measurement.weight_kilogram == 75.5


class TestWorkoutModels:
    """Test workout-related models."""
    
    def test_zone_durations(self):
        """Test ZoneDurations model creation."""
        zones = ZoneDurations(
            zone_zero_milli=300000,
            zone_one_milli=600000,
            zone_two_milli=900000,
            zone_three_milli=900000,
            zone_four_milli=600000,
            zone_five_milli=300000,
        )
        assert zones.zone_zero_milli == 300000
        assert zones.zone_five_milli == 300000
    
    def test_workout_score_creation(self):
        """Test WorkoutScore model creation."""
        score = WorkoutScore(
            strain=8.5,
            average_heart_rate=130,
            max_heart_rate=165,
            kilojoule=1500.0,
            percent_recorded=98.5,
            distance_meter=5000.0,
            zone_durations=ZoneDurations(
                zone_zero_milli=300000,
                zone_one_milli=600000,
                zone_two_milli=900000,
                zone_three_milli=900000,
                zone_four_milli=600000,
                zone_five_milli=300000,
            ),
        )
        assert score.strain == 8.5
        assert score.distance_meter == 5000.0
    
    def test_workout_creation(self):
        """Test WorkoutV2 model creation."""
        workout = WorkoutV2(
            id="550e8400-e29b-41d4-a716-446655440000",
            user_id=12345,
            created_at="2023-01-01T10:00:00Z",
            updated_at="2023-01-01T11:00:00Z",
            start="2023-01-01T06:00:00Z",
            end="2023-01-01T07:00:00Z",
            timezone_offset="-05:00",
            sport_name="running",
            score_state=ScoreState.SCORED,
        )
        assert workout.sport_name == "running"
        assert workout.score_state == ScoreState.SCORED


class TestValidation:
    """Test model validation."""
    
    def test_invalid_score_state(self):
        """Test invalid score state raises validation error."""
        with pytest.raises(ValidationError):
            Cycle(
                id=12345,
                user_id=67890,
                created_at="2023-01-01T10:00:00Z",
                updated_at="2023-01-01T11:00:00Z",
                start="2023-01-01T00:00:00Z",
                timezone_offset="-05:00",
                score_state="INVALID_STATE",  # Invalid enum value
            )
    
    def test_invalid_email(self):
        """Test invalid email raises validation error."""
        with pytest.raises(ValidationError):
            UserBasicProfile(
                user_id=12345,
                email="not-an-email",  # Invalid email format
                first_name="John",
                last_name="Doe",
            )
    
    def test_missing_required_field(self):
        """Test missing required field raises validation error."""
        with pytest.raises(ValidationError):
            CycleScore(
                strain=5.5,
                # Missing kilojoule, average_heart_rate, max_heart_rate
            )