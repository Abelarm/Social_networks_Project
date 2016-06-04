#!/usr/bin/python
from load_dataset import get_inverted, get_PageRank_graph, get_HITS_graph
from Dataset_Matching import *
import pprint
import operator
from collections import OrderedDict
import timeit
from get_query import query

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

print("-------------LOADING FULL DATASET-------------")
start_time = timeit.default_timer()
inverted_db = get_inverted()
elapsed = timeit.default_timer() - start_time
print("Database loading time: "+str(elapsed))
start_time = timeit.default_timer()
PageRank_graph = get_PageRank_graph()
elapsed = timeit.default_timer() - start_time
print("PageRank graph loading time: "+str(elapsed))
start_time = timeit.default_timer()
HITS_graph = get_HITS_graph()
elapsed = timeit.default_timer() - start_time
print("HITS loading time: "+str(elapsed))
print("---------------------------------------------")


queries_key = query()
print("--------------------LENGTH--------------------")
tot = 0
print(len(queries_key))
for q_k in queries_key:
    query = queries_key[q_k]
    print("--------------------QUERY--------------------")
    query = ' '.join(query)
    print(query)

    print("------------------BEST MATCH-----------------")
    start_time = timeit.default_timer()
    result = best_match(query, 0, inverted_db)
    elapsed = timeit.default_timer() - start_time
    print("Best Match time: "+str(elapsed))
    pprint.pprint(str(result))
    print(q_k)

    if q_k in result:
        tot += 1
        print("TUTTO COME SPERATOOOOOOOOOOOOOOOOOOOOOOO")
    
    print("--------BEST MATCH ORDERED BY PAGERANK-------")
    start_time = timeit.default_timer()
    resultPG = order_by_PageRank(result, PageRank_graph)
    elapsed = timeit.default_timer() - start_time
    #print("Best Match Pagerank ordering time: "+str(elapsed))
    #pprint.pprint(str(resultPG))
    
    print("----------BEST MATCH ORDERED BY HITS---------")
    start_time = timeit.default_timer()
    resultH = order_by_HITS(result, HITS_graph,"a")
    elapsed = timeit.default_timer() - start_time
    #print("Best Match HITS ordering time: "+str(elapsed))
    #pprint.pprint(str(resultH))
    
    print("-------------IMPROVED BEST MATCH-------------")
    start_time = timeit.default_timer()
    result2 = improved_best_match(query, inverted_db)
    elapsed = timeit.default_timer() - start_time
    #print("Improved Best Match time: "+str(elapsed))
    #pprint.pprint(str(result2))

    if q_k in result2:
        tot += 1
        print("TUTTO COME SPERATOOOOOOOOOOOOOOOOOOOOOOO")
    
    print("---IMPROVED BEST MATCH ORDERED BY PAGERANK---")
    start_time = timeit.default_timer()
    result2PG = order_by_PageRank(result2, PageRank_graph)
    elapsed = timeit.default_timer() - start_time
    #print("Improved Best Match Pagerank ordering time: "+str(elapsed))
    #pprint.pprint(str(result2PG))
    
    print("-----IMPROVED BEST MATCH ORDERED BY HITS-----")
    start_time = timeit.default_timer()
    result2H = order_by_HITS(result2, HITS_graph,"a")
    elapsed = timeit.default_timer() - start_time
    #print("Improved Best Match HITS ordering time: "+str(elapsed))
    #pprint.pprint(str(result2H))

    #print("---------------------------------------------")

print tot
