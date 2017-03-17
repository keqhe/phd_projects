#!/usr/bin/python
import random
import subprocess
import argparse
import os
import time

#TODO: congestion port, sockperf, 

sw1 = "10.82.64.1"
sw2 = "10.82.64.2"
sw3 = "10.82.64.3"
sw4 = "10.82.64.4"
sw5 = "10.82.64.5"

switches = [sw4]
#
# flow[i] is src[i] sending to dst[i]
#
#src = [20, 7, 14, 17, 8, 16, 5, 9, 15, 1, 3, 4, 6, 10, 11, 12]
containers = "/power/home/keq/workloads/program/acdctcp/ips.txt"
src = []
for line in open(containers,"r"):
	line = line[:-1]
	src.append(line)

			
def getIP(ctlIP):
	num = ctlIP[-1]
        num = int(num)
	pe = ctlIP.rfind('.')
	thrid = ctlIP[pe+1: -1]
	#print "10.1." + str(thrid) + "." + str(num)
	return "10.1." + str(thrid) + "." + str(num)

def getIP_phy(hostname):
	num = hostname[6:]
	return "10.0.2." + str(num)
# this function kills nuttcp everywhere, then does a ten second transfer 
def start_flows(args, run):
	#for cl in src + dst:
	#	kill_nuttcp(cl)
	#	kill_sockperf(cl)
	os.system("bash /power/home/keq/workloads/program/acdctcp/call_kill_tools.sh")
	time.sleep(2)
	####
        for sw in switches:
	    for i in xrange(1, 65):
                os.system("/power/home/keq/workloads/program/acdctcp/get_drops.exp %s %d > %s/run%04d/sw-before-%s-port%d"%(sw, i, args.dir, run, sw, i))
	#start servers
	for d in src:
		print "start workload-sink mice-sink on ", d
		cmd = "ssh %s python /power/home/keq/workloads/program/acdctcp/macro_4stride/start-workload-sink.py %s %s &"% (d, containers, d)
		print cmd
		os.system(cmd)

	time.sleep(10)

	#start clients
	#
	for si in range(0,0):
	#for si in range(0,len(src)):
		num = src[si][-1]
		num = int(num)
		num -= 2
		br = 'br' + str(num)
		cmd = 'sudo tcpdump -i %s -s 100 -G 20 -W 1 -w /tmp/wireshark-%s.pcap' % (br, src[si])
		#print cmd
		#os.system('ssh %s %s &'% (src[si], cmd))

	#for d in dst:
        #        os.system("ssh %s sudo tcpdump -i br0 -s 100 -G 20 -W 1 -w /tmp/wireshark-%s.pcap &"%(d,d))
	time.sleep(2)
	exptime = args.exptime 

	for d in src:
		print "start workload-sender, mice-sender on ", d
                os.system("ssh %s python /power/home/keq/workloads/program/acdctcp/macro_4stride/start-workload-sender.py %s %s %d %d &"% (d, containers, getIP_phy(d), 512000000, exptime))
	
	time.sleep(args.exptime+10)

	if run == args.runs:
		os.system("bash /power/home/keq/workloads/program/acdctcp/call_kill_tools.sh")
	time.sleep(5)

	for s in src:
                cmd = "scp %s:/tmp/*dcn*-dcn* %s/run%04d/ &"%(s, args.dir, run)
                print cmd
                os.system(cmd); #copy sock log back from each TCP sedner
        time.sleep(10)

	####
        for sw in switches:
	    for i in xrange(1, 65):
                os.system("/power/home/keq/workloads/program/acdctcp/get_drops.exp %s %d > %s/run%04d/sw-after-%s-port%d"%(sw, i, args.dir, run, sw, i))

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
