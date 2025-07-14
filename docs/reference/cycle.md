# Cycle Methods

The cycle methods provide access to physiological cycle data, which represents periods of activity and strain in a user's day.

## Overview

WHOOP tracks physiological cycles that typically run from when you wake up until you go to sleep. Each cycle contains strain data, heart rate metrics, and energy expenditure information.

## Methods

::: whoop_client.client.WhoopClient.get_cycle_by_id
    options:
        show_source: false
        heading_level: 3

::: whoop_client.client.WhoopClient.get_cycle_collection
    options:
        show_source: false
        heading_level: 3

::: whoop_client.client.WhoopClient.get_sleep_for_cycle
    options:
        show_source: false
        heading_level: 3

::: whoop_client.client.WhoopClient.iterate_cycles
    options:
        show_source: false
        heading_level: 3

## Models

::: whoop_client.models.cycle.Cycle
    options:
        show_source: false
        heading_level: 3

::: whoop_client.models.cycle.CycleScore
    options:
        show_source: false
        heading_level: 3

::: whoop_client.models.cycle.PaginatedCycleResponse
    options:
        show_source: false
        heading_level: 3

## Usage Examples

### Getting a Specific Cycle

```python
import asyncio
from whoop_client import WhoopClient

async def get_cycle_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get a specific cycle by ID
    cycle = await client.get_cycle_by_id(93845)
    
    print(f"Cycle ID: {cycle.id}")
    print(f"Start: {cycle.start}")
    print(f"End: {cycle.end}")
    
    if cycle.score:
        print(f"Strain: {cycle.score.strain}")
        print(f"Average HR: {cycle.score.average_heart_rate}")
        print(f"Kilojoules: {cycle.score.kilojoule}")

asyncio.run(get_cycle_example())
```

### Getting Multiple Cycles

```python
import asyncio
from datetime import datetime
from whoop_client import WhoopClient

async def get_cycles_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get cycles from the last 7 days
    start_date = datetime.now() - timedelta(days=7)
    
    response = await client.get_cycle_collection(
        limit=10,
        start=start_date
    )
    
    for cycle in response.records:
        print(f"Cycle {cycle.id}: {cycle.start} - {cycle.end}")
        if cycle.score:
            print(f"  Strain: {cycle.score.strain}")
    
    # Check if there are more pages
    if response.next_token:
        print("More cycles available...")

asyncio.run(get_cycles_example())
```

### Iterating Through All Cycles

```python
import asyncio
from whoop_client import WhoopClient

async def iterate_cycles_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Iterate through all cycles (handles pagination automatically)
    async for cycle in client.iterate_cycles(page_size=25):
        print(f"Processing cycle {cycle.id}")
        if cycle.score:
            print(f"  Strain: {cycle.score.strain}")
        
        # Process only the first 100 cycles
        if cycle.id <= 100:
            break

asyncio.run(iterate_cycles_example())
```

### Getting Sleep for a Cycle

```python
import asyncio
from whoop_client import WhoopClient

async def get_cycle_sleep_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get sleep data for a specific cycle
    sleep = await client.get_sleep_for_cycle(93845)
    
    print(f"Sleep ID: {sleep.id}")
    print(f"Start: {sleep.start}")
    print(f"End: {sleep.end}")
    print(f"Is nap: {sleep.nap}")
    
    if sleep.score:
        print(f"Sleep efficiency: {sleep.score.sleep_efficiency_percentage}%")
        print(f"Sleep cycles: {sleep.score.stage_summary.sleep_cycle_count}")

asyncio.run(get_cycle_sleep_example())
```

## Rate Limiting

The cycle methods are subject to WHOOP's rate limiting. The client will automatically handle token refresh, but you should implement appropriate retry logic with exponential backoff for rate limit errors.

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
        cycle = await client.get_cycle_by_id(999999)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print("Cycle not found")
        elif e.response.status_code == 401:
            print("Authentication failed")
        elif e.response.status_code == 429:
            print("Rate limit exceeded")
        else:
            print(f"HTTP error: {e.response.status_code}")
    except ValueError as e:
        print(f"Client error: {e}")

asyncio.run(error_handling_example())
```