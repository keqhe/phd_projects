import os, sys, commands

w = open('phy_ips.txt','w')

for line in open('../ips.txt'):
	line = line[:-1]
	num = line[6:]
	ip = "10.0.2." + num
	w.write("%s\n"%ip)
w.close()
