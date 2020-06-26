#!/usr/bin/env python3

import unittest
from tm.time_management import *


class TimeManagementTest(unittest.TestCase):
    # def setUp(self):
    #     self.app = App(file='/Volumes/untitled/План работы.txt')
    
    def test_valid_time(self):
        self.assertEqual(valid_time('01.55 - 02.10 - Б -'), ('Б', 15))

    def test_valid_time_english_category(self):
        self.assertEqual(valid_time('00.55 - 02.10 - B -'), ('Б', 75))

    def test_valid_time_empty(self):
        self.assertEqual(valid_time('01.55 - 02.10 -'), ())
        self.assertEqual(valid_time('archived it. Set goals'), ())


if __name__ == "__main__":
    unittest.main()
