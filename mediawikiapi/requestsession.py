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
    ) -> Dict[str, Any]:
        """
        Make a request to the Wikipedia API using the given search parameters,
        language and configuration

        Arguments:

        * params (dictionary)
        * config - the configuration to be used for request

        Keyword arguments:

        * language - the wiki language

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
        return data
