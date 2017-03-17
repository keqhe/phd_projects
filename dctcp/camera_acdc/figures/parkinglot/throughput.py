from __future__ import division
import os, sys, commands


fname = sys.argv[1]

global vm
vm = {}

lcount = 0
mytotal = 0.0
for line in open(fname, 'r'):
        line = line[:-1]
        no = float(line)
        #print no
        num = int(no)
	lcount += 1
	mytotal += num
        if not(vm.has_key(num)):
                vm[num] = 1
        else:
                vm[num] = vm[num] + 1

total =  0
for key in vm:
        total = total + vm[key]

print 'average tput is', mytotal/lcount

global perc
perc = {}

for key in vm:
        perc[key] = vm[key]/total

keys = perc.keys()
keys.sort()

global cdf
cdf = {}
now = 0.0
for key in keys:
        cdf[key] = perc[key] + now
        now = cdf[key]

keys = cdf.keys()
keys.sort()

wfname = fname + '.cdf'

w=open(wfname,'w')
for key in keys:
        w.write('%d %f\n' % (key, cdf[key]))

w.close()	
