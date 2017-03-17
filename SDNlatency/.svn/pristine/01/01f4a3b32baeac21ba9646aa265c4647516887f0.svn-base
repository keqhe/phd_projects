from __future__ import division
import math
import numpy
import os, sys, commands

home = sys.argv[1]
global B_delay
B_delay = {}

for dirname in os.listdir(home):
	if 'B' in dirname:# each dir has a 'B'
		indexB = dirname.find('B')
		bSize = int(dirname[indexB+1 :])
		print dirname, 'bSize is', bSize
		bVec = [] # for each dir, this vector needs to be re-initialized
		for filename in os.listdir(dirname):
			if '.txt' in filename: #real data file
				cur_file = dirname + '/' + filename
				max_delay = -1.0 #max delay in each file
				for line in open(cur_file):
					line = line.strip()
					words = line.split(' ')
					if float(words[3]) > max_delay:
						max_delay = float(words[3])
				#now you get the completion time
				bVec.append(max_delay)
		#get mean, max, min, std of bVec
		mean = sum(bVec)/len(bVec)
		maxi = max(bVec)
		mini = min(bVec)
		std = numpy.std(bVec)
		print bVec
		B_delay[bSize] = (mean, maxi, mini, std)

keys = B_delay.keys()
keys.sort() #sort on burst sieze


w = open('Intel_burst_effect.txt','w')
for b in keys:
	print b, B_delay[b]
	vec = B_delay[b]
	w.write('%d %f %f %f %f\n' % (b, vec[0], vec[1], vec[2], vec[3])) # mean, max, min, and std

w.close()
					
					
