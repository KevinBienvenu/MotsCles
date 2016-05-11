# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

from HTMLParser import HTMLParser
import codecs
from operator import itemgetter
import time
import urllib
import os

import unidecode
import TextProcessing 
import Test

def saveDict(dic,filename):
    with codecs.open(filename,'w','utf-8') as fichier:
        for item in dic.items():
            try:
                int(item[0])
                fichier.write(str(item[0]))
            except:
                fichier.write(item[0])
            fichier.write("-")
            try:
                int(item[1])
                fichier.write(str(item[1]))
            except:
                fichier.write(item[1])
            fichier.write("\n")

def importDict(filename):
    dic = {}
    with codecs.open(filename,'r','utf-8') as fichier:
        for line in fichier:
            tab = line.split("-")
            s = tab[0]
            for i in range(1,len(tab)-1):
                s+=tab[i]
            dic[s] = tab[-1]
    return dic
   
def printSortedDic(dic, nprint=0):      
    '''
    function that print a dic sorted according to its values
    if the parameter nprint in given and non zero, print only the nprint greatest values
    -- IN:
    dic : dic which values must be int or float (dic{object:float})
    nprint : number of values to print (int) default=0
    -- OUT:
    the function returns nothing
    '''
    l = dic.items()
    l.sort(key=itemgetter(1),reverse=True)
    imax = nprint
    if imax==0:
        imax = len(l)
    for i in range(min(imax,len(l))):
        print l[i][0],l[i][1]
       
def extractNAFDesc(codeNAF):
    page = urllib.urlopen("http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/naf2008/n5_"+codeNAF+".htm")
    s = page.read().decode("iso8859_1")
    s = HTMLParser().unescape(s)
    toComprend = True
    comprend = []
    comprendpas = []
    pair = 1
    while s.find("<tr>")!=-1:
        if pair%2==0:
            s1 = s[s.find("<tr>")+4:s.find("</tr>")]
            while s1.find("<td>")!=-1:
                if toComprend:
                    comprend.append(s1[s1.find("<td>")+4:s1.find("</td>")])
                else:
                    comprendpas.append(s1[s1.find("<td>")+4:s1.find("</td>")])
                s1 = s1[s1.find("</td>")+6:]
        else:
            s1 = s[s.find("<tr>")+4:s.find("</tr>")]
            toComprend = not("pas" in s1)  
        s = s[s.find("</tr>")+6:]
        pair+=1
    if len(comprend)>0:
        comprend = TextProcessing.nltkprocess(comprend[0])
    if len(comprendpas)>0:
        comprendpas = TextProcessing.nltkprocess(comprendpas[0])
    return (codeNAF,comprend,comprendpas)
                    
def getNbResultBing(searchword, toPrint=False):
    while searchword.find(" ")!=-1:
        searchword = searchword[:searchword.find(" ")]+"+"+searchword[searchword.find(" ")+1:]
    while searchword.find(",")!=-1:
        searchword = searchword[:searchword.find(",")]+searchword[searchword.find(",")+1:]
    url = ("https://www.bing.com/search?q="+unidecode.unidecode(searchword))
    s = "-1"
    if toPrint:
        print "requete bing:",searchword,"-",
    try:
        page = urllib.urlopen(url)
        for line in page:
            i = line.find(" results<")
            if i!=-1:
                s = line[i-13:i]
                s = s[s.find(">")+1:]
                while s.find(",")!=-1:
                    s = s[:s.find(",")]+s[s.find(",")+1:]
    except:
        print "erreur"
        pass
    if toPrint:
        print int(s),"résultats"
    return int(s)
                   
def saveGraphNode(graphNode, filename):
    with codecs.open(filename,"w","utf-8") as fichier:
        for node in graphNode:
            fichier.write(str(node)+"_"+graphNode[node][0]+"_"+str(graphNode[node][1])+"_")
            for codeNAF in graphNode[node][2]:
                fichier.write(str(codeNAF)+"-"+str(graphNode[node][2][codeNAF]))
                fichier.write(",")
            fichier.write("\n")

def importGraphNode(filename):
    graphNode = {}
    dicIdNode = {}
    with codecs.open(filename,"r","utf-8") as fichier:
        for line in fichier:
            tab = line.split("_")
            dicIdNode[tab[1]] = int(tab[0])
            graphNode[int(tab[0])] = [tab[1],float(tab[2]),{}]
            for element in tab[3].split(','):
                tab1 = element.split("-")
                if len(tab1)>1:
                    graphNode[int(tab[0])][2][tab1[0]] = float(tab1[1])
    return graphNode

def saveGraphEdge(graphEdge, filename):
    with codecs.open(filename,"w","utf-8") as fichier:
        for node in graphEdge:
            fichier.write(str(node[0])+"_"+str(node[1])+"_"+str('%.2f' %graphEdge[node][0])+"_"+str(graphEdge[node][1])+"\n")
                    
def importGraphEdge(filename): 
    graphEdge = {}
    with codecs.open(filename,"r","utf-8") as fichier:
        for line in fichier:
            if len(line)>3:
                tab = line.split("_")
                graphEdge[(tab[0],tab[1])]=[float(tab[2]),int(tab[3])]
    return graphEdge
       
