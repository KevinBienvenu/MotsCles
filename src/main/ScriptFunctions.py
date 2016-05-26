# -*- coding: utf-8 -*-
'''
Created on 26 mai 2016

@author: Kévin Bienvenu
'''

import Constants
import os
import pandas as pd


def createDescDatabase():
    print ""
    os.chdir(Constants.pathAgreg)
    fileNameVec = ['BRep_Step2_0_1000000.csv', 
               'BRep_Step2_1000000_2000000.csv', 
               'BRep_Step2_2000000_3000000.csv',
              'BRep_Step2_3000000_4000000.csv', 
              'BRep_Step2_4000000_5000000.csv', 
              'BRep_Step2_5000000_6000000.csv',
              'BRep_Step2_6000000_7000000.csv', 
              'BRep_Step2_7000000_8000000.csv', 
              'BRep_Step2_8000000_9176180.csv']
    db = pd.DataFrame(columns=['codeNAF','description','keywords'])
    for filename in fileNameVec:
        csvfile = pd.read_csv(filename, usecols=['codeNAF','description','keywords'])
        csvfile = csvfile[csvfile.description.notnull()]
        db = pd.concat([db,csvfile],copy=False)
        print len(db)
    db.to_csv("descriptions.csv", compression="bz2")
    
        
        
            