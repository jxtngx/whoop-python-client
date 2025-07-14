"""Cycle-related models for the WHOOP API."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .common import PaginatedResponse, ScoreState


class CycleScore(BaseModel):
    """WHOOP's measurements and evaluation of a physiological cycle.
    
    Attributes:
        strain: Cardiovascular load (0-21 scale) based on heart rate during the cycle.
        kilojoule: Energy expended during the cycle in kilojoules.
        average_heart_rate: Average heart rate in beats per minute during the cycle.
        max_heart_rate: Maximum heart rate in beats per minute during the cycle.
    """
    strain: float = Field(
        ...,
        description="WHOOP metric of cardiovascular load on a scale from 0 to 21.",
        example=5.2951527
    )
    kilojoule: float = Field(
        ...,
        description="Kilojoules the user expended during the cycle.",
        example=8288.297
    )
    average_heart_rate: int = Field(
        ...,
        description="The user's average heart rate during the cycle.",
        example=68
    )
    max_heart_rate: int = Field(
        ...,
        description="The user's max heart rate during the cycle.",
        example=141
    )


class Cycle(BaseModel):
    """Represents a physiological cycle in WHOOP.
    
    Attributes:
        id: Unique identifier for the physiological cycle.
        user_id: The WHOOP User ID for the physiological cycle.
        created_at: When the cycle was recorded in WHOOP.
        updated_at: When the cycle was last updated in WHOOP.
        start: Start time of the cycle.
        end: End time of the cycle. If not present, the user is currently in this cycle.
        timezone_offset: User's timezone offset when the cycle was recorded (format: ±hh:mm or Z).
        score_state: Current state of score calculation for this cycle.
        score: Measurements and evaluation of the cycle. Only present if score_state is SCORED.
    """
    id: int = Field(..., description="Unique identifier for the physiological cycle", example=93845)
    user_id: int = Field(..., description="The WHOOP User for the physiological cycle", example=10129)
    created_at: datetime = Field(
        ...,
        description="The time the cycle was recorded in WHOOP",
        example="2022-04-24T11:25:44.774Z"
    )
    updated_at: datetime = Field(
        ...,
        description="The time the cycle was last updated in WHOOP",
        example="2022-04-24T14:25:44.774Z"
    )
    start: datetime = Field(
        ...,
        description="Start time bound of the cycle",
        example="2022-04-24T02:25:44.774Z"
    )
    end: Optional[datetime] = Field(
        None,
        description="End time bound of the cycle. If not present, the user is currently in this cycle",
        example="2022-04-24T10:25:44.774Z"
    )
    timezone_offset: str = Field(
        ...,
        description="The user's timezone offset at the time the cycle was recorded. Format: '+hh:mm', '-hh:mm', or 'Z'",
        example="-05:00"
    )
    score_state: ScoreState = Field(
        ...,
        description="Current state of score calculation",
        example="SCORED"
    )
    score: Optional[CycleScore] = Field(
        None,
        description="WHOOP's measurements and evaluation of the cycle. Only present if score_state is SCORED"
    )


class PaginatedCycleResponse(PaginatedResponse):
    """Paginated response containing physiological cycles.
    
    Attributes:
        records: List of cycles in this page.
        next_token: Token for accessing the next page of records.
    """
    records: List[Cycle] = Field(
        default_factory=list,
        description="The collection of records in this page."
    )