from __future__ import division
import os, sys, commands

if len(sys.argv) < 3:
	print "Usgae: python parse_cpu.py <result folder> <runs>"
	exit(1)

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5


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

rr = []
ss = []

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
			#print smin, run
			savg += usage
			ss.append(usage)

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
			rr.append(usage)

print "old way, sender:", savg/total, smax, smin
print "old way, receiver:", ravg/total, rmax, rmin 

print "new way, sender:", mean(ss), pstdev(ss)
print "new way, receiver:", mean(rr), pstdev(rr)
