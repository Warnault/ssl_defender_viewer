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

		#Contient tous les kickcs marquant
		self.kicks = []
		#Tableau d'adjacence {tir -> def & def -> tir}
		self.dictNeighbors={}

		#Associe une valeur a un nom:
		#T0 -> [x, y] 
		self.tabKicks = {}
		#D0 -> [x, y] 
		self.tabDefs = {}

		#Solution:
		self.algoExact([], 0)
		

	def solver(self,file_pb):
		#Genere tous les défenseurs possible
		self.generate_all_posible_def(file_pb)
		#Genere tous les tirs marquant
		self.shootOnTarget()
		#Garde les défenseurs qui bloques les tirs
		self.defendersStopKicks()

		#Crée le dictionnaire avec nom: position
		self.createNameArray()

		#Crée list d'adjacence
		self.dictNeighbors = self.defendersNeighbors()
		dictKick = self.kicksNeighbors()
		self.dictNeighbors.update(dictKick)

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

	def defendersStopKicks(self):
		problem = self.problem
		defenders = self.solution
		new_defenders =[]
		for defender in defenders:
			intercepted = False
			for kick in self.kicks:
				collide_point = segmentCircleIntersection(
					kick[0], kick[1], defender, problem.robot_radius)
				if not collide_point is None:
					intercepted = True
			if(intercepted): 
				new_defenders.append(defender)
		self.solution = new_defenders
		

	def shootOnTarget(self):
		problem = self.problem
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
						self.kicks.append(sommet)
				kick_dir += problem.theta_step

	def defendersNeighbors(self):
		problem = self.problem
		defenders = self.solution
		dict = {}
		for defender in defenders:
			tabKick = []
			intercepted = False
			for kick in self.kicks:
				collide_point = segmentCircleIntersection(
					kick[0], kick[1], defender, problem.robot_radius)
				if not collide_point is None :
					nameKicked = findKey(self.tabKicks, kick)
					tabKick.append(nameKicked)
					intercepted = True
			if(intercepted) :
				nameDefender = findKey(self.tabDefs, defender)
				dict[nameDefender] = tabKick
		return dict

	def kicksNeighbors(self):
		problem = self.problem
		defenders = self.solution
		dict = {}
		for kick in self.kicks:
			tabDefs = []
			intercepted = False
			for defender in defenders:
				collide_point = segmentCircleIntersection(
					kick[0], kick[1], defender, problem.robot_radius)
				if not collide_point is None :
					nameDefs = findKey(self.tabDefs, defender)
					tabDefs.append(nameDefs)
					intercepted = True
			if(intercepted) :
				nameKicked = findKey(self.tabKicks, kick)
				dict[nameKicked] = tabDefs
		return dict		
		
	def createNameArray(self):
		self.tabKicks = giveName(self.kicks, "T")

		self.tabDefs = giveName(self.solution, "D")

	def algoExact(self, tabDef, currentDef):
		numDef = len(self.tabDefs)
		#Bloque si on a parcourut tous les défenseurs
		if(currentDef == numDef):
			return False
		for i in range(currentDef, numDef) :
			newTabDef = tabDef
			newTabDef.append(self.tabDefs.get(i))
			#Verifie si tous les tirs sont bloqué
			if(self.allKicksStop(newTabDef)):
				self.solution = self.chercheDefenders(newTabDef)
				return True
			#Relance l'algo avec un élément dans le tableau de plus
			return self.algoExact(newTabDef, i+1)

	def algoGlouton(self, tabKick, tabDef):
		tabKickLength = len(tabKick)
		tabDefLength = len(tabDef)
		maxNeighbourLength = 0
		if(tabKickLength):
			self.solution = self.chercheDefenders(newTabDef)
			return True
		if(tabDefLength):
			return False
		for defender in tabDef:
			num = self.numKickOfDefender(tabKick, tabDef.get(defender)):
			if(num > maxNeighbourLength)
				maxNeighbourLength = num
		
	
	#Récupérer les valeurs des defenders en fonctions de leurs nom
	def chercheDefenders(self, tabDef):
		return []

	#Verifie que le nombre de kicks bloquer est egale au total du nombre de kicks
	def allKicksStop(self, tabDef):
		return True
	
	#Cherche le nombre de voisin en fonction de ceux de la list
	def numKickOfDefender(self, tabKick, tabDef):
		return 0


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

def collision(tab, coord, radius):
	for e in tab:
		interval_x = [(e[0]-radius),(e[0]+radius)]
		interval_y = [(e[1]-radius),(e[1]+radius)]
		if( lies_in_range(interval_x,coord[0],radius) and lies_in_range(interval_y,coord[1],radius)):
			return True
	return False

def giveName(tab, letter): 
	num = 0
	dict = {}
	for element in tab:
		name = letter + str(num)
		dict[name] = element
		num += 1
	return dict

def findKey(dict, value):
	for key in dict :
		val = dict.get(key)
		if str(val) == str(value):
			return key
	return None
