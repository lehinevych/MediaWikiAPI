import sys
import re
import collections
import functools


class memoized_class(object):
  '''
  Decorator.
  Caches a function's return value each time it is called.
  If called later with the same arguments,
  the cached value is returned (not reevaluated).
  '''
  def __init__(self, func):
    self.func = func
    self.cache = {}
    functools.update_wrapper(self, func)

  def __call__(self, *args, **kwargs):
    if sys.version_info[0] < 3:
      hash_type = collections.Hashable
    else:
      hash_type = collections.abc.Hashable
    if not isinstance(args, hash_type):
      # uncacheable. a list, for instance.
      # better to not cache than blow up.
      return self.func(*args, **kwargs)
    key = str(args) + str(kwargs)
    if key in self.cache:
      return self.cache[key]
    else:
      value = self.func(*args, **kwargs)
      self.cache[key] = value
      return value

  def __repr__(self):
    '''Return the function's docstring.'''
    return self.func.__doc__

  def __get__(self, obj, objtype):
    '''Support instance methods.'''
    return functools.partial(self.__call__, obj)


# This decorator wrapper was added over class one for auto api document generation
def memorized(f):
    memoize = memoized_class(f)

    @functools.wraps(f)
    def helper(*args, **kws):
        return memoize(*args, **kws)

    return helper


def clean_infobox(text):
    text = re.sub(r"\[\d\]", '', text)
    text = re.sub(r"\n", ' ', text)
    if sys.version_info[0] < 3:
        text = text.replace(u'\xa0', u' ')
    else:
        text = text.replace('\xa0', ' ')
    return text.strip()
