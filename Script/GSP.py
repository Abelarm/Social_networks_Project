#!/usr/bin/python

#Implements a GSP auction
def gsp(slot_ctrs, adv_bids):
    
    #Sort advertisers names in decreasing order of their bids
    sort_advs=sorted(adv_bids.keys(), key=adv_bids.__getitem__, reverse=True)
    #Sort slots names in decreasing order of their clickthrough rates
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    #It will contain for each advertiser the name of the slot assigned to him
    adv_slots=dict()
    #It will contain for each advertiser the payment assigned to him
    adv_pays = dict()
    
    for i in range(min(len(sort_advs),len(sort_slots))):
        adv_slots[sort_advs[i]]=sort_slots[i] #The i-th advertiser takes the i-th slot
        if i == len(sort_advs) - 1: #If it is the last advertiser, the payment is 0
            adv_pays[sort_advs[i]]=0
        else: # Else the payment is the slot of the next advertiser
            adv_pays[sort_advs[i]]=adv_bids[sort_advs[i+1]]
    
    return adv_slots, adv_pays

#We implement a possible bot for an advertiser in a repeated GSP auction
#The bot of an advertiser is a program that, given the history of what occurred in previous auctions, suggest a bid for the next auction.
#Specifically, a bot takes in input
#- the name of the advertiser (it allows to use the same bot for multiple advertisers)
#- the value of the advertiser (it is necessary for evaluating the utility of the advertiser)
#- the clickthrough rates of the slots
#- the history
#We assume the history is represented as an array that contains an entry for each time step,
#i.e. history[i] contains the information about the i-th auction.
#In particular, for each time step we have that 
#- history[i]["adv_bids"] returns the advertisers' bids as a dictionary in which the keys are advertisers' names and values are their bids
#- history[i]["adv_slots"] returns the assignment as a dictionary in which the keys are advertisers' names and values are their assigned slots
#- history[i]["adv_pays"] returns the payments as a dictionary in which the keys are advertisers' names and values are their assigned prices

#The bot that we implement here is a symple best_response bot:
#it completely disregards the history except the last step,
#and suggest the bid that will maximize the advertiser utility
#given that the other advertisers do not change their bids.




