from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
# n = 20 #number of people
# k = 5 # k random closest (For scenario 1)
# location_set = [5, 5] #Each item in this set represents the # of randomly generated locations for Coffee Shops, Drugstores, etc
def stressTestScen1(n, k, location_set):
    #time is in seconds   
    obj = DrugStoreCoffeeShops(n, k, location_set)
    obj.setup()
    obj.runScen1()
    del obj

def stressTestScen2(n, k, location_set):
    #time is in seconds   
    obj = DrugStoreCoffeeShops(n, k, location_set)
    obj.setup()
    obj.runScen2()
    obj.getStats()
    del obj

def optimalSolution(n, k, location_set):
    obj = DrugStoreCoffeeShops(n, k, location_set)
    obj.setup()
    solution = obj.exhaustive_main()
    del obj
    return solution

if __name__ == "__main__" :
    # #k doesnn't matter with scen2
    stressTestScen2(100, 5, [10, 10])
    print(optimalSolution(100, 5, [10, 10]))
	# stressTestLocSize(stressTestScen2, 1000, 5)