#!/usr/bin/python3
import pygame
import sys
import json

from board import *
from Solver import *
from algorithm.callOfAlgo import callOfAlgoExect, callOfAlgoGlouton
 

#if (len(sys.argv) < 4):
#  sys.exit("Usage: " + sys.argv[0] + "<version (1:prof /2:la notre)> <problem.json> <solution.json>")

version_path = sys.argv[1]
problem_path = sys.argv[2]
solution_path = sys.argv[3]

if ( len(sys.argv) >4):
	algo_path = sys.argv[4]


if (version_path == '1') :
	with open(problem_path) as problem_file:
		problem = Problem(json.load(problem_file))
	with open(solution_path) as solution_file:
		solution = Solution(json.load(solution_file))
	print(solution.defenders.size/2)
	b = Board(problem, solution)
	b.run()

elif (version_path == '2' or version_path == '3'):
	algo = None
	if(algo_path == "-e"):
		algo = callOfAlgoExect
	elif(algo_path == "-g"):
		algo = callOfAlgoGlouton
	else:
		sys.exit("Error: the type of algorithm is unknown !")
	with open(problem_path) as problem_file:
		problem = Problem(json.load(problem_file))
	with open(solution_path,'a') as solution_file:
		if(version_path== '2'):
			solver = Solver(solution_path, problem,algo)
		else:
			solver =Solver(solution_path, problem,algo,True)
		solver.solver(problem_path)
	print('exec succes')

else :
	 sys.exit("Usage: " + sys.argv[0] + " <version> <problem.json> <solution.json> \n version 1 : prof \n version 2 : la notre")

sys.exit()
