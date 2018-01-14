import requests


class RequestSession(object):
  """ Request wrapper class for request"""
  def __init__(self):
    """Require configuration instance as argument"""
    self.__session = None

  def __del__(self):
    if self.session is not None:
      self.session.close()

  @property
  def session(self):
    if self.__session is None:
      # initialize a session
      self.__session = requests.Session()
    return self.__session

  def new_session(self):
    self.__session = requests.Session()

  def request(self, params, config, language=None):
      '''
      Make a request to the Wikipedia API using the given search parameters,
      language and configuration

      Arguments:

      * params (dictionary)
      * config - the configuration to be used for request

      Keyword arguments:

      * language - the wiki language

      '''
      params['format'] = 'json'
      if not 'action' in params:
        params['action'] = 'query'

      headers = {
        'User-Agent': config.user_agent
      }

      rate_limit = config.rate_limit
      rate_limit_last_call = config.rate_limit_last_call

      if rate_limit_last_call and rate_limit_last_call + rate_limit > datetime.now():
        # it hasn't been long enough since the last API call
        # so wait until we're in the clear to make the request
        wait_time = (rate_limit_last_call + rate_limit) - datetime.now()
        time.sleep(int(wait_time.total_seconds()))
      r = self.session.get(config.get_api_url(language), params=params, headers=headers, timeout=config.timeout)

      if rate_limit:
        config.rate_limit_last_call = datetime.now()

      return r.json()
