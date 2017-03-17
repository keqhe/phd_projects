import os, sys, commands

f1 = sys.argv[1]
f2 = sys.argv[2]
f3 = sys.argv[3]
f4 = sys.argv[4]
f5 = sys.argv[5]
f6 = sys.argv[6]
f7 = sys.argv[7]
f8 = sys.argv[8]
f9 = sys.argv[9]
f10= sys.argv[10]

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

for line in open(f4):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])

        id_delay[number].append(delay)
for line in open(f5):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])

        id_delay[number].append(delay)

for line in open(f6):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])
        id_delay[number].append(delay)

for line in open(f7):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])
        id_delay[number].append(delay)

for line in open(f8):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])
        id_delay[number].append(delay)
for line in open(f9):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])
        id_delay[number].append(delay)
for line in open(f10):
        line = line.strip()
        words = line.split()
        number = int(words[0]) + 1
        delay = float(words[3])
        id_delay[number].append(delay)
keys = id_delay.keys()
keys.sort()
w = open('same_priority_bcm.txt','w')
for key in keys:
	w.write('%d %f %f %f %f %f %f %f %f %f %f\n' % (key, id_delay[key][0],  id_delay[key][1],  id_delay[key][2],  id_delay[key][3],  
	id_delay[key][4],  id_delay[key][5],  id_delay[key][6], id_delay[key][7], id_delay[key][8], id_delay[key][9]))

w.close()
	
