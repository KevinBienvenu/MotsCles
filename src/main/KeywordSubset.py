# -*- coding: utf-8 -*-
'''
Created on 10 mai 2016

@author: Kévin Bienvenu
'''

from operator import itemgetter
import numpy as np
import pandas as pd
import codecs
import os
import IOFunctions
import TextProcessing
import GraphPreprocess

# user = "Utilisateur"
user = "KevinBienvenu"
path = "C:/Users/"+user+"/Documents/GitHub/MotsCles"
pathAgreg = "C:/Users/"+user+"/Google Drive/Camelia Tech/Donnees entreprise/Agregation B Reputation"
pathsubset = "C:/Users/"+user+"/Documents/GitHub/MotsCles/subsets"

def extractRandomSubset(n=10, subsetname="extrait_entreprises"):
    os.chdir(pathAgreg)
    print "== Extracting random subset of size",n
    fileNameVec = ['BRep_Step2_0_1000000.csv', 
               'BRep_Step2_1000000_2000000.csv', 
               'BRep_Step2_2000000_3000000.csv',
              'BRep_Step2_3000000_4000000.csv', 
              'BRep_Step2_4000000_5000000.csv', 
              'BRep_Step2_5000000_6000000.csv',
              'BRep_Step2_6000000_7000000.csv', 
              'BRep_Step2_7000000_8000000.csv', 
              'BRep_Step2_8000000_9176180.csv']
    entreprises = []
    for i in range(n):
        brepFile = fileNameVec[np.random.randint(0,9)]
        csvfile = pd.read_csv(brepFile, usecols=['siren','codeNaf', 'description'])
        csvfile = csvfile[csvfile.description.notnull()]
        line = csvfile.iloc[np.random.randint(0,len(csvfile))]
        entreprises.append([line[0],line[1],line[2]])
        print str(i+1)+"/"+str(n)
    os.chdir(pathsubset)
    i=0
    if subsetname not in os.listdir("."):
        os.mkdir("./"+subsetname)
    os.chdir("./"+subsetname)
    with open("subset_entreprises.txt","w") as fichier:
        for entreprise in entreprises:
            fichier.write(""+str(entreprise[0]))
            fichier.write("_"+str(entreprise[1])+"_")
            fichier.write(entreprise[2])
            fichier.write("\n")
    keywords = createKeywords(entreprises, subsetname)
#     printKeywordsSubset(entreprises = entreprises, keywords = keywords)
    dicWordWeight = GraphPreprocess.generateWordWeight(keywords)
    IOFunctions.saveDict(dicWordWeight, "dicWordWeight.txt")
    
def importSubset(subsetname):
    '''
    function that imports a previously computed subset 
    and puts it into the array entreprises
    -- IN:
    filename : the name of the subset to import (string)
    -- OUT:
    entreprises : array containing info about the entreprise (dic)
    keywords : dic of keywords
    '''
    # importing file
    os.chdir(pathsubset)
    if not(subsetname in os.listdir(".")):
        print "non-existing subset"
        return (None,None)
    os.chdir("./"+subsetname)
    entreprises = []
    with open("subset_entreprises.txt","r") as fichier:
        for line in fichier:
            entreprises.append(line.split("_"))
    keywords = IOFunctions.importKeywords(pathsubset+"/"+subsetname)
    dicWordWeight = IOFunctions.importDict("dicWordWeight.txt")
    return (entreprises, keywords, dicWordWeight)

def analyzeSubset(subsetname):
    # importing subset
    entreprises = importSubset(subsetname)
    # computing stats about codeNAF
    dicNAF1 = {}
    dicNAF2 = {}
    for entreprise in entreprises:
        naf1 = int(entreprise[1][:1])
        if not(naf1 in dicNAF1):
            dicNAF1[naf1] = 0
        dicNAF1[naf1]+=1
        naf2 = int(entreprise[1][:2])
        if not(naf2 in dicNAF2):
            dicNAF2[naf2] = 0
        dicNAF2[naf2]+=1
    l = dicNAF1.items()
    l.sort(key=itemgetter(1),reverse=True)
    l2 = dicNAF2.items()
    l2.sort(key=itemgetter(1),reverse=True)
    print l[:5]
    print l2[:5]

def createKeywords(entreprises,subsetname):
    '''
    function that import the keywords list and remove the unused one
    to create a restrictive list of used keywords
    -- IN:
    entreprises: the array containing the siren, naf and description of entreprises (array [[siren,naf,desc],..])
    -- OUT:
    keywords: dictionary of keywords which values are the tokenized keywords
    '''
    print "== Creating keywords for subset :",subsetname
    print ""
    print "- importing all keywords",
    # importing all keywords
    keywords = IOFunctions.importKeywords()
    print "... done"
    newKeywords = {}
    # extracting descriptions
    descriptions = [tab[2] for tab in entreprises]
    print "- analysing descriptions"
    print "   ",
    compt = IOFunctions.initProgress(descriptions, 10)
    for description in descriptions:
        compt = IOFunctions.updateProgress(compt)
        dic = TextProcessing.extractKeywordsFromString(description, keywords, {}) 
        for key in dic:
            newKeywords[key] = keywords[key]
            del keywords[key]
    print " ... done"
    os.chdir(pathsubset+"/"+subsetname)
    with codecs.open("keywords.txt","w","utf-8") as fichier:
        for keyword in newKeywords:
            fichier.write(keyword)
            fichier.write("\n")
    return newKeywords
        
def printKeywordsSubset(subsetname = "", entreprises=None, keywords=None):  
    if entreprises is None or keywords is None:  
        (entreprises, keywords) = importSubset("extrait1")
    for entreprise in entreprises:
        TextProcessing.extractKeywordsFromString(entreprise[2], keywords, True)


