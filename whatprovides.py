"""
This script provides search for an importing path of a module in the
*PYTHON PATH* of the currently activated virtual environment.

In used idea, it is a some analog of *whatprovides* command of *yum* package manager,
but works with python modules instead of packages.

>>> python whatprovides StringIO
todo Add doctest

Author:
 shmakovpn <shmakovpn@yandex.ru>

Date:
 2020-06-21
"""
import os
import sys
import re
from typing import List, Pattern, Match


class DeclarationType:
    """
    Python declaration type

    Declaration type can be one of this:
     - var: some_variable = some_value
     - def: def some_func(arg, ):
     - class: class SomeClass(SomeParent):

    :param name: a name of a declaration (var, def, class)
    :type name: str
    :param pattern: a pattern to match a declaration in a string
    :type pattern: Pattern
    """

    def __init__(self, name: str, pattern: Pattern):
        self.name = name
        if 'name' not in pattern.groupindex:
            raise RuntimeError(
                '"%s.__init__" pattern "%s" does not contains the "name" group' % (
                    self.__class__.__name__,
                    pattern,
                )
            )
        self.pattern = pattern

    def search(self, line: str) -> str:
        """
        Search in a *line* using *self.pattern*, returns the *name* matching group or an empty string,
        if search was failed

        :param line: a line to search
        :type line: str
        :return: the *name* matching group or an empty string if search was failed
        :rtype str:
        :raises KeyError: This exception raises if search result does not contains the 'name' group
        """
        match: Match = self.pattern.search(line)
        if not match:
            return ''  # returns an empty string if search was failed
        return match.group('name')

#
# #: This types of declaration will be parsed from source code files
# DECLARATION_TYPES = {
#     'var': {
#         'value': 1,
#         'pattern': re.compile(r'^(?P<name>[A-Za-z_][0-9A-Za-z_]*)\s*=\s*[^+*=/-]'),  # matches: name=value
#     },
#     'def': {
#         'value': 2,
#         'pattern': re.compile(r'^def\s+(?P<name>[A-Za-z_][0-9A-Za-z_]*)'),  # matches: def somefunc
#     },
#     'class': {
#         'value': 3,
#         'pattern': re.compile(r'^class\s+(?P<name>[A-Za-z_][0-9A-Za-z_]*)'),  # matches: class Someclass
#     }
# }
#
#
# class Declaration:
#     """
#     Declaration of a name in python
#
#     :param type: a type of a declaration (var, def, class ...)
#     :type type: int
#     """
#
#     def __init__(self, type, name, ):
#
# def filter_declaration(search: str, declarations: Iterable[Tuple[str]], ) -> Generator:
#     """
#     This generator will filter declarations tuple by
#     *search* case insensitive in the name field of each declaration
#     :param search: A part of a name for case insensitive search
#     :param declarations: An iterable of declaration tuples
#     :return:
#     """
#     for declaration in declarations:
#         if (not case_insensitive and (search in declaration[1])) \
#                 or (case_insensitive and (search in declaration[1].lower())):
#             yield declaration
