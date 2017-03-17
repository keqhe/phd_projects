import networkx as nx
from  topoBase import *

class FatTree(TopoBase):
	
  pods = None


  def __init__(self, k, serverUplink, edgeUplink, aggUplink): # k number of ports on each switch

    if k%2 is not 0:
      print "ERROR; k should be even"
      return
    startIndex = 0	
    self.edgeSWs = range (startIndex, startIndex + k*k/2)
    startIndex = k/2*k
    self.aggSWs  = range (startIndex, startIndex + k*k/2)
    startIndex = startIndex + k/2*k
    self.coreSWs = range (startIndex, startIndex + pow(k/2,2))
    startIndex = startIndex + pow(k/2,2)
    self.hosts    = range(startIndex, startIndex + ((k/2)*len(self.edgeSWs)))

    self.serverUplink=serverUplink
    self.edgeUplink=edgeUplink
    self.aggUplink=aggUplink



    self.pods = { }

    # dividing edge and agg switches in pods

    i = 0
    swNumber = 1
    for sw in self.edgeSWs:
      if i not in self.pods:
        self.pods[i] = []	
      self.pods[i].append(sw)
      if (swNumber  % (k/2) == 0) and (swNumber !=0):
        i = i +1			
      swNumber = swNumber +1
		

    i = 0
    swNumber = 1
    for sw in self.aggSWs:
      if i not in self.pods:
				self.pods[i] = []	
      self.pods[i].append(sw)
      if (swNumber  % (k/2) == 0) and (swNumber !=0):
				i = i +1			
      swNumber = swNumber +1
		

    self.topo = nx.DiGraph()

    self.topo.add_nodes_from(self.edgeSWs, type = 'edge', rules=0)	
    self.topo.add_nodes_from(self.aggSWs,  type = 'agg', rules=0)
    self.topo.add_nodes_from(self.coreSWs, type = 'core', rules=0)
    self.topo.add_nodes_from(self.hosts,   type = 'host', rules=0)
    
    
    self.topo.add_edges_from(self.agg_edge_edges(), type = 'edge-agg')
    self.topo.add_edges_from(self.core_agg_edges(k), type = 'agg-core')
    self.topo.add_edges_from(self.edge_host_edges(), type = 'host-edge')
    
    self.resetLinkCap()
    self.verifyPorts(k)
    
    self.plotTopo(self.topo)


  '''
    this method set the link cap to max
  '''  
  def resetLinkCap(self):

    for e in self.topo.edges():
      
      if self.topo.edge[e[0]][e[1]]['type'] == 'edge-agg':
        self.topo.edge[e[0]][e[1]]['cap'] = self.edgeUplink
      elif self.topo.edge[e[0]][e[1]]['type'] == 'agg-core':
        self.topo.edge[e[0]][e[1]]['cap'] = self.aggUplink
      elif self.topo.edge[e[0]][e[1]]['type'] == 'host-edge':
        self.topo.edge[e[0]][e[1]]['cap'] = self.serverUplink
        
    for n in self.topo.nodes():        
        self.topo.node[n]['rules'] = 0


  '''
    returns edges between edge and agg switch
  '''
  def agg_edge_edges(self):
    edges = []
    for i in self.pods:
      for src in range(len(self.pods[i])/2):
        for dst in range(len(self.pods[i])/2,len(self.pods[i])):
          pod = self.pods[i]
          edges.append((pod[src],pod[dst]))
          edges.append((pod[dst],pod[src]))
    return edges
	


  '''
    returns edges between core and agg switch
  '''	
  def core_agg_edges(self, k):	
    edges = []
    offset  = 0
    
    for c in range(len(self.aggSWs)):
      for i  in range(k/2):
         
        edges.append((self.aggSWs[c],self.coreSWs[offset + i] ))
        edges.append((self.coreSWs[offset + i] ,self.aggSWs[c]))
        
      offset = offset + (k/2)  
      if offset >= len(self.coreSWs):
        offset = 0
    return edges
		


  '''
    returns edges between edge switch and host 
  '''
	
  def edge_host_edges(self):
		edges = []
		k = len(self.hosts)/len(self.edgeSWs)

		for i  in range(0,len(self.edgeSWs)):
		  for h in range(i*k,(i*k)+k):
  			edges.append((self.hosts[h],self.edgeSWs[i]))
  			edges.append((self.edgeSWs[i],self.hosts[h]))
		return edges				
		


  '''
  This method verifies that  each switch has k number of ports (Fat Tree test)
  '''
  def verifyPorts(self,k):
  
    deg = nx.degree(self.topo)
    for node in self.topo.nodes():
      if self.topo.node[node]['type'] != 'host' and deg[node] != k*2 :
        print "ERROR: switch,",node ," has more than ",k, "ports"
  


  '''
    This method draw the topology
    Some code in this method is copied from mininet
  
  '''
  def plotTopo(self, topo):
    import matplotlib.pyplot as plt
  
    layers = {1:self.aggSWs,0:self.coreSWs,2:self.edgeSWs,3:self.hosts}    
    
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

