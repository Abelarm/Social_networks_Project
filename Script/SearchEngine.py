#!/usr/bin/python
from load_dataset import get_inverted, get_PageRank_graph, get_HITS_graph
from Dataset_Matching import *
import pprint
import operator
from collections import OrderedDict

def order_by_PageRank(result, PageRank_graph):
    temp = dict()
    for doc in result:
        temp[doc] = PageRank_graph[doc]
    resultPR = OrderedDict(sorted(temp.items(), key=operator.itemgetter(1), reverse=True))
    return resultPR

def order_by_HITS(result, HITS_graph):
    temp = dict()
    for doc in result:
        temp[doc] = HITS_graph[doc]
    resultH = OrderedDict(sorted(temp.items(), key=operator.itemgetter(1), reverse=True))
    return resultH

print("-------------LOADING FULL DATASET-------------")
inverted_db = get_inverted()
PageRank_graph = get_PageRank_graph()
HITS_graph = get_HITS_graph()
print("---------------------------------------------")

queries = []
queries.append("UN resolution China ban weapons")
queries.append("lego star wars")
queries.append("Hotel in Bolivia pleasant view")
queries.append("Obama")

for query in queries:
    print("--------------------QUERY--------------------")
    print(query)

    print("------------------BEST MATCH-----------------")
    result = best_match(query, 0, inverted_db)
    pprint.pprint(str(result))
    print("--------BEST MATCH ORDERED BY PAGERANK-------")
    resultPG = order_by_PageRank(result, PageRank_graph)
    pprint.pprint(str(resultPG))
    '''
    print("----------BEST MATCH ORDERED BY HITS---------")
    resultH = order_by_HITS(result, HITS_graph)
    pprint.pprint(str(resultH))
    '''
    
    print("-------------IMPROVED BEST MATCH-------------")
    result2 = improved_best_match(query, inverted_db)
    pprint.pprint(str(result2))
    print("---IMPROVED BEST MATCH ORDERED BY PAGERANK---")
    result2PG = order_by_PageRank(result2, PageRank_graph)
    pprint.pprint(str(result2PG))
    '''
    print("-----IMPROVED BEST MATCH ORDERED BY HITS-----")
    result2H = order_by_HITS(result2, HITS_graph)
    pprint.pprint(str(result2H))
    '''
    print("---------------------------------------------")
