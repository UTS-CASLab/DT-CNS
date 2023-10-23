import numpy as np
import pandas as pd
import networkx as nx
#import math
import heapq
import copy 
import os



class Process:
    def __init__(self,numNodes,infectedSet,infectionRate=0.2,recoveryRate=0.4,InfectionUtilityDiscount=0.2):

        self.numNodes = numNodes
        self.infectionRate = infectionRate
        self.recoveryRate = infectionRate
        self.nodeSet = set(list(range(self.numNodes)))
        self.infectedSet = infectedSet 
        self.healthySet = self.nodeSet.difference(infectedSet)

        self.infectionRateDict = dict(zip(list(range(self.numNodes)),list(np.ones(self.numNodes)*infectionRate)))
   
        self.recoveryRateDict = dict(zip(list(range(self.numNodes)),list(np.ones(self.numNodes)*recoveryRate)))

        self.InfectionUtilityDiscount=InfectionUtilityDiscount
        self.healthStatusHistoryRightAfterSpread = []
        epiData = pd.DataFrame([[0,1] for node in range(self.numNodes)],columns =["infected","healthy"])
        self.healthStatusHistoryRightAfterSpread.append(epiData)
        self.healthStatusHistoryRightAfterRecovery = []
        self.healthStatusHistoryRightAfterRecovery.append(epiData)

    def CalOneStepRisk(self,Graph):

        self.SpreadingRisk = np.array([(1- np.prod([(1-self.infectionRateDict[ObjNode])**np.array([(ObjNode in list(nx.neighbors(Graph,node)))*(ObjNode in self.healthySet)]) for ObjNode in range(self.numNodes)]))*(node in self.infectedSet) for node in range(self.numNodes)])
        self.InfectionRisk = np.array([(1- np.prod([(1-self.infectionRateDict[node])**np.array([(ObjNode in list(nx.neighbors(Graph,node)))*(ObjNode in self.infectedSet)]) for ObjNode in range(self.numNodes)]))*(node in self.healthySet) for node in range(self.numNodes)])
        self.RiskMultiplier = (1-self.SpreadingRisk)*(1-self.InfectionRisk)*(self.InfectionUtilityDiscount**np.array([1 if node in self.infectedSet else 0 for node in range(self.numNodes)]))


    def spread(self,Graph,randomseed,spreadStep=1,epiConditions=None):
        
        for step in range(spreadStep):
            np.random.seed(int(randomseed+step))
            self.CalOneStepRisk(Graph)
            randomNumberlist = list(np.random.uniform(0,1,self.numNodes))
            newinfectedset = set([i for i in range(self.numNodes) if self.InfectionRisk[i]>randomNumberlist[i]])
            self.infectedSet = self.infectedSet.union(newinfectedset)
            self.healthySet = self.healthySet.difference(newinfectedset)
            epiData = pd.DataFrame([[1,0] if node in self.infectedSet else [0,1] for node in range(self.numNodes)],columns =["infected","healthy"])
            self.healthStatusHistoryRightAfterSpread.append(epiData)


    def recover(self,Graph,randomseed,recoverStep=1):
        for step in range(recoverStep):
            np.random.seed(int(randomseed+step))
            randomNumberlist = list(np.random.uniform(0,1,self.numNodes))
            newhealthyset =  set([i for i in range(self.numNodes) if self.recoveryRateDict[i]>randomNumberlist[i]])
            self.infectedSet = self.infectedSet.difference(newhealthyset)
            self.healthySet = self.healthySet.union(newhealthyset)
            epiData = pd.DataFrame([[1,0] if node in self.infectedSet else [0,1] for node in range(self.numNodes)],columns =["infected","healthy"])
            self.healthStatusHistoryRightAfterRecovery.append(epiData)
    
    def writeHistory(self,saveDir,recoveryRecord=True,spreadRecord=True):
      
        epiEnd=max(len(self.healthStatusHistoryRightAfterRecovery),len(self.healthStatusHistoryRightAfterSpread))
        for iteration in range(epiEnd):
            if os.path.exists(saveDir+"/iteration"+str(iteration)):
                pass
            else:
                os.makedirs(saveDir+"/iteration"+str(iteration))
            

        if recoveryRecord==True:
            [self.healthStatusHistoryRightAfterRecovery[iteration].to_csv(saveDir+"/iteration"+str(list(range(epiEnd))[iteration])+"/epiDataAfterRecovery.csv") for iteration in range(len(self.healthStatusHistoryRightAfterRecovery))]
        else:
            pass 
        if spreadRecord == True:
            [self.healthStatusHistoryRightAfterSpread[iteration].to_csv(saveDir+"/iteration"+str(list(range(epiEnd))[iteration])+"/epiDataAfterSpread.csv") for iteration in range(len(self.healthStatusHistoryRightAfterSpread))]
        else:
            pass


