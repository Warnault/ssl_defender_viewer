#!/usr/bin/python3

import numpy
import sys
import json

from goal import *
from problem import *
from solution import *
from board import *

class Solver :
	def __init__(self,problem) :
		self.problem = problem
		self.solution = []

	def solving(self) :
		mandatory_keys = ["defenders"]
		sol = {}
		sol[mandatory_keys[0]] = [12.0,52.0]
		open('sol.json','w').write(json.dumps(sol))
		sys.exit(sol)
