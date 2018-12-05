# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 12:00:20 2018

@author: Maliha
"""
import math
from time import time
import numpy as np
import random


def main():
    #Extracting, Transforming and Loading Data
    tspdatafile = 'datasets/burma14.tsp'
    cities, disMat, num_of_cities = PreProcessData(tspdatafile)    

    #calculating the start of time of the algorithm
    start_time = time()
    
    #Making two dictionaries to avoid sending loads of parameters during function calling
    aco_params = {}
    aco_params["q"] = 10 #pheromone intensity
    aco_params["rho"] = 0.5 #pheromone decay coefficient
    aco_params["beta"] = 10.0 #relative importance of heuristic information
    aco_params["alpha"] = 1.0 #relative importance of pheromone
    aco_params["ant_count"] = num_of_cities #number of ants used
    aco_params["generations"] = 100 #number of iterations
    aco_params["update_strategy"] = 2 #pheromone update strategy. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
    
    graph={}
    graph["rank"] = num_of_cities
    graph["matrix"]=disMat
    graph["pheromone"] = [[1 / (graph["rank"]) for j in range(graph["rank"])] for i in range(graph["rank"])]
    graph["initial_pheromone"] = graph["pheromone"]
   
    #Calculating path and cost through Ant Colony Optimization Algorithm
    path, length = Ant_Colony_Optimization(aco_params,graph)
    
    #Calculating total time of computation of algorithm
    total_time = time() - start_time
    
    #Printing the ordered sequence of nodes to visit and the cost of the proposed solution
    print("Path: %s" % path)
    print( "Length of the Path: %s" % length)
    print( "Time: %s seconds" % round(total_time,2))  

######### Ant Colony Algorithm ##########################################################

def Ant_Colony_Optimization(aco, graph):
        best_cost = float('inf')
        best_solution = []
        for gen in range(aco["generations"]):
            #create the ants
            ants = [Create_Ant(aco, graph, count) for count in range(aco["ant_count"])]
            for index,ant in enumerate(ants):
                for i in range(graph["rank"] - 1):
                    ants[index] = ant_select_next(ant)
                #add distance of last node to first node 
                ants[index]["total_cost"] += graph["matrix"][ant["tabu"][-1]][ant["tabu"][0]]
                if ant["total_cost"] < best_cost:
                    best_cost = ant["total_cost"]
                    best_solution = [] + ant["tabu"]
                # update local pheromone of individual ants
                ants[index]= local_pheromone_update(aco,graph,ant)
            #update pheromone of only the best edges
            offline_pheromone_update(aco,graph,ants,best_solution,best_cost)
        return best_solution, best_cost

def Create_Ant(aco,graph,start):
        ant = {}
        ant["colony"] = aco
        ant["graph"] = graph
        ant["total_cost"] = 0.0
        ant["tabu"] = []  # tabu list
        ant["pheromone_local"] = []  # the local increase of pheromone
        ant["allowed"] = [i for i in range(graph["rank"])]  # nodes which are allowed for the next selection
        # heuristic information - inverse of the length of the edges
        ant["eta"] = [[0 if i == j else 1 / graph["matrix"][i][j] for j in range(graph["rank"])] for i in range(graph["rank"])]
        # uncomment the line below to start an ant randomly from any node
        #start = random.randint(0, graph["rank"] - 1)
        ant["tabu"].append(start) #assign an ant to each node
        ant["current"] = start
        ant["allowed"].remove(start)
        return ant
        
def ant_select_next(ant):
        denominator = 0
        for i in ant["allowed"]:
            denominator += ant["graph"]["pheromone"][ant["current"]][i] ** ant["colony"]["alpha"] * ant["eta"][ant["current"]][
                                                                                            i] ** ant["colony"]["beta"]
        # probabilities for moving to a node in the next step
        probabilities = [0 for i in range(ant["graph"]["rank"])]  
        for i in range(ant["graph"]["rank"]):
            try:
                ant["allowed"].index(i)  # test if allowed list contains i
                probabilities[i] = ant["graph"]["pheromone"][ant["current"]][i] ** ant["colony"]["alpha"] * \
                    ant["eta"][ant["current"]][i] ** ant["colony"]["beta"] / denominator
            except ValueError:
                pass  # do nothing
        
        # select next node by probability roulette
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        
        ant["allowed"].remove(selected)
        ant["tabu"].append(selected)
        ant["total_cost"] += ant["graph"]["matrix"][ant["current"]][selected]
        ant["current"] = selected    
        return ant

def local_pheromone_update(aco,graph,ant):
        ant["pheromone_local"] = [[0 for j in range(ant["graph"]["rank"])] for i in range(ant["graph"]["rank"])]
        for i, row in enumerate(graph["pheromone"]):
            for j, col in enumerate(row):
                graph["pheromone"][i][j] = ((1 - aco["rho"])*graph["pheromone"][i][j]) + (aco["rho"]*graph["initial_pheromone"][i][j])
                ant["pheromone_local"][i][j] = graph["pheromone"][i][j]
        return ant  
    
def offline_pheromone_update(aco,graph,ants,best_solution,best_cost):
        for i in range(graph["rank"]):
            if i < 13:
                graph["pheromone"][best_solution[i]][best_solution[i+1]] = ((1 - aco["rho"])*graph["pheromone"][best_solution[i]][best_solution[i+1]]) + (aco["rho"]*(1/best_cost))
    
#########Parsing Data and Computing Distance Matrix of Cities############################
    
def PreProcessData(tspdatafile):
        with open(tspdatafile) as f:
            num = 0 #city number
            find_num = False 
            temMat = []
            data = f.readlines()
            method=''
            numJudge = 0
            
            for line in data:

                stringJudge = []
                line = line.rstrip('\n')
                stringJudge = line.split()
                
                if stringJudge[0]=='EDGE_WEIGHT_TYPE:':
                    method = stringJudge[1]
                    
                if stringJudge[0] == 'DIMENSION:':    
                    numJudge = np.int(stringJudge[1])

                if find_num:    
                    if numJudge:
                        string_data = line.split()
                        temMat.append(string_data)
                        numJudge = numJudge - 1                        
                    else:
                        break
                    num = num + 1                        
                if stringJudge[0] == "NODE_COORD_SECTION":
                    find_num = True

            
            corMat = np.array(temMat)
            corMat = corMat.astype(np.float64)
            corMat = corMat[:,1:3]

            disMat = np.zeros((num,num),dtype = np.float64)

####################EU_2D######################################################
            
            if method == "EUC_2D":
                for i in range(num):
                    for j in range(num):
                        
                        if i != j:
                            xd = corMat[i][0]-corMat[j][0]
                            yd = corMat[i][1]-corMat[j][1]

                            # temDis = (int)(np.sqrt(np.float((xd*xd + yd*yd) ) ) + 0.5)
                            temDis = (int)(math.sqrt((xd*xd + yd*yd) ) + 0.5)

                            disMat[i][j] = disMat[j][i] = temDis

#####################GEO DISTANCE#############################################
            
            if method == "GEO":
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

##############################################################################
#corMat has cordinates of the cities，
#disMat is the distance matrix between cities,
#num is the number of nodes/cities present in the dataset
            return corMat,disMat,num;

##############################################################################

if __name__ == '__main__':
    main()