"""
This script provides tests for 'whatprovides' project

Author:
 shmakovpn <shmakovpn@yandex.ru>

Date:
 2020-06-21
"""
import re
import unittest
from typing import Pattern, List
from whatprovides import DeclarationType


class TestWhatprovides(unittest.TestCase):
    def setUp(self) -> None:
        self.declaration_types: List[DeclarationType] = [
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

    def test_declaration_type_init(self):
        try:
            self.declaration_types.append(
                DeclarationType(
                    name='wrong_pattern',
                    pattern=re.compile(r'^pattern withot the "name" group')
                )
            )
            self.assertTrue(False, f"Checking for wrong pattern failed")
        except RuntimeError as e:
            print(f"Checker for wrong pattern works! '{e}' was caught")
        line_var: str = 'some_var = "some value"'
        self.assertEqual(self.declaration_types[0].search(line=line_var), 'some_var')

    def test_declaration_type_search(self):
        #todo

#     def test_a(self):
#         def countdown_gen(n):
#             x = n
#             while x > 0:
#                 yield x
#                 x -= 1
#
#         print(type(countdown_gen(4)))
#         print(list(countdown_gen(4)))
#
#     def test_list(self):
#         class A:
#             some_list = []
#
#         a1 = A()
#         print(f"a1.some_list={a1.some_list}, {id(a1.some_list)}")
#         a2 = A()
#         print(f"a2.some_list={a2.some_list} {id(a2.some_list)}")
#         a1.some_list.append('hello')
#         print(f"a1.some_list={a1.some_list}, {id(a1.some_list)}")
#         print(f"a2.some_list={a2.some_list} {id(a2.some_list)}")
#
#     def test_search(self):
#         line = 'def some_func(arg1, arg2):'
#         pattern_var: Pattern = re.compile(r'^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s+=[^=]')
#         pattern_def: Pattern = re.compile(r'^def\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)[\s(]')
#         pattern_class: Pattern = re.compile(r'^class\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)[\s:(]')
#         print(pattern_def.search(line).groups())
#         print(pattern_def.search(line).groupdict())
#         pattern_nogroups: Pattern = re.compile(r'def some')
#         if pattern_nogroups.search(line).groups():
#             print('() is not None')  # this must never exec
#         print(f"self.__class__.__name__={self.__class__.__name__}")
#         print(f"pattern_var.groups={pattern_var.groups}")
#         print(f"pattern_var.groupindex={pattern_var.groupindex}")
#         if 'name' in pattern_var.groupindex:
