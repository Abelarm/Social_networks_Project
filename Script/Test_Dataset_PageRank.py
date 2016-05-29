#!/usr/bin/python
import json

from PageRank import pageRank2
from load_dataset import get_graph
import timeit

graph = get_graph()

start_time = timeit.default_timer()
print("---------DUMPING RESULT---------")
time2, rank2 = pageRank2(graph,0.85,75,0)
print("---------FINISHED PAGERANK---------")
elapsed2 = timeit.default_timer() - start_time
print (elapsed2)

print("---------DUMPING RESULT---------")
with open('PageRank.json','w') as PR:
	json.dump(rank2,fp)
print("---------FINISHED DUMPING---------")
