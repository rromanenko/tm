#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 01:49:20 2017

@author: romanromanenko
"""

def purchase(price_list, money_limit):
    if (price_list == ())
        return ()
    else:
         or (price_list[0] > money_limit):
        return (price_list[0],) + purchase(price_list[1:], money_limit-price_list[0])

#def purchase(price_list, money_limit):
#    if price_list:
#        print(money_limit)

#products = (6, 7, 1, 9, 4, 2, 6, 8, 4, 1)
products = (1,3,1)
money_limit = 4

print(purchase(products, money_limit))

