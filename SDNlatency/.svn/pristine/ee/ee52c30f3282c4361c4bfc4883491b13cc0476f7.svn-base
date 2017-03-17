import networkx as nx
from  topoBase import *

class Tier2(TopoBase):
	

  def __init__(self, n_cores, n_edges, hostPerEdge, serverUplink, edgeUplink): # k number of ports on each switch

    
    startIndex = 0	
    self.edgeSWs = range (startIndex, startIndex + n_edges)
    
    startIndex = n_edges
    self.coreSWs = range (startIndex, startIndex + n_cores)

    startIndex = startIndex + n_cores
    self.hosts    = range(startIndex, startIndex + (hostPerEdge* n_edges))

    self.serverUplink=serverUplink
    self.edgeUplink=edgeUplink

    self.topo = nx.DiGraph()

    self.topo.add_nodes_from(self.edgeSWs, type = 'edge', rules=0)	
    self.topo.add_nodes_from(self.coreSWs, type = 'core', rules=0)
    self.topo.add_nodes_from(self.hosts,   type = 'host', rules=0)
    
    
    self.topo.add_edges_from(self.core_edge_edges(), type = 'edge-core')
    self.topo.add_edges_from(self.edge_host_edges(hostPerEdge), type = 'host-edge')
    self.resetLinkCap()    

    self.verifyCorePorts()
    self.verifyEdgePorts(hostPerEdge)
    self.verifyHostPorts()    
    
#    self.plotTopo(self.topo)


  '''
    this method set the link cap to max
  '''  
  def resetLinkCap(self):

    for e in self.topo.edges():  
      
      if self.topo.edge[e[0]][e[1]]['type'] == 'edge-core':
        self.topo.edge[e[0]][e[1]]['cap'] = self.edgeUplink
      elif self.topo.edge[e[0]][e[1]]['type'] == 'host-edge':
        self.topo.edge[e[0]][e[1]]['cap'] = self.serverUplink
        
    for n in self.topo.nodes():        
        self.topo.node[n]['rules'] = 0



  '''
    returns edges between core and edge switch
  '''	
  def core_edge_edges(self):	
    edges = []
    
    for core in self.coreSWs:
      for edge in self.edgeSWs:
        edges.append((edge, core))
        edges.append((core, edge))    

    return edges
		


  '''
    returns edges between edge switch and host 
  '''
  def edge_host_edges(self,hostPerEdge):

    edges = []
    offset = 0

    for h in range(len(self.hosts)):

      if h % hostPerEdge == 0 and h!=0:
        offset = offset + 1


      edges.append((self.hosts[h],self.edgeSWs[offset]))
      edges.append((self.edgeSWs[offset],self.hosts[h]))
      

    return edges				


  '''
  This method verifies that  ports of core switches
  '''
  def verifyCorePorts(self):
  
    deg = nx.degree(self.topo)
    for node in self.topo.nodes():
      if self.topo.node[node]['type'] == 'core' and deg[node] != len(self.edgeSWs)*2: # 2 is for both directions
        print "ERROR: switch,",node ," does not have  ",len(self.coreSWs)*2, "ports"
  
  '''
  This method verifies that  ports of edge switches
  '''
  def verifyEdgePorts(self, hostPerEdge):
  
    deg = nx.degree(self.topo)
    for node in self.topo.nodes():
      if self.topo.node[node]['type'] == 'edge' and deg[node] != (len(self.coreSWs) + hostPerEdge) *2:
        print "ERROR: switch,",node ," does not have  ",(len(self.coreSWs) + hostPerEdge)*2, "ports"
        print deg[node]


  '''
  This method verifies that  ports of core switch
  '''
  def verifyHostPorts(self):
  
    deg = nx.degree(self.topo)
    for node in self.topo.nodes():
      if self.topo.node[node]['type'] == 'host' and deg[node] != 2:
        print "ERROR: Host,",node ," has invalid number of links"


  '''
    This method draw the topology
    Some code in this method is copied from mininet
  
  '''
  def plotTopo(self, topo):
    import matplotlib.pyplot as plt
  
    layers = {0:self.coreSWs,1:self.edgeSWs,2:self.hosts}    
    
    edge_width = 10
    node_size = 100
    node_color = 'g'
    edge_color = 'b'


    #copied the code f    self.edgeSWs = None
    pos = {} 
    for layer in range(len(layers)):

      v_boxes = len(layers)
      height = 1 - ((layer + 0.5) / v_boxes)

      layer_nodes = layers[layer]
      h_boxes = len(layer_nodes)
      
      for j, dpid in enumerate(layer_nodes):
        pos[dpid] = ((j + 0.5) / h_boxes, height)


    fig = plt.figure(1)
    fig.clf()
    ax = fig.add_axes([0, 0, 1, 1], frameon = False)
    nx.draw_networkx_nodes(topo, pos, ax = ax, node_size = node_size,
                 node_color = node_color, with_labels = True)
    nx.draw_networkx_edges(topo,pos)

    plt.show()
'''
		
if __name__ == "__main__":
    FatTree(6)

'''

