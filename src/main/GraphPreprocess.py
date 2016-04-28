# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2016

@author: Kévin Bienvenu
'''

import codecs
import os
import math
import operator
import random
import nltk
import pandas as pd
from nltk.corpus import stopwords
from main import IOFunctions, TextProcessing

path0 = "C:/Users/Utilisateur/Documents/GitHub/MotsCles"
path1 = "C:/Users/KevinBienvenu/Documents/GitHub/MotsCles"

pathAgreg0 = "C:/Users/Utilisateur/Google Drive/Camelia Tech/Donnees entreprise/Agregation B Reputation"
pathAgreg1 = "C:/Users/KevinBienvenu/Google Drive/Camelia Tech/Donnees entreprise/Agregation B Reputation"

path = path1
pathAgreg = pathAgreg1

def normalizeMotsClesKompass():
    path0 = "C:/Users/Utilisateur/Documents/GitHub/MotsCles/dicts"
    path1 = "C:/Users/KevinBienvenu/Documents/GitHub/MotsCles/dicts"
    os.chdir(path1)
    # first step compute normalization of kompass terms
    dicMainClasses = {}
    dicSubClasses = {}
    dicArborescence = {}
    with codecs.open("mots-cles-kompass.txt","r","utf-8") as fichier:
        total = len(fichier.readlines())
    with open("mots-cles-kompass.txt","r") as fichier:
        lastClass = ""
        percent = 1
        j=0
        for line in fichier:
            j+=1
            if 100.0*j/total>percent:
                print percent,"% -",
                percent+=1
                if percent%10==0:
                    print ""
            if len(line)>10 and line[:4]=="    " and line[4:8]!="    ":
                term = line[4:-1].lower()
                lastClass = term
                dicMainClasses[term] = max([IOFunctions.getNbResultBing(term) for i in range(10)])
            elif len(line)>10 and line[:8]=="        ":
                term = line[8:-1].lower()
                dicArborescence[term] = lastClass
                dicSubClasses[term] = max([IOFunctions.getNbResultBing(term) for i in range(5)])
    print "done"
    os.chdir("./dicts")
    IOFunctions.saveDict(dicMainClasses, "dicMainClasses.txt")
    IOFunctions.saveDict(dicSubClasses, "dicSubClasses.txt")
    IOFunctions.saveDict(dicArborescence, "dicArborescence.txt")

def normalizeMotsClesPJ():
    path0 = "C:/Users/Utilisateur/Documents/GitHub/MotsCles"
    path1 = "C:/Users/KevinBienvenu/Documents/GitHub/MotsCles"
    os.chdir(path1)
    # first step compute normalization of kompass terms
    dicMotsClesPJ = {}
    with codecs.open("mots-cles-pj.txt","r","utf-8") as fichier:
        total = len(fichier.readlines())
    with open("mots-cles-pj.txt","r") as fichier:
        percent = 1
        j=0
        for line in fichier:
            j+=1
            if 100.0*j/total>percent:
                print percent,"% -",
                percent+=1
                if percent%10==0:
                    print ""
            if len(line)>10 and line[:4]=="    ":
                term = line[4:-1].lower()
                dicMotsClesPJ[term] = max([IOFunctions.getNbResultBing(term) for i in range(3)])
    print "done"
    os.chdir("./dicts")
    IOFunctions.saveDict(dicMotsClesPJ, "dicMotsClesPJ.txt")

def normalizeCodeNAF1():
    path0 = "C:/Users/Utilisateur/Documents/GitHub/MotsCles"
    path1 = "C:/Users/KevinBienvenu/Documents/GitHub/MotsCles"
    os.chdir(path0)
    # first step compute normalization of kompass terms
    dicCodeNAF = {}
    with open("codeNAF1.txt","r") as fichier:
        total = len(fichier.readlines())
    with open("codeNAF1.txt","r") as fichier:
        percent = 10
        j=0
        for line in fichier:
            j+=1
            if 100.0*j/total>percent:
                print percent,"% -",
                percent+=10
                if percent%10==0:
                    print ""
            term = line[:-1].lower()
            codeNAF = term
            tab = term.split(" et ")
            term = []
            for mot in tab:
                for mot2 in mot.split(","):
                    term.append(mot2)
            norm = max([IOFunctions.getNbResultBing(mot,True) for mot in term])
            dicCodeNAF[codeNAF] = norm
    print "done"    
    os.chdir("./dicts")
    IOFunctions.saveDict(dicCodeNAF, "dicCodeNAF1.txt")

def importDicts():
    path0 = "C:/Users/Utilisateur/Documents/GitHub/MotsCles/dicts"
    path1 = "C:/Users/KevinBienvenu/Documents/GitHub/MotsCles/dicts"
    os.chdir(path0)
    dicPj = IOFunctions.importDict("dicMotsClesPJ.txt")
    dicMainKompass = IOFunctions.importDict("dicMainClasses.txt")
    dicSubKompass = IOFunctions.importDict("dicSubClasses.txt")
    return (dicPj,dicMainKompass,dicSubKompass)
    
def distanceMots(mot1, mot2, norm1, norm2):
    dis = 0
    dis += 1.0*min(IOFunctions.getNbResultBing(mot1+" "+mot2),IOFunctions.getNbResultBing(mot2+" "+mot1))
#     norm = math.sqrt(int(norm1)**2+int(norm2)**2+1)
    norm = 1.0*max(int(norm1),int(norm2))
    dis /= norm
    return dis

def findClassKompass(motclepj,dicPj,dicMainKompass,dicSubKompass):
    if not (motclepj in dicPj):
        return ""
    norm = dicPj[motclepj]
    dicResult = {}
    for subclass in dicSubKompass:
        dicResult[subclass] = distanceMots(mot1=motclepj, mot2=subclass, norm1=norm, norm2=dicSubKompass[subclass])
    dicResult= sorted(dicResult.items(), key=operator.itemgetter(1),reverse=True)
    for i in range(3):
        print "   ",dicResult[i][0],dicResult[i][1]
   
''' functions of graph handling '''

def addEdgeValue(id1, id2, value):
    '''
    function that add the value 'value' to the edge between the nodes 1 and 2
    -- IN
    id1 : id of the first node (int)
    id2 : id of the second node (int)
    value : the value to add to the edge (float)
    -- OUT
    returns nothing
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
        graphEdges[(i,j)] = 0
    graphEdges[(i,j)] += v
    
