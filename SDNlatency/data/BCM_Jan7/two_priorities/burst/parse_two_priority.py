import os, sys, commands

f1 = sys.argv[1]

global cdelay
cdelay = {}

for line in open(f1):
	line = line.strip()
	words = line.split()
	c = int(words[0])
	delay = float(words[3])
	cdelay[c] = delay

keys = cdelay.keys()
keys.sort()

w1 = open('BCM_two_pri_mod_0.txt','w')
w2 = open('BCM_two_pri_mod_1.txt','w')

for k in keys:
	if k % 2 == 0:
		w1.write('%d %f\n' % (k, cdelay[k]))	
	else:
		w2.write('%d %f\n' % (k, cdelay[k]))
w1.close()
w2.close()
	
