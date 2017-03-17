import os, sys, commands

if len(sys.argv) < 4:
	print "Usage: python <this program> <result file> <start> <interval>"
	exit(1)

result = sys.argv[1]
start = sys.argv[2]
inter = sys.argv[3]

out = open(result + '_' + start + '_' + inter, 'w')

for line in open(result, 'r'):
	line = line[:-1]
	words = line.split()
	ts = float(words[0])
	if ts >= float(start) and ts <= (float(start) + float(inter)):
		out.write('%.6f %s %s\n' % (ts - float(start), words[1], words[2]))
out.close()	
