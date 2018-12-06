'''
	steps
	1. decide starting city by random
	2. while until going to all the city
		decide next city by random
		if have not been to the city
			add distance
			now = next
			record as city arrived
		else
			reselect the next city
	3. go back to the starting city
	4. print total distance and route
'''
import numpy as np
import math
import random
import sys
from time import time

from ExtractDataVer2 import PreData

def RandomApproach(start, disMat, cityNum):
	visited_mat = [start]	# list for visited city
	nowcity = start	# city @ 
	totalDis = 0	# for total distance

	while len(visited_mat) != cityNum:
		nextcity = random.randrange(cityNum)	# next city

		if checkcity(nextcity, visited_mat):
		# if its a new city
			totalDis += disMat[nowcity][nextcity]
			nowcity = nextcity
			visited_mat.append(nowcity)

	# after going to all the city, we need to go back to the starting point
	visited_mat.append(start)
	totalDis += disMat[nowcity][start]

	return visited_mat,totalDis


def checkcity(nextcity, visited_mat):
	# check whether you have been to the city or not
	for i in visited_mat:
		if nextcity == i:
			# already have been to the city
			return  0
	return 1

def printresult(route, distance, opt, TIME):
	print("route: " + str(route))
	print("total distance: " + str(distance))
	print("Error persentage: "+str(round((distance/opt-1)*100,2)))
	print("time taken: " + str(round(time()-TIME,2)))

##### main #####	
startTIME = time()
#filename = './dataset/burma14.tsp'
#optAns = 3323
#filename = './dataset/berlin52.tsp'
#optAns = 7542
filename = './dataset/kroA100.tsp'
optAns = 21282

# initialization
disMat = PreData(filename,"geo",2)	# matrix that shows city distance
cityNum = PreData(filename,"geo",3)	# number of city total

#random approach
start = random.randrange(cityNum)	# starting city
route = RandomApproach(start, disMat, cityNum)
printresult(route[0],route[1],optAns,startTIME)

'''
# if you want to run them multiple time

count = 0
finalDis = sys.maxsize	# total distance (final answer)
finalRoute = []	# route (final answer)

while count < len(disMat)*1000*2:
	start = random.randrange(cityNum)	# starting city
	#random approach
	route = RandomApproach(start, disMat, cityNum)
#	print(route)
	if finalDis > route[1]:
		finalDis = route[1]
		finalRoute = route[0]
	count += 1
printresult(finalRoute, finalDis, optAns, startTIME)
'''
