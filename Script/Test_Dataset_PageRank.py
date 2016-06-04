#!/usr/bin/python
import json

from PageRank import pageRank2
from load_dataset import get_graph
import timeit

rep = 10
elapsed_load = 0
elapsed_dump = 0
elapsed = 0
for i in range(rep):

	start_time_load = timeit.default_timer()
	graph = get_graph()
	elapsed_load += timeit.default_timer() - start_time_load 

	start_time = timeit.default_timer()
	#print("---------STARTING PAGERANK---------")
	time2, rank2 = pageRank2(graph,0.85,75,0)
	#print("---------FINISHED PAGERANK---------")
	elapsed += timeit.default_timer() - start_time

	start_time_dump = timeit.default_timer()
	#print("---------DUMPING RESULT---------")
	with open('PageRank.json','w') as fp:
		json.dump(rank2,fp)
	#print("---------FINISHED DUMPING---------")
	elapsed_dump += timeit.default_timer() - start_time_dump

print("Load:\t"+str(elapsed_load))
print("Algorithn:\t"+str(elapsed))
print("Dump:\t"+str(elapsed_dump))