import os, sys

if len(sys.argv) < 4:
        print("Usage: python <this_program> <source_file> <ip address> <exptime>")
        exit()

fn = sys.argv[1]
selfip = sys.argv[2]
exp = int(sys.argv[3])

lc = 0

def getIP(ctlIP):
	num = ctlIP[-1]
	num = int(num)
	pe = ctlIP.rfind('.')
	thrid = ctlIP[pe+1: -1]
	#print "10.1." + str(thrid) + "." + str(num)
	return "10.1." + str(thrid) + "." + str(num)

cmd = "sudo rm -rf /tmp/dcn*-dcn*"
os.system(cmd)

#get port number
port = 0
dest = {}
for line in open(fn, 'r'):
  line = line[:-1]
  #print(line)
  if (line == selfip):
    port = lc
    #print (port, lc, line)
  dest[lc] = getIP(line)
  lc += 1
#print("this server's iperf destination port should be %d" % (6000+port))
if port <= 44:
	for i in range(1, 5):
		index = (port + i) % 45;
		data_dst = dest[index]
		data_src = getIP(selfip)
	
		cmd = "/power/home/keq/workloads/program/acdctcp/iperf-2.0.5/src/iperf -c %s -i 1 -t %d -f m -p %d > /tmp/dcn%s-dcn%s &" % (data_dst, exp, 6000+port, data_src, data_dst)
		#print(cmd)
		os.system(cmd)

	data_dst = dest[47]
	data_src = getIP(selfip)
	cmd = "/power/home/keq/workloads/program/acdctcp/iperf-2.0.5/src/iperf -c %s -i 1 -t %d -f m -p %d > /tmp/dcn%s-dcn%s &" % (data_dst, exp, 6000+port, data_src, data_dst)
	os.system(cmd)
