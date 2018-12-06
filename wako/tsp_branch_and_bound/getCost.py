import copy
import sys

from modifyDisMat import modifyDisMat

def getCost(disMat, cityNum, nowCity, nextCity, costbefore):
	tempDisMat = copy.deepcopy(disMat)
	for i in range(cityNum):
		tempDisMat[nowCity][i] = sys.maxsize
		tempDisMat[i][nextCity] = sys.maxsize
	tempDisMat[nextCity][nowCity] = sys.maxsize
	cost, newDisMat = modifyDisMat(tempDisMat,cityNum)
#	print("cost: "+str(cost))
	return [cost+disMat[nowCity][nextCity]+costbefore, newDisMat]