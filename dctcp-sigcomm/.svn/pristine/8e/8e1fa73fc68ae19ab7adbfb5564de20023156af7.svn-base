#!/usr/bin/python
import numpy as np
import sys
from collections import deque

#
# number of entries are not the same in syslog and tcpprobe
# so instead of using past number of samples, can instead use past time window
#

if (len(sys.argv) != 3):
        print "Usage: <file> <window,sec>"

inf = sys.argv[1]
win = float(sys.argv[2])

#simple moving average over n previous data points
#http://stackoverflow.com/questions/14313510/moving-average-function-on-numpy-scipy
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


tarray = deque([])
warray = deque([])
with open(inf) as fp:
    for line in fp:
	t,w,g = line.rstrip().split()
	t = float(t)
	w = float(w)
	tarray.append(t)
	warray.append(w)

	# we have something in window
	if (t < win):
		continue

	#remove all old entries
	removes = 0
	for i in range(0,len(tarray)-1):
		if (tarray[i] < t-win):
			#delete
			removes = removes + 1
		else:
			break

	for i in range(0,removes):
		tarray.popleft()
		warray.popleft()	
		

	#take average of what's left
	if (len(warray) > 0):
		print t, sum(warray)/len(warray), len(warray),tarray[0]
