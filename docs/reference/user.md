# User Methods

The user methods provide access to user profile information and body measurements.

## Overview

These methods allow you to retrieve basic profile information and physical measurements for the authenticated user.

## Methods

::: whoop_client.client.WhoopClient.get_profile_basic
    options:
        show_source: false
        heading_level: 3

::: whoop_client.client.WhoopClient.get_body_measurement
    options:
        show_source: false
        heading_level: 3

## Models

::: whoop_client.models.user.UserBasicProfile
    options:
        show_source: false
        heading_level: 3

::: whoop_client.models.user.UserBodyMeasurement
    options:
        show_source: false
        heading_level: 3

## Usage Examples

### Getting Basic Profile

```python
import asyncio
from whoop_client import WhoopClient

async def get_profile_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get basic user profile
    profile = await client.get_profile_basic()
    
    print(f"User ID: {profile.user_id}")
    print(f"Email: {profile.email}")
    print(f"Name: {profile.first_name} {profile.last_name}")

asyncio.run(get_profile_example())
```

### Getting Body Measurements

```python
import asyncio
from whoop_client import WhoopClient

async def get_measurements_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get body measurements
    measurements = await client.get_body_measurement()
    
    print(f"Height: {measurements.height_meter:.2f} meters")
    print(f"Weight: {measurements.weight_kilogram:.1f} kg")
    print(f"Max HR: {measurements.max_heart_rate} bpm")
    
    # Convert to imperial units
    height_feet = measurements.height_meter * 3.28084
    weight_pounds = measurements.weight_kilogram * 2.20462
    
    print(f"Height: {height_feet:.1f} feet")
    print(f"Weight: {weight_pounds:.1f} pounds")

asyncio.run(get_measurements_example())
```

### Complete User Information

```python
import asyncio
from whoop_client import WhoopClient

async def get_user_info_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get both profile and measurements
    profile, measurements = await asyncio.gather(
        client.get_profile_basic(),
        client.get_body_measurement()
    )
    
    print(f"User: {profile.first_name} {profile.last_name}")
    print(f"Email: {profile.email}")
    print(f"User ID: {profile.user_id}")
    print(f"Height: {measurements.height_meter:.2f}m")
    print(f"Weight: {measurements.weight_kilogram:.1f}kg")
    print(f"Max Heart Rate: {measurements.max_heart_rate} bpm")

asyncio.run(get_user_info_example())
```

## Required Scopes

- `read:profile` - Required for `get_profile_basic()`
- `read:body_measurement` - Required for `get_body_measurement()`

## Error Handling

```python
import asyncio
import httpx
from whoop_client import WhoopClient

async def error_handling_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    try:
        profile = await client.get_profile_basic()
        measurements = await client.get_body_measurement()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            print("Authentication failed - check your tokens")
        elif e.response.status_code == 403:
            print("Insufficient permissions - check your scopes")
        elif e.response.status_code == 404:
            print("User data not found")
        else:
            print(f"HTTP error: {e.response.status_code}")
    except ValueError as e:
        print(f"Client error: {e}")

asyncio.run(error_handling_example())
```