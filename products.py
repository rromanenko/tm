#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 01:49:20 2017

@author: romanromanenko
"""

#def purchase(price_list, money_limit):
#    if (price_list == ())
#        return ()
#    else:
#         or (price_list[0] > money_limit):
#        return (price_list[0],) + purchase(price_list[1:], money_limit-price_list[0])

def purchase(price_list, money_limit):
    for i in range(2**len(price_list)):
        bin_num = "{:0" + str(len(price_list)) + "b}"
        bin_num_list = list(bin_num.format(i))

        purchase_list = []
        for j in range(len(price_list)):
            new_elem = int(bin_num_list[j]) * price_list[j]
            if new_elem:
                purchase_list = purchase_list + [new_elem]

        if sum(purchase_list) <= money_limit:
            print(sum(purchase_list), purchase_list)

#products = [6, 7, 1, 9, 4, 2, 6, 8, 4, 1]
products = [1,3,2]
money_limit = 3
purchase(products, money_limit)

