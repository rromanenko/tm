#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 01:38:57 2017

@author: romanromanenko
"""

from time_management import valid_date, valid_time
import unittest

class TMTest(unittest.TestCase):
    def setUp(self):
        self.rand_text = 'SOME other text here'
    
    def test_valid_date(self):
        self.assertEqual( valid_date('THURSDAY'), 'THURSDAY' )
        self.assertEqual( valid_date(self.rand_text), '' )

    def test_valid_time(self):
        self.assertEqual( valid_time('01.55 - 02.10 - Б -'), ('Б', 15) )
        self.assertEqual( valid_time(self.rand_text), () )

#assertTrue, assertRaises

unittest.main()