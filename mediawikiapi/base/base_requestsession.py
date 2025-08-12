"""
Base class for request session implementations.

This module provides the abstract base class that both synchronous and
asynchronous request session implementations extend.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from ..config import Config


class BaseRequestSession(ABC):
    """
    Abstract base class for MediaWiki API request sessions.
    
    This class defines the interface for making requests to the MediaWiki API,
    with different implementations for synchronous and asynchronous operations.
    """
    
    def __init__(self) -> None:
        """Initialize the request session."""
        # Common initialization can go here
        pass
    
    @abstractmethod
    def request(
        self, params: Dict[str, Any], config: Config
    ) -> Any:
        """
        Make a request to the MediaWiki API.
        
        Args:
            params: API request parameters
            config: Configuration object
            
        Returns:
            API response (Dict for sync, Awaitable[Dict] for async)
        """
        pass
    
    def _build_api_url(self, config: Config) -> str:
        """
        Build the API URL from configuration.
        
        Args:
            config: Configuration object containing language
            
        Returns:
            URL for the MediaWiki API
        """
        return f"https://{config.language}.wikipedia.org/w/api.php"
    
    def _prepare_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare parameters for API request.
        
        Args:
            params: Original parameters
            
        Returns:
            Parameters with common defaults added
        """
        # Add common parameters like format=json
        default_params = {
            "format": "json",
            "action": "query",
        }
        
        # Don't override action if it's explicitly set
        if "action" in params:
            del default_params["action"]
            
        return {**default_params, **params}
    
    def _build_user_agent(self, config: Config) -> str:
        """
        Build the User-Agent string from configuration.
        
        Args:
            config: Configuration object
            
        Returns:
            User-Agent string for HTTP requests
        """
        return config.user_agent