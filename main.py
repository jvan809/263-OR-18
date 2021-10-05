import pandas as pd
import numpy as np
from pulp import *
from route_gen import *

# fetching the names of the stores and their respective demands
df = pd.read_csv("demandestimations.csv")
stores = list(df['Store'])

# generating the routes
n = 5000    # number of routes to generate
generate(n)

# fetching the routes and their respective costs
df = pd.read_csv("routes.csv")
routes = list(df['route'])
costs = dict(zip(routes, df['cost']))

# rewriting the route names as the actually stores rather than the indices of said stores
routesNamed = []
for i, route in enumerate(routes):
    temp = route.replace("[55,","").replace("]","").replace("!","").strip()
    array = temp.split(",")
    
    for j, x in enumerate(array):
            array[j] = int(x)
            if int(x) < 55:
                array[j] = stores[array[j]]
            else:
                array[j] = stores[array[j]-1]

    routesNamed.append(' '.join([store for store in array]))
# print(routesNamed)

# the variables are the number of each routes to take
routeVars = LpVariable.dicts("Routes", routes, cat='Integer', lowBound=0, upBound=1)

# adding the minimising cost problem 
prob  = LpProblem("Minimising_Costs_Problem", LpMinimize)
prob += lpSum([routeVars[route]*costs[route]] for route in routes)

# the total number of routes <= 60 because there are only 60 trucks
prob += lpSum(routeVars[route] for route in routes) <= 70

# adding the constraints that each store can be visited only once
for i, store in enumerate(stores):
    prob += lpSum([routeVars[route] for i, route in enumerate(routes) if store in routesNamed[i]]) == 1 

# solving problem
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Showing the chosen routes
print("The chosen routes are:")
for route in routes:
    if routeVars[route].value() == 1:
        print(route)

# The optimised objective function value of Ingredients pue is printed to the screen    
print("Total Cost of Distribution is $", value(prob.objective))