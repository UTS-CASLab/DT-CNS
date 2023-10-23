import numpy as np
import pandas as pd
import networkx as nx
import math
import copy 
import os




class Feature:

    def __init__(self,feature):
        self.feature = feature
        self.numNodes = feature.shape[0]#len(feature)
        self.numFeatures = feature.shape[1]
        self.featureNames = feature.columns
        self.nodes = list(range(self.numNodes))

    def CrispRepresentation(self):

        try:
            self.feature = (self.feature-self.feature.min(axis=0))/(self.feature.max(axis=0)-self.feature.min(axis=0)) 
        except:
            self.feature = self.feature*0
        featdiff = copy.deepcopy(self.feature)
        featdiff.columns = [name+" Difference" for name in featdiff.columns]
        self.featureDifferenceDict = dict(zip(self.nodes,[(featdiff - featdiff.loc[node]).abs() for node in self.nodes]))
        self.numFeatureDifferences = self.featureDifferenceDict[0].shape[1]
        self.featureNames = self.feature.columns

        self.NumFuzzyPdict = {}
        self.NumFuzzyHdict = {}
    
        self.FuzzyPparamsDict = {}
        self.FuzzyHparamsDict = {}

    def FuzzyRepresentation(self,NumFuzzyPdict,NumFuzzyHdict,minValue=None,maxValue=None,minDiffValue=None,maxDiffValue=None,FuzzyPparamsDict=None,FuzzyHparamsDict=None):

        self.NumFuzzyPdict =NumFuzzyPdict
        self.NumFuzzyHdict =NumFuzzyHdict
        self.FuzzyPparamsDict = FuzzyPparamsDict 
        self.FuzzyHparamsDict = FuzzyHparamsDict
        self.featureDifferenceDict = dict(zip(self.nodes,[(self.feature - self.feature.loc[node]).abs() for node in self.nodes]))
        
        if type(minValue)==type(None):
            minfeatvalues= self.feature.min(axis=0)
        else:
            minfeatvalues = minValue
        if type(maxValue)==type(None):
            maxfeatvalues = self.feature.max(axis=0)
        else:
            maxfeatvalues = maxValue
        if self.FuzzyPparamsDict ==None:
            ParamsDatalist=[]
            for featurename in self.featureNames:
                Fuzzydata=pd.DataFrame()
                if NumFuzzyPdict[featurename] ==1:
                    Fuzzydata["mu"] = [minfeatvalues[featurename]]
                    Fuzzydata["sigma"]=5
                else:
                    Fuzzydata["mu"] = np.linspace(minfeatvalues[featurename], maxfeatvalues[featurename],num=NumFuzzyPdict[featurename])
                    Fuzzydata["sigma"]=5
                ParamsDatalist.append(Fuzzydata)
            self.FuzzyPparamsDict = dict(zip(self.featureNames,ParamsDatalist))
        else:
            pass             

        if self.FuzzyHparamsDict ==None:
            ParamsDatalist=[]
            for featurename in self.featureNames:
                if (type(minDiffValue)==type(None)):
                    
                    minfeatDiffs= np.min([self.featureDifferenceDict[node][featurename].min(axis=0) for node in range(self.numNodes)])
               
                else:
                    minfeatDiffs = minDiffValue[featurename]
                if (type(maxDiffValue)==type(None)):
                    maxfeatDiffs = np.max([self.featureDifferenceDict[node][featurename].max(axis=0) for node in range(self.numNodes)])
                else:
                    maxfeatDiffs = maxDiffValue[featurename]

                Fuzzydata=pd.DataFrame()         
                if NumFuzzyHdict[featurename] ==1:
                    Fuzzydata["mu"] = [minfeatDiffs]
                    Fuzzydata["sigma"]=5
                else:
                    Fuzzydata["mu"] = np.linspace(minfeatDiffs, maxfeatDiffs,num=NumFuzzyHdict[featurename])
                    Fuzzydata["sigma"]=5
                ParamsDatalist.append(Fuzzydata)
            self.FuzzyHparamsDict= dict(zip(self.featureNames,ParamsDatalist))
        else:
            pass             

        NewFeatureData,featcolumns,featDiffcolumns=[],[],[]
        featureDiffNew = [[] for i in range(self.numNodes)] 

        for featurename in self.featureNames:
            featureNew = [list(np.exp(-(self.feature[featurename]-self.FuzzyPparamsDict[featurename].loc[i,"mu"])**2/(2*self.FuzzyPparamsDict[featurename].loc[i,"sigma"]**2)).values) for i in range(self.NumFuzzyPdict[featurename])]
            NewFeatureData.extend(featureNew)
            featcolumns.extend([featurename+"-Fuzzy"+str(i) for i in range(self.NumFuzzyPdict[featurename])])
            featDiffcolumns.extend([featurename+" Difference-Fuzzy"+str(i) for i in range(self.NumFuzzyHdict[featurename])])
            featureDiffNew=dict(zip(list(range(self.numNodes)),[featureDiffNew[node]+[list(np.exp(-(self.featureDifferenceDict[node][featurename]-self.FuzzyHparamsDict[featurename].loc[i,"mu"])**2/(2*self.FuzzyHparamsDict[featurename].loc[i,"sigma"]**2)).values) for i in range(self.NumFuzzyHdict[featurename])] for node in range(self.numNodes) ]))

        featureDiffNew = dict(zip(list(range(self.numNodes)),[pd.DataFrame(featureDiffNew[node],index=featDiffcolumns).T for node in range(self.numNodes)]))
        NewFeatureData = pd.DataFrame(NewFeatureData,index=featcolumns).T

        self.feature = NewFeatureData
        self.featureDifferenceDict = featureDiffNew#NewFeatureData
        self.numFeatures = self.feature.shape[1]
        self.numFeatureDifferences = self.featureDifferenceDict[0].shape[1]
        self.featureNames = self.feature.columns
        

    def FeatureAppend(self,AnotherFeature):
        self.feature = pd.concat([self.feature,AnotherFeature.feature],axis=1)
        self.numFeatures = self.feature.shape[1]
        self.featureNames = self.feature.columns
        self.featureDifferenceDict = dict(zip(list(range(self.numNodes)),[pd.concat([self.featureDifferenceDict[node],AnotherFeature.featureDifferenceDict[node]],axis=1) for node in range(self.numNodes)]))
        self.numFeatureDifferences = self.featureDifferenceDict[0].shape[1]
        
        self.NumFuzzyPdict.update(AnotherFeature.NumFuzzyPdict)
        self.NumFuzzyHdict.update(AnotherFeature.NumFuzzyHdict)
    
        self.FuzzyPparamsDict.update(AnotherFeature.FuzzyPparamsDict)
        self.FuzzyHparamsDict.update(AnotherFeature.FuzzyHparamsDict)
                                                             
    def FeatureUpdate(self,AnotherFeature,ReplaceFeatures=None):
        if type(ReplaceFeatures)==type(None):
            pass 
        else:                         
            newfeat = copy.deepcopy(self.feature)
            for featurename in self.feature.columns:
                for replacedfeat in ReplaceFeatures: 
                    if replacedfeat in self.NumFuzzyPdict.keys():
                        if (featurename.find(replacedfeat+"-Fuzzy")!=-1):
                            newfeat = newfeat.drop(featurename, axis=1) 
                    else:
                        if featurename == replacedfeat:#(featurename.find(replacedfeat)!=-1):
                            newfeat = newfeat.drop(featurename, axis=1)  
            self.feature = newfeat
            for featureDiffname in self.featureDifferenceDict[0].columns:
                for replacedfeat in ReplaceFeatures: 
                    if replacedfeat in self.NumFuzzyHdict.keys():
                        if featureDiffname.find(replacedfeat+" Difference-Fuzzy")!= -1:
                            [self.featureDifferenceDict.update({node:self.featureDifferenceDict[node].drop(featureDiffname, axis=1)}) for node in self.nodes]
                    else:
                        if featureDiffname == replacedfeat+" Difference":
                            [self.featureDifferenceDict.update({node:self.featureDifferenceDict[node].drop(featureDiffname, axis=1)}) for node in self.nodes]
                            

            
            try:
                [self.NumFuzzyPdict.pop(replacedfeat) for replacedfeat in ReplaceFeatures]
            except:
                pass
            try:
                [self.NumFuzzyHdict.pop(replacedfeat) for replacedfeat in ReplaceFeatures]
            except:
                pass
            try:              
                [self.FuzzyPparamsDict.pop(replacedfeat) for replacedfeat in ReplaceFeatures]
            except:
                pass
            try:                
                [self.FuzzyHparamsDict.pop(replacedfeat) for replacedfeat in ReplaceFeatures]
            except:
                pass
        self.FeatureAppend(AnotherFeature)
            
            
 

                                                             

