#!/usr/bin/python3

import numpy
import sys
import json
import math
import abc 

from algorithm.AlgoSolver import *

class AlgoGlouton(AlgoSolver) :
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
    res = self.algoGlouton(self.list_kick, self.list_defender, [])
    print(res)
    return self.chercheDefenders(res)

  def solver_with_keeper(self):
    print("Glouton")

  def algoGlouton(self, tabKick, tabDef, tabDefSol):
    tabKickLength = len(tabKick)
    tabDefLength = len(tabDef)
    maxDefender = None
    maxNeighbourLength = 0
    if(tabKickLength == 0):
      return tabDefSol
    if(tabDefLength == 0):
      return []
    for defender in tabDef:
      num = self.numKickOfDefender(tabKick, self.dictNeighbors.get(defender))
      if(num > maxNeighbourLength):
        maxNeighbourLength = num
        maxDefender = defender
        if(maxNeighbourLength == tabKickLength):
          tabDefSol.append(maxDefender)
          return tabDefSol
    tabDefSol.append(maxDefender)
    tabKick = self.removeKickStop(maxDefender, tabKick)
    tabDef.remove(maxDefender)
    return self.algoGlouton(tabKick, tabDef, tabDefSol)


  #Cherche le nombre de voisin en fonction de ceux de la list
  def numKickOfDefender(self, tabKick, kickStopByDefender):
    cpt = 0
    for kickStop in kickStopByDefender : 
      for kick in tabKick : 
        if(kickStop == kick):
          cpt = cpt + 1
          break
    return cpt

  def removeKickStop(self, defender, tabKick):
    kickRemove = self.dictNeighbors.get(defender)
    for kick in kickRemove:
      tabKick.remove(kick)
    return tabKick

