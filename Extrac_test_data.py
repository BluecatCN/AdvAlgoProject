#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-29 18:07:50
# @Author  : mutudeh (josephmathone@gmail.com)
# @Link    : ${link}
# @Version : $Id$

import numpy as np
import math
import tsplib95 as tp


def PreData(name_city):
#take tsp file path as input 
#output distance matrix and number of cities 

	name = name_city
	tsp = tp.load_problem(name)
	num = tsp.dimension #number of cities 
	numJudge = num
	temMat = []
	# the followng is to compute the distance matrix

	#distance matrix initialization
	disMat = np.zeros((num,num),dtype = np.float64) 
	process = False
	method = tsp.edge_weight_type


	if method == 'EXPLICIT':
		process = True
		for i in range(num):
			for j in range(num):
				disMat[i][j] = disMat[j][i] = tsp.wfunc(i,j)
		return disMat,num;

	else:
		with open(name) as f:

			#when flag is true, the next line will be the data we want 
			find_num = False
			temMat = []
			data = f.readlines()
			for line in data:

				stringJudge = []
				#eliminate the line break
				line = line.rstrip('\n') 
				stringJudge = line.split()

				if find_num:	
					#split data with blank
					if numJudge:
						string_data = line.split()
						temMat.append(string_data)
						numJudge = numJudge - 1
						
					else:
						break

				
				if stringJudge[0] == "NODE_COORD_SECTION":
					# after NODE_COORD_SECTION, the next line will be the data
					find_num = True

			# corMat = map(float,temMat)
			corMat = np.array(temMat)
			corMat = corMat.astype(np.float64)
			corMat = corMat[:,1:3]
##########################################################################
			#EU_2D
			if method == "EUC_2D":
				process = True
				A = np.matrix(corMat)
				B = np.matrix(corMat)

				BT = B.transpose()
				vecProd = A * BT
				SqA =  A.getA()**2
				sumSqA = np.matrix(np.sum(SqA, axis=1))
				sumSqAEx = np.tile(sumSqA.transpose(), (1, vecProd.shape[1]))    
				SqB = B.getA()**2
				sumSqB = np.sum(SqB, axis=1)
				sumSqBEx = np.tile(sumSqB, (vecProd.shape[0], 1))    
				SqED = sumSqBEx + sumSqAEx - 2*vecProd   
				ED = (SqED.getA())**0.5
				ED = ED.astype(int)

			if method == "CEIL_2D":
				process = True
				A = np.matrix(corMat)
				B = np.matrix(corMat)

				BT = B.transpose()
				vecProd = A * BT
				SqA =  A.getA()**2
				sumSqA = np.matrix(np.sum(SqA, axis=1))
				sumSqAEx = np.tile(sumSqA.transpose(), (1, vecProd.shape[1]))    
				SqB = B.getA()**2
				sumSqB = np.sum(SqB, axis=1)
				sumSqBEx = np.tile(sumSqB, (vecProd.shape[0], 1))    
				SqED = sumSqBEx + sumSqAEx - 2*vecProd   
				ED = (SqED.getA())**0.5
				ED = np.round(ED)
	##############################################################################

	##############################################################################
			#GEO Distance
			if method == "GEO":
				# Latitude is geoMat[:][0]
				# longitude is geoMat[:][1]

				process = True
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
		if process:
			return disMat,num
		else:
			print("The method is not defined!")