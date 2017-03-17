from __future__ import division
import os, sys, commands
from fnmatch import fnmatch
print "Usage: pyhton <result folder>"

result = sys.argv[1]

outfolder = result + '_tput.out'
out = open(outfolder,'w') 

src = [8, 16, 5, 9, 15]
dst = [19, 20, 7, 14, 17]

for i in xrange(1, 6):
	for j in xrange(0, len(src)):
		myfile = result + "/run000" + str(i) + '/dcn' + str(src[j]) + '-' + 'dcn' + str(dst[j])
		print myfile
		throw = 2
		lcount = 0
		care = 0
		avg = 0.0
		for line in open(myfile, 'r'):
			line = line[:-1]
			lcount += 1
			if lcount <= throw + 1:
				continue
			else:
				if care < 5:
					care += 1
					words = line.split()
					#print words
					avg += float(words[6])
		out.write('%f\n'%(avg/5))

out.close()
