#!/usr/bin/python
import argparse
import subprocess

#get time between segments (output to file)
#for given interval, output how large of flowlets we have
#mask = "10.5.2.13.5001:"  #nuttcp, sender
#mask = "10.5.2.17.53391:" #scp (13 was sending file to 17 and looked at interval on 17)
#mask = "10.5.2.13.55514:" #scp (17 sending file)
#mask = "10.5.2.13.60124:" #ftp

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Check inter-arrival times of segments for flowlet processing.')
        parser.add_argument('interval', metavar='I', type=float, help='an interval we use for flowlets')
        parser.add_argument('infile', metavar="F", help='input pcap file')
        parser.add_argument('src', metavar='S', type=int, help="Sender of scp. XX of arldcnXX")
        args = parser.parse_args()

#        print "got infile ", args.infile

        mask = "\"IP 10.3.1.%d.ssh\""%(args.src)

#	print "mask is ", mask	
#	print 'tcpdump -tt -r %s 2> /dev/null | grep %s | awk \'{print $1, $NF}\''%(args.infile, mask)
        p = subprocess.Popen('tcpdump -tt -r %s 2> /dev/null | grep %s | awk \'{print $1, $NF}\''%(args.infile, mask), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        prevTime = 0.0
        curFlowletSize = 0
        for line in p.stdout.readlines():
#                print line
                t = float(line.split(" ")[0])
                s = int(line.split(" ")[1])
                if (prevTime > 0 and t - prevTime > args.interval):
                        print "Got time %f and flowlet size %d"%(t,curFlowletSize)
                        curFlowletSize = 0
                curFlowletSize = curFlowletSize + s
                prevTime = t
        retval = p.wait()

        print "Got time 999999 and flowlet size %d"%(curFlowletSize)
