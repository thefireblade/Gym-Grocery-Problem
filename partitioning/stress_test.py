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

def findMethod(gObj, func):
    try:
        func = getattr(gObj, func)
        return func()
    except AttributeError:
        print("{func} not found".format(func = func))
    return -1

def compareTest(k, n_0 = 200, ls_0 = 30, ls_1 = 35, tests = 300, function1 = "runScen2_3_1", function2 = "runScen2_3"):
    n = n_0
    location_set = [ls_0, ls_1]
    win = 0
    loss = 0
    tie = 0
    for i in range(tests):
        print("Commencing test {num} for functions {func1} and {func2}".format(num = i, func1=function1, func2=function2))
        obj = DrugStoreCoffeeShops(n, k, location_set)
        obj.setup()
        
        result_0 = -1 #The maximum returned component of function1
        result_1 = -1 #The maximum returned compononent of function2
        try:
            result_0 = findMethod(obj, function1)

            # Write the results for scenario 2 (Pairing both shops to a person at a time)
            # writeResults(i, first_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])],
            # "unit_test_2_3.txt")
            
            obj.resetGraph() #Reset the graph so we can compare to the second test

            result_1 = findMethod(obj, function2)

            # Write the results for scenario 2.3 (Pairing a shop to each person at a time)
            # writeResults(i, second_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])], 
            # "unit_test_2_3.txt")
            
        except Exception as e: 
            traceback.print_exc()
            print(e)
            break
        if result_0 < 0 or result_1 < 0:
            pass
        if(result_0 == result_1):
            tie += 1
        else:
            if(result_0 > result_1):
                win += 1
            else:
                loss += 1
        del obj # Delete the DrugStoreCoffeeShop Object after using it  
    write("{func1} has {win} wins, {loss} losses, and {tie} ties over {func2}.\n".format(
        win=str(win), loss=str(loss), tie=str(tie), func1 = function1, func2 = function2)
        , "unit_test_2_3.txt")
    write("Constants : {n} People {l1} Gyms {l2} Stores; K closest match = {k}".format(
        n=n_0, k=k, l1 = ls_0, l2 = ls_1), "unit_test_2_3.txt")
        
def compareTestTest(k, n_0 = 130, ls_0 = 20, ls_1 = 25, tests = 300):
    function1 = "runScen2_3_1_rand" 
    function2 = "iterate(runScen2_3_1_rand)"
    n = n_0
    location_set = [ls_0, ls_1]
    win = 0
    loss = 0
    tie = 0
    timer_0 = 0
    timer_1 = 0
    for i in range(tests):
        print("Commencing test {num} for functions {func1} and {func2}".format(num = i, func1=function1, func2=function2))
        obj = DrugStoreCoffeeShops(n, k, location_set)
        obj.setup()
        
        result_0 = -1 #The maximum returned component of function1
        result_1 = -1 #The maximum returned compononent of function2
        start_0 = time.perf_counter()
        try:
            result_0 = findMethod(obj, function1)

            # Write the results for scenario 2 (Pairing both shops to a person at a time)
            # writeResults(i, first_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])],
            # "unit_test_2_3.txt")
            
            timer_0 += time.perf_counter() - start_0
            obj.resetGraph() #Reset the graph so we can compare to the second test

            start_1 = time.perf_counter()
            result_1 = obj.iterateMe(obj.runScen2_2Random.__name__, 500)
            timer_1 += time.perf_counter() - start_1
            # Write the results for scenario 2.3 (Pairing a shop to each person at a time)
            # writeResults(i, second_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])], 
            # "unit_test_2_3.txt")
            
        except Exception as e: 
            traceback.print_exc()
            print(e)
            break
        if result_0 < 0 or result_1 < 0:
            pass
        if(result_0 == result_1):
            tie += 1
        else:
            if(result_0 > result_1):
                win += 1
            else:
                loss += 1
        del obj # Delete the DrugStoreCoffeeShop Object after using it
    write("{func1} has {win} wins, {loss} losses, and {tie} ties over {func2}. \n".format(
        win=str(win), loss=str(loss), tie=str(tie), func1 = function1, func2 = function2)
        + " And {funcFast} was faster by ".format(funcFast = function1 if timer_0 < timer_1 else function2) 
        + "{:e}".format(timer_1 / timer_0 if timer_0 < timer_1 else timer_0 / timer_1) + "%"
        , "unit_test_2_3.txt")
    write("Constants : {n} People {l1} Gyms {l2} Stores; K closest match = {k}".format(
        n=n_0, k=k, l1 = ls_0, l2 = ls_1), "unit_test_2_3.txt")

