import math
import random
import classes

###### Distance between 2 point objects #######
def dist(point1, point2):
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

###### Generate random long island coordinates with 6 degrees of precision #######
def genRandXLI():
    return round(random.uniform(40.589971, 41.139365), 6)
def genRandYLI():
    return round(random.uniform(-73.768044, 72.225494), 6)