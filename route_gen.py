import random
import numpy as np
from numpy.lib import genfromtxt
from matplotlib import cm, pyplot
from copy import copy
from random import choices
import pandas as pd
import csv
from bisect import bisect_left



def enRoutes(times, demands, start = -1):
    # creates a partition (in the form of clusters) of a set of nodes obeying demand and timing data
    # Inputs:
    #   times - array: costs for any node to node traversal
    #   demands - vector array: demand of each store (all is index based so should match times)
    #   start - int: which node to start with (be default will start with the furthest node and work from there)
    # outputs:
    #   nodeRoutes - list: based on index which cluster each node belongs to (-1 for any unassinged)
    #   metalist - list of lists: list of clusters generated

    dist = 55 # index of the hub
    
    fromDist = copy(times[dist]) # times to get to places from the distribution hub
    fromDist = [times[dist][i]*(demands[i] > 0) for i in range(len(times[dist]))] # don't consider stores with 0 demand
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

        if start >= 0:
            furthest = start
            start = -1


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

        
def groupToRoute(nodes, times, demands):
    # turns a unordered list of nodes into a ordered route
    # Inputs:
    #   nodes - list of ints: unordered cluster of nodes to find a route
    #   times - numpy array: transit times 
    # Outputs:

    # Notes:
    #   cheapest insertion method
    #   meant for small groups

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
                cost = routeCost(testRoute, times, demands, unload = 0) # unload is invariant so is excluded in route finding
                if cost < mincost:
                    mincost = cost
                    newRoute = copy(testRoute)
                    newNode = n
        route = newRoute
        unvisited.pop(unvisited.index(newNode))

    finalCost = routeCost(route, times, demands, unload = 1) # incl unloading times for final cost 
    return route, finalCost
        

def routeCost(route,times, demands, unload = 1):
    # Determines the total cost of a proposed route
    # Inputs:
    #   route - list: ordered list of nodes that makes up the route
    #   times - array: transit times for every store to every other store 
    #   demands - vector (1xn array): simulated demands for every store (incl. dist center) - can be anything if unload = 0
    #   unload - bool: should unloading times be included?
    # Outputs:
    #   cost - float: total time taken to traverse this route (cycle)
    unloadTime = 7.5*60 # per pallete
    cost = 0
    for i in range(len(route)):
        start = route[i]
        end = route[(i+1)%len(route)] # so the last node loops back to start
        cost += times[start][end]
    

    if unload:
        routeDemands = [demands[node] for node in route] 
        cost += sum(routeDemands)*unloadTime
    
    return cost


def simRouteCost(route,times,demands):
    # determines total cost (incl. wet-hires) of a route with random demands and times
    # Inputs:
    #   route - list: ordered list of nodes that makes up the route (start at dist center eg. [55,25,0])
    #   times - array: transit times for every store to every other store 
    #   demands - vector (1xn array): simulated demands for every store (incl. dist center)
    # Outputs:
    #   times - list of floats: time in seconds for each truck - will generally be length one but may need to be split up based on demand

    capacity = 26
    rlen = len(route)
    maxTime = 4*3600 # pay period for wet-hires


    routeDemands = [demands[node] for node in route]

    if max(routeDemands) > capacity: ValueError("A node in this route as demand exceeding a full truck - no solution possible")

    totalDemand = sum(routeDemands)

    if totalDemand <= capacity: ## case where only one truck needed
        cost = routeCost(route, times, demands) # time to travel route
        return [cost]

    ## case where one truck cannot fill route

    # check route costs for removing any one node in the route + check if they 
    newCost = np.inf

    ## i'm presently assuming that no more than one node needs to be removed
    for i in range(1,rlen): # each node not incl dist
        node = route[i]
        newDemand = totalDemand - demands[node] # remove the node in consideration of route demand
        if newDemand > capacity: continue # don't consider new routes that still don't work
        
        # note: this method of costing assumes that the other route will be filled by wet-hire and is therefore of fixed cost.
        shortCost = routeCost([55, node], times, demands) # assume this is the route that is driven by our trucks
        newRoute = route.copy()
        newRoute.pop(i)
        longCost = routeCost(newRoute, times, demands) # route driven by wet-hire - assume it's fixed given not exceeding max time

        if (longCost <= maxTime) and (shortCost < newCost): 
            newCost = shortCost
            toRemove = i
    
    if newCost == np.inf: ValueError("Solution not found after shedding any one node - Jaqlin needs to do more work")

    route.pop(toRemove)
    longCost = routeCost(route, times, demands)

    return [shortCost, longCost]
    

