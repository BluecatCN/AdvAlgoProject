#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-07 20:18:51
# @Author  : mutudeh (josephmathone@gmail.com)
# @Link    : ${link}
# @Version : $Id$

import math

def verifyDis(array,disMat):
	#接受一个字符串，按照字符串的顺序输出路径长度

	numC = len(array)
	pathLen = 0
	CountNum = 0

	for i in range(numC):
		if CountNum != numC - 1:
			pathLen = pathLen + disMat[array[i]][array[i+1]]
			CountNum = CountNum + 1
	return pathLen + disMat[array[numC - 1]][array[0]]


