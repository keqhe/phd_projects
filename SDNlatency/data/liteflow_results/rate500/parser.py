from __future__ import division
import os, sys, commands
import time



#flow_mod = 'packet_mod_timestamp.txt'
flow_mod = 'raw_packet_timestamp.txt'
fst_out = 'packet_in_timestamp.txt'

global flow_mod_timestamp
flow_mod_timestamp = {}

global fst_out_timestamp
fst_out_timestamp = {}


for line in open(flow_mod):
        line = line.strip()
        words = line.split()
        print words
        srcip = words[1]
        if srcip == '0.0.0.0':
                continue
        dstip = words[3]
        sec = float(words[5])
        usec = float(words[7])
        flow_mod_timestamp[(srcip, dstip)] = (sec, usec)

for line in open(fst_out):
        line = line.strip()
        words = line.split()
        print words
	srcip = words[1]
        if srcip == '0.0.0.0':
                continue
        dstip = words[3]
        sec = float(words[5])
        usec = float(words[7])
        fst_out_timestamp[(srcip, dstip)] = (sec, usec)

w1 = open('flow_delays.txt','w')
count = 0
min_delay = 99999999.0
max_delay = -1.0
total_delay = 0.0
for key in flow_mod_timestamp:
        try:
                #print key, '%f' % packet_in_timestamp[key], pcap_pkt_in[key], '%f' % packet_out_timestamp[key],  pcap_pkt_out[key]
                if key in fst_out_timestamp:
                        count += 1
                        delay = (fst_out_timestamp[key][0] - flow_mod_timestamp[key][0]) * 1000000 + (fst_out_timestamp[key][1] - flow_mod_timestamp[key][1])
                        w1.write('%s %s %f\n' % (key[0], key[1],delay/1000))
                        if min_delay > delay/1000:
                                min_delay = delay/1000
                        if max_delay < delay/1000:
                                max_delay = delay/1000
                        total_delay += delay/1000
        except:
#               #print key
                pass
w1.close()

print 'total rules inserted successfully:' , count
print 'total delay for these rules:', total_delay
print 'avg rule insertion delay:', total_delay/count
print 'max rule insertion delay:', max_delay
print 'min rule insertion delay:', min_delay

global number_val
number_val = {}

for line in open('flow_delays.txt'):
        line = line.strip()
        words = line.split(' ')
        #print words
        dstip = words[1]
        byte = dstip.split('.')
        number = (int(byte[2]) - 56) * 256 + (int(byte[3]) - 0)
        number_val[number] = words

keys = number_val.keys()
keys.sort()

w = open("sorted_flow_delay.txt","w")
for key in keys:
        w.write('%d %s %s %s\n' % ( key, number_val[key][0], number_val[key][1], number_val[key][2]))

w.close()
