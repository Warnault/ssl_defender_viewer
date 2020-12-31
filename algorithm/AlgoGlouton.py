#!/usr/bin/python3

import numpy
import sys
import json
import math

class AlgoGlouton :
  def __init__(self,dictNeighbors,list_of_defencers) :
    self.list_name_of_defencers = list_of_defencers
    self.dictNeighbors = dictNeighbors
    self.list_defender = []
    self.list_kick = []

  def solver(self):
    self.createListKickAndDef()
    res = self.algoGlouton(self.list_kick, self.list_defender, [])
    print(res)
    return self.chercheDefenders(res)

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

	#Récupérer les valeurs des defenders en fonctions de leurs nom
  def chercheDefenders(self, tabDef):
    res = []
    for defender in tabDef:
      res.append(self.list_name_of_defencers.get(defender))
    return res

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

  def createListKickAndDef(self):
    for key in self.dictNeighbors :
      if "D" in key : 
        self.list_defender.append(key)
      else :
        self.list_kick.append(key)