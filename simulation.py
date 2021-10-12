import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from route_gen import *


def readInData():
    '''
        This function reads in the relevant data to perform the simulation on

        Outputs:
        --------
        routes1 : array
            array of the taken routes according 

    '''
    routeData = pd.read_csv("results.csv")
    strRoutes = list(routeData['Route'])
    split = strRoutes.index('Route')-1 # -1 compensates for one extra row (total cost) between results
    routes = [[int(x) for x in r[1:-1].split(',')] for r in strRoutes if (r[0] == '[')] # turn a string of a list into a list
    routes1 = routes[:split] # weekdays
    times = np.genfromtxt("WoolworthsTravelDurations.csv", delimiter = ',')[1:,1:]
    demands = np.genfromtxt("maxDemands.csv", delimiter = ",")[1:,1]
    demands = np.insert(demands, 55, 0)

    return routes1, times, demands


def demandToND():
    '''
        this function takes the csv file containing demands for the stores and converts them into values useful to standard deviation.

        Outputs:
        --------
        values : array
            array of the mean and standard deviation for the demand at each store.
    '''

    demands = np.genfromtxt("WoolworthsDemands.csv", delimiter = ",", skip_header = 1)[:,1:]
    demands = np.delete(demands,-1,1)
    demands = np.delete(demands,-1,1)
    demands = np.delete(demands,-6,1)
    demands = np.delete(demands,-6,1)
    demands = np.delete(demands,-11,1)
    demands = np.delete(demands,-11,1)
    demands = np.delete(demands,-16,1)
    demands = np.delete(demands,-16,1)
    
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


def main(n):
    '''
        This function will perform a Monte Carlo simulation
    '''

    # Initialising arrays for the cost of routes, number of trucks and overtime trucks
    RouteCosts = [0]*n
    NumTrucks  = [0]*n
    OTTrucks   = [0]*n

    # Reading in data to perform the simulation on
    routes, times = readInData()[0:2]

    # Creating a normal distribution of demands. 
    demandND = demandToND()

    # Creating a normal distribution of travel times.
    timeND = timesToND(times, 0.05)     # choosing to have 5% SD of times.
    
    # Simulation 
    for i in range(n):
        
        # generating demands
        demands = np.zeros(66)
        for j in range(66):
            demands[j] = np.random.normal(demandND[j,0], demandND[j,1], size = 1)

        # generating times
        times = np.zeros([66,66])
        for j in range(66):
            for k in range(66):
                times[j,k] = np.random.normal(timeND[j,k,0], timeND[j,k,1], size = 1)

        # running cost simulation
        RouteCosts[i], NumTrucks[i], OTTrucks[i] = totalCost(routes, times, demands)
 

    plt.hist(RouteCosts, bins = 100)
    plt.show()
    

if __name__ == "__main__":
    main(5000)