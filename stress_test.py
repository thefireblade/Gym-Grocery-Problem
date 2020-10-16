import time 
import traceback
from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
time_limit = 200
def writeResults(testNum, timeTaken, n, k, location_set, filename = "stressResults.txt"):
    f = open(filename, "a")
    f.write("Test #" + str(testNum) + ": num_ppl = " + str(n) + ", k = " + str(k) + ", locations = " 
            + str(location_set) + ", timeTaken = " + str(timeTaken) + " seconds\n")
    f.close()
    
def write(string, filename = "stressResults.txt"):
    f = open(filename, "a")
    f.write(string)
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

def stressTestScen2_3_1(n, k, location_set):
    #time is in seconds   
    obj = DrugStoreCoffeeShops(n, k, location_set)
    obj.setup()
    start = time.perf_counter()
    obj.runScen2_3_1()
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
        if(time_elapsed > time_limit):
            break
        n = n * 2

def stressTestLocSize(function, n, k):
    location_set = [10, 10]
    for i in range(100, 400): 
        time_elapsed = function(n, k, location_set)
        writeResults(i, time_elapsed, n, k, location_set)
        if(time_elapsed > time_limit):
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
        if(time_elapsed > time_limit):
            break
        x = x * 2

def stressTestCompareScen2_2Scen2_3(k, n_0 = 10, ls_0 = 3, ls_1 = 3):
    n = n_0
    location_set = [ls_0, ls_1]
    win = 0
    loss = 0
    tie = 0
    for i in range(10000):
        print("Commencing test #" + str(i))
        obj = DrugStoreCoffeeShops(n, k, location_set)
        obj.setup()
        
        result_0 = -1 #The maximum returned component of function1
        result_1 = -1 #The maximum returned compononent of function2
        start = time.perf_counter()
        try:
            result_0 = obj.runScen2_3()
            first_elapse = time.perf_counter() - start

            # Write the results for scenario 2 (Pairing both shops to a person at a time)
            writeResults(i, first_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])])
            
            obj.resetGraph() #Reset the graph so we can compare to the second test

            reset = time.perf_counter()
            result_1 = obj.runScen2_3_1()
            second_elapse = time.perf_counter() - reset

            # Write the results for scenario 2.3 (Pairing a shop to each person at a time)
            writeResults(i, second_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])])
            
        except Exception as e: 
            traceback.print_exc()
            print(e)
            break
        time_elapsed = time.perf_counter() - start
        if(result_0 == result_1):
            tie += 1
        else:
            if(result_0 > result_1):
                win += 1
            else:
                loss += 1
        if(time_elapsed > time_limit * 2):
            print("Time has elapsed over the time limit of " + str(time_limit * 2))
            break
        n = n * 3
        location_set = [location_set[0] * 2, location_set[1] * 2]
        del obj # Delete the DrugStoreCoffeeShop Object after using it
        write("Function 1 has {win} wins, {loss} losses, and {tie} ties over Function 2.\n".format(
            win=str(win), loss=str(loss), tie=str(tie)))

def compareScen2_2Scen2_3(k, n_0 = 200, ls_0 = 30, ls_1 = 35, tests = 300):
    n = n_0
    location_set = [ls_0, ls_1]
    win = 0
    loss = 0
    tie = 0
    for i in range(tests):
        print("Commencing test #" + str(i))
        obj = DrugStoreCoffeeShops(n, k, location_set)
        obj.setup()
        
        result_0 = -1 #The maximum returned component of function1
        result_1 = -1 #The maximum returned compononent of function2
        try:
            result_0 = obj.runScen2_3_1_rand()

            # Write the results for scenario 2 (Pairing both shops to a person at a time)
            # writeResults(i, first_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])],
            # "unit_test_2_3.txt")
            
            obj.resetGraph() #Reset the graph so we can compare to the second test

            result_1 = obj.runScen2_3_1()

            # Write the results for scenario 2.3 (Pairing a shop to each person at a time)
            # writeResults(i, second_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])], 
            # "unit_test_2_3.txt")
            
        except Exception as e: 
            traceback.print_exc()
            print(e)
            break
        if(result_0 == result_1):
            tie += 1
        else:
            if(result_0 > result_1):
                win += 1
            else:
                loss += 1
        del obj # Delete the DrugStoreCoffeeShop Object after using it
    write("Function 1 has {win} wins, {loss} losses, and {tie} ties over Function 2.\n".format(
        win=str(win), loss=str(loss), tie=str(tie)), "unit_test_2_3.txt")

if __name__ == "__main__" :
    # #k doesnn't matter with scen2
	stressTestN(stressTestScen2_3_1, 5, [5, 5])
	# stressTestLocNum(stressTestScen2, 100, 5)
	# stressTestLocSize(stressTestScen2, 1000, 5)
    # for i in range(20):
    #     compareScen2_2Scen2_3(6, tests = 500)
    # stressTestCompareScen2_2Scen2_3(3)