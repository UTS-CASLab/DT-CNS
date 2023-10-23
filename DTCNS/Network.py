import numpy as np
import pandas as pd
import networkx as nx
import copy 
import os
import warnings


class Network:
    def __init__(self,Feature,socialDNA,encounterRate=1,NumEdge=None,InteractionCost=0.5,randomInterference=0.01):
        
        if (type(NumEdge) == None) &(type(InteractionCost)==None):
            warnings.warn("NumEdge and InteractionCost cannot be null at the same time.")
        elif (type(NumEdge) == None) &(type(InteractionCost)==None):
            warnings.warn("NumEdge and InteractionCost cannot coexist.")
        else:
            pass 
     
        self.numNodes = Feature.numNodes
        
        Gstart = nx.Graph()
        Gstart.add_nodes_from(list(range(0,self.numNodes)))
     
        self.Graph = Gstart
        self.GraphHistory =[Gstart] 
     
        self.Feature=Feature 
        self.socialDNA = socialDNA
        self.socialDNAHistory = [dict(zip(["pDNA","hDNA"],[self.socialDNA.pDNA,self.socialDNA.hDNA]))]
        self.encounterRate = encounterRate
        self.InteractionCost = InteractionCost 
        self.randomInterference=randomInterference
        self.NumEdge = NumEdge
        

        self.GraphIntensityHistory =[np.zeros([self.numNodes,self.numNodes])]
        self.iterationNum=1

        self.nodeSets =[set([i]) for i in range(self.numNodes)]


    def Formation(self,randomseed):
        np.random.seed(randomseed)

        if self.randomInterference==None:
            UniScorematrixP=[list((self.Feature.feature*self.socialDNA.pDNA.loc[node]*self.socialDNA.pWeight.loc[node]).sum(axis=1)/self.Feature.numFeatures) for node in range(self.numNodes)]
            UniScorematrixH = [list((self.Feature.featureDifferenceDict[node]*self.socialDNA.hDNA.loc[node]*self.socialDNA.hWeight.loc[node]).sum(axis=1)/self.Feature.numFeatureDifferences) for node in range(self.numNodes)] # 
            UniScorematrix = (np.array(UniScorematrixP)+np.array(UniScorematrixH))/4+1/2#+np.random.normal(0,self.randomInterference,int(self.numNodes*self.numNodes)).reshape([self.numNodes,self.numNodes])*(1-np.identity(self.numNodes)) 
        else:
            UniScorematrixP=[list((self.Feature.feature*self.socialDNA.pDNA.loc[node]*self.socialDNA.pWeight.loc[node]).sum(axis=1)/self.Feature.numFeatures) for node in range(self.numNodes)]
            UniScorematrixH = [list((self.Feature.featureDifferenceDict[node]*self.socialDNA.hDNA.loc[node]*self.socialDNA.hWeight.loc[node]).sum(axis=1)/self.Feature.numFeatureDifferences) for node in range(self.numNodes)]
            UniScorematrix = (np.array(UniScorematrixP)+np.array(UniScorematrixH))/4+1/2+np.random.normal(0,self.randomInterference,int(self.numNodes*self.numNodes)).reshape([self.numNodes,self.numNodes])*(1-np.identity(self.numNodes)) 

        np.random.seed(randomseed)
        encounterOrNot = (np.reshape(np.random.uniform(0,1,self.numNodes**2),[self.numNodes,self.numNodes])+np.reshape(np.random.uniform(0,1,self.numNodes**2),[self.numNodes,self.numNodes]).T)/2<=self.encounterRate 

        UniScorematrix = UniScorematrix*encounterOrNot 
        row, col = np.diag_indices_from(UniScorematrix)
        UniScorematrix[row, col] = -10000# -float('inf')
        FinalScorematrix = (UniScorematrix+UniScorematrix.T)/2

        self.UniScorematrix = UniScorematrix 

        
        if type(self.NumEdge)==type(None):
            InteractionMatrix = ((FinalScorematrix>=self.InteractionCost)*(FinalScorematrix>=self.InteractionCost).T)>=1
            interactGraph =nx.from_numpy_array(InteractionMatrix)
        else:
            Imat = np.array([[FinalScorematrix[x,y] if x<y else 0 for x in range(self.numNodes)] for y in range(self.numNodes)])
            Scorelist = list(Imat.reshape([self.numNodes**2]))
            Scorelist.sort(reverse=True)
            NewIntCost = Scorelist[self.NumEdge]
            
            InteractionMatrix = (Imat > NewIntCost)
         
            interactGraph =nx.from_numpy_array(InteractionMatrix)

  
        self.Graph = interactGraph 
        self.InteractionMatrix = InteractionMatrix
        self.GraphHistory.append(self.Graph)
        
        self.GraphIntensity = InteractionMatrix*FinalScorematrix
        self.GraphIntensityHistory.append(self.GraphIntensity)

        


       
    

    def writeHistory(self,saveDir):
        if os.path.exists(saveDir):
            pass
        else:
            os.makedirs(saveDir)
                  
        nx.write_graphml(self.Graph,saveDir+"/Graph.graphml")
       
        pd.DataFrame(self.GraphIntensity).to_csv(saveDir+"/GraphIntensity.csv") 

        self.socialDNAHistory[0]["pDNA"].to_csv(saveDir+"/pDNA.csv")
        self.socialDNAHistory[0]["hDNA"].to_csv(saveDir+"/hDNA.csv") 
        

       





class SocialDNA:

  
    def __init__(self,Feature,pDNA=None,hDNA=None,pWeight=None,hWeight=None):
        self.numNodes = Feature.numNodes
    
        if isinstance(pDNA,type(None))==True:
            self.pDNA = pd.DataFrame(np.zeros([self.numNodes,Feature.numFeatures]),columns = Feature.feature.columns)
        else:
            self.pDNA = pDNA
        
        if isinstance(hDNA,type(None))==True:
            self.hDNA = pd.DataFrame(np.zeros([self.numNodes,Feature.numFeatureDifferences]),columns=Feature.featureDifferenceDict[0].columns)
        else:
            self.hDNA = hDNA



        if isinstance(pWeight,type(None))==True:
            self.pWeight = pd.DataFrame(np.ones([self.numNodes,Feature.numFeatures]),columns = Feature.feature.columns)
        else:
            self.pWeight = pWeight
        
        if isinstance(hWeight,type(None))==True:
            self.hWeight = pd.DataFrame(np.ones([self.numNodes,Feature.numFeatureDifferences]),columns=Feature.featureDifferenceDict[0].columns)
        else:
            self.hWeight=hWeight



        self.pDNAhistory,self.hDNAhistory=[self.pDNA],[self.hDNA]
        #self.pWeighthistory,self.hWeighthistory=[self.pWeight],[self.hWeight]
        

    
 



