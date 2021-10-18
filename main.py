import numpy as np
from numpy.random import default_rng
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from route_gen import *

def readInData(day):
    '''
        This function reads in the relevant data to perform the simulation on

        Inputs:
        --------
        day : {1,2}
        1 = weekdays (Mon-Fri), 2 = saturdays

        Outputs:
        --------
        routes1 : array
            array of the taken routes according 

    '''
    routeData = pd.read_csv("results.csv")
    strRoutes = list(routeData['Route'])
    split = strRoutes.index('Route')-1 # -1 compensates for one extra row (total cost) between results
    routes = [[int(x) for x in r[1:-1].split(',')] for r in strRoutes if (r[0] == '[')] # turn a string of a list into a list

    if day == 1: routes1 = routes[:split] # weekdays
    else: routes1 = routes[split:] # saturdays

    times = np.genfromtxt("WoolworthsTravelDurations.csv", delimiter = ',')[1:,1:]
    demands = np.genfromtxt("maxDemands.csv", delimiter = ",")[1:,1]
    demands = np.insert(demands, 55, 0)

    return routes1, times, demands


def demandToND(day):
    '''
        this function takes the csv files containing demands for the stores and converts them into values useful to standard deviation.

        Inputs:
        --------
        day : {1,2}
        1 = weekdays (Mon-Fri), 2 = saturdays


        Outputs:
        --------
        values : array
            array of the mean and standard deviation for the demand at each store.
    '''

    # removing weekends / non-sat is dealt with in the files
    demands = np.genfromtxt("WoolworthsDemands"+str(day)+".csv", delimiter = ",", skip_header = 1)[:,1:]  

    values = np.zeros([65,2])
    for i in range(65):
        values[i,0] = demands[i].mean()
        values[i,1] = demands[i].std()

    values = np.insert(values, 55, np.array((0,0)), axis = 0)

    return values




def timesToND(times, SD):
    '''
        this function takes the array for times from one node to another and creates a normal distribution of them.

        Inputs:
        -------
        times : array
            array of times from one node to another
        SD : float
            proportion of the data to be the standard distribution

        Outputs:
        --------
        values : array
            3d array of the mean and standard distribution for the times from each node to another.
    '''

    rows = len(times)
    cols = len(times[0])

    values = np.zeros([rows,cols,2])

    for i in range(rows):
        for j in range(cols):
                values[i,j,0] = times[i,j]
                values[i,j,1] = times[i,j]*SD

    return values


def main(n,day, isBoot = 0, slack = 0, isMerge = 0):
    '''
        This function will perform a Monte Carlo simulation

        Closing store 13 to merge with 2 and store 34 to merge with 52
    '''
    mergeStores = [(13,2),(34,52)]

    # Initialising arrays for the cost of routes, number of trucks and overtime trucks
    RouteCosts = [0]*n
    NumTrucks  = [0]*n
    OTTrucks   = [0]*n
    SumDemands = [0]*n
    if slack: CompCosts = [0]*n

    # Reading in data to perform the simulation on
    routes, times = readInData(day)[0:2]

    # Creating a normal distribution of demands. 
    demandND = demandToND(day)
    if isMerge:
        for x in mergeStores:
            close = x[0]
            merge = x[1]
            demandND[merge][0] += demandND[close][0]
            demandND[close] = np.array((0,0))




    # Creating a normal distribution of travel times.
    timeND = timesToND(times, 0.05)     # choosing to have 5% SD of times.
    
    numLocs = 66

    if isBoot:
        demandvals = np.genfromtxt("WoolworthsDemands"+str(day)+".csv", delimiter = ",", skip_header = 1)[:,1:]
        demandvals = np.insert(demandvals, 55, 0, axis = 0)  
        if isMerge:
            for x in mergeStores: # can add more stores here if desired
                close = x[0]
                merge = x[1]
                demandvals[merge] = [demandvals[merge][i] + demandvals[close][i] - 1 for i in range(len(demandvals[merge]))]
                demandvals[close] = [0]*len(demandvals[merge])

                        

    # Simulation 
    rng = np.random.default_rng(263)
    for i in range(n):
        
        # generating demands
        demands = np.zeros(numLocs)
        for j in range(numLocs):
            if isBoot: demands[j] = rng.choice(demandvals[j], size=1)[0]
            else: demands[j] = np.ceil(rng.normal(demandND[j,0], demandND[j,1], size = 1))

        # generating times
        times = np.zeros([numLocs,numLocs])
        for j in range(numLocs):
            for k in range(numLocs):
                times[j,k] = np.random.normal(timeND[j,k,0], timeND[j,k,1], size = 1)

        SumDemands[i] = sum(demands)

        # running cost simulation
        RouteCosts[i], NumTrucks[i], OTTrucks[i] = totalCost(routes + [[0]]*(slack), times, demands)

        if slack: CompCosts[i], x, x = totalCost(routes + [[0]]*(slack-2), times, demands) 

        if (i % 200) == 0:
            print("%3.0f percent done" % (i/n*100))
 
    if slack >= 3:
        diffCosts = [(CompCosts[i] - RouteCosts[i]) for i in range(n)]
        RouteCosts = [sum(diffCosts[i*20:i*20+20]) for i in range(n//20)]
        print(max(diffCosts))
        print(max(RouteCosts))

    RouteCosts.sort()
    for fraction in [0.025,0.5,0.975]:
        index = int(len(RouteCosts)*fraction)
        print(" %1.1fth Percentile: %1.2f " % (fraction*100, RouteCosts[index])) 

    print(max(RouteCosts))

    print("Mean: %1.1f" % np.mean(RouteCosts))

    for i in range(max(NumTrucks)+1):
        if i in NumTrucks:
            print( "%1.0i Routes: %3.2f percent" % (i, sum([i==t for t in NumTrucks])/len(NumTrucks)*100) )

    # histogram of the simulated costs
    plt.hist(RouteCosts, bins = 100, density=True)
    plt.axvline(np.mean(RouteCosts), color='k', linewidth=1)
    if day == 1: plt.axvline(20122.50, color='r', linestyle='dashed', linewidth=1)
    else:        plt.axvline(10695.00,  color='r', linestyle='dashed', linewidth=1)
    plt.show()

    # histogram of the simulated demands
    #plt.hist(SumDemands, bins = 100, density=True)
    #plt.axvline(np.mean(SumDemands), color='k', linewidth=1)

    # calculating average demand before random distribution
    #data = np.genfromtxt("demandestimationsfinal.csv", delimiter = ',', skip_header = 1, usecols = (1,2))[:,day-1]
    #plt.axvline(np.sum(data), color='r', linestyle='dashed', linewidth=1)
    #plt.show()


if __name__ == "__main__":
    #example histogram generation - not complete code for histograms in reports
    main(1000,1,1,isMerge=0, slack=1) # 13 trucks will give 1 slack
    main(1000,2,1,isMerge=0, slack=1)


