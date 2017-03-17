import os, sys, commands

if len(sys.argv) < 3:
        print("Usage: python <this_program> <source_file> <ip address>")
        exit()

fn = sys.argv[1]
selfip = sys.argv[2]

lc = 0

cmd = "/power/home/hek/workloads/program/presto/mice-sink 8899 > /dev/null &"
os.system(cmd)

for line in open(fn, 'r'):
        line = line[:-1]
        lc += 1
        #print(line)
        if (line == selfip):
                continue
        cmd = "/power/home/keq/workloads/program/acdctcp/workload-sink %d > /dev/null & " % (6000+lc-1)
        #print(cmd)
        os.system(cmd)
