#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 15:27:02 2018

@author: abdulbasit
"""



from sys import argv
from math import hypot
from timeit import default_timer
from random import randrange
import numpy as np


def PreProcessData(tspdatafile):
		with open(tspdatafile) as f:
			num = 0 #city number
			find_num = False 
			temMat = []
			data = f.readlines()
			method=''
			numJudge = 0
            
			for line in data:

				stringJudge = []
				line = line.rstrip('\n')
				stringJudge = line.split()
                
				if stringJudge[0]=='EDGE_WEIGHT_TYPE:':
					method = stringJudge[1]
                    
				if stringJudge[0] == 'DIMENSION:':	
					numJudge = np.int(stringJudge[1])

				if find_num:	
					if numJudge:
						string_data = line.split()
						temMat.append(string_data)
						numJudge = numJudge - 1						
					else:
						break
					num = num + 1						
				if stringJudge[0] == "NODE_COORD_SECTION":
					find_num = True

			
			corMat = np.array(temMat)
			corMat = corMat.astype(np.float64)
			corMat = corMat[:,1:3]

			disMat = np.zeros((num,num),dtype = np.float64)

####################EU_2D######################################################
			
			if method == "EUC_2D":
				for i in range(num):
					for j in range(num):
						
						if i != j:
							xd = corMat[i][0]-corMat[j][0]
							yd = corMat[i][1]-corMat[j][1]

							# temDis = (int)(np.sqrt(np.float((xd*xd + yd*yd) ) ) + 0.5)
							temDis = (int)(math.sqrt((xd*xd + yd*yd) ) + 0.5)

							disMat[i][j] = disMat[j][i] = temDis

#####################GEO DISTANCE#############################################
			
			if method == "GEO":
				# Latitude is geoMat[:][0]
				# longitude is geoMat[:][1]

				geoMat = np.zeros((num,2),dtype = np.float64)
				PI = np.float64(3.141592)
				RRR = np.float64(6378.388)

				for i in range(num):
					x = corMat[i][0]
					deg = (int)(x)
					min = np.float(x - deg)
					geoMat[i][0] = np.float(PI * (deg + 5.0 * min / 3.0) / 180.0 )

					y = corMat[i][1]
					deg = (int)(y)
					min = np.float(y - deg)
					geoMat[i][1] = np.float(PI * (deg + 5.0 * min / 3.0) / 180.0 )

				for i in range(num):
					for j in range(num):
						if i != j:
							q1 = np.float( np.cos(geoMat[i][1] - geoMat[j][1]) )
							q2 = np.float( np.cos(geoMat[i][0] - geoMat[j][0]) )
							q3 = np.float( np.cos(geoMat[i][0] + geoMat[j][0]) )
							disMat[i][j] = (np.int64)( RRR * np.arccos( 0.5 * ((1.0 + q1) * q2 
								- (1.0 - q1) * q3) ) + 1.0 ) 

##############################################################################
#corMat has cordinates of the cities，
#disMat is the distance matrix between cities,
#num is the number of nodes/cities present in the dataset
			return corMat,disMat,num;

##############################################################################

#Calculates and returns routes's/path's distance
def calc_route_distance(path,distance_matrix):
	dist=0
	for num in range(len(path)-1):
            dist +=  distance_matrix[path[num]][path[num+1]]
            #print()            
	dist+=distance_matrix[path[-1]][path[0]]
	return dist

#swap main logic. it will use 2-opt swap for improvement till no improvement can be acheived.
#Best path can be different as per start node selection
#returns best path
def swaptsp(route,distance_matrix):
	
	improvement = True
	best_route = route
	best_distance = calc_route_distance(route,distance_matrix)

#while there can be some improvement
	while improvement: 
		improvement = False
		for i in range(len(best_route) - 1):
			for k in range(i+1, len(best_route)):
				n_route = best_route[0:i]
				n_route.extend(reversed(best_route[i:k + 1]))
				n_route.extend(best_route[k+1:])
				new_route=n_route
				new_distance = calc_route_distance(new_route,distance_matrix)
				if new_distance < best_distance:
					best_distance = new_distance
					best_route = new_route
					improvement = True
					break #breaks if there is improvment
			if improvement:
				break
	
	return best_route


def main():
    route,distance_matrix,lencities = PreProcessData("datasets/burma14.txt")
    route = [i for i in range(len(route))]
    print(calc_route_distance([1, 0, 9, 8, 10, 7, 12, 6, 11, 5, 4, 3, 2, 13],distance_matrix))
    r = None

    start = default_timer() #start time of running 2opt
    route = swaptsp(route,distance_matrix)
    end = default_timer()   #end time of running 2opt
    print("Original input file : Burma")
    print("Dimension : " + str(len(route)))
    print(route)
    print("Total Distance : " + str(calc_route_distance(route,distance_matrix)))
    print("Time to run 2opt : %.2f seconds" % (end-start))

if __name__ == "__main__":
	main()
