"""Common models shared across different WHOOP API endpoints."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ScoreState(str, Enum):
    """State of score calculation.
    
    Attributes:
        SCORED: The activity was scored and measurement values are present.
        PENDING_SCORE: WHOOP is currently evaluating the activity.
        UNSCORABLE: The activity could not be scored, commonly due to insufficient metric data.
    """
    SCORED = "SCORED"
    PENDING_SCORE = "PENDING_SCORE"
    UNSCORABLE = "UNSCORABLE"


class PaginatedResponse(BaseModel):
    """Base model for paginated API responses.
    
    Attributes:
        next_token: Token for accessing the next page of records. If not present, no more records exist.
    """
    next_token: Optional[str] = Field(
        None,
        description="A token that can be used on the next request to access the next page of records."
    )