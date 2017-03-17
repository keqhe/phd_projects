from __future__ import division
import os, sys, commands


if (len(sys.argv) < 2):
	print "Usage: python <this program> <syslog file>"
	exit(1)

lcount = 0
syslog = sys.argv[1]

out = open(syslog + '.out', 'w')

ts = 0.0
MSS = 1446
matching = "57318"

order = []

for line in open(syslog, 'r'):
	if (line.find('mydebug') == -1 or line.find(matching) == -1):
		continue
	words = line.split()
       	index1 = line.find('[')
        index2 = line.find(']')
        rawts = line[index1+1:index2] 
        newts = float(rawts)
	#if (newts - ts) >= 0.0001:
	#print newts, ts
	order.append((newts, int(words[11]) / MSS, words[10])) 
	#out.write('%.6f %.2f\n' % ((newts - ts), int(words[11]) / MSS) )
	#ts = newts

myorder = sorted(order, key=lambda x: x[0])

c = 0;
align = 0.0
for i in myorder:
	c += 1
	if c == 1:
		align = i[0]
		out.write('%.6f %.2f %s\n' % (i[0] - align, i[1], i[2]))
	else:
		out.write('%.6f %.2f %s\n' % (i[0] - align, i[1], i[2]))
out.close()
