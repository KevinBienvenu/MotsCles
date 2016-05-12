# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import GraphPreprocess
import KeywordSubset
import  ExtractingKeywordsFromInternet
import  os
import  IOFunctions
import Constants


path = Constants.path
pathAgreg = Constants.pathAgreg
pathSubset = Constants.pathSubset

codeNAfs = ['4322B','4399C','6201Z','7311Z','9003A']

os.chdir(pathSubset)
graph = IOFunctions.importGraph("extrait_501")
for codeNaf in codeNAfs:
    print codeNaf, IOFunctions.saveGexfFileNaf("graphNAF.gexf", graph[0], graph[1], codeNaf)
for codeNaf in codeNAfs:
    (entreprises,_,_) = KeywordSubset.importSubset("extrait_501")
    compt = 0
    for entreprise in entreprises:
        if entreprise[1]==codeNaf:
            compt+=1
    print compt

# KeywordSubset.extractRandomSubset(501, "extrait_501")
# GraphPreprocess.extractGraphFromSubset("extrait_501")


# os.chdir("C:/Users/Utilisateur/Documents/GitHub/MotsCles/motscles")
# ExtractingKeywordsFromInternet.cleanMotsCles("keywords.txt")







