from __future__ import division
import os, sys, commands

print "exampleL: python raw_throughput_file number_of_flows"

myfile = sys.argv[1]
n = int(sys.argv[2])

lcount = 0
squre_tillnow = 0.0
sum_tillnow = 0.0

num_jain = 0
total_jain = 0.0

for line in open(myfile,'r'):
	lcount += 1

	line = line[:-1]
	num = float(line)

	squre_tillnow += num*num	
	sum_tillnow += num
	
	if (lcount % n == 0): # need to do jain
		jain = sum_tillnow * sum_tillnow / (n * squre_tillnow)
		
		num_jain += 1
		total_jain += jain
		
		squre_tillnow = 0.0
		sum_tillnow = 0.0

print "jain index is",total_jain/num_jain
	
	
