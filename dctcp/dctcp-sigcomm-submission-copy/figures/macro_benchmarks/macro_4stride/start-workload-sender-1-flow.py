import os, sys
import time

if len(sys.argv) < 5:
        print("Usage: python <this_program> <size (bytes)> <dest ip address> <port> <exptime (second)")
        exit()

size = sys.argv[1]
dip = sys.argv[2]
port = int(sys.argv[3])
exptime = int(sys.argv[4])

time_start = time.time()

while(time.time() < time_start + exptime):
	cmd = '/power/home/keq/workloads/program/acdctcp/workload-sender 1 %s %s %d' % (size,dip, port)
	os.system(cmd)
