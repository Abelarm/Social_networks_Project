#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from load_dataset import get_fullgraph
from joblib import Parallel, delayed

def HITS1(graph,step,confidence=1.0e-6):
  n = len(graph)
  nodes = range(n)
  done = 0
  time = 0
  
  #Initialization
  h = np.ones((n,1))
  L = np.matrix(graph)
  a = np.zeros((n,1))

  lastA = np.zeros((n,1))
  lastH = np.zeros((n,1))
    
  while not done and time < step:
    print("Step: " + str(time)+"/"+str(step))
    time += 1

    a = np.dot(L.transpose(),h)

    maxA = np.amax(a)
    a/=maxA

    h = np.dot(L,a)
    maxH = np.amax(h)
    h /=maxH

    diffa = np.abs(a - lastA).sum()
    diffh = np.abs(h - lastH).sum()
    lastA = a
    lastH = h
    
    if diffa <= confidence or diffh < confidence:
      done = 1
    
  return time, a.flatten().tolist(), h.flatten().tolist()

def HITS2(graph,step,confidence=1.0e-6):

  nodes=graph.keys()
  n=len(nodes)
  done = 0
  time = 0
  
  #Initialization
  a = dict()
  h = dict()
  lastA = dict()
  lastH = dict()
  olddiffa = 0
  olddiffh = 0
  for i in nodes:
    a[i] = 0.0
    lastA[i] = 0.0
    h[i] = 1.0 
    lastH[i] = 0.0


  
  while not done and time < step:
    #print("Step: " + str(time)+"/"+str(step))
    time += 1
    
    maxA = -1
    for n in nodes:
      incoming = graph[n]["incoming"]
      a[n] = 0
      if type(incoming) == float:
        incoming=[]
      for i in incoming:
          if i in h:
            a[n] += h[i]
      if a[n] > maxA:
        maxA = a[n]  
 
    for n in nodes:
      #print(a[n])
      a[n]/=maxA
      #print(a[n])

    maxH = -1 
    for n in nodes:
      outgoing = graph[n]["outgoing"]
      h[n] = 0
      if type(outgoing) == float:
        outgoing=[]
      for o in outgoing:
        if o in a:
          h[n] += a[o]
      if h[n] > maxH:
        maxH = h[n]

    for n in nodes:
      h[n]/=maxH

    #print("A: " +str(a))
    #print("H: " +str(h))
    #raw_input()

    #Computes the distance between the old rank vector and the new rank vector in L_1 norm

    npa = np.array(list(a.values()))
    nph = np.array(list(h.values()))
    nplastA = np.array(list(lastA.values()))
    nplastH = np.array(list(lastH.values()))

    diffa = np.abs(npa - nplastA).sum()
    diffh = np.abs(nph - nplastH).sum()
    lastA = a.copy()
    lastH = h.copy()

    #print(float(olddiffa)-diffa)

    if diffa <= confidence or diffh < confidence:
        done = 1

    if np.abs(olddiffa-diffa) <= confidence or np.abs(olddiffh-diffh) <= confidence:
        done = 1

    olddiffa = diffa
    olddiffh = diffh

    #print("Iteration: " + str(time) +"/" +str(step) + " diffa: " + str(diffa) + " diffh " + str(diffh))
    
  return time, a, h


def calculate_a(list_key, graph, h):

  a = dict()
  
  maxA = -1
  for n in list_key:
    incoming = graph[n]["incoming"]
    a[n] = 0
    if type(incoming) == float:
      incoming=[]
    for i in incoming:
        if i in h:
          a[n] += h[i]
    if a[n] > maxA:
      maxA = a[n] 

  return maxA, a

def calculate_h(list_key, graph, a):

  h = dict()
  maxH = -1 
  for n in list_key:
    outgoing = graph[n]["outgoing"]
    h[n] = 0
    if type(outgoing) == float:
      outgoing=[]
    for o in outgoing:
      if o in a:
        h[n] += a[o]
    if h[n] > maxH:
      maxH = h[n]

  return maxH, h


def HITS_parallel(graph,step,confidence=1.0e-6):

  num_procs = 4
  nodes=graph.keys()
  num_nodes=len(nodes)
  done = 0
  time = 0
  
  #Initialization
  a = dict()
  h = dict()
  lastA = dict()
  lastH = dict()
  olddiffa = 0
  olddiffh = 0
  for i in nodes:
    a[i] = 0.0
    lastA[i] = 0.0
    h[i] = 1.0 
    lastH[i] = 0.0

  with Parallel(n_jobs = num_procs) as parallel:
  
    while not done and time < step:
      #print("Step: " + str(time)+"/"+str(step))
      time += 1

      split_keys = lambda lst,sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]

      chunk_size = int(num_nodes/num_procs)

      keys = split_keys(list(graph.keys()), chunk_size)

      result_a = parallel(delayed(calculate_a)(keys[i], graph, h) for i in range(len(keys)))
      #print (result_a)

      maxA = max([result_a[i][0] for i in range(num_procs)])

      a = dict()

      for i in range(num_procs):
        a.update(result_a[i][1])

      for n in a:
        a[n] /= maxA

      result_h = parallel(delayed(calculate_h)(keys[i], graph,  a) for i in range(len(keys)))

      maxH = max([result_h[i][0] for i in range(num_procs)])

      h = dict()

      for i in range(num_procs):
        h.update(result_h[i][1])

      for n in h:
        h[n] /= maxH

      #print("A: " +str(a))
      #print("H: " +str(h))
      #raw_input()

      #Computes the distance between the old rank vector and the new rank vector in L_1 norm

      npa = np.array(list(a.values()))
      nph = np.array(list(h.values()))
      nplastA = np.array(list(lastA.values()))
      nplastH = np.array(list(lastH.values()))

      diffa = np.abs(npa - nplastA).sum()
      diffh = np.abs(nph - nplastH).sum()
      lastA = a.copy()
      lastH = h.copy()

      #print(float(olddiffa)-diffa)

      if diffa <= confidence or diffh < confidence:
          done = 1

      if np.abs(olddiffa-diffa) <= confidence or np.abs(olddiffh-diffh) <= confidence:
          done = 1

      olddiffa = diffa
      olddiffh = diffh

      #print("Iteration: " + str(time) +"/" +str(step) + " diffa: " + str(diffa) + " diffh " + str(diffh))

  return time, a, h