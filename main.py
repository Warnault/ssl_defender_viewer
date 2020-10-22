#!/usr/bin/python3
import pygame
import sys
import json

from board import *
from Solver import *

if (len(sys.argv) < 4):
  sys.exit("Usage: " + sys.argv[0] + "<version (1:prof /2:la notre)> <problem.json> <solution.json>")

version_path = sys.argv[1]
problem_path = sys.argv[2]
solution_path = sys.argv[3]

if (version_path == "1") :
	with open(problem_path) as problem_file:
		problem = Problem(json.load(problem_file))
	with open(solution_path) as solution_file:
		solution = Solution(json.load(solution_file))
	b = Board(problem, solution)
	b.run()


elif (version_path == "2"):
	with open(problem_path) as problem_file:
		problem = Problem(json.load(problem_file))
	with open(solution_path) as solution_file:
		solver = Solver(problem)
		solver.solver(problem_path)
		solution = Solution(json.load(solution_file))
	#b = Board(problem, solution)
	#b.run()
else :
	 sys.exit("Usage: " + sys.argv[0] + " <version> <problem.json> <solution.json> \n version 1 : prof \n version 2 : la notre")

sys.exit()
