import sys

def modifyDisMat(disMat, cityNum):
	x = []	#行
	y = []	#列
	for i in range(cityNum):		#全ての変数を最大化にする
		x.append(sys.maxsize)
		y.append(sys.maxsize)
	#各行の最小を求める
	for i in range(cityNum):	#行
		for j in range(cityNum):	#列
			if disMat[i][j] < x[i]:
				x[i] = disMat[i][j]
				print("i:"+str(i)+" 最小:" +str(x[i]))
		if x[i] == sys.maxsize:
			x[i] = 0
	#各行を最小の数で引く
	for i in range(cityNum):
		for j in range(cityNum):
			if disMat[i][j] != sys.maxsize:
				print("dismat:" +str(disMat[i][j])+" - "+str(x[i]))
				disMat[i][j] -= x[i]
				print("結果 dismat:" +str(disMat[i][j]))
	print("途中 dismat: "+str(disMat))
	print("--------------------------------")
	#各列の最小を求める
	for i in range(cityNum):
		for j in range(cityNum):
			if disMat[j][i] < y[i]:
				y[i] = disMat[j][i]
				print("i:"+str(i)+" 最小:" +str(y[i]))
		if y[i] == sys.maxsize:
			y[i] = 0				
	#各列を最小の数で引く
	for i in range(cityNum):
		for j in range(cityNum):
			if disMat[j][i] != sys.maxsize:
				print("dismat:" +str(disMat[j][i])+" - "+str(y[i]))
				disMat[j][i] -= y[i]
				print("結果 dismat:" +str(disMat[j][i]))
	print("cost: "+str(sum(x)+sum(y)))
	print("newDisMat: "+str(disMat))

disMat = [[1, 2, 9, 10], [30, 67, 1, 29], [98, 1, 32, 45], [4, 5, 1, 7]]
modifyDisMat(disMat, 4)