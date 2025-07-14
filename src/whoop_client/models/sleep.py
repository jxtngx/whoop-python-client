"""Sleep-related models for the WHOOP API."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .common import PaginatedResponse, ScoreState


class SleepStageSummary(BaseModel):
    """Summary of sleep stages during a sleep activity.
    
    Attributes:
        total_in_bed_time_milli: Total time spent in bed in milliseconds.
        total_awake_time_milli: Total time spent awake in milliseconds.
        total_no_data_time_milli: Total time with no data received in milliseconds.
        total_light_sleep_time_milli: Total time in light sleep in milliseconds.
        total_slow_wave_sleep_time_milli: Total time in Slow Wave Sleep (SWS) in milliseconds.
        total_rem_sleep_time_milli: Total time in Rapid Eye Movement (REM) sleep in milliseconds.
        sleep_cycle_count: Number of sleep cycles during the sleep.
        disturbance_count: Number of times the user was disturbed during sleep.
    """
    total_in_bed_time_milli: int = Field(
        ...,
        description="Total time the user spent in bed, in milliseconds",
        example=30272735
    )
    total_awake_time_milli: int = Field(
        ...,
        description="Total time the user spent awake, in milliseconds",
        example=1403507
    )
    total_no_data_time_milli: int = Field(
        ...,
        description="Total time WHOOP did not receive data from the user during the sleep, in milliseconds",
        example=0
    )
    total_light_sleep_time_milli: int = Field(
        ...,
        description="Total time the user spent in light sleep, in milliseconds",
        example=14905851
    )
    total_slow_wave_sleep_time_milli: int = Field(
        ...,
        description="Total time the user spent in Slow Wave Sleep (SWS), in milliseconds",
        example=6630370
    )
    total_rem_sleep_time_milli: int = Field(
        ...,
        description="Total time the user spent in Rapid Eye Movement (REM) sleep, in milliseconds",
        example=5879573
    )
    sleep_cycle_count: int = Field(
        ...,
        description="Number of sleep cycles during the user's sleep",
        example=3
    )
    disturbance_count: int = Field(
        ...,
        description="Number of times the user was disturbed during sleep",
        example=12
    )


class SleepNeeded(BaseModel):
    """Breakdown of sleep need calculation.
    
    Attributes:
        baseline_milli: Sleep needed based on historical trends in milliseconds.
        need_from_sleep_debt_milli: Additional sleep needed due to sleep debt in milliseconds.
        need_from_recent_strain_milli: Additional sleep needed due to recent strain in milliseconds.
        need_from_recent_nap_milli: Reduction in sleep need from recent naps (negative or zero) in milliseconds.
    """
    baseline_milli: int = Field(
        ...,
        description="The amount of sleep a user needed based on historical trends",
        example=27395716
    )
    need_from_sleep_debt_milli: int = Field(
        ...,
        description="The difference between required sleep and actual sleep",
        example=352230
    )
    need_from_recent_strain_milli: int = Field(
        ...,
        description="Additional sleep need accrued based on the user's strain",
        example=208595
    )
    need_from_recent_nap_milli: int = Field(
        ...,
        description="Reduction in sleep need from recent nap activity (negative value or zero)",
        example=-12312
    )


class SleepScore(BaseModel):
    """WHOOP's measurements and evaluation of a sleep activity.
    
    Attributes:
        stage_summary: Summary of time spent in each sleep stage.
        sleep_needed: Breakdown of sleep need calculation.
        respiratory_rate: Respiratory rate during sleep in breaths per minute.
        sleep_performance_percentage: Percentage of sleep achieved vs sleep needed (0-100%).
        sleep_consistency_percentage: Sleep/wake time consistency vs previous day (0-100%).
        sleep_efficiency_percentage: Percentage of time in bed actually sleeping (0-100%).
    """
    stage_summary: SleepStageSummary = Field(
        ...,
        description="Summary of the sleep stages"
    )
    sleep_needed: SleepNeeded = Field(
        ...,
        description="Breakdown of the amount of sleep needed"
    )
    respiratory_rate: Optional[float] = Field(
        None,
        description="The user's respiratory rate during the sleep",
        example=16.11328125
    )
    sleep_performance_percentage: Optional[float] = Field(
        None,
        description="Percentage (0-100%) of time asleep over sleep needed",
        example=98.0
    )
    sleep_consistency_percentage: Optional[float] = Field(
        None,
        description="Percentage (0-100%) of sleep/wake time consistency vs previous day",
        example=90.0
    )
    sleep_efficiency_percentage: Optional[float] = Field(
        None,
        description="Percentage (0-100%) of time in bed actually sleeping",
        example=91.69533848
    )


class Sleep(BaseModel):
    """Represents a sleep activity in WHOOP.
    
    Attributes:
        id: Unique identifier for the sleep activity.
        v1_id: Previous generation identifier (deprecated after 09/01/2025).
        user_id: The WHOOP User who performed the sleep activity.
        created_at: When the sleep activity was recorded in WHOOP.
        updated_at: When the sleep activity was last updated in WHOOP.
        start: Start time of the sleep.
        end: End time of the sleep.
        timezone_offset: User's timezone offset when the sleep was recorded (format: ±hh:mm or Z).
        nap: Whether this sleep activity was a nap.
        score_state: Current state of score calculation for this sleep.
        score: Measurements and evaluation of the sleep. Only present if score_state is SCORED.
    """
    id: UUID = Field(
        ...,
        description="Unique identifier for the sleep activity",
        example="ecfc6a15-4661-442f-a9a4-f160dd7afae8"
    )
    v1_id: Optional[int] = Field(
        None,
        description="Previous generation identifier. Will not exist past 09/01/2025",
        example=93845
    )
    user_id: int = Field(
        ...,
        description="The WHOOP User who performed the sleep activity",
        example=10129
    )
    created_at: datetime = Field(
        ...,
        description="The time the sleep activity was recorded in WHOOP",
        example="2022-04-24T11:25:44.774Z"
    )
    updated_at: datetime = Field(
        ...,
        description="The time the sleep activity was last updated in WHOOP",
        example="2022-04-24T14:25:44.774Z"
    )
    start: datetime = Field(
        ...,
        description="Start time bound of the sleep",
        example="2022-04-24T02:25:44.774Z"
    )
    end: datetime = Field(
        ...,
        description="End time bound of the sleep",
        example="2022-04-24T10:25:44.774Z"
    )
    timezone_offset: str = Field(
        ...,
        description="The user's timezone offset at the time the sleep was recorded. Format: '+hh:mm', '-hh:mm', or 'Z'",
        example="-05:00"
    )
    nap: bool = Field(
        ...,
        description="If true, this sleep activity was a nap for the user",
        example=False
    )
    score_state: ScoreState = Field(
        ...,
        description="Current state of score calculation",
        example="SCORED"
    )
    score: Optional[SleepScore] = Field(
        None,
        description="WHOOP's measurements and evaluation of the sleep. Only present if score_state is SCORED"
    )


class PaginatedSleepResponse(PaginatedResponse):
    """Paginated response containing sleep activities.
    
    Attributes:
        records: List of sleep activities in this page.
        next_token: Token for accessing the next page of records.
    """
    records: List[Sleep] = Field(
        default_factory=list,
        description="The collection of records in this page."
    )