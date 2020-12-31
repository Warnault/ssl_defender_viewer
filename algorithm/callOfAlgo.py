#!/usr/bin/python3

from algorithm.AlgoExact import *
from algorithm.AlgoGlouton import *

def callOfAlgoExect(solution,list_of_defencers):
  algoExact =  AlgoExact(solution,list_of_defencers)
  print("Exect")

def callOfAlgoGlouton(solution,list_of_defencers):
  algoGlouton = AlgoGlouton(solution,list_of_defencers)
  print("Glouton")