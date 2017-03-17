import os, sys, commands

f1 = sys.argv[1]
f2 = sys.argv[2]
f3 = sys.argv[3]

global id_delay
id_delay = {}

for line in open(f1):
	line = line.strip()
	words = line.split()
	number = int(words[0]) + 1
	delay = float(words[3])
	id_delay[number]  = [delay]

for line in open(f2):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])
        id_delay[number].append(delay)
	#print id_delay[number]
for line in open(f3):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])
        id_delay[number].append(delay)	

keys = id_delay.keys()
keys.sort()
w = open('same_priority_bcm.txt','w')
for key in keys:
	w.write('%d %f %f %f\n' % (key, id_delay[key][0],  id_delay[key][1],  id_delay[key][2]))

w.close()
	
