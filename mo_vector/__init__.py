# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
from mo_dots import Null


class Vector(object):
    def __init__(self, args_gen):
        self.args_gen = args_gen  # A GENERATOR OF FUNCTION ARGUMENTS

    def __iter__(self):
        for a in self.args_gen():
            yield a[0]

    ###########################################################################
    # CHAINED METHODS
    ###########################################################################

    def map(self, func, *args, **kwargs):
        def _map():
            for i, a in enumerate(self.args_gen()):
                yield (func(*(a[:1] + args), **kwargs), i)

        return Vector(_map)

    def append(self, value):
        def _append():
            i = 0
            for a in self.args_gen():
                yield (a[0], i)
                i = i + 1
            yield (value, i)

        return Vector(_append)

    def enumerate(self):
        def _enumerate():
            for i, a in enumerate(self.args_gen()):
                yield (a[0], i)

        return Vector(_enumerate)

    def limit(self, max):
        def _limit():
            for i, a in enumerate(self.args_gen()):
                if i >= max:
                    break
                yield a

        return Vector(_limit)

    ###########################################################################
    # TERMINAL METHODS (EXIT VECTOR MODE)
    ###########################################################################

    def max(self):
        output = Null
        for a in self.args_gen():
            if output < a[0]:
                output = a[0]
        return output

    def first(self):
        for a in self.args_gen():
            return a[0]
        return Null

    def list(self):
        return list(self)


###########################################################################
# ADD SOME SHORTCUTS FOR COMMON MAPPED METHODS
###########################################################################


def _add_map(func, name):
    def mapped(self, *args, **kwargs):
        return self.map(func, *args, **kwargs)

    setattr(Vector, name, mapped)


string = "".__class__
_add_map(string.expandtabs, "expandtabs")
_add_map(string.strip, "strip")
_add_map(string.lower, "lower")
_add_map(string.replace, "replace")


###########################################################################
# ADD EXISTING VECTOR OPERATIONS
###########################################################################


def _extend_vector(func, name):
    # add vector operation to Vector
    def vect(self):
        def output():
            for v in func(self):
                yield (v,)

        return Vector(output)

    setattr(Vector, name, vect)


_extend_vector(sorted, "sort")
_extend_vector(reversed, "reverse")


def _lazy(list):
    def output():
        for i in list:
            yield (i,)

    return output


###########################################################################
# ENTER VECTOR MODE
###########################################################################

def vector(list):
    return Vector(_lazy(list))


def items(data):
    def output():
        for k, v in data.items():
            yield [v, k]

    return Vector(output)


