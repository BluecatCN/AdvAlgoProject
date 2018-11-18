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
#此函数将获取一个文件名，文件名为 TSP 数据 ----  此项尚未完成
#并将读取数据最终输出城市坐标以及城市数目

	name = 'D:/Study/Jean Monnet/Advanced Algoirthm/Project/Data/bier127.tsp'
	tsp = tp.load_problem(name)
	num = tsp.dimension #统计城市数目
	numJudge = num
	temMat = []
	# 以下计算城市距离矩阵
	disMat = np.zeros((num,num),dtype = np.float64) #初始化距离矩阵


	if tsp.edge_weight_type == 'EXPLICIT':
		for i in range(num):
			for j in range(num):
				disMat[i][j] = disMat[j][i] = tsp.wfunc(i,j)
		return disMat,num;

	else:
		with open(name) as f:

			find_num = False # 标记找到的下一行即为真实城市数据
			temMat = []
			data = f.readlines()
			for line in data:

				stringJudge = []
				line = line.rstrip('\n') # 读取文件时逐行读取的话，在每一行的末尾会录入一个 \n 换行符
				stringJudge = line.split()
				typeDis = ""  #表示距离的种类

				if find_num:	
					#将数据按照空格分开
					if numJudge:
						string_data = line.split()
						temMat.append(string_data)
						numJudge = numJudge - 1
						
					else:
						break

				
				if stringJudge[0] == "NODE_COORD_SECTION":
					# 在 NODE_COORD_SECTION 的下一行即为真实数据
					find_num = True

			# corMat = map(float,temMat)
			corMat = np.array(temMat)
			corMat = corMat.astype(np.float64)
			corMat = corMat[:,1:3]
##########################################################################
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