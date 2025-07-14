# WHOOP Python Client

A comprehensive Python client for the WHOOP API that provides easy access to your fitness and recovery data.

## Features

- **Full API Coverage**: Access all WHOOP API endpoints including cycles, sleep, recovery, workouts, and user data
- **Type Safety**: Built with Pydantic models for robust data validation and IDE support
- **OAuth2 Authentication**: Complete OAuth2 flow implementation with automatic token refresh
- **Async Support**: Fully asynchronous API using HTTPX for efficient concurrent requests
- **Pagination Support**: Automatic pagination handling for large datasets
- **Error Handling**: Comprehensive error handling with meaningful error messages
- **Rate Limiting**: Built-in awareness of API rate limits
- **Documentation**: Extensive documentation with examples and best practices

## Quick Start

### Installation

```bash
pip install whoop-python-client
```

### Basic Usage

```python
import asyncio
from whoop_client import WhoopClient

async def main():
    # Initialize client
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="http://localhost:8000/callback",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get user profile
    profile = await client.get_profile_basic()
    print(f"Hello, {profile.first_name}!")
    
    # Get recent cycles
    cycles = await client.get_cycle_collection(limit=5)
    for cycle in cycles.records:
        if cycle.score:
            print(f"Cycle {cycle.id}: Strain {cycle.score.strain}")
    
    # Get sleep data
    sleep_data = await client.get_sleep_collection(limit=3)
    for sleep in sleep_data.records:
        if sleep.score and not sleep.nap:
            print(f"Sleep efficiency: {sleep.score.sleep_efficiency_percentage}%")

asyncio.run(main())
```

## API Coverage

The client provides access to all WHOOP API v2 endpoints:

### Cycles
- Get specific cycle by ID
- Get paginated cycle collection
- Get sleep data for a cycle
- Iterate through all cycles

### Sleep
- Get specific sleep by ID
- Get paginated sleep collection
- Detailed sleep stage analysis
- Sleep performance metrics

### Recovery
- Get recovery collection
- Get recovery for specific cycle
- HRV and recovery score data
- Skin temperature and SpO2 (4.0+ devices)

### Workouts
- Get specific workout by ID
- Get paginated workout collection
- Heart rate zones and strain data
- Distance and altitude metrics

### User
- Basic profile information
- Body measurements
- Height, weight, and max heart rate

## Data Models

All API responses are validated using Pydantic models:

```python
from whoop_client.models import Cycle, Sleep, Recovery, WorkoutV2

# Type-safe data access
cycle: Cycle = await client.get_cycle_by_id(12345)
print(f"Strain: {cycle.score.strain}")  # IDE autocomplete supported

# Validation ensures data integrity
sleep: Sleep = await client.get_sleep_by_id("uuid-string")
print(f"Sleep stages: {sleep.score.stage_summary}")
```

## Authentication

The client handles OAuth2 authentication with automatic token refresh:

```python
from whoop_client import WhoopClient

# Initialize with OAuth2 credentials
client = WhoopClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="http://localhost:8000/callback",
    scopes=["read:profile", "read:cycles", "read:sleep"]
)

# Get authorization URL
auth_url = client.auth.get_authorization_url()
print(f"Visit: {auth_url}")

# Exchange authorization code for tokens
tokens = await client.auth.exchange_code("authorization_code")

# Client automatically refreshes tokens when needed
profile = await client.get_profile_basic()
```

## Pagination Made Easy

Handle large datasets with automatic pagination:

```python
# Manual pagination
response = await client.get_cycle_collection(limit=25)
while response.next_token:
    response = await client.get_cycle_collection(
        limit=25, 
        next_token=response.next_token
    )

# Automatic pagination
async for cycle in client.iterate_cycles():
    print(f"Processing cycle {cycle.id}")
    if cycle.id < 1000:  # Process first 1000 cycles
        break
```

## Error Handling

Comprehensive error handling for robust applications:

```python
import httpx
from whoop_client import WhoopClient

try:
    profile = await client.get_profile_basic()
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        print("Authentication failed")
    elif e.response.status_code == 429:
        print("Rate limit exceeded")
    else:
        print(f"HTTP error: {e.response.status_code}")
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Next Steps

- [**Getting Started**](getting-started.md) - Complete setup guide and basic usage
- [**API Reference**](reference/client.md) - Detailed method documentation
- [**Endpoints**](endpoints/cycle.md) - Examples for each API endpoint
- [**Models**](reference/models.md) - Data model documentation

## Requirements

- Python 3.8+
- WHOOP Developer Account
- OAuth2 Application configured in WHOOP Developer Portal

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please see the contributing guidelines for details.

## Support

- [GitHub Issues](https://github.com/jxtngx/whoop-python-client/issues)
- [WHOOP Developer Documentation](https://developer.whoop.com/docs/)
- [API Reference](https://developer.whoop.com/api/)

---

*This client is not officially associated with WHOOP. WHOOP is a trademark of WHOOP, Inc.*