
import numpy as nm

class BinPacking():

  trafficMatrix  = None
  graph = None
  allPathsSet = None

  def __init__(self, allPaths, Graph):

    #self.trafficMatrix = trafficMatrix
    self.allPathsSet = allPaths
    self.graph = Graph

  '''
  Bin Packer,  Similar to MircoTE
  '''

  def binPacker(self, inputMatrix):
    tm = nm.empty_like (inputMatrix)
    tm[:] = inputMatrix
    tm =  tm.round()
    perTorTM, tm = self.perTorPairTraffic(tm)
#    print perTorTM.max()
    while(1):
      
      
      i,j = nm.unravel_index(perTorTM.argmax(),perTorTM.shape)
      src = self.graph.S_ToR[i]
      dst = self.graph.S_ToR[j]
      if tm.sum() == 0:
        break

      if dst != src:
        paths =  self.allPathsSet[src][dst]
        
        volToMap = 0
        for k in range(len(tm[i][j])):
          if tm[i][j][k] > 0:
            volToMap = tm[i][j][k]
            tm[i][j][k] = 0
            break
        if volToMap == 0:
          continue
        
        pathIndex, newNMaxEnt = self.graph.selectPath(paths, volToMap)
        
        perTorTM[i][j] = perTorTM [i][j] - volToMap
        if pathIndex != None:
          self.graph.updatePathCap(paths[pathIndex],volToMap)
          self.graph.markNodes(paths[pathIndex])

      else:
        perTorTM[i][j] = 0
        if tm[i][j].sum() > 0:
          for k in range(len(tm[i][j])):    
            tm[i][j][k] = 0



  def binPacker_NMaxEnt(self, inputMatrix, NMaxEnt):
    tm = nm.empty_like (inputMatrix)
    tm[:] = inputMatrix  
    tm =  tm.round()
    newNMaxEnt = NMaxEnt
    perTorTM, tm = self.perTorPairTraffic(tm)

    while(1):
    
      i,j = nm.unravel_index(perTorTM.argmax(),perTorTM.shape)
      src = self.graph.S_ToR[i]
      dst = self.graph.S_ToR[j]

      if tm.sum() == 0:
        break


      if dst != src:
        paths =  self.allPathsSet[src][dst]
        
        volToMap = 0
        for k in range(len(tm[i][j])):
          if tm[i][j][k] > 0:
            volToMap = tm[i][j][k]
            tm[i][j][k] = 0
            break
        if volToMap == 0:
          continue

        pathIndex, newNMaxEnt = self.graph.selectPath(paths, volToMap, newNMaxEnt)      
        perTorTM[i][j] = perTorTM [i][j] - volToMap

        if pathIndex != None:
        # updating edge capacities
          self.graph.updatePathCap(paths[pathIndex],volToMap)
        #installing rules
          self.graph.markNodes(paths[pathIndex])
          
      else:
        perTorTM[i][j] = 0
        if tm[i][j].sum() > 0:
          for k in range(len(tm[i][j])):    
            tm[i][j][k] =0
            

  def perTorPairTraffic(self, tm):

    TM = nm.zeros((tm.shape[0],tm.shape[1]))
    i = 0
    for u in tm:
      j = 0 
      for v in u:
        # sorting flows
        tm[i][j] = -tm[i][j]
        tm[i][j].sort()
        tm[i][j] = -tm[i][j]        
        # total data of ToR pair
        TM[i][j] = v.sum()
        j=j+1
      i = i +1
    return TM,tm

