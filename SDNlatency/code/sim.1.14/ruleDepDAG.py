import networkx as nx
from netaddr import *

'''Rule Dependencies Direct Acyclic Graph'''

class ruleDepDAG:

  dag = None
  ruleSet = None

  def __init__(self,ruleSet):
    self.dag = nx.DiGraph()
    self.ruleSet = ruleSet
    self.constructDAG()

#
# Checks if IPs are exclusive
#
  def areIPsDep(self,ip1,ip2):
    #print src1,src2
    if ip1 == "*" or ip2 == "*":
      return True
    nip1 = IPNetwork (ip1)
    nip2 = IPNetwork (ip2)
    if nip1 in nip2 or nip2 in nip1:
      return True

    return False

#
# Contruct a DAG based on input rules
#
  def constructDAG(self):
    # TODO: For now just checking SrcIP and DstIP
    for key in self.ruleSet.keys():
      self.dag.add_node(self.ruleSet[key].number, src = self.ruleSet[key].srcIP, dst = self.ruleSet[key].dstIP, prio = self.ruleSet[key].priority, tag = self.ruleSet[key].tag,canOffload = True)
    
    for i in self.dag.node:
      for j in self.dag.node:
        if i != j:
          #print self.areIPsDep(self.dag.node[i]['src'], self.dag.node[j]['src'])
          if self.areIPsDep(self.dag.node[i]['src'], self.dag.node[j]['src']) and self.areIPsDep(self.dag.node[i]['dst'], self.dag.node[j]['dst']) :
            #print self.areIPsDep(self.dag.node[i]['dst'], self.dag.node[j]['dst'])
            if self.dag.node[i]['prio'] > self.dag.node[j]['prio']:
              self.dag.add_edge(i,j)
            elif self.dag.node[j]['prio'] > self.dag.node[i]['prio']:         
              self.dag.add_edge(j,i)
    
    #nx.draw(self.dag)
    #plt.show()

#
# Sanity Checks
#    
  def verifyDAG(self):
    if is_directed_acyclic_graph(self.dag):
      print "DAG"
    else:
      print "ERROR: Not a DAG"

#
# Topological Sort
#  
  def toposort(self):
    return nx.topological_sort(self.dag)
  

