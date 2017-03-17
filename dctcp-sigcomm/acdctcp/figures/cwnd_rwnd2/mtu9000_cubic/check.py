import os, commands, sys

ts = 0
for line in open("tcpprobe.out", 'r'):
	line = line[:-1]
	words = line.split()
	newts = float(words[0])
	val = int(words[1])

	if newts > ts:
		ts = newts
	else:
		print ts, newts, line
