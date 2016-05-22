import json

def load():
    with open('dataset.json') as file:
        stri = file.read()
        data = json.loads(stri, encoding='utf-8')
    return data

def get_graph():
    all_graph = dict()
    data = load()
    print("LOAD FILE COMPLETE")
    for name in data.keys():
        graph = data[name]["graph"]
        all_graph.update(graph)
    return all_graph

def get_fullgraph():
  with open('full_graph.json') as file:
        stri = file.read()
        fullgraph = json.loads(stri, encoding='utf-8')
  return fullgraph

def inverted():

  data = load()
  return data["inv_db"]

def get_db():
   
   all_db = dict()
   data = load()
   for name in data:
       db = data[name]["db"]
       all_db.update(db)

   return all_db

def nodi_entranti(graph,name):
  toret = []
  for g in graph.keys():
    if not type(graph[g]) == float:
      if name in graph[g]:
        toret.append(g)

  return toret


def calcola_fullgraph(graph):
  incoming = []
  full_graph = dict()
  i=0
  for g in graph.keys():
    if not i%1000:
      print (i)
    incoming = nodi_entranti(graph,g)
    full_graph[g] = {"incoming": incoming, "outgoing": graph[g]}
    i += 1

  return full_graph


def dump_full_graph():
  graph_mid = graph()
  print("------CALCULATING FULLGRAPH------")
  full_graph = calcola_fullgraph(graph_mid)
  print("------FINISHED FULLGRAPH-----")
  print("------START DUMPING-----")
  with open('full_graph.json', 'w') as fp:
          stri = json.dumps(full_graph, ensure_ascii=False)
          fp.write(stri)
  print("------DONE-----")


#dump_full_graph()