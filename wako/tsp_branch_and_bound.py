from time import time
import sys
import random
import copy

from ExtractDataVer2 import PreData

def BranchAndBound(disMat, cityNum):
	cost = sys.maxsize						# 現時点の木全体の最小コスト
	route = []								# cost の道順（city番号)
	startCityList = list(range(cityNum))	# スタート地点メモのリスト
	cityInfo =[]							#[[cityNumber,cost,newDisMat]] in the order of leaf
	minCostRoute =[]						# 最小コストのrouteをcityInfoで保存している
	LastTempI = 0
	tempCost = sys.maxsize
	tempRoute = []
	skipflag = 0							# 2周目以降判別flag
	tempI = 0
	tempNextCity = 0
	
	
	while len(startCityList) != 0:
		#スタート地点の準備
		cityList = list(range(cityNum))			# 行ったことないcity のリスト
		start = random.choice(startCityList)
		nowCity = start
		startCityList.remove(nowCity)				# スタート地点リストから削除
		branchStartCost, newDisMat = modifyDisMat(disMat, cityNum)	# スタート地点のMatとコストを入手
		cityInfo.append([start,branchStartCost,newDisMat])	# cityInfo に追加
		minCostRoute.append(0)					# スタート地点は絶対に通るので追加
		cityList.remove(cityInfo[-1][0])	# 訪れた街としてリストから削除
		print("------------start "+str(start)+" "+str(nowCity)+" --------------")
		# スタートのコストの時点でcostより多かったら処理しない（2周目以降
		if cost < branchStartCost:
			print("reject in start")
			break
		else:
			# 木が完成（全ての街に行くまで）回す
			while(len(cityList) != 0):
				# 現時点から各city のコストを求める
				#print("cityInfo: "+str(cityInfo))
				for city in cityList:
					cityCost, newDisMat = getCost(disMat, cityNum, nowCity, city, cityInfo[minCostRoute[-1]][1])
					cityInfo.append([city,cityCost,newDisMat])
				#print("cityInfo: "+str(cityInfo))
				# 一番コストの少ないcityを求める
#				print("イマココ")
				tempMinCost = sys.maxsize
				for j in range(LastTempI,len(cityInfo)):
#					print("j"+str(j))
#					print("cityInfo: "+str(cityInfo[j][0])+" "+str(nowCity))
					if tempMinCost > cityInfo[j][1] and cityInfo[j][0]!=nowCity:	# 最小コストの場合city とコストを記録
						tempMinCost = cityInfo[j][1]
						tempNextCity = cityInfo[j][0]
						tempI = j
#						print("更新")
#				print("一番コストの少ないcityに移動するよ")
				# 一番コストの少ないcity に移動
				LastTempI = j + 1						# 次はここから始めるため
				minCostRoute.append(tempI)
				nowCity = tempNextCity
#				print("cityList: "+str(cityList))
#				print("nowCity: "+str(nowCity))
				cityList.remove(nowCity)
				# 他の木全体のコストより大きかったらその時点で抜ける
				if tempMinCost > cost:
#					print("cost "+str(tempMinCost)+" higher than upper bound "+str(cost)+", skip:")
					skipflag = 1
					break

			if skipflag == 0:
				# 木の合計コストを求める(仮)
				for j in minCostRoute:
					tempCost = cityInfo[j][1]
					tempRoute.append(cityInfo[j][0])
				# 木の合計コストがその時までで最小だった場合置き換え
				if tempCost < cost:
					cost = tempCost
					route = tempRoute
			print("cost: "+str(cost))
			print("middle route: "+str(route))
			# 初期化
#			print("初期化されたよ")
			minCostRoute = []
			skipflag = 0
			tempRoute = []
			cityInfo = []
			nowCity = None
			LastTempI = 0

	return route

		
def modifyDisMat(disMat, cityNum):
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

def getCost(disMat, cityNum, nowCity, nextCity, costbefore):
	tempDisMat = copy.deepcopy(disMat)
	for i in range(cityNum):
		tempDisMat[nowCity][i] = sys.maxsize
		tempDisMat[i][nextCity] = sys.maxsize
	tempDisMat[nextCity][nowCity] = sys.maxsize
	cost, newDisMat = modifyDisMat(tempDisMat,cityNum)
	return [cost+disMat[nowCity][nextCity]+costbefore, newDisMat]


def calcDIS(CityOrderList, disMat):
	'''
	配列を渡されたらその配列の距離を計算する
	'''
	totalDis = 0
	for i in range(len(CityOrderList)):
		# nowCity と nextCity を決める	
		nowCity = CityOrderList[i]
		if nowCity == CityOrderList[-1]:
			nextCity = CityOrderList[0]
		else:
			nextCity = CityOrderList[i+1]
		totalDis += disMat[nowCity][nextCity]

	return totalDis



def printresult(route,disMat,TIME):
	print("route: "+str(route))
	print("total distance: "+str(calcDIS(route,disMat)))
	print("time taken: "+str(time()-TIME))

##### main #####
TIME = time()

filename = './dataset/burma14.tsp'
optAns = 3323

# initialization
disMat = PreData(filename,"geo",2)	# matrix that shows city distance
cityNum = PreData(filename,"geo",3)	# number of city total

route = BranchAndBound(disMat, cityNum)
printresult(route,disMat,TIME)