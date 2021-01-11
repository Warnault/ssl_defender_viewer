#!/usr/bin/python3

from algorithm.AlgoExact import *
from algorithm.AlgoGlouton import *

def callOfAlgoExect(dictNeighbors,list_of_defencers,list_of_goals):
  return AlgoExact(dictNeighbors,list_of_defencers,list_of_goals)

def callOfAlgoGlouton(dictNeighbors,list_of_defencers,list_of_goals):
  return AlgoGlouton(dictNeighbors,list_of_defencers,list_of_goals)
  