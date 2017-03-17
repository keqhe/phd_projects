from __future__ import division 
import os, sys, commands

f1 = sys.argv[1]
f2 = sys.argv[2]
f3 = sys.argv[3]

global count_delays
count_delays = {}

for line in open(f1):
	line = line.strip()
	words = line.split(':')
	#print words
	count = int(words[0]) + 1
	delay = float(words[1])
	count_delays[count] = [delay]
	
#
for line in open(f2):
        line = line.strip()
        words = line.split(':')
	#print words
        count = int(words[0]) + 1
        delay = float(words[1])	
	count_delays[count].append(delay)
	#print count_delays[count]

#
for line in open(f3):
        line = line.strip()
        words = line.split(':')
        count = int(words[0]) + 1
        delay = float(words[1]) 
        count_delays[count].append(delay)


w = open('hp_dec_proactive.txt','w')

for key in count_delays:
	w.write('%d %f %f %f\n' % (key, count_delays[key][0]/1000, count_delays[key][1]/1000, count_delays[key][2]/1000))

w.close()
