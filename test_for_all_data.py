import numpy as np
import Extrac_test_data as te

file = open('D:/city.txt','r')

name1 = 'D:/city.txt'

with open(name1) as f:
	#take each dataset's name as input 
	cities = f.read()
	cities.rstrip('\n')
	cities_names = cities.split(',')
#
name = 'D:/Study/Jean Monnet/Advanced Algoirthm/Project/Data/'
count = 0
for i in cities_names:
	name_city = name + i
	name_city = name_city + '.tsp'
	#combine the absolute name path with dataset name
	dis,num = te.PreData(name_city)
	#out distance matrix and number of cities in that dataset

	# the following will your own algo
