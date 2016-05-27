#!/usr/bin/python
from load_dataset import get_inverted
from Dataset_Matching import *

inverted_db = get_inverted()
query = "UN resolution China ban weapons"
print("QUERY: "+query)

'''
result = best_match(query, 0.02, inverted_db)
print("BEST MATCH: "+str(result))

'''
result2 = improved_best_match(query, inverted_db)
print("IMPROVED BEST MATCH: "+str(result2))
