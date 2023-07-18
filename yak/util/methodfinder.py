"""
A half-baked implementation of a method finder, written in a few minutes after
playing a bit with smalltalk's method finder. It's far from comprehensive or robust.

CAREFUL AS THIS WILL PERFORM NETWORK CALLS, DB AND/OR FILE WRITES, AND ANY OTHER
KIND OF SIDE EFFECT IN THE WORLD.
"""

import copy
import importlib
import pprint

from collections import UserList


def find_method(obj, *args, **kwargs):
    return MethodFinder.for_object(obj, args, kwargs)


def find_function(module_name, *args, **kwargs):
    return MethodFinder.for_module(module_name, args, kwargs)


class MethodFinderResult(UserList):
    def prettyprint(self):
        return pprint.pprint(self)


class MethodFinder:
    @classmethod
    def for_module(cls, module_name, args=None, kwargs=None):
        loaded_module = importlib.import_module(module_name)
        return cls(loaded_module, args, kwargs)

    @classmethod
    def for_object(cls, obj, args=None, kwargs=None):
        return cls(copy.deepcopy(obj), args, kwargs)

    def __init__(self, obj, args=None, kwargs=None):
        self.obj = obj
        self.args = (args or [])
        self.kwargs = (kwargs or {})

    def that_returns(self, expected):
        methods_found = []
        for attribute_name in dir(self.obj):
            candidate_func = getattr(self.obj, attribute_name)

            if not callable(candidate_func):
                continue

            if not self._try_call(candidate_func, expected):
                continue

            methods_found.append(attribute_name)

        return MethodFinderResult(sorted(methods_found))

    def _try_call(self, candidate_func, expected):
        try:
            return candidate_func(*self.args, **self.kwargs) == expected
        except:
            pass
