from __future__ import division
import os, sys, commands


if (len(sys.argv) < 2):
	print "Usage: python <this program> <tcpprobe file>"
	exit(1)

lcount = 0
syslog = sys.argv[1]

out = open(syslog + '.out', 'w')

ts = 0.0
MSS = 1446
matching = "10.0.2.8:57318"
snd_una = "0xda81a0be"
start = 0;

order = []
for line in open(syslog, 'r'):
	line = line[:-1]
	if line.find(matching) == -1:
		continue
	word_test = line.split()
	if word_test[1] != matching:
		continue
	words = line.split()
	try:
        	newts = float(words[0])
		order.append((newts, int(words[6]), words[5]))	
		#out.write('%.6f %d %.9f\n' % (newts - ts, int(words[6]), newts) )
	except:
		print "flaot convertion error:", line
myorder = sorted(order, key=lambda x: x[0])

for i in myorder:
	if i[0] <= 5:
		out.write('%.6f %d %s\n' % (i[0], i[1], i[2]))
	else:
		#print i[2]
		pass
out.close()
