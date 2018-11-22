#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 9 20:34:02 2018

@author: abdulbasit
"""


import numpy as np
import math

#Common Function used by team to parse Data File and Build Distance matrix

def PreData(method):
		with open('burma14.tsp.txt') as f:
			num = 0 #city number
			find_num = False 
			temMat = []
			data = f.readlines()
			numJudge = 0

			for line in data:

				stringJudge = []
				line = line.rstrip('\n')
				stringJudge = line.split()

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
			#EU_2D
			if method == "eu":
				for i in range(num):
					for j in range(num):
						#计算两个城市之间的欧式距离
						if i != j:
							xd = corMat[i][0]-corMat[j][0]
							yd = corMat[i][1]-corMat[j][1]

							# temDis = (int)(np.sqrt(np.float((xd*xd + yd*yd) ) ) + 0.5)
							temDis = (int)(math.sqrt((xd*xd + yd*yd) ) + 0.5)

							disMat[i][j] = disMat[j][i] = temDis

##############################################################################

##############################################################################
			#GEO Distance
			if method == "geo":
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
					print np.float(PI * (deg + 5.0 * min / 3.0) / 180.0 )
					y = corMat[i][1]
					deg = (int)(y)
					min = np.float(y - deg)
					geoMat[i][1] = np.float(PI * (deg + 5.0 * min / 3.0) / 180.0 )
					print np.float(PI * (deg + 5.0 * min / 3.0) / 180.0 )
					#print geoMat                    
				for i in range(num):
					for j in range(num):
						if i != j:
							q1 = np.float( np.cos(geoMat[i][1] - geoMat[j][1]) )
							q2 = np.float( np.cos(geoMat[i][0] - geoMat[j][0]) )
							q3 = np.float( np.cos(geoMat[i][0] + geoMat[j][0]) )
							disMat[i][j] = (np.int64)( RRR * np.arccos( 0.5 * ((1.0 + q1) * q2 
								- (1.0 - q1) * q3) ) + 1.0 ) 

##############################################################################

			
			# disMat = np.around(disMat,decimals = 6)

		# 其
			return corMat,disMat,num;


# In[8]:








#Brute for for TSP
#Calling Parse daat function to get distance matrix and cordinates parsedd from file
cordinates,distance_matrix,cities = PreData('geo')


from itertools import permutations
from math import hypot
import timeit

#Starting time to calculate total executing time
start = timeit.default_timer()

#stores distances of each path
distances=[]
#current best distance, Defaults to infinity
bestdist=float('inf')
#current best path
bestpath=[]

#for permutation of all paths, For example for 4 cites 2^4= 16 paths 
for path in permutations( range(cities) ):
    #Initializing distanceeof this path
    dist=0
    #Summing distance of each cites in this path
    for num in range(cities-1):
        dist +=  distance_matrix[path[num]][path[num+1]]
    #Loop back distance, last to first city in the path
    dist+=distance_matrix[path[-1]][path[0]]
    #appending path distance to distance array(not of usejust fo debugging)
    distances.append(dist)
    #if currentpaths distance is better than best preious distance, replace and store it in best distance and best path
    if(dist<float('inf')):
        bestdist=dist
        bestpath=path

#print path,time,cost
stop = timeit.default_timer()
print "Minimum distance cost by brute force is "+str(bestdist)  
print "best path is "+str(bestpath)
print "time taken to calculate best route is "+str(round(stop - start,3))+" seconds"

