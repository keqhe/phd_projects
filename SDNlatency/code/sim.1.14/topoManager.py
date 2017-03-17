#####################################################
#	Converts the Topology in to switch only topo
#	keeps a list of S_TOR and SW
#
#	Author: Junaid Khalid
#####################################################


import networkx as nx


'''
  Raw Graph includes all the host nodes.
  It assumes that host node only has single uplink
  based on that it identifies the Hosts and ToR switches
'''

class TopoManager:

  topo = None
  S_ToR = None
  S = None
  hosts = None
    
    
  def __init__(self):
    self.topo = nx.DiGraph()
  '''
    gets a graph of typr nx.Graph
    fills the list of hosts and tor switches
  '''
  def addRawGraph(self, graph):
    self.topo = graph
    self.hosts = self.getHosts()
    self.S_ToR = self.getTorSwitch()
    self.removeHosts()
    self.S = self.topo.nodes()
    
  '''
    Identifies the host based on degree
    degree 1 means its a host
  '''
  def getHosts(self):

    hosts = []
    deg = nx.degree(self.topo)

    for n in self.topo.nodes():
      if deg[n] == 1:
        hosts.append(n)
      elif len(self.topo.neighbors(n)) == 1:
        hosts.append(n)
    return hosts

  '''
    Based on hosts, it identifies the TOR switches
  '''
  def getTorSwitch(self):
    S_ToR = []
    hosts = self.getHosts()
    for h in hosts:
      sw = self.topo.neighbors(h)
      if len(sw) is not 1:
        print "ERROR: host has more than one uplink"
      else:
        if sw[0] not in S_ToR:
          S_ToR.append(sw[0])
    return S_ToR

  '''
    Remove all the hosts from the graph
  '''
  def removeHosts(self):
    hosts = self.getHosts()
    self.topo.remove_nodes_from(hosts)
    
    
  def pathFreeSpace(self,path):
    
    edges = self.topo.edge
    min = edges[path[0]][path[1]]['cap']
    for index in range(len(path) -1):
      if edges[path[index]][path[index+1]]['cap'] < min:
        min = edges[path[index]][path[index+1]]['cap']
    return min

  def updatePathCap(self, path, vol):
    edges = self.topo.edge

    for index in range(len(path) -1):
      edges[path[index]][path[index+1]]['cap']  =  edges[path[index]][path[index+1]]['cap'] - vol
      if edges[path[index]][path[index+1]]['cap'] < 0:
        print "ERROR: over utilization ", edges[path[index]][path[index+1]]['cap']


  def markNodes(self,path):
    nodes = self.topo.node
    
    for k in path:
      nodes[k]['rules'] = nodes[k]['rules'] + 1

  def maxRuleAtPath(self, path):
  
    nodes = self.topo.node
    maxRules = 0  
    for k in path:
      if maxRules < nodes[k]['rules']:
        maxRules = nodes[k]['rules']
    return maxRules 


  def selectPath(self, paths, vol, NMaxEnt = None):

    pathCap = []
    newNMaxEnt = NMaxEnt

    # sorting based on cap 
    for index in range(len(paths)):
      pathCap.append((index,self.pathFreeSpace(paths[index])))

    pathCap = sorted(pathCap,key=lambda x: x[1],reverse = True)

    if pathCap[0][1] < vol:
      
      print "ERROR: does not have enough space",vol,pathCap[0][1]
      return None, newNMaxEnt

    if NMaxEnt == None:
      return pathCap[0][0],newNMaxEnt
      
    i = 0
    while 1:    
    
      if i >= len(pathCap):
        # increase the NMaxEnt 
        i = 0
        newNMaxEnt = newNMaxEnt + 1
        
      
      maxRules = self.maxRuleAtPath(paths[pathCap[i][0]])    
      
      if maxRules >= newNMaxEnt:
        i = i + 1
      else:
        break
        
        
    return pathCap[i][0], newNMaxEnt
        
  def maxUtil(self, host = None, edge = None, agg= None):
  
    max = 0.0
    edges = self.topo.edge

    for src in  edges:
      for dst in edges[src]:
        if edges[src][dst]['type'] == 'host-edge':
            edgeCap = host
        elif edges[src][dst]['type'] == 'edge-agg':
            edgeCap = edge
        elif edges[src][dst]['type'] == 'agg-core':
            edgeCap = agg
        elif edges[src][dst]['type'] == 'edge-core':
            edgeCap = edge
        if max < float((edgeCap - edges[src][dst]['cap']))/edgeCap:
          max =float((edgeCap - edges[src][dst]['cap']))/edgeCap    
    return max        
        
   
  def maxRules(self):
  
    nodes = self.topo.node
    maxRules = 0  
    typee = None
    for k in nodes:
      if maxRules < nodes[k]['rules'] and nodes[k]['type'] != 'edge':
        maxRules = nodes[k]['rules']
        typee = nodes[k]['type']
    
    return maxRules,typee
        

  '''
    this method set the link cap to max
  '''
  def resetLinkCap(self, edgeUplink = None, serverUplink = None, aggUplink = None):

    for e in self.topo.edges():

      if self.topo.edge[e[0]][e[1]]['type'] == 'edge-core':
        self.topo.edge[e[0]][e[1]]['cap'] = edgeUplink
      elif self.topo.edge[e[0]][e[1]]['type'] == 'host-edge':
        self.topo.edge[e[0]][e[1]]['cap'] = serverUplink
      elif self.topo.edge[e[0]][e[1]]['type'] == 'edge-agg':
        self.topo.edge[e[0]][e[1]]['cap'] = edgeUplink
      elif self.topo.edge[e[0]][e[1]]['type'] == 'agg-core':
        self.topo.edge[e[0]][e[1]]['cap'] = aggUplink
      else:
        print "ERRORR"

    for n in self.topo.nodes():
#        if self.topo.node[n]['type'] == 'core':
#          print self.topo.node[n]
        self.topo.node[n]['rules'] = 0

