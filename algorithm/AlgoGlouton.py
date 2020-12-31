#!/usr/bin/python3

import numpy
import sys
import json
import math

class AlgoGlouton :
  def __init__(self,dictNeighbors,list_of_defencers) :
    self.list_of_defencers = list_of_defencers
    self.dictNeighbors = dictNeighbors

  def algoGlouton(self, tabKick, tabDef, tabDefSol):
    tabKickLength = len(tabKick)
    tabDefLength = len(tabDef)
    maxDefender = None
    maxNeighbourLength = 0
    if(tabKickLength == 0):
      self.solution = self.chercheDefenders(tabDefSol)
      return True
    if(tabDefLength == 0):
      return False
    for defender in tabDef:
      num = self.numKickOfDefender(tabKick, tabDef.get(defender))
      if(num > maxNeighbourLength):
        maxNeighbourLength = num
        maxDefender = defender
      tabDefSol.append(maxDefender)
      tabKick = self.removeKickStop(maxDefender, tabKick)
      tabDef.remove(maxDefender)
      return self.algoGlouton(tabKick, tabDef, tabDefSol)

	#Récupérer les valeurs des defenders en fonctions de leurs nom
  def chercheDefenders(self, tabDef):
    res = []
    for defender in tabDef:
      res.append(self.list_of_defencers.get(defender))
    return res

	#Verifie que le nombre de kicks bloquer est egale au total du nombre de kicks
  def allKicksStop(self, tabDef):
    #tableau kicks -> []
    #Parcours def
    #Si kick pas dans tableau alors add 
    #si taille tableau kick == nombre de kick a arreté alors good
    return True
	
  #Cherche le nombre de voisin en fonction de ceux de la list
  def numKickOfDefender(self, tabKick, defender):
    cpt = 0
    kickStopByDefender = self.list_of_defencers.get(defender)
    for kickStop in kickStopByDefender : 
      for kick in tabKick : 
        if(kickStop == kick):
          cpt = cpt + 1
    return cpt

  def removeKickStop(self, defender, tabKick):
    kickRemove = self.list_of_defencers.get(defender)
    for kick in kickRemove:
      tabKick.remove(kick)
    return tabKick
