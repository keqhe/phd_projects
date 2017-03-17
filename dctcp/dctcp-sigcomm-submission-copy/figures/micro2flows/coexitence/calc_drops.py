#!/usr/bin/python
import argparse
import sys
import re
import string

# Assumes that get_drops.exp was run twice. Once before and once after the run.
# Need to save the outputs:
#    ./get_drops.exp 10.82.64.5 64 > after.port64
#
# Then feed the saved output (before and after) to this script:
#    ./calc_drops.py before.port64 after.port64
#
#UcastPkts:                 239953437             1546986166

beforedrops = [0]*65
afterdrops = [0]*65
beforepkts = [0]*65
afterpkts = [0]*65


#helper function
def _removeNonAscii(s):
	return ''.join(filter(lambda x: x in string.printable, s)) #"".join(i for i in s if ord(i)<128)

#there is some non-ascii in the expect output, so we need to remove it here
def clean_line(h):
        h = _removeNonAscii(h)
        m = re.match("(.*)Press(.*)continue\[0m(.*)", h)
        if (m):
#               print "got bad line\n"
                h =  m.group(3).strip()
        else:
                h = h.strip()
        return h	


def get_before(args):
    for h in args.before:
        line = clean_line(h)
#        print line	
	m = re.match("Interface statistics for port (.*):", line)
	if (m):
		port = int(m.group(1))
		#print line
#		print "got port %s"%(port)

#UcastPkts:                 239953437             1546986166
	p = re.match("UcastPkts:( *)([0-9]*)( *)([0-9]*)", line)
	if (p):
#		print "port %d UCAST %s"%(port, p.group(4))
		pkts = int(p.group(4).strip())
		beforepkts[port] = pkts

	n = re.match("VLAN Discards: (.*)       HOL-blocking Discards: (.*)", line)
	if (n):
		drops = int(n.group(2).strip())
		#print line
#		print "got drops %d"%(drops)
		beforedrops[port] = drops

def get_after(args):
    for h in args.after:
        line = clean_line(h)
#        print line
        m = re.match("Interface statistics for port (.*):", line)
        if (m):
                port = int(m.group(1))
                #print line
#                print "got port %s"%(port)

        p = re.match("UcastPkts:( *)([0-9]*)( *)([0-9]*)", line)
        if (p):
#               print "port %d UCAST %s"%(port, p.group(4))
                pkts = int(p.group(4).strip())
                afterpkts[port] = pkts

        n = re.match("VLAN Discards: (.*)       HOL-blocking Discards: (.*)", line)
        if (n):
                drops = int(n.group(2).strip())
                #print line
#                print "got drops %d"%(drops)
                afterdrops[port] = drops

def calc_drops():
	for i in range(1,65):
		drops = afterdrops[i] - beforedrops[i]
		pkts = afterpkts[i] - beforepkts[i]
		if (drops > 0):
			print "port %d pkts %d drops %d"%(i,pkts,drops)
			
##customer-ed by keqiang
def calc_drops_64():
        	i = 64
                drops = afterdrops[i] - beforedrops[i]
                pkts = afterpkts[i] - beforepkts[i]

		if afterdrops[i] < beforedrops[i] or afterpkts[i] < beforepkts[i]:
			print "counter overflow encountered"
                else:
                        print "port %d pkts %d drops %d"%(i,pkts,drops)

def get_drops(args):
	get_before(args)
	get_after(args)

	calc_drops_64()

#
# main method
#
def main():
    # Create the parser and subparsers
    parser = argparse.ArgumentParser(
        description='Calculate drops')
#    subparsers = parser.add_subparsers()
    # The hosts can either be generated or come from a file
    parser.add_argument('--before', type=argparse.FileType('r'), \
                        required=True, help='Drops file from before')
    
    #The hosts can either be generated or come from a file	
    parser.add_argument('--after', type=argparse.FileType('r'), \
                        required=True, help='Drops file from after')

    # Parse the arguments
    args = parser.parse_args()

    get_drops(args)



if __name__ == "__main__":
    main()
