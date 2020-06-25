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
from typing import List, Pattern, Match, Iterator, Generator


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


#: types of declaration used in python code (e.g. variables, function, classes)
declaration_types: List[DeclarationType] = [
    DeclarationType(
        name='var',
        pattern=re.compile(r'^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s+=[^=]'),
    ),
    DeclarationType(
        name='def',
        pattern=re.compile(r'^def\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)[\s(]'),
    ),
    DeclarationType(
        name='class',
        pattern=re.compile(r'^class\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)[\s:(]'),
    ),
]


class Declaration:
    """
    Declaration of a name in python

    :param declaration_type: a type of a declaration (variable, def, class ...)
    :type declaration_type: DeclarationType
    :param name: a name of a variable or a function or a class
    :type name: str
    :param module_path: a path to python_module where the declaration was found
    :type module_path: str
    """

    def __init__(self, declaration_type: DeclarationType, name: str, module_path: str):
        self.declaration_type = declaration_type
        self.name = name
        self.module_path = module_path


def filter_declaration(search: str, declarations: Iterator[Declaration], ) -> Generator[Declaration]:
    """
    This generator will filter declarations by name of declaration
    case sensitive

    :param search: A part of a name for case sensitive search
    :type search: str
    :param declarations: An iterable of declarations
    :type declarations: Iterator[Declaration]
    :return: generator of filtered declarations
    :rtype: Generator[Declaration]
    """
    for declaration in declarations:
        if search in declaration.name:
            yield declaration


def ifilter_declaration(search: str, declarations: Iterator[Declaration], ) -> Generator[Declaration]:
    """
    This generator will filter declarations by name of declaration
    case insensitive
    :param search: A part of a name of case insensitive search
    :type search: str
    :param declarations: An iterable of declarations
    :type declarations: Iterator[Declaration]
    :return: generator of filtered declarations
    :rtype: Generator[Declaration]
    """
    search_lower: str = search.lower()
    for declaration in declarations:
        if search_lower in declaration.name.lower():
            yield declaration


def re_filter_declaration(search: Pattern, declarations: Iterator[Declaration], ) -> Generator[Declaration]:
    """
    This generator will filter declarations by name if declaration
    using the compiled regular expression
    :param search: a pattern to match name of declaration
    :type search: Pattern
    :param declarations: An iterable of declarations
    :type declarations: Iterator[Declaration]
    :return: generator of filtered declarations
    :rtype: Generator[Declaration]
    """
    for declaration in declarations:
        if search.search(declaration.name):
            yield declaration


class FileLine:
    """
    A line of a file

    :param file_path: A path to a file contains this line
    :type file_path: str
    :param line_number: A number of this line
    :type line_number: int
    :param line: a content of this line
    :type line: str
    """
    def __init__(self, file_path: str, line_number: int, line: str):
        self.file_path: str = file_path
        self.line_number: int = line_number
        self.line: str = line


def get_declarations(lines: Iterator[FileLine]) -> Generator[Declaration]:
    """
    This generator creates instances of declaration
    from lines of code which contains declaration of variables or functions or classes

    :param lines: an iterable of lines of code
    :type lines: Iterator[FileLine]
    :return: a generator of instances of declaration
    :rtype: Generator[Declaration]
    """
    for line in lines:
        for declaration_type in declaration_types:
            declaration_name: str = declaration_type.search(line=line.line)
            if declaration_name:
                yield Declaration(
                    declaration_type=declaration_type,
                    name=declaration_name,
                    module_path=line.file_path,
                )
                break


def get_file_lines(file_paths: Iterator[str]) -> Generator[FileLine]:
    """
    This generator creates instances of a line of a file
    from paths to files

    :param file_paths: An iterable of file paths
    :type file_paths: Iterator[str]
    :return: a generator of instances of lines of files
    :rtype: Generator[FileLine]
    """
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            line_number = 0
            for line in file:
                yield FileLine(
                    file_path=file_path,
                    line_number=line_number,
                    line=line,
                )
                line_number += 1

