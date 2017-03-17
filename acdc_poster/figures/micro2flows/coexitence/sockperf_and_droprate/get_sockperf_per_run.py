import os, sys, commands
from fnmatch import fnmatch

print "python get_sockperf_per_run.py <result folder>"
result = sys.argv[1]

mycommand = 'cat ' + result + '/run00*/sockperf_dcn8-dcn19  >' +  result + '_CUBIC_sockperf'
os.system(mycommand)

mycommand = 'cat ' + result + '/run00*/sockperf_dcn16-dcn20  >' +  result + '_DCTCP_sockperf'
os.system(mycommand)