def addNodeValues(name, codeNAF="", valueNAF=0, genericity = 0):
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
    returns nothing    
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

def extractKeywordsFromDescription(desc):
    '''
    function that returns a list of keywords out of a description
    -- IN
    desc : the description (str)
    -- OUT
    dic : dic of keywords (dic{str:float})
    '''
    dic = {}
    stemmedDesc = TextProcessing.nltkprocess(desc)
    for keyword in keywords:
        v = getProbKeywordInDescription(keyword, stemmedDesc)
        if v>0.00:
            dic[keyword] = v
    return dic

def getProbKeywordInDescription(keyword, stemmedDesc):
    v=0
    for keywordslug in keywords[keyword]:
        coeff = 1.0
        for s in stemmedDesc:
            if keywordslug == s:
                v+=coeff
            coeff*=0.97
    if v>0:
        v = 1.0*v/len(keywords[keyword])
    return v

def extractDescription(desc,codeNAF):
    '''
    function that extracts the content of a description and fills the graph.
    extraction of the keywords ?
    -- IN
    desc : the description to extract (str)
    codeNAF : the corresponding codeNAF (str)
    -- OUT
    returns nothing
    '''
    listKeywords = extractKeywordsFromDescription(desc)
    for k in listKeywords:
        addNodeValues(k, codeNAF=codeNAF, valueNAF=listKeywords[k])
    for k in listKeywords:
        for k1 in listKeywords:
            if k!=k1:
                addEdgeValue(dicIdNodes[k], dicIdNodes[k1], listKeywords[k]+listKeywords[k1])

def importKeywords():
    os.chdir(path)
    with codecs.open("keyword.csv","r","utf-8") as fichier:
        for line in fichier:
            if len(line)>1:
                keywords[line[:-1]] = TextProcessing.nltkprocess(line[:-1])

def extractKeywords(codeNAF):
    nodes = {}
    for node in graphNodes:
        if codeNAF in graphNodes[node][2]:
            nodes[graphNodes[node][0]]=graphNodes[node][2][codeNAF]
    dic= sorted(nodes.items(), key=operator.itemgetter(1),reverse=True)
    return dic[:min(10,len(dic))]

def extractDescriptionFromCSV(filename):
    os.chdir(pathAgreg)
    db = pd.read_csv(filename,usecols=['codeNaf', 'description'])
    percent = 1
    i = 0
    total = len(db)
    for line in db.values:
        i+=1
        if 100.0*i/total>percent:
            print percent,"%",
            percent+=1
            if percent%10==0:
                print ""
        if str(line[1])!="nan":
            extractDescription(line[1],line[0])

     
# (dicPj,dicMainKompass,dicSubKompass) = importDicts()
# 
# for i in range(10):
#     motclepj = random.choice(dicPj.keys())
#     print motclepj
#     findClassKompass(motclepj, dicPj, dicMainKompass, dicSubKompass)

# Node V : id, name, genericite, dic{NAF:value}
# Edge E : dic{(id1,id2),value}
graphNodes = {}
graphEdges = {}
dicIdNodes = {}

keywords = {}

importKeywords()

extractDescriptionFromCSV("BRep_Step2_0_1000000.csv")

os.chdir(path)

IOFunctions.saveGraphNode(graphNodes, "vaneau.txt")


     
    




    