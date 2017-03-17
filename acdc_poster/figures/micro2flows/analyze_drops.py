from __future__ import division
import os, sys, commands
from fnmatch import fnmatch
#/power/home/keq/workloads/program/acdctcp/calc_drops.py --before run0001/sw-before-10.82.64.3 --after run0001/sw-after-10.82.64.3

print "python analyze_drops.py <result folder>"

sw = "10.82.64.3"
#port is specified in calc_drops.py

result = sys.argv[1]

total = 0
drops = 0

for i in xrange(1, 6):
	before_file = result + '/' + 'run000' + str(i) + '/' + 'sw-before-' + sw
	after_file = result + '/' + 'run000' + str(i) + '/' + 'sw-after-' + sw

	(stat, out) = commands.getstatusoutput('python calc_drops.py --before %s --after %s'%(before_file, after_file))
	print stat, out

	index1 = out.find('pkts')
	index2 = out.find('drops')

	#print out[index1 + 5:index2 - 1], out[index2 + 6:]
	total += long(out[index1 + 5:index2 - 1])
	drops += long(out[index2 + 6:])

print "total:", total, "drops", drops, "rate:", drops/total*100
