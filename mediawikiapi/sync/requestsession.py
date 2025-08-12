import time
from datetime import datetime
from typing import Any, Dict, Optional, Union

import requests

from ..base.base_requestsession import BaseRequestSession
from ..config import Config
from ..language import Language


class RequestSession(BaseRequestSession):
    """
    Synchronous request session for the MediaWiki API.
    
    This class extends BaseRequestSession with synchronous HTTP requests
    using the requests library.
    """

    def __init__(self) -> None:
        """Initialize the request session with a new requests Session."""
        super().__init__()
        self.__session: requests.Session = requests.Session()
        self.__rate_limit_last_call: Optional[datetime] = None

    def __del__(self) -> None:
        """Clean up the session when the object is deleted."""
        if self.session is not None:
            self.session.close()

    @property
    def session(self) -> requests.Session:
        """Get the underlying requests Session object."""
        return self.__session

    def new_session(self) -> None:
        """Create a new requests Session."""
        self.__session = requests.Session()

    def request(
        self,
        params: Dict[str, Any],
        config: Config,
        language: Optional[Union[str, Language]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the MediaWiki API.
        
        Args:
            params: API request parameters
            config: Configuration object
            language: Optional language override
            
        Returns:
            API response as a dictionary
        """
        # Prepare parameters using helper method from the base class
        params = self._prepare_params(params)
        
        # Build the user agent
        headers = {"User-Agent": self._build_user_agent(config)}
        
        # Handle rate limiting
        if (
            self.__rate_limit_last_call
            and config.rate_limit
            and (self.__rate_limit_last_call + config.rate_limit) > datetime.now()
        ):
            # It hasn't been long enough since the last API call
            # so wait until we're in the clear to make the request
            wait_time = (
                self.__rate_limit_last_call + config.rate_limit
            ) - datetime.now()
            time.sleep(int(wait_time.total_seconds()))
            self.__rate_limit_last_call = datetime.now()
        
        # Get the API URL using the configured language or the override
        api_url = config.get_api_url(language)
        
        # Make the request
        r = self.session.get(
            api_url,
            params=params,
            headers=headers,
            timeout=config.timeout,
        )
        
        data: Dict[str, Any] = r.json()
        
        # If there's no continue token, return the data as is
        if "continue" not in data:
            return data
        
        # Handle continuation
        result = data  # Start with the initial result
        
        # Continue requesting while there's a continue token
        while "continue" in result:
            # Copy the original parameters and update with continue tokens
            continue_params = params.copy()
            continue_params.update(result["continue"])
            
            # Respect rate limits
            if (
                self.__rate_limit_last_call
                and config.rate_limit
                and (self.__rate_limit_last_call + config.rate_limit) > datetime.now()
            ):
                wait_time = (
                    self.__rate_limit_last_call + config.rate_limit
                ) - datetime.now()
                if wait_time.total_seconds() > 0:
                    time.sleep(int(wait_time.total_seconds()))
            
            # Make the continuation request
            r = self.session.get(
                api_url,
                params=continue_params,
                headers=headers,
                timeout=config.timeout,
            )
            self.__rate_limit_last_call = datetime.now()
            
            # Get the continued data
            continued_data = r.json()
            
            # Merge the data from the continued request with the initial result
            if "query" in continued_data:
                # Handle pages
                if "pages" in continued_data.get("query", {}) and "pages" in result.get(
                    "query", {}
                ):
                    for pageid, page_data in continued_data["query"]["pages"].items():
                        if pageid in result["query"]["pages"]:
                            # Page exists in the result, merge properties
                            for prop, value in page_data.items():
                                if prop in result["query"]["pages"][pageid]:
                                    # If the property is a list, extend it
                                    if isinstance(value, list) and isinstance(
                                        result["query"]["pages"][pageid][prop], list
                                    ):
                                        result["query"]["pages"][pageid][prop].extend(
                                            value
                                        )
                                    else:
                                        # Otherwise, replace it
                                        result["query"]["pages"][pageid][prop] = value
                                else:
                                    # Property doesn't exist in the result, add it
                                    result["query"]["pages"][pageid][prop] = value
                        else:
                            # Page doesn't exist in the result, add it
                            result["query"]["pages"][pageid] = page_data
                
                # Handle lists in the query (like search results, backlinks, etc.)
                for prop, value in continued_data["query"].items():
                    if prop != "pages":
                        if prop not in result["query"]:
                            result["query"][prop] = value
                        elif isinstance(value, list) and isinstance(
                            result["query"][prop], list
                        ):
                            # If the property is a list, extend it
                            result["query"][prop].extend(value)
            
            # Update the continue token
            if "continue" in continued_data:
                result["continue"] = continued_data["continue"]
            else:
                # No more continue tokens, we're done
                if "continue" in result:
                    del result["continue"]
                break
        
        return result