#!/usr/bin/python3

import numpy
import sys
import json
import math


class AlgoExact :
  def __init__(self,dictNeighbors,list_of_defencers) :
    self.list_of_defencers = list_of_defencers
    self.dictNeighbors = dictNeighbors

  def solver(self):
    self.algoExactRec([],0)

  def algoExactRec(self, tabDef, currentDef):
    numDef = len(self.list_of_defencers)
    #Bloque si on a parcourut tous les défenseurs
    if(currentDef == numDef):
      return False
    for i in range(currentDef, numDef) :
      newTabDef = tabDef
      newTabDef.append(self.list_of_defencers.get(i))
      #Verifie si tous les tirs sont bloqué
      if(self.allKicksStop(newTabDef)):
        self.solution = self.chercheDefenders(newTabDef)
        return True
      #Relance l'algo avec un élément dans le tableau de plus
      return self.algoExactRec(newTabDef, i+1)

  def chercheDefenders(self, tabDef):
    res = []
    for defender in tabDef:
      res.append(self.list_of_defencers.get(defender))
    return res

	#Verifie que le nombre de kicks bloquer est egale au total du nombre de kicks
  def allKicksStop(self, tabDef):
    return True
		#tableau kicks -> []
		#Parcours def
		#Si kick pas dans tableau alors add 
		#si taille tableau kick == nombre de kick a arreté alors good