from __future__ import division
import math
import numpy
import os, sys, commands

home = sys.argv[1]
global B_delay
B_delay = {}
total = 0
for dirname in os.listdir(home):
	if 'Rate' in dirname:# each dir has a 'B'
		indexB = dirname.find('Rate')
		bSize = int(dirname[indexB+4 :])
		print dirname, 'bSize is', bSize
		bVec = [] #empty for each insertion rate
		for filename in os.listdir(dirname):
			if '.txt' in filename: #real data file
				cur_file = dirname + '/' + filename
				max_delay = -1.0 #default
				total = 0
				for line in open(cur_file):
					line = line.strip()
					words = line.split()
					total += 1
					#now you get the insertion time for each rule
					cur_delay = int(words[0])/bSize*1000 + float(words[3])
					if cur_delay > max_delay:
						max_delay = cur_delay
				bVec.append(max_delay)
		#get mean, max, min, std of bVec
		mean = sum(bVec)/len(bVec)
		maxi = max(bVec)
		mini = min(bVec)
		std = numpy.std(bVec)
		B_delay[bSize] = (mean, maxi, mini, std)

keys = B_delay.keys()
keys.sort() #sort on burst sieze


w = open('bcm_insertion_rate_effects_total.txt','w')
for b in keys:
	print b, B_delay[b]
	vec = B_delay[b]
	w.write('%d %d %f %f %f %f\n' % (b, total, vec[0], vec[1], vec[2], vec[3])) # mean, max, min, and std

w.close()
					
					
