"""WHOOP API models."""

from .common import PaginatedResponse, ScoreState
from .cycle import Cycle, CycleScore, PaginatedCycleResponse
from .recovery import Recovery, RecoveryCollection, RecoveryScore
from .sleep import (
    PaginatedSleepResponse,
    Sleep,
    SleepNeeded,
    SleepScore,
    SleepStageSummary,
)
from .user import UserBasicProfile, UserBodyMeasurement
from .workout import (
    WorkoutCollection,
    WorkoutScore,
    WorkoutV2,
    ZoneDurations,
)

__all__ = [
    # Common
    "ScoreState",
    "PaginatedResponse",
    # Cycle
    "Cycle",
    "CycleScore",
    "PaginatedCycleResponse",
    # Sleep
    "Sleep",
    "SleepScore",
    "SleepStageSummary",
    "SleepNeeded",
    "PaginatedSleepResponse",
    # Recovery
    "Recovery",
    "RecoveryScore",
    "RecoveryCollection",
    # User
    "UserBasicProfile",
    "UserBodyMeasurement",
    # Workout
    "WorkoutV2",
    "WorkoutScore",
    "ZoneDurations",
    "WorkoutCollection",
]