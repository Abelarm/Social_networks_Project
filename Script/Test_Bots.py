#!/usr/bin/python

from random import randint, random, uniform
from Balance import balance_gsp
from Bots import *

#All possible queries
queries=["prova","test","esempio"]

#For each query, lists the available slots and their clickthrough rate
slot_ctrs=dict()
slot_ctrs["prova"]=dict()
slot_ctrs["prova"]["id1"] = 0.40
slot_ctrs["prova"]["id2"] = 0.15

slot_ctrs["test"]=dict()
slot_ctrs["test"]["id1"] = 0.33
slot_ctrs["test"]["id2"] = 0.30

slot_ctrs["esempio"]=dict()
slot_ctrs["esempio"]["id1"] = 0.25
slot_ctrs["esempio"]["id2"] = 0.30

#For each query, lists the advertisers that have a interest in that query
adv_values=dict()
adv_values["prova"]=dict()
adv_values["prova"]["x"] = 5
adv_values["prova"]["y"] = 10
adv_values["prova"]["z"] = 7

adv_values["test"]=dict()
adv_values["test"]["x"] = 4
adv_values["test"]["y"] = 2
adv_values["test"]["z"] = 7

adv_values["esempio"]=dict()
adv_values["esempio"]["x"] = 6
adv_values["esempio"]["z"] = 5
adv_values["esempio"]["z"] = 7

#The initial budget of each advertisers
adv_budgets=dict()
adv_budgets["x"] = 25
adv_budgets["y"] = 15
adv_budgets["z"] = 35

#Advertisers' bots
adv_bots=dict()
adv_bots["x"] = budget_saving
adv_bots["y"] = budget_saving
adv_bots["z"] = budget_saving

#It denotes the lenght of the sequence of queries that we will consider
num_query=10
history=[]
adv_bids=dict()

#Generate a random sequence of num_query queries, with each query selected from the list queries
query_sequence=[]
for i in range(num_query):
    #query_sequence.append("prova")
    query_sequence.append(queries[randint(0,len(queries)-1)])
                          
print(query_sequence)

adv_cbudgets=adv_budgets.copy() #The current budgets of advertisers
revenue=0 #The current revenue of the auctioneer

for i in range(num_query):
    
    current_query = query_sequence[i]
    
    adv_bids[current_query]=dict()
    for adv in adv_values[current_query]:
            adv_bids[current_query][adv] = adv_bots[adv](adv,adv_values[current_query][adv],slot_ctrs,history, current_query)

    #For each query we use the balance algorithm for evaluating the assignment and the payments
    #query_winners, query_pay = balance_fpa(slot_ctrs, adv_bids, adv_budgets, adv_cbudgets, query_sequence[i])
    query_winners, query_pay = balance_gsp(slot_ctrs, adv_bids, adv_budgets, adv_cbudgets, current_query)
    
    #Update the history
    history.append(dict())
    history[i][current_query]=dict()
    history[i][current_query]["adv_bids"]=dict(adv_bids)
    history[i][current_query]["adv_slots"]=dict(query_winners)
    history[i][current_query]["adv_pays"]=dict(query_pay)
    

    for j in query_winners.keys():
        #We now simulate an user clicking on the ad with a probability that is equivalent to the slot's clickthrough rate
        #p = random() # A number chosen uniformly at random between 0 and 1
        p = uniform(0, 1)
        if p < slot_ctrs[query_sequence[i]][j]: #This event occurrs with probability that is exactly slot_ctrs[query_sequence[i]][j]
            adv_cbudgets[query_winners[j]] -= query_pay[query_winners[j]]
            revenue += query_pay[query_winners[j]]
            
    print(current_query, query_winners, query_pay, adv_cbudgets)
    
print(revenue)
