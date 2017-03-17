from __future__ import division
import math
import numpy
import os, sys, commands

home = sys.argv[1]
global B_delay
B_delay = {}

for dirname in os.listdir(home):
	if 'Rate' in dirname:# each dir has a 'B'
		indexB = dirname.find('Rate')
		bSize = int(dirname[indexB+4 :])
		print dirname, 'bSize is', bSize
		bVec = [] #empty for each insertion rate
		for filename in os.listdir(dirname):
			if '.txt' in filename: #real data file
				cur_file = dirname + '/' + filename
				for line in open(cur_file):
					line = line.strip()
					words = line.split()
					#now you get the insertion time for each rule
					bVec.append(float(words[3]))
		#get mean, max, min, std of bVec
		mean = sum(bVec)/len(bVec)
		maxi = max(bVec)
		mini = min(bVec)
		std = numpy.std(bVec)
		B_delay[bSize] = (mean, maxi, mini, std)

keys = B_delay.keys()
keys.sort() #sort on burst sieze


w = open('bcm_insertion_rate_effects.txt','w')
for b in keys:
	print b, B_delay[b]
	vec = B_delay[b]
	w.write('%d %f %f %f %f\n' % (b, vec[0], vec[1], vec[2], vec[3])) # mean, max, min, and std

w.close()
					
					
