"""Recovery-related models for the WHOOP API."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .common import PaginatedResponse, ScoreState


class RecoveryScore(BaseModel):
    """WHOOP's measurements and evaluation of recovery.
    
    Attributes:
        user_calibrating: True if user is still calibrating and not enough data is available.
        recovery_score: Percentage (0-100%) reflecting body's readiness for strain.
        resting_heart_rate: User's resting heart rate in beats per minute.
        hrv_rmssd_milli: Heart Rate Variability (RMSSD) in milliseconds.
        spo2_percentage: Blood oxygen percentage (only for 4.0+ devices).
        skin_temp_celsius: Skin temperature in Celsius (only for 4.0+ devices).
    """
    user_calibrating: bool = Field(
        ...,
        description="True if the user is still calibrating",
        example=False
    )
    recovery_score: float = Field(
        ...,
        description="Percentage (0-100%) that reflects body's readiness for strain",
        example=44.0
    )
    resting_heart_rate: float = Field(
        ...,
        description="The user's resting heart rate",
        example=64.0
    )
    hrv_rmssd_milli: float = Field(
        ...,
        description="Heart Rate Variability (RMSSD) in milliseconds",
        example=31.813562
    )
    spo2_percentage: Optional[float] = Field(
        None,
        description="Percentage of oxygen in the user's blood (4.0+ only)",
        example=95.6875
    )
    skin_temp_celsius: Optional[float] = Field(
        None,
        description="The user's skin temperature in Celsius (4.0+ only)",
        example=33.7
    )


class Recovery(BaseModel):
    """Represents a recovery measurement in WHOOP.
    
    Attributes:
        cycle_id: The physiological cycle ID this recovery is associated with.
        sleep_id: ID of the Sleep associated with the Recovery.
        user_id: The WHOOP User for the recovery.
        created_at: When the recovery was recorded in WHOOP.
        updated_at: When the recovery was last updated in WHOOP.
        score_state: Current state of score calculation for this recovery.
        score: Measurements and evaluation of the recovery. Only present if score_state is SCORED.
    """
    cycle_id: int = Field(
        ...,
        description="The Recovery represents how recovered the user is for this cycle",
        example=93845
    )
    sleep_id: UUID = Field(
        ...,
        description="ID of the Sleep associated with the Recovery",
        example="123e4567-e89b-12d3-a456-426614174000"
    )
    user_id: int = Field(
        ...,
        description="The WHOOP User for the recovery",
        example=10129
    )
    created_at: datetime = Field(
        ...,
        description="The time the recovery was recorded in WHOOP",
        example="2022-04-24T11:25:44.774Z"
    )
    updated_at: datetime = Field(
        ...,
        description="The time the recovery was last updated in WHOOP",
        example="2022-04-24T14:25:44.774Z"
    )
    score_state: ScoreState = Field(
        ...,
        description="Current state of score calculation",
        example="SCORED"
    )
    score: Optional[RecoveryScore] = Field(
        None,
        description="WHOOP's measurements and evaluation of the recovery. Only present if score_state is SCORED"
    )


class RecoveryCollection(PaginatedResponse):
    """Paginated response containing recovery activities.
    
    Attributes:
        records: List of recovery activities in this page.
        next_token: Token for accessing the next page of records.
    """
    records: List[Recovery] = Field(
        default_factory=list,
        description="The collection of records in this page."
    )