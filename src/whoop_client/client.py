"""WHOOP API client implementation."""

from datetime import datetime
from typing import AsyncIterator, Dict, List, Optional, Union
from uuid import UUID

import httpx

from .auth import OAuth2Handler
from .models import (
    Cycle,
    PaginatedCycleResponse,
    PaginatedSleepResponse,
    Recovery,
    RecoveryCollection,
    Sleep,
    UserBasicProfile,
    UserBodyMeasurement,
    WorkoutCollection,
    WorkoutV2,
)


class WhoopClient:
    """Client for interacting with the WHOOP API.
    
    This client provides methods for all WHOOP API endpoints including cycles,
    sleep, recovery, workouts, and user data. It handles OAuth2 authentication
    and automatic token refresh.
    
    Attributes:
        base_url: Base URL for WHOOP API.
        auth: OAuth2 authentication handler.
        timeout: Request timeout in seconds.
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        timeout: float = 30.0,
    ):
        """Initialize WHOOP API client.
        
        Args:
            client_id: OAuth2 client ID from WHOOP.
            client_secret: OAuth2 client secret from WHOOP.
            redirect_uri: Redirect URI configured in WHOOP app settings.
            access_token: Existing access token (optional).
            refresh_token: Existing refresh token (optional).
            scopes: List of OAuth2 scopes to request.
            timeout: Request timeout in seconds.
        """
        self.base_url = "https://api.prod.whoop.com/developer"
        self.auth = OAuth2Handler(client_id, client_secret, redirect_uri, scopes)
        self.timeout = timeout
        
        # Set existing tokens if provided
        if access_token and refresh_token:
            self.auth.set_tokens(access_token, refresh_token)
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
    ) -> httpx.Response:
        """Make an authenticated request to the WHOOP API.
        
        Args:
            method: HTTP method (GET, POST, etc.).
            endpoint: API endpoint path.
            params: Query parameters.
            json: JSON body data.
            
        Returns:
            HTTP response object.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
            ValueError: If no access token is available.
        """
        # Check token and refresh if needed
        if self.auth.is_token_expired() and self.auth.refresh_token:
            await self.auth.refresh_access_token(self.auth.refresh_token)
        
        if not self.auth.access_token:
            raise ValueError("No access token available. Please authenticate first.")
        
        headers = {"Authorization": f"Bearer {self.auth.access_token}"}
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
            )
            response.raise_for_status()
            return response
    
    # Cycle endpoints
    
    async def get_cycle_by_id(self, cycle_id: int) -> Cycle:
        """Get a specific cycle by ID.
        
        Args:
            cycle_id: ID of the cycle to retrieve.
            
        Returns:
            The requested cycle.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        response = await self._request("GET", f"/v2/cycle/{cycle_id}")
        return Cycle(**response.json())
    
    async def get_cycle_collection(
        self,
        limit: int = 10,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        next_token: Optional[str] = None,
    ) -> PaginatedCycleResponse:
        """Get all physiological cycles for a user, paginated.
        
        Results are sorted by start time in descending order.
        
        Args:
            limit: Maximum number of cycles to return (max 25, default 10).
            start: Return cycles that occurred after or during this time.
            end: Return cycles that ended before this time (default: now).
            next_token: Token from previous response to get next page.
            
        Returns:
            Paginated response containing cycles.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        params = {"limit": min(limit, 25)}
        
        if start:
            params["start"] = start.isoformat()
        if end:
            params["end"] = end.isoformat()
        if next_token:
            params["nextToken"] = next_token
            
        response = await self._request("GET", "/v2/cycle", params=params)
        return PaginatedCycleResponse(**response.json())
    
    async def get_sleep_for_cycle(self, cycle_id: int) -> Sleep:
        """Get the sleep for a specific cycle.
        
        Args:
            cycle_id: ID of the cycle to retrieve sleep for.
            
        Returns:
            The sleep activity for the cycle.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        response = await self._request("GET", f"/v2/cycle/{cycle_id}/sleep")
        return Sleep(**response.json())
    
    # Recovery endpoints
    
    async def get_recovery_collection(
        self,
        limit: int = 10,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        next_token: Optional[str] = None,
    ) -> RecoveryCollection:
        """Get all recoveries for a user, paginated.
        
        Results are sorted by start time of related sleep in descending order.
        
        Args:
            limit: Maximum number of recoveries to return (max 25, default 10).
            start: Return recoveries that occurred after or during this time.
            end: Return recoveries that ended before this time (default: now).
            next_token: Token from previous response to get next page.
            
        Returns:
            Paginated response containing recoveries.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        params = {"limit": min(limit, 25)}
        
        if start:
            params["start"] = start.isoformat()
        if end:
            params["end"] = end.isoformat()
        if next_token:
            params["nextToken"] = next_token
            
        response = await self._request("GET", "/v2/activity/recovery", params=params)
        return RecoveryCollection(**response.json())
    
    async def get_recovery_for_cycle(self, cycle_id: int) -> Recovery:
        """Get the recovery for a specific cycle.
        
        Args:
            cycle_id: ID of the cycle to retrieve recovery for.
            
        Returns:
            The recovery for the cycle.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        response = await self._request(
            "GET", f"/v2/activity/recovery/cycle/{cycle_id}/recovery"
        )
        return Recovery(**response.json())
    
    # Sleep endpoints
    
    async def get_sleep_by_id(self, sleep_id: Union[str, UUID]) -> Sleep:
        """Get a specific sleep by ID.
        
        Args:
            sleep_id: UUID of the sleep to retrieve.
            
        Returns:
            The requested sleep activity.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        sleep_id_str = str(sleep_id)
        response = await self._request("GET", f"/v2/activity/sleep/{sleep_id_str}")
        return Sleep(**response.json())
    
    async def get_sleep_collection(
        self,
        limit: int = 10,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        next_token: Optional[str] = None,
    ) -> PaginatedSleepResponse:
        """Get all sleeps for a user, paginated.
        
        Results are sorted by start time in descending order.
        
        Args:
            limit: Maximum number of sleeps to return (max 25, default 10).
            start: Return sleeps that occurred after or during this time.
            end: Return sleeps that ended before this time (default: now).
            next_token: Token from previous response to get next page.
            
        Returns:
            Paginated response containing sleep activities.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        params = {"limit": min(limit, 25)}
        
        if start:
            params["start"] = start.isoformat()
        if end:
            params["end"] = end.isoformat()
        if next_token:
            params["nextToken"] = next_token
            
        response = await self._request("GET", "/v2/activity/sleep", params=params)
        return PaginatedSleepResponse(**response.json())
    
    # User endpoints
    
    async def get_body_measurement(self) -> UserBodyMeasurement:
        """Get body measurements for the authenticated user.
        
        Returns:
            User's body measurements including height, weight, and max heart rate.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        response = await self._request("GET", "/v2/user/measurement/body")
        return UserBodyMeasurement(**response.json())
    
    async def get_profile_basic(self) -> UserBasicProfile:
        """Get basic profile information for the authenticated user.
        
        Returns:
            User's basic profile including name and email.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        response = await self._request("GET", "/v2/user/profile/basic")
        return UserBasicProfile(**response.json())
    
    # Workout endpoints
    
    async def get_workout_by_id(self, workout_id: Union[str, UUID]) -> WorkoutV2:
        """Get a specific workout by ID.
        
        Args:
            workout_id: UUID of the workout to retrieve.
            
        Returns:
            The requested workout activity.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        workout_id_str = str(workout_id)
        response = await self._request("GET", f"/v2/activity/workout/{workout_id_str}")
        return WorkoutV2(**response.json())
    
    async def get_workout_collection(
        self,
        limit: int = 10,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        next_token: Optional[str] = None,
    ) -> WorkoutCollection:
        """Get all workouts for a user, paginated.
        
        Results are sorted by start time in descending order.
        
        Args:
            limit: Maximum number of workouts to return (max 25, default 10).
            start: Return workouts that occurred after or during this time.
            end: Return workouts that ended before this time (default: now).
            next_token: Token from previous response to get next page.
            
        Returns:
            Paginated response containing workout activities.
            
        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        params = {"limit": min(limit, 25)}
        
        if start:
            params["start"] = start.isoformat()
        if end:
            params["end"] = end.isoformat()
        if next_token:
            params["nextToken"] = next_token
            
        response = await self._request("GET", "/v2/activity/workout", params=params)
        return WorkoutCollection(**response.json())
    
    # Pagination helpers
    
    async def iterate_cycles(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        page_size: int = 25,
    ) -> AsyncIterator[Cycle]:
        """Iterate through all cycles with automatic pagination.
        
        Args:
            start: Return cycles that occurred after or during this time.
            end: Return cycles that ended before this time.
            page_size: Number of items per page (max 25).
            
        Yields:
            Individual cycle objects.
        """
        next_token = None
        
        while True:
            response = await self.get_cycle_collection(
                limit=page_size, start=start, end=end, next_token=next_token
            )
            
            for cycle in response.records:
                yield cycle
                
            if not response.next_token:
                break
                
            next_token = response.next_token
    
    async def iterate_sleeps(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        page_size: int = 25,
    ) -> AsyncIterator[Sleep]:
        """Iterate through all sleeps with automatic pagination.
        
        Args:
            start: Return sleeps that occurred after or during this time.
            end: Return sleeps that ended before this time.
            page_size: Number of items per page (max 25).
            
        Yields:
            Individual sleep objects.
        """
        next_token = None
        
        while True:
            response = await self.get_sleep_collection(
                limit=page_size, start=start, end=end, next_token=next_token
            )
            
            for sleep in response.records:
                yield sleep
                
            if not response.next_token:
                break
                
            next_token = response.next_token
    
    async def iterate_recoveries(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        page_size: int = 25,
    ) -> AsyncIterator[Recovery]:
        """Iterate through all recoveries with automatic pagination.
        
        Args:
            start: Return recoveries that occurred after or during this time.
            end: Return recoveries that ended before this time.
            page_size: Number of items per page (max 25).
            
        Yields:
            Individual recovery objects.
        """
        next_token = None
        
        while True:
            response = await self.get_recovery_collection(
                limit=page_size, start=start, end=end, next_token=next_token
            )
            
            for recovery in response.records:
                yield recovery
                
            if not response.next_token:
                break
                
            next_token = response.next_token
    
    async def iterate_workouts(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        page_size: int = 25,
    ) -> AsyncIterator[WorkoutV2]:
        """Iterate through all workouts with automatic pagination.
        
        Args:
            start: Return workouts that occurred after or during this time.
            end: Return workouts that ended before this time.
            page_size: Number of items per page (max 25).
            
        Yields:
            Individual workout objects.
        """
        next_token = None
        
        while True:
            response = await self.get_workout_collection(
                limit=page_size, start=start, end=end, next_token=next_token
            )
            
            for workout in response.records:
                yield workout
                
            if not response.next_token:
                break
                
            next_token = response.next_token