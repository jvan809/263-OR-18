import pandas as pd
import numpy as np
from pulp import *

# fetching the names of the stores and their respective demands
df = pd.read_csv("demandestimations.csv")
stores = list(df['Store'])
# demand = list(df['Demand Estimation (Pellets)  '])
# demand = [round(num) for num in demand]

# fetching the routes and their respective costs
df = pd.read_csv("routesWithoutDistribution.csv")
routes = list(df['route'])
costs = dict(zip(routes, df['cost']))

# adding a self-titled dictionaries for each store that contains which routes it is visited by
# for store in stores:
#     globals()["%s"%store] = dict(zip(routes, df[store]))

# the variables are the number of each routes to take
routeVars = LpVariable.dicts("Routes", routes, cat='Integer', lowBound=0, upBound=1)

# adding the minimising cost problem 
prob  = LpProblem("Minimising_Costs_Problem", LpMinimize)
prob += lpSum([routeVars[route]*costs[route]] for route in routes)

# the total number of routes <= 60 because there are only 60 trucks
prob += lpSum(routeVars[route] for route in routes) <= 60

for i, store in enumerate(stores):
    prob += lpSum([routeVars[route] for route in routes if str(i) in route]) == 1 

prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Showing the chosen routes
print("The chosen routes are:")
for route in routes:
    if routeVars[route].value() == 1:
        print(route)

# The optimised objective function value of Ingredients pue is printed to the screen    
print("Total Profit from Ties = ", value(prob.objective))