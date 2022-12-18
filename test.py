import unittest
import pytest
from f_test import actions
from pytest_bdd import feature, scenario, given, when, then
from unittest import TestCase

'''
TDD:
'''
class TestActions(TestCase):
    def test1(self):
        self.assertEqual(actions('СТОП'), 'stopped')

    def test2(self):
        self.assertEqual(actions('два слова'), 'input_error_too_many_words')

    def test3(self):
        self.assertEqual(actions('fhfheifa'), 'input_error_word_does_not_exist')

    def test4(self):
        self.assertEqual(actions('бот%%'), 'input_error_weird_chars')

    def test5(self):
        self.assertEqual(actions('якорь'), 'input_error_ь')

    def test6(self):
        self.assertEqual(actions('ты'), 'input_error_ы')

def main():
    unittest.actions()