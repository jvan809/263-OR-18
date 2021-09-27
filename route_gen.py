import numpy as np
from numpy.lib import genfromtxt
from matplotlib import cm, pyplot 

def enRoutes(times, demands):
    dist = 55 # index of the hub
    fromDist = times[dist] # times to get to places from the distribution hub
    maxDemand = 26 # might be changed to add tolerances to problem or consider larger clusters

    # add zero demand for dist center to make things eaiser
    demands = np.insert(demands, 55, 0)

    route = 0
    nodeRoutes = [-1]*len(times)

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

        nodeRoutes[furthest] = route

        while totalDemand < maxDemand:
            n = np.where(enRoute == np.amin(enRoute))[0][0]  # find node with shortest en route cost 

            if fromDist[n]: # don't consider visited nodes 
                totalDemand += demands[n] # add this nodes demand to the total demand on this route
                nodes.append(n) # add to list of nodes
                fromDist[n] = 0 # remove this node from unclustered nodes
                nodeRoutes[n] = route

            enRoute[n] = np.inf # remove from nodes to consider adding
            if min(enRoute) == np.inf:
                break

        # output found cluster + total demand
        #print(nodes)
        #print(totalDemand)

    return nodeRoutes

        

        




if __name__ == "__main__":
    times = np.genfromtxt("WoolworthsTravelDurations.csv", delimiter = ',')[1:,1:]
    demands = np.genfromtxt("WoolworthsDemands.csv", delimiter = ",")[1:,1]
    #print(times[55]) #check loading worked as expected
    #print(demands)


    routes = enRoutes(times, demands)

    locs = np.genfromtxt("WoolworthsLocations.csv", delimiter = ',')[1:,-2:]
    #locs = np.append(locs, [[x] for x in routes], axis = 1)

    pyplot.scatter(locs[:,0], locs[:,1], s= 40, c = routes, cmap='Set1')

    pyplot.show()




    

    


