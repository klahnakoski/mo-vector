
# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
from mo_json import value2json

from mo_vector import vector

output = (
    vector([3, 2, 1])
        .append(4)
        .sort()
        .limit(10)
)

print(value2json(list(output)))


mystr = "\tDo you like\n\tgreen eggs and ham?"


def function(value):
    return "-" + value


output = (
    vector([mystr])
        .strip()
        .expandtabs()
        .lower()
        .replace("ham", "spam")
        .map(function)
)

print(value2json(list(output)))