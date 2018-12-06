import copy
import sys

def modifyDisMat(disMat, cityNum):
#	print("function modifyDismat")
	x = []	#行
	y = []	#列
	tempNewDisMat=copy.deepcopy(disMat)
	for i in range(cityNum):	#全ての変数を最大化にする
		x.append(sys.maxsize)
		y.append(sys.maxsize)
	#各行の最小を求める
	for i in range(cityNum):	#行
		for j in range(cityNum):	#列
			if tempNewDisMat[i][j] < x[i]:
				x[i] = tempNewDisMat[i][j]
		if x[i] == sys.maxsize:
			x[i] = 0
	#各行を最小の数で引く
	for i in range(cityNum):
		for j in range(cityNum):
			if tempNewDisMat[i][j] != sys.maxsize:
				tempNewDisMat[i][j] -= x[i]	
	#各列の最小を求める
	for i in range(cityNum):
		for j in range(cityNum):
			if tempNewDisMat[j][i] < y[i]:
				y[i] = tempNewDisMat[j][i]
		if y[i] == sys.maxsize:
			y[i] = 0				
	#各列を最小の数で引く
	for i in range(cityNum):
		for j in range(cityNum):
			if tempNewDisMat[j][i] != sys.maxsize:
				tempNewDisMat[j][i] -= y[i]
	return sum(x)+sum(y),tempNewDisMat # cost, new disMat