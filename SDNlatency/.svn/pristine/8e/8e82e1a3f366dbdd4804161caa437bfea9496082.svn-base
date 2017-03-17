import os, sys, commands


global burst
burst = {}
for line in open('sorted_flow_delay.txt'):
	line = line.strip()
	words = line.split()
	count = int(words[0]) + 1
	delay = float(words[1])
	burst[count] = delay

w = open('bcm_burst_simple.txt','w')
for c in burst:
	w.write('%d %f\n' % (c, burst[c]))

w.close()
	
	
