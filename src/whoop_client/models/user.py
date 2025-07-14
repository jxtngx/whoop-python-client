"""User-related models for the WHOOP API."""

from pydantic import BaseModel, EmailStr, Field


class UserBasicProfile(BaseModel):
    """Basic profile information for a WHOOP user.
    
    Attributes:
        user_id: The WHOOP User ID.
        email: User's email address.
        first_name: User's first name.
        last_name: User's last name.
    """
    user_id: int = Field(
        ...,
        description="The WHOOP User",
        example=10129
    )
    email: EmailStr = Field(
        ...,
        description="User's Email",
        example="jsmith123@whoop.com"
    )
    first_name: str = Field(
        ...,
        description="User's First Name",
        example="John"
    )
    last_name: str = Field(
        ...,
        description="User's Last Name",
        example="Smith"
    )


class UserBodyMeasurement(BaseModel):
    """Body measurements for a WHOOP user.
    
    Attributes:
        height_meter: User's height in meters.
        weight_kilogram: User's weight in kilograms.
        max_heart_rate: WHOOP-calculated maximum heart rate for the user.
    """
    height_meter: float = Field(
        ...,
        description="User's height in meters",
        example=1.8288
    )
    weight_kilogram: float = Field(
        ...,
        description="User's weight in kilograms",
        example=90.7185
    )
    max_heart_rate: int = Field(
        ...,
        description="The max heart rate WHOOP calculated for the user",
        example=200
    )