def totalCost(routes, times, demands):
    # determines total cost for a solution in dollars
    # inputs:
    #   routes - list of lists : list of ordered lists of nodes that makes up each route (start at dist center eg. [55,25,0])
    #   times - array: transit times for every store to every other store 
    #   demands - vector (1xn array): simulated demands for every store (incl. dist center)
    # outputs
    #   totalCost - float: total cost in dollars for final solution
    #   number of truck slots needed (int)
    #   number of trucks that are over time (above 4 hours) (int)

    maxTime = 4*60 # max 4 hours of minutes before OT
    rate = 225/60 # cost per min for internal trucks
    maxCost = maxTime*rate # 900
    OTrate = 50/60 # difference in cost/min of overtime

    cost = lambda time: time*rate + (time > maxTime)*(time - maxTime)*OTrate # converts times in minutes into cost in dollars for internal trucks

    truckTimes = []
    [truckTimes.extend(simRouteCost(r,times,demands)) for r in routes]


    truckCosts = [cost(-(-time//60)) for time in truckTimes] # ceiling divide by the minute
    truckCosts.sort()

    slots = 60
    wetHireCost = 2000
    hireTrucks = max(len(truckCosts) - slots,0) # number of trucks needed to be hired
    firstOT = bisect_left(truckCosts, maxCost)
    underTimeCosts = truckCosts[:firstOT]
    overTimeCosts = truckCosts[firstOT:] # length of this could be used as number of trucks that require overtime pay

    if len(underTimeCosts) < hireTrucks: ValueError("Some overtime trucks need to be hired for >4 hours - logic doesn't presently support this")
    underTimeCosts[slots:] = [wetHireCost]*hireTrucks # replace trucks costs over slots of trucks with wet hire cost

    totalCost = round(sum(underTimeCosts) + sum(overTimeCosts), 2)
    return totalCost, len(truckCosts), len(overTimeCosts)

  
def generate(n, index, mode = 'w'):  
    # generates a list of potential routes and writes to a csv with routes and costs
    #
    # inputs:
    #   n - int: total number of routes to have at the end of the process
    #   index - int: which column of the demand data spreadsheet to use
    #   mode - either 'w' or 'w+' for creating a new sheet or appending
    # Outputs:
    #   writes to a csv file 'routes[index].csv' with routes (as a list), cost of the route (seconds), and then bools

    # notes: 
    #   using this in append mode will cause a siginificant spin-up period - maxtries may need to be increased to accomadate this.
    #   append mode also requires the relevant file to already exist


    filename = 'routes' + str(index) + '.csv'
    #   mode - either 'w' for overwrite file or 'w+' to append to file  
    random.seed(263)
    dist = 55
    maxTries = 600
    routesToGen = n # will slightly overshoot (10-15 routes)
    times = np.genfromtxt("WoolworthsTravelDurations.csv", delimiter = ',')[1:,1:]
    
    demands = np.genfromtxt("demandestimationsfinalint.csv", delimiter = ",")[1:,index]
    # add zero demand for dist center to make things eaiser
    demands = np.insert(demands, dist, 0)
    #print(times[55]) #check loading worked as expected
    #print(demands)
    locs = np.genfromtxt("WoolworthsLocations.csv", delimiter = ',')[1:,-2:]
    #locs = np.append(locs, [[x] for x in routes], axis = 1)

    numStores = len(times)

    #print(max(routes))
    #pyplot.scatter(locs[:,0], locs[:,1], s= 40, c = routes, cmap='Set1')
    # route as list, price, binary variables 

    #pyplot.show()
    i = 0

    costs = []
    routes = []
    listofClusters = []

    if mode == 'w+':
        routeData = pd.read_csv("routes"+str(index)+".csv")
        strRoutes = list(routeData['route'])
        routes = [ [int(x) for x in r[1:-1].split(',')] for r in strRoutes if (r[0] == '[')] # turn a string of a list into a list
        costs = list(routeData['cost'])[65:]

    while len(routes) < routesToGen:
        _, cluster = enRoutes(times,demands)
        nonDupeclusters = [c for c in cluster if (not (c in listofClusters))]
        
        for r in nonDupeclusters:
            listofClusters.append(r)
            if len(r) == 1:
                continue # ignore routes that are just visiting one store and back

            route, cost = groupToRoute(r, times, demands) 
            cost = np.ceil(cost/60)*60 # round up to the minute for payment - seems reasonable

            if cost <= 4*3600 and (not (route in routes)): # brackets everywhere because I don't know how the logic works
                routes.append(route)
                costs.append(cost)

        i += 1
        if i % 25 == 0:
            print(len(routes))
            if i > maxTries:
                print("Maximum Tries Reached - Routes Generated: " + str(len(routes)))
                break

        
    
    with open(filename, mode, newline='') as f:
        w = csv.writer(f)
        
        # writing the header line that includes the name of all the stores
        df = pd.read_csv("WoolworthsDemands.csv")
        line = list(df['Store'])
        line.insert(0,'route')
        line.insert(1,'cost')
        w.writerow(line)

        # safety valve routes
        if mode == 'w':
            for i in range(numStores):
                
                bools = [False]*(numStores-1)
                if i < 55: bools[i] = True
                else: bools[i-1] = True
                line = ["!!"+str(i)] + [16000000] + bools # $100,000 for easy determination of how many are used
                if i != dist:
                    w.writerow(line)


        for i in range(len(routes)):

            bools = [ (x in routes[i]) for x in range(numStores) if x != dist] # checks for every store if it is in the route or not
            #print(  [ i for i in range(len(times)) if bools[i] ]  ) # checking if bool conversion worked like I thought it did

            line = [routes[i]] + [costs[i]] + bools

            w.writerow(line)


if __name__ == "__main__":
    #for i in range(1,3):
    #    generate(1000, i)

    routeData = pd.read_csv("results.csv")
    strRoutes = list(routeData['Route'])
    split = strRoutes.index('Route')-1 # -1 compensates for one extra row (total cost) between results
    routes = [ [int(x) for x in r[1:-1].split(',')] for r in strRoutes if (r[0] == '[')] # turn a string of a list into a list
    routes1 = routes[:split] # weekdays
    routes2 = routes[split:] # saturday

    times = np.genfromtxt("WoolworthsTravelDurations.csv", delimiter = ',')[1:,1:]
    
    demands = np.genfromtxt("demandestimationsfinalint.csv", delimiter = ",")[1:,2]
    demands = np.insert(demands, 55, 0)


    cost, trucks, OTTrucks = totalCost(routes2, times, demands)

    print(cost)
    print(trucks)
    print(OTTrucks)
