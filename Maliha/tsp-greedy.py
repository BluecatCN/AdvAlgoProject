# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:15:48 2018

@author: Maliha
"""
import numpy as np
from time import time
import math

def main():
	#loading data
    tspdatafile = 'datasets/burma14.txt'
    cities, disMat, numOfCities = PreProcessData(tspdatafile)
	    
	#calculating optimised path and time
    start_time = time()
    best_path = []
    best_length = float('inf')
    
    #Select a city one-by-one from the data, as the first city
    for index_start, start in enumerate(cities):
        path = [index_start]
        length = 0
        
        #get path for the selected first city
        index_next = index_start
        while len(path) < numOfCities:
            
			#getting the next nearest city
            best_distance = float('inf')

            for index, city in enumerate(cities):
                
                if index not in path:
                    distance = disMat[index_next][index]
                    
                    if distance < best_distance:
                        index_nearest_city = index
                        best_distance = distance

            #append the nearest city to path and select it as the next city
            length += best_distance
            path.append(index_nearest_city)
            index_next = index_nearest_city

        #adding length of "last node to first node" in total length
        length+=disMat[path[-1]][path[0]]
        
        #check if the selected first city gives a more short path else keep previous one
        if length < best_length:
            best_length = length
            best_path = path
    
    #Calculating time of computation
    total_time = time() - start_time
    
    #Printing the ordered sequence of nodes to visit and the cost of the proposed solution
    print("Path: %s" % best_path)
    print( "Length of the Path: %s" % best_length)
    print( "Time: %s seconds" % round(total_time,2))

#########Parsing Data and Computing Distance Matrix of Cities############################

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
    
if __name__ == "__main__":
	main()