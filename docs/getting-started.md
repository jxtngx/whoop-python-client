# Getting Started

This guide will help you get started with the WHOOP Python client.

## Installation

You can install the WHOOP Python client using pip:

```bash
pip install whoop-python-client
```

Or install from source:

```bash
git clone https://github.com/your-username/whoop-python-client.git
cd whoop-python-client
pip install -e .
```

## Prerequisites

Before using the WHOOP Python client, you'll need:

1. **WHOOP Developer Account**: Sign up at [WHOOP Developer Portal](https://developer.whoop.com/)
2. **OAuth2 Application**: Create an application to get your client ID and secret
3. **OAuth2 Scopes**: Configure the required scopes for your application

### Required Dependencies

The client requires the following dependencies:

- `httpx` - For HTTP requests
- `pydantic` - For data validation and serialization
- `python-dateutil` - For date/time handling (optional, for convenience)

## OAuth2 Setup

### 1. Create WHOOP Developer Application

1. Go to the [WHOOP Developer Portal](https://developer.whoop.com/)
2. Create a new application
3. Configure your redirect URI (e.g., `http://localhost:8000/callback`)
4. Note down your `client_id` and `client_secret`

### 2. Configure OAuth2 Scopes

The following scopes are available:

- `read:profile` - Read user profile information
- `read:body_measurement` - Read body measurements (height, weight, max HR)
- `read:cycles` - Read physiological cycle data
- `read:sleep` - Read sleep activity data
- `read:recovery` - Read recovery data
- `read:workout` - Read workout data

### 3. Authentication Flow

The WHOOP API uses OAuth2 Authorization Code flow:

```python
import asyncio
from whoop_client import WhoopClient

async def oauth_flow():
    # Initialize client
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="http://localhost:8000/callback",
        scopes=["read:profile", "read:sleep", "read:cycles"]
    )
    
    # Step 1: Get authorization URL
    auth_url = client.auth.get_authorization_url(state="random_state")
    print(f"Go to: {auth_url}")
    
    # Step 2: User authorizes and you get the code from redirect
    authorization_code = input("Enter the authorization code: ")
    
    # Step 3: Exchange code for tokens
    tokens = await client.auth.exchange_code(authorization_code)
    
    print(f"Access token: {tokens.access_token}")
    print(f"Refresh token: {tokens.refresh_token}")
    
    # Now you can use the client
    profile = await client.get_profile_basic()
    print(f"Hello, {profile.first_name}!")

asyncio.run(oauth_flow())
```

## Basic Usage

### Initialize the Client

```python
from whoop_client import WhoopClient

# With existing tokens
client = WhoopClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="http://localhost:8000/callback",
    access_token="your_access_token",
    refresh_token="your_refresh_token"
)
```

### Get User Information

```python
import asyncio

async def get_user_info():
    # Get basic profile
    profile = await client.get_profile_basic()
    print(f"User: {profile.first_name} {profile.last_name}")
    
    # Get body measurements
    measurements = await client.get_body_measurement()
    print(f"Height: {measurements.height_meter}m")
    print(f"Weight: {measurements.weight_kilogram}kg")

asyncio.run(get_user_info())
```

### Get Recent Data

```python
import asyncio
from datetime import datetime, timedelta

async def get_recent_data():
    # Get cycles from the last 7 days
    start_date = datetime.now() - timedelta(days=7)
    
    cycles = await client.get_cycle_collection(
        limit=10,
        start=start_date
    )
    
    for cycle in cycles.records:
        print(f"Cycle {cycle.id}: Strain {cycle.score.strain if cycle.score else 'N/A'}")
    
    # Get recent sleep
    sleep_data = await client.get_sleep_collection(limit=5)
    
    for sleep in sleep_data.records:
        if sleep.score and not sleep.nap:
            print(f"Sleep: {sleep.score.sleep_efficiency_percentage}% efficiency")

asyncio.run(get_recent_data())
```

### Iterate Through All Data

```python
import asyncio

async def iterate_all_data():
    # Iterate through all cycles (handles pagination automatically)
    cycle_count = 0
    async for cycle in client.iterate_cycles():
        cycle_count += 1
        if cycle_count >= 100:  # Limit to first 100
            break
    
    print(f"Processed {cycle_count} cycles")
    
    # Iterate through recent sleep data
    sleep_count = 0
    async for sleep in client.iterate_sleeps():
        if not sleep.nap:  # Only count actual sleep, not naps
            sleep_count += 1
        if sleep_count >= 30:  # Last 30 sleep sessions
            break
    
    print(f"Processed {sleep_count} sleep sessions")

asyncio.run(iterate_all_data())
```

## Error Handling

Always implement proper error handling:

```python
import asyncio
import httpx

async def error_handling_example():
    try:
        profile = await client.get_profile_basic()
        print(f"User: {profile.first_name}")
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            print("Authentication failed - check your tokens")
        elif e.response.status_code == 403:
            print("Insufficient permissions - check your scopes")
        elif e.response.status_code == 429:
            print("Rate limit exceeded - wait and retry")
        else:
            print(f"HTTP error: {e.response.status_code}")
            
    except ValueError as e:
        print(f"Client configuration error: {e}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")

asyncio.run(error_handling_example())
```

## Token Management

### Storing Tokens Securely

```python
import os
import json
from pathlib import Path

def save_tokens(access_token, refresh_token):
    """Save tokens to a secure location."""
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    
    # Save to user's home directory
    token_file = Path.home() / ".whoop_tokens.json"
    
    with open(token_file, 'w') as f:
        json.dump(tokens, f)
    
    # Make file readable only by owner
    token_file.chmod(0o600)

def load_tokens():
    """Load tokens from storage."""
    token_file = Path.home() / ".whoop_tokens.json"
    
    if token_file.exists():
        with open(token_file, 'r') as f:
            return json.load(f)
    
    return None

# Usage
tokens = load_tokens()
if tokens:
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="http://localhost:8000/callback",
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"]
    )
```

### Automatic Token Refresh

The client automatically handles token refresh:

```python
import asyncio

async def auto_refresh_example():
    # Client will automatically refresh tokens when needed
    profile = await client.get_profile_basic()
    
    # Get updated tokens after refresh
    if client.auth.access_token:
        save_tokens(client.auth.access_token, client.auth.refresh_token)

asyncio.run(auto_refresh_example())
```

## Rate Limiting

WHOOP API has rate limits. The client doesn't automatically retry, so implement your own retry logic:

```python
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def get_data_with_retry():
    try:
        return await client.get_profile_basic()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            print("Rate limited, retrying...")
            raise
        else:
            print(f"HTTP error: {e.response.status_code}")
            raise

# Usage
try:
    profile = await get_data_with_retry()
    print(f"User: {profile.first_name}")
except Exception as e:
    print(f"Failed after retries: {e}")
```

## Best Practices

1. **Use Environment Variables**: Store sensitive information in environment variables
2. **Implement Retry Logic**: Handle rate limiting and temporary failures
3. **Cache Data**: Don't make unnecessary API calls
4. **Use Pagination**: Don't fetch all data at once for large datasets
5. **Handle Timezones**: Be aware of timezone offsets in the data
6. **Respect Rate Limits**: Implement appropriate delays between requests

## Common Use Cases

### Daily Summary Dashboard

```python
import asyncio
from datetime import datetime, timedelta

async def daily_summary():
    today = datetime.now().date()
    
    # Get today's cycle
    cycles = await client.get_cycle_collection(
        start=datetime.combine(today, datetime.min.time()),
        limit=1
    )
    
    if cycles.records:
        cycle = cycles.records[0]
        print(f"Today's Strain: {cycle.score.strain if cycle.score else 'N/A'}")
    
    # Get last night's sleep
    sleep_data = await client.get_sleep_collection(limit=5)
    last_sleep = next((s for s in sleep_data.records if not s.nap), None)
    
    if last_sleep and last_sleep.score:
        print(f"Last Sleep Efficiency: {last_sleep.score.sleep_efficiency_percentage}%")
    
    # Get latest recovery
    recovery_data = await client.get_recovery_collection(limit=1)
    if recovery_data.records and recovery_data.records[0].score:
        recovery = recovery_data.records[0]
        print(f"Recovery Score: {recovery.score.recovery_score}%")

asyncio.run(daily_summary())
```

### Weekly Trend Analysis

```python
import asyncio
from datetime import datetime, timedelta

async def weekly_trends():
    week_ago = datetime.now() - timedelta(days=7)
    
    # Collect all data for the week
    cycles = []
    async for cycle in client.iterate_cycles(start=week_ago):
        cycles.append(cycle)
    
    # Calculate averages
    strains = [c.score.strain for c in cycles if c.score]
    avg_strain = sum(strains) / len(strains) if strains else 0
    
    print(f"Average Strain this week: {avg_strain:.1f}")
    print(f"Total cycles: {len(cycles)}")

asyncio.run(weekly_trends())
```

## Next Steps

- Explore the [API Reference](../reference/) for detailed method documentation
- Check out the [Examples](../examples/) for more complex use cases
- Review the [Models](../models/) documentation for data structure details

## Support

If you encounter issues:

1. Check the [Troubleshooting](../troubleshooting/) guide
2. Review the [WHOOP API Documentation](https://developer.whoop.com/docs/)
3. File an issue on [GitHub](https://github.com/jxtngx/whoop-python-client/issues)