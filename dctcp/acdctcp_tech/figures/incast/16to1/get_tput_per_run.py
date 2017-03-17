import os, sys, commands
from fnmatch import fnmatch
print "Usage: pyhton <result folder>"

result = sys.argv[1]

mycommand = "cat " + result + "/run00*/dcn* | grep RTT | awk '{print $7}'" + '>' + result + '_tput.out' 
os.system(mycommand)
