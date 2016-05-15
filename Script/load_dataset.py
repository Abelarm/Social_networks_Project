import json
from StringIO import StringIO

def load():
    with open('dataset.json') as file:
        data = json.load(file)
    return data

def graph():
    all_graph = dict()
    data = load()
    for name in data:
        
        graph = data[name]["graph"]
        all_graph.update(graph)

    return all_graph


def db():
   
   all_db = dict()
   data = load()
   for name in data:
       
       db = data[name]["db"]
       all_db.update(db)

   return all_db
