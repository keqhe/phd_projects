#!/usr/bin/python
import random
import subprocess
import argparse
import os
import time

#
# flow[i] is src[i] sending to dst[i]
#
src = [8]
dst = [19]
			
#path to programs being used
wpath="/power/home/erozner/workloads/program/acdctcp"
port=5050

#logs into arldcnX and kills nuttcp
def kill_iperf(X):
	os.system("ssh arldcn%d sudo killall -9 iperf nuttcp sockperf workload-sink threaded-sender sar"%(X))

# this function kills nuttcp everywhere, then does a ten second transfer 
def start_flows(args, run):
	for cl in src + dst:
		kill_iperf(cl)
	
	#start servers
	for d in dst:
		os.system("ssh arldcn%d 'sudo chmod 777 -R /tmp/'" %d)
		os.system("ssh arldcn%d '%s/workload-sink %d &> /tmp/sink & '" % (d,wpath,port))	
		os.system("ssh arldcn%d 'sudo rm /tmp/cpustat.txt'" %d)
	
	for s in src:
                os.system("ssh arldcn%d 'sudo chmod 777 -R /tmp/'" %s)
		os.system("ssh arldcn%d 'sudo rm /tmp/cpustat.txt'" %s)
		os.system("ssh arldcn%d 'sudo rm /tmp/*dcn*-flow*'" %s)
	
	#start clients
	exptime = args.exptime
	for si in range(0,len(src)):
		print "starting threader-sender on server arldcn%d"%(src[si])
		os.system("ssh arldcn%d '%s/threaded-sender 10.0.2.%d %d %d > /tmp/dcn%d-dcn%d-flow%d ' &"%(src[si],wpath,dst[si], port, args.flows,src[si],dst[si],args.flows))

	#wait until stable
	time.sleep(2)

	# we do not collect CPU usage for the first and last 2 seconds
	for s in src:
		os.system("ssh arldcn%d 'sar 1 %d > /tmp/cpustat.txt &'" %(s, args.exptime-3))
	for d in dst:
		os.system("ssh arldcn%d 'sar 1 %d > /tmp/cpustat.txt &'" %(d, args.exptime-3))
	#sleep for a bit
	time.sleep(args.exptime)


	#kill everything
        for cl in src + dst:
                kill_iperf(cl)
        
	for d in dst:
                 os.system("scp arldcn%d:/tmp/cpustat.txt %s/run%04d/cpustat-dcn%d.txt"%(d, args.dir, run, d) )

	for s in src:
                 os.system("scp arldcn%d:/tmp/cpustat.txt %s/run%04d/cpustat-dcn%d.txt"%(s, args.dir, run, s) )

	for s in src:
                 os.system("scp -r arldcn%d:/tmp/*dcn*-flow*  %s/run%04d/"%(s, args.dir, run) )

	time.sleep(1)


if __name__ == "__main__":
	# Create the parser and subparsers
	parser = argparse.ArgumentParser(description='Generate a bunch of flows for dumbbell topology, tcp flows.')

	#parser.add_argument('--flows', type=argparse.FileType('r'), required=True, help='Input file, one flow per line.')
	parser.add_argument('--dir', required=True, help='Output directory.')
	parser.add_argument("--flows", required=True, help="How many flows to run", type=int)
	parser.add_argument("--runs", help="How many runs to do", default=1, type=int)
	parser.add_argument("--seed", help="Random seed", default=1, type=int)
	parser.add_argument("--exptime", help="How many secs to run experiemnts", default=10, type=int)
	
    	# Parse the arguments
    	args = parser.parse_args()

    	os.system("mkdir -p %s"%args.dir)
    	print os.path.abspath(args.dir)

	
	#random seed
	random.seed(args.seed)
	
	#populate macs is slow, do it here
	#populate_macs()
	
	for i in range(1,args.runs+1):
		#delete the rules in the switch for our nodes
		#print "Deleting flow mods"
		#delete_flow_mods(args)

		#generate static flow pusher file
		#generate_flow_pusher(args,i)	
	
		#push static flow pusher file
		#os.system("sh %s/run%04d/curl"%(args.dir,i))
		
		rdir = "%s/run%04d"%(args.dir,i)
	        os.system("mkdir -p %s"%(rdir))	
		#start the flows!
		start_flows(args, i)
