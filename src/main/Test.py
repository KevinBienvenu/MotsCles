# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import GraphPreprocess, KeywordSubset, ExtractingKeywordsFromInternet, os, IOFunctions

# user = "Utilisateur"
user = "KevinBienvenu"
path = "C:/Users/"+user+"/Documents/GitHub/MotsCles"
pathAgreg = "C:/Users/"+user+"/Google Drive/Camelia Tech/Donnees entreprise/Agregation B Reputation"
pathSubset = "C:/Users/"+user+"/Documents/GitHub/MotsCles/subsets"

nbExtract = 5000
KeywordSubset.extractRandomSubset(nbExtract, "extrait_"+str(nbExtract))
GraphPreprocess.extractGraphFromSubset("extrait_"+str(nbExtract))


# os.chdir("C:/Users/Utilisateur/Documents/GitHub/MotsCles/motscles")
# ExtractingKeywordsFromInternet.cleanMotsCles("keywords.txt")







