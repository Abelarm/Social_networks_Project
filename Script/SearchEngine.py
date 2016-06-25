#!/usr/bin/python
from load_dataset import get_inverted, get_PageRank_graph, get_HITS_graph
from Dataset_Matching import *
import pprint
import operator
from collections import OrderedDict
import timeit

def order_by_PageRank(result, PageRank_graph):
    temp = dict()
    for doc in result:
        temp[doc] = PageRank_graph[doc]
    resultPR = OrderedDict(sorted(temp.items(), key=operator.itemgetter(1), reverse=True))
    return resultPR

def order_by_HITS(result, HITS_graph, tp):
    temp = dict()
    for doc in result:
        temp[doc] = HITS_graph[doc][tp]
    resultH = OrderedDict(sorted(temp.items(), key=operator.itemgetter(1), reverse=True))
    return resultH

#print("-------------LOADING FULL DATASET-------------")
#start_time = timeit.default_timer()
inverted_db = get_inverted()
#elapsed = timeit.default_timer() - start_time
#print("Database loading time: "+str(elapsed))
#start_time = timeit.default_timer()
PageRank_graph = get_PageRank_graph()
#elapsed = timeit.default_timer() - start_time
#print("PageRank graph loading time: "+str(elapsed))
#start_time = timeit.default_timer()
HITS_graph = get_HITS_graph()
#elapsed = timeit.default_timer() - start_time
#print("HITS loading time: "+str(elapsed))
#print("---------------------------------------------")



tot = 0
query = ""
print("--------------------QUERY--------------------")
print(query)
print("-------------EXPECTED DOCUMENT---------------")
print("ign")
print("------------------BEST MATCH-----------------")
start_time = timeit.default_timer()
result = best_match(query, 0, inverted_db)
elapsed = timeit.default_timer() - start_time
print("Best Match time: "+str(elapsed))
print(str(result))

for r in result:
    if "ign" in r:
        print("FOUND EXPECTED DOCUMENT")
        tot += 1

print("--------BEST MATCH ORDERED BY PAGERANK-------")
#start_time = timeit.default_timer()
resultPG = order_by_PageRank(result, PageRank_graph)
#elapsed = timeit.default_timer() - start_time
#print("Best Match Pagerank ordering time: "+str(elapsed))
print(str(resultPG))

print("----------BEST MATCH ORDERED BY HITS---------")
#start_time = timeit.default_timer()
resultH = order_by_HITS(result, HITS_graph,"a")
#elapsed = timeit.default_timer() - start_time
#print("Best Match HITS ordering time: "+str(elapsed))
print(str(resultH))

print("-------------IMPROVED BEST MATCH-------------")
start_time = timeit.default_timer()
result2 = improved_best_match(query, inverted_db)
elapsed = timeit.default_timer() - start_time
print("Improved Best Match time: "+str(elapsed))
print(str(result2))

for r in result2:
    if "ign" in r:
        print("FOUND EXPECTED DOCUMENT")
        tot += 1

print("---IMPROVED BEST MATCH ORDERED BY PAGERANK---")
#start_time = timeit.default_timer()
result2PG = order_by_PageRank(result2, PageRank_graph)
#elapsed = timeit.default_timer() - start_time
#print("Improved Best Match Pagerank ordering time: "+str(elapsed))
print(str(result2PG))

print("-----IMPROVED BEST MATCH ORDERED BY HITS-----")
#start_time = timeit.default_timer()
result2H = order_by_HITS(result2, HITS_graph,"a")
#elapsed = timeit.default_timer() - start_time
#print("Improved Best Match HITS ordering time: "+str(elapsed))
print(str(result2H))

#print("---------------------------------------------")
