#!/usr/bin/python3

import numpy
import sys
import json

from goal import *
from problem import *
from solution import *
from board import *

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
		step = data["pos_step"]
		last_x = width[0]
		last_y = heigth[0]
		print("W= "+str(width) + ", H= "+ str(heigth))
		for x in numpy.arange(width[0],width[1],step):
			if( (x==width[0]) or (last_x+data["robot_radius"] < x-data["robot_radius"]) ):
				for y in  numpy.arange(heigth[0],heigth[1],step):
					last_x = x
					if( (y==heigth[0]) or (last_y+data["robot_radius"] < y-data["robot_radius"]) ):
						last_y = y
						coord = [x,y]
						if(not collision_with_ennemy(file_pb,coord)): 
							self.solution.append(coord)
		
		#coordinates = [(x, y) for x in xrange(width) for y in xrange(height)]


def lies_in_range(interval,coord,radius):
	values = [(coord-radius),coord,(coord+radius)]
	for val in values:
		if( val>=interval[0] and val<=interval[1] ): 
			print("pass")
			return True
	#print("nontefghdf")
	return False
	
def collision_with_ennemy(file_pb,coord):
	file = open(file_pb,)
	data = json.load(file)
	opponent = data["opponents"]
	radius = data["robot_radius"]
	for e in opponent:
		interval_x = [(e[0]-radius),(e[0]+radius)]
		interval_y = [(e[1]-radius),(e[1]+radius)]
		if( lies_in_range(interval_x,coord[0],radius) and lies_in_range(interval_y,coord[1],radius)):
			return True
	return False
