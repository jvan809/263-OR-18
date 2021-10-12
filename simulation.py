import numpy as np
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


def main(n):
    '''
        This function will perform a Monte Carlo simulation
    '''

    # Initialising arrays for the cost of routes, number of trucks and overtime trucks
    RouteCosts = [0]*n
    NumTrucks = [0]*n
    OTTrucks = [0]*n

    # Reading in data to perform the simulation on
    routes1, times, demands = readInData()

    # Simulation 
    for i in range(n):
        RouteCosts[i], NumTrucks[i], OTTrucks[i] = totalCost(routes1, times, demands)
 
    # Unfortunately the randomness was not working for this function. Will follow up on Wednesday.

    plt.hist(RouteCosts, bins = 100)
    plt.show()
    

if __name__ == "__main__":
    main(1000)