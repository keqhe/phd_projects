from __future__ import division
import os, sys, commands


global delay_count
delay_count = {}

for line in open('flow_delays.txt'):
	line = line.strip()
	word = line.split()
	delay = float(word[2])
	if delay in delay_count:
		delay_count[delay] = delay_count[delay] + 1
	else:
		delay_count[delay] = 1

keys = delay_count.keys()
keys.sort()


global delay_CDF
delay_CDF = {}

start = 0
for key in keys:
	cur = delay_count[key]
	start += cur
	delay_CDF[key] = start
total = start

keys = delay_CDF.keys()
keys.sort()


w = open('myCDF.txt','w')
for key in keys:
	w.write('%f %f\n' % (key, delay_CDF[key]/total))

w.close()
	
	
