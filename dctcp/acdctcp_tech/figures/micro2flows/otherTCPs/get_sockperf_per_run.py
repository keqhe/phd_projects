import os, sys, commands
from fnmatch import fnmatch

print "python get_sockperf_per_run.py <result folder>"
result = sys.argv[1]

mycommand = 'cat ' + result + '/run00*/sockperf*  >' +  result + '_sockperf'
os.system(mycommand)

