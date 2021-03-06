#!/usr/bin/python

from collections import OrderedDict
from Parser import read_wibbi
import json
import random
import operator

def set_default(obj):
	if isinstance(obj,set):
		return list(obj)
	raise TypeError

def create_link(dataset):
  for name1 in dataset:
      for name2 in dataset:
         if name1!=name2:

             U = random.sample(dataset[name1]["graph"].keys(),10)
             V = random.sample(dataset[name2]["graph"].keys(),10)

             for i in range(len(U)):
                 if V[i] not in dataset[name1]["graph"][U[i]]: 
                     dataset[name1]["graph"][U[i]].add(V[i])


def invert_db(dataset):
  new_db = dict()
  temp_db = dict()
  azz = 0
  for name in dataset:
    db = dataset[name]["db"]
    
    for k in db:
      len_k = len(db[k])
      
      for w in db[k]:

        if w not in temp_db:
          temp_db[w]=dict()

        count = db[k].count(w)
        temp_db[w][k] = float(count)/len_k
  
  for w in temp_db:
    sorted_docs = OrderedDict(sorted(temp_db[w].items(), key=operator.itemgetter(1), reverse=True))
    new_db[w] = sorted_docs
  dataset["inv_db"] = new_db


siti = ["ARTS","BUSINESS","COMPUTERS","GAMES","HEALTH","HOME","KIDS","NEWS","RECREATION","REFERENCE","REGIONAL",
"SCIENCE","SHOPPING","SOCIETY","SPORTS"]

#siti = ["SOCIETY","SPORTS"]

dataset = dict()
for name in siti:
	print("Parsing: " + name)
	graph,db = read_wibbi(name+".pages")
	dataset[name] = {"graph":graph,"db":db}
	print("----------------")

print("------FINISHED PARSING-----")

print("------CREATING FAKE LINK -----")
create_link(dataset)
print("------FINISHED CREATING-------")
print("------INVERTING DATABASE------")
invert_db(dataset)
print("------INVERTING FINISHED------")
print("------START DUMPING-----")
with open('../dataset.json', 'w') as fp:
        stri = json.dumps(dataset, ensure_ascii=False, default = set_default)
        fp.write(stri)
print("------DONE-----")




