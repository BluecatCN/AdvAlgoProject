#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-29 18:07:50
# @Author  : mutudeh (josephmathone@gmail.com)
# @Link    : ${link}
# @Version : $Id$

# @Editor	: YukiWAKO (snow.csf@gmail.com)
# changed comment language to English
# added option, filename variables to the function

import numpy as np
import math

def PreData(filename,method,option):
		with open(filename) as f:
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

			# Calculate the city distance matrix below
			disMat = np.zeros((num,num),dtype = np.float64) # Initialization distance matrix
##########################################################################
			#EU_2D
			if method == "eu":
				for i in range(num):
					for j in range(num):
						# Calculate the Euclidean distance between two cities
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

			# Distance matrix retains two decimal places
			# disMat = np.around(disMat,decimals = 6)

		# corMat is the city coordinate matrix
		# disMat is the city distance matrix
		# num-1 is the number of cities
		'''
			option list
			0: all
			1: corMat - city coordinate matrix
			2: disMat - city distance matrix
			3: num - number of cities
		'''
		if option == 1:
			return corMat
		if option == 2:
			return disMat
		if option == 3:
			return num
		if option == 0:
			return corMat,disMat,num
