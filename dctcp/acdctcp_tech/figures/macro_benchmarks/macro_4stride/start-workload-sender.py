import os, sys

if len(sys.argv) < 4:
        print("Usage: python <this_program> <source_file> <self ip address> <transfer size> <exptime>")
        exit()

fn = sys.argv[1]
selfip = sys.argv[2]
size = int(sys.argv[3])
exptime = int(sys.argv[4])

lc = 0

cmd = "sudo rm -rf /tmp/*dcn*-dcn*"
os.system(cmd)

port = 0
dest = {}

def getIP_phy(hostname):
        num = hostname[6:]
        return "10.0.2." + str(num)


for line in open(fn, 'r'):
  line = line[:-1]
  line = getIP_phy(line)
  #print(line)
  if (line == selfip):
    port = lc
    #print (port, lc, line)
  dest[lc] = line
  lc += 1
#print("this server's iperf destination port should be %d" % (6000+port))
MICEINTER = 100
MICESIZE=16000
MICEPORT=8899
SOCK_DST=dest[(port+8)%17]

cmd = '/power/home/hek/workloads/program/presto/mice-sender %d %d %d %s %d > /tmp/mice-dcn%s-dcn%s &' % (exptime, MICEINTER, MICESIZE, SOCK_DST, MICEPORT, selfip, SOCK_DST)
os.system(cmd)

for i in range(1, 5):
                index = (port + 8 + i) % 17;
                data_dst = dest[index]

                cmd = "python /power/home/keq/workloads/program/acdctcp/macro_4stride/start-workload-sender-1-flow.py %d %s %d %d  > /tmp/background-dcn%s-dcn%s &" % (size, data_dst, 6000+port, exptime, selfip, data_dst)
		os.system(cmd)
