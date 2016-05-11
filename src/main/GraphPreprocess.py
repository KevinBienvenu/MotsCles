# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2016

@author: Kévin Bienvenu
'''

import os
import operator
import pandas as pd
import TextProcessing
import KeywordSubset
import IOFunctions
import Test

path = Test.path
pathAgreg = Test.pathAgreg



''' functions of graph handling '''

'''
 === Graph Description ===
- graphNodes V : dic{id, (name, genericite, dic{NAF:value})}

- graphEdges E : dic{(id1,id2),[value,nbOccurence]}
'''

def addEdgeValue(id1, id2, value, graphEdges):
    '''
    function that add the value 'value' to the edge between the nodes 1 and 2
    -- IN
    id1 : id of the first node (int)
    id2 : id of the second node (int)
    value : the value to add to the edge (float)
    -- OUT
    graphEdges : the dic of edges
    '''
    try:
        i = int(id1)
        j = int(id2)
        v = float(value)
    except:
        return
    if i>j:
        (i,j) = (j,i)
    if not((i,j) in graphEdges):
        graphEdges[(i,j)] = [0,0]
    graphEdges[(i,j)][0] += v
    graphEdges[(i,j)][1] += 1
    return graphEdges
    
def addNodeValues(name, dicIdNodes, graphNodes, codeNAF="", valueNAF=0, genericity = 0):
    '''
    function that change the node 'name'
    if the node doesn't exist 
        it is created
    if the codeNAF is different than ""
        if the node doesn't have a value for codeNAF, 
            it is set to zero
        add the value 'valueNAF' to the codeNAF
    if the genericity is different than 0
        the node get this genericity
    -- IN
    name : name of the node to change (str)
    codeNAF : name of the codeNAF to change (str) default = ""
    value : value to add to the code NAF (float) default = 0
    genericity : value to set to the genericity (float) default = 0
    -- OUT
    dicIdNodes : dic of nodes id
    graphNodes : graph of nodes  
    '''
    try:
        v = float(valueNAF)
        g = float(genericity)
    except:
        return
    if not(name in dicIdNodes):
        dicIdNodes[name] = len(dicIdNodes)
        graphNodes[dicIdNodes[name]] = [name, 0, {}]
    if codeNAF != "":
        if not(codeNAF in graphNodes[dicIdNodes[name]][2]):
            graphNodes[dicIdNodes[name]][2][codeNAF] = 0
        graphNodes[dicIdNodes[name]][2][codeNAF] += v
    if genericity>0:
        graphNodes[dicIdNodes[name]][1] = g
    return (dicIdNodes, graphNodes)

def extractDescription(desc,codeNAF,keywords, dicWordWeight, dicIdNodes, graphNodes, graphEdges):
    '''
    function that extracts the content of a description and fills the graph.
    extraction of the keywords ?
    -- IN
    desc : the description to extract (str)
    codeNAF : the corresponding codeNAF (str)
    keywords : global dic of keywords
    dicWordWeight : global dic of word weight
    dicIdNodes :
    graphNodes :
    graphEdges :
    -- OUT
    dicIdNodes :
    graphNodes :
    graphEdges :
    '''
    listKeywords = TextProcessing.extractKeywordsFromString(desc,keywords, dicWordWeight)
    for k in listKeywords:
        (dicIdNodes, graphNodes) = addNodeValues(k, dicIdNodes, graphNodes,codeNAF=codeNAF, valueNAF=listKeywords[k])
    for k in listKeywords:
        for k1 in listKeywords:
            if k!=k1:
                graphEdges = addEdgeValue(dicIdNodes[k], dicIdNodes[k1], listKeywords[k]+listKeywords[k1],graphEdges)
    return (dicIdNodes,graphNodes,graphEdges)

def generateWordWeight(keywords):
    '''
    function that generates a dic of word used in keywords and computes their weights.
    The more a word is present in keywords, the heavier it will weight.
    -- IN:
    keywords: dic of keywords (dic{str:[tokens]})
    -- OUT:
    dicWordWeight : dic of words and their weight (dic{str:int})
    '''
    dicWordWeight = {}
    for keywordstems in keywords.values():
        for word in keywordstems:
            if not(word in dicWordWeight):
                dicWordWeight[word] = 0
            dicWordWeight[word] += 1
    return dicWordWeight

''' experimental functions '''

def extractKeywords(codeNAF, graphNodes):
    '''
    experimental function that return the 10 first keywords for a particular codeNAF
    '''
    nodes = {}
    for node in graphNodes:
        if codeNAF in graphNodes[node][2]:
            nodes[graphNodes[node][0]]=graphNodes[node][2][codeNAF]
    dic= sorted(nodes.items(), key=operator.itemgetter(1),reverse=True)
    return dic[:min(10,len(dic))]

def extractGraphFromCSV(filename,keywords):
    ''' 
    non generic function that extract description and keywords from csv file
    '''
    os.chdir(pathAgreg)
    db = pd.read_csv(filename,usecols=['codeNaf', 'description'])
    percent = 1
    i = 0
    total = len(db)
    graphNodes = {}
    graphEdges = {}
    dicIdNodes = {}
    for line in db.values:
        i+=1
        if 100.0*i/total>percent:
            print percent,"%",
            percent+=1
            if percent%10==0:
                print ""
        if str(line[1])!="nan":
            (dicIdNodes,graphNodes,graphEdges)=extractDescription(line[1],line[0],keywords,dicIdNodes,graphNodes,graphEdges)
        break
    return (dicIdNodes,graphNodes,graphEdges)

     



# keywords = importKeywords()
# 
# fileNameVec = ['BRep_Step2_0_1000000.csv', 
#                'BRep_Step2_1000000_2000000.csv', 
#                'BRep_Step2_2000000_3000000.csv',
#               'BRep_Step2_3000000_4000000.csv', 
#               'BRep_Step2_4000000_5000000.csv', 
#               'BRep_Step2_5000000_6000000.csv',
#               'BRep_Step2_6000000_7000000.csv', 
#               'BRep_Step2_7000000_8000000.csv', 
#               'BRep_Step2_8000000_9176180.csv']
# 
# for filename in fileNameVec:
#     print "extracting file:",filename
#     extractDescriptionFromCSV(filename, keywords)
# 
# os.chdir(path)
# IOFunctions.saveGraphNode(graphNodes, "graphNode.txt")
# IOFunctions.saveGraphEdge(graphEdges, "graphEdge.txt")

# graphNodes = IOFunctions.importGraphNode("vaneau_copy.txt")

# codeNAFs = []
# for node in graphNodes:
#     for codeNAF in graphNodes[node][2]:
#         if not codeNAF in codeNAFs:
#             codeNAFs.append(codeNAF)
#             
# print len(codeNAFs)
# print len(graphNodes)
# 
# 
# print extractKeywords("2059Z")

def extractGraphFromSubset(subsetname):
    '''
    function that computes a graph (ie. dicIdNodes, graphNodes, graphEdges)
    out of a subset file, containing a 'keywords.txt' and a 'subsey_entreprises.txt' file
    -- IN:
    subsetname : name of the subset (string)
    -- OUT:
    dicIdNodes : dic of id of the nodes
    graphNodes : dic of the nodes
    graphEdges : dic of the edges
    '''
    print "== Extracting graph from subset:",subsetname
    print "- importing subset",
    (entreprises,keywords,dicWordWeight) = KeywordSubset.importSubset(subsetname)
    print "... done"
    if entreprises is None:
        return
    graphNodes = {}
    graphEdges = {}
    dicIdNodes = {}
    print "- analyzing entreprises"
    compt = IOFunctions.initProgress(entreprises, 10)
    for entreprise in entreprises:
        compt = IOFunctions.updateProgress(compt)
        (dicIdNodes,graphNodes,graphEdges) = extractDescription(entreprise[2],entreprise[1], keywords, dicWordWeight, dicIdNodes, graphNodes, graphEdges)
    print "... done"
    print "- saving graphs",
    os.chdir(KeywordSubset.pathsubset+"/"+subsetname)
    IOFunctions.saveGraphEdge(graphEdges, "graphEdges.txt")
    IOFunctions.saveGraphNode(graphNodes, "graphNodes.txt")
    IOFunctions.saveGexfFile("graph.gexf", graphNodes, graphEdges)
    print "... done"
     
    




    