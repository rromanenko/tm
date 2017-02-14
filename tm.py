#!/usr/bin/env python3

f = open("План работы.txt", "r",encoding="cp1251")

line = f.readlines()
print(line)

f.close()

# if valid_date
# while line in fin:
#	print(line)