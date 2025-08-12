import asyncio
import time
from datetime import datetime
from typing import Any, Dict, Optional, Union, Coroutine

import aiohttp

from ..base.base_requestsession import BaseRequestSession
from ..config import Config
from ..language import Language


class AsyncRequestSession(BaseRequestSession):
    """Asynchronous request wrapper class for aiohttp"""

    def __init__(self) -> None:
        """Initialize the async session"""
        super().__init__()
        self.__session: Optional[aiohttp.ClientSession] = None
        self.__rate_limit_last_call: Optional[datetime] = None

    @property
    async def session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp client session"""
        if self.__session is None or self.__session.closed:
            self.__session = aiohttp.ClientSession()
        return self.__session

    async def close(self) -> None:
        """Close the session if it exists"""
        if self.__session and not self.__session.closed:
            await self.__session.close()
            self.__session = None

    async def new_session(self) -> None:
        """Create a new session, closing the old one if it exists"""
        await self.close()
        self.__session = aiohttp.ClientSession()

    async def request(
        self,
        params: Dict[str, Any],
        config: Config,
        language: Optional[Union[str, Language]] = None,
    ) -> Dict[str, Any]:
        """
        Make an asynchronous request to the Wikipedia API using the given search parameters,
        language and configuration

        Arguments:

        * params (dictionary)
        * config - the configuration to be used for request

        Keyword arguments:

        * language - the wiki language
        """
        # Use base class method to prepare parameters
        params = self._prepare_params(params)

        headers = {"User-Agent": self._build_user_agent(config)}

        if (
            self.__rate_limit_last_call
            and config.rate_limit
            and (self.__rate_limit_last_call + config.rate_limit) > datetime.now()
        ):
            # it hasn't been long enough since the last API call
            # so wait until we're in the clear to make the request
            wait_time = (
                self.__rate_limit_last_call + config.rate_limit
            ) - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            self.__rate_limit_last_call = datetime.now()

        session = await self.session
        async with session.get(
            config.get_api_url(language),
            params=params,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=config.timeout),
        ) as response:
            data: Dict[str, Any] = await response.json()

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
                    await asyncio.sleep(wait_time.total_seconds())

            # Make the continuation request
            session = await self.session
            async with session.get(
                config.get_api_url(language),
                params=continue_params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=config.timeout),
            ) as response:
                self.__rate_limit_last_call = datetime.now()
                continued_data = await response.json()

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
