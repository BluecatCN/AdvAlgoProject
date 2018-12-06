from time import time
import sys
import random

from ExtractDataVer2 import PreData
from calcDIS import calcDIS
from getCost import getCost
from modifyDisMat import modifyDisMat

def printresult(route, disMat, TIME):
	print("route: "+str(route))
	print("total distance: "+str(calcDIS(route,disMat)))
	print("time taken: "+str(time()-TIME))
def BranchAndBound(disMat, cityTotal):
	upper = sys.maxsize			# upper bound
	route = []					# cost における道順(city番号)
	startCityList = list(range(cityTotal))	# 最初のcityのメモ

	while len(startCityList) != 0:			# 全てのスタート地点を試す
		# 初期化を兼ねた　変数宣言
		cityList = list(range(cityTotal))		# 巡回cityのメモ、行ったことない場所が入る
		cityInfo = []							# [[cityNumber,cost,newDisMat]] in the order of leaf
		
		nowCity = None							# 現在地点
		continueFrom = 0						# 木構造で処理するときの開始点
		tempRoute = []							# 最小コストを記録する一時的なルート, 表記は葉の番号
		tempRealRoute=[]						# 仮のroute, 実際のcity number で表記されているもの
		skipflag = 0							# 途中段階でスキップする場合のための flag

		#スタートの準備
		print("----------- start -----------")
		start = random.choice(startCityList)
		startCityList.remove(start)	# スタート地点として選ばれたものを削除
		nowCity = start 			# スタート地点を現在の場所として記録
		cityList.remove(nowCity)	# 巡回済みの場所としてリストから削除
		branchStartCost, newDisMat = modifyDisMat(disMat, cityTotal) # スタート地点の disMat と cost の入手
		cityInfo.append([start, branchStartCost, newDisMat])
		tempRoute.append(0)

#		print("start city: "+str(start)+" list:"+str(cityList))

		# start cost が upper より大きかった場合処理しない（２回目以降
		if upper < branchStartCost:
			break
		else:
			while len(cityList) != 0:
				# 現時点から各 city のコストを求める
				for nextCity in cityList:
					cityCost, newDisMat = getCost(disMat, cityTotal, nowCity, nextCity, cityInfo[tempRoute[-1]][1])
					cityInfo.append([nextCity, cityCost, newDisMat])

#				print("----------- finish define cost -----------")

				# 現時点から一番少ないコストのcityを求める
				cost = sys.maxsize									# 現時点における木全体の最小コスト
				for j in range(continueFrom,len(cityInfo)):
					if cost > cityInfo[j][1] and cityInfo[j][0]!=nowCity:
						cost = cityInfo[j][1]
						tempNextCity = cityInfo[j][0]
						tempJ = j
#						print("temp next city update done")

#				print("----------- finish chooseing next city -----------")
#				print("tempNextCity: " +str(tempNextCity))
#				print("cityList: " +str(cityList))

				# コストが一番少ない city に移動
				continueFrom = j+1
				tempRoute.append(tempJ)
				nowCity = tempNextCity
				cityList.remove(nowCity)

				# 現時点のcost が upper よりも大きくなった場合やめる
				if cost > upper:
					skipflag = 1
					break

			# upper の更新
			if skipflag == 0:
				for j in tempRoute:
					tempRealRoute.append(cityInfo[j][0])
				if cost < upper:
					upper = cost
					route = tempRealRoute
#			print("route: "+str(route))

	return route

##### main #####
TIME = time()

filename = './dataset/burma14.tsp'
optAns = 3323

# initialization
disMat = PreData(filename,"geo",2)	# matrix that shows city distance
cityTotal = PreData(filename,"geo",3)	# total number of city

route = BranchAndBound(disMat, cityTotal)
printresult(route,disMat,TIME)