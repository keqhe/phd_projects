import os, sys, commands

f1 = 'pkt_in_100_.txt'
f2 = 'pkt_in_200.txt'
f3 = 'pkt_in_300.txt'
f4 = 'pkt_in_400.txt'
f5 = 'pkt_in_500.txt'

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
	delay_out = float(words[3])
	pkt_in[c] = [delay_in]
	pkt_out[c] = [delay_out]

#
c = 0
for line in open(f2):
        line = line.strip()
        words = line.split()
        c = c + 1
        delay_in = float(words[2])
        delay_out = float(words[3])
        pkt_in[c].append(delay_in)
        pkt_out[c].append(delay_out)

#
c = 0
for line in open(f3):
        line = line.strip()
        words = line.split()
        c = c + 1
        delay_in = float(words[2])
        delay_out = float(words[3])
        pkt_in[c].append(delay_in)
        pkt_out[c].append(delay_out)

#
c = 0
for line in open(f4):
        line = line.strip()
        words = line.split()
        c = c + 1
        delay_in = float(words[2])
        delay_out = float(words[3])
        pkt_in[c].append(delay_in)
        pkt_out[c].append(delay_out)
	
#
c = 0
for line in open(f5):
        line = line.strip()
        words = line.split()
        c = c + 1
        delay_in = float(words[2])
        delay_out = float(words[3])
        pkt_in[c].append(delay_in)
        pkt_out[c].append(delay_out)


w1 = open('hp_packet_in_delays.txt','w')
w2 = open('hp_packet_out_delays.txt','w')

for key in pkt_in:
	w1.write('%d %f %f %f %f %f\n' % (key, pkt_in[key][0]/1000, pkt_in[key][1]/1000, pkt_in[key][2]/1000, pkt_in[key][3]/1000, pkt_in[key][4]/1000))
	w2.write('%d %f %f %f %f %f\n' % (key, pkt_out[key][0]/1000, pkt_out[key][1]/1000, pkt_out[key][2]/1000, pkt_out[key][3]/1000, pkt_out[key][4]/1000))

w1.close()
w2.close()	
