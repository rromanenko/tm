#!/usr/bin/env python3

from time_management import valid_time
import unittest

class TimeManagementTest(unittest.TestCase):
    def setUp(self):
        self.rand_text = 'SOME other text here'
    
    def test_valid_time(self):
        self.assertEqual( valid_time('01.55 - 02.10 - Б -'), ('Б', 15) )
        self.assertEqual( valid_time('01.55 - 02.10 -'), () )
        self.assertEqual( valid_time('archived it. Set goals'), () )


if __name__ == "__main__":
    unittest.main()