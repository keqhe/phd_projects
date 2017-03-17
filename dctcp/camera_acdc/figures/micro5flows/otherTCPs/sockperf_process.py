#!/usr/bin/python

#
# Read in sockperf dump file and plot CDF of latencies
#


import argparse
import sys
import os
import re
import create_cdf

def parse_lat(args):
    latencyTimes = []
    verbose = 0
    for line in args.file:
        match = re.match("(.*), (.*)", line)
        if (match):
            try:
                #the latency is RTT, so have to divide by 2 to get one way
                latency = (float(match.group(2)) - float(match.group(1))) 

                #let's just get usec, and round off
                latency = latency * 1000000
                #print line
                #print latency
                #print int(latency)
               	if (latency > 900):
			print line[:-1]
                #store in array
                latencyTimes.append(int(latency))


            except:
                continue

                
    #make cdf
    sto = "%s.cdf"%(args.file.name)
    cdfTimes = create_cdf.create_cdf(latencyTimes)
    cdfTimes.cdf(sto, verbose)
    


#
# main method
#
def main():
    # Create the parser and subparsers
    parser = argparse.ArgumentParser(
        description='Generate a CDF of latencies from sockperf output.')
    #subparsers = parser.add_subparsers()

    
    parser.add_argument('--file', type=argparse.FileType('r'), \
                        required=True, help='sockperf output file.')
  
    # Parse the arguments
    args = parser.parse_args()
 
    parse_lat(args)

if __name__ == "__main__":
    main()
