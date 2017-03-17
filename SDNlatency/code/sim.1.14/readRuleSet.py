import csv
import socket
import struct 
from netaddr import IPNetwork  

from defaultRules import *
def readFile(filename):
    count = 0
    fd = None
    ruleTable =[]
    table={}
    try:    
      fd = open(filename, "rb")
    except:
      print "ERROR: unable to open file"
      return
    reader = csv.reader(fd)
    for row in reader:
      rule = {}
      for item in row:
        pair = item.split("=")
        if pair[0] == 'nw_src' or pair[0] == 'nw_dst':
          if pair[1] != '*':
            pair[1]  = IPNetwork(pair[1]) 
        elif pair[0] == 'tag':
          None 
        else:
          pair[1] = int(pair[1])   
        rule[pair[0]] = pair[1]
        
      ruleTable.append(rule)
      if rule['pid'] not in table:
        table[rule['pid']] = []
      count = count +1
      table[rule['pid']].append(rule)
    print "Input Rules",count   
    defaultRules(table)
    
    

    
    
def ip2int(addr):                                                               
  return struct.unpack("!I", socket.inet_aton(addr))[0]                       


def int2ip(addr):                                                               
  return socket.inet_ntoa(struct.pack("!I", addr))     

if __name__ == "__main__":
   
  readFile("test")




