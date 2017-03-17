import networkx as nx
from  topoBase import *

class vl2(TopoBase):
	
  def __init__(self, Da, Di, serverUplink=1000): # k number of ports on each switch

    if Da is 0:
      print "ERROR; k should be even"
      return
    self.noOfAggSWs = Di
    self.noOfEdgeSWs = Di * Da / 4
    self.noOfCoreSWs = Da / 2

    startIndex = 0	
    self.edgeSWs = range (startIndex, startIndex + self.noOfEdgeSWs)
    startIndex = self.noOfEdgeSWs
    self.aggSWs  = range (startIndex, startIndex + self.noOfAggSWs)
    startIndex = startIndex + self.noOfAggSWs
    self.coreSWs = range (startIndex, startIndex + self.noOfCoreSWs)
    startIndex = startIndex + self.noOfCoreSWs
    self.hosts    = range(startIndex, startIndex + 20*len(self.edgeSWs))

    self.serverUplink= serverUplink
    self.edgeUplink= serverUplink * 10
    self.aggUplink= serverUplink * 10



    self.topo = nx.DiGraph()

    self.topo.add_nodes_from(self.edgeSWs, type = 'edge', rules=0)	
    self.topo.add_nodes_from(self.aggSWs,  type = 'agg', rules=0)
    self.topo.add_nodes_from(self.coreSWs, type = 'core', rules=0)
    self.topo.add_nodes_from(self.hosts,   type = 'host', rules=0)
    
    
    self.topo.add_edges_from(self.agg_edge_edges(), type = 'edge-agg')
    self.topo.add_edges_from(self.core_agg_edges(), type = 'agg-core')
    self.topo.add_edges_from(self.edge_host_edges(), type = 'host-edge')
    
    self.resetLinkCap()
    #self.verifyPorts(k)
    
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
    y = 0
    noOfAggPorts = self.noOfEdgeSWs * 2 / self.noOfAggSWs
    for src in range(self.noOfEdgeSWs, self.noOfEdgeSWs + self.noOfAggSWs):
      for dst in range(0, noOfAggPorts):
        dst = (dst * noOfAggPorts + y) %  self.noOfEdgeSWs 
        edges.append((src,dst))
        edges.append((dst,src))
      y = y + 1
    return edges
	


  '''
    returns edges between core and agg switch
  '''	
  def core_agg_edges(self):	
    edges = []
    
    for src in range(self.noOfEdgeSWs+self.noOfAggSWs, self.noOfEdgeSWs+self.noOfAggSWs + self.noOfCoreSWs):
      for dst  in range(self.noOfEdgeSWs, self.noOfEdgeSWs+self.noOfAggSWs):
        edges.append((src,dst))
        edges.append((dst,src))
    return edges
	

  '''
    returns edges between edge switch and host 
  '''
	
  def edge_host_edges(self):
    edges = []
    index = self.noOfEdgeSWs+self.noOfAggSWs + self.noOfCoreSWs
    for tor in range(0,len(self.edgeSWs)): 
      for h in range(index,index+20):
        edges.append((h,tor))
        edges.append((tor,h))
      index = index + 20
    return edges				
		

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

