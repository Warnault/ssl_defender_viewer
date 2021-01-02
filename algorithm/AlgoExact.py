#!/usr/bin/python3

import numpy
import sys
import json
import math
import itertools

from algorithm.AlgoSolver import *


class AlgoExact(AlgoSolver): 
  def __init__(self,dictNeighbors,list_of_defencers) :
    self.list_name_of_defencers = list_of_defencers
    self.dictNeighbors = dictNeighbors
    self.list_defender = []
    self.list_kick = []

  def solver(self):
    self.createListKickAndDef()
    for i in range(len(self.list_defender)):
      list_permutation = itertools.permutations(self.list_defender,i)
      for ele in list_permutation:
        if(self.allKicksStop(ele)):
          print("solver",ele)
          return self.chercheDefenders(ele)
    return []

  def createListKickAndDef(self):
    for key in self.dictNeighbors :
      if "D" in key : 
        self.list_defender.append(key)
      else :
        self.list_kick.append(key)

	#Verifie que le nombre de kicks bloquer est egale au total du nombre de kicks
  def allKicksStop(self, tabDef):
    allKicksStop = self.list_kick.copy()
    #print(allKicksStop)
    kickToStopByDefender = 0
    for defender in tabDef :
      kickToStopByDefender = self.dictNeighbors.get(defender)
      for kick in kickToStopByDefender :
        if kick in allKicksStop :
          allKicksStop.remove(kick)
    if(len(allKicksStop) == 0):
      return True
    return False

#  def algoExactRec(self, tabDef, index, list_defender):
#    numDef = len(list_defender)
#    if(index == numDef):
#      return []
#    for i in range(index):
#      for d in list_defender:
#        copy_tabDef = tabDef.copy()
#        #copy_list_defender = list_defender.copy()
#        if(d not in copy_tabDef):
#          copy_tabDef.append(d)      
#        #copy_list_defender.remove(d)
#        if(self.allKicksStop(copy_tabDef)):
#          print("Gagnee , normalement ",copy_tabDef)
#          return copy_tabDef
#    index+=1
#    return self.algoExactRec,tabDef,index,list_defender)
#