import os, sys

if len(sys.argv) < 3:
	print("Usage: python <this_program> <source_file> <ip address>")
	exit()

fn = sys.argv[1]
selfip = sys.argv[2]

lc = 0

for line in open(fn, 'r'):
	line = line[:-1]
	lc += 1
	#print(line)
	if (line == selfip):
		continue
	cmd = "iperf -s -p %d > /dev/null & " % (6000+lc-1)
	#print(cmd)
	os.system(cmd)
