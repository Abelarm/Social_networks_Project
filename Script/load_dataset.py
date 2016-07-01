import json
from collections import OrderedDict
import re
import operator

def load():
	print ("START LOADING")
	with open('dataset.json') as file:
		stri = file.read()
		data = json.loads(stri, object_pairs_hook = OrderedDict, encoding='utf-8')
	return data

def get_graph():
	all_graph = dict()
	data = load()
	print("LOAD FILE COMPLETE")
	for name in data.keys():
		graph = data[name]["graph"]
		all_graph.update(graph)
	return all_graph

def dump_forD3():
	graph = get_graph()
	nodes = []
	links = []
	keys = list(graph.keys())
	print ("Starting creating graph for d3")
	for k in keys:
		obj = dict()
		obj["name"] = k
		group =  re.search('^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)',k)
		if group.group(0):
			obj["group"] = group.group(0)
		else:
			obj["group"] =  "ukn"

		nodes.append(obj)
		if type(graph[k]) == float:
			continue
		for o in graph[k]:
			link = dict()
			link["source"] = keys.index(k)
			link["target"] = keys.index(o)
			link["value"] = 1
			links.append(link)

	graph_d3 = dict()
	graph_d3["nodes"] = nodes
	graph_d3["links"] = links
	print ("Starting dumping")
	with open('graph_D3.json', 'w') as fp:
		stri = json.dumps(graph_d3, ensure_ascii=False)
		fp.write(stri)


def get_graph_partial(num):
	all_graph = dict()
	data = load()
	print("LOAD FILE COMPLETE")
	sub_part = 1 + int(num/15)
	for name in data.keys():
		graph = data[name]["graph"]
		graph_key = list(graph.keys())[:sub_part]
		for k in graph_key:
			all_graph[k] = graph[k]
	print (len(all_graph))
	return all_graph	

def get_fullgraph():
	with open('full_graph.json') as file:
		stri = file.read()
		fullgraph = json.loads(stri, encoding='utf-8')
	return fullgraph

def get_fullgraph_num(num):
	with open('full_graph'+str(num)+'.json') as file:
		stri = file.read()
		fullgraph = json.loads(stri, encoding='utf-8')
	return fullgraph

def get_inverted():

	data = load()
	#print(len(data["inv_db"].keys()))
	return data["inv_db"]

def get_db():
	 
	all_db = dict()
	data = load()
	for name in data:
		if name == "inv_db":
			continue
		db = data[name]["db"]
		all_db.update(db)

	return all_db

def get_db_ordered():
	print("STARTING ORDERING")
	db = get_db()
	new_db = dict()
	
	for k in db:
		len_k = len(db[k])
		if len_k == 0:
			continue
		temp_db = dict()

		for w in db[k]:
			if w not in temp_db:
				temp_db[w]=dict()

			count = db[k].count(w)
			temp_db[w] = float(count)/len_k

		sorted_word = OrderedDict(sorted(temp_db.items(), key=operator.itemgetter(1), reverse=True))
		new_db[k] = list(sorted_word.keys())

	print("FINISHED ORDERING")
	return new_db


def count_word():
	data = load()
	sum = 0
	for name in data:
		if name == "inv_db":
			continue
		db = data[name]["db"]
		for l in db.keys():
			sum += len(db[l])
	return sum

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


def dump_full_graph_num(num):

	graph_mid = get_graph_partial(num)
	print("------CALCULATING FULLGRAPH------")
	full_graph = calcola_fullgraph(graph_mid)
	print("------FINISHED FULLGRAPH-----")
	print("------START DUMPING-----")
	with open('full_graph'+str(num)+'.json', 'w') as fp:
					stri = json.dumps(full_graph, ensure_ascii=False)
					fp.write(stri)
	print("------DONE-----")

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

def get_PageRank_graph():
	with open('PageRank.json') as file:
			stri = file.read()
			PageRank_graph = json.loads(stri, encoding='utf-8')
	return PageRank_graph

def get_HITS_graph():
	with open('HITS.json') as file:
			stri = file.read()
			HITS_graph = json.loads(stri, encoding='utf-8')
	return HITS_graph

#dump_full_graph_num(5000)