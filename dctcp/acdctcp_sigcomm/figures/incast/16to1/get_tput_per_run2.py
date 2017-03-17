from __future__ import division
import os, sys, commands
from fnmatch import fnmatch
print "Usage: pyhton <result folder>"

result = sys.argv[1]

outfolder = result + '_tput.out'
out = open(outfolder,'w') 

src = [20, 7, 14, 17, 8, 16, 5, 9, 15, 1, 3, 4, 6, 10, 11, 12]
dst = [19]

for i in xrange(1, 11):
	for j in xrange(0, len(src)):
		if i < 10:
			myfile = result + "/run000" + str(i) + '/dcn' + str(src[j]) + '-' + 'dcn' + str(dst[0])
		else:
			myfile = result + "/run00" + str(i) + '/dcn' + str(src[j]) + '-' + 'dcn' + str(dst[0])
		print myfile
		throw = 2 
		lcount = 0
		care = 0
		avg = 0.0
		for line in open(myfile, 'r'):
			line = line[:-1]
			if line.find("Mbits/sec") == -1:
				continue
			lcount += 1
			if lcount <= throw:
				continue
			else:
				if care < 5:
					care += 1
					words = line.split()
					
					#print words
					#print words[-2]
					avg += float(words[-2])
		if (care != 0):
			out.write('%f\n'%(avg/care))
		else:
			out.write('%f\n'%(avg))

out.close()
