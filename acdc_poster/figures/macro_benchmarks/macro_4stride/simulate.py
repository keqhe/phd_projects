import os, sys, commands

m = {}

for i in xrange(0, 17):
	m[i] = []

for i in xrange(0, 17):
	for j in xrange(1, 5):
		dst = (i + 8 + j) % 17
		print dst
		m[dst].append(i)

for k in m:
	print k, m[k] 
