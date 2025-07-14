# Sleep Endpoints

The sleep endpoints provide access to sleep activity data and sleep performance metrics.

## Overview

WHOOP tracks sleep activities including regular sleep and naps. Each sleep record contains detailed information about sleep stages, efficiency, and recovery metrics.

## Methods

::: whoop_client.client.WhoopClient.get_sleep_by_id
    options:
        show_source: false
        heading_level: 3

::: whoop_client.client.WhoopClient.get_sleep_collection
    options:
        show_source: false
        heading_level: 3

::: whoop_client.client.WhoopClient.iterate_sleeps
    options:
        show_source: false
        heading_level: 3

## Models

::: whoop_client.models.sleep.Sleep
    options:
        show_source: false
        heading_level: 3

::: whoop_client.models.sleep.SleepScore
    options:
        show_source: false
        heading_level: 3

::: whoop_client.models.sleep.SleepStageSummary
    options:
        show_source: false
        heading_level: 3

::: whoop_client.models.sleep.SleepNeeded
    options:
        show_source: false
        heading_level: 3

## Usage Examples

### Getting a Specific Sleep

```python
import asyncio
from whoop_client import WhoopClient

async def get_sleep_example():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get a specific sleep by ID
    sleep_id = "ecfc6a15-4661-442f-a9a4-f160dd7afae8"
    sleep = await client.get_sleep_by_id(sleep_id)
    
    print(f"Sleep ID: {sleep.id}")
    print(f"Start: {sleep.start}")
    print(f"End: {sleep.end}")
    print(f"Is nap: {sleep.nap}")
    
    if sleep.score:
        print(f"Sleep efficiency: {sleep.score.sleep_efficiency_percentage}%")
        print(f"Sleep performance: {sleep.score.sleep_performance_percentage}%")
        print(f"Sleep cycles: {sleep.score.stage_summary.sleep_cycle_count}")

asyncio.run(get_sleep_example())
```

### Analyzing Sleep Stages

```python
import asyncio
from whoop_client import WhoopClient

async def analyze_sleep_stages():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    response = await client.get_sleep_collection(limit=10)
    
    for sleep in response.records:
        if sleep.score and not sleep.nap:  # Only analyze actual sleep, not naps
            stages = sleep.score.stage_summary
            
            # Convert milliseconds to hours
            total_sleep_hours = (stages.total_light_sleep_time_milli + 
                               stages.total_slow_wave_sleep_time_milli + 
                               stages.total_rem_sleep_time_milli) / (1000 * 60 * 60)
            
            light_hours = stages.total_light_sleep_time_milli / (1000 * 60 * 60)
            deep_hours = stages.total_slow_wave_sleep_time_milli / (1000 * 60 * 60)
            rem_hours = stages.total_rem_sleep_time_milli / (1000 * 60 * 60)
            
            print(f"Sleep on {sleep.start.date()}:")
            print(f"  Total sleep: {total_sleep_hours:.1f} hours")
            print(f"  Light sleep: {light_hours:.1f}h ({light_hours/total_sleep_hours*100:.1f}%)")
            print(f"  Deep sleep: {deep_hours:.1f}h ({deep_hours/total_sleep_hours*100:.1f}%)")
            print(f"  REM sleep: {rem_hours:.1f}h ({rem_hours/total_sleep_hours*100:.1f}%)")
            print(f"  Disturbances: {stages.disturbance_count}")
            print()

asyncio.run(analyze_sleep_stages())
```

### Sleep Trends Analysis

```python
import asyncio
from datetime import datetime, timedelta
from whoop_client import WhoopClient

async def sleep_trends_analysis():
    client = WhoopClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="your_redirect_uri",
        access_token="your_access_token",
        refresh_token="your_refresh_token"
    )
    
    # Get sleep data for the last 30 days
    start_date = datetime.now() - timedelta(days=30)
    
    sleep_data = []
    async for sleep in client.iterate_sleeps(start=start_date):
        if sleep.score and not sleep.nap:
            sleep_data.append(sleep)
    
    # Calculate averages
    if sleep_data:
        avg_efficiency = sum(s.score.sleep_efficiency_percentage for s in sleep_data) / len(sleep_data)
        avg_performance = sum(s.score.sleep_performance_percentage for s in sleep_data if s.score.sleep_performance_percentage) / len([s for s in sleep_data if s.score.sleep_performance_percentage])
        avg_cycles = sum(s.score.stage_summary.sleep_cycle_count for s in sleep_data) / len(sleep_data)
        
        print(f"Sleep trends over last 30 days ({len(sleep_data)} nights):")
        print(f"Average sleep efficiency: {avg_efficiency:.1f}%")
        print(f"Average sleep performance: {avg_performance:.1f}%")
        print(f"Average sleep cycles: {avg_cycles:.1f}")

asyncio.run(sleep_trends_analysis())
```

## Required Scopes

- `read:sleep` - Required for all sleep endpoints

## Understanding Sleep Metrics

### Sleep Efficiency
The percentage of time spent in bed actually sleeping. Higher values indicate better sleep quality.

### Sleep Performance
The percentage of sleep need that was fulfilled. Values above 85% are generally considered good.

### Sleep Consistency
How similar sleep and wake times are compared to previous days. Consistent sleep schedules improve sleep quality.

### Sleep Stages
- **Light Sleep**: Transition between awake and deep sleep
- **Deep Sleep (SWS)**: Slow Wave Sleep, crucial for physical recovery
- **REM Sleep**: Rapid Eye Movement sleep, important for cognitive function

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
        sleep = await client.get_sleep_by_id("invalid-uuid")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print("Sleep not found")
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