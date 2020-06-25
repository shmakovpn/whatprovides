"""
This script provides tests for 'whatprovides' project

Author:
 shmakovpn <shmakovpn@yandex.ru>

Date:
 2020-06-21
"""
import os
import re
import unittest
from typing import Pattern, List
from whatprovides import DeclarationType, declaration_types, Declaration, filter_declaration, ifilter_declaration, \
    re_filter_declaration, FileLine, get_declarations, get_file_lines


SCRIPT_PATH: str = os.path.basename(os.path.abspath(__file__))


class TestWhatprovides(unittest.TestCase):
    def test_declaration_type_init(self):
        try:
            declaration_types.append(
                DeclarationType(
                    name='wrong_pattern',
                    pattern=re.compile(r'^pattern without the "name" group')
                )
            )
            self.assertTrue(False, f"Checking for wrong pattern failed")
        except RuntimeError as e:
            print(f"Checker for wrong pattern works! '{e}' was caught")
        line_var: str = 'some_var = "some value"'
        self.assertEqual(declaration_types[0].search(line=line_var), 'some_var')

    def test_declaration_type_search(self):
        line_var: str = 'variable_name = "variable value"'
        variable_name: str = declaration_types[0].search(line=line_var)
        self.assertEqual(variable_name, 'variable_name')
        line_def: str = 'def function_name(*args, **kwargs):'
        function_name: str = declaration_types[1].search(line=line_def)
        self.assertEqual(function_name, 'function_name')
        line_class: str = 'class ClassName(ParentClass):'
        class_name: str = declaration_types[2].search(line=line_class)
        self.assertEqual(class_name, 'ClassName')

    def test_filter_declaration(self):
        declarations: List[Declaration] = [
            Declaration(declaration_type=declaration_types[0], name='filtered', module_path=''),
            Declaration(declaration_type=declaration_types[0], name='not_filtered', module_path=''),
        ]
        filtered_declarations: List[Declaration] = list(
            filter_declaration(search='not', declarations=declarations)
        )
        self.assertEqual(len(filtered_declarations), 1)
        self.assertEqual(filtered_declarations[0].name, 'not_filtered')

    def test_ifilter_declaration(self):
        declarations: List[Declaration] = [
            Declaration(declaration_type=declaration_types[0], name='filtered', module_path=''),
            Declaration(declaration_type=declaration_types[0], name='NOT_filtered', module_path=''),
        ]
        filtered_declarations: List[Declaration] = list(
            ifilter_declaration(search='Not', declarations=declarations)
        )
        self.assertEqual(len(filtered_declarations), 1)
        self.assertEqual(filtered_declarations[0].name, 'NOT_filtered')

    def test_re_filter_declaration(self):
        declarations: List[Declaration] = [
            Declaration(declaration_type=declaration_types[0], name='filtered', module_path=''),
            Declaration(declaration_type=declaration_types[0], name='not_filtered_123', module_path=''),
        ]
        filter_declarations: List[Declaration] = list(
            re_filter_declaration(search=re.compile(r'not_[a-zA-Z0-9_]+'), declarations=declarations)
        )
        self.assertEqual(len(filter_declarations), 1)
        self.assertEqual(filter_declarations[0].name, 'not_filtered_123')

    def test_get_declarations(self):
        lines: List[FileLine] = [
            FileLine(file_path='', line_number=1, line='# some comment'),
            FileLine(file_path='', line_number=1, line='variable = "value"'),
            FileLine(file_path='', line_number=1, line='def some_function(*args, **kwargs):'),
            FileLine(file_path='', line_number=1, line='class SomeClass(ParentClass):'),
            FileLine(file_path='', line_number=1, line='x==1'),
            FileLine(file_path='', line_number=1, line='# def filtered_function():'),
            FileLine(file_path='', line_number=1, line='    class Meta:'),
        ]
        declarations: List[Declaration] = list(
            get_declarations(lines=lines)
        )
        self.assertEqual(len(declarations), 3)
        self.assertEqual(declarations[0].name, 'variable')
        self.assertEqual(declarations[0].declaration_type, declaration_types[0])
        self.assertEqual(declarations[1].name, 'some_function')
        self.assertEqual(declarations[1].declaration_type, declaration_types[1])
        self.assertEqual(declarations[2].name, 'SomeClass')
        self.assertEqual(declarations[2].declaration_type, declaration_types[2])

    def test_get_file_lines(self):
        test_path: str = os.path.join(SCRIPT_PATH, 'test')
        file_paths: List[str] = [
            os.path.join(test_path, 'test_data1.py'),
            os.path.join(test_path, 'test_data2.py'),
        ]
        file_lines: List[FileLine] = list(
            get_file_lines(file_paths=file_paths)
        )
        self.assertEqual(len(file_lines), 9)



