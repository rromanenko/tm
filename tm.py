# coding: Cyrillic
#!/usr/bin/env python3

import codecs

fin = codecs.open('План работы.txt',encoding='cp1251')

line = fin.readline().split()
print(line)

# if valid_date
# while line in fin:
#	print(line)