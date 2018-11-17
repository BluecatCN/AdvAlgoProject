#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-29 18:07:50
# @Author  : mutudeh (josephmathone@gmail.com)
# @Link    : ${link}
# @Version : $Id$

import numpy as np
import math
import tsplib95 as tp


def PreData(method):

	name = 'D:/Study/Jean Monnet/Advanced Algoirthm/Project/Data/gr21.tsp'
	tsp = tp.load_problem(name)
	num = tsp.dimension 
	numJudge = num
	temMat = []

	disMat = np.zeros((num,num),dtype = np.float64)


	if tsp.edge_weight_type == 'EXPLICIT':
		for i in range(num):
			for j in range(num):
				disMat[i][j] = disMat[j][i] = tsp.wfunc(i,j)
		return disMat,num;

	else:
		with open(name) as f:

			find_num = False 
			temMat = []
			data = f.readlines()
			for line in data:

				stringJudge = []
				line = line.rstrip('\n') 
				stringJudge = line.split()
				typeDis = "" 

				if find_num:	
			
					if numJudge:
						string_data = line.split()
						temMat.append(string_data)
						numJudge = numJudge - 1
						
					else:
						break

				
				if stringJudge[0] == "NODE_COORD_SECTION":
					
					find_num = True

			corMat = np.array(temMat)
			corMat = corMat.astype(np.float64)
			corMat = corMat[:,1:3]
##########################################################################
			#EU_2D
			if method == "eu":
				for i in range(num):
					for j in range(num):
						if i != j:
							xd = corMat[i][0]-corMat[j][0]
							yd = corMat[i][1]-corMat[j][1]

							temDis = (int)(math.sqrt((xd*xd + yd*yd) ) + 0.5)

							disMat[i][j] = disMat[j][i] = temDis

	##############################################################################

	##############################################################################
			#GEO Distance
			if method == "geo":

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
		return disMat,num;