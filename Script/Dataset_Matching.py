#!/usr/bin/python 
from collections import OrderedDict
import operator

###BEST MATCH###         
def best_match(query, threshold, word_advs):
    adv_weights = dict()
    best_docs = OrderedDict()
    
    query = query.lower()
    query_words = query.split()
    
    #For every word we look at each document in the list and we increment the document's weight (based on frequency)
    for word in query_words:
        if word not in word_advs:
            continue
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

def compute_weight(impacts, word_advs, doc):
    weight = 0
    for word in impacts:
        if doc in word_advs[word]:
            weight += word_advs[word][doc]
    return weight

def remove_and_add(docs, last_sorted_docs_key, k, weight):

    #print("Removed k:" + str(last_sorted_docs_key) +" v: " + str(docs[last_sorted_docs_key]))
    del docs[last_sorted_docs_key]

    #print("Added k:" + str(k) +" v: " + str(weight))
    docs[k] = weight

    return OrderedDict(sorted(docs.items(), key = operator.itemgetter(1), reverse=True))


def update_docs(to_consider, word_advs, impacts, impact_keys, docs):

    sorted_docs = OrderedDict(sorted(docs.items(), key = operator.itemgetter(1), reverse=True))
    sorted_docs_key = list(sorted_docs.keys())

    for not_cos_key in list(word_advs[to_consider].keys()):
        #print("Considering: " + to_consider)
        estimate_weight = word_advs[to_consider][not_cos_key]

        index_to_consider =  impact_keys.index(to_consider)

        for i in range(index_to_consider+1,len(impacts)):

            estimate_weight += impacts[impact_keys[i]]

        last_sorted_docs_key = sorted_docs_key[-1]
        if estimate_weight > sorted_docs[last_sorted_docs_key]:
            
            real_weight = compute_weight(impacts, word_advs, not_cos_key)

            if real_weight > sorted_docs[last_sorted_docs_key]:
                #print("Updating with: " + to_consider + "--------------")
                sorted_docs = remove_and_add(sorted_docs, last_sorted_docs_key, not_cos_key, real_weight)
                sorted_docs_key = list(sorted_docs.keys())
        else:
            break

    return sorted_docs

    
###BEST MATCH###         
def improved_best_match(query, word_advs):
    
    query = query.lower()
    query_words = query.split()
    
    #computing impact of query_words as the maximum frequency for that word
    temp = dict()
    for word in query_words:
        if word not in word_advs:
            continue
        #impact is first frequency of word, since in decreasing order
        temp[word] = list(word_advs[word].values())[0]
    #sorting impacts in decreasing order
    impacts = OrderedDict(sorted(temp.items(), key=operator.itemgetter(1), reverse=True))
    #print(impacts)

    impact_keys = list(impacts.keys())
    
    #consider the first 20 documents in the index of the first query term
    #if the first query term has an index with less than 20 documents
    #then complete the list of 20 documents with the first documents in
    #the index of the next query term
    #Then compute the score for each of these documents
    docs = dict()
    rem_len = 20
    for index, word in enumerate(impacts):
        while rem_len > 0:
            #print("TAKING DOCUMENTS from "+word)
            keys = list(word_advs[word].keys())
            for k in keys:
                docs[k] = compute_weight(impacts, word_advs, k)
                rem_len -= 1
                if rem_len == 0:
                    last_index = index
                    break;
        if index == len(impacts):
            return docs
        if last_index != index:
            #print(word+ " not in docs")
            docs = update_docs(word, word_advs, impacts, impact_keys, docs) 

    return docs        


