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
    
    Both synchronous and asynchronous implementations should support proper
    resource management through context managers or explicit close methods.
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
    
    @abstractmethod
    def close(self) -> Any:
        """
        Close the session and release resources.
        
        This method should be implemented by both synchronous and asynchronous
        implementations to ensure proper resource cleanup. The synchronous
        implementation returns None, while the asynchronous implementation
        returns a coroutine.
        
        Returns:
            None for sync, Awaitable[None] for async
        """
        pass
    
    @abstractmethod
    def new_session(self) -> Any:
        """
        Create a new session, closing the existing one if necessary.
        
        This method should be implemented by both synchronous and asynchronous
        implementations to ensure proper resource management when a new session
        is needed. The synchronous implementation returns None, while the
        asynchronous implementation returns a coroutine.
        
        Returns:
            None for sync, Awaitable[None] for async
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
    
    @abstractmethod
    def increment_reuse_counter(self) -> int:
        """
        Increment the session reuse counter and return the new value.
        
        This method is used to track how many times a session has been used,
        which can help determine when to refresh the session to prevent
        memory leaks or connection issues.
        
        Returns:
            Current reuse count after increment
        """
        pass
    
    @abstractmethod
    def should_refresh_session(self) -> bool:
        """
        Check if the session should be refreshed based on usage.
        
        Returns:
            True if the session should be refreshed, False otherwise
        """
        pass
    
    @abstractmethod
    def set_max_reuse_count(self, count: int) -> None:
        """
        Set the maximum number of times a session can be reused.
        
        Args:
            count: Maximum reuse count
        """
        pass