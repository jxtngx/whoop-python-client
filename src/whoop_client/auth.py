"""OAuth2 authentication for WHOOP API."""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from urllib.parse import urlencode

import httpx
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """OAuth2 token response from WHOOP.
    
    Attributes:
        access_token: The access token for API requests.
        token_type: The type of token (typically "bearer").
        expires_in: Number of seconds until the token expires.
        refresh_token: Token used to refresh the access token.
        scope: Space-separated list of granted scopes.
    """
    access_token: str = Field(..., description="The access token for API requests")
    token_type: str = Field(..., description="The type of token")
    expires_in: int = Field(..., description="Seconds until token expires")
    refresh_token: Optional[str] = Field(None, description="Token to refresh access token")
    scope: Optional[str] = Field(None, description="Granted scopes")


class OAuth2Handler:
    """Handles OAuth2 authentication flow for WHOOP API.
    
    This class manages the OAuth2 authorization code flow, token storage,
    and automatic token refresh.
    
    Attributes:
        client_id: OAuth2 client ID from WHOOP.
        client_secret: OAuth2 client secret from WHOOP.
        redirect_uri: Redirect URI configured in WHOOP app settings.
        auth_base_url: Base URL for OAuth2 authorization.
        token_url: URL for token exchange.
        scopes: List of requested OAuth2 scopes.
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: Optional[List[str]] = None,
    ):
        """Initialize OAuth2 handler.
        
        Args:
            client_id: OAuth2 client ID from WHOOP.
            client_secret: OAuth2 client secret from WHOOP.
            redirect_uri: Redirect URI configured in WHOOP app settings.
            scopes: List of OAuth2 scopes to request. Defaults to all available scopes.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_base_url = "https://api.prod.whoop.com/oauth/oauth2/auth"
        self.token_url = "https://api.prod.whoop.com/oauth/oauth2/token"
        
        # Default to all available scopes if none specified
        self.scopes = scopes or [
            "read:recovery",
            "read:cycles",
            "read:workout",
            "read:sleep",
            "read:profile",
            "read:body_measurement",
        ]
        
        self._token_data: Optional[TokenResponse] = None
        self._token_expiry: Optional[datetime] = None
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate the authorization URL for user consent.
        
        Args:
            state: Optional state parameter for CSRF protection.
            
        Returns:
            The authorization URL to redirect the user to.
        """
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
        }
        
        if state:
            params["state"] = state
            
        return f"{self.auth_base_url}?{urlencode(params)}"
    
    async def exchange_code(self, code: str) -> TokenResponse:
        """Exchange authorization code for access token.
        
        Args:
            code: The authorization code from the redirect.
            
        Returns:
            Token response containing access token and refresh token.
            
        Raises:
            httpx.HTTPStatusError: If the token exchange fails.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                },
            )
            response.raise_for_status()
            
        token_data = TokenResponse(**response.json())
        self._store_token(token_data)
        return token_data
    
    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Refresh the access token using a refresh token.
        
        Args:
            refresh_token: The refresh token.
            
        Returns:
            New token response with refreshed access token.
            
        Raises:
            httpx.HTTPStatusError: If the token refresh fails.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            response.raise_for_status()
            
        token_data = TokenResponse(**response.json())
        self._store_token(token_data)
        return token_data
    
    def _store_token(self, token_data: TokenResponse) -> None:
        """Store token data and calculate expiry time.
        
        Args:
            token_data: The token response to store.
        """
        self._token_data = token_data
        # Calculate expiry with 5-minute buffer for safety
        self._token_expiry = datetime.now(timezone.utc) + timedelta(
            seconds=token_data.expires_in - 300
        )
    
    @property
    def access_token(self) -> Optional[str]:
        """Get the current access token if available.
        
        Returns:
            The access token or None if not available.
        """
        return self._token_data.access_token if self._token_data else None
    
    @property
    def refresh_token(self) -> Optional[str]:
        """Get the current refresh token if available.
        
        Returns:
            The refresh token or None if not available.
        """
        return self._token_data.refresh_token if self._token_data else None
    
    def is_token_expired(self) -> bool:
        """Check if the current access token is expired.
        
        Returns:
            True if token is expired or not available, False otherwise.
        """
        if not self._token_expiry:
            return True
        return datetime.now(timezone.utc) >= self._token_expiry
    
    def set_tokens(self, access_token: str, refresh_token: str, expires_in: int = 3600) -> None:
        """Manually set tokens (useful for restoring from storage).
        
        Args:
            access_token: The access token.
            refresh_token: The refresh token.
            expires_in: Seconds until token expires (default 1 hour).
        """
        token_data = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
            refresh_token=refresh_token,
        )
        self._store_token(token_data)