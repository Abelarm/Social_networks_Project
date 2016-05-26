#!/usr/bin/python 
from collections import OrderedDict
import operator

#The operation of retriving advertisers or documents matching a given query can be executed in two phases:
#in the first phase, we build the necessary data structures;
#in the second phase, we answer to the given query.

#The first phase is usually run only once.
#The data structure that is usually built in this phase is an "inverted index".
#This is a dictionary that for every word (or for every query phrase) mantains a list of
#documents containing that word (query phrase) / advertisers requesting to appear on that word (query phrase).
#In this phase, we assume that there is a database in which we save for each document (advertiser, resp.)
#the link to the document (the name of the advertiser, resp.)
#and the list of word (or phrases) of the document (on which the advertiser request to appear, resp.).
#In the implementations below we assume that the database is a file as follows:
#    nome_adv1 prova,test,prova esame,esame,appello,appello esame
#    nome_adv2 prova,esempio,caso semplice,evidenza
#    nome_adv3 esempio test,esempio esame,esempio prova,esame prova

#The second phase must be executed for any issued query.
#Different strategies are available for this phase:
#either we look for an exact match of the query in the document / advertisers' requests
#or we look for document / advertiser' requests that are "good" match, but not necessarily exact.

###BEST MATCH###         
def best_match(query, threshold, word_advs):
    adv_weights = dict()
    best_docs = OrderedDict()
    
    query_words = query.split()
    
    #For every word we look at each document in the list and we increment the document's weight (based on frequency)
    for word in query_words:
        for doc in word_advs[word]:
            if doc not in adv_weights.keys():
                adv_weights[doc] = word_advs[word][doc]
            else:
                adv_weights[doc] += word_advs[word][doc]
    #We sort all documents by value, in decreasing order
    sorted_docs = OrderedDict(sorted(adv_weights.items(), key=operator.itemgetter(1), reverse=True))
    count = 0
    for doc in sorted_docs:
        #if the document's weight is more than threshold
        #and we haven't yet reached 20 documents
        if sorted_docs[doc]>=threshold and count < 20:
            best_docs[doc] = sorted_docs[doc]
            count += 1
        #this document and all the following are not more than threshold (since docs are in decreasing order)
        else:
            break
    return best_docs

###BEST MATCH###         
def improved_best_match(query, threshold, word_advs):
    adv_weights = dict()
    best_docs = OrderedDict()
    
    query_words = query.split()
    
    #computing impact of query_words as the maximum frequency for that word
    temp = dict()
    for word in query_words:
        #impact is first frequency of word, since in decreasing order
        temp[word] = word_advs[word].values()[0]
    #sorting impacts in decreasing order
    impacts = OrderedDict(sorted(temp.items(), key=operator.itemgetter(1), reverse=True))
    
    #consider the first 20 documents in the index of the first query term
    #if the first query term has an index with less than 20 documents
    #then complete the list of 20 documents with the first documents in
    #the index of the next query term
    taken_count = 0
    taken_docs = OrderedDict()
    for word in impacts:
        for doc in word_advs[word][:20] and taken_count<=20:
            taken.add()#TODO
    #We sort all documents by value, in decreasing order
    sorted_docs = OrderedDict(sorted(adv_weights.items(), key=operator.itemgetter(1), reverse=True))
    count = 0
    for doc in sorted_docs:
        #if the document's weight is more than threshold
        #and we haven't yet reached 20 documents
        if sorted_docs[doc]>=threshold and count < 20:
            best_docs[doc] = sorted_docs[doc]
            count += 1
        #this document and all the following are not more than threshold (since docs are in decreasing order)
        else:
            break
    return best_docs