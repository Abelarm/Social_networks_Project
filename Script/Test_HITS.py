from HITS import *
import json
import timeit
from load_dataset import get_fullgraph

rep = 10
elapsed_load = 0
elapsed_dump = 0
elapsed = 0
for i in range(rep):
	start_time_load = timeit.default_timer()
	graph = get_fullgraph()
	elapsed_load += timeit.default_timer() - start_time_load 

	print("STARTING HITS")
	start_time = timeit.default_timer()
	time , a, h = HITS2(graph,1000)
	elapsed += timeit.default_timer() - start_time
	print("HITS2 elapsed: " + str(elapsed))
	print("Time:" + str(time))


	result = dict()

	for k in graph:
		result[k] = {"a": a[k], "h": h[k]}

	start_time_dump = timeit.default_timer()
	print("---------DUMPING RESULT---------")
	with open('HITS.json','w') as fp:
		json.dump(result,fp)
	print("---------FINISHED DUMPING---------")
	elapsed_dump += timeit.default_timer() - start_time_dump


print("Load:\t"+str(elapsed_load))
print("Algorithn:\t"+str(elapsed))
print("Dump:\t"+str(elapsed_dump))