def compareAvgIterate(k, n_0 = 130, ls_0 = 20, ls_1 = 25, tests = 300, i = 50, function1 = "runScen2_3_1_rand" ):
    n = n_0
    location_set = [ls_0, ls_1]
    timer_0 = 0
    results_total = 0
    failed_tests = 0
    for j in range(tests):
        print("Commencing test {num} for function {func1}".format(num = j, func1 = "iterateMe({f},{i})".format(f=function1, i=i)))
        obj = DrugStoreCoffeeShops(n, k, location_set)
        obj.setup()
        result_0 = -1 #The maximum returned component of function1
        start_0 = time.perf_counter()
        try:
            result_0 = obj.iterateMe(function1, i)
            results_total += result_0
            # Write the results for scenario 2 (Pairing both shops to a person at a time)
            # writeResults(i, first_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])],
            # "unit_test_2_3.txt")
            
            timer_0 += time.perf_counter() - start_0
            # Write the results for scenario 2.3 (Pairing a shop to each person at a time)
            # writeResults(i, second_elapse, "{:e}".format(n), k, ["{:e}".format(location_set[0]), "{:e}".format(location_set[1])], 
            # "unit_test_2_3.txt")
            
        except Exception as e: 
            failed_tests += 1
            traceback.print_exc()
            print(e)
            pass
        del obj # Delete the DrugStoreCoffeeShop Object after using it
    tests -= failed_tests
    write("\n{func1} has an average largest people size of {numPeople}. \n".format(
        func1 = "iterateMe({f},{i})".format(f=function1, i=i) , numPeople = results_total / tests)
        + " {funcFast} ran at an average time of ".format(funcFast = "iterateMe({f},{i})".format(f=function1, i=i)) 
        + "{:e}".format(timer_0/tests) + "(s)\n"
        + "Constants : {n} People {l1} Gyms {l2} Stores; K closest match = {k}".format(
        n=n_0, k=k, l1 = ls_0, l2 = ls_1), "unit_test_2_3.txt")

def customTest():
    custom_graph = "../data/exports/random_50people_10gym_15store_3k.gml"
    results_total = 0
    tests = 2000
    total_time = 0

    for i in range(tests):
        print("Commencing test {i}".format(i = i))
        b = DrugStoreCoffeeShops(0, 0, [0,0])
        b.setup()
        b.import_lgraph(custom_graph, custom_graph)
        
        start_0 = time.perf_counter()
        # b.partition_lgraph_louvain()
        # b.G_to_disjoint()
        results_total += b.runScen2_3_1_rand()
        total_time += time.perf_counter() - start_0


    write("\n{func1} has an average largest people size of {numPeople}. \n".format( numPeople = (results_total / tests),
        func1 = "Random Algorithm (Queue Greedy Algorithm)")
        + "{funcFast} ran at an average time of ".format(funcFast = "Random Algorithm") 
        + "{:e}".format(total_time/tests) + "(s)\n"
        + "Constants : {n} People {l1} Gyms {l2} Stores; K closest match = {k}".format(
        n=50, k=3, l1 = 10, l2 = 15), "partition_test.txt")
if __name__ == "__main__" :
    # #k doesnn't matter with scen2
	# stressTestN(stressTestScen2_3_1, 5, [5, 5])
	# stressTestLocNum(stressTestScen2, 100, 5)
	# stressTestLocSize(stressTestScen2, 1000, 5)
    # tempObj = DrugStoreCoffeeShops(0, 0, [0,0])
    # compareTestTest(3, tests=50)
    # for b in range(1, 10):
    #     compareAvgIterate(3, tests = 200, i=b, function1=tempObj.runScen2_3_1_rand.__name__)
    customTest()
    # compareTest(3, tests = 3000, function1=tempObj.runScen2_3_1.__name__, function2=tempObj.runScen2_3_1_rand.__name__)
    # stressTestCompareScen2_2Scen2_3(3)