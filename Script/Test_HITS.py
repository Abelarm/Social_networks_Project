from HITS import *
import timeit
from load_dataset import get_fullgraph

graph = get_fullgraph()

print("STARTING HITS")
start_time = timeit.default_timer()
time , a, h = HITS2(graph,1000,0.001)
elapsed= timeit.default_timer() - start_time
print("HITS2 elapsed: " + str(elapsed))
print("Time:" + str(time))


result = dict()

for k in graph:
	result[k] = {"a": a[k], "h": h[k]}

print("---------DUMPING RESULT---------")
with open('HITS.json','w') as fp:
	json.dump(result,fp)
print("---------FINISHED DUMPING---------")


#print ("A: " + str(a))
#print ("H: "+ str(h))