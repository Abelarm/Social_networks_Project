from HITS import *
import timeit
from load_dataset import *

graph =  graph()

print("STARTING HITS")
start_time = timeit.default_timer()
time , a, h = HITS2(graph,1000,0.01)
elapsed= timeit.default_timer() - start_time
print("HITS2 elapsed: " + str(elapsed))
print("Time:" + str(time))
print ("A: " + str(a))
print ("H: "+ str(h))