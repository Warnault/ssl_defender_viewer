#!/usr/bin/python3

import numpy
import sys
import json
import math

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
		graph = self.createGraph()
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
		initialized_x = self.init_pos_x(data["opponents"])+step
		[born_min_y,born_max_y] = self.init_pos_y( data["opponents"], heigth, data["goals"][0]["posts"] )
		last_x = initialized_x
		last_y = born_min_y
		for x in numpy.arange(initialized_x,width[1],step):
			if( (x==initialized_x) or (last_x+data["robot_radius"] < x-data["robot_radius"]) ):
				for y in  numpy.arange(born_min_y,born_max_y,step):
					last_x = x
					if( (y==born_min_y) or (last_y+data["robot_radius"] < y-data["robot_radius"]) ):
						last_y = y
						coord = [x,y]
						if(not collision_with_ennemy(file_pb,coord)):
							self.solution.append(coord)
		#coordinates = [(x, y) for x in xrange(width) for y in xrange(height)]

	def init_pos_x(self,opponent) :
		x = opponent[0][0]
		for e in opponent:
			if( x>e[0] ): 
				x=e[0]
		return x

	def init_pos_y(self, opponent, coords_y, goal_pos):
		[min_y, max_y] = coords_y
		[min_y_b, max_y_b] = [goal_pos[0][1],goal_pos[1][1]]
		for e in opponent:
			if( e[1]>min_y and e[1]<min_y_b ):  min_y = e[1]
			elif( e[1]<max_y and e[1]>max_y_b ): max_y = e[1]
		return [min_y, max_y]

	def createGraph(self):
		problem = self.problem
		defenders = self.solution
		new_defenders =[]
		graph = {}
		kicks = shootOnTarget(problem)
		for defender in defenders:
			allkicksIntercepted = []
			for kick in kicks:
				collide_point = segmentCircleIntersection(
					kick[0], kick[1], defender, problem.robot_radius)
				if not collide_point is None :
					new_defenders.append(defender)
					allkicksIntercepted += kick
					#clé: defenseur --> "x,y"
					key = str(defender[0])+","+str(defender[1])
					#valeur: tableau des (opposant,tirs) arrêté
					graph[key] = allkicksIntercepted
		self.solution = new_defenders
		return graph

def lies_in_range(interval,coord,radius):
	values = [(coord-radius),coord,(coord+radius)]
	for val in values:
		if( val>=interval[0] and val<=interval[1] ): 
			return True
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

def shootOnTarget(problem):
	kicks = []
	for opp_id in range(problem.getNbOpponents()):
		opponent = problem.getOpponent(opp_id)
		kick_dir = 0
		while kick_dir < 2*math.pi :
			for goal in problem.goals :
				kick_result = goal.kickResult(opponent, kick_dir)
				if not kick_result is None:
					sommet = []
					sommet.append(opponent)
					sommet.append(kick_result)
					kicks.append(sommet)
			kick_dir += problem.theta_step
	#print(kicks)
	return kicks
