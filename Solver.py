#!/usr/bin/python3

import numpy
import sys
import json

from goal import *
from problem import *
from solution import *
from board import *

step =0.25
# write  defenders position in self.solution and call self.read_in_file() for create .json
class Solver :
	def __init__(self,problem) :
		self.problem = problem
		self.solution = []
		self.name_file = 'sol.json'
		

	def solver(self,file_pb):
		self.generate_all_posible_def(file_pb)
		self.write_in_file()
		#self.read_file()


	def write_in_file(self,) :
		mandatory_keys = "defenders"
		out = {}
		out[mandatory_keys] = self.solution
		with open(self.name_file, 'w') as jf:
			json.dump(out,jf)
			print("Create file : " + self.name_file)

	def read_file(self) :
		with open(self.name_file,'r') as f :
			data = json.load(f)


	def generate_all_posible_def(self,file_pb) :
		file = open(file_pb,)
		data = json.load(file)
		len_filed = data["field_limits"]
		width = len_filed[0]
		heigth = len_filed[1]
		list_defs = []
		print("W= "+str(width) + ", H= "+ str(heigth))
		for x in numpy.arange(width[0],width[1],step) :
			for y in  numpy.arange(heigth[0],heigth[1],step) :
				coord = [x,y]
				self.solution.append(coord)
		
		#coordinates = [(x, y) for x in xrange(width) for y in xrange(height)]

