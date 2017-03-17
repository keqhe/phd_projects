from __future__ import division
import os, sys, commands

f1 = sys.argv[1]
f2 = sys.argv[2]
f3 = sys.argv[3]
f4 = sys.argv[4]
f5 = sys.argv[5]

global cdelay1
cdelay1 = {}

global cdelay2
cdelay2 = {}

global cdelay3
cdelay3 = {}

global cdelay4
cdelay4 = {}

global cdelay5
cdelay5 = {}

#
for line in open(f1):
	line = line.strip()
	words = line.split()
	c = int(words[0])
	delay = float(words[3])
	cdelay1[c] = delay

#
for line in open(f2):
        line = line.strip()
        words = line.split()
        c = int(words[0])
        delay = float(words[3])
        cdelay2[c] = delay

#
for line in open(f3):
        line = line.strip()
        words = line.split()
        c = int(words[0])
        delay = float(words[3])
        cdelay3[c] = delay
#
for line in open(f4):
        line = line.strip()
        words = line.split()
        c = int(words[0])
        delay = float(words[3])
        cdelay4[c] = delay
#
for line in open(f5):
        line = line.strip()
        words = line.split()
        c = int(words[0])
        delay = float(words[3])
        cdelay5[c] = delay


global cdelay
cdelay = {}


keys = cdelay1.keys() #using the fist file
keys.sort()

for k in cdelay1:
	cdelay[k] = (cdelay1[k] + cdelay2[k] + cdelay3[k] + cdelay4[k] + cdelay5[k]) / 5

keys = cdelay.keys()
keys.sort()

#last = 0.0
#for k in cdelay:
#	cdelay[k] = last + cdelay[k]
#	last = cdelay[k]

w = open('BCM_same_rate200_acc_outbound.txt','w')

for k in keys:
		w.write('%d %f\n' % (k, cdelay[k]))	
w.close()
	
