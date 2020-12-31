#!/usr/bin/python3

from algorithm.AlgoExact import *
from algorithm.AlgoGlouton import *

def callOfAlgoExect(dictNeighbors,list_of_defencers):
  return AlgoExact(dictNeighbors,list_of_defencers)
  print("Exect")

def callOfAlgoGlouton(dictNeighbors,list_of_defencers):
  return AlgoGlouton(dictNeighbors,list_of_defencers)
  print("Glouton")