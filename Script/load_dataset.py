import json

def load():
    with open('dataset.json') as file:
        stri = file.read()
        data = json.loads(stri, encoding='utf-8')
    return data

def graph():
    all_graph = dict()
    data = load()
    print("LOAD FILE COMPLETE")
    for name in data.keys():
        graph = data[name]["graph"]
        all_graph.update(graph)
        
    return all_graph

def inverted():

  data = load()
  return data["inv_db"]

def db():
   
   all_db = dict()
   data = load()
   for name in data:
       db = data[name]["db"]
       all_db.update(db)

   return all_db

dt=inverted()
print(dt.keys())