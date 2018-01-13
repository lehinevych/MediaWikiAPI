from __future__ import print_function, unicode_literals

import sys
import collections
import functools


class memorized(object):
  '''
  Decorator.
  Caches a function's return value each time it is called.
  If called later with the same arguments,
  the cached value is returned (not reevaluated).
  '''
  def __init__(self, func):
    self.func = func
    self.cache = {}

  def __call__(self, *args, **kwargs):
    if not isinstance(args, collections.Hashable):
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
