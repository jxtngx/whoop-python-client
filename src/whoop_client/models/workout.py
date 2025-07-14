"""Workout-related models for the WHOOP API."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .common import PaginatedResponse, ScoreState


class ZoneDurations(BaseModel):
    """Breakdown of time spent in each heart rate zone during a workout.
    
    Attributes:
        zone_zero_milli: Time in Zone 0 (very light activity) in milliseconds.
        zone_one_milli: Time in Zone 1 (light activity) in milliseconds.
        zone_two_milli: Time in Zone 2 (moderate activity) in milliseconds.
        zone_three_milli: Time in Zone 3 (hard activity) in milliseconds.
        zone_four_milli: Time in Zone 4 (very hard activity) in milliseconds.
        zone_five_milli: Time in Zone 5 (maximum effort) in milliseconds.
    """
    zone_zero_milli: int = Field(
        ...,
        description="Duration in milliseconds spent in Zone 0 (very light activity)",
        example=300000
    )
    zone_one_milli: int = Field(
        ...,
        description="Duration in milliseconds spent in Zone 1 (light activity)",
        example=600000
    )
    zone_two_milli: int = Field(
        ...,
        description="Duration in milliseconds spent in Zone 2 (moderate activity)",
        example=900000
    )
    zone_three_milli: int = Field(
        ...,
        description="Duration in milliseconds spent in Zone 3 (hard activity)",
        example=900000
    )
    zone_four_milli: int = Field(
        ...,
        description="Duration in milliseconds spent in Zone 4 (very hard activity)",
        example=600000
    )
    zone_five_milli: int = Field(
        ...,
        description="Duration in milliseconds spent in Zone 5 (maximum effort)",
        example=300000
    )


class WorkoutScore(BaseModel):
    """WHOOP's measurements and evaluation of a workout activity.
    
    Attributes:
        strain: Cardiovascular load (0-21 scale) based on heart rate during the workout.
        average_heart_rate: Average heart rate in beats per minute during the workout.
        max_heart_rate: Maximum heart rate in beats per minute during the workout.
        kilojoule: Energy expended during the workout in kilojoules.
        percent_recorded: Percentage (0-100%) of heart rate data received during the workout.
        distance_meter: Distance traveled in meters (optional, if distance data available).
        altitude_gain_meter: Total altitude climbed in meters (optional, if altitude data available).
        altitude_change_meter: Net altitude change in meters (optional, if altitude data available).
        zone_durations: Time spent in each heart rate zone.
    """
    strain: float = Field(
        ...,
        description="WHOOP metric of cardiovascular load on a scale from 0 to 21",
        example=8.2463
    )
    average_heart_rate: int = Field(
        ...,
        description="The user's average heart rate (bpm) during the workout",
        example=123
    )
    max_heart_rate: int = Field(
        ...,
        description="The user's max heart rate (bpm) during the workout",
        example=146
    )
    kilojoule: float = Field(
        ...,
        description="Kilojoules the user expended during the workout",
        example=1569.34033203125
    )
    percent_recorded: float = Field(
        ...,
        description="Percentage (0-100%) of heart rate data WHOOP received",
        example=100.0
    )
    distance_meter: Optional[float] = Field(
        None,
        description="The distance the user travelled during the workout",
        example=1772.77035916
    )
    altitude_gain_meter: Optional[float] = Field(
        None,
        description="The altitude gained during the workout (upward travel only)",
        example=46.64384460449
    )
    altitude_change_meter: Optional[float] = Field(
        None,
        description="The altitude difference between start and end points",
        example=-0.781372010707855
    )
    zone_durations: ZoneDurations = Field(
        ...,
        description="Breakdown of time spent in each heart rate zone"
    )


class WorkoutV2(BaseModel):
    """Represents a workout activity in WHOOP.
    
    Attributes:
        id: Unique identifier for the workout activity.
        v1_id: Previous generation identifier (deprecated after 09/01/2025).
        user_id: The WHOOP User who performed the workout.
        created_at: When the workout activity was recorded in WHOOP.
        updated_at: When the workout activity was last updated in WHOOP.
        start: Start time of the workout.
        end: End time of the workout.
        timezone_offset: User's timezone offset when the workout was recorded (format: ±hh:mm or Z).
        sport_name: Name of the WHOOP Sport performed during the workout.
        sport_id: ID of the WHOOP Sport performed (deprecated after 09/01/2025).
        score_state: Current state of score calculation for this workout.
        score: Measurements and evaluation of the workout. Only present if score_state is SCORED.
    """
    id: UUID = Field(
        ...,
        description="Unique identifier for the workout activity",
        example="ecfc6a15-4661-442f-a9a4-f160dd7afae8"
    )
    v1_id: Optional[int] = Field(
        None,
        description="Previous generation identifier. Will not exist past 09/01/2025",
        example=1043
    )
    user_id: int = Field(
        ...,
        description="The WHOOP User who performed the workout",
        example=9012
    )
    created_at: datetime = Field(
        ...,
        description="The time the workout activity was recorded in WHOOP",
        example="2022-04-24T11:25:44.774Z"
    )
    updated_at: datetime = Field(
        ...,
        description="The time the workout activity was last updated in WHOOP",
        example="2022-04-24T14:25:44.774Z"
    )
    start: datetime = Field(
        ...,
        description="Start time bound of the workout",
        example="2022-04-24T02:25:44.774Z"
    )
    end: datetime = Field(
        ...,
        description="End time bound of the workout",
        example="2022-04-24T10:25:44.774Z"
    )
    timezone_offset: str = Field(
        ...,
        description="The user's timezone offset at the time the workout was recorded. Format: '+hh:mm', '-hh:mm', or 'Z'",
        example="-05:00"
    )
    sport_name: str = Field(
        ...,
        description="Name of the WHOOP Sport performed during the workout",
        example="running"
    )
    sport_id: Optional[int] = Field(
        None,
        description="ID of the WHOOP Sport performed. Will not exist past 09/01/2025",
        example=1
    )
    score_state: ScoreState = Field(
        ...,
        description="Current state of score calculation",
        example="SCORED"
    )
    score: Optional[WorkoutScore] = Field(
        None,
        description="WHOOP's measurements and evaluation of the workout. Only present if score_state is SCORED"
    )


class WorkoutCollection(PaginatedResponse):
    """Paginated response containing workout activities.
    
    Attributes:
        records: List of workout activities in this page.
        next_token: Token for accessing the next page of records.
    """
    records: List[WorkoutV2] = Field(
        default_factory=list,
        description="The collection of records in this page."
    )