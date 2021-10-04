import pandas as pd
import numpy as np
from pulp import *

# fetching the names of the stores and their respective demands
df = pd.read_csv("demandestimations.csv")
stores = list(df['Store'])
demand = list(df['Demand Estimation (Pellets)  '])

# fetching the routes and their respective costs
df = pd.read_csv("routesWithoutDistribution.csv")
routes = list(df['route'])
costs = dict(zip(routes, df['cost']))

# adding a self-titled dictionaries for each store that contains which routes it is visited by
for store in stores:
    globals()["%s"%store] = dict(zip(routes, df[store]))

# the variables are the number of each routes to take
routeVars = LpVariable.dicts("Routes", routes, cat='Binary')

# adding the minimising cost problem 
prob  = LpProblem("Minimising_Costs_Problem", LpMinimize)
prob += lpSum([routeVars[i]*costs[i]] for i in routes)

# the total number of routs <= 60 because there are only 60 trucks
prob += lpSum(routeVars[i] for i in routes) <= 60

# adding the demand requirements for each store
# for store in stores:
#     prob += >= demand[i]


print("hi")