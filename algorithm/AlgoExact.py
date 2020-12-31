#!/usr/bin/python3

import numpy
import sys
import json
import math

from algorithm.AlgoSolver import *


class AlgoExact(AlgoSolver): 
  def __init__(self,dictNeighbors,list_of_defencers) :
    self.list_name_of_defencers = list_of_defencers
    self.dictNeighbors = dictNeighbors
    self.list_defender = []
    self.list_kick = []

  def solver(self):
    self.createListKickAndDef()
    res = self.algoExactRec([],0)
    print(res)
    return self.chercheDefenders(res)

  def algoExactRec(self, tabDef, currentDef):
    numDef = len(self.list_defender)
    #Bloque si on a parcourut tous les défenseurs
    if(currentDef == numDef):
      return []
    for i in range(currentDef, numDef) :
      newTabDef = tabDef
      newTabDef.append(self.list_defender[i])
      #Verifie si tous les tirs sont bloqué
      if(self.allKicksStop(newTabDef)):
        return tabDef
      print("======================")
      print(tabDef)
      self.algoExactRec(newTabDef, i+1)

    
  def createListKickAndDef(self):
    for key in self.dictNeighbors :
      if "D" in key : 
        self.list_defender.append(key)
      else :
        self.list_kick.append(key)

	#Verifie que le nombre de kicks bloquer est egale au total du nombre de kicks
  def allKicksStop(self, tabDef):
    allKicksStop = self.list_kick
    for defender in tabDef :
      kickToStopByDefender = self.dictNeighbors.get(defender)
      for kick in kickToStopByDefender :
        if kick in allKicksStop :
          allKicksStop.remove(kick)
    if(len(allKicksStop) == 0):
      return True
    return False

  #Récupérer les valeurs des defenders en fonctions de leurs nom
  def chercheDefenders(self, tabDef):
    res = []
    for defender in tabDef:
      res.append(self.list_name_of_defencers.get(defender))
    return res