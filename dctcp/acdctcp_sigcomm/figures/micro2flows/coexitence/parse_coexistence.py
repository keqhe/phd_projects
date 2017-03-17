#!/usr/bin/python
from __future__ import division
import random
import subprocess
import argparse
import sys,os
import time

src = [8, 16]
dst = [19, 20]

if (len(sys.argv) < 2):
	print "usage: python parse_convergence.py <result folder>"

else:
	result = sys.argv[1]
	for i in xrange(0, len(src)):
		host_file = result + '/' + 'dcn' + str(src[i]) + '-' + 'dcn' + str(dst[i])
		print host_file
		outfile = 'dcn' + str(src[i]) + '-' + 'dcn' + str(dst[i]) + '_tput.dat'
		out = open(outfile, 'w')
		seconds = i*5

		if (i > 0):
                	out.write('%d %f\n' %(seconds, 0))

		for line in open(host_file, 'r'):
			line = line[:-1]
			if line.find('RTT') == -1 and line.find('bps') != -1:
				seconds = seconds + 1
				index1 = line.find('=')
				index2 = line.find('Mbps')
				tput = line[index1+1:index2-1]
				#print float(tput)		
				tput = float(tput)/1000
				#print tput
				out.write('%d %f\n'%(seconds, tput))
		if (i > 0):
			out.write('%d %f\n' %(seconds+1, 0))
		out.close()