def importKeywords(path = None):
    '''
    function that imports the keywords out of a file given by pathArg
    (the path must contain a file named keywords.txt
    if the given path is None (default) the extracted file is motscles/mots-cles.txt
    the function then put them in the dictionary 'keywords', which values are the tokenized keywords
    -- IN:
    path : the file to load (path) default = None
    -- OUT:
    keywords : the dictionary containing the keywords
    '''
    keywords = {}
    if path is None:
        path = Test.path
    os.chdir(path)
    with codecs.open("keywords.txt","r","utf-8") as fichier:
        for line in fichier:
            if len(line)>1:
                keywords[line[:-1]] = TextProcessing.nltkprocess(line[:-1])
    return keywords
 
def saveGexfFile(filename, graphNodes, graphEdges):
    with codecs.open(filename,"w","utf-8") as fichier:
        # writing header
        fichier.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        fichier.write("<gexf xmlns=\"http://www.gexf.net/1.2draft\" \
                        xmlns:viz=\"http://www.gexf.net/1.2draft/viz\" \
                        version=\"1.2\">\n")
        fichier.write("<meta lastmodifieddate=\""+time.strftime('%d/%m/%y',time.localtime())+"\">\n")
        fichier.write("<creator>Kevin Bienvenu</creator>\n")
        fichier.write("<description>A subset graph file</description>\n")
        fichier.write("</meta>\n")
        # writing graph
        fichier.write("<graph>\n")
        # writing nodes
        fichier.write("<nodes>\n")
        for node in graphNodes:
            fichier.write("<node id=\"")
            fichier.write(str(node))
            fichier.write("\" label=\"")
            fichier.write(graphNodes[node][0].replace("&","et"))
            fichier.write("\">\n")
            fichier.write("<viz:size value=\"")
            fichier.write(str(sum(graphNodes[node][2].values())))
            fichier.write("\"/>\n")
            fichier.write("</node>")
        fichier.write("</nodes>\n")
        # writing edges
        fichier.write("<edges>\n")
        i=0
        for edge in graphEdges:
            fichier.write("<edge id=\"")
            fichier.write(str(i))
            fichier.write("\" source=\"")
            fichier.write(str(edge[0]))
            fichier.write("\" target=\"")
            fichier.write(str(edge[1]))
            fichier.write("\" type=\"undirected\" weight=\"")
            fichier.write(str(3.0*graphEdges[edge][0]/graphEdges[edge][1]))
            fichier.write("\"/>\n")
            i+=1
        fichier.write("</edges>\n")
        fichier.write("</graph>\n")
        fichier.write("</gexf>")

def saveGexfFileNaf(filename, graphNodes, graphEdges, codeNAF):
    with codecs.open(filename,"w","utf-8") as fichier:
        # writing header
        fichier.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        fichier.write("<gexf xmlns=\"http://www.gexf.net/1.2draft\" \
                        xmlns:viz=\"http://www.gexf.net/1.2draft/viz\" \
                        version=\"1.2\">\n")
        fichier.write("<meta lastmodifieddate=\""+time.strftime('%d/%m/%y',time.localtime())+"\">\n")
        fichier.write("<creator>Kevin Bienvenu</creator>\n")
        fichier.write("<description>A subset graph file</description>\n")
        fichier.write("</meta>\n")
        # writing graph
        fichier.write("<graph>\n")
        # writing nodes
        fichier.write("<nodes>\n")
        for node in graphNodes:
            if codeNAF in graphNodes[node][2]:
                fichier.write("<node id=\"")
                fichier.write(str(node))
                fichier.write("\" label=\"")
                fichier.write(graphNodes[node][0].replace("&","et"))
                fichier.write("\">\n")
                fichier.write("<viz:size value=\"")
                fichier.write(str(graphNodes[node][2][codeNAF]))
                fichier.write("\"/>\n")
                fichier.write("</node>")
        fichier.write("</nodes>\n")
        # writing edges
        fichier.write("<edges>\n")
        i=0
        for edge in graphEdges:
            if codeNAF in graphNodes[edge[0]][2] or codeNAF in graphNodes[edge[1]][2] :
                fichier.write("<edge id=\"")
                fichier.write(str(i))
                fichier.write("\" source=\"")
                fichier.write(str(edge[0]))
                fichier.write("\" target=\"")
                fichier.write(str(edge[1]))
                fichier.write("\" type=\"undirected\" weight=\"")
                fichier.write(str(3.0*graphEdges[edge][0]/graphEdges[edge][1]))
                fichier.write("\"/>\n")
                i+=1
        fichier.write("</edges>\n")
        fichier.write("</graph>\n")
        fichier.write("</gexf>")
                     
''' function about progress printing '''

def initProgress(completefile, p = 10):
    '''
    function initializing the compt variable to print progress
    -- IN:
    completefile : any kind of iterable object, the len(completefile) must be a valid command
    p : step of percentage for the printing (int) default = 10
    -- OUT:
    compt : the compt variable containing (i=iteration variable, p=current percent,
                                            total=len(completefile),deltap=step of percent)
    '''
    i = 0
    total = len(completefile)
    compt = (i,p,total,p)   
    return compt   

def updateProgress(compt):
    '''
    function updating the compt variable and printing progress
    -- IN
    compt : compt variable to be updated (see initProgress)
    -- OUT
    compt : the updated compt variable
    '''
    (i,percent,total,deltap) = compt
    i+=1
    if 100.0*i/total > percent:
        print percent,"%",
        percent+=deltap
        if deltap==1 and percent%10==0:
            print ""
    compt = (i,percent,total,deltap)
    return compt               
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                