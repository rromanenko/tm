#!/usr/bin/env python3

''' old version
# coding: Cyrillic
import codecs

fin = codecs.open("План работы.txt",encoding='cp1251')
''''''''''

f = open("План работы.txt", "r",encoding="cp1251")

line = f.readlines()

#for i in line:
#    print (i)

print(line)

f.close()

#line = fin.readline().split()
#print(line)

# if valid_date
# while line in fin:
#	print(line)