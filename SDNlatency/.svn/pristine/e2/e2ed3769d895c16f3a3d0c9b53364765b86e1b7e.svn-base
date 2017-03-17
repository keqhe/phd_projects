import os, sys, commands

f1 = 'pkt_in_delays_200.txt'
f2 = 'pkt_in_delays_500.txt'
f3 = 'pkt_in_delays_1000.txt'

global pkt_in
pkt_in = {}

global pkt_out
pkt_out = {}


c = 0
for line in open(f1):
	line = line.strip()
	words = line.split()
	c = c + 1
	delay_in = float(words[2])
	pkt_in[c] = [delay_in]

#
c = 0
for line in open(f2):
        line = line.strip()
        words = line.split()
        c = c + 1
        delay_in = float(words[2])
        pkt_in[c].append(delay_in)

#
c = 0
for line in open(f3):
        line = line.strip()
        words = line.split()
        c = c + 1
        delay_in = float(words[2])
        pkt_in[c].append(delay_in)


w1 = open('hp_packet_only_in_delays.txt','w')

for key in pkt_in:
	w1.write('%d %f %f %f\n' % (key, pkt_in[key][0]/1000, pkt_in[key][1]/1000, pkt_in[key][2]/1000))

w1.close()
