import os, sys, commands

f = sys.argv[1]
fw = sys.argv[2]

global cdelay 
cdelay = {}

for line in open(f):
	line = line.strip()
	words = line.split()
	c = int(words[0])
	delay = float(words[3])
	cdelay[c] = delay

w = open(fw, 'w')	
for k in cdelay:
	w.write('%d %f\n' % (k, cdelay[k]))

w.close()

