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
 

siti = ["ARTS","BUSINESS","COMPUTERS","GAMES","HEALTH","HOME","KIDS","NEWS","RECREATION","REFERENCE","REGIONAL",
"SCIENCE","SHOPPING","SOCIETY","SPORTS"]

#siti = ["KIDS"]

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

print("------START DUMPING-----")
with open('../dataset.json', 'w') as fp:
        stri = json.dumps(dataset, ensure_ascii=False, default = set_default)
        fp.write(stri)
print("------DONE-----")




