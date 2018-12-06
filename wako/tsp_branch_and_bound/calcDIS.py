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