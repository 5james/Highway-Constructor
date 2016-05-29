#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import itertools
from algorithm import Point

myPoints = []


def is_odd(num):
    return num & 0x1

def readCities():
	mynumbers = []
	for line in sys.stdin:
		new_list = [int(elem) for elem in line.split(',')]
		mynumbers = mynumbers + new_list
	if len(mynumbers) % 2 == 1:
		print mynumbers
		print len(mynumbers)
		print ('Invalid input')
		sys.exit(-1)
	else:
		for i in range(0, len(mynumbers), 2):
			x = mynumbers[i]
			y = mynumbers[i+1]
			myPoints.append(Point(x, y, Point.TYPE_TOWN))

def main():
	readCities()
	for x in myPoints:
		print x


if __name__ == "__main__":
    main()