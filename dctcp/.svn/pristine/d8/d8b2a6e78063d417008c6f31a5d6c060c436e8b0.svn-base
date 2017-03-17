#!/usr/bin/python
import random
import subprocess
import argparse
import os
import time


sw1 = "10.82.64.1"
sw2 = "10.82.64.2"
sw3 = "10.82.64.3"
sw4 = "10.82.64.4"
sw5 = "10.82.64.5"

switches = [sw3]
#
# flow[i] is src[i] sending to dst[i]
#
src = [8, 16, 5, 9, 15]
dst = [19, 20, 7, 14, 17]
			
CONGESTION_PORT = 64

#logs into arldcnX and kills nuttcp
def kill_nuttcp(X):
	os.system("ssh arldcn%d sudo killall -9 nuttcp"%(X))
def kill_sockperf(X):
        os.system("ssh arldcn%d sudo killall -9 sockperf"%(X))
# this function kills nuttcp everywhere, then does a ten second transfer 
def start_flows(args, run):
	for cl in src + dst:
		kill_nuttcp(cl)
		kill_sockperf(cl)
	####
        for sw in switches:
                os.system("/power/home/keq/workloads/program/acdctcp/get_drops.exp %s %d > %s/run%04d/sw-before-%s"%(sw, CONGESTION_PORT, args.dir, run, sw))
	#start servers
	for d in dst:
		os.system("ssh arldcn%d nuttcp -S"%d)
	
	for d in dst:
                os.system("ssh arldcn%d /power/home/erozner/sockperf-2.5.241/target/bin/sockperf server -p 8899 --tcp &"%d)

	time.sleep(1)

	#start clients
	for si in range(0,len(src)):
		print "starting nuttcp on server arldcn%d"%(src[si])
		os.system("ssh arldcn%d nuttcp -t -i 1 -T %d 10.0.2.%d > %s/run%04d/dcn%d-dcn%d &"%(src[si],args.exptime,dst[si], args.dir, run, src[si],dst[si]))
	for si in range(0,len(src)):	
		os.system("ssh arldcn%d /power/home/erozner/sockperf-2.5.241/target/bin/sockperf ping-pong  -p 8899 -i 10.0.2.%d -t %d --tcp --pps=100 --full-log /tmp/sockperf.log &"%(src[si],dst[si], args.exptime))
	#sleep for a bit
	time.sleep(args.exptime+5)
	for si in range(0,len(src)):
                cmd = "scp arldcn%d:/tmp/sockperf.log %s/run%04d/sockperf_dcn%d-dcn%d"%(src[si], args.dir, run, src[si],dst[si])
                print cmd
                os.system("scp arldcn%d:/tmp/sockperf.log %s/run%04d/sockperf_dcn%d-dcn%d"%(src[si], args.dir, run, src[si],dst[si]) ); #copy sock log back from each TCP sedner
        time.sleep(1)

	####
        for sw in switches:
                os.system("/power/home/keq/workloads/program/acdctcp/get_drops.exp %s %d > %s/run%04d/sw-after-%s"%(sw, CONGESTION_PORT, args.dir, run, sw))

if __name__ == "__main__":
	# Create the parser and subparsers
	parser = argparse.ArgumentParser(description='Generate a bunch of flows for dumbbell topology, tcp flows.')

	#parser.add_argument('--flows', type=argparse.FileType('r'), required=True, help='Input file, one flow per line.')
	parser.add_argument('--dir', required=True, help='Output directory.')
	parser.add_argument("--runs", required=True, help="How many runs to do", type=int)
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
