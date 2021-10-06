import numpy as np
from numpy.lib import genfromtxt
from matplotlib import cm, pyplot
from copy import copy
from random import choices
import pandas as pd
import csv



def enRoutes(times, demands):
    dist = 55 # index of the hub
    
    fromDist = copy(times[dist]) # times to get to places from the distribution hub
    maxDemand = 26 # might be changed to add tolerances to problem or consider larger clusters
    cutOffTime = 2000
    temp = 1
    metalist = []

    numNodes = len(times)


    route = 0
    nodeRoutes = [-1]*numNodes

    while max(fromDist):
        # find the furthest point from the hub
        furthest = np.where(fromDist == np.amax(fromDist))[0][0]
        nodes = [furthest]
        totalDemand = demands[furthest]
        route += 1

        toFurthest = times[:,furthest] # time to go from somewhere to furthest point
        
        enRoute = fromDist + toFurthest # time for D to X to F 

        fromDist[furthest] = 0 # remove this node from unclustered nodes
        enRoute[furthest] = np.inf
        enRoute[dist] = np.inf

        nodeRoutes[furthest] = route

        while totalDemand < maxDemand:

            #n = np.where(enRoute == np.amin(enRoute))[0][0]  # find node with shortest en route cost 
            # ^^ deterministic, gets stuck sometimes in weird places

            # better random version - could change the exponent as a 'temp'
            n = choices(range(numNodes), weights = [ (1/(cost - np.amin(enRoute) + 1))**temp for cost in enRoute], k = 1 )[0]


            if fromDist[n] and (totalDemand + demands[n] <= maxDemand): # don't consider visited nodes 
                                                                            # or nodes that would bring sum of demands too high
                totalDemand += demands[n] # add this nodes demand to the total demand on this route
                nodes.append(n) # add to list of nodes
                fromDist[n] = 0 # remove this node from unclustered nodes
                nodeRoutes[n] = route

            enRoute[n] = np.inf # remove from nodes to consider adding
            if min(enRoute) > cutOffTime: # don't do large leaps / cut if all nodes are exausted
                break

        # output found cluster + total demand
        #print(nodes)
        #print(totalDemand)
        #print(groupToRoute(nodes,times))
        nodes.sort()
        metalist.append(nodes)

    return nodeRoutes, metalist


        
def groupToRoute(nodes, times):
    # nodes - list of ints

    # cheapest insertion method
    # meant for small groups

    currentNode = 55 # distribution center
    route = [currentNode]
    unvisited = copy(nodes)

    while len(route) <= len(nodes): # <= to account for dist hub
        mincost = np.inf
        newRoute = []

        for n in unvisited:
            for i in range(1,len(route)+1): # put the new node in every possible place (other than the start as start === end in this case)
                testRoute = copy(route)
                testRoute.insert(i,n)
                cost = routeCost(testRoute, times)
                if cost < mincost:
                    mincost = cost
                    newRoute = copy(testRoute)
                    newNode = n
        route = newRoute
        unvisited.pop(unvisited.index(newNode))


    return route, mincost

            

def routeCost(route,times):
    cost = 0
    for i in range(len(route)):
        start = route[i]
        end = route[(i+1)%len(route)] # so the last node loops back to start
        cost += times[start][end]
    return cost


  
def generate(n, index):    
    dist = 55
    maxTries = 200
    routesToGen = n # will slightly overshoot (10-15 routes)
    timedata = np.genfromtxt("WoolworthsTravelDurations.csv", delimiter = ',')[1:,1:]
    
    demands = np.genfromtxt("demandestimationsfinal.csv", delimiter = ",")[1:,index]
    # add zero demand for dist center to make things eaiser
    demands = np.insert(demands, dist, 0)
    #print(times[55]) #check loading worked as expected
    #print(demands)
    locs = np.genfromtxt("WoolworthsLocations.csv", delimiter = ',')[1:,-2:]
    #locs = np.append(locs, [[x] for x in routes], axis = 1)

    times = copy(timedata)
    numStores = len(times)

    #print(max(routes))
    #pyplot.scatter(locs[:,0], locs[:,1], s= 40, c = routes, cmap='Set1')
    # route as list, price, binary variables 

    #pyplot.show()
    i = 0

    costs = []
    routes = []
    listofClusters = []

    while len(routes) < routesToGen:
        _, cluster = enRoutes(times,demands)
        nonDupeclusters = [c for c in cluster if (not (c in listofClusters))]
        
        for r in nonDupeclusters:
            listofClusters.append(r)
            if len(r) == 1:
                continue # ignore routes that are just visiting one store and back

            route, cost = groupToRoute(r,times) 
            # add unloading times
            totalDemand = sum([demands[n] for n in r])
            cost += totalDemand*7.5*60
            cost = np.ceil(cost/60)*60 # round up to the minute for payment - seems reasonable

            if cost <= 4*3600:
                routes.append(route)
                costs.append(cost)

        i += 1
        if i%10 == 0:
            print(len(routes))
            if i > maxTries:
                print("Maximum Tries Reached - Routes Generated: " + str(len(routes)))
                break

        

    with open('routes.csv', 'w', newline='') as f:
        w = csv.writer(f)
        
        # writing the header line that includes the name of all the stores
        df = pd.read_csv("demandestimations.csv")
        line = list(df['Store'])
        line.insert(0,'route')
        line.insert(1,'cost')
        w.writerow(line)


        for i in range(len(routes)):

            bools = [ (x in routes[i]) for x in range(numStores) if x != dist] # checks for every store if it is in the route or not
            #print(  [ i for i in range(len(times)) if bools[i] ]  ) # checking if bool conversion worked like I thought it did

            line = [routes[i]] + [costs[i]] + bools

            w.writerow(line)
        # safety valve
        for i in range(numStores):
            
            bools = [False]*(numStores-1)
            if i < 55: bools[i] = True
            else: bools[i-1] = True
            line = ["!!"+str(i)] + [1600000] + bools # $100,000 for easy determination of how many are used
            if i != dist:
                w.writerow(line)



if __name__ == "__main__":
    generate(500, 1)