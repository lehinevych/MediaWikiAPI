import time
import requests
from datetime import datetime
from typing import Dict, Any, Union, Optional
from .config import Config
from .language import Language


class RequestSession(object):
    """Request wrapper class for request"""

    def __init__(self) -> None:
        """Require configuration instance as argument"""
        self.__session: requests.Session = requests.Session()
        self.__rate_limit_last_call: Optional[datetime] = None

    def __del__(self) -> None:
        if self.session is not None:
            self.session.close()

    @property
    def session(self) -> requests.Session:
        return self.__session

    def new_session(self) -> None:
        self.__session = requests.Session()

    def request(
        self,
        params: Dict[str, Any],
        config: Config,
        language: Optional[Union[str, Language]] = None,
        follow_continue: bool = False,
    ) -> Dict[str, Any]:
        """
        Make a request to the Wikipedia API using the given search parameters,
        language and configuration

        Arguments:

        * params (dictionary)
        * config - the configuration to be used for request

        Keyword arguments:

        * language - the wiki language
        * follow_continue - if True, automatically follow 'continue' tokens to get all results

        """
        params["format"] = "json"
        if "action" not in params:
            params["action"] = "query"

        headers = {"User-Agent": config.user_agent}

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
            time.sleep(int(wait_time.total_seconds()))
            self.__rate_limit_last_call = datetime.now()

        r = self.session.get(
            config.get_api_url(language),
            params=params,
            headers=headers,
            timeout=config.timeout,
        )

        data: Dict[str, Any] = r.json()

        # If follow_continue is False or there's no continue token, return the data as is
        if not follow_continue or "continue" not in data:
            return data

        # If follow_continue is True, handle continuation
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
                config.get_api_url(language),
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
