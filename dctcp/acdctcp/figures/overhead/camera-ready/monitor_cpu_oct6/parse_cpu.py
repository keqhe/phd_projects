from __future__ import division
import os, sys, commands

if len(sys.argv) < 3:
	print "Usgae: python parse_cpu.py <result folder> <runs>"
	exit(1)

result = sys.argv[1]
total = int(sys.argv[2])
sender = 8
receiver = 19

smax = 0
smin = 100
savg = 0

rmax = 0
rmin = 100
ravg = 0

for run in xrange(1, total+1):
	if (run < 10):
		filepath1 = result + '/run000' + str(run) + '/cpustat-dcn' + str(sender) + '.txt'
		filepath2 = result + '/run000' + str(run) + '/cpustat-dcn' + str(receiver) + '.txt'
	else:
		filepath1 = result + '/run00' + str(run) + '/cpustat-dcn' + str(sender) + '.txt'
                filepath2 = result + '/run00' + str(run) + '/cpustat-dcn' + str(receiver) + '.txt'
	#print filepath1
	for line in open(filepath1):
		line = line[:-1]
		if line.find("Average") != -1:
			words = line.split()
			usage = 100 - float(words[7])
			#print usage
			if usage > smax:
				smax = usage
			if usage < smin:
				smin = usage
			print smax, smin, run
			savg += usage

	for line in open(filepath2):
                line = line[:-1]
                if line.find("Average") != -1:
                        words = line.split()
                        usage = 100 - float(words[7])
                        #print usage
                        if usage > rmax:
                                rmax = usage
                        if usage < rmin:
                                rmin = usage
			ravg += usage

print "sender:", savg/total, smax, smin
print "receiver:", ravg/total, rmax, rmin 
