#!/usr/bin/python


from Parser import read_wibbi
import json
import random

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
  
  for name in dataset:
    db = dataset[name]["db"]
    
    for  k in db.keys():
      len_k = len(db[k])
      
      for w in db[k]:

        if w not in new_db:
          new_db[w]=dict()

        count = db[k].count(w)
        new_db[w][k] = float(count)/len_k

  dataset["inv_db"] = new_db


siti = ["ARTS","BUSINESS","COMPUTERS","GAMES","HEALTH","HOME","KIDS","NEWS","RECREATION","REFERENCE","REGIONAL",
"SCIENCE","SHOPPING","SOCIETY","SPORTS"]

siti = ["SOCIETY","SPORTS"]

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
li = list(dataset["inv_db"].keys())
for i in range(2):
    print(str(li[i])+": "+str(dataset["inv_db"][li[i]]))
print("------START DUMPING-----")
with open('../dataset.json', 'w') as fp:
        stri = json.dumps(dataset, ensure_ascii=False, default = set_default)
        fp.write(stri)
print("------DONE-----")




