import time 
from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
time_limit = 300
def writeResults(testNum, timeTaken, n, k, location_set):
    f = open("stressResults.txt", "a")
    f.write("Test #" + str(testNum) + ": num_ppl = " + str(n) + ", k = " + str(k) + ", locations = " 
            + str(location_set) + ", timeTaken = " + str(timeTaken) + " seconds\n")
    f.close()
# n = 20 #number of people
# k = 5 # k random closest (For scenario 1)
# location_set = [5, 5] #Each item in this set represents the # of randomly generated locations for Coffee Shops, Drugstores, etc
def stressTestScen1(n, k, location_set):
    #time is in seconds   
    obj = DrugStoreCoffeeShops(n, k, location_set)
    obj.setup()
    start = time.perf_counter()
    obj.runScen1()
    del obj
    return time.perf_counter() - start
def stressTestScen2(n, k, location_set):
    #time is in seconds   
    obj = DrugStoreCoffeeShops(n, k, location_set)
    obj.setup()
    start = time.perf_counter()
    obj.runScen2()
    del obj
    return time.perf_counter() - start

def stressTestN(function, k, location_set):
    n = 2
    for i in range(100000): 
        time_elapsed = 0
        try:
            time_elapsed = function(n, k, location_set)
        except:
            break
        writeResults(i, time_elapsed, "{:e}".format(n), k, location_set)
        if(time_elapsed > 1800):
            break
        n = n * 2

def stressTestLocSize(function, n, k):
    location_set = [10, 10]
    for i in range(100, 400): 
        time_elapsed = function(n, k, location_set)
        writeResults(i, time_elapsed, n, k, location_set)
        if(time_elapsed > 1800):
            break
        location_set.append(10)

def stressTestLocNum(function, n, k):
    x = 2
    for i in range(100000): 
        time_elapsed = 0
        location_set = [x, x]
        try:
            time_elapsed = function(n, k, location_set)
        except:
            break
        writeResults(i, time_elapsed, n, k, ["{:e}".format(x), "{:e}".format(x)])
        if(time_elapsed > 1800):
            break
        x = x * 2

if __name__ == "__main__" :
    # #k doesnn't matter with scen2
	stressTestN(stressTestScen2, 5, [5, 5])
	stressTestLocNum(stressTestScen2, 100, 5)
	# stressTestLocSize(stressTestScen2, 1000, 5)