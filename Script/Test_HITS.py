from HITS import *
import timeit


simple = [[0, 1, 1, 1, 0], [1, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]]


start_time = timeit.default_timer()
time , a, h = HITS1(simple,1000)
elapsed = timeit.default_timer() - start_time
print("HITS1 elapsed: " + str(elapsed))
print("Time:" + str(time))
print ("A: " + str(a))
print ("H: "+ str(h))

# Graph is represented with its adjacency lists
simple = dict()
simple['x'] = {'y','z','w'}
simple['y'] = {'x','w'}
simple['z'] = {'k'}
simple['w'] = {'y','z'}
simple['k'] = {}

start_time = timeit.default_timer()
time , a, h = HITS2(simple,1000)
elapsed= timeit.default_timer() - start_time
print("HITS2 elapsed: " + str(elapsed))
print("Time:" + str(time))
print ("A: " + str(a))
print ("H: "+ str(h))