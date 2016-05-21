import json
import ast

def load():
    with open('dataset.json') as file:
        stri = file.read()
        data = json.loads(stri, encoding='utf-8')
    return data

def graph():
    all_graph = dict()
    data = load()
    print("LOAD FILE COMPLETE")
    print(type(data))
    print(str(data)[:50])
    for name in data.keys():
        print("READING "+name)
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

#dt=load()
