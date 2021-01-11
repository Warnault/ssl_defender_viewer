#!/usr/bin/python3

import numpy
import sys
import json
import math
import itertools

from algorithm.AlgoSolver import *


class AlgoExact(AlgoSolver): 
  def __init__(self,dictNeighbors,list_of_defencers,list_of_goals) :
    self.list_name_of_defencers = list_of_defencers
    self.dictNeighbors = dictNeighbors
    self.list_defender = []
    self.list_kick = []
    self.list_of_goals = list_of_goals

  def solver(self):
    if (len(self.list_of_goals)==0):
        self.solver_without_keeper()
    else:
        self.solver_with_keeper()

  def solver_without_keeper(self): 
    self.createListKickAndDef()
    for i in range(len(self.list_defender)):
      list_permutation = itertools.permutations(self.list_defender,i)
      for ele in list_permutation:
        if(self.allKicksStop(ele)):
          return self.chercheDefenders(ele)
    return []

  def solver_with_keeper(self):
    print("KEEPER")


	#Verifie que le nombre de kicks bloquer est egale au total du nombre de kicks
  def allKicksStop(self, tabDef):
    allKicksStop = self.list_kick.copy()
    kickToStopByDefender = 0
    for defender in tabDef :
      kickToStopByDefender = self.dictNeighbors.get(defender)
      for kick in kickToStopByDefender :
        if kick in allKicksStop :
          allKicksStop.remove(kick)
    if(len(allKicksStop) == 0):
      return True
    return False